# 144 — Lượt GRPO thưởng `<point>`: kết quả huấn luyện, cổng khai báo, và phản biện

*Viết 6/9/2026, sau khi C1 (suy luận 4.463 bước) xong và TRƯỚC khi có `exec`.*
Đăng ký: `report/106` mục **(x19)**, ghi số ở **(x19d) ghi 1…5**. Mã `harness/grpo_point.py` ·
runbook `harness/colab_grpo_point.md` (train) và `harness/kaggle_grpo_point_6_9.md` (suy luận,
chấm) · tệp ở `runs/grpo_point/` · đọc lại bằng `harness/doc_grpo_local.py`.

---

## 1. Lượt train đã diễn ra đúng thiết kế

500/500 bước, 5,63 h A100, TRL 0.29.1 GRPO học tiếp adapter MIN-DESC/101, tham chiếu KL là bản
sao đóng băng của chính MIN, G=4, temp 1,0, lr 1e-5, β=0,04. Số theo 5 chặng 100 bước:

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

· `r_point` tăng đơn điệu **+0,072** nhưng **chững hẳn ở 100 bước cuối** (+0,0006); cùng lúc
  `frac_reward_zero_std` bò lên 0,515 và `entropy` giảm ⇒ **tín hiệu học đã cạn ở cấu hình này**.
· `r_format` bão hoà ngay từ đầu, `r_name` gần như đứng yên ⇒ toàn bộ mức tăng đến từ `r_point`.
· **Dịch chuyển trọng số thật 1,054e-02** so với MIN, gấp **6,4 lần** sàn nhiễu cast 1,652e-03
  (adapter lưu bf16, bản `ref` lưu fp32 — phải tách sàn này ra mới đọc được).

## 2. Suy luận và kiểm tệp

4.463/4.463 bước, 0,4 bước/giây, ~3,1 h Kaggle T4, **0 đồng**. Một chữ ký
`lora:grpo-point-adapter`, **0 câu rỗng**, **0 câu sót `<desc>`**. `kiem_preds.py` đạt **6/8**;
hai phép không đạt là số bản ghi 4.463 thay vì 6.958, đúng bằng phạm vi đã khai ở (x19d) ghi 3.
**Phép 5 đạt:** cả hai nhánh không bỏ bước nào ⇒ McNemar ghép cặp với MIN dùng trọn 4.463.

## 3. Cổng khai báo — tăng, và tăng có ý nghĩa

Ghép cặp trên 3.473 bước có tên vàng (`gate_desc_acc.py`, **0 GPU**, không gọi bộ trỏ):

| cột | MIN | GRPO | Δ | b (MIN đúng/GRPO sai) | c (ngược lại) | χ² | p | KTC95 |
|---|---|---|---|---|---|---|---|---|
| tên đúng | 67,0 | 69,5 | **+2,51** | 62 | 149 | 35,05 | 3,2e−09 | [+1,69 · +3,32] |
| point đúng | 71,8 | 74,0 | **+2,22** | 77 | 154 | 25,00 | 5,7e−07 | [+1,36 · +3,07] |
| **cả hai đúng** | 60,6 | 63,2 | **+2,56** | 75 | 164 | 32,40 | 1,3e−08 | [+1,69 · +3,44] |

Tỉ lệ sinh `<desc>` giữ **99,6%** ở cả hai nhánh.

## 4. Mức tăng nằm ở đâu, và nó là loại gì

· **Câu đổi 21,5%** (961/4.463). Trên 683 bước có tên vàng trong nhóm đó, "cả hai đúng"
  **43,3 → 52,4 (+9,08)**; nhóm giữ nguyên câu chỉ **+0,97**. Nhóm đã đổi là nhóm **khó hơn hẳn**
  (nền 43,3 so với 64,9).
· ⭐ **Không phải "nhích qua ngưỡng thưởng".** Point của **66,5%** số bước **đứng yên tuyệt đối**,
  trung vị sai số không đổi (18,0 ở cả hai nhánh) ⇒ mô hình không tinh chỉnh toàn cục. Trong
  **184 bước GRPO trúng mà MIN trượt**, MIN vốn lệch **trung vị 359** (p25 235 · p75 453), và
  **51,6% lệch quá 350** tức khác hẳn vùng màn, chỉ **17,9%** nằm sát ngưỡng (140–200).
  ⇒ Cơ chế là **chuyển sang phần tử khác**, đúng dạng lỗi lưỡng cực đã ghi ở (x13c), chứ không
  phải dịch điểm vài chục pixel cho lọt cửa sổ thưởng. Cải thiện dồn ở đuôi phân bố: p75
  **210 → 190**.
· **Câu không bị bẻ thành mật mã:** BLEU-4 **37,86 → 37,78 (−0,09)** · ROUGE-L **+0,06** · độ dài
  trung vị **34 ký tự ở cả hai** · câu dưới 4 token **107 ở cả hai** · mở đầu bằng động từ chạm
  **93,8 → 94,3%**. Xa ngưỡng "giảm quá 1,0" của (x19e).

## 5. Phản biện — tám đòn, xếp theo sức nặng

**⛔ Đ1. Không có nhánh so sánh "train thêm 500 bước".** Đây là đòn mạnh nhất và hiện **không
đóng được bằng dữ liệu đang có**. Mọi con số ở §3–4 so GRPO với MIN **đứng yên**, nên chúng lẫn
công của *thuật toán GRPO + phần thưởng `<point>`* với công của *việc học thêm 2.000 mẫu nữa*.
Tiền lệ ngay trong dự án cảnh báo đúng chuyện này: ở lượt MIN-DESC, khi có nhánh so sánh CE2-S2
thì **78–88% mức tăng hoá ra thuộc về nhánh so sánh**, phần riêng của ORPO chỉ còn +0,63 pp.
⇒ Cho tới khi có nhánh so sánh, **cấm viết** "GRPO nâng khai báo +2,56 pp"; câu đúng là
"học tiếp 500 bước bằng GRPO thưởng `<point>` cho +2,56 pp so với điểm dừng của MIN".

**⛔ Đ2. Hai cột của cổng khai báo KHÔNG độc lập với hàm thưởng.** Ngưỡng point của
`gate_desc_acc.py` là **±140 trên lưới 1000**, **trùng khít** cửa sổ ±140 của `r_point`; cột tên
cũng được thưởng qua `r_name`. Vậy §3 đo lại chính đại lượng đã tối ưu, chỉ khác là trên dữ liệu
chưa thấy — nó chứng minh **mức tăng có tổng quát hoá**, **không** chứng minh mức tăng có giá trị.
Thước độc lập duy nhất là `exec`, vì nó đưa **câu** cho UGround và **không đọc ô `<point>`**.

**Đ3. Cách chia nhóm "câu đã đổi / giữ nguyên" là hậu kiểm.** Nhóm được định nghĩa bằng hành vi
của chính mô hình đang xét — cùng dạng đã phải gắn cảnh báo cho lát 325 bước của S2. Con số
+9,08 pp là **mô tả cơ chế**, không phải hiệu ứng nhân quả, và phải mang nhãn hậu kiểm.

**Đ4. Dự báo `exec` dựa trên hệ số 0,43 là ngoại suy từ MỘT quan sát.** Hệ số đo trên đúng một
cặp (S2 → MIN) của chính dự án; văn liệu cho dải rộng 0,23–0,58. Dự báo **+1,10 pp** (dải
+0,59 … +1,49) vì thế là mốc để đối chiếu, không phải tiên đoán chắc.
⚠️ Có căn cứ để hệ số lần này **cao hơn** 0,43: §4 cho thấy hơn nửa số ca lật là đổi hẳn phần tử
chứ không phải dịch điểm, mà `exec` chấm bằng câu — sửa đúng phần tử thì câu mới đổi theo. Nhưng
đây là lý do **sau khi thấy số khai báo**, nên **không được dùng để nới dự báo** đã ghi ở (x19d)
ghi 5.

**Đ5. Một hạt giống.** Theo (x14b)/(x14c) và (x19e): chỉ gọi *tăng* khi Δ ≥ MDE **2,2 pp** và KTC
loại 0; dưới đó là **TRẮNG dù dấu nào**. Nhiễu giữa hạt giống đo được là 0,46–0,52 pp.

**Đ6. Không đo được bước không chạm.** Lượt này chỉ sinh 4.463 bước chạm (lý do vật chất ở ghi 3).
Tập thưởng cũng chỉ gồm bước chạm, mà MIN-DESC từng lộ giá **−19,75** đúng ở nhóm không chạm.
Rủi ro này **chưa được kiểm**, phải khai mỗi lần báo kết quả.

**Đ7. Tín hiệu học đã cạn trước khi hết 500 bước.** `frac_reward_zero_std` 0,515 và `r_point`
phẳng ở chặng cuối ⇒ kéo dài thêm ở cấu hình này khó mua thêm gì; muốn đi tiếp phải đổi G hoặc
temp, và đó là **quyết định mới**, không phải hệ quả của lượt này.

**Đ8. Chuyển giao train → test chỉ ~31%.** `r_point` trên tập thưởng +7,2 pp so với point đúng
trên tập kiểm +2,22 pp. ⚠️ Hai phép đo khác chế độ giải mã (train lấy mẫu temp 1,0 G=4; kiểm
greedy) nên chỉ đọc theo chiều và bậc độ lớn, không so mức tuyệt đối.

## 5b. `exec` ĐÃ CÓ (6/9): **60,07% · Δ = +0,02 pp · TRẮNG**, và vì sao nó trắng

| nhánh | exec Voronoi gated .14 | KTC95 |
|---|---|---|
| MIN-DESC/101 | 60,05% | [58,35 · 61,79] |
| **GRPO-point/101** | **60,07%** | [58,32 · 61,83] |

McNemar ghép cặp trên **n=4.463**: **b=98 · c=99 · Δ=+0,02 pp · χ²=0,00 · p=1**, KTC95
**[−0,59 · +0,64]**. ⇒ **TRẮNG** theo (x19e). Áp (x20a) và (x20c): **nhánh so sánh KHÔNG chạy ·
hạt 202 KHÔNG chạy**.

⭐ **Dự báo ghi trước bị BÁC, và bác một chiều rõ ràng.** (x19d) ghi 5 dự báo **+1,10 pp** (dải
+0,59 … +1,49) từ hệ số chuyển đổi 0,43; cận **trên** của KTC thật (+0,64) nằm gần cận **dưới**
của dự báo. Hệ số chuyển đổi thực tế của lượt này là **+2,56 → +0,02, tức ≈ 0,01**, không phải
0,43. ⇒ Hệ số 0,43 **không phải hằng số của bài toán**; nó phụ thuộc cách can thiệp.

Thước phụ: `action_ok` **98,88 → 98,86** · `toggle_ok` **99,89 → 99,89** · `hit_disk` thuần
**69,19 → 69,89**. D.3 **66,55 → 67,04** · D.3∧14% **62,69 → 62,96** (cùng chiều, cùng cỡ nhỏ).

### ⭐ Cơ chế KHÔNG hỏng — nó bị triệt tiêu. Hạch toán trọn vẹn trên 3.473 bước có tên vàng:

| nhóm | n | b (MIN đúng/GRPO sai) | c | ròng |
|---|---|---|---|---|
| khai báo **SỬA ĐƯỢC** (MIN sai → GRPO đúng) | 164 | 2 | 64 | **+62** |
| khai báo **HỎNG ĐI** (MIN đúng → GRPO sai) | 75 | 30 | 0 | **−30** |
| khai báo **giữ nguyên trạng thái** | 3.234 | 31 | 17 | **−14** |
| **cộng** | 3.473 | 63 | 81 | **+18** (= +0,52 pp) |
| *bước KHÔNG có tên vàng* (suy ra từ tổng 4.463) | 990 | 35 | 18 | **−17** |
| **TỔNG 4.463** | | **98** | **99** | **+1 bước = +0,02 pp** |

· ⭐ **Liên hệ khai báo → `exec` rất mạnh, không hề yếu:** ở 164 bước sửa được khai báo, `exec`
  nhảy **32,9 → 70,7 (+37,80 pp)**; ở 75 bước làm hỏng khai báo, `exec` rơi **69,3 → 29,3
  (−40,00 pp)**. Hai vế gần đối xứng. Riêng nhóm sửa được **mà câu có đổi** (n=106): `exec`
  **17,0 → 75,5 (+58,49 pp)**, b=2 c=64.
· **35,4% số bước sửa được khai báo lại không đổi câu** (58/164) ⇒ `exec` **không thể** đổi, vì
  thước tất định và ô khai báo bị cắt trước khi chấm. Công sửa ở đó rơi vào chỗ thước không nhìn.
· **Ba nguồn triệt tiêu, cộng lại −61 gần bằng đúng phần lợi +62:** làm hỏng khai báo ở 75 bước
  (−30) · đổi câu ở nơi khai báo **không** cải thiện (533 bước, −14) · và nhóm **không có tên
  vàng** (−17), là nhóm mà phần thưởng không có tín hiệu nào để học.
· ⇒ **Bài học phương pháp, đáng giá hơn con số:** phần thưởng đặt ở **tầng trung gian**
  (`<point>` và tên) nâng đúng tầng đó, nhưng **không có số hạng nào bảo vệ tầng đầu ra**. Khi
  trọng số dịch chuyển, câu đổi theo ở cả những bước phần thưởng không nói gì, và ở đó nó đổi
  theo hướng xấu vừa đủ để xoá sạch phần lợi. Đây là dạng thất bại **khác** với "cơ chế yếu".

## 6. Quyết định đã khoá ở (x20), 6/9, TRƯỚC khi có `exec`

Chủ luận văn quyết trong lúc commit C2 đang chạy, khi chưa ai nhìn thấy số. Toàn văn ở
`report/106` mục **(x20)**; rút gọn:

| mã | nội dung | điều kiện |
|---|---|---|
| **(x20a)** | Nhánh so sánh cho Đ1 — `min_ce_tiep_seed101`, học tiếp từ cùng điểm lưu MIN bằng **SFT cross-entropy** trên đúng 2.000 câu nhắc của tập thưởng, 1 epoch, lr 1e-5, lô 16 ⇒ 125 update | **chỉ chạy nếu `exec` ≥ +2,2 pp** |
| **(x20b)** | Bước KHÔNG chạm, 2.495 bước, thước là tỉ lệ khớp loại thao tác (`--mode noharm`) | **đo vô điều kiện** ngay sau C2 |
| **(x20c)** | Hạt giống 202 | chỉ nếu `exec` ≥ +2,2 pp |
| **(x20d)** | Lượt GRPO khác (đổi G hoặc temp) | **quyết định mới**, phải mở mục đăng ký riêng |

· Thiết kế của (x20a) **khoá luôn tại chỗ**, không để quyết sau khi thấy số. Điều phải khai kèm:
  GRPO sinh G=4 chuỗi mỗi câu nhắc nên thấy **8.000** chuỗi, còn SFT thấy **2.000** ⇒ hai nhánh
  **không đối xứng hoàn toàn**; trục đối xứng là *cùng dữ liệu, cùng số câu nhắc, khác mục tiêu*.
· Nếu (x20a) không chạy vì `exec` trắng: luận văn **phải** ghi thẳng rằng không tách được công của
  GRPO khỏi công của việc học thêm, kèm tiền lệ MIN vs CE2. ⛔ Cấm dùng +2,56 pp ở cổng khai báo
  để lấp chỗ đó.
· Ngưỡng của (x20b) **lấy nguyên từ mục 3 của bản gốc** (không thấp hơn quá **3 pp**), cố ý không
  đặt ngưỡng mới.

## 7. Việc kế, theo thứ tự phụ thuộc

1. **C2 — chấm `exec` trên 4.463 bước** (Kaggle T4, ~5,4 h, 0 đồng). Thước độc lập duy nhất, là
   headline. Đọc bằng **`harness/doc_exec_grpo.py`** (0 GPU): exec hai nhánh + KTC bootstrap cụm,
   McNemar ghép cặp, verdict theo (x19e), câu trả lời cho (x20a)/(x20c), thước phụ, bảng D.3, và
   phân rã theo nhóm câu đã đổi.
2. **C3 — bước không chạm**, chạy được song song với C2 vì dùng dataset ảnh riêng. Suy luận 2.495
   bước trên Kaggle (~1,7 h); **chấm ở máy nhà, 0 GPU**. Gói ảnh đã đóng sẵn:
   `test_images_nontap.tar` (1,54 GB, 2.495 ảnh, dựng từ ảnh có sẵn trên máy nên không phải tải
   `test_images.tar` từ Drive). Danh sách `--only`: `runs/grpo_point/only_nontap2495.jsonl`.
   Runbook: mục **C3** của `harness/kaggle_grpo_point_6_9.md`.
3. Chỉ khi `exec` ≥ +2,2 pp mới tới (x20a) và (x20c).
