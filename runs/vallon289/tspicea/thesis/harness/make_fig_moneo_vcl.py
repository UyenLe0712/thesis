# -*- coding: utf-8 -*-
"""Hình 2 của bài VCL: mỏ neo chữ trên MỘT MÀN HÌNH THẬT của tập kiểm.

Bước ep18187_s6 — màn chọn ứng dụng để chia sẻ. Bốn biểu tượng tròn cùng vai trò,
KHÔNG biểu tượng nào có tên trong cây trợ năng; thứ tách chúng ra là chuỗi chữ ngay bên dưới.

Chạy: python3 harness/make_fig_moneo_vcl.py  ->  paper/vcl2026/hinh/fig_moneo.png
"""
import os, json
from PIL import Image, ImageDraw, ImageFont

H   = "/mnt/d/Master/Thesis/harness"
IMG = os.path.join(H, "dg1_cache/test_ac/images/ep18187_s6.png")
OUT = "/mnt/d/Master/Thesis/paper/vcl2026/hinh/fig_moneo.png"
# Chữ trên hình phải cùng kiểu chữ với thân bài (TeX Gyre Termes). Tectonic tải font về
# kho nội dung nên tên tệp là mã băm; hàm dưới dò theo TÊN FONT rồi in ra đường dẫn đã dùng.
DEJA = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJAB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def tim_font(ten, du_phong):
    import glob
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        print("khong co fontTools, dung", du_phong)
        return du_phong
    for f in glob.glob(os.path.expanduser("~/.cache/Tectonic/files/*/*")):
        try:
            if open(f, "rb").read(4) not in (b"OTTO", b"\x00\x01\x00\x00"):
                continue
            if TTFont(f, fontNumber=0, lazy=True)["name"].getDebugName(4) == ten:
                print("font", ten, "->", f)
                return f
        except Exception:
            pass
    print("khong tim thay", ten, "- dung", du_phong)
    return du_phong

# toạ độ pixel thật, lấy từ cây trợ năng + tệp OCR của chính bước này
TARGET = (61, 2046, 208, 2193)          # biểu tượng cần chạm
OTHERS = [(331, 2046, 478, 2193), (601, 2046, 748, 2193), (871, 2046, 1018, 2193)]
ANCHOR = (93, 2211, 176, 2258)          # hộp chữ "Gmail"
POINT  = (120, 2167)                    # điểm chạm trong đáp án
CROP   = (16, 1955, 1064, 2300)
S      = 2                              # phóng to để nét vẽ và chữ đủ mịn

GREEN  = (34, 200, 120)
AMBER  = (255, 176, 64)
CYAN   = (94, 190, 255)
INK    = (24, 24, 24)
GREY   = (110, 110, 110)


def dash_rect(d, box, colour, w=3, dash=16, gap=12):
    x0, y0, x1, y1 = box
    for x in range(int(x0), int(x1), dash + gap):
        d.line([x, y0, min(x + dash, x1), y0], fill=colour, width=w)
        d.line([x, y1, min(x + dash, x1), y1], fill=colour, width=w)
    for y in range(int(y0), int(y1), dash + gap):
        d.line([x0, y, x0, min(y + dash, y1)], fill=colour, width=w)
        d.line([x1, y, x1, min(y + dash, y1)], fill=colour, width=w)


def sc(box, ox, oy):
    return [(box[0] - ox) * S, (box[1] - oy) * S, (box[2] - ox) * S, (box[3] - oy) * S]


def main():
    im = Image.open(IMG).convert("RGB")
    ox, oy, x1, y1 = CROP
    im = im.crop(CROP).resize(((x1 - ox) * S, (y1 - oy) * S), Image.LANCZOS)
    W, Hh = im.size

    LEG = 0
    canvas = Image.new("RGB", (W, Hh), (255, 255, 255))
    canvas.paste(im, (0, 0))
    d = ImageDraw.Draw(canvas)

    fb = ImageFont.truetype(tim_font("TeX Gyre Termes Bold", DEJAB), 40)
    f  = ImageFont.truetype(tim_font("TeX Gyre Termes", DEJA), 40)

    # ba phần tử cùng vai trò
    for b in OTHERS:
        dash_rect(d, sc(b, ox, oy), AMBER, w=3)

    # phần tử cần chạm
    t = sc(TARGET, ox, oy)
    d.rectangle(t, outline=GREEN, width=6)

    # điểm chạm
    px, py = (POINT[0] - ox) * S, (POINT[1] - oy) * S
    r = 16
    d.line([px - r, py - r, px + r, py + r], fill=GREEN, width=6)
    d.line([px + r, py - r, px - r, py + r], fill=GREEN, width=6)

    # mỏ neo chữ + đường đo khoảng cách, đặt lệch sang phải để không đè lên biểu tượng
    a = sc(ANCHOR, ox, oy)
    dash_rect(d, a, CYAN, w=3)
    ytam, yneo = (t[1] + t[3]) / 2, (a[1] + a[3]) / 2
    xd = t[2] + 30
    d.line([xd, ytam, xd, yneo], fill=CYAN, width=4)
    for yy, dy in ((ytam, 14), (yneo, -14)):
        d.line([xd - 12, yy + dy, xd, yy], fill=CYAN, width=4)
        d.line([xd + 12, yy + dy, xd, yy], fill=CYAN, width=4)
    d.line([t[2] + 4, ytam, xd, ytam], fill=CYAN, width=2)
    d.line([a[2] + 4, yneo, xd, yneo], fill=CYAN, width=2)
    d.text((xd + 14, (ytam + yneo) / 2 - 16), "114,5 px", font=f, fill=CYAN)

    # nhãn ngay trên hình
    d.text((t[0], t[1] - 66), "phần tử cần chạm", font=fb, fill=GREEN)
    d.text((sc(OTHERS[0], ox, oy)[0], sc(OTHERS[0], ox, oy)[1] - 66),
           "ba phần tử cùng vai trò trên cùng màn", font=fb, fill=AMBER)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    canvas.save(OUT)
    print("da ghi", OUT, canvas.size)


if __name__ == "__main__":
    main()
