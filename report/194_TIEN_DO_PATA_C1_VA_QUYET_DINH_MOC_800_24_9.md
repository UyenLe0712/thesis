# 194 — TIẾN ĐỘ PATA-C1 (23–24/9/2026) VÀ QUYẾT ĐỊNH CÒN TREO Ở MỐC 800

> **Tự chứa.** ⛔ **CẬP NHẬT 25/9: cổng cuối đã đọc — KHÔNG ĐẠT (§5c). Mục 6–8 chỉ còn giá trị lịch sử.** Viết 24/9 ~18:30 VN để một phiên khác đọc rồi quyết **A (dừng C1) hay B (chạy hết epoch)**
> mà không cần hỏi lại. Nhãn: **[đo]** = số chạy ra từ mã/log · **[suy]** = ước lượng.
> Spec: `report/185` (chép từ 9 ảnh) · quyết định KL box lớn: `report/193` · nhật ký chi tiết từng
> bước: `report/186` §3.1–3.14. Runbook: `harness/colab_pata_c1.md` (Colab) ·
> `harness/kaggle_pata_test.md` (Kaggle test/smoke) · `harness/kaggle_pata_cham_val600.md` (chấm P10).

---

## 0. Tóm tắt một bảng

| mục | trạng thái 25/9 ~01:40 VN (cập nhật từ bản 18:30) |
|---|---|
| phương pháp | PATA-Causal C1: TARGET token + localizer (KL multi-patch) + bridge cộng vào hidden state của TARGET sau block 17 |
| chuỗi train | **S (1 epoch, user chốt) → H (1 epoch) → C1 = J bridge bật (1 epoch)**; C0-Loc chưa chạy, chỉ chạy nếu C1 qua cổng §8 |
| Stage S | ✅ xong · CE_val(val400) **0,7295** |
| Stage H | ✅ xong · **cổng H ĐẠT** rõ (§4) |
| C1 | ✅ **chạy hết epoch** (2.512/2.512 update, ~22:05 VN 24/9) · `J/final` adapter sha `ac0885903d19…` · P9 xong (§5b) |
| mốc 800 | **3/4 tiêu chí đạt; tiêu chí 2 (tắt bridge làm ≥ 30% câu probe đổi) KHÔNG đạt: 6/40 = 15%** |
| **CỔNG CUỐI C1** | ⛔ **KHÔNG ĐẠT** (đk 5 trượt; đk 3, 4 chỉ đạt theo ước lượng điểm, KTC phủ 0) ⇒ **dừng: không chạy C0-Loc, không mở test**, kết luận *futility under budget* (§5c) |
| quyết định treo ở mốc 800 | hết hiệu lực: C1 đã chạy hết (thực tế là B) và cổng cuối đã đọc |
| GPU đã tiêu | A100 Colab: S (~6 h tổng, gồm phần chạy chậm trước khi vá) + H (~4 h) + C1 tới u800 (~2 h) · Kaggle T4 miễn phí ~2 h |

⚠️ **C1 vẫn chạy trong lúc chờ quyết** — mỗi giờ trì hoãn ≈ 450 update ≈ 1 giờ A100. Chọn A thì dừng càng
sớm càng đỡ tốn.

---

## 1. Spec và các quyết định đã chốt

**Spec `report/185`** (C1 PATA-Causal, bản rút gọn để triển khai):
- Backbone `Qwen/Qwen2.5-VL-3B-Instruct`, QLoRA NF4, BF16 compute, tháp thị giác đóng băng. Đầu vào:
  ảnh + goal + 3 bước lịch sử (câu chuẩn) + 24 dòng OCR. Đầu ra: một câu tiếng Anh.
- Assistant turn: `<TARGET>` được ép trước câu, nhãn −100, bị bỏ trước khi chấm.
- Localizer sau block 17: `q = Pq(LN(hT))`, `u_i = Pv(LN(v_i))`, `α = softmax(q·u/√d)`;
  bridge: `hT' = hT + sigmoid(g)·Wo(Σ α_i v_i)`, `Wo = 0`, `g = −2` lúc khởi tạo; thay hT bằng hT' rồi chạy
  block 18–35. Loss J: `mean(CE câu) + 1,0 · mean(KL(p_target‖α) trên bước có box)`.
- Ba chặng S (CE) → H (KL, backbone + LoRA đóng băng) → J (CE + KL, LoRA + localizer lr 2e−5, bridge
  lr 1e−4). **C1 − C0-Loc** (C0 = J với bridge tắt, cùng mọi thứ khác) là phép so duy nhất quy công cho
  bridge. C1 chạy một mình **không** chứng minh phương pháp tốt hơn; chỉ được nói "qua/không qua cổng
  futility".

**Quyết định của user trong đợt này:**
1. **Stage S chỉ 1 epoch** (spec ghi 2) — hệ quả: điều kiện 3 cổng §8 vẫn so đúng (C1 so với chính S
   của lượt này), nhưng S/C1 không so thẳng được với S1 cũ (2 epoch, học cả val).
2. **C1 trước; C0-Loc chỉ khi C1 tốt.**
3. **Tắt KL khi box phủ ≥ 50% màn, CE giữ** (`report/193`, thay đề xuất 0,25 của 186 — 10/18 lỗi đến từ
   mẫu lấy dư nên không được nhân với 883; ba ngưỡng bắt cùng số lỗi ⇒ chọn ngưỡng bảo thủ).
4. Chạy S trên L4 trước rồi chuyển A100 khi có máy; giữ cỡ lô hiệu dụng 16.

---

## 2. Chặng chuẩn bị (0 GPU, WSL) — [đo]

### 2.1 Dữ liệu (`harness/pata_data.py`)
| tập | bước chạm | có box | tắt KL vì box ≥ 0,50 | **kl_ok** | SHA-256 (16 đầu) |
|---|---|---|---|---|---|
| train_proper (từ `train_tru_val`) | 40.189 | 40.089 | 657 | **39.432** | `05d69b55c30ef4a6` |
| val400 | 400 | 400 | 2 | 398 | `1ea4c587ebb12663` |
| val600 | 602 | 601 | 14 | 587 | `2d7dfba02909ce83` |
| probe40 (từ val400, khoá) | 40 | 40 | 0 | 40 | `6c23c1898d85a0fd` |
- Thiếu box 100 bước = 91 không có descriptor + 9 điểm chạm vượt khung ảnh khai báo (KL tắt, CE giữ).
  117/41.099 box a11y thò ra ngoài màn ⇒ cắt vào khung ảnh.
- Ba tập rời nhau theo episode · (episode, step) · ảnh/OCR (assert).

### 2.2 Audit box (người gán: Uyên, 264/264 mẫu; `harness/pata_audit.py`)
- Tầng ngẫu nhiên U: **lỗi nặng 4/148 = 2,7%**, Wilson95 [1,1; 6,7] < ngưỡng khoá 5% ⇒ giữ box.
- Lỗi dồn vào box rất lớn (≥ 0,25 màn: 10/18 trong mẫu lấy dư; mọi lỗi stale ở box ≥ 0,5).
- Hạn chế phải khai: chỉ một người gán (chưa có κ/adjudication); ước lượng trên 8/76 shard có ảnh.

### 2.3 Mã (tất cả trong `harness/`)
`pata_data.py` · `pata_model.py` (TARGET, localizer, bridge qua forward hook trên block 17, đích patch,
KL, `load_base`, `enable_gc`) · `pata_train.py` (S/H/J, nối tiếp, cắt gradient theo nhóm) ·
`pata_eval.py` (`diag` cổng H/mốc 800; `gen` on/off/swapD/swapR, `--tag`) · `pata_test.py` (14 unit test) ·
`pata_audit.py` · `pata_swap.py` · `pata_cong_c1.py` (đọc cổng cuối, ngưỡng khoá) · `pata_profile.py`.

### 2.4 Unit test
- **14/14 ĐẠT** trên mô hình tí hon CPU; **13/13 ĐẠT trên 3B thật** (Kaggle T4, trước khi thêm test 14).
  Trên 3B: Wo = 0 ⇒ logits bật = tắt bridge (Δ = 0); tiền tố trước TARGET không đổi khi bật bridge (Δ = 0);
  teacher-forced = KV-cache (Δ 5,9e−2 trên 6 bước, FP16); save/reload Δ = 0, câu trùng; overfit 8 mẫu:
  CE 1,99 → 0,03 · KL 3,80 → 0,09 · mass 0,08 → 0,98.
- Test 14 (tí hon): ép α (swap) đổi hậu tố, không đổi tiền tố; ép đúng α tự sinh = không ép (Δ = 0).

---

## 3. Sự cố kỹ thuật đã gặp và cách xử (quan trọng để tin số)

| sự cố | phát hiện | xử lý | ảnh hưởng tới kết quả |
|---|---|---|---|
| OOM test 10 trên T4 | Kaggle lượt 1 | logits về CPU trong test | chỉ ở test |
| **gradient TARGET 300–2.200 làm tê các nhóm khác** (cắt gradient theo tổng chung) | log smoke | tách TARGET thành nhóm, cắt 1,0 **theo từng nhóm** | trước mọi lượt thật |
| `make_item` dựng đích KL theo `box` chứ không theo `kl_ok` | khi thi hành luật 0,50 | sửa theo `kl_ok` | trước mọi lượt thật |
| TARGET làm lệch speaker S (CE 1,12 → 2,36 khi chèn TARGET) | smoke | không phải lỗi mã; J hồi nhanh | tính chất của thiết kế, cả C1 và C0 đều chịu |
| A100 chậm 23,9 s/u (S1 cũ 10,3); lô 16×1 không nhanh hơn 4×4 | log A100 | — | — |
| **tháp thị giác bị kéo vào đồ thị gradient** bởi `enable_input_require_grads` (transformers gọi trong `gradient_checkpointing_enable`) — backward 2× forward, 4.748 lời gọi backward attention/bước | Kaggle profile K9 | gỡ hook ở tháp thị giác, giữ ở embedding ngôn ngữ | **tương đương**: tí hon Δ gradient = 0,0/41.345 phần tử; 3B thật: CE trùng, chuẩn gradient LoRA 4,9754 vs 4,9758. A100 23,9 → **8,0 s/u** |
| VM Colab mới thiếu `libnvrtc-builtins.so.13.0` (torch 2.11 cu130) | S khởi động lỗi | `LD_LIBRARY_PATH` trỏ `nvidia/cu13/lib`; P1 tự kiểm | môi trường |
| mất máy 1 lần giữa S | — | nối tiếp từ ckpt Drive | mất ≤ 40 phút |
| S, H, J đều tên thư mục `final` ⇒ `pata_eval` đè tệp | khi viết cổng cuối | cờ `--tag` | trước khi có số |

**Phải khai trong manifest §11:** S update 1–100 lô 4×4, từ 101 lô 16×1 (tương đương toán học; CPU: CE
update kế trùng 6 chữ số) · S update 1–1.500 có gradient thừa qua tháp thị giác, từ 1.501 không (tương
đương về phép toán) · S từ update 1.101 chạy trên VM torch 2.11 cu130 / Python 3.13 · H, C1 chạy trọn bản đã
vá, lô 16×1. Lựa chọn của phiên thi hành (spec không nói): d_k = 2048 · gate một vô hướng · clip 1,0 theo
nhóm · NF4 double-quant · CE chuẩn hoá theo token trên lô hiệu dụng · KL chia số mẫu có box trong lô.

---

## 4. Kết quả S và H — [đo]

- **S:** `S/final/adapter_model.safetensors` sha `da6484273196…`. **CE_val(val400) = 0,7295.**
- **H:** 39.432 mẫu, 2.465 update, 8.402.944 tham số học (LoRA đóng băng; adapter giữ nguyên sha của S).
  `H/final/pata_heads.pt` sha `6fc0d6a63059…`.
- **Cổng H trên val400 (n = 400; 398 bước có đích KL) — ĐẠT:**

| | localizer H | center prior | train-location prior | prompt xáo |
|---|---|---|---|---|
| mass trong box | **0,184** | 0,036 | 0,039 | 0,107 |
| Hit-in-box | **38,7%** | 5,3% | 5,3% | 21,9% |

  KL_val 2,580. Cận dưới 90% một phía: lift so center **+0,133** · so train prior **+0,131** · đúng − xáo
  **+0,067** (ở smoke 20 update vế này bằng 0).

---

## 5. C1 (Stage J, bridge bật) tới mốc 800 — [đo]

### 5.1 Log train (P5)
| update | CE | KL | mass (train) | gate = sigmoid(g) | resid = ‖Wo z‖/‖hT‖ |
|---|---|---|---|---|---|
| 2 | 1,27 | 2,88 | 0,13 | 0,11920 | 0,000 |
| 20 | 1,07 | 2,59 | 0,18 | 0,11923 | 0,008 |
| 40 | 0,71 | 2,43 | 0,21 | 0,11931 | 0,031 |
| 80 | 0,66 | 2,39 | 0,24 | 0,11940 | 0,067 |
| 120 | 0,60 | 2,39 | 0,24 | 0,11946 | 0,074 |
~8,1 s/update, VRAM ~15 GB. (Log u120–u800 nằm ở `pata_ck/J/train_log.jsonl` và `/content/pata_J.log`.)

### 5.2 Mốc 800 (P8: `J/ckpt-00800`)
**Teacher-forced val400:**
| | mốc 800 | so với |
|---|---|---|
| CE_val | **0,742** | S 0,730 |
| KL_val | **2,330** | H 2,580 |
| mass trong box | **0,241** | H 0,184 |
| Hit-in-box | **46,7%** | H 38,7% |
| mass prompt xáo | 0,108 | — |
| lift center / train (cận dưới 90%) | +0,185 / +0,183 | H +0,133 / +0,131 |
| đúng − xáo (cận dưới 90%) | **+0,117** | H +0,067 |

**Sinh câu probe 40:** format hợp lệ bật **40/40 = 100%** (độ dài TB 8,0 từ) · tắt 39/40 = 97,5% (7,7 từ) ·
**câu ĐỔI khi tắt bridge: 6/40 = 15,0%**.
Tệp để soi từng câu: `MyDrive/thesis/pata_ck/eval_m800/preds_J800_probe40_on.jsonl` và `…_off.jsonl`
(+ `diag_J800_val400.json`).

### 5.3 Đối chiếu bốn tiêu chí mốc 800 (§7b)
| tiêu chí | kết quả | |
|---|---|---|
| 1. CE_val, KL_val không phân kỳ | 0,742 (S 0,730) · 2,33 (H 2,58) | ✅ |
| 2. tắt bridge ⇒ ≥ 30% câu probe đổi | **15,0%** (6/40) | ❌ |
| 3. xáo prompt ⇒ mass giảm | 0,241 → 0,108 | ✅ |
| 4. format hợp lệ ≥ 95% | 100% | ✅ |
Tín hiệu rẻ của §7b ("`sigmoid(g)` kẹt ~0 **và** `‖Wo z‖/‖hT‖` ~0 ⇒ bridge không mở"): gate 0,119 (không ~0),
resid ~0,07 và đang tăng (không ~0) ⇒ **không** rơi vào dấu hiệu "bridge không mở".

**Thống kê của 6/40:** Clopper–Pearson 95% **[5,7%; 29,8%]** · P(X ≤ 6 | tỉ lệ thật 30%) = **0,024** ⇒ dữ
liệu **bác được** "tỉ lệ thật ≥ 30%" ở mức 5% · P(X ≥ 6 | tỉ lệ thật 5%) = 0,014 ⇒ cũng **bác được** "gần như
không đổi (≤ 5%)". Kết luận thống kê: bridge **được dùng, nhưng yếu hơn ngưỡng 30%**.

---

## 5b. C1 hết epoch + P9 (24/9 tối) — [đo]

**Train:** hết 2.512/2.512 update, không NaN/OOM, ~8,2 s/u, VRAM 16,67 GB. Mất máy **sau** khi P5 kết thúc:
ô R0 (runbook) kiểm `J/final` trên Drive theo `final_sha256.json` ⇒ khớp 5/5 tệp, không phải train lại.
SHA `J/final` (bản đủ ở `runs/pata/J_final_sha256.json`): adapter `ac0885903d19…` · `pata_heads.pt`
`b773373afa20…` · `meta.json` `6c989439b1fd…` · `adapter_config.json` `da0d95e635a2…`.

| log train | CE | KL | mass (train) | gate = sigmoid(g) | resid |
|---|---|---|---|---|---|
| u2200 | 0,661 | 2,05 | 0,30 | 0,12040 | 0,196 |
| u2240 | 0,664 | 2,03 | 0,32 | 0,12041 | 0,195 |

⚠️ `gate` gần như đứng yên cả epoch (0,11920 → 0,12041) trong khi `resid` lên ~0,20 ⇒ độ lớn bridge đến từ
`Wo` lớn dần, không phải từ cổng mở.

**Chẩn đoán J/final trên val400 (`diag_J_val400.json`):**

| | S | H | mốc 800 | **J/final** |
|---|---|---|---|---|
| CE_val | 0,72950 | — | 0,742 | **0,72954** |
| KL_val | — | 2,580 | 2,330 | **2,170** |
| mass trong box | — | 0,184 | 0,241 | **0,277** |
| Hit-in-box | — | 38,7% | 46,7% | **52,0%** |
| mass prompt xáo | — | 0,107 | 0,108 | 0,115 |
| lift center / train, cận dưới 90% | — | +0,133 / +0,131 | +0,185 / +0,183 | **+0,220 / +0,218** |
| đúng − xáo, cận dưới 90% | — | +0,067 | +0,117 | **+0,145** |

(CE_val J trùng S tới 4 chữ số: đã so số đủ, 0,7295419 vs 0,7295007 — hai phép đo khác nhau, không phải đọc
nhầm tệp; mass J khác H nên đầu localizer nạp đúng.)

**P9 — 5 tệp preds val600** (`runs/pata/cong_c1/`, kiểm trên WSL: 0 dòng trùng, khoá bước khớp đúng
`val600.jsonl`/`val600_swap.jsonl`, câu chuẩn khớp, `ckpt` đúng J/final hoặc S/final):

| biến thể | n | hợp lệ | độ dài TB (từ) | rỗng | câu khác so với C1 on |
|---|---|---|---|---|---|
| C1 on | 602 | 100% | 8,25 | 0 | — |
| C1 off (tắt bridge) | 602 | 99,3% | 8,12 | 4 | **90/602 = 15,0%** (Wilson 95% [12,3; 18,0]) |
| C1 swapD | 546 | 100% | 8,22 | 0 | 38/546 = 7,0% |
| C1 swapR | 546 | 100% | 8,24 | 0 | 35/546 = 6,4% |
| S on | 602 | 100% | 8,41 | 0 | 213/602 = 35,4% |

- **Tắt bridge trên val600 tái lập đúng 15% của probe 40** (6/40), nay với n = 602: mép trên KTC 18,0% < 30%
  (P(X ≤ 90 | 30%) ≈ 6·10⁻¹⁸) và mép dưới 12,3% > 5%. Kết luận §5.3 đứng: bridge **được dùng nhưng yếu**.
  ⚠️ Đây là val600 (tập cổng cuối), đo đúng một lần trong P9 theo runbook — không phải phép C của §6.2.
- **swapD vs swapR chỉ khác câu ở 39/546 = 7,1%.** Bộ trỏ tất định ⇒ ở 507 bước câu trùng, hiệu của đk 5
  bằng 0 ⇒ chênh "về phía D" **tối đa 7,1 điểm %**; đk 5 còn đạt được nếu 39 bước ấy nghiêng về D, nhưng biên
  mỏng. [suy]

**Cổng cuối — phần đã đọc được (ngưỡng khoá trong `pata_cong_c1.py`):**

| đk | tiêu chí | số | |
|---|---|---|---|
| 1 | hợp lệ ≥ 99% · dài ≤ 1,5× S · rỗng ≤ S + 1 điểm | 100% · 8,25 vs 8,41 · 0 vs 0 | ✅ |
| 2 | CE ≤ 1,25× S · KL ≤ 1,10× H · 3 cận dưới > 0 | 0,7295 ≤ 0,912 · 2,170 ≤ 2,838 · +0,220/+0,218/+0,145 | ✅ |
| 3 | exec(C1) ≥ exec(S) | xem §5c | ✅ (điểm) |
| 4 | exec(C1 bật) > exec(C1 tắt) | xem §5c | ✅ (điểm) |
| 5 | cận dưới 90% P(về D\|ép D) − P(về D\|ép R) > 0 | xem §5c | ❌ |

**P10 (Kaggle):** ô Q2 của `harness/kaggle_pata_cham_val600.md` **đã sửa 24/9 tối** trước khi chạy — bản cũ
tìm `ocr_val.jsonl` (dataset `thesis-val-cham` chỉ có `ocr.jsonl`) và lấy thư mục ảnh từ `.png` đầu tiên sau
sắp xếp, tức thư mục 440 ảnh của `thesis-pata` (đứng trước `thesis-val-cham` theo tên). Bản mới lấy mọi thứ
theo thư mục của `val_cham600.jsonl` và kiểm đủ ảnh cho 602 bước. ⛔ Dataset `thesis-val` cũ không thay được
(không có `val_cham600.jsonl`, chỉ phủ 391/602 ảnh). Dataset `thesis-pata` cũ dùng được (`score_run.py` không
đổi từ 14/9).

---

## 5c. CỔNG CUỐI C1 — KẾT QUẢ (P10 Kaggle T4×2, xong 25/9 ~01:30 VN) — [đo]

Chấm bằng UGround-V1-2B, luật `exec` (Voronoi ∧ ±14%), trên 602 bước chạm val600 (swap: 546). Tệp thô ở
`runs/pata/cong_c1/score_*_raw.jsonl`, log ở `runs/pata/cong_c1/log/`, kết quả máy đọc ở
`runs/pata/cong_c1/cong_c1.json`. Kiểm: đủ 602/602/602/546/546 dòng, 0 bước `n_buttons = 0` (cây trợ năng tải
đủ), 4 dòng `bo_qua: câu rỗng` của C1 off tính `exec = 0`, hai log không có Traceback.

| biến thể | exec | KTC95 (bootstrap cụm) | `action_ok` |
|---|---|---|---|
| **C1 bật bridge** | **61,13%** (368/602) | [56,97; 65,17] | 597 |
| C1 tắt bridge | 60,96% (367/602) | [56,90; 64,91] | 594 |
| S (không PATA) | 60,13% (362/602) | [55,94; 64,32] | 598 |
| C1 ép D | 61,54% (336/546) | [57,26; 65,71] | 542 |
| C1 ép R | 60,81% (332/546) | [56,57; 64,91] | 542 |

`pata_cong_c1.py --dir runs/pata/cong_c1` (ngưỡng khoá 24/9 trước khi C1 train):

| đk | tiêu chí | số | kết quả |
|---|---|---|---|
| 1 | hợp lệ ≥ 99% · dài ≤ 1,5× S · rỗng ≤ S + 1 điểm | 100% · 8,25 vs 8,41 · 0 vs 0 | ✅ |
| 2 | CE, KL không phân kỳ + 3 cận dưới > 0 | 0,7295 vs S 0,7295 · 2,170 vs H 2,580 · +0,220/+0,218/+0,145 | ✅ |
| 3 | exec(C1) ≥ exec(S) | **+1,00 điểm**, KTC95 [−1,74; +4,02], C1 hơn 26 / kém 20 bước, McNemar p = 0,46 | ✅ theo điểm, **không có ý nghĩa** |
| 4 | exec(C1 bật) > exec(C1 tắt) | **+0,17 điểm**, KTC95 [−1,03; +1,33], 8 / 7 bước, p = 1,0 | ✅ theo điểm, **bằng nhiễu** |
| 5 | cận dưới 90% [P(về D\|ép D) − P(về D\|ép R)] > 0 | 18,32% − 18,68% = **−0,37 điểm**, cận dưới 90% −0,86, KTC95 [−1,13; +0,33] | ❌ |

⇒ **CỔNG C1: KHÔNG ĐẠT.** Theo §8: dừng, không chạy C0-Loc, không mở test, kết luận *futility under budget*.

**Đọc cơ chế (vì sao trượt):**
- Localizer **học được vị trí thật**: hit-in-box 52,0% so với 5,3% của hai prior, xáo prompt làm mass giảm
  0,277 → 0,115 (§5b). Phần "nhìn đúng chỗ" của PATA hoạt động.
- Nhưng **bộ sinh câu gần như không nghe bridge**: tắt bridge chỉ đổi 15% câu, và trong số câu đổi, `exec`
  gần như không đổi (8 bước lên / 7 bước xuống). Ép α sang hộp nhiễu D chỉ làm câu khác ép R ở 39/546 bước;
  trong 39 bước đó, số câu trỏ về phía D là **6 khi ép D so với 8 khi ép R** — ngược chiều mong đợi. Tức
  nội dung câu **không đi theo** vị trí mà bridge đưa vào.
- `gate` đứng yên cả epoch (0,1192 → 0,1204) trong khi `resid` ~0,20: bridge đưa tín hiệu vào hidden state,
  nhưng decoder dùng nó như nhiễu nhỏ chứ không như thông tin vị trí.
- +1,0 điểm của C1 so với S (dưới ý nghĩa) nhiều khả năng đến từ **một epoch dạy thêm** (J tiếp tục CE trên
  cùng tập) chứ không từ bridge: tắt bridge vẫn giữ 60,96%, tức 83% phần hơn S còn nguyên khi không có bridge.

⚠️ Số val600 **không trích ra báo** như điểm của phương pháp (val là tập chọn/cổng, luật đọc val ở CLAUDE.md).
Luận văn chỉ được báo: cổng H đạt (localizer học vị trí), cổng cuối không đạt vì bridge không truyền vị trí
vào câu — một kết quả âm có cơ chế.

---

## 6. QUYẾT ĐỊNH CÒN TREO

### 6.1 Chỗ spec tự mâu thuẫn (trích nguyên văn `185`)
- **§7b, mốc 800, điều 2:** *"Disable bridge trên cùng probe 40: ≥ 30% câu phải đổi (không tính strip
  TARGET). Nếu gần như không đổi → decoder bỏ qua bridge → **dừng**, không tốn hết epoch."* và *"Nếu 1–4
  đạt: chạy hết 1 epoch."*
- **§8, mốc update 800:** *"**Chỉ được dừng vì lỗi kỹ thuật:** … bridge disable/swap **không làm output thay
  đổi** …"* và *"Nếu không có lỗi thảm họa, chạy hết một epoch."*
⇒ 15% **không đạt** ngưỡng số của §7b, nhưng **không phải** "gần như không đổi" / "không làm output thay
đổi" (thống kê bác cả ≤ 5%). Hai cách đọc cho hai hành động khác nhau.

### 6.2 Ba lựa chọn
| | làm gì | giá thêm | được gì | rủi ro / phải khai |
|---|---|---|---|---|
| **A** | dừng C1 ngay (`pkill -f harness/pata_train.py` trong Terminal Colab) | 0 (tiết kiệm ~3,5 h A100 + ~1 h P9) | kết luận "futility tại mốc 800: bridge được dùng yếu (15% < 30%)" | **không có `exec` nào của C1**; luận văn chỉ có chẩn đoán localizer (cổng H, mốc 800), không có số đầu ra |
| **B** | để chạy hết (xong ~22:00 VN) → P9 sinh câu val600 (C1 on/off/swapD/swapR + S) → P10 chấm Kaggle → `pata_cong_c1.py` | ~3,5 h A100 còn lại + ~1–1,5 h A100 P9 + ~2–2,5 h Kaggle T4 (0 đồng) | cổng cuối đo **trực tiếp** bridge bằng `exec` trên 602 bước (đk 4: bật > tắt) và C1 vs S (đk 3), cộng swap D/R (đk 5) | phải khai "15% < 30% ở §7b, chạy tiếp theo luật dừng §8"; nếu cổng cuối trượt vẫn là kết quả báo được |
| **C** (tuỳ chọn trước khi quyết) | đo tỉ lệ câu đổi khi tắt bridge trên **val400 đủ 400 bước** (tập chẩn đoán thường xuyên theo §3, không phải val600) bằng `J/ckpt-00800`, chạy song song trong Terminal | ~15–20 phút A100 (train chậm lại trong lúc đó) | ước lượng chặt hơn nhiều so với 40 bước | là phép đo **thêm sau khi thấy** 6/40 — chỉ để thông tin, phải khai; không dùng val600 |

Lệnh cho C (Terminal Colab, không Stop P5):
```
export LD_LIBRARY_PATH=/usr/local/lib/python3.13/dist-packages/nvidia/cu13/lib:$LD_LIBRARY_PATH
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True TQDM_DISABLE=1
cd /content/ws/thesis
python harness/pata_eval.py --ckpt /content/drive/MyDrive/thesis/pata_ck/J/ckpt-00800 --mode gen \
  --split val400 --variants on,off --tag J800 --bs 16 --data-root harness/dg1_cache/train_ac \
  --out /content/drive/MyDrive/thesis/pata_ck/eval_m800 > /content/m800_val400.log 2>&1
tail -5 /content/m800_val400.log
```
(`ckpt-00800` là mốc giữ vĩnh viễn trên Drive.)

### 6.3 Đề xuất của phiên này
**B** (có thể kèm C). Lý do: (i) §8 là mục "cổng" và chỉ cho dừng khi output **không** đổi — thống kê bác
"≤ 5%"; (ii) 40 bước quá nhỏ để quyết một mình (KTC 5,7–29,8%); (iii) tín hiệu §7b "gate/resid kẹt ~0"
không xảy ra; (iv) mọi chỉ số localizer ở mốc 800 đều tốt hơn lúc hết H; (v) chạy hết cho luận văn một
số `exec` thật của phương pháp, tốt hay xấu. Nếu ưu tiên tiết kiệm tuyệt đối thì A.
⚠️ Bất kể A hay B: **không** đổi λ, block, LR, gate init (§8); **không** mở test; **không** suy `exec` từ
probe 40.

---

## 7. Nếu chọn B — các bước còn lại và ước giờ
| bước | ô / tệp | ước giờ | ra |
|---|---|---|---|
| C1 chạy hết | P5 đang chạy | tới ~22:00 VN | `pata_ck/J/final` |
| P9 | `colab_pata_c1.md` P9 (diag J + gen C1 4 biến thể + gen S) | ~1–1,5 h A100 | `pata_ck/cong_c1/`: `diag_J_val400.json` + 5 preds |
| P10 | `kaggle_pata_cham_val600.md` Q0–Q4 (dataset `thesis-pata` cũ + `thesis-val-cham` + `thesis-pata-preds` mới; ô Q2 bản sửa 24/9 tối) | ~2–2,5 h T4×2, 0 đồng | 5 tệp `score_*_raw.jsonl` |
| đọc cổng | `~/.venvs/thesis/bin/python harness/pata_cong_c1.py --dir runs/pata/cong_c1` | vài giây, CPU | `cong_c1.json` + ĐẠT/KHÔNG |

**Ngưỡng cổng cuối đã khoá trong `pata_cong_c1.py` (24/9 ~13:00, trước khi C1 train):** (1) hợp lệ ≥ 99%,
độ dài ≤ 1,5× S, rỗng ≤ S + 1 điểm · (2) CE_val(J) ≤ 1,25× CE_val(S), KL_val(J) ≤ 1,10× KL_val(H), ba cận
dưới 90% > 0 · (3) exec(C1) ≥ exec(S) · (4) exec(C1 bật) > exec(C1 tắt) · (5) cận dưới 90% của
P(về D | ép D) − P(về D | ép R) > 0 (546 bước; D = hộp cùng cỡ vàng tại điểm `desc_neg` — xấp xỉ).
Đạt cả 5 ⇒ được chạy C0-Loc từ đúng `H/final` (sha `6fc0d6a63059…`), cùng mọi thứ, chỉ `--no-bridge`.

### 7.1 Mất máy
- **Giữa C1:** P1 → P2 → P4 (`STAGE="J"`, `BS, ACCUM = "16", "1"`) → P5. P4 chép điểm lưu J mới nhất trên Drive
  về; kiểm `grep -E "nối tiếp|kế hoạch" /content/pata_J.log | tail -2` phải thấy `[nối tiếp] … update N/2512`.
  Mất ≤ 100 update (~14 phút) + ~15 phút dựng máy. `ckpt-00800` giữ vĩnh viễn trên Drive.
- **Giữa P9:** P1 → P2 → chạy lại ô P9 (tự nối tiếp từng biến thể). ⚠️ Phải dùng gói dựng **sau `561d620`**:
  `pata_eval gen` nay mở–ghi–đóng tệp từng lô (bản trước mở một lần cho cả biến thể ⇒ mất máy là mất trọn
  tệp trên Drive, bài học 24/8).
- **Giữa P10 (Kaggle):** chạy lại ô Q3; `score_run.py` đọc lại tệp thô, chỉ chấm phần thiếu.

## 8. Nếu chọn A
`pkill -f harness/pata_train.py` trong Terminal Colab; P5 in "đã kết thúc" và đẩy điểm lưu cuối lên Drive.
Ghi kết luận "futility under budget tại mốc 800 (§7b điều 2: 6/40 = 15% < 30%)" vào `report/186`; **không**
kết luận "bridge vô ích" (§8). Không P9/P10.

---

## 9. Trạng thái máy và tệp

**Cập nhật 24/9 23:30 VN:** Colab đã Disconnect sau P9. Drive `pata_ck/J/` có `ckpt-00800`, `ckpt-02500`,
`ckpt-02512`, `final`, `final_sha256.json`; `pata_ck/cong_c1/` có đủ 3 diag + 5 preds, bản sao ở `runs/pata/cong_c1/`.
Việc kế: Kaggle P10 → `pata_cong_c1.py`. Các dòng dưới là trạng thái lúc 18:30.

- Colab A100 đang chạy C1 (PID tiến trình train 29880 lúc khởi động J; P5 theo dõi, đồng bộ Drive 5 phút/lần,
  Drive giữ 2 điểm lưu mới nhất + `ckpt-00800` + `final`).
- Drive `MyDrive/thesis/pata_ck/`: `S/final` · `H/final` · `J/ckpt-00800` + 2 điểm lưu mới nhất ·
  `eval/diag_final_val400.json` (S, bản gốc P6) · `cong_c1/diag_S_val400.json`, `diag_H_val400.json`,
  `diag_H_val400_rows.jsonl` · `eval_m800/` (diag + preds probe40 của mốc 800).
- Kho: mọi mã + runbook đã push; commit gần nhất của đợt này `f0d87e1` (report/186 §3.14).
- Gói: `_bundles/thesis_pata_colab.zip` và `_bundles/thesis_pata_kaggle.zip` dựng ở `8c0e869` (có swap,
  `--tag`, P10).
