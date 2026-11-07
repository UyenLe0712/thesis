# B3 — ba phần thưởng mới + H2 (6/11/2026)

## Phần thưởng mới (`harness/thuong_moi.py`)

| tên `--reward` | công thức | nguồn kế hoạch |
|---|---|---|
| `spice_cong` | r = SPICE · a − phạt độ dài; a = 1 nếu đúng loại thao tác, `THUONG_A_SAI` (mặc định 0,1) nếu sai | report/330 §7 hàng 5 |
| `ten_loai` | r = 0,5 · F1(tên vàng) + 0,5 · a − phạt; bước không có tên vàng: r = a − phạt | report/330 §7 hàng 6 |
| `loai` | r = a − phạt (chỉ đúng loại thao tác) | report/326 **T5** (chỉ để giải thích, không phải backbone T5) |

- Loại thao tác: `metric_exec.canon_action(·, strict_back=True)` của câu sinh so với của câu chuẩn.
- Phạt độ dài và câu rỗng = 0 giống mọi thưởng khác của lưới (`grpo_luoi.lam_thuong`).
- Tên vàng: `descriptors_ten.jsonl` (30.233 bước, tầng `ten_ro` của `harness/dg1_cache/train_ac/descriptors.jsonl`;
  tầng ký hiệu, không tên thì coi như không có tên). Tra theo cột `key` mà TRL chuyển vào hàm thưởng.
  F1 tính trên tập token; phía câu bỏ mạo từ/giới từ, động từ thao tác, từ vai trò chung và từ vị trí.

**Đăng ký:** không sửa `grpo_luoi.py`. Chạy bằng `thuong_moi.py` thay cho `grpo_luoi.py`, mọi cờ giữ nguyên:

```
python thuong_moi.py --train --reward spice_cong --bundle B --merged M --out O --resume auto
```

`thuong_moi.cai()` nối ba tên vào `GL.REWARDS` (nên `choices` của `--reward` nhận được) và thay
`GL.dung_bo_cham`/`GL.lam_thuong`. Thưởng cũ đi qua nguyên bản.
Khi dựng notebook train (việc của agent dựng notebook, không phải B3): chép thêm `thuong_moi.py`,
`metric_exec.py`, `descriptors_ten.jsonl` vào thư mục làm việc (có sẵn trong dataset `uyenle0712/thuong-moi-b3`),
và trong `make_nb.py` cho `tep_cua()` trả `thuong_moi.py` khi thưởng là `spice_cong|ten_loai|loai`.
Cảnh báo của report/330: `spice_cong` nghĩ ra sau khi đã thấy số test ck500, phải khai.

## Kiểm (Kaggle CPU, kernel `uyenle0712/h2-thuong-b3`)
- `thuong_moi.py --selftest-moi`: 7 nhóm assert (câu rỗng = 0; sai loại < đúng loại ở mọi thưởng; cổng = A_SAI·SPICE;
  `ten_loai` phân biệt phần tử còn `loai` thì không; bước không tên `ten_loai` = `loai`; F1 tên không phạt vai trò/vị trí;
  đăng ký vào `--reward`).
- `grpo_luoi.py --selftest-thuong` (spice, cider) vẫn đạt sau khi nạp cùng gói.
- H2 thử 30 bước, rồi đủ.
Kết quả (bản 2, 6/11 20:36): `--selftest-moi` ĐẠT · `--selftest-thuong spice,cider` ĐẠT · H2 thử và đủ mã thoát 0 (đủ: 344 s).
Bản 1 trượt selftest vì phép kiểm đòi SPICE câu đúng > câu sai ở cả "Scroll down", trong khi SPICE("Scroll down","Scroll down") = 0
(câu không có tuple); đã sửa phép kiểm, không sửa hàm thưởng.

## H2 (`harness/h2_thuong.py`)
Dữ liệu 8 mẫu C1 (S1/101, T = 1,0, 400 bước val; exec 249 bước chạm). Số VAL, không trích.
Kết quả ghi `report/320` mục 16, tệp `runs/giai_thich/h2_b3/`.
