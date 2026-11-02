import json,pickle,re,sys,collections,math
import numpy as np
sys.dont_write_bytecode=True
R='/mnt/d/Master/Thesis/runs/'
bd=pickle.load(open('ds328/base.pkl','rb'));SC=pickle.load(open('ds328/sc.pkl','rb'));pairs=bd['pairs'];idx={p:i for i,p in enumerate(pairs)};gold=bd['gold'];PV=bd['PV']
A={'spice':np.array(SC['spice']),'cider':np.array(SC['cider']),'bleu4':np.array(SC['bleu4']),'rougel':np.array(SC['rougel']),'chrf':np.array(SC['chrf']),'meteor':np.array(SC['meteor'])}
A['spider']=.5*A['spice']+.5*A['cider']
raw=lambda p:{(o['episode_id'],o['step_id']):o for o in map(json.loads,open(R+p,encoding='utf-8'))}
RAW={'f2':'floor/score_f2_khongten_raw.jsonl','p1':'paraphrase/score_para_p1_verb_v2_raw.jsonl','p2':'paraphrase/score_para_p2_order_v2_raw.jsonl','p3':'paraphrase/score_para_p3_nopos_v2_raw.jsonl'}
DD={v:raw(p) for v,p in RAW.items()}
aff={v:{k for k in DD[v] if k in gold and PV[v].get(k,'').strip() and PV[v][k].strip()!=gold[k].strip()} for v in RAW}
common=aff['f2']&aff['p1']&aff['p2']&aff['p3']
print('giao f2 p1 p2 p3',len(common),{v:len(aff[v]) for v in aff})
E=lambda v,K:100*np.mean([DD[v][k].get('executable',0) or 0 for k in K])
print('exec giao',{v:round(E(v,common),1) for v in RAW})
for m in A:
    print(m,{v:round(float(np.mean([A[m][idx[(PV[v][k].strip(),gold[k])]] for k in common])),3) for v in RAW})
# Ty so chon loc: dat f2 so voi p1,  tren giao f2 & p1
c2=aff['f2']&aff['p1'];print('giao f2 p1',len(c2),'exec f2',round(E('f2',c2),1),'p1',round(E('p1',c2),1))
for m in A:
    x=np.array([A[m][idx[(PV['f2'][k].strip(),gold[k])]] for k in c2]);y=np.array([A[m][idx[(PV['p1'][k].strip(),gold[k])]] for k in c2])
    print(' ',m,'f2',round(x.mean(),3),'p1',round(y.mean(),3),'p1-f2',round((y-x).mean(),3),'P(p1>f2)',round(100*np.mean(y>x+1e-9)+50*np.mean(np.abs(y-x)<=1e-9),1))
# Task-level
for lab,paths in [('lich su chuan',{'S1':'score_s1_seed101_raw.jsonl','ck':'grpo_spice/score_ck500_test_raw.jsonl','ck202':'grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl','xao':'xao101/test/score_ck500_xao101_test_raw.jsonl'})]:
    D={n:raw(p) for n,p in paths.items()}
    eps=collections.defaultdict(list)
    for k in D['S1']: eps[k[0]].append(k)
    print(lab,'tac vu co buoc cham',len(eps),'buoc cham/tac vu',round(np.mean([len(v) for v in eps.values()]),2))
    allok=lambda n:np.array([all(D[n][k].get('executable',0) for k in v) for v in eps.values()],float)
    for n in D: print(' ',n,round(100*allok(n).mean(),2))
    rng=np.random.default_rng(1)
    for n in ['ck','ck202','xao']:
        d=allok(n)-allok('S1');b=[d[rng.integers(0,len(d),len(d))].mean() for _ in range(5000)]
        print(' ',n,'-S1',round(100*d.mean(),2),np.round(np.percentile(b,[2.5,97.5])*100,2))
# power: seed
import math
s=0.51
for dl in (1.0,.7,.5): print('so hat moi nhanh de tach',dl,'voi sigma',s,':',math.ceil(2*(2.8*s/dl)**2))
for se in (.30,.35,.42,.55): print('Holm 50 phep nguong: SE',se,'=> delta can',round(3.29*se,2),'; p<0.05 chua hieu chinh',round(1.96*se,2))
