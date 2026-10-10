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

(Đã làm bước 1 ngày 10/10 — kết quả ở §4; bước 2 đang chạy — §4.4.)

1. Notebook G rút gọn: chỉ sinh `ra_k4` trên test (bỏ `ra_rong`, `cont` vì cả hai đã không đạt ở val), ~3,6 h, rồi chấm `ra_k4` và `ghep` 7 thước trên WSL.
2. Nếu muốn thử thêm theo bảng §7.1 action: cả hai nhánh thấp hơn ck500 ở 4/5 thước ⇒ hạ LR xuống `1e-5` chạy lại notebook T (~8,5 h). Ưu tiên sau bước 1 vì bước 1 rẻ hơn và trả lời luôn câu hỏi luật ghép có đứng trên test không.

## 4. Kết quả test (10/10) — số test, chấm một lần

### 4.1 Sinh câu (notebook G, uyenle) [đo]

`ra_k4` sinh đủ 4.463 câu click test, 0 rỗng, T4×2, 2,16 h cả notebook. Tệp `runs/ra304_G/pred_ra_k4_test.jsonl`.
`ghep` dựng trên CPU bằng `_scripts/304/kiem/ghep_test_304.py` (luật §3.3, không đổi gì sau khi thấy val):
→ `runs/ra304_G/pred_ghep_test.jsonl`. So từng byte với câu ck500: `ra_k4` khác ở 2.229 bước, `ghep` khác ở 453 bước
(nằm trọn trong 2.229).
`ra_k4` chép nguyên văn một ví dụ ở 19,1% bước, 43,5% số câu chép đúng câu chuẩn (val: 21,0% / 41,0%).
Câu rỗng duy nhất là bước (18710, 1), vốn rỗng sẵn ở ck500.

### 4.2 Bảy thước chữ (4.463 bước click) [đo]

Chấm hai lần độc lập trên Kaggle — notebook GPU `ra-score-test-304` và notebook CPU `ra-cham-cpu-304` — ra trùng tuyệt đối
(`runs/ra304_G/cham_test/diem_test_304.json`, `cham_cpu/diem_test_304_cpu.json`). Tự kiểm: ck500 khớp số đã công bố (lệch ≤ 0,02).
Công cụ: pycocoevalcap (BLEU-4, METEOR, ROUGE-L, CIDEr-D, SPICE) · sacrebleu chrF · BERTScore roberta-large rescaled (câu rỗng = 0).

| thước | ck500 | `ra_k4` | `ghep` |
|---|---:|---:|---:|
| BLEU-4 | 52,36 | 53,47 (+1,11) | 53,47 (+1,11) |
| METEOR | 37,91 | 37,79 (−0,12) | 38,33 (+0,42) |
| ROUGE-L | 68,34 | 68,67 (+0,33) | 68,97 (+0,63) |
| CIDEr-D | 430,04 | 437,54 (+7,50) | 441,53 (+11,49) |
| SPICE | 45,79 | 46,79 (+1,00) | 47,12 (+1,33) |
| chrF | 62,86 | 62,65 (−0,21) | 63,39 (+0,53) |
| BERTScore | 67,07 | 67,52 (+0,45) | 67,66 (+0,59) |

- `ra_k4` cao hơn ck500 ở **5/7** thước ⇒ ĐẠT tiêu chí chính của action (≥ 4/7). Trên val nó chỉ đạt 1/5 —
  test và val không cùng chiều ở BLEU-4/ROUGE-L.
- `ghep` cao hơn ck500 ở **7/7** thước. Luật ghép đặt ra sau khi thấy val nhưng chưa nhìn test ⇒ test là lần xác nhận đầu.
- Chưa có KTC cho thước chữ (BLEU-4/CIDEr-D/SPICE là thước mức tập hợp).

### 4.3 Thước hành vi — exec · D.3 · AitW (UGround) [đo]

Notebook `uyenle0712/ra-exec-test-304` (T4×2, 85 phút): chỉ chấm UGround các bước có câu **khác** ck500
(453 của `ghep` + 1.776 còn lại của `ra_k4`), bước còn lại lấy nguyên dòng của `runs/grpo_spice/score_ck500_test_raw.jsonl`
— cùng cách đã làm với TAGE test. Đọc bằng `_scripts/304/kiem/doc_exec_304.py` (KTC cụm theo app, McNemar ghép cặp).
Tệp: `runs/ra304_G/exec_out/exec_out/` (tệp thô từng phần, tệp gộp `score_{ra_k4,ghep}_gop_raw.jsonl`, `doc_exec_304.json`).

Tự kiểm đạt cả ba: 40 câu ck500 không đổi (chọn ngẫu nhiên, seed 20261010) chấm lại cho toạ độ và exec **trùng 40/40** với tệp
thô cũ · câu trong tệp thô trùng tệp pred · ck500 tái lập exec 60,65.

| nhánh | exec | D.3 | AitW |
|---|---|---|---|
| ck500 | 60,65 [58,90; 62,38] | 67,02 [65,28; 68,70] | 76,25 [74,73; 77,70] |
| `ghep` | 60,54 [58,79; 62,26] | 67,00 [65,31; 68,67] | 76,11 [74,62; 77,57] |
| `ra_k4` | 59,40 [57,65; 61,14] | 65,81 [64,09; 67,48] | 75,02 [73,52; 76,45] |
| S1/101 | 59,11 [57,33; 60,83] | 65,49 [63,76; 67,18] | 74,37 [72,83; 75,83] |

| phép so | exec | D.3 | AitW |
|---|---|---|---|
| `ghep` − ck500 | −0,11 [−0,44; +0,22] · cứu 24 phá 29 · p=0,58 | −0,02 [−0,35; +0,32] · p=1 | −0,13 [−0,45; +0,19] · p=0,49 |
| `ra_k4` − ck500 | **−1,25 [−2,06; −0,44]** · cứu 124 phá 180 · p=0,002 | **−1,21 [−2,00; −0,40]** · p=0,003 | **−1,23 [−2,00; −0,44]** · p=0,002 |
| `ghep` − S1/101 | **+1,43 [+0,72; +2,15]** · cứu 155 phá 91 · p=6e−5 | **+1,50 [+0,78; +2,24]** · p=4e−5 | **+1,75 [+1,07; +2,46]** · p=1e−6 |
| `ra_k4` − S1/101 | +0,29 [−0,45; +1,04] · p=0,47 | +0,31 [−0,42; +1,03] · p=0,44 | +0,65 [−0,07; +1,38] · p=0,09 |

Đọc:
- **`ra_k4` làm giảm định vị có ý nghĩa** dưới cả ba luật (KTC nằm hẳn dưới 0): thước chữ lên nhưng UGround trỏ trúng kém hơn ck500,
  gần như mất toàn bộ phần ck500 hơn S1.
- **`ghep` không đổi thước hành vi** so ck500 (|Δ| ≤ 0,13, KTC hẹp quanh 0): chép câu mẫu làm câu giống câu chuẩn hơn về chữ
  nhưng không giúp bộ trỏ tìm đúng phần tử hơn. `ghep` vẫn hơn S1/101 có ý nghĩa dưới cả ba luật, ngang mức ck500 − S1.
- [suy] Phần lợi của RA-SFT nằm ở bề mặt câu (trùng n-gram với câu chuẩn), không ở thông tin nhận diện phần tử —
  khớp mẫu hình của các lượt train thêm sau ck500.

### 4.4 Tóm tắt và việc đang chạy

- Nếu báo một nhánh: **`ghep`** — 7/7 thước chữ cao hơn ck500, thước hành vi ngang ck500 (không hại), hơn S1/101 có ý nghĩa.
  Phải khai: luật ghép đặt sau khi thấy val, và exec/D.3/AitW **không tăng** so với ck500.
- `ra_k4` đứng một mình: ĐẠT 5/7 thước chữ nhưng **giảm exec −1,25** có ý nghĩa ⇒ không dùng làm mô hình tiêu đề.
- (cập nhật: luật ghép mới R3 ở §5 thay `ghep`; LR 1e-5 xong, KHÔNG đạt — §5.4.)
- ▶️ Đã chạy (10/10, từ 07:23): notebook T với LR `1e-5` (bước 2 của §3.4), tài khoản trang,
  `https://www.kaggle.com/code/trangphngngc/ra-sft-t-lr1e5-304`; chỉ đổi LR và tên zip (`ket_qua_304_T_lr1e5.zip`), tự cắt ở 11 h.
  Kỳ vọng [suy]: có thể cải thiện thước chữ, khó kéo exec lên.
- ✅ **Kết quả LR `1e-5` (10/10):** train và val chạy xong; notebook báo ERROR chỉ vì ô đóng gói.
  `shutil.make_archive(f"{W}/ket_qua…", "zip", W, ".")` ghi tệp zip vào chính thư mục đang nén, nên zip tự nén lại
  chính nó tới khi đầy đĩa 20 GB (lượt 2e-5 thoát được vì zip lọt vào danh sách lúc còn 1,6 KB).
  Output tải về (`runs/ra304_T_lr1e5/`) chỉ còn `cont_sft/`, `diem_val_304.json/.log` và một zip 0 byte;
  `ra_sft/`, log train, pred val bị mất. Val 1.002 click (số val, cấm trích), so ck500:

  | thước | ck500 | ra_k4 1e-5 (2e-5) | cont 1e-5 (2e-5) |
  |---|---:|---:|---:|
  | BLEU-4 | 54,81 | 54,20 (53,95) | 54,71 (54,35) |
  | METEOR | 39,25 | 38,69 (38,47) | 38,94 (38,72) |
  | ROUGE-L | 70,52 | 70,16 (69,79) | 70,40 (70,12) |
  | CIDEr-D | 448,95 | 461,47 (459,31) | 459,26 (453,59) |
  | chrF | 64,50 | 63,50 (63,23) | 64,04 (63,80) |

  Hạ LR làm cả hai nhánh nhích lên ở mọi thước nhưng vẫn chỉ hơn ck500 ở CIDEr-D (1/5) ⇒ **không đạt**, không chạy
  notebook G cho LR `1e-5`. Sửa cho lần sau: ghi zip ra `/tmp` rồi chuyển vào `W`, hoặc dùng `zip -r … -x '*.zip'`.

## 5. Sửa luật ghép: chọn trên val, áp lên test một lần (10/10)

Lý do: `ghep` (R0) tăng 7/7 thước chữ nhưng exec test −0,11 so ck500. Có sẵn tệp thô UGround cho cả câu ck500 lẫn câu `ra_k4`
trên test nên thử luật trên test là 0 GPU — chính vì thế **không** chọn luật trên test. Thủ tục:
1. Viết các luật và tiêu chí chọn (`_scripts/304/kiem/luat_ghep_304.py`) **trước** khi có exec val của `ra_k4`.
2. Chấm UGround câu `ra_k4` trên val lớn (Kaggle `uyenle0712/ra-val-luat-304`; 366 câu mới, còn lại chép từ tệp thô 289).
3. Chọn luật trên val (`_scripts/304/kiem/doc_luat_304.py val` → `runs/ra304_luat/luat_chon.json`, không cho chọn lại).
4. Áp luật đã chọn lên test đúng một lần (`doc_luat_304.py test` → `runs/ra304_luat/test_R3.json`, không cho chạy lại).

### 5.1 Luật ứng viên (chỉ dùng chữ — không bộ trỏ, không câu chuẩn)

Lấy câu `ra_k4` khi…, còn lại giữ câu ck500:

| luật | điều kiện | val: câu đổi | test: câu đổi |
|---|---|---:|---:|
| R0 | câu trùng (sau tách từ) một ví dụ của khối — `ghep` cũ | 118 | 453 |
| R1 | R0 ∧ câu đó ở ≥ 2/4 ví dụ — **loại**: khối đã khử trùng, lấy 0 bước | 0 | 0 |
| R2 | R0 ∧ phần lõi (bỏ động từ, hư từ, chữ vị trí/kiểu nút) giao câu ck500 với Jaccard ≥ 0,5 | 84 | 311 |
| R3 | R0 ∧ lớp động từ đầu câu (chạm · nhấn giữ · gõ · cuộn · mở · quay lại) trùng câu ck500 | 106 | 402 |
| R4 | R2 ∧ R3 | 80 | 299 |

Tiêu chí (khoá trước): trong các luật hơn ck500 ở ≥ 4/5 thước chữ val, chọn exec val cao nhất; hoà thì đổi ít câu hơn.

### 5.2 Val lớn (1.002 click) [đo] — số val, chỉ để chọn, cấm trích

Hiệu chuẩn: 20 câu ck500 chấm lại trùng tệp thô 289, lệch 0 (lần đầu notebook quên `--n 20` cho tệp hiệu chuẩn, chạy lại riêng phần đó).

| luật | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | chrF | exec | Δexec so ck500 | cứu / phá |
|---|---:|---:|---:|---:|---:|---:|---|---|
| ck500 | 54,81 | 39,25 | 70,52 | 448,95 | 64,50 | 63,37 | | |
| R0 | 55,39 | 39,47 | 70,97 | 462,90 | 64,59 | 63,07 | −0,30 [−1,18; +0,51] | 9 / 12 |
| R2 | 55,49 | 39,63 | 71,22 | 460,94 | 64,95 | 63,47 | +0,10 [−0,31; +0,52] | 3 / 2 |
| **R3** | 55,38 | 39,55 | 71,17 | 461,98 | 64,72 | **63,57** | +0,20 [−0,49; +0,88] | 9 / 7 |
| R4 | 55,19 | 39,49 | 71,10 | 458,90 | 64,76 | 63,47 | +0,10 [−0,31; +0,52] | 3 / 2 |

Cả bốn đủ 5/5 thước chữ ⇒ chọn theo exec ⇒ **R3**.

### 5.3 R3 trên test (4.463 click) [đo]

Bảy thước chữ — Kaggle CPU `uyenle0712/ra-cham-r3-304`, tự kiểm ck500 KHỚP (`runs/ra304_luat/cham_r3/diem_test_R3.json`):

| thước | ck500 | R0 `ghep` | **R3** |
|---|---:|---:|---:|
| BLEU-4 | 52,36 | 53,47 | **53,47 (+1,11)** |
| METEOR | 37,91 | 38,33 | **38,37 (+0,46)** |
| ROUGE-L | 68,34 | 68,97 | **69,08 (+0,74)** |
| CIDEr-D | 430,04 | 441,53 | **442,02 (+11,98)** |
| SPICE | 45,79 | 47,12 | **47,13 (+1,34)** |
| chrF | 62,86 | 63,39 | **63,44 (+0,58)** |
| BERTScore | 67,07 | 67,66 | **67,73 (+0,66)** |

R3 cao hơn ck500 ở **7/7** thước, và ≥ R0 ở cả 7. Chép nguyên văn 19,1% bước, 44,4% số câu chép đúng câu chuẩn. Câu rỗng 1 (bước 18710/1, rỗng sẵn ở ck500).

Thước hành vi (UGround, từ tệp thô có sẵn, 0 GPU — `runs/ra304_luat/test_R3.json`, `score_R3_test_raw.jsonl`):

| nhánh | exec | D.3 | AitW |
|---|---|---|---|
| ck500 | 60,65 [58,90; 62,38] | 67,02 [65,28; 68,70] | 76,25 [74,73; 77,70] |
| **R3** | **60,68 [58,93; 62,40]** | **67,11 [65,39; 68,79]** | **76,32 [74,81; 77,77]** |
| R0 `ghep` | 60,54 | 67,00 | 76,11 |
| S1/101 | 59,11 | 65,49 | 74,37 |

| phép so | exec | D.3 | AitW |
|---|---|---|---|
| R3 − ck500 | +0,02 [−0,21; +0,26] · cứu 15 phá 14 · p=1 | +0,09 [−0,15; +0,33] · p=0,58 | +0,07 [−0,15; +0,29] · p=0,69 |
| R3 − S1/101 | **+1,57 [+0,86; +2,31]** · cứu 158 phá 88 · p=1e−5 | **+1,61 [+0,88; +2,35]** · p=8e−6 | **+1,95 [+1,27; +2,66]** · p=6e−8 |
| R3 − R0 | +0,13 [−0,09; +0,36] · p=0,31 | +0,11 · p=0,44 | +0,20 [−0,02; +0,44] · p=0,12 |

Đọc:
- **R3 là nhánh tốt nhất của 304:** 7/7 thước chữ hơn ck500, ba thước hành vi nhỉnh hơn ck500 (KTC phủ 0 ⇒ viết "ngang ck500, không hại"),
  hơn S1/101 có ý nghĩa ở cả ba luật (nhỉnh hơn ck500 − S1 = +1,55).
- Điều kiện "cùng loại thao tác" chặn kiểu lỗi chép câu của bước khác loại (bước chạm mà câu chép bảo gõ/mở app) — đúng chỗ R0 mất exec.
- Phải khai: R0 đặt sau khi thấy val; R3 chọn trên val trong 4 ứng viên (khoá trước exec val), áp test một lần; một hạt giống;
  các thước chữ chưa có KTC.

### 5.4 Notebook T, LR 1e-5 (tài khoản trang) [đo] — KHÔNG ĐẠT

`trangphngngc/ra-sft-t-lr1e5-304`: train + val xong; Kaggle báo ERROR ở khâu đóng zip cuối [suy, không tải được log đầy đủ — tệp zip lớn].
Điểm val (`runs/ra304_T_lr1e5/diem_val_304.log`):

| thước | ck500 | `ra_k4` | `cont` |
|---|---:|---:|---:|
| BLEU-4 | 54,81 | 54,20 (−0,61) | 54,71 (−0,10) |
| METEOR | 39,25 | 38,69 (−0,56) | 38,94 (−0,31) |
| ROUGE-L | 70,52 | 70,16 (−0,36) | 70,40 (−0,12) |
| CIDEr-D | 448,95 | 461,47 (+12,52) | 459,26 (+10,31) |
| chrF | 64,50 | 63,50 (−1,00) | 64,04 (−0,46) |

Cả hai nhánh 1/5 (chỉ CIDEr-D), cùng mẫu hình LR 2e-5, chỉ nhẹ hơn. Đề xuất dừng hướng train thêm; mô hình báo cáo của 304 là
**ck500 + luật R3** (không cần train mới). Adapter `cont_sft` LR 1e-5 (344 MB) chỉ nằm trên máy, không vào git.
