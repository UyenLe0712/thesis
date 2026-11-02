import json,urllib.request,urllib.parse,time
# Mỗi chủ đề: lọc tiêu đề+tóm tắt chứa đồng thời các cụm, sort trích dẫn, 15 bài đầu
Q={"cap":['"reinforcement learning" caption','"policy gradient" caption','"self-critical"'],
"vid":['"reinforcement learning" "video captioning"'],
"sum":['"reinforcement learning" summarization','"policy gradient" summarization'],
"nmt":['"reinforcement learning" "machine translation"','"minimum risk training"'],
"gen":['"reinforcement learning" "question generation"','"reinforcement learning" paraphrase','"reinforcement learning" "text generation"','"reinforcement learning" "dialogue generation" reward','"reinforcement learning" "data-to-text"','"code summarization" "reinforcement learning"'],
"sql":['"reinforcement learning" "text-to-SQL"','"reinforcement learning" "semantic parsing"'],
"vln":['"instruction generation" navigation speaker'],
"rew":['reward BLEU "reinforcement learning" generation','reward ROUGE "reinforcement learning"','reward CIDEr','reward SPICE caption']}
out={}
for m,qs in Q.items():
  for q in qs:
    for k in q and [q]:
        terms=q
        u="https://api.openalex.org/works?"+urllib.parse.urlencode({"filter":"title_and_abstract.search:"+terms.replace('" "','" AND "').replace(' "',' AND "').replace('" ','" AND ') if False else "title_and_abstract.search:"+terms,"per-page":15,"sort":"cited_by_count:desc","select":"title,cited_by_count,publication_year,doi,primary_location,type"})
        try:
            r=json.load(urllib.request.urlopen(u,timeout=60))
        except Exception as e:
            print("LOI",q,e);continue
        out[m+"|"+q]=[dict(t=w["title"],c=w["cited_by_count"],y=w["publication_year"],v=((w.get("primary_location") or {}).get("source") or {}).get("display_name"),ty=w["type"]) for w in r["results"]]
        print(q,r["meta"]["count"],flush=True); time.sleep(.5)
json.dump(out,open("oa_raw2.json","w"),ensure_ascii=False,indent=0)
