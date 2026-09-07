"""Thước tham chiếu (BLEU-4, ROUGE-L) cho mọi nhánh, tính từ tệp *_raw.jsonl — 0 giây GPU.

Bảng 6.1 luận văn in BLEU-4 / ROUGE-L cho Base (9,7 / 40,3), S1/101 (38,7 / 67,3) và câu
chuẩn (96,1 / 100,0). Script gốc không còn; file này tái lập ba cặp số đó trước rồi mới
điền cho các nhánh còn thiếu. Cách tính (khớp ba cặp số gốc, xem `--variants`):
  · BLEU-4 = trung bình BLEU mức câu (nltk, không làm mượt, token = \w+ thường hoá) × 100; câu chuẩn ngắn hơn bốn
    token cho 0 điểm — đúng con số 176/4.463 mà ch5 nêu.
  · ROUGE-L = trung bình F1 của rouge_score, không stem.
Chạy: ~/.venvs/thesis/bin/python harness/text_metrics.py [--variants]
"""
import argparse, json, statistics, sys, warnings
from pathlib import Path

warnings.filterwarnings("ignore")
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu, SmoothingFunction
from rouge_score import rouge_scorer
import sacrebleu

ROOT = Path(__file__).resolve().parent.parent
BRANCHES = [
    ("Base", "runs/score_base_raw.jsonl"),
    ("S1/101", "runs/score_s1_seed101_raw.jsonl"),
    ("S1/202", "runs/score_s1_seed202_raw.jsonl"),
    ("S2/101", "runs/score_s2_seed101_raw.jsonl"),
    ("CE2-S2/101", "runs/score_ce2_s2_seed101_raw.jsonl"),
    ("MIN-DESC/101", "runs/score_min_desc_seed101_raw.jsonl"),
    ("gui_sel/101", "runs/sel/score_gui_sel_seed101_raw.jsonl"),
    ("GRPO-point/101", "runs/grpo_point/score_grpo_point_seed101_raw.jsonl"),
    ("Câu chuẩn", "runs/score_ceiling_human_raw.jsonl"),
]


def load(path):
    rows = [json.loads(l) for l in open(ROOT / path, encoding="utf-8")]
    assert len(rows) == 4463, (path, len(rows))
    hyp = [(r.get("sent") or "").strip() for r in rows]
    ref = [(r.get("gold_instruction") or "").strip() for r in rows]
    return hyp, ref, rows


import re


def tok(s):
    # chỉ giữ chuỗi chữ-số, bỏ dấu câu, thường hoá — cách duy nhất tái lập đúng 38,7 / 96,1 và 176 câu ngắn
    return re.findall(r"\w+", s.lower())


def metrics(hyp, ref, variant="main"):
    if variant == "main":
        b = [sentence_bleu([tok(r)], tok(h)) if tok(h) else 0.0 for h, r in zip(hyp, ref)]
        sc = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)
        rl = [sc.score(r, h)["rougeL"].fmeasure for h, r in zip(hyp, ref)]
        return 100 * statistics.mean(b), 100 * statistics.mean(rl)
    if variant == "corpus_nltk":
        return 100 * corpus_bleu([[tok(r)] for r in ref], [tok(h) for h in hyp]), float("nan")
    if variant == "sacrebleu":
        return sacrebleu.corpus_bleu(hyp, [ref]).score, float("nan")
    if variant == "smooth1":
        sm = SmoothingFunction().method1
        b = [sentence_bleu([tok(r)], tok(h), smoothing_function=sm) if tok(h) else 0.0 for h, r in zip(hyp, ref)]
        return 100 * statistics.mean(b), float("nan")
    if variant == "rouge_stem":
        sc = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
        rl = [sc.score(r, h)["rougeL"].fmeasure for h, r in zip(hyp, ref)]
        return float("nan"), 100 * statistics.mean(rl)
    raise ValueError(variant)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variants", action="store_true", help="in thêm các cách tính khác trên ba nhánh gốc")
    ap.add_argument("--out", default="runs/text_metrics.json")
    a = ap.parse_args()

    if a.variants:
        for name, path in [BRANCHES[0], BRANCHES[1], BRANCHES[-1]]:
            hyp, ref, _ = load(path)
            for v in ["main", "corpus_nltk", "sacrebleu", "smooth1", "rouge_stem"]:
                b, r = metrics(hyp, ref, v)
                print(f"{name:14s} {v:12s} BLEU-4 {b:6.2f}  ROUGE-L {r:6.2f}")
        return

    out = {}
    print(f"{'nhánh':14s} {'BLEU-4':>7s} {'ROUGE-L':>8s} {'action_ok':>10s} {'exec':>6s}  n<4tok")
    for name, path in BRANCHES:
        if not (ROOT / path).exists():
            print(f"{name:14s}   ⛔ chưa có {path} — bỏ qua")
            continue
        hyp, ref, rows = load(path)
        b, r = metrics(hyp, ref)
        ao = 100 * statistics.mean(x.get("action_ok", 0) for x in rows)
        ex = 100 * statistics.mean(x.get("executable", 0) for x in rows)
        short = sum(1 for h in hyp if len(tok(h)) < 4)
        out[name] = {"bleu4": round(b, 2), "rougeL": round(r, 2), "action_ok": round(ao, 2), "exec": round(ex, 2), "n_short": short, "src": path}
        print(f"{name:14s} {b:7.2f} {r:8.2f} {ao:10.2f} {ex:6.2f}  {short}")
    json.dump(out, open(ROOT / a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ghi", a.out)


if __name__ == "__main__":
    main()
