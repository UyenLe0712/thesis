import json,sys,re,collections,math
import numpy as np
sys.dont_write_bytecode=True
H='/mnt/d/Master/Thesis/harness/';R='/mnt/d/Master/Thesis/runs/'
sys.path.insert(0,H)
import metric_exec as M
recs=[json.loads(l) for l in open(H+'dg1_cache/test_ac/test.jsonl',encoding='utf-8')]
TAPT=('click','long_press')
istap=lambda r:(r['action'].get('action_type') in TAPT and 'x' in r['action'])
def preds(p): return {(d['episode_id'],d['step_id']):(d.get('pred') or '').strip() for d in map(json.loads,open(R+p,encoding='utf-8'))}
S=preds('preds_s1_seed101.jsonl');Cn=preds('grpo_spice/pred_ck500_test_nontap.jsonl')
sc=lambda p:{(o['episode_id'],o['step_id']):o for o in map(json.loads,open(R+p,encoding='utf-8'))}
s1=sc('score_s1_seed101_raw.jsonl');ck=sc('grpo_spice/score_ck500_test_raw.jsonl')
ok=lambda s,g:int(bool(s) and M.canon_action(s,strict_back=True)==M.canon_action(g,strict_back=True))
rows=[]
for r in recs:
    k=(r['episode_id'],r['step_id']);g=r['gold_instruction'];a=r.get('app') or ''
    cid=a.strip().lower() or f"d{r['episode_id']}"
    if istap(r):
        rows.append((cid,'tap',s1[k].get('executable',0) or 0,ck[k].get('executable',0) or 0, ok(s1[k].get('sent',''),g),ok(ck[k].get('sent',''),g),r['action'].get('action_type')))
    else:
        rows.append((cid,'non',ok(S[k],g),ok(Cn[k],g),ok(S[k],g),ok(Cn[k],g),r['action'].get('action_type')))
print(len(rows),collections.Counter(x[1] for x in rows))
cs={c:i for i,c in enumerate(sorted({x[0] for x in rows}))};ci=np.array([cs[x[0]] for x in rows]);nc=len(cs)
def boot(v,B=10000):
    s=np.bincount(ci,weights=v,minlength=nc);n=np.bincount(ci,minlength=nc).astype(float)
    w=np.random.default_rng(3).multinomial(nc,[1/nc]*nc,size=B);e=(w*s).sum(1)/(w*n).sum(1)
    return round(v.mean()*100,2),round(np.percentile(e,2.5)*100,2),round(np.percentile(e,97.5)*100,2)
a=np.array([x[2] for x in rows],float);b=np.array([x[3] for x in rows],float)
print('tong hop exec(cham)+dung loai(khong cham): S1',a.mean()*100,'ck',b.mean()*100,'delta',boot(b-a),'buoc rong',(b-a).sum())
a2=np.array([x[4] for x in rows],float);b2=np.array([x[5] for x in rows],float)
print('dung loai toan bo: S1',a2.mean()*100,'ck',b2.mean()*100,boot(b2-a2),'rong',(b2-a2).sum())
for t in ('tap','non'):
    m=np.array([x[1]==t for x in rows]);print(t,m.sum(),'exec-or-ok rong',(b-a)[m].sum(),'ok-only rong',(b2-a2)[m].sum())
# nghieng ve cham: ty le cau quy ve cham theo nhom vang
# canon action names
def istapcanon(s): return M.canon_action(s,strict_back=True)
print('vi du canon',[istapcanon(x) for x in ['Click on X','Swipe up','Go back','Open the Clock app','Search for x','Type x in y','Wait']])
for t in ('tap','non'):
    c1=collections.Counter();c2=collections.Counter()
    for r in recs:
        if (t=='tap')!=istap(r):continue
        k=(r['episode_id'],r['step_id'])
        if t=='tap':x,y=s1[k].get('sent',''),ck[k].get('sent','')
        else:x,y=S[k],Cn[k]
        c1[str(istapcanon(x or ''))[:12]]+=1;c2[str(istapcanon(y or ''))[:12]]+=1
    print(t,'S1',c1.most_common(8));print(t,'ck',c2.most_common(8))
