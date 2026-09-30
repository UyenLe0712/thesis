# Tài liệu ngày 29/09/2026

- [`253_ACTION_GRPO_SPICE_S1_29_9_checked.md`](253_ACTION_GRPO_SPICE_S1_29_9_checked.md): action
  train GRPO thưởng SPICE cho S1/101, nhánh ablation "S1 + GRPO, tắt đầu khe". Ba pha: thăm dò
  (Kaggle T4, tương tác) → train 500 bước (commit) → sinh greedy val C1 + chấm `exec`, rồi đọc bằng
  Phụ lục B trên WSL.
- Bản chạy được của Phụ lục A: `harness/grpo_spice.py` (tách từ file này, đã sửa lỗi `n_`).
  Gói upload Kaggle `grpo-spice-script`: `_bundles/grpo-spice-script/` (dựng lại bằng hai lệnh `cp`
  ở mục 3 của file).
- Bản gốc soạn cho máy Mac; đã đổi đường dẫn sang WSL và sửa ba lỗi, ghi ở đầu file.
- Kết quả tải về đặt ở `runs/grpo_spice/`.
