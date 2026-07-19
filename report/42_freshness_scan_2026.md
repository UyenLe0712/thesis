# 🔭 Quét độ-mới 2025–2026: "pipeline/metric có lỗi thời không?" — verify 2026-07-03

> Deep-research 6 góc (`wf_3d7cdc91`, 7 agent, 0 lỗi) trả lời nỗi lo "giờ 2026 rồi".
> **PHÁN QUYẾT: KHÔNG lỗi thời, KHÔNG bị scoop.** Chỉ cần (a) thêm ~8 cite định vị vào related-work + (b) chạy thêm ≥1 generator đời mới. **Không đụng thiết kế lõi.**

## 1. Scoop-check — KHÔNG có ai làm gần trùng
Không tồn tại combo lõi của ta = *sinh hướng dẫn cho NGƯỜI ĐỌC từ ảnh+câu hỏi* + *lớp trung-thực-hoá đối chiếu VH* + *đánh giá no-gold không tự-chấm*. Ba bài "gần" + cách phân biệt:
- **AskEase (CHI 2026, 2601.18092)** — sinh hướng dẫn cho screen-reader user. *Khác:* live-context/accessibility, không screenshot+câu-hỏi→tutorial, không lớp VH, eval human-study.
- **LLM as a Meta-Judge (2603.09403, 2026)** — suy-giảm-ngữ-nghĩa validate metric không nhãn người → trùng *ý tưởng* perturbation của nhánh B. *Khác:* miền MT/QA/summ, không GUI; ta bơm lỗi ĐỘC LẬP matcher + trụ peer-reviewed (Sai EMNLP21).
- **Instruction Agent / TongUI** — tutorial cho AGENT thực thi / làm dữ liệu huấn luyện. *Khác trục:* ta sinh cho người + no-gold.

## 2. PHẢI CITE (related-work 2026 — đã verified)
| Bài | Venue | Vì sao phải cite | Ta khác chỗ nào |
|---|---|---|---|
| **FaithScore** | Findings EMNLP 2024 | metric faithfulness reference-free cho LVLM | ta verify với **VH có cấu trúc**, không để VLM tự-chấm-với-ảnh |
| **ALOHa** | NAACL 2024 | trụ matcher (đã có) | — |
| **Reliability without Validity** | preprint 2606.19544 (2026) | hậu thuẫn lấy **Cohen's κ làm headline**, chống exact-match phóng đại | ta đã báo κ |
| **LLM as a Meta-Judge** | preprint 2603.09403 (2026) | gần ý tưởng nhánh B → phải phân định | miền GUI + bơm-lỗi-độc-lập-matcher + trụ peer-reviewed |
| **Reference-free Eval Survey** | preprint 2501.12011 (2025) | định vị đóng góp B | — |
| **VECTOR / What Happens When** | preprint 2512.08979 (12/2025) | "GPT-4o giữ nguyên dự đoán khi đảo thứ tự" → luận cứ MẠNH cho DG2 + anti-leakage | ta ở miền GUI + gắn ordering→sinh hướng dẫn |
| **UI-TARS** | preprint 2501.12326 (2025) | phân biệt setup GUI-agent | ta sinh hướng dẫn cho NGƯỜI, không bấm máy |
| **GUI-Odyssey** · **AMEX** · **ScreenSpot-Pro** | ICCV25 · preprint · ACM MM25 | acknowledge landscape dataset → chặn "sao không dùng" | agent-control/element-detection, vai khác task ta |

*(No Free Labels 2503.05061 đã có trong related-work.)*

## 3. Khuyến nghị hành động
- **✅ Chỉ SỬA FILE (rẻ):** thêm 1 đoạn related-work nêu 8 cite trên + differentiator. Thêm 1 đoạn "related datasets" nêu lý-do-không-dùng GUI-Odyssey/AMEX/ScreenSpot-Pro.
- **✱ NÊN LÀM khi chạy số (tốn API — HỎI USER):** giữ gpt-4o-mini làm mốc rẻ, **THÊM ≥1 generator đời mới** để bảng số không kẹt ở model cũ. Máy không-GPU → ưu tiên API: **GPT-4.1** (nâng cấp 1 dòng) hoặc **Gemini-2.5-Flash** (khác-họ, rẻ); muốn trục đóng-vs-mở thì **Qwen3-VL** qua DashScope. ⚠️ generator=GPT thì LLM-judge phải khác họ (Gemini/Qwen).
- **Future-work (không gấp):** bộ trỏ **GUI-Actor/UI-TARS** làm điểm-dự-đoán độc lập cho grounding (né tautology tâm-bbox) thay ScreenSpot thuần.

## 4. GIỮ NGUYÊN — phần vững 2026 (trấn an hội đồng)
- **Niche chống-circularity của nhánh A ĐỘC NHẤT:** mọi metric hallucination-VLM mới verify với ẢNH hoặc nội-tại-model; KHÔNG cái nào đối chiếu **inventory phần tử UI có cấu trúc (VH)** như ta.
- **Perturbation-validate là trục ĐÚNG, đang SỐNG** (Meta-Judge, Sage, Contextual-Meta-Eval 2025-2026 cùng hướng) → ta không tự chế; trụ Sai EMNLP21 vẫn hợp lệ.
- **Bỏ human-correlation làm cổng đậu/rớt** được hậu thuẫn thêm (Sage 2512.16041: nhãn người tự bất-nhất).
- **DG2 order-shuffle là dòng ACTIVE 2025-2026** (VECTOR, ClinicalSkillQA) và ta là **bản GUI đầu tiên** gắn ordering→sinh hướng dẫn + partial-order từ gold.
- **Model-agnostic** → đổi generator 1 dòng code. **Bộ ba dataset** không bị bộ nào SUPERSEDES.

## 5. CẦN KIỂM VENUE TRƯỚC KHI TRÍCH (chưa verify — chỉ bổ trợ)
- Image Captioning Eval in Age of MLLMs (2503.14604) · ClinicalSkillQA 2026 (2606.02082) · Contextual Metric Meta-Eval (2503.19828) · Meta-Analysis NLG 2020-2025 (2601.07648) · GUI-Xplore (2503.17709) · MUIAnno (2605.17656). Không đưa vào xương sống cho tới khi verify.

---

## 6. ⭐ DEBATE GIÁM-KHẢO 2026 — "pipeline+metric có phù hợp 2026 không?" (`wf_73dfaaf9`, 25 đòn/13 sống)

### PHÁN QUYẾT: **PHÙ-HỢP-CẦN-ĐIỀU-CHỈNH.**
Khung KHÔNG lỗi thời, KHÔNG bị scoop — nhưng **bằng chứng đang neo vào 1 model đời-2024 + thiếu 2 baseline hợp-thời** → thiếu 3 vá thì bảo vệ sẽ bị bắt *"đề tài 2023 / chữa bệnh sắp tự khỏi"*.

### PHẢI NÂNG (major — điều kiện đậu 2026)
- **M1 — Đường-cong-bịa theo bậc-model (4/13 đòn hội tụ — NGUY HIỂM NHẤT).** Thêm ≥1 model **frontier 2025-26 RẺ** (Gemini-2.5-Flash / GPT-4.1-mini) chạy CHUNG mẻ 81-màn; báo tỉ-lệ-bịa + %fallback **PER-MODEL như đường cong**, KHÔNG headline tĩnh "¼". `env VLM_MODEL` đã sẵn → **không sửa code**. *Vì: "bịa tên nút" có thể là bệnh model-2024-yếu; phải cho thấy frontier VẪN bịa >0, nếu không lớp trung-thực-hoá bị coi là "chữa bệnh sắp tự khỏi" → đóng góp A bốc hơi.*
- **M2 — Baseline listwise một-shot.** Chạy 1 baseline all-N-ảnh-một-prompt (kiểu RankGPT) bằng chính VLM, chấm CÙNG τ-Fagin + Step-SR + **CỘT CHI PHÍ** (1 call vs O(N²)). Reframe pairwise KHÔNG phải "thuật-toán-sắp bắt buộc" mà là **substrate-audit** (quyết-định-từng-cặp cho stratification 1-cue + intransitivity audit-trail + partial-order-from-gold — thứ listwise hộp-đen không cấp). *Vì: VLM frontier nuốt N ảnh 1 context → không có baseline holistic thì Copeland/min-FAS trông thừa. Phản-công: VECTOR (2512.08979 "VLM mù thời gian") → long-context YẾU ở suy-luận-thứ-tự → pairwise là mitigation có nguyên tắc.*
- **M3 — Reframe trọng-lượng A sang "bền-với-frontier + niche on-device".** Bỏ "model-agnostic" tuyệt đối → **"hậu-kiểm model-agnostic BY CONSTRUCTION, kiểm chứng trên 3 đời model"**. Đẩy frame chính: lớp kiểm-tra-độc-lập là **NHU CẦU TRIỂN KHAI on-device** (a11y-tree LIVE nhưng model nhỏ/yếu không gọi được frontier) → nối làn sóng trợ-năng 2026 (AskEase CHI26). Neo "A ngang B" vào **DG2/Step-SR (thuật toán, bền) + đối-chứng-thất-bại correction→silent-error (đo được, độc-lập-model)**, KHÔNG neo vào ĐỘ LỚN con số bịa.

### NÊN NÂNG (minor)
- **m1** Related-work nhánh B: đặt cạnh Meta-Judge/Sage/Reliability-without-Validity/VECTOR, khai concurrent-2026 miền text, DELTA = perturbation bơm lỗi **có-cấu-trúc-UI** (đảo cặp-bắt-buộc từ gold, nút-không-tồn-tại) + inventory VH. Giữ Sai EMNLP21 làm TRỤ.
- **m2** K-pair thành **cổng cứng thứ-5** (đã ghi CLAUDE §5): pre-register sàn acc-pairwise, trích VECTOR; dưới sàn → "Stage-0 không kết luận cho model đó".
- **m3** Perturbation **graded-monotonicity**: nâng harness 4-loại-lỗi → 3-4 MỨC severity, báo Spearman(severity, 1−faithfulness)+CI. KHÔNG bê convergent-LLM-judge vào cổng đậu/rớt (family-bias, Panickssery).
- **m4** Bảng định-vị 3-cột (AskEase/FaithScore/Meta-Judge × nguồn-verify/miền/đầu-ra) + 1 ca phân-biệt-được (FaithScore false-pass khi VLM "thấy" nút trên ảnh mờ, inventory-check bắt được).

### VỮNG RỒI (không đụng — trấn an)
Không bị scoop · verify bằng **inventory-cấu-trúc audit-được** (khe phòng-thủ vs cả họ metric 2024-26) · partial-order-từ-gold cho GUI đa-màn (chưa ai làm ở lớp validate no-gold) · anti-circularity 3-cơ-chế đúng chuẩn 2026 · chống-leakage + 4 cổng + cluster-bootstrap + Holm đạt chuẩn · không claim leaderboard (đúng, tránh đối đầu sai-setup UI-TARS/GUI-Actor).

### 🎯 ĐÒN 2026 NGUY HIỂM NHẤT + THỦ SẴN
> **Đòn:** *"Anh đo bịa ¼ trên gpt-4o-mini đời 2024 — frontier 2025-26 đọc ảnh chuẩn hơn, bịa tụt gần 0, vậy lớp trung-thực-hoá đang chữa bệnh sắp tự khỏi."*
> **Thủ:** *"Chúng tôi báo bịa như ĐƯỜNG-CONG theo bậc-model gồm 1 frontier 2025-26 — bịa VẪN >0 ở model mạnh nhất (khớp FaithScore/POPE: hallucination-tham-chiếu chưa hết ở VLM frontier); và on-device có a11y-tree-live nhưng chạy model-nhỏ-không-gọi-được-frontier → lớp kiểm-tra-độc-lập là nhu-cầu-triển-khai BẤT BIẾN; trọng-lượng đóng góp neo vào DG2/Step-SR, không vào độ-lớn con số bịa."*

---

## 7. ✅ DEEP-RESEARCH CHỐT LẦN CUỐI 2026 (`wf_9c395ab3-f59`, 5 góc quét web 2024-2026 + 1 tổng hợp)

### PHÁN QUYẾT MỘT DÒNG: **ĐỦ VỮNG ĐỂ NỘP 2026 — KHÔNG có lỗi thiết kế.**
Rủi ro reject cao nhất KHÔNG ở pipeline/metric sai, mà ở (a) **novelty bị AskEase CHI2026 áp sát trục sinh-hướng-dẫn-cho-người**, (b) **cách đóng khung validation**. Cả hai thủ được bằng cách VIẾT, không phải làm lại thiết kế. Điều kiện đậu: (a) tự đo đường-cong tỉ-lệ-bịa per-model trên ≥1 frontier rẻ (không mượn số ngoài); (b) thêm 3 citation peer-reviewed + phân định AskEase & FaithScore; (c) đóng khung construct-validity + bổ sung 2 test perturbation (benign-robustness + error-type-discrimination).

### 7 LÝ-DO-CÓ-THỂ-REJECT (cao→thấp) + phản-thủ — ĐÃ ÁP VÀO `report/43`
- **R1 (CAO) AskEase CHI2026** cũng sinh hướng dẫn từng bước cho người (screen-reader) → phân định 3 điểm: ảnh-tĩnh+câu-hỏi vs live · no-gold neo VH vs user-study task-success · CÓ lớp trung-thực-hoá + sắp-màn vs KHÔNG. Dùng AskEase hậu thuẫn niche on-device. *(→ file 43 §9)*
- **R2 (CAO) FaithScore** (reference-free, cùng miền) VẪN báo human-correlation → viết đoạn phân định TRƯỚC khi giám khảo nêu: ta verify VH cấu trúc + matcher tất định (≠ self-check VLM); hạ human-correlation xuống future-work có chủ đích dưới khung measurement-theory. *(→ file 43 §7.2 + §9)*
- **R3 (TB-cao) "frontier hết bịa → lớp trung-thực-hoá thừa"** → bằng chứng preprint: ScreenSpot-Pro mọi model <90% (GPT-4o 0.8%, Qwen2.5-VL-72B 43.6%), Ferret-UI Lite 3B ~53%, object-hallucination truyền chéo 66.5%. BẮT BUỘC tự đo đường-cong-bịa; tách trục grounding-coords khỏi faithfulness-văn-bản. *(→ file 43 §9 + §5.3 + §10.3)*
- **R4 (TB) "chỉ áp method có sẵn"** cho pairwise→Copeland→min-FAS → có bài 2025-26 cùng lõi (2412.16181 preprint, EZ-Sort CIKM25, Dodgersort PAKDD26) → PHẢI cite; độ mới = 5 điểm ghép (miền GUI + điều-kiện-mục-tiêu + gắn-sinh-hướng-dẫn + partial-order-from-gold + 5-cue). *(→ file 43 §4.4)*
- **R5 (TB) tolerance 14% lỗi thời** → chuẩn 2025 = point-in-GT-bbox bbox-native (ScreenSpot-Pro/UI-TARS); hạ 14% xuống biến-thể-đối-chứng. M1 (rút khỏi headline) đúng hướng. *(→ file 43 §5.3)*
- **R6 (TB) perturbation-only chưa đủ bar 2025** → cần 4 tiêu chí (nhạy + đơn-điệu + benign-robustness + error-type-discrimination); đang có 3/4 → bổ sung 2 test. Trụ: BUMP ACL2023 + Sai EMNLP2021. *(→ file 43 §7.2)*
- **R7 (thấp) thống kê G≈17** → không có phương án sạch; nâng trụ Cameron-2008 → MacKinnon-Nielsen-Webb (J.Econometrics 2023) + jackknife CV3; khai caveat under-coverage; số = exploratory. *(→ file 43 §7.4)*

### CITATION PEER-REVIEWED MỚI (đã thêm vào file 43 Phụ lục C)
AskEase (CHI 2026) · BUMP (ACL 2023) · EZ-Sort (CIKM 2025) · Dodgersort (PAKDD 2026) · "Neither Valid nor Reliable?" + "Construct Validity in LLM Benchmarks" (NeurIPS 2025) · MacKinnon-Nielsen-Webb (J.Econometrics 2023).
⚠ Đối chiếu PDF/venue TRƯỚC KHI IN: DOI AskEase 10.1145/3772318.3790661; venue EZ-Sort/Dodgersort/2 bài NeurIPS2025 trên OpenReview.
Preprint (HalluClear, Ferret-UI Lite, ScreenSpot-Pro, UI-TARS, 2412.16181, LLM-as-Meta-Judge) = CHỈ định-vị-landscape, KHÔNG làm trụ đậu/rớt.

### SO VỚI §6 (report/42 cũ): KHÔNG mâu thuẫn — chỉ SIẾT CHẶT.
Xác nhận mạnh M1/M2/M3. Bổ sung mới: chuẩn grounding bbox-native (R5), khung construct-validity + 2 test perturbation (R6), scoop-thành-phần khối sắp-màn (R4), trụ thống kê MNW2023 (R7), 2 citation then-chốt AskEase+BUMP.

---

## 8. ✅ RESEARCH RIÊNG KIẾN TRÚC PIPELINE (`wf_1306a703-213`, 5 góc web + 1 tổng hợp) — 2026-07-05

### PHÁN QUYẾT: **Pipeline ĐÚNG nhu cầu 2026 — KHÔNG cần đổi kiến trúc, chỉ đóng-khung + 2 nhánh so-sánh.**
Cả hai khối ("sinh mù → hậu-kiểm đối chiếu VH → fallback mô-tả" và "pairwise→Copeland→min-FAS") nằm ĐÚNG dòng chính danh 2024–2026 (post-hoc verification đối-chiếu-nguồn-ngoài + ordering-tường-minh). Rủi ro còn lại = THUẦN FRAMING.

### ĐÒN NGUY HIỂM NHẤT (kiến trúc): "Sao không grounded-gen như AskEase CHI2026?"
Thuốc-giải 4 lớp (đã ÁP vào `report/43` §4.5):
1. Sinh mù = thiết bị ĐO, không phải kiến-trúc-deploy; deploy có thể grounded.
2. Grounded-gen làm HỎNG phép đo: thêm ngữ cảnh → ảo giác còn ~2% (Frontiers in AI 2025, PR) → model chép, hết đo được.
3. Grounded-gen không sạch: cây a11y thiếu nhãn (>77%, Chen ICSE20) → vẫn bịa.
4. Post-hoc verify chính danh: FaithScore EMNLP24, CoVe ACL24, RARR ACL23; tín hiệu NGOÀI phi-LLM tất định → KHÁC self-check nội tại bị Huang ICLR24 bác.

### 7 RỦI-RO-PIPELINE (đa số CHỈ đóng-khung, đã áp vào file 43):
- R1 grounded-gen (AskEase CHI26, PR) → §4.5 measurement-vs-deploy.
- R2 field rời a11y sang visual-grounding (ShowUI CVPR25) → phân định: trục agent-bấm-toạ-độ khác; VH chỉ dùng lúc chấm.
- R3 pairwise "bag-of-frames" acc~0.5 (TOMATO ICLR25) → **PHẢI-LÀM cổng K-pair** (rủi ro thực-nghiệm thật duy nhất).
- R4 pairwise O(N²) (Qin PRP NAACL24) → **PHẢI-THÊM baseline listwise + cột chi phí** (M2).
- R5 fallback mô-tả "vô dụng" → ranh giới agent-vs-người + đo chất lượng fallback = appropriate abstention.
- R6 khối không mới → độ mới ở TỔ-HỢP (§4.4).
- R7 gộp vào self-correct-bị-bác (Huang ICLR24) → tín hiệu NGOÀI phi-LLM.

### TRỤ PEER-REVIEWED bênh pipeline: FaithScore (EMNLP24) · CoVe (ACL24) · RARR (ACL23) · Huang (ICLR24) · TACL survey (2024) · Frontiers-AI (2025) · TOMATO (ICLR25) · Qin-PRP (NAACL24) · ShowUI (CVPR25) · AskEase (CHI26) · "Do GUI Grounders…" (EACL26).

### 3 VIỆC PHẢI LÀM (không đụng kiến trúc): (1) framing §4.5; (2) cổng K-pair; (3) baseline listwise. KHÔNG cần: đổi kiến trúc / grounded-gen vào lõi / self-refine / bỏ a11y-tree.

### ĐÃ GOM TẤT CẢ VÀO `report/43` — file 43 giờ TỰ-ĐỦ (thêm §4.5, Chương 11 lộ trình/môi trường/trạng thái, Chương 12 tổng hợp phòng thủ 3 vòng research, Q&A + citation mở rộng). User chỉ đọc file 43.
