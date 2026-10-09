# 304 — phép đo CPU trước GPU: khối truy hồi k=4 trên test có mang câu đúng mà ck500 chưa viết ra không.
import sys, json, collections, time
sys.path.insert(0, "_scripts/304/ra-sft-script"); sys.path.insert(0, "harness")
import ra_exemplars as RA
from ctg_grpo import tok as ctok  # không dùng; giữ tokenizer RA
t0=time.time()
doc=lambda p:[json.loads(l) for l in open(p,encoding="utf-8")]
va=doc("runs/vallon289/valdata/val_lon_recs.jsonl"); vep={r["episode_id"] for r in va}
kho=RA.Kho(doc("harness/dg1_cache/train_ac/train_tru_val.jsonl"),loai_ep=vep)
print("kho",len(kho.tr),len(kho.eid),"bỏ",len(vep),flush=True)
te=[r for r in doc("harness/dg1_cache/test_ac/test.jsonl") if (r.get("action") or {}).get("action_type") in ("click","long_press") and "x" in r["action"]]
ocr={o["image"]:o for o in doc("harness/dg1_cache/test_ac/ocr.jsonl")}
ck={(d["episode_id"],d["step_id"]):d["pred"] for d in doc("runs/grpo_spice/pred_ck500_test.jsonl")}
print("test click",len(te),"chung kho",len({r['episode_id'] for r in te}&set(kho.eid)),flush=True)
T=lambda s:RA.tok(s)
st=collections.Counter(); out=[]
for i,r in enumerate(te):
    o=ocr.get(r["image"]); ot={w for it in (o or {"items":[]})["items"][:24] for w in RA.tok(it.get("text",""))}
    ex=kho.cho_test(dict(goal=r["goal"],history=r.get("history") or []),4,ot)
    g=T(r["gold_instruction"]); c=T(ck[(r["episode_id"],r["step_id"])])
    hit=any(T(e["sent"])==g for e in ex); top=bool(ex) and T(ex[0]["sent"])==g
    st["n"]+=1; st["hit"]+=hit; st["top1"]+=top; st["ck_dung"]+=c==g
    st["hit_ck_dung"]+=hit and c==g; st["hit_ck_sai"]+=hit and c!=g
    st["ck_chep"]+=any(T(e["sent"])==c for e in ex)
    out.append(dict(episode_id=r["episode_id"],step_id=r["step_id"],exemplars=ex,ck=ck[(r["episode_id"],r["step_id"])],gold=r["gold_instruction"]))
    if (i+1)%1000==0: print(i+1,round(time.time()-t0),"s",flush=True)
json.dump(out,open("_scripts/304/kiem/ex_test_k4_kiem.json","w"),ensure_ascii=False)
n=st["n"]; print({k:(v,round(100*v/n,1)) for k,v in st.items()})
