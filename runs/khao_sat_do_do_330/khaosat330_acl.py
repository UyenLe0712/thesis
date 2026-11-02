import re,sys,urllib.request,json,html
UA={"User-Agent":"Mozilla/5.0"}
for i in sys.argv[1:]:
    try:
        h=urllib.request.urlopen(urllib.request.Request(f"https://aclanthology.org/{i}/",headers=UA),timeout=30).read().decode("utf8","ignore")
        t=re.search(r"<title>(.*?) - ACL Anthology",h); b=re.search(r'booktitle = &#34;(.*?)&#34;',h) or re.search(r'journal = &#34;(.*?)&#34;',h); p=re.search(r'pages = &#34;(.*?)&#34;',h); y=re.search(r'year = &#34;(\d+)',h)
        print(i,"|",html.unescape(t.group(1)) if t else None,"|",html.unescape(b.group(1)).replace("{","").replace("}","")[:80] if b else None,"|",y.group(1) if y else None,"|",p.group(1) if p else None)
    except Exception as e: print(i,"LOI",e)
