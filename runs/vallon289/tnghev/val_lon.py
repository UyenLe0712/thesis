# -*- coding: utf-8 -*-
"""Val lớn cho phễu sàng 289 (B.12 của 288): 1.567 bước / 1.002 click / 346 episode = val_cham400 ∪ val_cham600.

    python val_lon.py --dung --val V --out VD                       # dựng thư mục cho score_run.py
    python val_lon.py --gen --bundle B --merged M --val V [--ckpt CK] --out pred.jsonl [--n N] [--so tệp] [--no-q4]
    python val_lon.py --selftest [--repo R] [--bundle B]            # CPU

Không episode nào của val lớn nằm trong 1.000 câu nhắc GRPO của ck500. Sinh y đường `grpo_spice.py --gen`
(hoà S1 → gắn điểm lưu, greedy 96 token, câu nhắc SYS + prompt_body, ảnh trước chữ).
Viết lại 6/10/2026 từ bản mô tả B.12 (mã gốc ở máy Mac) ⇒ md5 khác bản gốc.
"""
import argparse, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TAPT = ("click", "long_press")
N_BUOC, N_CLICK, N_EP = 1567, 1002, 346


def doc(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def la_cham(r):
    return r["action"].get("action_type") in TAPT and "x" in r["action"]


def val_lon(V):
    d = {}
    for f in ("val_cham400.jsonl", "val_cham600.jsonl"):
        for r in doc(os.path.join(V, f)):
            d.setdefault((r["episode_id"], r["step_id"]), r)
    recs = [d[k] for k in sorted(d)]
    click = [r for r in recs if la_cham(r)]
    ep = {r["episode_id"] for r in recs}
    assert (len(recs), len(click), len(ep)) == (N_BUOC, N_CLICK, N_EP), (len(recs), len(click), len(ep))
    return recs, click


def dung(a):
    recs, click = val_lon(a.val)
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "val_lon_recs.jsonl"), "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps({**r, "gold_instruction": r.get("gold_instruction") or r["target_instruction"]},
                               ensure_ascii=False) + "\n")
    src, dst = os.path.join(a.val, "ocr.jsonl"), os.path.join(a.out, "ocr.jsonl")
    if os.path.abspath(src) != os.path.abspath(dst):
        import shutil; shutil.copy(src, dst)
    link = os.path.join(a.out, "images")
    if os.path.lexists(link):
        os.remove(link)
    os.symlink(os.path.abspath(os.path.join(a.val, "images")), link)
    thieu = [r["image"] for r in click if not os.path.exists(os.path.join(a.out, r["image"]))]
    print(f"[dựng] {a.out}: {len(recs)} bước · {len(click)} click · thiếu ảnh click {len(thieu)}", flush=True)
    assert not thieu, f"DỪNG: thiếu ảnh, ví dụ {thieu[:3]}"


def gen(a):
    import grpo_spice as GS
    recs, click = val_lon(a.val)
    if a.n:
        click = click[:a.n]
    ocr = GS.nap_ocr(a.bundle)
    PV = {(r["episode_id"], r["step_id"]): r for r in doc(os.path.join(a.bundle, "p1_val_rows.jsonl"))}
    lech = sum(1 for r in click if (r["episode_id"], r["step_id"]) not in PV
               or GS.body_of(r, ocr) != GS.body_of(PV[(r["episode_id"], r["step_id"])], ocr))
    t_ocr = sum(r["image"] not in ocr for r in click)
    t_anh = sum(not os.path.exists(os.path.join(a.bundle, r["image"])) for r in click)
    print(f"[dữ liệu] val lớn · {len(click)} bước click · thiếu OCR {t_ocr} · thiếu ảnh {t_anh} · "
          f"câu nhắc lệch p1_val_rows {lech}", flush=True)
    assert not (lech or t_ocr or t_anh), "DỪNG: dữ liệu val lớn lệch gói"

    a.adapter = os.path.join(a.bundle, "adapter_s1_seed101")
    import torch
    from PIL import Image
    proc, model, _ = GS.nap(a)
    if a.ckpt:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, a.ckpt)
        print("[điểm lưu]", a.ckpt, flush=True)
    else:
        print("[điểm lưu] KHÔNG gắn — đây là S1 hoà", flush=True)
    model.eval()
    xong = {(d["episode_id"], d["step_id"]) for d in doc(a.out)} if os.path.exists(a.out) else set()
    print(f"[nối tiếp] đã có {len(xong)}/{len(click)}", flush=True)
    t0, moi = time.time(), 0
    with open(a.out, "a", encoding="utf-8") as fo:
        for i, r in enumerate(click):
            k = (r["episode_id"], r["step_id"])
            if k in xong:
                continue
            msg = [{"role": "system", "content": GS.SYS},
                   {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + GS.body_of(r, ocr)}]}]
            text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
            img = Image.open(os.path.join(a.bundle, r["image"])).convert("RGB")
            inp = proc(text=[text], images=[img], return_tensors="pt").to(model.device)
            L = inp["input_ids"].shape[1]
            with torch.no_grad():
                g = model.generate(**inp, max_new_tokens=96, do_sample=False, use_cache=True,
                                   temperature=None, top_p=None, top_k=None)
            s = proc.decode(g[0][L:], skip_special_tokens=True).strip()
            fo.write(json.dumps({"episode_id": k[0], "step_id": k[1], "pred": s}, ensure_ascii=False) + "\n")
            fo.flush(); moi += 1
            if (i + 1) % 50 == 0:
                dt = time.time() - t0
                print(f"  {i+1}/{len(click)} · {dt/60:.1f} phút · {dt/moi:.2f} s/câu · {s[:60]!r}", flush=True)
    P = {(d["episode_id"], d["step_id"]): d["pred"] for d in doc(a.out)}
    print(f"[xong] {len(P)} câu · rỗng {sum(not v for v in P.values())}", flush=True)
    if a.so:
        S = {(d["episode_id"], d["step_id"]): d["pred"] for d in doc(a.so)}
        chung = [k for k in S if k in P]
        print(f"[so {os.path.basename(a.so)}] {sum(P[k] == S[k] for k in chung)}/{len(chung)} câu trùng", flush=True)


def selftest(a):
    from build_branch_data import prompt_body
    R = a.repo
    V = os.path.join(R, "harness", "dg1_cache", "train_ac")
    ok = []
    recs, click = val_lon(V)
    ok.append(("1.567 bước / 1.002 click / 346 episode", True))
    ocr = {o["image"]: o for o in doc(os.path.join(V, "ocr.jsonl"))}
    ok.append(("OCR phủ đủ val lớn", all(r["image"] in ocr for r in recs)))
    pk = json.load(open(os.path.join(R, "runs", "ctg", "p0", "p0_a3", "prompt_keys.json")))[:1000]
    ep_pk = {int(k.split("_")[0]) for k in pk}
    ok.append(("0 episode chung với 1.000 câu nhắc ck500", not ({r["episode_id"] for r in recs} & ep_pk)))
    C1 = os.path.join(R, "runs", "c1", "exec8")
    c1 = [r for r in doc(os.path.join(C1, "c1data", "c1_recs.jsonl")) if la_cham(r)]
    kc = {(r["episode_id"], r["step_id"]) for r in click}
    ok.append(("249 click C1 nằm trong 1.002 click", all((r["episode_id"], r["step_id"]) in kc for r in c1)))
    ocr1 = {o["image"]: o for o in doc(os.path.join(C1, "c1data", "ocr.jsonl"))}
    VL = {(r["episode_id"], r["step_id"]): r for r in recs}
    body = lambda r, o: prompt_body({"goal": r["goal"], "history": r.get("history") or []}, o.get(r["image"]))
    ok.append(("câu nhắc C1 dựng từ val lớn trùng câu nhắc dựng từ c1_recs",
               all(body(VL[(r["episode_id"], r["step_id"])], ocr) == body(r, ocr1) for r in c1)))
    tho = {(o["episode_id"], o["step_id"]) for o in doc(os.path.join(R, "runs", "grpo_spice", "score_ck500_raw.jsonl"))}
    ok.append(("tệp thô ck500 trên C1 (249) là tập con của val lớn", len(tho) == 249 and tho <= kc))
    if a.bundle:
        import grpo_spice as GS
        oc = GS.nap_ocr(a.bundle)
        PV = {(r["episode_id"], r["step_id"]): r for r in doc(os.path.join(a.bundle, "p1_val_rows.jsonl"))}
        ok.append(("[gói] câu nhắc val lớn trùng p1_val_rows",
                   all(GS.body_of(r, oc) == GS.body_of(PV[(r["episode_id"], r["step_id"])], oc) for r in click)))
    for t, v in ok:
        print(("✅ " if v else "⛔ ") + t)
    print(f"{'✅ selftest ĐẠT' if all(v for _, v in ok) else '⛔ selftest RỚT'} ({sum(v for _, v in ok)}/{len(ok)})")
    sys.exit(0 if all(v for _, v in ok) else 1)


def main():
    ap = argparse.ArgumentParser()
    for f in ("--dung", "--gen", "--selftest"):
        ap.add_argument(f, action="store_true")
    ap.add_argument("--val"); ap.add_argument("--out"); ap.add_argument("--bundle"); ap.add_argument("--merged")
    ap.add_argument("--ckpt"); ap.add_argument("--so"); ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--no-q4", dest="q4", action="store_false")
    ap.add_argument("--repo", default=os.path.abspath(os.path.join(HERE, "..", "..", "..")))
    a = ap.parse_args()
    if a.selftest:
        sys.path.append(os.path.join(a.repo, "harness"))
        selftest(a)
    elif a.dung:
        assert a.val and a.out, "cần --val --out"
        dung(a)
    elif a.gen:
        assert a.bundle and a.merged and a.val and a.out, "cần --bundle --merged --val --out"
        gen(a)
    else:
        ap.error("chọn --dung, --gen hoặc --selftest")


if __name__ == "__main__":
    main()
