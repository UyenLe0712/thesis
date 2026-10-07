import glob, json, os, sys, statistics
J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
if J:
    os.environ["JAVA_HOME"] = J[-1]; os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.cider.cider import Cider
from scipy.stats import spearmanr

R = "/mnt/d/Master/Thesis/"
BR = [("S1/101", "runs/score_s1_seed101_raw.jsonl"), ("S1/202", "runs/score_s1_seed202_raw.jsonl"),
      ("S2", "runs/score_s2_seed101_raw.jsonl"), ("CE2", "runs/score_ce2_s2_seed101_raw.jsonl"),
      ("MIN", "runs/score_min_desc_seed101_raw.jsonl"), ("gui_sel", "runs/sel/score_gui_sel_seed101_raw.jsonl"),
      ("GRPO", "runs/grpo_point/score_grpo_point_seed101_raw.jsonl")]
rows = {n: [json.loads(l) for l in open(R + p)] for n, p in BR}
names = [n for n, _ in BR]
N = 4463
key0 = [(r["episode_id"], r["step_id"]) for r in rows["S1/101"]]
for n in names:
    assert [(r["episode_id"], r["step_id"]) for r in rows[n]] == key0, n
ref = [(r["gold_instruction"] or "").strip() for r in rows["GRPO"]]
hyp = {n: [(r.get("sent") or "").strip() for r in rows[n]] for n in names}
ex = {n: [r.get("executable", 0) for r in rows[n]] for n in names}

tk = PTBTokenizer()
g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(ref)})
ht = {n: tk.tokenize({i: [{"caption": h}] for i, h in enumerate(hyp[n])}) for n in names}

def corpus(pick):
    c = {i: ht[pick[i]][i] for i in range(N)}
    b, _ = Bleu(4).compute_score(g, c, verbose=0)
    ci, _ = Cider().compute_score(g, c)
    e = 100 * statistics.mean(ex[pick[i]][i] for i in range(N))
    return round(100 * b[3], 2), round(100 * ci, 2), round(e, 2)

per = {}
for n in names:
    s, arr = Cider().compute_score(g, ht[n])
    per[n] = list(arr)
    print(f"{n:8s} corpus BLEU4/CIDEr/exec = {corpus([n]*N)}", flush=True)

def oracle(sub):
    return [max(sub, key=lambda n: (per[n][i], n == "S1/101")) for i in range(N)]

print("oracle best-of-2 (S1/101,S1/202):", corpus(oracle(["S1/101", "S1/202"])))
print("oracle best-of-7:", corpus(oracle(names)))

# MBR: tiện ích = CIDEr-D của câu i so với 6 câu còn lại làm tham chiếu
mbr = {}
for n in names:
    refs = {i: [ht[m][i][0] for m in names if m != n] for i in range(N)}
    _, arr = Cider().compute_score(refs, ht[n])
    mbr[n] = list(arr)
pick = [max(names, key=lambda n: (mbr[n][i], n == "S1/101")) for i in range(N)]
print("MBR chéo 7 nhánh:", corpus(pick))
xs = [mbr[n][i] for n in names for i in range(N)]
ys = [per[n][i] for n in names for i in range(N)]
print("Spearman(MBR, CIDEr thật) =", round(spearmanr(xs, ys).correlation, 3))
same2 = sum(hyp["S1/101"][i] == hyp["S1/202"][i] for i in range(N)) / N
all7 = sum(len({hyp[n][i] for n in names}) == 1 for i in range(N)) / N
print(f"S1/101 == S1/202 nguyên văn: {100*same2:.1f}%  · cả 7 giống hệt: {100*all7:.1f}%")
from collections import Counter
print("MBR chọn nhánh:", Counter(pick).most_common())
