# Neither Valid nor Reliable? Investigating the Use of LLMs as Judges (NeurIPS 2025, Position)

- **Link:** https://openreview.net/forum?id=yqKfMr0yvY · arXiv 2508.18076
- **Venue/năm:** **NeurIPS 2025 (Poster)** — ✔ đã xác nhận (R-07/R-08).
- **Vai trong luận văn:** hậu thuẫn quyết định **KHÔNG lấy LLM-as-judge làm trục validate chính** — §5.4, §7.

## 1. Bối cảnh & vấn đề
"LLM-as-judge" (dùng một LLM để chấm điểm đầu ra) đang phổ biến vì rẻ và nhanh. Nhưng bài position này đặt câu hỏi thẳng: nó có **hợp lệ (valid)** và **ổn định (reliable)** không? — hai tiêu chí tối thiểu của một công cụ đo lường.

## 2. Ý tưởng chính (dễ hiểu)
- **Validity:** LLM-judge có đo đúng thứ ta muốn đo, hay đo thứ khác (độ dài, văn phong, thiên vị họ nhà nó)?
- **Reliability:** chấm lại có ra kết quả nhất quán không, hay "hên xui" (rating roulette)?
- Kết luận cảnh báo: nhiều cách dùng LLM-judge hiện nay **chưa chứng minh được** cả hai → không nên coi nó là chuẩn vàng.

## 3. Vì sao quan trọng với luận văn
Luận văn **có dùng** một LLM-judge, nhưng **chỉ như 1 trong 3 cơ chế chấm độc lập** (cùng bge-m3 + token-overlap), và **khác họ generator** (chống self-preference — Panickssery). Bài này hậu thuẫn: **đúng khi KHÔNG nâng LLM-judge lên làm trục validate chính** — ta không validate matcher bằng nhãn-LLM, mà bằng perturbation + người (few-pairwise).

## 4. Điểm mạnh & giới hạn
- **Mạnh:** trụ để **phòng thủ trước** đòn "sao không dùng LLM-judge chấm hết cho gọn".
- **Giới hạn:** là *position paper* (quan điểm), không phải kết quả thực nghiệm mới.

## 5. Dùng refer gì cho bài của tôi
- **Trụ** cho §5.4/§7: LLM-judge chỉ là **một cơ chế phụ**, khác họ generator, KHÔNG làm cổng validate chính.
- Cùng "Measuring what Matters" nhập lăng kính **construct/validity-reliability** của reviewer 2026.
