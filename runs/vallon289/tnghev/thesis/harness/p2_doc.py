# -*- coding: utf-8 -*-
"""Đọc kết quả P2 của FGRB — CPU máy nhà, 0 GPU.

Chấm ba tệp gen_{s1,fgrb,hoanvi}.jsonl (1.567 bước val) bằng bộ chấm COCO chính thức (PTBTokenizer
+ BLEU-4 + CIDEr-D, như harness/text_metrics_coco.py) rồi áp ba điều kiện P2 của tài liệu 230:
  ① FGRB − S1 ≥ +0,3 BLEU-4 VÀ ≥ +3 CIDEr-D
  ② FGRB − hoán vị ≥ +0,3 BLEU-4
  ③ độ dài câu trung bình của FGRB lệch S1 không quá 15%
Kèm KTC95 bootstrap theo episode cho hai hiệu số, và vài số chẩn đoán (tỉ lệ câu đổi, cổng, |g·z|/|h|).
⛔ Số ở đây là số VAL — chỉ để phán P2, không trích ra báo.

    ~/.venvs/thesis/bin/python harness/p2_doc.py --dir ~/fgrb_p1/p2 [--out runs/fgrb_p2/p2_doc.json]
"""
import argparse, glob, json, os, random, statistics, collections

J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
if J and "JAVA_HOME" not in os.environ:
    os.environ["JAVA_HOME"] = J[-1]
    os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]

from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.cider.cider import Cider

MODES = ["s1", "fgrb", "hoanvi"]


def load(path):
    return {json.loads(x)["key"]: json.loads(x) for x in open(path, encoding="utf-8")}


def score(g, c, ids):
    gg = {i: g[i] for i in ids}
    cc = {i: c[i] for i in ids}
    b = Bleu(4).compute_score(gg, cc, verbose=0)[0][3]
    d = Cider().compute_score(gg, cc)[0]
    return 100 * b, 100 * d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--n-expect", type=int, default=1567)
    ap.add_argument("--boot", type=int, default=500)
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    R = {m: load(os.path.join(a.dir, f"gen_{m}.jsonl")) for m in MODES}
    keys = sorted(R["s1"])
    for m in MODES:
        assert sorted(R[m]) == keys, f"{m}: khoa lech voi s1"
    assert len(keys) == a.n_expect, f"co {len(keys)} buoc, can {a.n_expect} — chua sinh du"
    for k in keys:
        assert R["s1"][k]["gold"] == R["fgrb"][k]["gold"] == R["hoanvi"][k]["gold"]

    tk = PTBTokenizer()
    ref = tk.tokenize({k: [{"caption": R["s1"][k]["gold"]}] for k in keys})
    hyp = {m: tk.tokenize({k: [{"caption": R[m][k]["pred"]}] for k in keys}) for m in MODES}

    out = {"n": len(keys)}
    for m in MODES:
        b, d = score(ref, hyp[m], keys)
        ln = statistics.mean(len(hyp[m][k][0].split()) for k in keys)
        out[m] = {"bleu4": round(b, 2), "cider_d": round(d, 2), "len_tu": round(ln, 2)}
        print(f"{m:7s} BLEU-4 {b:6.2f}  CIDEr-D {d:7.2f}  do dai TB {ln:.2f} tu", flush=True)

    # bootstrap theo episode (cùng lát cho mọi chế độ ⇒ ghép cặp)
    ep = collections.defaultdict(list)
    for k in keys:
        ep[R["s1"][k]["episode_id"]].append(k)
    eps = sorted(ep)
    rng = random.Random(101)
    diffs = {"fgrb-s1_bleu": [], "fgrb-s1_cider": [], "fgrb-hoanvi_bleu": []}
    for _ in range(a.boot):
        pick = [rng.choice(eps) for _ in eps]
        ids, ref_b, h_b = [], {}, {m: {} for m in MODES}
        for n_, e in enumerate(pick):
            for k in ep[e]:
                nk = f"{n_}|{k}"
                ids.append(nk)
                ref_b[nk] = ref[k]
                for m in MODES:
                    h_b[m][nk] = hyp[m][k]
        s = {m: score(ref_b, h_b[m], ids) for m in MODES}
        diffs["fgrb-s1_bleu"].append(s["fgrb"][0] - s["s1"][0])
        diffs["fgrb-s1_cider"].append(s["fgrb"][1] - s["s1"][1])
        diffs["fgrb-hoanvi_bleu"].append(s["fgrb"][0] - s["hoanvi"][0])
    ci = {}
    for name, v in diffs.items():
        v = sorted(v)
        ci[name] = [round(float(v[int(0.025 * len(v))]), 2), round(float(v[int(0.975 * len(v)) - 1]), 2)]
    out["ktc95_bootstrap_episode"] = ci

    d_b = out["fgrb"]["bleu4"] - out["s1"]["bleu4"]
    d_c = out["fgrb"]["cider_d"] - out["s1"]["cider_d"]
    d_h = out["fgrb"]["bleu4"] - out["hoanvi"]["bleu4"]
    d_len = out["fgrb"]["len_tu"] / out["s1"]["len_tu"] - 1
    g1 = d_b >= 0.3 and d_c >= 3
    g2 = d_h >= 0.3
    g3 = abs(d_len) <= 0.15
    changed = sum(R["fgrb"][k]["pred"] != R["s1"][k]["pred"] for k in keys)
    changed_h = sum(R["hoanvi"][k]["pred"] != R["fgrb"][k]["pred"] for k in keys)
    out["chan_doan"] = {
        "cau_fgrb_khac_s1": changed, "cau_hoanvi_khac_fgrb": changed_h,
        "gate_tb": round(statistics.mean(R["fgrb"][k]["gate"] for k in keys), 4),
        "ratio_gz_h_tb": round(statistics.mean(R["fgrb"][k]["ratio"] for k in keys), 5)}
    out["cong"] = {"fgrb-s1_bleu": round(d_b, 2), "fgrb-s1_cider": round(d_c, 2),
                   "fgrb-hoanvi_bleu": round(d_h, 2), "lech_do_dai": round(100 * d_len, 2),
                   "dk1": g1, "dk2": g2, "dk3": g3}
    out["phan_quyet"] = "P2 DAT — duoc de xuat pilot, chua duoc train" if (g1 and g2 and g3) \
        else "P2 TRUOT — khong train"

    print(f"\nFGRB − S1     : BLEU-4 {d_b:+.2f} KTC95 {ci['fgrb-s1_bleu']}  "
          f"CIDEr-D {d_c:+.2f} KTC95 {ci['fgrb-s1_cider']}   dieu kien ①: {'DAT' if g1 else 'TRUOT'}")
    print(f"FGRB − hoán vị: BLEU-4 {d_h:+.2f} KTC95 {ci['fgrb-hoanvi_bleu']}   dieu kien ②: "
          f"{'DAT' if g2 else 'TRUOT'}")
    print(f"do dai FGRB/S1: {100*d_len:+.2f}%   dieu kien ③: {'DAT' if g3 else 'TRUOT'}")
    print(f"chan doan: {out['chan_doan']}")
    print(f"\n{out['phan_quyet']}")
    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("ghi", a.out)


if __name__ == "__main__":
    main()
