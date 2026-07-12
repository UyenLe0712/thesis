# 🧑‍⚖️ DG1 — PROTOCOL LLM-AS-JUDGE (scorer độc-lập #2) + nền nghiên cứu đã verify (2026-06-30)

> **File này lưu kết quả 3 agent research + protocol LLM-judge đã thiết kế** cho DG1, để KHỎI nghiên cứu lại.
> Cặp đôi với `report/27` (validate metric / gán-tay tối thiểu). Quyết định liên quan: scope = **Bậc VỮNG**;
> matcher chấm = **bge-m3 (embedder) + LLM-judge (khác họ, đã validate)**; validate metric = **perturbation, BỎ human-correlation**.
>
> **Bối cảnh:** LLM-judge ở DG1 KHÔNG chấm "tutorial hay/dở" (chủ quan, dễ bị vặn). Nó là một **phán đoán HẸP, nhị-phân,
> neo-tham-chiếu**: *"tên-nút model viết có ứng ĐÚNG MỘT nút THẬT trong View Hierarchy không?"* → đúng vùng LLM-judge đáng tin.

---

## §A. NỀN TẢNG LLM-JUDGE + KIỂM-SOÁT-BIAS (citation đã verify)

| Nguồn (peer-reviewed trừ khi ghi preprint) | Bài học cho ta |
|---|---|
| **Zheng et al., NeurIPS 2023 D&B** (MT-Bench, "Judging LLM-as-a-Judge") | (1) **Reference-guided grading** giảm tỉ-lệ-sai judge **70%→15%** trên bài kiểm-được → đưa danh-sách-nút-thật vào prompt = vũ khí mạnh nhất. (2) Judge đạt **80–85% đồng thuận với người** trên bài hẹp. (3) Position-bias → swap/few-shot (consistency 65%→77.5%). |
| **Wang et al., ACL 2024** ("LLMs are not Fair Evaluators") | Position-bias KHỔNG LỒ: GPT-4 lật kết-luận **46%** khi swap. Khử bằng **BPC** (chấm cả 2 chiều rồi trung-bình) + **MEC** (rationale-trước-điểm). |
| **Tripathi et al., COLM 2025** ("Pairwise or Pointwise?") | **Pointwise (chấm tuyệt đối) bền hơn pairwise ~4×** trước distractor (9% vs 35% bị lật) → ta dùng **pointwise yes/no**, KHÔNG pairwise. |
| **Wu & Aji, COLING 2025** ("Style Over Substance") | Judge (và người) chấm cao văn-trôi-chảy-nhưng-SAI → judge của ta **chỉ 1 chiều "nút tồn-tại"**, TUYỆT ĐỐI không trộn clarity/hữu-ích vào cùng call. |
| **Panickssery et al., NeurIPS 2024** ("Evaluators Favor Their Own Generations") | LLM nhận ra & thiên-vị output cùng-họ → generator = `gpt-4o-mini` ⇒ **judge PHẢI khác họ** (không phải GPT). |
| **Koo et al., Findings ACL 2024** (CoBBLEr) | LLM-judge **không tin được trên XẾP HẠNG MỞ** (40% so-sánh dính bias) → ta phải **nói rõ** bài ta là hẹp/nhị-phân/neo-tham-chiếu = vùng dễ, và **CHỨNG MINH bằng tập gold**. |
| **Wang et al., ICLR 2023** (Self-Consistency) | temp=0 cho verdict; lấy **k mẫu majority-vote** để ước lượng ổn định, đánh dấu "uncertain" khi lệch. |
| Gu et al., *A Survey on LLM-as-a-Judge*, **arXiv 2411.15594 (preprint)** | Taxonomy pointwise/pairwise/listwise · reference-free/based · constrained/structured output. *(Bản tạp chí The Innovation 2025 — CHƯA xác nhận DOI, đừng trích bản journal khi chưa kiểm.)* |

> *Honesty:* cấu hình chính xác của G-Eval (EMNLP 2023) chưa verify được số n=20/temp — đừng trích số cụ thể.

---

## §B. TIỀN-LỆ HALLUCINATION/GROUNDING (khung "verify từng claim theo reference")

| Nguồn | Map vào bài ta |
|---|---|
| **ALOHa, Petryk et al., NAACL 2024 short** (2404.02904) ⭐ gần nhất | Đo hallucination = **LLM trích đối-tượng + matcher ngữ-nghĩa (S-BERT) + Hungarian + lấy min**, so với **tập tham-chiếu**. Đúng cấu trúc bài ta. **ALOHa tự validate matcher vs nhãn người (HAT)** → tiền-lệ "matcher phải đo P/R". Giữ **Hungarian 1-1** (1 nút thật không "đỡ" nhiều tên bịa). |
| **FActScore, Min et al., EMNLP 2023** (Outstanding) | Tách thành claim nhỏ → **% claim được reference hỗ-trợ**; estimator retrieval+LM (<2% lỗi vs người). → faithfulness = #bước-match / #bước. |
| **RAGAS, Es et al., EACL 2024 demo** | Faithfulness = decompose → **mỗi statement: LLM phán "có được context entail không" (yes/no)** → #supported/#total. Template prompt sạch nhất cho ta (context = danh-sách-nút-thật). |
| **SummaC, Laban et al., TACL 2022** | Khung **NLI-entailment** ("màn có nút X" ⊨ "bấm X?") = cross-check **tất-định, KHÁC HỌ, miễn phí** (tùy chọn lớp 3). |
| **SeeClick, Cheng et al., ACL 2024** (nguồn ScreenSpot) | Chuẩn GUI chấm grounding = **point-in-bbox** (lập trình), KHÔNG phải LLM-judge → ít tiền-lệ LLM-judge cho "nút tồn-tại"; ta **mượn từ captioning/factuality** (điểm mạnh, không yếu). |
| *(preprint, đừng trình như đã bình duyệt)* AndroidControl-Curated (2510.18488), AgentStudio (2403.17918) | LLM-judge ở GUI chỉ dùng cho **trajectory-success/curation**, đều preprint. |

---

## §C. ⭐ PROTOCOL CỤ THỂ (scorer độc-lập #2 = LLM-judge)

> Vai: **scorer thứ 2** chấm faithfulness, ĐỘC LẬP & KHÁC HỌ. **TUYỆT ĐỐI không** dùng làm bộ quyết matched/fallback (đó vẫn là nomic) — chống circularity (ALOHa + CLAUDE.md).

**Input mỗi bước (neo-tham-chiếu · 1-chiều · pointwise):**
```
Danh sách nút THẬT trên màn (CHỈ những nút này tồn tại):
[0] "Submit"   [1] "Save draft"   [2] "Back"   [3] "Amount" ...
Bước hướng dẫn nói: người dùng bấm/dùng nút tên "Confirm".
NHIỆM VỤ: Tên này có ứng với ĐÚNG MỘT nút trong danh sách trên không?
CHỈ xét nút-có-tồn-tại — KHÔNG xét đúng-ý-người-dùng, KHÔNG xét rõ-ràng/hữu-ích.
Xuất JSON: {"verdict":"match"|"hallucinated","matched_index":<int|null>,"reason":"<≤12 từ>"}
```

**8 kiểm-soát-bias (mỗi cái gắn nguồn):**

| # | Kiểm soát | Nguồn |
|---|---|---|
| 1 | Tách 1 claim/bước, điểm = #match / #total | FActScore, RAGAS |
| 2 | Đưa **full danh sách nút thật** làm reference | Zheng (70%→15%) |
| 3 | **Pointwise** yes/no, không pairwise | Tripathi COLM'25 |
| 4 | **Chỉ 1 chiều "tồn-tại"**, không trộn clarity | Wu&Aji COLING'25 |
| 5 | **Judge khác HỌ** gpt-4o-mini | Panickssery NeurIPS'24 + D4 (report/27) |
| 6 | **Trộn thứ tự danh sách (seeded)** + uncertain → chạy chiều đảo (BPC) | Wang ACL'24 |
| 7 | **temp=0**; k=3 self-consistency → "uncertain" khi lệch | Wang ICLR'23 |
| 8 | **One-to-one** (1 nút thật không đỡ nhiều tên bịa) | ALOHa Hungarian |
| + | JSON schema = an-toàn-parse (KHÔNG phải bằng chứng đúng) | engineering hygiene |

`Faithfulness_LLM = #(verdict=match) / n`.

---

## §D. VALIDATE JUDGE + KẾT HỢP 3 SCORER (gán-tay tối thiểu — chi tiết `report/27`)

**Validate judge (khâu khiến nó chính danh):** chấm judge trên **CHÍNH tập gold** dùng freeze τA →
báo **Precision / Recall / F1 + Cohen's kappa** (kappa vì lớp mất-cân-bằng: đa số nút có thật → % thô bị thổi).
Mốc = vùng **~80–85% / kappa ngang người** (Zheng). **Gán-tay tối thiểu = HITLC** (report/27 A1): model mạnh khác-họ
pre-label hết, người **chỉ duyệt vùng-biên/bất-đồng** + audit nhỏ → giảm ~89% nhãn. **KHÔNG** validate judge bằng nhãn-LLM (circular, report/27 U6).

**Ba scorer — vai rõ ràng (chống circularity):**
| Scorer | Họ | Vai |
|---|---|---|
| **nomic** @τA | embedding A | **QUYẾT** matched/fallback (khâu hệ-thống, KHÔNG chấm) |
| **bge-m3** @τB | embedding B | **CHẤM headline** (tất-định, rẻ, tái lập) |
| **LLM-judge** | khác họ | **CHẤM đối-chứng** (đã validate P/R+kappa) — kết-luận phải đứng vững dưới CẢ HAI |

Báo faithfulness dưới **bge-m3 VÀ LLM-judge** + độ-đồng-thuận (kappa). LLM-judge thêm vai **trọng-tài vùng-biên** (chỉ chạy nơi cosine lưỡng-lự → rẻ).
*(Tùy chọn miễn phí: NLI-entailment kiểu SummaC làm lớp-3 tất-định.)*

**Chọn model judge — free-first:** thử **local khác-họ** trước (text-only, CPU chạy được — vd qwen2.5/llama bản instruct);
validate trên gold; **chỉ escalate API** (Claude/Gemini, KHÁC HỌ gpt-4o-mini) nếu local rớt. **KHÔNG** dùng GPT-family làm judge.
→ Test **15 mẫu local trước** để soi chất-lượng pipeline rồi mới chạy diện rộng.
