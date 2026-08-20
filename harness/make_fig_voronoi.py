# -*- coding: utf-8 -*-
"""FREE · offline — dựng hình minh hoạ luật chấm cho bài FAIR'2026.

Một bước thật của tập kiểm (ep19374, bước 3, màn hồ sơ cá nhân của một ứng dụng thể
dục). Đích là dòng "Birthday"; câu của mô hình gốc tả dòng "Gender" ngay phía trên. Bộ
trỏ trả điểm cách gold 128 px, tức **vẫn nằm trong dung sai 14% (151 px)**, nên luật
quy ước cho ĐÚNG; chỉ luật ô gần nhất bắt được là sai dòng. Đây đúng là lập luận trung
tâm của mục IV-B.

Chạy: ~/.venvs/thesis/bin/python harness/make_fig_voronoi.py
Ra:   paper/fair2026/fig_voronoi.png
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import a11y_inventory as A11Y
import metric_exec as M

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "dg1_cache/test_ac/images/ep19374_s3.png")
OUT = os.path.abspath(os.path.join(HERE, "../paper/fair2026/fig_voronoi.png"))

GOLD = (540.0, 586.0)          # điểm người thật chạm (dòng "Birthday")
PRED_S1 = (539.0, 588.0)       # bộ trỏ đọc câu của S1
PRED_BASE = (540.0, 458.0)     # bộ trỏ đọc câu của mô hình gốc (dòng "Gender")
CROP = (0, 348, 1080, 790)     # phần màn hình cần thấy (348: tránh cắt ngang chữ)
STEP = 3                       # bước lưới khi tô ô Voronoi

# --- màu (đủ tương phản cả khi in đen trắng) ---
C_CELL = (255, 214, 102, 90)   # ô Voronoi của nút đích
C_GOLD = (0, 0, 0)
C_OK = (0, 132, 61)
C_BAD = (200, 30, 30)
C_OTHER = (90, 90, 90)


def main():
    im = Image.open(IMG).convert("RGBA")
    w, h = im.size
    boxes = A11Y.elements("episode_19374_screenshot_3.png")
    centres = [((b[0] + b[2]) / 2, (b[1] + b[3]) / 2) for b in boxes]
    # đúng danh sách mà hàm chấm dùng: gold là site của nút đích, phần còn lại đã gộp
    sites = M.dedupe_buttons(centres, GOLD, (w, h))
    others = [s for s in sites if M._dist(s, GOLD) > 1e-6]

    # kiểm lại luật trên chính hình này, để hình không nói khác mã
    assert M.hit_disk(PRED_S1, GOLD, (w, h)) and M.hit_voronoi(PRED_S1, GOLD, centres, (w, h))
    assert M.hit_disk(PRED_BASE, GOLD, (w, h)) and not M.hit_voronoi(PRED_BASE, GOLD, centres, (w, h))

    # --- tô ô Voronoi của nút đích ---
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = CROP
    for py in range(y0, y1, STEP):
        run = None
        for px in range(x0, x1, STEP):
            dg = math.hypot(px - GOLD[0], py - GOLD[1])
            inside = all(math.hypot(px - o[0], py - o[1]) >= dg for o in others)
            if inside and run is None:
                run = px
            elif not inside and run is not None:
                d.rectangle([run, py, px, py + STEP], fill=C_CELL)
                run = None
        if run is not None:
            d.rectangle([run, py, x1, py + STEP], fill=C_CELL)
    im = Image.alpha_composite(im, lay)

    d = ImageDraw.Draw(im)
    # Dung sai 14% theo trục dọc là +-336 px quanh gold, tức 250..922: toàn bộ khung in
    # nằm trong đó. Không vẽ được biên nào trong khung, và đó chính là ý của hình.
    tol = 0.14 * w
    # tâm các phần tử khác
    for o in others:
        if y0 <= o[1] <= y1:
            d.ellipse([o[0] - 6, o[1] - 6, o[0] + 6, o[1] + 6], outline=C_OTHER, width=3)
    # điểm chạm thật
    d.line([GOLD[0] - 17, GOLD[1], GOLD[0] + 17, GOLD[1]], fill=C_GOLD, width=5)
    d.line([GOLD[0], GOLD[1] - 17, GOLD[0], GOLD[1] + 17], fill=C_GOLD, width=5)
    # hai điểm bộ trỏ trả về
    # khung dung sai quy ước +-0,14 canh: thu hai luat deu HIEN tren hinh
    x0, x1 = GOLD[0] - tol, GOLD[0] + tol
    y0, y1 = GOLD[1] - 0.14 * h, GOLD[1] + 0.14 * h
    dash = 18
    for x in range(int(x0), int(x1), dash * 2):
        d.line([x, y0, min(x + dash, x1), y0], fill=C_GOLD, width=3)
        d.line([x, y1, min(x + dash, x1), y1], fill=C_GOLD, width=3)
    for y in range(int(y0), int(y1), dash * 2):
        d.line([x0, y, x0, min(y + dash, y1)], fill=C_GOLD, width=3)
        d.line([x1, y, x1, min(y + dash, y1)], fill=C_GOLD, width=3)

    for pt, col in ((PRED_S1, C_OK), (PRED_BASE, C_BAD)):
        d.ellipse([pt[0] - 15, pt[1] - 15, pt[0] + 15, pt[1] + 15], outline=(255, 255, 255), width=7)
        d.ellipse([pt[0] - 15, pt[1] - 15, pt[0] + 15, pt[1] + 15], outline=col, width=4)

    im.crop(CROP).convert("RGB").save(OUT, dpi=(600, 600))
    print("đã ghi", OUT, im.crop(CROP).size)
    print("phần tử trên màn:", len(boxes), "→ sau gộp:", len(sites))
    print("lệch của điểm sai:", round(math.dist(PRED_BASE, GOLD)), "px | dung sai ngang:", round(tol), "px")


if __name__ == "__main__":
    main()
