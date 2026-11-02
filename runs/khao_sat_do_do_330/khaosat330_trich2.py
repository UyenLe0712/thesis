import json,re
M=json.load(open("meta.json"))
ME={"CID":r"CIDE[Rr]-?[DR]?\b|CIDEnt","BLE":r"BLEU|\bGLEU\b|\bbleu\b","ROU":r"ROUGE|\brouge\b","MET":r"METEOR","SPI":r"SPICE|SPIDEr","CHR":r"chrF","TER":r"\bTER\b|\bWER\b|edit distance|Levenshtein","EMB":r"BERT[- ]?[Ss]core|BLEURT|\bBEER\b|\bSimiLe\b|SIMILE|[Ww]ord [Mm]over|\bWMD\b|learned metric|semantic similarity|cosine","CLP":r"CLIP[- ]?S\b|CLIPScore|CLIP[- ]based|PAC-S","DIS":r"listener|self-retrieval|retrieval model|discriminab|comprehension|discriminator","EXE":r"execution|query result|denotation|unit test","LLM":r"LLM judge|judge|reward model|human feedback|human rating|verifier|critique","ENT":r"entail|saliency|question[- ]answer","GRA":r"scene graph|RadGraph|entity match|graph match|F1 score","ELE":r"\bIoU\b|bounding box|coverage|click|action type"}
RW=r"reward|optimi[sz]\w*|maximi[sz]\w*|self-critical|SCST|\brisk\b|\bMRT\b|REINFORCE|policy gradient|\bRL\b"
out=[]
for k,a in M.items():
    if a.get("miss") or a.get("mang")=="goc": continue
    try:t=open(f"txt/{a['aid'].replace('/','_')}.txt").read()
    except: out.append(f"=== {a['aid']} {a.get('title','')[:60]} [NOTEXT]");continue
    m=[x.start() for x in re.finditer(r"\n\s*(References|REFERENCES|Bibliography)\b",t)]
    b=t[:m[-1]] if m and m[-1]>len(t)*.3 else t
    b=re.sub(r"-\n","",b); b=re.sub(r"\s+"," ",b)
    out.append(f"=== [{a['mang']}] {a['aid']} {a['title'][:62]} ({a.get('year')})")
    L=[]
    for me,p in ME.items():
        tot=len(re.findall(p,b))
        if not tot: continue
        best=None
        for x in re.finditer(p,b):
            w=b[max(0,x.start()-70):x.end()+70]
            if re.search(r"reward",w,re.I): best=w;break
        if best is None:
            for x in re.finditer(p,b):
                w=b[max(0,x.start()-70):x.end()+70]
                if re.search(RW,w): best=w;break
        L.append(f"{me}{tot}"+(f":{best}" if best else ""))
    # tách: dòng có đoạn và dòng chỉ số
    out.append("  n: "+" ".join(x for x in L if ":" not in x))
    out+= ["  "+x for x in L if ":" in x and x[:3] in("CID","SPI","BLE","ROU","MET","EMB","CLP","DIS","EXE","LLM","GRA","ELE","ENT","TER")]
open("trich2.txt","w").write("\n".join(out)); print(len("\n".join(out)),len([1 for l in out if l.startswith("===")]))
