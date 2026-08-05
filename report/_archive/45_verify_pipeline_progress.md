# TIẾN ĐỘ KIỂM ĐỊNH PIPELINE (deep-research lần cuối) — LƯU ĐỂ CHẠY TIẾP

> 📒 **Chỉ mục tổng mọi đợt research ở `report/RESEARCH_LEDGER.md`** (đọc trước để biết cái gì đã chạy / chưa chạy). File này = đợt **R-07** trong sổ đó.

> **Mục đích file này:** lưu lại **toàn bộ những gì workflow deep-research đã làm được** (trước khi bị dừng)
> để **lần sau chỉ chạy phần còn lại**, khỏi làm lại từ đầu. Ngày lưu: 2026-07-05.
>
> **Cho agent phiên sau:** đọc file này trước. PHẦN A = trạng thái + đọc-sơ-bộ + việc-còn-lại + cách-resume.
> PHẦN B = dữ liệu thô đã thu (scope + 29 URL + 24 nguồn kèm claim). Các claim ở PHẦN B **đã trích nhưng CHƯA
> qua vòng phản-bác 3-phiếu** — đó chính là việc còn lại.

---

## PHẦN A — TRẠNG THÁI & ĐIỀU HÀNH

### A.1. Metadata run
- **Workflow:** `deep-research` (bản đầy đủ: Scope → Search → Fetch → Verify → Synthesize).
- **Run ID:** `wf_9284d315-f7c` · **Task ID (đã stop):** `wat84mlez`.
- **Transcript dir:** `…/subagents/workflows/wf_9284d315-f7c/` (journal.jsonl + agent-*.jsonl còn nguyên).
- **Câu hỏi:** kiểm định đối kháng (fact-check + phản-bác) phần PIPELINE của luận văn + xác minh venue/năm các citation nền tảng.

### A.2. Đã chạy xong (KHÔNG cần chạy lại)
| Giai đoạn | Trạng thái | Kết quả |
|---|---|---|
| **Scope** (phân rã 5 góc) | ✅ xong | 5 góc — xem B.1 |
| **Search** (5 tìm kiếm song song) | ✅ xong | 29 URL — xem B.2 |
| **Fetch + Extract claim** (24 nguồn) | ✅ xong | 24 nguồn kèm claim + chất-lượng + ngày — xem B.3 |

### A.3. CHƯA chạy (việc còn lại cho lần sau)
| Giai đoạn | Trạng thái | Cần làm |
|---|---|---|
| **Verify** (phản-bác 3-phiếu mỗi claim) | ⏳ chưa | với mỗi claim ở B.3, chạy 3 agent skeptic thử BÁC; giữ claim nếu <2/3 bác |
| **Synthesize** (tổng hợp có trích dẫn) | ⏳ chưa | gộp claim sống + xếp theo độ tin + viết phán quyết cuối |

### A.4. Cách CHẠY TIẾP (2 lựa chọn)
1. **Resume tự động (rẻ nhất):** gọi lại workflow `deep-research` với `resumeFromRunId: "wf_9284d315-f7c"` — các agent Fetch đã xong sẽ **replay từ cache**, chỉ Verify + Synthesize chạy mới. *(Điều kiện: cùng phiên hoặc cache còn; nếu cache mất thì dùng cách 2.)*
2. **Chạy Verify thủ công trên dữ liệu file này:** đưa PHẦN B cho một workflow nhỏ, mỗi claim "central/high" → 3 agent skeptic (schema verdict SUPPORTED/REFUTED/UNCERTAIN) → tổng hợp. Đây chính là "chạy verify với mấy cái còn lại" mà không cần fetch lại 24 nguồn.

### A.5. ĐỌC SƠ BỘ (từ claim đã trích — mạnh nhưng CHƯA qua 3-phiếu, coi như *chỉ dấu*)

> ✅ **CẬP NHẬT: §A.5/A.6 dưới đây là ảnh-chụp-lúc-dừng. Verify+Synthesize ĐÃ CHẠY XONG → xem `§C` (phán quyết chính thức).** Hai mục ⚠/🔴 dưới đã GIẢI QUYẾT: **TOMATO = ICLR 2025 Poster (xác nhận, hết ⚠)**; **số "~2%" đã sửa** trong report/43 §4.5 ("~38%→~18% với CoT"). Đừng hành động theo §A.5/A.6 nữa — dùng §C.

**✅ Citation ĐÃ được nguồn sơ cấp xác nhận đúng venue/năm (rất yên tâm):**
- FaithScore — **Findings EMNLP 2024** ✓ (nguồn 16)
- Chain-of-Verification / CoVe — **Findings ACL 2024** ✓ (nguồn 17)
- RARR — **ACL 2023** ✓ (nguồn 15)
- Huang "LLMs Cannot Self-Correct Reasoning Yet" — **ICLR 2024** ✓ (nguồn 12, 21)
- ALOHa — **NAACL 2024 (Short)** ✓ (nguồn 20)
- Qin — pairwise ranking prompting — **Findings NAACL 2024** ✓ (nguồn 8)
- "Do GUI Grounders Truly Understand UI Elements?" — **Findings EACL 2026** ✓ (nguồn 22)
- AskEase "From Struggle to Success" — **CHI 2026**, DOI 10.1145/3772318.3790661 ✓ (nguồn 24)

**⚠️ Citation CẦN TỰ VERIFY LẠI TRƯỚC KHI IN:**
- **TOMATO "(ICLR 2025)"** — nguồn 14 cảnh báo: trang arXiv 2410.23266 **không xác nhận** proceedings ICLR 2025 trên abstract. Nguồn 5 & 10 coi là ICLR 2025 nhưng chưa chắc. → **kiểm OpenReview `id=fCi4o83Mfs` trước khi trích "ICLR 2025"**; nếu không chắc thì ghi "preprint 2024/2025".
- *(Bù)* **GVL — Generative Value Learning (ICLR 2025, Google DeepMind)** là trụ **peer-reviewed chắc** cho ý "xáo trộn frame → suy lại thứ tự là hướng VLM khả thi" (nguồn 10) — có thể dùng thay/bổ trợ cho Stage-0.

**🔴 CLAIM CẦN SỬA TRONG `report/43`:**
- Con số **"~2%"** ở **§4.5** (grounded-gen làm ảo giác còn ~2%) **KHÔNG được nguồn ủng hộ** (nguồn 2 và 3 nói thẳng). Nguồn 3 (sơ cấp): mức giảm mạnh nhất quan sát được là CoT hạ ảo giác **38,3% → 18,1%**, *không phải ~2%*. → **Phải bỏ/sửa số "~2%"** trong §4.5: đổi thành "sụt **mạnh**" (định tính) HOẶC trích đúng "còn ~18% với CoT prompting" từ nguồn sơ cấp. Luận điểm (grounded-gen làm hỏng phép đo) **vẫn đúng** — chỉ con số cụ thể là sai.

**✅ Các khẳng định pipeline được chỉ-dấu ỦNG HỘ (chờ 3-phiếu chốt):**
- Post-hoc verification **vẫn chính danh** 2024–2026, **không** bị grounded-gen thay thế — nó *xếp lớp/hybrid* cùng grounded-gen (nguồn 1,3,4,6,15,17,20). *Sắc thái mới:* 2026 khuyến nghị **hybrid** (prompt + retrieval + post-hoc), không phải "post-hoc thay grounded". → nên phản ánh sắc thái này vào §4.5 (ta không chống grounded-gen, ta xếp lớp).
- Self-correction bằng **tín hiệu NGOÀI** hợp lệ; chỉ **tự-sửa NỘI TẠI** bị bác (Huang ICLR24) — phân định của ta ĐÚNG (nguồn 12,13,18,19,21).
- VLM **yếu suy luận thứ tự / "bag-of-frames"** → module sắp-thứ-tự KHÔNG thừa (nguồn 5,7,10,14; GPT-4o ~24% vs người ~80%).
- **Pairwise > listwise** (Qin PRP: hơn >10% chỉ số xếp hạng) (nguồn 8).
- **min-FAS** là công thức chuẩn cho rank-aggregation từ so-cặp, NP-complete → cần heuristic/trọng-số (nguồn 9) — khớp M2.
- **Describe-don't-guess / abstention** là chiến lược hợp lệ 2024-26; abstention ngây thơ thì quá bảo thủ (nguồn 6,11,23) — khớp caveat của ta.
- **AskEase KHÔNG scoop:** nó *không* hậu-kiểm đối chiếu View Hierarchy, *không* có metric no-gold tự động; grounding bằng RAG-tài-liệu + trạng-thái-live, đánh giá bằng user-study — combo của ta còn trống (nguồn 24).

**🟡 Nguồn phản biện (contrarian) cần đối mặt:**
- Nguồn 2 (blog) & 11 (preprint 2026): khuyến nghị *chủ đạo* nghiêng về grounded/retrieval-augmented; post-hoc bị gọi là "extrinsic, thêm độ trễ". → **Nhưng cả hai đều thừa nhận post-hoc vẫn hiệu quả, không lỗi thời.** Thủ: đóng khung ta = *đo lường* (cần post-hoc) + xếp-lớp, không phải chống grounded.

### A.6. Việc phải làm cho `report/43` (rút ra từ đợt này)
1. **[BẮT BUỘC] Sửa "~2%" ở §4.5** → định tính "sụt mạnh" hoặc trích "≈18% với CoT" (nguồn sơ cấp), bỏ số không có nguồn.
2. **[BẮT BUỘC] Thêm caveat venue cho TOMATO** (ICLR 2025 chưa chắc) — kiểm OpenReview trước khi in.
3. **[NÊN] Bổ sung sắc thái "hybrid" vào §4.5:** nói rõ ta *xếp lớp* post-hoc cùng grounded-gen (đúng khuyến nghị 2026), không đối đầu.
4. **[NÊN] Thêm trụ mới đã xác minh:** CaLM (ACL 2024), CRITIC (ICLR 2024), GVL (ICLR 2025), Tyen et al. (Findings ACL 2024) — đều hậu thuẫn "verify/correct bằng tín hiệu ngoài".

---
## PHẦN B — DỮ LIỆU THÔ ĐÃ THU (evidence, CHƯA qua Verify 3-phiếu)

### B.1. Scope — 5 góc quét (đã chạy)

> Câu hỏi gốc: Kiểm định lần cuối (adversarial, fact-check + phản bác) phần PIPELINE của luận văn thạc sĩ 2026 về sinh hướng dẫn sử dụng phần mềm từng bước từ ảnh UI + câu hỏi (no-gold): xác nhận pipeline vững, đúng-thời 2026, và mọi citation nền tảng là THẬT (đúng venue/năm) — hoặc chỉ ra chỗ sai.

- **citation-verification** — truy vấn: `FaithScore Findings EMNLP 2024 "Chain-of-Verification" CoVe ACL 2024 RARR ALOHa NAACL 2024 venue year verification`
- **contrarian-post-hoc-vs-grounded** — truy vấn: `post-hoc hallucination verification vs grounded generation LLM 2025 2026 which paradigm superior deprecated`
- **self-correction-external-signal** — truy vấn: `Huang "LLMs Cannot Self-Correct Reasoning Yet" ICLR 2024 external feedback vs intrinsic self-correction validity`
- **vlm-temporal-ordering-pairwise** — truy vấn: `VLM image sequence temporal order reasoning bag-of-frames TOMATO ICLR 2025 pairwise ranking prompting Qin NAACL 2024 Copeland feedback arc set`
- **novelty-gui-instruction-abstention** — truy vấn: `GUI software tutorial instruction generation from screenshot for human readers no-gold evaluation AskEase CHI 2026 abstention describe don't guess hallucination`

### B.2. Nguồn tìm được (URL, đã chạy Search)

- [LLM Hallucination: A 2026 Architectural Deep Dive](https://futureagi.com/blog/llm-hallucination-deep-dive-2026/)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Survey and analysis of hallucinations in LLMs: attribution to prompting strategies or model behavior](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1622292/full)
- [CaLM: Contrasting Large and Small Language Models to Verify Grounded Generation](https://arxiv.org/pdf/2406.05365)
- [Do I Really Know? Learning Factual Self-Verification for Hallucination Reduction](https://arxiv.org/pdf/2602.02018)
- [Mitigating LLM Hallucinations through Domain-Grounded Tiered Retrieval](https://arxiv.org/html/2603.17872v1)
- [TOMATO: Assessing Visual Temporal Reasoning Capabilities in Multimodal Foundation Models (ICLR 2025)](https://openreview.net/forum?id=fCi4o83Mfs)
- [Large Language Models are Effective Text Rankers with Pairwise Ranking Prompting — Qin et al. (Findi](https://aclanthology.org/2024.findings-naacl.97/)
- [Beyond Single Frames: Can LMMs Comprehend Temporal and Contextual Narratives in Image Sequences? (20](https://arxiv.org/html/2502.13925v1)
- [Feedback arc set (definitions and algorithms)](https://en.wikipedia.org/wiki/Feedback_arc_set)
- [Generative Value Learning: Vision Language Models are In-Context Value Learners](https://generative-value-learning.github.io/)
- [TOMATO (arXiv full text / ICLR 2025 camera-ready)](https://arxiv.org/pdf/2410.23266)
- [Large Language Models Cannot Self-Correct Reasoning Yet (Huang et al., ICLR 2024)](https://arxiv.org/abs/2310.01798)
- [CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing (Gou et al.)](https://arxiv.org/abs/2305.11738)
- [LLMs Cannot Find Reasoning Errors, but Can Correct Them Given the Error Location (Tyen et al., Findi](https://aclanthology.org/2024.findings-acl.826.pdf)
- [When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey (Kamoi et al., TACL 2024)](https://www.researchgate.net/publication/385650033_When_Can_LLMs_Actually_Correct_Their_Own_Mistakes_A_Critical_Survey_of_Self-Correction_of_LLMs)
- [Self-Correction Bench: The Self-Correction Blind Spot in LLMs (2025)](https://arxiv.org/pdf/2507.02778)
- [Can Large Vision-Language Models Correct Semantic Grounding Errors By Themselves? (Wu et al., 2024)](https://arxiv.org/pdf/2404.06510)
- [FaithScore: Fine-grained Evaluations of Hallucinations in Large Vision-Language Models — Findings of](https://aclanthology.org/2024.findings-emnlp.290/)
- [Chain-of-Verification Reduces Hallucination in Large Language Models — Findings of ACL 2024 (ACL Ant](https://aclanthology.org/2024.findings-acl.212/)
- [RARR: Researching and Revising What Language Models Say, Using Language Models — ACL 2023 (ACL Antho](https://aclanthology.org/2023.acl-long.910/)
- [Huang et al., Large Language Models Cannot Self-Correct Reasoning Yet — ICLR 2024](https://arxiv.org/pdf/2310.01798)
- [ALOHa: A New Measure for Hallucination in Captioning Models — NAACL 2024 (Short Papers, ACL Antholog](https://aclanthology.org/2024.naacl-short.30/)
- [AskEase — From Struggle to Success: Context-Aware Guidance for Screen Reader Users in Computer Use (](https://dl.acm.org/doi/full/10.1145/3772318.3790661)
- [Do GUI Grounders Truly Understand UI Elements? (Findings of EACL 2026)](https://aclanthology.org/2026.findings-eacl.144/)
- [Uncertainty-Based Abstention in LLMs Improves Safety and Reduces Hallucinations (OpenReview)](https://openreview.net/forum?id=1DIdt2YOPw)
- [Visual Description Grounding Reduces Hallucinations and Boosts Reasoning in LVLMs (arXiv 2405.15683)](https://arxiv.org/abs/2405.15683)
- [HalluClear: Diagnosing, Evaluating and Mitigating Hallucinations in GUI Agents (arXiv 2604.17284)](https://arxiv.org/pdf/2604.17284)
- [Aria-UI: Visual Grounding for GUI Instructions (Findings of ACL 2025)](https://aclanthology.org/2025.findings-acl.1152.pdf)

_Tổng: 29 URL._

### B.3. Claim đã trích từ 24 nguồn (đã chạy Fetch/Extract — MỖI claim CHƯA qua phản-bác 3-phiếu)

> Ký hiệu importance: central/high = claim lõi. `quality` = chất lượng nguồn; `date` = ngày/venue.


**Nguồn 1** — chất lượng: `secondary` · ngày/venue: `2025-09 (arXiv:2509.18970v1)`
- (central) As of 2025, post-hoc verification is one of three major mainstream categories of hallucination mitigation for LLM agents (alongside knowledge utilization and paradigm improvement), indicating detect-then-mitigate remains a valid current paradigm rather than being abandoned for grounded/end-to-end generation.
- (supporting) External references (expert knowledge, knowledge bases, world models) substantially reduce hallucination likelihood across agentic operations, supporting the legitimacy of verification/grounding against external structured sources.
- (supporting) The survey frames external-knowledge verification and internal knowledge activation as complementary pathways, not mutually exclusive competitors — consistent with post-hoc external-source checking coexisting with grounded generation.
- (tangential) The survey does not directly assert prevalence of post-hoc versus end-to-end approaches, so it provides only indirect support that post-hoc has not been displaced — it does not contain contrary evidence that the field abandoned post-hoc verification.

**Nguồn 2** — chất lượng: `blog` · ngày/venue: `2026-03-23 (updated 2026-05-20)`
- (central) The field's dominant recommendation for factual hallucination is grounded/retrieval-augmented generation that constrains generation upstream, not post-hoc correction alone.
- (central) Post-hoc detection/verification is still treated as essential even in a grounded-generation-favoring 2026 architecture (the two are layered, not mutually exclusive).
- (supporting) Adding retrieval/context to the prompt reduces hallucination sharply, but the source gives no specific percentage figure (does not support a '~2%' claim).
- (tangential) Faithfulness verification is framed around external groundedness/context-adherence checks (NLI classifiers, DeBERTa) rather than the named academic methods FaithScore, CoVe, or RARR, which are not cited.

**Nguồn 3** — chất lượng: `primary` · ngày/venue: `2025-09-30`
- (central) The claim that adding context/structured prompting drops hallucinations to ~2% is NOT supported by this source; the largest reduction reported is CoT prompting lowering hallucinations to 18.1% (from 38.3% for vague prompts) — so the thesis's '~2%' figure is not corroborated here and may be exaggerated.
- (supporting) Prompt engineering reduces but does not eliminate hallucinations and is not a universal fix, especially for models with strong internal biases — supporting the thesis argument that a separate post-hoc verification layer remains necessary.
- (central) Post-hoc verification remains a legitimate, current (2025) mitigation approach — the paper lists it as a viable component using auxiliary classifiers/LLMs-as-judges to score and post-edit content, rebutting the notion that the field has abandoned post-hoc in favor of grounded-only.
- (central) The recommended 2025 best practice is a HYBRID pipeline combining prompt construction, retrieval (RAG/grounding), AND post-generation verification — i.e., post-hoc verification and grounded generation coexist rather than one superseding the other.
- (supporting) Hallucinations arise from both prompt-dependent and model-intrinsic factors, so mitigation must be tailored — supporting the thesis rationale for 'blind generation' as a measurement mode to expose model-intrinsic hallucination independent of prompt context.

**Nguồn 4** — chất lượng: `primary` · ngày/venue: `2024-06-08`
- (central) Post-hoc verification of grounded generation via an external check remains an actively-developed, peer-reviewed paradigm in 2024 (CaLM, ACL 2024): it validates an already-generated response after the fact rather than replacing generation with a single grounded/end-to-end pass — directly supporting thesis claim 1 that generate-then-verify is not obsolete.
- (supporting) The design principle is that a trustworthy grounded output must be consistent with information derived only from an external cited source — the same logic the thesis uses when it hHecks VLM-generated button names against the View Hierarchy rather than trusting the model's parametric generation.
- (supporting) Constraining a verifier to an external source and correcting divergence produces measurable, reproducible gains (1.5%-7% absolute) without fine-tuning, evidence that external/structured-source post-hoc correction is a working, quantified method (relevant to thesis claim 3 on external-signal correction being valid).
- (supporting) Larger models' factual grounding is verified by smaller models that lean on provided documents rather than parametric memory, showing the field explicitly separates a generation step from an external-grounding verification step — reinforcing that post-hoc, source-anchored checking is current best practice, not superseded by grounded end-to-end generation.

**Nguồn 5** — chất lượng: `primary` · ngày/venue: `2024-10-30`
- (central) TOMATO benchmark shows multimodal foundation models fail at visual temporal reasoning, with a 57.3% human-model performance gap for the best model — supporting the thesis claim that VLMs are weak at temporal/order reasoning across frames.
- (central) VLMs can recognize events in isolated frames but fail to interpret frames as a continuous ordered sequence, empirically supporting the 'bag-of-frames' / order-agnostic weakness claim (research question #4).
- (supporting) Existing temporal benchmarks overestimate VLM temporal ability because many questions are solvable from a single, few, or out-of-order frames — implying models do not truly rely on frame order.
- (supporting) The source is an arXiv preprint (submitted Oct 30, 2024) of the paper accepted to ICLR 2025; the thesis citation 'TOMATO (ICLR 2025)' matches the venue, though it should be treated as supporting evidence given the underlying artifact is a preprint.

**Nguồn 6** — chất lượng: `primary` · ngày/venue: `2026-03-18`
- (supporting) A 2026 hallucination-mitigation system uses a HYBRID of intrinsic (internal confidence / early-exit) and EXTERNAL post-hoc verification (atomic claim-level cross-referencing against retrieved evidence), showing post-hoc verification against external sources remains an active, published paradigm in 2026 rather than being abandoned for pure grounded/end-to-end generation.
- (supporting) Adding tiered retrieval/context significantly reduces hallucination, with win rates of 83.7% (TimeQA v2) and 78.0% (MMLU Global Facts) over zero-shot baselines and groundedness 78.8%-86.4% — evidence that supplying external context suppresses hallucination (relevant to the thesis claim that loading context lowers measurable hallucination).
- (tangential) The system abstains (graceful refusal / circuit breaker) rather than emitting an unverifiable claim when evidence is exhausted, consistent with the 'describe-don't-guess'/abstention consensus rather than treating refusal as failure.

**Nguồn 7** — chất lượng: `blog` · ngày/venue: `2025-02`
- (central) State-of-the-art LMMs (including GPT-4o) perform far below humans on reordering shuffled image sequences, with GPT-4o at ~24% vs humans at ~80%, confirming weak temporal/order reasoning.
- (central) VLMs behave in an order-agnostic 'bag-of-frames' manner, relying on individual frame content rather than sequential relationships, since performance is similar even when sequences are shuffled.
- (central) The failure is specifically in temporal/logical sequence reasoning, not in semantic understanding of individual frames — supporting the need for an explicit ordering module rather than trusting the VLM's native sequence handling.

**Nguồn 8** — chất lượng: `primary` · ngày/venue: `2024-06`
- (central) The paper 'Large Language Models are Effective Text Rankers with Pairwise Ranking Prompting' by Qin et al. is published in Findings of the Association for Computational Linguistics: NAACL 2024 (June 2024), verifying the thesis citation 'Qin et al. pairwise ranking prompting (NAACL 2024)' as correct venue and year.
- (central) LLMs do not fully understand pointwise and listwise ranking formulations, so pairwise ranking prompting reduces the task burden and yields better ranking performance — supporting the thesis choice of pairwise 'which screen first?' comparisons over listwise one-shot ordering.
- (supporting) PRP with a moderate 20B open-source model matches GPT-4 (roughly 50x larger) and beats listwise/pointwise LLM solutions by over 10% on ranking metrics, providing quantitative evidence that pairwise prompting outperforms one-shot listwise ranking.
- (tangential) PRP variants can achieve competitive ranking with linear complexity, relevant to feasibility of the thesis's pairwise-comparison Stage-0 (though the paper does not itself describe Copeland or minimum feedback arc set aggregation).

**Nguồn 9** — chất lượng: `secondary` · ngày/venue: `?`
- (supporting) Minimum feedback arc set is NP-complete, one of Karp's 21 original NP-complete problems, so exact cycle-breaking on VLM pairwise comparisons requires heuristic/approximation algorithms.
- (central) A feedback arc set is a set of edges whose removal makes a directed graph acyclic, i.e. it breaks every cycle — matching the thesis's use of min-FAS to resolve contradictory ordering cycles.
- (central) Minimum feedback arc set is a standard, principled formulation for rank aggregation from pairwise comparisons, minimizing the number of upsets (lower-ranked beating higher-ranked), tied to the Kemeny-Young method.
- (supporting) The best known polynomial-time approximation for min-FAS is O(log n log log n); no constant-factor approximation is known, so the thesis's tie-breaking must rely on heuristics/margin weights rather than optimal solutions.

**Nguồn 10** — chất lượng: `primary` · ngày/venue: `2025 (ICLR 2025)`
- (supporting) Naively prompting a VLM to predict values across a natural (temporally-ordered) video sequence performs poorly because of strong temporal correlation between successive frames.
- (central) Reformulating the task as ordering/value estimation over SHUFFLED (order-disrupted) video frames improves VLM performance by forcing fuller use of its temporal/semantic grounding — i.e. VLMs handle shuffled frames better than naive ordered sequences, evidence that explicit ordering-over-shuffled-frames is a productive design choice.
- (supporting) GVL autoregressively predicts task-completion percentage over shuffled frames, demonstrating that treating a shuffled image set and re-inferring progress/order is a viable VLM methodology (parallels the thesis Stage-0: N shuffled screens -> infer order).
- (tangential) The method is published at ICLR 2025 by Google DeepMind / UPenn / Stanford authors, making it a peer-reviewed anchor rather than a preprint.

**Nguồn 11** — chất lượng: `primary` · ngày/venue: `2026-02-03`
- (central) The paper argues post-hoc/external verification approaches are 'extrinsic' and inferior because they add latency and act only after generation — providing contrarian evidence that the field is pushing toward intrinsic/training-time mitigation rather than post-hoc. (But it does NOT claim post-hoc is obsolete.)
- (supporting) Post-hoc external verification remains an acknowledged, effective mitigation family as of early 2026 — the paper explicitly concedes it works 'in controlled settings' and cites 2024-2025 works using it, so post-hoc is not portrayed as discredited/outdated.
- (tangential) VeriFY (training-time consistency-based self-verification) reduces factual hallucination rates by 9.7-53.3% with only 0.4-5.7% recall loss, offering a concrete measured alternative to abstention-heavy methods that this thesis could cite as the 'grounded/intrinsic' counterpoint.
- (supporting) Uncertainty-to-abstention fine-tuning tends to be over-conservative — supporting the thesis's 'describe-don't-guess' caution that naive abstention degrades usefulness (drops correct-response rate).

**Nguồn 12** — chất lượng: `primary` · ngày/venue: `2023-10-03 (v1); revised 2024-03-14; ICLR 2024`
- (central) Huang et al. 'Large Language Models Cannot Self-Correct Reasoning Yet' is genuinely an ICLR 2024 paper (arXiv:2310.01798, submitted Oct 2023, revised Mar 2024) — the citation venue/year in the thesis is CORRECT.
- (central) The paper demonstrates that LLMs cannot reliably self-correct their reasoning using only their own internal capabilities, without external feedback — supporting the thesis distinction that only INTRINSIC self-correction is shown ineffective.
- (central) Intrinsic self-correction is explicitly defined as correction based solely on the model's own capabilities without external feedback; the paper's negative result is scoped to this intrinsic setting, NOT to correction driven by external/oracle signals — validating the thesis claim that non-LLM/deterministic external-signal correction is not refuted by this paper.
- (supporting) With intrinsic self-correction, model performance can actually get worse rather than better, reinforcing that the thesis's pipeline should rely on external structured signals (View Hierarchy match) rather than the model self-judging.

**Nguồn 13** — chất lượng: `primary` · ngày/venue: `2023-05-19 (submitted); last revised 2024-02-21; published ICLR 2024`
- (central) CRITIC enables LLMs to self-correct via interaction with EXTERNAL tools (search engines, code interpreters), directly supporting the thesis's distinction that external/deterministic-signal correction is legitimate — unlike internal-only self-correction shown to fail.
- (central) CRITIC's central empirical finding is that external feedback is essential for LLM self-improvement, implying self-correction without external signals is unreliable — corroborating the thesis's claim that only INTERNAL self-correction was proven useless (Huang ICLR 2024) while external-signal correction is valid.
- (supporting) CRITIC is peer-reviewed at ICLR 2024, making it a citable backbone (not merely preprint) source for the legitimacy of tool-interactive / external-signal correction paradigms.
- (supporting) CRITIC embodies the generate-then-verify (post-hoc) paradigm — output first, then validate and amend against an external checker — which remains an accepted 2024 paradigm rather than being replaced by grounded end-to-end generation.

**Nguồn 14** — chất lượng: `primary` · ngày/venue: `2024-10-30 (revised 2025-08-25)`
- (central) Multimodal/vision-language models' temporal reasoning is overestimated because many temporal questions can be solved using a single, few, or out-of-order frames — i.e. models exploit order-agnostic shortcuts rather than reasoning over the sequence. This directly supports the thesis claim (assertion #4) that an explicit screen-ordering module is not redundant.
- (central) Even when models recognize isolated events correctly, they fail to interpret frames as a continuous sequence — evidence that VLMs lack genuine temporal/order understanding, reinforcing the need for a dedicated ordering stage (Stage-0) rather than relying on long-context VLM sequence handling.
- (supporting) There is a large human-model performance gap of 57.3% for the best model on visual temporal reasoning, quantifying how weak current frontier VLMs are at temporal ordering tasks.
- (supporting) TOMATO's benchmark of 1,484 questions over 1,417 videos was designed with a 'Frame Order Sensitivity' principle explicitly to expose shortcut behavior — methodological support that order-sensitivity is a real, measurable failure mode in 2024-2025 models.
- (supporting) CITATION CAVEAT: the arXiv record (2410.23266, submitted 30 Oct 2024, revised 25 Aug 2025) does NOT confirm publication at ICLR 2025 — the abstract page shows no conference proceedings, so the thesis's 'TOMATO (ICLR 2025)' venue attribution should be independently re-verified before printing.

**Nguồn 15** — chất lượng: `primary` · ngày/venue: `2023-07`
- (central) RARR was published at ACL 2023 (61st Annual Meeting of the Association for Computational Linguistics, Volume 1: Long Papers, July 2023, Toronto) — confirming the thesis citation 'RARR (ACL 2023)' is correct in venue and year.
- (central) RARR is a post-hoc verification/revision paradigm: it takes an already-generated LM output and edits it against externally retrieved evidence, rather than grounding at generation time — a peer-reviewed precedent for the thesis's 'generate first, verify against external source afterward' design.
- (supporting) RARR works on the output of ANY text generation model (model-agnostic post-hoc attribution), supporting the thesis's claim that its faithfulness-checking layer is model-agnostic and applied after generation.
- (supporting) RARR preserves the original output as much as possible while fixing unsupported content, aligning with the thesis's 'minimal-edit / describe-don't-guess' philosophy of altering only hallucinated spans rather than regenerating.

**Nguồn 16** — chất lượng: `primary` · ngày/venue: `2024-11`
- (central) FaithScore is a reference-free, fine-grained metric that measures the faithfulness of free-form VLM answers by verifying atomic facts against the input image (published Findings of EMNLP 2024) — confirming the exact venue/year the thesis cites.
- (supporting) FaithScore verifies VLM outputs by decomposing generation into identify sub-sentences, extract atomic facts, then verify consistency against the image — a post-hoc, decompose-then-verify pipeline that parallels the thesis's 'generate then check against external structure' philosophy.
- (supporting) Current vision-language systems still generate hallucinated content unfaithful to the image, establishing that hallucination measurement (the thesis's 'sinh mù để đo mức tự-ảo-giác') remains a live 2024 problem, not a solved one.

**Nguồn 17** — chất lượng: `primary` · ngày/venue: `2024-08`
- (central) The paper 'Chain-of-Verification Reduces Hallucination in Large Language Models' is published in Findings of the Association for Computational Linguistics: ACL 2024 (2024), confirming the citation 'CoVe (Findings ACL 2024)' has the correct venue and year.
- (central) CoVe implements a generate-then-verify (post-hoc) paradigm: the model drafts a response, then plans and answers verification questions, then produces a final verified answer — establishing post-hoc verification as a legitimate 2024 hallucination-reduction strategy.
- (supporting) Post-hoc verification (CoVe) empirically decreases hallucination across multiple task types, supporting that generate-then-check is effective rather than obsolete.
- (supporting) CoVe's verification is INTERNAL self-verification (the model fact-checks itself), not external-source anchoring — so it supports the general post-hoc paradigm but differs from the thesis's external View-Hierarchy anchoring, and does not by itself validate deterministic external-signal correction.

**Nguồn 18** — chất lượng: `primary` · ngày/venue: `2024-12-03`
- (central) The survey concludes self-correction works well specifically on tasks that can use RELIABLE EXTERNAL FEEDBACK, distinguishing this from intrinsic (self-evaluation only) correction — directly supporting the thesis distinction that external/deterministic signals make correction valid.
- (central) No prior work demonstrates successful self-correction using feedback from prompted LLMs (intrinsic), except on tasks exceptionally suited for self-correction — corroborating that intrinsic self-correction is not a reliable mechanism.
- (supporting) Intrinsic self-correction (model relying only on its own evaluation without external verification) is unreliable — models cannot reliably self-correct without external verification.
- (supporting) The critical survey is peer-reviewed and appeared in TACL 2024 (v3 dated December 2024), making it a citable peer-reviewed backbone source alongside Huang ICLR 2024.

**Nguồn 19** — chất lượng: `primary` · ngày/venue: `2024`
- (central) Poor LLM self-correction on reasoning stems from an inability to FIND errors, not an inability to correct a known error — separating the two capabilities.
- (central) When given ground-truth error location (an external signal), LLM correction is effective, boosting downstream performance across 5 reasoning tasks — i.e., correction conditioned on an external locator is robust.
- (supporting) Reliable error localization can come from an EXTERNAL, non-prompt system (a small trained classifier) that outperforms prompting a large model to self-detect — supporting deterministic/external signals over intrinsic self-judgment.
- (supporting) Intrinsic self-correction of reasoning errors often degrades outputs (correct answers become incorrect), corroborating Huang et al. — the paper positions this against externally-signaled correction.

**Nguồn 20** — chất lượng: `primary` · ngày/venue: `2024-06`
- (central) ALOHa ("ALOHa: A New Measure for Hallucination in Captioning Models") was published at NAACL 2024 in the Short Papers track, confirming the thesis's cited venue and year are correct.
- (central) ALOHa detects hallucination by using an LLM to extract groundable objects from a candidate caption and measuring their semantic similarity to reference objects and object detections, then applying Hungarian matching — an external-source, semantic-similarity post-hoc verification approach that supports the thesis's embedding-matching-against-external-source design.
- (supporting) ALOHa enables open-vocabulary hallucination detection via LLM semantic matching, outperforming the fixed-vocabulary CHAIR metric by identifying 13.6% more hallucinated objects on HAT and 30.8% more on nocaps.
- (central) The metric works by post-hoc verification: generation happens first, then objects are extracted and checked against external reference sources — validating the thesis's "generate then verify against external structured source" paradigm as a legitimate published approach.

**Nguồn 21** — chất lượng: `primary` · ngày/venue: `2023-10-03 (revised 2024-03-14; ICLR 2024)`
- (central) The paper's exact title is 'Large Language Models Cannot Self-Correct Reasoning Yet' and it was published at ICLR 2024 (Huang, Chen, Mishra, Zheng, Yu, Song, Zhou), confirming the thesis citation venue/year is correct.
- (central) The paper explicitly scopes its negative finding to INTRINSIC self-correction, defined as correction based solely on the model's own capabilities WITHOUT external feedback — supporting the thesis's distinction that only internal self-correction is shown ineffective.
- (central) The paper's main empirical finding is that LLMs fail to self-correct reasoning without external feedback, and performance can even degrade after self-correction.
- (supporting) The paper treats external feedback as a distinct category separate from intrinsic self-correction, implicitly leaving the door open that externally-guided (e.g., oracle/deterministic) correction is not covered by the negative result.

**Nguồn 22** — chất lượng: `primary` · ngày/venue: `2026-03`
- (central) The paper 'Do GUI Grounders Truly Understand UI Elements?' by Jandial, Li, Wagle, Koishida is published in Findings of the ACL: EACL 2026 (March 2026), confirming the exact venue and year cited in the thesis.
- (supporting) Frontier GUI/VLM models hallucinate even when producing a single grounding instruction for a UI element, evidencing that grounder output cannot be trusted at face value and needs external validation.
- (supporting) GUI grounding models rely on superficial pattern matching rather than genuine semantic UI understanding: they give inconsistent outputs across valid re-descriptions of the same element, and benchmark accuracy overstates true ability.
- (supporting) A diagnosis agent can generate instructions that make state-of-the-art GUI grounders fail at up to 84% success rate, showing grounders are brittle and unreliable on adversarial-but-valid instructions.
- (central) This paper concerns GUI grounding sensitivity/diagnosis for desktop agents, NOT step-by-step tutorial generation for human readers with View-Hierarchy-anchored post-hoc verification and no-gold evaluation — so it does not scoop the thesis's specific combination.

**Nguồn 23** — chất lượng: `primary` · ngày/venue: `2024-04-16`
- (supporting) Enabling LLMs to abstain from answering uncertain questions reduces hallucinations by approximately 50% by identifying unanswerable questions.
- (supporting) Uncertainty-based abstention improves correctness by 2-8% and increases safety by 70-99% with minimal computational overhead, and works across models with and without RLHF.
- (supporting) Abstention is framed as the desirable behavior under uncertainty, analogous to humans refraining from answering what they do not know — endorsing abstention as a legitimate reliability strategy rather than a failure mode.
- (tangential) The paper is authored by Christian Tomani, Kamalika Chaudhuri, Ivan Evtimov, Daniel Cremers, Mark Ibrahim (Meta FAIR), submitted April 16, 2024; the OpenReview page was behind a verification wall so accepted/peer-reviewed status could not be confirmed — treat as preprint.

**Nguồn 24** — chất lượng: `primary` · ngày/venue: `2026-04 (CHI 2026; arXiv preprint 2601.18092 dated 2026-01)`
- (central) AskEase (CHI 2026) generates step-by-step, screen-reader-friendly guidance for computer use from screenshots + structured screen state + a free-form user question, targeting screen reader (accessibility) users — an adjacent but distinct task from the thesis's 'generate GUI usage guidance for sighted people from screenshot + use-case question'.
- (central) AskEase does NOT perform post-hoc verification of generated steps against a ground-truth View Hierarchy / accessibility tree; it grounds via RAG over software documentation + live screen state (NVDA API), and its evaluation is a human user study (12 participants) plus binary success on 45 tasks with no automated no-gold quality metric — so it does not occupy the thesis's exact combo (VH-anchored post-hoc check + no-gold automated eval).
- (supporting) AskEase adopts an explicit abstention / 'state-uncertainty-rather-than-guess' policy, supporting the thesis claim that a describe-don't-guess / abstention stance matches 2025-26 consensus.
- (central) The citation 'AskEase — From Struggle to Success: Context-Aware Guidance for Screen Reader Users in Computer Use (CHI 2026)' is verified as a real, correctly-attributed paper: CHI '26 Proceedings, DOI 10.1145/3772318.3790661, Barcelona April 2026, arXiv 2601.18092, authors Nan Chen et al.
---

## PHẦN C — KẾT QUẢ VERIFY + SYNTHESIZE (R-07 HOÀN TẤT 2026-07-05, `wf_f227453f-dd5`)

### PHÁN QUYẾT: Pipeline (đóng góp A) ĐỦ làm đóng góp khoa học thạc sĩ — CÓ ĐIỀU KIỆN.
7/8 khẳng định lõi đứng vững sau phản-bác đối kháng 3-phiếu. Vượt ngưỡng "chỉ ghép công cụ" (có phát hiện silent-error + phương pháp VH-anchored post-hoc + độ mới combo + đối-chứng). Giữ "ngang B" cần: (i) hạ phát biểu tuyệt-đối; (ii) RA SỐ dương (K-pair>0.5, DG2/Step-SR dương, bảng 81 màn); (iii) neo novelty vào COMBO, không vào riêng VH-check.

### 8 khẳng định — kết quả phản-bác
| ID | Nội dung | Kết quả | Ghi chú |
|---|---|---|---|
| A1 | post-hoc verify chính danh 2024-26 | ✅ sống 0/3 | field coi grounded=PRIMARY, post-hoc=SECONDARY → đừng khoe post-hoc "tốt nhất" |
| A2 | sinh-mù để ĐO | ✅ sống 0/3 | hạ "ảo giác biến mất" → "che/nhiễu phép đo" (grounding chỉ giảm) |
| A3 | sửa bằng tín hiệu ngoài hợp lệ | ✅ sống 0/3 | external phải đáng-tin; Chen ICSE20 → đúng khi bỏ correction sang PA2 |
| A4 | VLM bag-of-frames, Stage-0 không thừa | ✅ sống 0/3 (mạnh nhất) | khai Stage-0 = scaffold có cấu trúc, không nói long-context "bất lực tuyệt đối" |
| A5 | pairwise>listwise; Copeland+min-FAS là CHUẨN | ❌ **bác 3/3** | chỉ bác tính TUYỆT-ĐỐI. Reframe "một-trong-nhiều cho VLM tầm-trung" + baseline listwise + ghi nhận Bradley-Terry/Elo |
| A6 | describe-don't-guess ≈ abstention | ✅ sống 0/2 | hạ "đồng thuận" → "xu hướng" (AbstentionBench: chưa giải) |
| A7 | combo chưa bị scoop | ✅ sống 0/3 | trích neighbor FSE'26 "From Task to Tutorial" (2509.21816) + a11y bug-report (2603.23828); neo novelty ở COMBO |
| A8 | đóng góp có chất, không chỉ ghép | ✅ sống 0/3 | như G-Eval/FActScore/RAGAS; nhưng chỉ thành research khi RA SỐ |

### Trụ peer-reviewed (đậu/rớt): CHAIR EMNLP18 · ALOHa NAACL24 · Kamoi TACL24 · Huang ICLR24 · Qin NAACL24 · RankGPT EMNLP23 · TOMATO ICLR25 · Apple video-benchmark NeurIPS25. Preprint (VECTOR, Burn-After-Reading, AbstentionBench, FSE'26 near-match…) = CHỈ bổ trợ.

### CITATION — 6/6 ĐÚNG venue (gỡ hết ⚠):
- TOMATO = **ICLR 2025 Poster** (OpenReview fCi4o83Mfs) · EZ-Sort = CIKM'25 (DOI 10.1145/3746252.3760848) · Dodgersort = PAKDD 2026 Part IV (DOI 10.1007/978-981-92-1468-6_32) · Measuring what Matters = NeurIPS 2025 **D&B Track**, tên đầy đủ "…in **Large Language Model** Benchmarks" (OpenReview mdA5lVvNcU) · Neither Valid nor Reliable = NeurIPS 2025 poster · MacKinnon-Nielsen-Webb = J.Econometrics 232(2) 2023 pp.272-299.
- Sửa nhãn khi in: ghi "Poster" cho TOMATO; tên đầy đủ + "D&B Track" cho Measuring-what-Matters.

### VIỆC PHẢI ÁP VÀO report/43 (từ đợt này):
1. A5: reframe pairwise/Copeland ở §4.3/§4.4/Q&A + thêm baseline listwise + ghi nhận Bradley-Terry.
2. Hạ chữ tuyệt-đối: A2 (§4.5 "biến mất"→"che/nhiễu"), A6 ("đồng thuận"→"xu hướng"), A4 (scaffold).
3. Citation: TOMATO "Poster" (bỏ ⚠); Measuring-what-Matters tên đầy đủ + D&B Track; gỡ ⚠ EZ-Sort/Dodgersort/MacKinnon (đã xác nhận).
4. A7: thêm 2 neighbor (FSE'26 2509.21816, a11y bug-report 2603.23828) vào related-work; neo novelty ở combo.
