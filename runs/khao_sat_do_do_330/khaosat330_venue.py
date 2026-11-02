import json,re,time,urllib.request,urllib.parse,os
def nz(s): return re.sub(r"\W+"," ",s.lower()).strip()
UA={"User-Agent":"thesis-survey/1.0"}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40)
M=json.load(open("meta.json"))
V=json.load(open("venue.json")) if os.path.exists("venue.json") else {}
for t,a in list(M.items()):
    if t in V or a.get("miss"): continue
    title=a["title"]
    r=dict(comment=a.get("comment"),jref=a.get("jref"),cr=[])
    try:
        d=json.load(get("https://api.crossref.org/works?"+urllib.parse.urlencode({"query.bibliographic":title,"rows":6,"select":"title,container-title,DOI,type,issued"})))
        for i in d["message"]["items"]:
            tt=(i.get("title") or [""])[0]
            if nz(tt)[:40]==nz(title)[:40]:
                r["cr"].append(((i.get("container-title") or [""])[0],i["DOI"],i.get("type"),(i.get("issued",{}).get("date-parts") or [[None]])[0][0]))
    except Exception as e: r["e"]=str(e)[:60]
    for c in r["cr"]:
        if c[1].startswith("10.18653/v1/"):
            aid=c[1].split("/")[-1]
            try:
                h=get(f"https://aclanthology.org/{aid}/").read().decode("utf8","ignore")
                m=re.search(r'citation_conference_title" content="([^"]+)"',h)
                r["acl"]=(aid,m.group(1) if m else "200")
            except Exception as e: r["acl"]=(aid,"LOI")
    V[t]=r; json.dump(V,open("venue.json","w"),ensure_ascii=False,indent=0)
    print(title[:55],"=>",[(c[0][:40],c[1],c[3]) for c in r["cr"]],r.get("acl"),(r["comment"] or "")[:50],flush=True)
    time.sleep(.6)
print("[xong venue]")
