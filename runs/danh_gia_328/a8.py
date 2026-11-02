import json,os,subprocess,sys,pickle,collections,re
import numpy as np
sys.dont_write_bytecode=True
H='/mnt/d/Master/Thesis/harness/';R='/mnt/d/Master/Thesis/runs/'
sys.path.insert(0,H)
import metric_exec as M
import pycocoevalcap.spice.spice as SP
d=os.path.dirname(SP.__file__)
def tuples(ss):
    u=sorted(set(s for s in ss if s.strip()))
    inp=[dict(image_id=i,test=s,refs=[s]) for i,s in enumerate(u)]
    os.makedirs('tmpsp',exist_ok=True);json.dump(inp,open('tmpsp/in2.json','w'));o=os.path.abspath('tmpsp/out2.json')
    subprocess.run(['java','-jar','-Xmx8G','spice-1.0.jar',os.path.abspath('tmpsp/in2.json'),'-cache',d+'/cache','-out',o,'-subset','-silent','-detailed'],cwd=d,capture_output=True,text=True,check=True)
    R_=json.load(open(o));return {u[x['image_id']]:[t['tuple'] for t in x['test_tuples']] for x in R_}
test=[json.loads(l) for l in open(H+'dg1_cache/test_ac/test.jsonl',encoding='utf-8')]
tr=[json.loads(l) for l in open('/home/uyenle/fgrb_p1/bundle/p1_train_rows.jsonl',encoding='utf-8')]
keys=set(json.load(open('/mnt/d/Master/Thesis/_bundles/luoi/ds/prompt_keys_ck500.json')))
tr1000=[r for r in tr if f"{r['episode_id']}_{r['step_id']}" in keys]
print('prompt ck500',len(keys),'khop',len(tr1000))
aitz=[json.loads(l) for l in open(R+'aitz/ace_26_10/z/out/score_gold_aitz_raw.jsonl',encoding='utf-8')]
ga=[(a.get('gold_instruction') or '').strip() for a in aitz]
allg=[r['gold_instruction'].strip() for r in test]+[(r.get('target_instruction') or '').strip() for r in tr]+ga
T=tuples(allg);print('tuple cho',len(T))
pickle.dump(T,open('ds328/tuples.pkl','wb'))
def bang(rows,gk):
    c=collections.defaultdict(list)
    for r in rows:
        g=(r.get(gk) or '').strip();t=r['action'].get('action_type')
        c[t].append(len(T.get(g,[])))
    tot=[x for v in c.values() for x in v]
    for t,v in sorted(c.items(),key=lambda x:-len(x[1])):
        print(f"  {t:14s} n {len(v):5d} tuple TB {np.mean(v):.2f}  bang0 {100*np.mean([x==0 for x in v]):.1f}%  <=1 {100*np.mean([x<=1 for x in v]):.1f}%")
    print('  toan bo',len(tot),'bang0',round(100*np.mean([x==0 for x in tot]),1))
print('TEST');bang(test,'gold_instruction');print('1000 cau nhac ck500');bang(tr1000,'target_instruction');print('3991/4000 train');bang(tr,'target_instruction')
# AitZ form
W=re.compile(r"[A-Za-z0-9'-]+")
print('AitZ gold: so tu TB',round(np.mean([len(W.findall(g)) for g in ga]),2),'tuple TB',round(np.mean([len(T.get(g,[])) for g in ga]),2),'bang0 %',round(100*np.mean([len(T.get(g,[]))==0 for g in ga]),1),'dau cau',collections.Counter((W.findall(g.lower()) or [''])[0] for g in ga).most_common(6))
gt=[r['gold_instruction'].strip() for r in test if r['action'].get('action_type') in('click','long_press')]
print('AC gold tap: so tu',round(np.mean([len(W.findall(g)) for g in gt]),2),'tuple TB',round(np.mean([len(T.get(g,[])) for g in gt]),2))
print('duy nhat aitz %',round(100*len(set(x.lower() for x in ga))/len(ga),1))
# Scroll harm theo gold tuple 0/>0
preds=lambda p:{(o['episode_id'],o['step_id']):(o.get('pred') or '').strip() for o in map(json.loads,open(R+p,encoding='utf-8'))}
S=preds('preds_s1_seed101.jsonl');C=preds('grpo_spice/pred_ck500_test_nontap.jsonl')
ok=lambda s,g:int(bool(s) and M.canon_action(s,strict_back=True)==M.canon_action(g,strict_back=True))
for t in ['scroll','navigate_back','input_text','wait','open_app']:
    for lab,f in [('gold 0 tuple',lambda n:n==0),('gold >0',lambda n:n>0)]:
        rr=[r for r in test if r['action'].get('action_type')==t and f(len(T.get(r['gold_instruction'].strip(),[])))]
        if not rr: continue
        k=[(r['episode_id'],r['step_id']) for r in rr]
        a=np.array([ok(S[x],r['gold_instruction']) for x,r in zip(k,rr)]);b=np.array([ok(C[x],r['gold_instruction']) for x,r in zip(k,rr)])
        print(f"  {t:14s} {lab:13s} n {len(rr):4d} S1 {100*a.mean():.1f} ck {100*b.mean():.1f} d {100*(b-a).mean():+.1f} pha {int(((a==1)&(b==0)).sum())} cuu {int(((a==0)&(b==1)).sum())}")
# Doi van phong: cau doi nhung tuple giong
sc=lambda p:{(o['episode_id'],o['step_id']):o for o in map(json.loads,open(R+p,encoding='utf-8'))}
B={'S1/202':'score_s1_seed202_raw.jsonl','xao101':'xao101/test/score_ck500_xao101_test_raw.jsonl','ck500':'grpo_spice/score_ck500_test_raw.jsonl','ck500/202':'grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl','A2_500':'a2_test299/score_A2_500_test_raw.jsonl'}
s1=sc('score_s1_seed101_raw.jsonl')
Tall=tuples([ (o.get('sent') or '').strip() for p in list(B.values())+['score_s1_seed101_raw.jsonl'] for o in sc(p).values()])
pickle.dump(Tall,open('ds328/tuples_sent.pkl','wb'))
fz=lambda s:frozenset(tuple(t) for t in Tall.get(s.strip(),[]))
for n,p in B.items():
    x=sc(p);ch=[k for k in s1 if (x[k].get('sent') or '').strip()!=(s1[k].get('sent') or '').strip()]
    same=[k for k in ch if fz(x[k].get('sent') or '')==fz(s1[k].get('sent') or '')]
    e=lambda D,k:int(D[k].get('executable',0) or 0)
    print(n,'doi',len(ch),'tuple giong',len(same),round(100*len(same)/len(ch),1),'%; trong nhom tuple khac cuu/pha',sum(e(x,k)>e(s1,k) for k in ch if k not in set(same)),sum(e(x,k)<e(s1,k) for k in ch if k not in set(same)),'; tuple giong cuu/pha',sum(e(x,k)>e(s1,k) for k in same),sum(e(x,k)<e(s1,k) for k in same))
    tb=lambda D:np.mean([len(Tall.get((D[k].get('sent') or '').strip(),[])) for k in s1])
    print('   tuple TB moi cau',round(tb(x),3),'S1',round(tb(s1),3))
