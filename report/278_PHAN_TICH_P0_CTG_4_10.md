# 278 — Phân tích P0 của CTG-GRPO (4/10/2026)

Nguồn: `runs/ctg/p0/p0b.json` (75 câu nhắc C1 có lớp vàng scroll/type/back, log P(token đầu là động từ
chạm) và logp/token câu chuẩn, cho S1 · ck250 · ck500) · `runs/grpo_spice/pred_ck{250,500}.jsonl` ·
`runs/c1/c1_mau.jsonl`. 0 GPU. **Số val, cấm trích.** Action gốc: `harness/tai_lieu_2026-10-04/276_…`.

## 1. Luật cũ trượt vì lấy trung bình của LOG

| lớp | TB log P(tap) S1 → ck500 | TB P(tap) S1 → ck250 → ck500 | Δ P(tap) ck500 − S1 [KTC95 bootstrap bước] |
|---|---|---|---|
| scroll (32) | −3,31 → −3,91 | **0,140 → 0,161 → 0,212** | **+0,072 [+0,025; +0,126]** |
| navigate_back (15) | −2,36 → −2,90 | 0,232 → 0,253 → 0,281 | +0,049 [−0,011; +0,119] |
| type (28) | −4,06 → −6,41 | 0,076 → 0,058 → 0,054 | −0,022 [−0,042; −0,005] |

Trung bình log là trung bình nhân, bị chi phối bởi các bước P(tap) gần 0 (trung vị P(tap) của S1 chỉ
0,026). Tính theo **xác suất**, tức đúng đại lượng quyết định câu lấy mẫu và đúng thứ `ĉ_k` của CTG
đo, thì scroll **tăng đơn điệu** qua hai điểm lưu, KTC loại 0. Phân tích này làm **sau khi thấy số**.

## 2. GRPO phân cực, không kéo đều

Chia 32 bước scroll theo P(tap) của S1:

| nhóm | P(tap) S1 → ck500 | số bước tăng | S1 đúng → ck500 lật sang chạm |
|---|---|---|---|
| thấp (10) | 0,006 → 0,002 | 0/10 | 0 |
| giữa (11) | 0,038 → 0,045 | 3/11 | 0 |
| cao (11) | **0,363 → 0,571** | **10/11** | **4** |

Tương quan giữa log P(tap) của S1 và mức đổi: **0,71** (75 bước). Bước S1 đã chắc chắn viết đúng loại
thì GRPO làm chắc hơn; bước S1 đã phân vân thì GRPO đẩy hẳn sang câu chạm.
Bốn bước scroll bị lật đều có P(tap) tăng đơn điệu S1 → ck250 → ck500:
0,394 → 0,611 → 0,947 · 0,120 → 0,209 → 0,530 · 0,328 → 0,405 → 0,595 · 0,259 → 0,288 → 0,442.
Trong 13 bước có greedy sai loại ở ít nhất một mô hình, 12 bước P(tap) tăng đơn điệu.
Theo số mẫu S1 là câu chạm (0 / 1–2 / ≥3 trong 8 mẫu): mọi lần lật đều ở nhóm có ≥1 mẫu chạm; 36 bước
0 mẫu chạm không lật bước nào.

Logp/token câu chuẩn cũng giảm (scroll −0,14 [−0,25; −0,06], back −0,20 [−0,42; −0,03]; type −0,05, KTC
phủ 0).

## 3. Hệ quả cho thiết kế CTG

- **Khớp:** CTG chỉ cộng khi `std(c) > 0`, tức nhóm có cả câu đúng loại lẫn câu chạm. Đó đúng là nhóm
  "phân vân", nơi mọi lần lật xảy ra. Bước 0 mẫu chạm thì CTG để yên, mà ở đó cũng không có gì phải sửa.
- **Lớp type:** GRPO tự làm type tốt lên (P(tap) giảm), CTG lớp type nhiều khả năng tự tắt (λ → 0).
  Không hại.
- ⚠️ **Rủi ro vùng chết của λ [suy, chưa đo]:** đích `p_k` lấy từ 9 câu S1 trên val C1 (scroll 0,837),
  trong khi ở P0(a) `ĉ_scroll` trên câu nhắc train là 0,87–0,90 (chỉ 3 nhóm, nhiễu). Nếu tỉ lệ đúng loại
  của S1 trên câu nhắc train thật sự cao hơn đích ~0,05 thì λ giảm dần về 0 trong khoảng 150–200 bước
  đầu, và chỉ tăng lại khi mô hình trôi quá 0,05, mà theo §1 phải tới khoảng ck500 mới trôi cỡ đó. Khi
  ấy A3 gần như trùng A2. Phép kiểm: Ô C6 của `colab_ctg_train.md` in λ_scroll mỗi 2 phút; nếu λ_scroll
  = 0 trước bước 250 thì rủi ro này đã xảy ra. Cách sửa đổi tham số khoá trước (cần user quyết):
  đo `p_k` của S1 trên chính 2.000 câu nhắc train (Kaggle T4, 0 đồng).

## 4. Kết luận đọc

Giả thuyết của 276 đúng ở dạng hẹp hơn: GRPO không kéo cả lớp về câu chạm, mà **đẩy các bước phân vân
sang câu chạm** và làm các bước dễ chắc hơn. Trung bình theo xác suất vẫn tăng có ý nghĩa ở scroll. Luật
P0(b) cũ (trung bình log) đo sai đại lượng; hai luật thay thế (đếm lật greedy, §2; trung bình xác suất,
§1) đều đạt nhưng đều đặt **sau khi thấy số** ⇒ phải khai.

## 5. Đo đích trên câu nhắc train (Kaggle T4, 4/10 chiều) — rủi ro vùng chết KHÔNG xảy ra

Nguồn: `runs/ctg/dich/` (S1, 8 mẫu nhiệt độ 1,0, 440 câu nhắc train, 0 câu rỗng, số từ TB 6,39).

| lớp | đích mới (train) [KTC95] | đích cũ (val C1) | câu nhắc "lẫn" (std(c) > 0, CTG có tác dụng) | câu sai loại thành tap |
|---|---|---|---|---|
| scroll (242) | 0,856 [0,820; 0,887] | 0,837 | 79 (33%) | 235/279 (84%) |
| type (114) | 0,814 [0,763; 0,860] | 0,813 | 55 (48%) | 168/170 |
| back (84) | 0,707 [0,644; 0,768] | 0,733 | 60 (71%) | 152/197 (44 thành scroll) |

- Đích mới gần như trùng đích cũ, KTC phủ đích cũ ở cả ba lớp. Con số 0,87–0,90 của P0(a) là nhiễu của
  3 nhóm, không phải lệch phân phối train/val. Mã dùng đích mới (`--dich`) vì đo đúng phân phối train.
- Mô phỏng λ (200 lượt, lấy mẫu lại từ phân bố trên, đúng tham số 276 §6): không trôi thì λ_scroll dao
  động quanh 0,84–0,93 (chạm 0 ở 1/4 đầu trong 32% lượt rồi hồi lại); trôi −0,07 (cỡ ck500) thì λ lên
  1,41 ở giữa lượt và 2,6 ở cuối ⇒ bộ điều khiển phản ứng đúng chiều. [mô phỏng, không phải đo]
- Câu sai của scroll 84% là câu chạm ⇒ CTG nhắm đúng dạng lỗi.
