# 298: chấm CHÍNH THỨC hai cột còn thiếu của RAF trên test 4.463 click — METEOR 1.5 và BERTScore — chạy trên WSL.
# SPICE của RAF đã có số chính xác (+0,53 [+0,03; +0,99], ghép từ điểm SPICE từng câu) → mặc định KHÔNG chạy SPICE.
# Ba chế độ:
#   mặc định        : METEOR (cần Java 8 ở ~/.jdk, qua pycocoevalcap) + BERTScore + chrF
#   --bo-meteor     : KHÔNG cần Java — chỉ BERTScore + chrF (METEOR khi đó dùng số proxy Python đã có)
#   --co-spice      : thêm SPICE (Java, chậm) — chỉ để đối chiếu, không bắt buộc
# Chạy từ GỐC KHO trên WSL:
#   ~/.venvs/thesis/bin/python cham_raf_wsl_298.py --raf raw_G4g_test.jsonl [--bo-meteor] [--bo-bert] [--co-spice]
# (chép nguyên văn từ ảnh 298_ACTION_CHOT_RAF_7_10.md §5, bản Mac 7/10/2026)
import argparse, glob, json, os, random, sys

ap = argparse.ArgumentParser()
ap.add_argument("--raf", required=True)
ap.add_argument("--goc", default="runs/grpo_spice/score_ck500_test_raw.jsonl")
ap.add_argument("--s1", default="runs/score_s1_seed101_raw.jsonl")
ap.add_argument("--B", type=int, default=2000)
ap.add_argument("--bo-meteor", action="store_true")
ap.add_argument("--bo-bert", action="store_true")
ap.add_argument("--co-spice", action="store_true")
ap.add_argument("--out", default="cham_raf_wsl_298.json")
a = ap.parse_args()
can_java = (not a.bo_meteor) or a.co_spice
if can_java:
    J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
    if J:
        os.environ["JAVA_HOME"] = J[-1]; os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]
sys.path.insert(0, "harness")
import sacrebleu


def nap(p):
    return {(int(r["episode_id"]), int(r["step_id"])): r for r in map(json.loads, open(p, encoding="utf-8"))}


F = {"RAF": nap(a.raf), "ck500": nap(a.goc), "S1": nap(a.s1)}
K = sorted(F["ck500"])
assert all(set(F[t]) == set(K) for t in F) and len(K) == 4463
REF = [(F["ck500"][k].get("gold_instruction") or "").strip() for k in K]   # quy ước harness/text_metrics.load
for t in F:
    assert [(F[t][k].get("gold_instruction") or "").strip() for k in K] == REF, t
HYP = {t: [(F[t][k].get("sent") or "").strip() for k in K] for t in F}
assert sum(h != c for h, c in zip(HYP["RAF"], HYP["ck500"])) <= 724

out, per = {t: {} for t in F}, {t: {} for t in F}
for t in F:
    out[t]["chrf"] = sacrebleu.CHRF().corpus_score(HYP[t], [REF]).score

if can_java:
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    tk = PTBTokenizer()
    G = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(REF)})
    for t in F:
        C = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(HYP[t])})
        if not a.bo_meteor:
            from pycocoevalcap.meteor.meteor import Meteor
            m, ms = Meteor().compute_score(G, C)
            out[t]["meteor"], per[t]["meteor"] = 100 * m, [100 * x for x in ms]
        if a.co_spice:
            from pycocoevalcap.spice.spice import Spice
            s, ss = Spice().compute_score(G, C)
            out[t]["spice"], per[t]["spice"] = 100 * s, [100 * x["All"]["f"] for x in ss]

if not a.bo_bert:
    import text_metrics_them as TM
    for t in F:
        out[t]["bertscore"] = TM.tinh(HYP[t], REF, bert=True)["bertscore_f1_rescaled"]
        _, _, f2 = TM.SC.score(HYP[t], REF)
        per[t]["bertscore"] = [0.0 if not h else 100 * x for h, x in zip(HYP[t], f2.tolist())]

for t in F:
    print(t, {x: round(v, 2) for x, v in out[t].items()}, flush=True)
print("đối chiếu số công bố: S1 METEOR 36,79 · BERTScore 66,33 · chrF 61,26 | ck500 METEOR 37,92 · BERTScore 67,07 · chrF 62,87")

by = {}
for i, k in enumerate(K):
    by.setdefault(k[0], []).append(i)
eps = sorted(by)
rnd = random.Random(0)
samp = [[i for e in (rnd.choice(eps) for _ in eps) for i in by[e]] for _ in range(a.B)]
ci = {}
for x in per["RAF"]:
    d = [u - v for u, v in zip(per["RAF"][x], per["ck500"][x])]
    bs = sorted(sum(d[i] for i in s) / len(s) for s in samp)
    ci[x] = (out["RAF"][x] - out["ck500"][x], bs[int(.025 * a.B)], bs[int(.975 * a.B)])
bs = sorted(sacrebleu.CHRF().corpus_score([HYP["RAF"][i] for i in s], [[REF[i] for i in s]]).score
            - sacrebleu.CHRF().corpus_score([HYP["ck500"][i] for i in s], [[REF[i] for i in s]]).score for s in samp[:1000])
ci["chrf"] = (out["RAF"]["chrf"] - out["ck500"]["chrf"], bs[25], bs[974])
print("\nRAF − ck500 (KTC95 bootstrap theo tác vụ; METEOR/BERTScore: Δ số tổng, KTC trên trung bình câu):")
for x, (d, lo, hi) in ci.items():
    print(f"  {x:10s} {d:+.2f} [{lo:+.2f}; {hi:+.2f}]")
json.dump({"tong": out, "ktc_RAF_ck500": ci}, open(a.out, "w"), ensure_ascii=False, indent=1)
print(f"→ {a.out}")
