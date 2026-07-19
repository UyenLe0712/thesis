# Large Language Models Cannot Self-Correct Reasoning Yet (Huang et al.)

- **Link:** https://arxiv.org/abs/2310.01798
- **Venue/năm:** ICLR 2024 — ✔ đã xác minh (report/45, nguồn 12 & 21)
- **Vai trong luận văn:** phân định **tự-sửa NỘI TẠI (bị bác) vs sửa bằng tín hiệu NGOÀI (hợp lệ)** — §4.5, §7.

## Paper này nói gì (cho người mới)
Nhiều người tưởng cứ bảo LLM "hãy tự kiểm lại và sửa" là nó tốt lên. Bài này chứng minh **ngược lại**: khi mô hình **chỉ dựa vào phán đoán của chính nó** (không có tín hiệu ngoài), việc tự-sửa **làm kết quả TỆ ĐI**, không tốt lên (ví dụ GPT-4 trên GSM8K tụt điểm sau khi "tự sửa").

## Điểm cần biết
- Kết quả tiêu cực **chỉ áp cho *intrinsic self-correction*** (tự-sửa nội tại, không tín hiệu ngoài).
- Bài **để ngỏ**: nếu có **tín hiệu NGOÀI/oracle** thì sửa lại có ích — không nằm trong kết quả tiêu cực.
- Đây là bài rất hay bị dùng để "đập" các hệ tự-sửa → ta phải phân định trước.

## Dùng refer gì cho bài của tôi
- **Lá chắn quan trọng:** khi giám khảo nói *"tự-sửa đã bị chứng minh vô dụng"*, ta đáp: lớp trung-thực-hoá dùng **tín hiệu NGOÀI, phi-LLM, tất định** (so-embedding vs View Hierarchy) → KHÔNG phải intrinsic self-correction → không bị bài này bác.
- Củng cố quyết định **bỏ "correction" cũ** (đoán nút gần nhất = tự-suy-đoán không tín hiệu tin cậy → silent error).
