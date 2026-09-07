# Luận văn thạc sĩ — thư mục `thesis/`

Bản LaTeX của luận văn **"Phát sinh tự động hướng dẫn sử dụng phần mềm dựa trên LLM từ các trường hợp sử dụng và giao diện người dùng"**,
trình bày theo mẫu luận văn thạc sĩ Trường ĐH Khoa học Tự nhiên, ĐHQG-HCM.

---

## 1. Biên dịch

```bash
cd thesis
./build.sh          # hoặc:  tectonic main.tex
```

Ra `thesis/main.pdf`. Hiện **117 trang** (bản 5/9/2026), biên dịch sạch, không có tham chiếu hay trích
dẫn hỏng.

Yêu cầu: `tectonic` (đã có sẵn ở `~/bin/tectonic` trên máy này). Tectonic tự tải các gói
cần thiết ở lần chạy đầu, không cần cài TeX Live.

Font: TeX Gyre Termes/Heros/Cursor qua `fontspec` — đúng bộ đã kiểm chạy được với tiếng
Việt trong `paper/fair2026/main.tex`. Cỡ chữ 13pt qua gói `fontsize`; nếu môi trường khác
không có gói này thì xoá dòng `\usepackage[fontsize=13pt]{fontsize}` trong `main.tex`,
tài liệu về 12pt và vẫn biên dịch được.

---

## 2. Cấu trúc

| Tệp | Nội dung |
|---|---|
| `main.tex` | Tiền tố, khai báo font, **các ô thông tin sửa được** (tên đề tài, GVHD, khóa…) |
| `chapters/00_bia.tex` | Bìa ngoài + bìa trong |
| `chapters/01_camdoan_camon.tex` | Lời cam đoan, Lời cảm ơn |
| `chapters/02_vietat.tex` | Danh mục từ viết tắt, khái niệm, thuật ngữ |
| `chapters/03_trangthongtin.tex` | Trang thông tin luận văn (tiếng Việt + tiếng Anh) |
| `chapters/ch1_gioithieu.tex` | Đặt vấn đề · động lực · mục đích · nghiên cứu liên quan · phạm vi · đóng góp |
| `chapters/ch2_tongquan.tex` | Nền tảng: VLM, LoRA/QLoRA, GUI grounding, AndroidControl, **vì sao thước cũ gãy** |
| `chapters/ch3_dulieu.tex` | Xây dựng bộ dữ liệu: ghép nguồn, OCR, nhãn mô tả, 4 nhánh, 9 bất biến |
| `chapters/ch4_phuongphap.tex` | "Mô tả trước, phát ngôn sau" · cấu hình huấn luyện · các nhánh · đăng ký trước |
| `chapters/ch5_thuocdo.tex` | **Thước executability**: định nghĩa, chọn luật trúng, cổng chặn, trần, bơm lỗi, thống kê |
| `chapters/ch6_thucnghiem.tex` | Kết quả 3 nhánh · McNemar · 6 đòn phản biện · phân tích lỗi · nhánh chưa chạy |
| `chapters/ch7_ketluan.tex` | Đóng góp · hạn chế · hướng phát triển |
| `chapters/ch8_congtrinh.tex` | Công trình đã/sẽ công bố |
| `chapters/99_tailieu.tex` | Tài liệu tham khảo (27 mục) |
| `figures/fig_voronoi.png` | Hình minh hoạ vì sao ngưỡng dung sai không đủ |

---

## 3. ⚠️ Những ô cần bạn điền / kiểm lại trước khi in

Tìm trong PDF bằng chữ **`[CẦN ĐIỀN:`** và **`[CHỜ SỐ:`** — chúng in màu đỏ nên không
thể bỏ sót.

### 3a. Thông tin hành chính — sửa ở đầu `main.tex`

| Biến | Giá trị hiện tại | Trạng thái |
|---|---|---|
| `\TenDeTai` | Phát sinh tự động hướng dẫn sử dụng phần mềm dựa trên LLM từ các trường hợp sử dụng và giao diện người dùng | tên đã đăng ký (user gửi 5/9) |
| `\HocVien` | Lê Đoàn Phương Uyên | |
| `\GVHD` | TS. Nguyễn Hồng Bửu Long | **kiểm lại học hàm/học vị** |
| `\MSHV` | 24C15039 | suy từ email trong `paper/fair2026/main.tex`, **cần xác nhận** |
| `\Khoa` | 33 | **CẦN ĐIỀN khóa đào tạo thật** |
| `\NamBaoVe` | 2026 | |
| `\MaNganh` | 8480107 | mã ngành Trí tuệ nhân tạo |

### 3b. Nội dung chờ số

| Chỗ | Nội dung | Điền khi nào |
|---|---|---|
| Bảng 6.1 (`tab:chinh`) | các dòng S1/202, S2, S2r, S2-nopoint, B-infer | sau khi chấm xong từng nhánh |
| Mục 6.7 | bảng ghép cặp cho $\Delta = $ S2 − S1 | sau khi có S2 |
| `ch8_congtrinh.tex` | trạng thái nộp bài FAIR 2026 | sau 31/8/2026 |
| `99_tailieu.tex`, mục `gcot` | danh sách tác giả arXiv:2503.12799 | trước khi in |

### 3c. Chỗ điền số về sau — đã bố trí sẵn

Khi các nhánh chạy xong, số chỉ cần điền vào **ba chỗ**, đã ghi rõ ở cuối Mục 6.7:
dòng tương ứng trong Bảng 6.1, một bảng ghép cặp theo mẫu Bảng 6.3, và ba lát cắt đã
khai trước ở Mục 4.6.

---

## 4. Nguyên tắc đã tuân thủ khi viết

Những nguyên tắc này ràng buộc nội dung và **không nên phá khi sửa về sau**:

- **Không có số nào bịa.** Mọi con số truy được về `report/108`, `report/110`,
  `report/112`, `paper/fair2026/main.tex` hoặc `runs/*.json`.
- **Dùng số đã cập nhật, không dùng số đã rút.** Cụ thể: trần là **75,7%** (không phải
  70,0% như slide cũ), trùng ứng dụng là **95,6%** (không phải 92%), MDE ghép cặp đo được
  là **2,2 pp**.
- **Không viết bất kỳ phát biểu nào về hiệu quả của S2** — nhánh đó chưa chạy.
- **Không dùng chữ "đầu tiên" / "mới" / "cơ chế mới"** cho thành phần mô hình; dòng REG
  phân biệt đã chiếm ý từ Mao CVPR 2016.
- **Không viết "bộ trỏ chưa từng thấy màn hình di động"**; viết "không được huấn luyện
  trên AndroidControl" — và với UGround thì phải khai ngược lại là nó **có** dùng
  AndroidControl (Mục 7.2).
- **Tiền ấn phẩm được đánh dấu là tiền ấn phẩm** trong danh mục tài liệu (Qwen2.5-VL,
  Shikra, GCoT).
- Giới hạn được khai **kèm số bác bỏ hoặc xác nhận**, không khai suông.

---

## 5. Quan hệ với các tệp khác trong kho

| Cần gì | Mở tệp nào |
|---|---|
| Cơ chế kỹ thuật, giải thích dài | `report/112_HIEU_TOAN_BO_KY_THUAT.md` |
| Đang ở đâu, việc kế tiếp | `report/109_BAN_DO_HIEN_TAI.md` |
| Thiết kế đã niêm phong, luật đọc kết quả | `report/106_DANG_KY_TRUOC.md` |
| Số nào tin được, số nào đã rút | `report/108_DA_LAM_DUOC_GI.md` |
| Bài báo tiếng Anh cùng nội dung | `paper/fair2026/main.tex` |
| Slide bảo vệ | `LUAN_VAN_SLIDE.pptx` |
