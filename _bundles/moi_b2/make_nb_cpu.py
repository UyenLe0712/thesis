# -*- coding: utf-8 -*-
"""Dựng gói dataset + notebook Kaggle CPU kiểm grpo_moi_b2.py bằng mô hình tí hon (tài khoản trang2).

  python make_nb_cpu.py            # chép mã harness vào ds/, viết k/
  kg trang2 datasets create -p ds --dir-mode zip   (lần sau: datasets version -p ds -m "..." --dir-mode zip)
  kg trang2 kernels push -p k
"""
import os, json, shutil, hashlib

H = os.path.dirname(os.path.abspath(__file__))
K = os.path.join(H, "..", "..", "harness")
FILES = ["grpo_moi_b2.py", "grpo_codien.py", "grpo_luoi.py", "grpo_spice.py", "build_branch_data.py"]
for f in FILES:
    shutil.copyfile(os.path.join(K, f), os.path.join(H, "ds", f))
MD5 = {f: hashlib.md5(open(os.path.join(H, "ds", f), "rb").read()).hexdigest() for f in FILES + ["test_cpu.py", "prep_tihon.py"]}
json.dump({"title": "moi-b2-code", "id": "trangphuongngoc/moi-b2-code", "licenses": [{"name": "CC0-1.0"}]},
          open(os.path.join(H, "ds", "dataset-metadata.json"), "w"), indent=1)

C1 = '''import subprocess, sys, os, glob, shutil, time, json, math
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True); print(r.stdout[-1500:], r.stderr[-1500:], flush=True); return r.returncode
sh(f"{sys.executable} -m pip install -q 'transformers==5.20.2' 'peft==0.21.2' 'trl==0.29.1' accelerate pycocoevalcap sacrebleu 2>&1 | tail -3")
sh(f"{sys.executable} -m pip uninstall -y torchao 2>&1 | tail -1")
sh("apt-get -qq update >/dev/null && apt-get -qq install -y openjdk-8-jre-headless >/dev/null; update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java; java -version")
assert sh(f\'\'\'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__); assert (trl.__version__, transformers.__version__, peft.__version__) == ('0.29.1', '5.20.2', '0.21.2')" \'\'\') == 0, "DUNG: moi truong"
'''
C2 = f'''MD5 = {json.dumps(MD5)}
import hashlib
SRC = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/grpo_moi_b2.py", recursive=True)]
print(SRC, flush=True); assert len(SRC) == 1, SRC
W = "/kaggle/working/w"; shutil.rmtree(W, ignore_errors=True); shutil.copytree(SRC[0], W)
for f, h in MD5.items():
    assert hashlib.md5(open(f"{{W}}/{{f}}", "rb").read()).hexdigest() == h, f"DUNG: md5 {{f}}"
print("md5 du", flush=True)
T = "/kaggle/working/tihon"; os.makedirs(T, exist_ok=True)
assert sh(f"cd {{W}} && {{sys.executable}} prep_tihon.py {{T}}") == 0, "DUNG: dung mo hinh ti hon"
'''
C3 = '''KQ, LOG = {}, "/kaggle/working/logs"; os.makedirs(LOG, exist_ok=True)
B = f"{T}/bundle"
def chay(ten, *co, ok=0):
    t0 = time.time(); lg = f"{LOG}/{ten}.log"
    p = subprocess.Popen(f"cd {W} && {sys.executable} -u test_cpu.py {T} " + " ".join(co) + f" > {lg} 2>&1", shell=True)
    while p.poll() is None:
        time.sleep(30); print(time.strftime("%H:%M:%S"), ten, open(lg, errors="ignore").read()[-160:].replace("\\n", " | "), flush=True)
    L = open(lg, errors="ignore").read()
    KQ[ten] = dict(ma=p.returncode, giay=round(time.time() - t0))
    print("=====", ten, "ma thoat", p.returncode, f"{time.time()-t0:.0f} s", flush=True); print(L[-3500:], flush=True)
    return L
def kiem_log(ten, o, khoa=()):
    """log_history.json: mọi số hữu hạn, có đủ bước, có các khoá riêng của thuật toán."""
    h = [d for d in json.load(open(f"{o}/log_history.json")) if "loss" in d or "reward" in d]
    so = [v for d in h for v in d.values() if isinstance(v, (int, float))]
    thieu = [k for k in khoa if not any(k in d for d in h)]
    KQ[ten].update(n_log=len(h), huu_han=all(math.isfinite(v) for v in so), thieu=thieu,
                   cuoi={k: v for k, v in h[-1].items() if isinstance(v, (int, float))} if h else {})
    print(ten, KQ[ten], flush=True)
    return KQ[ten]["huu_han"] and not thieu and len(h) > 0
CHUNG = ["--train", "--no-q4", "--bs", "4", "--accum", "2", "--G", "4", "--seed", "101", "--bundle", B, "--n-prompt", "16", "--resume", "auto"]
DAT = {}
chay("selftest_algo", "--selftest-algo"); DAT["selftest_algo"] = KQ["selftest_algo"]["ma"] == 0
L = chay("selftest_bcmr", "--selftest-thuong", "--bundle", B, "--rewards", "bcmr,cider,rougel,meteor"); DAT["selftest_bcmr"] = KQ["selftest_bcmr"]["ma"] == 0
VIEC = [("grpo_doi_chung", ["--algo", "grpo", "--reward", "spice"], 3, ()),
        ("bcmr", ["--algo", "grpo", "--reward", "bcmr"], 3, ("reward",)),
        ("rlce", ["--algo", "rlce", "--reward", "spice", "--ce-lam", "0.1"], 3, ("rlce/ce",)),
        ("mixer", ["--algo", "mixer", "--reward", "spice", "--mixer-rho0", "0.5", "--mixer-frac", "1.0"], 3, ("mixer/k_tb", "mixer/rho")),
        ("seqgan", ["--algo", "seqgan", "--reward", "spice", "--gan-warm", "1"], 3, ("seqgan/d_loss", "seqgan/d_fake")),
        ("quark", ["--algo", "quark", "--reward", "spice"], 3, ("quark/muc5", "quark/kho"))]
for ten, co, n, khoa in VIEC:
    o = f"/kaggle/working/out_{ten}"; shutil.rmtree(o, ignore_errors=True)
    L = chay(ten, *CHUNG, *co, "--out", o, "--max-steps", str(n))
    DAT[ten] = KQ[ten]["ma"] == 0 and "[xong]" in L and os.path.exists(f"{o}/log_history.json") and kiem_log(ten, o, khoa)
    if ten == "mixer":
        DAT[ten] = DAT[ten] and "kiểm mm_token_type_ids dựng lại trùng processor ✓" in L
# lưu điểm lưu + chạy tiếp cho hai nhánh có trạng thái riêng (bộ phân biệt, kho thưởng): save_steps = 25 cố định trong grpo_luoi
for ten, co, khoa, dau in (("seqgan_tiep", ["--algo", "seqgan", "--reward", "spice", "--gan-warm", "1"], ("seqgan/d_loss",), "[seqgan] nạp bộ phân biệt"),
                           ("quark_tiep", ["--algo", "quark", "--reward", "spice"], ("quark/kho",), "[quark] nạp kho")):
    o = f"/kaggle/working/out_{ten}"; shutil.rmtree(o, ignore_errors=True)
    L1 = chay(ten + "_1", *CHUNG, *co, "--out", o, "--max-steps", "25")
    L2 = chay(ten + "_2", *CHUNG, *co, "--out", o, "--max-steps", "27")
    KQ[ten] = dict(ma=KQ[ten + "_2"]["ma"])
    DAT[ten] = (KQ[ten + "_1"]["ma"] == 0 and KQ[ten + "_2"]["ma"] == 0 and os.path.isdir(f"{o}/checkpoint-25")
                and dau in L2 and "[nạp default]" in L2 and kiem_log(ten, o, khoa))
# ES: 3 bước, lưu mỗi 2 bước, rồi chạy tiếp tới 4
o = "/kaggle/working/out_es"; shutil.rmtree(o, ignore_errors=True)
ES = ["--algo", "es", "--reward", "spice", "--es-pop", "4", "--es-m", "2", "--es-save", "2"]
L1 = chay("es_1", *CHUNG, *ES, "--out", o, "--max-steps", "3")
L2 = chay("es_2", *CHUNG, *ES, "--out", o, "--max-steps", "4")
KQ["es"] = dict(ma=KQ["es_2"]["ma"])
st = json.load(open(f"{o}/checkpoint-4/trainer_state.json")) if os.path.exists(f"{o}/checkpoint-4/trainer_state.json") else {}
DAT["es"] = (KQ["es_1"]["ma"] == 0 and KQ["es_2"]["ma"] == 0 and "[nạp default]" in L2 and st.get("global_step") == 4
             and kiem_log("es", o, ("es/buoc_l2", "es/so_cau_khac", "es/buoc_tuong_doi")) and all(d["es/buoc_l2"] > 0 for d in st["log_history"]))
print(json.dumps(DAT, indent=1), flush=True)
json.dump(dict(dat=DAT, kq=KQ), open("/kaggle/working/ket_qua_cpu_b2.json", "w"), ensure_ascii=False, indent=1)
'''
C4 = '''for d in glob.glob("/kaggle/working/out_*"):
    for c in glob.glob(f"{d}/checkpoint-*") + glob.glob(f"{d}/final"):
        shutil.rmtree(c, ignore_errors=True)
shutil.rmtree(W, ignore_errors=True); shutil.rmtree(T, ignore_errors=True)
sh("cd /kaggle/working && zip -q -r ket_qua_cpu_b2.zip logs ket_qua_cpu_b2.json out_*/log_history.json && ls -la")
assert all(DAT.values()), {k: v for k, v in DAT.items() if not v}
'''
os.makedirs(os.path.join(H, "k"), exist_ok=True)
nb = {"cells": [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": c} for c in (C1, C2, C3, C4)],
      "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}, "nbformat": 4, "nbformat_minor": 4}
json.dump(nb, open(os.path.join(H, "k", "moi-b2-cpu.ipynb"), "w"), ensure_ascii=False, indent=1)
json.dump({"id": "trangphuongngoc/moi-b2-cpu", "title": "moi-b2-cpu", "code_file": "moi-b2-cpu.ipynb", "language": "python",
           "kernel_type": "notebook", "is_private": "true", "enable_gpu": "false", "enable_internet": "true",
           "dataset_sources": ["trangphuongngoc/moi-b2-code"], "competition_sources": [], "kernel_sources": []},
          open(os.path.join(H, "k", "kernel-metadata.json"), "w"), indent=1)
print("md5:", MD5)
