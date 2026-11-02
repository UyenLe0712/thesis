# Kiểm đặc tính độ đo trên câu chuẩn val (không dùng câu mô hình, không dùng test): biến đổi câu chuẩn có kiểm soát.
import json,random,re,sys,os,time
H="/mnt/d/Master/Thesis/harness"; sys.path.insert(0,H)
import grpo_luoi as GL, grpo_spice as GS
rows=[json.loads(l) for l in open(H+"/dg1_cache/train_ac/val_cham600.jsonl")]
gold=[r["target_instruction"].strip() for r in rows if r["action"]["action_type"] in("click","long_press") and r["target_instruction"].strip()]
tr=[json.loads(l) for l in open(H+"/dg1_cache/train_ac/train_tru_val.jsonl")]
refs=[r["target_instruction"].strip() for r in tr if r["action"]["action_type"] in("click","long_press") and r["target_instruction"].strip()]
rd=random.Random(20261101); rd.shuffle(refs); refs_df=refs[:3991]
GL.M["cider"]=GL.CiderD(refs_df)
from pycocoevalcap.rouge.rouge import Rouge; GL.M["rouge"]=Rouge()
from pycocoevalcap.meteor.meteor import Meteor; GL.M["meteor"]=Meteor()
wl=[len(GL.tok(g)) for g in gold]; 
all_w=[len(GL.tok(g)) for g in refs]
import statistics as st
print("số câu val chạm",len(gold),"số từ trung vị",st.median(wl))
print("tập dạy chạm:",len(refs),"trung vị",st.median(all_w),"≤3 từ %.1f%%"%(100*sum(w<=3 for w in all_w)/len(all_w)),"<4 từ",sum(w<4 for w in all_w),"≤5 từ %.1f%%"%(100*sum(w<=5 for w in all_w)/len(all_w)),"p10,p90",sorted(all_w)[len(all_w)//10],sorted(all_w)[len(all_w)*9//10])
POS=re.compile(r"\s+(?:(?:at|on|in|near|from|to|under|above|below|beside|next to)\s+(?:the\s+)?(?:very\s+)?(?:top|bottom|left|right|upper|lower|center|centre|middle|corner)\b.*)$",re.I)
VERB=re.compile(r"^(Click on|Click|Tap on|Tap|Press on|Press|Select|Choose|Open|Touch|Hit)\b\s*(?:on\s+)?(the\s+)?",re.I)
def tach(g):
    g0=g.rstrip(". ")
    m=VERB.match(g0)
    if not m: return None
    rest=g0[m.end():]
    p=POS.search(rest)
    name=rest[:p.start()] if p else rest
    pos=p.group(0).strip() if p else ""
    if not name.strip(): return None
    return m.group(1),name.strip(),pos,(m.group(2) or "")
parts=[(g,tach(g)) for g in gold]; parts=[(g,t) for g,t in parts if t]
print("tách được",len(parts),"/",len(gold),"có mệnh đề vị trí",sum(1 for g,t in parts if t[2]))
SYN={"click on":"Tap on","click":"Tap","tap on":"Click on","tap":"Click","press on":"Click on","press":"Tap","select":"Choose","choose":"Select","open":"Launch","touch":"Tap","hit":"Press"}
FL={"top":"bottom","bottom":"top","left":"right","right":"left","upper":"lower","lower":"upper"}
rng=random.Random(0); rng.shuffle(parts); parts=parts[:400]
names=[t[1] for g,t in parts]
V={k:[] for k in ["goc","td_swipe","td_long","td_back","nontap_click"]}
Pv={"vitri_sai":[],"goc_p":[]}
for i,(g,(v,n,p,d)) in enumerate(parts):
    tail=(" "+p) if p else ""
    V["goc"].append(g)
    V["td_swipe"].append(f"Swipe up on {d}{n}{tail}.")
    V["td_long"].append(f"Long press on {d}{n}{tail}.")
    V["td_back"].append(f"Go back from {d}{n}{tail}.")
    V["nontap_click"].append(f"Click on {d}{n}{tail}.")
    if p:
        pp=re.sub(r"\b(top|bottom|left|right|upper|lower)\b",lambda m:FL[m.group(1).lower()],p,flags=re.I)
        if pp!=p: Pv["vitri_sai"].append(f"{v} {d}{n} {pp}."); Pv["goc_p"].append(g)
print("ví dụ:");
for k in V: print(" ",k,":",V[k][3])
print("  vitri_sai:",Pv["vitri_sai"][0],"<-",Pv["goc_p"][0])
G=V["goc"]
ME=sys.argv[1].split(",")
OUT=json.load(open("stress2.json")) if os.path.exists("stress2.json") else {}
if "bertscore" in ME: GL.dung_bo_cham("bertscore","")
for me in ME:
    t=time.time();R={}
    for k in V: R[k]=GL.diem(me,V[k],G)
    R["vitri_sai"]=GL.diem(me,Pv["vitri_sai"],Pv["goc_p"]); R["goc_p"]=GL.diem(me,Pv["goc_p"],Pv["goc_p"])
    OUT[me]=R; json.dump(OUT,open("stress2.json","w"))
    m=lambda a:sum(a)/len(a)
    print(me,{k:round(m(R[k]),3) for k in R},"giây",round(time.time()-t),flush=True)
