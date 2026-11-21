# Lưới RL đợt B5 (20/11/2026): bốn phương pháp hậu-GRPO + đối chứng khớp

Nguồn thiết kế: `slides/ACTION_4_THUAT_TOAN_RL_2025_SO_VOI_GRPO_20_11_2026.md` mục 12 (bảng 12.3, yêu cầu 12.4). Chạy từ `_bundles/luoi`.
Mọi lượt seed 101, xuất phát S1 hoà + LoRA mới, 1.000 câu nhắc ck500, G 8, lr 1e-5, β 0,04, thưởng SPICE. Kết quả chỉ được gọi là "thăm dò ở seed 101".

## Lượt và ghép kernel

| # (12.3) | lượt (`make_nb.py`) | tệp chạy | bước | ước lượng T4 |
|---|---|---|---|---|
| 1 | `grpo_lon:spice:101` | `grpo_moi_b5.py` | 62 × 128 câu | ~20 min/bước ⇒ ~21 h [suy, theo docstring module] |
| 2 | `rpp:spice:101` | `grpo_moi_b5.py` | 62 × 128 câu | ~21 h [suy] |
| 3 | `grpo:spice:101:loss=grpo,mu=2,steps=1000,tag=mu2g` | `grpo_codien.py` | 1.000 | ~130 s/bước ⇒ ~36 h [đo smoke μ=2 6/11] |
| 4 | `gspo:spice:101:loss=grpo,steps=1000,tag=s1000g` | `grpo_moi_b1.py` | 1.000 | ~36 h [suy] |
| 5 | GRPO A/A μ=1 | **dùng lại** `grpo_spice_101` của `luoi-t2-3/4/11` (xem cuối file) | 500 | 0 h |
| 6a | `drgrpo_full:spice:101` | `grpo_moi_b1.py` | 500 | ~150 s/bước ⇒ ~21 h |
| 6b | `dapo_ds:spice:101:eps=0.28,tag=dapo` | `grpo_dapo_ds.py` | 500 nhóm-update | ~21 h × 1/(1 − tỉ lệ nhóm hoà) ≈ 25–32 h [suy] |

| kernel | GPU0 · GPU1 | số commit 11 h | giờ hạn mức |
|---|---|---|---|
| `luoi-b5-u-*` | 1 · 2 | 2 | ~22 |
| `luoi-b5-t-*` | 3 · 4 | 4 | ~44 |
| `luoi-b5-t2-*` | 6a · 6b | 3 (commit 3 chỉ còn 6b) | ~33 |
| probe ×3 | xem dưới | 1 × 2 h mỗi cái | ~6 |
| **tổng** | | | **~105 h** (≈ 1,2 tuần trên ba tài khoản) |

Kaggle tính giờ theo phiên, không theo số GPU. Nếu phải chạy lại A/A thì ghép vào GPU0 của commit 3 của `luoi-b5-t2-*` (lúc đó 6a đã xong), thêm ~1 commit: `grpo:spice:101:tag=aa2` (chạy thẳng `grpo_luoi.py`, đúng như A/A cũ).

## Bước 0 — chỉ làm khi cả hai module đã có

- `harness/grpo_moi_b5.py` (có, 20/11, không import `grpo_moi_b1`) và `harness/grpo_dapo_ds.py` (**chưa có lúc viết file này**).
- Chạy CPU ở máy nhà trước: `python3 harness/grpo_moi_b5.py --selftest-algo` · `python3 harness/grpo_dapo_ds.py --selftest-algo`.
- Dựng và đẩy kit mới cho **cả ba** tài khoản (notebook so md5, kit cũ là dừng ngay):
```
python3 make_kit.py uyenle0712      && kg uyenle datasets version -p kit_uyenle0712      -m "B5 + DAPO-DS 20/11"
python3 make_kit.py trangphngngc    && kg trang  datasets version -p kit_trangphngngc    -m "B5 + DAPO-DS 20/11"
python3 make_kit.py trangphuongngoc && kg trang2 datasets version -p kit_trangphuongngoc -m "B5 + DAPO-DS 20/11"
```
  Kiểm: `ls kit_*/grpo_moi_b5.py kit_*/grpo_dapo_ds.py` đủ 6 tệp. `grpo-luoi-script` không đổi (md5 `grpo_luoi.py` 92d0a9bc… như A/A).
- `make_nb.py` đọc mã nguồn module lúc dựng để biết có phải chép kèm `grpo_moi_b1.py` hay không, nên **dựng notebook sau khi module đã xong**. Dataset version cần vài phút mới dùng được.

## Bước 1 — probe (PROBE_H=2)

```
PROBE_H=2 python3 make_nb.py uyenle0712      luoi-b5-pb-u  probe grpo_lon:spice:101 rpp:spice:101
PROBE_H=2 python3 make_nb.py trangphngngc    luoi-b5-pb-t  probe grpo:spice:101:loss=grpo,mu=2,steps=1000,tag=mu2g gspo:spice:101:loss=grpo,steps=1000,tag=s1000g
PROBE_H=2 python3 make_nb.py trangphuongngoc luoi-b5-pb-t2 probe drgrpo_full:spice:101 dapo_ds:spice:101:eps=0.28,tag=dapo
kg uyenle kernels push -p k_luoi-b5-pb-u  --accelerator NvidiaTeslaT4
kg trang  kernels push -p k_luoi-b5-pb-t  --accelerator NvidiaTeslaT4
kg trang2 kernels push -p k_luoi-b5-pb-t2 --accelerator NvidiaTeslaT4
```
Probe B5 chỉ chạy **2 bước** (module tự ép, mỗi bước 128 câu ≈ 20 min); các lượt khác 20 bước. Đọc log: `kg <tk> kernels output <user>/<kernel> -p runs/luoi/20_11/<kernel> --file-pattern '\.(log|json|txt|md)$'`.

**Đạt khi đủ cả (mục 7.3 + 12.4):**
- Ô 3: selftest `grpo_moi_b5.py` / `grpo_dapo_ds.py` / `grpo_moi_b1.py` / cổ điển đều ĐẠT.
- Không Traceback/OOM; có dòng `[xong] … s/bước · đỉnh VRAM x GiB`.
- Dòng `GRPOConfig:` đúng:
  - lượt 1, 2: `gradient_accumulation_steps 32`, `generation_batch_size 128`, `steps_per_generation 32`, `num_iterations 1`, `loss_type dapo`; dòng `[b5]` in P 16 × G 8 = 128, max_steps 2 (probe).
  - lượt 3: `loss_type grpo`, `num_iterations 2`; `[đè cấu hình]` có `loss_type: grpo, num_iterations: 2`.
  - lượt 4: `loss_type grpo`, `num_iterations 2`; `[moi_b1] --algo gspo → grpo` và `[đè cấu hình]` có `importance_sampling_level sequence, epsilon 0.0003, epsilon_high 0.0004, loss_type grpo` (đã kiểm mã: bí danh `gspo` không có `loss_type`, cờ `--loss-type grpo` ghi sau nên đè đúng).
  - lượt 6a: `[moi_b1] --algo drgrpo_full → drgrpo`, `loss_type dr_grpo`, `scale_rewards none`, `num_iterations 1`, β 0,04.
  - lượt 6b: `epsilon_high 0.28`, `num_iterations 1`, β 0,04.
- **VRAM lô 128 (lượt 1, 2):** đỉnh ≤ ~14 GiB trên T4 16 GiB. Tràn hoặc > 14,5 GiB thì lùi P = 8 cho **cả hai** lượt (giữ một lô chung): `grpo_lon:spice:101:b5p=8,tag=p8` · `rpp:spice:101:b5p=8,tag=p8` (accum 16, 125 bước, tự suy). Log mỗi bước phải có `luoi/n_cau_lo` = 128 (hoặc 64), `luoi/rpp_std` hữu hạn > 0.
- **DAPO (6b):** log mỗi bước có tỉ lệ nhóm bị loại trong (0; 1), dự kiến 0,15–0,35 (luôn 0 ⇒ bộ lọc không chạy; gần 1 ⇒ thưởng hỏng) và **số lần lấy bù** > 0 ở một số bước; có hai ngân sách (nhóm dùng để update và tổng nhóm đã rollout). Tên dòng log xem docstring `grpo_dapo_ds.py` khi module xong (ô theo dõi in sẵn dòng bắt đầu `[dapo_ds]`).
- **GSPO (4):** `clip_ratio` > 0 ở một số bước (khoảng cắt 3e−4/4e−4 rất hẹp). Luôn 0 ⇒ dừng kiểm.
- **GRPO μ=2 (3):** `clip_ratio` = 0 là bình thường; kiểm μ=2 bằng `num_iterations 2` và nhịp thời gian (bước có sinh xen bước không sinh).

## Bước 2 — train

```
GIU_CK=3 CAT_H=10.8 python3 make_nb.py uyenle0712      luoi-b5-u-1  train grpo_lon:spice:101 rpp:spice:101
GIU_CK=3 CAT_H=10.8 python3 make_nb.py trangphngngc    luoi-b5-t-1  train grpo:spice:101:loss=grpo,mu=2,steps=1000,tag=mu2g gspo:spice:101:loss=grpo,steps=1000,tag=s1000g
GIU_CK=3 CAT_H=10.8 python3 make_nb.py trangphuongngoc luoi-b5-t2-1 train drgrpo_full:spice:101 dapo_ds:spice:101:eps=0.28,tag=dapo
kg uyenle kernels push -p k_luoi-b5-u-1  --accelerator NvidiaTeslaT4
kg trang  kernels push -p k_luoi-b5-t-1  --accelerator NvidiaTeslaT4
kg trang2 kernels push -p k_luoi-b5-t2-1 --accelerator NvidiaTeslaT4
```
- `GIU_CK=3` cho cả ba kernel: B5 lưu mỗi 2 bước (31 điểm lưu), μ=2 lưu mỗi 25 bước trên 1.000 bước (PPO 1.000 bước từng hết đĩa).
- `CAT_H` luôn đặt **dưới giờ còn lại** của tài khoản (`kg ca quota`), trừ ~0,3 h cho ô 1–3 và lưu Output. Còn < 11 h thì `CAT_H = còn lại − 0,3`.
- Đã dùng lại A/A thì không cần `MOI`, `CAN_CK`.

**Nối tiếp khi chạm trần** (cùng chuỗi lượt, trỏ kernel trước; ô 2 chép điểm lưu từ output kernel trước, thiếu là dừng):
```
GIU_CK=3 CAT_H=10.8 MOI= python3 make_nb.py uyenle0712 luoi-b5-u-2 train grpo_lon:spice:101 rpp:spice:101 uyenle0712/luoi-b5-u-1
kg uyenle kernels push -p k_luoi-b5-u-2 --accelerator NvidiaTeslaT4
```
(`luoi-b5-t-2…4` trỏ `trangphngngc/luoi-b5-t-<n−1>`; `luoi-b5-t2-2…3` trỏ `trangphuongngoc/luoi-b5-t2-<n−1>`.) Commit 3 của t2 nếu 6a đã xong: `… train dapo_ds:spice:101:eps=0.28,tag=dapo - trangphuongngoc/luoi-b5-t2-2` (hoặc thay `-` bằng `grpo:spice:101:tag=aa2` với `MOI=grpo:spice:101:tag=aa2` nếu phải chạy lại A/A).
- Log mỗi lượt nối tiếp **phải** có `[tiếp từ] …/checkpoint-N` và `[nạp default] … |lora_B| 0.0000 → x>0`. Thiếu là đã quay về S1: dừng.
- Lượt dapo_ds nối tiếp: bộ đếm hai ngân sách có thể bắt đầu lại từ 0 sau resume; cộng dồn từ log các commit.
- Theo dõi mỗi 2 phút: bước, s/bước, thưởng, KL (lượt cũ 0,002–0,05; > 0,1 kéo dài thì ghi lại).
- Ô theo dõi hiển thị bước/62 cho B5 (125 nếu `b5p=8`), /1.000 cho lượt 3–4, /500 cho 6a–6b.

## Phân công theo giờ còn lại

Đo bằng `kg ca quota` lúc 20/11 22:03 giờ VN (15:03 UTC), làm mới **21/11 00:00 UTC = 07:00 giờ VN thứ Bảy**:

| tài khoản | đã dùng | còn | không có kernel đang chạy |
|---|---|---|---|
| uyenle (uyenle0712) | 20,80 h | 9,20 h | ✔ |
| trang (trangphngngc) | 14,30 h | 15,70 h | ✔ |
| trang2 (trangphuongngoc) | 0,00 h | 30,00 h | ✔ |

- Tối 20/11 (trước 07:00 21/11): ba probe 2 h (mỗi tài khoản một) dùng giờ sắp mất. Giờ của trang2 sẽ mất 30 h lúc làm mới, nên probe t2 đạt thì đẩy luôn `luoi-b5-t2-1` [suy: phiên vắt qua mốc làm mới tính vào tuần nào thì chưa kiểm].
- Tuần 21–27/11 (mỗi tài khoản 30 h = 2 commit 11 h + ~8 h dư):
  - uyenle: `luoi-b5-u-1`, `-u-2` ⇒ xong lượt 1–2.
  - trang: `luoi-b5-t-1`, `-t-2` (lượt 3–4 mới ~50%).
  - trang2: `luoi-b5-t2-2` (+ `-t2-3` nếu `-t2-1` đã chạy tối 20/11) ⇒ xong 6a, 6b.
  - ~8 h dư mỗi tài khoản: chấm tập kiểm lượt nào xong trước (`make_test_nb2.py`, ~5–6 h).
- Tuần 28/11–4/12: trang `luoi-b5-t-3`, `-t-4` ⇒ xong lượt 3–4; hai tài khoản kia chấm test + độ đo văn bản (kernel CPU).

## Lượt 5 (GRPO A/A μ=1) — dùng lại, không chạy lại

Lượt `grpo:spice:101` = `luoi-t2-3` → `luoi-t2-4` (tiếp từ ck175) → `luoi-t2-11` (tiếp từ ck400), test ở `uyenle0712/luoi-test-u-4` (exec 59,74; `runs/luoi/8_11/test_u_4/score_grpo_spice_aa_101_test_raw.jsonl`, 4.463 dòng).
- Mã: md5 `grpo_luoi.py` 92d0a9bc…, `grpo_spice.py` 84891081…, `build_branch_data.py` 619e63e1… trong notebook ba kernel đó **trùng** bản hiện tại ở `ds/` và `harness/` (không commit nào sửa từ 2/11).
- Thư viện: trl 0.29.1 · transformers 5.20.2 · peft 0.21.2 (notebook ghim, assert) · torch 2.11.0; đúng bộ mà mọi lượt lưới mới sẽ chạy (log Kaggle gần nhất 16/11: torch 2.11.0+cu130).
- Giới hạn phải khai: commit đầu (bước 1–175) chạy torch 2.11.0+**cu128**, hai commit sau +cu130; A/A chạy thẳng `grpo_luoi.py`, còn 6a/6b đi qua lớp bọc (`grpo_moi_b1.py`, `grpo_dapo_ds.py`) với cấu hình mặc định giống hệt (vá `GRPOConfig` rỗng ở đường so sánh). Chạy lại A/A cũng không bỏ được biến thiên GPU giữa các lượt train (~0,7–0,9 exec, report/320 §21), nên chạy lại không làm phép so chặt hơn mà tốn thêm ~22 h.
- Kiểm khi chạy: dòng phiên bản ở ô 1 của mỗi kernel mới phải in `0.29.1 5.20.2 0.21.2 2.11.0+cu1xx`. Nếu Kaggle đã đổi torch (≠ 2.11.0) thì A/A không còn cùng môi trường: khi đó chạy lại `grpo:spice:101:tag=aa2` như mục trên.
