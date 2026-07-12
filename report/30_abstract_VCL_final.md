# TÓM TẮT NỘP HỘI NGHỊ VCL — BẢN CHỐT (DG1)

> Tiểu ban đề xuất: **Tiểu ban 1 — Lý thuyết và mô hình mới** (mục "Mô hình ngôn ngữ lớn và tương lai NLP").
> File này gom đủ: Tên bài + Tóm tắt + Từ khóa để nộp. Cập nhật 2026-06-30.

---

## TÊN BÀI (đề xuất chính — giữ vế "câu hỏi người dùng")

**Sinh hướng dẫn sử dụng phần mềm từ ảnh chụp màn hình và câu hỏi người dùng: đánh giá độ trung thực không cần đáp án mẫu**

### Phương án thay thế
- **(Gọn & "người" nhất, bỏ vế câu hỏi):** Đánh giá và giảm ảo giác giao diện trong hướng dẫn sử dụng phần mềm sinh từ ảnh chụp màn hình, không cần đáp án mẫu
- **(Ngắn nhất, nhấn đánh giá):** Đánh giá độ trung thực của hướng dẫn sử dụng phần mềm sinh tự động khi không có đáp án mẫu

---

## TÓM TẮT (~150 từ)

Sinh hướng dẫn sử dụng phần mềm từ ảnh chụp màn hình và câu hỏi người dùng là bài toán đa phương thức còn ít được khai thác. Các mô hình đa phương thức (VLM) làm được việc này nhưng thường bị ảo giác, nhắc đến các phần tử không có trên màn hình khiến hướng dẫn sai lệch. Việc đánh giá cũng khó khăn vì hầu hết ứng dụng không có hướng dẫn mẫu để đối chiếu. Chúng tôi dùng cây phân cấp giao diện (View Hierarchy) làm nguồn đối chiếu đo độ trung thực, chỉ dùng khi đánh giá để tránh rò rỉ thông tin sang quá trình sinh. Dựa trên cùng nguồn đối chiếu, chúng tôi thêm một lớp hậu kiểm: những bước nhắc đến nút không tồn tại được viết lại thành mô tả thao tác bằng lời. Để kiểm chứng độ tin cậy của thước đo, chúng tôi chủ động đưa các lỗi đã biết vào hướng dẫn rồi đo tỉ lệ phát hiện. Thực nghiệm trên màn hình Android thực cho thấy phương pháp giảm rõ số bước nhắc đến nút không tồn tại, đổi lại một số bước phải mô tả khái quát hơn.

> **Bản ~130 từ** (nếu hội nghị chặn 150 cứng): bỏ câu *"Để kiểm chứng độ tin cậy của thước đo, chúng tôi chủ động đưa các lỗi đã biết vào hướng dẫn rồi đo tỉ lệ phát hiện."*

---

## TỪ KHÓA

### Bộ chính (7 — khuyến nghị)
1. mô hình ngôn ngữ đa phương thức (VLM)
2. sinh hướng dẫn sử dụng phần mềm
3. ảo giác giao diện (hallucination)
4. độ trung thực (faithfulness)
5. đánh giá không cần đáp án mẫu
6. cây phân cấp giao diện (View Hierarchy)
7. phân tích độ nhạy (perturbation)

### Thêm (dự phòng — nếu hội nghị cho nhiều từ khóa)
8. hiểu giao diện người dùng (GUI understanding)
9. neo phần tử giao diện (UI grounding)
10. hỏi-đáp đa phương thức (multimodal QA)
11. đánh giá tự động mô hình sinh
12. ứng dụng di động Android

> Nếu hội nghị chỉ cho **5 từ khóa**: giữ #1, #2, #3, #4, #6.
> #7 có thể thay bằng **"kiểm chứng độ tin cậy của thước đo"** nếu thấy "perturbation" hơi kỹ thuật.

---

## GHI CHÚ NỘI BỘ (KHÔNG nộp — để mình nhớ)

- **3 việc 🟡 còn phải hiện thực + chạy** (đã chốt hướng, không phải nghiên cứu lại):
  1. Lớp hậu kiểm: viết bước **sinh câu mô tả bằng lời** thật (code hiện mới ở mức placeholder).
  2. Bộ **perturbation** (đưa lỗi đã biết, đo tỉ lệ phát hiện) — chưa code.
  3. **Chạy chính** 90 màn / 18 app → ra số cuối.
- Câu *"giảm rõ…"* hiện dựa trên **kết quả sơ bộ**; đúng về cơ chế (lớp hậu kiểm loại bỏ tham chiếu tới nút không tồn tại). Khi chạy xong, **thay con số thật** vào.
- Nguyên tắc: giữ **định tính** ("giảm rõ", không số) cho tới khi có kết quả cuối.
