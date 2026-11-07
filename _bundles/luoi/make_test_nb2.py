"""Dựng notebook Kaggle chấm TEST cho các lượt của lưới RL (thay make_test_nb.py, 6/11/2026).

Khác bản cũ (k_luoi-test-t-1 viết cứng hai lượt):
  · hàng đợi nhiều lượt trên 2 GPU T4, mỗi GPU lấy lượt kế khi xong lượt trước
  · adapter đọc từ dataset kit (mặc định <user>/sft-colab-kit) theo md5, không cần kernel train cùng tài khoản
  · trước khi chấm: kiểm bộ chấm (10 bước S1 phải trùng toạ độ tệp thô cũ) + kiểm hoà (≥16/20 trùng S1)
  · nối tiếp: có kernel trước thì chép pred/raw cũ rồi chạy nốt
  · chế độ smoke: sinh 20 câu + chấm 20 bước mỗi lượt, để kiểm đường chạy, KHÔNG dùng số

python make_test_nb2.py <user> <kernel> <full|smoke> <ten=thu_muc:md5> [...]
  biến môi trường: CAT_H (trần giờ, mặc định 11; smoke 0,42) · KIT (dataset kit) · PREV (kernel trước để nối tiếp)
ví dụ:
  python make_test_nb2.py uyenle0712 luoi-test-u-3 full sft_tiep_101=sft_final:113e2a3e6a0781fd5121acda99962d1b \
      rloo_spice_101=rloo_spice_101:0efff3eb11f96370097eeafa9410e8cc reinforce_spice_101=reinforce_spice_101:e0e9c51585f416337a25c52f6e7c8505
  kg uyenle kernels push -p k_luoi-test-u-3 --accelerator NvidiaTeslaT4
"""
import json, sys, os

user, name, mode, *spec = sys.argv[1:]
assert mode in ("full", "smoke", "nontap", "nontap-smoke") and spec
NT = mode.startswith("nontap")
LUOT = []
for s in spec:
    ten, rest = s.split("=")
    d, h = rest.split(":")
    assert len(h) == 32, s
    LUOT.append((ten, d, h))
CAT_H = float(os.environ.get("CAT_H", 0.42 if mode.endswith("smoke") else 11))
KIT = os.environ.get("KIT", f"{user}/sft-colab-kit")
PREV = os.environ.get("PREV")
N = 20 if mode.endswith("smoke") else 0
H = os.path.dirname(os.path.abspath(__file__))

C1 = '''import subprocess, sys, os, time, threading, glob, json, shutil, hashlib, queue, zipfile
T_NB = time.time()
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh(f"{sys.executable} -m pip install -q 'transformers==5.20.2' 'peft==0.21.2' 'trl==0.29.1' accelerate bitsandbytes 2>&1 | tail -3")
sh(f"{sys.executable} -m pip uninstall -y torchao 2>&1 | tail -1")
assert sh(f\'\'\'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.device_count(), torch.cuda.get_device_name(0)); assert (trl.__version__, transformers.__version__, peft.__version__) == ('0.29.1', '5.20.2', '0.21.2'), 'lech phien ban'; assert torch.cuda.device_count() == 2, 'can 2 GPU'" \'\'\') == 0, "DUNG: moi truong"
print("✅ moi truong", flush=True)
'''
C2 = f'''W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
MODE, N, CAT, NT = {mode!r}, {N}, 3600 * {CAT_H}, {NT!r}
LUOT = {LUOT!r}
KIT = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/gen_test_grpo.py", recursive=True)
       if "/notebooks/" not in p and os.path.isdir(os.path.join(os.path.dirname(p), "adapter_s1_seed101"))]
assert len(KIT) == 1, f"DUNG: can dung mot kit, thay {{KIT}}"
KIT = KIT[0]
assert md5(f"{{KIT}}/grpo_spice.py") == "07ea87b6d156d1faa391a4274dffd7cf", "DUNG: grpo_spice.py lech"
assert md5(f"{{KIT}}/gen_test_grpo.py") == "b18ec1aa3fd037ddffb9411db63c2a3f", "DUNG: gen_test_grpo.py lech"
assert md5(f"{{KIT}}/tai_dung_cham.py") == "574c56551510e031002a124a83aea6e0", "DUNG: tai_dung_cham.py lech"
S1P = f"{{KIT}}/preds_s1_seed101.jsonl"
assert sum(1 for _ in open(S1P)) == 6958
for f in ("grpo_spice.py", "gen_test_grpo.py", "build_branch_data.py", "tai_dung_cham.py"):
    shutil.copyfile(f"{{KIT}}/{{f}}", f"{{W}}/{{f}}")
CK = {{}}
for r, d, h in LUOT:
    p = f"{{KIT}}/{{d}}"
    assert md5(f"{{p}}/adapter_model.safetensors") == h, f"DUNG: adapter {{r}} lech md5"
    assert json.load(open(f"{{p}}/adapter_config.json"))["base_model_name_or_path"].endswith("s1_merged"), f"DUNG: {{r}} khong gan tren S1 hoa"
    if os.path.exists(f"{{p}}/trainer_state.json"):
        assert json.load(open(f"{{p}}/trainer_state.json"))["global_step"] == 500, f"DUNG: {{r}} khong phai buoc 500"
    CK[r] = p
    print(r, "←", p, flush=True)
NGUON = sorted(glob.glob(f"{{KIT}}/raw_*.jsonl")); assert len(NGUON) == 8, NGUON
TA = None
for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True):
    root = os.path.dirname(t)
    if sum(1 for _ in open(t)) == 6958 and len(glob.glob(f"{{root}}/images/*.png")) >= 4463 and os.path.exists(f"{{root}}/ocr.jsonl"):
        TA = root
assert TA, "DUNG: khong thay test_ac du anh"
assert md5(f"{{TA}}/test.jsonl") == "da58299ee551a926a21cbecb5232bf78", "DUNG: test.jsonl lech"
PKG = os.path.dirname(os.path.dirname(os.path.dirname(TA)))
shutil.copytree(f"{{PKG}}/harness", f"{{W}}/thesis/harness", dirs_exist_ok=True, ignore=shutil.ignore_patterns("images"))
link = f"{{W}}/thesis/harness/dg1_cache/test_ac/images"
if os.path.lexists(link): os.remove(link)
os.symlink(f"{{TA}}/images", link)
WS = f"{{W}}/thesis"
assert os.path.exists(f"{{WS}}/harness/score_run.py")
IMG_NT = None
if NT:   # ảnh bước không chạm: thư mục đúng 2.495 ảnh ngoài thesis-score, hoặc bung tệp .tar
    import tarfile
    def tim_anh():
        for d in glob.glob("/kaggle/input/**/images", recursive=True) + glob.glob(f"{{W}}/nontap/**/images", recursive=True):
            if "thesis-score" not in d and len(glob.glob(f"{{d}}/ep*_s*.png")) == 2495:
                return d
    IMG_NT = tim_anh()
    if not IMG_NT:
        tars = glob.glob("/kaggle/input/**/*.tar", recursive=True); assert tars, "DUNG: khong thay anh khong cham"
        tarfile.open(tars[0]).extractall(f"{{W}}/nontap"); IMG_NT = tim_anh()
    assert IMG_NT, "DUNG: khong co thu muc dung 2.495 anh khong cham"
    print("IMG_NT", IMG_NT, flush=True)
# nối tiếp từ kernel trước (chỉ chế độ chạy thật)
if not MODE.endswith("smoke"):
    for r, _, _ in LUOT:
        for p in glob.glob(f"/kaggle/input/**/pred_{{r}}_test.jsonl", recursive=True) + glob.glob(f"/kaggle/input/**/score_{{r}}_test_raw.jsonl*", recursive=True):
            shutil.copyfile(p, f"{{W}}/{{os.path.basename(p)}}"); print("chep tiep", os.path.basename(p), sum(1 for _ in open(p)), "dong", flush=True)
print("KIT", KIT, "· TA", TA, "·", len(NGUON), "tep tho de dung lai", flush=True)
'''
C3 = '''MERGED = f"{W}/s1_merged"
ENV = {**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1", "PYTORCH_ALLOC_CONF": "expandable_segments:True"}
HET = threading.Event()
def chay(cmd, log, cwd, gpu):
    t0 = time.time()
    with open(log, "a") as f:
        q = subprocess.Popen(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT, env={**ENV, "CUDA_VISIBLE_DEVICES": str(gpu)})
        while q.poll() is None:
            time.sleep(30 if MODE == "smoke" else 120)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"{(time.time()-T_NB)/3600:5.2f} h · gpu{gpu} · {os.path.basename(log)} · {L[-1][:110] if L else 'chua co dong'}", flush=True)
            if time.time() - T_NB > CAT:
                print("⛔ het gio, dung de Output kip luu", flush=True); HET.set(); q.terminate(); q.wait(); return None
    print(f"--- {os.path.basename(log)} · ma thoat {q.returncode} · {(time.time()-t0)/3600:.2f} h", flush=True)
    if q.returncode != 0:
        print(open(log, errors="ignore").read()[-2500:], flush=True)
    return q.returncode
r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", KIT, "--merged", MERGED], cwd=W, capture_output=True, text=True, env=ENV)
print((r.stdout + r.stderr)[-800:], flush=True); assert r.returncode == 0, "DUNG: hoa loi"
TA_ARGS = ["--recs", f"{TA}/test.jsonl", "--ocr", f"{TA}/ocr.jsonl", "--images", f"{TA}/images", "--tap-only", "--no-q4"]
# kiểm bộ chấm (GPU 1) song song với kiểm hoà (GPU 0)
S1R = {(x["episode_id"], x["step_id"]): x for x in map(json.loads, open(f"{KIT}/raw_s1.jsonl"))}
ST = f"{W}/kiem_cham.json"; STR = ST.replace(".json", "_raw.jsonl")
if os.path.exists(STR): os.remove(STR)
KC = {}
def kiem_cham():
    KC["rc"] = chay(["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", S1P, "--out", ST, "--n", "10"], f"{W}/kiem_cham.log", WS, 1)
th = threading.Thread(target=kiem_cham)
if not NT: th.start()   # bước không chạm chấm bằng noharm, không dùng UGround
kh = f"{W}/kiem_hoa_test.jsonl"
if os.path.exists(kh): os.remove(kh)
assert chay(["python", "gen_test_grpo.py", "--bundle", KIT, "--merged", MERGED, "--s1", S1P, "--n", "20", "--out", kh] + TA_ARGS, f"{W}/kiem_hoa_test.log", W, 0) == 0, "DUNG: kiem hoa loi"
if not NT: th.join()
dong = [l for l in open(f"{W}/kiem_hoa_test.log") if "[kiểm hoà]" in l]; print(dong, flush=True)
assert dong and int(dong[-1].split("]")[1].split("/")[0]) >= 16, "DUNG: kiem hoa duoi 16/20"
if not NT:
    assert KC.get("rc") == 0, "DUNG: bo cham loi"
    X = [json.loads(l) for l in open(STR)]
    trung = sum(x.get("pred_xy") == S1R[(x["episode_id"], x["step_id"])].get("pred_xy") for x in X)
    print(f"[kiem bo cham] {trung}/{len(X)} buoc trung toa do tep tho S1", flush=True)
    assert len(X) >= 5 and trung >= len(X) - 1, "DUNG: bo cham khong tai lap ban cu"
'''
C4 = '''KQ = {}
Q = queue.Queue()
for r, _, _ in LUOT: Q.put(r)
def nhanh_nt(r, gpu):
    PRED, SC = f"{W}/pred_{r}_test_nontap.jsonl", f"{W}/noharm_{r}.json"
    nn = ["--n", str(N)] if N else []
    NT_ARGS = ["--recs", f"{TA}/test.jsonl", "--ocr", f"{TA}/ocr.jsonl", "--images", IMG_NT, "--non-tap", "--no-q4"]
    if chay(["python", "gen_test_grpo.py", "--bundle", KIT, "--merged", MERGED, "--ckpt", CK[r], "--out", PRED] + nn + NT_ARGS, f"{W}/gen_nt_{r}.log", W, gpu) != 0:
        KQ[r] = "gen dung"; return
    dongs = [l for l in open(f"{W}/gen_nt_{r}.log") if l.startswith("[điểm lưu]")]
    assert dongs and CK[r] in dongs[-1], f"{r}: khong gan dung diem luu {dongs[-1:]}"
    n = sum(1 for _ in open(PRED)); assert n == (N or 2495), f"{r}: {n} cau"
    rr = subprocess.run(["python", "-u", "harness/score_run.py", "--mode", "noharm", "--preds", PRED, "--baseline", S1P, "--out", SC], cwd=WS, capture_output=True, text=True, env={**ENV, "CUDA_VISIBLE_DEVICES": ""})
    print(r, rr.stdout[-2500:], rr.stderr[-800:], flush=True)
    open(f"{W}/noharm_{r}.log", "w").write(rr.stdout + rr.stderr)
    if not os.path.exists(SC):
        KQ[r] = "noharm loi"; return
    J = json.load(open(SC))
    KQ[r] = f"{J['n']} buoc khong cham · khop loai {J['action_match']:.4f} · delta {J.get('delta', float('nan')):+.4f}" + (" (SMOKE, khong dung so)" if N else "")
def nhanh(r, gpu):
    if NT: return nhanh_nt(r, gpu)
    PRED, SC = f"{W}/pred_{r}_test.jsonl", f"{W}/score_{r}_test.json"
    RAW = SC.replace(".json", "_raw.jsonl")
    nn = ["--n", str(N)] if N else []
    if chay(["python", "gen_test_grpo.py", "--bundle", KIT, "--merged", MERGED, "--ckpt", CK[r], "--out", PRED] + nn + TA_ARGS, f"{W}/gen_{r}.log", W, gpu) != 0:
        KQ[r] = "gen dung"; return
    dongs = [l for l in open(f"{W}/gen_{r}.log") if l.startswith("[điểm lưu]")]
    assert dongs and CK[r] in dongs[-1], f"{r}: khong gan dung diem luu {dongs[-1:]}"
    n = sum(1 for _ in open(PRED)); assert n == (N or 4463), f"{r}: {n} cau"
    rr = subprocess.run(["python", "tai_dung_cham.py", "gieo", "--preds", PRED, "--raw", RAW, "--nguon"] + NGUON, cwd=W, capture_output=True, text=True)
    print(r, rr.stdout[-400:], rr.stderr[-400:], flush=True); assert rr.returncode == 0, "gieo loi"
    if chay(["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", PRED, "--out", SC] + nn, f"{W}/cham_{r}.log", WS, gpu) != 0:
        KQ[r] = "cham dung"; return
    rr = subprocess.run(["python", "tai_dung_cham.py", "kiem", "--raw", RAW, "--nguon"] + NGUON, cwd=W, capture_output=True, text=True)
    print(r, rr.stdout[-400:], rr.stderr[-400:], flush=True); assert rr.returncode == 0, "bo cham khong tai lap"
    R = [json.loads(l) for l in open(RAW)]
    KQ[r] = f"{len(R)} buoc · exec {sum(int(x.get('executable', 0)) for x in R)}" + (" (SMOKE, khong dung so)" if N else "")
def tho(gpu):
    while not HET.is_set():
        try: r = Q.get_nowait()
        except queue.Empty: return
        try: nhanh(r, gpu)
        except Exception as e:
            KQ[r] = f"LOI {e}"; print("⚠️", r, e, flush=True)
TH = [threading.Thread(target=tho, args=(g,)) for g in (0, 1)]
for t in TH: t.start(); time.sleep(60)
for t in TH: t.join()
print("===== KET QUA", KQ, flush=True)
shutil.rmtree(MERGED, ignore_errors=True); shutil.rmtree(f"{W}/thesis", ignore_errors=True)
fs = [f for f in glob.glob(f"{W}/*") if os.path.isfile(f) and not f.endswith(".zip")]
with zipfile.ZipFile(f"{W}/ket_qua_test.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in fs: z.write(f, os.path.basename(f))
print("da zip", len(fs), "tep", flush=True)
xong = [r for r, v in KQ.items() if "exec" in v or "khop loai" in v]
print(f"xong {len(xong)}/{len(LUOT)} luot ·", "chua xong:", [r for r, _, _ in LUOT if r not in xong], flush=True)
assert not any(v.startswith("LOI") for v in KQ.values()), f"co luot loi {KQ}"
'''
cells = [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": c.splitlines(True)}
         for c in (C1, C2, C3, C4)]
nb = {"cells": cells, "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}},
      "nbformat": 4, "nbformat_minor": 5}
d = os.path.join(H, f"k_{name}")
os.makedirs(d, exist_ok=True)
json.dump(nb, open(os.path.join(d, f"{name}.ipynb"), "w"), ensure_ascii=False, indent=1)
meta = {"id": f"{user}/{name}", "title": name, "code_file": f"{name}.ipynb", "language": "python",
        "kernel_type": "notebook", "is_private": "true", "enable_gpu": "true", "enable_internet": "true",
        "dataset_sources": [f"{user}/thesis-score", KIT] + ([f"{user}/thesis-nontap-images"] if NT else []), "competition_sources": [], "kernel_sources": [PREV] if PREV else []}
json.dump(meta, open(os.path.join(d, "kernel-metadata.json"), "w"), indent=1)
print("đã dựng", d, "·", [x[0] for x in LUOT], "·", mode, "· trần", CAT_H, "h")
