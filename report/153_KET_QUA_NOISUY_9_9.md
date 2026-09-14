# 153 — KẾT QUẢ V2: nội suy MIN ↔ GRPO trong không gian trọng số (9/9/2026)

**Kết luận một dòng: đường cong theo α ĐƠN ĐIỆU, cực đại đúng tại đầu mút α = 1. Phép nội suy
không cho thêm gì, và theo luật §5.4 của `151` thì khoá α = 0 — không có cấu hình nào được đưa
lên tập kiểm.**

Lượt chạy: Kaggle T4 miễn phí, 0 đồng. Suy luận 5 × 407 bước (~1,7 h) + chấm 5 × 262 bước
(~1,4 h). Tệp ở `runs/noisuy/`.

---

## 1. Số

| α | ý nghĩa | `exec` trên val | `exec_disk` |
|---|---|---|---|
| **0,00** | đúng MIN-DESC | **67,56** | 74,05 |
| 0,25 | | 67,94 | 74,43 |
| 0,50 | nửa đường | 67,94 | 74,81 |
| 0,75 | | 67,94 | 74,81 |
| **1,00** | đúng GRPO-point | **68,32** | 74,81 |

n = **262** bước chạm / 85 tác vụ. Điểm giữa cao nhất là 67,94, tức **thua đầu mút tốt hơn
0,38 điểm**. Không mức nào vượt.

| phép so ghép cặp | Δ | SE | KTC95 | |
|---|---|---|---|---|
| α=1 − α=0 | +0,76 | 0,949 | [−1,06 · +2,69] | TRẮNG |
| α=0,5 − α=0 | +0,38 | 0,392 | [+0,00 · +1,28] | TRẮNG |
| α=0,5 − α=1 | −0,38 | 0,861 | [−2,06 · +1,27] | TRẮNG |

---

## 2. Dự đoán ghi trước — ĐÚNG

`151` §5.2 ghi kỳ vọng **+0,2…+0,5 pp, có thể bằng 0**, và §5.1 nêu thẳng khả năng *"đường cong
có thể đơn điệu, cực đại đúng tại α = 1, và khi đó thu được 0"*. Đó chính là điều đã xảy ra.

Ngày 9/9 khi dựng adapter, một phép đo bổ sung đã làm hẹp kỳ vọng ấy thêm nữa: GRPO chỉ dịch
chuyển `lora_A` **1,39%** và `lora_B` **6,87%** so với MIN, nên hai đầu mút vốn rất gần nhau và
đường cong gần như phẳng. Ghi ở `152` §0 mục 7 **trước khi** có kết quả này.

---

## 3. Hai phép kiểm bắt thảm hoạ — ĐẠT

| # | kiểm | ngưỡng | kết quả |
|---|---|---|---|
| ① | hai đầu mút rơi trong 50–70 | bắt buộc | 67,56 và 68,32 ✅ |
| ② | năm mức không cách nhau > 3 SE ≈ 9 pp | bắt buộc | chênh lớn nhất 0,76 ✅ |
| ③ | S1 không cao hơn trung bình MIN và GRPO quá 2,32 pp | mềm | **không chạy** — adapter S1 không có trong kho |

⇒ Đường chấm val lành, dùng lại được cho A6 của Phase 2.

⭐ **Phép kiểm hai đầu mút trên CÂU cũng đạt, và đạt theo cách đẹp hơn mong đợi:** 155/407 bước
(38,1%) có câu khác nhau giữa α=0 và α=1, và số bước câu đổi **tăng đơn điệu theo α** —
53 · 95 · 127 · 155. Nghĩa là mã ghép nối theo hạng hoạt động đúng như thiết kế: α càng lớn thì
mô hình càng gần GRPO, chứ không phải nhảy giữa hai bộ trọng số.

---

## 4. ⭐ Bằng chứng định lượng cho việc CẤM trích số val

| | val (262 bước) | test (4.463 bước) |
|---|---|---|
| MIN-DESC | 67,56 | 60,05 |
| GRPO-point | 68,32 | 60,07 |
| **chênh hai nhánh** | **+0,76** | **+0,02** |

Val cao hơn test khoảng **7,5 điểm** ở cả hai nhánh, đúng như đã cảnh báo: val tách ra từ tập dạy
mà cả hai mô hình đã học trên đó, nên điểm val là điểm *train*. Đáng chú ý hơn là **val phóng đại
khoảng cách giữa hai nhánh gấp gần 40 lần** (0,76 so với 0,02). Nếu ai đó trích số val ra báo thì
vừa thổi phồng mức tuyệt đối, vừa thổi phồng mức chênh.

⇒ Luật *"không bao giờ trích một con số val nào ra báo"* nay có số đo chống lưng, không còn là
nguyên tắc suông.

---

## 5. Quyết định

1. **Khoá α = 0** theo §5.4 của `151`: điểm giữa không vượt đầu mút ≥ 2,0 pp, thậm chí không vượt
   nổi đầu mút nào.
2. ⛔ **V4 (bước B8) KHÔNG chạy.** Argmax-val là α = 1, tức đúng GRPO-point, vốn đã có điểm test
   **60,07** đo từ 6/9. Chấm lại là chấm lại chính nó. **Tiết kiệm ~5,6 h T4.**
3. **V3 (soup ba adapter) vẫn chạy được**, nhưng kỳ vọng phải hạ theo: nếu nội suy hai adapter
   cùng họ đã đơn điệu thì soup ba adapter cùng họ khó cho khác. ⚠️ Đây là suy luận sau khi thấy
   số, nên nếu chạy thì vẫn báo vô điều kiện; nếu bỏ thì ghi rõ lý do là kết quả V2.
4. Đóng góp mô hình của luận văn **giữ nguyên ở GRPO-point 60,07**, tiêu đề không đổi.

---

## 6. Điều này nói gì về VIS-SFT (Phase 2)

**Không nói gì trực tiếp** — hai chặng độc lập, và VIS-SFT tác động vào tầng thị giác chứ không
phải vào việc trộn hai bộ trọng số đã có.

Nhưng nó củng cố một điều gián tiếp: mọi cách sắp xếp lại **đồ đã có** đều đã hết chỗ. Ghép nhánh
ở đầu ra đã bị bác (mọi bộ chọn không-oracle ≤ 60,45), và nay ghép ở không gian trọng số cũng
không cho gì. Đường còn lại phải tạo ra **thông tin mới**, và trong các hướng còn lại thì VIS-SFT
là hướng duy nhất chạm đúng tầng mà chẩn đoán hai kênh định vị được.

---

## 7. Phân tích tệp thô sau khi tải về (9/9, 0 giây GPU)

Bốn phép đo dưới đây làm trên `runs/noisuy/score_val_a*_raw.jsonl` sau khi bung gói, **không
gọi lại bộ trỏ**. Chúng làm kết luận mục 5 chặt hơn hẳn.

### 7.1 ⭐ Đường cong phẳng ở CẢ SÁU luật chấm, không riêng Voronoi

| luật | a0,00 | a0,25 | a0,50 | a0,75 | a1,00 | dải |
|---|---|---|---|---|---|---|
| Voronoi .14 (tiêu đề) | 67,56 | 67,94 | 67,94 | 67,94 | **68,32** | 0,76 |
| D.3 trong hộp | 70,61 | 70,99 | 70,99 | 70,99 | **71,37** | 0,76 |
| D.3 ∧ ±14% | 68,70 | 69,08 | 69,08 | 69,08 | **69,47** | 0,76 |
| `hit_disk` thuần | 74,05 | 74,43 | **74,81** | **74,81** | **74,81** | 0,76 |
| chữ nhật ±14% gated | 74,05 | 74,43 | **74,81** | **74,81** | **74,81** | 0,76 |
| nL2 .14 gated | 71,37 | 71,37 | 71,76 | 71,76 | **72,14** | 0,76 |

Dải đúng **0,76 pp = 2 bước** ở **mọi** luật, và điểm giữa không vượt đầu mút ở luật nào (tốt
nhất là hoà, dưới hai luật lỏng nhất). ⇒ Kết luận âm **không phụ thuộc cách chấm** — đây là lá
chắn mạnh nhất của mục 5, vì đòn *"đổi thước thì Δ khác"* không mở được.
⭐ Phép kiểm nội bộ đi kèm: bản dựng lại độc lập của luật chữ nhật ±14% từ `pred_xy`/`gold_xy`/
`wh` **trùng khít `hit_disk`** ở cả năm mức ⇒ tệp thô đủ dữ kiện và phép tính lại đúng.

### 7.2 Ba mức giữa trùng điểm nhưng KHÁC tập bước — không phải lỗi

Luật của dự án nói *"kết quả trùng nhau giữa các cấu hình khác nhau là dấu hiệu HỎNG"*, nên đã
kiểm: a0,25 và a0,50 chung 177 bước, mỗi bên có riêng 1; a0,25 và a0,75 chung 176, mỗi bên riêng
2. Cộng với bảng khác-câu từng cặp (13,0 · 23,3 · 31,2 · 38,1% so với α=0, bốn cặp kề nhau đều
đặn 10,6–13,8%) ⇒ trùng 67,94 là **trùng ngẫu nhiên trên thước thô**: mỗi bước đáng 0,38 pp.

Hạch toán so với α=0: a0,25 **+1/−0** · a0,50 **+1/−0** · a0,75 **+2/−1** · a1,00 **+4/−2**.
McNemar hai đầu mút: b=2, c=4, χ²=0,167, **p=0,68**.

### 7.3 ⭐ Tách `<desc>` khỏi câu: Phụ lục D tái lập trên lát độc lập

Trên 262 bước chạm của val, so α=0 với α=1:

| | số bước | tỉ lệ |
|---|---|---|
| `<desc>` đổi | 90 | 34,4% |
| CÂU đổi | 46 | 17,6% |
| **chỉ `<desc>` đổi, câu đứng yên** | **65** | **72,22% của 90** |
| chỉ CÂU đổi, `<desc>` đứng yên | 21 | — |
| cả hai đổi | 25 | — |

Con số **72,22%** tái lập **66,67%** của `151` Phụ lục D, đo trên tập kiểm — hai lát độc lập,
cùng hiện tượng, cùng cỡ. ⚠️ Và lát này lộ thêm **chiều ngược**: 21 bước câu đổi mà khai báo
không đổi. ⇒ Quan hệ khai báo ↔ câu **lỏng theo cả hai chiều**; đừng viết một chiều.

Hệ quả cho `exec`: trong 216 bước câu giữ nguyên, `exec` **68,52 → 68,52, 0 bước lật**. Toàn bộ
chuyển động nằm trong 46 bước câu đổi (63,04 → 67,39). ⛔ Đừng đọc dòng này thành phát hiện —
bộ trỏ là hàm tất định của câu và ảnh, nên 0 lật ở nhóm câu giữ nguyên là **bắt buộc**; giá trị
của nó là một phép kiểm tính tất định của thước, và phép kiểm ấy **đạt**.

### 7.4 Sáu bước lật đều là ĐỔI HẲN PHẦN TỬ, không phải nhích qua ngưỡng

| bước | chiều | lệch bộ trỏ | câu MIN → câu GRPO |
|---|---|---|---|
| ep11122_s5 | MIN trượt → GRPO trúng | 53,8% → 0,1% | *send icon* → *suggested email id* |
| ep13970_s0 | trượt → trúng | 87,2% → 0,2% | *three dots icon* → *back icon* |
| ep4359_s0 | trượt → trúng | 191,4% → 0,1% | *menu icon* → *Active option* |
| ep4783_s5 | trượt → trúng | 57,6% → 0,1% | *send icon* → *email id* |
| ep2607_s2 | **trúng → trượt** | 0,4% → 57,8% | *tab Vivid* → *tab Save Copy* |
| ep8461_s0 | **trúng → trượt** | 0,5% → 57,7% | *first alarm* → *Grocery alarm* |

Không bước nào nằm gần ngưỡng: lệch hoặc **0,1–0,5%** hoặc **53–191%** bề ngang. Sáu trên sáu là
đổi sang một **phần tử khác**, không phải diễn đạt lại cùng phần tử. Đây là lần tái lập thứ ba
của dạng lỗi lưỡng cực — sau `106` (x13c) (trung vị 351 px, 76,5% ngoài dải 80–350) và
`report/136` (trung vị 398/1000) — và khớp cơ chế mà `report/144` mô tả cho GRPO.
Phân vị lệch của cả 262 bước cũng lưỡng cực và **gần như y hệt nhau ở hai đầu mút**: trung vị
1,36 so 1,34% · p75 22,65 so 22,04% · p90 78,43 so 78,40%.

### 7.5 ⛔ V3 còn một chặn kỹ thuật mà mục 5 chưa nêu

Kiểm trên WSL 9/9: kho chỉ có adapter **MIN**, **GRPO** và **`gui_sel`**. **Adapter CE2-S2/101
không có trên máy** — nó nằm trên Drive. Nên V3 không phải "chỉ 4 h T4" mà là kéo từ Drive →
dựng soup ba khối (`r` 8→24, `lora_alpha` 16→48) → upload dataset → rồi mới 4 h T4.
Cộng với mục 7.1 (phẳng ở mọi luật) và việc CE2-S2 thấp hơn MIN **0,63 pp** trên tập kiểm, đề
xuất là **không chạy V3**, và ghi lý do đúng như vậy.
