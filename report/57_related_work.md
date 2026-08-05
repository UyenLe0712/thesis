# 57 — RELATED WORK (kho luận điểm chung + 2 bản thảo tách FAIR/VCL)

> **Mục đích:** viết sẵn phần Công-trình-liên-quan cho CẢ HAI bài (FAIR = model tiếng Anh · VCL = sinh-tiếng-Việt + đánh giá).
> Soạn theo lựa chọn của user (2026-07-12): **viết chung một kho luận điểm → tách/viết-lại câu chữ cho từng bài** (chống trùng lặp).
> **Mọi citation trong file này đã verify venue/năm** (nguồn: `report/50`, `report/_archive/51`, `report/papers/`, + web-verify 2026-07-12). Preprint được gắn nhãn rõ; **KHÔNG trích preprint như trụ bình-duyệt**.
> Khi mâu thuẫn framing: `report/54` (pipeline) + `report/00` (trạng thái) thắng.
>
> **⚠️ CẬP NHẬT 2026-07-12 (sau debate `wf_e77fd58f`, 22 đòn web-verify, 0 đòn design):** đã vá trọn 4 nhóm — (1) scoop cần phân-định (DocVAL, dòng lọc-a11y-tree); (2) thiếu citation reviewer sẽ đòi (UGIF, screen-captioning-cho-người, VLM tiếng Việt, POPE/HallusionBench, eval-Việt, cross-lingual-tuning); (3) sửa citation sai (DreamStruct = synthetic-data code-gen, KHÔNG phải distillation); (4) framing/overclaim (hedge "internalized→persists", T4c reference-free, ZonUI recipe-collision, cắt đống grounding, salami FAIR2.4, self-cite ngôi-ba-ẩn-danh). Không đòn nào chạm thiết kế thí nghiệm.

---

## PHẦN 0 — Nguyên tắc & bản đồ đặt citation

**3 luật bất biến khi viết related work:**
1. **Không bịa** venue/năm/tác giả. Peer-reviewed vs preprint phân biệt rõ. Xương sống lập luận chỉ dựa trụ bình-duyệt; preprint chỉ minh hoạ "landscape/hiện vật kỹ thuật".
2. **Mỗi theme phải có 1 câu "ta KHÁC gì"** (distinguish). Related work không phải liệt kê — nó là hàng rào phòng thủ khi giám khảo hỏi "bài này đã có người làm chưa?".
3. **Chống trùng 2 bài:** FAIR nộp trước (15/8) → **VCL trích FAIR**. Vì cả hai đang bình-duyệt ẩn-danh, **self-citation viết NGÔI THỨ BA** ("a concurrent submission under review (Anonymous)…"), **CẤM "our/chúng tôi"** (lộ đồng-tác-giả → phá double-blind, có thể desk-reject). Theme distillation/GUI-model → thuộc FAIR. Theme validate-metric/judge → thuộc VCL. Theme faithfulness-VLM = **dùng chung nhưng đóng khung khác + VIẾT LẠI CÂU CHỮ** ở mỗi bài (FAIR tiếng Anh dễ bị quét trùng). ⚠ Trục salami THẬT = **data nguồn chung** (đã bù bằng khác-output + khác-câu-hỏi + trích-chéo); overlap phần methods là "minor" theo COPE nhưng vẫn nên tách để gọn.

**Bản đồ theme → bài:**

| Theme | FAIR (model) | VCL (eval-VN) |
|---|---|---|
| T1. GUI agents & grounding (VLM nhỏ cho UI) | **Trung tâm** | nhắc 1 câu (bối cảnh) |
| T1b. Sinh mô tả/hướng dẫn UI cho NGƯỜI (captioning, how-to) | **Trung tâm** (phân-định task) | nhắc |
| T2. Chưng cất VLM lớn→nhỏ (KD) | **Trung tâm** | — |
| T3. Self-training / lọc dữ liệu tổng hợp (gồm lọc-bằng-a11y-tree) | **Trung tâm** | nhắc (nguồn tín hiệu train) |
| T4. Ảo giác & trung thực trong VLM | **Trung tâm** (đo faithfulness = công cụ chấm model) | **Trung tâm** (nghiên cứu tính-HỢP-LỆ thước đo) |
| T5. On-device / model nhỏ khả thi | **Trung tâm** (biện minh student) | — |
| T6. LoRA & quên (forgetting) | phụ (limitations) | — |
| T7. Đánh giá sinh KHÔNG-tham-chiếu | phụ (đo faithfulness) | **Trung tâm** |
| T8. Validate metric bằng bơm-lỗi | nhắc | **Trung tâm (trụ hợp-lệ)** |
| T9. LLM-as-judge & tính hợp lệ | nhắc | **Trung tâm** |
| T10-VN. VLM & đánh giá tiếng Việt + cross-lingual | — | **Trung tâm** |
| T11. Sắp-thứ-tự nhiều-màn (Stage-0) | **HOÃN** → bài mở rộng sau | — |

> ⚠️ **Ranh giới tách 2 bài (đã sửa nhãn):** KHÔNG nói "FAIR = mục-tiêu-train / VCL = đối-tượng-đo" (sai — trụ Tier-2 của FAIR CŨNG đo faithfulness). Ranh giới ĐÚNG = **ngôn-ngữ-output (Anh vs Việt) + loại-đóng-góp**: FAIR dùng metric faithfulness như **CÔNG CỤ** chấm model của mình (Tier1/Tier2), output tiếng Anh; VCL nghiên cứu **TÍNH-HỢP-LỆ của chính thước đo đó** (validate bằng bơm-lỗi) + sinh tiếng Việt. Chỉ vế **validity + ngôn ngữ** là phần không trùng.
> ⚠️ **T11 (nhiều-màn) đã HOÃN khỏi mùa này** (report/00 §4). Chỉ đưa vào related-work của **bài tiếng-Anh-mở-rộng tương lai**. Giữ ở PHẦN 3.

---

## PHẦN 1 — KHO LUẬN ĐIỂM THEO THEME (dùng cho cả 2 bài)

Mỗi theme: *(a) prior work làm gì · (b) citation đã-verify · (c) TA KHÁC gì.*

### T1. GUI agents & visual grounding bằng VLM nhỏ
**(a)** Dòng GUI-agent 2024–2026 fine-tune VLM để **định vị/bấm nút** trên ảnh màn hình: dự đoán toạ độ (point-in-bbox) hoặc hành động, chấm bằng **quỹ đạo/nhãn vàng** có sẵn.
**(b) Trụ bình-duyệt (giữ 4 đại diện, tránh chất đống):**
- **SeeClick** (Cheng et al., **ACL 2024**) — grounding point-in-bbox + benchmark ScreenSpot gốc.
- **OS-Atlas / ScreenSpot-v2** (Wu et al., **ICLR 2025**) — foundation grounding, sửa 11–32% lỗi nhãn ScreenSpot.
- **UI-R1** (Lu et al., **AAAI 2026**) — GRPO trên Qwen2.5-VL-3B, reward point-in-bbox, chỉ 136 mẫu.
- **GUI-Actor** (Wu et al., Microsoft, **NeurIPS 2025**) — action-head coordinate-free + grounding verifier train riêng.
- *Landscape (gộp 1 câu, không dàn hàng):* SE-GUI (NeurIPS 2025, GRPO ~3k mẫu) · **ZonUI-3B/Qwen-GUI-3B (WACV 2026)** · VGA (Findings EMNLP 2024) · MobileVLM (Findings EMNLP 2024) cùng cho thấy LoRA/RL trên VLM 3B đạt grounding cạnh tranh. *Preprint (hiện vật, không trụ):* InfiGUI-R1-3B, GUI-AIMA-3B, ReGUIDE, LiteGUI.
**(c) TA KHÁC (distinguish tích cực, KHÔNG "nhiều-cite-mạnh-hơn"):** các hệ này **tối ưu điểm-bấm CÓ gold** (hàm mục tiêu = grounding accuracy). Ta **tối ưu chữ-hướng-dẫn KHÔNG-gold cho người đọc** — hai hàm mục tiêu khác nhau, nên không cạnh tranh cùng leaderboard và **ta không báo số ScreenSpot**. Đóng góp model đặt ở **lọc-trung-thực + generator on-device sinh chữ**, không ở grounding.
> ⚠ **ZonUI = vai FEASIBILITY-only.** ZonUI dùng ĐÚNG recipe của ta (LoRA Qwen2.5-VL-3B, r=8/α=16, 1 GPU 24GB). **KHÔNG khoe trùng config**; chỉ trích để chứng minh "một VLM 3B LoRA-tune được trên 1 GPU 24GB". Nói trước: *ta TÁI DÙNG recipe train đã kiểm chứng của ZonUI; đóng góp là BỘ LỌC DỮ LIỆU + tác-vụ-sinh-no-gold, KHÔNG phải recipe train* → chặn phản biện "chỉ chạy lại ZonUI trên data khác".

### T1b. Sinh mô tả / hướng dẫn UI cho NGƯỜI (captioning, how-to) — theme phân-định wedge
**(a)** Dòng công trình **sinh ngôn ngữ tự nhiên mô tả UI cho người** (accessibility, tóm tắt màn), và **theo hướng-dẫn how-to trên UI** — KHÁC agent-bấm-nút thuần.
**(b) Trụ bình-duyệt:**
- **Widget Captioning** (Li et al., **EMNLP 2020**) — sinh mô tả NL cho **phần tử UI** từ ảnh + View Hierarchy, động lực accessibility; 162.859 caption người-gán / 61.285 phần tử.
- **Screen2Words** (Wang et al., **UIST 2021**) — tóm tắt cả **màn** cho người, dùng screenshot + VH.
- **ScreenAI** (Baechler et al., **IJCAI 2024**) — VLM 5B hiểu UI/infographic; dùng **LLM tự-sinh screen-annotation + QA quy mô lớn để train** (tiền lệ "model sinh dữ liệu train UI").
- **UGIF-DataSet** (Venkatesh, Talukdar & Narayanan, **Findings of NAACL 2024**; gốc UGIF arXiv 2211.07615) — **UI how-to instruction đa ngôn ngữ (8 thứ tiếng), 4.184 tác vụ**: truy-xuất help-doc có sẵn → parse → **GROUND thành chuỗi hành động thực-thi** overlay lên UI, chấm bằng **task-completion (có gold)**; query một ngôn ngữ, hướng dẫn tiếng Anh, UI ngôn ngữ khác.
**(c) TA KHÁC (đây là chỗ wedge phải thu hẹp cho đúng, tránh bị bác "không ai sinh chữ-UI cho người"):**
- Widget Captioning/Screen2Words = caption **MỘT-phần-tử/MỘT-màn CÓ caption vàng** người-gán; ta sinh **hướng-dẫn THAO-TÁC ĐA-BƯỚC theo mục tiêu, KHÔNG gold tutorial**.
- ScreenAI = model **lớn server-side**, không lọc-faithfulness đối-chiếu-VH cho hành-vi-rủi-ro-cao, không nhắm on-device.
- UGIF = **ground doc CÓ SẴN thành macro cho MÁY chạy, có gold execution**; ta **SINH hướng dẫn MỚI cho NGƯỜI, không doc nguồn, không gold**, trung thực đến từ **lọc-VH** chứ không từ grounding-thực-thi. *(UGIF cũng là tiền lệ cross-lingual gần nhất cho VCL — xem T10-VN.)*

### T2. Chưng cất VLM lớn → nhỏ (knowledge distillation)
**(a)** Chuyển năng lực từ VLM lớn/đóng (teacher) sang VLM nhỏ (student) qua SFT trên dữ liệu teacher-sinh, **không đổi kiến trúc**; nhiều bài chứng minh student vượt base.
**(b) Trụ bình-duyệt:**
- **LLaVA-KD** (Cai et al., **ICCV 2025**, arXiv 2410.16236) — khung 3-giai-đoạn distill MLLM lớn→nhỏ, cải thiện student **không đổi kiến trúc**. *(Trụ neo chính cho distillation teacher→student.)*
- **VLsI** (**CVPR 2025**, arXiv 2412.01822) — distill lớn→nhỏ cho VLM **sinh** (2B/7B), tránh imitation-instability.
- **ScreenAI** (**IJCAI 2024**) — như T1b: **model tự-sinh dữ-liệu-train UI** = tiền lệ gần "teacher sinh data" của ta (nhưng server-side, không lọc-VH, không on-device).
- **BLIP / CapFilt** (Li et al., **ICML 2022**, spotlight) — captioner sinh caption + **filter loại caption nhiễu** = cấu trúc "sinh + lọc".
- *Preprint (bổ trợ, nhãn preprint):* ALLaVA (GPT-4V→lite VLM), GenRecal, KD survey (2402.13116).
**(c) TA KHÁC:** distillation trần KHÔNG mới. Ta khác ở **tín hiệu lọc = nguồn NGOÀI có cấu trúc (View Hierarchy), không self-consistency**, áp cho **hành-vi rủi-ro-cao** (gọi sai tên nút thật). Ta làm **sinh hướng-dẫn-thao-tác từng-bước cho người**; điểm mới **DUY NHẤT ở khối này** = **tín hiệu-lọc-VH** (không phải bản thân vòng generate–filter–retrain, vốn không mới — xem T3).
> 📎 **DreamStruct KHÔNG thuộc theme này** (đã sửa): DreamStruct (**ECCV 2024**, arXiv 2410.00201) fine-tune VLM nhỏ (LLaVA-1.5-13B) trên **dữ liệu UI/slide TỔNG HỢP sinh bằng CODE (nhãn cài-sẵn theo lập trình, + ít mẫu người)** — là **synthetic-data-generation (T3)**, KHÔNG phải distillation teacher→student. Trích như tiền lệ "train student UI trên dữ liệu không-human-gold", KHÔNG phải "teacher-VLM sinh data".

### T3. Self-training / bootstrapping / lọc dữ liệu tổng hợp không-gold
**(a)** Model sinh dữ liệu → **lọc theo một tín hiệu** → train lại trên phần đã lọc; cải thiện mà không cần nhãn người.
**(b) Trụ bình-duyệt:**
- **STaR: Self-Taught Reasoner** (Zelikman et al., **NeurIPS 2022**) — sinh rationale → giữ cái đúng → train lại.
- **BLIP/CapFilt** (**ICML 2022**) — như T2.
- **KnowAda** (Yanuka et al., **NAACL 2025**, Oral) — lọc/thích-nghi caption theo tri-thức model → giảm ảo giác VLM nhỏ.
- **MultiUI** (Liu et al., **ICLR 2025** Poster, arXiv 2410.13824) — **SINH 7,3M instruction TỪ accessibility-tree của 1M website** (dùng a11y-tree làm nguồn sinh).
- **Speculative KD** (**ICLR 2025**, arXiv 2410.11325) — chỉ đích danh distribution-mismatch của SFT-trên-static-teacher-data.
- **DreamStruct** (**ECCV 2024**) — synthetic-data code-gen cho UI (xem ghi chú T2).
- *Preprint (landscape lọc-bằng-a11y-tree, nhãn preprint):* **UI-Oceanus** (2604.02345 — lọc 3 tầng: MinHash structural dedup trên a11y-tree + pHash + VLM action-feedback-consistency) · **Mobile-Agent-v3/GUI-Owl** (2508.15144, Alibaba — pipeline grounding cho agent-click). *Preprint bổ trợ khác:* Mind-the-Gap self-improvement (2412.02674), "Winning Big with Small Models", FEWL.
**(c) TA KHÁC (đã thu hẹp — "lọc-bằng-nguồn-cấu-trúc" chung chung KHÔNG mới):** dùng nguồn UI có cấu trúc trong pipeline dữ-liệu GUI đã phổ biến (UI-Oceanus, MultiUI, Mobile-Agent-v3). Ta khác **3 trục**: (a) **HƯỚNG dùng** — họ dùng a11y-tree để NHẬN DIỆN/DEDUP phần tử hoặc SINH instruction từ a11y; ta dùng VH để **KIỂM & LOẠI tham-chiếu-nút-không-tồn-tại trong văn bản ĐÃ sinh**; (b) **HÀNH VI đích** — họ dedup/khớp-phản-hồi-môi-trường; ta nhắm hành-vi-rủi-ro-cao "gọi tên nút không có trên màn" trong **hướng-dẫn-cho-NGƯỜI**; (c) **ĐẦU RA** — họ tạo dữ-liệu-agent-BẤM có gold; ta sinh tutorial cho người, no-gold. Tính mới thu về **2 điểm** (report/00 §2): (i) **tín hiệu lọc = VH có cấu trúc bên ngoài, không self-probe**, cho hành-vi rủi-ro-cao; (ii) **trụ thực nghiệm số 1 = đo faithfulness khi TẮT VH lúc suy luận** (held-out theo app — kiểm *hành vi trung thực có CÒN GIỮ khi bỏ bộ lọc không*; câu hỏi **còn ít được xét trong bối cảnh sinh-hướng-dẫn-GUI** — dòng context-distillation/self-training đã hỏi dạng-tổng-quát "behavior có giữ khi bỏ scaffold lúc infer": Snell 2022, STaR NeurIPS 2022 — nhưng ở đây tín hiệu là **bộ-lọc-VH chọn-dữ-liệu**, không phải context-trong-prompt; **có thể null thật**).
> 🎯 **Scoop áp sát — PHẢI phân-định: DocVAL** (arXiv **2511.22521, PREPRINT** — tự khai ICML 2026 nhưng đăng 27/11/2025 *trước* hạn nộp ICML → **chưa xác nhận bình-duyệt, để nhãn preprint**). DocVAL ghép cả 2 wedge: distill teacher→student + **lọc dữ liệu bằng nguồn ngoài có cấu trúc** (text-detection đối chiếu gold bbox) + **gỡ nguồn lúc suy luận** ("no text detection required", model "internalizes spatial representations"). **Ta khác:** miền **document-VQA CÓ gold bbox** (chấm mAP/ANLS) vs ta **mobile-GUI đa-app, sinh-hướng-dẫn-cho-người KHÔNG gold tutorial, faithfulness về tên-nút-tồn-tại** thay vì toạ-độ-có-gold. Verify lại venue sát ngày nộp FAIR.

### T4. Ảo giác (hallucination) & trung thực (faithfulness) trong VLM
**(a)** VLM "bịa" nội dung không có trong ảnh; đo/giảm bằng đối chiếu ngữ nghĩa với nguồn, hoặc reference-free.
**(b) Trụ bình-duyệt:**
- **ALOHa** (**NAACL 2024**) — nền công thức **Độ trung thực = 1 − bịa/(bước-nhắc-nút)** (matcher open-vocab).
- **FaithScore** (**Findings of EMNLP 2024**) — faithfulness **reference-free** cho LVLM. *Đối thủ gần nhất về đo faithfulness.*
- **POPE** (Li et al., **EMNLP 2023**) — object-hallucination probing (câu hỏi yes/no "có <vật> trong ảnh?"), chấm Accuracy/F1.
- **HallusionBench** (Guan et al., **CVPR 2024**) — diagnostic entangled language-hallucination + visual-illusion, 346 ảnh/1129 câu.
- **VGA** (**Findings of EMNLP 2024**) — giảm ảo giác GUI bằng image-centric SFT.
- **KnowAda** (**NAACL 2025**), **FaithDial** (Dziri et al., **TACL 2022**) — như T3/faithfulness-với-nguồn.
**(c) TA KHÁC (đã sửa để KHÔNG tự-mâu-thuẫn):** POPE/HallusionBench probing tồn-tại-vật-thể / visual-illusion trên **ảnh tự nhiên**; FaithScore **reference-free lúc chấm**. Điểm khác biệt của ta **KHÔNG phải "reference-free scoring"** (thực tế ta DÙNG VH lúc chấm, như nhãn-bạc), mà là **ĐIỀU KIỆN SINH không-VH**: ta tách rõ **VH-lúc-SINH (BỎ)** khỏi **VH-lúc-chấm (GIỮ)**, và đo **bịa-tên-nút-UI có cấu-trúc-VH trong setting SINH hướng dẫn**, không phải probing yes/no. Chống tự-chấm: lọc bằng `nomic`, chấm bằng **3 cơ chế khác họ** (bge-m3 + LLM-judge llama3.2 + token-overlap).
> 📎 **Trùng-tên cần chặn:** "Faithful Mobile GUI Agents with Guided Advantage Estimator" (arXiv **2605.01208, preprint**) là **RL-agent bấm-nút** (GRPO, reward Trap-SR, có gold) — **KHÔNG scoop** (khác task) nhưng trùng tên "Faithful…Mobile-GUI" + từ khoá faithfulness/missing-element. Thêm 1 câu phân-định (RL-agent-có-gold vs SFT-sinh-no-gold) để tránh gộp-nhầm khi bình-duyệt ẩn danh. Ưu tiên thấp.

### T5. Model nhỏ on-device — vì sao train student thay vì gọi API
**(a)** VLM 3B chạy được trên phần cứng học-viên/điện-thoại; đúng size-class khi không gọi được frontier API.
**(b):** **LoRA Learns Less and Forgets Less** (Biderman et al., **TMLR 2024**, Featured Certification) — LoRA học ít hơn full-FT nhưng **quên ít hơn**. *Preprint (bổ trợ):* on-device VLM 3B (2507.08505), MobileVLM V2 (2402.03766), profiling LoRA/QLoRA consumer-GPU (2509.12229).
**(c) vai:** biện minh **chọn student nhỏ** (thoả yêu-cầu-train-model + niche on-device có a11y-tree live), KHÔNG phải đóng góp; không claim kỷ lục on-device.

### T6. LoRA & quên (limitations — dùng ở phần Hạn chế/phòng thủ)
**(a)** LoRA rank thấp có thể không đủ cho dịch-chuyển-năng-lực lớn; VLM fine-tune miền hẹp dễ quên năng lực nền.
**(b):** **LoRA Learns Less and Forgets Less** (**TMLR 2024**). *Preprint bổ trợ:* catastrophic-forgetting-LoRA (2402.15415), continual-learning-VLM (2506.03189).
**(c) vai:** khai thẳng **trần năng lực** + cam kết **đo forgetting** (held-out ngoài miền). Phòng thủ trung thực, không phải đóng góp.

### T7. Đánh giá sinh KHÔNG-tham-chiếu (no-gold) — trục chính VCL
**(a)** Đánh giá văn bản sinh khi **không có đáp án chuẩn do người soạn**; khung intrinsic/extrinsic, tín hiệu tự-động thay gold.
**(b) Trụ bình-duyệt:**
- **Chim, Ive & Liakata** — *Evaluating Synthetic Data Generation from User Generated Text* (**Computational Linguistics 51(1):191–233, 2025** — tạp chí; **KHÔNG phải "ACL 2025"**; bài **tham khảo thầy giới thiệu**). Khung neo Intrinsic + Extrinsic.
- **ALOHa** (**NAACL 2024**), **FaithScore** (**Findings EMNLP 2024**) — như T4.
**(c) TA KHÁC (đã mạnh hoá — không chỉ "thêm ảnh"):** Chim et al. là text→text với khung intrinsic/extrinsic. Ta **MỞ RỘNG khung đó bằng một tín-hiệu-INTRINSIC mới — đối-chiếu-cấu-trúc-VH — mà miền text không có**; đó là khác biệt **phương-pháp** (không chỉ multimodal). Miền GUI, đa phương thức.

### T8. Validate metric bằng bơm-lỗi (perturbation) — TRỤ HỢP-LỆ trung tâm của VCL
**(a)** Kiểm một metric có "thật sự đo cái nó nói" bằng cách **bơm lỗi đã-biết** rồi xem metric có phát-hiện/đơn-điệu không.
**(b) Trụ bình-duyệt:** **Sai et al.** (**EMNLP 2021**) — perturbation checklist cho NLG metric · **BUMP** (**ACL 2023**) — minimal-pair meta-eval hallucination.
**(c) vai / TA KHÁC:** đây là **cổng hợp-lệ CHÍNH của VCL** (không dùng chấm-người làm cổng đậu/rớt — Clark 2021), bơm lỗi **độc lập matcher**. Đóng khung "perturbation = độ nhạy = điều kiện cần, chưa phải convergent validity".

### T9. LLM-as-judge & tính hợp lệ của thước đo — trục hợp-lệ VCL (VCL-sở-hữu, FAIR không có)
**(a)** Dùng LLM chấm sinh; nhưng có thiên lệch tự-ưu-ái và câu hỏi construct-validity.
**(b) Trụ bình-duyệt:** **Panickssery et al.** (**NeurIPS 2024**) — self-preference bias → judge khác họ · **Clark et al.** (**ACL-IJCNLP 2021**) — bỏ human-correlation khỏi cổng đậu/rớt · **Measuring what Matters: Construct Validity** (**NeurIPS 2025**) · **Neither Valid nor Reliable?** (**NeurIPS 2025**, Position) · **Chen et al.** (**ICSE 2020**, Distinguished) — **>77% app thiếu nhãn a11y** → VH KHÔNG phải ground truth.
**(c) TA KHÁC:** LLM-judge **khác-họ (llama3.2, không GPT-family)** chỉ là **1 trong 3 cơ chế**, không làm trục validate chính; trục chính = **perturbation (T8)**.

### T10-VN. VLM & đánh giá tiếng Việt + cross-lingual — trục riêng VCL
**(a)** Bối cảnh Việt-ngữ: có VLM/LLM tiếng Việt, có benchmark NLU tiếng Việt, và dòng cross-lingual instruction tuning.
**(b):**
- *VLM/LLM tiếng Việt (đều **preprint** — nhãn rõ):* **Vintern-1B** (arXiv 2408.12480 — MLLM 1B on-device, Qwen2-0.5B+InternViT, OCR/VQA; **gần nhất, có thể làm baseline smoke-test**) · **LaVy** (arXiv 2404.07922 — VN multimodal LLM + LaVy-Bench) · **PhoGPT** (arXiv 2311.02945 — LLM 4B **text-only**, chỉ bối cảnh).
- *Benchmark tiếng Việt (peer-reviewed, đều **NLU**):* **ViGLUE** (**Findings NAACL 2024**, 12 tác vụ) · **VLUE** (**Findings NAACL 2024**; ⚠ trích peer-reviewed, không chỉ "arXiv 2403.15882") · **VMLU** (**ACL 2025** long, trắc-nghiệm 58 môn).
- *Cross-lingual instruction tuning:* **xCoT** (**AAAI 2024**, arXiv 2401.07037) · **X-Instruction** (**Findings ACL 2024**) · CrossIn (arXiv preprint / workshop SumEval-2 2025).
**(c) TA KHÁC:**
- Vintern/LaVy hướng OCR/VQA tổng quát, **KHÔNG có năng-lực grounding GUI**; ta chọn **Qwen2.5-VL-3B** vì phả-hệ GUI-grounding mạnh (UI-R1/ZonUI LoRA đúng backbone này), rồi **chuyển-giao Anh→Việt ở tầng SINH**. (Nêu Vintern-1B là đối-chứng định-tính tiềm năng.)
- ViGLUE/VLUE/VMLU đều **NLU có đáp-án-chuẩn**; **chưa có chuẩn NLG no-gold tiếng Việt cho hướng dẫn GUI** — VCL lấp đúng khoảng-trống đó.
- xCoT/X-Instruction là **kỹ-thuật-HUẤN-LUYỆN** để thu năng lực cross-lingual; VCL **KHÔNG train trên dữ liệu tiếng Việt, sinh liên-ngôn-ngữ ZERO-SHOT**, và **không đề xuất kỹ-thuật cross-lingual mới** — chỉ đánh giá độ-trung-thực output liên-ngôn-ngữ (câu phòng-thủ, không nâng thành đóng góp).

---

## PHẦN 2 — BẢN THẢO TÁCH SẴN

### 2.A — FAIR (tiếng Anh, bài model) — Related Work draft

> §2 Related Work. Peer-reviewed vs preprint đã tách. Điền lại citation-key theo bibtex khi dựng bài.

**2.1 GUI Grounding, UI Description, and On-Device Agents.**
Recent work fine-tunes VLMs to *localize and act on* UI elements: SeeClick (ACL 2024) and OS-Atlas / ScreenSpot-v2 (ICLR 2025) established point-in-bbox grounding, while UI-R1 (AAAI 2026) and GUI-Actor (NeurIPS 2025) reach competitive grounding with small data; a broader landscape (SE-GUI, NeurIPS 2025; ZonUI-3B, WACV 2026; VGA, Findings EMNLP 2024) shows LoRA/RL on 3B VLMs is viable. These optimize *clicking against gold trajectories*. A separate line **generates natural language about UIs for humans** — Widget Captioning (EMNLP 2020) and Screen2Words (UIST 2021) caption single widgets or whole screens from screenshots and the View Hierarchy, and ScreenAI (IJCAI 2024) is a UI VLM that uses an LLM to self-generate large-scale training annotations. Closest in task, UGIF (Findings of NAACL 2024) *retrieves an existing help document and grounds it into an executable macro*, scored by task completion. Our task differs in kind: we **generate new, multi-step, goal-conditioned instructions for a human reader** from a single screenshot and question, with **no source document and no gold tutorial**; faithfulness comes from VH-based filtering rather than executable grounding, and we do not claim leaderboard SOTA. *(We reuse ZonUI's validated LoRA recipe for a 3B VLM on a single 24GB GPU; our contribution is the data-filtering layer and the no-gold generation task, not the training recipe.)*

**2.2 Distillation into Small VLMs.**
Transferring a large teacher VLM into a compact student via SFT on teacher-generated data — without architectural change — is well established: LLaVA-KD (ICCV 2025) and VLsI (CVPR 2025) show small students can match larger models; BLIP's CapFilt (ICML 2022) is the canonical *generate-then-filter* precedent; and ScreenAI (IJCAI 2024) uses a model to synthesize UI training data at scale. DreamStruct (ECCV 2024) fine-tunes a small VLM (LLaVA-1.5-13B) on **code-generated synthetic UI data with programmatic labels** (a synthetic-data method, not teacher-student distillation). We build on the distillation line but differ in the **filtering signal**: rather than self-consistency or a learned filter, we filter teacher outputs against a **structured external source (the View Hierarchy)**, targeting a **high-risk behavior** — naming buttons that do not exist on screen.

**2.3 Self-Training and Faithfulness-Filtered Data.**
The generate → filter → retrain loop underlies STaR (NeurIPS 2022), CapFilt (ICML 2022) and KnowAda (NAACL 2025). Using a structured UI source inside a GUI data pipeline is itself common — UI-Oceanus and Mobile-Agent-v3 (arXiv preprints) filter agent data via the accessibility tree, and MultiUI (ICLR 2025) *generates* instructions from the accessibility tree — but those use the tree for element acquisition, structural dedup, or as a generation source for click-agent data; we instead use the VH to **verify and prune hallucinated element references in human-facing instructions**. We acknowledge that filtered self-training is **not itself novel**; our novelty is two-fold: (i) the filter is a **structured, GUI-specific verifier over a high-risk behavior, not a self-probe**; and (ii) our **primary empirical pillar measures whether faithful behavior persists at inference once the VH filter is removed (app-held-out)**. We treat weight-level internalization as **the hypothesis under test, not a proven mechanism**: persistence is behavioral evidence and cannot by itself rule out image-grounding or a shallow safety-distribution shift; we attribute the effect to the filtered training data via the filtered-vs-RAW ablation (Tier 1). *(Concurrent preprint DocVAL (arXiv 2511.22521) applies a similar distill + structured-source-filter + reference-removed-at-inference recipe to document-VQA with gold bounding boxes; we differ in the GUI, no-gold, human-facing, button-name-existence setting.)*

**2.4 Hallucination and Faithfulness in VLMs.**
Canonical VLM hallucination benchmarks — POPE (Li et al., EMNLP 2023, object-existence yes/no probing) and HallusionBench (Guan et al., CVPR 2024, entangled language hallucination and visual illusion) — evaluate on natural images, while reference-free faithfulness metrics such as ALOHa (NAACL 2024) and FaithScore (Findings of EMNLP 2024), and GUI-specific reduction such as VGA (Findings of EMNLP 2024), assume a reference or reference-free scoring at test time. We instead measure fabrication of UI-element names against a structured View Hierarchy in a **generation** setting with the VH **removed at generation time** and held-out apps. To validate the resulting scores we use independent, cross-family scorers that guard against self-scoring (details in §Setup). *(On feasibility, we adopt LoRA per its documented learn-less/forget-less trade-off — Biderman et al., TMLR 2024 — and treat forgetting as a measured limitation.)*

**FAIR — self-citation note:** FAIR nộp TRƯỚC (15/8) → **không** trích VCL (chưa tồn tại). FAIR phải **tự-chứa** cách chấm tối thiểu (Tier-2 = trụ của chính nó); **không thể defer sang "companion evaluation paper"**. Đưa **liệt kê 3-cơ-chế (bge-m3/judge/token-overlap) xuống §Experimental Setup**, để 2.4 (Related Work) chỉ là đoạn định-vị. Nếu lịch đảo (VCL trước) mới thêm câu dẫn companion (ngôi-ba-ẩn-danh).

---

### 2.B — VCL (tiếng Việt, bài sinh-VN + đánh giá) — Bản thảo Công trình liên quan

> §2. Tiếng Việt. Trục = **đánh giá no-gold + VALIDATE metric + sinh tiếng Việt** (foreground rõ wedge-riêng). Model nhắc 1 đoạn, **trích FAIR ngôi-ba-ẩn-danh**.

**Đóng góp riêng của bài (nêu ngay đầu related-work):** khác với công trình song hành (bài model), bài này tập trung vào **(i) SINH + đánh giá hướng dẫn GUI bằng TIẾNG VIỆT không-tham-chiếu** và **(ii) KIỂM CHỨNG TÍNH HỢP-LỆ của chính thước đo trung thực** — không lặp lại bảng số/kiến-trúc của bài model.

**2.1. Sinh hướng dẫn GUI và mô hình cơ sở.**
Các VLM gần đây được tinh chỉnh để định vị/thao tác trên giao diện (SeeClick, ACL 2024; OS-Atlas, ICLR 2025; UI-R1, AAAI 2026; GUI-Actor, NeurIPS 2025), nhưng đều là *tác tử bấm nút* chấm bằng quỹ đạo vàng. Gần nhất về tác vụ, **UGIF (Findings NAACL 2024)** truy-xuất tài-liệu-trợ-giúp có sẵn và **ground thành macro cho MÁY chạy** (đa ngôn ngữ, giữ hướng dẫn tiếng Anh, chấm task-completion). Bài này kế thừa **mô hình sinh hướng dẫn** được huấn luyện trong **một công trình song hành đang được bình duyệt (trích ẩn danh, ngôi thứ ba)**, và tập trung **sinh + đánh giá hướng dẫn bằng tiếng Việt** trên UI tiếng Anh: khác UGIF ở chỗ **sinh MỚI cho người (không doc nguồn, không gold), và ngôn-ngữ-đích-SINH là tiếng Việt** (không chỉ đổi ngôn ngữ query/UI).

**2.1b. Mô hình thị giác–ngôn ngữ tiếng Việt.** Đã có VLM tiếng Việt — **Vintern-1B** (arXiv preprint 2408.12480, 1B on-device, gần nhất) và **LaVy** (arXiv preprint 2404.07922, kèm LaVy-Bench); **PhoGPT** (arXiv preprint 2311.02945) chỉ là LLM text-Việt (bối cảnh). Chúng tôi chọn **Qwen2.5-VL-3B (train tiếng Anh rồi chuyển-giao Anh→Việt)** thay vì VLM-Việt sẵn có vì backbone này có **phả-hệ grounding GUI mạnh** (UI-R1 AAAI 2026, ZonUI-3B WACV 2026 đều LoRA trên đúng backbone), trong khi Vintern/LaVy hướng OCR/VQA tổng quát, thiếu năng-lực grounding GUI. *(Vintern-1B là đối-chứng định-tính tiềm năng cho smoke-test.)* So với dòng tinh-chỉnh-chỉ-dẫn liên-ngôn-ngữ nhằm CHUYỂN-GIAO năng lực sinh (xCoT, AAAI 2024; X-Instruction, Findings ACL 2024; CrossIn, arXiv preprint/SumEval-2 2025), chúng tôi **không huấn luyện trên dữ liệu tiếng Việt và không đề xuất kỹ-thuật cross-lingual mới**, mà đánh giá độ-trung-thực của hướng dẫn được sinh liên-ngôn-ngữ **zero-shot** trong điều kiện không tham chiếu.

**2.2. Đánh giá sinh không-tham-chiếu.**
Chúng tôi kế thừa khung đánh giá cho văn bản tổng hợp không-đáp-án-chuẩn của **Chim, Ive & Liakata (Computational Linguistics 51(1), 2025)**, và **MỞ RỘNG** khung intrinsic/extrinsic đó bằng một **tín-hiệu-intrinsic mới — đối-chiếu-cấu-trúc-View-Hierarchy** — mà miền text không có (không chỉ là "thêm ảnh"). Về độ trung thực, dựa trên matcher kiểu **ALOHa (NAACL 2024)** và tuyến reference-free **FaithScore (Findings EMNLP 2024)** (kế thừa khung độ-trung-thực của công trình song hành; ở đây tập trung tính-hợp-lệ cho tiếng Việt). Vì hơn 77% ứng dụng thiếu nhãn trợ-năng (**Chen et al., ICSE 2020**), View Hierarchy là *nhãn-bạc* cho hậu-kiểm + fallback, không phải chân-lý. Trong bối cảnh Việt-ngữ, các bộ chuẩn hiện có — **ViGLUE (Findings NAACL 2024), VLUE (Findings NAACL 2024), VMLU (ACL 2025)** — đều thuộc dạng **HIỂU** ngôn ngữ (NLU, có đáp-án-chuẩn); **chưa có bộ chuẩn SINH không-tham-chiếu (NLG no-gold) cho hướng dẫn GUI tiếng Việt** — bài này định vị vào đúng khoảng-trống đó.

**2.3. Kiểm chứng tính hợp lệ của thước đo (ĐÓNG GÓP TRỤ của bài).**
Đóng góp hợp-lệ trung tâm: thay vì lấy tương-quan-người làm cổng đậu/rớt (không còn chuẩn sạch — **Clark et al., ACL-IJCNLP 2021**), chúng tôi kiểm chứng thước đo chính bằng **bơm-lỗi tự động** theo **Sai et al. (EMNLP 2021)** và **BUMP (ACL 2023)** — đo khả-năng-phát-hiện và tính-đơn-điệu với lỗi đã-biết, bơm độc lập với matcher. Công trình song hành dùng thước đo này như **công cụ chấm model**; đóng góp của bài này là **kiểm-chứng tính hợp-lệ của chính thước đo đó** (perturbation = điều kiện cần, chưa phải convergent validity).

**2.4. LLM-as-judge và thiên lệch.**
Do mô hình chấm-bằng-LLM có thiên lệch tự-ưu-ái (**Panickssery et al., NeurIPS 2024**) và các câu hỏi construct-validity (**Measuring what Matters, NeurIPS 2025; Neither Valid nor Reliable, NeurIPS 2025**), chúng tôi chỉ dùng LLM-judge **khác họ với bộ sinh** như *một* trong ba cơ chế chấm độc lập, không lấy làm trục validate chính. *(Mục này VCL-sở-hữu — bài model không có phần judge.)*

**VCL — self-citation note:** VCL **PHẢI trích FAIR** ở 2.1, viết **NGÔI THỨ BA ẨN DANH** ("a concurrent submission under review (Anonymous)"; **CẤM "our/chúng tôi"** — phá double-blind). Trích unpublished-under-review **không** cho bảo-hộ ưu-tiên → lá chắn chống-salami thật = **khác-output (tiếng Việt) + khác-câu-hỏi + nêu-rõ-phần-mới**, không phải bản thân cross-cite. ⚠ **Kiểm chính sách double-blind + concurrent/dual-submission (ngưỡng overlap) của CẢ hai venue trước khi dán.** Nếu FAIR bị bỏ (fallback), đổi 2.1 thành mô tả model tự-chứa + reframe headline VCL sang "phương-pháp-đánh-giá thuần" (report/00 §4).

---

## PHẦN 3 — DỰ TRỮ: Related work nhiều-màn (T11, cho bài mở rộng tương lai — KHÔNG dùng mùa này)

> Đã verify sẵn, cất để bài tiếng-Anh-mở-rộng (FAIR'27/quốc tế). **Không đưa vào FAIR/VCL mùa này.**

- **Sắp thứ tự ảnh xáo:** Sort-Story (**EMNLP 2016**, Spearman) · Wu et al. (ACL 2022, τ) · RankGPT (EMNLP 2023, listwise).
- **Pairwise → tổng hợp:** Qin et al. PRP (**Findings NAACL 2024**) · Copeland/Dwork (**WWW 2001**) · Ailon et al. min-FAS (**JACM 2008**).
- **τ thứ-tự-bộ-phận:** **Fagin et al. (SIAM J. Discrete Math 2006)** + **Lapata (CL 2006)** — KHÔNG gọi "Kendall τ-b".
- **VLM yếu sắp thứ tự thời gian:** TOMATO (ICLR 2025 Poster) · GVL (ICLR 2025).
- **Phân-tầng-một-cue:** Gardner et al. Contrast Sets (**EMNLP 2020**).
- **Prior-art gần (phải phân định):** GUI Knowledge Bench (preprint 2510.26098) · TempVS (preprint) · EZ-Sort (CIKM 2025) · Dodgersort (PAKDD 2026).

---

## PHẦN 4 — Checklist trước khi dán vào bài

- [ ] Mỗi citation: đối chiếu bibtex (venue/năm khớp file này). Mốc dễ sai: **UI-R1 = AAAI 2026** · **Chim = CL 2025** (không "ACL 2025") · **UGIF = Findings NAACL 2024** · **MultiUI = ICLR 2025** · **ScreenAI = IJCAI 2024** · **Widget Captioning = EMNLP 2020** · **Screen2Words = UIST 2021** · **POPE = EMNLP 2023** · **HallusionBench = CVPR 2024** · **ViGLUE/VLUE = Findings NAACL 2024** · **VMLU = ACL 2025** · **xCoT = AAAI 2024** · **X-Instruction = Findings ACL 2024** · **DreamStruct = ECCV 2024** (synthetic-data, KHÔNG distillation).
- [ ] Preprint gắn nhãn "arXiv preprint", KHÔNG như đã-bình-duyệt: **DocVAL (2511.22521)** · **UI-Oceanus (2604.02345)** · **Mobile-Agent-v3/GUI-Owl (2508.15144)** · **Faithful-Agent (2605.01208)** · **Vintern-1B (2408.12480)** · **LaVy (2404.07922)** · **PhoGPT (2311.02945)** · CrossIn (workshop) · ALLaVA/GenRecal/Mind-the-Gap/MobileVLM-V2.
- [ ] **DocVAL:** verify lại venue (ICML 2026?) SÁT ngày nộp FAIR — hiện để preprint.
- [ ] **Scoop đã phân-định:** DocVAL (T3) + dòng lọc-a11y-tree (UI-Oceanus/Mobile-Agent-v3/MultiUI, T3) + wedge (i) thu hẹp 3-trục + Faithful-Agent trùng-tên (T4).
- [ ] **Missing đã bổ:** UGIF + screen-captioning trio (T1b) · POPE/HallusionBench (T4) · VLM-Việt + eval-Việt + cross-lingual (T10-VN).
- [ ] **Framing đã vá:** "internalized→persists" (hedge, FAIR 2.3/T3c) · T4c reference-free reframe · ZonUI feasibility-only · cắt đống grounding còn 4 trụ · FAIR 2.4 chuyển 3-cơ-chế xuống §Setup · nhãn theme "language+contribution" (không "target vs measure").
- [ ] FAIR ↔ VCL: distillation/GUI-model chỉ FAIR; validate-metric/judge chỉ VCL; theme faithfulness viết **câu chữ khác nhau**. 2.4 VCL (judge) KHÔNG trùng FAIR — đừng sửa nhầm thành "kế thừa FAIR".
- [ ] **Self-citation NGÔI-BA-ẨN-DANH** (cấm "our/chúng tôi"); đã kiểm policy double-blind + concurrent-submission từng venue.
- [ ] Self-citation đúng chiều theo thứ-tự-nộp (FAIR trước → VCL trích FAIR).
- [ ] T11 (nhiều-màn) KHÔNG lọt vào FAIR/VCL mùa này.
- [ ] Không câu nào claim SOTA leaderboard; mỗi theme có 1 câu "ta khác gì".
</content>
