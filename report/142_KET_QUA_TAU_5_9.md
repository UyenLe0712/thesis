# 142 — Kết quả quét ngưỡng τ trên lát dev 1.400 (5/9/2026) và phán quyết lượt ②

> Đầu vào: `runs/sel/seqscores_gui_sel_seed101_dev1400_gpu0.jsonl` + `_gpu1.jsonl` (700 + 700,
> hai commit Kaggle nối tiếp, chữ ký `seqscore:gui-sel-adapter`). Kiểm toàn vẹn 7/7: 0 dòng hỏng
> · khoá rời · phủ đúng 1.400 bước dev · một chữ ký · `tok_none` = 7 ở cả 1.400 · điểm âm ở mọi
> ứng viên · `scores` đủ `n_cand` · 783 dòng của commit 1 trùng khít giá trị trong bản nối tiếp.
> Mã: `harness/quet_tau.py` (thi hành (x16d) + (x17f) của `106`). Kết quả máy: `runs/sel/tau_scan.json`,
> `runs/sel/tau_scan_stdout.txt`, bảng theo bước `runs/sel/tau_rows_dev1400.json`. 0 giây GPU ở khâu này.

## 1. Kết quả — luật null thắng ở cả bốn nhánh

n = 1.400 · có ứng viên vàng (HasAns) 1.008 (72,0%) · không có (NoAns) 392.
Luật null = greedy hiện tại: đúng **888/1.400 = 63,43%** · bỏ cuộc sai 275 · %none 41,6 ·
`sel_acc`(HasAns) 57,54%.

| nhánh | định nghĩa | τ\* | đúng /1.400 | lift | KTC95 bootstrap | ngưỡng | kết cục |
|---|---|---|---|---|---|---|---|
| **X** (x16d) chính | điểm/token, phát c\* nếu m > τ | +1,229 | 528 (37,71%) | **−360** | [−397 · −322] | 18 | không đạt |
| A (x17f) lai, chuẩn hoá | greedy chọn ⇒ giữ; greedy none ⇒ c\* nếu m > τ | +1,529 | 889 (63,50%) | **+1** | [0 · +4] | 24 | không đạt |
| B (x17f) tổng log-prob | argmax Σlog p, phát nếu m_sum > τ | −2,328 | 836 (59,71%) | **−52** | [−83 · −21] | 24 | không đạt |
| C (x17f) lai, tổng | greedy chọn ⇒ giữ; greedy none ⇒ c\* của B nếu m_sum > τ | −1,456 | 896 (64,00%) | **+8** | [−11 · +27] | 24 | không đạt |

Mốc tiên nghiệm τ₀ = −log(0,5478/0,291) = −0,633 (Menon et al., ICLR 2021, dạng post-hoc) áp lên
m_sum: nhánh B **745** (53,21%, kém null 143 bước) · nhánh C **889** (+1).

⭐ **Phán quyết theo (x17b), đã khoá trước khi có số: KHÔNG chạy lượt ② `gui_sel_cham`/101.**
Không nhánh nào tới ngưỡng; nhánh gần nhất (C) đạt một phần ba ngưỡng và KTC phủ 0. Câu hỏi hạt
202 ở (x17b) trở thành vô nghĩa. Dự đoán ghi trước ở `report/136` mục 8 (*"0–3 pp, khả năng
luật null thắng là thật"*) đúng: mức tốt nhất +0,57 pp.

## 2. Vì sao τ thất bại — chẩn đoán trên chính 1.400 bước

### 2.1 Phần xếp hạng ứng viên KHÔNG hỏng; phép chia số token mới hỏng

Ép chọn trên 1.008 bước HasAns (τ = −∞):

| cách xếp hạng | vàng đứng đầu |
|---|---|
| điểm/token (x16d) | 386/1.008 = **38,3%** |
| tổng log-prob | 680/1.008 = **67,5%** |
| greedy khi mô hình tự chọn (733 bước) | 580/733 = 79,1% (precision) |
| ép chọn bằng sinh, đo 3/9 | `sel_acc` 69,5% |

Ứng viên greedy chọn trùng top-1 theo tổng log-prob **701/814**, trùng top-1 theo điểm/token
chỉ 390/814. Vậy xếp hạng theo tổng log-prob **là** cái greedy đang làm; phép chuẩn hoá độ dài
ưu ái span dài mà từng token dễ đoán (top-1 theo điểm/token dài trung vị 25 token, theo tổng
20 token). Phát hiện của probe 50 bước (x17f) tái lập ở 1.400 với đúng chiều và đúng cỡ.
Đây là lý do X âm 360 bước: nó phá phần xếp hạng vốn đang đúng.

### 2.2 Phần bỏ cuộc mới là điểm nghẽn, và điểm của chính mô hình không phân biệt được

AUC (0,5 = mù) của biên m khi tách HasAns khỏi NoAns:

| tập | m theo điểm/token | m theo tổng |
|---|---|---|
| toàn 1.400 | 0,708 | 0,781 |
| **trong 583 bước greedy bỏ cuộc** (275 sai · 308 đúng) | 0,555 | 0,693 |
| 120 bước cứu được (bỏ cuộc sai ∧ c\* tổng đúng) vs 308 bỏ cuộc đúng | — | **0,724** |

Trung vị điểm theo nhóm cho thấy hai nhóm mà τ cần tách **gần như trùng**:

| nhóm | n | s_none | s_star | m_sum |
|---|---|---|---|---|
| HasAns, greedy bỏ cuộc (sai) | 275 | −1,706 | −0,597 | −1,922 |
| NoAns, greedy bỏ cuộc (đúng) | 308 | −1,710 | −0,629 | −2,999 |
| HasAns, greedy chọn đúng | 580 | −1,985 | −0,625 | +0,313 |

Điểm của thẻ `none` **giống hệt** ở bước có vàng và bước không có vàng khi mô hình đã bỏ cuộc.
Tức khi mô hình nói `none`, xác suất nó gán cho `none` không mang thông tin về việc vàng có
trong khối hay không. Mọi ngưỡng đặt lên biên đều lật gần cùng tỉ lệ bước đúng và bước sai:
để cứu 120 bước phải trả ~308 × (1 − 0,724)/0,724 ≈ 1 bước sai cho mỗi bước cứu được, và
đó đúng là đường cong C: đỉnh +8 rồi đi xuống.

Trong 275 bước bỏ cuộc sai, chỉ **120 (43,6%)** có ứng viên đúng đứng đầu theo tổng log-prob.
Trong 120 bước đó, **32,5%** câu sinh ra mang động từ không chạm (swipe/back/type…) so với 1,6%
ở nhóm đưa ra lựa chọn ⇒ dù lật thẻ, câu vẫn sai loại thao tác, `exec` không tăng. Phần thật
sự cứu được về `exec` ước ~80/1.400 nếu cổng bỏ cuộc hoàn hảo — mà cổng không hoàn hảo.

### 2.3 Trần lý thuyết và khoảng cách

Nếu cổng bỏ cuộc hoàn hảo (biết trước bước nào có vàng): giữ greedy khi chọn, lấy top-1 tổng
khi greedy bỏ cuộc ⇒ **1.092/1.400 = 78,0%** so với null 63,43. Khoảng 14,6 điểm nằm **trọn** ở
cổng bỏ cuộc, và cổng ấy không đọc được từ likelihood của chính mô hình (AUC 0,69–0,72). Đây là
con số khoá lại nhánh: điểm nghẽn có thật, nằm đúng chỗ đã chẩn đoán, nhưng không sửa được ở
khâu suy luận.

### 2.4 Cỡ khối

| cỡ khối | n | HasAns | %none greedy | m_sum HasAns | m_sum NoAns | AUC |
|---|---|---|---|---|---|---|
| 6–10 | 255 | 74,1% | 30,6 | +0,084 | −3,149 | 0,842 |
| 11–20 | 367 | 74,4% | 38,7 | −0,344 | −2,400 | 0,744 |
| 21–30 | 290 | 75,2% | 40,7 | −0,442 | −1,810 | 0,749 |
| 31–40 | 488 | 67,2% | 50,2 | −0,482 | −2,794 | 0,790 |

Tỉ lệ bỏ cuộc tăng đơn điệu theo cỡ khối (tái lập `report/136`), nhưng tỉ lệ HasAns gần phẳng
⇒ mô hình bỏ cuộc theo **độ đông của khối**, không theo việc vàng có mặt hay không. Cỡ khối
một mình cũng không tách được nhóm cứu được khỏi nhóm bỏ cuộc đúng (AUC 0,466).

## 3. Ý nghĩa cho hướng mô hình

1. **Giả thuyết lệch tiên nghiệm (Rajpurkar 2018) không được phép thử rẻ ủng hộ.** Hiệu chỉnh
   logit theo tiên nghiệm (τ₀) là bản suy luận của việc cân lại nhãn `none` khi huấn luyện
   (Menon 2021); nó cho −143 và +1. Nếu bỏ cuộc quá mức chỉ do 54,78% `none` trong tập dạy thì
   dịch chuyển này phải cứu được phần lớn 275 bước. Nó không cứu được vì mô hình không phân
   biệt được hai loại bước, không phải vì ngưỡng đặt sai chỗ. Lượt ② đổi tiên nghiệm, không
   đổi năng lực phân biệt ⇒ 15 giờ A100 ấy nhiều khả năng cho cùng kết cục. Đó là lý do luật
   (x17b) nối hai việc với nhau, và luật đó nay quyết **không chạy**.
   ⚠️ Giới hạn của lập luận: huấn luyện lại còn bỏ 2.495 bước không chạm, tức bỏ luôn đường
   tắt *"động từ không chạm ⇔ none"* (38,9% câu ở nhóm bỏ cuộc sai mang động từ không chạm).
   Hiệu ứng đó τ₀ không mô phỏng được. Nhưng luật đã khoá trước khi thấy số, và không nới.
2. **Nhánh ứng viên đóng ở chẩn đoán.** Đóng góp mô hình của luận văn giữ ở MIN-DESC 60,05
   (Voronoi) / 62,69 (D.3∧14%) / 66,55 (D.3). Cascade `gui_sel`;none→MIN 60,72 vẫn trong dải trắng.
3. **Cái mang đi được từ lượt này** (đúng cam kết (x17e) báo cả khi null thắng):
   · điểm nghẽn định lượng: 14,6 điểm trên dev nằm trọn ở cổng bỏ cuộc, cổng ấy mù với
     likelihood của chính mô hình (AUC 0,69–0,72);
   · chuẩn hoá độ dài phá xếp hạng span trong khối ứng viên (38,3 vs 67,5) — đáng một đoạn
     ở hạn chế của thủ tục, và là lý do mọi thước sequence-score cho GUI phải khai cách chuẩn hoá;
   · mô hình bỏ cuộc theo độ đông khối, không theo sự có mặt của vàng.

## 4. Không làm

Không nới 18/24 · không đổi tiêu chí sang HasAns · không thêm nhánh thứ năm · không dùng
dev 1.400 để khớp một bộ phân loại bỏ cuộc rồi báo trên 3.062 (cùng mù, AUC trần ~0,78; và
là đầu mới) · không chạy `gui_sel_cham` với lý do *"τ₀ không mô phỏng hết"* — lý do đó đúng
nhưng đến sau khi thấy số.
