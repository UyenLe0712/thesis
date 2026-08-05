# report/61 — Deep-research Faithful Distillation: ĐÃ verify đối kháng (tiếp report/_archive/59)

> **TRẠNG THÁI: XONG.** Đây là bản chốt của deep-research bắt đầu ở `report/_archive/59` (chỉ mới xong Scope→Search→Fetch, claim thô chưa kiểm chứng). Lượt này chạy tiếp **Verify 3-phiếu đối kháng + Synthesize** (workflow `wf_8b7b6632-375`, resume 2026-07-16). `report/_archive/59` giữ lại làm log nguyên liệu thô, **đừng trích trực tiếp từ đó** — mọi claim ở đây đã qua ≥3 phiếu, cần ≥2 phiếu bác mới bị loại.
>
> **Kết quả xác minh:** 25 claim đưa vào vòng phiếu → **20 sống (3-0 đồng thuận tuyệt đối), 5 bị bác** (2 phiếu bác trở lên). Không có claim nào rơi vào trạng thái "không xác minh được" (verifier không lỗi hạ tầng). Tỉ lệ bác ~20% xác nhận đúng lo ngại nêu ở report/_archive/59 — vài claim "nghe hợp lý" đã bị lật khi tra kỹ.
>
> ⚠️ **Quy tắc trích dẫn (theo CLAUDE.md):** trong 20 claim sống, chỉ một phần có venue bình duyệt xác nhận — xem cột nguồn ở mỗi mục. Preprint chỉ dùng bổ trợ/bối cảnh, KHÔNG làm trụ trích dẫn chính khi đưa vào report/54 hay report/57 (Related Work).

---

## Tóm tắt điều hành (trả lời trực tiếp 6 câu hỏi gốc)

1. **DPO trên cặp (raw bịa, đã lọc) sinh miễn phí từ bước lọc GUI, verifier ngoài có cấu trúc:** **KHÔNG có tiền lệ.** Đây là khoảng trống thật — nhưng cũng đồng nghĩa không có công thức nào để bắt chước, rủi ro thực thi cao.
2. **Mode collapse/template memorization khi SFT trên fallback string lặp:** rủi ro **có cơ sở lý thuyết** (GEM, ICLR 2025) nhưng **chưa ai đo trực tiếp đúng kịch bản này** (một template rewrite hẹp). Không được coi là đã giải quyết.
3. **Risk-coverage/AURC thay cho cặp rời "tỉ-lệ-bịa + %fallback":** khung này **tồn tại và vận hành được trong literature liền kề** (GUI grounding, LLM/VLM calibration) — có cơ sở phương pháp luận vững để áp dụng, nhưng chưa ai làm đúng trong miền sinh-hướng-dẫn-GUI, và không nguồn nào nói thẳng "đây là bản thay thế của cặp rời".
4. **Filter-then-train vs constrained/grounded generation — so trực tiếp:** **không tìm thấy.** Hai trường phái tồn tại song song, chưa ai đặt cạnh nhau trên cùng task.
5. **77% (Chen ICSE 2020) đo lại 2023-2026 + fusion VH+OCR+icon-detector:** đã có **đo lại gián tiếp** (Fok CHI 2022, 55.6% mức phần-tử — khác đơn vị đo, không đối chiếu thẳng với 77%). **Không tìm thấy** công trình nào fusion VH+OCR+icon-detector cho đúng mục đích tăng recall nhãn accessibility.
6. **Đóng góp mạnh nhất nếu không giới hạn thời gian** — xếp hạng: **(a)** khung selective-prediction/abstention bám-VH đo bằng risk-coverage/AURC (tính mới cao nhất, khả thi 1 GPU Colab) → **(b)** so sánh trực tiếp filter-then-train vs constrained-generation (lấp khoảng trống thật, rủi ro thấp) → **(c)** DPO trên cặp miễn phí từ bước lọc (tính mới tuyệt đối cao nhất, rủi ro thực thi cao nhất).

---

## Chi tiết theo từng câu hỏi

### Q1 — DPO/preference-learning trên cặp tự sinh từ bước lọc (miền GUI, verifier ngoài có cấu trúc)

**Kết luận: khoảng trống thật, KHÔNG bị scoop.**

- **HII-DPO** (preprint, arXiv 2602.10425) dùng GroundingDINO (verifier ngoài có cấu trúc) — nhưng cặp DPO đến từ pipeline **ảnh phản-thực-tế xây riêng** (che/ẩn vật thể để ép model bịa), không phải sản phẩm phụ của một bước lọc sẵn có như thiết kế luận văn.
- **LPO** (ACL 2026 Findings — peer-reviewed, arXiv 2506.09373) dùng **GRPO**, không DPO, và nhắm toạ độ click chứ không phải tên nút bịa.
- **HalluClear** (preprint, arXiv 2604.17284) — GUI-agent hallucination, dùng GRPO reward luật-định; "DPO/preference" xuất hiện **0 lần** trong toàn văn.
- **VPD — Visual Program Distillation** (CVPR 2024, peer-reviewed) là bài GẦN NHẤT cùng họ filter-then-train (lọc rồi SFT) nhưng chỉ dùng SFT loss thuần, không có bước preference-learning đối chiếu raw-vs-filtered.

→ Chưa ai ghép đúng công thức "DPO + cặp miễn phí từ bước lọc sẵn có + verifier ngoài có cấu trúc" trong miền GUI. Nếu luận văn làm, đây là phần tính-mới cao nhất — nhưng vì không có tiền lệ, không có ai để "sao mã cách làm", nên rủi ro kỹ thuật (pha hyperparameter, cân bằng, ổn định DPO) toàn phải tự dò.

### Q2 — Mode collapse / template memorization khi SFT trên fallback string lặp

**Kết luận: rủi ro có cơ sở lý thuyết, CHƯA có bằng chứng trực tiếp đúng kịch bản.**

- **GEM** (ICLR 2025, peer-reviewed) xác nhận: CE-loss trong SFT chuẩn tối đa hoá likelihood dữ liệu quan sát mà không tính khả năng thay thế → dẫn tới over-memorization + giảm đa dạng đầu ra. Cách sửa đề xuất = entropy regularization (reverse-KL). **Nhưng** claim mở rộng "GEM được framing rõ ràng như thuốc chữa mode-collapse-do-lặp-fine-tune-trên-văn-bản-hẹp" đã **bị bác (1-2 phiếu)** — cơ chế nền đúng, nhưng bài không framing đúng như vậy.
- **R-Tuning** (NAACL 2024, Outstanding Paper) xác nhận đúng động cơ Q2/Q3: instruction-tuning cũ ép model trả lời bất kể có biết hay không → dẫn tới bịa. **Nhưng** claim "R-Tuning là tiền lệ cụ thể cho supervision-không-collapse thay thế một fallback string lặp" đã **bị bác (0-3 phiếu)** — R-Tuning refusal data KHÔNG phải một template đơn lặp lại theo đúng nghĩa thiết kế luận văn đang lo.

→ Hai bài này làm nền lý thuyết tốt nhưng không phải bằng chứng đã-giải-quyết. **Đây là câu hỏi thực nghiệm bỏ ngỏ** — luận văn có thể phải tự đo (ví dụ: so đa dạng lexical của output trước/sau SFT trên fallback template) chứ không trích được số có sẵn.

### Q3 — Selective prediction/abstention + risk-coverage/AURC

**Kết luận: khung phương pháp luận vững, khả dụng, nhưng "thay thế cặp rời" là suy luận của luận văn chứ chưa ai làm mẫu.**

- **CAP** (ACML 2025, PMLR v304 — peer-reviewed) train chính sách RL chọn ngưỡng rủi ro conformal (point/set/abstain) theo từng input; báo cáo dùng **AUARC** (diện tích dưới đường risk-coverage) + AUROC cho phát hiện bịa, coverage mục tiêu 90% cố định.
- **SafeGround** (preprint, 2/2026) formal hoá GUI-grounding-uncertainty thành selective prediction, hiệu chỉnh ngưỡng test-time với đảm bảo FDR thống kê.
- Claim mở rộng "các chỉ số này ĐƯỢC DÙNG THAY VÌ báo cặp tỉ-lệ-rời" đã **bị bác (0-3 phiếu)** — các bài chỉ chứng minh chỉ số này tồn tại và vận hành được, không có bài nào minh hoạ trực tiếp việc "thay thế" một cặp số rời có sẵn.

→ Đây là hướng nâng cấp thước đo **có cơ sở thật** (không phải bịa ra một framework mới) — nhưng việc "đổi headline từ tỉ-lệ-bịa+fallback sang risk-coverage" là quyết định thiết kế của luận văn, không phải điều literature đã xác nhận là chuẩn.

### Q4 — Filter-then-train vs constrained/grounded generation: so trực tiếp?

**Kết luận: không tìm thấy so sánh trực tiếp — khoảng trống, không nghiêng bên nào.**

- **CapFilt/BLIP** (ICML 2022) xác nhận đúng công thức filter-then-train.
- **Grounded Decoding** (NeurIPS 2023) xác nhận đúng công thức constrained/grounded generation (product-of-experts lúc decode) — nhưng miền robot, không benchmark với bất kỳ baseline filter-then-train nào.
- VPD (CVPR 2024) cũng không có ablation nào so với constrained/grounded decoding.

→ Hai trường phái sống song song trong literature, chưa ai đặt cạnh nhau trên cùng task. Nếu luận văn tự làm so sánh này (dù chỉ nhỏ, trên 1 GPU), đó là lấp khoảng trống thật với rủi ro thấp — không cần đấu với ai đã làm trước.

### Q5 — Đo lại 77% (Chen ICSE 2020) + fusion VH+OCR+icon-detector

**Kết luận: có đo lại gián tiếp, không có fusion.**

- **Fok et al.** (CHI 2022, peer-reviewed, crawl 312 app / 16 tháng): **55.6%** phần-tử ảnh duy nhất thiếu nhãn — đây là số đo-lại-thật hậu-2020, nhưng ở **mức phần-tử** (Chen đo mức app) nên không đối chiếu thẳng được với 77%; bài trích Chen chỉ 1 lần ở câu không liên quan.
- Phương pháp Fok thuần VH-field-parsing, **không có bước OCR/icon-detector** nào bù false-negative.
- **UIED** (ESEC/FSE 2020, peer-reviewed) là bộ dò OCR+CV+CNN thật — nhưng là phương án **thay thế VH hoàn toàn**, không phải fusion VỚI VH để tăng recall nhãn.
- **Explorer** (preprint 2025) xây bộ dò đa-tín-hiệu riêng nhưng không so sánh định lượng với baseline VH-only.

→ Khoảng trống fusion VH+OCR+icon-detector cho bài toán missing-label **vẫn mở** — không ai đã làm, luận văn không bị scoop ở điểm này.

### Q6 — Đóng góp mạnh nhất nếu không giới hạn thời gian (xếp hạng)

1. **Khung selective-prediction/abstention bám-VH, đo bằng risk-coverage/AURC.** Tính mới cao nhất vì **chưa ai dùng VH làm tín hiệu chất lượng cho abstention** — dòng gần nhất (Trust the Right Teacher, self-distillation GUI-grounding, 2026 preprint) dùng tín hiệu rollout NỘI BỘ của chính model, không dùng nguồn ngoài có cấu trúc. Khả thi 1 GPU Colab: **ZonUI-3B** (WACV 2026, peer-reviewed) là tiền lệ trực tiếp — train FULL một VLM 3B trên 1 RTX 4090 tiêu dùng, đạt hiệu năng GUI-grounding tương đương model lớn hơn.
2. **So sánh trực tiếp filter-then-train vs constrained-generation.** Lấp khoảng trống thật (Q4), rủi ro thấp vì không phải cạnh tranh tính-mới với ai.
3. **DPO trên cặp miễn phí từ bước lọc VH.** Tính mới tuyệt đối cao nhất (Q1) nhưng rủi ro thực thi cao nhất — không có công thức tiền lệ để dựa vào, phải tự dò từ đầu.

> Xếp hạng này là **tổng hợp/suy luận** từ các claim con đã verify riêng lẻ (không phải một claim đơn được đưa qua phiếu trực tiếp) — độ tin **medium**, không phải **high** như 5 câu trên.

---

## Claim đã bị verifier bác (giữ lại để minh bạch — ĐỪNG dùng làm bằng chứng)

| Claim | Phiếu | Nguồn |
|---|---|---|
| HII-DPO's core novelty = ảnh phản-thực-tế iterative-masking, khác cơ chế cặp (raw,filtered) văn bản | 1-2 | arXiv 2602.10425 |
| GEM's core mechanism được framing rõ ràng là thuốc chữa mode-collapse-do-lặp-fine-tune | 1-2 | ICLR 2025 proceedings |
| Diversity collapse phụ thuộc chủ yếu vào dữ liệu upstream (CoT hẹp) hơn là phương pháp train | 0-3 | arXiv 2604.16027 |
| R-Tuning's refusal data là tiền lệ cụ thể thay thế một fallback string lặp | 0-3 | NAACL 2024 |
| CAP cải thiện AUROC/AUARC so với conformal tĩnh, chứng minh risk-coverage "thay thế" cặp rời | 0-3 | ACML 2025 / PMLR v304 |

---

## Nguồn peer-reviewed chắc chắn (dùng làm trụ trích dẫn được)

- **GEM** — ICLR 2025 (entropy-regularized SFT, chống over-memorization)
- **R-Tuning** — NAACL 2024, Outstanding Paper (refusal-aware fine-tuning)
- **CAP** — ACML 2025, PMLR v304 (conformal abstention policy, RL)
- **Chen et al.** — ICSE 2020 (>77% app thiếu nhãn, mức APP)
- **Fok et al.** — CHI 2022 (55.6% phần-tử ảnh thiếu nhãn, longitudinal 16 tháng)
- **VPD (Visual Program Distillation)** — CVPR 2024
- **CapFilt/BLIP** — ICML 2022
- **Grounded Decoding** — NeurIPS 2023
- **UIED** — ESEC/FSE 2020
- **ZonUI-3B** — WACV 2026 (đã accept, hội nghị họp đầu 2026 — xác nhận qua abstract+GitHub, chưa qua proceedings chính thức)
- **LPO** — ACL 2026 Findings

**Preprint chỉ dùng bổ trợ/bối cảnh (chưa xác nhận venue bình duyệt):** HII-DPO, HalluClear, SafeGround, Trust the Right Teacher, Explorer.

---

## Câu hỏi mở còn treo (chưa có nguồn trả lời)

1. Có công trình nào (kể cả preprint rất mới, ngoài phạm vi tìm kiếm lần này) ghép DPO + cặp-miễn-phí-từ-filter + verifier-VH đúng trong miền sinh-hướng-dẫn-GUI (không chỉ GUI-grounding-toạ-độ) chưa?
2. Entropy regularization (GEM) hay refusal-aware fine-tuning (R-Tuning) có thực sự ngăn mode-collapse khi target là MỘT template rewrite hẹp (không phải nhiều loại refusal đa dạng) — cần tự đo, chưa có nguồn test đúng kịch bản này.
3. Nếu đổi headline đo lường sang AURC/coverage@risk, có cần một tập hiệu chỉnh (calibration set) tách theo app khác với thiết kế held-out-app hiện tại của Tier1/Tier2 (`report/56`) không?
4. Có nguồn 2023-2026 nào đối chiếu TRỰC TIẾP (cùng đơn vị đo, mức app) con số 77% với một số đo lại mới hơn, thay vì chỉ đưa ra một số khác ở mức phần-tử như Fok CHI2022?

---

## Việc tiếp theo — QUYẾT ĐỊNH CẦN USER CHỐT (không tự ý sửa report/54/56)

Kết quả này **CHƯA thay đổi thiết kế đã pre-register** (`report/56`) — chỉ là input để quyết định có nâng cấp không. Ba lựa chọn không loại trừ nhau:

- **(a) Giữ nguyên** thiết kế hiện tại (tỉ-lệ-bịa + %fallback, Tier1/Tier2) — an toàn, đã pre-register, đúng deadline 15/8.
- **(b) Nâng cấp thước đo** sang risk-coverage/AURC (Q3/Q6-a) — tính mới thật, có trụ CAP (ACML25) để trích, nhưng đổi thước đo sau khi đã pre-register `report/56` cần cân nhắc kỹ (ảnh hưởng lịch, có thể cần tính lại MDE).
- **(c) Thêm nhánh DPO** (Q1/Q6-c) — tính mới cao nhất nhưng rủi ro thực thi cao nhất, khó kịp 15/8 nếu làm thêm.

Free, không tốn API/GPU: đọc kỹ CAP (ACML25) + SafeGround để đánh giá chi phí đổi thước đo trước khi quyết.
