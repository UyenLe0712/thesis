# ALOHa: A New Measure for Hallucination in Captioning Models

- **Link:** https://aclanthology.org/2024.naacl-short.30/
- **Venue/năm:** NAACL 2024 (Short Papers) — ✔ đã xác minh (report/45, nguồn 20)
- **Vai trong luận văn:** nền cho công thức **Độ trung thực (Faithfulness)** ở §5.1.

## Paper này nói gì (cho người mới)
Khi một mô hình "chú thích ảnh" (image captioning) viết ra một câu, nó có thể nhắc tới **đồ vật không có trong ảnh** — đó là *ảo giác*. ALOHa là một cách **đo mức ảo giác** đó. Cách làm: (1) dùng một LLM **rút ra các danh từ/đồ vật** mà câu nhắc tới; (2) **so nghĩa** (semantic similarity) từng đồ vật đó với danh sách đồ vật thật trong ảnh (từ nhãn tham chiếu + bộ dò vật); (3) ghép cặp tối ưu (Hungarian) — đồ vật nào không khớp gì thì tính là *bịa*.

## Điểm cần biết
- Là **hậu-kiểm**: sinh câu trước, rồi mới đối chiếu với nguồn ngoài (không sửa lúc sinh).
- Dùng **so nghĩa mở** (open-vocabulary) thay vì danh sách cứng → bắt được nhiều loại ảo giác hơn thước cũ CHAIR (bắt thêm ~13,6% trên HAT, ~30,8% trên nocaps).
- Triết lý cốt lõi: *"đối chiếu thứ mô hình nói với một nguồn sự-thật độc lập"*.

## Dùng refer gì cho bài của tôi
- **Trụ chính** cho định nghĩa **Faith = 1 − (bước ảo giác)/(bước nhắc nút)**: ta thay "đồ vật trong ảnh" bằng "nút trong View Hierarchy", giữ nguyên ý "so nghĩa với nguồn ngoài".
- Biện minh chọn **so-embedding thay vì so mặt chữ** (Save ≈ Lưu).
- Khai thẳng: ta *thích nghi* ALOHa từ caption → GUI; độ mới của ta là **neo bằng VH có cấu trúc** (§5.3, §9).
