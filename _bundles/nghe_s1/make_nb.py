"""Dựng notebook Kaggle PROBE cho lượt "người nghe Phi-4 từ S1" (report/330 §7 hàng 7):
GRPO thưởng SPICE + người nghe (nhánh `nghe` = SPICE + LR, λ = 1), LoRA MỚI từ S1 (không --tu), hạt 101.
Policy ở GPU0, máy chủ người nghe Phi-4 ở GPU1 (venv riêng transformers 4.48.2). 20 bước, trần ~2 h.

    python3 -I make_nb.py [tài khoản, mặc định trangphuongngoc] [tên kernel, mặc định nghe-s1-probe]
    biến môi trường: TRAN_H (trần giờ cả notebook, mặc định 2.0) · BUOC (số bước, mặc định 20)
→ k_<tên kernel>/ (ipynb + kernel-metadata.json). Đẩy (user tự đẩy):
    kg trang2 kernels push -p k_nghe-s1-probe --accelerator NvidiaTeslaT4

Vì sao `--train --max-steps 20` mà KHÔNG dùng `--probe`: `--probe` của grpo_spice lấy 50 câu nhắc DÀI NHẤT,
chỉ 5/50 nằm trong bảng người nghe (đo trên máy nhà 7/11) ⇒ gần như không hỏi người nghe, đo sai tốc độ.
`--train` lấy đúng 1.000 câu nhắc ck500 (hạt 101); 40 câu nhắc của 20 bước đầu có 29 câu trong bảng.
Đỉnh VRAM phía người nghe đo riêng ở Ô 3 trên 20 màn nhiều ô nhất (tới 91 ô).
"""
import hashlib, json, os, sys

user = sys.argv[1] if len(sys.argv) > 1 else "trangphuongngoc"
name = sys.argv[2] if len(sys.argv) > 2 else "nghe-s1-probe"
TRAN_H = float(os.environ.get("TRAN_H", 2.0))
BUOC = int(os.environ.get("BUOC", 20))
H = os.path.dirname(os.path.abspath(__file__))
DS = os.path.join(H, f"ds_{user}")
assert os.path.isdir(DS), f"chạy build_ds.py {user} trước"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
MD5 = {f: md5(os.path.join(DS, f)) for f in sorted(os.listdir(DS)) if f != "dataset-metadata.json"}

C1 = r'''# Ô 1 — cài đặt: stack train ghim như lưới (trl 0.29.1 · transformers 5.20.2 · peft 0.21.2) + venv RIÊNG cho Phi-4 (transformers 4.48.2)
import subprocess, sys, os, time
T_NB = time.time()
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless")
sh("update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java")
sh("java -version")
sh(f"{sys.executable} -m pip install -q 'transformers==5.20.2' 'peft==0.21.2' 'trl==0.29.1' accelerate pycocoevalcap -U torchao 2>&1 | tail -3")
sh(f'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.device_count(), torch.cuda.get_device_name(0))"')
import trl, transformers, peft, torch
assert (trl.__version__, transformers.__version__, peft.__version__) == ("0.29.1", "5.20.2", "0.21.2"), "DUNG: lech phien ban"
assert torch.cuda.device_count() == 2, "DUNG: can 2 GPU T4"
# venv Phi-4: thấy torch của hệ thống (--system-site-packages), transformers/peft/accelerate riêng
VPY = "/tmp/vphi/bin/python"
if not os.path.exists("/tmp/vphi/bin/pip"):
    sh(f"{sys.executable} -m pip install -q virtualenv && {sys.executable} -m virtualenv -q --system-site-packages /tmp/vphi")
assert os.path.exists("/tmp/vphi/bin/pip"), "DUNG: chua dung duoc venv phi4"
sh("/tmp/vphi/bin/pip install -q transformers==4.48.2 peft==0.13.2 accelerate==1.3.0 backoff soundfile scipy 2>&1 | tail -3")
r = subprocess.run([VPY, "-c", "import sys; sys.modules['torchao'] = None; import transformers, peft, accelerate, torch; "
                    "print(transformers.__version__, peft.__version__, accelerate.__version__, torch.__version__)"],
                   capture_output=True, text=True)
print("venv phi4:", r.stdout.strip(), r.stderr[-800:], flush=True)
assert r.stdout.split()[:3] == ["4.48.2", "0.13.2", "1.3.0"], "DUNG: venv phi4 lech phien ban"
# tải Phi-4 ở nền, ghi log ra tệp (không để thanh tiến trình ngập log)
ENV_Q = {"TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1"}
TAI = subprocess.Popen([VPY, "-c", "from huggingface_hub import snapshot_download as s; print(s('microsoft/Phi-4-multimodal-instruct'))"],
                       stdout=open("/tmp/tai_phi4.log", "w"), stderr=subprocess.STDOUT, env={**os.environ, **ENV_Q})
print(f"Ô 1 xong · {(time.time()-T_NB)/60:.1f} phút · đang tải Phi-4 ở nền (PID {TAI.pid})", flush=True)
'''

C2 = r'''# Ô 2 — chép mã + md5, jar SPICE, selftest CPU, bật máy chủ người nghe ở GPU1, hoà S1 (fp16) ở GPU0
import glob, shutil, hashlib, json, threading
W = "/kaggle/working"; O = f"{W}/nghe_s1_probe"; os.makedirs(O, exist_ok=True)
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "images" in d)
MD5 = __MD5__
for f, h in MD5.items():
    k = [p for p in glob.glob(f"/kaggle/input/**/{f}", recursive=True) if "/notebooks/" not in p and md5(p) == h]
    assert k, f"DUNG: khong thay {f} dung md5 {h} (grpo-luoi-script co grpo_spice.py ban khac, phai lay ban nghe-s1-kit)"
    shutil.copy(k[0], f"{W}/{f}"); assert md5(f"{W}/{f}") == h
print("mã: md5 khớp", len(MD5), "tệp · BUNDLE", BUNDLE, flush=True)
import importlib.util
SPL = list(importlib.util.find_spec("pycocoevalcap").submodule_search_locations)[0] + "/spice/lib"
for j, sz in {"stanford-corenlp-3.6.0.jar": 7270741, "stanford-corenlp-3.6.0-models.jar": 378116526}.items():
    dst = f"{SPL}/{j}"
    if os.path.exists(dst) and os.path.getsize(dst) == sz: continue
    src = glob.glob(f"/kaggle/input/**/{j}", recursive=True); assert src, f"DUNG: thieu {j} (gan dataset grpo-luoi-script)"
    shutil.copy(src[0], dst); assert os.path.getsize(dst) == sz, f"DUNG: {j} sai kich thuoc"
print("jar SPICE đủ", flush=True)
B_ = json.load(open(f"{W}/bang_nghe.json"))["bang"]
thieu = [k for k, b in B_.items() if not os.path.exists(os.path.join(BUNDLE, b["image"]))]
print(f"bảng {len(B_)} màn · thiếu ảnh {len(thieu)}", flush=True); assert not thieu, f"DUNG: thieu anh {thieu[:3]}"
r = subprocess.run(["python", "grpo_nghe.py", "--selftest"], cwd=W, capture_output=True, text=True)
print((r.stdout + r.stderr)[-700:], flush=True); assert r.returncode == 0, "DUNG: selftest grpo_nghe rot"
# lấy mẫu VRAM hai GPU mỗi 10 s suốt notebook (đỉnh memory.used, MiB)
DINH = {"0": 0, "1": 0}
def lay_mau():
    while True:
        q = subprocess.run("nvidia-smi --query-gpu=index,memory.used --format=csv,noheader,nounits", shell=True,
                           capture_output=True, text=True).stdout.split("\n")
        for l in q:
            if "," in l:
                i, m = [x.strip() for x in l.split(",")]; DINH[i] = max(DINH.get(i, 0), int(m))
        time.sleep(10)
threading.Thread(target=lay_mau, daemon=True).start()
print("chờ tải Phi-4 …", flush=True)
while TAI.poll() is None:
    time.sleep(60)
    du = subprocess.run("du -sh ~/.cache/huggingface 2>/dev/null | cut -f1", shell=True, capture_output=True, text=True).stdout.strip()
    print(f"  {(time.time()-T_NB)/60:.1f} phút · cache HF {du or '?'}", flush=True)
print(open("/tmp/tai_phi4.log").read()[-400:], flush=True); assert TAI.returncode == 0, "DUNG: tai Phi-4 loi"
CONG = 47288
SV = subprocess.Popen([VPY, f"{W}/nghe_server.py", "--backend", "phi4", "--bang", f"{W}/bang_nghe.json", "--img-root", BUNDLE,
                       "--cong", str(CONG)], cwd=W, stdout=open(f"{O}/nghe_server.log", "a"), stderr=subprocess.STDOUT,
                      start_new_session=True,
                      env={**os.environ, **ENV_Q, "SOM_PHI4_CROPS": "16", "SOM_PHI4_ATTN": "sdpa", "CUDA_VISIBLE_DEVICES": "1",
                           "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"})
print("máy chủ người nghe PID", SV.pid, "· GPU1", flush=True)
MERGED = "/tmp/s1_merged"
r = subprocess.run(["python", "grpo_nghe.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED], cwd=W, capture_output=True, text=True,
                   env={**os.environ, **ENV_Q, "CUDA_VISIBLE_DEVICES": "0"})
print((r.stdout + r.stderr)[-700:], flush=True); assert r.returncode == 0, "DUNG: hoa S1 loi"
sys.path.insert(0, W); import grpo_nghe as GN
ten = GN.cho_may_chu(CONG, 1800)
print(f"máy chủ sẵn sàng: {ten} · {(time.time()-T_NB)/60:.1f} phút từ đầu notebook", flush=True)
print(open(f"{O}/nghe_server.log").read()[-800:], flush=True)
'''

C3 = r'''# Ô 3 — đo người nghe riêng (trước train): tốc độ trên 40 màn có đáp án + đỉnh VRAM GPU1 trên 20 màn NHIỀU Ô nhất
CAU = "Click on the search icon at the top"
ks = [k for k in sorted(B_) if B_[k]["dap_an"]][:40]
t0 = time.time(); q, loi = GN.hoi_may_chu([dict(key=k, sent=CAU) for k in ks], CONG, 900)
s_cau = (time.time() - t0) / len(ks)
nang = sorted(B_, key=lambda k: -len(B_[k]["boxes"]))[:20]
t1 = time.time(); q2, loi2 = GN.hoi_may_chu([dict(key=k, sent=CAU) for k in nang], CONG, 900)
s_nang = (time.time() - t1) / len(nang)
time.sleep(12)
DO_NGHE = {"s_cau_40": round(s_cau, 2), "loi_40": loi, "none_40": sum(x is None for x in (q or [])),
           "s_cau_nang20": round(s_nang, 2), "loi_nang20": loi2, "none_nang20": sum(x is None for x in (q2 or [])),
           "o_max": len(B_[nang[0]]["boxes"]), "dinh_gpu1_MiB_sau_do": DINH["1"]}
print("[đo người nghe]", DO_NGHE, flush=True)
print(open(f"{O}/nghe_server.log").read()[-400:], flush=True)
json.dump(DO_NGHE, open(f"{O}/do_nguoi_nghe.json", "w"), ensure_ascii=False, indent=1)
'''

C4 = r'''# Ô 4 — train __BUOC__ bước: GRPO nhánh `nghe` (SPICE + 1·h), LoRA MỚI từ S1 (KHÔNG --tu), GPU0; nhịp sống 2 phút; dừng ở trần
import re, ast, statistics as st
TRAN = 3600 * __TRAN_H__ - 8 * 60          # chừa 8 phút cho Ô 5 (zip)
OUT = f"{O}/nghe_101"
cmd = ["python", "grpo_nghe.py", "--train", "--arm", "nghe", "--seed", "101", "--no-q4", "--bs", "4", "--accum", "4",
       "--gen-chunk", "8", "--bundle", BUNDLE, "--merged", MERGED, "--out", OUT, "--resume", "auto", "--cong", str(CONG),
       "--max-steps", "__BUOC__", "--bang", f"{W}/bang_nghe.json"]
LOG = f"{O}/train_nghe_101.log"
P = subprocess.Popen(cmd, cwd=W, stdout=open(LOG, "a"), stderr=subprocess.STDOUT, start_new_session=True,
                     env={**os.environ, **ENV_Q, "CUDA_VISIBLE_DEVICES": "0", "PYTORCH_ALLOC_CONF": "expandable_segments:True",
                          "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"})
print(" ".join(cmd), "\nPID", P.pid, flush=True)
def doc():
    L = open(LOG, encoding="utf-8", errors="ignore").read().splitlines()
    D = []
    for l in L:
        if l.startswith("{'loss'"):
            try: D.append({k: float(v) for k, v in ast.literal_eval(l).items() if re.match(r"^[-\d.e+na]+$", str(v))})
            except Exception: pass
    ng = [l for l in L if l.startswith("[nghe] lần")]
    f_ = lambda pat: sum(int(m.group(1)) for l in ng if (m := re.search(pat, l)))
    T = [d["step_time"] for d in D[2:] if "step_time" in d]          # bỏ 2 bước đầu (khởi động)
    kq = {"buoc": len(D), "s_buoc_tb": round(st.mean(T), 1) if T else None, "s_buoc_tv": round(st.median(T), 1) if T else None,
          "thuong_tb10": round(st.mean(d["reward"] for d in D[-10:] if "reward" in d), 3) if any("reward" in d for d in D[-10:]) else None,
          "kl_tb10": round(st.mean(d.get("kl", 0) for d in D[-10:]), 4) if D else None,
          "nghe_lan": len(ng), "cham": f_(r"chạm (\d+)/"), "bat": f_(r"bật (\d+)"), "hoi": f_(r"hỏi (\d+)"),
          "trung": f_(r"trúng (\d+)"), "dinh_dang": f_(r"định dạng (\d+)"), "loi_may_chu": sum("lỗi máy chủ" in l for l in ng),
          "nghe_dt_tb": round(st.mean(float(m.group(1)) for l in ng if (m := re.search(r"· ([\d.]+)s$", l))), 1) if ng else None,
          "spice_s_lan": None}
    sp = [float(m.group(1)) for l in L if l.startswith("[spice]") and (m := re.search(r"· ([\d.]+)s ·", l))]
    if sp: kq["spice_s_lan"] = round(st.mean(sp), 1)
    xg = [m for l in L if l.startswith("[xong]") and (m := re.search(r"([\d.]+) s/bước", l))]
    if xg and not T: kq["s_buoc_tb"] = kq["s_buoc_tv"] = float(xg[-1].group(1))   # TRL không ghi step_time thì lấy dòng [xong] (gồm cả bước đầu)
    for k in ("[xong]", "[LoRA mới]", "[train tiếp]", "[nhánh]", "[lô]", "[tiếp từ]", "[câu nhắc]", "[bảng]", "[nghe] máy chủ"):
        y = [l for l in L if l.startswith(k)]
        if y: kq[k] = y[-1][:220]
    kq["traceback"] = any("Traceback" in l or "OutOfMemory" in l or "out of memory" in l for l in L)
    return kq
while P.poll() is None:
    time.sleep(120)
    ram = subprocess.run("free -g | awk '/Mem/{print $3\"/\"$2\" GB\"}'", shell=True, capture_output=True, text=True).stdout.strip()
    k = doc()
    print(f"{(time.time()-T_NB)/3600:5.2f} h · RAM {ram} · đỉnh VRAM MiB GPU0 {DINH['0']} · GPU1 {DINH['1']} · máy chủ "
          f"{'sống' if SV.poll() is None else 'CHẾT'}\n   bước {k['buoc']}/__BUOC__ · {k['s_buoc_tb']} s/bước (TB, bỏ 2 đầu) · "
          f"thưởng {k['thuong_tb10']} · kl {k['kl_tb10']} · SPICE {k['spice_s_lan']} s/lần\n   [nghe] lần {k['nghe_lan']} · hỏi {k['hoi']} câu · "
          f"trúng {k['trung']} · lỗi máy chủ {k['loi_may_chu']} · {k['nghe_dt_tb']} s/lần thưởng" + ("\n   ⛔ Traceback/OOM trong log" if k["traceback"] else ""), flush=True)
    if time.time() - T_NB > TRAN:
        print("⛔ chạm trần giờ, dừng train để kịp lưu Output", flush=True)
        P.terminate(); P.wait()
print("mã thoát train", P.returncode, flush=True)
print("\n".join(l for l in open(LOG, encoding="utf-8", errors="ignore").read().splitlines()[-40:]
                if not l.startswith(("PTB", "Parsing", "Threads", "Loading", "[main]"))), flush=True)
'''

C5 = r'''# Ô 5 — tổng kết + ước tính lượt đủ 500 bước, tắt máy chủ, zip RIÊNG thư mục kết quả
import math, zipfile
k = doc()
s = k["s_buoc_tv"] or k["s_buoc_tb"]
TK = {"ma_thoat": P.returncode, "dinh_VRAM_MiB": dict(DINH), "do_nguoi_nghe": DO_NGHE, **k,
      "uoc_500_buoc_h": round(500 * s / 3600, 1) if s else None,
      "uoc_commit_11h": math.ceil(500 * s / 3600 / 10.3) if s else None,
      "cau_nhac_trung_ck500": (json.load(open(f"{OUT}/prompt_keys.json")) == json.load(open(f"{W}/prompt_keys_ck500.json")))
                              if os.path.exists(f"{OUT}/prompt_keys.json") else None,
      "gio_notebook": round((time.time() - T_NB) / 3600, 2)}
print(json.dumps(TK, ensure_ascii=False, indent=1), flush=True)
json.dump(TK, open(f"{O}/tong_ket.json", "w"), ensure_ascii=False, indent=1)
try: os.killpg(SV.pid, 15)
except Exception as e: print("tắt máy chủ:", e)
shutil.rmtree(f"{OUT}/final", ignore_errors=True); shutil.rmtree(MERGED, ignore_errors=True)
Z = f"{W}/nghe_s1_probe.zip"
with zipfile.ZipFile(Z, "w", zipfile.ZIP_DEFLATED) as z:
    for r_, _, fs in os.walk(O):
        for f in fs:
            p = os.path.join(r_, f)
            if os.path.getsize(p) < 200 * 2**20 and "/checkpoint-" not in p:
                z.write(p, os.path.relpath(p, W))
for i in zipfile.ZipFile(Z).infolist(): print(f"  {i.file_size/1024:9.1f} KB  {i.filename}")
print("ZIP", Z, f"{os.path.getsize(Z)/2**20:.2f} MB", flush=True)
'''

C2 = C2.replace("__MD5__", repr(MD5))
C4 = C4.replace("__BUOC__", str(BUOC)).replace("__TRAN_H__", str(TRAN_H))
cells = [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": c.splitlines(True)}
         for c in (C1, C2, C3, C4, C5)]
nb = {"cells": cells, "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}},
      "nbformat": 4, "nbformat_minor": 5}
d = os.path.join(H, f"k_{name}")
os.makedirs(d, exist_ok=True)
json.dump(nb, open(os.path.join(d, f"{name}.ipynb"), "w"), ensure_ascii=False, indent=1)
meta = {"id": f"{user}/{name}", "title": name, "code_file": f"{name}.ipynb", "language": "python",
        "kernel_type": "notebook", "is_private": "true", "enable_gpu": "true", "enable_internet": "true",
        "dataset_sources": [f"{user}/fgrb-p1-bundle", f"{user}/grpo-luoi-script", f"{user}/nghe-s1-kit"],
        "competition_sources": [], "kernel_sources": []}
json.dump(meta, open(os.path.join(d, "kernel-metadata.json"), "w"), indent=1)
print("đã dựng", d, "·", BUOC, "bước · trần", TRAN_H, "h ·", len(MD5), "tệp kiểm md5")
