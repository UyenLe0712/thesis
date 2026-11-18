# BẢN SPICE-MATCH ck400 (16/11): sinh từ make_k.py, chỉ đổi adapter (ad/match_ck400), tên kernel, md5.
# -*- coding: utf-8 -*-
"""SA-SPICE-v3 ck400 — chấm TẬP KIỂM (4.463 bước chạm + 2.495 bước không chạm), Kaggle T4×2, tài khoản trang (15/11/2026).

Chọn ck400 theo DEV-v3 (report/333 §12–13). Không dựng dataset mới: dùng lại
  · trangphngngc/sa3-dev-v3   : adapter_s1_seed101, sft_final, ad/match_ck400, sa3_grpo.py, grpo_spice.py (bản harness), mau_0 + train_v3 (kiểm hoà)
  · trangphngngc/sft-colab-kit: gen_test_grpo.py, tai_dung_cham.py, preds_s1_seed101.jsonl, raw_*.jsonl (dùng lại chấm câu trùng)
  · trangphngngc/thesis-score : test_ac (test.jsonl, ocr, 4.463 ảnh chạm) + harness/score_run.py
  · trangphngngc/thesis-nontap-images: 2.495 ảnh bước không chạm
Đường mô hình = đường DEV-v3: hoà S1 → hoà SFT-cont (sft_cont_merged, kiểm 3/3 greedy) → gắn adapter GRPO.
Kiểm thêm: sft_cont_merged không adapter, 20 bước chạm đầu, phải trùng ≥16/20 câu SFT tiếp đã chấm test (luoi-test-u-3, exec 60,16);
bộ chấm 10 bước S1 trùng toạ độ cũ; câu SA phải khác câu SFT-cont ở ≥3% bước (adapter thật sự gắn).
GPU0: SA ck400 chạm (sinh → gieo → UGround → kiểm 40 bước). GPU1: SA ck400 không chạm → SFT-cont không chạm (noharm, CPU).

  python3 _bundles/sa3_test/make_k.py            # dựng _bundles/sa3_test/k_sa3-test-ck400/
  kg trang kernels push -p _bundles/sa3_test/k_sa3-test-ck400 --accelerator NvidiaTeslaT4
"""
import json, os, hashlib

USER, NAME = "trangphngngc", "sa3-test-match"
CAT_H = float(os.environ.get("CAT_H", 11.0))
H = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(os.path.dirname(H))
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()

MD5_SA = md5(f"{R}/_bundles/sa3_grpo/ck_match/checkpoint-400/adapter_model.safetensors")
assert MD5_SA == "e7ab0390d7a4270a9aca0463f13d11ee", MD5_SA   # SPICE-MATCH ck400 (Colab L4 16/11)
MD5_SA3 = {f: md5(f"{R}/_bundles/sa3_dev/ds/{f}") for f in ("sa3_grpo.py", "grpo_spice.py", "build_branch_data.py", "grpo_luoi.py",
                                                           "sa3_reward_screen.py", "sa3_action_verify.py", "h4_spice_tuple_7_11.py")}
for f in MD5_SA3:
    assert MD5_SA3[f] == md5(f"{R}/harness/{f}"), f"{f} trong sa3-dev-v3 lệch harness"
# 20 câu SFT tiếp (test, 20 bước chạm đầu theo thứ tự test.jsonl) để kiểm sft_cont_merged
SFTP = f"{R}/runs/luoi/7_11/test_u_3/pred_sft_tiep_101_test.jsonl"
assert sum(1 for _ in open(SFTP)) == 4463
TAPT = ("click", "long_press")
test = [json.loads(l) for l in open(f"{R}/harness/dg1_cache/test_ac/test.jsonl", encoding="utf-8")]
tap20 = [(r["episode_id"], r["step_id"]) for r in test if r["action"].get("action_type") in TAPT and "x" in r["action"]][:20]
SP = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(SFTP, encoding="utf-8"))}
SFT20 = [{"episode_id": k[0], "step_id": k[1], "pred": SP[k]} for k in tap20]

C1 = '''import subprocess, sys, os, time, threading, glob, json, shutil, hashlib, zipfile
T_NB = time.time()
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh(f"{sys.executable} -m pip install -q 'transformers==5.20.2' 'peft==0.21.2' 'trl==0.29.1' accelerate bitsandbytes pycocoevalcap sacrebleu 2>&1 | tail -3")
sh(f"{sys.executable} -m pip uninstall -y torchao 2>&1 | tail -1")
assert sh(f\'\'\'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.device_count()); assert (trl.__version__, transformers.__version__, peft.__version__) == ('0.29.1', '5.20.2', '0.21.2'); assert torch.cuda.device_count() == 2" \'\'\') == 0, "DUNG: moi truong"
print("✅ moi truong", flush=True)
'''
C2 = f'''W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
CAT = 3600 * {CAT_H}
# --- sa3-dev-v3: đường hoà SFT-cont ---
D = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/sa3_grpo.py", recursive=True) if "/notebooks/" not in p and os.path.isdir(os.path.join(os.path.dirname(p), "ad"))]
assert len(D) == 1, D; D = D[0]
for f, h in {MD5_SA3!r}.items():
    assert md5(f"{{D}}/{{f}}") == h, f"DUNG: {{f}} lech"
SA = f"{{D}}/ad/match_ck400"
assert md5(f"{{SA}}/adapter_model.safetensors") == "{MD5_SA}", "DUNG: adapter SA ck400 lech md5"
assert json.load(open(f"{{SA}}/adapter_config.json"))["base_model_name_or_path"].endswith("sft_cont_merged")
assert md5(f"{{D}}/sft_final/adapter_model.safetensors") == "113e2a3e6a0781fd5121acda99962d1b", "DUNG: sft_final lech"
W3 = f"{{W}}/sa3"; os.makedirs(W3, exist_ok=True)
for f in {tuple(MD5_SA3)!r}:
    shutil.copyfile(f"{{D}}/{{f}}", f"{{W3}}/{{f}}")
# --- kit chấm test (giống luoi-test) ---
KIT = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/gen_test_grpo.py", recursive=True)
       if "/notebooks/" not in p and os.path.isdir(os.path.join(os.path.dirname(p), "adapter_s1_seed101"))]
KIT = [k for k in KIT if os.path.exists(f"{{k}}/tai_dung_cham.py")]
assert len(KIT) == 1, KIT; KIT = KIT[0]
assert md5(f"{{KIT}}/grpo_spice.py") == "07ea87b6d156d1faa391a4274dffd7cf"
assert md5(f"{{KIT}}/gen_test_grpo.py") == "b18ec1aa3fd037ddffb9411db63c2a3f"
assert md5(f"{{KIT}}/tai_dung_cham.py") == "574c56551510e031002a124a83aea6e0"
for f in ("grpo_spice.py", "gen_test_grpo.py", "build_branch_data.py", "tai_dung_cham.py"):
    shutil.copyfile(f"{{KIT}}/{{f}}", f"{{W}}/{{f}}")
S1P = f"{{KIT}}/preds_s1_seed101.jsonl"; assert sum(1 for _ in open(S1P)) == 6958
NGUON = sorted(glob.glob(f"{{KIT}}/raw_*.jsonl")); assert len(NGUON) == 8, NGUON
TA = None
for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True):
    root = os.path.dirname(t)
    if sum(1 for _ in open(t)) == 6958 and len(glob.glob(f"{{root}}/images/*.png")) >= 4463 and os.path.exists(f"{{root}}/ocr.jsonl"):
        TA = root
assert TA and md5(f"{{TA}}/test.jsonl") == "da58299ee551a926a21cbecb5232bf78", "DUNG: test.jsonl"
PKG = os.path.dirname(os.path.dirname(os.path.dirname(TA)))
shutil.copytree(f"{{PKG}}/harness", f"{{W}}/thesis/harness", dirs_exist_ok=True, ignore=shutil.ignore_patterns("images"))
link = f"{{W}}/thesis/harness/dg1_cache/test_ac/images"
if os.path.lexists(link): os.remove(link)
os.symlink(f"{{TA}}/images", link)
WS = f"{{W}}/thesis"
IMG_NT = None
for d in glob.glob("/kaggle/input/**/images", recursive=True):
    if "thesis-score" not in d and "sa3" not in d and len(glob.glob(f"{{d}}/ep*_s*.png")) == 2495:
        IMG_NT = d
assert IMG_NT, "DUNG: khong co thu muc 2.495 anh khong cham"
SFT20 = f"{{W}}/sft_tiep_20.jsonl"
open(SFT20, "w").write({"".join(json.dumps(x, ensure_ascii=False) + chr(10) for x in SFT20)!r})
print("D", D, "· KIT", KIT, "· TA", TA, "· IMG_NT", IMG_NT, flush=True)
'''
C3 = '''ENV = {**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1",
       "PYTORCH_ALLOC_CONF": "expandable_segments:True", "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
HET = threading.Event()
def chay(cmd, log, cwd, gpu):
    t0 = time.time()
    with open(log, "a") as f:
        q = subprocess.Popen(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT, env={**ENV, "CUDA_VISIBLE_DEVICES": str(gpu)}, start_new_session=True)
        while q.poll() is None:
            time.sleep(120)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"{(time.time()-T_NB)/3600:5.2f} h · gpu{gpu} · {os.path.basename(log)} · {L[-1][:110] if L else 'chua co dong'}", flush=True)
            if time.time() - T_NB > CAT:
                print("⛔ het gio", flush=True); HET.set(); q.terminate(); q.wait(); return None
    print(f"--- {os.path.basename(log)} · ma thoat {q.returncode} · {(time.time()-t0)/3600:.2f} h", flush=True)
    if q.returncode != 0:
        print(open(log, errors="ignore").read()[-2500:], flush=True)
    return q.returncode
S1M, SFTM = "/tmp/s1_merged", "/tmp/sft_cont_merged"
assert chay(["python", "grpo_spice.py", "--merge", "--bundle", D, "--adapter", f"{D}/adapter_s1_seed101", "--merged", S1M], f"{W}/hoa.log", W3, 0) == 0, "DUNG: hoa S1"
assert chay(["python", "sa3_grpo.py", "--hoa", "--data", D, "--merged-s1", S1M, "--merged", SFTM], f"{W}/hoa.log", W3, 0) == 0, "DUNG: hoa SFT-cont"
shutil.rmtree(S1M, ignore_errors=True)
assert chay(["python", "sa3_grpo.py", "--kiem-hoa", "--data", D, "--merged", SFTM], f"{W}/hoa.log", W3, 0) == 0, "DUNG: kiem hoa 3/3"
print([l for l in open(f"{W}/hoa.log") if "kiểm hoà] greedy" in l], flush=True)
TA_ARGS = ["--recs", f"{TA}/test.jsonl", "--ocr", f"{TA}/ocr.jsonl", "--images", f"{TA}/images", "--tap-only", "--no-q4"]
# kiểm bộ chấm (GPU1) song song kiểm SFT-cont trên test (GPU0)
S1R = {(x["episode_id"], x["step_id"]): x for x in map(json.loads, open(f"{KIT}/raw_s1.jsonl"))}
ST = f"{W}/kiem_cham.json"; STR = ST.replace(".json", "_raw.jsonl")
KC = {}
def kiem_cham():
    KC["rc"] = chay(["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", S1P, "--out", ST, "--n", "10"], f"{W}/kiem_cham.log", WS, 1)
th = threading.Thread(target=kiem_cham); th.start()
kh = f"{W}/kiem_sftcont_test.jsonl"
assert chay(["python", "gen_test_grpo.py", "--bundle", KIT, "--merged", SFTM, "--s1", SFT20, "--n", "20", "--out", kh] + TA_ARGS, f"{W}/kiem_sftcont_test.log", W, 0) == 0
th.join()
dong = [l for l in open(f"{W}/kiem_sftcont_test.log") if "[kiểm hoà]" in l]; print(dong, flush=True)
assert dong and int(dong[-1].split("]")[1].split("/")[0]) >= 16, "DUNG: sft_cont_merged lech SFT tiep da cham (duoi 16/20)"
assert KC.get("rc") == 0, "DUNG: bo cham loi"
X = [json.loads(l) for l in open(STR)]
trung = sum(x.get("pred_xy") == S1R[(x["episode_id"], x["step_id"])].get("pred_xy") for x in X)
print(f"[kiem bo cham] {trung}/{len(X)} buoc trung toa do tep tho S1", flush=True)
assert len(X) >= 5 and trung >= len(X) - 1, "DUNG: bo cham khong tai lap"
print("✅ hoa + kiem SFT-cont tren test + bo cham", flush=True)
'''
C4 = '''KQ = {}
def tap_sa(gpu=0):
    PRED, SC = f"{W}/pred_match_ck400_test.jsonl", f"{W}/score_match_ck400_test.json"
    RAW = SC.replace(".json", "_raw.jsonl")
    if chay(["python", "gen_test_grpo.py", "--bundle", KIT, "--merged", SFTM, "--ckpt", SA, "--s1", SFT20, "--out", PRED] + TA_ARGS, f"{W}/gen_match_ck400.log", W, gpu) != 0:
        KQ["tap"] = "gen dung"; return
    assert any(l.startswith("[điểm lưu]") and SA in l for l in open(f"{W}/gen_match_ck400.log")), "khong gan adapter"
    n = sum(1 for _ in open(PRED)); assert n == 4463, n
    rr = subprocess.run(["python", "tai_dung_cham.py", "gieo", "--preds", PRED, "--raw", RAW, "--nguon"] + NGUON, cwd=W, capture_output=True, text=True)
    print(rr.stdout[-400:], rr.stderr[-400:], flush=True); assert rr.returncode == 0, "gieo loi"
    if chay(["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", PRED, "--out", SC], f"{W}/cham_match_ck400.log", WS, gpu) != 0:
        KQ["tap"] = "cham dung"; return
    rr = subprocess.run(["python", "tai_dung_cham.py", "kiem", "--raw", RAW, "--nguon"] + NGUON, cwd=W, capture_output=True, text=True)
    print(rr.stdout[-400:], rr.stderr[-400:], flush=True); assert rr.returncode == 0, "bo cham khong tai lap"
    Rr = [json.loads(l) for l in open(RAW)]
    KQ["tap"] = f"{len(Rr)} buoc · exec {sum(int(x.get('executable', 0)) for x in Rr)}"
def nontap(ten, ck, gpu=1):
    PRED, SC = f"{W}/pred_{ten}_test_nontap.jsonl", f"{W}/noharm_{ten}.json"
    NT_ARGS = ["--recs", f"{TA}/test.jsonl", "--ocr", f"{TA}/ocr.jsonl", "--images", IMG_NT, "--non-tap", "--no-q4"]
    if chay(["python", "gen_test_grpo.py", "--bundle", KIT, "--merged", SFTM, "--out", PRED] + (["--ckpt", ck] if ck else []) + NT_ARGS, f"{W}/gen_nt_{ten}.log", W, gpu) != 0:
        KQ[ten] = "gen dung"; return
    n = sum(1 for _ in open(PRED)); assert n == 2495, n
    rr = subprocess.run(["python", "-u", "harness/score_run.py", "--mode", "noharm", "--preds", PRED, "--baseline", S1P, "--out", SC], cwd=WS, capture_output=True, text=True, env={**ENV, "CUDA_VISIBLE_DEVICES": ""})
    open(f"{W}/noharm_{ten}.log", "w").write(rr.stdout + rr.stderr); print(ten, rr.stdout[-1500:], rr.stderr[-500:], flush=True)
    J = json.load(open(SC)) if os.path.exists(SC) else {}
    KQ[ten] = f"{J.get('n')} buoc khong cham · khop loai {J.get('action_match')}"
def an(f, *a):
    try: f(*a)
    except Exception as e:
        KQ[f"{f.__name__}{a}"] = f"LOI {e}"; print("⚠️", f.__name__, a, e, flush=True)
def gpu1():
    an(nontap, "match_ck400", SA)
    if not HET.is_set(): an(nontap, "sftcont", None)
TH = [threading.Thread(target=an, args=(tap_sa,)), threading.Thread(target=gpu1)]
for t in TH: t.start(); time.sleep(60)
for t in TH: t.join()
# adapter thật sự gắn: câu SA khác câu SFT-cont ở ≥3% bước không chạm
try:
    A_ = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{W}/pred_match_ck400_test_nontap.jsonl"))}
    B_ = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{W}/pred_sftcont_test_nontap.jsonl"))}
    k_ = [k for k in A_ if k in B_]; khac = sum(A_[k] != B_[k] for k in k_)
    print(f"[adapter gan that] cau SA khac SFT-cont {khac}/{len(k_)}", flush=True); KQ["khac_sftcont_nontap"] = f"{khac}/{len(k_)}"
except Exception as e:
    print("khong so duoc SA/SFT-cont", e, flush=True)
dong = [l for l in open(f"{W}/gen_match_ck400.log") if "[kiểm hoà]" in l] if os.path.exists(f"{W}/gen_match_ck400.log") else []
print("SA ck400 trung SFT tiep tren 20 buoc dau:", dong[-1:], flush=True)
print("===== KET QUA", KQ, flush=True)
shutil.rmtree(SFTM, ignore_errors=True); shutil.rmtree(f"{W}/thesis", ignore_errors=True); shutil.rmtree(W3, ignore_errors=True)
fs = [f for f in glob.glob(f"{W}/*") if os.path.isfile(f) and not f.endswith(".zip")]
with zipfile.ZipFile(f"{W}/sa3_test_out.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in fs: z.write(f, os.path.basename(f))
print("da zip", len(fs), "tep", flush=True)
assert not any(str(v).startswith("LOI") for v in KQ.values()), f"co nhanh loi {KQ}"
'''
cells = [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": c.splitlines(True)} for c in (C1, C2, C3, C4)]
nb = {"cells": cells, "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}, "nbformat": 4, "nbformat_minor": 5}
d = os.path.join(H, f"k_{NAME}"); os.makedirs(d, exist_ok=True)
json.dump(nb, open(os.path.join(d, f"{NAME}.ipynb"), "w"), ensure_ascii=False, indent=1)
json.dump({"id": f"{USER}/{NAME}", "title": NAME, "code_file": f"{NAME}.ipynb", "language": "python", "kernel_type": "notebook",
           "is_private": "true", "enable_gpu": "true", "enable_internet": "true",
           "dataset_sources": [f"{USER}/sa3-dev-v3", f"{USER}/sft-colab-kit", f"{USER}/thesis-score", f"{USER}/thesis-nontap-images"],
           "competition_sources": [], "kernel_sources": []}, open(os.path.join(d, "kernel-metadata.json"), "w"), indent=1)
print("dựng", d)
