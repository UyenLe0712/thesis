# Bản trình bày bảo vệ — Sinh tự động hướng dẫn sử dụng phần mềm từ ảnh giao diện

> Tài liệu dùng khi trình bày trước giảng viên hướng dẫn. Bố cục: (1) Bài toán — (2) Dữ liệu
> — (3) Phương pháp (pipeline) — (4) Đánh giá (metric) — (5) Tính hợp lệ — (6) **Bộ thí nghiệm**
> — (7) Đóng góp, giới hạn. Mỗi mục gồm: nội dung trình bày, luận điểm khoa học, và căn cứ
> trích dẫn. Văn phong báo cáo, không dùng lối nói.
>
> **Trọng tâm buổi trình bày:** thầy đã duyệt phần **dữ liệu** (ba bộ, `report/48`) nên mục 2
> chỉ nói vắn tắt để lấy ngữ cảnh; sức nặng dồn vào **pipeline (mục 3), metric (mục 4) và bộ
> thí nghiệm (mục 6)** — ba phần cần thầy phê duyệt kế hoạch chứng minh.
>
> **Nếu thầy hỏi “tham khảo ở đâu, sao em biết bài đó”:** mỗi chú thích *“Cơ sở …”* trong thân
> bài là bản rút gọn; bản đầy đủ nằm ở **Phụ lục C** (C.1–C.19) — mỗi bài gồm bốn phần: (1) công
> bố ở đâu, (2) nói gì kèm con số cụ thể, (3) mình mượn gì và ranh giới, (4) **em tìm ra bài đó
> nhờ đâu**. Mục **C.0** trả lời thẳng câu “sao em biết mấy bài này mà đọc” bằng cách kể lại
> đường tìm từ bài neo (Chim, Ive & Liakata) toả ra các nhánh từ khoá. Mỗi chú thích dưới đây
> đều ghi rõ trỏ tới mục C nào.
>
> *Cập nhật 2026-07-08 (bản 2): (a) THÊM mục 6 “Bộ thí nghiệm” — bảy thí nghiệm cốt lõi, ngưỡng
> đậu/rớt đăng ký trước, thứ tự chạy, cổng chặn — đồng bộ với `report/43` Ch.13; (b) đẩy phần
> đóng góp/giới hạn xuống mục 7. Bản 1 cùng ngày đã: đồng bộ chốt mẫu dữ liệu (`report/48`) và
> quyết định M1–M5 (`report/40`) — con số mẫu ba bộ, rút phép đo trỏ đúng vị trí khỏi bộ thước
> một màn (M1), làm rõ thống kê cụm-ứng-dụng nhiều cụm cỡ-một + estimand macro theo app.*

---

## 0. Định vị đề tài trong một đoạn

Luận văn giải quyết bài toán: cho một hoặc nhiều ảnh chụp màn hình phần mềm cùng một câu
hỏi bằng ngôn ngữ tự nhiên, hệ thống tự động sinh ra bản hướng dẫn thao tác theo từng bước
cho người đọc. Đây là bài toán đa phương thức (ảnh và văn bản sinh ra văn bản). Điểm khó
cốt lõi không nằm ở việc sinh văn bản, mà ở chỗ **không tồn tại tập hướng dẫn chuẩn do con
người biên soạn** để làm mốc đánh giá, trong khi các mô hình ngôn ngữ thị giác lại thường
**tham chiếu tới những nút không có thật trên màn hình**. Luận văn vì vậy có hai đóng góp
song song và ngang nhau **(có điều kiện — xem mục 7.1)**: một **hệ thống sinh hướng dẫn** hạn chế được lỗi ảo giác giao diện,
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

> *Phần này thầy đã duyệt (chốt mẫu ở `report/48`), khi trình bày chỉ nói vắn tắt để lấy ngữ
> cảnh: mỗi bộ đóng vai gì và con số mẫu đã chốt. Chi tiết dưới đây để tra cứu và phòng thủ
> câu hỏi.*

Nguyên tắc chọn dữ liệu: xương sống phương pháp chỉ dựa trên nguồn đã được bình duyệt; công
cụ kỹ thuật có thể là bản tiền ấn phẩm nhưng không được trình bày như đã bình duyệt.

| Bộ dữ liệu | Nội dung | Nhãn có sẵn | Vai trò | Mẫu đã chốt |
|---|---|---|---|---|
| **MobileViews** (một màn) | Ảnh + cây phân cấp giao diện (View Hierarchy) + toạ độ nút | Không có quỹ đạo vàng | Đánh giá độ trung thực với giao diện trên một màn | **127 màn / 30 ứng dụng** (mẫu phân tầng, sau khử trùng) |
| **AndroidControl** (nhiều màn) | Chuỗi màn của một tác vụ + cây trợ năng + thao tác đúng từng bước | Có quỹ đạo vàng | Đánh giá sắp thứ tự màn và hoàn thành tác vụ | **286 tập lõi** (N∈{4,5,6}) / **237 ứng dụng**, thêm 48 tập tầng N-dài |
| **ScreenSpot-v2** (đối chứng) | Ảnh + toạ độ nút chuẩn cho bài trỏ đúng nút | Có toạ độ chuẩn | Kiểm định độc lập độ chính xác trỏ đúng nút | **501 mục di động** (290 chữ / 211 biểu tượng) |

### 2.1. MobileViews — nhánh một màn
Mỗi ảnh đi kèm cây phân cấp giao diện: danh sách nút, nhãn hiển thị và toạ độ khung của từng
nút. Đây chính là **mốc neo (nhãn bạc)** thay cho bản hướng dẫn mẫu: ta không có hướng dẫn
chuẩn, nhưng ta có danh sách nút thật để kiểm tra mô hình có tham chiếu sai hay không. Ràng
buộc bất biến: **danh sách nút chỉ tham gia ở bước đánh giá, tuyệt đối không cung cấp cho mô
hình ở bước sinh**, nhằm tránh rò rỉ thông tin.

Mẫu đã chốt gồm **127 màn thuộc 30 ứng dụng** (chạy bộ, tuyển việc, game, thermostat,
kế toán, bán lẻ…), rút từ bản công khai MobileViews bằng tiêu chí lọc **đăng ký trước** rồi
khử trùng theo chữ ký cấu trúc cây giao diện — nên đây là số **mẫu hiệu dụng thật**, không
phải toàn bộ tập nguồn. Mẫu trải rộng độ phủ nhãn có chủ đích (55 màn phủ thấp, 38 trung, 45
cao) để kiểm tra thước đo ở cả màn nhiều biểu tượng lẫn màn nhiều chữ. MobileViews là bản
tiền ấn phẩm (arXiv 2409.14337, giấy phép MIT), thu thập tự động — hạn chế này được nêu chủ
động và bù bằng đối chứng ScreenSpot-v2 đã bình duyệt.

Lưu ý về chất lượng mốc neo: cây phân cấp giao diện có thể thiếu hoặc gán nhãn không đầy đủ
(nút không có nhãn văn bản, nhãn chung như “Button”). Để tránh phạt oan một bước đúng khi nút
tương ứng vắng nhãn, luận văn **đo và báo cáo độ phủ nhãn** (tỉ lệ nút thao tác được có nhãn
dùng được) và **loại các nút nhãn chung khỏi mẫu số độ trung thực**. Tính không đầy đủ của cây
trợ năng là hạn chế đã được ghi nhận trong tài liệu trợ năng Android (nêu ở mục 7.2).

*Cơ sở: không coi cây giao diện là chuẩn vàng — Chen et al. (ICSE 2020, Distinguished Paper) đo được phần lớn phần tử ảnh bấm được thiếu nhãn trợ năng (≈77% ảnh bấm được ở cấp phần tử; ~62% ứng dụng có nút-ảnh không nhãn), nên metadata giao diện không đủ tin làm ground-truth; vì vậy ta hậu-kiểm rồi né bịa bằng nhánh dự phòng thay vì tin tuyệt đối vào View Hierarchy. → Phụ lục C.17 (đầy đủ: công bố · nói gì kèm số · mình mượn gì · em tìm ra nhờ đâu).*

### 2.2. AndroidControl — nhánh nhiều màn
Mỗi tập là một chuỗi màn của một tác vụ hoàn chỉnh, kèm thao tác đúng ở mỗi bước và thứ tự
đúng của các màn. Cây trợ năng đóng vai trò tương đương View Hierarchy. Bộ này đã được bình
duyệt (Li et al., NeurIPS 2024, Datasets & Benchmarks; giấy phép CC0), cung cấp **quỹ đạo
vàng** — điều mà MobileViews không có — nên là nền tảng cho phép đo trật tự và mức hoàn thành
tác vụ. Khi thử nghiệm, các màn được xáo trộn để mô hình tự sắp xếp lại; quỹ đạo vàng chỉ
dùng để đối chiếu.

*Cơ sở: chấm hoàn thành tác vụ theo Step-Accuracy (teacher-forced) như AndroidControl (Li et al., NeurIPS 2024 D&B) — dùng đúng trục tham chiếu chuẩn ngành, không tự chế. → Phụ lục C.10 (đầy đủ: công bố · nói gì kèm số · mình mượn gì · em tìm ra nhờ đâu).*

Mẫu đã chốt: **286 tập lõi** có độ dài N∈{4,5,6} thuộc **237 ứng dụng**, cộng **48 tập tầng
N-dài** (N từ 7 đến 10) để báo đường cong độ đúng thứ tự theo độ dài. Mọi mốc N đều có đủ số
tập cho phân tầng. Hai điểm cần khai minh bạch khi trình bày: (a) nguồn lấy qua bản chia lại
`smolagents/android-control` trên HuggingFace — **không phải** tập kiểm tra giữ-lại chính
thức; điều này vô hại về rò rỉ vì luận văn chạy **zero-shot**, không tinh chỉnh trên
AndroidControl; (b) tập kiểm tra chính thức gồm bốn mảng con chồng nhau (tổng 2.855), số tập
duy nhất sau khử trùng khoảng 1.540 — nên **không** trình bày “2.855” như kích thước tập
kiểm tra.

### 2.3. ScreenSpot-v2 — đối chứng grounding
Là chuẩn phổ biến cho bài toán trỏ đúng nút từ mô tả. Vai trò: **kiểm định độc lập** độ chính
xác của bộ trỏ nút, trên dữ liệu tách khỏi tập đánh giá chính. Lý do cần bộ này: MobileViews
hiện là bản tiền ấn phẩm, nên cần một chuẩn đã bình duyệt để củng cố độ tin cậy của phép đo
trỏ đúng nút. ScreenSpot-v2 là bản làm sạch nhãn (OS-Atlas, ICLR 2025; giấy phép Apache-2.0);
phiên bản gốc thuộc SeeClick (ACL 2024). Dùng trọn **501 mục di động** (290 mục chữ, 211 mục
biểu tượng; nền iOS 238, Android 211, cửa hàng 52). Lưu ý khi trình bày: chỉ phần nền Android
mới bảo chứng trực tiếp cho MobileViews (cùng nền tảng); nên phép đo trỏ đúng nút được báo cáo
như **đối chứng độc lập** chứ không phải thước đo trong bộ chính của nhánh một màn (xem 4.1).

*Cơ sở: chấm "bấm trúng nút" bằng point-in-bbox theo SeeClick (Cheng et al., ACL 2024) — một dự đoán tính đúng khi điểm bấm rơi trong khung nút chuẩn; bộ đối chứng dùng ScreenSpot-v2 đã bình duyệt (OS-Atlas, ICLR 2025). → Phụ lục C.12 (SeeClick) và C.13 (ScreenSpot-v2).*

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

*Cơ sở (lối "sinh trước – kiểm sau"): phần đối chiếu kế thừa lối chấm của FActScore (Min et al., EMNLP 2023) — tách văn bản thành đơn vị nhỏ (mỗi bước hướng dẫn) rồi kiểm từng cái với nguồn ngoài (View Hierarchy). Lưu ý FActScore chỉ chấm văn bản có sẵn, không sinh; bước sinh-mù trước và luật "chỗ bịa chỉ mô tả, không đoán nút khác" là phần mới của ta. → Phụ lục C.3 (có khai thẳng ranh giới: FActScore chỉ chấm, không sinh).*

*Cơ sở (khớp bằng ngữ nghĩa, không so chuỗi cứng): theo ALOHa (NAACL 2024) — ALOHa bỏ so-chuỗi từ-vựng kiểu CHAIR, dùng tương đồng ngữ nghĩa và bắt được nhiều ảo giác hơn hẳn; nhờ vậy "Save changes" và "Save" không bị quy oan là bịa. → Phụ lục C.4 (đầy đủ: công bố · nói gì kèm số · mình mượn gì · em tìm ra nhờ đâu).*

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
thuẫn vòng (A > B > C > A), phá vòng bằng cách xấp xỉ **tập cung phản hồi tối thiểu**; trọng
số cạnh lấy từ **biên Copeland / tính nhất quán khi hỏi lặp / số cạnh phải bỏ tối thiểu**,
**không** dùng độ tin cậy do mô hình tự khai (mô hình ngôn ngữ thị giác hiệu chỉnh độ tin cậy
kém, nên tin vào nó sẽ sai). Khi sắp xếp, mô hình chỉ thấy ảnh đã che thanh trạng thái (đồng
hồ, pin, huy hiệu) và mục tiêu; quỹ đạo vàng chỉ dùng khi đánh giá.

*Cơ sở (động lực tách khối sắp thứ tự): TOMATO (ICLR 2025, Poster) chỉ ra mô hình ảnh-ngôn ngữ đọc chuỗi khung hình như "túi khung hình" (bag-of-frames), suy luận trật tự thời gian rất yếu — đây là bằng chứng ở miền video nên ta chỉ dùng làm động lực, còn năng lực thật trên ảnh giao diện thì tự đo lại qua cổng K-pair. → Phụ lục C.19 (khai thẳng ranh giới: bằng chứng miền video, dùng làm động lực).*

*Cơ sở (so từng cặp thay vì sắp cả dãy): Qin et al. (Findings NAACL 2024) chứng minh so-cặp (pairwise ranking prompting) cho thứ tự chuẩn và ổn định hơn hẳn kiểu bảo model xếp cả danh sách một lần. → Phụ lục C.5 (đầy đủ: công bố · nói gì kèm số · mình mượn gì · em tìm ra nhờ đâu).*

*Cơ sở (tổng hợp bằng Copeland): bài toán gộp nhiều phán đoán so-cặp thành một thứ tự (rank aggregation) đã được Dwork et al. (WWW 2001) đặt nền và bình duyệt; trong khung đó ta chọn Copeland — đếm số "trận thắng đứng-trước" — vì nó đơn giản, tái lập được và để lại dấu vết bắt mâu thuẫn (phương pháp Copeland có trụ riêng: Saari & Merlin, Economic Theory 1996). → Phụ lục C.6 (khai thẳng bẫy: Dwork đặt nền bài toán nhưng KHÔNG dùng Copeland — trụ Copeland là Saari & Merlin).*

*Cơ sở (phá vòng mâu thuẫn): cắt ít phán đoán nhất để hết vòng chính là tập cung phản hồi tối thiểu (min-feedback-arc-set) — đúng bài toán tổng-hợp-hạng-từ-so-cặp mà Ailon et al. (J. ACM 2008) đã hình thức hoá. → Phụ lục C.7 (đầy đủ: công bố · nói gì kèm số · mình mượn gì · em tìm ra nhờ đâu).*

Trước khi tổng hợp Copeland, luận văn đặt một **cổng kiểm tra (K-pair)**: đo độ chính xác so
cặp thô của mô hình so với quỹ đạo vàng. Nếu độ chính xác xấp xỉ 0,5 (đoán mò) thì bước sắp
thứ tự vô hiệu và luận văn khai thẳng điều đó thay vì báo con số Copeland đẹp giả tạo.

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

*Cơ sở (khung tổng thể): cả bộ đánh giá theo khung Intrinsic + Extrinsic của Chim, Ive & Liakata (Computational Linguistics 51(1), 2025) — họ dùng đúng khung này để đánh giá văn bản sinh tự động khi không có bản mẫu chuẩn; ta kế thừa khung đánh giá, không kế thừa bài toán sinh (họ làm text→text). → Phụ lục C.1 (đây là bài neo; C.0 kể đường từ bài này toả ra các nhánh còn lại).*

### 4.1. Nhánh một màn — hai thước đo chính (grounding tách thành đối chứng độc lập)

Nhánh một màn có **hai thước đo chính**, mỗi thước đo bắt một dạng lỗi riêng của bản hướng
dẫn. Phép đo trỏ đúng vị trí (grounding) **được rút khỏi bộ thước đo một màn** và chuyển
thành đối chứng độc lập — lý do nêu ở cuối mục.

1. **Độ trung thực** (không ảo giác):
   `Độ trung thực = 1 − (số bước tham chiếu nút không tồn tại) / (số bước có tham chiếu nút)`.
   Ví dụ: một bước ảo giác trên ba bước có tham chiếu nút cho giá trị 67%. Các bước không
   tham chiếu nút cụ thể (ví dụ “Cuộn xuống”) không tính vào mẫu số và được báo cáo riêng.

2. **Độ đúng nhãn** (gọi đúng tên hiển thị):
   `Độ đúng nhãn = (số bước gọi đúng tên) / (số bước tham chiếu nút hợp lệ)`.
   Ví dụ: “Confirm” khác “OK” nên bị tính là sai nhãn dù nút đích có thật. Đây là thước đo tự
   định nghĩa, được khai báo minh bạch là so khớp chuỗi, không đồng nhất với tính rõ ràng.

**Vì sao rút grounding khỏi nhánh một màn (một điều chỉnh có chủ đích).** Phép đo trỏ đúng vị
trí (điểm bấm `(x, y)` nằm trong khung nút `[l, t, r, b]`) chỉ có ý nghĩa khi toạ độ `(x, y)`
do một **bộ trỏ nút độc lập** (kiểu ScreenSpot) dự đoán từ tên nút và ảnh. Nếu lấy tâm khung
nút đã khớp thì điểm luôn nằm trong khung, chỉ số hoá thành 100% một cách hình thức (vòng lặp
luận lý). Trên nhánh một màn, MobileViews không có toạ độ vàng độc lập để chấm bộ trỏ, nên
luận văn **không** đưa grounding vào bộ thước đo một màn; thay vào đó đo trỏ đúng nút ở hai
chỗ có toạ độ chuẩn: (a) **đối chứng ScreenSpot-v2** (toạ độ chuẩn, đã bình duyệt) và (b)
**nhánh nhiều màn** (có toạ độ vàng ở mỗi bước, dùng trong Step-SR — mục 4.2). Cách này loại
bỏ nguy cơ tautology tâm-khung.

**Căn cứ.** So khớp tên nút theo ngữ nghĩa thay vì so chuỗi theo ALOHa (NAACL 2024): “Save
changes” và “Save” khác nhau theo chuỗi nhưng gần nhau theo ngữ nghĩa, nên so ngữ nghĩa tránh
quy oan ảo giác. Phép trỏ đúng vị trí (point-in-bbox) và bộ đối chứng ScreenSpot theo SeeClick
(ACL 2024).

*Cơ sở (đo trung thực không cần bản mẫu): theo hướng FaithScore (Findings EMNLP 2024) — reference-free faithfulness cho mô hình ảnh-ngôn ngữ, tách câu sinh thành các "sự thật nguyên tử" rồi kiểm nhất quán với ảnh; khác biệt của ta là đối chiếu với View Hierarchy có cấu trúc thay vì tự phân rã câu. → Phụ lục C.2 (đầy đủ: công bố · nói gì kèm số · mình mượn gì · em tìm ra nhờ đâu).*

> **Khai đúng phạm vi của nhánh một màn:** sau đối chiếu, độ trung thực tăng một cách tất yếu
> vì bước đối chiếu đã gỡ chính bước ảo giác ra khỏi phép đếm. Do đó con số có ý nghĩa **không**
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

*(Chỉ số phụ — PMR, Perfect Match Rate):* ngoài hai thước chính trên, luận văn báo thêm một **chỉ số phụ** là tỉ lệ episode được sắp **đúng trọn** thứ tự bắt buộc (mọi cặp bắt buộc đều đúng) — bù cho τ (τ đo *mức* đúng trên từng cặp, PMR đo *tỉ lệ episode hoàn hảo*). Đây chỉ là chỉ số phụ, **chưa có số thật** (nhánh nhiều màn chưa chạy); trên slide con số "42/100 → 42%" chỉ là minh hoạ cách tính, không phải kết quả.

**Căn cứ.** Ngưỡng dung sai 14% trích từ AITW (NeurIPS 2023). Độ tương quan thứ-tự-bộ-phận
theo Fagin et al. (2006); tiền lệ dùng làm thước đo chính cho bài toán sắp thứ tự có ở Lapata
(Computational Linguistics, 2006). Cần lưu ý gọi đúng tên: công thức `(C − D) / |M|` là độ
tương quan thứ-tự-bộ-phận, **không** phải Kendall τ-b có hiệu chỉnh đồng hạng.

*Cơ sở (chấm thứ tự): Fagin et al. (SIAM J. Discrete Math 2006) định nghĩa khung so hai xếp-hạng-bộ-phận có cặp không-thứ-tự, và Lapata (CL 2006) dùng τ làm thước đo chính cho bài toán sắp thứ tự thông tin — nên cặp tự do (điền email/số điện thoại) đảo vẫn tính đúng; ta khai đây là near-metric ta dùng, không phải "thước duy nhất đúng". → Phụ lục C.8 (Fagin) và C.9 (Lapata — tiền lệ dùng τ chấm sắp thứ tự).*

*Cơ sở (chấm từng bước + ngưỡng 14%): Step-Accuracy theo AndroidControl (NeurIPS 2024); ngưỡng dung sai 14% lấy từ AITW (NeurIPS 2023) — trong đó một thao tác bấm tính đúng khi lệch không quá 14% kích thước màn so với thao tác vàng, hoặc rơi cùng khung nút. → Phụ lục C.11 (AITW — nguồn ngưỡng 14%) và C.10 (AndroidControl — Step-Accuracy).*

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

*Cơ sở (chấm bằng model khác họ generator): Panickssery et al. (NeurIPS 2024) chứng minh LLM nhận ra và tự thiên vị chính bài của mình (self-preference), và mức thiên vị này tỉ lệ thuận với khả năng tự-nhận-diện — nên tách judge khác họ với generator là biện pháp mạnh nhất để loại thiên vị tự-chấm; Zheng et al. (MT-Bench, NeurIPS 2023) làm trụ bổ trợ cho khung LLM-as-judge. → Phụ lục C.15 (đầy đủ: công bố · nói gì kèm số · mình mượn gì · em tìm ra nhờ đâu).*

### 5.2. Kiểm định độ nhạy bằng nhiễu loạn có kiểm soát
Chèn lỗi đã biết vào một hướng dẫn đúng rồi kiểm tra thước đo có phát hiện: thêm một nút
không tồn tại thì độ trung thực phải giảm; thay tên bằng đồng nghĩa (“Save” thành “Lưu”, nút
vẫn có) thì độ trung thực giữ nguyên còn độ đúng nhãn giảm. Cách này chứng minh thước đo nhạy
với lỗi. Tiền lệ: Sai et al. (EMNLP 2021). Luận văn báo cáo cả đường cong phát hiện ở vùng
gần đồng nghĩa (trường hợp khó nhất) để bộc lộ giới hạn thay vì che giấu.

*Cơ sở (validate thước đo bằng nhiễu loạn): Sai et al. (EMNLP 2021) dùng perturbation checklist bơm lỗi đã biết (phủ định, trái nghĩa…) và cho thấy nhiều metric NLG phổ biến không nhạy ngay cả với nhiễu đơn giản — ta mượn đúng quy trình này để đo độ nhạy mà không cần người chấm; đây là điều kiện CẦN về độ nhạy, chưa phải convergent validity. → Phụ lục C.14 (đầy đủ: công bố · nói gì kèm số · mình mượn gì · em tìm ra nhờ đâu).*

*Cơ sở (không lấy chấm-người làm cổng đậu/rớt): Clark et al. (ACL-IJCNLP 2021) cho thấy người không được huấn luyện phân biệt văn bản GPT-3 với văn bản người chỉ ở mức ngẫu nhiên (huấn luyện nhanh cũng chỉ nâng tới ~55%), nên chấm-người với văn bản máy-sinh vốn thiếu ổn định — ta để human-correlation làm đối chiếu tương lai, không làm cổng đậu/rớt. → Phụ lục C.18 (trụ khái niệm — không đo trực tiếp trên dữ liệu của ta).*

### 5.3. Thiết kế thống kê
Tính khoảng tin cậy theo cụm ứng dụng (các màn cùng một ứng dụng không độc lập, nếu tính như
độc lập thì khoảng tin cậy hẹp giả tạo); báo khoảng tin cậy 95% kèm độ lớn hiệu ứng; hiệu
chỉnh đa kiểm định Holm cho nhiều thước đo; cố định hạt giống ngẫu nhiên với mười nghìn lần
lấy mẫu lại; đăng ký giả thuyết và ngưỡng trước khi quan sát kết quả. Theo nguyên tắc này,
ở nhánh đánh giá, kết quả không khác biệt vẫn là một đóng góp vì đã đăng ký trước.

*Cơ sở (gộp cụm theo app): MacKinnon, Nielsen & Webb (Journal of Econometrics 232(2):272–299, 2023) là cẩm nang thực hành cho suy luận cụm-vững, chỉ rõ khi số cụm ít phải dùng wild-cluster bootstrap để khoảng tin cậy khỏi hẹp giả — ta gộp cụm theo app vì các màn cùng một ứng dụng không độc lập. → Phụ lục C.16 (đầy đủ: công bố · nói gì kèm số · mình mượn gì · em tìm ra nhờ đâu).*

Ba điểm cần khai minh bạch về giới hạn thống kê (nêu chủ động thay vì để phản biện phát hiện):
- **Suy luận chính dùng wild-cluster bootstrap-t** (Cameron–Gelbach–Miller, 2008) vì số cụm
  ứng dụng còn khiêm tốn; với số cụm ít, bootstrap cụm thường sẽ dưới-phủ, còn bản wild-t áp
  giả thuyết không cho khoảng tin cậy đáng tin hơn.
- **Nhiều cụm cỡ một.** Ở nhánh nhiều màn, phần lớn ứng dụng chỉ có một tập (194/237 là cụm
  đơn), nên **không** trình bày “237 cụm” như một sức mạnh thống kê lớn; báo số cụm hiệu dụng
  và cỡ mẫu hiệu dụng (`N_eff`) đi kèm.
- **Estimand là trung bình vĩ mô — mỗi ứng dụng một phiếu** (macro-average theo app), **không**
  tuyên bố “đại diện cho ứng dụng nói chung”. Dữ liệu tiếng Việt bằng không (99,97% tiếng Anh),
  nên headline định lượng là “ứng dụng di động tiếng Anh”; phần tiếng Việt dừng ở minh hoạ
  định tính.

---

## 6. Bộ thí nghiệm — chương trình chứng minh hai đóng góp

Đây là phần **thầy cần duyệt nhất**: không chỉ mô tả phương pháp mà cho thấy **kế hoạch
chứng minh** đã khép kín. Nguyên tắc xuyên suốt: mỗi đóng góp gắn với một số câu hỏi nghiên
cứu; mỗi câu hỏi gắn với một thí nghiệm cụ thể (dữ liệu + cỡ mẫu + thước đo + đối chứng +
cổng chặn); **ngưỡng đậu/rớt được đăng ký trước khi nhìn kết quả**. Ở nhánh đánh giá, kết
quả không khác biệt vẫn là đóng góp hợp lệ vì đã đăng ký trước; ở nhánh sinh, luận văn kỳ
vọng con số dương thật.

### 6.1. Bảy câu hỏi nghiên cứu

| Mã | Câu hỏi | Thuộc đóng góp |
|---|---|---|
| **RQ1** | Mô hình sinh mù tham chiếu nút không tồn tại với tần suất bao nhiêu, và **biến thiên giữa các đời model** thế nào? | A — đo hiện tượng |
| **RQ2** | Bước đối chiếu với giao diện thật có giúp giảm ảo giác không, và **giá bao nhiêu** (%bước phải hạ thành mô tả)? *(RQ2b: “chỉ mô tả” so với “đoán nút gần nhất” gây bao nhiêu lỗi ngầm?)* | A — lõi |
| **RQ3** | Phương pháp đánh giá không cần bản mẫu có **hợp lệ** không (nhạy với lỗi, không tự chấm vòng tròn, khớp người ở mức tối thiểu)? | B — lõi |
| **RQ4** | Hệ sắp lại thứ tự các màn có đúng không (hơn ngẫu nhiên? ngang/hơn đối chứng listwise? từng khối đóng góp bao nhiêu)? | A — nhiều màn |
| **RQ5** | Năng lực thao tác **từng bước** thật ra sao (Step-SR dương thật không)? | điều kiện giữ “A ngang B” |
| **RQ6** | Bộ trỏ **độc lập** trúng khung nút ở tỉ lệ nào (tách chữ / biểu tượng)? | đối chứng |
| **RQ7** | Hướng dẫn có **thực sự dùng được** với người đọc không (định tính)? | bù trục hữu ích |

### 6.2. Bảy thí nghiệm cốt lõi (đếm trung thực)

Danh sách đánh số E1–E16 dễ gây cảm giác “mười lăm việc”, nhưng đếm trung thực chỉ **khoảng
bảy thí nghiệm thật** — cách đánh số chỉ để trích chéo. Bảng dưới gộp theo việc thật:

| Thí nghiệm | Trả lời câu hỏi | Dữ liệu + cỡ mẫu | Thước đo chính | Đối chứng / cổng |
|---|---|---|---|---|
| **E1 + E2** *(một lần chạy, hai lát cắt)* | RQ1, RQ2 | MobileViews **127 màn / 30 app** (đã có); **≥2 model** (gpt-4o-mini + một frontier rẻ) | tỉ lệ ảo giác **đường cong theo model**; độ trung thực trước/sau + **%fallback** + không-gây-hại | bật/tắt lớp đối chiếu; thêm nhánh “nạp danh sách nút lúc sinh” để đo rò rỉ nội bộ; cổng K1, M4 |
| **E3** | RQ2b | toàn mẫu E2 | **tỉ lệ lỗi ngầm** (nút thật nhưng sai chức năng) | “chỉ mô tả” so với “đoán nút gần nhất” |
| **E4** | RQ3a | mẫu con MobileViews + bản sinh | phát hiện / dương-tính-giả / đơn điệu | **bơm 10–15 loại lỗi đã biết** (perturbation) |
| **E5** | RQ3b | 80–120 cặp gán tay | Precision/Recall + Cohen κ | so bộ khớp; **freeze τ trước khi chạy** |
| **E6** | RQ3c | bản sinh E2 | đồng thuận **ba cơ chế khác họ** generator | chống tự chấm |
| **E8 (+cổng E9)** | RQ4 | AndroidControl **286 tập / 237 app** (N∈{4,5,6}) | độ đúng thứ tự τ + độ chính xác so cặp + PMR + **cột chi phí** | ngẫu nhiên / so-cặp+Copeland (ta) / listwise một-shot; **cổng K-pair** |
| **E14** | RQ5 | AndroidControl (lớp Step-SR) | **Step-SR** (đúng loại ∧ ≤14%) | phân tầng theo độ dài N; cổng KB |

*Nhóm phụ trợ / tuỳ chọn (không phải chân đóng góp bắt buộc):* **E16** kiểm hữu ích định
tính với người đọc (RQ7 — bù trục “dùng được”, không làm cổng đậu/rớt); **E10–E13** một gói
ablation mổ xẻ bước sắp thứ tự (Copeland / phá vòng / chống thiên lệch vị trí / phân tích tín
hiệu) — chạy **khi** nhánh nhiều màn có kết quả, để quy công từng khối nếu dương hoặc biến số
âm thành phát hiện có cấu trúc; **E15** đối chứng trỏ đúng nút trên ScreenSpot-v2 (cần bộ trỏ
độc lập); **E7** neo người cho bộ chấm tự động (tham khảo, không cổng).

> **Vì sao đếm trung thực “bảy” lại là điểm mạnh:** nó cho thấy bộ thí nghiệm **không phình
> để trông đồ sộ**. Mỗi thí nghiệm đo một trục riêng, không trùng lặp khoa học; ma trận
> đối chiếu đầy đủ giữa từng luận điểm và từng thí nghiệm nằm ở hồ sơ nội bộ (`report/47`).

### 6.3. Ngưỡng đậu/rớt — đăng ký trước khi nhìn kết quả

Đây là cam kết khoa học mạnh nhất trước hội đồng: chốt ngưỡng **trước** khi chạy, để kết quả
không bị uốn theo mong muốn.

| Thí nghiệm | Ngưỡng đăng ký trước |
|---|---|
| E1 | frontier **vẫn ảo giác ≥5%**, cận dưới khoảng tin cậy > 0 (vấn đề chưa tự khỏi ở model mới) |
| E2 | độ trung thực tăng ở mọi ngưỡng τ; %fallback quanh 19%; chỉ số phụ đứng yên (không gây hại) |
| E3 | nhánh “đoán nút” tạo lỗi ngầm > 0, cận dưới khoảng tin cậy > 0 |
| E4 | dương-tính-giả < 5%; đơn điệu Spearman ρ > 0,8 |
| E5 | Precision ≥ 0,95; κ ≥ 0,6 |
| E8 / E9 | ta > ngẫu nhiên (khoảng tin cậy tách rời); ngang listwise nghĩa là \|Δτ\| ≤ 0,05; **cổng K-pair: độ chính xác so cặp > 0,5** |
| E14 | Step-SR dương thật (cận dưới khoảng tin cậy > 0) |

*Thiết kế thống kê áp cho mọi thí nghiệm: khoảng tin cậy bootstrap 95% theo cụm ứng dụng;
so hai hệ bằng kiểm định bắt cặp (hoán vị xấp xỉ là chính); hiệu chỉnh Holm cho nhiều thước
đo; wild-cluster bootstrap-t vì số cụm còn khiêm tốn; báo cỡ mẫu hiệu dụng và hiệu-ứng-nhỏ-
nhất-phát-hiện-được để đọc “null” cho đúng — chi tiết ở mục 5.3.*

### 6.4. Thứ tự chạy — miễn phí trước, tốn API sau

Nguyên tắc chi tiêu: chạy một lần cho đúng, ưu tiên công cụ chạy máy cục bộ miễn phí, mọi
bước tốn API đều xin ý kiến trước.

1. **Đăng ký trước (miễn phí):** chốt ngưỡng, hạt giống, τ dự kiến vào hồ sơ `report/22`
   **trước** khi nhìn bất kỳ kết quả nào.
2. **Cổng cứng miễn phí (chạy máy cục bộ):** K1 (đo độ bao phủ của bộ dò nút) · M4 (đo độ phủ
   nhãn) · KN (biểu đồ độ dài episode — đã đạt) · KB (chống rò rỉ chỉ số bước) · dựng bộ bơm
   lỗi (E4) + gán tay 80–120 cặp (E5) + bộ chấm khác họ (E6).
3. **Tốn API tối thiểu (mỗi bước xin ý kiến):** sinh câu hỏi → sinh bản gốc 127 màn (E1/E2) →
   nhánh đối chiếu + đối chứng “đoán nút” (E3) → **cổng K-pair (E9)** → nếu qua cổng: E8 và
   gói ablation → Step-SR (E14) → đối chứng grounding (E15).

> **Cổng K-pair chặn cả nhánh nhiều màn:** nếu độ chính xác so cặp thô của mô hình chỉ xấp xỉ
> 0,5 (ngang đoán mò), bước sắp thứ tự bị tuyên vô hiệu và luận văn khai thẳng — biến kết quả
> âm thành **phát hiện hợp lệ** về giới hạn suy luận trật tự của mô hình ảnh-ngôn ngữ, vẫn nộp
> được.

### 6.5. Điều kiện then chốt giữ “hai đóng góp ngang nhau”

Rủi ro thực nghiệm thật duy nhất còn lại của toàn luận văn nằm ở nhánh nhiều màn: **cổng
K-pair phải qua và Step-SR / τ phải dương thật** (E9, E14). Nếu dương, đóng góp A có con số
năng lực thật để đứng ngang đóng góp B. Nếu âm, luận văn không giấu mà trình bày như một phát
hiện có cấu trúc về giới hạn của mô hình — và trọng lượng đóng góp A vẫn được giữ bằng ba chân
đã có: đối chứng lỗi ngầm đo được (E3), tỉ lệ ảo giác của bản gốc (E1), và tỉ lệ fallback công
bố minh bạch (E2).

---

## 7. Hai đóng góp, giới hạn và hướng phát triển

### 7.1. Hai đóng góp song song
- **Đóng góp A — hệ thống sinh hướng dẫn giảm ảo giác.** Một bước đối chiếu với giao diện thật,
  gắn được vào bất kỳ mô hình nào (độc lập mô hình), phát hiện bước tham chiếu nút không tồn tại
  và viết lại thành mô tả khái quát, kèm bước sắp lại thứ tự các màn cho tác vụ nhiều màn.
- **Đóng góp B — phương pháp đánh giá không cần bản mẫu và không tự chấm.** Bộ thước đo trên
  một màn và nhiều màn, kèm cơ chế chống vòng lặp luận lý, kiểm định độ nhạy và thiết kế thống
  kê chặt.

Hai đóng góp được đặt ngang nhau về vai trò. Ở thời điểm báo cáo, nhánh một màn đã có kết quả
sơ bộ (tỉ lệ ảo giác của bản sinh gốc khoảng một phần tư số bước; cái giá khoảng 19% số bước
chuyển sang mô tả khái quát; trên mẫu nhỏ, một mô hình, khoảng tin cậy còn chạm 0). Nhánh
nhiều màn đang được chạy. Vị thế ngang nhau được giữ vững với điều kiện độ hoàn thành tác vụ
cho kết quả dương thực — không do thiết kế mà có. Đây là mốc thiết kế; con số định lượng đầy
đủ sẽ được bổ sung.

### 7.2. Giới hạn được nêu chủ động
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
6. Tiêu chí lọc mẫu MobileViews (ưu tiên màn có nhiều nút-có-nhãn) có thể làm nhẹ tỉ lệ ảo
   giác quan sát được; vì vậy tỉ lệ ảo giác được báo cáo **phân tầng theo độ phủ nhãn** như
   một kiểm tra cơ chế (phủ nhãn thấp thì ảo giác tăng), thay vì một con số “một phần tư” tĩnh.
7. Nguồn AndroidControl là bản chia lại trên HuggingFace, không phải tập kiểm tra giữ-lại
   chính thức; vô hại về rò rỉ vì luận văn chạy zero-shot, nhưng được khai rõ nguồn gốc. Dữ
   liệu do bot thu thập nên vắng các luồng đăng nhập / thanh toán — thu hẹp phạm vi kết luận.

### 7.3. Hướng phát triển
Mô hình thế giới tự huấn luyện cho suy luận trật tự; chấm định lượng tiếng Việt trên ứng dụng
thực; mở rộng sang nhánh web với bộ dữ liệu tương ứng.

---

## Phụ lục — Câu hỏi phản biện dự kiến và cách trả lời

> Mỗi câu hỏi dưới đây viết đủ ý để đọc là hiểu ngay thầy đang lo điều gì; phần trả lời bám sát
> mối lo đó.

**H1 — “Bước đối chiếu với giao diện thật nghe khá đơn giản (so tên nút rồi thay chỗ bịa bằng
mô tả). Vậy đâu là phần nghiên cứu, hay chỉ là kỹ thuật ghép nối?”**
Đ: Đóng góp nằm ở **phát hiện thực nghiệm và cách đánh giá**, không ở độ phức tạp mã nguồn. Ba
chỗ làm nó thành nghiên cứu: (a) có **đối chứng một phương án thay thế thất bại đo được** —
cách “đoán nút gần nhất” tạo ra lỗi ngầm, nên quyết định “chỉ mô tả” là kết luận rút từ thực
nghiệm; (b) đo tỉ lệ ảo giác **trên nhiều đời mô hình** để cho thấy vấn đề chưa tự khỏi; (c)
nhánh nhiều màn cho **con số năng lực thật**. Nhiều công trình ở hội nghị hàng đầu cũng có quy
trình gọn mà giá trị nằm ở phát hiện và cách đánh giá (G-Eval, FActScore, ALOHa).

**H2 — “Sau bước đối chiếu, độ trung thực gần như 100%. Con số đẹp đó chứng minh được gì, hay
chỉ là hệ quả tất yếu của việc chính lớp kiểm đã gỡ bước bịa ra khỏi phép đếm?”**
Đ: Đúng — con số ~100% là **trần do thiết kế**, không phải thành tích. Vì thế luận văn **không**
lấy nó làm kết quả, mà báo hai con số có ý nghĩa: **tỉ lệ ảo giác của bản sinh gốc** (trước khi
kiểm) và **tỉ lệ bước phải hạ thành mô tả khái quát** (cái giá phải trả).

**H3 — “Phương pháp dựa vào danh sách nút thật để chấm. Nhưng khi triển khai thực tế, phần lớn
ứng dụng đâu có sẵn danh sách đó — vậy hệ có còn dùng được không?”**
Đ: Cần tách hai thời điểm. **Lúc chấm** (nghiên cứu) mới cần danh sách nút để đo hệ bịa bao
nhiêu. **Lúc triển khai** trên điện thoại, hệ điều hành Android cấp **cây trợ năng theo thời
gian thực** cho màn đang mở, nên thường vẫn có danh sách nút thật để đối chiếu — đây là nền của
hướng chạy trên thiết bị. Khi hoàn toàn không có nguồn nút, hệ **xuống cấp an toàn**: mô tả
việc cần làm bằng lời thay vì bịa tên nút, và báo minh bạch tỉ lệ bước phải hạ thành mô tả.

**H4 — “Nếu đưa luôn danh sách nút thật cho mô hình lúc sinh thì nó viết đúng ngay, khỏi bịa.
Sao lại cố tình giấu danh sách đó đi?”**
Đ: Vì **mục tiêu đo lường chính là ảo giác**. Nếu cung cấp danh sách nút ngay lúc sinh thì
không còn đo được mô hình tự bịa bao nhiêu — lỗi bị che mất. Khi *triển khai* có thể cung cấp
danh sách; khi *nghiên cứu* thì cố ý tách ra để đo được hiện tượng. (Luận văn còn có một nhánh
thí nghiệm “nạp danh sách nút lúc sinh” để chứng minh trên chính dữ liệu của mình rằng làm vậy
sẽ che mất ảo giác — mục 6.2, E2.)

**H5 — “Em gọi thước đo thứ tự là τ. Đây có phải hệ số Kendall τ-b quen thuộc không? Nếu không
thì khác chỗ nào, kẻo nhầm tên?”**
Đ: **Không phải τ-b.** Công thức `(C − D) / |M|` là **độ tương quan thứ-tự-bộ-phận** theo Fagin
et al. (2006), chỉ tính phạt trên **cặp bắt buộc** (cặp tự do như điền email/số điện thoại đảo
vẫn đúng). τ-b là biến thể có hiệu chỉnh đồng hạng cho tương quan toàn cục — luận văn gọi đúng
tên để tránh nhầm.

**H6 — “Sắp lại thứ tự ảnh thì đã có người làm rồi (Sort-Story, RankGPT). Vậy phần này của em
mới ở chỗ nào, hay chỉ áp lại đồ có sẵn?”**
Đ: Luận văn **thừa nhận tiền lệ** (Sort-Story, EMNLP 2016; Wu et al., ACL 2022; RankGPT, EMNLP
2023). Điểm mới không phải bản thân việc sắp thứ tự, mà là bốn chỗ: đặt nó vào **miền giao diện
phần mềm**, **gắn với mục tiêu người dùng**, **nối kết quả sắp thứ tự vào việc sinh hướng dẫn**,
và **chấm bằng độ tương quan thứ-tự-bộ-phận suy từ quỹ đạo vàng** (chỉ phạt cặp bắt buộc) thay
vì tương quan toàn cục.

---

## Phụ lục C — Sổ tay phòng thủ trích dẫn (đọc để trả lời thầy)

> Phần này để học viên **hiểu và thuộc** gốc từng quyết định, phòng khi thầy hỏi "paper đó nói
> ở đoạn nào" hay "sao em tìm ra nó". Mỗi mục gồm bốn phần: (1) tên và nơi công bố đầy đủ; (2)
> nó nói gì, ở đâu (kèm con số cụ thể); (3) vì sao nó hậu thuẫn lựa chọn của mình (và ranh giới
> nếu chỉ là tiền lệ / trụ khái niệm); (4) em tìm ra nhờ đâu. Nguyên tắc vàng khi đứng đáp:
> mỗi paper chỉ là **mỏ neo** — thuộc đúng "nó làm gì → mình mượn gì → phần mới của mình là gì",
> đừng nói lấp lửng để bị bắt "paper đó đâu có chứng minh cái em nói".

### C.0. Nếu thầy hỏi: "Sao em biết mấy paper này mà đọc?"

Em xuất phát từ bài báo neo khung đánh giá mà thầy đã biết — Chim, Ive & Liakata (*Evaluating
Synthetic Data Generation from User Generated Text*, Computational Linguistics 2025) — vì đề tài
của em cũng là "đánh giá văn bản sinh tự động khi không có bản mẫu chuẩn". Từ bài đó em tỏa ra
theo ba nhánh câu hỏi: (a) **đo ảo giác mà không có đáp án mẫu** — em tra Google Scholar theo
từ khoá *reference-free hallucination / faithfulness evaluation* rồi lần related-work xuống ALOHa,
FaithScore, FActScore; (b) **sắp thứ tự các ảnh màn hình** — em tìm *pairwise ranking prompting
LLM*, *rank aggregation*, *feedback arc set*, *partial ranking with ties*; (c) **làm sao tin được
thước đo** — em tìm *perturbation-based metric validation*, *LLM self-preference bias*,
*cluster-robust inference*. Các bộ dữ liệu (ScreenSpot, AndroidControl, AITW, MobileViews) em tìm
qua Papers-with-Code và HuggingFace theo từ khoá *GUI grounding benchmark* / *Android UI control
dataset*. Cách làm nhất quán là: đọc bài neo → theo dấu trích dẫn → search từ khoá hẹp → chọn bản
đã bình duyệt làm xương sống, bản tiền ấn phẩm chỉ để bổ trợ.

---

### C.1. Chim, Ive & Liakata — khung đánh giá không-gold *(quyết định D1 — trực tiếp)*
1. **Nơi công bố:** *Evaluating Synthetic Data Generation from User Generated Text*, Jenny Chim,
   Julia Ive, Maria Liakata — **Computational Linguistics 51(1):191–233, 2025** (MIT Press;
   DOI 10.1162/coli_a_00540). Đây là **tạp chí**, không phải "ACL 2025".
2. **Nói gì, ở đâu:** đề xuất khung đánh giá thống nhất **đầu tiên** cho văn bản người-dùng sinh
   tổng hợp, gồm ba khía cạnh — *giữ phong cách, giữ nghĩa, và độ phân kỳ (proxy cho quyền riêng
   tư)* — và cung cấp **cả đánh giá nội tại (intrinsic) lẫn ngoại tại (extrinsic)**.
3. **Vì sao hậu thuẫn:** em kế thừa đúng **khung Intrinsic + Extrinsic** này cho bài toán không có
   bản mẫu chuẩn. Ranh giới: họ làm text→text và mục tiêu quyền-riêng-tư; em **chỉ mượn khung đánh
   giá**, không mượn bài toán sinh — phần mới của em là áp khung đó vào sinh hướng dẫn từ ảnh GUI.
4. **Tìm ra nhờ đâu:** đây là **bài neo** thầy giao/gợi ý; từ đây em mới tỏa ra các nhánh còn lại.

### C.2. FaithScore — đo trung thực không cần đáp án *(D3 — trực tiếp)*
1. **Nơi công bố:** *FaithScore: Fine-grained Evaluations of Hallucinations in Large Vision-Language
   Models*, Jing, Li, Chen, Du — **Findings of EMNLP 2024** (arXiv 2311.01477).
2. **Nói gì, ở đâu:** là thước đo **reference-free** cho mô hình ảnh-ngôn ngữ; quy trình ba bước —
   nhận diện câu con mang phát biểu mô tả → trích danh sách **"sự thật nguyên tử" (atomic facts)** →
   kiểm nhất quán từng sự thật với ảnh đầu vào. Meta-đánh giá cho thấy nó **tương quan cao với
   phán đoán trung thực của con người**.
3. **Vì sao hậu thuẫn:** hợp thức hoá hướng "đo trung thực không cần đáp án mẫu". Khác biệt của em:
   đối chiếu với **View Hierarchy có cấu trúc** (danh sách nút thật) thay vì để mô hình tự phân rã
   câu — nên phép kiểm của em xác định hơn.
4. **Tìm ra nhờ đâu:** search Scholar *"reference-free faithfulness vision-language"*, đây là bài
   sát nhất với miền multimodal của em.

### C.3. FActScore — lối "tách nhỏ rồi kiểm với nguồn ngoài" *(D4 — tiền lệ)*
1. **Nơi công bố:** *FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form
   Text Generation*, Min et al. — **EMNLP 2023** (main; 2023.emnlp-main.741).
2. **Nói gì, ở đâu:** tách một đoạn sinh thành **các sự thật nguyên tử** rồi tính tỉ lệ được nguồn
   tri thức tin cậy hậu thuẫn. Con số nổi bật: tiểu sử do ChatGPT sinh chỉ đạt **FActScore 58%**
   (tức 42% sự thật nguyên tử không được hậu thuẫn), tiểu sử người viết ~88%; bộ ước lượng tự động
   sai **dưới 2%** so với người.
3. **Vì sao hậu thuẫn — CHÚ Ý RANH GIỚI:** em mượn **lối chấm** (decompose + verify-against-source)
   cho bước đối chiếu. **FActScore chỉ CHẤM văn bản có sẵn, KHÔNG hề sinh.** Nếu thầy hỏi "FActScore
   sinh chỗ nào?" thì trả lời thẳng: nó không sinh; phần **sinh-mù trước** và luật **"chỗ bịa chỉ
   mô tả, không đoán nút khác"** là đóng góp mới của em, đưa ý tưởng kiểm-sau đó vào *bên trong*
   một pipeline sinh.
4. **Tìm ra nhờ đâu:** cùng cụm với FaithScore khi search *"atomic fact verification factuality"*;
   FActScore là bản gốc của lối atomic-check nên em trích như tiền lệ phương pháp.

### C.4. ALOHa — khớp bằng ngữ nghĩa, bỏ so chuỗi cứng *(D2 — tiền lệ)*
1. **Nơi công bố:** *ALOHa: A New Measure for Hallucination in Captioning Models*, Petryk et al. —
   **NAACL 2024 (Short Papers)** (arXiv 2404.02904).
2. **Nói gì, ở đâu:** dùng mô hình ngôn ngữ để đo ảo giác **theo từ vựng mở**, bỏ so-chuỗi cố định
   kiểu CHAIR. Kết quả: bắt được **13,6% ảo giác nhiều hơn CHAIR trên HAT** (tập vàng con của MS
   COCO) và **30,8% nhiều hơn trên nocaps** (đối tượng ngoài danh mục COCO).
3. **Vì sao hậu thuẫn:** biện minh cho việc em **khớp tên nút bằng ngữ nghĩa** thay vì so chuỗi —
   nhờ vậy "Save changes" và "Save" gần nhau, không bị quy oan là bịa. Ranh giới: ALOHa làm ở miền
   chú thích ảnh (object hallucination); em **mượn nguyên lý khớp-ngữ-nghĩa**, áp vào so tên nút với
   View Hierarchy.
4. **Tìm ra nhờ đâu:** search *"open-vocabulary hallucination metric captioning"*; ALOHa là bài mới
   nhất thay CHAIR nên em lấy làm trụ cho lựa chọn ngữ-nghĩa.

### C.5. Qin et al. — so từng cặp thay vì sắp cả dãy *(D5 — tiền lệ)*
1. **Nơi công bố:** *Large Language Models are Effective Text Rankers with Pairwise Ranking
   Prompting*, Qin et al. — **Findings of NAACL 2024** (2024.findings-naacl.97).
2. **Nói gì, ở đâu:** đưa hai ứng viên cho LLM và hỏi cái nào hơn (pairwise). Trên **7 tác vụ BEIR**,
   PRP vượt ChatGPT **4,2%** và vượt lối pointwise **hơn 10%** NDCG@10; với FLAN-UL2 20B còn sánh
   ngang các lối tốt nhất dựa trên GPT-4.
3. **Vì sao hậu thuẫn:** hợp thức hoá quyết định cho mô hình **so từng cặp màn** thay vì bắt nó xếp
   cả danh sách một lần — so-cặp cho thứ tự ổn định hơn. Ranh giới: họ xếp hạng tài liệu theo độ liên
   quan; em áp so-cặp cho **thứ tự thời gian giữa các màn**, tổng hợp thêm bằng Copeland.
4. **Tìm ra nhờ đâu:** search *"pairwise ranking prompting LLM"* khi tìm cách để mô hình sắp thứ tự
   mà ít lỗi.

### C.6. Dwork et al. + Saari & Merlin — tổng hợp phiếu thành một thứ tự *(D6 — tiền lệ; có bẫy)*
1. **Nơi công bố:** *Rank Aggregation Methods for the Web*, Dwork, Kumar, Naor & Sivakumar —
   **WWW 2001 (ACM, pp. 613–622)** cho **bài toán** tổng hợp hạng. Phương pháp **Copeland** lấy trụ
   học thuật riêng: **Saari & Merlin, Economic Theory 8:51–76 (1996)** (bản gốc A.H. Copeland 1951
   chưa xuất bản).
2. **Nói gì, ở đâu:** Dwork et al. hình thức hoá bài toán gộp nhiều xếp hạng nguồn thành một, nêu
   bài toán **Kemeny-Young** (NP-hard) và đề xuất **thuật toán Markov-chain MC4** là tốt nhất trong
   thực nghiệm của họ. Copeland (Saari–Merlin) là quy tắc **đếm số "trận thắng đối đầu"** để xếp hạng.
3. **Vì sao hậu thuẫn — CHÚ Ý BẪY:** Dwork et al. là **trụ bình-duyệt cho BÀI TOÁN** rank-aggregation,
   **KHÔNG** phải bằng chứng "họ dùng Copeland" — chữ ký của họ là Markov-chain/Kemeny. Nếu thầy hỏi
   "Dwork có dùng Copeland không?" thì trả lời thẳng: **không**; em **chọn** Copeland trong khung
   rank-aggregation đã bình duyệt vì nó đơn giản, tái lập được và để lại dấu vết bắt mâu thuẫn — và
   trụ đúng-danh cho Copeland là Saari & Merlin (1996).
4. **Tìm ra nhờ đâu:** search *"rank aggregation from pairwise comparisons"* → Dwork WWW 2001 là bài
   kinh điển; khi cần trụ đúng cho riêng Copeland em tra *"Copeland method social choice"* → Saari &
   Merlin.

### C.7. Ailon, Charikar & Newman — phá vòng mâu thuẫn *(D7 — tiền lệ)*
1. **Nơi công bố:** *Aggregating Inconsistent Information: Ranking and Clustering*, Ailon, Charikar &
   Newman — **Journal of the ACM 55(5), Article 23, 2008** (bản sơ bộ STOC 2005).
2. **Nói gì, ở đâu:** với thông tin mâu thuẫn (giải đấu — tournament), tìm lời giải nhất quán toàn
   cục **cực tiểu hoá bất đồng**; kích thước **tập cung phản hồi tối thiểu** bằng số cạnh lùi ít nhất
   mà một thứ tự tuyến tính gây ra. Bài cho thuật toán xấp xỉ có bảo đảm.
3. **Vì sao hậu thuẫn:** khi các phán đoán so-cặp tạo vòng (A>B>C>A), em **cắt ít cạnh nhất để hết
   vòng** — đúng bài toán min-feedback-arc-set mà bài này hình thức hoá. Ranh giới: họ chứng minh
   xấp xỉ/độ khó; em dùng **phát biểu bài toán** làm nền cho bước phá vòng.
4. **Tìm ra nhờ đâu:** search *"minimum feedback arc set tournament ranking"* khi cần cách xử lý mâu
   thuẫn thứ tự.

### C.8. Fagin et al. — chấm bằng thứ-tự-bộ-phận *(D8 — trực tiếp)*
1. **Nơi công bố:** *Comparing partial rankings*, Fagin, Kumar, Mahdian, Sivakumar & Vee — **SIAM
   Journal on Discrete Mathematics 20(3):628–648, 2006**.
2. **Nói gì, ở đâu:** định nghĩa khung so **hai xếp hạng bộ phận** (có đồng hạng / có cặp không so
   được), tổng quát hoá Kendall τ và Spearman. *(Cần bạn tự xác nhận lại số trang 628–648 trên bản
   SIAM khi in — em lấy từ hồ sơ nội bộ report/39.)*
3. **Vì sao hậu thuẫn:** cho phép em **chỉ phạt cặp bắt buộc** và bỏ qua cặp tự do (điền email/số
   điện thoại đảo vẫn đúng). Ranh giới trung thực: khi trọng phạt cặp không-so-được về 0, độ đo là
   **near-metric** (không thoả bất đẳng thức tam giác) — nên em gọi "thước thứ-tự-bộ-phận TA DÙNG",
   không nói "thước duy nhất đúng".
4. **Tìm ra nhờ đâu:** search *"comparing partial rankings ties Kendall tau"* khi cần thước đo thứ tự
   không phạt cặp tự do.

### C.9. Lapata — tiền lệ dùng τ chấm thứ tự *(D8 bổ trợ — tiền lệ)*
1. **Nơi công bố:** Mirella Lapata — *Automatic Evaluation of Information Ordering: Kendall's Tau*,
   **Computational Linguistics 32(4), 2006**.
2. **Nói gì, ở đâu:** đề xuất dùng **Kendall τ** làm thước đo tự động cho bài toán **sắp thứ tự thông
   tin** (information ordering), và cho thấy nó tương quan với phán đoán người.
3. **Vì sao hậu thuẫn:** là tiền lệ cho việc lấy tương quan hạng làm **thước đo chính** của bài sắp
   thứ tự — em nối tiếp, chỉ đổi sang biến thể thứ-tự-bộ-phận suy từ quỹ đạo vàng.
4. **Tìm ra nhờ đâu:** cùng cụm khi tra *"Kendall tau information ordering evaluation"* với Fagin.

### C.10. AndroidControl (Li et al.) — quỹ đạo vàng + Step-Accuracy *(D9 — trực tiếp)*
1. **Nơi công bố:** *On the Effects of Data Scale on UI Control Agents*, Li et al. (Google DeepMind)
   — **NeurIPS 2024 Datasets & Benchmarks** (arXiv 2406.03679; giấy phép CC0).
2. **Nói gì, ở đâu:** bộ dữ liệu điều khiển UI Android người-thật, có **thao tác vàng từng bước**;
   dùng thước **Step-Accuracy (teacher-forced)** — đưa màn/ trạng thái vàng ở mỗi bước rồi chấm thao
   tác. *(Lưu ý khai thẳng: tập kiểm tra chính thức ~1.540 tập duy nhất, KHÔNG in "2.855".)*
3. **Vì sao hậu thuẫn:** cho em **quỹ đạo vàng** mà MobileViews không có, và **trục Step-SR chuẩn
   ngành** cho nhánh nhiều màn. Ranh giới: em không claim ngang leaderboard, chỉ dùng làm trục
   tham chiếu.
4. **Tìm ra nhờ đâu:** tìm trên Papers-with-Code / HuggingFace *"Android UI control dataset gold
   action"*.

### C.11. AITW (Android in the Wild) — ngưỡng dung sai 14% *(D9/D10 — trực tiếp)*
1. **Nơi công bố:** *Android in the Wild: A Large-Scale Dataset for Android Device Control*, Rawles
   et al. — **NeurIPS 2023 (Datasets & Benchmarks)**.
2. **Nói gì, ở đâu:** trong quy tắc **action matching**, một thao tác bấm tính đúng khi nằm trong
   **14% khoảng cách màn hình** so với thao tác vàng, **hoặc** rơi cùng khung nút; scroll đúng khi
   cùng trục cuộn.
3. **Vì sao hậu thuẫn:** em lấy đúng **ngưỡng 14%** này cho tiêu chí "bấm trúng" trong Step-SR và
   grounding — là con số có nguồn bình duyệt, không tự chế.
4. **Tìm ra nhờ đâu:** search *"Android in the wild action matching 14% screen distance"* khi cần
   nguồn cho ngưỡng dung sai toạ độ.

### C.12. SeeClick — point-in-bbox cho grounding *(D10 — trực tiếp)*
1. **Nơi công bố:** *SeeClick: Harnessing GUI Grounding for Advanced Visual GUI Agents*, Cheng et al.
   — **ACL 2024 (Long Papers)** (2024.acl-long.505).
2. **Nói gì, ở đâu:** đề xuất bài GUI grounding và benchmark **ScreenSpot**; độ đúng bấm (ClickAcc)
   tính bằng **điểm dự đoán rơi trong khung nút chuẩn** (point-in-bbox).
3. **Vì sao hậu thuẫn:** em chấm "bấm trúng nút" đúng theo point-in-bbox của SeeClick. Ranh giới
   quan trọng: toạ độ `(x,y)` phải do **bộ trỏ độc lập** dự đoán từ tên+ảnh, KHÔNG lấy tâm khung đã
   khớp (nếu lấy tâm → 100% giả tạo) — nên trên một màn em rút grounding thành đối chứng.
4. **Tìm ra nhờ đâu:** search *"GUI grounding benchmark ScreenSpot click accuracy"* trên
   Papers-with-Code.

### C.13. OS-Atlas / ScreenSpot-v2 — bộ đối chứng chuẩn *(D10 bổ trợ)*
1. **Nơi công bố:** ScreenSpot-v2 đi kèm *OS-Atlas: A Foundation Action Model for Generalist GUI
   Agents* — **ICLR 2025** (giấy phép Apache-2.0); bản gốc ScreenSpot thuộc SeeClick (ACL 2024).
2. **Nói gì, ở đâu:** ScreenSpot-v2 là bản **làm sạch nhãn** của ScreenSpot (sửa ~11% lỗi nhãn),
   1.272 chỉ dẫn (502 mobile / 334 desktop / 436 web), bbox chuẩn `[x1,y1,x2,y2]`.
3. **Vì sao hậu thuẫn:** là bộ **đối chứng grounding đã bình duyệt**, bù độ tin cậy cho MobileViews
   (bản tiền ấn phẩm). Ranh giới: chỉ phần nền Android mới bảo chứng trực tiếp cho MobileViews.
   *(Cần bạn tự xác nhận lại danh sách tác giả OS-Atlas trên OpenReview trước khi in — điều kiện
   chốt số 4 ở report/44.)*
4. **Tìm ra nhờ đâu:** cùng cụm SeeClick; theo dấu bản v2 làm sạch nhãn qua trang OS-Atlas ICLR 2025.

### C.14. Sai et al. — validate thước đo bằng nhiễu loạn *(D11 — trực tiếp)*
1. **Nơi công bố:** *Perturbation CheckLists for Evaluating NLG Evaluation Metrics*, Sai et al. —
   **EMNLP 2021** (2021.emnlp-main.575).
2. **Nói gì, ở đâu:** bơm các **nhiễu loạn có mục tiêu** (phủ định, trái nghĩa, ở mức câu/từ) rồi
   xem thước đo có phát hiện không; kết luận nhiều metric phổ biến (kể cả **BERTScore, BLEURT**)
   **không nhạy** ngay cả với nhiễu đơn giản, đặc biệt kém với phủ định.
3. **Vì sao hậu thuẫn:** em mượn đúng quy trình **perturbation** để đo độ nhạy thước đo mà không cần
   người chấm. Ranh giới: đây là điều kiện **cần về độ nhạy**, chưa phải convergent validity với
   người.
4. **Tìm ra nhờ đâu:** search *"perturbation checklist evaluate NLG metrics"* khi tìm cách validate
   thước đo không dựa chấm-người.

### C.15. Panickssery et al. — chống tự-chấm bằng judge khác họ *(D12 — trực tiếp)*
1. **Nơi công bố:** *LLM Evaluators Recognize and Favor Their Own Generations*, Panickssery, Bowman
   & Feng — **NeurIPS 2024**.
2. **Nói gì, ở đâu:** LLM (GPT-4, Llama 2) **nhận ra bài của chính mình** ở mức đáng kể, và mức
   **tự thiên vị (self-preference) tỉ lệ tuyến tính với khả năng tự-nhận-diện**; họ tinh chỉnh trên
   các thuộc tính gây nhiễu để lập luận nhân quả.
3. **Vì sao hậu thuẫn:** vì generator của em là họ GPT, nên judge phải **khác họ** — tách khác họ là
   biện pháp mạnh nhất loại thiên vị tự-chấm. Trụ bổ trợ cho khung LLM-as-judge: Zheng et al.
   (MT-Bench, NeurIPS 2023).
4. **Tìm ra nhờ đâu:** search *"LLM self-preference bias evaluator own generation"*.

### C.16. MacKinnon, Nielsen & Webb — gộp cụm theo app *(D13 — trực tiếp)*
1. **Nơi công bố:** *Cluster-Robust Inference: A Guide to Empirical Practice*, MacKinnon, Nielsen &
   Webb — **Journal of Econometrics 232(2):272–299, 2023**.
2. **Nói gì, ở đâu:** cẩm nang thực hành suy luận cụm-vững; nhấn mạnh khi **số cụm ít** phải dùng
   **wild-cluster bootstrap** để khoảng tin cậy khỏi hẹp giả / dưới-phủ.
3. **Vì sao hậu thuẫn:** các màn cùng một ứng dụng **không độc lập**, nên em gộp cụm theo app và
   dùng wild-cluster bootstrap-t (Cameron–Gelbach–Miller 2008) vì số cụm còn khiêm tốn.
4. **Tìm ra nhờ đâu:** search *"cluster-robust inference few clusters wild bootstrap"* khi thiết kế
   phần thống kê.

### C.17. Chen et al. — cây giao diện không phải chuẩn vàng *(D14 — trực tiếp)*
1. **Nơi công bố:** *Unblind Your Apps: Predicting Natural-Language Labels for Mobile GUI Components
   by Deep Learning*, Chen et al. — **ICSE 2020 (Distinguished Paper)**.
2. **Nói gì, ở đâu:** phân tích quy mô lớn cho thấy phần lớn phần tử ảnh bấm được thiếu nhãn trợ năng
   (content-description). Số chính xác cần nói đúng cấp độ để không bị bắt bí: ở **cấp ỨNG DỤNG**, khoảng
   **62% ứng dụng** có nút-ảnh không nhãn và **~74% ứng dụng** có ảnh-bấm-được không nhãn; ở **cấp PHẦN TỬ**,
   **76,68% ảnh bấm được** (clickable images) và 57,01% nút-ảnh (image buttons) không có nhãn. **Tránh nói
   "77% ứng dụng thiếu nhãn"** — con số ~77% là ở cấp phần-tử (ảnh bấm được), không phải cấp ứng dụng.
3. **Vì sao hậu thuẫn:** biện minh vì sao em **không coi View Hierarchy là ground-truth** mà hậu-kiểm
   rồi né bịa bằng nhánh dự phòng; cũng là trụ **khái niệm** cho luật "chỗ bịa chỉ mô tả" (đoán nút
   dựa vào metadata khuyết nhãn = sai ngầm).
4. **Tìm ra nhờ đâu:** search *"mobile GUI missing accessibility label content description"*.
   *(Đã web-verify 2026-07-08: số gốc trong paper — 61,98% ứng dụng có nút-ảnh không nhãn; 76,68% ảnh
   bấm được thiếu nhãn ở cấp phần tử.)*

### C.18. Clark et al. — không lấy chấm-người làm cổng *(D15 — trụ khái niệm)*
1. **Nơi công bố:** *All That's 'Human' Is Not Gold: Evaluating Human Evaluation of Generated Text*,
   Clark et al. — **ACL-IJCNLP 2021** (2021.acl-long.565).
2. **Nói gì, ở đâu:** người **không được huấn luyện** phân biệt văn bản GPT-3 với văn bản người chỉ
   ở **mức ngẫu nhiên**; ba cách huấn luyện nhanh cũng chỉ nâng độ chính xác tới ~**55%**, không cải
   thiện đáng kể trên ba miền (truyện, tin, công thức nấu ăn).
3. **Vì sao hậu thuẫn:** vì chấm-người với văn bản máy-sinh **vốn thiếu ổn định**, em **không** lấy
   human-correlation làm cổng đậu/rớt mà validate bằng perturbation; chấm-người để làm đối chiếu
   tương lai. Đây là trụ **khái niệm** cho quyết định bỏ cổng người, không phải đo trực tiếp trên
   dữ liệu của em.
4. **Tìm ra nhờ đâu:** search *"human evaluation generated text unreliable annotators"*.

### C.19. TOMATO — động lực tách khối sắp thứ tự *(D16 — trực tiếp, miền video; có bẫy tên)*
1. **Nơi công bố:** **TOMATO: Assessing Visual Temporal Reasoning Capabilities in Multimodal
   Foundation Models** — **ICLR 2025 (Poster; OpenReview fCi4o83Mfs)**. *(Tên đầy đủ phải đúng —
   nếu thầy tra OpenReview mà mình đọc sai tên là lộ gán ẩu.)*
2. **Nói gì, ở đâu:** benchmark suy luận thời gian trên **video** (khoảng 1.417 video), phát hiện
   mô hình ảnh-ngôn ngữ xử lý chuỗi khung hình như **"túi khung hình" (bag-of-frames)** — sắp trật
   tự thời gian yếu; khoảng cách người–máy **57,3%** ở model tốt nhất. *(Đã web-verify 2026-07-08 trên
   bản ICLR/arXiv 2410.23266: 1.484 câu hỏi trên **1.417 video**, khoảng cách người–máy **57,3%**, đánh
   giá 31 mô hình — nói chắc được.)*
3. **Vì sao hậu thuẫn — CHÚ Ý RANH GIỚI:** đây là bằng chứng **ở miền video**, em dùng làm **ĐỘNG
   LỰC** để tách riêng khối sắp thứ tự (so-cặp thay vì bảo model sắp cả dãy). **Không** nói TOMATO
   chứng minh khối của em đúng trên ảnh giao diện — năng lực thật trên GUI em **tự đo lại qua cổng
   K-pair** trước khi tổng hợp Copeland. Phần "chống rò rỉ chỉ-số-bước" TOMATO **không** hậu thuẫn,
   đừng gán.
4. **Tìm ra nhờ đâu:** search *"VLM temporal reasoning benchmark bag of frames"* khi tìm bằng chứng
   VLM yếu suy luận trật tự thời gian.

---

## Bảng nguồn trích dẫn (đã kiểm)

| Thành phần | Nguồn | Nơi công bố | Loại |
|---|---|---|---|
| Khung đánh giá không-gold (Intrinsic + Extrinsic) | Chim, Ive & Liakata | Computational Linguistics 51(1):191–233, 2025 | trực tiếp |
| Đo trung thực reference-free (LVLM) | FaithScore, Jing et al. | Findings of EMNLP 2024 | trực tiếp |
| Lối "tách nhỏ – kiểm với nguồn ngoài" | FActScore, Min et al. | EMNLP 2023 | tiền lệ |
| So khớp tên nút theo ngữ nghĩa | ALOHa, Petryk et al. | NAACL 2024 (short) | tiền lệ |
| So từng cặp (pairwise ranking) | Qin et al. | Findings of NAACL 2024 | tiền lệ |
| Bài toán tổng hợp hạng (rank aggregation) | Dwork, Kumar, Naor & Sivakumar | WWW 2001 (ACM, pp. 613–622) | tiền lệ |
| Phương pháp Copeland (trụ đúng-danh) | Saari & Merlin | Economic Theory 8:51–76, 1996 | tiền lệ |
| Phá vòng min-feedback-arc-set | Ailon, Charikar & Newman | J. ACM 55(5), 2008 | tiền lệ |
| Độ tương quan thứ-tự-bộ-phận | Fagin et al., “Comparing partial rankings” | SIAM J. Discrete Math 20(3):628–648, 2006 | trực tiếp |
| Tiền lệ τ làm thước đo sắp thứ tự | Lapata | Computational Linguistics 32(4), 2006 | tiền lệ |
| Quỹ đạo vàng nhiều màn + Step-Accuracy | AndroidControl (Li et al.) | NeurIPS 2024 (D&B) | trực tiếp |
| Ngưỡng dung sai 14% (action matching) | AITW (Rawles et al.) | NeurIPS 2023 (D&B) | trực tiếp |
| Point-in-bbox, ScreenSpot gốc | SeeClick, Cheng et al. | ACL 2024 (long) | trực tiếp |
| ScreenSpot-v2 (làm sạch nhãn) | OS-Atlas | ICLR 2025 | trực tiếp |
| Kiểm định thước đo bằng nhiễu loạn | Sai et al. | EMNLP 2021 | trực tiếp |
| Chống tự-chấm (judge khác họ) | Panickssery, Bowman & Feng | NeurIPS 2024 | trực tiếp |
| Gộp cụm theo app (wild-cluster bootstrap) | MacKinnon, Nielsen & Webb | Journal of Econometrics 232(2):272–299, 2023 | trực tiếp |
| Cây giao diện không phải chuẩn vàng (≈77% ảnh-bấm-được thiếu nhãn ở cấp phần tử) | Chen et al. | ICSE 2020 (Distinguished Paper) | trực tiếp |
| Bỏ human-correlation làm cổng đậu/rớt | Clark et al. | ACL-IJCNLP 2021 | trụ khái niệm |
| Động lực tách khối sắp thứ tự (VLM yếu suy luận thời gian) | TOMATO | ICLR 2025 (Poster) | trực tiếp (miền video) |

> Ghi chú loại: *trực tiếp* = paper làm/đo đúng việc mình mượn; *tiền lệ* = paper làm ở miền khác,
> mình mượn nguyên lý; *trụ khái niệm* = paper hậu thuẫn về mặt lập luận, không đo trực tiếp trên
> dữ liệu của mình. Ba chỗ khai thẳng ranh giới để không bị bắt hớ: **D4/FActScore** (chỉ chấm,
> không sinh), **D6/Dwork** (đặt nền bài toán, không dùng Copeland — Copeland trụ ở Saari & Merlin),
> **D16/TOMATO** (bằng chứng miền video, dùng làm động lực, năng lực GUI tự đo qua cổng K-pair).
