# Measuring what Matters: Construct Validity in Large Language Model Benchmarks (NeurIPS 2025 D&B)

- **Link:** https://openreview.net/forum?id=mdA5lVvNcU · arXiv 2511.04703
- **Venue/năm:** **NeurIPS 2025, Datasets & Benchmarks Track** — ✔ đã xác nhận (R-07/R-08). ⚠ *Khi in ghi ĐÚNG tên đầy đủ "…in **Large Language Model** Benchmarks" + "D&B Track".*
- **Vai trong luận văn:** nhập **lăng kính construct-validity** mà reviewer 2026 dùng để đọc metric — §7.2.

## 1. Bối cảnh & vấn đề
Rất nhiều "benchmark" cho LLM đo **không đúng thứ chúng tuyên bố đo** — điểm cao chưa chắc phản ánh năng lực thật. Trong khoa học đo lường, đây gọi là vấn đề **construct validity** ("thước có thật sự đo đúng khái niệm cần đo không?"). Bài này khảo sát hệ thống hàng trăm benchmark LLM qua lăng kính đó.

## 2. Ý tưởng chính (dễ hiểu)
- Rà soát **rất nhiều benchmark LLM** (hàng trăm) với nhiều người đánh giá.
- Chỉ ra các benchmark thường **thiếu định nghĩa rõ khái niệm** (construct) và thiếu bằng chứng rằng điểm số đo đúng khái niệm đó.
- Đề xuất/nhấn mạnh dùng **ngôn ngữ measurement-theory**: định nghĩa construct → chọn cách đo → chứng minh validity (nội dung, hội tụ, phân biệt…).

## 3. Vì sao quan trọng với luận văn
Đây là **cách reviewer 2026 sẽ soi metric của ta**. Nếu ta chỉ nói "chúng tôi validate bằng perturbation" mà không đóng khung theo construct-validity, dễ bị chê "sensitivity ≠ validity". Ngược lại, nếu ta khai rõ: **construct = "trung-thực-hoá"**, đo bằng **tam giác** (perturbation + đối-chứng-thất-bại + %fallback), và định vị human-correlation là *một facet future-work* — thì ta nói đúng "ngôn ngữ" của họ.

## 4. Điểm mạnh & giới hạn
- **Mạnh:** trụ **peer-reviewed** để hợp thức hoá khung measurement-theory.
- **Giới hạn:** là bài *position/khảo sát*, không cho công thức đo sẵn cho miền của ta.

## 5. Dùng refer gì cho bài của tôi
- **Trụ** cho §7.2: đóng khung validate metric theo **construct validity** (không chỉ "độ nhạy").
- Cùng "Neither Valid nor Reliable?" hậu thuẫn việc **không lấy LLM-judge làm trục validate chính**.
- Giúp trả lời đòn "thiếu validation": ta có **tam-giác-bằng-chứng** cho construct, human-correlation = future-work có chủ đích.
