# -*- coding: utf-8 -*-
"""
PATA · mô hình C1 (report/185 §4, §5). Không chạy gì khi import — chỉ định nghĩa.

Ba mảnh gắn vào Qwen2.5-VL-3B có sẵn, KHÔNG sửa mã transformers:

  1. TARGET token. Thêm chuỗi đặc biệt "<TARGET>" vào tokenizer (id 151665, nằm trong
     151.936 hàng embedding sẵn có ⇒ không đổi cỡ ma trận). Véc-tơ embedding của nó là một
     tham số RIÊNG `tvec` (khởi tạo = trung bình embedding từ vựng), cắm vào bằng hook trên
     `embed_tokens`. Không mở khoá cả ma trận embedding.

  2. Localizer (sau block `inject`, mặc định 17 — §4 "preregistered midpoint heuristic"):
         q  = Pq(LN(hT))       ui = Pv(LN(vi))       α = softmax(q·u / √d)
     Loss KL(p_target ‖ α) trên các ô thị giác giao box (§5).

  3. Bridge:  hT' = hT + sigmoid(g) · Wo(Σ αi vi),  Wo = 0, g = −2 lúc khởi tạo.
     Thay hT bằng hT' NGAY TRONG vòng decoder (hook trên block `inject`) ⇒ block 18–35 và
     KV-cache của chúng thấy TARGET đã được điều kiện hoá. `bridge_enabled=False` là C0-Loc.

Vì sao hook chứ không bọc module: bọc sẽ đổi tên tham số LoRA của block 17
("layers.17.layer.self_attn…") và adapter Stage S nạp vào sẽ lệch khoá trong im lặng.
Hook chạy BÊN TRONG gradient checkpointing ⇒ BẮT BUỘC `use_reentrant=False` (xem
`enable_gc`); unit test 6 kiểm gradient đi qua khi bật checkpointing.

Ba tham số mới (Pq, Pv, Wo, gate, LN, tvec) giữ ở FP32, không lượng tử (§4).
d_k = 2048 (bằng hidden) là lựa chọn của dự án, ghi vào manifest.
"""
import math, contextlib
import torch
import torch.nn as nn
import torch.nn.functional as F

TARGET = "<TARGET>"
IMAGE_TOKEN_ID = 151655
IM_START = 151644
ASSISTANT_ID = 77091
NL_ID = 198
MIN_PIX, MAX_PIX = 200704, 1003520          # khớp train_config.yaml và infer_branch.py


# ─────────────────────────────────────────────────────────────── tháo lớp mô hình
def parts(model):
    """Trả (base_causal_lm, vl_model, text_model) cho cả PeftModel lẫn mô hình trần,
    cho cả transformers 4.5x lẫn 5.x (cùng tên thuộc tính từ 4.52)."""
    base = model.get_base_model() if hasattr(model, "get_base_model") else model
    vl = base.model
    text = vl.language_model if hasattr(vl, "language_model") else vl
    return base, vl, text


def enable_gc(model):
    """Gradient checkpointing KHÔNG reentrant. Bản reentrant chạy forward trong no_grad nên α
    tính trong hook sẽ không có gradient — KL vẫn in ra số đẹp mà localizer không học gì."""
    base, _, _ = parts(model)
    base.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    base.config.use_cache = False


def load_base(tiny=False, revision="main", attn="sdpa", quant=True):
    """Nạp (processor, mô hình, inject, d_k, compute_dtype) — MỘT chỗ duy nhất cho train/eval/test.
    Thật: QLoRA NF4 double-quant, compute BF16 trên Ampere+ (A100/L4), FP16 trên T4."""
    from transformers import AutoProcessor
    base_id = "Qwen/Qwen2.5-VL-3B-Instruct"
    if tiny:
        import pata_test as PT
        proc = AutoProcessor.from_pretrained(base_id, min_pixels=28 * 28 * 16, max_pixels=28 * 28 * 64)
        return proc, PT.tiny_model(0), 1, 32, torch.float32
    import transformers
    from transformers import Qwen2_5_VLForConditionalGeneration, BitsAndBytesConfig
    cdt = torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16
    kw = {("dtype" if int(transformers.__version__.split(".")[0]) >= 5 else "torch_dtype"): cdt}
    if quant:
        kw["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=cdt,
            bnb_4bit_use_double_quant=True)
    proc = AutoProcessor.from_pretrained(base_id, min_pixels=MIN_PIX, max_pixels=MAX_PIX)
    m = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        base_id, revision=revision, device_map={"": 0}, attn_implementation=attn, **kw)
    print(f"[mô hình] {base_id}@{revision} · {'NF4' if quant else str(cdt)} · compute {cdt} · "
          f"attn {attn} · transformers {transformers.__version__}", flush=True)
    return proc, m, 17, 2048, cdt


# ─────────────────────────────────────────────────────────────── đầu PATA
class PataHeads(nn.Module):
    def __init__(self, hidden, d_k=2048, gate_init=-2.0):
        super().__init__()
        self.ln_q = nn.LayerNorm(hidden)
        self.ln_v = nn.LayerNorm(hidden)
        self.pq = nn.Linear(hidden, d_k)
        self.pv = nn.Linear(hidden, d_k)
        self.wo = nn.Linear(hidden, hidden, bias=False)
        nn.init.zeros_(self.wo.weight)                        # §4: Wo zero-init
        self.gate = nn.Parameter(torch.tensor(float(gate_init)))   # sigmoid(−2) ≈ 0,119
        self.tvec = nn.Parameter(torch.zeros(hidden))        # ghi đè bằng mean vocab ở attach()
        self.d_k = d_k

    def localize(self, hT, V):
        """hT (D,), V (N,D) → logα (N,). Tính FP32 — tắt autocast để Linear không bị hạ xuống BF16."""
        with torch.autocast(hT.device.type, enabled=False):
            return self._localize(hT, V)

    def _localize(self, hT, V):
        q = self.pq(self.ln_q(hT.float()))
        u = self.pv(self.ln_v(V.float()))
        return torch.log_softmax(u @ q / math.sqrt(self.d_k), dim=-1)

    def bridge(self, alpha, V):
        with torch.autocast(V.device.type, enabled=False):
            return self._bridge(alpha, V)

    def _bridge(self, alpha, V):
        z = alpha.float() @ V.float()
        return torch.sigmoid(self.gate) * self.wo(z)


class Pata:
    """Giữ trạng thái giữa các hook của MỘT lượt forward.

    Cờ điều khiển (đặt trước forward):
      bridge_enabled   False ⇒ C0-Loc / "disable bridge" (§8 điều 4)
      alpha_override   list[Tensor|None] theo mẫu ⇒ thay α khi tính z (swap / random-pool, §8 điều 5)
    Kết quả để lấy sau forward:
      last = list[dict] theo mẫu: logalpha, resid_ratio, n_vis, tpos
    """

    def __init__(self, model, tokenizer, inject=17, d_k=2048, gate_init=-2.0, device=None):
        self.model = model
        base, vl, text = parts(model)
        self.text = text
        n_new = tokenizer.add_special_tokens({"additional_special_tokens": [TARGET]})
        self.tid = tokenizer.convert_tokens_to_ids(TARGET)
        emb = text.embed_tokens.weight
        assert self.tid < emb.shape[0], "id TARGET vượt cỡ embedding — cần resize, không dự tính"
        self.inject = inject
        assert 0 <= inject < len(text.layers)
        hidden = emb.shape[1]
        dev = device or emb.device
        self.heads = PataHeads(hidden, d_k, gate_init).to(dev, torch.float32)
        with torch.no_grad():
            n_vocab = self.tid if n_new else len(tokenizer) - 1
            self.heads.tvec.copy_(emb[:n_vocab].float().mean(0))   # §4: mean vocabulary
        self.bridge_enabled = True
        self.alpha_override = None
        self._ids = None
        self.last = []
        self._h = [text.embed_tokens.register_forward_hook(self._embed_hook),
                   text.layers[inject].register_forward_hook(self._layer_hook)]

    # hook 1 — cắm tvec vào vị trí TARGET, ghi lại input_ids của chunk hiện tại
    def _embed_hook(self, mod, args, out):
        ids = args[0] if args else None
        self._ids = ids
        if ids is None:
            return out
        m = ids == self.tid
        if not m.any():
            return out
        t = self.heads.tvec.to(out.dtype)
        return torch.where(m.unsqueeze(-1), t.expand_as(out), out)

    # hook 2 — localizer + bridge sau block `inject`
    def _layer_hook(self, mod, args, out):
        h = out[0] if isinstance(out, tuple) else out
        ids = self._ids
        if ids is None or ids.shape[1] != h.shape[1]:
            return out                                   # bước giải mã từng token: không có TARGET
        self.last = []
        adds = []
        for b in range(h.shape[0]):
            tpos = (ids[b] == self.tid).nonzero().flatten()
            vis = (ids[b] == IMAGE_TOKEN_ID).nonzero().flatten()
            if len(tpos) == 0 or len(vis) == 0:
                self.last.append(None); adds.append(None); continue
            t = int(tpos[0])
            V = h[b, vis]
            logalpha = self.heads.localize(h[b, t], V)
            rec = {"logalpha": logalpha, "tpos": t, "n_vis": len(vis)}
            add = None
            if self.bridge_enabled:
                a = logalpha.exp()
                if self.alpha_override is not None and self.alpha_override[b] is not None:
                    a = self.alpha_override[b].to(a)
                add = self.heads.bridge(a, V)
                rec["resid_ratio"] = (add.norm() / (h[b, t].float().norm() + 1e-6)).detach()
            self.last.append(rec)
            adds.append((t, add))
        if not any(x is not None and x[1] is not None for x in adds):
            return out
        delta = torch.zeros_like(h)
        for b, x in enumerate(adds):
            if x is not None and x[1] is not None:
                delta[b, x[0]] = x[1].to(h.dtype)
        h2 = h + delta
        return (h2,) + tuple(out[1:]) if isinstance(out, tuple) else h2

    def remove(self):
        for x in self._h:
            x.remove()

    @contextlib.contextmanager
    def truncated(self):
        """Stage H chỉ cần tới block `inject`: cắt bỏ block sau đó trong lúc forward (tiết kiệm
        ~một nửa phép tính). Các block vẫn là CÙNG module, chỉ bỏ khỏi vòng lặp."""
        full = self.text.layers
        self.text.layers = nn.ModuleList(list(full)[: self.inject + 1])
        try:
            yield
        finally:
            self.text.layers = full

    # ── lưu / nạp ───────────────────────────────────────────────────────────
    def state_dict(self):
        return {"heads": self.heads.state_dict(), "tid": self.tid, "inject": self.inject,
                "d_k": self.heads.d_k}

    def load_state_dict(self, sd):
        assert sd["tid"] == self.tid and sd["inject"] == self.inject and sd["d_k"] == self.heads.d_k
        self.heads.load_state_dict(sd["heads"])


# ─────────────────────────────────────────────────────────────── đích patch (§4 "Patch target")
def patch_target(box, w, h, img_w, img_h, grid_thw, merge=2, patch=14):
    """Phân phối đích trên các ô thị giác SAU spatial merge, thứ tự raster.

    box        [x1,y1,x2,y2] theo toạ độ bản ghi (w×h)
    img_w/h    cỡ ảnh thật đưa vào processor (thường = w×h, nhưng đổi tỉ lệ cho chắc)
    grid_thw   (t, gh, gw) đọc từ processor — KHÔNG suy từ cỡ ảnh gốc
    Ảnh sau resize = (gh·14) × (gw·14); mỗi ô merge là 28×28 px. Ô là dương nếu GIAO box.
    """
    t, gh, gw = [int(x) for x in grid_thw]
    assert t == 1, "chỉ ảnh tĩnh"
    mh, mw = gh // merge, gw // merge
    cell = patch * merge
    sx = (gw * patch) / img_w * (img_w / w)
    sy = (gh * patch) / img_h * (img_h / h)
    x1, y1, x2, y2 = box[0] * sx, box[1] * sy, box[2] * sx, box[3] * sy
    cs = torch.arange(mw, dtype=torch.float64) * cell
    rs = torch.arange(mh, dtype=torch.float64) * cell
    colhit = (cs < x2) & (cs + cell > x1)
    rowhit = (rs < y2) & (rs + cell > y1)
    m = (rowhit[:, None] & colhit[None, :]).flatten().float()
    if m.sum() == 0:                                 # box suy biến (rộng 0): lấy ô chứa tâm
        cx = min(int(((x1 + x2) / 2) // cell), mw - 1)
        cy = min(int(((y1 + y2) / 2) // cell), mh - 1)
        m[cy * mw + cx] = 1.0
    return m / m.sum()


def kl_target_alpha(p, logalpha):
    """KL(p ‖ α) = Σ_{p>0} p (log p − log α)."""
    p = p.to(logalpha)
    pos = p > 0
    return (p[pos] * (p[pos].log() - logalpha[pos])).sum()


# ─────────────────────────────────────────────────────────────── dựng mẫu
def build_example(proc, sys_text, body, sentence, image, with_target, tid=None):
    """Chuỗi hội thoại giống hệt infer_branch.py lúc chấm, cộng <TARGET> ở đầu lượt trợ lý.
    Trả input_ids, labels (−100 ngoài câu và ở chính TARGET), pixel_values, image_grid_thw."""
    msgs = [{"role": "system", "content": sys_text},
            {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body}]}]
    prompt = proc.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    text = prompt + (TARGET if with_target else "") + sentence + "<|im_end|>\n"
    enc = proc(text=[text], images=[image], return_tensors="pt")
    ids = enc["input_ids"][0]
    st = [i for i in range(len(ids) - 2) if ids[i] == IM_START and ids[i + 1] == ASSISTANT_ID
          and ids[i + 2] == NL_ID]
    assert st, "không thấy đầu lượt trợ lý"
    a0 = st[-1] + 3
    labels = torch.full_like(ids, -100)
    labels[a0:] = ids[a0:]
    if with_target:
        assert int(ids[a0]) == tid, "TARGET không nằm ngay đầu lượt trợ lý"
        labels[a0] = -100
    # bỏ "\n" cuối sau <|im_end|> khỏi loss (khớp mặc định lượt trợ lý kết thúc ở im_end)
    if int(ids[-1]) == NL_ID:
        labels[-1] = -100
    return {"input_ids": ids, "labels": labels, "pixel_values": enc["pixel_values"],
            "image_grid_thw": enc["image_grid_thw"][0]}


def prompt_only(proc, sys_text, body, image, with_target):
    msgs = [{"role": "system", "content": sys_text},
            {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body}]}]
    return proc.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True) + \
        (TARGET if with_target else "")


LORA_REGEX = r"^(?!.*visual).*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj)$"


def add_lora(model, r=8, alpha=16, dropout=0.05):
    """LoRA 7 khối NGÔN NGỮ (§6 Stage S). Regex loại `visual` vì MLP của tháp thị giác cũng
    tên gate/up/down_proj — thiếu vế này là mở băng thị giác trong im lặng (bài học VIS-SFT)."""
    from peft import LoraConfig, get_peft_model
    cfg = LoraConfig(r=r, lora_alpha=alpha, lora_dropout=dropout, target_modules=LORA_REGEX,
                     bias="none", task_type="CAUSAL_LM")
    return get_peft_model(model, cfg)


def make_item(proc, rec, root, with_target, tid, img_open=None):
    """Bản ghi pata/*.jsonl → mẫu đã mã hoá + đích patch (nếu có box và có TARGET)."""
    import os, sys
    from PIL import Image
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    from build_branch_data import prompt_body, SYS
    ocr = rec.get("_ocr")
    img = (img_open or (lambda p: Image.open(p).convert("RGB")))(os.path.join(root, rec["image"]))
    body = prompt_body({"goal": rec["goal"], "history": rec.get("history") or []}, ocr)
    ex = build_example(proc, SYS, body, rec["target_instruction"].strip(), img, with_target, tid)
    ex["ptarget"] = None
    # ⛔ theo `kl_ok`, KHÔNG theo `box`: box lớn (≥ 25% màn) vẫn giữ trong bản ghi nhưng tắt KL.
    if with_target and rec.get("box") and rec.get("kl_ok", True):
        ex["ptarget"] = patch_target(rec["box"], rec["w"], rec["h"], img.width, img.height,
                                     ex["image_grid_thw"])
        n_vis = int((ex["input_ids"] == IMAGE_TOKEN_ID).sum())
        assert n_vis == ex["ptarget"].numel(), f"ô thị giác {n_vis} ≠ đích {ex['ptarget'].numel()}"
    ex["meta"] = {"episode_id": rec["episode_id"], "step_id": rec["step_id"]}
    return ex


def collate(batch, pad_id):
    L = max(len(x["input_ids"]) for x in batch)
    B = len(batch)
    ids = torch.full((B, L), pad_id, dtype=torch.long)
    lab = torch.full((B, L), -100, dtype=torch.long)
    att = torch.zeros((B, L), dtype=torch.long)
    for i, x in enumerate(batch):                    # đệm PHẢI khi dạy
        n = len(x["input_ids"])
        ids[i, :n] = x["input_ids"]; lab[i, :n] = x["labels"]; att[i, :n] = 1
    out = {"input_ids": ids, "labels": lab, "attention_mask": att,
           "pixel_values": torch.cat([x["pixel_values"] for x in batch]),
           "image_grid_thw": torch.stack([x["image_grid_thw"] for x in batch])}
    out["ptarget"] = [x.get("ptarget") for x in batch]
    out["meta"] = [x.get("meta") for x in batch]
    return out


# ─────────────────────────────────────────────────────────────── một bước tính loss
def forward_losses(model, pata, batch, *, need_ce=True, need_kl=True, truncate=False):
    """Trả (ce_sum, n_tok, kl_sum, n_kl, extra). Tổng chứ không trung bình: người gọi chia cho
    tổng của CẢ lô hiệu dụng (§2: KL trung bình trên số mẫu eligible của lô, không chia cả lô).

    CE chỉ gọi lm_head ở vị trí có nhãn (≈15 token/mẫu) thay vì cả chuỗi ~1.500 token ⇒ không
    dựng bảng logits 151.936 × chuỗi, lý do P4 từng tràn bộ nhớ (CLAUDE.md "bảng logits")."""
    base, vl, text = parts(model)
    dev = text.embed_tokens.weight.device
    kw = {k: batch[k].to(dev) for k in ("input_ids", "attention_mask", "pixel_values", "image_grid_thw")}
    ctx = pata.truncated() if truncate else contextlib.nullcontext()
    if pata is not None:
        pata.last = []
    with ctx:
        out = vl(**kw, use_cache=False, return_dict=True)
    hs = out.last_hidden_state
    ce_sum = hs.new_zeros((), dtype=torch.float32); n_tok = 0
    if need_ce and not truncate:
        lab = batch["labels"].to(dev)
        sel = lab[:, 1:] != -100
        h_sel = hs[:, :-1][sel]
        logits = base.lm_head(h_sel).float()
        ce_sum = F.cross_entropy(logits, lab[:, 1:][sel], reduction="sum")
        n_tok = int(sel.sum())
    kl_sum = torch.zeros((), device=dev); n_kl = 0
    extra = {"mass": [], "hit": [], "resid": []}
    for b, rec in enumerate(pata.last if pata is not None else []):
        if rec is None:
            continue
        if "resid_ratio" in rec:
            extra["resid"].append(float(rec["resid_ratio"]))
        p = batch["ptarget"][b]
        if p is None:
            continue
        la = rec["logalpha"]
        assert la.shape[0] == p.shape[0], f"số ô thị giác {la.shape[0]} ≠ đích {p.shape[0]}"
        if need_kl:
            kl_sum = kl_target_alpha(p, la) + kl_sum
            n_kl += 1
        with torch.no_grad():
            a = la.exp()
            pos = p.to(a) > 0
            extra["mass"].append(float(a[pos].sum()))
            extra["hit"].append(float(pos[int(a.argmax())]))
    return ce_sum, n_tok, kl_sum, n_kl, extra
