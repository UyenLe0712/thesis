# -*- coding: utf-8 -*-
"""P2 — FGRB: bottleneck mềm action/role/zone tiêm vào S1/101 đóng băng, sinh câu trên val.

Theo harness/tai_lieu_2026-09-27/230_ACTION_PROBE_FGRB_CHO_CHAT_LAM_27_9.md mục P2, với hai điểm
đã quyết SAU khi thấy số P1 (khai ở report/207 §9–10):
  · zone dùng lưới 3×3 (`zone_coarse`), không dùng 31 cách viết của regex gốc;
  · ba head khởi tạo từ head P1 đã khớp (harness/fgrb_p1_heads_zone3x3.pt), train tiếp ở lr 1e-4;
    codebook, W, u, b train ở lr 1e-3 như tài liệu 230.

Kiến trúc (khớp sơ đồ mục 2 của 230):
  feat = [trung bình hidden token ảnh ; hidden token cuối của prompt]   (sau norm cuối, như P1)
  P_a, P_r, P_z = softmax(head(chuẩn hoá(feat)))                        (mềm, không argmax)
  z  = W [P_a E_a ; P_r E_r ; P_z E_z]
  h' = h + sigmoid(u·h + b) · z      ở đầu ra norm cuối, mọi vị trí từ token cuối prompt trở đi
W khởi tạo 0 ⇒ trước khi train, FGRB trùng tuyệt đối S1 (--kiem-dong-nhat kiểm điều này).
Qwen + LoRA S1 đóng băng hoàn toàn. Không đọc test.jsonl hay bất kỳ tệp điểm test nào.

Ba giai đoạn (--stage all chạy lần lượt, mỗi giai đoạn nối tiếp được):
  train   4.000 bước P1, 1 epoch, tích luỹ 8 ⇒ 500 lần cập nhật → out/fgrb_params.pt
  gen     sinh greedy 1.567 bước val × ba chế độ: s1 (tắt tiêm) · fgrb · hoanvi (P_role, P_zone
          hoán vị giữa các mẫu val, hoán vị cố định seed 101; train KHÔNG hoán vị)
          → out/gen_{s1,fgrb,hoanvi}.jsonl, ghi dần, chạy lại tự bỏ qua bước đã có
Chấm: harness/p2_doc.py (CPU máy nhà, bộ chấm COCO).

    python p2_fgrb.py --bundle BUNDLE --heads fgrb_p1_heads_zone3x3.pt --out /kaggle/working/p2
"""
import os, sys, json, time, argparse, random

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"      # log ngập từng treo commit Kaggle 7 giờ
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from p1_probe_fgrb import (SYS, BASE, IMAGE_TOKEN_ID, prompt_body, label_role_zone, zone_coarse,
                           load_rows, load_ocr)

IM_START, ASSISTANT_ID, NL_ID = 151644, 77091, 198   # khớp harness/pata_model.py
MODES = ["s1", "fgrb", "hoanvi"]


def key(r):
    return f"{r['episode_id']}_{r['step_id']}"


def parts(model):
    base = model.get_base_model() if hasattr(model, "get_base_model") else model
    vl = base.model
    text = vl.language_model if hasattr(vl, "language_model") else vl
    return base, vl, text


def load_model(bundle, dtype_name):
    import torch
    from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
    import transformers
    from peft import PeftModel
    if dtype_name == "auto":
        if torch.cuda.is_available():
            dt = torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16
        else:
            dt = torch.float32
    else:
        dt = {"fp16": torch.float16, "bf16": torch.bfloat16, "fp32": torch.float32}[dtype_name]
    kw = {("dtype" if int(transformers.__version__.split(".")[0]) >= 5 else "torch_dtype"): dt}
    proc = AutoProcessor.from_pretrained(BASE, min_pixels=200704, max_pixels=1003520)
    dev_map = {"": 0} if torch.cuda.is_available() else {"": "cpu"}   # xem p1_probe_fgrb.load_model
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(BASE, device_map=dev_map, **kw)
    model = PeftModel.from_pretrained(model, os.path.join(bundle, "adapter_s1_seed101"))
    model.eval()
    for p in model.parameters():
        p.requires_grad = False
    print(f"model dtype={dt} device={next(model.parameters()).device}", flush=True)
    return model, proc


def build_fgrb(heads_path, hidden, d_c):
    import torch
    import torch.nn as nn

    class FGRB(nn.Module):
        def __init__(self):
            super().__init__()
            ck = torch.load(heads_path, map_location="cpu")
            assert ck["zone_coarse"], "P2 da chot zone luoi 3x3 — tep head phai train voi --zone-coarse"
            self.classes = (ck["act_classes"], ck["role_classes"], ck["zone_classes"])
            self.register_buffer("mu", ck["mu"].float())
            self.register_buffer("sd", ck["sd"].float())
            feat = self.mu.numel()
            self.head_a = nn.Linear(feat, len(self.classes[0]))
            self.head_r = nn.Linear(feat, len(self.classes[1]))
            self.head_z = nn.Linear(feat, len(self.classes[2]))
            self.head_a.load_state_dict(ck["head_act"])
            self.head_r.load_state_dict(ck["head_role"])
            self.head_z.load_state_dict(ck["head_zone"])
            g = torch.Generator().manual_seed(101)
            self.E_a = nn.Parameter(torch.randn(len(self.classes[0]), d_c, generator=g) * 0.02)
            self.E_r = nn.Parameter(torch.randn(len(self.classes[1]), d_c, generator=g) * 0.02)
            self.E_z = nn.Parameter(torch.randn(len(self.classes[2]), d_c, generator=g) * 0.02)
            self.W = nn.Linear(3 * d_c, hidden, bias=False)
            nn.init.zeros_(self.W.weight)          # bước 0: z = 0 ⇒ trùng S1
            self.u = nn.Parameter(torch.zeros(hidden))
            self.b = nn.Parameter(torch.zeros(()))

        def heads(self, feat):
            x = (feat - self.mu) / self.sd
            return self.head_a(x), self.head_r(x), self.head_z(x)

        def control(self, Pa, Pr, Pz):
            return self.W(torch.cat([Pa @ self.E_a, Pr @ self.E_r, Pz @ self.E_z], -1))

        def gate(self, h):
            return torch.sigmoid(h @ self.u + self.b).unsqueeze(-1)

    return FGRB()


class Tiem:
    """Hook ở norm cuối của mô hình ngôn ngữ. Batch 1.
    Prefill / train (chuỗi dài > 1): tính P từ vị trí prompt (chưa tiêm), tiêm từ token cuối prompt.
    Giải mã từng token: tiêm z đã tính ở prefill."""

    def __init__(self, model, fgrb):
        import torch
        self.torch = torch
        _, _, text = parts(model)
        self.f = fgrb
        self.enabled = False
        self.prompt_len = None      # None ⇒ cả chuỗi là prompt (prefill lúc sinh)
        self.override = None        # (P_r, P_z) thay cho dự đoán — chế độ hoán vị
        self.z = None
        self.logits = None
        self.P = None
        self.gate_mean = None
        self.ratio = None
        self._ids = None
        self._h = [text.embed_tokens.register_forward_hook(self._embed),
                   text.norm.register_forward_hook(self._norm)]

    def _embed(self, mod, args, out):
        self._ids = args[0] if args else None

    def _norm(self, mod, args, out):
        if not self.enabled:
            return out
        torch = self.torch
        h = out[0] if isinstance(out, tuple) else out
        assert h.shape[0] == 1, "Tiem chi ho tro batch 1"
        if h.shape[1] > 1:
            ids = self._ids
            assert ids is not None and ids.shape[1] == h.shape[1], "khong khop input_ids voi hidden"
            L = self.prompt_len or h.shape[1]
            img = ids[0, :L] == IMAGE_TOKEN_ID
            assert bool(img.any()), "khong thay token anh trong prompt"
            feat = torch.cat([h[0, :L][img].float().mean(0), h[0, L - 1].float()])
            la, lr, lz = self.f.heads(feat)
            Pa, Pr, Pz = la.softmax(-1), lr.softmax(-1), lz.softmax(-1)
            if self.override is not None:
                Pr, Pz = (x.to(Pr) for x in self.override)
            self.logits = (la, lr, lz)
            self.P = (Pa.detach(), Pr.detach(), Pz.detach())
            self.z = self.f.control(Pa, Pr, Pz)
            hs = h[0, L - 1:].float()
            g = self.f.gate(hs)
            new = hs + g * self.z
            self.gate_mean = float(g.mean())
            self.ratio = float((g * self.z).norm(dim=-1).mean() / (hs.norm(dim=-1).mean() + 1e-6))
            h2 = torch.cat([h[0, :L - 1], new.to(h.dtype)], 0).unsqueeze(0)
        else:
            assert self.z is not None, "buoc giai ma ma chua co z tu prefill"
            hs = h[0].float()
            h2 = (hs + self.f.gate(hs) * self.z).to(h.dtype).unsqueeze(0)
        return (h2,) + tuple(out[1:]) if isinstance(out, tuple) else h2


def labels_of(r, classes):
    act = (r.get("action") or {}).get("action_type", "?")
    role, zone = label_role_zone(r["target_instruction"])
    zone = zone_coarse(zone)
    return classes[0].index(act), classes[1].index(role), classes[2].index(zone)


def encode(proc, r, ocr, image_dir, with_answer):
    from PIL import Image
    msgs = [{"role": "system", "content": SYS},
            {"role": "user", "content": [
                {"type": "image"},
                {"type": "text", "text": "\n" + prompt_body(
                    {"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))}]}]
    prompt = proc.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    text = prompt + (r["target_instruction"].strip() + "<|im_end|>\n" if with_answer else "")
    img = Image.open(os.path.join(image_dir, r["image"])).convert("RGB")
    return proc(text=[text], images=[img], return_tensors="pt")


def stage_train(args, model, proc, fgrb, tiem, tr_rows, ocr):
    import torch
    import torch.nn.functional as F
    dst = os.path.join(args.out, "fgrb_params.pt")
    if os.path.exists(dst):
        fgrb.load_state_dict(torch.load(dst, map_location="cpu"))
        print(f"Da co {dst}, bo qua train.", flush=True)
        return
    base, _, _ = parts(model)
    dev = next(model.parameters()).device
    lm_w = base.lm_head.weight.detach().float()          # tính logits ở fp32, tránh tràn fp16
    cls = fgrb.classes
    Y = torch.tensor([labels_of(r, cls) for r in tr_rows])

    def cw(y, n):
        c = torch.bincount(y, minlength=n).float()
        w = 1.0 / c.clamp(min=1)
        return (w / w.sum() * n).to(dev)
    wa, wr, wz = cw(Y[:, 0], len(cls[0])), cw(Y[:, 1], len(cls[1])), cw(Y[:, 2], len(cls[2]))

    head_params = [p for n, p in fgrb.named_parameters() if n.startswith("head_")]
    ctrl_params = [p for n, p in fgrb.named_parameters() if not n.startswith("head_")]
    opt = torch.optim.AdamW([{"params": head_params, "lr": args.lr_head},
                             {"params": ctrl_params, "lr": args.lr}], weight_decay=1e-2)
    order = list(range(len(tr_rows)))
    random.Random(101).shuffle(order)
    tiem.enabled = True
    fgrb.train()
    t0 = time.time()
    acc = {"ce": 0.0, "aux": 0.0, "gate": 0.0, "ratio": 0.0, "n": 0}
    opt.zero_grad()
    for i, j in enumerate(order):
        r = tr_rows[j]
        enc = encode(proc, r, ocr, args.bundle, with_answer=True).to(dev)
        ids = enc["input_ids"][0]
        st = [k for k in range(len(ids) - 2) if ids[k] == IM_START and ids[k + 1] == ASSISTANT_ID
              and ids[k + 2] == NL_ID]
        assert st, "khong thay dau luot tro ly"
        a0 = st[-1] + 3
        labels = torch.full_like(ids, -100)
        labels[a0:] = ids[a0:]
        if int(ids[-1]) == NL_ID:
            labels[-1] = -100
        tiem.prompt_len = a0
        out = parts(model)[1](input_ids=enc["input_ids"], attention_mask=enc["attention_mask"],
                              pixel_values=enc["pixel_values"], image_grid_thw=enc["image_grid_thw"],
                              use_cache=False, return_dict=True)
        hs = out.last_hidden_state[0]
        sel = labels[1:] != -100
        logits = hs[:-1][sel].float() @ lm_w.T
        ce = F.cross_entropy(logits, labels[1:][sel])
        la, lr_, lz = tiem.logits
        ya, yr, yz = (Y[j, k].to(dev) for k in range(3))
        aux = (F.cross_entropy(la[None], ya[None], weight=wa) +
               F.cross_entropy(lr_[None], yr[None], weight=wr) +
               F.cross_entropy(lz[None], yz[None], weight=wz))
        loss = (ce + args.aux * aux) / args.accum
        loss.backward()
        acc["ce"] += ce.item(); acc["aux"] += aux.item(); acc["n"] += 1
        acc["gate"] += tiem.gate_mean; acc["ratio"] += tiem.ratio
        if (i + 1) % args.accum == 0 or i == len(order) - 1:
            opt.step()
            opt.zero_grad()
        if (i + 1) % args.log_every == 0 or i == len(order) - 1:
            n = acc["n"]
            el = time.time() - t0
            print(f"  train {i+1}/{len(order)}  ce {acc['ce']/n:.4f}  aux {acc['aux']/n:.4f}  "
                  f"gate {acc['gate']/n:.3f}  |g*z|/|h| {acc['ratio']/n:.4f}  "
                  f"{el/60:.1f} phut, con lai ~{el/(i+1)*(len(order)-i-1)/60:.1f} phut", flush=True)
            acc = {"ce": 0.0, "aux": 0.0, "gate": 0.0, "ratio": 0.0, "n": 0}
    tiem.prompt_len = None
    fgrb.eval()
    torch.save(fgrb.state_dict(), dst)
    print(f"Da ghi {dst}", flush=True)


def stage_gen(args, model, proc, fgrb, tiem, va_rows, ocr, mode):
    import torch
    dst = os.path.join(args.out, f"gen_{mode}.jsonl")
    done = set()
    if os.path.exists(dst):
        done = {json.loads(x)["key"] for x in open(dst, encoding="utf-8")}
    todo = [r for r in va_rows if key(r) not in done]
    print(f"Sinh che do {mode}: da co {len(done)}, con {len(todo)}", flush=True)
    if not todo:
        return
    perm_P = None
    if mode == "hoanvi":
        src = os.path.join(args.out, "gen_fgrb.jsonl")
        rec = {json.loads(x)["key"]: json.loads(x) for x in open(src, encoding="utf-8")}
        keys = [key(r) for r in va_rows]
        assert all(k in rec for k in keys), "hoanvi can gen_fgrb.jsonl day du truoc"
        perm = list(range(len(keys)))
        random.Random(101).shuffle(perm)
        perm_P = {keys[i]: (rec[keys[perm[i]]]["P_role"], rec[keys[perm[i]]]["P_zone"],
                            keys[perm[i]]) for i in range(len(keys))}
    dev = next(model.parameters()).device
    tiem.enabled = mode != "s1"
    tiem.prompt_len = None
    t0 = time.time()
    with open(dst, "a", encoding="utf-8") as f:
        for i, r in enumerate(todo):
            k = key(r)
            tiem.override = None
            if perm_P is not None:
                tiem.override = (torch.tensor(perm_P[k][0], device=dev),
                                 torch.tensor(perm_P[k][1], device=dev))
            tiem.z = None
            enc = encode(proc, r, ocr, args.bundle, with_answer=False).to(dev)
            with torch.no_grad():
                g = model.generate(**enc, max_new_tokens=args.max_new, do_sample=False,
                                   temperature=None, top_p=None, use_cache=True)
            txt = proc.decode(g[0][enc["input_ids"].shape[1]:], skip_special_tokens=True)
            o = {"key": k, "episode_id": r["episode_id"], "step_id": r["step_id"],
                 "raw": txt.strip(), "pred": txt.strip().split("\n")[0].strip(),
                 "gold": r["target_instruction"].strip()}
            if mode != "s1":
                o["P_role"] = [round(x, 5) for x in tiem.P[1].tolist()]
                o["P_zone"] = [round(x, 5) for x in tiem.P[2].tolist()]
                o["gate"] = round(tiem.gate_mean, 4)
                o["ratio"] = round(tiem.ratio, 5)
            if perm_P is not None:
                o["P_from"] = perm_P[k][2]
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
            f.flush()
            if (i + 1) % args.log_every == 0 or i == len(todo) - 1:
                el = time.time() - t0
                print(f"  gen {mode} {i+1}/{len(todo)}  {el/60:.1f} phut, con lai ~"
                      f"{el/(i+1)*(len(todo)-i-1)/60:.1f} phut", flush=True)
    tiem.override = None
    tiem.enabled = False


def kiem_dong_nhat(args, model, proc, tiem, va_rows, ocr):
    """W = 0 ⇒ FGRB phải sinh TRÙNG TỪNG KÝ TỰ với S1. Chạy trước train."""
    import torch
    dev = next(model.parameters()).device
    for r in va_rows[:2]:
        outs = []
        for en in (False, True):
            tiem.enabled = en
            tiem.z = None
            enc = encode(proc, r, ocr, args.bundle, with_answer=False).to(dev)
            with torch.no_grad():
                g = model.generate(**enc, max_new_tokens=args.max_new, do_sample=False,
                                   temperature=None, top_p=None, use_cache=True)
            outs.append(proc.decode(g[0][enc["input_ids"].shape[1]:], skip_special_tokens=True))
        tiem.enabled = False
        print(f"  kiem dong nhat {key(r)}: s1={outs[0]!r} | fgrb(W=0)={outs[1]!r}", flush=True)
        assert outs[0] == outs[1], "W=0 ma FGRB khac S1 — hook sai, DUNG LAI"
    print("Kiem dong nhat DAT: W=0 thi FGRB trung S1 tung ky tu.", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True, help="thu muc fgrb-p1-bundle (images/, ocr.jsonl, "
                     "p1_train_rows.jsonl, p1_val_rows.jsonl, adapter_s1_seed101/)")
    ap.add_argument("--heads", required=True, help="fgrb_p1_heads_zone3x3.pt")
    ap.add_argument("--out", default="/kaggle/working/p2")
    ap.add_argument("--stage", default="all", choices=["all", "train", "gen"])
    ap.add_argument("--modes", default=",".join(MODES))
    ap.add_argument("--d-c", type=int, default=256)
    ap.add_argument("--lr", type=float, default=1e-3, help="codebook, W, u, b (230: 1e-3)")
    ap.add_argument("--lr-head", type=float, default=1e-4, help="ba head, khoi tao tu P1")
    ap.add_argument("--aux", type=float, default=1.0, help="trong so CE cua ba head")
    ap.add_argument("--accum", type=int, default=8)
    ap.add_argument("--max-new", type=int, default=96)
    ap.add_argument("--dtype", default="auto", choices=["auto", "fp16", "bf16", "fp32"])
    ap.add_argument("--log-every", type=int, default=100)
    ap.add_argument("--limit", type=int, default=0,
                    help="CHI de thu: cat train/val con n dong. Co --limit thi so ra KHONG dung de phan P2")
    args = ap.parse_args()

    import torch
    torch.manual_seed(101)
    if args.limit:
        args.out = args.out.rstrip("/") + f"_limit{args.limit}"
    os.makedirs(args.out, exist_ok=True)
    tr_rows = load_rows(os.path.join(args.bundle, "p1_train_rows.jsonl"))
    va_rows = load_rows(os.path.join(args.bundle, "p1_val_rows.jsonl"))
    ocr = load_ocr(os.path.join(args.bundle, "ocr.jsonl"))
    print(f"train={len(tr_rows)} val={len(va_rows)} ocr_keys={len(ocr)} out={args.out}", flush=True)
    if args.limit:
        print(f"⚠️  --limit {args.limit}: LUOT THU, khong phai P2 that", flush=True)
        tr_rows, va_rows = tr_rows[:args.limit], va_rows[:args.limit]
    else:
        assert len(tr_rows) == 4000 and len(va_rows) == 1567
        assert len(ocr) > 0, "thieu ocr.jsonl — prompt S1 co OCR, bo OCR la doi dau vao"

    model, proc = load_model(args.bundle, args.dtype)
    hidden = parts(model)[2].embed_tokens.weight.shape[1]
    dev = next(model.parameters()).device
    fgrb = build_fgrb(args.heads, hidden, args.d_c).to(dev)
    n_tr = sum(p.numel() for p in fgrb.parameters())
    print(f"FGRB: hidden={hidden} d_c={args.d_c} tham so hoc={n_tr:,} "
          f"lop={[len(c) for c in fgrb.classes]}", flush=True)
    tiem = Tiem(model, fgrb)

    if args.stage in ("all", "train"):
        if not os.path.exists(os.path.join(args.out, "fgrb_params.pt")):
            kiem_dong_nhat(args, model, proc, tiem, va_rows, ocr)
        stage_train(args, model, proc, fgrb, tiem, tr_rows, ocr)
    if args.stage in ("all", "gen"):
        if args.stage == "gen" and args.modes != "s1":      # chế độ s1 tắt tiêm, không cần tham số
            fgrb.load_state_dict(torch.load(os.path.join(args.out, "fgrb_params.pt"), map_location="cpu"))
        fgrb.eval()
        for m in args.modes.split(","):
            stage_gen(args, model, proc, fgrb, tiem, va_rows, ocr, m)
    print("XONG. Tai ve cac tep gen_*.jsonl + fgrb_params.pt trong", args.out, flush=True)


if __name__ == "__main__":
    main()
