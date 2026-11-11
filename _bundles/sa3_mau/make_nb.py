# -*- coding: utf-8 -*-
"""Kernel Kaggle T4×2 cho SA-SPICE-v3 kernel 1: hoà S1 → probe ghép SFT-cont → greedy + 8 mẫu trên 1.000 câu nhắc TRAIN-v3.

  python3 _bundles/sa3_mau/make_nb.py
  kg trang2 datasets create -p _bundles/sa3_mau/ds --dir-mode zip
  kg trang2 kernels push -p _bundles/sa3_mau/k --accelerator NvidiaTeslaT4
Kết quả: /kaggle/working/sa3_mau_out.zip (mau_0/1.jsonl, *.probe.json, log).
"""
import json, os, hashlib

H = os.path.dirname(os.path.abspath(__file__))
DS, K = os.path.join(H, "ds"), os.path.join(H, "k")
os.makedirs(K, exist_ok=True)
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
M = {f: md5(os.path.join(DS, f)) for f in ("sa3_mau.py", "grpo_spice.py", "build_branch_data.py", "train_v3.jsonl")}
CAT_H = float(os.environ.get("CAT_H", "7.3"))
TIEP = os.environ.get("TIEP") == "1"   # 11/11: chạy tiếp shard 0 (chết ở câu 157) chia đôi cho hai GPU
KID = "trangphuongngoc/sa3-mau-k1b" if TIEP else "trangphuongngoc/sa3-mau-k1"
if TIEP:
    M["mau_0_cu.jsonl"] = md5(os.path.join(DS, "mau_0_cu.jsonl"))

c0 = f'''import subprocess, sys, os, time, threading, glob, json, shutil, hashlib, zipfile
T_NB = time.time()
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh(f"{{sys.executable}} -m pip install -q 'transformers==5.20.2' 'peft==0.21.2' accelerate 2>&1 | tail -3")
sh(f"{{sys.executable}} -m pip uninstall -y torchao 2>&1 | tail -1")
assert sh(f\'\'\'{{sys.executable}} -c "import transformers, peft, torch; print(transformers.__version__, peft.__version__, torch.__version__, torch.cuda.device_count(), torch.cuda.get_device_name(0)); assert (transformers.__version__, peft.__version__) == ('5.20.2', '0.21.2'); assert torch.cuda.device_count() == 2" \'\'\') == 0, "DUNG: moi truong"
print("✅ moi truong", flush=True)
'''

c1 = f'''W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
D = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/sa3_mau.py", recursive=True) if "/notebooks/" not in p]
assert len(D) == 1, D; D = D[0]
for f, h in {M!r}.items():
    assert md5(f"{{D}}/{{f}}") == h, f"DUNG: {{f}} lech md5"
for f in ("sa3_mau.py", "grpo_spice.py", "build_branch_data.py"):
    shutil.copyfile(f"{{D}}/{{f}}", f"{{W}}/{{f}}")
assert len(glob.glob(f"{{D}}/images/*.png")) == 1000
ENV = {{**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1", "PYTORCH_ALLOC_CONF": "expandable_segments:True"}}
MERGED = f"{{W}}/s1_merged"
r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", D, "--adapter", f"{{D}}/adapter_s1_seed101", "--merged", MERGED], cwd=W, capture_output=True, text=True, env=ENV)
print((r.stdout + r.stderr)[-800:], flush=True); assert r.returncode == 0, "DUNG: hoa S1 loi"
CAT = 3600 * {CAT_H}
def chay(cmd, log, gpu):
    t0 = time.time()
    with open(log, "a") as f:
        q = subprocess.Popen(cmd, cwd=W, stdout=f, stderr=subprocess.STDOUT, env={{**ENV, "CUDA_VISIBLE_DEVICES": str(gpu)}})
        while q.poll() is None:
            time.sleep(120)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"{{(time.time()-T_NB)/3600:5.2f}} h · gpu{{gpu}} · {{os.path.basename(log)}} · {{L[-1][:120] if L else 'chua co dong'}}", flush=True)
            if time.time() - T_NB > CAT:
                print("⛔ het gio, dung de Output kip luu", flush=True); q.terminate(); q.wait(); return None
    print(f"--- {{os.path.basename(log)}} · ma thoat {{q.returncode}} · {{(time.time()-t0)/3600:.2f}} h", flush=True)
    if q.returncode != 0:
        print(open(log, errors="ignore").read()[-2500:], flush=True)
    return q.returncode
ARGS = ["--data", D, "--merged", MERGED, "--sft", f"{{D}}/sft_final"]
'''

c2 = '''# thử 2 câu nhắc (có probe ghép) trước lượt đủ
assert chay(["python", "-u", "sa3_mau.py", *ARGS, "--n", "2", "--probe-n", "2", "--out", f"{W}/thu.jsonl"], f"{W}/thu.log", 0) == 0, "DUNG: thu loi"
print(open(f"{W}/thu.log").read()[-1500:], flush=True)
T = [json.loads(l) for l in open(f"{W}/thu.jsonl")]
assert len(T) == 2 and all(len(t["mau"]) == 8 and t["greedy"] for t in T), "DUNG: thu sai dinh dang"
print("✅ thu", T[0]["gold"], "|", T[0]["greedy"], "|", T[0]["mau"][:3], flush=True)
'''

c3 = '''RC = {}
def shard(i):
    RC[i] = chay(["python", "-u", "sa3_mau.py", *ARGS, "--shard", str(i), "--nshard", "2", "--out", f"{W}/mau_{i}.jsonl"], f"{W}/mau_{i}.log", i)
th = [threading.Thread(target=shard, args=(i,)) for i in (0, 1)]
[t.start() for t in th]; [t.join() for t in th]
for i in (0, 1):
    n = sum(1 for _ in open(f"{W}/mau_{i}.jsonl")) if os.path.exists(f"{W}/mau_{i}.jsonl") else 0
    print(f"shard {i}: ma thoat {RC.get(i)} · {n}/500 dong", flush=True)
    print(json.load(open(f"{W}/mau_{i}.jsonl.probe.json")) if os.path.exists(f"{W}/mau_{i}.jsonl.probe.json") else "khong co probe", flush=True)
'''

c4 = '''with zipfile.ZipFile(f"{W}/sa3_mau_out.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for p in glob.glob(f"{W}/*.jsonl") + glob.glob(f"{W}/*.probe.json") + glob.glob(f"{W}/*.log"):
        z.write(p, os.path.basename(p))
print("zip", os.path.getsize(f"{W}/sa3_mau_out.zip") // 1024, "KB", flush=True)
shutil.rmtree(f"{W}/s1_merged", ignore_errors=True)
'''

if TIEP:
    c2 = '''# chạy tiếp: mỗi phần bắt đầu từ 156 dòng cũ của shard 0 ⇒ không sinh lại
for i in (0, 1):
    shutil.copyfile(f"{D}/mau_0_cu.jsonl", f"{W}/mau_0_p{i}.jsonl")
print("dong cu", sum(1 for _ in open(f"{W}/mau_0_p0.jsonl")), flush=True)
'''
    c3 = '''RC = {}
def phan(i):
    RC[i] = chay(["python", "-u", "sa3_mau.py", *ARGS, "--shard", "0", "--nshard", "2", "--part", str(i), "--npart", "2", "--out", f"{W}/mau_0_p{i}.jsonl"], f"{W}/mau_0_p{i}.log", i)
th = [threading.Thread(target=phan, args=(i,)) for i in (0, 1)]
[t.start() for t in th]; [t.join() for t in th]
for i in (0, 1):
    n = sum(1 for _ in open(f"{W}/mau_0_p{i}.jsonl"))
    print(f"phan {i}: ma thoat {RC.get(i)} · {n} dong (156 cu + ~172 moi)", flush=True)
    print(json.load(open(f"{W}/mau_0_p{i}.jsonl.probe.json")), flush=True)
'''
nb = {"nbformat": 4, "nbformat_minor": 5,
      "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}, "language_info": {"name": "python"}},
      "cells": [{"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "id": f"o{i}", "source": c.splitlines(keepends=True)}
                for i, c in enumerate((c0, c1, c2, c3, c4))]}
for i, c in enumerate((c0, c1, c2, c3, c4)):
    compile(c, f"o{i}", "exec")
json.dump(nb, open(os.path.join(K, "sa3-mau-k1.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"id": KID, "title": KID.split("/")[1], "code_file": "sa3-mau-k1.ipynb",
           "language": "python", "kernel_type": "notebook", "is_private": "true", "enable_gpu": "true", "enable_internet": "true",
           "dataset_sources": ["trangphuongngoc/sa3-mau-train-v3"], "competition_sources": [], "kernel_sources": []},
          open(os.path.join(K, "kernel-metadata.json"), "w"), indent=1)
print("ok", M)
