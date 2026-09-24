# 186 — TÌNH HÌNH PATA-C1 SAU KHI NHẬN `185` (23/9/2026)

> Ghi lại mọi việc từ lúc nhận bản `185` (9 ảnh chụp máy Mac) tới 14:45 giờ VN ngày 23/9. Spec
> phương pháp là `report/185_CHOT_PHUONG_PHAP_ACTION_PATA_CAUSAL_22_9.md`; file này chỉ ghi **đã
> làm gì, đo được gì, còn treo gì**. Nhãn [đo] = số chạy ra từ mã/tệp; [suy] = ước lượng.

## 0. Tóm tắt một bảng

| hạng mục | trạng thái |
|---|---|
| spec `185` | đã chép từ 9 ảnh → `report/185_…md`; ảnh gốc ở `report/anh_185_pata_causal_23_9/` |
| quyết định user | **Stage S chạy 1 epoch** (spec ghi 2) · **C1 trước**, chỉ chạy C0-Loc khi C1 qua cổng §8 |
| chặng A (0 GPU) — mã | xong: dữ liệu · mô hình · 13 test · trainer S/H/J · đánh giá · audit · gói zip |
| 13 unit test, mô hình tí hon, CPU | **13/13 ĐẠT** [đo] |
| 13 unit test, mô hình 3B thật, Kaggle T4 | lượt 1 OOM ở test 10 (lỗi của chính test, đã vá) · **lượt 2: 13/13 ĐẠT** (§3.7) |
| smoke S/H/J trên Kaggle T4 | xong, §3.7: S 79 s/u · H 60 s/u · J 79 s/u · VRAM đỉnh ≤ 5,4 GB |
| audit box (A1) | xong phần một người gán: **lỗi nặng 2,7% < ngưỡng 5%** ⇒ giữ box |
| quyết định còn treo | ~~tắt KL box lớn~~ → **tắt KL khi area ≥ 0,50** (`report/193`, đã thi hành: kl_ok 39.432) · người gán thứ hai · swap/random-pool · Colab |
| GPU đã tiêu | **0 đồng**, chỉ Kaggle T4 miễn phí ~3 phút |

---

## 1. Dọn thư mục (yêu cầu đầu phiên)

- Zip `runs/gate_a/My Documents [23-09-2026 12_45].zip` (9 ảnh, 4,0 MB) **nằm nhầm chỗ** — giải
  nén, xem đủ 9 ảnh, **đã xoá zip**.
- Ảnh cất ở `report/anh_185_pata_causal_23_9/01…09_<tên gốc>.jpg`, đánh số theo thứ tự đọc (theo
  hậu tố tên tệp 29…37, khớp thứ tự các mục 1→14 của tài liệu).
- Chép toàn văn thành `report/185_…md` (14 mục). Chỗ phải lưu ý khi đọc bản chép: các URL ở §10
  chép từ ảnh mờ, chuỗi hash có thể lệch một ký tự — mở lại trước khi trích.
- CLAUDE.md: thêm một dòng đầu bảng "Đọc file nào" trỏ tới `185`.

## 2. Quyết định của user trong phiên

1. **Stage S = 1 epoch** thay vì 2 (user: *"1 epoch thôi"*). Hệ quả đã khai ở `185` phần *Quyết định
   + thi hành 23/9*: điều kiện 3 cổng §8 vẫn so đúng (C1 so với **chính** S của lượt này), nhưng số
   S/C1 không so thẳng với S1 cũ (2 epoch, học cả val).
2. Chỉ chạy **C1** để xem có tốt không rồi mới quyết chạy tiếp (C0-Loc, hạt 2) — trùng quyết định
   vận hành sẵn có trong `185`.
3. Việc nào làm được không tốn GPU, hoặc không cần A100, thì làm trước và hướng dẫn từng bước.

## 3. Chặng A — mã đã viết (0 GPU, WSL)

Tất cả trong `harness/`. Không mã nào gọi LLaMA-Factory.

| tệp | vai trò | ứng với `185` |
|---|---|---|
| `pata_data.py` | dựng Train-proper / val400 / val600 bước chạm + box + cờ `kl_ok`; assert rời nhau; SHA-256; khoá probe 40 | §2, §3, §7b, bước A2–A3 |
| `pata_model.py` | TARGET token, localizer, bridge, đích patch, KL, dựng mẫu, collator, `forward_losses`, `load_base` (QLoRA NF4) | §4, §5 |
| `pata_test.py` | 13 unit test; `--tiny` (CPU) và `--real` (GPU) | §7, bước A4 |
| `pata_train.py` | vòng lặp train chung S / H / J (C1 hoặc `--no-bridge` = C0-Loc), nối tiếp sau mất máy | §6, bước 7–11 |
| `pata_eval.py` | `diag` (cổng H, mốc 800: CE/KL/hit/mass/lift/xáo) · `gen` (sinh câu bật/tắt bridge, ra preds cho `score_run.py`) | §6 Stage H, §7b, §8 |
| `pata_audit.py` | `build` (mẫu + trang gán nhãn HTML) · `doc` (tỉ lệ lỗi, Wilson, κ nếu có hai người) | §2 audit, bước A1 |
| `kaggle_pata_test.md` | runbook Kaggle ô K0–K7 | bước A4–A5 |
| `make_bundle.py` | thêm hai loại gói `pata_kaggle` · `pata_colab` | — |

### 3.1 Dữ liệu (`pata_data.py`) — [đo]

| tập | bước chạm | có box | thiếu box | box cắt vào biên màn | SHA-256 (16 ký tự đầu) |
|---|---|---|---|---|---|
| train_proper | **40.189** | **40.089** (99,75%) | 100 | 107 | `fd4db36c03884ef9` |
| val400 | 400 | 400 | 0 | 0 | `68ccb1c6259f6c01` |
| val600 | 602 | 601 | 1 | 1 | `dfacd1b2fc41c278` |
| probe40 | 40 (từ val400, có box, hạt 20260923) | 40 | — | — | `6c23c1898d85a0fd` |

- 100 bước thiếu box ở Train-proper = **91** bước không có dòng trong `descriptors.jsonl` + **9** bước
  điểm chạm **vượt khung ảnh khai báo** (vd x = 2163 trên màn rộng 1080 — nhiều khả năng màn ngang).
  Cả hai nhóm: **KL tắt, CE giữ**, đúng luật §2. (`185` ghi 92 thiếu box trên toàn 64.567 bước; một
  ca rơi vào val, nên Train-proper còn 91 + 9 ca toạ độ lạ.)
- **117/41.099** box a11y thò ra ngoài màn (đo trên toàn tập dạy); cắt vào khung ảnh. Sau khi cắt,
  mọi box đều chứa điểm chạm (assert).
- Rời nhau: episode · (episode, step) · ảnh/khoá OCR giữa ba tập — **đạt**; episode của tập dạy không
  chạm episode nào của hai tập val kể cả bước không chạm.
- Chạy lại hai lần ra đúng cùng hash; probe 40 có khoá: nếu tệp đã tồn tại mà dựng lại ra hash khác
  thì script dừng.
- ~2.512 update/epoch ở cỡ lô 16 (khớp ước ~2.500 của `185` §14).

### 3.2 Mô hình (`pata_model.py`) — cách thi hành và lý do

- **TARGET** = chuỗi đặc biệt `<TARGET>`, id **151665** — nằm trong 151.936 hàng embedding sẵn có
  nên không phải đổi cỡ ma trận. Véc-tơ của nó là tham số riêng `tvec` (khởi tạo = trung bình
  embedding từ vựng, §4), cắm vào bằng hook trên `embed_tokens`; không mở khoá cả ma trận.
- **Localizer + bridge** gắn bằng **forward hook trên block 17**, không bọc module. Lý do: bọc sẽ
  đổi tên tham số LoRA của block 17 và adapter Stage S nạp vào sẽ lệch khoá mà không báo lỗi.
- Hook chạy **bên trong** gradient checkpointing ⇒ **bắt buộc `use_reentrant=False`**; bản reentrant
  chạy forward trong `no_grad` nên α sẽ không có gradient mà KL vẫn in ra số bình thường.
- Các tham số mới (LN, Pq, Pv, Wo, gate, tvec) ở **FP32**, tắt autocast bên trong (§4 cho phép
  BF16/FP32, không lượng tử).
- **Stage H** cắt forward sau block 17 (chỉ cần hT và visual tokens ở đó) ⇒ bớt khoảng một nửa phép
  tính của chặng H.
- **CE chỉ gọi `lm_head` ở vị trí có nhãn** (~15 token/mẫu) thay vì cả chuỗi ~1.500 token ⇒ không
  dựng bảng logits 151.936 × chuỗi — đúng thứ làm cấu hình P4 tràn bộ nhớ hồi tháng 8.
- Đích patch đọc lưới từ `image_grid_thw`, co box theo đúng cỡ resize của processor, ô 28×28 px sau
  merge là dương nếu giao box, thứ tự raster, chuẩn hoá tổng = 1. Box suy biến (rộng 0) lấy ô chứa
  tâm.
- Prompt dùng **đúng** `build_branch_data.prompt_body` + `SYS` như mọi nhánh cũ (goal + 3 bước lịch
  sử + 24 dòng OCR), ảnh 200.704–1.003.520 px như `train_config.yaml` ⇒ một ảnh 1080×2400 = **1.272**
  token thị giác (đo lại trên Kaggle, khớp).
- LoRA: r 8, α 16, dropout 0,05, 7 khối, regex **loại `visual`** (tháp thị giác cũng có
  `gate/up/down_proj`; thiếu vế này là mở băng thị giác trong im lặng).

**Lựa chọn của phiên thi hành (spec không nói) — phải vào manifest §11:** d_k = 2048 · gate là
**một vô hướng** · "action head" = LN + Pq + Pv · clip grad 1,0 · NF4 double-quant · CE chuẩn hoá
theo token trên cả lô hiệu dụng (khớp LLaMA-Factory của S1) · KL chia cho số mẫu có box **trong lô
hiệu dụng** (nạp trước đủ `accum` lô con để biết mẫu số) · hạt khởi tạo module mới 20260923, hạt
thứ tự dữ liệu 101 · lưu mỗi 100 update, giữ vĩnh viễn điểm lưu 800.

### 3.3 Unit test (`pata_test.py`) — [đo]

**Mô hình tí hon, CPU** (Qwen2.5-VL dựng từ đúng config thật, thu nhỏ chiều; cùng processor, cùng id
token ảnh; ~75 s): **13/13 ĐẠT**. Số đáng ghi:

| test | kết quả |
|---|---|
| 3 đổi hậu tố vàng không đổi α(TARGET) | Δ = 0 |
| 4 Wo = 0 ⇒ logits bật = tắt bridge | Δ = 0 |
| 5 Wo ≠ 0: tiền tố không đổi, hậu tố đổi | tiền tố 0 · hậu tố 0,285 |
| 9 teacher-forced = KV-cache | Δ 3,3e−07 trên 6 bước |
| 10 save → reload | logits 0 · α 0 · câu trùng |
| 6 / 7 gradient | Wo, Pq, Pv, TARGET, LoRA ≠ 0; gate = 0 ở bước đầu (vì Wo = 0) rồi ≠ 0 sau một bước |
| 8 tháp thị giác | không gradient, trọng số không đổi |
| 12 overfit 8 mẫu, 40 bước | CE 11,79 → 11,08 · KL 2,41 → 0,11 · mass trong box 0,12 → 0,97 |

**Mô hình 3B thật, Kaggle T4, lượt 1 (user chạy 23/9):**

| test | kết quả |
|---|---|
| 1 token thị giác | **1.272** mỗi ảnh = t·h·w/4 = số ô đích |
| 2 box bốn góc | đạt |
| 3 α không đổi khi đổi hậu tố | Δ = 0 |
| 4 Wo = 0 | Δ = **0** (không chỉ trong sai số FP16 — đúng bằng 0) |
| 5 tiền tố / hậu tố | tiền tố **0** · hậu tố 0,473 |
| 9 KV-cache | Δ 2,69e−02 — **chỉ trên 2 bước** vì mô hình sinh EOS sớm |
| 10 save/reload | **OOM** (14,56 GB T4) |

Nguyên nhân OOM nằm ở **mã test**, không ở PATA: `logits_full` trả bảng logits đầy đủ (3 mẫu × ~1.500
token × 151.936, ~1,4 GB FP16, ×2 khi đổi sang FP32) và giữ vài bảng trên GPU cùng lúc rồi nạp thêm
bản mô hình thứ hai. **Đã vá:** chuyển logits sang CPU ngay sau mỗi forward, `gc` + `empty_cache`
trước khi nạp bản thứ hai; test 9 đưa `ref` và logits sinh về cùng CPU (lỗi lệch thiết bị mà chế độ
tí hon không bắt được vì toàn CPU); test 9 ép **`min_new_tokens=6`** để so đủ 6 bước. Chạy lại tí hon
13/13 ĐẠT; gói Kaggle đã dựng lại.

### 3.4 Trainer (`pata_train.py`) — chạy thử trên CPU [đo]

- Ba chặng chạy thông trên mô hình tí hon (lọc về ảnh có trên máy).
- **Nối tiếp:** xin 5 update khi đã có điểm lưu 3 ⇒ in `[nối tiếp] … update 3/981`, chạy tiếp đúng
  u4–u5 (phép thử xin **nhiều hơn** số đã có, theo luật dự án).
- **H:** chỉ 4.480 tham số localizer học (tí hon), `gn` LoRA = 0 (LoRA S đóng băng đúng), KL có số.
- **J (C1) vs `--no-bridge` (C0-Loc):** cùng hạt thứ tự dữ liệu ⇒ update 1 và 2 ra **CE/KL trùng tuyệt
  đối** (vì Wo = 0 lúc đầu), lệch từ update 3 ⇒ bằng chứng hai nhánh thấy đúng cùng dữ liệu, ghép cặp
  được như §9 đòi. C0-Loc không có nhóm tham số bridge (37.248 vs 41.345 tham số học ở bản tí hon).
- Điểm lưu ghi vào thư mục tạm rồi đổi tên, chỉ tính là trọn khi có tệp `DONE`.

### 3.5 Đánh giá (`pata_eval.py`)

- `diag`: CE_val · KL_val · Hit-in-box · mass trong box · mass của **center prior** (Gauss σ = 0,25)
  và **train-location prior** (histogram phủ box 32×32 trên Train-proper) · mass khi **xáo
  goal/history** (hoán vị cố định, luôn lấy của episode khác). Cổng H in ra tự động: cận dưới KTC một
  phía 90% (bootstrap cụm theo episode, 10.000 lần) của cả ba hiệu > 0.
- `gen`: sinh tham lam bật/tắt bridge, ghi `preds_<ckpt>_<split>_<on|off>.jsonl` đúng định dạng
  `infer_branch.py` (có `gold_instruction`) để `score_run.py` chấm; in % câu đổi, format hợp lệ, độ
  dài. Chạy val600 in cảnh báo "chỉ một lần sau hết epoch".
- Đã chạy thử `diag` (H, S) và `gen` (J) trên CPU tí hon.
- ⛔ **Chưa viết swap / random-pool** (§8 điều 5): cần hộp của phần tử distractor, chưa có trong dữ
  liệu (descriptors chỉ có *điểm* của `desc_neg`). Chỉ cần tới ở bước 12, sau khi C1 train xong.

### 3.6 Gói chuyển máy

| gói | nội dung | cỡ |
|---|---|---|
| `_bundles/thesis_pata_kaggle.zip` | mã + `pata/*.jsonl` + 40 ảnh probe + 400 ảnh dạy (smoke) + OCR của đúng các ảnh đó | 159 MB |
| `_bundles/thesis_pata_colab.zip` | mã + `pata/*.jsonl` + `ocr.jsonl` đủ tập dạy, **không ảnh** (ảnh lấy từ `train_images_p*.tar` trên Drive) | 26 MB |

⚠️ `thesis_pata_colab.zip` dựng **trước** các bản vá test 23/9 chiều — dựng lại trước khi dùng.

### 3.7 Kaggle lượt 2 (gói đã vá) — [đo]

**13/13 ĐẠT trên mô hình 3B thật** (1.458 s). Số chính: test 4 và 5 lệch tiền tố **0** · test 9
KV-cache Δ 5,86e−02 trên **đủ 6 bước** · test 10 save/reload logits **0**, α **0**, câu trùng · test 6
gradient Wo 2,1 · Pq 6,1 · TARGET 130 · LoRA 110 · gate 0 (đúng vì Wo = 0) · test 7 gate 5,5e−02 sau một
bước · **test 12 overfit 8 mẫu: CE 1,99 → 0,03 · KL 3,80 → 0,09 · mass trong box 0,08 → 0,98.**

**Smoke 20 update mỗi chặng** (400 ảnh dạy trong gói, T4 FP16, lô 2 × gộp 8 = 16):

| chặng | tham số học | s/update | VRAM đỉnh | diễn biến |
|---|---|---|---|---|
| S | **14.966.784** (trùng khít số LoRA của S1 cũ trên LLaMA-Factory) | 79 | 4,5 GB | CE 2,32 → 1,88 → 1,47 → 0,89 (u1 → u15) |
| H | 8.402.944 = Pq + Pv + 2 LN + TARGET | 60 | 5,4 GB | KL 4,04 → 3,25–3,42 · mass 0,03 → 0,08 · `lora` grad = 0 |
| J (C1) | 27.564.033 = LoRA + localizer 23.369.728 + Wo 4.194.304 + **1** gate | 79 | ~4,9 GB | CE 2,41 → 1,20 · gate 0,11920 → 0,11927 · resid 0 → 0,050 |

- Chẩn đoán H trên probe 40 sau 20 update: cổng H **không đạt** (đúng dự kiến, chỉ thử script).
- Sinh câu C1 sau 20 update: tắt bridge làm **20%** câu đổi (ngưỡng mốc 800 là 30%).
- ⚠️ **H chỉ nhanh hơn S 24%**, không phải một nửa như ước: tháp thị giác + backward qua 18 block vẫn
  chạy. Sửa ước giờ ở §5.
- ⭐ **TARGET làm lệch speaker S** — phép kiểm CE trên probe 40: S không TARGET **1,12** · S + TARGET
  (điểm lưu H, LoRA S giữ nguyên) **2,36** · C1 sau 20 update ở lr 2e−5 **1,27**. ⇒ không phải lỗi nạp
  adapter; là tính chất của việc chèn token lạ trước câu, và J hồi rất nhanh. Phép so C1 − C0-Loc vẫn
  công bằng (cả hai có TARGET), nhưng cổng §8 điều 3 (C1 không thua S) phải trả phần "hồi" này ⇒ theo
  dõi ở mốc 800.
- **Hệ quả chọn máy:** 79 s/u × ~2.512 update ≈ 55 h/chặng trên T4 ⇒ **không train được trên T4** (Kaggle
  30 h/tuần, 12 h/phiên). VRAM ≤ 5,4 GB ⇒ L4 thừa bộ nhớ; tốc độ L4 so A100 phải đo trên Colab.

### 3.8 Đọc kỹ log smoke: gradient của TARGET làm tê liệt các nhóm khác — đã vá — [đo]

`runs/pata/kaggle_smoke/ck/*/train_log.jsonl`, chuẩn gradient TRƯỚC khi cắt:

| update | `tvec` (H) | `pq`/`pv` (H) | `tvec` (C1) | `lora` (C1) |
|---|---|---|---|---|
| 1 | 9,8 | 5,0 / 4,9 | 585 | 38 |
| 11 | 96 | 2,3 / 2,3 | 112 | 8 |
| 15 | **1.645** | 3,9 / 3,9 | 441 | 26 |
| 20 | 310 | 3,5 / 3,6 | 770 | 41 |

Trainer cắt gradient theo **tổng chuẩn chung** về 1,0 ⇒ khi `tvec` ~1.645, Pq/Pv/LoRA/Wo bị nhân hệ số
~1/1.645, gần như đứng yên. Khớp với log: KL chặng H chững 3,4–3,5 từ u5 tới u20, trong khi test 12
(không cắt gradient) KL 3,80 → 0,09.
Nguyên nhân [suy]: TARGET khởi tạo bằng trung bình 151k embedding ⇒ chuẩn rất nhỏ ⇒ RMSNorm đầu vào
khuếch đại gradient. AdamW tự chuẩn hoá bước của chính `tvec` nên TARGET vẫn học; chỉ cắt chung là hại.
**Vá (23/9 tối):** tách `tvec` thành nhóm riêng và cắt 1,0 **theo từng nhóm** (lora · localizer ·
target · bridge). LR từng nhóm giữ nguyên §6; khởi tạo mean-vocabulary giữ nguyên §4; spec không quy
định cách cắt gradient. Log thêm `tvec_norm`. Chạy thử CPU: S/H/J + nối tiếp đạt. ⚠️ Điểm lưu cũ (một
nhóm) không nối tiếp được sang bản mới — không sao vì chưa có lượt thật.

Các điều khác đọc được:
- Chẩn đoán H trên probe 40 sau 20 update: mass 0,075 vs center prior 0,025 / train prior 0,040; hit
  17,5% vs 0% / 7,5% ⇒ đã hơn prior. Nhưng **xáo goal/history không đổi mass (−0,0002)** ⇒ localizer
  mới học "vùng nào trông bấm được", chưa dùng mục tiêu — đúng vế thứ ba của cổng H; một phần có thể do
  lỗi cắt gradient ở trên. Phải theo dõi ở cổng H thật.
- C1: gate nhận gradient từ u5 (0,077), `resid` 0 → 0,053, CE 2,41 → 1,02. VRAM đỉnh ≤ 5,4 GB mọi chặng.
- Sinh câu probe 40: format hợp lệ bật 95% / tắt 87,5%. Một ca bật bridge đổi sang sai phần tử
  ("fade in" → "OK button") khi localizer còn kém — minh hoạ vì sao cổng H phải đứng trước C1.

### 3.9 Colab 23/9 tối — [đo]

P2 đạt: hash 4/4 · 40.189 chạm · 39.432 kl_ok · đủ 41.191 ảnh. **L4: 50,6 s/update, VRAM 6,49 GB**
(lô 4 × gộp 4) ⇒ S ≈ 35 h. A100 không kết nối được ⇒ **user quyết chạy S trên L4, lưu điểm lưu, hôm sau
đo A100 và nếu đạt luật 1,5× thì chạy tiếp từ điểm lưu L4 trên A100.** Quy trình đổi máy ở
`harness/colab_pata_c1.md` mục *Đo máy thực tế + đổi máy giữa lượt*.

### 3.10 Tốc độ trên A100 và thủ phạm (23–24/9) — [đo]

- Lô 4 × 4: 22,8 s/u · lô 16 × 1 (từ update 100): 23,9 s/u · chờ dữ liệu 0% · GPU bận 30–50% ⇒ giả
  thuyết "đói việc vì lô nhỏ" bị bác. Giữ 16 × 1 (tương đương toán học; CPU: CE update kế trùng 6 chữ số).
- Mất máy sau ckpt-01100 (Drive giữ 2 điểm lưu mới nhất + mốc 800 nên không có ckpt-00900 — đúng thiết kế).
- VM mới (torch 2.11 cu130, Python 3.13) thiếu `libnvrtc-builtins.so.13.0` ⇒ `image_grid_thw.prod(-1)` trên
  GPU hỏng lúc khởi động. Vá bằng `LD_LIBRARY_PATH` chỉ trỏ `nvidia/cu13/lib`; P1 nay tự kiểm.
- Kaggle K9: tháp thị giác 14% forward; attention `block` chậm hơn (0,60×), lệch tương đối 7e−3 ⇒ bỏ.
  **Backward gấp đôi forward, 4.748 lời gọi backward attention mỗi bước ⇒ tháp thị giác bị kéo vào đồ thị
  gradient** bởi `enable_input_require_grads()` mà `gradient_checkpointing_enable()` tự gọi. Vá trong
  `enable_gc`; tương đương từng bit trên mô hình tí hon (Δ gradient = 0,0 / 41.345 phần tử).

### 3.11 Sau khi vá gradient tháp thị giác (24/9) — [đo]

- **A100, Stage S nối tiếp từ ckpt-01500:** `u1520 … 8,2 s/u (gần 8,0) · vram 11,7–12,2 GB`, CE 0,66–0,77
  (trước vá 0,64–0,83), chuẩn gradient LoRA 1,1–1,9 ⇒ **nhanh gấp 3 lần (23,9 → 8,0 s/u)**, đường CE liền
  mạch. S dự kiến xong ~11:45 VN 24/9.
- **Kaggle T4, mô hình 3B thật, cùng lô, dropout tắt:** CE 3,307160 ở cả hai chế độ (trùng tuyệt đối) ·
  chuẩn gradient LoRA 4,9754 (có gradient thị giác) vs 4,9758 (không) trên 14.966.784 phần tử · lệch phần
  tử lớn nhất 2,7e−3 · thời gian bước 9,32 → 5,49 s (1,70×). Lệch còn lại là sai số FP16 do thứ tự tính
  lại khác nhau; tí hon FP32 trùng từng bit. ⚠️ Script in `cosine 1,001809` — **vượt 1 là sai số của chính
  phép cosine float32 trên 15 triệu phần tử**, không phải của gradient; nếu cần số sạch, tính lại float64.
- Manifest phải ghi: "Stage S update 1–1.500 có gradient thừa qua tháp thị giác, từ 1.501 không (tương
  đương về phép toán; lệch ở mức làm tròn FP)". H, C1, C0-Loc chạy trọn bằng bản đã vá.
- Ước giờ mới (A100, 8 s/u): H ~4–5 h (2.465 update, forward cắt sau block 17) · C1 ~5,5–6 h.

### 3.12 Stage S XONG · Stage H bắt đầu (24/9 ~11:40 VN) — [đo]

- `pata_ck/S/final` (SHA-256 cho manifest §11): `adapter_model.safetensors`
  `da6484273196946c81a971dd0fcb354e81d5fbb615a7b7e276aaba04a959c8f7` · `adapter_config.json`
  `da0d95e635a2…` · `meta.json` `3f29900d5f1f…`.
- **P6 — CE_val của S trên val400 = 0,7295** (n = 400; chỉ để bắt phân kỳ).
- H: 39.432 mẫu · 8.402.944 tham số học (localizer 8.400.896 + target 2.048) · 2.465 update · warmup 74 ·
  `gn lora = 0`. KL 3,88 → 3,49 → 3,22 → 3,16 → 3,11 · mass 0,047 → 0,049 → 0,079 → 0,094 → 0,099 (u2 → u80).
  ~5,6 s/u (lên ~8 lúc P6 chạy song song) ⇒ dự kiến xong ~15:30 VN.
- ⚠️ Terminal Colab KHÔNG thừa hưởng `LD_LIBRARY_PATH` của notebook — lệnh chạy trong Terminal phải
  `export LD_LIBRARY_PATH=/usr/local/lib/python3.13/dist-packages/nvidia/cu13/lib:$LD_LIBRARY_PATH` trước.

### 3.13 Công cụ cổng cuối C1 (viết 24/9 trong lúc H chạy, TRƯỚC khi C1 train)

- `harness/pata_swap.py` → `pata/val600_swap.jsonl` (sha `ef17c5820e6f…`, hạt 20260924): **546** bước val600
  có hộp D (cùng cỡ hộp vàng, tâm tại điểm `desc_neg` — ⚠️ xấp xỉ vì chỉ có điểm, không có hộp thật của
  phần tử gây nhiễu) và hộp R (hộp vàng của bước khác, chuẩn hoá theo màn). Bỏ: 15 không kl_ok · 36 không
  `desc_neg` · 5 D chồng vàng (IoU ≥ 0,3).
- `pata_eval.py gen`: thêm `swapD`/`swapR` (ép α của bridge), ghi dần + nối tiếp, cờ `--tag` (S/H/J đều
  tên `final` ⇒ không tag là đè tệp). **Test 14** (ép α đổi hậu tố, không đổi tiền tố; ép đúng α tự sinh
  = không ép, Δ = 0) ⇒ **14/14 ĐẠT**.
- `harness/pata_cong_c1.py`: 5 điều kiện §8, **ngưỡng khoá trong mã 24/9**: (1) hợp lệ ≥ 99%, độ dài
  ≤ 1,5× S, rỗng ≤ S + 1 điểm · (2) CE_val(J) ≤ 1,25× CE_val(S), KL_val(J) ≤ 1,10× KL_val(H), ba cận
  dưới 90% > 0 · (3) exec(C1) ≥ exec(S) · (4) exec(C1 bật) > exec(C1 tắt) · (5) cận dưới 90% của
  P(về D | ép D) − P(về D | ép R) > 0. Chạy thử trên dữ liệu giả: chạy thông.
- `harness/kaggle_pata_cham_val600.md` (P10): chấm 5 tệp preds trên Kaggle T4 × 2 song song.

## 4. Audit box (A1) — [đo]

Trang gán nhãn `dg1_cache/train_ac/pata/audit/audit.html` (ảnh vẽ box đỏ + điểm chạm xanh + khung
phóng; ẩn tầng, xáo thứ tự; tự lưu nháp). Quần thể lấy mẫu = bước chạm Train-proper **có ảnh trên
máy** (8 shard rải đều của `keo_anh_val.py`): 3.909 có box + 14 không box. ⚠️ Khai khi viết: ước
lượng trên 8/76 shard.

Mẫu: U 150 ngẫu nhiên (xác suất chọn 150/3.909) + năm tầng lấy dư 20 mẫu mỗi tầng + 14 bước không box
= **264**. User gán đủ 264/264 (người gán: Uyên).

| tầng | n | lỗi nặng | loại lỗi |
|---|---|---|---|
| **U (ước lượng quần thể)** | 148 (bỏ 2 "không rõ") | **4 = 2,7%** · Wilson95 **[1,1; 6,7]** | 4 × box thuộc phần tử khác |
| S1 widget nhỏ (area ≤ 0,002) | 20 | 1 = 5% | phần tử khác |
| **S2 container (area ≥ 0,089)** | 20 | **7 = 35%** | 4 phần tử khác · 3 stale · 1 lỗi nhẹ |
| S3 sát biên | 20 | 2 = 10% | stale, box phủ 79–87% màn |
| S4 tên từ OCR | 20 | 2 = 10% | phần tử khác |
| S5 không tên | 20 | 2 = 10% | stale, box phủ 55–92% màn |
| N không box | 14 | — | **14/14 có phần tử rõ tại điểm chạm** ⇒ thiếu box là labeler bỏ sót |

**Kết luận theo luật khoá trước (§2):** 2,7% < 5% ⇒ **giữ box, đi tiếp**. Phải khai: cận trên
Wilson 6,7% vượt 5%; chỉ **một** người gán nên chưa có κ và adjudication như §2 đòi.

**Phát hiện: lỗi nặng dồn vào box rất lớn** (gộp mọi tầng, bỏ "không rõ"):

| diện tích box | lỗi nặng |
|---|---|
| ≤ 0,01 | 2/130 |
| 0,01–0,05 | 1/64 |
| 0,05–0,089 | 3/17 |
| ≥ 0,089 | 12/37 |

| ngưỡng tắt KL | box lớn: lỗi nặng | phần còn lại | tầng U còn lại | số bước Train-proper mất KL |
|---|---|---|---|---|
| area ≥ 0,25 | **10/18** (Wilson ~[34; 75]%) | 8/230 | 3/145 = 2,1% | **883 (2,20%)** |
| area ≥ 0,4 | 10/17 | 8/231 | 3/145 | 708 (1,77%) |
| area ≥ 0,5 | 10/17 | 8/231 | 3/145 | 657 (1,64%) |

Mọi lỗi stale đều nằm ở box ≥ 0,5. Ba ngưỡng cho gần như cùng kết quả ⇒ con số 0,25 không nhạy.

**Lợi/hại của việc tắt KL cho box ≥ 0,25 (đã trình user, chờ quyết):**
- Lợi: bỏ ~300–650 nhãn KL sai [suy, từ 10/18 × 883]; bỏ nhãn gần như không mang thông tin vị trí
  (box 25% màn ≈ trên 300/1.272 ô cùng là "đúng"); cổng H sạch hơn vì box khổng lồ làm cả mass của mô
  hình lẫn của prior cùng cao.
- Hại: mất tín hiệu đúng ở ~nửa số box lớn (phần tử thật sự to, ~2% số bước); là quyết định **sau khi
  thấy audit** (trước mọi train, không đụng `exec`) nên phải khai; chỉ sửa được một phần (còn 8/230
  lỗi ở box nhỏ hơn).
- Khuyến nghị: tắt, và áp **cùng luật** cho `diag` trên val400/val600. Giữ nguyên cũng hợp lệ vì 2,7%
  đã dưới ngưỡng.

## 4b. Vì sao tắt KL cho box lớn (viết theo yêu cầu user 23/9)

> ⛔ **ĐÃ BỊ `report/193` THAY (23/9 tối): ngưỡng chốt là `area_share ≥ 0,50`, KHÔNG phải 0,25.**
> Hai lỗi trong mục này, giữ nguyên văn bên dưới để tra: ① "~300–650 nhãn sai" là SAI — 10/18 đến từ
> mẫu cố ý lấy dư box lớn, không được nhân với 883; ② câu "ba ngưỡng như nhau nên chọn 0,25" là suy
> ngược — kết quả audit bằng nhau thì phải chọn ngưỡng bảo thủ 0,50 (0,25 bỏ thêm 226 bước còn mang
> thông tin: 465/1.272 ô, center prior 0,454). Đã thi hành 0,50: Train-proper `kl_ok` **39.432**
> (tắt 657) · val400 398 (tắt 2) · val600 587 (tắt 14).

**Hướng đã chọn: tắt KL (CE giữ nguyên) cho bước có box ≥ 0,25 diện tích màn, áp cùng luật cho phép
đo vị trí trên val400/val600.** Sửa `pata_data.py` **sau** khi lượt Kaggle đang chạy xong, để gói
đang chạy không lệch với mã trên máy.

### Nhắc lại KL làm gì

Ở chặng H và J, bộ định vị của TARGET cho ra một phân phối chú ý α trên 1.272 ô ảnh (lưới 24 × 53, mỗi
ô 28 × 28 px sau resize). Đích p rải đều lên **mọi ô giao box**. KL(p ‖ α) kéo α dồn vào đúng các ô
đó. Box càng nhỏ, đích càng nhọn, tín hiệu "phần tử nằm ở đâu" càng rõ. Bridge sau đó lấy
z = Σ αᵢ vᵢ, tức **trung bình đặc trưng thị giác theo α**, đưa vào TARGET cho phần sinh câu dùng.

### Ba lý do, kèm số đo [đo trên `pata/*.jsonl`, 0 GPU]

**① Box lớn không mang thông tin vị trí: đích phủ gần hết màn.**

| diện tích box | tỉ lệ Train-proper | ô dương TB / 1.272 | mass của center prior trong box | mass của train-location prior |
|---|---|---|---|---|
| < 0,01 | 48,60% | 12,3 | 0,007 | 0,021 |
| 0,01–0,05 | 38,05% | 48,3 | 0,042 | 0,047 |
| 0,05–0,25 | 11,15% | 126,1 | 0,113 | 0,110 |
| **0,25–0,5** | **0,56%** (226) | **465,0** | **0,454** | 0,351 |
| **≥ 0,5** | **1,64%** (657) | **1.096,3** (86% màn) | **0,936** | 0,870 |

Với box ≥ 0,5, một phép đoán không nhìn ảnh ("nhìn vào giữa màn") đã có 0,94 mass trong box. KL trên
các bước này **không dạy được "phần tử ở đâu"**; nó chỉ dạy α **trải rộng ra**, ngược chiều với 97,8%
bước còn lại vốn dạy α **nhọn lại**. Kéo theo: z của bridge thành trung bình gần cả màn, không mang
thông tin gì về phần tử đích.

**② Box lớn phần lớn là nhãn sai** (audit §4): box ≥ 0,25 lỗi nặng **10/18** (Wilson ~[34; 75]%),
và **mọi** lỗi stale đều ở box ≥ 0,5. Phần còn lại 8/230. Nhìn ảnh audit, dạng lỗi điển hình là
labeler lấy **khung chứa** (cả thẻ, cả danh sách, cả vùng nội dung) thay cho nút bên trong — đúng dạng
luật "node usable nhỏ nhất chứa điểm chạm" gặp khi nút con không được đánh dấu bấm được.
⇒ ước **~300–650** bước đang dạy bộ định vị nhìn sai chỗ [suy: 10/18 × 883, cận theo Wilson].

**③ Chi phí gần bằng 0.** Mất KL ở **883/40.089 = 2,20%** bước; CE (học câu) giữ nguyên cho cả 883
bước; chặng H bớt 2,2% số mẫu ⇒ nhanh hơn chút. Tầng U sau khi bỏ box lớn còn lỗi nặng 3/145 = 2,1%.

### Cái mất và cái phải khai

- Mất tín hiệu đúng ở khoảng một nửa số box lớn (phần tử thật sự to: thẻ bài viết, ô danh sách rộng).
  Ở tập kiểm, với phần tử lớn, chỉ vào một phần của nó thường vẫn đúng ⇒ thiệt nhỏ [suy].
- Quyết định đưa ra **sau khi thấy audit**, trước mọi lượt train, không đụng `exec` hay dữ liệu kiểm.
  Ngưỡng 0,25 chọn nhìn theo audit; ngưỡng 0,4 và 0,5 cho gần như cùng kết quả (10/17 lỗi, mất
  1,6–1,8%) ⇒ không nhạy với lựa chọn.
- ⚠️ **Tự sửa một luận điểm đã nêu với user:** "cổng H sạch hơn" là **đúng về chiều nhưng nhỏ về cỡ**.
  val400 chỉ có **4** box ≥ 0,25 (1,0%), val600 có **19** (3,2%). Lợi chính của việc tắt nằm ở
  **tập dạy** (①, ②), không ở phép đo.
- Luật khoá trước của `185` §2 **không bắt buộc** việc này (2,7% < 5%). Đây là một lọc bổ sung, phải
  vào manifest §11 dưới mục *box eligibility rule*: `kl_ok = có box ∧ điểm chạm trong ảnh ∧ area_share < 0,25`.

### Việc sẽ làm khi thi hành

1. `pata_data.py`: thêm điều kiện `area_share < 0,25` vào `kl_ok`, đếm riêng `box_lon`; `box` vẫn giữ
   trong bản ghi (để audit/diag còn đọc được), chỉ `kl_ok` đổi.
2. Dựng lại `pata/*.jsonl` + `split_hash.json`. **probe40 giữ nguyên hash**: đã kiểm, không mẫu nào
   trong probe40 có box ≥ 0,25 [đo], nên luật mới không đụng tới probe (bể lấy mẫu của probe đổi
   nhưng vì probe là tệp khoá, script so hash tệp cũ chứ không bốc lại).
3. `pata_eval.py diag`: chỉ tính KL/mass/hit/lift trên bước `kl_ok` (đã vậy sẵn vì `ptarget` rỗng khi
   `kl_ok` sai).
4. Dựng lại hai gói zip, commit.

## 5. Ước giờ GPU (S 1 epoch) — [suy], chờ số đo smoke thay vào

| chặng | update | A100 sàn (10,3 s/u) | ghi chú |
|---|---|---|---|
| S, 1 epoch | ~2.512 | ~7 h | |
| H, 1 epoch | ~2.450 (39.432/16) | ~5–6 h | forward cắt sau block 17 nhưng đo trên T4 chỉ nhanh hơn S 24% |
| C1 (J), 1 epoch | ~2.512 | ~7 h | |
| chấm val600 bật/tắt bridge | — | 1–3 h | sinh câu trên GPU, chấm UGround trên Kaggle T4 |
| **tổng tới cổng C1** | | **~20–24 h** | spec gốc (S 2 epoch) là 29–35 h |

Theo luật chọn máy: smoke Kaggle (K4) cho đỉnh VRAM; nếu ≤ ~17 GB thì thử L4 trước, chỉ lên A100 khi
L4 chậm hơn 1,5 lần. Chặng H (chỉ học đầu nhỏ, forward nửa mô hình) là ứng viên L4 rõ nhất.

## 6. Việc kế, theo thứ tự

1. **User:** Kaggle — New Version dataset `thesis-pata` bằng `thesis_pata_kaggle.zip` mới → chạy lại
   K1 → K3 (phải `13/13 ĐẠT`) → K4–K6 smoke → K7 gom log vào `runs/pata/kaggle_smoke/`.
2. **User quyết:** tắt KL cho box ≥ 0,25 hay giữ.
3. **User quyết:** có người gán thứ hai cho 60 mẫu chồng (`audit.html#overlap`) không; không có thì
   khai là hạn chế.
4. **Phiên sau:** (nếu tắt) sửa `pata_data.py` + dựng lại hash/gói; seal manifest §11 (sau khi có SHA
   checkpoint S); viết runbook Colab S → H → C1 kèm phép đo L4 vs A100; viết swap/random-pool trước
   bước 12.

## 7. Tệp đã đổi trong phiên

- mới: `report/185_…md` · `report/186_…md` (file này) · `report/anh_185_pata_causal_23_9/` (9 ảnh) ·
  `harness/pata_{data,model,test,train,eval,audit}.py` · `harness/kaggle_pata_test.md`
- sửa: `harness/make_bundle.py` (thêm `pata_kaggle`, `pata_colab`) · `CLAUDE.md` (dòng trỏ `185`) ·
  `.gitignore` (mở cho `pata/split_hash.json`, `probe40.jsonl`, `audit/manifest.json`,
  `audit/audit.html`, `audit/audit_*.json` — tệp nhỏ nhưng cần để tái lập và giữ công gán nhãn)
- xoá: zip ảnh trong `runs/gate_a/`
- không commit: `pata/*.jsonl` lớn (dựng lại bằng `pata_data.py`, hash ở `split_hash.json`),
  `audit/img/` (dựng lại bằng `pata_audit.py build`), gói `_bundles/*.zip`
