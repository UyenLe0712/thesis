# -*- coding: utf-8 -*-
"""Gieo tệp thô trước khi chấm (B.10 của 288): câu đã chấm ở nhánh cũ thì chép nguyên bản ghi chấm.

    python gieo_tho.py --preds pred_X.jsonl --tho score_s1_raw.jsonl score_ck500_raw.jsonl --out score_X_raw.jsonl
    python gieo_tho.py --selftest --repo <repo>          # CPU, tệp thật của repo

Bộ trỏ tất định (đo 6/10: 2.795/2.795 câu trùng thì trùng toạ độ) ⇒ score_run.py (chế độ nối tiếp)
chỉ phải chấm câu mới. Tệp đầu trong --tho thắng khi trùng (ep, step, câu).
Viết lại 6/10/2026 từ bản mô tả B.10 (mã gốc ở máy Mac) ⇒ md5 khác bản gốc.
"""
import argparse, json, os, sys, tempfile


def doc(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def gieo_tho(preds, tho, out):
    if os.path.exists(out):
        sys.exit(f"DỪNG: {out} đã tồn tại — không gieo đè")
    P = {(d["episode_id"], d["step_id"]): d.get("pred") for d in doc(preds)}
    kho = {}
    for t in tho:
        for o in doc(t):
            if o.get("sent"):
                kho.setdefault((o["episode_id"], o["step_id"], o["sent"]), o)
    n = 0
    with open(out, "w", encoding="utf-8") as f:
        for (e, s), p in P.items():
            o = kho.get((e, s, p)) if p else None
            if o is not None:
                f.write(json.dumps(o, ensure_ascii=False) + "\n"); n += 1
    print(f"[gieo] {n}/{len(P)} bước chép từ tệp thô cũ · còn phải chấm {len(P) - n} câu → {out}", flush=True)
    return n


def selftest(repo):
    R = lambda *p: os.path.join(repo, "runs", *p)
    TAPT = ("click", "long_press")
    d = tempfile.mkdtemp()
    ok = True

    def kiem(out, goc):
        G = {(o["episode_id"], o["step_id"]): o for o in doc(goc)}
        return all(o == G[(o["episode_id"], o["step_id"])] for o in doc(out))

    n = gieo_tho(R("grpo_spice", "pred_ck500_test.jsonl"), [R("grpo_spice", "score_ck500_test_raw.jsonl")], f"{d}/a.jsonl")
    ok &= n == 4462 and kiem(f"{d}/a.jsonl", R("grpo_spice", "score_ck500_test_raw.jsonl"))
    print("(a) ck500 từ tệp thô ck500:", n, "/4463 · trùng bản gốc", kiem(f"{d}/a.jsonl", R("grpo_spice", "score_ck500_test_raw.jsonl")))

    recs = doc(os.path.join(repo, "harness", "dg1_cache", "test_ac", "test.jsonl"))
    tap = {(r["episode_id"], r["step_id"]) for r in recs if r["action"].get("action_type") in TAPT and "x" in r["action"]}
    with open(f"{d}/s1_tap.jsonl", "w", encoding="utf-8") as f:
        for p in doc(R("preds_s1_seed101.jsonl")):
            if (p["episode_id"], p["step_id"]) in tap:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
    n = gieo_tho(f"{d}/s1_tap.jsonl", [R("score_s1_seed101_raw.jsonl")], f"{d}/b.jsonl")
    ok &= n == 4462 and kiem(f"{d}/b.jsonl", R("score_s1_seed101_raw.jsonl"))
    print("(b) S1 từ tệp thô S1:", n, "/4463 · trùng bản gốc", kiem(f"{d}/b.jsonl", R("score_s1_seed101_raw.jsonl")))

    n = gieo_tho(R("grpo_spice", "pred_ck500_test.jsonl"), [R("score_s1_seed101_raw.jsonl")], f"{d}/c.jsonl")
    ok &= kiem(f"{d}/c.jsonl", R("score_s1_seed101_raw.jsonl"))
    print("(c) ck500 từ tệp thô S1:", n, "câu trùng S1 · trùng bản gốc", kiem(f"{d}/c.jsonl", R("score_s1_seed101_raw.jsonl")))
    print("✅ selftest ĐẠT" if ok else "⛔ selftest RỚT")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preds")
    ap.add_argument("--tho", nargs="+", default=[])
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--repo", default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
    a = ap.parse_args()
    if a.selftest:
        selftest(a.repo)
    else:
        assert a.preds and a.tho and a.out, "cần --preds --tho --out"
        gieo_tho(a.preds, a.tho, a.out)


if __name__ == "__main__":
    main()
