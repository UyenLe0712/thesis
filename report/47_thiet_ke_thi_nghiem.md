# THIẾT KẾ THÍ NGHIỆM — bản đầy đủ (nguồn-sự-thật cho Chương 13 của report/43)

> Kết quả workflow `wf_c3cf5aa6-510` (2026-07-05, R-10). Neo cỡ mẫu từ R-09 (`RESEARCH_LEDGER`).
> Bản GỌN đã đưa vào `report/43` Chương 13. File này giữ chi tiết + bảng-neo-nguồn đầy đủ cho context sau.

# CHƯƠNG: THIẾT KẾ THÍ NGHIỆM

> Chương này định nghĩa khung câu hỏi nghiên cứu (RQ), bộ thí nghiệm, thứ tự chạy, danh mục bảng/hình, và phân định phạm vi thạc-sĩ vs paper. Mỗi lựa chọn phương pháp luận được neo vào ≥1 nghiên cứu cùng loại đã bình duyệt. Quy ước nội bộ: **DG1 = một màn**, **DG2 = nhiều màn** (trong luận văn viết "một màn / nhiều màn"). Nguyên tắc xuyên suốt: (i) mọi con số kèm CI bootstrap 95% cluster-by-app; (ii) so-sánh 2 hệ dùng paired test trên cùng mẫu; (iii) pre-register ngưỡng TRƯỚC khi nhìn kết quả (commit `report/22`); (iv) KHÔNG claim SOTA leaderboard; (v) human-correlation là future-work, KHÔNG phải cổng đậu/rớt.

---

## 1. KHUNG RESEARCH QUESTIONS

Phần thực nghiệm tổ chức quanh 6 RQ tường minh; mỗi RQ ứng với một cụm bảng/hình (khung RQ chuẩn của paper đề-xuất-eval, thường 3–6 RQ mỗi cụm một bảng — *Zheng et al., NeurIPS 2023 D&B*). Ba RQ đầu phục vụ đóng góp (A) hệ thống + (B) phương pháp đánh giá ở nhánh một màn; ba RQ sau phục vụ nhánh nhiều màn và đối chứng.

**RQ1 — Đo hiện tượng (đóng góp A, phần "phát hiện thực nghiệm").**
VLM sinh-mù (chỉ thấy ảnh + câu hỏi, không thấy danh sách nút) tham chiếu tới nút KHÔNG tồn tại trên màn với tần suất bao nhiêu, và tần suất đó biến thiên thế nào GIỮA các model? → Báo tỉ-lệ-bịa dạng **đường-cong per-model**, không headline "¼" tĩnh.
*Vì sao là RQ độc lập:* đây là bằng chứng cho "vấn đề có thật, đo được", nền để RQ2 chứng minh lớp kiểm giúp ích. (multi-model curve: *FaithScore EMNLP24 Findings*, *SelfCheckGPT EMNLP23*, *FActScore EMNLP23*).

**RQ2 — Lớp trung-thực-hoá có giúp ích không, và giá bao nhiêu? (đóng góp A, lõi).**
Trên CÙNG một generator, lớp đối chiếu View-Hierarchy (BASE → BASE+kiểm) có làm giảm tham-chiếu-nút-không-tồn-tại không (before/after ở mọi τ), giá phải trả = %fallback bao nhiêu, và có gây hại chỉ số phụ (label-fidelity, format) không?
*Neo:* báo before/after trên cùng generator + một chỉ số bảo-toàn để lộ trade-off (*RARR ACL23* F1_AP = attribution × preservation); ta đọc %fallback là "preservation cost". Phân rã theo đơn-vị-bước, không mức toàn-đoạn (*FaithScore*).

**RQ2b (bên trong RQ2) — Đối-chứng-thất-bại đo được (chân biến A thành research).**
Nhánh "chỉ mô tả bằng lời" (fallback độc lập) so với nhánh đối-chứng "đoán nút gần nhất trong VH": nhánh đoán tạo bao nhiêu **silent-error** (bịa được gán tên thật, không phát hiện được)?
*Neo:* verify factored KHÔNG cho model nhìn lại câu trả lời gốc để tránh copy ảo giác (*CoVe Findings ACL24*); self-correction không có phản hồi ngoài có thể LÀM GIẢM độ chính xác (*"LLMs Cannot Self-Correct Reasoning Yet", ICLR 2024*). Đây là lý do chốt "chỉ mô tả".

**RQ3 — Phương pháp đánh giá no-gold có HỢP LỆ không? (đóng góp B, lõi).**
Metric không-đáp-án-mẫu có (a) nhạy với lỗi đã-biết (perturbation), (b) tách được bản-lỗi khỏi bản-đúng (minimal pairs), (c) không tự-chấm vòng tròn (anti-circularity), (d) khớp phán đoán người ở mức tối thiểu?
*Neo:* perturbation checklist là trục validate chính (*Sai EMNLP21*, *CheckList Ribeiro ACL20 Best Paper*); minimal-pair discriminability vs consistency tách riêng (*BUMP ACL23*); judge phải khác họ generator vì self-preference (*Panickssery NeurIPS24*); human-correlation là điều-kiện-cần chứ không phải bằng chứng validity đủ (*Clark ACL-IJCNLP21*).

**RQ4 — Hệ sắp thứ tự màn có đúng không? (đóng góp A, nhiều màn).**
Stage-0 (pairwise→Copeland→min-FAS) có khôi phục thứ tự N ảnh đã xáo trộn tốt hơn sàn (random) và tốt hơn/khác baseline listwise-một-shot không (chấm cùng τ/pairwise-acc/PMR/position-acc), chi phí thế nào, và từng khối (Copeland, min-FAS, chống position-bias) đóng góp bao nhiêu?
*Neo:* random-floor bắt buộc (*Sort-Story EMNLP16*); bộ metric permutation-recovery đa-góc (*Wu et al. NAACL/ACL22*, τ theo *Lapata CL06*); baseline listwise + trục chi-phí (*RankGPT EMNLP23*, *Qin PRP NAACL24*).

**RQ5 — Năng-lực-từng-bước thật là bao nhiêu? (điều kiện giữ "A ngang B").**
Trên chuỗi đã sắp, Step-SR teacher-forced (bước đúng loại thao tác VÀ sai lệch ≤14%) có ra số dương thật không?
*Neo:* ngưỡng 14% từ *AITW NeurIPS23*; Step-SR khung *AndroidControl NeurIPS24 D&B*. Đây là số quyết định trọng lượng đóng góp A (CLAUDE §2: "ngang nhau CÓ ĐIỀU KIỆN — chờ DG2 dương").

**RQ6 — Grounding đối chứng.**
Bộ trỏ độc lập dự đoán (x,y) từ tên+ảnh rơi trong khung nút với dung sai 14% ở tỉ lệ bao nhiêu (tách text/icon), so với đường tham chiếu ScreenSpot-v2?
*Neo:* point-in-bbox có dung sai, tách text/icon (*SeeClick ACL24*); (x,y) từ bộ trỏ ĐỘC LẬP, KHÔNG lấy tâm bbox đã khớp (tránh tautology 100%) — RQ6 nằm NGOÀI headline một-màn (CLAUDE M1).

---

## 2. BẢNG THÍ NGHIỆM TỔNG

> Bảng đọc ngang; nếu cần cuộn ngang trong bản in thì đặt landscape. Cột "Cổng" = kill-test phải GO trước khi con số được coi hợp lệ.

| # | RQ | Thí nghiệm | Dataset + cỡ mẫu | Metric | Baseline / Ablation | Thống kê | Cổng | Kỳ vọng | Caveat trung thực |
|---|---|---|---|---|---|---|---|---|---|
| E1 | RQ1 | Đo tỉ-lệ-bịa THÔ của VLM sinh-mù, **đường-cong per-model** | MobileViews ~150 màn/30+ app; ≥2 model (gpt-4o-mini + ≥1 frontier rẻ 2025-26: Gemini-2.5-Flash / GPT-4.1-mini) | faithfulness = 1−bịa/bước-nhắc-nút (ALOHa-style, per-step) | so GIỮA model (curve); không baseline nội bộ | CI95% cluster-boot-by-app, 10k | K1 (recall detector), M4 (độ-phủ-nhãn VH) | frontier vẫn bịa > 0 (đường-cong, không hội tụ 0) | báo "CÓ ĐIỀU KIỆN recall-VH"; loại nút icon-only/nhãn-chung khỏi mẫu số; exploratory |
| E2 | RQ2 | Toggle lớp đối chiếu: BASE vs BASE+kiểm, **cùng generator**, quét nhiều τ | MobileViews 81 màn/17 app (bản chính) + mở rộng 150 nếu ngân sách | faithfulness before/after + **%fallback** + no-harm (label-fidelity, format) | ablation on/off lớp VH; quét τ∈{...} | paired: approx-randomization (chính) + paired-bootstrap (phụ); Holm đa-τ; wild-cluster-t (G≈17) | M4; pre-reg τ | faithfulness ↑ mọi τ; %fallback ~19%; label/format đứng yên | báo cặp (↑, %fallback) song song, KHÔNG khoe ~100% trơ trọi; CI có thể chạm 0 ở n nhỏ |
| E3 | RQ2b | **Đối-chứng-thất-bại:** "chỉ mô tả" (fallback) vs "đoán nút gần nhất" (nhìn VH gán tên) | cùng E2 | silent-error-rate (bịa được gán tên thật, matcher-independent kiểm) | ablation 2 nhánh xử-lý-bước-bịa | paired-bootstrap CI của hiệu | — | nhánh đoán tạo silent-error đo được > 0 | đây là bằng chứng "A là research" — báo số cụ thể, không định tính |
| E4 | RQ3a | **Perturbation harness:** bơm 10–15 loại lỗi ĐỘC-LẬP-matcher × ≥30 mẫu/loại | MobileViews subset + bản sinh; lỗi: phủ định, đổi tên nút, thêm nút bịa, bỏ bước, xáo thứ tự, đổi thao tác... | detection-rate + false-positive-rate (cặp sạch) + monotonicity (điểm tụt đơn-điệu theo mức lỗi); AUC-PR mức bước | breakdown per-error-type (KHÔNG gộp) | CI95% per-type; Holm | — | metric tụt đúng hướng; FP thấp; đơn-điệu | discriminability ≠ consistency → báo cả hai (BUMP); đây là "độ nhạy", chưa phải convergent validity |
| E5 | RQ3b | **Validate matcher** vs người | 80–120 cặp gán-tay (khớp nút / bịa) | Precision / Recall + Cohen's κ; freeze τA sau đó | so matcher nomic τA | báo P/R + κ; error-rate bản tự-động vs người | — | P≥0.95; κ khá | ALOHa/FActScore-style; freeze τ TRƯỚC khi chạy chính |
| E6 | RQ3c | **Anti-circularity:** 3 cơ chế chấm độc lập | trên bản sinh E2 | mức đồng-thuận giữa bge-m3 (khác họ) + LLM-judge khác-họ + token-overlap; quyết matched/fallback = nomic | so 3 cơ chế; judge KHÁC GPT-family | agreement + CI | — | 3 cơ chế đồng thuận cao | quyết-định (nomic) tách khỏi chấm (bge-m3); judge không GPT vì generator là gpt-4o-mini |
| E7 | RQ3d | **Neo-người cho LLM-judge** | 100–200 cặp | κ / tương-quan judge vs người | — | κ; KHÔNG dùng làm cổng | — | κ đủ để "điều-kiện-cần" | human-correlation = future-work, KHÔNG cổng đậu/rớt (Clark) |
| E8 | RQ4a | **Sàn + đối kiến:** Random-shuffle vs Pairwise+Copeland (ta) vs Listwise-1-shot | AndroidControl ~500 episode, ≥30/mốc-N; xáo trộn, gold verify | τ(partial, Fagin) + pairwise-acc + PMR + position-acc + **cột chi-phí** (call LLM, O(n²)/O(n log n)/O(n)) | 3 hệ chấm cùng metric | paired vs random & vs listwise; Holm đa-metric; cluster-by-app | KN (histogram N), KZ' (prior-art, GO), K-pair, KB (chống leak) | ta > random; ≈/> listwise với chi-phí giải thích được | τ partial CHỈ phạt cặp bắt-buộc suy từ gold nhân-quả; KHÔNG NDCG (khác họ ranking-by-relevance) |
| E9 | RQ4b | **Cổng K-pair:** acc-pairwise THÔ của VLM vs gold TRƯỚC tổng hợp | cùng E8 | accuracy-pairwise thô | sàn 0.5 | CI | **K-pair** | > 0.5 | nếu ≈0.5 → Copeland vô hiệu, KHAI THẲNG, Stage-0 không claim |
| E10 | RQ4c | **Ablation tổng-hợp:** Copeland-allpair vs Borda vs bản rẻ (sorting/sliding) | cùng E8 | τ/PMR + chi-phí | ablation luật tổng hợp | paired | — | Copeland biện minh được | PRP-Allpair dùng chính Copeland (Qin) — nền peer-reviewed |
| E11 | RQ4d | **Ablation phá-vòng:** min-FAS vs luật ngây-thơ (cắt cạnh yếu) | cùng E8 | intransitivity-rate + τ/PMR | ablation khối min-FAS | paired | — | min-FAS ≥ ngây-thơ | báo tỉ-lệ episode có vòng; quy công cho min-FAS thay vì hộp-đen |
| E12 | RQ4e | **Chống position-bias:** permutation self-consistency / A\|B vs B\|A | cùng E8 | mức cải thiện τ; aggregate min-Kendall-τ | ablation self-consistency | paired | — | cải thiện đo được | hậu thuẫn "KHÔNG dùng confidence VLM tự-khai" (calibrate kém) |
| E13 | RQ4f | **Cue analysis:** stratification 1-cue (giữ cặp phân biệt bởi đúng 1/5 cue) | cùng E8, phân tầng | pairwise-acc per-cue (gating/nav/state-delta/title/drill-down) | phân tầng, KHÔNG che-pixel KHÔNG tin model tự-khai | CI per-cue | — | mỗi cue có tín hiệu | Made-to-Order CVPR24 làm nền phương pháp gỡ-neo-tín-hiệu |
| E14 | RQ5 | **Step-SR** teacher-forced trên chuỗi đã sắp | AndroidControl, ≥30/mốc-N | Step-SR = bước-đúng/bước-gold (đúng loại thao tác ∧ ≤14%) | phân tầng theo N | CI cluster-by-app; Holm | KB | số DƯƠNG thật | quyết định "A ngang B"; trục tham chiếu chuẩn ngành, KHÔNG claim leaderboard |
| E15 | RQ6 | **Grounding đối chứng**, (x,y) từ bộ trỏ ĐỘC LẬP | ScreenSpot-v2 502 mobile (+ MobileViews có bbox) | point-in-bbox @14%, tách text/icon | so đường tham chiếu ScreenSpot | CI | (hiệu chỉnh khung toạ-độ MobileViews) | trong khung tài liệu | KHÔNG lấy tâm bbox đã khớp (tautology); NGOÀI headline một-màn (M1) |

**Ghi chú thống kê chung (áp cho mọi dòng):** paired significance ưu tiên **approximate-randomization** (bảo thủ hơn bootstrap về Type-I — *Berg-Kirkpatrick EMNLP12*), phụ **paired-bootstrap 10k** (dùng được cả test nhỏ — *Koehn EMNLP04*); vì G≈17 app dùng **wild-cluster-bootstrap-t** + khai caveat under-coverage (*Cameron-Gelbach-Miller 2008*); đa-metric/đa-mốc-N hiệu chỉnh **Holm** (*Holm 1979*); nêu **tên test cho từng metric + lý do** (*Dror et al. ACL18*); khai **power/MDE**, kết quả không đạt ý nghĩa trình bày như **null/underpowered hợp lệ** — "absence of evidence ≠ evidence of absence", KHÔNG kết luận "bằng nhau" (*Card et al. EMNLP20*); nhấn **effect size + CI**, CI chồng nhau diễn giải thận trọng (*Berrada preprint, bổ trợ*); so **baseline mạnh**, KHÔNG kết luận SOTA từ một tập/một model (*Marie et al. ACL21*).

---

## 3. THỨ TỰ CHẠY (free trước → API sau; cổng chặn gì)

**Giai đoạn 0 — Pre-register (free, làm TRƯỚC mọi thứ).**
`git init` + commit `report/22` (ngưỡng đậu/rớt, seed, số resample, τ dự kiến) TRƯỚC khi nhìn kết quả. *Repo hiện đã là git — chỉ cần commit mốc pre-reg.* (chuẩn pre-register — *Berrada*; timestamp = CLAUDE M3.)

**Giai đoạn 1 — Cổng cứng free (không tốn API, chặn toàn bộ nhánh tương ứng).**
- **K1** (đo recall của detector VH) → chặn E1, E2 (nếu recall thấp, tỉ-lệ-bịa vô nghĩa).
- **M4** `dg1_vh_coverage.py` tính độ-phủ-nhãn VH → chặn cách BÁO E1/E2 (khoảng "có điều kiện recall-VH").
- **KN** (histogram độ dài episode) → chặn phân-tầng-N của E8/E14. *(đã GO)*
- **KZ'** (prior-art sắp-ảnh) → *(đã GO)*.
- **KB** (chống leak step-index: strip metadata + tái mã hoá ảnh + che status bar/đồng hồ/pin/badge + loại episode 2-ảnh trùng-pixel) → chặn E8/E14.
- Dựng **perturbation harness** (E4) + tập **gán-tay 80–120 cặp** (E5) + module **LLM-judge khác-họ** (E6/E7) — đều free/local (Ollama bge-m3, nomic).

**Giai đoạn 2 — API tối thiểu, có kiểm soát chi phí (mỗi bước ✱ HỎI USER TRƯỚC).**
Thứ tự: (a) sinh câu hỏi affordance-seeded + cổng answerability → (b) sinh BASE 81 (→150) màn E1/E2 → (c) sinh nhánh PA2 + nhánh đối-chứng "đoán nút" E3 → (d) **K-pair** E9 (sàn 0.5) — nếu FAIL thì DỪNG nhánh Stage-0, khai thẳng → (e) nếu K-pair GO: E8/E10/E11/E12/E13 Stage-0 → (f) E14 Step-SR → (g) E15 grounding (bộ trỏ độc lập).
*Nguyên tắc chi tiền (user): chạy MỘT lần cho đúng, ưu tiên local/free + cache, resume theo tag.*

**Cổng chặn cái gì — tóm tắt:** K1→E1/E2 · M4→cách báo E1/E2 · KN→phân-tầng E8/E14 · KB→E8/E14 · **K-pair→toàn bộ Stage-0 (E8–E13)**. Nếu K-pair fail, nhánh nhiều-màn chuyển thành "phát hiện âm tính hợp lệ" chứ không bỏ.

---

## 4. DANH SÁCH BẢNG / HÌNH TRONG LUẬN VĂN

**Bảng.**
- **Table 1** — Đặc tả 3 dataset (nguồn/venue/quy mô/giấy phép/cấu trúc/vai). *(report/44)*
- **Table 2** — Tỉ-lệ-bịa THÔ per-model, "có điều kiện recall-VH" (E1). *(FaithScore multi-model)*
- **Table 3** — Hiệu quả lớp trung-thực-hoá: faithfulness before/after × nhiều τ + %fallback + no-harm (label-fidelity, format) + CI95% cluster-boot (E2). *(RARR F1_AP)*
- **Table 4** — Đối-chứng-thất-bại: silent-error "đoán nút" vs "chỉ mô tả" (E3). *(CoVe / ICLR24)*
- **Table 5** — Validate metric: perturbation 10–15 loại × detection/FP/monotonicity, breakdown per-error-type (E4). *(Sai EMNLP21 / BUMP)*
- **Table 6** — Validate matcher: P/R + Cohen κ trên 80–120 cặp, τ freeze (E5). *(ALOHa / FActScore)*
- **Table 7** — Anti-circularity: đồng-thuận 3 cơ chế chấm độc lập (E6). *(SelfCheckGPT / Panickssery)*
- **Table 8** — Sắp thứ tự theo mốc-N: τ(partial)+pairwise-acc+PMR+position-acc, 3 hệ (random/pairwise-Copeland/listwise) + cột chi-phí (E8). *(Sort-Story / Wu / RankGPT)*
- **Table 9** — Ablation Stage-0: tổng-hợp (Copeland/Borda/rẻ) + phá-vòng (min-FAS/ngây-thơ) + position-bias (E10–E12). *(Qin PRP / Tang)*
- **Table 10** — Cue analysis: pairwise-acc per-cue (E13). *(Made-to-Order)*
- **Table 11** — Step-SR teacher-forced theo mốc-N (E14). *(AndroidControl / AITW)*
- **Table 12** — Grounding đối chứng ScreenSpot-v2, tách text/icon (E15). *(SeeClick)*

**Hình.**
- **Figure 1** — Sơ đồ pipeline (3 hộp một-màn + Stage-0 nhiều-màn, input router).
- **Figure 2** — Đường-cong tỉ-lệ-bịa per-model (trục model × faithfulness) (E1).
- **Figure 3** — Trade-off curve: faithfulness ↑ vs %fallback theo τ (E2). *(RARR trade-off)*
- **Figure 4** — Perturbation: monotonicity điểm-tụt theo mức lỗi, per-error-type (E4).
- **Figure 5** — τ theo N (độ khó tăng theo C(n,2)), 3 hệ (E8). *("Is Everything in Order" EMNLP21 — báo theo length)*
- **Figure 6** — Intransitivity-rate + hiệu quả min-FAS theo N (E11).
- **Figure 7** — Bar per-cue pairwise-acc (E13).
- **Figure 8** — Ví dụ định tính đầu-cuối: 1 màn bịa → fallback mô tả; 1 episode xáo → sắp lại (minh hoạ, không thay số).

---

## 5. PHÂN ĐỊNH THẠC-SĨ vs PAPER

Luận văn thạc-sĩ ĐƯỢC nhẹ hơn paper hội nghị: ít model/baseline hơn, cỡ mẫu khiêm tốn (median ~100 sample chấp nhận được trong eval), miễn khai rõ "exploratory" + giới hạn + pre-register; đổi lại phải định nghĩa/giải thích metric kỹ hơn (*Gehrmann/GEM, preprint — bổ trợ*; khung RQ *Zheng NeurIPS23*).

**BẮT BUỘC cho thạc-sĩ (không thể thiếu — mỗi cái là một chân đóng góp):**
1. **E2** (toggle lớp trung-thực-hoá before/after + %fallback + no-harm) — lõi đóng góp A.
2. **E3** (đối-chứng-thất-bại silent-error) — chân biến A thành research, KHÔNG chỉ engineering.
3. **E1** với **≥2 model** (gpt-4o-mini + ≥1 frontier rẻ) — vá đòn "neo 1 model đời-2024"; đường-cong, không headline tĩnh.
4. **E4** (perturbation harness) — trục validate CHÍNH của đóng góp B (thay human-correlation).
5. **E5** (validate matcher P/R+κ, freeze τ) — điều kiện để mọi con số faithfulness hợp lệ.
6. **E6** (anti-circularity ≥3 cơ chế) — chống tự-chấm, đã từng là blocker circularity.
7. **E8 + E9** (sắp thứ tự theo N + baseline random/listwise + **K-pair**) và **E14** (Step-SR) — điều kiện giữ "A ngang B CÓ ĐIỀU KIỆN". *Nếu K-pair fail → E8/E14 chuyển thành phát-hiện-âm-tính hợp lệ, vẫn nộp.*
8. Toàn bộ khung thống kê (CI bootstrap, paired test, Holm, wild-cluster-t, pre-register, khai power).

**NẾU CÒN THỜI GIAN / NGÂN SÁCH (nice-to-have):**
- **E7** neo-người LLM-judge 100–200 cặp — chỉ điều-kiện-cần, đã đóng khung future-work.
- Mở rộng MobileViews 81 → 150 màn/30+ app.
- **E10–E13** đầy đủ (ablation tổng-hợp/phá-vòng/position-bias/cue) — bản tối thiểu chỉ cần E8+E11; E10/E12/E13 làm sâu thêm quy-công-thành-phần.
- **E15** grounding ScreenSpot đối chứng — bù credibility, KHÔNG trong headline.
- Model thứ 3 (Qwen mở) cho trục "đóng vs mở".
- Human-correlation mở rộng, demo tiếng Việt định tính (~120 mẫu app VN — KHÔNG có bảng số VN định lượng, nói rõ với thầy).

**Ranh giới liêm chính (áp cả hai mức):** so baseline mạnh, không kết luận SOTA từ một tập/một model, luôn kèm significance (*Marie ACL21*, *Berg-Kirkpatrick EMNLP12*); khai "exploratory / mẫu nhỏ / 1-năm-app"; báo tỉ-lệ-bịa dạng khoảng/đường-cong, KHÔNG điểm tĩnh khi underpowered (*Card EMNLP20*).

---

## 6. BẢNG NEO NGUỒN (mỗi lựa chọn → 1 paper cùng loại)

| Lựa chọn phương pháp | Nguồn neo | Peer-reviewed |
|---|---|---|
| Before/after cùng generator + preservation lộ trade-off (F1_AP) → %fallback | RARR, ACL 2023 | ✔ |
| Factored KHÔNG nhìn lại + đo regression sửa-bậy → "chỉ mô tả" | CoVe, Findings ACL 2024 | ✔ |
| Self-correction không phản hồi ngoài làm GIẢM accuracy → silent-error đo bằng số | LLMs Cannot Self-Correct Reasoning Yet, ICLR 2024 | ✔ |
| Localization accuracy + validate matcher P/R vs người; faithfulness by matching | ALOHa, NAACL 2024 | ✔ |
| Atomic-fact per-unit + đánh giá nhiều model (per-model curve) | FaithScore, Findings EMNLP 2024 | ✔ |
| Estimator tự-động validate vs người, error-rate thấp, freeze ngưỡng | FActScore, EMNLP 2023 | ✔ |
| ≥3 cơ chế độc lập + AUC-PR detection + independent samples | SelfCheckGPT, EMNLP 2023 | ✔ |
| Perturbation checklist = trục validate metric chính (detection/FP/monotonicity) | Sai et al., EMNLP 2021 | ✔ |
| Minimal-pair: discriminability RIÊNG per-error-type ≠ consistency | BUMP, ACL 2023 | ✔ |
| Behavioral testing MFT/INV/DIR, báo failure-rate per-capability | CheckList (Ribeiro), ACL 2020 Best Paper | ✔ |
| Judge KHÁC HỌ generator (self-preference đo được, không giả định trung lập) | Panickssery et al., NeurIPS 2024 | ✔ |
| Human-correlation KHÔNG là cổng đậu/rớt (điều-kiện-cần) | Clark et al., ACL-IJCNLP 2021 | ✔ |
| Giảm ~80% nhãn-người → justify 80–200 cặp | Active Evaluation, ACL 2022 Best Paper | ✔ |
| Random-floor (τ≈0, pairwise≈0.5) làm mốc delta | Sort-Story, EMNLP 2016 | ✔ |
| Bộ metric permutation-recovery (τ/pairwise/PMR/position) | Wu et al., NAACL/ACL 2022 | ✔ |
| Định nghĩa τ (số nghịch-thế chuẩn hoá) | Lapata, CL 32(4) 2006 | ✔ |
| τ partial-order chỉ phạt cặp bắt-buộc | Fagin et al., SIAM 2006 | ✔ |
| Baseline listwise-1-shot + trục chi-phí | RankGPT, EMNLP 2023 Outstanding | ✔ |
| Pairwise Copeland-allpair O(n²) + biến-thể rẻ | Qin et al. (PRP), Findings NAACL 2024 | ✔ |
| Chống position-bias = permutation self-consistency / A\|B vs B\|A | Tang et al., NAACL 2024 | ✔ |
| Topological-sort-from-pairwise + min-FAS khi có vòng | Constraint graphs, AAAI 2021 (+ FAS-tournament) | ✔ |
| Cue/signal ablation gỡ-neo (không tin model tự-khai) | Made to Order, CVPR 2024 | ✔ |
| Phân-tầng theo N (độ khó ~C(n,2)) | Is Everything in Order?, EMNLP 2021 | ✔ |
| KHÔNG NDCG (task ta = permutation-recovery, khác ranking-by-relevance) | Qin PRP (đối chiếu miền), NAACL 2024 | ✔ |
| Khung RQ + meta-eval (τ hệ-thống, κ cặp) | Zheng et al., NeurIPS 2023 D&B | ✔ |
| Paired-bootstrap dùng được test nhỏ (~300) | Koehn, EMNLP 2004 | ✔ |
| Approx-randomization ưu tiên (bootstrap kém bảo thủ, kiểm generalize) | Berg-Kirkpatrick et al., EMNLP 2012 | ✔ |
| Protocol chọn/khai test cho từng metric | Dror et al., ACL 2018 | ✔ |
| Khai power/MDE + null-result hợp lệ | Card et al., EMNLP 2020 | ✔ |
| Wild-cluster-bootstrap-t khi G nhỏ (5–30) | Cameron-Gelbach-Miller, REStat 2008 | ✔ |
| Holm step-down đa-so-sánh | Holm, Scand. J. Stat. 1979 | ✔ |
| Grounding point-in-bbox có dung sai, tách text/icon | SeeClick, ACL 2024 | ✔ |
| Dung sai 14% | AITW, NeurIPS 2023 | ✔ |
| Step-SR khung + AndroidControl gold | Li et al. (AndroidControl), NeurIPS 2024 D&B | ✔ |
| So baseline mạnh, không SOTA từ 1 tập/1 model | Marie et al., ACL 2021 | ✔ |
| Thesis nhẹ hơn paper (ít model/baseline, mẫu khiêm tốn) | Gehrmann et al. (GEM), preprint — **bổ trợ** | ✘ |
| CI + effect-size + pre-register nhấn mạnh | Berrada et al., preprint — **bổ trợ** | ✘ |
| ScreenSpot-Pro ablation gỡ-từng-khối (minh hoạ cách trình bày) | Li et al., preprint — **bổ trợ** | ✘ |

Ba nguồn cuối là preprint → chỉ dùng bổ trợ định-dạng-trình-bày, KHÔNG làm trụ phương pháp. Toàn bộ trụ (E1–E15 + thống kê) đều neo peer-reviewed.

---

**Kết luận chương:** bộ 15 thí nghiệm (E1–E15) trên 6 RQ phủ đủ: đo bịa baseline vs sau-lớp-kiểm + %fallback (E1–E2); ablation silent-error (E3); đường-cong per-model ≥1 frontier (E1); perturbation 4 tiêu chí (E4); anti-circularity + validate matcher (E5–E7); τ partial + listwise vs pairwise + ablation phá-vòng/position-bias/tổng-hợp (E8–E12); cue 1-cue (E13); Step-SR (E14); grounding ScreenSpot đối chứng (E15). Mọi con số kèm CI cluster-bootstrap-by-app + paired test + Holm + wild-cluster-t (G≈17) + pre-register; human-correlation dời future-work; KHÔNG claim SOTA. Điều kiện then chốt giữ "hai đóng góp ngang nhau" = **K-pair GO + Step-SR/τ dương thật (E9/E14)**; nếu âm, khai thẳng như phát-hiện hợp lệ, KHÔNG che.