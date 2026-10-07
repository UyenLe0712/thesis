# -*- coding: utf-8 -*-
"""Cổng 0-GPU cho ứng viên R1 (truy hồi câu mẫu theo màn) — đợt tra cứu thứ hai 27/9.

Truy hồi top-k câu chuẩn của TẬP DẠY cho từng bước chạm của tập kiểm, khoá = TF-IDF(token OCR màn +
token goal), có/không bộ lọc "ví dụ phải có từ nội dung xuất hiện trong chữ của màn hiện tại".
Tập dạy và tập kiểm rời nhau theo episode (rò rỉ dạy–kiểm = 0, CLAUDE.md).

Luật đạt ghi TRƯỚC khi chạy:
  M3 (có lọc) ≥ 25%   : trên bước S1 đúng thao tác mà trượt, tỉ lệ có ≥1 câu top-5 chứa từ của tên
                        phần tử vàng mà câu S1 KHÔNG có
  M2 ≥ CIDEr-D của S1 : oracle best-of-5 câu truy hồi, mức kho, cùng 4.463 bước
  M3 có lọc > M3 không lọc
M4 (goal kiểm trùng nguyên văn goal dạy) chỉ để khai; > 10% thì phải báo.
Chạy:  ~/.venvs/thesis/bin/python harness/r1_truy_hoi_0gpu.py   → runs/r1_truy_hoi_0gpu.json
"""
import glob, json, math, os, re, collections
import numpy as np
from scipy import sparse

J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
if J and "JAVA_HOME" not in os.environ:
    os.environ["JAVA_HOME"] = J[-1]; os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.cider.cider import Cider

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
SW = set("the a an on in of to at for and or with from your you this that is it by as into click tap "
         "press select open option button icon go back type enter search then now".split())
w = lambda s: re.findall(r"[a-z0-9]+", (s or "").lower())
cw = lambda s: {t for t in w(s) if t not in SW and len(t) > 1}
K = 5


def rd(p):
    return [json.loads(l) for l in open(R + p, encoding="utf-8")]


def ocr_map(p):
    return {o["image"]: " ".join(it.get("text", "") for it in o.get("items", [])) for o in rd(p)}


tr = rd("harness/dg1_cache/train_ac/train.jsonl")
tr_ocr = ocr_map("harness/dg1_cache/train_ac/ocr.jsonl")
te = {(r["episode_id"], r["step_id"]): r for r in rd("harness/dg1_cache/test_ac/test.jsonl")}
te_ocr = ocr_map("harness/dg1_cache/test_ac/ocr.jsonl")
S1 = [r for r in rd("runs/score_s1_seed101_raw.jsonl")]
DESC = {(d["episode_id"], d["step_id"]): d for d in rd("harness/dg1_cache/test_ac/descriptors.jsonl")}
steps = [(r["episode_id"], r["step_id"]) for r in S1]
print(f"dạy {len(tr)} · kiểm chạm {len(steps)}", flush=True)

# TF-IDF thủ công
docs_tr = [w(tr_ocr.get(r["image"], "")) + w(r["goal"]) for r in tr]
docs_te = [w(te_ocr.get(te[k]["image"], "")) + w(te[k]["goal"]) for k in steps]
df = collections.Counter(t for d in docs_tr for t in set(d))
voc = {t: i for i, t in enumerate(df)}
N = len(docs_tr)
idf = np.array([math.log((1 + N) / (1 + df[t])) + 1 for t in voc], dtype=np.float32)


def mat(docs):
    rows, cols, vals = [], [], []
    for i, d in enumerate(docs):
        c = collections.Counter(t for t in d if t in voc)
        for t, n in c.items():
            rows.append(i); cols.append(voc[t]); vals.append(n * idf[voc[t]])
    m = sparse.csr_matrix((vals, (rows, cols)), shape=(len(docs), len(voc)), dtype=np.float32)
    nrm = np.sqrt(m.multiply(m).sum(1)).A1 + 1e-9
    return sparse.diags(1 / nrm) @ m


Dm, Qm = mat(docs_tr), mat(docs_te)
top = []
for s in range(0, len(steps), 300):
    sim = (Qm[s:s + 300] @ Dm.T).toarray()
    top.extend(np.argsort(-sim, axis=1)[:, :50].tolist())
print("truy hồi xong", flush=True)

def chon(i, loc):
    scr = cw(te_ocr.get(te[steps[i]]["image"], ""))
    out = []
    for j in top[i]:
        c = tr[j]["target_instruction"]
        if loc and not (cw(c) & scr):
            continue
        out.append(c)
        if len(out) == K:
            break
    while len(out) < K:
        out.append(tr[top[i][len(out)]]["target_instruction"])
    return out

res = {}
tk = PTBTokenizer()
gold = [te[k]["gold_instruction"] for k in steps]
g = tk.tokenize({i: [{"caption": x}] for i, x in enumerate(gold)})
s1t = tk.tokenize({i: [{"caption": (r.get("sent") or "")}] for i, r in enumerate(S1)})
ci_s1, per_s1 = Cider().compute_score(g, s1t)
res["S1_cider"] = round(100 * ci_s1, 2)
res["S1_bleu4"] = round(100 * Bleu(4).compute_score(g, s1t, verbose=0)[0][3], 2)
goals_tr = {r["goal"].strip().lower() for r in tr}
res["M4_goal_trung_nguyen_van_%"] = round(100 * sum(te[k]["goal"].strip().lower() in goals_tr for k in steps) / len(steps), 2)

for loc in (False, True):
    ten = "co_loc" if loc else "khong_loc"
    C = [chon(i, loc) for i in range(len(steps))]
    cand = [tk.tokenize({i: [{"caption": C[i][k]}] for i in range(len(steps))}) for k in range(K)]
    per = [list(Cider().compute_score(g, c)[1]) for c in cand]
    t1 = cand[0]
    best = {i: cand[max(range(K), key=lambda k: per[k][i])][i] for i in range(len(steps))}
    o = {"M1_top1_cider": round(100 * Cider().compute_score(g, t1)[0], 2),
         "M1_top1_bleu4": round(100 * Bleu(4).compute_score(g, t1, verbose=0)[0][3], 2),
         "M2_best5_cider": round(100 * Cider().compute_score(g, best)[0], 2),
         "M2_best5_bleu4": round(100 * Bleu(4).compute_score(g, best, verbose=0)[0][3], 2)}
    miss = [i for i, r in enumerate(S1) if r.get("action_ok") == 1 and r.get("executable") == 0]
    hit = 0; nm_n = 0
    for i in miss:
        nm = cw(DESC.get(steps[i], {}).get("name"))
        if not nm:
            continue
        nm_n += 1
        thieu = nm - cw(S1[i].get("sent"))
        hit += any(cw(c) & thieu for c in C[i])
    o["M3_%"] = round(100 * hit / nm_n, 2); o["M3_n"] = nm_n
    # đối chứng: câu top-5 NGẪU NHIÊN từ tập dạy (sàn của M3)
    rng = np.random.default_rng(0); hr = 0
    for i in miss:
        nm = cw(DESC.get(steps[i], {}).get("name"))
        if not nm:
            continue
        thieu = nm - cw(S1[i].get("sent"))
        hr += any(cw(tr[j]["target_instruction"]) & thieu for j in rng.integers(0, N, K))
    o["M3_san_ngau_nhien_%"] = round(100 * hr / nm_n, 2)
    res[ten] = o
    print(ten, o, flush=True)

lk, ll = res["khong_loc"], res["co_loc"]
res["luat"] = {"M3 co loc >= 25%": ll["M3_%"] >= 25,
               "M2 (co loc) >= CIDEr S1": ll["M2_best5_cider"] >= res["S1_cider"],
               "M3 co loc > khong loc": ll["M3_%"] > lk["M3_%"]}
res["R1"] = "DAT" if all(res["luat"].values()) else "KHONG DAT"
json.dump(res, open(R + "runs/r1_truy_hoi_0gpu.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
