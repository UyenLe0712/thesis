# Lập bản ghi cho tác vụ AndroidControl S1 chưa thấy (không thuộc tập dạy, không thuộc tập kiểm), cùng định dạng
# test_ac/test.jsonl (build_test_data.py): câu + thao tác + mục tiêu từ HarrytheOrange, bỏ bước câu chuẩn rỗng.
import json, glob, os, ast, collections, sys
sys.path.insert(0, "/mnt/d/Master/Thesis/harness")
from build_test_data import app_of
K = "/mnt/d/Master/Thesis"
p = glob.glob(os.path.expanduser("~/.cache/huggingface/hub/datasets--HarrytheOrange--parsed_AndroidControl/snapshots/*/parsed_android_control.jsonl"))[0]
pl = lambda v: v if isinstance(v, list) else ast.literal_eval(v)
G = {}
for l in open(p, encoding="utf-8"):
    o = json.loads(l); G[int(o["episode_id"])] = dict(goal=o["goal"], steps=pl(o["step_instructions"]), acts=pl(o["actions"]))
tr = {json.loads(l)["episode_id"] for l in open(f"{K}/harness/dg1_cache/train_ac/train.jsonl")}
te = {json.loads(l)["episode_id"] for l in open(f"{K}/harness/dg1_cache/test_ac/test.jsonl")}
U = sorted(set(G) - tr - te)
sp = json.load(open(f"{K}/runs/split_chinh_thuc/splits.json"))
sp_of = {int(e): k for k, v in sp.items() for e in v}
recs, st = [], collections.Counter()
for e in U:
    g = G[e]; app = app_of(g["acts"], g["goal"])
    for s, (ins, act) in enumerate(zip(g["steps"], g["acts"])):
        if not (ins or "").strip():
            st["bo_rong"] += 1; continue
        recs.append(dict(episode_id=e, step_id=s, image=f"images/ep{e}_s{s}.png", goal=g["goal"], gold_instruction=ins,
                         action=act, app=app, history=g["steps"][:s], app_seen_in_train=None, split_chinh_thuc=sp_of.get(e)))
        st[act.get("action_type")] += 1
tap = [r for r in recs if r["action"].get("action_type") in ("click", "long_press") and "x" in r["action"]]
os.makedirs(f"{K}/_bundles/acu_build/kit", exist_ok=True)
with open(f"{K}/_bundles/acu_build/kit/acu_test.jsonl", "w", encoding="utf-8") as f:
    for r in recs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("tác vụ", len(U), "· bước", len(recs), "· chạm", len(tap), "· tác vụ có bước chạm", len({r['episode_id'] for r in tap}), dict(st))
print("split chính thức (bước chạm):", collections.Counter(r["split_chinh_thuc"] for r in tap))
print("app gán được (bước chạm):", sum(bool(r["app"]) for r in tap), "· số app", len({r['app'] for r in tap if r['app']}))
