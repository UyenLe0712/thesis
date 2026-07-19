# Generative Value Learning (GVL): Vision-Language Models are In-Context Value Learners

- **Link:** https://generative-value-learning.github.io/ · (arXiv 2411.04549)
- **Venue/năm:** ICLR 2025 (Google DeepMind / UPenn / Stanford) — ✔ đã xác minh peer-reviewed (report/45, nguồn 10)
- **Vai trong luận văn:** trụ **bổ trợ** cho ý "**xáo-frame → suy lại thứ tự/tiến độ** là hướng VLM khả thi" — §4.3, §4.4.

## Paper này nói gì (cho người mới)
GVL cho VLM ước lượng **mức độ hoàn thành tác vụ** dọc theo một chuỗi khung hình. Phát hiện thú vị: nếu đưa chuỗi **theo đúng thứ tự thời gian**, mô hình làm **kém** (vì các khung liền nhau quá giống nhau, mô hình "lười"); nhưng nếu **xáo trộn thứ tự** rồi bắt mô hình **suy lại**, nó dùng khả năng grounding tốt hơn và làm **tốt hơn**.

## Điểm cần biết
- **Peer-reviewed ICLR 2025** (chắc chắn) → trụ vững, khác TOMATO (đang cần kiểm venue).
- Ý cốt: **"đưa ảnh xáo trộn rồi bắt suy lại thứ tự/tiến độ" là phương pháp VLM hợp lệ** — đúng tinh thần Stage-0 của ta (N màn xáo → suy thứ tự).

## Dùng refer gì cho bài của tôi
- **Trụ peer-reviewed** cho thiết kế Stage-0: "xáo trộn màn rồi buộc hệ khôi phục" là hướng có tiền lệ.
- Dùng thay/bổ trợ khi TOMATO chưa chắc venue.
- Củng cố: làm việc với **tập ảnh xáo trộn** không phải ý lạ, mà là hướng đang được nghiên cứu 2025.
