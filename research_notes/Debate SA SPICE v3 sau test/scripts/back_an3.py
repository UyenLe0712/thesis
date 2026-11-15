import json,sys,statistics as st
from collections import Counter
sys.path.insert(0,'/mnt/d/Master/Thesis/harness')
from sa3_action_verify import classify
R='/mnt/d/Master/Thesis/runs/sa_spice_v3/'
mau={}
for f in ['mau_k1/mau_0.jsonl','mau_k1/mau_1.jsonl']:
    for l in open(R+f):
        d=json.loads(l); mau[(d['episode_id'],d['step_id'])]=d
scr={}
for l in open(R+'screen/out/sa3_screen_buoc.jsonl'):
    d=json.loads(l); scr[(d['episode_id'],d['step_id'])]=d
CAN={'navigate_back':'back','scroll':'scroll','input_text':'type','open_app':'open_app','wait':'wait','click':'tap'}
print('prompts by action',Counter(d['action_type'] for d in mau.values()))
for at in ['navigate_back','scroll','input_text','open_app','click']:
    keys=[k for k,d in mau.items() if d['action_type']==at]
    canon=CAN[at]
    mixed=sum(1 for k in keys if len({classify(m)==canon for m in mau[k]['mau']})==2)
    anyr=sum(1 for k in keys if any(classify(m)==canon for m in mau[k]['mau']))
    frac=st.mean(classify(m)==canon for k in keys for m in mau[k]['mau'])
    print(f'{at}: n={len(keys)} any-right {anyr} mixed {mixed} frac-right-samples {frac:.3f}')
    for rw in ['SA-SPICE-v3','chrF','SPICE-MATCH','FIXED+A','ROUGE-L','SPIDEr-like']:
        w=l_=t=0; ar=[];aw=[]
        for k in keys:
            d=mau[k]; Rs=[x['R'][rw] for x in scr[k]['R'][1:]]; cls=[classify(m)==canon for m in d['mau']]
            if len(set(cls))<2: continue
            mu=st.mean(Rs); sd=st.pstdev(Rs)
            if sd<1e-12: continue
            for c,r in zip(cls,Rs):
                (ar if c else aw).append((r-mu)/sd)
            for c,r in zip(cls,Rs):
                for c2,r2 in zip(cls,Rs):
                    if c and not c2: w+=r>r2; l_+=r<r2; t+=r==r2
        conc=(w+0.5*t)/max(1,w+l_+t)
        print(f'   {rw:12s} right-vs-wrong concordance {conc:.3f} ({w}/{l_}/{t}) mean adv right {st.mean(ar):+.2f} wrong {st.mean(aw):+.2f}')
