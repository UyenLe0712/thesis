# Bản đăng ký trước — khoá thiết kế và luật đọc kết quả

**Ngày lập: 5/8/2026.** Văn bản này được commit vào git **trước khi chạy bất kỳ lệnh huấn luyện nào**. Mọi thứ ghi ở đây là cam kết: sau khi nhìn thấy kết quả, không được sửa ngưỡng, không được thêm nhánh, không được đổi thước.

Cơ sở thiết kế: `report/103_CHOT_THANH_PHAN.md` (bản 3, đã qua hai vòng phản biện độc lập và một vòng rà số tận PDF gốc).

> **Ghi chú về quy trình:** bản này lập trong tình huống chưa họp được với giảng viên hướng dẫn. Vì thiếu bước chốt miệng đó, văn bản này gánh luôn vai trò niêm phong thiết kế. Tài liệu đã gửi thầy: `report/103` (kế hoạch đầy đủ), `report/104` (bản trình bày), `report/105` (nguồn số). Nếu sau này thầy yêu cầu đổi thiết kế, việc đổi được ghi thành một mục sửa đổi có ngày tháng ở cuối file, **không sửa đè** lên phần đã khoá.

---

## 1. Câu hỏi nghiên cứu

**Câu hỏi chính.** Khi huấn luyện một mô hình thị giác - ngôn ngữ nhỏ sinh câu hướng dẫn giao diện cho người đọc, việc bắt mô hình sinh trước một dòng khai báo có cấu trúc về phần tử đích (vai trò · tên · toạ độ · dấu hiệu phân biệt) có làm câu sinh ra rõ hơn, đo bằng khả năng một bộ trỏ độc lập lần ra đúng phần tử, so với huấn luyện sinh thẳng câu hay không?

**Câu hỏi phụ.** (a) Phần đóng góp đến từ nội dung dòng khai báo hay chỉ từ việc chuỗi đích dài thêm? (b) Ô toạ độ đóng góp bao nhiêu trong hiệu ứng đó? (c) Nếu chỉ đưa thông tin phần tử vào đầu vào lúc suy luận, không huấn luyện, thì đạt được bao nhiêu? (d) Thêm khoản phạt câu mơ hồ vào hàm mất mát có cho tín hiệu không?

---

## 2. Các nhánh — khoá danh sách, không thêm bớt

| Mã | Tên gọi | Đích huấn luyện | Số hạt giống |
|---|---|---|---|
| **S1** | Bản thường | ảnh + mục tiêu + danh sách chữ OCR → câu | 2 |
| **S2** | Bản khai báo | ảnh + mục tiêu + danh sách chữ OCR → `<desc>…</desc>` + câu | 2 |
| **S2r** | Khai báo giả | như S2 nhưng nội dung `<desc>` lấy từ màn hình khác, toạ độ ngẫu nhiên, độ dài token ghép bằng bản thật theo từng mẫu | 1 |
| **S2-nopoint** | Bỏ toạ độ | như S2 nhưng `<desc>` không có ô `<point>` | 1 |
| **B-infer** | Đưa sẵn lúc chạy | dùng chính trọng số S1, lúc suy luận nối dòng mô tả phần tử vào đầu vào | 0 (không huấn luyện) |
| **S3-pilot** | Thử mức 2 | như S2, thêm khoản phạt lề giữa khai báo thật và khai báo giả từ nút hàng xóm; chỉ chạy trên lát 1.697 bước | 1 |

Hạt giống thứ ba cho S1 và S2 **chỉ được kích hoạt** khi khoảng cách giữa hai hạt giống của S1 lớn hơn hoặc bằng nửa hiệu số S2 − S1 quan sát được. Điều kiện này khoá từ bây giờ.

Mọi nhánh dùng: cùng bộ dữ liệu nguồn, cùng mô hình gốc Qwen2.5-VL-3B-Instruct, cùng siêu tham số QLoRA, cùng số lượt duyệt dữ liệu (2), cùng tập kiểm.

---

## 3. Thước đo

**Thước chính — executability.** Cắt bỏ toàn bộ phần `<desc>` khỏi đầu ra, chỉ giữ câu. Đưa câu cho một bộ trỏ độc lập khác họ với mô hình được chấm, cùng ảnh màn hình, nhận về một điểm. Bước được tính đúng khi: (i) loại thao tác mô hình mô tả khớp loại thao tác chuẩn sau khi gom nhóm chạm (tap/click/open/select coi như một), và (ii) phần tử gần điểm trỏ nhất chính là phần tử chứa toạ độ chuẩn. Cài đặt: `harness/metric_exec.py`.

**Thước phụ bắt buộc — không gây hại.** Trên các bước không phải bước chạm (cuộn, gõ, mở ứng dụng, chờ, quay lại — chiếm 41% tập kiểm), S2 không được thấp hơn S1 quá **3 điểm phần trăm** ở tỉ lệ khớp loại thao tác.

**Kiểm chéo bằng người.** 100 câu rút ngẫu nhiên có hạt giống cố định, hai người chấm độc lập theo khung `harness/cv_study/`, báo kèm hệ số đồng thuận. Kết quả người dùng để đối chiếu, **không** dùng thay thước chính.

**Đối tượng chấm.** Toàn bộ bước chạm của tập kiểm app-unseen (khoảng 2.000 bước, không lấy mẫu con).

---

## 4. Cổng trước khi tiêu tiền

**Cổng A — bộ trỏ.** Trước mọi khoản chi huấn luyện, đo sai số của bộ trỏ chuyên trên loại màn hình này. Điều kiện dùng làm thước chính: **sai số trung vị ≤ 3% chiều rộng màn**. Không đạt thì chuyển sang kế hoạch B ba bậc ở mục 8, và ghi rõ trong luận văn là đã chuyển.

**Cổng B — còn chỗ chứng minh không.** Sau khi huấn luyện S1 và chấm đủ: tính trần của thước, định nghĩa là điểm mà chính câu chuẩn do người viết đạt được khi chấm qua đúng thước này. Nếu (trần − điểm S1) < 2 × MDE thật thì dừng nhánh mô hình, chuyển trọng tâm sang chương đo lường, và ghi lý do.

**Cổng C — mức 2.** S3-pilot chỉ được mở rộng ra toàn bộ dữ liệu khi trên lát thử nó hơn S2 ít nhất bằng MDE của lát đó.

---

## 5. Trình tự cứng — không đảo

1. Commit bản đăng ký này.
2. Kiểm cổng A.
3. Huấn luyện S1 hai hạt giống. Chấm đủ.
4. Tính **MDE thật** từ phương sai quan sát được, và tính cỡ nhiễu hạt giống = |S1 hạt giống 1 − S1 hạt giống 2|.
5. **Khoá ngưỡng đậu rớt** (mục 6) bằng số vừa tính, ghi vào mục sửa đổi cuối file này kèm ngày.
6. Chạy phép thử trần trên S1: nối dòng khai báo chuẩn vào đầu vào, so với một đoạn đệm vô nghĩa cùng độ dài.
7. Huấn luyện S2 hai hạt giống. Chấm.
8. S2r, S2-nopoint, B-infer. Chấm.
9. S3-pilot.
10. Chấm tay 100 câu, kiểm không gây hại, bản trình diễn tiếng Việt.
11. Đóng băng mọi con số, viết chương kết quả.

Bước 4 và 5 **phải xong trước** bước 7. Nếu vì lý do kỹ thuật phải đảo, ghi lại lý do vào mục sửa đổi và coi kết quả là thăm dò.

---

## 6. Luật đọc kết quả — viết trước khi thấy số

Gọi Δ = điểm S2 − điểm S1, lấy trung bình trên các hạt giống, kèm khoảng tin cậy 95% bằng wild cluster bootstrap 10.000 lần, gom cụm theo ứng dụng, hạt giống cố định 20260805.

| Kết cục | Điều kiện | Kết luận được phép viết |
|---|---|---|
| **Dương** | cận dưới khoảng tin cậy của Δ > 0 **và** Δ > cỡ nhiễu hạt giống | Thành phần có tác dụng. Được nêu là kết quả chính. |
| **Dương yếu** | Δ > 0 nhưng khoảng tin cậy chạm 0 | Ghi là xu hướng chưa kết luận được. **Cấm** viết "cải thiện" ở phần tóm tắt. |
| **Trắng** | khoảng tin cậy phủ 0 và \|Δ\| < MDE thật | Kết quả âm có kiểm soát. Chương đo lường thành trọng tâm. Vẫn báo đủ mọi con số. |
| **Âm** | cận trên khoảng tin cậy < 0 | Báo trung thực là thành phần gây hại, kèm phân tích theo nguồn tên nhãn để tách "can thiệp vô dụng" khỏi "nhãn nhiễu kéo xuống". |

**Luật cho các câu hỏi phụ:**
- Nếu Δ dương nhưng (S2 − S2r) có khoảng tin cậy phủ 0 → **không được** kết luận nội dung khai báo là nguyên nhân; phải viết rằng không loại trừ được yếu tố độ dài chuỗi.
- Nếu B-infer đạt trong khoảng nhiễu hạt giống so với S2 → phải viết thẳng rằng huấn luyện không hơn việc đưa thông tin lúc suy luận trên thước này, và chuyển luận điểm sang chi phí suy luận cùng tính độc lập với cây trợ năng.
- Phép so S2 với S2r là hiệu của hiệu, chứng cứ yếu hơn phép chính, phải ghi rõ điều đó khi trình bày.

---

## 7. Phân tích phân tầng — đăng ký trước, không thêm sau

Ba lát cắt duy nhất được phép báo, định nghĩa trước khi chấm:

1. **Theo độ dài câu sinh ra**: chia đôi tại trung vị độ dài của S1.
2. **Lát khó**: các bước thuộc phần ba dưới của phân bố khoảng cách từ phần tử đích tới phần tử cùng vai trò gần nhất. Kỳ vọng: Δ ở lát khó lớn hơn Δ toàn tập. Nếu ngược lại, ghi rằng cơ chế không như giả thuyết.
3. **Theo nguồn tên trong nhãn**: nhóm tên lấy từ cây trợ năng, nhóm tên từ OCR, nhóm không có tên.

Lát cắt nào phát sinh sau khi thấy kết quả đều phải gắn nhãn thăm dò.

---

## 8. Kế hoạch dự phòng nếu cổng A rớt

Bậc 1 (sai số 3–5%): đổi thước chính sang kiểu vòng dung sai, hạ cách chấm nút-gần-nhất xuống vai phụ, báo kèm đường cong kết oan đã đo.
Bậc 2: gộp nhiều bộ trỏ, lấy đồng thuận.
Bậc 3: chuyển sang so thứ hạng tương đối giữa các nhánh trên cùng thước nhiễu, nâng chấm tay lên 200 câu thành thước đồng chính.

Thước dự phòng "chọn trong danh sách" chỉ dùng kèm hai điều kiện: luật tính đúng là mọi hộp chứa điểm chạm đều tính đúng (không dùng luật hộp nhỏ nhất, vì nhãn dạy dựng bằng chính luật đó), và mô hình đọc danh sách phải khác họ với cả mô hình được chấm lẫn mốc ngoài.

---

## 9. Những gì đã biết trước khi khoá

Ghi lại để sau này phân biệt được cái gì là dự đoán, cái gì là kết quả:

- Bệnh chính đã đo: câu cộc lốc giúp bộ trỏ tìm trúng 32%, câu tả rõ 69% (n = 76 câu chuẩn, chia đôi tại trung vị 8 từ; tương quan độ dài–trúng +0,327).
- Thước đã tự kiểm bằng bơm lỗi: đạt 8/10 tiêu chí; hai tiêu chí chưa đạt là kết oan khi bộ trỏ lệch nhiều (59,2% ở mức lệch thật của bộ trỏ rẻ) và luật đảo nghĩa ngoài bảng (0/83).
- Chất lượng nhãn khai báo trên 1.068 bước: 77% có tên rõ (số làm việc thận trọng 70–75%), 20% không tên, 76% rõ vai trò, ô toạ độ sạch 100%.
- MDE **ước chiếu** 4–7 điểm phần trăm. Đây là số tính từ giả định, **chưa phải số đo** — sẽ thay bằng số thật ở bước 4.
- Hiệu ứng kỳ vọng theo các nghiên cứu trước: 3–8 điểm, trung vị khoảng 5 (nguồn từng số: `report/105`).
- Xác suất chủ quan trước khi chạy, ghi để sau này đối chiếu: thắng cả hai mốc khoảng 0,70; thành phần vượt MDE khoảng 0,50–0,60.

---

## 10. Mã và cấu hình được niêm phong cùng bản này

`harness/metric_exec.py` (thước) · `harness/exec_injection_validate.py` (bơm lỗi, ngưỡng khoá cứng trong mã) · `harness/descriptor_label_pilot.py` (dựng nhãn — **phải nâng cấp trước khi dựng nhãn thật**, xem mục sửa đổi) · `harness/mde_recompute.py` (lực thống kê) · `harness/build_train_data.py`, `harness/prep_ocr_train.py` (dữ liệu) · `harness/train_config.yaml` (cấu hình huấn luyện).

Hạt giống dùng chung cho mọi phép lấy mẫu và bootstrap: **20260805**.

---

## Mục sửa đổi

*(Mọi thay đổi sau ngày lập đều ghi vào đây kèm ngày và lý do. Không sửa đè lên phần trên.)*

### 5/8/2026 — cân nhắc ĐẢO nguồn tên trong nhãn khai báo: **BÁC**. Áp cổng lọc thay thế.

**Vì sao đặt vấn đề.** Phát hiện bản dump cây trợ năng không có trường `text` nào, chỉ có
`content_description` — tức nhãn chức năng do lập trình viên viết, không phải chữ hiển thị.
Ô "tên" vì vậy đang trộn hai quy ước: tên chức năng (từ trợ năng) và chữ trên màn (từ OCR).
Đề xuất ban đầu là đảo thứ tự ưu tiên sang OCR trước, vì người dùng nhìn màn hình chỉ thấy
chữ hiển thị.

**Bằng chứng ban đầu, thuận chiều đảo.** Khi hai nguồn khác nhau (n=130), câu chuẩn do người
viết dùng chữ OCR 32 lần, dùng nhãn trợ năng 10 lần — gấp 3,2 lần.

**Vòng phản biện 5/8 (3 lập trường, mổ chéo, một chủ tịch tự đo lại) BÁC đề xuất**, bằng một
lập luận mà vòng đo đầu bỏ sót:

1. Bán kính thật của tranh cãi nhỏ: chỉ **72/1074 = 6,7%** nhãn đổi tên nếu đảo.
2. Trong 72 ca đó, **32 ca là chuỗi số có sẵn trong mục tiêu** (bộ chọn ngày giờ, bàn phím
   số: OCR đọc `10`, mục tiêu ghi "Set minutes to 10"). Ưu thế ở nhóm này đến từ đề bài,
   không từ chất lượng đặt tên.
3. Còn 40 ca lõi: OCR thắng 12, trợ năng thắng 3, không bên nào 25. **Nhưng 11/12 ca OCR
   thắng là vì nhãn trợ năng RÁC** (`plp_category_button`, `viewer.button.edit`,
   `No label specified`, `Search, Tab 2 of 3`, chuỗi có ký tự vô hình...). Đối đầu
   sạch-với-sạch: OCR thắng 1, trợ năng thắng 3.

⇒ **Ưu thế đo được của OCR là ưu thế của việc LỌC RÁC, không phải của thứ tự ưu tiên.**
Đảo thứ tự là đổi một luật đã niêm phong để mua nhầm thứ mà một bộ lọc lấy được rẻ hơn.

**Đã áp thay vào đó (phương án A′), quyết TRƯỚC khi huấn luyện dòng nào:**

- **Cổng hợp lệ cho nhãn trợ năng** (`clean_a11y` trong `descriptor_label_build.py`): cắt tại
  ký tự xuống dòng, bỏ ký tự vô hình, bỏ tiền tố `null,` và đuôi đọc-màn (`, Tab 2 of 3`,
  `. Button`); loại hẳn nếu là định danh mã nguồn, chuỗi số dài, nhãn rỗng nghĩa, hoặc còn
  dài quá 40 ký tự. Đo tại nút đích: **14,7% nhãn trợ năng là rác** (tự kiểm lại, phản biện
  ước 15,0%).
- **Cổng hình học cho OCR**: chỉ dùng chữ OCR khi hộp chiếm ≤25% màn. Hộp to hơn là khung
  ngoài, chữ bên trong thuộc phần tử khác — đo được 25 ca như vậy, **0/25 khớp câu chuẩn**.
- **Luật ghép OCR**: chỉ nối hai mục khi cùng dòng, tránh đẻ ra chuỗi không tồn tại trên màn
  (`= adidas Gmail`, `Showresults`).
- Thêm trường `a11y_raw` và giá trị `name_src = a11y_rejected` để sau này kiểm lại được.

**Ảnh hưởng lên phân bố nhãn** (thay số ở mục 9, dòng "chất lượng nhãn khai báo"):

| | luật cũ | sau A′ |
|---|---|---|
| tên rõ | 77,2% | **73,8%** |
| chỉ ký hiệu lẻ | 2,9% | 2,8% |
| không tên | 19,9% | **23,4%** |
| nguồn: trợ năng / OCR | 254 / 606 | 224 / 599 |

Tên ít đi 3,4 điểm, đổi lại nhãn còn lại sạch hơn — đúng nguyên tắc đã khoá ở mục 7: để trống
còn hơn đoán bừa.

**Ba giới hạn phải khai, không được lờ:**

- A′ không chạm tới 25/40 ca lõi mà người viết không dùng nguồn nào (`Create new reminder.` |
  `+` → người viết "the add icon"), cũng không chạm 23,4% bước không có tên.
- Toàn bộ nhóm quyết định này nằm trên 6,7% dữ liệu, **dưới mọi kịch bản MDE**. Cấm dùng A′
  để giải thích hậu kỳ nếu S2 thắng, và cấm hứa nó nâng điểm.
- Lát cắt "theo nguồn tên" (mục 7 ý 3) bị nhiễu: nhóm nguồn-trợ-năng thiên nặng về nút icon
  không chữ, tức là bước KHÓ hơn. Chênh lệch thấp ở nhóm đó không tách được "nhãn tệ" khỏi
  "bước khó". Lát này là mô tả, **không phải phép kiểm** — phải ghi rõ trong thân luận văn.

Nhật ký đầy đủ của vòng phản biện: `report/107_DEBATE_NGUON_TEN.md`.
