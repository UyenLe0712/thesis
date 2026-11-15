import json, sys, collections, statistics as st
sys.path.insert(0, "/mnt/d/Master/Thesis/harness")
import sa3_action_verify as V
from sa3_reward_screen import penalty
R="/mnt/d/Master/Thesis/runs/sa_spice_v3/"
rows={ (r["episode_id"],r["step_id"]):r for r in map(json.loads, open(R+"split/train_v3.jsonl"))}
M={}
for i in (0,1):
    for l in open(R+f"mau_k1/mau_{i}.jsonl"):
        d=json.loads(l); M[(d["episode_id"],d["step_id"])]=d
S={}
for l in open(R+"screen/out/sa3_screen_buoc.jsonl"):
    d=json.loads(l); S[(d["episode_id"],d["step_id"])]=d["R"]
clip=lambda x:min(1,max(0,x))
CLS={"navigate_back":"back","scroll":"scroll","open_app":"open_app","input_text":"type"}
def recover(y,g,x):
    d=penalty(y,g); s=(x["R"]["SPICE-MATCH"]-0.1+d)/0.8; c=x["R"]["chrF"]+d
    S_=(x["R"]["SA-SPICE-v3"]+d-0.2*x["A"])/0.8
    return s,c,d,S_
def arms(y,g,at,x,al):
    s,c,d,_=recover(y,g,x); A=x["A"]
    if not y.strip(): return dict(SA=0,T=0,T50=0,G=0)
    mis = V.trusted(g,at) and CLS.get(at) in ("back","scroll") and V.classify(y) not in (None, CLS[at])
    AT = 0.0 if mis else A
    SA=clip(0.8*(al*s+(1-al)*c)+0.2*A-d)
    T=clip(0.8*(al*s+(1-al)*c)+0.2*AT-d)
    T50=clip(0.8*(0.5*s+0.5*c)+0.2*AT-d)
    G=0.0 if mis else SA     # cổng cứng
    return dict(SA=SA,T=T,T50=T50,G=G)
def adv(Rs):
    m=sum(Rs)/len(Rs); sd=st.stdev(Rs); return [(r-m)/(sd+1e-4) for r in Rs]
for at in ["navigate_back","scroll"]:
    want=CLS[at]; res=collections.defaultdict(lambda: collections.defaultdict(list)); conc=collections.Counter(); npair=0
    for k,r in rows.items():
        if r["action"]["action_type"]!=at: continue
        g=r["target_instruction"]; ys=M[k]["mau"]; X=S[k][1:]
        # recover alpha from any sample with s!=c
        al=None
        for y,x in zip(ys,X):
            s,c,d,S_=recover(y,g,x)
            if abs(s-c)>0.05 and 0<x["R"]["SA-SPICE-v3"]<1: al=(S_-c)/(s-c); break
        al = min([0,0.8/3,1.6/3,0.8], key=lambda a: abs(a-(al if al is not None else 0)))
        ok=[V.classify(y)==want for y in ys]
        if all(ok) or not any(ok): continue
        RR={a:[arms(y,g,at,x,al)[a] for y,x in zip(ys,X)] for a in ["SA","T","T50","G"]}
        for a,Rs in RR.items():
            for i in range(8):
                for j in range(8):
                    if ok[i] and not ok[j]:
                        conc[a]+= (Rs[i]>Rs[j]) + 0.5*(Rs[i]==Rs[j])
                        if a=="SA": npair+=1
            if max(Rs)-min(Rs)<1e-12: continue
            for o,v in zip(ok,adv(Rs)):
                res[a]["ok" if o else "bad"].append(v)
    print("=====",at,"cặp đúng-sai loại",npair)
    for a in ["SA","T","T50","G"]:
        r=res[a]
        print(f"{a:4s} P(R đúng loại > R sai loại) {conc[a]/npair:.3f} · adv TB đúng {st.mean(r['ok']):+.3f} sai {st.mean(r['bad']):+.3f} · P(adv sai>0) {sum(v>0 for v in r['bad'])/len(r['bad']):.3f} · P(adv đúng<0) {sum(v<0 for v in r['ok'])/len(r['ok']):.3f} · tổng |adv| sai loại {sum(-v for v in r['bad']):.1f}")

print("\n##### lực đẩy ròng lên loại thao tác đúng (Σ adv của câu đúng loại) trong nhóm back/scroll, và tỉ phần khối |adv|")
tot_mass=collections.Counter(); type_push=collections.Counter(); neg_ok=collections.Counter(); n_ok=collections.Counter()
for k,r in rows.items():
    at=r["action"]["action_type"]; g=r["target_instruction"]; ys=M[k]["mau"]; X=S[k][1:]
    al=None
    for y,x in zip(ys,X):
        s,c,d,S_=recover(y,g,x)
        if abs(s-c)>0.05 and 0<x["R"]["SA-SPICE-v3"]<1: al=(S_-c)/(s-c); break
    al = min([0,0.8/3,1.6/3,0.8], key=lambda a: abs(a-(al if al is not None else 0)))
    RR={}
    for a in ["SA","T","G"]:
        RR[a]=[arms(y,g,at,x,al)[a] for y,x in zip(ys,X)]
    # canonical back: binary type
    if at=="navigate_back" and V.trusted(g,at):
        RR["CB"]=[ max(0.0,(1.0 if (V.classify(y)=="back" or V.BACK_TGT.search(V.toks(y))) else (0.5 if V.classify(y) is None else 0.0)) - penalty(y,g)) if y.strip() else 0.0 for y in ys]
    else:
        RR["CB"]=RR["G"]
    want=CLS.get(at)
    for a,Rs in RR.items():
        if max(Rs)-min(Rs)<1e-12: continue
        ad=adv(Rs)
        lab=at if at in ("navigate_back","scroll") else ("tap" if at in ("click","long_press") else "khac")
        tot_mass[(a,lab)]+=sum(abs(v) for v in ad)
        if want in ("back","scroll"):
            ok=[V.classify(y)==want for y in ys]
            type_push[(a,at)]+=sum(v for v,o in zip(ad,ok) if o)
            neg_ok[(a,at)]+=sum(1 for v,o in zip(ad,ok) if o and v<0); n_ok[(a,at)]+=sum(ok)
for a in ["SA","T","G","CB"]:
    tm=sum(v for (aa,l),v in tot_mass.items() if aa==a)
    print(a, " | ".join(f"{l}: {100*tot_mass[(a,l)]/tm:.1f}%" for l in ["tap","scroll","navigate_back","khac"]),
          "| Σadv đúng loại back", round(type_push[(a,'navigate_back')],1), f"(câu đúng loại adv<0: {neg_ok[(a,'navigate_back')]}/{n_ok[(a,'navigate_back')]})",
          "| scroll", round(type_push[(a,'scroll')],1), f"({neg_ok[(a,'scroll')]}/{n_ok[(a,'scroll')]})")
