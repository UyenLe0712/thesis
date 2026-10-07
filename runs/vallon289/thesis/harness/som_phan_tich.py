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


def nap_file(p):
    d = {}
    for l in open(p, encoding="utf-8"):
        o = json.loads(l); d[(str(o["episode_id"]), str(o["step_id"]))] = o
    return d


def nap_chon(ma):
    return nap_file(os.path.join(SOM, f"chon_phi4_{ma}.jsonl"))


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

    # (5) toàn vẹn: tệp gộp = hợp hai nửa GPU, không trùng, đúng chẵn/lẻ theo chỉ số; tất định với lát thử
    print("\nToàn vẹn tệp:")
    thu_tu = [(str(r["episode_id"]), str(r["step_id"])) for r in
              map(json.loads, open(os.path.join(HERE, "dg1_cache", "som", "som.jsonl"), encoding="utf-8"))]
    vi = {k: i for i, k in enumerate(thu_tu)}
    out["toan_ven"] = {}
    for _, ma, _ in NHANH:
        s0 = nap_file(os.path.join(SOM, f"chon_phi4_{ma}_s0.jsonl")); s1 = nap_file(os.path.join(SOM, f"chon_phi4_{ma}_s1.jsonl"))
        dong = sum(1 for _ in open(os.path.join(SOM, f"chon_phi4_{ma}.jsonl"), encoding="utf-8"))
        ok = (set(s0) | set(s1) == set(C[ma]) and not set(s0) & set(s1) and dong == len(C[ma])
              and all(vi[k] % 2 == 0 for k in s0) and all(vi[k] % 2 == 1 for k in s1))
        oom = sum(1 for o in C[ma].values() if o["raw"] == "__OOM__")
        khong_so = sum(1 for o in C[ma].values() if o["raw"] and o["chon"] is None)
        rong = sum(1 for o in C[ma].values() if not o["raw"])
        out["toan_ven"][ma] = dict(n=len(C[ma]), s0=len(s0), s1=len(s1), dat=ok, oom=oom, khong_ra_so=khong_so,
                                   khong_goi_mo_hinh=rong)
        print(f"  {ma:7s} n={len(C[ma])} s0={len(s0)} s1={len(s1)} đạt={ok} OOM={oom} không ra số={khong_so} "
              f"không gọi mô hình (câu rỗng/không ô)={rong}")
    for ma in ("chuan", "san"):
        M = nap_file(os.path.join(SOM, f"chon_phi4_{ma}_mau200.jsonl"))
        trung = sum(1 for k in M if M[k]["raw"] == C[ma][k]["raw"])
        out["toan_ven"][f"{ma}_tat_dinh_lat200"] = f"{trung}/{len(M)}"
        print(f"  lát 200 {ma}: câu trả lời thô trùng lượt đủ {trung}/{len(M)}")
    P = nap_file(os.path.join(SOM, "chon_pixtral_chuan_mau200.jsonl"))
    co_so = [o for o in P.values() if o["chon"] is not None]
    mo_dau = collections.Counter(" ".join((o["raw"] or "").split()[:2]) for o in P.values() if o["chon"] is None)
    out["pixtral_lat200"] = dict(n=len(P), ra_so=len(co_so), dung=sum(o["dung"] for o in co_so),
                                 mo_dau_khong_ra_so=mo_dau.most_common(5))
    print(f"  Pixtral lát 200: ra số {len(co_so)} · đúng {sum(o['dung'] for o in co_so)} · mở đầu khi không ra số {mo_dau.most_common(4)}")

    # (6) thiên lệch chọn ô: ô số 1 và ô trả lời phổ biến
    print("\nThiên lệch chọn ô (tỉ lệ chọn ô số 1 · tỉ lệ ô 1 là đáp án):")
    out["thien_lech_o1"] = {}
    o1_dap = 100 * sum(1 for k in C["chuan"] if 1 in som[k]["dap_an"]) / len(som)
    for ma in ("chuan", "grpo", "s1_101", "san"):
        t = 100 * sum(1 for o in C[ma].values() if o["chon"] == 1) / len(C[ma])
        out["thien_lech_o1"][ma] = round(t, 2)
        print(f"  {ma:7s} chọn ô 1: {t:5.2f}%")
    out["thien_lech_o1"]["o1_la_dap_an"] = round(o1_dap, 2)
    print(f"  ô 1 là đáp án: {o1_dap:.2f}%")

    # (7) có điều kiện: bước có đáp án trong khối; bước UGround trúng / trượt
    print("\nCó điều kiện:")
    out["co_dieu_kien"] = {}
    Kd = [k for k in som if som[k]["dap_an"]]
    for ma in ("chuan", "grpo", "s1_101", "san"):
        v = 100 * sum(C[ma][k]["dung"] for k in Kd) / len(Kd)
        hang = dict(co_dap_an=round(v, 2), n_co_dap_an=len(Kd))
        if ma in R:
            Kh = [k for k in C[ma] if R[ma][k]["executable"]]; Km = [k for k in C[ma] if not R[ma][k]["executable"]]
            hang.update(khi_uground_trung=round(100 * sum(C[ma][k]["dung"] for k in Kh) / len(Kh), 2), n_trung=len(Kh),
                        khi_uground_truot=round(100 * sum(C[ma][k]["dung"] for k in Km) / len(Km), 2), n_truot=len(Km))
        out["co_dieu_kien"][ma] = hang
        print(f"  {ma:7s} " + " · ".join(f"{a}={b}" for a, b in hang.items()))

    # (8) chặng ba vs S1: câu giống hệt / khác nhau; chiều lật dưới người nghe so với chiều lật dưới UGround
    print("\nChặng ba − S1/101 tách theo câu:")
    cau = {ma: {(str(o["episode_id"]), str(o["step_id"])): o["sent"] for o in
                map(json.loads, open(os.path.join(HERE, "dg1_cache", "som", f"cau_{ma}.jsonl"), encoding="utf-8"))}
           for ma in ("grpo", "s1_101")}
    giong = [k for k in som if cau["grpo"][k].strip() == cau["s1_101"][k].strip()]
    khac = [k for k in som if k not in set(giong)]
    lech_giong = sum(1 for k in giong if C["grpo"][k]["dung"] != C["s1_101"][k]["dung"])
    g_khac = ghep(C["grpo"], C["s1_101"], khac, lambda o: o["dung"])
    out["grpo_s1_theo_cau"] = dict(cau_giong=len(giong), lech_tren_cau_giong=lech_giong, cau_khac=g_khac)
    print(f"  câu giống hệt {len(giong)} bước (người nghe cho kết quả khác ở {lech_giong}) · "
          f"câu khác {g_khac['n']} bước Δ={g_khac['delta']:+.2f} [{g_khac['lo']:+.2f}; {g_khac['hi']:+.2f}] b={g_khac['b']} c={g_khac['c']}")
    ug = {k: int(R["grpo"][k]["executable"]) - int(R["s1_101"][k]["executable"]) for k in som}
    ln = {k: C["grpo"][k]["dung"] - C["s1_101"][k]["dung"] for k in som}
    bang = collections.Counter((ug[k], ln[k]) for k in som)
    out["lat_chieu"] = {f"UGround {a:+d} · người nghe {b:+d}": v for (a, b), v in sorted(bang.items())}
    cung = bang[(1, 1)] + bang[(-1, -1)]; nguoc = bang[(1, -1)] + bang[(-1, 1)]
    print(f"  bước cả hai dụng cụ cùng lật: cùng chiều {cung} · ngược chiều {nguoc}")
    for (a, b), v in sorted(bang.items()):
        print(f"    UGround {a:+d} · người nghe {b:+d}: {v}")
    out["lat_chieu_tom"] = dict(cung_chieu=cung, nguoc_chieu=nguoc)

    # (9) dải hữu dụng (trần − câu rỗng) cùng lát 800 của runs/floor
    K8 = sorted(L.nap(os.path.join(RUNS, "floor", "score_f1_trong_raw.jsonl")))
    K8 = [k for k in K8 if k in C["chuan"]]
    t8 = 100 * sum(C["chuan"][k]["dung"] for k in K8) / len(K8)
    s8 = 100 * sum(C["san"][k]["dung"] for k in K8) / len(K8)
    out["dai_lat800"] = dict(n=len(K8), tran=round(t8, 2), san=round(s8, 2), dai=round(t8 - s8, 2))
    print(f"\nLát 800 (cùng lát sàn của exec): trần {t8:.2f} · câu rỗng {s8:.2f} · dải {t8-s8:.2f}")

    q = os.path.join(SOM, "som_phan_tich.json")
    json.dump(out, open(q, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", os.path.relpath(q))


if __name__ == "__main__":
    main()
