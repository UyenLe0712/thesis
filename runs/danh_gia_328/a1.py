import json,sys,os,math,re,collections
import numpy as np
from math import comb
R='/mnt/d/Master/Thesis/runs/'
sys.path.insert(0,'/mnt/d/Master/Thesis/harness')
sys.dont_write_bytecode=True
import metric_exec as M
def nap(p):
    d={}
    for l in open(R+p,encoding='utf-8'):
        o=json.loads(l); o.setdefault('executable',0); o.setdefault('action_ok',0); o.setdefault('sent','')
        d[(o['episode_id'],o['step_id'])]=o
    return d
F={'S1/101':'score_s1_seed101_raw.jsonl','S1/202':'score_s1_seed202_raw.jsonl','ck500':'grpo_spice/score_ck500_test_raw.jsonl',
'ck500/202':'grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl','xao101':'xao101/test/score_ck500_xao101_test_raw.jsonl',
'A2_500':'a2_test299/score_A2_500_test_raw.jsonl','A2_1000':'a2_test299/score_A2_1000_test_raw.jsonl','Base':'score_base_raw.jsonl','GRPOpoint':'grpo_point/score_grpo_point_seed101_raw.jsonl','human':'score_ceiling_human_raw.jsonl'}
D={k:nap(v) for k,v in F.items() if os.path.exists(R+v)}
K=sorted(D['S1/101'])
print(len(K),{k:len(v) for k,v in D.items()})
def cum(o):
    a=(o.get('app') or '').strip().lower()
    return a if a else f"__don__{o['episode_id']}"
C=[cum(D['S1/101'][k]) for k in K]
cl={c:i for i,c in enumerate(sorted(set(C)))}; ci=np.array([cl[c] for c in C]); nc=len(cl); print('cum',nc)
def boot(v,B=10000,seed=1):
    # v per-step array; cluster bootstrap for mean (ratio estimator)
    s=np.bincount(ci,weights=v,minlength=nc); n=np.bincount(ci,minlength=nc).astype(float)
    r=np.random.default_rng(seed); w=r.multinomial(nc,[1/nc]*nc,size=B)
    est=(w*s).sum(1)/(w*n).sum(1)
    return v.mean()*100,np.percentile(est,2.5)*100,np.percentile(est,97.5)*100,est.std()*100
def vec(n,f='executable'): return np.array([float(D[n][k].get(f,0) or 0) for k in K])
def mc(a,b):
    bb=int(((a==1)&(b==0)).sum()); cc=int(((a==0)&(b==1)).sum()); n=bb+cc
    if n==0:return bb,cc,1
    # exact via log
    from scipy.stats import binomtest
    return bb,cc,binomtest(bb,n,.5).pvalue
print('--- exec level')
for n in D: print(n, round(vec(n).mean()*100,2), 'action_ok',round(vec(n,'action_ok').mean()*100,2))
print('--- paired')
P=[('ck500','S1/101'),('ck500/202','S1/101'),('ck500','S1/202'),('ck500/202','S1/202'),('ck500/202','ck500'),('S1/202','S1/101'),('xao101','S1/101'),('ck500','xao101'),('ck500/202','xao101'),('A2_500','S1/101'),('A2_500','ck500'),('A2_500','ck500/202'),('A2_1000','ck500'),('A2_1000','ck500/202'),('GRPOpoint','ck500'),('ck500','GRPOpoint')]
for a,b in P:
    if a in D and b in D:
        va,vb=vec(a),vec(b); m,l,h,s=boot(va-vb); x=mc(va,vb); print(f"{a} - {b}: {m:+.2f} [{l:+.2f};{h:+.2f}] se {s:.2f} cuu {x[0]} pha {x[1]} p={x[2]:.2g} sqrt(b+c)/n={100*math.sqrt(x[0]+x[1])/len(K):.2f}")
# mean 2 seeds
va=(vec('ck500')+vec('ck500/202'))/2; 
for b in ['S1/101','S1/202']:
    m,l,h,s=boot(va-vec(b)); print('mean2(ck500)-',b,round(m,2),round(l,2),round(h,2),'se',round(s,2))
vs=(vec('S1/101')+vec('S1/202'))/2
m,l,h,s=boot(va-vs); print('mean2(ck)-mean2(S1)',round(m,2),round(l,2),round(h,2),'se',round(s,2))
m,l,h,s=boot((vec('ck500')+vec('ck500/202')+vec('xao101'))*0+va-vec('xao101')); print('mean2-xao',round(m,2),round(l,2),round(h,2))
# decomposition
print('--- phan ra')
def dec(a,b,D_=D,K_=K):
    r=collections.Counter()
    for k in K_:
        x,y=D_[a][k],D_[b][k]
        ea,eb=int(x['executable'] or 0),int(y['executable'] or 0)
        oa,ob=int(x.get('action_ok') or 0),int(y.get('action_ok') or 0)
        if x['sent']!=y['sent']: r['doi_cau']+=1
        if ea==eb: continue
        if oa==ob==1: r['cung_dung_loai_cuu' if ea>eb else 'cung_dung_loai_pha']+=1
        else: r['loai_cuu' if ea>eb else 'loai_pha']+=1
    return dict(r)
for a,b in [('ck500','S1/101'),('ck500/202','S1/101'),('xao101','S1/101'),('A2_500','S1/101'),('S1/202','S1/101')]:
    if a in D: print(a,b,dec(a,b))
# only both action ok, restrict
for a in ['ck500','ck500/202','xao101','A2_500']:
    if a in D:
        mask=(vec(a,'action_ok')==1)&(vec('S1/101','action_ok')==1)
        print(a,'both ok n',mask.sum(),'exec',round(vec(a)[mask].mean()*100,2),'S1',round(vec('S1/101')[mask].mean()*100,2))
# ACU
print('--- ACU')
A={n:nap(f'acu/gen/out/score_{f}_acu_raw.jsonl') for n,f in {'S1':'s1','ck500':'ck500','ck202':'ck500_s202','base':'base','gold':'gold'}.items()}
KA=sorted(A['S1'])
print(len(KA),{n:round(100*np.mean([A[n][k]['executable'] for k in KA]),2) for n in A},{n:round(100*np.mean([A[n][k].get('action_ok',0) for k in KA]),2) for n in A})
for a in ['ck500','ck202']: print(a,dec(a,'S1',A,KA))
for n in ['S1','ck500','ck202','base','gold']:
    w=[M.nwords(A[n][k]['sent']) if hasattr(M,'nwords') else len(A[n][k]['sent'].split()) for k in KA]; print(n,'so tu tb',round(np.mean(w),2))
# both ok exec on ACU
m=[k for k in KA if A['S1'][k]['action_ok'] and A['ck500'][k]['action_ok']]
print('ACU bothok',len(m),round(100*np.mean([A['S1'][k]['executable'] for k in m]),2),round(100*np.mean([A['ck500'][k]['executable'] for k in m]),2))
# test comparison of verbs
for lab,DD,KK,n in [('test S1',D,K,'S1/101'),('test ck',D,K,'ck500'),('ACU S1',A,KA,'S1'),('ACU ck',A,KA,'ck500')]:
    c=collections.Counter(DD[n][k]['sent'].strip().lower().split(' ')[0] if DD[n][k]['sent'].strip() else '' for k in KK)
    print(lab,[ (w,round(100*x/len(KK),1)) for w,x in c.most_common(6)])
