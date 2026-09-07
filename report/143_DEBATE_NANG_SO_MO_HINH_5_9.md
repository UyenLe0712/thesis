# 143 — Debate: còn đóng góp mô hình nào đưa `exec` từ 60,05 lên 65–70? (5/9/2026 tối)

> Câu hỏi của chủ luận văn: *"60,05% là quá thấp, tôi cần 65–70% so với 75,7 của câu chuẩn."*
> Vai: bên A muốn số cao · bên B giám khảo khó tính · trọng tài đo bằng tệp thô (0 GPU) và tiền lệ
> đã mở tận nguồn. Số mới đo trong file này: `runs/score_min_desc_seed101_raw.jsonl` +
> `preds_min_desc_seed101.jsonl` + `descriptors.jsonl`. Tiền lệ mới: UI-TARS (Qin et al., 2025,
> arXiv 2501.12326, Bảng 8, đọc từ PDF trang 25) · UI-R1 (Lu et al., AAAI 2026, arXiv 2503.21620).

## 0. Khung: con số bị chặn bởi MỘT năng lực — nhận ra phần tử cần chạm

Chia 4.463 bước theo việc ô khai báo của MIN-DESC đúng (tên khớp **hoặc** điểm trong ±14%) hay sai:

| nhóm | n | % | MIN | S1 | câu chuẩn | gui_sel |
|---|---|---|---|---|---|---|
| khai báo **đúng** | 3.329 | 74,6 | **78,6** | 71,0 | 80,9 | 68,2 |
| khai báo **sai** cả tên cả điểm | 1.102 | 24,7 | **5,0** | 24,2 | 60,5 | 20,7 |
| không sinh khai báo | 17 | 0,4 | 0,0 | 0,0 | 58,8 | 0,0 |

Khi khai báo đúng, MIN **kém câu chuẩn 2,3 điểm** — phần viết câu đã gần chạm trần. Khi sai, MIN
rơi xuống **5,0**, dưới cả sàn câu rỗng nghĩa (12,0): câu gọi tên một nút không tồn tại còn tệ hơn
không gọi tên. Toàn bộ khoảng cách tới trần nằm ở **1.102 bước chọn sai phần tử**.

Quy đổi (giữ exec|đúng = 78,6 và exec|sai = 5,0):

| mục tiêu exec | cần độ chính xác khai báo | hiện |
|---|---|---|
| 65 | **82,1%** | 74,6% |
| 70 | **89,0%** | 74,6% |

Mốc ngành cho đúng năng lực này (chọn phần tử từ mục tiêu + lịch sử + màn, **không** có câu bước —
đúng thiết lập *AndroidControl-High*, cột *Grounding*, UI-TARS Bảng 8): SeeClick 62,9 · OS-Atlas-4B
73,8 · Qwen2-VL-7B (tinh chỉnh) 77,7 · UI-TARS-2B 78,4 · OS-Atlas-7B 78,5 · UI-TARS-7B 80,5 ·
**UI-TARS-72B 81,5**. ⚠️ Thước của họ là "điểm trong hộp" trên bước đúng loại thao tác, gần D.3;
của ta là tên khớp hoặc ±14% — cùng cỡ, không trùng định nghĩa, chỉ dùng để định vị.

⇒ **65% đòi độ chính xác chọn phần tử ngang UI-TARS-72B; 70% đòi vượt mọi agent GUI đã công bố
trên AndroidControl-High**, với một mô hình 3B và 64.567 bước dạy, không tiền huấn luyện GUI. Đây
không phải câu "phương pháp yếu"; đây là câu "mục tiêu đặt ở ngoài biên hiện tại của ngành". Mọi
đòn bẩy dưới đây phải đọc trên nền đó.

Oracle định tuyến giữa các nhánh đã có (biết trước nhánh nào trúng): MIN∪S1 **66,77** · MIN∪sel
66,10 · MIN∪S1∪sel **68,65** · trần 75,73. 475 bước (10,6%) câu chuẩn trúng mà cả ba nhánh trượt.

## 1. Bảy đòn bẩy, mỗi đòn một lượt A/B

### ① Sửa bỏ cuộc của `gui_sel` (bộ phân loại riêng, hoặc train lại chỉ bước chạm)
**A:** khi dám chọn `gui_sel` đạt 71,41, cao nhất mọi nhánh; triệt bỏ-cuộc-sai ⇒ 65,44 trên 4.463.
**B:** 65,44 là oracle. `report/142`: likelihood của chính mô hình mù với việc vàng có trong khối
hay không (AUC 0,69–0,72); mô hình bỏ cuộc theo độ đông khối. Một bộ phân loại riêng phải học đúng
điều mô hình không học được từ cùng đầu vào; không có lý do nó giỏi hơn. Train lại chỉ bước chạm:
phép thử rẻ τ₀ (tương đương cân lại tiên nghiệm) cho −143/+1 ⇒ không ủng hộ; luật (x17b) đã đóng.
**Phán quyết:** kỳ vọng thật **+0…+2**, 15 h A100, và phải khai là quyết định mới sau khi thấy số.
Không ưu tiên.

### ② Định tuyến MIN / S1 / gui_sel bằng độ tin cậy
**A:** oracle 66,77–68,65, chỉ cần bộ định tuyến "đủ tốt".
**B:** mọi luật ghép theo cỡ khối / độ dài đã đo ≤ 60,72 (`138`). Định tuyến cần dự đoán *khai báo
của MIN có đúng không* — đúng tín hiệu vừa thất bại ở `gui_sel`. Điều **chưa đo**: log-prob của
span khai báo của MIN có tương quan với đúng/sai không. Đo được với ~6 h Kaggle (teacher-force
4.463 span). Nếu AUC ~0,75 thì gain ≈ +1…+2; nếu ≤0,7 (như gui_sel) thì 0.
**Phán quyết:** phép dò rẻ, đáng chạy **trước** khi tiêu A100, nhưng không phải đòn chính; và hệ
hai mô hình khó gọi là "đóng góp mô hình".

### ③ Tính toán lúc suy luận: self-consistency trên ô khai báo
**A:** lấy mẫu 8 khai báo (temperature), bỏ phiếu theo phần tử, viết câu theo phần tử thắng
(Wang et al., ICLR 2023; cùng họ với "region consistency" cho grounding, arXiv 2508.05615).
**B:** không sửa được lỗi *lưỡng cực* đã đo (76,5% sai lệch trung vị 351 px: mô hình nhìn sang
vùng khác hẳn, không dao động quanh nút đúng); bỏ phiếu chỉ giúp khi các mẫu phân tán quanh đáp
án. Tốn 8× suy luận (~20 h Kaggle). Không phải đóng góp mô hình.
**Phán quyết:** **+0,5…+1,5**, để cuối, chỉ khi còn hạn mức.

### ④ Mục tiêu ưu tiên theo executability: lấy mẫu → chấm bằng bộ trỏ thứ hai trên tập DẠY → ORPO/DPO
**A:** đây là đòn đánh **thẳng vào đại lượng cần nâng**. Tập dạy có toạ độ vàng cho 41.191 bước
chạm. Lấy N = 8 câu/bước từ MIN trên một tập con, cho **UI-Venus** (không phải UGround) trỏ, gán
nhãn *executable / không* theo đúng luật Voronoi gated, dựng cặp (chosen = executable, rejected =
không), train ORPO tiếp từ MIN. Ba lý do nó khác MIN-ONPOLICY đã chết: (i) eligibility — với
p ≈ 0,6 và 8 mẫu, P(có cả hai loại) ≈ 1 − 0,6⁸ − 0,4⁸ ≈ **98%**, so với 3,3% của on-policy vì
on-policy đòi *cùng phần tử gọi khác tên*; (ii) cặp phạt đúng lỗi thật (chọn sai phần tử, gọi tên
không trỏ được), không phải lỗi giả định; (iii) tín hiệu là *hành vi của người đọc độc lập*, tức
đúng construct của thước. Tiền lệ: RL/ưu tiên với phần thưởng kiểm chứng được cho GUI trên 3B cho
mức tăng lớn — UI-R1-3B (AAAI 2026) nâng grounding AndroidControl-Low 72,3 → 82,6 chỉ với 136 mẫu
(so với zero-shot, không so với SFT đủ dữ liệu — phải khai đúng).
**B:** ba đòn. *Goodhart:* huấn luyện theo phần thưởng cùng construct với thước. Đỡ được **một
phần**: bộ trỏ thưởng (UI-Venus) ≠ bộ trỏ chấm (UGround), phép B đã cho thấy hai bộ trỏ đồng ý về
thứ tự nhánh nhưng lệch 2,8–4,1 điểm; phải báo cả hai bộ trỏ, và phải báo `f3`-style: câu có bị
biến thành "mật mã cho bộ trỏ" không (đo bằng BLEU/ROUGE với câu chuẩn không được sụt, và phép
người đọc 100 câu nếu cần). *Trần:* nó không tạo ra năng lực nhìn mới; nó chỉ dạy mô hình *im
lặng đúng chỗ* và *gọi tên theo cách bộ trỏ hiểu*. Trong 1.102 bước khai báo sai, câu chuẩn trúng
60,5% ⇒ có chỗ; nhưng MIN đang ở 5,0 vì gọi tên sai, ORPO có thể kéo về mức S1 (24,2) chứ khó tới
60. Ước: chuyển 1/3 số bước sai từ 5,0 lên 24,2 ⇒ +1,6; cộng phần "đúng phần tử nhưng câu chưa
trỏ được" (78,6 → 80,9, +1,7 tối đa) ⇒ **+2…+4**, kịch trần ~+5. *Giá:* sinh 8 × ~5.000 bước
(T4, 0,4 bước/s ⇒ ~28 h) + UI-Venus 40.000 lượt trỏ (4 s ⇒ ~44 h) ⇒ **~70 h Kaggle (2,5 tuần
hạn mức)** + ORPO ~5–10 h A100. Có thể cắt N = 4 và 3.000 bước ⇒ ~25 h Kaggle, giá là ít cặp hơn.
**Phán quyết:** **đòn bẩy có kỳ vọng/giá tốt nhất và là đóng góp mô hình thật** (mục tiêu huấn
luyện mới, nối tiếp câu chuyện ORPO của FAIR). Kỳ vọng thực **62–64**, không phải 65 một mình.

### ⑤ Backbone lớn hơn (Qwen2.5-VL-7B) hoặc backbone đã tiền huấn luyện GUI
**A:** UI-TARS Bảng 8: 2B → 7B nâng grounding AC-High 78,4 → 80,5; OS-Atlas 4B → 7B 73,8 → 78,5.
**B:** +2…+5 điểm khai báo ⇒ **+1…+3 exec**; phải train lại **cả S1 lẫn MIN** (~70 h A100 + 2 lượt
chấm) vì mọi phép so nội bộ đòi cùng backbone; bộ nhớ chưa đo ở cutoff 2560. Backbone GUI (OS-Atlas,
UI-TARS) có AndroidControl trong dữ liệu ⇒ phải truy lại rò rỉ tập kiểm, và cùng họ Qwen với bộ
trỏ — đòn "cùng họ" nặng thêm. Quyết định 30/8 giữ 3B vẫn đúng lý do; đây là đánh đổi ngân sách,
không phải phương pháp.
**Phán quyết:** đòn thứ hai nếu còn ngân sách; **không** là đóng góp.

### ⑥ Thêm dữ liệu có câu bước (GUI-Odyssey, AITZ)
**B:** UI-TARS/OS-Atlas dùng hàng triệu màn và vẫn dừng ở 78–81 grounding High. Thêm vài chục
nghìn bước không đổi hạng. Pipeline ghép nguồn mới tốn tuần công. **Loại.**

### ⑦ Đổi cách trình (D.3 báo kèm)
MIN 66,55 / câu chuẩn 83,82 dưới D.3 — đúng luật "điểm trong hộp" mà chính UI-TARS/OS-Atlas dùng
cho cột Grounding. Tỉ lệ so trần không đổi (79%). Đã làm; không phải đóng góp mô hình.

## 2. Xếp hạng và tổng cộng thực tế

| đòn | kỳ vọng exec | giá | là đóng góp mô hình? |
|---|---|---|---|
| ④ ORPO theo executability (UI-Venus thưởng) | **+2…+4** | ~25–70 h Kaggle + 10 h A100 | **có** |
| ⑤ backbone 7B | +1…+3 | ~70 h A100 + 2 lượt chấm | không |
| ② dò độ tin cậy khai báo của MIN | 0…+2 | ~6 h Kaggle | yếu |
| ③ self-consistency | +0,5…+1,5 | ~20 h Kaggle | không |
| ① sửa bỏ cuộc gui_sel | 0…+2 | 15 h A100 | đã đóng |

Cộng dồn lạc quan ④+⑤+③ ≈ **+4…+8 ⇒ 64–68**; thực tế **63–65**. **70 không có đường nào có
bằng chứng**: nó đòi 89% chọn đúng phần tử, trên mức UI-TARS-72B.

## 3. Đề nghị của trọng tài

1. **Chấp nhận khung §0 khi bảo vệ**: in 74,6% khai báo đúng cạnh cột Grounding AC-High của bảng
   UI-TARS (62,9–81,5), nói thẳng *phần viết câu đã gần trần (78,6 vs 80,9), phần còn lại là bài
   toán agent chưa ai giải ở 3B*. Đây là lá chắn mạnh hơn mọi điểm số.
2. Nếu vẫn muốn nâng số: chạy **④** như một **quyết định mới ghi ở (x19)**, khoá trước: N, cỡ
   tập con, luật cặp, bộ trỏ thưởng = UI-Venus, bộ trỏ chấm = UGround, ngưỡng đọc = MDE 2,2 trên
   4.463, một hạt = TRẮNG, báo BLEU/ROUGE để bắt "mật mã cho bộ trỏ". Kỳ vọng ghi trước: +2…+4.
3. **⑤ chỉ sau ④** và chỉ nếu ④ dương — nếu ④ trắng thì 7B không cứu được, vì hai đòn tác động
   hai chỗ khác nhau nhưng cùng bị chặn bởi 1.102 bước chọn sai.
4. Không làm ①, ⑥; ③ để cuối; ② chạy như phép dò rẻ nếu rảnh T4.

## 4. Lượt phản biện thứ hai (cùng đêm) — ĐỔI KHUYẾN NGHỊ

### 4.1 Số mới: khối ứng viên KHÔNG thêm thông tin nhận diện

Bảng chéo trên 4.448 bước: khai báo của MIN đúng/sai × `gui_sel` chọn đúng / chọn sai / bỏ cuộc.

| MIN khai báo | gui_sel | n | exec MIN | exec sel | câu chuẩn |
|---|---|---|---|---|---|
| đúng | chọn đúng | 1.912 | 81,3 | 82,0 | 83,1 |
| đúng | chọn sai | 231 | 64,9 | 29,0 | 68,8 |
| đúng | bỏ cuộc | 1.186 | 76,9 | 53,7 | 79,8 |
| **sai** | chọn đúng | **171** | 5,3 | 67,8 | 69,6 |
| **sai** | chọn sai | 265 | 2,3 | 3,8 | 58,9 |
| **sai** | bỏ cuộc | 683 | 5,9 | 14,9 | 58,9 |

`gui_sel` đúng ở chỗ MIN sai chỉ **171 bước (3,8%)**; 948/1.119 bước MIN sai thì `gui_sel` cũng sai
hoặc bỏ cuộc. ⇒ Lỗi nhận diện là **lỗi chung của mô hình 3B trên chính bước đó**, không phải lỗi
cách trình ứng viên. Đòn ①/② (định tuyến, khối ứng viên) hạ hạng: trần thật của chúng ~+3, không phải oracle 66–68.
Cùng nhóm MIN sai: Base 18,5 · S1 24,2 · MIN 5,0 ⇒ **cam kết sai tên làm mất 13–19 điểm** trên
nhóm này so với không cam kết. Nếu biết lúc nào không nên gọi tên, thu lại được tới +4,7.

### 4.2 Đòn bẩy bị bỏ sót ở §1: **RL với phần thưởng kiểm chứng được, miễn phí, đúng chỗ nghẽn**

Tập dạy có **toạ độ vàng** cho 41.191 bước chạm. Ô `<point>` của khai báo có thể chấm **tức thời,
không cần bộ trỏ nào**: trong hộp / trong dung sai vàng ⇒ 1, ngoài ⇒ 0. Đây là phần thưởng kiểm
chứng được (RLVR) đặt **thẳng lên năng lực đang chặn số** (nhận diện phần tử), khác ④ ở ba điểm:
· **không Goodhart**: phần thưởng là nhãn vàng của bộ dữ liệu, không phải một bộ trỏ;
· **0 giờ Kaggle** cho phần thưởng (④ tốn 25–70 h UI-Venus);
· **không đòi cặp**: GRPO so nhóm G mẫu của chính mô hình, tự có tín hiệu khi nhóm lẫn đúng/sai.
  Với p(đúng) ≈ 0,75 và G = 4: P(nhóm lẫn) ≈ 1 − 0,75⁴ − 0,25⁴ ≈ **68%**; G = 8: **90%** —
  so với eligibility 3,3% đã giết MIN-ONPOLICY (vì luật cặp đòi *cùng phần tử khác tên*).

Tiền lệ (đã mở nguồn): **GUI-R1** (Luo et al., 2025, arXiv 2504.10458): RFT trên Qwen2.5-VL-3B
**thắng SFT cùng dữ liệu** — ScreenSpot 80,08 vs 63,55; **UI-R1-3B** (Lu et al., AAAI 2026):
grounding AndroidControl-Low 72,3 → 82,6 với 136 mẫu, phần thưởng "điểm trong hộp vàng" đúng dạng
đề xuất ở đây. **GUI-G²** (2507.15846) và "Self-critiqued RL for GUI grounding" (2510.27266) là
cùng họ. ⚠️ Tất cả đều RL cho **agent chọn hành động**; tìm nhanh **không thấy** bài nào dùng RLVR
cho **sinh câu hướng dẫn** GUI — ghi *"không tìm thấy"*, không ghi *"đầu tiên"*. Về hạ tầng: TRL
`GRPOTrainer` chạy Qwen2.5-VL-3B + LoRA trên **một GPU** (HF cookbook *Post training a VLM for
reasoning with GRPO*), ms-swift cũng hỗ trợ.

**Phản biện của B, và trả lời:**
· *"RL chỉ khuếch đại năng lực sẵn có, không tạo năng lực nhìn mới; 948 bước là lỗi chung thì
  RL với gì?"* — Đúng một phần: UI-R1 xuất phát từ base 72,3 và thêm +10; ta xuất phát từ 74,6
  sau SFT, biên còn lại hẹp hơn. Nhưng GUI-R1 cho thấy RFT **vượt SFT cùng dữ liệu** ở 3B, tức
  SFT chưa vắt hết năng lực; 948 bước "chung" là chung giữa ba mô hình *cùng được SFT một cách*.
  Kỳ vọng ghi trước: **+3…+6 điểm khai báo ⇒ +2…+4 exec**, trần lạc quan 65.
· *"Thưởng điểm mà chấm câu — tách rời."* — Hai đỡ: (i) câu sinh sau khai báo, KL về MIN giữ
  văn phong; (ii) thêm hạng thưởng nhỏ *tên trong khai báo xuất hiện trong câu* (chuỗi, 0 GPU).
  Có thể thêm hạng thưởng executability bằng UI-Venus **về sau**, làm biến thể, không phải chính.
· *"Hạ tầng mới, dự án đã mất máy vì hạ tầng."* — Đúng, đây là rủi ro lớn nhất. Đỡ bằng thăm dò
  12 phút theo luật P10 (mẫu **dài nhất**, không phải mẫu đầu) + đường lùi: **ORPO ngoại tuyến**
  với cặp lấy mẫu từ chính MIN (N = 8, nhãn điểm-trong-hộp, stage `dpo` LLaMA-Factory đã smoke)
  — cùng tín hiệu, hạ tầng đã chứng minh, giá ~28 h Kaggle sinh mẫu.
· *"Hộp vàng của ta là hộp tự suy (139)."* — Phần thưởng dùng **dung sai ±14% quanh điểm chạm
  vàng** (đúng luật cổng khai báo đã có), không dùng hộp; hoặc dùng cả hai dạng OR. Khai rõ.

### 4.3 Khuyến nghị cuối (thay §3 mục 2)

**Chạy RLVR-GRPO tiếp từ MIN-DESC/101, phần thưởng = ô `<point>` đúng (±14% quanh chạm vàng)
+ định dạng + tên-khai-báo-có-trong-câu; đường lùi = ORPO ngoại tuyến cặp lấy mẫu.** Lý do xếp
trên ④: cùng chỗ nghẽn, phần thưởng sạch hơn (không Goodhart), rẻ hơn (0 h Kaggle cho thưởng),
đóng góp rõ hơn (RLVR cho sinh hướng dẫn, chưa thấy tiền lệ). ④ thành hạng thưởng phụ về sau.

Giá ước (phải đo lại bằng thăm dò): GRPO G = 4, ~3.000–4.000 câu nhắc, 20–40 s/bước ⇒ **8–20 h
A100**; chấm exec **5,6 h Kaggle**. Đường lùi: ~28 h Kaggle + 5 h A100.

Đăng ký (x19) trước khi chạy, khoá: hạt 101 · điểm lưu MIN-DESC/101 · G, số câu nhắc, hàm thưởng
nguyên văn · tiêu chí thăm dò (không OOM trên 50 mẫu dài nhất; ≥60% nhóm lẫn đúng/sai trên 200
câu nhắc; reward trung bình tăng trong 100 bước) · đọc trên đúng 4.463 bằng Voronoi gated, so
MIN/101, MDE 2,2, một hạt = TRẮNG · BLEU-4/ROUGE-L với câu chuẩn **không được giảm quá 1 điểm**
(bắt "mật mã cho bộ trỏ") · báo dù ra sao. Kỳ vọng ghi trước: **+2…+4 exec**.

Điều **không** làm: thưởng bằng UGround (là bộ trỏ chấm) · chạm 4.463 khi chọn siêu tham số ·
dùng dev 1.400 làm tập thưởng (đó là tập kiểm).

## 5. Thi hành (5/9 đêm)

User quyết chạy. Đăng ký ở `report/106` **(x19)** (hệ, tập thưởng, hàm thưởng nguyên văn, ba tiêu chí thăm dò, cách đọc). Mã `harness/grpo_point.py` (selftest 0 GPU đạt), runbook `harness/colab_grpo_point.md` (G1–G7). Gói mã `_bundles/thesis_rented.zip` dựng lại 5/9.
