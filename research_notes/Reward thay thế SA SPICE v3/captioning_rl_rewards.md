# Reward design for RL of image-to-text generation around SPICE and reference metrics (SCST 2017 → GRPO 2025–2026)

Notes compiled 15/11/2026. Every PDF marked "[read]" was opened and its text searched in this session, and the numbers below were copied from that text. Items marked "[snippet]" come only from search-engine summaries and were **not** checked against the paper. Items marked "[memory]" are from my prior knowledge, with a URL but not re-read here. They are kept to a minimum and must be checked before they go into the thesis.

---

## 1. SCST (Rennie et al., CVPR 2017) and SPIDEr (Liu et al., ICCV 2017): formulas, metric-as-reward ablations, what SPICE-only does to fluency

### Takeaway
SCST is REINFORCE with the greedy-decode reward as the baseline. In its ablation, **CIDEr(-D) was the only reward that raised every other metric**, while **METEOR as the reward dropped CIDEr below the cross-entropy model**. SPIDEr found that **SPICE alone produces long, ungrammatical captions with many repeated phrases**, so it uses **0.5·SPICE + 0.5·CIDEr**. The authors stopped reporting pure SPICE after the qualitative examples.

### Cited Findings
- **SCST gradient** (Eq. 9): ∂L/∂s_t = (r(w^s) − r(ŵ))·(p_θ(w_t|h_t) − 1_{w^s_t}). Here r(ŵ) is the reward of the caption that test-time inference produces (greedy decoding), so samples that score above the greedy output are pushed up and samples below it are suppressed. [read] — [Rennie et al., SCST, arXiv:1612.00563v2 (CVPR 2017), §4](https://arxiv.org/abs/1612.00563)
- **SCST Table 3** (Karpathy test split, FC-2K, greedy decoding). Training metric → evaluation CIDEr / BLEU-4 / ROUGE-L / METEOR: XE 90.9 / 28.6 / 52.3 / 24.1 · XE+beam 94.0 / 29.6 / 52.6 / 25.2 · **CIDEr 106.3 / 31.9 / 54.3 / 25.5** · BLEU 94.4 / **33.2** / 53.9 / 24.6 · ROUGE-L 97.7 / 31.6 / **55.4** / 24.5 · **METEOR 80.5** / 25.3 / 51.3 / **25.9**. [read] — [SCST arXiv v2, Table 3](https://arxiv.org/abs/1612.00563)
- SCST text: "optimizing for a given metric during training leads to the best performance on that same metric at test time… We experimented with training on multiple test metrics, and found that we were unable to outperform the overall performance of the model trained only on the CIDEr metric, which lifts the performance of all other metrics considerably." [read] — [SCST §5](https://arxiv.org/abs/1612.00563)
- **SCST Appendix D (EOS detail):** "One detail that was crucial to optimizing CIDEr… was to include the EOS tag as a word. When the EOS word was omitted, trivial sentence fragments such as 'with a' and 'and a' were dominating the metric gains." [read] — [SCST arXiv v2, App. D](https://arxiv.org/abs/1612.00563)
- **SPIDEr definition:** "We therefore combined SPICE with the CIDEr metric… a combination we call SPIDEr… Based on initial experiments, we decided to use an equal weighting for both." In other words, R = 0.5·SPICE + 0.5·CIDEr. Their BCMR baseline reward is 0.5·BLEU-1 + 0.5·BLEU-2 + 1.0·BLEU-3 + 1.0·BLEU-4 + 1.0·CIDEr + 5.0·METEOR + 2.0·ROUGE. [read] — [Liu et al., "Improved Image Captioning via Policy Gradient optimization of SPIDEr", arXiv:1612.00370 (ICCV 2017), §3.2](https://arxiv.org/abs/1612.00370)
- **SPICE-only failure:** "just optimizing SPICE tended to result in captions which are very detailed, but which often had many repeated phrases… SPICE… does not pay attention to syntactical factors (modulo the requirement that the generated sentence be parseable)." In §4.3: "PG-SPICE tends to generate ungrammatical sentences, with a lot of repeated phrases… We therefore ignore pure SPICE in the rest of this paper." [read] — [SPIDEr §3.2, §4.3](https://arxiv.org/abs/1612.00370)
- **Example PG-SPICE outputs (Table 2):** "a red double decker bus on a city street on a street with a bus on the street with a bus on the street in front of a bus on". The PG-SPIDEr output for the same image is "a red fire truck is on a city street." Another PG-SPICE example: "a man sitting in front of a book and a laptop on a table with a laptop computer on top of a table with a…". [read] — [SPIDEr Table 2](https://arxiv.org/abs/1612.00370)
- **SPIDEr Table 1** (COCO C-5 official test server, Nov 2016; values on a 0–1 scale, no SPICE column). CIDEr-D / METEOR / ROUGE-L / BLEU-4: MLE 0.947 / 0.251 / 0.531 / 0.294 · PG-BLEU-4 0.966 / 0.249 / 0.550 / **0.346** · PG-CIDEr 0.995 / 0.249 / 0.548 / 0.333 · PG-BCMR **1.013** / 0.257 / 0.55 / 0.332 · PG-SPIDEr 1.000 / 0.251 / 0.544 / 0.322. [read] — [SPIDEr Table 1](https://arxiv.org/abs/1612.00370)
- **SPIDEr human evaluation** (492 COCO test images, 3 raters, 4-point scale, "not bad" = okay/good/excellent). Ground truth is 87% "not bad"; MLE is 38%. All PG methods beat MLE significantly. "PG-SPIDEr outperforms PG-BCMR by a 4% margin, despite the fact that PG-BCMR outperforms PG-SPIDEr on all the COCO metrics." [read] — [SPIDEr §4.3, Fig. 3, Table 3](https://arxiv.org/abs/1612.00370)
- SPIDEr uses Monte-Carlo rollouts for a per-step value (PG-Rollout) rather than a greedy baseline, and calls MIXER "unstable" ("we had to try the method 10 times"). [read] — [SPIDEr §4.4](https://arxiv.org/abs/1612.00370)

### Inferences
- The thesis observation that GRPO+METEOR ≈ GRPO+CIDEr-D < GRPO+SPICE ≈ GRPO+ROUGE-L on exec matches the classic SCST finding that METEOR is a bad standalone reward (in SCST, METEOR drops CIDEr 90.9 → 80.5). That precedent can be cited.
- SPIDEr is the direct published precedent for "keep SPICE, but pair it with a fluency- or surface-sensitive metric." Using SPICE + chrF (or SPICE + ROUGE-L) instead of SPICE + CIDEr can be presented as "SPIDEr with the CIDEr term swapped for a metric that behaves well on single, short references." The weighting precedent is equal weights (0.5/0.5), chosen from "initial experiments", not tuned.
- The SPICE-only failure mode in SPIDEr (long, repetitive outputs that add tuples) shows up with **multiple, rich references** on COCO. With ~7-word single references and a length penalty already in the thesis reward, the risk is smaller, but the mechanism (recall over tuples rewards extra objects/attributes) still applies. Monitoring output length and repeated n-grams is justified.

### Gaps
- The SPIDEr paper does not report SPICE numbers for PG-SPICE vs PG-SPIDEr in a table (Table 1 has no SPICE column), so there is no quantitative "SPICE-only vs SPIDEr" comparison on SPICE itself.
- I did not open the CVF camera-ready copies (HTTP 403). The arXiv v2 texts were used, and the SPIDEr arXiv PDF still carries an "Under review… ICCV 2017" header. Table numbering may differ slightly in the camera-ready versions.

---

## 2. Mixing metrics and non-n-gram rewards: discriminability, CLIP-S, learned and semantic rewards, chrF in MT

### Takeaway
Adding a second term to an n-gram reward helps when the second term carries **information the reference metric lacks** (discriminability, image-text alignment), but only at a **small weight**. At large weights fluency collapses (CLIP-S alone gives BLEU-4 6.2 and a CIDEr of 11.2). In MT RL, sentence-level **chrF/chrF++ is repeatedly reported as a smoother, more effective reward than BLEU**, which matches the thesis's offline screen.

### Cited Findings
- **Discriminability (Luo et al., CVPR 2018).** R(ĉ, I) = CIDEr(ĉ) − λ·L_CON(ĉ, I), where L_CON is a contrastive image-caption retrieval loss from a separately trained retrieval model. The update uses the SCST greedy baseline (Eq. 10–11). Text: "For small λ, the solutions seemed stuck in a local minimum; but increasing λ would abruptly make output less fluent"; "the discriminability loss appears to 'cooperate' better with CIDEr than with log-likelihood." [read] — [Luo, Price, Cohen, Shakhnarovich, arXiv:1803.04376 (CVPR 2018), §4](https://arxiv.org/abs/1803.04376)
- **Luo et al. 2018 results** (COCO val, ATTN model). CIDEr / SPICE / retrieval Acc: ATTN+CIDEr 1.1332 / 0.2083 / 71.05% · **ATTN+CIDEr+DISC(λ=1) 1.1406 / 0.2113 / 75.74%** · DISC(5) 1.1026 / 0.2097 / 80.98% · DISC(10) 1.0552 / 0.2070 / 83.69%. A small λ improves CIDEr and SPICE over CIDEr-only; larger λ trades n-gram scores for discriminability. A separately trained retrieval model ("Acc-new") gives almost the same accuracy as the one used in training, so they report no overfitting to the reward model. [read] — [Luo et al. 2018, table on p. 7 and §5](https://arxiv.org/abs/1803.04376)
- **CLIP-S reward (Cho et al., Findings of NAACL 2022).** Reward R(I, c) = CLIP-S(I, c), trained with a greedy-baseline SCST variant ("the reward of the beam search is normalized with the baseline reward b from greedy"). Because "the CLIP-S reward often generates grammatically incorrect captions (e.g., repeated words)", they fine-tune the CLIP text encoder with a grammar head on negatives made by randomly repeating, inserting or swapping words. The final reward is **R(I, c) = λ·CLIP-S(I, c) + g(c), λ = 2**. [read] — [Cho et al., arXiv:2205.13115, §3](https://arxiv.org/abs/2205.13115)
- **Cho et al. Table 2** (COCO Karpathy test). BLEU-4 / CIDEr / METEOR / ROUGE-L / BERT-S / CLIP-S: MLE 32.5 / 110.3 / 27.2 / 55.2 / 0.937 / 0.758 · CIDEr reward 38.2 / 124.9 / 28.7 / 58.5 / 0.942 / 0.759 · **CLIP-S 6.2 / 11.2 / 18.7 / 31.6 / 0.882 / 0.860** · CIDEr+CLIP-S 37.7 / 124.6 / 28.8 / 58.3 / 0.941 / 0.772 · CLIP-S+Grammar 16.9 / 71.0 / 24.9 / 47.3 / 0.924 / 0.793. A degenerate CLIP-S caption looks like "…outside a terminal window motion position area motionn". [read] — [Cho et al. 2022, Tables 2–3](https://arxiv.org/abs/2205.13115)
- **Semantic-similarity reward in NMT (Wieting et al., ACL 2019, pp. 4344–4355).** The authors argue BLEU "gives no partial credit", has a limited output range and penalises semantically correct paraphrases. A semantic-similarity reward improves BLEU, semantic similarity and human judgments, and "converges faster", which they attribute to partial credit and more varied scores. [read: abstract page only] — [Wieting, Berg-Kirkpatrick, Gimpel, Neubig, ACL 2019](https://aclanthology.org/P19-1427/)
- **chrF++ vs BLEU as a GRPO-style reward in MT (preprint, arXiv 2601.12535, round-trip RL with NLLB).** Their ablation compares BLEU+chrF++ (uniform), BLEU only, and chrF++ only. BLEU gives "a weaker learning signal under sparse n-gram matching"; chrF++ "provides a smoother character-level similarity objective" and is "best in 4/6 conditions". "Adding BLEU to chrF++ is competitive and occasionally beneficial… but does not uniformly outperform chrF++ alone." The paper claims "chrF++ is a more effective training signal than BLEU or learned metrics" (BLEURT tried). [read] — [Attia & Fikri, arXiv:2601.12535 (preprint)](https://arxiv.org/abs/2601.12535)
- Other 2026 MT RL preprints reportedly keep chrF++ after a validation comparison with BLEU (speech translation GRPO), or use a 50/50 chrF++ + MetricX reward (Omnilingual MT). [snippet] — [arXiv:2609.26536](https://arxiv.org/pdf/2609.26536); [arXiv:2603.16309](https://arxiv.org/pdf/2603.16309)
- **Transfer reward learning** replaces n-gram overlap rewards with learned sentence-similarity rewards for captioning and reports gains on semantic-similarity metrics. [snippet, preprint] — [arXiv:1909.03622](https://arxiv.org/html/1909.03622)
- **Learned discriminative metric (Cui et al., CVPR 2018, "Learning to Evaluate Image Captioning").** This work trains a critic that tells human captions from machine captions as a metric. [memory: content not re-read here] — [CVPR 2018 open access](https://openaccess.thecvf.com/content_cvpr_2018/html/Cui_Learning_to_Evaluate_CVPR_2018_paper.html)

### Inferences
- The pattern across Luo 2018 and Cho 2022 is that **the reference-based n-gram term acts as the fluency anchor**. Non-reference terms help only at small weight (Luo: λ = 1 helps and λ = 10 hurts CIDEr; Cho: CLIP-S alone destroys fluency). For the thesis, this argues for SPICE (or SPICE + chrF) as the anchor and any "listener/grounder" term as a small additive bonus, not the other way round.
- Luo's "Acc-new" control (a separately trained discriminator scores about the same as the training discriminator) is the template for guarding against Goodhart if a grounder term enters the reward: **use one grounder in the reward and a different one (UGround) for evaluation.**
- The MT evidence (chrF++ smoother than BLEU under sparse n-gram matching; Wieting's partial credit and score-variance argument) gives a literature-backed mechanism for the thesis's offline finding that chrF ranks exec-correct samples best (0.794). Short single references make word n-gram and scene-graph tuple matching sparse, and character n-grams restore partial credit and within-group variance.

### Gaps
- I found no peer-reviewed captioning paper that uses **chrF** as an RL reward. The chrF-as-reward evidence is MT-only, and mostly 2025–2026 preprints.
- I did not verify Cui et al. 2018's RL results, if any, or the exact Wieting SimiLe formula (the length-penalty exponent was not visible on the abstract page).
- No source found that trains with a **BERTScore** reward for captioning together with reported numbers. Not searched exhaustively.

---

## 3. Reward-hacking patterns with n-gram / scene-graph / embedding rewards, and documented remedies

### Takeaway
The documented hacks are: (i) **bad endings** ("with a", "on a") under CIDEr/BLEU; (ii) **repeated phrases and over-long captions** under SPICE-only; (iii) **word salad and repetition** under CLIP-S; (iv) **verbosity or brevity** under LVLM-judge rewards. The documented remedies are: count EOS as a word, mix in a fluency-sensitive reference metric (SPIDEr), add a grammar critic, n-gram constraints on sampling, a KL anchor, and length handling in the loss.

### Cited Findings
- **Bad endings (Guo et al., EMNLP 2018):** "46.44% generated captions end with phrases as 'with a', 'on a', 'of a', etc." on COCO val under a self-critical baseline. "removing these endings results in a huge performance drop of around 6%", so the endings were earning reward. Their remedy, an n-gram language-model constraint on the action space plus prioritised sampling (update on the best of several samples), "prevent[s] the appearance of bad endings and expedite[s] the convergence while maintaining comparable performance". They report about 2× faster convergence. [read] — ["Improving Reinforcement Learning Based Image Captioning with Natural Language Prior", arXiv:1809.06227 (EMNLP 2018 per arXiv comment)](https://arxiv.org/abs/1809.06227)
- **EOS as a word** is what keeps CIDEr optimisation from rewarding "with a"/"and a" fragments (SCST App. D, quoted in §1). [read] — [SCST](https://arxiv.org/abs/1612.00563)
- **SPICE-only produces repeated phrases and ungrammatical, over-long captions**, and pairing with CIDEr fixes it (SPIDEr §3.2, §4.3, quoted in §1). [read] — [SPIDEr](https://arxiv.org/abs/1612.00370)
- **CLIP-S produces repetition and degenerate tokens**; the remedy is a learned grammar term g(c) added to the reward (Cho et al., quoted in §2). [read] — [Cho et al. 2022](https://arxiv.org/abs/2205.13115)
- **LVLM-as-judge rewards get hacked**: in CapRL Fig. 1, judges "suffer from limitations like rewarding verbosity or brevity, leading to low-quality captions and reward hacking". The figure annotates a judge reward "rapidly hacked" (training collapse; the model outputs only "description"). [read] — [CapRL, arXiv:2509.22647 (preprint), Fig. 1](https://arxiv.org/abs/2509.22647)
- **Discriminability term**: increasing λ "would abruptly make output less fluent" (Luo et al. 2018 §4.2). [read] — [Luo et al. 2018](https://arxiv.org/abs/1803.04376)
- **GRPO length bias**: the per-response length normalisation and std normalisation in GRPO introduce an optimisation bias that "artificially increases response length (especially for incorrect outputs)". Dr. GRPO removes both terms. [snippet + abstract; venue (COLM 2025) not verified] — [Liu et al., "Understanding R1-Zero-Like Training: A Critical Perspective", arXiv:2503.20783](https://arxiv.org/abs/2503.20783)
- **KL to a reference model** is a GRPO default. The GRPO-for-captioning preprint argues SCST "does not use KL divergence as a constraint, so it is prone to mode collapse". [read] — [Liang, arXiv:2503.01333 (preprint)](https://arxiv.org/abs/2503.01333)

### Inferences
- For ~7-word single references, the hacks most likely to matter are length growth (SPICE recall rewards extra tuples) and generic tails. The thesis's −0.02·length penalty and β = 0.04 KL are standard remedies. **Check the EOS/termination handling of the SPICE computation**: SPICE parses the sentence, so EOS is not a token there, unlike CIDEr. Truncated outputs could still score well if the parser recovers tuples.
- A plausible reason the thesis's CIDEr-D reward lowered test CIDEr-D: CIDEr-D's IDF and Gaussian length term were designed for 5 references per image. With one short reference, the reward is sparse and dominated by rare n-grams, and the "bad ending / EOS" effect may be active if EOS is not counted. This is a hypothesis to test by inspecting train-time CIDEr curves and output tails, not a literature finding.

### Gaps
- No source found that reports reward hacking specifically for **ROUGE-L or chrF rewards** in captioning (character n-gram rewards could plausibly reward partial-word fragments; not documented).
- The Dr. GRPO venue was not confirmed in this session.

---

## 4. GRPO / R1-style RL for captioning, REG and instruction generation, 2024–2026

### Takeaway
Published GRPO captioning work is thin and mostly preprint. The one direct "GRPO with a CIDEr reward" captioning paper (arXiv-only) reports GRPO > SCST by +2.4 CIDEr with a small model. The strongest 2025 LVLM captioning RL work (CapRL, preprint) **abandons reference metrics** for a **utility reward**: a text-only LLM answers MCQs from the caption. That is conceptually the same as the thesis's exec, with a grounder as the "reader".

### Cited Findings
- **GRPO for image captioning (Liang, arXiv:2503.01333, March 2025, preprint, no venue).** Reward = CIDEr. Advantage A_i = (r_i − mean(r)) / std(r); clipped ratio + β·KL to the reference model; G = 5 samples; GRPO trained 5 epochs vs SCST 20 epochs. **Table 1, COCO Karpathy test** (B4 / METEOR / ROUGE-L / CIDEr / SPICE): CE 26.8 / 23.7 / 50.5 / 84.3 / 16.4 · +SCST 30.5 / 23.8 / 52.5 / 97.6 / 16.4 · **+GRPO 31.4 / 24.4 / 53.2 / 100.0 / 17.1**. **Flickr8k**: SCST 36.6 CIDEr, 10.6 SPICE vs GRPO 38.3, 11.1. A small ResNet50 + 1-layer Transformer, single run, no variance reported. [read] — [arXiv:2503.01333](https://arxiv.org/abs/2503.01333)
- **CapRL (Xing et al., arXiv:2509.22647, Sept 2025, preprint).** The reward is the accuracy of a separate vision-free LLM answering multiple-choice questions from the caption alone ("1, if correct; 0, otherwise"; options shuffled and averaged). It is applied to Qwen2.5-VL-3B. The motivation given is that LVLM-as-judge rewards are hacked (verbosity or brevity bias). Reported: CapRL-3B is "comparable to Qwen2.5-VL-72B" in the Prism caption-quality framework and +8.4% average over the baseline. [read: abstract + Fig. 1] — [arXiv:2509.22647](https://arxiv.org/abs/2509.22647)
- **Pinto et al., "Tuning computer vision models with task rewards"** (ICML 2023 [memory]; arXiv v1 shows no venue). Captioning is tuned with REINFORCE on CIDEr computed on train-set statistics, using **"7 other samples to estimate the reward baseline"** (a leave-one-out group baseline, the same family as GRPO's group mean). [read] — [arXiv:2302.08242](https://arxiv.org/abs/2302.08242)
- **Leave-one-out baseline beats the greedy baseline (Luo, "A Better Variant of SCST", arXiv:2003.09971, preprint).** b_k = (1/(K−1))·Σ_{j≠k} R(ĉ_j) with K = 5. "our variant is better than SCST on all architectures, especially on Transformer", and the gap is consistent across seeds and longer training. [read] — [arXiv:2003.09971](https://arxiv.org/abs/2003.09971)
- **CycleGRPO** (arXiv:2607.11581, preprint) couples captioning with grounding under GRPO and reports +6.5 CIDEr, +1.1 METEOR on val over a SAMTok baseline. It notes that rewards usually rely on reference text (CIDEr) or costly LLM judges. **VCap** (arXiv:2605.28023, preprint) uses GRPO with a "hypergeometric" sentence-level reward against a reference caption. [snippet: not verified] — [CycleGRPO](https://arxiv.org/html/2607.11581); [VCap](https://arxiv.org/pdf/2605.28023)
- **TGRPO-SRM** (IEEE BigData 2025 per the listing): token-aware GRPO with semantic reward modelling for referring-expression grounding and generation. [snippet: abstract only] — [ResearchGate listing](https://www.researchgate.net/publication/401687078_TGRPO-SRM_Token-Aware_GRPO_with_Semantic_Reward_Modeling_for_Referring_Expression_Grounding)

### Inferences
- The thesis's setup (GRPO with G = 8, a metric reward, KL to SFT) is in line with the only direct GRPO-captioning precedent (Liang 2025: G = 5, CIDEr reward, KL). The thesis's comparison of SCST+SPICE vs GRPO+SPICE (60.54 vs 60.65 exec) matches the size of that paper's GRPO-over-SCST gain on text metrics, i.e. small.
- CapRL and the CycleGRPO note show that the 2025–2026 trend for LVLM captioning is **utility or verifiable rewards** (a reader model must succeed) rather than n-gram rewards. For a thesis that must keep SPICE at the core, the defensible framing is "SPICE as the reference-anchored reward, with optional utility bonus", following Luo 2018's discriminability recipe.

### Gaps
- I found **no peer-reviewed GRPO paper on referring-expression generation or GUI/instruction generation** with a reference-metric reward. TGRPO-SRM's reward design could not be checked.
- I did not verify whether CapRL was later accepted at a venue.

---

## 5. Softening SPICE: partial credit, synonyms, embeddings, very short references

### Takeaway
SPICE already gives synonym credit through WordNet, but it is otherwise **exact tuple F1**. Embedding-softened variants exist mainly in audio captioning (SPICE+). I found **no paper that uses a softened SPICE as an RL reward**, and no published fix for SPICE on very short references.

### Cited Findings
- SPICE computes F1 between candidate and reference scene-graph tuples (objects, attributes, relations), with WordNet-synonym matching. [snippet summary of the SPICE definition; original: Anderson et al., ECCV 2016] — [SPICE (Springer, ECCV 2016)](https://link.springer.com/doi/10.1007/978-3-319-46454-1_24); [arXiv:1607.08822](https://arxiv.org/abs/1607.08822)
- **SPICE+** (audio captioning): parses captions into semantic graphs with a deep dependency model plus refined rules, then compares **sentence embeddings of candidate and reference semantic elements** instead of exact matches. [snippet; venue not verified] — [SPICE+ (HAL)](https://hal.univ-lorraine.fr/LORIA-NLPKD/hal-03933981v1)
- An "intrinsic" captioning metric is motivated by hard token matching missing "semantic diverse but similar expressions". [snippet, preprint] — [arXiv:2012.07333](https://arxiv.org/pdf/2012.07333)
- SPIDEr's analysis that SPICE ignores syntax "modulo the requirement that the generated sentence be parseable" (§1 above) implies SPICE is blind to surface form beyond the parse. [read] — [SPIDEr §3.2](https://arxiv.org/abs/1612.00370)

### Inferences
- With K_gold ∈ {0, …, 3} tuples, SPICE-F1 can take only a handful of distinct values per prompt. For example, with K_gold = 2 and candidate tuple counts of 1–4, the possible F1 values are {0, 0.33, 0.4, 0.5, 0.67, 0.8, 1}. Many samples in a group of 8 will therefore tie exactly, which gives zero advantage under GRPO std normalisation. This is the arithmetic behind the zero-variance groups the thesis observed, and it is the main argument for adding a dense partner term (chrF) or a tie-break rather than rescaling SPICE.
- A "soft SPICE" (embedding similarity between tuple elements, à la SPICE+) would add partial credit, but it has no RL precedent, costs engineering time, and still yields zero tuples on many GUI references (K_gold = 0). For K_gold = 0 no tuple-based metric can provide signal. That is why the SA-SPICE-v3 design shifts weight to chrF (α ∝ K_gold/3), and the literature offers nothing better for this case.

### Gaps
- No source on SPICE behaviour with **single, very short references**, and no source on a "soft SPICE" RL reward.
- I did not re-open the SPICE ECCV paper to quote its tuple and synonym definitions verbatim.

---

## 6. Rank-based or relative rewards (group rank, pairwise wins) and zero-variance groups

### Takeaway
Captioning RL has used **relative baselines** (greedy in SCST, leave-one-out mean in Luo 2020 and Pinto 2023, group z-score in GRPO), and the leave-one-out and group baselines beat the greedy baseline. I found **no captioning paper that uses pure rank-based advantages**. General-RL preprints propose rank advantages (GOPO), and the LLM-RL literature handles zero-variance groups by filtering them (DAPO) or by removing std normalisation (Dr. GRPO).

### Cited Findings
- **Leave-one-out mean baseline > greedy baseline** for captioning (Luo 2020, quoted in §4). [read] — [arXiv:2003.09971](https://arxiv.org/abs/2003.09971)
- **GOPO** (arXiv:2602.03876, preprint) replaces reward magnitudes with an ordering-based advantage. It reports that rank-based advantages "typically increase the norm of policy gradient update, especially for small group sizes". [snippet] — [arXiv:2602.03876](https://arxiv.org/pdf/2602.03876)
- **Dr. GRPO** drops the std division (and length normalisation), arguing that the std term creates a question-level difficulty bias. Groups with low reward std get over-weighted. [snippet + abstract] — [arXiv:2503.20783](https://arxiv.org/abs/2503.20783)
- **DAPO dynamic sampling**: over-sample and filter out prompts whose group rewards are all identical (zero advantage). [memory; the search snippet only confirms "DAPO excludes groups where [std] equals zero"] — [DAPO, arXiv:2503.14476](https://arxiv.org/abs/2503.14476); [summary](https://aiweekly.co/alerts/new-paper-unifies-grpo-dr-grpo-dapo-under-group-std-dev-dial)
- **Prioritised sampling** (update on the best-rewarded of several samples) sped up captioning RL about 2× and helped remove bad endings (Guo et al. 2018, §3). [read] — [arXiv:1809.06227](https://arxiv.org/abs/1809.06227)

### Inferences
- For SPICE with heavy ties, a **lexicographic rank** (rank by SPICE, break ties by chrF, then convert ranks to centred advantages) keeps "the reward is SPICE" literally true: chrF only orders samples SPICE cannot separate. In practice this approximates R = SPICE + ε·chrF with ε → 0. There is no direct precedent, so it should be framed as an engineering choice motivated by GRPO's zero-advantage groups (DAPO/Dr. GRPO).
- Filtering zero-variance groups (DAPO-style) does not change the reward definition. It only stops wasting updates, and it is the cheapest defensible change if SA-SPICE-v3 underperforms.

### Gaps
- No captioning or REG paper found that compares rank-based vs raw-metric advantages empirically.

---

## 7. Implications for a SPICE-centered GRPO reward for short GUI instructions (ranked candidates)

### Takeaway
The literature supports **"SPICE plus a dense, fluency- and surface-sensitive partner"** (SPIDEr precedent) far more than **"SPICE alone"** (SPIDEr dropped it) or **"heavily composite rewards"** (SCST could not beat CIDEr-only with multi-metric rewards; Luo and Cho show large auxiliary weights hurt). For one short reference, the best-motivated partner is **chrF** (MT RL evidence plus the thesis's own concordance screen), with SPICE kept as the named, primary term.

### Cited Findings
- SCST: multi-metric rewards could not beat the CIDEr-only model overall, and METEOR reward lowered CIDEr from 90.9 to 80.5 (SCST Table 3). [read] — [SCST](https://arxiv.org/abs/1612.00563)
- SPIDEr: SPICE-only gives repetitive and ungrammatical output, and 0.5·SPICE + 0.5·CIDEr wins human evaluation (+4 points over BCMR despite lower COCO metrics). [read] — [SPIDEr](https://arxiv.org/abs/1612.00370)
- An auxiliary reward helps at small weight and hurts at large weight (Luo 2018: λ = 1 raises CIDEr 1.133 → 1.141 and SPICE 0.208 → 0.211; λ = 10 drops CIDEr to 1.055). CLIP-S alone collapses BLEU-4 to 6.2. [read] — [Luo 2018](https://arxiv.org/abs/1803.04376); [Cho 2022](https://arxiv.org/abs/2205.13115)
- chrF++ is smoother and more effective than BLEU as an RL reward under sparse n-gram matching (MT, preprint). [read] — [arXiv:2601.12535](https://arxiv.org/abs/2601.12535)

### Inferences (ranked candidates; the numbers in brackets are the thesis's own offline concordance values given in the task, not literature)
1. **SPICE-anchored SPIDEr-chrF with a tie-break floor.** R = SPICE + w·chrF − 0.02·len, with w ∈ {0.25, 0.5, 1.0} chosen on DEV (w = 1 corresponds to SPIDEr's equal weighting). Precedent: SPIDEr (equal-weight SPICE + n-gram partner), Luo 2018 (small auxiliary weight is safe). It is simpler than SA-SPICE-v3 (no K_gold-dependent α, no ActionMatch term, no clipping) and easier to defend ("SPIDEr with chrF because there is one short reference"). Expected effect: it removes most zero-variance groups and inherits chrF's best-in-screen ordering (0.794) while keeping SPICE as the named core.
2. **Lexicographic or tie-break reward: R = SPICE + ε·chrF (ε ≈ 0.05–0.1), or rank-based advantages with chrF only as tie-breaker.** This is the strongest "the reward is still SPICE" claim, since chrF changes only the ordering among SPICE-tied samples. Precedent is indirect: GRPO zero-variance handling (DAPO/Dr. GRPO) and GOPO rank advantages (preprint). This is the most conservative option if the thesis must report "GRPO + SPICE" verbatim.
3. **Keep the SPICE reward and add DAPO-style dynamic sampling** (drop groups whose 8 SPICE values are identical; resample prompts). The reward is unchanged, and it directly targets the sparsity and tie failure. It can be combined with option 1 or 2.
4. **SPICE + small listener/grounder bonus** (Luo 2018 discriminability recipe; CapRL utility reward): R = SPICE + w·chrF + λ·hit(grounder_B), with λ small, and **grounder_B ≠ UGround** (a separate model, following Luo's Acc-new control) to avoid Goodhart on the exec evaluator. Highest expected gain on exec, but the highest risk: evaluator leakage, extra GPU cost, and fluency loss at large λ.
5. **SA-SPICE-v3 as is** (clip(0.8·[α·SPICE + (1−α)·chrF] + 0.2·ActionMatch − len), α = 0.8·min(1, K_gold/3)). The idea is defensible (it degrades gracefully to chrF when there are no tuples), but its many hand-set constants (0.8, 0.2, /3, clipping) have no single literature precedent. SCST's warning that multi-metric rewards did not beat the best single metric applies, and the offline concordance is already below chrF alone (0.771 vs 0.794). If it underperforms, fall back to option 1 or 2 rather than tuning its constants.
- **Not recommended:** a CIDEr-D reward on single short references (SCST-style CIDEr assumes 5 references and needs EOS handling, and the thesis's CIDEr-D reward lowered CIDEr-D); METEOR as the reward (SCST Table 3 precedent of harming other metrics); CLIP-style rewards (screenshot text is unreadable at 224 px, and Cho shows fluency collapse); LVLM-judge rewards (CapRL documents rapid hacking).
- **Monitoring that the literature says to report alongside any of these:** mean output length, the rate of repeated n-grams and generic tails, the fraction of zero-variance groups per step, and, for option 4, exec under a grounder not used in training.

### Gaps
- No direct precedent exists for a SPICE + chrF reward, for rank or tie-break rewards in captioning, or for metric-reward RL on GUI instructions. Every ranking above is an inference from adjacent evidence and must be validated on the thesis's DEV split.
