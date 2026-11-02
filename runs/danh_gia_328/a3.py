import json,sys,os,time,pickle,collections
sys.dont_write_bytecode=True
H='/mnt/d/Master/Thesis/harness/';R='/mnt/d/Master/Thesis/runs/'
sys.path.insert(0,H)
import grpo_luoi as GL, grpo_spice as GS
OUT='ds328/'
def rd(p):
    d={}
    for l in open(R+p,encoding='utf-8'):
        o=json.loads(l);d[(o['episode_id'],o['step_id'])]=o
    return d
S1=rd('score_s1_seed101_raw.jsonl')
gold={k:(v.get('gold_instruction') or '') for k,v in S1.items()}
B={'S1/101':'score_s1_seed101_raw.jsonl','S1/202':'score_s1_seed202_raw.jsonl','ck500':'grpo_spice/score_ck500_test_raw.jsonl','ck500/202':'grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl','xao101':'xao101/test/score_ck500_xao101_test_raw.jsonl','A2_500':'a2_test299/score_A2_500_test_raw.jsonl'}
pairs=set()
sent={}
for n,f in B.items():
    d=rd(f);sent[n]={k:(d[k].get('sent') or '').strip() for k in gold}
    for k in gold: pairs.add((sent[n][k],gold[k]))
# floor/paraphrase
PV={}
for n,f in {'f1':'floor/preds_f1_trong.jsonl','f2':'floor/preds_f2_khongten.jsonl','f3':'floor/preds_f3_lechman.jsonl','p1':'paraphrase/preds_para_p1_verb_v2.jsonl','p2':'paraphrase/preds_para_p2_order_v2.jsonl','p3':'paraphrase/preds_para_p3_nopos_v2.jsonl','p4':'paraphrase/preds_para_p4_both_v2.jsonl'}.items():
    d={(o['episode_id'],o['step_id']):(o.get('pred') or '').strip() for o in map(json.loads,open(R+f,encoding='utf-8'))}
    PV[n]=d
    for k,s in d.items():
        if k in gold: pairs.add((s,gold[k]))
for k in gold: pairs.add((gold[k].strip(),gold[k]))
pairs=sorted(p for p in pairs if p[0])
print('cap duy nhat',len(pairs),flush=True)
pickle.dump(dict(sent=sent,PV=PV,gold=gold,pairs=pairs),open(OUT+'base.pkl','wb'))
c=[p[0] for p in pairs];g=[p[1] for p in pairs]
SC={}
# Non-java first
for name in ['bleu4','chrf','rougel','cider','meteor']:
    t=time.time();GL.dung_bo_cham(name,'/home/uyenle/fgrb_p1/bundle')
    SC[name]=[float(x) for x in GL.diem(name,c,g)];print(name,round(time.time()-t,1),'s',flush=True)
    pickle.dump(SC,open(OUT+'sc.pkl','wb'))
# SPICE with categories
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.spice.spice import Spice
t=time.time();tk=PTBTokenizer()
G=tk.tokenize({i:[{'caption':r}] for i,r in enumerate(g)});Cc=tk.tokenize({i:[{'caption':s}] for i,s in enumerate(c)})
print('ptb',round(time.time()-t,1),flush=True)
_,sc=Spice().compute_score(G,Cc)
print('spice',round(time.time()-t,1),flush=True)
SP={}
for cat in ['All','Object','Attribute','Relation']:
    SP[cat]=[(x[cat]['pr'],x[cat]['re'],x[cat]['f'],x[cat].get('numImTuples'),x[cat].get('numTestTuples')) for x in sc]
SC['spice']=[0.0 if (x['All']['f'] is None or x['All']['f']!=x['All']['f']) else float(x['All']['f']) for x in sc]
SC['spice_detail']=SP
pickle.dump(SC,open(OUT+'sc.pkl','wb'))
print('xong',flush=True)
