# OCR lại 1.484 ảnh ACU bằng rapidocr_onnxruntime 1.4.4 (bản đã dựng OCR tập kiểm/train) trong venv Python 3.12,
# vì Kaggle Python 3.13 chỉ cài được 1.2.3 (lượt acu-build-cpu: 1/20 ảnh trùng 24 dòng đầu). Ảnh lấy từ output acu-build-cpu.
# Dừng nếu phép kiểm 20 ảnh tập kiểm cũ không trùng tuyệt đối 20/20. Rồi dựng lại khối 4 ví dụ (y hệt pha 3 của acu_build.py).
import os, sys, json, glob, time, subprocess, shutil, hashlib
T0 = time.time()
WS = "/kaggle/working"; TOM = open(f"{WS}/tom_tat.txt", "a")
def ghi(*a):
    s = f"[{(time.time()-T0)/3600:5.2f} h] " + " ".join(map(str, a)); print(s, flush=True); TOM.write(s + "\n"); TOM.flush()
def sh(c): ghi("$", c); r = subprocess.run(c, shell=True, capture_output=True, text=True); ghi((r.stdout + r.stderr)[-1200:]); return r.returncode
V = "/kaggle/temp/v312"
assert sh(f"{sys.executable} -m pip install -q uv") == 0
assert sh(f"uv venv -q -p 3.12 {V}") == 0, "DỪNG: không dựng được venv 3.12"
assert sh(f"uv pip install -q -p {V}/bin/python 'rapidocr_onnxruntime==1.4.4' pillow numpy") == 0, "DỪNG: không cài được 1.4.4"
sh(f"uv pip show -p {V}/bin/python rapidocr_onnxruntime onnxruntime | grep -E 'Name|Version'")
PY = f"{V}/bin/python"
KIT = os.path.dirname(glob.glob("/kaggle/input/**/tfr.py", recursive=True)[0]); sys.path.insert(0, KIT)
SRC = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/acu_test/test.jsonl", recursive=True)]
assert len(SRC) == 1, SRC; D = SRC[0]; ghi("ảnh", D, len(os.listdir(f"{D}/images")))
O = f"{WS}/acu_ocr144"; os.makedirs(O, exist_ok=True)
R = [json.loads(l) for l in open(f"{D}/test.jsonl")]
TAPT = ("click", "long_press")
can = {(r["episode_id"], r["step_id"]): r for r in R if r["action"].get("action_type") in TAPT and "x" in r["action"]}
assert len(can) == 1484, len(can)
# Pha 2: OCR (4 tiến trình, mỗi tiến trình một luồng), cùng luật lọc prep_ocr_train.py; kiểm tái lập trên 20 ảnh tập kiểm cũ
OCR_PY = r'''
import os, sys, json
os.environ["OMP_NUM_THREADS"] = "1"
from rapidocr_onnxruntime import RapidOCR
from PIL import Image
import numpy as np
COLS = ["bên trái", "giữa", "bên phải"]; ROWS = ["trên đỉnh", "giữa màn", "dưới đáy"]
zone = lambda cx, cy, w, h: f"{ROWS[min(int(cy / h * 3), 2)]}, {COLS[min(int(cx / w * 3), 2)]}"
root, imgs, out = sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3]
try: ocr = RapidOCR(intra_op_num_threads=1)
except TypeError: ocr = RapidOCR()
done = {json.loads(l)["image"] for l in open(out)} if os.path.exists(out) else set()
with open(out, "a", encoding="utf-8") as f:
    for i, rel in enumerate(imgs):
        if rel in done: continue
        im = Image.open(os.path.join(root, rel)).convert("RGB"); w, h = im.size
        try: res, _ = ocr(im)
        except Exception: res, _ = ocr(np.array(im))
        items = []
        for box, txt, conf in (res or []):
            xs = [p[0] for p in box]; ys = [p[1] for p in box]; cx, cy = sum(xs) / 4, sum(ys) / 4; t = (txt or "").strip()
            if len(t) < 1 or float(conf) < 0.5: continue
            items.append({"text": t, "cx": round(cx), "cy": round(cy), "zone": zone(cx, cy, w, h)})
        f.write(json.dumps({"image": rel, "w": w, "h": h, "items": items}, ensure_ascii=False) + "\n"); f.flush()
        if (i + 1) % 50 == 0: print(i + 1, len(imgs), flush=True)
'''
open(f"{WS}/ocr_one.py", "w").write(OCR_PY)
kq = sorted(glob.glob(f"{KIT}/kiem_ocr/*.png")); KO = "/kaggle/temp/kiem_ocr"; os.makedirs(f"{KO}/images", exist_ok=True)
for p in kq: shutil.copy(p, f"{KO}/images/")
json.dump([f"images/{os.path.basename(p)}" for p in kq], open(f"{WS}/kiem.json", "w"))
if os.path.exists(f"{WS}/kiem_ocr.jsonl"): os.remove(f"{WS}/kiem_ocr.jsonl")
sh(f"{PY} {WS}/ocr_one.py {KO} {WS}/kiem.json {WS}/kiem_ocr.jsonl")
cu = {json.loads(l)["image"]: json.loads(l) for l in open(f"{KIT}/kiem_ocr/ocr.jsonl")}
moi = {json.loads(l)["image"]: json.loads(l) for l in open(f"{WS}/kiem_ocr.jsonl")}
tr = sum(moi[k]["items"] == cu[k]["items"] for k in cu)
tr24 = sum([x["text"] for x in moi[k]["items"][:24]] == [x["text"] for x in cu[k]["items"][:24]] for k in cu)
ghi(f"[kiểm OCR] {tr}/20 ảnh trùng tuyệt đối · {tr24}/20 trùng chữ 24 dòng đầu (phần đi vào câu nhắc)")
assert tr == 20, "DỪNG: OCR 1.4.4 không tái lập tập kiểm cũ"
imgs = sorted(r["image"] for r in can.values()); NP = os.cpu_count() or 4; ghi("tiến trình", NP)
procs = []
for k in range(NP):
    json.dump(imgs[k::NP], open(f"{WS}/imgs{k}.json", "w"))
    procs.append(subprocess.Popen([PY, f"{WS}/ocr_one.py", D, f"{WS}/imgs{k}.json", f"{WS}/ocr.part{k}.jsonl"],
                                  stdout=open(f"{WS}/ocr{k}.log", "a"), stderr=subprocess.STDOUT))
while any(q.poll() is None for q in procs):
    time.sleep(120)
    ghi("OCR", sum(sum(1 for _ in open(f"{WS}/ocr.part{k}.jsonl")) for k in range(NP) if os.path.exists(f"{WS}/ocr.part{k}.jsonl")), "/", len(imgs))
with open(f"{O}/ocr_acu_144.jsonl", "w", encoding="utf-8") as f:
    for k in range(NP):
        for l in open(f"{WS}/ocr.part{k}.jsonl"): f.write(l)
O_ = {json.loads(l)["image"]: json.loads(l) for l in open(f"{O}/ocr_acu_144.jsonl")}
ghi("OCR xong", len(O_), "· ảnh 0 dòng", sum(not o["items"] for o in O_.values())); assert len(O_) == len(imgs)

# Pha 3: khối 4 ví dụ cho ACE, y hệt xuat_ex_304.py (kho train_tru_val, bỏ episode val)
import ra_exemplars as RA
vep = set(json.load(open(f"{KIT}/val_eps.json")))
kho = RA.Kho([json.loads(l) for l in open(f"{KIT}/train_tru_val.jsonl")], loai_ep=vep); ghi("kho", len(kho.tr))
ot = lambda o: {w for it in (o or {"items": []})["items"][:24] for w in RA.tok(it.get("text", ""))}
h = 0
with open(f"{O}/ex_acu_k4.jsonl", "w", encoding="utf-8") as f:
    for r in R:
        k = (r["episode_id"], r["step_id"])
        if k not in can: continue
        ex = [dict(sent=e["sent"], goal=e["goal"], prev=e["prev"]) for e in kho.cho_test(dict(goal=r["goal"], history=r.get("history") or []), 4, ot(O_.get(r["image"])))]
        h += any(RA.tok(e["sent"]) == RA.tok(r["gold_instruction"]) for e in ex)
        f.write(json.dumps({"episode_id": k[0], "step_id": k[1], "exemplars": ex}, ensure_ascii=False) + "\n")
ghi(f"khối ví dụ 1484 bước · chứa đúng câu chuẩn {100*h/1484:.1f}%")
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
for f in ("ocr_acu_144.jsonl", "ex_acu_k4.jsonl"): ghi("md5", f, md5(f"{O}/{f}"))
shutil.copy(f"{WS}/kiem_ocr.jsonl", O); shutil.copy(f"{WS}/tom_tat.txt", O)
sh(f"cd {WS} && zip -qr acu_ocr144.zip acu_ocr144 && ls -la {WS}")
ghi("KẾT THÚC")
