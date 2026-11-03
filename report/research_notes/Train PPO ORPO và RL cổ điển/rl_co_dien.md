# Thuật toán RL cổ điển và phổ biến áp dụng được tới đâu cho Qwen2.5-VL-3B + LoRA, thưởng câu cuối câu (tra 3/11/2026)

Bối cảnh áp dụng: Qwen2.5-VL-3B, LoRA khoảng 15 triệu tham số ([report/151:104](../../151_BAN_CHOT_CUOI_PHUONG_PHAP_VA_THUOC_7_9.md) ghi 14.966.784), từ vựng 151.936 token, thưởng SPICE hoặc CIDEr-D chỉ có ở cuối câu, câu ngắn (khoảng 7 từ theo `CLAUDE.md`). Số đo máy của dự án: khoảng 150 s/bước và 12,71 GiB cho lượt sinh + chấm SPICE trên T4, 13,4 s/bước và 10,94 GiB cho SFT tiếp ([report/326](../../326_BAN_GIAO_LUOI_RL_1_11.md)). Không đếm lại độ phổ biến; bảng đếm ở [report/329](../../329_XEP_HANG_PHO_BIEN_RL_VA_THU_TU_CHAY_1_11.md).

Nhãn: **[suy]** là suy luận của tôi, chưa đo. **[nhớ]** là biết từ trí nhớ, chưa mở nguồn trong lượt này. Mọi số khác lấy từ tệp PDF hoặc trang nguồn đã mở.

## Mỗi thuật toán: có áp dụng được không, phải sửa gì, tiền lệ, số, còn xứng với tên không

### Takeaway
Có thật trên văn bản: REINFORCE, MIXER, SCST, actor-critic, PPO, MRT, RAML, softmax PG, SeqGAN, soft Q (PCL), ILQL, Quark, ES. Chỉ giữ được tên khi đổi tên: DQN, SAC, DPG. Không chạy được đúng nghĩa trên token: DDPG, TD3. TRPO có trong thư viện RL4LMs nhưng tôi không thấy bài nào báo số.

### Cited Findings

**Bảng tổng hợp.** Cột cuối là đánh giá của tôi [suy]; các cột khác có nguồn ở danh sách bên dưới.

| Thuật toán (venue) | Áp dụng | Phải sửa gì | Tiền lệ văn bản | Tên còn đúng khi nào [suy] |
|---|---|---|---|---|
| REINFORCE (Machine Learning 1992) | Có | Không cần sửa | SCST, Bahdanau, RLOO | Đúng, khai rõ mốc và phạt KL |
| A2C/A3C (ICML 2016) | Có | Đầu giá trị trên token | Bahdanau, Chen & Bansal (A2C) | "A2C" đúng nếu critic thật; A3C chỉ khác cách chạy song song |
| TRPO (ICML 2015) | Được, phải đo | Fisher-vector trên LoRA | Chỉ có mã trong RL4LMs, không thấy số | Đúng nếu có ràng buộc KL cứng, CG, line search |
| NPG (NIPS 2001) | Được, phải đo | Như TRPO, bỏ line search | ISOPO (preprint) xấp xỉ | "xấp xỉ NPG" nếu Fisher hạng thấp |
| PPO (arXiv 2017, không venue) | Có | Đầu giá trị, μ ≥ 2, GAE | RL4LMs, Quark, InstructGPT | Đúng nếu clip thật sự hoạt động |
| DQN/Double/Rainbow (Nature 2015, AAAI 2016, AAAI 2018) | Không đúng nghĩa | Logits làm Q | AE-DQN chỉ loại hành động trong game chữ | Chỉ đúng khi có max cứng, replay, mạng đích, ε-greedy |
| Soft Q / PCL (arXiv 2017, NIPS 2017) | Có | Logits làm Q | Guo Findings EMNLP 2022, GFlowVLM CVPR 2025 | Đúng, nên khai là soft Q chứ không phải DQN |
| SAC rời rạc (ICML 2018; bản rời rạc là preprint) | Rất đắt | Hai đầu Q cho cả từ vựng | Không thấy bài nào | Không; bỏ actor riêng thì thành soft Q |
| DDPG/TD3/DPG (ICLR 2016, ICML 2018, ICML 2014) | Không trên token | Nới liên tục hoặc đổi MDP | Gu EMNLP 2017 đổi MDP | Chỉ đúng khi hành động là vector ẩn |
| ILQL (ICLR 2023) | Có, ngoại tuyến | Thêm V, Q, mạng đích; sửa suy luận | Chính bài | Đúng nếu giữ cả ba mạng |
| CQL / IQL (NeurIPS 2020 / ICLR 2022) | Theo ILQL | Bản theo token | Hàng CQL trong ILQL | "theo token" |
| Decision Transformer (NeurIPS 2021) / Quark (NeurIPS 2022) | Có | Token thưởng trong câu nhắc | Hàng DT trong ILQL; Quark | Quark đúng nếu có kho mẫu + token phân vị; DT không đúng vì chỉ có một thưởng cuối |
| CEM | Có ở dạng câu | Giữ câu tốt nhất, SFT lại | ILQL gọi là filtered fine-tuning | Không phải CEM trên tham số; gọi là chọn lọc câu kiểu CEM |
| ES (arXiv 2017) | Có | Nhiễu trên LoRA | Qiu ICML 2026 | Đúng nếu là nhiễu tham số, không backprop |
| AWR (preprint 2019) | Có | Trọng số mũ trên mẫu | ILQL (AWR) | "kiểu AWR" khi không có replay |
| MIXER (ICLR 2016) | Có | Bước curriculum thừa với mô hình đã SFT | SCST so trực tiếp | "MIXER" chỉ khi có curriculum; không có thì là REINFORCE + mốc học được |
| SCST (CVPR 2017) | Có | Không cần sửa | Chính bài | Bản dự án: "mốc greedy kiểu SCST trong khung GRPO" |
| Actor-critic Bahdanau (ICLR 2017) | Có nhưng đắt | Critic Q nhìn câu chuẩn, mạng đích, phạt phương sai | Chính bài | Chỉ đúng khi tính kỳ vọng trên cả từ vựng |
| SeqGAN (AAAI 2017) | Có nhưng đổi thưởng | Bộ phân biệt thay SPICE | Chính bài | Thưởng SPICE thì không còn là SeqGAN |
| MRT (ACL 2016) | Có | G nhỏ hơn nhiều | Chính bài | Đúng |
| RAML (NIPS 2016) | Khó | SPICE không lấy mẫu trực tiếp được | Chính bài | "kiểu RAML" |
| Softmax PG (NIPS 2017) | Khó với SPICE | Cần thưởng từng token | Chính bài | Đúng với CIDEr, khó với SPICE |
| GAIL (NIPS 2016) | Không phục vụ câu hỏi | Bỏ SPICE | SeqGAN cùng dạng | Không cần chạy |

**Họ policy gradient theo câu**
- SCST so trực tiếp trên COCO (FC-2K, tối ưu CIDEr): XE 90,9; XE beam 94,0; MIXER-B 101,9; MIXER 104,9; SCST 106,3 — [Rennie et al.](https://arxiv.org/abs/1612.00563). Venue CVPR 2017 lấy từ [ghi chú dự án](../Baseline%20RL%20so%20với%20GRPO/caption_textgen_rl.md), PDF arXiv không in venue.
- Att2all, 4 hạt giống: REINFORCE 110,4 ±0,5; REINFORCE + mốc học được (MIXER bỏ curriculum) 113,2 ±0,2; SCST 113,8 ±0,3. Bài kiểm định lợi thế của SCST so MIXER bỏ curriculum ở α = 0,1, trừ ROUGE — [Rennie et al.](https://arxiv.org/abs/1612.00563).
- Cùng bài nhận thấy curriculum không cần thiết với SCST và REINFORCE có mốc học được trên COCO: tắt đi vẫn cho kết quả bằng hoặc tốt hơn, và nhanh hơn — [Rennie et al.](https://arxiv.org/abs/1612.00563).
- Trong RLHF, REINFORCE hơn PPO 3,2% đến 20,3% về win-rate trên mọi cặp dữ liệu và mô hình; RLOO hơn PPO, DPO, RAFT — [Ahmadian et al., ACL 2024](https://aclanthology.org/2024.acl-long.662.pdf).
- MRT: BLEU trên MT06 tăng 30,70 → 37,34 so MLE (RNNsearch), MT02 35,13 → 40,36. MRT dùng tập con mẫu và phân phối Q ∝ P^α chuẩn hoá trên tập con đó — [Shen et al.](https://arxiv.org/abs/1512.02433), [ACL 2016](https://aclanthology.org/P16-1159/).
- Softmax PG, tiêu đề Gigaword-10K ROUGE-L: MLE 35,2; RAML 36,4; SPG tốt nhất 37,8. Chú thích ảnh CIDEr: MLE 0,968; RAML 0,997; SPG tốt nhất 1,033. Từ vựng trong thí nghiệm tiêu đề là 220 nghìn từ. Bài dùng số gia thưởng R(z₁:ₜ) − R(z₁:ₜ₋₁) nên cần metric tính được trên tiền tố — [Ding & Soricut, NIPS 2017](https://arxiv.org/abs/1709.09346).
- RAML huấn luyện trên mẫu tỉ lệ với exp(thưởng/τ), bài cho ví dụ cụ thể với khoảng cách chỉnh sửa — [Norouzi et al., NIPS 2016](https://arxiv.org/abs/1609.00150).

**Họ actor-critic**
- IWSLT greedy (BLEU): LL 19,33; REINFORCE 20,92; RF-C 22,24; AC 21,66. MIXER của bài gốc 20,73 nhưng mốc LL của bài đó yếu hơn 1,6 điểm nên tác giả dặn phải thận trọng. Bản encoder hai chiều: RF-C 27,42; RF-C+LL 27,7; AC 27,27; AC+LL 27,49. WMT14 greedy: LL 29,33; AC+LL 30,85; RF-C+LL 29,83 — [Bahdanau et al., ICLR 2017](https://arxiv.org/abs/1607.07086).
- Tác giả viết rõ phương pháp tốt nhất trên IWSLT lại là REINFORCE có critic, không phải actor-critic — [Bahdanau et al.](https://arxiv.org/abs/1607.07086).
- Để chạy được, bài cần mạng đích (γθ = 1,0 thì "không chạy"), phạt phương sai của critic, delayed actor, và reward shaping — [Bahdanau et al.](https://arxiv.org/abs/1607.07086).
- Actor-critic so self-critical trên COCO dev: 1,162 và 1,140 CIDEr-D, preprint, hai bên không cùng hẳn kiến trúc — [ghi chú dự án](../Baseline%20RL%20so%20với%20GRPO/caption_textgen_rl.md), [Zhang et al.](https://arxiv.org/abs/1706.09601).
- A2C trong tóm tắt: [Chen & Bansal, ACL 2018](https://aclanthology.org/P18-1063/) (theo ghi chú dự án, không đọc lại trong lượt này).

**PPO trên mô hình ngôn ngữ**
- RL4LMs nói có cài PPO, TRPO, A2C, NLPO cho mô hình ngôn ngữ, nhưng kết quả GRUE báo năm nhánh: Supervised, PPO, Supervised+PPO, NLPO, Supervised+NLPO. Thứ tự trong khảo sát người: Supervised+NLPO > Supervised ≥ Supervised+PPO > NLPO ≥ PPO > Zero-shot — [Ramamurthy et al., ICLR 2023](https://arxiv.org/abs/2210.01241).
- Bài này có chỗ khai Supervised thắng Supervised+PPO ở 2/5 tác vụ theo đánh giá người dù metric tự động nói ngược, và tác giả coi đó có thể là reward hacking — [Ramamurthy et al.](https://arxiv.org/abs/2210.01241).
- Quark so PPO có phạt KL, RealToxicityPrompts: avg. max toxicity 0,218 và 0,196; xác suất 0,044 và 0,035; perplexity 14,27 và 12,47 — [Lu et al., NeurIPS 2022](https://arxiv.org/abs/2205.13636).
- Trên Countdown với Qwen2.5-3B: PPO-z 20,1; GRPO-z(8) 30,9; GRPO-z(30) 32,5; GRPO-v 37,8; Dr.GRPO-v 43,8; ES 60,5. Đây là số tự báo của tác giả ES, PDF in ICML 2026 (PMLR 306), OpenAlex lúc tra mới thấy arXiv — [Qiu et al.](https://arxiv.org/abs/2509.24372).

**Ngoại tuyến**
- Bảng 3 của ILQL, Visual Dialogue "y/n", điểm tốt nhất và độ lệch theo siêu tham số: ILQL −5,57 (σ 0,46); single-step RL −5,91 (0,35); DT −6,70 (1,15); CQL theo token −7,32 (1,98); filtered fine-tuning −7,48 (0,72); ψ-learning −10,05 (0,60); fine-tuning −10,85 — [Snell et al., ICLR 2023](https://arxiv.org/abs/2206.11871).
- Trích xuất chính sách từ cùng hàm giá trị: ILQL −5,57 (σ 0,46); AWR −5,96 (σ 2,82); GOLD −7,58 (σ 0,61) — [Snell et al.](https://arxiv.org/abs/2206.11871). Tức AWR gần bằng khi chỉnh tốt nhưng rất nhạy.
- ILQL gồm ba mạng: πβ, mạng giá trị với hai đầu Q và V, mạng đích Polyak. Lúc suy luận lấy mẫu bằng cách nhiễu log-prob của πβ bằng giá trị đã học, không có actor riêng — [Snell et al.](https://arxiv.org/abs/2206.11871).
- Ghi chú dự án trước đây gọi venue của ILQL, RL4LMs là chưa xác minh tận nguồn. Hai PDF đều in "Published as a conference paper at ICLR 2023" và trang [ICLR](https://iclr.cc/virtual/2023/oral/12652) có RL4LMs (oral).

**Không gradient**
- Qiu et al. tự báo ES hơn PPO và GRPO trên các mô hình 0,5B đến 8B, không cần backprop, ít tốn bộ nhớ hơn, ít bị reward hacking hơn; và nêu cỡ quần thể rất nhỏ so với các bài ES trước — [Qiu et al.](https://arxiv.org/abs/2509.24372). Bài blog cùng nhóm sau đó nói ES chỉ cạnh tranh được, không hẳn hơn, trên bài toán toán khó — [Medium](https://medium.com/@evolutionmlmail/evolution-strategies-at-scale-fine-tuning-harder-tasks-b4f29be26ae7); nguồn yếu.
- ESO theo nguyên lý ES với loss cross-entropy, tự báo ngang PPO trên bài toán căn chỉnh — [COLING 2025](https://aclanthology.org/2025.coling-main.357.pdf) (chỉ từ tóm tắt tìm kiếm).

**Đối kháng**
- SeqGAN: thơ Trung Quốc, điểm người MLE 0,4165 và SeqGAN 0,5356; BLEU-2 0,6670 và 0,7389 — [Yu et al., AAAI 2017](https://arxiv.org/abs/1609.05473).
- LeakGAN báo NLL dữ liệu tổng hợp độ dài 20: MLE 9,038; SeqGAN 8,736; RankGAN 8,247; LeakGAN 7,038 — [Guo et al., AAAI 2018](https://arxiv.org/abs/1709.08624).
- Nhưng khi đo trên toàn bộ dải chất lượng/đa dạng bằng nhiệt độ softmax, MLE vượt các biến thể GAN — [Caccia et al., ICLR 2020](https://arxiv.org/abs/1811.02549). Đây là phản bác cần ghi kèm mỗi khi nhắc SeqGAN.

### Inferences
- [suy] SCST hơn REINFORCE trong bảng chính bài; MIXER bỏ curriculum chỉ kém SCST 0,6 CIDEr, còn REINFORCE trần kém 3,4. Phần lớn mức tăng do mốc tốt, không do tên thuật toán. Bahdanau cũng vậy: có critic hơn không critic, nhưng critic dùng cách nào thì không ổn định chiều thắng. Điều này giải thích vì sao lưới của dự án dễ ra các hiệu số nhỏ.
- [suy] MIXER đầy đủ không có lý do chạy trên S1: S1 đã SFT, và curriculum tồn tại để khởi động mô hình chưa có chính sách tốt. Hàng "MIXER rút gọn" trong `report/329` thực chất là REINFORCE + mốc học được. Chạy A2C với mốc học được theo token đã gần trùng hàng này, nên có thể bỏ MIXER mà không mất thông tin. Câu trả lời trung thực là trích bảng của Rennie.
- [suy] Softmax PG và Bahdanau đều dùng số gia thưởng trên tiền tố. CIDEr-D tính được trên tiền tố, SPICE phải dựng đồ thị bằng Java cho từng tiền tố nên đắt và không ổn định về cú pháp. Vậy shaping theo tiền tố chỉ hợp lý với CIDEr-D.
- [suy] MRT trên dự án với G = 8 cách xa điều kiện gốc nếu bài gốc dùng tập mẫu lớn. Tôi nhớ S = 100 [nhớ], chưa mở lại đúng dòng.
- [suy] SeqGAN thay SPICE thành bộ phân biệt nên hiệu số so ck500 lẫn thuật toán và thưởng. Phải đọc như một phép đo về thưởng, không phải về thuật toán.

### Gaps
- Tôi không tìm thấy bài nào báo số TRPO trên mô hình ngôn ngữ, cả trong RL4LMs (chỉ nhắc một lần ở phần thư viện). A2C cũng không thấy hàng kết quả trong bảng tổng của bài đó.
- Bảng số của MIXER tôi không trích được từ PDF. Dùng lại bảng trong SCST và Bahdanau.
- Venue CVPR 2017 của SCST lấy qua ghi chú dự án. Double DQN, Rainbow (AAAI), IQL (ICLR 2022), Mnih (Nature 2015) lần này tôi không xác nhận được ở trang nguồn; các truy vấn Crossref trả về bản ghi không đúng, DBLP và OpenReview bị chặn. Đã xác nhận: [TRPO](https://proceedings.mlr.press/v37/schulman15.html), [A3C](https://proceedings.mlr.press/v48/mniha16.html), [DPG](https://proceedings.mlr.press/v32/silver14.html), [TD3](https://proceedings.mlr.press/v80/fujimoto18a.html), [SAC](https://proceedings.mlr.press/v80/haarnoja18b/haarnoja18b.pdf), [CQL](https://proceedings.neurips.cc/paper/2020/hash/0d2b2061826a5df3221116a5085a6052-Abstract.html), [DT](https://proceedings.neurips.cc/paper/2021/hash/7f489f642a0ddb10272b5c31057f0663-Abstract.html), [GAIL](https://proceedings.neurips.cc/paper/2016/hash/cc7e2b878868cbae992d1fb743995d8f-Abstract.html), [NPG](https://proceedings.neurips.cc/paper/2001/hash/4b86abe48d358ecf194c56c69108433e-Abstract.html), [PCL](https://proceedings.neurips.cc/paper/2017/hash/facf9f743b083008a894eee7baa16469-Abstract.html), [DDPG qua arXiv trỏ DBLP ICLR 2016](https://arxiv.org/abs/1509.02971).
- Tôi tra TextGAIL bằng một mã arXiv nhớ sai, nên không có thông tin đáng tin về bài đó.

## DQN và SAC: trở ngại thật là gì, logits có làm Q được không, thí nghiệm nhỏ nào bảo vệ được

### Takeaway
Logits **có** làm Q được, và đó là cách đã công bố: Guo et al. (Findings of EMNLP 2022) đặt thẳng Qθ(s, a) ≡ logit. Vì vậy lý do "logits của S1 không phải giá trị Q" trong `report/329` §3 cần sửa. Trở ngại thật là thống kê: chỉ token được lấy mẫu mới có nhãn, token hiếm bị đánh giá quá cao, và thưởng cuối câu làm TD một bước truyền chậm. Nhưng nếu lấy trọn câu và cập nhật on-policy, soft Q gần như trùng GRPO không chia std có KL theo câu, nên muốn thành một hàng riêng thì phải dùng off-policy.

### Cited Findings
- Schulman, Chen, Abbeel chứng minh trong RL có điều chuẩn entropy, soft Q-learning tương đương chính xác một phương pháp policy gradient; gradient của loss n-step Q-learning bằng gradient của n-step PG cộng với số hạng bình phương sai của hàm giá trị, tức dạng A3C. Bài còn nối Q-learning có replay với natural PG, và dựng được một Q-learning bám động học A3C mà không dùng mạng đích hay lịch ε — [arXiv 1704.06440](https://arxiv.org/abs/1704.06440). Trang arXiv không ghi venue nên phải trích là preprint.
- Chính sách tối ưu có dạng π ∝ exp(Q), nên PG đang giải Q tối ưu tới một hằng số cộng; bài dùng phạt KL về chính sách tham chiếu, tổng quát hơn entropy — [Schulman et al.](https://arxiv.org/abs/1704.06440).
- Guo et al. viết rằng policy gradient và Q-learning trên văn bản thường không hiệu quả hoặc thiếu ổn định vì không gian chuỗi lớn và thưởng chỉ có cuối câu. Họ đặt Q ≡ logit, gộp α vào thang thưởng, dùng PCL một bước và nhiều bước, và với cách làm này cập nhật được Q của mọi token trong từ vựng — [Findings of EMNLP 2022 theo OpenAlex](https://arxiv.org/abs/2106.07704).
- Số của Guo trên điều khiển chủ đề, perplexity: MLE+PG (5/10/15) 25,52/28,16/28,71 và SQL 25,94/26,95/29,10, tức không hơn nhau về độ trôi chảy. Phần hơn nằm ở độ chính xác chủ đề và tấn công đối kháng, chỉ có ở hình và bảng phụ lục — [Guo et al.](https://arxiv.org/abs/2106.07704). Với tấn công suy diễn, tác giả nói MLE+PG sụp về ít câu.
- PCL là loss nhất quán đường đi, thống nhất on-policy và off-policy — [Nachum et al., NIPS 2017](https://arxiv.org/abs/1702.08892). Một bài 2026 nhận xét với mô hình tự hồi quy, chuyển lùi cố định theo thứ tự token nên loss GFlowNet quy về PCL — [GFlowPO](https://arxiv.org/abs/2602.03358). Đây là preprint, tôi chỉ đọc đoạn tóm tắt của công cụ tìm kiếm.
- Trajectory Balance with Asynchrony dùng VarGrad: thay mạng Z(x) bằng ước lượng theo lô từ log πref − log πθ + r/β trên K mẫu, tự báo nhanh gấp 4 lần trở lên và hơn Online DPO, Dr. GRPO trên các mô hình từ Pythia 410M tới Qwen2.5-7B — [Bartoldson et al., NeurIPS 2025](https://arxiv.org/abs/2503.18929).
- Tiền lệ duy nhất tôi thấy trên VLM cho họ này: LLaVA-v1.6-Mistral-7B, bài toán dự đoán số tiếp theo, 1.000 mẫu, tỉ lệ thành công: không tinh chỉnh 15,7; SFT 21,7; PPO 50,2; GFlowVLM 76,4 — [Kang et al., CVPR 2025](https://openaccess.thecvf.com/content/CVPR2025/papers/Kang_GFlowVLM_Enhancing_Multi-step_Reasoning_in_Vision-Language_Models_with_Generative_Flow_CVPR_2025_paper.pdf). Bài toán hẹp, thưởng khác, đừng suy sang chú thích.
- Bahdanau mô tả đúng trở ngại từ vựng lớn: giá trị của hành động hiếm bị đánh giá quá cao mạnh, làm lệch gradient và có thể phân kỳ, phải phạt phương sai đầu ra của critic. Khi thưởng chỉ đặt ở bước cuối thì tín hiệu quá thưa cho critic — [Bahdanau et al.](https://arxiv.org/abs/1607.07086). Bài cũng gặp hiện tượng phân phối hành động bão hoà về tất định làm gradient tan biến.
- Sequence Tutor dùng Q-learning kèm log xác suất của mô hình đã học làm tiên nghiệm (KL-control), tức chính dạng "Q + log prior", đăng ở ICML 2017 — [Jaques et al.](https://arxiv.org/abs/1611.02796). Bài thử trên nhạc và phân tử, không trên câu.
- Tiền lệ DQN trực tiếp trên sinh chuỗi tôi chỉ thấy một bản arXiv 2015 "Generating Text with Deep Reinforcement Learning" — [Guo H.](https://arxiv.org/abs/1510.09292), không đọc được toàn văn, OpenAlex chỉ thấy arXiv. RL4LMs nhắc AE-DQN với vai trò loại hành động — [Ramamurthy et al.](https://arxiv.org/abs/2210.01241).
- SAC tự nhận là thuật toán cho hành động liên tục; bản rời rạc của Christodoulou là preprint, thử trên một số game Atari — [arXiv 1910.07207](https://arxiv.org/abs/1910.07207). Tìm riêng SAC trên LLM không ra bài nào hiện thực; một bài 2025 chỉ trích SAC làm lý do cho điều chuẩn entropy — [arXiv 2509.21170](https://arxiv.org/abs/2509.21170).
- Qwen2.5-VL-3B có `hidden_size` 2048 — [config](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct/raw/main/config.json).

### Inferences
- [suy] **Số hành động không phải chỗ đắt.** Một lượt forward đã cho logits của cả 151.936 token, nên max và tổng đều rẻ. Đắt là đầu Q **riêng**: 2048 × 151.936 ≈ 311 triệu tham số, gấp khoảng 21 lần LoRA 15 triệu, khoảng 593 MiB ở fp16 mỗi đầu. SAC rời rạc cần hai Q và hai đích, khoảng 2,4 GiB chỉ riêng các đầu, trong khi lượt sinh đã dùng 12,71 GiB trên T4. Dùng chung logits thì không tốn thêm, nhưng khi đó actor trùng critic và SAC trở thành soft Q.
- [suy] **Thang đo giải được bằng logits phần dư.** Đặt π₀ = S1 và objective E[R] − α KL(π‖π₀). Nghiệm là π*(y) ∝ π₀(y) exp(R(y)/α). Theo token: π*(a|s) = π₀(a|s) exp((Q(s,a) − V(s))/α), V(s) = α log Σₐ π₀(a|s) exp(Q(s,a)/α), và Q(sₜ, aₜ) = V(sₜ₊₁), V(cuối) = R. Vậy Q/α = f_θ − f_S1 (tới một hằng số), và lúc bắt đầu θ = S1 thì Q = 0, V = 0: không còn khoảng lệch thang đo. Dự án đã chạy forward của adapter tham chiếu để tính phạt KL, nên không tốn thêm [suy, chưa đo].
- [suy] **Nghiệm chung.** π₀ exp(R/α) cũng là đích của RAML, của KL-control, và của TB. Cả ba hàng này cùng một objective, chỉ khác bộ ước lượng. α = 0,04 làm ΔSPICE 0,1 thành tỉ lệ e^2,5 ≈ 12 lần. β = 0,04 của GRPO trong dự án là phạt theo trung bình token, nên α hiệu dụng khác (khoảng β chia độ dài câu), không dùng thẳng được.
- [suy] **Trọn câu, on-policy, soft Q trùng GRPO họ Dr.** Cộng dồn theo câu: V(s₀) + α Σₜ log(π/π₀) = R(y). Thay V(s₀) bằng trung bình nhóm (VarGrad, như TBA): δᵢ = α(Lᵢ − L̄) − (Rᵢ − R̄), với L = Σ log π/π₀, và gradient của ½Σδ² là Σδᵢ α∇Lᵢ. Đây đúng là PG có mốc trung bình nhóm, không chia std, cộng KL theo câu bằng score function. Tức là chạy bản này rồi gọi "họ Q-learning" thì không thêm được thông tin, và thầy biết RL sẽ nhận ra. Kết quả này phù hợp với Schulman (tương đương chính xác) và đoạn VarGrad của TBA, nhưng phần phép tính là của tôi; kiểm lại trước khi trích.
- [suy] Phần khác thật so với GRPO chỉ có ở hai chỗ: **dữ liệu off-policy** (kho mẫu cũ, TB/PCL vẫn hợp lệ còn GRPO thì không) và **V(s) theo từng tiền tố**.
- [suy] **Thí nghiệm nhỏ bảo vệ được.** Gọi tên "soft Q-learning (PCL nhiều bước, logits phần dư)", không gọi DQN.
  1. Selftest CPU: mô hình tí hon, kiểm V, Q và đồng nhất thức ở trên, kiểm gradient theo Schulman bằng số.
  2. Probe T4 20 bước: chỉ trả lời VRAM, s/bước, không NaN. Không trả lời chuyện học được hay không; 20 bước trong `report/329` §4 không đủ cho mục đó.
  3. Lượt 125 bước, khoảng 5,2 h theo tốc độ 150 s/bước: dùng kho câu đã chấm trên câu nhắc dạy (ví dụ mẫu của action 314 trong `runs/rd314/`, phải kiểm còn đủ không) trộn với mẫu mới, thế là off-policy thật. Đọc: phần dư PCL có giảm trên lô giữ riêng không, V(s₀) có bám R̄ không, entropy có sụp không, rồi chấm val 400 so S1. Ngang A2C thì đó là đúng dự báo của Schulman, ghi được như một kết quả.
  4. Biến thể gần DQN nhất: α nhỏ dần, mạng đích là adapter sao chép định kỳ, ε-greedy. Chỉ chạy nếu bước 3 có tín hiệu; nếu chạy thì mới được gọi "kiểu DQN". Bahdanau dự báo cần phạt phương sai.
- [suy] Câu ngắn làm TD đỡ khó hơn các bài trên: khoảng vài chục bước backup là hết câu. Nhưng n-step tới cuối câu thì chính là Monte Carlo, tức trở lại PG. Không có một mức n ở giữa mà dự án có lý do đặc biệt để chọn.

### Gaps
- Không thấy bài nào so trực tiếp DQN với SCST hay PPO trên câu cùng dữ liệu, cùng mô hình.
- Không thấy Double DQN hoặc Rainbow trên sinh câu với từ vựng lớn.
- Tôi chưa đọc phần phụ lục của Guo nên không có số chính xác cho phần hơn MLE+PG về chủ đề.
- Mức vượt trội của off-policy với thưởng SPICE trên VLM là câu hỏi mở; TBA chỉ tự báo trên các bài toán khác.

## TRPO và NPG: chi phí bậc hai, Fisher-vector trên LoRA, tiền lệ

### Takeaway
Bộ nhớ của vector không phải trở ngại: 15 triệu tham số nên CG rất rẻ. Trở ngại là đồ thị bậc hai với gradient checkpointing và fp16 trong khi T4 đã gần đầy, và số chuỗi trong lô quá ít để lấy mẫu con như bài gốc. Có đường đi chỉ cần bậc nhất. Khả thi về nguyên tắc, chưa đo, và tôi không thấy tiền lệ có số trên LLM.

### Cited Findings
- TRPO gốc: k = 10 vòng CG là đủ; làm thô thì hơn 90% công nằm ở Fisher-vector; tính Fisher trên 10% dữ liệu thì tổng công FVP xấp xỉ một lần gradient, vì Fisher chỉ đóng vai metric — [Schulman et al., ICML 2015](https://arxiv.org/abs/1502.05477).
- ISOPO: Fisher quá lớn nên NPG đầy đủ không làm được; proximal như GRPO xấp xỉ NPG; ISOPO xấp xỉ NPG trong một lượt backward với chi phí thêm không đáng kể, bằng cách chuẩn hoá gradient log-prob từng chuỗi theo metric Fisher — [Abrahamsen, preprint 12/2025](https://arxiv.org/abs/2512.23353). Một tác giả, chưa thấy venue.
- ACKTR dùng xấp xỉ Kronecker theo lớp cho actor và critic — [Wu et al.](https://arxiv.org/abs/1708.05144). Venue NIPS 2017 [nhớ], PDF arXiv không in. ISOPO xếp K-FAC, Shampoo, SOAP vào nhóm tác động trên chiều tham số — [Abrahamsen](https://arxiv.org/abs/2512.23353).
- RL4LMs nêu có TRPO trong thư viện, không thấy báo số — [Ramamurthy et al.](https://arxiv.org/abs/2210.01241). Tìm riêng TRPO/LLM không thấy thêm bài nào.
- PyTorch: `use_reentrant=False` làm `checkpoint` hoạt động đúng với `torch.autograd.grad` — [mã nguồn torch/utils/checkpoint.py](https://raw.githubusercontent.com/pytorch/pytorch/main/torch/utils/checkpoint.py). Tài liệu đoạn tôi đọc không nói về `create_graph`.
- Mã dự án đã bật `use_reentrant=False` và tự chọn bf16 hoặc fp16 — `harness/grpo_luoi.py:322-323`.
- LoRA khởi tạo B = 0 nên gradient ở bước đầu bằng 0 là chuyện đã biết trong dự án — [report/151:104](../../151_BAN_CHOT_CUOI_PHUONG_PHAP_VA_THUOC_7_9.md).

### Inferences
- [suy] **Bộ nhớ của vector:** 15 triệu × 4 byte ≈ 57 MiB mỗi vector, CG cần khoảng bốn vector, dưới 0,3 GiB. Ma trận đầy đủ 15M² ≈ 2,2×10¹⁴ phần tử thì bất khả thi, đúng như ISOPO nói, nhưng TRPO không dựng ma trận.
- [suy] **Thời gian, ước lượng rất thô:** mỗi FVP tương đương 1–2 lần gradient trên cùng lô. Lấy 13,4 s/bước SFT làm đơn vị (không cùng cỡ lô, chỉ để định cỡ) thì 10 FVP tốn thêm 134–268 s/bước trên nền 150 s. Một lượt 500 bước từ khoảng 20,6 h lên khoảng 40–60 h T4. Với lô con một phần tư, thêm khoảng 30–70 s/bước, tức khoảng 25–30 h. Chưa đo, phải probe.
- [suy] **Đồ thị bậc hai là chỗ rủi ro.** FVP chuẩn dùng `create_graph=True` qua checkpoint, tức giữ thêm đồ thị trên một GPU đã ở 12,71 GiB. Dự án cần thử trên mẫu dài nhất theo nguyên tắc P10. Dưới fp16 thì KL rất nhỏ gần θ hiện tại, gradient KL dễ chạm vùng số học kém.
- [suy] **Hai đường không cần bậc hai:**
  - FVP sai phân: Fv ≈ [∇θ′ KL(π_θ‖π_θ′)|θ′=θ+εv]/ε. Một forward no-grad + một forward/backward thường, tương thích checkpoint. Chọn ε phải cẩn thận dưới fp16; chạy phần này ở fp32 hoặc bf16 an toàn hơn. Vẫn là TRPO nếu giữ CG, KL cứng, line search.
  - Fisher hạng thấp: mẫu lấy từ chính π nên gradient log-prob từng câu cho ước lượng Monte Carlo của Fisher. Với N câu, giải hệ Woodbury N × N, không cần CG. Cần N backward riêng, chi phí tương đương G × cỡ lô. Với hạng ≤ N nhỏ thì phải gọi "xấp xỉ NPG hạng thấp", không gọi TRPO. Đây về ý tưởng gần MinSR và ISOPO.
- [suy] **Điểm riêng của LoRA:** ΔW = BA là song tuyến. Tại B = 0, score theo A bằng 0, nên Fisher có hàng và cột bằng 0, phải có damping ở bước đầu và bước đầu chỉ đi theo B. Bản `ck500` gắn LoRA mới nên gặp đúng trường hợp này.
- [suy] Lấy mẫu con 10% của TRPO gốc được thiết kế cho lô hàng chục nghìn bước; dự án chỉ có vài chục câu mỗi bước nên không giảm sâu được.
- [suy] Phạt KL hiện tại của dự án về S1 cố định, không phải về π_old, nên GRPO β=0,04 không phải dạng phạt của TRPO. Nếu cần hàng rẻ hơn, phạt KL về π_old là dạng PPO-penalty, không phải TRPO.

### Gaps
- Chưa có số đo VRAM hoặc s/bước nào cho FVP trên mô hình này; không chạy GPU trong lượt này.
- Chưa kiểm `create_graph=True` qua checkpoint non-reentrant với LoRA và mô hình thị giác; tài liệu phần tôi đọc không khẳng định, phải chạy selftest CPU.
- Không tìm thấy TRPO có số trên mô hình ngôn ngữ, nên hàng này sẽ không có mốc để đối chiếu cài đặt.

## DDPG, TD3, DPG: vì sao không áp dụng, nới rời rạc có giữ được tên không

### Takeaway
Ba thuật toán cần ∂Q/∂a tại hành động liên tục; token thì không có đạo hàm đó, và SPICE cũng không khả vi. Có ba lối sửa, nhưng mỗi lối đổi bản chất của phép so. Câu "không chạy, nêu lý do" vẫn đúng; lý do cần viết chính xác hơn "vì hành động liên tục".

### Cited Findings
- DPG là thuật toán gradient cho chính sách tất định, vốn đặt ra cho hành động liên tục — [Silver et al., ICML 2014](https://proceedings.mlr.press/v32/silver14.html).
- Wolpertinger: actor sinh proto-action liên tục, tra k láng giềng trong không gian nhúng, critic chọn hành động có Q cao nhất, huấn luyện bằng DDPG; thử tới một triệu hành động, abstract nêu mô hình ngôn ngữ là ví dụ nhiều hành động — [Dulac-Arnold et al.](https://arxiv.org/abs/1512.07679). OpenAlex chỉ thấy arXiv.
- Một bài 2026 cho rằng tra láng giềng khó đi với số chiều cao — [arXiv 2602.08616](https://arxiv.org/html/2602.08616v1), chỉ đọc đoạn tìm kiếm.
- Gumbel-softmax đi kèm GAN văn bản: RelGAN nhận là kiến trúc đầu tiên cho thấy GAN + Gumbel-softmax sinh được văn bản thực tế — [RelGAN](https://openreview.net/pdf/28ff6712d62fef4d4846fca5be5df06a8ffd41d2.pdf). Bản straight-through chuyển token rời rạc ở chiều xuôi và dùng nới lỏng ở chiều ngược, có độ lệch — [khoá học trực tuyến, nguồn yếu](https://apxml.com/courses/generative-adversarial-networks-gans/chapter-6-gans-beyond-image-generation/gumbel-softmax-text-gans).
- Tiền lệ DPG thật trên văn bản: Gu, Cho, Li đặt actor nhỏ quan sát và sửa hidden state của decoder NMT, huấn luyện bằng biến thể DPG, tối ưu các mục tiêu tuỳ ý — [EMNLP 2017](https://aclanthology.org/D17-1210/), [arXiv](https://arxiv.org/abs/1702.02429). Chỉ đọc tóm tắt.
- Không có kết quả nào trong các tìm kiếm của tôi cho thấy Wolpertinger đã dùng trên LLM.

### Inferences
- [suy] Đầy đủ hơn: DPG dùng ∇ₐQ(s,a)·∇θμ(s). Muốn có ∇ₐ thì a phải liên tục và Q phải khả vi theo a. SPICE không khả vi, nên buộc phải có critic học được trên một biểu diễn liên tục. Sai số của critic trở thành toàn bộ tín hiệu. PG thì không cần đạo hàm thưởng, đó là lý do họ này là lựa chọn tự nhiên.
- [suy] **Gumbel-softmax.** Khi đó a là vector trên simplex 151.936 chiều, bước kế nhận hỗn hợp nhúng thay vì một token. Với mô hình đã SFT, đó là đầu vào chưa từng thấy. Critic phải học trên phân phối đó. Tên thuật toán không còn đúng: nên gọi "actor-critic khả vi qua Gumbel". TD3 chỉ thêm double critic và trễ actor, nên cũng gồm những vấn đề đó và gấp đôi chi phí.
- [suy] **Wolpertinger.** Tên giữ được vì chính bài định nghĩa như vậy. Nhưng: chính sách tất định làm mất lấy mẫu mà GRPO/SCST cần; k láng giềng trong nhúng token không theo ngữ nghĩa thao tác; phải có Q riêng 311 triệu tham số (hoặc Q(s, nhúng a), là mạng mới). Không có tiền lệ sinh câu. Không đáng chạy.
- [suy] **Gu 2017.** Giữ được tên DPG vì đổi MDP: hành động là vector cộng vào hidden state, token sinh sau đó. Đây là phương án hợp lệ nhất, nhưng trả lời câu hỏi khác (bộ điều khiển thêm vào mô hình, không phải tinh chỉnh LoRA) và dự án từng gặp hiện tượng kênh gắn thêm bị decoder bỏ qua (PATA-C1, FGRB trong `CLAUDE.md`). Không khuyến nghị.

### Gaps
- Tôi không đọc toàn văn Gu 2017 nên không có số BLEU cụ thể.
- MADDPG dùng Gumbel cho hành động rời rạc [nhớ], chưa kiểm; không nằm ở phạm vi sinh câu.

## Nếu chỉ chạy được 4–6 thuật toán: chọn gì, và câu trung thực cho phần loại

### Takeaway
Sáu hàng thuyết phục nhất với một người biết RL: **REINFORCE gốc · SCST · A2C · PPO · soft Q off-policy · TRPO (nếu qua probe, không thì ES)**, với SFT tiếp làm đối chứng không tính vào sáu. Tiêu chí là mỗi hàng thay đúng một cơ chế (mốc, critic, clip, Q, metric), không phải độ phổ biến.

### Cited Findings
- Trong tiền lệ gần nhất, thứ tự giữa các thuật toán không ổn định theo tác vụ: RF-C > AC trên IWSLT nhưng AC+LL > RF-C+LL trên WMT14 — [Bahdanau et al.](https://arxiv.org/abs/1607.07086). REINFORCE hơn PPO — [Ahmadian et al.](https://aclanthology.org/2024.acl-long.662.pdf). PPO thấp hơn GRPO trên Qwen2.5-3B — [Qiu et al.](https://arxiv.org/abs/2509.24372). Supervised+RL hơn RL một mình — [Ramamurthy et al.](https://arxiv.org/abs/2210.01241).
- Trạng thái mã và chi phí: `harness/grpo_ppo.py` đã viết, chưa probe T4; PPO/A2C không có hệ số entropy, giữ β = 0,04, đầu giá trị nhỏ; clip không hoạt động khi `num_iterations` = 1 — [report/326](../../326_BAN_GIAO_LUOI_RL_1_11.md), `harness/grpo_ppo.py`.
- Với khoảng 50 phép so, Holm đòi p < 0,001 — [report/329](../../329_XEP_HANG_PHO_BIEN_RL_VA_THU_TU_CHAY_1_11.md) §4.

### Inferences
- [suy] **Thứ tự và phép đọc.**
  | # | Hàng | Thay cơ chế nào | Trả lời câu hỏi của thầy | Điều kiện để giữ tên |
  |---|---|---|---|---|
  | đối chứng | SFT tiếp | Không RL | Công của RL so với học thêm | |
  | 1 | REINFORCE không mốc | Không có gì | Gốc họ PG | Khai giữ KL hay không |
  | 2 | SCST + CIDEr-D | Mốc = greedy | Chuẩn chú thích ảnh | Khai là mốc greedy trong khung GRPO |
  | 3 | A2C | Mốc học được | Actor-critic | Có critic thật, khai đầu nhỏ |
  | 4 | PPO λ = 0,95 | Clip + GAE | Mốc phổ biến nhất của RLHF | `clip_ratio/region_mean` > 0 trong log |
  | 5 | Soft Q (PCL, off-policy) | Giá trị, Q ≡ logits | Đại diện DQN, SAC | Khai là soft Q, có dữ liệu off-policy |
  | 6 | TRPO | Ràng buộc KL + CG | Tổ tiên PPO | Có KL cứng, CG, line search; nếu không qua probe thì thay bằng ES |
- [suy] ES đứng sau TRPO vì tiền lệ ở Countdown, không gần bài toán này; nhưng nếu TRPO không vừa T4 thì ES là hàng hợp lý nhất, vì là họ khác hẳn (không gradient) và có số ICML 2026 để đối chiếu. ILQL là hàng thứ bảy: hợp về thưởng cuối câu và có bảng so nhiều phương pháp, nhưng đổi cách suy luận nên không còn một adapter duy nhất, khó đặt cạnh các hàng khác. Quark xếp sau vì đổi câu nhắc.
- [suy] Hàng 5 là chỗ dễ làm tốn thời gian nhất; nếu ép ngân sách thì hàng 5 được chạy ở mức selftest và probe, rồi báo kết quả tương đương của Schulman cộng với phép suy ở mục trên. Tuy nhiên báo bằng phép suy thì yếu hơn số thật; phải nói rõ là suy.
- [suy] Một lượt PPO cài kém mà thua ck500 thì không nói được gì về PPO. Nên công bố cả phép kiểm clip, explained variance của đầu giá trị, và KL trung bình mỗi bước. Với một hạt giống và hai hạt ck500 đã chênh 0,72 exec, khác biệt dưới khoảng 1 điểm không xếp hạng được. Câu kết luận nên là "không có thuật toán nào trong nhóm hơn rõ ck500 trên cùng dữ liệu" hoặc ngược lại, không phải một bảng xếp hạng theo thứ tự.
- [suy] **Câu trung thực cho phần loại** (đã soạn để dùng, văn phong luận văn):
  - DDPG, TD3, DPG: "Ba thuật toán này cần đạo hàm của hàm giá trị theo hành động, trong khi hành động ở đây là token rời rạc và SPICE không khả vi. Nới liên tục bằng Gumbel-softmax buộc mô hình đọc hỗn hợp nhúng chưa từng thấy và đổi bản chất thuật toán, nên chúng tôi không chạy."
  - DQN, Double DQN, Rainbow: "Dạng entropy của Q-learning tương đương policy gradient (Schulman và cộng sự, 2017), nên chúng tôi đại diện họ này bằng soft Q-learning với logits làm giá trị Q (Guo và cộng sự, 2022). Bản max cứng, replay và ε-greedy chưa có tiền lệ đáng tin cho sinh câu từ vựng lớn và chúng tôi không chạy riêng."
  - SAC: "SAC rời rạc cần hai đầu Q cho toàn bộ 151.936 token, khoảng 311 triệu tham số mỗi đầu so với 15 triệu tham số LoRA; khi dùng chung logits thì SAC quy về soft Q-learning đã chạy. Chúng tôi không tìm thấy tiền lệ trên mô hình ngôn ngữ."
  - A3C: "A3C và A2C khác nhau ở cách chạy song song; chúng tôi chạy A2C."
  - TRPO nếu không chạy: "Chúng tôi không tìm thấy tiền lệ có số trên mô hình ngôn ngữ và chi phí tính tích Fisher-vector vượt khả năng của phần cứng dùng trong đề tài [chỉ viết nếu đã đo]; PPO và GRPO là các xấp xỉ bậc nhất của cùng ý tưởng."
  - CQL, IQL, DT: "ILQL (Snell và cộng sự, 2023) đã so các phương pháp này trên ngôn ngữ; đề tài học on-policy và đánh giá từng adapter nên chỉ trích kết quả của họ."
  - MIXER: "Curriculum của MIXER dùng để khởi động mô hình chưa có chính sách tốt; Rennie và cộng sự (2017) cho thấy có thể bỏ. REINFORCE với mốc học được đã được đại diện bằng A2C."
  - GAIL: "GAIL học phần thưởng từ bộ phân biệt nên không dùng SPICE hay CIDEr-D, không trả lời câu hỏi so thuật toán trên cùng phần thưởng."
  - SeqGAN nếu không chạy: "SeqGAN thay phần thưởng bằng bộ phân biệt, và MLE đã được chứng minh vượt các GAN văn bản trên toàn dải chất lượng và đa dạng (Caccia và cộng sự, 2020)."

### Gaps
- Xếp hạng này là ý kiến của tôi dựa trên cấu trúc thuật toán; chưa có người hướng dẫn nào xác nhận. Nên hỏi thầy xem ông có muốn thấy hàng DQN gắn đúng tên hay không.
- Chi phí hàng 5 và 6 chưa đo.

## Có khảo sát nào đóng khung các họ này cho sinh văn bản không

### Takeaway
Có, nhưng không có bài nào chia theo policy-based và value-based cho LLM. Khung tốt nhất cho phần cổ điển là Keneshloo (TNNLS 2020), cho phần LLM là Wang et al. (arXiv), và khung lý thuyết tốt nhất để nối các họ là bài của Schulman cùng Nachum.

### Cited Findings
- Keneshloo et al., *Deep Reinforcement Learning for Sequence-to-Sequence Models*, IEEE TNNLS 31(7): 2469–2489: nêu hai vấn đề exposure bias và lệch giữa huấn luyện và kiểm thử, có thí nghiệm so các mô hình RL trên tóm tắt và phát hành mã — [arXiv](https://arxiv.org/abs/1805.09461), [NSF PAR](https://par.nsf.gov/biblio/10142308).
- Wang et al., *Reinforcement Learning for LLM Post-Training: A Survey*: khung policy gradient thống nhất PPO, GRPO cho RLHF, RLVR, và các phương pháp kiểu DPO — [arXiv 2407.16216](https://arxiv.org/abs/2407.16216). Tôi chỉ đọc qua tóm tắt tìm kiếm; chưa kiểm venue.
- Cao et al., *Reinforcement Learning for Generative AI: A Survey* — [arXiv 2308.14328](https://arxiv.org/abs/2308.14328).
- Yu et al., khảo sát RL cho LLM khi thiếu dữ liệu, ACL 2026, tr. 22823–22846, phân loại theo dữ liệu, huấn luyện, khung — [ACL Anthology](https://aclanthology.org/2026.acl-long.1045/). Chỉ đọc tóm tắt.
- Wu, khảo sát học từ phần thưởng cho LLM, Findings of EMNLP 2025 — [ACL Anthology](https://preview.aclanthology.org/new-sigs/2025.findings-emnlp.970/). Lai et al., ACL 2025, về post-training scaling — [ACL Anthology](https://aclanthology.org/2025.acl-long.140). Chỉ đọc tóm tắt.
- RL4LMs §2 có đoạn tổng kết ngắn dòng RL cho không gian hành động lớn: MIXER, Bahdanau, KG-A2C, TrufLL, AE-DQN, GALAD — [Ramamurthy et al.](https://arxiv.org/abs/2210.01241).

### Inferences
- [suy] Cách trình bày trong luận văn nên theo ba bậc: Keneshloo cho nhóm MIXER, SCST, actor-critic; Wang et al. cho PPO, GRPO, DPO; Schulman và Nachum nối Q-learning sang policy gradient. Nhóm "π₀ exp(R/α)" là sợi chỉ chung, ở mức ghi chú của đề tài chứ không phải khung có trong khảo sát nào tôi đọc.

### Gaps
- Tôi không thấy khảo sát nào đặt DQN, SAC, TRPO cạnh nhau cho sinh câu có số. Có thể đó là khoảng trống mà một phần so sánh của luận văn lấp được, nhưng phải khai là khảo sát của tôi chưa hệ thống, không được viết "chưa có ai".
