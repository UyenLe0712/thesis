# report/67 — Vòng C: Fusion VH+OCR giảm oan sai matcher (kết quả deep-research)

> Bối cảnh: matcher lọc-bịa đối chiếu tên nút với View Hierarchy; VH thiếu nhãn nhiều (chữ nằm trên ảnh) nên bước ĐÚNG bị đánh oan là "bịa" → đẩy %fallback lên oan. Vòng C hỏi: thêm OCR bù chỗ VH mù có được không, đặt ở đâu, có số để trích hay phải tự đo.
> Ngày: 2026-07-18.

**Lưu ý độ tin (đọc trước):** Trong khối JSON trả về, **chỉ C3 có nội dung thật và có bảng verdict thật** (4 SUPPORTED + 1 PARTIAL, đối chiếu tận nguồn fetch + tận mã nguồn repo). **C1 và C2 trả về placeholder** (`answer:"test"`, claim `"a"`/nguồn `"b"`) — tức nhánh research xếp-hạng-OCR và nhánh khâu-đặt-OCR **không cho ra dữ liệu kiểm chứng được**. Do đó, mọi kết luận về C1/C2 dưới đây **không neo vào research đã verify** mà (a) suy ra từ phần đã verify của C3, hoặc (b) là khuyến nghị kỹ thuật thường thức, **được gắn cờ rõ** và để user quyết. Không có chuyện bịa số cho C1/C2.

---

## Trả lời thẳng 3 câu hỏi (C1/C2/C3)

### C1 — Chọn OCR nào? (research trả placeholder → chưa có xếp hạng verify được)
Nhánh C1 không cho ra nguồn thật, nên **không có xếp hạng Tesseract vs PaddleOCR vs EasyOCR nào được kiểm chứng để trích**. Ba engine này chỉ được C3 nhắc như các lựa chọn local-free khả dĩ, không kèm so sánh recall.

Khuyến nghị kỹ thuật (KHÔNG từ research đã verify — thường thức kỹ thuật, user quyết cuối):
- **PaddleOCR** là lựa chọn mặc định hợp lý cho chữ UI tiếng Anh: mạnh với text ngắn/nhỏ đặc trưng giao diện, chạy CPU được, free. **EasyOCR** là phương án dự phòng gần tương đương. **Tesseract** nhẹ nhất nhưng yếu hơn với chữ trên nền phức tạp.
- Vì bản thân Vòng C **kết luận phải tự đo recall trên 127 màn** (xem C3), việc chọn engine **không cần chốt bằng research** — nên chốt bằng chính phép tự-đo: chạy thử 1–2 engine trên một lát dữ liệu, so Δrecall + tỉ lệ false-string, rồi giữ engine tốt hơn. Đây là quyết định thực nghiệm rẻ, không phải câu hỏi tài liệu.

### C2 — OCR vào khâu nào? (suy từ phần verify của C3)
- **Chỉ đưa OCR vào KHÂU LỌC**, cấp thêm chuỗi tham chiếu cho matcher `nomic`. **Tuyệt đối không đưa OCR vào kênh CHẤM độc lập** (`bge-m3` + LLM-judge khác họ + token-overlap). Đây là ràng buộc để không phá anti-circularity đã pre-register ở report/56 — và nó khớp với reasoning đã verify của C3.
- **Cách khai anti-circularity trong pre-reg:** ghi rõ một dòng "OCR tham gia DUY NHẤT ở khâu lọc (mở rộng tập nhãn tham chiếu VH ∪ OCR-trong-bbox); kênh chấm giữ nguyên VH gốc, không thấy chuỗi OCR" → kênh lọc và kênh chấm vẫn dùng nguồn khác nhau, không tự-chấm.
- **Tiền lệ fusion (có nguồn thật, verify SUPPORTED):**
  - **MobileViews (arXiv 2409.14337v3)** — chính dataset ta dùng — đã dùng OCR trong bước lọc ("verify component text is clearly visible and readable"). Tức đưa OCR vào khâu lọc là **đi đúng cách nhà làm dataset đã làm**.
  - **PW2SS (Fu et al., Neurocomputing 2024)** — OCR + graphic-detector sinh "Pixel-Words" đạt recall/precision **cao hơn leaf-node VH** (định lượng: +17.29% AR, +10.60% AP so với leaf-node VH, Table 1). Đây là trụ peer-reviewed cho luận cứ "OCR bù chỗ VH mù".
  - **Screen Recognition (Zhang et al., Apple, CHI 2021)** — 59% màn có ≥1 phần tử không khớp được VH, 94% app dính. Trụ cho động cơ "VH một mình không đủ".

### C3 — Có số để trích hay phải tự đo? (verify: SUPPORTED)
**Không có con số recall dạng cặp "VH-only vs VH+OCR về độ phủ nhãn phần tử UI" nào được công bố trên dataset công khai để trích thẳng.** Ba nguồn liên quan nhất đều xác nhận điều này:
- Fok CHI 2022 cho **55.6% phần tử ảnh thiếu nhãn** — số lân cận, biện minh động cơ, không phải recall-cặp.
- Zhang CHI 2021 cho **59%/94%** — cũng là động cơ, không phải Δrecall của fusion.
- PW2SS chứng minh OCR > VH nhưng bằng tác vụ downstream trên RICO-PW, **không có con số recall-độ-phủ-nhãn dạng cặp** để trích thẳng.

→ **Luận văn PHẢI TỰ ĐO** trên 127 màn của mình. Việc này FREE/LOCAL (đã có sẵn ảnh + VH, OCR chạy local).

---

## Cổng dừng C3

**KHÔNG ĐẠT ở nghĩa "có số trích thẳng" → chuyển sang tự đo. Nhưng đây là kết cục TỐT, không phải bế tắc.**

- Cổng dừng research: **ĐÓNG**. Đã xác nhận (SUPPORTED) rằng không tồn tại con số cặp để trích → **không research thêm về điểm này**.
- Hệ quả: biến thành **TASK CODE** — đo recall nhãn VH-only vs VH+OCR trên 127 màn/30 app, local, không tốn API.
- **Cảnh báo giới hạn (đã verify, phải khai):** recall tự-đo chỉ tính trên **phần tử ĐÃ có trong VH**. Phần tử tương tác **vắng hoàn toàn khỏi VH** (chính là 59%/94% của Zhang) thì OCR-trong-bbox không cứu được nếu không có bộ dò pixel độc lập. Phải khai thẳng: đây là **"recall CÓ ĐIỀU KIỆN trên tập VH liệt kê"**, không phải recall tuyệt đối.

---

## Bảng claim sống / bị bác

| Claim | Nguồn | Peer-reviewed? | Verdict | Ghi chú |
|---|---|---|---|---|
| Không có con số recall cặp VH-only vs VH+OCR để trích thẳng → phải tự đo trên 127 màn | Tổng hợp fetch MobileViews 2409.14337v3 + Screen2Words + PW2SS | Không (tổng hợp) | **SUPPORTED** | Claim phủ định sự-tồn-tại; ba nguồn viện dẫn đều xác nhận thiếu metric đó. Framing "để trích thẳng" khiến nó đứng vững thực dụng. |
| 55.6% phần tử ảnh thiếu nhãn accessibility (Android) | Fok et al., CHI 2022 (DOI 10.1145/3491102.3502143) | **Có** | **SUPPORTED** | Khớp abstract chính thức. Là % trên phần tử ảnh DUY NHẤT đã crawl (312 app/16 tháng), không phải mọi phần tử — diễn đạt vẫn trung thành. |
| 59% màn có ≥1 phần tử không khớp VH; 94% app dính | Zhang et al., Screen Recognition, CHI 2021 (Apple) | **Có** | **SUPPORTED** | Số khớp chính xác. ⚠ arXiv gốc là **2101.04893** (không phải 2101.00091 / 2310.00091 — cái sau là nguồn cấp hai trích lại). Sửa ID trước khi in. |
| OCR + graphic-detector recall/precision > leaf-node VH | Fu et al., PW2SS, Neurocomputing 2024 (arXiv 2105.11941) | **Có** | **SUPPORTED** | Có số định lượng (+17.29% AR, +10.60% AP...). Mạnh hơn cả cách phát biểu "định tính" trong claim. |
| Phép tự-đo recall (mẫu số = phần tử tương tác VH; VH-only = có text/content-desc; VH+OCR = nhãn VH HOẶC chuỗi OCR trong bbox; Δrecall = mức bù) khớp `dg1_vh_coverage.py` (M4) | Suy ra + hạ tầng sẵn có | Không (repo) | **PARTIAL** | **Chỉ nửa VH-only đúng**: `dg1_vh_coverage.py` (M4, report/40) đã tính mẫu số actionable + tử số text/content_description, chạy local. **Nửa VH+OCR + Δrecall KHÔNG có trong script đó**, chưa build, chưa pre-register — thuộc report/63/64/61. Nguồn quy chiếu đúng cho nửa fusion là report/63/64/61, KHÔNG phải report/40. |

**REFUTED:** không có claim nào bị bác hoàn toàn.
**PARTIAL cần lưu:** claim phép-đo — đừng viết như thể script fusion đã tồn tại; nó là **đề xuất chưa thực thi**.
**Placeholder (không có nguồn):** toàn bộ C1 (xếp hạng OCR) và C2 (nhánh riêng) — coi như **chưa research**, không được trích như kết quả.

---

## Khuyến nghị cho luận văn

*(Quyết định cuối cùng thuộc về user — dưới đây là đề xuất.)*

1. **Đặt OCR ở khâu lọc, ngoài kênh chấm.** Khai một dòng trong pre-reg (report/56): *"OCR bổ sung chuỗi tham chiếu cho matcher nomic ở khâu lọc; kênh chấm bge-m3 + LLM-judge + token-overlap không nhận chuỗi OCR."* Điều này giữ nguyên tính độc lập đã pre-register và có tiền lệ ngay trong MobileViews + PW2SS.

2. **Chọn engine bằng thực nghiệm, không bằng tài liệu.** Vì C1 không có xếp hạng verify được và ta phải tự đo anyway: chạy PaddleOCR (mặc định) + EasyOCR (đối chứng) trên một lát ~20 màn, so Δrecall và tỉ lệ chuỗi rác, giữ cái tốt hơn. Đừng tốn thời gian research thêm về "OCR nào tốt nhất".

3. **Viết TASK CODE tự-đo (bước tiếp theo cụ thể):** mở rộng `dg1_vh_coverage.py` thành phiên bản có nhánh OCR:
   - Mẫu số: phần tử **actionable** trong VH (clickable ∨ editable ∨ long_clickable, bounds hợp lệ) — giữ nguyên như M4.
   - Tử số VH-only: có `text` ∨ `content_description` dùng được (đã có `usable_label`).
   - Tử số VH+OCR: nhãn VH dùng được **HOẶC** có chuỗi OCR nằm trong bbox phần tử (containment/IoU ≥ ngưỡng).
   - Xuất: recall VH-only, recall VH+OCR, **Δrecall** (mức oan sai được cứu) + cluster-by-app.
   - Chạy local trên 127 màn, không API.

4. **Pre-register TRƯỚC khi chạy (tránh tuning post-hoc):**
   - **Ngưỡng containment/IoU** giữa bbox-VH và box-OCR để gọi là "khớp nhãn" — chốt con số trước, đừng dò sau khi nhìn kết quả.
   - Khai giới hạn "recall CÓ ĐIỀU KIỆN trên tập VH liệt kê" (không cứu được phần tử vắng hẳn khỏi VH — dẫn Zhang 59%/94%).
   - Ngưỡng τ của matcher: chạy **pilot nhỏ so %fallback trước/sau khi thêm OCR** để xác nhận OCR không làm dịch τ ngoài dự kiến.

5. **Sửa citation trước khi in:** arXiv của Screen Recognition là **2101.04893** (không dùng 2310.00091 — nguồn cấp hai). Verify lại định nghĩa mẫu số của 55.6% từ bản HTML/ACM sạch của Fok (PDF gốc lỗi parse, chưa xác minh trực tiếp).

---

## Việc phải tự làm (gaps)

- **[CODE]** Viết/mở rộng script tự-đo VH+OCR recall trên 127 màn (mô tả ở khuyến nghị #3). Đây là việc chính, thay cho research.
- **[PRE-REG]** Chốt ngưỡng containment/IoU trước khi chạy; khai OCR-chỉ-ở-lọc vào report/56.
- **[PILOT]** So %fallback trước/sau khi thêm OCR để kiểm τ không bị dịch.
- **[CITATION]** Xác minh lại 55.6% từ bản HTML/ACM sạch của Fok CHI 2022; sửa arXiv ID Screen Recognition thành 2101.04893.
- **[GIỚI HẠN]** Khai rõ recall tự-đo là "có điều kiện trên tập VH liệt kê"; phần tử vắng hẳn khỏi VH nằm ngoài tầm đo nếu không có bộ dò pixel độc lập.
- **[C1/C2 chưa có research]** Nhánh xếp-hạng-OCR và nhánh khâu-đặt riêng trả placeholder — nếu user muốn có kết luận research-based cho C1/C2 thì phải chạy lại; còn không thì giải quyết bằng thực nghiệm ở #2 (rẻ hơn, đủ dùng).
- **[PW2SS số cặp]** Muốn trích con số OCR-gain cụ thể của PW2SS phải đọc full-text bản Neurocomputing (paywall) — chỉ cần nếu muốn dẫn số +17.29% AR, còn dẫn định tính thì đã đủ từ ar5iv.