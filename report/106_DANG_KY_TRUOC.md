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
