# Probe "người nghe Phi-4 từ S1" trên Kaggle T4×2 (report/330 §7 hàng 7)

Lượt: GRPO thưởng SPICE + 1·h (nhánh `nghe`, tên luận văn SPICE + LR, λ = 1), **LoRA mới từ S1** (không `--tu`), hạt 101,
bs 4×4, G = 8, `--gen-chunk 8`, fp16, đúng 1.000 câu nhắc ck500. Policy ở GPU0, máy chủ Phi-4 ở GPU1.
Probe chạy **20 bước bằng `--train --max-steps 20`**, không dùng `--probe`: `--probe` lấy 50 câu nhắc dài nhất, mà chỉ
5/50 câu nằm trong bảng người nghe, nên gần như không gọi Phi-4. Ở 20 bước đầu của `--train` thì 29/40 câu nhắc nằm trong bảng.

## Tệp

| tệp | việc |
|---|---|
| `build_ds.py` | chép 8 tệp **nguyên văn** từ `_scripts/288/nghe/` (kiểm md5 bản 288) vào `ds_<tk>/`, kèm `dataset-metadata.json` |
| `make_nb.py` | sinh `k_<kernel>/` (ipynb + kernel-metadata.json, GPU, Internet) |
| `ds_trangphuongngoc/` | gói dataset `nghe-s1-kit` đã dựng |
| `k_nghe-s1-probe/` | notebook đã dựng, trần 2,0 h, 20 bước |

Không sửa dòng mã nào của 288. Hai môi trường: train dùng stack của lưới (trl 0.29.1 · transformers 5.20.2 · peft 0.21.2);
Phi-4 chạy trong venv `/tmp/vphi` (transformers 4.48.2 · peft 0.13.2 · accelerate 1.3.0, dùng chung torch của image), giống ô C3 của 288.

## Lệnh (chạy từ `_bundles/nghe_s1`)

```bash
kg ca quota                                                     # trang2 phải còn ≥ 2,5 h
python3 -I build_ds.py trangphuongngoc                          # đã chạy 7/11
kg trang2 datasets create -p ds_trangphuongngoc  # lần đầu (sửa tệp thì: datasets version -p ... -m "...")
python3 -I make_nb.py trangphuongngoc nghe-s1-probe             # đã chạy 7/11; đổi trần: TRAN_H=2.5 python3 -I make_nb.py ...
kg trang2 kernels push -p k_nghe-s1-probe --accelerator NvidiaTeslaT4
```

Notebook gắn ba dataset: `fgrb-p1-bundle` (ảnh + adapter S1), `grpo-luoi-script` (jar SPICE), `nghe-s1-kit`. Muốn dùng tài khoản khác thì
chạy hai script với tên tài khoản đó, và tài khoản ấy phải có sẵn hai dataset đầu.
⚠️ 7/11 `trang2` đang chạy `luoi-t2-4` (11 h). Đẩy thêm thì Kaggle có thể xếp hàng, và hạn mức tuần bị chia.

## Đọc kết quả

`kg trang2 kernels output trangphuongngoc/nghe-s1-probe -p ../../runs/nghe_s1/probe` rồi `unzip nghe_s1_probe.zip`.
Mở `nghe_s1_probe/tong_ket.json` và các log trong cùng thư mục:

- `s_buoc_tv` / `s_buoc_tb`: giây mỗi bước, bỏ hai bước đầu. Cột `uoc_500_buoc_h` = 500 × s/bước, còn `uoc_commit_11h` là số commit cần chạy.
- `dinh_VRAM_MiB` là đỉnh `memory.used` của GPU0 và GPU1, lấy mẫu 10 s một lần. Xem thêm dòng `[xong] … đỉnh VRAM` (policy, `max_memory_allocated`)
  và `do_nguoi_nghe.json` (s/câu trên 40 màn, s/câu trên 20 màn nhiều ô nhất, số `None`, tức OOM hoặc không ra số).
- Kiểm `[nghe]` trong `train_nghe_101.log`: số lần, số câu hỏi, số câu trúng, số lỗi máy chủ. Phải có câu hỏi và có câu trúng, lỗi máy chủ phải là 0.
- `[nhánh] nghe · … · LoRA mới` · `[LoRA mới] tham số học N · S1 có N` · `cau_nhac_trung_ck500: true`.
- Không có `Traceback`/`OutOfMemory` trong `train_nghe_101.log` lẫn `nghe_server.log`. RAM trong nhịp sống phải dưới ~29 GB.
- `ma_thoat` = 0. Nếu là −15 thì lượt đã chạm trần giờ, nhưng s/bước vẫn đọc được từ các bước đã chạy.

## Quy tắc quyết Kaggle hay Colab (đề xuất, user quyết)

Chọn **Kaggle** khi đủ cả bốn điều: không OOM ở hai GPU, 0 lỗi máy chủ, RAM không chạm trần, và `uoc_500_buoc_h` ≤ ~40 h
(tức ≤ 4 commit 11 h nối tiếp bằng `--resume auto`, khoảng 1,3 tuần hạn mức của một tài khoản).
Chọn **Colab** (report/330 §8 mục 1) khi có OOM hoặc lỗi máy chủ không gỡ được, hoặc khi ước tính vượt ~40 h. Nếu vượt ngưỡng
chỉ vì người nghe chậm, có thể so trước `s/bước` với lượt GRPO + SPICE của lưới (~150 s/bước T4 [đo, smoke t2 6/11]).
Lượt đủ chưa có notebook: cần thêm phần chép điểm lưu và `nghe_log.jsonl` từ kernel trước, giống `make_nb.py` của lưới.
