# 📌 PRE-REGISTRATION — DG1 (đăng ký TRƯỚC khi chạy)

> **Mục đích:** chốt **giả thuyết + ngưỡng + quy tắc quyết định + cấu hình** TRƯỚC khi chạy → **không chạy-lại-tới-khi-đẹp** (chống p-hacking + tốn kém). Mọi kết quả (kể cả null) đều báo theo đúng bảng này.
> **Ngày khoá:** 2026-06-27 (cuối tuần làm DG1 cho VCL). Local + free.
> **Sửa đổi 2026-06-30 (ghi log):** (i) H3 đổi từ "tương quan người (Track B)" → **validate TỰ ĐỘNG bằng perturbation test** (thầy không ưa chấm-người); (ii) câu hỏi đổi sang **gieo-từ-nút-thật + cổng answerability tự động** (bỏ người-duyệt thủ công); (iii) H2 model #2 dùng API cloud (local không-GPU bất khả). Lý do & phân tích đầy đủ: `report/25` PHẦN C.

## 1. GIẢ THUYẾT (bác-được)
- **H1 (chính — hiệu quả lớp trung-thực-hoá):** trên CÙNG model, **design E** (oracle + sửa/fallback) làm **Bịa GIẢM** và **Đúng-nhãn TĂNG** so với **BASE** (model viết tự do), mức chênh **vượt CI** (paired bootstrap, cận-dưới > 0).
- **H2 (model-agnostic):** dấu chênh ở H1 **dương trên ≥2 model sinh** (local Qwen bất khả vì không-GPU → model #2 dùng API cloud, vd gpt-4o; hoặc hạ H2 future-work).
- **H3 (metric ĐÁNG TIN — validate TỰ ĐỘNG, KHÔNG chấm-người):** metric vượt **bộ perturbation/sensitivity test** với ngưỡng pre-register: (a) *detection rate* bắt lỗi bơm-vào ≥ ngưỡng; (b) *false-positive rate* (vu oan khi không lỗi) ≤ ngưỡng; (c) *đơn-điệu* (bơm nhiều lỗi → điểm giảm). *(Thầy không ưa chấm-người → bỏ tiêu chí "tương quan với người". Track B = tùy chọn, 1-người, future-work; KHÔNG nằm trong đậu/rớt.)*

## 2. METRIC + CÁCH ĐO (chốt, không đổi sau khi chạy)
- **Bịa / Faithfulness:** matcher **ALOHa** (embedding `nomic-embed-text`, cosine), ngưỡng **τ = 0.55**. `Faithfulness = 1 − tỉ-lệ-bịa`.
- **Đúng-nhãn / Clarity:** so **chính xác** (chuẩn hoá chuỗi).
- **Grounded-existence:** tên khớp **một** nút thật trên cây-nút. *(ScreenSpot dùng riêng làm đối chứng point-in-bbox độc lập.)*
- **Format:** checklist máy-kiểm (đánh số · động từ mệnh lệnh đầu bước · 1 việc/bước) — strict + loose.
- **Coverage (proxy):** % nút actionable được nhắc. **CÔNG BỐ RÕ là proxy** (MobileViews không có gold → không làm headline).
- **Báo cặp [Bịa, Coverage]** cùng nhau.

## 3. QUY TẮC QUYẾT ĐỊNH (null vẫn đậu)
- H1 đạt (chênh vượt CI) → "lớp trung-thực-hoá cải thiện faithfulness/đúng-nhãn, lượng hoá được".
- H1 **không** đạt → **null vẫn báo:** "trong điều kiện đo, lớp không cải thiện faithfulness — và đây là cơ chế (vd recall/oracle đã chặn trần)". KHÔNG đổi metric để cố ra dương.
- H3 không đạt (metric trượt perturbation test) → báo thẳng "metric chưa đủ nhạy/đặc-hiệu, cần hiệu chỉnh matcher/ngưỡng" (giới hạn, không giấu). KHÔNG đổi test cho đậu.

## 4. CẤU HÌNH CỐ ĐỊNH TRƯỚC
- **Màn:** danh sách màn khoá trước (≈60–80), không thêm/bớt sau khi thấy kết quả.
- **Câu hỏi:** **GIEO TỪ NÚT-THẬT trong VH** (affordance-seeded: lấy target X actionable → model viết câu hỏi tự nhiên có lời-giải dùng X) + **CỔNG ANSWERABILITY TỰ ĐỘNG** (giữ câu chỉ khi mục-tiêu ánh xạ ≥1 nút thật; báo drop-rate). Model sinh câu hỏi (M1) ≠ model viết hướng dẫn (M2). Prompt khoá trước. *(Bỏ khâu người-duyệt thủ công; mọi cổng đều tự động.)*
- **Prompt sinh + prompt sửa:** khoá nguyên văn.
- **Model:** Qwen2.5-VL **3B** (chính) + **7B** (subset). Bước SỬA dùng **model KHÁC** (llama3.2).
- **Matcher τ = 0.55** (đã chọn từ tự-kiểm EN: synonym ~0.6–0.69, khác-nghĩa ~0.39).

## 5. CỠ MẪU + THỐNG KÊ
- DG1: ~60–80 màn × {BASE, design E} × {3B, (7B subset ~30)}.
- **Paired bootstrap CI** cho chênh BASE↔design E (per-màn delta); báo **effect size + CI-width**.
- **Validate metric (H3) = PERTURBATION TEST tự động:** với ~tất cả màn, sinh phiên-bản-lỗi (bơm nút-ma / đồng-nghĩa / phá-format / đổi-nút-đúng) → đo detection & false-positive & đơn-điệu, kèm CI. **Không** cần annotator.
- **Track B (chấm-người):** **tùy chọn, future-work**, nếu hội đồng đòi đối-chiếu người thì chạy sanity nhỏ do **chuyên gia** (gold-curated), đóng khung là phụ — KHÔNG trong tiêu chí đậu/rớt.

## 6. GIỚI HẠN CÔNG BỐ TRƯỚC (trung thực)
- Quy mô nhỏ (~60–80 màn), model mở nhỏ → tín hiệu, không phải bảng SOTA.
- Đa dạng app **tuỳ dữ liệu lấy được** (nếu chỉ 1–2 app → ghi rõ là giới hạn external validity).
- Validate metric bằng perturbation = chứng minh **độ nhạy/đặc-hiệu nội-tại**, KHÔNG thay được "người-dùng-thật-thấy-hữu-ích" (cái đó là future-work UX).
- Coverage = proxy (không gold).
- "Recover về nút thật" chứng minh trung-thực, **chưa** chứng minh đúng-mục-tiêu (đó là Step-SR/DG2/FAIR).

## 7. PROTOCOL CHỐNG-VÒNG-LẬP-LUẬN + VALIDATE MATCHER/JUDGE (chốt sau deep-research; TRỤ peer-reviewed ở `27` §7)
- **2 tầng tách biệt:** QUYẾT matched/fallback = **nomic** (τA freeze); CHẤM = 3 cơ chế KHÁC HỌ [bge-m3 + LLM-judge KHÁC-HỌ-generator (generator=gpt-4o-mini → judge KHÔNG dùng GPT-family) + token-overlap]. Headline = **tỉ-lệ-bịa-BASE** (không phải ~100% sau sửa).
- **Matcher đo theo NGỮ NGHĨA (không so chuỗi thô), validate vs người** trên 80–120 cặp gán-tay: báo **P/R + Cohen's κ** (không chỉ %); τ chọn theo precision≥0.95, **FREEZE trước khi chạy**. [TRỤ: **Petryk et al., ALOHa — NAACL 2024**; bổ trợ CHAIR EMNLP 2018. Caveat: ALOHa không báo tương quan → tương-quan-định-lượng dựa Sai et al.]
- **Gán-tay tối thiểu = few-pairwise/HITLC** (pre-label + người chỉ duyệt vùng-bất-đồng → **giảm tới ~80%** số nhãn). [TRỤ: **Mohankumar & Khapra, Active Evaluation — ACL 2022, Outstanding Paper**. *Đính chính:* con số peer-reviewed là **~80%**, KHÔNG phải "89%" (89% + "chỉ-chấm-vùng-bất-định" là ý uncertainty-sampling nội-bộ, chưa có trụ bình-duyệt).]
- **Judge khác họ + vẫn neo người**; **KHÔNG** validate judge bằng nhãn LLM. Nếu dùng quy trình 2-bước (r≥0.80 → z-score kappa) thì **baseline κ người-người TỰ ĐO lại** trên tập mình (không mượn 0.801). [TRỤ: **Panickssery, Bowman & Feng — NeurIPS 2024** (self-preference); bổ trợ **Zheng et al. — NeurIPS 2023** (self-enhancement bias). Preprint chỉ bổ trợ: 2510.09738 / 2505.19176 / 2508.06709]
- **VH/a11y KHÔNG phải ground truth hoàn hảo** (>77% app thiếu nhãn) → biện minh lớp hậu-kiểm + fallback-mô-tả. [TRỤ: **Chen et al. — ICSE 2020**, Distinguished Paper; bổ trợ Ross et al. TACCESS 2020]
- **Validate metric CHÍNH = perturbation tự động** (bơm lỗi đã-biết → đo detection/false-positive/đơn-điệu; adapt sang miền UI). [TRỤ: **Sai et al. — EMNLP 2021**; bổ trợ Ribeiro et al. CheckList ACL 2020]
- **BỎ human-correlation làm cổng đậu/rớt** (human-eval không phải chuẩn vàng tuyệt đối). [TRỤ: **Clark et al. — ACL-IJCNLP 2021**; bổ trợ Karpinska et al. EMNLP 2021]
- Nguyên tắc: mỗi quy tắc trụ có ≥1 nguồn peer-reviewed; nguồn preprint chỉ dùng bổ trợ/động cơ. **Cả 6 nguyên tắc GIỜ ĐÃ có trụ bình-duyệt** (xác minh `27` §7).

## 8. CẬP NHẬT SAU DEBATE PIPELINE (2026-07-02 — pre-register M1–M5, chi tiết `report/40` §4)
> Các quyết định dưới đây được **chốt TRƯỚC khi chạy bản chính**. Ghi ở đây để mai thực thi.

- **M1 — Grounding "đúng-chỗ" RA KHỎI nhánh một màn.** Metric point-in-bbox **chỉ dùng ở nhánh nhiều màn** (AndroidControl có gold-coords) HOẶC đối chứng trên ScreenSpot-v2. **KHÔNG** đưa vào headline một-màn (tránh tautology tâm-bbox). Nhánh một màn headline = độ trung thực; đúng-nhãn = phụ. *(Vì bộ trỏ độc lập kiểu ScreenSpot chưa dựng; nếu lấy tâm bbox đã khớp → 100% giả.)*
- **M2 — Thêm CỔNG CỨNG K-pair cho DG2 (song song K1).** TRƯỚC khi tổng hợp Copeland: đo **độ chính xác so-cặp THÔ** của VLM so gold trên cặp bắt-buộc; pre-register ngưỡng **> ngẫu-nhiên có ý nghĩa** (cluster-bootstrap theo app). Nếu ~0.5 → Stage-0 vô hiệu, khai thẳng. **Phá vòng KHÔNG dùng self-reported confidence của VLM** (calibrate kém) → dùng **margin-Copeland / self-consistency / min-cardinality feedback-arc-set**. Bắt buộc **ablation phá-vòng**: min-FAS vs cắt-ngẫu-nhiên vs không-phá-vòng. Baseline τ phải vượt: shuffle + heuristic đọc-top-down + listwise-một-phát.
- **M3 — Thống kê small-G.** Đổi §5 sang **wild-cluster bootstrap-t (Cameron-Gelbach-Miller 2008)** làm chính (17 app = 17 cụm < ~40 → cluster-robust thường hẹp giả tạo); báo số-cụm + caveat under-coverage. **Timestamp pre-registration = `git init` + commit file 22 TRƯỚC khi chạy 81 màn** (repo hiện chưa git → dễ bị quy post-hoc). Mọi số hiện tại đóng khung **"exploratory"** cho tới khi chạy confirmatory.
- **M4 — Headline tỉ-lệ-bịa "có điều kiện recall-VH".** TÍNH độ-phủ-nhãn VH trên mv_multiapp (script `harness/dg1_vh_coverage.py`, chạy mai); **loại nút icon-only / nhãn-chung khỏi mẫu số**; báo tỉ-lệ-bịa dạng **khoảng** (raw matcher = trần vì nút khuyết-VH bị tính oan). Đối chiếu Chen ICSE20 (>77% app thiếu nhãn). Hạ "~¼" xuống "quan sát sơ bộ, 1 model", KHÔNG làm headline-phát-hiện tổng quát.
- **M5 — "Ngang nhau CÓ ĐIỀU KIỆN".** Ở 36/38/slide: đổi "hai đóng góp ngang nhau" → **"ngang nhau CÓ ĐIỀU KIỆN (chờ DG2/Step-SR dương)"**; dời trụ chống-"chỉ-engineering" sang **3 chân ĐÃ CÓ** (đối-chứng-thất-bại đoán-nút→silent-error · tỉ-lệ-bịa-bản-gốc · %fallback); thêm 1 dòng giới hạn "nếu Step-SR null, A đứng bằng hệ-công-cụ + kết-quả-âm đo được, không tuyên ngang B ở nửa đa-màn cho tới khi có số".
