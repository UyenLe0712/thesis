# Prompt phản biện toàn bộ luận văn (dán vào một chat MỚI)

> Mục đích: cho một chat khác phản biện đối kháng TOÀN BỘ luận văn, khách quan nhất có thể — không chỉ tin bản tóm tắt. Copy nguyên khối dưới đây.

---

Trong repo này là một luận văn thạc sĩ AI đang xây dở — đề tài: một mô hình nhận **ảnh chụp màn hình app + câu hỏi** rồi sinh **các bước hướng dẫn cho người đọc**. Nhiệm vụ của bạn: **PHẢN BIỆN ĐỐI KHÁNG TOÀN BỘ luận văn này — độc lập, khách quan, không nể nang.**

**⚠️ CẢNH GIÁC NGUỒN:** mọi file trong `report/` và code trong `harness/` đều do **một trợ lý AI cùng xây dự án viết ra**. Hãy coi **mọi khẳng định** — kể cả "đã kiểm bằng số", "đã chốt", "cổng đã qua", "không bị scoop", "đủ lực thống kê" — là điều **CẦN TỰ KIỂM CHỨNG**, có thể đã tô hồng, nói quá, hoặc bỏ sót. Đừng tin theo giọng tự tin của tài liệu.

**QUY TRÌNH:**

1. **Nắm toàn cảnh (điểm xuất phát, KHÔNG phải sự thật):** đọc `report/88_TOAN_CANH_CHI_TIET.md` + `CLAUDE.md` (mục §0 ở đầu).

2. **Kiểm chống lời kể — soi DỮ LIỆU GỐC, không dừng ở văn:** với mỗi khẳng định quan trọng, mở tận:
   - **Kết quả thô:** `harness/*_results.json` (`k1_results`, `metric_v1_results`, `mde_pilot_results`, `ocr_coverage_results`, `k2_results`, `pilot_ac_results`...).
   - **Code:** `harness/*.py` (`metric_v1_validate`, `mde_pilot`, `k1_matcher_killtest`, `k2_hallucination_types`, `ocr_vh_coverage`, `pilot_androidcontrol`). **Nếu nghi ngờ một con số hay một kết luận, CHẠY LẠI code để tự kiểm** (venv: `~/.venvs/thesis/bin/python`; cần `ollama serve` cho nomic/bge-m3).
   - **Chi tiết từng phần:** `report/73–86` (bằng chứng), `report/85` (đăng-ký-trước), `report/82` + `report/57` (tính mới / văn liệu). Đọc bất cứ file nào bạn cần.

3. **Phản biện TOÀN DIỆN — không bỏ mảng nào.** Soi ít nhất các trục sau, và **tự thêm** bất cứ trục nào bạn thấy còn thiếu:
   - **Động cơ & bài toán:** đây có phải vấn đề nghiên cứu thật, hay bài toán tự nghĩ ra cho có?
   - **Logic đổi hướng** (prompting → train model → phương án "lai"): hợp lý, hay là biện minh sau khi hướng cũ thất bại?
   - **Thiết kế pipeline & huấn luyện:** có lỗ hổng nền tảng không? Train trên AndroidControl gold rồi chấm trên AndroidControl có phải "vừa học vừa chấm cùng loại" đến mức tầm thường không?
   - **Thước đo (quan trọng):** thước tách (thao-tác, đích) có thật sự đo đúng thứ cần không (construct validity — đo hướng-dẫn-cho-người hay chỉ đo khớp-thao-tác-máy)? Phép kiểm bằng bơm-lỗi có **vòng-vo / tự-dựng-nên-dễ-đạt** không (perturbation do chính tác giả tạo)? `AUC = 1.000` có đáng ngờ không, tại sao?
   - **Dữ liệu:** dùng split app-unseen đúng chưa? Có rò rỉ train/test không? Gán nhãn app (chỉ ~72% ep) có đủ tin để cụm thống kê theo app không?
   - **Thống kê:** MDE (~8-9 điểm %), cỡ mẫu pilot (26 app), phương pháp (sign-flip / bootstrap), ngưỡng "15-20 điểm" lấy từ đâu — có đứng vững không? Nếu hiệu ứng thật nhỏ hơn MDE thì sao?
   - **Bốn phép thử (K1/K2/OCR/VIỆC1):** kết luận có bị **khái quát quá** từ mẫu nhỏ / một miền app không (K2 chỉ 80 màn, một loại app, không xem ảnh)?
   - **Tính mới & chống scoop:** phòng thủ được thật không? Vòng kiểm scoop có bỏ sót bài nào (nhất là các bài tự nhận "chưa đọc hết": HalluClear, TIST 2022, hội nghị HCI)? Có bài nào có thể phủ định đóng góp?
   - **Đóng góp:** "đóng góp mô hình" là đóng góp thật hay chỉ là fine-tune có giám sát trên đáp án có sẵn (gần các bài đã có)? Có đủ ngưỡng luận văn thạc sĩ không?
   - **Trung thực báo cáo:** có chỗ nào prose (report) **nói mạnh hơn** số liệu/code cho phép không?
   - **Khả thi:** kịp thời gian/ngân sách (một người, ~7 tuần, hai bài báo) không? Rủi ro nào chưa được xử?

**KẾT QUẢ CẦN TRẢ:** liệt kê phát hiện theo **mức nghiêm trọng (nặng → nhẹ)**. Mỗi phát hiện ghi: (a) vấn đề là gì; (b) bằng chứng bạn dựa vào (tên file / con số / dòng code — nếu chạy lại code thì ghi kết quả); (c) phân loại: **"lỗi thật phải sửa"** vs **"điểm yếu tác giả đã tự khai"** vs **"chưa đủ dữ kiện để kết luận"**. Cuối cùng cho một **phán quyết tổng:** luận văn này đứng vững tới đâu, và **chỗ nào bắt buộc phải sửa TRƯỚC khi bỏ tiền huấn luyện**.

Đừng ngại kết luận rằng có chỗ hỏng. Mục tiêu là tìm ra lỗ **trước khi** thầy hướng dẫn / hội đồng tìm ra.

---

*(Tuỳ chọn: nếu chat đó có công cụ chạy nhiều tác nhân song song, có thể chia các trục trên cho nhiều tác nhân phản biện độc lập rồi tổng hợp — sẽ phủ rộng và ít thiên lệch hơn một góc nhìn.)*
