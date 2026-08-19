# `runs/` — điểm số đã chấm

Mỗi lượt để lại hai tệp. **Giữ cả hai**, và commit vào git — đây là số đi thẳng vào luận
văn nên cần lịch sử phiên bản để truy được số nào đo lúc nào bằng mã nào.

| tệp | vai |
|---|---|
| `score_<nhánh>_seed<n>.json` | số tổng hợp |
| `score_<nhánh>_seed<n>_raw.jsonl` | **một dòng mỗi bước** — đổi luật chấm hay thêm lát cắt thì chấm lại từ đây, **không gọi lại bộ trỏ** (tiết kiệm 5,6 giờ mỗi lần) |
| `preds_<nhánh>_seed<n>.jsonl` | câu do mô hình sinh, đầu vào của khâu chấm |

Trường trong tệp thô: `episode_id · step_id · app · app_seen_in_train · pred_xy · gold_xy ·
wh · n_buttons · sent · gold_instruction · action_ok · toggle_ok · hit_disk · hit_voronoi ·
executable`. Bước bị bỏ mang khoá `bo_qua` thay vì các trường chấm.

## Đã có

### `s1` hạt giống 101 — 14/8/2026, Kaggle T4, 5,6 giờ, 0 đồng

| | |
|---|---|
| **Executability (ô Voronoi, headline)** | **59,1%** KTC95 **[57,3 – 60,8]** |
| đĩa dung sai (báo kèm) | 69,2% [67,6 – 70,7] |
| n | **4.462** (tệp có 4.463; 1 bỏ vì câu rỗng — ep 18710/step 1) |
| cụm 1.091 · hiệu dụng | **454,3** |

**Đọc trên nền trần 70,0% [64,5–75,3], không phải trên nền 100.**

Lát cắt và phân tích đầy đủ: **`report/110` mục 4j-12**. Tóm tắt:

- **Không có lợi thế sân nhà:** app đã-thấy 59,1% (n=1.737) · chưa-thấy 59,0% (n=78) ·
  không-gán-được 59,2% (n=2.647).
- **Chỗ hỏng ở cách gọi tên phần tử:** đúng loại thao tác 94,4%; trong 1.824 bước trượt chỉ
  251 do sai thao tác, 1.573 (86%) là thao tác đúng mà bộ trỏ không tìm ra nút.
- **Thiên vị câu dài 5,4 pp:** câu >33 ký tự 61,9% (n=2.169) · ≤33 ký tự 56,5% (n=2.293).
- ⚠️ **Room thật ~485 bước (10,9 pp), không phải 1.573** — trần 70% nghĩa là câu người viết
  cũng trượt ~1.339/4.462.

## Cách tái tạo

Gói dữ liệu chấm dựng bằng `python harness/make_bundle.py score` (1,7 GB: mã + `test.jsonl`
đã gắn nhãn + `ocr` + `descriptors` + 4.463 ảnh bước chạm), tải lên Kaggle làm dataset dùng
lại cho mọi lượt. Lệnh chấm:

```bash
python harness/score_run.py --mode score --grounder uground \
    --preds <preds>.jsonl --out <score>.json
```

⚠️ `test.jsonl` phải là **bản đã gắn nhãn `app_seen_in_train`** (`score_run.py:405` đọc nhãn
thẳng từ đó). Bản đúng: 6.958 dòng, nhãn 2.991 / 139 / 3.828.
