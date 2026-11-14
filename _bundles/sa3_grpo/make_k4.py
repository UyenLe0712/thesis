# -*- coding: utf-8 -*-
"""SA-SPICE-v3 mức 2 (report/333 §11): một kernel Kaggle T4×2 train hai arm song song, mỗi arm một GPU, cùng seed.
Hoà S1 → hoà SFT-cont (kiểm greedy trùng kernel 1) → GRPO `harness/sa3_grpo.py` từ sft_cont_merged, 500 update, chạy tiếp được.
Giữ điểm lưu bước chia hết cho 100 (để chấm DEV 100…500) + 2 điểm lưu mới nhất (để chạy tiếp).

  python3 _bundles/sa3_grpo/make_k4.py <username> <tên kernel> [kernel trước]
  biến môi trường: CAT_H (trần giờ, mặc định 7,5) · ARMS (mặc định "SA-SPICE-v3,chrF") · SEED (mặc định 101) · DS_THEM (dataset thêm, ví dụ điểm lưu)
  kg <tk> datasets create -p _bundles/sa3_grpo/ds --dir-mode zip      (chỉ lần đầu cho mỗi tài khoản)
  kg <tk> kernels push -p _bundles/sa3_grpo/k_<tên kernel> --accelerator NvidiaTeslaT4
"""
import json, os, sys, shutil, hashlib, subprocess

user, name = sys.argv[1:3]
prev = sys.argv[3] if len(sys.argv) > 3 else None
CAT_H = float(os.environ.get("CAT_H", 7.5))
ARMS = os.environ.get("ARMS", "SA-SPICE-v3,chrF").split(",")
SEED = int(os.environ.get("SEED", 101))
DS_THEM = os.environ.get("DS_THEM", "").split()
assert 1 <= len(ARMS) <= 2
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.dirname(os.path.abspath(__file__))
DS, K = os.path.join(H, "ds"), os.path.join(H, f"k_{name}")
os.makedirs(DS, exist_ok=True); os.makedirs(K, exist_ok=True)
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()

SRC1 = f"{R}/_bundles/sa3_mau/ds"
for d in ("images", "adapter_s1_seed101", "sft_final"):
    if not os.path.isdir(f"{DS}/{d}"):
        shutil.copytree(f"{SRC1}/{d}", f"{DS}/{d}")
for f in ("ocr.jsonl",):
    shutil.copy2(f"{SRC1}/{f}", f"{DS}/{f}")
shutil.copy2(f"{R}/runs/sa_spice_v3/split/train_v3.jsonl", f"{DS}/train_v3.jsonl")
shutil.copy2(f"{R}/runs/sa_spice_v3/mau_k1/mau_0.jsonl", f"{DS}/mau_0.jsonl")
PY = ("sa3_grpo.py", "grpo_luoi.py", "grpo_spice.py", "build_branch_data.py", "sa3_reward_screen.py", "sa3_action_verify.py", "h4_spice_tuple_7_11.py")
for f in PY:
    shutil.copy2(f"{R}/harness/{f}", f"{DS}/{f}")
assert len(os.listdir(f"{DS}/images")) == 1000
assert md5(f"{DS}/train_v3.jsonl") == "e033ea809a18c0e5e3eb878305396f19"
assert md5(f"{DS}/sft_final/adapter_model.safetensors") == "113e2a3e6a0781fd5121acda99962d1b"
assert subprocess.run([sys.executable, f"{DS}/sa3_grpo.py", "--selftest"], capture_output=True).returncode == 0, "selftest WSL"
M = {f: md5(f"{DS}/{f}") for f in PY + ("train_v3.jsonl", "mau_0.jsonl", "ocr.jsonl")}
json.dump({"title": "sa3-grpo-v3", "id": f"{user}/sa3-grpo-v3", "licenses": [{"name": "other"}], "isPrivate": True},
          open(f"{DS}/dataset-metadata.json", "w"), indent=1)
TAG = {a: a.replace("+", "p").replace("-", "").lower() for a in ARMS}

c0 = '''import subprocess, sys, os, time, glob, json, shutil, hashlib, re, ast, statistics as st
T_NB = time.time()
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless")
sh("update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java")
sh("java -version")
sh(f"{sys.executable} -m pip install -q 'transformers==5.20.2' 'peft==0.21.2' 'trl==0.29.1' accelerate pycocoevalcap sacrebleu -U torchao 2>&1 | tail -3")
import trl, transformers, peft, torch
print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.device_count(), flush=True)
assert (trl.__version__, transformers.__version__, peft.__version__) == ("0.29.1", "5.20.2", "0.21.2"), "DUNG: lech phien ban"
assert torch.cuda.device_count() == 2, "DUNG: can 2 GPU T4"
'''
c1 = f'''W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
D = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/sa3_grpo.py", recursive=True) if "/notebooks/" not in p and os.path.isdir(os.path.join(os.path.dirname(p), "sft_final"))]
assert len(D) == 1, D; D = D[0]
for f, h in {M!r}.items():
    assert md5(f"{{D}}/{{f}}") == h, f"DUNG: {{f}} lech ban may nha"
for f in {PY!r}:
    shutil.copy(f"{{D}}/{{f}}", f"{{W}}/{{f}}")
import importlib.util
SPL = list(importlib.util.find_spec("pycocoevalcap").submodule_search_locations)[0] + "/spice/lib"
for j, sz in {{"stanford-corenlp-3.6.0.jar": 7270741, "stanford-corenlp-3.6.0-models.jar": 378116526}}.items():
    dst = f"{{SPL}}/{{j}}"
    if os.path.exists(dst) and os.path.getsize(dst) == sz: continue
    src = [p for p in glob.glob(f"/kaggle/input/**/{{j}}", recursive=True) if os.path.getsize(p) == sz]; assert src, f"DUNG: thieu {{j}}"
    shutil.copy(src[0], dst)
def py(*a):
    r = subprocess.run(["python", *a], cwd=W, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-2500:], flush=True); return r.returncode
assert py("sa3_grpo.py", "--selftest") == 0, "DUNG: selftest sa3_grpo"
assert py("grpo_luoi.py", "--selftest-algo") == 0, "DUNG: selftest algo"
ARMS, SEED, TAG = {ARMS!r}, {SEED}, {TAG!r}
OUT = {{a: f"{{W}}/sa3_{{TAG[a]}}_{{SEED}}" for a in ARMS}}
for a, o in OUT.items():
    os.makedirs(o, exist_ok=True)
    ck = [p for p in glob.glob(f"/kaggle/input/**/{{os.path.basename(o)}}/checkpoint-*", recursive=True) if os.path.isdir(p)]
    for p in ck:
        shutil.copytree(p, os.path.join(o, os.path.basename(p)), dirs_exist_ok=True)
    print(a, "→", o, "· diem luu da chep:", sorted(os.path.basename(p) for p in ck), flush=True)
    assert ck or not {bool(prev)!r}, f"DUNG: co kernel truoc ma khong thay diem luu cua {{o}}"
S1M, SFTM = "/tmp/s1_merged", "/tmp/sft_cont_merged"
print(sh("df -h /tmp /kaggle/working | tail -2"))
assert py("grpo_spice.py", "--merge", "--bundle", D, "--adapter", f"{{D}}/adapter_s1_seed101", "--merged", S1M) == 0, "DUNG: hoa S1"
assert py("sa3_grpo.py", "--hoa", "--data", D, "--merged-s1", S1M, "--merged", SFTM) == 0, "DUNG: hoa SFT-cont"
shutil.rmtree(S1M, ignore_errors=True)
assert py("sa3_grpo.py", "--kiem-hoa", "--data", D, "--merged", SFTM) == 0, "DUNG: kiem hoa"
print("✅ moi truong + hoa + kiem hoa", flush=True)
'''
c2 = f'''CAT = 3600 * {CAT_H}
P = []
for g, a in enumerate(ARMS):
    o = OUT[a]
    cmd = ["python", "sa3_grpo.py", "--train", "--arm", a, "--seed", str(SEED), "--data", D, "--merged", SFTM, "--out", o,
           "--no-q4", "--gen-chunk", "8", "--bs", "4", "--accum", "4", "--max-steps", "500", "--resume", "auto"]
    P.append((a, o, subprocess.Popen(cmd, cwd=W, stdout=open(f"{{o}}/train.log", "a"), stderr=subprocess.STDOUT, text=True,
        env={{**os.environ, "CUDA_VISIBLE_DEVICES": str(g), "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
             "PYTORCH_ALLOC_CONF": "expandable_segments:True", "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}})))
    time.sleep(90)
def cks(o):
    return sorted(glob.glob(f"{{o}}/checkpoint-*"), key=lambda s: int(s.rsplit("-", 1)[1]))
def tinh_trang(a, o):
    L = open(f"{{o}}/train.log", encoding="utf-8", errors="ignore").read().splitlines()
    tiep = [l for l in L if l.startswith("[tiếp từ]")]
    goc = int(re.findall(r"checkpoint-(\\d+)", tiep[-1])[0]) if tiep and "checkpoint-" in tiep[-1] else 0
    Dl = []
    for l in L:
        if l.startswith("{{'loss'"):
            try: Dl.append({{k: float(v) for k, v in ast.literal_eval(l).items() if re.match(r"^[-\\d.e+na]+$", str(v))}})
            except Exception: pass
    c = cks(o)
    msg = f"  [{{a}}] buoc {{goc + len([d for d in Dl if 'reward' in d])}}/500 (tiep tu {{goc}}) · luu {{os.path.basename(c[-1]) if c else 'chua co'}}"
    x = [d for d in Dl if "reward" in d][-10:]
    if x:
        msg += f" · {{st.mean(d.get('step_time', 0) for d in Dl[-20:]):.0f}} s/lan · thuong {{st.mean(d['reward'] for d in x):.3f}} · kl {{st.mean(d.get('kl', 0) for d in x):.4f}}"
    for k in ("[xong]", "[nạp default]", "[LoRA mới]", "[câu nhắc]"):
        y = [l for l in L if l.startswith(k)]
        if y: msg += "\\n      " + y[-1][:150]
    if any("Traceback" in l or "OutOfMemory" in l or "Killed" in l or "STOP" in l for l in L[-80:]): msg += "\\n      ⚠️ Traceback/OOM/STOP o cuoi log"
    return msg
while any(p.poll() is None for _, _, p in P):
    time.sleep(120)
    for _, o, _ in P:
        c = cks(o)
        for x in c[:-2]:
            if int(x.rsplit("-", 1)[1]) % 100:
                shutil.rmtree(x, ignore_errors=True); print("  [xoa diem luu]", os.path.basename(x), flush=True)
    m = subprocess.run("free -g | awk '/Mem/{{print $3\\"/\\"$2\\" GB RAM\\"}}'; nvidia-smi --query-gpu=memory.used --format=csv,noheader | tr '\\\\n' ' '",
                       shell=True, capture_output=True, text=True).stdout.strip()
    print(f"{{(time.time()-T_NB)/3600:5.2f}} h · {{m}}", flush=True)
    for a, o, p in P: print(tinh_trang(a, o), flush=True)
    if time.time() - T_NB > CAT:
        print("⛔ het gio, dung de Output kip luu", flush=True)
        for _, _, p in P:
            if p.poll() is None: p.terminate()
        for _, _, p in P: p.wait()
for a, o, p in P:
    c = cks(o)
    print(f"\\n===== {{a}} · ma thoat {{p.returncode}} · diem luu {{[os.path.basename(x) for x in c]}}")
    print("\\n".join(l for l in open(f"{{o}}/train.log", encoding="utf-8", errors="ignore").read().splitlines()[-25:]
                    if not l.startswith(("PTB", "Parsing", "Threads", "Loading", "[main]"))))
shutil.rmtree(SFTM, ignore_errors=True)
'''
cells = (c0, c1, c2)
for i, c in enumerate(cells):
    compile(c, f"o{i}", "exec")
nb = {"nbformat": 4, "nbformat_minor": 5,
      "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}, "language_info": {"name": "python"}},
      "cells": [{"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "id": f"o{i}", "source": c.splitlines(keepends=True)}
                for i, c in enumerate(cells)]}
json.dump(nb, open(f"{K}/{name}.ipynb", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"id": f"{user}/{name}", "title": name, "code_file": f"{name}.ipynb", "language": "python", "kernel_type": "notebook",
           "is_private": "true", "enable_gpu": "true", "enable_internet": "true",
           "dataset_sources": [f"{user}/sa3-grpo-v3", f"{user}/grpo-luoi-script"] + DS_THEM + ([prev] if False else []),
           "competition_sources": [], "kernel_sources": []},
          open(f"{K}/kernel-metadata.json", "w"), indent=1)
print("ok", name, ARMS, "seed", SEED, "trần", CAT_H, "h ·", len(M), "tệp md5")
