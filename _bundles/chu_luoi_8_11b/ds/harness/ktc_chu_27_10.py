# -*- coding: utf-8 -*-
"""KTC95 ghép cặp cho thước chữ của các nhánh mới 24–26/10 (S1/202, ck500/202, xao101, 7B, lịch sử tự sinh,
AitZ) — 0 GPU, CPU + Java 8. Mở rộng `ktc_thuoc_chu.py` (bản chỉ có S1/101 · ck500 · ACE).

    python -u ktc_chu_27_10.py [--B 2000]        # ghi runs/ktc_chu_27_10.json (ghi lại sau mỗi nhánh và cuối)

Cách tính, giống `ktc_thuoc_chu.py`:
  · Bootstrap theo cụm (AndroidControl: cụm = app, bước không có app gom theo tác vụ, lấy từ tệp thô S1/101;
    AitZ: cụm = episode). Mọi nhánh trong một nhóm dùng chung một lần rút cụm ⇒ Δ là Δ ghép cặp.
  · BLEU-4: tính lại mức kho từ số n-gram từng bước (BleuScorer COCO, option closest).
  · ROUGE-L · CIDEr-D · SPICE: trung bình điểm từng bước (IDF của CIDEr-D lấy trên cả tập, không tính lại mỗi mẫu).
  · chrF: mức kho đúng nghĩa, cộng thống kê từng câu của sacrebleu rồi tính điểm (bản cũ là trung bình mức câu).
  · BERTScore (roberta-large L17, rescaled, câu rỗng = 0): trung bình từng câu, đúng cách số mức kho được tính.
  · METEOR: KHÔNG có KTC (gộp mức kho bằng thống kê của chính METEOR).
Kiểm tái lập: điểm gốc từng nhánh phải khớp số đã lưu ở report/320 (±0,06; CIDEr-D ±0,1), lệch là dừng.
"""
import argparse, json, math, os, sys, time
from pathlib import Path

import numpy as np
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.bleu.bleu_scorer import BleuScorer
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.cider.cider import Cider
from pycocoevalcap.spice.spice import Spice
from sacrebleu.metrics import CHRF

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"
CACHE = RUNS / "ktc_chu_27_10_cache"

# tên: (tệp trong runs/, số dòng) — tệp tuantu_* xếp đúng thứ tự tệp thô S1/101
AC = {"S1/101": "score_s1_seed101_raw.jsonl", "S1/202": "score_s1_seed202_raw.jsonl",
      "ck500": "score_ck500_test_raw.jsonl", "ck500/202": "score_ck500_s202_test_raw.jsonl",
      "ACE": "score_R3_test_raw.jsonl", "xao101": "score_ck500_xao101_test_raw.jsonl",
      "7B": "score_qwen7b_test_raw.jsonl",
      "tự sinh S1": "tuantu_s1_rows.jsonl", "tự sinh ck500": "tuantu_ck500_rows.jsonl"}
AZ = {"AitZ Base": "score_base_aitz_raw.jsonl", "AitZ S1": "score_s1_aitz_raw.jsonl",
      "AitZ ck500": "score_ck500_aitz_raw.jsonl", "AitZ ck500/202": "score_ck500_s202_aitz_raw.jsonl",
      "AitZ ACE": "score_r3_aitz_raw.jsonl", "AitZ ra_k4": "score_ra_k4_aitz_raw.jsonl"}
ACU = {f"ACU {t}": f"score_{f}_acu_raw.jsonl" for t, f in
       (("câu chuẩn", "gold"), ("Base", "base"), ("S1", "s1"), ("ck500", "ck500"), ("ck500/202", "ck500_s202"),
        ("ACE", "r3"), ("ra_k4", "ra_k4"))}
# số mức kho đã lưu (report/320 mục 3, 6.3, 7): bleu4, rougeL, cider_d, spice, chrf, bert
DA = {"S1/101": (51.56, 67.35, 416.12, 44.37, 61.26, 66.33), "S1/202": (51.66, 67.71, 419.19, 44.23, 61.92, 66.75),
      "ck500": (52.36, 68.36, 430.05, 45.79, 62.87, 67.07), "ck500/202": (52.94, 68.48, 431.22, 45.69, 62.37, 67.12),
      "ACE": (53.47, 69.08, 442.02, 47.13, 63.44, 67.73), "xao101": (51.32, 67.36, 418.13, 44.40, 61.52, 66.40),
      "7B": (14.48, 39.79, 100.71, 18.74, 36.22, 39.70),
      "tự sinh S1": (43.44, 59.78, 331.42, 34.97, 53.71, 59.11), "tự sinh ck500": (43.50, 60.39, 333.58, 35.10, 54.54, 59.23),
      "AitZ Base": (18.68, 39.11, 86.98, 15.66, 35.24, 38.81), "AitZ S1": (21.01, 46.84, 120.24, 15.27, 35.66, 49.69),
      "AitZ ck500": (21.48, 46.92, 123.38, 16.37, 36.28, 49.68), "AitZ ck500/202": (19.76, 45.44, 117.26, 15.63, 34.43, 48.47),
      "AitZ ACE": (21.45, 46.91, 123.29, 16.40, 36.24, 49.63), "AitZ ra_k4": (19.94, 45.39, 117.42, 15.70, 34.24, 48.27)}
THUOC = ("bleu4", "rougeL", "cider_d", "spice", "chrf", "bert")
SO_AC = [("ck500", "S1/101"), ("ck500", "S1/202"), ("ck500/202", "S1/101"), ("ck500/202", "S1/202"),
         ("ck500/202", "ck500"), ("S1/202", "S1/101"), ("ACE", "S1/101"), ("ACE", "S1/202"), ("ACE", "ck500"),
         ("ACE", "ck500/202"), ("xao101", "S1/101"), ("ck500", "xao101"), ("S1/101", "7B"), ("ck500", "7B"),
         ("ACE", "7B"), ("tự sinh ck500", "tự sinh S1"), ("tự sinh S1", "S1/101"), ("tự sinh ck500", "ck500")]
SO_ACU = [("ACU ck500", "ACU S1"), ("ACU ck500/202", "ACU S1"), ("ACU ck500/202", "ACU ck500"),
          ("ACU ACE", "ACU S1"), ("ACU ACE", "ACU ck500"), ("ACU ra_k4", "ACU S1"), ("ACU S1", "ACU Base")]
SO_AZ = [("AitZ S1", "AitZ Base"), ("AitZ ck500", "AitZ Base"), ("AitZ ck500", "AitZ S1"),
         ("AitZ ck500/202", "AitZ S1"), ("AitZ ACE", "AitZ S1"), ("AitZ ACE", "AitZ ck500"), ("AitZ ra_k4", "AitZ S1")]

BERT = None


def bert_cau(hyp, ref):
    global BERT
    if BERT is None:
        from bert_score import BERTScorer
        import bert_score.utils as U
        goc = U.sent_encode
        U.sent_encode = lambda tk, s: tk("", add_special_tokens=True)["input_ids"] if s.strip() == "" else goc(tk, s)
        BERT = BERTScorer(lang="en", rescale_with_baseline=True, batch_size=64)
    _, _, f2 = BERT.score(hyp, ref)
    f2 = f2.numpy().astype(float)
    f2[[i for i, h in enumerate(hyp) if not h.strip()]] = 0.0      # câu rỗng = 0, như text_metrics_them
    return f2


kh = lambda r: (str(r["episode_id"]), str(r["step_id"]))


def tung_buoc(ten, f, thu_tu):
    """Tính từng bước theo đúng thứ tự `thu_tu` (thứ tự tệp thô đầu nhóm) để mọi nhánh ghép cặp theo chỉ số."""
    c = CACHE / (ten.replace("/", "_").replace(" ", "_") + ".npz")
    R = {kh(r): r for r in map(json.loads, open(RUNS / f, encoding="utf-8"))}
    assert len(R) == len(thu_tu) and set(R) == set(thu_tu), f"⛔ {ten}: tập bước khác nhánh đầu nhóm"
    rows = [R[k] for k in thu_tu]
    if c.exists():
        return dict(np.load(c)), rows
    t0 = time.time()
    hyp = [(r.get("sent") or "").strip() for r in rows]
    ref = [(r.get("gold_instruction") or "").strip() for r in rows]
    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(ref)})
    h = tk.tokenize({i: [{"caption": x}] for i, x in enumerate(hyp)})
    bs = BleuScorer(n=4)
    for i in sorted(g):
        bs += (h[i][0], g[i])
    bs.compute_score(option="closest")
    ct = bs.ctest
    d = dict(cor=np.array([x["correct"] for x in ct], float), gue=np.array([x["guess"] for x in ct], float),
             tl=np.array([x["testlen"] for x in ct], float), rl=np.array([x["reflen"] for x in ct], float))
    d["rouge"] = np.array(Rouge().compute_score(g, h)[1], float)
    d["cider"] = np.array(Cider().compute_score(g, h)[1], float)
    d["spice"] = np.array([s["All"]["f"] for s in Spice().compute_score(g, h)[1]], float)
    d["chrf_st"] = np.array(CHRF()._extract_corpus_statistics(hyp, [ref]), float)
    d["bert"] = bert_cau(hyp, ref)
    CACHE.mkdir(exist_ok=True)
    np.savez(c, **d)
    print(f"  {ten}: tính từng bước xong ({time.time()-t0:.0f} s)", flush=True)
    return d, rows


CH = CHRF()


def bleu4(cor, gue, tl, rl):
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
                spice=100 * s(d["spice"]).mean(),
                chrf=CH._compute_score_from_stats(list(s(d["chrf_st"]).sum(0))).score,
                bert=100 * s(d["bert"]).mean())


def nhom(ten_nhom, NH, SO, cum_cua, B, out, dich):
    D = {}
    goc = [json.loads(l) for l in open(RUNS / next(iter(NH.values())), encoding="utf-8")]
    thu_tu = [kh(r) for r in goc]
    for t, f in NH.items():
        D[t], _ = tung_buoc(t, f, thu_tu)
    loi = []
    pt0 = {t: diem(D[t]) for t in NH}
    for t in NH:
        if t not in DA:                                   # nhánh mới (ACU): chưa có số lưu để đối chiếu
            continue
        for k, v in zip(THUOC, DA[t]):
            if abs(pt0[t][k] - v) > (0.1 if k == "cider_d" else 0.06):
                loi.append(f"{t} {k} tính {pt0[t][k]:.2f} ≠ đã lưu {v}")
    if loi:
        sys.exit("⛔ DỪNG, không tái lập số đã lưu: " + " · ".join(loi))
    print(f"✅ {ten_nhom}: {len(NH)} nhánh tái lập số đã lưu", flush=True)
    cl = {}
    for i, r in enumerate(goc):
        cl.setdefault(cum_cua(r), []).append(i)
    cum = [np.array(v) for v in cl.values()]
    G = len(cum)
    rng = np.random.default_rng(20261027)
    kq = {t: {k: [] for k in THUOC} for t in NH}
    t0 = time.time()
    for b in range(B):
        idx = np.concatenate([cum[j] for j in rng.integers(0, G, G)])
        for t in NH:
            p = diem(D[t], idx)
            for k in THUOC:
                kq[t][k].append(p[k])
        if (b + 1) % 200 == 0:
            print(f"  {ten_nhom} bootstrap {b+1}/{B} · {time.time()-t0:.0f} s", flush=True)
    o = {"cum": G, "diem": {}, "so": {}, "meteor": {}}
    if not all(t in DA for t in NH):                      # METEOR mức kho (không KTC) cho nhánh mới
        from pycocoevalcap.meteor.meteor import Meteor
        for t, f in NH.items():
            rows = [json.loads(l) for l in open(RUNS / f, encoding="utf-8")]
            tk = PTBTokenizer()
            g = tk.tokenize({i: [{"caption": (r.get("gold_instruction") or "").strip()}] for i, r in enumerate(rows)})
            h = tk.tokenize({i: [{"caption": (r.get("sent") or "").strip()}] for i, r in enumerate(rows)})
            o["meteor"][t] = round(100 * Meteor().compute_score(g, h)[0], 2)
        print(f"  METEOR {o['meteor']}", flush=True)
    for t in NH:
        o["diem"][t] = {k: dict(diem=round(pt0[t][k], 2), lo=round(float(np.percentile(kq[t][k], 2.5)), 2),
                                hi=round(float(np.percentile(kq[t][k], 97.5)), 2)) for k in THUOC}
    for a, b in SO:
        o["so"][f"{a} − {b}"] = {}
        for k in THUOC:
            dl = np.array(kq[a][k]) - np.array(kq[b][k])
            o["so"][f"{a} − {b}"][k] = dict(delta=round(pt0[a][k] - pt0[b][k], 2),
                                            lo=round(float(np.percentile(dl, 2.5)), 2),
                                            hi=round(float(np.percentile(dl, 97.5)), 2))
        print(f"  {a} − {b}: " + " · ".join(f"{k} {v['delta']:+.2f} [{v['lo']:+.2f}; {v['hi']:+.2f}]"
                                           for k, v in o["so"][f"{a} − {b}"].items()), flush=True)
    out[ten_nhom] = o
    json.dump(out, open(dich, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=2000); a = ap.parse_args()
    dich = RUNS / "ktc_chu_27_10.json"
    out = {"B": a.B, "ghi_chu": "bootstrap cụm; METEOR không có KTC; chrF mức kho từ thống kê sacrebleu; "
                               "CIDEr-D giữ IDF của cả tập"}
    s1 = {(str(r["episode_id"]), str(r["step_id"])): (r.get("app") or f"ep{r['episode_id']}")
          for r in map(json.loads, open(RUNS / AC["S1/101"], encoding="utf-8"))}
    nhom("AndroidControl", AC, SO_AC, lambda r: s1[(str(r["episode_id"]), str(r["step_id"]))], a.B, out, dich)
    nhom("ACU", ACU, SO_ACU, lambda r: r.get("app") or f"ep{r['episode_id']}", a.B, out, dich)
    nhom("AitZ", AZ, SO_AZ, lambda r: f"ep{r['episode_id']}", a.B, out, dich)
    print("→", dich, flush=True)


if __name__ == "__main__":
    main()
