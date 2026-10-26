# Notebook acu-gen (trang2): sinh + chấm UGround trên 1.484 bước chạm AndroidControl S1 chưa thấy.
# Nhánh: trần câu chuẩn · S1 · ck500 · R3 (ACE = ra_k4 + luật R3 với ck500) · Base · ck500/202 (+ ra_k4 riêng nếu còn giờ).
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
G = os.path.dirname(glob.glob("/kaggle/input/**/gen_aitz.py", recursive=True)[0])      # aitz-gen-kit
A = os.path.dirname(glob.glob("/kaggle/input/**/ra_gen.py", recursive=True)[0])        # aitz-ace-kit
Z = os.path.dirname(glob.glob("/kaggle/input/**/only_tap_aitz.jsonl", recursive=True)[0])  # infer_branch cho Base
# ảnh: output của acu-build-cpu; OCR (rapidocr 1.4.4, máy nhà) + khối ví dụ: dataset acu-ocr144 — OCR 1.2.3 trên Kaggle lệch tập kiểm cũ (1/20 trùng)
SRC = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/acu_test/test.jsonl", recursive=True)]
assert len(SRC) == 1, SRC; SRC = SRC[0]
O144 = os.path.dirname(glob.glob("/kaggle/input/**/ocr_acu_144.jsonl", recursive=True)[0])
ACU = f"{W}/acu"; os.makedirs(ACU, exist_ok=True)
shutil.copy(f"{SRC}/test.jsonl", f"{ACU}/test.jsonl")
shutil.copy(f"{O144}/ocr_acu_144.jsonl", f"{ACU}/ocr.jsonl"); shutil.copy(f"{O144}/ex_acu_k4.jsonl", f"{ACU}/ex_acu_k4.jsonl")
if not os.path.exists(f"{ACU}/images"): os.symlink(f"{SRC}/images", f"{ACU}/images")
assert md5(f"{ACU}/ocr.jsonl") == "__MD5_OCR__" and md5(f"{ACU}/ex_acu_k4.jsonl") == "__MD5_EX__", "DỪNG: OCR/khối ví dụ lệch"
for f in ("grpo_spice.py", "build_branch_data.py", "gen_aitz.py"): shutil.copy(f"{G}/{f}", f"{W}/{f}")
for f in ("ra_gen.py", "ra_exemplars.py", "luat_ghep_304.py"): shutil.copy(f"{A}/{f}", f"{W}/{f}")
os.makedirs(f"{W}/harness", exist_ok=True)
for f in glob.glob(f"{G}/harness/*.py"): shutil.copy(f, f"{W}/harness/")
MD5 = {"grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf", "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912",
       "ra_gen.py": "d3969f6105b53b9eae81e7ce521cbb27", "ra_exemplars.py": "319857d87a6d5fdf8578886ffbb1ac0f",
       "luat_ghep_304.py": "4cb3af0bfd2894a5d09715d50b3d5d08"}
for f, h in MD5.items(): assert md5(f"{W}/{f}") == h, f"DỪNG: {f} lệch"
assert md5(f"{Z}/infer_branch.py") == "0eef768c215ce3c3c1fc379e5a46ec32"
AD = f"{G}/adapters"; RAK = f"{A}/adapters/ra_k4"
CK = {"ck500": f"{AD}/ck500", "ck500_s202": f"{AD}/ck500_s202"}
assert md5(f"{AD}/adapter_s1_seed101/adapter_model.safetensors") == "0c60a4418d54eaf27bf1d27b895538b7"
assert md5(f"{CK['ck500']}/adapter_model.safetensors") == "491fa6677340393f1e4464c08a0cec98"
assert md5(f"{CK['ck500_s202']}/adapter_model.safetensors") == "57e5d2eec23278b0a2dfe7393d9fc463"
assert md5(f"{RAK}/adapter_model.safetensors") == "f3c543b0047e1d8669b116ea5cb535c7"
R = [json.loads(l) for l in open(f"{ACU}/test.jsonl")]
TAPT = ("click", "long_press")
TAP = [r for r in R if r["action"].get("action_type") in TAPT and "x" in r["action"]]
n_ocr = sum(1 for _ in open(f"{ACU}/ocr.jsonl")); n_ex = sum(1 for _ in open(f"{ACU}/ex_acu_k4.jsonl"))
n_img = sum(os.path.exists(f"{ACU}/{r['image']}") for r in TAP)
ghi("ACU", ACU, "· bản ghi", len(R), "· chạm", len(TAP), "· ảnh", n_img, "· OCR", n_ocr, "· khối ví dụ", n_ex)
assert len(R) == 3103 and len(TAP) == 1484 and n_img == 1484 and n_ocr == 1484 and n_ex == 1484
with open(f"{OUT}/only_tap_acu.jsonl", "w") as f:
    for r in TAP: f.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"]}) + "\n")
with open(f"{OUT}/pred_gold_acu.jsonl", "w") as f:
    for r in TAP: f.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "pred": r["gold_instruction"]}, ensure_ascii=False) + "\n")
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
            if time.time() - T0 > 11.2 * 3600: q.terminate(); ghi("chạm trần giờ —", ten); break
    ghi(ten, "GPU", gpu, "mã thoát", q.returncode, f"· {(time.time()-t)/3600:.2f} h")
    return q.returncode''')
C.append(r'''r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", AD, "--merged", MERGED], cwd=W, capture_output=True, text=True,
                   env={**os.environ, "CUDA_VISIBLE_DEVICES": "0"})
print((r.stdout + r.stderr)[-1200:]); assert r.returncode == 0, "DỪNG: hoà lỗi"
# hai phép kiểm trên 20 bước chạm AndroidControl (luật cũ >= 16/20): S1 hoà so preds_s1_seed101; ra_k4 so câu ra_k4 của lượt test 304
KG, KA = f"{G}/kiem_ac", f"{A}/kiem_ac"
for p in (f"{OUT}/kiem_hoa_ac.jsonl", f"{OUT}/kiem_ra_ac.jsonl"):
    if os.path.exists(p): os.remove(p)
th = [threading.Thread(target=chay, args=a) for a in (
    ("kiem_hoa_ac", ["python", "gen_aitz.py", "--bundle", AD, "--merged", MERGED, "--s1", f"{KG}/preds_s1_seed101.jsonl", "--recs", f"{KG}/test.jsonl",
      "--ocr", f"{KG}/ocr.jsonl", "--images", f"{KG}/images", "--tap-only", "--no-q4", "--expect-rows", "20", "--expect-taps", "20", "--out", f"{OUT}/kiem_hoa_ac.jsonl"], 0),
    ("kiem_ra_ac", ["python", "ra_gen.py", "--merged", MERGED, "--ckpt", RAK, "--recs", f"{KA}/test.jsonl", "--ocr", f"{KA}/ocr.jsonl",
      "--images", f"{KA}/images", "--ra", f"{KA}/ex_kiem_k4.jsonl", "--expect", "20", "--out", f"{OUT}/kiem_ra_ac.jsonl"], 1))]
for t in th: t.start()
for t in th: t.join()
d = [l for l in open(f"{OUT}/kiem_hoa_ac.log") if "[kiểm hoà]" in l]; ghi(d)
x = int(d[-1].split("]")[1].split("/")[0]); assert x >= 16, f"DỪNG: kiểm hoà {x}/20"
P = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{OUT}/kiem_ra_ac.jsonl"))}
Q = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{KA}/pred_ra_k4_cu.jsonl"))}
y = sum(P[k] == Q[k] for k in Q); ghi(f"[kiểm ra_k4] {y}/20"); assert y >= 16, f"DỪNG: kiểm ra_k4 {y}/20"''')
C.append(r'''import sys; sys.path.insert(0, W)
ARGS = ["--recs", f"{ACU}/test.jsonl", "--ocr", f"{ACU}/ocr.jsonl", "--images", f"{ACU}/images"]
def gen(nh):
    o = f"{OUT}/pred_{nh}_acu.jsonl"
    if nh == "base":
        return ["python", f"{Z}/infer_branch.py", "--no-adapter", "--data-root", ACU, "--recs-file", "test.jsonl",
                "--only", f"{OUT}/only_tap_acu.jsonl", "--batch", "4", "--out", o]
    if nh == "ra_k4":
        return ["python", "ra_gen.py", "--merged", MERGED, "--ckpt", RAK, *ARGS, "--ra", f"{ACU}/ex_acu_k4.jsonl", "--expect", "1484", "--out", o]
    ck = ["--ckpt", CK[nh]] if nh in CK else []
    return ["python", "gen_aitz.py", "--bundle", AD, "--merged", MERGED, *ck, *ARGS, "--tap-only", "--no-q4",
            "--expect-rows", "3103", "--expect-taps", "1484", "--out", o]
def score(nh):
    return ["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--data-root", ACU,
            "--preds", f"{OUT}/pred_{nh}_acu.jsonl", "--out", f"{OUT}/score_{nh}_acu.json"]
def ghep_r3():
    import luat_ghep_304 as LG
    d = lambda p: {(x["episode_id"], x["step_id"]): x for x in map(json.loads, open(p))}
    ra, ck, ex = d(f"{OUT}/pred_ra_k4_acu.jsonl"), d(f"{OUT}/pred_ck500_acu.jsonl"), d(f"{ACU}/ex_acu_k4.jsonl")
    assert set(ra) == set(ck) == set(ex) and len(ra) == 1484
    lay = {k: LG.quyet(ra[k]["pred"], ck[k]["pred"], ex[k]["exemplars"])["R3"] for k in ck}
    with open(f"{OUT}/pred_r3_acu.jsonl", "w") as g:
        for k in ck: g.write(json.dumps({"episode_id": k[0], "step_id": k[1], "pred": ra[k]["pred"] if lay[k] else ck[k]["pred"]}, ensure_ascii=False) + "\n")
    ghi(f"[R3] lấy câu ra_k4 {sum(lay.values())} · khác ck500 {sum(lay[k] and ra[k]['pred'] != ck[k]['pred'] for k in ck)}")
def du(nh):
    p = f"{OUT}/pred_{nh}_acu.jsonl"; return os.path.exists(p) and sum(1 for _ in open(p)) == 1484
CAN = {"gold": [], "s1": ["s1"], "ck500": ["ck500"], "r3": ["ra_k4", "ck500"], "base": ["base"], "ck500_s202": ["ck500_s202"], "ra_k4": ["ra_k4"]}
viec = [("gen", n) for n in ("s1", "ck500", "ra_k4", "base", "ck500_s202")] + \
       [("score", n) for n in ("gold", "s1", "ck500", "r3", "base", "ck500_s202", "ra_k4")]
khoa = threading.Lock(); xong = set()
def tho(gpu):
    while True:
        with khoa:
            if not viec: return
            san = [v for v in viec if v[0] == "gen" or all(("gen", n) in xong for n in CAN[v[1]])]
            v = san[0] if san else None
            if v: viec.remove(v)
        if v is None: time.sleep(60); continue
        if time.time() - T0 > 10.5 * 3600: ghi("bỏ", v, "vì gần trần giờ"); continue
        if v == ("score", "r3"): ghep_r3()
        chay(f"{v[0]}_{v[1]}", gen(v[1]) if v[0] == "gen" else score(v[1]), gpu)
        if v[0] == "gen":
            ghi(v[1], "đủ câu" if du(v[1]) else "THIẾU CÂU")
            with khoa: xong.add(v)
ts = [threading.Thread(target=tho, args=(g,)) for g in (0, 1)]
for t in ts: t.start()
for t in ts: t.join()
for nh in CAN:
    p = f"{OUT}/score_{nh}_acu_raw.jsonl"
    if os.path.exists(p):
        Rr = [json.loads(l) for l in open(p)]
        ghi(f"== {nh}: {len(Rr)} bước · exec {sum(int(r.get('executable', 0)) for r in Rr)} · {100*sum(int(r.get('executable', 0)) for r in Rr)/max(len(Rr),1):.2f}")''')
C.append(r'''sh(f"cd {W} && zip -qr acu_gen_out.zip out && ls -la {W}")
ghi("KẾT THÚC")''')
nb = {"cells": [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": c} for c in C],
      "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}, "nbformat": 4, "nbformat_minor": 5}
json.dump(nb, open("/mnt/d/Master/Thesis/_bundles/acu_gen/k/acu-gen.ipynb", "w"), ensure_ascii=False, indent=1)
print("ok")
