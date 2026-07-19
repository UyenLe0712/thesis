# STRESS-TEST RIÊNG THIẾT KẾ THỐNG KÊ TIER 1/TIER 2 (2026-07-11)

> Nguồn: workflow `wf_12cb7cad-be3` (10 agent: 3 research + 3 đòn tấn công + 3 kiểm chứng + 1 tổng hợp). Đây là mảnh duy nhất trong toàn bộ thiết kế "Faithful Distillation" **chưa từng bị một vòng debate riêng nào soi trực tiếp** trước round này (5 vòng trước soi hướng đi/tính-mới/đủ-ngưỡng, không soi vào chính công thức thống kê).

**KẾT LUẬN: ĐỨNG VỮNG Ở CỐT LÕI, KHÔNG CẦN THIẾT KẾ LẠI.** Độ tự tin ~0.8. Cần vá chữ/bổ sung báo cáo ở vài chỗ, không đổi khung Tier 1/Tier 2.

---

## 1. Ba đòn tấn công + kết quả

| Đòn | Verdict ban đầu | Sau kiểm chứng |
|---|---|---|
| **Tier 1 không "an toàn" như tưởng** (train-trên-lọc có thể thua train-trên-thô) | cần sửa | **BỊ BÁC BỎ.** Đòn tấn công tự đánh tráo trụ trích dẫn (dùng AlpaGasus/NOVA thay vì đúng KnowAda/VGA đang trích trong dự án). Khi tra đúng KnowAda: cơ chế thật của nó ("sửa có chọn lọc chi tiết không-kiểm-chứng-được thành mô tả chung") **giống hệt PA2** — và KnowAda báo cáo cơ chế này HIỆU QUẢ. Tiền lệ dương cho đúng thao tác PA2 đã tồn tại. |
| **Công thức MDE/thống kê có lỗ hổng** | đứng vững, cần sửa | Đúng — 5 trích dẫn xác thực đúng venue, phép tính (4096 tổ hợp, MDE=3.077×SD/√12) đúng. Vấn đề thật: câu chữ định nghĩa SD(d_j) đang mơ hồ. |
| **12 app test quá mỏng** | đứng vững, cần sửa | Không phải lỗi thống kê (macro-per-app + G nhỏ được Ibragimov & Müller 2010 hợp thức hoá đúng cách) — mà là thiếu đoạn tự-giới-hạn phạm vi khái quát hoá (kiểu Mind2Web). |

## 2. Việc cần sửa cụ thể (đã áp vào report/53 + report/54)

**A. Thống kê:**
1. Định nghĩa lại rõ: SD(d_j) = độ lệch chuẩn của **12 giá trị d_j đã lấy trung bình theo app**, không phải hàm trực tiếp từ Var(f_base)/Var(f_student) thô cấp-màn.
2. Báo histogram + hệ số biến thiên CV(n_j) của số-màn/app trong 12 app test; nếu CV lớn, ghi rõ MDE là "cận dưới lạc quan" (Eldridge et al. 2006).
3. Đóng khung công thức MDE là **xấp xỉ liên tục kiểu Julious**, không phải MDE chính xác của exact sign-flip rời rạc (4096×0.025=102.4 không nguyên → mức ý nghĩa danh nghĩa 2.5% không đạt chính xác tuyệt đối).
4. Khai tường minh giả định độc lập giữa 12 app trong pre-registration (app cùng công ty/UI-kit? chấm cùng lô/ngày API?) — nếu được, xen kẽ ngẫu nhiên thứ tự gọi API giữa app/điều kiện.
5. Phân tích độ nhạy phụ: chạy lại có trọng số theo n_j (số màn/app), xem PASS/NULL có đổi không.

**B. Phạm vi claim:**
6. Viết kết luận Tier 2 theo mẫu Mind2Web: *"khái quát hoá TRONG phạm vi phân phối MobileViews đã qua gate K1"*, KHÔNG dùng cụm "tổng quát cho app GUI mới nói chung".
7. Trích tường minh ngưỡng "few clusters" (Cameron & Miller 2015) ngay trong pre-registration — biến thành giới hạn đã lường trước, lý do đã chọn exact sign-flip (Ibragimov & Müller 2010) thay vì cluster-robust SE tiệm cận.
8. Thêm đoạn limitation tách biệt "hợp lệ thống kê nội bộ" khỏi "tính đại diện quần thể" (chuỗi thu hẹp 3 tầng: auto-crawl → gate K1 → 12/30 app).

**C. Bảo hiểm rẻ (không phải sửa lỗi, chỉ đóng kín câu hỏi giám khảo dễ đoán):**
9. **KHÔNG đổi** "Tier 1 gần chắc dương" — cơ sở học thuật cho việc hạ khung không đủ mạnh.
10. Thêm một readout phụ dùng khung E16 có sẵn: so Student-filtered vs Student-RAW về **hữu-ích/mạch-lạc** (không phải trung thực) bằng LLM-judge khác họ, đặc biệt trên đúng nhóm bước từng bị PA2 viết-lại-thành-mô-tả-chung. Nếu Student-RAW được chấm hữu ích hơn ở đúng nhóm này → phải báo thẳng đánh-đổi cục bộ.
11. Báo % bước bị PA2 viết-lại trên 18 app train như một covariate (gần như free).

## 3. Trả lời trực tiếp: "Tier 1 gần chắc dương" còn đứng không?

**CÒN ĐỨNG.** Nỗi lo "văn phong cụ thể-nhưng-sai được chấm cao hơn mô tả mờ-nhưng-đúng" không có cơ sở trực tiếp trong tài liệu đã kiểm — ngược lại, đúng trụ trích dẫn của dự án (KnowAda) cho thấy đúng thao tác này hoạt động tốt.

## 4. Mức tự tin

**~0.8** rằng thiết kế thống kê Tier 1/Tier 2 đúng nguyên tắc, không cần thiết kế lại — chỉ cần các sửa liệt kê ở mục 2. Không cao hơn vì: (a) giả định độc lập giữa 12 app vẫn là rủi ro thật CHƯA kiểm chứng bằng dữ liệu (chỉ là caveat cần khai); (b) chưa tự mô phỏng lại power của chính exact sign-flip rời rạc để xác nhận MDE thật lệch bao nhiêu so với xấp xỉ Julious.
