# -*- coding: utf-8 -*-
"""
FREE · offline — DỰNG NHÃN THẬT cho tầng khai báo (bản chốt, thay bản pilot).

Khác bản pilot `descriptor_label_pilot.py` ba chỗ, đúng như report/106 mục 10 yêu cầu:
  1. Ô vị trí là TOẠ ĐỘ `<point>x,y</point>` lấy từ điểm chạm thật, không còn lưới 3x3.
  2. Ô phân biệt tính đủ hai vế: số phần tử cùng vai trò VÀ có trùng tên hay không.
  3. Sinh luôn chuỗi `<desc>…</desc>` ghép sẵn để nạp thẳng vào dữ liệu dạy,
     kèm một bản khai báo GIẢ lấy từ nút hàng xóm (dùng cho nhánh mức 2 / S3).

HỆ TOẠ ĐỘ — quyết định kỹ thuật, ghi lại để khỏi tranh cãi về sau:
  Ảnh bị co lại trước khi vào mô hình (Qwen2.5-VL co động theo bội số 28), nên toạ độ
  pixel của ảnh gốc không có nghĩa với mô hình trừ khi báo kèm kích thước gốc. Vì vậy
  mặc định quy về lưới [0,1000] theo chiều rộng/cao — không phụ thuộc độ phân giải.
  Muốn dùng pixel thô thì chạy với --abs (vẫn lưu cả hai trong tệp kết quả).

Chạy:
  ~/.venvs/thesis/bin/python harness/descriptor_label_build.py            # cả lát 1.697 bước
  ~/.venvs/thesis/bin/python harness/descriptor_label_build.py --limit 200
"""
import os, sys, json, re, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a11y_inventory as A11Y

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
OUT_JSONL = os.path.join(HERE, "dg1_cache", "train_ac", "descriptors.jsonl")
OUT_STATS = os.path.join(HERE, "descriptor_build_stats.json")

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


def overlapped(b1, b2):
    """True nếu hai hộp là một phần tử lồng nhau (cha chứa con) chứ không phải hai nút riêng.

    Cây trợ năng Android lồng nhiều tầng: một ViewGroup bọc một TextView, cả hai cùng
    mang chữ "CATEGORIES". Nếu không lọc, đếm trùng tên sẽ thổi phồng và khai báo giả
    lại trỏ vào chính nút đích. Luật: chứa nhau, hoặc chồng nhau quá nửa diện tích nhỏ.
    """
    ix = max(0, min(b1[2], b2[2]) - max(b1[0], b2[0]))
    iy = max(0, min(b1[3], b2[3]) - max(b1[1], b2[1]))
    inter = ix * iy
    if inter <= 0:
        return False
    a1 = (b1[2] - b1[0]) * (b1[3] - b1[1])
    a2 = (b2[2] - b2[0]) * (b2[3] - b2[1])
    return inter / max(1, min(a1, a2)) > 0.5


def nodes_of(rel):
    """Mọi phần tử hiển thị của màn: (hộp, class, tên)."""
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


def clean_a11y(name):
    """Làm sạch nhãn trợ năng, trả None nếu nhãn không dùng được làm TÊN.

    Đo trên 285 nhãn tại nút đích: 14,7% là rác. Bốn kiểu hay gặp, đều không phải
    tên mà người dùng nhìn thấy hay gọi ra được:
      · định danh trong mã nguồn: 'plp_category_button', 'viewer.button.edit'
      · phần đuôi do bộ đọc màn thêm vào: 'Search, Tab 2 of 3', 'Every Year. Button'
      · nhãn rỗng nghĩa: 'No label specified', tiền tố 'null, '
      · cả một câu thay vì một tên: 'Save as reminder and go back to home page.'
    Cắt tại ký tự xuống dòng TRƯỚC khi xét độ dài, vì nhiều nhãn có dạng
    'Basic\nI have a modest vocabulary...' mà dòng đầu chính là tên tử tế.
    """
    if not name:
        return None
    t = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", name).strip()
    t = t.split("\n")[0].strip()
    t = re.sub(r"^null,\s*", "", t, flags=re.I)
    t = re.sub(r"(,\s*Tab \d+ of \d+|[,.]\s*Button)$", "", t, flags=re.I).strip()
    if not t or len(t) > 40:
        return None
    if t.lower() in ("no label specified", "null", "unlabeled"):
        return None
    if re.fullmatch(r"[a-z0-9]+([._][a-z0-9]+)+", t) or re.fullmatch(r"[a-z]+_[a-z0-9_]+", t):
        return None                      # định danh mã nguồn
    if re.fullmatch(r"\d{5,}", t):
        return None                      # chuỗi số dài, thường là id
    if not re.search(r"[A-Za-z0-9]", t):
        return None
    return t


def name_of(box, a11y_name, ocr_rec, area_share=0.0):
    """Tên phần tử. Thứ tự: nhãn trợ năng ĐÃ QUA CỔNG HỢP LỆ, không qua thì tới OCR.

    Vòng phản biện 5/8 đã bác phương án đảo thứ tự sang OCR-trước. Lý do bằng số: trong
    72 ca hai nguồn khác nhau, bóc 32 ca mà chuỗi OCR chỉ là con số có sẵn trong mục tiêu
    (bộ chọn ngày giờ, bàn phím số) thì còn 40 ca lõi — OCR thắng 12, trợ năng thắng 3.
    Nhưng 11/12 ca OCR thắng là vì nhãn trợ năng RÁC. Đối đầu sạch với sạch: 1 ca OCR
    thắng, 3 ca trợ năng thắng. Tức ưu thế đo được của OCR là ưu thế của việc LỌC RÁC,
    không phải của thứ tự ưu tiên. Nên lọc rác, giữ thứ tự.

    Hai cổng, đều tiên nghiệm và đo được:
      · nhãn trợ năng phải qua clean_a11y
      · chữ OCR chỉ dùng khi hộp không quá to (>25% màn thì hộp là khung ngoài, chữ bên
        trong là của phần tử khác: đo được 25 ca như vậy, 0/25 khớp câu chuẩn)
    """
    clean = clean_a11y(a11y_name)
    if clean:
        return clean, "a11y"
    if ocr_rec and area_share <= 0.25:
        inside = [it for it in ocr_rec["items"]
                  if box[0] <= it["cx"] <= box[2] and box[1] <= it["cy"] <= box[3]]
        if inside:
            inside.sort(key=lambda it: (it["cy"], it["cx"]))
            # chỉ nối hai mục khi chúng CÙNG DÒNG; khác dòng mà nối sẽ đẻ ra chuỗi không
            # tồn tại trên màn ('= adidas Gmail', 'Showresults')
            keep = [inside[0]]
            if len(inside) > 1:
                h = max(box[3] - box[1], 1)
                if abs(inside[1]["cy"] - inside[0]["cy"]) < 0.5 * h:
                    keep.append(inside[1])
            t = " ".join(it["text"] for it in keep).strip()
            if re.search(r"[A-Za-z0-9]{2,}", t):
                return t, "ocr"
            return t or None, ("ocr" if t else None)
    return None, ("a11y_rejected" if a11y_name else None)


def tier_of(name):
    if name and re.search(r"[A-Za-z0-9]{2,}", name):
        return "ten_ro"
    if name:
        return "ky_hieu"
    return "khong_ten"


SCREEN_AREA = [1080 * 2400]      # đặt lại theo từng màn trong main()


def distinguish(box, cls, name, nds, ocr_rec):
    """Ô thứ tư: nói phần tử này khác gì các phần tử quanh nó.

    Hai vế, tính bằng luật, không đoán:
      · bao nhiêu phần tử cùng vai trò trên màn
      · có phần tử nào KHÁC trùng tên không (đây mới là ca mơ hồ thật)
    """
    same_role = [b for b, c, _ in nds if c == cls and b != box and not overlapped(b, box)]
    dup = 0
    if name:
        low = name.strip().lower()
        for b, c, nm in nds:
            if b == box or overlapped(b, box):
                continue
            a2 = (b[2] - b[0]) * (b[3] - b[1]) / max(SCREEN_AREA[0], 1)
            n2, _ = name_of(b, nm, ocr_rec, a2)
            if n2 and n2.strip().lower() == low:
                dup += 1
    if dup:
        return f"trùng tên với {dup} phần tử khác trên màn", dup, len(same_role)
    rname = ROLE.get(cls) or ("mục" if cls in GENERIC else "phần tử")
    k = len(same_role)
    if k == 0:
        return f"{rname} duy nhất trên màn", 0, 0
    # Đếm chính xác chỉ có nghĩa khi ít. "1 trong 118" là con số vô dụng — với màn dày
    # phần tử cùng loại thì thứ mô hình cần biết là "phải nói cho thật cụ thể", không
    # phải con số. Nên chia ba mức thay vì in số thô.
    if k <= 8:
        return f"1 trong {k+1} phần tử cùng loại", 0, k
    return "màn có nhiều phần tử cùng loại", 0, k


def nearest_other(box, cls, nds):
    """Phần tử cùng vai trò gần nhất — dùng làm khai báo GIẢ cho nhánh mức 2."""
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    best, bd = None, None
    for b, c, nm in nds:
        if b == box or c != cls or overlapped(b, box):
            continue
        d = ((b[0] + b[2]) / 2 - cx) ** 2 + ((b[1] + b[3]) / 2 - cy) ** 2
        if bd is None or d < bd:
            best, bd = (b, c, nm), d
    return best, (bd ** 0.5 if bd is not None else None)


def desc_str(role, name, pt, hint):
    return f"<desc>{role} | {name or '(không tên)'} | <point>{pt[0]},{pt[1]}</point> | {hint}</desc>"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="chỉ chạy N bước đầu (0 = tất cả)")
    ap.add_argument("--abs", action="store_true", help="dùng pixel thô thay vì lưới [0,1000]")
    args = ap.parse_args()

    ocr = {}
    with open(os.path.join(ROOT, "ocr.jsonl"), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            ocr[r["image"]] = r
    recs = [json.loads(l) for l in open(os.path.join(ROOT, "train.jsonl"), encoding="utf-8")]
    taps = [r for r in recs if r["action"].get("action_type") in ("click", "long_press")
            and "x" in r["action"]]
    if args.limit:
        taps = taps[:args.limit]

    st = collections.Counter()
    rows = []
    for r in taps:
        rel = f"episode_{r['episode_id']}_screenshot_{r['step_id']}.png"
        nds = nodes_of(rel)
        if not nds:
            st["bo_khong_co_a11y"] += 1
            continue
        gx, gy = float(r["action"]["x"]), float(r["action"]["y"])
        w, h = r.get("w") or 1080, r.get("h") or 2400
        cont = [(b, c, nm) for b, c, nm in nds if b[0] <= gx <= b[2] and b[1] <= gy <= b[3]]
        if not cont:
            st["bo_cham_ngoai_hop"] += 1
            continue

        box, cls, a11y_name = min(cont, key=lambda t: (t[0][2] - t[0][0]) * (t[0][3] - t[0][1]))
        area_share = (box[2] - box[0]) * (box[3] - box[1]) / (w * h)
        ocr_rec = ocr.get(r["image"])

        role = ROLE.get(cls) or ("mục" if cls in GENERIC else "phần tử")
        st["vai_tro_ro"] += 1 if cls in ROLE else 0
        st["vai_tro_generic"] += 1 if cls in GENERIC else 0

        SCREEN_AREA[0] = w * h
        name, src = name_of(box, a11y_name, ocr_rec, area_share)
        tier = tier_of(name)
        st[tier] += 1
        if src:
            st[f"nguon_{src}"] += 1
        if area_share > 0.25:
            st["hop_qua_to"] += 1
        if src == "a11y_rejected":
            st["a11y_bi_loai"] += 1

        hint, dup, same_role = distinguish(box, cls, name, nds, ocr_rec)
        if dup:
            st["co_trung_ten"] += 1

        pt_abs = (int(round(gx)), int(round(gy)))
        pt_norm = (int(round(gx / max(w, 1) * 1000)), int(round(gy / max(h, 1) * 1000)))
        pt = pt_abs if args.abs else pt_norm

        # khai báo GIẢ: nút cùng vai trò gần nhất (nhánh mức 2 cần)
        neg, neg_dist = nearest_other(box, cls, nds)
        neg_desc = None
        if neg:
            nb, ncls, nnm = neg
            nshare = (nb[2] - nb[0]) * (nb[3] - nb[1]) / max(w * h, 1)
            nname, _ = name_of(nb, nnm, ocr_rec, nshare)
            ncx = int(round((nb[0] + nb[2]) / 2))
            ncy = int(round((nb[1] + nb[3]) / 2))
            npt = (ncx, ncy) if args.abs else (int(round(ncx / max(w, 1) * 1000)),
                                               int(round(ncy / max(h, 1) * 1000)))
            nrole = ROLE.get(ncls) or ("mục" if ncls in GENERIC else "phần tử")
            neg_desc = desc_str(nrole, nname, npt, "phần tử hàng xóm")
            st["co_hang_xom"] += 1

        rows.append({
            "episode_id": r["episode_id"], "step_id": r["step_id"], "image": r["image"],
            "goal": r["goal"], "target_instruction": r["target_instruction"],
            "desc": desc_str(role, name, pt, hint),
            "desc_neg": neg_desc,
            "role": role, "role_class": cls, "name": name, "name_src": src, "tier": tier,
            "a11y_raw": a11y_name or None,
            "hint": hint, "dup_name": dup, "same_role": same_role,
            "point_abs": pt_abs, "point_norm": pt_norm,
            "box": [int(v) for v in box], "area_share": round(area_share, 3),
            "neighbor_dist_px": round(neg_dist, 1) if neg_dist else None,
        })

    n = len(rows)
    if not n:
        print("Không dựng được nhãn nào — kiểm lại dữ liệu nguồn.")
        return
    with open(OUT_JSONL, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print("=" * 78)
    print(f"DỰNG NHÃN TẦNG KHAI BÁO — {n} bước chạm dựng được"
          f"  (bỏ: {st['bo_khong_co_a11y']} thiếu cây trợ năng, {st['bo_cham_ngoai_hop']} chạm ngoài mọi hộp)")
    print(f"Hệ toạ độ: {'pixel thô' if args.abs else 'lưới [0,1000]'}")
    print("=" * 78)
    print(f"  tên rõ                    : {st['ten_ro']:5} = {st['ten_ro']/n:5.1%}"
          f"   (cây trợ năng {st['nguon_a11y']}, OCR {st['nguon_ocr']})")
    print(f"  chỉ ký hiệu lẻ            : {st['ky_hieu']:5} = {st['ky_hieu']/n:5.1%}")
    print(f"  không tên → để trống      : {st['khong_ten']:5} = {st['khong_ten']/n:5.1%}")
    print("-" * 78)
    print(f"  vai trò rõ                : {st['vai_tro_ro']:5} = {st['vai_tro_ro']/n:5.1%}")
    print(f"  có phần tử TRÙNG TÊN      : {st['co_trung_ten']:5} = {st['co_trung_ten']/n:5.1%}   ← ca mơ hồ thật")
    print(f"  có hàng xóm cùng vai trò  : {st['co_hang_xom']:5} = {st['co_hang_xom']/n:5.1%}   ← dựng được khai báo giả")
    print(f"  hộp to hơn nửa màn        : {st['hop_qua_to']:5} = {st['hop_qua_to']/n:5.1%}   ← nghi lấy nhầm khung ngoài")
    print("=" * 78)
    print("BA NHÃN ĐẦU, xem thử:")
    for row in rows[:3]:
        print(f"\n  {row['desc']}")
        print(f"  {row['target_instruction']}")
        if row["desc_neg"]:
            print(f"    (khai báo giả: {row['desc_neg']})")

    json.dump({"n": n, "stats": dict(st), "he_toa_do": "abs" if args.abs else "norm1000"},
              open(OUT_STATS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nĐã lưu {OUT_JSONL}  và  {OUT_STATS}")


if __name__ == "__main__":
    main()
