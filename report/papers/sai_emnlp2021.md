# Perturbation CheckLists for Evaluating NLG Evaluation Metrics (Sai et al.)

- **Link:** https://aclanthology.org/2021.emnlp-main.575/ · ⚠ *xác nhận link/số trang trước khi in*
- **Venue/năm:** EMNLP 2021.
- **Vai trong luận văn:** **trụ chính** cho cách validate thước đo bằng **nhiễu loạn (perturbation)** — §7.2.

## Paper này nói gì (cho người mới)
Muốn biết một **thước đo** (metric) có tốt không, đừng chỉ so nó với điểm người chấm. Hãy **cố ý bơm những lỗi đã biết** vào văn bản rồi xem thước có phản ứng đúng không: nếu ta làm câu tệ đi mà điểm không giảm → thước bị "mù". Bài đề xuất bộ **checklist nhiễu loạn** (đổi từ, đảo nghĩa, thêm lỗi…) để kiểm *độ nhạy* của metric một cách có hệ thống.

## Điểm cần biết
- Đổi khung đánh giá metric: từ "so với người" sang "**kiểm hành vi bằng lỗi có kiểm soát**".
- Đây là **paradigm bình duyệt** → hợp thức hoá việc ta **không** lấy human-correlation làm cổng đậu/rớt.
- Bổ trợ cùng CheckList (Ribeiro, ACL 2020) và BUMP (ACL 2023).

## Dùng refer gì cho bài của tôi
- **Trụ số 1** cho §7.2: "perturbation là cách validate metric chính danh, đo *độ nhạy*".
- Biện minh **harness bơm-lỗi-độc-lập-matcher** (chèn nút ma, đổi đồng nghĩa).
- Khung khiêm tốn: perturbation = *điều kiện cần* (độ nhạy), chưa phải convergent validity → cặp với measurement-theory.
