# GRPO phải đối đầu SFT, PPO và DPO

Lưới đang chạy mới trả lời được câu "mốc trừ nào tốt nhất", còn ba mốc mà người đọc tài liệu sẽ tìm đầu tiên vẫn thiếu: **SFT chạy tiếp, PPO có mô hình giá trị, và DPO xuất phát sạch từ S1**. Trong mẫu ghi chú, GRPO là mốc của 36/42 bài họ RLVR, SFT và PPO lần lượt có mặt ở 20/30 và 16/30 bài RLHF, SCST có mặt ở 13 bài chú thích ảnh, còn phần lớn bài GUI (23/32) không so với thuật toán RL khác. Vì vậy một luận văn GUI chạy nhiều thuật toán trên cùng dữ liệu, cùng mô hình, cùng phần thưởng đã kiểm soát chặt hơn đa số bài trong mẫu, nhưng phải có đủ các dòng đó thì mới không bị hỏi vặn. Danh sách đề xuất gồm 11 lượt đã có trong kế hoạch (6 đang chạy, 5 sắp chạy), 11 lượt mới ưu tiên một (đứng đầu là SFT tiếp, SCST + CIDEr-D, PPO, DPO, RFT), 15 lượt ưu tiên hai và 2 lượt tuỳ chọn; SAC, A2C, KTO và VinePPO không cần chạy, lý do ghi ở cuối mục danh sách. Khi soi mã còn thấy hai việc phải khai ngay: ck500 dùng `loss_type="dapo"` nên không phải GRPO gộp theo câu, và với `num_iterations=1` phép clip không hoạt động, nên phần "clip" của DAPO, GSPO và PPO không được kiểm tra trong lưới hiện tại. Mọi kết luận ở đây là một hạt giống; hai hạt ck500 đã chênh nhau 0,72 điểm exec ([report/323](../323_DEBATE_VA_ACTION_KHAO_SAT_GRPO_SPICE_ACE_1_11.md)), nên chênh lệch dưới khoảng 1 điểm không đủ để xếp hạng.

## Mẫu 153 bài cho thấy mỗi họ có một mốc mặc định riêng

Đây là **mẫu có chủ đích, không phải tổng quan hệ thống**, nên các tỉ lệ chỉ mô tả mẫu. Yêu cầu ban đầu là khoảng 100 bài; bốn nhóm ghi chú thực tế có 158 dòng bảng. Năm bài xuất hiện ở hai nhóm (ReMax, Back to Basics và DeepSeek-R1 ở RLVR lẫn RLHF; Learning to Summarize và RL4LMs ở RLHF lẫn chú thích ảnh), tức **153 bài riêng biệt**. Bài trùng được đếm một lần trong mỗi nhóm và tôi **không cộng các cột thành tổng chung**. Mẫu bị lệch theo cách lấy: các nhóm RLVR và GUI được gieo từ tên và từ khoá liên quan tới GRPO, nên tỉ lệ GRPO cao một phần do cách chọn.

| Nhóm | Dòng trong bảng | Được đếm mốc | Bỏ khỏi bảng đếm | Cách đọc mốc |
|---|---:|---:|---|---|
| RLVR / họ GRPO | 42 | 42 | 8 bài khác ở danh sách loại riêng (kể cả DeepSeekMath), không nằm trong 42 | toàn văn PDF tìm theo từ khoá, đọc đoạn và hàng bảng liên quan |
| RLHF và cặp ưu tiên | 32 | 30 | 2 dòng chưa kiểm mốc | như trên, chỉ đếm khi thấy số so sánh |
| Chú thích ảnh và sinh văn bản | 40 | 36 | 3 dòng chưa kiểm mốc, 1 dòng không dùng RL cho bên nói | như trên, chỉ tính so sánh thuật toán, không tính so kiến trúc |
| VLM (không GUI) | 11 | 11 | 0 | quét từ khoá toàn văn, có thể sót mốc chỉ ghi bằng tên mô hình |
| GUI, di động, computer use | 33 | 32 | DigiRL chưa kiểm mốc | như VLM |

Ở bảng dưới, mỗi ô là số bài của nhóm đó có thấy mốc này. Ô "n/đ" nghĩa là ghi chú không đếm hạng mục đó ở nhóm này, không có nghĩa là bằng 0.

| Mốc | RLVR (42) | RLHF (30) | Chú thích/văn bản | VLM (11) | GUI (32) |
|---|---:|---:|---|---:|---|
| GRPO | **36** | 1 | 1 bài đề xuất GRPO so với SCST, không làm mốc | 5 (kể cả so biến thể) | 7 (GRPO thuần hoặc biến thể của chính bài), cộng UI-TARS-2 |
| PPO | 10 | **16** | 1 (NLPO, không phải chú thích) | 0 | 0 có số; VEM chỉ có hình loss |
| DAPO | 15 | 0 | 0 | 3 | 0 |
| Dr. GRPO | 8 | 0 | 0 | 0 | 0 |
| RLOO | 5 | 1 | 0 | 0 | 0 |
| REINFORCE và biến thể | 4 (cộng 5 bài REINFORCE++) | 2 | 2 | 0 | 0 |
| GSPO | 5 | 0 | 0 | 0 | 0 |
| SCST | 0 | 0 | **13** (7 so với thuật toán khác, 6 giữ SCST và đổi phần thưởng) | 0 | 0 |
| SFT / supervised | n/đ | **20** | n/đ, XE thường là dòng đầu | n/đ | phần lớn trong 23 bài không có RL khác |
| DPO ngoại tuyến | n/đ | 15 | 1 (SC-Captioner) | 0 | 0 |
| RAFT / RFT | n/đ | 2 | 0 | 0 | 0 |
| SAC, A2C, A3C, TD3, TRPO | **0** | 0 | Chen & Bansal dùng A2C làm phương pháp, không làm mốc | 0 | 0 |

Đọc theo hàng, RLVR lấy GRPO + DAPO làm cặp đối chứng ([Harder Is Better](https://arxiv.org/abs/2601.20614), [FlowRL](https://arxiv.org/abs/2509.15207)). RLHF trực tuyến lấy PPO + SFT + DPO. RLHF ngoại tuyến lấy SFT + DPO, và **không bài ngoại tuyến nào trong mẫu so bằng số với REINFORCE, RLOO hay GRPO**; [QRPO](https://arxiv.org/abs/2507.08068) còn nêu phép so với GRPO là câu hỏi mở. Chú thích ảnh coi SCST là "tiêu chuẩn mới" ([Luo 2020](https://arxiv.org/abs/2003.09971)) và CIDEr là phần thưởng phổ biến nhất, có ở 20 dòng; BLEU và ROUGE theo sau xa, còn SPICE đứng một mình trong nhóm ghi chú này **không có hàng số nào**; [sửa 2/11] khảo sát `report/330` tìm được hàng số ở RL4LMs Bảng 12, đã đối chiếu PDF. Ở GUI, GRPO hoặc biến thể chiếm 26/33 bài có thuật toán RL hoặc ưu tiên, nhưng lý do thường là không cần mô hình giá trị và tiền lệ R1, ví dụ [UI-R1](https://arxiv.org/abs/2503.21620), [SE-GUI](https://arxiv.org/abs/2505.12370), [ZeroGUI](https://arxiv.org/abs/2505.23762). Bài GUI duy nhất chạy cả hai và chọn theo thí nghiệm là [UI-TARS-2](https://arxiv.org/abs/2509.02544), và bài đó chọn PPO. Đây là đòn nguy hiểm nhất nếu luận văn bỏ PPO.

## So sánh tốt giữ nguyên điểm xuất phát, tín hiệu và ngân sách mẫu

Tài liệu có bốn kiểu thiết kế, sức thuyết phục giảm dần. Kiểu thứ nhất là **chạy đối đầu trên cùng quy trình**: [VinePPO](https://arxiv.org/abs/2410.01679) ghi "all methods use the same SFT checkpoint" và cùng số episode, [CPGD](https://arxiv.org/abs/2505.12504) dùng cùng siêu tham số trên QwenVL2.5-7B, [λ-GRPO](https://arxiv.org/abs/2510.06870) giữ dữ liệu, khuôn câu nhắc và kiến trúc, còn [Lian 2025](https://arxiv.org/abs/2512.07611) áp PPO, GRPO, DAPO lên cùng mô hình và tập dạy. Kiểu thứ hai là **ablation tích luỹ**, như [DAPO](https://arxiv.org/abs/2503.14476) Bảng 1 thêm dần từng thành phần (30, 36, 38, 41), nên không phải đổi một yếu tố mỗi lần. Kiểu thứ ba **trộn mô hình tái lập có dữ liệu khác nhau**, như [AAPO](https://arxiv.org/abs/2505.14264) với cỡ tập dạy từ 8.523 tới hơn 230K. Kiểu thứ tư, phổ biến ở GUI, so với **mô hình khác** khác cả dữ liệu, nền và phần thưởng, nên không tách được công của thuật toán.

Các bài kiểm soát tốt còn có điều khoản công bằng đáng chép. [MathForge](https://arxiv.org/abs/2601.20614) tắt resampling của GPG và DAPO để so ở mức thuật toán. [GSPO](https://arxiv.org/abs/2507.18071) nói đã chỉnh dải clip của GRPO để so công bằng, còn [Pass@K](https://arxiv.org/abs/2505.15201) cố ý quét hệ số entropy cho mốc PPO. [QRPO](https://arxiv.org/abs/2507.08068) dùng cùng một mô hình thưởng để xếp cặp cho DPO, SimPO và để train REBEL, QRPO, gọi đó là "equal potential signal source". [Bridging](https://arxiv.org/abs/2506.21495) xếp hạng câu theo phần thưởng để tạo cặp DPO, so offline, bán trực tuyến, trực tuyến và GRPO. **Hai bài sau là khuôn gần nhất để đưa DPO vào lưới** với SPICE là tín hiệu chung.

Về báo cáo, đa số chỉ in điểm cuối hoặc đường cong. Nhiều hạt giống là ngoại lệ: [GVPO](https://arxiv.org/abs/2504.19599) dùng mười hạt ở một phép so, [Critique-GRPO](https://arxiv.org/abs/2506.03106) ba lượt, [SCST](https://arxiv.org/abs/1612.00563) bốn hạt. [Art of Scaling](https://arxiv.org/abs/2510.13786) khớp đường sigmoid theo chi phí tính toán thay vì một điểm cuối. Dòng chú thích ảnh có thói quen rất hợp với luận văn: bảng **phần thưởng × độ đo**, mỗi phần thưởng đo trên mọi độ đo ([Rennie Bảng 3](https://arxiv.org/abs/1612.00563), [Liu Bảng 1](https://arxiv.org/abs/1612.00370)). Dòng này còn cảnh báo về chơi độ đo: [ReST](https://arxiv.org/abs/2308.08998) mô tả PPO trực tuyến khai thác điểm yếu của độ đo và BLEU kiểm định giảm gần 8 điểm, [RL4LMs](https://arxiv.org/abs/2210.01241) cho thấy người chấm xếp Supervised trên Supervised+PPO ở 2/5 tác vụ dù độ đo tự động nói ngược lại, [AREL](https://aclanthology.org/P18-1083/) thấy METEOR-RL và ROUGE-RL sinh câu vô nghĩa, [Guo](https://arxiv.org/abs/1809.06227) đo SCST làm 43,7 đến 46,4% câu kết thúc lỗi. Bộ công cụ độc lập của dự án (UGround, UI-Venus, Phi-4) chính là lá chắn cho điểm này, và phải đo thêm hình thức câu.

Nhưng tôi không thấy trong mẫu **phép so nào đổi thuật toán trên phần thưởng liên tục dựa trên tham chiếu kiểu SPICE, từ một điểm SFT, với đủ PPO/REINFORCE/GRPO/DPO**. Ghi chú nhóm chú thích ảnh cũng không tìm thấy phép so bốn chiều SCST, REINFORCE, PPO, GRPO cùng mô hình, cùng phần thưởng. Đây là khoảng trống của mẫu, không phải bằng chứng rằng chưa ai làm.

## Số đối đầu nhỏ và đổi dấu theo bài

Bảng dưới chỉ lấy số trong ghi chú. Số so sánh được trong cùng hàng, **không so giữa các hàng**. Nhãn venue: [S] thấy trên trang kỷ yếu hoặc chương trình, [H] chỉ thấy ở đầu PDF hoặc chú thích arXiv, [Pre] chưa thấy venue.

| Phép so | Số | Nguồn, nhãn | Cách đọc |
|---|---|---|---|
| GRPO, Dr. GRPO, GPG, DAPO, GSPO; TB 6 bộ đo, Qwen2.5-Math-7B | 37,61 · 37,40 · 37,93 · 37,94 · 37,71 | [MathForge](https://arxiv.org/abs/2601.20614), ICLR 2026 [S] | Bảng kiểm soát tốt nhất; các phương pháp đã có chênh trong khoảng 0,33 so với GRPO |
| PPO, GRPO, DAPO không dynamic sampling; GSM8K/MATH/BBH/MMLU-Pro | 50,3/25,1/36,8/27,1 · 50,8/24,7/36,9/28,2 · 53,3/25,4/36,9/30,0 | [Lian 2025](https://arxiv.org/abs/2512.07611), [Pre] | PPO và GRPO đổi vị trí theo bộ đo |
| GRPO, Dr. GRPO, ReMax, REINFORCE++, GVPO; MATH500 | 80,0 · 81,2 · 82,0 · 80,4 · 83,8 | [GVPO](https://arxiv.org/abs/2504.19599), NeurIPS 2025 [S] | Bài đề xuất; ghi chú chưa xác nhận riêng mô hình của hàng này |
| REINFORCE++ k=1, GRPO k=4, RLOO k=4, ReMax; Chat-Arena-Hard | 46,7 · 46,8 · 44,6 · 45,1 | [REINFORCE++](https://arxiv.org/abs/2501.03262), [Pre] | Bài đề xuất |
| GRPO, DAPO; TB nhiều bộ đo đa phương thức | 45,1 · 46,1 (DAPO hơn 1,0) | [ReVisual-R1](https://proceedings.iclr.cc/paper_files/paper/2026/hash/3792ac815260f4ba55ed71c7906cce36-Abstract-Conference.html), ICLR 2026 [S] | Đa phương thức |
| GRPO, DAPO; TB 5 bộ đo, Qwen2.5-VL-7B | 57,16 · 56,92 (GRPO hơn 0,24) | [TGRL](https://arxiv.org/abs/2603.26126), [Pre] | Cùng họ nền; dấu ngược với hàng trên, là kết quả phụ |
| PPO so GRPO trên GUI | Chỉ đường cong thưởng train, không có bảng; bài viết PPO "consistently outperforms" | [UI-TARS-2](https://arxiv.org/abs/2509.02544), [Pre] | Đa lượt, có huấn luyện trước mô hình giá trị, không có số test |
| RLOO k=4, RAFT k=4, RLOO k=2, RAFT k=2, REINFORCE mốc, Vanilla PG, PPO, DPO; TL;DR | 77,9 · 73,2 · 74,2 · 72,1 · 70,7 · 70,4 · 67,6 · 66,6 | [Back to Basics](https://aclanthology.org/2024.acl-long.662/), ACL 2024 [S] (số từ [arXiv](https://arxiv.org/abs/2402.14740)) | Chép từ bảng, không chép câu mở đầu "3,2% to 20,3%" vì tính lại ra 2,8 đến 20,3 |
| PPO trên TL;DR, dòng khác | 77,6 (RLOO k=4 77,9, REBEL 78,1) | [REBEL](https://arxiv.org/abs/2404.16767), NeurIPS 2024 (Crossref) | Số mốc chép từ bài khác; 67,6 và 77,6 không phải tái lập có kiểm soát, nhưng cho thấy biên độ theo cách cài đặt |
| PPO theo λ | Ở λ=0,95 kém rõ so với GRPO; ở λ=1,0 gần GRPO | [DeepSeek-R1](https://arxiv.org/abs/2501.12948), Nature ([bài đăng](https://www.nature.com/articles/s41586-025-09422-z)) | Định tính; lý do còn lại của GRPO là chi phí chỉnh và bộ nhớ |
| GRPO, PPO, VinePPO; MATH 7B | 37,6 · 42,8 · 46,0 | [VinePPO](https://arxiv.org/abs/2410.01679), ICML 2025 [S] | Ánh xạ nhãn giả định theo thứ tự trích từ hình; **đối chiếu hình trước khi dùng** |
| Seed, DPO offline, bán trực tuyến s=10, DPO online, GRPO; AlpacaEval GPT-4-1106 | 27,3 · 53,2 · 81,6 · 83,1 · 75,2 | [Bridging](https://arxiv.org/abs/2506.21495), [Pre] | Trực tuyến hơn ngoại tuyến rõ rệt; riêng GPT-4o trên ArenaHard GRPO lại đứng đầu (54,3 so 50,4), tức bộ chấm đảo được thứ tự |
| XE, MIXER, SCST (FC-2K, CIDEr) | 90,9 · 104,9 · 106,3 | [SCST](https://arxiv.org/abs/1612.00563), CVPR 2017 [S] | Mức tăng do RL lớn hơn nhiều so với chênh giữa các thuật toán RL |
| REINFORCE, mốc học được, SCST (Att2all, 4 hạt) | 110,4 ± 0,5 · 113,2 ± 0,2 · 113,8 ± 0,3 | [SCST](https://arxiv.org/abs/1612.00563), CVPR 2017 [S] | Khoảng cách với mốc học được chỉ 0,6 |
| XE, SCST, PG-CIDEr, 1-step-sample (CIDEr) | 102,1 · 112,7 · 113,9 · 115,4 | [Gao](https://arxiv.org/abs/1904.06861), CVPR 2019 [S] | SCST vẫn dẫn ở BLEU-3/4, METEOR, ROUGE-L, SPICE |
| SCST so mốc bỏ-một trên 4 kiến trúc (CIDEr) | +0,8 tới +3,0 | [Luo 2020](https://arxiv.org/abs/2003.09971), [Pre] | Tiền lệ trực tiếp của RLOO trong chú thích ảnh |
| CE, SCST, GRPO; COCO CIDEr | 84,3 · 97,6 · 100,0 (SPICE 16,4 → 17,1) | [Liang 2025](https://arxiv.org/abs/2503.01333), [Pre] | Phép so GRPO và SCST duy nhất; nền yếu, một tác giả, không thấy nhiều hạt |
| Self-critical so actor-critic (dev COCO, CIDEr-D) | 1,140 · 1,162 | [Zhang 2017](https://arxiv.org/abs/1706.09601), [Pre] | Kiến trúc hai nhánh không hoàn toàn trùng |
| SFT, SFT+DPO, SFT+RL (DOCCI500, Qwen2-VL-7B; BLEU-4) | 40,92 · 43,13 · 43,70 | [SC-Captioner](https://arxiv.org/abs/2508.06125), ICCV 2025 [S] | Mốc gần nhất về họ nền và dạng từ SFT; RL là phương pháp của chính bài |

Về phần thưởng, số gần nhất nằm trong hai bảng cũ. [Rennie](https://arxiv.org/abs/1612.00563) Bảng 3 cho thấy train trên CIDEr nâng cả ba độ đo còn lại so với XE (106,3 · BLEU-4 31,9 · ROUGE-L 54,3 · METEOR 25,5), còn train trên METEOR làm CIDEr giảm từ 90,9 xuống 80,5 trong khi METEOR chỉ lên 25,9. [Sửa 2/11: bỏ câu nói bài này không vượt được CIDEr đơn lẻ khi train nhiều độ đo, vì `report/330` không tìm thấy câu đó trong PDF.] [Liu](https://arxiv.org/abs/1612.00370) Bảng 1 có PG-BCMR 1,013 và PG-SPIDEr 1,000 trên CIDEr-D, và trong đánh giá người trên 492 ảnh, PG-SPIDEr thắng PG-BCMR (p=0,014). Quan trọng hơn cả: **Liu viết PG-SPICE "tends to generate ungrammatical sentences, with a lot of repeated phrases" rồi bỏ SPICE thuần khỏi phần còn lại của bài.** ck500 chính là cấu hình mà bài gốc đã bỏ. Khác biệt là ck500 có phạt độ dài và đi từ điểm SFT với KL, nhưng ghi chú không có phép so nào cho biết các khác biệt đó đủ để tránh hiện tượng này. Vì vậy luận văn phải có phép đo hình thức câu (dòng F1 bên dưới). Kiểm tra sơ bộ của dự án cũng cho thấy SPICE có tín hiệu bước đầu yếu nhất trong các phần thưởng. Số đó là val nên chỉ dùng giải thích và không được trích, nhưng nó có nghĩa là phải chuẩn bị sẵn cách viết cho trường hợp SPICE không đứng đầu.

## Mã hiện tại làm ba thuật toán trùng nhau và để clip không hoạt động

Phần này không phải tài liệu mà là điều tôi đọc từ `harness/grpo_luoi.py` và log ck500, cần thiết để đặt tên lượt cho đúng. Theo chú thích đầu tệp, với `num_iterations=1` tỉ số PPO luôn bằng 1, nên các nhánh chỉ khác ở mốc trừ và chuẩn hoá. Log `runs/grpo_spice/train_c1.log` (262 dòng đầu) và `train_c3.log` (75 dòng cuối) xác nhận **`clip_ratio/region_mean` bằng 0 ở mọi dòng và `completions/clipped_ratio` cũng bằng 0**. Đây là log kỹ thuật lúc train, không phải kết quả.

Từ đó có bốn hệ quả. Thứ nhất, Clip-Higher và Overlong Filtering của DAPO không có tác dụng trong cấu hình này, và ck500 đã dùng gộp theo token của DAPO. Vậy phần DAPO còn lại khác ck500 chỉ là bỏ KL và dynamic sampling. Việc DAPO đặt β=0 không có trong ghi chú, cần kiểm trong [bài DAPO](https://arxiv.org/abs/2503.14476) trước khi viết. Thứ hai, [suy, cần đối chiếu công thức] GSPO ở μ=1 có gradient bằng GRPO gộp theo câu, nên muốn kiểm phần riêng của GSPO phải chạy μ>1, và lý do gốc của GSPO là ổn định trên mô hình MoE ([GSPO](https://arxiv.org/abs/2507.18071)) chứ không phải câu ngắn. Thứ ba, tên "ck500 = GRPO" cần khai: **`loss_type="dapo"` và lượt `drgrpo` của lưới vẫn giữ β=0,04**, trong khi Dr. GRPO kiểu R1-Zero đặt β=0 ([Dr. GRPO](https://arxiv.org/abs/2503.20783)). Lượt đó phải gọi là "GRPO bỏ chia độ lệch chuẩn", không gọi là Dr. GRPO đầy đủ.

Thứ tư là một nhiễu có thể làm sai cách đọc các nhánh không chuẩn hoá. Độ lệch chuẩn thưởng trong nhóm ở log ck500 có trung vị khoảng 0,35, nên nhánh không chia std có lợi thế nhỏ đi cỡ 2,9 lần. [Group-Standard-Deviation Identity](https://arxiv.org/abs/2607.00152) (preprint) nói Dr. GRPO, RLOO và REINFORCE có mốc trùng nhau tới một hằng số learning rate. Mã không đặt `optim`, nên [suy] dùng AdamW mặc định, vốn gần như không đổi khi nhân cả hàm mất mát với hằng số. Khi đó khác biệt thật nằm ở **trọng số tương đối với số hạng β·KL và ở trọng số từng câu nhắc**, chưa rõ lớn tới đâu. Hai điều nên làm từ đây: dùng thiết kế 2×2 (có/không std × β 0,04/0) để tách hai yếu tố, và coi RLOO so với "bỏ chia std" như một phép đo nhiễu. Hai nhánh chỉ khác hằng số 8/7 ([suy] gần như cùng một thuật toán dưới AdamW), nên chênh lệch exec của chúng cho biết độ dao động khi thay đổi vô hại, rất có ích khi đang tạm một hạt.

## Danh sách lượt chạy đề xuất

**Giữ nguyên ở mọi lượt** trừ cột "đổi": S1 hoà làm điểm xuất phát, LoRA mới cùng cỡ, đúng 1.000 câu nhắc của ck500, G=8, nhiệt độ 1, lr 1e-5, β 0,04, 500 bước, chấm điểm lưu cuối (không chọn điểm lưu), hạt 101, T4 fp16. Máy cũng là một biến: dự án đã đo L4 bf16 và T4 fp16 lệch được ±1 bước, nên **ưu tiên Kaggle kể cả khi Colab tiện hơn**, và lượt nào buộc sang Colab thì ghi rõ. **Gói chấm chung cho mọi lượt:** exec, D.3, AitW đầy đủ trên 4.463 bước, KTC ghép cặp và McNemar so ck500 và so S1; 7 độ đo văn bản; bước không chạm vì ck500 có tác hại scroll; log `frac_adv_zero`, KL, độ dài. Hai hoặc ba lượt đứng đầu mỗi trục chấm thêm UI-Venus và Phi-4 theo cảnh báo của ReST và RL4LMs.

**Cách viết ở cột "cho phép viết":** "hơn" nghĩa là KTC ghép cặp loại 0 và |Δ exec| ≥ 1, kèm nhãn một hạt giống; còn lại viết "không phân biệt được". Mọi dòng đều phải báo vô điều kiện, kể cả khi ck500 thua. Ngưỡng 1 điểm lấy từ report/323 §8.3, vẫn dưới MDE 2,11.

### Đã có trong kế hoạch

| Mã | Lượt | Trạng thái | Đổi so với ck500 | Máy, lý do | Mã nguồn | Cho phép viết | Nguồn |
|---|---|---|---|---|---|---|---|
| Đ1 | SCST + SPICE | **Đang chạy** | Mốc = thưởng câu greedy | Kaggle, probe 158 s/bước, 12,71 GiB | Xong, có selftest | So với chuẩn của chú thích ảnh, cùng phần thưởng | [SCST](https://arxiv.org/abs/1612.00563); cùng ý với [ReMax](https://arxiv.org/abs/2310.10505), ghi chú chưa đối chiếu lời văn |
| Đ2 | RLOO + SPICE | **Đang chạy** | Mốc bỏ-một, không chia std | Kaggle, cùng vòng lặp | Xong | So với RLOO; dùng được làm đo nhiễu với K1 | [Back to Basics](https://aclanthology.org/2024.acl-long.662/), [Luo](https://arxiv.org/abs/2003.09971) |
| Đ3 | REINFORCE EMA + SPICE | **Đang chạy** | Mốc trượt, không phụ thuộc câu nhắc | Kaggle | Xong | Mốc theo câu nhắc có đáng hay không. Mốc EMA là lựa chọn của dự án, nói rõ | [ReMax](https://arxiv.org/abs/2310.10505) (lập luận chống trung bình trượt), [SCST](https://arxiv.org/abs/1612.00563) |
| Đ4 | GRPO + CIDEr-D | **Đang chạy** | Phần thưởng | Kaggle, probe 149 s/bước | Xong | So với phần thưởng phổ biến nhất, thay lượt A2 cũ lệch ba biến | [SCST](https://arxiv.org/abs/1612.00563), [Liang](https://arxiv.org/abs/2503.01333) |
| Đ5 | GRPO + METEOR | **Đang chạy** | Phần thưởng | Kaggle | Xong | Thêm một hàng bảng phần thưởng × độ đo; kiểm dấu hiệu chơi độ đo | [SCST](https://arxiv.org/abs/1612.00563), [AREL](https://aclanthology.org/P18-1083/) |
| Đ6 | GRPO + ROUGE-L | **Đang chạy** | Phần thưởng | Kaggle | Xong | Như trên | [Paulus](https://arxiv.org/abs/1705.04304), [AREL](https://aclanthology.org/P18-1083/) |
| K1 | "GRPO bỏ chia std" (mã `drgrpo`) | Sắp chạy | `scale_rewards="none"`, giữ β | Kaggle | Xong | Tác dụng của riêng việc chia std, **không gọi là Dr. GRPO** | [Dr. GRPO](https://arxiv.org/abs/2503.20783), [MathForge](https://arxiv.org/abs/2601.20614) |
| K2 | GRPO + BLEU-4 | Sắp chạy | Phần thưởng | Kaggle | Xong | Hàng trong bảng phần thưởng | [SCST](https://arxiv.org/abs/1612.00563), [Liu](https://arxiv.org/abs/1612.00370) |
| K3 | GRPO + chrF | Sắp chạy | Phần thưởng | Kaggle | Xong | Độ đo ký tự; ghi chú không có tiền lệ làm phần thưởng nên khai là lựa chọn dự án | Không có trong ghi chú |
| K4 | GRPO + SPIDEr | Sắp chạy | Phần thưởng | Kaggle | Xong | Tiền lệ đúng nhất của ý dùng SPICE; so SPICE thuần với bản có CIDEr | [Liu](https://arxiv.org/abs/1612.00370) |
| K5 | GRPO + BERTScore | Sắp chạy | Phần thưởng | Kaggle nếu VRAM đủ sau probe (roberta-large trong vòng lặp), không thì Colab | Xong, chưa probe | Họ độ đo dựa trên embedding | RL4LMs liệt kê trong thư viện ([bài](https://arxiv.org/abs/2210.01241)) |

### Mới, ưu tiên một: thiếu là bị hỏi ngay

| Mã | Lượt | Đổi so với ck500 | Máy, lý do | Mã nguồn | Cho phép viết | Nguồn |
|---|---|---|---|---|---|---|
| A1 | **SFT tiếp** trên câu chuẩn | Không RL; cùng 1.000 câu nhắc, cùng lr, LoRA mới | Kaggle, chỉ train CE nên nhanh hơn GRPO | Cần sửa `_scripts/314/ds_raft314/ra_train.py`: script này nối tiếp từ ck500, đổi thành S1 + LoRA mới và khai lịch lr (đang cosine, ck500 là hằng số sau warmup). Lượt R-3 cũ của script đã chạy trên T4 ở 6,7 GiB | Mức tăng của ck500 có vượt "học thêm một chút" hay không. Đây là đòn còn mở từ (x20) và là mốc phổ biến nhất ở RLHF | [InstructGPT](https://arxiv.org/abs/2203.02155), [VinePPO](https://arxiv.org/abs/2410.01679), [ReMax](https://arxiv.org/abs/2310.10505), [SC-Captioner](https://arxiv.org/abs/2508.06125) |
| A2 | **SCST + CIDEr-D** | Hai yếu tố, có chủ ý | Kaggle | Bỏ phép chặn ở cả `main()` của `grpo_luoi.py` lẫn `make_nb.py` | Cấu hình mà người đọc chú thích ảnh chờ đợi; cùng Đ1, Đ4, ck500 tạo ô 2×2 thuật toán × phần thưởng và kiểm lại kết quả GRPO > SCST của Liang | [SCST](https://arxiv.org/abs/1612.00563), [Liang](https://arxiv.org/abs/2503.01333) |
| A3 | **PPO, λ=1,0** | Đầu giá trị (linear/MLP trên đặc trưng cuối), GAE, γ=1, μ>1 để clip hoạt động; μ ghi rõ | Kaggle nếu probe đạt; đỉnh hiện tại 12,7 GiB nên đo trên 50 câu nhắc dài nhất; tràn thì Colab | **Chưa viết**, VRAM chưa đo | Câu trả lời cho UI-TARS-2. Ngang nhau thì viết "bỏ critic không gây thiệt", không viết GRPO hơn PPO. Khai đổi hai yếu tố (mốc, μ) | [R1](https://arxiv.org/abs/2501.12948), [Back to Basics](https://aclanthology.org/2024.acl-long.662/), [VinePPO](https://arxiv.org/abs/2410.01679), [UI-TARS-2](https://arxiv.org/abs/2509.02544) |
| A4 | **PPO, λ=0,95** | Như A3, đổi λ | Như A3 | Dùng lại A3 | Độ nhạy theo λ trên phần thưởng liên tục; cho thấy kết quả PPO không do chọn λ | [R1](https://arxiv.org/abs/2501.12948), [Back to Basics](https://arxiv.org/abs/2402.14740) |
| A5 | **DPO trực tuyến từ S1** | Mỗi bước lấy 8 mẫu, cặp tốt nhất/kém nhất theo SPICE, DPO với tham chiếu S1, bỏ nhóm hoà | Kaggle sau khi đổi sang fp16; script hiện `assert` đòi L4/A100; fp16 lỗi thì Colab L4 và khai đổi máy | Sửa từ `ga_dpo.py`: λ_nll=0, nguồn cặp mới | Cùng tín hiệu, khác mục tiêu tối ưu. Chép đúng khuôn Bridging, QRPO | [Bridging](https://arxiv.org/abs/2506.21495), [OAIF](https://arxiv.org/abs/2402.04792), [QRPO](https://arxiv.org/abs/2507.08068) |
| A6 | **DPO ngoại tuyến từ S1** | Lấy 8 mẫu từ S1 một lần, cặp cố định | Như A5 | Như A5 | Mốc RLHF chuẩn, và cho biết trực tuyến có quan trọng ở bài này không. **Đặt tiêu chí "có học": acc và biên trên tập dạy; không đạt thì báo "không học", không báo "thua"** | [DPO](https://arxiv.org/abs/2305.18290), [Bridging](https://arxiv.org/abs/2506.21495) |
| A7 | **RFT một vòng từ S1** | Lấy mẫu S1, giữ mẫu SPICE cao nhất, SFT | Kaggle; lượt RAFT cũ đã chạy cả sinh mẫu lẫn SFT trên T4 | Sửa từ `raft_mau.py`, `raft_chon.py`, đổi điểm đầu thành S1 | Hàng đúng của bài gốc GRPO; thay lượt RAFT cũ chạy từ ck500, vốn chỉ là "học thêm sau GRPO" | [DeepSeekMath](https://arxiv.org/abs/2402.03300), [RAFT](https://arxiv.org/abs/2304.06767), [Back to Basics](https://aclanthology.org/2024.acl-long.662/) |
| A8 | **Online RFT từ S1** | Mỗi bước lấy mẫu từ chính sách hiện tại, CE trên mẫu tốt nhất | Kaggle | Viết mới, ngắn | Dùng mẫu tốt không cần lợi thế có đủ hay không. Cùng A7 lặp lại bố cục hình so sánh của bài GRPO | [DeepSeekMath](https://arxiv.org/abs/2402.03300) |
| A9 | **DAPO lõi** (bỏ KL, không dynamic sampling) | β=0 | Kaggle, nhẹ hơn vì không cần tham chiếu | `grpo_luoi.py` có sẵn `--beta`, `make_nb.py` cần truyền thêm cờ; TRL tự bỏ tham chiếu khi β=0, chưa chạy thử nên phải probe | Hàng DAPO theo khuôn MathForge và Lian. **Phải nói rõ clip và overlong không có tác dụng ở đây.** Ô thứ ba của 2×2 | [DAPO](https://arxiv.org/abs/2503.14476), [MathForge](https://arxiv.org/abs/2601.20614), [Lian](https://arxiv.org/abs/2512.07611) |
| A10 | **Dr. GRPO đủ** | Bỏ chia std, β=0 | Kaggle | `--algo drgrpo --beta 0`, thêm `loss_type="dr_grpo"` (TRL 0.29.1 có sẵn, chia cho hằng số `max_completion_length`); probe trước | Hàng Dr. GRPO đặt tên đúng; ô thứ tư của 2×2; tách công của std và KL | [Dr. GRPO](https://arxiv.org/abs/2503.20783), [DARO](https://arxiv.org/abs/2510.09001), [Art of Scaling](https://arxiv.org/abs/2510.13786) |
| A11 | **GRPO gộp theo câu** | `loss_type="grpo"` thay vì `"dapo"` (hợp lệ trong TRL 0.29.1, tài liệu của TRL cảnh báo lệch theo độ dài câu) | Kaggle | Một cờ | Khoá đòn "ck500 không phải GRPO"; [suy] đồng thời là GSPO ở μ=1. Tiền lệ so cách gộp token | [λ-GRPO](https://arxiv.org/abs/2510.06870), [GUI-G1](https://arxiv.org/abs/2505.15810) |
| F1 | **Đo hình thức câu**, không train | Trên câu đã sinh của mọi nhánh: lặp cụm, kết thúc lỗi, độ dài | CPU máy nhà hoặc Kaggle CPU | Viết mới, ngắn | Trả lời trực tiếp nhận xét của Liu về PG-SPICE, bằng số | [Liu](https://arxiv.org/abs/1612.00370), [Guo](https://arxiv.org/abs/1809.06227) |

### Mới, ưu tiên hai: làm bảng đầy đủ và trả lời câu hỏi tiếp theo

| Mã | Lượt | Đổi so với ck500 | Máy, lý do | Mã nguồn | Cho phép viết | Nguồn |
|---|---|---|---|---|---|---|
| B1 | DAPO đủ | β=0 + thay nhóm thưởng không đổi bằng nhóm mới | Kaggle | Viết mới (TRL 0.29.1 không có sẵn) | Dynamic sampling có giúp không. Đặc biệt đáng đo vì nhóm thưởng bằng nhau ở log ck500 chiếm trung bình 20 đến 31% | [DAPO](https://arxiv.org/abs/2503.14476), [Lian](https://arxiv.org/abs/2512.07611) |
| B2 | Chuẩn hoá theo lô | A chia std của lô thay vì của nhóm | Kaggle | TRL có sẵn `scale_rewards="batch"` | Phạm vi chuẩn hoá có quan trọng không. [suy] gần với REINFORCE++ khi giữ G=8; dùng `RLOO`/`GRPO` của dự án làm so | [REINFORCE++](https://arxiv.org/abs/2501.03262), [Tricks or Traps](https://arxiv.org/abs/2508.08221), [Art of Scaling](https://arxiv.org/abs/2510.13786) |
| B3 | Vanilla PG | A = r, không mốc | Kaggle | Một nhánh | Sàn của trục mốc trừ | [Back to Basics](https://aclanthology.org/2024.acl-long.662/), [SCST](https://arxiv.org/abs/1612.00563) |
| B4 | Actor-critic một lượt | Đầu giá trị, λ=1, μ=1 | Kaggle nếu A3 vừa | Dùng lại A3 | Đổi đúng một yếu tố (mốc học được). Không gọi là PPO vì clip không hoạt động. Tách công của critic khỏi công của μ | [PRIME](https://arxiv.org/abs/2502.01456), [Bahdanau](https://arxiv.org/abs/1607.07086) |
| B5 | PPO, critic đủ cỡ | Critic riêng, có huấn luyện trước mô hình giá trị | Kaggle: critic ở GPU 2; không khả thi thì **Colab**, A100 nếu L4 tràn | Viết mới | Chặn câu "PPO của em chỉ có đầu giá trị nhỏ". Báo thêm sai số dự đoán của critic, vì ghi chú không thấy bài nào đo đại lượng này trên thưởng LLM | [UI-TARS-2](https://arxiv.org/abs/2509.02544), [InstructGPT](https://arxiv.org/abs/2203.02155), [DeepSeekMath](https://arxiv.org/abs/2402.03300) |
| B6 | ORPO từ S1, mức câu | Cùng cặp A6, NLL + odds ratio, không tham chiếu | Như A5 | Thêm vào script A5 | Khác MIN-DESC cũ (từ S2, mức khai báo). Đối chiếu cả ORPO và DPO trên một nguồn cặp | [ORPO](https://aclanthology.org/2024.emnlp-main.626/), [KTO](https://arxiv.org/abs/2402.01306) |
| B7 | DPO bán trực tuyến | Lấy mẫu lại định kỳ | Như A5 | Thêm vào script A5 | Bridging cho thấy gần ngang trực tuyến, nên đáng biết với chi phí sinh ít | [Bridging](https://arxiv.org/abs/2506.21495), [ReST](https://arxiv.org/abs/2308.08998) |
| B8 | GPG | Chuẩn hoá và ngưỡng theo bài, không KL, không tham chiếu | Kaggle | Viết mới; phải đọc công thức từ bài, ghi chú không đủ | Một đại diện critic-free đã qua bình duyệt | [GPG](https://arxiv.org/abs/2504.02546), [MathForge](https://arxiv.org/abs/2601.20614) |
| B9 | GRPO + SPICE từ Base | Xuất phát từ mô hình gốc, không S1 | Kaggle; câu Base dài hơn nên đo thời gian trước | Đổi `--merged` | S1 có cần không. Ghi chú nêu chưa thấy bài nào kiểm giả thuyết "khởi tạo mạnh" bằng cách đổi điểm đầu | [Back to Basics](https://arxiv.org/abs/2402.14740), [RL4LMs](https://arxiv.org/abs/2210.01241) |
| B10 | GRPO + BCMR | Phần thưởng tổ hợp 4 độ đo | Kaggle; METEOR chạy được theo probe | Thêm một phần thưởng; lấy trọng số từ bài | Đối thủ trực tiếp của SPIDEr trong chính bài gốc. Trái với lưu ý của Rennie thì càng đáng báo | [Liu](https://arxiv.org/abs/1612.00370), [SCST](https://arxiv.org/abs/1612.00563) |
| B11 | G=4 | Cỡ nhóm | Kaggle | Cờ `--G` | Độ nhạy theo ngân sách mẫu | [Reinforce-Ada](https://arxiv.org/abs/2510.04996), [Back to Basics](https://aclanthology.org/2024.acl-long.662/) |
| B12 | G=16 | Cỡ nhóm | Kaggle nếu `--gen-chunk` đủ, tràn thì Colab | Cờ `--G` | Như trên | Như trên |
| B13 | GRPO μ=2 | Clip bắt đầu hoạt động | Kaggle, thời gian đo lại | `num_iterations=2`; cờ mới | Mốc cần cho B14, B15 | [GSPO](https://arxiv.org/abs/2507.18071) |
| B14 | GSPO μ=2 | Tỉ số mức câu; so **với B13** | Kaggle | TRL có sẵn `importance_sampling_level="sequence"` | Phần riêng của GSPO. Chỉnh dải clip như bài đã làm | [GSPO](https://arxiv.org/abs/2507.18071), [Art of Scaling](https://arxiv.org/abs/2510.13786) |
| B15 | Clip-Higher μ=2 | Dải clip bất đối xứng; so **với B13** | Kaggle | `epsilon_high` của TRL | Phần riêng của DAPO mà A9 không đo được | [DAPO](https://arxiv.org/abs/2503.14476) |

**Tuỳ chọn:** C1 là DGPO, đổi std thành mean absolute deviation, một công thức một dòng và có bài báo cáo +2,18 khi kèm phần khác ([MathForge](https://arxiv.org/abs/2601.20614)). C2 là SimPO trên cùng cặp A6, vì QRPO dùng SimPO làm đại diện ngoại tuyến cạnh tranh ([QRPO](https://arxiv.org/abs/2507.08068)). Làm khi tổng hợp xong mà hội đồng vẫn muốn thêm dòng.

**Khối lượng, chỉ để lập lịch:** [suy] 148 s/bước × 500 ≈ 20,6 giờ cho một lượt GRPO, hai lượt chung một commit hai GPU, cần hai commit, cộng khoảng 5,6 giờ sinh và chấm. 28 lượt mới cỡ GRPO mất khoảng 445 giờ hạn mức, tức khoảng 5 tuần trên ba tài khoản Kaggle (mỗi tài khoản 30 giờ một tuần). Không có lượt nào bị bỏ vì con số này.

### Không chạy và lý do (bản đầu, một phần đã bị mục mở rộng bên dưới thay)

| Phương pháp | Lý do (không phải chi phí) |
|---|---|
| SAC, A2C, A3C, TD3, TRPO | Không bài nào trong mẫu dùng làm mốc so; thiếu chúng không lạ với người đọc mảng này ([LUFFY](https://arxiv.org/abs/2504.14945) chỉ nhắc khi nêu ví dụ) |
| KTO | Có cặp rồi nên không cần dạng không cặp; QRPO bỏ KTO vì lệch mục tiêu và vì kết quả của SimPO ([QRPO](https://arxiv.org/abs/2507.08068)). Số GSM8k của KTO cao ([bảng 2](https://arxiv.org/abs/2402.01306)) nhưng là bài đề xuất |
| ReMax riêng | Cùng ý mốc greedy với SCST; Đ1 đại diện, viết rõ quan hệ sau khi đối chiếu lời văn. Chú ý bản SCST của dự án là 8 mẫu + 1 greedy |
| VinePPO, SPO, GRPO-λ | Giải quyết phân công tín dụng theo đoạn trong suy luận nhiều bước, ít gặp làm mốc (VinePPO 2/42); [suy] câu khoảng 8 token có ít đoạn để chia |
| NLPO, APA, P3O, REBEL, QRPO, CISPO, GVPO và các đề xuất mới khác | Xuất hiện chủ yếu như phương pháp của chính bài, tần suất làm mốc 0 đến 2. Chạy thêm không đổi cách trả lời "đã so với các mốc chuẩn" |
| Best-of-N | Mốc của bài ngoại tuyến (3/12) dùng mô hình thưởng lúc suy luận; ở đây phần thưởng cần câu chuẩn nên chỉ là oracle, không phải thuật toán |
| So với GUI-R1, UI-R1 hoặc mô hình GUI khác | Khác dữ liệu, nền và phần thưởng nên không tách được thuật toán, đúng điểm yếu của 23/32 bài GUI |
| "GA-DPO" | Không phải phương pháp công bố ([ghi chú tra cứu](../research_notes/Baseline%20RL%20so%20v%E1%BB%9Bi%20GRPO/rlhf_preference.md)). Lượt của dự án xuất phát từ ck500, không học và không có điểm test. A5, A6 thay vai trò này |

### Mở rộng theo yêu cầu 1/11 tối: RL nói chung và phương pháp cổ điển

User muốn so với nhiều phương pháp, kể cả cổ điển, không giới hạn ở RL cho GUI. Bảng dưới **đè lên mục "Không chạy" ở chỗ mâu thuẫn**: lý do cũ là "ít bài dùng làm mốc", nay không còn là tiêu chí loại. Chỉ loại khi phương pháp không áp dụng được cho đầu ra rời rạc. Các hàng này lấy từ tra cứu riêng hôm 1/11, không thuộc mẫu 153 bài và không tính vào các tỉ lệ ở trên. Giữ nguyên điều kiện chung và gói chấm chung như các lượt khác.

**Chạy Kaggle, mã đã xong.** `harness/grpo_codien.py` chỉ đổi trọng số từng câu mẫu; selftest đạt và mỗi nhánh đã chạy 2 bước thật qua vòng lặp TRL trên CPU với mô hình tí hon. Chưa probe T4, nhưng cùng vòng lặp với GRPO nên [suy] cùng VRAM.

| Mã | Lượt (`--algo`) | Trọng số câu mẫu | Khai khi viết | Nguồn |
|---|---|---|---|---|
| B3 | `vanilla` | A = r | Không mốc trừ. Thưởng gần như luôn dương nên chỉ đẩy lên, không có vế đẩy xuống | Williams 1992, Machine Learning [chưa kiểm]; [Back to Basics](https://aclanthology.org/2024.acl-long.662/) |
| A8 | `rft` | 1 cho câu tốt nhất nhóm | Online RFT, mã này thay cho "viết mới" ở hàng A8 | [DeepSeekMath](https://arxiv.org/abs/2402.03300) |
| E1 | `cem` | 1 cho 25% câu tốt nhất | Cross-entropy method áp lên câu mẫu | Rubinstein 1999 [chưa kiểm] |
| E2 | `awr` | exp((r − TB nhóm)/τ), chặn 20 | Mốc là TB nhóm thay cho mô hình giá trị, nên là **kiểu AWR**. τ = 0,2 do dự án chọn | [AWR](https://arxiv.org/abs/1910.00177) [Pre] |
| E3 | `raml` | G·softmax(r/τ) | **Kiểu RAML**: mẫu lấy từ chính sách, không lấy từ q* như bài gốc. Gần E2; nếu kết quả trùng thì đếm là một | [RAML](https://arxiv.org/abs/1609.00150), NeurIPS 2016 [S] |
| E4 | `rank` | Thứ hạng trong nhóm về [−0,5; 0,5] | Fitness shaping của ES, không phải ES đầy đủ | [ES](https://arxiv.org/abs/1703.03864) [Pre] |
| C1 | `mad` | (r − TB)/độ lệch tuyệt đối TB | Chuyển từ tuỳ chọn lên chạy | [MathForge](https://arxiv.org/abs/2601.20614) |

A9 và A10 đổi β=0 cũng đã chạy qua vòng lặp đó trên CPU. `make_nb.py` chưa nhận các nhánh này và chưa truyền `--beta`, sẽ sửa lúc đẩy lượt.

**Chạy Kaggle, phải viết mã trước.** Khi viết xong mỗi hàng phải qua selftest, chạy CPU và probe T4.

| Mã | Lượt | Cần thêm | Nguồn |
|---|---|---|---|
| E5 | MRT | Log-xác suất cả câu của từng mẫu | [Shen](https://aclanthology.org/P16-1159/), ACL 2016 [S] |
| E6 | Softmax policy gradient | Như E5 | [Ding & Soricut](https://proceedings.neurips.cc/paper/2017/hash/faafda66202d234463057972460c04f5-Abstract.html), NeurIPS 2017 [S] |
| E7 | MIXER (bản rút gọn, khai rõ) | Nối tiền tố câu chuẩn với phần sinh, giảm dần | [MIXER](https://arxiv.org/abs/1511.06732), ICLR 2016 [H] |
| E8 | Trộn RL + CE trên câu chuẩn | Thêm một lượt forward câu chuẩn mỗi bước | [Paulus](https://arxiv.org/abs/1705.04304), [SCST](https://arxiv.org/abs/1612.00563) |
| E9 | SeqGAN | Bộ phân biệt làm phần thưởng. Khai là đổi cả phần thưởng | [SeqGAN](https://ojs.aaai.org/index.php/AAAI/article/view/10804), AAAI 2017 [S] |
| E10 | Quark | Điều kiện theo mức thưởng, đổi câu nhắc. Decision Transformer cùng ý nên không chạy riêng | [Quark](https://proceedings.neurips.cc/paper_files/paper/2022/hash/b125999bde7e80910cbdbd323087df8f-Abstract.html), NeurIPS 2022 [S] |
| E11 | ES trên trọng số LoRA | Không dùng gradient; dò nhiễu rồi chấm câu sinh | [ES](https://arxiv.org/abs/1703.03864) [Pre] |
| B4 | A2C (đổi tên từ "Actor-critic một lượt") | Đầu giá trị, dùng chung mã với A3. A3C cho cùng gradient kiểu này nên A2C đại diện | [A3C](https://proceedings.mlr.press/v48/mniha16.html), ICML 2016 [S] |

**Cần Colab hoặc chưa chắc chạy nổi trên T4: chỉ ghi lại, user quyết sau.** Lý do bên dưới là [suy] từ cấu trúc thuật toán, chưa đo.

| Mã | Lượt | Vì sao có thể không vừa T4 | Mức quan trọng theo tôi |
|---|---|---|---|
| CL1 | B5, PPO critic đủ cỡ | Thêm một mô hình giá trị cỡ lớn | **Cao**, chặn câu hỏi về UI-TARS-2 |
| CL2 | TRPO | Tích Fisher-vector cần đạo hàm bậc hai và nhiều lần lặp liên hợp mỗi bước, khó đi với gradient checkpointing và fp16 | Trung bình: tổ tiên trực tiếp của PPO, thầy có thể nhắc |
| CL3 | ILQL | Đầu Q, V và mạng đích. Chỉ dùng được khi học offline từ mẫu S1 | Trung bình: đại diện họ Q-learning cho ngôn ngữ ([ILQL](https://arxiv.org/abs/2206.11871), ICLR 2023 [S]) |
| CL4 | SAC rời rạc | Hai đầu Q, mạng đích và replay trên từ vựng 151.936 token | Thấp: bản rời rạc là preprint ([Christodoulou](https://arxiv.org/abs/1910.07207)), không có tiền lệ cho sinh câu trong phần đã tra |

**Không chạy vì không áp dụng được:** TD3 và DDPG là thuật toán cho hành động liên tục, còn token là rời rạc. Muốn chạy phải thêm phép nới liên tục, khi đó không còn là thuật toán gốc. DQN thuần cũng không đi thẳng được với từ vựng cỡ này; CL3 đại diện họ này.

**Luật đọc khi so nhiều nhánh.** Khoảng 50 phép so với ck500 ở ngưỡng p < 0,05 thì dù không có khác biệt thật vẫn kỳ vọng khoảng 2,5 phép "có ý nghĩa". Vì vậy bảng cuối phải hiệu chỉnh Holm và in cả p gốc lẫn p đã hiệu chỉnh. So nhiều nhánh giúp thấy GRPO + SPICE đứng ở đâu, **không bảo đảm nó đứng đầu**; kết quả phải báo vô điều kiện, kể cả khi ck500 thua.

**Khối lượng cập nhật:** [suy] khoảng 50 lượt trên Kaggle, gồm 11 lượt đã có trong kế hoạch, tức khoảng 795 giờ hạn mức, chừng 9 tuần trên ba tài khoản nếu chạy liền, tới khoảng đầu tháng 1/2027. Con số này sát mốc trình thầy, nên làm theo thứ tự: A1–A3 và F1, các lượt cổ điển mã đã xong, rồi tới phần còn lại.

## Những câu không được viết, kể cả khi số đẹp

| Không viết | Vì sao | Viết thay |
|---|---|---|
| "GRPO + SPICE là tốt nhất" (khi chỉ có một hạt) | Hai hạt ck500 chênh 0,72, +1,55 còn dưới MDE 2,11; nhiều hạt mới hoãn | "Trong lưới một hạt giống, ck500 không thua lượt nào có KTC loại 0" hoặc đúng thứ tự thực tế, kèm nhãn |
| "Bỏ critic làm kết quả tốt hơn" | Ghi chú cho thấy lý do chính là chi phí; R1, Lian, FlowRL, VinePPO không cho thấy PPO kém khi đã chỉnh | "Lý do chọn là chi phí và tiền lệ; A3, A4 đo kết quả cụ thể trên bài này" |
| "Đầu tiên dùng RL sinh hướng dẫn trên AndroidControl" | Ghi chú chỉ thấy mẫu không có, không phải chứng minh; luật dự án cấm "đầu tiên" | "Trong các bài đã khảo sát, AndroidControl dùng cho dự đoán thao tác, định vị hoặc mô hình thế giới" |
| "GRPO hơn SCST" dẫn Liang như đã rõ | Preprint, nền yếu, không thấy nhiều hạt | Dẫn kèm nhãn preprint, rồi báo số của Đ1, Đ4, A2 |
| Đọc số val trong lưới hoặc kiểm tra sơ bộ thành kết quả | Luật dự án cấm trích; val phóng đại khoảng cách | Chỉ dùng giải thích, không in số |
| "DAPO" cho A9, "Dr. GRPO" cho K1, "PPO" cho B4, "GSPO" cho A11 | Mỗi lượt chỉ là một phần của phương pháp, xem mục mã | Tên mô tả đúng cấu hình, phương pháp gốc ghi ở chú thích |
| So thẳng số bài khác với 60,65 | Thước, dữ liệu và bộ chấm khác; Bridging cho thấy đổi bộ chấm đảo thứ tự | So trong cùng hàng của từng bài |
| Tỉ lệ 86%, 24%... là "ngành dùng" | Mẫu có chủ đích, gieo theo tên GRPO | "Trong mẫu N bài" |
| Dùng lượt GA-DPO hoặc MIN-DESC như thể là văn liệu về DPO, ORPO | Là kết quả nội bộ, khác điểm đầu và mức tác động | Ghi là lượt thử của dự án, tách khỏi phần khảo sát |

**Kiểm từng con số trước khi vào luận văn là bắt buộc.** Mọi số ở đây lấy từ trích văn bản PDF, chủ yếu bản arXiv, chưa đối chiếu bản đăng; ghi chú không đọc từng bài từ đầu tới cuối. Ghi chú còn **mâu thuẫn một chỗ**: nhóm RLVR ghi "RLOO k=2 72,1/37,7/58,4", còn nhóm RLHF ghi dãy đó là RAFT k=2 và RLOO k=2 là 74,2/47,6/62,2. Con số 74,2 mà REBEL chép lại ủng hộ bản RLHF, tôi dùng bản đó, nhưng phải mở Bảng 1 để xác nhận. Cần đặc biệt đối chiếu số VinePPO (trích từ hình theo thứ tự giả định), số ReMax ở Hình 7, hàng GVPO, các số ReMax/PPO mà REBEL chép, và các lý do của [Zhang 2021](https://doi.org/10.1016/j.imavis.2021.104126) (PPO cho chú thích ảnh, chỉ đọc qua tóm tắt tìm kiếm, không có số của bài).

**Venue chưa xác minh tận nguồn:** AAPO (ACL 2026, chỉ ở chú thích arXiv, URL thử trả 404), Dr. GRPO (COLM 2025, chỉ đầu PDF), RL4LMs và MIXER (ICLR, chỉ đầu PDF vì OpenReview chặn), Table-R1 (EMNLP 2025, chưa rõ main hay Findings), PAPO và Vision-R1 của Huang (ICLR 2026, tác giả tự ghi), Co-EPG và GUI-RCPO (AAAI 2026, tác giả tự ghi), GUI-Cursor (ICML 2026, tác giả tự ghi), InfiGUI-G1, GUI-Eyes và DigiRL (chỉ OpenAlex), DPO, ORPO, SimPO ở mức trang kỷ yếu nhưng số lấy từ arXiv, VEM (TMLR chỉ từ một danh sách thứ cấp, xem như preprint), APA chưa xác minh, OAIF ghi preprint vì không thấy trong các tập đã quét. Lian, Bridging, REINFORCE++, CPGD, TGRL, UI-TARS-2, Liang, Luo và ACST đều là [Pre]: dẫn được nhưng phải kèm nhãn, và "preprint" ở đây chỉ nghĩa là chưa tìm thấy venue do một phần API bị giới hạn lượt gọi. Có hai bài cùng tên Vision-R1, nên khi dẫn phải ghi đúng tác giả.

## Kết luận

Điều đáng giá nhất tài liệu cho luận văn không phải một xếp hạng, vì khoảng cách giữa các phương pháp không có critic thường nhỏ, đổi dấu theo bài và phụ thuộc cách cài đặt: mức tăng do RL trong [SCST](https://arxiv.org/abs/1612.00563) lớn hơn hẳn chênh lệch giữa các thuật toán RL với nhau. Vì vậy câu hỏi của thầy nên được trả lời theo thứ tự ngược với trực giác: trước hết chứng minh RL hơn SFT tiếp và hơn phương án lọc mẫu, sau đó cho thấy các lựa chọn mốc trừ khác biệt tới đâu, và chỉ khi có đủ dữ liệu mới nói GRPO cùng SPICE có phải lựa chọn tốt nhất hay chỉ là một lựa chọn đủ tốt. Nếu nhóm lượt không critic rơi vào cùng một dải, phần giải thích theo cơ chế sẽ phải trả lời vì sao chúng ngang nhau; đó vẫn là kết luận có giá trị và trung thực hơn lời khẳng định một người thắng.

Nên ưu tiên ngay A1, A2 và A3 trong số các lượt mới, vì mỗi lượt chặn một câu hỏi rất dễ gặp (SFT, chuẩn chú thích ảnh, PPO), và F1 vì tốn rất ít nhưng trả lời nhận xét của chính bài SPIDEr về SPICE thuần. Nếu A3 và A4 cho thấy PPO ngang hoặc hơn GRPO, luận văn vẫn đứng vững vì lý do chọn đã nói từ đầu là chi phí và sự đơn giản; chỉ nên đổi phương pháp chính khi kết quả hơn rõ và lặp lại khi nhiều hạt giống được khôi phục.
