---
name: vcl-fair-paper
description: >-
  Hỗ trợ VIẾT / SỬA 2 bài báo tách từ luận văn này: bài VCL (tiếng Việt, nộp trước, =DG1 đánh giá hướng dẫn 1 ảnh)
  và bài FAIR (tiếng Anh, nộp sau, =DG2 suy luận trật tự màn). Dùng khi người dùng nói về viết paper, abstract,
  related work, method, experiment, rebuttal, hoặc nhắc "VCL"/"FAIR". Bảo đảm KHÔNG trùng giữa 2 bài, KHÔNG bịa
  số liệu/citation, attribution đúng. Trao đổi bằng tiếng Việt.
---

# Skill: Viết 2 bài báo VCL (DG1, tiếng Việt) + FAIR (DG2, tiếng Anh)

> Skill này là "bộ não" cho các phiên VIẾT PAPER tách từ luận văn `D:\Master\Thesis`. Đọc kèm `CLAUDE.md`
> (auto-load) + `report/05_final_plan.md` (nguồn-sự-thật) + `report/KE_HOACH_2_BAI_BAO.md` (kế hoạch tách 2 bài).

## 0. Bối cảnh luận văn
Sinh tự động **hướng dẫn sử dụng phần mềm** (step-by-step) từ **ảnh giao diện + câu hỏi** bằng VLM. **HAI đóng góp NGANG NHAU (CHỐT 2026-06-25 — đổi từ khung cũ "pipeline chỉ là hệ tham chiếu"):** (A) **HỆ ReOrder-Tutor sinh tutorial TỐT** — phải RA KẾT QUẢ TỐT (giảm bịa/tăng đúng-chỗ so baseline viết-tự-do & so **GPT-4o E2E**; thắng GPT-4o toàn diện = bonus); (B) **PHƯƠNG PHÁP ĐÁNH GIÁ** khi không có gold tutorial. Hai nhánh đánh giá: **DG1** (1 ảnh) và **DG2** (nhiều ảnh xáo trộn → tự sắp xếp). **VẪN KHÔNG claim SOTA leaderboard** (setup khác — sinh tutorial cho người, không phải agent bấm máy). Lõi **off-the-shelf** (KHÔNG fine-tune); **LoRA-grounding = bậc nâng cấp tùy chọn**. **🔧 PIPELINE LÕI = DESIGN E (chốt 2026-06-25, spec `report/14`):** "lớp trung-thực-hoá độc-lập-model" — bộ sinh VLM **THAY ĐƯỢC** (Qwen mở lõi; GPT-5/Gemini-3 đối chứng) sinh **gọi nút theo TÊN** → **oracle grounding BÊN CẠNH** (không chặn sinh) → **fallback mô tả bằng lời**. OmniParser+SoM+constrained-ID = **1 bậc ablation**. Metric thêm **coverage có trọng số + Followability/Step-SR**. "Thắng" frontier = trục trung-thực/đúng-chỗ/làm-theo + rẻ + bền, **KHÔNG claim SOTA leaderboard**. Venue: ScreenSpot-Pro=**ACM MM2025**, GUI-Actor=NeurIPS2025, IFBench=NeurIPS2025.

## 1. Tách 2 bài — ai viết cái gì
| | **VCL** (nộp TRƯỚC · tiếng VIỆT · dễ hơn) | **FAIR** (nộp SAU · tiếng ANH · cạnh tranh hơn) |
|---|---|---|
| Đóng góp | **DG1** — khung đánh giá KHÔNG-tham-chiếu cho hướng dẫn từ **1 ảnh** | **DG2** — **Screen-Order Inference** (N ảnh xáo trộn → sắp xếp) |
| Dataset | **MobileViews** + **ScreenSpot** (đối chứng) | **AndroidControl** (+ GUI-Odyssey optional) |
| Metric headline | grounding (point-in-bbox) · hallucination · clarity | **Kendall τ-b partial-order-aware** · signal-attribution · ordering-gap |
| Điểm cộng riêng | demo định tính **tiếng Việt** · thang bậc C1/C3/C4 · pilot người | chống-vòng-lập-luận (D1) · GOAL-ONLY/VISUAL-ONLY · null-theo-N |

Tựa/abstract nháp (cả VN & EN) đã có sẵn trong `report/KE_HOACH_2_BAI_BAO.md` — dùng làm điểm xuất phát.

## 2. LUẬT chống TRÙNG (bất biến — vi phạm là hỏng cả 2 bài)
1. Mỗi bài MỘT câu hỏi + headline KHÁC nhau (xem bảng §1 — khác cả 7 trục).
2. KHÔNG nộp cùng kết quả/thí nghiệm cho cả hai.
3. **VCL ra trước ⇒ FAIR PHẢI trích dẫn VCL** (self-citation) + nêu rõ phần MỚI; FAIR không lặp bảng số DG1.
4. Phần dùng chung (pipeline ReOrder-Tutor, động cơ) → mỗi bài 1 đoạn ngắn + **dẫn bài kia**; **viết lại câu chữ** (FAIR tiếng Anh dễ bị quét trùng).
5. Mỗi bài tự-chứa (intro → method → experiments → conclusion riêng).

## 3. RÀNG BUỘC CỨNG (không bao giờ vi phạm)
- **KHÔNG BỊA** số liệu, citation, venue, năm. Chưa chạy thì ghi "kết quả dự kiến", KHÔNG điền số giả.
- **Phân biệt peer-reviewed vs preprint**; xương sống phương pháp chỉ trích peer-reviewed; preprint chỉ là **công cụ kỹ thuật**.
- Khi tư vấn về model/giá/API hoặc kiểm citation: **đọc nguồn, không trả lời theo trí nhớ** (verify lại venue/arXiv).
- **HAI đóng góp NGANG NHAU** (hệ ra kết quả TỐT + phương pháp đánh giá); **KHÔNG claim SOTA leaderboard** (setup khác). "Kết quả tốt" = thắng baseline trên metric của mình + so **GPT-4o E2E** + demo định tính.
- Nguyên tắc **"null vẫn đậu"** áp cho **nhánh đánh giá + phần "đo cơ chế nào trả công"** (giữ một phần lưới an toàn); **claim mức-chắc-thắng của hệ kỳ vọng DƯƠNG** (constrained-gen loại bịa tận gốc → gần như chắc thắng baseline về faithfulness).

## 4. CITATION & DATASET đã VERIFY (dùng đúng, đừng đổi)
- **Chim, Ive, Liakata** — *Evaluating Synthetic Data Generation from User Generated Text*, **Computational Linguistics 51(1):191–233, 2025** (tạp chí, KHÔNG phải ACL 2025). Là **bài THẦY GIỚI THIỆU / bài tham khảo** mình kế thừa khung Intrinsic/Extrinsic — **KHÔNG phải paper của thầy viết**; trích đúng tên tác giả.
- **MobileViews** — arXiv **2409.14337** ("A Million-scale and Diverse Mobile GUI Dataset"), **PREPRINT** (~600.000 màn). Chỉ dùng làm **nguồn ảnh + nhãn vị trí (view-hierarchy)**, không làm xương sống.
- **AndroidControl** — Li et al., arXiv **2406.03679**, **NeurIPS 2024 (Datasets & Benchmarks)** — đã bình duyệt. 15.283 episode · 833 app · mean ~5,5 bước · p95=13. Toạ độ là ĐIỂM click (x,y), không phải bbox. Histogram theo từng N chưa công bố → **tự đếm (cổng KN)**.
- **ScreenSpot** — bản gốc từ **SeeClick** (arXiv 2401.10935, **ACL 2024**); bản -v2 từ **OS-Atlas** (arXiv 2410.23218, **ICLR 2025**). ~1.272 mẫu, 3 nền tảng. Đối chứng point-in-bbox; chỉ đơn-bước.
- **Kendall τ-b**: Kendall 1938 + **Lapata, CL 32(4):471–484, 2006** (tiền lệ τ chấm ordering) + Gao et al. NAACL 2025 (meta-eval). **🔧 τ-b "chỉ cặp bắt buộc" (partial-order/bucket-order) = Fagin, Kumar, Sivakumar, SIAM JDM 17(1), 2003 (optimistic p=0) + Fagin et al. SIAM JDM 20(3), 2006** — PHẢI trích, KHÔNG claim "tự-định-nghĩa". Sort-Story (EMNLP2016) dùng **Spearman** (KHÔNG τ); Wu et al. ACL2022 dùng τ; RankGPT EMNLP2023 = **phương pháp listwise**; **pairwise+Copeland = PRP-Allpair (Qin et al., Findings NAACL 2024) + Copeland 1951** (bảo vệ bằng BẤT-BIẾN-thứ-tự-đầu-vào, không bằng "xếp chính xác hơn").
- **Ngưỡng 14%**: từ AITW (NeurIPS 2023).
- **Metric (đã ĐÍNH CHÍNH deep-research 2026-06):** grounding **point-in-bbox** (SeeClick ACL2024). Hallucination: **metric CHÍNH = matcher open-vocab kiểu ALOHa (NAACL2024 short)**; **HER/CHAIR (EMNLP2018) chỉ là baseline đối chứng** (vocab-đóng bỏ sót 13–31%) + **coverage** (VALOR-EVAL, Findings ACL2024); **BỎ POPE/SummaC/QAGS/SelfCheckGPT/HaluEval khỏi headline**; **FActScore/SAFE CẤM dùng cho trật-tự-màn** (mù thứ tự theo thiết kế). Clarity: **IFEval (arXiv 2311.07911, PREPRINT) chỉ gánh FORMAT, KHÔNG gánh Clarity** ("động-từ/1-action" = quy ước Microsoft Style Guide, không phải IFEval); **Clarity = rubric + G-Eval (EMNLP2023) + người chấm** (tiền lệ rubric: Excel-tutorial FSE Companion 2026). **Track B mạnh hơn:** pairwise-acc tie-calibration (Deutsch *Ties Matter*, EMNLP2023) + tách system/instance correlation (SummEval TACL2021) + **ĐO tương quan lỗi giữa các judge** (4 họ chỉ GIẢM, KHÔNG triệt shared-error — *Nine Judges, Two Effective Votes*). Self-refine NeurIPS2023 (**V2 model-KHÁC = external feedback** → thoát phê phán Huang ICLR2024 / Kamoi TACL2024). Constrained = **XGrammar MLSys2025 (peer-reviewed)**; Outlines/OpenAI Structured Outputs/DOMINO-Outlines = artifact.
- **Công cụ preprint (chỉ là "đồ nghề", KHÔNG trình như bình duyệt):** OmniParser (2408.00203), Set-of-Mark (2310.11441), IFEval, Outlines. **SoM không còn là grounding tốt nhất** (Qwen2.5-VL/UGround/OS-Atlas ground thẳng tốt hơn) → đóng khung SoM là "khung chống-bịa", thêm baseline **NATIVE-GROUNDING**.
- **🔧 BỔ SUNG deep-research (BẮT BUỘC, nhất là FAIR):** (a) prior-art sắp-thứ-tự GUI — **GUI Knowledge Bench (arXiv 2510.26098, 10/2025)** đã xáo plan→hỏi thứ tự theo goal+screenshot + **TempVS (2506.10415)** → PHẢI **trích-và-phân-định** (phần khác: N-ảnh-màn-đầy-đủ + hoán-vị-tự-do + gắn-ordering→sinh-tutorial + τ-b partial-order + audit người); (b) **AndroidControl-Curated (arXiv 2510.18488)** phản biện nhãn AndroidControl → ĐỌC trước khi khoá cách chấm DG2; (c) baseline **NATIVE-GROUNDING** + enum **`none/abstain`** (recall-miss → tránh ép bịa); (d) **DG2 LỌC episode** (loại bước `status`/`wait` + loại episode "màn-gần-trùng"; **KN đếm theo N-MÀN-PHÂN-BIỆT-ĐƯỢC**, không theo num_steps thô).
- **🔧 BẪY TOẠ ĐỘ (verify record thật — chi tiết `report/12`):** MobileViews `bounds`=`[[l,t],[r,b]]` lồng + field `width/height` JSON là RÁC (dùng kích thước ẢNH); AndroidControl `gold_action` có tiền tố `!FUNCTIONCALL`, click `(x,y)` pixel 1080×2400; ScreenSpot khác format theo mirror HF → pin 1 mirror + assert.
- **Dữ liệu thật mẫu** (ảnh + JSON raw) ở `dataset_samples/` (đối chiếu nguồn khớp 100%) — dùng làm ví dụ/figure. Khi trích dataset phải **dẫn paper GỐC** (bảng trên), KHÔNG dẫn tên người re-upload HuggingFace.

## 5. Bất biến PHƯƠNG PHÁP theo nhánh (giữ đúng để paper nhất quán luận văn)
**VCL/DG1:** reference-free, neo **VH-silver**; chấm grounding (point-in-bbox) + hallucination (**ALOHa open-vocab CHÍNH**, HER baseline) + clarity (IFEval=format + rubric/G-Eval); **VH chỉ vào lúc CHẤM** (chống rò-rỉ); ablation **thang bậc** C1 (baseline+self-refine) → C3 (constrained + verifier V1) → C4 (intent-critic V2) **+ nhánh NATIVE-GROUNDING (Qwen2.5-VL, không SoM)**; enum có **`none/abstain`**; **so thêm GPT-4o E2E** (chứng minh hệ bám-ảnh tốt hơn viết-tự-do); pilot người ≥60–80; demo tiếng Việt định tính. *Kết quả tốt = thắng baseline + GPT-4o về faithfulness/grounding (claim mức-chắc-thắng).*

**FAIR/DG2:** N ảnh **đã xáo trộn** → model tự xếp → sinh. Headline **τ-b partial-order-aware** — nhãn **"cặp BẮT BUỘC" suy TỪ GOLD trajectory bằng quy tắc tất định** (màn B chỉ xuất hiện sau gold-action ở A ⇒ (A,B) bắt buộc), **KHÔNG từ bộ phát-hiện cue** (chống tự-chấm). **5 ordering cues:** gating · nav-affordance · state-delta · title-progression · drill-down. **Signal-attribution = phân tầng một-cue** (không che pixel). **ordering-gap** = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER). Baseline: **GOAL-ONLY · VISUAL-ONLY · RANDOM-ORDER** (ngưỡng vượt-random = null EMPIRICAL theo từng N). Pre-register: ≥30 episode/mốc N, trục N∈[3,~6] headline (báo thêm tới ~8–10), Holm–Bonferroni. **Cổng cứng:** K1 (tự đo recall bộ dò) · KN (histogram độ dài episode — **đếm theo N-MÀN-PHÂN-BIỆT-ĐƯỢC**, loại bước status/wait) · KB (chống leak step-index: strip metadata + tái mã hoá + che status-bar/đồng-hồ/pin/badge-OS + loại episode 2-ảnh/màn-gần-trùng). **🔧 deep-research:** τ-b partial-order trích **Fagin 2003/2006**; pairwise+Copeland = **PRP-Allpair (NAACL2024)**; **LỌC episode** trước khi đo τ-b; trích-và-phân-định **GUI Knowledge Bench (2510.26098) + TempVS**; đọc **AndroidControl-Curated (2510.18488)** trước khi khoá chấm.

## 6. Khung (structure) gợi ý mỗi bài
**VCL (hội nghị VN, ~6–8 trang, tiếng Việt):** Tóm tắt · 1.Giới thiệu (bài toán + vì sao khó: không có đáp án mẫu) · 2.Liên quan (đánh giá sinh không-tham-chiếu; Chim et al.) · 3.Khung đánh giá đề xuất (3 tiêu chí + neo VH-silver + chống rò-rỉ) · 4.Thiết lập (MobileViews/ScreenSpot, pipeline, thang bậc) · 5.Kết quả (bảng C1/C3/C4 + **nhánh native-grounding** + **so GPT-4o E2E** + recall-conditioned + pilot người) · 6.Demo tiếng Việt · 7.Hạn chế & kết luận. Pre-register ghi rõ. *(Đóng khung: hệ ra kết quả TỐT + phương pháp đánh giá — hai đóng góp.)*

**FAIR (hội nghị, ~8–10 trang, English):** Abstract · 1.Introduction (Screen-Order Inference; **contributions = (i) the ReOrder system + (ii) the evaluation method**) · 2.Related Work (GUI agents; sequence/ordering: Sort-Story[Spearman], Wu 2022, RankGPT, **GUI Knowledge Bench, TempVS** — acknowledge & distinguish prior art; partial-order τ = **Fagin et al.**) · 3.Task & Data (AndroidControl + **AndroidControl-Curated caveat**, shuffle protocol, **episode filtering**, anti-leak KB) · 4.Evaluation Method (partial-order τ-b, anti-circular forced pairs, signal-attribution, ordering-gap, baselines, pre-registration) · 5.Experiments (τ-b vs N, cue attribution, gap) · 6.Discussion/Limitations · 7.Conclusion. Cite VCL as prior work.

## 7. File cần đọc khi viết
- `report/KE_HOACH_2_BAI_BAO.md` — kế hoạch tách + abstract nháp (điểm xuất phát).
- `report/05_final_plan.md` — nguồn-sự-thật phương pháp (khi mâu thuẫn, file này thắng).
- `report/01_metrics.md` — metric + citation chi tiết. `report/02_datasets.md` — dataset + vai.
- `dataset_samples/` (+ `report/_archive/DATASET_ITEM_THAT.md`) — ví dụ/figure dữ liệu thật (cho phần Data/figure).
- `report/12_trial_run_runbook.md` — format dữ liệu THẬT + bẫy toạ độ + lọc episode DG2 (cho phần Data/Method).
- `report/13_pipeline_metric_thi_nghiem_de_hieu.md` — bản dễ hiểu pipeline+metric+thí nghiệm (khung 2-đóng-góp).
- `report/03_pipeline.md` + `report/04_feasibility.md` — pipeline chi tiết + khả thi/kill-test.
- `CLAUDE.md` — bối cảnh tổng + các quyết định CHỐT. *(Bản rescope/luận-chứng/slide cũ ở `report/_archive/` nếu cần.)*

## 8. Cách làm việc
- Trao đổi **tiếng Việt** (bài FAIR nội dung tiếng Anh nhưng thảo luận tiếng Việt).
- Việc lớn (chọn framing, viết related-work, kiểm citation): nên **multi-agent debate / verify** + đối chiếu nguồn thật.
- **Hỏi trước khi chốt** điều chưa rõ (venue CFP, độ dài, deadline, đồng tác giả).
- Sau khi viết/sửa, cập nhật file liên quan; không để 2 bài lệch nhau hay lệch luận văn.

## 9. Checklist trước khi nộp (mỗi bài)
- [ ] Đọc **Call-for-Papers** của venue (chủ đề, độ dài, ngôn ngữ, format, **chính sách trùng-lặp/anonymity**).
- [ ] Headline + đóng góp KHÁC bài kia (đối chiếu bảng §1).
- [ ] FAIR: đã **trích VCL** + nêu delta; phần chung viết lại câu chữ.
- [ ] Mọi citation đã verify venue/năm; preprint ghi rõ; attribution Chim et al. đúng (không "paper của thầy").
- [ ] Không có số liệu bịa; pre-register ghi rõ; "null vẫn đậu" (cho nhánh đánh giá + đo-cơ-chế).
- [ ] Khung **2 đóng góp** (hệ ra kết quả TỐT + eval) nhất quán; có **so baseline + GPT-4o E2E**; **KHÔNG claim SOTA leaderboard**.
- [ ] τ-b partial-order trích **Fagin 2003/2006** (không "tự-định-nghĩa"); pairwise+Copeland = **PRP-Allpair NAACL2024**; **ALOHa** là metric hallucination CHÍNH (HER baseline); **IFEval chỉ Format**; trích-và-phân-định **GUI Knowledge Bench + TempVS**; đã đọc **AndroidControl-Curated**.
- [ ] Figure dữ liệu: dùng ảnh thật `dataset_samples/`; nếu vẽ overlay (bbox) thì **ghi rõ "do tác giả vẽ từ toạ độ, ảnh gốc không có khung"**.
