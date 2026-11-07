"""Dựng notebook Kaggle CPU kiểm grpo_moi_b1.py: selftest công thức + 3 bước mỗi thuật toán trên mô hình tí hon."""
import json, sys
ALGOS = sys.argv[1] if len(sys.argv) > 1 else ""
C1 = r'''import subprocess, sys, os, time, glob, shutil
def sh(c):
    p = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for l in p.stdout:
        print(l, end="", flush=True)
    return p.wait()
sh(f"{sys.executable} -m pip install -q 'transformers==5.20.2' 'peft==0.21.2' 'trl==0.29.1' accelerate 2>&1 | tail -3")
sh(f"{sys.executable} -m pip uninstall -y -q torchao 2>&1 | tail -1")
sh(f'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__)"')
'''
C2 = r'''SRC = next(r for r, d, f in os.walk("/kaggle/input") if "grpo_moi_b1.py" in f)
W = "/kaggle/working/code"; shutil.copytree(SRC, W, dirs_exist_ok=True)
print("[mã]", SRC, sorted(os.listdir(W)), flush=True)
os.environ.update(HF_HUB_DISABLE_PROGRESS_BARS="1", TRANSFORMERS_VERBOSITY="error", TOKENIZERS_PARALLELISM="false")
rc1 = sh(f"cd {W} && {sys.executable} grpo_moi_b1.py --selftest-algo 2>&1 | tee /kaggle/working/selftest_algo.log")
rc2 = sh(f"cd {W} && {sys.executable} grpo_moi_b1.py --selftest-cpu ALGOS --out /kaggle/working/cpu 2>&1 | tee /kaggle/working/selftest_cpu.log")
print("mã thoát", rc1, rc2, flush=True)
sh("cd /kaggle/working && rm -rf cpu/*/checkpoint-* && zip -qr ket_qua_moi_b1.zip selftest_algo.log selftest_cpu.log cpu/selftest_cpu.json; ls -la")
'''.replace("ALGOS", f"--algos {ALGOS}" if ALGOS else "")
nb = {"cells": [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": c} for c in (C1, C2)],
      "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}},
      "nbformat": 4, "nbformat_minor": 5}
json.dump(nb, open("k_moi-b1-cpu/moi-b1-cpu.ipynb", "w"), ensure_ascii=False, indent=1)
json.dump({"id": "trangphngngc/moi-b1-cpu", "title": "moi-b1-cpu", "code_file": "moi-b1-cpu.ipynb", "language": "python",
           "kernel_type": "notebook", "is_private": "true", "enable_gpu": "false", "enable_internet": "true",
           "dataset_sources": ["trangphngngc/moi-b1-code"], "competition_sources": [], "kernel_sources": []},
          open("k_moi-b1-cpu/kernel-metadata.json", "w"), indent=1)
print("ok")
