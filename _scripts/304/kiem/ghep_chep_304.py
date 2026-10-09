import json,sys
sys.path.insert(0,"/mnt/d/Master/Thesis/_scripts/304/ra-sft-script")
import ra_exemplars as RA
R="/mnt/d/Master/Thesis/runs/ra304_T/"; S="/mnt/d/Master/Thesis/_scripts/304/ra-sft-script/"
L=lambda p:{(d["episode_id"],d["step_id"]):d for d in map(json.loads,open(p))}
ra=L(R+"pred_val_ra_k4.jsonl"); ck=L(S+"pred_ck500_vallon.jsonl"); ex=L(S+"ex_val_k4.jsonl")
n=0
with open(R+"pred_val_ghep.jsonl","w") as f:
    for k,d in ra.items():
        chep=any(RA.tok(e["sent"])==RA.tok(d["pred"]) for e in ex[k]["exemplars"])
        n+=chep
        f.write(json.dumps(dict(episode_id=k[0],step_id=k[1],pred=d["pred"] if chep else ck[k]["pred"]))+"\n")
print("chep",n,len(ra))
