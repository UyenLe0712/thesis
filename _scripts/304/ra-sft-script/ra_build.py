# -*- coding: utf-8 -*-
"""304 — dựng dữ liệu RA-SFT từ ck500 (CPU, ~10–20 phút).

Ra trong --out:
  train_ra.jsonl    : câu nhắc S1 + khối ví dụ truy hồi (cho_train: bỏ chính tác vụ, k 2..6, 15% rỗng, 10% ngẫu nhiên)
  train_cont.jsonl  : CÙNG hàng, CÙNG thứ tự, CÙNG đích, câu nhắc S1 không khối (đối chứng "SFT thêm")
  ex_test_k4.jsonl  : 4 ví dụ cố định (cho_test) cho 4.463 bước click của test — chỉ đọc mục tiêu, lịch sử, OCR
  ex_val_k4.jsonl   : như trên cho các bước click của p1_val_rows (val lớn)
  build_stats.json

Kho truy hồi = train_tru_val.jsonl bỏ mọi tác vụ của p1_val_rows. Tác vụ test chung kho phải = 0.

  python ra_build.py --bundle B --kho train_tru_val.jsonl --test-recs T/test.jsonl --test-ocr T/ocr.jsonl --out O
  python ra_build.py ... --n-train 50          # chạy thử
"""
import os, sys, json, random, argparse, collections, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ra_exemplars as RA
from build_branch_data import prompt_body

TAPT = ("click", "long_press")


def doc(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")]


def la_cham(r):
    a = r.get("action") or {}
    return a.get("action_type") in TAPT and "x" in a


def ocr_toks(o):
    return {w for it in (o or {"items": []})["items"][:24] for w in RA.tok(it.get("text", ""))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--kho", required=True)
    ap.add_argument("--test-recs", default=None, help="bắt buộc khi không có --chi-train")
    ap.add_argument("--test-ocr", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=2026100901)
    ap.add_argument("--n-train", type=int, default=0, help="0 = mọi hàng p1_train_rows")
    ap.add_argument("--chi-train", action="store_true", help="bỏ qua xuất ex_test_k4/ex_val_k4 (đã có sẵn trong gói)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()

    tr = doc(os.path.join(a.bundle, "p1_train_rows.jsonl"))
    va = doc(os.path.join(a.bundle, "p1_val_rows.jsonl"))
    assert a.chi_train or (a.test_recs and a.test_ocr), "⛔ cần --test-recs và --test-ocr, hoặc --chi-train"
    te = doc(a.test_recs) if a.test_recs else []
    assert not te or len(te) == 6958, f"⛔ test.jsonl có {len(te)} dòng"
    vep = {r["episode_id"] for r in va}
    ocr = {o["image"]: o for o in doc(os.path.join(a.bundle, "ocr.jsonl"))}
    tocr = {o["image"]: o for o in doc(a.test_ocr)} if a.test_ocr else {}

    kho = RA.Kho(doc(a.kho), loai_ep=vep)
    tep = {r["episode_id"] for r in te}
    chung_test = len(tep & set(kho.eid)) if te else 0
    print(f"[kho] {len(kho.tr)} bước · {len(kho.eid)} tác vụ · bỏ {len(vep)} tác vụ val · "
          f"{chung_test} tác vụ test chung kho", flush=True)
    assert chung_test == 0, "⛔ kho chứa tác vụ test"
    assert len(kho.tr) > 60000, "⛔ kho quá nhỏ — sai tệp train_tru_val?"

    bo = collections.Counter()
    rows = []
    for r in tr:
        gold = (r.get("target_instruction") or "").strip()
        if not gold:
            bo["rong"] += 1
            continue
        if r["episode_id"] in vep:
            bo["trung_val"] += 1
            continue
        if not os.path.exists(os.path.join(a.bundle, r["image"])):
            bo["thieu_anh"] += 1
            continue
        if r["image"] not in ocr:
            bo["thieu_ocr"] += 1
            continue
        rows.append(r)
    assert bo["trung_val"] == 0, "⛔ p1_train_rows chạm tác vụ val"
    rng = random.Random(a.seed)
    rng.shuffle(rows)
    if a.n_train:
        rows = rows[:a.n_train]
    print(f"[train] {len(rows)} hàng · bỏ {dict(bo)} · loại thao tác "
          f"{dict(collections.Counter((r.get('action') or {}).get('action_type') for r in rows))}", flush=True)

    st = collections.Counter()
    with open(os.path.join(a.out, "train_ra.jsonl"), "w", encoding="utf-8") as fr, \
         open(os.path.join(a.out, "train_cont.jsonl"), "w", encoding="utf-8") as fc:
        for i, r in enumerate(rows):
            gold = r["target_instruction"].strip()
            body = prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
            ex = kho.cho_train(r, gold, r["episode_id"], rng)
            body_ra = RA.chen(body, ex) if ex else body
            assert body_ra.startswith(body[:-len(RA.LAST)]), "⛔ phần đầu câu nhắc RA khác câu nhắc S1"
            st["n"] += 1
            st["co_khoi"] += bool(ex)
            st["khoi_chua_dich"] += bool(ex) and any(RA.tok(e["sent"]) == RA.tok(gold) for e in ex)
            st["so_vi_du"] += len(ex) if ex else 0
            key = f"{r['episode_id']}_{r['step_id']}"
            img = os.path.join(a.bundle, r["image"])
            fr.write(json.dumps(dict(key=key, image=img, body=body_ra, gold=gold), ensure_ascii=False) + "\n")
            fc.write(json.dumps(dict(key=key, image=img, body=body, gold=gold), ensure_ascii=False) + "\n")
            if (i + 1) % 1000 == 0:
                print(f"  train {i+1}/{len(rows)} · {(time.time()-t0)/60:.1f} phút", flush=True)

    def xuat(recs, oc, path, tinh_dich):
        hit, n = 0, 0
        with open(path, "w", encoding="utf-8") as f:
            for r in recs:
                if not la_cham(r):
                    continue
                x = dict(goal=r["goal"], history=r.get("history") or [])
                ex = [dict(sent=e["sent"], goal=e["goal"], prev=e["prev"])
                      for e in kho.cho_test(x, 4, ocr_toks(oc.get(r["image"])))]
                n += 1
                if tinh_dich:
                    g = (r.get("target_instruction") or r.get("gold_instruction") or "").strip()
                    hit += any(RA.tok(e["sent"]) == RA.tok(g) for e in ex)
                f.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "exemplars": ex},
                                   ensure_ascii=False) + "\n")
        return n, hit

    nt = nv = hv = 0
    if not a.chi_train:
        nt, _ = xuat(te, tocr, os.path.join(a.out, "ex_test_k4.jsonl"), tinh_dich=False)
        assert nt == 4463, f"⛔ test có {nt} bước click"
        nv, hv = xuat(va, ocr, os.path.join(a.out, "ex_val_k4.jsonl"), tinh_dich=True)

    S = dict(
        train_rows=st["n"],
        train_co_khoi_pct=round(100 * st["co_khoi"] / max(st["n"], 1), 1),
        train_khoi_chua_dich_pct=round(100 * st["khoi_chua_dich"] / max(st["co_khoi"], 1), 1),
        train_so_vi_du_tb=round(st["so_vi_du"] / max(st["co_khoi"], 1), 2),
        test_click=nt, val_click=nv, val_khoi_chua_dich_pct=round(100 * hv / max(nv, 1), 1),
        kho_buoc=len(kho.tr), bo=dict(bo), seed=a.seed, phut=round((time.time() - t0) / 60, 1),
    )
    json.dump(S, open(os.path.join(a.out, "build_stats.json"), "w"), ensure_ascii=False, indent=1)
    print("[xong]", json.dumps(S, ensure_ascii=False), flush=True)
    vd = next(json.loads(l) for l in open(os.path.join(a.out, "train_ra.jsonl"), encoding="utf-8")
              if RA.HEADER in json.loads(l)["body"])
    print("--- ví dụ câu nhắc RA ---\n" + vd["body"] + "\n--- đích: " + vd["gold"], flush=True)


if __name__ == "__main__":
    main()
