# Cluster-Robust Inference: A Guide to Empirical Practice (MacKinnon, Nielsen & Webb)

- **Link:** *Journal of Econometrics* **232(2):272–299** (2023).
- **Venue/năm:** **Journal of Econometrics 232(2), 2023** — ✔ đã xác nhận (R-08).
- **Vai trong luận văn:** trụ **thống kê đương đại** cho suy luận với **ít cụm / cụm lệch cỡ** (G≈17) — §7.4.

## 1. Bối cảnh & vấn đề
Khi dữ liệu có **cấu trúc cụm** (ở ta: nhiều màn cùng một *app* → không độc lập), phải dùng **suy luận vững-theo-cụm** (cluster-robust) để khoảng tin cậy không bị **hẹp giả tạo**. Nhưng khi **số cụm nhỏ** (vài chục) và **kích thước cụm chênh nhau**, các phương pháp chuẩn dễ **under-coverage** (khoảng tin cậy hẹp hơn thực tế → kết luận quá tự tin).

## 2. Ý tưởng chính (dễ hiểu)
Đây là **bài hướng dẫn thực hành** tổng hợp: khi nào dùng gì, cạm bẫy ở đâu.
- Với **ít cụm**: sai số chuẩn cluster thường **kém**; nên dùng **wild cluster bootstrap-t**.
- Nhưng wild cluster bootstrap **cũng gãy** khi cụm lệch cỡ nặng → cần **kiểm chéo** bằng các biến thể **jackknife (CV3/CV3J)**.
- Nhấn mạnh **báo cáo trung thực** giới hạn khi G nhỏ, thay vì giả vờ khoảng tin cậy đẹp.

## 3. Vì sao quan trọng với luận văn
Dữ liệu ta gom cụm theo **app (~17 cụm)** — vừa **ít** vừa **lệch cỡ** (app nhiều màn, app ít màn). Đây đúng tình huống bài cảnh báo. Ta cần một trụ **đương đại** (2023) thay cho trích cũ Cameron-Gelbach-Miller (2008), và cần **khai thẳng caveat under-coverage**.

## 4. Điểm mạnh & giới hạn
- **Mạnh:** hướng dẫn mới nhất, uy tín (Journal of Econometrics) → chống đòn "thống kê ẩu".
- **Giới hạn:** không có "phương án sạch" cho ít-cụm — bài cũng thừa nhận mọi cách đều có điểm gãy → ta buộc phải **khai caveat + đánh dấu số exploratory**.

## 5. Dùng refer gì cho bài của tôi
- **Trụ chính** cho §7.4: wild cluster bootstrap-t (chính) + jackknife CV3/CV3J (kiểm chéo) + **caveat G≈17 lệch cỡ**.
- Trả lời đòn "17 cụm quá ít, thống kê không đáng tin": ta **không giấu** — dùng đúng guide 2023, khai caveat, số hiện là *exploratory*, pre-register ngưỡng trước.
