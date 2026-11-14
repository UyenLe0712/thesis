# -*- coding: utf-8 -*-
"""SA-SPICE-v3 — chấm DEV-v3 (report/333 §11): kernel Kaggle T4×2, mỗi GPU một mô hình: greedy 2.223 bước DEV-v3
(sa3_dev.py) rồi UGround chấm exec 1.338 bước chạm (score_run.py, recs_tap.jsonl). Bước không chạm đọc ở máy nhà từ tệp câu.

  python3 _bundles/sa3_dev/make_k.py <username> <tên kernel> <mô hình GPU0> <mô hình GPU1>
     mô hình ∈ sftcont · sa_ck400 · sa_ck500 · chrf_ck400 · …   (adapter lấy từ _bundles/sa3_grpo/ck_u3)
  kg <tk> datasets create -p _bundles/sa3_dev/ds --dir-mode zip
  kg <tk> kernels push -p _bundles/sa3_dev/k_<tên kernel> --accelerator NvidiaTeslaT4
"""
import json, os, sys, shutil, hashlib

user, name, *MODELS = sys.argv[1:]
assert len(MODELS) == 2, MODELS
CAT_H = float(os.environ.get("CAT_H", 10.5))
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.dirname(os.path.abspath(__file__))
DS, K = os.path.join(H, "ds"), os.path.join(H, f"k_{name}")
os.makedirs(DS + "/images", exist_ok=True); os.makedirs(DS + "/thesis/harness", exist_ok=True); os.makedirs(K, exist_ok=True)
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
TAPT = ("click", "long_press")
CK = {"sa": "sa3_saspicev3_101", "chrf": "sa3_chrf_101"}

# ---- dữ liệu DEV-v3 ----
TA = f"{R}/harness/dg1_cache/train_ac"
dev = [json.loads(l) for l in open(f"{R}/runs/sa_spice_v3/split/dev_v3.jsonl", encoding="utf-8")]
assert len(dev) == 2223
shutil.copy2(f"{R}/runs/sa_spice_v3/split/dev_v3.jsonl", f"{DS}/dev_v3.jsonl")
imgs = {r["image"] for r in dev}
with open(f"{DS}/ocr_dev.jsonl", "w", encoding="utf-8") as f:
    for l in open(f"{TA}/ocr.jsonl", encoding="utf-8"):
        if json.loads(l)["image"] in imgs:
            f.write(l)
for i in imgs:
    if not os.path.exists(f"{DS}/{i}"):
        shutil.copy2(f"{TA}/{i}", f"{DS}/{i}")
taps = [r for r in dev if r["action"]["action_type"] in TAPT and "x" in r["action"]]
with open(f"{DS}/recs_tap.jsonl", "w", encoding="utf-8") as f:
    for r in taps:
        f.write(json.dumps({**r, "gold_instruction": r["target_instruction"]}, ensure_ascii=False) + "\n")
NT = len(taps)
# ---- dựng sft_cont_merged + kiểm hoà (như make_k4) ----
SRC = f"{R}/_bundles/sa3_grpo/ds"
for d in ("adapter_s1_seed101", "sft_final"):
    if not os.path.isdir(f"{DS}/{d}"):
        shutil.copytree(f"{SRC}/{d}", f"{DS}/{d}")
shutil.copy2(f"{SRC}/mau_0.jsonl", f"{DS}/mau_0.jsonl"); shutil.copy2(f"{SRC}/train_v3.jsonl", f"{DS}/train_v3.jsonl")
m0 = [json.loads(l) for l in open(f"{DS}/mau_0.jsonl", encoding="utf-8")][:3]
tv = {(r["episode_id"], r["step_id"]): r for r in map(json.loads, open(f"{DS}/train_v3.jsonl", encoding="utf-8"))}
need = {tv[(d["episode_id"], d["step_id"])]["image"] for d in m0}
for i in need:
    shutil.copy2(f"{SRC}/{i}", f"{DS}/{i}")
with open(f"{DS}/ocr.jsonl", "w", encoding="utf-8") as f:            # cho kiem_hoa (3 câu nhắc train)
    for l in open(f"{SRC}/ocr.jsonl", encoding="utf-8"):
        if json.loads(l)["image"] in need:
            f.write(l)
# ---- adapter GRPO ----
for mo in ("sa_ck400", "sa_ck500", "chrf_ck400", "chrf_ck500", "sa_ck100", "sa_ck200", "sa_ck300", "chrf_ck100", "chrf_ck200", "chrf_ck300"):
    if mo in MODELS:
        arm, ck = mo.split("_ck")
        s, d = f"{R}/_bundles/sa3_grpo/ck_u3/{CK[arm]}/checkpoint-{ck}", f"{DS}/ad/{mo}"
        os.makedirs(d, exist_ok=True)
        for f in ("adapter_config.json", "adapter_model.safetensors"):
            shutil.copy2(f"{s}/{f}", f"{d}/{f}")
PY = ("sa3_dev.py", "sa3_grpo.py", "grpo_luoi.py", "grpo_spice.py", "build_branch_data.py", "sa3_reward_screen.py",
      "sa3_action_verify.py", "h4_spice_tuple_7_11.py")
for f in PY:
    shutil.copy2(f"{R}/harness/{f}", f"{DS}/{f}")
for f in ("score_run.py", "metric_exec.py", "a11y_inventory.py"):
    shutil.copy2(f"{R}/harness/{f}", f"{DS}/thesis/harness/{f}")
assert md5(f"{DS}/sft_final/adapter_model.safetensors") == "113e2a3e6a0781fd5121acda99962d1b"
assert len([i for i in os.listdir(f"{DS}/images")]) >= 2223
M = {f: md5(f"{DS}/{f}") for f in PY + ("dev_v3.jsonl", "recs_tap.jsonl", "ocr_dev.jsonl")}
M.update({f"ad/{mo}/adapter_model.safetensors": md5(f"{DS}/ad/{mo}/adapter_model.safetensors") for mo in MODELS if mo != "sftcont"})
json.dump({"title": "sa3-dev-v3", "id": f"{user}/sa3-dev-v3", "licenses": [{"name": "other"}], "isPrivate": True},
          open(f"{DS}/dataset-metadata.json", "w"), indent=1)

c0 = '''import subprocess, sys, os, time, glob, json, shutil, hashlib, threading, zipfile
T_NB = time.time()
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh(f"{sys.executable} -m pip install -q 'transformers==5.20.2' 'peft==0.21.2' 'trl==0.29.1' accelerate bitsandbytes pycocoevalcap sacrebleu 2>&1 | tail -3")
sh(f"{sys.executable} -m pip uninstall -y torchao 2>&1 | tail -1")
import transformers, peft, torch
print(transformers.__version__, peft.__version__, torch.__version__, torch.cuda.device_count(), flush=True)
assert (transformers.__version__, peft.__version__) == ("5.20.2", "0.21.2"), "DUNG: lech phien ban"
assert torch.cuda.device_count() == 2, "DUNG: can 2 GPU T4"
'''
c1 = f'''W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
D = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/sa3_dev.py", recursive=True) if "/notebooks/" not in p]
assert len(D) == 1, D; D = D[0]
for f, h in {M!r}.items():
    assert md5(f"{{D}}/{{f}}") == h, f"DUNG: {{f}} lech ban may nha"
for f in {PY!r}:
    shutil.copy(f"{{D}}/{{f}}", f"{{W}}/{{f}}")
WS = f"{{W}}/pk/thesis"; shutil.copytree(f"{{D}}/thesis", WS, dirs_exist_ok=True)
VD = f"{{W}}/data"; os.makedirs(VD, exist_ok=True)
shutil.copy(f"{{D}}/recs_tap.jsonl", f"{{VD}}/recs_tap.jsonl")
if not os.path.lexists(f"{{VD}}/images"): os.symlink(f"{{D}}/images", f"{{VD}}/images")
ENV = {{**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1",
        "PYTORCH_ALLOC_CONF": "expandable_segments:True", "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}}
def py(*a, gpu=0):
    r = subprocess.run(["python", *a], cwd=W, capture_output=True, text=True, env={{**ENV, "CUDA_VISIBLE_DEVICES": str(gpu)}})
    print((r.stdout + r.stderr)[-2500:], flush=True); return r.returncode
S1M, SFTM = "/tmp/s1_merged", "/tmp/sft_cont_merged"
assert py("grpo_spice.py", "--merge", "--bundle", D, "--adapter", f"{{D}}/adapter_s1_seed101", "--merged", S1M) == 0, "DUNG: hoa S1"
assert py("sa3_grpo.py", "--hoa", "--data", D, "--merged-s1", S1M, "--merged", SFTM) == 0, "DUNG: hoa SFT-cont"
shutil.rmtree(S1M, ignore_errors=True)
assert py("sa3_grpo.py", "--kiem-hoa", "--data", D, "--merged", SFTM) == 0, "DUNG: kiem hoa"
from huggingface_hub import snapshot_download
print("UGround:", snapshot_download("osunlp/UGround-V1-2B"), flush=True)
sys.path.insert(0, f"{{WS}}/harness")
import a11y_inventory as A11Y, score_run as SR
recs = [json.loads(l) for l in open(f"{{VD}}/recs_tap.jsonl")]
names = set(A11Y._zip().namelist())
co = sum(A11Y.key_for(f"episode_{{d['episode_id']}}_screenshot_{{d['step_id']}}.png") in names for d in recs)
rong = sum(len(SR.buttons_of(d)) == 0 for d in recs)
print(f"buoc cham {{len(recs)}} · cay tro nang {{co}}/{NT} · rong nut {{rong}}", flush=True)
assert len(recs) == {NT} and co == {NT} and rong <= 5, "DUNG: thieu cay tro nang"
print("✅ moi truong + hoa + kiem hoa + UGround", flush=True)
'''
c2 = f'''MODELS = {MODELS!r}
def gen_cmd(mo, out, n=0):
    c = ["python", "-u", "sa3_dev.py", "--data", D, "--merged", SFTM, "--out", out]
    if mo != "sftcont": c += ["--adapter", f"{{D}}/ad/{{mo}}"]
    return c + (["--n", str(n)] if n else [])
score = lambda mo, out: ["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", f"{{W}}/dev_{{mo}}.jsonl",
                         "--data-root", VD, "--recs-file", "recs_tap.jsonl", "--out", out]
# thử 3 bước mỗi mô hình (sinh) + 3 bước chấm
for g, mo in enumerate(MODELS):
    assert py(*gen_cmd(mo, f"{{W}}/thu_{{mo}}.jsonl", 3)[1:], gpu=g) == 0, f"DUNG: thu sinh {{mo}}"
    T = [json.loads(l) for l in open(f"{{W}}/thu_{{mo}}.jsonl")]
    assert len(T) == 3 and all(t["pred"] for t in T), f"DUNG: thu {{mo}} sai"
    print("✅ thu", mo, [(t["gold"], t["pred"]) for t in T], flush=True)
CAT = 3600 * {CAT_H}
RC = {{}}
def chay(g, mo):
    lg = open(f"{{W}}/{{mo}}.log", "a")
    for buoc, cmd, cwd in (("sinh", gen_cmd(mo, f"{{W}}/dev_{{mo}}.jsonl"), W), ("cham", score(mo, f"{{W}}/score/score_dev_{{mo}}.json"), WS)):
        os.makedirs(f"{{W}}/score", exist_ok=True)
        q = subprocess.Popen(cmd, cwd=cwd, stdout=lg, stderr=subprocess.STDOUT, env={{**ENV, "CUDA_VISIBLE_DEVICES": str(g)}}, start_new_session=True)
        while q.poll() is None:
            time.sleep(60)
            if time.time() - T_NB > CAT:
                q.terminate(); q.wait(); RC[mo] = f"het gio o {{buoc}}"; return
        if q.returncode != 0:
            RC[mo] = f"loi {{buoc}} {{q.returncode}}"; return
        if buoc == "sinh":
            n = sum(1 for _ in open(f"{{W}}/dev_{{mo}}.jsonl")); assert n == 2223, n
    RC[mo] = 0
TH = [threading.Thread(target=chay, args=(g, mo)) for g, mo in enumerate(MODELS)]
[t.start() for t in TH]
while any(t.is_alive() for t in TH):
    time.sleep(120)
    for mo in MODELS:
        L = [l.strip() for l in open(f"{{W}}/{{mo}}.log", errors="ignore") if l.strip()] if os.path.exists(f"{{W}}/{{mo}}.log") else []
        print(f"{{(time.time()-T_NB)/3600:5.2f}} h · {{mo}} · {{L[-1][:140] if L else 'chua co dong'}}", flush=True)
print("ket qua", RC, flush=True)
for mo in MODELS:
    if RC.get(mo) != 0: print(open(f"{{W}}/{{mo}}.log", errors="ignore").read()[-2500:], flush=True)
    p = f"{{W}}/score/score_dev_{{mo}}.json"
    if os.path.exists(p): print(mo, {{k: v for k, v in json.load(open(p)).items() if not isinstance(v, (list, dict))}}, flush=True)
'''
c3 = '''with zipfile.ZipFile(f"{W}/sa3_dev_out.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for p in glob.glob(f"{W}/*.jsonl") + glob.glob(f"{W}/*.log") + glob.glob(f"{W}/score/*"):
        z.write(p, os.path.relpath(p, W))
print("zip", os.path.getsize(f"{W}/sa3_dev_out.zip") // 1024, "KB", flush=True)
shutil.rmtree(SFTM, ignore_errors=True)
'''
cells = (c0, c1, c2, c3)
for i, c in enumerate(cells):
    compile(c, f"o{i}", "exec")
nb = {"nbformat": 4, "nbformat_minor": 5,
      "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}, "language_info": {"name": "python"}},
      "cells": [{"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "id": f"o{i}", "source": c.splitlines(keepends=True)}
                for i, c in enumerate(cells)]}
json.dump(nb, open(f"{K}/{name}.ipynb", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"id": f"{user}/{name}", "title": name, "code_file": f"{name}.ipynb", "language": "python", "kernel_type": "notebook",
           "is_private": "true", "enable_gpu": "true", "enable_internet": "true",
           "dataset_sources": [f"{user}/sa3-dev-v3"], "competition_sources": [], "kernel_sources": []},
          open(f"{K}/kernel-metadata.json", "w"), indent=1)
print("ok", name, MODELS, "· bước chạm", NT, "· trần", CAT_H, "h")
