# -*- coding: utf-8 -*-
"""
FREE · offline — độ nhạy của bộ tứ (trần/sàn/chênh) theo CÁCH XỬ LÝ danh sách nút.

Vì sao cần: con số chênh từng được báo là 13.2 rồi 32.9, khác nhau chỉ vì cách xử lý danh
sách nút. Thay vì trưng một con số kèm một lời giải thích, ở đây quét nhiều cách xử lý và
báo cả dải — nếu chênh sống sót qua mọi cách thì kết luận mới vững.

Sáu cách:
  1. đĩa dung sai (không dùng danh sách nút)
  2. nút gần nhất, danh sách = tâm hộp thô (không xử lý gì)
  3. nút gần nhất, tâm hộp, khử trùng bán kính 12dp / 24dp / 32dp
  4. nút gần nhất, dùng HỘP, loại hộp chứa điểm gold  ← đúng bản chất nhất
  5. nút gần nhất, dùng hộp, chỉ giữ hộp bộ dò tin cậy cao
  6. danh sách nút lấy từ OCR (nguồn hoàn toàn khác) để đối chiếu

Chạy: ~/.venvs/thesis/bin/python harness/voronoi_sensitivity.py
"""
import os, sys, re, json, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metric_exec as ME
import omni_boxes as OB
import a11y_inventory as A11Y

HERE = os.path.dirname(os.path.abspath(__file__))
HF = os.path.expanduser("~/.cache/huggingface/hub/datasets--wangyuanlei--android_control_test/snapshots")
BOXDIR = os.path.join(HERE, "dg1_cache", "omni_box")
OCRDIR = os.path.join(HERE, "dg1_cache", "ac_ocr")
CEIL = json.load(open(os.path.join(HERE, "dg1_cache", "ground_pilot", "pred.json"), encoding="utf-8"))
FLOOR = json.load(open(os.path.join(HERE, "dg1_cache", "ground_floor", "pred.json"), encoding="utf-8"))
OUT = os.path.join(HERE, "voronoi_sensitivity_results.json")
TOL = 0.14


def find_ep(eid):
    h = glob.glob(os.path.join(HF, "*", "test_output_json", "*", f"episode_{eid}.json"))
    return h[0] if h else None


def gold_of(rel):
    m = re.search(r"episode_(\d+)_screenshot_(\d+)\.png", rel)
    if not m:
        return None
    ep = find_ep(int(m.group(1)))
    if not ep:
        return None
    o = json.load(open(ep, encoding="utf-8"))
    a = o.get("actions") or []
    si = int(m.group(2))
    if si >= len(a) or "x" not in a[si]:
        return None
    return float(a[si]["x"]), float(a[si]["y"])


def boxes_of(rel):
    p = os.path.join(BOXDIR, OB.key_of(rel))
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


def ocr_centers(rel):
    p = os.path.join(OCRDIR, re.sub(r"[^\w]", "_", os.path.basename(rel)) + ".json")
    if not os.path.exists(p):
        return []
    return [(b["cx"], b["cy"]) for b in json.load(open(p, encoding="utf-8"))]


def centers(bs):
    return [((b[0] + b[2]) / 2, (b[1] + b[3]) / 2) for b in bs]


def area(b):
    return (b[2] - b[0]) * (b[3] - b[1])


# ---- các cách chấm ----
def m_disk(pt, g, rel, wh):
    return ME.hit_disk(pt, g, wh, TOL)


def m_raw_centers(pt, g, rel, wh):
    inv = [g] + centers(boxes_of(rel))
    if not ME.hit_disk(pt, g, wh, TOL):
        return False
    dg = ME._dist(pt, g)
    return all(ME._dist(pt, b) >= dg for b in inv if ME._dist(b, g) > 1e-6)


def m_dedupe(dp):
    def f(pt, g, rel, wh):
        old = ME.min_sep_px
        ME.min_sep_px = lambda w: dp * (w[0] / 411.0)
        try:
            return ME.hit_voronoi(pt, g, [g] + centers(boxes_of(rel)), wh, TOL)
        finally:
            ME.min_sep_px = old
    return f


def m_boxes(pt, g, rel, wh):
    return ME.hit_nearest_box(pt, g, boxes_of(rel), wh, TOL)


def m_boxes_big(pt, g, rel, wh):
    bs = [b for b in boxes_of(rel) if area(b) >= 0.002 * wh[0] * wh[1]]
    return ME.hit_nearest_box(pt, g, bs, wh, TOL)


def m_a11y(pt, g, rel, wh):
    return ME.hit_nearest_box(pt, g, A11Y.elements(rel), wh, TOL)


def m_a11y_big(pt, g, rel, wh):
    bs = [b for b in A11Y.elements(rel) if area(b) >= 0.002 * wh[0] * wh[1]]
    return ME.hit_nearest_box(pt, g, bs, wh, TOL)


def m_a11y_omni(pt, g, rel, wh):
    return ME.hit_nearest_box(pt, g, A11Y.elements(rel) + boxes_of(rel), wh, TOL)


def m_ocr(pt, g, rel, wh):
    return ME.hit_voronoi(pt, g, [g] + ocr_centers(rel), wh, TOL)


METHODS = [
    ("đĩa dung sai", m_disk),
    ("tâm hộp, không xử lý", m_raw_centers),
    ("tâm hộp, gộp 12dp", m_dedupe(12)),
    ("tâm hộp, gộp 24dp", m_dedupe(24)),
    ("tâm hộp, gộp 32dp", m_dedupe(32)),
    ("HỘP, loại hộp chứa gold", m_boxes),
    ("HỘP lớn, loại hộp chứa gold", m_boxes_big),
    ("tâm OCR, gộp 24dp", m_ocr),
    ("CÂY TRỢ NĂNG, loại hộp chứa gold", m_a11y),
    ("cây trợ năng, chỉ hộp lớn", m_a11y_big),
    ("cây trợ năng + bộ dò hình", m_a11y_omni),
]


def rate(pred, fn):
    ok = n = 0
    for rel, p in pred.items():
        if p.get("px") is None:
            continue
        g = gold_of(rel)
        if not g:
            continue
        n += 1
        if fn((p["px"], p["py"]), g, rel, (p["w"], p["h"])):
            ok += 1
    return ok / max(n, 1), n


def main():
    rows = []
    print("=" * 74)
    print(f"{'cách chấm':30}{'trần':>9}{'sàn':>9}{'chênh':>10}")
    print("=" * 74)
    for name, fn in METHODS:
        c, n = rate(CEIL, fn)
        f, _ = rate(FLOOR, fn)
        rows.append({"method": name, "ceil": c, "floor": f, "range": c - f, "n": n})
        print(f"{name:30}{c:>8.1%}{f:>9.1%}{c-f:>+10.1%}")
    print("=" * 74)
    rs = [r["range"] for r in rows[1:]]      # bỏ dòng đĩa (cách chấm dễ dãi)
    print(f"Chênh dưới MỌI cách chấm chặt: thấp nhất {min(rs):.1%} · cao nhất {max(rs):.1%}")
    print(f"Khoảng tin cậy nhị thức cho một tỉ lệ ~33% với n={rows[0]['n']}: khoảng ±10.6 điểm")
    json.dump({"rows": rows, "min_range": min(rs), "max_range": max(rs)},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Đã lưu", OUT)


if __name__ == "__main__":
    main()
