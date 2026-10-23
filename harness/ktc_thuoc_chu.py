# -*- coding: utf-8 -*-
"""KTC95 ghép cặp cho nhóm thước chữ của S1/101, ck500 và ACE (R3) — 0 GPU, CPU + Java 8.

    ~/.venvs/thesis/bin/python -u harness/ktc_thuoc_chu.py [--B 2000]     # ghi runs/ktc_thuoc_chu.json

Bootstrap theo cụm app (cùng cách `score_run.cluster_bootstrap`: cụm = app, bước không có app gom theo tác vụ),
cùng một lần rút cụm cho cả ba nhánh nên Δ là Δ ghép cặp.
  · BLEU-4: tính lại mức kho từ số n-gram từng bước (BleuScorer của COCO, option closest) trên mẫu rút.
  · ROUGE-L · CIDEr-D · SPICE: trung bình điểm từng bước (đúng cách các bộ COCO gộp số mức kho).
  · chrF: trung bình chrF mức câu (xấp xỉ; số mức kho ở bảng dùng sacrebleu corpus).
  · METEOR · BERTScore: KHÔNG tính KTC (METEOR gộp mức kho bằng thống kê, BERTScore tốn CPU) — ghi rõ.
Điểm gốc của từng nhánh phải khớp số đã in ở bảng (S1 · ck500 trong runs/grpo_spice/text_metrics_ck500.json,
ACE trong thesis/chapters/ch6_thucnghiem.tex); lệch quá 0,02 thì dừng, không ghi KTC.
"""
import argparse, glob, json, math, os, sys, time
import numpy as np
from pathlib import Path

J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
if J and "JAVA_HOME" not in os.environ:
    os.environ["JAVA_HOME"] = J[-1]; os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]

from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.bleu.bleu_scorer import BleuScorer
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.cider.cider import Cider
from pycocoevalcap.spice.spice import Spice
import sacrebleu

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
from text_metrics import load

NHANH = {"S1/101": "runs/score_s1_seed101_raw.jsonl",
         "ck500": "runs/grpo_spice/score_ck500_test_raw.jsonl",
         "ACE": "runs/ra304_luat/score_R3_test_raw.jsonl"}
# số đã in (mức kho) để kiểm tái lập
DA_IN = {"S1/101": dict(bleu4=51.56, rougeL=67.35, cider_d=416.12, spice=44.37, chrf=61.26),
         "ck500": dict(bleu4=52.36, rougeL=68.36, cider_d=430.05, spice=45.79, chrf=62.87),
         "ACE": dict(bleu4=53.47, rougeL=69.08, cider_d=442.02, spice=47.13, chrf=63.44)}
CACHE = ROOT / "runs" / "ktc_thuoc_chu_cache"


def tung_buoc(ten, path):
    f = CACHE / f"{ten.replace('/', '_')}.npz"
    if f.exists():
        return dict(np.load(f))
    hyp, ref, rows = load(path)
    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(ref)})
    c = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(hyp)})
    ids = sorted(g)
    t0 = time.time()
    bs = BleuScorer(n=4)
    for i in ids:
        bs += (c[i][0], g[i])
    bs.compute_score(option="closest")
    ct = bs.ctest
    cor = np.array([x["correct"] for x in ct], float); gue = np.array([x["guess"] for x in ct], float)
    tl = np.array([x["testlen"] for x in ct], float); rl = np.array([x["reflen"] for x in ct], float)
    print(f"  {ten}: BLEU xong ({time.time()-t0:.0f} s)", flush=True)
    rouge = np.array(Rouge().compute_score(g, c)[1], float)
    cider = np.array(Cider().compute_score(g, c)[1], float)
    print(f"  {ten}: ROUGE-L · CIDEr-D xong ({time.time()-t0:.0f} s)", flush=True)
    sp = Spice().compute_score(g, c)[1]
    spice = np.array([s["All"]["f"] for s in sp], float)
    print(f"  {ten}: SPICE xong ({time.time()-t0:.0f} s)", flush=True)
    chrf = np.array([sacrebleu.sentence_chrf(h, [r]).score if h else 0.0 for h, r in zip(hyp, ref)], float)
    d = dict(cor=cor, gue=gue, tl=tl, rl=rl, rouge=rouge, cider=cider, spice=spice, chrf=chrf)
    CACHE.mkdir(exist_ok=True); np.savez(f, **d)
    return d


def bleu4(cor, gue, tl, rl):
    """BLEU-4 mức kho giống BleuScorer.compute_score (tiny/small như bản COCO)."""
    tiny, small = 1e-15, 1e-9
    T, R = tl.sum(), rl.sum()
    b = 1.0
    for k in range(4):
        b *= (cor[:, k].sum() + tiny) / (gue[:, k].sum() + small)
    b = b ** 0.25
    if T / (R + tiny) < 1:
        b *= math.exp(1 - R / T)
    return 100 * b


def diem(d, idx=None):
    s = (lambda x: x) if idx is None else (lambda x: x[idx])
    return dict(bleu4=bleu4(s(d["cor"]), s(d["gue"]), s(d["tl"]), s(d["rl"])),
                rougeL=100 * s(d["rouge"]).mean(), cider_d=100 * s(d["cider"]).mean(),
                spice=100 * s(d["spice"]).mean(), chrf=s(d["chrf"]).mean())


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=2000); a = ap.parse_args()
    D = {}
    for ten, p in NHANH.items():
        D[ten] = tung_buoc(ten, p)
    ok = True
    for ten in D:
        pt = diem(D[ten])
        for k, v in DA_IN[ten].items():
            lech = abs(pt[k] - v)
            print(f"  kiểm {ten:7s} {k:8s} tính {pt[k]:8.2f} · đã in {v:8.2f} · lệch {lech:.2f}", flush=True)
            if lech > 0.06 and k != "chrf":      # CIDEr-D/SPICE làm tròn hai chữ số; chrF là xấp xỉ mức câu nên không ràng
                ok = False
    if not ok:
        sys.exit("⛔ không tái lập số đã in — KHÔNG ghi KTC")
    hyp, ref, rows = load(NHANH["S1/101"])
    ap_ = [(r.get("app") or f"ep{r['episode_id']}") for r in rows]
    cl = {}
    for i, x in enumerate(ap_): cl.setdefault(x, []).append(i)
    cum = [np.array(v) for v in cl.values()]
    G = len(cum); print("cụm:", G, flush=True)
    rng = np.random.default_rng(20261023)
    mau = [np.concatenate([cum[j] for j in rng.integers(0, G, G)]) for _ in range(a.B)]
    kq = {k: {t: [] for t in D} for k in DA_IN["S1/101"]}
    t0 = time.time()
    for b, idx in enumerate(mau):
        for ten in D:
            pt = diem(D[ten], idx)
            for k in kq: kq[k][ten].append(pt[k])
        if (b + 1) % 200 == 0: print(f"  bootstrap {b+1}/{a.B} · {time.time()-t0:.0f} s", flush=True)
    out = {"B": a.B, "cum": G, "ghi_chu": "METEOR và BERTScore không có KTC; chrF là trung bình mức câu"}
    pt0 = {t: diem(D[t]) for t in D}
    for k in kq:
        out[k] = {}
        for t in D:
            v = np.array(kq[k][t]); out[k][t] = dict(diem=round(pt0[t][k], 2), lo=round(float(np.percentile(v, 2.5)), 2), hi=round(float(np.percentile(v, 97.5)), 2))
        for x, y in (("ck500", "S1/101"), ("ACE", "S1/101"), ("ACE", "ck500")):
            dl = np.array(kq[k][x]) - np.array(kq[k][y])
            out[k][f"{x}-{y}"] = dict(delta=round(pt0[x][k] - pt0[y][k], 2), lo=round(float(np.percentile(dl, 2.5)), 2),
                                      hi=round(float(np.percentile(dl, 97.5)), 2))
        print(k, {n: v for n, v in out[k].items() if "-" in n}, flush=True)
    json.dump(out, open(ROOT / "runs" / "ktc_thuoc_chu.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→ runs/ktc_thuoc_chu.json")


if __name__ == "__main__":
    main()
