# -*- coding: utf-8 -*-
"""Đóng gói lượt chấm exec 8 mẫu C1 (harness/tai_lieu_2026-09-28/251_…md) cho Kaggle, 0 GPU.

Ra hai tệp:
  _bundles/c1_exec8.zip   → upload thành Kaggle Dataset `c1-exec8`
  _bundles/c1_exec8.ipynb → File → Import Notebook trên Kaggle, rồi Save & Run All (Commit)
Năm ô của notebook chép NGUYÊN VĂN từ năm khối ```python ở §4 của file 251 — một nguồn, không lệch.
Chạy:  python3 harness/make_c1_exec8.py
"""
import hashlib, json, os, re, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MD = os.path.join(HERE, "tai_lieu_2026-09-28", "251_ACTION_GPU_EXEC_8_MAU_C1_28_9.md")
OUTD = os.path.join(ROOT, "_bundles")

mau = os.path.join(ROOT, "runs/c1/c1_mau.jsonl")
picks = os.path.join(ROOT, "runs/c1/c1_picks.json")
assert os.path.exists(picks), "thiếu runs/c1/c1_picks.json — chạy harness/c1_oracle_spice.py trước"
P = json.load(open(picks, encoding="utf-8"))
assert len(P["picks"]) == 400 and P["doi_cau_click"] == 119, P

os.makedirs(OUTD, exist_ok=True)
zp = os.path.join(OUTD, "c1_exec8.zip")
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(mau, "c1_mau.jsonl")
    z.write(picks, "c1_picks.json")
    for f in ("score_run.py", "metric_exec.py", "a11y_inventory.py"):
        z.write(os.path.join(HERE, f), f"thesis/harness/{f}")
    print(zp, os.path.getsize(zp) // 1024, "KB:", z.namelist())

t = open(MD, encoding="utf-8").read()
sec4 = t.split("## 4.", 1)[1].split("\n## 5.", 1)[0]
o = re.findall(r"### (Ô \d[^\n]*)\n.*?```python\n(.*?)```", sec4, flags=re.S)
assert [x[0][:3] for x in o] == ["Ô 1", "Ô 2", "Ô 3", "Ô 4", "Ô 5"], [x[0] for x in o]
for ten, code in o:
    compile(code, ten, "exec")            # lỗi cú pháp thì hỏng ở đây, không phải trên Kaggle
nb = {"nbformat": 4, "nbformat_minor": 5,
      "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                   "language_info": {"name": "python"}},
      "cells": [{"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
                 "id": f"o{i+1}", "source": f"# {ten}\n{code}".splitlines(keepends=True)}
                for i, (ten, code) in enumerate(o)]}
ip = os.path.join(OUTD, "c1_exec8.ipynb")
json.dump(nb, open(ip, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(ip, "·", len(nb["cells"]), "ô")
print("md5 c1_mau.jsonl =", hashlib.md5(open(mau, "rb").read()).hexdigest())
