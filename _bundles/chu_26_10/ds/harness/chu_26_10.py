# -*- coding: utf-8 -*-
"""Thước chữ (7 thước của bảng nhiều thước) cho các nhánh có kết quả 25–26/10 — 0 GPU, CPU + Java 8.

Cùng hai đường đã sinh số luận văn (giống chu_s202.py): COCO (BLEU-4 · METEOR 1.5 · ROUGE-L · CIDEr-D · SPICE,
PTBTokenizer, mức kho) + text_metrics_them.tinh (chrF · BERTScore roberta-large L17 rescaled, câu rỗng = 0).
S1/101 tính lại trước và phải khớp số đã lưu (±0,025), lệch là dừng.
Ghi runs/text_metrics_26_10.json (ghi sau mỗi nhánh).
"""
import glob, json, os, sys, time
from pathlib import Path

from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.meteor.meteor import Meteor
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.cider.cider import Cider
from pycocoevalcap.spice.spice import Spice

ROOT = Path(__file__).resolve().parent.parent
import text_metrics_them as TM

NHANH = {
    "S1/101": ("score_s1_seed101_raw.jsonl", 4463),
    "xao101": ("score_ck500_xao101_test_raw.jsonl", 4463),
    "Qwen7B": ("score_qwen7b_test_raw.jsonl", 4463),
    "tuantu S1": ("tuantu_s1_rows.jsonl", 4463),
    "tuantu ck500": ("tuantu_ck500_rows.jsonl", 4463),
    "AitZ Base": ("score_base_aitz_raw.jsonl", 2736),
    "AitZ S1": ("score_s1_aitz_raw.jsonl", 2736),
    "AitZ ck500": ("score_ck500_aitz_raw.jsonl", 2736),
    "AitZ ck500/202": ("score_ck500_s202_aitz_raw.jsonl", 2736),
    "AitZ R3": ("score_r3_aitz_raw.jsonl", 2736),
    "AitZ ra_k4": ("score_ra_k4_aitz_raw.jsonl", 2736),
}


def load(f, n):
    rows = [json.loads(l) for l in open(ROOT / "runs" / f, encoding="utf-8")]
    assert len(rows) == n, (f, len(rows))
    return [(r.get("sent") or "").strip() for r in rows], [(r.get("gold_instruction") or "").strip() for r in rows]


def coco(hyp, ref):
    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(ref)})
    c = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(hyp)})
    b, _ = Bleu(4).compute_score(g, c, verbose=0)
    return dict(bleu4=round(100 * b[3], 2), meteor15=round(100 * Meteor().compute_score(g, c)[0], 2),
                rougeL=round(100 * float(Rouge().compute_score(g, c)[0]), 2),
                cider_d=round(100 * float(Cider().compute_score(g, c)[0]), 2),
                spice=round(100 * Spice().compute_score(g, c)[0], 2))


def main():
    ref_coco = json.load(open(ROOT / "runs/text_metrics_coco.json", encoding="utf-8"))["S1/101"]
    ref_them = json.load(open(ROOT / "runs/text_metrics_them.json", encoding="utf-8"))["S1/101"]
    dich = ROOT / "runs/text_metrics_26_10.json"
    out = {}
    for ten, (f, n) in NHANH.items():
        t0 = time.time()
        hyp, ref = load(f, n)
        o = coco(hyp, ref)
        t = TM.tinh(hyp, ref, bert=True)
        for k in ("chrf", "bertscore_f1_rescaled", "bertscore_f1", "bertscore_hash", "n", "n_rong"):
            if k in t:
                o[k] = t[k]
        o["src"] = f
        out[ten] = o
        print(f"{ten:15s} " + " · ".join(f"{k} {v}" for k, v in o.items() if k not in ("src", "bertscore_hash"))
              + f"  ({time.time()-t0:.0f} s)", flush=True)
        if ten == "S1/101":
            loi = [f"{k} {v} ≠ {ref_coco.get(k, ref_them.get(k))}" for k, v in o.items()
                   if isinstance(v, float) and isinstance(ref_coco.get(k, ref_them.get(k)), (int, float))
                   and abs(v - ref_coco.get(k, ref_them.get(k))) > 0.025]
            if loi:
                sys.exit("⛔ DỪNG, S1 không tái lập: " + " · ".join(loi))
            print("✅ S1 tái lập số đã lưu (±0,025)", flush=True)
        json.dump(out, open(dich, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", dich)


if __name__ == "__main__":
    main()
