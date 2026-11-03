# -*- coding: utf-8 -*-
"""Diễn biến lúc train của các lượt RL từ log (H-I, report/328): entropy, tỉ lệ nhóm thưởng bằng nhau, KL, độ dài câu — 0 GPU.

Ghép log nhiều commit theo epoch, trùng thì giữ bản sau. So 262 bước đầu với 75 bước cuối như report/328; lượt chưa đủ 400 bước chỉ in cửa sổ đầu.
Số thưởng là số train, không trích làm kết quả. Ghi runs/luoi/test_2_11/dien_bien_train.json.
"""
import ast, glob, json, os, re
K = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "runs")
L = lambda *p: [f for q in p for f in sorted(glob.glob(os.path.join(K, q)))]
N = {"ck500": L("grpo_spice/train_c1.log", "grpo_spice/train_c3.log"), "xao101": L("xao101/c1/train.log", "xao101/c2/train.log")}
for t in ("scst_spice_101", "grpo_cider_101", "grpo_meteor_101", "grpo_rougel_101", "rloo_spice_101", "reinforce_spice_101", "grpo_spice_101"):
    N[t] = L(f"luoi/lo1/*/{t}.train.log", f"luoi/lo2/*/{t}/train.log", f"luoi/lo3/*/{t}/train.log")
COT = {"entropy": "entropy", "frac_reward_zero_std": "nhom_bang", "kl": "kl", "completions/mean_length": "do_dai", "reward": "thuong"}


def doc(fs):
    D = {}
    for f in fs:
        for l in open(f, encoding="utf-8", errors="ignore"):
            if l.startswith("{'loss'"):
                try:
                    x = ast.literal_eval(l.strip())
                    D[float(x["epoch"])] = {v: float(x[k]) for k, v in COT.items() if k in x}
                except Exception:
                    pass
    return [D[k] for k in sorted(D)]


tb = lambda R, k: round(sum(r[k] for r in R if k in r) / max(1, sum(k in r for r in R)), 4)
out = {}
for t, fs in N.items():
    R = doc(fs)
    o = {"so_buoc": len(R), "tep": [os.path.relpath(f, K) for f in fs]}
    if R:
        o["dau_262"] = {k: tb(R[:262], k) for k in COT.values()}
        if len(R) >= 400:
            o["cuoi_75"] = {k: tb(R[-75:], k) for k in COT.values()}
    out[t] = o
    print(t, {k: v for k, v in o.items() if k != "tep"}, flush=True)
print("đối chiếu report/328 H-I: ck500 entropy 0,52 → 0,34; nhóm bằng nhau 20,2% → 31,3%", flush=True)
json.dump(out, open(os.path.join(K, "luoi/test_2_11/dien_bien_train.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
