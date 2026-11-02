# RL algorithms and RL baselines in papers on vision-language and GUI models (2023-2026)

Checked 1/11/2026. Method: full-text PDF extraction plus keyword scan of 47 arXiv papers, then reading of the comparison passages and tables that the scan surfaced.

Reading status used below:
- **Baseline status "none found (scan)"** means the full text was scanned for PPO, DAPO, DPO, REINFORCE, GSPO and for phrases such as "vanilla/standard/naive GRPO", "GRPO-only", "w/o GRPO", "over GRPO". Other algorithms appeared only in definitions or related work. Every table was not read line by line.
- **"not checked"** means the row is excluded from the baseline tally.
- PDF table extraction is sometimes garbled (bold values repeat). Numbers are quoted only where the row was legible.

Venue evidence codes:
- **P** = publisher, proceedings or conference page, or Crossref record for the proceedings DOI.
- **A** = author statement only (arXiv comment or journal-ref, PDF header).
- **O** = OpenAlex record only, publisher page not opened.
- **S** = secondary listing only, treat as unverified.
- **Preprint** = no venue found; arXiv only.

## Which algorithm do GUI/VLM RL papers use by default, and how many compare it to any other RL algorithm rather than only SFT or other models?

### Takeaway
GRPO or a direct GRPO variant is the default: 26 of 33 GUI papers that use an RL or preference algorithm, and all 11 VLM papers in the sample. Only 2 of the 32 GUI papers with a checked baseline status compare against a different named RL algorithm, and only one of those gives a number. Another 7 compare only against vanilla GRPO or their own variant, and the other 23 show no RL alternative.

### Cited Findings

#### Table A: VLM papers (not GUI). All 11 use a GRPO base.

| # | Paper, first author, year | Venue (evidence) | RL algorithm | RL baselines with numbers | Reward | Data; AC/AW flag | Link |
|---|---|---|---|---|---|---|---|
| 1 | Visual-RFT, Liu 2025 | ICCV 2025, pp. 2034-2044 (P) | GRPO | None found (scan) | Task-specific verifiable, e.g. IoU | Fine-grained classification, few-shot and open-vocabulary detection, grounding; no AC/AW | [CVF](https://openaccess.thecvf.com/content/ICCV2025/html/Liu_Visual-RFT_Visual_Reinforcement_Fine-Tuning_ICCV_2025_paper.html) |
| 2 | VLM-R1, Shen 2025 | Preprint | GRPO, LoRA option | None found (scan) | Rule-based on deterministic ground truth | Open-source grounding data; no AC/AW | [arXiv](https://arxiv.org/abs/2504.07615) |
| 3 | Vision-R1, Huang 2025 | ICLR 2026 (A) | GRPO + PTST | None found (scan) | Hard-formatting result | 10K multimodal math; no AC/AW | [arXiv](https://arxiv.org/abs/2503.06749) |
| 4 | Vision-R1, Zhan 2025. A different paper with the same name | CVPR 2026 Findings track (P, Crossref [DOI](https://doi.org/10.1109/cvprf71909.2026.00558)) | GRPO-based | None found (scan) | Criterion-driven vision feedback, progressive rule refinement | Instruction data; no AC/AW | [arXiv](https://arxiv.org/abs/2503.18013) |
| 5 | R1-Onevision, Yang 2025 | ICCV 2025 (P) | GRPO after SFT | None found (scan) | Two rule rewards | Own cross-modal dataset; no AC/AW | [CVF](https://openaccess.thecvf.com/content/ICCV2025/html/Yang_R1-Onevision_Advancing_Generalized_Multimodal_Reasoning_through_Cross-Modal_Formalization_ICCV_2025_paper.html) |
| 6 | OpenVLThinker, Deng 2025 | NeurIPS 2025 (P) | GRPO in SFT-RL cycles | None found; DAPO only cited as concurrent work | Outcome verification | MathVista and others; no AC/AW | [NeurIPS](https://neurips.cc/virtual/2025/poster/116720) |
| 7 | ReVisual-R1, Chen 2025 | ICLR 2026 (P) | GRPO + PAD, staged | **DAPO 46.1, GRPO-Baseline 45.1, PAD 47.7** (average, Table 4) | Binary correctness | Math and logic benchmarks; no AC/AW | [ICLR](https://proceedings.iclr.cc/paper_files/paper/2026/hash/3792ac815260f4ba55ed71c7906cce36-Abstract-Conference.html) |
| 8 | PAPO, Wang 2025 | ICLR 2026 (A) | PAPO, drop-in for GRPO or DAPO | **GRPO 47.92 vs PAPO-G 49.92** (overall). States 4.4-17.5% gain over GRPO and DAPO; DAPO row not extracted | Equivalence verifier | 8 multimodal benchmarks; no AC/AW | [arXiv](https://arxiv.org/abs/2507.06448) |
| 9 | TGRL, Lu 2026 | Preprint | GRPO and DAPO + expert trajectories | **GRPO 57.16, DAPO 56.92, TGRL-GRPO 58.46, TGRL-DAPO 59.51** (average) | Equivalence verifier | Math and hallucination benchmarks; no AC/AW | [arXiv](https://arxiv.org/abs/2603.26126) |
| 10 | OThink-MR1, Liu 2025 | Preprint | GRPO-D (dynamic KL) | **More than 13.59% relative gain over GRPO**, more than 5.72% over SFT | Verifiable | Two adapted datasets; no AC/AW | [arXiv](https://arxiv.org/abs/2503.16081) |
| 11 | Table-R1, Kang 2025 | EMNLP 2025 (A, journal-ref; main or Findings not checked) | PA-GRPO, HC-GRPO | **Qwen2-VL-7B: +16.38% and +8.79% over GRPO** (held-in, held-out) | Continuous TEDS and others | Table data; no AC/AW | [arXiv](https://arxiv.org/abs/2509.16889) |

#### Table B: GUI, mobile and computer-use papers

"AC" = AndroidControl, "AW" = AndroidWorld.

| # | Paper, first author, year | Venue (evidence) | RL algorithm | RL baselines with numbers | Reward | Data; AC/AW flag | Link |
|---|---|---|---|---|---|---|---|
| 12 | UI-R1, Lu 2025 | AAAI 2026 (P, Crossref [DOI](https://doi.org/10.1609/aaai.v40i21.38816)) | GRPO | None found (scan) | Action type + coordinate + format | 136 mobile tasks; AC used at evaluation | [arXiv](https://arxiv.org/abs/2503.21620) |
| 13 | GUI-R1, Luo 2025 | Preprint | GRPO | None found (scan) | Unified action-space rule | GUI-R1-3K; AC test split only | [arXiv](https://arxiv.org/abs/2504.10458) |
| 14 | InfiGUI-R1, Liu 2025 | Preprint ("work in progress") | **RLOO** | None found (scan) | Hit + IoU per GUI-G1 Table 3 | **AC in the RL training mix** (10k + 2k reflection trajectories) | [arXiv](https://arxiv.org/abs/2504.14239) |
| 15 | InfiGUI-G1, Liu 2025 | AAAI 2026, oral (O, [DOI](https://doi.org/10.1609/aaai.v40i38.40500); A) | AEPO; base objective named only as "PPO, GRPO or RLOO" | **Naive RLVR baseline, up to 9.0% relative gain** | Adaptive exploration reward | 44k instances; no AC/AW | [arXiv](https://arxiv.org/abs/2508.05731) |
| 16 | GUI-G1, Zhou 2025 | NeurIPS 2025 (P) | GRPO, modified objective | **Standard GRPO 82.3; |oi| to Max_Tokens 83.2; difficulty weighting 83.3** (ScreenSpot average) | Hit + IoU + Box | 17K grounding samples; AC discussed, not used | [NeurIPS](https://papers.neurips.cc/paper_files/paper/2025/hash/89dcbea9f19960edd7765068adb13b1d-Abstract-Conference.html) |
| 17 | GUI-G², Tang 2025 | AAAI 2026, pp. 33214-33222 (P) | GRPO | None found (scan); compares rewards | Gaussian point + coverage | About 100K grounding instances; no AC/AW | [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/40606) |
| 18 | SE-GUI, Yuan 2025 | NeurIPS 2025 (P, Crossref [DOI](https://doi.org/10.52202/085713-4251)) | GRPO, self-evolving | None found (scan) | Dense point | Filtered grounding data; AC evaluated zero-shot | [arXiv](https://arxiv.org/abs/2505.12370) |
| 19 | UI-Venus, Gu 2025 | Preprint (tech report) | GRPO | None found (scan) | Designed grounding and navigation rewards | About 350k self-built samples; AC and AW at evaluation; AC in training not confirmed | [arXiv](https://arxiv.org/abs/2508.10833) |
| 20 | UI-Venus-1.5, Venus Team 2026 | Preprint (tech report) | GRPO, offline then online, KL + entropy terms | None found (scan) | Trajectory verification | AW at evaluation | [arXiv](https://arxiv.org/abs/2602.09082) |
| 21 | UI-TARS, Qin 2025 | Preprint | **DPO** after SFT | None found; DPO contrasted with SFT | Preference pairs from corrected and erroneous steps | **AC in pretraining**, not shown in DPO pairs; AW at evaluation | [arXiv](https://arxiv.org/abs/2501.12326) |
| 22 | UI-TARS-2, Wang 2025 | Preprint (tech report) | **PPO**, value pretraining, clip-higher from DAPO | **PPO vs GRPO: Figure 12 training-reward curves only, no tabulated number** | Task outcome, multi-turn | Online; AW 73.3 at evaluation | [arXiv](https://arxiv.org/abs/2509.02544) |
| 23 | AgentCPM-GUI, Zhang 2025 | EMNLP 2025 System Demonstrations (P, Crossref [DOI](https://doi.org/10.18653/v1/2025.emnlp-demos.12)) | GRPO | None found (scan) | -1 format failure, 0 wrong, 1 correct; point in box | AC in warm-up SFT and evaluation | [arXiv](https://arxiv.org/abs/2506.01391) |
| 24 | MobileRL, Xu 2025 | ICLR 2026 (P) | AdaGRPO | **MobileRL 71.1, w/o AdaGRPO 56.8, w/o AdaPR 63.6, w/o FCF 64.8, w/o SPA 69.1** (AW). "w/o AdaGRPO" was not seen defined as vanilla GRPO | Trajectory {0,1} plus VLM reward models, shortest-path adjustment | AC in SFT only, stated "not included during the RL stage"; AW and AndroidLab in RL | [ICLR](https://iclr.cc/virtual/2026/poster/10010890) |
| 25 | ARPO, Lu 2025 | Preprint (no venue found) | GRPO + replay | **OSWorld: UI-Tars-7B-1.5 23.5, + GRPO 26.0, + ARPO 29.9; UI-Tars-7B-DPO 15.6, + GRPO 18.3, + ARPO 20.4** | Environment sparse reward | OSWorld; no AC/AW | [arXiv](https://arxiv.org/abs/2505.16282) |
| 26 | ZeroGUI, Yang 2025 | Preprint | GRPO, multi-step, k2-KL | k2-KL vs original k3-KL (Table 4, values not read) | VLM-judged success | OSWorld daily domain; no AC | [arXiv](https://arxiv.org/abs/2505.23762) |
| 27 | VEM, Zheng 2025 | TMLR 2026 only per a secondary listing whose key names a different author ([S](https://mlanthology.org/tmlr/2026/chen2026tmlr-vem/)); treat as preprint | PPO on a pretrained value model | **DigiRL offline 80.0/21.0, online 83.3/23.0 vs VEM 82.6/28.0** (AITW General, step/task SR). PPO loss stability shown by figure only | Value model estimate | AITW; no AC/AW | [arXiv](https://arxiv.org/abs/2502.18906) |
| 28 | DigiRL, Bai 2024 | NeurIPS 2024 (O) | AWR with value functions | Not checked | Device-control task success | AITW; no AC | [arXiv](https://arxiv.org/abs/2406.11896) |
| 29 | DART-GUI, Li 2025 | Preprint | Step-wise GRPO | None found (scan); ablation of data curation and decoupling | Task reward | OSWorld; no AC/AW | [arXiv](https://arxiv.org/abs/2509.23866) |
| 30 | Mobile-R1, Gu 2025 | ACL 2026 long (P, Crossref [DOI](https://doi.org/10.18653/v1/2026.acl-long.1422)) | On-policy then multi-turn GRPO | None found (scan) | Verifiable action feedback, task level | Chinese dataset, 24,521 annotations; AC at evaluation | [arXiv](https://arxiv.org/abs/2506.20332) |
| 31 | UI-AGILE, Lian 2025 | CVPR 2026 Findings track (P, Crossref [DOI](https://doi.org/10.1109/cvprf71909.2026.00823)) | GRPO | None found (scan) | Continuous grounding + crop resampling | 9k samples from UI-R1, GUI-R1, Aguvis, Grounding-R1 data; AC at evaluation | [arXiv](https://arxiv.org/abs/2507.22025) |
| 32 | Orcust, Lu 2025 | Preprint | GRPO | None found (scan) | Environment + LLM critique | 15K online VM trajectories; AC at evaluation | [arXiv](https://arxiv.org/abs/2509.17917) |
| 33 | MagicGUI, Tang 2025 | Preprint | GRPO | None found (scan) | Spatially enhanced composite | AC in pretraining and evaluation | [arXiv](https://arxiv.org/abs/2508.03700) |
| 34 | Co-EPG, Zhao 2025 | AAAI 2026 (A) | GRPO | SFT only: AC Mob-7B Iter 3 **w/o GRPO 82.0, with GRPO 83.1** | Grounding-based composite (C-DREM) | **AC used as the mobile benchmark, with no external data** | [arXiv](https://arxiv.org/abs/2511.10705) |
| 35 | GUI-Eyes, Chen 2026 | AAAI 2026 (O, [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/40175)) | Agent-centric GRPO variant | None found (scan) | Spatially continuous | **3,000 training instances sampled partly from AC** | [arXiv](https://arxiv.org/abs/2601.09770) |
| 36 | SCA, Yang 2026 | Preprint | Group-relative credit replacing GRPO advantage | **Synthetic only: binary GRPO gradient MSE 0.16201 vs SCA 0.14754.** Benchmark tables list other models | Click-location credit | ScreenSpot and action benchmarks | [arXiv](https://arxiv.org/abs/2609.36939) |
| 37 | GTA1, Yang 2025 | Preprint | GRPO, no thinking | None found (scan) | Not extracted | OSWorld, ScreenSpot; AC only cited in scan | [arXiv](https://arxiv.org/abs/2507.05791) |
| 38 | HyperClick, Zhang 2025 | Preprint | GRPO | None found (scan) | Format + correctness + confidence | ScreenSpot; no AC/AW | [arXiv](https://arxiv.org/abs/2510.27266) |
| 39 | GUI-RCPO, Du 2025 | AAAI 2026 (A) | GRPO at test time | None found (scan) | Region consistency | ScreenSpot; no AC/AW | [arXiv](https://arxiv.org/abs/2508.05615) |
| 40 | GUI-Cursor, Zhao 2025 | ICML 2026 (A) | GRPO | None found (scan) | Trajectory reward from visual feedback | ScreenSpot, OSWorld; no AC/AW | [arXiv](https://arxiv.org/abs/2509.21552) |
| 41 | POINTS-GUI-G, Zhao 2026 | Preprint | GRPO | None found (scan) | Not extracted | ScreenSpot, OSWorld; no AC/AW | [arXiv](https://arxiv.org/abs/2602.06391) |
| 42 | WM-R1, Han 2026 | Preprint | GRPO with world-model calls | Claims "GRPO-only baselines", but Table 1 rows seen are named models (GUI-R1-3B 17.4, UI-R1-3B 18.6, WM-R1-3B 29.5, AW Full) | Success + length + world-model call count | AC and AW at evaluation | [arXiv](https://arxiv.org/abs/2608.27508) |
| 43 | Code2World, Zheng 2026 | Preprint | GRPO after SFT | None found (scan) | Visual semantic + action consistency | **Over 80K AndroidCode samples derived from AC**; AW at evaluation | [arXiv](https://arxiv.org/abs/2602.09856) |
| 44 | DPO with LLM judge, Luo 2025 | Preprint | DPO | None found; PPO only as background | LLM-judge scores | OSWorld; no AC/AW | [arXiv](https://arxiv.org/abs/2506.03095) |

Rows 12-44 are 33 papers. Three named or adjacent papers were opened and excluded from the tally:
- [InfiGUIAgent](https://arxiv.org/abs/2501.04575) (preprint): keyword scan found no RL algorithm name.
- [UI-Venus-2](https://arxiv.org/abs/2609.00028) (preprint): RL is described, but GRPO and PPO do not appear in the scan, so the algorithm is unknown.
- [AppVLM](https://arxiv.org/abs/2502.06395) (preprint): its "Reinforce Fine-Tuning" is iterative SFT with rejection sampling, and the authors say it should not be confused with REINFORCE. It uses AC for SFT.

#### Tally

| Algorithm, GUI set (33) | Count | Rows |
|---|---|---|
| GRPO or direct variant | 26 | 12, 13, 16-20, 23-26, 29-43 |
| AEPO, base unnamed | 1 | 15 |
| RLOO | 1 | 14 |
| PPO | 2 | 22, 27 |
| AWR | 1 | 28 |
| DPO | 2 | 21, 44 |

| Baseline class, GUI set (32 checked; DigiRL excluded) | Count | Rows |
|---|---|---|
| A different named RL algorithm | 2 | 22 (figure only), 27 (numbers against DigiRL) |
| Vanilla GRPO or own variant only | 7 | 15, 16, 24, 25, 26, 36, 42 |
| No RL alternative found: SFT or other models | 23 | Remainder |

In the VLM set of 11: 3 compare different named algorithms with numbers (rows 7, 8, 9), 2 compare own variant against GRPO (rows 10, 11), and 6 show no RL alternative (rows 1-6).

### Inferences
- Most GUI "baselines" are other RL-trained models (GUI-R1, UI-R1), which differ in data, backbone and reward as well as algorithm. These comparisons do not isolate the algorithm.
- GRPO is effectively an unexamined default in GUI work: authors extend it and report improvement over it, but rarely test it against an alternative.
- The tally likely understates variety in the wider field because the sample is seeded with GRPO-related names and searches. It also likely overstates VLM cross-algorithm comparison, since I searched specifically for DAPO comparisons.
- [suy] A thesis comparing GRPO with PPO, DAPO or RLOO on the same GUI data, same backbone and same reward would fill a real gap in this sample.

### Gaps
- "None found (scan)" is not a line-by-line reading of every table. A competitor labeled only by a model name would be missed.
- ZeroGUI Table 4, the PAPO DAPO row, and the InfiGUI-G1 per-benchmark values were not reliably extracted.
- The sample is not a systematic review, and citation searches beyond arXiv were limited by rate limiting on DBLP, Semantic Scholar and part of OpenAlex.

## Is there any comparison of GRPO vs PPO vs DAPO vs DPO etc. on multimodal or GUI data, with numbers?

### Takeaway
Yes on multimodal data, for GRPO vs DAPO, and the gaps are about 1 point or less with no consistent winner. On GUI data the only direct PPO vs GRPO comparison found is UI-TARS-2, and it reports training-reward curves, not numbers. No paper in this sample compares GRPO, PPO, DAPO and DPO together on GUI or multimodal data.

### Cited Findings
- UI-TARS-2 says PPO "consistently outperforms GRPO by a clear margin" and "maintains higher rewards with lower volatility". This is a "preliminary evaluation" shown in Figure 12 on GUI-Browsing and GUI-General training sets, and led to choosing PPO for the main experiments. — [UI-TARS-2](https://arxiv.org/abs/2509.02544)
- ReVisual-R1 Table 4, average across six multimodal benchmarks: PAD 47.7, GRPO-Filter 46.0, Random-Sampling 46.2, DAPO 46.1, GRPO-Baseline 45.1. DAPO beats GRPO-Baseline by 1.0. — [ReVisual-R1](https://proceedings.iclr.cc/paper_files/paper/2026/hash/3792ac815260f4ba55ed71c7906cce36-Abstract-Conference.html)
- TGRL on Qwen2.5-VL-7B, average of five benchmarks: GRPO 57.16 vs DAPO 56.92, so GRPO is 0.24 higher. These appear as the "w/o Expert" rows. The paper's focus is its own method, so this is a side result, not a dedicated benchmark. — [TGRL](https://arxiv.org/abs/2603.26126)
- PAPO gives overall GRPO 47.92, GRPO + NoisyRollout 50.61, PAPO-G 49.92, PAPO-G + NoisyRollout 51.89, and states 4.4-17.5% average gains over GRPO and DAPO. Its GRPO baseline uses clip-higher in all experiments, so it is not plain GRPO. — [PAPO](https://arxiv.org/abs/2507.06448)
- On GUI data, adding GRPO then ARPO to the same base gives step-wise gains on OSWorld: UI-Tars-7B-1.5 23.5, + GRPO 26.0, + ARPO 29.9. — [ARPO](https://arxiv.org/abs/2505.16282)
- VEM shows PPO-style policy optimization on a pretrained value model against DigiRL on AITW General: VEM 82.6 step and 28.0 task SR, DigiRL online 83.3 and 23.0. Its claim of better stability than standard PPO rests on a loss figure. — [VEM](https://arxiv.org/abs/2502.18906)
- GUI-G1 on ScreenSpot average: Standard GRPO 82.3, length-debiased 83.2, difficulty-weighted 83.3. — [GUI-G1](https://arxiv.org/abs/2505.15810)
- A text-only study compares PPO, GRPO and DAPO on one model and dataset, and reports that DAPO's dynamic sampling gave no benefit while adding over 25% compute. I read only a search summary of this, so verify before citing. It is outside the multimodal scope. — [Lian 2025](https://arxiv.org/abs/2512.07611)

### Inferences
- GRPO vs DAPO differences here (+1.0 in one paper, -0.24 in another) are small and change sign, so neither paper supports a general ranking. Each uses different data and settings.
- Papers introducing a new method tend to report larger gains over vanilla baselines, so own-method rows should not be read as neutral algorithm benchmarks.

### Gaps
- UI-TARS-2 gives no tabulated PPO vs GRPO values, and the curves were not digitized.
- I found no GUI comparison with DPO, DAPO or RLOO as competing arms, and no numeric test-set PPO vs GRPO comparison on GUI data.
- No confidence intervals or repeated seeds were seen in the numeric rows above, except where MobileRL states a three-run average for its AW ablation and SCA reports three seeds.

## What reason do authors give for choosing that algorithm?

### Takeaway
The stated reasons are mostly about design and precedent: no critic or value model, the success of DeepSeek-R1, and efficiency or stability. Only UI-TARS-2 justifies its choice by an experiment against an alternative.

### Cited Findings
- UI-R1 presents GRPO as an alternative to PPO "by eliminating the need for a critic model", and notes many rule-based RL works adopt it. — [UI-R1](https://arxiv.org/abs/2503.21620)
- WM-R1 says PPO requires training a separate value network, whereas GRPO removes this overhead. — [WM-R1](https://arxiv.org/abs/2608.27508)
- ARPO calls GRPO a recent PPO variant that needs no value function, and cites its promising results. — [ARPO](https://arxiv.org/abs/2505.16282)
- SE-GUI says GRPO "stands out for its efficiency" by replacing heavy value models with a simple rule-based reward system. — [SE-GUI](https://arxiv.org/abs/2505.12370)
- UI-Venus-1.5 cites relative advantages estimated from a group of trajectories, bypassing a separate value function. — [UI-Venus-1.5](https://arxiv.org/abs/2602.09082)
- ZeroGUI starts from GRPO because it needs no extra value function and works in other LLM and VLM post-training settings. — [ZeroGUI](https://arxiv.org/abs/2505.23762)
- Precedent from DeepSeek-R1 is cited directly by Visual-RFT and by Vision-R1 (Zhan), and GUI-G1 and UI-Venus describe GUI work as following the same line. — [Visual-RFT](https://arxiv.org/abs/2503.01785); [Vision-R1 Zhan](https://arxiv.org/abs/2503.18013); [GUI-G1](https://arxiv.org/abs/2505.15810); [UI-Venus](https://arxiv.org/abs/2508.10833)
- R1-Onevision says GRPO's clipping prevents extreme policy shifts while KL regularization keeps the policy near the baseline. — [R1-Onevision](https://arxiv.org/abs/2503.10615)
- InfiGUI-R1 chooses RLOO because the leave-one-out baseline reduces gradient variance and removes the need for a separate value or critic model. — [InfiGUI-R1](https://arxiv.org/abs/2504.14239)
- UI-TARS chooses DPO so that erroneous steps from online bootstrapping are used as negatives, which SFT would ignore. — [UI-TARS](https://arxiv.org/abs/2501.12326)
- UI-TARS-2 chooses PPO because of its preliminary PPO vs GRPO evaluation, and pretrains the value model after observing value estimates negatively correlated with rewards. — [UI-TARS-2](https://arxiv.org/abs/2509.02544)
- Several papers also report GRPO weaknesses rather than reasons for it: gradient stagnation in multimodal RL (ReVisual-R1), dependence on initial accuracy on tables (Table-R1), length and difficulty biases (GUI-G1), uniform sampling inefficiency (MobileRL), and insufficient exploration compared with SFT at thousands of steps (OThink-MR1). — [ReVisual-R1](https://arxiv.org/abs/2506.04207); [Table-R1](https://arxiv.org/abs/2509.16889); [GUI-G1](https://arxiv.org/abs/2505.15810); [MobileRL](https://arxiv.org/abs/2509.18119); [OThink-MR1](https://arxiv.org/abs/2503.16081)

### Inferences
- "No critic" is a cost and simplicity argument, not evidence of better performance. The one GUI paper that ran both reached the opposite conclusion, though on training reward, multi-turn tasks and with a value-model pretraining step.
- A thesis can state fairly that GRPO's selection in this literature is driven mainly by design convenience and precedent.

### Gaps
- I did not read the full motivation section of every row, so other reasons may exist in the "None found (scan)" papers.

## Is there any paper training on AndroidControl with an RL objective?

### Takeaway
Yes, but rarely, and always for action prediction, grounding or world modeling. InfiGUI-R1 states it directly, with RLOO. Co-EPG and GUI-Eyes are probable GRPO cases, and Code2World uses data derived from AC. No paper in this sample trains an instruction-generation model on AC with an RL objective.

### Cited Findings
- InfiGUI-R1 says its RL phase uses core GUI trajectory data "e.g., from AndroidControl", and lists AC at 10k trajectories plus 2k reflection-focused trajectories in its mix. It uses RLOO and is a preprint. — [InfiGUI-R1](https://arxiv.org/abs/2504.14239)
- Co-EPG reports GRPO-based iteration relying "solely" on the benchmark dataset without external data, and Table 7 reports per-iteration results on AC (Mob-7B, 67.0/88.8/77.9 at iteration 1 w/o GRPO; 74.2/92.0/83.1 at iteration 3). — [Co-EPG](https://arxiv.org/abs/2511.10705)
- GUI-Eyes samples 3,000 training instances from OS-Atlas, OS-Genesis, GUI-R1 and AC, under a GRPO variant for a tool-augmented grounding task. — [GUI-Eyes](https://arxiv.org/abs/2601.09770)
- Code2World builds AndroidCode (over 80K samples) from AC trajectories, then uses GRPO in its render-aware stage. The model predicts the next UI rather than an action or instruction. — [Code2World](https://arxiv.org/abs/2602.09856)
- MobileRL explicitly excludes AC from RL: "data from AndroidControl was not included during the RL stage". AC is used only for SFT. — [MobileRL](https://arxiv.org/abs/2509.18119)
- AppVLM uses AC for SFT, then collects data on AndroidWorld with iterative SFT rather than an RL algorithm. — [AppVLM](https://arxiv.org/abs/2502.06395)
- SE-GUI evaluates AC zero-shot after training on grounding data only, and GUI-R1 uses only benchmark test splits. — [SE-GUI](https://arxiv.org/abs/2505.12370); [GUI-R1](https://arxiv.org/abs/2504.10458)
- AgentCPM-GUI adds AC thought-annotated data in its warm-up, not its described RFT trajectories. — [AgentCPM-GUI](https://arxiv.org/abs/2506.01391)

### Inferences
- [suy] Co-EPG's Mob models very probably run GRPO on AC training data, given "no external data" and Table 7, but I did not read a sentence stating that split directly.
- [suy] The thesis uses AC `step_instructions` as a generation target under a text-metric reward. That reverses the direction of every paper here, which maps an instruction to an action or point. No precedent appeared, but this sample cannot establish that none exists, so avoid "first" claims.

### Gaps
- MagicGUI and UI-Venus RL data composition were not fully confirmed: MagicGUI's AC use is confirmed in pretraining only, and UI-Venus's 350k dataset composition was not traced.
- **Names not found or not matching the brief:**
  - "Jedi": no RL or world-model paper of that name was found. It surfaced only in a search summary as a grounding dataset linked to OSWorld-G, which I did not open.
  - "Agent world-model style" work was covered with WM-R1 and Code2World. Their AC use is evaluation and data derivation respectively.
- **Venues not found:** VLM-R1, GUI-R1, InfiGUI-R1, ARPO, DART-GUI, Orcust and MagicGUI are labeled preprint because no venue was found, partly because of API rate limits. A later acceptance is possible.
- WM-R1 is recent and has no verified venue; check its table against released code before relying on its numbers.
