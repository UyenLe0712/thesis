# -*- coding: utf-8 -*-
"""Độ đo văn bản TẠM cho PPO λ=1 / λ=0,95 (ck1000) trên phần câu test đã sinh ở kernel luoi-test-t-ppo (12/11/2026)
— 0 GPU, CPU + Java 8.

    python -u chu_ppo_tam_13_11.py [--B 2000] [--smoke 40]     # ghi runs/chu_ppo_tam_13_11.json

Phiên Kaggle bị cắt ở trần giờ nên PPO λ=1 mới có 2.622 câu, λ=0,95 có 2.641 câu, đều là ĐOẠN ĐẦU của thứ tự tệp thô
S1/101. Mọi nhánh (11 lượt đã có + 2 PPO) bị cắt về đúng N bước chung đầu tiên rồi tính lại từ đầu trên tập con ⇒
CIDEr-D dùng IDF của tập con cho mọi nhánh, nên số tuyệt đối KHÔNG so được với số 4.463 bước; chỉ đọc các phép so
ghép cặp trong tệp này. Đoạn đầu không phải mẫu ngẫu nhiên. Khi đủ 4.463 câu thì chạy lại bằng chu_luoi_8_11*.

Tự kiểm: các thành phần từng bước không phụ thuộc tập (n-gram BLEU, ROUGE-L, SPICE, thống kê chrF, BERTScore) của
S1/101 và ck500 trên tập con phải trùng N dòng đầu cache đủ tập ktc_chu_27_10_cache (BERTScore lệch ≤ 1e-4).
"""
import argparse, json, sys
from pathlib import Path

import numpy as np

import ktc_chu_27_10 as K

DU = {"S1/101": "score_s1_seed101_raw.jsonl", "ck500": "score_ck500_test_raw.jsonl",
      "xao101": "score_ck500_xao101_test_raw.jsonl", "SCST + SPICE": "rows_scst_spice_101.jsonl",
      "GRPO + CIDEr-D": "rows_grpo_cider_101.jsonl", "GRPO + METEOR": "rows_grpo_meteor_101.jsonl",
      "GRPO + ROUGE-L": "rows_grpo_rougel_101.jsonl", "SFT tiếp": "rows_sft_tiep_101.jsonl",
      "REINFORCE + SPICE": "rows_reinforce_spice_101.jsonl", "RLOO + SPICE": "rows_rloo_spice_101.jsonl",
      "GRPO + SPICE (A/A)": "rows_grpo_spice_aa_101.jsonl"}
PPO = {"PPO λ=1": "pred_ppo_l1_101_test.jsonl", "PPO λ=0,95": "pred_ppo_l95_101_test.jsonl"}
MOC = ["ck500", "S1/101", "SFT tiếp", "GRPO + SPICE (A/A)", "SCST + SPICE", "RLOO + SPICE", "REINFORCE + SPICE"]
SO = ([(p, m) for p in PPO for m in MOC] + [("PPO λ=1", "PPO λ=0,95"), ("ck500", "S1/101"), ("ck500", "SFT tiếp")])
kh = lambda r: (str(r["episode_id"]), str(r["step_id"]))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=2000); ap.add_argument("--smoke", type=int, default=0)
    a = ap.parse_args()
    R = K.RUNS
    s1 = [json.loads(l) for l in open(R / DU["S1/101"], encoding="utf-8")]
    thu_tu = [kh(r) for r in s1]
    pp = {t: [json.loads(l) for l in open(R / f, encoding="utf-8")] for t, f in PPO.items()}
    for t, P in pp.items():                         # phải là đoạn đầu liền của thứ tự S1
        assert [kh(r) for r in P] == thu_tu[:len(P)], f"⛔ {t} không phải đoạn đầu thứ tự S1/101"
    N = min(len(P) for P in pp.values())
    if a.smoke:
        N = min(N, a.smoke)
    print(f"[tập con] N = {N} bước đầu (PPO: " + ", ".join(f"{t} {len(P)}" for t, P in pp.items()) + ")", flush=True)
    giu = set(thu_tu[:N])
    vang = {kh(r): r for r in s1}
    T = R / "tam_ppo"; T.mkdir(exist_ok=True)
    NH = {}
    for t, f in DU.items():
        rows = [r for r in map(json.loads, open(R / f, encoding="utf-8")) if kh(r) in giu]
        assert len(rows) == N, f"⛔ {t}: {len(rows)} ≠ {N}"
        ten = "tam_ppo/" + f
        with open(R / ten, "w", encoding="utf-8") as g:
            for r in rows:
                g.write(json.dumps(r, ensure_ascii=False) + "\n")
        NH[t] = ten
    for t, P in pp.items():
        ten = f"tam_ppo/rows_{PPO[t].replace('pred_', '').replace('_test', '')}"
        with open(R / ten, "w", encoding="utf-8") as g:
            for r in P[:N]:
                v = vang[kh(r)]
                g.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "sent": r.get("pred") or "",
                                    "gold_instruction": v.get("gold_instruction"), "app": v.get("app")},
                                   ensure_ascii=False) + "\n")
        NH[t] = ten
        print(f"  {t}: câu trống {sum(not (r.get('pred') or '').strip() for r in P[:N])}", flush=True)

    cache_du = K.CACHE
    K.CACHE = R / "chu_ppo_tam_cache"
    K.DA.clear()                                    # tập con: không có số đã lưu để đối chiếu
    dich = R / "chu_ppo_tam_13_11.json"
    out = {"B": a.B, "N": N, "ghi_chu": ("ĐỦ 4.463 bước; " if N == len(thu_tu) else "TẠM: N bước đầu thứ tự S1/101 (không ngẫu nhiên); ") + "CIDEr-D IDF của tập con; "
                                        "chỉ đọc phép so ghép cặp; bootstrap cụm app; METEOR không có KTC; một hạt giống"}
    app = {kh(r): (r.get("app") or f"ep{r['episode_id']}") for r in s1}
    K.nhom("AndroidControl_tap_con", NH, SO, lambda r: app[kh(r)], a.B, out, dich)

    loi = []
    for t, c in (("S1/101", "S1_101.npz"), ("ck500", "ck500.npz")):
        f = cache_du / c
        if not f.exists():
            loi.append(f"thiếu cache {c}"); continue
        du = dict(np.load(f)); tc = dict(np.load(K.CACHE / c))
        for k in ("cor", "gue", "tl", "rl", "rouge", "spice", "chrf_st", "bert"):
            d = float(np.abs(du[k][:N] - tc[k]).max())
            if d > (1e-4 if k == "bert" else 1e-9):
                loi.append(f"{t} {k} lệch {d:.2g}")
    out["tu_kiem"] = loi or "đạt"
    json.dump(out, open(dich, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("tự kiểm:", out["tu_kiem"], flush=True)
    if loi and not a.smoke:
        sys.exit("⛔ " + " · ".join(loi))
    print("→", dich, flush=True)


if __name__ == "__main__":
    main()
