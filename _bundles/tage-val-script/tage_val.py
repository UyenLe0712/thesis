# -*- coding: utf-8 -*-
"""TAGE — kiểm thử trên val C1 trước khi chạy thật (file 265, 2/10/2026).

Type-Aware Grounded Editor: ck500 viết câu nháp → (bộ định vị chỉ điểm) → cắt vùng quanh điểm →
bộ biên tập (LoRA riêng trên S1 đã hoà) nhìn màn + vùng + câu nháp rồi viết lại → cổng giữ/sửa
(tính offline ở `tage_doc.py`).

Chạy từ thư mục có grpo_spice.py và build_branch_data.py.

python tage_val.py --selftest --bundle B --neg tage_neg.jsonl --c1 C1 --out selftest
python tage_val.py --merge --bundle B --merged M
python tage_val.py --make-drafts --bundle B --merged M --ckpt CK500 --out drafts_train.jsonl
python tage_val.py --train-editor --bundle B --merged M --neg N --drafts D --crop gold --out ed_gold
python tage_val.py --edit-val --bundle B --merged M --neg N --c1 C1 --ck500-pred P --editor ed_gold --crop gold --out pred_gold.jsonl
python tage_val.py --train-locator --bundle B --merged M [--drafts D --with-draft] --out loc_d
python tage_val.py --locate-val --bundle B --merged M --c1 C1 --ck500-pred P --locator loc_d [--with-draft] --out loc_val_d.jsonl
python tage_val.py --edit-val ... --editor ed_gold --crop pred --points loc_val_d.jsonl --out pred_pred.jsonl

Không đọc test. Không dùng UGround trong train hay suy luận; UGround chỉ chấm qua score_run.py.
"""

import os, re, sys, json, time, math, random, argparse, collections

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_branch_data import SYS  # noqa: E402
from grpo_spice import BASE, SEED, SEED_C1, PIX, nap_ocr, body_of, merge, _kw  # noqa: E402

TAPT = ("click", "long_press")
CROP_FRAC = 0.4          # cạnh vùng cắt = 40% bề ngang ảnh, tâm tại điểm
CROP_PX = 448            # 448² = min_pixels của PIX ⇒ đúng 256 token ảnh
TOL = 140                # ±14% theo từng trục, thang 0–1000 (vế hit_disk của exec)
LORA_RE = r"^(?!.*visual).*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj)$"
STOP = {"the", "a", "an", "on", "in", "of", "to", "and", "or", "for", "at", "option", "button", "icon",
        "click", "tap", "select", "open", "text", "tab", "menu", "bar"}

DAN_SUA_CROP = "Ảnh thứ hai phóng to vùng quanh chỗ cần chạm. Viết lại câu hướng dẫn cho đúng phần tử ở vùng đó."
DAN_SUA_KHONG = "Viết lại câu hướng dẫn nếu câu nháp chưa đúng."
DAN_DINH_VI = "Chỉ ra điểm cần chạm, trả lời dạng (x, y) theo thang 0 đến 1000."
SO = re.compile(r"(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)")


# ───────────────────────────── dữ liệu ─────────────────────────────

def key(r):
    return (r["episode_id"], r["step_id"])


def la_click(r):
    a = r.get("action") or {}
    return a.get("action_type") in TAPT and "x" in a


def nap_neg(p):
    return {key(d): d for d in map(json.loads, open(p, encoding="utf-8"))}


def hang_train(bundle):
    """Bước click train của fgrb-p1-bundle, bỏ mọi episode có mặt ở val (như grpo_spice.dung_hang)."""
    tr = [json.loads(l) for l in open(os.path.join(bundle, "p1_train_rows.jsonl"), encoding="utf-8")]
    va = [json.loads(l) for l in open(os.path.join(bundle, "p1_val_rows.jsonl"), encoding="utf-8")]
    assert len(tr) == 4000 and len(va) == 1567, (len(tr), len(va))
    ev = {r["episode_id"] for r in va}
    rows = [r for r in tr if la_click(r) and r["episode_id"] not in ev
            and (r.get("target_instruction") or "").strip()]
    assert not {r["episode_id"] for r in rows} & ev
    return rows


def hang_val(bundle, c1_path, n=None):
    """400 bước C1 đúng thứ tự c1_mau.jsonl; trả về bước click (249) kèm bản ghi C1."""
    va = [json.loads(l) for l in open(os.path.join(bundle, "p1_val_rows.jsonl"), encoding="utf-8")]
    rows = random.Random(SEED_C1).sample(va, 400)
    C1 = [json.loads(l) for l in open(c1_path, encoding="utf-8")]
    assert [key(r) for r in rows] == [key(d) for d in C1], "⛔ thứ tự 400 bước lệch c1_mau.jsonl"
    cl = [r for r in rows if la_click(r)]
    return rows, (cl[:n] if n else cl)


def chuan(r, x, y):
    return round(1000 * x / r["w"]), round(1000 * y / r["h"])


def tuyet_doi(r, xn, yn):
    return xn * r["w"] / 1000, yn * r["h"] / 1000


def trong_vung(r, x, y, gx, gy):
    h = CROP_FRAC * r["w"] / 2
    return abs(x - gx) <= h and abs(y - gy) <= h


def diem_nhieu(r, neg, ocr, cho_trong=False):
    """Điểm cho vùng cắt nhiễu: phần tử lân cận cùng vai trò, không thì mục OCR gần nhất nằm ngoài vùng
    vàng, không nữa thì điểm đối xứng qua tâm màn. Trả (x, y, nguồn).

    Lúc train (`cho_trong=True`) nhận cả phần tử lân cận nằm trong vùng vàng — vùng cắt vẫn đặt phần tử
    đó ở tâm, đó là vế âm khó. Lúc chạy nhánh `neg` trên val chỉ nhận phần tử ngoài vùng vàng (file 265
    §2.2), để phép thử "bộ biên tập có đọc vùng cắt không" không bị hai vùng gần trùng nhau làm nhoè."""
    gx, gy = r["action"]["x"], r["action"]["y"]
    d = neg.get(key(r)) or {}
    p = d.get("point_neg_abs")
    if p and (cho_trong or not trong_vung(r, p[0], p[1], gx, gy)):
        return p[0], p[1], "lan_can"
    best = None
    for it in (ocr.get(r["image"]) or {}).get("items", []):
        x, y = it.get("cx"), it.get("cy")
        if x is None or trong_vung(r, x, y, gx, gy):
            continue
        dd = (x - gx) ** 2 + (y - gy) ** 2
        if best is None or dd < best[0]:
            best = (dd, x, y)
    if best:
        return best[1], best[2], "ocr"
    return r["w"] - gx, r["h"] - gy, "doi_xung"


def cat_vung(img, r, x, y):
    """Vùng vuông cạnh 40% bề ngang, tâm (x, y) theo toạ độ gốc; ảnh có thể nhỏ hơn toạ độ gốc
    (quy đổi theo tỉ lệ). Ra ngoài mép thì đệm đen để điểm luôn ở tâm. Đổi cỡ 448×448."""
    from PIL import Image
    sx, sy = img.width / r["w"], img.height / r["h"]
    px, py = x * sx, y * sy
    px, py = min(max(px, 0), img.width - 1), min(max(py, 0), img.height - 1)  # nhãn hỏng ngoài ảnh (ep14503_s1: x=2163 > 1080)
    s = max(1, round(CROP_FRAC * img.width))
    x0, y0 = round(px - s / 2), round(py - s / 2)
    nen = Image.new("RGB", (s, s))
    nen.paste(img.crop((max(0, x0), max(0, y0), min(img.width, x0 + s), min(img.height, y0 + s))),
              (max(0, -x0), max(0, -y0)))
    return nen.resize((CROP_PX, CROP_PX), Image.BICUBIC)


def lam_hong(cau, d):
    """Thay tên phần tử đúng trong câu bằng tên phần tử lân cận cùng vai trò. Không thay được → None.

    Khớp trọn tên (không phân biệt hoa thường); không có thì khớp đoạn từ liên tiếp dài nhất của tên
    (bỏ đoạn chỉ gồm từ chung chung như 'option', 'button')."""
    if not d or not d.get("name") or not d.get("name_neg"):
        return None
    ten, moi = d["name"].strip(), d["name_neg"].strip()
    if not ten or not moi or ten.lower() == moi.lower():
        return None
    i = cau.lower().find(ten.lower())
    if i >= 0:
        return cau[:i] + moi + cau[i + len(ten):]
    tu = re.findall(r"[A-Za-z0-9'&]+", ten)
    for L in range(len(tu), 0, -1):
        for j in range(len(tu) - L + 1):
            doan = tu[j:j + L]
            if all(w.lower() in STOP for w in doan) or sum(len(w) for w in doan) < 3:
                continue
            m = re.search(r"\b" + r"\W+".join(map(re.escape, doan)) + r"\b", cau, re.I)
            if m:
                return cau[:m.start()] + moi + cau[m.end():]
    return None


def doc_toa_do(s):
    m = SO.search(s or "")
    if not m:
        return None
    x, y = float(m.group(1)), float(m.group(2))
    if not (0 <= x <= 1000 and 0 <= y <= 1000):
        return None
    return x, y


# ───────────────────────────── mô hình ─────────────────────────────

def _dtype():
    import torch
    if not torch.cuda.is_available():
        return torch.float32
    return torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16


def _dev():
    import torch
    return "cuda" if torch.cuda.is_available() else "cpu"


def nap_mo_hinh(a):
    import torch
    from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
    dt = _dtype()
    proc = AutoProcessor.from_pretrained(BASE, **PIX)
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        a.merged, device_map={"": 0} if _dev() == "cuda" else None, **_kw(dt))
    ten = torch.cuda.get_device_name(0) if _dev() == "cuda" else "CPU"
    print(f"[nạp] {a.merged} · dtype {dt} · {ten}", flush=True)
    return proc, model, dt


def cau_nhac(proc, body, imgs):
    msg = [{"role": "system", "content": SYS},
           {"role": "user", "content": [{"type": "image"} for _ in imgs] + [{"type": "text", "text": "\n" + body}]}]
    return proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)


def mau_vao(proc, body, imgs, tra_loi=None):
    """Đầu vào cho một mẫu. Có `tra_loi` thì kèm nhãn, che toàn bộ phần câu nhắc.

    Che nhãn bằng độ dài câu nhắc đã token hoá riêng — chỉ đúng khi câu nhắc là TIỀN TỐ của chuỗi đầy
    đủ, nên kiểm thẳng điều đó (lệch là dừng, không suy đoán)."""
    import torch
    p = cau_nhac(proc, body, imgs)
    if tra_loi is None:
        return proc(text=[p], images=imgs, return_tensors="pt"), None
    P = proc(text=[p], images=imgs, return_tensors="pt")
    F = proc(text=[p + tra_loi + "<|im_end|>"], images=imgs, return_tensors="pt")
    L = P["input_ids"].shape[1]
    assert torch.equal(F["input_ids"][0, :L], P["input_ids"][0]), "⛔ câu nhắc không là tiền tố — che nhãn sai"
    lab = F["input_ids"].clone()
    lab[:, :L] = -100
    return F, lab


def nll_tb(model, inp, lab):
    """NLL trung bình mỗi token của phần trả lời (nat/token)."""
    import torch
    out = model(**inp)
    lg = out.logits[:, :-1].float()
    y = lab[:, 1:]
    return torch.nn.functional.cross_entropy(lg.reshape(-1, lg.shape[-1]), y.reshape(-1), ignore_index=-100)


def len_thiet_bi(inp, lab, dev):
    inp = {k: (v.to(dev) if hasattr(v, "to") else v) for k, v in inp.items()}
    return inp, (lab.to(dev) if lab is not None else None)


def sinh(model, proc, inp, n_tok, **kw):
    import torch
    L = inp["input_ids"].shape[1]
    with torch.no_grad():
        g = model.generate(**inp, max_new_tokens=n_tok, use_cache=True, **kw)
    return [proc.decode(x[L:], skip_special_tokens=True).strip() for x in g]


def gan_lora(model, a):
    import torch
    from peft import LoraConfig, get_peft_model
    lc = LoraConfig(r=a.r, lora_alpha=2 * a.r, lora_dropout=0.05, bias="none",
                    target_modules=LORA_RE, task_type="CAUSAL_LM")
    model = get_peft_model(model, lc)
    ntr = 0
    for n, p in model.named_parameters():
        if p.requires_grad:
            if "visual" in n:
                raise SystemExit(f"⛔ tháp thị giác đang học: {n}")
            if p.dtype != torch.float32:
                p.data = p.data.float()
            ntr += p.numel()
    if ntr == 0:
        print("\n".join(n for n, _ in model.named_modules() if n.endswith("proj"))[:3000])
        raise SystemExit("⛔ 0 tham số học — regex target_modules không khớp tên module (đã in tên ở trên)")
    return model, ntr


# ───────────────────────────── selftest (CPU) ─────────────────────────────

def selftest(a):
    from PIL import Image
    neg = nap_neg(a.neg)
    ocr = nap_ocr(a.bundle)
    tr = hang_train(a.bundle)
    rows, cl = hang_val(a.bundle, a.c1)
    co = sum(bool((neg.get(key(r)) or {}).get("point_neg_abs")) for r in cl)
    print(f"[val C1] {len(rows)} bước · click {len(cl)} · có phần tử lân cận cùng vai {co} ({100*co/len(cl):.1f}%)")
    assert len(rows) == 400 and len(cl) == 249, "⛔ val C1 phải 400 bước, 249 click"
    assert co / len(cl) >= 0.6, "⛔ phần tử lân cận phủ dưới 60%"

    cot = sum(bool((neg.get(key(r)) or {}).get("point_neg_abs")) for r in tr)
    hong = [lam_hong(r["target_instruction"], neg.get(key(r))) for r in tr]
    nguon = collections.Counter(diem_nhieu(r, neg, ocr, cho_trong=True)[2] for r in tr)
    print(f"[train] {len(tr)} bước click ngoài episode val · có lân cận {cot} ({100*cot/len(tr):.1f}%) · "
          f"làm hỏng được (trên câu người) {sum(h is not None for h in hong)} "
          f"({100*sum(h is not None for h in hong)/len(tr):.1f}%) · nguồn điểm nhiễu {dict(nguon)}")
    vd = [(r["target_instruction"], h) for r, h in zip(tr, hong) if h][:4]
    for g, h in vd:
        print(f"   ({g} → {h})")
    nv = collections.Counter(diem_nhieu(r, neg, ocr)[2] for r in cl)
    print(f"[val] nguồn điểm nhiễu {dict(nv)}")

    for s, kq in (("(512, 300)", (512, 300)), ("512,300", (512, 300)), ("x: 12.5, 999", (12.5, 999)),
                  ("không có số", None), ("(1200, 30)", None)):
        assert doc_toa_do(s) == kq, (s, doc_toa_do(s))
    assert lam_hong("Click on the Search here bar", {"name": "Search here", "name_neg": "Coffee"}) == \
        "Click on the Coffee bar"

    os.makedirs(a.out, exist_ok=True)
    lech = 0
    for r in (cl[:3] + tr[:3]):
        img = Image.open(os.path.join(a.bundle, r["image"])).convert("RGB")
        gx, gy = r["action"]["x"], r["action"]["y"]
        c = cat_vung(img, r, gx, gy)
        assert c.size == (CROP_PX, CROP_PX)
        nx, ny, _ = diem_nhieu(r, neg, ocr)
        tag = f"ep{r['episode_id']}_s{r['step_id']}"
        c.save(os.path.join(a.out, f"{tag}_gold.png"))
        cat_vung(img, r, nx, ny).save(os.path.join(a.out, f"{tag}_neg.png"))
        lech += trong_vung(r, nx, ny, gx, gy)
    assert lech == 0, "⛔ điểm nhiễu nằm trong vùng vàng"
    print(f"[ảnh] 6 cặp vùng cắt → {a.out}/*_gold.png · *_neg.png (đích phải ở tâm ảnh _gold)")
    print("✅ selftest ĐẠT", flush=True)


# ───────────────────────────── câu nháp train ─────────────────────────────

def make_drafts(a):
    import torch
    from PIL import Image
    from peft import PeftModel
    proc, model, _ = nap_mo_hinh(a)
    model = PeftModel.from_pretrained(model, a.ckpt)
    model.eval()
    print("[điểm lưu]", a.ckpt, flush=True)
    ocr = nap_ocr(a.bundle)
    tr = hang_train(a.bundle)[:a.n] if a.n else hang_train(a.bundle)
    xong = set()
    if os.path.exists(a.out):
        xong = {key(d) for d in map(json.loads, open(a.out, encoding="utf-8"))}
    fo = open(a.out, "a", encoding="utf-8")
    t0, m = time.time(), 0
    for i, r in enumerate(tr):
        if key(r) in xong:
            continue
        img = Image.open(os.path.join(a.bundle, r["image"])).convert("RGB")
        inp, _ = mau_vao(proc, body_of(r, ocr), [img])
        inp, _ = len_thiet_bi(inp, None, model.device)
        gr = sinh(model, proc, inp, 96, do_sample=False, temperature=None, top_p=None, top_k=None)[0]
        torch.manual_seed(SEED * 100003 + i)
        mau = sinh(model, proc, inp, 96, do_sample=True, temperature=1.0, top_p=1.0, top_k=0,
                   num_return_sequences=2)
        fo.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "greedy": gr, "mau": mau},
                            ensure_ascii=False) + "\n")
        fo.flush()
        m += 1
        if m % 20 == 0:
            print(f"  {i+1}/{len(tr)} · {(time.time()-t0)/m:.1f} s/bước · {gr[:60]!r}", flush=True)
    fo.close()
    D = {key(d): d for d in map(json.loads, open(a.out, encoding="utf-8"))}
    G = {key(r): r["target_instruction"].strip() for r in tr}
    trung = sum(D[k]["greedy"].strip().lower() == G[k].lower() for k in G if k in D)
    rong = sum(not D[k]["greedy"] for k in G if k in D)
    print(f"[nháp] {len(D)}/{len(tr)} bước · greedy trùng câu người {trung} ({100*trung/max(len(D),1):.1f}%) · "
          f"greedy rỗng {rong}", flush=True)
    assert len(D) >= len(tr), "⛔ thiếu bước"


# ───────────────────────────── vòng train chung ─────────────────────────────

def vong_train(a, model, proc, dt, mau_epoch, n_mau, tuong_phan):
    """mau_epoch(e) → danh sách mẫu (tất định theo e). Mỗi mẫu: dict(img, r, body, ans, cx, cy, nx, ny)."""
    import torch
    dev = model.device
    os.makedirs(a.out, exist_ok=True)
    tong = a.epochs * n_mau
    n_buoc = math.ceil(tong / a.accum)
    if a.max_steps:
        n_buoc = min(n_buoc, a.max_steps)
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=a.lr, weight_decay=0.0)
    def lich(s):  # tăng tuyến tính trong warmup, rồi giảm tuyến tính về 0
        if s < a.warmup:
            return (s + 1) / a.warmup
        return max(0.0, (n_buoc - s) / max(1, n_buoc - a.warmup))
    sch = torch.optim.lr_scheduler.LambdaLR(opt, lich)
    fp16 = dt == torch.float16
    scaler = torch.amp.GradScaler("cuda", enabled=fp16)
    ac = (lambda: torch.autocast("cuda", dtype=dt)) if dev.type == "cuda" else \
        (lambda: torch.autocast("cpu", enabled=False))

    ck = os.path.join(a.out, "ckpt_last")
    buoc, vi = 0, 0
    if os.path.exists(os.path.join(ck, "state.json")):
        from peft import set_peft_model_state_dict
        from safetensors.torch import load_file
        st = json.load(open(os.path.join(ck, "state.json")))
        set_peft_model_state_dict(model, load_file(os.path.join(ck, "adapter_model.safetensors")))
        opt.load_state_dict(torch.load(os.path.join(ck, "optimizer.pt"), map_location=dev))
        sch.load_state_dict(st["sch"])
        if fp16 and st.get("scaler"):
            scaler.load_state_dict(st["scaler"])
        buoc, vi = st["buoc"], st["vi"]
        print(f"[tiếp từ] bước {buoc} · mẫu {vi}", flush=True)

    def luu(thu_muc, day_du):
        model.save_pretrained(thu_muc)
        if day_du:
            torch.save(opt.state_dict(), os.path.join(thu_muc, "optimizer.pt"))
            json.dump({"buoc": buoc, "vi": vi, "sch": sch.state_dict(),
                       "scaler": scaler.state_dict() if fp16 else None}, open(os.path.join(thu_muc, "state.json"), "w"))

    if dev.type == "cuda":
        torch.cuda.reset_peak_memory_stats()
    t0, nho, dau = time.time(), collections.defaultdict(list), True
    model.train()
    opt.zero_grad(set_to_none=True)
    e_cu = None
    while buoc < n_buoc:
        e, j = divmod(vi, n_mau)
        if e >= a.epochs:
            break
        if e != e_cu:
            ds, e_cu = mau_epoch(e), e
        m = ds[j]
        inp, lab = len_thiet_bi(*mau_vao(proc, m["body"], m["imgs"], m["ans"]), dev)
        with ac():
            l_g = nll_tb(model, inp, lab)
            loss = l_g
            if tuong_phan and m.get("imgs_neg") is not None and a.lam_ctr > 0:
                inp2, lab2 = len_thiet_bi(*mau_vao(proc, m["body"], m["imgs_neg"], m["ans"]), dev)
                l_n = nll_tb(model, inp2, lab2)
                bien = torch.relu(a.margin - (l_n - l_g))
                loss = l_g + a.lam_ctr * bien
                nho["nll_nhieu"].append(l_n.item())
                nho["bien_hoat"].append(float(bien.item() > 0))
        if not torch.isfinite(loss):
            raise SystemExit(f"⛔ nan/inf ở loss, bước {buoc}, mẫu {vi}")
        if dau:
            print(f"[mẫu đầu] nll vàng {l_g.item():.3f} nat/token (hợp lý 0,3–2; gần 0 hoặc >5 là che nhãn sai) · "
                  f"{inp['input_ids'].shape[1]} token", flush=True)
            dau = False
        nho["nll_vang"].append(l_g.item())
        scaler.scale(loss / a.accum).backward()
        vi += 1
        if vi % a.accum == 0 or vi == a.epochs * n_mau:
            scaler.unscale_(opt)
            torch.nn.utils.clip_grad_norm_(params, 1.0)
            scaler.step(opt)
            scaler.update()
            sch.step()
            opt.zero_grad(set_to_none=True)
            buoc += 1
            if buoc % a.log_every == 0 or buoc == n_buoc:
                tb = lambda k: sum(nho[k]) / len(nho[k]) if nho[k] else float("nan")
                vr = torch.cuda.max_memory_allocated() / 2 ** 30 if dev.type == "cuda" else 0
                print(f"  bước {buoc}/{n_buoc} · epoch {e} · nll vàng {tb('nll_vang'):.3f} · nll nhiễu {tb('nll_nhieu'):.3f} · "
                      f"biên hoạt {tb('bien_hoat'):.2f} · lr {sch.get_last_lr()[0]:.2e} · "
                      f"{(time.time()-t0)/max(1, vi):.1f} s/mẫu · đỉnh VRAM {vr:.2f} GiB", flush=True)
                nho.clear()
            if a.save_every and buoc % a.save_every == 0:
                luu(ck, True)
        if vi % n_mau == 0:
            luu(os.path.join(a.out, f"epoch{vi // n_mau}"), False)
    luu(a.out, False)
    luu(ck, True)
    print(f"[xong] {buoc} bước · {vi} mẫu · {(time.time()-t0)/60:.1f} phút → {a.out}", flush=True)


def train_editor(a):
    import torch
    from PIL import Image
    proc, model, dt = nap_mo_hinh(a)
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.enable_input_require_grads()
    model, ntr = gan_lora(model, a)
    print(f"[LoRA editor/{a.crop}] r={a.r} · tham số học {ntr:,} · λctr {a.lam_ctr if a.crop == 'gold' else 0} · "
          f"margin {a.margin} · p_hỏng {a.p_hong}", flush=True)
    neg, ocr = nap_neg(a.neg), nap_ocr(a.bundle)
    D = {key(d): d for d in map(json.loads, open(a.drafts, encoding="utf-8"))}
    tr = [r for r in hang_train(a.bundle) if key(r) in D]
    print(f"[dữ liệu] {len(tr)} bước click train có câu nháp", flush=True)
    assert tr, "⛔ không bước nào có câu nháp"

    def mau_epoch(e):
        rng = random.Random(SEED * 1000 + e)
        ds, dem = [], collections.Counter()
        for r in rng.sample(tr, len(tr)):
            d = D[key(r)]
            nhap = rng.choice([d["greedy"]] + list(d.get("mau") or []))
            if rng.random() < a.p_hong:
                h = lam_hong(nhap, neg.get(key(r)))
                if h:
                    nhap, dem["hong"] = h, dem["hong"] + 1
            body = body_of(r, ocr) + "\nCâu nháp: " + nhap + "\n" + (DAN_SUA_CROP if a.crop == "gold" else DAN_SUA_KHONG)
            ds.append(dict(r=r, body=body, ans=r["target_instruction"].strip(), lazy=True))
        print(f"[epoch {e}] {len(ds)} mẫu · câu nháp làm hỏng {dem['hong']} ({100*dem['hong']/len(ds):.1f}%)", flush=True)
        return _LazyImgs(ds, a, neg, ocr)

    vong_train(a, model, proc, dt, mau_epoch, len(tr), tuong_phan=(a.crop == "gold"))


class _LazyImgs:
    """Nạp ảnh khi lấy mẫu, để danh sách một epoch không giữ cả nghìn ảnh trong RAM."""

    def __init__(self, ds, a, neg, ocr):
        self.ds, self.a, self.neg, self.ocr = ds, a, neg, ocr

    def __getitem__(self, j):
        from PIL import Image
        m = dict(self.ds[j])
        r = m["r"]
        img = Image.open(os.path.join(self.a.bundle, r["image"])).convert("RGB")
        if self.a.crop == "gold":
            gx, gy = r["action"]["x"], r["action"]["y"]
            nx, ny, _ = diem_nhieu(r, self.neg, self.ocr, cho_trong=True)
            m["imgs"] = [img, cat_vung(img, r, gx, gy)]
            m["imgs_neg"] = [img, cat_vung(img, r, nx, ny)]
        else:
            m["imgs"], m["imgs_neg"] = [img], None
        return m


# ───────────────────────────── sửa câu trên val ─────────────────────────────

def edit_val(a):
    import torch
    from PIL import Image
    from peft import PeftModel
    proc, model, _ = nap_mo_hinh(a)
    model = PeftModel.from_pretrained(model, a.editor)
    model.eval()
    print("[bộ biên tập]", a.editor, "· crop", a.crop, flush=True)
    neg, ocr = nap_neg(a.neg), nap_ocr(a.bundle)
    _, cl = hang_val(a.bundle, a.c1, a.n)
    P = {key(d): d["pred"] for d in map(json.loads, open(a.ck500_pred, encoding="utf-8"))}
    assert all(key(r) in P for r in cl), "⛔ pred_ck500 thiếu bước click val"
    PT = {}
    if a.crop == "pred":
        PT = {key(d): d.get("xy") for d in map(json.loads, open(a.points, encoding="utf-8"))}
        assert all(key(r) in PT for r in cl), "⛔ tệp điểm thiếu bước"
    meta_p = a.out.replace(".jsonl", "_meta.jsonl")
    xong = set()
    if os.path.exists(meta_p):
        xong = {key(d) for d in map(json.loads, open(meta_p, encoding="utf-8"))}
    fm = open(meta_p, "a", encoding="utf-8")
    t0, m, nguon = time.time(), 0, collections.Counter()
    for r in cl:
        if key(r) in xong:
            continue
        img = Image.open(os.path.join(a.bundle, r["image"])).convert("RGB")
        nhap = P[key(r)]
        xy = None
        if a.crop == "gold":
            xy = (r["action"]["x"], r["action"]["y"])
        elif a.crop == "neg":
            x, y, ng = diem_nhieu(r, neg, ocr)
            xy = (x, y)
            nguon[ng] += 1
        elif a.crop == "pred":
            if PT[key(r)] is not None:
                xy = tuyet_doi(r, *PT[key(r)])
            else:
                nguon["khong_doc_duoc"] += 1
        imgs = [img] + ([cat_vung(img, r, *xy)] if xy else [])
        if a.crop != "none" and not xy:      # bộ định vị không ra toạ độ ⇒ giữ câu nháp
            sua, lp_s, lp_n = nhap, 0.0, 0.0
        else:
            body = body_of(r, ocr) + "\nCâu nháp: " + nhap + "\n" + (DAN_SUA_CROP if a.crop != "none" else DAN_SUA_KHONG)
            inp, _ = len_thiet_bi(*mau_vao(proc, body, imgs), model.device)
            sua = sinh(model, proc, inp, 96, do_sample=False, temperature=None, top_p=None, top_k=None)[0] or nhap
            with torch.no_grad():
                lp_s = -nll_tb(model, *len_thiet_bi(*mau_vao(proc, body, imgs, sua), model.device)).item()
                lp_n = lp_s if sua == nhap else -nll_tb(model, *len_thiet_bi(*mau_vao(proc, body, imgs, nhap), model.device)).item()
        fm.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "draft": nhap, "edit": sua,
                             "lp_edit": round(lp_s, 5), "lp_draft": round(lp_n, 5),
                             "crop_xy": [round(v, 1) for v in xy] if xy else None}, ensure_ascii=False) + "\n")
        fm.flush()
        m += 1
        if m % 20 == 0:
            print(f"  {m}/{len(cl) - len(xong)} · {(time.time()-t0)/m:.1f} s/bước · {nhap[:40]!r} → {sua[:40]!r}", flush=True)
    fm.close()
    M = {key(d): d for d in map(json.loads, open(meta_p, encoding="utf-8"))}
    with open(a.out, "w", encoding="utf-8") as fo:
        for r in cl:
            fo.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "pred": M[key(r)]["edit"]},
                                ensure_ascii=False) + "\n")
    doi = sum(M[key(r)]["edit"] != M[key(r)]["draft"] for r in cl)
    dai = sorted(len(M[key(r)]["edit"].split()) for r in cl)
    viet = sum(bool(re.search(r"[ăâđêôơưạảấầẩẫậắằẳẵặẹẻẽếềểễệịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]", M[key(r)]["edit"].lower())) for r in cl)
    print(f"[edit-val {a.crop}] {len(cl)} bước click · đổi câu {doi} ({100*doi/len(cl):.1f}%) · số từ trung vị "
          f"{dai[len(dai)//2]} · max {dai[-1]} · câu có dấu tiếng Việt {viet}"
          + (f" · nguồn điểm {dict(nguon)}" if nguon else ""), flush=True)


# ───────────────────────────── bộ định vị ─────────────────────────────

def train_locator(a):
    proc, model, dt = nap_mo_hinh(a)
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.enable_input_require_grads()
    model, ntr = gan_lora(model, a)
    print(f"[LoRA locator] r={a.r} · tham số học {ntr:,} · đọc câu nháp {a.with_draft}", flush=True)
    ocr = nap_ocr(a.bundle)
    D = {}
    if a.with_draft:
        D = {key(d): d for d in map(json.loads, open(a.drafts, encoding="utf-8"))}
    tr = [r for r in hang_train(a.bundle) if not a.with_draft or key(r) in D]
    print(f"[dữ liệu] {len(tr)} bước click train", flush=True)

    def mau_epoch(e):
        rng = random.Random(SEED * 2000 + e)
        ds = []
        for r in rng.sample(tr, len(tr)):
            body = body_of(r, ocr)
            if a.with_draft:
                d = D[key(r)]
                body += "\nCâu nháp: " + rng.choice([d["greedy"]] + list(d.get("mau") or []))
            x, y = chuan(r, r["action"]["x"], r["action"]["y"])
            ds.append(dict(r=r, body=body + "\n" + DAN_DINH_VI, ans=f"({x}, {y})"))
        return _LazyLoc(ds, a)

    vong_train(a, model, proc, dt, mau_epoch, len(tr), tuong_phan=False)


class _LazyLoc:
    def __init__(self, ds, a):
        self.ds, self.a = ds, a

    def __getitem__(self, j):
        from PIL import Image
        m = dict(self.ds[j])
        m["imgs"] = [Image.open(os.path.join(self.a.bundle, m["r"]["image"])).convert("RGB")]
        m["imgs_neg"] = None
        return m


def locate_val(a):
    from PIL import Image
    from peft import PeftModel
    proc, model, _ = nap_mo_hinh(a)
    model = PeftModel.from_pretrained(model, a.locator)
    model.eval()
    print("[bộ định vị]", a.locator, "· đọc câu nháp", a.with_draft, flush=True)
    ocr = nap_ocr(a.bundle)
    _, cl = hang_val(a.bundle, a.c1, a.n)
    P = {key(d): d["pred"] for d in map(json.loads, open(a.ck500_pred, encoding="utf-8"))}
    xong = set()
    if os.path.exists(a.out):
        xong = {key(d) for d in map(json.loads, open(a.out, encoding="utf-8"))}
    fo = open(a.out, "a", encoding="utf-8")
    t0, m = time.time(), 0
    for r in cl:
        if key(r) in xong:
            continue
        img = Image.open(os.path.join(a.bundle, r["image"])).convert("RGB")
        body = body_of(r, ocr) + (("\nCâu nháp: " + P[key(r)]) if a.with_draft else "") + "\n" + DAN_DINH_VI
        inp, _ = len_thiet_bi(*mau_vao(proc, body, [img]), model.device)
        s = sinh(model, proc, inp, 16, do_sample=False, temperature=None, top_p=None, top_k=None)[0]
        xy = doc_toa_do(s)
        gx, gy = chuan(r, r["action"]["x"], r["action"]["y"])
        trung = int(xy is not None and abs(xy[0] - gx) <= TOL and abs(xy[1] - gy) <= TOL)
        fo.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "raw": s, "xy": xy,
                             "gold_norm": [gx, gy], "hit_disk": trung}, ensure_ascii=False) + "\n")
        fo.flush()
        m += 1
        if m % 20 == 0:
            print(f"  {m}/{len(cl) - len(xong)} · {(time.time()-t0)/m:.1f} s/bước · {s!r}", flush=True)
    fo.close()
    R = [d for d in map(json.loads, open(a.out, encoding="utf-8"))]
    hit = sum(d["hit_disk"] for d in R)
    khong = sum(d["xy"] is None for d in R)
    dong = f"[locate-val] {len(R)} bước · trúng đĩa ±14% {hit} ({100*hit/len(R):.1f}%) · không đọc được toạ độ {khong}"
    if a.ck500_score and os.path.exists(a.ck500_score):
        S = {key(d): d for d in map(json.loads, open(a.ck500_score, encoding="utf-8"))}
        sai = [d for d in R if key(d) in S and not S[key(d)]["executable"]]
        tro = [d for d in sai if S[key(d)]["action_ok"]]
        dong += (f" · trên {len(sai)} bước ck500 sai: {sum(d['hit_disk'] for d in sai)}"
                 f" · trên {len(tro)} bước ck500 trỏ sai: {sum(d['hit_disk'] for d in tro)}")
    print(dong, flush=True)
    assert khong <= 0.3 * len(R), "⛔ không đọc được toạ độ ở hơn 30% bước"


# ───────────────────────────── main ─────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    for f in ("--selftest", "--merge", "--make-drafts", "--train-editor", "--edit-val", "--train-locator",
              "--locate-val"):
        ap.add_argument(f, action="store_true")
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--merged", default="/kaggle/working/s1_merged")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--neg", default="tage_neg.jsonl")
    ap.add_argument("--c1")
    ap.add_argument("--ckpt")
    ap.add_argument("--drafts")
    ap.add_argument("--crop", choices=("gold", "neg", "none", "pred"), default="gold")
    ap.add_argument("--editor")
    ap.add_argument("--locator")
    ap.add_argument("--points")
    ap.add_argument("--ck500-pred")
    ap.add_argument("--ck500-score", default="score_ck500_raw.jsonl")
    ap.add_argument("--with-draft", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--r", type=int, default=16)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--warmup", type=int, default=30)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--accum", type=int, default=8)
    ap.add_argument("--lam-ctr", type=float, default=0.5)
    ap.add_argument("--margin", type=float, default=0.2)
    ap.add_argument("--p-hong", type=float, default=0.3)
    ap.add_argument("--max-steps", type=int, default=0)
    ap.add_argument("--save-every", type=int, default=50)
    ap.add_argument("--log-every", type=int, default=10)
    a = ap.parse_args()
    a.adapter = a.adapter or os.path.join(a.bundle, "adapter_s1_seed101")
    random.seed(SEED)

    if a.selftest:
        assert a.c1 and a.out, "cần --c1 và --out"
        selftest(a)
    elif a.merge:
        merge(a)
    elif a.make_drafts:
        assert a.ckpt and a.out
        make_drafts(a)
    elif a.train_editor:
        assert a.drafts and a.out and a.crop in ("gold", "none")
        train_editor(a)
    elif a.edit_val:
        assert a.c1 and a.ck500_pred and a.editor and a.out and (a.crop != "pred" or a.points)
        edit_val(a)
    elif a.train_locator:
        assert a.out and (not a.with_draft or a.drafts)
        train_locator(a)
    elif a.locate_val:
        assert a.c1 and a.ck500_pred and a.locator and a.out
        locate_val(a)
    else:
        ap.error("chọn một chế độ")


if __name__ == "__main__":
    main()
