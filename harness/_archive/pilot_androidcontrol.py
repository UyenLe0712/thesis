# -*- coding: utf-8 -*-
"""
PILOT AndroidControl (report/78 cổng go/no-go) — trục ĐÚNG có khả thi không?
Đo: (1) khung toạ độ gold khớp ảnh? (2) K-map: tỉ lệ gold-click lấy được TÊN nút.
Vì HF mirror KHÔNG có accessibility-tree → dùng OCR-tại-điểm làm CẬN DƯỚI của map-rate
(a11y thật sẽ cao hơn vì có bbox phần tử + content_description, nhưng không tải nhẹ được).

Chạy: ~/.venvs/thesis/bin/python harness/pilot_androidcontrol.py
"""
import json, io, os, re
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
from datasets import load_dataset

N_TARGET = 100
OUT = os.path.join(os.path.dirname(__file__), "pilot_ac_results.json")
IMGDIR = os.path.join(os.path.dirname(__file__), "dg1_cache", "ac_pilot_imgs")
os.makedirs(IMGDIR, exist_ok=True)

def get_action(jj):
    """Trả (action_type, x, y) từ field json của ckg (assistant message chứa FUNCTIONCALL)."""
    if isinstance(jj, str):
        jj = json.loads(jj)
    txt = ""
    for m in jj.get("messages", []):
        if m.get("role") == "assistant":
            txt = m.get("content", "")
    name = None; x = y = None
    mn = re.search(r'"name":\s*"(\w+)"', txt)
    if mn: name = mn.group(1)
    mx = re.search(r'"x":\s*(\d+)', txt); my = re.search(r'"y":\s*(\d+)', txt)
    if mx and my: x, y = int(mx.group(1)), int(my.group(1))
    sw = jj.get("screenshot_width") or jj.get("screen_w") or 1080
    sh = jj.get("screenshot_height") or jj.get("screen_h") or 2400
    return name, x, y, sw, sh

def to_pil(png):
    if isinstance(png, Image.Image):
        return png
    if isinstance(png, dict) and "bytes" in png:
        return Image.open(io.BytesIO(png["bytes"]))
    if isinstance(png, (bytes, bytearray)):
        return Image.open(io.BytesIO(png))
    return None

def main():
    print("Streaming ckg/AndroidControlParsedWithImages-20k-TESTONLY ...")
    ds = load_dataset("ckg/AndroidControlParsedWithImages-20k-TESTONLY", split="train", streaming=True)
    ocr = RapidOCR()
    steps = []
    scanned = 0
    for ex in ds:
        scanned += 1
        try:
            name, x, y, sw, sh = get_action(ex["json"])
        except Exception:
            continue
        if name not in ("click", "long_press") or x is None:
            continue
        img = to_pil(ex.get("png"))
        if img is None:
            continue
        W, H = img.size
        gx, gy = x * W / sw, y * H / sh
        res, _ = ocr(img.convert("RGB"))
        hit_strict = None; near = None; bestd = 1e9; hit_relax = None
        row_tol = 0.025 * H
        for box, txt, conf in (res or []):
            xs = [p[0] for p in box]; ys = [p[1] for p in box]
            l, t, r, b = min(xs), min(ys), max(xs), max(ys)
            cx, cy = (l + r) / 2, (t + b) / 2
            if l <= gx <= r and t <= gy <= b:
                hit_strict = txt
            # relaxed: cùng hàng (|dy| nhỏ) và điểm nằm trong dải mở rộng ngang
            if abs(cy - gy) <= max(row_tol, (b - t)) and (l - 0.06 * W) <= gx <= (r + 0.06 * W):
                if hit_relax is None:
                    hit_relax = txt
            d = abs(cx - gx) + abs(cy - gy)
            if d < bestd:
                bestd, near = d, txt
        steps.append({"action": name, "gx": round(gx), "gy": round(gy), "imgWH": [W, H],
                      "hit_strict": hit_strict, "hit_relax": hit_relax or hit_strict, "nearest": near})
        if len(steps) >= N_TARGET:
            break

    n = len(steps)
    st = sum(1 for s in steps if s["hit_strict"])
    rl = sum(1 for s in steps if s["hit_relax"])
    print("=" * 78)
    print(f"PILOT AndroidControl — K-map qua OCR-tại-điểm | {n} bước click/long_press (quét {scanned})")
    print("=" * 78)
    print(f"  Map được TÊN (strict: điểm nằm trong hộp chữ):   {st}/{n} = {100*st/n:.1f}%")
    print(f"  Map được TÊN (relaxed: chữ cùng hàng, gần điểm):  {rl}/{n} = {100*rl/n:.1f}%")
    print(f"  → CẬN DƯỚI map-rate = {100*st/n:.1f}% ; a11y-tree thật (bbox phần tử + content_desc) sẽ CAO HƠN")
    print(f"  → ~{100-100*rl/n:.0f}% gold-click KHÔNG có chữ gần (icon thuần) = sàn không map được, khớp K1/OCR")
    print()
    print("  Ví dụ (gold@điểm -> tên OCR strict | relaxed):")
    for s in steps[:20]:
        print(f"    @({s['gx']},{s['gy']}) img{s['imgWH']} -> strict:{s['hit_strict']!r}  relax:{s['hit_relax']!r}")
    json.dump({"n": n, "scanned": scanned, "strict": st, "relax": rl,
               "map_lower_bound_pct": 100*st/n, "relax_pct": 100*rl/n, "steps": steps},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nĐã lưu:", OUT)

if __name__ == "__main__":
    main()
