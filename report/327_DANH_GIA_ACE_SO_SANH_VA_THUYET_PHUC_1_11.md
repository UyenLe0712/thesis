# 327 — Đánh giá ACE: cần so với gì, đã đủ thuyết phục chưa, áp dụng được tới đâu (1/11/2026)

> Phạm vi: chỉ đánh giá. Chưa sửa luận văn, chưa đổi mã, chưa đẩy gì lên Kaggle/Colab.
> Nhãn: **[đo]** là số tính lại hôm nay từ tệp thô, 0 GPU. **[có sẵn]** là số test lấy từ report, nêu nguồn.
> **[suy]** là suy luận. **[val]** là số val, chỉ để giải thích, không trích ra báo.
> Mọi số không có nhãn [val] là số test trên 4.463 bước chạm, bộ trỏ UGround, trừ khi ghi khác.
> KTC trong các bảng [đo] là bootstrap cụm app (1.091 cụm, B = 1.000), nên có thể lệch vài phần trăm điểm so với lượt B = 2.000 ở `report/320`.
> Kết quả thô: `/tmp/claude-1000/-mnt-d-Master-Thesis/f8c22a00-f56d-41dc-bd70-6f4951a71b5e/scratchpad/ace327/` (`a2.json`, các tệp log). Thư mục này không bền. ⚠️ Các script `a1.py`–`a5.py` của lượt này đã bị một phiên khác ghi đè vì trùng tên trong cùng scratchpad, nên **hiện chưa có script chạy lại được**. Định nghĩa từng phép đo ghi đủ trong file này; việc 2 ở §6 phải viết lại script vào `harness/` và đối chiếu với số ở đây.

---

## 1. Kết luận

**ACE đủ để báo như một phần mở rộng hẹp, nhưng chưa đủ để đứng ngang ck500 như một đóng góp phương pháp.** Đề xuất hạ vai trò: đóng góp chính là ck500, ACE là bước tái dùng câu có chọn lọc sau khi sinh.

Điều đã vững:

- **Không hại hành vi.** ACE − ck500 về exec là +0,02 [−0,21; +0,26], cứu 15, phá 14 [có sẵn, `report/304` §5.3]. Mức này giữ dưới UI-Venus, Phi-Ground, Phi-4, trên ACU và AitZ (`report/320` mục 4, 6, 8).
- **Cổng chọn có tác dụng thật.** Cùng số câu nhưng chọn ngẫu nhiên từ `ra_k4` chỉ cho CIDEr-D khoảng +1,68, so với +11,97 của ACE [đo, §3.3].
- **Lặp lại trên tác vụ mới.** Luật đã khoá trước khi có ACU, và trên ACU các KTC độ đo văn bản đều loại 0, ví dụ CIDEr-D +13,00 [+7,88; +19,07] [có sẵn, `report/320` mục 8].

Điều còn yếu:

1. **Toàn bộ mức tăng độ đo văn bản đến từ việc câu trở thành đúng nguyên văn câu chuẩn.** 113 bước (2,5% tập kiểm) chuyển từ sai sang trùng câu chuẩn chiếm 117% mức tăng CIDEr-D. Bỏ 113 bước đó thì mức tăng về quanh 0 ở cả năm độ đo [đo, §3.1].
2. **ACE không tăng exec, không sửa được loại thao tác.** Số bước `action_ok` đúng bằng ck500 (4.283) [đo]. Câu "tác hại ở bước không chạm là lý do có ACE" ở `report/320` là sai về cơ chế.
3. **"Chọn trên val rồi áp test một lần" chỉ đúng một nửa.** Họ luật được viết sau khi đã thấy exec test của R0 [đo mốc giờ tệp, §3.2].
4. **Chưa có mốc ablation quan trọng nhất:** luật R3 áp lên nhánh `cont` (không có khối ví dụ). Chưa biết khối ví dụ giúp mô hình sinh hay chỉ đóng vai bộ lọc.
5. **Chưa đo:** bước không chạm, lịch sử tự sinh, hạt thứ hai của `ra_k4`, và exec của các mốc chép thẳng. Chưa có bằng chứng nào từ người đọc rằng câu tốt hơn.

Một kết quả mới có lợi cho ACE: mốc chép thẳng mà `report/323` lo ngại **thua rất xa về độ đo văn bản** (CIDEr-D −168 với NN-1) [đo]. Vậy đòn "chỉ cần lấy thẳng câu ví dụ" đã có câu trả lời về văn bản, còn exec phải chạy thêm khoảng 2 giờ T4.

---

## 2. Bảng phương pháp cần so

### 2.1 Đã có số (không cần chạy thêm)

| họ | phương pháp | tiền lệ gần nhất | Δ so ck500 (exec) | Δ CIDEr-D | cho phép viết |
|---|---|---|---:|---:|---|
| truy hồi trong câu nhắc | `ra_k4` dùng mọi bước | SmallCap, EXTRA | **−1,25** [−2,06; −0,44] | +7,50 | sinh có truy hồi tăng văn bản nhưng giảm định vị [có sẵn] |
| cơ chế chép học được | CW-RA, thẻ `[COPY i]`/`[WRITE]` | CopyNet, pointer-generator | **−2,13** [−2,94; −1,31] | −23 (thua 7/7) | để mô hình tự quyết chép là không đạt; hỏng ở nhánh viết [có sẵn, `report/310`] |
| RL có truy hồi | RA-GRPO | không thấy tiền lệ trong mẫu đã tra | không có số test | dừng ở G0 | không có điều kiện để train; không được viết "thua" [`report/312`, val] |
| sửa câu | TAGE (sửa theo vùng ảnh) | retrieve-and-edit, nhưng không truy hồi | −0,43 [−0,87; +0,02] | không so trực tiếp | sửa theo vùng cắt không giúp [có sẵn] |
| chọn giữa hai mô hình | RAF (S1 hoặc ck500) | hybrid retrieval/generation | −0,13…−0,38 (5 cột hành vi, KTC phủ 0) | +5,61 [+1,46; +9,61] | thua ACE về CIDEr-D, không hơn về hành vi [có sẵn, `report/298`] |
| học lại từ mẫu tốt | RAFT từ ck500 | RAFT (TMLR 2023, cần kiểm) | **−0,43** [−0,82; −0,04] | −6,97 | học thêm từ mẫu của chính ck500 không giúp [có sẵn, `report/314`] |
| chọn lại câu lúc suy luận | MBR; selector màn sau | MBR decoding | chỉ có val | | không đạt, chỉ nêu hướng đã thử [`report/208`, `report/233`] |
| bỏ cuộc | `gui_sel` + τ | selective prediction | chỉ có dev | | điểm của mô hình gần như mù ở bài toán bỏ cuộc, AUC 0,69–0,72 [`report/142`] |

### 2.2 Tính mới hôm nay, 0 GPU

| phương pháp | câu đổi | exec | CIDEr-D | BLEU-4 | SPICE | trùng câu chuẩn |
|---|---:|---:|---:|---:|---:|---:|
| ck500 (mốc) | 0 | 60,65 | 430,04 | 52,36 | 45,79 | 1.003 |
| **ACE (R3)** | 402 | **+0,02** [−0,21; +0,25] | **+11,97** [+8,93; +15,60] | +1,11 | +1,33 | 1.087 |
| R0 (chỉ cần trùng ví dụ) | 453 | −0,11 [−0,43; +0,20] | +11,49 | +1,11 | +1,32 | 1.090 |
| R2 (thêm cùng lõi) | 311 | −0,07 [−0,20; +0,04] | +8,75 | +0,79 | +1,00 | 1.075 |
| R4 (R2 ∧ R3) | 299 | 0,00 [−0,09; +0,09] | +8,42 | +0,78 | +0,98 | 1.072 |
| `ra_k4` khi cùng lớp thao tác, **không** cần trùng ví dụ | 1.972 | −0,45 [−1,15; +0,25] | +11,07 | +1,50 | +1,33 | 1.106 |
| `ra_k4` khi cùng lớp và **không** chép | 1.570 | −0,47 [−1,09; +0,17] | −0,91 [−6,37; +4,44] | +0,68 | −0,01 | 1.022 |
| `ra_k4` khi câu nằm trong kho và cùng lớp | 1.143 | −0,45 [−0,97; +0,07] | +12,26 | +1,70 | +1,24 | 1.106 |
| NN-1: ví dụ đầu, cùng lớp thao tác, **không có `ra_k4`** | 2.979 | chưa chấm | **−168,26** | −14,17 | −14,32 | 601 |
| NN-vote: ví dụ đầu có `cnt ≥ 2`, cùng lớp | 2.782 | chưa chấm | **−152,95** | −12,87 | −12,93 | 641 |
| SNAP: ví dụ gần câu ck500 nhất, Jaccard ≥ 0,7, cùng lớp | 767 | chưa chấm | −11,83 | −0,81 | −0,74 | 953 |
| đồng thuận 2/3 (S1, ck500/202, `ra_k4`), không truy hồi | 736 | −0,40 [−0,89; +0,07] | +3,08 | +0,76 | +0,57 | 1.045 |
| đồng thuận 2/2 (S1, ck500/202) | 210 | −0,04 [−0,29; +0,18] | +1,96 | +0,42 | +0,20 | 1.017 |
| đồng thuận 3/5 (thêm S1/202, nhánh ghép ngẫu nhiên) | 866 | **−0,65** [−1,24; −0,12] | −0,63 | +0,35 | −0,01 | 1.023 |
| cận trên: biết trước khối có câu chuẩn thì chép đúng | 529 | chưa chấm đủ | +65,37 | +5,05 | +6,16 | 1.441 |

Ghi chú khi đọc:

- SNAP: **không τ nào vượt ck500 trên cả bốn độ đo val** [val], nên phương pháp này không qua vòng chọn. Hàng trên chỉ để mô tả, τ = 0,7 không được chọn.
- Các hàng đồng thuận và các biến thể `ra_k4` là mô tả trên test, không được chọn trên val, nên không dùng làm phương pháp thay thế.
- Đọc chung [suy]: văn bản tăng không cần điều kiện chép, nhưng điều kiện chép là thứ giữ exec không giảm. ACE lấy gần trọn mức tăng CIDEr-D với số câu đổi ít hơn năm lần.
- ACE đứng đầu nhóm so với mọi phương án đã đo về cân bằng giữa văn bản và exec. Đây là so sánh trong mẫu các phương án đã thử, không phải chứng minh ACE là tối ưu.

### 2.3 Cần chạy, xếp theo ưu tiên

Không việc nào cần Colab. Tốc độ lấy từ log: sinh câu 3,08 s/bước trên một T4 (`runs/acu/gen/out/gen_ra_k4.log`), UGround 2,3 s/câu trên T4×2 (2.229 câu trong 85 phút, `report/304` §4.3). Thời gian ước lượng là [suy].

| ưu tiên | việc | trả lời | máy, thời gian | đọc thế nào |
|---|---:|---|---|---|
| 1 | Exec của NN-1, NN-vote, SNAP (hợp 2.991 câu mới) + hiệu chuẩn 40 câu | đòn "chỉ là sao chép" (Z3) | Kaggle T4×2, ~2 h | NN thua văn bản đã rõ; exec cho biết nó có giữ được định vị không |
| 2 | **`cont` + luật R3 trên test** (adapter ở `runs/ra304_T/cont_sft/`) | khối ví dụ có giúp gì không | T4×2 ~2,2 h sinh + ~1 h chấm + CPU văn bản | gần ACE: truy hồi chỉ là bộ lọc, mô hình thứ hai không cần thấy ví dụ. Thua xa: khối ví dụ có đóng góp thật |
| 3 | Bước không chạm: `ra_k4` trên 2.495 bước, áp R3 | phạm vi (việc #4 của `report/322`) | T4 ~2,1 h một GPU; chấm `noharm` 0 GPU | [suy] ACE không sửa được scroll vì buộc cùng lớp |
| 4 | Lịch sử tự sinh: `ra_k4` nhận lịch sử chuỗi ck500 đã có, truy hồi lại, áp R3 | triển khai thật | T4×2 ~2 h + chấm các câu đổi | so ACE − ck500 dưới lịch sử tự sinh (`runs/tuantu/`) |
| 5 | Hạt thứ hai của `ra_k4` (train + sinh + chấm) | một hạt giống | T4: ~7,5 h train + ~2,2 h sinh + ~1 h chấm | nền ck500 đã đổi được (§3.5), riêng `ra_k4` vẫn một hạt |
| 6 | Một mô hình + chấm hợp lý: ck500 tính log-prob của 4 ví dụ và câu của chính nó, chọn theo tổng log-prob, δ chọn trên val | bỏ mô hình thứ hai, giảm độ trễ | T4×2, viết mã từ `seq_score_sel.py`, ~5 h [suy, chưa đo] | nếu ngang ACE thì nên thay ACE vì rẻ hơn. Rủi ro: `report/142` thấy điểm mô hình không tách được bỏ cuộc |
| 7 | Truy hồi khác: bge-m3 trên văn bản, thêm OCR vào truy vấn, CLIP trên ảnh | vì sao TF-IDF | bước 1 CPU/T4: đo độ phủ câu chuẩn so 15,84%. Chỉ phủ hơn rõ mới sinh lại (~3,6 h T4) | SmallCap truy hồi **theo ảnh**, còn ACE chỉ dùng chữ |
| 8 | Bỏ cùng app khỏi kho rồi sinh lại `ra_k4` trên 1.815 bước có nhãn app | giới hạn app mới | T4 ~1,6 h, sau khi có độ phủ ở §4.3 | ACE − ck500 khi kho không có app đó |
| 9 | Chấm tay mù 100 cặp ck500/ACE, rút từ 344 câu khác nhau sau tách từ | câu có tốt hơn cho người đọc không | công của user; **user đã quyết không làm 6/9**, chỉ nêu để cân nhắc lại | đây là phép đo duy nhất phân biệt "tốt hơn" với "giống câu chuẩn hơn" |
| 10 | Retrieve-and-edit đúng nghĩa (k = 1, train editor) | tiền lệ gần nhất chưa chạy | T4 ~7,5 h + ~3,6 h | ưu tiên thấp: các lượt train thêm sau ck500 đều làm văn bản câu viết mới giảm |
| 11 | kNN-LM ở mức token | tiền lệ truy hồi lúc suy luận | T4, phải viết mới | chỉ ghi lại, chi phí mã cao so với câu hỏi trả lời được |

---

## 3. Các điểm yếu khoa học và phép đo chốt

### 3.1 Mức tăng văn bản có phải chỉ vì chép đúng câu chuẩn: **đúng**

Phân rã 402 bước đổi [đo]:

| nhóm | số bước | Δ CIDEr-D | Δ BLEU-4 | Δ SPICE | exec cứu/phá |
|---|---:|---:|---:|---:|---|
| ck500 sai → ACE trùng câu chuẩn | **113** | **+13,96** [+11,33; +16,90] | +1,01 | +1,46 | 8 / 1 |
| ck500 trùng câu chuẩn → ACE khác | 29 | −3,91 | −0,24 | −0,30 | 0 / 4 |
| chỉ khác chữ hoa, dấu câu | 58 | 0,00 | 0,00 | 0,00 | 0 / 1 |
| cả hai khác câu chuẩn, cùng lõi nội dung | 132 | +0,95 | +0,17 | +0,10 | 1 / 1 |
| cả hai khác câu chuẩn, khác lõi nội dung | 70 | +0,98 | +0,17 | +0,08 | 6 / 7 |
| **bỏ nhóm đầu, giữ 289 bước còn lại** | 289 | **−1,98** [−4,18; +0,11] | +0,10 [−0,13; +0,32] | −0,13 [−0,36; +0,11] | |

ROUGE-L và chrF cùng kiểu: nhóm đầu +0,63 và +0,61 trên tổng +0,74 và +0,58; bỏ nhóm đầu thì +0,11 và −0,03, KTC phủ 0.

Phải đọc đúng bảng này. Nhóm đầu được định nghĩa theo kết quả nên bỏ nó đi là thiên vị chống ACE, không phải "ACE không có tác dụng". Trúng câu chuẩn cũng là lợi ích thật, vì tỉ lệ trúng trong số câu đổi là 148/402 (36,8%), còn câu ck500 ở cùng các bước chỉ 64/402 (15,9%) [đo]. Cách đọc đúng: **"7/7 độ đo" là một hiện tượng đo bảy lần, không phải bảy bằng chứng độc lập.** Hiện tượng đó là số câu trùng nguyên văn tăng ròng +84 câu, từ 22,47% lên 24,36% [đo].

Phép tách không phụ thuộc kết quả của ACE, nhưng phải dùng câu chuẩn nên chỉ để giải thích [đo]:

| khối ví dụ | số bước | câu đổi | Δ CIDEr-D (trên nhóm) | exec ck500 → ACE | cứu/phá | p (chưa hiệu chỉnh) |
|---|---:|---:|---:|---|---|---:|
| có câu chuẩn | 707 | 185 | +86,99 [+68,39; +104,29] | 71,71 → 73,13 | 11 / 1 | 0,006 |
| không có câu chuẩn | 3.756 | 217 | −2,15 [−4,68; +0,16] | 58,57 → 58,33 | 4 / 13 | 0,049 |

Đây là phát hiện đáng khai nhất. **Lợi ích của ACE dồn vào lúc kho có đúng câu chuẩn; lúc kho không có thì không tăng văn bản, và exec có dấu hiệu giảm nhẹ.** Đây là phân tích nhóm hậu kiểm, một hạt, không kết luận được phần exec. Nhưng nó dự đoán đúng thứ tự trên ba tập: phủ khối 15,84% (tập kiểm) · 8,7% (ACU) · 0% (AitZ), và câu đổi 9,0% · 6,3% · 1,9%.

Hiểm họa về độ đo:

- Tất cả độ đo so với **một** câu chuẩn. Đổi "Click on" thành "Select" có thể được điểm hay mất điểm tuỳ người chú thích đã viết gì. Trong mẫu ngẫu nhiên (hạt 20261101) có: *"Click on the first search result" → "Select the first search result"* (câu chuẩn dùng "Select", exec 0 → 0), và *"Click on the second photo of the June month" → "Click on the second photo"* (exec 1 → 0).
- CIDEr-D thưởng rất cao cho câu trùng hoàn toàn, nên độ đo này nhạy nhất với việc chép.
- Tiền lệ cảnh báo trực tiếp (mẫu đã tra): Devlin et al. (arXiv 1505.04467, **preprint**) báo phương pháp láng giềng gần đạt ngang nhiều mô hình sinh theo độ đo tự động trên COCO, nhưng trong đánh giá của người thì câu sinh mới vẫn được ưa hơn. Liu et al. (ASE 2018) chỉ ra phần lớn test mà NMT làm tốt vốn gần với mẫu train, và một bộ láng giềng gần đơn giản hơn NMT 21% theo BLEU. Một tiến sĩ AI có thể nêu đúng hai bài này. Vì vậy mới cần mốc NN (đã có về văn bản) và chấm tay.

**Không dùng để viết:** "ACE cải thiện cách diễn đạt", "nâng chất lượng câu". Được viết: "tăng độ giống câu chuẩn, chủ yếu qua các câu trùng nguyên văn". Chỉ khi có chấm tay mới được nói về chất lượng.

Hai số phản bác ý "ACE biến đầu ra thành câu mẫu" [đo]: tỉ lệ câu nằm nguyên văn trong kho là S1 59,71% · ck500 57,00% · ACE 59,24% · câu chuẩn 51,62%. ACE không vượt S1. Phủ OCR của từ nội dung trên 402 bước gần như nhau (ck500 49,8 · ACE 48,8 · câu chuẩn 47,9), nên phép đo thô này không thấy ACE nêu thứ không có trên màn hơn. Phép đo này còn thô vì chỉ có 24 dòng OCR.

### 3.2 Có đi chợ luật không: thủ tục có lỗ, nhưng kết luận không phụ thuộc lỗ đó

Mốc giờ tệp (UTC, 10/10) [đo]:

| giờ | việc |
|---|---|
| 01:02 | `doc_exec_304.json`: đã có exec **test** của R0 (−0,11) và `ra_k4` (−1,25) |
| 01:14 | `luat_ghep_304.py`: viết họ luật R0–R4 |
| 13:19 | `luat_chon.json`: chọn R3 trên val |
| 13:21 | `test_R3.json`: áp test |

`report/304` §5 ghi thẳng lý do sửa luật là exec test của R0 âm. Vậy thủ tục đúng là "**chọn** trên val, áp test một lần", nhưng **ý tưởng họ luật có nhìn test**. Thêm vào đó:

- `ra_k4` không đạt tiêu chí val của chính action (1/5 độ đo, `report/304` §3.2) mà vẫn lên test.
- R3 thắng R2, R4 đúng **một bước** trên 1.002 bước val [val], tức là chọn gần như ngẫu nhiên giữa các ứng viên.
- ch4 hiện viết "Bốn biến thể được xây dựng từ trước" và không nói điều trên. Hội đồng đọc `report/304` hoặc git sẽ thấy ngay, nên phải khai.

Điều cứu được: trên test, cả bốn luật cùng một bức tranh [đo]. Exec trong khoảng −0,11…+0,02, mọi KTC phủ 0. CIDEr-D từ +8,42 đến +11,97, mọi KTC loại 0. Chọn luật nào cũng ra cùng kết luận. Và **ACU là phép xác nhận sạch** vì luật đã đông cứng trước khi có dữ liệu đó (ACE − ck500 trên ACU: exec +0,27 [−0,07; +0,66], cứu 6 phá 2, CIDEr-D +13,00 [+7,88; +19,07]; đổi 93 câu, trong đó 14 chỉ khác hoa/dấu, 31 sai→đúng, 8 đúng→sai [đo]). Bài nên dựa vào ACU, không dựa vào cụm "áp test một lần".

Chữ **"Action-Consistent"** trong tên chưa có bằng chứng đứng riêng: R3 − R0 về exec chỉ +0,13 [−0,09; +0,36], p = 0,31 [có sẵn]. 51 câu bị điều kiện này chặn cho exec −0,13 [−0,36; +0,09], cứu 9 phá 15 [đo]: đúng chiều, không có ý nghĩa. Viết "phù hợp với thiết kế", không viết "điều kiện này là thứ giữ exec". Điều giữ exec chủ yếu là điều kiện **trùng ví dụ** (R0 so với `ra_k4` đầy đủ: −0,11 so với −1,25).

### 3.3 Cổng chọn có giá trị không: **có**

Chọn ngẫu nhiên 402 bước trong số `ra_k4` khác ck500, 20 lần [đo]:

| cách chọn | Δ CIDEr-D (trung bình, min…max) | Δ SPICE | Δ exec (số bước) |
|---|---:|---:|---:|
| ngẫu nhiên trong 2.229 bước | +1,68 (−2,08…+3,70) | +0,23 | −9,2 (−25…+6) |
| ngẫu nhiên trong 1.972 bước cùng lớp | +2,87 (+0,32…+5,01) | +0,32 | −5,6 (−20…+11) |
| **ACE** | **+11,97** | **+1,33** | **+1** |

Đây là bằng chứng tốt nhất cho việc ACE có nội dung, không chỉ là một phép gộp.

### 3.4 Rò rỉ dạy–kiểm: không thấy, nhưng câu lặp là đặc điểm dữ liệu phải khai

[đo]:

- Giao tác vụ kho và tập kiểm: **0** (1.345 tác vụ có bước chạm, kho 12.549 tác vụ trước khi bỏ val). Kho loại tác vụ val, truy vấn không dùng câu chuẩn của bước đang xét.
- Câu lặp: kho có 28.507 câu riêng trên 63.000 bước, 100 câu đầu chiếm 16,1%. **51,62% câu chuẩn tập kiểm có nguyên văn trong kho.** Không phải rò rỉ theo nghĩa nhãn của bước kiểm lọt vào, nhưng là lý do khiến phương pháp chép có đất sống, và phương pháp sẽ yếu đi ở dữ liệu ít lặp.
- Tác vụ gần trùng: 315 bước (113 tác vụ) có mục tiêu trùng nguyên văn một tác vụ trong kho. Tỉ lệ đổi câu cao gấp đôi (16,5% so 8,4%). Bỏ nhóm này, CIDEr-D vẫn +12,07 [+8,41; +15,68] (tính trên nhóm), exec cứu 15 phá 12. **Mức tăng không do nhóm gần trùng.**
- Chưa đo: màn hình gần trùng giữa kho và tập kiểm (`report/209` cho biết 90% tác vụ kiểm thuộc split train chính thức, chia theo tác vụ). Không đáng ưu tiên vì kho chỉ dùng chữ.
- Sai số trong ghi chú: `report/320` ghi khối chứa câu chuẩn ở tập kiểm "khoảng 13%". Con số đo trên test là **15,84%** (707/4.463) [đo, khớp `report/304` §1]; 13,1% là của val.

### 3.5 Một hạt giống, kích thước hiệu ứng

- **Độ đo văn bản đã có KTC.** Ghi chú "chưa có KTC" ở `report/304` là cũ. `report/320` §3.2 có sáu độ đo, lượt tính lại hôm nay ra gần trùng (BLEU-4 +1,11 [+0,79; +1,43], SPICE +1,33 [+0,93; +1,76]). Riêng METEOR chưa có KTC, không cần làm thêm.
- **Nền ck500 đổi được, 0 GPU** [đo], với cùng `ra_k4`:

| nền | câu đổi | Δ CIDEr-D | Δ SPICE | Δ exec | cứu/phá |
|---|---:|---:|---:|---:|---|
| ck500/101 | 402 | +11,97 | +1,33 | +0,02 [−0,21; +0,25] | 15/14 |
| ck500/202 | 404 | +12,21 [+8,58; +16,08] | +1,31 | +0,22 [−0,05; +0,50] | 23/13 |
| S1/101 | 390 | +12,57 [+9,36; +16,05] | +1,36 | +0,13 [−0,07; +0,35] | 16/10 |

  Đọc: mức tăng lặp lại rất sát, và lớn hơn nhiễu hạt của ck500 (CIDEr-D chênh +1,17). Nhưng **cả ba dùng chung một `ra_k4`**, sinh từ ck500/101, nên đây là lặp lại trên nền, không phải hạt độc lập. Đồng thời bảng này cho thấy ACE **độc lập với GRPO**: gắn lên S1 cũng ra cùng mức. Đó là lý do nên trình ACE như một bước riêng, không phải hệ quả của ck500.
- **Độ lớn:** ACE − ck500 về exec nằm trong ±0,26. Với 29 cặp bất đồng, cỡ hiệu ứng lớn hơn 0,3 điểm là khó xảy ra [suy]; viết "không phát hiện khác biệt, KTC hẹp" tốt hơn "tương đương" vì không có biên tương đương đặt trước.
- ACE chỉ dùng được **18% cận trên** theo CIDEr-D (+11,97 trong +65,37) [đo]. Vẫn còn dư địa ở bài toán nhận ra câu đúng trong khối.

### 3.6 Phương pháp hay hậu xử lý: **hậu xử lý có cổng**, và nên gọi đúng tên

- Không có tham số học riêng cho cổng. Luật dựa trên chuỗi và sáu lớp động từ.
- Tuy nhiên `ra_k4` có train riêng, nên đây không phải hậu xử lý miễn phí.
- Tiền lệ cùng ý tưởng chọn giữa câu sinh và câu truy hồi là Song et al. (IJCAI 2018), Cao et al. (ACL 2018), Hossain et al. (ACL 2020). Trong các bài đó phần xếp hạng thường được học hoặc dùng tiêu chí riêng theo bài toán. **Đây là mẫu đã tra, không phải chứng minh chưa ai làm**, và không dùng chữ "đầu tiên".
- Đề xuất đặt ACE ở vai trò: *bước tái dùng câu sau sinh, chỉ can thiệp khi mô hình có truy hồi tự chọn đúng một câu trong khối*. Đóng góp chính nằm ở ck500, vì chính ck500 đem lại mức tăng exec. 60,68 của ACE gần như toàn bộ là 60,65 của ck500.

Cần sửa trong tài liệu (chưa sửa, ghi lại cho lượt sửa luận văn):

| chỗ | vấn đề | sửa thành |
|---|---|---|
| `report/320` dòng 41, 258, 536 | "tác hại ở bước không chạm là lý do/động lực có ACE" | bỏ. ACE buộc cùng lớp thao tác, `action_ok` không đổi một bước |
| ch4 §4.6 đoạn *Chọn điều kiện* | "xây dựng từ trước" | khai rõ: đặt sau khi thấy exec test của R0 |
| ch4 §4.6 | "theo ý tưởng của SmallCap" | SmallCap truy hồi theo độ tương đồng **ảnh–văn bản** trong CLIP; ACE truy hồi chỉ bằng chữ, nên chỉ chung ý đưa câu truy hồi vào câu nhắc |
| ch4 §4.6 | "nhánh so sánh không dùng câu ví dụ được giữ lại để tách ảnh hưởng của truy hồi" | nhánh này chỉ có val, chưa có số test; làm việc ưu tiên 2 rồi mới được nói |
| ch6 §6.4 | "thay 402 câu" | 402 câu khác chuỗi, 344 câu khác sau tách từ, 58 câu chỉ khác hoa/dấu |
| ch4, ch6, ch7, tóm tắt | "cải thiện cách diễn đạt", "chất lượng" | "tăng độ giống câu chuẩn" |
| `report/323` §4 | "chỉ ACE vừa giữ exec vừa tăng 7 độ đo" | R0, R2, R4 cũng vậy; viết "họ luật có điều kiện chép" |

---

## 4. Thực tiễn áp dụng

### 4.1 Cần gì lúc triển khai

| thành phần | số đo | nguồn |
|---|---|---|
| kho câu | 62.880 bước, tệp 30 MB | [đo] |
| chỉ mục TF-IDF | dựng 2,8 s; truy vấn trung bình 0,14 s, p95 0,24 s (Python thuần, một luồng); RSS cả tiến trình 447 MB | [đo, WSL CPU] |
| sinh câu | ck500 3,05 s/bước · `ra_k4` 3,08 s/bước trên một T4 | [đo từ log ACU] |
| ACE tổng | ~6,3 s/bước nếu chạy nối tiếp trên một T4, tức **gấp đôi ck500**; ~3,2 s nếu hai GPU song song | [suy từ các số trên] |
| adapter | 60 MB mỗi cái, cùng một mô hình nền hoà S1 | [đo] |
| VRAM suy luận | **chưa đo** (7,3 GiB là số lúc train) | |
| OCR | cần như các nhánh khác, dùng thêm cho xếp thứ tự ví dụ | mã |

Chi phí đáng kể nhất là **sinh mọi bước bằng mô hình thứ hai để dùng lại ở 9% bước**. Đó là lý do việc ưu tiên 6 đáng thử.

### 4.2 Có ích cho người dùng cuối ở đâu

Có bằng chứng: trong tập AndroidControl, khi thao tác phổ biến có sẵn câu trong kho, ACE đưa câu về đúng cách viết của người chú thích. Câu ACE hay dùng nhất là các thao tác chung: tìm kiếm, gửi, quay lại, xác nhận (`click on the search icon`, `go back to the previous screen`) [đo].

[suy, chưa có số] Ý nghĩa thực tế khả dĩ là văn phong nhất quán trong một bộ tài liệu hướng dẫn, và dễ mở rộng bằng cách thêm câu vào kho không cần train lại. Tiền lệ SmallCap, EXTRA và kNN-LM có báo cáo đổi kho để chuyển miền, nhưng **dự án chưa đo việc này**.

Không có bằng chứng rằng người dùng làm thao tác đúng hơn: exec không tăng, Phi-4 đúng 0,00, và không có chấm tay.

Rủi ro: 70 bước (1,6%) đổi sang câu khác lõi nội dung, cứu 6 phá 7 [đo], tức có đổi phần tử mà không có căn cứ từ ảnh ở tầng luật. Ví dụ trong mẫu: *"Click on the star icon of the first mail" → "Click on the star icon of the mail from Jane"*. Khi triển khai nên báo rõ câu đến từ kho.

### 4.3 Giới hạn khi gặp app mới

| tình huống | câu đổi | khối có câu chuẩn | ACE − ck500 exec | nguồn |
|---|---:|---:|---|---|
| tập kiểm chính | 402/4.463 (9,0%) | 15,84% | +0,02 | [đo] |
| ACU (tác vụ S1 chưa thấy) | 93/1.484 (6,3%) | 8,7% | +0,27 [−0,07; +0,66] | `report/320` mục 8 |
| app chưa thấy trong tập kiểm | 7/78 (9,0%) | 17,9% | 0 bước | [đo], n nhỏ |
| AitZ (bộ dữ liệu khác) | 52/2.736 (1,9%) | 0% | cứu 1 phá 1 | `report/320` mục 6 |
| **mô phỏng kho không có app đó** | chưa sinh lại | 11,43% (so 16,70% cùng lát 1.784 bước) | chưa đo | [đo độ phủ] |
| **lịch sử tự sinh** | chưa sinh lại | 14,18% (633/4.463) | chưa đo | [đo] |

Với lịch sử tự sinh: câu cuối trong lịch sử đổi ở 3.274 bước, 48,3% khối giữ y hệt. Độ phủ giảm vừa phải. Nhưng toàn bộ con số ACE đang báo dùng **lịch sử câu chuẩn**, cả lúc truy hồi lẫn lúc sinh câu, nên ACE dưới điều kiện triển khai thật **chưa có số** (ck500 thì đã có: exec giảm 4,21 điểm, `report/320` mục 7).

Trạng thái khi không khớp: ACE trả về đúng câu ck500. Trên AitZ, điều này được xác nhận: exec bằng nhau, mọi KTC văn bản phủ 0. Vậy ở app lạ ACE an toàn nhưng gần như không tác dụng, và vẫn tốn gấp đôi thời gian.

Mô phỏng app mới [đo]: với 1.784 bước có nhãn app (256 app), bỏ khỏi kho mọi tác vụ có mục tiêu nhắc tên app đó rồi truy hồi lại. Độ phủ khối giảm từ 16,70% xuống 11,43%, tức mất khoảng một phần ba. 49,27% câu chuẩn vẫn còn nguyên văn trong kho đã bỏ app. Đọc [suy]: nhiều câu là câu chung giữa các app, nên giới hạn chính có vẻ nằm ở **văn phong của người viết** hơn là ở app. AitZ (câu do GPT-4V sinh rồi người sửa) có độ phủ 0% cũng khớp cách đọc này, và khớp nhận định ở `report/320` §6.4.

Ba giới hạn của mô phỏng này: chỉ nhận ra app qua tên trong mục tiêu, nên có thể bỏ sót tác vụ cùng app và số 11,43% có thể cao hơn thực; chỉ phủ các bước có nhãn app (khoảng 40% tập kiểm); và đây mới là độ phủ của khối, chưa phải ACE − ck500. Muốn có số ACE thì phải sinh lại `ra_k4` (việc ưu tiên 8).

---

## 5. Câu trả lời đề xuất cho thầy

> **Vì sao chọn ACE, đã khảo sát chưa?**
>
> Em chia ACE ra khỏi đóng góp chính. Mức tăng exec là của GRPO thưởng SPICE; ACE không tăng exec (+0,02, KTC [−0,21; +0,26]) và không đổi loại thao tác. ACE chỉ làm một việc hẹp: khi mô hình có truy hồi tự viết đúng một câu trong khối ví dụ và câu đó cùng loại thao tác, lấy câu đó thay cho câu ban đầu.
>
> Về khảo sát: em xuất phát từ dòng sinh câu có truy hồi (SmallCap CVPR 2023, EXTRA EACL 2023), cơ chế chép (CopyNet ACL 2016, pointer-generator ACL 2017), retrieve-and-edit (NeurIPS 2018), và ghép câu sinh với câu truy hồi (IJCAI 2018, ACL 2020). Đó là mẫu em đã tra, không phải toàn bộ.
>
> Về số test, em đã chạy các phương án sau trên cùng tập kiểm:
> - dùng mô hình truy hồi cho mọi bước: exec −1,25, có ý nghĩa;
> - để mô hình tự học chép hay viết (CW-RA): exec −2,13, thua cả bảy độ đo văn bản;
> - RA-GRPO không qua được bước kiểm đầu;
> - lấy thẳng câu ví dụ không qua mô hình sinh: CIDEr-D −168, văn bản thua xa (exec của mốc này em chưa chấm);
> - chọn ngẫu nhiên cùng số câu: CIDEr-D chỉ +1,7, so với +12,0 của ACE.
>
> ACE là phương án duy nhất trong nhóm đã thử giữ được exec và tăng cả sáu độ đo có KTC, cùng với các biến thể gần của chính luật này.
>
> Những giới hạn em phải khai:
> - Mức tăng văn bản gần như hoàn toàn đến từ khoảng 2,5% số bước câu trở thành đúng nguyên văn câu chuẩn, nên em chỉ nói "giống câu chuẩn hơn", không nói "câu tốt hơn".
> - Họ luật được đặt sau khi em đã thấy exec test của biến thể đầu; lần xác nhận sạch là ACU (CIDEr-D +13,00 [+7,88; +19,07], exec +0,27 [−0,07; +0,66]).
> - Lợi ích phụ thuộc kho có câu phù hợp: AitZ gần như không kích hoạt.
> - `ra_k4` mới một hạt giống, và chi phí suy luận gấp đôi.

Khi nào dùng được thêm: câu về `cont` + R3, về bước không chạm, về lịch sử tự sinh chỉ thêm sau khi chạy các việc ở §2.3. Chưa chạy thì nói "chưa đo".

---

## 6. Việc cần làm theo thứ tự

1. **Quyết của user:** hạ ACE xuống phần mở rộng, đóng góp chính là ck500 (§1, §3.6). Việc này ảnh hưởng tóm tắt, ch1, ch4, ch7.
2. **0 GPU, làm ngay:** viết lại script vào `harness/`, chạy lại đối chiếu với số ở file này, ghi `runs/ace_ablation/` (đây là Z3 của `report/323`), rồi ghi kết quả vào `report/320` mục mới. Bảng R0–R4 phải khai R3 chọn trên val, và phần test của R0, R2, R4 chỉ để mô tả.
3. **T4 ~2 h:** exec cho NN-1, NN-vote, SNAP. Có thể ghép cùng commit với việc 4.
4. **T4 ~3,2 h:** `cont` + R3 trên test.
5. **T4 ~2,1 h + 0 GPU:** bước không chạm của ACE (`report/322` #4 còn nợ).
6. **T4 ~2 h + chấm:** ACE dưới lịch sử tự sinh.
7. **T4 ~10,7 h, hai commit:** hạt thứ hai của `ra_k4`.
8. **Tuỳ kết quả 4:** nếu `cont` + R3 ngang ACE, ưu tiên thử chấm log-prob một mô hình (việc 6 ở §2.3) và cân nhắc bỏ khối ví dụ khỏi mô hình thứ hai.
9. **CPU trước:** độ phủ của truy hồi dày và truy hồi theo ảnh. Chỉ khi phủ hơn rõ rệt mới sinh lại.
10. **User quyết:** chấm tay mù 100 cặp. Không làm thì giữ nguyên câu chữ "giống câu chuẩn hơn".
11. Sau cùng mới sửa luận văn một lượt, theo bảng ở §3.6.

Hàng đợi Kaggle cần xếp sau lô lưới RL đang chạy. Mục này không đụng `_bundles/luoi/`.

---

## 7. Nguồn tài liệu ngoài (kiểm 1/11/2026)

Đây là mẫu đã tra có chủ đích, không phải khảo sát đầy đủ.

| tài liệu | venue | mức kiểm | dùng cho |
|---|---|---|---|
| Ramos, Martins, Elliott, Kementchedjhieva. SmallCap | CVPR 2023, tr. 2840–2849 | đọc PDF arXiv: truy hồi theo độ tương đồng ảnh–văn bản CLIP; venue qua kết quả tra cứu CVF | truy hồi trong câu nhắc |
| Ramos, Elliott, Martins. Retrieval-augmented Image Captioning (EXTRA) | EACL 2023, tr. 3666–3681 | ACL Anthology + bản HTML: có ghi "sometimes even copying an entire sentence" và câu truy hồi có thể dẫn sai, **không có số đo** | rủi ro chép |
| Li, Li, Ramos, Tang, Elliott. Understanding Retrieval Robustness for Retrieval-augmented Image Captioning | ACL 2024, tr. 9285–9299 | qua kết quả tra cứu ACL Anthology | mô hình chép token đa số trong khối; lấy mẫu đa dạng lúc train |
| Hashimoto, Guu, Oren, Liang. Retrieve-and-Edit | NeurIPS 2018, tr. 10052–10062 | proceedings | retrieve-and-edit |
| Guu, Hashimoto, Oren, Liang. Generating Sentences by Editing Prototypes | TACL 2018, tập 6, tr. 437–450 | ACL Anthology | sửa nguyên mẫu |
| Weston, Dinan, Miller. Retrieve and Refine | SCAI @ EMNLP 2018, tr. 87–92 (**workshop**) | ACL Anthology | truy hồi rồi viết lại |
| Hossain, Ghazvininejad, Zettlemoyer. Retrieve-Edit-Rerank | ACL 2020, tr. 2532–2538 | ACL Anthology | xếp hạng lại |
| Cao, Li, Li, Wei. Retrieve, Rerank and Rewrite | ACL 2018, tr. 152–161 | qua kết quả tra cứu | khuôn mềm |
| Song et al. An Ensemble of Retrieval-Based and Generation-Based… | IJCAI 2018, tr. 4382–4388 | qua kết quả tra cứu trang IJCAI | ghép câu sinh + câu truy hồi, gần ACE nhất trong mẫu |
| Gu, Lu, Li, Li. CopyNet | ACL 2016, tr. 1631–1640 | ACL Anthology | cơ chế chép |
| See, Liu, Manning. Pointer-Generator | ACL 2017, tr. 1073–1083 | ACL Anthology | cơ chế chép |
| Bulte, Tezcan. Neural Fuzzy Repair | ACL 2019, tr. 1800–1809 | ACL Anthology | translation memory |
| Xu, Crego, Senellart. Boosting NMT with Similar Translations | ACL 2020, tr. 1580–1590 | ACL Anthology | translation memory |
| Khandelwal et al. kNN-LM | ICLR 2020 | qua trang hội nghị | kNN lúc suy luận |
| Khandelwal et al. kNN-MT | ICLR 2021 | trường comments trên arXiv | kNN lúc suy luận |
| Zhang et al. Rencos | ICSE 2020, tr. 1385–1397 | qua kết quả tra cứu; **không đọc toàn văn** | truy hồi trong tóm tắt mã |
| Zheng et al. Synapse | ICLR 2024 | qua trang hội nghị | truy hồi quỹ đạo cho tác vụ GUI |
| Geifman, El-Yaniv. SelectiveNet | ICML 2019, PMLR 97:2151–2159 | PMLR | selective prediction |
| Geifman, El-Yaniv. Selective Classification for DNN | **venue chưa kiểm** (bản 2017) | chưa kiểm | selective prediction |
| Liu et al. NMT-based commit message generation: how far are we? | ASE 2018, tr. 373–384 | qua kết quả tra cứu, chỉ đọc abstract | mốc láng giềng gần đơn giản |
| Allamanis. Adverse Effects of Code Duplication | SPLASH Onward! 2019 (theo trang arXiv) | trang arXiv | trùng lặp làm phồng số đo tới 100% |
| Devlin et al. Exploring Nearest Neighbor Approaches for Image Captioning | arXiv 2015, **preprint** | trang arXiv | NN đạt độ đo nhưng người ưa câu sinh |

---

## Bổ sung 2/11: đối chiếu độc lập

`harness/ace_doi_chieu.py` viết lại từ định nghĩa, kết quả ở `runs/ace_ablation/doi_chieu_327.json` (số test, 0 GPU).

- **Khớp đúng:** 402 bước đổi · nhóm 113, 29, 58 · exec 60,68 và 60,65 · `action_ok` 4.283 · cứu/phá 8/1, 0/4, 11/1, 4/13.
- **Khớp gần:** Δ CIDEr-D nhóm 113 là +14,07 (bài viết +13,96), tổng +12,04 (bài viết +11,97), do tách từ xấp xỉ và df khác cách của bộ chấm COCO. Khối có câu chuẩn 710/3.753 bước so với 707/3.756, do cách chuẩn hoá khi so câu. Exec theo khối 71,69 → 73,10 so với 71,71 → 73,13.
- **Chưa khớp:** hai nhóm "cùng lõi" và "khác lõi" (167/35 so với 132/70), vì script mới chỉ xấp xỉ định nghĩa lõi. Không dùng hai nhóm này từ script mới.
- **Chưa đối chiếu:** BLEU-4, SPICE, ROUGE-L, chrF và các KTC theo nhóm. Các số 327 có trong `runs/danh_gia_327/a2.log` nhưng chưa có script tái lập; trước khi đưa vào `report/320` phải bổ sung.
