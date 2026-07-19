# Rank Aggregation Methods for the Web (Dwork, Kumar, Naor, Sivakumar) — phương pháp Copeland

- **Link:** https://dl.acm.org/doi/10.1145/371920.372165 · ⚠ *xác nhận link trước khi in*
- **Venue/năm:** WWW 2001.
- **Vai trong luận văn:** nền cho bước **tổng hợp Copeland** (từ so-cặp → thứ tự tổng thể) — §4.3(b).

## Paper này nói gì (cho người mới)
Khi có nhiều "phiếu bầu" xếp hạng khác nhau (hoặc nhiều phán đoán so-cặp), làm sao gộp thành **một thứ tự chung** hợp lý? Bài kinh điển này bàn các **phương pháp tổng hợp hạng** cho web, trong đó có ý tưởng kiểu **Copeland**: mỗi đối tượng được tính điểm bằng **số "trận thắng"** (số cặp mà nó đứng trước), rồi xếp theo điểm giảm dần.

## Điểm cần biết
- Copeland = **đếm trận thắng** → đơn giản, bền, dễ giải thích.
- Là nền **rank aggregation** được trích rộng rãi.
- Xử lý được cả khi các phán đoán không hoàn toàn nhất quán (kết hợp với phá vòng — xem Ailon).

## Dùng refer gì cho bài của tôi
- **Trụ** cho Định nghĩa 4.2 (điểm Copeland) ở §4.3.
- Khẳng định: bước tổng hợp của ta **không phải tự chế** mà dựa nền peer-reviewed kinh điển.
- ⚠ Nên đối chiếu bản PDF gốc khi trích câu về Copeland (report/39 có ghi caveat này).
