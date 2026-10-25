# SOICT camera-ready 25/10: Voronoi ranking, gui_sel (D.3) va nguoi nghe Phi-4 cho phan bien. Chay: ~/.venvs/thesis/bin/python harness/soict_them.py
import os, sys, json
import numpy as np
H = "/mnt/d/Master/Thesis/harness"; sys.path.insert(0, H)
import luat_d3 as L, score_run as S
B = 10000
nh = dict(L.NHANH)
TEN = {"Base": "Base", "S": "S1/101", "D": "S2/101", "P": "MIN-DESC/101", "CE2": "CE2-S2/101",
       "sel": "gui_sel/101", "ref": "Câu người (trần)"}
X = {}
for a, t in TEN.items():
    R = L.nap(os.path.join(L.RUNS, nh[t]))
    X[a] = {k: L.luat(r, k) for k, r in R.items()}
    if a == "Base": ref = R
K = list(ref)
cum = {k: ref[k].get("app") or f"ep{ref[k]['episode_id']}" for k in K}
def ktc(f):
    U = [(k, f(k)) for k in K]
    pt, (lo, hi), G, _ = S.cluster_bootstrap(U, lambda u: cum[u[0]], lambda u: u[1], B=B, seed=S.SEED)
    return round(100*pt,2), round(100*lo,2), round(100*hi,2)
def p(f):
    cl = {}
    for k in K: cl.setdefault(cum[k], []).append(f(k))
    num = np.array([sum(v) for v in cl.values()], float); den = np.array([len(v) for v in cl.values()], float)
    G = len(num); rng = np.random.default_rng(S.SEED); idx = rng.integers(0, G, size=(B, G))
    d = num[idx].sum(1)/den[idx].sum(1)
    return min(1.0, 2*(min((d<=0).sum(), (d>=0).sum())+1)/(B+1))
for col in ("vor", "d3"):
    print("==", col)
    for a in TEN: print(a, ktc(lambda k: X[a][k][col]))
    for a, b in [("S","Base"),("D","S"),("P","S"),("P","CE2"),("sel","S"),("sel","Base"),("sel","P")]:
        f = lambda k: X[a][k][col]-X[b][k][col]
        print(f"{a}-{b}", ktc(f), "p=%.4g" % p(f))
# Phi-4
def nap4(path):
    return {(str(r["episode_id"]), str(r["step_id"])): r["dung"] for r in map(json.loads, open(path))}
P4 = {"Base": nap4("/mnt/d/Master/Thesis/runs/som/base_rest_24_10/chon_phi4_base_du_4463.jsonl"),
      "S": nap4("/mnt/d/Master/Thesis/runs/som/chon_phi4_s1_101.jsonl"),
      "ref": nap4("/mnt/d/Master/Thesis/runs/som/chon_phi4_chuan.jsonl")}
print("== phi4", {a: len(v) for a, v in P4.items()})
for a in P4: print(a, ktc(lambda k: P4[a].get(k, 0)))
for a, b in [("S","Base"),("ref","S")]:
    f = lambda k: P4[a].get(k,0)-P4[b].get(k,0); print(f"{a}-{b}", ktc(f), "p=%.4g" % p(f))
