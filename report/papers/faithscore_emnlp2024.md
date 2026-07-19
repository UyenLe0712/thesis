# FaithScore: Fine-grained Evaluations of Hallucinations in Large Vision-Language Models

- **Link:** https://aclanthology.org/2024.findings-emnlp.290/
- **Venue/năm:** Findings of EMNLP 2024 — ✔ đã xác minh (report/45, nguồn 16)
- **Vai trong luận văn:** **đối thủ gần nhất trên trục đánh giá** — phải phân định chủ động (§7.2, §9).

## Paper này nói gì (cho người mới)
FaithScore đo **độ trung thực** của câu trả lời tự do mà một mô hình ngôn ngữ-thị giác (VLM) sinh ra so với **ảnh đầu vào**, mà **không cần đáp án mẫu** (reference-free). Cách làm: (1) tách câu trả lời thành các câu con; (2) rút ra các **"atomic facts"** (khẳng định nhỏ nhất, ví dụ "có một con chó màu nâu"); (3) **kiểm từng khẳng định** xem có khớp ảnh không.

## Điểm cần biết
- Cùng họ ý tưởng với ta: **"sinh trước → tách nhỏ → kiểm từng phần"** (decompose-then-verify, hậu-kiểm).
- Nhưng nó **tự soi lại bằng chính mô hình thị giác** (self-check trên ảnh) → dễ kế thừa lỗi thị-giác của model, nên **bản thân nó cũng cần validate** (và họ validate bằng human-correlation).
- Được bình duyệt venue lớn → chứng minh hướng reference-free hậu-kiểm là **chính danh 2024**.

## Dùng refer gì cho bài của tôi
- **Định vị hướng đi:** "reference-free faithfulness cho VLM là hướng đã được công nhận" → ta không lạc dòng.
- **Điểm phân định (bắt buộc viết trước khi giám khảo hỏi):** ta đối chiếu với **View Hierarchy CÓ CẤU TRÚC + matcher tất định**, KHÔNG tự-soi-bằng-VLM → tránh được điểm yếu "self-check kế thừa lỗi".
- Dùng để trả lời đòn *"metric reference-free vẫn phải có human-correlation"*: ta hạ human-correlation xuống future-work *có chủ đích* dưới khung measurement-theory.
