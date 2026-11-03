# -*- coding: utf-8 -*-
"""Đọc các lượt lưới RL đã chấm test: exec · D.3 · D.3∧14% · AitW đầy đủ, so ghép cặp với ck500 và S1/101 — 0 GPU.

    ~/.venvs/thesis/bin/python harness/doc_luoi.py    # chạy trong harness/, ghi runs/luoi/test_2_11/so_ghep_cap_exec.json

Cùng hàm với so_d3_aitw_ck500.py (bootstrap cụm app, B = 10.000, McNemar chính xác). Lượt chưa chấm đủ 4.463 bước
được so trên phần chung và ghi rõ n. Holm chỉ áp lên các phép so exec với ck500 của những lượt đang có, nên là số tạm
cho tới khi đủ họ chính ở report/320 §13. Tự kiểm: ck500 − S1/101 exec phải ra +1,55 [+0,80; +2,33].
"""
import json, os

from scipy.stats import binomtest

import luat_d3 as L
from luat_aitw_day_du import aitw_full
import score_run as S

B, SEED = 10000, S.SEED
THU = "luoi/test_2_11"
MOC = {"S1/101": "score_s1_seed101_raw.jsonl", "ck500": "grpo_spice/score_ck500_test_raw.jsonl"}
LUOT = {"SCST + SPICE": "score_scst_spice_101_test_raw.jsonl", "GRPO + CIDEr-D": "score_grpo_cider_101_test_raw.jsonl",
        "GRPO + METEOR": "score_grpo_meteor_101_test_raw.jsonl", "GRPO + ROUGE-L": "score_grpo_rougel_101_test_raw.jsonl"}
COT = {"exec": "vor", "D.3": "d3", "D.3∧14%": "d3_gate", "AitW đầy đủ": "aitwf"}


def nap(f):
    return {k: dict(L.luat(r, k), aitwf=aitw_full(r, k), cum=r.get("app") or f"ep{r['episode_id']}",
                    aok=r.get("action_ok", 0), sent=(r.get("sent") or "").strip())
            for k, r in L.nap(os.path.join(L.RUNS, f)).items()}


def so(A, Bn, c, K):
    cum = {k: Bn[k]["cum"] for k in K}
    pt, (lo, hi), _, _ = S.cluster_bootstrap([(k, A[k][c] - Bn[k][c]) for k in K], lambda u: cum[u[0]],
                                             lambda u: u[1], B=B, seed=SEED)
    cu = sum(A[k][c] > Bn[k][c] for k in K); ph = sum(A[k][c] < Bn[k][c] for k in K)
    return dict(delta=round(100 * pt, 2), lo=round(100 * lo, 2), hi=round(100 * hi, 2), hon=cu, kem=ph, n=len(K),
                p=binomtest(cu, cu + ph).pvalue if cu + ph else 1.0)


def main():
    M = {t: nap(f) for t, f in MOC.items()}
    X = {t: nap(f"{THU}/{f}") for t, f in LUOT.items()}
    T = list(M["S1/101"])
    g = so(M["ck500"], M["S1/101"], "vor", T)
    if max(abs(g["delta"] - 1.55), abs(g["lo"] - 0.80), abs(g["hi"] - 2.33)) > 0.011:
        raise SystemExit(f"⛔ DỪNG, không tái lập ck500 − S1/101: {g}")
    print("✅ tái lập ck500 − S1/101 exec", g, flush=True)
    out = {"B": B, "seed": SEED, "diem": {}, "so": {}, "holm_tam_exec_voi_ck500": {}}
    for t, R in {**M, **X}.items():
        out["diem"][t] = {ten: round(100 * sum(r[c] for r in R.values()) / len(R), 2) for ten, c in COT.items()}
        out["diem"][t].update(n=len(R), action_ok=round(100 * sum(r["aok"] for r in R.values()) / len(R), 2))
    for t, R in X.items():
        K = [k for k in T if k in R]
        for m, Q in M.items():
            for ten, c in COT.items():
                out["so"][f"{t} − {m} · {ten}"] = so(R, Q, c, K)
            out["so"][f"{t} − {m} · câu trùng"] = sum(R[k]["sent"] == Q[k]["sent"] for k in K)
        print(t, {m: out["so"][f"{t} − {m} · exec"] for m in M}, flush=True)
    ps = sorted((out["so"][f"{t} − ck500 · exec"]["p"], t) for t in X)
    tich = 0.0
    for i, (p, t) in enumerate(ps):
        tich = max(tich, min(1.0, p * (len(ps) - i)))
        out["holm_tam_exec_voi_ck500"][t] = dict(p=p, p_holm=tich)
    d = os.path.join(L.RUNS, THU, "so_ghep_cap_exec.json")
    json.dump(out, open(d, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", d, json.dumps(out["diem"], ensure_ascii=False), out["holm_tam_exec_voi_ck500"], flush=True)


if __name__ == "__main__":
    main()
