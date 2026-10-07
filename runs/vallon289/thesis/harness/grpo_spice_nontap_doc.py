# -*- coding: utf-8 -*-
"""Đọc bước KHÔNG chạm của GRPO SPICE ck500 so S1/101 (report/261 §5.2, 2/10/2026) — 0 GPU, không bộ trỏ.

    python3 harness/grpo_spice_nontap_doc.py [--preds runs/grpo_spice/pred_ck500_test_nontap.jsonl]

Thước: đúng hàm `score_run.noharm` — `canon_action(câu mô hình) == canon_action(câu chuẩn)` với
`strict_back=True`, câu rỗng tính sai. Ghép cặp theo (episode_id, step_id) trên 2.495 bước, bootstrap
cụm = app bằng `score_run.cluster_bootstrap` (B = 10.000, như mọi KTC của luận văn).

Luật đọc khoá TRƯỚC khi có số (runbook `kaggle_grpo_spice_nontap_ck500.md`):
  · TOÀN BỘ 2.495 bước: cận dưới KTC Δ ≥ −3 điểm ⇒ ĐẠT (luật noharm gốc, `report/106` mục 3).
  · SCROLL (755 bước): Δ điểm ≥ −3 ⇒ ĐẠT (report/261 §5.3); in kèm KTC.
  · Cả hai đạt ⇒ chốt ck500 là mô hình cuối. Một trong hai rớt ⇒ khai là tác hại ở bước không chạm.
Tự kiểm trước: S1 so với chính nó Δ = 0; tệp ck500 đủ 2.495 khoá, không thừa bước chạm.
"""
import argparse, collections, json, os, sys

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import metric_exec as M
from score_run import cluster_bootstrap

ROOT = os.path.dirname(H)
TAPT = ("click", "long_press")


def nap_preds(p):
    return {(d["episode_id"], d["step_id"]): (d.get("pred") or "").strip()
            for d in map(json.loads, open(p, encoding="utf-8"))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preds", default="runs/grpo_spice/pred_ck500_test_nontap.jsonl")
    ap.add_argument("--baseline", default="runs/preds_s1_seed101.jsonl")
    ap.add_argument("--out", default="runs/grpo_spice/nontap_ck500_doc.json")
    a = ap.parse_args()
    recs = [json.loads(l) for l in open(os.path.join(H, "dg1_cache/test_ac/test.jsonl"), encoding="utf-8")]
    nt = [r for r in recs if not (r["action"].get("action_type") in TAPT and "x" in r["action"])]
    assert len(nt) == 2495, len(nt)
    K = [(r["episode_id"], r["step_id"]) for r in nt]
    S, C = nap_preds(os.path.join(ROOT, a.baseline)), nap_preds(os.path.join(ROOT, a.preds))
    thieu = [k for k in K if k not in C]
    thua = set(C) - set(K)
    print(f"[dữ liệu] {a.preds} · {len(C)} câu · thiếu {len(thieu)} bước không chạm · thừa {len(thua)}")
    assert not thieu and not thua, "⛔ tệp ck500 phải đúng 2.495 bước không chạm"
    assert all(k in S for k in K), "⛔ S1 thiếu bước không chạm"

    def ok(s, g):
        return int(bool(s) and M.canon_action(s, strict_back=True) == M.canon_action(g, strict_back=True))

    U = [{"episode_id": r["episode_id"], "app": r.get("app", ""), "typ": r["action"].get("action_type", "?"),
          "s1": ok(S[k], r["gold_instruction"]), "ck": ok(C[k], r["gold_instruction"]),
          "s1_rong": int(not S[k]), "ck_rong": int(not C[k]), "trung": int(S[k] == C[k])}
         for r, k in zip(nt, K)]
    key = lambda u: u["app"] or f"ep{u['episode_id']}"

    d0, _, _, _ = cluster_bootstrap(U, key, lambda u: u["s1"] - u["s1"])
    assert d0 == 0, "⛔ tự kiểm S1−S1 ≠ 0"

    out = {"n": len(U), "theo_loai": {}}
    print(f"\n{'nhóm':14s} {'n':>5s} {'S1':>7s} {'ck500':>7s} {'Δ':>7s}  KTC95 Δ (cụm app)   phá  cứu")
    nhom = [("TOÀN BỘ", U)] + [(t, [u for u in U if u["typ"] == t])
                               for t, _ in collections.Counter(u["typ"] for u in U).most_common()]
    for ten, X in nhom:
        s1 = 100 * sum(u["s1"] for u in X) / len(X)
        ck = 100 * sum(u["ck"] for u in X) / len(X)
        d, (lo, hi), _, _ = cluster_bootstrap(X, key, lambda u: u["ck"] - u["s1"])
        pha = sum(u["s1"] and not u["ck"] for u in X)
        cuu = sum(u["ck"] and not u["s1"] for u in X)
        print(f"{ten:14s} {len(X):5d} {s1:7.2f} {ck:7.2f} {100*d:+7.2f}  [{100*lo:+6.2f}; {100*hi:+6.2f}]   {pha:4d} {cuu:4d}")
        out["theo_loai"][ten] = dict(n=len(X), s1=round(s1, 2), ck500=round(ck, 2), delta=round(100 * d, 2),
                                     lo=round(100 * lo, 2), hi=round(100 * hi, 2), pha=pha, cuu=cuu)
    print(f"\ncâu trùng S1 {sum(u['trung'] for u in U)}/{len(U)} · câu rỗng S1 {sum(u['s1_rong'] for u in U)}"
          f" · ck500 {sum(u['ck_rong'] for u in U)}")

    T, SC = out["theo_loai"]["TOÀN BỘ"], out["theo_loai"].get("scroll")
    dat_tong = T["lo"] >= -3
    dat_scroll = SC is not None and SC["delta"] >= -3
    out.update(dat_tong=dat_tong, dat_scroll=dat_scroll)
    print(f"\n[luật] toàn bộ: cận dưới {T['lo']:+.2f} ≥ −3 ⇒ {'ĐẠT' if dat_tong else 'RỚT'} · "
          f"scroll: Δ {SC['delta']:+.2f} ≥ −3 ⇒ {'ĐẠT' if dat_scroll else 'RỚT'}")
    print("⇒ " + ("chốt ck500 là mô hình cuối (report/261 §5.3)." if dat_tong and dat_scroll else
                  "khai là tác hại ở bước không chạm, kể cả khi thước bước chạm thắng."))
    json.dump(out, open(os.path.join(ROOT, a.out), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", a.out)


if __name__ == "__main__":
    main()
