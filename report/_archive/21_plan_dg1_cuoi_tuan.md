# 🗓️ PLAN DG1 CUỐI TUẦN (cho VCL) + CHECK "ĐÃ THUYẾT PHỤC CHƯA"

> **Mục tiêu:** làm xong **DG1 từ đầu tới cuối** trong cuối tuần này (Thứ 7 → Chủ nhật). DG1 = đánh giá hướng dẫn **1 màn** (MobileViews + ScreenSpot đối chứng). **Chạy LOCAL + MIỄN PHÍ — không cần Colab.**
> *(DG2 = AndroidControl/Colab, để bài FAIR sau.)*

---

## PHẦN 1 — METRIC + PIPELINE DG1 ĐÃ THUYẾT PHỤC CHƯA? (check thẳng)

🟡 **Nền VỮNG, nhưng phải vá 4 lỗ hổng thì mới đủ thuyết phục cho 1 bài hội nghị:**

| # | Lỗ hổng (hội đồng/reviewer sẽ vặn) | Cách vá (làm được trong cuối tuần) |
|---|---|---|
| 1 | **"Có oracle thì 'không bịa' quá dễ → tầm thường?"** | Đóng khung rõ: oracle chỉ lo **TỒN TẠI**; cái khó còn lại = **đúng-ý + đủ-ý + rõ-ràng**, mình đo riêng. Và **đóng góp chính là CÁCH ĐÁNH GIÁ + lớp model-agnostic**, không claim "né-nút-ma là phát minh". |
| 2 | **"Metric tự động có khớp người không?"** (quan trọng nhất cho bài *đánh giá*) | **BẮT BUỘC làm Track B nhỏ:** 2–3 người chấm ~40–60 mục → đo tương quan + Krippendorff α + báo CI-width. Không có cái này thì bài yếu. |
| 3 | **"Câu hỏi tự soạn — có thiên vị không?"** | Viết **protocol câu hỏi** rõ (mỗi màn 1 câu "làm sao để X", X làm-được-trên-màn) + người duyệt + công bố số lượng. |
| 4 | **Grounding ≈ Faithfulness** trong thiết kế "gọi-theo-tên" (đang đo gần trùng) | Tách rõ: báo **"grounded-existence"** (tên khớp nút thật) + **ScreenSpot** làm đối chứng point-in-bbox **độc lập**. (Hoặc cho model xuất thêm toạ độ để có point-in-bbox thật.) |

**Điểm MẠNH đã có (giữ nguyên):** thiết kế design E hợp lý + model-agnostic · A/B đã chứng minh hệ giảm bịa thật (66.7%→100%) · tách **Bịa vs Đúng-nhãn** (điểm mới) · matcher ALOHa · "null vẫn đậu" (pre-register).

> **Kết luận:** pipeline + metric DG1 **đủ làm bài VCL** NẾU vá 4 lỗ hổng trên — và cả 4 đều làm được **trong cuối tuần, miễn phí** (trừ Track B cần người).

---

## PHẦN 2 — PHẠM VI DG1 CHỐT (gọn để kịp)
- **Dữ liệu:** ~**60–80 màn MobileViews** (nhiều app càng tốt) + **~50 mẫu ScreenSpot** (đối chứng grounding).
- **Model:** **Qwen 3B** (chính, nhanh) + **Qwen 7B** (subset ~30 màn, để cho thấy "hệ giúp trên mọi model"). *(Tùy chọn: ~20 màn qua GPT-4o-mini, ~$2, để có 1 model đóng.)*
- **2 điều kiện mỗi màn:** **BASE** (viết tự do) vs **design E** (oracle + sửa/fallback) → câu chuyện "hệ hiệu quả".
- **Metric báo:** Bịa(ALOHa) · Đúng-nhãn(Clarity) · Grounded-existence · Format(IFEval-style) · Coverage(proxy, công bố rõ là proxy).
- **Track B:** người chấm ~40–60 mục → tương quan auto-vs-người.

---

## PHẦN 3 — PLAN CHI TIẾT (Thứ 7 → Chủ nhật)

### 🟢 THỨ 7 — SÁNG (chuẩn bị, free, ~3h)
1. **Bảng PRE-REGISTRATION** (1 trang): giả thuyết (vd "design E giảm bịa & tăng đúng-nhãn so BASE, có ý nghĩa") + ngưỡng + quy tắc quyết định + ngưỡng matcher τ. *(Tôi soạn nháp.)*
2. **Tải thêm màn MobileViews đa-app** (hoặc dùng 266 màn đã có trong `mv.zip` + bù vài app). *(Tôi lo phần kỹ thuật.)*
3. **Mở rộng harness DG1 đầy đủ** (thêm Format + Coverage-proxy + gộp bảng). *(Nền đã có ở `harness/`.)*

### 🟢 THỨ 7 — CHIỀU (~4h)
4. **Soạn câu hỏi use-case** cho 60–80 màn (tôi DRAFT tự động theo protocol → **bạn duyệt nhanh**, sửa câu nào vô lý).
5. **Khởi động GENERATION chạy nền** (Qwen 3B, BASE + design E) trên 60–80 màn — CPU chậm nên **chạy qua đêm**.

### 🟢 THỨ 7 — TỐI (chạy nền, bạn nghỉ)
6. Generation 3B chạy nền. Tôi chuẩn bị bộ chấm + ScreenSpot control trong lúc chờ.

### 🟢 CHỦ NHẬT — SÁNG (~4h)
7. **Chấm toàn bộ** → ra **bảng DG1** (Bịa/Đúng-nhãn/Grounded/Format/Coverage; BASE vs design E; có CI).
8. **Chạy 7B** trên subset ~30 màn → so model (model-agnostic).
9. **ScreenSpot grounding control** (~50 mẫu, nhanh).

### 🟢 CHỦ NHẬT — CHIỀU (~3h)
10. **Track B pilot:** bạn + 1–2 người chấm so-đôi ~40–60 mục → tôi tính tương quan + α + CI-width.
11. *(Tùy chọn)* chạy ~20 màn GPT-4o-mini nếu muốn 1 model đóng.

### 🟢 CHỦ NHẬT — TỐI (~2h)
12. **Tổng hợp bảng kết quả DG1 + framing trung thực** (vá 4 lỗ hổng Phần 1) → sẵn sàng viết bài VCL.

---

## PHẦN 4 — CẦN BẠN CHUẨN BỊ / QUYẾT
1. **Người chấm Track B:** rủ **2–3 người** rảnh Chủ nhật chiều (chấm ~40–60 mục, mỗi mục 30 giây — khoảng 30–45 phút/người). *(Đây là thứ DUY NHẤT cần người — sắp xếp sớm.)*
2. **Duyệt câu hỏi** tôi draft (Thứ 7 chiều, ~30 phút).
3. *(Tùy chọn)* **API key** GPT-4o-mini nếu muốn thêm 1 model đóng (~$2).
4. Máy **để chạy nền qua đêm Thứ 7** (Ollama generation) — đừng tắt.

---

## PHẦN 5 — NẾU THIẾU THỜI GIAN (kế hoạch rút gọn)
- Bỏ 7B + GPT-4o-mini → chỉ Qwen 3B (vẫn có A/B + Track B = đủ 1 bài).
- Giảm còn ~40 màn.
- Track B chỉ 1–2 người, ~30 mục, báo "pilot, CI rộng" (trung thực).
> Lõi tối thiểu KHÔNG bỏ: **A/B (BASE vs design E)** + **Track B** + **framing 4-lỗ-hổng**. Đây là 3 thứ làm bài thuyết phục.

---

## MỘT DÒNG
**DG1 cho VCL làm trọn cuối tuần, LOCAL + FREE (không cần Colab): pipeline design E + metric (Bịa/Đúng-nhãn/Grounded/Format/Coverage) đã đủ NẾU vá 4 lỗ hổng (framing oracle · Track B người chấm · protocol câu hỏi · tách grounding); plan = T7 chuẩn bị + generation qua đêm, CN chấm + so-model + Track B + viết bảng. Thứ duy nhất cần người = 2–3 người chấm Chủ nhật.**

---

## PHẦN 6 — ✅ KẾT QUẢ THỰC TẾ (đã chạy 2026-06-27)

**Setup:** 80 màn MobileViews (app quản lý thời gian/dự án, nhãn tiếng Anh) · model sinh = **gpt-4o-mini** (vision, ~$0.05 tổng) · bước SỬA = **llama3.2 local** · matcher ALOHa = **nomic-embed-text local** (τ=0.55, batch+cache đĩa). 80 câu hỏi use-case sinh tự động + lưu `harness/dg1_cache/questions.json` (chờ duyệt tay).

| Metric | BASE (viết tự do) | design-E | Chênh [95% CI bootstrap] |
|---|---|---|---|
| **Faithfulness (không bịa)** | 75.4% | **100.0%** | **+24.6pp [+16.2, +33.3]** |
| **Đúng-nhãn / Clarity** | 67.9% | **89.8%** | **+21.9pp [+14.8, +30.0]** |
| Grounded-existence | 75.4% | 97.3% | — |
| Format (IFEval-style) | 74.4% | 74.4% | (design-E không đụng format) |
| Coverage (proxy) | 28.8% | 34.6% | (proxy yếu trên 1-màn — công bố rõ) |

design-E đã **SỬA 24 bước** lệch-tên về nút THẬT + **FALLBACK 4 bước** mô tả-bằng-lời.

**Đọc kết quả (trung thực — vá lỗ hổng #1):**
- **Faithfulness ~100% là DO THIẾT KẾ** (hệ không phát ra lệnh-sai-tự-tin: nút không khớp → sửa/mô tả). Giá-trị-đo-được = (a) BASE bịa bao nhiêu = **24.6pp** hệ chặn được, + (b) **Đúng-nhãn +21.9pp là cải thiện THẬT** (sửa về đúng tên nút trên màn, không phải hiệu ứng thiết kế). **CI cả hai loại 0 → có ý nghĩa thống kê** (n=80, paired bootstrap).
- **Coverage thấp (28.8/34.6%)**: proxy-coverage trên DG1 1-màn yếu (không có gold-steps) → để làm **limitation công bố rõ**, KHÔNG làm headline. Coverage gold thật chỉ có ở DG2/AndroidControl.
- **Grounding ≈ Faithfulness** (75.4 vs 75.4 ở BASE): đúng như lo ngại #4 → cần ScreenSpot point-in-bbox độc lập làm đối chứng (việc còn lại).

**Còn lại để khép DG1 (theo plan):** ① **model thứ 2** cho claim model-agnostic (H2) — qwen7b local hoặc gpt-4o; ② **Track B** (`harness/trackB.html` đã dựng, 40 màn ẩn-danh A/B) — **chỉ anh chấm**; ③ ScreenSpot grounding control; ④ demo định tính tiếng Việt (`questions_vi.json`).
