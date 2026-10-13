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
(Cập nhật 13/10 tối: phép kiểm ở §5 xác nhận hai lượt trên thiếu bước, nhưng cặp *cải thiện* không có tín hiệu chung ⇒ vẫn đóng.)
Cùng mẫu hình với TAGE, CW-RA, RAFT: các cách train tiếp hoặc sửa câu trên ck500 đến nay chưa cách nào vượt ck500.
Đối chứng `gold` (`ga_dpo.py --kieu gold`) mà action §7 đề xuất chỉ cần khi có nhánh thắng ⇒ không chạy.

## 5. Phép kiểm "thiếu bước hay cặp không có tín hiệu" (13/10 tối, Colab L4, 164 phút)

Runbook `harness/runbook/colab_kiem_hoc_dpo_314.md`, notebook `_scripts/314/colab_gadpo/kiem_hoc_dpo_314_colab.ipynb`,
script `_scripts/314/ds_gadpo314/kiem_hoc_dpo.py`. Tách 830 cặp theo câu nhắc thành 200 cặp **đã thấy** (train) + 200
cặp **giữ riêng** (không train), mỗi tập 100 cải thiện + 100 giữ. Train 5 epoch trên 200 cặp, lr 5e-5, accum 8
⇒ 125 bước, β 0,1, λ_nll 1,0, nền và LoRA như `ga_dpo.py`. Đo ở chế độ eval. Luật đọc viết trước khi chạy (runbook §0).

| epoch | đã thấy: acc | margin | lp chosen | lp rejected | giữ riêng: acc | margin | lp chosen | ‖B‖ |
|---|---|---|---|---|---|---|---|---|
| 0 | 0,000* | +0,000 | −0,260 | −0,367 | 0,000* | +0,000 | −0,261 | 0,0000 |
| 1 | 0,910 | +0,414 | −0,230 | −0,383 | 0,560 | +0,009 | −0,258 | 0,6452 |
| 3 | 0,990 | +8,290 | −0,072 | −1,130 | 0,600 | +1,130 | −0,358 | 1,4487 |
| 5 | **1,000** | +12,332 | −0,041 | −1,575 | **0,610** | +1,602 | **−0,457** | 1,5536 |

\* Epoch 0 policy trùng ref (‖B‖ = 0) nên margin đúng bằng 0, acc tính theo margin > 0 nên ra 0. Đây là phép kiểm nạp đúng, đạt.

Dòng `[kết luận]` của script: **CẶP CÓ TÍN HIỆU** (acc đã thấy ≥ 0,80, acc giữ riêng ≥ 0,60).

Đọc:
- **Khâu train không lỗi.** Học thuộc 200/200 cặp đã thấy. Hai lượt ở §2 (52 bước, mỗi cặp thấy một lần) không học
  là do **thiếu bước**, không phải do mã.
- **Tín hiệu chung có nhưng yếu.** Giữ riêng 0,610 = 122/200: hơn đoán mò (p ≈ 0,002, kiểm nhị thức một phía so 0,5)
  nhưng KTC95 ≈ [0,54; 0,68] nên không tách được khỏi mốc 0,60 của luật. Acc giữ riêng chững lại từ epoch 3
  (0,56 → 0,60 → 0,61) trong khi tập đã thấy lên 1,00 ⇒ phần lớn những gì học thêm sau epoch 3 là học thuộc.
- **Dấu hiệu bất lợi:** trên câu nhắc giữ riêng, log-p/token của câu chosen **giảm đều** −0,261 → −0,457. Margin dương
  lên chủ yếu nhờ đẩy câu rejected xuống mạnh hơn, NLL λ 1,0 không chặn được. Mô hình ít muốn viết câu chosen trên câu
  nhắc mới hơn trước khi train, nên greedy có thể trôi; chỉ chấm test mới biết.
- **Tách theo loại cặp (tập giữ riêng, mỗi loại n = 100):**

| epoch | cặp *cải thiện* (chosen = mẫu trội greedy) | cặp *giữ* (chosen = greedy, rejected = mẫu thua) |
|---|---|---|
| 1 | 0,46 | 0,66 |
| 3 | 0,47 | 0,73 |
| 5 | **0,46** [~0,36; 0,56] | **0,76** [~0,68; 0,84] |

  Toàn bộ 0,61 đến từ cặp *giữ*. Trên cặp *cải thiện*, mô hình **không đoán đúng hơn tung đồng xu** ở epoch nào,
  dù đã học thuộc 100/100 cặp cải thiện của tập đã thấy.

**Kết luận (theo câu đọc phụ đã viết trong runbook §0 trước khi chạy):** mô hình chỉ học "tránh mẫu thua", không học
"viết hơn greedy". Tránh mẫu thua không đổi được câu greedy theo hướng tốt, còn log-p câu greedy trên câu nhắc mới lại
giảm. Mẫu "trội greedy" mà ck500 tự sinh không chứa quy luật chung nào: chúng thắng nhờ dao động lấy mẫu so với một câu
chuẩn duy nhất. Đây là bằng chứng trực tiếp cho giả thuyết đã nêu ở §3 và ở `report/314_KET_QUA_RAFT_12_10.md` §4,
nay đã kiểm: cả RAFT lẫn GA-DPO hỏng vì **nguồn cặp**, không vì cách train.

⇒ **Không chạy GA-DPO đủ 830 cặp, không chấm test. Đóng action 314, giữ ck500** (+ R3/ACE khi cần số chữ).
Hệ quả cho các hướng sau: mọi cách tự cải thiện ck500 bằng chọn mẫu của chính ck500 theo thước câu (RAFT, DPO, best-of-n
làm đích) đều dùng chung nguồn tín hiệu này, nên không nên mở lại nếu không đổi cách lấy đích.

Tệp: `runs/rd314/D/kiem_hoc/` (`kiem_lam1/kiem_hoc_dpo.jsonl`, `ket_luan.json`, `kiem_lam1.log`, zip gốc).
