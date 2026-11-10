# ACTION CUỐI — GRPO + RGTC-SPICE THEO PROTOCOL KHOA HỌC — 10/11/2026

> **Ghi chú bản chép:** Nội dung được dựng lại từ 32 ảnh chụp màn hình trong ZIP, theo thứ tự đọc từ ảnh 32 về ảnh 1. Ảnh 31 và 32 trùng phần mở đầu, được gộp. Các biểu thức được chuyển thành LaTeX/inline code để dễ đọc. Nội dung không có trong khung hình sẽ không được suy diễn. Bản này là bản chép từ ảnh, không phải file Markdown nguồn gốc.

**Đây là file action duy nhất để chat khác thi hành.**

File này tự chứa: mục tiêu, phương pháp, dữ liệu, baseline, ablation, thứ tự CPU→GPU→eval, artifacts, kill gates, thống kê, chấm người, ngân sách và câu được phép bảo vệ.

File này thắng `ACTION_CUOI_6_11.md` về action reward/method mới. File `/Users/P836901/Documents/Self-learning/thesis/333_DEBATE_CHOT_GRPO_SPICE_METHOD_10_11.md` là biên bản debate/phương pháp chi tiết; action phải theo file này.

**Trạng thái thật:** SFT-cont đã train 500/500 và test `exec=60,16`; các baseline lưới lịch sử đã có số. Nhưng adapter SFT-cont `final/` không nằm trong clone. Toàn bộ pipeline RGTC mới (split/action verifier/counterfactual/reward/Gate B/train) chưa được triển khai.

**Mục tiêu khoa học:** Kiểm xem một reward SPICE-centered có target contrast và reliability gate, tối ưu bằng GRPO, có cải thiện GUI instruction generation so với các baseline matched hay không.

**Không khóa trước kết luận:** nếu phương pháp không thắng, báo kết quả âm.

> **Sửa đổi 10/11/2026 (user quyết, sau khi đã thấy số thử trên 1.500 bước, chưa có SPICE: 10,1% theo danh sách loại gốc, 35,5% khi bỏ danh sách).** (1) Ngưỡng độ phủ Gate B hạ từ 30% xuống 20%. (2) Bỏ danh sách role bị loại ở `target_role_not_generic`; bảng class → role lấy theo `harness/gate_b_rgtc.py`. Bốn cổng về độ tin cậy giữ nguyên: gold false rejection ≤5%, negative `T<0,5` ≥95%, giữ 100% action class, audit tay ≥190/200. Hai thay đổi này diễn ra sau khi thấy dữ liệu, nên phải khai trong luận văn và gọi phương pháp là **RGTC-SPICE v2**.

## EXECUTION CONTRACT — mặc định PREFLIGHT ONLY

```text
CURRENT_PHASE = PREFLIGHT_ONLY
TRACK = UNSET                # A_INTERNAL hoặc B_NEW_HOLDOUT
TIER = UNSET                 # MINIMUM_18 hoặc STRONG_23
HARDWARE = UNSET             # cùng loại máy/dtype cho toàn bộ phép so matched
PRIMARY_GROUNDER = osunlp/UGround-V1-2B  # phải pin revision/hash
INDEPENDENT_EVALUATOR = UNSET
HUMAN_STUDY = UNSET

REPO_ROOT = /Users/P836901/Documents/Self-learning/thesis/thesis-master
RUN_ROOT = /Users/P836901/Documents/Self-learning/thesis/_rgtc_runs
PRIVATE_ROOT = UNSET
```

Nếu còn giá trị `UNSET` cần cho phase được giao: **STOP**.

Nhiệm vụ mặc định hiện tại: **chỉ xác minh input, schema, hash và khả năng dựng split. Không viết code GPU, không train.**

## 0. Tóm tắt một trang

### Phương pháp

```text
S1/101
  ↓
SFT continuation
  ↓ merge
group-normalized GRPO + RGTC-SPICE
```

Reward:

\[
R=\operatorname{clip}_{[0,1]}(0.70S+0.15A+0.15T-d).
\]

- **S:** Sparse-SPICE/chrF semantic score.
- **A:** action score mềm, reliability-gated.
- **T:** same-screen target counterfactual contrast, reliability-gated.
- **d:** capped length penalty.

### Vì sao có ý nghĩa khoa học

Phương pháp đi theo cách các paper mạnh thường làm:

1. Cùng model/pipeline, chỉ đổi reward.
2. Baseline reward đơn và reward lai.
3. Ablation từng thành phần.
4. Chấm bằng metric độc lập với reward.
5. Kiểm reward hacking/thoái hóa.
6. Nhiều seed.
7. Holdout chưa dùng chọn phương pháp.
8. Human/blind evaluation hoặc evaluator độc lập.

Không sao chép reward của paper nào. Tiền lệ chỉ được dùng để thiết kế protocol.

### Việc phải làm theo thứ tự

1. Khôi phục SFT-cont weights.
2. Khóa dữ liệu dev/internal-confirm và quyết định holdout mới.
3. Viết action verifier.
4. Viết counterfactual builder.
5. Audit target/action trên CPU.
6. Viết production reward fail-closed.
7. Smoke CPU/Java/T4/resume/merge.
8. Chạy seed 101 cho matched baseline + ablations.
9. Chỉ nếu FULL thắng validation: chạy controls xác nhận.
10. Chạy confirmation seeds.
11. Mở internal-confirm/holdout một lần.
12. Chấm tap, non-tap, evaluator độc lập và human.
13. Viết kết luận theo decision table.

### Hai mức claim

**Mức A — có thể làm từ dữ liệu hiện có:** Xác nhận nội bộ ở tầng RL trên episode S1 đã thấy. Không gọi app-unseen, task-unseen hay confirmatory generalization.

**Mức B — muốn nói “best validated conditional on fixed seeds”:** Phải có holdout mới chưa được dùng train/design reward, nhiều seed, non-inferiority và human/grounder độc lập.

## 1. Vì sao protocol này giống cách paper làm

### 1.1 SPIDEr — bài học reward lai + human

SPIDEr, ICCV 2017:

- Train các nhánh reward khác nhau: BLEU, CIDEr, SPICE, BCMR, SPIDEr.
- SPIDEr = `0,5 SPICE + 0,5 CIDEr`.
- Pure SPICE sinh câu dài/lặp/sai ngữ pháp.
- Chấm metric tự động và ví dụ định tính.
- Chấm người 492 ảnh, 3 rater/caption.
- SPIDEr được người thích hơn BCMR khoảng 4 pp dù metric COCO thấp hơn; sign test `p=0,014`.

Luận văn học cách làm:

- Bắt buộc có SPICE-only, SPIDEr và reward khác.
- Đo câu dài/lặp/malformed.
- Không dùng chính metric reward làm kết luận cuối.
- Có blind human study.

### 1.2 FoCUS — bài học SFT→GRPO + factorial + reliability

FoCUS, EMNLP 2026:

- SFT rồi GRPO.
- Reward scene component có positive/negative weights.
- Object validity threshold và reasoning verification.
- Factorial ablation.
- Nhiều backbone.
- 3 GRPO seed.
- Evaluator khác training judge.
- Human study 140 pair, 14 rater/pair.
- Image-bootstrap 20.000 lần cho KTC benchmark SCoPE, không phải bootstrap riêng của human study.

Luận văn học cách làm:

- Tách reward scorer khỏi reward aggregation.
- Never-on / always-on / reliability-gated.
- Fixed-weight và positive-only controls.
- 3 seed tối thiểu.
- Evaluator độc lập và human.

### 1.3 SCST — bài học ma trận train-reward × eval-metric

SCST, CVPR 2017:

- Giữ model, đổi reward CIDEr/BLEU/ROUGE/METEOR.
- Chấm chéo mọi metric.
- So greedy baseline, learned baseline và REINFORCE.
- 4 seed trong phép so thuật toán, báo mean±SD/t-test.

Luận văn học cách làm:

- Giữ thuật toán cố định khi so reward.
- Giữ reward cố định khi so thuật toán.
- Chấm chéo, không chỉ metric được tối ưu.
- Báo seed variance.

### 1.4 BiGrounder/UI-R1/GDPO — bài học GUI và multi-reward

- BiGrounder: semantic similarity chưa đủ; grounding gate + audit tay 300 câu bắt lỗi tốt hơn.
- UI-R1: action reward trong GUI đã có; action tăng có thể che grounding giảm.
- GDPO: aggregate-then-normalize có thể làm multi-reward collapse; đây là động cơ để log phân phối, reward/advantage pattern và zero-variance từng channel, không phải định luật mọi channel ít variance đều biến mất.

Luận văn học cách làm:

- Tách action/target.
- Log từng channel.
- Audit tay reward/verifier.
- Không nhận novelty cho action reward hay multi-reward tự thân.

## 2. Tình trạng dữ liệu — phải đọc trước khi chạy

### 2.1 Dữ liệu đã bị dùng

| Dữ liệu | Quy mô | Trạng thái |
|---|---|---|
| AndroidControl project train | 64.567 bước / 12.895 episode | S1 đã học toàn bộ |
| Project test | 6.958 bước / 1.432 episode | Đã xem/chấm nhiều lần |
| C1 | 400 bước / 220 episode | Đã dùng thiết kế reward |
| `val_cham400+600` | 1.567 bước | Đã dùng nhiều thí nghiệm |
| ACU | 3.103 bước / 945 episode | Artifact tap đã chấm/phân tích |
| AitZ test | 4.724 bước / 506 episode | `exec/text` hiện trên 2.736 tap đã chấm/phân tích |

**Kết luận:** không còn holdout xác nhận sạch, có ảnh, sẵn dùng trong repo.

ACU ban đầu được liệt kê 3.113 bước/956 episode nhưng artifact hiện chỉ có 3.103/945; thiếu 10 bước/11 episode phải được reconcile nếu ACU còn dùng làm benchmark. Không tự điền bù.

### 2.2 Pool còn chưa dùng ở tầng RL

Sau khi loại mọi `prompt_keys` trong `runs`, C1, `val_cham400`, `val_cham600` và toàn bộ episode liên quan, candidate pool có:

- 49.046 bước.
- 10.726 episode.
- Thuộc `train_tru_val`.
- Chưa xuất hiện trong artifacts RL có prompt keys quan sát được.
- Nhưng S1 đã học.
- Repo hiện không có ảnh.

Hai số 49.046/10.726 **chưa phải split đã khóa**. Thêm artifacts/prompt keys mới có thể làm chúng đổi; manifest cuối phải in lại số và hash toàn bộ nguồn loại.

Tên đúng: **RL-stage held-out, S1-seen.** Đây mới là candidate pool theo exclusion hiện có; chỉ được gọi RL-stage held-out sau khi khôi phục lineage mọi run thiếu prompt keys và freeze manifest.

Không gọi: task-unseen, training-untouched, app-unseen, clean external holdout.

### 2.3 Split nội bộ bắt buộc

Sau khi khôi phục ảnh từ nguồn private/user-approved:

1. Dựng `exclusion_prompt_keys.json` từ:
   - Mọi `runs/**/prompt_keys.json`.
   - Đúng 1.000 prompt SFT-cont.
   - Mọi run lịch sử thiếu `prompt_keys` phải được khôi phục từ log/script/manifest, đặc biệt GRPO-point 2.000 prompt.
   - C1.
   - `val_cham400`.
   - `val_cham600`.
   - Retrieval/candidate artifacts đã dùng.
2. Mở rộng mọi excluded step thành excluded episode.
3. Nếu không khôi phục được đúng prompt keys SFT-cont: **STOP Track A**; nếu không khôi phục được lineage một run lịch sử: exclude toàn source episode liên quan hoặc **STOP Track A**.
4. Chia theo episode, không theo step.
5. Length bucket: `1–4`, `5–9`, `≥10` bước.
6. Dominant action = action có nhiều step nhất; hòa thì chọn tên action nhỏ nhất theo bytewise order.
7. Strata = dominant action × length bucket.
8. Trong mỗi stratum sort theo `SHA256(UTF8("rgtc-v1|" + decimal_episode_id))`.
9. Quota từng stratum dùng largest-remainder; hòa quota theo tên stratum bytewise.
10. Phân bổ:
    - 600 episode → `dev_internal`.
    - Từ phần còn lại, 800 episode → `confirm_internal`.
    - Phần còn lại → `reward_train_pool`.
11. Assert giao episode giữa ba tập bằng 0.
12. Khóa `confirm_internal` trước mọi generation/screening.

`confirm_internal` chỉ xác nhận post-SFT reward adaptation trên S1-seen data.

### 2.4 Holdout mạnh nếu muốn “best validated”

Khuyến nghị thu thập mới:

- 80 package/app ID chưa có trong nguồn train/retrieval/eval.
- 10 task/app = 800 task.
- 20 app/200 task dùng development.
- 60 app/600 task giữ kín confirm.
- Mục tiêu ≥4.000 bước trước khi mở.
- Mỗi step lưu package ID, screenshot hash, action log, target box, action type, instruction.
- 2 annotator độc lập viết instruction, bất đồng được adjudicate.
- Annotator không thấy output model.

Nếu không thu thập được: mọi kết luận là internal/exploratory; không dùng “best validated”, “generalizes” hoặc “app-unseen”.

## 3. Phương pháp đã khóa để kiểm

### 3.1 SFT continuation

- Khởi đầu S1/101.
- LoRA mới cùng cỡ.
- 1.000 prompt ck500.
- 500 update × 2 prompt/update.
- LR `1e-5`.
- AdamW, weight decay 0.
- Warmup 10 rồi constant.
- Grad clip 1,0.
- Final step 500.
- Merge thành `sft_cont_merged`.

### 3.2 GRPO

- Policy/reference: cùng `sft_cont_merged`; reference frozen.
- `G=8`.
- 2 prompt/update.
- 500 update.
- Temperature 1,0.
- Top-p 1, top-k 0.
- Max completion 96.
- LR `1e-5`.
- KL `β=0,04`.
- Group reward normalization.
- DAPO token aggregation.
- `num_iterations=1`.
- Vision frozen.
- LoRA ngôn ngữ 14.966.784 tham số.

Prompt train GRPO:

- Đúng 1.000 step key lấy từ `reward_train_pool`.
- `data_seed = 20261110`.
- Mỗi episode chọn một step có hash nhỏ nhất theo `SHA256("rgtc-step-v1|20261110|episode|step")`.
- Tạo `one_step_per_episode` từ kết quả trên.
- Quota action proportional theo `one_step_per_episode` (không theo toàn step pool), largest-remainder để tổng đúng 1.000.
- Trong action stratum sort `SHA256("rgtc-train-v1|20261110|episode|step")`, lấy theo quota.
- Hòa quota/order theo bytewise key.
- Giống tuyệt đối cho mọi arm.
- `run_seed` chỉ đổi sampling/training RNG.
- Không tái dùng 1.000 prompt SFT-cont/ck500.

### 3.3 Reward RGTC-SPICE

\[
R=\operatorname{clip}_{[0,1]}(0.70S+0.15A+0.15T-d).
\]

**Semantic**

\[
\alpha_g=0.8\min(1,K_g/3)
\]

\[
S=\alpha_g\operatorname{SPICE}(y,g)+(1-\alpha_g)\frac{\operatorname{chrF}(y,g)}{100}.
\]

`K_g` là số tuple SPICE canonical duy nhất. `chrF` dùng `sacrebleu.sentence_chrf(...).score` trên thang 0–100 rồi chia 100.

**Action**

\[
A\in\{0,0.5,1\}.
\]

- Đúng canonical action, không toggle contradiction: 1.
- Sai chắc chắn: 0.
- Unknown/untrusted: 0,5.
- v1 không dùng hướng scroll.

**Target**

Với gold \(g^+\), counterfactual \(g^-\):

\[
T=\operatorname{clip}_{[0,1]}\left(0.5+0.5\big[\operatorname{SPICE}(y,g^+)-\operatorname{SPICE}(y,g^-)\big]\right).
\]

- Never-on: `T=0,5`.
- Always-on: dùng contrast khi technically eligible.
- Reliability-gated: dùng khi eligible và metadata đáng tin.
- Ineligible/untrusted: `T=0,5`.

**Length**

\[
d=\min\left(0.05,\ 0.02\max(0,n_w(y)-n_w(g)-3)\right).
\]

`n_w` đếm regex `[A-Za-z0-9'-]+`, không phải model token. Câu rỗng reward 0.

### 3.4 Công thức từng arm — không được chỉ dùng tên

Ký hiệu: `s = SPICE(y,g)`, `c = CIDErD(y,g)/10`, `r = ROUGE_L(y,g)`. CIDEr document frequency chỉ dựng từ gold của `reward_train_pool`; cấm dùng dev/confirm. Neutral action/target = `0,5`.

| Arm | Reward |
|---|---|
| A0 / SPICE-MATCH | `clip(0.70s + 0.15×0.5 + 0.15×0.5 - d, 0, 1)` |
| A1 | `clip(0.70S + 0.15×0.5 + 0.15×0.5 - d, 0, 1)` |
| A2 | `clip(0.70S + 0.15A + 0.15×0.5 - d, 0, 1)` |
| A3 | `clip(0.70S + 0.15A + 0.15T_always - d, 0, 1)` |
| FULL | `clip(0.70S + 0.15A + 0.15T_reliable - d, 0, 1)` |
| SPIDEr-like (repo implementation) | `clip(0.50s + 0.50c - d, 0, 1)` |
| ROUGE-L | `clip(r - d, 0, 1)` |

`R0-HIST = SPICE - uncapped_length_penalty` chỉ tái lập lịch sử; không phải causal control.

SCST-like+FULL dùng cùng reward FULL và:

\[
A_i = R(y_i)-R(y_{greedy}),
\]

vẫn giữ `G=8`, KL `β=0,04`, DAPO token aggregation và cùng update budget.

GRPO group zero-std:

\[
A_i = \frac{R_i-\bar R}{\operatorname{std}(R)+10^{-4}};
\]

nhóm cùng reward cho advantage 0.

### 3.5 Scorer contract

- `K_g` = số tuple duy nhất trong SPICE detailed output, có tag loại:
  - Object: `O|object`.
  - Attribute: `A|object|attribute`.
  - Relation: `R|subject|relation|object`.
- Canonical từng field: UTF-8 NFC, lowercase, trim/collapse whitespace.
- Deduplicate theo toàn tagged serialization; object/attribute/relation có cùng text không bị gộp.
- Parser exception khác `K_g=0`: exception phải dừng.
- Batch interleaved: `[(sample_0,g+),(sample_0,g-),...,(sample_N-1,g+),(sample_N-1,g-)]`.
- Mỗi request/response có `sample_id` và `pair_side`.
- Không chỉ kiểm `len=2N`; assert đúng ID/side từng vị trí.
- Missing/partial/None/NaN/Inf: dừng, không đổi thành 0/neutral.

## 4. Blocker trước khi viết code GPU

### 4.1 SFT-cont weights

Clone hiện không thấy adapter SFT-cont trong thư mục `final/` (script không tạo `checkpoint-500`).

Phải:

1. Lấy output Kaggle/private artifact.
2. Hash tree.
3. Merge với S1.
4. Probe logits/greedy:
   - S1 merged + adapter bật.
   - Checkpoint đã merge.
5. Hai đường phải trùng trong tolerance.

Thiếu weights → **dừng**.

### 4.2 Ảnh cho split mới

Repo không có ảnh pool 49.046 bước. Phải dùng private Kaggle dataset/Drive artifact hiện có, hoặc nguồn khác do user duyệt. Không dựng split chỉ từ JSON mà không có ảnh/chấm được.

### 4.3 Quyết định claim

Trước khi code, user phải chọn:

- **Track A:** internal confirm trên S1-seen.
- **Track B:** thu holdout mới để claim mạnh.

Nếu chưa chọn: **STOP ở PREFLIGHT**, không tự mặc định Track A.

## 5. Phase 0 — freeze protocol, 0 GPU

Tạo ngoài mã train:

- `input_manifest.json`.
- `experiment_manifest.json`.
- `split_spec.json`.
- `claim.md`.
- `primary_family.json`.
- `noninferiority.json`.

Khóa: reward formula; `0,70/0,15/0,15`; action verifier version; target eligibility/reliability; seed; prompt keys; checkpoint rule; primary endpoint; five/three hypothesis family; non-inferiority margins; human protocol; kill gates.

Biên non-inferiority:

\[
\delta_{all}=1.0\ \mathrm{pp},\quad \delta_{scroll}=2.0\ \mathrm{pp},\quad \delta_{back}=2.0\ \mathrm{pp}.
\]

Không đổi sau khi nhìn validation.

### 5.1 Input manifest bắt buộc

Mỗi input ghi absolute path, kích thước và SHA-256:

- Base model revision + tree hash.
- Processor revision + tree hash.
- S1 `adapter_config.json` + `adapter_model.safetensors`.
- SFT-cont `final/adapter_config.json` + `final/adapter_model.safetensors`.
- `train_tru_val.jsonl`.
- Image root.
- Metadata root có package/app ID, box, actionable flag, canonical role và nguồn name.
- Exact SFT/C1/val/exclusion prompt keys.
- Primary grounder checkpoint/config/revision.

Thiếu file hoặc hash mismatch: **STOP**.

Tree hash:

```text
sort bytewise theo relative POSIX path
SHA256(relative_path<TAB>file_sha256<LF>...)
```

Probe merge phải khóa device/dtype; processor; probe keys; atol/rtol; logits/greedy expected hash.

## 6. Phase 1 — code CPU

### 6.1 File mới cần viết

Không sửa mã baseline lịch sử. Viết mới:

```text
harness/merge_sft_cont.py
harness/build_rgtc_splits.py
harness/action_reward_verify.py
harness/build_rgtc_counterfactual.py
harness/spice_failclosed.py
harness/reward_rgtc_spice.py
harness/screen_rgtc_cpu.py
harness/test_rgtc_spice.py
harness/grpo_rgtc.py
harness/analyze_rgtc.py
_bundles/rgtc/make_cpu_nb.py
_bundles/rgtc/make_train_nb.py
_bundles/rgtc/make_eval_nb.py
```

### 6.2 Action verifier

Không dùng thẳng `metric_exec.canon_action`.

Verifier phải trả: canonical action; known/unknown; toggle contradiction; reason code; version.

Trust/action contract:

- `expected` lấy từ normalized action log.
- Prompt trusted chỉ khi `expected` hợp lệ và action suy từ gold bằng `expected`.
- Prompt untrusted → `A=0,5` cho toàn group.
- Trusted + candidate match → `A=1`.
- Trusted + candidate chắc chắn mismatch/toggle contradiction → `A=0`.
- Trusted + candidate unknown → `A=0,5`.

Gate trên audit set khóa trước, không dùng để phát triển verifier:

- One-sided Clopper–Pearson 95% **lower bound** của precision *known wrong* `>98%`.
- One-sided Clopper–Pearson 95% **upper bound** của false reject từng action `<5%`.
- Unknown không ép thành tap.
- Direction scroll chưa vào reward v1.

Báo đầy đủ confusion matrix TP/FP/FN/unknown theo action. Nếu cỡ mẫu không đủ để đạt bound, gate là unresolved và FULL dừng; không thay bằng point estimate.

Audit sample size/strata phải được power script khóa trước khi mở nhãn; tối thiểu 200 mẫu và phải phủ mọi action class có trong reward train.

Trượt gate:

- FULL/RGTC-SPICE bị loại trước GPU.
- Không được neutral toàn bộ action rồi vẫn giữ tên FULL.
- Muốn tiếp tục phải đăng ký candidate mới với tên/công thức/claim mới.

### 6.3 Counterfactual builder

Mỗi row:

1. Tìm alias target duy nhất trong gold.
2. Lưu exact character offsets.
3. Xác định element actionable nhỏ nhất chứa điểm chạm.
4. Chọn một distractor cùng canonical actionable role.
5. Box không overlap, canonical name khác.
6. Tie-break `(distance, y, x, name)`.
7. Thay đúng một span.
8. Assert bytes ngoài span không đổi.
9. Modifier position/state/attribute phải còn đúng.
10. Action class không đổi.
11. SPICE graph gold/counterfactual phải khác.
12. Ghi eligibility `e_t`, reliability `m_t`, reason code, provenance.

Ineligible vẫn lưu `g-=g+` để scorer luôn có đúng `2N` pair; mask ép `T=0,5`.

Schema khóa trong artifacts:

- `canonical_roles.json`: mapping raw class/role → canonical actionable role.
- Actionable = `clickable || long_clickable`; text-only node không được làm distractor.
- Generic role blacklist: bỏ (sửa 10/11; bản gốc loại `container`, `layout`, `text`, `unknown`).
- Alias sources theo thứ tự provenance: a11y `text`, `content_description`, tail của `resource_id`, rồi OCR token nằm trong target box.
- Alias normalize: Unicode NFC, lowercase, collapse whitespace, strip punctuation, giữ digits.
- Deduplicate exact canonical alias nhưng giữ list provenance.
- Eligibility yêu cầu đúng một alias-span match duy nhất trong gold trên union aliases; nhiều alias cùng trỏ cùng span được gộp, nhiều span khác nhau → ineligible.
- Box overlap: yêu cầu IoU = 0; touching edge được phép.
- Positional modifier: grid 3×3 theo center box; gold/distractor phải cùng region nếu câu có top/bottom/left/right/center.
- Toggle/state modifier: metadata state phải trùng.
- Attribute modifier không xác minh được → ineligible.
- Mọi map/list/predicate có version/hash.

Truth table khóa trước DEV output:

```text
e_t = span_unique
      AND positive_actionable
      AND negative_actionable
      AND same_canonical_role
      AND box_iou == 0
      AND modifier_predicates_pass
      AND action_class_preserved
      AND spice_graphs_parse_and_differ

m_t = e_t
      AND gold_is_smallest_actionable_box_containing_touch
      AND target_role_not_generic
      AND canonical_target_name_occurs_once_on_screen
      AND target_name_source_is_a11y_or_ocr_inside_target_box
      AND target_box_area_ratio <= 0.25
      AND negative_box_area_ratio <= 0.25
```

Mọi predicate chỉ đọc metadata/input trước khi sinh output. Field thiếu → `False`, không suy đoán. Truth table và hash phải freeze trước DEV generation.

**RANDOM-MASK:** trong từng stratum khóa trước, đặt đúng `k = Σm_t` eligible rows active; sort eligible rows theo `SHA256("rgtc-random-mask-v1|episode|step")`, lấy `k` dòng đầu.

### 6.4 Artifacts CPU

- `action_trust.jsonl`.
- `counterfactuals.jsonl`.
- `tuple_cache.jsonl`.
- `audit_200.jsonl`.
- `reward_screen.json`.
- `split_manifest.json`.
- SHA-256 từng file.

`split_spec.json` khóa thuật toán ở Phase 0. `split_manifest.json` chỉ được sinh ở Phase 1 sau khi có input thật, phải audit và freeze hash trước mọi generation, screening hoặc training.

## 7. Phase 2 — gates CPU, 0 GPU

### 7.1 Chạy kit report 332

Dùng để fail-fast: SPICE thật, chrF, stress test, reward ties, zero-std, action trust. Không dùng C1 để chọn final reward.

### 7.2 Target Gate B

Phải đạt:

1. Active coverage \(P(e_tm_t=1\mid tap)\ge 20\%\) (sửa 10/11; bản gốc 30%).
2. Báo riêng \(P(e_t=1\mid tap)\), \(P(m_t=1\mid e_t)\).
3. Với \(y=g^+\):
   \[
   FR_{gold}=P(T(g^+)\le 0.5\mid e_tm_t=1)\le 5\%.
   \]
4. Với \(y=g^-\), ≥95% có target score `<0,5`.
5. 100% giữ action class.
6. Audit tay phân tầng 200 cặp theo action/app/name source/role/duplicate-name:
   - ≥190/200 one-factor negative đủ ngữ pháp.
   - 0/200 đổi action.
   - In exact CI, nhưng đây vẫn là QC gate chứ không phải chứng minh population.

Trượt một dòng:

- RGTC bị loại trước GPU.
- Không hạ ngưỡng thêm lần nào nữa (đã sửa một lần ngày 10/11, xem ghi chú đầu file).
- SA-SPICE là nghiên cứu khác, không giữ tên RGTC.

### 7.3 Production scorer gate

Scorer phải:

- Nhận batch `(y,g+),(y,g-)` đúng thứ tự.
- Trả đúng `2N` score.
- Finite `[0,1]`.
- Lỗi parser/JVM → dừng.
- Không biến lỗi thành zero tuple.
- Cache writer riêng.
- Thiếu key → dừng.
- In `S,A,T,R_pre,R`.
- In clip rate.
- In tie/zero-std.
- In pair-flip từng channel.
- In unknown/mask coverage/reason histogram.

## 8. Phase 3 — smoke

Chạy đúng thứ tự:

1. Unit test công thức/mask/offset/empty/clipping.
2. Java smoke 16–64 records.
3. Full CPU screen trên dev.
4. Tiny-model CPU train 2 bước.
5. T4 longest-prompt smoke 20 bước.
6. Resume smoke 10→20 bước.
7. Merge/logits equivalence.

T4 smoke phải xác nhận:

- Policy/reference trùng step 0, KL gần 0.
- LoRA-B 0 trước update, >0 sau.
- Group đúng 8 completion cùng key.
- Optimizer/scheduler/RNG resume đúng.
- Chunk không đổi order.
- VRAM có biên.
- Speed benchmark: sau 5 warmup step, lấy median optimizer-step time của step 6–20, warm cache, lặp hai smoke cùng hardware/dtype.
- Gate ≤216 giây/bước chỉ áp cho một run trên một T4 theo envelope 30 T4-hour/500 step; hardware khác phải khóa walltime budget riêng trước full run.

Trượt → đừng full run.

## 9. Phase 4 — seed 101 screening

### 9.0 DEV alias theo Track

- Track A: `DEV = dev_internal`, `CONFIRM = confirm_internal`.
- Track B: `DEV = 200-task external development`, `CONFIRM = 600-task external holdout`.

Mọi chỗ phía dưới ghi DEV/CONFIRM phải resolve đúng theo Track trong manifest.

### 9.1 Năm arm cơ chế

Tất cả từ cùng `sft_cont_merged`, cùng prompts/seed/budget:

| Arm | Semantic | Action | Target |
|---|---|---|---|
| A0 / SPICE-MATCH | SPICE matched wrapper | neutral | neutral |
| A1 | Sparse-SPICE | neutral | neutral |
| A2 | Sparse-SPICE | reliability | neutral |
| A3 | Sparse-SPICE | reliability | always-on eligible |
| FULL | Sparse-SPICE | reliability | reliability-gated |

### 9.2 Baseline reward

- GRPO+SPIDEr-like theo repo: `0,5 SPICE + 0,5 (CIDEr-D/10)`, rồi wrapper cuối clip reward.
- GRPO+ROUGE-L.
- SFT-cont không RL.

### 9.3 Chọn checkpoint

Chỉ chấm: `100, 200, 300, 400, 500`.

Feasible khi:

- Scroll/back không thấp hơn SFT-cont quá 3 pp trên dev.
- Unknown không tăng >2 pp.
- Empty không tăng >0,5 pp.
- Truncated không tăng >1 pp.
- Rolling-20 KL ≤0,10 và finite.

Rule:

1. Tìm feasible checkpoint có tap exec cao nhất `M`.
2. Dùng đúng cluster rule đã freeze ở mục 13.3bis; không quyết lại tại checkpoint selection.
3. Cluster-bootstrap `B=10.000` trên checkpoint `M`, không reselect checkpoint trong mỗi replicate.
4. `SE(M)` = sample SD của 10.000 bootstrap means.
5. Chọn checkpoint sớm nhất có mean ≥ `M − SE(M)`.
6. Nếu point mean hòa chính xác, chọn checkpoint sớm hơn.
7. Không feasible → arm fail, không nới.

### 9.4 Kill sau seed 101

Nếu FULL không hơn SPICE-MATCH trên dev:

- Dừng confirmation.
- Báo kết quả âm.
- Không quét thêm weights trên test.

## 10. Phase 5 — ablation xác nhận

Chỉ chạy nếu FULL qua seed-101 validation.

Mọi control giữ nguyên wrapper `clip(0.70S+0.15A+0.15T−d,0,1)`, initialization, prompts, budget và checkpoint rule.

1. **TARGET-POS**:

   \[
   T_{pos}=\begin{cases}
   0.5+0.5\operatorname{SPICE}(y,g^+),&e_tm_t=1,\\
   0.5,&\text{khác}.
   \end{cases}
   \]

2. **RANDOM-MASK**:
   - Dùng cùng target contrast như FULL.
   - Chỉ shuffle trong tập `e_t = 1`.
   - Thay `m_t` bằng mask deterministic shuffled trong từng app/action stratum.
   - Active coverage bằng đúng reliability mask.
   - Sort key `SHA256("rgtc-random-mask-v1|episode|step")`.
   - Mask khóa trước output.

3. **FIXED-MIX**:

   \[
   S_{fixed}=0.8\operatorname{SPICE}+0.2\frac{\operatorname{chrF}}{100}
   \]

   Cho mọi mẫu; action/target giống FULL.

4. **NO-SPICE-ALL**:

   \[
   S_{no\_spice}=\frac{\operatorname{chrF}(y,g^+)}{100},
   \]

   \[
   T_{no\_spice}=\operatorname{clip}_{[0,1]}\left(0.5+0.5\left[\frac{\operatorname{chrF}(y,g^+)-\operatorname{chrF}(y,g^-)}{100}\right]\right).
   \]

   Không channel nào được gọi SPICE; khi `e_t m_t = 0`, ép `T_no_spice = 0,5`.

5. **IDENTITY-POSITIVE-ONLY**:
   - Tokenizer: Unicode NFC, lowercase, regex `[a-z0-9'-]+`.
   - `F1_token` là multiset-token precision/recall F1.

   \[
   I_{pos}(y)=\max_{a\in aliases(g^+)}F1_{token}(y,a)
   \]

   \[
   T_{id}=\begin{cases}0.5+0.5I_{pos},&e_tm_t=1,\\0.5,&\text{khác}.
   \end{cases}
   \]

Ghim version/tokenizer của SPICE, chrF, CIDEr-D, ROUGE-L và alias normalization trong manifest.

Luật claim:

- FULL không thắng TARGET-POS → không claim counterfactual.
- FULL không thắng A3/RANDOM-MASK → không claim reliability.
- FULL không thắng NO-SPICE-ALL → không claim SPICE-centered.
- FULL không thắng FIXED-MIX → không claim tuple-aware routing.
- Reliability false rejection không giảm → không claim reliability giúp nhận.

Các control seed-101 là exploratory. Muốn dùng một ablation làm claim cơ chế, promote đúng arm liên quan lên ≥3 matched seeds. Không claim action reliability vì protocol hiện không có action always-on/random controls; action chỉ là correction phụ.

## 11. Phase 6 — confirmation seeds

### 11.1 Mức tối thiểu dễ bảo vệ

Seed 101 chạy toàn screen. Thêm seed 202,303 cho:

- FULL.
- SPICE-MATCH.
- Baseline mạnh nhất giữa SPIDEr-like và ROUGE-L, chọn bằng rule DEV khóa trước.

SFT-cont là mốc cố định; claim: *conditional on one fixed SFT-cont initialization, across three RL seeds*.

Run count:

- Seed 101: 7 RL screening arms.
- 5 control arms xác nhận.
- Seed 202/303 × 3 methods = 6.
- **Tổng 18 RL runs.**

### 11.2 Mức mạnh cho claim conditional trên fixed seeds

Ít nhất 3 seed cho:

- FULL.
- SPICE-MATCH.
- GRPO+SPIDEr-like.
- GRPO+ROUGE-L.
- SCST-like+RGTC-SPICE.

Run count strong-3-seed:

- Seed 101: 7 screening + 5 controls + 1 SCST = 13.
- Seed 202/303 × 5 primary-family methods = 10.
- **Tổng 23 RL runs.**

Ba seed chỉ cho inference conditional trên ba seed. Muốn suy rộng qua training randomness:

- Dùng ≥8 paired run seeds cho từng method trong primary family.
- Seed-level paired inference.
- Không dùng hàng nghìn step để giả sample size seed.

Mỗi method dùng cùng run seeds. Không chọn seed đẹp.

## 12. Phase 7 — mở confirm/holdout

### 12.1 Internal confirm

Chỉ mở sau khi khóa: code; reward; weights; masks; seeds; checkpoint rule; primary family; analysis script.

Câu được nói:

> better than SPICE-MATCH, SFT-cont and the DEV-selected SPIDEr-like/ROUGE-L baseline on RL-stage-held-out, S1-seen internal Confirm, conditional on the fixed run seeds.

Không nói unseen/generalization.

### 12.2 External/new holdout

Nếu có dữ liệu mới:

- Mở đúng một lần.
- Không sửa method sau.
- Mọi sửa đổi cần holdout mới.

## 13. Phase 8 — đánh giá

### 13.0 Evaluator contract

Trước train phải pin/hash:

- UGround checkpoint/revision.
- Processor.
- Prompt template.
- Image resize.
- `metric_exec` implementation.
- Action parser.
- Inventory builder/candidate source.

Primary `action_ok` không được dùng action verifier của reward. Reward cache/verifier không được tune bằng confirm. Grounder thứ hai/human là robustness, không thay primary sau khi thấy số.

Evaluation generation contract, khóa trước train:

- Hash system/user prompt template và image preprocessing.
- Deterministic greedy: `do_sample=False`.
- `max_new_tokens=96`.
- EOS/stopping = tokenizer/model chat-template `<|im_end|>` contract.
- `temperature/top_p/top_k=None` trong greedy.
- Fixed batching/chunk order.
- `use_cache=True`.
- Log processor/model revisions.
- Sinh đúng một prediction artifact đã hash cho mỗi method/seed/checkpoint và tái dùng cùng file cho UGround, grounder thứ hai, text metrics và human sampling.

Không evaluator nào được tự sinh lại câu.

### 13.1 Primary

**Tap exec = `action_ok` ∧ ±14% ∧ Voronoi.**

Không đổi headline sang D.3/AitW/text metric.

### 13.2 Primary family tối thiểu

Ba phép so:

1. FULL − SPICE-MATCH.
2. FULL − SFT-cont.
3. FULL − DEV-selected baseline giữa SPIDEr-like/ROUGE-L theo rule khóa trước.

Rule chọn baseline:

- Lấy mean tap exec dev cao hơn.
- Nếu chênh tuyệt đối ≤0,05 pp, chọn SPIDEr-like theo ưu tiên khóa trước.
- Chỉ chọn một lần, trước confirm.

Holm:

- `p` nhỏ nhất `<0,0167`.
- Tiếp theo `<0,025`.
- Cuối `<0,05`.

Báo: Δ, KTC95, `p` raw, `p` Holm, từng seed, mean±SD giữa seed.

Minimum tier chỉ được claim ba phép trên, không được viết “thắng mọi baseline”.

### 13.3 Family mạnh

Năm phép:

1. FULL − SFT-cont.
2. FULL − SPICE-MATCH.
3. FULL − SPIDEr-like.
4. FULL − ROUGE-L.
5. FULL − SCST-like+RGTC-SPICE.

Muốn nói *best validated conditional on fixed seeds*:

- Point estimate FULL cao hơn cả năm comparator.
- Cả năm raw one-sided p-value đều qua Holm.

Ngưỡng Holm theo thứ tự p tăng dần:

```text
0,0100 · 0,0125 · 0,0167 · 0,0250 · 0,0500
```

KTC95 báo riêng là unadjusted effect interval; không gọi nó “Holm-adjusted CI”.

### 13.3bis Seed estimand

Với 3 fixed run seeds:

1. Ở mỗi item, lấy mean outcome qua ba seed cho từng method.
2. Tính paired difference.
3. Cluster rule khóa trong split manifest trước output:
   - Track B: package ID bắt buộc 100%; cụm = package; thiếu package → STOP.
   - Track A: nếu package coverage =100% thì cụm = package cho toàn tập, ngược lại cụm = episode cho toàn tập; không trộn/fallback từng row.
   - `<30` cụm → endpoint `estimation-only`, không kiểm định.
4. KTC95 unadjusted: resample cụm 10.000 lần, giữ toàn row trong cụm, tính lại micro-average, lấy percentile 2,5/97,5.
5. Raw one-sided superiority `p`: cluster sign-flip 100.000 lần, cùng một dấu cho mọi row trong cụm, `p=(1+#(Δ_perm ≥ Δ_obs))/(100000+1)` dưới null đối xứng.
6. Holm step-down trên raw p.

Đây là inference conditional trên ba seed đã chạy, không suy rộng chắc chắn sang phân phối seed. Không pool 13.389 prediction như quan sát độc lập.

Muốn claim tổng quát qua training randomness:

- Dùng ≥8 paired run seeds/method trong primary family.
- Tính paired effect theo seed.
- One-sided exact sign-flip/permutation ở seed level.
- Episode/app bootstrap chỉ là uncertainty bên trong mỗi seed.

### 13.4 Non-tap non-inferiority

So FULL với SFT-cont:

\[
\delta_{all}=1.0\ \mathrm{pp},\quad \delta_{scroll}=2.0\ \mathrm{pp},\quad \delta_{back}=2.0\ \mathrm{pp}.
\]

Pass khi cận dưới KTC một phía 95% `> -δ` cho cả ba.

Cận dưới một phía = percentile 5% của cluster-bootstrap distribution; không dùng percentile 2,5% của KTC95 hai phía.

Dùng cùng seed aggregation và cluster resampling ở mục 13.3bis; đây vẫn là kết luận conditional trên fixed seeds nếu chỉ có ba seed. Ba margin được khóa chặt hơn cổng −3 pp lịch sử vì phương pháp mới tuyên bố sửa action; user phải chấp nhận chúng trong `noninferiority.json` trước validation.

Endpoint v1 là `non_tap_action_class_accuracy`: so canonical action class model với gold. Hàng Scroll chỉ đo model có nói đúng lớp scroll, không đo hướng cuộn. Nếu muốn direction, phải thêm endpoint `scroll_direction_accuracy`, khóa convention screen-motion/finger-motion và audit riêng trước confirm.

Không đủ lực → unresolved, không nói no-harm.

### 13.5 Secondary

- D.3.
- AitW.
- Action/target decomposition.
- SPICE, CIDEr-D, ROUGE-L, chrF.
- Length, repetition, distinct-1/2.
- Empty/malformed/no-action-verb.
- Compute/VRAM.
- Reward tie/zero-std.
- Mask coverage.
- Proxy-vs-exec theo checkpoint.

Toàn bộ secondary là descriptive/exploratory; không được cứu primary hoặc đổi headline.

### 13.5bis Blinded power pilot

Trước mở confirm, dùng pilot chỉ để ước lượng:

- Tap/non-tap rate.
- Discordance.
- Cluster ICC/design effect.
- Số scroll/back.
- Human tie rate.

Pilot chỉ dùng DEV hoặc một pilot subset tách khỏi CONFIRM. CONFIRM keys, outputs và human ratings không được xuất hiện trong pilot artifacts.

Pilot không được xem mean treatment difference. Khóa power/MDE và đánh dấu endpoint thiếu lực là `estimation-only/unresolved` trước confirm.

Planning constants:

- Family-wise `α=0,05`.
- Target power ≥80%.
- Tap SESOI = +1,0 pp.
- NI margins = 1/2/2 pp như mục 13.4.
- Human planning alternative = 60:40 preference trong non-tie, tie rate pilot 20%.

Simulation phải dùng cluster sizes/ICC và tap/scroll/back counts của split đã khóa. Nếu projected power `<80%` cho một endpoint, endpoint đó bắt buộc `estimation-only`; không được đổi SESOI/margin sau khi thấy effect.

### 13.6 Evaluator độc lập

Minimum claim cần ít nhất một:

- Grounder thứ hai.
- Blind human study.

Claim “best validated” strong tier cần cả hai. Nếu thiếu một, hạ claim.

Grounder thứ hai phải được pin trước holdout. Chấm cùng outputs/holdout/seeds, dùng cùng fixed `action_ok` parser nhưng tọa độ từ grounder thứ hai và cùng ±14%/Voronoi implementation.

Comparator robustness được chọn chỉ trên DEV trong năm primary comparators `{SFT-cont, SPICE-MATCH, SPIDEr-like, ROUGE-L, SCST-like+RGTC}`:

- Lấy mean tap exec DEV cao nhất.
- Nếu chênh ≤0,05 pp, tie-break theo thứ tự cố định: SFT-cont → SPICE-MATCH → SPIDEr-like → ROUGE-L → SCST-like.
- Freeze comparator trước CONFIRM.

Robustness gate FULL − comparator đã freeze:

- Point estimate tap exec `>0`.
- One-sided 95% lower bound `>-0,5 pp`.

Grounder thứ hai không nằm trong primary Holm family; nó là robustness gate. Nếu point estimate âm hoặc gate trượt, hạ strong claim và báo kết quả bất đồng.

## 14. Human study

### 14.1 Mẫu

Khuyến nghị:

- 150 item duy nhất.
- 100 tap, 50 non-tap.
- Cùng 150 item được chấm cho cả ba matched seed.
- Mỗi seed tạo 150 pair FULL-vs-baseline.
- Holdout/internal-confirm.
- Stratify package/app × action khi package ID có đủ; nếu thiếu thì action × episode-length và cấm claim app-disjoint.
- FULL vs non-RGTC baseline chọn trên DEV bằng đúng rule SPIDEr-like/ROUGE-L ở mục 13.2; freeze comparator trước CONFIRM.
- Mỗi item-seed pair có 3 rater độc lập.
- Tổng primary: 450 item-seed pair × 3 = **1.350 assignment**.
- Attention checks thêm ngoài primary: **135 assignment**.
- Tổng hiển thị = **1.485 assignment**.
- 1.350 primary assignments trả lời 3 câu hỏi = **4.050 primary question responses**.

Sample 150 keys trước khi sinh/xem output. Primary giữ cả output giống nhau. Phân tích changed-output chỉ là secondary và phải ghi “among changed outputs”; tỷ lệ output giống báo riêng.

### 14.2 Hiển thị

Cho rater thấy:

- Screenshot.
- Goal/history cần thiết.
- Gold action/target ở format trung tính.
- Hai instruction A/B.

Ẩn: model; seed; reward; metric; thứ tự gốc.

Random:

- Tráo A/B theo item-rater.
- Tráo item.
- Cân trái/phải.
- Không một rater thấy cùng item hai lần.
- 10% assignments là attention checks.
- Exclude rater nếu attention accuracy `<80%`, khóa rule trước unblind.
- Assignment bị loại được thay mù bằng một rater mới chưa thấy item, tối đa 2 replacement rounds.
- Mỗi item-seed pair phải có 3 valid unique raters.
- Sau 2 rounds, pair thiếu rater là missing; nếu valid pairs `<90%` kế hoạch, human endpoint `unresolved/inadequate power`.

### 14.3 Câu hỏi

Primary:

> Câu nào mô tả chính xác, không mơ hồ hơn thao tác lên đúng phần tử?

Đáp án: **A; B; Tie; Both unusable.**

Secondary:

- Câu nào dễ làm theo hơn.
- Câu nào tự nhiên/trôi chảy hơn.

### 14.4 Phân tích

- Majority 2/3.
- Majority `Both unusable` giữ nguyên category, không đổi thành tie.
- Trường hợp không có majority mới là tie.
- Mã hóa majority: FULL win `+1`, baseline win `−1`, Tie/Both `0`; Both báo riêng.
- Cluster = item, vì cùng item lặp qua ba seed.
- Primary statistic = mean outcome, null `E[outcome] ≤ 0`.
- Randomization one-sided 100.000 lần: tráo nhãn FULL/baseline bằng cùng một dấu cho cả ba seed trong mỗi item; stratify/report theo seed.
- Human “pass” khi point mean `>0` và raw one-sided `p≤0,05`.
- Exact sign test trên non-tie chỉ là phân tích phụ.
- Nếu kiểm cả ba câu hỏi, Holm.
- Báo tie/both-unusable.
- Báo Krippendorff's α nominal phụ.

Không có nguồn lực chấm người:

- Grounder thứ hai.
- Audit tay mù 100 lỗi bất đồng.
- Hạ claim.

## 15. Leakage checks

Fail-closed nếu:

1. Episode overlap reward-train/dev/confirm.
2. Confirm key xuất hiện prompt/reward cache/retrieval/candidates.
3. Ảnh trùng SHA/perceptual hash.
4. Goal/history/gold near-duplicate không được kiểm.
5. CIDEr DF/rarity/alias dùng confirm.
6. App-disjoint không dùng package ID.
7. Confirm output được dùng sửa reward/checkpoint.
8. Thiếu manifest hash.
9. Test cũ/ACU/AitZ bị gọi confirmatory.

Đặc tả:

- Ảnh exact SHA trùng → cùng group/exclude.
- pHash 63-bit DCT: apply EXIF orientation, RGB→grayscale, resize 32×32 bicubic, DCT, lấy 8×8 low-frequency bỏ DC còn 63 hệ số, threshold median; pin Pillow/NumPy/SciPy version.
- pHash Hamming `≤4` → near-duplicate, cùng group/exclude.
- Text normalize = Unicode NFC + lowercase + collapse whitespace + strip punctuation.
- Text shingles = token 3-gram.
- MinHash 128 permutation, seed `20261110`, hash family từ `SHA256(seed|permutation_index|shingle)`.
- Estimated Jaccard `≥0,90` → flag; manual adjudication trước freeze.
- App-disjoint chỉ dùng package ID; app unknown không được tính unseen.
- Mọi confirm key phải absent khỏi prompt, reward cache, retrieval, candidate và human-pilot files.

## 16. Artifacts và hash

Mỗi run lưu:

- `manifest.json`.
- `config.json`.
- `environment.txt`.
- Code snapshot/hash.
- Model/reference tree hash.
- Prompt keys raw/canonical SHA-256.
- Split SHA-256.
- Action verifier SHA-256.
- Counterfactual SHA-256.
- Tuple cache SHA-256.
- Reward definition SHA-256.
- First-batch records.
- Train log.
- Checkpoints.
- Validation predictions/raw scores.
- Checkpoint decision.
- Confirm predictions/raw scores.
- Runtime/VRAM.

**JSONL:**

- Raw byte hash.
- Data/split canonical schema bắt buộc `(source_dataset, episode_id, step_id)`; nếu raw thiếu `source_dataset`, canonicalizer inject constant source ID từ manifest nhưng không sửa raw.
- Data/split JSONL sort theo ba field trên.
- Run/prediction/reward JSONL dùng composite key quy định dưới.

Không chỉ dùng MD5.

**Run ID:**

```text
rgtc-v1__track-{A_INTERNAL|B_NEW_HOLDOUT}__tier-{MINIMUM_18|STRONG_23|SEED_GENERALIZED}__arm-{ARM}__seed-{SEED}
```

**Canonical JSONL:**

- UTF-8 NFC.
- JSON keys sort.
- Separators `,` và `:`.
- Newline LF.
- Single-prediction sort `(run_id, episode_id, step_id, checkpoint)`.
- Multi-sample reward/prediction sort `(run_id, episode_id, step_id, checkpoint, sample_id, pair_side)`.
- Field thuộc schema tương ứng là bắt buộc; thiếu field → STOP, không default.
- Duplicate composite key → STOP.

## 17. Ngân sách

Ước tính phải cập nhật sau smoke:

- Một GRPO 500 bước baseline: ~20,8 T4-hour.
- RGTC: ~23–27 T4-hour.
- SFT-cont đã đo: 1,86 T4-hour, 13,4 s/bước, VRAM 10,94 GiB.
- Validation 5 checkpoint: ~4–7 T4-hour/arm.
- Eval một checkpoint: ~9–11 T4-hour.

Seed-101 screen 7 RL arm + validation:

- ~180–247 T4-hour.

Minimum đúng 18 RL run:

- ~530–720 T4-hour cả train/validation/eval.

Strong đúng 23 RL run:

- ~710–955 T4-hour.

Các envelope trên chưa gồm chi phí grounder thứ hai, human study hoặc thu thập holdout. Sau khi user chọn evaluator, phải benchmark riêng và cộng vào manifest trước khi duyệt `STRONG_23`.

Claim tổng quát qua seed với ≥8 paired seeds cho năm primary methods cần ngân sách lớn hơn; phải tính lại sau smoke, không chép một con số giả chính xác.

Không trộn T4/fp16 và A100/bf16 trong cùng phép so nhân quả. Nếu đổi máy, chạy lại toàn bộ arms thuộc phép so.

## 18. Kill gates

Dừng ngay khi:

- Thiếu SFT-cont weights.
- Split overlap.
- SPICE/JVM lỗi, thiếu key, sai `2N`, NaN/Inf.
- Action precision exact lower bound `≤98%`.
- False reject action-class exact upper bound `≥5%`.
- Active target coverage `<20%` (sửa 10/11; bản gốc 30%).
- Gold target false rejection `>5%`.
- Negative `T<0,5` ở `<95%` mẫu.
- Audit `<190/200` hoặc có cặp đổi action.
- Merge/logits/reference/resume fail.
- Vượt speed/walltime gate đã khóa cho hardware.
- KL rolling `>0,10` hoặc non-finite.
- Unknown tăng `>2 pp`.
- Empty tăng `>0,5 pp`.
- Truncated tăng `>1 pp`.
- Không checkpoint feasible.

> **Giới hạn nguồn:** Ảnh 1 dừng ngay sau dòng “không checkpoint feasible”. Nếu Markdown gốc còn nội dung phía dưới thì không xuất hiện trong bộ ảnh ZIP, nên không thể chép tiếp mà không có ảnh bổ sung hoặc file nguồn.
