# CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing (Gou et al.)

- **Link:** https://arxiv.org/abs/2305.11738
- **Venue/năm:** ICLR 2024 — ✔ đã xác minh (report/45, nguồn 13)
- **Vai trong luận văn:** bằng chứng **sửa bằng TÍN HIỆU NGOÀI thì hợp lệ** (bổ sung cho Huang) — §4.5.

## Paper này nói gì (cho người mới)
CRITIC cho LLM **tự sửa nhờ tương tác với công cụ ngoài** (công cụ tìm kiếm, trình chạy mã…) chứ không tự phán một mình. Kết luận cốt lõi: **phản hồi từ bên ngoài là thiết yếu** để mô hình cải thiện — nếu chỉ tự soi thì không đáng tin.

## Điểm cần biết
- Là mặt **tích cực** đối lại Huang (ICLR 2024): *ngoài* thì được, *nội tại* thì không.
- Vẫn là **generate-then-verify** (sinh trước, kiểm/sửa bằng công cụ ngoài sau).
- Bình duyệt ICLR → dùng làm **trụ** (không phải preprint).

## Dùng refer gì cho bài của tôi
- Ghép cặp với Huang để **phân định**: "chỉ intrinsic bị bác; external-signal correction (như của chúng tôi) có tiền lệ bình duyệt CRITIC".
- Trụ cho luận điểm: matcher-đối-chiếu-VH của ta = một dạng **external-signal correction** hợp lệ.
