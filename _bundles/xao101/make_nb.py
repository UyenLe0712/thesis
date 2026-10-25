import json, sys
n = int(sys.argv[1]); prev = sys.argv[2] if len(sys.argv) > 2 else None
C1 = '''import subprocess, sys, os, time
T_NB = time.time()
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless")
sh("update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java")
sh("java -version")
sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes pycocoevalcap 'trl==0.29.1' 2>&1 | tail -3")
sh(f'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.get_device_name(0))"')
'''
C2 = '''import os, glob, shutil, hashlib
W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "images" in d)
C1 = glob.glob("/kaggle/input/**/c1_mau.jsonl", recursive=True); assert len(C1) == 1, C1; C1 = C1[0]
assert md5(C1) == "d757554326977309c3a65ae0b144c211", "DUNG: c1_mau.jsonl lech ban may nha"
SRC = [p for p in glob.glob("/kaggle/input/**/grpo_spice.py", recursive=True)
       if not os.path.exists(os.path.join(os.path.dirname(p), "train.log"))]
assert len(SRC) == 1, f"DUNG: can dung mot grpo_spice.py cua dataset, thay {SRC}"
for f in ("grpo_spice.py", "build_branch_data.py"):
    shutil.copy(os.path.join(os.path.dirname(SRC[0]), f), f"{W}/{f}")
assert md5(f"{W}/grpo_spice.py") == "8489108147c8d1ed80c3dc67c8ad3d3f", "DUNG: grpo_spice.py la ban cu"
assert md5(f"{W}/build_branch_data.py") == "619e63e123a6dbf60086e65ee94a3912", "DUNG: build_branch_data.py lech"
MERGED = f"{W}/s1_merged"; OUT = f"{W}/grpo_spice"
os.makedirs(OUT, exist_ok=True)
ck = [p for p in glob.glob("/kaggle/input/**/grpo_spice/checkpoint-*", recursive=True) if os.path.isdir(p)]
for p in ck:
    shutil.copytree(p, os.path.join(OUT, os.path.basename(p)), dirs_exist_ok=True)
print("diem luu da chep:", sorted((os.path.basename(p) for p in ck), key=lambda s: int(s.split("-")[1]))[-4:])
print("BUNDLE:", BUNDLE, "\\nC1:", C1, "\\nSRC:", SRC[0], "\\nmd5 khop", flush=True)
'''
C3 = '''import importlib.util
SPL = list(importlib.util.find_spec("pycocoevalcap").submodule_search_locations)[0] + "/spice/lib"
JARS = {"stanford-corenlp-3.6.0.jar": 7270741, "stanford-corenlp-3.6.0-models.jar": 378116526}
for j, sz in JARS.items():
    dst = f"{SPL}/{j}"
    if os.path.exists(dst) and os.path.getsize(dst) == sz: continue
    src = glob.glob(f"/kaggle/input/**/{j}", recursive=True); assert src, f"DUNG: thieu {j} trong dataset"
    shutil.copy(src[0], dst); assert os.path.getsize(dst) == sz, f"DUNG: {j} sai kich thuoc"
print("jar SPICE du", flush=True)
r = subprocess.run(["python", "grpo_spice.py", "--selftest", "--bundle", BUNDLE], cwd=W, capture_output=True, text=True)
print((r.stdout + r.stderr)[-1500:]); assert r.returncode == 0, "DUNG: selftest loi (SPICE khong chay?)"
r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED],
                   cwd=W, capture_output=True, text=True)
print((r.stdout + r.stderr)[-2000:]); assert r.returncode == 0, "DUNG: hoa loi"
'''
C4 = '''import subprocess, time, os, shutil, glob, ast, re, statistics as st
log = open(f"{W}/train.log", "a")
cmd = ["python", "grpo_spice.py", "--train", "--no-q4", "--bs", "4", "--accum", "4", "--gen-chunk", "8",
       "--reward", "shuffle", "--seed", "101",
       "--bundle", BUNDLE, "--merged", MERGED, "--out", OUT, "--resume", "auto"]
p = subprocess.Popen(cmd, cwd=W, stdout=log, stderr=subprocess.STDOUT, text=True,
    env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
         "PYTORCH_ALLOC_CONF": "expandable_segments:True", "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"})
TONG, CAT = 500, 3600 * 11
def ck_moi():
    c = sorted(glob.glob(f"{OUT}/checkpoint-*"), key=lambda s: int(s.rsplit("-", 1)[1]))
    return os.path.basename(c[-1]) if c else "chua co"
def tinh_trang():
    L = open(f"{W}/train.log", encoding="utf-8", errors="ignore").read().splitlines()
    tiep = [l for l in L if l.startswith("[tiếp từ]")]
    goc = int(re.findall(r"checkpoint-(\\d+)", tiep[-1])[0]) if tiep and "checkpoint-" in tiep[-1] else 0
    D = []
    for l in L:
        if l.startswith("{'loss'"):
            try: D.append({k: float(v) for k, v in ast.literal_eval(l).items() if re.match(r"^[-\\d.e+na]+$", str(v))})
            except Exception: pass
    sp = [l for l in L if l.startswith("[spice]")][-20:]
    thuong = [float(re.search(r"thưởng TB (-?[\\d.]+)", l).group(1)) for l in sp]
    tu = [float(re.search(r"số từ TB ([\\d.]+)", l).group(1)) for l in sp]
    buoc = goc + len(D)
    msg = f"{(time.time()-T_NB)/3600:5.2f} h · buoc {buoc}/{TONG} (tiep tu {goc}) · luu cuoi {ck_moi()}"
    for k in ("[cấu hình]", "[nạp default]", "[tiếp từ]", "[sinh theo khúc] bật"):
        x = [l for l in L if l.startswith(k)]
        if x: msg += "\\n      " + x[-1][:110]
    if D and thuong:
        spb = (time.time() - T_TRAIN) / len(D)
        kl = [d["kl"] for d in D[-20:] if "kl" in d]
        msg += (f"\\n      {spb:.0f} s/buoc · con ~{(TONG-buoc)*spb/3600:.1f} h toi 500"
                f"\\n      20 buoc gan nhat: thuong TB {st.mean(thuong):.3f} · so tu TB {st.mean(tu):.1f} · kl TB {st.mean(kl) if kl else float('nan'):.4f}")
    if any("Traceback" in l or "OutOfMemory" in l for l in L[-80:]): msg += "\\n      ⚠️ Traceback/OOM o cuoi log"
    return msg
T_TRAIN = time.time()
while p.poll() is None:
    time.sleep(120)
    print(tinh_trang(), flush=True)
    if time.time() - T_NB > CAT and p.poll() is None:
        print("⛔ da 11 h tu dau notebook, dung de Output kip luu", flush=True)
        p.terminate(); p.wait()
print("ma thoat", p.returncode, "· diem luu cuoi", ck_moi())
print("\\n".join(open(f"{W}/train.log", encoding="utf-8", errors="ignore").read().splitlines()[-40:]))
shutil.rmtree(MERGED, ignore_errors=True)
'''
cells = [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": c.splitlines(True)} for c in (C1, C2, C3, C4)]
nb = {"cells": cells, "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}, "nbformat": 4, "nbformat_minor": 5}
name = f"xao101-{n}"
json.dump(nb, open(f"k/{name}.ipynb", "w"), ensure_ascii=False, indent=1)
meta = {"id": f"uyenle0712/{name}", "title": name, "code_file": f"{name}.ipynb", "language": "python", "kernel_type": "notebook",
        "is_private": "true", "enable_gpu": "true", "enable_internet": "true",
        "dataset_sources": ["uyenle0712/fgrb-p1-bundle", "uyenle0712/c1-exec8", "uyenle0712/grpo-spice-xao"],
        "competition_sources": [], "kernel_sources": ([prev] if prev else [])}
json.dump(meta, open("k/kernel-metadata.json", "w"), indent=1)
