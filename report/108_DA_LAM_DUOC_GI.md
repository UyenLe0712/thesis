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
| ⚠️ Không phải app-unseen | 92% ứng dụng cũng có trong tập dạy — xem mục 8 |
| Gán được ứng dụng | 44,9% số bước (269 ứng dụng); còn lại thành cụm riêng từng tác vụ |
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

---

## 4. Dữ liệu bốn nhánh thí nghiệm

Mọi nhánh dùng **cùng một đầu vào** (ảnh + mục tiêu + lịch sử + chữ OCR), chỉ khác đích sinh.

| Nhánh | Đích sinh | Độ dài đích trung bình |
|---|---|---|
| s1 | câu | 35,4 ký tự |
| s2 | `<desc>` thật + câu | 94,5 |
| s2r | `<desc>` **giả** + câu | 94,4 |
| s2_nopoint | `<desc>` bỏ ô toạ độ + câu | 78,8 |

**Kiểm bất biến (6/8), tất cả đạt:**

- Đầu vào giống hệt nhau ở 4 nhánh: **1697/1697**
- s2r khác s2 ở mọi bước có khai báo: **1074/1074**
- s2_nopoint còn sót `<point>`: **0**
- Bước không-chạm giữ đích y hệt ở mọi nhánh: **623/623** → phép kiểm không-gây-hại đọc được
- Ảnh tồn tại: 200/200 mẫu ngẫu nhiên

**Khai báo giả lệch độ dài trung bình 0,5 ký tự** so với bản thật — sát tới mức không ai đổ được
hiệu ứng cho chuyện "chuỗi đích dài thêm". Theo tra cứu, nhánh đối chứng kiểu này **chưa nghiên
cứu nào từng chạy**. Mã: `harness/build_branch_data.py`.

---

## 5. Đường ống huấn luyện → chấm điểm

| Khâu | Mã | Trạng thái |
|---|---|---|
| Cấu hình huấn luyện | `harness/train_config.yaml` | một file cho mọi nhánh, chỉ đổi 3 dòng `dataset`/`seed`/`output_dir` |
| Suy luận | `harness/infer_branch.py` | dùng **chung hàm dựng câu nhắc** với lúc dạy (import, không chép) |
| Chấm điểm + cổng A | `harness/score_run.py` | bộ trỏ cắm rời, bootstrap gom cụm theo ứng dụng |
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
| Hình học màn | nút đích 189×126 px · nút khác gần nhất cách 69 px · bộ trỏ rẻ lệch trung vị 108,8 px | lát 76 bước | căn cứ đặt ngưỡng cổng A ở 3% |

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
| 1 | Thử đường ống bằng bộ trỏ rẻ, ~30 bước | ~0,3 đô | chưa chạy `score_run.py` thật lần nào |
| 2 | **Cổng A** — đo sai số bộ trỏ chuyên | 4–8 đô | cần GPU; quyết định thước chính có dùng được không |
| 3 | Huấn luyện S1 × 2 hạt giống → chấm đủ → **MDE thật** → khoá ngưỡng | 26–34 đô | trình tự cứng, không đảo |
| 4 | Huấn luyện S2 × 2 hạt giống → chấm | 26–32 đô | |
| 5 | S2r, S2-nopoint, B-infer | 26–32 đô | |
| 6 | Thử mức 2 trên lát nhỏ | 3–6 đô | |
| 7 | Chấm tay 100 câu (2 người) · demo tiếng Việt · kiểm không-gây-hại | 0–2 đô | |

Tổng phần chắc chắn **85–112 đô**, dưới ngân sách 200.