# Chain-of-Verification Reduces Hallucination in Large Language Models (CoVe)

- **Link:** https://aclanthology.org/2024.findings-acl.212/
- **Venue/năm:** Findings of ACL 2024 — ✔ đã xác minh (report/45, nguồn 17)
- **Vai trong luận văn:** tiền lệ **paradigm hậu-kiểm (sinh → kiểm)** — §4.5.

## Paper này nói gì (cho người mới)
CoVe cho mô hình làm 4 bước: (1) **viết nháp** câu trả lời; (2) **tự đặt câu hỏi kiểm chứng** cho từng chi tiết; (3) **trả lời các câu hỏi kiểm** đó; (4) **viết lại** bản cuối đã sửa theo kết quả kiểm. Nhờ tách bước "kiểm" ra riêng, ảo giác giảm trên nhiều loại tác vụ.

## Điểm cần biết
- Là **generate-then-verify** (sinh trước, kiểm sau) — cùng khung với pipeline của ta.
- **Lưu ý:** CoVe kiểm bằng *chính mô hình* (internal), KHÁC ta kiểm bằng **nguồn ngoài có cấu trúc (VH)**.
- Chứng minh **post-hoc verification vẫn hiệu quả 2024**, không lỗi thời.

## Dùng refer gì cho bài của tôi
- Trong §4.5: liệt kê cùng FaithScore/RARR/CaLM/CRITIC làm bằng chứng "hậu-kiểm là paradigm chính danh".
- Điểm phân định: ta mạnh hơn ở chỗ **tín hiệu kiểm đến từ NGUỒN NGOÀI tất định**, không phải mô hình tự soi.
