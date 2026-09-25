# -*- coding: utf-8 -*-
"""
PATA C2 · P1 — likelihood 7 nhánh trên val400 (harness/tai_lieu_2026-09-25/204 §4.2).

Câu hỏi: speaker S (đóng băng) có dùng được thông tin VÙNG không, và thiếu ROUTING hay thiếu PIXEL?
Cùng prompt, cùng câu vàng, chỉ đổi ảnh thứ hai:

    O              ảnh 1 = full, KHÔNG có ảnh 2
    L_G L_D L_R    ảnh 1 = full, ảnh 2 = crop lấy từ bản full ĐÃ RESIZE về cỡ mô hình thấy (không thêm chi tiết)
    H_G H_D H_R    ảnh 1 = full, ảnh 2 = crop lấy từ screenshot GỐC (có thêm chi tiết)

G/D/R = cửa sổ vuông cùng cạnh quanh phần tử vàng / phần tử gây nhiễu thật / vị trí ngẫu nhiên
(pata_true_d.py). Mọi crop resize về 448×448 ⇒ đúng 256 token ảnh, cùng số token trong họ L và họ H.
Không có branch ID trong prompt.

    s = mean_t log p(y_t | y_<t, nhánh)   trên token của CÂU VÀNG (không tính <|im_end|>)
    ΔL_GD = s(L_G) − s(L_D)   ΔL_GR = s(L_G) − s(L_R)   (tương tự ΔH)   Δres = ΔH − ΔL

Ba lệnh:
    ~/.venvs/thesis/bin/python harness/pata_p1.py prep          # CPU, WSL: dựng crop + KHOÁ p1_decision.json
    python harness/pata_p1.py run --adapter <S/final> --out <dir> # GPU (Kaggle T4): chấm, nối tiếp được
    ~/.venvs/thesis/bin/python harness/pata_p1.py doc --scores <dir>/p1_scores.jsonl   # CPU: bootstrap + quyết định

Assert khi `run` (204 §4.2): không dropout (mọi module eval) · token count khớp trong họ L và họ H ·
G=D nhân tạo ⇒ gap 0 · đổi thứ tự nhánh trong lô không đổi score. Hỏng bất kỳ ⇒ dừng trước khi chấm.
"""
import os, sys, json, glob, math, hashlib, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
CROP = 448                                   # 448² = 200.704 = MIN_PIX ⇒ processor giữ nguyên, 256 token
IM_END = 151645
TOL_GD0 = 1e-5                               # G=D nhân tạo: hai hàng giống hệt trong CÙNG lô
TOL_ORDER = 1e-3                             # đổi thứ tự trong lô (nats/token), = 5% ngưỡng 0,02

# ─────────────────────────────────────────────────────────────── luật quyết (KHOÁ ở prep)
LUAT = {
    "directional": "lower90(ΔF_GD) > 0 AND lower90(ΔF_GR) > 0 AND mean(ΔF_GD) >= 0.02 (F = L hoặc H)",
    "extra_resolution": "lower90(Δres_GD) > 0 AND lower90(Δres_GR) > 0 AND mean(Δres_GD) >= 0.01 "
                        "AND mean(Δres_GR) >= 0.01",
    "bootstrap": "cụm theo episode, 10.000 lần, lower90 = phân vị 10% (một phía 90%)",
    "bang_chon_theo_thu_tu": [
        ["dirL AND NOT res", "thiếu routing", "RCA r=128, 2 tầng"],
        ["dirL AND res", "routing + pixel; pixel thêm ích", "dual-view trước (đơn giản hơn)"],
        ["NOT dirL AND dirH AND res", "thiếu pixel", "dual-view predicted crop"],
        ["gd_only(L) OR gd_only(H)", "artefact D/R", "sửa control, chưa chọn"],
        ["NOT dirL AND NOT dirH", "vùng không đủ", "dừng C2 (ghi thêm cờ extra_image nếu H_*>O)"],
        ["còn lại", "không khớp bảng", "dừng, báo lại — không tự chọn"],
    ],
    "gd_only(F)": "lower90(ΔF_GD) > 0 AND mean(ΔF_GD) >= 0.02 AND NOT lower90(ΔF_GR) > 0",
    "extra_image": "lower90(mean(s(H_G),s(H_D),s(H_R)) − s(O)) > 0 — chỉ là cờ, không claim grounding",
    "ngưỡng": {"dir_mean": 0.02, "res_mean": 0.01},
}
NHANH = ("O", "LG", "LD", "LR", "HG", "HD", "HR")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def crop_name(r, fam, br):
    return f"{r['episode_id']}_{r['step_id']}_{fam}{br}.png"


# ─────────────────────────────────────────────────────────────── prep (CPU)
def prep(a):
    from PIL import Image
    from transformers.models.qwen2_vl.image_processing_qwen2_vl import smart_resize
    import pata_model as PM
    pd = os.path.join(ROOT, "pata")
    kq = sorted(glob.glob(os.path.join(pd, "audit_trueD_lan*", "ket_qua.json")))
    audit = json.load(open(kq[-1])) if kq else None
    if not (audit and audit.get("dat")):
        if not a.chua_audit:
            sys.exit("⛔ audit mù (pata_audit_d.py doc) chưa ĐẠT — P1 chỉ chạy sau P0. "
                     "Thử khô thì thêm --chua-audit (gói dựng từ đó bị make_bundle từ chối).")
        print("⚠️  --chua-audit: dựng crop để THỬ, p1_decision.json ghi audit_dat=false", flush=True)
    src = os.path.join(pd, "val400_trueD.jsonl")
    recs = [json.loads(l) for l in open(src, encoding="utf-8")]
    od = os.path.join(pd, "p1_crops")
    os.makedirs(od, exist_ok=True)
    hs = hashlib.sha256()
    for i, r in enumerate(recs):
        im = Image.open(os.path.join(ROOT, r["image"])).convert("RGB")
        W, H = im.size
        rh, rw = smart_resize(H, W, 28, PM.MIN_PIX, PM.MAX_PIX)     # đúng cỡ processor đưa vào mô hình
        low = im.resize((rw, rh), Image.BICUBIC)
        for br in "GDR":
            x1, y1, x2, y2 = r[f"win_{br}"]
            for fam, src_im, sx, sy in (("L", low, rw / r["w"], rh / r["h"]), ("H", im, W / r["w"], H / r["h"])):
                c = src_im.crop((round(x1 * sx), round(y1 * sy), round(x2 * sx), round(y2 * sy)))
                c = c.resize((CROP, CROP), Image.BICUBIC)
                p = os.path.join(od, crop_name(r, fam, br))
                c.save(p)
                hs.update(open(p, "rb").read())
        if i % 50 == 0:
            print(f"  crop {i}/{len(recs)}", flush=True)
    dec = {"luat": LUAT, "n_cap": len(recs), "crop_px": CROP, "audit_dat": bool(audit and audit.get("dat")),
           "audit": audit, "sha256": {"val400_trueD.jsonl": sha256(src), "p1_crops(ghep)": hs.hexdigest()},
           "tol": {"gd0": TOL_GD0, "order": TOL_ORDER}}
    p = os.path.join(pd, "p1_decision.json")
    json.dump(dec, open(p, "w"), indent=1, ensure_ascii=False)
    print(f"Crop: {len(recs)} cặp × 6 → {od}")
    print(f"KHOÁ luật quyết: {p}  sha256 {sha256(p)[:16]}…  (ghi con số này lại — `doc` sẽ đối chiếu)")


# ─────────────────────────────────────────────────────────────── run (GPU)
def run(a):
    import torch
    from PIL import Image
    from peft import PeftModel
    import pata_model as PM
    from build_branch_data import prompt_body, SYS

    dr = a.data_root
    dec_p = os.path.join(dr, "pata", "p1_decision.json")
    dec = json.load(open(dec_p))
    if not dec["audit_dat"] and not a.thu:
        sys.exit("⛔ p1_decision.json ghi audit_dat=false — gói này dựng khi audit chưa đạt. Thử khô: --thu")
    recs = [json.loads(l) for l in open(os.path.join(dr, "pata", "val400_trueD.jsonl"), encoding="utf-8")]
    assert sha256(os.path.join(dr, "pata", "val400_trueD.jsonl")) == dec["sha256"]["val400_trueD.jsonl"]
    if a.limit:
        recs = recs[: a.limit]
    ocr = {}
    for l in open(os.path.join(dr, "ocr.jsonl"), encoding="utf-8"):
        o = json.loads(l); ocr[o["image"]] = o
    assert os.path.exists(os.path.join(a.adapter, "adapter_config.json")), f"thiếu adapter ở {a.adapter}"
    assert not os.path.exists(os.path.join(a.adapter, "pata_heads.pt")), "⛔ đây là điểm lưu H/J/C1, P1 cần S"

    proc, m, _, _, cdt = PM.load_base(a.tiny)
    m = PeftModel.from_pretrained(m, a.adapter)
    m.eval()
    assert not any(x.training for x in m.modules()), "⛔ còn module ở chế độ train (dropout bật)"
    base, vl, text = PM.parts(m)
    dev = text.embed_tokens.weight.device
    print(f"[S] {a.adapter} · p1_decision sha256 {sha256(dec_p)[:16]}…", flush=True)

    def text_of(r, n_img):
        body = prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
        cont = [{"type": "image"}] * n_img + [{"type": "text", "text": "\n" + body}]
        msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": cont}]
        return (proc.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
                + r["target_instruction"].strip() + "<|im_end|>\n")

    def score(texts, images):
        """Trả list (s, n_tok, n_img_tok, seq_len) cho từng hàng của lô. Lô cùng độ dài ⇒ không đệm."""
        enc = proc(text=texts, images=images, return_tensors="pt", padding=True)
        assert bool(enc["attention_mask"].all()), "⛔ lô có đệm — các nhánh không cùng số token"
        kw = {k: enc[k].to(dev) for k in ("input_ids", "attention_mask", "pixel_values", "image_grid_thw")}
        with torch.no_grad(), torch.autocast(dev.type, dtype=cdt, enabled=dev.type == "cuda"):
            hs = vl(**kw, use_cache=False, return_dict=True).last_hidden_state
        out = []
        for b in range(hs.shape[0]):
            ids = enc["input_ids"][b]
            st = [i for i in range(len(ids) - 2) if ids[i] == PM.IM_START and ids[i + 1] == PM.ASSISTANT_ID
                  and ids[i + 2] == PM.NL_ID]
            a0 = st[-1] + 3
            e = max(i for i in range(len(ids)) if ids[i] == IM_END)
            assert e > a0
            with torch.no_grad():
                lg = base.lm_head(hs[b, a0 - 1: e - 1]).float()
                lp = torch.log_softmax(lg, -1).gather(1, ids[a0:e].to(dev)[:, None]).squeeze(1)
            out.append((float(lp.mean()), e - a0, int((ids == PM.IMAGE_TOKEN_ID).sum()), len(ids)))
        return out

    def load_crops(r, fam):
        return {br: Image.open(os.path.join(dr, "pata", "p1_crops", crop_name(r, fam, br))).convert("RGB")
                for br in "GDR"}

    def fam_score(r, full, fam, order="GDR"):
        c = load_crops(r, fam)
        t = text_of(r, 2)
        res = score([t] * 3, [x for br in order for x in (full, c[br])])
        return dict(zip(order, res))

    # ── assert trước khi chấm ──────────────────────────────────────────────
    for r in recs[: a.n_kiem]:
        full = Image.open(os.path.join(dr, r["image"])).convert("RGB")
        for fam in "LH":
            s1 = fam_score(r, full, fam, "GDR")
            s2 = fam_score(r, full, fam, "RDG")
            for br in "GDR":
                d = abs(s1[br][0] - s2[br][0])
                assert d <= TOL_ORDER, f"⛔ đổi thứ tự lô đổi score {fam}{br}: {d:.2e} ({r['episode_id']},{r['step_id']})"
            assert len({v[3] for v in s1.values()}) == 1 and len({v[2] for v in s1.values()}) == 1, \
                f"⛔ token count lệch trong họ {fam}: {s1}"
            c = load_crops(r, fam)
            t = text_of(r, 2)
            gg = score([t] * 3, [full, c["G"], full, c["G"], full, c["R"]])
            assert abs(gg[0][0] - gg[1][0]) <= TOL_GD0, f"⛔ G=D nhân tạo mà gap {gg[0][0] - gg[1][0]:.2e}"
        print(f"  kiểm ✓ ({r['episode_id']},{r['step_id']}) · tok ảnh L/H "
              f"{s1['G'][2]} · dài {s1['G'][3]}", flush=True)
    print(f"[assert] {min(a.n_kiem, len(recs))} cặp: thứ tự lô ≤ {TOL_ORDER} · G=D ≤ {TOL_GD0} · "
          f"token khớp trong họ · không dropout — ĐẠT", flush=True)

    # ── chấm, nối tiếp được, mở–ghi–đóng từng cặp ───────────────────────────
    os.makedirs(a.out, exist_ok=True)
    lock = os.path.join(a.out, "p1.pid")         # chặn hai tiến trình cùng ghi một tệp (đã xảy ra 25/9)
    if os.path.exists(lock):
        try:
            os.kill(int(open(lock).read()), 0)
            sys.exit(f"⛔ tiến trình {open(lock).read()} đang chấm vào {a.out} — không chạy thêm bản thứ hai")
        except (ProcessLookupError, ValueError):
            pass
    open(lock, "w").write(str(os.getpid()))
    fp = os.path.join(a.out, "p1_scores.jsonl")
    xong = set()
    if os.path.exists(fp):
        for l in open(fp, encoding="utf-8"):
            try:
                x = json.loads(l); xong.add((x["episode_id"], x["step_id"]))
            except Exception:
                pass
    todo = [r for r in recs if (r["episode_id"], r["step_id"]) not in xong]
    print(f"[chấm] {len(recs)} cặp · đã có {len(xong)} · còn {len(todo)}", flush=True)
    import time
    t0 = time.time()
    for i, r in enumerate(todo):
        full = Image.open(os.path.join(dr, r["image"])).convert("RGB")
        o = score([text_of(r, 1)], [full])[0]
        L = fam_score(r, full, "L")
        H = fam_score(r, full, "H")
        assert L["G"][3] == H["G"][3] and L["G"][2] == H["G"][2], "⛔ token count lệch giữa họ L và H"
        row = {"episode_id": r["episode_id"], "step_id": r["step_id"], "n_tok": o[1],
               "s_O": o[0], **{f"s_L{k}": v[0] for k, v in L.items()}, **{f"s_H{k}": v[0] for k, v in H.items()},
               "img_tok": {"O": o[2], "LH": L["G"][2]}, "len": {"O": o[3], "LH": L["G"][3]}}
        with open(fp, "a", encoding="utf-8") as f:
            f.write(json.dumps(row) + "\n")
        if i % 10 == 0:
            el = time.time() - t0
            print(f"  {len(xong) + i + 1}/{len(recs)} · {el / (i + 1):.1f} s/cặp · "
                  f"còn ~{el / (i + 1) * (len(todo) - i - 1) / 60:.0f} phút", flush=True)
    json.dump({"adapter": a.adapter, "p1_decision_sha256": sha256(dec_p), "n": len(recs)},
              open(os.path.join(a.out, "p1_run_meta.json"), "w"), indent=1)
    print(f"XONG → {fp}", flush=True)


# ─────────────────────────────────────────────────────────────── doc (CPU)
def doc(a):
    from pata_eval import lower90
    dec_p = os.path.join(ROOT, "pata", "p1_decision.json")
    rows, trung, lech = {}, 0, 0.0
    for l in open(a.scores, encoding="utf-8"):
        r = json.loads(l)
        k = (r["episode_id"], r["step_id"])
        if k in rows:                      # hai tiến trình cùng ghi (Q3 bấm hai lần) ⇒ cặp chấm hai lần
            trung += 1
            lech = max(lech, max(abs(r[f"s_{b}"] - rows[k][f"s_{b}"]) for b in NHANH))
            continue
        rows[k] = r
    rows = list(rows.values())
    if trung:
        print(f"gộp {trung} dòng trùng · lệch lớn nhất giữa hai lần chấm cùng cặp {lech:.2e} nats/token")
        assert lech <= TOL_ORDER, "⛔ chấm lại cùng cặp ra số khác — không tất định"
    meta_p = os.path.join(os.path.dirname(a.scores), "p1_run_meta.json")
    if os.path.exists(meta_p):
        ms = json.load(open(meta_p))["p1_decision_sha256"]
        assert ms == sha256(dec_p), "⛔ p1_decision.json trên máy KHÁC bản lượt chạy đã dùng — luật bị sửa sau?"
        print(f"luật quyết khớp bản lượt chạy dùng ✓ ({ms[:16]}…)")
    dec = json.load(open(dec_p))
    assert len(rows) == dec["n_cap"], f"mới có {len(rows)}/{dec['n_cap']} cặp — chấm chưa xong"
    # Số không hữu hạn (tràn fp16 trên T4 — gặp 1/232 cặp ở L_R ngày 25/9) ⇒ bỏ CẢ cặp ở mọi nhánh (ghép cặp),
    # khai tên cặp. Luật khoá không nói gì về NaN; bỏ ghép cặp là cách duy nhất không chọn phía.
    nan = [(r["episode_id"], r["step_id"], [b for b in NHANH if not math.isfinite(r[f"s_{b}"])])
           for r in rows if not all(math.isfinite(r[f"s_{b}"]) for b in NHANH)]
    if nan:
        print(f"⚠️ bỏ {len(nan)} cặp có số không hữu hạn (ghép cặp, mọi nhánh): {nan}")
        rows = [r for r in rows if all(math.isfinite(r[f"s_{b}"]) for b in NHANH)]
    ng = dec["luat"]["ngưỡng"]
    D = {}
    for F in "LH":
        D[f"{F}_GD"] = [(r["episode_id"], r[f"s_{F}G"] - r[f"s_{F}D"]) for r in rows]
        D[f"{F}_GR"] = [(r["episode_id"], r[f"s_{F}G"] - r[f"s_{F}R"]) for r in rows]
    for k in ("GD", "GR"):
        D[f"res_{k}"] = [(e, h - l) for (e, h), (_, l) in zip(D[f"H_{k}"], D[f"L_{k}"])]
    D["extra_image"] = [(r["episode_id"], (r["s_HG"] + r["s_HD"] + r["s_HR"]) / 3 - r["s_O"]) for r in rows]
    S = {k: lower90(v) for k, v in D.items()}
    print("=" * 72)
    print(f"P1 · {len(rows)} cặp · {len({r['episode_id'] for r in rows})} episode · nats/token")
    for k, (mu, lo) in S.items():
        print(f"  Δ{k:12} mean {mu:+.4f}   lower90 {lo:+.4f}")
    pos = lambda k: S[k][1] > 0
    dirF = {F: pos(f"{F}_GD") and pos(f"{F}_GR") and S[f"{F}_GD"][0] >= ng["dir_mean"] for F in "LH"}
    gd_only = {F: pos(f"{F}_GD") and S[f"{F}_GD"][0] >= ng["dir_mean"] and not pos(f"{F}_GR") for F in "LH"}
    res = (pos("res_GD") and pos("res_GR") and S["res_GD"][0] >= ng["res_mean"]
           and S["res_GR"][0] >= ng["res_mean"])
    extra = pos("extra_image")
    B = dec["luat"]["bang_chon_theo_thu_tu"]
    if dirF["L"] and not res:
        hang = B[0]
    elif dirF["L"] and res:
        hang = B[1]
    elif not dirF["L"] and dirF["H"] and res:
        hang = B[2]
    elif gd_only["L"] or gd_only["H"]:
        hang = B[3]
    elif not dirF["L"] and not dirF["H"]:
        hang = B[4]
    else:
        hang = B[5]
    print("-" * 72)
    print(f"  directional L {'ĐẠT' if dirF['L'] else 'không'} · H {'ĐẠT' if dirF['H'] else 'không'} · "
          f"extra-resolution {'ĐẠT' if res else 'không'} · gd_only L/H {gd_only['L']}/{gd_only['H']} · "
          f"extra_image {extra}")
    print(f"⇒ HÀNG: [{hang[0]}] → {hang[1]} → {hang[2]}")
    out = {"n": len(rows), "bo_nan": nan, "delta": {k: {"mean": v[0], "lower90": v[1]} for k, v in S.items()},
           "dirL": dirF["L"], "dirH": dirF["H"], "res": res, "gd_only": gd_only, "extra_image": extra,
           "hang": hang, "p1_decision_sha256": sha256(dec_p)}
    p = os.path.join(os.path.dirname(a.scores), "p1_ket_qua.json")
    json.dump(out, open(p, "w"), indent=1, ensure_ascii=False)
    print(f"→ {p}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["prep", "run", "doc"])
    ap.add_argument("--chua-audit", action="store_true", help="prep: dựng crop để thử khi audit chưa đạt")
    ap.add_argument("--adapter", help="run: thư mục S/final")
    ap.add_argument("--data-root", default=ROOT)
    ap.add_argument("--out", help="run: thư mục ra")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--n-kiem", type=int, default=6, help="run: số cặp dùng cho các assert trước khi chấm")
    ap.add_argument("--thu", action="store_true", help="run: cho phép gói dựng khi audit chưa đạt (thử khô)")
    ap.add_argument("--tiny", action="store_true", help="run: mô hình tí hon trên CPU, chỉ để thử dây nối")
    ap.add_argument("--scores", help="doc: đường dẫn p1_scores.jsonl")
    a = ap.parse_args()
    {"prep": prep, "run": run, "doc": doc}[a.cmd](a)
