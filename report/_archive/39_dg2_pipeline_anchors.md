# 🧭 Nền peer-reviewed cho pipeline DG2 (suy luận trật tự màn) — verify 2026-07-02

> **Mục đích:** neo mỗi thành phần của Stage-0 (sắp thứ tự màn) vào một nguồn ĐÃ BÌNH DUYỆT, để nhánh
> nhiều màn vững ngang nhánh đánh giá. Nguồn: deep-research `wf_72b00dd2` (6 agent WebSearch/WebFetch,
> xác minh venue qua ACL Anthology / ACM DL / DBLP / epubs.siam.org).
> **Kết quả: cả 6 thành phần PEER_REVIEWED_CONFIRMED** (5 trụ chính-danh đúng bài toán + 1 trụ khái niệm).

## 1. Bảng thành phần → trụ đã xác minh → cite-as

| Thành phần Stage-0 | Trụ (venue + năm) | Cite-as | Trạng thái |
|---|---|---|---|
| (a) Hỏi VLM từng CẶP "màn nào trước?" (pairwise) | **Findings of NAACL 2024**, pp. 1504–1518 | Qin et al. (2024), *LLMs are Effective Text Rankers with Pairwise Ranking Prompting*, Findings of NAACL 2024 | ✅ trụ chính |
| (b) Tổng hợp cặp → thứ tự toàn cục bằng **Copeland** | **WWW 2001** (ACM), pp. 613–622 | Dwork, Kumar, Naor & Sivakumar (2001), *Rank Aggregation Methods for the Web*, WWW 2001 | ✅ trụ chính |
| (c) Phá vòng mâu thuẫn (**min feedback arc set**) | **J. ACM 55(5), 2008** (prelim. STOC 2005) | Ailon, Charikar & Newman (2008), *Aggregating Inconsistent Information: Ranking and Clustering*, J. ACM 55(5) | ✅ trụ chính |
| (tiền lệ TÁC VỤ) xáo ảnh → sắp lại | **EMNLP 2016**, pp. 925–931 | Agrawal et al. (2016), *Sort Story: Sorting Jumbled Images and Captions into Stories*, EMNLP 2016 | ✅ trụ chính |
| (d) Chấm **τ thứ-tự-bộ-phận** (chỉ phạt cặp bắt buộc) | **SIAM J. Discrete Math. 20(3), 2006** (prelim. PODS 2004) | Fagin, Kumar, Mahdian, Sivakumar & Vee (2006), *Comparing Partial Rankings*, SIAM J. Discrete Math. 20(3):628–648 | ✅ trụ chính |
| (d') tiền lệ dùng τ làm headline ordering | **Computational Linguistics 32(4), 2006** | Lapata (2006), *Automatic Evaluation of Information Ordering: Kendall's Tau*, Comput. Linguist. 32(4):471–484 | ✅ trụ chính |
| (e) Phân tích cue bằng **stratification một-cue** | **Findings of EMNLP 2020**, pp. 1307–1323 | Gardner et al. (2020), *Evaluating Models' Local Decision Boundaries via Contrast Sets*, Findings of EMNLP 2020 | ⚠️ trụ KHÁI NIỆM |

- **Đối chứng listwise (tùy chọn):** Sun et al. (2023), *Is ChatGPT Good at Search?* (RankGPT), **EMNLP 2023** (Outstanding Paper), pp. 14918–14937.
- **Bổ trợ (e):** Ribeiro et al. (2020), *CheckList*, **ACL 2020** (Best Paper) — khung isolate-one-capability.
- **Bổ trợ (b):** Saari & Merlin (1996), *The Copeland method*, Economic Theory 8:51–76 (tính chất Copeland nếu cần lý thuyết).

## 2. Caveat ADAPT sang miền GUI (phải khai khi viết)

- **(a) Qin NAACL24:** gốc xếp *đoạn văn theo độ-liên-quan truy vấn (IR)*; ta xếp *màn GUI theo quan-hệ-thời-gian/nhân-quả*. → adaptation kỹ thuật prompting, KHÔNG cùng bài toán. Chi phí O(N²)=C(N,2) khớp trần N≤6.
- **(b) Copeland/Dwork WWW01 & (c) Ailon JACM08:** thuật toán tổng-hợp-hạng thuần, **độc lập miền** — chỉ input cặp là từ VLM/GUI; không cần adapt. Copeland gốc A.H. Copeland 1951 = tài liệu lịch sử chưa-xuất-bản → dùng Dwork 2001 làm trụ-dùng.
- **(Sort Story EMNLP16):** kiến trúc unary+pairwise→ensemble TRÙNG Stage-0, nhưng gốc là *ảnh đời thường + caption*; ta là *màn phần mềm KHÔNG caption*, suy từ pixel/cue, và **có goal điều-kiện-hoá**. Sort Story chấm Spearman thô; ta dùng τ bộ-phận.
- **(d) Fagin SIAM06:** gốc so ordering câu; **|M| = số cặp BẮT BUỘC suy từ gold trajectory** là định nghĩa riêng của luận văn, không phải công thức nguyên bản. **Dùng từ:** "τ thứ-tự-bộ-phận (partial-order-aware, Fagin 2006)", **KHÔNG gọi "Kendall τ-b"**.
- **(e) Gardner EMNLP20:** trụ KHÁI NIỆM — KHÔNG có bài trùng khít "stratification một-cue trên trật-tự-màn". Gardner *perturb* dữ liệu đổi gold label; ta KHÔNG perturb ảnh mà **stratify tập cặp quan sát sẵn** (observational, không can thiệp). → trình như "controlled comparison lấy cảm hứng từ contrast sets", không áp y nguyên. (Chọn stratify thay che-pixel còn tự có biện minh: che pixel tạo artifact out-of-distribution.)

## 3. Phán quyết + độ mới

**ĐỦ nền peer-reviewed để bảo vệ.** 5/6 thành phần lõi có trụ chính-danh đúng bài toán (đã xác minh venue + quote). Thành phần (e) chỉ có trụ khái niệm → **đó là chỗ đóng-góp-mới, không phải lỗ hổng** (trình như quyết định thiết kế được prior-art hậu thuẫn, KHÔNG over-claim là chuẩn có sẵn).

**Độ mới (chống "chỉ ghép đồ có sẵn") — tổ hợp + 5 khác biệt đo được:**
1. **Miền GUI/screen-flow** (không phải text ranking / story photos / ordering câu).
2. **Goal-conditioned ordering** — thứ tự phụ thuộc mục tiêu người dùng (các trụ đều không có goal).
3. **Gắn ordering → SINH HƯỚNG DẪN** (các trụ dừng ở "ra thứ tự"; ta nối vào pipeline sinh tutorial).
4. **τ thứ-tự-BỘ-PHẬN từ GOLD** — chỉ phạt cặp nhân-quả, cặp tự-do đảo vẫn đúng (mịn hơn Spearman thô).
5. **Signal-attribution theo 5 cue** bằng stratification một-cue — không tiền lệ nào làm cho screen-flow.

> Đóng khung an toàn: *"Không phát minh pairwise/Copeland/FAS/τ; là bài ĐẦU TIÊN ráp chúng thành hệ goal-conditioned screen-ordering → tutorial trên GUI, với chấm partial-order từ gold + phân tích cue."*

## 4. Cảnh báo trung thực (đừng tái phạm khi viết)

- **Copeland quote (Dwork 2001):** wording lấy qua WebSearch bề mặt (PDF gốc + ACM DL fetch fail/403) → **đối chiếu lại wording trên bản PDF chính thức trước khi in**. Venue đã chắc.
- **"τ thứ-tự-bộ-phận (Fagin)" ≠ "Kendall τ-b"** — τ-b xử lý ties trong bảng chéo tương quan, KHÁC khái niệm partial-ranking metric.
- **Screen-flow (arXiv 2503.06067) = PREPRINT** — không xác minh được đã nhận hội nghị → chỉ để related work, KHÔNG trình như đã-bình-duyệt.
- **Phá vòng (c):** nếu chỉ cần nền NP-hard thì Karp 1972 gọn hơn; Ailon et al. mạnh hơn vì trực tiếp "aggregating inconsistent pairwise → consistent ranking".
