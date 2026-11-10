#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepare a private, CPU-only Kaggle dataset+kernel for C1 SPICE reward screening.

From repository root:
    python3 _bundles/luoi/make_reward_cpu_8_11.py
The generated data are *validation* trajectories from an existing C1 run, not test.
Do not publish the dataset as public without reviewing AndroidControl licensing.
"""
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "_bundles" / "reward_cpu_8_11"
DATA = BASE / "ds"
KERNEL = BASE / "k"
DATA.mkdir(parents=True, exist_ok=True)
KERNEL.mkdir(parents=True, exist_ok=True)

src = ROOT / "runs" / "c1"
files = [("c1_mau.jsonl", src / "c1_mau.jsonl")]
files += [(f"score_k{i}_raw.jsonl", src / "exec8" / "c1score" / f"score_k{i}_raw.jsonl") for i in range(1, 9)]
files += [("reward_cpu_8_11.py", ROOT / "harness" / "reward_cpu_8_11.py")]
for filename, path in files:
    assert path.is_file(), path
    shutil.copy2(path, DATA / filename)

assert (DATA / "c1_mau.jsonl").read_text(encoding="utf8").count("\n") == 400
for i in range(1, 9):
    assert (DATA / f"score_k{i}_raw.jsonl").read_text(encoding="utf8").count("\n") == 249

# Kaggle source code/data must be kept private unless licensing is established.
dataset = {
    "title": "Thesis C1 GRPO-SPICE Reward CPU Validation",
    "id": "trangphngngc/grpo-spice-reward-c1-8-11",
    "subtitle": "C1 validation samples and cached executable outcomes for CPU-only reward audit",
    "description": "Private, derived validation data for research; no test-set results. Do not publish publicly.",
    "licenses": [{"name": "other"}],
    "isPrivate": True,
}
(DATA / "dataset-metadata.json").write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf8")

setup = r'''import sys, subprocess, os, shutil
from pathlib import Path
def run(cmd):
    print("+", " ".join(map(str,cmd)), flush=True)
    subprocess.run(cmd, check=True)
run([sys.executable, "-m", "pip", "install", "-q", "pycocoevalcap", "sacrebleu"])
from pycocoevalcap.spice import spice
from pycocoevalcap.tokenizer import ptbtokenizer
libs = Path(spice.__file__).resolve().parent / "lib"
libs.mkdir(exist_ok=True)
needed = {"stanford-corenlp-3.6.0.jar": 7270741,
          "stanford-corenlp-3.6.0-models.jar": 378116526}
for name, size in needed.items():
    have = libs / name
    if not have.is_file() or have.stat().st_size != size:
        candidates = [p for p in Path("/kaggle/input").rglob(name) if p.stat().st_size == size]
        assert candidates, f"Missing {name}: attach the private/public corenlp-360-jars dataset"
        shutil.copy2(candidates[0], have)
    assert have.stat().st_size == size, f"Incorrect CoreNLP JAR {name}"
import glob
_v = subprocess.run(["bash","-c","java -version 2>&1"],capture_output=True,text=True).stdout
if 'version "1.8' not in _v:   # SPICE 1.0 cần Java 8
    subprocess.run("apt-get update -qq && apt-get install -y -qq openjdk-8-jre-headless", shell=True, check=True)
    _j = sorted(glob.glob("/usr/lib/jvm/*8*"))
    assert _j, "no Java 8 after apt-get"
    os.environ["JAVA_HOME"] = _j[0]; os.environ["PATH"] = _j[0] + "/bin:" + os.environ["PATH"]
assert shutil.which("java"), "No Java: install OpenJDK before running SPICE"
print("Java", subprocess.run(["java","-version"],capture_output=True,text=True).stderr.splitlines()[:1])
print("Dependencies and CoreNLP jars OK")
'''
experiment = r'''import sys, subprocess, shutil, json
from pathlib import Path
data = [p.parent for p in Path("/kaggle/input").rglob("c1_mau.jsonl")
        if (p.parent/"reward_cpu_8_11.py").is_file()
        and (p.parent/"score_k8_raw.jsonl").is_file()]
assert len(data)==1, f"Expected one C1 CPU dataset, got {data}"
data=data[0]
dst=Path("/kaggle/working")
shutil.copy2(data/"reward_cpu_8_11.py", dst/"reward_cpu_8_11.py")
cmd=[sys.executable, str(dst/"reward_cpu_8_11.py"), "--data", str(data),
     "--out", str(dst/"reward_cpu_8_11"), "--batch-size", "350"]
import time
with (dst/"reward_cpu_8_11.log").open("w") as out:
    p=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT,text=True)
    while p.poll() is None:   # nhịp sống 2 phút
        time.sleep(120); print(time.strftime("%H:%M"), (dst/"reward_cpu_8_11.log").read_text(errors="replace")[-200:].replace("\n"," | "), flush=True)
log=(dst/"reward_cpu_8_11.log").read_text(errors="replace")
print(log[-8000:])
assert p.returncode == 0, f"CPU reward audit failed with code {p.returncode}"
result=json.loads((dst/"reward_cpu_8_11"/"reward_cpu_c1.json").read_text())
assert result["metadata"]["n_prompts"] == 400
assert result["rewards"]["R0_historical"]["tap"]["n"] == 249
assert result["rewards"]["R4_sparse_action"]["non_tap"]["n"] == 151
shutil.make_archive(str(dst/"reward_cpu_8_11_results"), "zip", str(dst/"reward_cpu_8_11"))
print("CPU audit DONE; output JSON and ZIP are in /kaggle/working")
'''
summary = r'''import json
from pathlib import Path
d=json.loads(Path("/kaggle/working/reward_cpu_8_11/reward_cpu_c1.json").read_text())
print("C1 VAL ONLY — does not show post-training improvement")
for name, m in d["rewards"].items():
    x,y=m["tap"],m["non_tap"]
    print(f"{name:25s} tap conc={x['concordance']} tie={x['tie']} std0={x['std0']} "
          f"non-tap proxy conc={y['concordance']} std0={y['std0']}")
print("Gold zero-SPICE fraction by action",d["gold_self"])
print("Gold action verifier coverage",d["trust_coverage"])
print("Stress pairs",len(d["stress"]))
'''
desc = """# C1 CPU reward diagnostics (8 Nov 2026)

**VALIDATION ONLY**: 400 AndroidControl C1 prompts with 8 sampled S1/101
completions each; 249 tap steps carry cached UGround executability,
151 other steps have only a *text action-type proxy*.

Tests reward variants R0 historical, R0 capped-length, fixed SPICE+chrF,
R2 sparse fallback, R3 hard action gate, R4 sparse+action gate. All
proposed variants are hypotheses, not trained models. Zero-tuple fallback
uses SPICE(gold, gold) == 0, which is a proxy for parser sparsity.

Action gate *abstains* when reference text contradicts the trajectory
or the candidate action is unknown. Reports subgroup action coverage and
gold self-score; misleading comparisons are not reported as model wins.

Do not use this validation ranking alone to claim that a reward improves
downstream executability after GRPO training. Select finalists then
evaluate with controlled training seeds and a separate holdout.
"""
nb = {
    "cells": [{"cell_type":"markdown","metadata":{},"source":desc.splitlines(True)}] +
             [{"cell_type":"code","metadata":{},"execution_count":None,"outputs":[],
               "source":code.splitlines(True)} for code in (setup,experiment,summary)],
    "metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
                "language_info":{"name":"python"}},
    "nbformat":4,"nbformat_minor":5,
}
(KERNEL/"reward-spice-c1-cpu-8-11.ipynb").write_text(json.dumps(nb,ensure_ascii=False,indent=2),encoding="utf8")
kernel = {
    "id":"trangphngngc/reward-spice-c1-cpu-8-11",
    "title":"reward-spice-c1-cpu-8-11",
    "code_file":"reward-spice-c1-cpu-8-11.ipynb",
    "language":"python","kernel_type":"notebook",
    "is_private":"true","enable_gpu":"false","enable_internet":"true",
    "dataset_sources":["trangphngngc/grpo-spice-reward-c1-8-11","trangphngngc/corenlp-360-jars"],
    "competition_sources":[],"kernel_sources":[]
}
(KERNEL/"kernel-metadata.json").write_text(json.dumps(kernel,ensure_ascii=False,indent=2),encoding="utf8")
print("PREPARED",BASE)
for p in (DATA/"c1_mau.jsonl",DATA/"reward_cpu_8_11.py",KERNEL/"reward-spice-c1-cpu-8-11.ipynb"):
    print(p.relative_to(ROOT),p.stat().st_size,"bytes")
print("Reminder: Kaggle authentication is required to upload the private dataset and push the CPU notebook.")
