#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dựng dataset + kernel Kaggle CPU cho phép đo Gate B của RGTC-SPICE (10/11/2026).

  python3 _bundles/gate_b_10_11/make.py   (từ gốc kho)
  kg trang datasets create -p _bundles/gate_b_10_11/ds --dir-mode zip
  kg trang kernels push -p _bundles/gate_b_10_11/k
Dataset chứa dữ liệu AndroidControl đã xử lý: giữ riêng tư.
"""
import glob, gzip, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
B = ROOT / "_bundles" / "gate_b_10_11"
DS, K = B / "ds", B / "k"
DS.mkdir(parents=True, exist_ok=True); K.mkdir(parents=True, exist_ok=True)
SRC = ROOT / "harness" / "dg1_cache" / "train_ac"

shutil.copy2(ROOT / "harness" / "gate_b_rgtc.py", DS / "gate_b_rgtc.py")
shutil.copy2(SRC / "train_tru_val.jsonl", DS / "train_tru_val.jsonl")
if not (DS / "ocr.jsonl.gz").exists():
    with open(SRC / "ocr.jsonl", "rb") as a, gzip.open(DS / "ocr.jsonl.gz", "wb", compresslevel=6) as b:
        shutil.copyfileobj(a, b)

ex = set()
fs = [p for pat in ("runs/**/*prompt_keys*.json", "_bundles/**/*prompt_keys*.json") for p in glob.glob(str(ROOT / pat), recursive=True)]
for f in fs:
    for k in json.load(open(f)):
        ex.add(str(k).split("_")[0])
json.dump(sorted(ex), open(DS / "excl_ep.json", "w"))
print("prompt_keys", len(fs), "episode loại", len(ex))

(DS / "dataset-metadata.json").write_text(json.dumps({
    "title": "gate-b-rgtc-10-11", "id": "trangphngngc/gate-b-rgtc-10-11",
    "licenses": [{"name": "other"}], "isPrivate": True}, indent=1))

setup = r'''import sys, subprocess, os, shutil, glob
from pathlib import Path
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pycocoevalcap", "huggingface_hub"], check=True)
from pycocoevalcap.spice import spice
libs = Path(spice.__file__).resolve().parent / "lib"; libs.mkdir(exist_ok=True)
for name, size in {"stanford-corenlp-3.6.0.jar": 7270741, "stanford-corenlp-3.6.0-models.jar": 378116526}.items():
    have = libs / name
    if not have.is_file() or have.stat().st_size != size:
        c = [p for p in Path("/kaggle/input").rglob(name) if p.stat().st_size == size]
        assert c, "thiếu " + name
        shutil.copy2(c[0], have)
v = subprocess.run(["bash", "-c", "java -version 2>&1"], capture_output=True, text=True).stdout
if 'version "1.8' not in v:
    subprocess.run("apt-get update -qq && apt-get install -y -qq openjdk-8-jre-headless", shell=True, check=True)
    j = sorted(glob.glob("/usr/lib/jvm/*8*")); assert j, "không có Java 8"
    os.environ["JAVA_HOME"] = j[0]; os.environ["PATH"] = j[0] + "/bin:" + os.environ["PATH"]
print(subprocess.run(["java", "-version"], capture_output=True, text=True).stderr.splitlines()[:1], flush=True)
'''
run = r'''import sys, subprocess, shutil, time, json
from pathlib import Path
from huggingface_hub import hf_hub_download
forest = hf_hub_download("HarrytheOrange/parsed_AndroidControl", "all_forest_dict.zip", repo_type="dataset")
d = [p.parent for p in Path("/kaggle/input").rglob("gate_b_rgtc.py")]
assert len(d) == 1, d
d = d[0]; w = Path("/kaggle/working"); out = w / "gate_b"
shutil.copy2(d / "gate_b_rgtc.py", w / "gate_b_rgtc.py")
assert subprocess.run([sys.executable, str(w / "gate_b_rgtc.py"), "--selftest"]).returncode == 0
log = w / "gate_b.log"
with log.open("w") as f:
    p = subprocess.Popen([sys.executable, "-u", str(w / "gate_b_rgtc.py"), "--root", str(d), "--forest", forest,
                          "--exclude", str(d / "excl_ep.json"), "--out", str(out)], stdout=f, stderr=subprocess.STDOUT, text=True)
    while p.poll() is None:
        time.sleep(120)
        print(time.strftime("%H:%M"), log.read_text(errors="replace")[-180:].replace("\n", " | "), flush=True)
print(log.read_text(errors="replace")[-9000:])
assert p.returncode == 0, p.returncode
r = json.loads((out / "gate_b_rgtc.json").read_text())
assert r["pool_steps"] == 49046 and r["pool_episodes"] == 10726, (r["pool_steps"], r["pool_episodes"])
shutil.make_archive(str(w / "gate_b_ket_qua"), "zip", str(out))
print("XONG")
'''
nb = {"cells": [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": c.splitlines(True)} for c in (setup, run)],
      "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}},
      "nbformat": 4, "nbformat_minor": 5}
(K / "gate-b-rgtc-10-11-cpu.ipynb").write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf8")
(K / "kernel-metadata.json").write_text(json.dumps({
    "id": "trangphngngc/gate-b-rgtc-10-11-cpu", "title": "gate-b-rgtc-10-11-cpu", "code_file": "gate-b-rgtc-10-11-cpu.ipynb",
    "language": "python", "kernel_type": "notebook", "is_private": "true", "enable_gpu": "false", "enable_internet": "true",
    "dataset_sources": ["trangphngngc/gate-b-rgtc-10-11", "trangphngngc/corenlp-360-jars"], "competition_sources": [], "kernel_sources": []}, indent=1))
print("đã dựng", B)
