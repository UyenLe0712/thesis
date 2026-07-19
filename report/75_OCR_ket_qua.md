# report/75 — VIỆC OCR: kết quả đo độ phủ nhãn VH-only vs VH+OCR

> VIỆC OCR (report/72) / Vòng C (report/67). Đo OCR bù được bao nhiêu nút actionable mà VH bỏ nhãn — nguồn KẾT OAN mà K2 (report/74) tìm ra. Chạy trên 127 màn MobileViews thật (3964 nút actionable), OCR = RapidOCR (ONNX, CPU, free). Code: `harness/ocr_vh_coverage.py`, số: `harness/ocr_coverage_results.json`. Ngưỡng khoá trước khi chạy: gán OCR cho nút nếu tâm hộp chữ nằm trong khung nút + conf≥0.5 + có ký tự chữ-số. Ngày: 2026-07-18.

## Phán quyết 1 dòng

**OCR có giúp, nhưng ở mức KHIÊM TỐN và KHÔNG phải thuốc tiên.** Độ phủ nhãn nút-cỡ-nút tăng **+6 điểm** (74→80%); cứu được nhãn text thật (OK, Search, X, tên tab) — NHƯNG ~28% "cứu" là rác (chữ hiển thị gán nhầm vào vùng bấm to), và **hoàn toàn không cứu được icon thuần** (`+` `✓` mũi tên) vốn chiếm ~50% ca kết-oan ở K2. → OCR đáng thêm vào bước lọc **kèm hai điều kiện**: (a) luật gán chặt hơn, (b) một **từ-điển-ký-hiệu** cho icon.

## Số liệu

| Phép đo | VH-only | VH+OCR | Δ |
|---|---|---|---|
| Micro (gộp mọi nút, gồm cả container to) | 69,8% | 81,0% | **+11,2 điểm** |
| Macro (trung bình theo màn) | 64,5% | 80,7% | **+16,2 điểm** |
| **Chỉ nút cỡ-nút** (area < 5% màn — trung thực nhất) | 74,0% | 80,0% | **+6,0 điểm** |

- OCR bù thêm 444 nút = **37% số nút bị VH bỏ nhãn**.
- Khung toạ độ **khớp** (0/2053 hộp OCR vượt kích thước ảnh; 1085 hộp rơi đúng trong một nút) → không dính bẫy lệch-khung như report/44 §8 lo.

## Vì sao con số thô (+11/+16) bị THỔI

Luật containment gán **mọi** chữ nằm trong một vùng bấm cho vùng đó. Mà nhiều vùng bấm là **container to** (thẻ, dòng danh sách) chứa đầy chữ hiển thị. Nên nhiều "nhãn cứu được" thực ra là chữ nội dung, không phải tên nút:

- **Rác điển hình:** `12167STEPS`, `"WHATGOODISTHE`, `NN`, `HELO`, `149` — chữ trên thẻ, không phải nhãn nút.
- Tách ra: trong 444 nút OCR bù, ~**28% là chuỗi rác** (câu dài / toàn số); phần "sạch" (≤3 từ, có chữ) vẫn còn lẫn chữ-hiển-thị như `12167STEPS`. → con số nút-cỡ-nút **+6 điểm** đáng tin hơn con số thô.

## Cái OCR cứu ĐƯỢC vs KHÔNG cứu được (nối với K2)

**Cứu được (nhãn text thật):** `OK` (đúng ca dialog K2 gặp), `X`/`✕` (nút đóng), `Search`, `Calories`, `Active Time`, `Miles`, và loại nút chữ-hoa (ADD LOCATION / EXPENSES kiểu K2). Đây là phần thật sự giảm kết-oan.

**KHÔNG cứu được: icon thuần** — `+` (thêm), `✓` (xác nhận), mũi tên `‹ ›` điều-hướng. OCR không đọc chúng thành chữ có nghĩa. Mà K2 cho thấy **20/40 ca kết-oan là đúng loại icon thuần này** → OCR một mình chỉ chữa được ~nửa vấn đề kết-oan.

## Hệ quả — cách sửa trọng tài (cập nhật sau K1+K2+OCR)

Trọng tài lọc-bịa nên là **đa tầng**, theo thứ tự:

1. **So-chuỗi trước** (bắt bịa gần-nghĩa — K1 cho thấy so-chuỗi bỏ lọt chỉ 5%).
2. **Nhãn VH** (nguồn gốc).
3. **OCR-trong-bbox** với **luật chặt hơn** (hộp OCR phải ~lấp khung nút, không phải mọi chữ trong container; conf cao; dedup) — cứu nhãn text VH thiếu.
4. **Từ-điển-ký-hiệu** cho icon phổ biến: `+`→"add", `✓`→"confirm/done", `✕`/`X`→"close", `‹`/`›`→"back/next", `☰`→"menu". Rẻ, tất định, cứu đúng 20/40 ca icon mà OCR chịu thua.
5. Chỉ khi cả bốn tầng đều trượt → mới coi là bịa → viết-lại fallback.

## Cập nhật (đo trọng tài 3 tầng — sau khi kiểm glyph OCR)

Kiểm cache OCR: **OCR ĐỌC ĐƯỢC nhiều icon glyph** — `+` (23 lần), `X/x/×` (97), `<`/`>` (46), `三`≈menu (8) — chỉ `✓` (dấu tích) là không. Nên từ-điển-ký-hiệu gắn thẳng lên glyph OCR trả về (không cần model dò icon). Đo lại độ phủ nút-cỡ-nút, 3 tầng tham chiếu:

| Tầng tham chiếu | Độ phủ | Δ |
|---|---|---|
| VH-only | 74,0% | — |
| + OCR text | 79,2% | +5,2 |
| + từ-điển-ký-hiệu (glyph→tên) | 79,5% | +5,5 tổng (**+0,3 riêng icon**) |

- Từ-điển-icon chỉ thêm **+0,3 điểm** ở mức tổng — vì phần lớn glyph OCR đọc nằm trên nút VỐN đã có nhãn. Nó vẫn đáng có (cứu đúng ca teacher nói "+"/"X" trên nút trống) nhưng **không phải đòn lớn** như tưởng.
- **Sàn kết-oan còn lại: ~20,5%** nút vẫn không khớp được kể cả VH+OCR+ký-hiệu (icon hình thuần như `✓`, avatar, logo) → giới hạn không xoá hết bằng OCR; muốn hết phải phân-loại-icon bằng thị giác (ngoài phạm vi).

→ **Kết luận trọng tài:** OCR đưa "nút thật khớp được" từ 74% lên ~80%; từ-điển-ký-hiệu vét thêm chút; **~20% icon hình thuần là sàn kết-oan phải khai như giới hạn.** Gộp với K2 (bịa thật ~0): ngay cả trọng tài cải tiến vẫn chủ yếu đang xử lý nút-thật-không-nhãn, càng củng cố nghi ngờ 5.

## Việc kế

1. **Không dùng OCR-thô một mình.** Nếu gắn OCR vào bước lọc, phải kèm luật-gán-chặt + từ-điển-ký-hiệu, nếu không sẽ thêm nhiễu (rác) và vẫn để lọt icon.
2. **Đo lại kết-oan sau khi ghép [so-chuỗi + VH + OCR-chặt + từ-điển-icon]** trên chính các ca K2 → xác nhận tỉ lệ đánh-oan nút thật tụt bao nhiêu. Đây là con số nên mang lên gặp thầy cạnh K1/K2.
3. **Khoá ngưỡng cuối** (conf OCR, tỉ lệ hộp/khung) TRƯỚC khi build data.

## Giới hạn (khai thẳng)

- **RapidOCR chưa phải PaddleOCR "xịn"** — dùng vì nhẹ/CPU/free; nếu cần độ chính xác cao hơn có thể đổi engine, nhưng kết luận cấu trúc (OCR cứu text, thua icon) không đổi.
- **Luật clean-label thô** (≤3 từ) vẫn lọt chữ-hiển-thị → con số "cứu sạch 72%" là cận trên; số thật thấp hơn, nên tin **+6 điểm nút-cỡ-nút**.
- **Chưa đo trực tiếp trên ca K2** (K2 dùng bộ 80 màn pilot cũ tên `app1_sN`; OCR chạy trên bộ 127 chuẩn) — cùng vấn đề VH-thiếu-nhãn nên kết luận chuyển giao, nhưng phép đo ghép-trọng-tài ở "việc kế #2" nên chạy trên cùng một bộ.

> Tóm: OCR đáng thêm nhưng **không đủ một mình** — nó vá phần nút-có-chữ (~text half của kết-oan), còn phần icon thuần phải nhờ **từ-điển-ký-hiệu** (rẻ, tất định). Cặp [OCR-chặt + từ-điển-icon], đặt SAU so-chuỗi, mới là trọng tài lành mạnh. Con số cần cho thầy: +6 điểm phủ nhãn (OCR) + hứa hẹn từ-điển-icon cho 20/40 ca K2.
