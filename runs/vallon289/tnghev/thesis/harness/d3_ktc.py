# -*- coding: utf-8 -*-
"""KTC95 + phép so ghép cặp cho luật D.3, đặt cạnh executability — 0 giây GPU, ~3 phút CPU.

    python3 harness/d3_ktc.py        # in bảng + ghi runs/d3_ktc.json

Vì sao cần: từ 13/9 luận văn báo D.3 SONG SONG với executability, nhưng trước đó chỉ exec có
khoảng tin cậy và McNemar. File này dùng lại đúng hàm luật của `luat_d3.py` và đúng hàm bootstrap
của `score_run.py` (cụm = app; tác vụ không gán được app tự thành một cụm, G = 1.091), nên hai
thước được đo cùng một cách.

Tự kiểm trước khi ghi: KTC exec của năm nhánh phải khớp TUYỆT ĐỐI `ci_voronoi` trong score_*.json
(cùng hàm `score_run.cluster_bootstrap`, cùng hạt giống, cùng thứ tự dòng), và McNemar exec của
S1−Base (χ² 243,2) cùng GRPO−MIN (b=98, c=99) phải khớp. Đạt 14/9/2026.
"""
import json, math, os

import luat_d3 as L
from luat_aitw_day_du import aitw_full
import score_run as S          # dùng ĐÚNG hàm bootstrap đã sinh mọi KTC exec trong luận văn

B, SEED = 10000, S.SEED
NHANH = dict(L.NHANH)
SO = [("S1/101", "Base"), ("S1/202", "Base"), ("MIN-DESC/101", "S1/101"),
      ("GRPO-point/101", "S1/101"), ("GRPO-point/101", "S1/202"), ("GRPO-point/101", "MIN-DESC/101"),
      ("Câu người (trần)", "GRPO-point/101"),
      ("S2/101", "S1/101"), ("CE2-S2/101", "S2/101"), ("MIN-DESC/101", "S2/101"), ("MIN-DESC/101", "CE2-S2/101"),
      ("GRPO-point/101", "S2/101")]


def nap_nhanh(ten):
    R = L.nap(os.path.join(L.RUNS, NHANH[ten]))            # dict giữ thứ tự dòng của tệp thô
    return {k: dict(L.luat(r, k), aitwf=aitw_full(r, k), cum=r.get("app") or f"ep{r['episode_id']}")
            for k, r in R.items()}


def ktc(K, V, cot, cum_of):
    """KTC95 bằng `score_run.cluster_bootstrap` (cụm = app, tác vụ không app tự thành cụm).
    Thứ tự `K` quyết định thứ tự cụm nên phải là thứ tự dòng của tệp thô, để exec tái lập tuyệt đối."""
    U = [(k, V(k, cot)) for k in K]
    pt, (lo, hi), G, _ = S.cluster_bootstrap(U, lambda u: cum_of[u[0]], lambda u: u[1], B=B, seed=SEED)
    return 100 * pt, 100 * lo, 100 * hi, G


def mcnemar(K, A, Bn, cot):
    b = sum(1 for k in K if A[k][cot] == 1 and Bn[k][cot] == 0)
    c = sum(1 for k in K if A[k][cot] == 0 and Bn[k][cot] == 1)
    chi = (abs(b - c) - 1) ** 2 / (b + c) if b + c else 0.0
    return b, c, chi, (math.erfc(math.sqrt(chi / 2)) if b + c else 1.0)


def main():
    X = {t: nap_nhanh(t) for t in NHANH}
    assert all(len(X[t]) == 4463 and set(X[t]) == set(X["Base"]) for t in X), "quần thể phải là 4.463 bước chung"
    cum_of = {k: X["S1/101"][k]["cum"] for k in X["Base"]}
    out = {"ktc": {}, "so_sanh": {}, "B": B, "seed": SEED}

    print(f"{'nhánh':20s} {'exec':>7s} {'KTC95 exec':>17s} {'D.3':>7s} {'KTC95 D.3':>17s}")
    for t in NHANH:
        o = {}
        for cot in ("vor", "d3", "aitwf"):
            p, lo, hi, G = ktc(list(X[t]), lambda k, c: X[t][k][c], cot, cum_of)
            o[cot] = dict(diem=round(p, 2), lo=round(lo, 2), hi=round(hi, 2), G=G)
        out["ktc"][t] = o
        print(f"{t:20s} " + "  ".join(f"{c} {o[c]['diem']:6.2f} [{o[c]['lo']:6.2f}; {o[c]['hi']:6.2f}]"
                                       for c in ("vor", "d3", "aitwf")))
    print(f"G = {out['ktc']['Base']['vor']['G']} cụm\n")

    print(f"{'phép so':34s} {'luật':5s} {'Δ':>6s} {'KTC95 Δ':>17s} {'b':>5s} {'c':>5s} {'χ²':>7s} {'p':>9s}")
    for a, bb in SO:
        for cot in ("vor", "d3", "aitwf"):
            d, lo, hi, _ = ktc(list(X[a]), lambda k, c: X[a][k][c] - X[bb][k][c], cot, cum_of)
            b, c, chi, p = mcnemar(list(X[a]), X[bb], X[a], cot)
            out["so_sanh"][f"{a} − {bb} · {cot}"] = dict(delta=round(d, 2), lo=round(lo, 2),
                                                         hi=round(hi, 2), b=b, c=c,
                                                         chi2=round(chi, 2), p=p)
            print(f"{a+' − '+bb:34s} {cot:5s} {d:+6.2f} [{lo:+6.2f}; {hi:+6.2f}] {b:5d} {c:5d} "
                  f"{chi:7.2f} {p:9.2e}")

    # ── tự kiểm với số đã in trong luận văn ─────────────────────────────────────
    s = out["so_sanh"]
    loi = []
    JS = {"Base": "score_base.json", "S1/101": "score_s1_seed101.json",
          "MIN-DESC/101": "score_min_desc_seed101.json", "Câu người (trần)": "score_ceiling_human.json",
          "GRPO-point/101": "grpo_point/score_grpo_point_seed101.json"}
    for t, f in JS.items():
        ci = json.load(open(os.path.join(L.RUNS, f)))["ci_voronoi"]
        g = out["ktc"][t]["vor"]
        if abs(g["lo"] - 100 * ci[0]) > 0.006 or abs(g["hi"] - 100 * ci[1]) > 0.006:
            loi.append(f"KTC exec {t} {g} ≠ {f} {ci}")
    if abs(s["S1/101 − Base · vor"]["chi2"] - 243.2) > 0.1:
        loi.append(f"χ² S1−Base {s['S1/101 − Base · vor']['chi2']} ≠ 243,2")
    g = s["GRPO-point/101 − MIN-DESC/101 · vor"]
    if (g["b"], g["c"]) != (98, 99):
        loi.append(f"GRPO−MIN b,c = {g['b']},{g['c']} ≠ 98,99")
    if loi:
        raise SystemExit("⛔ DỪNG, không ghi: " + " · ".join(loi))
    print("\n✅ tự kiểm: KTC exec và McNemar exec khớp số đã in trong luận văn")
    p = os.path.join(L.RUNS, "d3_ktc.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", os.path.relpath(p))


if __name__ == "__main__":
    main()
