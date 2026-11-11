# -*- coding: utf-8 -*-
"""SA-SPICE-v3 kernel 2 (Kaggle T4×2): UGround chấm exec cho greedy + 8 mẫu SFT-cont trên mọi bước chạm TRAIN-v3.
Khuôn = runbook report/251 (exec 8 mẫu C1), chỉ đổi dữ liệu. Chạy SAU khi đã tải output kernel 1 về runs/sa_spice_v3/mau_k1/.

  python3 _bundles/sa3_cham/make_k2.py <tài khoản kaggle> <username>
  kg <tk> datasets create -p _bundles/sa3_cham/ds --dir-mode zip
  kg <tk> kernels push -p _bundles/sa3_cham/k --accelerator NvidiaTeslaT4
"""
import json, os, sys, shutil, hashlib

acc, user = sys.argv[1:3]
KS = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else list(range(9))   # tệp câu chấm ở kernel này
CAT_H = float(os.environ.get("CAT_H", "10.5"))
TAG = "" if len(sys.argv) <= 3 else "-" + "".join(map(str, KS))
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.dirname(os.path.abspath(__file__))
DS, K = os.path.join(H, "ds"), os.path.join(H, "k")
os.makedirs(DS + "/images", exist_ok=True); os.makedirs(DS + "/thesis/harness", exist_ok=True); os.makedirs(K, exist_ok=True)
TAPT = ("click", "long_press")

rows = [json.loads(l) for l in open(f"{R}/runs/sa_spice_v3/split/train_v3.jsonl", encoding="utf-8")]
M = {}
for i in (0, 1):
    for l in open(f"{R}/runs/sa_spice_v3/mau_k1/mau_{i}.jsonl", encoding="utf-8"):
        d = json.loads(l); M[(d["episode_id"], d["step_id"])] = d
assert len(M) == 1000, len(M)
taps = [r for r in rows if r["action"]["action_type"] in TAPT and "x" in r["action"]]
with open(f"{DS}/recs.jsonl", "w", encoding="utf-8") as f:
    for r in taps:
        f.write(json.dumps({**r, "gold_instruction": r["target_instruction"]}, ensure_ascii=False) + "\n")
os.makedirs(f"{DS}/preds", exist_ok=True)
for k in range(9):
    with open(f"{DS}/preds/k{k}.jsonl", "w", encoding="utf-8") as f:
        for r in taps:
            m = M[(r["episode_id"], r["step_id"])]
            f.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"],
                                "pred": m["greedy"] if k == 0 else m["mau"][k - 1]}, ensure_ascii=False) + "\n")
for r in taps:
    d = f"{DS}/{r['image']}"
    if not os.path.exists(d):
        shutil.copy2(f"{R}/harness/dg1_cache/train_ac/{r['image']}", d)
for f in ("score_run.py", "metric_exec.py", "a11y_inventory.py"):
    shutil.copy2(f"{R}/harness/{f}", f"{DS}/thesis/harness/{f}")
NT = len(taps)
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
MD5 = md5(f"{DS}/recs.jsonl")
json.dump({"title": "sa3-cham-train-v3", "id": f"{user}/sa3-cham-train-v3", "licenses": [{"name": "other"}], "isPrivate": True},
          open(f"{DS}/dataset-metadata.json", "w"), indent=1)

c0 = '''import os, subprocess, sys, glob, json, shutil, time
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"; os.environ["TQDM_DISABLE"] = "1"
subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "-q", "torchao"])
import torch, hashlib
NGPU = torch.cuda.device_count(); assert NGPU >= 1
print("NGPU", NGPU, [torch.cuda.get_device_name(i) for i in range(NGPU)], flush=True)
'''
c1 = f'''W = "/kaggle/working"
P = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/recs.jsonl", recursive=True) if os.path.isdir(os.path.join(os.path.dirname(p), "preds"))]
assert len(P) == 1, P; P = P[0]
assert hashlib.md5(open(f"{{P}}/recs.jsonl", "rb").read()).hexdigest() == "{MD5}", "DUNG: recs lech"
WS = f"{{W}}/pk/thesis"; shutil.copytree(f"{{P}}/thesis", WS, dirs_exist_ok=True)
VD = f"{{W}}/data"; os.makedirs(VD, exist_ok=True)
shutil.copy(f"{{P}}/recs.jsonl", f"{{VD}}/recs.jsonl")
if os.path.lexists(f"{{VD}}/images"): os.remove(f"{{VD}}/images")
os.symlink(f"{{P}}/images", f"{{VD}}/images")
recs = [json.loads(l) for l in open(f"{{VD}}/recs.jsonl")]
assert len(recs) == {NT} and all(os.path.exists(f"{{VD}}/{{r['image']}}") for r in recs)
PD, OUT = f"{{P}}/preds", f"{{W}}/score"; os.makedirs(OUT, exist_ok=True)
from huggingface_hub import snapshot_download
print("UGround:", snapshot_download("osunlp/UGround-V1-2B"), flush=True)
sys.path.insert(0, f"{{WS}}/harness")
import a11y_inventory as A11Y, score_run as SR
names = set(A11Y._zip().namelist())
co = sum(A11Y.key_for(f"episode_{{d['episode_id']}}_screenshot_{{d['step_id']}}.png") in names for d in recs)
rong = sum(len(SR.buttons_of(d)) == 0 for d in recs)
print(f"cay tro nang {{co}}/{NT} · rong nut {{rong}}", flush=True)
assert co == {NT} and rong <= 3, "DUNG: thieu cay tro nang"  # 11/11: 1/622 buoc cay khong nut ⇒ Voronoi = cua so 14%
'''
c2 = f'''env = {{**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1"}}
lenh = lambda k, out: f"python harness/score_run.py --mode score --grounder uground --preds {{PD}}/k{{k}}.jsonl --data-root {{VD}} --recs-file recs.jsonl --out {{out}}"
os.makedirs(f"{{W}}/thu", exist_ok=True)
with open(f"{{W}}/thu.log", "w") as lg:
    rc = subprocess.run(lenh(0, f"{{W}}/thu/score_thu.json") + " --n 3", shell=True, cwd=WS, env={{**env, "CUDA_VISIBLE_DEVICES": "0"}}, stdout=lg, stderr=subprocess.STDOUT).returncode
tl = open(f"{{W}}/thu.log").read(); print(tl[-1200:], flush=True)
thu = [json.loads(l) for l in open(f"{{W}}/thu/score_thu_raw.jsonl")]
assert rc == 0 and len(thu) == 3 and f"[dữ liệu] {{VD}}/recs.jsonl" in tl and "[uground] nạp osunlp/UGround-V1-2B" in tl
assert all(o.get("pred_xy") and o.get("n_buttons", 0) > 0 for o in thu)
print("THU 3 BUOC: DAT", flush=True)
KS = {KS!r}
chuoi = {{g: [k for i, k in enumerate(KS) if i % NGPU == g] for g in range(NGPU)}}
PS = [subprocess.Popen(["bash", "-c", " && ".join(lenh(k, f"{{OUT}}/score_k{{k}}.json") for k in ks)], cwd=WS, env={{**env, "CUDA_VISIBLE_DEVICES": str(g)}},
                       start_new_session=True, stdout=open(f"{{W}}/cham_gpu{{g}}.log", "a"), stderr=subprocess.STDOUT) for g, ks in chuoi.items()]
dem = lambda: [sum(1 for _ in open(f"{{OUT}}/score_k{{k}}_raw.jsonl")) if os.path.exists(f"{{OUT}}/score_k{{k}}_raw.jsonl") else 0 for k in KS]
t0 = time.time()
while any(p.poll() is None for p in PS):
    time.sleep(120)
    print(f"{{(time.time()-t0)/3600:4.2f}} h · " + " ".join(f"k{{k}}:{{n}}/{NT}" for k, n in zip(KS, dem())), flush=True)
    if time.time() - t0 > {CAT_H} * 3600:
        [p.terminate() for p in PS]; print("⛔ qua tran gio — dung, giu phan da ghi", flush=True)
print("ma thoat", [p.returncode for p in PS], "dem", dem(), flush=True)
'''
c3 = '''import zipfile
with zipfile.ZipFile(f"{W}/sa3_cham_out.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for p in glob.glob(f"{OUT}/*") + glob.glob(f"{W}/*.log"):
        z.write(p, os.path.basename(p))
print("zip", os.path.getsize(f"{W}/sa3_cham_out.zip") // 1024, "KB", flush=True)
'''
nb = {"nbformat": 4, "nbformat_minor": 5,
      "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}, "language_info": {"name": "python"}},
      "cells": [{"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "id": f"o{i}", "source": c.splitlines(keepends=True)}
                for i, c in enumerate((c0, c1, c2, c3))]}
for i, c in enumerate((c0, c1, c2, c3)):
    compile(c, f"o{i}", "exec")
json.dump(nb, open(f"{K}/sa3-cham-k2.ipynb", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"id": f"{user}/sa3-cham-k2{TAG}", "title": f"sa3-cham-k2{TAG}", "code_file": "sa3-cham-k2.ipynb", "language": "python",
           "kernel_type": "notebook", "is_private": "true", "enable_gpu": "true", "enable_internet": "true",
           "dataset_sources": [f"{user}/sa3-cham-train-v3"], "competition_sources": [], "kernel_sources": []},
          open(f"{K}/kernel-metadata.json", "w"), indent=1)
print("bước chạm", NT, "· recs md5", MD5)
