import sys,json,os
sys.dont_write_bytecode=True
sys.path.insert(0,'/mnt/d/Master/Thesis/harness')
import numpy as np
import thuong_dac_tinh as T, grpo_luoi as GL, grpo_spice as GS
keys,gold,sent,ex=T.nap()
print('dl',len(keys))
out={}
B='/home/uyenle/fgrb_p1/bundle'
for name in ['spice','cider','meteor','rougel','bleu4','chrf']:
    GL.dung_bo_cham(name,B)
    R=np.array(T.thuong_cua(name,gold,sent));E=np.array(ex)
    # diem khong phat: cong lai phat
    pen=np.array([[GS.MU*max(0,GS.nwords(s.strip())-GS.nwords(g)-3) if s.strip() else 0 for s in row] for row,g in zip(sent,gold)])
    raw=R+pen
    r8,e8,p8,raw8=R[:,1:],E[:,1:],pen[:,1:],raw[:,1:]
    sd=r8.std(1,ddof=1);sdraw=raw8.std(1,ddof=1)
    only=((sdraw<1e-9)&(sd>1e-9)).mean()
    d={'std0':(sd<1e-9).mean(),'chi_nho_phat':only,'mau_bi_phat':(p8>0).mean(),'std_tv':np.median(sd),'std<0.02':((sd>1e-9)&(sd<.02)).mean(),'std<0.05':((sd>1e-9)&(sd<.05)).mean()}
    # SCST zero-adv
    A=r8-R[:,[0]];d['scst_A0']=(np.abs(A)<1e-6).mean();d['scst_Atb']=A.mean()
    mex=e8.mean(1,keepdims=True);mask=(np.abs(A)>1e-6)&(np.abs(e8-mex)>1e-9);d['scst_dau']=((A>0)==(e8>mex))[mask].mean()
    # cap khong hoa
    h=0;n=0;t=0
    for r,e in zip(r8,e8):
        for i in range(8):
            for j in range(i+1,8):
                if e[i]!=e[j]:
                    n+=1
                    hi,lo=(i,j) if e[i]>e[j] else (j,i)
                    if abs(r[hi]-r[lo])<1e-9: t+=1
                    elif r[hi]>r[lo]: h+=1
    d['dung_khong_hoa']=h/(n-t);d['hoa_trong_cap_khac_exec']=t/n
    # lap tuong doi: trong nhom co cau trung greedy
    out[name]={k:round(float(v)*(100 if k not in('std_tv','scst_Atb') else 1),2 if k not in('std_tv','scst_Atb') else 4) for k,v in d.items()}
    print(name,out[name],flush=True)
json.dump(out,open('ds328/c1_them.json','w'),indent=1)
