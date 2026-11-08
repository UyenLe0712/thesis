# -*- coding: utf-8 -*-
"""Độ đo văn bản (bảy thước của report/320 mục 3) + KTC ghép cặp cho các lượt lưới RL đã sinh câu test (đợt 2/11 + đợt 7/11: SFT tiếp · REINFORCE · RLOO) — 0 GPU, CPU + Java 8.

    python -u chu_luoi_7_11.py [--B 2000] [--smoke 60]    # ghi runs/chu_luoi_7_11.json

Dùng nguyên hàm của ktc_chu_27_10.py nên cùng cách tính và cùng hạt bootstrap. S1/101, ck500, xao101 được tính lại và
phải khớp số đã lưu, lệch là dừng. Bốn lượt đọc từ rows_*.jsonl dựng từ tệp pred (đủ 4.463 câu), câu chuẩn lấy của S1/101.
"""
import argparse, json, sys

import ktc_chu_27_10 as K

AC = {"S1/101": "score_s1_seed101_raw.jsonl", "ck500": "score_ck500_test_raw.jsonl",
      "xao101": "score_ck500_xao101_test_raw.jsonl", "SCST + SPICE": "rows_scst_spice_101.jsonl",
      "GRPO + CIDEr-D": "rows_grpo_cider_101.jsonl", "GRPO + METEOR": "rows_grpo_meteor_101.jsonl",
      "GRPO + ROUGE-L": "rows_grpo_rougel_101.jsonl", "SFT tiếp": "rows_sft_tiep_101.jsonl",
      "REINFORCE + SPICE": "rows_reinforce_spice_101.jsonl", "RLOO + SPICE": "rows_rloo_spice_101.jsonl"}
LUOT = [t for t in AC if t not in ("S1/101", "ck500", "xao101")]
SO = ([(t, m) for t in LUOT for m in ("ck500", "S1/101")] + [("ck500", "S1/101"), ("ck500", "xao101")]
      + [("REINFORCE + SPICE", "SFT tiếp"), ("RLOO + SPICE", "SFT tiếp")])
METEOR_DA = {"S1/101": 36.79, "ck500": 37.92, "xao101": 36.95}
KTC_DA = {"spice": (1.42, 0.71, 2.16), "cider_d": (13.93, 8.05, 19.91)}   # ck500 − S1/101, report/320 §3.2


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=2000); ap.add_argument("--smoke", type=int, default=0)
    a = ap.parse_args()
    dich = K.RUNS / "chu_luoi_7_11.json"
    if a.smoke:                                    # chạy thử: cắt tệp, tắt đối chiếu số đã lưu
        K.DA.clear()
    out = {"B": a.B, "ghi_chu": "bootstrap cụm app; METEOR không có KTC; một hạt giống"}
    s1 = {(str(r["episode_id"]), str(r["step_id"])): (r.get("app") or f"ep{r['episode_id']}")
          for r in map(json.loads, open(K.RUNS / AC["S1/101"], encoding="utf-8"))}
    K.nhom("AndroidControl", AC, SO, lambda r: s1[(str(r["episode_id"]), str(r["step_id"]))], a.B, out, dich)
    o = out["AndroidControl"]
    if not a.smoke:
        loi = [f"METEOR {t} {o['meteor'][t]} ≠ {v}" for t, v in METEOR_DA.items() if abs(o["meteor"][t] - v) > 0.06]
        for k, ref in KTC_DA.items():
            g = o["so"]["ck500 − S1/101"][k]
            if max(abs(g["delta"] - ref[0]), abs(g["lo"] - ref[1]), abs(g["hi"] - ref[2])) > (0.5 if k == "cider_d" else 0.1):
                loi.append(f"KTC ck500 − S1/101 {k} {g} ≠ {ref}")
        out["tu_kiem"] = loi or "đạt"
        json.dump(out, open(dich, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("tự kiểm:", out["tu_kiem"], flush=True)
        if loi:
            sys.exit("⛔ " + " · ".join(loi))
    print("→", dich, flush=True)


if __name__ == "__main__":
    main()
