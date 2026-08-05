# report/76 — VIỆC 1: đọc tay câu fallback (có dùng được thật không?)

> Kiểm giả định YẾU NHẤT của thiết kế: khi một bước bị coi là "bịa", pipeline viết-lại thành câu mô tả chung chung — giả định câu đó vẫn dùng được cho người. Sinh 127 câu fallback THẬT từ output teacher (dùng note thật, khuôn mẫu `dg3_rewrite_fallback.py`), đọc tay đánh giá. FREE. Ngày: 2026-07-18.

## Phán quyết 1 dòng

**Giả định đứng NỬA VỜI.** Câu fallback **không gây hại** (không bịa nút mới, luôn có ý-định từ note — 0/127 rơi vào câu chung-chung-trơ). NHƯNG **giá trị điều hướng thấp**: ~80% chỉ **lặp lại mục tiêu** người dùng đã hỏi mà không chỉ vị trí/hình dạng, và ~20% **lặp động từ ngô nghê** ("Tap the option that would let you **tap**..."). Cộng với K2 (fallback chủ yếu thay NÚT THẬT), nhiều ca fallback **làm hướng dẫn tệ đi** chứ không cứu.

## Số liệu (127 câu fallback thật)

| Đặc điểm | Tỉ lệ | Nghĩa |
|---|---|---|
| Có ý-định từ note (không rơi câu trơ) | **100%** | tốt — câu trơ "Find the relevant control..." không hề bị kích hoạt |
| Câu **lặp động từ** rõ ("Tap...let you tap", "Enter...let you enter") | **20%** | đọc sượng, lỗi ngữ pháp |
| Intent bắt đầu bằng động-từ-hành-động (nguy cơ sượng) | 60% | do note teacher là câu mệnh lệnh, không phải mục tiêu |
| Còn lại: trơn ngữ pháp nhưng **lặp lại mục tiêu** (không chỉ vị trí) | ~80% | "vô dụng lịch sự" |

## Đọc tay — ba nhóm

**(a) Dùng tạm được (~mục tiêu rõ, ngữ pháp ổn):** ví dụ *"Tap the option on this screen that would let you add a new task."* — người dùng biết mình muốn thêm task, được nhắc tìm một control. Nhưng để ý: nó **chỉ nói lại đúng câu hỏi** ("How do I add a new task?"), không thêm thông tin *ở đâu / nút nào / hình gì*. Với người ĐANG KẸT thì đây là xác nhận mục tiêu, không phải chỉ đường.

**(b) Sượng vì lặp động từ (~20%):** note teacher vốn là mệnh lệnh ("Tap on the field to edit the hours") → sinh ra *"Tap the option that would let you **tap on the field** to edit the hours."* / *"Enter the option that would let you **enter** the new start time."* Đọc lủng củng, lộ máy-móc.

**(c) Circular — điểm yếu sâu nhất:** gần như MỌI câu có dạng "tap the option that would let you {mục-tiêu}", mà mục-tiêu = chính việc người dùng hỏi. Không câu nào chỉ **vị trí** (góc trên, thanh dưới) hay **hình dạng** (nút dấu cộng, biểu tượng bánh răng). Người dùng kẹt vì không biết chạm ĐÂU — câu fallback không trả lời "ở đâu".

## Nối với K1/K2 — vì sao đây là vấn đề thật

K2 cho thấy các bước bị đánh "bịa" **hầu hết là NÚT THẬT** (icon `+`, ADD LOCATION...). Nghĩa là fallback thường **thay một tham chiếu cụ thể-đúng** ("Tap +" / "Tap Add location") bằng một câu **mơ hồ-lặp-lại** ("Tap the option that would let you add a new task"). → với những ca đó, fallback **làm hướng dẫn TỆ ĐI**, đúng nỗi lo "đổi sai-nguy-hiểm lấy vô-dụng-lịch-sự". Chuỗi K1+K2+VIỆC1 cùng chỉ một gốc: **fallback kích hoạt quá nhiều vì matcher đánh oan, và bản thân câu fallback giá trị thấp.**

## Hệ quả / cách sửa

1. **Sửa gốc = fallback ÍT ĐI.** Cách tăng "usefulness" hiệu quả nhất không phải viết câu hay hơn, mà là **đừng fallback nhầm nút thật** — tức nâng matcher (OCR + so-chuỗi + từ-điển-icon, report/73/75). Giảm kích hoạt oan → giữ được tham chiếu cụ thể-đúng.
2. **Vá ngữ pháp:** `clean_intent_clause` cần cắt thêm động-từ-mệnh-lệnh dẫn đầu ("tap on", "select", "enter", "move") để không sinh "let you tap...". Rẻ, sửa ngay được.
3. **Thêm chỉ dẫn vị trí/hình khi có thể:** dùng bbox nút (góc/thanh) hoặc loại-phần-tử để câu bớt circular ("nút ở thanh dưới cùng cho phép..."). Cần thông tin vị trí — làm được vì bbox có sẵn.
4. **Đa dạng câu (Vòng B, 10 biến thể)** vẫn nên làm, nhưng **thứ yếu** so với (1)/(2) — vì vấn đề là NỘI DUNG circular, không phải chỉ lặp-chữ.

## Giới hạn (khai thẳng)

- **Đánh giá của một người (tôi), không phải mẫu người dùng thật** — đủ để KILL/giữ giả định, chưa phải con số có κ. Nếu thầy cho phép, một mẫu-người-nhỏ (5 người × 20 câu) sẽ thành bằng chứng khai được (đúng câu hỏi thầy #2 ở report/71).
- **Một miền app** (quản lý dự án/chi phí), một teacher. Note teacher ở đây khá đầy đủ nên 0% rơi câu-trơ; miền khác note nghèo hơn có thể rơi câu-trơ nhiều → tệ hơn.

> Tóm: fallback **an toàn nhưng yếu** — không bịa, nhưng chủ yếu nói lại mục tiêu, 1/5 sượng ngữ pháp, và (vì K2) thường thay nút thật bằng câu mơ hồ. Giả định "mô tả chung chung vẫn dùng được" **không đổ hẳn nhưng lung lay**. Sửa hiệu quả nhất = fallback ít đi (nâng matcher) + vá ngữ pháp + thêm chỉ-vị-trí, chứ không chỉ đa dạng câu.
