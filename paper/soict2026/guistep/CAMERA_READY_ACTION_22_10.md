# SOICT 2026 — CAMERA-READY: bối cảnh + ACTION (lập 22/10/2026)

**Hạn: 30/10/2026** (còn 8 ngày; README cũ ghi 23/10 là SAI, đã thay). Hội nghị 4–5/12/2026, TP.HCM.
Nguồn thư: 5 mail user dán 22/10 (chấp nhận oral · mail camera-ready · mail template mới · mail hướng dẫn nộp).
Trang quy cách đã tra 22/10: https://soict.org/submission/camera-ready-submission/

## 1. Kết quả

- **ACCEPTED, ORAL + xuất bản Springer CCIS** (DBLP, Scopus, EI…). Bài trình bày **15 phút gồm hỏi đáp**; có thể kèm poster (in miễn phí, gửi file).
- Tiêu đề trong mail: *GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation* — khớp `guistep/main.tex`.
- ✅ Paper ID = **5590** (user xác nhận 22/10; #5577 trong README cũ là số cũ).
- ✅ **Một tác giả: Uyen Le Doan Phuong** (thầy không đứng tên, user quyết 22/10). `main.tex` đã sửa, form đã điền khớp.

## 2. Quy cách (tra từ trang camera-ready)

| mục | yêu cầu |
|---|---|
| Số trang | **12–15 trang TÍNH CẢ hình, bảng, tài liệu tham khảo** (bản hiện tại **11 trang gồm cả tham khảo** ⇒ **thiếu ít nhất 1 trang**, trần cũ "12 không kể tham khảo" hết hiệu lực) |
| Mẫu | Springer CCIS (`llncs.cls`, đang dùng; trang web không cấp mẫu riêng, chỉ trỏ hướng dẫn Springer) |
| Số trang in | bỏ `\pagestyle{empty}` (dòng 20) và `\thispagestyle{empty}` (dòng 36) |
| Tác giả liên hệ | **đúng MỘT**, đánh dấu trên bài, nên dùng ký hiệu phong bì `\email`/`\thanks{[ ]}`; họ tên + email phải **trùng** ở: bài · form · txt · EasyChair |
| Sửa tên/tiêu đề/email | làm **trên EasyChair TRƯỚC khi ký** (sửa trên form không đồng bộ sang Springer) |
| Đạo văn | trang yêu cầu sửa các đoạn bị gắn cờ: kiểm xem mail chấp nhận/EasyChair có báo đoạn nào không |
| Đăng ký | mỗi bài cần **một đăng ký full** thì mới vào kỷ yếu; trang không ghi hạn riêng ⇒ xem https://soict.org/registration/ |
| Statement phát hành | trang **không** ghi đoạn chữ phải chèn trong bài (mail 1 nói "include the permission statement" — chỉ hiểu là form License to Publish; hỏi ban tổ chức nếu muốn chắc) |

## 3. Việc hành chính (có hạn cứng, ưu tiên trước)

1. [x] Tác giả liên hệ = Uyen Le Doan Phuong, `24C15039@student.hcmus.edu.vn` (đã vào bài, form).
2. [ ] **Kiểm EasyChair**: danh sách tác giả hiện một người (khớp), tên "Uyen Le Doan Phuong", email trùng; không cần sửa nếu đúng như vậy. Làm trước khi ký.
3. [ ] **Form**: đã điền sẵn `License_to_Publish_5590_dien_san.docx` (tiêu đề, tên tác giả, tác giả liên hệ, Print Name, Email). **User tự**: mở bằng Word kiểm, in, **viết ngày, địa chỉ, ký mực**, quét PDF (chữ ký số không nhận). Ghi chú: form nói không đổi danh sách tác giả sau khi nhận bài.
4. [ ] `Corresponding_Author.txt`: tiêu đề · họ tên · email người liên hệ.
5. [ ] **Dựng gói**: `Source/` (main.tex, llncs.cls, fig1_screen.png, mọi tệp để dựng lại PDF; bibliography đang nằm trong `main.tex`) + txt + PDF form đã ký → **một ZIP**.
6. [ ] **Upload trên EasyChair** ở vai "proceedings author" (SOICT 2026 Proceedings): PDF cuối + ZIP, **cập nhật mục có sẵn, đừng tạo submission mới**, nhấn nút lưu, mở lại danh sách tệp kiểm cả hai.
7. [ ] **Đăng ký hội nghị** (ít nhất một tác giả, full) — kiểm hạn ở trang registration. Chuẩn bị slide 15 phút (xem `slides/`, tạo deck riêng; chưa có).

## 3b. TIẾN ĐỘ 24/10 (đã sửa vào `main.tex`, dựng 14 trang, 0 overfull)

Thứ tự ưu tiên theo số reviewer nêu: ① độ tin cậy thước (R2·R3·R4) ② viết khó theo dõi (R1·R3) ③ P không hơn S, tính mới hẹp (R2·R3) ④ một dữ liệu/một backbone (R1·R4) ⑤ thiếu baseline ngoài (R2·R4).

- [x] **A1** 11,14 / 11,02 ghi rõ là lát 2.532 bước; +11,9 của Bảng 3 là toàn 4.463 bước.
- [x] **A2** "1.443 mô tả sai phần tử" → "không đạt kiểm tra định vị", nêu ba nguyên nhân có thể, bỏ kết luận "element naming is the main problem".
- [x] **A3 + B1** bỏ "upper bounds". Chạy lại bộ bơm lỗi dưới D.3 (`harness/exec_injection_d3.py` → `exec_injection_d3_results.json`, cùng mẫu/hạt giống/ngưỡng): **ĐẠT 6/10 (Voronoi 8/10)**. Lân cận gần 25,6% · lân cận vừa 82,0% (Voronoi 99,6) · xa 94,5% (ngưỡng 95, trượt 0,5) · kết oan paraphrase 6,5% (Voronoi 0,0). Phần bị lọt tập trung ở hộp lớn (trung vị 14,7% màn vs 0,9%). Bảng 2 thay bằng bảng hai cột D.3 | Voronoi, đủ 10 tiêu chí. Phải khai là xấu hơn bản cũ.
- [x] **B2** thay 17,3% bằng số có script: `harness/soict_camera_ready.py` → `runs/soict_camera_ready.json`. Câu lặp (hạ chữ thường, bỏ dấu câu) **2.347/4.463 = 52,6%**; nguyên văn chỉ cắt khoảng trắng 43,3%. Mục 6.3 + Bảng 4: S−Base +15,0 (lặp) vs +8,4 (chưa lặp); P−S +0,3 vs +1,9 (p=0,031); app chưa thấy 78 bước/20 app (không phải 22 như ghi chú cũ).
- [x] **B3** McNemar → bootstrap cụm (cụm = app, bước không có app thì cụm theo tác vụ). P−S p=0,073 · P−CE2 +0,52 p=0,043 (vẫn có ý nghĩa) · D−S p=0,003. Đã tự kiểm: Δ và KTC khớp tuyệt đối `runs/d3_ktc.json`.
- [x] **B4** khai hạt giống đơn ở mục 6.2 và Limitations.
- [x] **B5 (một phần)** Phụ lục A: prompt sinh (nguyên văn tiếng Việt kèm dịch), prompt người nghe, luật chấm. Độ trễ không đo, khai trong Limitations. ⚠️ **Chưa có liên kết mã/adapter trong bài**: cần user bật công khai GitHub Release rồi mới thêm.
- [x] **C3** Limitations viết lại (bốn đoạn: tính hợp lệ của thước, phạm vi, giao thức đánh giá, tính mới).
- [ ] **C1** tách khung chung khỏi AndroidControl + sơ đồ tổng quan · **C2** bảng định nghĩa S/D/P/CE2 · **C4** soát giọng AI · **B7a** user chấm tay 60–100 câu · liên kết mã.
- [x] **25/10** C1: tách §3 *The GUIStep Framework* (khung chung, Hình 2 tổng quan) khỏi §4 *Experimental Setup on AndroidControl*; C2: Bảng 1 định nghĩa S/D/P/control; C4: giảm "therefore", bỏ "79,4% của trần" (thay bằng khoảng cách 17,3 điểm); thêm đóng góp thứ ba (ablation có nhánh so sánh). Bổ sung theo phản biện: thứ tự 5 hệ giữ nguyên dưới Voronoi (R2/R4 lân cận); người nghe Phi-4 ngoài họ Qwen: câu chuẩn 54,9 · S 44,6 · backbone 38,2, S−backbone +6,4 [+5,1; +7,7] (R2/R3/R4); hàng `gui_sel` là biến thể chọn-đích-rồi-diễn-đạt, D.3 62,4 [60,5; 64,2], −3,1 so S (R2/R4), khai lệch ba biến. Số tính lại từ tệp thô (script `harness/soict_them.py`, D.3 khớp bài tuyệt đối). Hai trích dẫn mới (Phi-4-Mini arXiv:2503.01743, Set-of-Mark arXiv:2310.11441) đã kiểm tại arXiv. **15 trang (trần), 0 overfull, 0 undefined.**
- ⚠️ Còn phải đưa user duyệt: câu "Since confusion between neighbouring controls … absolute levels should be read with that weakness in mind" (mục 5.2) và đoạn Limitations nói thẳng "fails four of ten criteria".

## 4. Việc sửa bài theo phản biện — ĐÃ KIỂM LẠI 22/10 bằng mã và tệp thô trong kho

Bài hiện **11 trang**, cần 12–15 (gồm tham khảo) ⇒ có 1–4 trang để thêm nội dung bên dưới.
Nhãn: **[0]** chỉ sửa chữ · **[CPU]** tính từ tệp có sẵn, máy nhà · **[KG]** cần Kaggle T4 (0 đồng) · **[TAY]** người làm tay.

### ⛔ USER QUYẾT 22/10: KHÔNG CHẠY KAGGLE cho bài này ⇒ B6 và B7b bên dưới BỎ; B5 không đo độ trễ (ghi thẳng trong Limitations là chưa đo, chỉ nêu cỡ mô hình, lượng tử hoá 4-bit, đỉnh VRAM khi train); thay baseline bằng `gui_sel` + khai giới hạn; người nghe thứ hai chỉ khai số Phi-4 đã có (S1, câu chuẩn).

### ✅ KẾT LUẬN VỀ KAGGLE: phần BẮT BUỘC không cần Kaggle. Kaggle chỉ cho hai việc TUỲ CHỌN (mục B6, B7b)

Lý do (đã kiểm): bộ bơm lỗi (`harness/exec_injection_v3.py`) **không gọi bộ trỏ lần nào**: vị trí điểm dự đoán được mô phỏng bằng độ lệch tổng hợp, chỉ cần hàm chấm `score_step`. Mọi phép tách nhóm (câu lặp / app chưa thấy), p theo cụm và con số 11,14 đều tính được từ `runs/*_raw.jsonl` + `descriptors.jsonl` (đã kiểm chạy được, mục dưới).

### A. Ba lỗi cụ thể (Reviewer 2) — làm trước, đều [0]/[CPU]
- [ ] **A1 [0] Hai con số 11,14 và ≈11,9 ĐÃ TRUY ĐƯỢC, cả hai đúng, chỉ khác tập chấm** (tính lại 22/10 từ tệp thô, D.3): S1 − Base **+11,14** là UGround trên **lát 2.532 bước** của phép đối chiếu (59,48 − 48,34); **+11,02** là UI-Venus trên đúng lát đó (59,76 − 48,74); **+11,90** là UGround trên **toàn 4.463 bước** (65,49 − 53,60, Bảng 3). Việc: sửa dòng 366–369 của `main.tex` ghi rõ "on the 2,532-step slice" và nêu +11,90 cho toàn tập. Thêm một câu ở §5.3.
- [ ] **A2 [0] "1.443 mô tả sai phần tử" (dòng 453)** → "lỗi định vị (*localisation failures*)", ghi nguyên nhân có thể là người nghe sai hoặc hộp dựng lại sai; sửa câu kết "element naming is the main remaining problem" cho nhẹ lại (chỉ là giả thuyết, chưa kiểm tay; liên hệ mục B7a).
- [ ] **A3 [CPU] "upper bounds" (dòng 464–467)**: phản biện đúng, lập luận không có căn cứ (D.3 dùng hộp vàng, Voronoi dùng tâm các phần tử, hai vùng chấp nhận không lồng nhau). Cách làm: **chạy lại bộ bơm lỗi dưới D.3** (xem B1), thay Bảng 2 bằng số mới, bỏ câu "upper bounds".

### B. Thực nghiệm
- [ ] **B1 [CPU] Chạy lại bộ bơm lỗi dưới D.3.** Cách: copy `exec_injection_v3.py` → bản D.3, thay `judge()` bằng hàm D.3 (`harness/luat_d3.py`: điểm nằm trong `box` của `descriptors.jsonl`, cùng điều kiện action_ok ∧ toggle_ok). ⚠️ Phải quyết cách mô phỏng "điểm rơi vào phần tử lân cận" dưới D.3: điểm đặt tại tâm **hộp** của phần tử lân cận (không phải tâm nút); ghi rõ trong bài. Giữ nguyên 10 tiêu chí và ngưỡng đã khoá, báo kết quả dù xấu hơn. Ca kiểm: tập kiểm thật (test.jsonl), seed 20260805, n=400. Máy nhà, vài phút.
- [ ] **B2 [CPU] Tách "câu lặp" và "câu chưa thấy" + app chưa thấy.** ⛔⛔ **PHÁT HIỆN: con số 17,3% trong bài KHÔNG tái lập.** Truy nguồn: chỉ có ghi chú ở `report/118:238` và `report/129:451` ("17,3% nguyên văn trong 2,6% tập dạy"), không script. Đo lại 22/10: câu chuẩn của **4.463 bước chạm khớp NGUYÊN VĂN một `target_instruction` của tập dạy ở 41,2%** (43,3% sau `strip`; 6.958 bước: 43,8%); sau khi bỏ hoa/thường và dấu câu: 52,3%. Phải **thay 17,3% bằng số tính lại có script** và đưa script vào kho (gợi ý `harness/soict_tach_lap.py` ghi `runs/soict_tach_lap.json`).
  Kết quả sơ bộ (D.3, nhóm khớp sau chuẩn hoá = 2.333 bước, chưa-lặp = 2.130): Base 58,7 / 48,0 · **S 73,7 / 56,5** · D 71,7 / 54,8 · **P 74,0 / 58,4** · CE2 73,9 / 57,4. ⇒ mức tăng S − Base là **+15,0 ở nhóm lặp, +8,5 ở nhóm chưa thấy**: có đóng góp thật ở câu chưa thấy nhưng gần một nửa mức tăng đến từ việc học lại cách viết quen; P − S là +0,3 (lặp) và **+1,9 (chưa thấy)**. Nên đưa cả hai nhóm vào bảng. App chưa thấy (78 bước, 22 app): Base 56,4 · S 65,4 · D 59,0 · P 68,0 · CE2 66,7 (n nhỏ, chỉ khai).
  Chốt một định nghĩa rồi dùng cho mọi chỗ trong bài; thêm KTC bootstrap cụm.
- [ ] **B3 [CPU] p theo cụm thay cho McNemar.** `score_run.cluster_bootstrap` (cụm = tác vụ hoặc app, ghi rõ chọn cái nào) cho hiệu ghép cặp P−S, P−CE2, D−S, S−Base; báo p và KTC mới. Quan sát: P − CE2 +0,52 [+0,02; +1,00] có thể mất ý nghĩa; viết trung thực.
- [ ] **B4 [0] Hạt giống lặp**: chỉ S có hạt 101 và 202. Khai thẳng ở Limitations rằng D, P, CE2 một hạt, nên chênh nhỏ giữa cấu hình chưa kết luận được. Không train thêm (hạt 202 cho D/P tốn ~20 giờ A100, không đáng).
- [ ] **B5 [0/CPU] Độ trễ, bộ nhớ, prompt, luật chấm, mã.** Prompt đầy đủ + luật chấm → **phụ lục** (tính vào số trang, nên là chỗ lấp trang). Bộ nhớ train (đỉnh VRAM) lấy từ `report/110`, `harness/runbook/chon_may.md`. **Độ trễ suy luận chưa có số sạch trong kho** (chỉ có s/bước của lượt chấm trộn bộ trỏ): nếu muốn, đo bằng một ô Kaggle T4 ~20 phút (xem B7b), nếu không thì chỉ nêu cỡ mô hình (3B, 4-bit NF4) và ghi "chưa đo" là không được: phải đo hoặc bỏ yêu cầu này khỏi phần hứa trả lời. Mã: user quyết **công khai nếu reviewer đòi** ⇒ Reviewer 2 đã đòi ⇒ ghi liên kết GitHub Release (adapter có sẵn `noisuy-adapters-v1`; bật công khai trước khi nộp; kiểm không có khoá API/tên người khác trong kho công khai).
- [ ] **B6 [TUỲ CHỌN, KG] Baseline VLM khác**: Reviewers 2, 4. Rẻ nhất: Phi-4-multimodal zero-shot sinh câu trên **lát 800 bước** (~1 h sinh + chấm UGround ~1,5 h, T4, 0 đồng), cùng ảnh/mục tiêu/lịch sử/OCR. Nếu không chạy: dùng nhánh **`gui_sel` (chọn đích rồi diễn đạt, exec 56,13; D.3 62,38)** làm đại diện cho "pipeline chọn đích rồi nói", kèm cảnh báo lệch ba biến (`report/136`), và khai "không có hệ sinh câu ngoài so sánh được vì chưa tồn tại bản công khai cho đúng tác vụ".
- [ ] **B7 [QUYẾT user: làm nhỏ]** Đánh giá người nhỏ, gồm hai phần:
  - **B7a [TAY]** chấm tay **60–100 câu** trong 1.493 bước P sai: tôi dựng sẵn bảng (ảnh + câu + điểm trỏ + hộp vàng) cho user gán nhãn {câu mô tả sai phần tử · câu mơ hồ nhưng đúng · người nghe trỏ sai · hộp dựng lại sai}. Việc tay của user, khoảng 1–2 giờ. Kết quả trả lời trực tiếp A2 và Reviewers 2–3.
  - **B7b [KG, tuỳ chọn]** Phi-4 làm người nghe thứ hai: đã có Phi-4 cho câu chuẩn 54,9 · S1 44,6 · câu rỗng 15,9 · Base 38,6 (**dở dang, 3.566/4.463**). **Thiếu D (S2), P (MIN), CE2**. Nếu muốn có thứ tự S/D/P dưới người nghe độc lập: Kaggle T4×2, ~2,3 giờ mỗi nhánh (đã đo 3,36 s/bước/1 GPU) ⇒ tối thiểu **P + hoàn tất Base ≈ 3 giờ**, đủ D+P+CE2 ≈ 7–8 giờ, trong hạn mức 30 giờ/tuần, 0 đồng. Runbook sẵn: `harness/runbook/kaggle_som_listener.md`. Đặt lượt **trước 24/10** nếu muốn kịp. Có thể gộp đo độ trễ vào cùng phiên.

### C. Viết lại cho dễ đọc (Reviewers 1, 3), không cần tính toán
- [ ] **C1 Tách khung chung khỏi AndroidControl.** §GUIStep (dòng 206) → *Framework* (đầu vào; đích khai báo từ cây trợ năng; cặp ưu tiên khác ở phần tử khai báo; bộ chấm bằng người nghe; không phụ thuộc bộ dữ liệu) và *Experimental setup* (AndroidControl, Qwen2.5-VL-3B, QLoRA r, 2.560, 64.567 mẫu, phân chia). Thêm sơ đồ tổng quan.
- [ ] **C2** Một bảng nhỏ định nghĩa S / D / P / CE2 ngay đầu phần thực nghiệm.
- [ ] **C3 Limitations** viết lại bao đủ: chỉ một bộ dữ liệu và một backbone; chỉ bước chạm; lịch sử là câu chuẩn nên **không có tích luỹ lỗi** (Reviewer 4); người nghe là mô hình học; nhãn khai báo tự động; tính mới ở tầng mô hình hẹp (tự khai: phần lớn mức tăng đến từ SFT trơn); hạt giống đơn.
- [ ] **C4** Soát giọng AI còn sót (`rather than`, `---`).
- [ ] **C5 Thư trả lời phản biện không cần nộp** (camera-ready chỉ cần bản cuối), nhưng nên giữ bảng "phản biện → chỗ đã sửa" cho user dùng khi trình bày.

## 5. Thứ tự làm (8 ngày, hạn 30/10; nộp xong trước 29/10)

| ngày | việc |
|---|---|
| **22–23/10** | (nếu chọn B7b/B6) **đặt lượt Kaggle ngay** · A1–A3 · B2 (kể cả tìm nguồn 17,3%) · B3 · B1 |
| 24–26/10 | C1–C3 viết lại, phụ lục (B5), B7a user chấm tay · đọc kết quả Kaggle |
| 27–28/10 | dựng PDF (tectonic `--keep-logs`, 12–15 trang, 0 overfull), soát số khớp `runs/`, đưa user duyệt lần cuối |
| 28–29/10 | user in, ký form, quét; tôi dựng gói ZIP (`Source/`, txt, form PDF) |
| **29/10** | upload EasyChair, mở lại danh sách tệp kiểm |
| sau | đăng ký hội nghị, slide 15 phút (+ poster tuỳ chọn) |

## 6. Quyết định của user (22/10/2026)

1. **Tác giả đứng tên + liên hệ: Uyen Le Doan Phuong, `24C15039@student.hcmus.edu.vn`.**
2. **Paper ID = 5590** (README đã ghi, #5577 coi là cũ).
3. **Đánh giá người (B7): chỉ làm nhỏ**, làm "nếu người ta nói chắc" tức coi như có làm, quy mô nhỏ (chấm tay ~50–100 câu sai + thêm người nghe Phi-4).
4. **Công khai mã/adapter nếu reviewer yêu cầu**: reviewer 2 đã yêu cầu ("availability of code or checkpoints") ⇒ ghi liên kết GitHub Release trong bài (cần user bật công khai repo/Release trước khi nộp).
5. **Form Word**: đã điền sẵn → `License_to_Publish_5590_dien_san.docx` (cùng thư mục). Gốc: `thesis/SNCS_ProceedingsPaper_LTP_ST_SN_Singapore.docx` (mẫu Singapore, bản v2.0.1 12/2025).

### Form đã điền / còn trống
- Đã điền: Proposed Title · Author(s) Full Name(s) · Corresponding Author Name · Print Name · Email.
- **Còn trống, user tự viết tay khi ký**: chữ ký (mực), **Date**, **Address**.
- ⚠️ Form ghi: *"Changes of authorship … not permitted after acceptance"* ⇒ danh sách tác giả phải chốt **trước khi ký**.
- ✅ **22/10: thầy KHÔNG đứng tên** (user quyết). `main.tex` đã sửa còn một tác giả (Uyen Le Doan Phuong, ký hiệu (✉), email 24C15039@…), bỏ `\pagestyle{empty}`; dựng lại 11 trang, 0 overfull. Form đã khớp. Việc còn: EasyChair giữ nguyên một tác giả; không cần sửa gì thêm.
- (cũ) Form chỉ điền MỘT tác giả theo EasyChair/mail hiện tại. **Bản thảo `main.tex` đang ghi hai tác giả (thêm thầy Nguyen Hong Buu Long).** Hai cái phải khớp nhau. Còn treo: thầy có đứng tên không? Nếu có ⇒ sửa EasyChair thêm thầy, điền lại hai ô "Author(s) Full Name(s)", rồi ký; nếu không ⇒ bỏ thầy khỏi `\author` trong `main.tex` và để lời cảm ơn.
- Mở bằng Word để kiểm, máy WSL không có LibreOffice nên tôi chưa render thử ra PDF.
