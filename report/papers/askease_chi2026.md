# AskEase — From Struggle to Success: Context-Aware Guidance for Screen Reader Users in Computer Use

- **Link:** https://dl.acm.org/doi/full/10.1145/3772318.3790661 · (arXiv 2601.18092)
- **Venue/năm:** **CHI 2026**, DOI 10.1145/3772318.3790661 — ✔ đã xác minh (report/45, nguồn 24)
- **Vai trong luận văn:** **bài gần nhất trên trục "sinh hướng dẫn cho người"** → rủi ro novelty cao nhất, phải phân định (§9, §12).

## Paper này nói gì (cho người mới)
AskEase là trợ lý AI sinh **hướng dẫn từng bước thân-thiện-trình-đọc-màn-hình** cho **người khiếm thị** đang dùng máy tính. Nó lấy ngữ cảnh từ **trạng thái màn hình LIVE** (qua API NVDA) + **tài liệu phần mềm** (RAG), đánh giá bằng **user-study 12 người** + test 45 tác vụ (thành công 96,6%).

## Điểm cần biết (vì sao KHÔNG scoop bài của ta)
- **Đầu vào khác:** AskEase là trợ-lý *LIVE* có trạng thái runtime + ý định người dùng; ta sinh từ **ảnh tĩnh + câu hỏi**.
- **Đánh giá khác:** AskEase dùng *user-study HCI* (người hoàn thành = gold ngầm); ta dùng **no-gold neo View Hierarchy** + đo tỉ-lệ-ảo-giác.
- **Thành phần khác:** AskEase **KHÔNG** hậu-kiểm đối chiếu VH, **KHÔNG** có nhánh sắp-thứ-tự-màn; grounding bằng RAG-tài-liệu.
- **Điểm chung tích cực:** cùng theo **abstention / "nêu-không-chắc-thay-vì-đoán"** → hậu thuẫn "describe-don't-guess" của ta.

## Dùng refer gì cho bài của tôi
- **Bắt buộc** có 1 đoạn phân-định AskEase trong related-work (giám khảo sẽ hỏi "khác AskEase chỗ nào").
- Dùng **hậu thuẫn niche on-device / trợ năng** — nơi lớp trung-thực-hoá có giá trị nhất.
- Trả lời đòn "grounded-gen như AskEase là mặc-định-ngành": ta = *chế-độ-ĐO*, deploy có thể grounded (§4.5).
