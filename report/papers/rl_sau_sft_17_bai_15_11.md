# 17 bài RL/GRPO: có SFT trước không, đóng góp gì, generic hay specific (đọc 15/11/2026)

Câu hỏi: các bài RL nổi tiếng (nhất là GRPO) có SFT rồi mới RL hay RL thẳng, đóng góp của họ thuộc loại gì, và đóng góp đó dùng chung được (generic) hay chỉ cho một bài toán/dataset (specific).

**Cách đọc:** tải PDF từ arXiv, trích chữ, đọc phần quy trình huấn luyện và phần đóng góp tác giả tự nêu. Câu trong ngoặc kép là trích nguyên văn từ PDF. **Venue:** ✔ = PDF hoặc trang arXiv có in venue; ⚠ = chưa kiểm, phải kiểm trước khi đưa vào luận văn.

---

## 1. Kết luận nhanh

1. **Hai cách đều có.** RL thẳng từ base ("zero RL") chủ yếu nằm ở toán/suy luận có đáp án kiểm được, nơi mô hình gốc đã tự giải đúng một phần. SFT trước RL là cách làm khi đầu ra phải theo định dạng/văn phong riêng hoặc mô hình gốc còn yếu ở bài toán đó. Đây cũng là truyền thống của captioning (SCST, SPIDEr).
2. **Không bài nào nhận công ở bước SFT**, trừ khi dữ liệu SFT do họ tự dựng (Vision-R1, InfiGUI-R1). SFT chỉ là điểm xuất phát.
3. **Đóng góp generic** (thuật toán mới, công thức huấn luyện, phân tích chung) gần như toàn của lab lớn: DeepSeek, OpenAI, ByteDance, AI2, Moonshot, Qwen. Họ chứng minh trên rất nhiều benchmark với tài nguyên tính toán lớn.
4. **Bài ứng dụng vào một bài toán** dùng thuật toán có sẵn (GRPO/PPO). Đóng góp nằm ở **reward thiết kế cho bài toán**, **dữ liệu** hoặc **cách biểu diễn bài toán**. Đây là loại specific, phổ biến nhất ở mảng GUI và captioning.
5. **Đề tài (S1 → GRPO thưởng SPICE = ck500) thuộc loại specific**, cùng ô với SPIDEr và UI-R1: thuật toán có sẵn, đóng góp ở reward + bài toán + cách đánh giá.

---

## 2. Bảng tổng hợp

| # | bài | venue | SFT trước RL? | loại đóng góp | generic / specific |
|---|---|---|---|---|---|
| 1 | InstructGPT (2203.02155) | ⚠ | **Có**: SFT → reward model → PPO | công thức RLHF + mô hình + phân tích | generic |
| 2 | SCST (1612.00563) | ✔ CVPR 2017 | **Có**: mô hình cross-entropy làm "seed" | thuật toán | thuật toán generic, thí nghiệm captioning |
| 3 | SPIDEr (1612.00370) | ✔ ICCV 2017 | **Có**: MLE warm start | thuật toán + reward | thuật toán generic, reward captioning |
| 4 | DeepSeekMath (2402.03300) | ⚠ preprint | **Có**: Base → Instruct (SFT) → GRPO | dữ liệu + thuật toán GRPO + phân tích | cả hai |
| 5 | DeepSeek-R1 (2501.12948) | ✔ Nature 2025 | **R1-Zero không, R1 có** | phát hiện + công thức nhiều chặng + chưng cất | generic (miền kiểm được) |
| 6 | Kimi k1.5 (2501.12599) | ⚠ | **Có**: SFT → long-CoT SFT → RL | công thức + thuật toán (mirror descent) | generic |
| 7 | Tülu 3 (2411.15124) | ⚠ | **Có**: SFT, DPO, RLVR | công thức mở + dữ liệu + RLVR + đánh giá | generic |
| 8 | Qwen3 (2505.09388) | báo cáo kỹ thuật | **Có**: cold start → RL suy luận → … | công thức | generic |
| 9 | SFT Memorizes, RL Generalizes (2501.17161) | ✔ ICML 2025 | **Có**, và lập luận là cần | phân tích | kết luận generic, đo trên 2 môi trường |
| 10 | Vision-R1 (2503.06749) | ✔ ICLR 2026 | **Có**: cold start 200K CoT → GRPO | dữ liệu + chiến lược train | specific (toán đa phương thức) |
| 11 | InfiGUI-R1 (2504.14239) | ⚠ | **Có**: chưng cất suy luận → RL | reward + công thức 2 chặng | specific (GUI) |
| 12 | DAPO (2503.14476) | ⚠ | **Không**: RL thẳng trên base | thuật toán + hệ thống mở | generic |
| 13 | Dr. GRPO (2503.20783) | ✔ COLM 2025 | **Không** | phân tích + sửa thuật toán | generic |
| 14 | SimpleRL-Zoo (2503.18892) | ⚠ | **Không**, có thí nghiệm so với SFT trước | phân tích | generic (toán) |
| 15 | Visual-RFT (2503.01785) | ⚠ | **Không** | reward kiểm được theo tác vụ | khung generic, reward theo tác vụ |
| 16 | UI-R1 (2503.21620) | ⚠ | **Không**: GRPO trên Qwen2.5-VL-3B | reward + dữ liệu nhỏ | specific (GUI) |
| 17 | GUI-R1 (2504.10458) | ⚠ | **Không** | không gian hành động + dữ liệu | specific (GUI) |

---

## 3. Từng bài

### 3.1. Nhóm SFT trước rồi RL

**InstructGPT: Training language models to follow instructions with human feedback** · [arXiv 2203.02155](https://arxiv.org/abs/2203.02155) · ⚠ venue
- Quy trình: *"three steps of our method: (1) supervised fine-tuning (SFT), (2) reward model (RM) training, and (3) reinforcement learning via proximal policy optimization (PPO)"*.
- Đóng góp: công thức RLHF, mô hình InstructGPT (1,3B được ưa hơn GPT-3 175B), phân tích tính trung thực/độc hại. PPO có sẵn.
- Loại: generic.

**SCST: Self-critical Sequence Training for Image Captioning** (Rennie et al.) · [arXiv 1612.00563](https://arxiv.org/abs/1612.00563) · ✔ CVPR 2017
- Quy trình: mô hình cross-entropy làm điểm xuất phát; RL *"improve the seed cross-entropy trained model"*.
- Đóng góp: thuật toán, REINFORCE với mốc là chính câu greedy của mô hình lúc suy luận, thay cho mốc học được.
- Loại: thuật toán generic, thí nghiệm chỉ trên captioning COCO (thưởng CIDEr).
- Với đề tài: tiền lệ gần nhất về quy trình (sinh câu, độ đo so với câu chuẩn, SFT trước RL).

**SPIDEr: Improved Image Captioning via Policy Gradient optimization of SPIDEr** (Liu et al.) · [arXiv 1612.00370](https://arxiv.org/abs/1612.00370) · ✔ ICCV 2017
- Quy trình: *"To help 'warm start' the training, we pre-train the RNN decoder (stochastic policy) using MLE training, before switching to PG training."*
- Đóng góp: thuật toán (Monte Carlo rollout thay cho trộn MLE kiểu MIXER) + reward SPIDEr = SPICE + CIDEr.
- Loại: thuật toán generic, reward riêng cho captioning.
- ⚠️ **Câu hội đồng có thể hỏi:** *"optimizing SPICE produced long repetitive sentences… SPICE ignores syntactic quality"*. Đề tài thưởng SPICE nhưng có phạt độ dài, và số từ không tăng (7,19 vs 7,28 trên val, `report/254`). Khi trích SPIDEr nên khai rõ điểm này.

**DeepSeekMath** (Shao et al., bài đặt ra GRPO) · [arXiv 2402.03300](https://arxiv.org/abs/2402.03300) · ⚠ preprint
- Quy trình: DeepSeekMath-Base → *"mathematical instruction tuning"* thành DeepSeekMath-Instruct 7B → GRPO thành DeepSeekMath-RL 7B. RL nâng *"GSM8K: 82.9% → 88.2%, MATH: 46.8% → 51.7%"* so với bản Instruct.
- Đóng góp: dữ liệu toán từ Common Crawl (specific), GRPO (*"a variant … of PPO"*, generic), một khung chung xem RFT/DPO/PPO/GRPO là cùng một dạng (generic).
- Loại: cả hai.

**DeepSeek-R1** · [arXiv 2501.12948](https://arxiv.org/abs/2501.12948) · ✔ Nature 645 (2025)
- R1-Zero: *"relies exclusively on reinforcement learning without supervised fine-tuning"*, dùng GRPO.
- R1-Zero gặp *"poor readability and language mixing"* nên R1 thêm: cold-start SFT (vài nghìn mẫu) → RL → rejection sampling + SFT → RL.
- Về mô hình nhỏ: *"distilling more powerful models into smaller ones yields excellent results, whereas smaller models relying on the large-scale RL … may not even achieve the performance of distillation."*
- Đóng góp: phát hiện RL thuần làm nảy ra suy luận, công thức nhiều chặng, chưng cất.
- Loại: generic, nhưng chứng minh trên miền kiểm được (toán, code, STEM).

**Kimi k1.5** · [arXiv 2501.12599](https://arxiv.org/abs/2501.12599) · ⚠ venue
- Quy trình: *"pretraining, vanilla supervised fine-tuning (SFT), long-CoT supervised fine-turning, and reinforcement learning (RL)"*.
- Đóng góp: mở rộng ngữ cảnh dài cho RL, *"a variant of online mirror descent"* (không phải GRPO), long2short, công thức dữ liệu.
- Loại: generic.

**Tülu 3** (AI2) · [arXiv 2411.15124](https://arxiv.org/abs/2411.15124) · ⚠ venue
- Quy trình: SFT, DPO, RLVR (các bảng in theo thứ tự Tülu 3 SFT → DPO → RLVR).
- Đóng góp: công thức hậu huấn luyện mở hoàn toàn (dữ liệu, mã), phương pháp RLVR (RL với thưởng kiểm được), bộ đánh giá đa nhiệm.
- Loại: generic.

**Qwen3 Technical Report** · [arXiv 2505.09388](https://arxiv.org/abs/2505.09388) · báo cáo kỹ thuật
- Quy trình: *"Stage 1 Long-CoT Cold Start, Stage 2 Reasoning RL, Stage 3 Thinking Mode Fusion, Stage 4 General RL"*, mô hình nhỏ dùng chưng cất.
- Đóng góp: công thức huấn luyện.
- Loại: generic.

**SFT Memorizes, RL Generalizes** (Chu et al.) · [arXiv 2501.17161](https://arxiv.org/abs/2501.17161) · ✔ ICML 2025
- Kết luận: RL tổng quát hoá tốt hơn, SFT học thuộc; nhưng SFT vẫn cần trước RL vì *"SFT stabilizes the model's output format"*.
- Đóng góp: phân tích, không đề xuất mô hình.
- Loại: kết luận nêu generic, nhưng chỉ đo trên hai môi trường tự dựng (GeneralPoints, V-IRL).

**Vision-R1** · [arXiv 2503.06749](https://arxiv.org/abs/2503.06749) · ✔ ICLR 2026
- Quy trình: dựng *"200K multimodal CoT dataset"* làm cold start → GRPO, kèm chiến lược PTST. Hình 1 ghi rằng áp RL thẳng lên MLLM không khơi được suy luận hiệu quả.
- Đóng góp: dữ liệu + chiến lược train.
- Loại: specific (suy luận toán đa phương thức).

**InfiGUI-R1** · [arXiv 2504.14239](https://arxiv.org/abs/2504.14239) · ⚠ venue
- Quy trình: chặng 1 *"Spatial Reasoning Distillation"* (SFT trên quỹ đạo có suy luận), chặng 2 RL với reward *"Sub-goal Guidance"* và *"Error Recovery"*.
- Đóng góp: reward riêng + công thức 2 chặng.
- Loại: specific (GUI agent).

### 3.2. Nhóm RL thẳng

**DAPO** (ByteDance) · [arXiv 2503.14476](https://arxiv.org/abs/2503.14476) · ⚠ venue
- Quy trình: RL thẳng *"using Qwen2.5-32B base model"*.
- Đóng góp: thuật toán (*"four key techniques"*: decoupled clip, dynamic sampling…) + hệ thống mở.
- Loại: generic.

**Dr. GRPO: Understanding R1-Zero-Like Training** · [arXiv 2503.20783](https://arxiv.org/abs/2503.20783) · ✔ COLM 2025
- Quy trình: RL thẳng trên base.
- Đóng góp: phân tích mô hình base (*"DeepSeek-V3-Base already exhibit 'Aha moment'"*) + sửa *"an optimization bias in GRPO, which artificially increases response length"*.
- Loại: generic.

**SimpleRL-Zoo** · [arXiv 2503.18892](https://arxiv.org/abs/2503.18892) · ⚠ venue
- Quy trình: zero RL trên 10 mô hình base (Llama3, Mistral, Qwen2.5…).
- **Thí nghiệm SFT trước RL:** *"starting from SFT models initially boosts performance significantly; however, these models encounter notable limitations in their maximum achievable accuracy and response length"*, và càng SFT lâu thì giới hạn càng rõ.
- Đóng góp: phân tích.
- Loại: generic (toán).
- ⚠️ **Câu hội đồng có thể hỏi:** "SFT trước làm hạn chế trần của RL". Trả lời: họ đo trên suy luận toán với CoT dài, khác bài toán sinh câu theo văn phong. Ở đề tài SFT là cần: Base exec 47,6 vs S1 59,1, BLEU-4 15,3 vs 51,6. Lý do giống SCST, SPIDEr và Vision-R1.

**Visual-RFT** · [arXiv 2503.01785](https://arxiv.org/abs/2503.01785) · ⚠ venue
- Quy trình: GRPO thẳng.
- Đóng góp: *"different verifiable reward functions for different perception tasks, such as the Intersection over Union (IoU) reward"*.
- Loại: khung generic, reward theo từng tác vụ.

**UI-R1** · [arXiv 2503.21620](https://arxiv.org/abs/2503.21620) · ⚠ venue
- Quy trình: GRPO thẳng trên Qwen2.5-VL-3B, *"136 challenging tasks"*.
- Đóng góp: *"a novel rule-based action reward"* + dữ liệu nhỏ chọn lọc. Có báo kết quả trên AndroidControl.
- Loại: specific (GUI).

**GUI-R1** · [arXiv 2504.10458](https://arxiv.org/abs/2504.10458) · ⚠ venue
- Quy trình: GRPO, *"only 0.02% of the data (3K vs. 13M)"* so với OS-Atlas.
- Đóng góp: không gian hành động thống nhất cho nhiều nền tảng + dữ liệu.
- Loại: specific (GUI).

---

## 4. Áp vào đề tài

- **ck500 thuộc loại specific**, cùng ô với SPIDEr và UI-R1: thuật toán có sẵn (GRPO), đóng góp ở reward + bài toán (sinh câu hướng dẫn GUI) + cách đánh giá (exec bằng bộ trỏ độc lập). Đây là kiểu bài bình thường của mảng ứng dụng, không phải điểm yếu. Luận văn đã khai điểm mới hẹp, không nhận mới ở thuật toán hay ở việc chọn SPICE.
- **SFT trước RL có tiền lệ đủ:** SCST, SPIDEr, DeepSeekMath, R1, Kimi, Qwen3, Vision-R1, InfiGUI-R1.
- **Hai câu nên chuẩn bị trả lời:** SPIDEr (thưởng SPICE một mình cho câu dài lặp) và SimpleRL-Zoo (SFT trước giới hạn trần), xem các mục tương ứng ở trên.
- **Nếu SA-SPICE-v3 / SPICE-MATCH thắng rõ trên test**, đó là đóng góp reward đúng loại SPIDEr / UI-R1 / Visual-RFT.
- **Nếu không reward mới nào thắng**, đề tài vẫn đứng được ở loại phân tích (như SFT Memorizes, Dr. GRPO, SimpleRL-Zoo): độ đo nào làm thưởng thì đẩy được exec, và vì sao theo phân rã thành phần.

## 5. Việc còn treo

- Kiểm venue các bài ⚠ trước khi trích vào luận văn (InstructGPT, DeepSeekMath, Kimi, Tülu 3, InfiGUI-R1, DAPO, SimpleRL-Zoo, Visual-RFT, UI-R1, GUI-R1).
- Chưa kiểm UI-R1 / GUI-R1 xuất phát từ bản Qwen2.5-VL Base hay Instruct (PDF chỉ ghi "Qwen2.5-VL-3B").
- Văn bản trích từ PDF nằm ở scratchpad phiên 15/11 (tạm, có thể đã bị xoá); muốn đọc lại thì tải từ các link arXiv ở trên.
