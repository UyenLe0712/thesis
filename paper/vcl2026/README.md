# Bài VCL2026 — thư mục nộp

Hội thảo Quốc gia lần 4 về Ngôn ngữ học Tính toán · HUFLIT, 27/11/2026
Hạn nộp: **30/8/2026** · https://vcl.huflit.edu.vn/

## Tệp trong thư mục

| tệp | là gì |
|---|---|
| `main.tex` | bản thảo (nguồn) |
| `main.pdf` | **bản nộp** — 21 trang, 0 overfull, 14 DOI đã tra và xác minh; **thân bài 17 trang** (tr.1–17), tài liệu tham khảo tr.18–19, Phụ lục A + thông tin tác giả tr.19–20. Rút từ 24 trang ngày 30/8, bản cũ ở `_archive/main_TRUOC_RUT_TRANG_30_8.tex.bak` |
| `bang_anh/Bang_1..5.png` · `Hinh_1..2.png` | ảnh 5 bảng + 2 hình, 300 dpi, gửi kèm theo quy cách |
| `bang_anh.tex` · `bang_anh.pdf` | mã dựng ra bộ ảnh trên. **Sinh tự động** bằng script ở mục *Dựng lại bộ ảnh* — trích thẳng khối `table`/`figure` từ `main.tex`, không chép tay |
| `VCL_Conference_Paper_Template for authors.docx` | template chính thức ban tổ chức phát |
| `_archive/main_TRUOC_APA.tex.bak` | bản trước khi áp template (bố cục đo từ kỷ yếu VCL 2025) |

## Lệnh dựng

```
rm -f main.log && tectonic -X compile main.tex --outdir . --keep-logs
grep -oE "Output written on main\.xdv \([0-9]+ page" main.log   # số trang
grep -c Overfull main.log                                        # phải là 0
```

Máy này **không có `xelatex`**. Đừng bao giờ nuốt lỗi bằng `>/dev/null 2>&1` — lệnh sai sẽ
im lặng và ta đọc nhầm PDF cũ. `main.log` chỉ được ghi khi có `--keep-logs`.

`hinh/fig_moneo.png` (Hình 2) dựng lại bằng `python3 harness/make_fig_moneo_vcl.py` —
ảnh chụp màn hình thật của bước `ep18187_s6` trong tập kiểm, phủ lớp vẽ; hộp bao lấy từ cây
trợ năng, vị trí chuỗi chữ lấy từ `dg1_cache/test_ac/ocr.jsonl`. Hình 1 là sơ đồ TikZ nằm
thẳng trong `main.tex`.

Dựng lại bộ ảnh bảng và hình. `bang_anh.tex` **sinh tự động**, không sửa tay: phần khai báo
chép nguyên từ `main.tex` (chỉ đổi `pagestyle` và thêm gói `float`) nên mọi màu và lệnh tự
định nghĩa đều theo kịp, còn thân file là mọi khối `table`/`figure` của bài, mỗi khối một
trang. Chạy lại mỗi khi thêm bớt bảng hoặc hình:
```
tectonic -X compile bang_anh.tex --outdir .
python3 - <<'PY'
import fitz
d = fitz.open('bang_anh.pdf')
for i, p in enumerate(d):
    b = p.get_text("blocks")
    x0=min(x[0] for x in b); y0=min(x[1] for x in b)
    x1=max(x[2] for x in b); y1=max(x[3] for x in b)
    for dr in p.get_drawings():
        r=dr['rect']; x0=min(x0,r.x0); y0=min(y0,r.y0); x1=max(x1,r.x1); y1=max(y1,r.y1)
    p.get_pixmap(dpi=300, clip=fitz.Rect(x0-10,y0-10,x1+10,y1+10)).save(f'bang_anh/Bang_{i+1}.png')
PY
```

## Quy cách đang áp — nguồn của từng thông số

Bố cục đọc **trực tiếp từ XML** của `VCL_Conference_Paper_Template for authors.docx`,
không phải từ ghi chú:

| thông số | giá trị | nguồn |
|---|---|---|
| khổ · lề | A4 · 2,54 cm cả bốn phía | `sectPr/pgMar` = 1440 twips |
| font · cỡ | Times New Roman 12 | `sz=24` half-point |
| giãn dòng thân bài | **1,5** | ⚠️ xem *Hai chỗ mâu thuẫn* bên dưới |
| tóm tắt · bảng · tài liệu tham khảo | giãn đơn | `line=240` |
| thụt đầu dòng | 0,5 inch (36 pt) | `ind/firstLine=720` |
| cách đoạn | trước 0 pt, sau 6 pt | chữ trong template |
| nhan đề | đậm 14, canh giữa | style `RALs-Title` (`b`, `sz=28`, `jc=center`) |
| tác giả | nghiêng, canh giữa, nối tên cuối bằng `&` | style `RALs-Authors` |
| mục cấp 1 | số **Ả Rập** "1.", đậm, **canh giữa** | style `RALs-Heading1` |
| mục cấp 2 | "1.1." đậm-nghiêng, canh trái | style `RALs-Heading2` |
| mục cấp 3 | "1.1.1." nghiêng | style `RALs-Heading3` |
| bảng | **không kẻ dọc**, chỉ ba đường ngang | `tblBorders` + `tcBorders` của bảng mẫu |
| nhan đề bảng | **đặt TRÊN**: "Bảng n" đậm dòng riêng, tiêu đề nghiêng dòng dưới, canh trái | style `RALs-TableCaption` |
| nội dung bảng | **10 pt** (lệnh `\bangchu`) | style `RALs-APA-Table` (`sz=20`) |
| ghi chú bảng | đặt dưới, **9 pt**, "Ghi chú." nghiêng | style `RALs-TableNote` (`sz=18`) |
| nhan đề hình | **canh giữa** (khác nhan đề bảng canh trái) | style `RALs-FigureCaption` |
| tài liệu tham khảo | **APA 7th**, xếp bảng chữ cái, thụt treo 0,5 in, sang trang mới | style `RALs-ReferencesList` + tiêu đề "References (APA 7th style)" |
| cuối bài | Bionote + tên thật, bút danh, học hàm/học vị, nơi công tác, địa chỉ, điện thoại, email | template có mục Bionote; phần còn lại theo thông báo hội thảo |

Template **không có tiêu đề chạy trang** ⇒ đã bỏ dòng "VCL 2026 – …" và hai đường kẻ ngang
mà bản trước có; chỉ giữ số trang.

## ⚠️ Hai chỗ template mâu thuẫn với thông báo hội thảo

| | thông báo | template | đang dùng |
|---|---|---|---|
| giãn dòng thân bài | 1,5 | đôi (`line=480`) | **1,5** — chủ luận văn quyết 29/8 |
| độ dài tóm tắt | 100–150 từ | 150–250 từ | **đúng 150 từ** — thoả cả hai |

Tóm tắt để đúng 150 từ là cố ý: đó là con số duy nhất nằm trong cả hai khoảng.
Đếm lại bằng:
```
python3 - <<'PY'
import re
s=open('main.tex',encoding='utf-8').read()
i=s.index('Sinh hướng dẫn thao tác từ ảnh'); j=s.index('%% -- Từ khoá')
ab=s[i:j]; ab=ab[:ab.rindex('\\par}')]
for a,b in [(r'\%','%'),('$',''),('{,}',',')]: ab=ab.replace(a,b)
print(len([x for x in ab.split() if re.search(r'\w',x)]), 'từ')
PY
```

## Còn treo trước khi nộp

1. ✅ **Số điện thoại — ĐÃ ĐIỀN 30/8** cho tác giả 1: `(+84) 0764 484 984`.
   Tác giả 2 để trống theo quyết định của chủ luận văn.
2. **Địa chỉ** — đang ghi địa chỉ cơ quan (227 Nguyễn Văn Cừ). Đổi nếu ban tổ chức muốn
   địa chỉ liên hệ cá nhân.
3. **Định dạng nộp**: template phát ra là `.docx`, ta nộp `.pdf`. Thông báo không nói rõ
   bắt buộc `.docx`. Máy này không có `pandoc` lẫn `libreoffice` nên chưa chuyển được.
   Nếu ban tổ chức đòi Word thì phải chuyển trên máy khác.
4. ✅ **Chính sách trùng lặp — ĐÃ KIỂM 29/8, không vi phạm.**
   · **VCL không có điều khoản nào** về bài chưa công bố / nộp đồng thời / bản quyền —
     kiểm ba lượt độc lập (CFP VCL2026, trang overview, và thể lệ VCL2025).
   · **FAIR thì có**: *"Submissions must be original and not under consideration for
     publication elsewhere"*, kèm cam kết bản quyền IEEE.
   · Điều khoản đó áp cho *cùng một bài* gửi hai nơi. Đây là hai bài khác nhau, chia số
     độc quyền, phần chung chỉ là quy mô dữ liệu. **Trích chéo dạng "đang bình duyệt"
     chính là cách khai minh bạch — giữ nguyên, đừng gỡ.**

5. 💰 **Phí tham dự: 1.000.000 VNĐ cho mỗi báo cáo được duyệt**, tác giả tự lo đi lại.
   (Đọc từ CFP ngày 29/8; trước đó không ghi ở đâu.)
