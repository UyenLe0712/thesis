# 328. Đánh giá GRPO + SPICE và cách thuyết phục thầy (1/11/2026)

Nhãn: **[đo]** là số tôi tính lại trong phiên này từ tệp thô, 0 GPU. **[val]** là số trên tập kiểm định C1, chỉ để giải thích, không trích làm kết quả. **[suy]** là suy luận chưa đo. Số không có nhãn lấy từ `report/259`, `261`, `320`. Lưới đang chạy chưa có số nào, mọi câu về lưới ở đây là dự đoán.

## 1. Kết luận

**Hiện tại chưa đủ để nói "GRPO + SPICE là tốt nhất", và tôi không nghĩ lưới một hạt giống sẽ làm được việc đó.** Phát biểu số đỡ được hiện nay hẹp hơn nhiều: học tiếp từ S1 bằng GRPO với phần thưởng so câu sinh với câu chuẩn làm tăng exec khoảng **+0,8 đến +1,55** so với S1/101 qua hai hạt, và ghép ngẫu nhiên thưởng thì mất hết mức tăng.

Năm phát hiện từ tệp thô đổi cách kể chuyện:

1. **Phần lặp lại được của mức tăng là sửa loại thao tác, không phải sửa tên phần tử.** ck500/101 ròng +69 bước = +28 (loại thao tác) + 41 (cả hai đúng loại). Hạt 202 ròng +37 = +32 + **5**. CIDEr-D (A2) ròng +38 = +35 + 3. Phần +41 chỉ có ở một hạt. [đo]
2. **+4,58 trên ACU gần như toàn là sửa loại thao tác, đo trên toàn bước chạm.** ck500 ròng +68 = +57 + 11 (84%), hạt 202 ròng +60 = +57 + 3 (95%). Chưa đo bước không chạm của ACU, đúng chỗ dịch về câu chạm gây hại. [đo]
3. **Tính cả bước không chạm, lợi ích gần như hết.** Trên 6.958 bước, lấy exec ở bước chạm và đúng loại thao tác ở bước không chạm: **+0,39 [−0,21; +0,99]**, ròng +27 bước. Tác hại cũng không riêng SPICE: thưởng CIDEr-D (A2_1000) có scroll 77,62, ck500 77,75, S1 83,97; tổng hợp của A2_1000 là +0,01 [−0,66; +0,68]. [đo]
4. **SPICE là phần thưởng dự báo exec kém nhất, cả trên test chứ không riêng val.** AUC trên câu S1/101: SPICE 0,671, CIDEr-D 0,741, METEOR 0,750. Trên 349 cặp câu bất đồng exec không qua chọn lọc: SPICE xếp đúng 72,2%, CIDEr-D 83,1%, METEOR và chrF 85,2%. [đo]
5. **Hiện chưa có bằng chứng SPICE hơn CIDEr-D.** A2_500 − ck500/101 −0,69 p = 0,040, nhưng A2_500 − ck500/202 **+0,02** p = 1. A2 còn lệch ba biến so với ck500 (2.000 câu nhắc, A100 bf16, có ghi log CTG), nên phép so này chưa sạch theo cả hai chiều. Câu ở ch6 "GRPO-SPICE đạt kết quả tốt nhất" không đứng được khi có hạt thứ hai. [đo]

Điểm vững thì có thật và nên nói rõ: nhánh ghép ngẫu nhiên, bốn dụng cụ, hai hạt, và hình thức câu không xấu đi (mục 2.1).

**Phát biểu đề nghị dùng thay "tốt nhất"**, cả khi lưới ra đẹp: *"GRPO thưởng SPICE thuộc nhóm dẫn đầu trong các cấu hình đã so; lý do chọn là chi phí, tiền lệ và không dùng bộ trỏ trong phần thưởng; mức tăng lặp lại được chủ yếu là sửa lỗi loại thao tác còn lại sau SFT, đổi lại có tác hại ở bước cuộn và quay lại."* Chỉ dùng được vế "nhóm dẫn đầu" nếu lưới cho đúng như vậy; mục 6 có bản cho trường hợp ngược lại.

---

## 2. Hiện đã đủ chưa, sau lưới sẽ đủ chưa

### 2.1 Những gì đứng vững

| bằng chứng | số | ghi chú |
|---|---|---|
| Ghép ngẫu nhiên thưởng | xao101 − S1 +0,00 [−0,41; +0,42], cứu 45 phá 45; ck500 − xao101 +1,55 [+0,80; +2,31] [đo] | Nhánh này chạy **cùng đường sinh** với ck500 nên đóng luôn nghi ngờ "lẫn đường sinh" nêu ở `report/259` §5.1 mà không cần chấm S1-hoà |
| Hai hạt GRPO | ck500/101 +1,55, ck500/202 +0,83; trung bình hai hạt − S1/101 **+1,19 [+0,44; +1,93]** [đo] | Nên dùng con số trung bình này; +1,55 là hạt cao hơn |
| So cả hai hạt S1 | TB hai hạt ck500 − TB hai hạt S1 +0,93 [+0,27; +1,59] [đo] | ck500 đều xuất phát từ S1/101, nên phép này chỉ là mô tả |
| Dụng cụ khác | UI-Venus +69 bước, đúng bằng UGround; phần cùng đúng loại +44 so với +41 [đo] | Câu của hạt 101 thật sự giúp, không phải đặc thù của bộ trỏ. Hạt 202 chưa chấm UI-Venus |
| Phi-4 không áp cổng loại thao tác | `dung` +0,69, ròng +31; kèm cổng +42 [đo] | Số Phi-4 đã báo chưa áp cổng mà vẫn dương, nên có một phần là nội dung, ở hạt 101 |
| Mức tác vụ | Mọi bước chạm đều trúng: S1 29,74, ck500 31,82 (+2,08 [+0,82; +3,35]), ck500/202 31,08 (+1,34 [0,00; +2,75]), xao101 29,74 (1.345 tác vụ, bootstrap theo tác vụ) [đo] | Lịch sử chuẩn. Mức cụ thể cho người đọc hình dung |
| Hình thức câu (F1 sơ bộ) | Xem dưới | Trả lời nhận xét của Liu về PG-SPICE |

F1 sơ bộ [đo], 4.463 bước:

| nhánh | số từ TB | lặp 2-gram | lặp 3-gram | kết thúc treo | dài > 20 từ | ≤ 2 từ |
|---|---:|---:|---:|---:|---:|---:|
| câu chuẩn | 7,84 | 6,27% | 0,34% | 0,16% | 0,27% | 0,25% |
| S1/101 | 7,85 | 3,56% | 0,13% | 0,22% | 0,22% | 0,78% |
| xao101 | 7,94 | 3,76% | 0,13% | 0,25% | 0,22% | 0,63% |
| ck500 | 7,99 | 3,32% | 0,25% | 0,20% | 0,29% | 0,58% |
| ck500/202 | 7,75 | 2,80% | 0,25% | 0,18% | 0,31% | 0,58% |
| A2_500 | 7,64 | 3,14% | 0,18% | 0,13% | 0,27% | 0,56% |

Không có dấu hiệu lặp cụm như Liu mô tả. Đây mới là đếm mặt chữ, "kết thúc treo" dùng danh sách từ tự chọn, chưa đo ngữ pháp bằng bộ phân tích cú pháp. Có thể giải thích khác biệt so với Liu bằng việc ck500 chỉ dịch rất ít (kl cuối khoảng 0,03) [suy].

### 2.2 Bảng điểm yếu và phép đo chốt

"Có" nghĩa là đã có trong danh sách lượt. "Thêm" nghĩa là phải thêm.

| # | Điểm yếu | Số hiện có | Phép đo chốt | Trong danh sách? | Máy |
|---|---|---|---|---|---|
| 1 | **Đòn "chỉ là học thêm" chưa đóng.** `report/320` §2.3 ghi "đã đóng" nhờ xao101, câu đó quá tay. xao101 có lợi thế trung bình 0 nên không có hướng học nào, kl 75 bước cuối 0,001 so với 0,030 của ck500, grad_norm 0,51 so với 1,22 [đo]. Nó bác "cứ cập nhật là tăng", không bác "thêm CE trên câu chuẩn cũng tăng". | Tiền lệ cảnh báo: CE2 chiếm 78% mức tăng ở MIN-DESC (trên nền S2, không so thẳng được). Ngược lại, SFT làm giảm action_ok (Base 96,46, S1 94,35) nên cũng có thể không sửa được loại thao tác [suy] | A1 SFT tiếp: S1 hoà + LoRA mới, đúng 1.000 câu nhắc và thứ tự, 2 câu nhắc mỗi cập nhật, 500 cập nhật, lr hằng 1e-5, chấm 250 và 500 | Có, A1. Đưa lên ngay sau lô 1 | Kaggle |
| 2 | **+1,55 chưa tính nhiễu hạt.** McNemar và KTC chỉ tính nhiễu mẫu test. Hai cấu hình giống hệt vẫn cho −0,72 **p = 0,011** [đo]. Vậy "KTC loại 0" không đủ để xếp hạng hai lượt. | Trung bình hai hạt +1,19. Nếu σ hạt ≈ 0,51 (một bậc tự do, rất thô): tách 1,0 điểm cần 5 hạt mỗi nhánh, 0,7 cần 9, 0,5 cần 17 [đo công thức, σ thô] | Nhiều hạt cho nhóm đứng đầu | Hoãn theo user. Phải ghi đây là giới hạn của mọi xếp hạng | Kaggle |
| 3 | **Phần tăng ở tên phần tử không lặp lại.** Cùng đúng loại: ck500/101 62,62 → 63,60; ck500/202 → 62,74; A2 → 62,74; xao101 → 62,76 [đo]. Tức +0,98 chỉ ở một hạt, còn lại ngang nhau. | 123/82 so với 126/121 | Chấm ck500/202 bằng UI-Venus và Phi-4 (chỉ câu mới). Bảng phân rã này cho mọi lượt của lưới | **Thêm** (ck500/202). Bảng phân rã 0 GPU khi có lưới | Kaggle |
| 4 | **Dịch về câu chạm và tác hại.** Tỉ lệ câu quy về chạm trên 6.958 bước: S1 76,5%, ck500 79,8%, câu chuẩn 78,7% [đo], tức S1 thiếu, ck500 hơi thừa. Đúng loại toàn bộ +0,60 [+0,13; +1,07], ròng +42 bước. Tổng hợp với exec +0,39 [−0,21; +0,99] [đo]. | A2_1000 đã có (`runs/ctg/test_nontap/`): toàn bộ 84,45, scroll 77,62, back 65,56; ck500 84,29, 77,75, 67,04 [đo]. Chưa có ck500/202, xao101 | Bước không chạm cho hai lượt đó (khoảng 2 h T4 mỗi lượt, chấm 0 GPU). In cột tổng hợp 6.958 bước cho mọi lượt | **Thêm** hai lượt cũ. Lưới mới đã có trong gói chấm | Kaggle |
| 5 | **ACU đo toàn bước chạm.** S1 trên ACU viết "swipe" ở 11,7% bước chạm (tập kiểm chính 3,1%), action_ok 84,64, nên có nhiều chỗ để sửa [đo]. `report/320` đọc "gấp ba, tác vụ mới" là thiếu vế này. Lý do S1 sai loại thao tác nhiều hơn hẳn trên ACU chưa rõ. | ck500 90,90, Base 92,72 [đo]; cùng đúng loại 61,63 → 62,51 [đo] | Dựng bước không chạm ACU, sinh S1 và ck500. xao101 và A2 trên ACU | **Thêm** | CPU dựng + Kaggle |
| 6 | **Lưới chưa thật sự đổi một yếu tố ở trục thuật toán.** RLOO, REINFORCE, SCST đều đổi mốc **và** bỏ chia std (lợi thế nhỏ đi cỡ 2,9 lần), kéo theo tỉ trọng KL và phép cắt gradient đổi theo. grad_norm trung vị ck500 0,90–1,17, ngưỡng 1,0, nên nhánh chuẩn hoá bị cắt khoảng nửa số bước, nhánh không chuẩn hoá ít khi bị [đo log, suy phần sau]. | Chưa có | K1 ("GRPO bỏ chia std") là điểm so chung: GRPO → K1 đo std, K1 → RLOO/SCST/REINFORCE đo mốc | Có K1, nhưng xếp "sắp chạy". **Phải chạy trước khi đọc Đ1–Đ3** | Kaggle |
| 7 | **Ô tham chiếu của lưới khác mã.** ck500 sinh bằng `grpo_spice.py`, 250 bước đầu không bật sinh theo khúc (log `train_c1` không có dòng này, `train_c3` có), nối ở 250 và 425, thiếu log 251–425. Lưới dùng `grpo_luoi.py` có khúc từ đầu. | Chưa có | `grpo:spice:101` qua `grpo_luoi.py`, cùng tổ hợp máy. Trùng 60,65 thì mọi so sánh sạch; lệch thì độ lệch này là mức nhiễu của đường chạy | **Thêm, ưu tiên cao** | Kaggle |
| 8 | **0,72 không đúng là nhiễu của lưới.** `--seed` đổi cả tập 1.000 câu nhắc lẫn hạt lấy mẫu, còn lưới giữ câu nhắc [đọc mã]. | RLOO và K1 chỉ khác hằng số 8/7 nên dùng làm phép đo nhiễu (đã nêu ở khảo sát) | So RLOO với K1 | Có | Kaggle |
| 9 | **Trục phần thưởng đổi kèm tỉ trọng phạt độ dài.** 9,59% mẫu bị phạt; với SPICE, 6,43% nhóm chỉ còn phần phạt tạo khác biệt và 7,23% không có khác biệt nào; với CIDEr-D 0,80% và 1,61% [val]. Cùng hệ số 0,02 nhưng vai trò khác nhau. | xao101 ghép ngẫu nhiên **cả phần phạt** (`r_spice` xáo sau khi trừ), nên "công của SPICE" thật ra là công của SPICE + phạt | SPICE không phạt, và chỉ phạt | **Thêm**, ưu tiên hai, cần sửa mã | Kaggle |
| 10 | **ck500 thực chất là gì.** `loss_type` dapo, gộp theo token. Clip không hoạt động. Vậy là policy gradient với mốc nhóm chuẩn hoá cộng KL nhỏ. kl cuối 0,03 × β 0,04 ≈ 0,0012, trong khi loss dao động cỡ −0,25 đến +0,39 [đo log]; so sánh độ lớn giá trị, chưa so gradient. Không được viết "nhờ giới hạn vùng tin cậy". | | A9, A10, A11 tách KL và cách gộp | Có | Kaggle |
| 11 | **Dụng cụ độc lập giảm dần.** UGround, UI-Venus +1,55; Phi-Ground +0,78; Phi-4 +0,69. So S1/202 dưới Phi-4 −0,20. | Chỉ có ck500/101 ở hai dụng cụ sau | Lượt top của lưới chấm thêm UI-Venus, Phi-4 | Có. Thêm ck500/202 (dòng 3) | Kaggle |
| 12 | **Nhiều phép so.** Holm với khoảng 50 phép so nghĩa là p < 0,001 ở phép đầu. Với SE ghép cặp 0,30–0,55 [đo] cần |Δ| khoảng **1,0–1,8**. Ngưỡng "|Δ| ≥ 1" hiện tại chưa đạt mức này khi SE ≥ 0,31. Ngoài ra còn nhân theo nhiều tiêu chí và nhiều dụng cụ. | | Chọn trước một họ chính khoảng 6 phép (SFT tiếp, SCST, K1, CIDEr-D, PPO, xao101) trên exec; còn lại ghi là mô tả. Vẫn in Holm cho toàn bộ | Luật đọc mới, **thêm** | 0 GPU |
| 13 | **Lập luận cũ không đứng được.** `report/323` §3 nói CIDEr-D "dễ thưởng chép cụm hiếm hơn gọi đúng phần tử". Đo: 67,6% khối lượng IDF của câu chuẩn nằm ngoài các từ khuôn, và CIDEr-D nhạy với việc bỏ tên nhất (mục 3.2) [đo, danh sách từ khuôn tự chọn]. | | Bỏ lập luận này | | |
| 14 | **Căn cứ chọn SPICE ở ch4 dẫn số val và thiếu vế bất lợi.** Câu "nhóm có điểm SPICE cao hơn cũng đạt exec cao hơn" đúng nhưng mọi độ đo khác cũng vậy và mạnh hơn. | | Sửa khi tới lượt sửa luận văn; không nói SPICE được chọn vì tín hiệu tốt nhất | | |

Một rủi ro vận hành tôi thấy khi đọc mã: kernel `trangphuongngoc/luoi-t2-1` chạy **hai lượt SPICE cùng lúc** trong một phiên, mỗi lần gọi một JVM `-Xmx8G`, dùng chung thư mục cache LMDB của `pycocoevalcap`. Probe chỉ có SCST + CIDEr-D, tức một tiến trình SPICE, nên trường hợp này chưa được thử [suy, chưa thấy lỗi]. Khi kernel dừng, kiểm thêm thời gian mỗi lần thưởng, thưởng trung bình và lỗi Java trong log của RLOO và REINFORCE trước khi nối commit 2.

### 2.3 Sau khi lưới xong sẽ đủ tới đâu

| câu hỏi | 6 lượt đang chạy | thêm K1, A1, SCST + CIDEr-D, PPO, A/A | thêm nhiều hạt cho nhóm đầu |
|---|---|---|---|
| "Đã so với cùng họ và độ đo khác chưa" | Một phần | **Đủ** | Đủ |
| "RL có hơn học thêm không" | Không | **Đủ để trả lời** | Đủ |
| "SPICE có hơn độ đo khác không" | Chỉ thấy chênh ≥ khoảng 1,5 [suy] | Như cũ | Tách được khoảng 1,0 với 5 hạt |
| "Tốt nhất" | Không | Chỉ "nhóm dẫn đầu" | Nói được nếu tách rõ và lặp lại |

Dự đoán của tôi [suy]: phần lớn lượt có thưởng thật rơi trong một dải khoảng 1 điểm exec, nên kết luận hợp lý nhất sẽ là "không phân biệt được". Khảo sát cũng thấy khoảng cách giữa các phương pháp không có critic thường nhỏ và đổi dấu theo bài.

---

## 3. Giả thuyết cơ chế

### 3.1 Dữ kiện về AndroidControl [đo]

| | AndroidControl, bước chạm | AitZ |
|---|---:|---:|
| Số từ trung bình câu chuẩn | 7,84 | 13,68 |
| Số tuple SPICE của câu chuẩn | 3,77 | 8,99 |
| Mở đầu "click" | 80,7% | gần như toàn bộ |

- 98,8% câu chuẩn có tuple đối tượng, 85,8% có thuộc tính, 38,2% có quan hệ.
- SPICE **không nhìn thấy động từ thao tác**: "Click on the Settings tab" và "Press the Settings icon" chỉ cho `tab`, `tab|settings` và `icon`, `icon|settings`. "Swipe up" và "Scroll down to view more" cho **0 tuple**.
- 37,8% câu S1 ở bước chạm có SPICE bằng 0.
- Câu chuẩn dạng 0 tuple không phổ biến: toàn tập 2,9–3,7%, scroll 14–16%, back 9–14%.

### 3.2 Phản ứng của độ đo với các phép biến đổi câu chuẩn [đo]

Cùng 193 bước, câu chuẩn có mệnh đề vị trí, exec lấy từ các lượt phép A và sàn đã chấm. Phần thưởng lý tưởng phải gần giữ nguyên ở ba cột đầu và giảm ở cột cuối.

| | đổi động từ | đổi trật tự | bỏ vị trí | bỏ tên |
|---|---:|---:|---:|---:|
| **exec** | **90,2** | **90,2** | **86,0** | **61,1** |
| SPICE | 0,965 | 0,538 | 0,476 | 0,639 |
| CIDEr-D | 0,790 | 0,743 | 0,318 | 0,323 |
| SPIDEr | 0,877 | 0,640 | 0,397 | 0,481 |
| BLEU-4 | 0,821 | 0,700 | 0,273 | 0,625 |
| ROUGE-L | 0,863 | 0,592 | 0,549 | 0,849 |
| chrF | 0,850 | 0,881 | 0,450 | 0,728 |
| METEOR | 0,524 | 0,580 | 0,283 | 0,426 |

Đọc: SPICE gần như không đổi khi đổi động từ (đúng như exec), nhưng phạt đổi trật tự và bỏ vị trí **nặng hơn** bỏ tên, ngược với exec. CIDEr-D gần exec nhất ở bước quan trọng nhất (bỏ tên 0,323, đổi trật tự 0,743), chỉ sai ở chỗ phạt bỏ vị trí quá nặng. ROUGE-L gần như mù với việc bỏ tên. Vậy câu "SPICE nhắm đúng vào tên phần tử" **không được số đỡ**; cái đỡ được là "SPICE không phản ứng với đổi động từ".

### 3.3 Khả năng dự báo exec [đo trên test]

| phần thưởng (kèm phạt độ dài) | AUC trên câu S1/101 | xếp đúng 349 cặp không chọn lọc [KTC] | hoà | xếp đúng 290 cặp cùng đúng loại |
|---|---:|---|---:|---:|
| SPICE | **0,671** | **72,2** [68,3; 76,1] | 25,8% | 73,4 |
| SPIDEr | 0,725 | 81,9 [77,9; 86,0] | 1,7% | 80,3 |
| BLEU-4 | 0,711 | 80,1 [75,9; 84,1] | 3,7% | 77,8 |
| ROUGE-L | 0,728 | 82,2 [78,4; 86,1] | 5,2% | 79,8 |
| CIDEr-D | 0,741 | 83,1 [79,1; 86,8] | 1,7% | 81,0 |
| chrF | 0,730 | 85,2 [81,4; 89,0] | 0,3% | 82,9 |
| METEOR | 0,750 | 85,2 [81,7; 88,7] | 3,2% | 82,6 |

Cặp không chọn lọc lấy từ S1/202 − S1/101 và xao101 − S1/101, không lượt nào học theo thưởng thật. Hoà tính 0,5; KTC bootstrap theo cặp, chưa theo cụm. Phần yếu không chỉ do hoà: trên val, bỏ cặp hoà thì SPICE còn 75,3%, CIDEr-D 87,4%, METEOR 88,1% [val]. CIDEr-D ở đây dùng df của 3.991 câu chuẩn huấn luyện, đúng như lúc train, nên khác CIDEr-D báo cáo.

**Nhưng dự báo tốt không đồng nghĩa dẫn học tốt.** Mức thay đổi của từng độ đo khi đổi phần thưởng thật [đo, trung bình mức câu × 100, so với S1/101]:

| | ΔSPICE | ΔCIDEr-D/10 | ΔMETEOR | Δexec | loại thao tác / cùng đúng loại (bước) |
|---|---:|---:|---:|---:|---|
| ck500/101 (SPICE) | +1,36 | +1,38 | +1,07 | +1,55 | +28 / +41 |
| ck500/202 (SPICE) | +1,37 | +1,58 | +1,08 | +0,83 | +32 / +5 |
| A2_500 (CIDEr-D) | +1,04 | +1,36 | +0,94 | +0,85 | +35 / +3 |
| xao101 | 0,00 | +0,17 | +0,17 | +0,00 | −3 / +3 |

Các phần thưởng kéo nhau đi cùng chiều: thưởng SPICE nâng CIDEr-D ngang chính thưởng CIDEr-D. Đây là căn cứ để dự đoán các phần thưởng khó tách nhau.

Phân rã SPICE theo loại tuple [đo, tái lập 44,37 · 45,79 · 45,69 · 45,27 · 44,40, chạy WSL khoảng 2 phút, nên phần Z4 của `report/323` không cần lên Kaggle]:

| | Object | Attribute | Relation |
|---|---:|---:|---:|
| S1/101 | 49,46 | 36,61 | 12,90 |
| ck500/101 | +1,54 | +1,14 | +1,36 |
| ck500/202 | +1,31 | +1,04 | +0,63 |
| A2_500 | +0,78 | +0,79 | 0,00 |
| xao101 | +0,02 | +0,11 | +0,22 |

Thưởng SPICE nâng tuple đối tượng ổn định qua hai hạt và cao hơn thưởng CIDEr-D, nhưng ở hạt 202 việc đó không đi kèm exec tăng. Đối chiếu với nhóm lỗi "đúng thao tác, bộ trỏ không tìm ra phần tử": dự đoán H4 của `report/323` đúng về độ đo, chưa đúng về hành vi.

### 3.4 Các giả thuyết và phép đo phân biệt

| Giả thuyết | Dự đoán kiểm được | Số hiện có | Phép đo (máy) | Tình trạng |
|---|---|---|---|---|
| **H-A. Cơ chế chung:** mọi phần thưởng so với câu chuẩn đều sửa lỗi loại thao tác SFT để lại | Mọi lượt thưởng thật: phần loại thao tác ròng +25 đến +40 bước, xao101 khoảng 0 | +28, +32, +35, −3 [đo] | Bảng phân rã cho cả lưới (0 GPU). **GRPO + thưởng chỉ đúng loại thao tác**: nếu ra khoảng +30 bước loại và 0 bước phần tử thì khẳng định (Kaggle, thêm) | Đang được ủng hộ mạnh nhất |
| **H-B. SPICE sửa tên phần tử** | Phần cùng đúng loại của thưởng SPICE > thưởng khác, qua nhiều hạt | Hạt 101 +41 (UI-Venus +44), hạt 202 +5, A2 +3 [đo] | ck500/202 dưới UI-Venus, Phi-4; A/A; nhiều hạt (Kaggle) | Một hạt ủng hộ, một hạt không |
| **H-C. Tín hiệu lúc đầu quyết định thứ hạng** (D1 ở `report/323`) | Thứ hạng lưới theo cột mục 3.3: METEOR, chrF, CIDEr-D ≥ SPICE | Bảng 3.3 [đo]. A2 ngang hạt 202 | Spearman giữa bảng 3.3 và exec của 8 phần thưởng (0 GPU sau lưới; 8 điểm, chỉ đọc chiều) | Chờ lưới |
| **H-D. Vì SPICE không phản ứng với đổi động từ, thưởng không bị dùng để đổi văn phong** | Tỉ lệ câu đổi mà tập tuple giữ nguyên thấp hơn ở thưởng SPICE | ck500 17,0%, ck500/202 13,8%, A2 16,5%, S1/202 15,9%, xao101 17,4% [đo] | Lặp cho METEOR, ROUGE-L, BLEU-4 (0 GPU sau lưới) | Chưa được ủng hộ trên A2 |
| **H-E. SPICE lệch về câu chạm vì câu không chạm ít tuple** | Tác hại tập trung ở câu chuẩn 0 tuple; thưởng CIDEr-D không có tác hại scroll | scroll 0 tuple −7,5 (n 107), có tuple −6,0 (n 648); A2_1000 scroll 77,62 so với ck500 77,75 [đo] | Không cần đo thêm cho CIDEr-D. Xem thêm METEOR, ROUGE-L khi có lưới (0 GPU) | **Bị bác cả hai vế.** Không viết tác hại là do SPICE |
| **H-F. Tác hại là mặt trái của H-A, lan từ 63% câu nhắc chạm** | Mọi phần thưởng so với câu chuẩn có tác hại scroll cùng cỡ. Thưởng chỉ đúng loại thao tác có thể giảm tác hại vì câu nhắc scroll được thưởng trực tiếp | 630/1000 câu nhắc là click, scroll 120; SPICE và CIDEr-D cùng cỡ [đo] | Bước không chạm của lưới (Kaggle); T5 | Đang được ủng hộ |
| **H-G. Mốc nhóm hợp hơn mốc greedy vì nhiều mẫu cùng điểm với greedy** (D2) | SCST < K1. Thiệt hại của SCST nặng hơn ở SPICE so với CIDEr-D (tương tác). `frac_adv_zero` đi theo bảng | Lợi thế SCST bằng 0: SPICE 42,7%, CIDEr-D 25,6%, METEOR 27,5%, chrF 19,4%; lợi thế TB khoảng −0,13 [val] | Ô 2×2 Đ1, A2 (SCST + CIDEr-D), Đ4, ck500; log (Kaggle) | Chờ. Dự đoán tương tác là mới so với D2 |
| **H-H. Chia std có tác dụng thật** | GRPO ≠ K1; ô 2×2 std × β tách được | Chia std chỉ đổi độ lớn, và AdamW ít nhạy với hằng số [suy] nên dự đoán chênh nhỏ | K1, A9, A10 (Kaggle) | Chờ |
| **H-I. GRPO chủ yếu làm chính sách tập trung lại** | Entropy giảm, tỉ lệ nhóm thưởng bằng nhau tăng theo bước; xao101 thì không | ck500 entropy 0,52 → 0,34, nhóm bằng nhau 20,2% → 31,3% (262 bước đầu so với 75 bước cuối). xao101 entropy 0,57 → 0,53, nhóm bằng nhau 14,7% → 19,3% (75 đầu so với 75 cuối) [đo log] | Log mọi lượt lưới (0 GPU). Nhóm bằng nhau cao hơn nhiều mức câu chuẩn 0 tuple 3,7% và mức 7,23% ở C1 chỉ gồm bước chạm [val], nên phải có nguyên nhân khác, nhiều khả năng là câu trùng và câu nhắc không chạm [suy] | Được ủng hộ sơ bộ; nên ghi thêm câu mẫu ở một lượt để xác nhận |
| **H-J. Không chuyển sang AitZ vì văn phong khác** | ck500 ≈ S1 trên AitZ; lượt top khác cũng vậy; tuple gấp đôi | 13,68 từ và 8,99 tuple so với 7,84 và 3,77 [đo]. ck500 − S1 −0,51 | Lượt top của lưới trên AitZ (Kaggle) | Phù hợp, chưa phân biệt được |

Bức tranh chung hiện nay: H-A và H-F là một cơ chế nhìn từ hai phía, cùng được số ủng hộ và không riêng SPICE. Đây cũng là lý do tôi dự đoán các phần thưởng sẽ khó tách.

Hai giả thuyết trong ghi chú cũ tôi không đưa vào vì số đã ngược: "SPICE cân bằng tốt nhất giữa phân biệt và khớp exec" (bác ở `report/323` §9.1, nay cả trên test), và "SPICE ít bị khuếch đại nhóm std nhỏ" (nhóm std dưới 0,05: SPICE 6,0%, METEOR 6,0%, ROUGE-L 4,4%, CIDEr-D 10,0% [val], không tách được).

---

## 4. Thực tiễn áp dụng

| mục | số | trạng thái |
|---|---|---|
| Thời gian train | 143–160 s/bước trên T4, 500 bước khoảng 20–22 h, hai commit. Colab L4 87 s/bước (75 bước cuối ck500/202) | Đã đo |
| Bộ nhớ train | Đỉnh 11,8–13,2 GiB | Đã đo |
| Thêm so với SFT | SFT S1 khoảng 23 h A100; GRPO thêm khoảng 21 h T4 | Đã đo |
| Chi phí phần thưởng | SPICE trung vị 9,7 s/lần cho 16 câu, lần đầu 84 s, khoảng 6,5% thời gian mỗi bước. Nghẽn nằm ở sinh mẫu [đo log] | Đã đo |
| Phụ thuộc lúc train | Java 8, jar CoreNLP 378 MB + 7 MB, JVM tối đa 8 GB | Đã đọc mã |
| Phụ thuộc lúc suy luận | **Không cần** Java, SPICE, câu chuẩn. Chỉ cần mô hình, ảnh, mục tiêu, lịch sử, OCR | Đã đọc mã: `gen_test_grpo.py` không gọi phần thưởng |
| Câu chuẩn cần ở đâu | Chỉ lúc train: 1.000 câu nhắc có câu chuẩn của bước đó. Lúc sinh không dùng câu chuẩn của bước đang xét, nhưng số chính dùng câu chuẩn của các bước trước làm lịch sử; lịch sử tự sinh làm giảm khoảng 4 điểm | Đã đo |
| Độ trễ sinh | 2,80 s/bước trên T4, fp16, một câu mỗi lần, ảnh + câu (log `gen_test`) | Đã đo. **Chưa đo tách riêng** thời gian OCR và đỉnh VRAM lúc suy luận |
| So S1 về độ trễ | LoRA mới có thể hoà vào trọng số, cùng cỡ với S1, câu dài gần bằng, nên dự đoán ngang nhau [suy] | **Còn phải đo** trên cùng đường sinh, chỉ cần đọc log xao101 và ck500 |
| Kích thước | Adapter cỡ 59,9 MB | Đã đo |
| Máy người dùng cuối | Chưa thử trên thiết bị di động, chỉ có T4 | Chưa đo |

**Mức tăng có nghĩa gì với người dùng.** Thước exec đo một bộ trỏ đọc câu, không đo người đọc câu. Chưa có đánh giá người (user đã quyết không chấm tay).
- Mỗi 100 bước chạm, khoảng 1–1,5 câu thêm đủ để bộ trỏ tìm đúng phần tử.
- Lịch sử chuẩn: tác vụ có mọi bước chạm đều trúng từ 29,74% lên 31,82% (hạt 202: 31,08%), trung bình 3,32 bước chạm mỗi tác vụ [đo].
- Lịch sử tự sinh, gần với dùng thật hơn: exec 56,44 so với 54,96 (+1,48 [+0,54; +2,43]), tác vụ đủ ảnh 29,24 so với 28,67 (chưa có KTC).
- Nhưng mức tăng từ SFT là +11,52, từ 7B prompting lên 3B đã tinh chỉnh là +7,6. GRPO là phần cộng thêm nhỏ so với SFT.

**Khi nào đáng dùng so với chỉ SFT.**
- Đáng dùng khi có sẵn câu chuẩn, câu hướng dẫn chủ yếu cho thao tác chạm, sản phẩm cuối ưu tiên đúng phần tử, và có khoảng một ngày T4.
- Không đáng dùng khi nhiều bước cuộn và quay lại: scroll −6,23, back −5,93, và với lịch sử tự sinh, bước không chạm −4,49. Tổng toàn bộ bước chỉ +0,39, KTC phủ 0.
- Khi đổi nguồn câu chuẩn: chưa thấy lợi ích. Trên AitZ ck500 −0,51 và hạt 202 −1,17.

**Giới hạn với app mới.** ACU là tác vụ mới, không phải app mới: 1.383/1.484 bước thuộc split train chính thức và chỉ 68/1.484 bước gán được app, nên không thể khẳng định về app chưa thấy. Mẫu app chưa thấy ở tập kiểm chính rất nhỏ (139 bước tính mọi loại thao tác, 78 bước chạm). Không có thông tin nào cho biết giao diện khác hẳn (web, tablet).

---

## 5. Cần so thêm gì ngoài danh sách

Chỉ những dòng có lý do cụ thể. Mọi dòng dưới đây chạy Kaggle, không cần Colab.

| # | Lượt | Lý do | Chi phí [suy] |
|---|---|---|---|
| T1 | **`grpo:spice:101` qua `grpo_luoi.py`** | Ô tham chiếu cùng mã với lưới, đo mức lệch đường chạy (điểm yếu 7) | Khoảng 26 h T4 |
| T2 | **ck500/202 chấm UI-Venus, Phi-4** (chỉ câu chưa chấm) | Quyết định phần tăng ở tên phần tử có lặp lại không | Vài giờ T4 |
| T3 | **Bước không chạm cho ck500/202, xao101** | So tác hại giữa hai hạt và với nhánh kiểm. xao101 chỉ có điểm lưu trên máy nhà trong `runs/xao101/`, ck500/202 cần kiểm tình trạng adapter. A2_1000 đã có sẵn | 2 h T4 mỗi lượt |
| T4 | **ACU: bước không chạm của S1, ck500; xao101 và A2 cho bước chạm** (A2 cần kiểm adapter còn ở đâu) | Khoá cách đọc +4,58 | CPU dựng dữ liệu + khoảng 2–4 lượt T4 |
| T5 | **GRPO + thưởng chỉ đúng loại thao tác** | Phép kiểm trực tiếp H-A và H-F, chỉ để giải thích, không đề xuất làm phương pháp. Phải khai là nghĩ ra sau khi đã thấy số test | Khoảng 26 h T4, sửa mã nhỏ |
| T6 | **SPICE không phạt và chỉ phạt độ dài** | xao101 không tách được hai phần (điểm yếu 9). Ưu tiên sau T1–T5 | 2 × 26 h T4 |
| T7 | **Điểm xuất phát S1/202 + GRPO + SPICE** | Hai hạt ck500 hiện đều từ S1/101, nên chưa từng đo nhiễu của hạt SFT trong GRPO. Thuộc phần nhiều hạt đã hoãn | Khoảng 26 h T4 |

Không đề xuất thêm thuật toán. Danh sách khoảng 50 lượt đã dài hơn mức dữ liệu một hạt có thể tách. **Nên dừng thêm phương pháp cổ điển trước khi chạy xong A1, K1, SCST + CIDEr-D, PPO**, vì mỗi lượt thêm làm ngưỡng Holm khắt khe hơn nếu tính chung một họ. Việc này là ý kiến của tôi, user đã chốt so càng nhiều càng tốt, nên cách dung hoà là giữ họ chính khoảng 6 phép và ghi các lượt còn lại là mô tả.

Cần Colab, ghi lại để user quyết: không có dòng mới. PPO critic đủ cỡ vẫn là dòng quan trọng duy nhất có khả năng cần Colab, đã ghi ở khảo sát.

---

## 6. Câu trả lời đề xuất cho ba câu hỏi của thầy

Chỗ `[CHỜ SỐ: …]` phải điền từ lượt chạy. Không dùng bản nào khi số chưa khớp điều kiện đầu dòng. "Nhóm dẫn đầu" định nghĩa trước: các lượt cách lượt cao nhất dưới 1 điểm exec, hoặc không bị Holm bác trong họ chính.

### Câu 1. So GRPO với các thuật toán cùng họ RL

**Phần chung, dùng được ngay.** Phần thưởng là điểm cho cả câu, không khả vi, nên cần họ policy gradient như SCST [Rennie và cộng sự, CVPR 2017] và PG-SPIDEr [Liu và cộng sự, ICCV 2017]. Cấu hình ck500 chạy một lượt cập nhật trên mỗi lô mẫu nên phép clip không hoạt động; thực chất là policy gradient với mốc trung bình nhóm, chia độ lệch chuẩn nhóm, gộp theo token và phạt KL về S1. Chúng tôi giữ nguyên điểm xuất phát, 1.000 câu nhắc, số mẫu, lr, β, số bước và chỉ đổi cách tính lợi thế. Ahmadian và cộng sự [ACL 2024, tr. 12248–12267] báo cáo các biến thể kiểu REINFORCE đơn giản vượt PPO, DPO, RAFT trên bài toán học từ phản hồi, nhưng đó là miền khác và không thay được phép đo trên AndroidControl.

**Bản A, nếu ck500 trong nhóm dẫn đầu** (và K1, SFT tiếp đã có):
> Trong lưới một hạt giống, GRPO [CHỜ SỐ: exec, Δ so SCST, K1, RLOO, REINFORCE, PPO kèm KTC, p gốc, p Holm] không thua có ý nghĩa lượt nào và không tách được khỏi [CHỜ SỐ: danh sách]. So với SFT tiếp cùng số bước, [CHỜ SỐ: Δ]. Chúng tôi chọn GRPO vì không cần mô hình giá trị, chi phí bộ nhớ [CHỜ SỐ: VRAM PPO so 12,7 GiB] và có tiền lệ, không vì GRPO vượt các phương án khác. Khác biệt giữa hai hạt ck500 là 0,72 nên chênh dưới 1 điểm chưa đủ để xếp hạng.

**Bản B, nếu lượt khác đứng trên ck500 rõ** (cách ≥ 1 điểm, KTC loại 0, qua Holm trong họ chính):
> [CHỜ SỐ: tên lượt] hơn ck500 [CHỜ SỐ: Δ, KTC, p]. Kết quả này một hạt giống. Chúng tôi chạy lại [CHỜ SỐ: số hạt] và [CHỜ SỐ: kết quả]. Nếu lặp lại thì phương pháp chính đổi thành [user quyết]; nếu không thì báo là không phân biệt được.

**Bản B′, nếu SFT tiếp ≥ ck500:**
> Mức tăng của GRPO so với S1 không vượt phần học thêm bằng CE. Đóng góp được giữ lại là phần phân tích: lỗi loại thao tác còn lại sau SFT và tác hại khi dịch về câu chạm. Đề xuất với thầy: [user quyết] có giữ GRPO là phương pháp chính hay không.

Không viết: "bỏ critic làm kết quả tốt hơn"; "nhờ cơ chế clip của PPO/GRPO"; "GRPO hơn SCST" dẫn Liang (preprint) như đã rõ.

### Câu 2. So SPICE với các độ đo khác làm phần thưởng

**Phần chung, dùng được ngay, phải nói chủ động trước khi bị hỏi.**
> Xét riêng khả năng dự báo exec, SPICE là độ đo yếu nhất trong các độ đo đã xét: trên test AUC 0,671 so với 0,711–0,750, và xếp đúng 72,2% cặp bất đồng so với 80,1–85,2%. Nhiều nguyên nhân: SPICE hoà nhiều (25,8%), không nhìn thấy động từ, và phản ứng với trật tự từ mạnh hơn exec. Vì vậy chúng tôi không biện minh lựa chọn SPICE bằng chất lượng tín hiệu. SPICE có tiền lệ làm một nửa của SPIDEr [Liu, ICCV 2017], nhưng chính bài đó ghi PG-SPICE "tends to generate ungrammatical sentences, with a lot of repeated phrases"; trên câu của chúng tôi chưa thấy dấu hiệu này ở mức đếm mặt chữ (lặp 3-gram 0,25% so với 0,34% ở câu chuẩn). Zhao và cộng sự [EACL 2021] khuyên dùng SPICE để xếp hạng hệ thống sinh chỉ dẫn khi có câu tham chiếu, đó là khuyến nghị cho đánh giá, không phải cho phần thưởng.

**Bản A, nếu SPICE trong nhóm dẫn đầu nhưng không tách được khỏi các độ đo khác:**
> Với cùng GRPO, các phần thưởng [CHỜ SỐ: danh sách, exec, Δ, KTC, Holm] không phân biệt được với SPICE. Điều này phù hợp với việc các phần thưởng kéo nhau cùng chiều (thưởng SPICE nâng CIDEr-D +1,38, thưởng CIDEr-D nâng +1,36) và phần lặp lại được là sửa loại thao tác, mà độ đo nào so với câu chuẩn cũng thấy. SPICE là một lựa chọn đủ tốt, không phải lựa chọn tối ưu đã được chứng minh. Khi không có khác biệt về exec, ưu tiên [CHỜ SỐ: bước không chạm, độ đo văn bản, chi phí; Java so với không Java] để chọn.

**Bản B, nếu SPICE đứng đầu rõ, qua nhiều hạt:**
> SPICE hơn [CHỜ SỐ]. Tín hiệu bước đầu dự đoán ngược lại (dự đoán D1 ghi trước khi có số), nên tín hiệu bước đầu không quyết định thứ hạng. Giải thích khả dĩ [CHỜ SỐ: phép đo H-B, H-D, H-I]. Phần chưa kiểm được thì nói là chưa kiểm.

**Bản C, nếu một độ đo khác đứng trên SPICE rõ:**
> [CHỜ SỐ: tên] hơn SPICE [CHỜ SỐ], khớp với thứ tự tín hiệu ở bảng dự báo exec. Lựa chọn SPICE ban đầu dựa trên tiền lệ và chưa so sạch; lượt A2 cũ lệch ba biến. Đề xuất đổi phần thưởng [user quyết], kèm hạt thứ hai trước khi đổi.

Không viết: "SPICE so đúng tên phần tử"; "CIDEr-D chỉ thưởng chép cụm hiếm"; "SPICE tốt hơn CIDEr-D" dẫn −0,69 mà không kèm +0,02 của hạt 202.

### Câu 3. Vì sao tốt nhất trên AndroidControl

**Trả lời thẳng nên là: chúng tôi không khẳng định tốt nhất.** Thay câu hỏi bằng "cơ chế nào tạo ra mức tăng trên AndroidControl, khi nào nó mất".

**Phần dùng được ngay, số đã có:**
1. Câu chuẩn AndroidControl ngắn (7,84 từ), 80,1% bước chạm mở đầu "click on", một câu chuẩn cho mỗi bước.
2. Sau SFT, S1 còn thiên về câu không chạm: viết câu chạm ở 76,5% số bước so với 78,7% ở câu chuẩn, và viết "swipe" ở bước chạm (3,1% trên tập kiểm, 11,7% trên ACU).
3. Học tiếp bằng GRPO với câu chuẩn làm tham chiếu sửa đúng lỗi đó. Phần này lặp lại qua hai hạt và hai phần thưởng (+28, +32, +35 bước; xao101 −3), và chiếm 84–95% mức tăng trên ACU.
4. Đổi lại, cùng thiên hướng đó gây hại ở bước không chạm (scroll −6,23, back −5,93), với mức ròng trên toàn bộ bước chỉ +0,39 [−0,21; +0,99]. Thưởng CIDEr-D cũng vậy (scroll −6,35), nên đây không phải đặc điểm riêng của SPICE.
5. Trên AitZ, câu chuẩn dài gấp gần hai lần (13,68 từ), số tuple gấp hơn hai lần, nên lợi ích không chuyển sang (−0,51). Đây là phù hợp, chưa phải chứng minh cơ chế.
6. Riêng việc đổi đúng phần tử: hạt 101 có +41 bước và giữ dưới UI-Venus (+44), hạt 202 chỉ +5. Chúng tôi chưa kết luận phần này.

**Bản A, nếu H-A được xác nhận** (phân rã lưới và lượt T5 cùng hướng):
> Trên AndroidControl, mức tăng chủ yếu đến từ việc sửa lỗi loại thao tác còn lại sau SFT, không riêng SPICE: [CHỜ SỐ: bảng phân rã]. Vì vậy các phần thưởng cho kết quả gần nhau, và lựa chọn thực tế nên cân nhắc thêm tác hại ở bước không chạm [CHỜ SỐ].

**Bản B, nếu H-B được xác nhận** (phần cùng đúng loại của thưởng SPICE cao hơn các phần thưởng khác ở nhiều hạt):
> Ngoài lỗi loại thao tác, SPICE giúp đổi đúng phần tử [CHỜ SỐ: phần cùng đúng loại, UI-Venus, Phi-4, Object tuple]. Cơ chế khả dĩ là SPICE không phản ứng với đổi động từ (0,965) nên [CHỜ SỐ: H-D]. Lưu ý độ đo này cũng phạt đổi trật tự mạnh hơn exec.

**Bản C, nếu không giả thuyết nào qua:**
> Thứ hạng lưới không được giải thích bởi các đặc tính đã đo. Phần đã loại được: tín hiệu bước đầu [CHỜ SỐ nếu lệch], câu chuẩn 0 tuple, văn phong. Kết luận trung thực là mức tăng khiêm tốn, gần mức nhiễu giữa các hạt.

---

## 7. Việc cần làm theo thứ tự

1. **Sáng 2/11, khi lô 1 dừng:** kiểm log như `report/326` §4, thêm phần SPICE song song ở `luoi-t2-1`.
2. **Trước khi đọc số lưới, ghi vào `report/320`:** họ chính 6 phép, định nghĩa "nhóm dẫn đầu", bảng dự đoán H-A đến H-J. Không phải đăng ký thủ tục, chỉ để giữ thế không kể lại sau khi đã biết số.
3. **Xếp lại lô sau:** T1 (A/A), K1, A1 (SFT tiếp), SCST + CIDEr-D đứng trước các lượt phần thưởng còn lại và các lượt cổ điển. PPO khi viết xong mã. `make_nb.py` có phép chặn cần bỏ cho SCST + CIDEr-D, theo `report/326` §6.
4. **Ngay, rẻ:** T2, T3. T2 quyết phần tăng ở tên phần tử; T3 cho biết tác hại có lặp lại ở hạt 202 không.
5. **Song song:** T4 (ACU). Tới lúc đó ngừng viết "+4,58 trên tác vụ mới" mà không kèm phân rã và tình trạng chưa đo bước không chạm.
6. **Khi lưới có số:** bảng phân rã, bảng thưởng × độ đo, cột tổng hợp 6.958 bước, SPICE theo tuple, F1, mục 3.4 cho từng lượt, toàn bộ 0 GPU trên WSL (SPICE 27.096 cặp chạy khoảng 2 phút).
7. **Đo F1 đủ hơn:** thêm kiểm ngữ pháp bằng bộ phân tích cú pháp hoặc CoreNLP; đọc tay 50 câu chỉ để tìm ví dụ, không báo là chấm tay.
8. **T5, rồi T6.** Sau đó quyết nhiều hạt cho 3 nhóm đầu (user đang hoãn), gồm T7.
9. **Lượt sửa luận văn** (chưa làm), các câu hiện không đứng được khi có số mới:
   - ch4 "Cơ sở lựa chọn": căn cứ val và thiếu vế SPICE yếu nhất;
   - ch6 bước không chạm: nói rõ tác hại xuất hiện cả với thưởng CIDEr-D;
   - ch6 §Ảnh hưởng của SPICE: "đạt kết quả tốt nhất" phải kèm hạt 202 và A2, AitW của A2 cao hơn (76,52 so với 76,25);
   - ch6 ACU: thêm phân rã 84–95% và giới hạn bước chạm;
   - `report/320` §1 mục 1 và §2.3 về đòn học thêm.
   Theo chỉ đạo user, ghi các việc này vào `report/320` khi tới lúc, tôi chưa đụng.

---

## 8. Nguồn và cách tái lập

**Đã mở tận nguồn hôm nay:**
- Liu và cộng sự, *Improved Image Captioning via Policy Gradient optimization of SPIDEr*, trường Comments của arXiv 1612.00370 ghi ICCV 2017. Câu trích ở tr. 6 PDF arXiv; tr. 5 ghi "many repeated phrases".
- Zhao và cộng sự, *On the Evaluation of Vision-and-Language Navigation Instructions*, EACL 2021, tr. 1302–1316, ACL Anthology. Câu "For ranking instruction generation systems, if reference instructions are available we recommend using SPICE" ở tóm tắt.
- Anderson và cộng sự, *SPICE*, arXiv 1607.08822 ghi ECCV 2016. Chưa dùng số của bài này ở trên; tương quan 0,88 là trên chú thích ảnh, không chuyển sang GUI được.
- Ahmadian và cộng sự, *Back to Basics*, ACL 2024, tr. 12248–12267. Trang Anthology không nêu tên RLOO; muốn dẫn RLOO phải mở Bảng 1 (khảo sát còn ghi một mâu thuẫn ở hàng RLOO/RAFT k=2).
- Rennie và cộng sự, *Self-critical Sequence Training*, arXiv 1612.00563 ghi CVPR 2017.

**Chưa kiểm hôm nay:** mọi số và venue khác trong `report/reports/Baseline RL so với GRPO.md`. Mục tiền lệ ở đây là mẫu đã tra, không phải chứng minh chưa ai làm.

**Script tạm** ở `/tmp/claude-1000/-mnt-d-Master-Thesis/f8c22a00-f56d-41dc-bd70-6f4951a71b5e/scratchpad/` (có thể mất, chép ra nếu muốn giữ): `a1.py` (ghép cặp, phân rã, ACU) · `a2.py` (tổng hợp 6.958 bước) · `a3.py` (chấm mức câu 27.096 cặp, tái lập được các điểm SPICE đã công bố) · `a4.py` (dữ kiện câu chuẩn) · `a5.py` (F1) · `a6.py` → `a6.out` (biến đổi câu, dự báo exec, tuple) · `a7.py`, `a8.py` (tuple theo loại thao tác, tác hại, AitZ) · `a9.py` (bổ sung C1, số val) · `a10.py` (193 bước, mức tác vụ, sức mạnh) · `a12.py` (UI-Venus). Chạy bằng `~/.venvs/thesis/bin/python -B`, cần Java 8 ở `~/.jdk/jdk8u504-b01/bin` trong PATH và `/home/uyenle/fgrb_p1/bundle`.

**Tự kiểm:** tính lại khớp +1,55, +1,03, +0,83, −0,72, +0,00, −0,69 và cứu/phá của `report/320`; KTC bootstrap của tôi lệch tối đa 0,03 so với hàm `score_run.cluster_bootstrap` (ví dụ [+0,80; +2,30] so với [+0,80; +2,33]) vì khác hạt ngẫu nhiên. Số đúng loại toàn bộ +0,60 khớp `report/320` §7. A2_1000 scroll, back, toàn bộ khớp `report/279` §4g. `a13.py` tính phần A2_1000. SPICE mức câu khớp số công bố đủ năm nhánh.

**Không đánh giá ACE** ở đây; xem `report/327`.

---

## Bổ sung 2/11: đo hình thức câu có bộ phân tích cú pháp

`harness/hinh_thuc_cau.py`, kết quả `runs/hinh_thuc_cau/ket_qua.json` (spaCy `en_core_web_sm`, 4.463 bước, số test, bootstrap theo app). Đơn vị: điểm phần trăm, hiệu so với S1/101.

| nhánh | ROOT không phải động từ | lặp 2-gram | lặp 3-gram |
|---|---|---|---|
| câu chuẩn (mức tuyệt đối 7,46% · 6,27% · 0,34%) | +1,41 [+0,68; +2,13] | +2,71 [+1,98; +3,41] | +0,20 [+0,04; +0,39] |
| ck500 | −0,47 [−0,90; −0,07] | −0,25 [−0,61; +0,10] | +0,11 [0,00; +0,25] |
| ck500/202 | −0,72 [−1,14; −0,30] | −0,76 [−1,17; −0,36] | +0,11 [0,00; +0,26] |
| CIDEr-D (A2_500) | −0,47 [−0,84; −0,09] | −0,43 [−0,79; −0,05] | +0,05 [−0,04; +0,14] |
| xao101 | 0,00 [−0,27; +0,25] | +0,20 [−0,02; +0,44] | 0,00 |

Trên các chỉ báo này không thấy hiện tượng Liu mô tả ở PG-SPICE; mức lặp 3-gram tăng rất nhỏ và vẫn thấp hơn câu chuẩn. Giới hạn: đây là chỉ báo của bộ phân tích cú pháp, chưa kiểm định độ chính xác trên câu GUI, và câu chuẩn cũng có tỉ lệ cao hơn cả mô hình nên không đo được "đúng ngữ pháp" theo nghĩa chặt. Khác biệt với Liu còn có thể do phạt độ dài, điểm SFT và KL; chưa tách được.
