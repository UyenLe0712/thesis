# -*- coding: utf-8 -*-
"""Đọc kết quả TAGE trên TẬP TEST (Kaggle commit 4/10/2026, `runs/tage_test/`) — 0 GPU.

    ~/.venvs/thesis/bin/python harness/tage_test_doc.py      # cần Java 8 cho SPICE

Hệ TAGE pred+cổng trên test = câu nháp ck500, trừ các bước cổng (τ = 0,73767, chọn trên val) nhận câu sửa.
Bước giữ câu nháp lấy kết quả chấm ck500 test đã có; bước nhận sửa lấy `score_pred_cong_raw.jsonl` (cùng
`score_run.py`, cùng T4). So S1/101 và ck500 trên đúng 4.463 bước, ghép cặp, KTC bằng hàm của `d3_ktc.py`.

Tự kiểm trước khi in số (lệch là dừng): câu nháp trong meta trùng `pred_ck500_test.jsonl`; tệp cổng khớp
luật τ áp lại trên meta; câu trong tệp chấm mới trùng câu sửa; ck500 exec 60,65 tái lập.
"""
import collections, json, os, statistics, sys

import grpo_spice_test_doc as GD          # đặt JAVA_HOME + hàm SPICE
import luat_d3 as L
from d3_ktc import ktc, mcnemar
from luat_aitw_day_du import aitw_full

T = os.path.join(L.RUNS, "tage_test")
TAU = 0.73767
kh = lambda d: (str(d["episode_id"]), str(d["step_id"]))
jl = lambda p: [json.loads(l) for l in open(p, encoding="utf-8")]


def bo(R):
    return {k: dict(L.luat(r, k), aitwf=aitw_full(r, k), aok=int(bool(r.get("action_ok"))),
                    sent=(r.get("sent") or "").strip(), gold=(r.get("gold_instruction") or "").strip(),
                    cum=r.get("app") or f"ep{r['episode_id']}", ep=f"ep{r['episode_id']}")
            for k, r in R.items()}


def main():
    loi = []
    R_s1 = L.nap(os.path.join(L.RUNS, "score_s1_seed101_raw.jsonl"))
    R_ck = L.nap(os.path.join(L.RUNS, "grpo_spice/score_ck500_test_raw.jsonl"))
    M = {kh(d): d for f in ("pred_test_s0_meta.jsonl", "pred_test_s1_meta.jsonl") for d in jl(os.path.join(T, f))}
    LOC = {kh(d): d for d in jl(os.path.join(T, "loc_test.jsonl"))}
    CONG = {kh(d): d["pred"] for d in jl(os.path.join(T, "pred_test_cong.jsonl"))}
    R_new = {kh(r): r for r in jl(os.path.join(T, "score_pred_cong_raw.jsonl"))}
    K = list(R_s1)

    # ── tự kiểm ──
    if not (len(K) == 4463 and set(K) == set(R_ck) == set(M) == set(LOC)):
        loi.append(f"quần thể lệch: S1 {len(K)} · ck500 {len(R_ck)} · meta {len(M)} · loc {len(LOC)}")
    P = {kh(d): d["pred"].strip() for d in jl(os.path.join(L.RUNS, "grpo_spice/pred_ck500_test.jsonl"))}
    lech = [k for k in K if M[k]["draft"].strip() != P[k]]
    if lech:
        loi.append(f"{len(lech)} câu nháp ≠ pred_ck500_test")
    nhan = {k for k, d in M.items() if d["lp_edit"] - d["lp_draft"] > TAU and d["edit"] != d["draft"]}
    if nhan != set(CONG):
        loi.append(f"tập cổng nhận {len(nhan)} ≠ pred_test_cong {len(CONG)}")
    if set(R_new) != set(CONG):
        loi.append("tệp chấm mới không trùng tập cổng nhận")
    lech2 = [k for k in R_new if (R_new[k].get("sent") or "").strip() != CONG[k].strip()]
    if lech2:
        loi.append(f"{len(lech2)} câu trong tệp chấm ≠ câu sửa")
    if abs(100 * sum(int(R_ck[k]["executable"]) for k in K) / 4463 - 60.65) > 0.006:
        loi.append("ck500 exec ≠ 60,65")
    if loi:
        sys.exit("⛔ DỪNG: " + " · ".join(loi))
    print(f"✅ tự kiểm đạt: 4.463 bước · câu nháp = ck500 · cổng nhận {len(nhan)} khớp · câu chấm khớp")

    # ── dựng hệ TAGE ──
    R_tage = {k: (dict(R_new[k], **{f: R_new[k].get(f, 0) for f in ("executable", "action_ok", "toggle_ok", "hit_disk")})
                  if k in nhan else R_ck[k]) for k in K}
    A, C, B = bo(R_s1), bo(R_ck), bo(R_tage)
    cum = {k: A[k]["cum"] for k in K}
    cum_ep = {k: A[k]["ep"] for k in K}
    out = {"n_nhan": len(nhan)}

    # ── 1. đường ống ──
    hit = sum(LOC[k]["hit_disk"] for k in K)
    doi = sum(M[k]["edit"].strip() != M[k]["draft"].strip() for k in K)
    lp = [M[k]["lp_edit"] - M[k]["lp_draft"] for k in K if M[k]["edit"] != M[k]["draft"]]
    print(f"\n[1. đường ống] bộ định vị trúng ±14%: {hit}/4463 = {100*hit/4463:.2f}% (val 193/249 = 77,5%)")
    print(f"  bộ biên tập đổi câu {doi}/4463 = {100*doi/4463:.1f}% · Δlp (câu đổi) trung vị {statistics.median(lp):+.3f}"
          f" · p90 {sorted(lp)[int(.9*len(lp))]:+.3f}")
    print(f"  cổng τ={TAU} nhận {len(nhan)}/4463 = {100*len(nhan)/4463:.2f}% (val 11/249 = 4,4%)")
    out["pipeline"] = dict(loc_hit=hit, doi_cau=doi, nhan=len(nhan))

    # ── 2. bảng chính ──
    print("\n[SPICE] chạy Java …", flush=True)
    for X in (A, C, B):
        tb, ds = GD.spice_tung_cau([X[k]["sent"] for k in K], [X[k]["gold"] for k in K])
        for k, v in zip(K, ds):
            X[k]["spice"] = v / 100
    out["diem"], out["so"] = {}, {}
    print(f"\n[2. bảng 4.463 bước]\n{'thước':12s} {'S1/101':>7s} {'ck500':>7s} {'TAGE':>7s}  "
          f"{'TAGE−S1 [KTC app]':>24s} {'p':>8s}  {'TAGE−ck500 [KTC app]':>24s} {'cứu':>4s} {'phá':>4s} {'p':>8s}")
    for cot, ten in (("vor", "exec"), ("d3", "D.3"), ("aitwf", "AitW đầy đủ"), ("d14_truc", "±14% trục"),
                     ("aok", "action_ok"), ("spice", "SPICE")):
        s = [100 * sum(X[k][cot] for k in K) / 4463 for X in (A, C, B)]
        d1, lo1, hi1, _ = ktc(K, lambda k, c: B[k][c] - A[k][c], cot, cum)
        d2, lo2, hi2, _ = ktc(K, lambda k, c: B[k][c] - C[k][c], cot, cum)
        _, elo, ehi, _ = ktc(K, lambda k, c: B[k][c] - A[k][c], cot, cum_ep)
        if cot == "spice":
            p1 = p2 = float("nan"); b2 = c2 = 0
        else:
            *_, p1 = mcnemar(K, A, B, cot)
            b2, c2, _, p2 = mcnemar(K, C, B, cot)
        out["diem"][ten] = dict(S1=round(s[0], 2), ck500=round(s[1], 2), TAGE=round(s[2], 2))
        out["so"][ten] = dict(tage_s1=[round(d1, 2), round(lo1, 2), round(hi1, 2)], tage_s1_ep=[round(elo, 2), round(ehi, 2)],
                              p_s1=p1, tage_ck=[round(d2, 2), round(lo2, 2), round(hi2, 2)], cuu=c2, pha=b2, p_ck=p2)
        print(f"{ten:12s} {s[0]:7.2f} {s[1]:7.2f} {s[2]:7.2f}  {d1:+6.2f} [{lo1:+5.2f}; {hi1:+5.2f}] {p1:8.1e}"
              f"  {d2:+6.2f} [{lo2:+5.2f}; {hi2:+5.2f}] {c2:4d} {b2:4d} {p2:8.1e}")

    # ── 3. riêng các bước cổng nhận sửa ──
    N = [k for k in K if k in nhan]
    e = lambda X, S_, c="vor": sum(X[k][c] for k in S_)
    print(f"\n[3. {len(N)} bước cổng nhận sửa] exec ck500 {e(C,N)} ({100*e(C,N)/len(N):.1f}%) → TAGE {e(B,N)}"
          f" ({100*e(B,N)/len(N):.1f}%) · S1 {e(A,N)} · action_ok ck500 {e(C,N,'aok')} → TAGE {e(B,N,'aok')}")
    for ten, S_ in (("bộ định vị trúng", [k for k in N if LOC[k]["hit_disk"]]),
                    ("bộ định vị trượt", [k for k in N if not LOC[k]["hit_disk"]])):
        if S_:
            print(f"  {ten:17s} n={len(S_):3d} · ck500 {e(C,S_)} → TAGE {e(B,S_)}"
                  f" · cứu {sum(C[k]['vor']==0 and B[k]['vor']==1 for k in S_)} phá {sum(C[k]['vor']==1 and B[k]['vor']==0 for k in S_)}")
    bins = [(TAU, 1.0), (1.0, 1.5), (1.5, 99)]
    for lo, hi in bins:
        S_ = [k for k in N if lo < M[k]["lp_edit"] - M[k]["lp_draft"] <= hi]
        if S_:
            print(f"  Δlp ({lo:.2f}; {hi:.2f}] n={len(S_):3d} · ck500 {e(C,S_)} → TAGE {e(B,S_)}")
    print("  mở đầu câu sửa:", dict(collections.Counter(GD.mo_dau(B[k]['sent']) for k in N).most_common(5)),
          "· câu nháp:", dict(collections.Counter(GD.mo_dau(C[k]['sent']) for k in N).most_common(5)))
    print(f"  số từ TB nháp {statistics.mean(len(C[k]['sent'].split()) for k in N):.2f} → sửa "
          f"{statistics.mean(len(B[k]['sent'].split()) for k in N):.2f}")
    vd = [k for k in N if C[k]["vor"] != B[k]["vor"]][:12]
    print("  ví dụ (exec nháp→sửa):")
    for k in vd:
        print(f"   {k} {C[k]['vor']}→{B[k]['vor']} loc{'✓' if LOC[k]['hit_disk'] else '✗'}  {C[k]['sent']!r} → {B[k]['sent']!r}"
              f"  | chuẩn {A[k]['gold']!r}")
    out["nhan"] = dict(n=len(N), ck500=e(C, N), tage=e(B, N), s1=e(A, N))

    p = os.path.join(T, "tage_test_doc.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n→", os.path.relpath(p))


if __name__ == "__main__":
    main()
