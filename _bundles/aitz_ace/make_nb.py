# Dựng notebook aitz-ace-tran: (1) trần câu chuẩn AitZ qua UGround, (2) ACE/R3 trên AitZ (ra_k4 + luật R3 với ck500), (3) ra_k4 đứng một mình.
import json
C = []
C.append(r'''import subprocess, sys, os, time
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate bitsandbytes 'trl==0.29.1' 2>&1 | tail -3")
sh(f'{sys.executable} -m pip uninstall -y torchao 2>&1 | tail -1')
sh(f'{sys.executable} -c "import transformers, peft, torch; print(transformers.__version__, peft.__version__, torch.__version__, torch.cuda.device_count(), torch.cuda.get_device_name(0))"')''')
C.append(r'''import os, glob, json, shutil, hashlib, threading
W = "/kaggle/working"; TMP = "/kaggle/temp"; os.makedirs(TMP, exist_ok=True)
OUT = f"{W}/out"; os.makedirs(OUT, exist_ok=True)
T0 = time.time(); TOM = open(f"{OUT}/tom_tat.txt", "a")
def ghi(*a):
    s = f"[{(time.time()-T0)/3600:5.2f} h] " + " ".join(map(str, a)); print(s, flush=True); TOM.write(s + "\n"); TOM.flush()
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
import torch
assert torch.cuda.device_count() == 2, "DỪNG: cần 2 GPU (T4 x2)"
KIT = os.path.dirname(glob.glob("/kaggle/input/**/ra_gen.py", recursive=True)[0])
MD5 = {"grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf", "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912",
       "ra_gen.py": "d3969f6105b53b9eae81e7ce521cbb27", "ra_exemplars.py": "319857d87a6d5fdf8578886ffbb1ac0f",
       "luat_ghep_304.py": "4cb3af0bfd2894a5d09715d50b3d5d08"}
for f, h in MD5.items():
    shutil.copy(f"{KIT}/{f}", f"{W}/{f}"); assert md5(f"{W}/{f}") == h, f"DỪNG: {f} lệch"
os.makedirs(f"{W}/harness", exist_ok=True)
for f in glob.glob(f"{KIT}/harness/*.py"): shutil.copy(f, f"{W}/harness/")
AD = f"{KIT}/adapters"; RAK = f"{AD}/ra_k4"
assert md5(f"{AD}/adapter_s1_seed101/adapter_model.safetensors") == "0c60a4418d54eaf27bf1d27b895538b7"
assert md5(f"{RAK}/adapter_model.safetensors") == "f3c543b0047e1d8669b116ea5cb535c7"
KA = f"{KIT}/kiem_ac"
AZ = [os.path.dirname(t) for t in glob.glob("/kaggle/input/**/aitz_test/test.jsonl", recursive=True)]
assert len(AZ) == 1, f"DỪNG: cần đúng một aitz_test, thấy {AZ}"
AZ = AZ[0]
n_rec = sum(1 for _ in open(f"{AZ}/test.jsonl")); n_img = len(glob.glob(f"{AZ}/images/*.png"))
ghi("AitZ", AZ, "· bản ghi", n_rec, "· ảnh", n_img); assert n_rec == 4724 and n_img == 4724
assert sum(1 for _ in open(f"{KIT}/ex_aitz_k4.jsonl")) == 2736 and sum(1 for _ in open(f"{KIT}/pred_ck500_aitz.jsonl")) == 2736
MERGED = f"{TMP}/s1_merged"
def chay(ten, cmd, gpu, cwd=W):
    log = f"{OUT}/{ten}.log"; t = time.time()
    env = {**os.environ, "CUDA_VISIBLE_DEVICES": str(gpu), "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1"}
    with open(log, "a") as f:
        q = subprocess.Popen(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT, env=env, start_new_session=True)
        while q.poll() is None:
            time.sleep(120)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"  {(time.time()-T0)/3600:5.2f} h · GPU{gpu} · {ten} · {L[-1][:100] if L else ''}", flush=True)
            if time.time() - T0 > 11.0 * 3600: q.terminate(); ghi("chạm trần giờ —", ten); break
    ghi(ten, "GPU", gpu, "mã thoát", q.returncode, f"· {(time.time()-t)/3600:.2f} h")
    return q.returncode''')
C.append(r'''r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", AD, "--merged", MERGED], cwd=W, capture_output=True, text=True,
                   env={**os.environ, "CUDA_VISIBLE_DEVICES": "0"})
print((r.stdout + r.stderr)[-1200:]); assert r.returncode == 0, "DỪNG: hoà lỗi"
# kiểm: ra_k4 trên S1 hoà sinh lại 20 bước chạm AndroidControl, so câu ra_k4 của lượt test 304 (luật hoà cũ: >= 16/20)
kh = f"{OUT}/kiem_ra_ac.jsonl"
if os.path.exists(kh): os.remove(kh)
chay("kiem_ra_ac", ["python", "ra_gen.py", "--merged", MERGED, "--ckpt", RAK, "--recs", f"{KA}/test.jsonl", "--ocr", f"{KA}/ocr.jsonl",
     "--images", f"{KA}/images", "--ra", f"{KA}/ex_kiem_k4.jsonl", "--expect", "20", "--out", kh], 0)
P = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(kh))}
Q = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{KA}/pred_ra_k4_cu.jsonl"))}
x = sum(P[k] == Q[k] for k in Q); ghi(f"[kiểm ra_k4] {x}/20 trùng câu ra_k4 của lượt test 304")
assert x >= 16, f"DỪNG: kiểm ra_k4 {x}/20"''')
C.append(r'''import sys; sys.path.insert(0, W)
# câu chuẩn AitZ làm "dự đoán" ⇒ trần của dụng cụ trên AitZ (cùng cách đo trần 75,7 của AndroidControl)
TAPT = ("click", "long_press")
with open(f"{OUT}/pred_gold_aitz.jsonl", "w") as f:
    for r in map(json.loads, open(f"{AZ}/test.jsonl")):
        if r["action"].get("action_type") in TAPT and "x" in r["action"]:
            f.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "pred": r["gold_instruction"]}, ensure_ascii=False) + "\n")
assert sum(1 for _ in open(f"{OUT}/pred_gold_aitz.jsonl")) == 2736
def gen_ra(i):
    return ["python", "ra_gen.py", "--merged", MERGED, "--ckpt", RAK, "--recs", f"{AZ}/test.jsonl", "--ocr", f"{AZ}/ocr.jsonl",
            "--images", f"{AZ}/images", "--ra", f"{KIT}/ex_aitz_k4.jsonl", "--expect", "2736", "--shard", f"{i}/2",
            "--out", f"{OUT}/pred_ra_k4_aitz_{i}.jsonl"]
def score(nh):
    return ["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--data-root", AZ,
            "--preds", f"{OUT}/pred_{nh}_aitz.jsonl", "--out", f"{OUT}/score_{nh}_aitz.json"]
def ghep():
    import luat_ghep_304 as LG
    d = lambda p: {(x["episode_id"], x["step_id"]): x for x in map(json.loads, open(p))}
    ra = {**d(f"{OUT}/pred_ra_k4_aitz_0.jsonl"), **d(f"{OUT}/pred_ra_k4_aitz_1.jsonl")}
    ck = d(f"{KIT}/pred_ck500_aitz.jsonl"); ex = d(f"{KIT}/ex_aitz_k4.jsonl")
    assert set(ra) == set(ck) == set(ex) and len(ra) == 2736, (len(ra), len(ck), len(ex))
    lay = {k: LG.quyet(ra[k]["pred"], ck[k]["pred"], ex[k]["exemplars"])["R3"] for k in ck}
    with open(f"{OUT}/pred_ra_k4_aitz.jsonl", "w") as f, open(f"{OUT}/pred_r3_aitz.jsonl", "w") as g:
        for k in ck:
            f.write(json.dumps(ra[k], ensure_ascii=False) + "\n")
            g.write(json.dumps({"episode_id": k[0], "step_id": k[1], "pred": ra[k]["pred"] if lay[k] else ck[k]["pred"]}, ensure_ascii=False) + "\n")
    chep = sum(any(LG.RA.tok(e["sent"]) == LG.RA.tok(ra[k]["pred"]) for e in ex[k]["exemplars"]) for k in ck)
    ghi(f"[R3] ra_k4 chép ví dụ {chep}/2736 · R3 lấy câu ra_k4 {sum(lay.values())} · khác ck500 {sum(lay[k] and ra[k]['pred'] != ck[k]['pred'] for k in ck)}"
        f" · ra_k4 khác ck500 {sum(ra[k]['pred'] != ck[k]['pred'] for k in ck)}")
xong = {0: False, 1: False}
def tho(gpu):
    chay(f"gen_ra_k4_{gpu}", gen_ra(gpu), gpu); xong[gpu] = True
    if gpu == 0:
        chay("score_gold", score("gold"), 0)
        while not all(xong.values()): time.sleep(60)
        chay("score_ra_k4", score("ra_k4"), 0)
    else:
        while not all(xong.values()): time.sleep(60)
        ghep(); chay("score_r3", score("r3"), 1)
ts = [threading.Thread(target=tho, args=(g,)) for g in (0, 1)]
for t in ts: t.start()
for t in ts: t.join()
for nh in ("gold", "r3", "ra_k4"):
    p = f"{OUT}/score_{nh}_aitz_raw.jsonl"
    if os.path.exists(p):
        R = [json.loads(l) for l in open(p)]
        ghi(f"== {nh}: {len(R)} bước · exec {sum(int(r.get('executable', 0)) for r in R)} · {100*sum(int(r.get('executable', 0)) for r in R)/max(len(R),1):.2f}")''')
C.append(r'''sh(f"cd {W} && zip -qr aitz_ace_out.zip out && ls -la {W}")
ghi("KẾT THÚC")''')
nb = {"cells": [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": c} for c in C],
      "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}, "nbformat": 4, "nbformat_minor": 5}
json.dump(nb, open("/mnt/d/Master/Thesis/_bundles/aitz_ace/k/aitz-ace-tran.ipynb", "w"), ensure_ascii=False, indent=1)
print("ok")
