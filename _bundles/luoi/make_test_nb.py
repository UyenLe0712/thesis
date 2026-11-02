"""Notebook sinh câu test cho hai lượt của lưới, mỗi GPU một lượt (điểm lưu 500 lấy từ output kernel train).

python make_test_nb.py <user> <tên kernel> <kernel train> <thư mục lượt 0> <thư mục lượt 1> <trần giờ>
Ô cài đặt chép nguyên từ notebook train (cùng phiên bản thư viện). Ví dụ:
  python make_test_nb.py trangphngngc luoi-gen-t trangphngngc/luoi-t-2 grpo_meteor_101 grpo_rougel_101 4.8
"""
import json, os, sys
user, name, prev, r0, r1, cap = sys.argv[1:7]
H = os.path.dirname(os.path.abspath(__file__))
C0 = "".join(json.load(open(f"{H}/k_luoi-u-2/luoi-u-2.ipynb"))["cells"][0]["source"])
C1 = f'''import os, glob, json, shutil, hashlib, subprocess, time
W = "/kaggle/working"; T0 = time.time(); RUNS = {[r0, r1]!r}; CAP = {float(cap)!r} * 3600
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
SRC = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/gen_test_grpo.py", recursive=True)
       if all(os.path.exists(os.path.join(os.path.dirname(p), f)) for f in ("grpo_spice.py", "build_branch_data.py", "preds_s1_seed101.jsonl"))]
assert len(SRC) == 1, f"DUNG: can dung mot grpo-spice-script, thay {{SRC}}"
SRC = SRC[0]
for f in ("grpo_spice.py", "build_branch_data.py", "gen_test_grpo.py"):
    shutil.copy(f"{{SRC}}/{{f}}", f"{{W}}/{{f}}")
assert md5(f"{{W}}/grpo_spice.py") == "07ea87b6d156d1faa391a4274dffd7cf", "DUNG: grpo_spice.py khac ban da sinh cau ck500"
assert md5(f"{{W}}/gen_test_grpo.py") == "b18ec1aa3fd037ddffb9411db63c2a3f", "DUNG: gen_test_grpo.py lech"
S1P = f"{{SRC}}/preds_s1_seed101.jsonl"
BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d)
MERGED = f"{{W}}/s1_merged"
CK = {{}}
for r in RUNS:
    c = glob.glob(f"/kaggle/input/**/{{r}}/checkpoint-500/adapter_model.safetensors", recursive=True)
    assert len(c) == 1, f"DUNG: {{r}} can dung mot checkpoint-500, thay {{c}}"
    CK[r] = os.path.dirname(c[0])
    assert json.load(open(f"{{CK[r]}}/trainer_state.json"))["global_step"] == 500, f"DUNG: {{r}} chua du 500 buoc"
    print(r, CK[r], "md5 adapter", md5(c[0]), flush=True)
TA = None
for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True):
    root = os.path.dirname(t)
    if sum(1 for _ in open(t)) == 6958 and len(glob.glob(f"{{root}}/images/*.png")) >= 4463 and os.path.exists(f"{{root}}/ocr.jsonl"):
        TA = root
assert TA and md5(f"{{TA}}/test.jsonl") == "da58299ee551a926a21cbecb5232bf78", f"DUNG: test_ac sai: {{TA}}"
ARGS = ["--recs", f"{{TA}}/test.jsonl", "--ocr", f"{{TA}}/ocr.jsonl", "--images", f"{{TA}}/images", "--tap-only", "--no-q4"]
ENV = lambda g: {{**os.environ, "CUDA_VISIBLE_DEVICES": str(g), "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1"}}
r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED], cwd=W, capture_output=True, text=True, env=ENV(0))
print((r.stdout + r.stderr)[-1200:], flush=True); assert r.returncode == 0, "DUNG: hoa loi"
'''
C2 = '''r = subprocess.run(["python", "gen_test_grpo.py", "--bundle", BUNDLE, "--merged", MERGED, "--s1", S1P, "--n", "20", "--out", f"{W}/kiem_hoa.jsonl"] + ARGS,
                   cwd=W, capture_output=True, text=True, env=ENV(0))
open(f"{W}/kiem_hoa.log", "w").write(r.stdout + r.stderr)
d = [l for l in (r.stdout + r.stderr).splitlines() if "[kiểm hoà]" in l]
print(d or (r.stdout + r.stderr)[-1500:], flush=True)
x = int(d[-1].split("]")[1].split("/")[0]); assert x >= 16, f"DUNG: kiem hoa {x}/20"
'''
C3 = '''P = []
for g, r in enumerate(RUNS):
    f = open(f"{W}/gen_{r}.log", "a")
    P.append((r, subprocess.Popen(["python", "gen_test_grpo.py", "--bundle", BUNDLE, "--merged", MERGED, "--ckpt", CK[r], "--out", f"{W}/pred_{r}_test.jsonl"] + ARGS,
                                  cwd=W, stdout=f, stderr=subprocess.STDOUT, env=ENV(g))))
def dem(r):
    p = f"{W}/pred_{r}_test.jsonl"
    return sum(1 for _ in open(p)) if os.path.exists(p) else 0
while any(p.poll() is None for _, p in P):
    time.sleep(120)
    print(f"{(time.time()-T0)/3600:5.2f} h · " + " · ".join(f"{r} {dem(r)}/4463" for r, _ in P), flush=True)
    for r, p in P:
        L = [l.strip() for l in open(f"{W}/gen_{r}.log", errors="ignore") if l.strip()]
        print("   ", r, L[-1][:120] if L else "chua co dong nao", flush=True)
    if time.time() - T0 > CAP:
        print("het tran gio, dung de Output kip luu", flush=True)
        for _, p in P:
            if p.poll() is None: p.terminate()
        for _, p in P: p.wait()
for r, p in P:
    print(f"===== {r} · ma thoat {p.returncode} · {dem(r)}/4463", flush=True)
    print("".join(open(f"{W}/gen_{r}.log", errors="ignore").readlines()[-4:]), flush=True)
shutil.rmtree(MERGED, ignore_errors=True)
import zipfile
fs = [f for f in glob.glob(f"{W}/*") if os.path.isfile(f) and f.endswith((".jsonl", ".log"))]
with zipfile.ZipFile(f"{W}/ket_qua_gen.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in fs: z.write(f, os.path.basename(f))
print("da zip", sorted(os.path.basename(f) for f in fs), flush=True)
'''
cells = [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": c.splitlines(True)} for c in (C0, C1, C2, C3)]
nb = {"cells": cells, "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}, "nbformat": 4, "nbformat_minor": 5}
d = f"{H}/k_{name}"; os.makedirs(d, exist_ok=True)
json.dump(nb, open(f"{d}/{name}.ipynb", "w"), ensure_ascii=False, indent=1)
json.dump({"id": f"{user}/{name}", "title": name, "code_file": f"{name}.ipynb", "language": "python", "kernel_type": "notebook", "is_private": "true",
           "enable_gpu": "true", "enable_internet": "true",
           "dataset_sources": [f"{user}/thesis-score", f"{user}/fgrb-p1-bundle", f"{user}/grpo-spice-script"],
           "competition_sources": [], "kernel_sources": [prev]}, open(f"{d}/kernel-metadata.json", "w"), indent=1)
print("đã dựng", d)
