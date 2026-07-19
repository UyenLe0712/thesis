# Unblind Your Apps: Predicting Natural-Language Labels for Mobile GUI Components (Chen et al.)

- **Link:** https://arxiv.org/abs/2003.00380 · ⚠ *xác nhận link trước khi in*
- **Venue/năm:** ICSE 2020 (**Distinguished Paper**).
- **Vai trong luận văn:** bằng chứng **>77% ứng dụng có nút thiếu nhãn** — nền cho cách xử lý VH không hoàn hảo (§2.2, §3.1, §7.3).

## Paper này nói gì (cho người mới)
Nhiều nút trong app Android **không có nhãn chữ** (nhất là nút chỉ có biểu tượng), nên trình đọc màn hình cho người khiếm thị "đọc" không ra. Bài đo được **hơn 77% ứng dụng** có nút thiếu nhãn dùng được, và đề xuất dùng học sâu để **đoán nhãn** cho các nút đó.

## Điểm cần biết
- Xác nhận: **cây phân cấp giao diện (VH) KHÔNG hoàn hảo** — có nút không nhãn / nhãn chung ("Image").
- Là **Distinguished Paper ICSE** → con số 77% rất đáng tin để trích.
- Hệ quả: nếu coi VH là chân lý tuyệt đối, ta sẽ **tính oan** ảo giác cho những nút vốn thiếu nhãn.

## Dùng refer gì cho bài của tôi
- Biện minh **báo tỉ-lệ-ảo-giác "có điều kiện độ-phủ-nhãn"** + **loại nút nhãn-chung khỏi mẫu số** (§5.1, §7.3).
- Chống đòn *"có sẵn khung nút nên rủi ro bị chặn"* — ta KHÔNG được nói vậy, vì mâu thuẫn Chen.
- Củng cố **cổng K1** (phải đo recall của VH/bộ dò trước khi tin mẫu số).
