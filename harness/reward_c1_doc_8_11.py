# -*- coding: utf-8 -*-
"""Đọc reward_groups.jsonl của kernel reward-spice-c1-cpu-8-11 (val C1, bước chạm): độ đồng thuận có/bỏ cặp hoà, mốc chrF một mình,
KTC95 bootstrap cụm episode (B = 2.000, hạt 20261109). Vài chục giây CPU. Chỉ val, chỉ để sàng lọc.

    python reward_c1_doc_8_11.py   # ghi runs/luoi/8_11/reward_c1/doc_c1.json
"""
import itertools, json
from pathlib import Path

import numpy as np
from sacrebleu.metrics import CHRF

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "runs/luoi/8_11/reward_c1"
G = [json.loads(l) for l in open(D / "reward_cpu_8_11/reward_groups.jsonl", encoding="utf8")]
C = [json.loads(l) for l in open(ROOT / "runs/c1/c1_mau.jsonl", encoding="utf8")]
assert [(a["episode_id"], a["step_id"]) for a in G] == [(a["episode_id"], a["step_id"]) for a in C]
ch = CHRF()
for g, c in zip(G, C):
    g["rs"]["chrF_only"] = [ch.sentence_score(s or "", [c["gold"]]).score / 100 for s in c["mau"]]
T = [g for g in G if g["action"] == "click"]
assert len(T) == 249


def dem(g, n):
    r, e = g["rs"][n], g["outcomes"]
    w = l = t = 0
    for i, j in itertools.combinations(range(8), 2):
        if e[i] == e[j]:
            continue
        if abs(r[i] - r[j]) < 1e-9:
            t += 1
        elif (r[i] - r[j]) * (e[i] - e[j]) > 0:
            w += 1
        else:
            l += 1
    return w, l, t


A = {n: np.array([dem(g, n) for g in T]) for n in T[0]["rs"]}


def f(n, I, hoa):
    w, l, t = A[n][I].sum(0)
    return (w + .5 * t) / (w + l + t) if hoa else w / (w + l)


out = {"pham_vi": "val C1, 249 bước chạm, 8 mẫu S1/101; chỉ sàng lọc", "muc": {}, "so": {}}
all_I = np.arange(len(T))
for n in A:
    w, l, t = (int(x) for x in A[n].sum(0))
    out["muc"][n] = dict(dung=w, sai=l, hoa=t, dong_thuan=round(f(n, all_I, True), 4), bo_hoa=round(f(n, all_I, False), 4))
eps = sorted({g["episode_id"] for g in T})
idx = {e: [i for i, g in enumerate(T) if g["episode_id"] == e] for e in eps}
rng = np.random.default_rng(20261109)
for x, y in [("R4_sparse_action", "R0_historical"), ("R2_sparse", "R0_historical"), ("R_fixed_spice_chrf", "R0_historical"),
             ("chrF_only", "R0_historical"), ("R4_sparse_action", "R2_sparse"), ("R4_sparse_action", "chrF_only"),
             ("R3_action", "R0_historical")]:
    for hoa in (True, False):
        b = [f(x, I, hoa) - f(y, I, hoa) for I in
             (np.concatenate([idx[eps[j]] for j in rng.integers(0, len(eps), len(eps))]) for _ in range(2000))]
        out["so"][f"{x} − {y} ({'có' if hoa else 'bỏ'} hoà)"] = dict(
            delta=round(f(x, all_I, hoa) - f(y, all_I, hoa), 4), lo=round(float(np.percentile(b, 2.5)), 4), hi=round(float(np.percentile(b, 97.5)), 4))
json.dump(out, open(D / "doc_c1.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=0)[:1800])
