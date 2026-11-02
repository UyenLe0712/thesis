# 330. Khảo sát độ đo có thể làm phần thưởng thay SPICE (1–2/11/2026)

Nhãn: **[đo]** là số tôi tính lại trong phiên này, 0 GPU. **[val]** là số trên tập kiểm định, chỉ để giải thích, không trích như kết quả. **[suy]** là suy luận chưa đo. Số trong bảng trích từ bài khác được chép từ PDF. Phần cơ chế của ck500 nằm ở `report/328`, ở đây không nhắc lại. Lưới đang chạy chưa có số nào, nên mọi câu về lưới là dự đoán.

## 1. Kết luận ngắn

1. **Chưa thể trả lời thầy rằng SPICE tốt nhất.** Hiện chỉ có thể nói: đã khảo sát, SPICE có lý do chọn nhưng không phải lựa chọn phổ biến, và phép so trên cùng kịch bản đang chạy.
2. **Độ phổ biến làm thưởng, trong 161 bài đọc được có thưởng:** CIDEr 39, ROUGE 37, BLEU 33, thực thi thật 17, nhúng/embedding 15 (BERTScore 9), LLM giám khảo 14, bộ phân biệt GAN 13, thưởng học từ người 13, METEOR 10, đối chiếu tập thực thể 10. **SPICE thuần 3, SPIDEr 2.** Mỗi độ đo cổ điển gần như chỉ thống trị mảng của nó: CIDEr 37/64 ở chú thích ảnh và video, ROUGE 21/23 ở tóm tắt, BLEU 17/19 ở dịch máy. Đây là mẫu có chủ đích, không phải tỉ lệ của ngành.
3. **Tiền lệ của SPICE thuần làm thưởng nghiêng về phía bất lợi.** Liu 2017 và Pasunuru 2017 thử rồi bỏ vì câu dài, lặp cụm. RL4LMs (ICLR 2023) là bài duy nhất trong mẫu có hàng số; ở dòng khởi đầu từ mô hình đã tinh chỉnh, thưởng SPICE ngang Rouge-1, thua METEOR, và không vượt mô hình tinh chỉnh trên chính cột SPICE (0,288 so với 0,299). Bảng này **sửa** câu "SPICE đứng một mình không có hàng số nào" trong `report/reports/Baseline RL so với GRPO.md`.
4. **Không được dùng Zhao EACL 2021 làm căn cứ cho SPICE làm thưởng.** Bài khuyên SPICE ở mức hệ thống, và viết rõ ở mức từng chỉ dẫn SPICE không tương quan với kết quả người đi theo vì phương sai cao. GRPO chấm từng câu, tức đúng mức mà bài nói SPICE không dùng được. Phản biện này nặng hơn lời chê của Liu.
5. **Nhận xét của Liu không lặp lại trên ck500.** Trên 4.463 câu test [đo]: lặp bigram ck500 3,32% so với S1 3,56% và câu chuẩn 6,27%; số từ 8,00 so với 7,86 và 7,85. Điểm khác giữa bài đó và ck500 là phạt độ dài và khởi đầu từ S1; chưa có phép đo nào tách được yếu tố nào gây ra sự khác biệt này.
6. **Kiểm đặc tính trên câu chuẩn val [đo]:** SPICE gần như không thấy loại thao tác. Đổi "Click" thành "Swipe up" vẫn được 0,919, trong khi sáu độ đo còn lại cho 0,453–0,789. Câu chuẩn có trung vị 3 tuple, nên thang điểm thô. Ngược lại SPICE tách tên sai rất tốt và bền trước đổi động từ đồng nghĩa. CIDEr-D tách sai tên mạnh nhất, nên lập luận ở `323` §3 rằng IDF làm CIDEr-D kém hơn SPICE khi gọi đúng phần tử **không được phép thử này ủng hộ**.
7. **Thêm vào lưới:** BCMR, SPICE có cổng loại thao tác, thưởng tên phần tử + loại thao tác, người nghe Phi-4 xuất phát từ S1, CIDEr-R (có điều kiện). Xếp lại phần chờ: BLEU-4 → SPIDEr → BERTScore → BCMR → chrF. Mục 7 và 8 ghi máy và điều kiện.
8. **CLIP đo rồi mới loại [đo]:** CLIP-S có tín hiệu nhưng rất yếu trên màn hình: P(đổi động từ > sai tên) 0,690 so với 0,965–1,000 của các độ đo chữ. Đổi căn cứ từ "224 px không đọc được chữ" sang số này.

## 2. Cách lấy mẫu và giới hạn

| tầng | cách lấy | bài đọc | ghi chú |
|---|---|---:|---|
| A, chọn tay | tôi liệt kê theo mảng từ ghi chú cũ và hiểu biết của mình | 120 | có chủ đích, nghiêng về bài nổi tiếng |
| B, từ truy vấn | 10 truy vấn OpenAlex lọc tiêu đề + tóm tắt, sắp theo trích dẫn; 18 truy vấn arXiv trên tóm tắt; tôi chọn tay bài đúng chủ đề trong kết quả | 78 | giảm thiên lệch, không khử được |
| Bài gốc độ đo | chỉ đọc để trích, không đếm | 14 | 12 qua arXiv, BLEURT và ViLBERTScore qua Anthology |

**Tiêu chí đếm "làm thưởng":** tôi đọc đoạn trích quanh tên độ đo và từ khoá thưởng, tính khi bài **tự train** với độ đo đó làm thưởng, rủi ro (MRT) hoặc mục tiêu mức chuỗi. Không tính khi chỉ nhắc trong tổng quan. Một bài có thể có nhiều nhãn. Bài thử rồi bỏ nhưng không in số (Liu với SPICE, Pasunuru với SPICE) vẫn tính và được ghi riêng. Trong 198 bài: 161 có nhãn, 37 không có. Trong 37 bài có 5 bài tôi chưa xác định được thưởng từ đoạn đọc (1812.02378, 1904.03870, 1810.06667, 1803.11070, 2106.04080).

**Tiêu chí "chỉ đánh giá":** bài nhắc tên độ đo từ 3 lần trở lên trong phần trước tài liệu tham khảo mà không có nhãn thưởng. Đây là số đếm tự động và thô, đọc như "có mặt trong bài", không phải "chắc chắn dùng để đánh giá".

**Giới hạn, phải khai khi dùng:**
- Mẫu có chủ đích. Viết "trong mẫu 161 bài", không viết "ngành dùng". Không thấy trong mẫu không có nghĩa là chưa ai làm.
- Thành phần mẫu quyết định xếp hạng tổng. Vì tôi đọc nhiều chú thích ảnh (50 + 14 bài video), CIDEr đứng đầu. Nên đọc bảng theo mảng cùng bảng tổng.
- Truy vấn arXiv tầng B có chứa tên độ đo (BERTScore, CLIPScore, SPICE, CIDEr, METEOR, BLEU, ROUGE, BLEURT), nên số của họ embedding bị đẩy lên: 11/15 bài đến từ tầng B.
- OpenAlex trả 429 sau 10/21 truy vấn (hạn mức miễn phí dùng chung theo IP), nên phần còn lại đi qua arXiv: sắp theo liên quan, không theo trích dẫn. DBLP chặn bằng trang xác minh, Semantic Scholar trả 429.
- Nhãn đến từ đoạn trích, không đọc trọn từng bài. Tôi kiểm chéo tự động: mọi nhãn CIDEr/ROUGE/BLEU/METEOR đều có tên độ đo gần từ khoá thưởng trong bài, trừ 1 bài do ngắt dòng (2005.03642, đã đọc tay). Bảng số ở mục 4 thì chép trực tiếp từ PDF.
- Venue: 62 bài mở được trang ACL Anthology, 72 có bản ghi Crossref, 22 theo ghi chú arXiv, 42 **chưa kiểm hoặc là preprint** (cột "kiểm" ở Phụ lục A). ICLR và NeurIPS không có trong Crossref nên hay rơi vào nhóm này. Các hàng chữ "(preprint)" ở mục 4 phải mở lại trước khi vào luận văn.
- Nhiều bài 2025–2026 là preprint, mới, chưa qua bình duyệt. Hàng thời gian ≥2024 cần đọc với điều đó.

Tái lập: `runs/khao_sat_do_do_330/` (script tiền tố `khaosat330_`, `meta.json`, `venue.json`, `dem.json`, `phuluc.json`, `stress*.json`, `clip.json`). PDF không lưu trong kho.

## 3. Bảng xếp hạng độ phổ biến

### 3.1 Toàn mẫu (161 bài có thưởng)

| hạng | độ đo hoặc họ | làm thưởng | mảng chính | ≤2019 / 2020–23 / ≥2024 | tầng A / B | có mặt ≥3 lần, không làm thưởng | trong lưới? |
|---:|---|---:|---|---|---|---:|---|
| 1 | **CIDEr, CIDEr-D** | 39 | chú thích 29, video 8 | 25 / 11 / 3 | 30 / 9 | 23 | đang chạy |
| 2 | **ROUGE** (các biến thể) | 37 | tóm tắt 21, sinh khác 7 | 23 / 10 / 4 | 22 / 15 | 51 | đang chạy (ROUGE-L) |
| 3 | **BLEU** (các biến thể) | 33 | dịch 17, chú thích 6 | 22 / 8 / 3 | 19 / 14 | 68 | sắp chạy |
| 4 | Thực thi thật | 17 | SQL/chương trình 15, GUI 2 | 4 / 1 / 12 | 11 / 6 | | không (mục 5) |
| 5 | Nhúng, embedding (BERTScore 9, còn lại SimiLe, BLEURT, WMD, nhúng ảnh–câu, khoảng cách tập, tương đồng) | 15 | chú thích 6, sinh khác 4 | 4 / 5 / 6 | 4 / 11 | BERTScore 4 | sắp chạy (BERTScore) |
| 6 | LLM giám khảo, kiểm câu hỏi | 14 | chú thích 6, RLHF 5 | 0 / 2 / 12 | 6 / 8 | | không |
| 7= | Bộ phân biệt GAN | 13 | sinh khác 5, chú thích 4 | 11 / 1 / 1 | 7 / 6 | | đang xếp đợt 4 (SeqGAN) |
| 7= | Mô hình thưởng học từ người | 13 | dịch 4, RLHF 4 | 4 / 6 / 3 | 9 / 4 | | không (không chấm người) |
| 9= | **METEOR** | 10 | chú thích 4, video 3 | 4 / 3 / 3 | 5 / 5 | 50 | đang chạy |
| 9= | Đối chiếu tập thực thể, đồ thị (không phải SPICE) | 10 | chú thích 6, video 3 | 0 / 2 / 8 | 1 / 9 | | không; SPICE là họ gần nhất |
| 11 | Đúng câu trả lời của mô hình hỏi đáp | 9 | sinh khác 5, tóm tắt 3 | 5 / 3 / 1 | 4 / 5 | | không |
| 12= | Người nghe, truy hồi, người đi theo | 8 | chú thích 6 | 4 / 0 / 4 | 3 / 5 | | từng thử, xem mục 5 |
| 12= | Thưởng học đối kháng, IRL | 8 | video 2, tóm tắt 2, sinh khác 2 | 5 / 2 / 1 | 5 / 3 | | không |
| 14 | Luật miền (toạ độ, IoU, định dạng) | 6 | GUI 4 | 1 / 1 / 4 | 5 / 1 | | từng thử (`report/144`) |
| 15= | CLIP-S, PAC-S | 5 | chú thích 5 | 0 / 2 / 3 | 4 / 1 | | không, mục 5 |
| 15= | Suy diễn, entailment | 5 | | 2 / 2 / 1 | 2 / 3 | | không |
| 17 | **SPICE thuần** | **3** | chú thích 1, video 1, sinh khác 1 | 2 / 1 / 0 | 3 / 0 | 30 | **ck500** |
| 18= | **SPIDEr** | 2 | chú thích 1, sinh khác 1 | 1 / 1 / 0 | 2 / 0 | | sắp chạy |
| 18= | TER, WER | 2 | | 1 / 1 / 0 | 1 / 1 | | không |
| 20= | **BCMR** | 1 | chú thích | 1 / 0 / 0 | 1 / 0 | | ưu tiên hai, đề nghị nâng |
| 20= | **chrF** | 1 | dịch (kèm BLEU, GAN) | 1 / 0 / 0 | 0 / 1 | | sắp chạy |

### 3.2 Theo mảng (ba nhãn đứng đầu)

| mảng | số bài | đứng đầu |
|---|---:|---|
| Chú thích ảnh + video | 64 | CIDEr 37 · BLEU 10 · tập thực thể 9 (rồi LLM 8) |
| Tóm tắt | 23 | ROUGE 21 · hỏi đáp 3 · (người, embedding, IRL mỗi loại 2) |
| Dịch máy | 19 | BLEU 17 · người 4 · GAN 3 |
| Sinh văn bản khác | 24 | ROUGE 7 · BLEU, GAN, hỏi đáp mỗi loại 5 |
| Text-to-SQL, chương trình | 15 | thực thi 15 (bao gồm một bài thay bằng so đồ thị SQL) |
| RLHF | 9 | người 4, LLM 5 (có bài chung) |
| GUI | 5 | luật miền 4 · thực thi 2 |
| Chỉ dẫn điều hướng | 1 thưởng / 10 đọc | thưởng học (SAS, preprint hoặc chưa kiểm); 9 bài còn lại không thấy độ đo câu làm thưởng |
| Từ 2024, trừ SQL | 37 | LLM 11 · tập thực thể 7 · embedding 6 · (ROUGE, luật miền, người nghe mỗi loại 4) · CIDEr 3 |

Đọc theo thời gian: trước 2020 ba độ đo n-gram chiếm phần lớn (CIDEr 25, ROUGE 23, BLEU 22 trên 80 bài). Từ 2024 trong mẫu này, tinh chỉnh LVLM chuyển sang LLM giám khảo, đối chiếu tập thực thể và thực thi. Xu hướng này một phần do truy vấn của tôi, nhưng khớp ghi chú cũ (`caption_textgen_rl.md`, các dòng 26, 27).

Tầng A và B đồng thuận ba độ đo đầu nhưng khác thứ tự: A là CIDEr 30, ROUGE 22, BLEU 19; B là ROUGE 15, BLEU 14, rồi embedding 11. CIDEr ở B chỉ 9 ⇒ vị trí số một của CIDEr **phụ thuộc** việc tôi đọc nhiều chú thích ảnh. Câu an toàn: "ba độ đo n-gram là cặp nền phổ biến; trong chú thích ảnh là CIDEr".

### 3.3 Bài gốc của từng độ đo

| độ đo | bài gốc | venue, kiểm |
|---|---|---|
| BLEU | Papineni và cộng sự, 2002 | ACL 2002, tr. 311–318, Anthology P02-1040, đã mở |
| ROUGE | Lin, 2004 | Text Summarization Branches Out, tr. 74–81, Anthology W04-1013, đã mở |
| METEOR | Banerjee & Lavie, 2005; Denkowski & Lavie, 2014 | Workshop ACL 2005, W05-0909; WMT 2014, W14-3348, đã mở |
| CIDEr, CIDEr-D | Vedantam và cộng sự, 2015 | CVPR 2015, trang CVF mở được; §8 của bài bàn việc chống khai thác. CIDEr-R: Santos và cộng sự, W-NUT 2021, 2021.wnut-1.39 |
| SPICE | Anderson và cộng sự, 2016 | ECCV 2016, Crossref 10.1007/978-3-319-46454-1_24 |
| SPIDEr, BCMR | Liu và cộng sự, 2017 | ICCV 2017, Crossref 10.1109/ICCV.2017.100 (theo ghi chú cũ, arXiv 1612.00370 đã đọc) |
| chrF | Popović, 2015 | WMT 2015, W15-3049, đã mở |
| BERTScore | Zhang và cộng sự | arXiv 1904.09675; ICLR 2020 **chưa kiểm** tại nguồn (OpenReview chặn) |
| BLEURT | Sellam và cộng sự, 2020 | ACL 2020, 2020.acl-main.704, đã mở |
| SimiLe | Wieting và cộng sự, 2019 | ACL 2019, P19-1427, đã mở |
| WMD (cho chú thích ảnh) | Kusner 2015 gốc **chưa kiểm**; Kilickaya và cộng sự | EACL 2017, E17-1019, đã mở |
| CLIPScore, RefCLIPScore | Hessel và cộng sự, 2021 | EMNLP 2021, 2021.emnlp-main.595, đã mở |
| PAC-S | Sarto và cộng sự, 2023 | CVPR 2023, trang CVF mở được |
| Polos | Wada và cộng sự, 2024 | CVPR 2024, trang CVF mở được |
| TIGEr | Jiang và cộng sự, 2019 | EMNLP 2019, D19-1220, đã mở |
| ViLBERTScore | Lee và cộng sự, 2020 | Eval4NLP 2020, 2020.eval4nlp-1.4, đã mở |
| LEIC | Cui và cộng sự, 2018 | CVPR 2018, trang CVF mở được |
| CLAIR | Chan và cộng sự, 2023 | EMNLP 2023, 2023.emnlp-main.841, đã mở |

### 3.4 Thứ tự ưu tiên chạy các độ đo

Đang chạy: CIDEr-D, METEOR, ROUGE-L. Phần chờ đề nghị xếp lại, thay thứ tự "BLEU-4, chrF, SPIDEr, BERTScore" ở `326`:

BLEU-4 (33 bài) → SPIDEr (tiền lệ trực tiếp, hai bài cho kết quả trái chiều) → BERTScore (9 bài, thêm họ mới) → BCMR (bài gốc của SPIDEr dùng làm đối thủ) → chrF (1 bài, lại đi kèm BLEU và GAN).

## 4. Bảng số đối đầu

**Luật đọc:** chỉ so trong cùng một bảng và cùng mô hình. Số giữa các bảng khác mô hình, dữ liệu, cách chia. Cột "phổ biến" của độ đo không phải chứng cứ về chất lượng.

### 4.1 Rennie và cộng sự, CVPR 2017, Bảng 3 (FC-2K, SCST, test Karpathy, COCO)

| thưởng | CIDEr | BLEU4 | ROUGE-L | METEOR |
|---|---:|---:|---:|---:|
| XE | 90,9 | 28,6 | 52,3 | 24,1 |
| **CIDEr** | **106,3** | 31,9 | 54,3 | 25,5 |
| BLEU | 94,4 | **33,2** | 53,9 | 24,6 |
| ROUGE-L | 97,7 | 31,6 | **55,4** | 24,5 |
| METEOR | 80,5 | 25,3 | 51,3 | **25,9** |

Chính bài viết: tối ưu CIDEr làm tăng mạnh nhất các độ đo khác. Không có SPICE. Ghi chú cũ ghi "train nhiều độ đo không vượt CIDEr đơn lẻ"; khi tìm lại tôi không thấy câu đó trong bản PDF, nên **không dùng câu này**.

### 4.2 Liu và cộng sự, ICCV 2017, Bảng 1 (Show-Tell, COCO C-5)

| phương pháp | CIDEr-D | METEOR | ROUGE-L | BLEU-4 |
|---|---:|---:|---:|---:|
| MLE | 0,947 | 0,251 | 0,531 | 0,294 |
| PG-BLEU-4 | 0,966 | 0,249 | 0,550 | 0,346 |
| PG-CIDEr | 0,995 | 0,249 | 0,548 | 0,333 |
| MIXER-BCMR-A | 0,991 | 0,258 | 0,545 | 0,317 |
| PG-BCMR | **1,013** | 0,257 | 0,550 | 0,332 |
| PG-SPIDEr | 1,000 | 0,251 | 0,544 | 0,322 |

BCMR = 0,5·BLEU-1 + 0,5·BLEU-2 + 1·BLEU-3 + 1·BLEU-4 + 1·CIDEr + 5·METEOR + 2·ROUGE; SPIDEr là "equal weight on SPICE and on CIDEr". Đánh giá người trên 492 ảnh: PG-SPIDEr thắng PG-BCMR (p = 0,014) dù thua trên mọi độ đo COCO. Nguyên văn về SPICE thuần: *"optimizing SPICE produced long repetitive sentences which are not good results"*, lý do *"SPICE ignores syntactic quality"*. Không có hàng số PG-SPICE.

⚠️ SPIDEr của lưới dùng 0,5·SPICE + 0,5·CIDEr-D/10, nên hai vế cùng cỡ [val: thưởng TB 0,348 và 0,310]. Nếu "equal weight" trong bài là hệ số 1 trên điểm thô thì CIDEr chiếm phần lớn [suy]. Phải khai đây là biến thể chia thang.

### 4.3 RL4LMs (Ramamurthy và cộng sự, ICLR 2023, Bảng 12, CommonGen, T5-base). Bảng gần ck500 nhất về thiết kế

Nguyên văn "we also train with task-specific rewards such as CIDEr, SPICE and SPiDer". Số trung bình theo PDF; độ lệch chuẩn bỏ để bảng gọn, chênh dưới khoảng 0,004–0,010 ở các cột 0–1 nên đọc thận trọng.

| khởi đầu + thuật toán | thưởng | Rouge-L | BLEU-4 | METEOR | CIDEr | SPICE | Coverage |
|---|---|---:|---:|---:|---:|---:|---:|
| Zero-shot | - | 0,264 | 0,006 | 0,203 | 6,200 | 0,115 | 91,07 |
| PPO từ T5 gốc | Rouge-1 | 0,354 | 0,087 | 0,235 | 8,673 | 0,157 | 88,54 |
| | METEOR | 0,308 | 0,088 | 0,220 | 7,251 | 0,161 | 79,72 |
| | **SPICE** | 0,302 | 0,067 | 0,193 | 6,571 | **0,175** | 69,34 |
| | CIDEr | 0,304 | 0,074 | 0,211 | 6,877 | 0,143 | 80,11 |
| | SPIDEr | 0,352 | 0,137 | 0,226 | **9,162** | **0,186** | 73,37 |
| Supervised | - | 0,438 | 0,329 | 0,321 | 16,385 | **0,299** | 94,48 |
| Supervised + PPO | Rouge-1 | **0,453** | 0,338 | 0,320 | 16,233 | 0,288 | 96,41 |
| | **METEOR** | 0,450 | **0,342** | **0,327** | **16,797** | 0,295 | **97,69** |
| | **SPICE** | 0,447 | 0,336 | 0,319 | 16,208 | 0,288 | 96,49 |
| | CIDEr | 0,446 | 0,309 | 0,316 | 15,497 | 0,283 | 96,34 |
| | SPIDEr | 0,448 | 0,319 | 0,317 | 15,678 | 0,281 | 96,15 |

Đọc [suy]: đây là bằng chứng gần nhất nhưng khác nhiều (câu từ tập khái niệm, T5, PPO). Khi đã có điểm tinh chỉnh, METEOR tốt nhất, SPICE không cao hơn Supervised trên chính SPICE, CIDEr thấp nhất. Khi xuất phát từ mô hình gốc, SPIDEr dẫn và coverage giảm mạnh theo SPICE. Bài cũng ghi nếu không có khởi đầu tốt thì "policies suffer from reward hacking". Hàng METEOR ở đây **không phải** bằng chứng cho cấu hình của dự án, nhưng đáng để dự đoán D1 ở `323` §9.3 được đọc nghiêm túc.

### 4.4 Consensus-based Sequence Training (Phan và cộng sự, 2017, preprint hoặc chưa kiểm, Bảng 4, video; tập dữ liệu của bảng chưa đối chiếu)

| thưởng | BLEU-4 | METEOR | ROUGE-L | CIDEr |
|---|---:|---:|---:|---:|
| XE | 43,0 | 28,7 | 61,7 | 47,3 |
| BLEU-4 | 41,9 | 28,4 | 61,1 | 45,5 |
| METEOR | 42,6 | 28,7 | 61,4 | 47,7 |
| ROUGE-L | 43,9 | 29,0 | 62,1 | 48,6 |
| **CIDEr** | **44,1** | **29,1** | **62,4** | **49,7** |

### 4.5 AREL (Wang và cộng sự, ACL 2018, Bảng 2, VIST)

| thưởng | BLEU-4 | METEOR | ROUGE-L | CIDEr |
|---|---:|---:|---:|---:|
| XE-ss | 13,7 | 34,8 | 29,7 | 8,7 |
| BLEU-RL | 13,9 | 34,6 | 29,0 | 8,9 |
| METEOR-RL | 6,8 | **40,2** | 30,0 | 1,2 |
| ROUGE-RL | 0 | 27,0 | **33,8** | 0 |
| CIDEr-RL | 13,8 | 34,9 | 29,7 | 8,1 |

Nguyên văn: "they are gaming their own metrics with nonsense sentences". Câu trong VIST dài và nhiều câu trong một mẫu, khác hẳn câu 7 từ của dự án.

### 4.6 Chú thích ảnh: phần thưởng có thêm thành phần

| bài, bảng | cấu hình | số | đọc |
|---|---|---|---|
| Chen, AAAI 2019 (cGAN, COCO, chọn λ) | CIDEr-D, λ = 0,3 | CIDEr 1,232 · BLEU-4 0,383 · SPICE 0,221 | các thưởng khác ở ghi chú cũ; không có SPICE làm thưởng |
| Luo, CVPR 2018 (ATTN, **val**) | MLE · CIDEr · CIDEr+DISC(1) | CIDEr 1,1078 · 1,1332 · 1,1406; SPICE 0,2019 · 0,2083 · 0,2113; truy hồi 72,40 · 71,05 · 75,74% | người nghe với trọng số nhỏ tăng cả CIDEr, SPICE lẫn truy hồi |
| Cho, Findings NAACL 2022 (COCO) | MLE · CIDEr · CLIP-S · CIDEr+CLIP-S · CLIP-S+Grammar | CIDEr 110,3 · 124,9 · 11,2 · 124,6 · 71,0; R@1 21,8 · 20,9 · 42,5 · 24,4 · 35,8 | CLIP thuần phá độ đo so câu; có người chấm ưa CLIP-S+Grammar (51,0 thắng, 30,8 thua) |
| Self-Cap, ICPR 2024 (RN50) | không · CIDEr · CLIP-S · PAC-S · Self-Cap | CIDEr 109,8 · 126,8 · 3,1 · 32,2 · 72,0; SPICE 20,3 · 21,2 · 21,2 · 21,7 · 21,8; **Rep-1** 1,516 · 1,384 · 11,762 · 5,453 · 2,706 | SPICE ít thay đổi kể cả khi CIDEr sập; thưởng CLIP sinh câu lặp |
| CIDEr-R, W-NUT 2021 (AoANet, **COCO một câu chuẩn**) | tối ưu CIDEr-D · CIDEr-R | CIDEr-R 101,0 · 110,5; CIDEr-D 97,9 · 93,5; SPICE 22,7 · 23,5; ROUGE-L 36,8 · 36,2; METEOR 16,7 · 15,6; BLEU-4 11,0 · 9,5 | bối cảnh gần dự án nhất về "một câu chuẩn", nhưng câu dài hơn (13,7 từ); kết quả không một chiều |
| DMO, ACL 2024 (GIT-base, Flickr8k, **không RL**) | CIDEr · BLEU-4 · METEOR · ROUGE-L · LM | CIDEr 97,0 · 96,8 · 96,1 · 96,0 · 95,1 | chênh rất nhỏ; Bảng 1 bài |
| FOCUS, EMNLP 2026 theo ghi chú arXiv (Qwen2.5-VL-3B, CompreCap, General) | SFT · SFT+CLIP · SFT+CompreCap · SFT+FOCUS | Overall 47,08 · 45,35 · 46,76 · 50,82 | GRPO, thưởng tập thực thể có LLM xác minh; chính tác giả đề xuất; thang điểm của bài, **chưa kiểm venue tại trang kỷ yếu** |

### 4.7 Video, tóm tắt, dịch máy, báo cáo y khoa

| bài, bảng | thưởng và số | đọc |
|---|---|---|
| Pasunuru & Bansal, EMNLP 2017, Bảng 5 (MSVD) | XE · CIDEr-RL · CIDEnt-RL: BLEU 52,4 · 53,3 · 54,4; CIDEr 83,9 · 89,4 · 88,6; CIDEnt 68,1 · 69,4 · 71,6 | Có câu "as a reward... produced long repetitive phrases" về SPICE, không có hàng số |
| Pasunuru & Bansal, NAACL 2018, Bảng 1 (CNN/DM) | XE · ROUGE · Entail · ROUGESal · ROUGESal+Ent: R-L 36,07 · 36,66 · 36,44 · 37,00 · 37,10; METEOR 18,27 · 18,93 · 20,15 · 19,84 · 20,02 | Thưởng sửa từ ROUGE hơn ROUGE thuần |
| Li, EMNLP 2019, Bảng 1 (Gigaword) | XENT · ROUGE · ROUGE+XENT · DSR (BERTScore): F_BERT 65,78 · 61,46 · 66,50 · 67,06; ROUGE 40,77 · 42,73 · 42,72 · 41,73 | Thưởng nào thắng cột của nó. Người chấm: DSR thắng ROUGE+XENT 45,4/27,2 về liên quan, 45,4/28,8 về trôi chảy (Gigaword) |
| Yan, 2021, preprint hoặc chưa kiểm, Bảng 2 (Ru-En) | Baseline · R-SBLEU · R-BLEURT: BLEU 34,20 · 35,11 · 33,07; BLEURT 0,086 · 0,094 · 0,155 | BLEURT làm tăng độ đầy đủ theo người, nhưng BLEU giảm; Ja-En BLEU rơi 28,81 → 20,75 |
| Ive và cộng sự, EACL 2021, Bảng 1 (Multi30K EN-FR 2016) | MLE · ERAC · SAC BLEU · SAC không giám sát: BLEU 57,5 · 59,4 · 57,9 · 56,9 | "sparse and biased" là lập luận, số không chênh nhiều |
| Miura, NAACL 2021, Bảng 2 (Open-i) | NLL · NLL+CDr · NLL+BS · NLL+BS+factENT · NLL+BS+factENTNLI: BLEU4 8,2 · 13,4 · 12,3 · 12,0 · 13,1; CIDEr-D 64,4 · 97,2 · 87,3 · 99,6 · 103,4; factENT 31,1 · 40,6 · 41,5 · 44,4 · 43,6 | Thưởng F1 thực thể tăng cả CIDEr-D, gần ý SPICE nhất ngoài SPICE |
| Delbrouck, Findings EMNLP 2022, Bảng 1 (MIMIC-CXR) | NLL · factENT (Miura) · RGER: factENT 28,0 · 39,5 · 42,5; RG_ER 20,2 · − · 34,7; BLEU4 10,5 · 11,1 · 11,4 | Thưởng đồ thị riêng miền (RadGraph) |
| SDR, 2026, preprint hoặc chưa kiểm, Bảng 1 (ReXGradient, Qwen3-VL-2B) | SFT · R_exact · R_Chamfer · R_Haus: BERTScore 0,339 · 0,332 · 0,367 · 0,339; RadGraph 0,247 · 0,244 · 0,224 · 0,258 | GRPO, trung bình 5 hạt giống; khoảng cách tập trên embedding thắng so khớp chính xác; không thắng tất cả cột |

### 4.8 Độ đo khớp với hành vi tới đâu (Zhao, EACL 2021, Bảng 3; Kendall τ, khoảng 90%)

Dấu mong muốn: âm với sai số NE, dương với SR, SPL, Quality.

| mức | điểm | NE↓ | SR↑ | SPL↑ | Quality↑ |
|---|---|---:|---:|---:|---:|
| **Hệ thống**, tất cả | **SPICE** | (−0,67; −0,28) | (−0,06; 0,61) | (0,44; 0,78) | (0,56; 0,83) |
| | CIDEr | (0,06; 0,39) | (−0,22; 0,39) | (−0,22; 0,00) | (0,17; 0,39) |
| | BERTScore | (0,06; 0,39) | (−0,22; 0,39) | (−0,22; 0,00) | (0,17; 0,39) |
| **Từng chỉ dẫn**, tất cả | **SPICE** | (−0,05; −0,02) | (0,00; 0,04) | (0,03; 0,06) | (0,03; 0,07) |
| | BERTScore | (−0,04; 0,00) | (0,07; 0,12) | (−0,01; 0,03) | (0,07; 0,11) |
| | Tương thích (mô hình) | (−0,20; −0,17) | (0,13; 0,17) | (0,17; 0,20) | (0,19; 0,23) |
| **Từng chỉ dẫn**, chỉ câu mô hình | **SPICE** | (−0,05; 0,00) | (0,00; 0,05) | (0,00; 0,05) | (0,01; 0,06) |
| | CIDEr, BLEU-4, METEOR | quanh 0 | quanh 0 | quanh 0 | quanh 0 |
| | BERTScore | (−0,22; −0,18) | (0,19; 0,24) | (0,18; 0,23) | (0,16; 0,20) |
| | SPL 3 tác tử | (−0,26; −0,21) | (0,21; 0,27) | (0,21; 0,26) | (0,09; 0,14) |
| | Tương thích | (−0,25; −0,20) | (0,22; 0,27) | (0,21; 0,25) | (0,18; 0,23) |

Nguyên văn: *"SPICE scores for individual instructions have high variance, and so SPICE does not correlate with wayfinder performance at the instruction level."*

Hệ quả: nếu Zhao đúng cho GUI thì độ đo chữ cổ điển đều yếu ở mức câu, còn BERTScore và điểm từ tác tử đi theo mới mang tín hiệu. Đối chiếu với COCO: Learning Compact Reward (preprint), Bảng 3, tương quan mức câu với người: SPICE Pearson 0,44, CIDEr 0,40, BLEU4 0,33. Hai nguồn trái nhau, có thể do miền và độ dài câu [suy].

### 4.9 SPICE làm thưởng: bài nào nói gì

| lập trường | nguồn | nội dung | hạn chế khi áp vào bài này |
|---|---|---|---|
| Ủng hộ gián tiếp | Anderson, ECCV 2016 | tương quan với người trên COCO | đánh giá, không phải thưởng; nhiều câu chuẩn |
| Ủng hộ gián tiếp | Liu 2017 | SPIDEr được người chấm hơn BCMR, tức thành phần SPICE có giá trị | SPICE phải đi với CIDEr |
| Ủng hộ gián tiếp | Compact Reward (preprint) | tương quan mức câu cao nhất trong nhóm thủ công | COCO |
| Ủng hộ gián tiếp | Miura, Delbrouck, SC-Captioner (ICCV 2025), FOCUS | thưởng dạng F1 trên tập thực thể tốt hơn thưởng n-gram | độ đo riêng miền hoặc có LLM, không phải SPICE; tôi là người đọc ra sự tương đồng |
| Có số, trung tính đến bất lợi | RL4LMs | Bảng 4.3 | khác nhiệm vụ, PPO |
| Phản đối | Liu 2017 | câu dài, lặp cụm, bỏ cấu hình | không có phạt độ dài, không khởi đầu từ điểm SFT mạnh như dự án; không có số |
| Phản đối | Pasunuru 2017 | như Liu | không có số |
| Phản đối phạm vi | Zhao 2021 | mức câu không tương quan | điều hướng, chỉ dẫn dài |
| Phản đối gián tiếp | `report/328` [đo] và `323` §9 [val] | SPICE dự báo exec kém nhất: AUC 0,671 so với CIDEr-D 0,741, METEOR 0,750 | khả năng dự báo trên câu tĩnh không chứng minh kết quả train |

Số của dự án: thưởng SPICE ck500/101 exec 60,65, ck500/202 cao hơn S1/101 +0,83, ghép ngẫu nhiên ngang S1 (`report/328`). Đây là chỗ ủng hộ duy nhất có số trên đúng dữ liệu, và nó chứng minh *SPICE có tín hiệu*, chưa chứng minh SPICE hơn độ đo khác. A2 (CIDEr-D, lệch ba biến) − ck500/101 −0,69 [−1,34; −0,02], − ck500/202 +0,02.

### 4.10 Điểm yếu đã biết, kèm kiểm trên chính câu chuẩn của dự án

**Kiểm đặc tính [đo].** 400 câu chuẩn bước chạm của `val_cham600` (lấy từ 602, tách được 558), biến đổi có kiểm soát, điểm so với câu gốc bằng đúng hàm thưởng của lưới, không có phạt độ dài. Không dùng câu mô hình hay bộ trỏ, nên không phải kết quả về mô hình. Trung vị **6 từ** (tập dạy 40.174 câu chạm: 4,3% ≤ 3 từ, 40,5% ≤ 5 từ, p10 = 4, p90 = 13).

| biến đổi | SPICE | CIDEr-D/10 | BLEU-4 | ROUGE-L | METEOR | chrF | BERTScore | muốn |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| đổi động từ đồng nghĩa ("Click" → "Tap") | **0,975** | 0,827 | 0,677 | 0,841 | 0,478 | 0,789 | 0,872 | cao |
| đảo trật tự (vị trí lên trước) | 0,855 | 0,912 | 0,918 | 0,888 | 0,882 | 0,967 | 0,954 | cao |
| bỏ mệnh đề vị trí | 0,836 | 0,789 | 0,658 | 0,871 | 0,797 | 0,839 | 0,859 | trung bình |
| đổi vị trí đối xứng (n = 110) | 0,677 | 0,763 | 0,693 | 0,881 | 0,474 | 0,815 | **0,942** | thấp |
| **sai tên phần tử**, giữ khung | 0,198 | **0,102** | 0,323 | 0,592 | 0,269 | 0,475 | 0,506 | thấp |
| câu của bước khác | 0,053 | 0,011 | 0,155 | 0,386 | 0,160 | 0,295 | 0,347 | thấp |
| "Click on the button." | 0,046 | 0,007 | 0,211 | 0,480 | 0,175 | 0,315 | 0,485 | thấp |
| lặp tên phần tử hai lần ở cuối | 0,698 | 0,272 | 0,455 | 0,756 | 0,515 | 0,818 | 0,673 | thấp |
| **sai loại thao tác** ("Swipe up on …") | **0,919** | 0,604 | 0,583 | 0,789 | 0,453 | 0,774 | 0,744 | thấp |
| sai loại ("Go back from …") | **0,945** | 0,516 | 0,466 | 0,656 | 0,397 | 0,705 | 0,665 | thấp |
| P(đổi động từ > sai tên) | 0,991 | **1,000** | 0,988 | 0,965 | 0,980 | 0,983 | **1,000** | ≈ 1 |
| P(bỏ vị trí > sai tên) | 0,776 | **0,870** | 0,740 | 0,730 | 0,743 | 0,738 | 0,823 | cao |
| P(câu gốc > sai loại "Swipe") | **0,670** | 1,000 | 1,000 | 1,000 | 1,000 | 1,000 | 1,000 | ≈ 1 |

SPICE thêm [đo]: 97,3% câu đổi động từ có điểm **bằng đúng** câu gốc. Mỗi câu chuẩn có trung vị 3 tuple (TB 3,68: đối tượng 1,81, thuộc tính 1,38, **quan hệ 0,50**); 46% có ≤ 2 tuple; 1,7% không có tuple nào. Lập luận "SPICE so đối tượng, thuộc tính, quan hệ" (`323` §3) phải sửa: trên câu GUI quan hệ gần như vắng mặt. Với 300 câu chuẩn **không chạm**, đổi sang câu "Click on …" cùng từ vựng: SPICE 0,780 (scroll 0,771, quay lại 0,886), trong khi tự so với chính nó chỉ 0,914 và 8,6% câu không chạm có SPICE = 0. So sánh: BLEU-4 0,538, CIDEr-D 0,609, chrF 0,750.

⚠️ **Phép kiểm này không dự báo thứ hạng lưới.** Nó đo tính chất của độ đo trên biến đổi do tôi chọn. Động từ và tên thay bằng luật đơn giản, câu sinh của mô hình không giống vậy. "Sai loại thao tác" là phép thay từ, không phải câu thật của bước khác loại.

**Tổng hợp điểm yếu:**

| độ đo | từ tài liệu | trên dữ liệu dự án [đo] | câu ngắn, một câu chuẩn |
|---|---|---|---|
| **BLEU-4** | Mức câu cần làm mượt (Chen & Cherry, WMT 2014, W14-3346); không tương quan tốt với người (Liu 2017, Zhao 2021); tốt cho cột của nó, PG-BLEU-4 (Bảng 4.2) | 40,5% câu dạy ≤ 5 từ, nên 4-gram rất ít; khuôn câu vẫn được 0,211 do làm mượt | yếu nhất về lý thuyết; câu ≤ 3 từ (4,3%) không có 4-gram |
| **ROUGE-L** | AREL "gaming"; Paulus: ROUGE-2 làm câu đạt độ dài tối đa, chọn ROUGE-L; Guo: RL ROUGE khó đọc | Dải hẹp nhất: khuôn 0,480, sai tên 0,592 | LCS trên 6 từ thì khung câu chiếm nhiều |
| **METEOR** | AREL; ReGen dùng làm thưởng tốt nhất trên WebNLG; RL4LMs tốt nhất Bảng 4.3 | Đổi Click → Tap chỉ 0,478, gần bằng đổi vị trí; WordNet không cứu từ GUI | phạt phân mảnh rất mạnh; tốc độ bị Java (28 s/3.500 câu) |
| **CIDEr-D** | Cần IDF kho; Vedantam tự khai khả năng bị khai thác; Guo: kết thúc lỗi 43,7–46,4%; Hu 2023 (SacreEOS, LNCS theo Crossref): đoạn câu vụn khớp mảnh câu chuẩn; CIDEr-R: yếu khi một câu chuẩn và độ dài biến thiên | Tách tên sai mạnh nhất; phạt lặp (0,272). df cố định từ câu dạy; chỉ 0,11–0,13% câu A2 kết thúc bằng hư từ (test) nên chứng lỗi của Guo không lặp lại | CIDEr gốc là "consensus" nhiều câu chuẩn; với một câu chuẩn tiêu chuẩn của điểm khác (lớn hơn 100, `289`). Phạt độ dài σ = 6 hầu như không tác dụng khi câu 7 từ [suy] |
| **SPICE** | Liu, Pasunuru, Zhao; phụ thuộc parser | Mù loại thao tác; tuple rất ít; hoà 38,21% cặp trong nhóm [val] | Nhiều nhóm 8 câu hoà toàn bộ [val 7,23%, gấp 4 lần CIDEr-D] |
| **SPIDEr** | Liu: người thích hơn BCMR; RL4LMs: khi có Supervised thì CIDEr và SPICE đều không nâng | Thừa hưởng độ mù một phần: bên CIDEr-D vẫn thấy thao tác [suy] | Chia thang của lưới là tuỳ chọn của dự án |
| **BERTScore** | Li 2019 tốt; Zhao mức câu cao hơn độ đo chữ; PrefBERT (preprint) chê ROUGE-L, BERTScore kém người chấm | Gần như mù vị trí (0,942), khuôn vẫn 0,485 | Rescaled giúp, nhưng khung câu giữ điểm |
| **chrF** | Chỉ thấy 1 bài dùng làm thưởng (Kong và cộng sự, AAAI 2019) | Lặp được thưởng (0,818); không tách mạnh | Có đủ dữ liệu ký tự; không có IDF |

## 5. Các họ khác và khả năng áp dụng

| họ | ví dụ có số | hợp bài toán? | đã thử trong dự án | máy | đề xuất |
|---|---|---|---|---|---|
| **CLIPScore, RefCLIPScore** | Cho, Self-Cap; DiCO (BMVC 2024) dùng KL để giữ CIDEr | **Yếu [đo]:** CLIP ViT-B/32 (224 px), 400 màn: gốc 0,645 · đổi động từ 0,642 · sai tên 0,597 · câu khác 0,588 · khuôn 0,582; P(đổi động từ > sai tên) 0,690; P(gốc > khuôn) 0,805. Có tín hiệu, nên không viết "không đọc được chữ", viết "tín hiệu nhỏ hơn hẳn". Lịch sử cho thấy thưởng CLIP dễ sinh câu lặp | chưa (test CPU trong phiên này) | CPU | **Không chạy.** Trình số trên |
| **BLEURT** | Yan 2021: BLEU có thể tụt | Câu dài nhiều ngôn ngữ; huấn luyện cho dịch, chưa thấy dùng câu GUI | chưa | cần tải mô hình; [suy] Kaggle | Chỉ khi BERTScore đứng cao |
| **TIGEr, ViLBERTScore, Polos** | đều là độ đo đánh giá; không thấy dùng làm thưởng trong mẫu | Cần đặc trưng vùng ảnh hoặc học trên COCO, câu GUI khác xa | chưa | Colab nếu làm | Không chạy, không có tiền lệ thưởng |
| **Embedding khác (SimiLe, WMD)** | Wieting 2019, Chen ICLR 2020 (BLEU + WMD), không bảng so riêng WMD ở đây | Tên phần tử là tên riêng, embedding từ không phân biệt được [suy] | chưa | CPU | Không chạy, BERTScore đại diện |
| **Người nghe, truy hồi** | Luo 2018 (Bảng 4.6) có số dương; Liu 2018; LoGIC, RRG (ECCV 2026 theo ghi chú arXiv) | **Hợp nhất về lý thuyết:** thưởng "câu đủ để bên kia trỏ đúng", và Zhao cho thấy điểm từ tác tử có tín hiệu mức câu | **Đã có từ ck500:** SPICE-cont, SPICE+LR, SPICE+GLR (`288`–`289`), không qua sàng [val]; `CLAUDE.md` có Phi-4 3,13 s/bước. **Chưa thử từ S1.** | T4×2 [suy] nếu Phi-4 chiếm GPU thứ hai; chưa probe | **Thêm** (mục 7) |
| **Thực thi bằng bộ trỏ** | SQL: toàn bộ 15 bài dùng thực thi, ở đó kết quả đúng là đúng khách quan | Khác cơ bản: bộ thực thi là mô hình học được. Dùng UGround = tối ưu đúng dụng cụ chấm (Goodhart). Dùng UI-Venus thì độc lập hơn nhưng cùng họ Qwen; đo được bằng UGround | gần nhất là Phi-4 | Colab; [suy] thêm 4 s × 32 câu mỗi bước | **Ghi lại** (mục 8) |
| **LLM giám khảo** | CapRL, CCCaption, BalCapRL, Rubric; các bài này nói rõ về reward hacking | Câu 7 từ có câu chuẩn: giám khảo chỉ so nghĩa, khó thêm gì so với METEOR hay BERTScore [suy]; thêm GPU; thêm khả năng bị khai thác | chưa | Kaggle nếu LLM nhỏ | Không ưu tiên |
| **Hỏi đáp (QA)** | Scialom 2019; Xie và cộng sự: thưởng trả lời được có thể đưa vào thiên lệch (COLING 2020, 2020.coling-main.228) | Câu GUI không chứa thông tin để hỏi; người nghe là bản đúng hơn [suy] | chưa | | Không chạy |
| **Tập thực thể, tên phần tử** | Miura, Delbrouck (Bảng 4.7) | Hợp: `descriptors.jsonl` có tên chuẩn từ OCR/cây trợ năng; điểm nghẽn đã đo là gọi tên (bỏ tên −28,5 pp) | Gần: GRPO `<point>` (`144`), r_name thưởng ≤ 0,1; khai báo tăng +2,56 nhưng exec +0,02; khác vì không phải câu | Kaggle | **Thêm** (mục 7) |
| **Loại thao tác** | CIDEnt là tiền lệ về "cổng" sửa phần thưởng | Trực tiếp vá điểm mù SPICE [đo] | A7 (CIDEr-D + đúng loại) định nghĩa ở `279`, chưa chạy; CTG có test nhưng là cộng vào lợi thế | Kaggle | **Thêm** (mục 7) |
| **Tổ hợp BCMR, SPIDEr** | Liu 2017; không tổ hợp nào thắng toàn diện | Rẻ, tiền lệ trực tiếp | SPIDEr sắp chạy; BCMR xếp B10 | Kaggle | Nâng BCMR |
| **CIDEr-R** | Bảng 4.6 | Sinh ra cho một câu chuẩn, nhưng độ dài dự án hẹp (p10–p90: 4–13), ưu thế về độ dài ít quan trọng [suy] | chưa | Kaggle | Có điều kiện |
| **GAN, IRL** | SeqGAN, AREL, Compact Reward | Đổi cả nguồn thưởng; khó ổn định; phiên bản dự án không có người chấm để xác nhận | chưa | Kaggle, viết mới | Đã ở đợt 4 (`329`), giữ nguyên |
| **Thưởng người** | InstructGPT, Stiennon | Cần nhãn người; user quyết không chấm 100 câu | không | không | Không chạy |

## 6. Debate

### Lập trường A: bảo vệ SPICE

- Chạy thật có kết quả: hai hạt hơn S1, ghép ngẫu nhiên ngang S1. Tín hiệu là thật (`328`). Không độ đo nào khác có điều này trên kịch bản sạch tính tới hôm nay.
- Kiểm đặc tính [đo]: SPICE là độ đo duy nhất giữ gần nguyên điểm khi đổi động từ đồng nghĩa, phạt khuôn câu mạnh. Người ta nói "Click" hay "Tap" đều trỏ được, nên phần thưởng không nên phạt việc đó. BLEU-4, METEOR phạt nặng tới 0,48–0,68.
- Nhận xét của Liu không lặp lại [đo]: ck500 lặp bigram còn thấp hơn S1.
- "Yếu ở tín hiệu bước đầu" có thể là điểm mạnh: thưởng hoà nhiều, cập nhật ít, chính sách ít trôi khỏi S1, giữ được đặc tính của tập dạy [suy, D1 ở `323`].
- Không có bộ trỏ trong thưởng nên không tối ưu theo dụng cụ.

**Bị phản bác:** "ít trôi" chưa đo được, và có thể nói y hệt về thưởng yếu nói chung. Bền trước đổi động từ cũng là mù loại thao tác. Không có tiền lệ thuận chiều trực tiếp.

### Lập trường B: phản đối SPICE

- Tiền lệ: hai bài thử rồi bỏ, bài có số không ủng hộ. Mức câu không tương quan (Zhao).
- Trên dữ liệu: ít tuple (trung vị 3); thưởng hoà nhiều nhất; dự báo exec kém nhất cả trên test (`328`); mù loại thao tác [đo]. Điều cuối giải thích được một phần việc ck500 rớt scroll: câu nêu đúng tên phần tử được điểm cao dù sai động từ, trong khi tập dạy thiên về câu chạm [suy]. Nhưng A2 (CIDEr-D) cũng rớt scroll tương đương (77,62, `328`), nên điểm mù này **không phải** lời giải thích đủ.
- Phần lặp lại được của mức tăng lại là sửa loại thao tác (`328`), điều SPICE không thấy trực tiếp ⇒ phần tăng có thể đến từ việc "học thêm có tín hiệu" chứ không phải từ tính chất đặc biệt của SPICE [suy].

**Bị phản bác:** bài nói SPICE sinh câu lặp không áp dụng; dự báo trên câu tĩnh không chứng minh kết quả train (tiền lệ `252`: oracle mạnh nhưng policy không theo); phép so cũ với CIDEr-D chưa sạch.

### Lập trường C: nên chọn CIDEr-D

- Phổ biến nhất ở chú thích ảnh; tiền lệ dày nhất cả về nâng độ đo khác (Rennie, CST).
- Kiểm đặc tính tốt nhất cho điều quan trọng nhất: sai tên 0,102 và P = 0,870; thấy được loại thao tác; phạt lặp. IDF ở đây **là ưu điểm**: tên riêng phần tử hiếm nên nặng ký [đo gián tiếp].
- Không có Java nặng; `326` đo 149 s/bước, nhanh hơn SCST + SPICE 158 s/bước.

**Bị phản bác:** khoảng cách kho không ổn định theo tập; với một câu chuẩn CIDEr-R cho thấy có vấn đề; AUC cao chưa thành exec; A2 test ngang hoặc thua ck500 tuỳ hạt. Bảng 4.3 CIDEr làm thưởng lại thấp nhất. Chỉ có bài dùng nhiều câu chuẩn (COCO) mới ủng hộ mạnh.

### Lập trường D: nên chọn SPIDEr

- Tiền lệ đúng ý và là cách chữa chính lời chê của Liu. Có đánh giá người p = 0,014. Bù: SPICE bền với đồng nghĩa, CIDEr-D thấy thao tác và trật tự.

**Bị phản bác:** RL4LMs dòng Supervised: SPIDEr không hơn thành phần nào. `thuong_dac_tinh` [val] cho SPIDEr tín hiệu không vượt CIDEr-D. Nếu SPICE vốn đã không có tác hại lặp thì động cơ gốc của SPIDEr không còn.

### Lập trường E: nên thưởng người nghe

- Khớp đúng mục tiêu: câu đủ để mô hình khác trỏ đúng. Có số dương ở Luo 2018. Từ 2024 có thêm LoGIC, RRG, REMUL.
- Zhao: điểm theo tác tử có tín hiệu mức câu, khác hẳn độ đo chữ.

**Bị phản bác:** Dessì 2022 và Luo 2017 cảnh báo bộ máy thích câu máy kiểu riêng (`report/141`); `289` (từ ck500) không qua sàng, văn bản xấu đi [val]; đắt gấp đôi; có nguy cơ cùng họ nếu chọn bộ trỏ Qwen. Phi-4 không phải bộ chấm headline nên Goodhart thấp hơn, không phải bằng 0. Một lượt từ S1 mới là phép so sạch.

### Kết luận debate

1. **Không lập trường nào thắng được bằng tài liệu.** Tài liệu đủ để loại CLIP, BLEURT, LLM giám khảo khỏi ưu tiên, không đủ chọn giữa SPICE, CIDEr-D, METEOR, SPIDEr. Đây là câu hỏi thực nghiệm và lưới là cách trả lời đúng.
2. Trục mạnh nhất cho SPICE không phải "nó bắt ý nghĩa", mà là **chạy thật có tín hiệu, ít khai thác được trên câu ngắn, không có bộ trỏ trong thưởng**. Trục "tiền lệ" nên bỏ, trục "Zhao khuyên" phải bỏ.
3. Nếu METEOR hoặc CIDEr-D ≥ SPICE, đúng dự đoán D1 và giải thích được bằng tín hiệu. Nếu SPICE vẫn hơn cả hai hạt, phải giải thích bằng cơ chế khác, không được viết như một điều đã biết trước.
4. Một hạt giống: "hơn" theo luật `326` §7: KTC ghép cặp loại 0 và |Δexec| ≥ 1, Holm cho nhiều phép so. Theo `328`, kết cục có khả năng nhất là một nhóm ngang nhau, nên phải chuẩn bị câu trả lời đó.

## 7. Lượt nên thêm hoặc xếp lại trong lưới

Tất cả GRPO, hạt 101, cùng kịch bản với lưới; mỗi lượt [suy] khoảng 20,6 h T4 trừ khi ghi khác. Tôi không đẩy lượt nào. Mã `grpo_luoi.py` khoá md5 tới hết lô 1, nên phần thưởng mới phải đợi tới lúc đó.

| ưu tiên | lượt | lý do | máy | mã | đọc kết quả |
|---:|---|---|---|---|---|
| 1 (có sẵn) | BLEU-4 | phổ biến thứ ba | Kaggle | xong | |
| 2 (có sẵn) | SPIDEr | tiền lệ trực tiếp | Kaggle | xong | khai biến thể chia thang |
| 3 (có sẵn) | BERTScore | họ embedding | Kaggle | xong, chưa probe | [đo] roberta-large trên CPU máy nhà 0,11–0,23 s/câu ⇒ 32 câu ≈ 4–7 s/bước; [suy] có thể đặt CPU để tránh rủi ro VRAM 12,71 GiB |
| 4 (nâng) | **BCMR** (đúng trọng số của Liu; thay đổi nào cũng phải khai) | đối thủ trực tiếp của SPIDEr trong bài gốc; đang ở B10 | Kaggle; METEOR Java đã chạy được | thêm một phần thưởng | |
| 5 (mới) | **SPICE có cổng loại thao tác:** r = SPICE · a, a = 1 nếu đúng loại, a nhỏ nếu sai; bổ sung so với A7 | vá điểm mù [đo], thử trực tiếp giả thuyết "mù thao tác gây rớt scroll"; tiền lệ dạng CIDEnt | Kaggle | hàm loại thao tác `canon_action` có sẵn; **đo tỉ lệ bước không chạm trong câu nhắc** vì 3.991 câu nhắc có thể chỉ gồm bước chạm | ⚠️ nghĩ ra sau khi đã thấy số test ck500, phải khai; đo cả bước không chạm |
| 6 (mới) | **Tên phần tử + loại thao tác**: F1 token với tên vàng, cộng a | khác hẳn các thưởng so câu; khớp điểm nghẽn "gọi tên"; tiền lệ factENT | Kaggle | viết mới, ghép `descriptors.jsonl`; bước không có tên vàng phải có luật rõ | có thể dạy mô hình chép tên, kiểm hình thức câu |
| 7 (mới, probe trước) | **Người nghe Phi-4 từ S1**, SPICE + LR | so sạch họ người nghe; `288`–`289` chỉ đi từ ck500 | T4×2: một lượt chiếm cả hai GPU. [suy] thêm khoảng 100 s/bước ⇒ ~35 h, 3–4 commit, gấp đôi hạn mức. Probe VRAM; tràn thì mục 8 | sửa từ `_scripts/288/` | so cả exec và độ đo văn bản |
| 8 (có sẵn) | chrF | một tiền lệ, đi sau | Kaggle | xong | |
| 9 (điều kiện) | CIDEr-R | chỉ khi CIDEr-D ≥ SPICE | Kaggle | công thức ngắn, viết mới | |

Không đề nghị: CLIP, BLEURT, TIGEr, ViLBERTScore, Polos, QA, LLM giám khảo (trừ khi user muốn dòng đại diện). Việc 0 GPU nên làm cùng: đo hình thức câu cho mọi lượt sau khi có câu (`runs/khao_sat_do_do_330/khaosat330_hinhthuc.py`, bản rút gọn của bước F1 ở báo cáo khảo sát).

## 8. Cần Colab: ghi lại, user quyết

| thứ tự | việc | vì sao | mức quan trọng |
|---:|---|---|---|
| 1 | Người nghe Phi-4 từ S1 nếu probe T4×2 tràn hoặc quá lâu | lượt 7 ở trên; `288` từng chạy A100 80 GB, ~40–55 đơn vị/phiên | Cao |
| 2 | Thưởng bằng UI-Venus-7B (bộ trỏ khác), chấm bằng UGround | đại diện họ "thực thi"; ~4 s/câu × 32 câu/bước [suy, từ phép B]; UI-Venus cùng họ Qwen, phải khai; rất tốn | Trung bình đến cao |
| 3 | LLM giám khảo có ảnh (nếu thầy hỏi tới) | đại diện xu hướng 2024+, có thêm mô hình | Thấp |

## 9. Câu trả lời đề xuất cho thầy

**Dùng ngay hôm nay, chưa có số lưới (không có số val):**

> Thưa thầy, em chưa kết luận SPICE tốt nhất. Em đã khảo sát 198 bài có chủ đích ở chú thích ảnh, video, tóm tắt, dịch máy, sinh văn bản, text-to-SQL, chỉ dẫn điều hướng, RLHF và GUI. Trong mẫu này, độ đo làm thưởng phổ biến nhất là CIDEr ở chú thích ảnh, ROUGE ở tóm tắt, BLEU ở dịch máy; SPICE thuần ít gặp và tiền lệ không thuận: Liu ICCV 2017 và Pasunuru EMNLP 2017 thấy câu dài, lặp, còn RL4LMs ICLR 2023 không cho thấy SPICE hơn. Zhao EACL 2021 chỉ khuyên SPICE ở mức hệ thống. Vì vậy em không dựa vào tiền lệ để chọn SPICE. Lý do đưa ra được là trên câu ngắn, độ đo này giữ điểm khi đổi động từ đồng nghĩa và phạt mạnh câu sai phần tử, không dùng bộ trỏ trong phần thưởng, và ck500 không tái lập việc lặp câu. Em cũng đo được điểm yếu: SPICE gần như không thấy loại thao tác. Phần so trực tiếp, cùng kịch bản, với CIDEr-D, METEOR, ROUGE-L, BLEU-4, SPIDEr, BERTScore đang chạy, chưa có số; em sẽ báo vô điều kiện.

**Trường hợp 1: SPICE đứng đầu, KTC ghép cặp loại 0 và |Δexec| ≥ 1 sau Holm, lặp lại ở hạt thứ hai.** (Điền số vào [ ].)

> Trên cùng kịch bản và hạt giống, thưởng SPICE đạt exec [ ], hơn [độ đo đứng hai] [ ] với KTC [ ], hơn cả ở hạt [ ]. Điều này đi ngược dự đoán em ghi trước khi chạy dựa trên tín hiệu ở bước đầu, nơi SPICE yếu nhất, nên kết quả không được giải thích bằng "SPICE dự báo exec tốt hơn". Giải thích em kiểm là [theo kết quả H1, H3–H5]. Điểm yếu vẫn còn: [số bước không chạm], [hình thức câu]. Em viết là "đứng đầu trong các cấu hình đã so", không viết là tốt nhất nói chung, vì khảo sát cho thấy ở nhiệm vụ khác SPICE không nổi trội, và kết luận giới hạn ở AndroidControl, câu ngắn, một câu chuẩn.

Nếu chỉ một hạt: thêm "một hạt giống, hai hạt ck500 chênh 0,72, chờ xác nhận"; không dùng từ "đứng đầu" nếu Δ < 1.

**Trường hợp 2a: có độ đo khác hơn SPICE rõ.**

> Thưởng [X] đạt exec [ ], hơn SPICE [ ], KTC [ ]; đúng với dự đoán em ghi trước (tín hiệu bước đầu). Do đó SPICE không phải lựa chọn tốt nhất. ck500 vẫn cho thấy RL có tín hiệu thật, nhưng đề xuất đổi phương pháp chính sang [X] nếu lặp lại ở hạt thứ hai; khảo sát cho biết lý do của [X] là [ ]. Em đề nghị thầy cho quyết định sau hạt thứ hai và phép đo bước không chạm.

**Trường hợp 2b: các độ đo hàng đầu ngang nhau, kết cục có khả năng nhất [suy].**

> Các thưởng [ ] nằm trong cùng dải, chênh không vượt nhiễu hạt giống, ghép ngẫu nhiên thì không tăng. Em kết luận yếu tố quan trọng là có phần thưởng so với câu chuẩn; việc chọn độ đo trong nhóm này ảnh hưởng ít hơn. Em giữ SPICE vì [lý do thực dụng] và khai rõ không chứng minh được nó tốt hơn. Câu này khớp mẫu hình tài liệu: DMO có chênh dưới 1 điểm giữa các độ đo, và chênh giữa RL với CE lớn hơn nhiều chênh giữa các thưởng ở Rennie, CST.

Không viết trong mọi trường hợp: "SPICE được chọn vì Zhao khuyên", "SPICE so được quan hệ giữa các phần tử", "SPICE tốt nhất" với một hạt, số val.

## 10. Những câu trong tài liệu khác cần sửa (tôi không tự sửa)

| tài liệu | câu | sửa thành |
|---|---|---|
| `323` §3 | "Zhao… khuyên dùng SPICE" làm lý do bảo vệ | chỉ ở mức hệ thống; mức câu bài nói ngược lại |
| `323` §3 | SPICE so "đối tượng + thuộc tính + quan hệ" trên câu hướng dẫn | quan hệ TB 0,50 tuple/câu [đo] |
| `323` §3 | CIDEr-D "dễ thưởng chép cụm hiếm hơn là gọi đúng phần tử" | kiểm đặc tính cho thấy ngược lại; bỏ hoặc đổi thành giả thuyết |
| `323` §3 | CLIP "loại bằng lý do, không cần chạy" | có số [đo] ở mục 5 |
| `report/reports/Baseline RL so với GRPO.md` dòng 34, `caption_textgen_rl.md` | "SPICE đứng một mình không có hàng số nào" | có hàng số ở RL4LMs Bảng 12 |
| `caption_textgen_rl.md`, báo cáo khảo sát | Rennie "không vượt CIDEr khi train nhiều độ đo" | chưa tìm thấy câu đó trong PDF khi kiểm lại |
| Luận văn ch2/ch4 nếu có lý do "theo Zhao" | như dòng đầu | sửa khi tới lượt sửa luận văn |

Chưa làm rõ: Dessì 2022, Luo 2017 chỉ dẫn lại từ `report/141`; Dou & Peng 2022 (follower gradient làm thưởng) chỉ thấy qua dẫn trong SAS; Chen ICLR 2020 chưa kiểm bằng OpenReview.

## Phụ lục A. Danh sách bài và nhãn

Cột "kiểm": A = mở được trang ACL Anthology; C = Crossref có bản ghi; K = theo ghi chú arXiv; "-" = preprint hoặc chưa kiểm. Nhãn thưởng: CIDEr · BLEU · ROUGE · METEOR · SPICE · SPIDEr · BCMR · chrF · TER_WER · EMB (embedding) · CLIP · GRAPH (tập thực thể, đồ thị) · ENTAIL · QA · EXEC · LISTENER · DISC (bộ phân biệt GAN) · LEARNEDIRL · HUMAN · LLMJ · RULE.

**Chú thích ảnh (51 bài)**

| mã | bài | venue | kiểm | nhãn thưởng | tầng |
|---|---|---|:-:|---|:-:|
| 1612.00563 | Self-critical Sequence Training for Image Captioning | 2017 IEEE Conference on Computer Vision and Pattern Recogn, 2017 | C | CIDEr BLEU ROUGE METEOR | A |
| 1612.00370 | Improved Image Captioning via Policy Gradient optimization of SPIDEr | 2017 IEEE International Conference on Computer Vision, 2017 | C | BLEU CIDEr BCMR SPIDEr SPICE | A |
| 1704.03899 | Deep Reinforcement Learning-based Image Captioning with Embedding Rewa | 2017 IEEE Conference on Computer Vision and Pattern Recogn, 2017 | C | EMB | A |
| 1706.09601 | Actor-Critic Sequence Training for Image Captioning | preprint hoặc chưa kiểm | - | CIDEr | A |
| 1707.07998 | Bottom-Up and Top-Down Attention for Image Captioning and Visual Quest | 2018 IEEE/CVF Conference on Computer Vision and Pattern Re, 2018 | C | CIDEr | A |
| 1803.04376 | Discriminability objective for training descriptive captions | 2018 IEEE/CVF Conference on Computer Vision and Pattern Re, 2018 | C | CIDEr LISTENER | A |
| 1803.08314 | Show, Tell and Discriminate: Image Captioning by Self-retrieval with P | Lecture Notes in Computer Science, 2018 | C | CIDEr LISTENER | A |
| 1809.06227 | Improving Reinforcement Learning Based Image Captioning with Natural L | ACL Anthology d18-1083 | A | CIDEr | A |
| 1805.07112 | Improving Image Captioning with Conditional Generative Adversarial Net | Proceedings of the AAAI Conference on Artificial Intellige, 2019 | C | CIDEr BLEU ROUGE METEOR DISC | A |
| 1904.06861 | Self-critical n-step Training for Image Captioning | 2019 IEEE/CVF Conference on Computer Vision and Pattern Re, 2019 | C | CIDEr | A |
| 1908.06954 | Attention on Attention for Image Captioning | 2019 IEEE/CVF International Conference on Computer Vision, 2019 | C | CIDEr | A |
| 1912.08226 | Meshed-Memory Transformer for Image Captioning | 2020 IEEE/CVF Conference on Computer Vision and Pattern Re, 2020 | C | CIDEr | A |
| 2003.14080 | X-Linear Attention Networks for Image Captioning | 2020 IEEE/CVF Conference on Computer Vision and Pattern Re, 2020 | C | CIDEr | A |
| 1911.09753 | Reinforcing an Image Caption Generator Using Off-Line Human Feedback | Proceedings of the AAAI Conference on Artificial Intellige, 2020 | C | HUMAN | A |
| 2003.09971 | A Better Variant of Self-Critical Sequence Training | preprint hoặc chưa kiểm | - | CIDEr | A |
| 2004.02435 | B-SCST: Bayesian Self-Critical Sequence Training for Image Captioning | preprint hoặc chưa kiểm | - | CIDEr | A |
| 2205.13115 | Fine-grained Image Captioning with CLIP Reward | ACL Anthology 2022.findings-naacl.39 | A | CIDEr CLIP | A |
| 2208.04254 | Distinctive Image Captioning via CLIP Guided Group Optimization | Lecture Notes in Computer Science, 2023 | C | CIDEr CLIP | A |
| acl_dmo | Direct Metric Optimization for Image Captioning through Reward-Weighte | ACL Anthology 2024.acl-long.453 | A | CIDEr BLEU METEOR ROUGE | A |
| 2408.16827 | Fluent and Accurate Image Captioning with a Self-Trained Reward Model | Lecture Notes in Computer Science, 2024 | C | CIDEr CLIP DISC | A |
| 2408.14547 | Revisiting Image Captioning Training Paradigm via Direct CLIP-based Op | BMVC 2024 | K | CLIP | A |
| 2503.01333 | Group Relative Policy Optimization for Image Captioning | preprint hoặc chưa kiểm | - | CIDEr | A |
| 2508.06125 | SC-Captioner: Improving Image Captioning with Self-Correction by Reinf | 2025 IEEE/CVF International Conference on Computer Vision, 2025 | C | GRAPH | A |
| 2509.22647 | CapRL: Stimulating Dense Image Caption Capabilities via Reinforcement  | preprint hoặc chưa kiểm | - | QA LLMJ | A |
| 2602.21655 | CCCaption: Dual-Reward Reinforcement Learning for Complete and Correct | CVPR 2026 | K | LLMJ | A |
| 2003.10925 | Learning Compact Reward for Image Captioning | preprint hoặc chưa kiểm | - | CIDEr LEARNEDIRL | A |
| 1709.03376 | Stack-Captioning: Coarse-to-Fine Learning for Image Captioning | Proceedings of the AAAI Conference on Artificial Intellige, 2018 | C | CIDEr | A |
| 1808.05864 | Context-Aware Visual Policy Network for Sequence-Level Image Captionin | Proceedings of the 26th ACM international conference on Mu, 2018 | C | CIDEr | A |
| 1906.05963 | Image Captioning: Transforming Objects into Words | preprint hoặc chưa kiểm | - | CIDEr | A |
| iccv_entangled | Entangled Transformer for Image Captioning | 2019 IEEE/CVF International Conference on Computer Vision, 2019 | C | CIDEr | A |
| 1511.06732 | Sequence Level Training with Recurrent Neural Networks | preprint hoặc chưa kiểm | - | BLEU ROUGE | A |
| 2606.00440 | SDR: Set-Distance Rewards for Radiology Report Generation | preprint hoặc chưa kiểm | - | EMB | B |
| 2010.10042 | Improving Factual Completeness and Consistency of Image-to-Text Radiol | ACL Anthology 2021.naacl-main.416 | A | CIDEr EMB GRAPH ENTAIL | B |
| 2408.03500 | e-Health CSIRO at RRG24: Entropy-Augmented Self-Critical Sequence Trai | ACL Anthology 2024.bionlp-1.8 | A | GRAPH | B |
| 2109.13701 | CIDEr-R: Robust Consensus-based Image Description Evaluation | ACL Anthology 2021.wnut-1.39 | A | CIDEr | B |
| 2305.12254 | A request for clarity over the End of Sequence token in the Self-Criti | Lecture Notes in Computer Science, 2023 | C | CIDEr | B |
| 1903.12020 | Describing like humans: on diversity in image captioning | 2019 IEEE/CVF Conference on Computer Vision and Pattern Re, 2019 | C | CIDEr LISTENER | B |
| 2007.06877 | Compare and Reweight: Distinctive Image Captioning Using Similar Image | Lecture Notes in Computer Science, 2020 | C | CIDEr | B |
| 2606.28845 | Personalizing MLLMs via Reinforced Multimodal Reference Game | Lecture Notes in Computer Science, 2026 | C | LISTENER LLMJ | B |
| 2507.08610 | Emergent Natural Language with Communication Games for Improving Image | preprint hoặc chưa kiểm | - | LISTENER | B |
| 1703.06029 | Towards Diverse and Natural Image Descriptions via a Conditional GAN | 2017 IEEE International Conference on Computer Vision, 2017 | C | DISC | B |
| 1705.00930 | Show, Adapt and Tell: Adversarial Training of Cross-domain Image Capti | 2017 IEEE International Conference on Computer Vision, 2017 | C | DISC | B |
| 1706.00130 | Teaching Machines to Describe Images via Natural Language Feedback | preprint hoặc chưa kiểm | - | BLEU | B |
| 2210.12186 | Improving the Factual Correctness of Radiology Report Generation with  | ACL Anthology 2022.findings-emnlp.319 | A | GRAPH EMB | B |
| 2605.07394 | BalCapRL: A Balanced Framework for RL-Based MLLM Image Captioning | preprint hoặc chưa kiểm | - | LLMJ | B |
| 2610.14976 | Metric-Driven Reinforcement Learning for Object Hallucination Reductio | IEEE Access, 2026 | C | METEOR EMB GRAPH | B |
| 2609.00709 | Controllable Image Captioning with Prompt-Conditioned Scene Rewards | Proceedings of the 2026 Conference on Empirical Methods in, 2026 | C | GRAPH LLMJ CLIP | B |
| 2608.21305 | Re$^3$Cap: Retrieval-Guided Refinement for Image Captioning Enhancemen | EMNLP 2026 Main Conference | K | LISTENER | B |
| 2606.09871 | SD-GRPO: Verifiable Segment Decomposition for Long-Form Vision-Languag | preprint hoặc chưa kiểm | - | ROUGE EMB | B |
| 2610.31111 | Where Do Long Captions Fail? Position-Aware Diagnosis and Reinforcemen | NeurIPS 2026 | K | LLMJ | B |
| 1812.02378 | Auto-Encoding Scene Graphs for Image Captioning | 2019 IEEE/CVF Conference on Computer Vision and Pattern Re, 2019 | C | (không dùng độ đo làm thưởng) | A |

**Video, kể chuyện (15 bài)**

| mã | bài | venue | kiểm | nhãn thưởng | tầng |
|---|---|---|:-:|---|:-:|
| 1708.02300 | Reinforced Video Captioning with Entailment Rewards | ACL Anthology d17-1103 | A | CIDEr ENTAIL BLEU SPICE | A |
| 1711.11135 | Video Captioning via Hierarchical Reinforcement Learning | 2018 IEEE/CVF Conference on Computer Vision and Pattern Re, 2018 | C | CIDEr | A |
| 1804.09160 | No Metrics Are Perfect: Adversarial Reward Learning for Visual Storyte | ACL Anthology p18-1083 | A | BLEU METEOR ROUGE CIDEr LEARNEDIRL | A |
| 1803.01457 | Less Is More: Picking Informative Frames for Video Captioning | Lecture Notes in Computer Science, 2018 | C | CIDEr | A |
| 1805.08191 | Hierarchically Structured Reinforcement Learning for Topically Coheren | Proceedings of the AAAI Conference on Artificial Intellige, 2019 | C | CIDEr | A |
| 2510.10395 | AVoCaDO: An Audiovisual Video Captioner Driven by Temporal Orchestrati | preprint hoặc chưa kiểm | - | GRAPH LLMJ | B |
| 2212.10690 | METEOR Guided Divergence for Video Captioning | 2023 International Joint Conference on Neural Networks, 2023 | C | METEOR | B |
| 1909.05316 | What Makes A Good Story? Designing Composite Rewards for Visual Storyt | Proceedings of the AAAI Conference on Artificial Intellige, 2020 | C | LEARNEDIRL | B |
| 1906.01452 | Reconstruct and Represent Video Contents for Captioning via Reinforcem | IEEE Transactions on Pattern Analysis and Machine Intellig, 2020 | C | CIDEr | B |
| 1803.07950 | End-to-End Video Captioning with Multitask Reinforcement Learning | 2019 IEEE Winter Conference on Applications of Computer Vi, 2019 | C | CIDEr | B |
| 1712.09532 | Consensus-based Sequence Training for Video Captioning | preprint hoặc chưa kiểm | - | BLEU METEOR ROUGE CIDEr | B |
| 2608.06930 | AVCap: Reinforcing Audio-Video Joint Caption with Detail-Aware Reward | preprint hoặc chưa kiểm | - | BLEU LLMJ | B |
| 2506.01725 | VideoCap-R1: Enhancing MLLMs for Video Captioning via Structured Think | preprint hoặc chưa kiểm | - | GRAPH | B |
| 2508.18634 | OwlCap: Harmonizing Motion-Detail for Video Captioning via HMD-270K an | Proceedings of the AAAI Conference on Artificial Intellige, 2026 | C | GRAPH | B |
| 1803.11438 | Reconstruction Network for Video Captioning | 2018 IEEE/CVF Conference on Computer Vision and Pattern Re, 2018 | C | (không dùng độ đo làm thưởng) | A |

**Biểu thức tham chiếu (6 bài)**

| mã | bài | venue | kiểm | nhãn thưởng | tầng |
|---|---|---|:-:|---|:-:|
| 1612.09542 | A Joint Speaker-Listener-Reinforcer Model for Referring Expressions | 2017 IEEE Conference on Computer Vision and Pattern Recogn, 2017 | C | LISTENER | A |
| 1511.02283 | Generation and Comprehension of Unambiguous Object Descriptions | 2016 IEEE Conference on Computer Vision and Pattern Recogn, 2016 | C | (không dùng độ đo làm thưởng) | A |
| 1701.03439 | Comprehension-guided referring expressions | 2017 IEEE Conference on Computer Vision and Pattern Recogn, 2017 | C | (không dùng độ đo làm thưởng) | A |
| 1701.02870 | Context-aware Captions from Context-agnostic Supervision | 2017 IEEE Conference on Computer Vision and Pattern Recogn, 2017 | C | (không dùng độ đo làm thưởng) | A |
| 1804.05417 | Pragmatically Informative Image Captioning with Character-Level Infere | ACL Anthology n18-2070 | A | (không dùng độ đo làm thưởng) | A |
| 1604.00562 | Reasoning About Pragmatics with Neural Listeners and Speakers | ACL Anthology d16-1125 | A | (không dùng độ đo làm thưởng) | A |

**Dịch máy (21 bài)**

| mã | bài | venue | kiểm | nhãn thưởng | tầng |
|---|---|---|:-:|---|:-:|
| 1512.02433 | Minimum Risk Training for Neural Machine Translation | ACL Anthology p16-1159 | A | BLEU TER_WER | A |
| 1607.07086 | An Actor-Critic Algorithm for Sequence Prediction | preprint hoặc chưa kiểm | - | BLEU | A |
| 1606.02960 | Sequence-to-Sequence Learning as Beam-Search Optimization | ACL Anthology d16-1137 | A | BLEU | A |
| 1711.04956 | Classical Structured Prediction Losses for Sequence to Sequence Learni | ACL Anthology n18-1033 | A | BLEU ROUGE | A |
| 1707.07402 | Reinforcement Learning for Bandit Neural Machine Translation with Simu | ACL Anthology d17-1153 | A | BLEU | A |
| 1909.06694 | Beyond BLEU: Training Neural Machine Translation with Semantic Similar | ACL Anthology p19-1427 | A | BLEU EMB | A |
| 1704.06497 | Bandit Structured Prediction for Neural Sequence-to-Sequence Learning | ACL Anthology p17-1138 | A | BLEU | A |
| 1808.08866 | A Study of Reinforcement Learning for Neural Machine Translation | ACL Anthology d18-1397 | A | BLEU | A |
| 1703.04887 | Improving Neural Machine Translation with Conditional Sequence Generat | ACL Anthology n18-1122 | A | BLEU DISC | A |
| 2104.07541 | Reward Optimization for Neural Machine Translation with Learned Metric | preprint hoặc chưa kiểm | - | BLEU EMB | B |
| 1805.10627 | Reliability and Learnability of Human Bandit Feedback for Sequence-to- | ACL Anthology p18-1165 | A | BLEU HUMAN | A |
| 1704.06933 | Adversarial Neural Machine Translation | preprint hoặc chưa kiểm | - | DISC | A |
| 2102.11403 | Exploring Supervised and Unsupervised Rewards in Machine Translation | ACL Anthology 2021.eacl-main.164 | A | BLEU | B |
| 2410.10228 | QE-EBM: Using Quality Estimators as Energy Loss for Machine Translatio | preprint hoặc chưa kiểm | - | HUMAN | B |
| 2506.05070 | RIVAL: Reinforcement Learning with Iterative and Adversarial Optimizat | ACL Anthology 2025.findings-emnlp.166 | A | BLEU HUMAN | B |
| 1811.08541 | Neural Machine Translation with Adequacy-Oriented Learning | Proceedings of the AAAI Conference on Artificial Intellige, 2019 | C | BLEU chrF DISC | B |
| 2308.02223 | ESRL: Efficient Sampling-based Reinforcement Learning for Sequence Gen | Proceedings of the AAAI Conference on Artificial Intellige, 2024 | C | BLEU ROUGE HUMAN | B |
| 1907.01752 | On the Weaknesses of Reinforcement Learning for Neural Machine Transla | ICLR 2020 (matching content | K | BLEU | B |
| 2005.03642 | On Exposure Bias, Hallucination and Domain Shift in Neural Machine Tra | ACL Anthology 2020.acl-main.326 | A | BLEU | B |
| 1611.00179 | Dual Learning for Machine Translation | NIPS 2016 | K | (không dùng độ đo làm thưởng) | A |
| 1810.12081 | Learning to Teach with Dynamic Loss Functions | NIPS 2018 | K | (không dùng độ đo làm thưởng) | A |

**Tóm tắt (25 bài)**

| mã | bài | venue | kiểm | nhãn thưởng | tầng |
|---|---|---|:-:|---|:-:|
| 1705.04304 | A Deep Reinforced Model for Abstractive Summarization | preprint hoặc chưa kiểm | - | ROUGE | A |
| 1804.06451 | Multi-Reward Reinforced Summarization with Saliency and Entailment | ACL Anthology n18-2102 | A | ROUGE ENTAIL | A |
| 1803.10357 | Deep Communicating Agents for Abstractive Summarization | ACL Anthology n18-1150 | A | ROUGE | A |
| 1805.11080 | Fast Abstractive Summarization with Reinforce-Selected Sentence Rewrit | ACL Anthology p18-1063 | A | ROUGE | A |
| 2009.01325 | Learning to summarize from human feedback | NeurIPS 2020 | K | ROUGE HUMAN | A |
| 1909.01214 | Better Rewards Yield Better Summaries: Learning to Summarise Without R | ACL Anthology d19-1307 | A | ROUGE HUMAN | A |
| 1909.00141 | Deep Reinforcement Learning with Distributional Semantic Rewards for A | ACL Anthology d19-1623 | A | ROUGE EMB | A |
| 1909.01610 | Answers Unite! Unsupervised Metrics for Reinforced Summarization Model | ACL Anthology d19-1320 | A | ROUGE QA | A |
| 1809.09672 | BanditSum: Extractive Summarization as a Contextual Bandit | ACL Anthology d18-1409 | A | ROUGE | A |
| 1802.08636 | Ranking Sentences for Extractive Summarization with Reinforcement Lear | ACL Anthology n18-1158 | A | ROUGE | A |
| 1904.02321 | Guiding Extractive Summarization with Question-Answering Rewards | ACL Anthology n19-1264 | A | QA | A |
| 1805.10392 | Reinforced Extractive Summarization with Question-Focused Rewards | ACL Anthology p18-3015 | A | QA | A |
| 1809.04585 | Closed-Book Training to Improve Summarization Encoder Memory | ACL Anthology d18-1440 | A | ROUGE | A |
| 1808.07913 | Improving Abstraction in Text Summarization | ACL Anthology d18-1207 | A | ROUGE | A |
| 1804.07036 | Learning to Extract Coherent Summary via Deep Reinforcement Learning | Proceedings of the AAAI Conference on Artificial Intellige, 2018 | C | ROUGE | A |
| 1907.12894 | Reward Learning for Efficient Reinforcement Learning in Extractive Doc | Proceedings of the Twenty-Eighth International Joint Confe, 2019 | C | ROUGE LEARNEDIRL | A |
| 2010.00117 | Multi-document Summarization with Maximal Marginal Relevance-guided Re | ACL Anthology 2020.emnlp-main.136 | A | ROUGE | A |
| 2203.02894 | A Multi-Document Coverage Reward for RELAXed Multi-Document Summarizat | ACL Anthology 2022.acl-long.351 | A | ROUGE | B |
| 2212.09917 | Inverse Reinforcement Learning for Text Summarization | ACL Anthology 2023.findings-emnlp.436 | A | ROUGE LEARNEDIRL | B |
| 2311.17514 | Reinforcement Replaces Supervision: Query focused Summarization using  | ACL Anthology 2023.emnlp-main.977 | A | ROUGE BLEU EMB | B |
| 1805.03616 | A Reinforced Topic-Aware Convolutional Sequence-to-Sequence Model for  | Proceedings of the Twenty-Seventh International Joint Conf, 2018 | C | ROUGE | B |
| 1912.05493 | Quality of syntactic implication of RL-based sentence summarization | Communications in Computer and Information Science, 2020 | C | ROUGE | B |
| 1902.07110 | A novel repetition normalized adversarial reward for headline generati | ICASSP 2019 - 2019 IEEE International Conference on Acoust, 2019 | C | ROUGE DISC | B |
| 2002.07767 | Learning by Semantic Similarity Makes Abstractive Summarization Better | preprint hoặc chưa kiểm | - | (không dùng độ đo làm thưởng) | A |
| 2105.05361 | The Summary Loop: Learning to Write Abstractive Summaries Without Exam | ACL Anthology 2020.acl-main.460 | A | (không dùng độ đo làm thưởng) | A |

**Sinh văn bản khác (28 bài)**

| mã | bài | venue | kiểm | nhãn thưởng | tầng |
|---|---|---|:-:|---|:-:|
| 1908.04942 | Reinforcement Learning Based Graph-to-Sequence Model for Natural Quest | ICLR 2020 | K | BLEU EMB | A |
| 1711.00279 | Paraphrase Generation with Deep Reinforcement Learning | ACL Anthology d18-1421 | A | LEARNEDIRL | A |
| 1606.01541 | Deep Reinforcement Learning for Dialogue Generation | preprint hoặc chưa kiểm | - | RULE | A |
| 1701.06547 | Adversarial Learning for Neural Dialogue Generation | ACL Anthology d17-1230 | A | DISC | A |
| 1609.05473 | SeqGAN: Sequence Generative Adversarial Nets with Policy Gradient | Proceedings of the AAAI Conference on Artificial Intellige, 2017 | C | DISC | A |
| 2210.01241 | Is Reinforcement Learning (Not) for Natural Language Processing: Bench | ICLR 2023 | K | CIDEr ROUGE METEOR SPICE SPIDEr HUMAN | A |
| 2205.13636 | Quark: Controllable Text Generation with Reinforced Unlearning | Advances in Neural Information Processing Systems 35, 2022 | C | RULE | A |
| 1811.07234 | Improving Automatic Source Code Summarization via Deep Reinforcement L | Proceedings of the 33rd ACM/IEEE International Conference , 2018 | C | BLEU | A |
| 1801.07736 | MaskGAN: Better Text Generation via Filling in the______ | ICLR 2018 | K | DISC | A |
| 1804.11258 | Toward Diverse Text Generation with Inverse Reinforcement Learning | Proceedings of the Twenty-Seventh International Joint Conf, 2018 | C | LEARNEDIRL | A |
| 2506.15068 | Semantically-Aware Rewards for Open-Ended R1 Training in Free-Form Gen | preprint hoặc chưa kiểm | - | ROUGE EMB HUMAN | B |
| 2605.25988 | What Makes a Medical Checker Trainable? Diagnosing Signal Collapse and | preprint hoặc chưa kiểm | - | ENTAIL | B |
| 2604.17188 | Beyond Overlap Metrics: Rewarding Reasoning and Preferences for Faithf | ACL Anthology 2026.findings-acl.1161 | A | ROUGE EMB | B |
| 2011.07635 | DORB: Dynamically Optimizing Multiple Rewards with Bandits | ACL Anthology 2020.emnlp-main.625 | A | BLEU ROUGE ENTAIL QA | B |
| 2108.12472 | ReGen: Reinforcement Learning for Text and Knowledge Base Generation u | ACL Anthology 2021.emnlp-main.83 | A | METEOR BLEU | B |
| 2204.06260 | Self-critical Sequence Training for Automatic Speech Recognition | ICASSP 2022 - 2022 IEEE International Conference on Acoust, 2022 | C | TER_WER | B |
| 2004.02143 | Reinforced Multi-task Approach for Multi-hop Question Generation | ACL Anthology 2020.coling-main.249 | A | ROUGE BLEU QA | B |
| 2602.16154 | Balancing Faithfulness and Performance in Reasoning via Multi-Listener | Findings of the Association for Computational Linguistics:, 2026 | C | LISTENER | B |
| 2301.12729 | Response-act Guided Reinforced Dialogue Generation for Mental Health C | Proceedings of the ACM Web Conference 2023, 2023 | C | ROUGE EMB | B |
| 1709.08624 | Long Text Generation via Adversarial Training with Leaked Information | Proceedings of the AAAI Conference on Artificial Intellige, 2018 | C | DISC | B |
| 1709.09346 | Cold-Start Reinforcement Learning with Softmax Policy Gradient | preprint hoặc chưa kiểm | - | ROUGE CIDEr | B |
| 1907.12667 | Reinforced Dynamic Reasoning for Conversational Question Generation | ACL Anthology p19-1203 | A | QA | B |
| 2011.01102 | Exploring Question-Specific Rewards for Generating Deep Questions | ACL Anthology 2020.coling-main.228 | A | QA DISC | B |
| 1705.07830 | Ask the Right Questions: Active Question Reformulation with Reinforcem | ICLR) | K | QA | B |
| 2102.02810 | Controlling Hallucinations at Word Level in Data-to-Text Generation | Data Mining and Knowledge Discovery, 2021 | C | (không dùng độ đo làm thưởng) | A |
| 2206.11871 | Offline RL for Natural Language Generation with Implicit Language Q Le | preprint hoặc chưa kiểm | - | (không dùng độ đo làm thưởng) | A |
| 1805.06087 | Learning to Write with Cooperative Discriminators | ACL Anthology p18-1152 | A | (không dùng độ đo làm thưởng) | A |
| 2005.00969 | Towards Faithful Neural Table-to-Text Generation with Content-Matching | ACL Anthology 2020.acl-main.101 | A | (không dùng độ đo làm thưởng) | A |

**Text-to-SQL, chương trình (16 bài)**

| mã | bài | venue | kiểm | nhãn thưởng | tầng |
|---|---|---|:-:|---|:-:|
| 1709.00103 | Seq2SQL: Generating Structured Queries from Natural Language using Rei | preprint hoặc chưa kiểm | - | EXEC | A |
| 1611.00020 | Neural Symbolic Machines: Learning Semantic Parsers on Freebase with W | ACL Anthology p17-1003 | A | EXEC | A |
| 1807.02322 | Memory Augmented Policy Optimization for Program Synthesis and Semanti | NeurIPS 2018 | K | EXEC | A |
| 1805.04276 | Leveraging Grammar and Reinforcement Learning for Neural Program Synth | ICLR 2018 | K | EXEC | A |
| 2505.04671 | Reward-SQL: Boosting Text-to-SQL via Stepwise Execution-Aware Reasonin | Proceedings of the ACM on Management of Data, 2026 | C | EXEC | A |
| 2504.08600 | SQL-R1: Training Natural Language to SQL Reasoning Model By Reinforcem | Advances in Neural Information Processing Systems 38, 2025 | C | EXEC | A |
| 2504.15077 | Think2SQL: Reinforce LLM Reasoning Capabilities for Text2SQL | preprint hoặc chưa kiểm | - | EXEC | A |
| 2505.20315 | Arctic-Text2SQL-R1: Simple Rewards, Strong Reasoning in Text-to-SQL | ACL Anthology 2026.findings-acl.1345 | A | EXEC | A |
| 2207.01780 | CodeRL: Mastering Code Generation through Pretrained Models and Deep R | Advances in Neural Information Processing Systems 35, 2022 | C | EXEC | A |
| 2606.06825 | Progress-SQL: Improving Reinforcement Learning for Text-to-SQL via Pro | Findings of the Association for Computational Linguistics:, 2026 | C | EXEC | B |
| 2511.22258 | Beyond Query-Level Comparison: Fine-Grained Reinforcement Learning for | preprint hoặc chưa kiểm | - | EXEC LLMJ | B |
| 2606.23693 | EXPO-SQL: Execution-based Clause-level Policy Optimization for Text-to | ACL Anthology 2026.findings-acl.1107 | A | EXEC | B |
| 2509.07159 | PaVeRL-SQL: Text-to-SQL via Partial-Match Rewards and Verbal Reinforce | 2025 IEEE International Conference on Big Data, 2025 | C | EXEC | B |
| 2505.12380 | Graph-Reward-SQL: Execution-Free Reinforcement Learning for Text-to-SQ | ACL Anthology 2025.findings-emnlp.694 | A | GRAPH EXEC | B |
| 2505.00016 | Sparks of Tabular Reasoning via Text2SQL Reinforcement Learning | ACL Anthology 2025.trl-1.20 | A | EXEC | B |
| 1711.04436 | SQLNet: Generating Structured Queries From Natural Language Without Re | ICLR 2018 | K | (không dùng độ đo làm thưởng) | A |

**Chỉ dẫn điều hướng (8 bài)**

| mã | bài | venue | kiểm | nhãn thưởng | tầng |
|---|---|---|:-:|---|:-:|
| 2409.05583 | Spatially-Aware Speaker for Vision-and-Language Navigation Instruction | ACL Anthology 2024.acl-long.734 | A | LEARNEDIRL | B |
| 1806.02724 | Speaker-Follower Models for Vision-and-Language Navigation | NIPS 2018 | K | (không dùng độ đo làm thưởng) | A |
| 2203.16586 | Counterfactual Cycle-Consistent Learning for Instruction Following and | 2022 IEEE/CVF Conference on Computer Vision and Pattern Re, 2022 | C | (không dùng độ đo làm thưởng) | A |
| 2101.10504 | On the Evaluation of Vision-and-Language Navigation Instructions | ACL Anthology 2021.eacl-main.111 | A | (không dùng độ đo làm thưởng) | A |
| 2111.12872 | Less is More: Generating Grounded Navigation Instructions from Landmar | 2022 IEEE/CVF Conference on Computer Vision and Pattern Re, 2022 | C | (không dùng độ đo làm thưởng) | A |
| 1904.04195 | Learning to Navigate Unseen Environments: Back Translation with Enviro | ACL Anthology n19-1268 | A | (không dùng độ đo làm thưởng) | A |
| 1711.04987 | Unified Pragmatic Models for Generating and Following Instructions | ACL Anthology n18-1177 | A | (không dùng độ đo làm thưởng) | A |
| 2303.08409 | Lana: A Language-Capable Navigator for Instruction Following and Gener | 2023 IEEE/CVF Conference on Computer Vision and Pattern Re, 2023 | C | (không dùng độ đo làm thưởng) | A |

**RLHF, LLM giám khảo (9 bài)**

| mã | bài | venue | kiểm | nhãn thưởng | tầng |
|---|---|---|:-:|---|:-:|
| 1909.08593 | Fine-Tuning Language Models from Human Preferences | preprint hoặc chưa kiểm | - | HUMAN | A |
| 2203.02155 | Training language models to follow instructions with human feedback | Advances in Neural Information Processing Systems 35, 2022 | C | HUMAN | A |
| 2306.01693 | Fine-Grained Human Feedback Gives Better Rewards for Language Model Tr | Advances in Neural Information Processing Systems 36, 2023 | C | HUMAN | A |
| 2212.08073 | Constitutional AI: Harmlessness from AI Feedback | preprint hoặc chưa kiểm | - | LLMJ | A |
| 2506.03106 | Critique-GRPO: Advancing LLM Reasoning with Natural Language and Numer | ICML 2026 Spotlight | K | LLMJ | A |
| 2401.10020 | Self-Rewarding Language Models | ICML 2024 | K | LLMJ | A |
| 2309.00267 | RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback wit | ICML 2024 Proceedings of the 41st | K | LLMJ HUMAN | A |
| 2504.09895 | Learning from Reference Answers: Versatile Language Model Alignment wi | preprint hoặc chưa kiểm | - | EMB METEOR | B |
| 2605.08061 | Rubric-Grounded RL: Structured Judge Rewards for Generalizable Reasoni | preprint hoặc chưa kiểm | - | LLMJ | B |

**GUI (7 bài)**

| mã | bài | venue | kiểm | nhãn thưởng | tầng |
|---|---|---|:-:|---|:-:|
| 2503.21620 | UI-R1: Enhancing Efficient Action Prediction of GUI Agents by Reinforc | Proceedings of the AAAI Conference on Artificial Intellige, 2026 | C | RULE | A |
| 2505.12370 | Enhancing Visual Grounding for GUI Agents via Self-Evolutionary Reinfo | preprint hoặc chưa kiểm | - | RULE | A |
| 2508.10833 | UI-Venus Technical Report: Building High-performance UI Agents with RF | preprint hoặc chưa kiểm | - | RULE EXEC | A |
| 2505.23762 | ZeroGUI: Automating Online GUI Learning at Zero Human Cost | preprint hoặc chưa kiểm | - | EXEC | A |
| 2509.21552 | Learning GUI Grounding with Spatial Reasoning from Visual Feedback | ICML 2026 | K | RULE | B |
| 2010.04295 | Widget Captioning: Generating Natural Language Description for Mobile  | ACL Anthology 2020.emnlp-main.443 | A | (không dùng độ đo làm thưởng) | A |
| 2108.03353 | Screen2Words: Automatic Mobile UI Summarization with Multimodal Learni | The 34th Annual ACM Symposium on User Interface Software a, 2021 | C | (không dùng độ đo làm thưởng) | A |

**Tầng B (không dùng độ đo làm thưởng) (12 bài)**

| mã | bài | venue | kiểm | nhãn thưởng | tầng |
|---|---|---|:-:|---|:-:|
| 2307.13368 | Kefa: A Knowledge Enhanced and Fine-grained Aligned Speaker for Naviga | preprint hoặc chưa kiểm | - | (không dùng độ đo làm thưởng) | B |
| 2305.11918 | PASTS: Progress-Aware Spatio-Temporal Transformer Speaker For Vision-a | Engineering Applications of Artificial Intelligence, 2024 | C | (không dùng độ đo làm thưởng) | B |
| 2609.00591 | A Glance Is All You Need: Single-Pass Fine-Grained Image Captioning wi | preprint hoặc chưa kiểm | - | (không dùng độ đo làm thưởng) | B |
| 2009.07839 | Text Generation by Learning from Demonstrations | ICLR 2021 | K | (không dùng độ đo làm thưởng) | B |
| 1703.10931 | Sentence Simplification with Deep Reinforcement Learning | ACL Anthology d17-1062 | A | (không dùng độ đo làm thưởng) | B |
| 2007.02244 | Unsupervised Paraphrasing via Deep Reinforcement Learning | Proceedings of the 26th ACM SIGKDD International Conferenc, 2020 | C | (không dùng độ đo làm thưởng) | B |
| 1911.11404 | Natural Language Generation Using Reinforcement Learning with External | ICMLA 2019 | K | (không dùng độ đo làm thưởng) | B |
| 1904.03870 | Streamlined Dense Video Captioning | 2019 IEEE/CVF Conference on Computer Vision and Pattern Re, 2019 | C | (không dùng độ đo làm thưởng) | B |
| 1810.06667 | Deep Transfer Reinforcement Learning for Text Summarization | Proceedings of the 2019 SIAM International Conference on D, 2019 | C | (không dùng độ đo làm thưởng) | B |
| 1803.11070 | Actor-Critic based Training Framework for Abstractive Summarization | preprint hoặc chưa kiểm | - | (không dùng độ đo làm thưởng) | B |
| 2106.04080 | RewardsOfSum: Exploring Reinforcement Learning Rewards for Summarisati | ACL Anthology 2021.spnlp-1.1 | A | (không dùng độ đo làm thưởng) | B |
| 2605.28534 | GUI-CIDER: Mid-training GUI Agents via Causal Internalization and Dens | preprint hoặc chưa kiểm | - | (không dùng độ đo làm thưởng) | B |
