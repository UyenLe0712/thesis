import json,re,time,urllib.request,urllib.parse,os,sys
import xml.etree.ElementTree as ET
from pypdf import PdfReader
sys.path.insert(0,'.')
from khaosat330_seed import S,GOC
NS={"a":"http://www.w3.org/2005/Atom","x":"http://arxiv.org/schemas/atom"}
def nz(s): return re.sub(r"\W+"," ",s.lower()).strip()
def api(q):
    for k in range(5):
        try:
            return ET.fromstring(urllib.request.urlopen("https://export.arxiv.org/api/query?"+q,timeout=40).read())
        except Exception as e:
            time.sleep(10+10*k)
    return None
def meta(e):
    g=lambda p:(e.find(p,NS).text if e.find(p,NS) is not None else None)
    return dict(aid=g("a:id").split("/abs/")[-1].split("v")[0],title=" ".join(g("a:title").split()),comment=g("x:comment"),jref=g("x:journal_ref"),year=g("a:published")[:4])
def tim(t):
    time.sleep(3.2)
    if t.startswith("id:"):
        r=api(urllib.parse.urlencode({"id_list":t[3:]}))
        es=r.findall("a:entry",NS) if r is not None else []
        return meta(es[0]) if es else None
    tt=re.sub(r'[^\w\s-]',' ',t); tt=" ".join(tt.split())
    r=api(urllib.parse.urlencode({"search_query":'ti:"%s"'%tt,"max_results":5}))
    if r is None: return None
    for e in r.findall("a:entry",NS):
        m=meta(e)
        if nz(m["title"])==nz(t) or nz(t)[:45]==nz(m["title"])[:45]: return m
    return None
def body(aid):
    f=f"txt/{aid.replace('/','_')}.txt"
    if os.path.exists(f): return True
    p=f"pdf/{aid.replace('/','_')}.pdf"
    if not os.path.exists(p):
        time.sleep(3.2); urllib.request.urlretrieve(f"https://export.arxiv.org/pdf/{aid}",p)
    t="\n".join((pg.extract_text() or "") for pg in PdfReader(p).pages[:40])
    open(f,"w").write(t); return True
R=json.load(open("meta.json")) if os.path.exists("meta.json") else {}
items=[(m,t) for m,l in S.items() for t in l]+[("goc",t) for t in GOC]
if os.path.exists("tangB.json"):
    items+=[("B",t) for t in json.load(open("tangB.json"))]
for i,(m,t) in enumerate(items):
    if t in R and (R[t].get("aid") or R[t].get("miss")): continue
    a=tim(t)
    if not a: R[t]=dict(mang=m,miss=True); print("KHONG",m,t[:70],flush=True)
    else:
        a["mang"]=m
        try: body(a["aid"])
        except Exception as e: a["err"]=str(e)[:80]; print("LOI",t[:60],e,flush=True)
        R[t]=a; print(i,len(items),m,a["aid"],a["title"][:60],flush=True)
    json.dump(R,open("meta.json","w"),ensure_ascii=False,indent=0)
print("[xong]")
