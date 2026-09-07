# 146 — BÀN GIAO CHO PHIÊN DEBATE: có cách nào nâng `exec` lên nữa không?

*Viết 7/9/2026. **Tự chứa** — đọc một mình file này là đủ để tranh luận, không cần mở file khác.*
*Mọi con số dưới đây đã được tái lập từ tệp thô trong phiên viết, không chép lại từ ghi chú.*

---

## 0. Câu hỏi đặt ra cho phiên debate

Chủ luận văn nói thẳng: **"tôi chỉ cần số thôi"** — muốn `exec` cao hơn 60,07 hiện tại.
Nhiệm vụ của phiên debate: tìm cách nâng `exec`, hoặc chứng minh bằng số rằng không còn cách nào
trong ngân sách.

**Hai ranh giới không được vượt** (chủ luận văn đã tự khoá từ 5/8/2026, và hội đồng đối chiếu được
bằng `git log`):
· ⛔ **Không đổi thước headline sau khi đã thấy điểm.** Thước chính là `exec` Voronoi gated .14,
  niêm 5/8/2026. Đổi sang luật lỏng hơn để lấy số đẹp là gian lận đo lường.
· ⛔ **Không tối ưu thẳng vào bộ trỏ chấm** (UGround-V1-2B). Dùng chính nó để chọn câu, để lọc, để
  thưởng lúc train đều biến thước từ phép đo độc lập thành hàm mục tiêu.
Ngoài hai ranh giới đó, **mọi hướng đều mở**, kể cả train lại, đổi backbone, đổi dữ liệu.

---

## 1. Bài toán và thước đo

**Đầu vào:** ảnh chụp màn hình Android + mục tiêu tổng của tác vụ + lịch sử các bước trước (là câu
chuẩn do người chú thích viết, teacher-forced) + 24 dòng chữ OCR trích từ chính màn hình đó.
**Đầu ra:** một câu tiếng Anh hướng dẫn thao tác cho bước hiện tại, ví dụ *"Tap the search icon at
the top right"*.
**Mô hình:** Qwen2.5-VL-3B-Instruct, QLoRA 4-bit, phần thị giác đóng băng, cutoff 2560.

**Thước `exec` (executability), tất định:** đưa câu mô hình sinh ra cho một mô hình định vị độc lập
(UGround-V1-2B) cùng ảnh màn hình; mô hình đó trả về một toạ độ; câu được tính là **đạt** khi
① loại thao tác suy ra từ câu khớp loại thao tác chuẩn, **và** ② toạ độ nằm trong cửa sổ
$\pm 14\%$ chiều rộng/cao quanh toạ độ chuẩn, **và** ③ trong ô Voronoi của điểm chạm chuẩn (tức
không có phần tử nào khác gần hơn). Điều kiện ③ làm thước **chặt hơn** quy ước ngành.

**Dữ liệu:** AndroidControl (Li et al., NeurIPS 2024 D&B, CC0). Tập dạy 64.567 bước (41.191 bước
chạm), tập kiểm 6.958 bước, trong đó **4.463 bước chạm** là quần thể chấm điểm. Rò rỉ dạy–kiểm = 0
ở mức tác vụ.

**Hai đầu thang đã đo:**
· **Trần 75,73** = chấm chính câu chuẩn do người chú thích viết, qua cùng dụng cụ. Đây là **giới
  hạn dụng cụ**, không phải giới hạn ngôn ngữ: 21% số bước cả câu chuẩn lẫn mọi nhánh mô hình đều
  trượt; 72% ca thước mù là do bộ trỏ lệch quá 14%.
· **Sàn 12,0** = mọi bước đều trả câu `"Tap the button."`. Sàn phụ 6,1 = câu thật nhưng của bước
  khác (đúng văn phong, sai màn hình) — **thấp hơn** sàn câu chung chung, hai khoảng tin cậy rời
  nhau, nên thước không cho điểm theo văn phong.
· ⇒ **Dải dùng được: 12,0 → 75,73.**

**Ngưỡng phát hiện tối thiểu (MDE) = 2,2 pp**, đo bằng bootstrap cụm trên chính dữ liệu này
(SE 0,79 pp, hệ số nở do cụm 1,10×). Nhiễu giữa hai hạt giống đo được **0,46–0,52 pp**.
**Luật đọc bốn ô** (khoá 17/8/2026, trước khi chặng khai báo chạy): $\ge +2{,}8$ và KTC loại 0 là
dương · $+1{,}7 \dots +2{,}8$ là dương yếu · $-2{,}8 \dots +1{,}7$ là **không kết luận được** ·
$\le -2{,}8$ là gây hại. Một hạt giống thì mọi kết quả đều mang nhãn *một hạt giống*.

---

## 2. TOÀN BỘ ĐIỂM HIỆN CÓ (cùng 4.463 bước, cùng dụng cụ)

| nhánh | mô tả | `exec` |
|---|---|---|
| Base | Qwen2.5-VL-3B chưa tinh chỉnh | **47,59** |
| S1/101 | tinh chỉnh thuần (chỉ sinh câu) | **59,11** |
| S1/202 | như trên, hạt giống khác | **59,62** |
| S2/101 | sinh khai báo `<desc>` trước rồi mới sinh câu | **57,18** |
| CE2-S2 | học có giám sát tiếp từ S2 (nhánh so sánh của MIN) | **59,42** |
| MIN-DESC/101 | ORPO trên cặp quy chiếu tối thiểu ở tầng khai báo | **60,05** |
| **GRPO-point/101** | **học tăng cường thưởng ô `<point>`, lượt mới nhất 6/9** | **60,07** |
| gui_sel/101 | chọn phần tử trong khối ≤40 ứng viên của chính màn hình | **56,13** |
| *câu chuẩn của người* | *trần dụng cụ* | *75,73* |

**Mức chênh đáng chú ý:** S1 − Base = **+11,52** (χ²=243, p<0,001) là mức tăng lớn nhất của cả dự
án, và nó thuộc về **tinh chỉnh thuần**, không thuộc thành phần đề xuất nào. Mọi cải tiến sau S1
đều nằm trong dải không kết luận được: MIN − S1 = +0,94 (p=0,11) · GRPO − MIN = +0,02 (p=1).

---

## 3. LƯỢT MỚI NHẤT: GRPO thưởng `<point>` — thiết kế và kết quả

**Thiết kế.** Học tiếp từ điểm lưu MIN-DESC/101 bằng TRL 0.29.1 GRPO. Mỗi câu nhắc sinh G=4 câu
trả lời ở nhiệt độ 1,0; mô hình tham chiếu cho số hạng KL là bản sao đóng băng của chính điểm lưu
xuất phát; β=0,04; lr 1e-5; 2.000 câu nhắc lấy từ bước chạm của tập dạy, một lượt duyệt = **500
bước cập nhật**, 5,63 giờ A100.

**Phần thưởng (khoá trước khi chạy):** ô toạ độ đúng (điểm trong `<point>` nằm trong cửa sổ ±14%
quanh toạ độ chuẩn) = **1,0** · định dạng đúng = **0,2** · tên phần tử khớp = **0,1**.
⭐ **Không có mô hình định vị nào trong phần thưởng** — chỉ so ô toạ độ mô hình tự viết với nhãn có
sẵn. Nên lượt này không tối ưu thẳng vào thước.

**Nhật ký huấn luyện, 5 chặng 100 bước:**

| đại lượng | ch1 | ch2 | ch3 | ch4 | ch5 |
|---|---|---|---|---|---|
| `rewards/r_point/mean` | 0,686 | 0,702 | 0,709 | 0,758 | **0,758** |
| `reward` tổng | 0,946 | 0,960 | 0,967 | 1,018 | 1,023 |
| `rewards/r_name/mean` (trần 0,1) | 0,062 | 0,060 | 0,059 | 0,062 | 0,068 |
| `rewards/r_format/mean` (trần 0,2) | 0,198 | 0,198 | 0,199 | 0,198 | 0,198 |
| `frac_reward_zero_std` | 0,420 | 0,445 | 0,488 | 0,475 | **0,515** |
| `kl` | 0,0013 | 0,0017 | 0,0023 | 0,0030 | 0,0037 |
| `entropy` | 0,274 | 0,267 | 0,251 | 0,247 | 0,248 |
| `completions/mean_length` | 46,08 | 45,99 | 46,12 | 46,26 | 46,19 |

· `r_point` tăng **+0,072** nhưng **chững hẳn** ở 100 bước cuối (+0,0006), `frac_reward_zero_std`
  bò lên 0,515 và entropy giảm ⇒ **tín hiệu học đã cạn ở cấu hình này**.
· `r_format` bão hoà ngay từ đầu, `r_name` gần như đứng yên ⇒ toàn bộ mức tăng đến từ `r_point`.
· Dịch chuyển trọng số thật so với MIN: $\|\Delta\|/\|W\| = 1{,}054 \times 10^{-2}$, gấp 6,4 lần
  sàn nhiễu của phép ép kiểu số (adapter lưu bf16, bản tham chiếu lưu fp32).

**Kết quả ở tầng khai báo (`gate_desc_acc`, 0 GPU, ghép cặp 3.473 bước có tên chuẩn):**

| cột | MIN | GRPO | Δ | b | c | p | KTC95 |
|---|---|---|---|---|---|---|---|
| tên đúng | 67,0 | 69,5 | +2,51 | 62 | 149 | 3,2e−09 | [+1,69 · +3,32] |
| toạ độ đúng | 71,8 | 74,0 | +2,22 | 77 | 154 | 5,7e−07 | [+1,36 · +3,07] |
| **cả hai đúng** | 60,6 | 63,2 | **+2,56** | 75 | 164 | 1,3e−08 | [+1,69 · +3,44] |

⚠️ **Phép đo này KHÔNG độc lập với hàm thưởng**: ngưỡng ±140 trên lưới 1000 của `gate_desc_acc`
trùng khít cửa sổ ±14% của `r_point`, và cột tên cũng được thưởng qua `r_name`. Nó chứng minh mức
tăng **tổng quát hoá được** sang dữ liệu chưa thấy, **không** chứng minh mức tăng có giá trị.

**Kết quả ở thước độc lập (`exec`):**

| nhánh | `exec` | KTC95 |
|---|---|---|
| MIN-DESC/101 | 60,05 | [58,35 · 61,79] |
| GRPO-point/101 | **60,07** | [58,32 · 61,83] |

McNemar ghép cặp n=4.463: **b=98 · c=99 · Δ=+0,02 pp · χ²=0,00 · p=1**, KTC95 **[−0,59 · +0,64]**.
⇒ **Không kết luận được**, và KTC hẹp tới mức loại được mọi mức tăng từ +0,64 pp trở lên.
Thước phụ không đổi: khớp loại thao tác 98,88 → 98,86 · BLEU-4 37,86 → 37,78 · ROUGE-L 68,40 →
68,47 · độ dài trung vị 34 ký tự ở cả hai · luật hộp phần tử D.3 66,55 → 67,04.

**Một dự báo ghi TRƯỚC đã bị bác.** Trước khi chấm, mức tăng khai báo được quy thành dự báo `exec`
bằng hệ số chuyển đổi **0,43** (đo ở chặng trước: +6,70 pp khai báo cho +2,87 pp `exec`), ra
**+1,10 pp** [dải +0,59 … +1,49]. Đo được **+0,02**. Hệ số thực ≈ **0,01**.
⇒ Hệ số chuyển đổi **không phải hằng số của bài toán**, nó phụ thuộc dạng can thiệp.

---

## 4. ⭐ HẠCH TOÁN: vì sao +2,56 ở tầng khai báo chỉ còn +0,02 ở đầu ra

Đây là phần có giá trị nhất của lượt này. **Cơ chế không yếu — nó bị triệt tiêu.**

**Liên hệ khai báo → `exec` rất mạnh, hai chiều gần đối xứng:**
· 164 bước GRPO **sửa được** ô khai báo: `exec` **32,9 → 70,7 (+37,80 pp)**;
  riêng nhóm sửa được **mà câu có đổi** (n=106): **17,0 → 75,5 (+58,49 pp)**, b=2 c=64.
· 75 bước GRPO **làm hỏng** ô khai báo: `exec` **69,3 → 29,3 (−40,00 pp)**.

**Hạch toán trọn vẹn, mỗi bước thuộc đúng một nhóm:**

| nhóm | n | b (MIN đúng, GRPO sai) | c | ròng |
|---|---|---|---|---|
| khai báo **sửa được** | 164 | 2 | 64 | **+62** |
| khai báo **hỏng đi** | 75 | 30 | 0 | **−30** |
| khai báo giữ nguyên trạng thái | 3.234 | 31 | 17 | **−14** |
| bước **không có tên chuẩn** để chấm khai báo | 990 | 35 | 18 | **−17** |
| **tổng** | **4.463** | **98** | **99** | **+1 bước = +0,02 pp** |

**Bảng chéo *khai báo có đổi × câu có đổi*, toàn quần thể:**

| khai báo | câu | n | b | c | ròng | `exec` MIN → GRPO |
|---|---|---|---|---|---|---|
| không đổi | không đổi | 2.202 | 0 | 0 | 0 | 65,9 → 65,9 |
| không đổi | đổi | 311 | 10 | 5 | −5 | 61,4 → 59,8 |
| **đổi** | **không đổi** | **1.300** | 0 | 0 | 0 | 58,9 → 58,9 |
| đổi | đổi | 650 | 88 | 94 | +6 | 41,8 → 42,8 |

⭐ **1.300/1.950 = 66,7% số bước mà ô khai báo đổi nhưng câu KHÔNG đổi một ký tự.** Ô khai báo bị
cắt trước khi chấm và thước là hàm tất định, nên ở những bước ấy `exec` **không thể** đổi. Hai phần
ba công của phần thưởng rơi vào chỗ thước không nhìn thấy. Toàn bộ 197 lần đổi chiều của `exec` nằm
gọn trong 961 bước có câu thay đổi.

**Bài học phương pháp:** phần thưởng đặt ở **tầng biểu diễn trung gian** nâng đúng tầng đó, nhưng
**không có số hạng nào ràng buộc tầng đầu ra**. Khi trọng số dịch chuyển, câu ở đầu ra đổi theo cả
ở những bước phần thưởng không có tín hiệu, và mức thiệt ở đó vừa đủ xoá phần lợi.

---

## 5. ⭐ ĐIỂM NGHẼN THẬT: nhận diện phần tử, không phải viết câu

Phân tầng theo việc ô khai báo của MIN có đúng hay không (tên khớp **và** toạ độ trong ±14%):

| tầng | n | MIN | GRPO | S1 | Base | **câu chuẩn** |
|---|---|---|---|---|---|---|
| khai báo **đúng** | 2.106 | **87,1** | 85,5 | 78,3 | 67,3 | **86,3** |
| khai báo **sai** | 1.367 | 21,8 | 25,7 | 32,9 | 25,1 | **61,4** |
| không có tên chuẩn | 990 | 55,3 | 53,5 | — | — | 73,0 |

⭐⭐ **Khi mô hình nhận ĐÚNG phần tử, nó đạt 87,1 — vượt cả câu chuẩn 86,3.** Tầng viết câu đã hết
dư địa. **Toàn bộ khoảng cách 15,7 điểm còn lại nằm ở 1.367 bước nhận SAI phần tử** (21,8 so với
61,4 của câu chuẩn).
⚠️ Lát cắt này định nghĩa bằng hành vi của chính mô hình ⇒ **hậu kiểm**; ô 87,1 vượt 86,3 chính là
dấu hiệu hiệu ứng chọn mẫu, phải khai chứ không được trình như năng lực.

**Dạng lỗi, tái lập ba lần độc lập:** khi mô hình gọi sai phần tử, nó nhìn sang **vùng khác hẳn**
màn hình chứ không nhầm hai nút cạnh nhau — lệch trung vị **351** (lượt on-policy) / **398**
(nhánh ứng viên) / **359** (lượt GRPO) đơn vị trên lưới 1000. Trong 184 bước GRPO lật đúng, MIN vốn
lệch trung vị 359 với **51,6% lệch quá 350**, chỉ 17,9% nằm sát ngưỡng.

---

## 6. ⭐ TRẦN CỦA VIỆC GHÉP NHÁNH (đo 6/9, số mới)

Nếu biết trước nhánh nào trúng ở từng bước (oracle):

| ghép | `exec` |
|---|---|
| MIN một mình | 60,05 |
| S1/202 + MIN | **67,04** |
| Base + S1/202 + MIN | **70,24** |
| Base + S1/202 + MIN + gui_sel | 71,45 |
| **cả 8 nhánh** | **72,80** |
| câu chuẩn | 75,73 |

⭐ Tám nhánh cộng lại phủ **72,80**, gần chạm trần dụng cụ. **Base (47,59) lọt vào bộ ba tốt nhất**
vì nó sai khác kiểu với các nhánh đã tinh chỉnh.
· Chỉ **878 bước (19,7%)** là không nhánh nào trúng **và** câu chuẩn cũng trượt — đó là vùng mù của
  dụng cụ.

**Nhưng bốn luật chọn rẻ đều không bắt được dư địa đó** (0 GPU, trên 6 nhánh có đủ tệp dự đoán,
oracle của 6 nhánh này là 69,86):

| luật chọn câu | `exec` |
|---|---|
| luôn dùng MIN | 60,05 |
| chọn câu dài nhất | 59,15 |
| chọn câu ngắn nhất | 57,18 |
| chọn câu khớp chữ OCR trên màn nhiều nhất | 59,11 |
| **chọn câu mà đa số nhánh đồng ý** | **60,36** |
| *oracle 6 nhánh* | *69,86* |

Luật tốt nhất được **+0,31 pp**, dưới MDE. Khoảng cách **9,8 điểm** giữa luật rẻ nhất và oracle là
cái giá của việc không có bộ định tuyến.

---

## 7. NHỮNG HƯỚNG ĐÃ ĐÓNG, kèm số đóng chúng

Phiên debate **không nên đề xuất lại** những hướng này trừ khi có lập luận mới bác được số:

1. **Vá lỗi của chính lượt GRPO** (thêm số hạng bảo vệ tầng đầu ra). Trần: nếu triệt tiêu hoàn
   toàn cả ba nguồn cản thì `exec` chỉ lên **62/4.463 = +1,39 pp**, vẫn dưới MDE 2,2.
2. **Kéo dài lượt GRPO.** `frac_reward_zero_std` đã 0,515 và `r_point` phẳng ở chặng cuối.
3. **Chọn giữa MIN và GRPO bằng ngưỡng tự tin.** Oracle hai nhánh chỉ +2,22 pp, vừa chạm MDE, mà
   đòi bộ định tuyến đã đo hai lần độc lập là không có: quét ngưỡng trên điểm chuỗi cho AUC biên
   **0,69–0,72** và luật null thắng; nhánh ứng viên bỏ cuộc mù với likelihood của chính nó.
4. **Viết câu hay hơn.** Tầng này đã vượt mốc câu chuẩn (87,1 vs 86,3) ở nhóm nhận đúng phần tử.
5. **Khối ứng viên (`gui_sel`).** Đã chạy: 56,13, thấp hơn MIN. Cơ chế chọn không hỏng (nhóm dám
   chọn đạt 71,41) nhưng bỏ cuộc quá mức 27,27%; ép chọn thì độ đúng cả bước **tụt** 63,3 → 50,0.
6. **Ngưỡng τ trên điểm chuỗi** để lật quyết định bỏ cuộc. Đã quét đủ 1.400 bước dev: luật null
   thắng, lift tốt nhất +8/1.400 so với ngưỡng cần 18. Chuẩn hoá theo độ dài làm hỏng xếp hạng
   (top-1 đúng 38,3% so với 67,5% khi dùng tổng log-prob).
7. **Học từ chính đầu ra của mô hình (on-policy) ở tầng khai báo.** Tỉ lệ cặp hợp lệ chỉ 3,3% so
   với ngưỡng 25%. Lý do đo được: lỗi lưỡng cực, 76,5% bước sai nằm ngoài dải cần thiết.
8. **Đổi bộ trỏ mạnh hơn khi chấm.** Đã thử UI-Venus-Ground-7B: cho điểm **thấp hơn** ở cả ba
   nhánh, và nâng thì nâng **đều** mọi nhánh nên tỉ lệ không đổi.
9. **Đổi luật chấm sang luật lỏng hơn.** Nâng cả sàn lẫn trần; và dưới luật đĩa thì MIN ngang S1
   (69,2 vs 69,2), tức xoá luôn mức chênh. Ngoài ra vi phạm ranh giới ở mục 0.

---

## 8. RÀNG BUỘC THỰC TẾ

**Máy.** Không có GPU tại chỗ. Bậc thang chi phí bắt buộc đi từ trên xuống:
CPU (0 đồng) → **Kaggle T4×2 miễn phí, 30 giờ/tuần** → L4 → A100 (đắt nhất, trả tiền).
Đo thật: suy luận 4.463 bước trên T4 mất **3,1 giờ** (0,4 bước/giây); chấm `exec` 4.463 bước mất
**5,4 giờ** (0,23 bước/giây). Train một epoch đầy đủ trên A100 khoảng **23 giờ**.
Chủ luận văn đã chốt **ưu tiên tiết kiệm chi phí**; bước tốn tiền phải hỏi trước.

**Dữ liệu đã có sẵn, không phải mua:** 64.567 ảnh tập dạy + 6.958 ảnh tập kiểm (đã có trên máy);
cây trợ năng của 99.131 màn hình (⚠️ chỉ **12,6%** phần tử có tên, đo trên 120 màn lấy ngẫu nhiên);
OCR đã trích cho toàn bộ hai tập; khối ≤40 ứng viên mỗi màn đã dựng sẵn (`candidates.jsonl`);
mọi tệp dự đoán và tệp chấm thô của 8 nhánh.

**Tài sản quan trọng:** giữ `*_raw.jsonl` nên **đổi luật chấm hay đổi cách ghép nhánh đều tính lại
được mà không gọi lại bộ trỏ** — mọi phép đo ở mục 4, 5, 6 đều 0 GPU.

---

## 9. CÂU HỎI CHO PHIÊN DEBATE

1. Với chẩn đoán *"điểm nghẽn là nhận diện phần tử, tầng viết câu đã hết dư địa"*, can thiệp nào
   tấn công đúng chỗ đó mà **chưa** nằm trong mục 7? Nêu rõ dữ liệu lấy từ đâu (phải có sẵn), mục
   tiêu huấn luyện là gì, và chi phí theo bậc thang ở mục 8.
2. Có tín hiệu nào chọn được câu đúng trong 6–8 câu của các nhánh, **không dùng bộ trỏ chấm**, mà
   bắt được một phần khoảng cách 9,8 điểm tới oracle 69,86? Nếu bắt được một phần ba thì `exec` lên
   ~63–64, tức vượt MDE. Ước lượng phải dựa trên số có thật.
3. Trong văn liệu đã bình duyệt, có kỹ thuật nào nâng độ chính xác **nhận diện phần tử GUI** mà
   khả thi với mô hình 3B, QLoRA, Kaggle T4 miễn phí? (Ví dụ cần kiểm: đánh dấu phần tử lên ảnh,
   đưa cây trợ năng vào đầu vào, chưng cất từ một mô hình định vị ngoài họ Qwen.) ⚠️ Phải xác minh
   venue tận nguồn; dự án cấm trình bản tiền ấn phẩm như đã bình duyệt.
4. Nếu kết luận là **không còn cách nào trong ngân sách**, hãy chứng minh bằng số thay vì bằng lời,
   và nói rõ con số nào đóng hướng nào.

---

## 10. TỆP ĐỂ TRA THÊM (nếu cần, nhưng file này đã tự chứa)

`report/144_KET_QUA_GRPO_POINT_6_9.md` — lượt GRPO đầy đủ, tám đòn phản biện ·
`report/145_CHOT_HUONG_SAU_GRPO_6_9.md` — phán quyết dừng thực nghiệm và các trần đã tính ·
`report/143_DEBATE_NANG_SO_MO_HINH_5_9.md` — debate nâng số vòng trước ·
`report/106_DANG_KY_TRUOC.md` mục (x19), (x19d), (x20) — thiết kế và luật đọc đã khoá ·
`CLAUDE.md` — bối cảnh toàn dự án, bảng số đã rút, luật vận hành máy ·
`runs/grpo_point/` — adapter, tệp dự đoán, tệp chấm thô, nhật ký huấn luyện ·
`harness/doc_exec_grpo.py` và `harness/doc_grpo_local.py` — hai script đọc kết quả, 0 GPU.
