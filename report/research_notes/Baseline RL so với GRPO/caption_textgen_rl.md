# RL with sentence-metric rewards: algorithm baselines and reward metrics in captioning and text generation

Method note. Tables and text were read from the PDFs (arXiv or ACL Anthology) by text extraction on 1/11/2026. "CVF" means the CVF Open Access page loaded with its conference metadata. Where the publisher page was blocked, the venue evidence is named (PDF header, DBLP key through Semantic Scholar, Crossref). OpenReview returned a browser check, so ICLR venues rest on PDF headers or DBLP keys. All numbers are test-set values on the split the paper names, unless marked otherwise. They are not comparable between rows, because models, features and splits differ.

## Objective: paper-by-paper table and tally

### Takeaway
SCST is the default training algorithm and the usual comparator in captioning. Metric-reward comparisons are few, and only a handful directly test another RL algorithm against it on caption quality.

### Cited Findings

"Algorithm baselines" lists only algorithms compared numerically in that paper. Architecture rows in a state-of-the-art table are not counted as algorithm baselines.

**A. Image captioning**

| # | Paper | Venue (evidence) | RL algorithm | Algorithm baselines numerically compared | Reward metric(s) | Dataset |
|---|---|---|---|---|---|---|
| 1 | Ranzato, Chopra, Auli, Zaremba. [Sequence Level Training with RNNs (MIXER)](https://arxiv.org/abs/1511.06732) | ICLR 2016 (PDF header) | REINFORCE + learned baseline + XE-to-RL schedule | XENT, DAD, E2E | BLEU (up to 4-grams), ROUGE-2 | COCO captions, translation, summarization |
| 2 | Rennie et al. [SCST](https://openaccess.thecvf.com/content_cvpr_2017/html/Rennie_Self-Critical_Sequence_Training_CVPR_2017_paper.html) ([arXiv](https://arxiv.org/abs/1612.00563)) | CVPR 2017 (CVF) | REINFORCE + greedy baseline | XE, REINFORCE, MIXER, MIXER-B, MIXER-CL | CIDEr, BLEU, ROUGE-L, METEOR | COCO Karpathy |
| 3 | Liu, Zhu, Ye, Guadarrama, Murphy. [PG optimization of SPIDEr](https://arxiv.org/abs/1612.00370) | ICCV 2017 ([Crossref DOI 10.1109/ICCV.2017.100](https://doi.org/10.1109/ICCV.2017.100)) | PG + Monte Carlo rollouts | MLE, MIXER-BCMR, MIXER-BCMR-A | BLEU-4, CIDEr, BCMR, SPICE, SPIDEr | COCO C-5 |
| 4 | Ren et al. [Embedding Reward](https://openaccess.thecvf.com/content_cvpr_2017/html/Ren_Deep_Reinforcement_Learning-Based_CVPR_2017_paper.html) ([arXiv](https://arxiv.org/abs/1704.03899)) | CVPR 2017 (CVF) | Actor-critic + curriculum | SL and own variants; MIXER only as published BLEU-4 | Visual-semantic embedding (not a sentence metric) | COCO |
| 5 | Zhang et al. [Actor-Critic Sequence Training](https://arxiv.org/abs/1706.09601) | Preprint (no venue found) | Actor-critic, per-token advantage | XE, Self-critical on same "Semantic" encoder | CIDEr | COCO dev, leaderboard |
| 6 | Anderson et al. [Up-Down](https://openaccess.thecvf.com/content_cvpr_2018/html/Anderson_Bottom-Up_and_Top-Down_CVPR_2018_paper.html) ([arXiv](https://arxiv.org/abs/1707.07998)) | CVPR 2018 (CVF) | SCST | None (XE vs CIDEr-optimized; architectures only) | CIDEr | COCO |
| 7 | Luo et al. [Discriminability objective](https://openaccess.thecvf.com/content_cvpr_2018/html/Luo_Discriminability_Objective_for_CVPR_2018_paper.html) ([arXiv](https://arxiv.org/abs/1803.04376)) | CVPR 2018 (CVF) | SCST-style | MLE, CIDEr, with and without DISC | CIDEr + retrieval-model discriminability | COCO val |
| 8 | Liu et al. [Show, Tell and Discriminate](https://openaccess.thecvf.com/content_ECCV_2018/html/Xihui_Liu_Show_Tell_and_ECCV_2018_paper.html) ([arXiv](https://arxiv.org/abs/1803.08314)) | ECCV 2018 (CVF) | REINFORCE | Ablation on retrieval weight (α=0 is the baseline) | CIDEr + self-retrieval | COCO, Flickr30k |
| 9 | Guo et al. [Natural Language Prior](https://arxiv.org/abs/1809.06227) | EMNLP 2018 (ACL ID D18-1083 through Semantic Scholar) | SCST + n-gram prior | XE, ED-SC, Att-SC; MIXER and Ren as published | Reward not stated in passages read (CIDEr discussed; scores adjusted for bad endings) | COCO |
| 10 | Chen et al. [Conditional GANs](https://arxiv.org/abs/1805.07112) | AAAI 2019 (DOI 10.1609/AAAI.V33I01.33018142 through Semantic Scholar) | SCST + discriminator | SCST alone (λ=0) | CIDEr, CIDEr-D, BLEU-4, ROUGE-L, METEOR, plus discriminator | COCO Karpathy |
| 11 | Gao et al. [Self-critical n-step](https://openaccess.thecvf.com/content_CVPR_2019/html/Gao_Self-Critical_N-Step_Training_for_Image_Captioning_CVPR_2019_paper.html) ([arXiv](https://arxiv.org/abs/1904.06861)) | CVPR 2019 (CVF) | Self-critical per-token advantage | XENT, SCST, PG-CIDEr (re-implemented) | CIDEr | COCO Karpathy |
| 12 | Huang et al. [AoANet](https://openaccess.thecvf.com/content_ICCV_2019/html/Huang_Attention_on_Attention_for_Image_Captioning_ICCV_2019_paper.html) ([arXiv](https://arxiv.org/abs/1908.06954)) | ICCV 2019 (CVF) | SCST | None (architectures) | CIDEr-D | COCO |
| 13 | Cornia et al. [M2 Transformer](https://openaccess.thecvf.com/content_CVPR_2020/html/Cornia_Meshed-Memory_Transformer_for_Image_Captioning_CVPR_2020_paper.html) ([arXiv](https://arxiv.org/abs/1912.08226)) | CVPR 2020 (CVF) | SCST variant, mean baseline over beam | None numerically (architectures) | CIDEr-D | COCO |
| 14 | Pan et al. [X-LAN](https://openaccess.thecvf.com/content_CVPR_2020/html/Pan_X-Linear_Attention_Networks_for_Image_Captioning_CVPR_2020_paper.html) ([arXiv](https://arxiv.org/abs/2003.14080)) | CVPR 2020 (CVF) | SCST | None (architectures) | "Sentence-level reward"; metric not named at that passage | COCO |
| 15 | Seo et al. [Off-line human feedback](https://arxiv.org/abs/1911.09753) | AAAI 2020 (DOI 10.1609/AAAI.V34I03.5655 through Semantic Scholar) | Off-policy PG | Baseline, Baseline+, OnPG | Human ratings | Conceptual Captions |
| 16 | Luo. [Better Variant of SCST](https://arxiv.org/abs/2003.09971) | Preprint (Semantic Scholar lists arXiv only) | REINFORCE + leave-one-out sample baseline | SCST | CIDEr | COCO Karpathy |
| 17 | [B-SCST](https://arxiv.org/abs/2004.02435) | Preprint (Semantic Scholar lists arXiv only) | Bayesian SCST | SCST | CIDEr-D | Flickr30k, COCO, VizWiz |
| 18 | Zhang, Zhang, Zhao, Zou. [Image captioning via PPO](https://doi.org/10.1016/j.imavis.2021.104126) | Image and Vision Computing 2021 (Crossref, OpenAlex) | PPO | Baselines not checked (full text 403) | CIDEr (highlights) | Baselines not checked |
| 19 | Cho et al. [CLIP Reward](https://aclanthology.org/2022.findings-naacl.39/) | Findings of NAACL 2022 (ACL Anthology) | SCST | MLE (reward varies) | CIDEr, CLIP-S, CIDEr+CLIP-S, CLIP-S+Grammar | COCO, FineCapEval |
| 20 | Zhang et al. [CLIP Guided Group Optimization](https://arxiv.org/abs/2208.04254) | ECCV Workshops 2022 (arXiv comment) | SCST | MLE, SCST with CIDEr (reward varies) | CIDEr, group embedding gap | COCO |
| 21 | Takada et al. [DMO](https://aclanthology.org/2024.acl-long.453.pdf) | ACL 2024 (PDF header) | Not RL: reward-weighted augmented data | LM, SCST | CIDEr, BLEU-4, METEOR, ROUGE-L | Flickr8k, COCO |
| 22 | Moratelli et al. [Self-Cap](https://arxiv.org/abs/2408.16827) | ICPR 2024 (arXiv comment) | SCST | None (reward varies) | CIDEr, CLIP-S, PAC-S, CLIP-S+Gr, self-trained | COCO |
| 23 | Moratelli et al. [DiCO](https://arxiv.org/abs/2408.14547) | BMVC 2024 (DBLP key conf/bmvc through Semantic Scholar) | RL-free, derived from a PPO objective | SCST, Cho et al. | CLIP-S, PAC-S | COCO, Flickr30k |
| 24 | Liang. [GRPO for Image Captioning](https://arxiv.org/abs/2503.01333) | Preprint | GRPO | CE, SCST | CIDEr | COCO Karpathy, Flickr8k |
| 25 | Zhang et al. [SC-Captioner](https://arxiv.org/abs/2508.06125) | ICCV 2025 ([poster page](https://iccv.thecvf.com/virtual/2025/poster/2454)) | Multi-turn PG with reference-model KL | Zero-shot, SFT, SFT+DPO | Scene-graph set bonus and penalty | RefinedCaps, DOCCI500 |
| 26 | Xing et al. [CapRL](https://arxiv.org/abs/2509.22647) | Preprint (PDF header) | GRPO | Dataset comparison only | LLM answer accuracy on VQA questions | Own |
| 27 | Tang et al. [CCCaption](https://arxiv.org/abs/2602.21655) | CVPR 2026 ([poster page](https://cvpr.thecvf.com/virtual/2026/poster/38974)) | GRPO | Other models only (benchmarks) | Completeness + correctness queries | Own, CapArena, Prism |

**B. Text generation, video, instructions, referring expressions**

| # | Paper | Venue (evidence) | RL algorithm | Algorithm baselines numerically compared | Reward metric(s) | Dataset |
|---|---|---|---|---|---|---|
| 28 | Bahdanau et al. [Actor-Critic for Sequence Prediction](https://arxiv.org/abs/1607.07086) | ICLR 2017 (PDF header) | Actor-critic | LL, REINFORCE, REINFORCE-critic; MIXER as published | BLEU (smoothed) for translation | Spelling correction, IWSLT 2014, WMT14 |
| 29 | Paulus, Xiong, Socher. [Deep Reinforced Model](https://arxiv.org/abs/1705.04304) | ICLR 2018 (DBLP key conf/iclr through Semantic Scholar) | SCST | ML, RL, ML+RL | ROUGE-L (ROUGE-2 rejected) | CNN/DM, NYT |
| 30 | Pasunuru, Bansal. [Entailment Rewards](https://aclanthology.org/D17-1103/) | EMNLP 2017 (ACL Anthology) | PG + baseline estimator, mixed loss | XE | CIDEr, CIDEnt | MSR-VTT |
| 31 | Pasunuru, Bansal. [Multi-Reward](https://aclanthology.org/N18-2102/) | NAACL 2018 (ACL Anthology) | SCST, mixed loss | XE | ROUGE, Entail, ROUGESal, combinations | CNN/DM, DUC-2002 |
| 32 | Celikyilmaz et al. [Deep Communicating Agents](https://aclanthology.org/N18-1150/) | NAACL 2018 (ACL Anthology) | SCST | Baselines not checked | Reward metric not confirmed | Baselines not checked |
| 33 | Chen, Bansal. [Fast Abstractive](https://aclanthology.org/P18-1063/) | ACL 2018 (ACL Anthology) | A2C | Own without RL; Paulus RL+ML as published | ROUGE-L F1 | CNN/DM, DUC-2002 |
| 34 | Wang et al. [AREL](https://aclanthology.org/P18-1083/) | ACL 2018 (ACL Anthology) | PG with learned reward | XE-ss, GAN | BLEU, METEOR, ROUGE, CIDEr, learned | VIST |
| 35 | Wang et al. [Hierarchical RL](https://openaccess.thecvf.com/content_cvpr_2018/html/Wang_Video_Captioning_via_CVPR_2018_paper.html) ([arXiv](https://arxiv.org/abs/1711.11135)) | CVPR 2018 (CVF) | Hierarchical RL | XE-baseline, RL-baseline | CIDEr | MSR-VTT, Charades |
| 36 | Yu, Tan, Bansal, Berg. [Speaker-Listener-Reinforcer](https://openaccess.thecvf.com/content_cvpr_2017/html/Yu_A_Joint_Speaker-Listener-Reinforcer_CVPR_2017_paper.html) ([arXiv](https://arxiv.org/abs/1612.09542)) | CVPR 2017 (CVF) | PG | Ablation, MMI (RL algorithms none) | Learned discriminative classifier | RefCLEF, RefCOCO family |
| 37 | Fried et al. [Speaker-Follower](https://proceedings.neurips.cc/paper/2018/hash/6a81681a7af700c6385d36577ebec359-Abstract.html) ([arXiv](https://arxiv.org/abs/1806.02724)) | NeurIPS 2018 (proceedings page) | No RL on the speaker: MLE, cross-entropy | n/a | n/a | R2R |
| 38 | Wang et al. [Counterfactual Cycle-Consistent](https://openaccess.thecvf.com/content/CVPR2022/html/Wang_Counterfactual_Cycle-Consistent_Learning_for_Instruction_Following_and_Generation_in_Vision-Language_CVPR_2022_paper.html) ([arXiv](https://arxiv.org/abs/2203.16586)) | CVPR 2022 (CVF) | PG in framework | Baselines not checked | Not a sentence-metric reward as far as read | R2R |
| 39 | Stiennon et al. [Learning to Summarize](https://proceedings.neurips.cc/paper/2020/hash/1f89885d556929e98d3ef9b86448f951-Abstract.html) ([arXiv](https://arxiv.org/abs/2009.01325)) | NeurIPS 2020 (proceedings page) | PPO | Reward model vs ROUGE-optimized | Learned human reward, ROUGE | TL;DR, CNN/DM |
| 40 | Ramamurthy et al. [RL4LMs / NLPO](https://arxiv.org/abs/2210.01241) | ICLR 2023 (PDF header) | NLPO | PPO, Supervised, Zero Shot | Task rewards; library offers ROUGE, BLEU, METEOR, BERTScore | GRUE (7 tasks) |

Read but excluded from the table and tally: [Off-Policy Self-Critical Training](https://arxiv.org/abs/2006.11714) (venue not verified; baselines not read). [ViCrit](https://arxiv.org/abs/2506.10128) uses GRPO, but its reward is exact string match on an injected error, not a sentence metric. [Keneshloo et al.](https://arxiv.org/abs/1805.09461) is a survey (TNNLS, DOI 10.1109/TNNLS.2019.2929141).

**Tally: algorithm comparators** (papers whose own numbers include the comparator; "baselines not checked" rows excluded)

| Comparator | Count | Papers |
|---|---|---|
| SCST against a different training algorithm | 7 | ACST, n-step, Better-SCST, B-SCST, DMO, DiCO, GRPO (#5, 11, 16, 17, 21, 23, 24) |
| SCST held fixed, reward or add-on varied | 6 | Luo-DISC, Guo, cGAN, Cho, GEG, Self-Cap (#7, 9, 10, 19, 20, 22) |
| MIXER or MIXER-like | 2 run by the authors, 3 as published numbers | Run: SCST, Liu (#2, 3). Published: Ren, Guo, Bahdanau (#4, 9, 28) |
| Plain REINFORCE | 2 | SCST, Bahdanau (#2, 28) |
| Learned critic or parametrized estimator | 3 | Bahdanau RF-C, Gao PG-CIDEr, Rennie MIXER-CL (#28, 11, 2) |
| Actor-critic against SCST on captions | 1 | ACST, preprint (#5) |
| PPO as comparator | 1 | NLPO, not on captions (#40) |
| DPO as comparator | 1 | SC-Captioner (#25) |
| Trained with SCST but no algorithm comparison | 3 confirmed | Up-Down, AoANet, X-LAN; M2 uses a variant (#6, 12, 14, 13) |

**Tally: reward metrics** (papers that train with it, among rows where the metric was read)

| Reward | Count | Papers |
|---|---|---|
| CIDEr or CIDEr-D (including combined) | 20 | #2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 16, 17, 19, 20, 21, 22, 24, 30, 34, 35 |
| ROUGE variants | 8 | #1, 2, 10, 21, 29, 31, 33, 34 |
| BLEU | 7 | #1, 2, 3, 10, 21, 28, 34 |
| METEOR | 4 | #2, 10, 21, 34 |
| SPICE alone or SPICE-mix | 1 with numbers | #3 (PG-SPIDEr); PG-SPICE only described in text. #30 says it tried SPICE, numbers not in the main table |
| CLIP-S or PAC-S | 4 | #19, 20 (CLIP-based gap), 22, 23 |
| Learned, human or retrieval reward | 7 | #7, 8, 15, 22, 34, 36, 39 |
| LLM or query-based verification | 2 | #26, 27 |
| Scene-graph set reward | 1 | #25 |

### Inferences
- CIDEr is the default reward in this sample by a wide margin. The counts come from my sample, not a systematic review, so they show relative order only.
- GRPO appears in recent caption work (#24, 26, 27), and in #26 and 27 with verification-style rewards instead of CIDEr.

### Gaps
- Sampling was purposive, so tallies are not population estimates.
- ICLR entries could not be checked on OpenReview (browser check); AAAI OJS was also blocked.

## How standard is SCST and what do later papers compare it with?

### Takeaway
SCST is treated as the standard, and later papers mostly compare it with variants of itself. Reported gains over it on COCO are small, about +1 to +3 CIDEr points, and the one GRPO row sits in that range on a weak base model.

### Cited Findings
- Luo calls SCST "the new standard for training captioning models" and lists uses in video captioning, summarization, paragraph generation and speech recognition — [Luo 2020](https://arxiv.org/abs/2003.09971).
- Moratelli et al. call SCST the "most adopted paradigm" — [Self-Cap](https://arxiv.org/abs/2408.16827).
- Against MIXER (FC-2K, CIDEr-optimized, Karpathy test): XE 90.9, MIXER-B 101.9, MIXER 104.9, SCST 106.3 — [Rennie et al.](https://arxiv.org/abs/1612.00563)
- Against REINFORCE variants (Att2all, 4 seeds): REINFORCE 110.4 ± 0.5, REINFORCE with learned baseline (MIXER less CL) 113.2 ± 0.2, SCST 113.8 ± 0.3. The t-test rejects the null at α=0.1 on all metrics except ROUGE — [Rennie et al.](https://arxiv.org/abs/1612.00563)
- MIXER originally reported captioning BLEU-4 of XENT 27.8, DAD 28.16, E2E 26.42, MIXER 29.16 — [Ranzato et al.](https://arxiv.org/abs/1511.06732)
- N-step (greedy search, CIDEr): XENT 102.1, SCST 112.7, PG-CIDEr 113.9, 1-step-maxpro 115.1, 1-step-sample 115.4. In this re-implementation PG-CIDEr beats SCST on CIDEr, while SCST leads on BLEU-3, BLEU-4, METEOR, ROUGE-L and SPICE — [Gao et al.](https://arxiv.org/abs/1904.06861)
- Leave-one-out sample baseline, CIDEr: FC 104.5→105.3, Att2in 117.4→119.5, UpDown 122.7→123.9, Transformer 126.6→129.6 — [Luo 2020](https://arxiv.org/abs/2003.09971)
- M2 replaces the greedy baseline with the mean reward over the beam, "as we found it to slightly improve the final performance" — [Cornia et al.](https://arxiv.org/abs/1912.08226)
- B-SCST, COCO test, CIDEr-D: SCST 128.9, B-SCST 131.0 — [B-SCST](https://arxiv.org/abs/2004.02435)
- GRPO vs SCST: COCO CIDEr 97.6→100.0, SPICE 16.4→17.1, BLEU-4 30.5→31.4; Flickr8k CIDEr 36.6→38.3. GRPO was trained for 5 epochs. CE starts at only 84.3 — [Liang 2025](https://arxiv.org/abs/2503.01333)
- SCST also degrades output form: 46.4% and 43.7% bad-ending rate for ED-SC and Att-SC, against 0% for XE. Adjusted CIDEr falls 101.8→96.1 and 105.7→100.8 — [Guo et al.](https://arxiv.org/abs/1809.06227)
- DMO reaches comparable scores without RL. SCST still scores highest by epoch 20, but needs far more forward passes — [Takada et al.](https://aclanthology.org/2024.acl-long.453.pdf)

### Inferences
- Later gains over SCST on COCO fall between about +0.8 and +3 CIDEr points. Liang's +2.4 is in this range, but on a weak base model (CE 84.3), from a single author, with no seeds reported in what I read.

### Gaps
- Citation counts for SCST were not collected.
- B-SCST's and Luo's venues beyond arXiv were not found.

## Which papers directly compare reward metrics, with what numbers?

### Takeaway
Rennie, Liu, Wang (AREL), Cho and Moratelli give the clearest tables. CIDEr lifts other metrics most, narrow metrics get gamed, and CLIP rewards raise distinctiveness while wrecking reference-based scores. SPICE as sole reward has no numeric row in anything I read.

### Cited Findings
**Rennie et al. Table 3** (FC-2K, SCST, Karpathy test, greedy) — [source](https://arxiv.org/abs/1612.00563):

| Trained on | CIDEr | BLEU4 | ROUGE-L | METEOR |
|---|---|---|---|---|
| XE | 90.9 | 28.6 | 52.3 | 24.1 |
| CIDEr | 106.3 | 31.9 | 54.3 | 25.5 |
| BLEU | 94.4 | 33.2 | 53.9 | 24.6 |
| ROUGE-L | 97.7 | 31.6 | 55.4 | 24.5 |
| METEOR | 80.5 | 25.3 | 51.3 | 25.9 |

Rennie et al. also report being unable to beat CIDEr-only training with multiple-metric training. SPICE was not a training metric in this table — [source](https://arxiv.org/abs/1612.00563).

**Liu et al. Table 1** (Show-Tell, COCO C-5) — [source](https://arxiv.org/abs/1612.00370):

| Method | CIDEr-D | METEOR | ROUGE-L | BLEU-4 |
|---|---|---|---|---|
| MLE | 0.947 | 0.251 | 0.531 | 0.294 |
| PG-BLEU-4 | 0.966 | 0.249 | 0.550 | 0.346 |
| PG-CIDEr | 0.995 | 0.249 | 0.548 | 0.333 |
| MIXER-BCMR | 0.924 | 0.245 | 0.532 | 0.306 |
| MIXER-BCMR-A | 0.991 | 0.258 | 0.545 | 0.317 |
| PG-BCMR | 1.013 | 0.257 | 0.55 | 0.332 |
| PG-SPIDEr | 1.000 | 0.251 | 0.544 | 0.322 |

- Human evaluation on 492 images: PG-SPIDEr beats PG-BCMR (p=0.014) and MLE (p<0.001); PG-BCMR beats MLE (p=0.003). MLE "not bad" rate is 38%, human ceiling 87% — [Liu et al.](https://arxiv.org/abs/1612.00370)
- PG-SPICE "tends to generate ungrammatical sentences, with a lot of repeated phrases", and the authors "ignore pure SPICE in the rest of this paper" — [Liu et al.](https://arxiv.org/abs/1612.00370)

**Other tables**
- Cho et al. (COCO Karpathy; CIDEr / BLEU-4 / CLIP-S / R@1): MLE 110.3 / 32.5 / 0.758 / 21.8; CIDEr 124.9 / 38.2 / 0.759 / 20.9; CLIP-S 11.2 / 6.2 / 0.860 / 42.5; CIDEr+CLIP-S 124.6 / 37.7 / 0.772 / 24.4; CLIP-S+Grammar 71.0 / 16.9 / 0.793 / 35.8 — [Cho et al.](https://aclanthology.org/2022.findings-naacl.39/)
- Human preference, overall, CLIP-S+Grammar vs CIDEr: win 51.0, lose 30.8, tie 18.2 — [Cho et al.](https://aclanthology.org/2022.findings-naacl.39/)
- Self-Cap (RN50; CIDEr / SPICE / CLIP-S): none 109.8 / 20.3 / 0.743; CIDEr 126.8 / 21.2 / 0.739; CLIP-S 3.1 / 21.2 / 0.804; PAC-S 32.2 / 21.7 / 0.799; Self-Cap 72.0 / 21.8 / 0.780 — [Moratelli et al.](https://arxiv.org/abs/2408.16827)
- AREL (VIST; BLEU-4 / METEOR / ROUGE / CIDEr): XE-ss 13.7 / 34.8 / 29.7 / 8.7; BLEU-RL 13.9 / 34.6 / 29.0 / 8.9; METEOR-RL 6.8 / 40.2 / 30.0 / 1.2; ROUGE-RL 0 / 27.0 / 33.8 / 0; CIDEr-RL 13.8 / 34.9 / 29.7 / 8.1. The authors say METEOR-RL and ROUGE-RL game their metric with nonsense sentences — [Wang et al.](https://aclanthology.org/P18-1083/)
- Video captioning (CIDEr-D / CIDEnt): XE 44.6 / 34.4; CIDEr-RL 51.0 / 37.4; CIDEnt-RL 51.7 / 44.0. The text says CIDEr did best against rewards based on BLEU and SPICE, but those numbers are not in the main table — [Pasunuru & Bansal 2017](https://aclanthology.org/D17-1103/)
- Discriminability (ATTN; CIDEr / SPICE / Acc): MLE 1.1078 / .2019 / 72.40%; CIDEr 1.1332 / .2083 / 71.05%; CIDEr+DISC(1) 1.1406 / .2113 / 75.74%; CIDEr+DISC(10) 1.0552 / .2070 / 83.69%. Validation set — [Luo et al.](https://arxiv.org/abs/1803.04376)
- cGAN (reward under λ=0.3; CIDEr / BLEU-4 / SPICE): CIDEr 1.248 / .381 / .213; CIDEr-D 1.232 / .383 / .221; BLEU-4 1.182 / .383 / .209; ROUGE-L 1.195 / .368 / .217; METEOR 1.180 / .377 / .214 — [Chen et al.](https://arxiv.org/abs/1805.07112)
- DMO (not RL; GIT-base, Flickr8k; CIDEr scored): trained on CIDEr 97.0, BLEU-4 96.8, METEOR 96.1, ROUGE-L 96.0, standard LM 95.1 — [Takada et al.](https://aclanthology.org/2024.acl-long.453.pdf)
- Summarization (CNN/DM; R-1 / R-2 / R-L): XE 39.41 / 17.33 / 36.07; ROUGE 39.99 / 17.72 / 36.66; Entail 39.53 / 17.51 / 36.44; ROUGESal 40.36 / 17.97 / 37.00; ROUGESal+Ent 40.43 / 18.00 / 37.10 — [Pasunuru & Bansal 2018](https://aclanthology.org/N18-2102/)
- Paulus rejects ROUGE-2 as reward because summaries "almost always reached the maximum length", and uses ROUGE-L — [Paulus et al.](https://arxiv.org/abs/1705.04304)
- MIXER summarization: XENT and MIXER trained with ROUGE score 8.16 and 5.80 on BLEU, against 9.32 for MIXER trained with BLEU — [Ranzato et al.](https://arxiv.org/abs/1511.06732)

### Inferences
- Pattern across tables: training on a metric maximizes that metric. CIDEr is the only reward here that consistently lifts the others, and METEOR, ROUGE and pure SPICE are reported to degrade output when used alone.
- SC-Captioner's scene-graph set reward is close to SPICE in what it matches (objects, attributes, relations), but it rewards corrections rather than scoring a caption. This is my reading, not the authors' claim.

### Gaps
- No PG-SPICE numeric row was found. Liu's Table 1 has no SPICE column and PG-SPICE is not listed in it.
- Exact "not bad" percentages for Liu's PG methods are in a figure and were not extracted.
- Cho's PAC-S was not tested; Self-Cap covers it.

## Has any paper compared PPO or actor-critic to SCST on caption quality?

### Takeaway
Actor-critic: yes, one preprint with a small gain over SCST on a dev set. PPO: one journal paper exists, but I could not read its numbers. GRPO vs SCST: one preprint. I found no peer-reviewed paper I could read with a controlled PPO vs SCST row.

### Cited Findings
- Actor-critic vs SCST, same Semantic encoder, greedy, COCO dev: self-critical CIDEr-D 1.140, BLEU-4 .323, METEOR .266, ROUGE-L .554; actor-critic 1.162, .344, .267, .558. Per-minibatch time is 0.13 s vs 0.07 s, though "ours" also lacks the attention cell — [Zhang et al. 2017, preprint](https://arxiv.org/abs/1706.09601)
- Ren's actor-critic with embedding reward: CIDEr 0.937, BLEU-4 0.304, against MIXER's published 0.29 BLEU-4 and SL 0.872 / 0.289. It has no SCST row in the tables I read, and the reward differs — [Ren et al.](https://arxiv.org/abs/1704.03899)
- Outside captioning, IWSLT 2014 translation, BLEU greedy: LL 19.33, RF 20.92, RF-C 22.24, AC 21.66, MIXER* 20.73; beam: 21.46, 21.35, 22.58, 22.45. REINFORCE-critic beats actor-critic here, while on spelling correction AC is better in 3 of 4 settings without log-likelihood — [Bahdanau et al.](https://arxiv.org/abs/1607.07086)
- PPO applied to the X-Transformer model: the paper's highlights report that PPO can enforce trust-region constraints, that performance decreases when dropout is combined with PPO, and that word-level baselines are preferred to sentence-level ones in CIDEr optimization. The pre-trained X-Transformer starts at CIDEr 132.8. This comes from a search summary of the ScienceDirect page, not the full text — [Zhang et al. 2021](https://www.sciencedirect.com/science/article/abs/pii/S0262885621000317).
- X-Transformer's 132.8 single-model CIDEr-optimized score — [Pan et al.](https://arxiv.org/abs/2003.14080)
- GRPO vs SCST numbers are given above; Liang credits multiple candidates and the KL constraint — [Liang 2025](https://arxiv.org/abs/2503.01333)
- PPO vs NLPO on IMDB (not captions): sentiment PPO 0.602 vs NLPO 0.611, perplexity 33.816 vs 33.832. Without KL, sentiment jumps to 0.838 and perplexity to 41.897 — [Ramamurthy et al.](https://arxiv.org/abs/2210.01241)
- SC-Captioner on DOCCI500, Qwen2-VL-7B (BLEU-4 / METEOR / CAPTURE, first-turn): SFT 40.92 / 22.04 / 62.05; SFT+DPO 43.13 / 22.88 / 62.56; SFT+Ours 43.70 / 23.35 / 63.00. Self-corrected: DPO 44.49 / 23.84 / 62.51; Ours 44.88 / 25.18 / 63.34 — [Zhang et al. 2025](https://arxiv.org/abs/2508.06125)
- DiCO starts from a PPO objective with a per-token KL penalty but optimizes it directly without RL. On ViT-L/14 (CIDEr / PAC-S): SCST with PAC-S 51.1 / 0.862; DiCO with PAC-S 89.1 / 0.877 — [Moratelli et al. 2024](https://arxiv.org/abs/2408.14547)
- Stiennon's PPO comparison varies the reward (human model vs ROUGE), not the algorithm — [Stiennon et al.](https://arxiv.org/abs/2009.01325)

### Inferences
- Evidence for replacing SCST with PPO on CIDEr is thin. KL-regularized methods do seem to help when the reward is unstable (CLIP-style), as DiCO's gap and RL4LMs' no-KL rows suggest.
- A four-way comparison (SCST vs REINFORCE vs PPO vs GRPO, same model, same reward) was not found in this sample.

### Gaps
- The PPO paper's own final CIDEr and its SCST row are unread (ScienceDirect 403, OpenAlex and Crossref give no abstract). Its "plain policy gradient with clipping did not help" statement came only from a search summary, so treat it as unverified.
- I did not check for PPO captioning papers in journals outside this search.

## Why have critics been replaced by greedy baselines, according to the authors?

### Takeaway
Authors give three reasons: training difficulty of a second network, gradient variance, and test-time consistency. The measured gain over a learned baseline is small, and at least two papers report critics or other estimators doing as well.

### Cited Findings
- SCST "avoids all the inherent training difficulties associated with actor-critic methods, where a second 'critic' network must be trained to estimate value functions" — [Rennie et al.](https://arxiv.org/abs/1612.00563)
- SCST avoids "having to learn a (context-dependent) estimate of expected future rewards as a baseline", and has "much lower variance" — [Rennie et al.](https://arxiv.org/abs/1612.00563)
- The baseline is the test-time estimate, so "SCST is forced to improve the performance of the model under the inference algorithm used at test time" — [Rennie et al.](https://arxiv.org/abs/1612.00563)
- Rennie's gradient variance caveat: SCST has much higher variance than MIXER less CL in the first epoch, because samples initially score lower than greedy — [Rennie et al.](https://arxiv.org/abs/1612.00563)
- Luo says the self-critical baseline "is proved to be better than learned baseline function", then drops greedy decoding as well: no extra greedy pass, slightly faster, and better scores — [Luo 2020](https://arxiv.org/abs/2003.09971)
- MIXER is "very sensitive to the form of the annealing schedule, as well as other hyper-parameters, such as the learning rate or gradient scaling of the baseline estimator" — [Liu et al.](https://arxiv.org/abs/1612.00370)
- Gao concludes "self-critical per-token advantage is better than parametrized per-token advantage" (1-step-sample 115.4 vs PG-CIDEr 113.9) — [Gao et al.](https://arxiv.org/abs/1904.06861)
- Guo describes actor-critic as "often adopted" but needing an additional value network, while self-critical "leads to further performance gains" — [Guo et al.](https://arxiv.org/abs/1809.06227)
- Counterpoints: per-token actor-critic is reported above SCST, with the authors attributing this to per-token advantage and SCST needing two sampling passes per iteration — [Zhang et al. 2017](https://arxiv.org/abs/1706.09601). SCST's single greedy baseline can raise variance when the model is unstable, and limits diversity — [Liang 2025](https://arxiv.org/abs/2503.01333).
- Bahdanau's critic reduces the variance of REINFORCE and helps; RF-C uses it purely as a baseline — [Bahdanau et al.](https://arxiv.org/abs/1607.07086)

### Inferences
- The switch is justified mainly by simplicity. In Rennie's own 4-seed table the learned-baseline gap is 0.6 CIDEr points, far smaller than the gain of RL over XE.
- Later baselines (mean of beam, leave-one-out, group mean) keep the "no critic network" property and drop greedy decoding. GRPO's group-mean advantage belongs to this line (my reading; Luo's and Cornia's baselines are the closest published precedent in this sample).

### Gaps
- No paper here isolates the cost of training a critic in hours or GPU memory against SCST on the same model. Zhang's timing mixes architecture differences.
