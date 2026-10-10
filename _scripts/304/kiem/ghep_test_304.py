# Luật ghép chọn-khi-chép trên test: câu ra_k4 nếu trùng (tách từ) một trong 4 ví dụ, còn lại câu ck500.
# python ghep_test_304.py <pred_ra_k4_test.jsonl> <out_pred_ghep_test.jsonl>
import json, sys
sys.path.insert(0, "/mnt/d/Master/Thesis/_scripts/304/ra-sft-script")
import ra_exemplars as RA
S = "/mnt/d/Master/Thesis/_scripts/304/ra-sft-script/"
L = lambda p: {(d["episode_id"], d["step_id"]): d for d in map(json.loads, open(p, encoding="utf-8"))}
ra, ck, ex = L(sys.argv[1]), L(S + "pred_ck500_test.jsonl"), L(S + "ex_test_k4.jsonl")
assert len(ra) == 4463 and set(ra) <= set(ck) and set(ra) <= set(ex)
n = 0
with open(sys.argv[2], "w", encoding="utf-8") as f:
    for k, d in ra.items():
        chep = any(RA.tok(e["sent"]) == RA.tok(d["pred"]) for e in ex[k]["exemplars"])
        n += chep
        f.write(json.dumps(dict(episode_id=k[0], step_id=k[1], pred=d["pred"] if chep else ck[k]["pred"]), ensure_ascii=False) + "\n")
print("chép", n, "/", len(ra))
