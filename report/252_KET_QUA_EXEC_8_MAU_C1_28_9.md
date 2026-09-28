# 252 — Kết quả chấm `exec` cho greedy và 8 mẫu S1 trên 249 bước click C1 (28/9/2026)

Runbook: `harness/251_ACTION_GPU_EXEC_8_MAU_C1_28_9.md`. Kaggle T4×2, dạng commit, 0 đồng.
Tệp: `runs/c1/exec8/` (output Kaggle nguyên vẹn) · đọc bằng `harness/c1_exec8_doc.py` (CPU + Java 8).

⚠️ **Số val.** S1 đã thấy các bước này lúc train ⇒ mọi số dưới đây lạc quan có hệ thống, chỉ dùng
để quyết trong nội bộ dự án. **Không trích ra luận văn.**

---

## 1. Kết luận

**Cổng §6 của 251 ĐẠT.** Oracle SPICE hơn greedy **+5,22 exec** (KTC95 bootstrap theo episode
[+1,22; +9,36]), thoả cả hai điều kiện: ≥ +2,0 và cận dưới > 0 ⇒ theo luật chốt trước, **được phép
train GRPO thưởng theo metric câu**.

Có ba điểm đi kèm (§4): SPICE là oracle **yếu nhất** trong bốn metric câu đã thử (CIDEr-D +9,64) ·
SPICE hoà ở 33,8% cặp câu cần phân biệt · oracle best-of-9 chỉ là trần, không phải mức RL thu được.

## 2. Kiểm toàn vẹn [đo]

- Câu trong tệp thô khớp `runs/c1/c1_mau.jsonl`: **2.241/2.241** lượt; câu chuẩn khớp 249/249.
- Mọi bước có nút (`n_buttons > 0`), cây trợ năng 249/249 theo log.
- Tính lại từ `score_k*_raw.jsonl` ra đúng từng số của `c1_exec_tong.json`.
- SPICE từng câu tính lại trên WSL tái lập đúng chuỗi `runs/c1/c1_picks.json`.
- UGround-V1-2B commit `ea7109f9…`; cây trợ năng `HarrytheOrange/parsed_AndroidControl` commit `131de085…`.

## 3. Số chính (249 bước click)

| | exec | hit_disk |
|---|---:|---:|
| Greedy S1 | **63,45** | 70,68 |
| Oracle SPICE (1 trong 9 câu, hoà lấy greedy) | **68,67** | 76,31 |
| Trung bình một mẫu (nhiệt độ 1,0) | 55,72 | — |
| Chọn ngẫu nhiên 1 trong 9 câu (kỳ vọng) | 56,58 | — |
| Có ít nhất 1/9 câu bấm trúng (trần chọn trong mẫu) | 79,12 | — |

Từng mẫu k1…k8: 51,81 · 55,02 · 55,82 · 57,83 · 55,42 · 59,04 · 56,22 · 54,62.

Oracle đổi câu ở **119/249** bước. Trên các bước đó greedy đạt 57,98 và oracle đạt 68,91. Có **20**
bước greedy trượt mà oracle trúng, **7** bước ngược lại (McNemar chính xác p = 0,019).
Trong 39 bước greedy trượt nhưng có ít nhất một câu trúng, oracle SPICE cứu được 20 bước.

## 4. Phân tích thêm [đo, ngoài luật §6]

### 4.1 Mức tăng không đến từ việc đổi câu

| trên 119 bước oracle đổi câu | exec |
|---|---:|
| greedy | 57,98 |
| một mẫu chọn ngẫu nhiên (kỳ vọng) | 55,67 |
| oracle SPICE | **68,91** |

Nếu đổi câu ở đúng 119 bước đó nhưng lấy mẫu ngẫu nhiên, tổng 249 bước còn **62,35**, thấp hơn
greedy. Oracle ngược (câu SPICE thấp nhất) chỉ **47,79**. Vậy mức tăng là do SPICE chọn đúng câu,
không phải do hiệu ứng chọn bước.

### 4.2 SPICE có thứ bậc trong cùng bước

exec theo hạng SPICE trong mỗi bước (1 = cao nhất):
**68,7 · 62,2 · 58,6 · 59,4 · 53,8 · 56,2 · 53,8 · 51,4 · 45,0**.

Trong 1.882 cặp câu cùng bước mà một câu trúng một câu trượt: câu trúng có SPICE cao hơn ở
**51,6%**, bằng ở **33,8%**, thấp hơn ở 14,6% (hiệu trung vị +0,098).
⇒ Một phần ba số cặp không phân biệt được bằng SPICE. Ở GRPO, nhóm có mọi câu cùng điểm cho
advantage bằng 0 và không sinh gradient.

### 4.3 Oracle theo các metric câu khác

Cùng cách chọn (argmax trong 9 câu, hoà lấy greedy), cùng 249 bước:

| metric | exec | Δ so greedy | KTC95 | số bước đổi câu |
|---|---:|---:|---|---:|
| SPICE | 68,67 | +5,22 | [+1,22; +9,36] | 119 |
| BLEU-4 | 71,08 | +7,63 | [+3,12; +12,24] | 136 |
| ROUGE-L | 72,29 | +8,84 | [+4,26; +13,55] | 128 |
| **CIDEr-D** | **73,09** | **+9,64** | [+5,00; +14,29] | 138 |

CIDEr-D từng câu dùng IDF tính trên 400 câu chuẩn của C1.
⚠️ Bảng này có **sau khi** đã thấy kết quả SPICE. Đổi phần thưởng sang CIDEr-D được phép theo chỉ
đạo 14/9, nhưng phải ghi rõ là lựa chọn hậu kiểm.

## 5. Giới hạn [suy]

- **Oracle không phải policy.** +5,22 là trần best-of-9 có nhìn câu chuẩn. RL thường chỉ thu được
  một phần mức này. Tiền lệ trong dự án không lạc quan: GRPO `<point>` tăng khai báo +2,56 nhưng
  `exec` chỉ +0,02 (`report/144`). Nếu thu được 30–50% thì còn khoảng +1,5…+2,5, ngang MDE 2,11.
- **Mẫu ở nhiệt độ 1,0 kém greedy 7,7 điểm** ⇒ sau train phải chấm bằng greedy.
- 249 bước, 164 episode: KTC rộng (~8 điểm).
- Val đã thấy lúc train; val từng phóng đại khoảng cách giữa hai nhánh gần 40 lần (`report/153`).

## 6. Việc kế

Quyết phần thưởng cho GRPO: SPICE (đúng luật đã chốt) hay CIDEr-D (oracle mạnh hơn, ít hoà hơn,
nhưng chọn hậu kiểm). Trước lượt GPU, chạy thủ tục chọn máy (`harness/chon_may.md`).
