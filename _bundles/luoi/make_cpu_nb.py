"""Notebook Kaggle CPU kiểm cấu hình lưới RL trước khi tốn giờ GPU (agent A, 6/11/2026).

Với mỗi lượt (cú pháp như make_nb.py), chạy ĐÚNG script và cờ dòng lệnh mà notebook train dùng
(grpo_luoi.py / grpo_codien.py / grpo_ppo.py), nhưng thay mô hình bằng Qwen2.5-VL tí hon
(trl-internal-testing/tiny-Qwen2_5_VLForConditionalGeneration) và ảnh xám nhỏ, train 2 bước trên CPU.
Bắt được: cờ sai, GRPOConfig không nhận khoá, công thức lợi thế/thưởng ném lỗi, thưởng mới (bleu4, chrf,
spider, bertscore) không chạy. KHÔNG bắt được: tràn bộ nhớ T4, tốc độ, hành vi học — phần đó cần probe GPU.

python make_cpu_nb.py <tài khoản> <tên kernel> <lượt> [<lượt> ...]
"""
import json, sys, os, hashlib

user, name, *RUNS = sys.argv[1:]
H = os.path.dirname(os.path.abspath(__file__))
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
FILES = ["grpo_luoi.py", "grpo_spice.py", "build_branch_data.py", "grpo_codien.py", "grpo_ppo.py",
         "grpo_moi_b1.py", "grpo_moi_b2.py", "thuong_moi.py", "metric_exec.py", "descriptors_ten.jsonl",
         "grpo_moi_b4.py", "thuong_t6.py"]   # 7/11: B4 + T6 (tu=base không kiểm ở đây: nó ép nạp Qwen 3B thật)
MD5 = {f: md5(os.path.join(H, "ds", f) if os.path.exists(os.path.join(H, "ds", f)) else os.path.join(H, f"kit_{user}", f)) for f in FILES}
BASE = ("grpo_luoi.py", "grpo_spice.py", "build_branch_data.py")

WRAP = r'''"""python thu.py <file script> <cờ...>: chạy script như __main__ nhưng nạp mô hình tí hon."""
import os, sys, runpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import torch
import grpo_spice as GS
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
TINY = "trl-internal-testing/tiny-Qwen2_5_VLForConditionalGeneration"
class AnyEq(int):
    def __eq__(self, o): return True
    __hash__ = int.__hash__
def nap(a):
    return AutoProcessor.from_pretrained(TINY), Qwen2_5_VLForConditionalGeneration.from_pretrained(TINY, dtype=torch.float32), torch.float32
GS.nap = nap
GS._n_s1 = lambda p: AnyEq(0)
f = sys.argv[1]
sys.argv = sys.argv[1:]
runpy.run_path(f, run_name="__main__")
'''

C1 = f'''import subprocess, sys, os, time, glob, shutil, hashlib, json
T0 = time.time()
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless")
sh("update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java")
sh(f"{{sys.executable}} -m pip install -q 'transformers==5.20.2' 'peft==0.21.2' 'trl==0.29.1' accelerate pycocoevalcap sacrebleu bert_score 2>&1 | tail -3")
sh(f"{{sys.executable}} -m pip uninstall -y -q torchao")
r = subprocess.run([sys.executable, "-c", "import trl, transformers, peft; print(trl.__version__, transformers.__version__, peft.__version__)"], capture_output=True, text=True)
print(r.stdout, r.stderr[-500:], flush=True)
assert r.stdout.split() == ["0.29.1", "5.20.2", "0.21.2"], "DUNG: lech phien ban"
W = "/kaggle/working"; S = f"{{W}}/s"; OUT = f"{{W}}/out"
os.makedirs(S, exist_ok=True); os.makedirs(OUT, exist_ok=True)
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
MD5 = {MD5!r}
for f, h in MD5.items():
    k = [p for p in glob.glob(f"/kaggle/input/**/{{f}}", recursive=True) if "/notebooks/" not in p]
    if len(k) > 1: k = [p for p in k if md5(p) == MD5[f]]
    assert len(k) == 1, f"DUNG: can dung mot {{f}}, thay {{k}}"
    shutil.copyfile(k[0], f"{{S}}/{{f}}"); assert md5(f"{{S}}/{{f}}") == h, f"DUNG: {{f}} lech ban may nha"
open(f"{{S}}/thu.py", "w").write({WRAP!r})
import importlib.util
SPL = list(importlib.util.find_spec("pycocoevalcap").submodule_search_locations)[0] + "/spice/lib"
for j, sz in {{"stanford-corenlp-3.6.0.jar": 7270741, "stanford-corenlp-3.6.0-models.jar": 378116526}}.items():
    src = glob.glob(f"/kaggle/input/**/{{j}}", recursive=True); assert src, f"DUNG: thieu {{j}}"
    shutil.copyfile(src[0], f"{{SPL}}/{{j}}"); assert os.path.getsize(f"{{SPL}}/{{j}}") == sz
# bundle nhỏ: dữ liệu thật (câu nhắc, câu chuẩn, OCR), ảnh xám 112x224, adapter giả r=8
REAL = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "images" in d)
B = "/tmp/bundle_thu"   # ngoài /kaggle/working để Output không kéo 4.000 ảnh
os.makedirs(f"{{B}}/adapter_s1_seed101", exist_ok=True)
for f in ("p1_train_rows.jsonl", "p1_val_rows.jsonl", "ocr.jsonl"):
    shutil.copyfile(f"{{REAL}}/{{f}}", f"{{B}}/{{f}}")
from PIL import Image
for l in open(f"{{B}}/p1_train_rows.jsonl"):
    p = f"{{B}}/" + json.loads(l)["image"]; os.makedirs(os.path.dirname(p), exist_ok=True)
    if not os.path.exists(p): Image.new("RGB", (112, 224), (200, 200, 200)).save(p)
json.dump({{"r": 8, "lora_alpha": 16, "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"]}}, open(f"{{B}}/adapter_s1_seed101/adapter_config.json", "w"))
print("chuan bi xong", round(time.time() - T0), "s", flush=True)
'''

C2 = f'''RUNS = {RUNS!r}
CD = ("vanilla", "mad", "rft", "cem", "awr", "raml", "rank")
B1 = ("dpo_on", "dpo_off", "rft_off", "mrt", "spg", "drgrpo_full", "grpo_seq", "gspo")
B2 = ("seqgan", "mixer", "rlce", "quark", "es")
B3 = ("spice_cong", "ten_loai", "loai")
B4 = ("orpo_on", "orpo_off", "dpo_semi", "gpg")
T6 = ("spice_kp", "phat_dai")
CO = {{"beta": "--beta", "loss": "--loss-type", "scale": "--scale-rewards", "mu": "--mu", "lam": "--lam", "is": "--is-level",
      "eps": "--eps-high", "steps": "--max-steps", "G": "--G",
      "dpob": "--dpo-beta", "mrta": "--mrt-alpha", "spgt": "--spg-tau", "epsl": "--eps-low",
      "celam": "--ce-lam", "rho0": "--mixer-rho0", "mfrac": "--mixer-frac", "ganmix": "--gan-mix", "ganwarm": "--gan-warm",
      "ganlr": "--gan-lr", "qk": "--quark-k", "qpool": "--quark-pool", "espop": "--es-pop", "esm": "--es-m",
      "essig": "--es-sigma", "eslr": "--es-lr", "orpol": "--orpo-lam", "dsync": "--dpo-sync", "gstd": "--gpg-std"}}
def opt_of(r):
    x = r.split(":")[3:]
    return dict(kv.split("=") for kv in x[0].split(",")) if x else {{}}
def tep_cua(r):   # chép đúng luật chọn script của make_nb.py
    al, rw = r.split(":")[:2]; ok = opt_of(r)
    if al in ("ppo", "a2c"): return "grpo_ppo.py"
    assert ok.get("tu") != "base", "tu=base không kiểm được trên CPU"
    if al in B4: return "grpo_moi_b4.py"
    if rw in T6: return "thuong_t6.py"
    if al in B1: return "grpo_moi_b1.py"
    if al in B2 or rw == "bcmr": return "grpo_moi_b2.py"
    if rw in B3: return "thuong_moi.py"
    return "grpo_codien.py" if al in CD or set(ok) - {{"tag"}} or (al != "grpo" and rw != "spice") else "grpo_luoi.py"
for f, a in (("grpo_luoi.py", "--selftest-algo"), ("grpo_codien.py", "--selftest-algo"), ("grpo_ppo.py", "--selftest-algo"),
             ("grpo_moi_b1.py", "--selftest-algo"), ("grpo_moi_b2.py", "--selftest-algo"), ("grpo_moi_b4.py", "--selftest-algo"),
             ("thuong_t6.py", "--selftest-t6")):
    r = subprocess.run([sys.executable, f, a], cwd=S, capture_output=True, text=True)
    print(f, a, "ma", r.returncode, (r.stdout + r.stderr)[-300:], flush=True); assert r.returncode == 0
KQ = {{}}
for r in RUNS:
    al, rw, sd = r.split(":")[:3]; ok = opt_of(r)
    tag = f"{{al}}_{{rw}}_{{sd}}" + ("_" + ok["tag"] if "tag" in ok else "")
    o = f"{{OUT}}/{{tag}}"; shutil.rmtree(o, ignore_errors=True)
    cmd = [sys.executable, "thu.py", tep_cua(r), "--train", "--no-q4", "--bs", "4", "--accum", "4", "--algo", al, "--reward", rw,
           "--seed", sd, "--bundle", B, "--merged", "x", "--out", o]
    for k, v in ok.items():
        if k not in ("tag", "steps"): cmd += [CO[k], v]
    cmd += ["--max-steps", "2"]
    t = time.time()
    with open(f"{{OUT}}/{{tag}}.log", "w") as lg:
        p = subprocess.run(cmd, cwd=S, stdout=lg, stderr=subprocess.STDOUT, text=True,
                           env={{**os.environ, "CUDA_VISIBLE_DEVICES": "", "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1"}})
    L = open(f"{{OUT}}/{{tag}}.log", errors="ignore").read().splitlines()
    hp = f"{{o}}/log_history.json"
    h = json.load(open(hp)) if os.path.exists(hp) else []
    buoc = max([x.get("step", 0) for x in h] or [0])
    dat = p.returncode == 0 and buoc >= 2 and not any("Traceback" in l for l in L)
    KQ[r] = dict(ma=p.returncode, buoc=buoc, giay=round(time.time() - t), dat=dat)
    print(f"{{(time.time()-T0)/60:5.1f}} ph · {{'DAT ' if dat else 'LOI '}} {{r}} · ma {{p.returncode}} · buoc {{buoc}} · {{KQ[r]['giay']}} s", flush=True)
    for l in L:
        if l.startswith(("[đè cấu hình]", "[cấu hình]", "[PPO]", "[bertscore]", "[cider]", "[moi_b4]", "[dpo_semi]", "[moi_b1]")) or "num_iterations" in l: print("     ", l[:220], flush=True)
    if h:
        print("      log cuoi:", {{k: (round(v, 4) if isinstance(v, float) else v) for k, v in h[-1].items()
              if k.startswith(("reward", "luoi", "loss", "kl", "clip", "step", "frac"))}}, flush=True)
    if not dat: print("\\n".join("      | " + l for l in L[-25:]), flush=True)
json.dump(KQ, open(f"{{OUT}}/ket_qua.json", "w"), indent=1, ensure_ascii=False)
shutil.make_archive(f"{{W}}/thu_cpu", "zip", OUT)
print("\\nTONG:", sum(v["dat"] for v in KQ.values()), "/", len(KQ), "dat", flush=True)
assert all(v["dat"] for v in KQ.values()), [k for k, v in KQ.items() if not v["dat"]]
'''
cells = [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": c.splitlines(True)} for c in (C1, C2)]
nb = {"cells": cells, "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}},
      "nbformat": 4, "nbformat_minor": 5}
d = os.path.join(H, f"k_{name}")
os.makedirs(d, exist_ok=True)
json.dump(nb, open(os.path.join(d, f"{name}.ipynb"), "w"), ensure_ascii=False, indent=1)
meta = {"id": f"{user}/{name}", "title": name, "code_file": f"{name}.ipynb", "language": "python",
        "kernel_type": "notebook", "is_private": "true", "enable_gpu": "false", "enable_internet": "true",
        "dataset_sources": [f"{user}/fgrb-p1-bundle", f"{user}/grpo-luoi-script", f"{user}/luoi-kit"],
        "competition_sources": [], "kernel_sources": []}
json.dump(meta, open(os.path.join(d, "kernel-metadata.json"), "w"), indent=1)
print("đã dựng", d, "·", len(RUNS), "lượt")
