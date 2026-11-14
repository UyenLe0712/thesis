# -*- coding: utf-8 -*-
"""Chuyển một notebook Kaggle (thư mục có <tên>.ipynb + kernel-metadata.json) thành notebook Colab chạy y hệt (11/11/2026).

  CAT_H=… python3 make_*.py … (trần giờ đặt lúc dựng notebook Kaggle)
  python3 _bundles/colab_tu_kaggle.py <thư mục kernel> [--them-kernel user/kernel ...]

Colab chỉ có 1 GPU, nên mọi tiến trình con đều chạy trên GPU 0 (A100 40 GB chứa được hai tiến trình 3B fp16).
Ô đầu (thêm vào):
  · gắn Drive, tải mọi dataset_sources/kernel_sources của kernel về /kaggle/input/<slug> bằng Kaggle CLI
    (Colab secret KAGGLE_<CHỦ DATASET viết hoa>, ví dụ KAGGLE_UYENLE0712 = khoá KGAT_ của tài khoản đó)
  · vá subprocess.Popen thêm start_new_session=True (bấm Stop một ô không giết tiến trình train)
Trước ô cuối: chép /content/drive/MyDrive/thesis/colab_kaggle/<tên>/ về /kaggle/working (chạy tiếp sau khi mất máy),
rồi luồng nền đồng bộ /kaggle/working → Drive mỗi 5 phút. Ô cuối thêm: đồng bộ lần chót.
"""
import json, os, re, sys, argparse

ap = argparse.ArgumentParser()
ap.add_argument("kdir")
ap.add_argument("--them-kernel", nargs="*", default=[], help="kernel output thêm vào /kaggle/input")
a = ap.parse_args()
meta = json.load(open(os.path.join(a.kdir, "kernel-metadata.json")))
nb = json.load(open(os.path.join(a.kdir, meta["code_file"]), encoding="utf-8"))
name = meta["title"]
owner = meta["id"].split("/")[0]
DS = meta.get("dataset_sources", [])
KS = meta.get("kernel_sources", []) + a.them_kernel

cells = ["".join(c["source"]) for c in nb["cells"]]
out = []
for c in cells:
    c = c.replace("torch.cuda.device_count() == 2", "torch.cuda.device_count() >= 1")
    c = c.replace('"CUDA_VISIBLE_DEVICES": str(gpu)', '"CUDA_VISIBLE_DEVICES": "0"')
    c = c.replace('"CUDA_VISIBLE_DEVICES": str(g)', '"CUDA_VISIBLE_DEVICES": "0"')
    c = c.replace('"CUDA_VISIBLE_DEVICES": str(i)', '"CUDA_VISIBLE_DEVICES": "0"')
    # kiểm hoà SA-SPICE trên GPU khác T4: cho lệch tối đa 1/3 câu (fp16 khác phần cứng), in cảnh báo rõ
    c = c.replace('assert py("sa3_grpo.py", "--kiem-hoa", "--data", D, "--merged", SFTM) == 0, "DUNG: kiem hoa"',
                  'KH = py("sa3_grpo.py", "--kiem-hoa", "--data", D, "--merged", SFTM)\n'
                  'if KH != 0:\n'
                  '    r_ = subprocess.run(["python", "sa3_grpo.py", "--kiem-hoa", "--data", D, "--merged", SFTM], cwd=W, capture_output=True, text=True).stdout\n'
                  '    k_ = re.findall(r"trùng kernel 1: (\\d+)/(\\d+)", r_)\n'
                  '    assert k_ and int(k_[-1][0]) >= int(k_[-1][1]) - 1, "DUNG: kiem hoa lech qua 1 cau"\n'
                  '    print("⚠️ COLAB: kiem hoa lech", k_[-1], "— GPU khac T4, chap nhan lech 1 cau, GHI VAO BAO CAO", flush=True)')
    for bad in ("str(gpu)", "str(g)"):
        assert f'"CUDA_VISIBLE_DEVICES": {bad}' not in c
    out.append(c)

dl_ds = "\n".join(f'tai(["datasets", "download", "-d", "{d}", "-p", "/kaggle/input/{d.split("/")[1]}", "--unzip"])' for d in DS)
dl_k = "\n".join(f'tai(["kernels", "output", "{k}", "-p", "/kaggle/input/{k.split("/")[1]}"])' for k in KS)
C0 = f'''# ===== Ô COLAB (thêm bởi _bundles/colab_tu_kaggle.py) — notebook gốc: {meta["id"]} =====
# Cần: Runtime GPU (A100 nếu chạy hai tiến trình), Colab secret KAGGLE_{owner.upper()} = khoá KGAT_ của tài khoản Kaggle "{owner}".
import os, subprocess, sys, glob, time, threading, shutil, json
import subprocess as _sp
class _Popen(_sp.Popen):
    def __init__(self, *a, **k):
        k.setdefault("start_new_session", True); super().__init__(*a, **k)
_sp.Popen = _Popen
from google.colab import drive, userdata
if not os.path.isdir("/content/drive/MyDrive"):   # chạy qua Colab CLI thì gắn trước bằng `colab drivemount`
    drive.mount("/content/drive")
DRIVE = "/content/drive/MyDrive/thesis/colab_kaggle/{name}"
os.makedirs(DRIVE, exist_ok=True); os.makedirs("/kaggle/input", exist_ok=True); os.makedirs("/kaggle/working", exist_ok=True)
SEC = "KAGGLE_{owner.upper()}"   # Colab secret: khoá KGAT_ của tài khoản {owner}
TOKF = "/content/.kaggle_tok/access_token"   # Colab CLI: `colab upload` tệp khoá lên đây (KAGGLE_API_TOKEN nhận đường dẫn tệp)
if os.path.isfile(TOKF): os.environ["KAGGLE_API_TOKEN"] = TOKF
else:
  try: os.environ["KAGGLE_API_TOKEN"] = userdata.get(SEC)
  except Exception: raise SystemExit(f"DUNG: them Colab secret {{SEC}} (khoa KGAT_ cua tai khoan {owner}) va bat 'Notebook access'")
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "kaggle>=2.2.4"], check=True)
def tai(args):
    t0 = time.time()
    r = subprocess.run(["kaggle", *args], capture_output=True, text=True)
    print(" ".join(args[:3]), "· ma", r.returncode, f"· {{time.time()-t0:.0f}} s", (r.stdout + r.stderr)[-300:].replace(os.environ["KAGGLE_API_TOKEN"], "***"), flush=True)
    assert r.returncode == 0, "DUNG: tai tu Kaggle loi (sai tai khoan? can tai khoan {owner})"
{dl_ds}
{dl_k}
print(subprocess.run("du -sh /kaggle/input/* ; nvidia-smi --query-gpu=name,memory.total --format=csv,noheader; df -h / | tail -1", shell=True, capture_output=True, text=True).stdout, flush=True)
'''
C_RESTORE = '''# ===== Ô COLAB: chạy tiếp sau mất máy + đồng bộ Drive mỗi 5 phút =====
if os.listdir(DRIVE):
    print("khoi phuc tu Drive:", subprocess.run(f"rsync -a '{DRIVE}/' /kaggle/working/ && du -sh /kaggle/working", shell=True, capture_output=True, text=True).stdout, flush=True)
def _dong_bo():
    while True:
        time.sleep(300)
        subprocess.run(f"rsync -a --exclude '*.zip' /kaggle/working/ '{DRIVE}/'", shell=True)
threading.Thread(target=_dong_bo, daemon=True).start()
print("✅ dong bo Drive moi 5 phut →", DRIVE, flush=True)
'''
C_END = '''# ===== Ô COLAB: đồng bộ lần chót =====
print(subprocess.run(f"rsync -a /kaggle/working/ '{DRIVE}/' && ls -la '{DRIVE}' | tail -20", shell=True, capture_output=True, text=True).stdout, flush=True)
'''
allc = [C0] + out[:-1] + [C_RESTORE, out[-1], C_END]
for i, c in enumerate(allc):
    compile(c, f"c{i}", "exec")
nb2 = {"nbformat": 4, "nbformat_minor": 5,
       "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}, "language_info": {"name": "python"},
                    "accelerator": "GPU", "colab": {"provenance": []}},
       "cells": [{"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "id": f"c{i}", "source": c.splitlines(keepends=True)}
                 for i, c in enumerate(allc)]}
# bản một-lệnh cho Colab CLI: cả notebook chạy trong MỘT lần exec ⇒ laptop tắt giữa chừng vẫn chạy hết các ô
cli = ("# -*- coding: utf-8 -*-\n# Sinh bởi colab_tu_kaggle.py — chạy: colab exec -s <phiên> -f " + f"{name}_colab_cli.py\n"
       "import json as _json, time as _t\n_O = _json.loads(" + repr(json.dumps(allc, ensure_ascii=False)) + ")\n"
       "for _i, _c in enumerate(_O):\n"
       "    print(f'===== O {_i}/{len(_O)-1} · {_t.strftime(\"%H:%M:%S\")} =====', flush=True)\n"
       "    exec(compile(_c, f'o{_i}', 'exec'), globals())\n"
       "print('===== XONG CA NOTEBOOK =====', flush=True)\n")
compile(cli, "cli", "exec")
open(os.path.join(a.kdir, f"{name}_colab_cli.py"), "w", encoding="utf-8").write(cli)
dst = os.path.join(a.kdir, f"{name}_colab.ipynb")
json.dump(nb2, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("đã dựng", dst, "· tài khoản", owner, "· dataset", DS, "· kernel", KS)
