import json,os,sys,glob,collections
sys.dont_write_bytecode=True
R='/mnt/d/Master/Thesis/runs/'
def L(p): return {(o["episode_id"], o["step_id"]): o for o in map(json.loads, open(p, encoding="utf-8"))}
F={"s1":"score_s1_seed101_raw.jsonl","ck500":"grpo_spice/score_ck500_test_raw.jsonl"}
Z={n:L(R+p) for n,p in F.items()}
V={}
for p in ["venus/score_venus_s1_2532_raw.jsonl"]+[f"venus/ck500_r3_22_10/score_{n}_raw.jsonl" for n in("s1","ck500","r3")]+glob.glob(R+"venus/bu_22_10/score_*_raw.jsonl"):
    p=p if p.startswith('/') else R+p
    for k,o in L(p).items():
        if "sent" in o: V[(k,o["sent"].strip())]=int(o["executable"])
c=collections.Counter();tot=collections.Counter();miss=0
for k in Z['s1']:
    r={}
    for n in Z:
        s=(Z[n][k].get('sent') or '').strip()
        r[n]=0 if not s else V.get((k,s))
    if None in r.values(): miss+=1;continue
    tot['s1']+=r['s1'];tot['ck']+=r['ck500'];tot['n']+=1
    if r['s1']!=r['ck500']:
        b=Z['s1'][k].get('action_ok') and Z['ck500'][k].get('action_ok')
        c[('cung' if b else 'loai')+('_cuu' if r['ck500']>r['s1'] else '_pha')]+=1
print('venus',dict(c),dict(tot),'thieu',miss)
# phi4
def P(fs):
    d={}
    for f in fs:
        for o in map(json.loads,open(f,encoding='utf-8')):
            d[(int(o['episode_id']),int(o['step_id']))]=o
    return d
print([os.path.basename(x) for x in glob.glob(R+'som/chon_phi4_*.jsonl')])
