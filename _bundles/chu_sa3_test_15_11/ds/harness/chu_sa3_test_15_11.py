# -*- coding: utf-8 -*-
"""Độ đo văn bản TẬP KIỂM cho SA-SPICE-v3 ck400 (kernel sa3-test-ck400, 15/11/2026) — CPU + Java 8 (Kaggle CPU).

    python -u chu_sa3_test_15_11.py [--B 2000] [--khong-sa]     # → runs/chu_sa3_test_15_11.json

4.463 bước chạm, cùng cách tính với ktc_chu_27_10 / chu_ppo_tam_13_11 (bootstrap cụm app, CIDEr-D IDF của câu chuẩn
4.463 bước, METEOR mức kho không KTC). Chín lượt cũ nạp điểm từng bước từ cache đủ tập của kernel chu-ppo-du-14-11
(chu_sa3_test_cache/*.npz); chỉ SA ck400 phải tính mới.
Tự kiểm: mức kho của chín lượt cũ phải trùng số đã lưu (report/334 bảng văn bản) — lệch thì dừng.
--khong-sa: bỏ SA, chỉ kiểm cache + số đã lưu (chạy thử ở máy nhà).
"""
import argparse, json, sys

import ktc_chu_27_10 as K

R = K.RUNS
NH = {"S1/101": "score_s1_seed101_raw.jsonl", "ck500": "score_ck500_test_raw.jsonl",
      "SFT tiếp": "rows_sft_tiep_101.jsonl", "GRPO + SPICE (A/A)": "rows_grpo_spice_aa_101.jsonl",
      "SCST + SPICE": "rows_scst_spice_101.jsonl", "GRPO + ROUGE-L": "rows_grpo_rougel_101.jsonl",
      "GRPO + METEOR": "rows_grpo_meteor_101.jsonl", "GRPO + CIDEr-D": "rows_grpo_cider_101.jsonl",
      "xao101": "score_ck500_xao101_test_raw.jsonl",
      "SA-SPICE-v3 ck400": "score_sa_ck400_test_raw.jsonl"}
# số mức kho đã lưu (bleu4, rougeL, cider_d, spice, chrf, bert) — report/334, chu_luoi_8_11b.json
K.DA.update({"SFT tiếp": (52.07, 68.55, 425.79, 45.33, 62.64, 67.05),
             "GRPO + SPICE (A/A)": (52.97, 68.44, 430.92, 46.00, 62.39, 67.09),
             "SCST + SPICE": (51.97, 68.70, 430.89, 45.93, 63.31, 67.25),
             "GRPO + ROUGE-L": (52.59, 69.27, 432.81, 45.57, 63.42, 67.57),
             "GRPO + METEOR": (50.76, 69.14, 426.61, 45.13, 64.19, 67.35),
             "GRPO + CIDEr-D": (51.59, 68.47, 424.52, 44.43, 62.90, 67.03)})
SA = "SA-SPICE-v3 ck400"
SO = [(SA, m) for m in ("SFT tiếp", "ck500", "S1/101", "GRPO + SPICE (A/A)", "SCST + SPICE", "GRPO + ROUGE-L",
                        "GRPO + METEOR", "GRPO + CIDEr-D", "xao101")] + [("ck500", "S1/101"), ("SFT tiếp", "S1/101")]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--khong-sa", action="store_true"); a = ap.parse_args()
    K.CACHE = R / "chu_sa3_test_cache"
    nh, so = dict(NH), list(SO)
    if a.khong_sa:
        nh.pop(SA); so = [p for p in so if SA not in p]
    for t, f in nh.items():
        if t != SA:
            c = K.CACHE / (t.replace("/", "_").replace(" ", "_") + ".npz")
            assert c.exists(), f"⛔ thiếu cache {c.name} (bung chu_cache.zip của chu-ppo-du-14-11)"
    sa_rows = [json.loads(l) for l in open(R / NH[SA], encoding="utf-8")]
    trong = [K.kh(r) for r in sa_rows if not (r.get("sent") or "").strip()]
    assert len(sa_rows) == 4463 and trong == [("18710", "1")], trong   # cùng bước S1 cũng trống
    app = {K.kh(r): (r.get("app") or f"ep{r['episode_id']}") for r in map(json.loads, open(R / NH["S1/101"], encoding="utf-8"))}
    dich = R / ("chu_sa3_test_15_11" + ("_khong_sa" if a.khong_sa else "") + ".json")
    out = {"B": a.B, "ghi_chu": "TẬP KIỂM 4.463 bước chạm; bootstrap cụm app; CIDEr-D IDF câu chuẩn; METEOR không KTC; một hạt giống"}
    K.nhom("AndroidControl", nh, so, lambda r: app[K.kh(r)], a.B, out, dich)
    print("→", dich, flush=True)


if __name__ == "__main__":
    main()
