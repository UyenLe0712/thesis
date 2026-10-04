# 254 — Tình trạng GRPO thưởng SPICE cho S1/101 (30/9/2026, tối)

Tệp bàn giao, đọc một mình là hiểu. Viết cho phiên chat kế tiếp.
Nguồn gốc: action `harness/tai_lieu_2026-09-29/253_ACTION_GRPO_SPICE_S1_29_9_checked.md`.
Số trong tệp này đều là **số val C1, cấm trích ra báo**.

## 1. Đang làm gì

Nhánh ablation **"S1 + GRPO, tắt đầu khe"** của phương pháp ở `report/208` §6. Làm như sau: hoà
S1/101 vào trọng số rồi gắn LoRA mới (B = 0), nên tham chiếu KL đúng bằng S1. G = 8, 500 bước,
thưởng = SPICE − 0,02·phạt độ dài. Chạy trên Kaggle T4 (0 đồng), khoảng 146–160 s/bước, nên phải
nối nhiều commit.

- Mã: `harness/grpo_spice.py` (md5 bản đang dùng `d99d03c0c01718283e84ac3851ef5591`).
- Runbook train: `harness/runbook/kaggle_grpo_spice_commit.md`.
- Runbook chấm: `harness/runbook/kaggle_grpo_spice_pha3_ck250.md`.
- Đọc kết quả (0 GPU, WSL): `~/.venvs/thesis/bin/python harness/grpo_spice_doc.py`.
- Tệp kết quả: `runs/grpo_spice/`.

## 2. Luật đọc (§2 của 253, khoá trước khi có số)

Chấm `checkpoint-250` và `checkpoint-500`. Mỗi điểm lưu sinh greedy trên 400 bước C1:
SPICE so với S1 greedy **57,30**; `exec` trên 249 bước click so với S1 greedy **63,45**.

| kết quả | kết luận |
|---|---|
| ΔSPICE ≥ +2,0 và Δexec ≥ 0 | **ĐẠT**: viết action đầu khe, rồi chấm test một lần |
| **cả hai** điểm lưu: Δexec ≤ −3,0 hoặc ΔSPICE < +1,0 | **DỪNG** nhánh GRPO |
| còn lại | báo người dùng quyết |

Kèm hai phép kiểm lệch thưởng: số từ không tăng quá 3 so với S1, và 0 câu rỗng. Không nới ngưỡng
sau khi thấy số.

## 3. Kết quả `checkpoint-250` (xong 30/9)

Điểm lưu lấy từ **commit 1**: 250 bước liền mạch từ S1, hợp lệ.

| | S1 greedy | ck250 | Δ | KTC95 bootstrap theo episode |
|---|---|---|---|---|
| SPICE (400 bước) | 57,30 | **57,91** | **+0,61** | [−1,40; +2,66] |
| exec (249 click) | 63,45 | **64,66** | **+1,20** | [−1,17; +3,73] |

- exec: cứu 6 bước, phá 3 (McNemar p ≈ 0,5), nên chưa phân biệt được với nhiễu.
- 328/400 câu (82%) trùng từng ký tự với S1. Số từ 7,19 so với 7,28 của S1. 0 câu rỗng.
- **Phép kiểm dụng cụ đạt:** greedy S1 chấm lại trong cùng phiên (`score_k0_lai_raw.jsonl`) ra
  158/249, trùng tuyệt đối lượt 251 (cùng khoá, lệch toạ độ 0, lệch exec 0). Mốc SPICE S1 in đúng 57,30.
- Log train commit 1 (`train_c1.log`, 262 bước): thưởng trung bình theo khối 25 bước gần như phẳng,
  0,44 → 0,52. KL tăng chậm 0 → ~0,012 ở bước 201–250 (~0,018 ở 251–262). Mô hình mới dịch khỏi S1 rất ít.

**Đọc theo §2:** chưa ĐẠT (ΔSPICE +0,61 < +2,0). ck250 thoả vế DỪNG (ΔSPICE < +1,0), nhưng DỪNG
đòi **cả hai** điểm lưu, nên kết quả rơi vào ô "còn lại". Người dùng quyết **chạy tiếp 250 → 500**.

## 4. Sự cố commit 2 (đã sửa) và lượt đang chạy

Commit 2 đầu tiên chạy tiếp **sai**. Khi điểm lưu có thư mục con `ref/`, transformers chỉ nạp thư
mục con đó và bỏ adapter `default` ở gốc, nên policy âm thầm quay về S1 (KL 0,012 → 0,001). Mọi
điểm lưu 275–500 của lượt đó **không hợp lệ**. Mã đã sửa: nạp tay `default` và in dòng
`[nạp default] … |lora_B| 0.0000 → x`, dừng nếu x = 0. Chi tiết ở `harness/runbook/kaggle_grpo_spice_commit.md`
mục *SỰ CỐ 30/9*.

**Lượt chạy lại 250 → 500 đang chạy** (ảnh log người dùng gửi tối 30/9):

- 6,36 h, bước 406/500 (tiếp từ 250), lưu cuối `checkpoint-400`.
- 145–146 s/bước, còn khoảng 3,8 h. Tổng khoảng 10,2 h, dưới mốc dừng 11 h, nên **commit này
  dự kiến tự tới bước 500**.
- 20 bước gần nhất: thưởng TB 0,40–0,43 · số từ TB 6,3–6,5 · rỗng 0 · bước grad≈0 0/20 ·
  **kl TB 0,0012–0,0013**.

### ⚠️ Cờ đỏ chưa gỡ: KL quá thấp

Cuối commit 1, KL là ~0,012–0,018. Runbook ghi rõ: chạy tiếp đúng thì KL phải *xấp xỉ mức cuối lượt
trước, không về ~0*. Ở bước ~400 (150 bước sau khi nạp lại), KL chỉ **0,0012**, tức đúng mức của
lượt hỏng (~0,001). Hai khả năng:

1. **Lượt này vẫn hỏng như commit 2 cũ** (policy về S1). Có thể do dataset `grpo-spice-script` chưa
   New Version bản sửa, hoặc notebook gắn nhầm Output.
2. Lượt này đúng, nhưng policy tự co về gần S1. Khả năng này ít hơn: KL không có lý do tụt 10 lần
   trong khi lr giữ 1e-5.

Hai dấu hiệu phụ cùng chiều với khả năng 1, nhưng **không** đủ kết luận: thưởng TB (~0,40) thấp
hơn cuối commit 1 (~0,50), và số từ TB (~6,4) ngắn hơn (~8–9). Hai con số này đo trên lô câu nhắc
khác nhau nên không so thẳng được.

**Việc đầu tiên của phiên sau: kiểm cờ này, TRƯỚC khi chấm ck500.** Trong log của commit đang chạy:

- phải có dòng `[nạp default] … |lora_B| 0.0000 → x` với **x > 0**;
- md5 `grpo_spice.py` in ra phải là `d99d03c0…`;
- `kl TB` ở các dòng đầu (bước 251–270) phải ~0,01. Nếu ngay từ đầu đã ~0,001 thì là khả năng 1.

Nếu thiếu dòng `[nạp default]`, hoặc x = 0: `checkpoint-500` của lượt này **không hợp lệ**, cấm chấm
như mô hình 500 bước.

## 5. Việc kế

1. Kiểm cờ đỏ ở §4 (chỉ đọc log, 0 GPU).
2. Nếu hợp lệ: khi commit xong, tải `grpo_spice/checkpoint-500/` → dataset riêng (như
   `grpo-spice-ck250`) → chạy Pha 3 cho ck500. Chép `kaggle_grpo_spice_pha3_ck250.md`, đổi tên
   dataset, điểm lưu và tên tệp ra (`pred_ck500.jsonl`, `score_ck500_raw.jsonl`). Khoảng 1,5 h T4.
3. Tải về `runs/grpo_spice/`, chạy `grpo_spice_doc.py` (in cả ck250 lẫn ck500), rồi đọc theo bảng §2.
   ⚠️ Kaggle hay tải tệp về với đuôi `.txt`, phải đổi về `.jsonl`/`.json`/`.log` trước khi chạy.
4. Kỳ vọng thấp: để ck500 ĐẠT, ΔSPICE phải tăng từ +0,61 lên ≥ +2,0, trong khi thưởng nửa đầu phẳng.
   Nếu ck500 cũng có ΔSPICE < +1,0 thì theo luật là **DỪNG nhánh GRPO**, báo người dùng.

## 6. Tệp trong `runs/grpo_spice/`

`pred_ck250.jsonl` (400) · `score_ck250_raw.jsonl` (249) · `score_ck250.json` ·
`score_k0_lai_raw.jsonl` (249) · `score_k0_lai.json` · `gen_ck250.log` · `cham_ck250.log` ·
`cham_k0_lai.log` · `train_c1.log` (log train commit 1).

## 7. Kết quả `checkpoint-500` (1/10) — theo §2: **DỪNG**, chờ người dùng xác nhận

### 7.1 Đường đi tới ck500 và phép kiểm hợp lệ

- Lượt chạy lại 250 → 500 **OOM hai lần ở bước ~443** (điểm lưu cuối `checkpoint-425`), sửa bằng
  `--bs 2 --accum 8` rồi `--gen-chunk 8` (md5 `07ea87b6…`). Chi tiết ở `harness/runbook/kaggle_grpo_spice_commit.md`.
- Commit nối 425 → 500 (`train_c3.log`): `[tiếp từ] checkpoint-425` · `[nạp default] 504 tensor ·
  |lora_B| 0.0000 → 9.1140 · khoá lạ 0` · đủ 75 bước · 156,6 s/bước · đỉnh VRAM 12,38 GiB · không
  Traceback. kl TB 0,014–0,037 (lượt hỏng kiểu commit 2 cũ là ~0,001) ⇒ **cờ đỏ §4 đã gỡ cho đoạn này**.
- Phải khai: bước 426–500 chạy ở micro-batch 2 + sinh theo khúc (tương đương về toán, lệch số học fp16).
- Chấm trên tài khoản Kaggle thứ hai: greedy S1 chấm lại (`score_k0_lai500_raw.jsonl`) **trùng từng
  byte** với `score_k0_lai_raw.jsonl` của phiên ck250 ⇒ dụng cụ ổn định qua hai tài khoản.
- ⚠️ Thiếu: `train.log` của lượt chạy lại 250 → 443 (version OOM). Không chặn việc đọc, nên tải về
  đặt tên `train_c2b.log` để lưu vết KL đoạn đó.

### 7.2 Số (`grpo_spice_doc.py`, số val, cấm trích)

| | S1 greedy | ck250 | ck500 |
|---|---|---|---|
| SPICE (400 bước) | 57,30 | 57,91 (Δ +0,61 [−1,40; +2,66]) | **57,45 (Δ +0,15 [−2,59; +2,79])** |
| exec (249 click) | 63,45 | 64,66 (Δ +1,20 [−1,17; +3,73]) | **66,27 (Δ +2,81 [0,00; +6,02])** |
| cứu / phá | | 6 / 3 (McNemar p = 0,51) | 12 / 5 (p = 0,14) |
| câu trùng S1 | | 328/400 | 277/400 |
| số từ · rỗng | 7,28 · 0 | 7,19 · 0 | 7,37 · 0 |

**Đọc theo §2:** cả hai điểm lưu ΔSPICE < +1,0 ⇒ **DỪNG nhánh GRPO**. Hai phép kiểm lệch thưởng đạt.
Thưởng train tăng 0,44 → ~0,55–0,60 nhưng SPICE trên val không tăng ⇒ thưởng không tổng quát hoá sang val.

### 7.3 Phân rã Δexec của ck500 (+7 bước ròng)

- **5/12 bước cứu là sửa loại thao tác**: S1 viết *"Swipe up …"* ở bước click, ck500 viết *"Click on …"*
  (`action_ok` 0 → 1). Không bước phá nào do loại thao tác. `action_ok` trên 249 click: 239 → 245.
- 7 bước cứu còn lại và cả 5 bước phá là **đổi phần tử được gọi tên** (`action_ok` giữ 1) ⇒ phần định vị
  chỉ ròng **+2 bước (+0,80 pp)**.
- Cả 6 bước cứu của ck250 đều còn ở ck500 ⇒ xu hướng nhất quán, không phải nhiễu ngẫu nhiên giữa hai điểm lưu.
- ⚠️ **Mặt trái không nằm trong exec:** ở 32 bước `scroll`, câu mở đầu bằng swipe/scroll giảm 27 → 23,
  bằng click tăng 3 → 6. GRPO dịch chung về phía "click" — được ở bước click, mất ở bước cuộn, mà exec
  chỉ chấm bước click. Cùng mẫu hình với `report` 21/9: mức tăng đến từ cổng loại thao tác, không phải định vị.
- Tiền lệ val phóng đại: GRPO `<point>` +0,76 trên val còn +0,02 trên test (`report/153`).

### 7.4 Việc người dùng quyết

1. Xác nhận **DỪNG** theo §2 (khuyến nghị), ghi vào luận văn như một kết quả âm/trắng có phân rã ở 7.3; hoặc
2. Chấm test 4.463 bước bằng ck500 (Kaggle T4 ~5,6 h, 0 đồng) chỉ để xem exec. Kỳ vọng thấp theo 7.3;
   nếu chạy thì phải báo kèm `action_ok` trên **mọi** loại thao tác, không chỉ bước chạm.

Tệp mới trong `runs/grpo_spice/`: `pred_ck500.jsonl` · `score_ck500{,_raw}.json[l]` ·
`score_k0_lai500{,_raw}.json[l]` · `gen_ck500.log` · `cham_ck500.log` · `cham_k0_lai500.log` · `train_c3.log`.
Adapter ck500 (60 MB, ngoài git): `_bundles/grpo-spice-ck500/grpo_spice/checkpoint-500/` (md5 `491fa667…`).
