# -*- coding: utf-8 -*-
"""Đọc kết quả Kaggle của report 251 (exec cho greedy + 8 mẫu S1 trên 249 bước click C1), CPU + Java 8.

1. Tính lại mọi số của c1_exec_tong.json từ tệp thô (kiểm notebook, không tin JSON).
2. Kiểm tệp thô khớp câu của runs/c1/c1_mau.jsonl.
3. Phép đối chứng hiệu ứng chọn mẫu: oracle SPICE so với chọn ngẫu nhiên một câu KHÁC greedy
   trên cùng các bước đổi câu, và oracle theo các metric câu khác (BLEU-4, ROUGE-L, CIDEr-D).
4. Liên hệ trong cùng bước: câu SPICE cao hơn có bấm trúng hơn không (so cặp trong bước).
Điểm SPICE/BLEU/ROUGE/CIDEr từng câu cache ở runs/c1/exec8/metric_tung_cau.json.
Chạy:  ~/.venvs/thesis/bin/python harness/c1_exec8_doc.py
⚠️ Số val, S1 đã thấy lúc train: không trích ra luận văn.
"""
import glob, json, os, random, math

R0 = "runs/c1"
EX = f"{R0}/exec8"
C1 = [json.loads(l) for l in open(f"{R0}/c1_mau.jsonl", encoding="utf-8")]
PICKS = json.load(open(f"{R0}/c1_picks.json", encoding="utf-8"))["picks"]
n400 = len(C1)
cau = [[d["greedy"]] + d["mau"] for d in C1]

# ---------- metric từng câu (cache) ----------
CACHE = f"{EX}/metric_tung_cau.json"
if not os.path.exists(CACHE):
    J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
    if J and "JAVA_HOME" not in os.environ:
        os.environ["JAVA_HOME"] = J[-1]
        os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    from pycocoevalcap.spice.spice import Spice
    from pycocoevalcap.bleu.bleu import Bleu
    from pycocoevalcap.rouge.rouge import Rouge
    from pycocoevalcap.cider.cider import Cider
    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": d["gold"]}] for i, d in enumerate(C1)})
    M = {m: [] for m in ("spice", "bleu4", "rougeL", "ciderD")}
    for k in range(9):
        c = tk.tokenize({i: [{"caption": cau[i][k]}] for i in range(n400)})
        ids = sorted(g.keys())
        _, s = Spice().compute_score(g, c)
        M["spice"].append([s[j]["All"]["f"] for j in range(len(ids))])
        _, b = Bleu(4).compute_score(g, c, verbose=0)
        M["bleu4"].append(list(b[3]))
        _, r = Rouge().compute_score(g, c)
        M["rougeL"].append(list(map(float, r)))
        _, ci = Cider().compute_score(g, c)
        M["ciderD"].append(list(map(float, ci)))
        print(f"k{k} xong", flush=True)
    json.dump({"ids": ids, **M}, open(CACHE, "w"))
M = json.load(open(CACHE))
ids = M["ids"]
assert ids == list(range(n400))
# kiểm cache SPICE tái lập đúng chuỗi picks
pk2 = "".join(str(max(range(9), key=lambda k: (M["spice"][k][i], -k))) for i in range(n400))
assert pk2 == PICKS, "SPICE từng câu không tái lập c1_picks.json"

# ---------- tệp thô ----------
R = {}
for k in range(9):
    R[k] = {}
    for line in open(f"{EX}/c1score/score_k{k}_raw.jsonl", encoding="utf-8"):
        o = json.loads(line)
        R[k][(o["episode_id"], o["step_id"])] = o
idx = {(d["episode_id"], d["step_id"]): i for i, d in enumerate(C1)}
tap = [(d["episode_id"], d["step_id"]) for d in C1 if (d["episode_id"], d["step_id"]) in R[0]]
assert len(tap) == 249 and all(set(R[k]) == set(tap) for k in range(9))
lech = sum(R[k][q]["sent"] != cau[idx[q]][k] for k in range(9) for q in tap)
lech_gold = sum(R[0][q]["gold_instruction"] != C1[idx[q]]["gold"] for q in tap)
print(f"câu trong tệp thô lệch c1_mau: {lech}/2241 · câu chuẩn lệch: {lech_gold}/249")
assert all(R[k][q]["n_buttons"] > 0 for k in range(9) for q in tap)

ex = lambda k, q: int(R[k][q]["executable"])
n = len(tap)
pct = lambda xs: round(100 * sum(xs) / len(xs), 2)
pick = {q: int(PICKS[idx[q]]) for q in tap}

tong = json.load(open(f"{EX}/c1_exec_tong.json"))
assert pct([ex(0, q) for q in tap]) == tong["exec_greedy"]
assert pct([ex(pick[q], q) for q in tap]) == tong["exec_oracle_spice"]
assert pct([max(ex(k, q) for k in range(9)) for q in tap]) == tong["ti_le_co_it_nhat_1_cau_trung_trong_9"]
print("tính lại từ tệp thô: khớp c1_exec_tong.json")

# McNemar chính xác cho oracle − greedy
b = sum(1 for q in tap if not ex(0, q) and ex(pick[q], q))
c = sum(1 for q in tap if ex(0, q) and not ex(pick[q], q))
def binom_p(b, c):
    m = b + c
    t = sum(math.comb(m, i) for i in range(0, min(b, c) + 1)) / 2 ** m
    return min(1.0, 2 * t)
print(f"oracle SPICE − greedy: +{b} −{c}, McNemar chính xác p={binom_p(b, c):.4f}")

eps = sorted({q[0] for q in tap})
theo_ep = {e: [q for q in tap if q[0] == e] for e in eps}
def ktc(fd, B=10000, seed=101):
    rng = random.Random(seed)
    ds = []
    for _ in range(B):
        qs = [q for e in (rng.choice(eps) for _ in eps) for q in theo_ep[e]]
        ds.append(100 * sum(fd(q) for q in qs) / len(qs))
    ds.sort()
    return [round(ds[int(.025 * B)], 2), round(ds[int(.975 * B) - 1], 2)]

# ---------- oracle theo từng metric ----------
def oracle(m):
    return {q: max(range(9), key=lambda k: (M[m][k][idx[q]], -k)) for q in tap}
print("\noracle theo metric (249 click): exec · Δ so greedy · KTC95 · số bước đổi câu")
for m in ("spice", "bleu4", "rougeL", "ciderD"):
    p = oracle(m)
    d = pct([ex(p[q], q) for q in tap]) - pct([ex(0, q) for q in tap])
    print(f"  {m:7s} {pct([ex(p[q], q) for q in tap]):6.2f}  {d:+5.2f}  {ktc(lambda q: ex(p[q], q) - ex(0, q))}"
          f"  {sum(p[q] != 0 for q in tap)}")
# anti-oracle: câu SPICE thấp nhất
anti = {q: min(range(9), key=lambda k: (M['spice'][k][idx[q]], k)) for q in tap}
print(f"  anti-SPICE (câu SPICE thấp nhất) {pct([ex(anti[q], q) for q in tap]):.2f}")

# ---------- đối chứng hiệu ứng chọn mẫu ----------
doi = [q for q in tap if pick[q] != 0]
e_rand = sum(sum(ex(k, q) for k in range(1, 9)) / 8 for q in doi) / len(doi) * 100
e_rand9 = sum(sum(ex(k, q) for k in range(9)) / 9 for q in tap) / n * 100
print(f"\n119 bước oracle đổi câu: greedy {pct([ex(0, q) for q in doi])} · oracle {pct([ex(pick[q], q) for q in doi])}"
      f" · một mẫu ngẫu nhiên (kỳ vọng) {e_rand:.2f}")
print(f"249 bước: chọn ngẫu nhiên 1 trong 9 câu (kỳ vọng) {e_rand9:.2f}")
# thay oracle bằng 'mẫu ngẫu nhiên' đúng ở các bước oracle đổi câu, giữ greedy chỗ còn lại
e_ctrl = (sum(ex(0, q) for q in tap if pick[q] == 0) + sum(sum(ex(k, q) for k in range(1, 9)) / 8 for q in doi)) / n * 100
print(f"đối chứng 'đổi câu ở đúng 119 bước đó nhưng chọn mẫu ngẫu nhiên': {e_ctrl:.2f}")

# ---------- liên hệ trong cùng bước ----------
# mọi cặp câu (i,j) trong cùng bước có exec khác nhau: câu trúng có SPICE cao hơn bao nhiêu phần
tot = hon = hoa = 0
dspice = []
for q in tap:
    i = idx[q]
    for a in range(9):
        for bb in range(a + 1, 9):
            if ex(a, q) != ex(bb, q):
                t, s = (a, bb) if ex(a, q) else (bb, a)
                st, ss = M["spice"][t][i], M["spice"][s][i]
                tot += 1
                hon += st > ss
                hoa += st == ss
                dspice.append(st - ss)
print(f"\ncặp câu cùng bước, một trúng một trượt: {tot} cặp · câu trúng SPICE cao hơn {100*hon/tot:.1f}%"
      f" · bằng {100*hoa/tot:.1f}% · thấp hơn {100*(tot-hon-hoa)/tot:.1f}%")
dspice.sort()
print(f"  SPICE(trúng) − SPICE(trượt): trung vị {dspice[len(dspice)//2]:+.3f}, TB {sum(dspice)/len(dspice):+.3f}")

# theo hạng SPICE trong bước
for m in ("spice",):
    byrank = [[] for _ in range(9)]
    for q in tap:
        i = idx[q]
        order = sorted(range(9), key=lambda k: (-M[m][k][i], k))
        for r, k in enumerate(order):
            byrank[r].append(ex(k, q))
    print("  exec theo hạng SPICE trong bước (1 = cao nhất):", " ".join(f"{pct(x):.1f}" for x in byrank))

# bước có ít nhất một câu trúng nhưng greedy trượt: oracle SPICE cứu được bao nhiêu
cuu = [q for q in tap if not ex(0, q) and max(ex(k, q) for k in range(9))]
print(f"\ngreedy trượt nhưng có ≥1 câu trúng: {len(cuu)} bước · oracle SPICE cứu {sum(ex(pick[q], q) for q in cuu)}")
