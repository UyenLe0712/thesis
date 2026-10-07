# -*- coding: utf-8 -*-
"""Dựng lại hình minh hoạ luật chấm cho LUẬN VĂN: cùng dữ liệu, cùng phép kiểm,
nhưng thêm chú giải trong hình và làm các dấu tách khỏi chữ trên ảnh.

Chạy: python3 fig2.py  ->  thesis/figures/fig_voronoi.png
"""
import os, sys, math
H = "/mnt/d/Master/Thesis/harness"
sys.path.insert(0, H)
from PIL import Image, ImageDraw, ImageFont
import a11y_inventory as A11Y
import metric_exec as M

IMG = os.path.join(H, "dg1_cache/test_ac/images/ep19374_s3.png")
OUT = "/mnt/d/Master/Thesis/thesis/figures/fig_voronoi.png"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

GOLD, PRED_S1, PRED_BASE = (540.0, 586.0), (539.0, 588.0), (540.0, 458.0)
CROP = (0, 340, 1080, 800)
STEP = 3
C_CELL = (255, 214, 102, 105)
C_GOLD, C_OK, C_BAD, C_OTHER = (0, 0, 0), (0, 118, 54), (198, 26, 26), (110, 110, 110)
LEG_H = 280          # dải chú giải thêm ở dưới


def main():
    im = Image.open(IMG).convert("RGBA")
    w, h = im.size
    boxes = A11Y.elements("episode_19374_screenshot_3.png")
    centres = [((b[0] + b[2]) / 2, (b[1] + b[3]) / 2) for b in boxes]
    sites = M.dedupe_buttons(centres, GOLD, (w, h))
    others = [s for s in sites if M._dist(s, GOLD) > 1e-6]

    # hình không được nói khác mã chấm
    assert M.hit_disk(PRED_S1, GOLD, (w, h)) and M.hit_voronoi(PRED_S1, GOLD, centres, (w, h))
    assert M.hit_disk(PRED_BASE, GOLD, (w, h)) and not M.hit_voronoi(PRED_BASE, GOLD, centres, (w, h))

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
                d.rectangle([run, py, px, py + STEP], fill=C_CELL); run = None
        if run is not None:
            d.rectangle([run, py, x1, py + STEP], fill=C_CELL)
    im = Image.alpha_composite(im, lay)
    d = ImageDraw.Draw(im)

    def cham_tron(pt, col, r, wdt):
        """vòng tròn có viền trắng bên ngoài để không lẫn vào chữ trên ảnh"""
        d.ellipse([pt[0]-r, pt[1]-r, pt[0]+r, pt[1]+r], outline=(255, 255, 255), width=wdt+4)
        d.ellipse([pt[0]-r, pt[1]-r, pt[0]+r, pt[1]+r], outline=col, width=wdt)

    for o in others:                       # tâm phần tử cạnh tranh
        if y0 <= o[1] <= y1:
            cham_tron(o, C_OTHER, 6, 2)

    tol_x, tol_y = 0.14 * w, 0.14 * h      # khung dung sai quy ước
    bx0, bx1 = GOLD[0] - tol_x, GOLD[0] + tol_x
    by0, by1 = GOLD[1] - tol_y, GOLD[1] + tol_y
    dash = 20
    for x in range(int(bx0), int(bx1), dash * 2):
        for yy in (by0, by1):
            d.line([x, yy, min(x + dash, bx1), yy], fill=C_GOLD, width=3)
    for y in range(int(by0), int(by1), dash * 2):
        for xx in (bx0, bx1):
            d.line([xx, y, xx, min(y + dash, by1)], fill=C_GOLD, width=3)

    cham_tron(PRED_BASE, C_BAD, 17, 5)
    cham_tron(PRED_S1, C_OK, 28, 5)      # to hơn để không che dấu chữ thập bên trong
    # điểm chạm thật: chữ thập viền trắng
    for wdt, col in ((11, (255, 255, 255)), (5, C_GOLD)):
        d.line([GOLD[0]-19, GOLD[1], GOLD[0]+19, GOLD[1]], fill=col, width=wdt)
        d.line([GOLD[0], GOLD[1]-19, GOLD[0], GOLD[1]+19], fill=col, width=wdt)

    im = im.crop(CROP).convert("RGB")
    cw, ch = im.size

    # ---- dải chú giải ----
    out = Image.new("RGB", (cw, ch + LEG_H), (255, 255, 255))
    out.paste(im, (0, 0))
    d = ImageDraw.Draw(out)
    d.rectangle([0, 0, cw - 1, ch - 1], outline=(120, 120, 120), width=2)
    f = ImageFont.truetype(FONT, 26)
    yA, yB, yC = ch + 55, ch + 130, ch + 205
    def muc(x, y, ve, chu):
        ve(x, y)
        d.text((x + 34, y - 15), chu, font=f, fill=(20, 20, 20))
    def cross(x, y):
        d.line([x-14, y, x+14, y], fill=C_GOLD, width=5)
        d.line([x, y-14, x, y+14], fill=C_GOLD, width=5)
    def ring(col, r=13, wdt=4):
        return lambda x, y: d.ellipse([x-r, y-r, x+r, y+r], outline=col, width=wdt)
    def patch(x, y):
        d.rectangle([x-15, y-13, x+15, y+13], fill=(255, 214, 102), outline=(190, 150, 40))
    def dashbox(x, y):
        for i in range(-15, 15, 10):
            d.line([x+i, y-13, x+min(i+6, 15), y-13], fill=C_GOLD, width=3)
            d.line([x+i, y+13, x+min(i+6, 15), y+13], fill=C_GOLD, width=3)
        for i in range(-13, 13, 10):
            d.line([x-15, y+i, x-15, y+min(i+6, 13)], fill=C_GOLD, width=3)
            d.line([x+15, y+i, x+15, y+min(i+6, 13)], fill=C_GOLD, width=3)

    muc(50,  yA, cross,               "điểm người dùng chạm")
    muc(50,  yB, ring(C_OK),          "điểm trả về cho câu của S1: trúng")
    muc(50,  yC, ring(C_BAD),         "điểm trả về cho câu của Base: trượt")
    muc(590, yA, patch,               "ô Voronoi của điểm chạm")
    muc(590, yB, dashbox,             "vùng dung sai quy ước")
    muc(590, yC, ring(C_OTHER, 8, 3), "tâm một phần tử cạnh tranh")

    out.save(OUT, dpi=(600, 600))
    print("đã ghi", OUT, out.size)
    print("phần tử trên màn:", len(boxes), "→ sau gộp:", len(sites))
    print("lệch của điểm sai:", round(math.dist(PRED_BASE, GOLD)), "px · dung sai ngang:", round(tol_x), "px")


main()
