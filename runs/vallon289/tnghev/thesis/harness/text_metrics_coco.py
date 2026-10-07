# -*- coding: utf-8 -*-
"""Bộ chấm COCO-caption chính thức (pycocoevalcap) cho mọi nhánh — 0 giây GPU, chạy CPU + Java 8.

Đúng quy trình mà Widget Captioning (EMNLP 2020) và Screen2Words (UIST 2021) dùng, và Zhao et al.
(EACL 2021) chạy cho chỉ dẫn điều hướng: tách từ PTBTokenizer (Stanford CoreNLP) rồi
BLEU-1..4 · METEOR 1.5 · ROUGE-L · CIDEr-D · SPICE, tất cả tính mức KHO.
⚠️ Một câu tham chiếu mỗi bước (AndroidControl chỉ có một) ⇒ CIDEr-D đọc thận trọng.
⚠️ Zhao 2021: SPICE chỉ đọc ở mức HỆ THỐNG, không phân tích theo từng câu.

Cần Java 8:  export JAVA_HOME=~/.jdk/jdk8u504-b01 (script tự đặt nếu thấy thư mục đó).
Chạy:  ~/.venvs/thesis/bin/python harness/text_metrics_coco.py [--limit N] [--bo-spice]
Ghi:   runs/text_metrics_coco.json
"""
import argparse, glob, json, os, time
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
from text_metrics import BRANCHES, load


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--bo-spice", action="store_true")
    ap.add_argument("--out", default="runs/text_metrics_coco.json")
    a = ap.parse_args()
    dich = ROOT / a.out
    out = {} if a.limit or not dich.exists() else json.load(open(dich, encoding="utf-8"))
    for name, path in BRANCHES:
        if name in out:
            print(f"{name:14s} đã có trong {a.out}, bỏ qua", flush=True)
            continue
        if not (ROOT / path).exists():
            print(f"{name:14s} ⛔ chưa có {path}", flush=True)
            continue
        t0 = time.time()
        hyp, ref, _ = load(path)
        if a.limit:
            hyp, ref = hyp[:a.limit], ref[:a.limit]
        tk = PTBTokenizer()
        # câu rỗng: PTBTokenizer giữ chuỗi rỗng ⇒ vẫn nằm trong quần thể, được 0 ở mọi thước
        g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(ref)})
        c = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(hyp)})
        o = {}
        b, _ = Bleu(4).compute_score(g, c, verbose=0)
        for k in range(4):
            o[f"bleu{k+1}"] = round(100 * b[k], 2)
        o["meteor15"] = round(100 * Meteor().compute_score(g, c)[0], 2)
        o["rougeL"] = round(100 * Rouge().compute_score(g, c)[0], 2)
        o["cider_d"] = round(100 * Cider().compute_score(g, c)[0], 2)
        if not a.bo_spice:
            o["spice"] = round(100 * Spice().compute_score(g, c)[0], 2)
        o["n"] = len(hyp)
        o["src"] = path
        out[name] = o
        if not a.limit:   # ghi sau MỖI nhánh ⇒ bị ngắt giữa chừng vẫn giữ các nhánh đã xong
            json.dump(out, open(dich, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{name:14s} " + " · ".join(f"{k} {v}" for k, v in o.items() if k != "src") +
              f"  ({time.time()-t0:.0f} s)", flush=True)
    if not a.limit:
        json.dump(out, open(ROOT / a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("ghi", a.out)


if __name__ == "__main__":
    main()
