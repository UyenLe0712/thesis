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

**Thước phụ bắt buộc — không gây hại.** Trên các bước không phải bước chạm (cuộn, gõ, mở ứng dụng, chờ, quay lại — chiếm 35,9% tập kiểm, xem mục sửa đổi 6/8 h), S2 không được thấp hơn S1 quá **3 điểm phần trăm** ở tỉ lệ khớp loại thao tác.

**Kiểm chéo bằng người.** 100 câu rút ngẫu nhiên có hạt giống cố định, hai người chấm độc lập theo khung `harness/cv_study/`, báo kèm hệ số đồng thuận. Kết quả người dùng để đối chiếu, **không** dùng thay thước chính.

**Đối tượng chấm.** Toàn bộ bước chạm của tập kiểm giữ-riêng-theo-tác-vụ — 4.463 bước, không lấy
mẫu con. *(Sửa 6/8: bản gốc ghi "app-unseen" và ước 2.000 bước; xem mục sửa đổi.)*

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

---

### 6/8/2026 — sửa mô tả tập kiểm: **KHÔNG phải app-unseen**. Hạ mốc ngoài xuống tham khảo.

**Phát hiện khi rà lại trước khi tiêu tiền.** Mục 3 bản gốc ghi tập kiểm là "app-unseen". Đối
chiếu thật thì sai: tập kiểm dựng từ split `test` của kho ảnh, và **248/269 app trong đó (92%)
cũng xuất hiện ở phần dữ liệu dạy**. Chỉ 21 app là chưa từng thấy, ứng với 126 bước / **67 bước
chạm** — quá ít để làm tập chính.

Nguồn của nhầm lẫn: con số "631 tác vụ app-unseen" trong hồ sơ cũ (`report/103`) lấy từ vòng làm
việc tháng 7, khi định dùng split app-unseen chính thức của Google. Split đó nằm trong TFRecord
gzip trên GCS, cần TensorFlow — đúng thứ dự án đã chọn tránh khi chuyển sang bản HuggingFace.
Bản HF chỉ có split `test` chung, không kèm nhãn phân loại app-unseen / task-unseen.

**Đã kiểm, phần KHÔNG hỏng:** không có tác vụ nào trùng giữa dạy và kiểm (**0/1432**). Đây vẫn là
tập giữ-riêng hợp lệ, chỉ là giữ riêng theo **tác vụ** chứ không theo **ứng dụng**.

**Sửa như sau:**

1. **Mục 3 đọc lại thành:** "toàn bộ bước chạm của tập kiểm giữ-riêng-theo-tác-vụ (0 tác vụ trùng
   với tập dạy; phần lớn ứng dụng có xuất hiện trong tập dạy)". Bỏ chữ *app-unseen*.
2. **Phép so chính (S1 vs S2) không đổi và vẫn hợp lệ**: hai nhánh dùng chung dữ liệu dạy, chung
   mô hình gốc, chung tập kiểm. Điều kiện đối xứng nên chênh lệch vẫn quy được về can thiệp. Đây
   là lý do việc này không làm hỏng kết quả chính.
3. **Mốc ngoài (so với gpt-4o-mini) HẠ xuống tham khảo, kèm khai bắt buộc**: mô hình của luận văn
   được học các ứng dụng đó, gpt-4o-mini thì không — lợi thế sân nhà. Cấm viết "vượt gpt-4o-mini"
   như một kết luận độc lập; phải kèm câu về nhiễm ứng dụng ngay tại chỗ trình số.
4. **Thêm một lát cắt phụ, đăng ký từ bây giờ**: nhóm ứng dụng chưa thấy lúc dạy (67 bước chạm).
   Khai trước là **thiếu lực nghiêm trọng** — chỉ đọc theo hướng, không kết luận, không dùng để
   cứu nếu kết quả chính không như ý. Nhãn `app_seen_in_train` (True/False/None) đã ghi sẵn vào
   từng bản ghi `test.jsonl` để lát này tính được mà không cần quyết định gì thêm về sau.

**Phân bố tập kiểm sau khi gắn nhãn:**

| nhóm | bước | bước chạm |
|---|---|---|
| ứng dụng đã thấy lúc dạy | 3.004 | 1.748 |
| ứng dụng chưa thấy | 126 | 67 |
| không gán được ứng dụng | 3.828 | 2.648 |

### 6/8/2026 — hai sửa nhỏ cùng lượt rà

- **Loại 11 bản ghi không có câu chuẩn** khỏi tập kiểm (đều là bước 0 của một số tác vụ, phần lớn
  là `wait`). Nếu để lại sẽ tính vào mẫu số và thành trừ điểm oan. Tập kiểm còn **6.958 bước /
  4.463 bước chạm / 1.432 tác vụ**.
- **Khai một giới hạn của nhánh mức 2**: khai báo giả dựng từ nút hàng xóm cùng vai trò, nhưng
  **162/1074 ca (15,1%) hàng xóm trùng tên với nút đích**. Ở các ca đó khai báo thật và giả chỉ
  khác toạ độ, nên khoản phạt lề ép mô hình làm câu phụ thuộc toạ độ chứ không phụ thuộc dấu hiệu
  phân biệt — tức cơ chế không đánh trúng đúng nhóm ca mơ hồ mà nó nhắm tới. Mức 2 vẫn chạy như
  đăng ký (bản thử nhỏ), nhưng khi đọc kết quả phải tách riêng nhóm 15,1% này, và nếu mức 2 không
  có tín hiệu thì đây là một cách giải thích phải nêu trước khi kết luận "cơ chế vô dụng".

**Ghi chú về thời điểm:** cả ba sửa trên quyết định **trước khi huấn luyện dòng nào** và trước mọi
khoản chi. Không có con số kết quả nào tồn tại ở thời điểm này.

---

### 6/8/2026 (b) — CHỐT LUẬT CHẤM bằng số. Bậc dự phòng cũ đã chết, thay bằng bậc khác.

**Vì sao phải chốt lại.** Vòng rà 11 giám khảo phát hiện: bộ tự kiểm bơm lỗi
(`exec_injection_validate.py:140`) gọi `hit_nearest_box` — chấm trên **hộp** — trong khi đường
chấm thật (`score_run.py` → `metric_exec.score_step:195`) gọi `hit_voronoi` — chấm trên **tâm**.
Tức con số "**8/10**" đang nói về một hàm **khác** với hàm sẽ chấm luận văn. `hit_nearest_box`
không xuất hiện ở bất kỳ đâu trong đường chấm thật.

**Đã tự đo lại trần và sàn của cả ba ứng viên** trên 250 bước chạm rút ngẫu nhiên từ tập kiểm
(hạt giống 20260805, nhiễu bơm theo góc ngẫu nhiên, 4 lần mỗi bước; cây trợ năng phủ 250/250,
trung vị 71 phần tử mỗi màn):

| sai số bộ trỏ | đĩa dung sai 14% | **ô-Voronoi tâm** | hộp-gần-nhất |
|---|---|---|---|
| 0% | 100,0% | 100,0% | 100,0% |
| 3% | 100,0% | **99,7%** | 78,6% |
| 5% | 100,0% | **93,3%** | 44,6% |
| 8% | 100,0% | **74,4%** | 20,3% |
| **SÀN** (trỏ vào tâm phần tử **khác** gần nhất) | **84,3%** | **2,8%** | 4,8% |

**Chốt: headline là `hit_voronoi` trên tâm phần tử của cây trợ năng.** Lý do là **SÀN**, không
phải trần: dải động 99,7 − 2,8 ≈ **97 điểm** ở ngưỡng cổng A, rộng nhất trong ba ứng viên. Đây
cũng chính là hàm đang nối dây trong `score_run.py`, nên **không đổi mã chấm** — chỉ chốt bằng
văn bản và sửa cái nhãn in sai (`score_run.py` đang in "nút-gần-nhất" cho con số Voronoi; nếu
không sửa thì tên sai đi thẳng vào luận văn).

**Hai thứ bị bác bằng chính bảng trên:**

- **Đĩa dung sai không được làm headline.** Sàn **84,3%** nghĩa là trỏ nhầm sang nút bên cạnh
  vẫn được cho qua 84% số ca. Dải động chỉ ~16 điểm. Vẫn báo kèm để minh bạch, nhưng chỉ là
  cột phụ.
- **`hit_nearest_box` không dùng.** Trần chỉ 78,6% ngay tại ngưỡng cổng A, tức kết oan 21% câu
  đúng kể cả khi bộ trỏ tốt.

**Bậc dự phòng ở mục 8 — VIẾT LẠI.** Bậc cũ ("rớt cổng A 3–5% → đổi thước chính sang đĩa dung
sai") là một cái bẫy: nó chuyển sang đúng cái thước gần như không phân biệt được gì. Bậc mới,
dựa trên bảng trên và một phép đo bổ sung cho top-k:

| Sai số bộ trỏ đo được | Làm gì |
|---|---|
| ≤ 5% | Giữ nguyên Voronoi làm headline. Trần 93,3–99,7%, sàn 2,8% — đọc bình thường. |
| 5–8% | Vẫn giữ Voronoi (trần 74,4%, sàn 2,8%, dải 71,6 điểm — vẫn tốt hơn mọi ứng viên khác). **Bắt buộc** in kèm bảng trần này và diễn giải mọi con số như cận dưới. |
| > 8% | **Không đổi sang thước yếu hơn.** Đo được: top-2 ở mức này có trần 96,3% nhưng sàn **61,4%** (dải 35 điểm), đĩa dung sai còn tệ hơn. Thay vào đó: nâng **chấm tay lên 200 câu thành thước đồng-chính**, và chỉ báo **thứ hạng tương đối** giữa các nhánh trên cùng thước nhiễu, không báo con số tuyệt đối. |

Hạt giống, cỡ mẫu và mã của phép đo trên: 250 bước, `random.Random(20260805)`, gọi thẳng
`metric_exec.hit_disk / hit_voronoi / hit_nearest_box`. Con số này quyết **trước** khi có bất kỳ
kết quả huấn luyện nào.

**Hệ quả bắt buộc — đọc mục sửa đổi 6/8 (c) ngay dưới:** vì thước chốt lại, con số 8/10 của phần
tự kiểm không còn mô tả thước đang dùng, phải chạy lại.

---

### 6/8/2026 (c) — chạy lại BƠM LỖI bằng đúng dụng cụ. Vẫn 8/10, nhưng **hai tiêu chí rớt đã đổi**.

`harness/exec_injection_v3.py` — giữ nguyên mười tiêu chí và mười ngưỡng đã khoá của bản 2, chỉ
đổi dụng cụ: ca kiểm lấy từ **tập kiểm thật** (398 bước chạm, trung vị 65 phần tử mỗi màn), danh
sách nút qua đúng hàm `score_run.buttons_of`, chấm bằng đúng `metric_exec.score_step`.

| Tiêu chí | Bản 2 (dụng cụ sai) | **Bản 3 (dụng cụ thật)** | n |
|---|---|---|---|
| fp_paraphrase_thuc_te ≤10% | **59,2% ✘** | **0,0% ✔** | 398 |
| fp_action_gate ≤15% | ✔ | 0,0% ✔ | 398 |
| fp_flip_rule ≤5% | ✔ | 0,0% ✔ | 398 |
| det_nut_canh_gan ≥80% | ✔ | **33,1% ✘** | 121 |
| det_nut_canh_xa ≥90% | ✔ | 99,6% ✔ | 233 |
| det_nut_rat_xa ≥95% | ✔ | 100,0% ✔ | 397 |
| det_flip_heldout ≥50% | **0% ✘** | **20,0% ✘** | 15 |
| det_wrong_action ≥80% | ✔ | 100,0% ✔ | 369 |
| det_wrong_content ≥90% | ✔ | 91,1% ✔ | 494 |
| det_wrong_direction ≥90% | ✔ | 100,0% ✔ | 755 |
| | 8/10 | **8/10** | |

**Cùng điểm số nhưng khác bản chất — phải trình đúng chỗ này:**

- **Điểm yếu cũ biến mất.** Kết oan câu đúng từ 59,2% xuống **0,0%**. Đường cong kết oan cũng
  tốt hơn hẳn: lệch 3% → **0,0%** (bản cũ 2,6%) · 5% → 7,5% · 8% → 24,1% (bản cũ 42%) ·
  13% → 55,0%. Nghĩa là cổng A ở mức 3% có biên rộng hơn ta tưởng.
- **Điểm yếu mới lộ ra:** thước **không phân biệt được điểm trỏ lệch dưới ~63 px** (bắt được chỉ
  33,1%). Nguyên nhân là luật gộp phần tử của chính thước: hai tâm cách nhau dưới 24dp ≈ 63 px
  bị coi là một. Đây là **hành vi cố ý**, không phải lỗi — nút đích trung bình 189×126 px nên
  lệch dưới 63 px thường vẫn nằm trong cùng một nút. Nhưng phải khai thẳng: thước này đo được
  "trỏ nhầm sang nút khác", **không** đo được "trỏ hơi lệch trong cùng một nút".
- **Luật từ ngược nghĩa vẫn rớt** (20%, và chỉ n=15 — cỡ mẫu quá nhỏ để nói gì chắc). Giữ nguyên
  cách khai của bản 2: đây là lưới thưa cho một chỗ mù nhỏ.

**Đã cân nhắc và loại một phương án:** sửa `hit_nearest_box` bằng cách bỏ hộp lồng nhau (đúng lỗi
đã gặp ở khâu dựng nhãn). Có cải thiện nhưng không đủ — ở mức lệch 3%, trần 84,2% so với 100% của
Voronoi, và sàn tệ hơn (9,2% so với 2,8%). Quyết định giữ Voronoi đứng vững.

**Khai bắt buộc khi trình:** phải in cột **n** cạnh mỗi tiêu chí. Có tiêu chí đo trên n=755, có
tiêu chí chỉ n=15 — trình "8/10" trần trụi là che mất chuyện đó.

---

## Sửa đổi 6/8 (d) — chạy thử đường ống, và một con số nền bị rút

**Việc đã làm.** Chạy `score_run.py --mode gate --grounder openai --n 10` trên tập kiểm
(chi phí dưới 0,01 đô). Mục đích không phải lấy kết quả mà là để lần đầu tiên cho cả đường
ống chạm vào một bộ trỏ thật. Đường ống **chạy thông**: gọi API, đọc được toạ độ, quy về
pixel ảnh gốc, ghi `gate10_raw.jsonl` đủ trường.

**Kết quả.** Sai số trung vị **29,3% bề ngang màn**, phân vị 75 là 50,1%, **không bước nào
vào nổi 3%**. Bốn trong mười lần bộ trỏ trả đúng giữa màn (`500,400` trong thang 0-1000) —
đoán bừa, không phải trỏ. Điều này không bất ngờ và không đổi kế hoạch: gpt-4o-mini vốn chỉ
để chạy thử, bộ trỏ dùng cho thước chính là UGround.

**Nhưng nó lật một con số nền của hồ sơ.** Trước đó nhiều chỗ ghi "bộ trỏ rẻ lệch trung vị
8% cạnh". Truy ra: số đó tính bằng `real_offsets()` (`exec_injection_validate.py:144`), hàm
**chỉ lấy sai số của những ca bộ trỏ đã trúng dung sai** rồi mới tính trung vị — nghĩa là đã
loại sạch mọi lần trượt trước khi đo. Trung vị không lọc:

| Nguồn | Công thức | Trung vị | n |
|---|---|---|---|
| `ground_pilot_results.json` | `hypot((px−gx)/W, (py−gy)/H)` | **15,0%** | 76 |
| cổng A, đo 6/8 | `dist(p,g)/W` | **29,3%** | 10 |
| `report/98` dòng 388 (cây trợ năng) | pixel | **256 px** = 23,7% | 76 |
| ~~`real_offsets`, đã rút~~ | pixel, *có lọc* | ~~87 px = 8%~~ | — |

Hai chuyện phải tách bạch. **Thứ nhất, lỗi chọn mẫu**: 87 px là trung vị *có điều kiện đã
trúng*. **Thứ hai, hai công thức khác nhau cùng gọi là "phần trăm"**: `ground_pilot` chia
lệch dọc cho chiều CAO (2400) nên nhẹ đi 2,2 lần so với chia bề NGANG; trên cùng 10 bước,
công thức cổng A ra số lớn hơn 1,63 lần. Ngưỡng 3% của cổng A neo theo công thức cổng A,
vì nó suy ra từ "phần tử khác gần nhất cách 69 px".

**Hệ quả với cách đọc cổng A.** Khoảng cách từ bộ trỏ rẻ tới ngưỡng bị hồ sơ cũ thu nhỏ
khoảng 3,5 lần. Ngưỡng 3% **không đổi** — nó có căn cứ hình học độc lập. Nhưng phải hạ kỳ
vọng: nếu bộ trỏ chuyên cũng không đạt, đó là kết cục đã lường trước, xử theo bậc thang ở
mục 8, **không** được nới ngưỡng sau khi nhìn số.

---

## Sửa đổi 6/8 (e) — luật gộp cụm chưa xác định, và ô "dấu hiệu phân biệt" gần như rỗng nghĩa

Hai chỗ này tìm ra khi rà lại phần free trước lúc tiêu tiền. Cả hai **phải chốt bây giờ**, vì
sau khi có điểm số thì mọi lựa chọn đều thành lựa-cái-có-lợi.

### (e1) Bản đăng ký nói một đằng, con số MDE lấy một nẻo

Mục 4 viết "gom cụm theo ứng dụng". Nhưng **59,3% bước chạm của tập kiểm không gán được app**
(1.815/4.463 gán được, 259 app riêng biệt). Bản đăng ký **không nói xử nhóm còn lại thế nào**,
mà đúng chỗ đó lại quyết định lực thống kê:

| Luật gộp cụm | G | G hiệu dụng (Kish) | MDE khi hai nhánh khác nhau 20% |
|---|---|---|---|
| Cụm-đơn: mỗi tác vụ không-rõ-app là một cụm | 1.091 | **454** | **5,9 pp** |
| Chỉ dùng 40,7% bước gán được app | 259 | **107** | **12,1 pp** |
| Bảo thủ: gom hết bước không-rõ-app vào một cụm | 260 | 3 | không dùng được |

Con số "MDE ước chiếu 4–7 pp" ở mục 6 chỉ đúng dưới luật **cụm-đơn**. Còn "G hiệu dụng ~98"
từng ghi ở `report/103` lại là con số của luật **app-only** — mà luật đó cho MDE 8,6–14,8 pp.
Hai con số bị đặt cạnh nhau như thể cùng một phép tính. **Chúng không phải.**

**Chốt:** phân tích chính dùng luật **cụm-đơn** (đúng ý định đã ghi từ trước), và **bắt buộc**
in kèm phân tích nhạy cảm theo luật app-only. Cam kết trước, không được rút lại:

> Nếu Δ quan sát được nằm giữa hai MDE (tức khoảng **4–9 pp**), kết luận **phụ thuộc luật gộp
> cụm**. Trường hợp đó phải báo là **chưa kết luận được**, không được chọn luật nào có lợi hơn.
> Chỉ khi Δ vượt MDE của **cả hai** luật mới được gọi là dương.

### (e2) Ô "dấu hiệu phân biệt" hầu như không phân biệt gì

Đếm trên đủ 1.074 nhãn:

| Nội dung ô | Số | Tỉ lệ |
|---|---|---|
| Chỉ đếm số phần tử cùng loại — *"1 trong 8 phần tử cùng loại"*, *"màn có nhiều phần tử cùng loại"* | 921 | **85,8%** |
| Báo là có mơ hồ nhưng không nói cách gỡ — *"trùng tên với 1 phần tử khác trên màn"* | 75 | 7,0% |
| Thật sự gỡ được mơ hồ — *"ô nhập liệu duy nhất trên màn"* | 78 | **7,3%** |

Nghĩa là **92,7% số nhãn có ô này rỗng nghĩa về mặt phân biệt**. Đây là ô mang tên của chính
thành phần đóng góp ("mô tả **phân biệt** trước, phát ngôn sau"), nên phải khai thẳng.

**Chốt cách đọc, cam kết trước:**

> Nếu S2 thắng S1, **cấm** quy công cho "tính phân biệt của mô tả". Ô đó không mang đủ thông tin
> để gánh lời giải thích ấy. Việc quy công phải dựa vào hai nhánh đối chứng đã đăng ký:
> **S2-nopoint** tách phần đóng góp của ô toạ độ, **S2r** tách phần đóng góp của việc chuỗi dài
> thêm. Phần dư sau khi trừ hai thứ đó mới được bàn tới nội dung khai báo.
> Đồng thời phải in bảng phân tầng kết quả theo ba nhóm ô trên (85,8% / 7,0% / 7,3%).

---

## Sửa đổi 6/8 (f) — nâng ô "dấu hiệu phân biệt", và siết ghép độ dài của nhánh đối chứng

Sửa đổi này ra đời **trước khi có bất kỳ điểm số nào**, và đó là điều kiện để nó hợp lệ. Sau
lượt huấn luyện đầu tiên thì không được đụng vào đặc tả nhãn nữa.

### (f1) Ô thứ tư nay nói được cách gỡ mơ hồ

Sửa đổi (e2) đo ra ô này rỗng nghĩa 92,7%. Nguyên nhân nằm ở **thứ tự ưu tiên trong luật sinh**:
vế "đếm số phần tử cùng loại" đứng trước nên nuốt gần hết, dù nó không gỡ được gì. Đã xếp lại
theo tiêu chí *vế nào gỡ được mơ hồ*:

1. phần tử duy nhất thuộc vai trò đó — gỡ hẳn
2. **mỏ neo chữ** — chuỗi chữ gần nhất bên cạnh, kèm hướng: *"ngay dưới chữ «Create folder»"*
3. đếm số phần tử cùng loại — chỉ dùng khi hết đường

Ca trùng tên là ca mơ hồ nặng nhất nên nay được **ghép thêm mỏ neo** thay vì chỉ nói triệu chứng.

Vì sao chọn mỏ neo chữ chứ không chọn mô tả vị trí kiểu *"nửa dưới, bên phải"*: ô `<point>` đã
ghi vị trí, và ghi chính xác hơn hẳn một cách nói ước lượng. Mô tả vị trí bằng lời **không thêm
thông tin nào** ngoài thứ toạ độ đã có. Mỏ neo thì khác — nó là **quan hệ với xung quanh**, không
suy ra được từ toạ độ, và đúng là thứ tách được hai nút trông y hệt nhau.

Ba điều kiện lọc, đều đã kiểm bằng số trên đủ 1.074 nhãn: chuỗi phải nằm **ngoài** hộp phần tử
(nằm trong hộp thì nó chính là nhãn của phần tử, lặp lại ô TÊN); không được trùng tên phần tử;
phải có ít nhất hai ký tự chữ-số (không có luật này thì lọt rác OCR một ký tự kiểu `α`, `S`).
Hướng của mỏ neo kiểm riêng: **737/737 ca đúng chiều, 0 sai**.

| Nội dung ô | Bản cũ | **Bản mới** |
|---|---|---|
| Mỏ neo chữ | — | **686 = 63,9%** |
| Trùng tên, có kèm mỏ neo | — | 51 = 4,7% |
| Phần tử duy nhất trên màn | 78 = 7,3% | 78 = 7,3% |
| Trùng tên, không mỏ neo | 75 = 7,0% | 24 = 2,2% |
| Chỉ đếm số phần tử cùng loại | 921 = 85,8% | 235 = 21,9% |
| **Gỡ được mơ hồ** | **7,3%** | **75,9%** |

**Cách đọc kết quả vẫn giữ nguyên như (e2)** — không nới. Ô này khá hơn nhiều nhưng vẫn còn
24,1% không gỡ được, và việc quy công cho "tính phân biệt" vẫn phải đi qua hai nhánh đối chứng
S2-nopoint và S2r, kèm bảng phân tầng theo ba nhóm trên. Sửa nhãn không phải là bằng chứng.

### (f2) Nhánh S2r nay ghép độ dài theo token

Mục 2 đăng ký S2r là "độ dài **token** ghép bằng bản thật theo từng mẫu". Kiểm lại thì mã ghép
theo **ký tự**. Trung vị lệch 0 ký tự nghe rất khít, nhưng đo theo token thì chỉ **54,0%** số cặp
nằm trong 2 token, biên độ tới −17/+14. Trung bình vẫn ~0 nên đối chứng không lệch hệ thống, song
mã không làm đúng thứ đã đăng ký. Đã đổi sang ghép theo token của chính `Qwen2.5-VL-3B-Instruct`:

| | trước | sau |
|---|---|---|
| Cặp lệch ≤ 2 token | 54,0% | **99,3%** |
| Biên độ | −17 / +14 | **−3 / +6** |
| Tổng token đích (S2 vs S2r) | — | 54.021 vs 53.891 |

Bảy bất biến của bốn nhánh kiểm lại sau khi dựng: câu đem chấm trùng S1 ở cả ba nhánh, S1 không
chứa khai báo, 1.074 nhãn ở cả ba, S2-nopoint sạch ô toạ độ, S2 bỏ toạ độ đúng bằng S2-nopoint,
S2 khác S2r đúng 1.074 chỗ, khai báo giả mức 2 không trùng toạ độ đích — **đạt cả bảy**.

---

## Sửa đổi 6/8 (g) — nhãn `app_seen_in_train` không tái lập được, và không tự sửa theo tập dạy

Mục sửa đổi 6/8 đầu tiên viết *"Nhãn `app_seen_in_train` đã ghi sẵn trong test.jsonl"* và dùng nó
làm lát phụ. Rà lại thì **không có dòng mã nào trong repo sinh ra nhãn đó** — nó do một lượt vá
tay để lại. Hai vấn đề:

- **Không kiểm được.** Không tái lập thì không biết nó tính đúng hay sai.
- **Không tự sửa theo tập dạy.** Đối chiếu với lát dạy đang có (2 shard, 129 ứng dụng):
  **2.136/3.130 bản ghi có nhãn mâu thuẫn**. Nhãn cũ cho 96% "đã thấy", nhiều khả năng tính theo
  toàn bộ 15.283 tác vụ của AndroidControl — đúng **nếu** cuối cùng train đủ 76 shard, sai nếu ít
  hơn. Mà số shard tới lúc chạy mới biết.

**Chốt:** nhãn này là **hàm của tập dạy thật sự dùng**, nên phải tính sau khi dựng xong dữ liệu
dạy, không phải lúc dựng tập kiểm. Đã viết `harness/tag_app_seen.py` và nối vào `run_on_rented.sh`
ngay sau khâu dựng dữ liệu. Luật gán ứng dụng bê nguyên `build_test_data.app_of` — chỉ lấy từ thao
tác `open_app`, không đoán từ chữ trong mục tiêu.

**Ba giá trị, bắt buộc phân biệt khi đọc:** `True` đã thấy · `False` gán được app và chưa thấy ·
`None` **không gán được app, tức KHÔNG BIẾT**. Nhóm `None` chiếm **3.828/6.958 = 55,0%** và
**cấm đọc thành "chưa thấy"**.

**Hệ quả với con số đã công bố.** Câu *"92% ứng dụng trong tập kiểm cũng có ở tập dạy"* ở mục sửa
đổi 6/8 đầu tiên lấy từ nhãn cũ, tức nói về **toàn bộ tập dạy AndroidControl**, không phải về tập
dạy sẽ dùng. Con số đúng chỉ chốt được sau khi dựng xong dữ liệu dạy trên máy thuê. Kết luận
"tập kiểm KHÔNG phải app-unseen" **không đổi** — nó dựa trên tập dạy đầy đủ, và mọi phương án
train đều lấy từ chính tập đó. Chỉ có tỉ lệ chính xác là còn treo.

---

## Sửa đổi 6/8 (h) — thước phụ bắt buộc chưa có mã chạy

Mục 3 đăng ký "thước phụ **bắt buộc** — không gây hại" trên bước không phải bước chạm. Rà lại thì
`score_run.py --mode score` **lọc sẵn chỉ còn bước chạm**, và không có chỗ nào khác chạy phép kiểm
này. Nghĩa là tới lúc cần trình, thước bắt buộc sẽ không có số. Đây đúng loại lỗi đã bắt một lần
ngày 5/8 (thiếu hẳn script suy luận và script chấm) — thước nằm trong hồ sơ nhưng không nằm trong mã.

**Đã bổ sung `score_run.py --mode noharm`.** Chấm bằng đúng hàm của thước chính:
`canon_action(câu mô hình) == canon_action(câu chuẩn)` — hai câu, không phải câu với mã thao tác,
để không đẻ ra một định nghĩa "khớp thao tác" thứ hai lệch với định nghĩa đang dùng. Có
`--baseline` để tính hiệu số theo cặp kèm khoảng tin cậy bootstrap gom cụm, và tự đọc luật 3 điểm
phần trăm đã khoá.

Kiểm bốn chiều bằng dự đoán dựng sẵn, trước khi có mô hình:

| Phép thử | Kỳ vọng | Đo được |
|---|---|---|
| Dự đoán = câu chuẩn | ~100% | **100,0%** |
| Mọi động từ đổi thành "Tap" | thấp | 53,3% (cuộn tụt còn **1,3%**) |
| Bản hỏng so với bản chuẩn | RỚT | Δ = −46,7%, KTC95 [−49,5%, −43,8%] → **RỚT** |
| Bản chuẩn so với chính nó | ĐẠT | Δ = +0,0% → **ĐẠT** |

Con số 53,3% ở phép thử thứ hai **không phải lỗi**: bước `open_app` vẫn khớp vì luật gom nhóm chạm
đã khoá coi *open* và *tap* là một. Chỗ đáng nhìn là cuộn tụt xuống 1,3% — đúng phần thước phải bắt.

**Sửa số:** mục 3 ghi bước không-chạm "chiếm 41% tập kiểm". Đếm lại trên tập kiểm đã chốt:
**2.495/6.958 = 35,9%** (cuộn 755 · chờ 505 · gõ chữ 494 · mở ứng dụng 469 · quay lại 270). Con số
41% thuộc bản đếm cũ trước khi loại 11 bản ghi không có câu chuẩn và trước khi chốt tập kiểm.

---

## Sửa đổi 6/8 (i) — ghi trước con số kỳ vọng của cổng A, và ngưỡng "số này có mùi lỗi"

Mục này ghi **trước khi chạy**, và đó là toàn bộ giá trị của nó. Lý do có mục này: vòng rà 6/8
cho thấy loại lỗi nguy hiểm nhất còn lại không phải lỗi làm chương trình chết, mà là **số ra sai
nhưng trông hợp lý** — vì lúc đó không ai đi kiểm nữa. Chính cơ chế này đã cứu một lần: hồ sơ ghi
sai số bộ trỏ 8%, đo ra 29,3%, đi truy vì lệch quá, và moi ra 8% là con số đã lọc bỏ phần hỏng.
Nếu hồ sơ ghi 30% thì đã gật đầu cho qua.

### Hai điều đo được trước, làm nền cho mọi dự đoán

**Sàn không thể vượt ≈ 0.** Toạ độ chạm của AndroidControl **không phải vị trí ngón tay thô**:
79,4% điểm chạm nằm trong 1,5 px của tâm một phần tử trợ năng, trung vị **0,7 px**, 9,7% trùng
khít. Nó là tâm phần tử. Vậy một bộ trỏ hoàn hảo đạt sai số ~0 — ngưỡng 3% khả thi về nguyên tắc,
không bị chặn bởi bản chất dữ liệu.

**Biên sai số mà thước cho phép** (nửa khoảng cách từ đích sang phần tử khác gần nhất, tính sau
khi gộp phần tử cách nhau dưới 24dp), đo trên 1.496 bước chạm:

| | px | % bề ngang |
|---|---|---|
| Phân vị 10 | 39 | 3,6% |
| Phân vị 25 | 52 | 4,8% |
| **Trung vị** | **67** | **6,2%** |
| Phân vị 75 | 92 | 8,6% |

Suy ra tỉ lệ qua được nếu bộ trỏ lệch đều một mức: **2% → 100,0% · 3% → 98,6% · 5% → 72,3% ·
8% → 28,3%**. Ngưỡng 3% đã khoá nằm **dưới cả phân vị 10** của biên, nên nó là ngưỡng chặt có căn
cứ hình học chứ không phải con số chọn bừa.

### Dự đoán ghi trước cho UGround

Sai số của một bộ trỏ chuyên gần như bị quyết định bởi **nó có chọn đúng phần tử hay không**, chứ
không phải trỏ lệch bao nhiêu trong phần tử: chọn đúng thì tâm phần tử ≈ điểm chuẩn nên sai số
gần 0; chọn nhầm thì rơi thẳng sang phần tử khác, cách 100–300 px tức 10–28%. Phân phối vì vậy
sẽ **hai cụm**, và trung vị chỉ nói lên tỉ lệ chọn đúng có quá nửa hay không.

| Sai số trung vị đo được | Đọc thế nào |
|---|---|
| **< 0,5%** | **NGHI LỖI** — quá đẹp. Phải kiểm bộ trỏ có vô tình nhận được toạ độ chuẩn không, và ảnh đưa vào có đúng ảnh của bước đó không |
| **0,5% – 5%** | **Đúng kỳ vọng.** Đạt cổng hoặc sát cổng, chạy tiếp theo kế hoạch |
| **5% – 15%** | Kém hơn mong đợi nhưng **hợp lý** — bộ trỏ thật sự vật lộn với màn dày phần tử. Xử theo bậc thang mục 8 |
| **> 15%** | **NGHI LỖI, không được đọc thành "bộ trỏ kém".** Đây là vùng của gpt-4o-mini (29,3%), mà UGround là mô hình chuyên. Phải loại trừ lỗi trước: sai câu nhắc · nhầm thang toạ độ (0-1000 với pixel thô) · ảnh bị co mà không quy đổi lại · đọc nhầm định dạng đầu ra |

**Bốn dấu hiệu lỗi phải kiểm trong `gate_A_raw.jsonl` TRƯỚC khi kết luận rớt cổng:**

Bốn dấu hiệu này **đã cài thẳng vào `score_run.py --mode gate`** và in ngay dưới con số chính —
để cam kết ở đây không thành lời suông. Ngưỡng kêu ghi trong ngoặc:

1. **Không đọc được toạ độ** (>5%) — đầu ra sai định dạng so với cách đọc.
2. **Toạ độ dồn về một chỗ** (>10% rơi vào cùng một điểm) — mô hình bỏ cuộc, trả mặc định.
3. **Toạ độ bội của 50 trong thang chuẩn hoá 0-1000** (>25%) — trỏ theo lưới thô, không thật sự
   định vị. Phải xét trên thang chuẩn hoá: bộ trỏ trả `500,400` rồi mới quy về pixel thành
   `(540, 960)` — chẳng chia hết cho 50 nào, nên kiểm trên pixel là kiểm nhầm thang và bộ dò sẽ
   im lặng đúng lúc cần kêu.
4. **x đúng giữa màn** (>20%) — kiểu bỏ cuộc theo trục ngang: trả x = 500 rồi đoán y.

**Đã kiểm bộ dò có hoạt động không**, bằng cách chạy lại chính 10 bước của gpt-4o-mini — một bộ
trỏ đã biết là hỏng. Ba trong bốn dấu hiệu kêu đúng: dồn một chỗ **30,0%** · bội của 50
**100,0%** · x đúng giữa **50,0%**. Dấu hiệu còn lại (không đọc được toạ độ) im, đúng, vì đầu ra
của nó đọc được hết. Một bộ dò không bao giờ kêu thì vô dụng ngang không có.

**Cam kết:** rớt cổng chỉ được ghi vào hồ sơ là "bộ trỏ không đạt" **sau khi** bốn dấu hiệu trên
đã loại trừ. Rớt vì lỗi cài đặt thì sửa rồi chạy lại, và **không** tính là một lần thử.

---

## Sửa đổi 7/8 — ba thứ đã đăng ký nhưng chưa có mã, và một định nghĩa mơ hồ đủ để đẻ ra kết luận sai

Quét đối chiếu từng thứ đăng ký ở bản này với mã trong `harness/`. Mười hai hạng mục, **chín có
mã, ba không**. Ghi lại vì đây đã là lần thứ ba cùng một loại lỗi: thứ nằm trong hồ sơ mà không
nằm trong mã (trước đó: script suy luận và script chấm ngày 5/8, thước phụ không-gây-hại ngày 6/8).

### (a) `--selftest-batch` — cờ được hướng dẫn dùng nhưng không tồn tại

Phép tự kiểm thứ ba (lô 1 và lô n có ra cùng câu không — phép bắt lỗi đệm sai bên) in ra dòng
*"chạy trên máy thuê bằng `--selftest-batch`"*. **Cờ đó không có trong `argparse`.** Ai làm theo
hướng dẫn cũng nhận `unrecognized arguments` rồi bỏ qua, và tưởng đã kiểm. Mà đệm sai bên là lỗi
không báo gì cả, chỉ làm điểm tụt không đều theo thứ tự bản ghi.

Đã cài `selftest_batch()` và cờ tương ứng, đồng thời nối vào `run_on_rented.sh` ở bước `infer`:
chạy một lần trước lượt sinh đầu tiên, rớt thì dừng hẳn, đạt thì đánh dấu để khỏi chạy lại.

### (b) Thước phụ không-gây-hại chưa được gọi trong kịch bản máy thuê

Chế độ `--mode noharm` đã có từ 6/8 nhưng `run_on_rented.sh` không gọi. Đã thêm lệnh
`noharm <nhánh> <hạt giống> <nhánh nền> <hạt giống nền>`.

### (c) ⚠️ B-infer — hai cách hiểu, và luật đọc kết quả chỉ đúng với một cách

Bảng ở mục 2 ghi B-infer là *"lúc suy luận nối dòng mô tả phần tử vào đầu vào"*; `report/103`
ghi *"nhét dòng mô tả nút (dựng từ cây trợ năng + OCR)"*. Hai câu đó đọc được thành hai thí
nghiệm khác hẳn nhau:

- **Cách 1 — nhét khai báo của ĐÚNG nút đích.** Đây là điều kiện *có lời giải sẵn*: đầu vào đã
  chỉ thẳng phần tử cần nói tới. Nó gần như chắc chắn thắng S2, và thắng chẳng chứng minh gì.
- **Cách 2 — nhét DANH SÁCH phần tử trên màn**, không đánh dấu cái nào là đích. Đây mới là phép
  so công bằng với S2.

**Cách 1 trùng với thí nghiệm đã có.** Mục 5 bước 6 đã đăng ký riêng *"phép thử **trần** trên S1:
nối dòng khai báo chuẩn vào đầu vào, so với một đoạn đệm vô nghĩa cùng độ dài"* — đúng là cách 1,
và đã được gọi đúng tên là **trần**. Nếu B-infer cũng là cách 1 thì hai bước là một thí nghiệm.

**Quyết định thì nằm ở luật đọc kết quả.** Mục 6 viết: *"Nếu B-infer đạt trong khoảng nhiễu hạt
giống so với S2 → phải viết thẳng rằng huấn luyện không hơn việc đưa thông tin lúc suy luận."*
Luật này **chỉ đúng dưới cách 2**. Dưới cách 1 nó sẽ bắt ta kết luận "huấn luyện mất lý do tồn
tại" từ việc một điều kiện có-lời-giải-sẵn thắng một điều kiện không có — một kết luận sai.

⇒ **Chốt: B-infer là cách 2.** Danh sách phần tử hiển thị của màn (vai trò, tên nếu có, toạ độ
`<point>`), **không đánh dấu phần tử nào là đích**, xếp theo thứ tự đọc từ trên xuống, cắt còn tối
đa 40 phần tử. Bước 6 giữ nguyên vai trò **trần**, tách bạch.

**Giới hạn phải khai kèm:** đo trên 300 màn của tập kiểm, cây trợ năng cho trung vị **89 phần tử
mỗi màn** nhưng **chỉ 14,1% có tên**. Nên danh sách nhét vào đầu vào phần lớn là vai trò kèm toạ
độ, ít chữ. Nghĩa là B-infer là một đối thủ **yếu hơn cái tên của nó gợi ra**, và nếu S2 thắng
B-infer thì **không được** kết luận "huấn luyện hơn đưa-thông-tin-lúc-chạy" một cách tổng quát —
chỉ được nói là hơn *khi thông tin đưa vào nghèo tên như ở đây*.

### (d) S3-pilot chưa có mã huấn luyện — khai thẳng

Nhánh S3-pilot (khoản phạt lề giữa khai báo thật và khai báo giả từ nút hàng xóm) mới có **dữ
liệu** (`desc_neg` trong `descriptors.jsonl`, dựng được cho 995/1074 bước) chứ **chưa có mã tính
mất mát**. Cần một hàm mất mát riêng gắn vào LLaMA-Factory. Chưa viết, và **cố ý chưa viết**: nó
nằm sau cổng C trong trình tự, còn viết bây giờ thì thành thêm một đoạn mã chưa từng chạy. Nếu tới
cổng C mà không kịp làm, phải khai là **nhánh đã đăng ký nhưng không chạy**, không được im lặng bỏ.

---

## Sửa đổi 9/8/2026 — KẾT QUẢ CỔNG A, và trần của thước

Cổng A đã chạy thật: UGround-V1-2B, 300 bước của tập kiểm lấy theo hạt giống 20260805, trên
Tesla T4 của Kaggle (miễn phí). Vết thô lưu ở `runs/gate_a/gate_A_raw.jsonl`.

### (a) Cổng A ĐẠT

| | |
|---|---|
| sai số trung vị | **0,7%** bề ngang màn (ngưỡng đã khoá: ≤3%) |
| phân vị 75 | 8,8% |
| số bước ≤3% | 62,7% |
| phân bố | p10 0,1% · p25 0,2% · p50 0,7% · p75 9,1% · p90 36,3% |

Dụng cụ này hai thái cực: trúng thì trúng ngay tâm, trượt thì trượt hẳn. **⇒ dùng ô-Voronoi làm
thước chính, chạy tiếp theo kế hoạch.**

Nhắc lại để khỏi đọc nhầm về sau: con số này đo trên **câu chuẩn do người viết**, tức đầu vào
hoàn hảo. Nó đo DỤNG CỤ, không đo mô hình nào cả.

### (b) Một trong bốn dấu hiệu lỗi cài đặt có kêu — đã truy, và nó KHÔNG phải lỗi cài đặt

Dấu hiệu "x đúng giữa màn" kêu ở 30,7% (ngưỡng 20%). Truy bằng bảng 2×2, chéo với vị trí của
chính điểm chạm chuẩn:

| | n | trung vị | ≤3% |
|---|---|---|---|
| trỏ giữa · chuẩn **giữa** | 46 | 0,4% | 82,6% |
| trỏ giữa · chuẩn **lệch** | 46 | 12,2% | 6,5% |
| trỏ lệch · chuẩn giữa | 9 | 44,3% | 0,0% |
| trỏ lệch · chuẩn lệch | 199 | 0,4% | 73,9% |

Điểm chạm chuẩn của người cũng nằm giữa màn ở **18,3%** số bước — hợp lý, vì hàng danh sách,
thanh tìm kiếm và nút toàn chiều rộng đều có tâm ở giữa. Nhưng trong 245 bước có chuẩn **không**
ở giữa, bộ trỏ vẫn trả x đúng giữa ở 46 bước; tính riêng trong nhóm trượt thì khoảng 45% số lần
trượt là trượt về đúng giữa màn. Dải "đúng giữa" chỉ chiếm ~1% trục x, nên trượt ngẫu nhiên
không rơi vào đó nhiều thế được.

⇒ **Đây là một kiểu hỏng thật của bộ trỏ** (không nhận ra phần tử thì bỏ trục ngang về giữa),
ảnh hưởng **15,3%** số bước. Nó làm con số xấu đi chứ không đẹp lên, nên cổng A đạt một cách hợp
lệ. **Phải khai kèm mỗi lần trình cổng A.**

### (c) TRẦN CỦA THƯỚC = 70,0% — số phải in cạnh mọi kết quả S1/S2

> ⛔ **SỐ TRONG MỤC NÀY ĐÃ ĐƯỢC THAY — xem mục sửa đổi (r) ngày 15/8 ở cuối file.**
> Trần đo lại trên **đủ 4.462 bước** ra **75,7% [74,1–77,3]**, không phải 70,0%. Mục này giữ
> nguyên làm bản ghi phép đo 9/8 trên mẫu con 300 bước, **không dùng số**.

Cổng A đo khoảng cách, còn thước chính là ô-Voronoi. Đem chính 300 điểm trỏ đó chấm bằng
`hit_voronoi` (mã: `harness/gate_a_ceiling.py`, chạy offline, không gọi lại bộ trỏ):

| | |
|---|---|
| **ô-Voronoi tâm — trần** | **70,0%**  KTC95 [64,5%, 75,3%] |
| đĩa dung sai — trần | 81,3%  KTC95 [76,6%, 86,0%] |
| cụm | 239 (hiệu dụng 191,5) · trung vị 72 phần tử mỗi màn · 0 màn thiếu cây trợ năng |

Vì câu đưa vào là câu chuẩn nên `action_ok` và `toggle_ok` đúng theo định nghĩa; điểm
executable rút gọn còn đúng phần định vị. **Mọi điểm S1/S2 phải đọc trên nền 70, không phải
100.** Một nhánh đạt 45% là đạt 64% của trần chứ không phải "kém quá nửa". Và vì câu mô hình
khác câu chuẩn, 70,0% là **cận trên**: bộ trỏ nhận câu tệ hơn thì chỉ có thể tệ đi.

### (d) Ngưỡng 3% được xác nhận bằng dụng cụ thật, trên tập kiểm thật

| dải sai số | n | Voronoi | đĩa |
|---|---|---|---|
| ≤3% | 188 | **100,0%** | 100,0% |
| 3-5% | 21 | 66,7% | 100,0% |
| 5-8% | 16 | 43,8% | 100,0% |
| 8-14% | 12 | 8,3% | 100,0% |
| >14% | 63 | 0,0% | 11,1% |

Dưới 3% thì **không có ca kết oan nào** — đúng như đường cong đo trước bằng Voronoi trên cây trợ
năng (3% → 0%), nay xác nhận lại trên đúng dụng cụ và đúng tập sẽ dùng để chấm. Ngưỡng cổng A
không còn là con số mượn.

Bảng này cũng chốt lại việc đã quyết ngày 6/8: **đĩa dung sai vô dụng** — nó cho 100% ngay cả khi
bộ trỏ lệch 8-14% bề ngang màn. Giữ ở vai trò báo kèm, không bao giờ làm headline.

### (e) `use_cache=False` trong generation_config của UGround

Đo trên T4: 32 token mất **38,65 s** với cache tắt, **4,16 s** với cache bật — chậm 9,3 lần.
Cổng A đã chạy ở cấu hình mặc định (tắt), nên **kết quả trên không bị ảnh hưởng**.

**Đã kiểm chứ không suy luận:** chạy lại 50 bước đầu của chính mẫu 300 đó với cache bật, so từng
toạ độ với vết đã lưu — **trùng tuyệt đối 50/50**, sai khác đúng bằng 0 chứ không phải "trong
dung sai" (`runs/gate_a/cache_check.jsonl`, 201,5 s cho 50 bước = 4,03 s/bước). ⇒ bật `use_cache=True`
nói thẳng ở mọi chỗ gọi `generate` trong `score_run.py` và `infer_branch.py`, không để mặc định
của mô hình quyết. Một lượt chấm đủ 4.463 bước rút từ ~48 giờ xuống **~5 giờ**.

### (f) Cấu trúc cụm của tập kiểm đủ — đầu vào cho MDE

Tính trên toàn bộ 4.463 bước chạm, theo đúng luật cụm-đơn đã khoá ở sửa đổi 6/8 (e1):

| | G | G hiệu dụng | app thật | cụm-đơn |
|---|---|---|---|---|
| toàn bộ bước chạm | 1.091 | **454,3** | 259 | 832 |
| mẫu 300 của cổng A | 239 | 191,5 | 83 | 156 |

Cụm lớn nhất của tập đủ là 58 bước, tức không có ứng dụng nào chi phối. MDE **chiếu** theo
`2,8·sd/√G_eff`: sd hiệu số theo cặp 0,30 → 3,9 pp · 0,40 → 5,3 pp · 0,50 → 6,6 pp. Vẫn là
**chiếu, chưa phải đo** — sd thật chỉ biết sau khi có điểm S1 hai hạt giống, và cam kết "Δ rơi
vào 4-9 pp thì báo chưa kết luận được" giữ nguyên.


### (g) Cấu hình huấn luyện đã được LLaMA-Factory nhận — chạy thử 10 bước, miễn phí

Chạy trên Kaggle T4, 60 mẫu nhánh S1, 10 bước (`thesis_kaggle_smoketrain.zip`). Mục đích là
kiểm cấu hình, **không** lấy trọng số — đã xoá ngay sau khi chạy.

**Tham số huấn luyện đếm được: 14.966.784.** Tính tay lại cho Qwen2.5-VL-3B: 36 tầng ×
(q 32.768 + k 18.432 + v 18.432 + o 32.768 + gate 104.448 + up 104.448 + down 104.448) =
14.966.784 — khớp từng chữ số. ⇒ LoRA r=8 gắn đúng cả 7 mô-đun trên đủ 36 tầng, và
`freeze_vision_tower: true` có tác dụng thật (không đóng băng thì con số phải lớn hơn nhiều).
Ảnh vào thật: `<image>` không có ảnh đi kèm thì bộ xử lý Qwen2-VL báo lỗi cứng, không im lặng.

**Không được đọc từ lượt chạy này:** mất mát không giảm (1,508 → 2,025). Ở 10 bước cỡ lô 2 thì
đó là chênh lệch giữa các mẫu, không phải chênh lệch do học. `grad_norm: inf` ở bước 8 là fp16
tràn số trên T4, máy thuê chạy bf16 sẽ không gặp.

**Ghi nhớ cho máy thuê:** Kaggle cấp T4 ×2 nên nó tự chạy song song và cỡ lô hiệu dụng thành 2
thay vì 1. Cỡ lô hiệu dụng phải giữ y hệt giữa các nhánh, nên trước mỗi lượt train phải kiểm số
card thật sự có.

### (h) `cutoff_len: 2048` không cắt cụt nhánh nào

Đếm bằng chính bộ tách token của `Qwen2.5-VL-3B` trên toàn bộ 1.697 mẫu mỗi nhánh, cộng 320
token thị giác (trần theo `image_max_pixels: 1003520`):

| nhánh | trung vị | p95 | tối đa | vượt 2048 |
|---|---|---|---|---|
| s1 | 515 | 595 | 756 | 0 |
| s2 | 541 | 625 | 785 | 0 |
| s2r | 540 | 625 | 785 | 0 |
| s2_nopoint | 531 | 612 | 771 | 0 |

Biên còn rộng gấp 2,6 lần. Đồng thời xác nhận lại phép ghép độ dài của S2r trên **toàn bộ** dữ
liệu chứ không chỉ trên mẫu: trung vị 540 so với 541 của S2, chênh 1 token.

---

## Sửa đổi 9/8/2026 (bổ sung) — tiền trạm đường sinh câu, chạy miễn phí trước khi thuê máy

Rà dấu vết trên đĩa cho thấy `infer_branch.py` **chưa từng chạy một lần nào** (không có tệp
`preds_*.jsonl` nào trong repo), và `score_run --mode score` cũng vậy. Nếu để nguyên thì lỗi ở
hai script này chỉ lộ ra **sau 18 giờ tiền máy** của lượt train đầu. Đã chạy hết trên Kaggle T4
bằng mô hình gốc chưa huấn luyện.

### (i) Ba mắt xích đã thông

| phép | kết quả |
|---|---|
| `--selftest-batch` (lô 1 vs lô 8) | **8/8 trùng nguyên văn** — đệm bên trái đúng, chấm theo lô an toàn |
| sinh câu 20 bước | chạy hết, có OCR, câu tiếng Anh đọc được |
| `--mode score` trên 20 bước đó | in đủ ô-Voronoi + khoảng tin cậy + số cụm, không lỗi |

Điểm của mô hình **chưa huấn luyện**: 45,0% ô-Voronoi, KTC95 [23,8%, 68,4%] trên n=20. Khoảng
tin cậy rộng tới mức không kết luận được gì — **không được trích như một mốc**. Nhưng nó gợi một
việc nên làm, xem mục (k).

### (j) B-infer: câu nhắc dài gấp đôi vùng đã thấy lúc dạy — GIỚI HẠN MỚI PHẢI KHAI

Đo trên 300 bản ghi, đếm bằng bộ tách token của Qwen2.5-VL-3B, cộng 320 token thị giác:

| | trung vị | p95 | tối đa |
|---|---|---|---|
| câu nhắc thường | 486 | 556 | 763 |
| câu nhắc B-infer | **1.149** | 1.338 | 2.048 |

Chuỗi dài nhất trong toàn bộ dữ liệu dạy là **785 token** (sửa đổi mục h). ⇒ **257/300 = 85,7%**
bản ghi của B-infer nằm ngoài vùng độ dài mô hình từng thấy. Thêm nữa, trần 40 phần tử chạm ở
gần như mọi màn (trung vị 40 = tối đa 40, trong khi màn có trung vị 72 phần tử), nên danh sách
đưa vào luôn là bản đã cắt.

**Hệ quả cho luật đọc kết quả:** nếu B-infer thua S2, **không được** kết luận thẳng "đưa thông
tin lúc chạy kém hơn huấn luyện". Phải khai kèm hai điều kiện làm B-infer thiệt: câu nhắc dài
gấp 2,4 lần vùng đã dạy, và danh sách bị cắt còn 40/72 phần tử. Cộng với giới hạn đã khai ở sửa
đổi 7/8 mục c (chỉ 14,1% phần tử có tên), B-infer là **đối thủ yếu hơn tên gọi của nó** ở ba
phương diện độc lập.

### (k) Đề xuất thêm một nhánh tham chiếu: mô hình gốc, không huấn luyện

Sáu nhánh đã đăng ký đều là nhánh **đã huấn luyện** (trừ B-infer, dùng trọng số S1). Không nhánh
nào trả lời câu hỏi: *bản thân việc SFT mua được bao nhiêu?* Nếu S1 xấp xỉ mô hình gốc thì tiền
đề của cả thiết kế lung lay, và tốt nhất là biết điều đó trước khi diễn giải Δ giữa S1 và S2.

Nhánh này **chỉ tốn suy luận, không tốn huấn luyện** (~1,5 giờ máy), và đăng ký ở đây là hợp lệ
vì **chưa có nhánh nào được huấn luyện, chưa thấy một con số thật nào**. Vai trò: **tham chiếu,
không phải headline**. Headline vẫn là Δ = S2 − S1.


### (l) S3-pilot: khai báo giả tách được bằng một chuỗi cố định — phải sửa dữ liệu trước khi viết mã

Rà `desc_neg` trong `descriptors.jsonl` (995/1074 bước) thấy **ô thứ tư của khai báo giả là hằng
số**: chuỗi `"phần tử hàng xóm"` xuất hiện ở **994/995 = 99,9%** bản ghi, trong khi ô thứ tư của
khai báo thật không bao giờ mang chuỗi đó (**trùng 0/995**). Khai báo thật có mỏ neo chữ ở 68,6%,
khai báo giả **0%**.

⇒ Khoản phạt lề sẽ **không dạy được gì về tính phân biệt**. Mô hình chỉ cần học "chuỗi *phần tử
hàng xóm* là bản xấu" — một luật dò chữ, không cần nhìn ảnh. Nếu để nguyên mà chạy, S3-pilot có
thể cho lề rất đẹp và con số đó **hoàn toàn vô nghĩa**.

**Cách sửa đã chốt:** ô thứ tư của khai báo giả phải tính bằng **đúng hàm đã dùng cho khai báo
thật**, nhưng chạy trên phần tử hàng xóm — tức mỏ neo chữ của chính nó, hoặc vế đếm của chính
nó. Sửa nằm trong `descriptor_label_build.py`, phải xong **trước** khi dựng dữ liệu ở quy mô đủ
trên máy thuê, vì dựng lại sau là dựng lại từ đầu.

**Không ảnh hưởng nhánh nào khác:** S2r bốc khai báo giả từ **màn khác** chứ không dùng
`desc_neg` (`build_branch_data.py` dòng 97-149), nên đối chứng của phép so chính vẫn sạch.


### (m) Phép thử TRẦN (bước 6) không có mã ở bất cứ đâu — đã cài, 9/8

Rà `run_on_rented.sh` đối chiếu với trình tự cứng mục 5 thì bước 6 — *"nối dòng khai báo chuẩn
vào đầu vào, so với một đoạn đệm vô nghĩa cùng độ dài"* — **không có lệnh nào chạy được**, và
`infer_branch.py` cũng không có chế độ đó. Đây là chỗ thứ tư cùng loại đã bắt (sau script suy
luận, script chấm, thước không-gây-hại): nằm trong hồ sơ, tới lúc cần thì không có gì chạy.

**Đã cài:**

- `descriptor_label_build.py --split test` — dựng nhãn khai báo cho tập kiểm. Đo được:
  **4.448/4.463 = 99,7%** bước chạm dựng được; tên rõ 74,1% · vai trò rõ 74,9% · trùng tên 7,6%
  — khớp sát tập dạy (73,8% / 76,0% / 7,0%), tức hai tập cùng phân bố.
  ⚠ Tập kiểm **không ghi w/h** và **4,75% ảnh không phải 1080×2400** (có cả 1440×3120 và
  1080×2340). Mặc định cứng sẽ tính sai ô `<point>` ở đúng nhóm đó mà không báo gì — nay đọc
  kích thước thật từ tệp ảnh.
- `infer_branch.py --ceiling gold|filler` — nối khai báo chuẩn của phần tử đích vào đầu vào, và
  nhánh đệm vô nghĩa **ghép độ dài theo TOKEN** (không theo ký tự — đúng lỗi đã bắt ở S2r ngày
  7/8). Đo trên 120 bản ghi: **120/120 lệch ≤2 token**, và đệm luôn dài hơn gold đúng 1 token,
  tức đối chứng lệch về phía **bất lợi cho nhánh gold**, không nới tay.
- `run_on_rented.sh ceiling <nhánh> <hạt giống>` chạy cả hai rồi chấm.
- Chặn cứng: `--b-infer` và `--ceiling` **không chạy chung được** — hai thí nghiệm khác nhau.

**Luật đọc:** trần là **hiệu số gold − filler**. Hiệu số gold − S1 gồm cả phần do đầu vào dài
thêm, không được dùng thay.

### (n) Nhánh tham chiếu mô hình gốc — đã có lệnh

`run_on_rented.sh base` chạy `--no-adapter` rồi chấm. Chỉ tốn suy luận.

### (o) Sửa đổi 11/8/2026 — máy, cấu hình chạy, và LUẬT CHỌN ĐIỂM LƯU

Ghi **trước** khi lượt train đầu tiên chạy xong, tức trước khi nhìn thấy bất kỳ con số kết
quả nào.

**1. Máy và cấu hình chạy.** Google Colab, **A100-SXM4-40GB**, một card, bf16 thật. Cấu hình
= `harness/train_config.yaml` giữ nguyên, **thêm đúng một khoá `enable_liger_kernel: true`**.

Liger là kernel hợp nhất — cùng công thức, chỉ khác thứ tự cộng dồn dấu phẩy động. Đã kiểm
chứ không tin lời thư viện: chạy có và không có liger trên **cùng 200 mẫu, cùng `seed 101`,
cùng thứ tự**, loss trùng tới chữ số thứ tư (3.189/3.188 · 3.014/3.015 · 2.597/2.595 ·
2.545/2.545). ⇒ **mọi siêu tham số QLoRA khoá ở mục 2 giữ nguyên**, đây không phải thay đổi
thiết kế. Lý do dùng: nhanh hơn 3% và giảm bộ nhớ bảng logits.

⛔ Đã thử và **loại**: bỏ lượng tử hoá 4-bit (chậm hơn 38% — trái với dự đoán, mô hình 3B đủ
nhỏ để khâu giải nén không thành nút thắt); tắt gradient checkpointing (nhanh hơn 15% trên
mẫu thường nhưng **tràn bộ nhớ ở chuỗi dài nhất của s2**, tức sẽ chết giữa lượt train 23
giờ). Số đo đầy đủ: `report/110` mục 4h → 4h-6.

**2. `cutoff_len` nâng 2048 → 2560** (11/8, trước lượt train đầu tiên — thời điểm duy nhất
được phép đổi). Lý do đo được: chuỗi dài nhất của s2 là 2.017 token, dư đúng 31 token so với
trần cũ, mỏng hơn sai số của phép đếm. Cắt cụt xảy ra ở **đuôi**, mà đuôi là đích sinh, và
**s2 dài hơn s1 nên bị cắt nhiều hơn** — tức thiên vị đúng chiều làm hỏng con số headline.
Nâng trần không tốn thêm gì vì đệm theo lô chứ không theo trần.

**3. LUẬT CHỌN ĐIỂM LƯU — khoá từ bây giờ.** Bản gốc không nói chọn điểm lưu nào; đó là một
bậc tự do chưa khoá và phải bịt trước khi có số.

- **Dùng điểm lưu CUỐI CÙNG** (hết đủ 2 lượt duyệt) cho **mọi nhánh, mọi hạt giống**. Số
  lượt duyệt đã khoá bằng 2 ở mục 2; chọn điểm lưu cuối là hệ quả trực tiếp.
- Điểm lưu cuối lượt duyệt thứ nhất (bước 4.000) được **sao ra thư mục riêng làm bảo hiểm
  kỹ thuật**, phòng khi lượt hai hỏng. **Không được dùng nó để chọn theo điểm trên tập
  kiểm** — chọn như vậy là để tập kiểm lọt vào quyết định huấn luyện.
- Chỉ được dùng bản một lượt duyệt khi lượt hai **hỏng rõ ràng và độc lập với điểm số**
  (mất mát phân kỳ hoặc `nan`), và khi đó **phải khai trong luận văn**.
- Không có tập thẩm định trong lúc huấn luyện (`val_size: 0.0`) — đây là lựa chọn có ý
  thức: tách tập thẩm định từ dữ liệu dạy sẽ làm bốn nhánh lệch nhau, mà điều kiện sống còn
  của phép so là bốn nhánh thấy đúng cùng một bộ dữ liệu.

### (p) Sửa đổi 12/8/2026 — định nghĩa lại nhãn `app_seen_in_train` của lát cắt phụ

**Ghi TRƯỚC khi có bất kỳ điểm số nào.** Lượt train s1 hạt giống 101 đang chạy, chưa có
câu sinh, chưa chấm. Đây là điều kiện để việc sửa này không phải là chọn theo kết quả.

**Đụng cái gì.** Chỉ lát cắt phụ đăng ký ở mục sửa đổi 6/8 ý 4 ("nhóm ứng dụng chưa thấy
lúc dạy"). **Không** đụng phép so chính S1-vs-S2, không đụng thước đo, không đụng tập kiểm
(vẫn 6.958 bước / 4.463 bước chạm / 1.432 tác vụ), không đụng dữ liệu dạy.

**Vì sao phải sửa.** Nhãn cũ có hai khuyết tật đã đo được:

1. Con số **67 bước chạm** ghi ở mục sửa đổi 6/8 do một lượt vá tay để lại, **không có mã
   sinh ra** nên không tái lập được, và nó đối chiếu với split train ĐẦY ĐỦ của
   AndroidControl chứ không phải 12.895 tác vụ thật sự đem dạy. Nhãn này phải là hàm của
   tập dạy thật sự dùng.
2. `harness/tag_app_seen.py` (viết 6/8 để thay lượt vá tay) suy tên ứng dụng của tập dạy
   bằng **regex trên câu chữ**, trong khi tập kiểm đọc trường `app_name`. Nó quét `goal`
   trước lịch sử rồi dừng, nên câu mục tiêu dài lọt vào thành tên ứng dụng và tên sạch
   trong lịch sử không bao giờ được đọc tới. Đo trên lát 1.697 bước: **42/129 tên suy ra là
   rác**, và **27 ứng dụng có thật trong tập dạy bị đếm nhầm thành chưa-thấy** (`maps`,
   `nike`, `citymapper`, `skyscanner`, `tripadvisor`, `google play books`…).

**Định nghĩa mới, khoá từ đây.** Một ứng dụng được coi là **đã thấy lúc dạy** khi tên của
nó — sau chuẩn hoá — xuất hiện trong dữ liệu dạy thật sự dùng, theo một trong hai nguồn:

- **nguồn chính:** trường `app_name` của thao tác `open_app` trong `train.jsonl`. Đây đúng
  là trường mà `build_test_data.app_of` dùng cho tập kiểm, nên hai bên đọc cùng một nguồn.
- **nguồn phụ:** câu chuẩn dạng "Open the X app" trong lịch sử, để bắt các tác vụ mở ứng
  dụng bằng cách bấm thay vì bằng thao tác `open_app`.
- **chuẩn hoá:** hạ chữ thường, gộp khoảng trắng, bỏ dấu chấm ở hai đầu, và bỏ ký tự vô
  hình — tập kiểm có `audio­mack` (gạch nối mềm), `yandex maps` (khoảng trắng cứng),
  `contacts﻿+` (BOM), đều là chỗ so chuỗi trượt mà mắt thường không thấy.

**Chiều lỗi chọn có chủ ý, khai luôn:** giữ nguồn phụ làm cho nhãn nghiêng về "đã thấy".
Gán nhầm thành *đã thấy* chỉ pha loãng nhóm lớn (~2.500 bước); gán nhầm thành *chưa thấy*
bóp méo đúng nhóm nhỏ đang xét. Đã kiểm nguồn phụ không kéo theo rác: 2 chuỗi rác nó sinh
ra không trùng tên ứng dụng nào của tập kiểm.

**Ba giá trị giữ nguyên cách đọc:** `True` đã thấy · `False` gán được ứng dụng và không có
trong tập dạy · `None` **không gán được ứng dụng = KHÔNG BIẾT**, cấm đọc thành "chưa thấy"
(nhóm này 3.828 bước, lớn hơn cả hai nhóm kia cộng lại).

**Cỡ mẫu mới chưa biết, và không được dùng để cứu.** Số thật chỉ có sau khi chạy ô A.1d
trên Colab với `train.jsonl` đủ 64.567 bước. Dù ra bao nhiêu, lát này vẫn giữ nguyên tư
cách đã đăng ký 6/8: **thiếu lực nghiêm trọng, chỉ đọc theo hướng, không kết luận, không
dùng để cứu nếu kết quả chính không như ý.**

**Mã:** `harness/tag_app_seen.py` (docstring ghi chi tiết) · chạy bằng ô A.1d của
`harness/run_on_colab.md` · lý do đầy đủ ở `report/110` mục 4j-5.

### (q) Sửa đổi 14/8/2026 — NHÃN KHAI BÁO ĐỔI SANG TIẾNG ANH

**Ghi TRƯỚC khi có bất kỳ điểm số nào và TRƯỚC khi huấn luyện nhánh s2.** Lượt s1
hạt giống 101 vừa chạy xong phần train, chưa sinh câu, chưa chấm. Đây là điều kiện
để việc sửa này không phải là chọn theo kết quả.

**Vì sao.** Đích của s2 là `<desc>…</desc>` rồi mới tới câu. Khai báo viết bằng
**tiếng Việt** (`mục | CATEGORIES | <point>127,238</point> | bên trái chữ "MEN"`)
còn câu đem chấm bằng **tiếng Anh**. Nghĩa là s2 khác s1 ở **hai** thứ cùng lúc: có
thêm dòng khai báo, **và** có thêm một lần chuyển ngữ. Hiệu `s2 − s1` — con số
headline khoá ở mục 6 — vì vậy lẫn cả phần do chuyển ngữ, và không có nhánh nào
tách được phần đó ra. (`s2 − s2r` thì tách được, vì s2r cũng tiếng Việt, nhưng mục 6
khoá headline là `s2 − s1`.)

**Đã đổi.** `harness/descriptor_label_build.py`: bảng `ROLE`, vế lùi
`("item" if cls in GENERIC else "element")`, bốn từ chỉ hướng của mỏ neo, năm chuỗi
của ô thứ tư, và `(không tên)` → `(no name)`. **Chỉ đổi chuỗi xuất ra, không đổi một
dòng logic nào.**

**Chứng minh là thay đổi thuần từ vựng** — dựng lại trên lát 1.697 bước rồi đối
chiếu từng trường với bản cũ:

| | |
|---|---|
| Cùng tập khoá | có · n = 1.074 |
| Trường ĐỔI | đúng 4: `desc` · `role` · `hint` · `desc_neg` |
| Trường GIỮ NGUYÊN 100% | 17 trường, gồm `point_norm` · `point_abs` · `box` · `name` · `name_src` · `tier` · `dup_name` · `same_role` · `neighbor_dist_px` · `area_share` · `target_instruction` |
| Ký tự tiếng Việt còn lại trong nhãn | **0** |
| Phân bố nhãn | **trùng khít**: tên rõ 793 = 73,8% (trợ năng 224 · OCR 599) · ký hiệu 30 = 2,8% · không tên 251 = 23,4% · vai trò rõ 816 = 76,0% · trùng tên 75 = 7,0% · có hàng xóm 995 = 92,6% · hộp quá to 25 = 2,3% |

Phân bố không xê dịch một ca nào ⇒ mọi con số đã công bố về chất lượng nhãn **vẫn
đúng nguyên văn**, không phải đo lại.

**KHÔNG đổi:** thước đo · tập kiểm · luật đọc kết quả · danh sách nhánh · siêu tham
số · tập dạy. Lượt s1 đang có **không phải train lại**, vì đích của s1 là câu trơn,
không chứa khai báo.

**Việc bắt buộc trước khi train s2:** dựng lại `descriptors.jsonl` và bốn tệp nhánh ở
**quy mô đủ** trên Colab (ô 0.10 → 0.11), rồi chạy lại 9 bất biến và phép ghép độ dài
token của S2r. Lát 1.697 bước ở máy nhà chỉ đủ chứng minh thay đổi là thuần từ vựng,
**không thay được bản dựng đủ**.

**Một thứ CỐ Ý KHÔNG đổi, và phải khai.** Câu nhắc đưa vào mô hình
(`build_branch_data.SYS` và `prompt_body`) cũng là tiếng Việt: nhãn trường
*"Mục tiêu / Đã làm / Chữ đọc được trên màn"*, kèm lệnh viết câu trả lời bằng tiếng
Anh. Giữ nguyên vì hai lý do: (a) câu nhắc **giống hệt nhau ở mọi nhánh và ở cả khâu
chấm** (mọi nhánh gọi chung `prompt_of`), nên nó là hằng số của thí nghiệm và không
thể giải thích chênh lệch giữa các nhánh; (b) đổi nó thì phải train lại s1 (~24 giờ,
~126 đơn vị) mà không mua được tính hợp lệ nào. Đã khai thẳng trong bài FAIR mục V-A.

---

## Sửa đổi 15/8/2026 — (r) TRẦN CỦA THƯỚC ĐO LẠI: 70,0% → **75,7%**

**Không sửa đè mục (c) ở trên.** Mục đó giữ nguyên làm bản ghi phép đo ngày 9/8; mục này ghi
phép đo thay thế.

**Vì sao đo lại.** Trần ở mục (c) tính offline từ **300 điểm trỏ** mà cổng A giữ lại
(`gate_a_ceiling.py`). Ba nhánh đã chấm (Base · S1 · Human) đều chấm trên **4.462 bước**, nên
trần nằm trên tập khác với thứ nó dùng để đọc — không ghép cặp được, và khoảng tin cậy rộng
±5,4 điểm.

**Cách đo mới, 0 đồng và không cần GPU sinh câu.** Dựng tệp dự đoán trong đó `pred` chính là
`gold_instruction` của từng bước (`runs/preds_ceiling_human.jsonl`), rồi chấm bằng đúng
`score_run.py --mode score` như mọi nhánh. Vì `sent == gold_instruction` nên `action_ok` và
`toggle_ok` đúng theo định nghĩa và điểm rút gọn còn đúng phần định vị — cùng nguyên tắc với
mục (c). Đã kiểm tệp trước khi chạy: **4.462/4.462 câu trùng khít** `gold_instruction` mà
`score_run` tự ghi ra ở lượt S1.

| | cỡ mẫu | ô-Voronoi | đĩa |
|---|---|---|---|
| mục (c), 9/8 | 300 | ~~70,0% [64,5–75,3]~~ | 81,3% |
| **bản dùng, 15/8** | **4.462** | **75,7% [74,1–77,3]** | **84,3%** |

Chênh **+5,7 điểm**, nằm **ngoài mép trên** khoảng tin cậy cũ; KTC hẹp từ ±5,4 xuống **±1,6**.
⇒ **Mọi điểm S1/S2 đọc trên nền 75,7%, không phải 70,0%.**

**Ba số kéo theo phải sửa:** room cho can thiệp **741 bước / 16,6 pp** (bản cũ: 485 / 10,9) ·
S1 đạt **78,1% của trần** (bản cũ: 84,4%) · SFT lấy được **41%** khoảng Base→trần.

**Không đụng tới thiết kế nào đã đăng ký:** không đổi thước, không đổi luật chấm
(`metric_exec.py` không sửa dòng nào), không đổi nhánh, không đổi trình tự. Chỉ là **đo lại
cùng đại lượng trên toàn tập thay vì mẫu con**.

### (s) MDE phải tính theo thiết kế GHÉP CẶP, không phải hai mẫu độc lập

Các nhánh chấm trên **cùng tập bước**, nên hiệu số giữa hai nhánh là đại lượng ghép cặp: chỉ
đếm bước **bất đồng** (nhánh A đúng/B sai và ngược lại), kiểm định **McNemar**. Đo trên cặp
Base-vs-S1: SE của hiệu **0,64–0,75 pp**, so với **0,94 pp** nếu coi là hai tỉ lệ độc lập
⇒ **MDE ghép cặp 1,8–2,1 pp** chưa hiệu chỉnh cụm, **ước 2,7–4,5 pp có cụm** (so với MDE
chiếu cũ 3,9–6,6 pp).

Đây là thay đổi ở **cách đọc**, không ở dữ liệu, và nó **siết ngưỡng chứ không nới**. Ngưỡng
chốt vẫn phải tính lại từ **cặp hạt giống S1 thật** (101 và 202) rồi mới khoá — mục 5 không
đổi. Khi khoá, ghi **cả hai cách tính** vào mục sửa đổi để người đọc thấy đã chọn cách nào và
vì sao.

### (t) Sửa đổi 16/8/2026 — MDE ĐO ĐƯỢC LÀ 2,2 pp; DẢI "KHÔNG KẾT LUẬN ĐƯỢC" 4–9 pp BỊ RÚT

Ghi **trước khi chấm bất kỳ nhánh xử lý nào** (S2 chưa train xong). Đây là thời điểm hợp lệ
duy nhất để đụng vào luật đọc kết quả.

**Chỗ sai của bản cũ.** Công thức MDE `2,8·σ̂/√G_eff` (mục 6) chia cho căn của **G hiệu dụng
Kish**. Kish chỉ tính từ **kích thước cụm**, không đụng tương quan nội cụm — dùng nó làm mẫu số
là ngầm đặt tương quan nội cụm **bằng 1**. Trên dữ liệu thật, hệ số nở do gom cụm đo được chỉ
**1,10 lần**, nên công thức cũ **thổi MDE lên khoảng ba lần**.

**Số đo, thay cho số đoán.** Bootstrap gom cụm 10.000 lượt trên hiệu ghép cặp, cụm theo đúng
quy tắc đã đăng ký (app · mỗi tác vụ một cụm khi không gán được app):

| cặp | SE của hiệu | MDE (lực 80%, mức 5%) |
|---|---|---|
| S1 − Base, **có cụm** | **0,785 pp** | **2,20 pp** |
| Human − S1, có cụm | 0,759 pp | 2,12 pp |
| S1 − Base, không cụm | 0,717 pp | 2,01 pp |

⇒ Con số **2,7–4,5 pp** ở mục sửa đổi (s) là **ước chiếu, không phải phép đo — nay bị rút**.

**Hệ quả với luật đọc kết quả.** Bản cũ (mục 6) khai: hiệu số rơi giữa hai MDE, **khoảng
4–9 pp, đọc là "không kết luận được"**. Với MDE thật 2,2 pp, một hiệu ứng **+3 pp** sẽ có
khoảng tin cậy **loại trừ 0 ở p<0,001** mà vẫn bị luật cũ vứt đi — bảo thủ **sai hướng**, và
cái giá là lỗi loại II trên chính câu hỏi luận văn đặt ra.

**Luật thay thế, khoá từ đây:** ngưỡng lấy từ **SE bootstrap gom cụm của hiệu ghép cặp**, đo
trên các nhánh đã chấm. Hiệu số vượt 2,2 pp **và** vượt nhiễu giữa hai hạt giống S1 thì đọc là
dương; dưới nhiễu hạt giống thì đọc là âm có kiểm soát. Vẫn **cấm chọn quy tắc gom cụm sau khi
thấy điểm**, vẫn **báo cả hai cách tính** (độc lập và ghép cặp) trong mọi trường hợp.

**Không đụng:** thước, luật chấm, danh sách nhánh, trình tự chạy, ba lát cắt đã đăng ký.

### (u) Sửa đổi 16/8/2026 — BỘ TRỎ KHÔNG SẠCH ANDROIDCONTROL, VÀ CÙNG HỌ VỚI MÔ HÌNH ĐƯỢC CHẤM

Hồ sơ 29/7 ghi *"UGround SẠCH (không AC trong recipe)"*. **Sai, đã tra tận nguồn:** Bảng 1 của
arXiv 2410.05243 liệt kê **AndroidControl 47K phần tử, nhãn người**, cạnh Widget Caption 41K ·
UIBert 16K · AITZ 8K. Và **UGround-V1-2B dựng trên Qwen2-VL**, cùng dòng với Qwen2.5-VL-3B đang
bị chấm — nên câu "bộ trỏ khác họ mô hình" cũng sai.

**Mức độ nghiêm trọng, đo được:** họ dùng **split train** (*"we use the human-annotated actions
from the training set"*), tập kiểm của ta dựng từ **split test** ⇒ **không chồng lấn ở mức màn
hình**, không phải rò rỉ nhãn. Nhưng bộ trỏ **đã thấy văn phong chú thích của kho này**, mà s1
được dạy sinh đúng văn phong đó (đo được: **24,5% câu s1 lặp nguyên từ nội dung của câu chuẩn**)
⇒ **một lời giải thích thay thế cho chênh lệch s1−base mà 6 đòn phản biện chưa loại được**.

**Đã làm:** khai thẳng ở mục Limitations của bài FAIR; sửa chú thích sai trong `score_run.py`;
rút câu trong `CLAUDE.md`. **Chưa làm được, và là việc duy nhất đóng được đòn này:** chấm lại
lát ≥500 bước bằng bộ trỏ đã xác minh sạch AndroidControl (ứng viên tra 15/8:
`inclusionAI/UI-Venus-Ground-7B`), báo lại cả trần lẫn thứ tự ba nhánh.

**Không đụng thiết kế:** mọi nhánh vẫn chấm bằng **cùng một** bộ trỏ, nên phép so giữa các
nhánh vẫn là phép so trong cùng dụng cụ. Thứ bị ảnh hưởng là **mức độ tin của số tuyệt đối** và
**một đòn phản biện chưa khoá được**.

### (v) Sửa đổi 16/8/2026 — LỖI `canon_action`: `go back` BỊ QUY THÀNH CHẠM

**Lỗi.** `canon_action` quét câu từ trái sang phải, mà `go` và `navigate` (đều ánh xạ
sang *chạm*) đứng trước `back` trong câu, nên `go back`, `navigate back`, `press the
back button` đều ra **"tap"**. Lớp `navigate_back` mà mục 4 liệt kê là lớp riêng
**gần như không thể đạt tới** bằng ba cách nói tự nhiên nhất của nó.

**Ảnh hưởng, đo được trên quần thể chấm (toàn bước chạm):** 81 bước đổi phán quyết ở
s1, 47 ở base, **0 ở nhánh trần**; điểm đổi **59,12 → 58,81** và **47,60 → 47,40**.
Chênh lệch giữa hai nhánh gần như không đổi (11,52 → 11,41 pp).

**Xử lý — KHÔNG chấm lại ba nhánh đã chấm.** Sửa thước sau khi đã thấy điểm đúng là
thứ hồ sơ đăng ký sinh ra để chặn, **kể cả khi sửa làm số xấu đi**; và ở đây ảnh
hưởng dưới 0,4 pp, không đụng kết luận nào. Bài FAIR khai thẳng lỗi này cùng con số
ảnh hưởng, ngay tại chỗ định nghĩa điều kiện (i).

**Nhưng bản vá là BẮT BUỘC cho phép kiểm không-gây-hại.** Phép kiểm đó chạy trên
**35,9% bước không-chạm**, nơi thao tác `back` là thật và chiếm phần đáng kể — với
hàm cũ nó **không đo được thứ nó tuyên bố đo**. Phép kiểm này **chưa chạy lần nào**
(cần S2), nên vá bây giờ là hợp lệ tuyệt đối.

**Cách vá:** `metric_exec.canon_action(text, strict_back=False)`. Mặc định giữ hành vi
cũ để ba nhánh đã chấm còn tái lập được; **phải truyền `strict_back=True`** cho phép
kiểm không-gây-hại và cho mọi nhánh chấm từ đây trở đi nếu quyết định chấm lại toàn
bộ. Nếu về sau chấm lại tất cả bằng bản vá thì phải chấm lại **cả ba nhánh cũ** trong
cùng một lượt, không được trộn hai phiên bản thước trong một bảng.

---

## Sửa đổi 17/8/2026 — (w) CẶP HẠT GIỐNG ĐÃ ĐỦ. NGƯỠNG CHO S2 KHOÁ Ở **2,8 pp**

> Đây là mục **khoá ngưỡng** mà trình tự cứng ở mục 5 đòi phải hoàn tất **trước khi train
> S2**. Từ đây trở đi, mọi con số của S2 đọc theo luật ghi trong mục này. Mã tái lập:
> `harness/mde_that.py` (bootstrap cụm 10.000 lượt, hạt giống 20260805).

### 1. Null thực nghiệm — hai hạt giống, không can thiệp gì

Lượt `s1/seed202` xong 17/8, chấm trên **đúng 4.462 bước** như s1/101, Base và trần (cả hai
hạt giống bỏ **cùng một** bước `(18710, 1)` vì câu rỗng ⇒ ghép cặp sạch, không trừ bù).

| | |
|---|---|
| s1/101 → s1/202 | 59,12% → **59,64%** |
| hiệu ghép cặp | **+0,52 pp**, KTC95 bootstrap cụm **[−0,21 · +1,28]** |
| SE của hiệu | **0,38 pp** |
| McNemar | 101 trúng/202 trượt **132** · ngược lại **155** · χ²=1,69 **p=0,194** |
| bước bất đồng | **287 = 6,4%** |

✔ **KTC chứa 0 và p không có ý nghĩa** — đúng thứ một null phải cho. Nếu nó *không* chứa 0
thì đã có gì đó ngoài hạt giống thay đổi giữa hai lượt, và phải truy trước khi đi tiếp.

⭐ **Tỉ lệ bất đồng mới là thứ phân biệt null với hiệu ứng thật**, không phải con số hiệu:

| cặp | hiệu | bước bất đồng |
|---|---|---|
| 101 vs 202 (chỉ khác hạt giống) | +0,52 pp | **6,4%** |
| S1/101 vs Base (can thiệp thật) | +11,52 pp | 24,2% |
| S1/202 vs Base (can thiệp thật) | +12,03 pp | 24,0% |
| Trần vs S1/101 | +16,61 pp | 21,2% |

⭐ **Phát hiện chính đã TÁI LẬP bằng hạt giống độc lập:** S1−Base = **+11,52** và **+12,03 pp**,
hai KTC chồng lấn gần trọn ([+10,08 · +12,98] và [+10,62 · +13,46]). Bài viết được "hai lượt
train độc lập", không phải "một lượt".

**Nhiễu giữa hạt giống đi TRỌN VẸN qua đường câu chữ:** trong 287 bước bất đồng, **0 bước** có
hai câu giống nhau. Không có chút nhiễu nào đến từ thước. Và nhiễu tập trung vào **bước giải
được nhưng sát ranh giới** — ở nhóm bất đồng, câu người trúng **88,5%** so với 74,9% ở nhóm
đồng thuận; sai số trỏ trung vị 7,41%/4,11% so với 2,00% toàn tập.

### 2. Ngưỡng — cộng CẢ HAI nguồn nhiễu

So S2 với S1 có hai nguồn nhiễu, không phải một:

| nguồn | cách đo | giá trị |
|---|---|---|
| (a) nhiễu **thước** trên một cặp nhánh | bootstrap cụm trên hiệu ghép cặp | SE **0,38 pp** |
| (b) nhiễu **giữa hạt giống** | chính cặp 101/202 này | σ ≈ **0,46 pp** |

σ suy từ `E|X−Y| = 1,128·σ`. ⚠️ **Ước từ MỘT quan sát, 1 bậc tự do** — sai số của chính ước
lượng này rất lớn, σ thật có thể gấp đôi hoặc bằng nửa.

| thiết kế | SE tổng | MDE (lực 80%, α=0,05) |
|---|---|---|
| 1 hạt giống mỗi nhánh | 0,75 | 2,11 pp |
| **2 hạt giống mỗi nhánh** (đã đăng ký) | 0,60 | 1,67 pp |
| **THẬN TRỌNG — σ hạt giống ×2** | 0,99 | **2,78 pp** |

### 3. ⭐ LUẬT ĐỌC KẾT QUẢ S2 — khoá tại đây, không sửa sau

**Ngưỡng chốt: 2,8 pp** (làm tròn từ dòng thận trọng). Chọn dòng thận trọng vì (b) chỉ có 1 bậc
tự do; **khoá theo ước lỏng rồi tuyên bố dương là cách tự cho mình một kết quả dương giả**.

| Δ = S2 − S1 (trung bình 2 hạt giống mỗi nhánh, ghép cặp) | Kết luận |
|---|---|
| **≥ +2,8 pp** và KTC95 loại trừ 0 | **DƯƠNG** — thành phần có tác dụng |
| **+1,7 … +2,8 pp**, KTC95 loại trừ 0 | **DƯƠNG YẾU** — báo kèm nguyên văn cảnh báo rằng nó nằm dưới ngưỡng thận trọng và trên ngưỡng thiết kế; **không** đưa vào abstract |
| **−2,8 … +1,7 pp** | **TRẮNG** — không kết luận được; báo là kết quả âm có kiểm soát |
| **≤ −2,8 pp** | **ÂM** — thành phần làm hại; báo thẳng |

⛔ **Dải "4–9 pp là không kết luận được" của bản đăng ký gốc CHÍNH THỨC BỊ RÚT** (đã báo trước
ở mục sửa đổi (t) với số ước 2,2 pp; nay có số đo nên thay hẳn). Giữ nó sẽ **vứt bỏ một hiệu
ứng thật** có KTC loại trừ 0 ở p<0,001.

**Bắt buộc kèm khi báo Δ, không được bỏ:**
1. **Cả bốn con số riêng lẻ** (S1×2 hạt giống, S2×2 hạt giống), không chỉ trung bình
2. **Tỉ lệ bước bất đồng** — mốc so đã có: null 6,4% · can thiệp thật 24%
3. **Phân tầng theo độ dài câu** — thiên vị câu dài đo được 5,4 pp ở S1 và −1,4 pp ở Base,
   tức nó **không phải quy luật chung của thước**, phải đo riêng cho S2
4. Nếu hai hạt giống S2 lệch nhau **> 1,5 pp** (gấp ~3 lần null này) thì **dừng lại truy
   nguyên nhân** trước khi đọc Δ

**Dư địa:** 16,6 pp tới trần ⇒ S2 phải lấy **17% dư địa** mới đọc được. Hiệu ứng kỳ vọng theo
văn liệu trung vị ~+5 pp ⇒ **nằm trên ngưỡng**, nên thí nghiệm còn đáng chạy.

---

## Ghi nhận 18/8/2026 — điều kiện bắt buộc của mục sửa đổi (q) ĐÃ THỰC HIỆN

Mục (q) ngày 14/8 đổi nhãn khai báo sang tiếng Anh và ghi: *"Việc bắt buộc trước khi train s2:
dựng lại `descriptors.jsonl` và bốn tệp nhánh ở quy mô đủ trên Colab, rồi chạy lại 9 bất biến
và phép ghép độ dài token của S2r."*

**Thực hiện 18/8, TRƯỚC khi khởi động lượt train s2 đầu tiên.** Phát hiện dữ liệu trên Drive
vẫn là bản tiếng Việt khi đọc trường `labels` của lượt thăm dò bộ nhớ — tức bắt được ở khâu
kiểm, không phải sau khi đã train.

| phép kiểm | kết quả |
|---|---|
| tiếng Việt ở **khuôn mẫu** (vai trò · dấu hiệu) | **0** |
| dấu phụ ở **tên phần tử** | 1 (`Save Tôrres to lists`) — chữ thật trên màn, hợp lệ |
| chín bất biến của bốn nhánh | **9/9 ĐẠT** |
| s2r ghép độ dài token với s2 | **99,9%** trong 2 token (mốc 14/8: 99,3%) |
| quy mô | **64.567** mẫu mỗi nhánh · **41.099** khai báo |

**Bằng chứng độc lập rằng đây là thay đổi thuần từ vựng:** `total_flos` của lượt thăm dò 20
bước trên 200 mẫu dài nhất — bản tiếng Anh **10.812.978 GF**, bản tiếng Việt **10.816.688 GF**,
lệch **0,03%**. Đổi ngôn ngữ không làm chuỗi dài ra hay ngắn đi, đúng như (q) tuyên bố.

Tệp: `MyDrive/thesis/derived_train_en.tar.gz`. Bản tiếng Việt giữ ở `branches_vi_0818/` để đối
chiếu, **không xoá**.

**Không đụng:** thước, luật chấm, danh sách nhánh, siêu tham số, tập kiểm, ngưỡng 2,8 pp.

---

## Sửa đổi 23/8/2026 — (x) NHÁNH S2 DỪNG Ở MỘT HẠT GIỐNG · ĐĂNG KÝ TRƯỚC **MIN-DESC**

> **Mục này viết TRƯỚC khi có bất kỳ lượt huấn luyện MIN-DESC nào.** Không tồn tại checkpoint,
> log hay điểm số nào của MIN-DESC vào lúc viết. Kiểm được bằng `git log`: commit chứa mục này
> phải đứng trước mọi commit có kết quả MIN-DESC.

### (x1) Nhánh S2 dừng — quyết định của chủ luận văn 23/8/2026

Estimand đã khoá ở mục (w) là `Δ = mean(S2/101, S2/202) − mean(S1/101, S1/202)`. **Hạt giống
S2/202 sẽ không được chạy.** Quyết định của chủ luận văn, lý do ngân sách. Hệ quả, ghi thẳng:

- Estimand (w) **vĩnh viễn không hoàn tất**. `−2,19 pp` của S2/101 nằm trong dải **trắng**
  (−2,8 … +1,7), và **ở nguyên đó** — không được nâng lên thành kết quả âm về sau.
- Bốn câu cấm ở `report/116` Mục 2 chuyển từ *cấm tạm* thành **cấm vĩnh viễn**: không được viết
  "giả thuyết chính đã bị bác bỏ", "S2 gây hại theo đại lượng đăng ký trước", "hiệu ứng gấp 3,7
  lần nhiễu nên đã kết luận", "McNemar p<0,001 đã bao gồm biến thiên hạt giống".
- Câu duy nhất được phép nói về S2 là câu ở `report/116` Mục 2, kèm chữ **thăm dò, một hạt giống**.
- Mọi phân tích S2 trong luận văn (kể cả chẩn đoán 4j-18 và phép B UI-Venus) mang nhãn **thăm dò**.

### (x2) MIN-DESC là estimand MỚI, và headline mới là lựa chọn HẬU KIỂM — khai thẳng

MIN-DESC **không** nằm trong hồ sơ gốc 5/8. Việc chọn nó làm đóng góp mô hình diễn ra **sau khi**
đã thấy S2/101 thấp hơn S1. Đó là lựa chọn hậu kiểm và **phải được trình bày đúng như vậy**;
không được viết như thể nó đã được đăng ký từ đầu. Cái được khoá trước là **thiết kế, thước và
ngưỡng của chính MIN-DESC** — mục này — chứ không phải việc chọn nó.

### (x3) Thiết kế

Tiếp tục huấn luyện từ **checkpoint S2** bằng ORPO trên cặp quy chiếu tối thiểu ở **tầng khai báo**:

```
chosen   = <desc>đúng</desc>       + "\n" + câu người
rejected = <desc>desc_neg</desc>   + "\n" + câu người      ← câu Y HỆT, chỉ ô khai báo đổi
```

`desc_neg` do `descriptor_label_build.nearest_other()` dựng sẵn từ tháng 8, không dựng mới cho
mục đích này. Cặp dựng bằng `harness/build_min_desc.py`, biến đổi thẳng từ `branches/s2.json`
nên prompt và đường dẫn ảnh trùng byte-với-byte nhánh S2.

**Sáu điều kiện nhận cặp:** có `desc` và `desc_neg` · hai chuỗi khác nhau · ô TÊN khác nhau sau
chuẩn hoá · ô POINT khác nhau · khoảng cách tâm tới negative trong **80–350 px** · mẫu `s2.json`
khớp đúng khai báo trong `descriptors.jsonl`.

**Đối chứng quy công CE2-S2:** tiếp tục SFT từ **đúng cùng checkpoint S2**, trên **đúng cùng
22.854 bước**, học **đúng vế chosen**, cùng số update, cùng LR schedule, cùng hạt giống.

**Bốn lượt:** MIN-DESC/101 · MIN-DESC/202 · CE2-S2/101 · CE2-S2/202. Stage-2 tối đa **800
optimizer updates**, `pref_loss: orpo`, `β = 0,1`, một rejected mỗi chosen, **final checkpoint**
— không chọn best checkpoint bằng bất cứ thứ gì.

### (x4) Số đã đo TRƯỚC khi train, ghi lại để sau này kiểm được

| phép đo | kết quả |
|---|---|
| eligibility tầng khai báo, có lọc 80–350 px | **22.854 / 41.099 = 55,61%** |
| eligibility tầng khai báo, không lọc khoảng cách | 31.358 = 76,30% |
| eligibility tầng CÂU (thiết kế `report/116` Mục 12.2) | **26,40%** (chặt) · 27,53% (nới) |
| bảy bất biến của tập cặp | **7/7 ĐẠT** |
| mẫu `s2.json` lệch khai báo | **0** |
| lệch độ dài chosen − rejected | trung vị **+0** ký tự · trung bình −1,10 |
| luật shortcut "chọn vế dài hơn" đoán đúng | **43,2%** (ngưỡng 55%) |

⭐ **Lý do chọn tầng khai báo thay vì tầng câu đã được ghi trong `report/116` Mục 12.2:** tầng câu
chỉ đạt **26,40%**, sát cổng 25% và đó mới là **cận trên** (chưa trừ audit bằng chứng OCR/a11y,
parent/child, action-compatible). Tầng khai báo đạt **55,61%** và không cần điều kiện ngặt nhất
của tầng câu — *"tên phải xuất hiện literal trong câu người"*, chỗ làm rơi 78,0% → 42,3%.

### (x5) Estimand và ngưỡng — KHOÁ

```
Δ_component = mean_2seed(MIN-DESC − CE2-S2)      ← primary, quy công cho mục tiêu huấn luyện
Δ_system    = mean_2seed(MIN-DESC − S1)          ← secondary, model cuối so hệ mạnh nhất hiện có
Δ_vs_S2     = mean_2seed(MIN-DESC − S2/101)      ← mô tả, KHÔNG dùng quy công (S2 chỉ một hạt giống)
```

Thước không đổi: `UGround Executability@Voronoi = action_ok AND toggle_ok AND hit_voronoi`, đủ
**4.463** bước, câu rỗng tính `exec = 0`, `metric_exec.py` **không sửa**.

Dải đọc **giữ nguyên** dải đã khoá ở mục (w), không phát minh dải mới:

| Δ trung bình hai hạt giống | cách đọc |
|---|---|
| ≥ +2,8 pp và KTC95 loại 0 | Dương |
| +1,7 … +2,8 pp và KTC95 loại 0 | Dương yếu |
| −2,8 … +1,7 pp, hoặc KTC phủ 0 | **Trắng, không kết luận được** |
| ≤ −2,8 pp và KTC95 loại 0 | Âm |

**Được claim "thành phần huấn luyện này làm model tốt hơn" khi và chỉ khi CẢ BỐN:**
1. `Δ_component ≥ +1,7 pp`, KTC95 bootstrap cụm loại 0;
2. `Δ_system ≥ +1,7 pp`, KTC95 loại 0;
3. hiệu của **cả hai** hạt giống, cho **cả hai** estimand, đều dương;
4. không có no-harm failure trên bước **không-chạm**: cận dưới `> −3 pp`, chạy với `strict_back=True`.

Chỉ đạt (1) mà không đạt (2) ⇒ mục tiêu có hiệu ứng so với CE nhưng chưa tạo model cuối tốt hơn S1.
Chỉ đạt (2) mà không đạt (1) ⇒ **không được quy công cho MIN-DESC**, vì chặng train thêm có thể là
nguyên nhân.

### (x6) Cổng STOP — khoá trước, không nới sau khi thấy số

- eligibility trên tập cặp cuối `< 25%`;
- audit mù 300 cặp cho false-negative `≥ 5%`;
- probe text-only hoặc shuffled-image đạt preference accuracy `> 55%` một cách rõ ràng;
- wrong-referent counterfactual trên câu người **không** làm executability giảm ít nhất **10 pp**
  trên lát đủ điều kiện với KTC ghép cặp loại 0 (đây là validity gate của thước, **không** dùng để
  chọn model);
- smoke ORPO trên 200 cặp dài nhất bị OOM/NaN, hoặc resume/save-load sai;
- sau seed 101: MIN-DESC **không** học margin tốt hơn CE2-S2 trên held-out, hoặc action/toggle tụt
  quá **3 pp** ⇒ dừng, không chạy seed 202.

⛔ **Cấm dùng UGround hoặc UI-Venus** để chọn β, chọn checkpoint, chọn negative, rerank, sửa câu,
hay làm điều kiện chạy hạt giống thứ hai. Cổng sau seed 101 chỉ được dùng tín hiệu **không cần bộ
trỏ**: CE/log-odds loss, preference accuracy, độ chính xác ô `name`/`point` của khai báo so với
nhãn vàng, parser action/toggle.

### (x7) Ba chỗ lệch so với `report/116` Mục 12, khai trước

1. **Cặp ở tầng khai báo, không phải tầng câu.** Lý do: số ở (x4).
2. **Không trộn bước không-chạm vào stage-2** (Mục 12.5 của `report/116` yêu cầu trộn). Lý do:
   stage `dpo`/`ranking` của LLaMA-Factory không nhận lẫn dữ liệu không-cặp một cách sạch sẽ.
   Giảm nhẹ: **MIN-DESC và CE2-S2 bỏ y hệt nhau**, nên chênh lệch giữa hai nhánh không thể do khác
   dữ liệu; và phép kiểm no-harm trên bước không-chạm ở điều kiện (4) của (x5) là **bắt buộc**,
   chính nó bắt được trôi action prior nếu có.
3. **Điều kiện độ dài ≤2 token không áp.** Lý do: đo ra cặp **tự nhiên cân độ dài** — trung vị
   lệch 0, luật "chọn vế dài hơn" chỉ đoán đúng 43,2%. Nếu probe shortcut ở cổng STOP vẫn báo
   vượt 55%, phương án dự phòng **đã khoá sẵn**: siết `|Δ ký tự| ≤ 8`, còn **15.421 cặp = 37,52%**,
   vẫn trên cổng 25%. Không được chọn giữa hai bản sau khi nhìn điểm test.

### (x8) Không đụng

Thước, luật chấm, `metric_exec.py`, tập kiểm, mẫu số 4.463, dải quyết định, hạt giống 101/202,
cấu hình QLoRA P9, và toàn bộ kết quả S1/base/trần/sàn/phép B đã công bố.

### (x3b) Bổ sung 23/8, **vẫn trước mọi lượt train**: learning rate của stage-2 và cổng cơ học

**LR hạ xuống `2.0e-5`** cho **cả hai** nhánh MIN-DESC và CE2-S2, thay vì thừa hưởng `1.0e-4`
của lượt SFT gốc. Lý do: đây là lượt **nối tiếp một adapter đã hội tụ**; khởi động lại ở LR đầy
đủ với một chu kỳ cosine mới là *re-train* chứ không phải *tinh chỉnh*, và rủi ro là **cả hai
nhánh cùng trôi khỏi S2** rồi so nhau trong vùng đã hỏng.

⚠️ **Đây là phán đoán thiết kế, không phải số đo.** Khai thẳng vì không có dữ liệu nào trong dự
án nói LR nào đúng cho ORPO nối tiếp. Hai điều làm nó an toàn: (a) hai nhánh dùng **chung** con
số, nên dù chọn sai thì `Δ_component` vẫn là phép so công bằng; (b) cổng cơ học dưới đây đo trực
tiếp xem lượt train có làm hỏng khả năng nhận diện không.

**Cổng cơ học, không gọi bộ trỏ** — `harness/gate_desc_acc.py`. Nó đối chiếu ô `<desc>` model tự
sinh với nhãn vàng `test_ac/descriptors.jsonl`: ô TÊN khớp, ô POINT trong dung sai ±14% cạnh
(cùng dung sai với `metric_exec.hit_disk`), và **cả hai cùng đúng**.

**Mốc S2/101, đo 23/8 TRƯỚC khi train MIN-DESC**, trên 3.473 bước có tên vàng:

| | sinh `<desc>` | tên đúng | point đúng | **cả hai đúng** |
|---|---|---|---|---|
| S2/101 | 93,4% | 59,2% | 66,9% | **53,9%** |

**Luật đọc cổng, khoá trước:**
- `Δ(cả hai đúng)` của MIN-DESC/101 so với S2/101 **dương** ⇒ được chạy hạt giống 202;
- **âm** ⇒ lượt train làm hỏng khả năng nhận diện (nghi LR quá cao) ⇒ **dừng, không chạy 202**,
  ghi lại và báo.

⛔ Cổng này **không phải** executability và **không thay thế** nó. Chấm 4.463 vẫn làm **một lần**,
sau khi cả bốn checkpoint đóng băng.

### (x3c) Kết quả smoke 23/8 — ghi lại trước khi train

| phép | kết quả |
|---|---|
| ORPO chạy thật | ✅ log có `rewards/accuracies`, `rewards/margins`, `sft_loss`, `odds_ratio_loss` |
| adapter S2 nạp thật | ✅ `Loaded adapter(s): …/ckpt/s2_seed101` · `trainable params 14.966.784 (0,397%)` |
| **không** tạo reference model | ✅ không có dòng nào về ref model — đúng đặc tính ORPO |
| chạy tiếp sau khi mất máy | ✅ `Fast-forwarding the dataloader … to resume from the exact training state`; `global_step` 12 → **20**; điểm lưu có `optimizer.pt` · `scheduler.pt` · `rng_state.pth` |
| OOM / NaN | ✅ không |
| **cỡ lô GPU 2** (× tích luỹ 8, hiệu dụng vẫn 16) | chạy được nhưng chỉ **nhanh hơn 2%** (413,1 s vs 422,9 s) và tốn **thêm 2% FLOPs** vì đệm ⇒ **giữ cỡ lô 1** |
| tốc độ trên **200 cặp nặng nhất** | **~21 s/bước** ⇒ 800 bước ≈ **4,7 giờ** (cận trên; tập thật nhẹ hơn) |
| ⚠️ liger ở stage `dpo` | log **không in dòng nào** về liger ⇒ nhiều khả năng bị bỏ qua ở đường pairwise. Không cản trở gì, nhưng **cấm** viết "dùng liger" cho MIN-DESC |
| ⭐ **phiên bản đã PIN** (yêu cầu của (x6)) | LLaMA-Factory `c4e09c7cbe18844816af9e18a97fe465515edbcd` · `transformers 5.8.0` · Python 3.13 · TRL `DPOTrainer` · card A100. **Cả bốn lượt phải dùng đúng SHA này** — LLaMA-Factory đổi hành vi giữa các bản (xem hàng dưới), nên lượt 1 và lượt 4 khác bản là hỏng phép so |
| ⚠️ **trường của `trainer_log.jsonl`** | chỉ còn **sáu**: `current_steps` · `total_steps` · `epoch` · `percentage` · `elapsed_time` · `remaining_time`. **Mất `loss` và `lr`** so với stack tháng 8 ⇒ ô theo dõi phải đọc **hai nguồn** (tiến độ từ jsonl, số học từ stdout `.log`) |
| ⚠️ LR lúc smoke | **1,0e-4** — máy ảo bung gói `thesis_rented.zip` **cũ**. Không ảnh hưởng kết luận cơ học của smoke, nhưng **phải upload gói mới trước lượt train thật** |

Chồng chất `rewards/margins` trong smoke cỡ lô 2 (20 bước, 200 cặp): **0,0109 → 0,0162 → 0,0190 →
0,0211**, `rewards/accuracies` **0,850 → 0,863 → 0,958 → 0,950**. Mục tiêu ưu tiên có tác dụng cơ
học; ⚠️ đây là 1,56 epoch trên 200 mẫu nên phần lớn là **thuộc lòng**, không đọc thành hiệu quả.

**Đo được ở smoke 23/8 — `rewards/accuracies` KHÔNG dùng làm cổng.** Nó đã ở **0,94–0,97 ngay từ
bước log đầu tiên**, không phải sau khi học. Lý do có tính cấu tạo: `chosen` chính là chuỗi mà
checkpoint S2 đã được dạy sinh ra suốt hai epoch, nên log-xác-suất của nó cao hơn `rejected` một
cách tất yếu, trước khi ORPO kịp làm gì. ⇒ Ngưỡng *"acc > 0,6"* dự định lúc đầu là **rỗng nghĩa**,
đã bỏ. Thay bằng: `rewards/margins` phải **tăng** so với mốc đầu (~0,019), và cổng chính vẫn là
`gate_desc_acc.py` so với mốc S2 **53,9%**. `acc` chỉ còn dùng để phát hiện **hỏng** (tụt dưới 0,8).

---

## Sửa đổi 23/8/2026 — (y) VÁ `mde_that.py`: hai lệch so với hồ sơ đã khoá

Phát hiện trong phiên debate 23/8, kiểm lại bằng mã và **đúng cả hai**. Cả hai đều lệch theo
hướng **làm số đẹp lên**, nên phải sửa dù ảnh hưởng nhỏ.

### (y1) Gom cụm theo BƯỚC thay vì theo TÁC VỤ

Sửa đổi (e) khoá luật *"mỗi **tác vụ** không-rõ-app là một cụm"* và ghi **G = 1.091**. Bài FAIR
đang trích đúng con số đó (`main.tex:411`: *"1,091 clusters (effective 454.3)"*). Nhưng
`mde_that.cum()` trả `__don__{episode}_{step}` — mỗi **bước** một cụm, cho **2.906 cụm**, nhiều
gấp 2,7 lần. Chia nhỏ cụm hơn hồ sơ cho phép làm SE nhỏ đi, tức **nới ngưỡng**.

⇒ Đã đổi fallback về `__don__{episode}`. Kiểm lại: **1.091 cụm**, khớp hồ sơ và khớp bài báo.

### (y2) Complete-case analysis trong `nap()`

Bản cũ: `if "bo_qua" not in o` — loại khỏi **cả tử số lẫn mẫu số** đúng những bước mà chính model
làm hỏng. Mục 1 của `report/116` và quy tắc mẫu số 4.463 đều cấm điều này.

⇒ Đã đổi: giữ mọi dòng, `o.setdefault("executable", 0)`. Số bước ghép cặp **4.461 → 4.463**.

### Ảnh hưởng thật — báo đúng, không thổi

| | trước | sau |
|---|---|---|
| số bước ghép cặp | 4.461 | **4.463** |
| số cụm | 2.906 | **1.091** |
| SE bootstrap cụm | 0,386 pp | **0,375 pp** (~3%) |
| MDE, 2 hạt giống | 1,67 pp | **1,66 pp** |
| MDE, thận trọng (dòng đã khoá) | 2,78 pp | **2,77 pp** |

⇒ Ngưỡng đổi **0,01 pp**. Dải quyết định đã khoá ở (w) là **+1,7 / +2,8** (số làm tròn), nên
**không dải nào đổi** và **không kết luận nào đổi**. Sửa vì đây là lệch hồ sơ đăng ký và lệch so
với chính bài báo, **không** vì nó cứu được con số nào.

⚠️ Ba con số của bài FAIR **không bị ảnh hưởng**: trần 75,7% và G = 454,3 tính bằng
`gate_a_ceiling.py` (vốn đã dùng luật tác vụ, nên bài báo luôn đúng); `mde_that.py` chỉ dùng để
khoá ngưỡng.

### (x3d) Đo 24/8 sau khi có hai checkpoint hạt giống 101 — trôi phân biệt chạm/không-chạm

Lát 1.200 bước đầu tập kiểm (800 chạm · 400 không-chạm), ba nhánh trên **cùng** quần thể:

| nhánh | sinh `<desc>` ở bước CHẠM | sinh `<desc>` ở bước KHÔNG-chạm |
|---|---|---|
| S2/101 | 724/800 = **90,5%** | 56/400 = **14,0%** |
| CE2-S2/101 | 799/800 = **99,9%** | 279/400 = **69,8%** |
| MIN-DESC/101 | 799/800 = **99,9%** | 273/400 = **68,2%** |

**Hai kết luận, cả hai đều quan trọng:**

1. ⭐ **Trôi không-chạm là do DỮ LIỆU, không do ORPO.** CE2 và MIN-DESC trùng nhau gần tuyệt đối
   (69,8% vs 68,2%), tức việc bỏ bước không-chạm khỏi stage-2 — lệch chuẩn đã khai ở **(x7) điểm
   2** — mới là nguyên nhân. ⇒ `Δ_component = MIN − CE2` **không bị ảnh hưởng**, hai nhánh trôi
   y hệt nhau. Thiết kế quy công còn nguyên.
2. ⭐ **Chặng stage-2 sửa gần hết lỗi 4j-18.** Nhóm "không sinh khai báo trên bước chạm" — nhóm
   chỉ đạt 10,8% executability và gánh −0,63 pp của S2 — teo từ 76/800 xuống **1/800**. Nhưng
   cũng là công của *train thêm trên dữ liệu chạm*, **không** của ORPO, vì cả hai nhánh bằng nhau.

⚠️ **Cái giá:** điều kiện claim **(x5) mục 4** (*no-harm trên bước không-chạm, cận dưới > −3 pp*)
nhiều khả năng **trượt ở cả hai nhánh**. Executability chỉ chấm trên 4.463 bước chạm nên điểm
chính không bị đụng, nhưng điều kiện đã khoá thì vẫn là điều kiện. Cách sửa đã biết:
trộn bước không-chạm dạng CE thuần vào stage-2, đúng như `report/116` Mục 12.5 yêu cầu ban đầu.
Nay đã có số đo cái giá của việc bỏ nó, thay vì chỉ có phán đoán.

### (x3e) 24/8 — ĐIỀU KIỆN (x5) MỤC 4 TRƯỢT: no-harm trên bước không-chạm mất ~20 pp

Thước đúng theo mục (v): `action_ok` = lớp thao tác của câu model khớp lớp thao tác của **câu
người**, chạy với **`strict_back=True`**. Lát 400 bước không-chạm trong 1.200 bước đầu tập kiểm
(scroll 96 · wait 86 · input_text 82 · open_app 81 · navigate_back 55):

| nhánh | action_ok | Δ so S2 |
|---|---|---|
| S2/101 | **83,5%** | — |
| CE2-S2/101 | 63,0% | **−20,50 pp** |
| MIN-DESC/101 | 63,8% | **−19,75 pp** |

Ngưỡng ở (x5) mục 4 là **cận dưới > −3 pp** ⇒ **TRƯỢT, cách ngưỡng gần bảy lần.**

**Phân rã MIN-DESC vs S2 theo loại thao tác:**

| thao tác | S2 | MIN-DESC | Δ |
|---|---|---|---|
| scroll | 82,3% | 38,5% | **−43,8** |
| navigate_back | 70,9% | 34,5% | **−36,4** |
| input_text | 78,0% | 48,8% | **−29,2** |
| wait | 88,4% | 94,2% | +5,8 |
| open_app | 93,8% | 96,3% | +2,5 |

**Cơ chế:** ba loại sụp là ba loại mà câu đúng **không nhắc tên phần tử nào**. Model nay gắn khai
báo về một nút rồi viết câu kiểu chạm theo sau. Hai loại không sụp chỉ vì `ACTION_MAP` quy `open`
về `tap`, nên câu kiểu chạm vô tình khớp — không phải vì model làm đúng.

**Quy trách nhiệm:** CE2 −20,50 và MIN-DESC −19,75 ⇒ hỏng như nhau, MIN-DESC còn nhỉnh hơn.
Nguyên nhân là **stage-2 chỉ có bước chạm** (lệch chuẩn đã khai ở **(x7) điểm 2**), **không phải
mục tiêu ORPO**. Cách sửa đã biết: trộn bước không-chạm dạng CE thuần, đúng như `report/116`
Mục 12.5 yêu cầu ban đầu.

⛔ **Hệ quả cho câu chữ:** executability chỉ chấm trên 4.463 bước **chạm**, nên điểm chính không
bị đụng. Nhưng **cấm** viết *"model cuối tốt hơn"* không kèm điều kiện. Câu được phép:
*"trên quần thể đã đăng ký (bước chạm), … ; đồng thời chúng tôi đo được mức tụt 20 pp ở lớp
thao tác trên bước không-chạm, do thiết kế dữ liệu stage-2, và báo cáo như một giới hạn."*

⚠️ Con số **45,5% → 23%** ghi trong phiên chat theo thước *"trùng nguyên văn câu chuẩn"* là thước
SAI và thổi phồng thiệt hại — nó phạt cả khi model nói đúng ý bằng chữ khác. Thước đúng của (v)
là `action_ok`. Không dùng lại con số trùng-nguyên-văn.

---

## Sửa đổi 24/8/2026 — (x8) CHUYỂN MIN-DESC/CE2 SANG NHÁNH THĂM DÒ MỘT HẠT GIỐNG

> **Viết TRƯỚC khi chấm 4.463.** Không có điểm executability nào của MIN-DESC hay CE2-S2 tồn tại
> vào lúc viết mục này. Kiểm được bằng `git log`.

### (x8a) Đổi cái gì

Mục **(x6)** khoá: *"Không chấm 4.463 sau seed 101"* và *"cấm dùng bộ trỏ làm điều kiện chạy hạt
giống thứ hai"*. Chủ luận văn quyết **chấm ngay hạt giống 101** để biết số thật trước khi cân nhắc
chi thêm ~8 giờ GPU cho hạt giống 202.

⇒ **MIN-DESC/101 và CE2-S2/101 chuyển sang nhãn THĂM DÒ, MỘT HẠT GIỐNG**, cùng hạng với S2/101.
Estimand `Δ_component` và `Δ_system` ở (x5) **chưa hoàn tất**.

### (x8b) Cái gì được phép nói sau khi có điểm

- ✅ *"Ở hạt giống duy nhất, checkpoint MIN-DESC/101 đạt X% executability trên 4.463 bước, so với
  S1 59,1/59,6% và S2/101 57,2%. Kết quả thăm dò, một hạt giống."*
- ⛔ **Cấm** *"MIN-DESC làm model tốt hơn"* · *"mục tiêu ưu tiên có tác dụng"* · *"Δ_component =
  …"* · mọi câu khẳng định về **phương pháp**, vì một hạt giống không tách được tác dụng khỏi
  biến thiên huấn luyện (sàn nhiễu đo trên S1 là ±0,52 pp).
- Cùng luật đã áp cho S2 ở **(x1)**. Không có ngoại lệ vì lần này số đẹp hơn.

### (x8c) Cam kết giữ cho phép chọn-sau-khi-thấy không phá kết quả

**Nếu sau khi thấy điểm hạt giống 101 mà quyết chạy hạt giống 202:**
1. chạy **cả hai** nhánh MIN-DESC/202 và CE2-S2/202, không chạy một nhánh;
2. **báo trung bình hai hạt giống bất kể nó ra sao** — kể cả khi hạt 202 kéo trung bình xuống dưới
   ngưỡng, kể cả khi nó lật dấu;
3. **khai thẳng trong bài** rằng hạt giống thứ hai được chạy **sau khi** đã thấy điểm hạt thứ nhất,
   và vì vậy `Δ` hai hạt giống mang một mức chọn-lọc-theo-kết-quả không loại bỏ được.

Cam kết (2) là thứ duy nhất giữ cho trung bình hai hạt giống còn đọc được. Vi phạm nó thì con số
mất giá trị hoàn toàn — nặng hơn cả việc dừng ở một hạt giống.

### (x8d) Không đụng

Thước, luật chấm, `metric_exec.py`, mẫu số 4.463, dải quyết định ở (w), cấu hình đã khoá ở (x3),
và mọi kết quả S1/base/trần/sàn/phép B đã công bố.

---

## Sửa đổi 25/8/2026 — (x9) CỔNG CƠ HỌC ĐÃ CHẠY: **ĐẠT** · và một lệch chuẩn phải khai

> Viết **sau** khi có kết quả cổng, **trước** khi chấm 4.463. Chưa có điểm executability nào
> của MIN-DESC hay CE2-S2 tồn tại vào lúc viết mục này.

### (x9a) Kết quả cổng — phán quyết ĐẠT

Cổng khoá ở **(x3b)**: `gate_desc_acc.py`, đo độ chính xác ô khai báo, **không gọi bộ trỏ**,
mốc S2/101 = **53,9%**. Chạy ngày 25/8 trên máy nhà, 0 đồng, 0 giây GPU:

```
GIAO của 3 tệp preds: 3.473 bước có tên vàng · dung sai ô point ±14% cạnh

tệp preds                        n   sinh desc   tên đúng   point đúng   CẢ HAI
preds_s2_seed101              3473      93,4%      59,2%        66,9%     53,9%
preds_ce2_s2_seed101          3473      99,6%      66,2%        71,2%     59,8%
preds_min_desc_seed101        3473      99,6%      67,0%        71,8%     60,6%
```

**Δ 'cả hai đúng' (MIN-DESC − S2) = +6,77 pp ⇒ cổng ĐẠT.** Điều kiện ở (x3b) là Δ dương so mốc
53,9%; không nới, không đổi thước, không đổi quần thể.

⭐ **Mốc S2 tái lập tới chữ số thập phân:** 53,9% đo lại ngày 25/8 trùng đúng con số ghi ngày
23/8 ở (x3b). Thước không trôi giữa hai lần chạy ⇒ phép so đọc được.

⚠️ **Đọc đúng cách quy công, đừng đọc con số +6,77:**

| phép so | Δ | thuộc về |
|---|---|---|
| CE2-S2 − S2 | **+5,90 pp** | *train thêm stage-2 trên bước chạm* — SFT thuần, không phải ORPO |
| MIN-DESC − CE2-S2 | **+0,80 pp** | phần riêng của **mục tiêu ưu tiên** — đây mới là thứ bài báo đặt cược |
| MIN-DESC − S2 | +6,77 pp | tổng hai phần trên, **không** được trình như công của ORPO |

⇒ 87% mức tăng đến từ nhánh đối chứng. Đúng mẫu hình đã thấy ở **(x3d)**: hai nhánh dịch chuyển
gần như song song, thứ tách chúng ra chỉ còn dưới một điểm phần trăm. Trên **một hạt giống**, và
sàn nhiễu giữa hạt giống đo trên S1 là **±0,52 pp** — cùng bậc độ lớn với chính +0,80.

⛔ **Cổng ĐẠT chỉ chứng minh lượt train KHÔNG làm hỏng khả năng nhận diện phần tử.** Nó không
chứng minh mục tiêu ưu tiên có tác dụng, và **không thay thế** executability. Luật câu chữ ở
**(x8b)** giữ nguyên, không có ngoại lệ vì lần này số dương.

### (x9b) Lệch chuẩn phải khai: tệp preds CE2 sinh bằng **hai môi trường**

Máy ảo Colab bị thu hồi lúc lượt suy luận CE2 chạy được **3.616/6.958 bước** (24/8, ~23:20).
Dựng lại máy rồi chạy tiếp bằng cơ chế nối tiếp của `infer_branch.py`. Hệ quả: một tệp preds
duy nhất được sinh bởi hai môi trường khác nhau.

| | 3.616 bước đầu | 3.342 bước sau |
|---|---|---|
| card | A100-SXM4-40GB | A100-SXM4-40GB |
| kiểu số (`pick_dtype`) | bf16 | bf16 |
| `peft` | bản LLaMA-Factory ghim (cài kèm ô T1) | bản mới nhất trên PyPI |
| `torchao` | có sẵn, không đụng | **đã gỡ** (peft mới `raise ImportError` với torchao < 0,16) |

**Vì sao vẫn dùng được:** phép áp LoRA là phép cộng ma trận tất định, cùng card và cùng bf16 nên
không có nguồn ngẫu nhiên nào; sinh câu chạy greedy. **Vì sao vẫn phải khai:** không ai đo lại
hai môi trường trên cùng một lát để chứng minh chúng trùng, nên đây là *lập luận*, không phải
*phép đo*. Nhánh MIN-DESC **không** dính — nó sinh trọn trong một môi trường.

**Kiểm đã chạy trên tệp ghép** (`runs/preds_ce2_s2_seed101.jsonl`): 6.958 bản ghi · **0 khoá
trùng** · phủ đủ 4.463 bước chạm · **một chữ ký duy nhất** `lora:ce2_s2_seed101` · 0 câu rỗng ·
0 câu sót `<desc>` · ranh giới bước 3.616 liền mạch. So với nhánh MIN-DESC: `pred` trùng 82,4%,
`raw` trùng 65,1% ⇒ hai tệp là hai lượt sinh khác nhau thật, không phải chép nhầm adapter.

### (x9c) Không đụng

Thước, luật chấm, `metric_exec.py`, mẫu số 4.463, mốc S2 53,9%, dải quyết định ở (w), luật câu
chữ ở (x8b), cam kết hạt giống thứ hai ở (x8c).

---

## Sửa đổi 25/8/2026 — (x10) ĐIỂM EXECUTABILITY CỦA MIN-DESC/101 + chẩn đoán chỗ nghẽn

### (x10a) Số chính

`runs/score_min_desc_seed101.json`, UGround, 4.463 bước chạm, cùng mẫu số mọi nhánh:

**MIN-DESC/101 = 60,05%**, KTC95 **[58,33 · 61,77]**, `exec_disk` 69,19%, `clusters` 1.091,
`g_eff` 454,33.

| phép so ghép cặp | Δ | KTC95 cụm | b | c | χ² | p |
|---|---|---|---|---|---|---|
| MIN − S2/101 | **+2,87** | [+2,03 · +3,76] | 258 | 130 | 41,6 | 1,1e-10 |
| **MIN − S1/101** | **+0,94** | **[−0,09 · +2,05]** | 342 | 300 | 2,6 | **0,11** |
| MIN − Base | +12,46 | [+11,03 · +14,00] | 827 | 271 | 280,5 | 5,7e-63 |
| S1 − S2 *(tự kiểm)* | +1,93 | [+0,82 · +3,00] | 340 | 254 | 12,2 | 0,00049 |

Hàng cuối tái lập **đúng** −1,93 pp của S2−S1 đã công bố, b/c trùng 340/254 ⇒ đường phân tích
không trôi.

**Đọc theo luật đã khoá:** Δ so S1 nằm **dưới MDE 2,2 pp** và KTC chứa 0 ⇒ theo bảng bốn kết cục
ở mục (w), đây là ô **TRẮNG** đối với phép so MIN-vs-S1. Ô `hit_voronoi` thuần nói cùng một
chuyện bằng cách trực tiếp hơn: **MIN 60,4 · S1 60,2** — khả năng trỏ đúng phần tử **ngang** SFT
trơn. Cái tăng so với S2 nằm ở `action_ok` (98,9 vs 94,9) và ở việc dẹp nhóm không-sinh-khai-báo
(324 bước → **17 bước**) — tức **sửa thiệt hại do chính S2 gây ra**, không phải năng lực mới.

⚠️ `action_ok` 98,9% trên bước chạm **phải** đọc kèm **(x3e)**: cùng lúc đó `action_ok` trên bước
KHÔNG-chạm tụt −19,75 pp. Hai con số là **một hiện tượng** — mô hình co về *"mọi thứ đều là chạm"*.
Quần thể đăng ký trước chỉ có bước chạm nên thước không nhìn thấy phần thiệt. **Cấm** nêu 98,9%
mà không kèm (x3e).

⚠️ `Δ_component = MIN − CE2` **chưa tính được** — CE2 chưa có điểm (xem x10c).

### (x10b) 🔬 THĂM DÒ, HẬU KIỂM, KHÔNG ĐĂNG KÝ TRƯỚC — chỗ nghẽn nằm ở đâu

Chia 3.473 bước có tên vàng theo việc ô khai báo của **chính MIN-DESC** có đúng không
(đúng = tên khớp **và** point trong ±14% cạnh, cùng luật với `gate_desc_acc.py`):

| nhóm | n | MIN exec | S1 exec | Δ (ghép cặp) | trần nhóm |
|---|---|---|---|---|---|
| MIN tả **ĐÚNG** phần tử | 2.106 (60,6%) | **87,1%** | 78,3% | **+8,83** | 86,3% |
| MIN tả **SAI** phần tử | 1.367 (39,4%) | **21,8%** | 32,9% | **−11,12** | 61,4% |

⭐ **Cơ chế KHÔNG hỏng — nó bị chặn bởi độ chính xác ô khai báo.** Khi mô tả đúng phần tử,
MIN-DESC hơn SFT trơn **+8,83 pp** trên cùng những bước ấy, và **vượt cả trần câu người của nhóm
đó** (87,1 vs 86,3). Khi mô tả sai, nó **thua SFT trơn 11,12 pp**: mô hình chốt vào một phần tử
sai rồi viết câu tự tin về phần tử đó, trong khi S1 viết câu chung chung nên còn cơ may.
Hai chiều gần như triệt tiêu nhau ⇒ tổng +0,94 pp không ý nghĩa.

**Số học của chỗ nghẽn:** chuyển một bước từ nhóm dưới lên nhóm trên đáng ~65 pp cho bước đó.
Giữ nguyên +8,83 mà **triệt tiêu** được −11,12 thì Δ so S1 thành ~**+5,4 pp** — trên MDE 2,2 gấp
2,4 lần. Nâng độ chính xác khai báo từ 60,6% lên 70% đáng thêm ~+6 pp.

· Câu sinh ra có nhắc tên vàng: MIN **45,1%** vs S1 **44,6%** — gần như nhau. Nhưng **riêng** nhóm
  tả đúng, MIN nhắc lại tên trong câu **64,0%** ⇒ còn 36% số ca *biết đúng mà không dùng*.

⚠️ **Giới hạn phải khai:** biến chia nhóm là **hành vi của chính MIN-DESC**, không phải lát cắt
ngẫu nhiên — hai nhóm khác hẳn nhau về độ khó (trần 86,3% vs 61,4%). Phép so **MIN vs S1 bên
trong mỗi nhóm** vẫn hợp lệ vì ghép cặp trên **cùng bước**, nhưng **cấm** so nhóm trên với nhóm
dưới. Cùng loại giới hạn đã khai cho nhóm 325 ở chẩn đoán 4j-18.

### (x10c) Sự cố vận hành: 5,3 giờ quota chấm nhầm nhánh

Hai commit Kaggle chạy song song ngày 25/8 **đều chấm `min_desc`**. Notebook thứ hai (dành cho
CE2) còn dòng `TEN_COMMIT = ["min_desc_seed101"]` **bên trong ô 2**, gán đè giá trị mà Ô 1 đặt;
ô 1b chạy trước nên in ra `ce2` — đúng — rồi bị đè. Không lỗi, không cảnh báo.
Phát hiện lúc giải nén: hai tệp thô **trùng nhau từng byte**.
Đã vá: ô 1b niêm phong `NHANH_CHOT`, ô 2 `assert` so với nó và in `▶ CHẤM NHÁNH:` ngay dòng đầu.

⭐ **Lợi ngoài ý muốn — bằng chứng TẤT ĐỊNH mạnh hơn hẳn bản cũ:** hai lượt chấm độc lập, hai
phiên Kaggle khác nhau, khác giờ, cho tệp thô **trùng từng byte** (`md5 7ab8197edebb…`) trên
**toàn bộ 4.463 bước**. Bản công bố cũ chỉ có *0 bất đồng trên 1.625 phép so qua bốn lượt*.
Con số mới dùng được cho chương đo lường.

---

## Sửa đổi 25/8/2026 — (x11) ĐĂNG KÝ BIẾN THỂ **MIN-ONPOLICY**: đổi NGUỒN vế âm

> **Viết TRƯỚC khi sinh một khai báo nào.** Chưa có checkpoint, chưa có dữ liệu, chưa có số.
> Kiểm được bằng `git log`. Đây là biến thể **thứ tư**, chọn **hậu kiểm** sau khi thấy điểm
> MIN-DESC ⇒ mang nhãn **thăm dò**, và luật câu chữ (x8b) áp nguyên.

### (x11a) Đổi đúng MỘT thứ

| | MIN-DESC (đã chạy) | **MIN-ONPOLICY** (đăng ký ở đây) |
|---|---|---|
| `chosen` | `<desc>` vàng + "\n" + câu | **y hệt** |
| `rejected` | `<desc>` từ `nearest_other()` + "\n" + **câu y hệt** | `<desc>` **đúc lại từ phần tử mà S2 tự chọn nhầm** + "\n" + **câu y hệt** |
| mọi thứ khác | `train_config_orpo.yaml` | **không đổi một khoá nào** — cùng 800 bước, cùng `pref_beta 0.1`, cùng LR, cùng adapter nền S2 |
| đối chứng | CE2-S2 | **CE2-ONPOLICY** — SFT thuần trên đúng vế `chosen` của **đúng những bước ấy** |

**Lý do đo được, không phải cảm tính:** trong số bước S2 sai tên, chỉ **7,4%** rơi đúng vào hàng
xóm cùng vai trò gần nhất mà `nearest_other()` chọn (CE2 10,4% · MIN-DESC 9,8%). Heuristic bỏ sót
~90% khối lỗi thật. Nói theo Song et al. (**NeurIPS 2024**): dữ liệu off-policy hiện tại **không
phủ toàn cục** không gian lỗi, mà đó là điều kiện *cần* để một mục tiêu tương phản offline hội tụ
về đúng đích.

### (x11b) ⛔ BẢN NGÂY THƠ BỊ CẤM — đã có người đo và ra số ÂM

**KHÔNG được lấy chuỗi thô S2 sinh ra làm `rejected`.** D'Oosterlinck et al., **TACL Vol. 13
(2025)**, tr. 442–460, dựng bốn tập cặp trên cùng prompt/cùng mô hình, chỉ khác cách ghép. Tập
**Stronger Preferred** (`rejected` = mô hình đích tự sinh, `chosen` = nguồn khác mạnh hơn) — **đúng
cấu trúc ngây thơ của biến thể này** — là tập **duy nhất** cho số âm sâu: MaxΔ **−5,00**, MeanΔ
**−6,94**, dù vế thắng khách quan là chất lượng cao nhất. Nguyên nhân họ nêu: hai vế khác nhau ở
quá nhiều trục ngoài trục cần học ⇒ mô hình học **đặc trưng nguồn** thay vì nội dung.
Cùng chiều: NAT (**NAACL 2025**) đổi nguồn negative sang một mô hình 7B đã fine-tune: **+8,74 → −3,16**.

⇒ **Bắt buộc ĐÚC LẠI:** chỉ lấy ra *phần tử nào* S2 chọn nhầm, ánh xạ về node đó trong cây trợ
năng, rồi dựng lại `<desc>` bằng **chính `descriptor_label_build.desc_str()`** đã dựng nhãn vàng.
Negative thành **on-policy về nội dung lỗi, off-policy về hình thức** — giữ tương phản tối thiểu
mà không để lọt chênh lệch định dạng/độ dài/kiểu viết toạ độ giữa hai vế.

### (x11c) Ba cổng phải ĐẠT trước khi tiêu một giờ train

| cổng | ngưỡng | vì sao |
|---|---|---|
| **① lối tắt văn phong** — mô hình chỉ-văn-bản có tách được `chosen`/`rejected` không | luật "vế ngắn hơn" đoán đúng **< 55%** (cùng ngưỡng x6) · **0%** cặp tách được bằng một chuỗi ký tự cố định | phép chẩn đoán của mDPO (**EMNLP 2024**). Cặp MIN-DESC tự động qua vì hai vế chỉ khác ô `<desc>`; cặp on-policy **KHÔNG** tự động qua vì khác nguồn |
| **② false negative** | phần tử S2 chọn nhầm phải cách gold **80–350 px**, cùng dải `hop_le()` đang dùng | dưới ngưỡng gộp 63 px của `dedupe_buttons` thì Voronoi vẫn chấm **trúng** ⇒ giữ lại là dạy mô hình **ghét đáp án đúng**. Chuyển vị *denoised hard negatives* của RocketQA (**NAACL 2021**) |
| **③ eligibility** | ≥ **25%**, cùng ngưỡng (x6) | `do_eligibility.py` |

Trượt bất kỳ cổng nào ⇒ **dừng, không train**, ghi lại lý do. Không nới ngưỡng sau khi thấy số —
dự án đã tự khai hai lần nới, không có lần thứ ba.

### (x11d) Đại lượng báo cáo và cam kết trước khi thấy số

- **Đại lượng chính của biến thể này là ở TẦNG KHAI BÁO**, không phải executability:
  `Δ_desc = gate_desc_acc(MIN-ONPOLICY) − gate_desc_acc(CE2-ONPOLICY)`, đo bằng
  `harness/gate_desc_acc.py`, **không gọi bộ trỏ** ⇒ (x6) cho phép.
  Lý do chọn tầng khai báo: hệ số chuyển đổi khai-báo→exec đo được là **0,43** (x10), nên tín hiệu
  ở tầng exec đã bị bóp hơn một nửa trước khi ta kịp nhìn.
- **Chỉ chấm executability nếu `Δ_desc` ≥ +2,0 pp** so với MIN-DESC hiện tại ở cùng cổng. Ngưỡng
  này khoá **ở đây, trước khi có số**.
- **Cam kết báo cả hai chiều:** dù `Δ_desc` âm, dương hay trắng, kết quả vào bài dưới dạng một
  **ablation về NGUỒN vế âm** với ba nhánh cạnh nhau (heuristic · on-policy · CE2). Không giấu
  nhánh nào. Cùng tinh thần cam kết (x8c).

### (x11e) Kỳ vọng — khai trước để sau này không tự lừa

Ba nguồn độc lập cùng dự báo hiệu ứng **nhỏ**: Tajwar et al. (**ICML 2024**) — on-policy có lợi
*khi đỉnh phần thưởng nằm xa* mô hình nền, mà `chosen` của ta là nhãn vàng và S2 đã được SFT trên
đúng khuôn đó ⇒ đỉnh nằm **gần**; Chen et al. (**NeurIPS 2024**) — mục tiêu DPO *"ill-suited to
fix even mild ranking errors in the reference model"*, mà S2 đã đúng ô khai báo 53,9%; và hệ số
chuyển đổi **0,43**. ⇒ Xác suất vượt MDE 2,2 pp ở tầng executability, ước trước khi chạy: **thấp**.
Biến thể này chạy vì nó là **ablation sạch về nguồn cặp**, không vì kỳ vọng thắng.

### (x11f) Chữ CẤM dùng

Đây là **hard-negative mining động**, có chủ từ **OHEM (CVPR 2016)** và **ANCE (ICLR 2021)**;
trong miền GUI, **WEPO (AAAI 2025)** đã dùng DPO với vế rejected là một phần tử web khác trên cùng
trang, và **LPO (Findings of ACL 2026, tr. 14617–14628)** đã dùng mẫu do chính mô hình sinh làm
negative ở tầng toạ độ. ⛔ **Cấm "đầu tiên"/"mới"/"cơ chế mới".** Cách viết đúng: *"chúng tôi áp
lại hard-negative mining động vào tầng khai báo phần tử"*, điểm phân định là **tầng đặt cặp**.

### (x11g) Không đụng

Thước, luật chấm, `metric_exec.py`, mẫu số 4.463, mốc S2 53,9%, cấu hình đã khoá ở (x3), luật câu
chữ (x8b), cam kết (x8c). Mọi kết quả S1/base/trần/sàn/phép B/MIN-DESC đã công bố.

---

## Sửa đổi 25/8/2026 — (x12) ĐIỂM CE2-S2/101 · **`Δ_component` = +0,63 pp**

### (x12a) Số

`runs/score_ce2_s2_seed101.json` — UGround, 4.463 bước chạm, cùng bản `metric_exec.py`
(`9bf0b84145458fd5…`), trường `preds` xác nhận đúng `preds_ce2_s2_seed101.jsonl`.

**CE2-S2/101 = 59,42%**, KTC95 **[57,69 · 61,14]**, `exec_disk` 68,92%.

| nhánh | exec | action_ok | `hit_voronoi` thuần |
|---|---|---|---|
| Câu người (trần) | 75,73% | 100,0 | 75,8 |
| **MIN-DESC/101** | **60,05%** | 98,9 | **60,4** |
| **CE2-S2/101** | **59,42%** | 98,9 | 59,8 |
| S1/101 | 59,11% | 94,4 | 60,2 |
| S2/101 | 57,18% | 94,9 | 58,1 |
| Base | 47,59% | 96,5 | 48,9 |

### (x12b) Bảng ghép cặp trên đúng 4.463 bước — GIAO sáu nhánh

| phép so | Δ pp | KTC95 cụm | b | c | χ² | p |
|---|---|---|---|---|---|---|
| ⭐ **MIN − CE2 = `Δ_component`** | **+0,63** | **[+0,16 · +1,10]** | 70 | 42 | 6,5 | **0,011** |
| CE2 − S2 | +2,24 | [+1,41 · +3,11] | 227 | 127 | 27,7 | 1,4e-07 |
| MIN − S2 | +2,87 | [+2,03 · +3,76] | 258 | 130 | 41,6 | 1,1e-10 |
| CE2 − S1 | +0,31 | [−0,76 · +1,45] | 326 | 312 | 0,3 | 0,61 |
| MIN − S1 | +0,94 | [−0,09 · +2,05] | 342 | 300 | 2,6 | 0,11 |

### (x12c) ĐỌC — chỗ này dễ đọc sai theo cả hai chiều

⚠️ **`Δ_component` = +0,63 pp có ý nghĩa thống kê (p=0,011, KTC không chứa 0) NHƯNG vẫn KHÔNG
kết luận được về phương pháp.** Hai loại nhiễu khác nhau:

| nhiễu | đo bằng | giá trị |
|---|---|---|
| (a) nhiễu **thước** trên một cặp checkpoint | bootstrap cụm ghép cặp — chính KTC ở trên | SE **0,38 pp** |
| (b) nhiễu **giữa hạt giống huấn luyện** | cặp S1/101 vs S1/202, mục (w) | σ ≈ **0,46 pp** |

KTC [+0,16 · +1,10] chỉ tính (a). MDE **2,11 pp** cho thiết kế **một hạt giống** (mục w) tính cả
hai. **+0,63 pp chỉ bằng 1,4× σ giữa hạt giống** ⇒ *phân biệt được với nhiễu ĐO, không phân biệt
được với nhiễu HUẤN LUYỆN*. Đây đúng là lý do (w) đòi hai hạt giống.

⇒ **Phán quyết: dưới MDE ⇒ ô TRẮNG cho estimand `Δ_component`.** Luật câu chữ (x8b) áp nguyên.

**✅ Được viết:** *"Ở hạt giống duy nhất, mục tiêu ưu tiên ở tầng khai báo đóng góp +0,63 pp
executability so với đối chứng SFT cùng bước (KTC95 [+0,16 · +1,10] trên nhiễu đo), dưới MDE
2,11 pp của thiết kế một hạt giống. Kết quả thăm dò."*

**⛔ Cấm:** *"mục tiêu ưu tiên CÓ tác dụng"* · *"ORPO cải thiện mô hình"* · trích p=0,011 mà
không kèm câu MDE 2,11 và σ giữa hạt giống 0,46.

### (x12d) ⭐ Quy công đã hoàn tất — đây là kết quả đáng giá nhất của mục này

Toàn bộ chặng stage-2 từ S2, tách được thành hai phần **đo được**:

| chặng | Δ so bước trước | thuộc về |
|---|---|---|
| S2 → CE2-S2 | **+2,24 pp** (p=1,4e-07) | *train thêm 800 update SFT trên bước chạm* — **không** phải ORPO |
| CE2-S2 → MIN-DESC | **+0,63 pp** (p=0,011) | **phần riêng của mục tiêu ưu tiên** |
| **tổng S2 → MIN-DESC** | **+2,87 pp** | — |

⇒ **78% mức tăng thuộc nhánh đối chứng, 22% thuộc ORPO.** Ở tầng khai báo tỉ lệ là 88/12
(+5,90 vs +0,80). ⛔ **Cấm trình +2,87 pp như công của MIN-DESC.**

⇒ Và cả ba nhánh cộng lại **vẫn không vượt SFT trơn**: CE2 − S1 = +0,31 (p=0,61) ·
MIN − S1 = +0,94 (p=0,11). Chặng S2 đào hố −1,93; CE2 lấp lại; MIN nhô thêm 0,63.

### (x12e) Hệ số chuyển đổi khai-báo → exec, đo trên hai cặp

| cặp | Δ khai báo | Δ exec | hệ số |
|---|---|---|---|
| MIN − S2 | +6,70 | +2,87 | **0,43** |
| MIN − CE2 | +0,80 | +0,63 | **0,79** |

Hai điểm, hai giá trị khác nhau, đều nằm trong dải văn liệu 0,3–1,0 (Dong & Lapata **ACL 2018**
27–62% · Wang et al. **ACL 2023** ~97%). ⚠️ Mỗi con số là **một quan sát**, không phải ước lượng
có sai số — cấm trình như hằng số của pipeline. Dự báo viết trước ở (x11e) là **+0,35 pp**; thực
tế **+0,63** ⇒ mô hình dự báo đúng bậc độ lớn, hơi bảo thủ.

### (x12f) Không đụng

Thước, luật chấm, mẫu số 4.463, MDE 2,11/1,67 của (w), luật câu chữ (x8b), cam kết (x8c), hồ sơ
biến thể MIN-ONPOLICY ở (x11).

---

## (x13) KẾT QUẢ MIN-ONPOLICY — ⛔ TRƯỢT CỔNG ③, DỪNG THEO ĐÚNG HỒ SƠ (x11c)

Ngày 25/8/2026. Hồ sơ đăng ký ở (x11) đóng lại tại đây bằng một **kết quả âm về tính khả thi**,
không phải bằng một số điểm. Chi phí: **~4,5 giờ A100** (ô O1), **0 giờ Kaggle**.

### (x13a) Số thô

Ô O1 sinh khai báo của chính S2 trên **14.000** màn tập dạy. Ô O2 dựng cặp cho ra **459 cặp**.

| lý do bỏ | n |
|---|---|
| `thieu_du_lieu` (ngoài lát 14.000 đã sinh) | 50.567 |
| `s2_da_dung_ten` — S2 gọi ĐÚNG tên, không có vế âm | 7.067 |
| `gold_khong_ten` | 2.889 |
| **`ngoai_dai_80_350`** — cổng khoảng cách của (x11c)② | **2.482** |
| `thieu_khai_bao` | 792 |
| `node_chong_lan_gold` | 169 |
| `node_khong_dat_ten_duoc` | 131 |
| `thieu_point` · `duc_lai_trung_gold` | 6 · 5 |
| **cặp dựng được** | **459** |

Cộng dồn khớp tuyệt đối: 64.108 + 459 = 64.567.

### (x13b) ⚠️ Mẫu số in ra SAI — và cổng vẫn trượt dưới mọi cách đếm

`build_min_desc_onpolicy.py:207` ghi cứng mẫu số **41.099** (toàn bộ nhãn vàng), nhưng lượt này
chỉ sinh khai báo cho **14.000** màn ⇒ dòng `1,1%` là mẫu số của một lượt chưa hề chạy.
Đây là **lỗi của mã**, ghi lại để không ai đọc lại con số 1,1% như số thật.

Bốn cách đếm, **không** cách nào đạt ngưỡng 25%:

| mẫu số | nghĩa | eligibility |
|---|---|---|
| 41.099 | như mã in — sai | 1,1% |
| **14.000** | **đã thử thật** | **3,3%** |
| 10.319 | có khai báo hai bên **và** gold có tên | 4,4% |
| 3.252 | chỉ những bước **S2 gọi SAI tên** — rộng lượng nhất có thể biện hộ | **14,1%** |

⇒ **Trượt cổng ③ dưới mọi mẫu số.** Không có chỗ nào để nới, và cũng không cần nới để ra phán
quyết — đó là ý nghĩa của việc khoá ngưỡng trước khi thấy số.

⛔ **Chạy lại O1 với `--limit` lớn hơn KHÔNG cứu được.** Cổng ③ là cổng **tỉ lệ**, không phải
cổng **số lượng**. `--limit 30000` cho ~980 cặp nhưng tỉ lệ giữ nguyên ~3,3%. Đã cân nhắc và
loại, không tiêu thêm giờ GPU.

### (x13c) ⭐ VÌ SAO trượt — đây mới là phần đi vào bài

**76,5% số bước S2 gọi sai tên có `<point>` nằm NGOÀI dải 80–350 px** (2.482/3.246).
Phân bố khoảng cách phần-tử-nhầm ↔ gold: **p25 = 70 px · trung vị = 351 px · p75 = 748 px**.

Đọc phân bố đó:
· **Đuôi dưới (< 80 px):** mô hình trỏ gần như trúng phần tử đúng, chỉ **gọi tên khác đi**. Đây
  không phải chọn nhầm phần tử ⇒ dùng làm vế âm là dạy sai (false negative), cổng ② chặn đúng.
· **Đuôi trên (> 350 px):** mô hình trỏ sang **một vùng khác hẳn của màn**. Cặp như vậy không
  còn là *quy chiếu tối thiểu* — hai vế khác nhau ở quá nhiều thứ, gradient không rơi vào việc
  phân biệt phần tử nữa.
· **Khoảng giữa 80–350 px — vùng "nhầm sang nút hàng xóm" — chỉ chiếm 23,5%.**

⭐ **Phát hiện:** lỗi khai báo của S2 **không phải lỗi lẫn giữa hai phần tử cạnh nhau.** Nó là
lưỡng cực — hoặc cùng phần tử gọi khác tên, hoặc nhìn nhầm sang chỗ khác trên màn. Tiền đề của
biến thể on-policy — *"vế âm tốt nhất là chính cái mô hình hay nhầm"* — **giả định một dạng lẫn
cục bộ mà mô hình này không mắc**.

⇒ Điều này **giải thích ngược** vì sao nguồn heuristic (ép 80–350 px) là cách duy nhất dựng được
tương phản: nó **tạo ra** vùng nhầm-hàng-xóm mà dữ liệu thật gần như không có.
⇒ Và nó nói rõ chỗ nghẽn ở (x10b) — độ chính xác khai báo 60,6% — **không** phải bài toán phân
biệt cục bộ. Hướng chữa bằng tương phản tinh vi hơn ở tầng khai báo đã hết chỗ đi.

### (x13d) Đòn thứ hai, độc lập: 459 cặp là quá ít về mặt số học

Cấu hình đã khoá ở (x3) là 800 bước × tích luỹ 16 = **12.800 lượt mẫu** ⇒ **27,9 epoch** trên
459 cặp. MIN-DESC chạy 22.854 cặp = 0,56 epoch. Ngay cả khi cổng ③ đạt, phép so *"chỉ đổi nguồn
vế âm"* cũng đã hỏng: hai nhánh khác nhau **hai** thứ (nguồn vế âm **và** số epoch). Sửa số bước
để bằng epoch là sửa cấu hình đã khoá ⇒ không làm.

### (x13e) Số phụ đáng giữ

**S2 gọi ĐÚNG tên trên tập DẠY: 68,5%** (7.067/10.319). So với **60,6%** đo trên tập kiểm ở
(x10b) — chênh 7,9 pp đúng chiều kỳ vọng của khoảng cách dạy/kiểm. Hai phép đo độc lập nhau
(một từ `sinh_desc_train.py` trên màn dạy, một từ `gate_desc_acc.py` trên màn kiểm) và khớp về
bậc độ lớn ⇒ củng cố con số 60,6%.

### (x13f) Cam kết (x11d) vẫn thi hành

Bài **phải** báo cả ba nhánh: heuristic (MIN-DESC) · on-policy (**dừng ở cổng, kèm lý do đo
được**) · CE2. Cấm im lặng bỏ nhánh on-policy khỏi bảng. Cấm viết *"chúng tôi chọn heuristic"*
như một lựa chọn thiết kế thuần — nó là kết luận **sau khi** on-policy bị dữ liệu bác.

### (x13g) Không đụng

Thước, luật chấm, mẫu số 4.463, mọi số của (x10) và (x12). Nhánh MIN-DESC và CE2-S2 giữ nguyên
tư cách kết quả chính; (x13) chỉ đóng hồ sơ biến thể.

---

## (x14) ĐĂNG KÝ TRƯỚC — BA NHÁNH CỦA GIAI ĐOẠN THÁNG 9 (khoá 25/8/2026)

Viết **trước khi dựng bất kỳ tệp dữ liệu nào** của ba nhánh dưới đây và **trước khi có bất kỳ
điểm nào**. Căn cứ: phân rã ô quyết định ở (x14a), đo hôm nay bằng 0 giờ GPU trên tệp `*_raw.jsonl`
đã có.

### (x14a) Phân rã ô — nền của mọi quyết định dưới đây

Trên 4.463 bước, cắt theo việc khai báo của MIN-DESC đúng tên / đúng toạ độ:

| ô | n | % | MIN | S1 | người | dư địa tới người |
|---|---|---|---|---|---|---|
| A tên✓ point✓ | 2.082 | 46,7% | **87,1** | 78,2 | 86,3 | **−0,36** |
| B tên✓ point✗ | 220 | 4,9% | 26,4 | 27,7 | 32,3 | +0,29 |
| C tên✗ point✓ | 411 | 9,2% | 57,2 | 53,0 | 73,0 | +1,46 |
| D không sinh desc | 15 | 0,3% | 0,0 | 0,0 | 60,0 | +0,20 |
| **D tên✗ point✗** | **745** | **16,7%** | **3,6** | **25,8** | 64,4 | **+10,15** |
| ngoài lát (không tên vàng) | 990 | 22,2% | 55,3 | 54,4 | 73,0 | +3,94 |
| **TỔNG** | 4.463 | | **60,05** | 59,11 | 75,73 | **+16,04** |

Ba điều đọc ra, và cả ba đều ràng buộc thiết kế:
1. ⭐ **Ô A đã hết chỗ — MIN vượt trần câu người** (87,1 vs 86,3) trên 46,7% số bước.
2. ⭐ **63% dư địa nằm gọn ở ô D**, nơi **MIN 3,6% trong khi S1 25,8%** ⇒ khai báo sai không chỉ
   vô ích, nó **phá câu nặng hơn là không khai báo**. Đây là bản sắc nét của chẩn đoán (x10b).
3. **Trần của mọi can thiệp lúc suy luận rất thấp:** bộ định tuyến **hoàn hảo** (biết trước khai
   báo đúng/sai, sai thì lùi về S1) cho **63,46%**; chỉ ở ô D cho **63,75%**. ⇒ Né không đủ,
   phải **sửa việc nhắm**.

### (x14b) ⚠️ SỬA MỘT CÁCH ĐỌC SAI CỦA CHÍNH DỰ ÁN — không phải sửa ngưỡng

Bảng dải (w)§3 định trên **Δ so S1 tính bằng pp**, cho **trung bình hai hạt giống mỗi nhánh**.
Trợ lý đã có lúc quy nhầm sang mức tuyệt đối và báo *"65% là ngưỡng dương yếu"*. Quy đúng, với
S1 hai hạt giống = **59,36%** (59,11 và 59,62):

| dải | Δ so S1 | mức tuyệt đối |
|---|---|---|
| TRẮNG | −2,8 … +1,7 | 56,56 – **61,06** |
| **DƯƠNG YẾU** | +1,7 … +2,8 | **61,06 – 62,16** |
| **DƯƠNG** | ≥ +2,8 | **≥ 62,16** |

⛔ **Ngưỡng KHÔNG đổi một chữ** — vẫn là +1,7 / +2,8 pp khoá ngày 5/8. Chỉ sửa phép quy đổi.
📌 Con số **65,0%** trong `paper/fair2026/main.tex` **đúng** nhưng trả lời câu khác: đó là điểm
mà lượt **S2/202 đã huỷ** sẽ phải đạt để trung bình hai hạt của S2 chạm mép dương yếu
(`2 × 61,06 − 57,18 = 64,95`). Đừng đọc nó thành ngưỡng của một nhánh.
📌 MIN-DESC 60,05 ⇒ Δ = **+0,69 pp**, còn **2,11 pp** nữa là DƯƠNG.

### (x14c) ⭐ MỞ RỘNG PHẠM VI BẢNG DẢI — khai báo minh bạch

Bảng (w)§3 viết cho `Δ = S2 − S1`. Ba nhánh dưới đây **không phải S2**. Tại đây đăng ký việc
**dùng nguyên bảng đó cho mọi nhánh mới**, không sửa ngưỡng, vì hai nguồn nhiễu dựng nên ngưỡng
(SE thước 0,38 pp · σ giữa hạt giống 0,46 pp) là thuộc tính của **bố trí đo**, không của riêng S2.
⛔ Cấm phát minh dải mới cho nhánh mới. ⛔ Cấm đọc bảng khi chỉ có một hạt giống — khi đó
**mọi kết quả là TRẮNG theo định nghĩa**, đúng như (w)§3 phát biểu.

### (x14d) Ba nhánh, và ĐÚNG MỘT lý do tồn tại cho mỗi nhánh

**① NHÁNH-ỨNG-VIÊN** (đường tới ô D — *sửa việc nhắm*)
Đưa vào **đầu vào** một khối ứng viên `tên <point>x,y</point>` dựng từ **OCR ∪ cây trợ năng
offline**. Ô `<desc>` đổi từ **sinh tự do** thành **chọn trong danh sách của chính màn đó**.
Ba số làm trụ, đo hôm nay: tên vàng có trong OCR ∪ a11y **99,7%** · tồn tại ứng viên vừa khớp tên
vừa trong ±14% điểm vàng **80,2%** (so khai báo hiện tại **59,9%** ⇒ dư địa **+20,3 pp**) · câu
nhắc hiện chỉ nhét **24 dòng OCR KHÔNG kèm toạ độ** (`build_branch_data.py:31`), mà **67,7%** số
bước MIN gọi sai tên đã có tên vàng nằm sẵn trong 24 dòng đó ⇒ **thông tin có sẵn mà không dùng
được vì thiếu neo vị trí**.
⚠️ **Thêm đầu vào ⇒ KẾT QUẢ MỨC HỆ THỐNG.** Bắt buộc: (a) train **đối chứng cùng đầu vào** và
luôn trình theo cặp; (b) giữ nguyên bảng cũ không đầu vào phụ, không thay thế; (c) không so trực
tiếp với S1/Base như thể cùng điều kiện.

**② NHÁNH-LÙI** (đường hạn chế thiệt hại ở ô D — *selective prediction học được*)
Dựng đích SFT từ **14.000 rollout S2 đã có** (68,5% đúng tên): bước mô hình **từng sai** có đích
`<desc>không chắc</desc>` + câu chung chung kiểu S1; bước **từng đúng** giữ khai báo vàng + câu
đặc tả. Một mô hình duy nhất, **không thêm đầu vào** ⇒ so với S1 vẫn công bằng.
⚠️ Thiên lệch biết trước, phải ghi Limitations: nhãn "từng sai" là hành vi của **S2 trên tập dạy**
(68,5% đúng) trong khi tập kiểm chỉ 60,6% ⇒ mô hình sẽ **lùi ít hơn mức cần**.

**③ MIX** (không nhắm điểm — *gỡ điều kiện claim đang trượt*)
Trộn bước **không-chạm** dạng CE thuần vào stage-2. Lý do duy nhất: điều kiện (x5) mục 4 đang
**TRƯỢT** (−19,75 pp, ngưỡng > −3 pp) theo (x3e). ⛔ **Cấm trình MIX như một cải tiến điểm số.**

### (x14e) Cổng chặn — khoá số TRƯỚC khi thấy dữ liệu

| cổng | khi nào | ĐẠT | TRƯỢT ⇒ |
|---|---|---|---|
| G1 phủ | dựng xong khối ứng viên, 0 GPU | tên vàng trong khối ≥ **95%** | bỏ nhánh ① |
| G2 C3 | như trên | tồn tại ứng viên khớp tên ∧ trong ±14% ≥ **75%** | bỏ nhánh ① |
| G3 rò rỉ | kiểm mù **300 mẫu** | khối ứng viên **không** chứa dấu hiệu nào chỉ ra phần tử đích | bỏ nhánh ① |
| G4 độ dài | 200 mẫu **dài nhất** | token câu nhắc ≤ `cutoff_len` **2560** | sửa cách cắt danh sách, không sửa `cutoff_len` |
| G5 smoke | 20 bước, ~40 phút | `train_runtime` ~200–500 s (không ~15 s) · loss đúng dải của stage | dừng |
| G6 sớm | nhánh ① ở **600 bước**, ~2 h | `gate_desc_acc` ≥ **+3,0 pp** so mốc MIN **60,6%** | **dừng, cứu ~40 h** |
| G7 dải lùi | nhánh ② trên tập kiểm | tỉ lệ lùi ∈ **[15%, 45%]** | ngoài dải ⇒ sập hoặc không học, dừng |

### (x14f) Điểm quyết định — cũng khoá số tại đây

· **D1** sau nhánh ②: exec ≥ **61,5%** thì giữ, dưới thì bỏ.
· **D2** sau nhánh ①: exec ≥ **62,0%** **và** (① − đối chứng cùng đầu vào) ≥ **+2,0 pp**. Thiếu một
  trong hai vế là bỏ — vế thứ hai chặn việc quy công cho khối ứng viên thứ mà bất kỳ đầu vào giàu
  hơn nào cũng cho.
· **D3**: chọn **ĐÚNG MỘT** nhánh để nhân hạt giống. Chọn theo D1/D2, không chọn sau khi ngó số.

### (x14g) Cam kết trước khi thấy số

1. Nhánh nào chạy hạt giống thứ hai thì **báo trung bình hai hạt bất kể ra sao** — (x8c) áp nguyên.
2. Khi báo Δ, kèm đủ bốn thứ của (w)§3: bốn số riêng lẻ · tỉ lệ bước bất đồng (mốc null 6,4% ·
   can thiệp thật 24%) · phân tầng độ dài câu · **hai hạt lệch > 1,5 pp thì dừng truy nguyên nhân
   trước khi đọc Δ**.
3. **Báo cả ba nhánh** kể cả nhánh trượt cổng — như (x11d) đã buộc và (x13) đã thi hành.
4. Không đụng: thước · luật chấm · mẫu số 4.463 · luật cắt `<desc>` · luật chọn điểm lưu ·
   `cutoff_len` · cấu hình P9.

### (x14h) Chữ CẤM dùng

⛔ **"đầu tiên" / "novel" / "cơ chế mới"** cho việc đưa danh sách ứng viên vào đầu vào — bài gốc
AndroidControl (**NeurIPS 2024 D&B**) đã fine-tune với danh sách a11y làm INPUT; Mind2Web
(**NeurIPS 2023 D&B**) và Zheng và cs. (**ICML 2024**) đã lọc ứng viên ở tầng hành động.
⛔ **"đầu tiên"** cho ý *học cách từ chối* — ASPIRE (**Findings of EMNLP 2023, tr. 5190–5213**)
đã chiếm từ 2023.
⛔ Cấm trích Wang và cs. (**ICLR 2023**) *"+17,9%"* mà không kèm điều kiện **k=40 trên 137B–540B**.
⛔ Cấm trình preprint như đã bình duyệt: RFT (arXiv 2308.01825) · PET-SQL (arXiv 2403.09732) ·
SafeGround (arXiv 2602.02419) · UI-TARS (arXiv 2501.12326).

### (x14i) Đã loại, kèm lý do ĐO ĐƯỢC (không phải lý do giá)

· **định tuyến/abstention lúc suy luận** — trần **oracle 63,46%**; bảy bộ định tuyến thật cho
  60,0–60,34%, tức nhiễu.
· **ràng buộc giải mã ô tên** — dư địa vật lý **+1,46 pp**, và ở ô D **68,6%** tên mô hình sinh ra
  **đã là chuỗi có thật trên màn** ⇒ ràng buộc **không kích hoạt** ở phần lớn khối lỗi. Mô hình
  không bịa tên, nó chọn đúng chuỗi của **sai phần tử**.
· **sửa tên chọn lọc** — tầng khai báo +3,85 pp (b=133, c=0, χ²=131) nhưng trần exec **60,01%**
  vì 107/133 bước sửa được **đã trúng sẵn**. ⭐ Đây là ca hệ số chuyển đổi 0,43–0,79 **dự báo sai**:
  nó ước trên can thiệp đổi **cả tên lẫn điểm**.
· **self-consistency k=5** — số duy nhất trên đầu ra có cấu trúc là +0,4% (preprint).
· **RFT/STaR trên 14.000 rollout** — mức tăng teo theo độ mạnh của nền: +4,8…+6,1 pp ở nền
  35,9–50,0%, **−0,1 pp ở nền 54,6%**; nền của ta **68,5%**.
· **copy/pointer từ OCR** — lấy mục OCR gần điểm vàng nhất cho tên đúng **64,9%**, **thấp hơn**
  66,3% mô hình tự đạt.
· **`--ceiling gold`** — oracle leak, câu người chứa nguyên văn tên phần tử 53,9%.
· **`s2_nopoint` / `s2r`** — `report/117` Mục 3 đứng vững **không dựa vào giá**: toạ độ đúng một
  mình +1,12 pp vs tên đúng một mình +0,54 pp; tái lập ở ô C (411 bước đang được toạ độ cứu).
· **rerank bằng bộ trỏ** — trọng tài trùng thước, vòng tròn.

---

## (x15) SỬA ĐỔI — NÂNG `cutoff_len` 2560 → 3072 CHO CẶP NHÁNH-ỨNG-VIÊN

Ghi 25/8/2026, **trước khi train**, **trước khi có bất kỳ điểm nào** của nhánh ỨNG-VIÊN.
Mục (x14g) điểm 4 xếp `cutoff_len` vào danh sách "không đụng"; mục này **sửa đúng một dòng đó**,
chỉ cho cặp nhánh ỨNG-VIÊN, và nêu lý do đo được.

### (x15a) Vì sao buộc phải đổi

Khối ứng viên tốn token. Đo 25/8 bằng bộ tách token của chính mô hình nền:

| trần ứng viên | phủ tên vàng (cổng G1 đòi ≥95%) | token khối, max |
|---|---|---|
| 16 | **76,2%** ⛔ | 492 |
| 32 | 93,2% ⛔ | 656 (đã dùng cách viết gọn nhất trong bốn dạng thử) |
| **40** | **96,7%** ✅ (đủ tập kiểm) | 1.012 |

Ngân sách dưới `cutoff_len` 2560 chỉ còn **543 token**: cấu hình đã ghi **ảnh chiếm 1.272 token**
và mẫu dài nhất của nhánh s2 là **2.017**. ⇒ Trần khả thi là 16, mà 16 **trượt cổng G1**.
⇒ Hoặc bỏ nhánh, hoặc nâng trần chuỗi. Không có cửa thứ ba: đã thử nén cách viết (bốn dạng) và
đã cân nhắc hạ `image_max_pixels` 1003520 → 602112 (giải phóng ~509 token) rồi **loại**, vì tác vụ
là **đọc chữ nhỏ trên giao diện** — hạ độ phân giải đánh thẳng vào năng lực cần dùng.

### (x15b) Vì sao đổi vẫn hợp lệ

1. **Chưa có bất kỳ điểm nào của nhánh này.** Vi phạm là *nới ngưỡng sau khi thấy số*; đây là
   ràng buộc kỹ thuật lộ ra lúc **dựng dữ liệu**, không phải lúc đọc kết quả.
2. **Thước, luật chấm, tập kiểm, mẫu số 4.463, bảng dải (w)§3 — không đụng một chữ.** Cái đổi
   nằm ở khâu **nạp dữ liệu**.
3. **Đổi cho CẢ nhánh xử lý lẫn đối chứng cùng đầu vào** ⇒ hiệu số nội bộ không lệch.
4. **Tiền lệ trong chính dự án:** 11/8 đã nâng 2048 → 2560, cùng đúng lý do (cắt cụt câm nuốt mất
   đích sinh), ghi lại trước lượt train đầu tiên.
5. **Nâng trần không tốn thêm gì** — đệm theo mẫu dài nhất trong từng lô, không đệm tới
   `cutoff_len` (ghi sẵn ở `train_config.yaml`). ⚠️ Nhưng **bộ nhớ đỉnh** thì có đổi ⇒ cổng G5
   (probe 200 mẫu dài nhất) thành **bắt buộc**, đúng bài học P10.

### (x15c) Ba điều kiện ràng buộc — thiếu một là vi phạm

1. Mục này phải đứng **trước** mọi lượt train của nhánh ỨNG-VIÊN trong `git log`.
2. ⛔ **Cặp mới chỉ đọc nội bộ với nhau.** Cấm đặt điểm của nhánh ỨNG-VIÊN cạnh S1/S2/MIN/CE2 rồi
   tính hiệu — khác `cutoff_len` **và** khác đầu vào. Đại lượng đọc bằng bảng dải là
   `Δ = ỨNG-VIÊN − ĐỐI-CHỨNG-CÙNG-ĐẦU-VÀO`, cả hai ở `cutoff_len` 3072.
3. Bài phải **nói thẳng** nhánh này được chuỗi vào dài hơn, vì sao, và đối chứng cũng y như vậy.

### (x15d) Con số chốt

`cutoff_len: 3072`. Suy ra từ 2.017 (mẫu dài nhất hiện tại, đã gồm ảnh 1.272) + 1.012 (khối ứng
viên dài nhất ở trần 40) = 3.029, làm tròn lên bội của 256.
Trần ứng viên **40**. Cách viết `tên <point>x,y</point>` ngăn bằng ` · ` — **giữ dạng `<point>`**
để mô hình chép thẳng sang ô khai báo được, dù dạng nén tiết kiệm hơn ~30%.

### (x15e) Không đụng

Mọi thứ khác của cấu hình P9: `image_min_pixels` · `image_max_pixels` · `per_device_train_batch_size`
· `gradient_accumulation_steps` · lịch `lr` · số bước · luật chọn điểm lưu · `enable_liger_kernel`.
Và toàn bộ khâu chấm.

---

## (x16) SỬA ĐỔI — THU HẸP PHẠM VI SAU KHI CỔNG G6 TRƯỢT, VÀ ĐĂNG KÝ TRƯỚC NGƯỠNG τ

Ghi **4/9/2026 (ICT)**, **trước** lượt chấm `exec` đầu tiên của nhánh ỨNG-VIÊN, **trước** khi
train nhánh đối chứng, và **trước** khi tính bất kỳ điểm sequence-score nào. Nguồn phán quyết:
`report/134_CHOT_4_9_HANDOFF_CHAT.md` (chốt sau vòng debate nhiều họ mô hình ngày 4/9).

Mục này **không nới một ngưỡng nào**. Nó làm ba việc: thu hẹp phạm vi lượt chạy, hạ vai một thước
đã đăng ký, và **đăng ký trước một thủ tục chọn ngưỡng chưa từng có trong hồ sơ**.

### (x16a) Sự việc — cổng G6 trượt và GIỮ trượt

Cổng G6 của (x14e) đòi `sel_acc ≥ 63,6%` trên các bước có ứng viên vàng của lát dev 1.400.
Đo được **580/1.008 = 57,54%**, kém **6,1 điểm**. Đã xác minh ba cách trước khi tin số: 100% bản
ghi có thẻ `<sel>` · 99,6% tên được chọn nằm trong khối ứng viên · n = 1.008.

⛔ **Cổng giữ nguyên phán quyết TRƯỢT.** Không nới, không đổi mẫu số, không đổi lát. Hệ quả đã
thi hành: năm lượt train còn lại của (x14) **không chạy**.

### (x16b) Thu hẹp phạm vi — hai lượt A100 còn MỘT

Gói sáu lượt của `report/128` (≈69 h A100) **đã huỷ** cùng lúc với phán quyết G6. Bản này chốt
tiếp: trong hai lượt từng dự kiến còn lại, **chỉ chạy một** — `gui_sft_match`/hạt 101.

**Bị bỏ, kèm lý do:**
· `gui_sel`/**202** — hạt thứ hai của nhánh xử lý. Bỏ vì cổng đầu vào của chính nhánh đó đã trượt;
  chi thêm ~23–30 h A100 để đo lại một cơ chế đã biết là chưa qua cổng thì không mua thêm thông tin.
· **`S1-match`** — lượt tách công của khối ứng viên. Bỏ vì ngân sách, **và kéo theo một hệ quả
  phải khai**: thiếu nó thì **không được claim công của khối ứng viên** (xem (x16i)).

⚠️ **Hệ quả vĩnh viễn, cùng dạng với (x1):** estimand hai hạt của nhánh ỨNG-VIÊN **không hoàn
tất**. `Δ_sel` là số **một hạt giống**, nằm dưới MDE 2,11 pp của thiết kế một hạt ⇒ theo đúng luật
(w) đang có hiệu lực, nó rơi vào ô **TRẮNG theo thiết kế**, không phải kết quả âm và cũng không
phải kết quả dương. **Cấm** đọc nó qua bảng bốn kết cục Dương/Âm.

### (x16c) Hạ vai `sel_acc`, giữ nguyên định nghĩa

`sel_acc` **giữ đúng định nghĩa đã khoá** và **giữ nguyên phán quyết trượt** của nó. Cái đổi là
**vai trò khi trình bày**: từ 4/9 nó là **thước phụ**, không phải headline.

Lý do đo được, không phải lý do thẩm mỹ: `sel_acc` chỉ đếm nhóm có ứng viên vàng, tức đúng cột
*HasAns* của SQuAD 2.0 khi báo một mình. Phép chẩn đoán ép-phải-chọn ngày 3/9 cho thấy **bỏ hoàn
toàn cơ chế bỏ cuộc kéo `sel_acc` 57,54 → 69,05 (+11,51 pp) trong khi độ đúng trên toàn bộ 1.400
bước TỤT 63,43 → 49,71 (−13,71 pp)**. Một thước mà cải thiện nó bằng cách làm hệ thống tệ đi thì
không được đứng ở vị trí headline.

⭐ **Headline confirmatory từ 4/9: `exec` = `action_ok ∧ toggle_ok ∧ hit_voronoi`, dung sai .14,
trên n = 4.463 bước chạm.** Đây **không phải thước mới** — nó là thước primary đã niêm từ 5/8 cho
mọi nhánh của dự án, và bảng dải (w) áp cho nó. Việc làm ở đây là **quay về** thước gốc, không
phải đổi thước.

Thứ bậc thước, khoá tại đây:
· **Confirmatory / quyết Δ / headline:** `exec` Voronoi gated .14, n = 4.463.
· **Thứ cấp, interval-only:** nhánh khoảng cách nL2 .14 và chữ nhật .14 (`hit_disk`). Được in
  khoảng tin cậy để định vị so với văn liệu, **cấm dùng để cứu một Δ Voronoi trắng**.
· **Cấm:** Holm hay bất kỳ thủ tục nào lấy thước thứ cấp cứu primary.

### (x16d) ⭐ ĐĂNG KÝ TRƯỚC — thủ tục chọn ngưỡng τ cho cơ chế bỏ cuộc

Đây là phần **mới hoàn toàn** so với hồ sơ 5/8. Đăng ký đầy đủ tại đây, **trước khi tính điểm
sequence-score đầu tiên**, để thủ tục không thể bị chỉnh sau khi thấy số.

**Điểm số.** Với câu nhắc cố định `x`, mỗi phương án `c` là **toàn bộ span chọn**, lấy nguyên văn
từ artifact đã pin và render bằng đúng hàm dựng chuỗi của khâu dạy, dạng
`<sel>{tên ứng viên} <point>x,y</point></sel>` hoặc `<sel>none</sel>`. Teacher-force từng span,
chỉ cộng log-probability của token **thuộc span đó** (không cộng câu nhắc, không cộng câu hướng
dẫn), rồi chia cho số token của span:

`s(c|x) = ( Σ_t log p(token_t | x, token_<t) ) / số_token(span_c)`

**Quyết định.** `c* = argmax s(c|x)` trên các ứng viên **thật**; margin `m = s(c*) − s(none)`.
Phát `c*` khi `m > τ`, ngược lại phát `none`.

**Split.** Quét τ **chỉ trên lát dev 1.400**. Áp **một lần duy nhất** lên phần còn lại.

**Tiêu chí chọn τ.** Cực đại **độ đúng trên toàn bộ 1.400 bước** — không phải trên `sel_acc`,
không phải trên nhóm HasAns. Hoà thì chọn phương án cho **ít `none` sai hơn**.

**Luật null nằm trong lưới quét.** Lưới τ **bao gồm** phương án "giữ nguyên hành vi greedy hiện
tại" (tức không áp τ). ⛔ **Nếu mức cải thiện tốt nhất nhỏ hơn ~18/1.400 bước (khoảng một sai số
chuẩn nhị thức), thì khoá luật null** — báo cáo rằng thủ tục không mua được gì. Toàn bộ đường
cong được in **kể cả khi luật null thắng**.

**Thứ tự bắt buộc.** τ phải được khoá **trước khi nhìn** `exec` của nhánh đối chứng **và trước
khi nhìn** phần 3.062 bước. Vi phạm thứ tự này là vi phạm đăng ký trước.

**Nhãn.** Toàn bộ dòng τ mang nhãn **thăm dò (exploratory)**. Nó không nằm trong estimand đã niêm
5/8 và **không được trình như kết quả xác nhận**.

⚠️ **Điểm dùng để quyết định là điểm chuỗi đầy đủ, không phải xác suất token đầu.** `p_none` đo ở
bước đầu tiên, nếu có chạy, chỉ là **chẩn đoán nhị phân**, không phải xác suất của ứng viên, và
**không đủ để gọi tên thủ tục của Devlin et al.** Hợp đồng này **thay** phương án τ-first-token
từng ghi ở `report/133`.

### (x16e) Sửa một thuật ngữ dùng sai của chính dự án — 3.062 KHÔNG phải hold-out

`report/132` và `133` gọi phần 3.063 bước còn lại là *"hold-out"*. **Sai thuật ngữ.** Phần đó
không được tách ra và niêm phong từ trước như một confirmatory split; nó là **phần dư** sau khi
lát dev 1.400 đã được chấm.

⇒ Từ 4/9 nó mang đúng tên: **one-look hậu kiểm**, nhìn **đúng một lần** sau khi τ đã khoá.
Sau khi loại đúng một episode trùng với lát dev (`18852`, 1 bước) còn **3.062 bước / 891 episode**.
⛔ Cấm gọi nó là hold-out đăng ký trước trong bất kỳ bản thảo nào.
⚠️ Mẫu số của `exec` **vẫn luôn là 4.463**, không phải 3.062 — hai đại lượng khác nhau, đừng trộn.

### (x16f) Cách đọc kết quả mới — thăm dò, không thay bảng dải

Bộ đọc kết quả cho cơ chế bỏ cuộc, khoá tại đây, mang nhãn **thăm dò**:
① bộ ba kiểu SQuAD 2.0 — báo **HasAns**, **NoAns** và **overall** cùng lúc, không bao giờ báo
HasAns một mình; ② **risk tại coverage cố định** và đường cong risk–coverage; ③ ngưỡng τ theo
(x16d). Tiền lệ và cách trích dẫn ở `report/135`.

⛔ Bộ đọc này **không thay** bảng dải (w) và **không** áp cho `Δ_sel`. `Δ_sel` vẫn đọc bằng đúng
luật cũ, và vì một hạt nên rơi vào ô TRẮNG theo thiết kế.

### (x16g) Cam kết trước khi thấy số

1. Báo cả nhánh **dừng ở cổng**, đúng cam kết (x11d) đã thi hành hai lần trước đây.
2. `exec` của nhánh ỨNG-VIÊN được báo **dù nó ra sao**, kể cả khi thấp hơn S1 cũ.
3. Đường cong risk–coverage in **trọn**, không cắt đoạn xấu.
4. Nếu luật null thắng ở (x16d) thì **nói thẳng là thủ tục không mua được gì**.
5. Nếu lượt đối chứng không kịp về đích trước mốc giết (đạt dưới ≈2.422/4.036 bước lúc 8/9 12:00
   ICT) thì **bỏ lượt đó**, không dùng điểm lưu dở, và bài chỉ còn phần chẩn đoán.

### (x16h) Chữ CẤM dùng

⛔ *"hold-out"* cho 3.062 · *"đầu tiên"/"mới"* cho cơ chế bỏ cuộc (xem `report/135` §5) ·
*"AITW"* cho luật chữ nhật ±14% · *"human ceiling"* cho mốc 75,73 (đúng tên: **mốc câu người dưới
cùng dụng cụ**) · gọi `Δ_sel` là **Dương** · trình công của khối ứng viên khi thiếu `S1-match` ·
đặt điểm nhánh ỨNG-VIÊN cạnh S1 cũ rồi tính hiệu (lệch `cutoff_len` **và** lệch đầu vào, đã cấm ở
(x15c) điểm 2).

### (x16i) Không đụng

Thước và luật chấm · mẫu số 4.463 · bảng dải (w) và ba ngưỡng của nó (TRẮNG −2,8…+1,7 · Dương
+2,8 · MDE 2,11) · định nghĩa `sel_acc` và phán quyết trượt của G6 · constructor khối ứng viên
(max 40, thứ tự đọc, merge cùng tên overlap only) · cấu hình train của (x15) · luật chọn điểm lưu
· hạt giống · tập kiểm.

## (x17) SỬA ĐỔI — BỎ HẠN SOICT, HUỶ ĐỐI CHỨNG A100, VÀ ĐĂNG KÝ TRƯỚC LUẬT QUYẾT LƯỢT ② (khoá 5/9/2026, trước khi có điểm τ)

Ghi lúc commit Kaggle 1 của lượt sequence-score đang chạy (bắt đầu ~02:45 ICT 5/9), **chưa có
bất kỳ điểm τ nào trên đĩa** ngoài probe 50 bước (`runs/sel/probe50_seqscore.jsonl`, chỉ để kiểm
mã). Mọi ngưỡng dưới đây khoá tại đây.

### (x17a) Sự việc

Chủ luận văn quyết 5/9: **không nộp SOICT 16/9**; mục tiêu còn lại là đóng góp mô hình cho luận
văn với số dễ bảo vệ hơn. Hệ quả: lượt A100 `gui_sft_match`/101 (x16b) **huỷ, không chạy**;
`Δ_sel` **không tồn tại** và sẽ không được tính. Mọi ràng buộc "không làm trước 16/9" của
`report/134` mục 0 hết hiệu lực. **Không đụng:** thước headline, mẫu số 4.463, bảng dải (w), luật
một-hạt-giống-là-TRẮNG (x14c), thủ tục τ (x16d), cam kết (x16g) mục 1–4.

### (x17b) Lượt ② — `gui_sel_cham`, và điều kiện chạy

**Định nghĩa.** Train lại nhánh ỨNG-VIÊN trên **41.191 bước chạm** (`click`/`long_press`) của
tập dạy, lọc theo chỉ số từ `gui_sel.json` bằng `harness/make_sel_cham.py` → `gui_sel_cham.json`
(đã dựng 5/9 02:26, 41.191 mẫu). **Đúng một biến đổi: tập mẫu** — câu nhắc, khối ứng viên, thẻ
`<sel>`, yaml (x15), hạt 101 giữ nguyên. Căn cứ: tỉ lệ `<sel>none</sel>` 54,78% ở tập dạy so
với 29,1% trên bước chạm và 28,34% ở tập kiểm (`report/136` mục 11); Rajpurkar và cs. (ACL 2018)
*"different proportions of negative examples at training and test time"*; Menon và cs. (ICLR
2021) về sửa tiên nghiệm lúc train. Số bước ≈ 2.575, ≈ 15 h A100.

**Luật quyết — đọc từ `harness/quet_tau.py` trên đủ 1.400 bước dev, theo (x16d):**

| kết quả quét τ | hành động |
|---|---|
| lift ≥ 18/1.400 so với greedy | **chạy ② hạt 101** |
| lift < 18/1.400 (khoá luật null) | **không chạy ②**; nhánh ỨNG-VIÊN đóng ở chẩn đoán; đóng góp mô hình chốt ở MIN-DESC |

Không có ô thứ ba. Không đổi ngưỡng 18 sau khi thấy đường cong.

**Hạt 202.** Quyết định chạy hay không chạy `gui_sel_cham`/202 phải ghi vào mục (x18) **trước
khi nhìn `exec` của ②/101**. Không quyết thì ② là một hạt ⇒ TRẮNG theo (x14c), không có ngoại lệ.

### (x17c) Hệ `gui_sel`+τ — cách lấy `exec`, đăng ký trước

τ lật lựa chọn ở một bước thì câu đi kèm chưa tồn tại (câu sinh sau thẻ). Thủ tục: với mọi
bước mà `chọn(τ*) ≠ chọn(greedy)`, sinh lại câu bằng **ép thẻ** `<sel>…</sel>` đúng phương án
của τ* (cùng mẫu `preds_gui_sel_forcesel_273.jsonl` ngày 3/9), giữ nguyên câu ở các bước không
lật, rồi chấm UGround như mọi nhánh. Làm trên dev 1.400 trước, one-look 3.062 sau, **cùng một
τ*** đã khoá. Nhãn **thăm dò**. So sánh hợp lệ: `gui_sel` greedy vs `gui_sel`+τ (cùng adapter),
và ②/101 greedy vs `gui_sel`+τ (cùng chẩn đoán, hai cách sửa). Không so với S1/MIN như Δ sạch.

### (x17d) Thước đồng-báo D.3 — vị trí và giới hạn

Luật hộp của Phụ lục D.3 (AndroidControl) tính bằng `harness/luat_d3.py`, kết quả
`runs/luat_d3.json`. Vị trí: **bảng độ nhạy luật chấm**, cạnh năm luật của
`rule_sensitivity.py`, cột nguồn + cột "tính 5/9, sau khi có điểm". Không vào bảng chính, không
vào tóm tắt. Con số dùng khi bảo vệ là biến thể **D.3 ∧ cửa sổ 14%**. Ba số phải khai kèm
(`report/139`): 48% hộp là nút con không nhận chạm · 78% mức tăng từ hộp rộng hơn nửa màn · 120
bước container cho điểm gần miễn phí.

### (x17e) Cam kết

1. Báo kết quả quét τ **dù null thắng**, in trọn đường cong (x16d).
2. Nếu ② chạy: báo `exec` của nó **dù ra sao**, cạnh `gui_sel`/101 greedy, trên đúng 4.463.
3. Không nới 18/1.400, không đổi tiêu chí "đúng toàn 1.400", không đổi mẫu số.
4. Không dùng D.3 làm headline; không trình 83,82 như "trần mới".

### (x17f) Hai nhánh luật τ phụ — đăng ký 5/9 SAU probe 50 bước, TRƯỚC khi có 1.400

**Sự việc dẫn tới mục này, khai thẳng:** chạy `quet_tau.py` trên probe 50 bước (tệp chỉ để
kiểm mã) thấy ở τ = −∞ (luôn phát c\*) luật (x16d) chỉ đúng vàng **22/40** bước có vàng, trong
khi greedy dám chọn 30/40 và đúng 26. Truy: xếp hạng ứng viên theo **tổng** log-prob (không
chia số token) cho vàng đứng đầu **30/40**. Tức phép **chuẩn hoá độ dài** của (x16d) làm hỏng
phần *xếp hạng ứng viên* (thiên về span dài mà từng token dễ đoán), dù nó vẫn hợp lý cho phần
*bỏ cuộc hay không*. Trên 50 bước, lift so với greedy: (x16d) **−6** · lai **0** · tổng **+2**
· lai-tổng **+3**. n = 50 nên đây chỉ là dấu hiệu, không phải kết quả.

**Đăng ký** ba nhánh phụ, định nghĩa cố định, thi hành trong cùng `quet_tau.py`:
· **A — lai, chuẩn hoá:** greedy chọn ⇒ giữ nguyên; greedy `none` ⇒ phát c\* của (x16d) nếu
  m > τ. Chỉ đụng phần bỏ cuộc, không đụng phần xếp hạng.
· **B — tổng log-prob:** c\* = argmax Σ log p (= điểm/token × số token); m_sum = log p(c\*) −
  log p(none); phát c\* nếu m_sum > τ. Mốc tiên nghiệm τ₀ = −0,633 áp thẳng lên m_sum (Menon
  2021, dạng post-hoc), in làm tham chiếu.
· **C — lai, tổng:** greedy chọn ⇒ giữ; greedy `none` ⇒ c\* của B nếu m_sum > τ.

**Luật đọc.** (x16d) vẫn là nhánh **chính**, ngưỡng 18/1.400 giữ nguyên. Ba nhánh phụ dùng
ngưỡng **24/1.400** (≈ +1 SE, bù cho việc chọn trong ba). Luật quyết lượt ② ở (x17b) đọc
**nhánh đạt ngưỡng có lift lớn nhất**; không nhánh nào đạt ⇒ luật null. Mọi đường cong in trọn.
Nhãn **thăm dò** cho cả bốn.

**Không được:** thêm nhánh thứ năm sau khi thấy 1.400 · đổi tiêu chí sang HasAns · đổi 18/24.


## (x18) KẾT QUẢ QUÉT τ VÀ QUYẾT ĐỊNH LƯỢT ② (ghi 5/9/2026 21:00 ICT, SAU khi có 1.400)

**Sự việc.** `quet_tau.py` chạy trên đủ 1.400 bước dev (hai commit Kaggle nối tiếp, 7/7 phép
kiểm toàn vẹn đạt). Luật null (greedy) đúng **888/1.400 = 63,43%**. Lift so với null: X (x16d)
**−360** [−397 · −322] · A **+1** [0 · +4] · B **−52** [−83 · −21] · C **+8** [−11 · +27].
Ngưỡng 18 (X) / 24 (A·B·C). τ₀ = −0,633 áp lên B: −143; lên C: +1. Toàn văn `report/142`.

**Áp luật (x17b) + (x17f), không nới:** không nhánh nào đạt ⇒ **khoá luật null** ⇒ **lượt ②
`gui_sel_cham`/101 KHÔNG chạy.** Câu hỏi hạt 202 của (x17b) vô hiệu. Hệ `gui_sel`+τ không tồn
tại ⇒ (x17c) không áp dụng, không chấm exec nào thêm.

**Ghi nhận theo (x17e).** Báo trọn bốn đường cong (đã in ở `runs/sel/tau_scan_stdout.txt`).
Chẩn đoán: xếp hạng ứng viên theo tổng log-prob đúng 67,5% HasAns (chuẩn hoá/token 38,3%);
điểm thẻ `none` ở 275 bước bỏ-cuộc-sai và 308 bước bỏ-cuộc-đúng trùng nhau (trung vị −1,706 vs
−1,710), AUC biên 0,69–0,72 ⇒ khâu bỏ cuộc mù với likelihood của chính mô hình; trần nếu bỏ
cuộc hoàn hảo 78,0% trên dev.

**Khai thẳng một lý do đến sau khi thấy số, và KHÔNG dùng:** τ₀ không mô phỏng được việc lượt
② bỏ 2.495 bước không chạm (bỏ luôn đường tắt *động từ không chạm ⇔ none*, 38,9% câu ở nhóm
bỏ-cuộc-sai). Lý lẽ này hợp lý nhưng sinh ra sau khi nhìn kết quả; theo (x17f) *"không nới sau
khi thấy số"*, không dùng nó để mở lại lượt ②. Nếu về sau có lượt train nào theo hướng này thì
phải ghi là quyết định mới, không phải hệ quả của (x17b).

**Trạng thái nhánh ứng viên: ĐÓNG ở chẩn đoán.** Đóng góp mô hình của luận văn giữ ở MIN-DESC.

## (x19) QUYẾT ĐỊNH MỚI 5/9/2026 (đêm, ICT) — GRPO THƯỞNG `<point>` NỐI TIẾP TỪ MIN-DESC/101 — khoá TRƯỚC khi chạy

**Bối cảnh, khai thẳng.** Đây là quyết định **mới** sau khi đã thấy mọi điểm hiện có (MIN 60,05 ·
τ null thắng · bảng chéo MIN×gui_sel ở `report/143` §4.1), do chủ luận văn yêu cầu nâng số
(*"cần 65–70"*). Nó **không** là hệ quả của mục nào trước; các luật đọc của `106` (thước
headline Voronoi gated · mẫu số 4.463 · MDE 2,2 · một hạt = TRẮNG) **giữ nguyên**.
Lý do chọn hướng này thay cho các hướng khác: `report/143` §4.2–4.3.

### (x19a) Hệ thống
· Khởi tạo: adapter **MIN-DESC/101** (gốc `ckpt/min_desc_seed101`, bước 800) trên Qwen2.5-VL-3B
  4-bit NF4; **học tiếp chính adapter đó** (không adapter mới, không merge).
· Thuật toán: GRPO (TRL **0.29.1**, pin), `loss_type` mặc định của bản đó (`dapo`), `epsilon` 0,2,
  `num_iterations` 1, `scale_rewards="group"`, **β = 0,04** với mô hình tham chiếu = **bản sao
  adapter MIN** (TRL `add_adapter("ref")` sao chép trọng số `default` ⇒ KL neo về MIN, không về
  mô hình gốc).
· Lấy mẫu: **G = 4**/câu nhắc, temperature **1,0**, top-p 1, `max_completion_length` 128,
  `mask_truncated_completions=True`.
· Tối ưu: lr **1e-5** (LoRA), constant + 10 bước warmup, `max_grad_norm` 1, bf16, gradient
  checkpointing, cỡ lô 4 × tích luỹ 4 ⇒ **4 câu nhắc × 4 mẫu = 16 chuỗi/update**, **500 update**
  ⇒ **2.000 câu nhắc, đúng 1 epoch** trên tập thưởng. Hạt **101**. Điểm lưu mỗi 50 bước trên Drive.
· Ảnh: `min_pixels 200704 · max_pixels 1003520` (trùng SFT/ORPO/suy luận). Câu nhắc lấy **nguyên
  văn** từ `branches/s2.json` (trùng byte lúc dạy S2/MIN); khối ảnh đứng trước khối chữ, chữ bắt
  đầu bằng `"\n"` — đúng cách `infer_branch.py` đã kiểm *"chuỗi lúc chấm trùng lúc dạy"*.

### (x19b) Tập thưởng và hàm thưởng — nguyên văn, khoá
· Tập: **2.000 bước chạm** lấy ngẫu nhiên (seed 101) từ **41.090** = 41.099 bước có khai báo
  vàng trong `train_ac` **trừ 9** bước `point_norm` ngoài [0,1000]. `assert` không có episode
  tập kiểm. Danh sách khoá ghi `prompt_keys.json` trong thư mục ra.
· Vàng: `point_norm` (lưới 0–1000) của `train_ac/descriptors.jsonl`.
· **r_point = 1,0** nếu completion tách được đúng một khối `<desc>…</desc>` có `<point>x,y</point>`
  và |x−gx| ≤ 140 ∧ |y−gy| ≤ 140 (đúng `TAU` của cổng khai báo `gate_desc_acc.py`); 0 nếu không.
· **r_format = 0,2** nếu khối `<desc>` tách được **4 ô** (neo vào ô `<point>`; ô tên được chứa
  `|` — 67/41.090 tên vàng có `|`), sau `</desc>` là `"\n"` rồi câu **2–40 từ** không còn thẻ.
· **r_name = 0,1** nếu ≥1 token của ô tên (không phải từ dừng) xuất hiện trong câu.
· Tổng tối đa **1,3**. Không có phần thưởng nào gọi bộ trỏ. Không có phần thưởng độ dài.
· Selftest 0 GPU (`grpo_point.py --selftest`): khai báo vàng + câu bất kỳ đạt r_point 500/500,
  r_format 100/100 — đã chạy 5/9 trên WSL, ĐẠT.

### (x19c) Thăm dò 20 bước trên 50 câu nhắc DÀI NHẤT (luật P10) — ba tiêu chí, quyết TRƯỚC
① không OOM; ② `frac_reward_zero_std` trung bình **≤ 0,60** (≥40% nhóm có cả đúng cả sai);
③ `reward/r_point/mean` trong **[0,55; 0,95]** (≈0,75 là kỳ vọng từ 74,6% khai báo đúng).
Sửa được **đúng hai thứ, mỗi thứ một lần**, phải ghi (x19d): OOM ⇒ tích luỹ 4 → **2** (và 500 →
1.000 update để giữ 2.000 câu nhắc); ② > 0,60 ⇒ temperature 1,0 → **1,2**. Vẫn không đạt ⇒
**không chạy**, ghi kết quả thăm dò, nhánh đóng.

### (x19d) Sổ sửa đổi trong lượt (điền khi có)
_(trống — mọi thay đổi sau (x19c) ghi ở đây kèm giờ ICT và lý do)_

### (x19e) Cách đọc kết quả — khoá TRƯỚC
· Suy luận **greedy** trên 6.958 bước tập kiểm bằng `infer_branch.py` **không đổi tham số**, rồi
  chấm **một lần** bằng UGround trên đúng **4.463** bước chạm, `exec` Voronoi gated .14 (headline).
· Phép so chính: **GRPO/101 − MIN/101 (60,05)**, McNemar ghép cặp, KTC bootstrap. Đọc theo luật
  (x14b)/(x14c): **một hạt giống ⇒ nhãn "một hạt giống"**, chỉ gọi *tăng* khi Δ ≥ MDE **2,2** và KTC
  loại 0; dưới đó là TRẮNG dù dấu nào. **Kỳ vọng ghi trước: +2 … +4 pp.** Trên +5 ⇒ soi kỹ hơn
  bình thường (đối chiếu gate_desc_acc và BLEU trước khi tin).
· Thước phụ bắt buộc báo kèm: `gate_desc_acc.py` (độ chính xác khai báo, cơ học) · BLEU-4 /
  ROUGE-L với câu chuẩn theo `text_metrics.py` — **BLEU-4 giảm quá 1,0 so với MIN (mốc ở
  `report/141` §6) là dấu hiệu câu bị bẻ thành mật mã, phải khai và hạ kết luận** · `action_ok` ·
  D.3 và nL2 đồng-báo · tỉ lệ sinh `<desc>`.
· Hạt 202: **chỉ** chạy nếu GRPO/101 − MIN/101 ≥ 2,2; quyết ở (x20) trước khi nhìn số 202.
· Báo kết quả **dù ra sao**, kể cả âm. Không nới bất kỳ ngưỡng nào ở đây sau khi thấy số.

### (x19f) Không được
Thưởng bằng UGround (là bộ trỏ chấm) hay bất kỳ bộ trỏ nào · dùng dev 1.400 hoặc 3.062 làm tập
thưởng · chọn siêu tham số theo exec tập kiểm · thêm hạng thưởng sau khi thấy G4 · đổi
`infer_branch.py` lúc suy luận · so GRPO với S1/Base làm headline (headline là so MIN).
Mã: `harness/grpo_point.py` · runbook `harness/colab_grpo_point.md`.

**(x19d) — ghi 1:** G4 5/9 (ICT đêm): ① không OOM · ② zero-std **0,25** · độ dài 46,5 token ·
**44,3 s/bước** ở 50 câu nhắc dài nhất ⇒ 500 bước ≈ 6 h. ③ chưa đọc được vì ô đọc dùng sai tên
khoá metric (`reward/…` theo tài liệu, bản 0.29.1 in tên khác) — sửa **ô đọc** để tìm khoá chứa
`r_point`; **không đổi tham số huấn luyện nào**. Đồng thời tắt `log_completions` ở lượt thật (chỉ giữ
ở probe) để log còn đọc được — thay đổi về ghi log, không về thuật toán.

**(x19d) — ghi 2:** ③ đọc lại từ `log_history.json` của probe: `rewards/r_point/mean` trung bình
**0,591** trên 50 câu nhắc dài nhất (5 bước cuối 1,00/0,75/0,50/0,31/0,62) ⇒ **ĐẠT** cả ba tiêu chí
(x19c). Không sửa tham số nào. Lượt thật G5 được phép phóng với cấu hình (x19a) nguyên văn.

**(x19d) — ghi 3 (6/9, TRƯỚC khi có bất kỳ điểm `exec` nào của nhánh GRPO):** lượt G5 chạy trọn
**500/500 bước** (5,63 h). Khâu đọc kết quả và khâu suy luận chuyển từ Colab A100 sang **Kaggle
T4 miễn phí** (user quyết 6/9, lý do chi phí; runbook `harness/kaggle_grpo_point_6_9.md`). Ba
điều chỉnh, **không điều nào đụng thuật toán, thước hay ngưỡng**:

· **Phạm vi suy luận hẹp lại: 4.463 bước chạm thay vì 6.958 bước.** Lý do vật chất: dataset
  Kaggle `thesis-score` chỉ chứa 4.463 ảnh, ảnh của 2.495 bước không chạm nằm trong
  `test_images.tar` trên Drive. Điều này **không đổi con số headline** vì `history` trong câu
  nhắc là câu chuẩn của người (trùng nguyên văn 5.318/5.318) nên mỗi bước sinh độc lập với các
  bước khác; tập 4.463 cho kết quả y hệt như khi cắt ra từ lượt 6.958. **Cái mất phải khai:**
  lượt này **không đo được** hành vi ở bước không chạm, trong khi tập thưởng chỉ gồm bước chạm và
  MIN-DESC từng lộ giá **−19,75** đúng ở nhóm đó. Bù được bằng một lượt thêm (~1,7 h) nếu upload
  ảnh; **không** phải điều kiện của headline, và **không** được dùng sự vắng mặt của nó để chọn
  cách đọc có lợi.
· **Ô kiểm log của G7 có lỗi dò khoá** — nó tìm tên khoá chỉ trong bản ghi cuối `h[-1]`, mà bản
  ghi cuối của HF Trainer là dòng tổng kết không mang metric thưởng, nên in ra `bước: 0` và
  `0.0 → 0.0`. Sửa **ô đọc** (quét toàn bộ bản ghi, ô G7a + `harness/doc_grpo_local.py`, chạy
  0 GPU trên máy nhà). Cùng dạng đã ghi ở ghi 1; không đụng dữ liệu.
· **`pip uninstall torchao`** trên máy suy luận: `peft` bản mới do TRL 0.29.1 kéo theo ném
  `ImportError` khi thấy `torchao 0.10.0` có sẵn của Colab. Dự án không dùng torchao lần nào
  (4-bit là bitsandbytes). Gỡ, không nâng — nâng sẽ kéo theo torch đang pin bản CUDA.

Luật đọc (x19e) giữ nguyên từng chữ: headline vẫn `exec` Voronoi gated .14 so MIN 60,05, một hạt
giống, ngưỡng 2,2 pp, báo dù ra sao.

**(x19d) — ghi 4 (6/9, vẫn TRƯỚC mọi điểm `exec`):** đọc trọn `log_history.json` của lượt G5
(501 bản ghi = 500 bước + dòng tổng kết) và đo dịch chuyển trọng số, cả hai đều 0 GPU trên máy
nhà (`harness/doc_grpo_local.py`, tệp ở `runs/grpo_point/`). Số theo 5 chặng 100 bước:

| đại lượng | ch1 | ch2 | ch3 | ch4 | ch5 |
|---|---|---|---|---|---|
| `rewards/r_point/mean` | 0,686 | 0,702 | 0,709 | 0,758 | **0,758** |
| `reward` (tổng) | 0,946 | 0,960 | 0,967 | 1,018 | 1,023 |
| `rewards/r_name/mean` (trần 0,1) | 0,062 | 0,060 | 0,059 | 0,062 | 0,068 |
| `rewards/r_format/mean` (trần 0,2) | 0,198 | 0,198 | 0,199 | 0,198 | 0,198 |
| `frac_reward_zero_std` | 0,420 | 0,445 | 0,488 | 0,475 | **0,515** |
| `kl` | 0,0013 | 0,0017 | 0,0023 | 0,0030 | 0,0037 |
| `entropy` | 0,274 | 0,267 | 0,251 | 0,247 | 0,248 |
| `completions/mean_length` | 46,08 | 45,99 | 46,12 | 46,26 | 46,19 |

· **`r_point` tăng đơn điệu +0,072** (0,686 → 0,758) nhưng **chững hẳn ở 100 bước cuối**
  (+0,0006 giữa ch4 và ch5), trong khi `frac_reward_zero_std` bò từ 0,420 lên 0,515 và `entropy`
  giảm 0,274 → 0,248 ⇒ tín hiệu học đang cạn: hơn nửa nhóm G=4 cho cùng phần thưởng nên không
  còn gradient. Vẫn dưới ngưỡng dừng 0,60 của (x19c), nên lượt hợp lệ; nhưng **kéo dài quá 500
  bước ở cấu hình này khó mua thêm gì** — nếu về sau có lượt nữa thì phải đổi G hoặc temp, và đó
  là quyết định mới.
· **`r_format` bão hoà ngay từ đầu** (0,198/0,200) ⇒ định dạng không phải chỗ học được gì;
  **`r_name` gần như đứng yên** (+0,0055 trên trần 0,1). Toàn bộ mức tăng của `reward` đến từ
  `r_point`.
· **Độ dài câu sinh phẳng** (46,1 → 46,2 token) và `completions/clipped_ratio` = 0 ở cả 500 bước
  ⇒ chưa có dấu hiệu câu bị bẻ ngắn thành mật mã. **Không thay được phép kiểm BLEU-4 của (x19e)**,
  chỉ là dấu hiệu sớm cùng chiều.
· **`kl` cực nhỏ** (0,0037 ở cuối, β=0,04) ⇒ mô hình vẫn rất gần MIN.
· **Dịch chuyển trọng số:** `‖Δ‖/‖MIN‖` thô 1,067e-02, **sàn nhiễu cast 1,652e-03** (adapter train
  lưu bf16, bản `ref` lưu fp32), **dịch chuyển thật 1,054e-02** — gấp **6,4 lần** sàn, vượt mốc
  1e-2 của runbook. Lệch lớn nhất ở `layers.31.mlp.gate_proj.lora_B`.
⇒ **Đủ căn cứ chạy suy luận + chấm.** ⚠️ Nhắc để khỏi đọc quá: `r_point` đo trên **tập thưởng**
(2.000 câu nhắc bước chạm của tập dạy) bằng cửa sổ ±140, còn `exec` chấm bằng cách đưa **câu** cho
UGround và **không** đọc ô `<point>` của mô hình. +0,072 ở `r_point` vì vậy **không** quy thẳng
thành +7,2 pp `exec`; kỳ vọng ghi trước **+2 … +4 pp** của (x19e) giữ nguyên, không nới.

**(x19d) — ghi 5 (6/9, suy luận C1 XONG, `exec` CHƯA chấm — dự báo ghi TRƯỚC):** lượt Kaggle C1
sinh trọn **4.463/4.463** bước, 0,4 bước/giây, ~3,1 h, chữ ký `lora:grpo-point-adapter`, **0 câu
rỗng**, **0 câu sót `<desc>`**. `kiem_preds.py` đạt **6/8**; hai phép không đạt là ① và ③ (số bản
ghi 4.463 thay vì 6.958) — **đúng bằng phạm vi đã khai ở ghi 3**, không phải lỗi mới. Phép 5 đạt:
cả hai nhánh **không bỏ bước nào**, nên McNemar ghép cặp với MIN dùng được trọn 4.463.

**Thước phụ đo được ngay, 0 GPU:**
· **Cổng khai báo cơ học** (`gate_desc_acc.py`, giao 3.473 bước có tên vàng): tên đúng
  **67,0 → 69,5** (+2,51) · point đúng **71,8 → 74,0** (+2,22) · **cả hai đúng 60,6 → 63,2
  (+2,56 pp)**. Tỉ lệ sinh `<desc>` giữ **99,6%** ở cả hai nhánh.
· **Mức tăng dồn vào nhóm câu đã đổi**, không rải đều: 961/4.463 câu (**21,5%**) khác MIN; trên
  683 bước có tên vàng trong nhóm đó, "cả hai đúng" **43,3 → 52,4 (+9,08 pp)**, còn nhóm giữ
  nguyên câu chỉ **+0,97**. Nhóm đã đổi cũng là nhóm **khó hơn hẳn** (nền 43,3 so với 64,9).
· **Câu không bị bẻ thành mật mã:** BLEU-4 **37,86 → 37,78 (−0,09)** · ROUGE-L **68,40 → 68,47
  (+0,06)** · độ dài trung vị **34 ký tự ở cả hai** · số câu dưới 4 token **107 ở cả hai** · mở đầu
  bằng động từ chạm **93,8 → 94,3%**. Xa ngưỡng "giảm quá 1,0" của (x19e).
· **Chuyển giao train → test yếu hơn nhiều lần:** `r_point` trên tập thưởng tăng **+7,2 pp**
  (0,686 → 0,758) trong khi point đúng trên tập kiểm chỉ **+2,22 pp**, tức khoảng **31%**.
  ⚠️ Hai phép đo khác chế độ giải mã (train: lấy mẫu temp 1,0, G=4; kiểm: greedy) nên **không so
  thẳng mức tuyệt đối**; chỉ đọc theo chiều và bậc độ lớn.

**⭐ DỰ BÁO `exec`, ghi trước khi chấm:** hệ số chuyển đổi khai-báo→exec đo trên chính dữ liệu này
là **0,43** (§6.1 của `report/120`, từ cặp S2→MIN: +6,70 pp khai báo cho +2,87 pp exec). Ca đó là
can thiệp đổi **cả tên lẫn điểm** — cùng loại với lượt này (tên +2,51, point +2,22) — nên áp được,
khác ca "sửa tên chọn lọc" mà hệ số từng dự báo sai. ⇒ **+2,56 × 0,43 ≈ +1,10 pp**, tức `exec`
quanh **61,2%**; dải theo biên văn liệu 0,23–0,58 là **+0,59 … +1,49**.
⇒ **Dự báo này THẤP HƠN kỳ vọng +2 … +4 pp ghi ở (x19e)**, và **dưới MDE 2,2** ⇒ nếu đúng thì
verdict là **TRẮNG** và hạt 202 **không** chạy. Ghi rõ ở đây để khỏi chỉnh câu chữ sau khi thấy số:
· ra trong **+0,6 … +1,5** ⇒ khớp hệ số, TRẮNG, kết luận là "cơ chế có tác dụng ở tầng khai báo
  nhưng không đủ chuyển thành `exec`";
· ra **≥ +2,2** ⇒ vượt cả dự báo hệ số lẫn MDE, **phải soi kỹ hơn bình thường** trước khi tin
  (đối chiếu `action_ok`, D.3, nL2, và phân bố theo nhóm câu đã đổi);
· ra **âm** ⇒ báo âm, không viện dẫn mức tăng khai báo để làm nhẹ.

### (x20) Luật quyết SAU lượt GRPO — khoá 6/9, TRƯỚC khi có bất kỳ điểm `exec` nào

Viết trong lúc commit C2 đang chạy. Chủ luận văn quyết hai điều dưới đây khi chưa ai nhìn thấy
số. Không nới, không thêm ô thứ ba.

**(x20a) Nhánh so sánh cho đòn Đ1 — CHỈ chạy nếu `exec`(GRPO) − `exec`(MIN) ≥ +2,2 pp.**
Căn cứ: nhánh so sánh chỉ dùng để **quy công** một hiệu ứng; `exec` dưới MDE là ô TRẮNG, không có
gì để chia, nên chi tiền cho nó là mua một phép quy công cho hiệu ứng chưa chứng minh được là có.
· Nếu chạy, thiết kế **khoá luôn tại đây**: học tiếp từ **cùng điểm lưu MIN-DESC/101**, bằng
  **SFT cross-entropy** trên **đúng 2.000 câu nhắc của tập thưởng** (cùng seed 101, cùng danh
  sách), nhãn là target gốc của MIN-DESC, **1 epoch**, lr **1e-5** (bằng GRPO), lô hiệu dụng 16
  ⇒ **125 update**. Tên nhánh `min_ce_tiep_seed101`.
· Trục đối xứng là **cùng dữ liệu, cùng số câu nhắc nhìn thấy, khác mục tiêu**. ⚠️ Không đối xứng
  hoàn toàn: GRPO sinh G=4 chuỗi mỗi câu nhắc nên thấy 8.000 chuỗi, SFT thấy 2.000. Khai điều này
  mỗi lần trình bảng quy công, đừng lặng lẽ.
· Đọc: **Δ_grpo = `exec`(GRPO) − `exec`(min_ce_tiep)** là phần quy được cho *thuật toán GRPO +
  phần thưởng `<point>`*; phần còn lại thuộc về *việc học thêm*. Áp đúng luật bốn ô như mọi Δ khác.
· Nếu **không** chạy (tức `exec` < +2,2): luận văn **phải** ghi thẳng rằng không tách được công
  của GRPO khỏi công của việc học thêm 2.000 câu nhắc, kèm tiền lệ MIN vs CE2 (78–88% mức tăng
  thuộc nhánh so sánh). ⛔ Cấm dùng mức tăng ở cổng khai báo (+2,56 pp) để lấp chỗ đó.

**(x20b) Bước KHÔNG chạm — đo NGAY sau C2, vô điều kiện.** Chủ luận văn quyết đóng hạn chế này
thay vì để ngỏ. 2.495 bước, suy luận trên Kaggle T4 (~1,7 h, 0 đồng); khâu chấm là
`score_run.py --mode noharm --baseline runs/preds_min_desc_seed101.jsonl`, **không gọi bộ trỏ**
nên chạy được ở máy nhà, 0 GPU.
· Thước là **tỉ lệ khớp loại thao tác** (`canon_action` của câu mô hình so với câu chuẩn,
  `strict_back=True`), cộng *không đảo nghĩa* và *câu rỗng*.
· **Ngưỡng đã có sẵn từ mục 3 của bản gốc, dùng nguyên, không đặt ngưỡng mới:** nhánh có khai báo
  không được thấp hơn nhánh thường quá **3 điểm phần trăm**. Ở đây so **GRPO với MIN-DESC**.
· Kết cục: thấp hơn MIN quá 3 pp ⇒ **báo là tác hại ở bước không chạm**, và mọi chỗ trình `exec`
  của nhánh GRPO phải in kèm con số đó. Trong 3 pp ⇒ báo là không thấy tác hại, kèm n và KTC.
· ⛔ Kết quả của phép này **không** được dùng để đổi cách đọc `exec`, theo cả hai chiều.

**(x20c) Hạt giống 202** — giữ nguyên (x19e): chỉ chạy nếu `exec`(GRPO) − `exec`(MIN) ≥ 2,2 pp.
Nếu chạy thì **phải báo trung bình hai hạt bất kể ra sao**, theo cam kết (x8c).

**(x20d) Lượt GRPO tiếp theo (đổi G hoặc temp) là QUYẾT ĐỊNH MỚI.** `frac_reward_zero_std` đã lên
0,515 và `r_point` phẳng ở chặng cuối ⇒ cấu hình này đã cạn tín hiệu. Muốn đi tiếp phải mở mục
đăng ký mới, **không** được trình như phần tiếp diễn của (x19).
