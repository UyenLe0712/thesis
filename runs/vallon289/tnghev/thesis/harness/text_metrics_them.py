# -*- coding: utf-8 -*-
"""Thêm các thước tham chiếu chuẩn cho mọi nhánh, tính từ tệp *_raw.jsonl — 0 giây GPU, chạy CPU.

Bổ sung cho `text_metrics.py` (BLEU-4 trung bình mức câu · ROUGE-L · action_ok). File này KHÔNG
sửa tệp kết quả của script kia, ghi riêng `runs/text_metrics_them.json`.

Thước và cấu hình:
  · sacreBLEU  — BLEU-4 mức KHO (corpus), cấu hình mặc định của sacrebleu (tokenizer 13a), in kèm
                 chữ ký. Đây là cách báo BLEU chuẩn (Post, WMT 2018); khác số BLEU-4 trung bình
                 mức câu của bảng 6.1 ⇒ phải ghi rõ tên.
  · chrF       — sacrebleu mặc định (chrF2, n ký tự = 6).
  · METEOR     — nltk `meteor_score` (khớp exact + stem + WordNet), trung bình mức câu. ⚠️ KHÔNG
                 phải bản Java METEOR 1.5 chính thức ⇒ ghi là "METEOR (nltk)".
  · CIDEr-D    — pycocoevalcap `Cider` (bản CIDEr-D của coco-caption), một câu tham chiếu mỗi bước,
                 token hoá bằng \\w+ thường hoá (bỏ PTBTokenizer vì nó đòi Java).
  · BERTScore  — F1, `roberta-large` tầng 17 (mặc định cho tiếng Anh), idf=False; in cả bản thô
                 lẫn bản rescale_with_baseline (bản thô luôn ~0,85–0,95 kể cả câu tệ).

Quần thể: đủ 4.463 bước chạm của mỗi nhánh; câu rỗng giữ nguyên trong quần thể.
Chạy:  ~/.venvs/thesis/bin/python harness/text_metrics_them.py [--limit N] [--bo-bert]
"""
import argparse, json, re, statistics, time, warnings
from pathlib import Path

warnings.filterwarnings("ignore")
import sacrebleu
from nltk.translate.meteor_score import meteor_score
from pycocoevalcap.cider.cider import Cider

ROOT = Path(__file__).resolve().parent.parent
from text_metrics import BRANCHES, load  # dùng lại đúng danh sách nhánh + hàm nạp


def tok(s):
    return re.findall(r"\w+", s.lower())


SC = None


def tinh(hyp, ref, bert=True):
    o = {}
    B, C = sacrebleu.BLEU(), sacrebleu.CHRF()
    o["sacrebleu"] = round(B.corpus_score(hyp, [ref]).score, 2)
    o["sacrebleu_sig"] = str(B.get_signature())
    o["chrf"] = round(C.corpus_score(hyp, [ref]).score, 2)
    o["meteor_nltk"] = round(100 * statistics.mean(
        meteor_score([tok(r)], tok(h)) if tok(h) else 0.0 for h, r in zip(hyp, ref)), 2)
    g = {i: [" ".join(tok(r))] for i, r in enumerate(ref)}
    c = {i: [" ".join(tok(h))] for i, h in enumerate(hyp)}
    o["cider_d"] = round(100 * Cider().compute_score(g, c)[0], 2)
    if bert:
        global SC
        if SC is None:
            from bert_score import BERTScorer
            import bert_score.utils as U
            _goc = U.sent_encode

            def _sent_encode(tokenizer, sent):
                # bert_score 0.3.12 gọi build_inputs_with_special_tokens([]) cho câu rỗng, hàm này đã bị
                # gỡ khỏi transformers mới ⇒ AttributeError. Trả đúng thứ bản gốc định trả: [CLS, SEP].
                if sent.strip() == "":
                    return tokenizer("", add_special_tokens=True)["input_ids"]
                return _goc(tokenizer, sent)
            U.sent_encode = _sent_encode
            SC = BERTScorer(lang="en", rescale_with_baseline=True, batch_size=64)
        _, _, f2 = SC.score(hyp, ref)                       # đã rescale
        b = SC.baseline_vals[2].item()                      # baseline F1
        f1 = f2 * (1 - b) + b                               # đảo phép rescale tuyến tính
        # câu rỗng: F1 thô 0 ⇒ bản rescale ra ~ -490 điểm, một câu kéo trung bình đi ~0,1 điểm.
        # Quy ước giống executability: câu rỗng giữ trong quần thể và được 0 ở CẢ HAI bản.
        rong = [i for i, h in enumerate(hyp) if not h.strip()]
        f1[rong] = 0.0
        f2[rong] = 0.0
        o["bertscore_f1_rescaled"] = round(100 * f2.mean().item(), 2)
        o["bertscore_f1"] = round(100 * f1.mean().item(), 2)
        o["bertscore_hash"] = SC.hash
    o["n"] = len(hyp)
    o["n_rong"] = sum(1 for h in hyp if not h)
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="chỉ lấy N bước đầu (chạy thử)")
    ap.add_argument("--bo-bert", action="store_true")
    ap.add_argument("--out", default="runs/text_metrics_them.json")
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
        o = tinh(hyp, ref, bert=not a.bo_bert)
        o["src"] = path
        out[name] = o
        if not a.limit:   # ghi sau MỖI nhánh ⇒ bị ngắt giữa chừng vẫn giữ các nhánh đã xong
            json.dump(out, open(dich, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{name:14s} " + " · ".join(f"{k} {v}" for k, v in o.items()
                                           if k not in ("src", "sacrebleu_sig", "bertscore_hash")) +
              f"  ({time.time()-t0:.0f} s)", flush=True)
    if not a.limit:
        json.dump(out, open(ROOT / a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("ghi", a.out)


if __name__ == "__main__":
    main()
