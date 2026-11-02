# Baselines used in RLHF and offline preference-optimization papers (2017-2026)

Evidence basis: full text of arXiv PDFs was extracted and searched on 1/11/2026 (tables, figures and the sentences naming comparators). Numbers below are therefore from the **arXiv versions**; published versions were not diffed. Venue status was checked at proceedings pages, PDF headers or Crossref DOI records, as noted per row.

## Which baselines are standard for RLHF papers?

### Takeaway
In this hand-picked sample, online methods are compared mostly against **PPO (10/15)**, SFT (8/15) and offline DPO (6/15). Offline methods are compared mostly against **SFT (9/12)** and **DPO (8/12)**, with PPO in 5/12, and the newest offline papers read here (SimPO, β-DPO, QRPO) no longer run PPO. **No offline paper in the sample compares numerically against REINFORCE, RLOO or GRPO.** QRPO and SimPO explicitly leave that comparison open.

### Cited Findings

#### Paper-by-paper table

Mode: **On** = samples from the current policy during training; **Semi** = alternates sampling rounds and training rounds; **Off** = fixed pairs or a dataset sampled before training. "Baselines" lists only comparators seen in tables, figures or text. PPO* means the paper says "RLHF" and the PPO identification is mine or is only indirect.

| # | Paper (authors, year) | Venue and how it was verified | Proposed | Mode | Baselines numerically compared | Task / dataset |
|---|---|---|---|---|---|---|
| 1 | Fine-Tuning Language Models from Human Preferences (Ziegler et al., 2019) | [arXiv](https://arxiv.org/abs/1909.08593), preprint (no venue found) | PPO + human preferences | On | Zero-shot, supervised fine-tuning, lead-3 copy baseline | Sentiment, descriptiveness, summarization |
| 2 | Learning to summarize from human feedback (Stiennon et al., 2020) | [NeurIPS 2020 page](https://proceedings.neurips.cc/paper_files/paper/2020/hash/1f89885d556929e98d3ef9b86448f951-Abstract.html), whose title reads "with human feedback"; [arXiv](https://arxiv.org/abs/2009.01325) reads "from" | PPO + reward model | On | Supervised-only models, human references | TL;DR, CNN/DM |
| 3 | Training language models to follow instructions with human feedback, InstructGPT (Ouyang et al., 2022) | [NeurIPS 2022 page](https://proceedings.neurips.cc/paper_files/paper/2022/hash/b1efde53be364a73914f58805a001731-Abstract-Conference.html) | PPO-ptx | On | GPT-3, prompted GPT-3, SFT, FLAN, T0++ | API prompts |
| 4 | Training a Helpful and Harmless Assistant (Bai et al., 2022) | [arXiv](https://arxiv.org/abs/2204.05862), preprint | RLHF (PPO) | On | **baselines not checked** (excluded from tally) | HH |
| 5 | RL4LMs / NLPO (Ramamurthy et al.) | ICLR 2023, from [PDF header](https://arxiv.org/pdf/2210.01241); OpenReview blocked the fetch | NLPO | On | PPO, Supervised, Supervised+PPO, zero-shot | GRUE benchmark |
| 6 | Quark (Lu et al., 2022) | [NeurIPS 2022 page](https://proceedings.neurips.cc/paper_files/paper/2022/hash/b125999bde7e80910cbdbd323087df8f-Abstract-Conference.html) | Quark | On | PPO, PPLM, GeDi and others (non-PPO numbers reused from earlier work) | Toxicity and other control tasks |
| 7 | Fine-Tuning with Advantage-Induced Policy Alignment, APA (Zhu et al.) | [arXiv](https://arxiv.org/abs/2306.02231); venue not verified | APA | On | PPO, AWR | StackExchange, HH, TL;DR |
| 8 | Pairwise PPO, P3O (Wu et al.) | [arXiv](https://arxiv.org/abs/2310.00212), header "under review", preprint | P3O | On | PPO, DPO, online-DPO | KL-reward trade-off, GPT-4 evaluation |
| 9 | ReMax (Li et al., 2024) | **ICML 2024**, [PMLR 235:29128-29163](https://proceedings.mlr.press/v235/li24cd.html) | ReMax | On | SFT, PPO, DPO, DPO+ReMax | full-hh-rlhf, AlpacaEval, MT-Bench |
| 10 | Back to Basics (Ahmadian et al., 2024) | **ACL 2024 long**, [Anthology pp. 12248-12267](https://aclanthology.org/2024.acl-long.662/) | RLOO | On | PPO, Vanilla PG, REINFORCE w/ baseline, RAFT, DPO | TL;DR, HH (Pythia, Llama) |
| 11 | RAFT (Dong et al., 2023) | TMLR 12/2023, from [PDF header](https://arxiv.org/pdf/2304.06767) | RAFT | On (filter rounds) | PPO, SFT | HH-RLHF |
| 12 | DeepSeekMath / GRPO (Shao et al., 2024) | [arXiv](https://arxiv.org/abs/2402.03300), preprint | GRPO | On | RFT, Online RFT in Figure 5. SFT, DPO and PPO are described in the unified framework, but I did **not** see them plotted in Figure 5 | GSM8K, MATH |
| 13 | DeepSeek-R1 (DeepSeek-AI, 2025) | [Nature](https://www.nature.com/articles/s41586-025-09422-z); [arXiv](https://arxiv.org/abs/2501.12948) | GRPO at scale | On | PPO (Supplementary A.3, Figure 4) | MATH |
| 14 | REBEL (Gao et al., 2024) | NeurIPS 2024, Crossref DOI 10.52202/079017-1660; [arXiv](https://arxiv.org/abs/2404.16767) | REBEL | On | SFT, DPO, REINFORCE, RLOO, PPO, Iterative DPO, APA. **REINFORCE, RLOO and PPO numbers are copied from other papers** | TL;DR, general chat |
| 15 | Direct Language Model Alignment from Online AI Feedback, OAIF (Guo et al., 2024) | [arXiv](https://arxiv.org/abs/2402.04792), **labelled preprint**: not in the volumes I scanned (Findings ACL, EMNLP, NAACL 2024) | Online DPO/IPO/SLiC | On | Offline DPO/IPO/SLiC, RLHF (PPO*), RLAIF, SFT | TL;DR, Helpfulness, Harmlessness |
| 16 | Bridging Offline and Online RL for LLMs (Lanchantin et al., 2025) | [arXiv](https://arxiv.org/abs/2506.21495), preprint | Comparative study | On + Semi | Seed, offline DPO, semi-online DPO, online DPO, GRPO | Math500, NuminaMath, AMC23, AlpacaEval, ArenaHard |
| 17 | ReST (Gulcehre et al., 2023) | [arXiv](https://arxiv.org/abs/2308.08998), preprint | ReST | Semi | BC, OAC, BVMPO, GOLD, PPO | IWSLT 2014, WMT 2020, Web Domain |
| 18 | SPIN (Chen et al., 2024) | ICML 2024, [PMLR v235](https://proceedings.mlr.press/v235/chen24j.html) | SPIN | Semi | zephyr-7b-sft-full (SFT), DPO | Benchmarks in the paper |
| 19 | Self-Rewarding Language Models (Yuan et al., 2024) | ICML 2024, [PMLR v235](https://proceedings.mlr.press/v235/yuan24d.html) | Self-rewarding + iterative DPO | Semi | SFT baseline, GPT-4 Turbo | AlpacaEval and others |
| 20 | DPO (Rafailov et al., 2023) | **NeurIPS 2023**, [proceedings page](https://papers.nips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html) | DPO | Off | PPO, PPO-GT, SFT, Preferred-FT, Unlikelihood, Best-of-N, zero/2-shot | Sentiment, TL;DR, HH |
| 21 | RRHF (Yuan et al., 2023) | NeurIPS 2023, [proceedings page](https://papers.nips.cc/paper_files/paper/2023/hash/23e6f78bdec844a9f7b6c957de2aae91-Abstract-Conference.html) | RRHF | Off (sampled before training) | PPO, SFT variants, Best-of-4 | HH |
| 22 | SLiC-HF (Zhao et al., 2023) | [arXiv](https://arxiv.org/abs/2305.10425), preprint | SLiC-HF | Off | SFT, continued SFT on best decodes, RLHF-PPO (Stiennon's decodes, not re-run) | TL;DR |
| 23 | PRO (Song et al., 2024) | AAAI 2024, Crossref DOI 10.1609/aaai.v38i17.29865 and [arXiv comment](https://arxiv.org/abs/2306.17492) | PRO | Off | SFT, RLHF (PPO*), CoH, DPO, RRHF, BoN | HH-RLHF |
| 24 | IPO (Azar et al., 2024) | AISTATS 2024, [PMLR v238](https://proceedings.mlr.press/v238/gheshlaghi-azar24a.html) | IPO | Off | DPO (bandit examples only) | Toy bandits |
| 25 | KTO (Ethayarajh et al., 2024) | **ICML 2024**, [PMLR v235, first page 12634](https://proceedings.mlr.press/v235/ethayarajh24a.html); the page title is "Model Alignment as Prospect Theoretic Optimization" | KTO | Off | SFT, DPO, ORPO, SLiC, CSFT, offline PPO variant | MMLU, GSM8k, HumanEval, BBH, others |
| 26 | ORPO (Hong et al., 2024) | **EMNLP 2024 main**, [Anthology 2024.emnlp-main.626](https://aclanthology.org/2024.emnlp-main.626/) | ORPO | Off | SFT, DPO, PPO, Zephyr models | HH-RLHF, UltraFeedback, AlpacaEval |
| 27 | SimPO (Meng et al., 2024) | NeurIPS 2024, [proceedings page](https://proceedings.neurips.cc/paper_files/paper/2024/hash/e099c1c9699814af0be873a175361713-Abstract-Conference.html) | SimPO | Off | SFT, RRHF, SLiC-HF, DPO, IPO, CPO, KTO, ORPO, R-DPO | AlpacaEval 2, Arena-Hard, MT-Bench |
| 28 | β-DPO (Wu et al., 2024) | NeurIPS 2024, Crossref DOI 10.52202/079017-4128 and [arXiv comment](https://arxiv.org/abs/2407.08639) | β-DPO | Off | DPO, data filtering, SimPO | HH, AlpacaEval |
| 29 | Relative Preference Optimization (Yin et al.) | [arXiv](https://arxiv.org/abs/2402.10958), preprint | RPO | Off | DPO, IPO, KTO (from text; tables not read in full) | Dialogue, summarization |
| 30 | Offline Regularised RL, DRO (Richemond et al., 2024) | [arXiv](https://arxiv.org/abs/2405.19107), preprint | DRO-V | Off | SFT, KTO | Side-by-side evaluation on T5-L, T5-XL |
| 31 | QRPO (Matrenok et al., 2025) | NeurIPS 2025, [proceedings page](https://proceedings.nips.cc/paper_files/paper/2025/hash/94840c41497ead6a84f493f029eba7fa-Abstract-Conference.html) | QRPO | Off / off-policy | Initial model, SFT-chosen, DPO, SimPO, REBEL | Magpie-Air, UltraFeedback, code |
| 32 | Loose lips sink ships, ODIN (Shen et al., 2023) | Findings of EMNLP 2023, [Anthology volume](https://aclanthology.org/volumes/2023.findings-emnlp/) | Reward-model debiasing + RLHF | On | **baselines not checked** (excluded) | HH, TL;DR |

Background rows, excluded from the tally: [PPO, Schulman et al. 2017](https://arxiv.org/abs/1707.06347) and [Christiano et al. 2017](https://arxiv.org/abs/1706.03741) are not LLM papers. [Korbak et al.](https://proceedings.mlr.press/v202/korbak23a.html) (ICML) studies pretraining rather than an RLHF stage.

**"GA-DPO" is not a published method as far as I can find.** In this repository it is the project's own name for "DPO + NLL anchored on ck500's greedy sentence" (`_scripts/314/ds_gadpo314/ga_dpo.py`). A web search found no paper with that name. The nearest matches, unread and baselines not checked, are [SGPO](https://arxiv.org/abs/2507.20181), [RS-DPO](https://arxiv.org/abs/2402.10038) and [CodeDPO](https://arxiv.org/abs/2410.05605). Do not cite GA-DPO as literature.

#### Baseline tally

The tally counts papers in which the baseline was seen as a numeric comparator. It excludes rows 4 and 32. A method is not counted as a baseline of its own paper. Tallied from the table above.

| Baseline | Online (n=15: rows 1-3, 5-16) | Semi (n=3: rows 17-19) | Offline (n=12: rows 20-31) | Total (n=30) |
|---|---|---|---|---|
| SFT / supervised | 8 | 3 | 9 | 20 |
| Offline DPO | 6 | 1 | 8 | 15 |
| PPO (or RLHF-PPO) | 10 (one PPO*) | 1 | 5 (one PPO*; a further offline variant in KTO is not counted) | 16 |
| Best-of-N | 0 | 0 | 3 | 3 |
| KTO | 0 | 0 | 3 | 3 |
| SimPO | 0 | 0 | 2 | 2 |
| IPO (offline) | 1 | 0 | 2 | 3 |
| ORPO | 0 | 0 | 2 | 2 |
| RRHF | 0 | 0 | 2 | 2 |
| SLiC (offline) | 1 | 0 | 2 | 3 |
| RAFT / RFT | 2 (BtB; DeepSeekMath's RFT) | 0 | 0 | 2 |
| REINFORCE | 2 (BtB, REBEL) | 0 | 0 | 2 |
| RLOO | 1 (REBEL) | 0 | 0 | 1 |
| GRPO | 1 (Bridging) | 0 | 0 | 1 |
| APA | 1 (REBEL) | 0 | 0 | 1 |
| REBEL | 0 | 0 | 1 (QRPO) | 1 |
| Online DPO variants | 2 (P3O, Bridging; REBEL's "Iterative DPO" adds one more if counted) | 0 | 0 | 2-3 |

- SimPO states that many studies already compare DPO and PPO and leaves "the comparison of PPO and SimPO to future work" — [SimPO, footnote 7](https://arxiv.org/abs/2405.14734).
- QRPO does not compare with online methods: "An open question is the impact of online data... and a comparison to policy improvement methods such as GRPO" — [QRPO, "Limitations and open questions"](https://arxiv.org/abs/2507.08068).
- QRPO explains its baseline choice: it uses DPO to stand for most preference methods, SimPO as the competitive inductive-bias variant, and REBEL for reward-difference optimization. It drops KTO because of divergence from the objective and because of SimPO's empirical results — [QRPO, §5](https://arxiv.org/abs/2507.08068).

### Inferences
- A paper proposing a new online method can defensibly use PPO + DPO + SFT as its minimum set. A new offline method can use SFT + DPO, usually with one recent winner such as SimPO. This is a reading of the sample, not a stated norm in any paper.
- The online and offline literatures rarely meet. Direct evidence between them comes from about eight papers (rows 8, 9, 10, 14, 15, 16, 20, 26), so any survey claim about "RLHF baselines" should name which side it means.

### Gaps
- The sample is hand-picked rather than a systematic review, so counts are descriptive and carry no statistical weight.
- DBLP and the Semantic Scholar API failed or rate-limited during verification. "Preprint" therefore means no venue was found in what I checked, not proof that none exists.
- APA's venue was not verified. My memory of a Findings venue for OAIF could not be confirmed, so it is labelled preprint.

## What head-to-head evidence exists between critic-free online methods, PPO and offline pair methods?

### Takeaway
Critic-free methods generally match or beat PPO in the papers proposing them, but **the PPO margin depends heavily on implementation**. The same TL;DR setup reports PPO at 67.6 in one paper and 77.6 in another. Online sampling beats offline pairs in several independent comparisons, yet online DPO and semi-online DPO match GRPO, so "online" appears to matter more than the choice of loss.

### Cited Findings

#### Critic-free vs PPO

**Back to Basics Table 1**, final win rates (GPT-4 judged) — [Ahmadian et al., ACL 2024; arXiv numbers](https://arxiv.org/abs/2402.14740):

| Method | TL;DR | HH (Pythia) | HH (Llama) |
|---|---|---|---|
| RLOO k=4 | 77.9 | 43.7 | 64.1 |
| RAFT k=4 | 73.2 | 42.1 | 63.3 |
| RLOO k=2 | 74.2 | 47.6 | 62.2 |
| RAFT k=2 | 72.1 | 37.7 | 58.4 |
| REINFORCE w/ baseline | 70.7 | 37.9 | 55.3 |
| Vanilla PG | 70.4 | 36.4 | 52.3 |
| PPO | 67.6 | 29.2 | 32.0 |
| DPO | 66.6 | 39.0 | 61.9 |

- The paper states RLOO k=4 outperforms PPO by 10.3, 14.5 and 32.1 — [same source](https://arxiv.org/abs/2402.14740).
- The paper's introduction claims Vanilla PG beats PPO "by 3.2% to 20.3%". From Table 1, Vanilla PG minus PPO gives **2.8 to 20.3**, so the lower figure does not reproduce from this arXiv table — [same source](https://arxiv.org/abs/2402.14740). Quote the table, not the sentence.
- **ReMax** on Llama-2-7B / full-hh-rlhf: rewards comparable to PPO and about 1.6× faster. GPT-4 win rate over SFT on AlpacaEval's 805 prompts improved by 31.4 points with SFT+ReMax. Figure 7 bars read 50.0 (SFT), 68.3, 78.3, 81.4 and 84.7 (DPO+ReMax) — [Li et al., ICML 2024](https://proceedings.mlr.press/v235/li24cd.html). Text extraction reverses the bar order, so the assignment 68.3 = SFT+DPO and 78.3 = SFT+PPO is my reading and should be checked against the figure.
- **ReMax memory and time** (Table 2, 4×A800-80GB, 33k samples): without offload PPO could not train while ReMax ran at batch size 96 in 1.8 h. With offload, PPO ran at batch 112 in 2.9 h and ReMax at batch 152 in 2.0 h — [arXiv 2310.10505](https://arxiv.org/abs/2310.10505).
- **R1 Supplementary A.3** is the most useful moderating evidence: at GAE λ=0.95, "PPO performs considerably worse than GRPO", but with λ=1.0 "PPO's performance improves substantially, nearing that of GRPO". The remaining GRPO advantage it claims is tuning and memory cost — [DeepSeek-R1, arXiv version](https://arxiv.org/abs/2501.12948).
- **REBEL Table 1**, TL;DR 6.9B: SFT 45.2, DPO 68.4, REINFORCE 70.7, PPO **77.6**, RLOO k=2 74.2, RLOO k=4 77.9, REBEL 78.1. The REINFORCE and RLOO numbers are copied from Ahmadian et al. and the PPO number from Huang et al. 2024 — [Gao et al.](https://arxiv.org/abs/2404.16767). Those PPO numbers come from different papers, so 67.6 vs 77.6 is not a controlled replication, but it shows how large the implementation gap can be.
- **RAFT** on HH-RLHF: SFT reward 0.772, PPO 2.077, RAFT 2.294 — [Dong et al., TMLR](https://arxiv.org/abs/2304.06767).
- **RRHF** on HH with Alpaca: PPO −1.03, RRHF_DP −1.03, RRHF_SP −0.96, Best-of-4 −0.97 — [Yuan et al.](https://arxiv.org/abs/2304.05302).
- **APA and P3O** claim to outperform PPO, in reward-model score and in the KL-reward trade-off respectively — [APA](https://arxiv.org/abs/2306.02231); [P3O](https://arxiv.org/abs/2310.00212). I read these claims but did not extract the numbers.

#### Online vs offline

- **DPO vs PPO, in favor of offline:** on TL;DR, DPO reaches about 61% vs PPO's 57% at its best temperature, and DPO samples were preferred 58% of the time over PPO samples at temperature 0. In the sentiment task DPO's reward/KL frontier "strictly dominates PPO", even PPO with ground-truth reward — [Rafailov et al.](https://arxiv.org/abs/2305.18290).
- **ORPO vs PPO, in favor of offline:** ORPO's pairwise win rate over PPO on OPT-125M/350M/1.3B is 66.1/79.4/65.9 (HH) and 71.4/85.8/65.7 (UltraFeedback). Over DPO it is 41.7/49.4/70.9 and 48.8/50.5/57.8, so ORPO loses or ties DPO at smaller scale — [Hong et al.](https://aclanthology.org/2024.emnlp-main.626/).
- **SLiC-HF vs PPO:** with a reward model the result is similar to RLHF-PPO, and with a ranking model better — [Zhao et al.](https://arxiv.org/abs/2305.10425). It compares against Stiennon's saved decodes rather than re-running PPO.
- **Back to Basics vs DPO, mixed:** RLOO beats DPO on all three columns, but REINFORCE w/ baseline loses to DPO on both HH columns (37.9 vs 39.0, 55.3 vs 61.9) and RAFT k=2 also does (37.7, 58.4) — [Table 1](https://arxiv.org/abs/2402.14740). "Online beats DPO" is not universal even in that paper.
- **OAIF, online vs offline for the same loss** (human raters, TL;DR): DPO 63.74/28.57/7.69 win/tie/loss, IPO 64.81/31.48/3.71, SLiC 71.43/26.98/1.59. Offline DPO overfits from about step 3,500. In a 4-way human comparison online DPO was preferred 58% of the time over SFT, RLHF and RLAIF. It also notes much longer responses as a confound and controls for it by length buckets — [Guo et al., preprint](https://arxiv.org/abs/2402.04792).
- **Bridging Table 2** (LC AlpacaEval GPT-4-1106 / GPT-4o; ArenaHard GPT-4-1106 / GPT-4o) — [Lanchantin et al., preprint](https://arxiv.org/abs/2506.21495):

| Method | AE GPT-4-1106 | AE GPT-4o | Arena GPT-4-1106 | Arena GPT-4o |
|---|---|---|---|---|
| Seed | 27.3 | 21.3 | 32.0 | 27.8 |
| Offline DPO | 53.2 | 38.3 | 39.4 | 38.2 |
| Semi-online DPO s=10 | 81.6 | 59.4 | 61.1 | 43.0 |
| Online DPO | 83.1 | 60.1 | 62.8 | 50.4 |
| GRPO | 75.2 | 55.0 | 59.1 | 54.3 |

- **Bridging Table 1** on math (Math500): seed 47.4, offline DPO 53.7, semi-online s=100 58.9, online 58.7. The paper reports semi-online DPO, online DPO and GRPO as performing similarly — [same source](https://arxiv.org/abs/2506.21495).
- **QRPO vs REBEL in offline or off-policy mode** (Llama 8B Tülu, Magpie-Air, AlpacaEval LC): DPO 47.7, SimPO 49.2, REBEL 46.3, QRPO 50.6 — [Matrenok et al.](https://arxiv.org/abs/2507.08068). Here REBEL is not run in its online regime as in its own paper, so this is not an online-vs-offline test.
- **ReST vs PPO:** online RL performs as well as ReST (G=1, I=0), and ReST with Improve steps is "significantly better" — [Gulcehre et al., preprint](https://arxiv.org/abs/2308.08998).
- **Same-side offline evidence:** KTO's offline PPO variant with dummy +1/−1 rewards performs as well as DPO for all models except Llama-30B — [KTO](https://proceedings.mlr.press/v235/ethayarajh24a.html). On Zephyr-β-SFT (MMLU, GSM8k, HumanEval, BBH), SFT 57.2/39.0/30.1/46.3, DPO 58.2/40.0/30.1/44.1, ORPO 57.1/36.5/29.5/47.5, KTO 58.6/53.5/30.9/52.6 — [KTO Table 2](https://arxiv.org/abs/2402.01306). In KTO's data ORPO does not beat SFT on three of four columns, and KTO's authors also report that up to 7B alignment gives "virtually no gains over SFT alone".
- **SimPO:** Mistral-Base AlpacaEval LC SFT 8.4, RRHF 11.6, SLiC 10.9, DPO 15.1, IPO 11.8, CPO 9.8, KTO 13.1. SimPO beats the best baseline by 3.6 to 4.8 points — [Meng et al.](https://arxiv.org/abs/2405.14734).
- **DRO-V vs KTO:** 63.4% (T5-L) and 57.5% (T5-XL) side by side — [Richemond et al., preprint](https://arxiv.org/abs/2405.19107).

### Inferences
- The most defensible summary: **removing the critic does not hurt in these settings, but "beats PPO" is not a stable effect size.** Back to Basics' PPO deficit should be read with R1's λ result and with the 77.6 figure from another implementation.
- Nearly all evaluation here is LLM-judged win rate. GPT-4 win rate and reward-model score are not comparable across papers, and the Bridging table shows judge choice can reverse order (online DPO vs GRPO on ArenaHard).
- Results also favor the proposing paper. Independent comparison papers such as Bridging and QRPO are therefore worth more per row than proposal papers.

### Gaps
- No preregistered or independent multi-seed replication of REINFORCE vs PPO in LLMs was found. Huang et al. 2024 was seen only as cited by REBEL.
- I did not capture the GRPO row of Bridging Table 1 (math) in extraction; the paper's text says it performs similarly.
- DeepSeekMath's Figure 5 compares RFT, Online RFT and GRPO variants as curves. I read no numeric table for them.
- I found no head-to-head of GRPO against RLOO or ReMax in the papers read.

## How do authors explain why a critic is or isn't needed for LLM RL?

### Takeaway
The arguments against a critic are of five kinds: reward arrives only at the end of a sequence, the environment is effectively deterministic, simulation is cheap, a pretrained model reduces variance, and a value model costs memory. The arguments keeping a value model are fewer, mostly regression-derived designs that use it as a learned partition function.

### Cited Findings
- **Pretrained start lowers the variance problem.** Earlier failures of REINFORCE "were based on scenarios with poor conditioning when training from random or weak initialization as opposed to warm-starting it from a strong pre-trained model", and prompt conditioning concentrates probability on a few tokens per step, so reducing variance further "at the cost of introducing bias is not worth it" — [Ahmadian et al.](https://arxiv.org/abs/2402.14740). This is the argument closest to starting RL from an SFT checkpoint.
- **Bias from bootstrapping.** In the same paper, PPO reward decreases monotonically as GAE λ decreases, and removing clipping does not hurt. At λ=1 PPO reduces toward Vanilla PG — [same source](https://arxiv.org/abs/2402.14740).
- **Token-level modeling is unnecessary.** REINFORCE w/ baseline, treating the whole generation as one action, is on par with Vanilla PG on Pythia and better on Llama (55.3 vs 52.3), and needs one less model copy — [same source](https://arxiv.org/abs/2402.14740).
- **Three properties of the RLHF problem:** fast simulation, a deterministic environment, and a trajectory-level reward, making it close to a "single-stage" optimization problem, so "the value model designed in PPO does not fit the RLHF problem" — [ReMax, §3.3](https://arxiv.org/abs/2310.10505). The paper also says the value model and its training components take 46% of GPU memory on a 7B model and more than 4× memory compared with inference.
- **Prompt-adaptive baseline replaces the critic.** ReMax subtracts the reward of the greedy response, which needs no training. Its footnote argues a moving-average baseline does not adapt across prompts — [ReMax](https://arxiv.org/abs/2310.10505). Note that this baseline is the same idea as SCST's greedy baseline; the [SCST paper](https://arxiv.org/abs/1612.00563) was downloaded, and its relation to ReMax's wording was not checked.
- **Group mean replaces the critic.** GRPO "foregoes the critic model", because a value model of comparable size adds memory and computation, and because in LLMs usually only the last token gets a reward, "which may complicate the training of a value function that is accurate at each token" — [DeepSeekMath](https://arxiv.org/abs/2402.03300). R1 says predicting expected return from each position is "inherently difficult, especially when only the final outcome reward is available" — [DeepSeek-R1](https://arxiv.org/abs/2501.12948).
- **Other removal routes:** P3O expands the baseline using a second sample y′ into an unbiased estimator, "bypassing the need to learn an additional value function V", and also skips GAE — [Wu et al.](https://arxiv.org/abs/2310.00212). REBEL eliminates "the complexity of using value networks" by regression on reward differences — [Gao et al.](https://arxiv.org/abs/2404.16767). RRHF notes PPO requires one more value model and four models in total — [Yuan et al.](https://arxiv.org/abs/2304.05302).
- **DPO's framing of actor-critic instability:** the normalization term can be read as the soft value function of the reference policy, and without it the policy gradient "could have high variance" — [Rafailov et al.](https://arxiv.org/abs/2305.18290).
- **Keeping a value model:** DRO-V learns a value function jointly, and QRPO's authors say this loses the simplicity of policy-fitting methods — [DRO](https://arxiv.org/abs/2405.19107); [QRPO](https://arxiv.org/abs/2507.08068). InstructGPT initializes its value function from the reward model — [Ouyang et al.](https://arxiv.org/abs/2203.02155).

### Inferences
- These arguments apply directly to short deterministic-reward generation such as sentence-level SPICE reward: one terminal reward and a strong SFT start. They would apply less to multi-turn or environment-interactive tasks, and none of these papers tests that setting.
- Most stated reasons are structural or about cost. Direct measurement of bias vs variance appears mainly in Back to Basics' λ experiment and R1's PPO λ comparison.

### Gaps
- No paper here measures the actual critic prediction error on LLM rewards.
- None directly tests whether the "strong initialization" explanation holds by varying initialization quality while holding the algorithm fixed.

## Are there comparisons where the policy starts from an SFT checkpoint with a metric-based reward rather than human preference?

### Takeaway
Yes, but few within the LLM RLHF literature. **ReST, RL4LMs and DeepSeekMath/R1** are the closest, and they use metric or verifiable rewards. ReST and RL4LMs carry the warning most relevant here: online PPO on a metric can exploit it, and supervised warm-starting helps in part because of this.

### Cited Findings
- **ReST** starts from a policy "pre-trained using BC" and uses machine-translation metric reward models (Metric X in the main experiments, plus BLEURT, COMET, BLEU). Its footnote says "online PPO algorithm can learn to exploit the weaknesses and biases of these two metrics quickly", which can maximize reward while worsening output. In its PPO comparison the validation BLEU of the online RL policy dropped nearly 8 points while ReST's did not change. The paper reads that as potential reward hacking — [Gulcehre et al., preprint](https://arxiv.org/abs/2308.08998). I did not confirm that the PPO arm starts from the same BC checkpoint; it follows the setup of Donato et al. 2022.
- **RL4LMs** has an explicit warm-start arm: "NLPO+supervised and PPO+supervised usually always outperforms NLPO/PPO (or supervised in isolation)". Warm-starting is "particularly effective for Commongen and ToTTo", tasks it describes as more prone to reward hacking. DailyDialog is the exception, attributed to weak supervised models. Its human ranking is Supervised+NLPO > Supervised ≥ Supervised+PPO > NLPO ≥ PPO > Zero-shot, with Supervised beating Supervised+PPO on 2 of 5 tasks even when automated metrics said otherwise — [Ramamurthy et al., ICLR 2023](https://arxiv.org/abs/2210.01241).
- **DeepSeekMath:** "PPO/GRPO initializes the policy model using the SFT model", and compares RFT, Online RFT and GRPO on GSM8K/MATH with an answer-correctness reward — [Shao et al., preprint](https://arxiv.org/abs/2402.03300).
- **R1:** PPO vs GRPO on MATH, using a verifiable reward task — [DeepSeek-AI](https://arxiv.org/abs/2501.12948). I did not check whether its starting model is SFT in the same sense.
- **Bridging:** verifiable math with a seed Llama-3.1-8B-Instruct model, comparing offline DPO, online DPO and GRPO. Pairs for DPO come from ranking responses by reward — [Lanchantin et al., preprint](https://arxiv.org/abs/2506.21495). This is the closest template for running both pair-based and online arms on one scalar reward. The seed is an off-the-shelf instruct model rather than the authors' SFT checkpoint.
- **QRPO:** the same reward model, ArmoRM, is used to rank pairs for DPO and SimPO and to train REBEL and QRPO, "ensuring an equal potential signal source for all methods". SFT-chosen is one of its starting options — [Matrenok et al.](https://arxiv.org/abs/2507.08068). The reward is a neural judge rather than a reference metric.
- **Older non-LLM sequence-training line** (seen only as headers and keyword counts here, so **baselines not checked**, excluded from the tally): [MIXER, ICLR 2016](https://arxiv.org/abs/1511.06732), [Actor-Critic for sequence prediction, ICLR 2017](https://arxiv.org/abs/1607.07086), [SCST](https://arxiv.org/abs/1612.00563), [Paulus et al.](https://arxiv.org/abs/1705.04304). These pretrain with cross-entropy and then optimize a metric, which is the thesis's own setting. Back to Basics cites Ranzato and Bahdanau as the earlier evidence for REINFORCE's high variance.
- **ROUGE as a warning:** DPO says summarization metrics such as ROUGE "can be poorly correlated with human" preferences — [Rafailov et al.](https://arxiv.org/abs/2305.18290).

### Inferences
- **Implication for the thesis's comparison design:** a fair same-signal test would follow QRPO or Bridging, where one scalar reward (SPICE here) drives both online arms and pair construction, starting from the same SFT checkpoint. I found no published head-to-head of PPO/REINFORCE/RLOO/GRPO vs DPO/ORPO from an SFT checkpoint under a **reference-based text metric** on an LLM. If that holds up under the other research strands, this is a real gap the thesis could state, though not a claim of novelty.
- ReST and RL4LMs suggest reporting an independent metric or tool alongside the reward metric, since gaming shows up there. The project's executability score and independent pointers already serve this role.

### Gaps
- Exact reward definitions for each RL4LMs GRUE task were not extracted.
- ReST's Table 1 values were not extracted because of table layout in the PDF text.
- Whether DPO-from-SFT under a metric reward appears in image-captioning or summarization venues was outside this scope and may be covered by adjacent notes.
