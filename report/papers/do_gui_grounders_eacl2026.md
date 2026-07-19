# Do GUI Grounders Truly Understand UI Elements? (Jandial, Li, Wagle, Koishida)

- **Link:** https://aclanthology.org/2026.findings-eacl.144/
- **Venue/năm:** **Findings of EACL 2026** — ✔ đã xác minh (report/45, nguồn 22)
- **Vai trong luận văn:** hậu thuẫn "**không tin lời model, phải đối chiếu nguồn cấu trúc**" — §9, §4.5.

## Paper này nói gì (cho người mới)
Các mô hình "định vị nút GUI" (GUI grounders) trông có vẻ giỏi, nhưng bài này cho thấy chúng **không thực sự hiểu** phần tử giao diện: chúng dựa vào **khớp mẫu hời hợt**, cho kết quả **thiếu nhất quán** khi đổi cách diễn đạt cùng một nút, và một "agent chẩn đoán" có thể khiến chúng **sai tới 84%** bằng các chỉ dẫn hợp lệ nhưng lạ.

## Điểm cần biết
- Bằng chứng **2026, peer-reviewed**: đầu ra của model GUI **không đáng tin ở mặt chữ** → cần **kiểm bằng nguồn ngoài**.
- Điểm số benchmark **thổi phồng** năng lực thật của grounder.
- Bài này về **chẩn đoán grounder cho agent desktop**, KHÁC bài toán sinh-hướng-dẫn-cho-người của ta → **không scoop**.

## Dùng refer gì cho bài của tôi
- Trụ **2026** cho luận điểm: "phải hậu-kiểm đối chiếu nguồn cấu trúc, không tin model tự khai".
- Củng cố việc ta dùng **matcher tất định vs VH** thay vì tin tên nút model sinh.
- Phân định setup: họ = chẩn đoán grounder/agent; ta = sinh hướng dẫn cho người + no-gold eval.
