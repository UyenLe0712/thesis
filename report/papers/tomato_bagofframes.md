# TOMATO: Assessing Visual Temporal Reasoning Capabilities in Multimodal Foundation Models

- **Link:** https://openreview.net/forum?id=fCi4o83Mfs · arXiv: https://arxiv.org/abs/2410.23266
- **Venue/năm:** **ICLR 2025 (Poster)** — ✔ đã xác nhận (R-07: OpenReview `fCi4o83Mfs`; arXiv 2410.23266). Khi trích trạng thái ghi rõ **"Poster"**.
- **Vai trong luận văn:** bằng chứng **VLM yếu suy luận thứ tự / "bag-of-frames"** → module sắp-thứ-tự KHÔNG thừa — §4.3, §4.4, §12.

## Paper này nói gì (cho người mới)
TOMATO kiểm xem các mô hình đa phương thức có **thật sự hiểu thứ tự thời gian** của một chuỗi ảnh/khung hình không. Kết quả: chúng **nhận ra sự kiện trong từng khung riêng lẻ tốt**, nhưng **kém khi phải hiểu chuỗi có thứ tự** — khoảng cách với người tới **57,3%** ở mô hình tốt nhất. Nhiều benchmark cũ **thổi phồng** năng lực này vì câu hỏi giải được từ một/vài khung lẻ.

## Điểm cần biết
- Thuật ngữ **"bag-of-frames"**: mô hình đối xử chuỗi ảnh như *túi ảnh rời*, gần như bỏ qua thứ tự.
- Có số minh hoạ mạnh (bài liên quan: GPT-4o ~24% vs người ~80% khi sắp ảnh xáo trộn).
- ⚠ *Sắc thái (R-07):* dùng để nói VLM **yếu** ở suy-luận-thứ-tự → Stage-0 là **scaffold có cấu trúc**; **KHÔNG** nói long-context "bất lực tuyệt đối" (CoT nội-model có thể thay module).

## Dùng refer gì cho bài của tôi
- **Trụ** chống đòn *"long-context nuốt N ảnh là tự sắp được, module Stage-0 thừa"*: VLM KHÔNG dùng thứ tự thật.
- Củng cố **cổng K-pair** (phải đo acc so-cặp thô > 0,5).
- Đi kèm **GVL (ICLR 2025)** — cả hai peer-reviewed → trụ đôi cho "xáo-frame → suy-thứ-tự là hướng khả thi + VLM yếu bẩm sinh".
