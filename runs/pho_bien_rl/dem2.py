import json,re
from pypdf import PdfReader
R=json.load(open("kq.json"))
AC={"PPO":r"\bPPO\b","TRPO":r"\bTRPO\b","DQN":r"\bDQN\b","DDPG":r"\bDDPG\b","SAC":r"\bSAC\b","A3C":r"\bA3C\b","A2C":r"\bA2C\b","TD3":r"\bTD3\b","REINFORCE":r"\bREINFORCE\b","GAE":r"\bGAE\b","Double DQN":r"\bDDQN\b","Rainbow":r"\bRainbow\b","MCTS":r"\bMCTS\b","Behavior Cloning":r"\bBC\b","GAIL":r"\bGAIL\b","CEM":r"\bCEM\b","ES":r"\bCMA-?ES\b","NPG":r"\bNPG\b","IMPALA":r"\bIMPALA\b","ACER":r"\bACER\b","CQL":r"\bCQL\b","BCQ":r"\bBCQ\b","IQL":r"\bIQL\b","AWR/AWAC":r"\bAWR\b|\bAWAC\b","MPO":r"\bMPO\b","SARSA":r"\bSARSA\b|\bSarsa\b","DPG":r"\bDPG\b"}
AI={"PPO":r"proximal\s+policy\s+optimi[sz]ation","TRPO":r"trust\s+region\s+policy","DQN":r"deep\s+q[-\s]*(networks?|learning)","DDPG":r"deep\s+deterministic\s+policy","SAC":r"soft\s+actor[-\s]*critic","A3C":r"asynchronous\s+advantage","TD3":r"twin\s+delayed","GAE":r"generali[sz]ed\s+advantage","Q-learning (nói chung)":r"q[-\s]learning","Double DQN":r"double\s+(dqn|q)","MCTS":r"monte[-\s]carlo\s+tree","Behavior Cloning":r"behaviou?ral?\s+cloning","GAIL":r"generative\s+adversarial\s+imitation","CEM":r"cross[-\s]entropy\s+method","ES":r"evolution(ary)?\s+strateg","NPG":r"natural\s+(policy\s+)?gradient","Decision Transformer":r"decision\s+transformer","Soft Q-learning":r"soft\s+q[-\s]learning","Actor-critic (nói chung)":r"actor[-\s]critic","Policy gradient (nói chung)":r"policy[-\s]gradient","DPG":r"deterministic\s+policy\s+gradient"}
OUT={}
for t,v in R.items():
    if "c" not in v: OUT[t]={"aid":v.get("aid")};continue
    txt=" ".join((p.extract_text() or "") for p in PdfReader(f"pdf/{v['aid']}.pdf").pages[:40])
    m=[x.start() for x in re.finditer(r"\n\s*(References|REFERENCES|Bibliography)\b",txt)]
    b=txt[:m[-1]] if m and m[-1]>len(txt)*.3 else txt
    sf=set(v["self"]); c={}
    for a in set(AC)|set(AI):
        if a in sf: continue
        n=len(re.findall(AC[a],b)) if a in AC else 0
        if a in AI: n+=len(re.findall(AI[a],b,re.I))
        c[a]=n
    OUT[t]={"aid":v["aid"],"c":c,"self":sorted(sf)}
json.dump(OUT,open("kq2.json","w"),ensure_ascii=False,indent=0)
ok=[v for v in OUT.values() if "c" in v]
rows=[]
for a in sorted(set(AC)|set(AI)):
    den=[v for v in ok if a in v["c"]]
    rows.append((a,sum(v["c"][a]>=2 for v in den),sum(v["c"][a]>=5 for v in den),len(den)))
for r in sorted(rows,key=lambda x:-x[1]): print(f"{r[0]:30s} >=2:{r[1]:3d} >=5:{r[2]:3d} /{r[3]}")
