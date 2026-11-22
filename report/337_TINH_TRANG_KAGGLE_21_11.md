# Tình trạng Kaggle đợt B5 + trục thưởng — cập nhật 21/11/2026 07:00 VN

Đọc file này trước khi đẩy kernel mới hoặc nối tiếp. Runbook lệnh: `_bundles/luoi/CHAY_B5.md`.
Thiết kế: `slides/ACTION_4_THUAT_TOAN_RL_2025_SO_VOI_GRPO_20_11_2026.md` mục 12. Danh sách việc: `report/336`.
Mọi lượt: seed 101, xuất phát S1 hoà + LoRA mới, 1.000 câu nhắc ck500, G 8, lr 1e-5, β 0,04.
⚠️ Mọi mã/kernel ở đây **chưa commit git** (`harness/grpo_moi_b5.py`, `harness/grpo_dapo_ds.py`, `_bundles/luoi/k_luoi-*`, `make_nb.py`, `make_kit.py`).

## 1. Kernel theo tài khoản

| tài khoản (`kg …`) | kernel | GPU0 · GPU1 | trạng thái 21/11 06:47 | dự kiến dừng |
|---|---|---|---|---|
| uyenle (`uyenle0712`) | `luoi-rw-u-1` | GRPO + chrF · GRPO + BLEU-4 | ✅ COMPLETE | — |
| trang (`trangphngngc`) | `luoi-rw-t-1` | GRPO + SPIDEr · GRPO + BERTScore | ✅ COMPLETE | — |
| trang | `luoi-b5-t-1` | 6a Dr.GRPO đầy đủ · 6b DAPO lấy mẫu động (eps 0,28) | ▶️ RUNNING | ~08:50 |
| trang2 (`trangphuongngoc`) | `luoi-b5-t2-1` | 3 GRPO μ=2 (`mu2g`) · 4 GSPO (`s1000g`), 1.000 bước | ▶️ RUNNING | ~08:50 |
| trang2 | `luoi-dpoon-t2-1` | DPO trực tuyến | ▶️ RUNNING | ~09:15 |

Đã chết / huỷ (không có điểm lưu, đừng chạy lại nguyên trạng):
- `luoi-b5-pb-t2` (probe DAPO): user bảo huỷ, đã `kernels delete`.
- `luoi-b5-pb-u`, `luoi-b5-u-1`, `luoi-b5p8-t-1`, `luoi-b5g-u-1`, `luoi-b5r-t-1` (lô lớn grpo_lon / rpp): **chết RAM (-9)** 6–8 phút sau khi bắt đầu, kể cả khi chạy một tiến trình. Xem mục 3.

## 2. Kết quả hai kernel đã xong (log ở `runs/luoi/20_11/<kernel>/`)

| lượt | điểm lưu cuối | thưởng TB 25 bước đầu → cuối | KL TB / max |
|---|---|---|---|
| GRPO + chrF (`grpo_chrf_101`) | ck175 | 0,591 → 0,625 | 0,012 / 0,098 |
| GRPO + BLEU-4 (`grpo_bleu4_101`) | ck200 | 0,474 → 0,571 | 0,010 / 0,147 |
| GRPO + SPIDEr (`grpo_spider_101`) | ck125 | 0,464 → 0,453 (phẳng) | 0,001 / 0,006 |
| GRPO + BERTScore (`grpo_bertscore_101`) | ck125 | 0,646 → 0,659 | 0,002 / 0,014 |

Dừng do trần giờ, không lỗi. Chưa lượt nào tới 500 bước ⇒ phải nối tiếp. SPIDEr chậm nhất (~125 bước / 5,8 h).

## 3. Lỗi RAM của lô lớn (B5: grpo_lon, rpp) — chưa sửa

TRL tiền xử lý cả lô sinh 128 ảnh một lần. Đo máy nhà (Qwen2VLImageProcessorPil, ảnh 1080×2400):
16 ảnh 1,52 GB · 64 ảnh 4,83 GB / 108 s · 128 ảnh 9,83 GB / 342 s.
Hướng sửa (chưa làm, **user chưa đồng ý**): sinh theo lô nhỏ rồi gộp nhiều lô vào một bước tối ưu; rpp cần std trên cả lô 128 nên phải tự giữ đệm thưởng. Hoặc giảm RAM bước tiền xử lý.

## 4. Việc kế

1. **Sau 07:00 21/11 (hạn mức đã làm mới):** đẩy nối tiếp
   - uyenle: `luoi-rw-u-2` (chrF + BLEU-4) trỏ `uyenle0712/luoi-rw-u-1`;
   - trang: `luoi-rw-t-2` (SPIDEr + BERTScore) trỏ `trangphngngc/luoi-rw-t-1` — trang chỉ còn 1 suất vì `luoi-b5-t-1` đang chạy.
   - uyenle còn 1 suất trống: chưa có việc (B5 lô lớn chờ sửa mã).
2. Khi `luoi-b5-t-1`, `luoi-b5-t2-1`, `luoi-dpoon-t2-1` dừng: tải log về `runs/luoi/20_11/<kernel>`, kiểm tốc độ, thưởng, KL; DAPO: số lần bù > 0, tỉ lệ nhóm hoà trong (0; 1). Rồi nối tiếp `…-2` theo CHAY_B5.md.
3. Mọi lượt nối tiếp: log **phải** có `[tiếp từ] …/checkpoint-N` và `[nạp default] … |lora_B| 0.0000 → x>0`. Thiếu là quay về S1: dừng.
4. Xong train: chấm test, thêm số vào `harness/bang_tong_hop.py` (report/334), cập nhật `report/HUONG_DA_THU.md` và `report/320`.

## 5. Luật vận hành nhắc lại

- Tối đa 2 phiên GPU/tài khoản; notebook T4×2 chạy 2 lượt (mỗi GPU một lượt); hạn mức tính theo giờ phiên; làm mới 00:00 UTC = 07:00 VN.
- Không có lệnh huỷ kernel (chỉ `kernels delete -y`, mất log). `kernels logs` rỗng khi đang chạy; log/output chỉ lấy được sau khi dừng.
- Đọc giờ bằng `TZ='Asia/Ho_Chi_Minh' date`. Không in khoá Kaggle.

## 6. Cập nhật 21/11 ~07:15 VN

- Sửa `harness/grpo_moi_b5.py` (md5 nay `bb57daf6…`): ép `dataloader_num_workers=0` qua `CD.OVERRIDE` cho grpo_lon/rpp. Selftest công thức đạt. Kit uyenle đã đẩy version mới (kit trang/trang2 CHƯA dựng lại).
- Đẩy `uyenle0712/luoi-b5rp8-u-1`: **REINFORCE++ lô 64** (`rpp:spice:101:b5p=8,tag=p8`, 125 bước, một lượt/notebook, CAT_H 10,8). Đánh đổi: std tính trên 64 câu, phải khai. Đối chứng `grpo_lon:spice:101:b5p=8,tag=p8` chưa đẩy (chờ suất trống sau ~08:50).
- Đẩy nối tiếp `uyenle0712/luoi-rw-u-2` (chrF + BLEU-4, trỏ rw-u-1) và `trangphngngc/luoi-rw-t-2` (SPIDEr + BERTScore, trỏ rw-t-1), CAT_H 10,8. Khi xong kiểm `[nạp default] … → x>0`.
- Đang chạy đủ 6 phiên: uyenle (b5rp8-u-1, rw-u-2) · trang (b5-t-1, rw-t-2) · trang2 (b5-t2-1, dpoon-t2-1).

## 7. Cập nhật 21/11 ~10:00 VN — kết quả phiên 1 của bốn thuật toán + DPO trực tuyến

Log ở `runs/luoi/20_11/<kernel>/`. Thưởng = TB 25 bước đầu → 25 bước cuối (SPICE).

| lượt | kernel | điểm lưu cuối | thưởng | KL TB / max | ghi chú |
|---|---|---|---|---|---|
| Dr.GRPO đầy đủ | b5-t-1 | ck250/500 | 0,467 → 0,512 | 0,005 / 0,043 | |
| DAPO lấy mẫu động | b5-t-1 | ck200/500 | 0,465 → 0,521 | 0,004 / 0,028 | nhóm hoà bị loại 118/568 = 20,8% (trong dải 0,15–0,35), lấy bù 84 lần ⇒ bộ lọc chạy đúng |
| GRPO μ=2 | b5-t2-1 | ck300/1.000 | 0,500 → 0,511 | 0,010 / 0,072 | clip 0 (bình thường với μ=2) |
| GSPO | b5-t2-1 | ck275/1.000 | 0,496 → 0,465 | 0,005 / 0,033 | clip_ratio vùng 0,19 → 0,36 (> 0, khoảng cắt hẹp hoạt động); thưởng chưa tăng |
| DPO trực tuyến | dpoon-t2-1 | ck225/500 | 0,486 → 0,504 | — | margin 0,006 → 0,116; ~170 s/bước |
| REINFORCE++ lô 64 | b5rp8-u-1 | ck6/125 | (6 bước) | — | **qua lỗi RAM** nhưng **OOM GPU** ở bước 7 (prefill khúc 8 chuỗi, 14,2/14,56 GiB); ~13 phút/bước ⇒ 125 bước ≈ 27 h |

grad_norm NaN lẻ tẻ (0–3 bước/lượt), thưởng không bị ảnh hưởng.

Đẩy tiếp ~09:50–10:00 (GIU_CK 3, CAT_H 10,8): `trangphngngc/luoi-b5-t-2` · `trangphuongngoc/luoi-b5-t2-2` · `trangphuongngoc/luoi-dpoon-t2-2` · `uyenle0712/luoi-b5rp8-u-2` (REINFORCE++ nối tiếp từ ck6, sau khi sửa `grpo_moi_b5.py` ép `--gen-chunk 4`, md5 `2d5e4ce2…`, kit uyenle đã đẩy lại). Khi xong kiểm `[tiếp từ]` + `[nạp default] … → x>0`.
Đang chạy đủ 6 phiên: uyenle (rw-u-2, b5rp8-u-2) · trang (rw-t-2, b5-t-2) · trang2 (b5-t2-2, dpoon-t2-2). Đối chứng GRPO lô lớn 64 (`grpo_lon:spice:101:b5p=8,tag=p8`) chưa có suất.

## 8. Cập nhật 21/11 ~21:30 VN — phiên 2 xong, đẩy phiên 3

Sáu kernel phiên 2 COMPLETE lúc ~18:00 (rw) và ~20:59 (còn lại). Mọi lượt có `[tiếp từ]` + `|lora_B| 0 → x>0`.

| lượt | điểm lưu cuối | còn |
|---|---|---|
| Dr.GRPO đầy đủ | **ck500/500 — xong train** | chấm test |
| DPO trực tuyến | ck450/500 | 50 bước |
| GRPO + BLEU-4 · + chrF | ck475 · ck450 /500 | 25 · 50 bước |
| GRPO + SPIDEr · + BERTScore | ck350 · ck375 /500 | 150 · 125 bước |
| DAPO lấy mẫu động | ck400/500 | 100 bước |
| GRPO μ=2 · GSPO | ck625 · ck600 /1.000 | ~400 bước |
| REINFORCE++ lô 64 | ck70/125 | 55 bước (~13 phút/bước) |

Hạn mức tới 28/11 (đo 21:10): uyenle 7,04 h · trang 8,33 h · trang2 8,35 h ⇒ không đủ cho mọi lượt + test (~50–60 h).
Ưu tiên tuần này: chạy nốt lượt ngắn rồi sinh câu test. Đẩy 21:30 (GIU_CK 3):
- `uyenle0712/luoi-rw-u-3` (chrF + BLEU-4, trỏ rw-u-2, CAT_H 3,5) → sau đó test hai lượt này trên uyenle (`make_test_nb2.py`, nối tiếp tuần sau nếu thiếu giờ).
- `trangphngngc/luoi-rw-t-3` (SPIDEr + BERTScore, trỏ rw-t-2, CAT_H 7,5).
- `trangphuongngoc/luoi-dpoon-t2-3` (DPO trực tuyến, trỏ dpoon-t2-2, CAT_H 3,5) → sau đó test DPO + Dr.GRPO trên trang2 (adapter Dr.GRPO ck500 phải upload thành dataset của trang2, notebook test tìm theo md5).
- Tuần 28/11: DAPO (trang), μ=2 + GSPO (trang2), REINFORCE++ (uyenle), test các lượt còn lại, rồi độ đo văn bản (kernel CPU).

Log + điểm lưu cuối ở `runs/luoi/20_11/<kernel>/`; thư mục phiên 1 đã xoá điểm lưu, giữ log + `trainer_state_last.json`.
⚠️ 21/11 lỡ xoá điểm lưu cuối của rw-t-2 ở máy nhà (lỗi sắp xếp đường dẫn có dấu `-`), đã tải lại từ output Kaggle. Script dọn đúng: `scratchpad/don.py` (đối chiếu `global_step`).

### 8b. Thưởng và KL sau phiên 2 (từ `trainer_state.json` điểm lưu cuối, gồm cả lịch sử phiên 1)

Thưởng = TB 25 bước đầu → 25 bước cuối (theo thước thưởng của từng lượt, không so được giữa các thước). KL = TB / max.

| lượt | điểm lưu | thưởng | KL TB / max |
|---|---|---|---|
| Dr.GRPO đầy đủ | ck500 | 0,467 → 0,520 | 0,014 / 0,095 |
| DAPO lấy mẫu động | ck400 | 0,465 → 0,486 | 0,021 / 0,211 |
| GRPO μ=2 | ck625 | 0,500 → 0,500 | 0,030 / **0,592** |
| GSPO | ck600 | 0,496 → 0,455 (giảm) | 0,010 / 0,083 |
| REINFORCE++ lô 64 | ck70 | 0,470 → 0,472 | 0,001 / 0,006 |
| DPO trực tuyến | ck450 | 0,486 → 0,511 | — (log không có KL) |
| GRPO + chrF | ck450 | 0,591 → 0,656 | 0,044 / **0,923** |
| GRPO + BLEU-4 | ck475 | 0,474 → 0,618 | 0,032 / 0,311 |
| GRPO + SPIDEr | ck350 | 0,464 → 0,500 | 0,018 / 0,158 |
| GRPO + BERTScore | ck375 | 0,646 → 0,685 | 0,021 / 0,236 |

⚠️ KL max của chrF (0,923) và μ=2 (0,592) cao hơn hẳn các lượt cũ (0,002–0,05); trước đây GRPO + chrF từ SFT-cont cũng trượt tiêu chí không chạm vì KL > 0,10 (report/333). Khi có số test, đọc kèm bước không chạm. GSPO thưởng giảm sau 600 bước. Chưa có số test nào.

## 9. Cập nhật 22/11 ~08:00 VN — phiên 3 xong

- `luoi-rw-u-3`, `luoi-rw-t-3`, `luoi-dpoon-t2-3` COMPLETE. Cả 5 lượt tới **ck500/500** (có `[tiếp từ]` đúng điểm lưu trước + `|lora_B| 0 → x>0`). Đã tải về `runs/luoi/20_11/<kernel>/`, chỉ giữ checkpoint-500.
- ⛔ `luoi-test-u-5` (bản 1) **ERROR sau 1 phút**: dataset `b5-ck-21-11` upload phẳng (mất thư mục con `drgrpo_full_spice_101/`), notebook tìm theo tên thư mục nên không thấy adapter. Tốn ~1 phút GPU. Đã vá `make_test_nb2.py`: không thấy theo tên thì tìm theo md5 trên mọi `adapter_model.safetensors`. Đẩy lại bản 2 lúc 07:55, CAT_H 4,4 (uyenle còn 4,99 h) ⇒ nhiều khả năng chưa đủ 4.463 bước, nối tiếp sau 28/11 bằng `PREV=uyenle0712/luoi-test-u-5`.
- 07:57 đẩy `trangphuongngoc/luoi-b5-t2-3` (μ=2 + GSPO, trỏ b5-t2-2, GIU_CK 3, CAT_H 5,4; notebook chỉ khác b5-t2-2 ở CAT_H). Nhịp phiên 2 ~30 bước/h ⇒ dự kiến tới ~ck775/750.
- trang còn 1,8 h: không đẩy DAPO (nhịp ~18 bước/h, lưu mỗi 25 bước ⇒ dễ không kịp lưu điểm nào).

| lượt | điểm lưu | thưởng (TB 25 đầu → 25 cuối) | KL TB / max |
|---|---|---|---|
| GRPO + chrF | ck500 | 0,591 → 0,708 | 0,048 / **0,923** |
| GRPO + BLEU-4 | ck500 | 0,474 → 0,578 | 0,033 / 0,311 |
| GRPO + SPIDEr | ck500 | 0,464 → 0,547 | 0,029 / 0,353 |
| GRPO + BERTScore | ck500 | 0,646 → 0,716 | 0,032 / **0,496** |
| DPO trực tuyến | ck500 | 0,486 → 0,510 | — |

Chờ test (6 lượt xong train: Dr.GRPO, DPO trực tuyến, chrF, BLEU-4, SPIDEr, BERTScore). Hạn mức không đủ tuần này; test các lượt này sau 28/11 (adapter phải upload thành dataset, nhớ `--dir-mode zip` hoặc dựa vào tìm theo md5).
