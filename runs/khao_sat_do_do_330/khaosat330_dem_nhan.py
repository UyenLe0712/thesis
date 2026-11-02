import json,re,collections
from khaosat330_nhan import R,KHONG
M={a["aid"]:a for a in json.load(open("meta.json")).values() if a.get("aid")}
HO=["CIDEr","ROUGE","BLEU","METEOR","SPICE","SPIDEr","BCMR","chrF","TER_WER","EMB","CLIP","GRAPH","ENTAIL","QA","EXEC","LISTENER","DISC","LEARNEDIRL","HUMAN","LLMJ","RULE"]
EV={"CIDEr":r"CIDE[Rr]","ROUGE":r"ROUGE|\brouge\b","BLEU":r"BLEU|\bbleu\b","METEOR":r"METEOR","SPICE":r"SPICE","chrF":r"chrF|CHRF|CHR F","EMB":r"BERT[- ]?[Ss]core"}
miss=[k for k in R if k not in M]; print("thiếu meta",miss)
def tier(k): return M[k]["mang"]=="B"
def y(k):
    if k=="acl_dmo": return 2024
    if k=="iccv_entangled": return 2019
    return int(M[k]["year"])
cnt=collections.Counter(); by=collections.defaultdict(collections.Counter); ty=collections.defaultdict(collections.Counter); per=collections.defaultdict(collections.Counter)
for k,(m,l) in R.items():
    for h in l.split():
        cnt[h]+=1; by[h][m]+=1; ty[h]["B" if tier(k) else "A"]+=1
        yy=y(k); per[h]["<=2019" if yy<=2019 else ("2020-23" if yy<=2023 else ">=2024")]+=1
N=len(R); print("bài có thưởng",N,"bài không",len(KHONG),"tổng đọc",N+len(KHONG))
print("theo mảng",collections.Counter(m for m,_ in R.values()))
print("tầng",collections.Counter("B" if tier(k) else "A" for k in R), "năm",collections.Counter("<=2019" if y(k)<=2019 else ("2020-23" if y(k)<=2023 else ">=2024") for k in R))
# chỉ đánh giá
ev=collections.Counter()
allk=list(R)+KHONG
for k in allk:
    a=M[k]
    try: t=open(f"txt/{a['aid'].replace('/','_')}.txt").read()
    except: continue
    q=[x.start() for x in re.finditer(r"\n\s*(References|REFERENCES|Bibliography)\b",t)]
    b=t[:q[-1]] if q and q[-1]>len(t)*.3 else t
    lab=R.get(k,("",""))[1].split()
    for h,p in EV.items():
        c=len(re.findall(p,b))
        if c>=3 and h not in lab and not (h=="SPICE" and "SPIDEr" in lab): ev[h]+=1
for h in HO:
    print(h,cnt[h],dict(by[h]),dict(ty[h]),dict(per[h]),"| chỉ đánh giá/nhắc≥3:",ev.get(h,"-"))
json.dump({"cnt":cnt,"by":by,"ty":ty,"per":per,"ev":ev,"N":N},open("dem.json","w"),ensure_ascii=False,indent=0)
# bài có SPICE/SPIDEr
print([k for k,(m,l) in R.items() if "SPICE" in l or "SPIDEr" in l])
print("GRPO/LLM từ 2025:",[ (k,R[k][1]) for k in R if y(k)>=2025 and M[k]["mang"]!="sql"][:40])
