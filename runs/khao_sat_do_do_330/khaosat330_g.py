import sys,re,json,os
from pypdf import PdfReader
M=json.load(open('meta.json'))
key,pat,n,w=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
fs=[]
if os.path.exists(f'ngoai/{key}.pdf'):
    tf=f'ngoai/{key}.txt'
    if not os.path.exists(tf): open(tf,'w').write("\n".join((p.extract_text() or "") for p in PdfReader(f'ngoai/{key}.pdf').pages))
    fs=[(key,tf)]
else:
    for t,a in M.items():
        if (key.lower() in t.lower() or key==a.get('aid')) and a.get('aid'):
            fs.append((a['aid']+' '+a['title'][:60],'txt/'+a['aid'].replace('/','_')+'.txt'))
for name,f in fs:
    s=re.sub(r'\s+',' ',open(f).read()); print('##',name,len(s))
    last=-10**9;c=0
    for m in re.finditer(pat,s):
        if m.start()-last<w: continue
        print('  ..',s[max(0,m.start()-w):m.end()+w]); last=m.start();c+=1
        if c>=n: break
