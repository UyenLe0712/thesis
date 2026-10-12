# -*- coding: utf-8 -*-
"""311 — KTC95 bootstrap gom cụm theo tác vụ cho hiệu số thước chữ giữa hai tệp câu trên 4.463 bước click tập kiểm (CPU).

BLEU-4 (corpus, gộp thống kê n-gram), ROUGE-L (trung bình câu, β = 1,2), CIDEr-D (trung bình câu, df trên câu chuẩn tập kiểm),
tách từ xấp xỉ PTBTokenizer — cùng bộ đo đã tái lập Δ chính thức của ra_k4/R3 lệch ≤ 0,06 (file 308 §2.1).
Số điểm tuyệt đối lấy từ ra_score.py (bản chính thức); script này chỉ cho khoảng tin cậy của hiệu số. B = 1000, hạt 20261010.

    python ktc_chu.py --a pred_rag500_test.jsonl --b pred_ck500_test.jsonl [--ten-a rag500 --ten-b ck500]
    python ktc_chu.py --tu-kiem        # R3 - ck500 phải ra +1,12 [+0,78; +1,45] · +0,76 · +12,04 như 308 §11.1
"""
import argparse, json, math, os, random, re
from collections import Counter, defaultdict

KHO = next(p for p in ("/mnt/d/Master/Thesis", "/Users/P836901/Documents/Self-learning/thesis/thesis-master") if os.path.isdir(p))
PUNCT = {"''", '"', "``", "-lrb-", "-rrb-", "-lcb-", "-rcb-", ".", "?", "!", ",", ":", "-", "--", "...", ";", "'"}
TOK = re.compile(r"n't|'s|'re|'ve|'ll|'d|'m|[a-z0-9]+(?:[-./][a-z0-9]+)*|[^\sa-z0-9]")


def tok(s):
    s = (s or "").lower().replace("“", '"').replace("”", '"').replace("’", "'")
    s = re.sub(r"(\w)n't\b", r"\1 n't", s)
    return [t for t in TOK.findall(s) if t not in PUNCT and t != ""]


def ngrams(ws, n=4):
    c = defaultdict(int)
    for k in range(1, n + 1):
        for i in range(len(ws) - k + 1):
            c[tuple(ws[i:i + k])] += 1
    return c


class CiderD:
    def __init__(self, refs, n=4, sigma=6.0):
        self.n, self.sigma, self.df = n, sigma, defaultdict(float)
        for r in refs:
            for ng in set(ngrams(tok(r), n)):
                self.df[ng] += 1
        self.log_n = math.log(float(len(refs)))

    def _vec(self, s):
        vec, norm, length = [dict() for _ in range(self.n)], [0.0] * self.n, 0
        for ng, tf in ngrams(tok(s), self.n).items():
            k = len(ng) - 1
            w = float(tf) * (self.log_n - math.log(max(1.0, self.df.get(ng, 0.0))))
            vec[k][ng] = w
            norm[k] += w * w
            if k == 1:
                length += tf
        return vec, [math.sqrt(x) for x in norm], length

    def score(self, cand, ref):
        vh, nh, lh = self._vec(cand)
        vr, nr, lr = self._vec(ref)
        pen = math.exp(-((lh - lr) ** 2) / (2 * self.sigma ** 2))
        tot = 0.0
        for k in range(self.n):
            v = sum(min(w, vr[k].get(ng, 0.0)) * vr[k].get(ng, 0.0) for ng, w in vh[k].items())
            if nh[k] != 0 and nr[k] != 0:
                v /= nh[k] * nr[k]
            tot += v * pen
        return 10.0 * tot / self.n


def lcs(a, b):
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def rouge_l(c, r, beta=1.2):
    a, b = tok(c), tok(r)
    l = lcs(a, b)
    if l == 0:
        return 0.0
    p, rc = l / len(a), l / len(b)
    return ((1 + beta ** 2) * p * rc) / (rc + beta ** 2 * p)


def bleu_stats(h, r):
    H, R = tok(h), tok(r)
    st = [len(H), len(R)]
    for n in range(1, 5):
        hc = Counter(tuple(H[i:i + n]) for i in range(len(H) - n + 1))
        rc = Counter(tuple(R[i:i + n]) for i in range(len(R) - n + 1))
        st += [sum(min(c, rc[g]) for g, c in hc.items()), max(0, len(H) - n + 1)]
    return st


def bleu_corpus(S):
    hl = sum(s[0] for s in S); rl = sum(s[1] for s in S); lp = 0.0
    for n in range(4):
        m = sum(s[2 + 2 * n] for s in S); t = sum(s[3 + 2 * n] for s in S)
        if m == 0 or t == 0:
            return 0.0
        lp += math.log(m / t) / 4
    return 100 * (1.0 if hl > rl else math.exp(1 - rl / max(hl, 1))) * math.exp(lp)


def nap(p):
    return {(str(d["episode_id"]), str(d["step_id"])): d.get("pred") or "" for d in map(json.loads, open(p, encoding="utf-8"))}


def ktc(pa, pb, ta="A", tb="B", B=1000):
    raw = [json.loads(l) for l in open(f"{KHO}/runs/grpo_spice/score_ck500_test_raw.jsonl", encoding="utf-8")]
    REF = {(str(d["episode_id"]), str(d["step_id"])): d.get("gold_instruction") or "" for d in raw}
    K = sorted(REF)
    A, Bp = nap(pa), nap(pb)
    assert set(K) <= set(A) and set(K) <= set(Bp), "⛔ tệp câu thiếu bước click tập kiểm"
    CID = CiderD([REF[k] for k in K])
    per = {t: {k: (bleu_stats(H[k], REF[k]), rouge_l(H[k], REF[k]), CID.score(H[k], REF[k])) for k in K}
           for t, H in ((ta, A), (tb, Bp))}
    cum = defaultdict(list)
    for k in K:
        cum[k[0]].append(k)
    eps = sorted(cum)
    diem = lambda t, ks: (bleu_corpus([per[t][k][0] for k in ks]),
                          100 * sum(per[t][k][1] for k in ks) / len(ks),
                          100 * sum(per[t][k][2] for k in ks) / len(ks))
    d0 = [x - y for x, y in zip(diem(ta, K), diem(tb, K))]
    rng = random.Random(20261010)
    bs = []
    for _ in range(B):
        ks = [k for e in (rng.choice(eps) for _ in eps) for k in cum[e]]
        bs.append([x - y for x, y in zip(diem(ta, ks), diem(tb, ks))])
    out = {}
    for j, m in enumerate(("bleu4", "rougeL", "cider_d")):
        v = sorted(b[j] for b in bs)
        out[m] = dict(delta=round(d0[j], 2), lo=round(v[int(0.025 * B)], 2), hi=round(v[int(0.975 * B) - 1], 2))
    doi = sum(A[k] != Bp[k] for k in K)
    print(f"{ta} - {tb} - câu khác {doi}/{len(K)} - " + " - ".join(f"{m} {r['delta']:+.2f} [{r['lo']:+.2f}; {r['hi']:+.2f}]" for m, r in out.items()))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a"); ap.add_argument("--b")
    ap.add_argument("--ten-a", default="A"); ap.add_argument("--ten-b", default="B")
    ap.add_argument("--out")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        o = ktc(f"{KHO}/runs/ra304_luat/pred_R3_test.jsonl", f"{KHO}/_scripts/304/ra-sft-script/pred_ck500_test.jsonl", "R3", "ck500")
        assert o["bleu4"] == dict(delta=1.12, lo=0.78, hi=1.45) and o["rougeL"]["delta"] == 0.76 and o["cider_d"]["delta"] == 12.04, o
        print("[tự kiểm] ĐẠT - tái lập đúng 308 §11.1")
    else:
        o = ktc(a.a, a.b, a.ten_a, a.ten_b)
        if a.out:
            json.dump(o, open(a.out, "w"), indent=1)
