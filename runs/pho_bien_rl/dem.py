import json,re,time,urllib.request,urllib.parse,os,sys
import xml.etree.ElementTree as ET
from pypdf import PdfReader
K=json.load(open("ungvien.json"))
IDX=[0,1,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,24,26,29,31,32,34,36,39,42,44,46,50,52,53,54,58,59,60,63,68,70,74,75,76,82,84,87,89,90,94,96,103,113,114,118,119,123,125,128,129,137,141,146,147,158,162,165]
T=[K[i]["title"] for i in IDX]
T+=["Prioritized Experience Replay","A Distributional Perspective on Reinforcement Learning","Implicit Quantile Networks for Distributional Reinforcement Learning","Noisy Networks for Exploration","Distributed Prioritized Experience Replay","Recurrent Experience Replay in Distributed Reinforcement Learning","Agent57: Outperforming the Atari Human Benchmark","Hindsight Experience Replay","Curiosity-driven Exploration by Self-supervised Prediction","Exploration by Random Network Distillation","Diversity is All You Need: Learning Skills without a Reward Function","Go-Explore: a New Approach for Hard-Exploration Problems","Dream to Control: Learning Behaviors by Latent Imagination","Mastering Atari with Discrete World Models","Learning Latent Dynamics for Planning from Pixels","CURL: Contrastive Unsupervised Representations for Reinforcement Learning","Image Augmentation Is All You Need: Regularizing Deep Reinforcement Learning from Pixels","Mastering Atari Games with Limited Data","Offline Reinforcement Learning with Implicit Q-Learning","A Minimalist Approach to Offline Reinforcement Learning","MOPO: Model-based Offline Policy Optimization","Advantage-Weighted Regression: Simple and Scalable Off-Policy Reinforcement Learning","AWAC: Accelerating Online Reinforcement Learning with Offline Datasets","Critic Regularized Regression","Maximum a Posteriori Policy Optimisation","Implementation Matters in Deep Policy Gradients: A Case Study on PPO and TRPO","What Matters In On-Policy Reinforcement Learning? A Large-Scale Empirical Study","The Surprising Effectiveness of PPO in Cooperative, Multi-Agent Games","Phasic Policy Gradient","Deep Reinforcement Learning at the Edge of the Statistical Precipice","Training language models to follow instructions with human feedback","Deep reinforcement learning from human preferences"]
A={"PPO":r"\bPPO\b|Proximal Policy Optimi[sz]ation","TRPO":r"\bTRPO\b|Trust Region Policy","DQN":r"\bDQN\b|Deep Q.Networks?","DDPG":r"\bDDPG\b|Deep Deterministic Policy","SAC":r"\bSAC\b|Soft Actor.Critic","A3C":r"\bA3C\b|Asynchronous Advantage","A2C":r"\bA2C\b","TD3":r"\bTD3\b","REINFORCE":r"\bREINFORCE\b","GAE":r"\bGAE\b|Generali[sz]ed Advantage","Q-learning (nói chung)":r"Q.learning","Double DQN":r"Double (DQN|Q)|\bDDQN\b","Rainbow":r"\bRainbow\b","MCTS":r"\bMCTS\b|Monte.Carlo Tree","Behavior Cloning":r"Behaviou?ral? Cloning|\bBC\b","GAIL":r"\bGAIL\b","CEM":r"\bCEM\b|[Cc]ross.[Ee]ntropy [Mm]ethod","ES":r"Evolution(ary)? Strateg|\bCMA.ES\b","NPG":r"\bNPG\b|[Nn]atural [Pp]olicy [Gg]radient","IMPALA":r"\bIMPALA\b","ACER":r"\bACER\b","CQL":r"\bCQL\b","BCQ":r"\bBCQ\b","IQL":r"\bIQL\b","AWR/AWAC":r"\bAWR\b|\bAWAC\b","Decision Transformer":r"Decision Transformer","MPO":r"\bMPO\b","SARSA":r"\bSARSA\b|\bSarsa\b","DPG":r"\bDPG\b","Soft Q-learning":r"Soft Q.[Ll]earning"}
SELF={"Proximal Policy":"PPO","Trust Region Policy":"TRPO","Playing Atari":"DQN","Continuous control with deep":"DDPG","Soft Actor-Critic":"SAC","Asynchronous Methods":"A3C|A2C","Addressing Function":"TD3","High-Dimensional Continuous Control":"GAE","Double Q":"Double DQN","Rainbow":"Rainbow","Generative Adversarial Imitation":"GAIL","Evolution Strategies":"ES","IMPALA":"IMPALA","Sample Efficient Actor-Critic":"ACER","Conservative Q":"CQL","Off-Policy Deep Reinforcement Learning without":"BCQ","Implicit Q":"IQL","Advantage-Weighted":"AWR/AWAC","AWAC":"AWR/AWAC","Decision Transformer":"Decision Transformer","Maximum a Posteriori":"MPO","Deterministic Policy Gradient":"DPG","Deep Energy-Based":"Soft Q-learning"}
def nz(s): return re.sub(r"\W+"," ",s.lower()).strip()
def tim(t):
    q=urllib.parse.urlencode({"search_query":'ti:"%s"'%re.sub(r'[^\w\s-]',' ',t),"max_results":5})
    for _ in range(4):
        try:
            x=urllib.request.urlopen("https://export.arxiv.org/api/query?"+q,timeout=40).read();break
        except Exception as e: time.sleep(15); x=None
    if not x: return None
    ns={"a":"http://www.w3.org/2005/Atom"}
    for e in ET.fromstring(x).findall("a:entry",ns):
        if nz(e.find("a:title",ns).text)==nz(t) or nz(t)[:50]==nz(e.find("a:title",ns).text)[:50]:
            return e.find("a:id",ns).text.split("/abs/")[-1].split("v")[0]
R=json.load(open("kq.json")) if os.path.exists("kq.json") else {}
for i,t in enumerate(T):
    if t in R: continue
    time.sleep(3.2); aid=tim(t)
    if not aid: R[t]={"aid":None}; print("KHONG",t[:60],flush=True); json.dump(R,open("kq.json","w"),ensure_ascii=False); continue
    f=f"pdf/{aid}.pdf"
    try:
        if not os.path.exists(f):
            time.sleep(3.2); urllib.request.urlretrieve(f"https://export.arxiv.org/pdf/{aid}",f)
        txt=" ".join((p.extract_text() or "") for p in PdfReader(f).pages[:40])
        m=[x.start() for x in re.finditer(r"\n\s*(References|REFERENCES|Bibliography)\b",txt)]
        body=txt[:m[-1]] if m and m[-1]>len(txt)*.3 else txt
        sf=set()
        for k,v in SELF.items():
            if k.lower() in t.lower(): sf|=set(v.split("|"))
        R[t]={"aid":aid,"n":len(body),"c":{a:len(re.findall(p,body)) for a,p in A.items() if a not in sf},"self":sorted(sf)}
        print(i,len(T),aid,t[:50],flush=True)
    except Exception as e:
        R[t]={"aid":aid,"err":str(e)[:100]}; print("LOI",t[:50],e,flush=True)
    json.dump(R,open("kq.json","w"),ensure_ascii=False)
print("[xong]",len(T))
