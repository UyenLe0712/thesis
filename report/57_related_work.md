# 57 — RELATED WORK (kho luận điểm chung + 2 bản thảo tách FAIR/VCL)

> **Mục đích:** viết sẵn phần Công-trình-liên-quan cho CẢ HAI bài (FAIR = model tiếng Anh · VCL = sinh-tiếng-Việt + đánh giá).
> Soạn theo lựa chọn của user (2026-07-12): **viết chung một kho luận điểm → tách/viết-lại câu chữ cho từng bài** (chống trùng lặp).
> **Mọi citation trong file này đã verify venue/năm** (nguồn: `report/50`, `report/51`, `report/papers/`, + web-verify 2026-07-12). Preprint được gắn nhãn rõ; **KHÔNG trích preprint như trụ bình-duyệt**.
> Khi mâu thuẫn framing: `report/54` (pipeline) + `report/00` (trạng thái) thắng.

---

## PHẦN 0 — Nguyên tắc & bản đồ đặt citation

**3 luật bất biến khi viết related work:**
1. **Không bịa** venue/năm/tác giả. Peer-reviewed vs preprint phân biệt rõ. Xương sống lập luận chỉ dựa trụ bình-duyệt; preprint chỉ minh hoạ "landscape/hiện vật kỹ thuật".
2. **Mỗi theme phải có 1 câu "ta KHÁC gì"** (distinguish). Related work không phải liệt kê — nó là hàng rào phòng thủ khi giám khảo hỏi "bài này đã có người làm chưa?".
3. **Chống trùng 2 bài:** FAIR nộp trước (15/8) → **VCL trích FAIR** (self-citation, viết ở ngôi thứ ba do ẩn danh). Theme distillation/GUI-model → thuộc FAIR. Theme validate-metric/LLM-judge → thuộc VCL. Theme faithfulness-VLM = **dùng chung nhưng đóng khung khác** (FAIR: mục-tiêu-huấn-luyện; VCL: đối-tượng-đo). **Viết lại câu chữ** ở mỗi bài (FAIR tiếng Anh dễ bị quét trùng).

**Bản đồ theme → bài:**

| Theme | FAIR (model) | VCL (eval-VN) |
|---|---|---|
| T1. GUI agents & grounding (VLM nhỏ cho UI) | **Trung tâm** | nhắc 1 câu (bối cảnh) |
| T2. Chưng cất VLM lớn→nhỏ (KD) | **Trung tâm** | — |
| T3. Self-training / lọc dữ liệu tổng hợp | **Trung tâm** | nhắc (nguồn tín hiệu train) |
| T4. Ảo giác & trung thực trong VLM | **Trung tâm** (mục tiêu train) | **Trung tâm** (đối tượng đo) |
| T5. On-device / model nhỏ khả thi | **Trung tâm** (biện minh student) | — |
| T6. LoRA & quên (forgetting) | phụ (limitations) | — |
| T7. Đánh giá sinh KHÔNG-tham-chiếu | phụ (đo faithfulness) | **Trung tâm** |
| T8. Validate metric bằng bơm-lỗi | nhắc | **Trung tâm** |
| T9. LLM-as-judge & tính hợp lệ | nhắc | **Trung tâm** |
| T10. Sắp-thứ-tự nhiều-màn (Stage-0) | **HOÃN** → bài mở rộng sau | — |

> ⚠️ **T10 (nhiều-màn) đã HOÃN khỏi mùa này** (report/00 §4). Chỉ đưa vào related-work của **bài tiếng-Anh-mở-rộng tương lai**, KHÔNG vào FAIR/VCL mùa này. Giữ ở PHẦN 3 để không mất công verify lại.

---

## PHẦN 1 — KHO LUẬN ĐIỂM THEO THEME (dùng cho cả 2 bài)

Mỗi theme: *(a) prior work làm gì · (b) citation đã-verify · (c) TA KHÁC gì.*

### T1. GUI agents & visual grounding bằng VLM nhỏ
**(a)** Dòng GUI-agent 2024–2026 fine-tune VLM để **định vị/bấm nút** trên ảnh màn hình: dự đoán toạ độ (point-in-bbox) hoặc hành động, chấm bằng **quỹ đạo/nhãn vàng** có sẵn.
**(b) Trụ bình-duyệt:**
- **SeeClick** (Cheng et al., **ACL 2024**) — grounding point-in-bbox + benchmark ScreenSpot gốc.
- **OS-Atlas / ScreenSpot-v2** (Wu et al., **ICLR 2025**) — sửa 11–32% lỗi nhãn ScreenSpot, foundation grounding.
- **UI-R1** (Lu et al., **AAAI 2026**) — GRPO trên Qwen2.5-VL-3B, reward `R_type+R_coord+R_format`, **chỉ 136 mẫu → +22,1% ScreenSpot**.
- **SE-GUI** (**NeurIPS 2025**) — GRPO data-efficient (~3k mẫu), SOTA-scale-7B.
- **GUI-Actor** (Wu et al., Microsoft, **NeurIPS 2025**) — action-head coordinate-free + **grounding verifier train riêng**; biến thể LiteTrain đóng-băng-backbone 19–103M tham số.
- **ZonUI-3B / Qwen-GUI-3B** (**WACV 2026**) — LoRA Qwen2.5-VL-3B (r=8, α=16) trên **1 GPU 24GB, ~24K mẫu → 86,4% ScreenSpot-v2**.
- **VGA: Vision GUI Assistant** (Meng et al., **Findings of EMNLP 2024**) — fine-tune VLM nhỏ cho GUI, **trực tiếp giảm ảo giác** bằng image-centric SFT.
- **MobileVLM** (**Findings of EMNLP 2024**) — pretrain VLM chuyên UI (Mobile3M) vượt VLM tổng quát về hiểu UI.
- *Preprint (hiện vật):* InfiGUI-R1-3B, GUI-AIMA-3B, ReGUIDE, LiteGUI — chỉ dùng làm template kỹ thuật, **không làm trụ**.
**(c) TA KHÁC:** tất cả prior-art trên là **agent-bấm-máy CÓ gold** (định vị/hành động chấm bằng nhãn vàng). Ta **sinh hướng dẫn từng-bước CHO NGƯỜI ĐỌC**, tác vụ **KHÔNG có gold tutorial**, và đóng góp đặt ở **lọc-trung-thực + model on-device sinh chữ**, không ở độ chính xác grounding. Càng nhiều bài grounding LoRA→GRPO càng chứng minh **wedge của ta nằm ở tác-vụ-sinh-no-gold**, không cạnh tranh cùng sân leaderboard.

### T2. Chưng cất VLM lớn → nhỏ (knowledge distillation)
**(a)** Chuyển năng lực từ VLM lớn/đóng (teacher) sang VLM nhỏ (student) qua SFT trên dữ liệu teacher-sinh, **không đổi kiến trúc**; nhiều bài chứng minh student vượt base, thậm chí vượt model lớn hơn.
**(b) Trụ bình-duyệt:**
- **LLaVA-KD** (Cai et al., **ICCV 2025**, arXiv 2410.16236) — khung 3-giai-đoạn distill MLLM lớn→nhỏ, **"significantly improves s-MLLMs performance without altering the model architecture"**.
- **VLsI** (**CVPR 2025**, arXiv 2412.01822) — distill lớn→nhỏ cho VLM **sinh** (2B/7B), +11,0%/+17,4% so GPT-4V, tránh imitation-instability.
- **DreamStruct** (**ECCV 2024**) — fine-tune VLM nhỏ (LLaVA-1.5-13B) trên dữ liệu **teacher-sinh, KHÔNG human gold** cho UI/slide → vượt base + baseline caption-người. *Tiền lệ gần nhất về framing.*
- **BLIP / CapFilt** (Li et al., **ICML 2022**, spotlight) — captioner sinh caption tổng hợp + **filter loại caption nhiễu** → cấu trúc y hệt "teacher sinh + lọc-bịa" của ta.
- *Preprint (bổ trợ):* ALLaVA (GPT-4V→lite VLM), GenRecal (distill sinh, Recalibrator), KD survey (2402.13116) — **nhãn preprint**.
**(c) TA KHÁC:** distillation trần KHÔNG mới. Ta khác ở **tín hiệu lọc = nguồn NGOÀI có cấu trúc (View Hierarchy), không self-consistency**, và áp cho **hành vi rủi-ro-cao** (gọi sai tên nút thật → dẫn người bấm nhầm). DreamStruct/VGA làm captioning/recognition; ta làm **sinh hướng-dẫn-thao-tác từng-bước** + có **vòng lọc-faithfulness đối-chiếu-VH** — đó là điểm mới.

### T3. Self-training / bootstrapping / lọc dữ liệu tổng hợp không-gold
**(a)** Model sinh dữ liệu → **lọc theo một tín hiệu** → train lại trên phần đã lọc; cải thiện mà không cần nhãn người.
**(b) Trụ bình-duyệt:**
- **STaR: Self-Taught Reasoner** (Zelikman et al., **NeurIPS 2022**) — sinh rationale → giữ cái dẫn tới đáp án đúng → train lại. Kinh điển của "sinh→lọc→train".
- **BLIP/CapFilt** (**ICML 2022**) — như T2.
- **KnowAda** (Yanuka et al., **NAACL 2025**, Oral) — **lọc/thích-nghi caption theo tri-thức model** → giảm mâu thuẫn (ảo giác) trên nhiều VLM nhỏ, giữ độ mô tả.
- **Speculative Knowledge Distillation** (**ICLR 2025**, arXiv 2410.11325) — chỉ đích danh **distribution-mismatch** của SFT-trên-static-teacher-data + cơ chế lọc mẫu chất-lượng-thấp.
- *Preprint (bổ trợ):* Mind-the-Gap self-improvement (2412.02674 — "generation-verification gap"), "Winning Big with Small Models" (self-training ≈ KD cho hallucination-QA), "Measuring & Reducing LLM Hallucination without Gold" (FEWL) — **nhãn preprint**.
**(c) TA KHÁC:** công thức "sinh→lọc→train lại" đã có (STaR/CapFilt/KnowAda). Tính mới của ta thu về **2 điểm** (report/00 §2): (i) **lọc bằng nguồn ngoài có cấu trúc (VH), không self-probe**, cho hành vi rủi-ro-cao; (ii) **trụ thực nghiệm số 1 = đo faithfulness khi TẮT VH lúc suy luận** (held-out theo app — kiểm "thói quen trung thực có nội-tại-hoá vào trọng số không", câu hỏi mới, có thể null thật).

### T4. Ảo giác (hallucination) & trung thực (faithfulness) trong VLM
**(a)** VLM "bịa" nội dung không có trong ảnh; đo/giảm bằng đối chiếu ngữ nghĩa với nguồn, hoặc reference-free.
**(b) Trụ bình-duyệt:**
- **ALOHa** (**NAACL 2024**) — nền công thức **Độ trung thực = 1 − bịa/(bước-nhắc-nút)** (matcher open-vocab, đối chiếu ngữ nghĩa với nguồn ngoài).
- **FaithScore** (**Findings of EMNLP 2024**) — faithfulness reference-free cho LVLM (tách atomic facts → verify). *Đối thủ gần nhất về đo faithfulness.*
- **VGA** (**Findings of EMNLP 2024**) — giảm ảo giác GUI bằng image-centric SFT (đã ở T1).
- **KnowAda** (**NAACL 2025**) — giảm contradiction-rate (đã ở T3).
- **FaithDial** (Dziri et al., **TACL 2022**) — benchmark hội thoại trung-thực bằng cách **sửa câu ảo-giác**; kinh điển "faithfulness khi có nguồn tri-thức".
**(c) TA KHÁC:** FaithScore/ALOHa đo faithfulness **có tài liệu tham chiếu tại lúc chấm**; ta đo **khi mô hình KHÔNG được cấp VH lúc suy luận** (đo nội-tại-hoá), và VH chỉ vào lúc **lọc-train + chấm**, không vào lúc sinh. Ta cũng chống **tự-chấm**: lọc bằng `nomic`, chấm bằng **3 cơ chế khác họ** (bge-m3 + LLM-judge llama3.2 + token-overlap).

### T5. Model nhỏ on-device — vì sao train student thay vì gọi API
**(a)** VLM 3B chạy được trên phần cứng học-viên/điện-thoại; là size-class đúng cho triển khai khi không gọi được frontier API.
**(b):**
- **LoRA Learns Less and Forgets Less** (Biderman et al., **TMLR 2024**, Featured Certification) — LoRA học ít hơn full-FT nhưng **quên ít hơn** → biện minh chọn LoRA cho student 3B.
- *Preprint (bổ trợ):* "Efficient Deployment of VLMs on Mobile (OnePlus 13R)" (2507.08505 — chạy VLM 3B thật trên điện thoại), MobileVLM V2 (2402.03766 — 3B vượt loạt 7B), "Profiling LoRA/QLoRA on Consumer GPUs" (2509.12229 — số VRAM/thời-gian cho ngân sách Colab). **Nhãn preprint.**
**(c) TA KHÁC / vai:** dùng để **biện minh chọn student nhỏ** (thoả yêu-cầu-train-model của thầy + niche on-device có a11y-tree live), KHÔNG phải đóng góp. Ta không claim kỷ lục hiệu năng on-device.

### T6. LoRA & quên (limitations — dùng ở phần Hạn chế/phòng thủ)
**(a)** LoRA rank thấp có thể không đủ cho dịch-chuyển-năng-lực lớn, và VLM fine-tune miền hẹp dễ quên năng lực nền.
**(b):** **LoRA Learns Less and Forgets Less** (**TMLR 2024**) — trụ chính. *Preprint bổ trợ:* catastrophic-forgetting-LoRA (2402.15415), continual-learning-VLM (2506.03189).
**(c) TA KHÁC / vai:** khai thẳng **trần năng lực** (student khó vượt teacher tổng quát; chỉ kỳ vọng cải-thiện trên chiều faithfulness-GUI) + cam kết **đo forgetting** (held-out ngoài miền). Đây là "phòng thủ trung thực", không phải đóng góp.

### T7. Đánh giá sinh KHÔNG-tham-chiếu (no-gold) — trục chính VCL
**(a)** Đánh giá văn bản sinh khi **không có đáp án chuẩn do người soạn**; dùng khung intrinsic/extrinsic, tín hiệu tự-động thay gold.
**(b) Trụ bình-duyệt:**
- **Chim, Ive & Liakata** — *Evaluating Synthetic Data Generation from User Generated Text* (**Computational Linguistics 51(1):191–233, 2025** — tạp chí; **KHÔNG phải "ACL 2025"**; đây là bài **tham khảo thầy giới thiệu**, không phải bài của thầy). Khung đánh giá neo (Intrinsic + Extrinsic) cho "synthetic text không đáp-án-chuẩn".
- **ALOHa** (**NAACL 2024**), **FaithScore** (**Findings EMNLP 2024**) — như T4.
**(c) TA KHÁC:** Chim et al. là **text→text**; ta là **ảnh+text→text** (multimodal, miền GUI) và neo tín hiệu bằng **View Hierarchy có cấu trúc**, không bằng LLM tự-chấm.

### T8. Validate metric bằng bơm-lỗi (perturbation) — trục hợp-lệ VCL
**(a)** Kiểm một metric có "thật sự đo cái nó nói" bằng cách **bơm lỗi đã-biết** rồi xem metric có phát-hiện/đơn-điệu không.
**(b) Trụ bình-duyệt:**
- **Sai et al.** (**EMNLP 2021**) — perturbation checklist cho NLG metric (trụ chính).
- **BUMP** (**ACL 2023**) — minimal-pair meta-eval cho hallucination metric (cặp trụ với Sai).
**(c) TA KHÁC / vai:** ta dùng perturbation làm **cổng hợp-lệ CHÍNH** (không dùng chấm-người làm cổng đậu/rớt vì thầy không ưa chấm-người + Clark 2021), bơm lỗi **độc lập matcher**. Đóng khung "perturbation = độ nhạy = điều kiện cần, chưa phải convergent validity".

### T9. LLM-as-judge & tính hợp lệ của thước đo — trục hợp-lệ VCL
**(a)** Dùng LLM chấm sinh; nhưng có thiên lệch tự-ưu-ái và câu hỏi construct-validity.
**(b) Trụ bình-duyệt:**
- **Panickssery et al.** (**NeurIPS 2024**) — self-preference bias → judge **PHẢI khác họ** generator.
- **Clark et al.** (**ACL-IJCNLP 2021**) — human-eval không còn là gold sạch → **bỏ human-correlation khỏi cổng đậu/rớt**.
- **Measuring what Matters: Construct Validity in LLM Benchmarks** (**NeurIPS 2025**) — lăng kính construct-validity.
- **Neither Valid nor Reliable?** (**NeurIPS 2025**, Position) — không lấy LLM-judge làm trục validate chính.
- **Chen et al.** (**ICSE 2020**, Distinguished Paper) — **>77% app thiếu nhãn a11y** → VH KHÔNG phải ground truth → biện minh hậu-kiểm + fallback.
**(c) TA KHÁC:** ta dùng LLM-judge **khác-họ (llama3.2, không GPT-family vì gpt-4o-mini là teacher)** chỉ như **1 trong 3 cơ chế chấm**, không làm trục validate chính; trục chính là **perturbation** (T8).

---

## PHẦN 2 — BẢN THẢO TÁCH SẴN

### 2.A — FAIR (tiếng Anh, bài model) — Related Work draft

> Đưa vào §2 Related Work. 4 tiểu-mục. **Peer-reviewed vs preprint đã tách.** Cần điền lại số/citation-key theo bibtex khi dựng bài.

**2.1 GUI Grounding and On-Device UI Agents.**
Recent work fine-tunes vision–language models (VLMs) to *localize and act on* UI elements. SeeClick (ACL 2024) and OS-Atlas / ScreenSpot-v2 (ICLR 2025) established point-in-bbox grounding benchmarks; UI-R1 (AAAI 2026), SE-GUI (NeurIPS 2025) and GUI-Actor (NeurIPS 2025) show that reinforcement or action-head training over Qwen2.5-VL-3B reaches competitive grounding with as few as ~100–3k examples, and ZonUI-3B (WACV 2026) demonstrates that LoRA fine-tuning of a 3B VLM on a single 24GB GPU is sufficient. All of these target *agents that click*, evaluated against **gold action trajectories**. Our task is different in kind: we generate **step-by-step instructions for a human reader** from a single screenshot and a natural-language question, a setting with **no gold tutorial** to score against. We therefore place our modeling contribution in faithfulness-filtered data curation and an on-device generator, not in grounding accuracy, and we do **not** claim leaderboard SOTA.

**2.2 Distillation into Small VLMs.**
Transferring a large teacher VLM into a compact student via SFT on teacher-generated data — without architectural change — is well established: LLaVA-KD (ICCV 2025) and VLsI (CVPR 2025) show small students can match or exceed much larger models, and DreamStruct (ECCV 2024) fine-tunes a small VLM on **teacher-generated UI data with no human gold**, beating both the base model and human-caption baselines. BLIP's CapFilt (ICML 2022) is the canonical *generate-then-filter* precedent. We build on this line but differ in the **filtering signal**: rather than self-consistency or a learned filter, we filter teacher outputs against a **structured external source (the View Hierarchy)**, targeting a **high-risk behavior** — naming buttons that do not exist on screen.

**2.3 Self-Training and Faithfulness-Filtered Data.**
The generate → filter → retrain loop underlies STaR (NeurIPS 2022), CapFilt (ICML 2022) and KnowAda (NAACL 2025), the last of which shows that adapting/filtering captions to a model's knowledge reduces hallucination in small VLMs. Speculative KD (ICLR 2025) diagnoses the distribution mismatch of SFT on static teacher data. We explicitly acknowledge that filtered self-training is **not itself novel**; our novelty is two-fold: (i) the filter is a **structured, GUI-specific verifier (VH), not a self-probe**; and (ii) our **primary empirical pillar measures faithfulness with the VH switched off at inference time** (app-held-out), testing whether faithful behavior is **internalized into the student's weights** rather than propped up by the filter.

**2.4 Hallucination and Faithfulness in VLMs.**
Faithfulness metrics such as ALOHa (NAACL 2024) and FaithScore (Findings of EMNLP 2024), and GUI-specific hallucination reduction such as VGA (Findings of EMNLP 2024), evaluate or reduce ungrounded content **with a reference available at scoring time**. FaithDial (TACL 2022) is the classic faithfulness-with-a-source benchmark. Our evaluation departs by scoring the student **without any VH at inference**, and by guarding against self-scoring: the training filter uses one embedding family (nomic) while scoring uses three **independent** mechanisms (bge-m3, a cross-family LLM judge, and token overlap). *(On feasibility, we adopt LoRA following its documented learn-less/forget-less trade-off — Biderman et al., TMLR 2024 — and treat catastrophic forgetting as a measured limitation, not an afterthought.)*

**FAIR — self-citation note:** vì FAIR nộp TRƯỚC (15/8), FAIR **không** trích VCL (VCL chưa tồn tại lúc nộp). Nếu lịch đảo (FAIR trượt, VCL trước) thì thêm 1 câu ở 2.4 dẫn "our companion evaluation paper". Giữ mục 2.4 gọn để không lấn phần eval của VCL.

---

### 2.B — VCL (tiếng Việt, bài sinh-VN + đánh giá) — Bản thảo Công trình liên quan

> Đưa vào §2. Viết tiếng Việt. Trục = **đánh giá no-gold + validate metric + judge**; model chỉ nhắc 1 đoạn và **trích FAIR** (self-citation).

**2.1. Sinh hướng dẫn GUI và mô hình cơ sở.**
Các mô hình thị giác–ngôn ngữ gần đây được tinh chỉnh để định vị và thao tác trên giao diện (SeeClick, ACL 2024; OS-Atlas, ICLR 2025; UI-R1, AAAI 2026; GUI-Actor, NeurIPS 2025), nhưng đều là *tác tử bấm nút* được chấm bằng quỹ đạo vàng. Bài này kế thừa **mô hình sinh hướng dẫn** được huấn luyện trong công trình song hành của chúng tôi [trích FAIR — ẩn danh, ngôi thứ ba] và tập trung vào **đánh giá đầu ra sinh bằng tiếng Việt khi không có bộ hướng dẫn mẫu**.

**2.2. Đánh giá sinh không-tham-chiếu.**
Chúng tôi kế thừa khung đánh giá cho văn bản tổng hợp không-đáp-án-chuẩn của **Chim, Ive & Liakata (Computational Linguistics 51(1), 2025)** — khung Intrinsic/Extrinsic; khác biệt là bài toán của chúng tôi **đa phương thức (ảnh + câu hỏi → hướng dẫn)** trong miền GUI. Về độ trung thực, chúng tôi dựa trên matcher đối-chiếu-ngữ-nghĩa kiểu **ALOHa (NAACL 2024)** và tuyến reference-free **FaithScore (Findings EMNLP 2024)**, nhưng neo tín hiệu bằng **View Hierarchy có cấu trúc** thay vì để mô hình tự-chấm. Vì hơn 77% ứng dụng thiếu nhãn trợ-năng đầy đủ (**Chen et al., ICSE 2020**), View Hierarchy được xem là *nhãn-bạc* dùng cho hậu-kiểm + fallback, **không phải chân-lý**.

**2.3. Kiểm chứng tính hợp lệ của thước đo.**
Thay vì lấy tương-quan-người làm cổng đậu/rớt (vốn không còn là chuẩn sạch — **Clark et al., ACL-IJCNLP 2021**), chúng tôi kiểm chứng thước đo chính bằng **bơm-lỗi tự động** theo **Sai et al. (EMNLP 2021)** và **BUMP (ACL 2023)** — đo khả-năng-phát-hiện và tính-đơn-điệu với lỗi đã-biết, bơm độc lập với matcher. Chúng tôi đóng khung perturbation là *điều kiện cần* (độ nhạy), chưa phải convergent validity.

**2.4. LLM-as-judge và thiên lệch.**
Do mô hình chấm-bằng-LLM có thiên lệch tự-ưu-ái (**Panickssery et al., NeurIPS 2024**) và các câu hỏi về construct-validity (**Measuring what Matters, NeurIPS 2025; Neither Valid nor Reliable, NeurIPS 2025**), chúng tôi chỉ dùng LLM-judge **khác họ với bộ sinh** như *một* trong ba cơ chế chấm độc lập, và không lấy nó làm trục validate chính.

**VCL — self-citation note:** vì FAIR nộp trước, VCL **PHẢI trích FAIR** ở 2.1 và nêu rõ phần MỚI (output tiếng Việt + đánh giá no-gold; VCL **không** lặp bảng số/kiến-trúc của FAIR). Do có thể ẩn danh → viết "our companion paper" ở ngôi thứ ba. ⚠️ Nếu FAIR bị bỏ (fallback), đổi 2.1 thành mô tả model tự-chứa + reframe headline VCL sang "phương-pháp-đánh-giá thuần" (report/00 §4).

---

## PHẦN 3 — DỰ TRỮ: Related work nhiều-màn (T10, cho bài mở rộng tương lai — KHÔNG dùng mùa này)

> Đã verify sẵn, cất để bài tiếng-Anh-mở-rộng (FAIR'27/quốc tế) dùng lại. **Không đưa vào FAIR/VCL mùa này.**

- **Sắp thứ tự ảnh xáo:** Sort-Story (**EMNLP 2016**, Spearman) · Wu et al. (ACL 2022, τ) · RankGPT (EMNLP 2023, listwise).
- **Pairwise → tổng hợp:** Qin et al. PRP (**Findings NAACL 2024**, pairwise > listwise) · Copeland/Dwork (**WWW 2001**, rank aggregation) · Ailon et al. min-FAS (**JACM 2008**, phá vòng).
- **τ thứ-tự-bộ-phận:** **Fagin et al. (SIAM J. Discrete Math 2006)** + **Lapata (CL 2006)** — KHÔNG gọi "Kendall τ-b".
- **VLM yếu sắp thứ tự thời gian:** TOMATO (ICLR 2025 Poster) · GVL (ICLR 2025) — module Stage-0 không thừa.
- **Phân-tầng-một-cue:** Gardner et al. Contrast Sets (**EMNLP 2020**) — trụ khái niệm.
- **Prior-art gần (phải phân định):** GUI Knowledge Bench (preprint 2510.26098) · TempVS (preprint) · EZ-Sort (CIKM 2025) · Dodgersort (PAKDD 2026).

---

## PHẦN 4 — Checklist trước khi dán vào bài

- [ ] Mỗi citation: đối chiếu lại bibtex (venue/năm khớp file này) — đặc biệt UI-R1 = **AAAI 2026** (không 2025), Chim = **CL 2025** (không "ACL 2025").
- [ ] Preprint gắn nhãn "arXiv preprint" trong bài, KHÔNG viết như đã bình-duyệt (ALLaVA, GenRecal, Mind-the-Gap, MobileVLM-V2, on-device-OnePlus, các GUI-preprint).
- [ ] FAIR ↔ VCL: theme distillation/GUI-model chỉ ở FAIR; validate-metric/judge chỉ ở VCL; theme faithfulness viết **câu chữ khác nhau** ở 2 bài.
- [ ] Self-citation đúng chiều theo thứ-tự-nộp thực tế (FAIR trước → VCL trích FAIR).
- [ ] T10 (nhiều-màn) KHÔNG lọt vào FAIR/VCL mùa này.
- [ ] Không câu nào claim SOTA leaderboard; mỗi theme có 1 câu "ta khác gì".
</content>
</invoke>
