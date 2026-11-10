#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dựng dataset + kernel Kaggle CPU cho phép kiểm điểm target T trên 8 mẫu val C1 (10/11/2026).

  python3 _bundles/rgtc_c1_t_10_11/make.py   (từ gốc kho)
  kg trang datasets create -p _bundles/rgtc_c1_t_10_11/ds --dir-mode zip
  kg trang kernels push -p _bundles/rgtc_c1_t_10_11/k
Dataset chứa dữ liệu AndroidControl đã xử lý: giữ riêng tư.
"""
import json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
B = ROOT / "_bundles" / "rgtc_c1_t_10_11"
DS, K = B / "ds", B / "k"
DS.mkdir(parents=True, exist_ok=True); K.mkdir(parents=True, exist_ok=True)
for f in ("harness/gate_b_rgtc.py", "harness/rgtc_c1_t_10_11.py", "runs/c1/c1_mau.jsonl",
          "runs/luoi/8_11/reward_c1/reward_cpu_8_11/reward_groups.jsonl",
          "runs/c1/exec8/c1data/c1_recs.jsonl", "runs/c1/exec8/c1data/ocr.jsonl"):
    shutil.copy2(ROOT / f, DS / Path(f).name)
(DS / "dataset-metadata.json").write_text(json.dumps({
    "title": "rgtc-c1-t-10-11", "id": "trangphngngc/rgtc-c1-t-10-11",
    "licenses": [{"name": "other"}], "isPrivate": True}, indent=1))
setup = r'''import sys, subprocess, os, shutil, glob
from pathlib import Path
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pycocoevalcap", "sacrebleu", "huggingface_hub"], check=True)
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
d = [p.parent for p in Path("/kaggle/input").rglob("rgtc_c1_t_10_11.py")]
assert len(d) == 1, d
d = d[0]; w = Path("/kaggle/working"); out = w / "c1_t"
for f in ("rgtc_c1_t_10_11.py", "gate_b_rgtc.py"):
    shutil.copy2(d / f, w / f)
log = w / "c1_t.log"
with log.open("w") as f:
    p = subprocess.Popen([sys.executable, "-u", str(w / "rgtc_c1_t_10_11.py"), "--data", str(d), "--forest", forest, "--out", str(out)],
                         stdout=f, stderr=subprocess.STDOUT, text=True)
    while p.poll() is None:
        time.sleep(60)
        print(time.strftime("%H:%M"), log.read_text(errors="replace")[-180:].replace("\n", " | "), flush=True)
print(log.read_text(errors="replace")[-7000:])
assert p.returncode == 0, p.returncode
shutil.make_archive(str(w / "c1_t_ket_qua"), "zip", str(out))
print("XONG")
'''
nb = {"cells": [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": c.splitlines(True)} for c in (setup, run)],
      "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}},
      "nbformat": 4, "nbformat_minor": 5}
(K / "rgtc-c1-t-10-11-cpu.ipynb").write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf8")
(K / "kernel-metadata.json").write_text(json.dumps({
    "id": "trangphngngc/rgtc-c1-t-10-11-cpu", "title": "rgtc-c1-t-10-11-cpu", "code_file": "rgtc-c1-t-10-11-cpu.ipynb",
    "language": "python", "kernel_type": "notebook", "is_private": "true", "enable_gpu": "false", "enable_internet": "true",
    "dataset_sources": ["trangphngngc/rgtc-c1-t-10-11", "trangphngngc/corenlp-360-jars"], "competition_sources": [], "kernel_sources": []}, indent=1))
print("đã dựng", B)
