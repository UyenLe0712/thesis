# Lệnh chạy Kaggle sau khi hạn mức làm mới (7/11/2026, 7:00 giờ VN)

Dựng ngày 6/11. Mỗi notebook đã có bản chạy thử ngắn trên Kaggle tối 6/11, kết quả ghi ở mục cuối.
Chạy từ thư mục `_bundles/luoi`. Kiểm hạn mức trước: `kg ca quota`.

| Thứ tự | Tài khoản | Kernel | Việc | Trần | Đã chạy thử |
|---|---|---|---|---|---|
| 1 | `uyenle` | `luoi-test-u-3` | Test SFT tiếp · RLOO · REINFORCE EMA (+ SPICE), hàng đợi trên 2 GPU | 11 h | `luoi-test-smoke-u` |
| 2 | `trang2` | `luoi-t2-4` | Chạy tiếp A/A `grpo:spice:101` từ điểm lưu 175 · K1 `drgrpo:spice:101` (GRPO bỏ chia std) | 11 h | `luoi-train-smoke-t2` (A/A + PPO) |
| 3 | `trang` | `luoi-t-3` | PPO λ=1 và λ=0,95 (μ=2, 1.000 bước, mỗi GPU một lượt) | 11 h | PPO λ=1 trong `luoi-train-smoke-t2` |
| 4 | `trang` | `luoi-nt-t-1` | Bước không chạm (2.495 bước, noharm so S1) cho ck500/202 và xao101 | 11 h (dự kiến ~2,5 h) | `luoi-nt-smoke-t` |
| 5 | `uyenle` | `luoi-probe-u-2` | Probe SCST + CIDEr-D và REINFORCE không mốc (`vanilla`), 20 bước | 1,5 h | chưa (chế độ probe của make_nb đã dùng nhiều lần) |

```
kg uyenle kernels push -p k_luoi-test-u-3 --accelerator NvidiaTeslaT4
kg trang2 kernels push -p k_luoi-t2-4 --accelerator NvidiaTeslaT4
kg trang  kernels push -p k_luoi-t-3 --accelerator NvidiaTeslaT4
# sau khi luoi-t-3 xong hoặc nếu Kaggle cho chạy song song hai phiên GPU:
kg trang  kernels push -p k_luoi-nt-t-1 --accelerator NvidiaTeslaT4
kg uyenle kernels push -p k_luoi-probe-u-2 --accelerator NvidiaTeslaT4   # sau luoi-test-u-3
```

Nối tiếp khi chạm trần:
- test: `PREV=uyenle0712/luoi-test-u-3 python3 make_test_nb2.py uyenle0712 luoi-test-u-4 full <cùng danh sách lượt>`; notebook chép pred/raw cũ rồi chạy nốt.
- train: `MOI= python3 make_nb.py <user> <kernel mới> train <lượt0> <lượt1> <kernel trước>`; phải thấy dòng `[nạp default] … → x>0` trong log của lượt nối tiếp.
- PPO 1.000 bước cần khoảng 41 h một GPU [suy, từ probe 3/11] ⇒ khoảng 4 commit, qua hai tuần hạn mức.

Đọc kết quả: tải `kernels output`, đặt thẳng vào `runs/luoi/<thư mục của đợt>`, rồi ghi số vào `report/320` mục 14.
Số của bản chạy thử (`SMOKE`) chỉ để kiểm đường chạy, không dùng.

## Kết quả chạy thử 6/11 tối
- `luoi-test-smoke-u` (uyenle): ĐẠT. Phiên bản đúng, 2×T4, hoà S1 16/20, bộ chấm 10/10, 3 lượt × 20 câu, dùng lại kết quả cũ 20/20; 0,18 h. Tệp `runs/luoi/smoke_6_11/test_u/`.
- `luoi-nt-smoke-t` (trang): ĐẠT. Tìm thấy IMG_NT (`thesis-nontap-images/test_ac/images`), hoà 16/20, mỗi lượt 20 câu không chạm 0 rỗng, noharm chạy xong cho ck202_500 và xao101_500. Hai lượt cho cùng số (khớp loại 0,80) nhưng câu khác nhau 4/20 ⇒ nạp đúng hai adapter khác nhau. ~0,13 h. Tệp `runs/luoi/smoke_6_11/nt_t/`.
- `giai-thich-6-11-k` (trang, CPU): xong, số ở `report/320` mục 15.
- `luoi-train-smoke-t2` (trang2): ĐẠT. A/A `grpo:spice:101` nối tiếp từ checkpoint-175: `[nạp default] 504 tensor · |lora_B| 0 → 5,78` (x>0), chạy bước 176–183, kl 0,003–0,005 (không về 0 ⇒ không quay lại S1), ~153 s/bước. PPO λ=1 chạy 8 bước, 137–142 s/bước, v_ev/v_loss ghi được, 0 Traceback, 0 IndexError. Cả hai dừng do trần giờ chạy thử (mã thoát −15, đúng dự kiến). `|A| nan` ở GRPO thường là bình thường (TRL không ghi chỉ số này, các lượt cũ cũng vậy). Tệp `runs/luoi/smoke_6_11/train_t2/`.
