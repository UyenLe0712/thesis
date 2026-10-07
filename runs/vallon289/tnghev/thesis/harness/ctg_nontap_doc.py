# -*- coding: utf-8 -*-
"""Đọc bước KHÔNG chạm trên TEST của CTG-GRPO A3/A2 (report/279 §6, 5/10/2026) — 0 GPU, không bộ trỏ.

    ~/.venvs/thesis/bin/python harness/ctg_nontap_doc.py            # đọc runs/ctg/test_nontap/
    ~/.venvs/thesis/bin/python harness/ctg_nontap_doc.py --kho       # chạy khô: câu S1 làm giả A3, ck500 làm giả A2

Thước: đúng `score_run.noharm` (như `grpo_spice_nontap_doc.py`): `canon_action(câu) == canon_action(câu chuẩn)`
với `strict_back=True`, câu rỗng tính sai. Ghép cặp theo (episode_id, step_id) trên 2.495 bước, KTC bootstrap
cụm = app bằng `score_run.cluster_bootstrap` (B = 10.000).

So bốn cặp: A3 − A2 (phần của riêng CTG, cùng đường sinh, sạch) · A3 − S1 · A2 − S1 · A3 − ck500.
⚠️ S1 sinh bằng `infer_branch` (LoRA chưa hoà), A3/A2/ck500 sinh trên S1 đã hoà fp16 ⇒ các cặp so S1 lẫn biến
đường sinh (như report/259 §5.1); cặp A3 − A2 và A3 − ck500 thì không.

Luật đọc (279 §6, ghi trước khi có số):
  · R-CTG    : scroll, cận dưới KTC của Δ(A3 − A2) > 0.
  · R-noharm : scroll, Δ(A3 − S1) ≥ −3 điểm; toàn bộ 2.495 bước, cận dưới KTC Δ(A3 − S1) ≥ −3.
"""
import argparse, collections, json, os, re, sys

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import metric_exec as M
from score_run import cluster_bootstrap

ROOT = os.path.dirname(H)
TAPT = ("click", "long_press")
D = os.path.join(ROOT, "runs/ctg/test_nontap")


def nap(p):
    return {(d["episode_id"], d["step_id"]): (d.get("pred") or "").strip()
            for d in map(json.loads, open(p, encoding="utf-8"))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kho", action="store_true")
    a = ap.parse_args()
    recs = [json.loads(l) for l in open(os.path.join(H, "dg1_cache/test_ac/test.jsonl"), encoding="utf-8")]
    nt = [r for r in recs if not (r["action"].get("action_type") in TAPT and "x" in r["action"])]
    assert len(nt) == 2495, len(nt)
    K = [(r["episode_id"], r["step_id"]) for r in nt]

    P = {"S1": nap(os.path.join(ROOT, "runs/preds_s1_seed101.jsonl")),
         "ck500": nap(os.path.join(ROOT, "runs/grpo_spice/pred_ck500_test_nontap.jsonl"))}
    if a.kho:
        P["A3"], P["A2"] = {k: P["S1"][k] for k in K}, dict(P["ck500"])
        print("⚠️ CHẠY KHÔ: A3 = câu S1, A2 = câu ck500 — số dưới đây không phải kết quả")
    else:
        for arm in ("A3", "A2"):
            P[arm] = nap(os.path.join(D, f"pred_{arm}_1000_test_nontap.jsonl"))
    for t in ("ck500", "A3", "A2"):
        thieu, thua = [k for k in K if k not in P[t]], set(P[t]) - set(K)
        print(f"[dữ liệu] {t}: {len(P[t])} câu · thiếu {len(thieu)} · thừa {len(thua)}")
        assert not thieu and not thua, f"⛔ {t} phải đúng 2.495 bước không chạm"
    assert all(k in P["S1"] for k in K), "⛔ S1 thiếu bước không chạm"

    lop = lambda s: M.canon_action(s, strict_back=True)
    OK = {t: {k: int(bool(P[t][k]) and lop(P[t][k]) == lop(r["gold_instruction"])) for r, k in zip(nt, K)} for t in P}
    U = [{"k": k, "app": r.get("app", ""), "ep": r["episode_id"], "typ": r["action"].get("action_type", "?")}
         for r, k in zip(nt, K)]
    key = lambda u: u["app"] or f"ep{u['ep']}"
    d0, _, _, _ = cluster_bootstrap(U, key, lambda u: OK["S1"][u["k"]] - OK["S1"][u["k"]])
    assert d0 == 0, "⛔ tự kiểm S1 − S1 ≠ 0"

    nhom = [("TOÀN BỘ", U)] + [(t, [u for u in U if u["typ"] == t])
                               for t, _ in collections.Counter(u["typ"] for u in U).most_common() if t != "navigate_home"]
    out = {"n": len(U), "muc": {}, "cap": {}}

    print(f"\n{'nhóm':14s} {'n':>5s}" + "".join(f"{t:>8s}" for t in ("S1", "ck500", "A2", "A3")))
    for ten, X in nhom:
        v = {t: 100 * sum(OK[t][u["k"]] for u in X) / len(X) for t in ("S1", "ck500", "A2", "A3")}
        out["muc"][ten] = dict(n=len(X), **{t: round(x, 2) for t, x in v.items()})
        print(f"{ten:14s} {len(X):5d}" + "".join(f"{v[t]:8.2f}" for t in ("S1", "ck500", "A2", "A3")))

    for a_, b_ in (("A3", "A2"), ("A3", "S1"), ("A2", "S1"), ("A3", "ck500"), ("A2", "ck500")):
        print(f"\n=== {a_} − {b_} ===\n{'nhóm':14s} {'Δ':>7s}  KTC95 (cụm app)      phá  cứu")
        out["cap"][f"{a_}-{b_}"] = {}
        for ten, X in nhom:
            d, (lo, hi), _, _ = cluster_bootstrap(X, key, lambda u: OK[a_][u["k"]] - OK[b_][u["k"]])
            pha = sum(OK[b_][u["k"]] and not OK[a_][u["k"]] for u in X)
            cuu = sum(OK[a_][u["k"]] and not OK[b_][u["k"]] for u in X)
            print(f"{ten:14s} {100*d:+7.2f}  [{100*lo:+6.2f}; {100*hi:+6.2f}]   {pha:4d} {cuu:4d}")
            out["cap"][f"{a_}-{b_}"][ten] = dict(delta=round(100 * d, 2), lo=round(100 * lo, 2), hi=round(100 * hi, 2),
                                                  pha=pha, cuu=cuu)

    # câu sai loại: thành loại gì; và lối "Search for X" (quy về tap) đã thấy trên val
    print("\n=== câu sai loại: (loại vàng → loại câu), 6 dạng nhiều nhất ===")
    for t in ("S1", "ck500", "A2", "A3"):
        cf = collections.Counter((lop(r["gold_instruction"]), lop(P[t][k]))
                                 for r, k in zip(nt, K) if not OK[t][k])
        print(f"{t:6s}", ", ".join(f"{g}→{p} {n}" for (g, p), n in cf.most_common(6)))
    sf = re.compile(r"^\s*search for\b", re.I)
    print("\ncâu mở đầu 'Search for' (bước input_text): " + " · ".join(
        f"{t} {sum(bool(sf.match(P[t][u['k']])) for u in U if u['typ'] == 'input_text')}" for t in ("S1", "ck500", "A2", "A3")))
    print("câu trùng S1: " + " · ".join(f"{t} {sum(P[t][k] == P['S1'][k] for k in K)}" for t in ("ck500", "A2", "A3"))
          + f" · A3 trùng A2 {sum(P['A3'][k] == P['A2'][k] for k in K)} /2495"
          + " · rỗng: " + " · ".join(f"{t} {sum(not P[t][k] for k in K)}" for t in ("A2", "A3")))

    c = out["cap"]
    r_ctg = c["A3-A2"]["scroll"]["lo"] > 0
    r_nh_sc = c["A3-S1"]["scroll"]["delta"] >= -3
    r_nh_all = c["A3-S1"]["TOÀN BỘ"]["lo"] >= -3
    out["luat"] = dict(R_CTG=r_ctg, R_noharm_scroll=r_nh_sc, R_noharm_toanbo=r_nh_all)
    print(f"\n[luật] R-CTG scroll A3 − A2 cận dưới {c['A3-A2']['scroll']['lo']:+.2f} > 0 ⇒ {'ĐẠT' if r_ctg else 'KHÔNG ĐẠT'}")
    print(f"[luật] R-noharm scroll A3 − S1 {c['A3-S1']['scroll']['delta']:+.2f} ≥ −3 ⇒ {'ĐẠT' if r_nh_sc else 'KHÔNG ĐẠT'}"
          f" · toàn bộ cận dưới {c['A3-S1']['TOÀN BỘ']['lo']:+.2f} ≥ −3 ⇒ {'ĐẠT' if r_nh_all else 'KHÔNG ĐẠT'}")
    if not a.kho:
        p = os.path.join(D, "ctg_nontap_doc.json")
        json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("→", os.path.relpath(p, ROOT))


if __name__ == "__main__":
    main()
