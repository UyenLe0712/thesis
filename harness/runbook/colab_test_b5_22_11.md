# Colab: sinh câu test + chấm exec cho 5 lượt B5 đã xong ck500 (dựng 22/11/2026, CHƯA chạy)

Lượt: GRPO + chrF · GRPO + BLEU-4 · GRPO + SPIDEr · GRPO + BERTScore · DPO trực tuyến (đều từ S1/101, ck500).
Notebook: `_bundles/luoi/k_luoi-test-c-b5/luoi-test-c-b5_colab.ipynb` (sinh bởi `make_test_nb2.py` + `_bundles/colab_tu_kaggle.py`;
bản chạy bằng Colab CLI: `luoi-test-c-b5_colab_cli.py`). Cùng mã với các lượt test Kaggle (Dr.GRPO `luoi-test-u-5`), trần giờ 22 h.

## 0. Trước khi mở Colab (máy nhà, một lần)

Upload dataset adapter (289 MB, giữ thư mục con):

```
cd _bundles/luoi && kg uyenle datasets create -p ck_b5_22_11 --dir-mode zip
kg uyenle datasets status uyenle0712/b5-ck-22-11      # chờ "ready"
```

md5 adapter (notebook tự kiểm, lệch là dừng) ở `ck_b5_22_11/spec.txt`. Không thấy theo tên thư mục thì notebook tìm theo md5.

## 1. Colab

- Colab secret `KAGGLE_UYENLE0712` = khoá KGAT_ của tài khoản uyenle0712, bật *Notebook access*.
- GPU: notebook tự đọc VRAM. **A100 (40 GB) chạy hai lượt cùng lúc**, L4/T4 chạy lần lượt.
  Chưa đo tốc độ sinh trên Colab. Mốc đã đo: Kaggle T4 2,78 s/bước ⇒ một lượt ~3,4 h sinh + chấm ⇒ 5 lượt lần lượt ~18–20 h.
  Theo thủ tục chọn máy: chạy ~10 phút trên L4, đọc s/bước ở dòng log `gen_*.log`, rồi mới quyết có lên A100 hay không.
- Run all. Kết quả đồng bộ lên Drive mỗi 5 phút: `MyDrive/thesis/colab_kaggle/luoi-test-c-b5/`.
- Mất máy: mở lại, Run all — ô khôi phục chép Drive về `/kaggle/working`, câu đã sinh được nối tiếp.
- Không bấm Stop ô đang chạy (Popen đã có `start_new_session=True`, nhưng vẫn hạn chế).

## 2. Kiểm trong log

- `[kiểm hoà] x/20` ≥ 16 và `[kiem bo cham] ≥ 9/10` (chạy trên GPU khác T4 có thể lệch; dưới ngưỡng thì notebook dừng).
- Mỗi lượt có dòng `[điểm lưu] …/<lượt>` đúng adapter, `4463 câu`, và `===== KET QUA` có `exec` cho cả 5.

## 3. Sau khi xong

- Tải `MyDrive/thesis/colab_kaggle/luoi-test-c-b5/` về `runs/luoi/20_11/luoi-test-c-b5/`.
- Đọc ghép cặp như Dr.GRPO (report/320 §30): so ck500, A/A, SFT tiếp, S1.
- Độ đo văn bản: kernel CPU kiểu `_bundles/chu_drgrpo_22_11/` (thay nhánh mới, cache S1/ck500/SFT tiếp/A/A có ở `runs/luoi/20_11/chu_drgrpo/chu_cache.zip`).
- Ghi report/320, `harness/bang_tong_hop.py` (report/334), `HUONG_DA_THU.md`, report/337, memory.
- ⚠️ Nếu kiểm hoà lệch do GPU khác T4 thì ghi rõ trong báo cáo.
