# 314 — Kết quả GA-DPO từ ck500 (12–13/10/2026): hai lượt đều không học, không chấm, đóng hướng

Nhánh thứ hai của action 314 (`harness/314_ACTION_RAFT_VA_GADPO_12_10_full.md`). Nhánh RAFT cùng action đã có
kết quả riêng ở `report/314_KET_QUA_RAFT_12_10.md` (thua ck500 0/7 thước chữ, exec −0,43). File này ghi nhánh GA-DPO.

Tệp kết quả: `runs/rd314/D/lr5e6/` và `runs/rd314/D/lr5e5/` (log train + `tron_meta.json`, kéo từ Kaggle dataset
`uyenle0712/gadpo-314-adapter` và `gadpo-314-adapter-lr5e5`). Cặp train: `runs/rd314/cap_all.jsonl`.
Mã: `_scripts/314/ds_gadpo314/` (`ga_dpo.py` · `mau_sang_ga.py` · `tron_adapter.py`), notebook
`_scripts/314/colab_gadpo/gadpo_314_colab.ipynb`.

## 1. Thiết kế

- Cùng bộ mẫu với RAFT: ck500 sinh greedy + 8 mẫu (T = 0,7) trên 2.000 câu nhắc train hàng `[1000, 3000)`.
- **830 cặp** = 415 cặp *cải thiện* (chosen = mẫu trội greedy trên các thước câu, rejected = greedy) + 415 cặp *giữ*
  (chosen = greedy, rejected = mẫu thua greedy ở mọi thước). 415 trùng đúng số câu nhắc RAFT đổi đích (20,75%).
- Mục tiêu DPO (β = 0,1) cộng NLL trên câu chosen (λ = 1,0). LoRA mới gắn trên S1 + ck500 đã hoà ở fp32, 52 bước,
  Colab L4 bf16, ~107 phút mỗi lượt. Sau train ghép adapter DPO với ck500 bằng `tron_adapter.py` (r 16, α 32).
- Luật chấm đặt trước lượt 2: chỉ đẩy lên Kaggle chấm test khi log cho thấy margin dương và tăng, acc > 0,6 từ
  khoảng bước 20.

## 2. Log train

| bước | lượt 1: lr 5e-6 · margin | acc | log-p chosen | lượt 2: lr 5e-5 · margin | acc | log-p chosen |
|---|---|---|---|---|---|---|
| 10 | −0,007 | 0,375 | −0,266 | +0,002 | 0,444 | −0,265 |
| 20 | −0,001 | 0,481 | −0,257 | +0,002 | 0,431 | −0,256 |
| 30 | −0,016 | 0,400 | −0,271 | −0,012 | 0,500 | −0,271 |
| 40 | +0,002 | 0,494 | −0,251 | +0,064 | 0,512 | −0,244 |
| 50 | −0,016 | 0,475 | −0,279 | +0,033 | 0,525 | −0,276 |
| 51 | −0,015 | 0,475 | −0,280 | +0,050 | 0,544 | −0,275 |

log-p/token câu chosen đầu → cuối: lượt 1 −0,270 → −0,279 · lượt 2 −0,269 → −0,272. Loss quanh 0,93–0,97 suốt cả hai lượt.
Dòng kiểm token trả lời của lượt 2 đúng (`'Click on the search button.<|im_end|>'`), nên mặt nạ nhãn không sai.

## 3. Đọc kết quả

- **Lượt 1 (lr 5e-6):** policy không dịch khỏi ref, margin dao động quanh 0, acc dưới 0,5. Không chấm.
- **Lượt 2 (lr 5e-5, chỉ đổi lr, đổi sau khi thấy log lượt 1, phải khai):** margin có nhích dương từ bước 40
  (cao nhất +0,064) nhưng không tăng đều, acc cao nhất **0,544 < 0,6**, log-p câu chosen không lên.
  ⇒ **Không đạt luật chấm đặt trước, không chấm test** (tiết kiệm ~5 h T4). Adapter vẫn giữ ở dataset
  `gadpo-314-adapter-lr5e5` nếu sau này cần.
- Không có số test nào cho GA-DPO, nên **không được viết "GA-DPO thua ck500"**. Câu đúng: với 830 cặp, 52 bước,
  LoRA mới khởi tạo B = 0, hai mức lr đã thử không kéo được policy khỏi ref đủ để đáng chấm.
- Một lý do khả dĩ (chưa kiểm): chosen và rejected của cặp cải thiện là hai câu cùng phân bố của ck500, chênh nhau
  chủ yếu ở dao động lấy mẫu. Đây cũng là giả thuyết đã nêu cho việc RAFT không chuyển được ΔSPICE +0,57 trên train
  thành cải thiện trên test. Nếu đúng, tăng lr hay số bước cũng khó cho tín hiệu thật.

## 4. Tổng kết action 314

| nhánh | trạng thái | so ck500 |
|---|---|---|
| RAFT | đã chấm test | 0/7 thước chữ · exec −0,43 [−0,82; −0,04] p = 0,046 |
| GA-DPO lượt 1 (lr 5e-6) | không học, không chấm | — |
| GA-DPO lượt 2 (lr 5e-5) | acc 0,544, dưới luật chấm, không chấm | — |

⇒ **Đóng action 314.** Mô hình giữ **ck500** (+ luật ghép R3/ACE khi cần số chữ, `report/304` §4–5).
Cùng mẫu hình với TAGE, CW-RA, RAFT: các cách train tiếp hoặc sửa câu trên ck500 đến nay chưa cách nào vượt ck500.
Đối chứng `gold` (`ga_dpo.py --kieu gold`) mà action §7 đề xuất chỉ cần khi có nhánh thắng ⇒ không chạy.
