# -*- coding: utf-8 -*-
"""Bộ đọc phễu sàng (val lớn) và xác nhận (test) của 289 = 288 bản 4 (B.13 của 288).

    python _scripts/289/doc_289.py sang --nhanh S1:… --nhanh ck500:… --nhanh tspicea:… --nhanh tnghev:… --nhanh tnghe:… \
           [--dung tnghev] --out vallon289/sang_289.json
    python _scripts/289/doc_289.py test --sang vallon289/sang_289.json --nhanh base:… --nhanh S1:… --nhanh ck500:… \
           --nhanh tspicea:… --nhanh tnghev:… --venus ck500:… --venus tnghev:… --out goc289/test_289.json
    python _scripts/289/doc_289.py kiem [--repo R]          # tự kiểm trên dữ liệu thật của repo + nhánh giả

Ba nhánh của 289 (đều train TIẾP 250 bước từ ck500, cùng 1.000 câu nhắc hạt 101, cùng phiên A100):
tspicea (SPICE y ck500, đối chứng "train lâu hơn") · tnghev (người nghe có cổng v) · tnghe (không cổng).
Luật khoá ở §00.5 / Phụ lục A mục 7. Val lớn CHỈ để chọn — cấm viết số val vào luận văn như kết quả.
Sửa 6/10 (chủ luận văn giao quyết): thêm hai nhánh liều mạnh tnghevm/tnghem, ngưỡng sàng +0,5.
Viết lại 6/10/2026 từ bản mô tả B.13 (mã gốc ở máy Mac) ⇒ md5 khác bản gốc (6c1b97f4…).
"""
import argparse, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from doc_286 import cluster_ci, mcnemar

NGUONG_SANG = 0.5          # 6/10: hạ từ 1,0 (chấm test trên Kaggle không tốn tiền ⇒ không loại sớm nhánh có triển vọng)
XS = ("tnghev", "tnghe", "tnghevm", "tnghem")      # "m" = liều mạnh W = 2
CAP_V = (("tnghev", "tnghe"), ("tnghevm", "tnghem"))   # (có cổng v, không cổng) cùng liều
N_VAL = 1002


def nap_raw(p):
    out = {}
    for l in open(p, encoding="utf-8"):
        if l.strip():
            o = json.loads(l)
            out[(o["episode_id"], o["step_id"])] = int(o.get("executable") or 0)
    return out


def so(A, B, q=0.025):
    keys = sorted(A.keys() & B.keys())
    a = np.array([A[k] for k in keys], float); b = np.array([B[k] for k in keys], float)
    d, lo, hi = cluster_ci(a - b, [k[0] for k in keys], np.random.default_rng(101), q=q)
    cuu, pha = int(((a == 1) & (b == 0)).sum()), int(((a == 0) & (b == 1)).sum())
    return {"n": len(keys), "a": round(100 * a.mean(), 2), "b": round(100 * b.mean(), 2), "d": round(d, 2),
            "lo": round(lo, 2), "hi": round(hi, 2), "ktc": round(100 * (1 - 2 * q), 2), "cuu": cuu, "pha": pha,
            "p": round(mcnemar(cuu, pha), 4)}


def dong(ten, r):
    return (f"  {ten:<22} n={r['n']:>5} · {r['a']:6.2f} vs {r['b']:6.2f} · Δ {r['d']:+6.2f} "
            f"[{r['lo']:+.2f}; {r['hi']:+.2f}] (KTC {r['ktc']:g}%) · cứu {r['cuu']} phá {r['pha']}")


# ─────────────────────────── sàng ───────────────────────────
def sang(N, dung=(), can_1002=True, in_ra=True):
    """N: {tên: {khoá: exec}}. → {"len": [...], "ket_cuc", "ly_do", "so"}."""
    for t in ("S1", "ck500", "tspicea"):
        if t not in N:
            raise SystemExit(f"DỪNG: sàng bắt buộc có {t}")
    for t, v in N.items():
        if can_1002 and len(v) != N_VAL:
            raise SystemExit(f"DỪNG: {t} có {len(v)} bước, cần đủ {N_VAL} (chấm nốt rồi đọc lại)")
        if v.keys() != N["S1"].keys():
            raise SystemExit(f"DỪNG: {t} lệch tập bước với S1 ({len(v)} vs {len(N['S1'])}) — tệp thiếu bước")
    P = {}
    for t in N:
        if t != "S1":
            P[f"{t}-S1"] = so(N[t], N["S1"])
        if t not in ("S1", "ck500"):
            P[f"{t}-ck500"] = so(N[t], N["ck500"])
    len_, ly = [], {}
    for x in XS:
        if x not in N:
            ly[x] = "dừng theo luật train" if x in dung else "không train"
            continue
        P[f"{x}-tspicea"] = so(N[x], N["tspicea"])
        du, dc = P[f"{x}-tspicea"]["d"], P[f"{x}-ck500"]["d"]
        if dc >= NGUONG_SANG and du > 0:
            len_.append(x); ly[x] = f"LÊN (Δ−ck500 {dc:+.2f}, Δ−tspicea {du:+.2f})"
        else:
            ly[x] = f"không lên (Δ−ck500 {dc:+.2f}, cần ≥ {NGUONG_SANG}; Δ−tspicea {du:+.2f}, cần > 0)"
    for v_, k_ in CAP_V:
        if v_ in N and k_ in N:
            P[f"{v_}-{k_}"] = so(N[v_], N[k_])
    if len_:
        len_.append("tspicea"); ly["tspicea"] = "LÊN (đối chứng bắt buộc)"
        kc = "LÊN TEST"
    elif P["tspicea-ck500"]["d"] >= NGUONG_SANG:
        len_ = ["tspicea"]; ly["tspicea"] = f"LÊN một mình (Δ−ck500 {P['tspicea-ck500']['d']:+.2f}) — chỉ là \"train lâu hơn\""
        kc = "LÊN TEST"
    else:
        kc = "DỪNG"; ly["tspicea"] = f"không lên (Δ−ck500 {P['tspicea-ck500']['d']:+.2f})"
    if in_ra:
        print("SÀNG (val lớn — chỉ để chọn, cấm viết vào luận văn như kết quả)")
        for k, r in P.items():
            print(dong(k, r))
        for k, v in ly.items():
            print(f"  {k}: {v}")
        print(f"⇒ {kc}: {len_ if len_ else 'không chấm test nhánh nào; đóng góp mô hình = ck500'}")
    return {"len": len_, "ket_cuc": kc, "ly_do": ly, "so": P}


# ─────────────────────────── xác nhận ───────────────────────────
def xac_nhan(len_, N, V, in_ra=True):
    X = [x for x in len_ if x in XS]
    q = 0.025 / max(len(X), 1)
    for t in ["S1", "ck500"] + list(len_):
        if t not in N:
            raise SystemExit(f"DỪNG: thiếu tệp test của {t}")
    P, chay_them, vuot, dk = {}, [], {}, {}
    for t in len_:
        for m in ("base", "S1", "ck500"):
            if m in N:
                P[f"{t}-{m}"] = so(N[t], N[m])
    for a_, b_ in (("S1", "base"), ("ck500", "base"), ("ck500", "S1")):
        if a_ in N and b_ in N:
            P[f"{a_}-{b_}"] = so(N[a_], N[b_])
    if "tspicea" in N:
        P["tspicea-ck500"] = so(N["tspicea"], N["ck500"])
    for x in X:
        c, s = so(N[x], N["ck500"], q), so(N[x], N["S1"], q)
        P[f"{x}-ck500 (Bonf.)"], P[f"{x}-S1 (Bonf.)"] = c, s
        u = so(N[x], N["tspicea"]) if "tspicea" in N else None
        if u:
            P[f"{x}-tspicea"] = u
        else:
            chay_them.append("test tspicea")
        v = so(V[x], V["ck500"]) if x in V and "ck500" in V else None
        if v:
            P[f"UI-Venus {x}-ck500"] = v
        else:
            chay_them.append(f"UI-Venus {x}" if "ck500" in V else "UI-Venus ck500")
        dk[x] = {"LB(X−ck500)>0": c["lo"] > 0, "LB(X−S1)>0": s["lo"] > 0,
                 "Δ(X−tspicea)>0": bool(u and u["d"] > 0), "Δ_UIVenus(X−ck500)>0": bool(v and v["d"] > 0)}
        vuot[x] = all(dk[x].values())
    v_gay_ra = None
    for v_, k_ in CAP_V:
        if vuot.get(v_):
            if k_ in N:
                P[f"{v_}-{k_}"] = so(N[v_], N[k_])
                v_gay_ra = bool(v_gay_ra) or P[f"{v_}-{k_}"]["lo"] > 0
            else:
                chay_them.append(f"test {k_}")
    chay_them = sorted(set(chay_them))
    if chay_them:
        kc = "CHỜ: " + ", ".join(chay_them)
    elif not X:
        lb = P.get("tspicea-ck500", {}).get("lo", -1)
        kc = "T0 — không thành phần mới" + (" (train lâu hơn nâng exec có ý nghĩa: LB(tspicea−ck500) > 0)" if lb > 0 else "")
    elif not any(vuot.values()):
        kc = "T1 — thưởng người nghe tăng trên val nhưng không qua xác nhận trên test"
    elif v_gay_ra:
        kc = "T3 — VƯỢT ∧ v gây ra"
    else:
        kc = "T2 — VƯỢT" + (", cổng v KHÔNG được chứng minh" if vuot.get("tnghev") or vuot.get("tnghevm") else "")
    if in_ra:
        print(f"XÁC NHẬN (test, k = {len(X)} nhánh người nghe, KTC Bonferroni {100 * (1 - 2 * q):g}%)")
        for k, r in P.items():
            print(dong(k, r))
        for x, d in dk.items():
            print(f"  {x}: {' · '.join(f'{k} {chr(10003) if v else chr(10007)}' for k, v in d.items())} ⇒ VƯỢT {vuot[x]}")
        print(f"⇒ KẾT CỤC: {kc}")
    return {"ket_cuc": kc, "vuot": vuot, "dieu_kien": dk, "v_gay_ra": v_gay_ra, "chay_them": chay_them, "so": P}


# ─────────────────────────── tự kiểm ───────────────────────────
def gia(N0, n, hat, chieu=1, pha=0):
    rng = np.random.default_rng(hat)
    N = dict(N0)

    def lat(v0, m):
        k = np.array(sorted(x for x, v in N0.items() if v == v0))
        if m == 0 or len(k) == 0:
            return []
        return [tuple(int(t) for t in r) for r in rng.permutation(k)[:m]]
    v1 = 0 if chieu > 0 else 1
    for k in lat(v1, n):
        N[k] = 1 - v1
    for k in lat(1 - v1, pha):
        N[k] = v1
    return N


def kiem(repo):
    R = lambda *p: os.path.join(repo, "runs", *p)
    ok = []

    def chk(ten, dk):
        ok.append(dk); print(("✅ " if dk else "⛔ ") + ten, flush=True)

    S1c, c5c = nap_raw(R("grpo_spice", "score_k0_lai500_raw.jsonl")), nap_raw(R("grpo_spice", "score_ck500_raw.jsonl"))
    CA = [("X +2,4 hơn cả hai", {"tnghev": gia(c5c, 6, 1)}, (), ["tnghev", "tspicea"]),
          ("X +0,8", {"tnghev": gia(c5c, 2, 1)}, (), ["tnghev", "tspicea"]),
          ("X +0,4", {"tnghev": gia(c5c, 1, 1)}, (), []),
          ("tspicea +2,0, X = tspicea", {"tspicea": gia(c5c, 5, 2), "tnghev": gia(c5c, 5, 2)}, (), ["tspicea"]),
          ("X hơn ck500 +3,2, hơn tspicea +0,4", {"tspicea": gia(c5c, 7, 3), "tnghev": gia(c5c, 8, 3)}, (), ["tnghev", "tspicea"]),
          ("X hơn ck500 +2,8, thua tspicea", {"tspicea": gia(c5c, 8, 3), "tnghev": gia(c5c, 7, 3)}, (), ["tspicea"]),
          ("nhánh liều mạnh lên", {"tnghem": gia(c5c, 6, 1)}, (), ["tnghem", "tspicea"]),
          ("cả hai X lên", {"tnghev": gia(c5c, 6, 1), "tnghe": gia(c5c, 4, 5)}, (), ["tnghev", "tnghe", "tspicea"]),
          ("tnghev dừng, tnghe lên", {"tnghe": gia(c5c, 4, 5)}, ("tnghev",), ["tnghe", "tspicea"]),
          ("không ai lên", {"tspicea": gia(c5c, 1, 9)}, (), [])]
    for ten, ex, dung, mong in CA:
        N = {"S1": S1c, "ck500": c5c, "tspicea": c5c, **ex}
        kq = sang(N, dung, can_1002=False, in_ra=False)
        chk(f"sàng C1 · {ten}: {kq['len'] or 'DỪNG'}", sorted(kq["len"]) == sorted(mong) and (kq["ket_cuc"] == "DỪNG") == (not mong))
    try:
        sang({"S1": S1c, "ck500": c5c, "tspicea": c5c}, in_ra=False); chk("sàng đòi 1.002 bước chặn tệp 249 bước", False)
    except SystemExit:
        chk("sàng đòi 1.002 bước chặn tệp 249 bước", True)
    thieu = dict(c5c); thieu.pop(next(iter(thieu)))
    try:
        sang({"S1": S1c, "ck500": c5c, "tspicea": thieu}, can_1002=False, in_ra=False); chk("tệp thiếu bước ⇒ dừng", False)
    except SystemExit:
        chk("tệp thiếu bước ⇒ dừng", True)

    base, S1, c5 = nap_raw(R("score_base_raw.jsonl")), nap_raw(R("score_s1_seed101_raw.jsonl")), nap_raw(R("grpo_spice", "score_ck500_test_raw.jsonl"))
    r = so(c5, S1)
    chk(f"tái lập test thật: ck500−S1 = ({r['a']}; {r['b']}; {r['d']:+}) [{r['lo']:+}; {r['hi']:+}] · base {so(base, S1)['a']}",
        (r["a"], r["b"], r["d"]) == (60.65, 59.11, 1.55) and so(base, S1)["a"] == 47.59)
    Vs = nap_raw(R("venus", "score_venus_s1_2532_raw.jsonl"))
    X3 = gia(c5, 334, 11, pha=200)
    Vok = gia(Vs, 30, 1)
    TC = [("tnghe = X3, venus tnghe +", ["tnghe", "tspicea"], {"tnghe": X3}, {"tnghe": Vok}, "T2"),
          ("như trên nhưng không có venus", ["tnghe", "tspicea"], {"tnghe": X3}, {}, "CHỜ"),
          ("venus tnghe chiều xấu", ["tnghe", "tspicea"], {"tnghe": X3}, {"tnghe": gia(Vs, 30, 1, -1)}, "T1"),
          ("tnghe ≈ +0,5", ["tnghe", "tspicea"], {"tnghe": gia(c5, 222, 11, pha=200)}, {"tnghe": Vok}, "T1"),
          ("tnghev = X3, chưa có tnghe", ["tnghev", "tspicea"], {"tnghev": X3}, {"tnghev": Vok}, "CHỜ"),
          ("tnghev = X3, tnghe ≈ +0,2", ["tnghev", "tspicea"], {"tnghev": X3, "tnghe": gia(c5, 210, 4, pha=200)}, {"tnghev": Vok}, "T3"),
          ("tnghev = tnghe = X3", ["tnghev", "tspicea"], {"tnghev": X3, "tnghe": X3}, {"tnghev": Vok}, "T2"),
          ("tspicea +4,5, tnghe = X3", ["tnghe", "tspicea"], {"tspicea": gia(c5, 400, 12, pha=200), "tnghe": X3}, {"tnghe": Vok}, "T1"),
          ("chỉ tspicea = X3", ["tspicea"], {"tspicea": X3}, {}, "T0")]
    for ten, len_, ex, vx, mong in TC:
        N = {"base": base, "S1": S1, "ck500": c5, "tspicea": c5, **ex}
        V = {"ck500": Vs, **vx}
        kq = xac_nhan(len_, N, V, in_ra=False)
        chk(f"test · {ten}: {kq['ket_cuc'][:60]}", kq["ket_cuc"].startswith(mong))
    print(f"{'✅ tự kiểm ĐẠT' if all(ok) else '⛔ tự kiểm RỚT'} ({sum(ok)}/{len(ok)})")
    sys.exit(0 if all(ok) else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("che_do", choices=["sang", "test", "kiem"])
    ap.add_argument("--nhanh", action="append", default=[])
    ap.add_argument("--venus", action="append", default=[])
    ap.add_argument("--dung", action="append", default=[])
    ap.add_argument("--sang")
    ap.add_argument("--repo", default=os.path.abspath(os.path.join(HERE, "..", "..")))
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.che_do == "kiem":
        kiem(a.repo)
    tach = lambda xs: {x.split(":", 1)[0]: nap_raw(x.split(":", 1)[1]) for x in xs}
    N, V = tach(a.nhanh), tach(a.venus)
    if a.che_do == "sang":
        kq = sang(N, a.dung)
    else:
        assert a.sang, "chế độ test bắt buộc --sang sang_289.json"
        S = json.load(open(a.sang, encoding="utf-8"))
        if S["ket_cuc"] == "DỪNG":
            sys.exit("Sàng đã DỪNG — không có nhánh nào lên test.")
        kq = xac_nhan(S["len"], N, V)
    out = a.out or f"{a.che_do}_289.json"
    json.dump(kq, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("ghi", out)


if __name__ == "__main__":
    main()
