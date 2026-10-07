# -*- coding: utf-8 -*-
"""
FREE — thay inventory OCR bằng BỘ DÒ PHẦN TỬ OmniParser-v2 (YOLO, CPU), tính lại Voronoi.
Trả lời M7 chính xác hơn: OCR bỏ nút icon + chèn rác; OmniParser dò được cả nút icon.
So ba cách: đĩa · Voronoi(OCR) · Voronoi(OmniParser).
"""
import os, sys, json, re, glob
sys.path.insert(0, os.path.dirname(__file__))
from metric_exec import hit_disk, hit_voronoi
from ultralytics import YOLO
from huggingface_hub import hf_hub_download

HERE = os.path.dirname(os.path.abspath(__file__))
HF = os.path.expanduser("~/.cache/huggingface/hub/datasets--wangyuanlei--android_control_test/snapshots")
OCRDIR = os.path.join(HERE, "dg1_cache", "ac_ocr")
DET_CACHE = os.path.join(HERE, "dg1_cache", "omni_det")
os.makedirs(DET_CACHE, exist_ok=True)
CEIL = json.load(open(os.path.join(HERE, "dg1_cache", "ground_pilot", "pred.json"), encoding="utf-8"))
FLOOR = json.load(open(os.path.join(HERE, "dg1_cache", "ground_floor", "pred.json"), encoding="utf-8"))
TOL = 0.14

_w = hf_hub_download("microsoft/OmniParser-v2.0", "icon_detect/model.pt")
MODEL = YOLO(_w)


def find_png(rel):
    h = glob.glob(os.path.join(HF, "*", rel)); return h[0] if h else None


def find_ep(eid):
    h = glob.glob(os.path.join(HF, "*", "test_output_json", "*", f"episode_{eid}.json")); return h[0] if h else None


def gold_of(rel):
    m = re.search(r"episode_(\d+)_screenshot_(\d+)\.png", rel)
    eid, si = int(m.group(1)), int(m.group(2)); ep = find_ep(eid)
    if not ep: return None
    o = json.load(open(ep, encoding="utf-8")); a = o.get("actions") or []
    if si >= len(a) or "x" not in a[si]: return None
    return float(a[si]["x"]), float(a[si]["y"])


def omni_centers(rel):
    key = re.sub(r"[^\w]", "_", os.path.basename(rel)) + ".json"
    cp = os.path.join(DET_CACHE, key)
    if os.path.exists(cp):
        return json.load(open(cp, encoding="utf-8"))
    png = find_png(rel)
    if not png: return []
    r = MODEL.predict(png, conf=0.05, iou=0.1, verbose=False)[0]
    cs = []
    for b in r.boxes.xyxy.tolist():
        cs.append([(b[0] + b[2]) / 2, (b[1] + b[3]) / 2])
    json.dump(cs, open(cp, "w"), ensure_ascii=False)
    return cs


def ocr_centers(rel):
    p = os.path.join(OCRDIR, re.sub(r"[^\w]", "_", os.path.basename(rel)) + ".json")
    if not os.path.exists(p): return []
    return [[b["cx"], b["cy"]] for b in json.load(open(p, encoding="utf-8"))]


def evalset(pred, inv_fn):
    d = v = n = 0
    for rel, p in pred.items():
        if p.get("px") is None: continue
        g = gold_of(rel)
        if not g: continue
        wh = (p["w"], p["h"]); pt = (p["px"], p["py"]); inv = [g] + inv_fn(rel)
        n += 1
        if hit_disk(pt, g, wh, TOL): d += 1
        if hit_voronoi(pt, g, inv, wh, TOL): v += 1
    return d / n, v / n, n


print("Đang dò phần tử OmniParser trên các màn (CPU, có cache)...")
# đo trung vị số hộp OmniParser
nb = []
for rel in CEIL:
    if CEIL[rel].get("px") is not None:
        nb.append(len(omni_centers(rel)))
nb.sort(); med_omni = nb[len(nb) // 2] if nb else 0

cd, cv_ocr, nc = evalset(CEIL, ocr_centers)
_, cv_omni, _ = evalset(CEIL, omni_centers)
fd, fv_ocr, nf = evalset(FLOOR, ocr_centers)
_, fv_omni, _ = evalset(FLOOR, omni_centers)

print("=" * 72)
print(f"n_trần={nc} n_sàn={nf} | OmniParser trung vị {med_omni} phần tử/màn (OCR: 24)")
print("=" * 72)
print(f"{'':16}{'ĐĨA':>11}{'VOR(OCR)':>12}{'VOR(Omni)':>12}")
print(f"{'Trần (gold)':16}{cd:>10.1%}{cv_ocr:>12.1%}{cv_omni:>12.1%}")
print(f"{'Sàn (∅)':16}{fd:>10.1%}{fv_ocr:>12.1%}{fv_omni:>12.1%}")
print(f"{'CHÊNH':16}{cd-fd:>+10.1%}{cv_ocr-fv_ocr:>+12.1%}{cv_omni-fv_omni:>+12.1%}")
print("=" * 72)
print("OmniParser dò được nút icon (OCR bỏ) + ít rác hơn → inventory sát thật hơn.")
print("Chênh Voronoi(Omni) là con số de-risk chính: >0 rõ = thước sống sau khi siết trên inventory tốt.")

json.dump({"ceil_disk": cd, "ceil_vor_ocr": cv_ocr, "ceil_vor_omni": cv_omni,
           "floor_disk": fd, "floor_vor_ocr": fv_ocr, "floor_vor_omni": fv_omni,
           "range_disk": cd - fd, "range_vor_ocr": cv_ocr - fv_ocr, "range_vor_omni": cv_omni - fv_omni,
           "median_omni_boxes": med_omni, "n": nc},
          open(os.path.join(HERE, "voronoi_omni_results.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nĐã lưu voronoi_omni_results.json")
