import json,pickle,re,sys,collections
import numpy as np
sys.dont_write_bytecode=True
R='/mnt/d/Master/Thesis/runs/'
bd=pickle.load(open('ds328/base.pkl','rb'));SC=pickle.load(open('ds328/sc.pkl','rb'))
pairs=bd['pairs'];idx={p:i for i,p in enumerate(pairs)};gold=bd['gold'];sent=bd['sent'];PV=bd['PV']
W=re.compile(r"[A-Za-z0-9'-]+");nw=lambda s:len(W.findall(s or ''))
MET=['spice','cider','bleu4','rougel','chrf','meteor']
sp=np.array(SC['spice']);ci=np.array(SC['cider'])
A={'spice':sp,'cider':ci,'bleu4':np.array(SC['bleu4']),'rougel':np.array(SC['rougel']),'chrf':np.array(SC['chrf']),'meteor':np.array(SC['meteor'])}
A['spider']=.5*sp+.5*ci
MET.append('spider')
def r(m,s,g,pen=True):
    s=s.strip()
    if not s:return 0.0
    v=float(A[m][idx[(s,g)]])
    return v-(0.02*max(0,nw(s)-nw(g)-3) if pen else 0)
raw=lambda p:{(o['episode_id'],o['step_id']):o for o in map(json.loads,open(R+p,encoding='utf-8'))}
print('kiem: spice gold-gold',np.mean([r('spice',g.strip(),g,False) for g in list(gold.values())[:500] if g.strip()]))
# ---------- T1 perturbation
RAW={'f1':'floor/score_f1_trong_raw.jsonl','f2':'floor/score_f2_khongten_raw.jsonl','f3':'floor/score_f3_lechman_raw.jsonl','p1':'paraphrase/score_para_p1_verb_v2_raw.jsonl','p2':'paraphrase/score_para_p2_order_v2_raw.jsonl','p3':'paraphrase/score_para_p3_nopos_v2_raw.jsonl','p4':'paraphrase/score_para_p4_both_v2_raw.jsonl'}
H=raw('score_ceiling_human_raw.jsonl')
print('\nT1 cau chuan bi bien doi: chi tinh buoc pred khac cau chuan va co diem cham');T1={}
for v,p in RAW.items():
    d=raw(p);K=[k for k in d if k in gold and PV[v].get(k,'').strip() and PV[v][k].strip()!=gold[k].strip()]
    ex=np.mean([d[k].get('executable',0) or 0 for k in K])*100;exh=np.mean([H[k].get('executable',0) or 0 for k in K])*100
    row={m:np.mean([r(m,PV[v][k].strip(),gold[k],False) for k in K]) for m in MET}
    T1[v]=dict(n=len(K),exec_bien=ex,exec_goc=exh,**row)
    print(v,'n',len(K),'exec',round(exh,1),'->',round(ex,1),{m:round(row[m],3) for m in MET})
# ---------- T2 concordance on discordant-exec pairs
B={'S1/101':'score_s1_seed101_raw.jsonl','S1/202':'score_s1_seed202_raw.jsonl','ck500':'grpo_spice/score_ck500_test_raw.jsonl','ck500/202':'grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl','xao101':'xao101/test/score_ck500_xao101_test_raw.jsonl','A2_500':'a2_test299/score_A2_500_test_raw.jsonl'}
D={n:raw(p) for n,p in B.items()};K=sorted(gold)
e=lambda n,k:int(D[n][k].get('executable',0) or 0);ok=lambda n,k:int(D[n][k].get('action_ok',0) or 0)
rng=np.random.default_rng(5)
def cong(a,b,subset=None):
    out={}
    Kd=[k for k in K if e(a,k)!=e(b,k) and (subset is None or subset(a,b,k))]
    for m in MET:
        v=[];t=0;nn=[]
        for k in Kd:
            hi,lo=(a,b) if e(a,k)>e(b,k) else (b,a)
            rh,rl=r(m,sent[hi][k],gold[k]),r(m,sent[lo][k],gold[k])
            if abs(rh-rl)<1e-9: v.append(.5);t+=1
            else: v.append(float(rh>rl));nn.append(float(rh>rl))
        v=np.array(v);bs=[v[rng.integers(0,len(v),len(v))].mean() for _ in range(1000)]
        out[m]=(round(100*v.mean(),1),round(100*np.percentile(bs,2.5),1),round(100*np.percentile(bs,97.5),1),round(100*t/len(v),1),round(100*np.mean(nn),1) if nn else None)
    return len(Kd),out
both=lambda a,b,k:ok(a,k)==1 and ok(b,k)==1
print('\nT2 cap bat dong exec (xep dung%, KTC, hoa%, dung khi khong hoa%) ')
for a,b in [('S1/202','S1/101'),('xao101','S1/101'),('ck500','S1/101'),('ck500/202','S1/101'),('A2_500','S1/101'),('ck500/202','ck500'),('A2_500','ck500')]:
    n,o=cong(a,b);print(a,b,'n',n);[print('   ',m,o[m]) for m in MET]
print('\nT2b chi cap ca hai dung loai thao tac (doi phan tu)')
for a,b in [('S1/202','S1/101'),('xao101','S1/101'),('ck500','S1/101'),('ck500/202','S1/101'),('A2_500','S1/101')]:
    n,o=cong(a,b,both);print(a,b,'n',n);print('   ',{m:o[m][:1]+o[m][3:] for m in MET})
# gop cap khong bi chon (khong qua thuong that): S1 hai hat + xao
def gop(pairs_,subset=None):
    rows=[]
    for a,b in pairs_:
        for k in K:
            if e(a,k)!=e(b,k) and (subset is None or subset(a,b,k)):
                hi,lo=(a,b) if e(a,k)>e(b,k) else (b,a)
                rows.append((sent[hi][k],sent[lo][k],gold[k]))
    rows=list(set(rows));o={}
    for m in MET:
        v=[];t=0
        for h,l,g in rows:
            x,y=r(m,h,g),r(m,l,g)
            if abs(x-y)<1e-9:v.append(.5);t+=1
            else:v.append(float(x>y))
        v=np.array(v);bs=[v[rng.integers(0,len(v),len(v))].mean() for _ in range(2000)]
        o[m]=(round(100*v.mean(),1),round(100*np.percentile(bs,2.5),1),round(100*np.percentile(bs,97.5),1),round(100*t/len(v),1))
    return len(rows),o
print('\nGOP khong chon (S1/202-S1/101, xao-S1):',gop([('S1/202','S1/101'),('xao101','S1/101')]))
print('GOP khong chon, ca hai dung loai:',gop([('S1/202','S1/101'),('xao101','S1/101')],both))
# ---------- T3 tuple categories + delta
det=SC['spice_detail']
print('\nT3 SPICE theo loai tuple (F TB; pr; re), 4463 buoc cham')
def fv(c,s,g):
    if not s.strip():return (0,0,0)
    x=det[c][idx[(s.strip(),g)]];z=lambda q:0.0 if (q is None or q!=q) else float(q)
    return z(x[0]),z(x[1]),z(x[2])
for n in ['S1/101','S1/202','xao101','ck500','ck500/202','A2_500']:
    print(n,{c:tuple(round(100*np.mean([fv(c,sent[n][k],gold[k])[j] for k in K]),2) for j in (2,0,1)) for c in ['All','Object','Attribute','Relation']})
print('so tuple cau chuan TB',{c:round(np.mean([ (det[c][idx[(gold[k].strip(),gold[k])]][3] or 0) for k in K if gold[k].strip()]),2) for c in ['All','Object','Attribute','Relation']})
print('ty le cau chuan co it nhat 1 tuple',{c:round(100*np.mean([ (det[c][idx[(gold[k].strip(),gold[k])]][3] or 0)>0 for k in K if gold[k].strip()]),1) for c in ['All','Object','Attribute','Relation']})
print('SPICE=0 %',{n:round(100*np.mean([r('spice',sent[n][k],gold[k],False)<=1e-9 for k in K]),1) for n in ['S1/101','ck500','ck500/202','A2_500']})
print('gold tu cham SPICE<1 %',round(100*np.mean([r('spice',gold[k].strip(),gold[k],False)<0.999 for k in K if gold[k].strip()]),1))
# metric -> exec AUC tren cau S1 (muc buoc)
def auc(x,y):
    from scipy.stats import rankdata
    x=np.array(x);y=np.array(y);rk=rankdata(x);n1=y.sum();n0=len(y)-n1
    return (rk[y==1].sum()-n1*(n1+1)/2)/(n1*n0)
print('\nAUC metric -> exec tren cau S1/101',{m:round(auc([r(m,sent['S1/101'][k],gold[k]) for k in K],[e('S1/101',k) for k in K]),3) for m in MET})
pickle.dump(T1,open('ds328/t1.pkl','wb'))
# mean delta per metric ck500 - S1 by seed
print('\nDelta TB thuong (ck500-S1, ck202-S1, A2-S1, xao-S1)',{m:tuple(round(100*np.mean([r(m,sent[n][k],gold[k])-r(m,sent['S1/101'][k],gold[k]) for k in K]),2) for n in ['ck500','ck500/202','A2_500','xao101']) for m in MET})
