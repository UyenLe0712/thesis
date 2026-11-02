# Đo hình thức câu test (trùng số trong report/330 mục 1): chạy từ thư mục runs/
import json,re,collections
def tok(s): return re.findall(r"[a-z0-9']+",(s or "").lower())
BAD={"a","an","the","of","in","on","at","to","with","and","for","from","by","or","is","are"}
ck=[json.loads(l) for l in open("grpo_spice/pred_ck500_test.jsonl")]; tgt={(r["episode_id"],r["step_id"]) for r in ck}
def stat(name,S):
    n=len(S);L=[tok(x) for x in S]
    rb=sum(any(c>1 for c in collections.Counter(zip(t,t[1:])).values()) for t in L)
    be=sum(1 for t in L if t and t[-1] in BAD)
    print(name,n,"từ %.2f lặp bigram %.2f%% kết thúc hư từ %.2f%%"%(sum(map(len,L))/n,100*rb/n,100*be/n))
g=[json.loads(l) for l in open("preds_s1_seed101.jsonl")]; g=[r for r in g if (r["episode_id"],r["step_id"]) in tgt]
stat("gold",[r["gold_instruction"] for r in g]);stat("S1",[r["pred"] for r in g]);stat("ck500",[r["pred"] for r in ck])
for p in ("A2_500","A2_1000"):
    stat(p,[json.loads(l)["pred"] for l in open(f"a2_test299/pred_{p}_test.jsonl")])
