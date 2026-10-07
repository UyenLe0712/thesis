# -*- coding: utf-8 -*-
"""Phân rã Δ(chặng ba − S1) theo cổng loại thao tác, dưới ba luật (exec · D.3 · AitW đầy đủ) — 0 GPU.

    python3 harness/phan_ra_cong_thao_tac.py     # in bảng + ghi runs/phan_ra_cong_thao_tac.json

Chia 4.463 bước chạm theo việc S1 có qua cổng (action_ok ∧ toggle_ok) hay không:
  · nhóm S1 sai cổng        — phần Δ do sửa loại thao tác
  · nhóm cả hai qua cổng    — phần Δ do định vị (hình học)
  · phần còn lại            — chặng ba sai cổng mà S1 qua
Đo 21/9/2026: dưới AitW, Δ +2,94 = +3,11 (256 bước S1 sai cổng) + 0,11 (4.189 bước cả hai qua) − 0,29.
"""
import os, json
import luat_d3 as L, luat_aitw_day_du as A

LUAT = {"exec": lambda r, k: int(r["executable"]),
        "d3": lambda r, k: L.luat(r, k)["d3"],
        "aitw": lambda r, k: A.aitw_full(r, k)}
gate = lambda r: int(r["action_ok"] and r["toggle_ok"])

def main():
    R = {t: L.nap(os.path.join(L.RUNS, f)) for t, f in L.NHANH}
    P, out = R["GRPO-point/101"], {}
    for base in ("S1/101", "S1/202"):
        B = R[base]; K = sorted(set(P) & set(B)); n = len(K)
        s1sai = [k for k in K if not gate(B[k])]
        caihai = [k for k in K if gate(P[k]) and gate(B[k])]
        o = {"n": n, "n_s1_sai_cong": len(s1sai), "n_ca_hai_qua": len(caihai)}
        for ten, f in LUAT.items():
            d = lambda S: 100 * sum(f(P[k], k) - f(B[k], k) for k in S) / n
            o[ten] = dict(tong=round(d(K), 2), tu_s1_sai_cong=round(d(s1sai), 2),
                          tu_ca_hai_qua=round(d(caihai), 2),
                          trung_ca_hai_qua_grpo=round(100 * sum(f(P[k], k) for k in caihai) / len(caihai), 2),
                          trung_ca_hai_qua_s1=round(100 * sum(f(B[k], k) for k in caihai) / len(caihai), 2))
            print(f"{base} {ten:5s} Δ {o[ten]['tong']:+.2f} = S1 sai cổng {o[ten]['tu_s1_sai_cong']:+.2f}"
                  f" · cả hai qua {o[ten]['tu_ca_hai_qua']:+.2f}"
                  f"  (trúng khi cả hai qua: {o[ten]['trung_ca_hai_qua_grpo']} vs {o[ten]['trung_ca_hai_qua_s1']})")
        out["GRPO-point/101 − " + base] = o
    json.dump(out, open(os.path.join(L.RUNS, "phan_ra_cong_thao_tac.json"), "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
