# -*- coding: utf-8 -*-
"""Truy hồi ví dụ quỹ đạo cho sinh câu hướng dẫn (RA-SFT · RA-GRPO · sinh val/test).

Đích dán đề xuất: thesis-master/harness/ra_exemplars.py (người dùng tự chép và commit).
Kho = bước train (train_tru_val.jsonl) đã loại mọi tác vụ val; truy vấn chỉ dùng mục tiêu + lịch sử (đầu vào).
Hai khoá, hợp lại rồi khử trùng câu:
  R1 mức bước (kiểu SmallCap): TF-IDF trên (mục tiêu + câu lịch sử cuối, tiền tố H_).
  R2 mức quỹ đạo (kiểu Synapse): TF-IDF trên mục tiêu → tác vụ gần nhất, căn bước theo câu-trước = câu lịch sử cuối.
Lúc dạy: bỏ chính tác vụ (leave-one-episode-out), c-sample-k + xáo thứ tự (RobustCap), k ngẫu nhiên 2..6,
15% bỏ khối, 10% ví dụ ngẫu nhiên, bỏ ví dụ trùng câu chuẩn với xác suất q để tỉ lệ khớp lúc dạy ≈ lúc chấm.
Lúc chấm: cố định, k=4, xếp theo số lần xuất hiện → độ phủ OCR → hạng.
"""
import math, re, random, heapq
from collections import Counter, defaultdict

PUNCT = {"''", '""', "``", "`", "-lrb-", "-rrb-", "-lcb-", "-rcb-", ".", "?", "!", ",", ":", "_", "--", "...", ";"}
TOK = re.compile(r"n't|'s|'re|'ve|'ll|'d|'m|[a-z0-9]+(?:[-./][a-z0-9]+)*|[^\sa-z0-9]")
FUNC = set("click tap select open press choose go type enter on the a an at of to in for and or from with by is be as "
           "into it its this that then next now please screen top bottom left right corner side middle center centre "
           "icon button option options tab bar field text page menu above below near beside under up down first "
           "second third last".split())
HEADER = "Ví dụ bước tương tự từ tác vụ khác (có thể không khớp màn này):"
LAST = "Viết câu hướng dẫn cho bước tiếp theo."

def tok(s):
    s = (s or "").lower().replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'")
    s = re.sub(r"(\w)n't\b", r"\1 n't", s)
    return [t for t in TOK.findall(s) if t not in PUNCT and t != ""]

def _tfidf(docs):
    df = Counter(w for d in docs for w in set(d))
    idf = {w: math.log(len(docs) / c) for w, c in df.items()}
    inv = defaultdict(list)
    for i, d in enumerate(docs):
        v = {w: tf * idf[w] for w, tf in Counter(d).items()}
        n = math.sqrt(sum(x * x for x in v.values())) or 1.0
        for w, x in v.items():
            inv[w].append((i, x / n))
    return idf, inv

def _q(idx, q, k):
    idf, inv = idx
    v = {w: tf * idf.get(w, 0.0) for w, tf in Counter(q).items()}
    n = math.sqrt(sum(x * x for x in v.values())) or 1.0
    sc = defaultdict(float)
    for w, x in v.items():
        for i, y in inv.get(w, ()):
            sc[i] += x / n * y
    return heapq.nlargest(k, sc.items(), key=lambda t: t[1])

def _jacc(a, b):
    a, b = set(tok(a)), set(tok(b))
    return len(a & b) / max(1, len(a | b))

def _hlast(x):
    h = x.get("history") or []
    return h[-1] if h else "<start>"

class Kho:
    def __init__(self, recs, loai_ep=()):
        bo = set(loai_ep)
        self.tr = [t for t in recs if t["episode_id"] not in bo and (t.get("target_instruction") or "").strip()]
        self.idx1 = _tfidf([self._k1(t) for t in self.tr])
        self.eps = defaultdict(dict)
        for t in self.tr:
            self.eps[t["episode_id"]][t["step_id"]] = t
        self.eid = sorted(self.eps)
        self.idx2 = _tfidf([tok(next(iter(self.eps[e].values()))["goal"]) for e in self.eid])
        self.click = [i for i, t in enumerate(self.tr) if (t.get("action") or {}).get("action_type") == "click"]

    @staticmethod
    def _k1(x):
        return tok(x["goal"]) + ["H_" + w for w in tok(_hlast(x))]

    def _e(self, t):
        return dict(sent=t["target_instruction"].strip(), goal=t["goal"], prev=_hlast(t))

    def r1(self, x, k, own):
        out = []
        for i, _ in _q(self.idx1, self._k1(x), 4 * k + 12):
            if self.tr[i]["episode_id"] != own:
                out.append(self._e(self.tr[i]))
                if len(out) == k:
                    break
        return out

    def r2(self, x, m, own):
        h, out = x.get("history") or [], []
        for i, _ in _q(self.idx2, tok(x["goal"]), m + 3):
            if self.eid[i] == own:
                continue
            st = self.eps[self.eid[i]]
            if not h:
                j = min(st)
            else:
                c = [(_jacc(st[s - 1]["target_instruction"], h[-1]), -abs(s - len(h)), s) for s in st if s - 1 in st]
                if not c:
                    continue
                j = max(c)[2]
            out.append(self._e(st[j]))
            if len(out) == m:
                break
        return out

    def pool(self, x, own=None, n1=8, n2=8):
        """Hợp R1∪R2, khử trùng theo câu đã token hoá; cnt = số lần câu xuất hiện trong hai danh sách thô."""
        seen, out = {}, []
        for r, e in enumerate(self.r1(x, n1, own) + self.r2(x, n2, own)):
            key = " ".join(tok(e["sent"]))
            if key in seen:
                seen[key]["cnt"] += 1
                continue
            seen[key] = dict(e, cnt=1, rank=r % max(n1, n2))
            out.append(seen[key])
        return out

    def cho_test(self, x, k=4, ocr_tokens=None, own=None):
        """Cố định (không ngẫu nhiên). own = tác vụ của chính câu nhắc khi dùng cho câu nhắc TRAIN (GRPO)."""
        P = self.pool(x, own, 4, 4)
        def phu(e):
            c = [w for w in tok(e["sent"]) if w not in FUNC and len(w) > 1]
            return float(bool(c) and ocr_tokens is not None and all(w in ocr_tokens for w in c))
        return sorted(P, key=lambda e: (-e["cnt"], -phu(e), e["rank"]))[:k]

    def cho_train(self, x, gold, own, rng, q_trung=0.0, kmin=2, kmax=6, N=12, p_rong=0.15, p_ngau=0.10):
        u = rng.random()
        if u < p_rong:
            return None
        k = rng.randint(kmin, kmax)
        if u < p_rong + p_ngau:
            cand = [self.tr[i] for i in rng.sample(self.click, 4 * k) if self.tr[i]["episode_id"] != own]
            return [self._e(t) for t in cand[:k]]
        P = self.pool(x, own)[:N]
        g = tok(gold)
        if q_trung and any(tok(e["sent"]) == g for e in P) and rng.random() < q_trung:
            P = [e for e in P if tok(e["sent"]) != g]
        if not P:
            return None
        out = [P[0]] + rng.sample(P[1:], min(k - 1, len(P) - 1))
        rng.shuffle(out)
        return out

def khoi(exs, goal_words=12):
    if not exs:
        return ""
    L = [HEADER]
    for i, e in enumerate(exs, 1):
        prev = "(bước đầu)" if e["prev"] == "<start>" else e["prev"].strip()
        L.append(f"{i}. Mục tiêu: {' '.join(e['goal'].split()[:goal_words])} | Bước trước: {prev} | "
                 f"Bước kế: {e['sent']}")
    return "\n".join(L)

def chen(body, exs):
    """Chèn khối ngay trước dòng cuối của prompt_body; phần trước giữ nguyên từng byte như câu nhắc của S1."""
    b = khoi(exs)
    if not b:
        return body
    assert body.endswith(LAST), "prompt_body đổi dòng cuối - sửa LAST"
    return body[:-len(LAST)] + b + "\n" + LAST
