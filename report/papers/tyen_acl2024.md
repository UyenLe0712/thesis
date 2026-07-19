# LLMs Cannot Find Reasoning Errors, but Can Correct Them Given the Error Location (Tyen et al.)

- **Link:** https://aclanthology.org/2024.findings-acl.826.pdf
- **Venue/năm:** Findings of ACL 2024 — ✔ đã xác minh (report/45, nguồn 19)
- **Vai trong luận văn:** tinh chỉnh phân định tự-sửa — **"tìm lỗi" mới là chỗ khó, không phải "sửa lỗi"** — §4.5.

## Paper này nói gì (cho người mới)
Bài tách đôi năng lực: (1) **tìm ra chỗ sai** và (2) **sửa chỗ sai đã biết**. Phát hiện: LLM **kém ở (1)** nhưng **khá ở (2)** — nếu **ai đó chỉ cho nó vị trí lỗi** (một tín hiệu ngoài), nó sửa rất tốt. Bộ định-vị-lỗi ngoài (kể cả một bộ phân loại nhỏ) còn tốt hơn để mô hình tự dò.

## Điểm cần biết
- Củng cố: **tín hiệu định-vị-lỗi từ bên ngoài** làm việc sửa trở nên đáng tin.
- Khớp thiết kế của ta: **matcher (bên ngoài) chỉ ra "bước này bịa"**, rồi mới xử lý — thay vì để mô hình tự dò.

## Dùng refer gì cho bài của tôi
- Trụ cho vai của **bước 2 (đối chiếu ngữ nghĩa)**: nó chính là "bộ định-vị-lỗi ngoài" — đúng thứ Tyen chứng minh là hữu ích.
- Cùng Huang/CRITIC làm bộ ba lập luận "external-signal > intrinsic" trong §4.5.
