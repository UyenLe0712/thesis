# Dodgersort: Uncertainty-Aware VLM-Guided Human-in-the-Loop Pairwise Ranking

- **Link:** https://link.springer.com/chapter/10.1007/978-981-92-1468-6_32 (DOI 10.1007/978-981-92-1468-6_32)
- **Venue/năm:** **PAKDD 2026** (Advances in Knowledge Discovery and Data Mining, Part IV — Springer LNCS, peer-reviewed) — ✔ đã xác nhận (R-07; tác giả Yujin Park, Haejun Chung, Ikbeom Jang).
- **Vai trong luận văn:** trụ cho lựa chọn **trọng-số-theo-độ-bất-định thay vì confidence VLM tự-khai** (M2) — §4.3(c).

## 1. Bối cảnh & vấn đề
Khi xếp hạng bằng so-cặp có VLM tham gia, một câu hỏi thực tế là: **tin phán đoán cặp nào tới đâu?** Nếu tin bừa vào "độ tự tin" mà mô hình tự nói ra thì nguy hiểm (mô hình **calibrate kém** — tự tin cả khi sai). Dodgersort xử lý bằng cách **mô hình hoá độ bất định** một cách bài bản.

## 2. Ý tưởng chính (dễ hiểu)
- Kết hợp nhiều mô hình xếp hạng (kiểu Elo / Bradley-Terry / Gaussian Process) thành **ensemble**.
- Phân tách **độ bất định**: loại "do thiếu dữ liệu" (epistemic) và loại "do nhiễu bản chất" (aleatoric).
- Dùng **lý thuyết thông tin** để **chọn cặp nào đáng hỏi tiếp** (hỏi ở chỗ giảm bất định nhiều nhất) → giảm ~11–16% công gán nhãn.

## 3. Vì sao quan trọng với luận văn
Nó là **tiền lệ bình duyệt** cho nguyên tắc: **trọng số/độ-tin của phán đoán so-cặp nên đến từ mô hình-hoá-bất-định, KHÔNG từ "confidence" mà mô hình tự khai**. Đây đúng là lý lẽ đằng sau **M2** của ta (dùng margin-Copeland / self-consistency thay vì confidence VLM).

## 4. Điểm mạnh & giới hạn (so với bài của ta)
- **Mạnh:** chính danh hoá "uncertainty-aware pairwise".
- **Khác ta:** Dodgersort **có người trong vòng lặp**, miền ảnh tổng quát (y tế/thẩm mỹ); ta **tự động** trong miền **GUI** và **suy nhãn cặp-bắt-buộc từ gold**.

## 5. Dùng refer gì cho bài của tôi
- **Trụ** cho M2 (§4.3): biện minh "không tin confidence tự-khai, dùng trọng-số-bất-định".
- Cùng EZ-Sort trong related-work Stage-0 để phân định độ mới.
- ⚠ Xác nhận DOI/venue Springer trước khi trích chính thức.
