# -*- coding: utf-8 -*-
"""
FREE · offline — CỔNG SỐNG CHẾT của trụ "mô tả trước, phát ngôn sau":
dựng thử nhãn tầng mô tả trên các bước chạm của dữ liệu dạy, đo xem bao nhiêu phần
trăm dùng được, hỏng ở khâu nào.

Bộ mô tả bốn trường: [vai trò | chữ hoặc hình | vị trí | dấu hiệu phân biệt]
  · vai trò   ← class_name của hộp a11y nhỏ nhất chứa điểm chạm
  · tên       ← text/content_description của hộp, không có thì chữ OCR nằm trong hộp
  · vị trí    ← tâm hộp quy về lưới 3x3
  · phân biệt ← đếm hộp khác cùng vai trò trên màn / trùng chữ

Đầu ra: phân tầng chất lượng + mẫu để soi tay. Nếu tỉ lệ "có tên dùng được" quá thấp
thì trụ không chạy được như thiết kế — phải biết TRƯỚC khi tiêu tiền.

Chạy: ~/.venvs/thesis/bin/python harness/descriptor_label_pilot.py
"""
import os, sys, json, random, re, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a11y_inventory as A11Y

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
OUT = os.path.join(HERE, "descriptor_label_results.json")
random.seed(20260729)

# class Android → vai trò tiếng thường; các class chứa chung chung coi là KHÔNG informative
ROLE = {
    "Button": "nút", "ImageButton": "nút hình", "ImageView": "hình/biểu tượng",
    "TextView": "chữ bấm được", "EditText": "ô nhập liệu", "CheckBox": "ô đánh dấu",
    "Switch": "công tắc", "RadioButton": "nút chọn", "Spinner": "hộp chọn",
    "SeekBar": "thanh kéo", "ToggleButton": "công tắc", "CheckedTextView": "mục chọn",
    "AutoCompleteTextView": "ô nhập liệu", "MultiAutoCompleteTextView": "ô nhập liệu",
}
GENERIC = {"RelativeLayout", "LinearLayout", "FrameLayout", "ViewGroup", "View",
           "RecyclerView", "ListView", "ScrollView", "ConstraintLayout", "CardView",
           "GridView", "ViewPager", "HorizontalScrollView", "WebView"}

COLS = ["bên trái", "giữa", "bên phải"]
ROWS = ["trên đỉnh", "giữa màn", "dưới đáy"]


def nodes_of(rel):
    """Mọi node hiển thị kèm (box, class, name)."""
    o = A11Y._load(A11Y.key_for(rel) or "")
    if not o:
        return []
    out = []
    for w in o:
        if w.get("window_type") == 3:
            continue
        for n in w.get("tree", []):
            if not n.get("is_visible_to_user"):
                continue
            b = n.get("bounds_in_screen") or {}
            x1, y1, x2, y2 = b.get("left", 0), b.get("top", 0), b.get("right", 0), b.get("bottom", 0)
            if x2 - x1 < 8 or y2 - y1 < 8:
                continue
            cls = (n.get("class_name") or "").split(".")[-1]
            name = (n.get("text") or "").strip() or (n.get("content_description") or "").strip()
            out.append(((x1, y1, x2, y2), cls, name))
    return out


def zone(box, w, h):
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    return f"{ROWS[min(int(cy / max(h,1) * 3), 2)]}, {COLS[min(int(cx / max(w,1) * 3), 2)]}"


def main():
    ocr = {}
    with open(os.path.join(ROOT, "ocr.jsonl"), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            ocr[r["image"]] = r
    recs = [json.loads(l) for l in open(os.path.join(ROOT, "train.jsonl"), encoding="utf-8")]
    taps = [r for r in recs if r["action"].get("action_type") == "click" and "x" in r["action"]]
    random.shuffle(taps)

    n = 0
    stats = collections.Counter()
    role_src = collections.Counter()
    samples = []
    for r in taps:
        rel = f"episode_{r['episode_id']}_screenshot_{r['step_id']}.png"
        nds = nodes_of(rel)
        if not nds:
            stats["khong_co_a11y"] += 1
            continue
        gx, gy = float(r["action"]["x"]), float(r["action"]["y"])
        w, h = r.get("w") or 1080, r.get("h") or 2400
        cont = [(b, c, nm) for b, c, nm in nds if b[0] <= gx <= b[2] and b[1] <= gy <= b[3]]
        if not cont:
            stats["cham_ngoai_moi_hop"] += 1
            continue
        n += 1
        box, cls, a11y_name = min(cont, key=lambda t: (t[0][2] - t[0][0]) * (t[0][3] - t[0][1]))
        area_share = (box[2] - box[0]) * (box[3] - box[1]) / (w * h)

        # vai trò
        informative = cls in ROLE
        role = ROLE.get(cls, cls)
        role_src["informative" if informative else ("generic" if cls in GENERIC else "khac")] += 1

        # tên: a11y trước, OCR sau
        name, src = None, None
        if a11y_name:
            name, src = a11y_name, "a11y"
        else:
            o = ocr.get(r["image"])
            if o:
                inside = [it for it in o["items"]
                          if box[0] <= it["cx"] <= box[2] and box[1] <= it["cy"] <= box[3]]
                if inside:
                    inside.sort(key=lambda it: (it["cy"], it["cx"]))
                    name = " ".join(it["text"] for it in inside[:2]).strip()
                    src = "ocr"
        # phân loại chất lượng tên
        if name and re.search(r"[A-Za-z0-9]{2,}", name):
            tier = "ten_ro"                     # có chữ đàng hoàng
        elif name:
            tier = "ky_hieu"                    # chỉ ký tự lẻ kiểu "+", "Q"
        else:
            tier = "khong_ten"                  # phải nhờ caption crop
        stats[tier] += 1
        if src:
            stats[f"nguon_{src}"] += 1
        if area_share > 0.5:
            stats["hop_qua_to"] += 1

        # phân biệt: hộp khác cùng class trên màn
        same_cls = sum(1 for b, c, _ in nds if c == cls) - 1

        if len(samples) < 24:
            samples.append({
                "goal": r["goal"][:60], "gold_cau": r["target_instruction"][:60],
                "vai_tro": role, "informative": informative,
                "ten": (name or "—")[:45], "nguon": src or "—", "tier": tier,
                "vi_tri": zone(box, w, h), "cung_loai": same_cls,
                "hop": [int(v) for v in box], "area_share": round(area_share, 2),
            })

    print("=" * 76)
    print(f"DỰNG THỬ NHÃN TẦNG MÔ TẢ — {n} bước chạm (a11y thiếu: {stats['khong_co_a11y']}, "
          f"chạm ngoài mọi hộp: {stats['cham_ngoai_moi_hop']})")
    print("=" * 76)
    print(f"  TÊN rõ (chữ đọc được)        : {stats['ten_ro']:4} = {stats['ten_ro']/n:.0%}"
          f"   (a11y: {stats['nguon_a11y']}, OCR: {stats['nguon_ocr']})")
    print(f"  chỉ ký hiệu lẻ ('+','Q'...)   : {stats['ky_hieu']:4} = {stats['ky_hieu']/n:.0%}")
    print(f"  KHÔNG tên → cần caption crop  : {stats['khong_ten']:4} = {stats['khong_ten']/n:.0%}")
    print("-" * 76)
    print(f"  vai trò informative (Button, EditText...): {role_src['informative']}/{n} = {role_src['informative']/n:.0%}")
    print(f"  vai trò generic (RelativeLayout...)       : {role_src['generic']}/{n} = {role_src['generic']/n:.0%}")
    print(f"  hộp chứa điểm chạm to hơn nửa màn (nghi lấy nhầm container): {stats['hop_qua_to']}/{n} = {stats['hop_qua_to']/n:.0%}")
    print("=" * 76)
    print("MẪU ĐỂ SOI TAY (24 ca ngẫu nhiên):")
    for s in samples:
        flag = "✓" if s["tier"] == "ten_ro" else ("~" if s["tier"] == "ky_hieu" else "✗")
        print(f"  {flag} [{s['vai_tro'][:14]:14}|{s['ten']:45}|{s['vi_tri']:20}] gold: {s['gold_cau']}")
    json.dump({"n": n, "stats": dict(stats), "role": dict(role_src), "samples": samples},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nĐã lưu", OUT)


if __name__ == "__main__":
    main()
