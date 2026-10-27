# -*- coding: utf-8 -*-
"""Đọc kết quả ACU (phần AndroidControl S1 chưa thấy, report/322 #8) — 0 GPU.

    ~/.venvs/thesis/bin/python harness/doc_acu.py      # in bảng + ghi runs/acu/ket_qua_acu.json

Thước: exec (Voronoi gated 14%) và vế khoảng cách của AitW (Euclid chuẩn hoá ≤ 0,14 ∧ đúng loại thao tác).
ACU không có hộp phần tử vàng nên KHÔNG tính D.3 / AitW đầy đủ.
Bootstrap cụm = app, bước không có app gom theo tác vụ (ACU không có app ⇒ cụm = tác vụ), B = 10.000,
hàm `score_run.cluster_bootstrap`; p là McNemar chính xác.
Gộp: ACU 1.484 + tập kiểm chính 4.463 = 5.947 bước (khai là gộp hai tập).
"""
import json, math, os

from scipy.stats import binomtest

import score_run as S

H = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(H, "..", "runs")
ACU = {t: f"acu/gen/out/score_{f}_acu_raw.jsonl" for t, f in
       (("câu chuẩn", "gold"), ("Base", "base"), ("S1/101", "s1"), ("ck500", "ck500"),
        ("ck500/202", "ck500_s202"), ("ACE", "r3"), ("ra_k4", "ra_k4"))}
CHINH = {"câu chuẩn": "score_ceiling_human_raw.jsonl", "Base": "score_base_raw.jsonl",
         "S1/101": "score_s1_seed101_raw.jsonl", "ck500": "grpo_spice/score_ck500_test_raw.jsonl",
         "ck500/202": "grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl",
         "ACE": "ra304_luat/score_R3_test_raw.jsonl"}
SO = [("ck500", "S1/101"), ("ck500/202", "S1/101"), ("ck500/202", "ck500"), ("ACE", "S1/101"),
      ("ACE", "ck500"), ("ra_k4", "S1/101"), ("S1/101", "Base"), ("ck500", "Base"), ("câu chuẩn", "S1/101")]


def nap(f, tien_to):
    out = {}
    for l in open(os.path.join(R, f), encoding="utf-8"):
        r = json.loads(l)
        ex = int(r.get("executable", 0))
        aw = 0
        if r.get("pred_xy") and r.get("action_ok") and r.get("toggle_ok", 1):
            (x, y), (gx, gy), (w, h) = r["pred_xy"], r["gold_xy"], r["wh"]
            aw = int(math.hypot((x - gx) / w, (y - gy) / h) <= .14)
        out[(tien_to, str(r["episode_id"]), str(r["step_id"]))] = dict(
            exec=ex, aitw=aw, cum=f"{tien_to}:" + (r.get("app") or f"ep{r['episode_id']}"))
    return out


def main():
    A = {t: nap(f, "acu") for t, f in ACU.items()}
    C = {t: nap(f, "ac") for t, f in CHINH.items()}
    KA = list(A["S1/101"])
    assert all(len(A[t]) == 1484 and set(A[t]) == set(KA) for t in A)
    KC = list(C["S1/101"])
    assert all(len(C[t]) == 4463 and set(C[t]) == set(KC) for t in C)
    G = {t: {**C[t], **A[t]} for t in C}
    KG = KC + KA

    def bs(K, X, f):
        pt, (lo, hi), n, _ = S.cluster_bootstrap([(k, f(k)) for k in K], lambda u: X[u[0]]["cum"],
                                                 lambda u: u[1], B=10000, seed=S.SEED)
        return [round(100 * pt, 2), round(100 * lo, 2), round(100 * hi, 2)], n

    out = {}
    for ten, X, K in (("ACU", A, KA), ("gộp 5.947", G, KG)):
        o = {"diem": {}, "so": {}}
        for t in X:
            o["diem"][t] = {c: bs(K, X[t], lambda k: X[t][k][c])[0] for c in ("exec", "aitw")}
        o["cum"] = bs(K, X["S1/101"], lambda k: 0)[1]
        for a, b in SO:
            if a not in X or b not in X:
                continue
            for c in ("exec", "aitw"):
                d, _ = bs(K, X[a], lambda k: X[a][k][c] - X[b][k][c])
                cu = sum(X[a][k][c] > X[b][k][c] for k in K); ph = sum(X[a][k][c] < X[b][k][c] for k in K)
                o["so"][f"{a} − {b} · {c}"] = dict(delta=d[0], lo=d[1], hi=d[2], cuu=cu, pha=ph,
                                                   p=binomtest(cu, cu + ph).pvalue if cu + ph else 1.0)
        out[ten] = o
        print(f"\n== {ten} · {len(K)} bước · {o['cum']} cụm")
        for t, v in o["diem"].items():
            print(f"  {t:10s} exec {v['exec'][0]:6.2f} [{v['exec'][1]:6.2f}; {v['exec'][2]:6.2f}]  AitW-kc {v['aitw'][0]:6.2f}")
        for k, g in o["so"].items():
            print(f"  {k:28s} {g['delta']:+6.2f} [{g['lo']:+6.2f}; {g['hi']:+6.2f}]  cứu {g['cuu']:4d} phá {g['pha']:4d}  p {g['p']:.2g}")
    # ACE: số bước luật R3 lấy câu ra_k4
    P = {t: {(str(d["episode_id"]), str(d["step_id"])): d.get("pred", d.get("sent"))
             for d in map(json.loads, open(os.path.join(R, f"acu/gen/out/pred_{f}_acu.jsonl"), encoding="utf-8"))}
         for t, f in (("ck500", "ck500"), ("ACE", "r3"), ("ra_k4", "ra_k4"), ("S1/101", "s1"))}
    ks = [k[1:] for k in KA]
    out["ACU"]["ace"] = dict(khac_ck500=sum(P["ACE"][k] != P["ck500"][k] for k in ks),
                             ck500_khac_s1=sum(P["ck500"][k] != P["S1/101"][k] for k in ks))
    print("\nACE khác ck500:", out["ACU"]["ace"])
    json.dump(out, open(os.path.join(R, "acu", "ket_qua_acu.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→ runs/acu/ket_qua_acu.json")


if __name__ == "__main__":
    main()
