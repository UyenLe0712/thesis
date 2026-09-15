# -*- coding: utf-8 -*-
"""Phân tích sâu kết quả người nghe trắc nghiệm Phi-4 (lượt commit đêm 14/9) — CPU, 0 GPU, ~1 phút.

    python3 harness/som_phan_tich.py         # in bảng + ghi runs/som/som_phan_tich.json

Bổ sung cho `som_doc.py` (KTC từng nhánh + McNemar) bốn thứ:
 (1) KTC95 GHÉP CẶP bootstrap cụm app cho hiệu hai nhánh (cùng `score_run.cluster_bootstrap`, giá trị = hiệu 0/±1);
 (2) trên đúng 3.566 bước mà nhánh Base đã chấm xong: xếp hạng bốn nhánh dưới người nghe cạnh exec · D.3 · AitW
     ⇒ kiểm thứ tự nhánh có giữ khi đổi sang người nghe ngoài họ Qwen hay không;
 (3) mức đoán ngẫu nhiên, trần phủ đáp án, độ chính xác theo cỡ khối ứng viên;
 (4) mức đồng thuận từng bước giữa người nghe và UGround (exec) trên câu chuẩn và chặng ba.
"""
import collections, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score_run as S
import luat_d3 as L
from luat_aitw_day_du import aitw_full

RUNS = os.path.join(HERE, "..", "runs")
SOM = os.path.join(RUNS, "som")
APP = {(str(o["episode_id"]), str(o["step_id"])): (o.get("app") or f"ep{o['episode_id']}")
       for o in map(json.loads, open(os.path.join(RUNS, "score_s1_seed101_raw.jsonl"), encoding="utf-8"))}
NHANH = [("Câu chuẩn", "chuan", "score_ceiling_human_raw.jsonl"),
         ("Chặng ba (GRPO)", "grpo", "grpo_point/score_grpo_point_seed101_raw.jsonl"),
         ("S1/101", "s1_101", "score_s1_seed101_raw.jsonl"),
         ("Base", "base", "score_base_raw.jsonl"),
         ("Câu rỗng nghĩa", "san", None)]


def nap_chon(ma):
    d = {}
    for l in open(os.path.join(SOM, f"chon_phi4_{ma}.jsonl"), encoding="utf-8"):
        o = json.loads(l); d[(str(o["episode_id"]), str(o["step_id"]))] = o
    return d


def ghep(A, B, K, f):
    U = [(k, f(A[k]) - f(B[k])) for k in K]
    pt, (lo, hi), G, _ = S.cluster_bootstrap(U, lambda u: APP[u[0]], lambda u: u[1])
    b = sum(1 for _, v in U if v < 0); c = sum(1 for _, v in U if v > 0)
    chi = (abs(b - c) - 1) ** 2 / (b + c) if b + c else 0.0
    return dict(n=len(K), delta=round(100 * pt, 2), lo=round(100 * lo, 2), hi=round(100 * hi, 2),
                b=b, c=c, p=math.erfc(math.sqrt(chi / 2)) if b + c else 1.0)


def main():
    som = {(str(r["episode_id"]), str(r["step_id"])): r
           for r in map(json.loads, open(os.path.join(HERE, "dg1_cache", "som", "som.jsonl"), encoding="utf-8"))}
    C = {ma: nap_chon(ma) for _, ma, _ in NHANH}
    for ma, D in C.items():
        assert set(D) <= set(som), ma
    R = {ma: L.nap(os.path.join(RUNS, tep)) for _, ma, tep in NHANH if tep}
    out = {}

    # (3) mốc tham chiếu của thang
    phu = 100 * sum(1 for r in som.values() if r["dap_an"]) / len(som)
    ngau = 100 * sum(len(r["dap_an"]) / len(r["boxes"]) for r in som.values() if r["boxes"]) / len(som)
    out["moc"] = dict(phu_dap_an=round(phu, 2), doan_ngau_nhien=round(ngau, 2), n=len(som))
    print(f"Trần phủ đáp án {phu:.2f} · đoán ngẫu nhiên {ngau:.2f} (kỳ vọng) · n={len(som)}")

    # (1) ghép cặp trên 4.463 bước
    print("\nGhép cặp, người nghe Phi-4 (KTC95 bootstrap cụm app):")
    out["ghep_cap"] = {}
    for a, b in [("chuan", "grpo"), ("grpo", "s1_101"), ("chuan", "s1_101"), ("s1_101", "san"), ("grpo", "san")]:
        K = sorted(set(C[a]) & set(C[b]))
        g = ghep(C[a], C[b], K, lambda o: o["dung"])
        out["ghep_cap"][f"{a} − {b}"] = g
        print(f"  {a:7s} − {b:7s} n={g['n']} Δ={g['delta']:+6.2f} [{g['lo']:+.2f}; {g['hi']:+.2f}] b={g['b']} c={g['c']} p={g['p']:.1e}")

    # (2) lát chung với Base (3.566 bước)
    K = sorted(set(C["base"]))
    print(f"\nLát chung {len(K)} bước (Base chấm dở) — bốn thước:")
    thuoc = {"nguoi_nghe": lambda ma, k: C[ma][k]["dung"],
             "exec": lambda ma, k: int(R[ma][k]["executable"]) if ma in R else None,
             "d3": lambda ma, k: L.luat(R[ma][k], k)["d3"] if ma in R else None,
             "aitw": lambda ma, k: aitw_full(R[ma][k], k) if ma in R else None}
    out["lat_base"] = {"n": len(K), "bang": {}, "ghep_cap": {}}
    print(f"  {'nhánh':18s} {'người nghe':>10s} {'exec':>7s} {'D.3':>7s} {'AitW':>7s}")
    for ten, ma, _ in NHANH:
        hang = {}
        for t, f in thuoc.items():
            v = [f(ma, k) for k in K]
            hang[t] = None if v[0] is None else round(100 * sum(v) / len(K), 2)
        out["lat_base"]["bang"][ten] = hang
        print(f"  {ten:18s} " + " ".join(f"{hang[t]:>7.2f}" if hang[t] is not None else f"{'-':>7s}"
                                         for t in thuoc).replace("  ", " ", 0))
    for a, b in [("s1_101", "base"), ("grpo", "base"), ("grpo", "s1_101")]:
        for t, f in thuoc.items():
            U = [(k, f(a, k) - f(b, k)) for k in K]
            pt, (lo, hi), _, _ = S.cluster_bootstrap(U, lambda u: APP[u[0]], lambda u: u[1])
            out["lat_base"]["ghep_cap"][f"{a} − {b} · {t}"] = dict(delta=round(100 * pt, 2), lo=round(100 * lo, 2),
                                                                   hi=round(100 * hi, 2))
            print(f"  {a:6s} − {b:6s} {t:10s} Δ={100*pt:+6.2f} [{100*lo:+.2f}; {100*hi:+.2f}]")

    # tỉ lệ khoảng cách mô hình ↔ câu chuẩn so với khoảng Base ↔ câu chuẩn (lát chung)
    print("\nVị trí trong dải Base → câu chuẩn (lát chung):")
    out["vi_tri_dai"] = {}
    for t in thuoc:
        B_, H_ = out["lat_base"]["bang"]["Base"][t], out["lat_base"]["bang"]["Câu chuẩn"][t]
        for ten in ("S1/101", "Chặng ba (GRPO)"):
            v = out["lat_base"]["bang"][ten][t]
            out["vi_tri_dai"][f"{ten} · {t}"] = round(100 * (v - B_) / (H_ - B_), 1)
            print(f"  {t:10s} {ten:16s} {100*(v-B_)/(H_-B_):5.1f}%")

    # (3b) theo cỡ khối ứng viên, trên 4.463 bước
    print("\nTheo cỡ khối ứng viên (4.463 bước):")
    xo = [(1, 5), (6, 10), (11, 20), (21, 40), (41, 10**6)]
    out["theo_co_khoi"] = {}
    for lo_, hi_ in xo:
        Kx = [k for k, r in som.items() if lo_ <= len(r["boxes"]) <= hi_]
        hang = {ma: round(100 * sum(C[ma][k]["dung"] for k in Kx) / len(Kx), 1) for ma in ("chuan", "grpo", "s1_101", "san")}
        out["theo_co_khoi"][f"{lo_}-{hi_ if hi_ < 10**6 else '∞'}"] = dict(n=len(Kx), **hang)
        print(f"  {lo_:>2d}–{hi_ if hi_ < 10**6 else '∞':<3} n={len(Kx):4d} " + " ".join(f"{m} {v:5.1f}" for m, v in hang.items()))

    # (4) đồng thuận người nghe ↔ UGround
    print("\nĐồng thuận từng bước người nghe (đúng) ↔ UGround (exec):")
    out["dong_thuan"] = {}
    for ma in ("chuan", "grpo", "s1_101"):
        K4 = sorted(C[ma])
        n11 = sum(1 for k in K4 if C[ma][k]["dung"] and R[ma][k]["executable"])
        n10 = sum(1 for k in K4 if C[ma][k]["dung"] and not R[ma][k]["executable"])
        n01 = sum(1 for k in K4 if not C[ma][k]["dung"] and R[ma][k]["executable"])
        n00 = len(K4) - n11 - n10 - n01
        dong = 100 * (n11 + n00) / len(K4)
        pe = ((n11 + n10) * (n11 + n01) + (n00 + n01) * (n00 + n10)) / len(K4) ** 2
        kappa = (dong / 100 - pe) / (1 - pe)
        hoac = 100 * (n11 + n10 + n01) / len(K4)
        out["dong_thuan"][ma] = dict(ca_hai=n11, chi_nguoi_nghe=n10, chi_uground=n01, ca_hai_truot=n00,
                                     dong_thuan=round(dong, 2), kappa=round(kappa, 3), mot_trong_hai=round(hoac, 2))
        print(f"  {ma:7s} cả hai {n11} · chỉ người nghe {n10} · chỉ UGround {n01} · cả hai trượt {n00} · "
              f"đồng thuận {dong:.1f}% κ={kappa:.3f} · một trong hai {hoac:.1f}%")

    q = os.path.join(SOM, "som_phan_tich.json")
    json.dump(out, open(q, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", os.path.relpath(q))


if __name__ == "__main__":
    main()
