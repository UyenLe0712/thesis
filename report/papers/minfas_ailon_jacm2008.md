# Aggregating Inconsistent Information: Ranking and Clustering (Ailon, Charikar, Newman) — minimum feedback arc set

- **Link:** https://dl.acm.org/doi/10.1145/1411509.1411513 · ⚠ *xác nhận link trước khi in*
- **Venue/năm:** JACM 2008 (bản hội nghị: STOC 2005).
- **Vai trong luận văn:** nền cho bước **phá vòng mâu thuẫn** bằng *minimum feedback arc set* — §4.3(c).

## Paper này nói gì (cho người mới)
Khi các phán đoán so-cặp **mâu thuẫn** (A trước B, B trước C, nhưng C lại trước A → thành vòng), ta không xếp thành hàng được. **Feedback arc set** là tập cạnh mà nếu **bỏ đi** thì đồ thị hết vòng; **minimum** = bỏ **ít cạnh nhất**. Bài đưa thuật toán xấp xỉ để làm việc này.

## Điểm cần biết
- Bài toán **NP-đầy đủ** → thực tế phải dùng **heuristic / trọng số**, không giải tối ưu tuyệt đối.
- Là **công thức chuẩn** cho gộp-hạng từ so-cặp (giảm số "upset").
- Cho phép Stage-0 vẫn ra thứ tự dù VLM phán mâu thuẫn.

## Dùng refer gì cho bài của tôi
- **Trụ** cho §4.3(c): phá vòng bằng min-FAS.
- Biện minh **M2**: vì bài NP-đầy-đủ nên phải dùng **trọng số** (margin-Copeland/self-consistency), không thể "cắt cạnh ít-chắc-nhất" ngây thơ.
- Khẳng định độ mới của ta KHÔNG ở thuật toán (đã có Ailon) mà ở **miền GUI + trọng số + partial-order-from-gold** (§4.4).
