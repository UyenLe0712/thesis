# Sort Story: Sorting Jumbled Images and Captions into Stories (Agrawal et al.)

- **Link:** https://aclanthology.org/D16-1091/ · arXiv: https://arxiv.org/abs/1606.07493 · ⚠ *xác nhận link anthology trước khi in*
- **Venue/năm:** EMNLP 2016.
- **Vai trong luận văn:** **prior-art kinh điển** của bài toán "sắp ảnh xáo trộn thành trình tự" — phải thừa nhận (§4.4, §9).

## 1. Bối cảnh & vấn đề
Cho một **tập ảnh (và/hoặc chú thích) bị xáo trộn** của cùng một câu chuyện, hãy **sắp lại đúng thứ tự** để thành một câu chuyện mạch lạc. Đây là bài toán "temporal ordering" trên dữ liệu thị giác — rất gần với **Stage-0** của luận văn (N màn xáo → khôi phục thứ tự), chỉ khác miền (truyện ảnh đời thường vs màn GUI).

## 2. Ý tưởng chính (dễ hiểu)
Họ học các **đặc trưng** (từ ảnh + text) rồi huấn luyện mô hình dự đoán quan hệ thứ tự. Một kỹ thuật quan trọng: thay vì đoán cả dãy một lần, họ dùng **các phán đoán theo cặp** ("ảnh nào trước?") rồi **bỏ phiếu/tổng hợp** thành thứ tự cuối — ý tưởng cùng họ với pairwise + aggregation mà ta dùng.

## 3. Cách đo & kết quả chính
- Chất lượng sắp xếp được đo bằng **tương quan thứ hạng Spearman** (và các độ đo trùng-cặp) so với thứ tự vàng.
- Cho thấy kết hợp tín hiệu ảnh + ngôn ngữ + học theo-cặp giúp sắp tốt hơn baseline.

## 4. Điểm mạnh & giới hạn (so với bài của ta)
- **Mạnh:** đặt nền cho "sắp chuỗi thị giác bằng so-cặp + tổng hợp".
- **Khác ta:** (a) miền truyện ảnh, không phải GUI; (b) dùng **Spearman/Kendall toàn phần** (phạt mọi cặp), còn ta dùng **partial-order chỉ phạt cặp bắt buộc** (Fagin/Lapata); (c) họ **không** điều-kiện-hoá theo *mục tiêu tác vụ* và **không** gắn với *sinh hướng dẫn*.

## 5. Dùng refer gì cho bài của tôi
- **Bắt buộc trích** trong related-work sắp-ảnh để thể hiện ta biết prior-art (chống đòn "chưa đọc nền").
- Làm **điểm tựa để phát biểu độ mới** (§4.4): miền GUI + điều-kiện-mục-tiêu + partial-order-from-gold + gắn-sinh-hướng-dẫn + 5-cue — những thứ Sort-Story không có.
- Ghi rõ: ta **không** claim mới ở "ý tưởng sắp ảnh" (đã có từ 2016), mà ở tổ-hợp trên.
