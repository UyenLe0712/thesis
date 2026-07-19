# AndroidControl (On the Effects of Data Scale on UI Control Agents) — Li et al.

- **Link:** https://arxiv.org/abs/2406.03679
- **Venue/năm:** **NeurIPS 2024 Datasets & Benchmarks** (Google DeepMind). Giấy phép **CC0** (peer-reviewed).
- **Vai trong luận văn:** bộ dữ liệu cho **nhánh NHIỀU MÀN** + đo **Step-SR** (§3.2).

## Paper này nói gì (cho người mới)
Bộ dữ liệu **người thật** thao tác trên điện thoại Pixel suốt ~1 năm, ghi lại **từng bước**. Mỗi *quy trình* (episode) có một **mục tiêu** (câu mô tả tác vụ) và một **quỹ đạo vàng** (chuỗi thao tác đúng: click(x,y), scroll, type…). Có **15.283 quy trình / 833 app**, trung bình **~5,5 bước** (p95 = 13), **8 loại thao tác**.

## Điểm cần biết
- **CÓ quỹ đạo vàng** → cho phép đo *sắp đúng thứ tự* (τ) và *làm tới đích* (Step-SR).
- **Peer-reviewed NeurIPS D&B** → trụ dữ liệu vững.
- ⚠ Tập **test = 1.542** (KHÔNG phải "2.855" — đừng in nhầm; report/44 §8).
- ⚠ Chưa có **histogram độ dài theo N** → phải tự đếm (cổng KN).

## Dùng refer gì cho bài của tôi
- Nguồn cho toàn bộ **nhánh nhiều màn**: xáo trộn màn → khôi phục → chấm bằng gold.
- Trụ cho **Step-SR** (§5.2) — "trục tham chiếu chuẩn ngành", không claim leaderboard.
- Ví dụ thật `ep2_14851` (tạo lối tắt PDF Drive) dùng minh hoạ đầu-cuối (§3.2, §6.2).
