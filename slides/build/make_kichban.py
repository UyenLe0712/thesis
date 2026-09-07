# -*- coding: utf-8 -*-
"""Trich phan ghi chu cua LUAN_VAN_SLIDE_BAOCAO.pptx ra slides/KICH_BAN_BAO_VE.md.
Chay sau moi lan `node build_baove.js`:  python3 make_kichban.py"""
import zipfile, re, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PPTX = os.path.join(ROOT, "slides", "LUAN_VAN_SLIDE_BAOCAO.pptx")
OUT  = os.path.join(ROOT, "slides", "KICH_BAN_BAO_VE.md")
z = zipfile.ZipFile(PPTX)
num = lambda n: int(re.findall(r"\d+", n)[0])
sl = sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)], key=num)
nt = {int(m.group(1)): n for n in z.namelist()
      for m in [re.match(r"ppt/notesSlides/notesSlide(\d+)\.xml$", n)] if m}

def notes_body(path):
    x = z.read(path).decode("utf-8"); out = []
    for sp in re.findall(r"<p:sp>.*?</p:sp>", x, re.S):
        if 'type="sldNum"' in sp: continue          # bo o so trang
        out.append("".join(re.findall(r"<a:t>(.*?)</a:t>", sp, re.S)))
    return "".join(out).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")

def title(path):
    for sp in re.findall(r"<p:sp>.*?</p:sp>", z.read(path).decode("utf-8"), re.S):
        m = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/>', sp)
        if m and int(m.group(2)) < 70000:
            t = "".join(re.findall(r"<a:t>(.*?)</a:t>", sp, re.S)).strip()
            if t and "ĐẠI HỌC" not in t:
                return re.sub(r"^Dự phòng · ", "", t)
    return ""

L = ["# Kịch bản trình bày bảo vệ luận văn", "",
     "Sinh tự động từ `slides/build/build_baove.js`. Sửa lời dẫn trong script rồi chạy lại",
     "`node build_baove.js && python3 make_kichban.py`, đừng sửa tay file này.", "", "---", ""]
run = 0
for i, n in enumerate(sl, 1):
    body = notes_body(nt[i]) if i in nt else ""
    m = re.match(r"\[~(\d+) giây\]\s*", body); sec = int(m.group(1)) if m else 0
    if m: body = body[m.end():]
    tt = title(n) or "(bìa)"
    if i <= 26:
        run += sec
        L += [f"## Slide {i} · {tt}  —  ~{sec}s  (cộng dồn {run//60}:{run%60:02d})", ""]
    else:
        L += [f"## Dự phòng {i-26} · {tt}", ""]
    L += ([p.strip() for para in body.split("\n") if para.strip() for p in (para, "")]
          if body.strip() else ["_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_", ""])
L += ["---", "",
      f"**Tổng phần trình bày: {run//60} phút {run%60:02d} giây** ở tốc độ 135 từ mỗi phút, "
      "chưa tính thời gian chuyển slide và dừng lại chỉ bảng.", "",
      "Mười hai slide dự phòng nằm sau slide 26, không thuộc mạch chính. "
      "Lúc trình chiếu, gõ số slide rồi Enter để mở.", ""]
open(OUT, "w", encoding="utf-8").write("\n".join(L))
print("Da ghi", OUT, "| tong %d:%02d" % (run//60, run % 60))
