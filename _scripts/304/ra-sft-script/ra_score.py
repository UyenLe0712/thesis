# -*- coding: utf-8 -*-
"""304 — chấm 7 thước chữ trên bước click, cùng công cụ đã ra số luận văn của ck500:
BLEU-4 · METEOR 1.5 · ROUGE-L · CIDEr-D · SPICE (pycocoevalcap, PTBTokenizer, mục kho; cần Java 8)
chrF (sacrebleu mặc định) · BERTScore F1 rescale (roberta-large, câu rỗng = 0, như text_metrics_them.tinh)
So mọi nhánh với nhánh gốc (mặc định ck500). --check: ck500 phải tái lập số test đã công bố (lệch ≤ 0,06).

  python ra_score.py --recs T/test.jsonl --pred ck500=pred_ck500_test.jsonl --pred ra_k4=pred_ra_k4.jsonl \
      --pred ra_rong=pred_ra_rong.jsonl --pred cont=pred_cont.jsonl --ra ra_k4=ex_test_k4.jsonl --check --out diem.json
  python ra_score.py ... --no-bert --no-spice    # nhanh, khi chỉ cần xem chiều
"""
import os, re, sys, json, argparse, warnings

warnings.filterwarnings("ignore")
TAPT = ("click", "long_press")
CK500_TEST = dict(bleu4=52.36, meteor=37.92, rougeL=68.36, cider_d=430.05, spice=45.79, chrf=62.87, bertscore=67.07)
TEN = dict(bleu4="BLEU-4", meteor="METEOR", rougeL="ROUGE-L", cider_d="CIDEr-D", spice="SPICE", chrf="chrF",
           bertscore="BERTScore")


def tokw(s):
    return re.findall(r"\w+", (s or "").lower())


def bert_scorer():
    from bert_score import BERTScorer
    import bert_score.utils as U
    goc = U.sent_encode

    def enc(tokenizer, sent):
        if sent.strip() == "":
            return tokenizer("", add_special_tokens=True)["input_ids"]
        return goc(tokenizer, sent)

    U.sent_encode = enc
    return BERTScorer(lang="en", rescale_with_baseline=True, batch_size=64)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recs", required=True)
    ap.add_argument("--pred", action="append", required=True, help="ten=duong_dan")
    ap.add_argument("--base", default="ck500")
    ap.add_argument("--ra", action="append", default=[], help="ten=tep_vi_du — đo tỉ lệ chép nguyên văn ví dụ")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--no-bert", action="store_true")
    ap.add_argument("--no-spice", action="store_true")
    ap.add_argument("--out", default="diem_304.json")
    a = ap.parse_args()

    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    from pycocoevalcap.bleu.bleu import Bleu
    from pycocoevalcap.meteor.meteor import Meteor
    from pycocoevalcap.rouge.rouge import Rouge
    from pycocoevalcap.cider.cider import Cider
    import sacrebleu

    recs = [json.loads(l) for l in open(a.recs, encoding="utf-8")]
    recs = [r for r in recs if (r.get("action") or {}).get("action_type") in TAPT and "x" in r["action"]]
    K = [(r["episode_id"], r["step_id"]) for r in recs]
    REF = [(r.get("gold_instruction") or r.get("target_instruction") or "").strip() for r in recs]
    P = {}
    for s in a.pred:
        ten, p = s.split("=", 1)
        d = {(x["episode_id"], x["step_id"]): (x.get("pred") or "").strip()
             for x in map(json.loads, open(p, encoding="utf-8"))}
        miss = [k for k in K if k not in d]
        assert not miss, f"⛔ {ten}: thiếu {len(miss)} bước, ví dụ {miss[:3]}"
        P[ten] = [d[k] for k in K]
    assert a.base in P, f"⛔ thiếu nhánh gốc {a.base}"
    print(f"[dữ liệu] {len(K)} bước click · nhánh {list(P)}", flush=True)

    tk = PTBTokenizer()
    G = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(REF)})
    SC = None if a.no_bert else bert_scorer()
    out = {}
    for ten, H in P.items():
        C = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(H)})
        b, _ = Bleu(4).compute_score(G, C, verbose=0)
        o = dict(bleu4=100 * b[3], meteor=100 * Meteor().compute_score(G, C)[0],
                 rougeL=100 * Rouge().compute_score(G, C)[0], cider_d=100 * Cider().compute_score(G, C)[0])
        if not a.no_spice:
            from pycocoevalcap.spice.spice import Spice
            o["spice"] = 100 * Spice().compute_score(G, C)[0]
        o["chrf"] = sacrebleu.CHRF().corpus_score(H, [REF]).score
        if SC is not None:
            _, _, f2 = SC.score(H, REF)
            for i, h in enumerate(H):
                if not h:
                    f2[i] = 0.0
            o["bertscore"] = 100 * f2.mean().item()
        o = {k: round(v, 2) for k, v in o.items()}
        o["rong"] = sum(not h for h in H)
        o["doi_cau_so_goc_pct"] = round(100 * sum(tokw(h) != tokw(g) for h, g in zip(H, P[a.base])) / len(H), 1)
        o["trung_chuan_pct"] = round(100 * sum(tokw(h) == tokw(r) for h, r in zip(H, REF)) / len(H), 1)
        out[ten] = o
        print(f"{ten:10s} " + " · ".join(f"{k} {v}" for k, v in o.items()), flush=True)

    for s in a.ra:
        ten, p = s.split("=", 1)
        E = {(x["episode_id"], x["step_id"]): x["exemplars"] for x in map(json.loads, open(p, encoding="utf-8"))}
        cop = [any(tokw(e["sent"]) == tokw(h) for e in E[k]) for k, h in zip(K, P[ten])]
        dung = [c and tokw(h) == tokw(r) for c, h, r in zip(cop, P[ten], REF)]
        out[ten]["chep_vi_du_pct"] = round(100 * sum(cop) / len(K), 1)
        out[ten]["chep_dung_pct_trong_so_chep"] = round(100 * sum(dung) / max(sum(cop), 1), 1)
        print(f"[chép] {ten}: chép nguyên văn một ví dụ ở {out[ten]['chep_vi_du_pct']}% bước · "
              f"trong số đó đúng câu chuẩn {out[ten]['chep_dung_pct_trong_so_chep']}%", flush=True)

    M = [m for m in TEN if m in out[a.base]]
    tin = True
    if a.check:
        lech = {m: round(out[a.base][m] - CK500_TEST[m], 2) for m in M}
        tin = all(abs(v) <= 0.06 for v in lech.values())
        print(f"[tự kiểm] {a.base} — số đã công bố: {lech} → {'KHỚP' if tin else '⚠ LỆCH — dừng đọc Δ'}", flush=True)

    print(f"\n| thước | {a.base} | " + " | ".join(t for t in P if t != a.base) + " |")
    print("|---|---:|" + "---:|" * (len(P) - 1))
    for m in M:
        print(f"| {TEN[m]} | {out[a.base][m]:.2f} | " + " | ".join(
            f"{out[t][m]:.2f} ({out[t][m] - out[a.base][m]:+.2f})" for t in P if t != a.base) + " |")

    ket = {}
    for t in P:
        if t == a.base:
            continue
        hon = [m for m in M if out[t][m] > out[a.base][m]]
        ket[t] = dict(hon=len(hon), tong=len(M), thuoc_hon=[TEN[m] for m in hon],
                      dat=len(hon) >= (4 if len(M) == 7 else (len(M) // 2 + 1)))
        print(f"[kết luận] {t}: cao hơn {a.base} ở {len(hon)}/{len(M)} thước "
              f"({', '.join(TEN[m] for m in hon) or '—'}) · {'ĐẠT' if ket[t]['dat'] else 'chưa đạt'}", flush=True)

    json.dump(dict(diem=out, ket_luan=ket, tu_kiem_khop=tin, base=a.base, n=len(K)),
              open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", a.out)


if __name__ == "__main__":
    main()
