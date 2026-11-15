# Kaggle CPU: phép so D.3/AitW (so_d3_aitw_ck500.py) và ACU (doc_acu.py), chạy song song, có nhịp sống.
import glob, os, shutil, subprocess, sys, time, zipfile
W = "/kaggle/working/w"; shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
S = [p for p in glob.glob("/kaggle/input/**/so-27-10", recursive=True) if os.path.isdir(p)] or glob.glob("/kaggle/input/*")
S = S[0]; print("nguồn", S, os.listdir(S), flush=True)
for d in ("harness", "runs"):
    if os.path.isdir(f"{S}/{d}"): shutil.copytree(f"{S}/{d}", f"{W}/{d}", dirs_exist_ok=True)
    elif os.path.exists(f"{S}/{d}.zip"): zipfile.ZipFile(f"{S}/{d}.zip").extractall(f"{W}/{d}")
subprocess.run(f"{sys.executable} -m pip install -q scipy", shell=True)
os.makedirs(f"{W}/runs/acu", exist_ok=True)
P = {n: subprocess.Popen(f"cd {W}/harness && {sys.executable} -u {n}.py > {W}/{n}.log 2>&1", shell=True)
     for n in ("so_d3_aitw_ck500", "doc_acu")}
t0 = time.time()
while any(p.poll() is None for p in P.values()):
    time.sleep(120)
    print(f"[{(time.time()-t0)/3600:.2f} h]", {n: (p.poll(), open(f"{W}/{n}.log").read()[-150:].replace("\n", " | ")) for n, p in P.items()}, flush=True)
for n, p in P.items():
    print("==", n, "mã thoát", p.returncode); print(open(f"{W}/{n}.log").read()[-6000:], flush=True)
    shutil.copy(f"{W}/{n}.log", f"/kaggle/working/{n}.log")
for f in (f"{W}/runs/so_d3_aitw_ck500.json", f"{W}/runs/acu/ket_qua_acu.json"):
    if os.path.exists(f): shutil.copy(f, "/kaggle/working/")
shutil.rmtree(W); print(os.listdir("/kaggle/working"))
