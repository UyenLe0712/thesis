# 📚 DEEP-RESEARCH: Validate metric/judge với MỨC GÁN-TAY TỐI THIỂU (lưu kết quả 2026-06-30)

> **File này lưu kết quả deep-research** (workflow `/deep-research`) chạy 2026-06-30 cho câu hỏi:
> *"Cách validate hiệu quả các bộ chấm faithfulness/hallucination tự động (embedding matcher + reference-grounded LLM-judge) cho luận văn đánh giá tutorial UI, với mức gán-tay tối thiểu."*
>
> **✅ TRẠNG THÁI: ĐÃ HOÀN TẤT (2026-07-01).** 6 claim U1–U6 (trước bỏ dở) đã re-verify xong bằng workflow
> `wf_7a51cf9f` (fetch nguồn + chấm đối kháng) → **kết quả + protocol chốt ở §6 CUỐI FILE.** Tổng 31 claim đã xử lý.
> - Kết quả re-verify: **5 SUPPORTED + 1 PARTIAL (U6)**, KHÔNG claim nào bị bác. NHƯNG **cả 6 nguồn là preprint arXiv
>   chưa bình duyệt** → chỉ dùng làm **luận cứ bổ trợ / động cơ thiết kế**, mỗi nguyên tắc trụ phải có ≥1 nguồn peer-reviewed.
> - (Lịch sử: Scope 5 góc → Search 5 agent/21 nguồn → Fetch 15 nguồn/99 claim → Verify 25 claim [15 đậu, 4 bác] + 6 claim này.)
>
> **Thông tin RESUME workflow (nếu muốn chạy tiếp bằng máy):**
> - `runId`: `wf_4f756710-46b`
> - `scriptPath`: `C:\Users\Admin\.claude\projects\D--Master-Thesis-report\71f5bc27-6c0f-4882-ac44-429e1153ac94\workflows\scripts\deep-research-wf_4f756710-46b.js`
> - Lệnh: `Workflow({scriptPath, resumeFromRunId: "wf_4f756710-46b"})` → các agent đã xong trả cache tức thì, chỉ chạy lại phần lỗi.
> - Output gốc đầy đủ: `…\Temp\claude\…\tasks\wso08hn22.output` (2498 dòng; dòng 1-334 là kết quả, còn lại là metadata).

---

## §1. CLAIM ĐÃ XÁC NHẬN (15 — verify 3-vote, ✓ = ≥2/3 không-bác)

### Nhóm A — Cắt công gán-tay (minimal annotation / HITLC / active learning)

| # | Claim | Nguồn | Vote |
|---|---|---|---|
| A1 ⭐ | **Hybrid model-based: chỉ cho người chấm các mẫu mà metric tự-động "bất định cao" → giảm thêm 89% số nhãn người.** Đây CHÍNH là HITLC "adjudicate-uncertain-only" ta định dùng. | [Active Evaluation, ACL 2022](https://aclanthology.org/2022.acl-long.600/) — quote *"reduces the number of human annotations required further by 89%"* | 3-0 |
| A2 | **Dueling-bandit chọn cặp để so → giảm 80% số nhãn người** để tìm hệ top so với so-cặp vét cạn. | [ACL 2022](https://aclanthology.org/2022.acl-long.600/) — *"the number of human annotations can be reduced by 80%"* | 3-0 |
| A3 | **Tự dựng benchmark meta-eval từ dataset đã-có-nhãn-người, KHÔNG cần nhãn mới** (tránh chi phí + contamination) → ủng hộ việc mượn gold sẵn. | [ACL 2025](https://aclanthology.org/2025.acl-long.1327/) — *"…automatically constructed based on any existing NLG evaluation benchmark…avoids the cost of additional human annotations and potential data contamination."* | 2-1 |
| A4 | **Protocol gán-nhãn fine-grained (Atomic Content Units) → đạt inter-annotator agreement cao** = đường "thiết kế protocol" để giảm nhiễu/chi-phí mà giữ hợp lệ. | [RoSE, arXiv 2212.07981](https://arxiv.org/pdf/2212.07981) — *"…Atomic Content Units (ACUs)…allows for a high inter-annotator agreement."* | 3-0 |

### Nhóm B — Cỡ mẫu tối thiểu & cảnh báo thống kê

| # | Claim | Nguồn | Vote |
|---|---|---|---|
| B1 ⚠️ | **Meta-eval ổn-định cần benchmark NGƯỜI lớn — RoSE = 22,000 nhãn / 28 hệ / 3 dataset.** Tức validation thống-kê-vững dựa trên nhãn-người quy-mô-lớn, không phải mẫu nhỏ. | [RoSE, 2212.07981](https://arxiv.org/pdf/2212.07981) | 2-1 |
| B2 ⚠️ | **Benchmark meta-eval hiện có bất-định-thống-kê cao (CI rộng)** → benchmark nhỏ KHÔNG phân biệt tin cậy chất-lượng-metric. Cảnh báo trực tiếp về cỡ mẫu tối thiểu. | [arXiv 2409.19507](https://arxiv.org/pdf/2409.19507) — *"high uncertainty (large confidence intervals)…"* | 3-0 |

### Nhóm C — Bẫy về tương quan / tính hợp lệ của metric

| # | Claim | Nguồn | Vote |
|---|---|---|---|
| C1 ⭐ | **Tương quan cao với người KHÔNG đủ để kết luận metric hợp lệ** — có metric tương-quan-tốt nhưng vẫn vô-dụng ở chiều cần đo (vd faithfulness). | [arXiv 2409.19507](https://arxiv.org/pdf/2409.19507) — *"some evaluation metrics…are, in fact, ineffective in measuring the considered dimension despite correlating well."* | 3-0 |
| C2 | **Granularity tương quan (system-level vs instance/sentence-level) làm ĐẢO kết luận** → bản thân thiết kế validation là một confound. (Tác giả thật: Anastasia Shimorina, KHÔNG phải Novikova.) | [arXiv 1805.11474](https://arxiv.org/pdf/1805.11474) | 3-0 |
| C3 | **Ngay ở instance-level, tương quan auto-vs-người TỐT NHẤT chỉ vừa phải** (ρ=0.73 METEOR; còn lại ρ=0.43–0.59) → không được giả định matcher hợp-lệ per-item khi chưa đo. | [arXiv 1805.11474](https://arxiv.org/pdf/1805.11474) | 3-0 |
| C4 | **Hệ tinh-chỉnh-bằng-người (vd GPT-3.5) overfit "human eval không-ràng-buộc" phản ánh prior input-agnostic của annotator** → nên dùng eval **targeted, reference-grounded** thay vì phán-đoán-tự-do. | [RoSE, 2212.07981](https://arxiv.org/pdf/2212.07981) | 3-0 |

### Nhóm D — Circularity / self-preference / cùng-họ

| # | Claim | Nguồn | Vote |
|---|---|---|---|
| D1 ⭐ | **Bias do perplexity/familiarity, KHÔNG phải do tự-viết:** LLM cho điểm cao văn-bản perplexity-thấp (quen) hơn người, KỂ CẢ khi văn-bản KHÔNG do nó sinh → "khác họ" là CẦN nhưng **vẫn phải validate với người**; judge cùng phân-bố-huấn-luyện vẫn lệch. | [arXiv 2410.21819](https://arxiv.org/pdf/2410.21819) | 3-0 |
| D2 | **Self-enhancement bias: judge thổi điểm cho output CÙNG HỌ** → dùng judge cùng-họ với generator = circular & lệch. | [arXiv 2508.18076](https://arxiv.org/html/2508.18076v1) | 2-1 |
| D3 | **Preference leakage: khi model sinh-data và model đánh-giá quan-hệ-gần → phá tính độc-lập** cần cho eval hợp lệ. | [arXiv 2508.18076](https://arxiv.org/html/2508.18076v1) | 3-0 |
| D4 ⭐ | **Self-bias lan ra cả HỌ: judge cho điểm cao hơn cho completion của model CÙNG HỌ** → "khác-model-nhưng-cùng-họ" KHÔNG khử được bias; cần judge **thật-sự khác họ**. | [arXiv 2508.06709](https://arxiv.org/html/2508.06709v1) — *"Claude and GPT judges tend to give higher scores to completions of other models within the same family"* | 3-0 |

---

## §2. CLAIM BỊ BÁC (4 — verify GIẾT; ĐỪNG dùng nguyên văn)

> *Lưu ý:* các claim này bị bác phần lớn vì **phát-biểu QUÁ TUYỆT-ĐỐI** so với điều paper thật sự nói (không phải vì hướng sai). Hướng chung vẫn đúng; chỉ đừng trích nguyên văn.

| Claim (bị bác) | Vote | Nguồn |
|---|---|---|
| "Cơ chế cắt chi phí = tự-động loại hệ kém + chỉ để người chấm ca bất-định" (phát biểu sai cơ chế paper) | 0-3 | ACL 2022 2022.acl-long.600 |
| "GPT-4 (cụ thể) có self-preference đáng kể, thiên vị output của chính nó" (over-stated cho GPT-4) | 1-2 | arXiv 2410.21819 |
| "Meta-eval = tương quan metric↔người, BẮT BUỘC cần nhãn người" (quá tuyệt đối) | 0-3 | arXiv 2409.19507 |
| "GPT-4o & Claude 3.5 có self-bias dương có-ý-nghĩa-thống-kê" (over-stated) | 1-2 | arXiv 2508.06709 |

---

## §3. CLAIM U1–U6 → ✅ ĐÃ RE-VERIFY XONG (2026-07-01) — xem KẾT QUẢ ở §6

> Bảng dưới là claim GỐC (giả thuyết trước verify). **Kết quả verify thật + verdict + cách trích an toàn ở §6 cuối file.**
> Tóm: U1/U2/U3/U4/U5 = SUPPORTED (số khớp nguyên văn), U6 = PARTIAL (nguồn không dùng chữ "circular", chỉ suy ra
> gián tiếp). **Mọi nguồn là preprint arXiv** → chỉ bổ trợ, không làm trụ.

| # | Claim (chờ verify) | Nguồn |
|---|---|---|
| U1 ⭐⭐ | **Tương quan đơn-thuần KHÔNG đủ; phải đo Cohen's kappa (chỉnh-may-rủi).** Ví dụ cụ thể: **r=0.95 nhưng kappa chỉ 0.45**, human-likeness z = −15.2 → judge "siêu tương quan" vẫn lệch hệ thống. | [arXiv 2510.09738](https://arxiv.org/pdf/2510.09738) |
| U2 ⭐⭐ | **Protocol 2-bước validate judge:** B1 giữ judge có **Pearson r ≥ 0.80**; B2 test "human-likeness" bằng **z-score của Cohen's kappa** so với baseline người-người (kappa=0.801), nhận judge nếu **|z|<1** (giống-người), cờ-đỏ nếu z>1 ("super-consistent"). | [arXiv 2510.09738](https://arxiv.org/pdf/2510.09738) |
| U3 | **Teacher-preference bias:** judge huấn-luyện TRÊN (hoặc cùng-lineage) model bị-chấm → thiên vị model đó bất kể chất lượng. Circularity sinh ra cả khi **train trên output generator**, không chỉ khi chung weights. | [arXiv 2505.19176](https://arxiv.org/pdf/2505.19176) |
| U4 | **Bằng chứng adversarial (OffsetBias):** judge train từ data GPT-4 chỉ đạt **0.182 acc** vs **0.269** của judge train từ GPT-3.5, ở chỗ output của teacher cố-tình là đáp-án TỆ HƠN → judge cùng-nguồn miscalibrate đúng nơi output generator SAI. | [arXiv 2505.19176](https://arxiv.org/pdf/2505.19176) |
| U5 | **Đa số công trình LLM-judge validate bằng cách khớp phán-đoán-người, BỎ QUA việc nhãn-người cũng có bias/sai** → "agreement-with-human" cũng có thể lỗi; gold người không tuyệt đối. | [arXiv 2504.17087](https://arxiv.org/pdf/2504.17087) |
| U6 | **Thay điểm-tham-chiếu-người bằng điểm-LLM-judge khi calibrate/validate judge = circular & vô-hiệu** về phương pháp (đúng bẫy ta cần tránh). | [arXiv 2508.06709](https://arxiv.org/html/2508.06709v1) |

---

## §4. NGUỒN (21 — kèm nhận-dạng & chất lượng)

| URL | Nhận dạng | Quality |
|---|---|---|
| aclanthology.org/2022.acl-long.600 | **Active Evaluation: Efficient NLG Evaluation with Few Pairwise Comparisons (ACL 2022)** — dueling bandits, hybrid 89% | primary |
| arxiv.org/abs/2404.02904 | **ALOHa (NAACL 2024)** — LLM-extract + embedding + Hungarian, validated vs HAT (tiền-lệ matcher) | primary |
| proceedings.neurips.cc/…a79f3ef3… | **AndroidControl (NeurIPS 2024 D&B)** — gold action mỗi bước (proxy gold GUI) | primary |
| arxiv.org/pdf/2212.07981 | **RoSE / ACU** (meta-eval summarization, 22k nhãn) | primary |
| arxiv.org/pdf/2409.19507 | Meta-eval: tương quan không đủ + bất-định cao | primary |
| arxiv.org/pdf/1805.11474 | **Shimorina** — granularity tương quan system vs sentence | primary |
| arxiv.org/abs/2410.16834 | Analyzing Correlation Measures in NLG Meta-Eval (Xiao et al.) | primary |
| arxiv.org/html/2508.18076v1 | "Neither Valid nor Reliable? LLMs as Judges" — self-enhancement, preference leakage | primary |
| arxiv.org/html/2508.06709v1 | Self-bias lan ra cả họ | primary |
| arxiv.org/pdf/2510.09738 | **Protocol 2-bước: Pearson≥0.80 + human-likeness z (kappa)** (U1/U2) | primary |
| arxiv.org/pdf/2505.19176 | Teacher-preference bias / OffsetBias (U3/U4) | primary |
| arxiv.org/pdf/2504.17087 | Nhãn-người cũng có bias (U5) | primary |
| arxiv.org/pdf/2410.21819 | Self-preference do perplexity/familiarity (D1) | primary |
| arxiv.org/pdf/2105.12437 | Bias-variance tradeoff: người unbiased-high-variance vs metric biased-low-variance | primary |
| arxiv.org/html/2510.18488v1 | AndroidControl-Curated (LLM review+rewrite) — preprint | primary |
| arxiv.org/html/2409.14337v1 · 2410.23218 · abs/2501.14883 | (GUI/meta-eval phụ — chưa khai thác claim chính) | primary |
| galileo.ai/blog/llm-as-a-judge-vs-human-evaluation | ">80% agreement khi calibrate+human-validation" | blog (không trích làm bằng chứng) |

---

## §5. SYNTHESIS (tôi tự viết — vì pha synthesize của workflow bị lỗi-limit)

**Kết luận cho DG1 — cách validate matcher/judge với gán-tay TỐI THIỂU mà vẫn chính danh:**

1. **HITLC "chỉ-chấm-vùng-bất-định" là đường chính thức, có bằng chứng** (số peer-reviewed CHẮC = **~80%**, Mohankumar & Khapra ACL 2022; "89%" hybrid chỉ dùng thận trọng — §7.3).
   → **Áp dụng:** model mạnh khác-họ pre-label TẤT CẢ cặp candidate; người **chỉ duyệt vùng-biên/bất-đồng** giữa các matcher + mẫu audit ngẫu nhiên nhỏ. Đây là mức gán-tay tối thiểu **có cơ sở học thuật**, không phải tùy tiện.

2. **Mượn gold sẵn = được nhưng MỘT PHẦN** (A3 ủng hộ tái dùng dataset có nhãn). AndroidControl có **gold action mỗi bước** (proxy cho grounding), ScreenSpot có instruction→bbox. **NHƯNG** cả hai là *grounding/action*, KHÔNG phải đúng bài "tên↔nhãn matching" của DG1 → proxy chỉ bù một phần; **vẫn cần tập người-neo nhỏ** cho phán-đoán tên-khớp-nút. *(ALOHa là tiền-lệ: matcher PHẢI validate vs nhãn người — 2404.02904.)*

3. **Mức nhãn-người tối thiểu — phải KHIÊM TỐN & TRUNG THỰC** (B1/B2/C1/C3):
   - Benchmark meta-eval vững cần **quy mô lớn** (RoSE 22k) và benchmark nhỏ **CI rộng** → **KHÔNG over-claim** "metric đã được validate đầy đủ".
   - Đóng khung tập gán-tay của ta là **"tập HIỆU-CHỈNH/calibration" (freeze τ + đo P/R), KHÔNG phải meta-eval benchmark**. Báo CI thẳng thắn.
   - **Tương quan cao ≠ hợp lệ** (C1) và **chỉ vừa phải ở per-item** (C3) → báo thêm **Cohen's kappa** (U1/U2 — chỉnh may-rủi vì lớp mất-cân-bằng), không chỉ % thô.

4. **Bẫy circularity — đã có bằng chứng mạnh** (D1-D4, U3-U6):
   - Generator = `gpt-4o-mini` → judge **phải khác HỌ** (không chỉ khác model). D4/U3/U4: cùng-họ/cùng-lineage vẫn lệch, tệ nhất đúng nơi output generator SAI.
   - **TUYỆT ĐỐI không** validate judge bằng nhãn do chính LLM tạo (U6 = circular). Tập neo PHẢI có người (dù nhỏ, qua HITLC).
   - "Khác họ" là **cần nhưng chưa đủ** (D1) → vẫn validate vs người + báo kappa.

5. **Áp vào pre-registration (`22`):** mục H3/validate-metric thêm: (a) HITLC adjudicate-uncertain-only làm cách dựng gold; (b) báo **P/R + Cohen's kappa** (không chỉ %); (c) đóng-khung "calibration set, không phải meta-eval benchmark", báo CI; (d) judge khác-họ + vẫn neo-người; (e) trích Active-Evaluation ACL 2022 + ALOHa + (sau verify) protocol 2510.09738.

> **VIỆC CÒN LẠI:** (i) ✅ ĐÃ re-verify 6 claim (§6); (ii) ✅ ĐÃ xác nhận venue/tác-giả (§6.2 — đều preprint); (iii) gộp protocol §6.3 vào file `22` (còn lại).

---

## §6. ✅ KẾT QUẢ RE-VERIFY 6 CLAIM (2026-07-01, workflow `wf_7a51cf9f` — fetch nguồn + chấm đối kháng)

### §6.1. Bảng chốt 6 claim

| ID | Verdict | Dùng được? | Cách phát biểu AN TOÀN |
|----|---------|-----------|------------------------|
| **U1** | SUPPORTED | CÓ (số khớp, là ví-dụ-minh-hoạ) | Han et al. (2025) minh hoạ kịch bản judge có r=0.95 nhưng Cohen's κ=0.45, z=−15.2 → tương quan cao KHÔNG đủ, phải đo kappa. *(nêu rõ "kịch bản minh hoạ", nguồn preprint)* |
| **U2** | SUPPORTED | CÓ | Quy trình 2 bước (Han et al.): B1 lọc judge Pearson r≥0.80; B2 human-likeness z-score, baseline người-người κ=0.801, nhận nếu \|z\|<1. *(κ=0.801 là của họ → ta phải TỰ ĐO lại trên tập mình)* |
| **U3** | SUPPORTED | CÓ (giới hạn phạm vi) | Teacher-preference bias xuất hiện CẢ khi judge chỉ học trên OUTPUT của generator (Liu et al.) → biện minh judge KHÁC HỌ. *(bài chỉ chứng minh cho proxy judge FINE-TUNE)* |
| **U4** | SUPPORTED | CÓ (adversarial phụ) | Judge fine-tune từ nhãn GPT-4 chỉ 0.182 acc trên OffsetBias vs 0.269 từ GPT-3.5 (Liu et al., Table 1). *(là proxy Mistral-7B fine-tune, KHÔNG phải GPT làm judge trực tiếp — đừng over-claim)* |
| **U5** | SUPPORTED | CÓ (định tính) | Nhãn con người cũng có bias/sai → "agreement-with-human" không phải chuẩn vàng tuyệt đối (Li et al.) → hậu thuẫn perturbation. *(định tính, KHÔNG có số)* |
| **U6** | **PARTIAL** | CÓ HẠN CHẾ (gián tiếp) | LLM-judge có self-bias + family-bias → mốc hiệu chỉnh/validate phải độc-lập/khác-họ (suy ra từ Spiliopoulou et al.). *(bài KHÔNG dùng chữ "circular" → đừng trích như tuyên bố trực tiếp)* |

**Tổng: 5 SUPPORTED + 1 PARTIAL, không claim nào bị bác. Nhưng cả 6 nguồn là PREPRINT arXiv chưa bình duyệt.**

### §6.2. Citation đã xác nhận (metadata — đều PREPRINT)

| arXiv id | Tiêu đề / tác giả | Trạng thái |
|----------|-------------------|-----------|
| **2510.09738** | *Judge's Verdict: A Comprehensive Analysis of LLM Judge Capability Through Human Agreement* — Han, Titericz, Balough, Zhou (NVIDIA) | preprint, "under review ICLR 2026" — CHƯA peer-review |
| **2505.19176** | *Assistant-Guided Mitigation of Teacher Preference Bias in LLM-as-a-Judge* — Liu, Li, Deng, Wang, Feng | preprint (v3 09/2025), chưa rõ venue |
| **2504.17087** | *Leveraging LLMs as Meta-Judges…* — Li, Mohamud, Sun, Wu, Boulet | preprint 2025, chưa rõ venue |
| **2508.06709** | *Play Favorites: A Statistical Method to Measure Self-Bias in LLM-as-a-Judge* — Spiliopoulou et al. | preprint 08/2025, chưa rõ venue |

→ Nguyên tắc CLAUDE.md: 4 nguồn này chỉ dùng **bổ trợ / động cơ**, KHÔNG làm trụ. Mỗi nguyên tắc trụ phải kèm ≥1 peer-reviewed.

### §6.3. PROTOCOL VALIDATE-METRIC CHỐT (→ gộp vào `report/22`)

**Kiến trúc chống-vòng-lập-luận (2 tầng tách biệt):** QUYẾT matched/fallback = **nomic** (τA freeze); CHẤM = 3 cơ chế KHÁC HỌ [bge-m3 + LLM-judge khác-họ-generator + token-overlap]. Headline faithfulness = **tỉ-lệ-bịa-BASE**.

**4 quy tắc (mỗi cái gắn nguồn TRỤ peer-reviewed):**
1. **Matcher validate vs người** trên 80–120 cặp gán-tay: báo **P/R + Cohen's κ** (không chỉ %); chọn τ theo precision≥0.95, **FREEZE trước khi chạy**. [Trụ: **ALOHa, NAACL 2024**]
2. **Gán-tay tối thiểu = few-pairwise/HITLC** (pre-label + người chỉ duyệt vùng-bất-đồng → giảm **tới ~80%** số nhãn; số peer-reviewed CHẮC = 80%, "89%" chỉ dùng thận trọng — xem §7.3). [Trụ: **Active Evaluation, ACL 2022, Outstanding Paper**]
3. **LLM-judge KHÁC HỌ generator + vẫn NEO người** (né self/family-bias). [Trụ: **Panickssery, NeurIPS 2024** (self-preference) — NÊN THÊM; bổ trợ: U3/U4/U6 preprint]
4. **KHÔNG validate judge bằng nhãn LLM.** Nếu chạy 2-bước Han et al. thì **baseline κ người-người phải TỰ ĐO lại** trên tập tutorial UI (KHÔNG mượn 0.801). [Bổ trợ: U1/U2 preprint]

**Trục validate metric CHÍNH = PERTURBATION tự động** (lỗi bơm định-nghĩa ĐỘC LẬP matcher; đo detection/false-positive/đơn-điệu). [Trụ: **Sai et al., EMNLP 2021**] Human-correlation (Track B) = future-work, KHÔNG trong đậu/rớt.

**Về số cụ thể:** mọi số (r=0.95/κ=0.45/z=−15.2; r≥0.80/κ=0.801; 0.182/0.269) khớp NGUYÊN VĂN nhưng: U1 là kịch-bản-minh-hoạ (không phải đo thực nghiệm); κ=0.801 không chuyển domain; 0.182/0.269 là proxy fine-tune. → trích được nhưng luôn gắn nhãn PREPRINT + ngữ cảnh; nếu hội đồng đòi số peer-reviewed thì các số này chỉ minh-hoạ, không làm trụ.

---

## §7. ✅ TRỤ PEER-REVIEWED CHO 6 NGUYÊN TẮC VALIDATE-METRIC (xác minh 2026-07-02)

> **Bối cảnh:** §6.3 chốt protocol nhưng nhiều nguyên tắc trước đây CHỈ có preprint arXiv chống lưng (U1–U6, D1–D4).
> Nguyên tắc CLAUDE.md: **xương sống phương pháp CHỈ trích peer-reviewed**; preprint chỉ bổ trợ. Đợt này đi tìm + xác minh
> (WebSearch/WebFetch → kiểm trang proceedings aclanthology / neurips / dl.acm.org) nguồn ĐÃ BÌNH DUYỆT mạnh nhất làm TRỤ
> cho từng nguyên tắc. **Kết quả: cả 6 nguyên tắc GIỜ ĐÃ có trụ peer-reviewed** (tồn dư preprint chỉ ở vài SỐ cụ thể — khai ở §7.3).

### §7.1. BẢNG nguyên tắc → TRỤ peer-reviewed đã xác minh → dòng cite-as

| # | Nguyên tắc (dùng ở đâu) | TRỤ peer-reviewed (venue + năm) | Trạng thái | Cite-as (dán thẳng) |
|---|---|---|---|---|
| **P1** | **LLM-judge PHẢI khác HỌ generator** (né self/family-bias) — §6.3 QT3, `22` §7 | **Panickssery, Bowman & Feng — NeurIPS 2024** (Main, Oral) + bổ trợ **Zheng et al. — NeurIPS 2023** (thuật ngữ "self-enhancement bias") | ✅ PEER-REVIEWED | Panickssery, Bowman & Feng (2024), "LLM Evaluators Recognize and Favor Their Own Generations," NeurIPS 2024. |
| **P2** | **Matcher đo theo NGỮ NGHĨA (không so chuỗi thô) + validate vs nhãn người** — §6.3 QT1, metric Bịa/Faithfulness | **Petryk et al. (ALOHa) — NAACL 2024** (Short) + bổ trợ **Rohrbach et al. (CHAIR) — EMNLP 2018** | ✅ PEER-REVIEWED | Petryk et al. (2024), "ALOHa: A New Measure for Hallucination in Captioning Models," NAACL-HLT 2024 (Short), pp. 342–357. |
| **P3** | **Giảm khối lượng gán-tay bằng few pairwise / chọn cặp thông minh (HITLC)** — §6.3 QT2, `22` §7 | **Mohankumar & Khapra (Active Evaluation) — ACL 2022** (Long, **Outstanding Paper**) | ✅ PEER-REVIEWED | Mohankumar & Khapra (2022), "Active Evaluation: Efficient NLG Evaluation with Few Pairwise Comparisons," ACL 2022 (Long), pp. 8761–8781. |
| **P4** | **Validate metric bằng PERTURBATION (bơm lỗi đã-biết → đo độ nhạy)** — H3 `22`, trục validate chính | **Sai et al. — EMNLP 2021** (Main) + bổ trợ **Ribeiro et al. (CheckList) — ACL 2020** (Best Paper) | ✅ PEER-REVIEWED | Sai et al. (2021), "Perturbation CheckLists for Evaluating NLG Evaluation Metrics," EMNLP 2021, pp. 7219–7234. |
| **P5** | **View Hierarchy / a11y tree KHÔNG phải ground truth hoàn hảo** (thiếu/nhiễu nhãn) → cần lớp hậu kiểm + fallback | **Chen et al. — ICSE 2020** (ACM/IEEE, Distinguished Paper) + bổ trợ **Ross et al. — TACCESS 2020** (tạp chí) | ✅ PEER-REVIEWED | Chen et al. (2020), "Unblind Your Apps: Predicting Natural-Language Labels for Mobile GUI Components by Deep Learning," ICSE 2020, pp. 322–334. |
| **P6** | **Human-eval KHÔNG phải chuẩn vàng tuyệt đối** → biện hộ BỎ human-correlation làm cổng đậu/rớt, dùng perturbation | **Clark et al. — ACL-IJCNLP 2021** (Long) + bổ trợ **Karpinska et al. — EMNLP 2021** | ✅ PEER-REVIEWED | Clark et al. (2021), "All That's 'Human' Is Not Gold: Evaluating Human Evaluation of Generated Text," ACL-IJCNLP 2021, pp. 7282–7296. |

**Kết luận bảng:** 6/6 nguyên tắc đã có TRỤ bình-duyệt → thay được toàn bộ vai "trụ" mà trước kia preprint (U1–U6, D1–D4) tạm giữ.
Preprint KHÔNG bị vứt — hạ xuống đúng vai **bổ trợ/động cơ** (chi tiết số cụ thể ở §7.3).

### §7.2. Mỗi trụ: venue chính xác + vì-sao-đủ-làm-trụ (kèm quote đã verify)

- **P1 — Panickssery, Bowman & Feng, NeurIPS 2024** (Advances in NeurIPS 37, Main Conference, Oral; verify trên `proceedings.neurips.cc/…/7f1f0218…`).
  *Đủ làm trụ vì:* là bài peer-reviewed chuyên đề self-preference, chứng minh trực tiếp "LLM evaluator scores its own outputs higher than others' while human annotators consider them of equal quality" → căn cứ vững cho yêu cầu judge-khác-họ.
  *Caveat:* bài chứng minh HIỆN TƯỢNG bias, KHÔNG chứng minh "đổi họ thì khử sạch" → phát biểu là biện-pháp-GIẢM-THIỂU. Ghép thêm Zheng et al. NeurIPS 2023 cho thuật ngữ chuẩn "self-enhancement bias".
- **P2 — Petryk et al. (ALOHa), NAACL 2024 Short**, pp. 342–357 (`aclanthology.org/2024.naacl-short.30/`).
  *Đủ làm trụ vì:* chính là tiền lệ matcher mà DG1 kế thừa — "semantic similarity + Hungarian matching" (không so chuỗi thô), và được đo độ chính xác trên **HAT — gold-standard subset annotated for hallucinations** (tập nhãn NGƯỜI) → hậu thuẫn cả "đo theo ngữ nghĩa" lẫn "matcher bám phán đoán người".
  *Caveat:* ALOHa báo "13.6% more hallucinated objects" (so độ chính xác trên gold), KHÔNG báo hệ số tương quan matcher↔người → nếu muốn claim "validated vs human bằng tương quan định lượng" thì dựa Sai et al. (P4), đừng dồn hết vào ALOHa. CHAIR (EMNLP 2018) bổ trợ cho ý "đối chiếu tập-đối-tượng-thật thay vì so chuỗi".
- **P3 — Mohankumar & Khapra (Active Evaluation), ACL 2022 Long, Outstanding Paper**, pp. 8761–8781 (`aclanthology.org/2022.acl-long.600/`).
  *Đủ làm trụ vì:* là bài giải thưởng, chứng minh "the number of human annotations can be reduced by 80%" bằng dueling-bandits/few-pairwise → trụ vững cho luận điểm "giảm mạnh gán-tay có cơ sở học thuật".
  *Caveat QUAN TRỌNG:* con số CHÍNH THỐNG là **80%** (tìm hệ-xếp-hạng-đầu bằng ít so-cặp), KHÔNG phải "89%" như report/27 §5/§6.3 và report/22 đang ghi. "89%" và ý "chỉ chấm vùng-bất-định model pre-label" là active-learning/uncertainty-sampling KHÁC, hiện CHƯA có trụ peer-reviewed → xem §7.3.
- **P4 — Sai et al., EMNLP 2021 Main**, pp. 7219–7234 (`aclanthology.org/2021.emnlp-main.575/`).
  *Đủ làm trụ vì:* làm ĐÚNG việc ta cần — "perturb the output such that the quality gets affected only along this specific criteria … a fine-grained assessment of automatic evaluation metrics exposing their limitations" → trụ trực tiếp và mạnh nhất cho H3 (validate metric bằng bơm lỗi có chủ đích). Ribeiro et al. ACL 2020 (CheckList, Best Paper) bổ trợ nền phương pháp behavioral-testing.
  *Caveat:* cả hai ở miền NLG text→text → trong luận văn phải nói rõ là "ADAPT phương pháp perturbation-based metric validation sang miền tutorial UI (image→text)", KHÔNG claim hai bài đã validate chính các metric của ta.
- **P5 — Chen et al., ICSE 2020** (ACM/IEEE, SIGSOFT Distinguished Paper), pp. 322–334 (`dl.acm.org/doi/10.1145/3377811.3380327`).
  *Đủ làm trụ vì:* định lượng ">77% apps have issues of missing labels" trên 10,408 app → chứng cứ mạnh rằng VH/a11y tree KHÔNG phải chân lý hoàn hảo, biện minh cho lớp hậu-kiểm + fallback-mô-tả của DG1. Ross et al. TACCESS 2020 (tạp chí) bổ trợ phổ rào cản nhãn.
  *Caveat:* trích tập trung ở khía cạnh THIẾU nhãn; vế "nhãn generic/nhiễu" chỉ hàm ý → nếu cần trụ riêng cho nhãn-kém-chất-lượng thì thêm Ross et al.
- **P6 — Clark et al., ACL-IJCNLP 2021 Long**, pp. 7282–7296 (`aclanthology.org/2021.acl-long.565/`).
  *Đủ làm trụ vì:* chứng minh trực tiếp "without training, evaluators distinguished between GPT3- and human-authored text at random chance level" → nhãn người (chưa huấn luyện) có bias/bất-nhất, đủ biện hộ quyết định BỎ human-correlation làm cổng đậu/rớt và dùng perturbation tự động. Karpinska et al. EMNLP 2021 bổ trợ (crowd kém tin cậy).
  *Caveat:* bài nói về con người ĐÁNH GIÁ text sinh, KHÔNG trực tiếp về inter-annotator agreement khi chấm chất lượng → nếu cần luận điểm "agreement thấp" thuần thì thêm Karpinska/Amidei làm phụ.

### §7.3. TỒN DƯ chỉ-preprint (khai TRUNG THỰC — không làm trụ, chỉ bổ trợ/động cơ)

| Ý / số cụ thể | Trạng thái nguồn | Cách phát biểu AN TOÀN |
|---|---|---|
| **"Giảm ~89% nhãn" + "chỉ chấm vùng-bất-định (adjudicate-uncertain-only)"** | ONLY_PREPRINT (con số 89% không có trong bài ACL 2022; nó là ý active-learning khác) | **SỬA "89%"→"tới ~80%"** và trích Mohankumar & Khapra ACL 2022. Ý "chỉ duyệt vùng-bất-định" đóng khung là **thiết-kế-nội-bộ/động-cơ** (uncertainty sampling), KHÔNG gắn số peer-reviewed. |
| **Protocol 2-bước Pearson r≥0.80 + human-likeness z-score kappa (κ=0.801)** — U1/U2 | ONLY_PREPRINT (Han et al., arXiv 2510.09738, "under review ICLR 2026") | Giữ như **quy trình tham khảo/bổ trợ**; nếu áp thì **TỰ ĐO lại baseline κ người-người** trên tập tutorial UI. Trụ đậu/rớt vẫn là perturbation (P4). |
| **Teacher-preference / family-level self-bias chi tiết** — U3/U4/U6, D2/D4 | ONLY_PREPRINT (2505.19176, 2508.06709, 2508.18076) | Dùng **bổ trợ** cho P1; TRỤ là Panickssery NeurIPS 2024. Đừng trích số 0.182/0.269 như bằng chứng chính (proxy fine-tune Mistral, không phải GPT-judge). |
| **Cohen's κ như tiêu chí phụ khi báo P/R matcher** | Bản thân κ (Cohen 1960, *Educ. Psychol. Meas.*) là peer-reviewed kinh điển | Được — trích Cohen (1960) cho κ; nhưng "ngưỡng |z|<1 / r≥0.80" thì vẫn chỉ preprint. |

→ **KHÔNG có nguyên tắc nào NOT_FOUND.** Toàn bộ 6 nguyên tắc TRỤ đã có nguồn bình-duyệt; phần preprint co lại đúng vai bổ trợ.

### §7.4. DANH SÁCH CẬP NHẬT cần sửa (đã áp một phần vào `22` §7)

**Trong `report/27`:**
- §5 mục 1 và §6.3 QT2: đổi **"giảm thêm 89% số nhãn"** → **"giảm tới ~80% (Mohankumar & Khapra, ACL 2022)"**; tách ý "chỉ-chấm-vùng-bất-định" thành thiết-kế-nội-bộ (không gắn con số).
- §6.3 QT1: thêm trụ **ALOHa NAACL 2024** (đã có) + ghi caveat "ALOHa không báo tương quan; tương quan-định-lượng dựa Sai et al.".
- §6.3 QT3: xác nhận trụ **Panickssery NeurIPS 2024** (thay "NÊN THÊM" → "ĐÃ CHỐT"); Zheng NeurIPS 2023 bổ trợ.
- §6.3 dòng "Trục validate CHÍNH = perturbation": trụ **Sai et al. EMNLP 2021** (đã có) + thêm Ribeiro ACL 2020 bổ trợ.

**Trong `report/22` §7:** (đã cập nhật — xem file) đổi "~89%"→"~80% (ACL 2022)"; chốt Panickssery NeurIPS 2024 làm trụ P1 (bỏ chữ "cần thêm"); thêm trụ P5 (Chen ICSE 2020) và P6 (Clark ACL 2021) vào phần biện hộ VH-không-hoàn-hảo + bỏ-human-correlation.

---

## §8. ✅ METRIC-VERIFY ĐỐI KHÁNG "ĐỦ ĐÓNG GÓP THẠC SĨ?" (R-08, 2026-07-05, `wf_38650b3d-e50`)

> Đối xứng với R-07 (pipeline). Phản-bác 3-phiếu 8 khẳng định lõi của phương pháp đánh giá (contribution B) + kiểm venue.

### PHÁN QUYẾT: B ĐỦ làm đóng góp khoa học thạc sĩ — CÓ ĐIỀU KIỆN (đối xứng A). 7/8 sống, 1 đổ (M6).
Mọi đòn hạ được đều nhắm phần **PHÁT-BIỂU TUYỆT-ĐỐI**, không chạm thiết kế lõi → đóng góp vững-cấu-trúc nhưng đang overclaim câu chữ.

### 8 khẳng định
| ID | Nội dung | Kết quả | Chữa |
|---|---|---|---|
| M1 | no-gold neo cấu trúc (VH/gold) | ✅ sống (1 refute framing) | "thay được vai người-viết" → "proxy no-gold CÓ ĐIỀU KIỆN, recall-conditioned, validate per-task" (VH lossy: chỉ grounding/thứ-tự, không adequacy/clarity) |
| M2 | perturbation = trục validate chính | ✅ sống (1 refute) | GIỮ hedge "điều kiện CẦN không đủ" (Xiao EMNLP23), KHÔNG nâng "đủ" |
| M3 | bỏ human-correlation khỏi cổng | ✅ sống — NHƯNG đòn đáng lo nhất | phần "đẩy HẲN future-work, 0 annotate" BỊ BÁC → **BẮT BUỘC chạy ≥1 mẫu-nhỏ human-validation per-criterion NGAY** (không làm gate cứng); gọi "content+sensitivity validity (partial)", đừng claim construct-validity đầy đủ |
| M4 | anti-circularity 3 cơ chế độc lập | ✅ sống (1 refute) | "ĐỘC LẬP"/"khác-họ là ĐỦ" → "GIẢM không LOẠI tương quan; token-overlap = trục phi-neural thực-sự-khác; báo phi/neff giữa judges". (Bước QUYẾT dùng embedding ≠ generator nên circularity generator-tự-chấm vốn không tồn tại ở bước quyết.) |
| M5 | τ thứ-tự-bộ-phận | ✅✅ sống sạch 0/3 | attribution: thêm **Brandenburg-Gleißner-Hofmeier** cho ca cặp-tự-do (khớp hơn Fagin); khai "near-metric dùng scoring", tránh "the correct measure" |
| M6 | Step-SR = trục "làm tới đích" | ❌ **ĐỔ 2/2** | **TỰ-BÁC bởi chính AndroidControl (Li NeurIPS24):** step-acc không dự báo human-ranking; teacher-forcing che lỗi tích lũy → KHÔNG đo "tới đích". **Reframe: Step-SR = proxy chẩn-đoán NĂNG-LỰC-TỪNG-BƯỚC (teacher-forced), KHÔNG phải thước tới-đích**; 14% = ngưỡng-mượn-AITW. Sau reframe vẫn hợp lệ. |
| M7 | thống kê cluster ít | ✅✅ sống sạch 0/3 | headline = wild-bootstrap/CV3 (không phải pairs-bootstrap); báo kèm effective-#clusters (Carter-Schnepel-Steigerwald) |
| M8 | B đủ tư cách đóng góp | ✅✅ sống sạch 0/3 | combo không bị scoop; NeurIPS guidelines công nhận "novel combination"; điều kiện: insight không-tầm-thường = đối-chứng-thất-bại + DG2 dương |

### B KHÁC G-Eval/RAGAS ở đâu (lằn ranh khoa học): (1) neo NGUỒN CẤU TRÚC phi-model (VH/gold) thay vì LLM tự phán; (2) validate bằng perturbation độc-lập-matcher; (3) tách QUYẾT/CHẤM + judge khác-họ. → vượt "áp G-Eval vào GUI".

### CITATION — sửa 1 lỗi: **Active Evaluation (Mohankumar & Khapra, ACL 2022) = OUTSTANDING Paper, KHÔNG phải "Best Paper"** (Best Paper ACL22 = Kitaev-Lu-Klein). Sửa CLAUDE.md §4 + report/27 §7 P3 + report/22. Số 80% giữ nguyên. (BUMP/Ribeiro/Fagin/Lapata/Chim đều ĐÚNG venue.)

### "HAI ĐÓNG GÓP NGANG NHAU" — GIỮ ĐƯỢC (ngang nhau CÓ ĐIỀU KIỆN, đối xứng):
- B **mạnh hơn A** ở nền peer-reviewed (M5/M7/M8 sống sạch); **ngang A** ở phụ thuộc số chưa-chạy.
- Cả hai = "đủ-có-điều-kiện, chờ DG2 dương". Không bên nào rơi "chỉ engineering".
- Điều kiện giữ ngang của B = 3 việc rẻ: reframe M6 · mẫu-nhỏ human-validation (M3) · dựng perturbation harness ra số.

### Preprint (chỉ bổ trợ, KHÔNG trụ): refute-M4 correlated-errors (2605.29800, 2601.22548) · refute-M3 validation-gap (2601.07648) · Han 2510.09738 · Liu 2505.19176. Trụ đậu/rớt vẫn peer-reviewed (Sai, Panickssery, ALOHa, Clark, MacKinnon, AndroidControl…).
