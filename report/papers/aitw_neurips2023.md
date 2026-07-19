# Android in the Wild (AITW): A Large-Scale Dataset for Android Device Control

- **Link:** https://arxiv.org/abs/2307.10088
- **Venue/năm:** NeurIPS 2023 (Datasets & Benchmarks).
- **Vai trong luận văn:** **nguồn ngưỡng dung sai 14%** cho "bấm đúng chỗ" (§5.2, §5.3) — trích bắt buộc.

## Paper này nói gì (cho người mới)
Bộ dữ liệu lớn về **điều khiển thiết bị Android**: các chuỗi thao tác (chạm, vuốt, gõ) trên nhiều app/website. Khi chấm một hành động "chạm" là đúng hay sai, họ dùng **ngưỡng dung sai**: điểm chạm dự đoán chỉ cần nằm trong **~14% khoảng cách** so với vị trí đúng là tính "trúng" (vì không cần chính xác tuyệt đối từng pixel).

## Điểm cần biết
- Là **nguồn gốc con số 14%** mà ta dùng cho point-in-bbox / Step-SR.
- Bình duyệt NeurIPS 2023.
- ⚠ Chuẩn grounding **mới hơn (2025)** là point-in-GT-bbox nguyên bản → ta để 14% làm **biến-thể-đối-chứng**, không làm định nghĩa chính (§5.3).

## Dùng refer gì cho bài của tôi
- **Trích bắt buộc** khi nêu ngưỡng dung sai 14% (Step-SR, đối chứng grounding).
- Làm dataset đối chứng thêm là **tuỳ chọn** (không bắt buộc).
