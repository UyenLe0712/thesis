# Bàn giao — TAGE trên tập test, Kaggle commit (3–4/10/2026)

Đọc kèm: `report/267` (số val + thiết kế) · runbook `harness/runbook/kaggle_tage_test.md` (Ô 1–5).
Số val cấm trích vào luận văn. TAGE **chưa có số test** tại thời điểm viết.

## 1. Đã làm 3–4/10

| việc | trạng thái |
|---|---|
| Runbook Kaggle commit + gói `_bundles/tage-test-script/` (6 tệp) | xong, commit `742f321` |
| Adapter `ed_gold`, `loc_g`, `ed_none` nén từ Drive thành `tage-adapters.zip` (ZIP_STORED, arcname `{v}/{tệp}`, 6 tệp) → dataset Kaggle `tage-adapters` | xong (user làm) |
| Chạy thử tương tác trên Kaggle, `TEST = True` (`--n 4` mỗi shard ⇒ 8 bước) | **đạt toàn chuỗi**, xem §2 |
| Lỗi `AssertionError` ở `tage_val.py:739`: phép kiểm tham số của `--locate-val`/`--edit-val` đòi `--c1`, chế độ `--rows` không có | **đã sửa** `(a.c1 or a.rows)` ở cả hai chế độ, commit `6155433`; md5 mới `2a6aa15eabf4d53bfca67ae9abb580ee` (đã cập nhật ở bảng runbook và dict `MD` của Ô 2) |
| Commit 1 (nhánh pred, `TEST = False`) | **xong 4/10**, tệp ở `runs/tage_test/`, kết quả `report/269` |

## 2. Kết quả lượt thử (8 bước, chỉ để kiểm đường ống, không đọc thành số)

- Ô 2: dò đúng 4 dataset, md5 khớp, mỗi adapter đúng 1 bản.
- Ô 3: hoà S1 fp16 xong. Cảnh báo torchao / HF_TOKEN / FutureWarning `min_pixels` vô hại.
- Ô 4: shard 2232/2231 · định vị 8/8, 0 bước không đọc được toạ độ · sửa câu 8/8, 0 câu tiếng Việt.
- Ô 5 với τ thật 0,73767: nhận sửa 0/8 ⇒ khâu chấm bị bỏ qua, nên chạy thêm τ = −99 để ép khâu chấm:
  nhận 6/8, `score_run --mode score --grounder uground --n 99999` chấm đủ 6 bước, exec 5, không lỗi,
  `XONG · 0.18 h`. ⇒ khâu chấm tập con (lọc `taps` theo preds, `score_run.py:565`) chạy đúng.

## 3. Trước khi bấm commit (5 việc)

1. Ô 5: đổi lại **`TAU = 0.73767`** (lượt thử để −99).
2. Ô 3: **`TEST = False`**.
3. Dataset `tage-test-script` → New Version, thay `tage_val.py` bằng bản trong `_bundles/tage-test-script/`.
4. Xoá ô vá `str.replace` đã thêm trong phiên thử; Ô 2 phải báo md5 `2a6aa15e…`.
5. GPU T4 ×2 → Save Version → **Save & Run All (Commit)**.

## 4. Theo dõi commit

Tab Logs của version, nhịp sống mỗi 2 phút. Không có dòng nhịp sống sau 4 phút ⇒ huỷ. Mốc an tâm: dòng
`20/2232 · X s/bước` xuất hiện ở **cả hai shard** (~0,15–0,25 h) và không có Traceback. Lấy X để ước tổng
thời gian (ước trước: 6–9 h; Ô 4 tự dừng sinh ở mốc 10,5 h, phần dở nối tiếp ở commit sau bằng cách gắn output
commit này làm Input).

## 5. Sau khi commit xong (0 GPU, WSL)

1. Tải `tage_test_out.zip` (runbook Ô 6 hoặc notebook CPU nếu commit thiếu Ô 6), `unzip -d runs/tage_test/`.
2. Gộp: bước cổng nhận sửa lấy từ raw mới; bước còn lại lấy từ `runs/grpo_spice/score_ck500_test_raw.jsonl`.
3. So S1/101 (và ck500) trên 4.463 bước, đủ các cột như `report/261` (exec, D.3, AitW, ±14%, văn bản), KTC bằng
   `score_run.cluster_bootstrap`.
4. Cập nhật `report/267` §6 và dòng TAGE trong `CLAUDE.md`.
5. Commit 2 (nhánh `none`, `τ_none = −0,04327`) là tuỳ chọn, hỏi user trước.
