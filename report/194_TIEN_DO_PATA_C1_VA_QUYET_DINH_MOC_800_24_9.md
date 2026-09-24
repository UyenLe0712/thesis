# 194 — TIẾN ĐỘ PATA-C1 (23–24/9/2026) VÀ QUYẾT ĐỊNH CÒN TREO Ở MỐC 800

> **Tự chứa.** Viết 24/9 ~18:30 VN để một phiên khác đọc rồi quyết **A (dừng C1) hay B (chạy hết epoch)**
> mà không cần hỏi lại. Nhãn: **[đo]** = số chạy ra từ mã/log · **[suy]** = ước lượng.
> Spec: `report/185` (chép từ 9 ảnh) · quyết định KL box lớn: `report/193` · nhật ký chi tiết từng
> bước: `report/186` §3.1–3.14. Runbook: `harness/colab_pata_c1.md` (Colab) ·
> `harness/kaggle_pata_test.md` (Kaggle test/smoke) · `harness/kaggle_pata_cham_val600.md` (chấm P10).

---

## 0. Tóm tắt một bảng

| mục | trạng thái 24/9 18:30 VN |
|---|---|
| phương pháp | PATA-Causal C1: TARGET token + localizer (KL multi-patch) + bridge cộng vào hidden state của TARGET sau block 17 |
| chuỗi train | **S (1 epoch, user chốt) → H (1 epoch) → C1 = J bridge bật (1 epoch)**; C0-Loc chưa chạy, chỉ chạy nếu C1 qua cổng §8 |
| Stage S | ✅ xong · CE_val(val400) **0,7295** |
| Stage H | ✅ xong · **cổng H ĐẠT** rõ (§4) |
| C1 | ▶️ **đang chạy trên A100**, qua update 800/2.512, ~8,1 s/update, dự kiến xong **~22:00 VN 24/9** |
| mốc 800 | **3/4 tiêu chí đạt; tiêu chí 2 (tắt bridge làm ≥ 30% câu probe đổi) KHÔNG đạt: 6/40 = 15%** |
| quyết định treo | **A dừng C1 ngay · B chạy hết epoch rồi đọc cổng cuối §8** (§6) |
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
| P10 | `kaggle_pata_cham_val600.md` Q0–Q4 (upload `thesis_pata_kaggle.zip` mới + dataset preds) | ~2–2,5 h T4×2, 0 đồng | 5 tệp `score_*_raw.jsonl` |
| đọc cổng | `~/.venvs/thesis/bin/python harness/pata_cong_c1.py --dir runs/pata/cong_c1` | vài giây, CPU | `cong_c1.json` + ĐẠT/KHÔNG |

**Ngưỡng cổng cuối đã khoá trong `pata_cong_c1.py` (24/9 ~13:00, trước khi C1 train):** (1) hợp lệ ≥ 99%,
độ dài ≤ 1,5× S, rỗng ≤ S + 1 điểm · (2) CE_val(J) ≤ 1,25× CE_val(S), KL_val(J) ≤ 1,10× KL_val(H), ba cận
dưới 90% > 0 · (3) exec(C1) ≥ exec(S) · (4) exec(C1 bật) > exec(C1 tắt) · (5) cận dưới 90% của
P(về D | ép D) − P(về D | ép R) > 0 (546 bước; D = hộp cùng cỡ vàng tại điểm `desc_neg` — xấp xỉ).
Đạt cả 5 ⇒ được chạy C0-Loc từ đúng `H/final` (sha `6fc0d6a63059…`), cùng mọi thứ, chỉ `--no-bridge`.

## 8. Nếu chọn A
`pkill -f harness/pata_train.py` trong Terminal Colab; P5 in "đã kết thúc" và đẩy điểm lưu cuối lên Drive.
Ghi kết luận "futility under budget tại mốc 800 (§7b điều 2: 6/40 = 15% < 30%)" vào `report/186`; **không**
kết luận "bridge vô ích" (§8). Không P9/P10.

---

## 9. Trạng thái máy và tệp
- Colab A100 đang chạy C1 (PID tiến trình train 29880 lúc khởi động J; P5 theo dõi, đồng bộ Drive 5 phút/lần,
  Drive giữ 2 điểm lưu mới nhất + `ckpt-00800` + `final`).
- Drive `MyDrive/thesis/pata_ck/`: `S/final` · `H/final` · `J/ckpt-00800` + 2 điểm lưu mới nhất ·
  `eval/diag_final_val400.json` (S, bản gốc P6) · `cong_c1/diag_S_val400.json`, `diag_H_val400.json`,
  `diag_H_val400_rows.jsonl` · `eval_m800/` (diag + preds probe40 của mốc 800).
- Kho: mọi mã + runbook đã push; commit gần nhất của đợt này `f0d87e1` (report/186 §3.14).
- Gói: `_bundles/thesis_pata_colab.zip` và `_bundles/thesis_pata_kaggle.zip` dựng ở `8c0e869` (có swap,
  `--tag`, P10).
