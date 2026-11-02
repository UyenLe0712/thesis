import json,random,re,sys,collections,statistics as st
H="/mnt/d/Master/Thesis/harness"; sys.path.insert(0,H)
import grpo_luoi as GL
rows=[json.loads(l) for l in open(H+"/dg1_cache/train_ac/val_cham600.jsonl")]
tap=[r["target_instruction"].strip() for r in rows if r["action"]["action_type"] in("click","long_press") and r["target_instruction"].strip()]
non=[(r["target_instruction"].strip(),r["action"]["action_type"]) for r in rows if r["action"]["action_type"] not in("click","long_press","wait") and r["target_instruction"].strip()]
print(collections.Counter(a for _,a in non))
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.spice.spice import Spice
def run(c,g):
    tk=PTBTokenizer()
    G=tk.tokenize({i:[{"caption":x}] for i,x in enumerate(g)}); C=tk.tokenize({i:[{"caption":x}] for i,x in enumerate(c)})
    _,sc=Spice().compute_score(G,C); return sc
sc=run(tap,tap)
n=[x["All"]["numGT"] if "numGT" in x["All"] else None for x in sc]
print(sc[0]["All"].keys(),[k for k in sc[0].keys()])
ng=[x["All"].get("numRef",x["All"].get("numGT",x["All"].get("fn",0)+x["All"].get("tp",0))) for x in sc]
c=collections.Counter(ng); print("số tuple mỗi câu chuẩn (val chạm):",sorted(c.items())[:12],"trung vị",st.median(ng),"TB",sum(ng)/len(ng),"=0:",c[0]/len(ng))
print("tuple theo loại:",{k:sum((x[k].get('tp',0)+x[k].get('fn',0)) for x in sc)/len(sc) for k in sc[0] if k not in('All',)})
# bước không chạm: đổi hẳn thành câu chạm cùng từ vựng
rng=random.Random(0); rng.shuffle(non); non=non[:300]
g=[x for x,_ in non]
def to_click(s):
    w=re.sub(r"^(Scroll|Swipe|Go|Navigate|Move|Type|Enter|Input|Press|Slide)\b\s*(?:up|down|left|right|back|to|in|on)?\s*","",s,flags=re.I)
    return "Click on "+w if w else "Click on the screen."
c=[to_click(s) for s in g]
print(list(zip(g,c))[:6])
s1=run(c,g); v=[0.0 if x["All"]["f"]!=x["All"]["f"] else x["All"]["f"] for x in s1]
by=collections.defaultdict(list)
for (s,a),x in zip(non,v): by[a].append(x)
print("SPICE(câu chạm thay câu không chạm) theo loại:",{k:(len(q),round(sum(q)/len(q),3)) for k,q in by.items()},"TB",sum(v)/len(v))
G2=[x for x in g]
GL.M["cider"]=GL.CiderD(tap)
for me in ["bleu4","chrf"]:
    q=GL.diem(me,c,g); print(me,round(sum(q)/len(q),3))
q=GL.diem("cider",c,g); print("cider",round(sum(q)/len(q),3))
self_=[x["All"]["f"] for x in run(g,g)]; self_=[0 if y!=y else y for y in self_]; print("SPICE(câu chuẩn không chạm với chính nó)=",sum(self_)/len(self_),"=0:",sum(y==0 for y in self_)/len(self_))
