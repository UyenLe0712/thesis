# report/74 — K2: kết quả đếm phân loại kiểu bịa THẬT

> VIỆC 0b trong report/72. Đếm bịa THẬT của teacher gpt-4o-mini trên 80 màn output đã cache (FREE, không API mới), để biết điểm mù của matcher (K1 phát hiện) có thật sự nghiêm trọng trong thực tế không. Code: `harness/k2_hallucination_types.py`, số: `harness/k2_results.json`. Ngày: 2026-07-18.

## Phán quyết 1 dòng

**Điểm mù "bỏ lọt bịa gần-nghĩa" mà K1 lo → gần như KHÔNG xảy ra trong output thật (0/127 ca rõ).** Ngược lại, lỗi thật sự áp đảo là **KẾT OAN**: matcher đánh oan **nút icon/mô tả CÓ THẬT** thành "bịa" vì VH thiếu nhãn. → ưu tiên sửa đảo chiều: **OCR/nhận-icon là fix số 1**, không phải chống-bỏ-lọt. Và một cảnh báo nền: **gpt-4o-mini bịa RẤT ÍT trên dữ liệu này** → đụng thẳng nghi ngờ 5 (ít bịa thì lọc được gì).

## Số liệu (127 bước teacher thật, 80 màn)

| Loại | Số | % | Nghĩa |
|---|---|---|---|
| **Verbatim** (khớp y-chữ nhãn VH) | 87 | 68,5% | tham chiếu nút THẬT, đúng |
| **Không verbatim** | 40 | 31,5% | ứng viên "bịa" mà matcher xét |

Phân loại tay 40 ca không-verbatim (soi từng cái: element + ghi chú + nhãn gần nhất):

| Nhóm | Số | Thực chất | Matcher xử |
|---|---|---|---|
| **Icon/ký hiệu thật** (`+` `✓` `<` `>`) | 20 | nút add/confirm/điều-hướng CÓ THẬT, VH không có chữ | đánh BỊA = **kết oan** |
| **Field/nút mô tả thật** (Project name, Add description, slider, toggle, contact...) | 11 | field/control THẬT, VH ghi nhãn khác | phần lớn kết oan |
| **Nút CHỮ-HOA thật** (ADD LOCATION, EXPENSES, ADD NEW) | 4 | nút/tab THẬT | đánh BỊA = kết oan |
| **Placeholder `<...>`** (`<date>`, `<new charge rate>`) | 3 | teacher xuất khuôn mẫu, không phải tên nút | tạp — lỗi prompt |
| **Khác** (OK, "30") | 2 | nhiều khả năng thật (nút OK, giá trị 30 phút) | — |
| **Bịa nút-không-tồn-tại gần-nghĩa** | **0** | — | — |

**Không tìm thấy ca nào là "teacher bịa một nút nghe hợp lý nhưng không có thật"** (loại near-synonym mà K1 stress-test). 35/40 ca không-verbatim là **nút THẬT bị VH bỏ nhãn** (icon/mô tả/chữ-hoa); 3 là artifact khuôn mẫu; 2 mơ hồ nhưng nhiều khả năng thật.

## K1 và K2 ăn khớp thế nào (không mâu thuẫn)

- **K1** (adversarial): matcher *về nguyên tắc* không tách được bịa-gần-nghĩa với paraphrase, và **hay đánh oan** (chiều false-positive).
- **K2** (output thật): lỗi *thực tế xảy ra* gần như toàn bộ là **kết oan** (đánh oan 35/40 nút thật vì VH thiếu nhãn); bịa-gần-nghĩa **không thấy**.
- Gộp lại: **chiều kết-oan của K1 là vấn đề thật (K2 xác nhận), chiều bỏ-lọt tuy có trên lý thuyết nhưng gần như không bị kích hoạt bởi teacher này.** → dồn công sửa vào kết-oan.

Khớp luôn với con số K1: VH chỉ phủ 62,4% nút actionable → 37,6% icon-only không nhãn. K2 cho thấy chính 37,6% đó (nút `+`/`✓`/mũi tên/toggle) là nguồn kết-oan chính.

## Hai hệ quả LỚN (phải đưa lên bàn với thầy)

### 1. Bộ lọc hiện tại có nguy cơ LÀM HẠI dữ liệu, không phải làm sạch
Nếu ~31,5% bước bị đánh "bịa" rồi viết-lại thành câu chung chung, mà ~gần hết trong số đó là **nút thật**, thì "lọc" đang **biến hướng dẫn cụ thể-đúng thành mô tả mơ hồ** — giảm chất lượng data, không tăng. **Phải sửa matcher (OCR/nhận-icon) TRƯỚC khi build data**, nếu không Tier 1 đo được "khác biệt" cũng chỉ là nhiễu, không phải lọc-bịa thật.

### 2. gpt-4o-mini bịa rất ít trên dữ liệu này → nghi ngờ 5 thành hiện thực
Bịa thật ≈ 0–2/127 bước (dưới ~2%), thấp xa con số "~¼" trong dân gian. **Con số "~¼ bịa" cũ nhiều khả năng là kết-oan (VH thiếu nhãn) bị đọc nhầm thành bịa**, không phải bịa thật. Hệ quả: nếu teacher gần như không bịa → tập data-lọc và data-thô **gần như giống nhau** → **Tier 1 có nguy cơ null vì lý do tầm thường** (chẳng có gì để lọc). Đây đúng là nghi ngờ 5, giờ có số.

Cách gỡ (bàn với thầy): (a) đo lại bịa thật sau khi sửa matcher (OCR) trên mẫu rộng hơn; (b) cân nhắc teacher yếu hơn / câu hỏi khó hơn / app dễ gây bịa hơn để CÓ bịa mà lọc; (c) nếu bịa vốn ít, đổi khung đóng góp: nhấn "giữ được độ đúng khi chưng cất xuống model nhỏ on-device" thay vì "lọc bỏ bịa nhiều".

## Giới hạn của K2 (khai thẳng)

- **Không xem được ảnh** → "thật hay bịa" là suy luận từ element + ghi chú + nhãn gần nhất, không phải xác nhận pixel. Một số ca "thật" có thể là bịa; nhưng kể cả vậy, chúng **không thuộc loại near-synonym** (matcher vẫn bắt vì sim thấp).
- **Mẫu hẹp**: 80 màn, một teacher (gpt-4o-mini), một-hai miền app (quản lý dự án/chi phí), câu hỏi teacher làm khá tốt. Miền khác có thể bịa nhiều hơn.
- **Artifact prompt** (`<...>`) làm nhiễu — cần sửa prompt sinh của teacher.

## Việc kế (đề xuất, cập nhật sau K1+K2)

1. **OCR/nhận-icon là fix số 1** (VIỆC OCR / Vòng C) — giờ có bằng chứng thật: 20/40 lỗi là icon `+`/`✓`/mũi tên, 4/40 là nút chữ-hoa OCR đọc được. Làm free/local.
2. **Sửa prompt teacher** để bỏ khuôn mẫu `<...>`.
3. **Đo lại bịa thật SAU khi có matcher-OCR** trên mẫu rộng hơn → mới biết còn đủ bịa để lọc không.
4. **Mang K1+K2 lên gặp thầy** như một cặp: matcher yếu (K1) + lỗi thực tế là kết-oan + teacher ít bịa (K2) → quyết định lớn: sửa trọng tài + có thể phải chỉnh khung đóng góp (nghi ngờ 5).

> Tóm: K2 cho tin tốt lẫn tin đáng lo. **Tốt:** cái nguy hiểm nhất K1 sợ (bỏ lọt bịa gần-nghĩa) hầu như không xảy ra thật. **Đáng lo:** lỗi thật là kết-oan nút thật (sửa được bằng OCR), và teacher bịa quá ít nên bản thân việc "lọc bịa" có thể không tạo đủ khác biệt cho Tier 1 — phải bàn thầy trước khi đổ tiền train.
