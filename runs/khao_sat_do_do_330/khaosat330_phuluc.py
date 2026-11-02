import json,re
from khaosat330_nhan import R,KHONG
M={a["aid"]:(t,a) for t,a in json.load(open("meta.json")).items() if a.get("aid")}
V=json.load(open("venue.json"))
def venue(t,a):
    v=V.get(t,{})
    ev=""
    if v.get("acl"): return (re.sub(r"^Proceedings of the \S+ (Annual Meeting of the )?","",v["cr"][0][0] if v["cr"] and v["cr"][0][0] else "")[:0]+"ACL Anthology "+v["acl"][0], "A")
    for c in v.get("cr",[]):
        if c[0] and "arXiv" not in c[0]:
            n=c[0]
            n=re.sub(r"\s*\(.*?\)","",n)
            return (f"{n[:58]}, {c[3]}","C")
    cm=(v.get("comment") or "")+" "+(v.get("jref") or "")
    m=re.search(r"(NeurIPS|NIPS|ICLR|ICML|CVPR|ICCV|ECCV|AAAI|IJCAI|ACL|EMNLP|NAACL|EACL|COLING|BMVC|ICPR|IEEE ACCESS|Findings)[^,;.]{0,30}",cm)
    if m: return (m.group(0).strip()[:50],"K")
    return ("preprint hoặc chưa kiểm","-")
rows=[]
for k,(m,l) in R.items():
    t,a=M[k]; ve,e=venue(t,a); rows.append((m,k,a["title"],ve,e,l,a["mang"]=="B"))
for k in KHONG:
    t,a=M[k]; ve,e=venue(t,a); rows.append((a["mang"],k,a["title"],ve,e,"(không dùng độ đo làm thưởng)",a["mang"]=="B"))
json.dump(rows,open("phuluc.json","w"),ensure_ascii=False,indent=0)
import collections
print(collections.Counter(r[4] for r in rows)); print([r[1:4] for r in rows if r[4]=="-"][:60])
