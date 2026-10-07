# -*- coding: utf-8 -*-
"""Quét ngưỡng τ trên lát dev 1.400 — thi hành thủ tục đã đăng ký ở `report/106` (x16d) và
hai nhánh phụ đăng ký ở (x17f).

    python3 harness/quet_tau.py runs/sel/seqscores_gui_sel_seed101_dev1400_gpu0.jsonl \
                                runs/sel/seqscores_gui_sel_seed101_dev1400_gpu1.jsonl

Đầu vào: tệp do `seq_score_sel.py` sinh (mỗi dòng: `s_none`, `tok_none`, `s_star`, `margin`,
`scores` = điểm/token + số token của MỌI ứng viên, `gold_in_menu`, `gold_cand`). Luật null
(greedy hiện tại) đọc từ thẻ `<sel>` trong `raw` của `preds_gui_sel_seed101_dev1400.jsonl`.

Bốn nhánh luật, cùng tiêu chí (x16d): cực đại ĐỘ ĐÚNG TRÊN TOÀN BỘ 1.400 (đúng ứng viên khi có
vàng, đúng none khi không có vàng); hoà ⇒ ít none-sai hơn; luật null trong lưới; in trọn đường
cong kể cả khi null thắng.
  X  (x16d) CHÍNH   : c* = argmax điểm/token; phát c* nếu m = s(c*) − s(none) > τ
  A  (x17f) lai     : greedy chọn ⇒ giữ; greedy none ⇒ c* của X nếu m > τ
  B  (x17f) tổng    : c* = argmax TỔNG logprob (điểm/token × số token); phát c* nếu
                      m_sum = logp(c*) − logp(none) > τ
  C  (x17f) lai-tổng: greedy chọn ⇒ giữ; greedy none ⇒ c* của B nếu m_sum > τ
Luật quyết lượt ② (x17b + x17f): X cần lift ≥ 18/1.400; A/B/C cần lift ≥ 24/1.400 (bù cho việc
chọn trong ba nhánh phụ). Không nới sau khi thấy số.
Thước "đúng ứng viên" import từ `gate_sel_acc.py` (chuan + TOL), không viết bản thứ hai.

⛔ Tệp này KHÔNG đọc `exec`, KHÔNG đọc 3.062.
⚠️ KTC của lift là bootstrap ghép cặp tại τ* đã chọn (không refit) ⇒ hơi lạc quan.
"""
import os, sys, json, math, glob, random, argparse, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gate_sel_acc as G                # chuan(), tach_sel(), TOL, kh()

TAU0_SUM = -math.log(0.5478 / 0.291)     # −0,633: hiệu chỉnh logit theo tiên nghiệm, áp lên m_sum
NGUONG = {"X": 18, "A": 24, "B": 24, "C": 24}


def eq(c, g):
    return bool(c) and G.chuan(c["name"]) == G.chuan(g["name"]) \
        and abs(c["x"] - g["x"]) <= G.TOL and abs(c["y"] - g["y"]) <= G.TOL


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scores", nargs="+")
    ap.add_argument("--preds", default=os.path.join(HERE, "..", "runs", "sel",
                                                     "preds_gui_sel_seed101_dev1400.jsonl"))
    ap.add_argument("--out", default=os.path.join(HERE, "..", "runs", "sel", "tau_scan.json"))
    ap.add_argument("--n-boot", type=int, default=2000)
    a = ap.parse_args()

    R, runs = {}, set()
    for pat in a.scores:
        for p in sorted(glob.glob(pat)):
            for l in open(p, encoding="utf-8"):
                try:
                    r = json.loads(l)
                except Exception:
                    continue
                R[(str(r["episode_id"]), str(r["step_id"]))] = r
                runs.add(r.get("run"))
    assert len(runs) == 1, f"DỪNG: nhiều chữ ký lượt chạy: {runs}"
    print(f"điểm: {len(R)} bước · chữ ký {runs.pop()!r}")
    if len(R) < 1400:
        print(f"⚠️ chưa đủ 1.400 bước ({len(R)}) — kết quả CHƯA phải bản khoá")

    P = {G.kh(r): r for r in map(json.loads, open(a.preds, encoding="utf-8"))}
    K = sorted(k for k in R if k in P)
    assert len(K) == len(R), f"DỪNG: {len(R)-len(K)} bước có điểm nhưng không có pred greedy"
    n = len(K); n_has = sum(R[k]["gold_in_menu"] for k in K)

    greedy = {}
    for k in K:
        t, x, y = G.tach_sel(P[k].get("raw") or "")
        greedy[k] = None if t in (None, "none") else {"name": t, "x": x or -9999, "y": y or -9999}

    def dung(k, c):
        r = R[k]
        return eq(c, r["gold_cand"]) if r["gold_in_menu"] else (c is None)

    # c* và margin theo hai cách xếp hạng
    def star_norm(k):
        r = R[k]; return r["cand_star"], r["margin"]
    def star_sum(k):
        sc = R[k]["scores"]
        if not sc: return None, None
        c = max(sc, key=lambda s: s["s"] * s["tok"])
        return c, c["s"] * c["tok"] - R[k]["s_none"] * R[k]["tok_none"]
    STAR = {k: {"norm": star_norm(k), "sum": star_sum(k)} for k in K}

    def chon(nhanh, k, tau):
        if nhanh in ("A", "C") and greedy[k] is not None:
            return greedy[k]
        c, m = STAR[k]["norm" if nhanh in ("X", "A") else "sum"]
        return c if (m is not None and m > tau) else None

    def danh_gia(nhanh, tau):
        ok = none_sai = chon_sai = phat_none = sel_dung = 0
        for k in K:
            c = chon(nhanh, k, tau); d = dung(k, c); ok += d
            if c is None:
                phat_none += 1; none_sai += R[k]["gold_in_menu"]
            else:
                chon_sai += (not d); sel_dung += (R[k]["gold_in_menu"] and d)
        return dict(tau=tau, dung=ok, acc=ok / n, none_sai=none_sai, chon_sai=chon_sai,
                    ti_le_none=phat_none / n, sel_acc=(sel_dung / n_has if n_has else None))

    ok_null = {k: dung(k, greedy[k]) for k in K}
    null_dung = sum(ok_null.values())
    null = dict(tau="greedy", dung=null_dung, acc=null_dung / n,
                none_sai=sum(1 for k in K if greedy[k] is None and R[k]["gold_in_menu"]),
                ti_le_none=sum(1 for k in K if greedy[k] is None) / n,
                sel_acc=(sum(1 for k in K if R[k]["gold_in_menu"] and ok_null[k]) / n_has
                         if n_has else None))
    print(f"\nn = {n} · có ứng viên vàng {n_has} ({100*n_has/n:.1f}%)")
    print(f"NULL greedy: đúng {null_dung}/{n} = {100*null['acc']:.2f}% · none-sai {null['none_sai']} "
          f"· %none {100*null['ti_le_none']:.1f} · sel_acc(HasAns) {100*null['sel_acc']:.2f}%")

    rng = random.Random(20260805)
    KQ = {}
    for nhanh, ten in [("X", "(x16d) chính — chuẩn hoá/token"), ("A", "lai, chuẩn hoá"),
                       ("B", "tổng logprob"), ("C", "lai, tổng logprob")]:
        loai = "norm" if nhanh in ("X", "A") else "sum"
        ms = sorted(set(STAR[k][loai][1] for k in K if STAR[k][loai][1] is not None))
        grid = [-math.inf] + [(ms[i] + ms[i+1]) / 2 for i in range(len(ms) - 1)] + [math.inf]
        duong = [danh_gia(nhanh, t) for t in grid]
        best = max(duong, key=lambda d: (d["dung"], -d["none_sai"]))
        lift = best["dung"] - null_dung
        ok_b = {k: dung(k, chon(nhanh, k, best["tau"])) for k in K}
        diff = [int(ok_b[k]) - int(ok_null[k]) for k in K]
        bs = sorted(sum(diff[rng.randrange(n)] for _ in range(n)) for _ in range(a.n_boot))
        ci = (bs[int(0.025 * a.n_boot)], bs[int(0.975 * a.n_boot)])
        print(f"\n━━ nhánh {nhanh}: {ten} ━━")
        print(f"τ* = {best['tau']:+.4f}: đúng {best['dung']}/{n} = {100*best['acc']:.2f}% · none-sai "
              f"{best['none_sai']} · chọn-sai {best['chon_sai']} · %none {100*best['ti_le_none']:.1f} "
              f"· sel_acc(HasAns) {100*best['sel_acc']:.2f}%")
        print(f"LIFT = {lift:+d} bước ({100*lift/n:+.2f} pp) · KTC95 [{ci[0]:+d} · {ci[1]:+d}] "
              f"· ngưỡng {NGUONG[nhanh]} ⇒ {'ĐẠT' if lift >= NGUONG[nhanh] else 'không đạt'}")
        if loai == "sum":
            d0 = danh_gia(nhanh, TAU0_SUM)
            print(f"  tham chiếu τ₀ = {TAU0_SUM:+.3f} (tiên nghiệm): đúng {d0['dung']} "
                  f"({100*d0['acc']:.2f}%) · none-sai {d0['none_sai']} · %none {100*d0['ti_le_none']:.1f}")
        buoc = max(1, len(duong) // 25)
        print(f"  {'τ':>9s} {'đúng':>5s} {'acc%':>6s} {'none-sai':>8s} {'chọn-sai':>8s} {'%none':>6s}")
        for d in duong[::buoc]:
            t = d["tau"]; ts = f"{t:+.3f}" if math.isfinite(t) else str(t)
            print(f"  {ts:>9s} {d['dung']:5d} {100*d['acc']:6.2f} {d['none_sai']:8d} {d['chon_sai']:8d} {100*d['ti_le_none']:6.1f}")
        KQ[nhanh] = dict(ten=ten, best=best, lift=lift, lift_ci95=ci, dat=lift >= NGUONG[nhanh],
                         duong=[{kk: (v if not isinstance(v, float) or math.isfinite(v) else str(v))
                                 for kk, v in d.items()} for d in duong])

    dat = [nh for nh in KQ if KQ[nh]["dat"]]
    if dat:
        nh = max(dat, key=lambda z: KQ[z]["lift"])
        quyet = (f"ĐẠT ở nhánh {nh} (lift {KQ[nh]['lift']:+d}, τ* = {KQ[nh]['best']['tau']:+.4f}) "
                 f"⇒ theo (x17b): CHẠY lượt ② gui_sel_cham/101")
    else:
        quyet = "KHÔNG nhánh nào đạt ngưỡng ⇒ KHOÁ LUẬT NULL; theo (x17b): KHÔNG chạy lượt ②"
    print(f"\n⭐ {quyet}")
    print("   τ khoá TRƯỚC khi nhìn exec đối chứng / 3.062 (x16d). Nhãn: thăm dò.")

    out = dict(luc=time.strftime("%Y-%m-%d %H:%M:%S"), n=n, n_has=n_has, null=null, nhanh=KQ,
               nguong=NGUONG, tau0_sum=TAU0_SUM, quyet=quyet)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", a.out)


if __name__ == "__main__":
    main()
