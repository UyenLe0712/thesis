# -*- coding: utf-8 -*-
"""Đọc kết quả val C1 của CTG-GRPO (276 §8: K1, K2, K3, chọn điểm lưu), 0 GPU. Số val, cấm trích.

Đặt tệp từ Kaggle (runbook kaggle_ctg_val.md) vào runs/ctg/val/:
    pred_<tên>.jsonl · score_<tên>_raw.jsonl   với <tên> kiểu A3_250, A2_250, A3_500 …
và ctg_log của lượt train vào runs/ctg/<nhánh>/ctg_log.jsonl. Rồi:
    ~/.venvs/thesis/bin/python harness/ctg_doc.py
Kiểm đường: S1 phải in 66/75 đúng loại và exec 158/249 (63,45); ck500 63/75.
"""
import json, os, re, sys, glob, random, collections
from pathlib import Path

T = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(T / "harness"))
from metric_exec import canon_action  # noqa: E402

lop = lambda s: canon_action(s, strict_back=True)
WORD = re.compile(r"[A-Za-z0-9'-]+")
CTG_LOP = ("scroll", "type", "navigate_back")
V = T / "runs/ctg/val"

C1 = [json.loads(l) for l in open(T / "runs/c1/c1_mau.jsonl", encoding="utf-8")]
KEYS = [(d["episode_id"], d["step_id"]) for d in C1]
GOLD = {k: d["gold"] for k, d in zip(KEYS, C1)}
NT = [k for k in KEYS if lop(GOLD[k]) in CTG_LOP]
assert len(NT) == 75, len(NT)


def nap_pred(p):
    return {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(p, encoding="utf-8"))}


def nap_exec(p):
    return {(o["episode_id"], o["step_id"]): int(o["executable"]) for o in map(json.loads, open(p, encoding="utf-8"))}


PRED = {"S1": {k: d["greedy"] for k, d in zip(KEYS, C1)}}
EXEC = {"S1": nap_exec(T / "runs/grpo_spice/score_k0_lai_raw.jsonl")}
for t in ("ck250", "ck500"):
    PRED[t] = nap_pred(T / f"runs/grpo_spice/pred_{t}.jsonl")
    EXEC[t] = nap_exec(T / f"runs/grpo_spice/score_{t}_raw.jsonl")
for p in sorted(glob.glob(str(V / "pred_*.jsonl"))):
    t = Path(p).stem[5:]
    PRED[t] = nap_pred(p)
    s = V / f"score_{t}_raw.jsonl"
    if s.exists():
        EXEC[t] = nap_exec(s)
CLICK = sorted(EXEC["S1"])
assert len(CLICK) == 249


def boot(a, b, ks, n=10000):
    """KTC95 của hiệu trung bình (a − b) theo cụm episode."""
    th = collections.defaultdict(list)
    for k in ks:
        th[k[0]].append(a[k] - b[k])
    E = sorted(th)
    rng = random.Random(101)
    ds = []
    for _ in range(n):
        x = [v for e in (rng.choice(E) for _ in E) for v in th[e]]
        ds.append(100 * sum(x) / len(x))
    ds.sort()
    return ds[int(0.025 * n)], ds[int(0.975 * n)]


print(f"{'nhánh':<10}{'đúng loại 75':>14}{'scroll':>8}{'type':>6}{'back':>6}{'exec 249':>10}{'rỗng %':>8}{'số từ':>7}")
DL = {}
for t, P in PRED.items():
    ok = {k: int(bool(P.get(k)) and lop(P[k]) == lop(GOLD[k])) for k in NT}
    DL[t] = ok
    theo = {g: sum(ok[k] for k in NT if lop(GOLD[k]) == g) for g in CTG_LOP}
    n_g = {g: sum(lop(GOLD[k]) == g for k in NT) for g in CTG_LOP}
    ex = EXEC.get(t)
    exs = f"{sum(ex.values())} ({100*sum(ex.values())/len(ex):.2f})" if ex else "-"
    rong = 100 * sum(not P.get(k) for k in KEYS) / len(KEYS)
    tu = sum(len(WORD.findall(P.get(k) or "")) for k in KEYS) / len(KEYS)
    print(f"{t:<10}{sum(ok.values()):>10}/75{theo['scroll']:>5}/{n_g['scroll']}{theo['type']:>3}/{n_g['type']}"
          f"{theo['navigate_back']:>3}/{n_g['navigate_back']}{exs:>14}{rong:>7.2f}{tu:>7.2f}")

tu_s1 = sum(len(WORD.findall(PRED["S1"][k])) for k in KEYS) / len(KEYS)
print("\n=== luật dừng (276 §8) ===")
for buoc in (250, 500, 750, 1000):
    a3, a2 = f"A3_{buoc}", f"A2_{buoc}"
    if a3 not in PRED:
        continue
    P = PRED[a3]
    rong = 100 * sum(not P.get(k) for k in KEYS) / len(KEYS)
    tu = sum(len(WORD.findall(P.get(k) or "")) for k in KEYS) / len(KEYS)
    print(f"[K3 bước {buoc}] rỗng {rong:.2f}% (dừng > 1) · số từ {tu:.2f} vs S1 {tu_s1:.2f}"
          f" lệch {100*(tu/tu_s1-1):+.1f}% (dừng > ±30)")
    if a2 not in PRED:
        print(f"   chưa có {a2}, chưa xét K1/K2")
        continue
    if buoc == 500:
        d = sum(DL[a3].values()) - sum(DL[a2].values())
        print(f"[K1 bước 500] đúng loại không-tap A3 {sum(DL[a3].values())} − A2 {sum(DL[a2].values())} = {d:+d}"
              f" ⇒ {'DỪNG A3' if d <= 0 else 'qua'}")
    if buoc in (250, 500) and a3 in EXEC and a2 in EXEC:
        d = 100 * (sum(EXEC[a3].values()) - sum(EXEC[a2].values())) / 249
        lo, hi = boot(EXEC[a3], EXEC[a2], CLICK)
        print(f"[K2 bước {buoc}] exec A3 − A2 = {d:+.2f} [{lo:+.2f}; {hi:+.2f}] ⇒ {'DỪNG' if d < -2.6 else 'qua'}")

print("\n=== chọn điểm lưu (mặc định 1000, lùi 500 nếu exec@1000 thấp hơn exec@500 quá 2,6) ===")
for arm in ("A3", "A2"):
    a, b = EXEC.get(f"{arm}_1000"), EXEC.get(f"{arm}_500")
    if a and b:
        d = 100 * (sum(a.values()) - sum(b.values())) / 249
        print(f"{arm}: exec@1000 − exec@500 = {d:+.2f} ⇒ chọn checkpoint-{500 if d < -2.6 else 1000}")

print("\n=== so S1 (exec 249 click, KTC cụm episode) ===")
for t in EXEC:
    if t != "S1":
        d = 100 * (sum(EXEC[t].values()) - sum(EXEC["S1"].values())) / 249
        lo, hi = boot(EXEC[t], EXEC["S1"], CLICK)
        print(f"{t:<10} {d:+.2f} [{lo:+.2f}; {hi:+.2f}]")

# ---- λ, ĉ, lực đẩy theo bước ----
for arm in ("A3", "A2", "A4", "A7"):
    p = T / f"runs/ctg/{arm}/ctg_log.jsonl"
    if not p.exists():
        continue
    L = [json.loads(l) for l in open(p, encoding="utf-8")]
    print(f"\n[{arm}] ctg_log {len(L)} nhóm · bước cuối {L[-1]['buoc']}")
    for g in CTG_LOP:
        x = [r for r in L if r.get("lop") == g and "lam" in r]
        if x:
            tran = max((sum(1 for _ in grp) for v, grp in __import__("itertools").groupby(r["lam"] >= 3.0 for r in x) if v),
                       default=0)
            print(f"   {g}: {len(x)} nhóm · λ cuối {x[-1]['lam']:.3f} · ĉ cuối {x[-1]['chat']:.3f} · "
                  f"std>0 {100*sum(r['std_pos'] for r in x)/len(x):.0f}% · chuỗi λ ở trần dài nhất {tran}"
                  f"{' ⛔ K3' if tran > 100 else ''}")
    nt = [r for r in L if r["lop"] in CTG_LOP]
    if nt:
        print(f"   lực đẩy về tap (TB tổng advantage câu tap, nhóm không-tap): trước {sum(r['day_truoc'] for r in nt)/len(nt):+.3f}"
              f" · sau {sum(r.get('day_sau', r['day_truoc']) for r in nt)/len(nt):+.3f}")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 3, figsize=(13, 3.2))
        for g in CTG_LOP:
            x = [r for r in L if r.get("lop") == g and "lam" in r]
            ax[0].plot([r["buoc"] for r in x], [r["lam"] for r in x], label=g)
            ax[1].plot([r["buoc"] for r in x], [r["chat"] for r in x], label=g)
        w = 25
        ys = [r["day_truoc"] for r in nt]
        ax[2].plot([r["buoc"] for r in nt][w - 1:], [sum(ys[i - w + 1:i + 1]) / w for i in range(w - 1, len(ys))])
        for a_, tt in zip(ax, ("λ_k", "ĉ_k", "lực đẩy về tap (TB trượt 25 nhóm)")):
            a_.set_title(tt)
            a_.set_xlabel("bước")
        ax[0].legend()
        fig.tight_layout()
        fig.savefig(T / f"runs/ctg/{arm}/ctg_lambda.png", dpi=120)
        print(f"   hình: runs/ctg/{arm}/ctg_lambda.png")
    except ImportError:
        pass
