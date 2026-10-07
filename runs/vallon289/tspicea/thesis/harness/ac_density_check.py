# -*- coding: utf-8 -*-
"""
Đo MẬT ĐỘ NÚT trên AndroidControl (lỗ #4 report/96/97) — FREE, không API.
Câu hỏi: dung sai 14% (~151px trên cạnh 1080) có "nuốt" nhiều nút cạnh không?
Nếu quanh nút gold còn nút KHÁC nằm trong vùng dung sai → bộ trỏ trỏ trật sang
nút sai vẫn tính TRÚNG → thước executability dương giả.

report/96 đo con số này = 55% NHƯNG trên MobileViews (có VH/bbox). Bản HF nhẹ của
AndroidControl thiếu bbox → ở đây dùng RapidOCR (ONNX/CPU/free) lấy TÂM HỘP CHỮ làm
nút-proxy, đo TRỰC TIẾP trên ảnh AndroidControl.

Cách: với mỗi bước click gold (x,y):
  - OCR ảnh → các hộp chữ (conf≥0.5, có ký tự chữ-số) → tâm hộp = nút-proxy.
  - Đếm số nút-proxy có tâm nằm trong hộp dung sai ±14%·w × ±14%·h quanh gold.
  - Hộp gần gold nhất (≤5% cạnh) coi là CHÍNH nút gold; các hộp còn lại trong dung sai = NÚT GÂY NHIỄU.
Báo: % bước có ≥1 nút gây nhiễu (dương-giả tiềm tàng), phân bố số nút trong dung sai.
Cache OCR để không chạy lại.

Chạy: ~/.venvs/thesis/bin/python harness/ac_density_check.py
"""
import os, sys, json, re, glob
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, "dg1_cache", "mde_pilot", "gen.json")
OCR_CACHE = os.path.join(HERE, "dg1_cache", "ac_ocr")
os.makedirs(OCR_CACHE, exist_ok=True)
HF = os.path.expanduser("~/.cache/huggingface/hub/datasets--wangyuanlei--android_control_test/snapshots")

TOL = 0.14          # dung sai AITW ~14% cạnh màn (khớp ground_pilot.py)
SELF = 0.05         # hộp ≤5% cạnh coi là chính nút gold, không phải nút nhiễu
CONF = 0.5


def find_episode(eid):
    hits = glob.glob(os.path.join(HF, "*", "test_output_json", "*", f"episode_{eid}.json"))
    return hits[0] if hits else None


def find_png(rel):
    hits = glob.glob(os.path.join(HF, "*", rel))
    return hits[0] if hits else None


def run_ocr(png, ocr):
    """OCR 1 ảnh → list [{cx,cy,text,conf}] (tâm hộp px), có cache."""
    key = re.sub(r"[^\w]", "_", os.path.basename(png)) + ".json"
    cp = os.path.join(OCR_CACHE, key)
    if os.path.exists(cp):
        return json.load(open(cp, encoding="utf-8"))
    res, _ = ocr(png)
    out = []
    if res:
        for box, text, conf in res:
            if conf < CONF:
                continue
            if not re.search(r"[A-Za-z0-9]", text or ""):
                continue
            xs = [p[0] for p in box]; ys = [p[1] for p in box]
            out.append({"cx": sum(xs) / 4.0, "cy": sum(ys) / 4.0,
                        "text": text, "conf": float(conf)})
    json.dump(out, open(cp, "w", encoding="utf-8"), ensure_ascii=False)
    return out


def main():
    gen = json.load(open(GEN, encoding="utf-8"))
    items = []
    for rel in gen:
        m = re.search(r"episode_(\d+)_screenshot_(\d+)\.png", rel)
        if not m:
            continue
        eid, si = int(m.group(1)), int(m.group(2))
        ep, png = find_episode(eid), find_png(rel)
        if not ep or not png:
            continue
        o = json.load(open(ep, encoding="utf-8"))
        acts = o.get("actions") or []
        if si >= len(acts):
            continue
        a = acts[si]
        if a.get("action_type") not in ("click", "long_press") or "x" not in a:
            continue
        items.append({"png": png, "gx": float(a["x"]), "gy": float(a["y"])})
    print(f"Bước click có gold toạ độ + ảnh local: {len(items)}")

    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR()

    in_tol = []          # tổng hộp OCR trong dung sai (gồm cả nút gold)
    confusers = []       # số nút NHIỄU (loại bỏ nút gold)
    has_confuser = 0
    n_boxes_all = []
    for i, it in enumerate(items):
        im = Image.open(it["png"]); w, h = im.size
        boxes = run_ocr(it["png"], ocr)
        n_boxes_all.append(len(boxes))
        within, self_hit = 0, False
        for b in boxes:
            ddx = abs(b["cx"] - it["gx"]) / w
            ddy = abs(b["cy"] - it["gy"]) / h
            if ddx <= TOL and ddy <= TOL:
                within += 1
                if ddx <= SELF and ddy <= SELF:
                    self_hit = True
        # nút nhiễu = số hộp trong dung sai, trừ 1 nếu có hộp trùng chính nút gold
        conf_n = within - (1 if self_hit else 0)
        in_tol.append(within)
        confusers.append(conf_n)
        if conf_n >= 1:
            has_confuser += 1
        if (i + 1) % 20 == 0:
            print(f"  ...{i+1}/{len(items)} ảnh đã OCR")

    n = len(items)
    def med(a): a = sorted(a); return a[len(a)//2] if a else 0
    res = {
        "n_click_steps": n,
        "tol": TOL,
        "median_ocr_boxes_per_screen": med(n_boxes_all),
        "pct_step_with_ge1_confuser": has_confuser / max(n, 1),
        "pct_step_with_ge1_box_in_tol": sum(1 for x in in_tol if x >= 1) / max(n, 1),
        "pct_step_with_ge2_box_in_tol": sum(1 for x in in_tol if x >= 2) / max(n, 1),
        "median_boxes_in_tol": med(in_tol),
        "median_confusers": med(confusers),
    }
    print("\n" + "=" * 68)
    print(f"CHẤM {n} bước click AndroidControl (nút-proxy = hộp chữ OCR conf≥{CONF})")
    print(f"  Trung vị hộp chữ / màn: {res['median_ocr_boxes_per_screen']}")
    print(f"  % bước có ≥1 NÚT NHIỄU trong dung sai ±{int(TOL*100)}%: {res['pct_step_with_ge1_confuser']:.1%}")
    print(f"  % bước có ≥2 hộp trong dung sai: {res['pct_step_with_ge2_box_in_tol']:.1%}")
    print(f"  Trung vị số nút nhiễu / bước: {res['median_confusers']}")
    print("=" * 68)
    print("So report/96 (MobileViews, có VH): 55.2% bước có nút cạnh trong 151px.")
    print("CHÚ Ý: OCR chỉ thấy nút-CÓ-CHỮ; icon thuần (+, ✓, mũi tên) KHÔNG đếm được")
    print("→ đây là CẬN DƯỚI của mật độ thật; mật độ thật ≥ số này.")
    json.dump(res, open(os.path.join(HERE, "ac_density_results.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Đã lưu ac_density_results.json")


if __name__ == "__main__":
    main()
