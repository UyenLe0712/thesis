# 314 — Kết quả RAFT từ ck500 (12/10/2026): thua ck500, đóng hướng

Action gốc: `harness/314_ACTION_RAFT_VA_GADPO_12_10_full.md`. Tệp kết quả: `runs/rd314/R/` (sinh mẫu, chọn, train)
và `runs/rd314/E/` (sinh câu val/test, chấm chữ, chấm exec). Mã: `_scripts/314/`.

## 1. Đã chạy gì

| pha | máy | việc | kết quả |
|---|---|---|---|
| R-1 | Kaggle T4×2 | ck500 sinh greedy + 8 mẫu (T = 0,7) trên 2.000 câu nhắc train hàng `[1000, 3000)` — ck500 chưa thấy trong GRPO | 2.000 hàng, 0 rỗng |
| R-2 | Kaggle CPU | chọn mẫu trội greedy trên ba thước (SPICE · chrF · …), loại mẫu lệch độ dài > 3 từ | đổi đích ở **415/2.000 (20,75%)**, ΔSPICE TB khi đổi **+0,57**; cổng ngưỡng 15% **ĐẠT** |
| R-3 | Kaggle T4 | SFT tiếp ck500 trên 2.000 đích đã chọn: 125 bước × lô 16, lr 1e-5 (warmup 10 bước, cosine) | loss 0,31 → ~0,2; 110,7 s/bước; VRAM 6,7 GiB; 230,8 phút |
| E | Kaggle T4×2 | sinh greedy val 1.002 + test 4.463 bước; chấm 7 thước chữ; UGround chấm các bước câu khác ck500 | 2,74 h |
| máy nhà | WSL CPU | `harness/ra_grpo/doc_exec_cw.py` ghép exec · `ktc_chu.py` KTC thước chữ | hiệu chuẩn 40 câu ck500 chấm lại lệch 0 |

## 2. Thước chữ, tập kiểm (n = 4.463)

| thước | ck500 | RAFT | Δ |
|---|---|---|---|
| BLEU-4 | 52,36 | 51,65 | −0,71 [−1,06; −0,30] |
| METEOR | 37,91 | 37,52 | −0,39 |
| ROUGE-L | 68,34 | 67,79 | −0,56 [−0,84; −0,26] |
| CIDEr-D | 430,04 | 423,21 | −6,97 [−10,82; −3,05] |
| SPICE | 45,79 | 44,89 | −0,90 |
| chrF | 62,86 | 62,37 | −0,49 |
| BERTScore | 67,07 | 66,62 | −0,45 |

**0/7 thước hơn ck500** (luật thắng: ≥ 4/7). KTC ghép cặp có cho ba thước (`ktc_chu.py`), cả ba nằm trọn dưới 0.
Câu khác ck500: 710/4.463 bước chạm. Câu rỗng: 1 ở cả hai nhánh. Trên val cũng 0/6 (số val, không trích).

## 3. exec, D.3, AitW (4.463 bước chạm)

| nhánh | exec | D.3 | AitW |
|---|---|---|---|
| ck500 | 60,65 [58,90; 62,38] | 67,02 | 76,25 |
| RAFT | 60,23 [58,50; 61,93] | 66,52 | 75,87 |
| S1/101 | 59,11 | 65,49 | 74,37 |

| phép so | exec | D.3 | AitW |
|---|---|---|---|
| RAFT − ck500 | **−0,43 [−0,82; −0,04]**, cứu 31 phá 50, p = 0,046 | −0,49 [−0,89; −0,11], p = 0,019 | −0,38 [−0,81; +0,04], p = 0,086 |
| RAFT − S1/101 | +1,12 [+0,36; +1,88], p = 0,003 | +1,03 | +1,50 |

Kaggle chỉ gọi UGround ở 710 bước câu khác ck500 (mỗi GPU 355); bước còn lại lấy nguyên dòng tệp thô
`runs/grpo_spice/score_ck500_test_raw.jsonl`. Tệp gộp: `runs/rd314/E/exec_raft/score_raft_gop_raw.jsonl`.

## 4. Đọc kết quả

- Theo bảng §6 của action: **RAFT < 4/7 ⇒ ghi vào "các hướng đã thử", giữ ck500** (+ R3/ACE khi cần số chữ).
- RAFT kém ck500 nhẹ nhưng có ý nghĩa ở cả chữ lẫn exec: đổi 16% câu thì phá nhiều hơn cứu (50 vs 31 bước exec).
  Cùng mẫu hình với TAGE (−0,43 exec) và CW-RA (−2,13): mọi cách train/sửa tiếp trên ck500 đến nay đều kéo ck500 xuống.
- Chọn mẫu theo thước câu trên câu nhắc train cho ΔSPICE +0,57 ở 21% câu nhắc, nhưng SFT trên các đích đó không
  chuyển thành cải thiện trên test. Một khả năng: đích trội greedy chỉ nhờ dao động lấy mẫu (thắng một câu chuẩn duy
  nhất), không phải câu tốt hơn một cách có hệ thống. Chưa kiểm.
- So S1/101 RAFT vẫn hơn (+1,12 exec), nhưng phần hơn đó là của ck500 (ck500 − S1 = +1,55).

## 5. Nhánh GA-DPO (cùng action) — trạng thái 12/10

- Lượt 1 (lr 5e-6, 830 cặp, 52 bước, Colab L4, 107 phút): policy **không dịch khỏi ref** — margin trong
  [−0,016; +0,002], acc 0,38–0,49, log-p câu chosen −0,270 → −0,279. Nguyên nhân: LoRA mới (B = 0) + lr 5e-6 + 52 bước.
  Đây là lỗi siêu tham số, không phải bằng chứng GA-DPO hỏng. Không chấm lượt này (tiết kiệm ~5 h T4).
  Lưu ở Drive `thesis/gadpo314/` và Kaggle dataset `gadpo-314-adapter`.
- Lượt 2: chỉ đổi lr lên **5e-5** (đổi sau khi thấy log lượt 1 — phải khai). Ô D-7/D-8/D-9 trong
  `_scripts/314/colab_gadpo/gadpo_314_colab.ipynb`, ghi ra Drive `gadpo314/lr5e5/` và dataset `gadpo-314-adapter-lr5e5`.
  Chỉ chấm trên Kaggle nếu log cho thấy margin dương và tăng, acc > 0,6 từ khoảng bước 20.
- **Cập nhật 13/10:** lượt 2 acc cao nhất 0,544, margin ≤ +0,064 ⇒ không đạt luật chấm, không chấm.
  Chi tiết và tổng kết action ở `report/314_KET_QUA_GADPO_13_10.md`.
