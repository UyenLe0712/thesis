# 312 — Kết quả cổng G0 của RA-GRPO (12/10/2026) — KHÔNG ĐẠT, dừng hướng RA-GRPO

Action: `report/312_ACTION_RA_GRPO_KAGGLE_12_10_extracted.md`. Mã: `harness/ra_grpo/`.
Notebook: `_scripts/312/kaggle/nb_ra-grpo-g0-312/` (Kaggle `uyenle0712/ra-grpo-g0-312`, T4 ×2, ~1,6 h).
Dataset: `uyenle0712/ra-grpo-312` (= `ra-sft-script` của lượt 304 + 3 script 312 + `pred_S1_vallon.jsonl`).
Tệp thô: `runs/rag312/g0/`. **Số val, cấm trích.**

## Kết quả

Greedy S1 hoà trên 1.002 bước click val (không khối là `pred_S1_vallon` của lượt 289):

| | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF |
|---|---:|---:|---:|---:|---:|---:|
| S1 không khối | 54,13 | 38,51 | 70,20 | 449,71 | 47,34 | 63,50 |
| **S1 có khối** | 39,17 | 29,03 | 56,44 | 291,46 | 32,55 | 50,43 |
| ck500 | 54,81 | 39,25 | 70,52 | 448,95 | 49,22 | 64,50 |

S1 có khối đổi câu ở 78,5% bước, chép nguyên văn một câu mẫu ở 46,0% bước, và trong số câu chép
chỉ 11,3% trùng câu chuẩn.

8 mẫu T = 1,0 trên 300 bước val (hạt 20261012):

| | best-of-8 SPICE | best-of-8 CIDEr-D | có mẫu trùng câu chuẩn | mẫu trùng câu mẫu |
|---|---:|---:|---:|---:|
| không khối | 68,59 | 614,5 | 37,3% | 7,6% |
| **có khối** | 53,75 | 441,0 | 22,7% | 32,6% |

Ở 40 bước khối chứa đúng câu chuẩn: có mẫu chép đúng 62,5% (có khối) so với 52,5% (không khối).

## Đọc theo luật cổng

- G0-1 (trần): có khối − không khối = SPICE **−14,8**, CIDEr-D **−173** ⇒ không đạt (cần ≥ +1,0 / +10).
- G0-2 (mốc KL): greedy CIDEr-D **−158**, SPICE **−14,8** ⇒ không đạt (cho phép tối đa −10 / −1,0).
- ⇒ **KHÔNG ĐẠT, dừng RA-GRPO.** Không rơi vào nhánh "Phương án B" vì G0-2 cũng trượt.

Cơ chế: S1 chưa từng thấy khối nên không bỏ qua nó mà **bị nó kéo đi**. S1 chép câu của bước
tương tự ở tác vụ khác (ví dụ viết "Swipe up to view…" theo câu mẫu, trong khi câu đúng là một lần
chạm). Chỉ ở số ít bước khối chứa đúng câu chuẩn thì việc chép mới có lợi (+10 điểm phần trăm). Mẫu
của nhóm có khối kém hẳn, nên GRPO xuất phát từ S1 không có mẫu tốt hơn để thưởng, và mốc KL (S1
nhìn khối) đã kém sẵn.

## Đã sửa trong mã 312 trước khi chạy

- `ra_grpo_g0.py`: `proc, model, _, _ = GS.nap(a)` → `proc, model, _ = GS.nap(a)` (`nap` trả 3 giá trị;
  để nguyên thì G0 chết ngay lúc nạp mô hình).
- `doc_exec_cw.py`: `runs/score_s1_seed101_ra.jsonl` → `_raw.jsonl` (lỗi khi chép từ ảnh).
- Thêm đường dẫn WSL cho `--tu-kiem`. Năm phép tự kiểm CPU đều ĐẠT, tái lập R3.
- Notebook T (`_scripts/312/kaggle/nb_ra-grpo-t-312/`) đã dựng, **không đẩy**.
