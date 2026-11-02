# trích đoạn: độ đo đứng gần từ khoá thưởng/tối ưu trong phần trước tài liệu tham khảo
import json,re,sys
M=json.load(open("meta.json"))
KW=re.compile(r"reward|self-critical|SCST|REINFORCE|policy gradient|directly optimi[sz]|optimi[sz]\w* (for |the |on |towards? )?|maximi[sz]\w*|minimum risk|\bMRT\b|risk|scoring function|cost function|train\w* (on|with|to optimi)|\bRL\b|critic",re.I)
ME={"CIDEr":r"CIDE[Rr]|CIDEnt","BLEU":r"BLEU|\bGLEU\b|\bbleu\b","ROUGE":r"ROUGE|\brouge\b","METEOR":r"METEOR","SPICE":r"SPICE|SPIDEr","chrF":r"chrF|CharacTER|character n-gram","WER/TER/ED":r"\bTER\b|\bWER\b|edit distance|Levenshtein","BERTS":r"BERT[- ]?[Ss]core|BLEURT|\bBEER\b|\bSimiLe\b|SIMILE|word mover|\bWMD\b|learned metric|semantic similarity","CLIP":r"CLIP[- ]?S\b|CLIPScore|CLIP reward|PAC-S|CLIP-based","listener":r"listener|retrieval|discriminab|comprehension|speaker-listener|discriminator|contrastive","exec":r"execut|query result|denotation|unit test|test case","LLM":r"LLM judge|GPT-4|LLM[- ]based|critique|verifier|reward model|human feedback|human rating|preference","entail":r"entail|saliency|question[- ]answer|QA[- ]based","element":r"\bIoU\b|click|bounding box|coverage|grounding reward|action type"}
def sents(t):
    t=re.sub(r"-\n","",t); t=re.sub(r"\s+"," ",t)
    return re.split(r"(?<=[\.\?\!])\s+(?=[A-Z\(\[])",t)
out=[]
for k,a in M.items():
    if a.get("miss") or a.get("mang")=="goc": continue
    try: t=open(f"txt/{a['aid'].replace('/','_')}.txt").read()
    except: out.append(f"\n=== {a['aid']} {a['title'][:70]} [KHONG TEXT]"); continue
    m=[x.start() for x in re.finditer(r"\n\s*(References|REFERENCES|Bibliography)\b",t)]
    b=t[:m[-1]] if m and m[-1]>len(t)*.3 else t
    S=sents(b)
    out.append(f"\n=== [{a['mang']}] {a['aid']} {a['title'][:75]} (n={len(b)})")
    for me,p in ME.items():
        c=0;tot=len(re.findall(p,b))
        if not tot: continue
        if not [1 for s in S if re.search(p,s) and re.search(r"reward|self-critical|SCST|optimi[sz]|maximi[sz]|\brisk\b|\bMRT\b|REINFORCE|policy gradient",s,re.I)]: continue
        hits=[s for s in S if re.search(p,s) and KW.search(s) and re.search(r"reward|self-critical|SCST|optimi[sz]|maximi[sz]|\brisk\b|\bMRT\b|REINFORCE|policy gradient|train\w* (on|with|to)",s,re.I) and len(s)<600]
        hr=[s for s in hits if re.search(r"reward|optimi[sz]",s,re.I)]
        pick=(hr+[s for s in hits if s not in hr])[:(2 if me in("CIDEr","SPICE") else 1)]
        out.append(f"  {me}({tot}/{len(hits)}):"+" // ".join(re.sub(r'\s+',' ',s)[:170] for s in pick))
open("trich.txt","w").write("\n".join(out)); print(len("\n".join(out)))
