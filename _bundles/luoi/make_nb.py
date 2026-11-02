"""Dựng notebook Kaggle cho lưới GRPO (report/323 §8): HAI lượt train song song, mỗi lượt một GPU T4.

python make_nb.py <tài khoản kaggle> <tên kernel> <che_do: probe|train> <lượt0> <lượt1> [kernel trước]
  biến môi trường: CAT_H = trần giờ của phiên (đặt dưới hạn mức còn lại) · MOI = các lượt mới, cách nhau dấu cách, khi có kernel trước
  tệp ngoài ba tệp gốc nằm ở dataset nhỏ <tài khoản>/luoi-kit (dựng bằng make_kit.py), không phải tải lại jar
  lượt = algo:reward:seed[:k=v,k=v], ví dụ scst:spice:101 · grpo:spice:101:beta=0,loss=dr_grpo,tag=b0 · ppo:spice:101:mu=2,lam=0.95,steps=1000,tag=l95
  k: beta · loss · scale · mu · lam · is · eps · steps · G · tag (phần đuôi thư mục, bắt buộc khi có k đổi cấu hình)
  Lượt không có k và thuật toán của lô 1 thì notebook giữ nguyên như cũ, chỉ cần dataset cũ.
Kết quả ở k_<tên kernel>/ (ipynb + kernel-metadata.json); đẩy bằng
  kg <tk> kernels push -p k_<tên kernel> --accelerator NvidiaTeslaT4
"""
import json, sys, os, hashlib

user, name, mode, r0, r1 = sys.argv[1:6]
prev = sys.argv[6] if len(sys.argv) > 6 else None
assert mode in ("probe", "train")
H = os.path.dirname(os.path.abspath(__file__))
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
CU = ("grpo", "drgrpo", "rloo", "reinforce", "scst")
CD = ("vanilla", "mad", "rft", "cem", "awr", "raml", "rank")
CO = {"beta": "--beta", "loss": "--loss-type", "scale": "--scale-rewards", "mu": "--mu", "lam": "--lam", "is": "--is-level",
      "eps": "--eps-high", "steps": "--max-steps", "G": "--G"}
RUNS = [r0, r1]
FILES = ["grpo_luoi.py", "grpo_spice.py", "build_branch_data.py"]
for r in RUNS:
    al, rw, sd, *x = r.split(":")
    opt = dict(kv.split("=") for kv in x[0].split(",")) if x else {}
    assert set(opt) <= set(CO) | {"tag"} and (not set(opt) - {"tag"} or "tag" in opt), f"cờ sai hoặc thiếu tag: {r}"
    assert al in CU + CD + ("ppo", "a2c", "sft") and int(sd) > 0
    assert rw in ("spice", "cider", "bleu4", "rougel", "chrf", "meteor", "bertscore", "spider")
    assert al == "grpo" or rw == "spice" or (al, rw) == ("scst", "cider"), f"lưới chỉ đổi một yếu tố: {r}"
    assert "lam" not in opt or al in ("ppo", "a2c"), r
    for f in ({"ppo": ["grpo_codien.py", "grpo_ppo.py"], "a2c": ["grpo_codien.py", "grpo_ppo.py"], "sft": ["sft_tiep.py"]}.get(al, [])
              or (["grpo_codien.py"] if al in CD or set(opt) - {"tag"} or rw != "spice" and al != "grpo" else [])):
        if f not in FILES:
            FILES.append(f)
MD5 = {f: md5(os.path.join(H, "ds", f)) for f in FILES}

CAT_H = float(os.environ.get("CAT_H", 11))
MOI = os.environ.get("MOI", "").split()
BASE = ("grpo_luoi.py", "grpo_spice.py", "build_branch_data.py")
C1 = f'''import subprocess, sys, os, time
T_NB = time.time()
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless")
sh("update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java")
sh("java -version")
sh(f"{{sys.executable}} -m pip install -q 'transformers==5.20.2' 'peft==0.21.2' 'trl==0.29.1' accelerate pycocoevalcap sacrebleu{' bert_score' if any(':bertscore:' in r for r in RUNS) else ''} -U torchao 2>&1 | tail -3")
sh(f'{{sys.executable}} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.device_count(), torch.cuda.get_device_name(0))"')
import trl, transformers, peft, torch
assert (trl.__version__, transformers.__version__, peft.__version__) == ("0.29.1", "5.20.2", "0.21.2"), "DUNG: lech phien ban"
assert torch.cuda.device_count() == 2, "DUNG: can 2 GPU T4"
'''
C2 = f'''import os, glob, shutil, hashlib
W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "images" in d)
SRC = [p for p in glob.glob("/kaggle/input/**/grpo_luoi.py", recursive=True) if "/notebooks/" not in p]   # output kernel trước cũng có bản chép
assert len(SRC) == 1, f"DUNG: can dung mot grpo_luoi.py, thay {{SRC}}"
MD5 = {MD5!r}
def nguon(f):
    if f in {BASE!r}:
        return os.path.join(os.path.dirname(SRC[0]), f)
    k = [p for p in glob.glob(f"/kaggle/input/**/{{f}}", recursive=True) if "/notebooks/" not in p]
    assert len(k) == 1, f"DUNG: can dung mot {{f}} trong luoi-kit, thay {{k}}"
    return k[0]
for f, h in MD5.items():
    shutil.copy(nguon(f), f"{{W}}/{{f}}")
    assert md5(f"{{W}}/{{f}}") == h, f"DUNG: {{f}} lech ban may nha"
KEYS = os.path.join(os.path.dirname(SRC[0]), "prompt_keys_ck500.json")
assert md5(KEYS) == "{md5(os.path.join(H, "ds", "prompt_keys_ck500.json"))}"
RUNS = {RUNS!r}
MODE = "{mode}"
MERGED = f"{{W}}/s1_merged"
def opt_of(r):
    x = r.split(":")[3:]
    return dict(kv.split("=") for kv in x[0].split(",")) if x else {{}}
def out_of(r):
    al, rw, sd = r.split(":")[:3]
    tag = opt_of(r).get("tag")
    return f"{{W}}/{{'probe_' if MODE == 'probe' else ''}}{{al}}_{{rw}}_{{sd}}{{'_' + tag if tag else ''}}"
for r in RUNS:
    o = out_of(r); os.makedirs(o, exist_ok=True)
    ck = [p for p in glob.glob(f"/kaggle/input/**/{{os.path.basename(o)}}/checkpoint-*", recursive=True) if os.path.isdir(p)]
    for p in ck:
        shutil.copytree(p, os.path.join(o, os.path.basename(p)), dirs_exist_ok=True)
    print(r, "→", o, "· diem luu da chep:", sorted((os.path.basename(p) for p in ck), key=lambda s: int(s.split("-")[1]))[-3:])
    assert ck or not {bool(prev)!r} or r in {MOI!r}, f"DUNG: co kernel truoc ma khong thay diem luu cua {{o}}"
print("BUNDLE:", BUNDLE, "· md5 khop", flush=True)
'''
C3 = '''import importlib.util, subprocess
SPL = list(importlib.util.find_spec("pycocoevalcap").submodule_search_locations)[0] + "/spice/lib"
JARS = {"stanford-corenlp-3.6.0.jar": 7270741, "stanford-corenlp-3.6.0-models.jar": 378116526}
for j, sz in JARS.items():
    dst = f"{SPL}/{j}"
    if os.path.exists(dst) and os.path.getsize(dst) == sz: continue
    src = glob.glob(f"/kaggle/input/**/{j}", recursive=True); assert src, f"DUNG: thieu {j}"
    shutil.copy(src[0], dst); assert os.path.getsize(dst) == sz, f"DUNG: {j} sai kich thuoc"
print("jar SPICE du", flush=True)
def py(*a):
    r = subprocess.run(["python", *a], cwd=W, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
assert py("grpo_luoi.py", "--selftest-algo") == 0, "DUNG: selftest algo"
rws = sorted({r.split(":")[1] for r in RUNS})
if os.path.exists(f"{W}/grpo_codien.py"):
    assert py("grpo_codien.py", "--selftest-algo") == 0, "DUNG: selftest co dien"
if os.path.exists(f"{W}/grpo_ppo.py"):
    assert py("grpo_ppo.py", "--selftest-algo") == 0, "DUNG: selftest GAE"
assert py("grpo_luoi.py", "--selftest-thuong", "--bundle", BUNDLE, "--rewards", ",".join(rws)) == 0, "DUNG: selftest thuong"
assert py("grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED) == 0, "DUNG: hoa loi"
'''
C4 = '''import subprocess, time, re, ast, statistics as st
TONG = 20 if MODE == "probe" else 500
CAT = 3600 * (1.5 if MODE == "probe" else CAT_GIO)
CD = ("vanilla", "mad", "rft", "cem", "awr", "raml", "rank")
CO = {"beta": "--beta", "loss": "--loss-type", "scale": "--scale-rewards", "mu": "--mu", "lam": "--lam", "is": "--is-level",
      "eps": "--eps-high", "steps": "--max-steps", "G": "--G"}
def tep_cua(r):
    al, rw = r.split(":")[:2]
    ok = opt_of(r)
    if al in ("ppo", "a2c"): return "grpo_ppo.py"
    if al == "sft": return "sft_tiep.py"
    return "grpo_codien.py" if al in CD or set(ok) - {"tag"} or (al != "grpo" and rw != "spice") else "grpo_luoi.py"
def tong_cua(r):
    return 20 if MODE == "probe" else int(opt_of(r).get("steps", TONG))
P = []
for g, r in enumerate(RUNS):
    al, rw, sd = r.split(":")[:3]
    o = out_of(r)
    cmd = ["python", tep_cua(r), "--probe" if MODE == "probe" else "--train", "--no-q4",
           "--bs", "4", "--accum", "4", "--gen-chunk", "8", "--algo", al, "--reward", rw, "--seed", sd,
           "--bundle", BUNDLE, "--merged", MERGED, "--out", o, "--resume", "auto"]
    for k, v in opt_of(r).items():
        if k != "tag":
            cmd += [CO[k], v]
    if sd == "101" and MODE == "train":
        cmd += ["--keys-ck500", KEYS]
    log = open(f"{o}/train.log", "a")
    P.append((r, o, subprocess.Popen(cmd, cwd=W, stdout=log, stderr=subprocess.STDOUT, text=True,
        env={**os.environ, "CUDA_VISIBLE_DEVICES": str(g), "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
             "PYTORCH_ALLOC_CONF": "expandable_segments:True", "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"})))
    time.sleep(90)   # lệch giờ nạp mô hình để RAM không chạm đỉnh cùng lúc
def ck_moi(o):
    c = sorted(glob.glob(f"{o}/checkpoint-*"), key=lambda s: int(s.rsplit("-", 1)[1]))
    return os.path.basename(c[-1]) if c else "chua co"
def tinh_trang(r, o):
    L = open(f"{o}/train.log", encoding="utf-8", errors="ignore").read().splitlines()
    tiep = [l for l in L if l.startswith("[tiếp từ]")]
    goc = int(re.findall(r"checkpoint-(\\d+)", tiep[-1])[0]) if tiep and "checkpoint-" in tiep[-1] else 0
    D = []
    for l in L:
        if l.startswith("{'loss'"):
            try: D.append({k: float(v) for k, v in ast.literal_eval(l).items() if re.match(r"^[-\\d.e+na]+$", str(v))})
            except Exception: pass
    msg = f"  [{r}] buoc {goc + len(D)}/{tong_cua(r)} (tiep tu {goc}) · luu {ck_moi(o)}"
    if D:
        x = D[-10:]
        msg += (f" · {st.mean(d.get('step_time', 0) for d in x):.0f} s/buoc · thuong {st.mean(d.get('reward', 0) for d in x):.3f}"
                f" · kl {st.mean(d.get('kl', 0) for d in x):.4f} · |A| {st.mean(d.get('luoi/adv_abs_mean', float('nan')) for d in x):.3f}")
    for k in ("[xong]", "[nạp default]", "[câu nhắc] trùng"):
        y = [l for l in L if l.startswith(k)]
        if y: msg += "\\n      " + y[-1][:150]
    if any("Traceback" in l or "OutOfMemory" in l or "Killed" in l for l in L[-80:]): msg += "\\n      ⚠️ Traceback/OOM o cuoi log"
    return msg
while any(p.poll() is None for _, _, p in P):
    time.sleep(120)
    m = subprocess.run("free -g | awk '/Mem/{print $3\\"/\\"$2\\" GB RAM\\"}'; nvidia-smi --query-gpu=memory.used --format=csv,noheader | tr '\\\\n' ' '",
                       shell=True, capture_output=True, text=True).stdout.strip()
    print(f"{(time.time()-T_NB)/3600:5.2f} h · {m}", flush=True)
    for r, o, p in P: print(tinh_trang(r, o), flush=True)
    if time.time() - T_NB > CAT:
        print("⛔ het gio, dung de Output kip luu", flush=True)
        for _, _, p in P:
            if p.poll() is None: p.terminate()
        for _, _, p in P: p.wait()
for r, o, p in P:
    print(f"\\n===== {r} · ma thoat {p.returncode} · luu cuoi {ck_moi(o)}")
    print("\\n".join(l for l in open(f"{o}/train.log", encoding="utf-8", errors="ignore").read().splitlines()[-30:]
                    if not l.startswith(("PTB", "Parsing", "Threads", "Loading", "[main]"))))
shutil.rmtree(MERGED, ignore_errors=True)
'''
cells = [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": c.splitlines(True)}
         for c in (C1, C2, C3, C4.replace("CAT_GIO", str(CAT_H)))]
nb = {"cells": cells, "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}},
      "nbformat": 4, "nbformat_minor": 5}
d = os.path.join(H, f"k_{name}")
os.makedirs(d, exist_ok=True)
json.dump(nb, open(os.path.join(d, f"{name}.ipynb"), "w"), ensure_ascii=False, indent=1)
meta = {"id": f"{user}/{name}", "title": name, "code_file": f"{name}.ipynb", "language": "python",
        "kernel_type": "notebook", "is_private": "true", "enable_gpu": "true", "enable_internet": "true",
        "dataset_sources": [f"{user}/fgrb-p1-bundle", f"{user}/grpo-luoi-script"] + ([f"{user}/luoi-kit"] if set(FILES) - set(BASE) else []),
        "competition_sources": [], "kernel_sources": ([prev] if prev else [])}
json.dump(meta, open(os.path.join(d, "kernel-metadata.json"), "w"), indent=1)
print("đã dựng", d, "·", RUNS, "·", mode)
