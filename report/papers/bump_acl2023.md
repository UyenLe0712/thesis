# BUMP: A Benchmark of Unfaithful Minimal Pairs for Meta-Evaluation of Faithfulness Metrics

- **Link:** https://arxiv.org/abs/2212.09955 (bản ACL Anthology: ACL 2023) · ⚠ *xác nhận link anthology trước khi in*
- **Venue/năm:** ACL 2023.
- **Vai trong luận văn:** trụ bình-duyệt cho **perturbation/minimal-pair meta-eval** (cặp với Sai 2021) — §7.2.

## Paper này nói gì (cho người mới)
BUMP tạo ra các **"cặp tối thiểu không-trung-thực"**: lấy một bản tóm tắt đúng, rồi **bơm đúng MỘT lỗi** để nó thành sai một cách tối thiểu. Sau đó kiểm xem các **thước đo faithfulness** có phân biệt được bản đúng và bản đã-bơm-lỗi không. Nếu không phân biệt được → thước dở.

## Điểm cần biết
- Đúng **cơ chế perturbation** mà luận văn dùng, nhưng ở dạng benchmark chuẩn hoá.
- Bình duyệt tại ACL → củng cố "bơm-một-lỗi-rồi-đo-thước" là hợp lệ, không cần human làm trục chính.
- Nhấn mạnh cả **monotonicity** (lỗi nặng hơn → điểm tệ hơn) và phân biệt loại lỗi.

## Dùng refer gì cho bài của tôi
- Cùng Sai (2021) làm **cặp trụ** cho §7.2: "meta-eval bằng minimal-pair/perturbation là chính danh".
- Biện minh 2 test bổ sung ta cần thêm (**benign-robustness** + **error-type-discrimination**) để đủ 4 tiêu chí.
