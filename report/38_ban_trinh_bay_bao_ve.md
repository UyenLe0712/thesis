# Bản trình bày bảo vệ — Sinh tự động hướng dẫn sử dụng phần mềm từ ảnh giao diện

> Tài liệu dùng khi trình bày trước giảng viên hướng dẫn. Bám theo bố cục slide
> `LUAN_VAN_SLIDE.pptx`: (1) Bài toán — (2) Dữ liệu — (3) Phương pháp — (4) Đánh giá —
> (5) Tính hợp lệ — (6) Đóng góp, giới hạn. Mỗi mục gồm: nội dung trình bày, luận điểm
> khoa học, và căn cứ trích dẫn. Văn phong báo cáo, không dùng lối nói.

---

## 0. Định vị đề tài trong một đoạn

Luận văn giải quyết bài toán: cho một hoặc nhiều ảnh chụp màn hình phần mềm cùng một câu
hỏi bằng ngôn ngữ tự nhiên, hệ thống tự động sinh ra bản hướng dẫn thao tác theo từng bước
cho người đọc. Đây là bài toán đa phương thức (ảnh và văn bản sinh ra văn bản). Điểm khó
cốt lõi không nằm ở việc sinh văn bản, mà ở chỗ **không tồn tại tập hướng dẫn chuẩn do con
người biên soạn** để làm mốc đánh giá, trong khi các mô hình ngôn ngữ thị giác lại thường
**tham chiếu tới những nút không có thật trên màn hình**. Luận văn vì vậy có hai đóng góp
song song và ngang nhau **(có điều kiện — xem mục 6.1)**: một **hệ thống sinh hướng dẫn** hạn chế được lỗi ảo giác giao diện,
và một **phương pháp đánh giá** đáng tin trong điều kiện thiếu bản mẫu.

---

## 1. Bài toán và động lực

### 1.1. Hợp đồng đầu vào — đầu ra
- **Đầu vào:** một ảnh (tác vụ trong một màn) hoặc nhiều ảnh đã xáo trộn của cùng một luồng
  thao tác (tác vụ trải nhiều màn), kèm một câu hỏi sử dụng.
- **Đầu ra:** hướng dẫn thao tác đánh số theo bước, bám sát ngữ cảnh ảnh.
- Ví dụ minh hoạ (một màn): với ảnh hộp thoại đặt giờ và câu hỏi *“Cần thao tác gì để đặt
  giờ 20:35 và xác nhận?”*, đầu ra mong muốn là: *(1) Chọn giờ “8”, phút “35”; (2)
  Chọn buổi “PM”; (3) Chọn “OK”.*

### 1.2. Ba thách thức trọng tâm (đây là phần biện minh vì sao đề tài là nghiên cứu)
1. **Ảo giác giao diện.** Mô hình sinh ra bước thao tác trỏ tới nút không tồn tại trên màn
   hình. Hệ quả trực tiếp: người dùng không thể thực hiện theo. Đây là dạng lỗi đặc thù của
   sinh văn bản có điều kiện thị giác, cần được đo lường tách bạch.
2. **Thiếu bản hướng dẫn mẫu.** Không có tập hướng dẫn chuẩn do con người biên soạn cho mọi
   ứng dụng. Khi không có mốc tham chiếu, câu hỏi đặt ra là: dựa vào đâu để chấm điểm một
   cách khách quan.
3. **Thứ tự các màn.** Khi đầu vào là nhiều ảnh bị xáo trộn, hệ thống phải tự suy ra thứ tự
   đúng. Câu hỏi khoa học: mô hình dựa trên tín hiệu nào để xác định thứ tự, và ta đo năng
   lực đó ra sao.

> **Luận điểm:** ba thách thức này không thể giải quyết bằng cách áp dụng thẳng một mô hình
> sinh mạnh. Chúng đòi hỏi (a) một cơ chế hậu kiểm để chặn ảo giác, (b) một mốc neo thay thế
> cho bản mẫu, và (c) một phép đo trật tự độc lập. Đó là nội dung nghiên cứu của luận văn.

---

## 2. Dữ liệu — ba bộ và vai trò phân định

Nguyên tắc chọn dữ liệu: xương sống phương pháp chỉ dựa trên nguồn đã được bình duyệt; công
cụ kỹ thuật có thể là bản tiền ấn phẩm nhưng không được trình bày như đã bình duyệt.

| Bộ dữ liệu | Nội dung | Nhãn có sẵn | Vai trò |
|---|---|---|---|
| **MobileViews** (một màn) | Ảnh + cây phân cấp giao diện (View Hierarchy) + toạ độ nút | Không có quỹ đạo vàng | Đánh giá độ trung thực với giao diện trên một màn |
| **AndroidControl** (nhiều màn) | Chuỗi màn của một tác vụ + cây trợ năng + thao tác đúng từng bước | Có quỹ đạo vàng | Đánh giá sắp thứ tự màn và hoàn thành tác vụ |
| **ScreenSpot-v2** (đối chứng) | Ảnh + toạ độ nút chuẩn cho bài trỏ đúng nút | Có toạ độ chuẩn | Kiểm định độc lập độ chính xác trỏ đúng nút |

### 2.1. MobileViews — nhánh một màn
Mỗi ảnh đi kèm cây phân cấp giao diện: danh sách nút, nhãn hiển thị và toạ độ khung của từng
nút. Đây chính là **mốc neo (nhãn bạc)** thay cho bản hướng dẫn mẫu: ta không có hướng dẫn
chuẩn, nhưng ta có danh sách nút thật để kiểm tra mô hình có tham chiếu sai hay không. Ràng
buộc bất biến: **danh sách nút chỉ tham gia ở bước đánh giá, tuyệt đối không cung cấp cho mô
hình ở bước sinh**, nhằm tránh rò rỉ thông tin.

Lưu ý về chất lượng mốc neo: cây phân cấp giao diện có thể thiếu hoặc gán nhãn không đầy đủ
(nút không có nhãn văn bản, nhãn chung như “Button”). Để tránh phạt oan một bước đúng khi nút
tương ứng vắng nhãn, luận văn **đo và báo cáo độ phủ nhãn** (tỉ lệ nút thao tác được có nhãn
dùng được) và **loại các nút nhãn chung khỏi mẫu số độ trung thực**. Tính không đầy đủ của cây
trợ năng là hạn chế đã được ghi nhận trong tài liệu trợ năng Android (nêu ở mục 6.2).

### 2.2. AndroidControl — nhánh nhiều màn
Mỗi tập là một chuỗi màn của một tác vụ hoàn chỉnh, kèm thao tác đúng ở mỗi bước và thứ tự
đúng của các màn. Cây trợ năng đóng vai trò tương đương View Hierarchy. Bộ này đã được bình
duyệt (Li et al., NeurIPS 2024, Datasets & Benchmarks), cung cấp **quỹ đạo vàng** — điều mà
MobileViews không có — nên là nền tảng cho phép đo trật tự và mức hoàn thành tác vụ. Khi thử
nghiệm, các màn được xáo trộn để mô hình tự sắp xếp lại; quỹ đạo vàng chỉ dùng để đối chiếu.

### 2.3. ScreenSpot-v2 — đối chứng grounding
Là chuẩn phổ biến cho bài toán trỏ đúng nút từ mô tả. Vai trò: **kiểm định độc lập** độ chính
xác của bộ trỏ nút, trên dữ liệu tách khỏi tập đánh giá chính. Lý do cần bộ này: MobileViews
hiện là bản tiền ấn phẩm, nên cần một chuẩn đã bình duyệt để củng cố độ tin cậy của phép đo
trỏ đúng nút. ScreenSpot-v2 là bản làm sạch nhãn (OS-Atlas, ICLR 2025); phiên bản gốc thuộc
SeeClick (ACL 2024).

> **Trả lời trước câu hỏi thường gặp — “bộ nào không có View Hierarchy thì không dùng
> được?”:** Phương pháp cần một nguồn phần tử tham chiếu (cây giao diện hoặc toạ độ nút). Cả
> ba bộ trên đều đáp ứng. Với dữ liệu chỉ có ảnh, cần một bộ dò phần tử và mọi số liệu được
> đóng khung “có điều kiện độ bao phủ đã đo”. Khi triển khai trên thiết bị, cây trợ năng do
> hệ điều hành cung cấp trực tiếp nên bước hậu kiểm chạy được ngay.

---

## 3. Phương pháp — hệ thống sinh hướng dẫn

Kiến trúc là một hệ thống thống nhất có bộ định tuyến đầu vào: đầu vào một ảnh đi theo nhánh
một màn; đầu vào nhiều ảnh kích hoạt thêm bước sắp thứ tự ở đầu, rồi mới đi vào nhánh một màn
cho từng ảnh.

### 3.1. Nhánh một màn — sinh trước, đối chiếu sau

**Bước 1 — Sinh.** Mô hình chỉ nhận ảnh và câu hỏi, sinh ra bản hướng dẫn gốc. Danh sách nút
thật không được cung cấp ở bước này. Câu hỏi cũng không chứa tên nút (kiểm tra trùng lặp từ
vựng bằng không), buộc mô hình phải tự đọc ảnh để gọi tên — và đó chính là chỗ phát sinh ảo
giác cần đo.

**Bước 2 — Đối chiếu.** Một thuật toán so khớp ngữ nghĩa đối chiếu từng bước với danh sách
nút thật:
- Bước tham chiếu một nút có thật: giữ nguyên.
- Bước tham chiếu một nút không tồn tại: **thay bằng mô tả khái quát, không suy đoán nút thay
  thế.**

Điểm cần nhấn mạnh: bước đối chiếu là một thuật toán so khớp, không phải một mô hình ngôn
ngữ thứ hai; và danh sách nút chỉ tham gia ở bước 2.

**Ví dụ xuyên suốt** (ảnh hộp thoại đặt giờ; nút thật: *hour, minute, PM, OK, Cancel*):

| Mô hình sinh ra | Nút thật gần nhất | Kết luận |
|---|---|---|
| Chọn giờ và phút | hour / minute | hợp lệ |
| Chọn “PM” | PM | hợp lệ |
| Mở “Cài đặt” | (không có nút tương ứng) | ảo giác |

Quy tắc quyết định: độ giống ngữ nghĩa với danh sách nút thật đạt ngưỡng τ thì bước hợp lệ,
dưới ngưỡng thì tính ảo giác. Lớp đối chiếu chỉ can thiệp vào bước ảo giác: *“Mở Cài đặt”*
(màn chỉ có hour, minute, PM, OK, Cancel) được viết lại thành *“Tìm mục cài đặt liên quan
trên màn hình”*. Hai bước hợp lệ được giữ nguyên. Lưu ý: cặp gần nghĩa như “Confirm” và “OK”
KHÔNG bị tính ảo giác — chúng khớp nút thật, chỉ bị trừ ở thước đo độ đúng nhãn (mục 4.1).

> **Vì sao không suy đoán nút thay thế — đây là một kết quả thực nghiệm, không phải lựa chọn
> tuỳ tiện.** Phương án ngây thơ “thay nút ảo giác bằng nút thật gần nhất” đo được nhưng tạo
> ra **lỗi ngầm**: ví dụ “Submit” bị thay thành “Save” trong khi thao tác đúng là một nút
> khác, khiến người dùng thao tác sai mà không nhận ra. Vì có một phương án thay thế thất bại
> đo được, quyết định “chỉ mô tả khái quát” là kết luận rút ra từ đối chứng, mang tính nghiên
> cứu.

### 3.2. Nhánh nhiều màn — sắp thứ tự bằng so cặp và tổng hợp Copeland

Các màn được xáo trộn. Mô hình so sánh từng cặp (“màn nào trước?”), sau đó tổng hợp bằng
**điểm Copeland** — số cặp mà mỗi màn thắng. Ví dụ ba màn: nếu A trước B, A trước C, B trước
C thì A thắng hai, B thắng một, C thắng không, suy ra thứ tự A < B < C. Nếu xuất hiện mâu
thuẫn vòng (A > B > C > A), loại bỏ phán đoán cặp có độ tin cậy thấp nhất để phá vòng (xấp xỉ
tập cung phản hồi tối thiểu). Khi sắp xếp, mô hình chỉ thấy ảnh đã che thanh trạng thái (đồng
hồ, pin, huy hiệu) và mục tiêu; quỹ đạo vàng chỉ dùng khi đánh giá.

Chuỗi đã sắp xếp được đưa vào nhánh một màn cho từng màn, nên mọi bước vẫn được đối chiếu đầy
đủ. Nhánh nhiều màn thừa kế toàn bộ nhánh một màn và chỉ bổ sung bước sắp thứ tự ở đầu.

### 3.3. Căn cứ lựa chọn phương pháp (tổng hợp)

| Thách thức | Giải pháp | Căn cứ |
|---|---|---|
| Ảo giác giao diện | Sinh trước, đối chiếu nút thật sau | Đo được tỉ lệ ảo giác mà không rò rỉ thông tin |
| Thiếu bản mẫu | Neo bằng danh sách nút thật (nhãn bạc) | Có mốc đánh giá khách quan, không cần biên soạn thủ công |
| Hiệu chỉnh gây lỗi ngầm | Chỉ mô tả khái quát, không suy đoán nút | Tránh dẫn người dùng đến thao tác sai |
| Thứ tự nhiều màn | So cặp và tổng hợp Copeland | Đơn giản, có thể diễn giải, tránh vòng lặp luận lý |

> **Về lo ngại “cơ chế đơn giản”:** cơ chế hậu kiểm cố ý giữ đơn giản; trọng lượng khoa học
> đến từ **phát hiện thực nghiệm** (đo tỉ lệ ảo giác trên nhiều mô hình, đối chứng phương án
> thất bại, đo năng lực sắp thứ tự và phân tích tín hiệu), chứ không từ độ phức tạp mã nguồn.
> Tiền lệ cho hướng “quy trình gọn nhưng đóng góp ở phát hiện và cách đánh giá” gồm G-Eval,
> SelfCheckGPT, FActScore (EMNLP 2023), RAGAS (EACL 2024), ALOHa (NAACL 2024).

---

## 4. Đánh giá — thước đo, ví dụ và căn cứ

### 4.1. Nhánh một màn — ba thước đo

Ba thước đo được thiết kế để bắt đúng ba dạng lỗi khác nhau của một bản hướng dẫn.

1. **Độ trung thực** (không ảo giác):
   `Độ trung thực = 1 − (số bước tham chiếu nút không tồn tại) / (số bước có tham chiếu nút)`.
   Ví dụ: một bước ảo giác trên ba bước có tham chiếu nút cho giá trị 67%. Các bước không
   tham chiếu nút cụ thể (ví dụ “Cuộn xuống”) không tính vào mẫu số và được báo cáo riêng.

2. **Độ đúng nhãn** (gọi đúng tên hiển thị):
   `Độ đúng nhãn = (số bước gọi đúng tên) / (số bước tham chiếu nút hợp lệ)`.
   Ví dụ: “Confirm” khác “OK” nên bị tính là sai nhãn dù nút đích có thật. Đây là thước đo tự
   định nghĩa, được khai báo minh bạch là so khớp chuỗi, không đồng nhất với tính rõ ràng.

3. **Độ đúng vị trí** (grounding, point-in-bbox):
   Điểm bấm `(x, y)` hợp lệ khi nằm trong khung nút `[l, t, r, b]`, tức `l ≤ x ≤ r` và
   `t ≤ y ≤ b`. Minh hoạ: điểm bấm rơi trong khung nút lật ống kính là hợp lệ.
   **Nguồn toạ độ:** `(x, y)` do một bộ trỏ nút độc lập (kiểu ScreenSpot) dự đoán từ tên nút
   và ảnh, **không** lấy tâm khung nút đã khớp — nếu lấy tâm khung thì điểm luôn nằm trong
   khung và chỉ số trở nên vô nghĩa. Độ chính xác của bộ trỏ được đo riêng trên ScreenSpot-v2,
   nên chỉ số này được đóng khung có điều kiện theo độ chính xác của bộ trỏ.

**Căn cứ.** Point-in-bbox theo SeeClick (ACL 2024) — cũng là nguồn của ScreenSpot. So khớp
theo ngữ nghĩa thay vì so chuỗi theo ALOHa (NAACL 2024): “Save changes” và “Save” khác nhau
theo chuỗi nhưng gần nhau theo ngữ nghĩa, nên so ngữ nghĩa tránh quy oan ảo giác.

> **Khai đúng phạm vi của nhánh một màn:** sau đối chiếu, độ trung thực tăng một cách tất yếu
> vì lớp hậu kiểm gỡ chính bước ảo giác ra khỏi phép đếm. Do đó con số có ý nghĩa **không**
> phải “100% sau hậu kiểm”, mà là (a) **tỉ lệ ảo giác của bản sinh gốc** và (b) **cái giá =
> tỉ lệ bước phải chuyển sang mô tả khái quát**. Luận văn không tuyên bố lớp này làm hướng
> dẫn “đúng ý định hơn” trên một màn; phần đúng ý định được đo ở nhánh nhiều màn.

### 4.2. Nhánh nhiều màn — hai thước đo

1. **Độ đúng thứ tự** (τ thứ-tự-bộ-phận):
   `τ = (số cặp thuận − số cặp nghịch) / (số cặp bắt buộc)`, giá trị trong [−1, +1].
   Ví dụ: quỹ đạo vàng A < B < C, mô hình xếp A, C, B cho hai cặp thuận và một cặp nghịch,
   τ = +0,33. Điểm mấu chốt: **chỉ tính phạt trên cặp bắt buộc**. Cặp không ràng buộc thứ tự
   (ví dụ điền email và số điện thoại, làm trước sau đều được) khi đảo vẫn tính hợp lệ, tránh
   phạt oan. Nhãn “cặp bắt buộc” suy từ quỹ đạo vàng theo quy tắc nhân quả (màn B chỉ xuất
   hiện sau khi thực thi thao tác vàng trên màn A), **không** lấy từ mô hình.

2. **Độ hoàn thành tác vụ** (Step-SR):
   `Step-SR = (số bước thực hiện đúng) / (số bước của quỹ đạo vàng)`.
   Một bước đúng khi đúng loại thao tác (chạm, gõ, cuộn) và điểm bấm sai lệch không quá 14%
   kích thước màn so với toạ độ vàng (hoặc rơi cùng khung nút). Chuẩn hoá theo độ dài quỹ đạo
   vàng. Được báo cáo theo chế độ teacher-forced (đưa màn vàng ở mỗi bước) làm trục tham
   chiếu chuẩn ngành.

**Căn cứ.** Ngưỡng dung sai 14% trích từ AITW (NeurIPS 2023). Độ tương quan thứ-tự-bộ-phận
theo Fagin et al. (2006); tiền lệ dùng làm thước đo chính cho bài toán sắp thứ tự có ở Lapata
(Computational Linguistics, 2006). Cần lưu ý gọi đúng tên: công thức `(C − D) / |M|` là độ
tương quan thứ-tự-bộ-phận, **không** phải Kendall τ-b có hiệu chỉnh đồng hạng.

> **Vì sao hai thước này quan trọng:** độ đúng thứ tự đo riêng năng lực sắp xếp; độ hoàn thành
> tác vụ cung cấp con số định lượng cho mức đạt mục tiêu — bằng chứng “dùng được thật” mà
> nhánh một màn không đo được. Step-SR là cận dưới (so với một quỹ đạo vàng; các đường đúng
> khác bị tính là sai), nên luận văn báo cáo cả bản teacher-forced (đưa màn vàng ở mỗi bước)
> lẫn bản chạy tự do, để tách lỗi sắp thứ tự khỏi lỗi thao tác.

---

## 5. Tính hợp lệ của phương pháp đánh giá

Đây là phần bảo vệ trước phản biện gay gắt nhất: làm sao tin được các con số.

### 5.1. Chống vòng lặp luận lý
Nếu cùng một công cụ vừa quyết định “bước nào ảo giác nên viết lại” vừa chấm “còn ảo giác
không”, độ trung thực sẽ đạt 100% một cách hình thức. Để tránh:
- **Nhánh một màn:** lá chắn chính là con số công bố — **tỉ lệ ảo giác của bản sinh gốc**
  (trước hiệu chỉnh), không phải con số gần 100% sau hiệu chỉnh vốn là trần do thiết kế. Bổ
  trợ: công cụ quyết định và công cụ chấm điểm khác nhau, kèm một bộ thẩm định khác họ.
- **Nhánh nhiều màn:** nhãn “cặp bắt buộc” suy từ quỹ đạo vàng theo quy tắc nhân quả, không
  lấy từ mô hình, nên thước đo độc lập với đối tượng được chấm.

### 5.2. Kiểm định độ nhạy bằng nhiễu loạn có kiểm soát
Chèn lỗi đã biết vào một hướng dẫn đúng rồi kiểm tra thước đo có phát hiện: thêm một nút
không tồn tại thì độ trung thực phải giảm; thay tên bằng đồng nghĩa (“Save” thành “Lưu”, nút
vẫn có) thì độ trung thực giữ nguyên còn độ đúng nhãn giảm. Cách này chứng minh thước đo nhạy
với lỗi. Tiền lệ: Sai et al. (EMNLP 2021). Luận văn báo cáo cả đường cong phát hiện ở vùng
gần đồng nghĩa (trường hợp khó nhất) để bộc lộ giới hạn thay vì che giấu.

### 5.3. Thiết kế thống kê
Tính khoảng tin cậy theo cụm ứng dụng (các màn cùng một ứng dụng không độc lập, nếu tính như
độc lập thì khoảng tin cậy hẹp giả tạo); báo khoảng tin cậy 95% kèm độ lớn hiệu ứng; hiệu
chỉnh đa kiểm định Holm cho nhiều thước đo; cố định hạt giống ngẫu nhiên với mười nghìn lần
lấy mẫu lại; đăng ký giả thuyết và ngưỡng trước khi quan sát kết quả. Theo nguyên tắc này,
ở nhánh đánh giá, kết quả không khác biệt vẫn là một đóng góp vì đã đăng ký trước.

---

## 6. Hai đóng góp, giới hạn và hướng phát triển

### 6.1. Hai đóng góp song song
- **Đóng góp A — hệ thống sinh hướng dẫn giảm ảo giác.** Một lớp hậu kiểm gắn được vào bất kỳ
  mô hình nào (độc lập mô hình), phát hiện bước tham chiếu nút không tồn tại và chuyển thành
  mô tả khái quát, kèm khối sắp thứ tự màn cho tác vụ nhiều màn.
- **Đóng góp B — phương pháp đánh giá không cần bản mẫu và không tự chấm.** Bộ thước đo trên
  một màn và nhiều màn, kèm cơ chế chống vòng lặp luận lý, kiểm định độ nhạy và thiết kế thống
  kê chặt.

Hai đóng góp được đặt ngang nhau về vai trò. Ở thời điểm báo cáo, nhánh một màn đã có kết quả
sơ bộ (tỉ lệ ảo giác của bản sinh gốc khoảng một phần tư số bước; cái giá khoảng 19% số bước
chuyển sang mô tả khái quát; trên mẫu nhỏ, một mô hình, khoảng tin cậy còn chạm 0). Nhánh
nhiều màn đang được chạy. Vị thế ngang nhau được giữ vững với điều kiện độ hoàn thành tác vụ
cho kết quả dương thực — không do thiết kế mà có. Đây là mốc thiết kế; con số định lượng đầy
đủ sẽ được bổ sung.

### 6.2. Giới hạn được nêu chủ động
1. Nhánh một màn chỉ đo độ trung thực với giao diện, chưa đo mức đúng ý định; mức đúng ý định đo ở nhánh
   nhiều màn.
2. Độ trung thực gần 100% sau đối chiếu là trần do thiết kế; báo cáo tỉ lệ ảo giác của bản
   sinh gốc và cái giá kèm theo.
3. Danh sách nút là ảnh chụp một trạng thái; nút chỉ hiện sau khi cuộn có thể bị nhận nhầm,
   cần lọc các bước này.
4. Triển khai từ ảnh đơn thuần cần bộ dò nút và chịu sai số; độ bao phủ được đo trước (điều
   kiện K1). Trên thiết bị, cây trợ năng do hệ điều hành cung cấp trực tiếp.
5. Chưa có bảng số định lượng tiếng Việt do thiếu dữ liệu chuẩn; phần định lượng chạy trên dữ
   liệu tiếng Anh, tiếng Việt dừng ở minh hoạ định tính.

### 6.3. Hướng phát triển
Mô hình thế giới tự huấn luyện cho suy luận trật tự; chấm định lượng tiếng Việt trên ứng dụng
thực; mở rộng sang nhánh web với bộ dữ liệu tương ứng.

---

## Phụ lục — Câu hỏi phản biện dự kiến và cách trả lời

**H: Lớp hậu kiểm quá đơn giản, đóng góp nằm ở đâu?**
Đ: Đóng góp nằm ở phát hiện thực nghiệm và cách đánh giá, không ở độ phức tạp mã nguồn. Có
đối chứng một phương án thay thế thất bại đo được (thay nút gần nhất gây lỗi ngầm), có đo trên
nhiều mô hình, và có nhánh nhiều màn cho con số năng lực thật. Nhiều công trình được công nhận
ở hội nghị hàng đầu có quy trình gọn tương tự (G-Eval, FActScore, ALOHa).

**H: Độ trung thực đạt 100% thì chứng minh được gì?**
Đ: Con số ~100% là trần do thiết kế, không phải kết quả. Con số được báo cáo là tỉ lệ ảo giác
của bản sinh gốc và tỉ lệ bước phải chuyển sang mô tả khái quát.

**H: Thực tiễn lấy đâu ra danh sách nút?**
Đ: Trên thiết bị, cây trợ năng do hệ điều hành cung cấp trực tiếp — đây là kịch bản trợ năng
thực tế. Với ảnh đơn thuần, dùng bộ dò nút và đóng khung số liệu theo độ bao phủ đã đo.

**H: Vì sao không đưa danh sách nút cho mô hình để nó viết đúng luôn?**
Đ: Vì mục tiêu đo lường là ảo giác. Nếu cung cấp danh sách nút khi sinh thì không còn đo được
mô hình tự ảo giác bao nhiêu. Khi triển khai, có thể cung cấp; khi nghiên cứu, cố ý tách ra.

**H: τ ở đây có phải Kendall τ-b không?**
Đ: Không. Công thức `(C − D) / |M|` là độ tương quan thứ-tự-bộ-phận theo Fagin et al. (2006),
tính trên cặp bắt buộc; luận văn gọi đúng tên để tránh nhầm với τ-b có hiệu chỉnh đồng hạng.

**H: Sắp thứ tự ảnh đã có người làm (Sort-Story, RankGPT) — điểm mới ở đâu?**
Đ: Luận văn thừa nhận tiền lệ sắp thứ tự ảnh (Sort-Story, EMNLP 2016; Wu et al., ACL 2022;
RankGPT, EMNLP 2023). Điểm mới không phải bản thân việc sắp thứ tự, mà là: đặt nó vào **miền
giao diện phần mềm**, **điều kiện hoá theo mục tiêu người dùng**, **gắn kết quả sắp thứ tự với
việc sinh hướng dẫn**, và **chấm bằng độ tương quan thứ-tự-bộ-phận suy từ quỹ đạo vàng** (chỉ
phạt cặp bắt buộc) thay vì tương quan toàn cục.

---

## Bảng nguồn trích dẫn (đã kiểm)

| Thành phần | Nguồn | Nơi công bố |
|---|---|---|
| So khớp tên nút theo ngữ nghĩa | ALOHa | NAACL 2024 (short) |
| Point-in-bbox, ScreenSpot gốc | SeeClick | ACL 2024 |
| ScreenSpot-v2 (làm sạch nhãn) | OS-Atlas | ICLR 2025 |
| Ngưỡng dung sai 14% | AITW | NeurIPS 2023 |
| Quỹ đạo vàng nhiều màn | AndroidControl (Li et al.) | NeurIPS 2024 (D&B) |
| Độ tương quan thứ-tự-bộ-phận | Fagin et al., “Comparing partial rankings” | 2006 |
| Tiền lệ τ làm thước đo sắp thứ tự | Lapata | Computational Linguistics, 2006 |
| Kiểm định thước đo bằng nhiễu loạn | Sai et al. | EMNLP 2021 |
| Khung đánh giá dữ liệu tổng hợp | Chim, Ive, Liakata | Computational Linguistics 51(1), 2025 |
