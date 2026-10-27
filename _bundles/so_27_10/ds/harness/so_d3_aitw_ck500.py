# -*- coding: utf-8 -*-
"""Phép so ghép cặp dưới exec · D.3 · D.3∧14% · AitW đầy đủ cho các nhánh của phương pháp chính
(ck500, ACE, hạt 202, xao101, 7B) — 0 GPU, vài phút CPU.

    ~/.venvs/thesis/bin/python harness/so_d3_aitw_ck500.py     # in bảng + ghi runs/so_d3_aitw_ck500.json

Dùng lại đúng hàm luật của `luat_d3.py` / `luat_aitw_day_du.py` và hàm bootstrap của `score_run.py`
(cụm = app, B = 10.000), như `d3_ktc.py`. p là McNemar chính xác (nhị thức), như report/320.
Tự kiểm: exec của ck500 − S1/101 phải ra +1,55 [+0,80; +2,33] và ck500 − S1/202 +1,03 [+0,25; +1,83].
"""
import json, os

from scipy.stats import binomtest

import luat_d3 as L
from luat_aitw_day_du import aitw_full
import score_run as S

B, SEED = 10000, S.SEED
NHANH = {"Base": "score_base_raw.jsonl",
         "S1/101": "score_s1_seed101_raw.jsonl",
         "S1/202": "score_s1_seed202_raw.jsonl",
         "ck500": "grpo_spice/score_ck500_test_raw.jsonl",
         "ck500/202": "grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl",
         "ACE": "ra304_luat/score_R3_test_raw.jsonl",
         "xao101": "xao101/test/score_ck500_xao101_test_raw.jsonl",
         "7B": "qwen7b/test_25_10/score_qwen7b_test_raw.jsonl"}
SO = [("ck500", "S1/101"), ("ck500", "S1/202"), ("ck500/202", "S1/101"), ("ck500/202", "S1/202"),
      ("ck500/202", "ck500"), ("S1/202", "S1/101"),
      ("ACE", "S1/101"), ("ACE", "S1/202"), ("ACE", "ck500"), ("ACE", "ck500/202"),
      ("xao101", "S1/101"), ("ck500", "xao101"), ("ck500/202", "xao101"), ("ACE", "xao101"),
      ("7B", "Base"), ("S1/101", "7B"), ("ck500", "7B"), ("ACE", "7B")]
COT = {"exec": "vor", "D.3": "d3", "D.3∧14%": "d3_gate", "AitW đầy đủ": "aitwf"}


def nap_nhanh(f):
    R = L.nap(os.path.join(L.RUNS, f))
    return {k: dict(L.luat(r, k), aitwf=aitw_full(r, k), cum=r.get("app") or f"ep{r['episode_id']}")
            for k, r in R.items()}


def main():
    X = {t: nap_nhanh(f) for t, f in NHANH.items()}
    K = list(X["S1/101"])
    assert all(len(X[t]) == 4463 and set(X[t]) == set(K) for t in X), "quần thể phải là 4.463 bước chung"
    cum = {k: X["S1/101"][k]["cum"] for k in K}

    def ktc(f):
        pt, (lo, hi), G, _ = S.cluster_bootstrap([(k, f(k)) for k in K], lambda u: cum[u[0]],
                                                 lambda u: u[1], B=B, seed=SEED)
        return round(100 * pt, 2), round(100 * lo, 2), round(100 * hi, 2)

    out = {"diem": {}, "so": {}, "B": B, "seed": SEED}
    for t in X:
        out["diem"][t] = {ten: round(100 * sum(X[t][k][c] for k in K) / len(K), 2) for ten, c in COT.items()}
    for a, b in SO:
        for ten, c in COT.items():
            d = ktc(lambda k: X[a][k][c] - X[b][k][c])
            cu = sum(X[a][k][c] > X[b][k][c] for k in K); ph = sum(X[a][k][c] < X[b][k][c] for k in K)
            p = binomtest(cu, cu + ph).pvalue if cu + ph else 1.0
            out["so"][f"{a} − {b} · {ten}"] = dict(delta=d[0], lo=d[1], hi=d[2], cuu=cu, pha=ph, p=p)

    loi = []
    for key, ref in (("ck500 − S1/101 · exec", (1.55, 0.80, 2.33)), ("ck500 − S1/202 · exec", (1.03, 0.25, 1.83))):
        g = out["so"][key]
        if max(abs(g["delta"] - ref[0]), abs(g["lo"] - ref[1]), abs(g["hi"] - ref[2])) > 0.011:
            loi.append(f"{key} {g} ≠ {ref}")
    if loi:
        raise SystemExit("⛔ DỪNG, không ghi: " + " · ".join(loi))

    for t, v in out["diem"].items():
        print(f"{t:10s} " + "  ".join(f"{n} {x:6.2f}" for n, x in v.items()))
    print()
    for k, g in out["so"].items():
        print(f"{k:34s} {g['delta']:+6.2f} [{g['lo']:+6.2f}; {g['hi']:+6.2f}]  cứu {g['cuu']:4d} phá {g['pha']:4d}  p {g['p']:.2g}")
    p = os.path.join(L.RUNS, "so_d3_aitw_ck500.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n✅ tự kiểm exec khớp →", os.path.relpath(p))


if __name__ == "__main__":
    main()
