# THƯ VIỆN PAPER THAM KHẢO — mỗi bài 1 file

> Mỗi file = **link + tóm tắt dễ hiểu cho người mới + "dùng refer gì cho bài của tôi"**.
> ✅ = đã viết file · ⏳ = chưa viết (nói tôi viết tiếp). Trạng thái venue: ✔ đã xác minh (report/45) · ⚠ cần kiểm.

## A. Thước đo & đánh giá (nền cho metric + tính hợp lệ)
- ✅ [ALOHa (NAACL 2024)](aloha_naacl2024.md) ✔ — nền công thức **Độ trung thực** (đối chiếu ngữ nghĩa với nguồn ngoài).
- ✅ [FaithScore (Findings EMNLP 2024)](faithscore_emnlp2024.md) ✔ — faithfulness reference-free cho VLM; đối thủ gần + phân định.
- ✅ [Chim, Ive & Liakata (Computational Linguistics 2025)](chim_ive_liakata_cl2025.md) — **khung đánh giá neo** (no-gold).
- ✅ [Sai et al. (EMNLP 2021)](sai_emnlp2021.md) — trụ **perturbation** validate metric.
- ✅ [BUMP (ACL 2023)](bump_acl2023.md) — minimal-pair meta-eval (cặp trụ với Sai).
- ✅ [Chen et al. (ICSE 2020)](chen_icse2020.md) — **>77% app thiếu nhãn** → biện minh độ-phủ + fallback.
- ✅ [Panickssery et al. (NeurIPS 2024)](panickssery_neurips2024.md) — self-preference bias → judge KHÁC HỌ.
- ✅ [Clark et al. (ACL-IJCNLP 2021)](clark_acl2021.md) — human-eval không còn là gold sạch (bỏ human khỏi cổng đậu/rớt).
- ✅ [Measuring what Matters: Construct Validity in LLM Benchmarks (NeurIPS 2025)](construct_validity_neurips2025.md) — lăng kính construct-validity.
- ✅ [Neither Valid nor Reliable? (NeurIPS 2025, Position)](neither_valid_nor_reliable_neurips2025.md) — không lấy LLM-judge làm trục validate chính.

## B. Pipeline: hậu-kiểm & sửa bằng tín hiệu ngoài (nền cho §4.5)
- ✅ [Huang et al. — "LLMs Cannot Self-Correct Reasoning Yet" (ICLR 2024)](huang_iclr2024.md) ✔ — chỉ **tự-sửa nội tại** bị bác.
- ✅ [Chain-of-Verification / CoVe (Findings ACL 2024)](cove_acl2024.md) ✔ — sinh→kiểm (post-hoc).
- ✅ [RARR (ACL 2023)](rarr_acl2023.md) ✔ — sửa theo nguồn ngoài, minimal-edit.
- ✅ [CaLM (ACL 2024)](calm_acl2024.md) ✔ — verify grounded generation bằng nguồn ngoài.
- ✅ [CRITIC (ICLR 2024)](critic_iclr2024.md) ✔ — sửa bằng công cụ/tín hiệu ngoài.
- ✅ [Tyen et al. (Findings ACL 2024)](tyen_acl2024.md) ✔ — sửa tốt khi được cấp vị-trí-lỗi ngoài.

## C. Sắp thứ tự màn (nền cho Stage-0)
- ✅ [Qin et al. — Pairwise Ranking Prompting (Findings NAACL 2024)](qin_prp_naacl2024.md) ✔ — pairwise > listwise.
- ✅ [Dwork et al. (WWW 2001)](copeland_dwork_www2001.md) — **Copeland** (rank aggregation).
- ✅ [Ailon et al. (JACM 2008)](minfas_ailon_jacm2008.md) — **minimum feedback arc set** (phá vòng).
- ✅ [Fagin 2006 + Lapata (CL 2006)](partial_ranking_fagin_lapata.md) — **τ thứ-tự-bộ-phận**.
- ✅ [TOMATO — bag-of-frames](tomato_bagofframes.md) ✔ — VLM yếu sắp thứ tự (module không thừa); ICLR 2025 Poster.
- ✅ [GVL (ICLR 2025)](gvl_iclr2025.md) ✔ — xáo-frame→suy-thứ-tự là hướng khả thi.
- ✅ [Sort-Story (EMNLP 2016)](sort_story_emnlp2016.md) — prior-art kinh điển sắp ảnh xáo trộn.
- ✅ [Gardner et al. — Contrast Sets (EMNLP 2020)](gardner_contrast_sets_emnlp2020.md) — trụ khái niệm cho phân-tầng-một-cue.
- ✅ [EZ-Sort (CIKM 2025)](ezsort_cikm2025.md) — prior-art VLM/CLIP-pairwise-sort (phân định).
- ✅ [Dodgersort (PAKDD 2026)](dodgersort_pakdd2026.md) — trọng-số-theo-bất-định (nền M2).

## D. Dữ liệu
- ✅ [MobileViews (preprint arXiv 2409.14337)](mobileviews.md) — một màn (ảnh + View Hierarchy).
- ✅ [AndroidControl (NeurIPS 2024 D&B)](androidcontrol_neurips2024.md) — nhiều màn (quỹ đạo vàng).
- ✅ [ScreenSpot-v2 / OS-Atlas (ICLR 2025)](screenspot_v2_osatlas_iclr2025.md) — đối chứng grounding.
- ✅ [AITW (NeurIPS 2023)](aitw_neurips2023.md) — nguồn ngưỡng dung sai 14%.
- ✅ [SeeClick (ACL 2024)](seeclick_acl2024.md) — nguồn gốc thước grounding point-in-bbox + benchmark ScreenSpot.

## E. Định vị 2026
- ✅ [AskEase (CHI 2026)](askease_chi2026.md) ✔ — bài gần nhất; phân định novelty.
- ✅ [Do GUI Grounders Truly Understand UI Elements? (Findings EACL 2026)](do_gui_grounders_eacl2026.md) ✔ — grounder không đáng tin → cần đối chiếu nguồn.

## F. Thống kê & tính hợp lệ (đo lường)
- ✅ [MacKinnon, Nielsen & Webb (Journal of Econometrics 2023)](mackinnon_nielsen_webb_2023.md) — hướng dẫn suy luận cluster-robust ít-cụm (nền §7.4).
- *(construct-validity NeurIPS 2025 → xem mục A; Sai/BUMP/Clark → mục A.)*

---
*Nguồn link/venue đã xác minh: `report/45` (deep-research 2026-07-05). Bài ⚠ cần kiểm venue trước khi in.*
