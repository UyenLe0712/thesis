# 304 — Đánh giá RA-SFT trước GPU + trạng thái lượt chạy (9/10/2026)

Action: `304_ACTION_RA_SFT_TU_CK500_VA_KHO_RONG_9_10_double_checked.md` (gốc kho).
Script chép từ Phụ lục A ra `_scripts/304/ra-sft-script/` (md5 `ra_*.py` khác bản Mac vì chép lại từ
markdown; `grpo_spice.py`, `build_branch_data.py`, `train_tru_val.jsonl`, hai tệp pred ck500 trùng md5 của action).

## 1. Đo CPU trên test (0 GPU, không mô hình) — `_scripts/304/kiem/`

Kho 62.880 bước / 12.542 tác vụ (bỏ 346 tác vụ val) · tác vụ test chung kho 0 — trùng action.
Khối k = 4 cố định trên 4.463 bước click test:

| đại lượng | số bước | % |
|---|---:|---:|
| khối chứa nguyên văn câu chuẩn | 707 | 15,8 |
| ví dụ số 1 là câu chuẩn | 419 | 9,4 |
| ck500 đã viết đúng nguyên văn câu chuẩn | 1.003 | 22,5 |
| khối chứa câu chuẩn **và** ck500 đã đúng | 269 | 6,0 |
| khối chứa câu chuẩn **và** ck500 sai (chỗ có thể lời) | 438 | 9,8 |

Val lớn: khối chứa đích 13,1% (action ghi 13,3%; bản `p1_val_rows` của bundle khác md5 tệp val 289 nhưng cùng 346 tác vụ).

Thước chữ khi thay câu ck500 bằng câu mẫu (BLEU-4 · ROUGE-L · CIDEr-D · chrF, pycocoevalcap):

| cách | BLEU-4 | ROUGE-L | CIDEr-D | chrF |
|---|---:|---:|---:|---:|
| ck500 | 52,36 | 68,34 | 430,0 | 62,86 |
| cận trên: chép đúng khi khối chứa câu chuẩn (oracle) | 57,41 | 71,87 | 495,4 | 66,42 |
| luôn chép ví dụ 1 | 28,25 | 46,80 | 178,8 | 40,56 |
| chép ví dụ 1 khi nó xuất hiện ≥ 3 lần trong hai khoá | 48,56 | 64,04 | 380,5 | 58,42 |

Đọc:
- Có chỗ để lên: nếu mô hình biết chép đúng lúc, trần là +5 BLEU, +65 CIDEr-D. Lớn hơn RAF (+0,7 / +5,6).
- Chép mù thì sập; luật đồng thuận đơn giản (không nhìn ảnh) cũng thua ck500. Toàn bộ lợi phụ thuộc
  vào việc mô hình học được *khi nào* câu mẫu khớp màn — mà điểm nghẽn đã đo của dự án là tri giác (§`sec:haikenh`).
- Rủi ro riêng của thiết kế: `p1_train_rows` là dữ liệu S1 đã học, nên mô hình đã thuộc câu đích
  kể cả khi không có khối ⇒ tín hiệu "dùng khối" yếu (~3.400 hàng có khối, ~650 hàng khối chứa đích).
- Rủi ro chung: mọi lượt train thêm sau ck500 đã thử (tspicea, A2, CTG) đều làm thước chữ giảm; nhánh `cont` đo đúng rủi ro này.
- Ước lượng chủ quan đạt ≥ 4/7 thước chữ: ~40–50% (thấp hơn 55–65% của action, vì hai rủi ro trên). [suy]

## 2. Lượt chạy

Notebook T (train `ra` + `cont`, chạy thử 2 bước rồi train thật, rồi val 1.002 click 5 thước), một commit:
`https://www.kaggle.com/code/trangphngngc/ra-sft-t-304`, tài khoản trang (11,55 h hạn mức lúc đẩy, 09:5x 9/10 giờ VN).
Dataset `trangphngngc/ra-sft-script` (12 tệp, md5 ở `scratchpad/k304/md5.json`, bảng §1 file này).
Khác runbook: Ô 1 ghim `transformers 5.18.0 · peft 0.21.1` + gỡ torchao (bẫy 6/10); notebook tự giới hạn ≤ 11 h
(không vượt hạn mức trang); ô cuối đóng `ket_qua_304_T.zip`.
Notebook G (sinh test 3 cấu hình + 7 thước) chưa chạy — xem §3.4.

## 3. Kết quả notebook T (9/10, xong ~21:00 giờ VN)

Tệp ở `runs/ra304_T/` (log, câu sinh val, điểm). Adapter `ra_sft/final`, `cont_sft/final` (344 MB mỗi nhánh)
và `ket_qua_304_T.zip` chỉ nằm trên máy, không vào git.

### 3.1 Train [đo]

| nhánh | bước | thời gian | s/bước | VRAM | loss bước 5 → 125 → 250 |
|---|---:|---:|---:|---:|---|
| `ra` (có khối ví dụ) | 250 | 450 phút | 108 | 7,3 GiB | 0,78 → 0,45 → 0,42 |
| `cont` (không khối) | 250 | 402 phút | 96,5 | 6,8 GiB | 0,54 → 0,46 → 0,45 |

Loss của `ra` khởi đầu cao hơn vì ck500 chưa từng gặp câu nhắc có khối, rồi xuống dưới `cont` từ giữa lượt.
Train thật mất ~7,5 h, gấp rưỡi mức 4–6 h action ghi. Sinh val 1.002 câu: 49 phút (`ra_k4`), 44 phút (`cont`).
Dữ liệu train 3.991 hàng, 85,2% có khối, 12,9% khối chứa đúng câu đích.

### 3.2 Val lớn (1.002 bước click, 5 thước, không SPICE/BERTScore) [đo]

Chấm lại trên WSL bằng chính `ra_score.py` (val rows md5 `91b599f1…`) ra trùng tuyệt đối số của Kaggle.

| thước | ck500 | `ra_k4` | `cont` | `ghep` (§3.3) |
|---|---:|---:|---:|---:|
| BLEU-4 | 54,81 | 53,95 (−0,86) | 54,35 (−0,46) | 55,39 (+0,58) |
| METEOR | 39,25 | 38,47 (−0,78) | 38,72 (−0,53) | 39,47 (+0,22) |
| ROUGE-L | 70,52 | 69,79 (−0,73) | 70,12 (−0,40) | 70,97 (+0,45) |
| CIDEr-D | 448,95 | 459,31 (+10,36) | 453,59 (+4,64) | 462,90 (+13,95) |
| chrF | 64,50 | 63,23 (−1,27) | 63,80 (−0,70) | 64,59 (+0,09) |
| câu trùng nguyên văn câu chuẩn | 23,1% | 26,6% | 24,6% | 25,1% |
| câu khác ck500 | 0 | 46,1% | 27,0% | 10,3% |

Đọc theo §7 của action:
- **Chính: `ra_k4` CHƯA ĐẠT** — cao hơn ck500 ở 1/5 thước (chỉ CIDEr-D). `cont` cũng 1/5.
- **Quy công:** `ra_k4` hơn `cont` chỉ ở CIDEr-D (+5,7), thua ở bốn thước còn lại ⇒ theo luật action không quy được lợi cho truy hồi.
- **Chẩn đoán chép:** `ra_k4` chép nguyên văn một ví dụ ở 21,0% bước, 41,0% trong số đó đúng câu chuẩn ⇒ không phải chép mù (ngưỡng chép mù của action là > 40% chép với < 15% đúng).
- Mẫu hình: SFT thêm (cả hai nhánh) làm nhích số câu trùng nguyên văn (CIDEr-D lên) nhưng làm các câu còn lại kém đi (BLEU/METEOR/ROUGE-L/chrF xuống) — lặp lại mẫu hình của mọi lượt train thêm sau ck500.

### 3.3 Luật ghép chọn-khi-chép (0 GPU, chọn SAU khi thấy val) [đo]

`_scripts/304/kiem/ghep_chep_304.py`: lấy câu của `ra_k4` **chỉ khi** câu đó trùng (sau tách từ) một trong 4 ví dụ của khối;
còn lại giữ câu ck500. 208/1.002 bước (20,8%) lấy câu RA. Kết quả: **cao hơn ck500 ở 5/5 thước val**, CIDEr-D +13,95.

Diễn giải [suy]: phần có ích của RA-SFT nằm gọn ở các bước mô hình quyết định chép một câu mẫu (độ đúng 41% so với 23% chung);
phần hại nằm ở các bước mô hình viết câu mới — ở đó lượt SFT thêm làm câu kém ck500. Luật ghép giữ phần lợi, bỏ phần hại.

⚠️ Luật này đặt ra **sau** khi thấy số val, một biến thể duy nhất, chưa có KTC (action không đòi), và val lớn có tác vụ
mà ck500 không thấy nhưng S1 đã thấy. ⇒ Chỉ coi là ứng viên, phải xác nhận trên test. Trên test luật cần câu `ra_k4` cho
4.463 bước (notebook G, chỉ nhánh `ra_k4`, ~3,6 h T4 theo 2,93 s/bước đo ở val) rồi ghép với `pred_ck500_test.jsonl` và chấm đủ 7 thước trên CPU.

### 3.4 Việc kế (đề xuất)

1. Notebook G rút gọn: chỉ sinh `ra_k4` trên test (bỏ `ra_rong`, `cont` vì cả hai đã không đạt ở val), ~3,6 h, rồi chấm `ra_k4` và `ghep` 7 thước trên WSL.
2. Nếu muốn thử thêm theo bảng §7.1 action: cả hai nhánh thấp hơn ck500 ở 4/5 thước ⇒ hạ LR xuống `1e-5` chạy lại notebook T (~8,5 h). Ưu tiên sau bước 1 vì bước 1 rẻ hơn và trả lời luôn câu hỏi luật ghép có đứng trên test không.
