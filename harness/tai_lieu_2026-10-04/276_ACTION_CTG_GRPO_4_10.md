# 276 — VIỆC CẦN LÀM CHO CTG-GRPO (bản gọn, 4/10/2026)

Cho chat viết mã và chạy thí nghiệm. **Tự chứa: đủ để cài đặt, chạy và báo cáo mà không cần file khác.**

- Lý do chọn CTG, tiền lệ, debate, đánh giá đóng góp và các đề xuất khác nằm ở file `277_HO_SO_NEN_CTG_RESEARCH_DEBATE_DE_XUAT_KHAC_4_10.md`. Đó là hồ sơ nền, không cần để cài đặt.
- File này thay bản 276 dài trước đây. Bản dài được giữ nguyên trong file 277.
- **Hai việc agent không tự làm: không chạy `git` / `gh`; không tự thuê máy.**

## ⚙️ Đã thi hành 4/10 — mã, runbook, và năm chỗ kiểm lệch so với bản gốc

Tệp này trước nằm ở `harness/276_DEEP_RESEARCH_…_extracted.md`, chuyển về đây 4/10.

| việc | tệp |
|---|---|
| mã (r_cider · CTGTrainer · lưu/nạp `ctg_state.json` · `ctg_log.jsonl` · A4 · A7 · P0(b)) | `harness/ctg_grpo.py` |
| đọc val: K1/K2/K3, chọn điểm lưu, hình λ | `harness/ctg_doc.py` |
| P0 trên Kaggle T4 | `harness/kaggle_ctg_p0.md` |
| train A3/A2/A4/A7 trên Colab (kèm bước đo L4) | `harness/colab_ctg_train.md` |
| chấm val C1 các điểm lưu | `harness/kaggle_ctg_val.md` |
| gói upload | `_bundles/ctg-grpo-script/` |

Tự kiểm 0 GPU đã ĐẠT trên WSL: tái lập CIDEr-D **3.484/3.600 · 399/400**; selftest (thưởng, 2.000 câu nhắc,
A4, bốn phép kiểm CTG); `ctg_doc.py` tái lập S1 66/75 · exec 158/249, ck250 66/75 · 161, ck500 63/75 · 165;
CTGTrainer chạy với lớp TRL giả (A3 cộng, A2 không cộng). Chưa chạy trên GPU.

**Năm chỗ lệch:**
1. **Phụ lục A thiếu `'"'` trong `PUNCT`.** Chép đúng nguyên văn thì chỉ 3.407/3.600 · 397/400 (trượt tự
   kiểm). Thêm `'"'` (PTBTokenizer đổi `"` thành ``` `` ```/`''` rồi bỏ) thì ra đúng con số 3.484 · 399 mà
   bản gốc ghi ⇒ ký tự rơi lúc chép. Đã sửa trong mã.
2. **A7 ghi `R ← R − 1[canon(câu) = canon(chuẩn)]`, dấu trừ trái với tên "cộng loại".** Mã cài **dấu cộng**
   (hàm `r_loai`, thưởng +1 khi đúng loại). ⚠️ Cần user xác nhận trước khi chạy A7.
3. **`p_k` lấy trên 9 câu (greedy + 8 mẫu), không phải 8 mẫu.** Đo lại: 8 mẫu cho 0,828 · 0,804 · 0,725;
   9 câu cho đúng 0,837 · 0,813 · 0,733. Mã giữ nguyên số khoá trước.
4. **Điều kiện "canon_action(gold) nhận loại ≥ 99%" luôn đúng** vì `canon_action` không bao giờ trả rỗng
   (mặc định `tap`). Phép kiểm có nghĩa là khớp với `action_type`: 96,1% chung; scroll 241/248, back 72/73,
   nhưng **input_text chỉ 102/146** ⇒ CTG lớp `type` chỉ phủ ~70% bước nhập chữ (phần còn lại câu chuẩn
   quy về `tap`, CTG để yên). Lớp vàng trên 2.000 câu nhắc: tap 1.557 · scroll 242 · type 114 · back 84.
5. **File `277_HO_SO_NEN_…` không có trong kho** (tìm cả `report/` và `harness/`).

Luật P0(b) cụ thể hoá trước khi đo (bản gốc chỉ ghi "không tăng theo checkpoint"): đo log P(token đầu là
động từ chạm) trên 32 câu nhắc scroll của C1; **ĐẠT khi ck500 > S1 và ck250 ≥ S1 − 0,05**.

## 0. Tóm tắt một màn hình

| | |
|---|---|
| **Mô hình đề xuất (A3)** | GRPO trên S1/101 (Qwen2.5-VL-3B + LoRA), thưởng CIDEr-D + CTG, 1.000 bước, A100, seed 101 |
| **Ablation (A2)** | Như A3 nhưng tắt CTG |
| **Đối chứng (A4, A7)** | A4: lấy mẫu lại theo lớp (kiểu DISCO), 500 bước. A7: cộng loại toàn cục (kiểu Co-EPG), 500 bước |
| **Thứ tự** | Viết mã → P0 trên T4 → A3, A2 trên A100 → A4, A7 → chọn checkpoint trên val → chấm test trên T4 → UI-Venus → báo cáo |
| **Chi phí** | khoảng 23–33 giờ A100 (khoảng 30–65 USD) + khoảng 22 giờ T4 Kaggle |
| **CTG nâng gì** | scroll, back, nhập chữ (giữ không tụt dưới S1); không đụng click. Click tăng nhờ CIDEr-D (áp dụng, không phải đóng góp) |

## 1. CTG là gì

Với mỗi nhóm G = 8 câu sinh cho một câu nhắc có loại thao tác chuẩn g:

\[
A_i = z_G(R)_i + \mathbb{1}[g \in \{\text{scroll},\text{type},\text{navigate\_back}\}]\lambda_g\, z_G(c)_i, \qquad c_i = \mathbb{1}[\text{canon}(y_i) = g]
\]

\[
\hat c_g \leftarrow 0{,}8\,\hat c_g + 0{,}2\,\overline{c},\qquad
\lambda_g \leftarrow \mathrm{clip}\big(\lambda_g + 0{,}5(p_g - 0{,}01 - \hat c_g);0;3\big)
\]

- `z_G` là chuẩn hoá trong nhóm, đúng như TRL: trừ trung bình, chia std unbiased + `1e-4`.
- `λ_tap ≡ 0`, nên nhóm click giữ nguyên advantage gốc.
- `p_g` là đích, lấy bằng tỉ lệ đúng loại của S1 (mục 6).
- Ý nghĩa của cập nhật dual:
  - mô hình trôi khỏi đích thì λ tự tăng;
  - mô hình giữ được đích thì λ tự giảm về 0.

## 2. Mốc so sánh (TEST đã chốt, `report/262`)

| | S1/101 | ck500 (GRPO SPICE) | Δ [KTC95, cụm app] |
|---|---:|---:|---:|
| exec, 4.463 bước click | 59,11 | 60,65 | +1,55 [+0,80; +2,33] |
| ck500 so với GRPO-point (tiêu đề hiện hành 60,07) |  |  | +0,58, p = 0,31 |
| bước không chạm, 2.495 bước | 85,97 | 84,29 | −1,68 [−2,76; −0,62] |
| scroll (755) | 83,97 | 77,75 | −6,23 ⇒ rớt noharm (ngưỡng −3) |
| navigate_back (270) | 72,96 | 67,04 | −5,93 |
| input_text (494) | 81,58 | 79,55 | −2,02 |

**Mục tiêu của A3:**

- exec click cao hơn 60,07 có ý nghĩa;
- scroll Δ so với S1 ≥ −3.

**Dự báo (chưa train):** click test khoảng 62–64; xác suất vượt 60,07 có ý nghĩa khoảng 55–65%.

## 3. Đã kiểm và chưa chắc (0 GPU, trên val C1 400 bước)

| điều | trạng thái |
|---|---|
| GRPO đẩy rộng về câu tap ở các câu nhắc không-tap | SPICE +4,99 [+0,54; +9,69]; CIDEr-D +8,34 [+2,73; +13,67] (bootstrap theo episode) |
| CTG đối đầu lực đẩy | CIDEr-D, λ = 1: −5,76 [−14,58; +2,54]; λ = 0,5 chỉ +1,29 ⇒ λ khởi tạo 1,0, λ_max 3 |
| CIDEr-D tốt hơn SPICE để chọn câu | oracle exec 73,09 so với 68,67; xếp cặp đúng 86,0% so với 51,6% |
| Cắm CTG vào TRL 0.29.1 | Đã đọc mã thật: sửa `advantages` sau `super()._generate_and_score_completions` là đủ (mục 6) |
| Clip PPO không ảnh hưởng | `old_per_token_logps = None` (`num_iterations` 1, `steps_per_generation ≤ accum`) ⇒ tỉ số = 1 |
| Thưởng CIDEr-D Python thuần | Tái lập pycocoevalcap 3.484/3.600 câu trùng tuyệt đối; 0,5 ms mỗi lượt 16 câu |
| ck500 chưa bão hoà ở 500 | exec val 63,45 → 64,66 → 66,27 (S1, ck250, ck500) ⇒ chọn 1.000 bước |
| Trồi loại chỉ xuất hiện sau bước 250 | không-tap đúng loại val: S1 66/75, ck250 66/75, ck500 63/75 ⇒ đối chứng phải chạy ≥ 500 |
| Số test cuối | **CHƯA chắc**, chỉ train thật mới biết |
| Lấy chéo là nguyên nhân thật | **CHƯA chắc**, P0 kiểm trước khi tiêu tiền A100 |

## 4. Checklist theo thứ tự

1. **Viết mã (mục 5–7):**
   - `r_cider`;
   - `CTGTrainer`;
   - callback lưu và nạp `ctg_state.json`;
   - `ctg_log.jsonl`;
   - các assert;
   - bộ lấy mẫu lại cho A4;
   - cộng toàn cục cho A7.
2. **Tự kiểm 0 GPU ở máy nhà:** tái lập CIDEr-D đạt ≥ 3.480/3.600 câu trùng (mục 5).
3. **P0 trên T4 (mục 8):**
   - 20 bước A3 để kiểm mã, assert và log λ;
   - kiểm log-prob động từ chạm trên câu nhắc scroll với S1, ck250, ck500.
   - **Trượt thì dừng, báo người dùng.**
4. **Thuê A100 (người dùng làm).** Đo 20 bước đầu: trên 60 s/bước thì dừng và báo.
5. **Chạy A3 và A2, 1.000 bước, lưu mỗi 250 bước.** Áp luật dừng K1–K3.
6. **Chạy A4 và A7, 500 bước.**
7. **Chọn checkpoint trên val C1 (mục 8).** Test chỉ nhìn một lần.
8. **Chấm test trên T4 Kaggle cho A3 và A2 (đường chấm của ck500).** Sau đó chấm UI-Venus cho A3 và A2.
9. **Báo cáo theo mục 9.**

## 5. Thưởng CIDEr-D (`r_cider`, dùng cho A2, A3, A4, A7)

- **Công thức:** đúng `pycocoevalcap` CiderScorer: n = 4, σ = 6, clip, ×10.
  - df và N cố định, tính một lần từ toàn bộ câu chuẩn của `p1_train_rows.jsonl` (đủ mọi loại thao tác).
  - Không tính lại theo lô. Không gọi Java/PTBTokenizer lúc train.
- **Thưởng:**
  - R = CIDEr-D/10 − 0,02 · max(0, số từ câu sinh − số từ câu chuẩn − 3);
  - câu rỗng → 0;
  - giữ đúng `nwords` và `MU = 0.02` của `grpo_spice.py`.
- **Mã:** chép nguyên khối ở Phụ lục A.
- **Assert khi khởi động:**
  - câu trùng câu chuẩn ⇒ điểm > 0;
  - câu rỗng ⇒ 0;
  - `"Swipe up"` so với câu chuẩn `"Click on the search bar"` ⇒ < 0,05.
- **Tự kiểm tái lập (một lần, 0 GPU):**
  - Dùng `CiderD` với IDF từ 400 câu chuẩn C1 (`runs/c1/exec8/c1data/c1_recs.jsonl`, trường `gold_instruction`).
  - Chấm 9 câu S1 mỗi bước và so với cột `ciderD` của `runs/c1/exec8/metric_tung_cau.json`.
  - Phải có ≥ 3.480/3.600 câu trùng tuyệt đối (`|Δ| < 1e-6`) và ≥ 399/400 bước chọn cùng câu tốt nhất.
  - Phần lệch đã biết chỉ ở token có `@ . _` (email, tên tệp).

## 6. CTG trong TRL 0.29.1

`CTGTrainer(GRPOTrainer)` chỉ ghi đè một phương thức. Mã giả đã đối chiếu với mã TRL thật:

```text
_generate_and_score_completions(self, inputs):
    out = super()._generate_and_score_completions(inputs)      # advantages (B,) đã z-score theo nhóm
    G = self.num_generations; assert len(inputs) % G == 0
    txt = processing_class.batch_decode(out["completion_ids"], skip_special_tokens=True)
    với mỗi nhóm j = 0, G, 2G, …:
        assert mọi inputs[j..j+G-1]["key"] bằng nhau           # nhóm liền khối (RepeatSampler, rewards.view(-1, G))
        k = canon_action(inputs[j]["gold"], strict_back=True)   # lớp vàng từ CÂU CHUẨN, không dùng cột action_type
        nếu k ∉ {scroll, type, navigate_back}: bỏ qua            # λ_tap = 0
        c_i = 1[canon_action(txt_i, strict_back=True) == k]
        ĉ_k ← 0,8·ĉ_k + 0,2·mean(c)                              # chỉ cập nhật khi lớp k xuất hiện
        λ_k ← clip(λ_k + 0,5·(p_k − 0,01 − ĉ_k), 0, 3)
        nếu std(c) > 0:
            z = (c − mean(c)) / (std(c, unbiased=True) + 1e−4)  # cùng công thức std của TRL
            out["advantages"][nhóm j] += λ_k · z
        ghi log
```

- `_prepare_inputs` xáo và chia lô sau bước này, nên sửa ở đây là an toàn.
- `_compute_loss` nhận advantage dạng `(B,)`.
- `canon_action` nằm ở `harness/metric_exec.py`. Câu `"Open the X app"` quy về `tap`.

**Tham số (khoá trước):**

| tham số | giá trị |
|---|---|
| `p_k` (đích = tỉ lệ đúng loại của 8 mẫu S1 trên C1) | scroll 0,837 · type 0,813 · navigate_back 0,733 |
| `ĉ_k` khởi tạo | = `p_k` |
| `λ_k` khởi tạo | 1,0 |
| η | 0,5 |
| `λ_max` | 3 |
| δ | 0,01 |
| EMA | 0,8 |

**Bắt buộc:**

1. Lưu `{λ, ĉ}` vào `ctg_state.json` trong mỗi `checkpoint-*`, qua `TrainerCallback.on_save`, và nạp lại khi resume. Thiếu bước này thì λ âm thầm về giá trị khởi tạo.
2. Trước khi train:
   - `canon_action(gold)` nhận được loại cho ≥ 99% câu chuẩn của 2.000 câu nhắc;
   - in phân bố lớp vàng.
3. Log mỗi lượt sinh vào `ctg_log.jsonl`:
   - bước, lớp, λ, ĉ, `std(c) > 0`;
   - tổng advantage đặt lên câu tap trong nhóm (lực đẩy).
   - Ghi cả ở A2 (tính nhưng không cộng vào advantage), để so lực đẩy giữa A2 và A3.
4. Chỉ một tiến trình, một GPU. `process_slice` cắt advantage theo tiến trình.
5. Không đổi: `scale_rewards="group"`, `loss_type="dapo"`, β = 0,04, lr 1e-5, nhiệt độ 1,0.

## 7. Cấu hình các nhánh

Mọi nhánh: A100 40 GB, `bf16=True`, seed 101, `--n-prompt 2000`. `dung_hang` xáo bằng seed rồi cắt `[:2000]`, nên 1.000 câu đầu trùng tập của ck500. Batch như ck500:

- G = 8;
- `per_device_train_batch_size` 4, `gradient_accumulation_steps` 4;
- `steps_per_generation` 4, tức 2 câu nhắc mỗi lượt sinh.

| nhánh | thưởng | CTG | khác | `max_steps` | lưu mỗi |
|---|---|---|---|---:|---:|
| A3 | `r_cider` | bật, λ₀ = 1,0 | — | 1.000 | 250 |
| A2 | `r_cider` | tắt (vẫn log) | — | 1.000 | 250 |
| A4 | `r_cider` | tắt | nhân bản câu nhắc lớp scroll / type / navigate_back theo w = log(1 + 1/p_lớp) (p_lớp là tỉ phần lớp trong 2.000 câu nhắc), chuẩn hoá tổng = 2.000 | 500 | 250 |
| A7 | `r_cider` | tắt | R ← R − 1[canon(câu) = canon(chuẩn)] cho mọi câu nhắc | 500 | 250 |

**Tệp trong repo:**

- **Train:**
  - `harness/grpo_spice.py` (`train()`, `r_spice()`); runbook mẫu `harness/kaggle_grpo_spice_commit.md`.
  - Giữ nguyên `dung_hang()`, `remove_unused_columns=False`, và cách nạp lại adapter `default` khi resume.
- **Chấm test click:** `harness/kaggle_grpo_spice_test_ck500.md`, sau đó `harness/grpo_spice_test_doc.py`.
- **Chấm test không chạm:** `harness/kaggle_grpo_spice_nontap_ck500.md`, sau đó `harness/grpo_spice_nontap_doc.py`.

## 8. Luật (khoá trước khi chạy)

Val C1: 249 bước click (exec UGround) và 151 bước không chạm (đúng loại thao tác).

**Dừng:**

- **P0 (T4, trước khi thuê A100):**
  - (a) 20 bước A3 chạy được, assert qua, λ có log.
  - (b) Log-prob teacher-forced của câu `"Click on ..."` trên câu nhắc scroll (so với câu chuẩn scroll), đo với S1, ck250, ck500.
  - **Không tăng theo checkpoint ⇒ giả thuyết lấy chéo sai ⇒ dừng, báo người dùng.**
- **Tốc độ:** 20 bước đầu trên A100. Trên 60 s/bước thì dừng, báo.
- **K1 (bước 500):** tỉ lệ đúng loại không-tap C1 của A3 không cao hơn A2 ⇒ dừng A3.
- **K2 (bước 250, 500):** exec click C1 của A3 thấp hơn A2 quá 2,6 ⇒ dừng.
- **K3 (bất kỳ lúc nào):** dừng nếu gặp một trong:
  - câu rỗng > 1%;
  - số từ trung bình lệch > 30% so với S1;
  - một λ ở trần 3 liền hơn 100 lượt sinh;
  - KL gấp 3 lần ck500 ở cùng bước.

**Chọn checkpoint:**

- Mặc định checkpoint-1000.
- Lùi về checkpoint-500 chỉ khi exec click C1 ở 1.000 thấp hơn ở 500 quá 2,6.
- Cùng luật cho A2. Test nhìn **một lần** mỗi nhánh.

**Quyết định trên test (KTC ghép cặp theo cụm app; không trích số val):**

- **R-click:**
  - báo exec click A3 cùng KTC so với S1, ck500, 60,07;
  - chỉ nói "cao nhất có ý nghĩa" khi cận dưới KTC > 0;
  - in đủ 13 cột, đánh dấu CIDEr-D là "đã tối ưu trực tiếp".
- **R-CTG:**
  - A3 − A2 trên scroll có cận dưới KTC > 0;
  - A3 − A2 trên exec click có cận dưới > −1;
  - đúng loại không-tap trên val của A3 ≥ A4 và ≥ A7.
- **R-noharm:** scroll Δ của A3 so với S1 ≥ −3. Nếu A3 và A2 cùng trượt: CTG chưa đủ mạnh, báo thật, đề xuất tăng `λ_max`.
- **R-giữ ngoài:** trên UI-Venus, A3 − S1 cùng dấu với UGround.

## 9. Chat nhận file phải giao lại

1. Mã đã sửa và runbook. Ghi rõ đường dẫn, kèm câu lệnh commit cho người dùng tự chạy. Agent không chạy git.
2. Bảng số theo mẫu mục 2. Gồm:
   - exec click và 13 cột;
   - không chạm theo từng lớp;
   - UI-Venus;
   - điểm toàn bộ bước (chỉ báo, không khoá).
3. Hình λ_k, ĉ_k và lực đẩy theo bước, từ `ctg_log.jsonl` của A3 và A2.
4. Kết luận theo luật mục 8. Trượt luật nào thì nói thẳng.

## 10. Người dùng tự làm / tự quyết

1. Thuê A100 40 GB (Colab Pro+ / RunPod / Lambda), sau khi P0 qua.
2. Chỗ ghi mã:
   - (a) ngoài repo, `thesis/_exports/ctg/`: an toàn khi xoá clone, người dùng tự chép vào repo; hay
   - (b) thẳng vào `thesis-master/harness/`: phải commit trước khi xoá clone.
3. Commit và push mã sau khi chat kia viết xong. Ví dụ, nếu chọn (b): `git add harness/ && git commit -m "CTG-GRPO + r_cider" && git push`.

## 11. Sau khi có số — chỉ khi A3 qua R-click, R-CTG và R-noharm

| mã | việc | máy / giờ |
|---|---|---|
| E1 | Thêm seed 102, 103 cho A3 và A2; báo trung bình ± KTC theo seed | A100, khoảng 28–44 giờ |
| E2 | Chấm UI-Venus thêm cho S1, ck500, A4, A7 | T4, khoảng 1–2 giờ mỗi checkpoint |
| E3 | A4, A7 chạy đủ 1.000 bước, so ở cùng mốc cuối với A3 | A100, 2 × 7–11 giờ |

- Nếu A3 trượt R-CTG: **không chạy E1–E3**, báo lại để quyết hướng khác.
- Thực nghiệm mở rộng khác (thêm dataset hoặc mô hình, SPICE + CTG, LoRA tách theo loại) nằm ở file 277, mục 16.5–16.6.

## Phụ lục A — mã CIDEr-D Python thuần (chép nguyên văn vào `r_cider`)

Đã kiểm: tái lập pycocoevalcap **3.484/3.600 câu trùng tuyệt đối, 399/400 bước chọn cùng câu** (IDF từ 400 câu chuẩn val). Khi train, dựng `CiderD(ref_corpus)` một lần, với `ref_corpus` = toàn bộ câu chuẩn của `p1_train_rows.jsonl`.

```python
import math, re
from collections import defaultdict

PUNCT = {"''", "'", "``", "`", "-lrb-", "-rrb-", "-lcb-", "-rcb-", ".", "?", "!", ",", ":", "-", "--",
         "...", ";"}
TOK = re.compile(r"n't|'s|'re|'ve|'ll|'d|'m|[a-z0-9]+(?:[-./][a-z0-9]+)*|[^\sa-z0-9]")


def tok(s):
    """Xấp xỉ PTBTokenizer của pycocoevalcap: chữ thường, tách n't / 's, bỏ dấu câu."""
    s = (s or "").lower().replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'")
    s = re.sub(r"(\w)n't\b", r"\1 n't", s)
    return [t for t in TOK.findall(s) if t not in PUNCT and t != ""]


def ngrams(ws, n=4):
    c = defaultdict(int)
    for k in range(1, n + 1):
        for i in range(len(ws) - k + 1):
            c[tuple(ws[i:i + k])] += 1
    return c


class CiderD:
    """CIDEr-D đúng công thức pycocoevalcap (sigma 6, clip, x10) nhưng df và số tài liệu CỐ ĐỊNH."""

    def __init__(self, ref_corpus, n=4, sigma=6.0):
        self.n, self.sigma = n, sigma
        self.df = defaultdict(float)
        for r in ref_corpus:
            for ng in set(ngrams(tok(r), n)):
                self.df[ng] += 1
        self.log_n = math.log(float(len(ref_corpus)))

    def _vec(self, cnts):
        vec = [dict() for _ in range(self.n)]
        norm = [0.0] * self.n
        length = 0
        for ng, tf in cnts.items():
            k = len(ng) - 1
            w = float(tf) * (self.log_n - math.log(max(1.0, self.df.get(ng, 0.0))))
            vec[k][ng] = w
            norm[k] += w * w
            if k == 1:
                length += tf
        return vec, [math.sqrt(x) for x in norm], length

    def score(self, cand, refs):
        vh, nh, lh = self._vec(ngrams(tok(cand), self.n))
        tot = [0.0] * self.n
        for r in refs:
            vr, nr, lr = self._vec(ngrams(tok(r), self.n))
            pen = math.exp(-((lh - lr) ** 2) / (2 * self.sigma ** 2))
            for k in range(self.n):
                v = sum(min(w, vr[k].get(ng, 0.0)) * vr[k].get(ng, 0.0) for ng, w in vh[k].items())
                if nh[k] != 0 and nr[k] != 0:
                    v /= nh[k] * nr[k]
                tot[k] += v * pen
        return 10.0 * (sum(tot) / self.n) / len(refs)
```
