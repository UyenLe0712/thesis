# -*- coding: utf-8 -*-
"""
M4 (debate 2026-07-02): ĐO ĐỘ-PHỦ-NHÃN của View Hierarchy trên mv_multiapp.

Vì sao cần: matcher gắn cờ "bịa" khi tên nút AI viết KHÔNG khớp nút nào trong VH.
Nhưng VH có thể THIẾU nhãn (nút chỉ có icon, content_description rỗng, nhãn chung
"Button"/"ImageView"...). Nút thật mà khuyết-nhãn-VH sẽ bị tính OAN là bịa → thổi
tỉ-lệ-bịa. Script này đo: trong số nút ACTIONABLE, bao nhiêu % có nhãn TEXT dùng được.
→ báo tỉ-lệ-bịa dạng "CÓ ĐIỀU KIỆN recall-VH = X%" và loại nút nhãn-chung khỏi mẫu số.

KHÔNG sửa gì, chỉ IN số. Chạy:
  $env:PYTHONIOENCODING="utf-8"; python harness/dg1_vh_coverage.py
Nguồn dữ liệu: dataset_samples/mv_multiapp/*.viewhierarchy.json (81 màn/17 app đã lọc).
Đối chiếu: Chen et al. ICSE 2020 báo >77% app có nút thiếu nhãn.
"""
import os, sys, json, glob, re
from collections import defaultdict

HERE = os.path.dirname(__file__)
MV = os.path.join(HERE, "..", "dataset_samples", "mv_multiapp")
KEPT = os.path.join(HERE, "dg1_cache", "kept_screens.json")

# nhãn CHUNG / vô nghĩa → coi như KHÔNG có nhãn dùng được
GENERIC = {"button", "imagebutton", "imageview", "image", "icon", "view", "item",
           "textview", "layout", "container", "group", "row", "cell", "", "•", "…"}

def usable_label(label):
    """Nhãn dùng được = có chữ, không phải nhãn-chung, dài ≥2 ký tự chữ-số."""
    s = (label or "").strip()
    low = s.lower()
    if low in GENERIC:
        return False
    alnum = re.sub(r"[^0-9a-zA-ZÀ-ỹ]", "", s)   # giữ cả tiếng Việt có dấu
    return len(alnum) >= 2

def parse_actionable(vh_path):
    """Trả (tong_actionable, co_nhan_dung_duoc). Đếm CẢ nút actionable KHÔNG nhãn."""
    try:
        o = json.load(open(vh_path, encoding="utf-8"))
    except Exception:
        return (0, 0)
    views = o.get("views") or o.get("nodes") or []
    tot = good = 0
    for n in views:
        actionable = bool(n.get("clickable") or n.get("editable") or n.get("long_clickable"))
        if not actionable:
            continue
        tot += 1
        label = (n.get("text") or n.get("content_description") or "").strip()
        if usable_label(label):
            good += 1
    return (tot, good)

def screen_list():
    if os.path.exists(KEPT):
        names = json.load(open(KEPT, encoding="utf-8"))
        # kept_screens.json có thể là list tên hoặc list dict — chuẩn hoá về path
        out = []
        for x in names:
            nm = x if isinstance(x, str) else (x.get("screen") or x.get("name"))
            if nm:
                p = os.path.join(MV, nm + ".viewhierarchy.json")
                if os.path.exists(p):
                    out.append(p)
        if out:
            return out
    return sorted(glob.glob(os.path.join(MV, "*.viewhierarchy.json")))

def main():
    files = screen_list()
    if not files:
        print("Khong tim thay VH trong", MV); return
    by_app = defaultdict(lambda: [0, 0, 0])   # app -> [tong_act, co_nhan, so_man]
    tot_act = tot_good = 0
    for p in files:
        name = os.path.basename(p).split(".")[0]
        app = name.split("_")[0]
        a, g = parse_actionable(p)
        by_app[app][0] += a; by_app[app][1] += g; by_app[app][2] += 1
        tot_act += a; tot_good += g

    print("=" * 72)
    print(f"DO-PHU-NHAN VH | {len(files)} man / {len(by_app)} app")
    print("=" * 72)
    print(f"{'APP':22} {'#man':>5} {'#actionable':>12} {'co-nhan':>8} {'phu %':>7}")
    for app in sorted(by_app):
        a, g, m = by_app[app]
        cov = (g / a * 100) if a else 0.0
        print(f"{app:22} {m:5d} {a:12d} {g:8d} {cov:6.1f}%")
    overall = (tot_good / tot_act * 100) if tot_act else 0.0
    print("-" * 72)
    print(f"{'TONG':22} {len(files):5d} {tot_act:12d} {tot_good:8d} {overall:6.1f}%")
    print("=" * 72)
    print(f"DOC: do-phu-nhan chung = {overall:.1f}%. Nut KHUYET nhan-VH = {100-overall:.1f}% "
          f"-> se bi tinh OAN la bia neu AI goi dung. => bao ti-le-bia 'co dieu kien recall-VH', "
          f"loai nut nhan-chung khoi mau so. (Doi chieu Chen ICSE20 >77% app thieu nhan.)")

if __name__ == "__main__":
    main()
