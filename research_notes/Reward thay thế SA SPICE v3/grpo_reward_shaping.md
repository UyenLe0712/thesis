# Multi-reward aggregation and reward shaping in GRPO-family algorithms (2024–2026), for dense-but-noisy metric rewards on short text

Scope note: these notes come from 15 tool calls, mostly against primary pages (arXiv abstract/HTML pages, TRL docs, NeurIPS proceedings). Where only a search snippet or a third-party summary was available, the note says so. "Preprint" means I found no peer-reviewed venue at the source.

## Q1. Multi-reward aggregation: sum-then-normalize vs normalize-each-then-sum, weighting, gating

### Takeaway
Two independent 2025–2026 papers (GDPO, NVIDIA tech report, preprint; MO-GRPO, arXiv 2509.22047, which appears to be a 2026 TACL paper but I could not confirm that) both show that GRPO's default "sum the rewards, then z-score inside the group" has two problems. It lets the highest-variance component drive the advantage, and it maps distinct reward combinations onto the same advantage. Both fix this by normalizing each reward within the group before summing. TRL now ships this as `multi_objective_aggregation="normalize_then_sum"`. For priorities, GDPO finds that gating (conditioning) works better than weights.

### Cited Findings
- **GRPO baseline (sum-then-normalize).** TRL documents its default: "First sums the weighted rewards from each reward function, then applies reward scaling/normalization as specified by `scale_rewards`." The advantage is Â = (r_i − mean(r))/std(r), where r = Σ_k w_k r_k. — [TRL GRPOTrainer docs](https://huggingface.co/docs/trl/main/en/grpo_trainer)
- **GDPO formula.** Liu, Dong, Lu, …, Choi, Kautz, Molchanov, "GDPO: Group reward-Decoupled Normalization Policy Optimization for Multi-reward RL Optimization", arXiv 2601.05242, 8 Jan 2026, labelled "NVIDIA-Tech Report", **preprint**. The steps are:
  - Eq. 4: A_k^(i,j) = (r_k^(i,j) − mean_j r_k^(i,·)) / std_j r_k^(i,·), computed per reward k within the group.
  - Eq. 5: A_sum = A_1 + … + A_n.
  - Eq. 6: A_sum is then normalized over all questions in the batch, with ε in the denominator, "so the numerical scale … does not grow as additional rewards are introduced".
  - Eq. 7 (weighted): A_sum = Σ w_k A_k.
  — [GDPO HTML](https://arxiv.org/html/2601.05242v1); [abstract](https://arxiv.org/abs/2601.05242)
- **GDPO's "advantage collapse" example.** With 2 rollouts and two binary rewards (total reward ∈ {0,1,2}), GRPO maps (0,1), (0,2) and (1,2) all to (−0.7071, +0.7071). GDPO maps (0,1) to ±0.7071 and (0,2) to ±1.4142, so it keeps the "both satisfied" signal. Dropping only std normalization gives just "modest gains" in the number of distinct advantage groups. — [GDPO HTML](https://arxiv.org/html/2601.05242v1)
- **GDPO results** (GRPO → GDPO):
  - Tool calling, BFCL-v3, averaged over 5 runs: Qwen2.5-1.5B 30.18 → 32.81% accuracy and 76.33 → 80.66% correct format; Qwen2.5-3B 39.20 → 40.87% accuracy and 81.64 → 82.23% format.
  - Math with a 4,000-token length constraint: DeepSeek-R1-1.5B on AIME, accuracy 23.1 → 29.4% and over-length 10.8 → 6.5%.
  - Coding: Codecontests pass rate 63.2 → 65.8%.
  - GRPO without std normalization reached 29.26% accuracy but **0% correct format** (1.5B, tool calling). Removing std scaling is therefore not a safe fix.
  — [GDPO HTML](https://arxiv.org/html/2601.05242v1)
- **GDPO caveats.** Runs without the batch-wise normalization step "occasionally fail to converge" (Appendix A). Run counts are given only for tool calling (5 runs). GDPO showed higher variance in the number of steps needed to converge on the format reward. — [GDPO HTML](https://arxiv.org/html/2601.05242v1)
- **Weights are unreliable when one reward is much easier.** The model maximizes the easy reward almost regardless of its weight. Lowering the length-reward weight to 0.75 or 0.5 "had little effect"; a clear change appeared only at 0.25. — [GDPO HTML](https://arxiv.org/html/2601.05242v1)
- **Conditional (gated) reward, GDPO Eq. 8.** r_k is kept only if another reward r_l ≥ t, and otherwise set to 0. In their math task, the length reward is 1 only when the answer is also correct. GDPO with the conditioned length reward beat GRPO with the same reward by +4.4% AIME accuracy, with 16.9% fewer over-length responses. The trade-off is that the conditioned version relaxes the constraint (GDPO AIME over-length 12.3% conditioned vs 0.2% unconditioned). — [GDPO HTML](https://arxiv.org/html/2601.05242v1)
- **MO-GRPO.** Ichihara et al., "MO-GRPO: Mitigating Reward Hacking of Group Relative Policy Optimization on Multi-Objective Problems", arXiv 2509.22047 (v1 Sep 2025, v2 9 Jan 2026). The arXiv page shows no venue. A search hit lists an ACL Anthology TACL 2026 PDF (2026.tacl-1.84) next to it, but I did **not confirm** that this PDF is MO-GRPO.
  - Advantage: A_g^MO = Σ_i (R_i(q,o_g) − mean(R_i)) / std(R_i), with per-objective group statistics.
  - Theorem 1: under GRPO, corr(advantage, R_i) = (σ_i² + X)/(σ·σ_i), where X sums the covariances with the other rewards. The authors conclude GRPO is "biased toward reward functions with high variance", so low-variance objectives get ignored.
  - The authors say the method preserves the preference ordering under positive affine rescaling of each reward, so manual scale tuning is not needed.
  — [MO-GRPO HTML v2](https://arxiv.org/html/2509.22047v2); [search listing incl. TACL hit](https://aclanthology.org/2026.tacl-1.84.pdf)
- **MO-GRPO on machine translation (metric rewards, closest analogue to this thesis).** Rewards were BLEURT plus a readability scorer (jReadability for En-Ja, TRank for En-Zh), on Qwen2.5-3B-Instruct, Llama-3.2-3B and Sarashina, training on WMT-21/22/23 and testing on WMT-24.
  - Under plain GRPO, Llama En-Ja raised jReadability 0.67 → 0.90 while BLEURT fell 0.65 → 0.60, and the GPT-4o-mini judge win rate dropped to 35.6% (base = 50%).
  - In En-Zh, 68.7% of GRPO outputs were not in Chinese (base 14.7%, MO-GRPO 5.6%).
  - MO-GRPO (Llama En-Ja) reached BLEURT 0.66, jReadability 0.69 and a 68.8% judge win rate.
  - On AlpacaFarm, GRPO and Dr.GRPO sacrificed the length reward to raise the RM score, while MO-GRPO kept it.
  — [MO-GRPO HTML v2](https://arxiv.org/html/2509.22047v2)
- **TRL support.** `multi_objective_aggregation` supports `"sum_then_normalize"` (default) and `"normalize_then_sum"`. The latter is described as: "First normalizes/scales each reward function across generations (within each group), then sums the normalized rewards using the specified weights. The aggregated reward is then normalized at the batch level … the suggested approach from [GDPO]." Other relevant options:
  - `reward_weights` (default: all 1.0).
  - A reward function may return `None` for a sample, which excludes that function for that sample.
  — [TRL GRPOTrainer docs](https://huggingface.co/docs/trl/main/en/grpo_trainer)

### Inferences
- The thesis composite R = clip(0.8·[α·SPICE + (1−α)·chrF] + 0.2·ActionMatch − lenPen) is aggregated sum-then-normalize. By MO-GRPO's Theorem 1, the within-group advantage is driven mainly by whichever component has the larger within-group variance.
  - chrF is continuous and almost never ties. SPICE ties often (≈6% of groups have zero std, plus many partial ties).
  - So the "SPICE-centered" composite is most likely chrF-driven in practice. That fits two observations: the composite gives about the same exec gain as pure chrF (+0.30 ns), and the composite's concordance (0.771) sits near chrF/ROUGE rather than SPICE (0.677).
  - Fixing α by gold tuple count does not prevent this, because α scales the raw reward, not its within-group variance.
- ActionMatch is binary and mostly 1 on tap steps, so its within-group variance is near zero and it contributes almost nothing under sum-then-normalize. Under normalize-then-sum it would get full weight in the rare groups where it varies. That is exactly where the "back/scroll written as tap" failures happen.
- GDPO's finding that weights barely move an easy objective (meaningful change only at 0.25) suggests that tuning α or the 0.8/0.2 split is a weak lever compared with changing the aggregation or adding gating.

### Gaps
- No paper found that tests GDPO or MO-GRPO on a reward where one component is **tie-heavy and low-variance** (like SPICE on 0–3 tuples). Per-component group-std normalization of such a component can amplify tiny differences, as discussed under Q2.
- The MO-GRPO venue (TACL 2026) is unconfirmed. GDPO is a tech report with no peer review.

## Q2. Ties and zero-variance groups: dynamic sampling, tie-breaking, rank advantages

### Takeaway
DAPO (NeurIPS 2025) drops groups whose rewards are all equal and resamples. In DAPO's math setting this was the single biggest late-stage gain, but there zero-variance groups were common. With ≈6% zero-std groups here, filtering mainly removes wasted compute. The bigger problem is **partial ties plus std normalization**: when only one sample breaks a tie by a small amount, z-scoring inflates that gap to a full-size advantage. Remedies in the literature:
- Rank-based advantages (GOPO, preprint).
- A secondary tie-breaking signal kept subordinate to the primary reward (RLRR, preprint).
- Synthetic signal for homogeneous groups (NGRPO, AGPO, preprints).
- Batch-level std instead of group std (TRL `scale_rewards="batch"`, from Lite PPO, preprint).

### Cited Findings
- **DAPO.** Yu et al., "DAPO: An Open-Source LLM Reinforcement Learning System at Scale", NeurIPS 2025 per mlanthology; official proceedings page not opened; arXiv 2503.14476.
  - Dynamic sampling over-samples and filters out prompts whose group accuracy is 0 or 1, so every batch has a non-zero gradient signal.
  - Clip-Higher decouples the lower and upper clip ranges to fight entropy collapse.
  - One review reports that dynamic sampling raised AIME from 42 to 50 in the ablation (third-party figure; I did not check it against the paper).
  — [mlanthology NeurIPS 2025](https://mlanthology.org/neurips/2025/yu2025neurips-dapo); [arXiv](https://arxiv.org/abs/2503.14476v1); [liner review](https://liner.com/review/dapo-opensource-llm-reinforcement-learning-system-at-scale)
- **RLRR**, "From Absolute to Relative: Rethinking Reward Shaping in Group-Based Reinforcement Learning", arXiv 2601.23058, Jan 2026, **preprint**. It replaces absolute rewards with within-group rankings from a listwise Ranking Reward Model. The ranking is used to break ties where ground-truth rewards are identical, "so ground truth remains primary while ties are broken by preference information". This description is from search snippets; I did not read the full text. — [arXiv PDF](https://arxiv.org/pdf/2601.23058); [alphaxiv](https://www.alphaxiv.org/abs/2601.23058)
- **GOPO**, arXiv 2602.03876, **preprint**. Its advantage keeps only the reward ranking and discards magnitudes, as opposed to GRPO's z-score. It is not framed as a tie-break mechanism (from snippet). — [arXiv PDF](https://www.arxiv.org/pdf/2602.03876)
- **NGRPO**, arXiv 2509.18851, preprint. It adds a virtual maximum-reward sample when computing advantages, so all-wrong groups get non-zero advantages. **AGPO**, arXiv 2503.15952, preprint, revises the advantage estimate for zero-variance groups. Both from snippets. — [NGRPO](https://arxiv.org/pdf/2509.18851v1); [AGPO](https://arxiv.org/html/2503.15952v3)
- **Batch-level std scaling.** In TRL, `scale_rewards="batch"` takes the mean within the group and the std across the whole batch, "as recommended in the PPO Lite paper". The source is Liu et al., "Part I: Tricks or Traps? A Deep Dive into RL for LLM Reasoning", arXiv 2508.08221, preprint. Its abstract says a "minimalist combination of two techniques" with the vanilla PPO loss outperforms GRPO and DAPO; the abstract does not name the techniques. — [TRL docs](https://huggingface.co/docs/trl/main/en/grpo_trainer); [arXiv 2508.08221](https://arxiv.org/abs/2508.08221)
- **Std-normalization difficulty bias.** Dividing by the per-question reward std over-weights questions whose rewards are very consistent, i.e. near-ties (Dr.GRPO). — [arXiv 2503.20783](https://arxiv.org/html/2503.20783v2)

### Inferences
- **Partial ties under group-std normalization.** Take a group of 8 where 7 samples have SPICE 0.40 and one has 0.45. Standard z-scoring gives that one sample an advantage of about +2.6 and the other seven about −0.38 each (sample std; the exact value depends on the std estimator). That is as large as a group where one sample is fully correct and seven are fully wrong. With 0–3 gold tuples, SPICE moves in large discrete steps, so tie-dominated groups are common. Std normalization therefore gives high-magnitude, low-reliability updates, which fits SPICE's low concordance (0.677).
- Batch std (`scale_rewards="batch"`) shrinks these updates in proportion to the true gap and needs no new hyperparameter. This is the cheapest cleanup.
- **Lexicographic reward.** R = SPICE + ε·chrF with small ε (e.g. 0.05) keeps SPICE primary. In groups that tie on SPICE, chrF decides the order. With group std this ordering is again blown up to full scale, with batch std it stays small. Precedent: RLRR's "ground truth primary, ranking breaks ties" (preprint).
- **Rank transform.** Mid-ranks for ties, then centering, makes the advantage invariant to SPICE's discrete scale. It optimizes exactly what the offline "concordance" measures. It cannot raise SPICE's own concordance; it only removes scale artifacts.
- **DAPO filtering at 6% zero-std groups** recovers at most about 6% of compute. With only 2 prompts per update, dropping a group halves that update's effective batch unless it is resampled. Expect a small benefit.

### Gaps
- I found no controlled study of tie-break or lexicographic rewards for **metric** rewards (BLEU, SPICE, CIDEr), and no head-to-head of rank vs z-score advantages on text-generation metrics. Neither GOPO's nor RLRR's numbers were verified.

## Q3. Rank, pairwise and relative rewards (BT-style, BRPO)

### Takeaway
Pairwise, reference-anchored advantages have been used to make GRPO work when scalar rewards are unreliable. Writing-Zero's BRPO compares each sample to a randomly chosen in-group reference with a pairwise judge (preprint). No 2025–2026 paper found applies pairwise or BT advantages to n-gram or scene-graph metrics.

### Cited Findings
- **Writing-Zero.** Jiang et al., arXiv 2506.00103, May 2025, **preprint**. It introduces a pairwise generative reward model and **BRPO (Bootstrapped Relative Policy Optimization)**, a GRPO variant that picks a reference response at random from the current group, so advantages have zero expectation. The pairwise GenRM turns subjective quality into "pseudo-verifiable binary signals". The motivation is that scalar RMs are prone to over-explanation and length hacking. A third-party summary reports WritingBench 6.89 → 8.29; not verified. — [arXiv PDF](https://arxiv.org/pdf/2506.00103); [emergentmind](https://www.emergentmind.com/papers/2506.00103)
- **GOPO** uses rank-only advantages (preprint; see Q2). — [arXiv PDF](https://www.arxiv.org/pdf/2602.03876)

### Inferences
- With a deterministic metric, a "pairwise reward" over a group of 8 equals a win-rate transform:

  A_i = (1/(G−1)) · Σ_{j≠i} sign(SPICE_i − SPICE_j), with ties counted as 0.

  That is a centered rank, so it adds nothing beyond the rank transform in Q2 unless the comparison itself uses extra information. One example of extra information: a pairwise SPICE comparison that also counts a chrF win when SPICE ties, which is the lexicographic idea again.

### Gaps
- No evidence found on BT or pairwise advantages for captioning or instruction metrics.

## Q4. Reward noise: how noisy or imperfect rewards affect GRPO, and reward-variance theory

### Takeaway
Razin et al. (NeurIPS 2025) prove that reward **variance** under the current policy, not only accuracy, controls how fast RLHF optimizes. A low-variance reward gives a flat objective even when it is accurate. Empirical RLVR results on noise conflict:
- Lv et al. (preprint) find GRPO tolerates 40% flipped rewards on math.
- A 2026 critique, per a search snippet only, argues the earlier robustness came from contamination.
- Spurious-reward gains (Shao et al., preprint) are model-dependent and attributed to clipping bias.

### Cited Findings
- **Razin et al., "What Makes a Reward Model a Good Teacher? An Optimization Perspective", NeurIPS 2025** (proceedings page found; arXiv 2503.15477).
  - Low reward variance gives a flat objective landscape and slow optimization, "regardless of how accurate a reward model is".
  - A perfectly accurate reward with low variance can be slower than less accurate, higher-variance rewards.
  - Variance is measured over the policy's own samples, so the same reward can teach one policy well and another poorly. Experiments go up to 8B models.
  — [NeurIPS 2025 proceedings](https://proceedings.nips.cc/paper_files/paper/2025/hash/554e056fe2b6d9fd27ffcd3367ae1267-Abstract-Conference.html); [arXiv](https://arxiv.org/abs/2503.15477)
- **Lv et al., "The Climb Carves Wisdom Deeper Than the Summit: On the Noisy Rewards in Learning to Reason"**, arXiv 2505.22653, May 2025, **preprint**.
  - With 40% of rewards flipped, Qwen-2.5-7B still improved from 5% to 72% on math, versus 75% with clean rewards.
  - Rewarding only reasoning-pattern phrases (RPR) gave over 70%.
  - RPR combined with noisy reward models reduced false negatives on open-ended tasks.
  — [arXiv](https://arxiv.org/abs/2505.22653)
- **Pushback and corrections, from search snippets only (papers not opened):**
  - A 2026 paper attributed to Zhu & Kang argues that the "noisy" sets contained correct answers labelled wrong, and that under truly noisy data RLVR collapses toward a format-only baseline.
  - Cai et al. (2025) model the verifier as an asymmetric FP/FN channel and propose backward and forward corrections.
  - Shao et al., "Spurious Rewards" (arXiv 2506.10947), find that random rewards lift Qwen2.5-Math, attribute this to GRPO clipping bias, and say it is model-dependent.
  — [search: arXiv 2603.16140](https://arxiv.org/pdf/2603.16140); [arXiv 2510.00915](https://arxiv.org/abs/2510.00915v1); [Spurious Rewards listing](https://www.opentrain.ai/papers/spurious-rewards-rethinking-training-signals-in-rlvr--arxiv-2506.10947)

### Inferences
- **SPICE is a weak teacher on both of Razin's axes for this task.**
  - It has lower within-group variance, because of ties: in Razin's terms, a flatter landscape.
  - It has lower "accuracy" with respect to the true objective (exec): concordance 0.677 vs chrF 0.794.
  - chrF scores higher on both, which matches its larger KL movement (0.11 vs 0.04) and its slightly better exec.
  - The flat training-reward curves for the composite are consistent with a low-variance teacher plus small batches (2 prompts/update × 500 updates ≈ 1,000 prompts).
- The math-RLVR noise-robustness results use binary correctness with ~0.5 base variance. They should **not** be taken to mean SPICE noise is harmless: SPICE's problem is low variance plus weak alignment with exec, not random flips.

### Gaps
- The attributions of Zhu & Kang (2026) and Cai et al. (2025) to the URLs above come from a search summary and need checking before citation.
- No quantitative study found linking reward-vs-downstream concordance to GRPO gains for text metrics. The offline concordance screen in this project seems to have no close published precedent.

## Q5. Std-normalization and length biases (Dr.GRPO) for short outputs

### Takeaway
Dr.GRPO identifies two biases in GRPO:
- A **length bias** from per-response 1/|o| normalization.
- A **difficulty bias** from per-question std normalization.

It removes both. For ~7-word outputs, the length bias is minor. The std/difficulty bias matters more because ties make group std small and noisy. TRL's default `loss_type="dapo"` (token-level normalization) already avoids the original length bias.

### Cited Findings
- **Liu et al., "Understanding R1-Zero-Like Training: A Critical Perspective"**, arXiv 2503.20783.
  - Per-response length normalization favors longer incorrect responses.
  - Per-question std normalization over-weights too-easy or too-hard (consistent-reward) questions.
  - Dr.GRPO drops both terms.
  - Venue: only a Hugging Face discussion page states COLM 2025, so this is **unconfirmed**.
  — [arXiv HTML](https://arxiv.org/html/2503.20783v2); [HF discussion re: COLM](https://huggingface.co/datasets/rl-llm-wiki/knowledge-base/discussions/95)
- **TRL `loss_type` options:**
  - `"grpo"` is "not recommended due to length bias: prefers shorter completions with positive advantages and longer ones with negative".
  - `"dr_grpo"` normalizes by the constant `max_completion_length`.
  - `"dapo"` (default) normalizes by active tokens in the global batch.
  - TRL also documents `scale_rewards="none"` as the Dr.GRPO recommendation.
  — [TRL docs](https://huggingface.co/docs/trl/main/en/grpo_trainer)
- **Caveat from GDPO.** Removing std normalization in multi-reward tool calling gave 0% correct format. — [GDPO HTML](https://arxiv.org/html/2601.05242v1)

### Inferences
- For short outputs, loss aggregation (dapo vs dr_grpo) should barely matter.
- The choice that matters is the scaling: group std, batch std or none. Batch std is the middle option: it keeps scale stability, which GDPO and Lite PPO find important, without the near-tie amplification.

### Gaps
- No study found of Dr.GRPO vs GRPO on very short outputs (<20 tokens).

## Q6. KL, reference choice, entropy collapse, number of updates

### Takeaway
The sources mostly offer **knobs** rather than evidence specific to this setting:
- DAPO's Clip-Higher against entropy collapse.
- Entropy bonuses (Skywork-OR1 adaptive entropy, available in TRL).
- Periodic reference resets (TR-DPO-style `sync_ref_model`).
- KL that the GRPO captioning paper credits with limiting over-fitting to high-reward outputs.

### Cited Findings
- **DAPO Clip-Higher** decouples the clip ranges "to promote diversity and prevent entropy collapse". — [arXiv 2503.14476](https://arxiv.org/abs/2503.14476v1); [AReaL docs](https://inclusionai.github.io/AReaL/algorithms/dapo.html)
- **TRL entropy and reference options:**
  - `entropy_coef`, plus adaptive entropy control from Skywork-OR1 (`use_adaptive_entropy`, `entropy_target`). TRL warns the default target of 0.2 nats "almost never triggers"; it should be set near the observed early entropy.
  - `top_entropy_quantile` (Beyond the 80/20 Rule; recommended 0.2).
  - `sync_ref_model` with π_ref = α·π_θ + (1−α)·π_ref_prev (TR-DPO).
  — [TRL docs](https://huggingface.co/docs/trl/main/en/grpo_trainer)
- **GRPO for image captioning with a CIDEr reward** (arXiv 2503.01333, **preprint**): GRPO on MSCOCO, reporting +2.4% CIDEr over SCST. The KL constraint is credited with limiting over-fitting to high-reward outputs, per a third-party summary; length gaming was not tested. — [arXiv PDF](https://arxiv.org/pdf/2503.01333); [chatpaper summary](https://chatpaper.com/paper/116899)

### Inferences
- KL 0.04 for the composite vs 0.11 for chrF, at the same β, indicates the composite moves the policy less. That fits a weaker effective signal (Q4), not over-regularization.
- Lowering β would not fix a low-variance reward. Raising signal quality (Q1/Q2 fixes) comes first.

### Gaps
- No source found giving update counts needed for short-text metric RL. Claims about "how many updates" could not be sourced.

## Q7. Reward-hacking mitigation for metric rewards

### Takeaway
Documented mitigations are:
- Per-objective normalization, so no single high-variance metric dominates (MO-GRPO on MT).
- Gating a secondary reward on a primary one (GDPO).
- KL to a reference.
- Using verifiable task-grounded rewards instead of judge scores (CapRL, a captioning precedent).

### Cited Findings
- Plain GRPO hacked the high-variance readability reward on MT, with BLEURT down and outputs drifting out of the target language. MO-GRPO fixed this. — [MO-GRPO HTML v2](https://arxiv.org/html/2509.22047v2)
- CapRL (from a snippet) replaces LVLM-judge captioning rewards, which favor verbose or overly brief captions, with a verifiable reward: the accuracy of an LLM answering multiple-choice questions from the caption, used inside GRPO. This is the same idea as using exec as a downstream-grounded reward. — [airaxiv](https://airaxiv.com/arxiv/pdf/3734); [chatpaper](https://chatpaper.com/paper/192229)
- Hacking reference-free captioning metrics raises scores while making captions unreadable. — [Frontiers of Computer Science](https://journal.hep.com.cn/fcs/EN/10.1007/s11704-025-50178-6)

### Inferences
- The observed **non-tap degradation** (back and scroll steps written as taps) is the same pattern as the MT hacking: the policy optimizes the components that vary most (n-gram overlap on tap-dominated data) and neglects a rare, low-variance objective (action type on non-tap steps). The documented fixes are per-component normalization and gating.

### Gaps
- No paper found that specifically studies hacking of SPICE or chrF under GRPO.

## Q8. Choosing reward weights without tuning on test

### Takeaway
Two principled, test-free options have precedent:
- **Normalize each component** (within the group: GDPO/MO-GRPO; or within the batch). This makes the method invariant to each reward's affine scale, so raw weights no longer carry hidden variance effects.
- **Gate rather than weight** when one objective must take priority.

Weights can then be set on dev or train screens, such as the existing offline concordance screen, never on test.

### Cited Findings
- MO-GRPO is invariant to positive affine rescaling of each reward, so manual scale tuning is not needed. — [MO-GRPO HTML v2](https://arxiv.org/html/2509.22047v2)
- GDPO: weights have little effect until they are extreme (0.25), and conditioning works better than reweighting for priorities. — [GDPO HTML](https://arxiv.org/html/2601.05242v1)

### Inferences
- **Variance matching.** w_k ∝ 1/σ_k, where σ_k is component k's std over a batch of rollouts from the SFT policy, computed on train prompts. This is the batch-level analogue of MO-GRPO, computed once before training. It avoids the group-level noise amplification for tie-heavy SPICE.

### Gaps
- No paper found comparing batch-level variance matching with group-level per-component normalization.

---

**Implications (ranked recipes for a SPICE-centered GRPO reward in this setting).** Each recipe gives its expected effect, risk, cost and precedent. All are inferences from the sources above, not measured results.

1. **Switch std scaling to batch level (`scale_rewards="batch"`).**
   - Effect: removes the near-tie amplification (Q2/Q5) that turns a 0.05 SPICE gap into a full-size advantage, so updates scale with true reward gaps.
   - Risk: low. GDPO and Lite PPO both use batch-level scale, and only a full removal of std scaling broke format learning in GDPO.
   - Cost: one config flag, zero GPU to implement.
   - Precedent: Lite PPO (preprint), TRL, GDPO Eq. 6.
2. **Lexicographic tie-break: R = SPICE + ε·chrF (ε ≈ 0.05–0.1), combined with recipe 1.**
   - Effect: SPICE stays primary, and the ≈6% zero-std groups plus the many partial-tie groups now get an ordering from the component with higher concordance (0.794). This should raise effective variance (Razin) without letting chrF dominate, because batch std keeps the ε term small.
   - Risk: medium. If ε is too large it becomes "chrF with extra steps". Choose ε on train/dev concordance, and report it as SPICE-primary only if most of the advantage mass still comes from SPICE (log the split).
   - Cost: trivial.
   - Precedent: RLRR's "ground truth primary, ranking breaks ties" (preprint).
3. **Gate the text reward on action type (GDPO Eq. 8 style).** For example R = 1[action_type(pred) = gold] · text_reward, or a separate action reward with per-component normalization.
   - Effect: directly targets the back/scroll-as-tap degradation, because a wrong action type can no longer earn n-gram credit.
   - Risk: medium. On tap-dominated data the gate rarely fires, so the effect is limited to non-tap prompts. A rule-based action-type parser may be noisy. GDPO shows gating trades off the gated constraint.
   - Cost: low.
   - Precedent: GDPO conditional reward (+4.4% AIME in their setting).
4. **Per-component normalize-then-sum (`multi_objective_aggregation="normalize_then_sum"`) for SPICE, chrF and ActionMatch, with an ε or std floor per component.**
   - Effect: removes the "highest-variance component wins" bias (MO-GRPO Theorem 1). SPICE and ActionMatch get real weight in the groups where they vary.
   - Risk: medium-high for SPICE specifically. Group-level per-component z-scoring amplifies tiny, tie-breaking SPICE gaps (Q2) and binary ActionMatch flips. Use a minimum std (e.g. clamp σ_k ≥ a train-estimated floor) or batch-level per-component σ (variance matching, Q8).
   - Cost: a flag in TRL, or a few lines in a custom trainer.
   - Precedent: GDPO (tech report), MO-GRPO (MT with BLEURT, possibly TACL 2026).
5. **Rank-transform the (lexicographic) reward within the group**: mid-ranks for ties, then centering.
   - Effect: scale-free advantages that optimize exactly the ordering measured by concordance. It is robust to SPICE's discrete jumps.
   - Risk: discards magnitude, so a big win counts the same as a marginal one. It cannot raise SPICE's own concordance.
   - Cost: low.
   - Precedent: GOPO (preprint). The pairwise/BRPO form is equivalent here (Q3).
6. **DAPO dynamic sampling (drop and resample zero-std groups).**
   - Effect: small. It recovers at most about 6% of compute and avoids updates where one of the two prompts carries zero signal.
   - Risk: low.
   - Cost: extra generation.
   - Precedent: DAPO (NeurIPS 2025).
7. **Raise effective signal per update rather than lowering β.** Use more prompts per update (e.g. 4–8 instead of 2) at fixed G.
   - Effect: lower-variance gradients for a low-variance teacher, consistent with Razin's flat-landscape argument.
   - Risk: more compute per update on a T4.
   - Precedent: indirect, Razin et al. (NeurIPS 2025).
8. **Not recommended as primary fixes:**
   - Re-tuning α or the 0.8/0.2 weights: GDPO shows weights are a weak lever.
   - Removing std scaling entirely: format collapse in GDPO.
   - Expecting noise robustness from the math-RLVR literature: different noise type, and the findings are contested.
