# Khối 4 câu ví dụ cho 2.736 bước chạm AitZ (CPU), y hệt xuat_ex_304.py: cùng kho (train_tru_val, bỏ episode val),
# cùng khoá truy hồi (goal + history + chữ của 24 dòng OCR đầu). Tự kiểm: dựng lại 30 bước chạm đầu của test
# AndroidControl phải trùng ex_test_k4.jsonl đã dùng cho R3.
import sys, json
K = "/mnt/d/Master/Thesis"
sys.path.insert(0, f"{K}/_scripts/304/ra-sft-script"); import ra_exemplars as RA
doc = lambda p: [json.loads(l) for l in open(p, encoding="utf-8")]
vep = {r["episode_id"] for r in doc("/home/uyenle/fgrb_p1/bundle/p1_val_rows.jsonl")}
kho = RA.Kho(doc(f"{K}/harness/dg1_cache/train_ac/train_tru_val.jsonl"), loai_ep=vep); print("kho", len(kho.tr), flush=True)
la = lambda r: (r.get("action") or {}).get("action_type") in ("click", "long_press") and "x" in r["action"]
ot = lambda o: {w for it in (o or {"items": []})["items"][:24] for w in RA.tok(it.get("text", ""))}
def khoi(r, O_):
    return [dict(sent=e["sent"], goal=e["goal"], prev=e["prev"]) for e in kho.cho_test(dict(goal=r["goal"], history=r.get("history") or []), 4, ot(O_.get(r["image"])))]
# tự kiểm trên AndroidControl
O_ = {o["image"]: o for o in doc(f"{K}/harness/dg1_cache/test_ac/ocr.jsonl")}
cu = {(d["episode_id"], d["step_id"]): d["exemplars"] for d in doc(f"{K}/_scripts/304/ra-sft-script/ex_test_k4.jsonl")}
T = [r for r in doc(f"{K}/harness/dg1_cache/test_ac/test.jsonl") if la(r)][:30]
ok = sum(khoi(r, O_) == cu[(r["episode_id"], r["step_id"])] for r in T); print(f"[tự kiểm AC] {ok}/30 trùng ex_test_k4", flush=True)
assert ok == 30
A = f"{K}/runs/aitz/build_v3_25_10/out"
O_ = {o["image"]: o for o in doc(f"{A}/ocr.jsonl")}
R = [r for r in doc(f"{A}/test.jsonl") if la(r)]; assert len(R) == 2736, len(R)
n = h = 0
with open(f"{K}/_bundles/aitz_ace/kit/ex_aitz_k4.jsonl", "w", encoding="utf-8") as f:
    for r in R:
        ex = khoi(r, O_); n += 1
        h += any(RA.tok(e["sent"]) == RA.tok(r["gold_instruction"]) for e in ex)
        f.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "exemplars": ex}, ensure_ascii=False) + "\n")
print("aitz", n, "bước chạm · khối chứa đúng câu chuẩn", round(100*h/n, 1), "%", flush=True)
