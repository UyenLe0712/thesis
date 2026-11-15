# 336. Việc cần làm sau 15/11/2026

Ghi lúc 15/11 tối, sau khi SA-SPICE-v3 ck400 đã đủ số test (vị trí, không chạm, văn bản; commit `23bb59e`). Chưa việc nào dưới đây được chạy. **Mọi lượt GPU phải hỏi user trước** ("hỏi rồi tôi chốt, đừng chạy liền").

Nguồn: phán quyết debate `research_notes/Debate SA SPICE v3 sau test/03_phan_quyet.md`, `report/329` (độ phổ biến RL), `report/334` (bảng kết quả).

## 1. Đang chạy

| việc | ở đâu | việc khi xong |
|---|---|---|
| SPICE-MATCH (SPICE thuần từ SFT-cont, seed 101, 500 update) | Colab L4 phiên `match`, bắt đầu ~20:40 15/11, ~12 h | tải điểm lưu về `_bundles/sa3_grpo/ck_match/`, `colab stop -s match`, chấm DEV-v3 ck400/ck500 trên Kaggle T4, rồi chấm test (vị trí + không chạm + văn bản). Khai: card L4 thay T4 (đã ép fp16) |

## 2. Việc cần làm, theo thứ tự

| # | việc | vì sao | máy, chi phí [suy] | trạng thái |
|---|---|---|---|---|
| 1 | **DPO trực tuyến** từ S1, thưởng SPICE (user chọn 15/11) | thuật toán phổ biến nhất còn thiếu ở phía RL cho LLM (mốc so ở 15/30 bài RLHF, report/329 §2); lưới đã có GRPO, PPO, REINFORCE, RLOO, SCST | viết mã + selftest CPU, rồi probe T4, rồi Kaggle T4 ~20 h | đang thiết kế, chưa viết mã (§3) |
| 2 | SA-SPICE-v3 seed 401 và 503, công thức y hệt, chọn điểm lưu trên DEV-v3 bằng cùng tiêu chí | mọi số SA chỉ một seed, A/A lệch 0,72–0,92 exec | Kaggle T4×2, ~20 h/lượt, hai tài khoản song song | chờ user chốt tài khoản |
| 3 | Đưa lưới RL + trục thưởng + SA vào luận văn | thầy yêu cầu so họ RL và độ đo thưởng, giải thích vì sao; số đã ở report/334, report/320 §14–§29, `thesis/chapters/` chưa có | CPU | chờ user cho phép sửa `thesis/` |
| 4 | SA + câu nhắc phân tầng (back ~8%), tên riêng | chữa back không chạm 71,1 → 58,5 | Kaggle T4 ~20 h + DEV | luật đi tiếp ghi trước (DEV-v3): back ≥ 72/104, không chạm tụt ≤ 2 so SFT-cont, exec ≥ SA ck400 − 0,5 |
| 5 | Dr.GRPO chạy nốt 475 → 500 rồi chấm test | gần như không tốn, thêm một hàng | Kaggle T4 | chờ user |
| 6 | **R1** — phân rã SA − SFT tiếp (sửa loại thao tác / đổi phần tử) + hình thức câu của SA | giải thích vì sao SA tăng exec mà SPICE không tăng | Kaggle CPU, 0 GPU | chưa làm, chi tiết §2b |
| 7 | **R2** — GRPO + SPIDEr từ S1 | tiền lệ trực tiếp của SPICE làm thưởng (ICCV 2017) | Kaggle T4 ~20 h + test | mã có sẵn, chờ user |
| 8 | **R4** — GRPO + chrF từ S1 | đối thủ mạnh nhất ở sàng tĩnh, thành phần của SA | Kaggle T4 ~20 h + test | mã có sẵn, chờ user |
| 9 | **R3** — GRPO + BLEU-4 từ S1 | độ đo cổ điển nhất (MIXER) | Kaggle T4 ~20 h + test | mã có sẵn, chờ user |
| 10 | **R5** — GRPO + BERTScore từ S1 | đại diện độ đo học được | Kaggle T4, phải probe trước | chờ user |
| 11 | **R6** — Sparse-SPICE từ SFT-cont (sau SPICE-MATCH) | ablation thưởng composite | Kaggle T4 | chờ kết quả SPICE-MATCH |
| 12 | Tuỳ chọn: NT (back chấm theo loại thao tác) | chỉ khi #4 không cứu được back | — | — |
| 13 | RL cổ điển khác: A2C (mã + probe xong), DQN/soft-Q, TRPO, MIXER, MRT | so rộng hơn; DQN phổ biến nhất (41 bài) nhưng phải viết mã mới | MIXER/MRT sau khi hạn mức làm mới 21/11 | user chưa chọn, chỉ chọn DPO |

## 2b. Trục phần thưởng: còn làm được gì (đề xuất 15/11, user chưa chọn)

Đã có số test (từ S1, cùng mã lưới): SPICE (ck500, A/A), ROUGE-L, METEOR, CIDEr-D (3 lượt), SPICE ghép ngẫu nhiên (kiểm soát); từ SFT-cont: SA-SPICE-v3. Đã giải thích bằng CPU: H1–H5 (report/320 §15–§17), CIDEr-D thấp CIDEr-D (§22), sàng biến thể SPICE (§23). Chỗ hở lớn nhất: H2 (độ khớp exec của thưởng trên mẫu tĩnh) **không** dự đoán được thứ hạng sau train.

| # | việc | máy | vì sao |
|---|---|---|---|
| R1 | Phân rã mức tăng của SA − SFT tiếp (sửa loại thao tác / đổi phần tử, như §14.5) + hình thức câu (spaCy, như §14.7) | Kaggle CPU, 0 GPU | giải thích vì sao SA tăng exec dù SPICE không tăng; SA chưa có hai phép đo này |
| R2 | GRPO + SPIDEr từ S1 | Kaggle T4 ~20 h + sinh test | tiền lệ trực tiếp dùng SPICE làm thưởng (Liu et al., ICCV 2017); hội đồng dễ hỏi. Mã có sẵn (`grpo_luoi.py --reward spider`) |
| R3 | GRPO + BLEU-4 từ S1 | như trên | độ đo cổ điển nhất, thưởng của MIXER (Ranzato et al., ICLR 2016). Mã có sẵn |
| R4 | GRPO + chrF từ S1 | như trên | đứng đầu sàng tĩnh, là thành phần của SA; cho phép so SPICE vs chrF cùng điểm xuất phát S1. Mã có sẵn |
| R5 | GRPO + BERTScore từ S1 | như trên, chấm thưởng bằng roberta-large nên chậm hơn [suy] | đại diện độ đo học được. Mã có sẵn, chưa probe |
| R6 | SPICE-MATCH (đang chạy) rồi Sparse-SPICE từ SFT-cont | Colab L4 / Kaggle T4 | ablation cho thưởng composite |

Tranh chấp hạn mức Kaggle với DPO (#1) và SA hai seed (#2): mỗi lượt ~20 h T4, mỗi tài khoản 30 h/tuần.

## 3. Thiết kế DPO trực tuyến (chưa viết mã)

- **Giữ như lưới:** S1/101 hoà + LoRA mới cỡ S1, 1.000 câu nhắc (trùng thứ tự ck500), G = 8 mẫu/câu nhắc, temperature 1,0, lr 1e-5, 500 update (2 câu nhắc/update), seed 101, thưởng SPICE − 0,02·phạt độ dài.
- **Đổi:** hàm mất mát. Mỗi nhóm 8 câu: câu thưởng cao nhất = chosen, thấp nhất = rejected; nhóm có max − min < 1e-6 bỏ (không có tín hiệu). Loss = −log σ(β·[(log π_c − log π_ref,c) − (log π_r − log π_ref,r)]), log-prob tổng theo câu, β_DPO = 0,1 (mặc định DPO), π_ref = S1 (tắt adapter). Không có số hạng KL riêng (DPO đã ngầm có).
- **Cài vào `grpo_luoi.py` dạng lớp con (như `grpo_ppo.py`), không sửa mã lưới cũ.** Đọc TRL 0.29.1 (`grpo_trainer.py`) thấy ba chỗ phải xử:
  1. `_prepare_inputs` xáo thứ tự (`shuffle_sequence_dict`) rồi chia lô nhỏ 4 hàng ⇒ cặp chosen/rejected có thể rơi vào hai lô nhỏ khác nhau. Phải đặt 4 hàng cặp (2 nhóm × 2) vào đầu lô sinh và tắt xáo cho nhánh DPO; 3 lô nhỏ còn lại trả loss 0 không cần forward (rẻ hơn GRPO).
  2. Log-prob tham chiếu chỉ được TRL tính khi `beta != 0` ⇒ giữ `beta` của GRPOConfig ≠ 0 để có `ref_per_token_logps`, dùng β_DPO riêng trong loss.
  3. Thang loss: TRL đặt `model_accepts_loss_kwargs = False`; loss `dapo` tự chia theo `num_items_in_batch` của cả lô sinh ⇒ loss DPO trả về sao cho tổng qua các lô nhỏ = trung bình theo cặp. Phải kiểm bằng selftest CPU (mô hình tí hon) trước.
- **Ghi log:** số cặp hợp lệ/update, độ chênh thưởng chosen − rejected, phần thưởng ngầm (β·Δ), độ chính xác ngầm (tỉ lệ cặp có lề > 0).
- **Khai khi viết:** đây là DPO trực tuyến kiểu best-vs-worst trong khung lấy mẫu GRPO, không phải DPO ngoại tuyến; lần GA-DPO 13/10 (ngoại tuyến, cặp khác) không học được.
- **Không cần học được** (user 15/11): mục đích là có hàng so sánh; không học thì vẫn báo số.
- Bước tiếp: viết mã → selftest CPU → hỏi user → probe T4 ngắn → hỏi user → chạy đủ.
