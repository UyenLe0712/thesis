# -*- coding: utf-8 -*-
"""Độ đo văn bản TẬP KIỂM cho Dr.GRPO đầy đủ + SPICE (kernel luoi-test-u-5, 22/11/2026) — CPU + Java 8 (Kaggle CPU).

    python -u chu_drgrpo_22_11.py [--B 2000] [--chi-cache]     # → runs/chu_drgrpo_22_11.json

Cùng cách tính với chu_match_17_11 (4.463 bước chạm, bootstrap cụm app, CIDEr-D IDF câu chuẩn, METEOR mức kho không KTC).
S1/101, ck500, SFT tiếp nạp từ cache (chu_drgrpo_cache/*.npz, lấy từ kernel chu-match-17-11); Dr.GRPO và A/A tính mới.
Tự kiểm: mức kho S1/ck500/SFT tiếp/A/A phải trùng số đã lưu (report/334) — lệch thì dừng.
--chi-cache: bỏ hai nhánh tính mới, chỉ kiểm cache (chạy thử ở máy nhà).
"""
import argparse, json

import ktc_chu_27_10 as K

R = K.RUNS
DR, AA = "Dr.GRPO đầy đủ", "GRPO A/A"
NH = {"S1/101": "score_s1_seed101_raw.jsonl", "ck500": "score_ck500_test_raw.jsonl",
      "SFT tiếp": "rows_sft_tiep_101.jsonl", AA: "score_grpo_spice_aa_101_test_raw.jsonl",
      DR: "score_drgrpo_full_spice_101_test_raw.jsonl"}
# (bleu4, rougeL, cider_d, spice, chrf, bert) đã lưu — report/334
K.DA.update({"SFT tiếp": (52.07, 68.55, 425.79, 45.33, 62.64, 67.05),
             AA: (52.97, 68.44, 430.92, 46.00, 62.39, 67.09)})
MOI = (DR, AA)
SO = [(DR, m) for m in ("ck500", AA, "SFT tiếp", "S1/101")]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--chi-cache", action="store_true"); a = ap.parse_args()
    K.CACHE = R / "chu_drgrpo_cache"
    nh, so = dict(NH), list(SO)
    if a.chi_cache:
        for t in MOI:
            nh.pop(t)
        so = [("ck500", "S1/101")]
    for t in nh:
        if t not in MOI:
            c = K.CACHE / (t.replace("/", "_").replace(" ", "_") + ".npz")
            assert c.exists(), f"⛔ thiếu cache {c.name}"
    rows = [json.loads(l) for l in open(R / NH[DR], encoding="utf-8")]
    assert len(rows) == 4463, len(rows)
    print("câu trống Dr.GRPO:", [K.kh(r) for r in rows if not (r.get("sent") or "").strip()], flush=True)
    app = {K.kh(r): (r.get("app") or f"ep{r['episode_id']}") for r in map(json.loads, open(R / NH["S1/101"], encoding="utf-8"))}
    dich = R / ("chu_drgrpo_22_11" + ("_chi_cache" if a.chi_cache else "") + ".json")
    out = {"B": a.B, "ghi_chu": "TẬP KIỂM 4.463 bước chạm; bootstrap cụm app; CIDEr-D IDF câu chuẩn; METEOR không KTC; một hạt giống"}
    K.nhom("AndroidControl", nh, so, lambda r: app[K.kh(r)], a.B, out, dich)
    print("→", dich, flush=True)


if __name__ == "__main__":
    main()
