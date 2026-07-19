# CaLM: Contrasting Large and Small Language Models to Verify Grounded Generation

- **Link:** https://arxiv.org/abs/2406.05365
- **Venue/năm:** ACL 2024 — ✔ đã xác minh (report/45, nguồn 4)
- **Vai trong luận văn:** bằng chứng **hậu-kiểm grounded generation bằng nguồn ngoài vẫn phát triển mạnh 2024** — §4.5.

## Paper này nói gì (cho người mới)
CaLM kiểm một câu trả lời **đã được "neo" vào tài liệu (grounded)** xem nó có **thật sự nhất quán với nguồn được trích** không. Ý tưởng: một câu trả lời đáng tin phải suy được **chỉ từ nguồn ngoài đã dẫn**. Mô hình nhỏ (dựa vào tài liệu) được dùng để **kiểm chéo** mô hình lớn (hay dựa vào trí nhớ tham số).

## Điểm cần biết
- Cho thấy ngành **tách bạch** rõ: bước **sinh** ≠ bước **kiểm-đối-chiếu-nguồn**.
- Cho gain đo được (khoảng 1,5–7% tuyệt đối) **không cần fine-tune** → hậu-kiểm là phương pháp làm việc thật.
- Đúng logic ta dùng: **đối chiếu với nguồn ngoài thay vì tin trí nhớ mô hình**.

## Dùng refer gì cho bài của tôi
- Bằng chứng **2024** rằng "hậu-kiểm đối-chiếu-nguồn-ngoài" là **hướng đang phát triển**, không phải chắp vá cũ.
- Củng cố §4.5 điểm 4 (post-hoc verify chính danh) — trả lời đòn "sao không grounded-gen".
