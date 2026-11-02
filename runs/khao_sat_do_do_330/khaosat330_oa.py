import json,urllib.request,urllib.parse,time
Q=["reinforcement learning image captioning","self-critical sequence training","reinforcement learning video captioning","reinforcement learning abstractive summarization","reinforcement learning neural machine translation","policy gradient sequence generation reward metric","reinforcement learning question generation","reinforcement learning text-to-SQL","reinforcement learning paraphrase generation","navigation instruction generation speaker reinforcement","reinforcement learning data-to-text generation","reward function text generation evaluation metric optimization"]
out={};seen=set()
for q in Q:
    u="https://api.openalex.org/works?"+urllib.parse.urlencode({"search":q,"per-page":25,"sort":"cited_by_count:desc","filter":"from_publication_date:2015-01-01,to_publication_date:2026-10-31","select":"title,cited_by_count,publication_year,doi,primary_location,type"})
    r=json.load(urllib.request.urlopen(u,timeout=60))
    out[q]=[dict(t=w["title"],c=w["cited_by_count"],y=w["publication_year"],doi=w["doi"],v=((w.get("primary_location") or {}).get("source") or {}).get("display_name"),ty=w["type"]) for w in r["results"]]
    print(q,len(out[q]),r["meta"].get("cost_usd"),flush=True)
    time.sleep(1)
json.dump(out,open("oa_raw.json","w"),ensure_ascii=False,indent=0)
