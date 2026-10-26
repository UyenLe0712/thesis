# AndroidControl phần S1 chưa thấy (956 tác vụ, 1.484 bước chạm): lấy ảnh từ TFRecord gốc (reece124/android_control,
# 20 shard GZIP), OCR bằng RapidOCR cùng luật prep_ocr_train.py, dựng khối 4 ví dụ cho ACE. Kaggle CPU, có internet.
import os, sys, json, glob, time, subprocess, collections, shutil, hashlib
T0 = time.time()
WS = "/kaggle/working"; D = f"{WS}/acu_test"; os.makedirs(f"{D}/images", exist_ok=True)
TOM = open(f"{WS}/tom_tat.txt", "a")
def ghi(*a):
    s = f"[{(time.time()-T0)/3600:5.2f} h] " + " ".join(map(str, a)); print(s, flush=True); TOM.write(s + "\n"); TOM.flush()
def sh(c): ghi("$", c); r = subprocess.run(c, shell=True, capture_output=True, text=True); ghi((r.stdout + r.stderr)[-1200:]); return r.returncode
# 1.4.4 là bản đã dựng OCR tập kiểm cũ; Kaggle (Python 3.13) chỉ có tới 1.2.3 ⇒ cài bản mới nhất cài được, ghi phiên bản,
# và đo mức lệch bằng phép kiểm 20 ảnh tập kiểm cũ bên dưới
sh(f"{sys.executable} -m pip install -q huggingface_hub")
if sh(f"{sys.executable} -m pip install -q 'rapidocr_onnxruntime==1.4.4'"):
    assert sh(f"{sys.executable} -m pip install -q rapidocr_onnxruntime") == 0, "DỪNG: không cài được rapidocr_onnxruntime"
sh(f"{sys.executable} -m pip show rapidocr_onnxruntime onnxruntime | grep -E 'Name|Version'")
KIT = os.path.dirname(glob.glob("/kaggle/input/**/tfr.py", recursive=True)[0]); sys.path.insert(0, KIT)
import tfr
R = [json.loads(l) for l in open(f"{KIT}/acu_test.jsonl")]
TAPT = ("click", "long_press")
can = {(r["episode_id"], r["step_id"]): r for r in R if r["action"].get("action_type") in TAPT and "x" in r["action"]}
ghi("bản ghi", len(R), "· bước chạm cần ảnh", len(can)); assert len(R) == 3103 and len(can) == 1484
EP = collections.defaultdict(list)
for r in R: EP[r["episode_id"]].append(r)

# Pha 1: quét 20 shard, chỉ ghi ảnh của bước chạm cần; đối chiếu câu và thao tác của TFRecord với HarrytheOrange
from huggingface_hub import hf_hub_download
lech = collections.Counter(); gap = set(); wh = {}
TMPD = "/kaggle/temp/tfr"; os.makedirs(TMPD, exist_ok=True)
for s in range(20):
    t = time.time(); fn = f"android_control-{s:05d}-of-00020"
    p = hf_hub_download("reece124/android_control", fn, repo_type="dataset", local_dir=TMPD)
    n = 0
    for b in tfr.records(p):
        d = tfr.example(b); e = d["episode_id"][0]
        if e not in EP: continue
        gap.add(e); n += 1
        ins = [x.decode() for x in d["step_instructions"]]; act = [json.loads(x) for x in d["actions"]]
        for r in EP[e]:
            sid = r["step_id"]
            if sid >= len(ins) or ins[sid] != r["gold_instruction"]: lech["câu"] += 1
            if sid >= len(act) or act[sid] != r["action"]: lech["thao tác"] += 1
            k = (e, sid)
            if k in can:
                if sid >= len(d["screenshots"]): lech["thiếu ảnh"] += 1; continue
                open(f"{D}/{r['image']}", "wb").write(d["screenshots"][sid])
                wh[r["image"]] = (d["screenshot_widths"][sid], d["screenshot_heights"][sid])
    os.remove(p)
    ghi(f"shard {s}: {n} tác vụ cần · tổng gặp {len(gap)}/{len(EP)} · ảnh {len(wh)}/{len(can)} · lệch {dict(lech)} · {time.time()-t:.0f}s")
thieu = [k for k, r in can.items() if r["image"] not in wh]
ghi("thiếu ảnh", len(thieu), thieu[:5]); ghi("lệch với HarrytheOrange", dict(lech))
with open(f"{D}/test.jsonl", "w", encoding="utf-8") as f:
    for r in R: f.write(json.dumps(r, ensure_ascii=False) + "\n")

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
sh(f"{sys.executable} {WS}/ocr_one.py {KO} {WS}/kiem.json {WS}/kiem_ocr.jsonl")
cu = {json.loads(l)["image"]: json.loads(l) for l in open(f"{KIT}/kiem_ocr/ocr.jsonl")}
moi = {json.loads(l)["image"]: json.loads(l) for l in open(f"{WS}/kiem_ocr.jsonl")}
tr = sum(moi[k]["items"] == cu[k]["items"] for k in cu)
tr24 = sum([x["text"] for x in moi[k]["items"][:24]] == [x["text"] for x in cu[k]["items"][:24]] for k in cu)
ghi(f"[kiểm OCR] {tr}/20 ảnh trùng tuyệt đối · {tr24}/20 trùng chữ 24 dòng đầu (phần đi vào câu nhắc)")
imgs = sorted(r["image"] for r in can.values()); NP = 4
procs = []
for k in range(NP):
    json.dump(imgs[k::NP], open(f"{WS}/imgs{k}.json", "w"))
    procs.append(subprocess.Popen([sys.executable, f"{WS}/ocr_one.py", D, f"{WS}/imgs{k}.json", f"{WS}/ocr.part{k}.jsonl"],
                                  stdout=open(f"{WS}/ocr{k}.log", "a"), stderr=subprocess.STDOUT))
while any(q.poll() is None for q in procs):
    time.sleep(120)
    ghi("OCR", sum(sum(1 for _ in open(f"{WS}/ocr.part{k}.jsonl")) for k in range(NP) if os.path.exists(f"{WS}/ocr.part{k}.jsonl")), "/", len(imgs))
with open(f"{D}/ocr.jsonl", "w", encoding="utf-8") as f:
    for k in range(NP):
        for l in open(f"{WS}/ocr.part{k}.jsonl"): f.write(l)
O_ = {json.loads(l)["image"]: json.loads(l) for l in open(f"{D}/ocr.jsonl")}
ghi("OCR xong", len(O_), "· ảnh 0 dòng", sum(not o["items"] for o in O_.values())); assert len(O_) == len(imgs)

# Pha 3: khối 4 ví dụ cho ACE, y hệt xuat_ex_304.py (kho train_tru_val, bỏ episode val)
import ra_exemplars as RA
vep = set(json.load(open(f"{KIT}/val_eps.json")))
kho = RA.Kho([json.loads(l) for l in open(f"{KIT}/train_tru_val.jsonl")], loai_ep=vep); ghi("kho", len(kho.tr))
ot = lambda o: {w for it in (o or {"items": []})["items"][:24] for w in RA.tok(it.get("text", ""))}
h = 0
with open(f"{D}/ex_acu_k4.jsonl", "w", encoding="utf-8") as f:
    for r in R:
        k = (r["episode_id"], r["step_id"])
        if k not in can: continue
        ex = [dict(sent=e["sent"], goal=e["goal"], prev=e["prev"]) for e in kho.cho_test(dict(goal=r["goal"], history=r.get("history") or []), 4, ot(O_.get(r["image"])))]
        h += any(RA.tok(e["sent"]) == RA.tok(r["gold_instruction"]) for e in ex)
        f.write(json.dumps({"episode_id": k[0], "step_id": k[1], "exemplars": ex}, ensure_ascii=False) + "\n")
ghi(f"khối ví dụ 1484 bước · chứa đúng câu chuẩn {100*h/1484:.1f}%")
sh(f"cd {WS} && zip -qr acu_test.zip acu_test tom_tat.txt kiem_ocr.jsonl && ls -la {WS}")
ghi("KẾT THÚC")
