# RARR: Researching and Revising What Language Models Say, Using Language Models

- **Link:** https://aclanthology.org/2023.acl-long.910/
- **Venue/năm:** ACL 2023 — ✔ đã xác minh (report/45, nguồn 15)
- **Vai trong luận văn:** tiền lệ **sửa theo nguồn ngoài + minimal-edit** — §4.5 (khớp triết lý "describe-don't-guess").

## Paper này nói gì (cho người mới)
RARR lấy **đầu ra đã sinh** của một mô hình, đi **tìm bằng chứng ngoài** (retrieval), rồi **chỉ sửa những chỗ không được bằng chứng ủng hộ** — cố **giữ nguyên phần còn lại** càng nhiều càng tốt. Đây là "hiệu đính có dẫn nguồn" sau khi sinh, áp cho **bất kỳ** mô hình sinh nào (model-agnostic).

## Điểm cần biết
- **Hậu-kiểm + sửa tối thiểu** dựa trên **nguồn ngoài** (không grounding lúc sinh).
- **Model-agnostic** — chạy trên output của mô hình bất kỳ.
- Triết lý "sửa ít nhất, giữ nguyên phần đúng" ≈ **"describe-don't-guess"** của ta (chỉ đụng bước ảo giác).

## Dùng refer gì cho bài của tôi
- Trụ cho **tính model-agnostic** của lớp trung-thực-hoá (chạy sau, không train, đổi model được).
- Trụ cho triết lý **chỉ can thiệp bước ảo giác** (fallback), giữ nguyên bước đúng.
- Cùng CoVe/CaLM/CRITIC trong danh sách "hậu-kiểm chính danh" ở §4.5.
