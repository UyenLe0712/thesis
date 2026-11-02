# 329. Xếp hạng độ phổ biến thuật toán RL và thứ tự chạy (1/11/2026)

**Kết luận:** chạy theo thứ tự SFT tiếp (Behavior Cloning) · REINFORCE · PPO và A2C · SCST + CIDEr-D, rồi tới phần còn lại. Thuật toán phổ biến nhất trong RL nói chung là họ Q-learning/DQN, nhưng không chạy ngay được trên câu sinh: phải viết mã, rủi ro cao, nên đi sau và cần thử trước. DDPG và TD3 rất phổ biến nhưng dành cho hành động liên tục, nên không chạy.

Bảng này trả lời "thuật toán nào phổ biến", **không** chứng minh thuật toán nào hợp bài toán này. Thứ tự chỉ quyết định chạy gì trước. Thay đổi thứ tự ở đây thắng thứ tự ưu tiên trong `report/reports/Baseline RL so với GRPO.md`; danh sách lượt và cách viết kết quả vẫn theo file đó.

## 1. Cách đếm

- **Mẫu:** 99 bài RL. 67 bài tôi chọn tay từ danh sách trích dẫn cao nhất của OpenAlex (bỏ khảo sát, ứng dụng, điều khiển kinh điển), 32 bài tôi thêm vì nổi tiếng mà truy vấn tiêu đề không bắt được. **Có yếu tố chọn tay, không phải tổng quan hệ thống.**
- **Đọc được:** 93 bài toàn văn từ arXiv. 6 bài không tìm thấy trên arXiv theo tiêu đề, trong đó có AlphaZero, AlphaStar, DPG, R2D2.
- **Đếm:** một bài được tính nếu nhắc tên thuật toán từ 2 lần trở lên trong phần trước tài liệu tham khảo. Không đếm bài gốc của chính thuật toán đó, nên mẫu số là 91–93.
- **Trích dẫn:** số của OpenAlex lấy ngày 1/11/2026.
- **Giới hạn:** nhắc tên không có nghĩa là dùng làm mốc so; mẫu nghiêng về 2013–2021; khớp theo mẫu chữ có thể bắt nhầm (`BC`, `Rainbow`); bài mới và preprint bị đếm thiếu trích dẫn. Trích dẫn của DeepSeekMath (101) rõ ràng thấp, GSPO khớp nhầm bài khác, nên hai số này không dùng. Số trong file này **chỉ để sắp thứ tự, không đưa vào luận văn** trừ khi kiểm lại.

Tái lập: `runs/pho_bien_rl/` (`dem.py` tải và đếm, `dem2.py` đếm lại sau khi sửa lỗi hoa thường, `dem_100_bai.json` là số từng bài).

## 2. Độ phổ biến

Cột "Nhắc ≥ 2 lần" là số bài trên khoảng 92. Ba hàng cuối cột đầu ghi "(họ)" là cụm từ chung, không phải một thuật toán.

| Thuật toán | Nhắc ≥ 2 lần | Trích dẫn bài gốc | Chạy được ở bài này? |
|---|---:|---:|---|
| DQN | 41 | 30.374 (Nature 2015) | Khó, xem mục 3 |
| DDPG | 23 | 10.767 | **Không**: hành động liên tục |
| PPO | 23 | 10.618 | Có, phải viết mã |
| TRPO | 20 | 4.363 | Khó, ghi lại cho Colab |
| SAC | 18 | 5.586 | Khó, chỉ có bản rời rạc |
| A3C / A2C | 16 / 3 | 7.126 | A2C có, phải viết mã; A3C để A2C đại diện |
| Behavior Cloning | 14 | không tra | **Có**, chính là SFT tiếp |
| DPG | 14 | không tra | **Không**: hành động liên tục |
| Double DQN / Rainbow | 12 / 10 | không tra | Không riêng; là cải tiến của DQN |
| NPG | 7 | không tra | Đi cùng TRPO |
| REINFORCE | 6 | 6.997 (Williams 1992) | **Có**, mã đã xong và đang chạy một bản |
| TD3 | 6 | 3.650 | **Không**: hành động liên tục |
| CEM | 5 | 902 | **Có**, mã đã xong |
| GAE | 4 | 2.012 | Đi cùng PPO |
| CQL / BCQ / IQL | 3 / 3 / 1 | 725 / không tra / 209 | Khó; ILQL đại diện |
| AWR, AWAC | 2 | 158 (AWR) | Bản rút gọn, mã đã xong |
| Decision Transformer | 2 | 623 | Quark đại diện |
| ES | 1 | 968 | Bản xếp hạng mã đã xong; ES đủ phải viết |
| GAIL | 0 | không tra | Không chạy |
| (họ) Policy gradient | 53 | | |
| (họ) Q-learning | 47 | | |
| (họ) Actor-critic | 42 | | |

Các phương pháp của riêng mảng sinh văn bản ít xuất hiện trong mẫu RL chung, nên tra trích dẫn: SeqGAN 2.342 · SCST 2.178 · InstructGPT 4.208 (PPO + SFT) · DeepSeek-R1 1.701 (GRPO) · MIXER 937 · DPO 694 · Bahdanau 423 · MRT 376 · RAML 126 · ORPO 118 · Quark 51 · softmax PG 23 · ILQL 9. Tỉ lệ dùng làm mốc trong mảng này ở mẫu 153 bài: GRPO 36/42 bài RLVR · PPO 16/30 và SFT 20/30 bài RLHF · DPO ngoại tuyến 15/30 · SCST 13 bài chú thích ảnh.

## 3. Debate

**"Cứ xếp đúng theo độ phổ biến":** DQN đứng đầu mọi cột, thầy làm RL sẽ tìm dòng này trước. Nhưng DQN cần Q(s, a) cho 151.936 token ở mỗi vị trí, phần thưởng chỉ có ở cuối câu, và logits của S1 không phải giá trị Q nên thang đo lệch hẳn thưởng trong [0, 1]. Làm trước tiên thì rủi ro tốn nhiều tuần mà không ra số. **Chốt:** giữ DQN ở nhóm quan trọng nhưng đi sau, thử nhỏ trước.

**"Chỉ cần mốc của đúng mảng":** tiêu chí này đặt GRPO, DAPO, SCST lên đầu và bỏ DQN, SAC, TRPO. Thầy đã yêu cầu so rộng hơn, và mẫu 153 bài được gieo từ GRPO nên tự nó thiên về họ này. **Chốt:** dùng cả hai nguồn. Thuật toán phổ biến ở cả RL chung lẫn mảng sinh văn bản (PPO, REINFORCE, Behavior Cloning) đi trước.

**"Thuật toán phổ biến nhưng không áp dụng được thì sao?"** DDPG, TD3, DPG đứng cao nhưng ép chạy phải thêm phép nới liên tục, khi đó không còn là thuật toán gốc và số không đại diện được cho chúng. **Chốt:** không chạy, trình lý do. Câu này dễ bảo vệ hơn một dòng số vô nghĩa.

**"Các phương pháp ít phổ biến có đáng chạy không?"** AWR, RAML, xếp hạng kiểu ES đều ít trích dẫn. Chi phí viết gần như bằng 0 vì mã đã xong, nhưng vẫn tốn 20,6 giờ mỗi lượt. **Chốt:** chạy sau các lượt phổ biến, không chạy trước chỉ vì dễ.

**Rủi ro chung:** nhiều dòng không tự làm kết luận mạnh hơn. Chạy nhiều phương pháp yếu hay cài đặt hời hợt thì ck500 thắng cũng không chứng minh gì; thuật toán nổi tiếng phải được cài đúng, và bản rút gọn phải khai là bản rút gọn. Lượt PPO quan trọng hơn năm lượt phụ cộng lại.

## 4. Thứ tự chạy trên Kaggle

Đang chạy (không đổi): SCST, RLOO, REINFORCE EMA + SPICE · GRPO + CIDEr-D, METEOR, ROUGE-L.

| Đợt | Lượt | Lý do | Trạng thái mã |
|---|---|---|---|
| **1** | **GRPO bỏ chia std (K1) và lượt A/A `grpo:spice:101` qua `grpo_luoi.py`** (thêm sau `report/328`) | Không phải vì phổ biến: RLOO, REINFORCE, SCST đổi cả mốc lẫn chia std nên thiếu K1 thì chưa đọc được; ck500 chạy bằng mã khác nên cần A/A làm mốc cùng mã | Xong |
| **1** | SFT tiếp (Behavior Cloning) | Phổ biến ở cả hai nguồn; chặn đòn "chỉ là học thêm" | Sửa từ `ra_train.py` |
| **1** | REINFORCE không mốc (`vanilla`) | Thuật toán gốc của họ policy gradient | Xong |
| **1** | PPO λ=1,0 và λ=0,95, A2C | Phổ biến ở cả hai nguồn; câu trả lời cho UI-TARS-2 | Chưa viết, phải đo VRAM; tràn thì chuyển mục 5 |
| **1** | SCST + CIDEr-D | Chuẩn của chú thích ảnh | Bỏ phép chặn |
| **1** | Đo hình thức câu (không train) | Rẻ, trả lời nhận xét của Liu về SPICE thuần | Viết mới, ngắn |
| **2** | GRPO + BLEU-4, SPIDEr, BERTScore, BCMR, SPICE có cổng loại thao tác, tên phần tử + loại thao tác, chrF (theo `report/330` §7) | Trục phần thưởng, câu hỏi 2 của thầy | Có sẵn: BLEU-4, SPIDEr, chrF, BERTScore (chưa probe). Phải viết: BCMR và hai thưởng mới |
| **2** | Cải tiến cùng họ: bỏ chia std · DAPO lõi · Dr. GRPO · GRPO gộp theo câu | Mốc mặc định của RLVR | Xong hoặc một cờ; cần probe |
| **3** | DPO trực tuyến và ngoại tuyến từ S1 · RFT một vòng và online · ORPO · CEM | Mốc của RLHF và của bài gốc GRPO | Sửa từ mã cũ; `rft`, `cem` xong |
| **3** | Thử nhỏ DQN / soft Q trên logits (20 bước, 1 phiên) | Họ phổ biến nhất; chỉ chạy đủ 500 bước nếu qua thử | Chưa viết; [suy] dùng adapter làm mạng đích nên có thể vừa T4; rủi ro cao |
| **4** | SeqGAN · MIXER rút gọn · trộn RL + CE · MRT · Quark · ES | Cổ điển của mảng sinh văn bản | Chưa viết |
| **4** | Kiểu AWR · kiểu RAML · xếp hạng · `mad` · chuẩn hoá theo lô · GPG · GSPO, Clip-Higher, μ=2 | Ít phổ biến hơn | Phần lớn xong hoặc một cờ |
| **4** | Độ nhạy: G=4, G=16, xuất phát từ Base · DAPO đủ | Câu hỏi tiếp theo, không phải mốc | Một cờ hoặc viết thêm |

**Đọc kết quả (theo `report/328` §2):** với khoảng 50 phép so, Holm đòi p < 0,001 ở phép đầu, tương ứng |Δ| cỡ 1,0–1,8, nên ngưỡng |Δ| ≥ 1 chưa đủ khi đã hiệu chỉnh. Nên xong các lượt đợt 1 rồi mới đọc các phương pháp cổ điển.

Khoảng 9 tuần nếu chạy hết (đầu tháng 1/2027). Hết thời gian thì đợt 4 là phần cắt được, đợt 1 không cắt được.

## 5. Cần Colab hoặc chưa chắc vừa T4: ghi lại, user quyết

Lý do là [suy] từ cấu trúc thuật toán, chưa đo. Xếp theo mức quan trọng, đã tính độ phổ biến mới.

| Thứ tự | Phương pháp | Vì sao có thể cần Colab | Mức quan trọng |
|---|---|---|---|
| 1 | PPO critic đủ cỡ (và PPO đầu nhỏ nếu probe tràn) | Thêm một mô hình giá trị | **Rất cao** |
| 2 | TRPO (kèm NPG) | Đạo hàm bậc hai và nhiều lần lặp liên hợp mỗi bước, khó đi với gradient checkpointing và fp16; có thể chậm gấp nhiều lần | **Cao**: 20 bài, tổ tiên của PPO |
| 3 | DQN / soft Q đủ cỡ nếu thử nhỏ không vừa T4 | Q cho toàn từ vựng, mạng đích | **Cao**: phổ biến nhất, nhưng rủi ro không học |
| 4 | SAC rời rạc | Hai đầu Q, mạng đích, replay | Trung bình (nâng từ thấp): 18 bài, nhưng bản rời rạc là preprint |
| 5 | ILQL | Đầu Q, V và mạng đích; học offline | Trung bình: đại diện offline RL cho ngôn ngữ, ít trích dẫn |

## 6. Không chạy

DDPG, TD3, DPG: hành động liên tục. A3C: A2C đại diện. Double DQN, Rainbow: cải tiến trên DQN, chỉ xét nếu DQN học được. GAIL: không dùng được phần thưởng SPICE, và SeqGAN đã đại diện dạng đối kháng. Decision Transformer: Quark đại diện.
