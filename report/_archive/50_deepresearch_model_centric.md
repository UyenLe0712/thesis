# Deep research — Phương pháp lấy-model-làm-trung-tâm cho luận văn (BẢN CHỐT)

> Nguồn: workflow deep-research `wf_ed61af89` (chạy 2026-07-08; 101 agent, 19 nguồn → 91 claim → verify đối kháng 25 claim: **20 xác nhận, 5 bác**). Bối cảnh bước ngoặt: thầy yêu cầu luận văn PHẢI train model thật — xem `CLAUDE.md §0` + memory `advisor-pivot-must-train-model`.

---

## 0. KẾT LUẬN MỘT ĐOẠN (đọc cái này trước)

Bằng chứng bình duyệt 2024–2026 hội tụ vào **một công thức chốt**: **fine-tune một VLM nhỏ (Qwen2.5-VL-3B) bằng LoRA cho GUI grounding, rồi hậu-huấn-luyện bằng RL với reward TỰ ĐỘNG DỰA-LUẬT (GRPO/RLVR)** — trong đó **chính tín hiệu point-in-bbox / faithfulness của phương pháp no-gold trở thành HÀM REWARD**. Cách này vừa **"tạo model thật"** (đập tan lời chê "chỉ prompting"), vừa **tái dùng trọn 3 dataset + phương pháp đánh giá đã có** (metric giờ làm 2 vai: reward khi train + thước khi đo).

> ⚠️ **CẢNH BÁO TRUNG TÂM (phải nhớ):** hầu hết precedent là tác-vụ **AGENT bấm-nút CÓ gold**, KHÔNG phải **sinh-hướng-dẫn-cho-người no-gold**. → Đóng góp *model* nên đặt ở **grounding / verifier** (nơi có reward tự động); phần **sinh hướng dẫn** giữ vai **ứng dụng + đánh giá no-gold** (điểm mạnh riêng, không đụng ai).

---

## 1. XẾP HẠNG CÁC HƯỚNG (đã verify)

### 🥇 Hạng 1 — Fine-tune 3B VLM cho GUI grounding bằng LoRA *(hướng b)* — confidence CAO
- **Vì sao nhất:** khả thi nhất trên Colab Pro (24GB) + bằng chứng bình duyệt mạnh nhất; khớp thẳng tài sản ScreenSpot-v2 (bbox) + toạ độ vàng AndroidControl.
- **Bằng chứng:** **ZonUI-3B / Qwen-GUI-3B** (arXiv 2506.23491, *WACV 2026 — bình duyệt*) LoRA Qwen2.5-VL-3B (rank 8, alpha 16) trên **MỘT GPU 24GB, ~24K mẫu** → **84,9% ScreenSpot / 86,4% ScreenSpot-v2**, vượt UI-TARS-2B, ngang baseline 7B. GUI-AIMA-3B (2511.00810, preprint) đạt **92,1% ScreenSpot-v2**. UI-TARS xác nhận fine-tune VLM có-sẵn (không train from-scratch) là lộ trình chuẩn.

### 🥈 Hạng 2 — RL data-efficient (GRPO/RLVR) với reward point-in-bbox tự động *(b + f)* — confidence CAO
- **Vì sao mạnh:** đây là **đòn chống "chỉ prompting" mạnh nhất** — reward chính là metric đánh giá tự động (RLVR), biến phương pháp no-gold thành tín hiệu train; cực kỳ ít dữ liệu.
- **Bằng chứng:** **UI-R1** (arXiv 2503.21620, *AAAI 2026 — bình duyệt, KHÔNG PHẢI AAAI 2025 [sửa 2026-07-12: bài nộp 3/2025 nhưng AAAI chính thức chấp nhận cho kỳ 2026, hội nghị họp 1/2026, Proceedings AAAI Vol.40 Issue 21]*) GRPO trên Qwen2.5-VL-3B, reward `R = R_type + R_coord + R_format`, trong đó **R_coord = 1 nếu toạ độ dự đoán nằm TRONG bbox vàng** (đúng tín hiệu point-in-bbox của luận văn) — reward hoàn toàn tự động, **chỉ 136 mẫu → +22,1% ScreenSpot, +12,7% AndroidControl**. **SE-GUI** (2505.12370, *NeurIPS 2025*) SOTA-scale-7B với **~3k mẫu**. ReGUIDE (2505.15259, preprint) nâng 3B từ 55,5%→87,3% ScreenSpot với 0,2% dữ liệu.

### 🥉 Hạng 3 — Distillation từ teacher lớn + light-RL vào student nhỏ *(a + e)* — confidence TRUNG BÌNH
- **Vì sao:** template cho model nhỏ; **dùng gold-trajectory AndroidControl làm oracle reference chống ảo-giác** (song song trực tiếp ý tưởng distill từ gpt-4o-mini + lọc faithfulness).
- **Bằng chứng:** LiteGUI (2605.07505, preprint — teacher Qwen3-VL-32B, on-policy distill + dual-GRPO), InfiGUI-R1-3B (2504.14239, preprint — distill reasoning rồi RL, 87,5% ScreenSpot, 92,1%/71,1% AndroidControl-Low/High).
- **⚠ Rủi ro:** full-RL 3B + distill có thể **vượt 1 GPU Colab** → phải làm bản LoRA-distill rút gọn. Và đây là tác-vụ agent có gold, không phải sinh no-gold.

### 🛡️ Lá chắn bổ sung — Train một VERIFIER / action-head nhẹ riêng *(d + g)* — confidence CAO
- **Vì sao hay:** biến **lớp faithfulness sẵn có thành một MODEL được huấn luyện thật** (rõ ràng "train model"), mà lại rất nhẹ.
- **Bằng chứng:** **GUI-Actor** (arXiv 2506.03143, *NeurIPS 2025 — Microsoft*) action-head coordinate-free; biến thể **LiteTrain đóng băng backbone, chỉ train 19–103M tham số** → fit 1 GPU. GUI-Actor còn có **grounding verifier train riêng** để chấm+chọn action-region hợp lý — tương tự trực tiếp việc train một verifier phát-hiện-ảo-giác làm đóng góp model.

---

## 2. NEO CITATION (theo luật luận văn: xương-sống chỉ trích bình duyệt)

**Chỉ 4 nguồn THỰC SỰ bình duyệt → dùng làm trụ phương pháp:**
- **UI-R1** — AAAI 2026 (KHÔNG PHẢI AAAI 2025 — sửa 2026-07-12) (RL reward point-in-bbox, 3B, 136 mẫu). `arXiv 2503.21620`
- **SE-GUI** — NeurIPS 2025 (GRPO data-efficient, ~3k mẫu). `arXiv 2505.12370`
- **GUI-Actor** — NeurIPS 2025 (action-head + verifier, LiteTrain nhẹ). `arXiv 2506.03143`
- **ZonUI-3B / Qwen-GUI-3B** — WACV 2026 (LoRA 3B trên 1 GPU 24GB). `arXiv 2506.23491`

**Còn lại = preprint arXiv (LiteGUI, GUI-AIMA, ReGUIDE, InfiGUI-R1, self-distillation…)** → chỉ dùng làm *hiện vật kỹ thuật / template*, KHÔNG làm trụ. ⚠ **Verify lại arXiv ID + venue** trước khi trích (vài ID trông "tương lai" 2605/2606/2511 — kiểm trên arXiv/OpenReview).

---

## 3. CLAIM BỊ BÁC (0-3 / 1-2) — TRÁNH dựa vào

- ❌ **SUQ probe classifier** (dò ảo-giác từ hidden-activation) — **0-3**: đừng làm verifier (hướng d) theo kiểu probe hidden-state.
- ❌ **UI-UG joint understanding+generation cải thiện cả hai** — 0-3.
- ❌ **Model chuyên-biệt nhỏ đánh bại MLLM lớn** — 0-3: đừng claim "3B đánh bại model lớn".
- ⚠ **GRPO-3B ngang/hơn 7B SFT** — 1-2 (yếu, đừng nói chắc). **Grounding = ghép mô tả↔toạ độ chuẩn hoá quy mô 24,4M** — 1-2.

---

## 4. CÂU HỎI MỞ PHẢI TỰ TRẢ LỜI (khe hở trung thực)

1. Với **sinh hướng-dẫn no-gold** (không phải bấm nút), reward tự động nào ngoài point-in-bbox? Faithfulness `1−bịa/bước` có đủ *dày & ít nhiễu* để làm reward RL ổn định, hay **chỉ nên dùng làm bộ lọc distillation**?
2. Bản LoRA-distill + light-RL cho 3B chạy **bao lâu / bao nhiêu VRAM trên Colab Pro L4 24GB** (không phải RTX 4090) với 127 màn MobileViews + subset AndroidControl? Có cần offload/ZeRO?
3. Train **verifier phát-hiện-ảo-giác** thì lấy nhãn +/− ở đâu khi không có gold? → **sinh cặp perturbation tự động (bơm lỗi đã-biết)** có đủ để verifier đạt κ tốt với người không?
4. Đóng góp model đặt ở **grounding (b)** hay **verifier (d)** để vừa thoả "train model" vừa giữ eval no-gold làm điểm mạnh, **KHÔNG biến thành bản trùng InfiGUI-R1/SE-GUI**?

---

## 5. KHUYẾN NGHỊ CHỐT (kiến trúc + train + eval + đóng khung)

**Đặt đóng góp model = "GROUNDING MODEL train bằng RLVR, reward = point-in-bbox tự động", đặt BÊN TRONG hệ sinh hướng dẫn no-gold.**

- **Model & train:**
  - Base: **Qwen2.5-VL-3B-Instruct**, LoRA (rank 8, alpha 16) — Stage 1 SFT grounding, Stage 2 **GRPO/RLVR** với reward = point-in-bbox (+ đúng loại thao tác).
  - **Reward chính = metric no-gold của bạn** → đây là chỗ "phương pháp đánh giá thành tín hiệu train" (điểm mới + chống "chỉ prompting").
- **Dataset:** train grounding trên **ScreenSpot-v2 + AndroidControl (toạ độ/thao-tác vàng)**; **MobileViews + faithfulness** giữ vai **đánh giá no-gold** cho phần sinh hướng dẫn (bọc ngoài, dùng grounding-model đã train để "bấm trúng").
- **Compute:** LoRA 3B nằm trong tầm Colab Pro 24GB (bằng chứng ZonUI/Qwen-GUI-3B). RLVR ít mẫu (UI-R1: 136; SE-GUI: 3k) → **rất vừa túi**.
- **Đóng khung chống "prompting trá hình":** "Em **huấn luyện** một mô hình grounding 3B bằng RL, trong đó **hàm reward chính là thước đo no-gold** em đề xuất; mô hình này là lõi bấm-trúng-nút của hệ sinh hướng dẫn." → có trọng số train, có đường cong học, có ablation SFT-vs-RL.
- **Giữ điểm mạnh riêng (khác InfiGUI/SE-GUI):** họ làm **agent bấm máy**; bạn dùng grounding-model **bên trong bộ sinh hướng-dẫn-cho-người**, với **faithfulness-làm-reward** cho tác-vụ **no-gold** — đó là wedge độc nhất.

**Việc cần chốt với thầy:** đóng góp model trọng tâm là **grounding-RLVR (b+f)** hay thêm **verifier nhẹ (d/g)** — xem câu hỏi mở #4.

---

## 6. CHỐT HƯỚNG + CHI PHÍ (2026-07-08)

- **ĐÃ CHỐT (working direction):** **Option 1 — Grounding-model + RLVR** (Qwen2.5-VL-3B, LoRA SFT → GRPO reward=point-in-bbox). Lý do: hiệu quả/đồng-tiền cao nhất, trụ bình duyệt chắc nhất, rủi ro compute thấp nhất, câu chuyện đẹp nhất (metric = reward). Verifier nhẹ (Option 2) để **Phase 2** nếu còn thời gian. Distill (Option 3) rủi ro compute cao + ít trụ → không làm trọng tâm.
- **Kiến trúc đầy đủ đã viết vào `report/43` Chương 0** (đọc một lần hiểu hết).
- **Chi phí Colab (giá 2026):** Pro $9,99/th · **Pro+ $49,99/th** (background execution) · pay-as-you-go $9,99/100 CU. A100 ~15 CU/h (~$1,5/h), L4 ~$0,4–0,5/h (ước), T4 ~$0,18/h. Cả luận văn ~**40–80 GPU-giờ** → **~$100–150** (Pro+ 2–3 tháng) hoặc **< $50** nếu thuê RunPod/Vast (~$0,4/h GPU 24GB). *(Giá đổi theo thời điểm — kiểm lại khi mua.)*

---

## 7. ⚠️ DEBATE GIÁM KHẢO (2026-07-09) — ĐẢO LẠI KHUYẾN NGHỊ §6

> Chạy debate 5 góc trước khi cam kết (3/5 agent trả về do lỗi hạ tầng, nhưng hội tụ mạnh). **Kết quả: hướng "grounding + RLVR (point-in-bbox=reward)" ở §5–§6 CÓ 3 LỖ HỔNG LỚN — cần đổi trọng-tâm.**

**Lỗ hổng chí mạng:**
1. **Vòng lặp / Goodhart (góc circularity):** point-in-bbox VỪA là reward train VỪA là metric eval → *train-to-the-metric rồi chấm bằng chính nó* = tautology. **Đúng lỗi luận văn từng vá** (matcher vừa-sửa-vừa-chấm) + **mâu thuẫn quyết định M1** (đã rút point-in-bbox khỏi headline vì tautology). *Vá:* point-in-bbox chỉ là **proxy train**, phán quyết dời sang **thước khác họ** (faithfulness đầu-cuối bge-m3) trên **held-out theo APP** + baseline null (center/random) + stratify theo kích thước bbox.
2. **Đặt model SAI CHỖ (góc ý-thầy):** thầy chê "chưa thấy model" là chê **bước SINH hướng dẫn (cốt lõi) đang prompting**. Train một *grounding phụ trợ* KHÔNG trả lời được — bước sinh vẫn prompting. Grounding lại **trùng SOTA có sẵn** (SeeClick/OS-Atlas) → "so leaderboard chắc thua", đúng thứ đã dặn KHÔNG claim; và **rời lá chắn no-gold**. *Vá:* **dời trọng-tâm-train về BƯỚC SINH** — fine-tune/distill một VLM nhỏ sinh hướng dẫn bám-VH, hoặc biến **lớp trung-thực-hoá thành module HỌC ĐƯỢC** (classifier bịa/không-bịa; reranker thứ-tự-màn học từ gold AndroidControl). Grounding giữ vai **off-the-shelf** ở đối-chứng.
3. **Dữ liệu train mỏng + lệch trục (góc khả thi):** 127 MobileViews là **tập ĐO** (train lên thì mất held-out); ScreenSpot là **benchmark** (train lên = leak); grounding-data sạch thực chỉ AndroidControl → mỏng. GRPO reward-thưa trên Colab 1-GPU **bất ổn** (VRAM/session/variance). *Vá:* **SFT-LoRA làm lõi** (ổn định), **GRPO chỉ là thí-nghiệm-thưởng pre-register null**; split **disjoint theo app**; train ≠ tập đo.

**→ KHUYẾN NGHỊ ĐẢO (thay §6):** **Trọng-tâm-train = MÔ HÌNH SINH hướng dẫn** (fine-tune/distill VLM nhỏ: teacher gpt-4o-mini sinh → lớp faithfulness lọc → SFT), HOẶC **module học-được trong lớp trung-thực-hoá** — vì (a) đúng bước cốt lõi thầy đòi, (b) giữ bản sắc no-gold (đánh giá bằng faithfulness, KHÔNG train-to-coordinate), (c) tránh vòng lặp, (d) trùng khớp ý tưởng distillation ban đầu. **Grounding = off-the-shelf**, chỉ để đo point-in-bbox ở đối-chứng (không phải đóng góp model). → Chương 0 report/43 cần viết lại center theo hướng này (đang gắn cờ ⚠️).

**Hai góc còn lại (2026-07-09, đã chạy) — XÁC NHẬN + LÀM MẠNH:**
4. **Độ mới / trùng lặp (chí mạng):** grounding LoRA→GRPO + point-in-bbox = **tái lập UI-R1/SE-GUI đổi tên** ("chạy lại notebook có sẵn") — không mới ở kiến trúc/reward/dữ liệu/tác vụ; và **model không chạm bài toán no-gold trung tâm**. Càng trích UI-R1/SE-GUI/ZonUI càng **tự tố** ở cùng sân. *Vá:* đặt model ở chỗ **reward KHÔNG cần gold** — **faithfulness-rewriter** (học phát-hiện + viết-lại bước bịa) hoặc **model sắp-thứ-tự-màn** = đất trống thật.
5. **Bản sắc no-gold (chí mạng):** grounding CÓ-gold → **phản bản sắc**; output (x,y) **người đọc không dùng** (chỉ agent-bấm-máy dùng — paradigm đã từ chối) → **bolt-on**; luận văn **chẻ đôi** (nửa grounding có-gold, nửa sinh no-gold, không chung RQ). *Vá:* train **module học-được TRONG lớp trung-thực-hoá** (phân loại matched/fabricated, nhãn từ **perturbation bơm-lỗi**, chấm bằng detection-rate/FP/đơn-điệu = đúng pipeline validate no-gold đã pre-register) — model-agnostic, phục vụ TRỰC TIẾP đóng góp; grounding chỉ sống với vai **bộ-dò fallback khi VH thiếu nhãn** (>77% app).

**★ KHUYẾN NGHỊ CHỐT SAU DEBATE (5/5 góc hội tụ) — xếp hạng center MỚI:**
1. **🥇 Module trung-thực-hoá HỌC ĐƯỢC** (classifier/rewriter phát-hiện + viết-lại bước bịa) — train bằng **nhãn perturbation tự sinh** (không cần gold hướng dẫn), chấm bằng detection-rate/FP/đơn-điệu. ĐÚNG trục no-gold, model-agnostic, nhẹ (hợp Colab), là **đóng góp thật sự mới** (reward-without-gold cho faithfulness GUI = chưa ai làm), đúng bước cốt lõi thầy đòi.
2. **🥈 RLVR/GRPO trên GENERATOR** với reward = **điểm faithfulness VH-grounded (bge-m3/VH-consistency), KHÔNG phải point-in-bbox** → "verifiable reward không cần human-gold". (Cẩn thận vòng lặp: reward khác-họ với thước phán quyết + held-out.)
3. **🥉 Model sắp-thứ-tự-màn (Stage-0)** học pairwise từ partial-order-suy-từ-gold.

**Grounding = OFF-THE-SHELF**, chỉ để đo point-in-bbox ở đối-chứng / làm bộ-dò-fallback — **KHÔNG phải đóng góp model.** → Chương 0 report/43 viết lại center theo #1.

---

## 8. DEBATE LẦN 2 (2026-07-09) — SOI CHÍNH HƯỚNG MỚI (5/5 góc)

> Debate hướng #1 (module trung-thực-hoá học được) + #2 (generator-RLVR). **Kết quả: #2 CHẾT; #1 SỐNG nhưng CHỈ với một khung hẹp cụ thể.**

**#2 (RLVR trên generator) — LOẠI KHỎI LÕI (chí mạng):** nặng hơn grounding-RLVR đã bị chê (sinh văn bản dài × K rollout × ảnh, 1 GPU khó hội tụ); reward faithfulness **KHÔNG verifiable** (proxy nhiễu, sai bản chất RLVR) và **tự-hack về "mô tả mơ hồ, không bao giờ nêu tên nút"** → faithfulness cao mà vô dụng; no-gold không có tín hiệu "hữu ích" để cân → bế tắc thiết kế. → **Bỏ (để future-work).**

**#1 (module học được) — 4 lỗ hổng lớn hội tụ:**
1. **Vòng lặp lần 2:** train trên nhãn perturbation rồi chấm bằng chính perturbation = tautology in-distribution; module chỉ "học lại bộ bơm lỗi", chưa chắc bắt bịa THẬT.
2. **Nhãn & thước cùng nguồn matcher/VH:** module chỉ "chưng cất matcher" → không thêm thông tin; "sao không dùng thẳng matcher?".
3. **Trùng lặp + bẫy SUQ:** learned faithfulness verifier ≈ domain-transfer FaithScore/CHAIR; và SUQ-probe đã bị bác (0-3) sẽ lây nếu gọi là "trained hallucination probe".
4. **Không có headroom + thiếu power:** chỗ duy nhất learned thắng embedding (icon-only/nhãn-chung) đã bị **M4 loại khỏi mẫu số**; mẫu 127 màn/~24 app hiệu dụng → delta CI chạm 0, không chứng minh được dù có thật.

**★ KHUNG SỐNG DUY NHẤT cho #1 (5/5 góc cùng chỉ) — phải làm ĐÚNG như sau:**
- **Lý do tồn tại = phủ chỗ MATCHER MÙ**, KHÔNG phải tái tạo matcher: (a) **kịch bản ON-DEVICE KHÔNG có VH** (>77% app thiếu nhãn — Chen ICSE20) → learned model đoán faithfulness từ ảnh+text, matcher rule-based không chạy được ở đây; (b) nút **icon-only / nhãn-chung** matcher bỏ sót → báo metric RIÊNG cho nhóm này.
- **Seed "hướng dẫn đúng" từ AndroidControl gold-action-verified** (có thao-tác vàng → dựng câu đúng THẬT), KHÔNG tự-lọc bằng VLM (tránh vòng lặp với matcher).
- **Perturbation = CHỈ để train + đo độ nhạy**; **cổng đậu/rớt = test-set lỗi-THẬT do người gán** (lấy output bịa thật của gpt-4o-mini/frontier), chấm bằng **thước khác họ** (bge-m3 + người). Báo **gap synthetic→real**.
- **Split leave-apps-out** + mượn **833 app AndroidControl** tăng đa dạng; **pre-register MDE** (nếu thiếu power → khai exploratory).
- **Độ mới phải neo:** verify-với-**VH-có-cấu-trúc** + phân định DỨT KHOÁT khỏi SUQ (hidden-state) và khỏi chính lớp by-construction; (nếu làm được) dùng verifier làm **reward-without-gold** = chỗ chưa ai làm.
- **Nếu chỉ là classifier nhị phân trên embedding đông cứng → thầy chê "chưa phải model".** Nâng thành **fine-tune end-to-end** hoặc **rewriter hợp nhất detect+rewrite** (mô hình sinh có điều kiện = chính deliverable). ⚠ nhưng rewriter cần giám sát mà no-gold không có → chỉ khả thi nếu seed từ AndroidControl gold.

**KẾT LUẬN THẲNG:** sau 2 vòng debate, cả grounding lẫn generator-RLVR đã chết; module học được **sống có điều kiện HẸP** (phủ-chỗ-matcher-mù, seed AndroidControl-gold, test lỗi-thật). Rủi ro thật còn lại: **delta có thể nhỏ + thiếu power** → phải pre-register và chấp nhận "null vẫn đậu". **Trước khi tiêu tiền: chốt khung này với thầy + chạy pilot nhỏ (rẻ, encoder nhỏ/LoRA-head vừa Colab).**

---

## 9. DEBATE LẦN 3 (2026-07-09) — SOI CHÍNH PIPELINE SFT-DISTILLATION (5/5 góc) → **SỐNG, ĐÂY LÀ HƯỚNG CHỐT**

> Ràng buộc mới (user xác nhận): thầy muốn ≥1 **model tự train làm ĐÓNG GÓP CHÍNH** (không cần mỗi bước một model); **đánh giá no-gold = chương PHỤ**; **<3 tháng**, solo, Colab; đề tài CỐ ĐỊNH. → Debate pipeline: **SFT-distillation một VLM nhỏ (Qwen2.5-VL-3B) làm bộ SINH hướng dẫn**. Nhiều agent phán **PASS-CÓ-ĐIỀU-KIỆN** (khả thi + hợp lệ nếu đóng khung đúng). Đây là hướng **tốt nhất** — nhưng phải theo 8 vá dưới đây.

**Tên hướng chốt: "FAITHFUL DISTILLATION"** — chưng cất một VLM nhỏ on-device từ **dữ liệu teacher ĐÃ LỌC BỊA**.

**8 điều PHẢI làm (từ debate), nếu không sẽ bị bác:**
1. **Đóng góp = QUY TRÌNH LỌC-FAITHFULNESS tạo data sạch, KHÔNG phải "distillation".** ("Distill teacher" trần = novelty 0, recipe đã biết.) Novelty: teacher gpt-4o-mini **bịa ~¼**; ta distill từ **bản đã qua lớp trung-thực-hoá**. → **Ablation bắt buộc: train-trên-bản-LỌC vs train-trên-bản-RAW** → cô lập giá trị của lớp lọc = đóng góp đo được.
2. **ĐỔI ESTIMAND (quan trọng nhất):** KHÔNG đo faithfulness-sau-hậu-kiểm (đã bão hoà ~100% → train vô ích). Đo **%fallback ↓ / hữu-ích ở cùng mức faithfulness** (train giảm bịa NGAY LÚC SINH → ít fallback → hướng dẫn cụ thể hơn), VÀ/HOẶC **faithfulness trên màn KHÔNG-VH / recall thấp (tắt hậu-kiểm)** — nơi train là tuyến phòng thủ DUY NHẤT = niche on-device.
3. **Chống vòng lặp:** thước LỌC (nomic) ≠ thước CHẤM (bge-m3 + LLM-judge non-GPT + neo người ~80–120 mẫu, báo κ); **held-out theo APP** (không chỉ theo màn).
4. **Chất lượng target:** teacher bịa 25% × VH mù >77% = nhiễu kép → **đo silent-error của bộ lọc TRƯỚC** (cổng K1, recall-conditioned); cân nhắc **seed target ĐÚNG-THẬT từ AndroidControl gold-action** thay vì teacher tự sinh; loại episode %fallback quá cao (target cụt).
5. **Giữ luật vàng:** distill hành-vi "**mô tả bằng lời khi không chắc**" (từ đầu-ra PA2 hậu-kiểm), KHÔNG distill "tra tên nút từ VH"; input train vẫn **ảnh + câu hỏi**, không VH (kẻo leakage + faithfulness giả).
6. **Thống kê (mẫu ~24 app):** **paired design** (student vs base trên CÙNG màn → paired bootstrap, triệt phương sai giữa-app) + **pre-register MDE** + wild-cluster bootstrap-t; nếu thiếu power → khai "exploratory/đường-cong", **null vẫn đậu**.
7. **Framing claim:** KHÔNG "vượt teacher / SOTA" (chắc thua) → **"đạt faithfulness ngang teacher với 1/50 chi phí, chạy on-device"** + "faithful-by-construction SỐNG SÓT qua distill". Baseline = base model **cùng prompt/pipeline**; báo teacher làm trần.
8. **Khả thi <3 tháng:** **CẮT DG2 (nhiều màn) khỏi train** (eval-only / để bài FAIR); **mở rộng pool màn** (MobileViews public lớn) sinh ~1,5–3k mẫu (teacher API chỉ ~$5–20); **smoke-test 20 mẫu chạy trọn vòng TRƯỚC khi scale**; QLoRA + gradient-checkpointing + save-to-Drive; deadline cứng 3 tuần cho khâu SFT.

**Bảng số tối thiểu phải có:** (a) tỉ-lệ-bịa held-out: base / teacher-raw / teacher-lọc / student (student ≤ teacher-raw); (b) ablation lọc-vs-raw; (c) %fallback + hữu-ích (E16 định tính blind A/B); (d) chi-phí/latency/VRAM (niche on-device); (e) 2×2 {base,train}×{không,có hậu-kiểm}; tất cả kèm CI paired-bootstrap-theo-app.

**→ Đây là hướng CHỐT cho luận văn (VCL, một-màn).** Deep-research #2 (`wf_45ce881b`, literature cho faithful-distillation + on-device VLM) **đang dở — bản thô đã lưu `report/_archive/51_deepresearch_faithful_distillation_partial.md`** (kèm cách resume). Khi có synthesis → chọn trụ bình-duyệt → **VIẾT LẠI Chương 0 report/43** theo Faithful Distillation. **Việc còn thiếu + cách resume: xem `report/51` cuối file.**
