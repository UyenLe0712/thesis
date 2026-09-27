# -*- coding: utf-8 -*-
"""Cổng C3 (report/208 §6) — 0 giây GPU: mức nhiễu và tương quan lỗi của hai người nghe dự kiến dùng
trong THƯỞNG (UI-Venus-7B, Phi-4 SoM), đối chiếu với bộ trỏ CHẤM (UGround), trên dữ liệu tập kiểm sẵn có.

Luật đạt ghi TRƯỚC khi chạy (27/9):
  (i)  mỗi người nghe có tỉ lệ trượt trên câu chuẩn > 15%  (dưới mức đó, theo arXiv 2604.07666,
       hiệu chỉnh nhiễu gần như không đổi kết quả ⇒ cổng mềm vô ích)
  (ii) κ(UI-Venus, Phi-4) trên câu S1 ≤ 0,60                (lỗi không trùng nhau tới mức hai người nghe
       chỉ bằng một)
  (iii) P(UGround trúng | cả hai người nghe trúng) − max(P(UGround trúng | từng người nghe trúng)) ≥ +3 pp
       (gộp hai người nghe phải dự báo bộ trỏ chấm độc lập tốt hơn từng người)
⚠️ Đây là đại diện trên TẬP KIỂM (UGround đóng vai "sự thật" nhiễu); hiệu chỉnh thật làm trên tập dạy
bằng hộp vàng. Không số nào ở đây vào bài như kết quả.
Chạy:  python3 harness/c3_nhieu_nguoi_nghe.py   (ghi runs/c3_nhieu_nguoi_nghe.json)
"""
import json
from pathlib import Path

R = Path(__file__).resolve().parent.parent


def rd(p):
    return [json.loads(l) for l in open(R / p, encoding="utf-8")]


def key(r):
    return (int(r["episode_id"]), int(r["step_id"]))


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def pct(xs):
    return round(100 * sum(xs) / len(xs), 2) if xs else float("nan")


def main():
    out = {}
    # (i) trượt trên câu chuẩn
    ug_h = [r.get("hit_voronoi", 0) for r in rd("runs/score_ceiling_human_raw.jsonl") if "sent" in r]
    ph_h = [r["dung"] for r in rd("runs/som/chon_phi4_chuan.jsonl")]
    ve_h = [int(r["err_frac"] <= 0.14) for r in rd("runs/venus/venus_gate_raw.jsonl")]
    out["truot_cau_chuan"] = {"UGround_voronoi_n4463": round(100 - pct(ug_h), 2),
                               "Phi4_n4463": round(100 - pct(ph_h), 2),
                               "UIVenus_err14_n300": round(100 - pct(ve_h), 2)}
    out["trung_cau_rong_Phi4"] = pct([r["dung"] for r in rd("runs/som/chon_phi4_san.jsonl")])

    # (ii)(iii) trên câu S1/101, giao ba nguồn
    U = {key(r): r for r in rd("runs/score_s1_seed101_raw.jsonl") if "sent" in r}
    V = {key(r): r for r in rd("runs/venus/score_venus_s1_2532_raw.jsonl") if "sent" in r}
    P = {key(r): r for r in rd("runs/som/chon_phi4_s1_101.jsonl")}
    ks = sorted(set(U) & set(V) & set(P))
    v = [V[k]["hit_voronoi"] for k in ks]
    p = [P[k]["dung"] for k in ks]
    u = [U[k]["hit_voronoi"] for k in ks]
    ue = [U[k]["executable"] for k in ks]
    out["n_giao"] = len(ks)
    out["ti_le_trung"] = {"UIVenus": pct(v), "Phi4": pct(p), "UGround": pct(u)}
    out["kappa"] = {"Venus_Phi4": round(kappa(v, p), 3), "Venus_UGround": round(kappa(v, u), 3),
                    "Phi4_UGround": round(kappa(p, u), 3)}
    o = {}
    for vv in (1, 0):
        for pp in (1, 0):
            idx = [i for i in range(len(ks)) if v[i] == vv and p[i] == pp]
            o[f"V{vv}P{pp}"] = {"n": len(idx), "UGround_voronoi": pct([u[i] for i in idx]),
                                "UGround_exec": pct([ue[i] for i in idx])}
    out["UGround_theo_o"] = o
    cond = {"|V=1": pct([u[i] for i in range(len(ks)) if v[i]]),
            "|P=1": pct([u[i] for i in range(len(ks)) if p[i]]),
            "|V=1∧P=1": o["V1P1"]["UGround_voronoi"]}
    out["UGround_co_dieu_kien"] = cond
    miss_v = [i for i in range(len(ks)) if not v[i]]
    out["P(Phi4 truot)"] = round(100 - pct(p), 2)
    out["P(Phi4 truot | Venus truot)"] = round(100 - pct([p[i] for i in miss_v]), 2)

    lift = cond["|V=1∧P=1"] - max(cond["|V=1"], cond["|P=1"])
    tr = out["truot_cau_chuan"]
    dat = {"(i) moi nguoi nghe truot cau chuan >15%": min(tr["Phi4_n4463"], tr["UIVenus_err14_n300"]) > 15,
           "(ii) kappa Venus-Phi4 <= 0.60": out["kappa"]["Venus_Phi4"] <= 0.60,
           "(iii) lift gop hai nguoi nghe >= +3pp": lift >= 3.0}
    out["lift_pp"] = round(lift, 2)
    out["luat"] = dat
    out["C3"] = "DAT" if all(dat.values()) else "KHONG DAT"
    json.dump(out, open(R / "runs/c3_nhieu_nguoi_nghe.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
