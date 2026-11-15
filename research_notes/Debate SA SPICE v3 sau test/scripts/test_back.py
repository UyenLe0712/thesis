import json, sys, collections
sys.path.insert(0, "/mnt/d/Master/Thesis/harness")
import sa3_action_verify as V
from sa3_reward_screen import rewards, k_gold, penalty
import sacrebleu
from h4_spice_tuple_7_11 import spice_chi_tiet
T="/mnt/d/Master/Thesis/runs/sa_spice_v3/test/"
G={}
for l in open("/mnt/d/Master/Thesis/harness/dg1_cache/test_ac/test.jsonl"):
    d=json.loads(l)
    if d["action"]["action_type"]=="navigate_back": G[(d["episode_id"],d["step_id"])]=d["gold_instruction"]
P={}
for name in ["sa_ck400","sftcont"]:
    P[name]={ (d["episode_id"],d["step_id"]):d["pred"] for d in map(json.loads, open(T+f"pred_{name}_test_nontap.jsonl"))}
keys=sorted(k for k in G if k in P["sa_ck400"])
print("back test", len(keys))
probe=[("Go back to the previous page","Go back to the previous page"),("Go back","Go back"),("Go back to the previous page","Go back to the previous page."),("Go back to the previous screen","Go back to the previous page"),("Click on the close icon at the top right corner","Go back to the previous page"),("Click on the screen","Go back to the previous page")]
hyp=[p for p,_ in probe]; ref=[g for _,g in probe]
for k in keys:
    for n in ["sa_ck400","sftcont"]:
        hyp.append(P[n][k] or "x"); ref.append(G[k])
res=spice_chi_tiet(hyp, ref)
def R(y,g,o):
    s=float(o["scores"]["All"]["f"]); K=k_gold(o["ref"]); c=sacrebleu.sentence_chrf(y,[g]).score/100
    A,_=V.score_action(y,g,"navigate_back")
    rr=rewards(y,g,s,c,0,0,A,K)
    # variants
    A1=A
    if V.trusted(g,"navigate_back") and V.classify(y) not in (None,"back"): A1=0.0
    d=penalty(y,g); al=0.8*min(1,K/3)
    clip=lambda x:min(1,max(0,x))
    v1=clip(0.8*(al*s+(1-al)*c)+0.2*A1-d)
    v3=clip(0.8*(0.5*s+0.5*c)+0.2*A1-d)
    return dict(s=s,c=c,K=K,A=A,SA=rr["SA-SPICE-v3"],chrF=rr["chrF"],SPICE=rr["SPICE-MATCH"],V1=v1,V3=v3)
for i,(p,g) in enumerate(probe):
    print(repr(p),"vs",repr(g), {k:round(v,3) for k,v in R(p,g,res[i]).items()})
out=[]
j=len(probe)
agg=collections.defaultdict(list)
for k in keys:
    rs={}
    for n in ["sa_ck400","sftcont"]:
        y=hyp[j]; rs[n]=(y,R(y,G[k],res[j]),V.classify(y)); j+=1
    out.append((k,G[k],rs))
    cs,cf=rs["sa_ck400"][2],rs["sftcont"][2]
    grp="pha" if (cf=="back" and cs!="back") else ("cuu" if (cs=="back" and cf!="back") else ("ca2dung" if cs==cf=="back" else "ca2sai"))
    for n in ["sa_ck400","sftcont"]:
        for m,v in rs[n][1].items():
            agg[(grp,n,m)].append(v)
print(collections.Counter(g for g,n,m in agg if n=="sa_ck400" and m=="SA"))
for grp in ["pha","cuu","ca2dung","ca2sai"]:
    if (grp,"sa_ck400","SA") not in agg: continue
    n=len(agg[(grp,"sa_ck400","SA")])
    print(grp,n, " | ".join(f"{m}: SFT {sum(agg[(grp,'sftcont',m)])/n:.3f} SA {sum(agg[(grp,'sa_ck400',m)])/n:.3f}" for m in ["s","c","SA","V1","V3","chrF"]))
json.dump([[list(k),g,{n:[v[0],v[1],v[2]] for n,v in rs.items()}] for k,g,rs in out], open("test_back_rewards.json","w"),ensure_ascii=False)
