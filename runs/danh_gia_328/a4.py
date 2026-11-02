import json,re,collections,sys,math
sys.dont_write_bytecode=True
H='/mnt/d/Master/Thesis/harness/';R='/mnt/d/Master/Thesis/runs/'
sys.path.insert(0,H)
import numpy as np
WORD=re.compile(r"[A-Za-z0-9'-]+")
test=[json.loads(l) for l in open(H+'dg1_cache/test_ac/test.jsonl',encoding='utf-8')]
train=[json.loads(l) for l in open(H+'dg1_cache/train_ac/train.jsonl',encoding='utf-8')]
def stat(name,gs):
    L=[len(WORD.findall(g)) for g in gs]
    first=collections.Counter((WORD.findall(g.lower()) or [''])[0] for g in gs)
    two=collections.Counter(' '.join(WORD.findall(g.lower())[:2]) for g in gs)
    print(name,len(gs),'so tu tb',round(np.mean(L),2),'tv',np.median(L),'p90',np.percentile(L,90),'duy nhat %',round(100*len(set(x.lower().strip() for x in gs))/len(gs),1))
    print('  dau cau',[(w,round(100*c/len(gs),1)) for w,c in first.most_common(6)])
    print('  hai tu',[(w,round(100*c/len(gs),1)) for w,c in two.most_common(5)])
tg=[r['gold_instruction'] for r in test]; stat('test all',tg)
TAP=('click','long_press')
stat('test tap',[r['gold_instruction'] for r in test if r['action'].get('action_type') in TAP])
stat('test scroll',[r['gold_instruction'] for r in test if r['action'].get('action_type')=='scroll'])
stat('train all',[r['target_instruction'] for r in train])
at=collections.Counter(r['action'].get('action_type') for r in test);print(at)
# Gold tap canon rate
import metric_exec as M
c=collections.Counter(M.canon_action(g,strict_back=True) for g in tg);print('canon gold',c)
print('gold canon tap in non-tap steps',sum(M.canon_action(r['gold_instruction'],strict_back=True)=='tap' for r in test if not(r['action'].get('action_type') in TAP and 'x' in r['action'])),'/2495')
# IDF mass: name vs template tokens in gold tap with desc name
import grpo_luoi as GL
tr=[json.loads(l) for l in open('/home/uyenle/fgrb_p1/bundle/p1_train_rows.jsonl',encoding='utf-8')]
refs=[(r.get('target_instruction') or '').strip() for r in tr];refs=[r for r in refs if r]
df=collections.Counter()
for r in refs:
    for w in set(GL.tok(r)): df[w]+=1
N=len(refs);print('refs',N)
idf=lambda w: math.log(N)-math.log(max(1,df.get(w,0)))
TPL=set("click on the tap select press open a an at in of to top bottom left right corner screen button icon option go back swipe scroll up down".split())
mass=[];cnt=[]
for g in [r['gold_instruction'] for r in test if r['action'].get('action_type') in TAP]:
    ws=GL.tok(g)
    if not ws: continue
    tot=sum(idf(w) for w in ws);nm=sum(idf(w) for w in ws if w not in TPL)
    mass.append(nm/tot if tot else 0);cnt.append(sum(w not in TPL for w in ws)/len(ws))
print('ty le tu ngoai khuon',round(np.mean(cnt),3),'ty le khoi luong IDF don ngoai khuon',round(np.mean(mass),3))
print('idf vi du',{w:round(idf(w),2) for w in ['click','on','the','search','icon','settings','swipe','up','tommy']})
print('khong co tu ngoai khuon: %',round(100*np.mean([c==0 for c in cnt]),1))
