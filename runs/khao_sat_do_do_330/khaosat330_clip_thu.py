import json,re,sys,random
src=open('khaosat330_stress.py').read().split('print("ví dụ:")')[0]
exec(src)
import torch
from PIL import Image
from transformers import CLIPModel,CLIPProcessor
H2="/mnt/d/Master/Thesis/harness/dg1_cache/train_ac/"
img={r["target_instruction"].strip():r["image"] for r in rows}
mid="openai/clip-vit-base-patch32"
m=CLIPModel.from_pretrained(mid).eval(); p=CLIPProcessor.from_pretrained(mid)
print("ảnh vào",p.image_processor.size,p.image_processor.crop_size,flush=True)
S={k:[] for k in V}
n=0
torch.set_num_threads(8)
for i in range(len(V["goc"])):
    g=V["goc"][i]
    try: im=Image.open(H2+img[g]).convert("RGB")
    except Exception as e: continue
    keys=list(V)
    tx=[V[k][i] for k in keys]
    with torch.no_grad():
        inp=p(text=tx,images=im,return_tensors="pt",padding=True,truncation=True)
        o=m(**inp)
        ie=o.image_embeds; te=o.text_embeds
        c=(te@ie.T).squeeze(1)
    for k,x in zip(keys,c.tolist()): S[k].append(max(x,0)*2.5)
    n+=1
    if n%100==0: print(n,flush=True)
json.dump(S,open('clip.json','w'))
mean=lambda a:sum(a)/len(a)
print("n",n,{k:round(mean(v),3) for k,v in S.items()})
w=lambda a,b:sum((x>y)+.5*(x==y) for x,y in zip(a,b))/len(a)
for k in S:
    if k!="goc": print("P(goc>%s)=%.3f"%(k,w(S["goc"],S[k])))
print("P(dong_tu>ten_sai)=%.3f"%w(S["dong_tu"],S["ten_sai"]),"P(bo_vitri>ten_sai)=%.3f"%w(S["bo_vitri"],S["ten_sai"]))
