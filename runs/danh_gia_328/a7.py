import json,os,subprocess,tempfile,sys,random,pickle,collections
import pycocoevalcap.spice.spice as SP
d=os.path.dirname(SP.__file__)
bd=pickle.load(open('ds328/base.pkl','rb'));gold=bd['gold']
K=sorted(gold);random.Random(7).shuffle(K)
samp=["Click on the search icon at the top of the screen","Click on the search icon","Swipe up","Scroll down to view more","Go back to the previous page","Open the Clock app","Click on technology","Type Grocery in the title section","Click on the three dots next to the Grocery alarm","Select the first option","Click on the Settings icon at the top right corner","Press the Settings icon","Click on the Settings tab","Click on the Play button","click on 3 star"]
inp=[]
for i,s in enumerate(samp): inp.append(dict(image_id=i,test=s,refs=[s]))
gs=[gold[k].strip() for k in K if gold[k].strip()]
for j,s in enumerate(gs): inp.append(dict(image_id=1000+j,test=s,refs=[s]))
os.makedirs('tmpsp',exist_ok=True)
json.dump(inp,open('tmpsp/in.json','w'))
out=os.path.abspath('tmpsp/out.json')
r=subprocess.run(['java','-jar','-Xmx8G','spice-1.0.jar',os.path.abspath('tmpsp/in.json'),'-cache',d+'/cache','-out',out,'-subset','-silent','-detailed'],cwd=d,capture_output=True,text=True)
print(r.returncode,r.stderr[-200:])
R=json.load(open(out))
print(list(R[0].keys()),list(R[0]['scores']['All'].keys()))
for x in R[:15]:
    print(x['image_id'],samp[x['image_id']],'=>',[ '|'.join(t['tuple']) for t in x['test_tuples']])
ns=[];oc=collections.Counter();n1=[]
for x in R[15:]:
    tt=[t['tuple'] for t in x['test_tuples']]
    ns.append(len(tt));c=collections.Counter(len(t) for t in tt)
    oc['obj']+=c[1];oc['attr']+=c[2];oc['rel']+=c[3];n1.append((c[1]>0,c[2]>0,c[3]>0))
import numpy as np
print('cau chuan',len(ns),'tuple TB',np.mean(ns),'trung vi',np.median(ns),'bang 0 %',100*np.mean([n==0 for n in ns]),'<=1 %',100*np.mean([n<=1 for n in ns]),oc)
print('co obj/attr/rel %',100*np.mean(n1,axis=0))
