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

### Trạng thái đợt 1, cập nhật 3/11 (thắng cột trạng thái mã ở bảng trên)

| Thứ tự làm sau 7/11 | Lượt | Trạng thái | Việc còn lại |
|---|---|---|---|
| 1 | SFT tiếp | Train đủ 500 bước (`luoi-t2-3`) | Sinh câu + chấm test |
| 2 | PPO λ=1,0 và λ=0,95, A2C | Mã xong (`harness/grpo_ppo.py`), **đã probe T4 3/11** (xem dưới), PPO λ=0,95 chưa probe nhưng cùng cỡ bộ nhớ | Cập nhật dataset script (đã sửa log), rồi train |
| 3 | GRPO bỏ chia std (K1) | Mã xong, chưa chạy | Train + test |
| 4 | Lượt A/A `grpo:spice:101` | Dừng ở trần, khoảng bước 183, điểm lưu 175 | Nối tiếp tới 500, rồi test |
| 5 | SCST + CIDEr-D | Mã cho phép (`harness/grpo_codien.py`), chưa probe | Train + test |
| 6 | REINFORCE không mốc (`vanilla`) | Mã xong, chưa probe | Train + test |
| | RLOO, REINFORCE EMA + SPICE | Đủ 500 bước | Sinh câu + chấm test |
| | SCST + SPICE, GRPO + METEOR, ROUGE-L, CIDEr-D | **Đã có số test**, `report/320` mục 14 | Đã đủ 4.463 bước; phân rã và diễn biến train ở `report/320` mục 14.5–14.6 |
| | Đo hình thức câu | Đã có cho các nhánh cũ (`runs/hinh_thuc_cau/`) | Đã đo bốn lượt có số test (`report/320` mục 14.7); còn các lượt chưa test |

**Probe PPO và A2C, 3/11** (`trangphngngc/luoi-probe-ppo`, T4×2, mỗi lượt một GPU, S1 + SPICE, seed 101, 50 câu nhắc, trần 0,65 h; log `runs/luoi/probe_ppo/`). Cả hai dừng ở trần như dự kiến (mã thoát −15), không có Traceback hay tràn bộ nhớ, không có `nan` trong số train.

| | PPO λ=1, μ=2 | A2C λ=1 |
|---|---|---|
| Đã chạy | 12 bước (6 lô sinh) | 10 bước (10 lô sinh) |
| Thời gian một lô sinh | 209 s + 90 s lặp lại = 299 s | 187 s |
| Giữ 1.000 câu nhắc | 1.000 bước, khoảng 41 h một GPU [suy] | 500 bước, khoảng 26 h một GPU [suy] |
| Bộ nhớ đã giữ, hai GPU, theo `nvidia-smi` | 13.847 và 14.267 MiB, log không ghi GPU nào của lượt nào | |
| `clip_ratio/region_mean` | 0 ở mọi dòng | 0 (μ=1 nên không thể khác) |

Mốc so: ck500 160,6 s/bước ở probe 29/9, GRPO + CIDEr-D 149,1 và SCST + SPICE 158,1 ở probe 1/11. A2C chậm hơn ck500 khoảng 17%, [suy] do thêm một lượt lan truyền để lấy trạng thái ẩn; hai probe khác ngày nên con số chỉ để ước giờ. `nvidia-smi` đo bộ nhớ đã giữ, không phải đỉnh cấp phát. Probe không chọn mẫu dài nhất, nên chưa loại được tràn bộ nhớ ở chuỗi dài; biên còn khoảng 0,6 GiB so với 14,56 GiB dùng được của T4.

Bốn điều đọc được:

1. Clip chưa hoạt động lần nào. Warmup kéo lr lên 1e-5 ở bước 10, nên chỉ hai dòng cuối chạy ở lr đầy đủ. Loss ở vòng lặp thứ hai lớn nhất cỡ 1e−3 về độ lớn, gợi ý tỉ số xác suất mới/cũ chỉ lệch khoảng đó, còn ngưỡng clip là 0,2 [suy]. Nếu lượt đầy đủ vẫn 0, PPO μ=2 ở lr 1e-5 về cơ chế chỉ là A2C cập nhật hai lần mỗi lô, khi viết phải khai đúng vậy và không được nói "tác dụng của clip".
2. Đầu giá trị có học: `v_loss` của PPO từ 0,88 xuống dải 0,06–0,30, nhưng còn nhiễu và 12 bước chưa cho biết có hội tụ không. `v_ev` trong probe không đọc được vì một lô 4 mẫu có thể cùng đích (ra −8e5), đã đổi sang đo trên 64 lô gần nhất.
3. Thưởng và độ dài câu của hai lượt trùng nhau tới 4 chữ số ở 6 lô đầu. Đây không phải dấu hiệu lạc cấu hình: `grad_norm`, `kl` và `v_loss` có khác, chung seed và lr warmup rất nhỏ nên mẫu sinh còn giống nhau [suy].
4. Chữ `|A| nan` và số thưởng thấp ở dòng theo dõi của PPO là lỗi hiển thị: dòng của vòng lặp thứ hai không có hai trường này. Ngoài ra `luoi/adv_abs_mean` trong probe là trung bình lẫn lợi thế tạm của lớp cha với lợi thế thật, `luoi/frac_adv_zero` là của lớp cha. Đã sửa `harness/grpo_ppo.py` và `_bundles/luoi/make_nb.py`, chỉ đụng phần ghi log, không đổi phép train; selftest GAE chạy lại trên CPU vẫn đạt, chưa chạy lại trên T4.

Thứ tự này là đề xuất 3/11: SFT tiếp đứng đầu vì rẻ nhất và tách được công của RL với công của việc train thêm; PPO đứng thứ hai vì mục 3 đã chốt "lượt PPO quan trọng hơn năm lượt phụ cộng lại". Họ chính để đọc Holm vẫn theo `report/320` mục 13.

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

## 7. Ghi chú về SCST, phải khai khi viết

- **SCST là gì:** *Self-Critical Sequence Training* (Rennie và cộng sự, CVPR 2017), REINFORCE với mốc là điểm của câu greedy trên cùng đầu vào. Trong mẫu 153 bài, SCST là mốc của mảng chú thích ảnh (13 bài), không phải mốc mặc định của RLVR hay RLHF.
- **Lượt của dự án không phải SCST gốc.** Theo log `runs/luoi/lo1/luoi-u-1/scst_spice_101.train.log`, lượt này giữ khung của ck500: G = 8, β = 0,04 (phạt KL), `num_iterations` = 1, 500 bước, chỉ đổi lợi thế thành r − r(câu greedy) như `harness/grpo_luoi.py`. Phải viết là "mốc greedy kiểu SCST trong khung GRPO", không viết "SCST" trần khi so với tài liệu.
- **Ai so GRPO với SCST:** Liang, *GRPO for Image Captioning* (arXiv 2503.01333, preprint), so với CE và SCST trên CIDEr. Bài gốc GRPO (DeepSeekMath) không phải: hình so sánh của bài đó có RFT và Online RFT; PPO chỉ xuất hiện ở phần suy dẫn, phép so trực tiếp với PPO có ở DeepSeek-R1. Các điều này đọc từ ghi chú khảo sát, phải mở bài gốc trước khi trích.
- **Khoảng trống:** ghi chú nhóm chú thích ảnh không thấy phép so bốn chiều SCST, REINFORCE, PPO, GRPO cùng mô hình và cùng phần thưởng.
