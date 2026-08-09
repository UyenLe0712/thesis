# Sổ kê khai: đã làm được gì, số nào tin được, tra ở đâu

> **Mục đích.** Chỗ duy nhất cần mở khi viết luận văn và cần kê khai công việc. Mỗi mục ghi:
> làm gì · kết quả bằng số · mã ở đâu · con số đó *dùng được tới đâu*.
>
> **Nguyên tắc của sổ này:** chỉ ghi thứ **đã chạy và đã kiểm**. Thứ mới lên kế hoạch nằm ở
> `report/106` (bản đăng ký trước). Số nào đã bị rút thì ghi vào mục 9 chứ không xoá, để không
> ai vô tình dùng lại.
>
> Cập nhật lần cuối: **9/8/2026**. Chưa huấn luyện mô hình nào. Chưa tiêu đồng nào cho GPU —
> cổng A và toàn bộ phần tiền trạm chạy trên GPU **miễn phí** của Kaggle.

---

## 1. Trạng thái một dòng

**Cổng A đã ĐẠT và toàn bộ đường ống đã chạy thật ít nhất một lần — vẫn chưa tiêu đồng nào.**

Dữ liệu dạy 4 nhánh, tập kiểm 6.958 bước có OCR, nhãn khai báo, đường ống huấn luyện → suy luận
→ chấm điểm: tất cả đã dựng và đã chạy. Thiết kế niêm phong trong git trước khi chạy. Bốn mắt
xích từng chỉ tồn tại trên giấy — cổng A, tự kiểm lô, sinh câu, chấm điểm — nay đều có vết chạy
thật, làm trên T4 miễn phí của Kaggle thay vì máy thuê.

Hai con số định vị mọi kết quả về sau: **sai số bộ trỏ trung vị 0,7%** (ngưỡng 3%) và **trần của
thước 70,0%**. Việc kế tiếp là khoản chi đầu tiên và cũng là khoản lớn nhất: huấn luyện S1.

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
| **Bộ lọc 11 bản ghi rỗng không nằm trong mã dựng** | `build_test_data.py` chỉ bỏ bước không có trong bảng câu chuẩn, **không** bỏ bước có câu chuẩn RỖNG — 11 bản ghi đó bị loại bằng một lượt vá tay. Dựng lại ở máy khác sẽ ra **6.969 chứ không phải 6.958**, đủ để mẫu ngẫu nhiên 300 bước của cổng A lệch khỏi tập đã đăng ký, mà lệch thì không ai thấy | đưa luật lọc vào `build()`; thêm sẵn khoá `app_seen_in_train` để bản ghi đủ trường ngay từ đầu |
| **bf16 ép cứng ở ba chỗ nạp mô hình** | T4 (Turing) và P100 (Pascal) — hai card của Colab/Kaggle bản miễn phí — **không hỗ trợ bf16**. Chạy ở đó sẽ lỗi hoặc rơi vào đường giả lập chậm khủng khiếp, rồi kết quả bị đọc nhầm thành "bộ trỏ kém". Cũng chính vì tưởng phải có bf16 mà cả kế hoạch mặc định là **phải thuê máy** | `pick_dtype()` tự dò rồi lùi về fp16; mở đường chạy cổng A miễn phí. **Bản vá đầu SAI, xem dòng dưới** |
| **Bản vá bf16 hỏi nhầm chỗ** | `pick_dtype()` hỏi `torch.cuda.is_bf16_supported()`, mà PyTorch đời mới **tính cả đường giả lập** nên trả `True` cho cả T4 — đo thẳng trên Kaggle ngày 9/8: `Tesla T4 · bf16: True`. Bản vá vừa viết hôm trước để mở đường chạy miễn phí lại tự vô hiệu hoá đúng ở chỗ nó sinh ra để phục vụ, và vô hiệu **im lặng**: mô hình vẫn nạp, vẫn sinh câu, chỉ chậm và có nguy cơ số lệch | hỏi đời kiến trúc thay vì hỏi thư viện: `get_device_capability()[0] >= 8` (bf16 chạy thật từ Ampere). `kaggle_precheck.py` in cả hai để đối chiếu |
| **Mẫu 300 bước của cổng A lấy từ một tập kiểm khác** | `run_on_free_gpu.md` hướng dẫn dựng `--shards 2` với chú thích "đủ cho 300 bước". Sai: mẫu lấy bằng cách xáo **toàn bộ 4.463 bước chạm** với hạt giống 20260805 rồi cắt 300 đầu, nên tập kiểm ngắn hơn cho ra mẫu khác hẳn tập đã đăng ký. Chương trình vẫn chạy trơn và vẫn in ra một con số trông bình thường | sửa hướng dẫn thành đủ 9 shard; viết `harness/kaggle_precheck.py` kiểm ba thứ trước khi tốn quota GPU: tập kiểm có đúng 6.958/4.463 không, mẫu xáo ra có trùng bản đã đăng ký không (kiểm cả bản ghi đầu lẫn cuối, bắt luôn khả năng bản Python xáo khác đi), và 300 ảnh đó có đủ không |
| **Cờ `--selftest-batch` được hướng dẫn dùng nhưng không tồn tại** | phép tự kiểm thứ ba (lô 1 vs lô n — phép bắt lỗi đệm sai bên) in ra dòng bảo chạy `--selftest-batch`, mà `argparse` không có cờ đó. Làm theo hướng dẫn sẽ nhận `unrecognized arguments` rồi bỏ qua, và **tưởng đã kiểm**. Đệm sai bên là lỗi không báo gì, chỉ làm điểm tụt không đều theo thứ tự bản ghi | cài `selftest_batch()` + cờ; nối vào `run_on_rented.sh` bước `infer`, rớt thì dừng hẳn |
| **B-infer định nghĩa mơ hồ đủ để đẻ ra kết luận sai** | hồ sơ đọc được thành hai thí nghiệm: nhét khai báo của **đúng nút đích** (có lời giải sẵn) hay nhét **danh sách phần tử** (so công bằng). Cách thứ nhất trùng với phép thử TRẦN đã đăng ký riêng, và luật đọc kết quả đã khoá — *"B-infer bằng S2 thì huấn luyện mất lý do tồn tại"* — **chỉ đúng dưới cách thứ hai** | chốt cách thứ hai, ghi vào `report/106` sửa đổi 7/8 mục c; cài `--b-infer` |
| **Danh sách phần tử của B-infer toàn khung chứa** | bản đầu cho ra `(không tên) <point>500,500</point>` lặp lại — tâm các khung phủ gần hết màn đều rơi vào giữa. Đúng lỗi hộp lồng nhau đã bắt ở khâu dựng nhãn, lặp lại ở chỗ mới | lọc hộp lớn hơn 25% màn + gộp trùng tâm + ưu tiên phần tử có tên: tỉ lệ có tên **14,1% → 40,0%** |
| **Ô "dấu hiệu phân biệt" rỗng nghĩa 92,7%** | đếm đủ 1.074 nhãn: **85,8% chỉ đếm** ("1 trong 8 phần tử cùng loại"), 7,0% báo có mơ hồ mà không nói cách gỡ, chỉ **7,3%** thật sự gỡ được. Mà đây là ô mang tên của chính thành phần đóng góp. Không bắt thì rất dễ quy công cho "tính phân biệt" trong khi hiệu ứng thật đến từ ô toạ độ | xếp lại thứ tự luật sinh + thêm mỏ neo chữ → gỡ được **75,9%** (mục 3.1); luật đọc kết quả **không nới**: cấm quy công cho tính phân biệt, việc quy công chuyển sang S2-nopoint và S2r (`report/106` sửa đổi 6/8 e2 + f1) |
| **Cache parquet không bao giờ được giải phóng** | `hf_hub_download` giữ lại mọi shard đã tải. 76 shard parquet ~67 GB, mà ảnh PNG bung ra cũng ~67 GB — hai thứ cùng nằm trên đĩa là ~134 GB, cộng tập kiểm và cache mô hình thành ~157 GB. Trên máy thuê container 200 GB thì đó là **hết đĩa giữa chừng, sau khi đã trả tiền cho mấy tiếng tải về** | xoá parquet ngay sau khi đọc xong từng shard, theo `realpath` để xoá cả khối dữ liệu chứ không chỉ liên kết mềm; đỉnh đĩa **134 GB → 70 GB**, container 100 GB là đủ |
| **Không có git remote, mà `run_on_rented.sh` giả định `git clone`** | máy thuê không có cách nào lấy mã về. Phát hiện lúc rà, trước khi thuê | đóng gói `thesis_rented.zip` 2,7 MB chuyển bằng `scp`, mang theo cả kết quả OCR tập kiểm 14 MB để khỏi chạy lại 6 giờ OCR trên máy tính tiền |
| **Ô thứ tư của khai báo GIẢ là hằng số** | `desc_neg` ghi `"phần tử hàng xóm"` ở **994/995 = 99,9%** bản ghi, khai báo thật không bao giờ mang chuỗi đó (trùng 0/995; mỏ neo chữ 68,6% so với 0%). Khoản phạt lề của S3-pilot khi đó chỉ dạy mô hình **dò một chuỗi**, không cần nhìn ảnh — mà lề vẫn đẹp nên con số trông y như thành công | tính bằng đúng hàm dùng cho khai báo thật, chạy trên chính phần tử hàng xóm. Sau khi vá: mỏ neo 80,8% vs 74,0% · đếm 17,9% vs 23,6% · không còn chuỗi hằng nào. Bốn nhánh dựng lại: **nội dung không đổi một mẫu** |
| **`build_test_data` ghi đè `test.jsonl` mà nhãn khai báo dựng từ bản cũ** | trong runbook Colab, ô dựng tập kiểm chạy **sau** khi đã bung nhãn khai báo mang theo. Hai bản lệch một bản ghi thì phép thử TRẦN lặng lẽ phủ thiếu — vẫn chạy, vẫn ra số, chỉ là số của một tập nhỏ hơn | thêm ô đối chiếu ba con số ngay sau đó: 6.958 bước · 4.463 bước chạm · nhãn phủ ~99,7% |
| **OCR song song không ghim luồng — càng nhiều lõi càng chậm** | `run_on_rented.sh` chạy `nproc` tiến trình RapidOCR, mà ONNX Runtime mặc định lấy **hết số lõi** cho phần tính trong một phép. Trên máy 32 lõi thành 32 tiến trình × 32 luồng = hơn 1.000 luồng tranh 32 lõi. Nhìn vào chỉ thấy "OCR lâu hơn dự tính", mà lâu ở đây là tiền vì card nằm không. Ước tính "32 lõi = 1,1 giờ" khi đó sai hẳn | ghim `OMP_NUM_THREADS=1` (đặt **trước** khi onnxruntime nạp) + `RapidOCR(intra_op_num_threads=1)`; song song ở mức tiến trình |
| **Số tiến trình OCR lấy đúng bằng số lõi, không nhìn RAM** | mỗi tiến trình RapidOCR ăn ~0,5–1 GB. Máy nhiều lõi ít RAM sẽ hết bộ nhớ giữa chừng, mà OOM ở đây giết cả lượt và phải chạy lại từ đầu | `NP = min(số lõi, RAM trống/2, 24)`, in ra để biết đã chọn gì |
| **`pyyaml` không có trong danh sách cài, mà lệnh `train` cần** | bước sinh cấu hình cho từng nhánh dùng `import yaml`. Ảnh nền PyTorch trơn không chắc có sẵn — hỏng ở đúng lúc bắt đầu lượt train đầu tiên | thêm vào `pip install` của `setup` |
| **Không có phép kiểm máy trước khi làm việc dài** | thuê nhầm máy 2 card thì LLaMA-Factory tự nhân cỡ lô lên; đĩa thiếu thì chết sau vài giờ tải. Cả hai biết được trong 5 giây | `setup` kiểm số card (≠1 thì dừng hẳn) và đĩa trống (<90 GB thì dừng), in kèm số lõi |
| **Bước 6 của trình tự cứng — phép thử TRẦN — không có mã** | `run_on_rented.sh` không có lệnh, `infer_branch.py` không có chế độ. Chỗ thứ tư cùng loại (sau script suy luận, script chấm, thước không-gây-hại). Tới lúc cần thì hoặc bỏ một thí nghiệm đã đăng ký, hoặc viết mã mới giữa lúc máy đang tính tiền | cài `--split test` cho khâu dựng nhãn (99,7% bước chạm dựng được) + `--ceiling gold\|filler` + lệnh `ceiling`; đệm ghép theo TOKEN, 120/120 lệch ≤2 |
| **Tập kiểm không ghi w/h, mà 4,75% ảnh không phải 1080×2400** | khâu dựng nhãn mặc định cứng 1080×2400. Có cả 1440×3120 và 1080×2340 trong tập kiểm, nên ô `<point>` của nhóm đó bị tính sai mà không báo gì | đọc kích thước thật từ tệp ảnh khi dựng nhãn cho tập kiểm |
| **Khai báo giả của S3-pilot tách được bằng một chuỗi cố định** | ô thứ tư của `desc_neg` là hằng số `"phần tử hàng xóm"` ở **994/995 = 99,9%** bản ghi, còn khai báo thật không bao giờ mang chuỗi đó (trùng 0/995; mỏ neo chữ 68,6% so với 0%). Khoản phạt lề sẽ chỉ dạy mô hình dò một chuỗi, không dạy tính phân biệt — mà lề vẫn đẹp, nên con số trông như thành công | tính ô thứ tư của khai báo giả bằng **đúng hàm đã dùng cho khai báo thật**, chạy trên phần tử hàng xóm. Phải sửa trước khi dựng dữ liệu đủ trên máy thuê. S2r không dính vì nó bốc khai báo từ màn KHÁC |
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
| ~~1~~ | ~~Thử đường ống bằng bộ trỏ rẻ~~ — **XONG 6/8** | — | bộ trỏ rẻ lệch 29,3%, không chấm được |
| ~~2~~ | ~~**Cổng A**~~ — **XONG 9/8, MIỄN PHÍ** trên Kaggle T4 | **0 đô** | ĐẠT: lệch trung vị 0,7% · trần thước 70,0% |
| ~~2b~~ | ~~Tiền trạm đường sinh câu~~ — **XONG 9/8, MIỄN PHÍ** | **0 đô** | tự kiểm lô 8/8 · sinh câu · chấm điểm · B-infer, cả bốn chạy thật |
| 3 | Huấn luyện S1 × 2 hạt giống → sinh câu → **MDE thật** → khoá ngưỡng | 19–30 đô | trình tự cứng, không đảo |
| 4 | Huấn luyện S2 × 2 hạt giống | 17–28 đô | |
| 5 | S2r, S2-nopoint | 17–28 đô | |
| 6 | B-infer + mốc mô hình gốc (chỉ suy luận) | 3 đô | |
| 7 | Thử mức 2 trên lát nhỏ (S3-pilot — **chưa có mã**) | 1 đô | sau cổng C |
| 8 | Chấm tay 100 câu (2 người) · demo tiếng Việt · kiểm không-gây-hại | 0 đô | |
| — | Dựng dữ liệu + OCR 64.500 ảnh trên máy thuê | 2 đô | |
| — | Đĩa 100 GB giữ 5–10 ngày + băng thông ~70 GB | 5–10 đô | tính cả lúc máy tắt |

Tổng **~$65–100**, dưới ngân sách 200. **Khâu chấm điểm không nằm trong bảng** — đem về Kaggle
chạy miễn phí, ~5 giờ một nhánh trong hạn mức 30 giờ/tuần, nhờ việc bật cache khoá-giá trị.
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

### Bốn mục "chưa kiểm được" của bản 6/8 — nay đã kiểm hết, ngày 9/8, miễn phí

| Mục treo hồi 6/8 | Đã làm gì | Kết quả |
|---|---|---|
| `train_config.yaml` chưa từng chạy qua LLaMA-Factory | 10 bước trên Kaggle T4, 60 mẫu | nhận cấu hình; **LoRA khớp 14.966.784 tham số** — tính tay ra đúng 36 tầng × 7 mô-đun, xác nhận `freeze_vision_tower` có tác dụng |
| Tự kiểm lô 1 vs lô n cần GPU | `--selftest-batch --no-adapter --batch 8` | **8/8 trùng nguyên văn** — đệm bên trái đúng, chấm theo lô an toàn |
| `UGround` chưa được nạp lần nào | cổng A, 300 bước | **ĐẠT**, xem mục 13 |
| `run_on_rented.sh` chưa chạy | rà tay, chưa chạy | tìm ra 2 lỗi chặn đường (cache parquet · không có git remote), đã vá trước khi thuê |

Thêm ba thứ **chưa từng chạy** mà bản 6/8 không liệt vì không ai để ý: `infer_branch.py` chưa
sinh một câu nào (không có tệp `preds_*.jsonl` nào trong repo), `score_run --mode score` chưa
chấm lần nào, và `--b-infer` chưa chèn danh sách lần nào. Cả ba đã chạy ngày 9/8 trên mô hình
gốc chưa huấn luyện. Cách phát hiện đáng ghi lại: **rà dấu vết trên đĩa**, không hỏi trí nhớ.

### Còn lại chưa kiểm

1. `run_on_rented.sh` vẫn chưa chạy trọn trên máy thuê.
2. `build_train_data.py` chưa chạy quá 2 shard; bản đủ là 76.
3. **S3-pilot không có mã** hàm phạt lề — cố ý, nằm sau cổng C.

### Rủi ro lớn nhất còn lại, xếp theo mức

1. ~~**Bộ trỏ chuyên có đạt cổng A không**~~ — **đã trả lời 9/8: ĐẠT**, lệch trung vị 0,7%.
   Rủi ro thay thế: **trần của thước chỉ 70,0%**, nên khoảng trống cho S2 hẹp hơn tưởng, và mọi
   điểm phải đọc trên nền 70 chứ không phải 100.
2. **Hiệu ứng rơi vào vùng 4–9 pp** — kết luận đổi theo luật gộp cụm, phải báo là chưa kết luận
   được (mục 7.1).
3. **Thước không phân biệt được lệch dưới ~63 px** (bơm lỗi bắt được 33,1%). Đây là hành vi cố ý
   của luật gộp phần tử, nhưng phải khai: thước đo được *trỏ nhầm sang nút khác*, **không** đo
   được *trỏ hơi lệch trong cùng một nút*.


---

## 13. Kết quả đo trên GPU miễn phí — 9/8/2026

Toàn bộ mục này chạy trên **Kaggle Tesla T4, không tốn đồng nào**. Trước đó cả bốn mắt xích ở
đây đều được xếp vào loại "phải thuê máy mới biết".

### 13.1. Cổng A — ĐẠT

UGround-V1-2B, 300 bước lấy theo hạt giống 20260805 từ 4.463 bước chạm. Vết thô: `ckpt/gate_A_raw.jsonl`.

| | |
|---|---|
| **sai số trung vị** | **0,7%** bề ngang màn (ngưỡng khoá trước: ≤3%) |
| phân vị 75 | 8,8% |
| số bước ≤3% | 62,7% |
| phân bố | p10 0,1% · p25 0,2% · p50 0,7% · p75 9,1% · p90 36,3% |

Dụng cụ hai thái cực: trúng thì trúng ngay tâm, trượt thì trượt hẳn. Đo trên **câu chuẩn của
người viết**, nên đây là phép đo DỤNG CỤ, không đo mô hình nào.

Một trong bốn dấu hiệu lỗi cài đặt có kêu (*x đúng giữa màn 30,7%*, ngưỡng 20%). Truy bằng bảng
2×2 chéo với vị trí điểm chạm chuẩn: điểm chạm của người cũng nằm giữa màn 18,3% số bước, nhưng
trong 245 bước có chuẩn **không** ở giữa thì bộ trỏ vẫn trả x giữa ở 46 bước — tính riêng trong
nhóm trượt là ~45%. Dải "đúng giữa" chỉ chiếm ~1% trục x nên trượt ngẫu nhiên không rơi vào đó
nhiều thế. ⇒ **kiểu hỏng thật của bộ trỏ** (không nhận ra phần tử thì bỏ trục ngang về giữa),
ảnh hưởng 15,3% số bước, **không** phải lỗi cài đặt. Làm số xấu đi chứ không đẹp lên, nên cổng
đạt hợp lệ. Phải khai kèm mỗi lần trình.

### 13.2. Trần của thước = 70,0% — số phải in cạnh mọi kết quả S1/S2

Cổng A đo khoảng cách, thước chính là ô-Voronoi. Đem chính 300 điểm trỏ đó chấm bằng
`hit_voronoi` (`harness/gate_a_ceiling.py`, offline, không gọi lại bộ trỏ):

| | |
|---|---|
| **ô-Voronoi tâm — trần** | **70,0%** KTC95 [64,5%, 75,3%] |
| đĩa dung sai — trần | 81,3% KTC95 [76,6%, 86,0%] |
| cụm | 239 (hiệu dụng 191,5) · trung vị 72 phần tử/màn · 0 màn thiếu cây trợ năng |

Câu đưa vào là câu chuẩn nên `action_ok`/`toggle_ok` đúng theo định nghĩa; điểm rút gọn còn đúng
phần định vị. **Nhánh đạt 45% là đạt 64% của trần, không phải "kém quá nửa".** Và vì câu mô hình
tệ hơn câu chuẩn, 70,0% là **cận trên**.

### 13.3. Ngưỡng 3% — xác nhận bằng dụng cụ thật, trên tập thật

| dải sai số | n | Voronoi | đĩa |
|---|---|---|---|
| ≤3% | 188 | **100,0%** | 100,0% |
| 3–5% | 21 | 66,7% | 100,0% |
| 5–8% | 16 | 43,8% | 100,0% |
| 8–14% | 12 | 8,3% | 100,0% |
| >14% | 63 | 0,0% | 11,1% |

Dưới 3% **không có ca kết oan nào** — trùng đường cong đo trước bằng dụng cụ mô phỏng (3% → 0%),
nay xác nhận trên đúng bộ trỏ và đúng tập sẽ chấm. Ngưỡng cổng A không còn là con số mượn.

Bảng này cũng đóng đinh quyết định 6/8: **đĩa dung sai vô dụng để phân biệt** — cho 100% ngay cả
khi lệch 8–14% bề ngang màn. Giữ ở vai trò báo kèm, không bao giờ làm headline.

### 13.4. Bộ nhớ đệm khoá-giá trị — 9,3 lần, và đã chứng minh không đổi kết quả

`generation_config` của UGround đặt `use_cache=False`. Trên T4: 32 token mất **38,65 s** tắt
cache, **4,16 s** bật. Không suy luận rằng "toán học bảo toàn nên chắc bằng nhau" — chạy lại 50
bước đầu của chính mẫu cổng A với cache bật rồi so từng toạ độ: **trùng tuyệt đối 50/50**, sai
khác đúng bằng 0 (`ckpt/cache_check.jsonl`). Đã bật `use_cache=True` nói thẳng ở mọi chỗ gọi
`generate`. **Một lượt chấm đủ 4.463 bước: ~48 giờ → ~5 giờ**, tức Kaggle miễn phí gánh được cả
khâu chấm điểm của mọi nhánh.

### 13.5. Cấu trúc cụm của tập kiểm đủ — đầu vào cho MDE

| | G | G hiệu dụng | app thật | cụm-đơn |
|---|---|---|---|---|
| toàn bộ 4.463 bước chạm | 1.091 | **454,3** | 259 | 832 |
| mẫu 300 của cổng A | 239 | 191,5 | 83 | 156 |

Cụm lớn nhất 58 bước → không ứng dụng nào chi phối. MDE **chiếu** theo `2,8·sd/√G_eff`: sd 0,30
→ 3,9 pp · 0,40 → 5,3 pp · 0,50 → 6,6 pp. Vẫn là chiếu; sd thật chỉ biết sau khi có điểm S1 hai
hạt giống. Cam kết "Δ rơi 4–9 pp thì báo chưa kết luận được" giữ nguyên.

### 13.6. Đường sinh câu — bốn phép, đều đạt

| phép | kết quả |
|---|---|
| `--selftest` (CPU, 3 phép) | chuỗi lúc chấm trùng lúc dạy ĐẠT · **1.272 token ảnh** trong đầu vào ĐẠT |
| `--selftest-batch` (GPU) | **8/8 trùng nguyên văn** |
| sinh câu 20 bước, mô hình gốc | chạy hết, có OCR, câu tiếng Anh đọc được |
| `--mode score` trên 20 bước đó | in đủ Voronoi + KTC + số cụm, không lỗi |
| `--b-infer` | câu nhắc nở 580 → 2.076 ký tự; **11/20 bước cho câu khác** bản thường |
| `metric_exec` tự kiểm nội bộ | 6/6 test, hai giới hạn inventory nêu rõ |

Điểm của mô hình **chưa huấn luyện**: 45,0% Voronoi, KTC95 [23,8%, 68,4%] ở n=20 — rộng tới mức
**không được trích như một mốc**. Nhưng nó là lý do đăng ký thêm nhánh tham chiếu "mô hình gốc"
(`report/106` sửa đổi 9/8 mục k): nếu S1 xấp xỉ mô hình gốc thì tiền đề của cả thiết kế lung
lay, và nên biết trước khi diễn giải Δ giữa S1 và S2.

### 13.7. Độ dài chuỗi — không nhánh nào chạm trần, trừ B-infer

Đếm bằng bộ tách token của Qwen2.5-VL-3B, cộng 320 token thị giác. `cutoff_len: 2048`.

| | trung vị | p95 | tối đa |
|---|---|---|---|
| s1 / s2 / s2r / s2_nopoint (đích dạy) | 515–541 | 595–625 | **785** |
| câu nhắc lúc chấm, thường | 486 | 556 | 763 |
| câu nhắc **B-infer** | **1.149** | 1.338 | 2.048 |

⇒ **257/300 = 85,7%** bản ghi của B-infer nằm **ngoài** vùng độ dài mô hình từng thấy lúc dạy.
Cộng với trần 40 phần tử chạm ở gần như mọi màn (trung vị 40 = tối đa 40, trong khi màn có trung
vị 72 phần tử) và chỉ 14,1% phần tử có tên, B-infer là **đối thủ yếu hơn tên gọi của nó ở ba
phương diện độc lập**. Nếu nó thua S2 thì không được kết luận thẳng "đưa thông tin lúc chạy kém
hơn huấn luyện" — phải khai cả ba.


---

## 14. Rà runbook trước khi tiêu tiền — 9/8/2026

Sau khi chốt dùng Colab Pro thay vì thuê máy, soạn `harness/run_on_colab.md` rồi rà lại ba lượt.
Mục này ghi những gì lượt rà tìm ra, vì chúng là loại **thiếu sót trong quy trình**, khác với
lỗi trong mã ở mục 8 — nhưng hậu quả bằng nhau.

### 14.1. Ba kiểu hỏng âm thầm trong bản runbook đầu

| | Hậu quả nếu để nguyên | Đã xử |
|---|---|---|
| OCR chạy trong ô, không chạy nền | 3 giờ đổ hàng vạn dòng vào trình duyệt cho tới lúc treo tab; tab treo giữa lúc OCR là mất cả khâu | mọi khâu trên 10 phút chạy `nohup … > log &`, theo dõi bằng ô nhẹ |
| Không có ô kiểm phủ OCR | gộp từ 12 phần rời mà một tiến trình chết sớm thì tệp gộp **vẫn hợp lệ**, chỉ thiếu vài nghìn ảnh — những bước đó vào huấn luyện với đầu vào thiếu chữ, khác hẳn lúc chấm | ô đối chiếu phủ với `train.jsonl` (phải 0 thiếu) + ô theo dõi in **số tiến trình còn sống** |
| Không thăm dò trước khi cam kết 15 giờ | không biết có tràn bộ nhớ, không biết giây/bước nên không tính được số đơn vị thật | ô chạy 20 bước rồi trích từ log: tham số huấn luyện (chờ 14.966.784), cỡ lô hiệu dụng (chờ 16), giây/bước, có tràn bộ nhớ không |

### 14.2. Bốn phép kiểm bắt buộc, không nằm trong bản đăng ký

| Phép | Chặn gì |
|---|---|
| **rò rỉ tác vụ dạy ↔ kiểm** ở quy mô 76 shard | "0 tác vụ trùng" **mới chỉ kiểm trên lát 2 shard**. Trùng thì mô hình học đúng đề thi, và **không có cách nào chữa sau khi đã train** |
| phủ OCR 100% | xem 14.1 |
| 9 bất biến bốn nhánh ở quy mô đủ | rớt một cái là bốn nhánh không so được với nhau |
| **thử nối tiếp** sau khi cố ý giết tiến trình | cả kế hoạch Colab dựa vào việc LLaMA-Factory tự dò điểm lưu mà chạy tiếp — cơ chế dựng bằng cách **cố ý bỏ trống** `resume_from_checkpoint` (lỗi bắt 7/8) và **chưa từng chạy thử**. Biết nó hỏng ở phút 30 mất 30 phút; biết ở giờ thứ 11 mất 11 giờ |

### 14.3. Bốn khâu đã đăng ký mà bản runbook đầu bỏ sót

Thước **không-gây-hại** (bắt buộc, 35,9% bước không phải bước chạm) · **ba lát cắt** đã đăng ký
(toàn tập / lát khó / app chưa thấy) · **chấm tay 100 câu hai người** · **bản trình diễn tiếng
Việt**. Cả bốn không cần GPU. Bỏ quên thì tới lúc trình không có số — đúng loại lỗi đã bắt bốn
lần (script suy luận, script chấm, thước không-gây-hại, phép thử trần).

### 14.4. Lưu vết — quy tắc chốt

**Thứ gì tính lại tốn tiền hoặc tốn giờ thì phải nằm trên Drive trước khi tắt máy.** Colab xoá
sạch `/content` khi phiên chết. Danh sách bắt buộc: `cfg.yaml` của **từng** lượt (đây là **bằng
chứng** cho câu "sáu nhánh chỉ khác ba dòng" — không có nó thì đó là lời khai) · `train.log` +
`loss_curve.json` (hình trong luận văn) · `probe.log` (giây/bước, cho phần chi phí tính toán) ·
`resume.log` · `preds_*.jsonl` · `score_*_raw.jsonl` · `descriptor_build_stats*.json` · `ckpt/`.

### 14.5. Trạng thái runbook

35 ô mã · 0 lỗi cú pháp · **6 mốc dừng** để dán kết quả ra phân tích trước khi tiêu tiếp · 14
lệnh gọi script, 0 cờ sai khi đối chiếu với `argparse` thật · một bảng ánh xạ **từng mục của
`report/106`** sang chỗ nó chạy, trong đó ghi thẳng hai chỗ **chưa có mã** (hàm phạt lề S3-pilot,
bộ chấm tay mù).
