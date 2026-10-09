# Xuất ex_test_k4.jsonl + ex_val_k4.jsonl đúng định dạng xuat() của ra_build.py (CPU).
import sys, json
sys.path.insert(0,"_scripts/304/ra-sft-script"); import ra_exemplars as RA
doc=lambda p:[json.loads(l) for l in open(p,encoding="utf-8")]
B="/home/uyenle/fgrb_p1/bundle"; O="_scripts/304/ra-sft-script"
va=doc(f"{B}/p1_val_rows.jsonl"); vep={r["episode_id"] for r in va}
kho=RA.Kho(doc("harness/dg1_cache/train_ac/train_tru_val.jsonl"),loai_ep=vep); print("kho",len(kho.tr),flush=True)
la=lambda r:(r.get("action") or {}).get("action_type") in ("click","long_press") and "x" in r["action"]
ot=lambda o:{w for it in (o or {"items":[]})["items"][:24] for w in RA.tok(it.get("text",""))}
for ten,recs,oc,dich in (("test",doc("harness/dg1_cache/test_ac/test.jsonl"),"harness/dg1_cache/test_ac/ocr.jsonl",False),("val",va,f"{B}/ocr.jsonl",True)):
    O_={o["image"]:o for o in doc(oc)}; n=h=0
    with open(f"{O}/ex_{ten}_k4.jsonl","w",encoding="utf-8") as f:
        for r in recs:
            if not la(r): continue
            ex=[dict(sent=e["sent"],goal=e["goal"],prev=e["prev"]) for e in kho.cho_test(dict(goal=r["goal"],history=r.get("history") or []),4,ot(O_.get(r["image"])))]
            n+=1
            if dich: h+=any(RA.tok(e["sent"])==RA.tok(r.get("target_instruction") or "") for e in ex)
            f.write(json.dumps({"episode_id":r["episode_id"],"step_id":r["step_id"],"exemplars":ex},ensure_ascii=False)+"\n")
    print(ten,n,"click · khối chứa đích",round(100*h/max(n,1),1),flush=True)
