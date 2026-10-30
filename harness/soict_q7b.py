# -*- coding: utf-8 -*-
"""SOICT camera-ready (GUIStep, 5590): mốc ngoài Qwen2.5-VL-7B prompting + hạt S thứ hai, dưới D.3.

    ~/.venvs/thesis/bin/python harness/soict_q7b.py   # ghi runs/soict_q7b.json

7B dùng đúng câu nhắc của Base (ảnh, mục tiêu, lịch sử, OCR), tệp thô `runs/qwen7b/test_25_10/`.
Cùng quy ước cụm, bootstrap, p hai phía như `soict_camera_ready.py`.
"""
import os, json, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import luat_d3 as L
import score_run as S
B = 10000
TEP = {"Base": "score_base_raw.jsonl", "S": "score_s1_seed101_raw.jsonl",
       "S202": "score_s1_seed202_raw.jsonl", "P": "score_min_desc_seed101_raw.jsonl",
       "D": "score_s2_seed101_raw.jsonl", "q7b": "qwen7b/test_25_10/score_qwen7b_test_raw.jsonl"}
R = {a: L.nap(os.path.join(L.RUNS, t)) for a, t in TEP.items()}
K = list(R["Base"]); assert len(K) == 4463 and all(set(R[a]) == set(K) for a in R), {a: len(R[a]) for a in R}
X = {a: {k: L.luat(R[a][k], k)["d3"] for k in K} for a in R}
cum = {k: R["Base"][k].get("app") or f"ep{R['Base'][k]['episode_id']}" for k in K}

def ktc(f):
    pt, (lo, hi), G, _ = S.cluster_bootstrap([(k, f(k)) for k in K], lambda u: cum[u[0]], lambda u: u[1], B=B, seed=S.SEED)
    return round(100 * pt, 2), round(100 * lo, 2), round(100 * hi, 2)

def boot_p(f):
    cl = {}
    for k in K: cl.setdefault(cum[k], []).append(f(k))
    num = np.array([sum(v) for v in cl.values()], float); den = np.array([len(v) for v in cl.values()], float)
    idx = np.random.default_rng(S.SEED).integers(0, len(num), size=(B, len(num)))
    d = num[idx].sum(1) / den[idx].sum(1)
    return round(min(1.0, 2 * (min((d <= 0).sum(), (d >= 0).sum()) + 1) / (B + 1)), 4)

out = {"diem": {a: ktc(lambda k, a=a: X[a][k]) for a in R}, "so_sanh": {}}
for a, b in [("q7b", "Base"), ("S", "q7b"), ("P", "q7b"), ("D", "q7b"), ("S202", "S"), ("P", "S202")]:
    f = lambda k: X[a][k] - X[b][k]
    out["so_sanh"][f"{a}-{b}"] = (*ktc(f), boot_p(f))
L7 = [len(R["q7b"][k].get("sent") or "") for k in K]; LS = [len(R["S"][k].get("sent") or "") for k in K]
out["do_dai_trung_vi"] = {"q7b": float(np.median(L7)), "S": float(np.median(LS))}
out["action_ok_q7b"] = round(100 * np.mean([R["q7b"][k]["action_ok"] for k in K]), 2)
print(json.dumps(out, ensure_ascii=False, indent=1))
json.dump(out, open(os.path.join(L.RUNS, "soict_q7b.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
