import json,sys,collections
import numpy as np
sys.dont_write_bytecode=True
H='/mnt/d/Master/Thesis/harness/';R='/mnt/d/Master/Thesis/runs/'
sys.path.insert(0,H)
import metric_exec as M
recs=[json.loads(l) for l in open(H+'dg1_cache/test_ac/test.jsonl',encoding='utf-8')]
TAPT=('click','long_press');istap=lambda r:(r['action'].get('action_type') in TAPT and 'x' in r['action'])
pr=lambda p:{(d['episode_id'],d['step_id']):(d.get('pred') or '').strip() for d in map(json.loads,open(R+p,encoding='utf-8'))}
S=pr('preds_s1_seed101.jsonl');A=pr('ctg/test_nontap/pred_A2_1000_test_nontap.jsonl');C=pr('grpo_spice/pred_ck500_test_nontap.jsonl')
sc=lambda p:{(o['episode_id'],o['step_id']):o for o in map(json.loads,open(R+p,encoding='utf-8'))}
s1=sc('score_s1_seed101_raw.jsonl');a2=sc('a2_test299/score_A2_1000_test_raw.jsonl')
ok=lambda s,g:int(bool(s) and M.canon_action(s,strict_back=True)==M.canon_action(g,strict_back=True))
rows=[]
for r in recs:
    k=(r['episode_id'],r['step_id']);g=r['gold_instruction'];cid=(r.get('app') or '').strip().lower() or f"d{r['episode_id']}"
    if istap(r): rows.append((cid,s1[k].get('executable',0) or 0,a2[k].get('executable',0) or 0))
    else: rows.append((cid,ok(S[k],g),ok(A[k],g)))
cs={c:i for i,c in enumerate(sorted({x[0] for x in rows}))};ci=np.array([cs[x[0]] for x in rows]);nc=len(cs)
v=np.array([x[2]-x[1] for x in rows],float);s=np.bincount(ci,weights=v,minlength=nc);n=np.bincount(ci,minlength=nc).astype(float)
w=np.random.default_rng(3).multinomial(nc,[1/nc]*nc,size=10000);e=(w*s).sum(1)/(w*n).sum(1)
print('A2_1000 tong hop',round(v.mean()*100,2),np.round(np.percentile(e,[2.5,97.5])*100,2),'rong',v.sum())
for t in ['scroll','navigate_back','input_text','wait','open_app']:
    rr=[r for r in recs if r['action'].get('action_type')==t and not istap(r)]
    k=[(r['episode_id'],r['step_id']) for r in rr]
    a=np.array([ok(S[x],r['gold_instruction']) for x,r in zip(k,rr)]);b=np.array([ok(A[x],r['gold_instruction']) for x,r in zip(k,rr)]);c=np.array([ok(C[x],r['gold_instruction']) for x,r in zip(k,rr)])
    print(t,len(rr),'S1',round(100*a.mean(),2),'A2_1000',round(100*b.mean(),2),'ck500',round(100*c.mean(),2))
nt=[r for r in recs if not istap(r)];k=[(r['episode_id'],r['step_id']) for r in nt]
print('toan bo',len(nt),[round(100*np.mean([ok(X[x],r['gold_instruction']) for x,r in zip(k,nt)]),2) for X in (S,A,C)])
