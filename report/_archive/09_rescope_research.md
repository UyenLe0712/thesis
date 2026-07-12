# Báo cáo rà soát nền tảng luận văn theo SCOPE MỚI: "Cho sẵn N ảnh → tự sắp xếp" thay cho "1 ảnh → tự đoán màn chưa thấy"

> Sản phẩm của nghiên cứu đa-agent (35 agent, có web-search + kiểm chứng đối kháng từng citation). Mục đích: kiểm tra lại toàn bộ dataset/metric/pipeline (vốn chọn cho scope cũ "1 ảnh tự đoán màn") có còn khớp scope mới "cho sẵn N ảnh xáo trộn → tự sắp xếp → sinh hướng dẫn" hay không, và cần thay/thêm/sửa gì.

## 1. Tóm tắt điều hành

Scope chuyển từ **blind-horizon** (1 ảnh → model đoán mù các màn CHƯA THẤY) sang **screen-order inference** (cho sẵn N ảnh THẬT của 1 luồng, XÁO TRỘN → model tự suy thứ tự rồi sinh hướng dẫn). **Kết luận tổng quát: nền tảng hiện tại VỮNG, KHÔNG phải thay trụ cột nào**; phần lớn lựa chọn còn KHỚP HƠN scope cũ. Lý do: vì mọi màn của nhánh đa ảnh giờ là ảnh THẬT (chỉ bị xáo), grounding (point-in-bbox) và hallucination (HER+coverage) chấm được ĐẦY ĐỦ trên toàn chuỗi — biến mất vùng "unverifiable" của màn tưởng tượng trong scope cũ; và Kendall τ-b — vốn gần như vô nghĩa khi đoán mù — nay trở thành headline đo CHÍNH XÁC năng lực suy luận trật tự.

Điều CẦN đổi chủ yếu là **biên tập caveat di sản scope cũ** + **bổ sung citation/baseline/cơ chế** chứ không phải thay phương pháp. Bốn việc mới SINH RA từ scope mới (đều là cổng hoặc augment): cổng chống leak step-index (KB), cổng tự đếm histogram độ dài episode (KN), baseline đối xứng GOAL-ONLY/VISUAL-ONLY, và confound recall→ordering. **AndroidControl là dataset HƯỞNG LỢI rõ nhất**; Mind2Web giữ future-work nhưng PHẢI đổi lý do (thiếu bbox pixel native + nhánh web, không còn là "thiếu blind-horizon gap").

## 2. Bảng KEEP / CHANGE / ADD theo 5 trụ cột

| Trụ cột | Lựa chọn | Quyết định | Lý do bám scope | Nguồn (trạng thái) |
|---|---|---|---|---|
| **Dataset đơn (DG1)** | MobileViews (màn-0, VH bbox pixel) | **KEEP** | Vai DG1 độc lập trục 1-vs-N → neutral; là bộ UI hiện đại duy nhất có VH bbox-pixel quy mô lớn | arXiv 2409.14337 — **PREPRINT** (chỉ dùng làm hiện vật kỹ thuật) |
| | ScreenSpot / ScreenSpot-v2 | **KEEP** (đối chứng grounding đơn-vị) | Bù credibility cho MobileViews preprint; chỉ đơn-bước, KHÔNG validate DG2 | SeeClick **ACL 2024** + OS-Atlas **ICLR 2025** — PEER-REVIEWED |
| | PixelHelp / AndroidHowTo / Rico-SCA (seq2act) | **ADD** | Vá điểm yếu R11: nguồn câu-hỏi-thủ-tục THẬT để neo phong cách khi tự soạn câu hỏi MobileViews | **ACL 2020** — PEER-REVIEWED |
| | Rico / Screen2Words / Widget Captioning / ScreenQA | **KEEP-OUT** (ghi nhận, không dùng làm trục) | Đều là tóm tắt/Q&A nội dung, không phải hướng dẫn thủ tục | UIST2017 / UIST2021 / EMNLP2020 / NAACL2025 — PEER-REVIEWED |
| | MoTIF | **KEEP-OUT** (future-work) | Là trajectory đa bước, AndroidControl đủ và tốt hơn cho DG2 | ECCV 2022 — PEER-REVIEWED |
| **Dataset đa (DG2)** | AndroidControl | **KEEP** (trục chính) | Khớp NHẤT: gold trajectory → suy nhãn cặp bắt buộc + neo τ-b; single-app low-level hợp signal-attribution | **NeurIPS 2024 D&B** — PEER-REVIEWED |
| | GUI-Odyssey | **ADD** (phụ, robustness N cao) | avg 15.3 step phủ N=8–13 mà AndroidControl thưa | **ICCV 2025** — PEER-REVIEWED |
| | AMEX | **ADD-có-điều-kiện** (đối chứng grounding native) | bbox human-cleaned; nhưng nhỏ (~3k) + không phải trục thứ-tự | Findings **ACL 2025** — PEER-REVIEWED (bỏ claim "tốt hơn SAM2") |
| | AndroidWorld / Mobile-Env / AndroidArena | **KEEP-OUT** | Environment động, không xáo trộn offline được — sai paradigm | AndroidWorld ICLR2025 — PEER-REVIEWED |
| | Mind2Web | **CHANGE lý do** (giữ future-work) | Đổi lý do sang "thiếu bbox pixel native + nhánh web", bỏ lý do cũ "thiếu blind-horizon gap" | NeurIPS 2023 D&B — PEER-REVIEWED |
| **Metric DG1** | Point-in-bbox grounding | **KEEP** | Chuẩn de-facto; phạm vi nở rộng sang mọi màn DG2 | SeeClick **ACL 2024** — PEER-REVIEWED |
| | HER/CHAIR + coverage + matcher kiểu ALOHa | **KEEP** | Metric tồn-tại 1 màn; mạnh hơn ở DG2 (toàn chuỗi verify được) | CHAIR EMNLP2018 / VALOR-EVAL Findings ACL2024 / ALOHa NAACL2024 — PEER-REVIEWED |
| | IFEval (cứng) + G-Eval (mềm, qua Track B) | **KEEP** | Clarity/format ngôn-ngữ-độc-lập → neutral | G-Eval **EMNLP 2023** PEER-REVIEWED; **IFEval = arXiv 2311.07911 PREPRINT** (chỉ công cụ) |
| | CLIPScore | **ADD-thận-trọng / hạ exploratory** | Reference-free thuần ảnh-text; NHƯNG yếu fine-grained → chỉ sanity-check, cần meta-eval trước | CLIPScore EMNLP2021 + FaithScore Findings EMNLP2024 — PEER-REVIEWED |
| | Sửa caveat scope-cũ + siết ánh xạ Chim et al. | **ADD** (biên tập) | Hết mâu thuẫn nội bộ ('unverifiable' chỉ áp DG1 màn-0) | Chim/Ive/Liakata **CL 51(1) 2025** + SelfCheckGPT EMNLP2023 — PEER-REVIEWED |
| **Metric DG2** | Headline Kendall τ-b partial-order-aware | **KEEP** | Trục chính đo đúng năng lực ordering | (xem ADD Lapata bên dưới) |
| | **Lapata 2006** làm backbone τ cho ordering | **ADD** | Lấp đúng chỗ: tiền lệ peer-reviewed dùng τ chấm information ordering (hiện chỉ neo Kendall1938 + Gao) | **CL 32(4) 2006** — PEER-REVIEWED |
| | LCS / LC-substring | **ADD** (phụ) | Bắt "mạch liên tục đúng" mà τ-b/position-acc không bắt; bám Wu et al. | Wu et al. **ACL 2022** — PEER-REVIEWED |
| | Đính chính lineage prior-art | **CHANGE** (câu chữ) | Sort-Story dùng Spearman (KHÔNG τ); Wu mới dùng τ; RankGPT là phương pháp listwise, không phải metric | Sort-Story EMNLP2016 / RankGPT EMNLP2023 — PEER-REVIEWED |
| | Đóng khung partial-order-τ là ADAPTATION | **CHANGE** (framing) | Không trình như metric chuẩn-tên; giữ τ-b-thô làm sàn + audit người ≥90% | Brandenburg 2012 = **NON-NLP math/CS** (chỉ hiện vật khái niệm) |
| | Tier A teacher-forced (Action-Type/Step-SR/Grounding@14%) | **KEEP** | Trục tham chiếu chuẩn ngành (skyline), neutral với scope | AndroidControl NeurIPS2024 + AITW NeurIPS2023 — PEER-REVIEWED; **OS-Atlas = ICLR 2025 PEER-REVIEWED** (sửa nhãn) |
| **Pipeline** | Pairwise+Copeland (chính) + listwise (đối chứng) + MFAS verifier | **KEEP** | Module DUY NHẤT sản sinh nhãn-cặp+cue cho signal-attribution; intransitivity LLM biện minh full matrix | RankGPT **EMNLP 2023** PEER-REVIEWED; motivation intransitivity = arXiv PREPRINT (chỉ động cơ) |
| | Ordering reasoner đọc ẢNH THÔ (không qua parser) | **REVISE** ("clarify + add ablation", không phải "replace") | Tách confound recall→τ-b; nhưng chỉ "giảm 1 nguồn confound", không "khử confound thị giác" | OmniParser arXiv2408.00203 **PREPRINT** + SeeClick ACL2024 |
| | Setwise làm đối chứng RẺ thứ hai | **ADD** | So 3 họ (pairwise/listwise/setwise) ở fair-compute trả lời câu hỏi "phương pháp xếp tốt nhất" | Setwise **SIGIR 2024** — PEER-REVIEWED |
| | Carry-over state + V1 membership per-screen | **REVISE** (chấp nhận cơ chế, sửa framing citation) | Vá lỗi "cite ID đúng-tồn-tại nhưng SAI MÀN"; là kỹ thuật triển khai, KHÔNG có paper riêng bảo chứng | Self-Refine NeurIPS2023 + DOMINO ICML2024 |
| | Lõi chống-hallucination (constrained-gen + V1/V2/V3) | **KEEP** | Per-screen, ngôn-ngữ/thứ-tự-độc-lập, tái dùng hợp lệ ở DG2 | DOMINO **ICML2024** + Self-Refine **NeurIPS2023** PEER-REVIEWED; **Set-of-Mark = arXiv 2310.11441 PREPRINT** (chỉ công cụ) |

## 3. Phân tích từng trụ cột

### 3.1. Dataset đơn (DG1) — verdict tổng: KEEP

- **MobileViews (KEEP, confirm):** vai DG1 không phụ thuộc trục 1-vs-N nên scope mới = neutral. Là PREPRINT (arXiv 2409.14337) → chỉ là hiện vật kỹ thuật (nguồn ảnh+bbox), KHÔNG làm xương sống phương pháp. Khi trích phải ghi rõ phiên bản (v1 9/2024 downstream-tasks vs v3 11/2025 RL-grounding). Đóng khung mọi số "conditioned on recall=X% (K1)" + audit ~20 màn báo tỷ lệ nhãn VH-silver lỗi + verify shard tải về (HF có báo "Data Corruption Issue").
- **ScreenSpot/-v2 (KEEP, confirm):** đối chứng grounding đơn-vị. ScreenSpot gốc = SeeClick **ACL 2024**; -v2 = OS-Atlas **ICLR 2025** — KHÔNG gộp "-v2" vào ACL 2024. Nói rõ ScreenSpot là ĐƠN-BƯỚC, KHÔNG validate DG2.
- **seq2act/PixelHelp (ADD, confirm — verdict mạnh nhất nhóm):** vá điểm yếu R11 (MobileViews thiếu câu hỏi thủ tục). Dùng làm mỏ tham chiếu phong cách khi tự soạn + demo định tính nhỏ, KHÔNG thay mỏ neo grounding. **ACL 2020**, peer-reviewed.
- **Rico/Screen2Words/Widget Captioning/ScreenQA, MoTIF (KEEP-OUT, confirm):** *Sửa nhỏ:* lý do loại MoTIF nên là "là trajectory đa bước, AndroidControl đủ và tốt hơn", KHÔNG nên là "thiếu bbox" (VH Android của MoTIF thực tế có thuộc tính bounds).

### 3.2. Dataset đa (DG2) — verdict tổng: KEEP + AUGMENT

- **AndroidControl (KEEP, confirm):** hưởng lợi RÕ NHẤT từ scope mới. **NeurIPS 2024 D&B**, peer-reviewed. Số đã verify: 15,283 demonstration / 833 app, mean ~5.5 step, p5=1, p95=13. *Caveat trung thực:* Table 1 ghi mean 4.8 nhưng train tính lại ~5.49 (chênh nội bộ paper, không phải bịa); histogram theo từng N KHÔNG công bố → PHẢI tự đếm (cổng KN). Tọa độ là ĐIỂM click (x,y), không phải bbox → harness phải convert. Nhãn "cặp bắt buộc" là quy tắc SUY LUẬN, không phải field có sẵn → pre-register + audit người.
- **GUI-Odyssey (ADD, confirm):** phủ N cao (avg 15.3). **ICCV 2025**, peer-reviewed (điểm mạnh credibility). 3 caveat: tọa độ [0,1000] phải convert; bbox từ **SAM2 segmentation** (suy ra) → grounding hạng hai, KHÔNG ngang VH-silver; cross-app → gating app-switch có thể thổi phồng signal-attribution. *Lưu ý số:* paper 8,334 episode (dùng số này), GitHub README ghi 8,834 — verify khi tải.
- **AMEX (ADD, verdict=REVISE):** chấp nhận làm đối chứng grounding native, NHƯNG **phải bỏ claim "chất lượng cao hơn SAM2"** — paper AMEX không hề so với SAM2/GUI-Odyssey (chỉ so AitW). ~3,046 instruction, ~12.8 step. KHÔNG thay AndroidControl ở trục thứ-tự. Findings **ACL 2025**, peer-reviewed.
- **AndroidWorld/Mobile-Env/AndroidArena (KEEP-OUT, confirm):** environment động, sai paradigm offline-shuffle. *Caveat:* số MoTIF/Mobile-Env và định danh "AndroidArena" chưa verify trực tiếp — làm nhẹ câu chữ khi viết.
- **Mind2Web (CHANGE lý do, confirm):** **PHẢI sửa trong report/02** — đổi lý do future-work từ "không có blind-horizon gap" (lỗi thời) sang "thiếu bbox pixel native (chỉ DOM-derived) + nhánh web". Multimodal-Mind2Web thực ra CÓ bounding_box_rect suy từ DOM chuẩn-hoá [0,1] → diễn đạt "thiếu bbox pixel NATIVE/human-authored" chính xác hơn "thiếu bbox".

### 3.3. Metric DG1 — verdict tổng: KEEP + 1 ADD biên tập + 1 ADD thận trọng

- **Point-in-bbox, HER/coverage, IFEval+G-Eval (KEEP, confirm):** mọi citation xương sống đã verify peer-reviewed (SeeClick ACL2024; CHAIR EMNLP2018; VALOR-EVAL Findings ACL2024; ALOHa NAACL2024; G-Eval EMNLP2023). **IFEval = arXiv 2311.07911 PREPRINT** — đóng khung là "công cụ/giao thức". *Sửa câu chữ:* mô tả matcher là "kiểu ALOHa" (ALOHa thực tế dùng LLM trích object trước, RỒI mới embedding+Hungarian). G-Eval ρ~0.514 là SummEval-specific → coi là trần, BẮT BUỘC qua Track B. Cho DG2: định nghĩa cách tổng hợp coverage qua N màn (per-screen rồi macro-average) + checklist IFEval trung-lập-độ-dài.
- **CLIPScore (ADD, verdict=REVISE → hạ exploratory):** citation thật, nhưng **lý do tự mâu thuẫn**: đề xuất nói CLIPScore bắt lỗi sai-màu/vị-trí/widget — đó CHÍNH LÀ thứ CLIP yếu nhất (fine-grained). Sửa: chỉ làm sanity-check ảnh-text TOÀN CỤC thô, pre-register exploratory, chạy meta-eval với người trên pilot TRƯỚC; yếu trên UI thì BỎ. FaithScore (đã có) mạnh hơn cho lỗ này.
- **Sửa caveat scope-cũ + ánh xạ Chim et al. (ADD biên tập, confirm):** Chim/Ive/Liakata = **CL 51(1):191-233, 2025** (TẠP CHÍ, KHÔNG phải ACL 2025). Phải sửa CAVEAT TOÀN CỤC (01_metrics): "unverifiable/màn tưởng tượng" CHỈ áp MobileViews màn-0 (DG1), KHÔNG áp DG2. Hạ SelfCheckGPT xuống chỉ triangulate màn-0. Khai trung thực mức ánh xạ: Meaning→Grounding+Hallucination (CHẶT); Style→Clarity (hợp lý, KHÔNG 1-1); Divergence (lỏng nhất).

### 3.4. Metric DG2 — verdict tổng: KEEP + AUGMENT

- **Headline τ-b partial-order-aware (KEEP):** trục chính, khớp scope rất cao.
- **Lapata 2006 (ADD, confirm — bổ sung citation quan trọng nhất):** **CL 32(4):471-484, 2006**, peer-reviewed — bài chuẩn-ngành đầu tiên đề xuất τ chấm information ordering + chứng minh tương quan với người. Hiện báo cáo chỉ neo Kendall 1938 (thống kê thuần) + Gao NAACL2025 (về correlation meta-eval, KHÔNG về ordering) → THIẾU biện minh trực tiếp. *Giữ Gao ở vai meta-eval, THÊM Lapata ở vai justify-ordering.* Lapata dùng τ trên TOTAL order → trình là "nền cho dùng τ", partial-order vẫn là adaptation.
- **LCS/LC-substring (ADD, confirm):** Wu et al. **ACL 2022** dùng đúng bộ {τ, LCS, LC-substring, position-Acc, PMR, Distance}. **Caveat:** LCS gốc giả định TOTAL order → phạt cặp tự-do → CHỈ làm phụ (reading sàn/robustness), KHÔNG headline.
- **Đính chính lineage (CHANGE câu chữ, confirm):** Sort-Story (EMNLP2016) dùng **Spearman + pairwise + distance, KHÔNG dùng τ**; Wu (ACL2022) mới dùng τ; RankGPT (EMNLP2023, Outstanding Paper) là **phương pháp listwise**, KHÔNG phải nguồn metric. *Làm chặt thêm:* Wu dùng τ thường (không tie-corrected), luận văn dùng τ-b (hiệu chỉnh tie) → là MỞ RỘNG, củng cố độ mới.
- **Đóng khung partial-order-τ là ADAPTATION (CHANGE framing, confirm):** Brandenburg et al. 2012 là **venue toán/CS NON-NLP** → chỉ hiện vật khái niệm. Bắt buộc giữ: τ-b-thô làm sàn + audit người 50-80 cặp (≥90% mới giữ partial-order làm headline) + độ nhạy nhãn sai 10% (D1).
- **Tier A teacher-forced (KEEP, confirm — 1 sửa nhãn):** AITW (NeurIPS2023) + AndroidControl (NeurIPS2024) peer-reviewed; định nghĩa 14% đã verify. **SỬA NHÃN QUAN TRỌNG: OS-Atlas KHÔNG còn là preprint — đã ICLR 2025 (Spotlight) → PEER-REVIEWED.** Phải cập nhật trong report. Step-SR/Grounding@14% đo TỪNG BƯỚC độc lập → KHÔNG phải "điểm ordering", tách bảng khỏi τ-b.

### 3.5. Pipeline — verdict tổng: KEEP hệ chính + AUGMENT 4 điểm

- **Pairwise+Copeland + listwise + MFAS (KEEP, confirm):** RankGPT **EMNLP2023** peer-reviewed làm xương sống. *Trung thực nguồn:* motivation intransitivity chỉ dùng arXiv PREPRINT → chỉ làm động cơ. *Tăng cường:* nên thêm "Investigating Non-Transitivity in LLM-as-a-Judge" (**ICML 2025 poster**, peer-reviewed). Pre-register rõ: chọn pairwise vì sản sinh cue cho signal-attribution, KHÔNG vì τ-b cao hơn. Tie-break Copeland phải theo chỉ-số POST-shuffle (tránh leak gold).
- **Ordering reasoner đọc ảnh thô (REVISE — hạ "replace" xuống "clarify + add ablation"):** confound recall→ordering là THẬT. Báo 03 đã ngầm mô tả S0b hỏi VLM trực tiếp cặp ảnh; chỉ cần LÀM RÕ S0b đọc ảnh thô (parser S0a tùy chọn) + pre-register ablation "có/không parser-feature" gắn K1. *Sửa over-claim:* đọc ảnh thô chỉ "giảm 1 nguồn confound", KHÔNG "khử confound thị giác". K1 phải đo recall trên CẢ AndroidControl, không chỉ MobileViews.
- **Setwise (ADD, confirm):** **SIGIR 2024**, peer-reviewed — đối chứng RẺ thứ ba trên trục chi phí. *Caveat:* biến thể logit-based cần model mở (Qwen2.5-VL); API đóng dùng biến thể generation. Gốc text-IR → port sang ảnh-UI là adaptation. KHÔNG thay pairwise làm chính.
- **Carry-over state + V1 per-screen (REVISE — chấp nhận cơ chế, sửa framing citation):** lỗ hổng THẬT — pipeline hiện chạy lõi per-screen, V1 dùng một tập E chung → không bắt lỗi "cite ID đúng-tồn-tại nhưng SAI MÀN". **Sửa:** carry-over + per-screen E là KỸ THUẬT TRIỂN KHAI, KHÔNG có paper riêng bảo chứng. Carry-over chỉ đưa text bước model tự sinh, KHÔNG đưa VH/gold (giữ no-leak R7). Pre-register E_k per-screen + đo riêng tỷ lệ "wrong-screen hallucination".
- **Lõi chống-hallucination (KEEP, confirm):** DOMINO **ICML2024** + Self-Refine **NeurIPS2023** peer-reviewed. **Set-of-Mark (arXiv 2310.11441) + OmniParser (arXiv 2408.00203) là PREPRINT** → chỉ công cụ. Clutter SoM trên UI mobile dày + trần recall vẫn là rủi ro tồn vong (K1).

## 4. Tác động tới 2 nhánh & trọng số

- Cả DG1 và DG2 đều BẮT BUỘC, trọng số gần ngang (đa có thể nhẹ hơn chút nếu quá khó). Scope mới làm **DG2 mạnh hơn hẳn** thiết kế đoán-mù cũ.
- **DG1 gần như không đổi** (neutral toàn diện): MobileViews + bộ metric đơn-ảnh giữ nguyên, chỉ thêm seq2act làm mỏ phong cách câu hỏi + sửa vài caveat biên tập.
- **Lý do để đa NHẸ hơn chút:** chi phí pairwise C(N,2) + cổng KN có thể làm số episode mốc N cao (~8-10) mỏng → trần headline N≤8; recall nhân theo N màn; thêm baseline đối xứng tốn compute. Đề nghị: headline DG2 = τ-b trên N∈[3,8], báo thêm tới ~10 nếu ngân sách cho phép; DG1 giữ đầy đủ.

## 5. Rủi ro & khả thi

- **Recall OmniParser (rủi ro tồn vong số 1, cổng K1):** ~57% trên ScreenSpot là *grounding accuracy* — chỉ số KHÁC recall. Scope mới NHÂN rủi ro: (a) lõi 5 bước chạy mỗi màn → grounding-quality DG2 nhân trần recall theo N; (b) **confound MỚI**: nếu ordering dựa feature đã-parse và parser miss element mang tín hiệu thứ tự → τ-b giảm không do model kém. Giảm nhẹ: ordering đọc ảnh thô + K1 đo recall trên CẢ AndroidControl. Mọi số đóng khung "conditioned on recall=X%".
- **Chi phí C(N,2) (ngân sách $100-300):** N≤8 → 28 call/episode (pairwise). Tổng thực = pairwise + listwise fair-compute + Setwise + GOAL-ONLY + VISUAL-ONLY + RANDOM, có thể vượt. **Cần bảng chi phí Stage-0 TÁCH theo baseline.** MFAS verifier là code thuần (0 call). Trần N≤8 + ≥30 episode/mốc là giả định kiểm soát ngân sách.
- **Cổng KB (chống leak step-index):** chỉ phát sinh từ scope mới. Bắt buộc strip metadata + tái mã hóa + UUID + che status bar/đồng hồ/pin/badge-OS + loại episode 2-ảnh trùng-pixel; CI test detector mù.
- **Cổng KN (histogram độ dài episode):** tiền-điều-kiện CỨNG cho τ-b — phải tự đếm để biết có đủ ≥30 episode mỗi mốc N≥3. Pre-register + Holm-Bonferroni (hoặc hạ giả thuyết phụ xuống exploratory).
- **Khả thi tổng:** 1 GPU 24GB + off-the-shelf đủ; Qwen2.5-VL-7B chính (free local, lấy được logit cho Setwise), tùy chọn slice GPT-4o API. Không fine-tune lớn.

## 6. Câu hỏi/đề xuất CẦN CHỐT với thầy

1. **Trần N cho đường cong headline:** chốt N≤8 (báo thêm tới ~10 nếu ngân sách cho phép) — hay ép tới N=13 (p95) bất chấp chi phí pairwise tăng mạnh (78 call/episode)?
2. **Trọng số DG1 vs DG2:** xác nhận "gần ngang, đa nhẹ hơn chút khi khó" — hay thầy muốn một tỷ lệ cụ thể?
3. **Bộ dataset phụ DG2:** có chấp nhận THÊM GUI-Odyssey (ICCV2025) và/hoặc AMEX (ACL2025 Findings) làm robustness — hay giữ AndroidControl đơn độc cho gọn scope?
4. **CLIPScore:** giữ làm metric phụ exploratory (sau meta-eval pilot) hay bỏ hẳn?
5. **partial-order-aware τ-b:** chấp nhận đóng khung là ADAPTATION (có τ-b-thô làm sàn + audit người ≥90%) — hay dùng τ-b-thô (total-order chuẩn) làm headline cho an toàn citation?
6. **Tier A — claim:** xác nhận KHÔNG claim ngang leaderboard, chỉ là trục tham chiếu chuẩn ngành.
7. **Tiếng Việt:** xác nhận định lượng chạy EN/ZH, tiếng Việt chỉ demo định tính + sanity-check OCR.
8. **Các sửa biên tập bắt buộc trong report** (xin thầy duyệt nguyên tắc): (a) đổi lý do future-work Mind2Web; (b) sửa nhãn OS-Atlas từ preprint → ICLR 2025 peer-reviewed; (c) sửa CAVEAT TOÀN CỤC 01_metrics ("unverifiable" chỉ áp DG1); (d) đính chính lineage Sort-Story (Spearman ≠ τ).

---

*Ghi chú độ tin cậy nguồn (trung thực tuyệt đối):* Xương sống PHƯƠNG PHÁP đều peer-reviewed (SeeClick ACL2024, CHAIR EMNLP2018, VALOR-EVAL/ALOHa, G-Eval EMNLP2023, Lapata CL2006, Wu ACL2022, Kendall, AndroidControl NeurIPS2024, AITW NeurIPS2023, OS-Atlas ICLR2025, RankGPT EMNLP2023, Setwise SIGIR2024, DOMINO ICML2024, Self-Refine NeurIPS2023, Chim/Ive/Liakata CL2025). PREPRINT chỉ làm công cụ/động cơ, KHÔNG trình như đã bình duyệt: MobileViews (2409.14337), OmniParser (2408.00203), Set-of-Mark (2310.11441), IFEval (2311.07911), các bài intransitivity motivation. NON-NLP: Brandenburg 2012 (hiện vật khái niệm). Không có citation bịa trong toàn bộ dữ liệu đã verify.
