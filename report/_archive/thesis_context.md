# THESIS CONTEXT EXPORT (mồi context cho phiên chat mới)

> Dùng file này để cung cấp bối cảnh cho một phiên chat (session) mới với LLM, giúp hiểu ngay đề tài + phương pháp đã chốt.
> File này **đồng bộ với `CLAUDE.md`**; khi mâu thuẫn thì **`report/05_final_plan.md` là nguồn-sự-thật**. Cập nhật lần cuối theo bước ngoặt "Đa bước = SẮP THỨ TỰ MÀN" (Screen-Order Inference).

---

## 1. THÔNG TIN CHUNG VỀ LUẬN VĂN

* **Tên đề tài:** Sinh tự động hướng dẫn sử dụng phần mềm qua LLM, từ use case + ảnh giao diện (UI screenshot).
* **Đầu vào (Input):** Ảnh chụp màn hình + một câu hỏi/use case bằng ngôn ngữ tự nhiên. Hệ có **bộ định tuyến (input router):** **1 ảnh → chế độ đơn bước (DG1)**; **N ảnh (≥2) → chế độ suy luận trật tự màn (DG2)**. (VD đơn bước: "Tôi muốn kiểm tra đã nộp thuế chưa thì vào đâu?".)
* **Đầu ra (Output):** Văn bản hướng dẫn **từng bước** cho con người đọc, bám sát ngữ cảnh ảnh.
* **Tính chất/Khó khăn:** Multimodal (Ảnh + Text → Text). **Không** có sẵn dataset hướng dẫn chuẩn do người viết để làm Ground Truth → đóng góp lõi là **CÁCH ĐÁNH GIÁ khi không có đáp án mẫu**. Phải chạy tổng quát trên nhiều app.

---

## 2. BÀI BÁO THAM KHẢO & CÁCH ỨNG DỤNG

* **Bài báo:** *Evaluating Synthetic Data Generation from User Generated Text* (Chim, Ive, Liakata — **Computational Linguistics 51(1):191–233, MIT Press, 2025** — bài *tạp chí*, KHÔNG phải "ACL 2025"; aclanthology 2025.cl-1.6). Vốn là bài toán **text-to-text rewriting** bảo vệ privacy.
* **Cách dùng:** KHÔNG kế thừa bài toán sinh (họ text→text, ta image→text). **Kế thừa khung ĐÁNH GIÁ** (Intrinsic + Extrinsic). Văn bản hướng dẫn LLM sinh ra = "synthetic text" cần đánh giá khi không có đáp án chuẩn.

---

## 3. FRAMEWORK ĐÁNH GIÁ (ĐÃ CHỐT) — HAI ĐÓNG GÓP DG1 + DG2

> **Trục phân định = "CÓ gold trajectory để chấm hay KHÔNG"** (gold trajectory = chuỗi thao tác đúng có sẵn trong dataset). **Đã bỏ ký hiệu cũ TH1/TH2.** Đã **bỏ hẳn** blind-horizon / observability gap / k* / "Tier B đoán mù từ 1 ảnh".

### DG1 — Tutorial màn-0, KHÔNG có gold tutorial của người (reference-free, neo bằng VH-silver)
* **Meaning → Intent & UI Grounding:** giải đúng nhu cầu? toạ độ [x,y] model click có nằm trong bbox của element trên View Hierarchy (VH) không? (point-in-bbox, SeeClick ACL 2024).
* **Style → Clarity & Format:** đánh số (1,2,3), có động từ hành động (IFEval + G-Eval EMNLP 2023).
* **Divergence → Hallucination:** có sinh thao tác trên nút KHÔNG tồn tại trong VH? (HER/CHAIR EMNLP 2018 + coverage (matcher kiểu ALOHa)).
* *"reference-free" hiểu theo nghĩa hẹp = KHÔNG có tutorial gold do người viết; VẪN neo bằng VH-silver. VH chỉ dùng lúc CHẤM, không đưa cho model lúc sinh (tránh data-leakage).*

### DG2 — Suy luận trật tự màn (Screen-Order Inference), reference-based (AndroidControl, NeurIPS 2024 D&B)
* **Bài toán:** đưa **N ảnh ĐÃ XÁO TRỘN** của 1 luồng đa bước + mục tiêu → model phải (1) **suy ra THỨ TỰ đúng** các màn, (2) **sinh hướng dẫn** theo thứ tự đó. Là bài toán đặt ra **ĐỂ ĐO năng lực suy luận trật tự** — trả lời câu hỏi của thầy *"làm sao model biết trật tự?"*; KHÔNG khẳng định N-ảnh là nhu cầu deploy phổ biến.
* **Model dựa vào 5 ORDERING CUES:** gating (đăng nhập/cấp quyền trước) · nav-affordance (Next/Back/breadcrumb) · state-delta (toggle off→on, ô trống→đã điền) · title-progression · drill-down (màn sau = chi tiết item màn trước).
* **Headline metric = Kendall τ-b** (Kendall 1938 + **Lapata CL 2006** = tiền lệ dùng τ chấm ordering + Gao et al. NAACL 2025 ở vai meta-eval), chấm **partial-order-aware**: chỉ PHẠT khi sai **cặp BẮT BUỘC**; cặp TỰ-DO (vd điền email/sđt) đảo vẫn ĐÚNG.
  * **QUAN TRỌNG (chống vòng-lập-luận):** nhãn "cặp BẮT BUỘC" **suy từ GOLD trajectory** bằng quy tắc tất định (màn B chỉ tới SAU gold-action trên A ⇒ (A,B) bắt buộc) — **KHÔNG** từ bộ phát-hiện cue mà model dùng. Pre-register: tỉ lệ cặp + audit người 50–80 cặp + độ nhạy khi gán nhãn sai 10%.
  * Phụ: pairwise-order-acc, position-acc. Bỏ Exact-Order-Match khỏi headline. Loại N≤2; trục N∈[3, ~10] (chốt trần đường-cong headline N≤6 — LÕI/Gọn; báo thêm tới ~8–10 nếu ngân sách).
* **ORACLE-ORDER (skyline)** = N ảnh đã sắp đúng → chỉ sinh; **SELF-ORDER (thật)** = ảnh xáo trộn → tự xếp rồi sinh. **ordering gap = chất-lượng(ORACLE) − chất-lượng(SELF)** = "cái giá của việc không biết trật tự". Sanity (đã nới): ORACLE ≥ SELF − ε; pre-register test nhạy-thứ-tự (floor-effect) — nếu metric tutorial không nhạy thứ tự thì bỏ gap, giữ τ-b.
* **Tier A (teacher-forced)** giữ làm **trục tham chiếu chuẩn ngành**: mỗi bước đưa model MÀN THẬT của đáp án vàng rồi đoán thao tác kế (Action-Type / Grounding@14% / Step-SR). KHÔNG còn là "đa bước chính", KHÔNG claim ngang leaderboard.
* **Validate độ tin:** pilot chuyên gia BWS (ACL 2017) + Spearman/Kendall + Krippendorff α (N≥60–80) — sanity, không hứa tương quan cực chặt.

> **Nguyên tắc "null vẫn đậu":** đóng góp = quy trình ĐÁNH GIÁ + câu hỏi khoa học có pre-register; kết quả null (đã đăng ký trước) vẫn là đóng góp hợp lệ. Áp cho cả DG1 + DG2.

---

## 4. DỮ LIỆU (3 bộ — vai cố định)

* **MobileViews** (preprint; ảnh + VH + bbox pixel) → **màn-0 / DG1** (chấm grounding).
* **AndroidControl** (NeurIPS 2024 D&B, peer-reviewed; arXiv 2406.03679; 15.283 episode, mean ~5,5 bước, p95=13) → **DG2** (xáo trộn ảnh để đo sắp-thứ-tự) **+ Tier A** (gold action mỗi bước).
* **ScreenSpot / ScreenSpot-v2** (SeeClick ACL 2024 / OS-Atlas ICLR 2025) → **đối chứng grounding** (point-in-bbox của resolver).
* **AITW** (NeurIPS 2023) = **nguồn ngưỡng 14% bắt buộc** (citation) + đối chứng tùy chọn. **Mind2Web = future-work** (nhánh web, chỉ có DOM, không bbox pixel).

---

## 5. PIPELINE ĐỀ XUẤT — ReOrder-Tutor (chi tiết: `report/03_pipeline.md`)

* **Input router (một hệ duy nhất):** N=1 → Stage-0 rỗng → pipeline 5 bước cũ; N≥2 → bật **Stage 0 "Screen-Ordering"**.
* **Stage 0:** S0a feature mỗi màn (tái dùng parser M1) · **S0b ordering reasoner = pairwise-then-aggregate** (hỏi VLM từng cặp "màn nào trước?" + trích ≥1 cue → **Copeland score**, phá-tie tất định; **listwise 1-call** làm đối chứng **fair-compute = cùng tổng LLM-call**; chi phí C(N,2): mốc CHỐT N=6→15 call, minh hoạ N=10→45, p95 13→78 ⇒ chốt trần N≤6 — LÕI/Gọn) · S0c order verifier (code thuần).
* **5 bước trên từng màn:** (1) dò & đánh số nút (OmniParser+OCR) → (2) vẽ số (Set-of-Mark) → (3) **sinh có ràng buộc** (model chỉ được cite ID đã có — CHỐNG BỊA cốt lõi) → (4) kiểm 3 tầng (V1 code membership / V2 LLM-khác intent / V3 self-refine ≤2) → (5) đổi số → toạ độ.
* **Baseline:** E2E-VLM + Self-Refine; **GOAL-ONLY** (che ảnh) + **VISUAL-ONLY** (che mục tiêu, đối xứng) + **RANDOM-ORDER**. **Signal-attribution = stratification cấp một-cue** (KHÔNG che pixel); kết luận cue dựa stratification, không dựa lời model tự khai. **Future-work:** AGENT-NSI (world-model có train).

---

## 6. KILL-TEST & HIỆN TRẠNG

* **10 kill-test (K1, K3–K8 + KN + KZ′ + KB) — BỐN cổng cứng K1/KN/KZ′/KB:**
  * **K1** = tự đo recall detector (cổng go/no-go; recall UI mobile chưa công bố rõ — chỉ có grounding accuracy ~57%, là chỉ số khác).
  * **KN** = tự đếm histogram độ dài episode AndroidControl (đã khảo sơ bộ mean ~5,5 / p95=13 → **GO**).
  * **KZ′** = rà prior-art sắp-ảnh (Sort-Story EMNLP 2016 / "Sequencing Multimodal Instructional Manuals" ACL 2022 / RankGPT EMNLP 2023) → **GO**; **KHÔNG claim "xếp ảnh xáo là mới"**, độ mới = domain GUI + điều kiện hoá mục tiêu + gắn ordering→sinh tutorial + signal-attribution.
  * **KB** = chống leak step-index (strip metadata + tái mã hoá ảnh + UUID + che status bar/đồng hồ/pin/badge + loại episode 2-ảnh trùng-pixel; CI test detector mù không xếp tốt hơn ngẫu nhiên).
* **Giai đoạn:** mới đề cương/ý tưởng. Báo cáo trình thầy ở `report/00`–`08`; **`report/05_final_plan.md` = nguồn-sự-thật**; deck = `LUAN_VAN_SLIDE.pptx`.
* **Việc tiếp theo (tuần 1):** chạy K1 (recall) + KN (histogram) + KB (chống leak) → chốt khung với thầy → P2 harness → P3 ablation ladder C0–C4.

---

## Ghi chú làm việc
* Trao đổi bằng **tiếng Việt**. Khi tư vấn model/giá/API Claude/Anthropic: đọc tài liệu, không trả lời theo trí nhớ.
* **Tiếng Việt = demo định tính** + sanity-check OCR (không có bảng số VN vì không có dữ liệu VH tiếng Việt); định lượng chạy EN/ZH.
* Xương sống phương pháp chỉ trích **peer-reviewed** (ACL/EMNLP/NAACL/CL journal); công cụ (OmniParser/Qwen/SoM) là preprint → chỉ là hiện vật kỹ thuật, không trình như đã bình duyệt. **Không bịa số/citation.**
