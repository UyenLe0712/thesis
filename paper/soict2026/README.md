# Bài SOICT 2026 — thư mục nộp

The 15th International Symposium on Information and Communication Technology · TP.HCM, 4–5/12/2026
Kỷ yếu **Springer CCIS** (template LNCS `llncs.cls`) · https://soict.org/submission/paper-submission/

| mốc | ngày (tra 21/9/2026) |
|---|---|
| abstract · full paper | 20/9/2026, **EasyChair còn mở tới 25/9** |
| báo kết quả | 12/10/2026 |
| camera-ready | 23/10/2026 |

Nộp tại: https://easychair.org/conferences/?conf=soict2026

**Quy cách:** tối đa **12 trang không kể tài liệu tham khảo** · bình duyệt **một chiều mù**
(ghi tên tác giả + đơn vị) · PDF **không đánh số trang** (`\pagestyle{empty}` đã có sẵn; bỏ hai
dòng đó khi nộp camera-ready) · ít nhất 3 phản biện.

## Tệp

| tệp | là gì |
|---|---|
| `main.tex` | bản thảo. **Chép lại 21/9 từ 15 ảnh chụp màn hình** trong `_nguon_anh/` (bản gốc nằm ở máy khác, không có trong kho) |
| `main.pdf` | bản dựng bằng tectonic |
| `_nguon_anh/soict2026_main_tex_15_anh_21_9.zip` | 15 ảnh gốc, dòng 1–797 của `main.tex`, không commit (`.gitignore`) |

⚠️ Chép từ ảnh ⇒ có thể lệch từng ký tự. Nếu còn bản gốc trên máy kia, **diff với bản này trước
khi nộp**.

## Những gì đã đổi so với ảnh (21/9) — chỉ trình bày, không đổi chữ nào của nội dung

1. `\setlength{\emergencystretch}{1.5em}` — gỡ 3 dòng tràn lề ở Related Work / Data / Systems.
2. Bảng 1: thêm `\par` trước chú thích †. Bản gốc thiếu nên chú thích dính vào dòng của bảng
   và in lệch sang phải (lỗi này cũng xảy ra trên Overleaf).
3. Bảng 1, 3, 4 dùng `\small`; Bảng 2 thêm `\resizebox{\textwidth}` (tràn 69 pt).
4. Bảng 3: tách dòng *"same analysis against the second baseline run"* thành hai dòng (tràn 28 pt).
5. Hình 1: dời nhãn `hit-disk / no gate` sang phải điểm (bản gốc đè lên số 70 của trục x).

## Lệnh dựng

```
rm -f main.log && tectonic -X compile main.tex --outdir . --keep-logs
grep -oE "Output written on main\.xdv \([0-9]+ page" main.log
grep -c Overfull main.log        # phải là 0
```

Trạng thái 21/9 (sau khi cắt): **14 trang = 12 trang thân bài + References bắt đầu đầu trang 13**,
0 overfull, 23 tài liệu đều được trích. Trang 12 còn ~2–3 dòng trống.

## Nội dung đã cắt / viết lại 21/9 (user duyệt: "phần nào không quan trọng thì cắt")

Bản trước khi cắt: scratchpad phiên 21/9, `main_soict_truoc_cat.tex` (không giữ trong kho).
- Bỏ đóng góp thứ tư "A reusable instrument" (Discussion đã nói việc tính lại từ tệp dự đoán) ⇒ "three contributions".
- Bỏ đoạn phân định chữ *executability* với Open Grounded Planning, kèm tài liệu `ogp`.
- Bỏ câu kiểm phép ghép hai kho (48% vs 20% trên 400 bước).
- Bỏ đoạn độ dài / độ đa dạng câu ở §6.4 (hai cột vẫn nằm trong Bảng 4).
- Bỏ câu thành công mức episode (+8,55 / +2,90) và câu 1.345 episode ở mục Data.
- Bỏ câu lặp "listener đóng băng" ở §4.2; viết gọn Kết luận.
- **Viết lại ý OS-Atlas** ở Related Work và Discussion: bài agent đã tách Type · Grounding · SR
  (OS-Atlas, ICLR 2025); đóng góp của bài là đưa thói quen đó sang chấm câu bằng người nghe, thay cho
  câu cũ "this literature does not report" (phản biện bác được).

## Lượt review 21/9 (sau khi sửa tóm tắt)
- Khổ A4 (`a4paper`); tóm tắt viết lại câu giữa, 244 từ.
- Limitations rút còn một đoạn "Limitations and Future Work" (user quyết: không nhắc một hạt giống, không nhắc đánh giá người).
- Sửa tác giả DisCLIP (Bracha, Shaar, Shamsian, Fetaya, Chechik — BMVC 2023) và câu trích DisCLIP; tên đầy đủ báo cáo Phi-4-Mini.
- Intro: ScreenSpot click accuracy không có cổng; chỉ khi agent benchmark áp vào bước mới thành phép hội.
- Bảng 3 chia theo $A$ (252 bước), không theo $A\wedge T$ (256) — tính lại từ tệp thô khớp 34,92 / 62,65 / 61,58 và 5,42% / +36,36 / −1,61.
- Mục 6.3: "trùng câu" là trùng sau khi bỏ hoa/thường và dấu câu (45,93%, Δ −0,24, 329/281; đối chứng 154/129).
- CE2 là đối chứng của chặng ưu tiên, không phải của cả chuỗi; "neither quantity moves" nói rõ là giữa chặng DESC và chuỗi đầy đủ.

## ĐÃ NỘP 21/9/2026 — EasyChair #5577
Track: Multimedia Processing, Computer Vision, and Multimodal Intelligence. Người nộp
24C15039@student.hcmus.edu.vn. ⚠️ Mail xác nhận chỉ liệt kê MỘT tác giả (thiếu thầy Nguyen Hong Buu Long)
và tên hiện "Uyen Le Doan Phuong" — cần sửa trên EasyChair trước 25/9. Báo kết quả 12/10.
