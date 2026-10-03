# -*- coding: utf-8 -*-
"""So mọi nhánh TAGE với S1/101 trên 249 bước click val C1 — exec + các thước chữ (0 GPU, CPU + Java 8).

    ~/.venvs/thesis/bin/python harness/tage_text_metrics.py [--bo-bert]

Nhánh: S1/101 greedy (k0, lượt 251) · ck500 · gold · neg · none · none+cổng · pred · pred+cổng.
Câu của nhánh +cổng: nhận câu sửa khi lp_edit − lp_draft > τ, τ chọn chéo theo episode — đúng hàm
`cong` của `tage_doc.py` (giữ câu nháp thì dùng câu và kết quả chấm của ck500).
Thước chữ: BLEU-4 · METEOR 1.5 · ROUGE-L · CIDEr-D · SPICE (pycocoevalcap, mức kho, như
`text_metrics_coco.py`) · chrF · BERTScore (đúng `text_metrics_them.tinh`). Một câu tham chiếu mỗi bước.
Δexec so S1: KTC95 bootstrap theo episode (như `tage_doc.ktc`).
Ghi `runs/tage_val/that/so_s1.json`. ⛔ Số val — không trích vào luận văn.
"""
import argparse, glob, json, os, random, sys
from pathlib import Path

J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
if J and "JAVA_HOME" not in os.environ:
    os.environ["JAVA_HOME"] = J[-1]
    os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
import tage_doc  # noqa: E402

D = ROOT / "runs/tage_val/that"
nap = tage_doc.nap


def chon_cong(keys, meta):
    """Tập bước nhận câu sửa — cùng phép chọn τ chéo như tage_doc.cong."""
    ep = sorted({k[0] for k in keys})
    random.Random(tage_doc.SEED).shuffle(ep)
    nua = {e: i % 2 for i, e in enumerate(ep)}
    return {k for k in keys if meta[k]["lp_edit"] - meta[k]["lp_draft"] > _tau[1 - nua[k[0]]]}   # τ chọn trên nửa KIA, như tage_doc.cong


_tau = {}


def coco(hyp, ref):
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    from pycocoevalcap.bleu.bleu import Bleu
    from pycocoevalcap.meteor.meteor import Meteor
    from pycocoevalcap.rouge.rouge import Rouge
    from pycocoevalcap.cider.cider import Cider
    from pycocoevalcap.spice.spice import Spice
    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(ref)})
    c = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(hyp)})
    return {"BLEU-4": 100 * Bleu(4).compute_score(g, c, verbose=0)[0][3],
            "METEOR": 100 * Meteor().compute_score(g, c)[0],
            "ROUGE-L": 100 * Rouge().compute_score(g, c)[0],
            "CIDEr-D": 100 * Cider().compute_score(g, c)[0],
            "SPICE": 100 * Spice().compute_score(g, c)[0]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bo-bert", action="store_true")
    a = ap.parse_args()
    C = nap(ROOT / "runs/grpo_spice/score_ck500_raw.jsonl")
    keys = sorted(C)
    S = {"S1/101": nap(ROOT / "runs/c1/exec8/c1score/score_k0_raw.jsonl"), "ck500": C}
    for t in ("gold", "neg", "none", "pred"):
        S[t] = nap(D / f"score_{t}_raw.jsonl")
    for t in ("none", "pred"):
        M = nap(D / f"pred_{t}_meta.jsonl")
        ck = {k: int(C[k]["executable"]) for k in keys}
        _, taus, _ = tage_doc.cong(keys, ck, {k: int(S[t][k]["executable"]) for k in keys}, M)
        _tau.update({0: taus[0], 1: taus[1]})
        sua = chon_cong(keys, M)
        S[t + "+cổng"] = {k: (S[t][k] if k in sua else C[k]) for k in keys}
        kq, _, _ = tage_doc.cong(keys, ck, {k: int(S[t][k]["executable"]) for k in keys}, M)
        assert sum(int(S[t + "+cổng"][k]["executable"]) for k in keys) == sum(kq.values()), "lệch tage_doc.cong"
    assert all(set(v) == set(keys) for v in S.values())
    ref = [C[k]["gold_instruction"] for k in keys]
    s1 = {k: int(S["S1/101"][k]["executable"]) for k in keys}

    them = None
    if not a.bo_bert:
        from text_metrics_them import tinh as them

    out = {}
    for ten, R in S.items():
        hyp = [R[k]["sent"] or "" for k in keys]
        x = {k: int(R[k]["executable"]) for k in keys}
        o = {"exec": 100 * sum(x.values()) / len(keys),
             "action_ok": 100 * sum(int(R[k]["action_ok"]) for k in keys) / len(keys),
             "hit_±14%": 100 * sum(int(R[k]["hit_disk"]) for k in keys) / len(keys)}
        d = {k: x[k] - s1[k] for k in keys}
        lo, hi = tage_doc.ktc(keys, d)
        o.update({"Δexec_vs_S1": 100 * sum(d.values()) / len(keys), "KTC_lo": lo, "KTC_hi": hi,
                  "cuu_vs_S1": sum(v > 0 for v in d.values()), "pha_vs_S1": sum(v < 0 for v in d.values()),
                  "doi_cau_vs_S1": sum(hyp[i] != S["S1/101"][k]["sent"] for i, k in enumerate(keys))})
        o.update(coco(hyp, ref))
        if them:
            t = them(hyp, ref, bert=True)
            o.update({"chrF": t["chrf"], "BERTScore": t["bertscore_f1_rescaled"]})
        out[ten] = {k: (round(v, 2) if isinstance(v, float) else v) for k, v in o.items()}
        print(ten, out[ten], flush=True)
    json.dump(out, open(D / "so_s1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", D / "so_s1.json")


if __name__ == "__main__":
    main()
