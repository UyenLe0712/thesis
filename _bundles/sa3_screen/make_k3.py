# -*- coding: utf-8 -*-
"""SA-SPICE-v3 kernel 3 (Kaggle CPU): sàng 9 reward offline trên TRAIN-v3 bằng harness/sa3_reward_screen.py.
Chạy SAU khi đã có đủ score_k0..8_raw.jsonl (622 dòng) ở runs/sa_spice_v3/cham_k2/{k0123,k45678}/out.

  python3 _bundles/sa3_screen/make_k3.py
  kg trang datasets create -p _bundles/sa3_screen/ds --dir-mode zip
  kg trang kernels push -p _bundles/sa3_screen/k
"""
import json, os, shutil, hashlib, subprocess, sys

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.dirname(os.path.abspath(__file__))
DS, K = os.path.join(H, "ds"), os.path.join(H, "k")
USER = "trangphngngc"
os.makedirs(DS, exist_ok=True); os.makedirs(K, exist_ok=True)
shutil.copy2(f"{R}/runs/sa_spice_v3/split/train_v3.jsonl", f"{DS}/train_v3.jsonl")
for i in (0, 1):
    shutil.copy2(f"{R}/runs/sa_spice_v3/mau_k1/mau_{i}.jsonl", f"{DS}/mau_{i}.jsonl")
for k in range(9):
    src = f"{R}/runs/sa_spice_v3/cham_k2/{'k0123' if k < 4 else 'k45678'}/out/score_k{k}_raw.jsonl"
    n = sum(1 for _ in open(src))
    assert n == 622, (src, n)
    shutil.copy2(src, f"{DS}/score_k{k}_raw.jsonl")
for f in ("sa3_reward_screen.py", "grpo_luoi.py", "grpo_spice.py", "h4_spice_tuple_7_11.py", "sa3_action_verify.py", "build_branch_data.py"):
    shutil.copy2(f"{R}/harness/{f}", f"{DS}/{f}")
assert subprocess.run([sys.executable, f"{DS}/sa3_reward_screen.py", "--selftest"]).returncode == 0
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
M = {f: md5(f"{DS}/{f}") for f in sorted(os.listdir(DS)) if f.endswith((".py", ".jsonl"))}
json.dump({"title": "sa3-screen-train-v3", "id": f"{USER}/sa3-screen-train-v3", "licenses": [{"name": "other"}], "isPrivate": True},
          open(f"{DS}/dataset-metadata.json", "w"), indent=1)

c0 = '''import sys, subprocess, os, shutil, glob, json, time, hashlib, zipfile
from pathlib import Path
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pycocoevalcap", "sacrebleu"], check=True)
from pycocoevalcap.spice import spice
libs = Path(spice.__file__).resolve().parent / "lib"; libs.mkdir(exist_ok=True)
for name, size in {"stanford-corenlp-3.6.0.jar": 7270741, "stanford-corenlp-3.6.0-models.jar": 378116526}.items():
    have = libs / name
    if not have.is_file() or have.stat().st_size != size:
        c = [p for p in Path("/kaggle/input").rglob(name) if p.stat().st_size == size]
        assert c, f"DUNG: thieu {name}"
        shutil.copy2(c[0], have)
_v = subprocess.run(["bash", "-c", "java -version 2>&1"], capture_output=True, text=True).stdout
if 'version "1.8' not in _v:
    subprocess.run("apt-get update -qq && apt-get install -y -qq openjdk-8-jre-headless", shell=True, check=True)
    _j = sorted(glob.glob("/usr/lib/jvm/*8*")); assert _j, "DUNG: khong co Java 8"
    os.environ["JAVA_HOME"] = _j[0]; os.environ["PATH"] = _j[0] + "/bin:" + os.environ["PATH"]
print("Java", subprocess.run(["java", "-version"], capture_output=True, text=True).stderr.splitlines()[:1], "· CPU", os.cpu_count(), flush=True)
'''
c1 = f'''W = "/kaggle/working"
D = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/sa3_reward_screen.py", recursive=True) if "/notebooks/" not in p]
assert len(D) == 1, D; D = D[0]
for f, h in {M!r}.items():
    assert hashlib.md5(open(f"{{D}}/{{f}}", "rb").read()).hexdigest() == h, f"DUNG: {{f}} lech md5"
CODE = f"{{W}}/code"; os.makedirs(CODE, exist_ok=True)
for f in glob.glob(f"{{D}}/*.py"):
    shutil.copy2(f, CODE)
assert subprocess.run([sys.executable, f"{{CODE}}/sa3_reward_screen.py", "--selftest"]).returncode == 0, "DUNG: selftest"
OUT = f"{{W}}/screen"; os.makedirs(OUT, exist_ok=True)
log = f"{{W}}/screen.log"
cmd = [sys.executable, "-u", f"{{CODE}}/sa3_reward_screen.py", "--data", D, "--mau", D, "--score", D, "--out", f"{{OUT}}/sa3_screen.json"]
t0 = time.time()
with open(log, "w") as f:
    p = subprocess.Popen(cmd, cwd=CODE, stdout=f, stderr=subprocess.STDOUT, env={{**os.environ, "PYTHONUNBUFFERED": "1"}})
    while p.poll() is None:
        time.sleep(120)
        L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
        print(f"{{(time.time()-t0)/60:5.1f}} phut · {{L[-1][:150] if L else 'chua co dong'}}", flush=True)
print(open(log, errors="ignore").read()[-6000:], flush=True)
print("ma thoat", p.returncode, flush=True)
'''
c2 = '''with zipfile.ZipFile(f"{W}/sa3_screen_out.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for p in glob.glob(f"{OUT}/*") + [log]:
        z.write(p, os.path.basename(p))
print("zip", os.path.getsize(f"{W}/sa3_screen_out.zip") // 1024, "KB", flush=True)
assert p.returncode == 0 if False else True
'''
c2 = c2.replace("assert p.returncode == 0 if False else True\n", "")
cells = (c0, c1, c2)
for i, c in enumerate(cells):
    compile(c, f"o{i}", "exec")
nb = {"nbformat": 4, "nbformat_minor": 5,
      "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}, "language_info": {"name": "python"}},
      "cells": [{"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "id": f"o{i}", "source": c.splitlines(keepends=True)}
                for i, c in enumerate(cells)]}
json.dump(nb, open(f"{K}/sa3-screen-k3.ipynb", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"id": f"{USER}/sa3-screen-k3", "title": "sa3-screen-k3", "code_file": "sa3-screen-k3.ipynb", "language": "python",
           "kernel_type": "notebook", "is_private": "true", "enable_gpu": "false", "enable_internet": "true",
           "dataset_sources": [f"{USER}/sa3-screen-train-v3", f"{USER}/corenlp-360-jars"], "competition_sources": [], "kernel_sources": []},
          open(f"{K}/kernel-metadata.json", "w"), indent=1)
print("ok", len(M), "tep")
