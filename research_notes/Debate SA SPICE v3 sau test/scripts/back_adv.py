import json, sys, collections, statistics as st
sys.path.insert(0, "/mnt/d/Master/Thesis/harness")
import sa3_action_verify as V
R="/mnt/d/Master/Thesis/runs/sa_spice_v3/"
rows={ (r["episode_id"],r["step_id"]):r for r in map(json.loads, open(R+"split/train_v3.jsonl"))}
M={}
for i in (0,1):
    for l in open(R+f"mau_k1/mau_{i}.jsonl"):
        d=json.loads(l); M[(d["episode_id"],d["step_id"])]=d
S={}
for l in open(R+"screen/out/sa3_screen_buoc.jsonl"):
    d=json.loads(l); S[(d["episode_id"],d["step_id"])]=d["R"]
ARMS=["SA-SPICE-v3","chrF","SPICE-MATCH","FIXED+A","Action-SPICE"]
def adv(Rs, unbiased=True):
    m=sum(Rs)/len(Rs); sd=st.stdev(Rs) if unbiased else st.pstdev(Rs)
    return [(r-m)/(sd+1e-4) for r in Rs]
gold_back=collections.Counter()
for at in ["navigate_back","scroll"]:
    print("=====",at)
    stats={a:{"ok":[], "bad":[], "rok":[], "rbad":[]} for a in ARMS}
    ng=nmix=0; Acount=collections.Counter(); trusted=0
    for k,r in rows.items():
        if r["action"]["action_type"]!=at: continue
        ng+=1
        g=r["target_instruction"]
        if at=="navigate_back": gold_back[g]+=1
        if V.trusted(g,at): trusted+=1
        ys=M[k]["mau"]; RR=S[k][1:]
        cl=[V.classify(y) for y in ys]
        want="back" if at=="navigate_back" else "scroll"
        ok=[c==want for c in cl]
        for x in RR: Acount[x["A"]]+=1
        if any(ok) and not all(ok): nmix+=1
        else: continue
        for a in ARMS:
            Rs=[x["R"][a] for x in RR]
            if max(Rs)-min(Rs)<1e-12: continue
            ad=adv(Rs)
            for o,v,rv in zip(ok,ad,Rs):
                stats[a]["ok" if o else "bad"].append(v); stats[a]["rok" if o else "rbad"].append(rv)
    print("nhóm",ng,"trusted gold",trusted,"nhóm lẫn",nmix,"A phân bố",dict(Acount))
    for a in ARMS:
        s=stats[a]
        print(f"{a:13s} adv TB đúng loại {st.mean(s['ok']):+.3f} (n={len(s['ok'])}) · sai loại {st.mean(s['bad']):+.3f} (n={len(s['bad'])}) · R TB đúng {st.mean(s['rok']):.3f} sai {st.mean(s['rbad']):.3f} · P(adv sai>0) {sum(v>0 for v in s['bad'])/len(s['bad']):.2f} · P(adv đúng<0) {sum(v<0 for v in s['ok'])/len(s['ok']):.2f}")
print(gold_back.most_common(15))
