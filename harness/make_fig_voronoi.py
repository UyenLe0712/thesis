# -*- coding: utf-8 -*-
"""FREE · offline — dựng hình minh hoạ luật chấm cho bài FAIR'2026.

Một bước thật của tập kiểm (ep19374, bước 3, màn hồ sơ cá nhân của một ứng dụng thể
dục). Đích là dòng "Birthday"; câu của mô hình gốc tả dòng "Gender" ngay phía trên. Bộ
trỏ trả điểm cách gold 128 px, tức **vẫn nằm trong dung sai 14% (151 px ngang, 336 px
dọc)**, nên luật quy ước cho ĐÚNG; chỉ luật ô gần nhất bắt được là sai dòng.

Bản 30/8: thêm dải chú giải trong hình + mũi tên khoảng cách, theo mẫu bản tiếng Việt
(make_fig_voronoi_vi.py), để hình tự đọc được mà không cần dò trong caption.

Chạy: ~/.venvs/thesis/bin/python harness/make_fig_voronoi.py
Ra:   paper/fair2026/fig_voronoi.png
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
import a11y_inventory as A11Y
import metric_exec as M

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "dg1_cache/test_ac/images/ep19374_s3.png")
OUT = os.path.abspath(os.path.join(HERE, "../paper/fair2026/fig_voronoi.png"))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

GOLD = (540.0, 586.0)          # điểm người thật chạm (dòng "Birthday")
PRED_S1 = (539.0, 588.0)       # bộ trỏ đọc câu của S1
PRED_BASE = (540.0, 458.0)     # bộ trỏ đọc câu của mô hình gốc (dòng "Gender")
CROP = (0, 352, 1080, 772)     # phần màn hình cần thấy
STEP = 3                       # bước lưới khi tô ô Voronoi
LEG_H = 285                    # dải chú giải thêm ở dưới

# --- màu (đủ tương phản cả khi in đen trắng) ---
C_CELL = (255, 214, 102, 105)  # ô Voronoi của nút đích
C_GOLD = (0, 0, 0)
C_OK = (0, 118, 54)
C_BAD = (198, 26, 26)
C_OTHER = (110, 110, 110)


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

    def ring(pt, col, r, wdt):
        """vòng tròn có viền trắng bên ngoài để không lẫn vào chữ trên ảnh"""
        d.ellipse([pt[0]-r, pt[1]-r, pt[0]+r, pt[1]+r], outline=(255, 255, 255), width=wdt+4)
        d.ellipse([pt[0]-r, pt[1]-r, pt[0]+r, pt[1]+r], outline=col, width=wdt)

    for o in others:                        # tâm các phần tử cạnh tranh
        if y0 <= o[1] <= y1:
            ring(o, C_OTHER, 6, 2)

    tol_x, tol_y = 0.14 * w, 0.14 * h       # khung dung sai quy ước
    bx0, bx1 = GOLD[0] - tol_x, GOLD[0] + tol_x
    by0, by1 = GOLD[1] - tol_y, GOLD[1] + tol_y
    dash = 20
    for x in range(int(bx0), int(bx1), dash * 2):
        for yy in (by0, by1):
            d.line([x, yy, min(x + dash, bx1), yy], fill=C_GOLD, width=3)
    for y in range(int(by0), int(by1), dash * 2):
        for xx in (bx0, bx1):
            d.line([xx, y, xx, min(y + dash, by1)], fill=C_GOLD, width=3)

    # mũi tên khoảng cách giữa hai điểm bộ trỏ trả về
    ax = GOLD[0] + 108
    d.line([ax, PRED_BASE[1], ax, GOLD[1]], fill=C_GOLD, width=4)
    for yy, s in ((PRED_BASE[1], 1), (GOLD[1], -1)):
        d.line([ax - 9, yy + 11 * s, ax, yy], fill=C_GOLD, width=4)
        d.line([ax + 9, yy + 11 * s, ax, yy], fill=C_GOLD, width=4)
    fd = ImageFont.truetype(FONT, 40)
    lbl = "128 px"
    tw = d.textlength(lbl, font=fd)
    ty = (PRED_BASE[1] + GOLD[1]) / 2 - 24
    d.rectangle([ax + 10, ty - 8, ax + 20 + tw, ty + 48], fill=(255, 255, 255))
    d.text((ax + 14, ty), lbl, font=fd, fill=(20, 20, 20))

    ring(PRED_BASE, C_BAD, 17, 5)
    ring(PRED_S1, C_OK, 28, 5)              # to hơn để không che dấu chữ thập bên trong
    for wdt, col in ((11, (255, 255, 255)), (5, C_GOLD)):   # điểm chạm thật
        d.line([GOLD[0]-19, GOLD[1], GOLD[0]+19, GOLD[1]], fill=col, width=wdt)
        d.line([GOLD[0], GOLD[1]-19, GOLD[0], GOLD[1]+19], fill=col, width=wdt)

    im = im.crop(CROP).convert("RGB")
    cw, ch = im.size

    # ---- dải chú giải ----
    out = Image.new("RGB", (cw, ch + LEG_H), (255, 255, 255))
    out.paste(im, (0, 0))
    d = ImageDraw.Draw(out)
    d.rectangle([0, 0, cw - 1, ch - 1], outline=(120, 120, 120), width=2)
    f = ImageFont.truetype(FONT, 34)
    yA, yB, yC = ch + 55, ch + 145, ch + 235

    def item(x, y, draw_mark, text):
        draw_mark(x, y)
        d.text((x + 40, y - 23), text, font=f, fill=(20, 20, 20))

    def cross(x, y):
        d.line([x-13, y, x+13, y], fill=C_GOLD, width=5)
        d.line([x, y-13, x, y+13], fill=C_GOLD, width=5)

    def circ(col, r=15, wdt=5):
        return lambda x, y: d.ellipse([x-r, y-r, x+r, y+r], outline=col, width=wdt)

    def patch(x, y):
        d.rectangle([x-14, y-12, x+14, y+12], fill=(255, 214, 102), outline=(190, 150, 40))

    def dashbox(x, y):
        for i in range(-14, 14, 10):
            d.line([x+i, y-12, x+min(i+6, 14), y-12], fill=C_GOLD, width=3)
            d.line([x+i, y+12, x+min(i+6, 14), y+12], fill=C_GOLD, width=3)
        for i in range(-12, 12, 10):
            d.line([x-14, y+i, x-14, y+min(i+6, 12)], fill=C_GOLD, width=3)
            d.line([x+14, y+i, x+14, y+min(i+6, 12)], fill=C_GOLD, width=3)

    item(40,  yA, cross,                 "human touch")
    item(40,  yB, circ(C_OK),            "fine-tuned: correct")
    item(40,  yC, dashbox,               "14% tolerance")
    item(600, yA, patch,                 "target cell")
    item(600, yB, circ(C_BAD),           "untuned: wrong")
    item(600, yC, circ(C_OTHER, 10, 4), "competing centre")

    out.save(OUT, dpi=(600, 600))
    print("đã ghi", OUT, out.size)
    print("phần tử trên màn:", len(boxes), "→ sau gộp:", len(sites))
    print("lệch của điểm sai:", round(math.dist(PRED_BASE, GOLD)), "px | dung sai ngang:", round(tol_x), "px")


if __name__ == "__main__":
    main()
