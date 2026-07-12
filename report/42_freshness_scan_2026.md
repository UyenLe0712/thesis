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
