# -*- coding: utf-8 -*-
"""
FREE — tính lại sàn/trần/chênh dưới ĐĨA vs VORONOI, dùng inventory OCR đã cache.
Trả lời debate M6/M7: Voronoi có siết trần (bớt trúng-giả do nút cạnh) không, chênh có giữ không.
Không API, không GPU. Dùng: ground_pilot pred (trần, câu gold) + ground_floor pred (sàn, không câu)
+ OCR boxes (inventory nút-proxy) + gold coord.
"""
import os, sys, json, re, glob
sys.path.insert(0, os.path.dirname(__file__))
from metric_exec import hit_disk, hit_voronoi

HERE = os.path.dirname(os.path.abspath(__file__))
HF = os.path.expanduser("~/.cache/huggingface/hub/datasets--wangyuanlei--android_control_test/snapshots")
OCR = os.path.join(HERE, "dg1_cache", "ac_ocr")
CEIL = json.load(open(os.path.join(HERE, "dg1_cache", "ground_pilot", "pred.json"), encoding="utf-8"))
FLOOR = json.load(open(os.path.join(HERE, "dg1_cache", "ground_floor", "pred.json"), encoding="utf-8"))
TOL = 0.14


def find_ep(eid):
    h = glob.glob(os.path.join(HF, "*", "test_output_json", "*", f"episode_{eid}.json"))
    return h[0] if h else None


def ocr_centers(rel):
    key = re.sub(r"[^\w]", "_", os.path.basename(rel)) + ".json"
    p = os.path.join(OCR, key)
    if not os.path.exists(p):
        return None
    return [(b["cx"], b["cy"]) for b in json.load(open(p, encoding="utf-8"))]


def gold_of(rel):
    m = re.search(r"episode_(\d+)_screenshot_(\d+)\.png", rel)
    eid, si = int(m.group(1)), int(m.group(2))
    ep = find_ep(eid)
    if not ep:
        return None
    o = json.load(open(ep, encoding="utf-8")); a = o.get("actions") or []
    if si >= len(a) or "x" not in a[si]:
        return None
    return float(a[si]["x"]), float(a[si]["y"])


def evalset(pred):
    """trả (disk_hit_rate, voronoi_hit_rate, n, n_no_ocr)"""
    dh = vh = n = no_ocr = 0
    for rel, p in pred.items():
        if p.get("px") is None:
            continue
        g = gold_of(rel)
        if not g:
            continue
        boxes = ocr_centers(rel)
        if boxes is None:
            no_ocr += 1; boxes = []
        wh = (p["w"], p["h"])
        inv = [g] + boxes                       # gold + nút-proxy OCR (gold luôn là ứng viên)
        pt = (p["px"], p["py"])
        n += 1
        if hit_disk(pt, g, wh, TOL):
            dh += 1
        if hit_voronoi(pt, g, inv, wh, TOL):
            vh += 1
    return dh / n, vh / n, n, no_ocr


cd, cv, nc, _ = evalset(CEIL)
fd, fv, nf, _ = evalset(FLOOR)
med_boxes = 0
allb = [len(ocr_centers(r) or []) for r in CEIL if ocr_centers(r) is not None]
if allb:
    allb.sort(); med_boxes = allb[len(allb) // 2]

print("=" * 64)
print(f"Inventory = OCR (trung vị {med_boxes} hộp/màn) + điểm gold. n_trần={nc}, n_sàn={nf}")
print("=" * 64)
print(f"{'':16}{'ĐĨA (cũ)':>12}{'VORONOI':>12}")
print(f"{'Trần (câu gold)':16}{cd:>11.1%}{cv:>12.1%}")
print(f"{'Sàn (không câu)':16}{fd:>11.1%}{fv:>12.1%}")
print(f"{'CHÊNH':16}{cd-fd:>+11.1%}{cv-fv:>+12.1%}")
print("=" * 64)
print("Đọc: nếu trần Voronoi TỤT nhiều so đĩa → nhiều 'trúng' cũ là trỏ-nhầm-nút-cạnh (thước cũ dễ dãi thật).")
print("     nếu CHÊNH Voronoi vẫn dương rõ → thước vẫn phân biệt được sau khi siết.")
print("Lưu ý: inventory OCR THỦNG (bỏ nút icon, chèn rác — report/75) → số này là ƯỚC LƯỢNG, bộ dò phần tử (OmniParser) sẽ chính xác hơn.")

json.dump({"ceil_disk": cd, "ceil_voronoi": cv, "floor_disk": fd, "floor_voronoi": fv,
           "range_disk": cd - fd, "range_voronoi": cv - fv, "n_ceil": nc, "n_floor": nf,
           "median_ocr_boxes": med_boxes},
          open(os.path.join(HERE, "voronoi_recheck_results.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nĐã lưu voronoi_recheck_results.json")
