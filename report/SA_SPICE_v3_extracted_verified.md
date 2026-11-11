# QUYẾT ĐỊNH SAU RGTC TRƯỢT — SA-SPICE-v3 — 11/11/2026

> **Phán quyết: dừng RGTC target contrast. Không train FULL/RGTC.**
>
> **Đăng ký nghiên cứu mới:**
>
> ## GRPO + SA-SPICE-v3
>
> **Sparse-Aware Action-Corrected SPICE**
>
> Đây là nghiên cứu mới, không phải RGTC rút gọn và không dùng lại C1/test để tuning.

## 0. Vì sao chốt hướng này

### Target contrast đã trượt

Trên C1:

```text
FULL – A2 = 0,0000
KTC95 = [−0,0121; +0,0102]
```

Target **T** có tín hiệu riêng ở một số cặp nhưng không tạo marginal gain khi ghép vào reward.

### Sparse+action là candidate, chưa phải winner

Trên C1 reused validation:

| Reward | tap concordance | tap zero-std | tap oracle uplift |
|---|---:|---:|---:|
| SPICE lịch sử | 0,6846 | 7,23% | +11,33 pp |
| fixed SPICE+chrF | 0,7929 | 0,80% | +13,35 pp |
| R4 sparse+action kit | 0,8161 | 1,20% | +14,16 pp |
| chrF-only | **0,8355** | — | chưa dùng làm claim |

Toàn bộ/non-tap của R4:

- all concordance: 0,8401;
- non-tap: 0,8917;
- scroll/back: 1,0 trong proxy C1.

Nhưng:

- R4−chrF khoảng **−0,018**, KTC95 phủ 0;
- R4−sparse-only chỉ khoảng **+0,024**, KTC95 chạm/phủ 0;
- non-tap dùng cùng action heuristic với reward nên có tính vòng tròn;
- R4 hard-gate khác công thức v3;
- C1 là reused validation và chỉ S1/101.

Vì vậy **pilot chỉ tạo giả thuyết, không xếp hạng SA-SPICE-v3**. chrF là baseline bắt buộc.

### Vì sao không chọn hướng khác

**Action-SPIDEr**

- prior mạnh;
- nhưng chưa có GPU result trong dự án;
- CIDEr-D hiện chỉ `exec=60,27`;
- offline SPIDEr thấp hơn ROUGE-L và gần SA.

Giữ làm baseline bắt buộc.

**SPICE+ROUGE-L+action**

- ROUGE-L hiện `exec=60,63`;
- nhưng dễ xuất hiện mixture sau khi thấy số này sẽ bị gọi metric shopping;
- không có prior trực tiếp mạnh như SPIDEr.

Giữ GRPO+ROUGE-L làm baseline, không dùng làm phương pháp đề xuất.

## 1. Claim hẹp

Được nghiên cứu:

> Formulate and evaluate a SPICE-centered reward with tuple-sparsity interpolation and reliability-aware action correction for natural-language GUI instruction generation, optimized with GRPO.

Không claim:

- phát minh SPICE;
- phát minh GRPO;
- phát minh action reward;
- first;
- best/SOTA trước confirm;
- target-aware;
- RGTC validated.

Novelty mức vừa-thấp. Giá trị chính:

1. đo hai lỗi chuyển miền của SPICE trên GUI;
2. nội suy theo độ thưa tuple;
3. action correction chỉ khi metadata đáng tin;
4. đánh giá matched với SPICE/SPIDEr/ROUGE và non-tap.

## 2. Công thức khóa

Với câu sinh $y$, câu gold $g$:

$$
s = \operatorname{SPICE}(y,g), \qquad c = \operatorname{chrF}(y,g)/100.
$$

Số tuple gold:

$$K_g = |T(g)|.$$

Trọng số semantic:

$$\alpha_g = 0{,}8\min(1,K_g/3).$$

Sparse semantic score:

$$S = \alpha_g s + (1-\alpha_g)c.$$

Action score:

$$A \in \{0; 0{,}5; 1\}.$$

- **A = 1**: đúng canonical action chắc chắn;
- **A = 0**: sai action/toggle chắc chắn;
- **A = 0,5**: unknown hoặc metadata untrusted.

Length penalty:

$$d = \min\bigl(0{,}05,\;0{,}02\max(0,n_w(y)-n_w(g)-3)\bigr).$$

Reward:

$$\boxed{R_{SA\text{-}v3}=\operatorname{clip}_{[0,1]}(0{,}8S+0{,}2A-d)}$$

Câu rỗng reward **0**.

SPICE parser/JVM missing/NaN/exception → **dừng**. Không đổi lỗi thành 0.

### 2bis. Scorer và baseline contract

Ghim trong manifest:

- `pycocoevalcap` source hash;
- `spice-1.0.jar` + CoreNLP JAR hashes;
- Java/Python/sacrebleu versions;
- tokenizer/version từng metric.

Tuple count $K_g$:

- object: `O|object`;
- attribute: `A|object|attribute`;
- relation: `R|subject|relation|object`;
- mỗi field NFC/lowercase/collapse whitespace;
- deduplicate theo tagged serialization.

Mọi reward: câu rỗng = 0, scorer missing/None/NaN/Inf → **STOP**.

Baseline:

```text
chrF = sacrebleu.sentence_chrf(...).score / 100
CIDEr = CiderD.score(...)/10, DF chỉ từ TRAIN-v3 gold
SPIDEr-like = clip(0.5*SPICE + 0.5*CIDEr - d, 0, 1)
ROUGE-L = pycocoevalcap.Rouge.calc_score trên tokenizer đã pin
ROUGE reward = clip(ROUGE-L - d, 0, 1)
```

Mọi arm dùng cùng empty handling, penalty và clipping; khác biệt phải ghi rõ trong arm ID.

## 3. Vì sao hệ số 0,8/0,2

Đây là fallback đã được ghi trước khi RGTC trượt:

- semantic giữ vai trò chính;
- action chỉ correction;
- không thêm hệ số mới sau C1;
- không sweep weight trên test.

Coefficient không đồng nghĩa 80% gradient vì GRPO còn group-normalize.

Phải log:

- variance từng channel;
- pair-flip;
- zero-std;
- clipping;
- unknown coverage.

## 4. Dữ liệu mới — tuyệt đối không dùng C1/test để chọn

### 4.1 Exclusion

Loại toàn episode liên quan:

- C1;
- project test;
- val400/600;
- 1.000 prompt SFT-cont;
- ck500/GRPO-point và mọi run lịch sử;
- retrieval/candidate artifacts;
- mọi `prompt_keys` trong repo;
- near-duplicate image/goal/history.

### 4.2 Split

Từ pool còn lại, sau khi khôi phục đầy đủ lineage/ảnh:

- `TRAIN-v3`: 1.000 step, tối đa một step/episode;
- `DEV-v3`: 600 episode;
- `CONFIRM-v3`: 1.500 episode.

**Episode-disjoint tuyệt đối.**

Chia deterministic:

- strata = dominant action × episode-length bucket;
- hash seed cố định;
- freeze manifest/hash trước output.

Đặc tả:

- key bắt buộc `(source_dataset, episode_id, step_id)`;
- duplicate key/thiếu lineage → STOP;
- length bucket `1–4`, `5–9`, `≥10`;
- dominant action hóa → bytewise action name;
- trong stratum sort `SHA256("sa-spice-v3|source_dataset|episode_id")`;
- quota largest-remainder, tie bytewise;
- DEV/CONFIRM chấm toàn bộ step của episode đã chọn;
- TRAIN chọn tối đa một step/episode bằng `SHA256("sa-spice-v3-step|source_dataset|episode_id|step_id")`;
- exact image SHA trùng → cùng group/exclude;
- pHash DCT 63-bit, Hamming ≤4 → near-duplicate/exclude;
- text normalize NFC/lowercase/whitespace, MinHash token-3gram ≥0,90 → manual adjudication;
- confirm key phải vắng prompt/reward cache/retrieval/candidate/human-pilot files;
- freeze raw/canonical split hash trước mọi model/reward/evaluator output.

Manifest phải in step/episode/package counts theo action cho cả ba split.

`CONFIRM-v3` không được mở trước khi khóa formula, code, seeds, checkpoint rule và analysis.

### 4.3 Phạm vi claim

Pool này S1 đã thấy.

Tên đúng:

> RL-stage-held-out, S1-seen internal confirmation.

Không gọi:

- task-unseen;
- app-unseen;
- generalization;
- external clean test.

## 5. Action verifier gate

Verifier trusted khi:

1. action log hợp lệ;
2. action suy từ gold khớp log;
3. không mâu thuẫn wait/action;
4. verifier version/hash khóa trước.

Candidate:

- đúng → 1;
- sai chắc chắn → 0;
- unknown → 0,5.

Audit set độc lập, khóa trước:

- one-sided Clopper–Pearson 95% lower bound PPV của nhãn `known wrong` >98%;
- one-sided lower bound PPV của nhãn `correct` >98%;
- upper bound false reject trên candidate thật sự đúng, từng active action <5%;
- upper bound false accept trên candidate thật sự sai, từng active action <5%;
- unknown không ép tap;
- chưa dùng scroll direction ở v3.

Audit phân tầng theo action/toggle, blind với verifier output. Cỡ mẫu từng stratum phải đủ để bound có thể đạt; không dùng một tổng n=300 nếu class hiếm không đủ denominator.

Gate trượt:

> **SA-SPICE-v3 NO-GO.**

Không neutral toàn bộ action rồi vẫn giữ tên SA-SPICE.

## 6. Ma trận thực nghiệm

Ba fresh paired seeds:

```text
401, 503, 907
```

Seed 101/C1 không tham gia inference.

### 6.1 Factorial cơ chế 3×2

| Semantic | Action neutral | Action on |
|---|---|---|
| pure SPICE | `SPICE-MATCH = clip(0,8s+0,1−d)` | `Action-SPICE = clip(0,8s+0,2A−d)` |
| fixed mix | `FIXED = clip(0,8(0,8s+0,2c)+0,1−d)` | `FIXED+A = clip(0,8(0,8s+0,2c)+0,2A−d)` |
| adaptive sparse | `Sparse-SPICE = clip(0,8S+0,1−d)` | `SA-SPICE-v3 = clip(0,8S+0,2A−d)` |

*Các biểu thức `clip` trong bảng đều giới hạn về [0,1].*

Contrast:

- thêm chrF: FIXED − SPICE-MATCH;
- adaptive routing: Sparse-SPICE − FIXED;
- action trên pure: Action-SPICE − SPICE-MATCH;
- action trên adaptive: SA-SPICE − Sparse-SPICE;
- action×routing interaction: `[(SA−Sparse) − (FIXED+A−FIXED)]`.

### 6.2 Baseline bắt buộc

- SFT-cont, không RL;
- GRPO+chrF;
- GRPO+SPIDEr-like;
- GRPO+ROUGE-L.

### 6.3 Run count

- 6 factorial arms ×3 seed = **18**;
- chrF/SPIDEr-like/ROUGE-L ×3 seed = **9**;
- tổng **27 RL runs**;
- SFT-cont là fixed non-RL comparator.

Không chọn seed đẹp. Training divergence là outcome.

## 7. GRPO recipe

Mọi arm:

- cùng `sft_cont_merged`;
- cùng 1.000 TRAIN-v3 prompt/order;
- `G=8`;
- 2 prompt/update;
- 500 update;
- temperature 1,0;
- top-p 1, top-k 0;
- max completion 96;
- LR `1e-5`;
- group std;
- DAPO token aggregation;
- KL `β=0,04`;
- `num_iterations=1`;
- grad clip 1,0;
- vision frozen;
- cùng hardware/dtype.

Không thay weight/reward giữa seed.

## 7bis. Evaluator/generation contract

Khóa trước train:

- UGround checkpoint/revision/hash;
- processor, prompt template, image resize;
- independent `action_ok` parser, không dùng reward verifier;
- `±14%`/Voronoi implementation và inventory builder hash;
- deterministic greedy, `do_sample=False`, `max_new_tokens=96`, EOS `<|im_end|>`;
- một prediction artifact/hash dùng lại cho mọi evaluator/metric.

DEV deltas luôn so với SFT-cont trên cùng item.

One-SE rule:

1. cluster = package ID; thiếu package ở bất kỳ DEV row → endpoint chỉ descriptive/STOP checkpoint inference, không fallback hậu nghiệm;
2. yêu cầu ≥30 package clusters;
3. bootstrap 10.000 lần trên checkpoint có mean cao nhất $M$;
4. `SE(M)` là SD bootstrap, không reselect trong replicate;
5. chọn checkpoint sớm nhất có mean ≥ $M−SE(M)$.

## 8. DEV/checkpoint

Chấm step:

```text
100, 200, 300, 400, 500
```

Feasible nếu:

- non-tap không giảm >3 pp;
- scroll/back không giảm >5 pp;
- unknown không tăng >2 pp;
- empty không tăng >0,5 pp;
- truncated không tăng >1 pp;
- KL finite, rolling-20 ≤0,10.

Mọi delta feasibility tính trên **mean ba seed** của arm so với SFT-cont trên cùng item. Báo từng seed nhưng không loại arm chỉ vì một seed xấu; không optional-stop.

Chọn một checkpoint chung cho ba seed mỗi arm:

1. mean tap `exec` qua ba seed;
2. one-SE rule;
3. checkpoint sớm nhất trong 1 SE cực đại;
4. không feasible → arm fail.

Chỉ mở CONFIRM khi:

- SA-SPICE point estimate cao hơn SPICE-MATCH;
- SA-SPICE point estimate cao hơn Sparse-SPICE;
- bounded-harm DEV pass.

Trượt:

> dừng, báo DEV âm, không đổi 0,8/0,2.

## 9. Primary confirmatory

Primary endpoint:

$$\text{tap exec}=\text{action\_ok}\ \land\ \pm14\%\ \land\ \text{Voronoi}. $$

Primary family:

1. SA-SPICE − Sparse-SPICE — công action;
2. SA-SPICE − FIXED+A — công adaptive tuple routing khi action bật;
3. SA-SPICE − SPICE-MATCH — công toàn reward mới;
4. SA-SPICE − chrF — so semantic baseline mạnh trong pilot;
5. SA-SPICE − SPIDEr-like — so prior reward lại;
6. SA-SPICE − ROUGE-L — so reward có điểm GPU mạnh nhất trong lưới hiện tại.

Holm familywise 0,05.

Phân tích conditional trên ba fixed seeds:

1. mean outcome qua seed ở từng item;
2. paired difference;
3. cluster = package ID; thiếu package → endpoint estimation-only, không fallback hậu nghiệm;
4. yêu cầu ≥30 package clusters;
5. cluster bootstrap 10.000;
6. one-sided wild cluster bootstrap-t 100.000, center dưới null;
7. báo raw p, Holm p, KTC95 hai phía và từng seed.

Pass:

- effect >0;
- p qua Holm.

Practical target +1 pp chỉ là target; không đổi thành criterion hậu nghiệm.

Trước CONFIRM, dùng DEV/blinded pilot để estimate discordance, cluster ICC và số tap/scroll/back; không xem treatment mean difference. Simulation power phải đạt ≥80% cho +1 pp và ba NI margins. Endpoint thiếu lực được khóa trước là `estimation-only/unresolved`.

Secondary:

- Sparse-SPICE − FIXED — adaptive routing khi action neutral;
- SA-SPICE vs SFT-cont;
- factorial interaction.

Chỉ khi cả sáu phép primary qua Holm mới được nói SA-SPICE tốt nhất trong các reward alternatives đã đăng ký.

## 10. Non-tap bắt buộc

Endpoint: canonical action-class accuracy, không chấm hướng scroll.

So SA-SPICE với SFT-cont.

Non-inferiority margins:

- all non-tap: −1 pp;
- scroll: −2 pp;
- back: −2 pp.

Pass khi one-sided 95% lower bound > margin cho cả ba.

Dùng cùng mean-ba-seed aggregation và package-cluster bootstrap như primary. One-sided lower bound = percentile 5% của bootstrap distribution. Endpoint thiếu ≥30 package clusters hoặc power <80% được khóa trước là `estimation-only/unresolved`.

Trượt:

> tap gain đi kèm trade-off; không nói no-harm/cải thiện tổng thể.

## 11. Secondary diagnostics

- D.3/AitW;
- action/target decomposition;
- SPICE/CIDEr-D/ROUGE-L/chrF;
- length/repetition/distinct-1/2;
- empty/malformed/no-action-verb;
- zero-std/tie;
- reward channel variance;
- pair-flip;
- best-of-8;
- compute/VRAM;
- proxy-exec theo checkpoint.

Secondary không cứu primary.

## 12. Human/evaluator

Nếu claim instruction tốt hơn:

- 300 CONFIRM prompts khóa trước output;
- 3 blind raters/pair;
- SA-SPICE vs strongest matched baseline;
- đúng action;
- đúng target/groundability;
- dễ làm theo;
- tự nhiên/rõ;
- overall preference.

Ngoài ra:

- audit verifier độc lập, phân tầng; cỡ từng stratum do exact-bound power quyết, không dùng một tổng n=300 thay cho denominator từng action;
- grounder thứ hai nếu có.

Không có human/independent evaluator:

> hạ claim về automatic proxy.

## 13. Stop rules

Dừng trước GPU nếu:

- split/manifest/hash thiếu;
- SFT-cont weights/ảnh thiếu;
- action verifier gate trượt;
- SPICE parse fail-open;
- smoke/resume/merge/logits fail.

Trong train chỉ dừng vì technical failure đã khóa:

- NaN/Inf;
- KL rolling >0,10;
- empty +0,5 pp;
- unknown +2 pp;
- truncation +1 pp;
- OOM.

Không dừng vì seed đầu xấu. Chạy đủ ba seed.

## 14. Câu được phép viết

Nếu primary pass:

> Trên internal confirmation episode-disjoint ở tầng RL nhưng đã được S1 thấy, GRPO với SA-SPICE-v3 cải thiện tap executability so với sáu controls/reward alternatives trong primary family đã đăng ký, conditional trên ba seed cố định.

Nếu action contrast pass:

> Reliability-aware action correction có marginal contribution ngoài sparse semantic fallback.

Không được viết:

- SA-SPICE tốt nhất/SOTA;
- generalizes/app-unseen;
- action correction cải thiện target;
- RGTC chứng minh SA-SPICE;
- C1 chứng minh method;
- no-harm nếu NI chưa pass;
- stable nếu chưa seed-generalized.

## 15. Quyết định cuối

### Chọn

> **GRPO + SA-SPICE-v3**

### Không chọn

- RGTC target contrast;
- SPICE+ROUGE custom method;
- Action-SPIDEr làm main method.

### Lý do

- target đã fail marginal gate;
- SA là fallback đã viết trước;
- pilot R4 tốt hơn SPICE/fixed mixture ở một số chỉ báo nhưng chưa hơn chrF; chỉ đủ đề cử, không chứng minh winner;
- công thức đơn giản;
- vẫn đúng hướng GRPO+SPICE;
- dễ ablate và bảo vệ hơn các mixture hậu nghiệm.

### Trạng thái

> **PREFLIGHT / NO-GO GPU** cho tới khi có split mới, action verifier audit, SFT weights, ảnh, manifest/hash và protocol freeze.

## 16. Việc user phải quyết

1. Có chấp nhận dừng RGTC và đăng ký SA-SPICE-v3 không?
2. Có cấp SFT-cont `final/`, ảnh và metadata không?
3. Có duyệt ngân sách 27 RL runs cho factorial + chrF/SPIDEr-like/ROUGE-L không?
4. Có chấp nhận kết quả âm không đổi hệ số không?
5. Có human/grounder thứ hai không?

Agent không được tự quyết.

## 17. Prompt gửi chat thi hành

```text
Đọc QUYET_DINH_SAU_RGTC_TRUOT_SA_SPICE_V3_11_11.md.

RGTC target đã dừng. Không sửa gate cũ và không dùng lại C1/test để tune.
Candidate mới là GRPO + SA-SPICE-v3.

Nhiệm vụ hiện tại chỉ PREFLIGHT:
1) kiểm SFT-cont weights/ảnh/metadata,
2) dựng lineage + split spec,
3) viết action verifier audit plan,
4) đóng băng formula/seeds/checkpoint/analysis,
5) trả GO/NO-GO.

Chưa chạy GPU.
```

*Hết — decision memo 11/11/2026. Đây là nghiên cứu mới; phải hash/timestamp trước bất kỳ DEV-v3 rollout nào.*
