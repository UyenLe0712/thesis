# AitZ (Findings EMNLP 2024) → định dạng tập kiểm của dự án. Chạy Kaggle CPU, có internet.
# Pha 1: tải + thống kê + dựng test.jsonl/ảnh. Pha 2: OCR (RapidOCR, cùng luật lọc với prep_ocr_train.py).
import os, sys, json, glob, time, math, subprocess, collections, zipfile, shutil
T0 = time.time()
WS = "/kaggle/working"; OUT = f"{WS}/out"; os.makedirs(OUT, exist_ok=True)
TOM = open(f"{OUT}/tom_tat.txt", "a")
def ghi(*a):
    s = f"[{(time.time()-T0)/3600:5.2f} h] " + " ".join(map(str, a)); print(s, flush=True); TOM.write(s + "\n"); TOM.flush()
def sh(c): ghi("$", c); r = subprocess.run(c, shell=True, capture_output=True, text=True); ghi((r.stdout + r.stderr)[-1500:]); return r.returncode

sh("pip install -q gdown rapidocr_onnxruntime 2>&1 | tail -2")
Z = "/kaggle/temp/aitz.zip"; os.makedirs("/kaggle/temp", exist_ok=True)
if not os.path.exists(Z):
    sh(f"gdown --fuzzy 'https://drive.google.com/file/d/12xOV2m62fBUFLhMcWIsFiC6zwV7a2RhI/view' -O {Z}")
assert os.path.exists(Z), "tải Google Drive không được"
ghi("zip", os.path.getsize(Z) / 2**30, "GiB")
zf = zipfile.ZipFile(Z); names = zf.namelist()
ghi("số tệp trong zip", len(names)); ghi("ví dụ", names[:8])
top = collections.Counter("/".join(n.split("/")[:3]) for n in names); ghi("thư mục", top.most_common(20))
js = [n for n in names if n.endswith(".json") and "/test/" in n]
ghi("json test", len(js))
assert js, "không thấy thư mục test"

def L(v): return json.loads(v) if isinstance(v, str) else v
D = "/kaggle/temp/aitz_test"; IM = f"{D}/images"; os.makedirs(IM, exist_ok=True)
recs, st = [], collections.Counter(); sizes = collections.Counter(); cat = collections.Counter()
img_names = {n.split("/")[-1]: n for n in names if n.endswith(".png") and "/test/" in n}
from PIL import Image
for n in sorted(js):
    ep = json.loads(zf.read(n))
    if not isinstance(ep, list): continue
    ep = sorted(ep, key=lambda s: int(s["step_id"]))
    hist = []
    for s in ep:
        eid = str(s["episode_id"]); sid = int(s["step_id"]); c = n.split("/")[-3] if n.count("/") >= 2 else ""
        at = int(s["result_action_type"]); t = L(s["result_touch_yx"]); l = L(s["result_lift_yx"])
        desc = (s.get("coat_action_desc") or "").strip()
        png = s["image_path"].split("/")[-1]
        if png not in img_names: st["thiếu ảnh"] += 1; hist.append(desc); continue
        rel = f"images/aitz_{eid}_{sid}.png"
        with open(f"{D}/{rel}", "wb") as f: f.write(zf.read(img_names[png]))
        W, H = Image.open(f"{D}/{rel}").size; sizes[(W, H)] += 1
        if at == 4:
            if math.dist(t, l) <= 0.04: act = {"action_type": "click", "x": round(t[1] * W, 1), "y": round(t[0] * H, 1)}
            else: act = {"action_type": "scroll", "touch_yx": t, "lift_yx": l}
        else: act = {"action_type": {3: "input_text", 5: "navigate_back", 6: "navigate_home", 7: "enter", 10: "status_complete", 11: "status_impossible"}.get(at, f"t{at}"), "text": s.get("result_action_text", "")}
        st[act["action_type"]] += 1; cat[c] += 1
        P = L(s.get("ui_positions") or "[]"); TX = L(s.get("ui_text") or "[]"); TY = L(s.get("ui_types") or "[]")
        boxes = [[p[1], p[0], p[1] + p[3], p[0] + p[2]] for p in P]   # [y,x,h,w] px → [x1,y1,x2,y2]
        recs.append({"episode_id": eid, "step_id": sid, "image": rel, "goal": s["instruction"],
                     "gold_instruction": desc, "action": act, "app": "", "category": c,
                     "history": list(hist), "app_seen_in_train": None,
                     "buttons": [[(b[0] + b[2]) / 2, (b[1] + b[3]) / 2] for b in boxes],
                     "boxes": boxes, "ui_text": TX, "ui_types": TY})
        hist.append(desc)
with open(f"{D}/test.jsonl", "w", encoding="utf-8") as f:
    for r in recs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
taps = [r for r in recs if r["action"]["action_type"] == "click"]
ghi("tác vụ", len({r["episode_id"] for r in recs}), "· bước", len(recs), "· bước chạm", len(taps))
ghi("loại thao tác", dict(st)); ghi("nhóm", dict(cat)); ghi("cỡ ảnh", sizes.most_common(6))
ghi("bước chạm không có khung phần tử", sum(1 for r in taps if not r["boxes"]))
inbox = sum(1 for r in taps if any(b[0] <= r["action"]["x"] <= b[2] and b[1] <= r["action"]["y"] <= b[3] for b in r["boxes"]))
ghi("điểm chạm vàng nằm trong ít nhất một khung", inbox, "/", len(taps))
ghi("câu mô tả rỗng ở bước chạm", sum(1 for r in taps if not r["gold_instruction"]))
for r in taps[:12]: ghi("  ví dụ:", r["goal"][:60], "|", r["gold_instruction"][:100])
json.dump({"tac_vu": len({r['episode_id'] for r in recs}), "buoc": len(recs), "buoc_cham": len(taps), "loai": dict(st), "nhom": dict(cat),
           "co_anh": [[list(k), v] for k, v in sizes.most_common(10)], "trong_khung": inbox}, open(f"{OUT}/thong_ke.json", "w"), ensure_ascii=False, indent=1)
zf.close(); os.remove(Z)
sh(f"cd /kaggle/temp && zip -qr {OUT}/aitz_test_khong_ocr.zip aitz_test && ls -la {OUT}")

# Pha 2: OCR — cùng luật với harness/prep_ocr_train.py (bỏ conf < 0.5, lưới 3x3 chữ tiếng Việt)
COLS = ["bên trái", "giữa", "bên phải"]; ROWS = ["trên đỉnh", "giữa màn", "dưới đáy"]
def zone(cx, cy, w, h): return f"{ROWS[min(int(cy / h * 3), 2)]}, {COLS[min(int(cx / w * 3), 2)]}"
def lam(args):
    k, n = args
    os.environ["OMP_NUM_THREADS"] = "1"
    from rapidocr_onnxruntime import RapidOCR
    try: ocr = RapidOCR(intra_op_num_threads=1)
    except TypeError: ocr = RapidOCR()
    p = f"{D}/ocr.part{k}.jsonl"; done = set()
    if os.path.exists(p): done = {json.loads(l)["image"] for l in open(p)}
    with open(p, "a", encoding="utf-8") as f:
        for i, r in enumerate(recs):
            if i % n != k or r["image"] in done: continue
            im = Image.open(f"{D}/{r['image']}").convert("RGB"); w, h = im.size
            res, _ = ocr(f"{D}/{r['image']}"); items = []
            for box, txt, conf in (res or []):
                cx = sum(q[0] for q in box) / 4; cy = sum(q[1] for q in box) / 4; t = (txt or "").strip()
                if len(t) < 1 or conf < 0.5: continue
                items.append({"text": t, "cx": round(cx), "cy": round(cy), "zone": zone(cx, cy, w, h)})
            f.write(json.dumps({"image": r["image"], "w": w, "h": h, "items": items}, ensure_ascii=False) + "\n"); f.flush()
    return k
import traceback
try:
  from multiprocessing import Pool
  N = os.cpu_count() or 4; ghi("OCR", len(recs), "ảnh ·", N, "tiến trình")
  with Pool(N) as pool:
      it = pool.imap_unordered(lam, [(k, N) for k in range(N)])
      import threading
      stop = False
      def nhip():
          while not stop:
              time.sleep(120); c = sum(sum(1 for _ in open(p)) for p in glob.glob(f"{D}/ocr.part*.jsonl"))
              print(f"  {(time.time()-T0)/3600:5.2f} h · OCR {c}/{len(recs)}", flush=True)
      th = threading.Thread(target=nhip, daemon=True); th.start()
      for _ in it: pass
      stop = True
  seen = set()
  with open(f"{D}/ocr.jsonl", "w", encoding="utf-8") as w:
      for p in sorted(glob.glob(f"{D}/ocr.part*.jsonl")):
          for l in open(p):
              k = json.loads(l)["image"]
              if k not in seen: seen.add(k); w.write(l)
  for p in glob.glob(f"{D}/ocr.part*.jsonl"): os.remove(p)
  ghi("OCR xong", len(seen), "ảnh")
except Exception:
  ghi("OCR LỖI:\n" + traceback.format_exc())
sh(f"cd /kaggle/temp && zip -qr {OUT}/aitz_test.zip aitz_test && cp aitz_test/test.jsonl aitz_test/ocr.jsonl {OUT}/ && rm -f {OUT}/aitz_test_khong_ocr.zip && ls -la {OUT}")
ghi("KẾT THÚC")
