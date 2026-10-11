# 265 — Kiểm thử TAGE trên val C1 trước khi chạy thật (2/10/2026) — bản đã kiểm

Bản sắp xếp lại từ `265_…_manual_transcription.md` (chép tay từ 8 ảnh, cùng thư mục). Ảnh chỉ có
**phần đầu** Phụ lục A và **không có** Phụ lục B, C, D, nên máy WSL viết lại toàn bộ script theo đặc tả
ở thân bài (§4). Các ô chạy: **`harness/runbook/colab_tage_val_l4.md`** (Colab L4 — đang dùng, vì Kaggle T4 tuần
này chỉ còn ~1 h); bản Kaggle T4 ba commit giữ ở `harness/runbook/kaggle_tage_val.md` cho lượt sau.
⛔ **Mọi số ở đây và mọi số lượt này sinh ra là số val — không trích vào luận văn.**

## 0. Tóm tắt

Phiên lập kế hoạch vẫn chốt **TAGE** (Type-Aware Grounded Editor), đứng đầu tám ứng viên (8,70/10).
Hệ chạy bốn bước:

1. ck500 viết câu nháp như hiện nay (vd. `Click on the share option`).
2. Bộ định vị đọc màn, mục tiêu, lịch sử (có thể thêm câu nháp) rồi chỉ điểm cần chạm.
3. Cắt vùng vuông quanh điểm đó. Bộ biên tập (LoRA riêng trên S1 đã hoà) nhìn **cả màn + vùng cắt + câu
   nháp** rồi viết lại câu; câu nháp gọi sai phần tử thì sửa theo vùng cắt.
4. Cổng giữ/sửa: chỉ nhận câu sửa khi bộ biên tập đủ tự tin, không thì giữ câu nháp.

Khác PATA/FGRB: vùng đích không phải nhánh phụ mà decoder lờ đi được — bộ biên tập học từ đầu để đọc
vùng cắt, cộng loss tương phản (câu đúng phải dễ sinh hơn khi vùng cắt đúng phần tử so với khi vùng cắt
phần tử lân cận). UGround không dùng trong train hay suy luận, chỉ để chấm.

Lượt này không chạy thật, chỉ trả lời ba câu hỏi theo thứ tự rẻ → đắt:

| cổng | câu hỏi | không đạt thì |
|---|---|---|
| V1 | Cho vùng cắt đúng tuyệt đối (điểm chạm vàng), bộ biên tập có sửa được ck500 không? Vùng cắt sai phần tử có làm nó tệ đi không? | dừng TAGE — vùng hoàn hảo mà không giúp thì bộ định vị vô ích |
| V2 | Bộ định vị tự học có chỉ đúng phần tử ở những bước ck500 đang trỏ sai không? | cần thêm dữ liệu train cho bộ định vị trước V3 |
| V3 | Ghép thật (vùng dự đoán + cổng) có hơn ck500, và hơn bộ biên tập không vùng cắt không? | báo người dùng, chưa chạy thật |

## 1. Mốc phải vượt — đã tính lại trên WSL 2/10, khớp cả năm số

Val C1 = 400 bước lấy từ 1.567 bước val bằng `random.Random(20260927).sample`, có **249 bước click**.
Nguồn: `runs/grpo_spice/score_ck500_raw.jsonl` và `runs/c1/exec8/c1score/score_k{0..8}_raw.jsonl`
(bản chép tay ghi nhầm `score_AE_raw.jsonl`).

| | S1 greedy | ck500 |
|---|---:|---:|
| exec trên 249 click | 63,45 (158) | **66,27 (165)** |

84 bước ck500 sai: **63** đúng loại thao tác nhưng điểm bấm ngoài cửa sổ ±14% (gọi sai phần tử) ·
**17** trong cửa sổ nhưng sai ô Voronoi (nhầm phần tử sát bên) · **4** sai loại thao tác ⇒ **80 bước
"trỏ sai"** là đích của V2.

- **52/84** bước không có câu nào trong 9 câu S1 (greedy + 8 mẫu nhiệt độ 1,0) thực thi được ⇒ chọn lại
  câu (reranker, best-of-N) không cứu được; phải đưa thêm thông tin (vùng đích). Đây là lý do TAGE thắng
  speaker–listener reranker.
- Trần chọn câu (ck500, hoặc câu nào trong 9 câu S1 thực thi được) **79,12** (197/249) — dùng câu người
  để chọn, không phải hệ thật.

Mốc lượt này: **ck500 = 165/249**. S1 đã thấy val lúc SFT.

## 2. Thiết kế

Mọi nhánh dùng chung nền S1 hoà vào Qwen gốc (`s1_merged`), cùng ảnh, cùng câu nhắc như lúc sinh ck500
(`grpo_spice.body_of`). Câu nháp ở val là đúng câu ck500 đã sinh và đã chấm (`pred_ck500.jsonl`) ⇒ hiệu
số so ck500 là hiệu số ghép cặp.

### 2.1 Dữ liệu train

- **2.554 bước click train** của `fgrb-p1-bundle` (4.000 bước train có ảnh), không chung episode nào với val
  (bản chép tay ghi 2.523, đo trên bundle giả; bundle thật ra 2.554).
- Câu nháp train: ck500 sinh greedy + 2 mẫu nhiệt độ 1,0 cho từng bước. S1 đã học tập train lúc SFT nên
  câu greedy hay gần câu người; mẫu nhiệt độ và câu làm hỏng bù cho chuyện đó. Script in tỉ lệ greedy
  trùng câu người.
- Câu làm hỏng: xác suất 0,3, thay tên phần tử đúng bằng tên phần tử lân cận cùng vai trò (`tage_neg.jsonl`).
  ⚠️ Bản chép tay ghi "~58% bước làm hỏng được ⇒ ~17% mẫu"; **đo lại trên câu người: 43,8%** (1.119/2.554)
  ⇒ ~13% mẫu. Tỉ lệ trên câu nháp thật in ra ở dòng `[epoch 0]`.
- Vùng cắt: vuông, cạnh 40% bề ngang ảnh, tâm tại điểm chạm, đổi cỡ 448×448 (256 token ảnh). Ra ngoài mép
  thì đệm đen để điểm luôn ở tâm.
- Vùng cắt nhiễu cho loss tương phản: phần tử lân cận cùng vai trò (`point_neg_abs`, phủ 90,9% bước click
  train), không có thì mục OCR gần nhất nằm ngoài vùng vàng.

### 2.2 Các nhánh

| nhánh | bộ biên tập train với | vùng cắt lúc chạy val | trả lời |
|---|---|---|---|
| `gold` | vùng vàng + loss tương phản | vàng (điểm chạm thật) | trần của TAGE nếu bộ định vị hoàn hảo |
| `neg` | cùng bộ biên tập `gold` | phần tử lân cận **ngoài** vùng vàng (không có thì mục OCR gần nhất ngoài vùng) | bộ biên tập có thật sự đọc vùng cắt không |
| `none` | không vùng cắt, cùng dữ liệu và số bước | không | lợi ích có phải chỉ do train thêm LoRA |
| `pred` | cùng bộ biên tập `gold` | điểm bộ định vị dự đoán | hệ thật |

Mỗi nhánh có bản `+cổng`: sửa khi `lp_edit − lp_draft > τ` (log-xác suất trung bình mỗi token của câu sửa
và câu nháp, dưới chính bộ biên tập). τ chọn chéo theo episode: chọn trên nửa này, áp lên nửa kia. Cổng
tính offline ở máy nhà.

Bộ định vị, hai bản, đều LoRA r=16 sinh `(x, y)` thang 0–1000: `loc_g` (ảnh + mục tiêu + lịch sử) và
`loc_d` (thêm câu nháp ck500; lúc train lấy ngẫu nhiên greedy hoặc mẫu). Lấy bản trúng nhiều hơn trên 80
bước ck500 trỏ sai.

### 2.3 Siêu tham số mặc định (đổi được, ghi lại khi đổi)

LoRA r=16, alpha 32, dropout 0,05, chỉ tầng ngôn ngữ (assert không tham số nào thuộc `visual`) · lr 1e-4 ·
warmup 30 bước rồi giảm tuyến tính · 2 epoch · lô 1, tích luỹ 8 · λctr 0,5 · margin 0,2 nat/token ·
p_hỏng 0,3 · bf16 trên L4/A100, fp16 + GradScaler trên T4.

⚠️ **Đổi 2/10: 1 epoch thay vì 2** (cả `gold` lẫn `none`). Lượt TEST trên L4 đo 6,7 s/mẫu ⇒ 2 epoch ~9,5 h
chỉ riêng pha train. Lượt này là PoC để quyết có dùng TAGE không, nên người dùng chọn 1 epoch (~8,5–9 h tổng).
Hệ quả khi đọc: V1 âm hoặc vùng giữa có thể một phần do train chưa đủ; vùng giữa thì cân train tiếp epoch 2.

## 3. Ngưỡng đi tiếp

Không phải ngưỡng cho luận văn — chỉ để quyết có tốn thêm GPU không. Người dùng cho tối ưu tự do trên val;
đổi siêu tham số rồi chạy lại thì được, nhưng ghi lại mỗi lần chạy kèm số.

| cổng | đi tiếp khi | dừng khi |
|---|---|---|
| V1 | `gold` hoặc `gold+cổng` hơn ck500 ≥ 10 bước ròng (+4 điểm), **và** `gold` hơn `neg` ≥ 10 bước | `gold+cổng` ≤ ck500 + 1 điểm |
| V2 | bộ định vị tốt hơn trúng ±14% ≥ 20/80 bước trỏ sai | < 10/80 ⇒ cần train bộ định vị trên đủ 41 nghìn bước click, báo người dùng |
| V3 | `pred+cổng` hơn ck500 ≥ +1,5 điểm và hơn `none+cổng` | còn lại: báo người dùng |

Giữa hai cột thì báo người dùng quyết. Với 249 bước, KTC95 của một hiệu số ròng cỡ ±4–5 điểm ⇒ V3 đạt
chỉ là tín hiệu hướng. Trần thô tự kiểm: bộ định vị trúng `h`/80 và bộ biên tập sửa được tỉ lệ `f` (đọc từ
`gold`) ⇒ `pred` cứu ≈ `h·f` bước, trừ số bước cổng để lọt câu phá.
`tage_doc.py` in sẵn dòng `[V1]`, `[V2]`, `[V3]` theo bảng này.

## 4. Đã làm trên WSL 2/10

| tệp | việc |
|---|---|
| `harness/tage_val.py` | viết mới toàn bộ (Phụ lục A): `--selftest` · `--merge` · `--make-drafts` · `--train-editor` · `--edit-val` · `--train-locator` · `--locate-val`. Dùng lại `grpo_spice` (hoà S1, câu nhắc, hằng số) và `build_branch_data.SYS` |
| `harness/tage_doc.py` | viết mới (Phụ lục B): đọc mốc, các nhánh, cổng chọn chéo, bộ định vị, phán quyết V1–V3 |
| `harness/tage_neg_build.py` | viết mới (Phụ lục C): `tage_neg.jsonl` từ `descriptors_trueD.jsonl`, 41.099 dòng, 91,6% có phần tử lân cận |
| `harness/runbook/kaggle_tage_val.md` | runbook; Phụ lục D = Ô 7 (nguyên văn Ô 5 của `kaggle_grpo_spice_pha3_ck500.md`) |
| `_bundles/tage-val-script/` | 6 tệp cho dataset Kaggle, md5 ở runbook |

**Khác bản chép tay, có chủ ý:**
- md5 `tage_val.py` mới (`e15f9d52…`), vì script viết lại; `tage_doc.py` chạy ở máy nhà, không vào gói. md5 `c1_mau.jsonl` đúng là
  `d757554326977309c3a65ae0b144c211` (bản chép tay đọc nhầm `…b1d4c211`); tệp là `c1_mau.jsonl`, không phải
  `c1_raw.jsonl`. Ô 2 của bản chép tay còn có lỗi `sorted(...).values()`, đã bỏ.
- Đường dẫn Mac (`/Users/P836901/…`, `_exports/tage_val/`) đổi sang kho WSL: kết quả về `runs/tage_val/that/`.
- **Ba commit Kaggle T4** (câu nháp · train bộ biên tập · sửa val + chấm) thay cho một phiên: V1 ước lượng
  ~12 h trên T4, chạm trần phiên. Train lưu `ckpt_last/` (kèm optimizer) mỗi 50 bước nên commit bị cắt thì
  chạy tiếp được.
- Vế âm của loss tương phản lúc **train** nhận cả phần tử lân cận nằm trong vùng vàng (vế âm khó, vùng cắt
  vẫn đặt phần tử đó ở tâm); nhánh `neg` trên **val** chỉ nhận phần tử ngoài vùng vàng, như §2.2. Lý do đo
  được: nếu train cũng chỉ nhận phần tử ngoài vùng thì chỉ 833/2.554 vế âm là phần tử lân cận, 1.720 tụt
  về mục OCR (phần lớn phần tử lân cận cách đích 80–350 px, nằm trong nửa cạnh 216 px). Selftest hiện in:
  train lân cận 2.321 · OCR 233; val `neg` lân cận 93 · OCR 156.
- Che nhãn không giả định tokenizer: script token hoá câu nhắc riêng rồi **assert** nó là tiền tố của chuỗi
  đầy đủ (lệch là dừng).

**Đã kiểm trên WSL:**
- selftest với bundle thật (CPU, 2 giây): 400 bước · 249 click · lân cận 233 (93,6%) · 2.554 click train ·
  bộ đọc toạ độ · câu làm hỏng đúng dạng (`Click on the ok button.` → `Click on the Cancel button.`) · 6 cặp
  vùng cắt, xem bằng mắt: đích ở tâm, vùng nhiễu là phần tử khác.
- Mô hình Qwen2.5-VL tí hon (đúng kiến trúc, 2 tầng, trọng số ngẫu nhiên, CPU): `--make-drafts` chạy trọn
  (greedy + 2 mẫu với `num_return_sequences`); `--train-editor` qua được bước nạp, gắn LoRA (chỉ tầng ngôn
  ngữ), dựng câu nhắc **hai ảnh**, assert tiền tố che nhãn, và lượt forward đầu (nll 12,4 ≈ ln 151.936 — đúng
  với trọng số ngẫu nhiên). Dừng giữa chừng theo yêu cầu người dùng (nặng máy).
- `tage_doc.py` chạy khô với tệp giả: mốc ck500 ra đúng 66,27 (165/249) · 84 sai · 80 trỏ sai; k0_lai so
  ck500 −2,81 [−6,02; +0,40], khớp `report/254` §7.

**Lỗi bắt được ở lượt thật 2/10 (Colab L4):** train chết ở bước ~150–160 vì một nhãn hỏng trong tập dạy,
`ep14503_s1` có x = 2163 trên màn rộng 1080 ⇒ hàm cắt vùng ra khung rỗng (`right < left`). Thứ tự mẫu cố định
nên lượt chạy tiếp chết lại đúng chỗ đó; "mất máy" lần đầu thực ra là lỗi này (máy ảo vẫn sống, `s1_merged`
còn). Sửa: kéo điểm về trong ảnh trước khi cắt (không đổi thứ tự mẫu ⇒ điểm lưu cũ dùng tiếp được). Đã quét cả
train lẫn val: chỉ một bước này; 249 bước val sạch. md5 mới `e15f9d52…`.

**Chưa chạy lần nào:** trọn vòng train (bước tối ưu, lưu/tiếp), `--edit-val`, `--train-locator`,
`--locate-val`. Lượt `TEST = True` trên Kaggle là để bắt lỗi ở đây.

## 5. Thời gian ước lượng (chưa đo — lượt TEST in s/mẫu, s/bước)

| việc | A100 | L4 | T4 |
|---|---:|---:|---:|
| câu nháp train, ~2.554 bước × 3 câu | 1 h | 2 h | 3–4 h |
| bộ biên tập `gold`, 2 epoch, hai forward/mẫu | 1,5–2 h | 3–4 h | 6–8 h |
| sửa val, mỗi nhánh 249 bước | 10–15 ph | 20–30 ph | 40–60 ph |
| chấm UGround, mỗi tệp 249 bước | 10–20 ph | như A100 | 20–30 ph |
| **V1 cộng lại** | ~4 h | ~7 h | ~12 h |
| bộ biên tập `none` + hai bộ định vị | 2–3 h | 4–6 h | 8–12 h |
| **V2 + V3 cộng lại** | ~4 h | ~7 h | ~12 h |

Thủ tục chọn máy: T4 Kaggle 0 đồng là bậc đầu, nhưng hạn mức tuần đã gần hết (~1 h) ⇒ **người dùng chọn
Colab L4 (2/10)**. Một phiên L4 chạy trọn V1 (~7 h ước lượng), không phải tách commit.

## 6. Không tự làm

- Không chấm test. Không chạy thật trên toàn bộ train (lượt sau, người dùng quyết sau V3).
- Không dùng điểm vàng làm đầu vào hệ thật — nhánh `gold` chỉ để chẩn đoán.
- Không dùng UGround ngoài `score_run.py`.

**Người dùng quyết:** ① upload `tage-val-script`, chạy TEST, rồi ba commit · ② sau V1: đi tiếp V2/V3 hay
dừng · ③ sau V3: có mở lượt thật không (ảnh 41 nghìn bước click train ~12 GB, chấm toàn val, rồi mới chấm
test một lần).

Kết quả ghi vào `report/266_KET_QUA_TAGE_VAL_<ngày>.md`: bảng số, phán quyết theo §3, tóm tắt log train
(nll vàng, nll nhiễu, s/bước, VRAM).
