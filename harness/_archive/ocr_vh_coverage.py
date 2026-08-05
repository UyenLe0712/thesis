# -*- coding: utf-8 -*-
"""
VIỆC OCR (report/72 / Vòng C report/67) — đo độ phủ nhãn NÚT: VH-only vs VH+OCR trên 127 màn.
Trả lời: OCR bù được bao nhiêu nút actionable mà VH bỏ nhãn (nguồn KẾT OAN mà K2 tìm ra).

NGƯỠNG ĐÃ KHOÁ TRƯỚC KHI CHẠY (pre-register):
  - Mẫu số = phần tử ACTIONABLE (clickable ∨ editable ∨ long_clickable), có bbox hợp lệ.
  - Nút "có nhãn VH" = text ∨ content_description khác rỗng.
  - Gán OCR: một hộp chữ OCR thuộc về nút nếu TÂM hộp OCR nằm TRONG bbox nút (containment),
    và độ tin OCR ≥ 0.5, và chuỗi OCR có ≥1 ký tự chữ-số.
  - Nút "có nhãn VH+OCR" = có nhãn VH HOẶC được gán ≥1 hộp OCR hợp lệ.
  - Khung toạ độ: bbox VH và hộp OCR đều theo PIXEL ảnh thật (PIL). Có kiểm sanity.

Chạy: ~/.venvs/thesis/bin/python harness/ocr_vh_coverage.py
"""
import json, os, glob, re
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "dataset_samples", "mv_multiapp")
KEPT = os.path.join(HERE, "kept_screens_final.json")
OCR_CACHE = os.path.join(HERE, "dg1_cache", "ocr_cache.json")
CONF_MIN = 0.5

_ocr = None
def get_ocr():
    global _ocr
    if _ocr is None:
        _ocr = RapidOCR()
    return _ocr

def load_ocr_cache():
    try:
        return json.load(open(OCR_CACHE, encoding="utf-8"))
    except Exception:
        return {}

def run_ocr(img_path, cache):
    key = os.path.basename(img_path)
    if key in cache:
        return cache[key]
    res, _ = get_ocr()(img_path)
    boxes = []
    for r in (res or []):
        box, txt, conf = r
        xs = [p[0] for p in box]; ys = [p[1] for p in box]
        cx, cy = sum(xs) / 4.0, sum(ys) / 4.0
        boxes.append({"text": txt, "conf": float(conf), "cx": cx, "cy": cy,
                      "bbox": [min(xs), min(ys), max(xs), max(ys)]})
    cache[key] = boxes
    return boxes

def vh_elems(vh_path):
    o = json.load(open(vh_path, encoding="utf-8"))
    img = vh_path.replace(".viewhierarchy.json", ".jpg")
    W, H = Image.open(img).size
    els = []
    for n in o.get("views", []):
        b = n.get("bounds")
        if not b:
            continue
        (l, t), (r, bot) = b
        if r <= l or bot <= t:
            continue
        text = (n.get("text") or "").strip()
        cd = (n.get("content_description") or "").strip()
        act = bool(n.get("clickable") or n.get("editable") or n.get("long_clickable"))
        els.append({"bbox": (l, t, r, bot), "vh_label": text or cd, "actionable": act})
    return els, W, H, img

def has_alnum(s):
    return bool(re.search(r"[0-9A-Za-zÀ-ỹ]", s or ""))

def center_in(cx, cy, bbox):
    l, t, r, b = bbox
    return l <= cx <= r and t <= cy <= b

def main():
    kept = set(json.load(open(KEPT, encoding="utf-8"))["kept"])
    files = sorted(f for f in glob.glob(DATA + "/*.viewhierarchy.json")
                   if os.path.basename(f).split(".")[0] in kept)
    cache = load_ocr_cache()

    tot_act = 0; vh_lab = 0; vhocr_lab = 0
    ocr_added_examples = []
    per_screen = []          # (recall_vh, recall_vhocr)
    sane_ocr_in_any = 0; sane_ocr_total = 0
    W_over = 0

    for i, f in enumerate(files):
        els, W, H, img = vh_elems(f)
        boxes = run_ocr(img, cache)
        # sanity khung toạ độ: hộp OCR có rơi trong ẢNH + trong nút nào không
        for bx in boxes:
            sane_ocr_total += 1
            if bx["cx"] > W or bx["cy"] > H:
                W_over += 1
        acts = [e for e in els if e["actionable"]]
        n_act = len(acts) or 0
        s_vh = s_vhocr = 0
        for e in acts:
            has_vh = bool(e["vh_label"])
            ocr_hit = None
            for bx in boxes:
                if bx["conf"] >= CONF_MIN and has_alnum(bx["text"]) and center_in(bx["cx"], bx["cy"], e["bbox"]):
                    ocr_hit = bx["text"]; break
            if ocr_hit is not None:
                sane_ocr_in_any += 1
            if has_vh:
                s_vh += 1; s_vhocr += 1
            elif ocr_hit is not None:
                s_vhocr += 1
                if len(ocr_added_examples) < 40:
                    ocr_added_examples.append((os.path.basename(img).split(".")[0], ocr_hit))
        tot_act += n_act; vh_lab += s_vh; vhocr_lab += s_vhocr
        if n_act:
            per_screen.append((s_vh / n_act, s_vhocr / n_act))

    rec_vh = vh_lab / tot_act
    rec_vhocr = vhocr_lab / tot_act
    macro_vh = sum(a for a, _ in per_screen) / len(per_screen)
    macro_vhocr = sum(b for _, b in per_screen) / len(per_screen)

    print("=" * 80)
    print("VIỆC OCR — ĐỘ PHỦ NHÃN NÚT: VH-only vs VH+OCR | %d màn, %d nút actionable" % (len(files), tot_act))
    print("=" * 80)
    print("Kiểm khung toạ độ (sanity): %d/%d hộp OCR rơi TRONG một nút actionable; %d hộp vượt kích thước ảnh"
          % (sane_ocr_in_any, sane_ocr_total, W_over))
    print()
    print("  ĐỘ PHỦ NHÃN (micro, gộp mọi nút):")
    print("    VH-only :  %d/%d = %.1f%%" % (vh_lab, tot_act, rec_vh * 100))
    print("    VH+OCR  :  %d/%d = %.1f%%  (Δ = +%.1f điểm)" % (vhocr_lab, tot_act, rec_vhocr * 100, (rec_vhocr - rec_vh) * 100))
    print("    → OCR bù thêm %d nút (%.1f%% số nút bị VH bỏ nhãn được OCR cứu)"
          % (vhocr_lab - vh_lab, (vhocr_lab - vh_lab) / (tot_act - vh_lab) * 100 if tot_act - vh_lab else 0))
    print()
    print("  ĐỘ PHỦ NHÃN (macro theo màn):")
    print("    VH-only :  %.1f%%" % (macro_vh * 100))
    print("    VH+OCR  :  %.1f%%  (Δ = +%.1f điểm)" % (macro_vhocr * 100, (macro_vhocr - macro_vh) * 100))
    print()
    print("  Ví dụ nút VH bỏ nhãn được OCR cứu (chuỗi OCR đọc ra):")
    for sid, txt in ocr_added_examples[:25]:
        print("    %-22s '%s'" % (sid, txt))

    json.dump(cache, open(OCR_CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    out = os.path.join(HERE, "ocr_coverage_results.json")
    json.dump({"n_screens": len(files), "n_actionable": tot_act,
               "recall_vh_micro": rec_vh, "recall_vhocr_micro": rec_vhocr,
               "recall_vh_macro": macro_vh, "recall_vhocr_macro": macro_vhocr,
               "ocr_added": vhocr_lab - vh_lab, "conf_min": CONF_MIN,
               "sanity_ocr_in_element": [sane_ocr_in_any, sane_ocr_total, W_over],
               "examples": ocr_added_examples}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nĐã lưu:", out)

if __name__ == "__main__":
    main()
