# -*- coding: utf-8 -*-
"""Độ đo văn bản TẬP KIỂM cho SPICE-MATCH ck400 (kernel sa3-test-match, 17/11/2026) — CPU + Java 8 (Kaggle CPU).

    python -u chu_match_17_11.py [--B 2000] [--khong-match]     # → runs/chu_match_17_11.json

Cùng cách tính với chu_sa3_test_15_11 (4.463 bước chạm, bootstrap cụm app, CIDEr-D IDF câu chuẩn, METEOR mức kho không KTC).
Bốn nhánh so sánh nạp điểm từng bước từ cache của kernel chu-sa3-test-15-11 (chu_match_cache/*.npz); chỉ MATCH tính mới.
Tự kiểm: mức kho của bốn nhánh cũ phải trùng số đã lưu (report/334) — lệch thì dừng.
--khong-match: bỏ MATCH, chỉ kiểm cache + số đã lưu (chạy thử ở máy nhà).
"""
import argparse, json

import ktc_chu_27_10 as K

R = K.RUNS
NH = {"S1/101": "score_s1_seed101_raw.jsonl", "ck500": "score_ck500_test_raw.jsonl",
      "SFT tiếp": "rows_sft_tiep_101.jsonl", "SA-SPICE-v3 ck400": "score_sa_ck400_test_raw.jsonl",
      "SPICE-MATCH ck400": "score_match_ck400_test_raw.jsonl"}
# số mức kho đã lưu (bleu4, rougeL, cider_d, spice, chrf, bert) — report/334, chu_sa3_test_15_11.json
K.DA.update({"SFT tiếp": (52.07, 68.55, 425.79, 45.33, 62.64, 67.05),
             "SA-SPICE-v3 ck400": (51.24, 69.31, 429.12, 45.76, 64.40, 67.59)})
MA = "SPICE-MATCH ck400"
SO = [(MA, m) for m in ("SA-SPICE-v3 ck400", "SFT tiếp", "ck500", "S1/101")] + [("SA-SPICE-v3 ck400", "SFT tiếp")]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--khong-match", action="store_true"); a = ap.parse_args()
    K.CACHE = R / "chu_match_cache"
    nh, so = dict(NH), list(SO)
    if a.khong_match:
        nh.pop(MA); so = [p for p in so if MA not in p]
    for t in nh:
        if t != MA:
            c = K.CACHE / (t.replace("/", "_").replace(" ", "_") + ".npz")
            assert c.exists(), f"⛔ thiếu cache {c.name} (bung chu_cache.zip của chu-sa3-test-15-11)"
    rows = [json.loads(l) for l in open(R / NH[MA], encoding="utf-8")]
    trong = [K.kh(r) for r in rows if not (r.get("sent") or "").strip()]
    assert len(rows) == 4463 and trong == [("18710", "1")], trong   # cùng bước S1 cũng trống
    app = {K.kh(r): (r.get("app") or f"ep{r['episode_id']}") for r in map(json.loads, open(R / NH["S1/101"], encoding="utf-8"))}
    dich = R / ("chu_match_17_11" + ("_khong_match" if a.khong_match else "") + ".json")
    out = {"B": a.B, "ghi_chu": "TẬP KIỂM 4.463 bước chạm; bootstrap cụm app; CIDEr-D IDF câu chuẩn; METEOR không KTC; một hạt giống"}
    K.nhom("AndroidControl", nh, so, lambda r: app[K.kh(r)], a.B, out, dich)
    print("→", dich, flush=True)


if __name__ == "__main__":
    main()
