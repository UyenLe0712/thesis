# 296-R: DỰNG tệp thô câu lai G4g trên tập kiểm 4.463 click — luật ĐÃ ĐÓNG BĂNG trên val lớn:
#   (1) câu S1/101 ≠ câu ck500 sau token hoá; (2) cùng lớp thao tác canon_action; (3) đồng thuận với 4 câu bước-kề của
#   4 quỹ đạo train có mục tiêu gần nhất (R2 kiểu Synapse, m=4), điểm = TB CIDEr-D(câu, câu truy hồi) với df từ câu TRAIN;
#   lùi về S1 nếu điểm S1 > điểm ck500 (biên 0; hoà → ck500).
#   CHƯA CHẠY. Chỉ chạy khi người dùng đồng ý chấm test MỘT lần. Quyết định lùi KHÔNG đọc câu chuẩn: chỉ đọc
#   goal/history của test.jsonl và trường `sent` của hai tệp thô; hàng ghi ra là hàng thô nguyên vẹn của S1/101 hoặc ck500.
# (chép từ 2 ảnh màn hình Mac 7/10/2026. Khác bản Mac đúng hai chỗ:
#   · bản Mac exec phần đầu `_scripts/296/do_296_vallon.py` để lấy `tok` + `CiderD`; tệp đó không có trên WSL nên lấy
#     từ harness/ctg_grpo.py (CIDEr-D chép nguyên văn Phụ lục A của 276, cùng giao diện CiderD(list).score(câu, refs));
#     ⚠️ CiderD.score của ctg_grpo nhận list ⇒ bọc lớp con nhận MỘT câu như bản Mac gọi;
#   · đường dẫn "thesis-master/…" đổi thành tương đối từ gốc kho.)
# Chạy từ GỐC KHO trên WSL:  ~/.venvs/thesis/bin/python _scripts/296/do_296_R_test_lai.py
import json, math, os, statistics as st, sys
from collections import defaultdict, Counter

sys.path.insert(0, "harness")
from ctg_grpo import tok, CiderD as _CiderD


class CiderD(_CiderD):
    # bản Mac gọi score(câu, MỘT câu tham chiếu); CiderD của ctg_grpo nhận DANH SÁCH tham chiếu ⇒ bọc lại.
    # (không bọc thì chuỗi bị duyệt từng ký tự, 1.299/1.351 cặp ra 0 = hoà, chỉ 19 bước lùi — đã gặp 7/10)
    def score(self, cand, ref):
        return super().score(cand, [ref])
from metric_exec import canon_action

R = "runs/"
kk = lambda e, s: (int(e), int(s))
doc = lambda p: {kk(x["episode_id"], x["step_id"]): x for x in map(json.loads, open(p, encoding="utf-8"))}
RS1, RCK = doc(R + "score_s1_seed101_raw.jsonl"), doc(R + "grpo_spice/score_ck500_test_raw.jsonl")
KK = sorted(RCK)
assert set(RS1) == set(KK) and len(KK) == 4463
INP = {}
for l in open("harness/dg1_cache/test_ac/test.jsonl", encoding="utf-8"):
    x = json.loads(l)
    k = kk(x["episode_id"], x["step_id"])
    if k in RCK:
        INP[k] = {"goal": x["goal"], "history": x.get("history") or []}
assert set(INP) == set(KK)

tr = [json.loads(l) for l in open("harness/dg1_cache/train_ac/train_tru_val.jsonl", encoding="utf-8")]
tr = [t for t in tr if t.get("target_instruction")]


def tfidf(docs):
    df = Counter(w for d in docs for w in set(d))
    N = len(docs)
    idf = {w: math.log(N / c) for w, c in df.items()}
    inv = defaultdict(list)
    for i, d in enumerate(docs):
        v = {w: tf * idf[w] for w, tf in Counter(d).items()}
        n = math.sqrt(sum(x * x for x in v.values())) or 1.0
        for w, x in v.items():
            inv[w].append((i, x / n))
    return idf, inv


def query(idx, q, k):
    idf, inv = idx
    v = {w: tf * idf.get(w, 0.0) for w, tf in Counter(q).items()}
    n = math.sqrt(sum(x * x for x in v.values())) or 1.0
    sc = defaultdict(float)
    for w, x in v.items():
        for i, y in inv.get(w, ()):
            sc[i] += x / n * y
    return sorted(sc, key=lambda i: -sc[i])[:k]


eps = defaultdict(dict)
for t in tr:
    eps[t["episode_id"]][t["step_id"]] = t
eid = sorted(eps)
goal_of = {e: next(iter(eps[e].values()))["goal"] for e in eid}
idx2 = tfidf([tok(goal_of[e]) for e in eid])


def jacc(a, b):
    a, b = set(tok(a)), set(tok(b))
    return len(a & b) / max(1, len(a | b))


def r2(x, m=4):
    h = x["history"]
    out = []
    for i in query(idx2, tok(x["goal"]), m):
        st_ = eps[eid[i]]
        if not h:
            j = min(st_)
        else:
            cand = [(jacc(st_[s - 1]["target_instruction"], h[-1]), -abs(s - len(h)), s) for s in st_ if s - 1 in st_]
            if not cand:
                continue
            j = max(cand)[2]
        out.append(st_[j]["target_instruction"])
    return out


cd_tr = CiderD([t["target_instruction"] for t in tr])
gate = set()
for k in KK:
    s1, ck = RS1[k].get("sent") or "", RCK[k].get("sent") or ""
    if tok(s1) == tok(ck) or canon_action(s1) != canon_action(ck):
        continue
    ret = r2(INP[k])
    if ret and st.mean(100 * cd_tr.score(s1, r) for r in ret) > st.mean(100 * cd_tr.score(ck, r) for r in ret) + 1e-9:
        gate.add(k)
os.makedirs("_scripts/296/lai_test", exist_ok=True)
with open("_scripts/296/lai_test/raw_G4g_test.jsonl", "w", encoding="utf-8") as f:
    for k in KK:
        f.write(json.dumps((RS1 if k in gate else RCK)[k], ensure_ascii=False) + "\n")
json.dump(sorted(gate), open("_scripts/296/lai_test/cong_G4g_test.json", "w"))
print(f"G4g lùi về S1 ở {len(gate)}/{len(KK)} bước → _scripts/296/lai_test/raw_G4g_test.jsonl")
