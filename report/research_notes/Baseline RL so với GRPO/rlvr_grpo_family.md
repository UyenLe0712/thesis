# RL baselines used by papers on online policy-gradient RL for LLMs (GRPO family, RLVR), 2024-2026

Checked 1/11/2026. All 49 arXiv PDFs below were downloaded and their text searched (RLOO's venue page was also read at ACL Anthology); passages and table rows were read as extracted text. I did not read each PDF cover to cover and did not view figures as images, so a "figure" baseline means it appears in the figure's legend, caption or surrounding text.

## Which algorithms are compared against most often (GRPO, PPO, REINFORCE, DAPO, Dr. GRPO, SAC, A2C, etc.)?

### Takeaway
Across 42 papers with checked RL baselines, GRPO is the baseline in 36 (86%), then DAPO 15 (36%), PPO 10 (24%) and Dr. GRPO 8 (19%). No paper uses SAC, A2C, A3C or TD3 as a compared method. PPO is much rarer than its role in the narrative suggests, and it was not plotted against GRPO even in the original GRPO paper.

### Paper-by-paper table

**How to read it**
- **Venue check.** [S] means the title was seen on the official proceedings or programme page. [H] means only the PDF header or arXiv comment states the venue, because the official list was not reached. [Pre] means no venue in the arXiv metadata or the lists checked, so it is labelled preprint. A [Pre] paper may have been accepted somewhere I did not check.
- **Official pages used.** [NeurIPS 2025 list](https://neurips.cc/virtual/2025/papers.html), [ICLR 2026 list](https://iclr.cc/virtual/2026/papers.html), [ICML 2026 list](https://icml.cc/virtual/2026/papers.html), [ICLR 2025 list](https://iclr.cc/virtual/2025/papers.html), [PMLR v235](https://proceedings.mlr.press/v235/), [PMLR v267](https://proceedings.mlr.press/v267/), [EMNLP 2025 Anthology](https://aclanthology.org/events/emnlp-2025/).
- **RL baselines column.** Only compared methods seen in tables, figure text or results text. Non-RL or offline comparators are in parentheses and are not tallied.
- **Ctrl column** (see the second question).
  - **Y**: the paper states the same model and training setup, or the numbers come from one uniform head-to-head run.
  - **Abl**: ablation or plug-in on the same pipeline.
  - **Mix**: some rows are reproduced or third-party models with different data.
  - **?**: not established from what I read.

| # | Paper (first author, arXiv year) | Venue | Proposed | RL baselines seen | Task / data | Ctrl |
|---|---|---|---|---|---|---|
| 1 | [ReMax: A Simple, Effective, and Efficient RL Method for Aligning LLMs](https://arxiv.org/abs/2310.10505) (Li, 2023) | ICML 2024 [S] | ReMax | PPO (compute cost, Table 2; performance only via third-party Llama-2-Chat), REINFORCE (Fig. 4) (DPO) | RLHF, reward model; HH, Mistral-7B | Mix |
| 2 | [Back to Basics: Revisiting REINFORCE-Style Optimization…](https://aclanthology.org/2024.acl-long.662/) (Ahmadian, 2024) | ACL 2024 Long [S] | RLOO | PPO, REINFORCE w/ baseline, Vanilla PG (DPO, RAFT) | RLHF; TL;DR, Anthropic-HH | Y |
| 3 | [VinePPO: Refining Credit Assignment in RL Training of LLMs](https://arxiv.org/abs/2410.01679) (Kazemnejad, 2024) | ICML 2025 [S] | VinePPO | PPO, GRPO, RLOO (RestEM, DPO+) | MATH, GSM8K; RhoMath, DeepSeekMath | Y |
| 4 | [DeepSeek-R1](https://arxiv.org/abs/2501.12948) (DeepSeek-AI, 2025) | Nature 645 (2025) per arXiv journal-ref [H] | R1 pipeline (GRPO) | PPO (Fig. 4) | MATH; DeepSeek-Coder-V2-Lite | Y |
| 5 | [REINFORCE++: Stabilizing Critic-Free Policy Optimization…](https://arxiv.org/abs/2501.03262) (Hu, 2025) | [Pre] | REINFORCE++ | GRPO, RLOO, ReMax (Table 1); PPO (results claim, row not inspected) | Chat-Arena-Hard, ZeroTIR, AIME | ? |
| 6 | [Process Reinforcement through Implicit Rewards](https://arxiv.org/abs/2502.01456) (Cui, 2025) | [Pre] | PRIME | RLOO, REINFORCE, GRPO, PPO, VinePPO | Math + LeetCode; Qwen2.5-Math-7B | Abl |
| 7 | [DAPO](https://arxiv.org/abs/2503.14476) (Yu, 2025) | [NeurIPS 2025](https://papers.nips.cc/paper_files/paper/2025/hash/a4277440d50f1f15d2cb4c14f7e0c0d2-Abstract-Conference.html) [S] | DAPO | Naive GRPO (Table 1, progressive) | AIME24; Qwen2.5-32B Base | Abl |
| 8 | [Understanding R1-Zero-Like Training](https://arxiv.org/abs/2503.20783) (Liu, 2025) | COLM 2025 [H] | Dr. GRPO | GRPO | MATH; Qwen2.5-Math-7B, Llama | Mix |
| 9 | [GRPO-LEAD](https://arxiv.org/abs/2504.09696) (Zhang, 2025) | EMNLP 2025 Main [S + arXiv comment] | GRPO-LEAD | GRPO | AIME24/25; R1-Distill 7B, 14B | Abl |
| 10 | [GPG](https://arxiv.org/abs/2504.02546) (Chu, 2025) | ICLR 2026 [S] | GPG | GRPO, Dr. GRPO (reproduced) | MATH; Qwen2.5-Math-7B | ? |
| 11 | [GVPO](https://arxiv.org/abs/2504.19599) (Zhang, 2025) | NeurIPS 2025 [S] | GVPO | GRPO, Dr. GRPO, ReMax, REINFORCE++ | MATH; Qwen2.5-Math-1.5B/7B | Y |
| 12 | [Learning to Reason under Off-Policy Guidance](https://arxiv.org/abs/2504.14945) (Yan, 2025) | NeurIPS 2025 [S] | LUFFY | Dr. GRPO (own on-policy replication); plus previous RLVR models (SFT, RL w/ SFT loss, SFT+RL) | Math; Qwen2.5-Math-7B | Mix |
| 13 | [CPGD](https://arxiv.org/abs/2505.12504) (Liu, 2025) | [Pre] | CPGD | GRPO, REINFORCE++, RLOO | MMK12; QwenVL2.5-7B | Y |
| 14 | [AAPO](https://arxiv.org/abs/2505.14264) (Xiong, 2025) | ACL 2026 Main, arXiv comment only [H] (ACL 2026 URL tried returned 404) | AAPO | GRPO, GPG, Oat-Zero (Dr. GRPO recipe); plus SimpleRL-Zero, OpenReasoner-Zero, PRIME models | Math, Llama and Qwen | Mix |
| 15 | [Pass@K Policy Optimization](https://arxiv.org/abs/2505.15201) (Walder, 2025) | NeurIPS 2025 [S] | PKPO | PPO + entropy (tuned sweep), [TZSM25] special case | MATH, coding; Llama, Gemma | Y |
| 16 | [On the Design of KL-Regularized PG Algorithms](https://arxiv.org/abs/2505.17508) (Zhang, 2025) | ICLR 2026 [S] | RPG / RPG-REINFORCE | GRPO, DAPO, REINFORCE++ | AIME24/25; Qwen3 | ? |
| 17 | [Revisiting GRPO: On-/Off-Policy](https://arxiv.org/abs/2505.22257) (Mroueh, 2025) | ICLR 2026 [S] | Off-policy GRPO | On-policy GRPO | AIME24 | Y |
| 18 | [Segment Policy Optimization](https://arxiv.org/abs/2505.23564) (Guo, 2025) | NeurIPS 2025 [S] | SPO | PPO, GRPO, RLOO, VinePPO (RestEM, DPO) | GSM8K, MATH500, AIME24 | ? |
| 19 | [Beyond the 80/20 Rule](https://arxiv.org/abs/2506.01939) (Wang, 2025) | NeurIPS 2025 [S] | Forking tokens | DAPO | Math, code; Qwen3 | Abl |
| 20 | [Critique-GRPO / Advancing LLM Reasoning with NL and Numerical Feedback](https://arxiv.org/abs/2506.03106) (Zhang, 2025) | ICML 2026 [S] (spotlight per comment) | Critique-GRPO | R1-GRPO, R1-Dr. GRPO (SFT, RAFT, CITL-FT) | Math and science; Qwen2.5/3 | Y |
| 21 | [MiniMax-M1](https://arxiv.org/abs/2506.13585) (MiniMax, 2025) | Tech report [Pre] | CISPO | GRPO (text claim), DAPO (2x speedup) | Qwen2.5-32B | Y (by own wording) |
| 22 | [ReDit](https://arxiv.org/abs/2506.18631) (Wei, 2025) | [Pre] | ReDit | GRPO, DAPO, Dr. GRPO, REINFORCE++ | GSM8K, MATH | Abl |
| 23 | [GSPO](https://arxiv.org/abs/2507.18071) (Zheng, 2025) | [Pre] | GSPO | GRPO (clip range tuned) | Qwen3 MoE | Y |
| 24 | [Geometric-Mean Policy Optimization](https://arxiv.org/abs/2507.20673) (Zhao, 2025) | [Pre] | GMPO | GRPO | Math, Geometry3K | ? |
| 25 | [GTPO and GRPO-S](https://arxiv.org/abs/2508.04349) (Tan, 2025) | ICML 2026 [S] | GTPO, GRPO-S | GRPO, DAPO, DAPO w/ Forking | AIME, MATH500 | ? |
| 26 | [Part I: Tricks or Traps?](https://arxiv.org/abs/2508.08221) (Liu, 2025) | [Pre] | LitePPO | GRPO, DAPO | Math | Y |
| 27 | [Sample More to Think Less (GFPO)](https://arxiv.org/abs/2508.09726) (Shrivastava, 2025) | ICLR 2026 [S] | GFPO | GRPO (Phi-4-reasoning-plus) (SFT) | AIME, GPQA | ? |
| 28 | [FlowRL](https://arxiv.org/abs/2509.15207) (Zhu, 2025) | ICLR 2026 [S] | FlowRL | REINFORCE++, PPO, GRPO | Math, code; 7B, 32B | Y |
| 29 | [MAPO](https://arxiv.org/abs/2509.18849) (Huang, 2025) | [Pre] | MAPO | GRPO, DAPO ("Vanilla" = base model) | Geo3K, emotion; Qwen2.5-VL-7B | Y |
| 30 | [VCRL](https://arxiv.org/abs/2509.19803) (Jiang, 2025) | [Pre] | VCRL | GRPO, DAPO, GSPO | Math; Qwen3 | ? |
| 31 | [Risk-Sensitive RL (RS-GRPO)](https://arxiv.org/abs/2509.24261) (Jiang, 2025) | [Pre] | RS-GRPO | GRPO | Math; six LLMs | ? |
| 32 | [GRPO-λ: Credit Assignment](https://arxiv.org/abs/2510.00194) (Parthasarathi, 2025) | [Pre] | GRPO-λ | GRPO | Math; 1.5B-7B | ? |
| 33 | [LSPO](https://arxiv.org/abs/2510.01459) (Chen, 2025) | [Pre] | LSPO | GRPO, DAPO, GSPO (each as base) | Math; Qwen, Llama | Abl |
| 34 | [Reinforce-Ada](https://arxiv.org/abs/2510.04996) (Xiong, 2025) | [Pre] | Reinforce-Ada | GRPO n=4/8/16 (DAPO conceptual only) | Math | Y |
| 35 | [λ-GRPO: Unifying the GRPO Frameworks](https://arxiv.org/abs/2510.06870) (Wang, 2025) | Header says under review at ICLR 2026, not found in list [Pre] | λ-GRPO | GRPO, DAPO-style token-mean (Dr. GRPO deliberately excluded) | Math; Qwen2.5 1.5B-7B | Y |
| 36 | [DARO](https://arxiv.org/abs/2510.09001) (Zhou, 2025) | [Pre] | DARO | GRPO, DAPO, LIPO (LitePPO), Dr. GRPO | Math; Qwen2.5, Llama3.1 | ? |
| 37 | [The Art of Scaling RL Compute](https://arxiv.org/abs/2510.13786) (Khatri, 2025) | ICLR 2026 [S] | ScaleRL | GRPO, DAPO, GSPO, CISPO; recipes incl. Magistral, MiniMax | Math, code | Y |
| 38 | [Beyond the Sampled Token (CaSP)](https://arxiv.org/abs/2510.14807) (Peng, 2025) | Tech report [Pre] | CaSP | GRPO, W-REINFORCE, PSR, NSR, KL-Cov, forking tokens, P@k T., Entropy-Adv, GRPO + entropy | Math, code | ? |
| 39 | [Comparative Analysis of PPO, GRPO, DAPO](https://arxiv.org/abs/2512.07611) (Lian, 2025) | [Pre] | None (comparison) | PPO, GRPO, DAPO | Countdown (train); GSM8K, MATH, BBH, MMLU-Pro | Y |
| 40 | [Harder Is Better (MathForge)](https://arxiv.org/abs/2601.20614) (Dai, 2026) | ICLR 2026 [S] | DGPO + MQR | GRPO, Dr. GRPO, GPG, DAPO, GSPO, GRPO-AD | MATH; Qwen2.5-Math | Y |
| 41 | [Soft Sequence Policy Optimization](https://arxiv.org/abs/2602.19327) (Glazyrina, 2026) | [Pre] | SSPO | GRPO, SAPO, GMPO, GSPO | GSM8K, MATH500, AIME25 | ? |
| 42 | [Experience Augmented Policy Optimization](https://arxiv.org/abs/2606.30420) (Lu, 2026) | ICML 2026 [S] | EAPO | GRPO, DAPO (OPD, MOPD) | AIME, AMC; Qwen | ? |

**In scope but excluded from the tally** (reason given):
- [DeepSeekMath / GRPO](https://arxiv.org/abs/2402.03300) (Shao, 2024, preprint): compares GRPO+OS and GRPO+PS with RFT and Online RFT. PPO appears only in the derivation and the unified table, plus a third-party leaderboard entry (Math-Shepherd), with no PPO curve found.
- [TOPR](https://arxiv.org/abs/2503.14286) (Le Roux, 2025, NeurIPS 2025 [S]): compares DPO, PPO, naive REINFORCE, but states it focuses on the "single-iteration, fully offline regime".
- [TIS-DPO](https://arxiv.org/abs/2410.04350) (Liu, 2024, ICLR 2025 [S]): offline preference learning, compared with DPO, PPO, IPO, TDPO, KTO.
- [Group-Standard-Deviation Identity](https://arxiv.org/abs/2607.00152) (Bay, 2026, preprint): analytic treatment of GRPO, Dr. GRPO, DAPO with a controlled Bernoulli-logit run, not an LLM benchmark.
- [Kimi k1.5](https://arxiv.org/abs/2501.12599) and [Magistral](https://arxiv.org/abs/2506.10910) (tech reports): design reports, no RL baseline head-to-head found.
- [OP-GRPO](https://arxiv.org/abs/2604.04142) (preprint): compares with Flow-GRPO, but on flow-matching image and video generation, not LLMs.
- [Flow-GRPO](https://neurips.cc/virtual/2025/papers.html) (NeurIPS 2025 list): "baselines not checked". The arXiv ID I tried was a wrong paper, so it was not opened. It is also an image model method, not an LLM one.

### Tally (42 papers; a paper counts once per baseline; self-comparison to a tuned variant of the proposed method is not counted)

| RL baseline | All 42 | % | Subset of 23 with a venue (S or H) |
|---|---:|---:|---:|
| GRPO | 36 | 86% | 17 |
| DAPO | 15 | 36% | 6 |
| PPO | 10 | 24% | 7 |
| Dr. GRPO (including Oat-Zero recipe in AAPO) | 8 | 19% | 6 |
| RLOO | 5 | 12% | 2 |
| REINFORCE++ | 5 | 12% | 3 |
| GSPO | 5 | 12% | 2 |
| REINFORCE / Vanilla PG / W-REINFORCE | 4 | 10% | 2 |
| VinePPO | 2 | 5% | 1 |
| ReMax | 2 | 5% | 1 |
| GPG | 2 | 5% | 2 |
| LitePPO, CISPO, GMPO, SAPO | 1 each | 2% | 0, 1, 0, 0 |
| SAC, A2C, A3C, TD3, TRPO | 0 | 0% | 0 |

The six counted papers without GRPO as a baseline are ReMax, RLOO, R1, LUFFY, Pass@K and Beyond 80/20. Of those, ReMax and RLOO predate GRPO's spread, R1 is GRPO's own vs-PPO test, and the last three use another GRPO-derived method or PPO + entropy as the anchor.

### Cited Findings
- verl's baseline page lists PPO, PRIME, GRPO, ReMax, SPPO, RLOO, SPIN, GPG and DAPO, among others — [verl docs](https://verl.readthedocs.io/en/latest/algo/baseline.html).
- TRL's taxonomy lists `GRPOTrainer` and `RLOOTrainer` as stable online methods. A2PO, AsyncGRPO, GMPO and OnlineDPO are experimental online methods. No PPO trainer appears in this taxonomy — [TRL docs](https://huggingface.co/docs/trl/en/index).
- Full-text scan for SAC, A2C, A3C, TD3 and "Soft Actor" across all 49 PDFs, excluding reference lists where detectable: the only hit is LUFFY naming "TRPO, A2C/A3C, PPO" as examples of on-policy methods, not as compared methods — [LUFFY](https://arxiv.org/abs/2504.14945).
- The original GRPO paper's method-comparison figure shows RFT, Online RFT, GRPO+OS and GRPO+PS. PPO is described and tabulated, not plotted — [DeepSeekMath](https://arxiv.org/abs/2402.03300). The direct PPO vs GRPO figure arrives in R1 — [DeepSeek-R1](https://arxiv.org/abs/2501.12948).

### Inferences
- GRPO is now the default control, DAPO the "strong" second control. A new variant without a GRPO row would be unusual.
- A paper comparing GRPO, a PPO with critic, and a critic-free REINFORCE-style method together is a minority design: only VinePPO, PRIME, FlowRL, SPO, REINFORCE++ and the Lian comparison study include both PPO and GRPO in the tally besides R1's pair.
- Off-policy actor-critic methods (SAC) have no presence as baselines here. Omitting them would not look unusual to a reviewer familiar with this literature.

### Gaps
- Selection bias: the set comes from my candidate list plus searches, and is not an exhaustive review. The percentages describe this sample only. Seed-GRPO, OPO, BNPO, EMPO, SAPO, Trust Region and others seen cited were not opened.
- Row 5 (PPO in REINFORCE++) and row 21 (GRPO in CISPO) are text claims; I did not locate the numeric row or plotted values.

## Do these papers report controlled comparisons where only the algorithm changes (same model, same reward)?

### Takeaway
Many state same model, data and hyperparameters, but changing "only the algorithm" is rarely literal, because reward signal, sampling budget, clip tuning or added components often move too. The rarest design is what one would want most: several seeds, confidence intervals, and multiple algorithms under the same recipe.

### Cited Findings
Stated controls:
- VinePPO: "All methods use the same SFT checkpoint", and all methods consume the same number of episodes — [VinePPO](https://arxiv.org/abs/2410.01679).
- CPGD: all RL algorithms use QwenVL2.5-7B "under the same hyperparameters" — [CPGD](https://arxiv.org/abs/2505.12504).
- FlowRL: baselines "follow the official veRL recipes" with the same learning rate, batch size and training steps — [FlowRL](https://arxiv.org/abs/2509.15207).
- λ-GRPO: "identical datasets, prompt templates, and model architectures". Dr. GRPO is left out because the paper compares token-aggregation rules — [λ-GRPO](https://arxiv.org/abs/2510.06870).
- MathForge: "For a fair algorithm-level comparison, we disable the resampling components in GPG and DAPO" — [Harder Is Better](https://arxiv.org/abs/2601.20614).
- Lian: applies PPO, GRPO and DAPO "to the same model and training dataset" in order to isolate each strategy's contribution — [Lian 2025](https://arxiv.org/abs/2512.07611).
- Reinforce-Ada: standardizes the update group size at n=4, and also reports GRPO at n=8 and 16 — [Reinforce-Ada](https://arxiv.org/abs/2510.04996).
- GSPO: GRPO's clip ranges are "carefully tuned to ensure a fair comparison", but GRPO needs Routing Replay and GSPO does not, so the training setups differ for MoE models — [GSPO](https://arxiv.org/abs/2507.18071).
- Pass@K: gives its entropy-regularized PPO baseline "an arguably unfair advantage" by sweeping coefficients per (model, benchmark) pair — [Pass@K](https://arxiv.org/abs/2505.15201).
- GVPO: ten seeds for GRPO vs GVPO on 1.5B, reported as mean ± std — [GVPO](https://arxiv.org/abs/2504.19599). Critique-GRPO: three runs, states p<0.01 — [Critique-GRPO](https://arxiv.org/abs/2506.03106).

Mixed or weaker designs:
- AAPO Table 1 mixes reproduced models with very different training sizes (for example 8,523 vs 57K vs 230K+150K) — [AAPO](https://arxiv.org/abs/2505.14264).
- Dr. GRPO's Fig. 2 places Oat-Zero next to SimpleRL-Zero, Prime-Zero and OpenReasoner-Zero (different recipes), though its Fig. 5 is GRPO vs Dr. GRPO — [Dr. GRPO](https://arxiv.org/abs/2503.20783).
- LUFFY states "all prior methods" differ "in dataset composition… and optimization strategies", while its own Dr. GRPO replication uses "the same reward and data" — [LUFFY](https://arxiv.org/abs/2504.14945).
- DAPO's Table 1 is cumulative, not one-factor-at-a-time: Naive GRPO 30, + Overlong Filtering 36, + Clip-Higher 38, + Soft Overlong Punishment 41 — [DAPO](https://arxiv.org/abs/2503.14476).
- MiniMax-M1 says "controlled study" for its 2x-vs-DAPO claim; the setup details were not inspected — [MiniMax-M1](https://arxiv.org/abs/2506.13585).
- Tricks or Traps says "inconsistent experimental settings, variations in training data, and differences in model initialization have led to conflicting conclusions" in this field — [Tricks or Traps](https://arxiv.org/abs/2508.08221).
- Art of Scaling compares recipes by fitting sigmoid curves of reward against compute, rather than by one final score — [Art of Scaling](https://arxiv.org/abs/2510.13786).

### Inferences
- "Same model, same reward, only the algorithm differs" is the best-supported reading for rows 3, 13, 28, 35, 39 and 40, and for R1's PPO/GRPO pair. Most rows are "new method beats GRPO under our recipe".
- Gains in the controlled MathForge table are small among established methods (see next question), which suggests that large gains claimed elsewhere may partly reflect recipe differences. This is my inference, not a tested result.
- A thesis study changing only the algorithm on one model and reward, reporting paired CI per seed, would be more controlled than most of these papers.

### Gaps
- I did not audit every paper's appendix for seeds and hyperparameter parity. "?" in the table means not established, not that controls are absent.
- Nearly all use binary verifiers on math or code, or reward-model RLHF. I found no comparison with a continuous metric reward (such as SPICE or CIDEr) in this set.

## What empirical conclusions do they reach about baseline choice, std normalization, value models/critics?

### Takeaway
Differences among established critic-free methods are small in the best-controlled table (within about 0.3 points of GRPO), and evidence on dividing by std is mixed, not a clear win for removal. PPO with a critic is not uniformly worse: it beats GRPO in some head-to-head tables.

### Cited Findings
Baseline choice and head-to-heads:
- MathForge Table 1 average over six benchmarks on Qwen2.5-Math-7B: GRPO 37.61, Dr. GRPO 37.40 (−0.21), GPG 37.93 (+0.32), DAPO 37.94 (+0.33), GSPO 37.71 (+0.10) — [Harder Is Better](https://arxiv.org/abs/2601.20614).
- Lian Table 3 (GSM8K, MATH, BBH, MMLU-Pro): PPO 50.3/25.1/36.8/27.1, GRPO 50.8/24.7/36.9/28.2, DAPO without dynamic sampling 53.3/25.4/36.9/30.0 — [Lian 2025](https://arxiv.org/abs/2512.07611).
- GVPO table (surrounding text says Qwen2.5-Math-7B; the row's model was not separately confirmed): on MATH500, GRPO 80.0, Dr. GRPO 81.2, ReMax 82.0, REINFORCE++ 80.4, GVPO 83.8 — [GVPO](https://arxiv.org/abs/2504.19599). Note the older ReMax is above GRPO here.
- CPGD: "GRPO outperforms RLOO and REINFORCE++ on most benchmarks" among baselines — [CPGD](https://arxiv.org/abs/2505.12504).
- VCRL Table 1 (Qwen3-4B): GRPO avg 41.76, DAPO 40.60, GSPO 40.08, so GRPO tops the two later variants on that model; the text names GSPO as the strongest baseline in another comparison I did not map to a row — [VCRL](https://arxiv.org/abs/2509.19803).
- Dr. GRPO "lags behind the baseline on all models" in DARO's table — [DARO](https://arxiv.org/abs/2510.09001). LSPO's "Acc-only" rows put GRPO/DAPO/GSPO within about 1 point on avg@32 — [LSPO](https://arxiv.org/abs/2510.01459).
- REINFORCE++ Table 1 on Chat-Arena-Hard: REINFORCE++ (k=1) 46.7, GRPO (k=4) 46.8, RLOO (k=4) 44.6, ReMax 45.1 — [REINFORCE++](https://arxiv.org/abs/2501.03262).
- RLOO Table 1: RLOO (k=2) win-rates 72.1/37.7/58.4 vs REINFORCE w/ baseline 70.7/37.9/55.3, Vanilla PG 70.4/36.4/52.3, PPO 67.6/29.2/32.0, DPO 66.6/39.0/61.9 — [Back to Basics](https://aclanthology.org/2024.acl-long.662/).
- Lian: dynamic sampling "does not guarantee improvements in task-level performance" and adds compute — [Lian 2025](https://arxiv.org/abs/2512.07611).
- ScaleRL finds common interventions (loss aggregation, data curriculum, length penalty, advantage normalization) "mainly adjust compute efficiency… while not changing the performance ceiling considerably" — [Art of Scaling](https://arxiv.org/abs/2510.13786). In the same paper, GSPO and CISPO substantially beat DAPO on asymptotic pass rate — [Art of Scaling](https://arxiv.org/abs/2510.13786).

Std normalization:
- Removal, with bias argument: Dr. GRPO removes length and std normalization as biased — [Dr. GRPO](https://arxiv.org/abs/2503.20783). GVPO omits it, citing that scaling conflates prompt difficulty with reward — [GVPO](https://arxiv.org/abs/2504.19599). RS-GRPO omits it, citing Dr. GRPO — [RS-GRPO](https://arxiv.org/abs/2509.24261).
- Formal view: per-prompt GRPO updates scale by group reward std, and the std operation, not the baseline, is the objective-changing distinction; Dr. GRPO equals RLOO and baselined REINFORCE up to a learning-rate constant — [Identity paper, preprint](https://arxiv.org/abs/2607.00152).
- Evidence against simple removal: GPG reports the GRPO-style std setting beats Fnorm=1 by 1.4 average points at α=1, although its best variant (48.3) uses Fnorm=1 plus α and a threshold — [GPG](https://arxiv.org/abs/2504.02546). The MathForge and DARO results above also show Dr. GRPO not beating GRPO.
- No difference: prompt-level, batch-level and no normalization "all three… yield similar performance" — [Art of Scaling](https://arxiv.org/abs/2510.13786).
- Global or batch std preference: prompt-level estimator is argued to be biased, and global normalization to generalize better — [REINFORCE++](https://arxiv.org/abs/2501.03262). Group-level mean with batch-level std is "further robust", and group-level alone is robust across reward settings — [Tricks or Traps](https://arxiv.org/abs/2508.08221). Magistral uses group mean, then normalizes in the minibatch — [Magistral](https://arxiv.org/abs/2506.10910).
- Alternative scales: MathForge's DGPO uses mean absolute deviation rather than std (DGPO 39.79, +2.18) — [Harder Is Better](https://arxiv.org/abs/2601.20614). CPGD shows STD weights make its advantage match GRPO's, and STD-weight CPGD scores about the same overall as the clip-filter variant (1.11 vs 1.10) — [CPGD](https://arxiv.org/abs/2505.12504).

Value models:
- VinePPO's Figure 4 text reads, for MATH on 7B in the order Init, SFT, RestEM, RLOO, GRPO, DPO+, PPO, VinePPO: 32.8, 34.9, 36.8, 36.4, 37.6, 42.8, 46.0. PPO is above GRPO and RLOO, and Monte Carlo VinePPO is highest — [VinePPO](https://arxiv.org/abs/2410.01679). The mapping from extracted numbers to labels assumes the same order; verify against the figure before quoting.
- VinePPO finds value networks "often produce poor estimate" of expected returns in reasoning tasks — [VinePPO](https://arxiv.org/abs/2410.01679).
- PRIME: "Comparing PPO and REINFORCE, we find that an additional value model does not benefit policy performance" — [PRIME](https://arxiv.org/abs/2502.01456).
- R1: with λ=0.95 PPO performs "considerably worse than GRPO", while λ=1.0 brings it near GRPO — [DeepSeek-R1](https://arxiv.org/abs/2501.12948).
- FlowRL reports its math improvement as 10.0% over GRPO and 5.1% over PPO, which implies PPO ahead of GRPO in that setup — [FlowRL](https://arxiv.org/abs/2509.15207).
- SPO claims 6-12 points over PPO and GRPO on GSM8K with its own method — [SPO](https://arxiv.org/abs/2505.23564).

### Inferences
- The evidence does not support saying GRPO is simply dominated by a later variant. Choice of baseline should be justified by the task, not by assuming the newest is best.
- Whether to divide by std is an open empirical question. Results seem to depend on reward density and difficulty, as the identity paper's difficulty-weight account would predict. Any reward that is not binary falls outside that paper's analysis, as it states.
- Critic-free adoption rests more on cost and tuning burden than on a demonstrated accuracy gain, since PPO is competitive once tuned in several direct tests.

### Gaps
- Many numbers are one seed or do not report intervals, so differences under about 1 point are not interpretable as a ranking.
- These tasks are mostly math with binary verifiers. Transfer to instruction generation with SPICE-style rewards is untested in this set.

## Is the critic of PPO dropped, and what reason do authors give?

### Takeaway
Yes, in almost every method here: the common reason is memory and compute cost of a policy-sized model, with secondary reasons being tuning sensitivity and poor value estimates when reward arrives only at the end. A minority keep credit assignment finer than a group baseline by other means, and few retain a learned critic.

### Cited Findings
Reasons given:
- **Memory and compute.** "the value function employed in PPO is typically another model of comparable size as the policy model, it brings a substantial memory and computational burden" — [DeepSeekMath](https://arxiv.org/abs/2402.03300). R1 repeats this — [DeepSeek-R1](https://arxiv.org/abs/2501.12948). The same reason appears in GSPO, VCRL and AAPO — [GSPO](https://arxiv.org/abs/2507.18071); [VCRL](https://arxiv.org/abs/2509.19803); [AAPO](https://arxiv.org/abs/2505.14264).
- **Terminal reward.** "usually only the last token is assigned a reward score by the reward model, which may complicate the training of a value function" — [DeepSeekMath](https://arxiv.org/abs/2402.03300).
- **Four models loaded.** PPO typically loads generator, reference, critic and reward model, and variance concerns from classic RL may not transfer — [Back to Basics](https://aclanthology.org/2024.acl-long.662/). ReMax removes "all the components related to the value model" — [ReMax](https://arxiv.org/abs/2310.10505).
- **Tuning burden.** GAE λ sensitivity adds hyperparameter search cost — [DeepSeek-R1](https://arxiv.org/abs/2501.12948).
- **Inaccurate estimates.** Value networks give poor estimates in reasoning tasks — [VinePPO](https://arxiv.org/abs/2410.01679). Accurately training PPO's critic is hard — [SPO](https://arxiv.org/abs/2505.23564).
- **Unsuitability hypothesis.** Kimi excludes the value network, saying it improves efficiency and hypothesizing that conventional value-based credit assignment may not suit this setting — [Kimi k1.5](https://arxiv.org/abs/2501.12599).
- **Variance.** Lian's comparison table lists "eliminating the high-variance critic" as the simplification — [Lian 2025](https://arxiv.org/abs/2512.07611).
- **No benefit measured.** Linear-head value model baseline did not help in REINFORCE tests — [PRIME](https://arxiv.org/abs/2502.01456).

Formal relation and exceptions:
- REINFORCE++ is "formally equivalent to a PPO agent" with critic removed, GAE λ=1, γ=1 and global normalization in place of a learned value function — [REINFORCE++](https://arxiv.org/abs/2501.03262).
- Tricks or Traps builds on vanilla PPO loss with REINFORCE-computed advantages and no critic — [Tricks or Traps](https://arxiv.org/abs/2508.08221).
- Finer credit without a learned critic: VinePPO (Monte Carlo from intermediate states) — [VinePPO](https://arxiv.org/abs/2410.01679); SPO (segment-level Monte Carlo) — [SPO](https://arxiv.org/abs/2505.23564); GRPO-λ ("critic-free approximation of the temporal-difference error") — [GRPO-λ](https://arxiv.org/abs/2510.00194).
- Note: Reinforce-Ada mentions a "lightweight value network" as an estimator for pass rate only, and flags its overhead — [Reinforce-Ada](https://arxiv.org/abs/2510.04996).
- ICLR 2026 GPG removes critic and reference models and the KL constraint — [GPG](https://arxiv.org/abs/2504.02546). R1-Zero-style Dr. GRPO uses β=0 so also drops the reference model — [Dr. GRPO](https://arxiv.org/abs/2503.20783).

### Inferences
- The main justification is cost, stated without a controlled accuracy test in most papers that repeat it. The tests that exist (R1 with λ, VinePPO, Lian, FlowRL) do not show PPO is inaccurate once tuned, though VinePPO shows the value estimates themselves are poor.
- Keeping PPO as a comparison arm in a study is defensible and uncommon (24% of this sample), and needs GAE λ reported, given R1's sensitivity result.

### Gaps
- I found no paper in this set testing a small critic (for example a linear head on the policy backbone with shared weights) against GRPO across RLVR tasks, apart from PRIME's linear-head test in REINFORCE. Absence here is limited to the sample read.
- I did not determine for each paper whether the critic argument is original or copied from GRPO.
