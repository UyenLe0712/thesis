# `runs/grpo_point/` — lượt GRPO thưởng `<point>` nối tiếp MIN-DESC/101

Đăng ký: `report/106` mục **(x19)** · mã `harness/grpo_point.py` · runbook train
`harness/colab_grpo_point.md` · runbook suy luận + chấm `harness/kaggle_grpo_point_6_9.md`.

| tệp | là gì |
|---|---|
| `log_history.json` | `trainer.state.log_history` của lượt G5 — 501 bản ghi (500 bước + 1 dòng tổng kết) |
| `adapter_grpo_point_seed101/` | adapter sau 500 bước, **bfloat16**, 504 tensor, r=8 alpha=16 |
| `adapter_ref_min/` | bản sao adapter MIN-DESC/101 mà TRL đóng băng làm tham chiếu KL, **float32** |
| `preds_grpo_point_seed101.jsonl` | câu sinh trên **4.463 bước chạm** (Kaggle T4, 3,1 h), chữ ký `lora:grpo-point-adapter` |
| `c1_infer.log` | log lượt suy luận C1 |
| `only_nontap2495.jsonl` | danh sách `--only` cho lượt **bước KHÔNG chạm** theo (x20b) |
| `score_grpo_point_seed101{_raw,}.jsonl/.json` | *(chưa có)* kết quả chấm `exec` của C2 |
| `preds_grpo_point_seed101_nontap.jsonl` | *(chưa có)* câu sinh trên 2.495 bước không chạm, lượt C3 |

⛔ Hai thư mục adapter **không vào git** (`.gitignore`); trọng số gốc ở Drive
`MyDrive/thesis/ckpt/grpo_point_seed101/`.
⛔ `adapter_ref_min/` là MIN, **không** phải kết quả lượt này. Đừng upload nó lên Kaggle —
chấm nhầm nó thì ra lại 60,05 mà không có lỗi nào báo.

Đọc bằng:

```
~/.venvs/thesis/bin/python harness/doc_grpo_local.py \
  --grpo runs/grpo_point/adapter_grpo_point_seed101 \
  --min  runs/grpo_point/adapter_ref_min \
  --log  runs/grpo_point/logs/log_history.json
```

⚠️ Hai adapter khác dtype nên `‖Δ‖` thô lẫn sai số cast (~1,65e-03). Chỉ đọc dòng
**dịch chuyển THẬT**, đo sau khi ép bản đối chiếu về cùng lưới số.

---

## Đọc kết quả

`exec` (sau khi C2 về, đặt tệp thô vào chính thư mục này):

```
~/.venvs/thesis/bin/python harness/doc_exec_grpo.py
```

In exec hai nhánh kèm KTC bootstrap **cụm**, McNemar ghép cặp với MIN (mốc **60,05**), verdict
theo (x19e) với MDE **2,2**, câu trả lời cho (x20a)/(x20c), thước phụ, bảng D.3, và phân rã theo
nhóm câu đã đổi. ⚠️ Dự báo ghi trước ở (x19d) ghi 5 là **+1,10 pp** (dải +0,59 … +1,49).

Bước không chạm (lượt C3, **0 GPU**):

```
python3 harness/score_run.py --mode noharm \
    --preds runs/grpo_point/preds_grpo_point_seed101_nontap.jsonl \
    --baseline runs/preds_min_desc_seed101.jsonl \
    --out runs/grpo_point/noharm_grpo_point_seed101.json
```

Ngưỡng (x20b): không thấp hơn MIN quá **3 pp** ở tỉ lệ khớp loại thao tác.

Đọc lượt train (log + dịch chuyển trọng số): `harness/doc_grpo_local.py`, xem đầu file này.
