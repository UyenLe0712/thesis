# CLAUDE.md — Bối cảnh luận văn (auto-load mỗi phiên)

> File này được Claude Code tự động nạp khi làm việc trong `D:\Master\Thesis`.
> Mục tiêu: mồi context để LLM hiểu ngay đề tài, bài báo tham khảo, phương pháp luận đã chốt,
> và các điểm còn đang cân nhắc. Chi tiết gốc xem thêm `thesis_context.md`.

---

## 1. Đề tài (CHỐT — yêu cầu của thầy)

- **Tên:** Sinh tự động hướng dẫn sử dụng phần mềm qua LLM, từ use case + ảnh giao diện (UI screenshot).
- **Input của người dùng:** `1 ảnh chụp màn hình UI tĩnh` + `1 câu hỏi/use case bằng ngôn ngữ tự nhiên`
  (VD: "Tôi muốn kiểm tra đã nộp thuế chưa thì vào đâu?").
- **Output:** Văn bản hướng dẫn **từng bước (step-by-step)** cho con người đọc, bám sát ngữ cảnh ảnh.
- **Tính chất:** Multimodal (ảnh + text → text). **Không** có sẵn dataset hướng dẫn chuẩn do người viết
  để làm ground truth. Phải chạy tổng quát trên nhiều app.

### Quy ước quan trọng đã làm rõ
- **Đơn bước vs đa bước:** Người dùng luôn chỉ nhập **1 ảnh**. Output chia 2 loại:
  - *Đơn bước:* câu hỏi giải quyết được ngay trên màn hình trong ảnh.
  - *Đa bước:* phải bấm element → mở màn hình mới → tiếp tục. Model phải **suy luận/dự đoán** các màn hình
    kế tiếp dù chỉ thấy 1 ảnh.
- **Hợp đồng với người dùng:** chỉ `ảnh + câu hỏi → hướng dẫn`. Mọi xử lý bên dưới là hộp đen.

---

## 2. Bài báo tham khảo (CHỐT)

- **Bài:** *Evaluating Synthetic Data Generation from User Generated Text* (Chim, Ive, Liakata —
  **Computational Linguistics 51(1):191–233, MIT Press, 2025**, bài báo *tạp chí* — KHÔNG phải "ACL 2025"; aclanthology 2025.cl-1.6).
  Vốn là bài toán **text-to-text rewriting** để bảo vệ privacy.
- **Cách dùng:** KHÔNG kế thừa bài toán sinh (họ text→text, ta image→text). **Kế thừa khung ĐÁNH GIÁ**
  (Intrinsic + Extrinsic). Văn bản hướng dẫn LLM sinh ra = "synthetic text" cần đánh giá khi không có đáp án chuẩn.

---

## 3. Framework đánh giá (CHỐT)

Khung gồm **HAI nhánh đóng góp song song = DG1 + DG2** (đã bỏ ký hiệu cũ TH1/TH2). **Trục phân định = "CÓ gold
trajectory để chấm hay KHÔNG"** (*gold trajectory* = chuỗi thao tác đúng có sẵn trong dataset), **không** dùng trục
"reference-free vs reference-based" làm trục gốc (vì DG2 vẫn là reference-based).

**Quy ước cấm (bất biến):** (1) **VH CHỈ dùng để CHẤM**, không phải input lúc sinh — lúc sinh trích element từ chính
ẢNH (VLM/OCR/grounding) để tránh data leakage; (2) không để cụm **"reference-free"** đứng trần — luôn kèm "vẫn neo
bằng **VH-silver**" (*silver* = nhãn tự động đủ tin cậy nhưng không phải vàng do người soạn); (3) **không claim Tier A
ngang hàng leaderboard**.

### DG1 — Tutorial màn-0, KHÔNG có gold tutorial của người (neo bằng VH-silver)
Ánh xạ tiêu chí bài báo gốc:
- **Meaning Preservation → Intent & UI Grounding:** giải đúng nhu cầu? tọa độ [x,y] model click có nằm trong bbox của element trên VH không?
- **Style Preservation → Clarity & Format:** đánh số thứ tự (1,2,3), có động từ hành động (Click, Nhập...).
- **Divergence → Hallucination:** có sinh thao tác trên nút KHÔNG tồn tại trong VH không?

### DG2 — Suy luận trật tự màn (Screen-Order Inference), reference-based (AndroidControl, NeurIPS 2024)
**Đổi trục:** thay vì "đoán mù chuỗi từ 1 ảnh", DG2 giờ là bài toán **suy luận trật tự màn**. Input = **N ảnh ĐÃ
XÁO TRỘN** của 1 luồng đa bước + mục tiêu → model phải (1) suy ra **THỨ TỰ đúng** của các màn, (2) sinh hướng dẫn
từng bước theo thứ tự đó. Đây là **bài toán đặt ra ĐỂ ĐO năng lực suy luận trật tự** (trả lời đúng câu hỏi của thầy
"làm sao model biết trật tự") — KHÔNG khẳng định N-ảnh là nhu cầu deploy phổ biến.

**Input router (một hệ duy nhất):** N=1 → đơn bước (DG1 nguyên vẹn, MobileViews màn-0); N≥2 → bật chế độ sap-thu-tu
(DG2). N=1 chính là Stage-0 rỗng → về pipeline cũ.

- **ORACLE-ORDER (skyline):** N ảnh **ĐÃ sắp đúng** + mục tiêu → chỉ sinh hướng dẫn. Là cận-trên: model không phải
  tự xếp.
- **SELF-ORDER (thật):** N ảnh **xáo trộn** → tự xếp rồi mới sinh.
- **ordering gap** = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER) = **"cái giá của việc không biết trật tự"**.
  Sanity cứng: ORACLE-ORDER ≥ SELF-ORDER ở **mọi episode** (vi phạm = bug). Cảnh báo floor-effect: gap chỉ có nghĩa
  nếu metric tutorial NHẠY với thứ tự; nếu không, **τ-b là trục chính**, gap chỉ phụ.

**Metric trật tự — HEADLINE = Kendall τ-b** (nguồn: Kendall 1938 + Gao et al. NAACL 2025 — đã có trong `01_metrics`
Track B). KHÔNG dùng pairwise-acc thô làm headline (tautology). Phụ: pairwise-order-accuracy + position-accuracy@correct-place.
Bỏ Exact-Order-Match khỏi headline (N=3 EM~17% ngẫu nhiên, N≥6 ~0). **Chấm theo thứ-tự-bộ-phận (partial-order-aware):**
chỉ PHẠT khi sai **cặp BẮT BUỘC** (gating/drill-down: đảo là sai thật); cặp **TỰ-DO** (vd điền mail/sdt trước-sau đều
được) đảo vẫn tính ĐÚNG. *Ví dụ:* điền Email/SĐT độc lập → đảo vẫn đúng; đăng-nhập-trước-xem-kết-quả → đảo là sai.
HEADLINE τ-b chỉ tính trên **cặp bắt buộc**; báo THÊM **τ-b-thô** trên toàn tập làm "điểm sàn" (robustness). Loại
N≤2 (N=2 chỉ 1 cặp → τ-b chỉ {−1,+1} vô nghĩa); trục N thực tế N∈[3, ~10].

**Còn Tier A — teacher-forced** giữ làm **trục tham chiếu chuẩn ngành** (thầy expect): mỗi bước đưa model **MÀN THẬT
của đáp án vàng** rồi để model đoán thao tác kế. Metric: **Action-Type accuracy**, **Grounding@14%** (*ngưỡng dung
sai 14%*, trích từ AITW), **Step-SR**. KHÔNG còn là "đa bước chính"; KHÔNG claim ngang leaderboard (setup khác +
recall detector chưa công bố rõ, tự đo ở K1). ORACLE-ORDER là skyline của trục ordering.

**Chất lượng tutorial từng màn** vẫn chấm: grounding (point-in-bbox, SeeClick ACL 2024), hallucination (HER+coverage),
format (IFEval). Mỗi số kèm "recall detector = X% (K1)" + báo RAW vs ORACLE.



## 4. Pipeline đề xuất (chi tiết: `report/03_pipeline.md`)

- **Hệ chính (đề xuất): ReOrder-Tutor** — **SoM-Tutor ⊕ GroundFirst** + **Stage 0 "Screen-Ordering"** đặt TRƯỚC
  pipeline 5 bước hiện tại (một hệ duy nhất, N=1 → Stage-0 rỗng → về pipeline cũ):
  - **S0a per-screen feature:** TÁI DÙNG parser Stage-1/M1 (không thêm module).
  - **S0b ordering reasoner (CHÍNH = pairwise-then-aggregate):** mỗi cặp hỏi VLM "màn nào trước?" + bắt trích ≥1
    ordering cue → tổng hợp bằng **Copeland score**. **Listwise** (1 call ép permutation) làm ĐỐI CHỨNG chạy fair-compute.
  - **S0c order verifier:** code thuần, không LLM; chu trình mâu thuẫn → min-feedback-arc-set xấp xỉ.
  - Chuỗi đã sắp → chạy **pipeline 5 bước cũ** (SoM + sinh có ràng buộc chỉ cite ID đã có + V1 code / V2 LLM-khác /
    V3 self-refine) TRÊN từng màn → grounding chấm ĐẦY ĐỦ mọi bước. VH chỉ vào lúc chấm.
  - **Baseline bắt buộc:** E2E-VLM + Self-Refine; **GOAL-ONLY** (che hết ảnh, chỉ goal+nhãn trong: goal-only đã cao →
    cue giao diện không phải nguồn tín hiệu) + **RANDOM-ORDER**. **Future-work:** AGENT-NSI (world-model có train).
- **5 ORDERING CUES (đặt tên, trả lời câu hỏi thầy "model dựa vào đâu để biết trật tự"):** gating (đăng nhập/cấp
  quyền trước) · nav-affordance (Next/Back/breadcrumb) · state-delta (toggle off→on, ô trống→đã điền, badge 0→1) ·
  title-progression (tiêu đề theo phiếu) · drill-down (màn sau = chi tiết item màn trước).
- **Signal-attribution = STRATIFICATION cấp một-cue:** chỉ giữ cặp phân biệt bởi ĐÚNG MỘT cue, đo acc theo nhóm cue
  — KHÔNG che pixel (che pixel tạo artifact) + phân tích lỗi mở (đọc cặp xếp sai).
- **Thí nghiệm cốt lõi:** (a) ablation DG1 "thêm SoM + verifier tồn-tại có giảm hallucination/tăng grounding không";
  (b) DG2 đo τ-b ordering (SELF-ORDER vs ORACLE-ORDER) + signal-attribution theo cue.
- 🟢 **PHÁN QUYẾT KHẢ THI (`report/04_feasibility.md`): GO — THU HẸP.** Lõi DG1 trên **màn-0 (EN/ZH MobileViews)**.
- **DG2 = SUY LUẬN TRẬT TỰ MÀN (CHỐT, hướng sắp-thứ-tự):** input N ảnh xáo trộn + mục tiêu → model tự xếp rồi sinh
  tutorial theo thứ tự; headline = **Kendall τ-b** chấm partial-order-aware (chỉ phạt cặp bắt buộc). Mạnh hơn cách
  đoán-mù cũ vì grounding chấm đầy đủ mọi màn. Hai cổng cứng **KN + KZ'** đã GO.
  - **Tier A (teacher-forced)** giữ làm **trục tham chiếu chuẩn ngành** (metric Action-Type/Grounding@14%/Step-SR);
    **KHÔNG phải sản phẩm 1-ảnh, KHÔNG claim ngang leaderboard** (setup khác + recall detector chưa công bố rõ, tự đo K1).
  - → **Future-work:** world-model tự-train (AGENT-NSI) + chấm định lượng tiếng Việt + nhánh web Mind2Web.
- **Rủi ro tồn vong:** recall phát hiện element của detector (OmniParser) trên UI mobile dày **chưa được công bố rõ** (nguồn chỉ có *grounding accuracy* ~57% trên ScreenSpot — chỉ số KHÁC, không phải recall); giả thuyết làm việc: có thể chỉ ~một nửa element được dò → mọi số grounding đóng khung **"có điều kiện recall đã đo"**. **Kill-test K1 = TỰ ĐO recall TRƯỚC khi chốt với thầy (cổng cứng).** Thêm 3 cổng mới (xem mục 7): **KN** (tự đếm histogram độ dài episode), **KZ'** (prior-art sắp-ảnh), **KB** (chống leak step-index).
- **Tiếng Việt:** định lượng chạy EN/ZH; VN chỉ là động cơ + sanity-check OCR + demo định tính (nói rõ với thầy sớm — không có bảng số VN).
- **Dataset (cập nhật theo `07`): 3 bộ với VAI CỐ ĐỊNH** —
  (1) **MobileViews** (preprint arXiv, ghi rõ v1/v3 khi trích): ảnh + VH + bbox pixel → **màn-0 / DG1**;
  (2) **AndroidControl** (NeurIPS 2024, peer-reviewed): episode đa bước + gold action mỗi bước → **Tier A (teacher-forced) + DG2 (sắp-thứ-tự)**.
  *Ghi chú:* để đo DG2, **episode bị XÁO TRỘN** (N ảnh các màn của 1 luồng bị đảo thứ tự) rồi model phải xếp lại — gold
  trajectory dùng để verify thứ tự đúng (số liệu episode đã verify: **15,283 episode, 833 app**; train 13,604 ep / 74,722 step;
  mean ~5.5 step/episode — Table 1 ghi 4.8, train tính lại 5.49; percentile-5 = 1 step, percentile-95 = 13 step. Nguồn: Li et al.,
  NeurIPS 2024 D&B, arXiv 2406.03679. **KHÔNG có sẵn số đếm theo từng N → phải TỰ ĐẾM histogram, việc tuần-1 cổng KN**);
  (3) **ScreenSpot-v2** (bản làm sạch nhãn kèm **OS-Atlas, ICLR 2025**; ScreenSpot gốc từ **SeeClick, ACL 2024** — đều peer-reviewed): **đối chứng grounding** (point-in-bbox accuracy của resolver) + bù credibility MobileViews.
  **AITW (NeurIPS 2023) phân vai ĐÔI:** (a) **nguồn ngưỡng 14% = trích BẮT BUỘC** (citation), (b) dataset đối chứng = **tùy chọn**.
  **Mind2Web = future-work** (nhánh web). → Vừa theo thông lệ ≥2 bộ, vừa **bù điểm yếu credibility** của MobileViews.
- **Credibility:** metric hầu hết peer-reviewed (ACL/EMNLP/NAACL/CL journal) — mạnh; công cụ (OmniParser/Qwen/SoM) là preprint nhưng chỉ là hiện vật kỹ thuật. Nguyên tắc: xương sống phương pháp chỉ trích peer-reviewed; không trình preprint như đã bình duyệt.

---

## 5. Đóng góp của luận văn (CHỐT)

**Cả hai song hành:** (a) pipeline sinh tutorial (constrained generation + chống hallucination) là sản phẩm chính;
(b) framework đánh giá hai nhánh DG1 + DG2 giúp bảo vệ kết quả khi không có ground truth.

**Trục phân định hai nhánh đánh giá = "CÓ gold trajectory để chấm hay KHÔNG"** (KHÔNG dùng trục
reference-free/reference-based làm trục gốc, vì DG2 cũng là reference-based):
- **DG1 — đánh giá tutorial màn-0 KHÔNG có gold tutorial của người**, neo bằng VH-silver (chấm grounding + hallucination + clarity).
- **DG2 — SUY LUẬN TRẬT TỰ MÀN (Screen-Order Inference) reference-based trên AndroidControl**: N ảnh xáo trộn + mục tiêu →
  model tự xếp lại thứ tự rồi sinh tutorial theo thứ tự đó; headline = **Kendall τ-b** chấm partial-order-aware (chỉ phạt cặp
  bắt buộc). **Tier A** teacher-forced giữ làm **trục tham chiếu chuẩn ngành** (skyline), **ORACLE-ORDER** là skyline của trục ordering.

Nguyên tắc **"null vẫn đậu"** (kết quả null vẫn là đóng góp nếu đã đăng ký trước) áp **cho CẢ HAI nhánh** khi pre-register.

---

## 6. Các điểm CHƯA CHỐT + khuyến nghị hiện tại

> Đánh dấu rõ "khuyến nghị" — chưa phải quyết định cuối.

> *Lưu ý: nền tảng Mobile + vai 3 dataset (gồm ScreenSpot đối chứng, AITW nguồn-14%) ĐÃ CHỐT ở mục 4; mục 6 chỉ còn liệt những điểm THỰC SỰ chưa quyết (vd model open/closed, nhánh web).*

> *Đã CHỐT (chuyển ra khỏi danh sách chưa-chốt): framing đa bước = **DG2 suy luận trật tự màn** (hướng sắp-thứ-tự: N ảnh xáo trộn → tự xếp → sinh tutorial; headline Kendall τ-b partial-order-aware). Hai cổng cứng **KN** (tự đếm histogram độ dài episode) + **KZ'** (prior-art sắp-ảnh) đã **GO**.*

- **Nền tảng (chưa chốt):** *Khuyến nghị Mobile (đã củng cố bằng nghiên cứu — xem `report/02_datasets.md`)* —
  lý do mạnh nhất: (1) chỉ **MobileViews** có sẵn **bbox pixel** trong VH để chấm grounding; Mind2Web chỉ có DOM
  (không bbox); (2) chỉ MobileViews **Complete Traces** mới neo được đặc tả lõi "suy luận màn hình kế từ 1 ảnh" —
  Mind2Web đưa luôn trang kế thật nên KHÔNG test được điều này. **Mind2Web = future-work nhánh web** + mượn bộ
  metric Task Success chuẩn (Step SR/Element Acc/Op F1).
  *(AndroidControl đã là dataset CHỐT cho DG2 ở mục 4 — không liệt ở đây nữa.)* Dataset đã chốt vai (xem mục 4):
  ScreenSpot/-v2 (grounding — đối chứng cố định), AITW (trajectory mobile — đồng thời là nguồn ngưỡng 14% bắt buộc).
  ⚠️ **Lưu ý phiên bản (đã đính chính):** metric "chính thức" của MobileViews **đổi theo bản** — v1 (9/2024) dùng downstream tasks
  (Tappability/ScreenQA…, split 90/10, so Rico); v3 (11/2025) thay bằng RL GUI grounding (GRPO/VLM-R1) trên ScreenSpot-v2/Pro.
  KHÔNG phải "bịa" — khi trích phải ghi rõ phiên bản. (Dù sao metric chấm tutorial lấy từ `report/01_metrics.md`, không bê metric nội bộ MobileViews.)
- **Model (chưa chốt):** *Khuyến nghị* bắt đầu bằng VLM API (GPT-4o/Claude/Gemini) làm baseline mạnh, không cần GPU,
  tiếng Việt tốt; sau đó thêm **Qwen2.5-VL** (grounding tốt, đa ngôn ngữ, fine-tune được) để so sánh "đóng vs mở".
- **Ngôn ngữ:** Thầy **ưu tiên tiếng Việt**. Dataset chuẩn đa phần tiếng Anh ⇒ chiến lược dung hòa:
  pipeline/metric vốn ngôn-ngữ-độc-lập (chấm bằng tọa độ/bbox/format) → validate metric trên dataset tiếng Anh diện rộng (DG1/DG2);
  xây tập ~120 mẫu **tiếng Việt** trên app VN thật cho chuyên gia chấm + demo định tính.

---

## 7. Hiện trạng

- Giai đoạn: **mới đề cương/ý tưởng**.
- **Đã có (báo cáo trình thầy):**
  - ⭐ `report/00_TONG_QUAN.md` — TỔNG QUAN đọc-là-hiểu (đọc đầu tiên): toàn cảnh đề tài/dataset/pipeline/đánh giá qua ví dụ xuyên suốt.
  - `report/00_CHANGELOG_review.md` — nhật ký review đối kháng (21 sửa + 3 giữ nguyên).
  - `report/01_metrics.md` — bộ metric có citation đã kiểm chứng 2 vòng cho 4 tiêu chí + track validate.
  - `report/02_datasets.md` — 3 bộ dataset chốt + vai (MobileViews màn-0 / AndroidControl đa bước / ScreenSpot đối chứng; AITW nguồn ngưỡng 14%; Mind2Web future-work) + đính chính phiên bản MobileViews.
  - `report/03_pipeline.md` — pipeline đề xuất (SoM-Tutor ⊕ GroundFirst + baseline E2E + future AGENT-NSI), đã chấm đối kháng.
  - `report/04_feasibility.md` — red-team khả thi: phán quyết GO-có-thu-hẹp + bảng rủi ro + 10 kill-test (K1, K3–K8 + KN + KZ' + KB) + đoạn nói với thầy.
  - ⭐ **`report/05_final_plan.md` — KẾ HOẠCH CHỐT CUỐI (nguồn-sự-thật; khi mâu thuẫn với 01–04, file 05 thắng).**
  - `report/06_de_xuat_chot_scope.md` — bản trình thầy chốt scope (dễ hiểu, có đối đáp).
  - `report/07_luan_chung.md` — luận chứng sâu metric/dataset/pipeline (nguồn + venue + cách áp dụng) để bảo vệ scope.
- **Khoá chính (từ `05`):** đóng góp = **quy trình ĐÁNH GIÁ** (null vẫn đậu nếu pre-register); ablation = **THANG BẬC C0–C4** (không phải A/B);
  chấm **cả 2 nhánh trên CÙNG lá VH** (không phải tập E riêng); **resolver đối xứng**; metric chấm ≠ verifier V1; **câu hỏi use-case phải TỰ SOẠN**;
  pilot người = sanity (Kendall + CI-width, N≥60–80). 6 pha có cổng (P0, P1, P2, P2b, P3, P4), **cổng cứng: K1 (recall) + KN (histogram độ dài episode) + KZ' (prior-art sắp-ảnh) + KB (chống leak step-index)**.
- **Việc tiếp theo (kill-test tuần-1):** chạy **K1 (đo recall, cổng go/no-go)** + **KN (TỰ ĐẾM histogram độ dài episode AndroidControl** — khảo sơ bộ mean ~5.5, p95=13 → GO có điều kiện, cần tự đếm chính xác theo từng N) + **KZ' (prior-art sắp-ảnh — đã khảo, GO; lineage Sort-Story EMNLP 2016 / Wu et al. ACL 2022 / RankGPT EMNLP 2023, độ mới = domain GUI + điều-kiện-hoá theo mục tiêu + gắn ordering→sinh tutorial + signal-attribution)** + **KB (xáo trộn PHẢI strip metadata + tái mã hóa ảnh + đặt tên UUID; CI test: detector mù xem pixel không suy ra thứ tự tốt hơn ngẫu nhiên)** → chốt khung với thầy theo §9 file 05 → P2 harness → P3 ablation ladder.

---

## Ghi chú làm việc cho trợ lý
- Trao đổi với người dùng bằng **tiếng Việt**.
- Khi tư vấn về model/giá/API của Claude/Anthropic: đọc tài liệu, không trả lời theo trí nhớ.
- Khi một điểm "chưa chốt" được quyết, cập nhật lại mục 6 (chuyển sang CHỐT) trong file này.
