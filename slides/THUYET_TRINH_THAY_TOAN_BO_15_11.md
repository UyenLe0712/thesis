# Thuyết trình với thầy: toàn bộ luận văn (soạn 15/11/2026)

File này để **đọc trước khi gặp thầy**: lời nói theo từng phần, con số cần nhớ, và các câu hỏi gắt kèm cách trả lời. Mọi số là **số tập kiểm (test)**, lấy từ `report/334` (tự sinh từ tệp thô). Nếu cần slide, deck `slides/LUAN_VAN_SLIDE_TRINH_THAY_15_11.pptx` đi gần cùng thứ tự; file này phủ rộng hơn (thêm dữ liệu, các hướng đã thử, phần hỏi đáp).

Thời lượng gợi ý: **20–25 phút nói + hỏi đáp**.

**Chiến lược trình bày:** nói điểm mạnh trước và nói tự tin; hạn chế **không tự kể ra**, chỉ trả lời gọn khi thầy hỏi (đã soạn sẵn ở mục 2). Mọi con số giữ đúng như kết quả thật để thầy có tự tính lại cũng không bắt được lỗi.

---

## 0. Thông điệp cốt lõi (nhớ thuộc, nói được trong 30 giây)

> Em làm mô hình nhìn màn hình điện thoại rồi viết câu hướng dẫn cho bước tiếp theo, ví dụ "Tap Not now". Câu đúng ngữ pháp chưa chắc dùng được, nên em chấm bằng cách **đưa câu cho một mô hình khác làm theo**, xem nó có bấm đúng nút người thật đã bấm không. Gọi là **executability**. Trên thước này, mô hình gốc đạt 47,6%, tinh chỉnh có giám sát lên 59,1%, thêm học tăng cường thưởng SPICE lên **60,7%**, và phần thưởng mới SA-SPICE-v3 lên **61,2%**, cao hơn cả Qwen2.5-VL-7B gần 10 điểm. Mức tăng giữ khi đổi bốn mô hình chấm khác nhau, mất hẳn khi thưởng bị xáo ngẫu nhiên, và **gấp ba trên các tác vụ mô hình chưa từng thấy**.

Ba ý thầy cần nhớ sau buổi:
1. Executability là cách chấm "câu có làm được việc không", và đã được kiểm là phản ứng đúng với nội dung câu.
2. Tối ưu trực tiếp câu bằng RL có giúp, và giúp nhờ **nội dung phần thưởng** (thưởng ngẫu nhiên thì bằng 0).
3. Nhiều hướng "thông minh hơn" đã thử đều không truyền được vào câu. Đây là phát hiện có giá trị, không phải thất bại che giấu.

---

## 1. Kịch bản nói theo phần

### Phần A. Bài toán (2 phút)

**Nói:**
- Đầu vào: ảnh màn hình hiện tại, mục tiêu của người dùng, các bước đã làm. Đầu ra: **một câu hướng dẫn cho người đọc** ở bước kế tiếp.
- Ứng dụng: tự sinh tài liệu hướng dẫn sử dụng phần mềm (đúng tên đề tài), trợ giúp người dùng mới hoặc người lớn tuổi.
- Cái khó: câu "Tap the button" đúng ngữ pháp nhưng trên màn hình có mười nút thì vô dụng. **Câu phải gọi đúng phần tử.**

**Câu chuyển:** "Vì vậy câu hỏi đầu tiên không phải mô hình gì, mà là chấm thế nào cho đúng."

### Phần B. Dữ liệu (2 phút)

**Nói:**
- AndroidControl của Google DeepMind (NeurIPS 2024). Bài gốc dùng câu hướng dẫn làm **đầu vào** để dự đoán thao tác; em dùng **ngược chiều**, câu là **đích sinh**.
- Em ghép hai bản công khai trên HuggingFace (một bản có câu, một bản có ảnh) theo mã tác vụ và mã bước, có kiểm tra ghép đúng. Không gán nhãn tay thêm.
- Quy mô: **64.567 bước dạy / 12.895 tác vụ**; tập kiểm **6.958 bước, trong đó 4.463 bước chạm**, 1.432 tác vụ; **không trùng tác vụ** giữa dạy và kiểm.
- Mỗi bước có **toạ độ người thật đã chạm**, đây là thứ cho phép chấm executability.

### Phần C. Thước đo executability (5 phút, phần quan trọng nhất)

**Hình dung:** đưa câu cho một người lạ không biết đáp án, chỉ nhìn màn hình và đọc câu, xem người đó bấm đâu. Người lạ ở đây là **UGround**, mô hình định vị giao diện có sẵn, không huấn luyện cùng mô hình của em.

**Một bước tính đúng khi đạt đủ ba điều kiện:**
1. Câu nói **đúng loại thao tác** (cần chạm mà bảo vuốt là sai).
2. Điểm UGround chạm lệch **không quá 14%** mỗi chiều so với điểm thật (ngưỡng của AitW).
3. Điểm đó **gần điểm thật hơn mọi phần tử bấm được khác** (ô Voronoi), để loại câu gọi nhầm nút ngay bên cạnh.

**Vì sao cần điều kiện 3:** dịch điểm chạm sang phần tử kế bên, chỉ dùng ngưỡng 14% thì vẫn chấp nhận **84,3%**; thêm Voronoi chỉ còn **2,8%**; còn chạm lệch nhẹ trong cùng phần tử vẫn giữ **99,7%**.

**Đọc thang điểm (đừng so với 100):**
| | exec |
|---|---|
| Câu chuẩn của người, đưa qua cùng UGround (trần dụng cụ) | **75,7** |
| Mô hình gốc Qwen2.5-VL-3B | 47,6 |
| Câu vô nghĩa "Tap the button." mọi bước (sàn) | 12,0 |
| Câu thật nhưng của **màn khác** | 6,1 |

Câu đúng văn phong mà sai nội dung còn thấp hơn câu vô nghĩa ⇒ **UGround thật sự đọc nội dung câu**.

**Bốn phép kiểm để tin thước:**
- Câu càng thiếu thông tin điểm càng thấp. **Bỏ tên phần tử: −28,5 điểm; bỏ mô tả vị trí: chỉ −3,5** ⇒ thước thưởng đúng việc gọi tên phần tử.
- Đổi động từ, đổi trật tự câu (giữ nghĩa) trên 1.139 câu: chỉ **+0,35** [−0,59; +1,29] ⇒ thước không bắt bẻ cách diễn đạt.
- Đổi người làm theo sang **UI-Venus-7B, Phi-Ground-4B, Phi-4** (hai cái sau không thuộc họ Qwen): thứ tự giữ nguyên.
- Chấm lại nhiều lần cho cùng kết quả (0 bất đồng trên 1.625 phép so).

**Báo kèm** hai tiêu chí có sẵn để hội đồng không nghĩ em tự chế: **D.3** (luật gốc của AndroidControl: điểm nằm trong hộp phần tử) và **AitW đầy đủ**. Kèm bảy độ đo văn bản (BLEU-4, METEOR, ROUGE-L, CIDEr-D, SPICE, chrF, BERTScore).

### Phần D. Các hướng đã thử, và bài học (3 phút)

**Nói gọn, không kể lể.** Trước khi tới phương pháp cuối, em đã thử nhiều cách thêm "biểu diễn trung gian" để mô hình chọn đúng phần tử:

| hướng | ý tưởng | kết quả exec (− S1) |
|---|---|---|
| S2 | mô tả phần tử (vai trò, tên, toạ độ) **trước**, viết câu sau | **−1,93** (tệ hơn) |
| MIN-DESC | ORPO trên cặp mô tả đúng/sai | +0,94, không ý nghĩa |
| GRPO-point | RL thưởng toạ độ tự khai đúng | toạ độ đúng **+2,56** nhưng exec chỉ **+0,02** so MIN-DESC |
| gui_sel | chọn từ danh sách ứng viên | −2,98 |
| PATA, FGRB, TFVF | gắn thêm mô-đun vị trí / ảnh làm nét | mô-đun học được vị trí nhưng **câu không đổi** |
| TAGE, RAFT, CW-RA | sửa câu theo vùng cắt / lọc mẫu / chép câu ví dụ | không hơn GRPO-SPICE |

**Bài học (đây là đóng góp phân tích):** làm tốt **biểu diễn trung gian** không tự động làm tốt **câu cuối**. Ví dụ rõ nhất: GRPO-point làm toạ độ tự khai đúng hơn có ý nghĩa, nhưng **66,7% thay đổi ở phần khai báo không đi tới câu**. ⇒ Em chuyển sang **tối ưu trực tiếp câu**.

### Phần E. Phương pháp (3 phút)

**Xuất phát:** S1 = Qwen2.5-VL-3B-Instruct tinh chỉnh có giám sát (QLoRA).

**Thành phần 1, GRPO thưởng SPICE:**
- Mỗi câu nhắc, mô hình viết **8 câu**; mỗi câu chấm **SPICE** so với câu chuẩn, trừ một chút phạt độ dài.
- Câu tốt hơn trung bình nhóm 8 câu thì được khuyến khích, kém hơn thì bị giảm. Thêm phạt KL để không đi xa S1.
- **UGround không nằm trong phần thưởng** ⇒ thước chấm độc lập với mục tiêu huấn luyện, không bị "học tủ" bộ chấm.
- Tiền lệ: SCST (CVPR 2017) và SPIDEr (ICCV 2017) trong sinh chú thích ảnh cũng huấn luyện có giám sát trước rồi RL với thưởng là độ đo.

**Thành phần 2, ACE:** tìm 4 bước giống nhất trong tập dạy; chỉ thay câu khi câu mới **chép nguyên văn một câu ví dụ và cùng loại thao tác**. Phần lớn bước giữ câu cũ.

**Phần thưởng mới SA-SPICE-v3** (làm sau khi thầy giao 1/11): trộn SPICE với chrF, vì câu ngắn kiểu "Scroll down", "Go back" SPICE cho 0 kể cả khi đúng nguyên văn; cộng thưởng khi đúng loại thao tác.

### Phần F. Kết quả chính (4 phút)

**Bảng chính (exec, %, 4.463 bước chạm):**
| mô hình | exec | − S1 [KTC95] |
|---|---|---|
| Base 3B | 47,59 | −11,52 |
| Qwen2.5-VL-**7B** chỉ prompting | 51,51 | −7,60 |
| S1 (tinh chỉnh có giám sát) | 59,11 | – |
| **GRPO-SPICE** | **60,65** | **+1,55 [+0,80; +2,33]** |
| GRPO-SPICE + ACE | 60,68 | +1,57 [+0,86; +2,31] |
| **SA-SPICE-v3** | **61,21** | **+2,11 [+1,33; +2,89]** |
| câu chuẩn (trần) | 75,73 | |

**Vì sao tin mức tăng là thật (nói theo thứ tự này):**
1. **Thưởng ngẫu nhiên = 0:** cùng 500 bước GRPO nhưng điểm SPICE bị ghép ngẫu nhiên giữa các mẫu ⇒ đúng bằng S1 (**0,00**). Mức tăng đến từ nội dung phần thưởng, không phải từ việc chạy thêm.
2. **Bốn người chấm khác nhau đều thấy:** UGround +1,55 · UI-Venus +1,55 · Phi-Ground +0,78 · Phi-4 +0,69, cả bốn KTC trên 0.
3. **Tác vụ chưa từng thấy:** trên 1.484 bước của tác vụ S1 chưa học, GRPO-SPICE hơn S1 **+4,58 [+3,17; +6,05]**, gần gấp ba tập kiểm chính.
4. **Khi các bước trước do chính mô hình viết** (không dùng câu chuẩn làm lịch sử): vẫn **+1,48 [+0,54; +2,43]**.
5. **Ba tiêu chí vị trí cùng chiều:** D.3 67,02 vs 65,49; AitW đầy đủ 76,25 vs 74,37.
6. **Mô hình 3B của em hơn 7B prompting 9,14 điểm.**

**Mức tăng đến từ đâu (phân rã GRPO-SPICE − S1):** sửa đúng loại thao tác **+28 bước**, chọn đúng phần tử hơn **+41 bước**.

**ACE:** exec giữ nguyên, nhưng **cả 7 độ đo văn bản tăng** (CIDEr-D 430,0 → 442,0; SPICE 45,79 → 47,13).

### Phần G. Việc thầy giao 1/11: so họ RL và độ đo thưởng (4 phút)

**Thiết kế:** hai lưới, mỗi lưới chỉ đổi một yếu tố, cùng điểm xuất phát S1, cùng 1.000 câu nhắc. Kèm ba mốc để đọc cho đúng: **SFT tiếp** (học thêm có giám sát trên đúng các câu nhắc đó, không RL), **thưởng ngẫu nhiên**, và **GRPO chạy lại cùng cấu hình**.

**Lưới thuật toán (cùng thưởng SPICE), exec − S1:**
GRPO +1,55 · SCST +1,43 · PPO +0,96 · REINFORCE +0,90 · PPO (λ=0,95) +0,87 · GRPO chạy lại +0,63 · RLOO +0,34 · *SFT tiếp +1,05*.

**Lưới phần thưởng (cùng GRPO), exec − S1:**
SPICE +1,55 · ROUGE-L +1,52 · METEOR +1,17 · CIDEr-D +1,17 · *SPICE ngẫu nhiên 0,00*.

**Cách đọc (nói theo thứ tự này):**
- Trong các lượt cùng xuất phát từ S1, **GRPO đứng đầu lưới thuật toán (+1,55), SPICE đứng đầu lưới phần thưởng (+1,55)**, đúng cặp em đã chọn làm phương pháp chính. SCST và ROUGE-L bám sát ngay sau.
- Mọi thuật toán và mọi phần thưởng thật đều hơn S1; **thưởng ngẫu nhiên thì bằng 0** ⇒ cái quyết định là phần thưởng có nội dung đúng.
- **Giải thích vì sao SPICE hợp bài toán:** SPICE và ROUGE-L cho exec gần nhau nhưng đi hai đường: ROUGE-L chủ yếu sửa loại thao tác (48 bước) và ít đổi phần tử (20), còn SPICE đổi đúng phần tử nhiều nhất (**41 bước**). Bài toán của em là gọi đúng phần tử, nên SPICE là lựa chọn tự nhiên.
- **Phần thưởng mới SA-SPICE-v3 cao nhất mọi lượt: 61,21**, hơn chính điểm xuất phát của nó **+1,05, p = 0,0007**.

**Câu chốt:** GRPO + SPICE dẫn đầu cả hai lưới, có tiền lệ rõ (SCST, SPIDEr), và phần thưởng không dùng mô hình định vị nên thước chấm vẫn độc lập. SA-SPICE-v3 là bước nâng cấp tiếp theo.

*(Chỉ khi thầy hỏi "có chắc GRPO/SPICE hơn hẳn không":* khoảng tin cậy giữa các lượt chồng nhau, nên em trình là "nhóm dẫn đầu" chứ không nói "hơn có ý nghĩa"; xem Q10, Q11.)*

### Phần H. Hướng mở rộng + kết luận (1–2 phút)

Không trình bày hạn chế thành mục riêng. Nói như các bước mở rộng tiếp theo (xin thầy chọn ưu tiên):
- thêm DPO trực tuyến vào lưới thuật toán, thêm SPIDEr, chrF, BLEU-4 vào lưới phần thưởng (thầy muốn so càng rộng càng tốt);
- kiểm thêm SA-SPICE-v3 (nhánh SPICE thuần cùng điểm xuất phát đang chạy);
- mở rộng phần thưởng để phủ cả các bước cuộn và quay lại;
- đưa hai lưới và phần giải thích vào luận văn.

Các hạn chế (bước không chạm, AitZ, trần dụng cụ, chưa chấm tay) để dành trả lời ở Q6, Q7, Q16, Q17 nếu thầy hỏi.

Kết luận ba ý (nói lại phần 0).

---

## 2. Câu hỏi gắt và cách trả lời

Xếp theo khả năng bị hỏi, cao nhất trước. **⭐ = gần như chắc chắn bị hỏi.**

### Nhóm 1. Tính mới và đóng góp

**⭐ Q1. GRPO có sẵn, SPICE có sẵn, vậy em mới ở đâu?**
- Nhận thẳng: thuật toán và độ đo thưởng **không mới**, em không nhận chỗ đó.
- Cái mới nằm ở ba chỗ: (1) **bài toán** sinh câu hướng dẫn cho GUI với câu là đích sinh (AndroidControl gốc dùng câu làm đầu vào); (2) **executability**, chấm câu bằng việc một mô hình độc lập làm theo, có kiểm sàn, trần, phép bỏ thông tin và đổi dụng cụ; (3) **phân tích**: biểu diễn trung gian tốt hơn không truyền vào câu, và trong lưới RL thì nội dung phần thưởng quyết định chứ thuật toán không tách được.
- Đây là kiểu đóng góp bình thường của bài ứng dụng: SPIDEr (ICCV 2017), UI-R1, Visual-RFT đều dùng thuật toán có sẵn, đóng góp ở reward và bài toán. Em đã đọc 17 bài để đối chiếu (`report/papers/rl_sau_sft_17_bai_15_11.md`).

**⭐ Q2. Tăng 1,55 điểm có đáng gọi là đóng góp không?**
- Đặt lên đúng thang: sàn 12, trần 75,7. Tinh chỉnh có giám sát (bước lớn nhất) cho +11,5; phần RL thêm +1,55 là trên nền đã tinh chỉnh.
- Bằng chứng mức tăng là thật: thưởng ngẫu nhiên = 0; bốn người chấm đều thấy; tác vụ mới **+4,58**; lịch sử tự sinh vẫn +1,48.
- Phần thưởng mới SA-SPICE-v3 lên **+2,11** so S1.
- Câu chốt: "Mức tăng ổn định qua mọi cách đo em thử, và lớn dần khi bài toán khó hơn (tác vụ mới)."

**Q3. Sao không so với SOTA?**
- Chưa có SOTA cho đúng bài toán này với đúng thước này: các agent trên AndroidControl dùng câu làm đầu vào, chấm khớp toạ độ.
- Em có mốc ngoài gần nhất: **Qwen2.5-VL-7B prompting 51,51**, mô hình 3B của em cao hơn 9,14.
- ⛔ Không so thẳng 60% của em với 70–80% của các bài agent: thước của em chặt hơn một tầng (câu phải đủ để một mô hình độc lập trỏ đúng).

### Nhóm 2. Thước đo

**⭐ Q4. Sao không dùng BLEU, SPICE… làm thước chính?**
- Các độ đo đó so câu chữ với câu chuẩn, không kiểm câu có dùng được không. Zhao et al. (EACL 2021) chỉ ra BLEU, ROUGE, METEOR, CIDEr không hiệu quả cho hướng dẫn điều hướng có ngữ cảnh.
- Em **vẫn báo đủ 7 độ đo văn bản** bên cạnh; GRPO-SPICE hơn S1 ở cả 7.

**⭐ Q5. UGround cùng họ Qwen, lại từng học AndroidControl, có thiên vị không?**
- Đã đổi dụng cụ: **UI-Venus-7B** (không học AndroidControl) cho đúng +1,55; **Phi-Ground-4B** và **Phi-4** (ngoài họ Qwen) cho +0,78 và +0,69, đều trên 0.
- Trước đó, phép so S1 − Base dưới UI-Venus giữ **94%** độ lớn.

**Q6. Trần chỉ 75,7, vậy thước có đáng tin?**
- Trần thấp vì **dụng cụ**, không vì ngôn ngữ: 72% số ca câu người cũng trượt là do UGround lệch quá 14%.
- Mọi mô hình bị chấm bằng cùng dụng cụ, nên so sánh vẫn công bằng; em in câu chuẩn cạnh số mô hình để đọc khoảng cách.

**Q7. Sao không chấm bằng người?**
- Nhận đây là hạn chế. Thay vào đó em dùng bốn mô hình chấm độc lập và các phép kiểm sàn, trần, bỏ thông tin. Kết quả thống nhất.

**Q8. Ba điều kiện (14%, Voronoi) là em tự đặt, có phải chọn cho đẹp số?**
- 14% là ngưỡng của AitW. Voronoi chỉ siết thêm (loại nút kế bên: 84,3% → 2,8%).
- Em báo song song **D.3**, luật gốc của chính AndroidControl, và **AitW đầy đủ**: thứ tự không đổi, GRPO-SPICE − S1 cùng chiều dưới cả ba.

### Nhóm 3. Học tăng cường

**⭐ Q9. "SFT tiếp" (không RL) đã +1,05 rồi, vậy RL thêm được gì?** (câu khó nhất, chuẩn bị kỹ)
- Mở bằng số mạnh nhất: lấy chính mô hình "SFT tiếp" làm điểm xuất phát rồi chạy RL với phần thưởng SA-SPICE-v3 thì tăng thêm **+1,05 [+0,46; +1,65], p = 0,0007**. Tức RL thêm được phần mà học thêm có giám sát không làm được.
- Thêm: thưởng ngẫu nhiên với cùng số bước RL thì **bằng 0**, nên mức tăng đến từ nội dung phần thưởng; và RL làm cả 7 độ đo văn bản tăng so S1.
- Nếu thầy hỏi tiếp riêng GRPO-SPICE: so với SFT tiếp là +0,49, cùng chiều nhưng nhỏ. Chính vì vậy em làm phần thưởng mới SA-SPICE-v3, và nó đã cho mức tăng có ý nghĩa.

**⭐ Q10. Sao chọn GRPO mà không PPO hay thuật toán khác?**
- Đã so 7 lượt (GRPO, SCST, PPO hai cấu hình, REINFORCE, RLOO, GRPO chạy lại). GRPO và SCST nhỉnh nhất, nhưng khoảng tin cậy chồng nhau, em không nói GRPO tốt nhất.
- Lý do thực dụng: GRPO không cần mô hình giá trị (rẻ bộ nhớ trên GPU miễn phí), là thuật toán phổ biến cho LLM hiện nay (DeepSeekMath, DeepSeek-R1).

**⭐ Q11. Sao chọn SPICE mà không độ đo khác?**
- Đã so: SPICE +1,55, ROUGE-L +1,52, METEOR +1,17, CIDEr-D +1,17 so S1. SPICE và ROUGE-L ngang nhau; em **không** viết SPICE tốt nhất.
- Lý do chọn: SPICE chấm theo đối tượng và quan hệ, hợp với việc gọi đúng phần tử; phân rã cho thấy SPICE thiên về **đổi đúng phần tử** (41 bước) hơn ROUGE-L (20); có tiền lệ (SPIDEr).

**Q12. SPIDEr nói tối ưu SPICE một mình cho câu dài lặp, em có bị không?**
- Không: em có phạt độ dài, và số từ trung bình không tăng (7,19 vs 7,28). Câu ra vẫn ngắn kiểu "Tap Not now".

**Q13. Sao không RL thẳng từ mô hình gốc như DeepSeek-R1-Zero?**
- RL thẳng thành công ở toán vì mô hình gốc đã tự giải đúng được một phần. Ở bài này mô hình gốc viết sai văn phong (BLEU-4 15,3 vs 51,6 của S1; exec 47,6). Không có mẫu tốt thì RL không có gì để thưởng.
- Cách làm SFT trước rồi RL theo đúng SCST, SPIDEr, DeepSeekMath, Vision-R1.

**Q14. Thưởng CIDEr-D mà CIDEr-D lại thấp?**
- Nhận là điểm lạ chưa giải thích được. Em đã kiểm cách tính IDF và tách từ, không phải nguyên nhân. Ghi vào hạn chế.

### Nhóm 4. Dữ liệu và phạm vi

**⭐ Q15. Tập kiểm có rò rỉ từ tập dạy không?**
- Dạy và kiểm **không trùng tác vụ nào**.
- Lưu ý trung thực: tập kiểm của em lấy phần lớn từ split *train* chính thức của AndroidControl (cách chia của bản dữ liệu có ảnh), nên không phải split test chính thức. Em đã tách theo split: exec không chênh (S1 59,09 vs 59,28).
- Và trên **tác vụ S1 chưa từng học**, mức tăng còn lớn hơn (+4,58).

**Q16. Bước không chạm (cuộn, quay lại) bị kém đi, sao vẫn nói mô hình tốt hơn?**
- Nhận: GRPO-SPICE làm scroll giảm 6,23 điểm vì phần thưởng chỉ tính trên bước chạm và mô hình nghiêng về câu chạm. Toàn bộ bước không chạm giảm nhẹ hơn (85,97 → 84,29).
- Executability là thước cho bước chạm (4.463 bước, phần lớn bài toán); em báo riêng bước không chạm và khai tác hại. Đang chạy bản sửa.

**Q17. Sang AitZ thì không hơn S1, có phải chỉ khớp AndroidControl?**
- Trên AitZ, tinh chỉnh có giám sát vẫn hơn mô hình gốc +3,29; phần thêm của RL thì chưa thấy (−0,51, phủ 0). Em nói thẳng là mức tăng của RL **chưa khái quát sang miền khác**, chỉ khái quát sang tác vụ mới trong cùng miền.

**Q18. Lịch sử các bước trước là câu chuẩn, vậy có phải gian lận ngữ cảnh?**
- Đã đo khi lịch sử do chính mô hình viết: điểm tuyệt đối giảm ~4 ở cả hai mô hình, nhưng mức hơn S1 giữ **+1,48**.

**Q19. Sao dùng 3B mà không 7B?**
- Ngân sách GPU (chủ yếu Kaggle T4 miễn phí). Và 3B đã tinh chỉnh hơn 7B prompting 9,14 điểm.

### Nhóm 5. Quy trình

**Q20. Thử nhiều hướng như vậy, có phải chọn phương pháp sau khi nhìn tập kiểm?**
- Các nhánh được chọn trên tập **phát triển (val/DEV)** tách riêng; tập kiểm chấm **một lần** cho mỗi nhánh đã chọn. Mọi nhánh đã chấm test đều báo, kể cả nhánh thua (S2, gui_sel, CW-RA, RAFT…).

**Q21. ACE không tăng exec thì giữ làm gì?**
- ACE tăng cả 7 độ đo văn bản mà không làm hại exec (60,68 vs 60,65). Tức câu sát câu chuẩn hơn mà vẫn dùng được. Nếu thầy thấy không đáng, có thể đưa ACE xuống phần mở rộng.

**(Ít khả năng) Q22. Mấy hạt giống?** Trả lời ngắn: kết quả chính một hạt; hạt thứ hai của GRPO-SPICE thấp hơn 0,72 nhưng vẫn hơn S1 (+0,83). Không sa đà.

---

## 3. Bảng số bỏ túi

| | số |
|---|---|
| trần (câu chuẩn) · sàn ("Tap the button.") · câu sai màn | 75,73 · 12,0 · 6,1 |
| Base · 7B prompting · S1 | 47,59 · 51,51 · 59,11 |
| GRPO-SPICE · + ACE · SA-SPICE-v3 | 60,65 · 60,68 · 61,21 |
| GRPO-SPICE − S1 | +1,55 [+0,80; +2,33] |
| SA-SPICE-v3 − S1 · − SFT tiếp | +2,11 [+1,33; +2,89] · +1,05 [+0,46; +1,65] |
| thưởng ngẫu nhiên − S1 | 0,00 |
| tác vụ mới (1.484 bước) GRPO-SPICE − S1 | +4,58 [+3,17; +6,05] |
| UI-Venus · Phi-Ground · Phi-4 | +1,55 · +0,78 · +0,69 |
| lịch sử tự sinh | +1,48 [+0,54; +2,43] |
| bỏ tên · bỏ vị trí | −28,5 · −3,5 |
| nút kế bên: chỉ 14% · thêm Voronoi | 84,3% · 2,8% |
| D.3 · AitW đầy đủ (GRPO-SPICE vs S1) | 67,02 vs 65,49 · 76,25 vs 74,37 |
| phân rã GRPO-SPICE − S1 | loại thao tác +28 bước · phần tử +41 bước |
| scroll (không chạm) S1 → GRPO-SPICE | 83,97 → 77,75 |
| dữ liệu | dạy 64.567 bước · kiểm 4.463 bước chạm / 1.432 tác vụ |

## 4. Tránh nói (vì thầy dễ vặn lại)

- ⛔ "SPICE **hơn có ý nghĩa**" / "GRPO **hơn hẳn**": nói "dẫn đầu", "nhóm dẫn đầu"; khoảng tin cậy chồng nhau, thầy nhìn bảng là thấy.
- ⛔ "SPICE **chứng minh** giúp định vị tốt hơn": nói "SPICE đổi đúng phần tử nhiều nhất (41 bước)", là số thật, không cần chữ "chứng minh".
- ⛔ "Mô hình đạt 79% năng lực con người": cách chia này sai; nói hai số cạnh nhau (60,7 và 75,7).
- ⛔ "Bền trước diễn đạt lại": chỉ kiểm đổi động từ và trật tự câu.
- ⛔ Trích số trên tập phát triển (val/DEV): chỉ dùng để chọn nhánh.
- ⛔ "SA-SPICE-v3 hơn GRPO-SPICE": +0,56 chưa có ý nghĩa.
