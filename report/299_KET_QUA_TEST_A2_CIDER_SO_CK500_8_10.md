# 299 — Kết quả test: GRPO thưởng CIDEr-D (A2) so với ck500 (8/10/2026)

Action gốc: `harness/tai_lieu_2026-10-07/299_ACTION_CHAM_TEST_A2_CIDER_SO_CK500_7_10.md`.
Số dưới đây là **số test** (4.463 bước chạm), trích được.

## 1. Kết luận

**Hàng S theo luật §4 ⇒ giữ ck500.** Phép so chính `A2_500 − ck500` executability
**−0,69 [−1,34; −0,02]**, p McNemar 0,04 (cứu 91 / phá 122). Cận trên KTC dưới 0: ở cùng
500 bước, thưởng SPICE cho exec cao hơn thưởng CIDEr-D.

`A2_1000` (chỉ đọc thêm, không đổi hàng): −0,67 [−1,33; +0,00], p 0,057.
Cả hai A2 vẫn hơn S1/101 khoảng +0,85 (KTC sát 0, cận dưới +0,02).

⚠️ Một hạt giống mỗi nhánh. Δ −0,69 nhỏ hơn mức chênh giữa hai hạt S1 (0,52) không nhiều,
nên luận văn nên ghi kèm điều này. Hai nhánh còn khác tập câu nhắc (1.000 so với 2.000 câu)
và máy train (T4 fp16 so với A100 bf16), xem §2 của action.

## 2. Thước vị trí (4.463 bước chạm)

| thước | S1/101 | ck500 | A2_500 | A2_1000 |
|---|---:|---:|---:|---:|
| Executability | 59,11 | 60,65 | 59,96 | 59,98 |
| Hộp phần tử (D.3) | 65,49 | 67,02 | 66,44 | 66,35 |
| AitW | 74,37 | 76,25 | 76,52 | 76,07 |
| AitW cận trên | 81,04 | 82,90 | 83,22 | 83,35 |
| ±14% theo trục | 67,24 | 68,90 | 68,83 | 68,70 |
| Đúng loại thao tác | 94,35 | 95,97 | 96,21 | 96,24 |
| số từ TB | 7,83 | 7,96 | 7,61 | 7,73 |
| câu trùng ck500 | 2.795 | 4.463 | 2.943 | 2.455 |

So ghép cặp với ck500 (KTC95 bootstrap cụm theo app, B = 10.000):

| thước | A2_500 − ck500 | A2_1000 − ck500 |
|---|---|---|
| Executability | **−0,69 [−1,34; −0,02]** p 0,04 | −0,67 [−1,33; +0,00] p 0,057 |
| D.3 | −0,58 [−1,26; +0,09] | −0,67 [−1,37; +0,04] |
| AitW | +0,27 [−0,40; +0,96] | −0,18 [−0,83; +0,50] |
| AitW cận trên | +0,31 [−0,31; +0,96] | +0,45 [−0,13; +1,04] |
| ±14% theo trục | −0,07 [−0,74; +0,61] | −0,20 [−0,91; +0,53] |
| Đúng loại thao tác | +0,25 [−0,02; +0,53] | +0,27 [−0,02; +0,57] |

`A2_1000 − A2_500`: exec +0,02 [−0,55; +0,59] ⇒ train thêm 500 bước không đổi gì.

**Phân rã** (A2_500 − ck500): cứu 91 (ck500 sai loại thao tác 15) · phá 122 (A2_500 sai
loại thao tác 5) ⇒ ròng từ loại thao tác **+10**, ròng từ đổi phần tử **−41**. A2_1000 gần
như y hệt (+10 / −40). Tức A2 viết đúng loại thao tác hơn một chút, nhưng chọn sai phần tử
nhiều hơn; chỉ dưới exec và D.3 (đòi đúng phần tử) mới thấy thua, dưới AitW thì hoà.

## 3. Thước chữ (chỉ mô tả, không đổi hàng)

| thước | S1/101 | ck500 | A2_500 | A2_1000 | A2_500 − ck500 | A2_1000 − ck500 |
|---|---:|---:|---:|---:|---:|---:|
| BLEU-4 | 51,56 | 52,36 | 52,38 | 52,82 | +0,02 | +0,46 |
| METEOR | 36,79 | 37,92 | 37,24 | 37,37 | −0,68 | −0,55 |
| ROUGE-L | 67,35 | 68,36 | 68,59 | 68,46 | +0,23 | +0,10 |
| CIDEr-D | 416,12 | 430,05 | 428,27 | 427,98 | −1,78 | −2,07 |
| SPICE | 44,37 | 45,79 | 45,27 | 44,45 | −0,52 | −1,34 |
| chrF | 61,26 | 62,87 | 61,76 | 61,92 | −1,11 | −0,95 |

ΔSPICE có KTC: A2_500 − ck500 −0,53 [−1,24; +0,19] · A2_1000 − ck500 **−1,34 [−2,11; −0,58]** ·
A2_500 − S1 +0,90 [+0,03; +1,79].

⚠️ Ngược với dự đoán ở §4 action ("A2 gần như chắc chắn cao hơn ở CIDEr-D"): **A2 được thưởng
CIDEr-D mà CIDEr-D test vẫn thấp hơn ck500** (−1,78 / −2,07, chưa có KTC). Chỉ ghi nhận, chưa
truy nguyên nhân.

## 4. Kiểm lượt chạy

- Kaggle `uyenle0712/a2-test-299`, T4 ×2, 8,66 h, không chạm mốc tự dừng 11,2 h.
- `[kiểm ck500] 20/20 câu trùng lượt 2/10` ⇒ đường sinh tái lập ck500.
- Mỗi nhánh 4.463/4.463 câu (rỗng 1, cùng bước như mọi nhánh), chấm 4.463/4.463, thiếu OCR 0,
  thiếu ảnh 0. md5 điểm lưu: A2_500 `daa3b5f6…`, A2_1000 `d45058d5…`.
- Tự kiểm của `doc_299.py` đạt: S1 và ck500 tái lập exec, KTC và sáu thước chữ đã công bố.
- Khác runbook một chỗ: Ô 1 ghim `trl 0.29.1 · transformers 5.18.0 · peft 0.21.1` và gỡ
  `torchao` (image Kaggle mới làm hỏng peft), cùng phiên bản lượt ck500. Phép kiểm 20/20 cho
  thấy không đổi đường sinh.

## 5. Câu cho luận văn (§7 action, hàng S — chưa dán vào `ch6`)

> Ở cùng $500$ bước cập nhật, nhánh thưởng CIDEr-D đạt executability $59{,}96$, chênh $-0{,}69$
> điểm so với nhánh thưởng SPICE, khoảng tin cậy $[-1{,}34; -0{,}02]$. Khoảng tin cậy nằm hẳn
> dưới $0$, tức trong hai phần thưởng có tiền lệ, SPICE cho câu dẫn tới đúng phần tử thường
> xuyên hơn.

## Tệp

`runs/a2_test299/` (câu, tệp chấm thô, log sinh/chấm, `doc_299.log` + `doc_299_vitri.json` thước
vị trí, `doc_299_chu.log` + `doc_299.json` có cả thước chữ) · `_scripts/299/doc_299.py`.
