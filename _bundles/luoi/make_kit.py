"""Dựng dataset nhỏ luoi-kit cho một tài khoản: python make_kit.py <tài khoản kaggle> ; rồi kg <tk> datasets create -p kit_<tk> (hoặc version)."""
import os, sys, json, shutil
u = sys.argv[1]
H = os.path.dirname(os.path.abspath(__file__))
K = os.path.join(H, "..", "..")
d = os.path.join(H, f"kit_{u}")
os.makedirs(d, exist_ok=True)
for f in ("grpo_codien.py", "grpo_ppo.py", "sft_tiep.py", "tai_dung_cham.py"):
    shutil.copy(os.path.join(K, "harness", f), d)
for ten, p in (("raw_s1.jsonl", "runs/score_s1_seed101_raw.jsonl"), ("raw_ck500.jsonl", "runs/grpo_spice/score_ck500_test_raw.jsonl"),
               ("raw_xao101.jsonl", "runs/xao101/test/score_ck500_xao101_test_raw.jsonl"),
               ("raw_ck202.jsonl", "runs/grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl")):
    shutil.copy(os.path.join(K, p), os.path.join(d, ten))
json.dump({"title": "luoi-kit", "id": f"{u}/luoi-kit", "licenses": [{"name": "CC0-1.0"}]}, open(os.path.join(d, "dataset-metadata.json"), "w"))
print("đã dựng", d, sorted(os.listdir(d)))
