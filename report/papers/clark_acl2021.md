# All That's 'Human' Is Not Gold: Evaluating Human Evaluation of Generated Text (Clark et al.)

- **Link:** https://aclanthology.org/2021.acl-long.565/ · ⚠ *xác nhận link trước khi in*
- **Venue/năm:** ACL-IJCNLP 2021.
- **Vai trong luận văn:** trụ để **KHÔNG lấy "chấm người" làm cổng đậu/rớt** — §7.2 (khung measurement-theory).

## 1. Bối cảnh & vấn đề
Trong đánh giá văn bản do máy sinh (NLG), nhiều người mặc định **"con người chấm là chuẩn vàng"** (human evaluation = gold standard). Nhưng nếu chính con người chấm cũng **không đáng tin**, thì lấy nó làm mốc để phán các thước đo tự động khác là sai lầm. Bài này kiểm tra thẳng giả định đó.

## 2. Ý tưởng chính (dễ hiểu)
Họ cho người **chưa huấn luyện** đọc các đoạn văn và đoán: đoạn này do **người viết** hay do **máy (GPT-2/GPT-3) viết**? Kết quả gây sốc: với văn bản từ GPT-3, người đoán đúng chỉ **~50%** — tức **ngang tung đồng xu**, gần như không phân biệt nổi. Họ cũng thử các cách "huấn luyện nhanh" người chấm (cho ví dụ, hướng dẫn, giải thích) để xem có cải thiện không.

## 3. Kết quả & bài học chính
- Người **không được huấn luyện kỹ** đánh giá văn bản máy **rất kém** (gần mức ngẫu nhiên).
- Chất lượng đánh giá phụ thuộc nặng vào **cách thiết kế quy trình chấm** (hướng dẫn, đào tạo, ví dụ) — chứ không tự nhiên tốt.
- Hàm ý: "human eval" **không phải một mốc tuyệt đối, sạch sẽ**; nó có nhiễu, có thiên lệch, và cần được thiết kế cẩn thận mới đáng tin.

## 4. Điểm mạnh & giới hạn
- **Mạnh:** đập tan giả định "người chấm luôn là gold" — bình duyệt tại venue hàng đầu.
- **Giới hạn:** không nói "đừng bao giờ dùng human eval", mà nói "**đừng dùng human eval cẩu thả làm chuẩn**".

## 5. Dùng refer gì cho bài của tôi
- **Trụ chính** cho quyết định: **bỏ human-correlation khỏi cổng đậu/rớt**, đưa xuống future-work có chủ đích (§7.2, §10).
- Câu-thủ trực tiếp khi giám khảo hỏi *"sao không chấm người?"*: "human-eval bản thân agreement thấp / gần ngẫu nhiên (Clark 2021), ép nó làm gold-gate là **nguỵ hợp lệ**".
- Ghép với measurement-theory: perturbation đo *độ nhạy* (điều kiện cần); convergent-validity-bằng-người là *một facet future-work*, không phải cổng.
