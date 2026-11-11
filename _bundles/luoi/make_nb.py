"""Dựng notebook Kaggle cho lưới GRPO (report/323 §8): HAI lượt train song song, mỗi lượt một GPU T4.

python make_nb.py <tài khoản kaggle> <tên kernel> <che_do: probe|train> <lượt0> <lượt1 hoặc -> [kernel trước]
  biến môi trường: PROBE_H = trần giờ chế độ probe (mặc định 1,5) · CAT_H = trần giờ của phiên (đặt dưới hạn mức còn lại) · MOI = các lượt mới, cách nhau dấu cách, khi có kernel trước
  tệp ngoài ba tệp gốc nằm ở dataset nhỏ <tài khoản>/luoi-kit (dựng bằng make_kit.py), không phải tải lại jar
  lượt = algo:reward:seed[:k=v,k=v], ví dụ scst:spice:101 · grpo:spice:101:beta=0,loss=dr_grpo,tag=b0 · ppo:spice:101:mu=2,lam=0.95,steps=1000,tag=l95
  k: beta · loss · scale · mu · lam · is · eps · steps · G · B1: dpob mrta spgt epsl · B2: celam rho0 mfrac ganmix ganwarm ganlr qk qpool espop esm essig eslr · B4: orpol dsync gstd · tu=base (xuất phát từ Qwen gốc, chỉ thuật toán grpo_luoi) · tag (phần đuôi thư mục, bắt buộc khi có k đổi cấu hình)
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
B1 = ("dpo_on", "dpo_off", "rft_off", "mrt", "spg", "drgrpo_full", "grpo_seq", "gspo")   # grpo_moi_b1.py
B2 = ("seqgan", "mixer", "rlce", "quark", "es")                                             # grpo_moi_b2.py (+ thưởng bcmr)
B3 = ("spice_cong", "ten_loai", "loai")                                                     # thuong_moi.py
B4 = ("orpo_on", "orpo_off", "dpo_semi", "gpg")                                          # grpo_moi_b4.py
T6 = ("spice_kp", "phat_dai")                                                             # thuong_t6.py
CO = {"beta": "--beta", "loss": "--loss-type", "scale": "--scale-rewards", "mu": "--mu", "lam": "--lam", "is": "--is-level",
      "eps": "--eps-high", "steps": "--max-steps", "G": "--G",
      "dpob": "--dpo-beta", "mrta": "--mrt-alpha", "spgt": "--spg-tau", "epsl": "--eps-low",
      "celam": "--ce-lam", "rho0": "--mixer-rho0", "mfrac": "--mixer-frac", "ganmix": "--gan-mix", "ganwarm": "--gan-warm",
      "ganlr": "--gan-lr", "qk": "--quark-k", "qpool": "--quark-pool", "espop": "--es-pop", "esm": "--es-m",
      "essig": "--es-sigma", "eslr": "--es-lr",
      "orpol": "--orpo-lam", "dsync": "--dpo-sync", "gstd": "--gpg-std"}
RUNS = [r0] if r1 == "-" else [r0, r1]   # "-": chỉ một lượt, GPU thứ hai để trống
FILES = ["grpo_luoi.py", "grpo_spice.py", "build_branch_data.py"]
for r in RUNS:
    al, rw, sd, *x = r.split(":")
    opt = dict(kv.split("=") for kv in x[0].split(",")) if x else {}
    assert set(opt) <= set(CO) | {"tag", "tu"} and (not set(opt) - {"tag"} or "tag" in opt), f"cờ sai hoặc thiếu tag: {r}"
    assert al in CU + CD + B1 + B2 + B4 + ("ppo", "a2c", "sft") and int(sd) > 0
    assert rw in ("spice", "cider", "bleu4", "rougel", "chrf", "meteor", "bertscore", "spider", "bcmr") + B3 + T6
    assert rw not in T6 or (al == "grpo" and not set(opt) - {"tag"}), f"thưởng T6 chỉ đi với grpo mặc định: {r}"
    assert opt.get("tu", "base") == "base" and ("tu" not in opt or (al in CU and set(opt) <= {"tag", "tu"})), \
        f"tu=base chỉ đi với thuật toán của grpo_luoi, không cờ khác: {r}"
    assert rw not in B3 or (al == "grpo" and not set(opt) - {"tag"}), f"thưởng B3 chỉ đi với grpo mặc định: {r}"
    assert rw != "bcmr" or al == "grpo", f"bcmr chỉ đi với grpo: {r}"
    assert al == "grpo" or rw == "spice" or (al, rw) == ("scst", "cider"), f"lưới chỉ đổi một yếu tố: {r}"
    assert "lam" not in opt or al in ("ppo", "a2c"), r
    for f in ({"ppo": ["grpo_codien.py", "grpo_ppo.py"], "a2c": ["grpo_codien.py", "grpo_ppo.py"], "sft": ["sft_tiep.py"]}.get(al, [])
              or (["grpo_tu_base.py"] if opt.get("tu") == "base" else [])
              or (["grpo_codien.py", "grpo_moi_b1.py", "grpo_moi_b4.py"] if al in B4 else [])
              or (["thuong_t6.py"] if rw in T6 else [])
              or (["grpo_codien.py", "grpo_moi_b1.py"] if al in B1 else [])
              or (["grpo_codien.py", "grpo_moi_b2.py"] if al in B2 or rw == "bcmr" else [])
              or (["thuong_moi.py", "metric_exec.py", "descriptors_ten.jsonl"] if rw in B3 else [])
              or (["grpo_codien.py"] if al in CD or set(opt) - {"tag", "tu"} or rw != "spice" and al != "grpo" else [])):
        if f not in FILES:
            FILES.append(f)
MD5 = {f: md5(os.path.join(H, "ds", f) if os.path.exists(os.path.join(H, "ds", f)) else os.path.join(H, f"kit_{user}", f)) for f in FILES}   # tệp mới chỉ có ở kit

CAT_H = float(os.environ.get("CAT_H", 11))
PROBE_H = float(os.environ.get("PROBE_H", 1.5))   # trần giờ ở chế độ probe; mặc định giữ như cũ
MOI = os.environ.get("MOI", "").split()
CAN_CK = os.environ.get("CAN_CK") == "1"          # 11/11: chạy tiếp từ dataset điểm lưu, không thấy điểm lưu thì dừng
GIU_CK = int(os.environ.get("GIU_CK", 0))          # 11/11: >0 thì chỉ giữ GIU_CK điểm lưu mới nhất mỗi lượt (luoi-t-11 hết đĩa)
DS_THEM = os.environ.get("DS_THEM", "").split()    # dataset thêm, ví dụ dataset điểm lưu chép từ tài khoản khác
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
    if len(k) > 1: k = [p for p in k if md5(p) == MD5[f]]   # tệp trùng tên ở dataset khác: chọn bản đúng md5
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
    assert ck or not ({bool(prev)!r} or {CAN_CK!r}) or r in {MOI!r}, f"DUNG: co kernel truoc ma khong thay diem luu cua {{o}}"
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
if os.path.exists(f"{W}/grpo_moi_b1.py"):
    assert py("grpo_moi_b1.py", "--selftest-algo") == 0, "DUNG: selftest B1"
if os.path.exists(f"{W}/grpo_moi_b2.py"):
    assert py("grpo_moi_b2.py", "--selftest-algo") == 0, "DUNG: selftest B2"
    if "bcmr" in rws:
        assert py("grpo_moi_b2.py", "--selftest-thuong", "--bundle", BUNDLE, "--rewards", "bcmr") == 0, "DUNG: selftest bcmr"
if os.path.exists(f"{W}/thuong_moi.py"):
    assert py("thuong_moi.py", "--selftest-moi", "--bundle", BUNDLE) == 0, "DUNG: selftest thuong B3"
if os.path.exists(f"{W}/grpo_moi_b4.py"):
    assert py("grpo_moi_b4.py", "--selftest-algo") == 0, "DUNG: selftest B4"
if os.path.exists(f"{W}/thuong_t6.py"):
    assert py("thuong_t6.py", "--selftest-t6", "--bundle", BUNDLE) == 0, "DUNG: selftest thuong T6"
if os.path.exists(f"{W}/grpo_tu_base.py"):
    assert py("grpo_tu_base.py", "--selftest-base") == 0, "DUNG: selftest xuat phat Base"
rws0 = [x for x in rws if x not in ("bcmr", "spice_cong", "ten_loai", "loai", "spice_kp", "phat_dai")] or ["spice"]
assert py("grpo_luoi.py", "--selftest-thuong", "--bundle", BUNDLE, "--rewards", ",".join(rws0)) == 0, "DUNG: selftest thuong"
assert py("grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED) == 0, "DUNG: hoa loi"
'''
C4 = '''import subprocess, time, re, ast, statistics as st
TONG = 20 if MODE == "probe" else 500
CAT = 3600 * (PROBE_GIO if MODE == "probe" else CAT_GIO)
CD = ("vanilla", "mad", "rft", "cem", "awr", "raml", "rank")
B1 = ("dpo_on", "dpo_off", "rft_off", "mrt", "spg", "drgrpo_full", "grpo_seq", "gspo")   # grpo_moi_b1.py
B2 = ("seqgan", "mixer", "rlce", "quark", "es")                                             # grpo_moi_b2.py (+ thưởng bcmr)
B3 = ("spice_cong", "ten_loai", "loai")                                                     # thuong_moi.py
B4 = ("orpo_on", "orpo_off", "dpo_semi", "gpg")                                          # grpo_moi_b4.py
T6 = ("spice_kp", "phat_dai")                                                             # thuong_t6.py
CO = {"beta": "--beta", "loss": "--loss-type", "scale": "--scale-rewards", "mu": "--mu", "lam": "--lam", "is": "--is-level",
      "eps": "--eps-high", "steps": "--max-steps", "G": "--G",
      "dpob": "--dpo-beta", "mrta": "--mrt-alpha", "spgt": "--spg-tau", "epsl": "--eps-low",
      "celam": "--ce-lam", "rho0": "--mixer-rho0", "mfrac": "--mixer-frac", "ganmix": "--gan-mix", "ganwarm": "--gan-warm",
      "ganlr": "--gan-lr", "qk": "--quark-k", "qpool": "--quark-pool", "espop": "--es-pop", "esm": "--es-m",
      "essig": "--es-sigma", "eslr": "--es-lr",
      "orpol": "--orpo-lam", "dsync": "--dpo-sync", "gstd": "--gpg-std"}
def tep_cua(r):
    al, rw = r.split(":")[:2]
    ok = opt_of(r)
    if al in ("ppo", "a2c"): return "grpo_ppo.py"
    if al == "sft": return "sft_tiep.py"
    if ok.get("tu") == "base": return "grpo_tu_base.py"
    if al in B4: return "grpo_moi_b4.py"
    if rw in T6: return "thuong_t6.py"
    if al in B1: return "grpo_moi_b1.py"
    if al in B2 or rw == "bcmr": return "grpo_moi_b2.py"
    if rw in B3: return "thuong_moi.py"
    return "grpo_codien.py" if al in CD or set(ok) - {"tag", "tu"} or (al != "grpo" and rw != "spice") else "grpo_luoi.py"
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
        if k not in ("tag", "tu"):
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
        msg += (f" · {st.mean(d.get('step_time', 0) for d in x):.0f} s/buoc · thuong {st.mean(d['reward'] for d in x if 'reward' in d) if any('reward' in d for d in x) else float('nan'):.3f}"
                f" · kl {st.mean(d.get('kl', 0) for d in x):.4f} · |A| {st.mean(d['luoi/adv_abs_mean'] for d in x if 'luoi/adv_abs_mean' in d) if any('luoi/adv_abs_mean' in d for d in x) else float('nan'):.3f}")
    for k in ("[xong]", "[nạp default]", "[câu nhắc] trùng", "[xuất phát]", "[moi_b4]"):
        y = [l for l in L if l.startswith(k)]
        if y: msg += "\\n      " + y[-1][:150]
    if any("Traceback" in l or "OutOfMemory" in l or "Killed" in l for l in L[-80:]): msg += "\\n      ⚠️ Traceback/OOM o cuoi log"
    return msg
while any(p.poll() is None for _, _, p in P):
    time.sleep(120)
    if GIU_SO > 0:
        for _, o, _ in P:
            c = sorted(glob.glob(f"{o}/checkpoint-*"), key=lambda s: int(s.rsplit("-", 1)[1]))
            for x in c[:-GIU_SO]:
                shutil.rmtree(x, ignore_errors=True); print("  [xoa diem luu cu]", x, flush=True)
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
         for c in (C1, C2, C3, C4.replace("CAT_GIO", str(CAT_H)).replace("GIU_SO", str(GIU_CK)).replace("PROBE_GIO", str(PROBE_H)))]
nb = {"cells": cells, "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}},
      "nbformat": 4, "nbformat_minor": 5}
d = os.path.join(H, f"k_{name}")
os.makedirs(d, exist_ok=True)
json.dump(nb, open(os.path.join(d, f"{name}.ipynb"), "w"), ensure_ascii=False, indent=1)
meta = {"id": f"{user}/{name}", "title": name, "code_file": f"{name}.ipynb", "language": "python",
        "kernel_type": "notebook", "is_private": "true", "enable_gpu": "true", "enable_internet": "true",
        "dataset_sources": [f"{user}/fgrb-p1-bundle", f"{user}/grpo-luoi-script"] + ([f"{user}/luoi-kit"] if set(FILES) - set(BASE) else []) + DS_THEM,
        "competition_sources": [], "kernel_sources": ([prev] if prev else [])}
json.dump(meta, open(os.path.join(d, "kernel-metadata.json"), "w"), indent=1)
print("đã dựng", d, "·", RUNS, "·", mode)
