# -*- coding: utf-8 -*-
"""Độ đo văn bản 8/11/2026 bản b: thêm ck500 hạt 202 vào cùng khung KTC và so mọi lượt lưới với A/A — 0 GPU, CPU + Java 8.

    python -u chu_luoi_8_11b.py [--B 2000]    # ghi runs/chu_luoi_8_11b.json

Dùng lại cache từng bước của chu-luoi-8-11-cpu (11 lượt), chỉ tính mới ck500/202 (đối chiếu số đã lưu ở DA).
Tự kiểm: mọi phép so đã có ở chu_luoi_8_11.json phải ra TRÙNG tuyệt đối (cùng hạt bootstrap, chỉ số mẫu không phụ thuộc
số nhánh) và METEOR 11 lượt cũ trùng.
"""
import argparse, json, sys

import ktc_chu_27_10 as K
import chu_luoi_8_11 as C

AA, S202 = "GRPO + SPICE (A/A)", "ck500/202"
AC = dict(C.AC); AC[S202] = "score_ck500_s202_test_raw.jsonl"
LUOI = ["SCST + SPICE", "GRPO + CIDEr-D", "GRPO + METEOR", "GRPO + ROUGE-L", "SFT tiếp", "REINFORCE + SPICE", "RLOO + SPICE"]
SO = (list(C.SO) + [(t, AA) for t in LUOI]
      + [(AA, S202), ("ck500", S202), (S202, "S1/101"), (S202, "SFT tiếp")] + [(t, S202) for t in LUOI])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=2000); a = ap.parse_args()
    dich = K.RUNS / "chu_luoi_8_11b.json"
    out = {"B": a.B, "ghi_chu": "bootstrap cụm app; METEOR không có KTC; một hạt giống"}
    s1 = {(str(r["episode_id"]), str(r["step_id"])): (r.get("app") or f"ep{r['episode_id']}")
          for r in map(json.loads, open(K.RUNS / AC["S1/101"], encoding="utf-8"))}
    K.nhom("AndroidControl", AC, SO, lambda r: s1[(str(r["episode_id"]), str(r["step_id"]))], a.B, out, dich)
    o = out["AndroidControl"]
    cu = json.load(open(K.RUNS / "chu_luoi_8_11.json", encoding="utf-8"))["AndroidControl"]
    loi = [f"so {k}" for k, v in cu["so"].items() if o["so"].get(k) != v]
    loi += [f"diem {k}" for k, v in cu["diem"].items() if o["diem"].get(k) != v]
    loi += [f"METEOR {k}" for k, v in cu["meteor"].items() if abs(o["meteor"][k] - v) > 0.011]
    out["tu_kiem"] = loi or "đạt"
    json.dump(out, open(dich, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("tự kiểm:", out["tu_kiem"], flush=True)
    if loi:
        sys.exit("⛔ không trùng chu_luoi_8_11.json: " + " · ".join(loi[:10]))
    print("→", dich, flush=True)


if __name__ == "__main__":
    main()
