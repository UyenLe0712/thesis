"""Dựng dataset nhỏ luoi-kit cho một tài khoản: python make_kit.py <tài khoản kaggle> ; rồi kg <tk> datasets create -p kit_<tk> (hoặc version)."""
import os, sys, json, shutil
u = sys.argv[1]
H = os.path.dirname(os.path.abspath(__file__))
K = os.path.join(H, "..", "..")
d = os.path.join(H, f"kit_{u}")
os.makedirs(d, exist_ok=True)
for f in ("grpo_codien.py", "grpo_ppo.py", "sft_tiep.py", "tai_dung_cham.py",
          "grpo_moi_b1.py", "thuong_moi.py", "metric_exec.py"):   # 6/11: mã mới B1 (DPO/MRT/SPG/GSPO…) + B3 (thưởng mới)
    shutil.copy(os.path.join(K, "harness", f), d)
for f in ("grpo_moi_b2.py", "grpo_moi_b4.py", "thuong_t6.py", "grpo_tu_base.py"):   # 7/11: B4 (ORPO/DPO bán trực tuyến/GPG), T6, xuất phát Base                                       # B2 (MIXER/SeqGAN/…) khi đã có
    if os.path.exists(os.path.join(K, "harness", f)):
        shutil.copy(os.path.join(K, "harness", f), d)
shutil.copy(os.path.join(H, "..", "moi_b3", "ds", "descriptors_ten.jsonl"), d)   # tên vàng cho thưởng ten_loai
for ten, p in (("raw_s1.jsonl", "runs/score_s1_seed101_raw.jsonl"), ("raw_ck500.jsonl", "runs/grpo_spice/score_ck500_test_raw.jsonl"),
               ("raw_xao101.jsonl", "runs/xao101/test/score_ck500_xao101_test_raw.jsonl"),
               ("raw_ck202.jsonl", "runs/grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl")):
    shutil.copy(os.path.join(K, p), os.path.join(d, ten))
json.dump({"title": "luoi-kit", "id": f"{u}/luoi-kit", "licenses": [{"name": "CC0-1.0"}]}, open(os.path.join(d, "dataset-metadata.json"), "w"))
print("đã dựng", d, sorted(os.listdir(d)))
