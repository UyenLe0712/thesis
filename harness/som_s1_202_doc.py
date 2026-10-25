# -*- coding: utf-8 -*-
"""Phi-4 người nghe: S1/202 so với ck500 và R3 (0 GPU). Chạy: python3 -I harness/som_s1_202_doc.py
S1/202 chỉ được chấm ở bước câu khác S1/101 (tệp *_s1_202_diff); bước hai câu giống nhau lấy kết quả S1/101.
Câu rỗng tính 0. Δ ghép cặp + KTC95 bootstrap cụm app + McNemar chính xác."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import score_run as S
R = os.path.join(HERE, "..", "runs")
key = lambda o: (str(o["episode_id"]), str(o["step_id"]))
def L(p): return {key(o): o for o in map(json.loads, open(os.path.join(R, p), encoding="utf-8"))}
sc = {n: L(p) for n, p in {"s1_101": "score_s1_seed101_raw.jsonl", "s1_202": "score_s1_seed202_raw.jsonl",
      "ck500": "grpo_spice/score_ck500_test_raw.jsonl", "r3": "ra304_luat/score_R3_test_raw.jsonl"}.items()}
ph = {"s1_101": L("som/chon_phi4_s1_101.jsonl"), "ck500": L("som/chon_phi4_ck500.jsonl"),
      "r3": L("som/chon_phi4_r3.jsonl"), "diff": L("som/chon_phi4_s1_202_diff.jsonl")}
K = sorted(sc["s1_101"]); assert all(set(v) == set(K) for v in list(sc.values()) + list(ph.values()))
sent = lambda n, k: (sc[n][k].get("sent") or "").strip()
res = {n: {} for n in ("s1_101", "s1_202", "ck500", "r3")}
dung_chung = 0
for k in K:
    for n in ("s1_101", "ck500", "r3"): res[n][k] = int(ph[n][k]["dung"])
    s2, s1 = sent("s1_202", k), sent("s1_101", k)
    if not s2: res["s1_202"][k] = 0
    elif s2 == s1: res["s1_202"][k] = res["s1_101"][k]; dung_chung += 1
    else:
        res["s1_202"][k] = int(ph["diff"][k]["dung"])
print(f"bước {len(K)} · S1/202 khác S1/101: {sum(1 for k in K if sent('s1_202',k) and sent('s1_202',k)!=sent('s1_101',k))} · dùng chung kết quả S1/101: {dung_chung}")
for n in res: print(f"  {n:7s} Phi-4 chọn đúng = {100*sum(res[n].values())/len(K):.2f}")
APP = {k: (sc["s1_101"][k].get("app") or f"ep{k[0]}") for k in K}
def so(a, b):
    d = {k: res[a][k] - res[b][k] for k in K}
    pt, (lo, hi), G, _ = S.cluster_bootstrap(list(d.items()), lambda u: APP[u[0]], lambda u: u[1])
    x = sum(v > 0 for v in d.values()); y = sum(v < 0 for v in d.values()); n = x + y
    p = min(1, 2 * sum(math.comb(n, i) for i in range(min(x, y) + 1)) / 2 ** n) if n else 1
    print(f"  {a:7s}-{b:7s} Δ={100*pt:+.2f} [{100*lo:+.2f}; {100*hi:+.2f}] b={x} c={y} p={p:.3g}")
for a, b in (("ck500", "s1_202"), ("r3", "s1_202"), ("ck500", "s1_101"), ("s1_202", "s1_101"), ("r3", "ck500")): so(a, b)
