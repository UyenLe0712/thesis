# -*- coding: utf-8 -*-
"""Phân tích sâu lưới RL đợt hai (7/11/2026) — 0 GPU, chạy Kaggle CPU.

Câu hỏi chính: ck500 (GRPO + SPICE) hơn nhánh SFT tiếp (cùng 2.000 câu nhắc, cùng số bước) ở đâu, và REINFORCE/RLOO
thua ck500 ở đâu. Chỉ đọc tệp raw đã chấm (UGround), không gọi bộ trỏ.

  python giai_thich_7_11.py --out ../runs/luoi/7_11/giai_thich/giai_thich_7_11.json

Phần:
  A. Phân rã Δexec so S1/101 (cùng định nghĩa phan_ra_luoi.py). Tự kiểm ck500 +28/+41.
  B. Phân rã ghép cặp X − Y (ck500 − SFT tiếp, RL − SFT tiếp, ck500 − REINFORCE/RLOO): phần sửa loại thao tác và phần
     đổi phần tử, mỗi phần có KTC95 bootstrap cụm app (B = 10.000, cùng hàm score_run.cluster_bootstrap).
     Tự kiểm: tổng hai phần = Δexec của doc_luoi (SFT tiếp − ck500 = −0,49 [−1,07; +0,09]).
  C. Δexec theo nhóm: S1 sai loại / đúng loại thao tác; câu hai nhánh trùng / khác; loại thao tác vàng (click/long_press).
  D. Mô tả câu: số từ, câu trống, trùng S1/ck500/SFT tiếp, distinct-1/2, động từ đầu câu, mẫu "Open … app" / "Search".
  E. Họ đầy đủ: exec, D.3, D.3∧14%, AitW đầy đủ của mọi lượt RL đã chấm test + SFT tiếp so ck500, Holm trên exec.
Số mô tả, hậu kiểm, một hạt giống 101.
"""
import argparse, collections, json, os, re, sys, time

from scipy.stats import binomtest

import luat_d3 as L
from luat_aitw_day_du import aitw_full
import score_run as S

B, SEED = 10000, S.SEED
T2, T7 = "luoi/test_2_11", "luoi/7_11/test_u_3"
NHANH = {
    "S1/101": "score_s1_seed101_raw.jsonl",
    "ck500": "grpo_spice/score_ck500_test_raw.jsonl",
    "xao101": "xao101/test/score_ck500_xao101_test_raw.jsonl",
    "SFT tiếp": f"{T7}/score_sft_tiep_101_test_raw.jsonl",
    "REINFORCE + SPICE": f"{T7}/score_reinforce_spice_101_test_raw.jsonl",
    "RLOO + SPICE": f"{T7}/score_rloo_spice_101_test_raw.jsonl",
    "SCST + SPICE": f"{T2}/score_scst_spice_101_test_raw.jsonl",
    "GRPO + CIDEr-D": f"{T2}/score_grpo_cider_101_test_raw.jsonl",
    "GRPO + METEOR": f"{T2}/score_grpo_meteor_101_test_raw.jsonl",
    "GRPO + ROUGE-L": f"{T2}/score_grpo_rougel_101_test_raw.jsonl",
}
COT = {"exec": "vor", "D.3": "d3", "D.3∧14%": "d3_gate", "AitW đầy đủ": "aitwf"}
CAP = [("ck500", "SFT tiếp"), ("REINFORCE + SPICE", "SFT tiếp"), ("RLOO + SPICE", "SFT tiếp"),
       ("ck500", "REINFORCE + SPICE"), ("ck500", "RLOO + SPICE"), ("ck500", "xao101"), ("SFT tiếp", "S1/101")]
t0 = time.time()
LOAI = {(str(d["episode_id"]), str(d["step_id"])): d["action"]["action_type"]
        for d in map(json.loads, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dg1_cache", "test_ac", "test.jsonl"), encoding="utf-8"))}


def log(*a):
    print(f"[{time.time() - t0:6.0f} s]", *a, flush=True)


def nap(f):
    out = {}
    for k, r in L.nap(os.path.join(L.RUNS, f)).items():
        out[k] = dict(L.luat(r, k), aitwf=aitw_full(r, k), cum=r.get("app") or f"ep{r['episode_id']}",
                      e=int(bool(r.get("executable", 0))), a=int(bool(r.get("action_ok", 0))),
                      sent=(r.get("sent") or "").strip(), loai=LOAI.get(k, "?"))
    return out


def ktc(K, f, cum):
    pt, (lo, hi), _, _ = S.cluster_bootstrap([(k, f(k)) for k in K], lambda u: cum[u[0]], lambda u: u[1], B=B, seed=SEED)
    return dict(delta=round(100 * pt, 2), lo=round(100 * lo, 2), hi=round(100 * hi, 2))


def so(A, Bn, c, K, cum):
    r = ktc(K, lambda k: A[k][c] - Bn[k][c], cum)
    cu = sum(A[k][c] > Bn[k][c] for k in K); ph = sum(A[k][c] < Bn[k][c] for k in K)
    r.update(hon=cu, kem=ph, n=len(K), p=binomtest(cu, cu + ph).pvalue if cu + ph else 1.0)
    return r


def phan_ra(X, Y, K):
    """X − Y: cứu = Y trượt X trúng; phần loại = cứu mà Y sai loại − phá mà X sai loại; còn lại là đổi phần tử."""
    cuu = [k for k in K if not Y[k]["e"] and X[k]["e"]]
    pha = [k for k in K if Y[k]["e"] and not X[k]["e"]]
    ca = sum(not Y[k]["a"] for k in cuu); pa = sum(not X[k]["a"] for k in pha)
    return dict(cuu=len(cuu), pha=len(pha), cuu_sua_loai=ca, pha_sai_loai=pa, rong_loai=ca - pa,
                rong_phan_tu=(len(cuu) - ca) - (len(pha) - pa), rong_tong=len(cuu) - len(pha))


def tu(s):
    return re.findall(r"[a-z0-9']+", s.lower())


def mo_ta(R, ref):
    w = [len(tu(r["sent"])) for r in R.values()]
    w.sort()
    u1, u2, n1, n2 = set(), set(), 0, 0
    dong = collections.Counter()
    mau = collections.Counter()
    for r in R.values():
        t = tu(r["sent"])
        u1.update(t); n1 += len(t)
        b = list(zip(t, t[1:])); u2.update(b); n2 += len(b)
        dong[t[0] if t else "<trống>"] += 1
        s = r["sent"].lower()
        mau["open_app"] += bool(re.match(r"^(open|launch)\b.*\bapp\b", s))
        mau["search_for"] += s.startswith("search")
        mau["scroll_swipe"] += bool(re.search(r"\b(scroll|swipe)\b", s))
        mau["go_back"] += bool(re.search(r"\bgo back\b|\bnavigate back\b", s))
        mau["type_enter"] += bool(re.search(r"\b(type|enter|input)\b", s))
    n = len(R)
    out = dict(n=n, tu_tb=round(sum(w) / n, 3), tu_trung_vi=w[n // 2], tu_p90=w[int(0.9 * n)],
               cau_trong=sum(not r["sent"] for r in R.values()), distinct1=round(len(u1) / max(1, n1), 4),
               distinct2=round(len(u2) / max(1, n2), 4), so_cau_khac_nhau=len({r["sent"] for r in R.values()}),
               dong_tu_dau_top10=dong.most_common(10), mau={k: v for k, v in mau.items()})
    for t, Q in ref.items():
        out[f"trung_{t}"] = sum(R[k]["sent"] == Q[k]["sent"] for k in R)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    R = {}
    for t, f in NHANH.items():
        R[t] = nap(f)
        log(f"nạp {t}: {len(R[t])} bước · exec {100 * sum(r['vor'] for r in R[t].values()) / len(R[t]):.2f}")
    K = sorted(R["S1/101"])
    assert len(K) == 4463, len(K)
    for t in R:
        assert set(R[t]) == set(K), t
        lech = sum(R[t][k]["vor"] != R[t][k]["e"] for k in K)
        log(f"  kiểm {t}: vor của luat_d3 lệch trường executable {lech} bước")
        assert lech == 0, t
    cum = {k: R["S1/101"][k]["cum"] for k in K}
    out = {"B": B, "seed": SEED, "n": len(K)}

    # A
    out["A_phan_ra_so_S1"] = {t: phan_ra(R[t], R["S1/101"], K) for t in R if t != "S1/101"}
    for t, v in out["A_phan_ra_so_S1"].items():
        log("A", t, v)
    ck = out["A_phan_ra_so_S1"]["ck500"]
    if (ck["rong_loai"], ck["rong_phan_tu"]) != (28, 41):
        sys.exit(f"⛔ DỪNG, không tái lập ck500 +28/+41: {ck}")
    log("✅ tự kiểm A: ck500 − S1 +28 loại / +41 phần tử")

    # B
    out["B_phan_ra_ghep_cap"] = {}
    for x, y in CAP:
        X, Y = R[x], R[y]
        d = phan_ra(X, Y, K)
        loai = lambda k: int(X[k]["e"] and not Y[k]["e"] and not Y[k]["a"]) - int(Y[k]["e"] and not X[k]["e"] and not X[k]["a"])
        d["exec"] = so(X, Y, "vor", K, cum)
        d["ktc_loai"] = ktc(K, loai, cum)
        d["ktc_phan_tu"] = ktc(K, lambda k: (X[k]["e"] - Y[k]["e"]) - loai(k), cum)
        d["action_ok"] = so(X, Y, "a", K, cum)
        c2 = [k for k in K if X[k]["a"] and Y[k]["a"]]
        d["ca_hai_dung_loai"] = so(X, Y, "vor", c2, cum)
        out["B_phan_ra_ghep_cap"][f"{x} − {y}"] = d
        log("B", x, "−", y, json.dumps(d, ensure_ascii=False))
    g = out["B_phan_ra_ghep_cap"]["ck500 − SFT tiếp"]["exec"]
    if max(abs(g["delta"] - 0.49), abs(g["lo"] + 0.09), abs(g["hi"] - 1.07)) > 0.011:
        sys.exit(f"⛔ DỪNG, không tái lập ck500 − SFT tiếp +0,49 [−0,09; +1,07]: {g}")
    log("✅ tự kiểm B: ck500 − SFT tiếp exec", g)

    # C
    out["C_theo_nhom"] = {}
    s1 = R["S1/101"]
    nhom = {"S1 sai loại": [k for k in K if not s1[k]["a"]], "S1 đúng loại": [k for k in K if s1[k]["a"]]}
    loai_vang = collections.Counter(s1[k]["loai"] for k in K)
    for lv in loai_vang:
        nhom[f"loại vàng {lv}"] = [k for k in K if s1[k]["loai"] == lv]
    for x, y in CAP[:5]:
        X, Y = R[x], R[y]
        r = {}
        for ten, ks in nhom.items():
            if len(ks) >= 30:
                r[ten] = so(X, Y, "vor", ks, cum)
        tr = [k for k in K if X[k]["sent"] == Y[k]["sent"]]; kh = [k for k in K if X[k]["sent"] != Y[k]["sent"]]
        r["câu khác nhau"] = so(X, Y, "vor", kh, cum)
        r["câu trùng (phải 0 bất đồng)"] = dict(n=len(tr), bat_dong=sum(X[k]["vor"] != Y[k]["vor"] for k in tr))
        out["C_theo_nhom"][f"{x} − {y}"] = r
        log("C", x, "−", y, json.dumps(r, ensure_ascii=False))
        assert r["câu trùng (phải 0 bất đồng)"]["bat_dong"] == 0, "câu trùng mà exec khác: bộ trỏ không tất định?"
    out["C_loai_vang"] = dict(loai_vang)
    assert "?" not in loai_vang, loai_vang

    # D
    ref = {t: R[t] for t in ("S1/101", "ck500", "SFT tiếp")}
    out["D_mo_ta"] = {t: mo_ta(R[t], ref) for t in R}
    for t, v in out["D_mo_ta"].items():
        log("D", t, json.dumps(v, ensure_ascii=False))

    # E
    out["E_ho_so_ck500"] = {}
    for t in R:
        if t in ("ck500", "S1/101"):
            continue
        out["E_ho_so_ck500"][t] = {ten: so(R[t], R["ck500"], c, K, cum) for ten, c in COT.items()}
    out["E_diem"] = {t: {ten: round(100 * sum(r[c] for r in R[t].values()) / len(K), 2) for ten, c in COT.items()} for t in R}
    ho = [t for t in out["E_ho_so_ck500"] if t != "xao101"]
    ps = sorted((out["E_ho_so_ck500"][t]["exec"]["p"], t) for t in ho)
    out["E_holm_exec"], tich = {}, 0.0
    for i, (p, t) in enumerate(ps):
        tich = max(tich, min(1.0, p * (len(ps) - i)))
        out["E_holm_exec"][t] = dict(delta=out["E_ho_so_ck500"][t]["exec"]["delta"], p=p, p_holm=tich)
    log("E holm", json.dumps(out["E_holm_exec"], ensure_ascii=False))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    log("[xong] ghi", a.out)


if __name__ == "__main__":
    main()
