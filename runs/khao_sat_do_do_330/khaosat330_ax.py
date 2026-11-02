import json,re,time,urllib.parse,urllib.request
import xml.etree.ElementTree as ET
NS={"a":"http://www.w3.org/2005/Atom"}
Q=['abs:"reinforcement learning" AND abs:"text-to-SQL"','abs:"reinforcement learning" AND abs:"semantic parsing" AND abs:reward','abs:"reinforcement learning" AND abs:"data-to-text"','abs:"reinforcement learning" AND abs:"code summarization"','abs:"instruction generation" AND abs:navigation AND abs:speaker','abs:reward AND abs:BLEU AND abs:"reinforcement learning"','abs:reward AND abs:ROUGE AND abs:"reinforcement learning"','abs:reward AND abs:CIDEr','abs:reward AND abs:SPICE AND abs:caption','abs:reward AND abs:BERTScore','abs:reward AND abs:CLIPScore','abs:reward AND abs:"BLEURT"','abs:reward AND abs:METEOR AND abs:"reinforcement learning"','abs:reward AND abs:listener AND abs:generation AND abs:speaker','abs:GRPO AND abs:caption','abs:"self-critical sequence training"','abs:GRPO AND abs:"LLM judge"','abs:reinforcement AND abs:"GUI" AND abs:"instruction generation"']
out={}
for q in Q:
    time.sleep(3.5)
    u="https://export.arxiv.org/api/query?"+urllib.parse.urlencode({"search_query":q,"max_results":15,"sortBy":"relevance"})
    for k in range(4):
        try: r=ET.fromstring(urllib.request.urlopen(u,timeout=40).read()); break
        except Exception as e: r=None; time.sleep(15)
    if r is None: print("LOI",q); continue
    out[q]=[(e.find("a:id",NS).text.split("/abs/")[-1].split("v")[0]," ".join(e.find("a:title",NS).text.split()),e.find("a:published",NS).text[:4]) for e in r.findall("a:entry",NS)]
    print("##",q,flush=True)
    for x in out[q]: print(" ",x[0],x[2],x[1][:90],flush=True)
json.dump(out,open("ax_raw.json","w"),ensure_ascii=False,indent=0)
