# -*- coding: utf-8 -*-
"""Phân tích lượt train lại ck500 (A/A, 8/11/2026) — 0 GPU, Kaggle CPU. Dùng lại hàm của giai_thich_7_11.py.

  python giai_thich_8_11.py --out ../runs/luoi/8_11/giai_thich/giai_thich_8_11.json

Thêm vào NHANH: "GRPO + SPICE (A/A)" (luoi-t2-11 ck500, mã grpo_luoi.py) và "ck500/202" (mã cũ, hạt 202).
  A–E như bản 7/11 (tự kiểm ck500 +28/+41 và ck500 − SFT tiếp +0,49 giữ nguyên).
  F. Họ so với A/A (mốc công bằng trong lưới: cùng mã train): exec, D.3, D.3∧14%, AitW đầy đủ cho mọi lượt lưới
     + SFT tiếp, Holm trên exec. Tự kiểm A/A − ck500 = −0,92 [−1,36; −0,49] (doc_luoi, 8/11).
  G. Ba điểm lưu GRPO + SPICE (ck500/101, ck500/202, A/A): phân rã ghép cặp từng đôi + KTC hai phần, độ trùng câu.
Số mô tả, hậu kiểm.
"""
import argparse, json, os, sys

import giai_thich_7_11 as G

AA, S202 = "GRPO + SPICE (A/A)", "ck500/202"
G.NHANH[AA] = "luoi/8_11/test_u_4/score_grpo_spice_aa_101_test_raw.jsonl"
G.NHANH[S202] = "grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl"
# 5 cặp đầu đi vào phần C (theo nhóm); hai cặp đầu giữ để tự kiểm B của bản 7/11.
G.CAP = [("ck500", "SFT tiếp"), (AA, "ck500"), (AA, "SFT tiếp"), (AA, S202), ("ck500", S202),
         (AA, "S1/101"), (S202, "S1/101"), (S202, "SFT tiếp"),
         ("SCST + SPICE", AA), ("GRPO + ROUGE-L", AA), ("GRPO + METEOR", AA), ("GRPO + CIDEr-D", AA),
         ("REINFORCE + SPICE", AA), ("RLOO + SPICE", AA)]
BA = ("ck500", S202, AA)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    tam = a.out[:-5] + "_A_E.json"
    sys.argv = [sys.argv[0], "--out", tam]
    G.main()  # A–E, tự kiểm của bản 7/11 nằm trong đây
    out = json.load(open(tam, encoding="utf-8"))
    R = {t: G.nap(f) for t, f in G.NHANH.items()}
    K = sorted(R["S1/101"])
    cum = {k: R["S1/101"][k]["cum"] for k in K}

    # F
    out["F_ho_so_AA"] = {t: {ten: G.so(R[t], R[AA], c, K, cum) for ten, c in G.COT.items()}
                         for t in R if t not in (AA, "S1/101", "xao101", "ck500", S202)}
    ps = sorted((v["exec"]["p"], t) for t, v in out["F_ho_so_AA"].items())
    out["F_holm_exec"], tich = {}, 0.0
    for i, (p, t) in enumerate(ps):
        tich = max(tich, min(1.0, p * (len(ps) - i)))
        out["F_holm_exec"][t] = dict(delta=out["F_ho_so_AA"][t]["exec"]["delta"], p=p, p_holm=tich)
    G.log("F holm so A/A", json.dumps(out["F_holm_exec"], ensure_ascii=False))
    g = G.so(R[AA], R["ck500"], "vor", K, cum)
    if max(abs(g["delta"] + 0.92), abs(g["lo"] + 1.36), abs(g["hi"] + 0.49)) > 0.011:
        sys.exit(f"⛔ DỪNG, không tái lập A/A − ck500 −0,92 [−1,36; −0,49]: {g}")
    G.log("✅ tự kiểm F: A/A − ck500", g)

    # G
    out["G_ba_diem_luu"] = {}
    for i in range(3):
        for j in range(i + 1, 3):
            x, y = BA[i], BA[j]
            X, Y = R[x], R[y]
            loai = lambda k: int(X[k]["e"] and not Y[k]["e"] and not Y[k]["a"]) - int(Y[k]["e"] and not X[k]["e"] and not X[k]["a"])
            d = G.phan_ra(X, Y, K)
            d.update({ten: G.so(X, Y, c, K, cum) for ten, c in G.COT.items()})
            d["ktc_loai"] = G.ktc(K, loai, cum)
            d["ktc_phan_tu"] = G.ktc(K, lambda k: (X[k]["e"] - Y[k]["e"]) - loai(k), cum)
            d["cau_trung"] = sum(X[k]["sent"] == Y[k]["sent"] for k in K)
            out["G_ba_diem_luu"][f"{x} − {y}"] = d
            G.log("G", x, "−", y, json.dumps(d, ensure_ascii=False))
    out["G_diem"] = {t: out["E_diem"][t] for t in BA}
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    G.log("[xong] ghi", a.out)


if __name__ == "__main__":
    main()
