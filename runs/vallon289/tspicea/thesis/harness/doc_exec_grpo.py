#!/usr/bin/env python3
"""Đọc kết quả `exec` của nhánh GRPO `<point>` — 0 GPU, chạy từ tệp thô.

Thi hành đúng luật đã khoá ở `report/106` (x19e) và (x20): headline là exec Voronoi gated .14
trên n=4.463, phép so chính là GRPO/101 − MIN/101 (60,05), McNemar ghép cặp + KTC bootstrap cụm.
Báo kèm D.3 / D.3∧14% (qua `luat_d3.py`) và phân rã theo nhóm câu đã đổi so với MIN.

    ~/.venvs/thesis/bin/python harness/doc_exec_grpo.py
"""
import json, os, sys, math, random, statistics as st, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)

A_RAW = os.path.join(ROOT, "runs/grpo_point/score_grpo_point_seed101_raw.jsonl")
B_RAW = os.path.join(ROOT, "runs/score_min_desc_seed101_raw.jsonl")
A_PRED = os.path.join(ROOT, "runs/grpo_point/preds_grpo_point_seed101.jsonl")
B_PRED = os.path.join(ROOT, "runs/preds_min_desc_seed101.jsonl")
MOC_MIN, MDE = 60.05, 2.2
kh = lambda r: (str(r["episode_id"]), str(r["step_id"]))


def nap(p):
    return {kh(r): r for r in map(json.loads, open(p, encoding="utf-8"))}


def mcnemar(pairs):
    b = sum(1 for x, y in pairs if x and not y)
    c = sum(1 for x, y in pairs if y and not x)
    if b + c == 0:
        return b, c, float("nan"), 1.0
    chi = (abs(b - c) - 1) ** 2 / (b + c)
    return b, c, chi, math.erfc(math.sqrt(chi / 2))


def boot_cum(rows, lay, key, n=2000, seed=20260906):
    """KTC bootstrap theo CỤM (app, hoặc episode khi thiếu app) — như mde_that.py."""
    cum = collections.defaultdict(list)
    for r in rows:
        cum[r.get("app") or f"ep{r['episode_id']}"].append(r)
    ks, rnd, out = list(cum), random.Random(seed), []
    for _ in range(n):
        mau = [x for k in (rnd.choice(ks) for _ in ks) for x in cum[k]]
        out.append(100 * st.mean(lay(x) for x in mau))
    out.sort()
    return out[int(.025 * n)], out[int(.975 * n)]


def main():
    for p in (A_RAW, B_RAW):
        if not os.path.exists(p):
            sys.exit(f"DỪNG: chưa có {p}")
    A, B = nap(A_RAW), nap(B_RAW)
    chung = sorted(set(A) & set(B))
    print(f"n ghép cặp: {len(chung)} (GRPO {len(A)} · MIN {len(B)})")

    print("\n── headline: exec Voronoi gated .14 ──")
    for ten, R in (("MIN-DESC/101", B), ("GRPO-point/101", A)):
        v = [R[k]["executable"] for k in chung]
        lo, hi = boot_cum([R[k] for k in chung], lambda r: r["executable"], None)
        print(f"  {ten:16s} {100*st.mean(v):6.2f}%  KTC95 [{lo:.2f} · {hi:.2f}]")

    pr = [(bool(B[k]["executable"]), bool(A[k]["executable"])) for k in chung]
    b, c, chi, p = mcnemar(pr)
    d = 100 * (c - b) / len(pr)
    se = 100 * math.sqrt(b + c) / len(pr)
    print(f"\n  Δ = {d:+.2f} pp · b={b} (MIN đúng/GRPO sai) · c={c} · χ²={chi:.2f} · p={p:.3g}")
    print(f"  KTC95 xấp xỉ [{d-1.96*se:+.2f} · {d+1.96*se:+.2f}]")
    verdict = ("TĂNG" if d >= MDE and (d - 1.96 * se) > 0 else
               "ÂM"   if d <= -MDE and (d + 1.96 * se) < 0 else "TRẮNG")
    print(f"  ⇒ theo (x19e): **{verdict}** (MDE {MDE}, một hạt giống)")
    print(f"  ⇒ (x20a) nhánh so sánh: {'CHẠY' if d >= MDE else 'KHÔNG chạy'} · "
          f"(x20c) hạt 202: {'CHẠY' if d >= MDE else 'KHÔNG chạy'}")
    print(f"  ⚠️ dự báo ghi trước ở (x19d) ghi 5: +1,10 pp (dải +0,59 … +1,49)")

    print("\n── thước phụ trên cùng 4.463 bước ──")
    for ten, R in (("MIN-DESC/101", B), ("GRPO-point/101", A)):
        print(f"  {ten:16s} action_ok {100*st.mean(R[k]['action_ok'] for k in chung):5.2f}% · "
              f"toggle_ok {100*st.mean(R[k]['toggle_ok'] for k in chung):5.2f}% · "
              f"hit_disk {100*st.mean(R[k]['hit_disk'] for k in chung):5.2f}%")

    try:
        import luat_d3
        print("\n── luật D.3 của AndroidControl (báo kèm, không phải headline) ──")
        for ten, tep in (("MIN-DESC/101", "score_min_desc_seed101_raw.jsonl"),
                         ("GRPO-point/101", "grpo_point/score_grpo_point_seed101_raw.jsonl")):
            r, n = luat_d3.bang(tep, keys=chung)
            print(f"  {ten:16s} Voronoi {r['vor']:6.2f} · D.3 {r['d3']:6.2f} · "
                  f"D.3∧14% {r['d3_gate']:6.2f} · D.3 bỏ container {r['d3_nocont']:6.2f}  (n={n})")
    except Exception as e:
        print(f"\n⚠️ không tính được bảng D.3: {e}")

    if os.path.exists(A_PRED) and os.path.exists(B_PRED):
        PA, PB = nap(A_PRED), nap(B_PRED)
        doi = {k for k in chung
               if (PA[k].get("pred") or "").strip() != (PB[k].get("pred") or "").strip()}
        print("\n── phân rã theo nhóm (HẬU KIỂM, nhóm định nghĩa bằng hành vi của chính mô hình) ──")
        for ten, tap in (("câu ĐÃ ĐỔI", doi), ("câu GIỮ NGUYÊN", set(chung) - doi)):
            if not tap:
                continue
            t = sorted(tap)
            eb = 100 * st.mean(B[k]["executable"] for k in t)
            ea = 100 * st.mean(A[k]["executable"] for k in t)
            bb, cc, _, pp = mcnemar([(bool(B[k]["executable"]), bool(A[k]["executable"])) for k in t])
            print(f"  {ten:16s} n={len(t):5d} · {eb:6.2f} → {ea:6.2f} ({ea-eb:+5.2f} pp) · "
                  f"b={bb} c={cc} · p={pp:.3g}")


if __name__ == "__main__":
    main()
