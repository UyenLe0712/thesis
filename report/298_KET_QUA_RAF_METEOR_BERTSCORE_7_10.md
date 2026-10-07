# 298 — Kết quả RAF trên test: METEOR + BERTScore (7/10/2026, WSL)

Action gốc: `harness/tai_lieu_2026-10-07/298_ACTION_CHOT_RAF_7_10.md` (chép từ 6 ảnh, ảnh ở `anh/` và `anh_2/`).
Mục tiêu của action: lấy hai cột còn thiếu (METEOR, BERTScore) để biết RAF hơn ck500 ở 7/13 hay 6/13 cột.
Toàn bộ số dưới đây là **số test** (4.463 bước chạm), chạy CPU trên WSL, 0 GPU.

## 1. Kết luận

**RAF hơn ck500 ở 7/13 cột** theo luật đọc của action (METEOR Δ > 0 và BERTScore Δ > 0).

| cột | RAF | ck500 | S1/101 | Δ RAF − ck500 | KTC95 (bootstrap theo tác vụ, B = 2000) |
|---|---|---|---|---|---|
| METEOR 1.5 (mức kho) | 38,09 | 37,92 | 36,79 | **+0,17** | METEOR_KTC |
| BERTScore F1 rescaled | 67,62 | 67,07 | 66,33 | **+0,55** | [+0,29; +0,82] |
| chrF | 63,08 | 62,87 | 61,26 | +0,20 | [−0,10; +0,51] |

Tự kiểm của action ĐẠT: hàng S1 và ck500 trùng tuyệt đối số đã công bố (S1 36,79 · 66,33 · 61,26;
ck500 37,92 · 67,07 · 62,87).

Bảng 13 cột đầy đủ sau khi có hai số này (các cột khác lấy từ §3 của action, số Mac):

| cột | Δ RAF − ck500 | |
|---|---|---|
| BLEU-4 | +0,72 [+0,31; +1,12] | ✅ |
| ROUGE-L | +0,68 [+0,38; +0,98] | ✅ |
| CIDEr-D | +5,61 [+1,46; +9,61] | ✅ |
| SPICE | +0,53 [+0,03; +0,99] | ✅ |
| METEOR | +0,17 | ✅ (xem §3) |
| BERTScore | +0,55 [+0,29; +0,82] | ✅ |
| chrF | +0,20 [−0,10; +0,51] | dương, không ý nghĩa |
| 5 cột hành vi | −0,13 … −0,38 | âm nhẹ, KTC phủ 0 |
| đúng loại thao tác | 0,00 | hoà |

⇒ 7 cột dương (6 có KTC loại 0 nếu METEOR qua §3), 1 cột dương không ý nghĩa, 5 cột âm nhẹ không ý nghĩa.
BERTScore +0,55 cao hơn mức dự báo trong action (≈ +0,18).

## 2. Dựng lại câu RAF trên WSL

`raw_G4g_test.jsonl` chỉ có trên Mac, nên dựng lại bằng script 296-R chép từ ảnh
(`_scripts/296/do_296_R_test_lai.py`, CPU ~1 phút). Hai chỗ khác bản Mac: `tok`/`CiderD` lấy từ
`harness/ctg_grpo.py` vì `do_296_vallon.py` không có trên WSL (phải bọc `score` cho nhận một câu
tham chiếu như bản Mac gọi), và đường dẫn tương đối từ gốc kho.

Kiểm tái lập:
- Cổng lùi về S1 ở **724/4.463** bước, trùng `assert … <= 724` mà script 298 đặt sẵn.
  Tầng lọc: 1.445 bước câu khác token → 1.351 cùng lớp thao tác → 724 lùi.
- Ba cột §3 tính lại bằng pycocoevalcap: BLEU-4 +0,69 (Mac +0,72) · ROUGE-L +0,68 (trùng) ·
  CIDEr-D +5,54 (Mac +5,61). Còn lệch nhỏ chưa truy được; cần `cong_G4g_test.json` của Mac để so
  từng bước. Hai cột mới (METEOR, BERTScore) tính trên tệp dựng lại này.

## 3. METEOR: vì sao phải chạy bootstrap riêng

Script 298 in METEOR `+0,17 [+0,28; +1,03]`: khoảng **không chứa** chính Δ. Lý do là METEOR tổng
của pycocoevalcap do Java gộp thống kê khớp (số từ khớp, số đoạn, độ dài) của cả kho rồi mới tính
điểm, chứ không lấy trung bình điểm từng câu. Còn KTC của script 298 dựng trên trung bình điểm từng câu,
tức một đại lượng khác. BERTScore và chrF không bị lỗi này (BERTScore là trung bình câu; chrF đã
bootstrap đúng ở mức kho).

Cách đúng (`_scripts/298/meteor_bootstrap_298.py`): lấy thống kê khớp của từng câu một lần, rồi mỗi
lượt bootstrap gửi lại thống kê của mẫu lấy lại cho Java gộp. Cùng mẫu bootstrap với script 298
(theo tác vụ, `Random(0)`, B = 2000). Đã kiểm gộp toàn bộ ra đúng 38,0874 và 37,9205.

Kết quả: METEOR_KQ

## 4. Cách viết trong luận văn (theo §2 của action)

- RAF không phát minh phép chấm, phép chấm là consensus reranking của Mao et al. (ICLR 2015).
  Phần của đề tài là áp vào việc chọn giữa chính sách SFT và RL kèm cổng bảo thủ, bộ nhớ là quỹ đạo
  GUI căn theo bước, và bằng chứng xếp hạng n-best kiểu Mao hỏng trên bài này.
- Không viết: "RAF là phương pháp mới hoàn toàn", "RAF tổng quát hoá", "chrF tăng có ý nghĩa".

## Tệp

`runs/raf298/cham_raf_wsl_298.{json,log}` · `runs/raf298/meteor_bootstrap_298.{json,log}` ·
`_scripts/296/do_296_R_test_lai.py` · `_scripts/296/lai_test/{raw_G4g_test.jsonl,cong_G4g_test.json}` ·
`_scripts/298/cham_raf_wsl_298.py` · `_scripts/298/meteor_bootstrap_298.py`
