# Sổ kê khai: đã làm được gì, số nào tin được, tra ở đâu

> **Mục đích.** Chỗ duy nhất cần mở khi viết luận văn và cần kê khai công việc. Mỗi mục ghi:
> làm gì · kết quả bằng số · mã ở đâu · con số đó *dùng được tới đâu*.
>
> **Nguyên tắc của sổ này:** chỉ ghi thứ **đã chạy và đã kiểm**. Thứ mới lên kế hoạch nằm ở
> `report/106` (bản đăng ký trước). Số nào đã bị rút thì ghi vào mục 9 chứ không xoá, để không
> ai vô tình dùng lại.
>
> Cập nhật lần cuối: **6/8/2026**. Chưa huấn luyện mô hình nào, chưa tiêu đồng nào cho GPU.

---

## 1. Trạng thái một dòng

Toàn bộ phần **không tốn tiền** đã xong và đã kiểm: dữ liệu dạy 4 nhánh, tập kiểm 6.958 bước có
OCR, nhãn khai báo, và trọn đường ống huấn luyện → suy luận → chấm điểm. Thiết kế đã niêm phong
trong git trước khi chạy. Việc kế tiếp là khoản chi đầu tiên (cổng A, 4–8 đô).

---

## 2. Dữ liệu đã dựng

### 2.1. Tập dạy — 1.697 bước (lát thử; bản đầy đủ dựng trên máy thuê)

| | |
|---|---|
| Nguồn | AndroidControl (NeurIPS 2024), ghép hai bản HuggingFace: câu người viết (`HarrytheOrange/parsed_AndroidControl`) + ảnh (`ckg/AndroidControlParsedWithImages-20k`) |
| Quy mô đã dựng tại máy | 1.697 bước / 347 tác vụ / 843 MB (2 trong 76 shard) |
| Bước chạm có toạ độ | 1.075 (63,3%) — dựng được nhãn cho **1.074**; 1 ca điểm chạm nằm ngoài mọi hộp của cây trợ năng |
| **Kiểm phép ghép** | chữ OCR tại điểm chạm khớp câu chuẩn **47%**, đối chứng ghép-lệch-một-bước **27%** → chênh 1,7 lần, ghép chuẩn |
| Mã | `harness/build_train_data.py` |

### 2.2. Tập kiểm — 6.958 bước

| | |
|---|---|
| Quy mô | 6.958 bước / 1.432 tác vụ / 3,3 GB (9 shard, đủ) |
| **Bước chạm — đối tượng chấm** | **4.463** (64,1%) |
| Thao tác khác | cuộn 10,8% · chờ 7,3% · gõ chữ 7,1% · mở ứng dụng 6,8% · quay lại 3,9% |
| **Kiểm phép ghép** | khớp **37%** vs đối chứng lệch **10%** → chênh 3,7 lần, chắc hơn tập dạy |
| Rò rỉ với tập dạy | **0 tác vụ trùng** (kiểm 6/8) |
| ⚠️ Không phải app-unseen | 92% ứng dụng cũng có trong tập dạy **đầy đủ của AndroidControl** — xem mục 8. Tỉ lệ chính xác so với tập dạy *sẽ dùng* chỉ chốt được sau khi dựng xong dữ liệu trên máy thuê; `harness/tag_app_seen.py` tính lại |
| Gán được ứng dụng | **40,7%** số bước chạm (259 ứng dụng); còn lại thành cụm riêng từng tác vụ — xem mục 7.1, đây là chỗ quyết định lực thống kê |
| Mã | `harness/build_test_data.py` |

### 2.3. OCR — chạy trước cho cả hai tập

| | tập kiểm | tập dạy |
|---|---|---|
| Phủ | 6.969 bản ghi, phủ 6.958/6.958 bước của tập kiểm (100%) | đủ |
| Dòng chữ mỗi màn (trung vị) | 22 | 21 |
| Màn không đọc được chữ nào | 0,1% | 0,1% |
| Bước chạm có chữ gần điểm chạm | 41,4% | — |

Hai tập khớp phân bố — điều kiện cần, vì đầu vào lúc chấm và lúc dạy đi qua **cùng một hàm dựng
câu nhắc**. Bộ đọc: RapidOCR (ONNX, CPU). Chạy 6 luồng song song mất ~6 giờ (một luồng ~24 giờ).
Mã: `harness/prep_ocr_train.py` (`--split test`, `--shard/--nshard`, `--merge`).

---

## 3. Nhãn tầng khai báo

Dựng **hoàn toàn tự động**, không thuê người dán nhãn. Quy trình: toạ độ chạm thật → tra cây trợ
năng lấy hộp nhỏ nhất chứa điểm đó → vai trò từ cây → tên từ cây (qua cổng lọc) hoặc OCR → dấu
hiệu phân biệt tính bằng luật.

Kết quả trên 1.074 bước chạm:

| | |
|---|---|
| Tên rõ | **73,8%** (nguồn: OCR 599, cây trợ năng 224) |
| Chỉ ký hiệu lẻ | 2,8% |
| Không tên → để trống, không đoán bừa | **23,4%** |
| Vai trò rõ | 76,0% |
| **Ô toạ độ** | **sạch 100%** — lấy từ hành vi người thật |
| Có phần tử trùng tên trên màn (ca mơ hồ thật) | 7,0% |
| Dựng được khai báo giả cho nhánh mức 2 | 92,6% |

**Kiểm tính đúng (6/8):** toạ độ trong `<desc>` khớp `point_norm` **1074/1074** · điểm chạm nằm
trong hộp đã chọn **1074/1074** · không còn tên class Android lọt vào nhãn **0 ca**.

Hệ toạ độ: lưới **[0,1000]**, không dùng pixel thô — ảnh bị co lại trước khi vào mô hình nên pixel
gốc vô nghĩa nếu không kèm kích thước. Mã: `harness/descriptor_label_build.py`.

### 3.1. Ô "dấu hiệu phân biệt" — chỗ phải viết kỹ khi lên luận văn

Ô thứ tư của khai báo mang đúng cái tên của thành phần đóng góp, nên nó là chỗ dễ bị vặn nhất.
Rà lại 6/8 phát hiện bản đầu **rỗng nghĩa 92,7%**: 85,8% số nhãn chỉ ghi một con số đếm kiểu
*"1 trong 8 phần tử cùng loại"*, thứ báo là **có** mơ hồ chứ không nói gỡ bằng cách nào. Nguyên
nhân nằm ở thứ tự ưu tiên trong luật sinh — vế đếm đứng trước nên nuốt gần hết.

Đã xếp lại theo tiêu chí *vế nào gỡ được mơ hồ*, và thêm **mỏ neo chữ**: chuỗi OCR gần nhất bên
cạnh phần tử, kèm hướng — *"ngay dưới chữ «Create folder»"*.

| Nội dung ô | Bản đầu | **Bản dùng** |
|---|---|---|
| Mỏ neo chữ | — | **63,9%** |
| Trùng tên, kèm mỏ neo | — | 4,7% |
| Phần tử duy nhất trên màn | 7,3% | 7,3% |
| Trùng tên, không mỏ neo | 7,0% | 2,2% |
| Chỉ đếm số phần tử cùng loại | 85,8% | 21,9% |
| **Gỡ được mơ hồ** | **7,3%** | **75,9%** |

**Lý lẽ thiết kế, cần cho phần bảo vệ:** không chọn mô tả vị trí bằng lời (*"nửa dưới, bên phải"*)
dù nó phủ 100%, vì ô `<point>` đã ghi vị trí chính xác hơn — nói lại bằng lời không thêm thông tin
nào. Mỏ neo chữ thì **không suy ra được từ toạ độ**: nó là quan hệ với xung quanh, và đúng là thứ
tách được hai nút trông y hệt nhau.

**Ba luật lọc, đều có lý do đo được:** chuỗi phải nằm **ngoài** hộp phần tử (nằm trong hộp thì nó
chính là nhãn của phần tử, chỉ lặp lại ô TÊN) · không trùng tên phần tử · ít nhất hai ký tự
chữ-số (không có luật này thì lọt rác OCR một ký tự kiểu `α`, `S`). Kiểm hướng riêng:
**737/737 ca đúng chiều, 0 sai**.

**Vẫn phải khai khi trình:** còn 24,1% không gỡ được, và việc sửa nhãn **không phải bằng chứng**
rằng thành phần có tác dụng. Luật đọc kết quả không đổi — quy công cho tính phân biệt phải đi qua
S2-nopoint và S2r (`report/106` sửa đổi 6/8 e2 và f1).

---

## 4. Dữ liệu bốn nhánh thí nghiệm

Mọi nhánh dùng **cùng một đầu vào** (ảnh + mục tiêu + lịch sử + chữ OCR), chỉ khác đích sinh.

| Nhánh | Đích sinh | Độ dài đích trung bình |
|---|---|---|
| s1 | câu | 35,4 ký tự |
| s2 | `<desc>` thật + câu | 94,8 |
| s2r | `<desc>` **giả** + câu | 94,3 |
| s2_nopoint | `<desc>` bỏ ô toạ độ + câu | 79,1 |

**Kiểm bất biến, tất cả đạt** (chạy lại đủ sau mỗi lần dựng lại, gần nhất 6/8):

- Câu đem chấm của s2 / s2r / s2_nopoint trùng s1: **1697/1697** ở cả ba
- s1 không chứa khai báo: **0 ca**
- Số nhãn khai báo bằng nhau ở ba nhánh: **1074 / 1074 / 1074**
- s2_nopoint còn sót `<point>`: **0**
- s2 bỏ ô toạ độ đúng bằng s2_nopoint: **1697/1697**
- s2r khác s2 đúng ở các bước có khai báo: **1074/1074**
- Khai báo giả mức 2 trùng toạ độ đích: **0 ca**
- Bước không-chạm giữ đích y hệt ở mọi nhánh: **623/623** → phép kiểm không-gây-hại đọc được

**Ghép độ dài cho nhánh đối chứng — sửa 6/8.** Bản đăng ký ghi S2r ghép độ dài **token**, nhưng
mã ghép theo **ký tự**. Trung vị lệch 0 ký tự nghe rất khít; đo lại theo token thì chỉ **54,0%**
số cặp nằm trong 2 token, biên độ −17/+14. Trung bình vẫn ~0 nên đối chứng không lệch hệ thống,
song mã không làm đúng thứ đã đăng ký. Đã đổi sang ghép bằng bộ tách token của chính
`Qwen2.5-VL-3B-Instruct`:

| | trước | sau |
|---|---|---|
| Cặp lệch ≤ 2 token | 54,0% | **99,3%** |
| Biên độ | −17 / +14 | **−3 / +6** |
| Tổng token đích, S2 vs S2r | — | 54.021 vs 53.891 |

Sát tới mức không ai đổ được hiệu ứng cho chuyện "chuỗi đích dài thêm". Khai báo giả là một khai
báo **thật của màn khác**, toạ độ thay bằng số ngẫu nhiên — nên nó giống bản thật về hình thức và
chỉ sai về nội dung. Theo tra cứu, nhánh đối chứng kiểu này **chưa nghiên cứu nào từng chạy**.
Mã: `harness/build_branch_data.py`.

---

## 5. Đường ống huấn luyện → chấm điểm

| Khâu | Mã | Trạng thái |
|---|---|---|
| Cấu hình huấn luyện | `harness/train_config.yaml` | một file cho mọi nhánh, chỉ đổi 3 dòng `dataset`/`seed`/`output_dir` |
| Suy luận | `harness/infer_branch.py` | dùng **chung hàm dựng câu nhắc** với lúc dạy (import, không chép) |
| Chấm điểm + cổng A | `harness/score_run.py` | ba chế độ: `gate` (đo sai số bộ trỏ) · `score` (thước chính trên bước chạm) · `noharm` (thước phụ bắt buộc trên bước không-chạm, có `--baseline` tính hiệu số theo cặp). Bộ trỏ cắm rời, bootstrap gom cụm |
| Gắn nhãn ứng dụng đã-thấy-lúc-dạy | `harness/tag_app_seen.py` | phải chạy **sau** khâu dựng dữ liệu dạy, vì nhãn là hàm của tập dạy thật sự dùng |
| Nhánh B-infer | `harness/infer_branch.py --b-infer` | không huấn luyện; nhét danh sách phần tử của màn vào đầu vào lúc chạy |
| **S3-pilot (mức 2)** | — | ⚠️ **CHƯA CÓ MÃ.** Mới có dữ liệu (`desc_neg`, dựng được 995/1074 bước), chưa có hàm mất mát. Cố ý chưa viết: nằm sau cổng C, viết bây giờ thành thêm một đoạn mã chưa từng chạy. Không kịp làm thì phải khai là **nhánh đã đăng ký nhưng không chạy** |
| Hàm chấm từng bước | `harness/metric_exec.py` | có sẵn từ trước |
| Chạy trên máy thuê | `harness/run_on_rented.sh` | một lệnh, tự nối lại khi máy rẻ bị ngắt |

**Kiểm chạy được (cập nhật 6/8 sau vòng rà):**

- `infer_branch.py --selftest` — chạy trên CPU, ba phép: chuỗi lúc chấm **trùng lúc dạy từng
  ký tự** ĐẠT · số token ảnh trong đầu vào **1.272** ĐẠT · phép thứ ba (lô 1 vs lô n ra cùng
  câu) cần GPU, chạy trên máy thuê trước lượt chấm đầu.
- `score_run.py` chế độ **score** chạy đủ hai chiều: bộ trỏ trả None → 0,0% · bộ trỏ trỏ đúng
  (lệch 2% cạnh) → 100,0%.
- `metric_exec.py` tự kiểm nội bộ qua hết.
- Cây trợ năng phủ tập kiểm **200/200** bước mẫu, trung vị 70 phần tử mỗi màn; điểm chạm gần
  một phần tử trong danh sách **195/200**.
- Dữ liệu 4 nhánh và `descriptors.jsonl` trên đĩa **khớp đúng thứ mã hiện tại sinh ra** (kiểm
  bằng cách dựng lại vào thư mục tạm rồi so từng byte — cần vì mã đã sửa sau khi dựng).

⚠️ **Phép kiểm cũ đã bị lật, ghi lại để không lặp:** bản trước ghi *"câu nhắc lúc chấm khớp lúc
dạy 4/4 mục"*. Nó chỉ so **chuỗi ký tự**, không render qua chat template. Render ra thì đầu vào
có **0 token ảnh** — mô hình chạy mù. Bài học: kiểm phải đi tới đầu ra cuối của đường ống.

---

## 6. Thước đo và phần tự kiểm thước

**Cách chấm.** Đưa câu mô hình viết cho một bộ trỏ độc lập khác họ, chưa biết đáp án, đọc rồi chỉ
lên ảnh. Trỏ đúng phần tử người thật đã chạm thì tính đúng. **Không phải kiểu mô hình cho điểm**
— barem là toạ độ thật có sẵn trong dữ liệu, đúng sai rạch ròi.

**Luật chấm đã chốt bằng số (6/8).** Đo trần và sàn cả ba ứng viên trên 250 bước chạm của tập
kiểm:

| sai số bộ trỏ | đĩa dung sai | **ô-Voronoi tâm** | hộp-gần-nhất |
|---|---|---|---|
| 3% | 100,0% | **100,0%** | 78,6% |
| 8% | 100,0% | **74,4%** | 20,3% |
| **SÀN** (trỏ vào phần tử **khác** gần nhất) | **84,3%** | **2,8%** | 4,8% |

Chốt **Voronoi** vì SÀN, không vì trần: dải động ~97 điểm. Đĩa dung sai bị loại khỏi vai
headline — sàn 84,3% nghĩa là trỏ nhầm sang nút bên cạnh vẫn cho qua 84% số ca.

**Tự kiểm bằng bơm lỗi** (phương pháp Sai và cộng sự, EMNLP 2021), **chạy lại bằng đúng dụng cụ
sẽ chấm** — `harness/exec_injection_v3.py`, 398 bước của tập kiểm, giữ nguyên 10 ngưỡng đã khoá:

**Đạt 8/10**, nhưng hai tiêu chí rớt **khác** bản cũ:

1. ✔ *Kết oan câu đúng: 59,2% → **0,0%***. Đường cong cũng tốt hơn hẳn: lệch 3% → **0,0%** ·
   5% → 7,5% · 8% → 24,1% · 13% → 55,0%. Cổng A ở 3% có biên rộng hơn tưởng.
2. ✘ *Không phân biệt được lệch dưới ~63 px* (bắt 33,1%). Là **hành vi cố ý** của luật gộp 24dp,
   không phải lỗi — nút đích trung bình 189×126 px. Khai: thước đo được "trỏ nhầm sang nút
   khác", **không** đo được "trỏ hơi lệch trong cùng một nút".
3. ✘ *Luật từ ngược nghĩa ngoài bảng*: 20,0%, và chỉ n=15 — cỡ mẫu quá nhỏ để kết luận.

Khi trình phải in cột **n** cạnh mỗi tiêu chí: có tiêu chí n=755, có tiêu chí n=15.

Mã: `harness/exec_injection_v3.py` (bản dùng), `harness/exec_injection_validate.py` (bản 2, giữ
làm bản ghi — nó chấm bằng `hit_nearest_box` trên hộp OmniParser, **không** phải đường chấm thật).

---

## 7. Số đo nền — dùng để định vị bài toán

| Số | Giá trị | Đo thế nào | Dùng được tới đâu |
|---|---|---|---|
| **Bệnh chính: câu mơ hồ** | câu cộc lốc trỏ trúng **32%**, câu tả rõ **69%** | 76 câu chuẩn, chia đôi tại trung vị 8 từ, bộ trỏ gpt-4o-mini, dung sai 14% cạnh | n=38 mỗi nhánh → dấu hiệu chỉ hướng, chưa phải bằng chứng chắc |
| Tương quan độ dài–trúng | +0,327 | cùng phép đo trên | phải khai vì thước thiên vị câu dài |
| Lỗi bịa nút không tồn tại | **0–2%** | soi tay 40 ca | đủ để loại hướng chống-bịa |
| Chênh trần–sàn của thước ⚠️ | **số cũ, ĐỊNH NGHĨA KHÁC** — +44,7 / +32,9 / +19,7 | 76 bước, sàn = điểm khi KHÔNG đưa câu | **Đừng trích chung với bảng trần–sàn ở mục 6.** Bảng mục 6 định nghĩa sàn là *trỏ vào phần tử khác gần nhất*, đo trên 250 bước của tập kiểm, và đó mới là bảng dùng để chọn luật chấm |
| Cây trợ năng có tên | chỉ **12,6%** phần tử | đo trên 99.131 màn | lý do phải dùng OCR bù |
| Nhãn trợ năng là rác | **14,7%** tại nút đích | tự kiểm 6/8 | căn cứ của cổng lọc `clean_a11y` |
| Hình học màn | nút đích 189×126 px · nút khác gần nhất cách **69 px** | lát 76 bước | căn cứ đặt ngưỡng cổng A ở 3% (~32 px), có biên |
| **Sai số bộ trỏ rẻ** | **29,3%** bề ngang màn, phân vị 75 là 50,1%, **0 bước** vào nổi 3% | 10 bước tập kiểm, chạy thử 6/8, `score_run --mode gate --grounder openai` | gpt-4o-mini **không dùng để chấm được**; 4/10 lần nó trả đúng giữa màn tức đoán bừa |
| Phủ của thước trên tập kiểm | **4.452 / 4.463** bước chạm chấm được (99,8%), trung vị 69 phần tử mỗi màn | duyệt đủ tập kiểm qua `score_run.buttons_of` | không mất mẫu ở khâu này |

### 7.1. Lực thống kê — con số quyết định đọc được hay không

Đo trên đủ 4.463 bước chạm của tập kiểm. **59,3% bước không gán được app** (1.815/4.463 gán được,
259 app riêng biệt, 1.345 tác vụ), nên luật gộp cụm quyết định tất cả:

| Luật gộp cụm | G | G hiệu dụng (Kish) | MDE khi hai nhánh khác nhau 20% |
|---|---|---|---|
| Cụm-đơn — mỗi tác vụ không rõ app là một cụm | 1.091 | **454** | **5,9 pp** |
| Chỉ dùng 40,7% bước gán được app | 259 | **107** | **12,1 pp** |
| Bảo thủ — gom hết bước không rõ app vào một cụm | 260 | 3 | không dùng được |

Hiệu ứng kỳ vọng của thành phần là **+3…+11 pp, trung vị ~+5** — tức rơi đúng vào vùng mà kết
luận đổi theo luật gộp cụm. Vì vậy `report/106` sửa đổi 6/8 (e1) đã cam kết trước: Δ rơi vào
khoảng **4–9 pp** thì báo **chưa kết luận được**, không được chọn luật có lợi hơn.

---

## 8. Những chỗ đã bắt được lỗi — phần đáng viết vào luận văn nhất

Đây là mục nên đọc khi viết chương phương pháp: mỗi dòng là một lỗi **chạy vẫn trơn nhưng kết quả
sai**, tìm ra nhờ đi kiểm chứ không nhờ báo lỗi.

| Lỗi | Hậu quả nếu không bắt | Đã xử |
|---|---|---|
| **Cây trợ năng lồng nhau** — cha và con cùng mang một chữ | "trùng tên" thổi từ 30% xuống còn đúng 6,9%; và khai báo giả của nhánh mức 2 trỏ vào **chính nút đích** → nhánh đó vô hiệu mà vẫn chạy trơn | lọc hộp chồng nhau quá nửa diện tích |
| **Thiếu `seed` trong cấu hình** | giao thức hai hạt giống không có chỗ khai → chạy hai lần ra y hệt, cả lập luận chống nhiễu huấn luyện thành vô nghĩa | thêm `seed`, khoá 101/202/303 |
| **`val_size: held_out_by_app`** — ghi chú ý định bị viết nhầm vào chỗ tham số | không phải giá trị hợp lệ; chia ngẫu nhiên theo dòng sẽ rò rỉ vì màn cùng app na ná nhau | `val_size: 0.0`, việc chia làm ở khâu dựng dữ liệu |
| **Không có script suy luận, không có script chấm** | `metric_exec.py` hoá ra chỉ là thư viện hàm chấm từng bước; khâu cho ra con số headline chưa tồn tại | viết `infer_branch.py` + `score_run.py` |
| **Tập kiểm không phải app-unseen** | bản đăng ký cam kết app-unseen, thực tế 92% ứng dụng đã thấy lúc dạy → mốc so với gpt-4o-mini có lợi thế sân nhà | sửa mô tả, hạ mốc ngoài xuống tham khảo, gắn nhãn `app_seen_in_train` vào từng bản ghi |
| **11 bản ghi không có câu chuẩn** | tính vào mẫu số thành trừ điểm oan | loại khỏi tập kiểm |
| **Khai báo giả trùng tên nút đích 15,1%** | khoản phạt của mức 2 ép mô hình làm câu phụ thuộc toạ độ, không phụ thuộc dấu hiệu phân biệt | khai vào hồ sơ, tách nhóm này khi đọc kết quả mức 2 |
| **`pgrep -f` đếm cả chính nó** | cảnh báo "tiến trình chết" không bao giờ kêu | đổi sang kiểm tên tiến trình |
| **Hai bộ trỏ dùng sai câu nhắc** | UGround được huấn luyện với một câu nhắc tiếng Anh cố định, nhưng nhận câu tiếng Việt tự chế; gpt-4o-mini bị hỏi toạ độ pixel trên ảnh nguyên cỡ trong khi `ground_pilot.py` — nơi đẻ ra cặp 32%/69% — hỏi toạ độ chuẩn hoá 0-1000 trên ảnh thu về bề ngang 512. Cổng A sẽ ra số rác và bị đọc thành "bộ trỏ không đạt" | bê nguyên văn câu nhắc chính thức và quy ước cũ |
| **`resume_from_checkpoint: auto`** | LLaMA-Factory chỉ tự dò checkpoint gần nhất **khi trường này còn trống**; điền vào là tắt đúng cái định bật, rồi ném chuỗi `auto` cho Trainer như một đường dẫn. Máy thuê loại rẻ bị ngắt giữa chừng sẽ không chạy tiếp được — mất cả lượt đã trả tiền | bỏ hẳn dòng đó |
| **OCR rơi về một luồng trên máy tính tiền** | `run_on_rented.sh` gọi `prep_ocr_train.py` không chia mảnh: 64.500 ảnh tập dạy hết ~34 giờ thay vì ~5,7 giờ, card đồ hoạ nằm không suốt thời gian đó | chia mảnh theo `nproc` |
| **Kết quả OCR nằm ngoài git** | 6 giờ OCR tập kiểm đã chạy xong ở máy nhà nhưng máy thuê clone repo về sẽ không thấy và làm lại từ đầu | đưa `test_ac/ocr.jsonl` + `test.jsonl` + `train_ac/ocr.jsonl` vào repo; `setup` kiểm tra có sẵn thì bỏ qua |
| **"Sai số bộ trỏ rẻ = 8% cạnh" là số đã lọc bỏ phần hỏng** | số này đẻ từ `real_offsets()` (`exec_injection_validate.py:144`) — **chỉ lấy các ca bộ trỏ ĐÃ trúng dung sai** rồi mới tính trung vị. Nó lan vào report/98, report/100, report/107 và hai chỗ trong `score_run.py`, và làm khoảng cách tới cổng A trông gần hơn thực tế khoảng 3,5 lần. Nếu tin nó thì sẽ đọc kết quả cổng A sai chiều | rút; dùng số không lọc: 15,0% (công thức `ground_pilot`, n=76) và 29,3% (công thức cổng A, n=10 tập kiểm) |
| **Hai công thức sai số cùng gọi là "phần trăm"** | `ground_pilot` tính `hypot(dx/W, dy/H)` — lệch dọc chia cho chiều CAO nên nhẹ đi 2,2 lần; cổng A tính `dist(p,g)/W`. Chênh **1,63 lần** trên cùng dữ liệu. Trộn hai số là so nhầm | ghi rõ công thức cạnh mỗi con số; ngưỡng 3% neo theo công thức cổng A vì nó suy ra từ "phần tử khác gần nhất cách 69 px" |
| **Luật gộp cụm chưa xác định, mà MDE lại phụ thuộc hẳn vào nó** | bản đăng ký ghi "gom cụm theo ứng dụng" nhưng **59,3% bước không gán được app**, và không nói xử nhóm đó ra sao. Luật cụm-đơn cho G hiệu dụng 454 (MDE 5,9 pp); luật app-only cho 107 (MDE 12,1 pp). Con số "MDE 4–7 pp" và con số "G hiệu dụng ~98" từng đứng cạnh nhau như cùng một phép tính — thực ra thuộc hai luật khác nhau. Nếu để hở, sau khi có điểm sẽ tự chọn luật có lợi | chốt luật chính + bắt buộc phân tích nhạy cảm; cam kết trước: Δ rơi vào 4–9 pp thì báo **chưa kết luận được** (`report/106` sửa đổi 6/8 e1) |
| **Nhãn `app_seen_in_train` không có mã sinh ra** | trường này nằm sẵn trong `test.jsonl` và được `score_run` ghi ra vết để cắt lát phụ, nhưng grep cả repo không thấy dòng nào tính nó — do một lượt vá tay để lại. Không tái lập được thì không kiểm được, và nó **không tự sửa theo tập dạy thật**: đối chiếu với lát dạy đang có thì 2.136/3.130 bản ghi mâu thuẫn | viết `harness/tag_app_seen.py`, nối vào `run_on_rented.sh` ngay sau khâu dựng dữ liệu; phân biệt rõ `None` = *không gán được app* (55,0%) chứ không phải *chưa thấy* |
| **Thước phụ BẮT BUỘC không có mã chạy** | `report/106` mục 3 đăng ký phép kiểm không-gây-hại trên bước không-chạm, nhưng `score_run --mode score` lọc sẵn chỉ còn bước chạm. Tới lúc trình sẽ không có số — đúng loại lỗi đã bắt ngày 5/8 với script suy luận và script chấm | thêm `--mode noharm` dùng đúng hàm `canon_action` của thước chính, có `--baseline` tính hiệu số theo cặp; kiểm bốn chiều bằng dự đoán dựng sẵn: 100,0% / 53,3% / RỚT −46,7% / ĐẠT +0,0% |
| **Cờ `--selftest-batch` được hướng dẫn dùng nhưng không tồn tại** | phép tự kiểm thứ ba (lô 1 vs lô n — phép bắt lỗi đệm sai bên) in ra dòng bảo chạy `--selftest-batch`, mà `argparse` không có cờ đó. Làm theo hướng dẫn sẽ nhận `unrecognized arguments` rồi bỏ qua, và **tưởng đã kiểm**. Đệm sai bên là lỗi không báo gì, chỉ làm điểm tụt không đều theo thứ tự bản ghi | cài `selftest_batch()` + cờ; nối vào `run_on_rented.sh` bước `infer`, rớt thì dừng hẳn |
| **B-infer định nghĩa mơ hồ đủ để đẻ ra kết luận sai** | hồ sơ đọc được thành hai thí nghiệm: nhét khai báo của **đúng nút đích** (có lời giải sẵn) hay nhét **danh sách phần tử** (so công bằng). Cách thứ nhất trùng với phép thử TRẦN đã đăng ký riêng, và luật đọc kết quả đã khoá — *"B-infer bằng S2 thì huấn luyện mất lý do tồn tại"* — **chỉ đúng dưới cách thứ hai** | chốt cách thứ hai, ghi vào `report/106` sửa đổi 7/8 mục c; cài `--b-infer` |
| **Danh sách phần tử của B-infer toàn khung chứa** | bản đầu cho ra `(không tên) <point>500,500</point>` lặp lại — tâm các khung phủ gần hết màn đều rơi vào giữa. Đúng lỗi hộp lồng nhau đã bắt ở khâu dựng nhãn, lặp lại ở chỗ mới | lọc hộp lớn hơn 25% màn + gộp trùng tâm + ưu tiên phần tử có tên: tỉ lệ có tên **14,1% → 40,0%** |
| **Ô "dấu hiệu phân biệt" rỗng nghĩa 92,7%** | đếm đủ 1.074 nhãn: **85,8% chỉ đếm** ("1 trong 8 phần tử cùng loại"), 7,0% báo có mơ hồ mà không nói cách gỡ, chỉ **7,3%** thật sự gỡ được. Mà đây là ô mang tên của chính thành phần đóng góp. Không bắt thì rất dễ quy công cho "tính phân biệt" trong khi hiệu ứng thật đến từ ô toạ độ | xếp lại thứ tự luật sinh + thêm mỏ neo chữ → gỡ được **75,9%** (mục 3.1); luật đọc kết quả **không nới**: cấm quy công cho tính phân biệt, việc quy công chuyển sang S2-nopoint và S2r (`report/106` sửa đổi 6/8 e2 + f1) |
| **S2r ghép độ dài theo ký tự trong khi đăng ký ghi token** | mất mát tính trên token, nên "độ dài" cần ghép là token. Đo lại: chỉ **54,0%** cặp nằm trong 2 token, biên độ −17/+14 — trong khi tính theo ký tự thì trung vị lệch 0, nghe như đã khít. Trung bình ~0 nên không lệch hệ thống, nhưng mã không làm đúng thứ đã đăng ký | ghép bằng bộ tách token của `Qwen2.5-VL-3B`: **99,3%** cặp trong 2 token, biên −3/+6 |

---

## 9. Quyết định đã chốt, và số đã bị rút

### Chốt

| Ngày | Quyết định | Nơi ghi |
|---|---|---|
| 1/8 | Thành phần đóng góp: "mô tả phân biệt trước, phát ngôn sau", hai mức | `report/103` |
| 5/8 | **Niêm phong thiết kế** bằng bản đăng ký trước, thay vai trò buổi chốt với thầy | `report/106`, commit `51ddb35` |
| 5/8 | **Bác** việc đảo nguồn tên sang OCR-trước; áp cổng lọc A′ thay vào đó | `report/106` mục sửa đổi + `report/107` |
| 6/8 | Sửa mô tả tập kiểm, hạ mốc ngoài xuống tham khảo | `report/106` mục sửa đổi |

### Số đã bị rút — **cấm dùng lại**

- "MDE 4,4–6,0 là số chốt" — là số ước chiếu, phải đo lại từ kết quả S1 thật
- "8/10 bơm lỗi" mà không kèm hai tiêu chí rớt
- "31 bước mỗi ứng dụng" — chia sai quần thể
- "GCoT chứng minh định-vị-trước làm câu kém đi" — chỉ đúng ở chế độ ra lệnh, không đúng khi huấn luyện
- "câu cộc 35% vs câu rõ 69%" — số đúng là **32/69**
- "−42,8 là số của bài GCoT" — số tự tính từ hai bảng; bài viết 45,4
- "UI-Ins: −3,2 vs +4,7" ghép thành một cặp — hai mô hình nền khác nhau
- **"Bộ trỏ rẻ lệch trung vị 87 px, tức 8% cạnh"** — trung vị tính **chỉ trên các ca đã trúng dung sai**, tức đã loại hết phần trượt. Số không lọc: 15,0% (công thức `ground_pilot`) / 29,3% (công thức cổng A). Chính `report/98` dòng 388 đã ghi 256 px, chỏi với dòng 390 ghi 87 px
- **Đường cong kết oan "3% → 2,6% · 5% → 25% · 8% → 42% · 13% → 60%"** — đo trên hộp OmniParser với luật hộp-gần-nhất, không phải dụng cụ sẽ chấm. Số của dụng cụ thật (cây trợ năng + Voronoi): 3% → 0% · 5% → 7,5% · 8% → 24,1% · 13% → 55%
- "GuideMe không đụng toạ độ" — có, GPT-5 trả toạ độ trực tiếp
- "tập kiểm app-unseen 631 tác vụ" — không áp dụng cho dữ liệu đang dùng (mục 8)

---

## 10. Tài liệu — mở cái nào khi cần gì

| Cần gì | Mở |
|---|---|
| Kế hoạch đầy đủ, đã qua phản biện | `report/103_CHOT_THANH_PHAN.md` |
| Trình bày với thầy (15 phút) | `report/104_SCRIPT_GAP_THAY.md` + `LUAN_VAN_SLIDE_v9.pptx` |
| Nguồn từng con số trích dẫn, kèm ảnh bảng gốc | `report/105_NGUON_SO_BANG_GOC.md` |
| **Thiết kế đã khoá + luật đọc kết quả** | `report/106_DANG_KY_TRUOC.md` |
| Vì sao không đảo nguồn tên | `report/107_DEBATE_NGUON_TEN.md` |
| Đã làm được gì (file này) | `report/108_DA_LAM_DUOC_GI.md` |

---

## 11. Việc kế tiếp

| # | Việc | Tiền | Chặn ở đâu |
|---|---|---|---|
| ~~1~~ | ~~Thử đường ống bằng bộ trỏ rẻ~~ — **XONG 6/8**, 10 bước, ~0,002 đô | — | đường ống chạy thông; bộ trỏ rẻ lệch 29,3%, không chấm được |
| 2 | **Cổng A** — đo sai số bộ trỏ chuyên | 4–8 đô | cần GPU; quyết định thước chính có dùng được không |
| 3 | Huấn luyện S1 × 2 hạt giống → chấm đủ → **MDE thật** → khoá ngưỡng | 26–34 đô | trình tự cứng, không đảo |
| 4 | Huấn luyện S2 × 2 hạt giống → chấm | 26–32 đô | |
| 5 | S2r, S2-nopoint, B-infer | 26–32 đô | |
| 6 | Thử mức 2 trên lát nhỏ | 3–6 đô | |
| 7 | Chấm tay 100 câu (2 người) · demo tiếng Việt · kiểm không-gây-hại | 0–2 đô | |

Tổng phần chắc chắn **85–112 đô**, dưới ngân sách 200.
---

## 12. Phần free đã chạy hết — trạng thái sẵn sàng, và những gì còn chưa biết

Chốt 6/8 sau ba vòng rà. Mục này để trả lời đúng một câu: **cái gì đã kiểm bằng cách chạy thật,
cái gì mới chỉ là tin tưởng.**

### Đã kiểm bằng cách chạy, tin được

| Hạng mục | Bằng chứng |
|---|---|
| Mọi script trong `harness/` parse được | chạy đủ |
| OCR phủ tập kiểm | 6.958/6.958 bước, 0 thiếu, 0 trùng, 0,1% ảnh không ra chữ |
| Dữ liệu 4 nhánh khớp đúng thứ mã hiện tại sinh ra | dựng lại vào thư mục tạm rồi so từng tệp |
| Nhãn khai báo khớp mã hiện tại | so MD5 sau khi dựng lại |
| Bảy bất biến của bốn nhánh | đạt cả bảy |
| Hướng của mỏ neo chữ | 737/737 đúng chiều |
| `metric_exec` tự kiểm nội bộ | đạt |
| `score_run` chế độ chấm, hai chiều | bộ trỏ trả None → 0,0% · trỏ đúng → 100,0% |
| Câu nhắc lúc suy luận trùng lúc dạy | so chuỗi đã dựng, khớp từng ký tự, 1.272 token ảnh |
| Bơm lỗi bản 3 trên dụng cụ thật | 8/10, hai chỗ rớt đã khai |
| Mọi khoá trong `train_config.yaml` | đối chiếu mã nguồn LLaMA-Factory: 0 khoá lạ, giá trị hợp lệ |
| Đường ống chấm chạm được bộ trỏ thật | chạy 10 bước qua API, ghi vết đủ trường |

### Chưa kiểm được — chỉ biết khi chạy trên máy có GPU

1. `train_config.yaml` **chưa từng chạy** qua LLaMA-Factory. Đã đối chiếu từng khoá với mã nguồn
   nên chắc hơn nhiều, nhưng đối chiếu không thay được một lượt chạy.
2. Phép tự kiểm thứ ba của `infer_branch.py` — *lô 1 và lô 8 có ra cùng một câu không* — cần GPU.
   Phải chạy `--selftest-batch` **trước lượt chấm đầu tiên**.
3. `UGround` **chưa được nạp lần nào**. Câu nhắc nay đã bê nguyên văn bản chính thức, nhưng cách
   nó trả toạ độ và hành xử thật thì chưa ai thấy.
4. `run_on_rented.sh` chưa chạy trên máy thuê nào.

### Rủi ro lớn nhất còn lại, xếp theo mức

1. **Bộ trỏ chuyên có đạt cổng A không.** Hồ sơ cũ tưởng bộ trỏ rẻ cách ngưỡng 8%/3%; thực tế
   29,3%/3%. UGround mạnh hơn nhiều nhưng chưa ai đo nó trên bộ dữ liệu này. Rớt cổng thì xử theo
   bậc thang ở `report/106` mục 8, **không nới ngưỡng sau khi nhìn số**.
2. **Hiệu ứng rơi vào vùng 4–9 pp** — kết luận đổi theo luật gộp cụm, phải báo là chưa kết luận
   được (mục 7.1).
3. **Thước không phân biệt được lệch dưới ~63 px** (bơm lỗi bắt được 33,1%). Đây là hành vi cố ý
   của luật gộp phần tử, nhưng phải khai: thước đo được *trỏ nhầm sang nút khác*, **không** đo
   được *trỏ hơi lệch trong cùng một nút*.
