import json,os,glob,collections,sys,ast,re
import numpy as np
R='/mnt/d/Master/Thesis/runs/'
raw=lambda p:{(o['episode_id'],o['step_id']):o for o in map(json.loads,open(p,encoding='utf-8'))}
def dec(a,b,lab):
    K=sorted(set(a)&set(b));e=lambda d,k:int(d[k].get('executable',0) or 0);ok=lambda d,k:int(d[k].get('action_ok',0) or 0)
    c=collections.Counter()
    for k in K:
        x,y=e(a,k),e(b,k)
        if x==y: continue
        key=('cung' if ok(a,k)==ok(b,k)==1 else 'loai')+('_cuu' if x>y else '_pha');c[key]+=1
    print(lab,len(K),dict(c),'exec',round(100*np.mean([e(a,k) for k in K]),2),round(100*np.mean([e(b,k) for k in K]),2))
v=R+'venus/ck500_r3_22_10/'
dec(raw(v+'score_ck500_raw.jsonl'),raw(v+'score_s1_raw.jsonl'),'venus file 22_10')
print(sorted(glob.glob(R+'venus/bu_22_10/*'))[:12])
print(sorted(glob.glob(R+'phiground/*'))[:15])
print(sorted(glob.glob(R+'som/*'))[:20])
