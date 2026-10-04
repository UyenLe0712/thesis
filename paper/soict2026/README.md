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

## ⭐ Bản GUIStep (chép từ 14 ảnh nhận 26/9) — `guistep/` — KHÁC bài đã nộp #5577

⚠️ **Đây là bài khác**, không phải bản "strictness ladder" của `main.tex` (đã nộp 21/9). Khung mô hình
trước: nhan đề *GUIStep: A Compact Vision–Language Model for GUI Step Instruction Generation*; ba
cấu hình GUIStep-S/D/P (= S1/101 · S2/101 · MIN-DESC/101) + đối chứng CE2; thước chính **D.3**; kết
quả 66,5 vs 53,6 (Base), P − S = +1,05 (p=0,078, không ý nghĩa) ⇒ bài **tự khai** phần lớn công thuộc
SFT trơn. Không đè `main.tex` cũ.

| tệp | là gì |
|---|---|
| `guistep/main.tex` | bản nộp: chép từ ảnh + sửa giọng văn + sửa lỗi (danh sách dưới) |
| `guistep/main_chep_tu_anh.tex` | bản chép trung thành trước khi sửa — `diff` với `main.tex` ra đúng các chỗ đã đổi |
| `guistep/fig1_screen.png` | dựng lại từ `train_ac/images/ep11904_s3.png`, cắt (0,0,1080,1104), khớp đúng toạ độ vòng tròn 14,2% / 33,2% ghi trong nguồn |
| `_nguon_anh/soict2026_guistep_main_tex_14_anh_26_9.zip` | 14 ảnh gốc, dòng 1–717 (không commit) |

Dựng: `cd guistep && rm -f main.log && tectonic -X compile main.tex --outdir . --keep-logs` →
**11 trang gồm cả tài liệu tham khảo (trần 12 không kể tham khảo), 0 overfull, 0 tham chiếu hỏng,
27/27 tài liệu được trích.**

**Đối chiếu số với `runs/` (26/9):** bảng chính + KTC (`d3_ktc.json`) · P−S +1,05 p=0,078 · D−S −1,86 ·
P−CE2 +0,52 [+0,02;+1,00] · bảng văn bản (`text_metrics_coco/them.json`) · −34,2 điểm khi bỏ tên (193
bước, `report/139`) · 33,1% (n=121) và 8/10 tiêu chí (`report/106`) · 97,5% và 0,336 (`report/112`) ·
UI-Venus +11,14 → +11,02 **tính lại từ `runs/venus/*_raw.jsonl`** ra đúng · **12 ô Bảng 1 (lát 800) khớp
`runs/luat_d3.json`** (kể cả khoảng dùng được 68,9 / 62,9 / 62,5).
**Chưa đối chiếu được, lấy nguyên từ ảnh (tra trước khi nộp nếu có thời gian):** −0,09 [−0,93;+0,79] của 1.139
câu viết lại dưới D.3 (số Voronoi trong CLAUDE.md là +0,35) · 4,7 điểm khi bỏ vị trí · trung vị hộp 1,0% /
cửa sổ 7,8% · 15 bước không có hộp · 1.493 bước sai / 50 sai loại thao tác · 12 động từ, 9 cặp đảo cực
tính · 0,0/99,6/100,0/91,1% của bảng bơm lỗi (số bản 3 của `report/106` khớp, nhưng chạy dưới Voronoi).

**Lỗi bắt được khi chép (đã sửa trong `main.tex`):**
1. ⛔ **Hình 1 ghi *"held-out episode"* nhưng ep11904 nằm trong `train.jsonl` (64.567 bước)** — S1/MIN đã
   train trên bước này; câu "generated" lấy từ `runs/noisuy/preds_val_a0.00.jsonl` (α=0 = MIN-DESC).
   Chú thích nay ghi "training-split episode … not a scored example".
2. ⛔ **Mục `groundersunderstand` sai** (tiêu đề *"On the robustness of GUI grounding models…"*,
   arXiv:2408.04744 — không truy được). Đã thay bằng bản đúng như `thesis/chapters/99_tailieu.tex`:
   Jandial, Li, Wagle, Koishida, *Do GUI grounders truly understand UI elements?*, Findings ACL: EACL
   2026, tr. 2772–2785.
3. Bảng 2 chỉ có 8 dòng nhưng văn bản viết "đạt 8/10 tiêu chí" ⇒ chú thích nay nêu ba tiêu chí lược đi
   (đều đạt: 0,0 / 100,0 / 100,0, lấy từ `report/106` bảng bản 3).
4. Bảng 4 chỉ in đậm SPICE cho S trong khi văn bản viết S dẫn BLEU-4, CIDEr-D, SPICE ⇒ in đậm đủ ba.
5. Tiêu đề bị ngắt lẻ chữ *for* và Hình 1 đẩy sang trang 2 làm trống 1/3 trang 1 (đã sửa: ngắt tiêu đề lại, `[!ht]`). Hai chỗ tràn lề (hai URL Hugging Face → chú thích chân trang; Bảng 4 → `resizebox`), Bảng 2 căn trái.

**Giọng văn AI đã bỏ (giữ nguyên số và kết luận):** cụm *"rather than"* từ **14 → 1** lần (lượt cuối 26/9: bỏ thêm "only", "however" đệm, "thus", câu CIDEr lặp ở Related Work, "second difficulty" → "a further difficulty"); bỏ *"the picture it
gives is more qualified"*, *"recover their added complexity"* (tóm tắt nay nói thẳng: D −1,9, P không hơn
S có ý nghĩa), *"Overall"* ×2, *"moreover"*, *"itself"*, *"Applications may occur in both partitions"* →
*"The same app can appear in both partitions"*; câu mở đầu bài viết lại; *"second difficulty"* nêu rõ.

**Chưa làm / user quyết:** (a) EasyChair #5577 đang là bản *ladder*; nộp bản này nghĩa là **thay bài** —
xác nhận với thầy, và nhớ sửa danh sách tác giả (còn thiếu thầy Long trong mail xác nhận). (b) Nếu muốn
Hình 1 là ví dụ **test** thật thì phải chọn một bước trong `test.jsonl` rồi viết lại ba dòng chữ trong hình.

> **4/10/2026:** ảnh gốc đã xoá khỏi đĩa sau khi chép xong (bản chép là tệp .md/.tex trong thư mục này). Ảnh đã từng commit thì vẫn lấy lại được từ lịch sử git; ảnh/zip chưa commit thì không còn.
