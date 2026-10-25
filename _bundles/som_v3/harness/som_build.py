# -*- coding: utf-8 -*-
"""Dựng dữ liệu cho phép chấm NGƯỜI NGHE TRẮC NGHIỆM (comprehension accuracy) — chạy CPU, 0 GPU.

    ~/.venvs/thesis/bin/python harness/som_build.py [--limit N] [--out harness/dg1_cache/som]

Giao thức (khoá TRƯỚC khi có điểm nào của người nghe, 14/9/2026):
  · Tiền lệ: đánh giá câu sinh bằng một bộ hiểu chọn vùng trong tập ứng viên — Mao et al. CVPR 2016,
    Luo et al. CVPR 2017; trên giao diện: Seq2Act ACL 2020, Mind2Web NeurIPS 2023 D&B. Vẽ số lên ảnh
    theo kiểu Set-of-Mark.
  · ỨNG VIÊN của mỗi màn = mọi nút trong cây trợ năng (cùng cây đã dựng nhãn vàng) thoả: hiển thị,
    có hành động CLICK (16) hoặc LONG_CLICK (32), cạnh ≥ 8 px, diện tích ≤ 50% màn. Gộp các hộp gần
    trùng nhau (IoU ≥ 0,9, giữ một). KHÔNG cắt theo số lượng ⇒ không có luật cắt nào phụ thuộc đáp án.
    Đánh số theo thứ tự đọc (trên → dưới, trái → phải) — độc lập với đáp án.
  · ĐÁP ÁN = mọi ứng viên có hộp chứa điểm chạm vàng (chạm vào đâu trong phần tử cũng kích hoạt phần
    tử, đúng lý do của luật D.3 AndroidControl). Bước không có ứng viên nào chứa điểm vàng vẫn nằm
    trong quần thể và chắc chắn tính TRƯỢT (bảo thủ).
  · Ảnh vẽ số: khung màu + nhãn số nền đặc ở góc trên trái hộp, ghi JPEG chất lượng 92.

Ghi ra `<out>/som.jsonl` (một dòng một bước chạm) và `--ve-anh` ảnh mẫu ở `<out>/img/` để xem mắt.
Ảnh đầy đủ được vẽ ngay trên Kaggle bằng CHÍNH hàm `ve()` của file này (`som_listener.py` import).
"""
import argparse, colorsys, json, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

TEST = os.path.join(HERE, "dg1_cache", "test_ac")


def iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / ua if ua > 0 else 0.0


def ung_vien(rel, W, H):
    import a11y_inventory as A          # nạp muộn: Kaggle chỉ cần ve(), không cần cây trợ năng
    o = A._load(A.key_for(rel) or "") or []
    bx = []
    for w in o:
        if w.get("window_type") == 3:
            continue
        for n in w.get("tree", []):
            if not n.get("is_visible_to_user"):
                continue
            if not (set(n.get("actions") or []) & {16, 32}):
                continue
            b = n.get("bounds_in_screen") or {}
            x1, y1 = max(0, b.get("left", 0)), max(0, b.get("top", 0))
            x2, y2 = min(W, b.get("right", 0)), min(H, b.get("bottom", 0))
            if x2 - x1 < 8 or y2 - y1 < 8 or (x2 - x1) * (y2 - y1) > 0.5 * W * H:
                continue
            bx.append((x1, y1, x2, y2))
    giu = []
    for b in bx:
        if all(iou(b, k) < 0.9 for k in giu):
            giu.append(b)
    giu.sort(key=lambda b: (b[1], b[0]))
    return giu


def mau(i):
    r, g, b = colorsys.hsv_to_rgb((i * 0.618034) % 1.0, 0.9, 0.85)
    return int(r * 255), int(g * 255), int(b * 255)


def ve(img, boxes):
    im = img.convert("RGB")
    d = ImageDraw.Draw(im)
    W, H = im.size
    fs = max(22, int(W * 0.028))
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", fs)
    except OSError:
        font = ImageFont.load_default(size=fs)
    lw = max(3, W // 300)
    for i, (x1, y1, x2, y2) in enumerate(boxes, 1):
        c = mau(i)
        d.rectangle([x1, y1, x2, y2], outline=c, width=lw)
        t = str(i)
        tw, th = d.textbbox((0, 0), t, font=font)[2:]
        lx, ly = x1, max(0, y1 - th - 6) if y1 - th - 6 >= 0 else y1
        d.rectangle([lx, ly, lx + tw + 8, ly + th + 6], fill=c)
        d.text((lx + 4, ly + 2), t, fill=(255, 255, 255), font=font)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default=os.path.join(HERE, "dg1_cache", "som"))
    ap.add_argument("--ve-anh", type=int, default=20,
                    help="chỉ vẽ N ảnh đầu để xem mắt; Kaggle tự vẽ từ ảnh gốc bằng đúng hàm ve()")
    a = ap.parse_args()
    os.makedirs(os.path.join(a.out, "img"), exist_ok=True)
    recs = [json.loads(l) for l in open(os.path.join(TEST, "test.jsonl"), encoding="utf-8")]
    taps = [r for r in recs if r["action"].get("action_type") in ("click", "long_press") and "x" in r["action"]]
    assert len(taps) == 4463, len(taps)
    if a.limit:
        taps = taps[:a.limit]
    n_phu, so = 0, []
    tep = os.path.join(a.out, "som.jsonl" if not a.limit else f"som_thu_{a.limit}.jsonl")
    with open(tep, "w", encoding="utf-8") as f:
        for i, r in enumerate(taps):
            rel = f"episode_{r['episode_id']}_screenshot_{r['step_id']}.png"
            img = Image.open(os.path.join(TEST, r["image"]))
            W, H = img.size
            bx = ung_vien(rel, W, H)
            gx, gy = float(r["action"]["x"]), float(r["action"]["y"])
            dap = [k for k, b in enumerate(bx, 1) if b[0] <= gx <= b[2] and b[1] <= gy <= b[3]]
            n_phu += bool(dap); so.append(len(bx))
            ten = f"img/{r['episode_id']}_{r['step_id']}.jpg"
            if i < a.ve_anh:
                ve(img, bx).save(os.path.join(a.out, ten), quality=92)
            f.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "image": ten,
                                "image_goc": r["image"], "w": W, "h": H, "boxes": bx, "dap_an": dap}, ensure_ascii=False) + "\n")
            if (i + 1) % 500 == 0:
                print(f"  {i+1}/{len(taps)}", flush=True)
    so.sort()
    print(f"ghi {tep}: {len(so)} bước · ứng viên/màn trung vị {so[len(so)//2]} · p90 {so[int(.9*len(so))]}"
          f" · max {so[-1]} · không có ứng viên {sum(1 for x in so if x == 0)}")
    print(f"phủ đáp án (có ≥1 ứng viên chứa điểm vàng): {n_phu}/{len(so)} = {n_phu/len(so):.1%}")


if __name__ == "__main__":
    main()
