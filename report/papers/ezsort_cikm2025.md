# EZ-Sort: Efficient Pairwise Comparison via Zero-Shot CLIP-Based Pre-Ordering and Human-in-the-Loop Sorting

- **Link:** https://dl.acm.org/doi/10.1145/3746252.3760848 · arXiv 2508.21550
- **Venue/năm:** **CIKM 2025** (peer-reviewed) — ✔ đã xác nhận (R-07, DOI 10.1145/3746252.3760848).
- **Vai trong luận văn:** **prior-art bình duyệt 2025** cho "dùng mô hình thị giác + so-cặp để sắp ảnh" — phải phân định (§4.4).

## 1. Bối cảnh & vấn đề
Sắp một tập lớn đối tượng bằng **so-cặp** thì chính xác nhưng **tốn** (số cặp tăng theo bình phương). Nếu để người so-cặp thủ công thì càng đắt. EZ-Sort tìm cách **giảm số lần so-cặp** mà vẫn giữ độ tin cậy.

## 2. Ý tưởng chính (dễ hiểu)
Hai tầng: (1) **CLIP (mô hình ảnh-text) sắp thô trước** một cách zero-shot để có thứ tự ban đầu tương đối; (2) rồi **con người chỉ so-cặp ở những chỗ thật sự cần** (merge-sort có hướng dẫn bởi **độ bất định**), tập trung công sức vào các cặp khó/gần nhau thay vì so hết. Kết quả: **ít cặp phải so hơn** và **độ đồng thuận giữa người chấm tăng**.

## 3. Điểm mạnh & giới hạn (so với bài của ta)
- **Mạnh:** cho thấy "pre-order bằng mô hình thị giác + so-cặp có chọn lọc theo độ-bất-định" là hướng hiệu quả, được bình duyệt 2025.
- **Khác ta rõ:** (a) EZ-Sort **có người trong vòng lặp** lúc sắp; ta **tự động hoàn toàn** ở thì suy luận; (b) miền ảnh tổng quát, không phải **màn GUI**; (c) EZ-Sort tối ưu *chi phí gán nhãn*, ta thì **gắn ordering vào sinh hướng dẫn** + partial-order-from-gold.

## 4. Dùng refer gì cho bài của tôi
- **Bắt buộc trích** trong related-work Stage-0 (§4.4) để không bị nói "chỉ áp method có sẵn".
- Làm mốc phân định độ mới: ta khác ở **tự-động + miền GUI + mục-tiêu-điều-kiện-hoá + gắn sinh-hướng-dẫn**.
- Cùng Dodgersort hậu thuẫn ý "sắp-cặp có tính tới **độ bất định**" (nối M2: trọng-số không tin confidence tự-khai).
