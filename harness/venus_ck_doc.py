# -*- coding: utf-8 -*-
"""Ghép kết quả UI-Venus của S1/101, ck500, R3 trên đủ 4.463 bước chạm (0 GPU).
Một câu ở một bước chỉ cần chấm một lần: kết quả tra theo (bước, câu). Câu rỗng tính exec = 0.
Δ ghép cặp + KTC95 bootstrap theo cụm app (score_run.cluster_bootstrap) + McNemar chính xác."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import score_run as S
R = os.path.join(HERE, "..", "runs")
def L(p): return {(o["episode_id"], o["step_id"]): o for o in map(json.loads, open(p, encoding="utf-8"))}
F = {"s1": "score_s1_seed101_raw.jsonl", "ck500": "grpo_spice/score_ck500_test_raw.jsonl", "r3": "ra304_luat/score_R3_test_raw.jsonl"}
Z = {n: L(os.path.join(R, p)) for n, p in F.items()}
V = {}
for p in ["venus/score_venus_s1_2532_raw.jsonl"] + [f"venus/ck500_r3_22_10/score_{n}_raw.jsonl" for n in ("s1", "ck500", "r3")] + ["venus/bu_22_10/score_m1_raw.jsonl"]:
    for k, o in L(os.path.join(R, p)).items():
        if "sent" in o: V[(k, o["sent"].strip())] = int(o["executable"])
APP = {k: (o.get("app") or f"ep{k[0]}") for k, o in Z["s1"].items()}
res, thieu = {n: {} for n in Z}, 0
for k in Z["s1"]:
    for n in Z:
        s = (Z[n][k].get("sent") or "").strip()
        if not s: res[n][k] = 0
        elif (k, s) in V: res[n][k] = V[(k, s)]
        else: thieu += 1; res[n][k] = None
assert thieu == 0, f"thiếu {thieu} lượt chấm"
K = sorted(Z["s1"]); print("bước:", len(K), "· khác nhau:", sum(1 for k in K if len({(Z[n][k].get('sent') or '').strip() for n in Z}) > 1))
for n in Z: print(f"  {n:6s} Venus exec = {100*sum(res[n].values())/len(K):.2f}")
def so(a, b):
    d = {k: res[a][k] - res[b][k] for k in K}
    pt, (lo, hi), G, _ = S.cluster_bootstrap(list(d.items()), lambda u: APP[u[0]], lambda u: u[1])
    x = sum(v > 0 for v in d.values()); y = sum(v < 0 for v in d.values()); n = x + y
    p = min(1, 2 * sum(math.comb(n, i) for i in range(min(x, y) + 1)) / 2 ** n) if n else 1
    print(f"  {a:6s}-{b:6s} Δ={100*pt:+.2f} [{100*lo:+.2f}; {100*hi:+.2f}] b={x} c={y} p={p:.3g}")
for a, b in (("ck500", "s1"), ("r3", "s1"), ("r3", "ck500")): so(a, b)
