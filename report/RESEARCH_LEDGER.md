# 📒 SỔ TRA DEEP-RESEARCH — "đã research gì rồi" (đọc TRƯỚC mọi đợt research mới)

> **Mục đích:** trước khi chạy bất kỳ deep-research/workflow nào, **đọc file này** để biết cái gì **ĐÃ làm** (skip, khỏi
> tốn token) và cái gì **CHƯA** (chỉ chạy phần đó). Đây là *index mỏng* — không chứa nội dung chi tiết, chỉ trỏ tới file gốc.
> Cập nhật: 2026-07-05. **Quy tắc: mỗi đợt research xong PHẢI thêm 1 dòng vào bảng §1 + cập nhật §2/§3.**

---

## §1. CÁC ĐỢT ĐÃ CHẠY (bảng tra nhanh)

| # | Chủ đề | Trạng thái | File kết quả | Run ID (resume nếu cần) |
|---|---|---|---|---|
| R-01 | **Validate METRIC / bộ chấm** (matcher + LLM-judge, mức gán-tay tối thiểu) | ✅ XONG | `report/27` §6–§7 | `wf_4f756710-46b` · re-verify `wf_7a51cf9f` |
| R-02 | **Dữ liệu** (3 bộ verify tận file: nguồn/venue/quy mô/giấy phép) | ✅ XONG | `report/44` | `wf_6d07419b` |
| R-03 | **Freshness scan 2025–2026** (đề tài lỗi thời / bị scoop?) | ✅ XONG | `report/42` §1–§5 | `wf_3d7cdc91` |
| R-04 | **Debate giám-khảo pipeline+metric 2026** | ✅ XONG | `report/42` §6 | `wf_73dfaaf9` |
| R-05 | **Deep-research đối kháng (7 rủi ro reject R1–R7)** | ✅ XONG | `report/42` §7 | `wf_9c395ab3-f59` |
| R-06 | **Research riêng KIẾN TRÚC pipeline (đúng thời 2026?)** | ✅ XONG | `report/42` §8 | `wf_1306a703-213` |
| R-07 | **Verify pipeline (đóng góp A) — đủ đóng góp thạc sĩ? (đối kháng)** | ✅ XONG | `report/45` (§C = phán quyết) | fetch `wf_9284d315-f7c` · verify+synth `wf_f227453f-dd5` |
| R-08 | **Verify metric (đóng góp B) — đủ đóng góp thạc sĩ? (đối kháng)** | ✅ XONG | `report/27` (§8 = phán quyết) | `wf_38650b3d-e50` |
| R-09 | **Cỡ mẫu mỗi bộ dataset (bao nhiêu item là đủ chuẩn thạc sĩ?)** | ✅ XONG | tóm ở §2 dưới + `report/43` §11.4/Ch.13 | `wf_54b20a21-030` |
| R-10 | **Thiết kế thí nghiệm (6 RQ · 15 thí nghiệm E1–E15)** | ✅ XONG | `report/47` (đầy đủ) · `report/43` Ch.13 (gọn) | `wf_c3cf5aa6-510` |
| R-11 | **Chọn item 3 bộ dataset + 2 vòng debate → CHỐT-CÓ-ĐIỀU-KIỆN** | ✅ XONG — MV 127/30 · SS 501 · AC 286/169; không lỗi thiết kế; gate cứng = freeze manifest+git trước API (`report/48` §7) | `report/48` · `harness/kept_screens_final.json` · `dataset_samples/screenspot_full/` · `harness/androidcontrol_selected.json` | debate `wf_4ebb6d96-04c` + `wf_ebb4fbaf-dbb` |
| R-12 | **Audit độ vững pipeline Faithful Distillation (Fable 5, 64 quyết định + citation/thống kê)** | ✅ XONG — CẦN-VÁ→ĐÃ VÁ: thiết kế vững (60/64 khớp), 6 lỗ tài liệu/pre-reg đã vá `report/54`+`53`; UI-R1 sửa AAAI2025→**2026**; FEWL hạ preprint | `report/54` (Phụ lục E/G) · `report/53` §5.2/§5.6 · CLAUDE.md §0 | `wf_0ebe080f-bae` |
| R-13 | **Định danh venue VCL & FAIR + fit 2 bài + chính sách trùng lặp** | ✅ XONG — FAIR=NC Nghiên cứu Cơ bản&Ứng dụng CNTT (lần 19, dl 15/8/2026, tiếng Anh, RỘNG); VCL=Ngôn ngữ học Tính toán HUFLIT (30/8, tiếng Việt, thuần NLP). **→ ĐÃ CHỐT (sau trao đổi user): nộp CẢ HAI — FAIR=bài model (English), VCL=bài sinh-hướng-dẫn-tiếng-Việt (user OK fit "miễn có chất ngôn ngữ"); không có dataset GUI tiếng Việt (quét MobileViews chỉ 2 màn lẻ) → VCL dùng màn English + output tiếng Việt.** CHƯA có nguồn: tỉ lệ nhận/index/dual-submission | block ⚠️ đầu `report/KE_HOACH_2_BAI_BAO.md` (bản 3) · CLAUDE.md §2 | `wf_ef24768f-5ad` (verify 1-vote) |

---

## §2. ĐÃ CHỐT — ĐỪNG CHẠY LẠI (kết luận đã ổn định, chỉ cần trích)

- **✅ CẢ HAI ĐÓNG GÓP đủ tư cách khoa học thạc sĩ (đối xứng, "ngang nhau CÓ ĐIỀU KIỆN"):** A/pipeline (R-07, `report/45` §C) 7/8 vững; B/metric (R-08, `report/27` §8) 7/8 vững. Cả hai chờ SỐ thực nghiệm dương (DG2). → **Phần RESEARCH/thiết kế cả 3 trụ (pipeline/metric/dataset) đã CHỐT.** Việc còn lại = áp-fix câu chữ + THỰC NGHIỆM, không phải research.

- **Protocol validate metric/judge** (6 nguyên tắc, đều có trụ peer-reviewed: Panickssery NeurIPS24 · ALOHa NAACL24 · Active-Eval ACL22 · Sai EMNLP21 · Chen ICSE20 · Clark ACL21) → **`report/27` §6.3 + §7**. *(HITLC giảm ~80% nhãn — KHÔNG phải 89%.)*
- **Pipeline đúng nhu cầu 2026, KHÔNG cần đổi kiến trúc** — rủi ro chỉ ở cách trình bày → **`report/42` §8 · `report/43` §4.5, §12**.
- **7 rủi ro reject R1–R7 + phản-thủ** (AskEase/FaithScore/frontier-hết-bịa/scoop-khối-sắp-màn/tolerance-14%/perturbation-4-tiêu-chí/thống-kê-ít-cụm) → **`report/42` §7 · `report/43` (Ch.4/5/7/9/12)**.
- **Không lỗi thời / không bị scoop** — combo "sinh-hướng-dẫn-cho-người + neo-VH + no-gold" còn trống → **`report/42` · `report/43` §9**.
- **11 citation venue ĐÃ xác nhận** (FaithScore EMNLP24 · CoVe ACL24 · RARR ACL23 · Huang ICLR24 · ALOHa NAACL24 · Qin NAACL24 · EACL26 · AskEase CHI26 · CaLM ACL24 · CRITIC ICLR24 · GVL ICLR25) → **`report/45` §A.5 · `report/43` Phụ lục C**.
- **Thư viện paper** (34 bài, mỗi bài tóm tắt + refer-gì) → **`report/papers/`**.
- **Cỡ mẫu chốt (R-09):** MobileViews **~150 màn / 30+ app** (nút thắt là SỐ APP G≈17, không phải số màn) · AndroidControl **~500 episode, ≥30/mốc-N** (neo "Random-500" của chính bài) · ScreenSpot-v2 **502 mobile** (chấm trọn, không cắt) · gán-tay matcher **80–120 cặp** · perturbation **10–15 loại × ≥30** · judge neo-người **100–200 cặp**. Thạc sĩ ĐƯỢC khung "exploratory + CI + caveat"; không cần full 2.855 ep / 1.000 màn.
- **Thiết kế thí nghiệm (R-10):** 6 RQ · 15 thí nghiệm E1–E15 · bắt-buộc-thạc-sĩ = E1(≥2 model)/E2/E3/E4/E5/E6/E8+E9/E14 · điều kiện "A ngang B" = K-pair GO + Step-SR/τ dương. Đầy đủ `report/47`; gọn `report/43` Ch.13.

## §3. CHƯA CHẠY / CHẠY TIẾP KHI CẦN (đây là chỗ đáng chạy đợt sau)

- ✅ ~~R-07 Verify+Synthesize~~ → **XONG** (`wf_f227453f-dd5`): pipeline ĐỦ đóng góp thạc sĩ (7/8 khẳng định vững; A5 hạ claim), 6/6 citation venue ĐÚNG. Kết quả `report/45` §C.
- ✅ ~~Kiểm venue bài ⚠~~ → **XONG** (gộp trong R-07): TOMATO=ICLR2025 Poster · EZ-Sort=CIKM'25 · Dodgersort=PAKDD2026 · construct-validity + Neither-Valid = NeurIPS2025 · MacKinnon = J.Econometrics 2023. Tất cả ĐÚNG.
- ✅ ~~Áp fix R-07 + R-08 vào `report/43` + `papers/`~~ → **XONG** (2026-07-05): A5 reframe pairwise/Copeland; hạ "biến mất"/"đồng thuận"/"độc lập"/"tới đích"; M6 Step-SR reframe; M1 no-gold "có điều kiện"; M3 mẫu-nhỏ human-validation; M4 "khác-cơ-chế"; M5 Brandenburg; nhãn citation (TOMATO Poster, gỡ ⚠ EZ-Sort/Dodgersort/NeurIPS2025/MacKinnon); 2 neighbor A7. File 45 §A đã gắn banner "dùng §C".
- ✅ ~~Sửa "Best Paper → Outstanding Paper"~~ → **XONG** (Active Evaluation, ACL 2022): sửa ở `CLAUDE.md §4` · `report/27` (3 chỗ) · `report/22` · `GEMINI_CONTEXT.md`. Giữ nguyên "Best Paper" của Ribeiro/CheckList (đúng thật). Số 80% giữ nguyên.
- ⏳ **Human-correlation / convergent validity:** *cố ý* để future-work (không phải thiếu sót) — chỉ chạy nếu hội đồng đòi.
- ⏳ **Verify link cổ điển:** Copeland (Dwork WWW01), min-FAS (Ailon JACM08), Fagin/Lapata 2006 — link còn ⚠ trong `report/papers/` (chưa qua verify sơ cấp).
- ⏳ **Follow-up R-13 (venue — CHƯA có nguồn chính thức, USER tự verify, đừng bịa):** **deadline CFP VCL2026 thật** (30/8 = user nhớ, chưa xác nhận) · tỉ lệ chấp nhận FAIR/VCL · index Scopus/DBLP · ISBN kỷ yếu · độ dài/template bài · **chính sách dual-submission & self-plagiarism từng venue** (QUAN TRỌNG vì 2 bài dùng chung data nguồn) · rủi ro "bản tiếng Việt = prior publication" khi mở rộng ra bài quốc tế. Tra thẳng trang venue + quy định khoa, KHÔNG suy đoán. *(Chỗ-nộp ĐÃ chốt: cả 2 bài, FAIR=model/VCL=sinh-tiếng-Việt — không còn chờ.)*

## §4. CÁCH DÙNG CHO ĐỢT RESEARCH SAU (prompt mẫu)

> Đọc `report/RESEARCH_LEDGER.md`. Mục nào ở §2 (ĐÃ CHỐT) thì **SKIP, không chạy lại**. Chỉ chạy các mục ở §3 (CHƯA CHẠY)
> — hoặc chủ đề mới chưa có trong bảng §1. Nếu là R-07, resume từ `report/45` §B (evidence đã fetch, chỉ chạy Verify+Synthesize).
> Xong thì **cập nhật lại sổ này** (thêm dòng §1 + chuyển mục từ §3 sang §2).

*Ghi chú resume kỹ thuật: `Workflow({ name/scriptPath, resumeFromRunId })` chỉ replay-cache khi **cùng phiên**; sang phiên mới cache thường mất → dùng dữ-liệu-đã-lưu-trong-file (vd `report/45` §B) để chạy tiếp, KHÔNG fetch lại.*

---
*Liên quan: `report/27` (metric) · `report/42` (pipeline/freshness) · `report/44` (dữ liệu) · `report/45` (pipeline verify — evidence) · `report/43` (hồ sơ tổng, tự-đủ) · `report/papers/` (thư viện trích dẫn).*
