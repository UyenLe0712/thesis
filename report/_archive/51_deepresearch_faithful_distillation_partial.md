# Deep research — Faithful Distillation (BẢN DỞ, đang verify)

> ⚠️ Trích từ workflow `wf_45ce881b` lúc đang chạy (scope + 5 tìm kiếm + ~20 nguồn + ~57 phiếu verify; CHƯA có synthesis cuối). Câu hỏi: SFT-distillation VLM nhỏ làm bộ SINH hướng dẫn có vững/khả thi/đủ đóng góp thạc sĩ không. Lưu 2026-07-09. **RESUME:** xem cuối file.

## 1. Góc tìm kiếm
- **broad/primary — VLM distillation ảnh→text sinh** — `knowledge distillation small vision-language model image captioning generation teacher larger VLM 2024 2025 peer-reviewed`
- **academic/technical — fine-tune VLM nhỏ hiểu/mô tả GUI** — `fine-tuning small vision language model GUI screenshot understanding instruction generation Qwen2.5-VL LoRA mobile UI 2025`
- **methodology — self-training/lọc dữ liệu no-gold** — `self-training bootstrapping LLM filtered synthetic data faithfulness verification without gold labels student outperforms teacher distillation 2024 2025`
- **practitioner/feasibility — QLoRA 3B on Colab** — `QLoRA fine-tuning 3B multimodal model single GPU consumer VRAM Colab training time cost on-device small VLM deployment`
- **contrarian/skeptical — bẫy distillation & forgetting** — `limitations knowledge distillation student mimics teacher no new capability catastrophic forgetting LoRA fine-tuning vision-language teacher data quality bias 2024 2025`

## 2. Nguồn tìm được (5 góc)
- **Efficient Deployment of Vision-Language Models on Mobile Devices: A Case Study on OnePlus 13R** [high]  
  https://arxiv.org/abs/2507.08505  
  Directly supports the on-device niche argument (part d). Benchmarks 3B-class VLMs — MobileVLM-3B and Imp-v1.5 3B alongside LLaVA-1.5 7B — actually running on a real phone (OnePlus 13R) via llama.cpp / MLC / mllm, documenting latency, memory and energy. Concrete peer-reviewed-style evidence that a small (3B) VLM is the right size class for on-device deployment where frontier APIs cannot run — the core justification for training a small student model rather than just calling gpt-4o-mini.
- **Profiling LoRA/QLoRA Fine-Tuning Efficiency on Consumer GPUs: An RTX 4060 Case Study** [high]  
  https://arxiv.org/html/2509.12229v1  
  Feasibility backbone: empirical VRAM/time/throughput profiling of LoRA vs QLoRA on a consumer 8GB GPU, close analog to Colab T4 (16GB). Gives defensible numbers for the ~$100-150 Colab budget claim — QLoRA loads base in 4-bit NF4, trains adapters in full precision, fitting 7B in 16GB (so 3B is comfortable). Useful to cite when arguing the training run is reproducible on student-grade hardware.
- **An Efficient Training Pipeline for Reasoning Graphical User Interface Agents** [high]  
  https://arxiv.org/pdf/2511.08172  
  Closest in-domain precedent: fine-tunes Qwen2.5-VL (3B/7B) on GUI screenshots with LoRA (4-bit, rank=8, adapters in attention+FFN, aspect-ratio-preserving resize of large screenshots). Confirms the exact base model + PEFT recipe is viable for GUI screen tasks and gives concrete config numbers. Note: it targets GUI *agents/grounding*, so the thesis must differentiate on the *generation* (instruction-writing-for-humans) task to avoid overlap/scoop.
- **MobileVLM V2: Faster and Stronger Baseline for Vision-Language Model** [medium]  
  https://arxiv.org/pdf/2402.03766  
  Peer-reviewed reference model for the mobile-scale VLM niche (MobileLLaMA 1.4B/2.7B + lightweight downsample projector, designed for resource-constrained devices). Anchors the 'small multimodal generator on-device' framing (part d) and provides a citable baseline/size class to position Qwen2.5-VL-3B against. Reinforces that sub-3B multimodal generation is an established, defensible research target.
- **BLIP: Bootstrapping Language-Image Pre-training (CapFilt captioner + filter)** [medium]  
  https://arxiv.org/pdf/2201.12086  
  Foundational peer-reviewed precedent for the 'train on teacher output filtered for faithfulness' idea (part c). CapFilt = a captioner distills knowledge via synthetic captions and a filter removes noisy ones — structurally identical to the thesis's teacher(gpt-4o-mini)-generates + VH-faithfulness-filter loop, minus human gold. Strong citation to legitimize filtered-self-training/bootstrapping as a real contribution, not mere copying.
- **How to Fine-Tune Qwen2.5-VL with a Custom Dataset (Roboflow)** [medium]  
  https://blog.roboflow.com/fine-tune-qwen-2-5/  
  Practitioner walkthrough (not peer-reviewed) of LoRA fine-tuning Qwen2.5-VL on custom screenshot data with a live Gradio interface, showing it teaches domain-specific vocabulary/patterns. Useful only as an implementation reference for the Colab pipeline (data format, adapter setup, inference) — cite academic sources above for claims, use this for engineering feasibility.
- **LLaVA-KD: A Framework of Distilling Multimodal Large Language Models (ICCV 2025)** [high]  
  https://openaccess.thecvf.com/content/ICCV2025/html/Cai_LLaVA-KD_A_Framework_of_Distilling_Multimodal_Large_Language_Models_ICCV_2025_paper.html  
  PEER-REVIEWED anchor (ICCV 2025) directly supporting direction (a): transfers knowledge from a large MLLM teacher to a small-scale MLLM student for multimodal understanding/generation, WITHOUT changing architecture. Its 3-stage recipe (distilled pre-train → SFT → distilled fine-tune) and evidence that the small student improves over its base is exactly the framing to rebut 'just distilling the teacher' and to show a small VLM can be a legitimate trained core. arXiv 2410.16236.
- **VGA: Vision GUI Assistant — Minimizing Hallucinations through Image-Centric Fine-Tuning** [high]  
  https://arxiv.org/pdf/2406.14056  
  Bridges (a)+(b)+(c) on the exact task: fine-tunes a small VLM specifically for GUI/screen understanding and directly targets HALLUCINATION reduction via image-centric supervised fine-tuning. Strong precedent that faithfulness-oriented SFT of a small VLM on GUI images is a recognized, publishable contribution — and useful to differentiate the thesis' VH-grounded faithfulness filtering.
- **VLsI: Verbalized Layers-to-Interactions from Large to Small Vision Language Models** [medium]  
  https://arxiv.org/pdf/2412.01822  
  Direct large→small VLM distillation for a GENERATIVE VLM (not classification/grounding), reinforcing that distilling generation capacity into a compact student is an active, credible line. Useful as a comparison point for the distillation recipe and for arguing a small student can approach a larger teacher; note it is a 2024 preprint, so use as supporting evidence rather than a peer-reviewed pillar.
- **GenRecal: Generation after Recalibration from Large to Small Vision-Language Models** [medium]  
  https://arxiv.org/pdf/2506.15681  
  Recent method explicitly on distilling from large to small VLMs for GENERATION, tackling the token/logit-mismatch problem across heterogeneous teacher–student pairs. Relevant to the SFT-distillation recipe and to the 'student ≈ teacher vs. adds value' question (risk e); use as supporting evidence for feasibility of small generative students.
- **A Survey on Knowledge Distillation of Large Language Models** [medium]  
  https://arxiv.org/pdf/2402.13116  
  Broad taxonomy covering teacher-generated data synthesis, self-training/bootstrapping, and skill distillation — useful scaffolding for framing the pipeline (data curation from teacher + filtering) and for citing the 'distill data-synthesis capability into a cheap small model via SFT' paradigm. Helps position the thesis within an established, well-surveyed research direction and address the 'only copies the teacher' critique.
- **Winning Big with Small Models: Knowledge Distillation vs. Self-Training for Reducing Hallucination in Product QA Agents** [high]  
  https://arxiv.org/pdf/2502.19545  
  Directly compares KD-from-a-teacher vs self-training for making a SMALL model that hallucinates less on a grounded QA task — exactly the design axis in the thesis (teacher = gpt-4o-mini vs student trained on filtered/own data). Peer-reviewed-style empirical evidence that a small student can match or beat teacher-distillation for hallucination reduction, and that filtered self-training is a legitimate, publishable methodology. Strong armor against the 'you only copied the teacher' critique because it shows student-side gains and quantifies when self-training wins.
- **Measuring and Reducing LLM Hallucination without Gold-Standard Answers** [high]  
  https://arxiv.org/pdf/2402.10412  
  Core support for angle (c): reduces hallucination when NO human gold answers exist, using a self-consistency/verification signal to filter — the same no-gold regime the thesis lives in (no human-authored gold instructions). Establishes that reference-free filtering to curate training data is an accepted method, giving the 'faithfulness-filter creates value' framing peer-reviewed footing.
- **Mind the Gap: Examining the Self-Improvement Capabilities of Large Language Models** [high]  
  https://arxiv.org/pdf/2412.02674  
  Directly addresses risk (e) 'student ≈ teacher / does distillation create new value.' Formalizes the generation-verification gap: self-improvement (and by extension filtered self-training) yields real gains precisely when verification is easier/more reliable than generation. This is the exact justification the thesis needs — the VH-based faithfulness filter is a cheap, reliable verifier over a hard-to-generate output, so filtering can lift the student above naive teacher-copying. Also warns when the gap closes (collapse risk to pre-register against).
- **Bridging the Visual Gap: Fine-Tuning Multimodal Models with Knowledge-Adapted Captions** [high]  
  https://arxiv.org/html/2411.09018v3  
  Critical risk evidence for (b)+(e): shows distilling a large VLM's captions into a SMALLER VLM can INCREASE hallucination when target captions are too complex for the student's pretrained capacity, and that adapting/filtering the training captions to the student fixes it. Warns the thesis that raw teacher output must be curated (their faithfulness filter is well-motivated) and directly supports feasibility of small-VLM SFT on curated image→text data on a modest budget.
- **Distill Not Only Data but Also Rewards: Can Smaller Language Models Surpass Larger Ones?** [medium]  
  https://arxiv.org/pdf/2502.19557  
  Support for the 'student can exceed teacher' claim (e) and for framing distillation as more than copying. Argues quality-filtered / reward-aware distillation lets a smaller model surpass a larger one, reinforcing the 'must show student > base (and ideally > teacher-on-metric)' evidentiary bar the thesis should hit to count as a real contribution rather than plain distillation.
- **Low-hallucination Synthetic Captions for Large-Scale Vision-Language Model Pre-training** [medium]  
  https://arxiv.org/pdf/2504.13123  
  Concrete recipe evidence for (a)+(c) in the multimodal setting: uses filtered/curated synthetic captions (teacher-generated image→text) specifically to lower hallucination when training VLMs. Backs the pipeline choice of teacher-generates → faithfulness-filter → SFT for a generation task on GUI images, and shows filtering synthetic image-text data is an established quality-control step rather than an ad-hoc trick.
- **MobileVLM: A Vision-Language Model for Better Intra- and Inter-UI Understanding (Findings of EMNLP 2024)** [high]  
  https://aclanthology.org/2024.findings-emnlp.599/  
  Peer-reviewed (EMNLP 2024 Findings) proof that fine-tuning a VLM specifically on mobile-UI data materially beats general-domain VLMs at recognizing UI elements and understanding fine-grained intra-UI content plus page-transition (inter-UI) actions. Directly supports angle (b): a general VLM lacks GUI-specific capability, and domain fine-tuning creates measurable new value — the exact 'student > base' argument the thesis needs. Also validates the DG2 idea (page transitions as directed graph). Caveat: uses full multi-stage pretraining on 3M pages (Mobile3M), heavier than the student's LoRA-3B plan — cite as motivation, not as the feasible recipe.
- **DreamStruct: Understanding Slides and User Interfaces via Synthetic Data Generation (ECCV 2024)** [high]  
  https://link.springer.com/chapter/10.1007/978-3-031-72691-0_26  
  The single closest peer-reviewed precedent for the thesis framing: fine-tune a SMALL VLM (LLaVA-1.5-13B) on TEACHER-generated (synthetic) UI/slide data with NO human gold captions, then show it beats the base model and human-caption baselines (UI captioning win rate 64.8%; 55.3 vs 44.3 mAP element recognition; 67.9% vs 33.5% classification). Establishes that 'distill a teacher into a smaller model for UI description/generation' is an accepted, publishable contribution — the strongest shield against the 'just distilling the teacher' critique. Differentiator to preserve: DreamStruct does captioning/recognition, NOT step-by-step how-to instruction generation, and has no faithfulness-filtering/VH-check loop — that is the thesis's novel wedge.
- **ALLaVA: Harnessing GPT4V-Synthesized Data for Lite Vision-Language Models** [high]  
  https://arxiv.org/pdf/2402.11684  
  Direct evidence for the distillation recipe: uses a strong teacher (GPT-4V) to synthesize caption+instruction data, then trains a LITE (3B-class) VLM that reaches competitive quality — the same teacher->small-student SFT-distillation pattern the thesis proposes with gpt-4o-mini teacher + Qwen2.5-VL-3B student. Useful for (a)/(d): data-recipe design, scale of synthetic examples, and the on-device/lite motivation. Also a reference for the risk (c)/(e): student quality is capped by and correlated with teacher data quality, so a faithfulness-filtering layer is the defensible differentiator rather than raw distillation.
- **DeskVision: Large Scale Desktop Region Captioning for Advanced GUI Agents (with automated annotation + faithfulness-style filtering)** [medium]  
  https://arxiv.org/pdf/2503.11170  
  2025 GUI work that builds a large screen-captioning dataset via an automated VLM pipeline with an automatic quality/consistency check (Auto-CD), then fine-tunes VLMs — mirrors the thesis's 'generate with teacher, then filter for faithfulness before training' loop applied to GUI. Supports angle (c): self-generated GUI descriptions curated by an automatic verifier improve downstream models without human gold labels. Use to justify the filter-then-SFT design and to position the VH-based faithfulness filter as a GUI-specific, structured (not just heuristic) instance of this accepted pattern.
- **Leveraging Vision-Language Models for Visual Grounding and Analysis of Automotive UI (2025)** [medium]  
  https://arxiv.org/html/2505.05895v1  
  2025 case study fine-tuning small/mid VLMs (incl. LoRA) on a specialized UI domain (automotive interfaces) for grounding and description, reporting large gains over base models. Reinforces the generality of angle (b) — that LoRA fine-tuning adapts VLMs to a narrow UI vocabulary/layout the base model misses — and supports the 'niche on-device / domain-specialized small model' framing. Weaker fit because it centers on grounding rather than free-form step instruction generation, so cite as supporting landscape, not core precedent.
- **LoRA Learns Less and Forgets Less (Biderman et al., TMLR 2024)** [high]  
  https://arxiv.org/pdf/2405.09673  
  Trụ peer-reviewed (TMLR) trực tiếp cho bẫy (e) của luận văn: LoRA HỌC ÍT HƠN full fine-tune (đặc biệt trên miền xa dữ liệu gốc như code/GUI) NHƯNG cũng QUÊN ÍT HƠN — đúng hai mặt của đề tài. Đây là con dao hai lưỡi cần khai thẳng: SFT-LoRA 3B trên output teacher sẽ bị TRẦN năng lực (student khó vượt teacher), nhưng đổi lại giữ được năng lực nền của Qwen2.5-VL. Dùng để (1) biện minh chọn LoRA thay full-FT (chống forgetting), (2) đặt kỳ vọng đúng cho 'student>base' — cải thiện trên tác vụ faithfulness-GUI, KHÔNG kỳ vọng nhảy vọt tổng quát.
- **Speculative Knowledge Distillation: Bridging the Teacher-Student Gap Through Interleaved Sampling (ICLR 2025)** [high]  
  https://arxiv.org/abs/2410.11325  
  Bằng chứng ICLR 2025 chỉ đích danh lỗ hổng của công thức luận văn đang chọn (SFT trên static dataset teacher): 'supervised KD suffers from DISTRIBUTION MISMATCH with static datasets' + 'errors propagate' + lọc mẫu chất-lượng-thấp. Chính là rủi ro teacher-error-propagation + student off-distribution mà đề tài phải phòng thủ. Ngụ ý: dữ liệu train nên bám phân phối inference của student, và lớp lọc-faithfulness (loại bước bịa) của luận văn CHÍNH là cơ chế phòng thủ tương đồng — điểm đóng góp có thể neo vào đây, nhưng phải thừa nhận trần của static-SFT so với on-policy.
- **Understanding Catastrophic Forgetting in LoRA via Mean-Field Attention Dynamics (2024)** [medium]  
  https://arxiv.org/pdf/2402.15415  
  Phân tích lý thuyết: LoRA VẪN gây catastrophic forgetting qua động lực attention, bác bỏ giả định 'LoRA an toàn tuyệt đối'. Quan trọng cho luận văn vì Qwen2.5-VL-3B fine-tune trên miền hẹp (GUI screenshot) dễ quên năng lực mô tả ảnh tổng quát. Củng cố yêu cầu phải ĐO forgetting (giữ tập held-out ngoài miền) + cân nhắc rank thấp / mix general-knowledge adapter, không chỉ báo số tăng trên tác vụ đích.
- **Continual Learning in Vision-Language Models via Aligned Model Merging / LoRA (2025)** [medium]  
  https://arxiv.org/pdf/2506.03189  
  Cụ thể cho VLM: fine-tune một hoặc mixture LoRA trên VLM NHẠY với thứ tự tác vụ (độ lệch chuẩn cao giữa các chuỗi), plasticity lấn stability. Cảnh báo trực tiếp cho pipeline: nếu train tuần tự trên nhiều nguồn (MobileViews rồi AndroidControl) student có thể quên; nên trộn dữ liệu (mix, không sequential) và báo variance theo seed/thứ tự. Hậu thuẫn bẫy forgetting ở đúng dòng model của đề tài.
- **Rethinking On-Policy Distillation of LLMs: Phenomenology, Mechanism, and Recipe (2026)** [medium]  
  https://arxiv.org/html/2604.13016v1  
  Phản-biện cân bằng: thách thức niềm tin 'distillation luôn suy-giảm-chất-lượng' — 'conflates teacher DISTRIBUTION with teacher BEST outputs'. Nghĩa là nếu luận văn LỌC lấy CHỈ output tốt nhất của teacher (faithfulness-filtered, bỏ bước bịa) thì student CÓ THỂ vượt teacher-trung-bình trên chiều faithfulness — đây chính là luận cứ 'student>base và >teacher-thô' có cơ sở. Dùng để phản công lời chê 'chỉ sao chép teacher': curate + filter tạo giá trị mới đo được, miễn phải chứng minh bằng số (student vs teacher-unfiltered vs base).

## 3. Claim trích từ nguồn (THÔ — nhiều claim đã bị verify BÁC, xem mục 4)
### Nguồn #1 (chất lượng primary)
- Small 3B vision-language models (MobileVLM-3B, Imp-v1.5 3B) and a 7B model (LLaVA-1.5 7B) can be deployed and run on a consumer smartphone (OnePlus 13R), demonstrating on-device feasibility of small VLMs for image-to-text tasks.  
  *quote:* VLM Models Deployed: LLaVA-1.5 7B, MobileVLM-3B, Imp-v1.5 3B
- On-device VLM inference on the OnePlus 13R was bottlenecked by CPU: during token generation CPU was consistently over-utilized while GPU and NPU accelerators sat largely idle, indicating a practical latency/efficiency constraint for on-device generation.  
  *quote:* CPU resources were consistently over-utilized during token generation, while GPU and NPU accelerators were largely unused.
- The study evaluated deployment frameworks (llama.cpp, MLC-Imp, mllm) on real-device metrics including inference time, power consumption, temperature, and CPU/GPU/NPU utilization, providing a practitioner benchmark for running small VLMs on phones.  
  *quote:* examining CPU, GPU, and NPU utilization, temperature, inference time, power consumption, and user experience

### Nguồn #2 (chất lượng primary)
- QLoRA fine-tuning of a 1.5B-parameter model (Qwen2.5-1.5B-Instruct) fits within 8 GB of VRAM, with peak usage between 6.2 and 8.1 GB even at 2048-token sequence lengths.  
  *quote:* VRAM footprint varied between 6.2 GB and 8.1 GB across runs ... sequence lengths up to 2048 tokens were feasible using parameter-efficient strategies
- PagedAdamW improves training throughput by up to 25% over standard AdamW on consumer GPUs, aiding feasibility on constrained hardware.  
  *quote:* PagedAdamW improved throughput by up to 25% vs. standard AdamW
- On the RTX 4060, fp16 consistently outperforms bf16 in throughput and energy per token during LoRA/QLoRA fine-tuning.  
  *quote:* fp16 consistently outperforms bf16 ... bf16 substantially reduced throughput and increased energy per token

### Nguồn #3 (chất lượng blog)
- Qwen2.5-VL-3B can be fine-tuned with LoRA + 4-bit quantization (QLoRA) on a free-tier Colab T4 GPU, demonstrating Colab feasibility for the thesis's proposed on-device small-VLM SFT.  
  *quote:* 4-bit quantization, preserving the model's performance ... LoRA (Low-Rank Adapation). This adaptation configures Qwen with smaller matrices, saving memory during training ... a T4 GPU in colab
- The fine-tuning targets a vision-to-structured-text generation task (extracting pallet manifest info into JSON), showing Qwen2.5-VL-3B can be adapted for image->text generation rather than only detection/grounding.  
  *quote:* extract[ion]...of palette manifests and extract the relevant information into a well-structured JSON format
- The tutorial reports only a qualitative improvement impression and an edit-distance validation, with no quantitative base-vs-fine-tuned comparison, so it does not by itself establish that student surpasses base.  
  *quote:* it performs quite remarkably! ... references "edit distance metric" for validation, but provides no quantitative performance comparisons between base and fine-tuned models

### Nguồn #4 (chất lượng primary)
- A 3B-parameter mobile VLM (MobileVLM V2 3B) can outperform a wide range of VLMs at the 7B+ scale on standard vision-language benchmarks, showing a small VLM can match/beat much larger models.  
  *quote:* 3B parameter model: "outperforms a large variety of VLMs at the 7B+ scale"
- A 1.7B-parameter mobile VLM achieves better or on-par performance versus much larger 3B-scale VLMs, supporting feasibility of very small on-device generative multimodal models.  
  *quote:* 1.7B parameter model: Achieves "better or on-par performance on standard VLM benchmarks compared with much larger VLMs at the 3B scale"
- Gains for small mobile VLMs come chiefly from an improved training scheme plus high-quality dataset curation rather than scale, aligning with a data-curation/faithfulness-filtering training strategy.  
  *quote:* "a delicate orchestration of novel architectural design, an improved training scheme tailored for mobile VLMs, and rich high-quality dataset curation" yielding substantial performance gains
- The work explicitly targets mobile/edge deployment with faster inference, supporting the on-device niche framing for a small student VLM.  
  *quote:* The title highlights "Faster and Stronger Baseline," indicating dual emphasis on inference speed and performance

### Nguồn #5 (chất lượng primary)
- BLIP introduces CapFilt, a dataset-bootstrapping method where a learned captioner generates synthetic captions and a learned filter removes noisy/unfaithful captions — directly precedent for the thesis's 'generate with teacher, then filter unfaithful steps' data pipeline (RQ part c).  
  *quote:* a captioner generates synthetic captions and a filter removes the noisy ones
- Filtering generated captions and bootstrapping from noisy web data (no clean human gold) yields state-of-the-art gains across multiple vision-language tasks, quantified as +2.7% average recall@1 (retrieval), +2.8% CIDEr (captioning), and +1.6% VQA score — peer-reviewed evidence that faithfulness-style filtering of synthetic data improves downstream models.  
  *quote:* image-text retrieval (+2.7% in average recall@1), image captioning (+2.8% in CIDEr), and VQA (+1.6% in VQA score)
- BLIP demonstrates that a model can effectively learn from noisy generated/web data by bootstrapping captions rather than requiring gold annotations — supporting the thesis premise that no human-authored gold instructions are needed if generation is paired with filtering.  
  *quote:* effectively utilizes the noisy web data by bootstrapping the captions

### Nguồn #6 (chất lượng primary)
- Distilling knowledge from a large MLLM into a small-scale MLLM (s-MLLM) significantly improves the small model's performance without changing its architecture, making distillation a validated route to strong compact VLMs.  
  *quote:* significantly improves s-MLLMs performance without altering the model architecture
- Small-scale MLLMs, though built to cut compute cost, typically suffer performance degradation versus large MLLMs — the exact gap that distillation is used to close, motivating a small on-device VLM as a legitimate research target.  
  *quote:* small-scale MLLMs (s-MLLMs) are designed to reduce computational costs, they typically suffer from performance degradation
- The proposed distillation recipe is a three-stage scheme: Distilled Pre-Training (visual-linguistic alignment), Supervised Fine-Tuning (multimodal understanding), then Distilled Fine-Tuning (refining student knowledge).  
  *quote:* three-stage training scheme ... Distilled Pre-Training to strengthen the alignment between visual-linguistic representations in s-MLLMs ... Supervised Fine-Tuning to equip the s-MLLMs with multimodal understanding capacity ... Distilled Fine-Tuning to refine s-MLLM's knowledge
- The framework distills via representation- and relation-level signals (MDist transfers teacher representations across visual+linguistic modalities; RDist transfers visual-token relationships) rather than only imitating teacher text outputs, i.e. a heavier KD than plain output-SFT-distillation.  
  *quote:* Multimodal Distillation (MDist) to transfer teacher model's robust representations across both visual and linguistic modalities ... Relation Distillation (RDist) to transfer teacher model's ability to capture visual token relationships

### Nguồn #7 (chất lượng primary)
- A VLM can be fine-tuned specifically to reduce GUI hallucinations by making outputs image-centric (grounded in visual content), which is exactly the faithfulness goal of the thesis pipeline for a small generator VLM.  
  *quote:* Existing LVLMs often overly depend on internal knowledge and neglect image content, resulting in hallucinations. [...] the model's responses are highly depend on visual content within the image
- The authors built a 63.8k-example GUI VQA training set via a 'Referent Method' to enforce visual grounding, showing that constructing a curated instruction/VQA dataset (rather than relying on human-gold labels) is a valid, peer-reviewed route to fine-tune a VLM for GUI tasks.  
  *quote:* We first construct a Vision Question Answering (VQA) dataset of 63.8k high-quality examples with our propose Referent Method, which ensures the model's responses are highly depend on visual content.
- A two-stage supervised fine-tuning recipe (Foundation and Advanced Comprehension) improved image information extraction and human-intent alignment, supporting SFT (not RL) as the training method for GUI VLMs.  
  *quote:* we design a two-stage fine-tuning method called Foundation and Advanced Comprehension (FAC) to enhance both the model's ability to extract information from image content and alignment with human intent.
- Fine-tuning for GUI understanding achieved state-of-the-art results on GUI understanding tasks, demonstrating the approach is competitive enough to count as a real modeling contribution.  
  *quote:* Experiments show that our approach enhances the model's ability to extract information from images and achieves state-of-the-art results in GUI understanding tasks.

### Nguồn #8 (chất lượng primary)
- A 3B VLM (Qwen-2.5-VL-3B) fine-tuned with LoRA on only 12K model-filtered examples (curated from 4.8M) matches or surpasses much larger (7B) GUI grounding baselines on ScreenSpot, Multimodal-Mind2Web and AndroidControl, evidencing that small-VLM adaptation with data curation is a viable, contribution-worthy direction.  
  *quote:* From 4.8M synthetic examples, 12K clean and diverse instances are curated ... On this data, a 3B-parameter Vision-Language Model is trained ... Models trained with the filtered data and lightweight training strategies match or surpass larger baselines on benchmarks such as ScreenSpot, Multimodal-Mind2Web, and AndroidControl.
- Their core contribution is a model-based faithfulness/alignment filtering pipeline (base VLM scores difficulty, a Qwen-2.5-VL-3B ranker removes misaligned instruction-region pairs, clustering for diversity, GPT-4o-mini post-filter), i.e., data curation itself is framed as the research contribution rather than the training being novel.  
  *quote:* The main contributions of this work are: (i) a detailed filtering method for curating misaligned synthetic data stemming from data generation pipelines using the same base-model as a critic for GUI training instances
- GPT-4o-mini is used as a teacher/oracle both to generate chain-of-thought reasoning traces and as a final post-processing filter to select unambiguous training examples, demonstrating the gpt-4o-mini-as-teacher + distillation-into-small-VLM recipe in peer-reviewed-style GUI work.  
  *quote:* In addition to the filtered examples, we provide chain-of-thought traces derived from GPT-4o mini. ... Finally, we apply a post-processing filtering stage by using GPT-4o mini to further select examples where the instruction clearly points to the correct GUI element without any notion of ambiguity.
- The LoRA/QLoRA training was run on 2x A100 80GB (not single consumer/Colab GPU), with LoRA rank 32-256 and DeepSpeed Stage 3, which is a compute footprint above a typical Colab budget and a feasibility caveat for the thesis constraints.  
  *quote:* All experiments were conducted using 2× A100 80GB.
- Chain-of-thought augmentation gave mixed/degraded results and only GRPO (RL) reached state-of-the-art, meaning the SFT-only path yields strong-but-not-SOTA results — relevant to a thesis that deliberately excludes RL and keeps SFT-distillation only.  
  *quote:* the integration of chain-of-thought reasoning shows mixed results ... The combination of CoT+LoRA adapters on the vision backbone results in performance degradation compared to the SFT variant ... our GRPO-optimised GUI-Qwen (VL) model achieves state-of-the-art results

### Nguồn #9 (chất lượng primary)
- Distilling knowledge from large VLMs into smaller, more efficient VLMs is an established, actively-pursued research direction motivated by deployment on resource-constrained devices — directly supporting the thesis's on-device niche framing.  
  *quote:* This has spurred interest in distilling knowledge from large VLMs into smaller, more efficient counterparts.
- A peer-reviewed/arXiv distillation framework (GenRecal) demonstrates that a distilled small VLM can outperform large-scale open- and closed-source VLMs on multiple benchmarks, providing precedent that student models can exceed baselines rather than merely copying the teacher.  
  *quote:* Through extensive experiments on multiple challenging benchmarks, we demonstrate that GenRecal significantly improves baseline performances, eventually outperforming large-scale open- and closed-source VLMs.
- Cross-VLM distillation faces a concrete technical challenge because different VLMs use different token vocabularies, token splits, and index orderings; naive logit distillation is therefore limited to same-family models — relevant to the thesis choosing SFT-on-teacher-text (which sidesteps this) rather than logit distillation.  
  *quote:* A key challenge arises here from the diversity of VLM architectures, which are built on different LLMs and employ varying token types-differing in vocabulary size, token splits, and token index ordering.
- GenRecal transfers knowledge via a feature-space Recalibrator adapter aligning heterogeneous VLM representations, not via curated/faithfulness-filtered teacher text — so it does not overlap with the thesis's data-curation-by-faithfulness contribution and does not scoop it.  
  *quote:* GenRecal incorporates a Recalibrator that aligns and adapts feature representations between heterogeneous VLMs, enabling effective knowledge transfer across different types of VLMs.
- The work targets general-purpose generative VLM capability rather than grounding/action prediction, confirming that distillation for image-to-text generation tasks is a legitimate research target in 2025-2026.  
  *quote:* we present Generation after Recalibration (GenRecal), a general-purpose distillation framework for VLMs.

### Nguồn #10 (chất lượng primary)
- Distilling a large VLM into small VLMs (2B and 7B) is a viable, peer-reviewed research direction explicitly motivated by deployment on resource-constrained devices like mobile platforms — directly supporting the thesis' on-device niche framing.  
  *quote:* scaling VLMs to improve performance using larger models brings significant computational challenges, especially for deployment on resource-constrained devices like mobile platforms and robots. To address this, we propose VLsI: Verbalized Layers-to-Interactions, a new VLM family in 2B and 7B model sizes, which prioritizes efficiency without compromising accuracy.
- A small distilled VLM (2B/7B) can exceed a much larger teacher-class model (GPT-4V) on vision-language benchmarks (+11.0% for 2B, +17.4% for 7B), evidence that distillation into a small student can produce value beyond mere teacher-copying (student>base, and even student>large-model).  
  *quote:* We validate VLsI across ten challenging vision-language benchmarks, achieving notable performance gains (11.0% for 2B and 17.4% for 7B) over GPT-4V without the need for model scaling, merging, or architectural changes.
- Naive output-imitation distillation (copying teacher final outputs) suffers training instability; VLsI's layer-wise verbalizer approach is proposed specifically to mitigate this, a caution relevant to the thesis' plain SFT-on-teacher-outputs recipe.  
  *quote:* This approach mitigates the training instability often encountered in output imitation and goes beyond typical final-layer tuning by aligning the small VLMs' layer-wise progression with that of the large ones.
- The current wave of open-source small VLMs is itself built by tuning on instruction samples generated by closed-source VLMs like GPT-4V, legitimizing the thesis' teacher=gpt-4o-mini data-generation strategy as standard practice.  
  *quote:* The recent surge in high-quality visual instruction tuning samples from closed-source vision-language models (VLMs) such as GPT-4V has accelerated the release of open-source VLMs across various model sizes.
- VLsI is a December 2024 peer-reviewed-track arXiv preprint targeting text-generation quality from vision inputs, using verbalizers that map each layer's features into natural-language space — a generation (not grounding/action) oriented distillation, matching the thesis' generation task axis.  
  *quote:* introducing intermediate "verbalizers" that map features from each layer to natural language space, allowing smaller VLMs to flexibly align with the reasoning processes of larger VLMs

### Nguồn #11 (chất lượng secondary)
- Knowledge distillation is an established methodology for transferring advanced capabilities from large proprietary LLMs (e.g., GPT-4) into smaller open-source models (e.g., LLaMA, Mistral), which supports the thesis's teacher(gpt-4o-mini)→student(Qwen2.5-VL-3B) distillation direction as a recognized paradigm.  
  *quote:* KD emerges as a pivotal methodology for transferring advanced capabilities from leading proprietary LLMs, such as GPT-4, to their open-source counterparts like LLaMA and Mistral.
- Data augmentation is a core paradigm within the KD framework used to generate training data that boosts student performance, which supports building a training set from teacher outputs (as the thesis proposes) rather than requiring human gold labels.  
  *quote:* DA emerges as a powerful paradigm within the KD framework to bolster LLMs' performance
- Distillation via the student employing itself/teacher enables self-improvement, supporting the thesis's framing that distillation is not mere copying but can facilitate capability gains (student > base).  
  *quote:* KD plays a crucial role in both compressing these models, and facilitating their self-improvement by employing themselves as teachers.
- The KD survey organizes the field around three pillars — algorithm, skill, and verticalization — indicating distillation applied to a specific vertical/domain (e.g., GUI instruction generation) is a recognized contribution axis, useful for framing the thesis's niche.  
  *quote:* The survey organizes distillation around "algorithm, skill, and verticalization" examining "KD mechanisms, the enhancement of specific cognitive abilities, and their practical implications across diverse fields."

### Nguồn #12 (chất lượng primary)
- LLM self-improvement can operate without gold labels via a verify-filter-distill loop where the model verifies its own outputs, filters/reweights data on that verification, and distills the filtered data.  
  *quote:* the model verifies its own outputs, filters or reweights data based on this verification, and distills the filtered data
- The capacity for self-improvement from self-generated filtered data is governed by a formal quantity called the generation-verification gap — i.e., improvement is bounded by how much better the model can verify than generate.  
  *quote:* a quantity which we formalize as the generation-verification gap
- A variant of the generation-verification gap scales monotonically with model pre-training FLOPs, implying verification-driven self-improvement headroom grows with model scale (and is limited for small models).  
  *quote:* a variant of the generation-verification gap scales monotonically with the model pre-training flops

### Nguồn #13 (chất lượng primary)
- Hallucination can be measured without gold-standard answers by using off-the-shelf reference LLMs as a proxy for gold answers, with a weighting scheme (FEWL) that quantifies each reference LLM's expertise to avoid naively trusting them.  
  *quote:* FEWL (Factualness Evaluations via Weighting LLMs) ... leverages the answers from off-the-shelf LLMs that serve as a proxy of gold-standard answers
- The reference-LLM-as-proxy measure can be used downstream to reduce hallucination through both in-context learning and supervised fine-tuning, i.e., a no-gold signal can drive training-time improvement.  
  *quote:* reduce hallucination through both in-context learning and supervised fine-tuning
- FEWL was validated on the TruthfulQA, CHALE, and HaluEval benchmarks and gives more accurate hallucination measures than naively averaging multiple reference LLMs.  
  *quote:* experiments on Truthful-QA, CHALE, and HaluEval datasets demonstrate the effectiveness of FEWL ... gives more accurate hallucination measures than naively using reference LLMs
- The method and its evidence are for text-only LLM factual QA, not multimodal/VLM screenshot-to-instruction generation, so it only transfers to the thesis by analogy (no direct GUI/VLM evidence).  
  *quote:* This is a text-only LLM study focused on factual hallucination in question-answering tasks. No multimodal/VLM applications are mentioned.

### Nguồn #14 (chất lượng primary)
- Synthetic data generated by an LLM teacher outperforms crowdsourced human-written data for reducing hallucination in fine-tuned models, supporting a no-human-gold, teacher-generated training-data approach.  
  *quote:* we demonstrate that synthetic data generated by LLMs outperforms crowdsourced data in reducing hallucination in finetuned models
- Self-training (fine-tuning a model on its own outputs) achieves hallucination reduction comparable to knowledge distillation from a stronger teacher (e.g., GPT-4o), i.e., distilling from a bigger teacher is not strictly necessary for the hallucination-reduction gain.  
  *quote:* We also compare self-training (fine-tuning models on their own outputs) and knowledge distillation (fine-tuning on stronger models' outputs, e.g., GPT-4o), and find that self-training achieves comparable hallucination reduction.
- The surprising near-parity of self-training with distillation is attributed to increased exposure-bias issues in the distillation setting, a documented risk when training a student on a teacher's outputs.  
  *quote:* We conjecture that this surprising finding can be attributed to increased exposure bias issues in the knowledge distillation case and support this conjecture with post hoc analysis.
- Scalable, cost-efficient QA systems can be built with synthetic data plus open-source (small) models, reducing reliance on proprietary/costly tools — evidence for the small-open-model, cost-constrained niche.  
  *quote:* These findings show that scalable, cost-efficient QA systems can be built using synthetic data and self-training with open-source models, reducing reliance on proprietary tools or costly human annotations.
- The pipeline improves robustness to unanswerable questions and retrieval failures via contextualized "I don't know" responses — a faithfulness-preserving abstention mechanism analogous to a fallback for un-verifiable steps.  
  *quote:* We also improve robustness to unanswerable questions and retrieval failures with contextualized "I don't know" responses.

### Nguồn #15 (chất lượng primary)
- General-domain VLMs lack mobile-UI-specific capabilities, motivating domain-specific fine-tuning/pretraining for UI understanding tasks.  
  *quote:* these VLMs are typically pre-trained on general-domain data, which often results in a lack of fundamental capabilities specific to the mobile domain
- MobileVLM adds two extra UI-focused pre-training stages with four UI-based tasks to improve both intra-UI and inter-UI understanding.  
  *quote:* two additional pre-training stages to enhance both intra- and inter-UI understanding
- A domain-adapted VLM for UI outperforms existing general VLMs on mobile benchmarks, evidencing that UI-specialized training yields measurable gains.  
  *quote:* Experimental results show MobileVLM excels on both our test set and public mobile benchmarks, outperforming existing VLMs.
- MobileVLM relies on a purpose-built 3-million-page Chinese UI dataset (Mobile3M), i.e. large-scale domain pretraining rather than teacher-distillation from a small curated set — a scale not feasible on a ~$100-150 Colab budget.  
  *quote:* Mobile3M from scratch, which contains 3 million UI pages, and real-world transition actions, forming a directed graph structure

### Nguồn #16 (chất lượng primary)
- Fine-tuning small VLMs (2B-7B) on dense/complex captions containing content not grounded in the model's pre-existing knowledge increases hallucination; adapting training captions to the model's existing capabilities reduces it.  
  *quote:* fine-tuning on content not grounded in a model's pre-existing factual-knowledge can lead to an increase in hallucinations
- A data-centric filtering/adaptation approach (KnowAda) that removes ungrounded information from teacher/annotated captions consistently reduces the contradiction (hallucination) rate across multiple fine-tuned small models while keeping descriptiveness.  
  *quote:* KnowAda "consistently reduces the contradiction rate...across different trained models" for both human and synthetic captions
- Curating training data by filtering out unfaithful content trades off faithfulness against descriptiveness: it lowers descriptiveness recall but not precision.  
  *quote:* reducing contradictions decreases descriptiveness recall (though not precision)
- Small VLMs including PaliGemma-3B and TinyLLaVA-2.4B can be effectively fine-tuned for image-to-text description tasks in the exact 2B-7B parameter range relevant to on-device small generators.  
  *quote:* Models Fine-tuned (2B-7B parameter range): LLaVA-1.5-7B, PaliGemma (3B), TinyLLaVA (2.4B)
- The method uses an LLM/VLM-generated question-answer probing loop plus an LLM rewriter to adapt captions, demonstrating an automated no-human-gold pipeline for producing faithfulness-filtered training data.  
  *quote:* Caption Adaptation: Use an LLM to remove information corresponding to unknown questions

### Nguồn #17 (chất lượng primary)
- Supervised (offline) knowledge distillation suffers from a distribution mismatch between training on a static teacher-generated dataset and inference over the student's own outputs — directly relevant to the thesis's SFT-distillation-on-static-teacher-outputs plan.  
  *quote:* supervised KD suffers from 'a distribution mismatch between training with a static dataset and inference over final student-generated outputs,' while on-policy KD struggles with low-quality examples unfamiliar to teacher models
- Speculative Knowledge Distillation (SKD) improves over standard KD by having student and teacher cooperate to generate high-quality training data on-the-fly aligned with the student's inference-time distribution, rather than using purely static teacher outputs.  
  *quote:* cooperation between student and teacher models to generate high-quality training data on-the-fly while aligning with the student's inference-time distribution
- SKD consistently outperforms existing KD methods across different domains, data sizes, and model initialization strategies, evaluated on translation, summarization, math, and instruction-following.  
  *quote:* SKD 'consistently outperforms existing KD methods across different domains, data sizes, and model initialization strategies.'

### Nguồn #18 (chất lượng primary)
- LoRA substantially underperforms full fine-tuning in standard low-rank settings on target domains (programming and math), meaning LoRA 'learns less' new domain capability.  
  *quote:* LoRA "substantially underperforms full finetuning" in standard low-rank settings on target domains (programming and math)
- LoRA better preserves out-of-domain / base-model capabilities (forgets less) and does so more effectively than common regularizers like weight decay and dropout.  
  *quote:* LoRA "mitigates forgetting more than common regularization techniques such as weight decay and dropout" while maintaining more diverse generation outputs on out-of-domain tasks.
- Full fine-tuning learns weight perturbations of much higher rank (10-100x) than typical LoRA configurations, implying low ranks may be insufficient for large capability shifts.  
  *quote:* Full finetuning learns perturbations with ranks 10-100X greater than typical LoRA configurations
- The paper is peer-reviewed, published in TMLR (August 2024) with Featured Certification, and studies LoRA on instruction fine-tuning (~100K pairs) and continued pretraining (20B tokens).  
  *quote:* Venue: Transactions on Machine Learning Research (Featured Certification); Acceptance Date: August 2024 ... instruction finetuning (~100K pairs) and continued pretraining (20B tokens) scenarios.

### Nguồn #19 (chất lượng primary)
- ALLaVA distills a proprietary large VLM (GPT-4V) into a lite (~3B/4B-scale) vision-language model by using GPT-4V to synthesize both fine-grained image captions and reasoning VQA pairs — directly supporting the feasibility of SFT-distillation of a large VLM into a small one for image→text tasks.  
  *quote:* leverage strong proprietary models to generate (i) fine-grained image annotations for vision-language alignment and (ii) complex reasoning visual question-answering pairs for visual instruction fine-tuning.
- A small (4B-class) student VLM trained purely on GPT-4V-synthesized data reaches competitive performance on 17 benchmarks and can match 7B/13B models, evidence that a distilled small student can be strong rather than merely a weak teacher-copy.  
  *quote:* achieve competitive performance on 17 benchmarks among 4B LVLMs, and even perform on par with 7B/13B-scale models.
- The training set consists of 1.3M teacher-generated synthetic samples with no human-authored gold labels, showing teacher-synthesized data at scale is a viable substitute for human annotation.  
  *quote:* 1.3M samples in total
- The stated contribution is that high-quality synthetic training data alone can close the gap between full-scale and resource-friendly lite VLMs — a framing usable to argue on-device small-model distillation is a real contribution.  
  *quote:* bridge the performance gap between traditional-scale LVLMs and resource-friendly lite versions by adopting high-quality training data.
- The paper's abstract does not report training configuration or compute requirements, so Colab-feasibility (VRAM/time) for the thesis must be sourced elsewhere.  
  *quote:* The abstract does not specify model size details, training configuration, batch sizes, learning rates, or compute infrastructure requirements.

### Nguồn #20 (chất lượng primary)
- DreamStruct is peer-reviewed evidence (ECCV 2024) that models can be trained to understand and describe GUI/UI elements and slides using synthetic labeled data plus only a small number of human-annotated examples, supporting the feasibility of training small models for GUI understanding without large human-gold datasets.  
  *quote:* we present a method to generate synthetic, structured visuals with target labels using code generation ... create datasets with built-in labels and train models with a small number of human-annotated examples
- DreamStruct's synthetic training data is produced by CODE GENERATION (deterministic, built-in labels), not by distilling outputs from a large teacher VLM — a different data-creation mechanism than SFT-distillation from gpt-4o-mini, so it does not scoop the thesis's teacher-distillation-with-faithfulness-filtering approach.  
  *quote:* To overcome this challenge, we present a method to generate synthetic, structured visuals with target labels using code generation.
- DreamStruct's tasks are recognizing, describing, and classifying visual elements of UIs/slides — GUI understanding/perception rather than generating step-by-step usage instructions from a use-case question, so the generation task in the thesis remains distinct.  
  *quote:* The paper demonstrates improvements across three understanding tasks: Recognizing visual elements, Describing visual content, Classifying visual content types
- The paper motivates synthetic-data training by the cost of manual GUI/slide annotation, echoing the thesis premise that human-authored gold guidance is unavailable and must be substituted by generated/curated data.  
  *quote:* achieving such understanding computationally has required manual data collection and annotation, which is time-consuming and labor-intensive

## 4. Kết quả VERIFY (57 phiếu — refuted=true nghĩa là claim bị BÁC)
- refuted=**False** · confidence=high — Claim is directly supported by the primary source. LLaVA-KD (Cai et al., ICCV 2025; arXiv 2410.16236) is a genuine peer-reviewed CVF paper. The supporting quote "significantly improves s-MLLMs performance without altering the model architecture" is verbatim from its abstract. The paper's framework (
- refuted=**False** · confidence=high — The source is a genuine peer-reviewed ICCV 2025 paper (Cai et al., "LLaVA-KD", arXiv 2410.16236, CVF Open Access proceedings, official GitHub Fantasyele/LLaVA-KD, HuggingFace/Semantic Scholar all confirm). The supporting quote — "significantly improves s-MLLMs performance without altering the model 
- refuted=**False** · confidence=high — The claim is a faithful paraphrase of the peer-reviewed ICCV 2025 abstract (Cai et al., LLaVA-KD, arXiv 2410.16236), which states verbatim "significantly improves s-MLLMs performance without altering the model architecture." Source is a CVF primary proceedings paper, current (2025), peer-reviewed, n
- refuted=**False** · confidence=medium — Primary source 2406.14056 is titled "VGA: Vision GUI Assistant — Minimizing Hallucinations through Image-Centric Fine-Tuning." Abstract confirms: existing LVLMs "overly depend on internal knowledge and neglect image content, resulting in hallucinations" in GUI comprehension; VGA is a fine-tuned mode
- refuted=**False** · confidence=medium — Paper 2406.14056 is genuinely titled "VGA: Vision GUI Assistant — Minimizing Hallucinations through Image-Centric Fine-Tuning" (verified via arXiv listing). Its abstract states exactly what the claim asserts: "Existing LVLMs often overly depend on internal knowledge and neglect image content, result
- refuted=**False** · confidence=high — Verified: arXiv 2406.14056 = "VGA: Vision GUI Assistant — Minimizing Hallucinations through Image-Centric Fine-Tuning," published in Findings of EMNLP 2024 (peer-reviewed, ECNU). The paper is explicitly GUI-specific and fine-tunes a VLM (LLaVA-based) via a two-stage FAC method plus a 63.8k VQA datas
- refuted=**False** · confidence=high — Claim CONFIRMED. arXiv 2406.14056 = "VGA: Vision GUI Assistant — Minimizing Hallucinations through Image-Centric Fine-Tuning", ACCEPTED at EMNLP 2024 (peer-reviewed, not just preprint). The supporting quote is accurate and verified: they construct a 63.8k-example VQA dataset via the "Referent Method
- refuted=**False** · confidence=high — Claim is well-supported and current. VLsI (arXiv 2412.01822) is confirmed accepted to CVPR 2025 (verified via CVPR virtual poster page cvpr.thecvf.com/virtual/2025/poster/34531 and NVIDIA Research Taiwan publication page) — so "peer-reviewed" holds, not merely a preprint. The supplied quote directly
- refuted=**False** · confidence=high — Primary source confirmed: arXiv 2406.14056 = "VGA: Vision GUI Assistant — Minimizing Hallucinations through Image-Centric Fine-Tuning" (Meng, Dai, Gong, Guo, Tang, Wei), published at EMNLP 2024 (peer-reviewed). The paper constructs a 63.8k-example VQA dataset via a proposed "Referent Method" that "e
- refuted=**False** · confidence=high — Claim verified against primary source. arXiv 2406.14056 = "VGA: Vision GUI Assistant -- Minimizing Hallucinations through Image-Centric Fine-Tuning" (Meng et al., ECNU). The supporting quote accurately reflects the paper: it constructs a 63.8k-example VQA dataset via the "Referent Method" to make re
- refuted=**False** · confidence=high — VLsI (arXiv 2412.01822) is NOT merely a preprint — it was accepted to CVPR 2025 (confirmed via NVIDIA Research Taiwan publication page research.nvidia.com/labs/twn/publication/cvpr_2025_vlsi/ and cvpr.thecvf.com/virtual/2025/poster/34531). So "peer-reviewed" is accurate at a top-tier venue. The supp
- refuted=**False** · confidence=high — VLsI (arXiv 2412.01822) is peer-reviewed — accepted as a CVPR 2025 poster (cvpr.thecvf.com/virtual/2025/poster/34531), not just a preprint. The supporting quote verbatim states the motivation is "deployment on resource-constrained devices like mobile platforms and robots" and proposes "2B and 7B mod
- refuted=**False** · confidence=high — The primary source arXiv 2506.15681 (GenRecal: "Generation after Recalibration from Large to Small Vision-Language Models") genuinely concerns distilling large VLMs into smaller efficient ones for resource-constrained deployment; the quote accurately reflects its motivation. The claim is corroborate
- refuted=**False** · confidence=high — The claim is modest and directly matched by the supporting quote ("This has spurred interest in distilling knowledge from large VLMs into smaller, more efficient counterparts") — no overreach. It is strongly corroborated by an abundance of peer-reviewed/arXiv work: PromptKD (CVPR 2024, CLIP teacher→
- refuted=**True** · confidence=medium — The +11.0%/+17.4% numbers are real and peer-reviewed (VLsI, CVPR 2025), but the claim misreads them. VLsI is "Verbalized Layers-to-Interactions from LARGE to SMALL VLMs": the distillation TEACHER is a larger VLM in the same family, and GPT-4V is only an external benchmark baseline, NOT the teacher. 
- refuted=**False** · confidence=high — Claim is modest and well-supported by the quote and independent peer-reviewed literature. VLM->smaller-VLM distillation is a demonstrably active direction: EfficientVLM (arXiv:2210.07795, retains 98.4% perf at 44.3% params, 2.2x speedup), LLaVA-KD (2024), ALIGN-KD (cross-modal distillation for MOBIL
- refuted=**True** · confidence=medium — MISREAD OF TEACHER-STUDENT (primary refutation): In VLsI (arxiv 2412.01822, CVPR 2025), GPT-4V is NOT the teacher — it is only a benchmark leaderboard baseline. The actual teacher is a LARGER open VLM ("align with the reasoning processes of larger VLMs" via verbalized layer-wise distillation). Confi
- refuted=**True** · confidence=medium — The quote's literal numbers (+11.0%/2B, +17.4%/7B over GPT-4V) are real and from a solid venue (VLsI, CVPR 2025 — peer-reviewed, not a preprint), so source quality/recency are NOT the problem. The problem is the claim's interpretation. (1) GPT-4V is NOT VLsI's teacher. VLsI does layer-wise 'verbaliz
- refuted=**False** · confidence=high — Claim is well-supported by the primary source (arXiv 2402.11684, ALLaVA: Harnessing GPT4V-Synthesized Data for Lite Vision-Language Models). WebSearch confirms: ALLaVA uses GPT-4V to synthesize (i) fine-grained image annotations for alignment and (ii) complex reasoning VQA pairs for instruction fine
- refuted=**False** · confidence=high — The claim is accurately supported by the primary source. ALLaVA (arXiv 2402.11684, "Harnessing GPT4V-Synthesized Data for Lite Vision-Language Models") uses GPT-4V to synthesize (i) fine-grained image captions for vision-language alignment and (ii) complex reasoning VQA pairs for visual instruction 
- refuted=**True** · confidence=medium — GenRecal (arXiv 2506.15681, Jun 2025) is a real large→small VLM distillation paper whose abstract does say it ends up "outperforming large-scale open- and closed-source VLMs" — so the surface quote checks out. BUT the claim overreaches: "outperforming large-scale VLMs" means beating OTHER large mode
- refuted=**False** · confidence=medium — Claim is supported. Primary source arXiv 2506.15681 (GenRecal, Byung-Kwan Lee/KAIST+NVIDIA) abstract states verbatim: "significantly improves baseline performances, eventually outperforming large-scale open- and closed-source VLMs." Source quality is high: NVIDIA Research page (research.nvidia.com/l
- refuted=**False** · confidence=high — Claim is directly supported by the primary source. Paper title: "ALLaVA: Harnessing GPT4V-Synthesized Data for Lite Vision-Language Models" (arXiv 2402.11684). Teacher=GPT-4V, student=lite VLM at 3B/4B scale (confirmed model FreedomIntelligence/ALLaVA-3B; paper reports competitive results "up to 3B"
- refuted=**True** · confidence=medium — GenRecal (arXiv 2506.15681, ECCV 2026) abstract does say it "eventually outperform[s] large-scale open- and closed-source VLMs," but the results tables refute the claim's operative use. (1) Cherry-picked: GenRecal-8B scores 68.1 on the headline MMMU benchmark vs GPT-4o 69.1 and Claude-3.5 Sonnet 68.
- refuted=**True** · confidence=medium — ALLaVA (arXiv 2402.11684) is a NON-peer-reviewed preprint (confirmed: arXiv v1/v2 Feb 2024; HF papers page and ADS show no conference/journal venue), yet the research question explicitly demands peer-reviewed evidence — source strength is insufficient for a strong 'can match 7B/13B' claim. The liter
- refuted=**False** · confidence=medium — Claim is verbatim-supported by the ALLaVA primary source (arXiv 2402.11684, FreedomIntelligence). Abstract states: "achieve competitive performance on 17 benchmarks among 4B LVLMs, and even perform on par with 7B/13B-scale models" — direct match. No contradicting source found; the finding is unconte
- refuted=**False** · confidence=medium — The quote is a verbatim sentence from the abstract of arxiv 2502.19545 ("Winning Big with Small Models: Knowledge Distillation vs. Self-Training for Reducing Hallucination in Product QA Agents", Lewis et al., Ohio State + Mitsubishi Electric / MERL TR2025-114, Feb 2025). The claim is therefore direc
- refuted=**True** · confidence=medium — arXiv 2402.11684 (ALLaVA) is a non-peer-reviewed preprint (v2 June 2024; no venue found), and the RQ prioritizes peer-reviewed evidence. The "match 7B/13B" figure is the authors' OWN abstract self-report, and the original wording hedges "on par with 7B/13B-scale models ON VARIOUS BENCHMARKS" — the c
- refuted=**True** · confidence=medium — The quote is genuine (arXiv 2502.19545, "Winning Big with Small Models," ACL 2025 GEM workshop / MERL TR2025-114), but the claim overgeneralizes and misframes it. (1) Single-domain: the synthetic-beats-crowdsourced result comes ONLY from text RAG QA over one Samsung Smart TV user manual — not multi-
- refuted=**True** · confidence=medium — The quote IS in arxiv 2502.19545, but the claim over-generalizes a single narrow study. (1) DOMAIN MISMATCH: the paper is text-only grounded RAG QA over ONE document (Samsung Smart TV manual), where synthetic answers are generated with the source doc in context (hence grounded), and "crowdsourced" a
- refuted=**False** · confidence=high — Claim is a faithful restatement of the primary-source abstract (arXiv 2402.10412, "Measuring and Reducing LLM Hallucination without Gold-Standard Answers", FEWL method). Abstract verbatim: "We also show how to leverage FEWL to reduce hallucination through both in-context learning and supervised fine
- refuted=**True** · confidence=medium — The quote is accurate and the paper (arXiv 2502.19545 = MERL TR2025-114, "Winning Big with Small Models," Lewis et al.) genuinely reports self-training ≈ GPT-4o distillation for hallucination reduction. BUT: (1) the setting is TEXT-ONLY retrieval-augmented product-QA (Samsung TV manual) — not multim
- refuted=**False** · confidence=high — Claim is verbatim from the abstract of arXiv 2402.10412 "Measuring and Reducing LLM Hallucination without Gold-Standard Answers" (FEWL, Wei/Yao/Ton/Guo/Estornell/Liu). Abstract: "We also show how to leverage FEWL to reduce hallucination through both in-context learning and supervised fine-tuning," v
- refuted=**True** · confidence=medium — The quote is real, but the claim overreaches. Source 2502.19545 ("Winning Big with Small Models: Knowledge Distillation vs. Self-Training for Reducing Hallucination in Product QA Agents") studies TEXT-ONLY, retrieval-augmented product QA (Samsung Smart TV manuals) — NOT vision-language, image captio
- refuted=**True** · confidence=medium — Quote is verbatim-faithful to arXiv 2502.19545 (MERL "Winning Big with Small Models"), but the claim overreaches: the paper's domain is text-only retrieval-augmented product QA (Samsung Smart TV manual), NOT multimodal/vision-language/GUI generation — so it gives zero evidence for the thesis's VLM s
- refuted=**False** · confidence=high — Paper 2402.10412 is "Measuring and Reducing LLM Hallucination without Gold-Standard Answers" (FEWL). Its abstract states verbatim: "FEWL leverages the answers from off-the-shelf LLMs that serve as a proxy of gold-standard answers" and "We also show how to leverage FEWL to reduce hallucination throug
- refuted=**False** · confidence=medium — Primary source arXiv 2412.02674 (Song, Zhang, Eisenach, Kakade, Foster, Ghai — "Mind the Gap: Examining the Self-Improvement Capabilities of LLMs", Dec 2024) states verbatim that self-improvement is "largely governed by a quantity which we formalize as the generation-verification gap," and reports i
- refuted=**False** · confidence=high — arxiv 2412.02674 "Mind the Gap: Examining the Self-Improvement Capabilities of Large Language Models" (Song, Zhang, Eisenach, Kakade, Foster, Ghai; ICLR 2025) formalizes the "generation-verification gap" as the quantity governing self-improvement from self-generated, verified/filtered, then distille
- refuted=**False** · confidence=high — Claim is accurately supported by the primary source, which is peer-reviewed (NAACL 2025 long paper, aclanthology 2025.naacl-long.527; arXiv 2411.09018v3), titled "Bridging the Visual Gap: Fine-Tuning Multimodal Models with Knowledge-Adapted Captions." Verbatim quote: "fine-tuning on content not grou
- refuted=**False** · confidence=high — Primary source arXiv 2412.02674 ("Mind the Gap: Examining the Self-Improvement Capabilities of LLMs") abstract confirms the claim: self-improvement is "largely governed by a quantity which we formalize as the generation-verification gap." The exact supporting quote is verbatim. No contradicting sour
- refuted=**False** · confidence=high — Claim matches primary source arXiv 2411.09018v3 (KnowAda / "Bridging the Visual Gap"), which fine-tunes exactly 2B-7B VLMs (PaliGemma 3B, TinyLLaVA 2.4B, LLaVA-7B) on DOCCI/PixelProse and reports both directions of the claim: ungrounded/complex captions increase hallucination ("fine-tuning on conten
- refuted=**False** · confidence=high — Claim is directly supported by primary source arXiv:2411.09018v3 "Bridging the Visual Gap: Fine-Tuning Multimodal Models with Knowledge-Adapted Captions" (KnowAda). The paper tests exactly the claimed 2B-7B range (PaliGemma-3B, TinyLLaVA-2.4B, LLaVA-1.5-7B) and states: "fine-tuning on content not gr
- refuted=**False** · confidence=high — Primary source arXiv 2411.09018v3 (KnowAda) states verbatim: "fine-tuning on KnowAda captions consistently reduces the hallucination rate while maintaining high descriptiveness across different trained models." It further reports KnowAda "significantly reduces the contradiction rate in terms of both
- refuted=**False** · confidence=high — Primary source arXiv 2411.09018v3 directly supports the claim with near-verbatim text: "fine-tuning on KnowAda captions consistently reduces the hallucination rate while maintaining high descriptiveness across different trained models" and "KnowAda significantly reduces the contradiction rate in ter
- refuted=**False** · confidence=high — Claim is supported by a peer-reviewed primary source: KnowAda "Bridging the Visual Gap: Fine-Tuning Multimodal Models with Knowledge-Adapted Captions," NAACL 2025 Oral (ACL Anthology 2025.naacl-long.527; arXiv 2411.09018v3). Paper explicitly states fine-tuning on KnowAda captions "consistently reduc
- refuted=**True** · confidence=medium — Primary source (arxiv abstract 2511.08172, "An Efficient Training Pipeline for Reasoning GUI Agents") confirms only the skeleton: 4.8M→12K curated, a 3B VLM, and "match or surpass larger baselines" on ScreenSpot/Multimodal-Mind2Web/AndroidControl. But the claim adds several unsupported specifics NOT
- refuted=**True** · confidence=high — Verified against the verbatim abstract of arXiv 2511.08172 ("An Efficient Training Pipeline for Reasoning GUI Agents," Pantazopoulos & Özyiğit, Nov 2025, v3). Two independent misreads refute the claim as worded: (1) FABRICATED "7B" — the abstract says only "larger baselines" and gives NO parameter s
- refuted=**False** · confidence=high — Primary source (arXiv 2511.08172, "An Efficient Training Pipeline for Reasoning GUI Agents") lists contribution (i) as "a detailed filtering method for curating misaligned synthetic data ... using the same base-model as a critic for GUI training instances" — directly supporting "data curation framed
- refuted=**True** · confidence=medium — The core facts check out against arXiv:2511.08172 ("An Efficient Training Pipeline for Reasoning GUI Agents", Pantazopoulos & Özyiğit): a 3B VLM (Qwen-VL family) is LoRA-trained on 12K instances curated from 4.8M synthetic examples, on ScreenSpot / Multimodal-Mind2Web / AndroidControl. But the stron
- refuted=**False** · confidence=high — Primary source arXiv 2511.08172v1 (HTML) confirms every component verbatim. Stated contributions: "(i) a detailed filtering method for curating misaligned synthetic data stemming from data generation pipelines using the same base-model as a critic for GUI training instances; (ii) a unified framework
- refuted=**False** · confidence=high — Claim verified verbatim against primary source arXiv 2511.08172v3 (§3.2). Every component confirmed: base VLM difficulty scoring = "We utilise Qwen-2.5-VL-3B in a zero-shot setting and generate bounding box predictions... otherwise the example is considered hard"; alignment ranker = "we train a rank
- refuted=**False** · confidence=high — Quote verified verbatim in BLIP abstract (arXiv 2201.12086, Li et al., ICML 2022 — peer-reviewed): "bootstrapping the captions, where a captioner generates synthetic captions and a filter removes the noisy ones." CapFilt is genuinely a dataset-bootstrapping method that generates synthetic captions t
- refuted=**True** · confidence=medium — arXiv:2511.08172 ("An Efficient Training Pipeline for Reasoning Graphical User Interface Agents", Pantazopoulos & Özyiğit, Nov 2025) literally DOES use GPT-4o mini both to generate CoT traces and as a post-processing filter, and trains a 3B VLM — so the raw facts hold. BUT the claim overreaches: (1)
- refuted=**False** · confidence=high — BLIP (arXiv 2201.12086, ICML 2022 spotlight — peer-reviewed) does introduce CapFilt: a learned captioner generates synthetic captions for web images and a learned filter (image-grounded text encoder finetuned with ITC/ITM) removes texts the ITM head predicts as unmatched to the image ("noisy"). The 
- refuted=**True** · confidence=medium — arxiv 2511.08172 ("An Efficient Training Pipeline for Reasoning GUI Agents", Pantazopoulos & Ozyigit, Alan Turing Institute, Nov 2025) is an arXiv PREPRINT, not peer-reviewed — so "peer-reviewed-style GUI work" is a misleading hedge that cannot serve as peer-reviewed precedent. The dual GPT-4o-mini 
- refuted=**True** · confidence=medium — Primary source arXiv:2511.08172v3 ("An Efficient Training Pipeline for Reasoning GUI Agents", Pantazopoulos & Ozyigit, Alan Turing Institute, submitted Nov 2025) verbatim confirms the two factual sub-claims: "we provide chain-of-thought traces derived from GPT-4o mini" and "we apply a post-processin
- refuted=**False** · confidence=high — The claim is accurately supported by the primary source (BLIP, Li et al., ICML 2022, arXiv 2201.12086). The abstract states verbatim: "a captioner generates synthetic captions and a filter removes the noisy ones." The paper body confirms the mechanism precisely: the captioner produces synthetic capt

---
## RESUME CHECKPOINT (lần sau bắt đầu từ đây)
- **ĐÃ XONG (không cần chạy lại):** deep-research #1 + 3 vòng debate + chốt hướng **Faithful Distillation** + 8 điều kiện → **`report/50` §1–§9** (nguồn-sự-thật). Ràng buộc: ≥1 model là chính, eval phụ, <3 tháng, đề tài cố định.
- **deep-research #2 (`wf_45ce881b`):** workflow TREO ở synthesis cuối, NHƯNG **verify đã xong (39 claim SỐNG / 18 bác)** → tôi đã trích tay các claim sống và **gấp trụ citation vào `report/43` Chương 0 §0.11** (VGA EMNLP24, KnowAda NAACL25, BLIP-CapFilt ICML22, ALLaVA, LLaVA-KD ICCV25, VLsI CVPR25, FEWL, Mind-the-Gap ICLR25). → **KHÔNG cần resume workflow nữa.** (Nếu vẫn muốn synthesis gọn: resume `wf_45ce881b` — cache replay.)
- **✅ ĐÃ XONG (2026-07-09):** **`report/43` CHƯƠNG 0 đã VIẾT LẠI** theo Faithful Distillation (sơ đồ, model+train, quy trình lọc, estimand, chống vòng lặp, lịch <3 tháng, rủi ro, citation). Phương án grounding cũ dời xuống "Phụ lục 0-CŨ". CLAUDE §0 + memory đã đồng bộ.
- **TODO lần sau (chỉ còn 2):** (1) **PILOT ~$5–20** — teacher sinh vài trăm mẫu → lọc faithfulness → SFT-LoRA Qwen2.5-VL-3B thử → đo student vs base (paired, held-out-app); (2) **chốt khung với thầy**. Sau pilot dương → scale + viết luận văn theo Chương 0.