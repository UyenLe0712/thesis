import json,sys,re,statistics as st
sys.path.insert(0,'/mnt/d/Master/Thesis/harness')
from sa3_action_verify import classify
R='/mnt/d/Master/Thesis/runs/sa_spice_v3/'
WORD = re.compile(r"[A-Za-z0-9'-]+"); nw=lambda s: len(WORD.findall(s or ""))
pen=lambda y,g: min(0.05,0.02*max(0,nw(y)-nw(g)-3)); clip=lambda x:min(1.0,max(0.0,x))
mau={}
for f in ['mau_k1/mau_0.jsonl','mau_k1/mau_1.jsonl']:
    for l in open(R+f):
        d=json.loads(l); mau[(d['episode_id'],d['step_id'])]=d
scr={}
for l in open(R+'screen/out/sa3_screen_buoc.jsonl'):
    d=json.loads(l); scr[(d['episode_id'],d['step_id'])]=d['R']
CAN={'navigate_back':'back','scroll':'scroll','input_text':'type','open_app':'open_app'}
def N2(y,g,a,A):
    d=pen(y,g); s=(a['SPICE-MATCH']-0.1+d)/0.8; c=(a['FIXED']-0.1+d-0.64*s)/0.16
    return clip(0.8*(0.5*s+0.5*c)+0.2*A-d)
for at,canon in CAN.items():
    keys=[k for k,d in mau.items() if d['action_type']==at]
    res={}
    for name in ['SA-SPICE-v3','N2 SPICE-chrF-A','chrF']:
        w=l_=t=0
        for k in keys:
            d=mau[k]; g=d['gold']; recs=scr[k][1:]
            Rs=[]
            for y,rec in zip(d['mau'],recs):
                if not (y or '').strip(): Rs.append(0.0); continue
                Rs.append(N2(y,g,rec['R'],rec['A']) if name.startswith('N2') else rec['R'][name])
            cls=[classify(m)==canon for m in d['mau']]
            for c,r in zip(cls,Rs):
                for c2,r2 in zip(cls,Rs):
                    if c and not c2: w+=r>r2+1e-12; l_+=r<r2-1e-12; t+=abs(r-r2)<=1e-12
        res[name]=((w+.5*t)/max(1,w+l_+t),w,l_,t)
    print(at,len(keys),{k:(round(v[0],3),v[1:]) for k,v in res.items()})
