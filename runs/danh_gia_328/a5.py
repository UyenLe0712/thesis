import json,re,collections
import numpy as np
R='/mnt/d/Master/Thesis/runs/'
B={'human':'score_ceiling_human_raw.jsonl','S1/101':'score_s1_seed101_raw.jsonl','S1/202':'score_s1_seed202_raw.jsonl','xao101':'xao101/test/score_ck500_xao101_test_raw.jsonl','ck500':'grpo_spice/score_ck500_test_raw.jsonl','ck500/202':'grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl','A2_500':'a2_test299/score_A2_500_test_raw.jsonl','Base':'score_base_raw.jsonl'}
W=re.compile(r"[A-Za-z0-9'-]+")
DANG=set("the a an of on in at to and or with for by from his her my your this that is are then".split())
def f(s):
    w=[x.lower() for x in W.findall(s)]
    bg=list(zip(w,w[1:]));tg=list(zip(w,w[1:],w[2:]))
    return dict(n=len(w),lap_tu=int(any(a==b for a,b in zip(w,w[1:]))),lap2=int(len(bg)!=len(set(bg))),lap3=int(len(tg)!=len(set(tg))),
      treo=int(bool(w) and w[-1] in DANG),rong=int(not w),cham=int(s.strip().endswith('.')),dai=int(len(w)>20),ngan=int(len(w)<=2),hoa=int(s[:1].isupper()))
print(f"{'nhanh':10s} n_tu  p95 lap_tu% lap2gram% lap3gram% treo% rong dai>20% <=2tu% cham% hoa% duynhat%")
for n,p in B.items():
    S=[]
    for l in open(R+p,encoding='utf-8'):
        o=json.loads(l);S.append((o.get('sent') or '').strip())
    F=[f(s) for s in S];m=lambda k:100*np.mean([x[k] for x in F])
    print(f"{n:10s} {np.mean([x['n'] for x in F]):.2f} {np.percentile([x['n'] for x in F],95):.0f} {m('lap_tu'):.2f} {m('lap2'):.2f} {m('lap3'):.2f} {m('treo'):.2f} {sum(x['rong'] for x in F)} {m('dai'):.2f} {m('ngan'):.2f} {m('cham'):.1f} {m('hoa'):.1f} {100*len(set(s.lower() for s in S))/len(S):.1f}")
