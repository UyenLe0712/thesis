# -*- coding: utf-8 -*-
"""Cột chữ của bảng nhiều thước cho GRPO SPICE ck500 (action 261, 2/10/2026) — 0 GPU, CPU + Java 8.

    ~/.venvs/thesis/bin/python harness/ck500_text_metrics.py [--bo-bert]

Tính S1/101 và ck500 bằng ĐÚNG hai đường đã sinh số luận văn:
  · `text_metrics_coco.py`  → BLEU-4 · METEOR 1.5 · ROUGE-L · CIDEr-D · SPICE (PTBTokenizer, mức kho)
  · `text_metrics_them.tinh` → chrF (sacrebleu) · BERTScore roberta-large L17 rescaled (câu rỗng = 0)
S1 phải tái lập số đã lưu ở `runs/text_metrics_coco.json` · `runs/text_metrics_them.json`
(lệch > 0,02 là dừng, không ghi ck500). Ghi `runs/grpo_spice/text_metrics_ck500.json`.
"""
import argparse, glob, json, os, sys, time
from pathlib import Path

J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
if J and "JAVA_HOME" not in os.environ:
    os.environ["JAVA_HOME"] = J[-1]
    os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]

from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.meteor.meteor import Meteor
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.cider.cider import Cider
from pycocoevalcap.spice.spice import Spice

ROOT = Path(__file__).resolve().parent.parent
from text_metrics import load
import text_metrics_them as TM

NHANH = {"S1/101": "runs/score_s1_seed101_raw.jsonl", "ck500": "runs/grpo_spice/score_ck500_test_raw.jsonl"}


def coco(hyp, ref):
    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(ref)})
    c = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(hyp)})
    b, _ = Bleu(4).compute_score(g, c, verbose=0)
    return dict(bleu4=round(100 * b[3], 2), meteor15=round(100 * Meteor().compute_score(g, c)[0], 2),
                rougeL=round(100 * Rouge().compute_score(g, c)[0], 2),
                cider_d=round(100 * Cider().compute_score(g, c)[0], 2),
                spice=round(100 * Spice().compute_score(g, c)[0], 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bo-bert", action="store_true")
    a = ap.parse_args()
    ref_coco = json.load(open(ROOT / "runs/text_metrics_coco.json", encoding="utf-8"))["S1/101"]
    ref_them = json.load(open(ROOT / "runs/text_metrics_them.json", encoding="utf-8"))["S1/101"]
    out, loi = {}, []
    for ten, path in NHANH.items():
        t0 = time.time()
        hyp, ref, rows = load(path)
        o = coco(hyp, ref)
        t = TM.tinh(hyp, ref, bert=not a.bo_bert)
        o["chrf"] = t["chrf"]
        for k in ("bertscore_f1_rescaled", "bertscore_f1", "bertscore_hash"):
            if k in t:
                o[k] = t[k]
        o.update(n=t["n"], n_rong=t["n_rong"],
                 rong=[(r["episode_id"], r["step_id"]) for r, h in zip(rows, hyp) if not h], src=path)
        out[ten] = o
        print(f"{ten:7s} " + " · ".join(f"{k} {v}" for k, v in o.items() if k not in ("src", "bertscore_hash"))
              + f"  ({time.time()-t0:.0f} s)", flush=True)
        if ten == "S1/101":
            for k, v in o.items():
                r = ref_coco.get(k, ref_them.get(k))
                if isinstance(r, (int, float)) and isinstance(v, (int, float)) and k not in ("n", "n_rong") \
                        and abs(v - r) > 0.025:
                    loi.append(f"S1 {k} {v} ≠ đã lưu {r}")
            if "bertscore_hash" in o and o["bertscore_hash"] != ref_them["bertscore_hash"]:
                print(f"  ⚠️ hash khác: {o['bertscore_hash']} vs {ref_them['bertscore_hash']}", flush=True)
            if loi:
                sys.exit("⛔ DỪNG, không tái lập S1 — KHÔNG tính ck500: " + " · ".join(loi))
            print("✅ S1 tái lập số đã lưu (±0,02)", flush=True)
    out["delta"] = {k: round(out["ck500"][k] - out["S1/101"][k], 2) for k in out["ck500"]
                    if isinstance(out["ck500"][k], float)}
    p = ROOT / "runs/grpo_spice/text_metrics_ck500.json"
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Δ", out["delta"], "\n→", p.relative_to(ROOT))


if __name__ == "__main__":
    main()
