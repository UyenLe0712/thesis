# 259 — Kết quả chấm TEST một lần của GRPO SPICE `checkpoint-500` (action 258) · 2/10/2026

Bàn giao cho chat lập kế hoạch. Tự chứa. Đây là **số test**, chấm đúng **một lần**, không sinh lại,
không đổi điểm lưu. Đọc theo luật 258 §0 đã khoá trước khi có số.

## 1. Đã chạy gì

- Kaggle T4, một commit 9,4 h (sinh 3,5 h · 2,80 s/bước; chấm 4,9 h · 0,25 bước/s), 0 đồng.
- Đường sinh như val: hoà `adapter_s1_seed101` → `s1_merged` (fp16) → gắn `checkpoint-500`
  (adapter md5 `491fa6677340393f1e4464c08a0cec98`) → greedy, 96 token, câu nhắc `prompt_body + SYS`.
- Chấm bằng **đúng bản `score_run.py` trong dataset `thesis-score`** — bản đã chấm S1/101 ra 59,11.
- Runbook đã chạy: `harness/runbook/kaggle_grpo_spice_test_ck500.md` · script sinh `harness/gen_test_grpo.py` ·
  script đọc `harness/grpo_spice_test_doc.py` · tệp `runs/grpo_spice/*_test*` + `test_ck500_doc.json`.

### Sáu chỗ 258 (chép từ ảnh) phải sửa mới chạy được

1. `grpo_spice.map(a)` → `grpo_spice.nap(a)` (không có hàm `map` ⇒ AttributeError).
2. `one(".../build_branch_data.py")` ra 2 tệp (`thesis-score` cũng có) ⇒ lấy bản cạnh `grpo_spice.py`.
   Người dùng đã gặp đúng lỗi này khi chạy nguyên văn 258.
3. `score_run.py` trong `thesis-score` là bản cũ, **không có** `--data-root/--recs-file` ⇒ gọi không cờ.
4. Ô 3 dán tay → tệp `gen_test_grpo.py` trong dataset script (thêm dòng `[dữ liệu]`, kiểm thiếu ảnh).
5. Kiểm hoà trên 20 **bước click** đầu (258 lấy 20 bản ghi đầu mọi loại thao tác).
6. Cắt sinh ở 6 h thay vì 11 h (sinh + chấm ≈ 9,4 h; quá 6 h thì không đủ giờ chấm).

Bảng mốc của 258 bị OCR đọc sai tên: "Hộp phản từ (0.3)" = **D.3** 65,49; "A11y đầy đủ" = **AitW
đầy đủ** 74,37. Phụ lục máy nhà của 258 bị cắt và trỏ đường Mac ⇒ thay bằng `grpo_spice_test_doc.py`.

## 2. Phép kiểm (đều đạt)

- Script đọc tái lập mốc S1: exec **59,11**, KTC [57,33; 60,83] khớp tuyệt đối `score_s1_seed101.json`;
  SPICE **44,37** khớp `text_metrics_coco.json` (cùng PTBTokenizer + SPICE, Java 8).
- KTC exec ck500 tính lại khớp tuyệt đối số Kaggle in ra [58,90; 62,38].
- Câu trong tệp thô chấm trùng `pred_ck500_test.jsonl` **4.463/4.463** từng ký tự.
- Cùng quần thể: 4.463 bước, G = 1.091 cụm, G hiệu dụng 454,3; bước rỗng duy nhất **(18710, 1)**,
  trùng đúng bước rỗng của S1/101.
- Log sinh: `[dữ liệu] … 4463 bước · thiếu OCR 0 · thiếu ảnh 0`, `[điểm lưu] …grpo-spice-ck500`, không lỗi.
- **Kiểm hoà 16/20** (ngưỡng ≥ 16): S1-hoà sinh trên test khác S1 công bố ở 4/20 câu (xem §5.1).

## 3. Số test, ck500 so với S1/101, ghép cặp 4.463 bước click

| thước | S1/101 | ck500 | Δ | KTC95 (cụm app) | KTC95 (cụm episode) | cứu / phá | p McNemar |
|---|---:|---:|---:|---|---|---|---|
| **exec** | 59,11 | **60,65** | **+1,55** | [+0,80; +2,33] | [+0,82; +2,28] | 159 / 90 | 1,6e−5 |
| **SPICE** | 44,37 | **45,79** | **+1,42** | [+0,69; +2,16] | [+0,72; +2,15] | | |
| action_ok | 94,35 | 95,97 | +1,61 | [+1,17; +2,08] | [+1,19; +2,05] | 83 / 11 | 2,4e−13 |
| D.3 | 65,49 | 67,02 | +1,52 | [+0,77; +2,29] | [+0,79; +2,29] | 165 / 97 | 3,5e−5 |
| AitW đầy đủ | 74,37 | 76,25 | +1,88 | [+1,17; +2,63] | [+1,16; +2,62] | 172 / 88 | 2,6e−7 |

Bootstrap: đúng `score_run.cluster_bootstrap` (cụm = app, như mọi KTC trong luận văn), B = 10.000.
SPICE: trung bình F theo câu (bằng SPICE mức hệ thống của pycocoevalcap), bootstrap trên cùng cụm.

**Luật 258 §0 ⇒ Hàng 1:** Δexec > 0, cận dưới KTC > 0, ΔSPICE > 0 — *"giữ checkpoint 500, được báo
là hơn S1 trên cả hai metric của lượt này"*.

### Phân rã Δexec (258 §0 đòi in action_ok)

- Cứu 159 (36 bước S1 sai loại thao tác) · phá 90 (8 bước ck500 sai loại thao tác).
- Ròng từ **sửa loại thao tác**: +28 bước (+0,63 pp) · ròng từ **đổi phần tử** (cả hai đúng loại thao
  tác): **+41 bước (+0,92 pp)**. Trên 4.200 bước cả hai đúng loại thao tác: exec 62,62 → 63,60.
- ⇒ Trên test, mức tăng **không** nằm gần hết ở action_ok (khác nỗi lo từ val: 5/12 bước cứu là
  swipe→click, phần định vị ròng chỉ +2 bước).
- Câu mở đầu bằng "swipe" ở bước click: 140 → 66. Câu trùng S1: 2.795/4.463. Số từ TB 7,83 → 7,96.

### So với các nhánh khác (exec, cùng 4.463 bước)

| phép so | Δ | KTC95 | cứu / phá | p |
|---|---:|---|---|---|
| ck500 − S1/202 (59,62) | +1,03 | [+0,25; +1,83] | 191 / 145 | 0,014 |
| ck500 − GRPO-point/101 (60,07, tiêu đề hiện hành) | **+0,58** | [−0,50; +1,69] | 312 / 286 | 0,31 |
| ck500 − MIN-DESC/101 (60,05) | +0,60 | [−0,52; +1,73] | 331 / 304 | 0,30 |

## 4. Đối chiếu với val

Val C1 (249 bước, số val, cấm trích): Δexec +2,81 [0,00; +6,02], ΔSPICE +0,15. Test: Δexec nhỏ hơn
nhưng chặt hơn nhiều, **ΔSPICE dương rõ** (+1,42) dù trên val gần 0. Trái chiều với tiền lệ GRPO
`<point>` (val +0,76 → test +0,02).

## 5. Chỗ phải khai / chưa đóng

1. **Lẫn biến đường sinh.** ck500 sinh trên S1 đã hoà, fp16, từng câu; S1/101 công bố sinh qua
   `infer_branch` (LoRA chưa hoà, theo lô, đệm trái). Kiểm hoà: 4/20 câu đổi chỉ vì đổi đường:
   - (18176,2) "One-way **option**" → "One-way **tab**" · (18176,12) đổi mệnh đề cuối ·
     (18176,15) "text 3" → "text "3" under the image of a person" · (18178,1) "search icon" → "Cruise Search tab".
   - Ở 2/4 câu, ck500 ra **đúng câu của S1-hoà** ⇒ một phần chênh ck500−S1 có thể là chênh đường sinh.
   - **Đề xuất đóng:** sinh + chấm **S1-hoà** trên test bằng đúng runbook, bỏ `--ckpt` (~9,5 h T4,
     0 đồng). Khi đó ck500 − S1-hoà chỉ còn một biến là GRPO.
2. **Dải bốn ô ở ch4 luận văn**: +1,55 nằm trong dải "trắng" (−2,8 … +1,7) và dưới MDE 2,11; một
   hạt giống. Chỉ đạo 14/9 bỏ khung đăng ký trước, nhưng bảng ch4 vẫn in dải này ⇒ phải xử lý câu chữ
   trước khi viết "hơn S1".
3. **Chưa có nhánh so sánh "train thêm cùng số bước không GRPO"** (cùng đòn đã áp cho GRPO-point).
4. **Bước không chạm chưa chấm** (`thesis-score` chỉ có ảnh click) ⇒ hàng 4 của 258 §0 (scroll) chưa
   kiểm được. Gói `test_images_nontap.tar` 1,54 GB đang ở scratchpad `/tmp` cũ, cần chuyển ra chỗ bền.
5. Không vượt điểm tiêu đề 60,07 có ý nghĩa (+0,58, p = 0,31).

## 6. Cần chat lập kế hoạch quyết

1. Có chạy lượt **S1-hoà trên test** (§5.1) trước khi đưa ck500 vào luận văn không. Khuyến nghị: có.
2. Có chạy bước không chạm (§5.4) không — cần thêm ~2 h T4 sinh + chấm `noharm` 0 GPU.
3. Cách đưa vào luận văn: thay tiêu đề 60,07 → 60,65, hay báo như một nhánh RL thưởng metric câu
   cạnh GRPO-point; và câu chữ về dải bốn ô.
