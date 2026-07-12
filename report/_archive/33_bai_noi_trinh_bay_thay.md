# 🗣️ BÀI NÓI TRÌNH BÀY VỚI THẦY (đọc/nói miệng) — DG1 + DG2

> **Cách dùng:** đây là **văn nói**, đọc lên gần như thành bài. Các nhãn `[...]` chỉ để bạn định vị, **không đọc**. Chỗ in đậm là chỗ nên nhấn giọng. Cuối có **phần dự phòng câu hỏi**.
> **Nhịp:** ~12–15 phút. Nói chậm ở 3 chỗ quan trọng: *chống vòng-lập-luận*, *Kendall τ-b*, *Step-SR*.

---

## [MỞ ĐẦU]

Thưa thầy, hôm nay em xin trình bày toàn bộ hướng làm của luận văn — cả phần **sinh hướng dẫn** lẫn phần **đánh giá**. Em sẽ đi từ bài toán, rồi tới hai đóng góp, sau đó đi sâu vào **cách em đánh giá**, vì đó là phần em đầu tư nhiều nhất và cũng là chỗ dễ bị vặn nhất, nên em muốn trình bày thật rõ và **tự nêu luôn những giới hạn** của mình.

---

## [BÀI TOÁN]

Bài toán của em là: khi một người dùng gặp một phần mềm lạ, họ thường chỉ biết hỏi một câu rất đời thường, kiểu *"muốn làm việc này thì bấm vào đâu?"*. Em muốn một mô hình **đa phương thức** — tức là loại AI **vừa nhìn được ảnh vừa đọc được chữ** — nhìn vào ảnh chụp màn hình cộng với câu hỏi đó, rồi **tự viết ra hướng dẫn từng bước** cho người dùng làm theo.

Đầu vào có hai dạng. Dạng thứ nhất là **một ảnh**, khi việc cần làm nằm gọn trên một màn hình. Dạng thứ hai là **nhiều ảnh đã bị xáo trộn** của cùng một luồng thao tác — lúc này model phải **tự suy ra thứ tự đúng** của các màn rồi mới hướng dẫn theo thứ tự đó. Em tách hai dạng này bằng một bộ định tuyến đơn giản: một ảnh thì đi đường đơn-bước, nhiều ảnh thì bật chế độ sắp-thứ-tự.

Có **ba cái khó** mà em phải đối mặt. **Thứ nhất**, mô hình hay bị **"ảo giác"** — tức là nó nhắc tới những nút hoặc menu **không hề có trên màn hình** — khiến người làm theo bị lạc. **Thứ hai**, với mỗi phần mềm, **gần như không có sẵn một bản hướng dẫn chuẩn do con người soạn** để em đối chiếu mà chấm điểm — đây là cái khó trung tâm, vì các bài toán như dịch máy thì có bản dịch chuẩn, còn bài của em thì không. **Thứ ba**, ở chế độ nhiều ảnh, câu hỏi đặt ra là: **làm sao biết model xếp đúng thứ tự các màn, và nó dựa vào tín hiệu gì để biết?** — đây đúng là câu hỏi thầy hay hỏi em, nên em đã thiết kế hẳn một nhánh để **đo** điều đó.

---

## [HAI ĐÓNG GÓP]

Từ ba cái khó đó, luận văn của em có **hai đóng góp ngang nhau**.

Đóng góp thứ nhất là một **phương pháp tạo sinh** hướng dẫn bám sát màn hình — em gọi là "lớp làm-cho-trung-thực" — nó **gắn được lên bất kỳ mô hình mạnh nào** để giảm việc bịa nút.

Đóng góp thứ hai, và cũng là phần em coi trọng ngang bằng, là một **khung đánh giá hai nhánh** đáng tin **khi không có đáp án mẫu chuẩn**. Khung này em **kế thừa tinh thần** từ một bài trên tạp chí *Computational Linguistics* năm 2025 của Chim, Ive và Liakata — họ đánh giá văn bản do máy sinh ra khi không có đáp án chuẩn; em mượn khung đó và áp vào bài hướng dẫn giao diện.

Em xin nói thẳng ngay từ đầu: em **không** tuyên bố hệ của em mạnh nhất thế giới hay hơn GPT-5. Em chứng minh hai điều cụ thể và đo được: **cách đo của em đáng tin**, và **lớp sinh của em làm hướng dẫn trung thực hơn** so với để chính mô hình đó viết tự do — kèm theo **cái giá phải trả** một cách minh bạch.

---

## [KHUNG ĐÁNH GIÁ HAI NHÁNH]

Phần quan trọng nhất là **khung đánh giá**. Em chia làm hai nhánh, và **trục phân chia là: có đáp án vàng để chấm hay không**.

**Nhánh thứ nhất, em gọi là DG1**: đánh giá hướng dẫn trên **một màn hình**, trong điều kiện **không có** hướng dẫn mẫu của con người.

**Nhánh thứ hai, DG2**: đánh giá **năng lực suy luận thứ tự nhiều màn**, và ở nhánh này em **có** đáp án vàng — em dùng bộ dữ liệu **AndroidControl**, một dataset đã được bình duyệt ở hội nghị NeurIPS 2024, trong đó mỗi bước thao tác **có sẵn đáp án đúng**.

Điểm mấu chốt là hai nhánh **bù cho nhau**: DG1 đo được *"hướng dẫn có bịa không"* khi không có gold, còn DG2 đo được *"hướng dẫn có đúng-ý, có làm-tới-đích không"* khi **có** gold. Cái mà DG1 **không** trả lời được — là "đúng-ý" — thì **DG2 trả lời được**. Đó là lý do em phải trình cả hai, vì chỉ một nhánh thì chưa đủ sức nặng.

---

## [DG1 — CÁCH LÀM]

Em đi vào DG1 trước. Ý tưởng then chốt giúp bài này khả thi là: mỗi màn hình Android đều có sẵn một thứ gọi là **cây phân cấp giao diện**, tiếng Anh là *View Hierarchy* — đây là một bản kê khai do hệ điều hành cung cấp, liệt kê **mọi nút thật trên màn, kèm tên và toạ độ**. Em dùng nó làm **"đáp án bạc"** để chấm: với mỗi bước hướng dẫn, em hỏi *"cái nút mà bước này nhắc tới có thật sự nằm trong danh sách nút của màn không?"*.

Em gọi nó là "bạc" chứ không phải "vàng", vì nó là nhãn **tự động, đủ tin nhưng không hoàn hảo** — đôi khi thiếu vài nút vẽ bằng ảnh — và em **khai thẳng** điều này chứ không giấu.

Có một **luật vàng** em luôn giữ: cây phân cấp này **chỉ được dùng lúc CHẤM**, **tuyệt đối không đưa cho mô hình lúc đang SINH**. Vì nếu em mớm danh sách nút cho model lúc nó viết, thì chuyện "không bịa" thành hiển nhiên — kết quả sẽ là giả. Đây chính là chống **rò rỉ thông tin**.

Pipeline DG1 gồm bốn bước: mô hình sinh ra bản hướng dẫn gốc; em đối chiếu từng bước với cây phân cấp; bước nào trỏ tới nút **không tồn tại** thì **lớp hậu kiểm** sẽ viết lại thành **mô tả bằng lời** thay vì bắt người dùng đi tìm một cái nút không có thật; cuối cùng em chấm điểm.

---

## [DG1 — CÁCH ĐO & CHỐNG VÒNG LẬP LUẬN]

*(Nói chậm chỗ này.)* Bây giờ tới phần em muốn trình bày kỹ nhất, vì nó là chỗ một hội đồng khó tính sẽ đánh ngay: **làm sao tránh vòng lập luận**.

Vấn đề là thế này. Nếu em dùng **cùng một công cụ** để vừa **quyết định** "bước này bịa, đem cách-ly", vừa **chấm điểm** "còn bịa không", thì điểm trung thực sau cùng **đương nhiên là 100%** — đó là một **đẳng thức**, không phải một kết quả thực nghiệm.

Để chống điều đó, em **tách đôi công cụ**. Việc **quyết định** cách-ly thì dùng một mô hình embedding tên là `nomic`. Còn việc **chấm điểm** thì em dùng một mô hình **khác**, tên `bge-m3`, **cộng thêm một bộ chấm bằng LLM thuộc họ khác** với mô hình sinh. Và quan trọng nhất: **con số em báo cáo không phải là 100% sau-lớp** — con số đó em nói thẳng là **trần do thiết kế** — mà là **tỉ lệ bịa của bản gốc**, tức là *độ lớn của vấn đề* mà mô hình mắc phải.

Về bộ chấm bằng LLM, em xin nói rõ để thầy yên tâm: em **không** để AI chấm "hay hay dở" — đó là vùng AI hay thiên lệch. Em chỉ giao cho nó một **phán đoán rất hẹp, nhị phân, và có sẵn tham chiếu**: *"tên nút này có khớp đúng một nút trong danh sách thật không?"*. Đây là vùng đáng tin nhất của LLM-judge; có bài ở NeurIPS 2023 chứng minh khi đưa sẵn tham chiếu vào thì tỉ lệ sai của bộ chấm giảm từ 70% xuống còn 15%. Bộ chấm này thuộc **họ khác** với mô hình sinh, và em **đo độ chính xác của nó so với nhãn người**.

Cuối cùng, để chứng minh **chính thước đo** của em đáng tin mà **không cần đi nhờ người chấm thủ công**, em dùng một kỹ thuật gọi là **perturbation** — tức là em **tự bơm những lỗi đã biết** vào một bản hướng dẫn đúng, ví dụ đổi một nút thật thành một nút ma, rồi xem **thước đo có bắt được không**. Vì lỗi do em tạo nên đáp án đúng đã biết trước, em đo được độ nhạy của thước đo một cách hoàn toàn khách quan. Cách này có tiền lệ ở hội nghị EMNLP 2021.

---

## [DG1 — PHẠM VI: lá chắn]

Và đây là lá chắn mạnh nhất của em — em **tự nêu giới hạn trước khi thầy hỏi**. Với DG1, em chỉ khẳng định **đúng một điều**: lớp hậu kiểm **giảm việc nhắc tới nút không tồn tại**, và **cái giá là một số bước phải mô tả khái quát hơn**. Em **không** khẳng định nó làm hướng dẫn "đúng-ý" hay "hữu ích" — vì điều đó cần đáp án vàng, và em để dành cho DG2. Em cũng tự nêu hai hạn chế kỹ thuật: cây phân cấp là ảnh chụp **một trạng thái** nên nút sau khi cuộn có thể bị nhầm là không tồn tại — em xử lý bằng cách lọc các bước đó; và độ phủ của cây phân cấp là một ẩn số nên em **tự đo nó trước** và đóng khung mọi con số là "có điều kiện".

---

## [DG2 — BÀI TOÁN THỨ TỰ]

*(Chuyển giọng — phần này là sức nặng khoa học.)* Bây giờ em sang **DG2**, phần em nghĩ là có hàm lượng khoa học nặng nhất.

Bài toán là: em đưa cho mô hình **N tấm ảnh đã bị xáo trộn** của một luồng thao tác, kèm mục tiêu, rồi yêu cầu nó **tự suy ra thứ tự đúng** của các màn, sau đó sinh hướng dẫn theo thứ tự đó. Đây chính là bài toán em **đặt ra để ĐO** năng lực suy luận thứ tự — để trả lời thẳng câu hỏi của thầy là *"làm sao model biết màn nào trước màn nào sau"*.

Em xin nói trước một lo ngại thầy có thể có: *"lỡ model đọc lén thông tin thứ tự trong ảnh, ví dụ đồng hồ hay pin, thì sao?"*. Em chống điều đó rất kỹ: em **xóa metadata, mã hóa lại ảnh, che thanh trạng thái, đồng hồ, pin, badge**, và loại bỏ các luồng có màn gần-trùng nhau. Em còn có một bài kiểm tra: một bộ dò chỉ-nhìn-pixel **không** suy ra được thứ tự tốt hơn đoán ngẫu nhiên — nghĩa là thông tin thứ tự **không** rò qua đường tiểu tiết.

---

## [DG2 — KENDALL τ-b & CHỐNG TỰ CHẤM]

*(Nói chậm.)* Thước đo trụ cột của DG2 là hệ số **Kendall tau-b**. Nói đơn giản, nó là một con số từ âm-một tới dương-một, đo **mức độ thứ tự mà model xếp ra giống thứ tự đúng**: dương-một là trùng khít, còn không là như đoán bừa.

Nhưng em không chấm thứ tự một cách máy móc. Em chấm theo kiểu **thứ-tự-bộ-phận**: em **chỉ trừ điểm khi model sai một "cặp bắt buộc"**. Cặp bắt buộc là hai màn mà một cái **chắc chắn phải đứng trước** cái kia — ví dụ phải đăng nhập rồi mới xem được kết quả. Còn những cặp **tự do** — ví dụ điền email hay điền số điện thoại trước đều được — thì model đảo thứ tự **vẫn được tính là đúng**. Điều này giúp em **không phạt oan**.

Và đây là chỗ then chốt để **chống tự-ra-đề-tự-chấm**: cái nhãn "cặp nào là bắt buộc" em **không** lấy từ chính bộ phận mà model dùng để đoán; em **suy nó ra từ đáp án vàng bằng một quy tắc nhân-quả tất định** — cụ thể, nếu màn B chỉ xuất hiện **sau** khi thực hiện đúng thao tác vàng ở màn A, thì cặp A-trước-B là bắt buộc. Như vậy thước đo độc lập với cái mà em đang chấm. Em còn cho **người kiểm tra một mẫu 50 đến 80 cặp** để xác nhận quy tắc này khớp với đánh giá của con người.

---

## [DG2 — ORDERING GAP & STEP-SR]

Để biết "năng lực sắp thứ tự" đáng giá bao nhiêu, em so hai tình huống. Một là **đưa sẵn thứ tự đúng** cho model rồi để nó chỉ việc sinh — đây là cận trên lý tưởng. Hai là **đưa ảnh xáo** để nó **tự sắp** rồi mới sinh. **Khoảng cách giữa hai cái** chính là *"cái giá của việc không biết thứ tự"*. Và để giải thích model dựa vào đâu, em định nghĩa **năm loại tín hiệu giao diện** — như việc đăng nhập phải đứng trước, hay nút Next/Back, hay một ô từ trống chuyển sang đã điền — rồi em **phân tầng kết quả theo từng tín hiệu** để biết tín hiệu nào thực sự giúp model.

Và cuối cùng, phần em coi là **xương sống khoa học**: vì DG2 có đáp án vàng, em đo được **Step-SR** — tức là **làm theo hướng dẫn của model thì có tới đích không**. Đây là bằng chứng khó cãi nhất rằng hướng dẫn **dùng được thật**, chứ không chỉ "không bịa". Đây chính là cái **"đúng-ý"** mà DG1 không đo được, và là lý do DG2 cho luận văn sức nặng. Em chấm theo chuẩn ngành trên AndroidControl, với ngưỡng dung sai 14% trích từ một bài ở NeurIPS 2023.

---

## [PIPELINE]

Về kiến trúc hệ thống, em đặt một **tầng sắp-thứ-tự đứng trước**. Tầng này hỏi mô hình theo **từng cặp** — "màn này hay màn kia trước?" — rồi tổng hợp lại bằng một cách tính điểm gọi là Copeland, sau đó một bộ kiểm tra bằng code thuần sẽ gỡ các mâu thuẫn vòng. Em chốt trần ở N nhỏ hơn hoặc bằng 6 để chi phí vừa phải. Sau khi đã sắp xong, chuỗi màn đi vào pipeline sinh hướng dẫn, với **oracle đặt bên cạnh** chứ không đặt trước — nghĩa là nếu bộ dò sót nút thì nó **chỉ làm giảm độ tin của phép đo, chứ không cắt mất bước nào** trong hướng dẫn. Em **không fine-tune** phần lõi, dùng mô hình có sẵn.

---

## [ĐỘ CHẶT]

Về độ chặt phương pháp, em xin nhấn mấy điểm. Em chống vòng-lập-luận ở **cả hai tầng** như đã nói. Em **đăng ký trước** giả thuyết, ngưỡng, và quy tắc quyết định — trước khi nhìn kết quả — để không ai nói được là em "chạy tới khi đẹp"; và em theo nguyên tắc **"kết quả null vẫn là đóng góp"**. Về thống kê, em **gộp theo ứng dụng** khi tính khoảng tin cậy, vì các màn cùng một app thì không độc lập với nhau — nếu không gộp thì khoảng tin cậy sẽ giả-chặt. Và em có **bốn cổng kiểm tra cứng** trước khi chạy chính, trong đó có cổng tự đo độ phủ của bộ dò.

---

## [ĐÓNG GÓP & KẾT]

Tóm lại, luận văn của em có hai đóng góp ngang nhau: một **phương pháp tạo sinh** hướng dẫn bám-sát-màn, model thay được; và một **khung đánh giá hai nhánh** — DG1 đo trung thực khi không có đáp án vàng, DG2 đo thứ tự và đúng-ý khi có đáp án vàng.

Em **khai thật** rằng độ mới của em là **gia tăng** chứ không phải đột phá: em thừa nhận đã có những công trình trước về sắp thứ tự ảnh; cái mới của em nằm ở việc **áp vào lĩnh vực giao diện**, **điều kiện hóa theo mục tiêu**, **gắn việc sắp thứ tự với sinh hướng dẫn**, và **chống vòng-lập-luận hai tầng**. Và quan trọng nhất, mọi giả thuyết em đều **đăng ký trước**, mọi giới hạn em đều **tự nêu** — nên em tin mỗi câu em nói đều đứng vững.

Em xin hết phần trình bày, và rất mong nhận góp ý của thầy ạ.

---
---

## 📎 PHẦN DỰ PHÒNG — NẾU THẦY HỎI (không đọc, chỉ để thủ)

**Nếu thầy hỏi số liệu cụ thể:** *"Dạ số cuối em đang chạy. Sơ bộ thì đúng hướng — mô hình mạnh hơn bịa ít hơn, và thước đo phân biệt được mô hình tốt với mô hình dở. Em đang chạy chính trên 17 ứng dụng để có bảng số và khoảng tin cậy đầy đủ ạ."* **(Đừng bịa số.)**

**"DG1 chỉ đo tự-nhất-quán, có tautology không?"** → *"Dạ đúng, em thừa nhận. Faithfulness 100% là trần do thiết kế, em báo tỉ-lệ-bịa của bản gốc chứ không trưng 100%. Phần 'đúng-ý' em đo ở DG2 bằng Step-SR có đáp án vàng — hai nhánh bù nhau ạ."*

**"AI chấm AI có tin được không?"** → *"Em không cho AI chấm hay-dở. Em chỉ giao một phán đoán nhị phân, có sẵn tham chiếu, và em đo độ chính xác của nó với nhãn người ạ."*

**"Hai embedder có thật sự độc lập?"** → *"Dạ chúng tương quan cao vì cùng họ, nên em không dựa hẳn vào đó — em thêm một bộ chấm khác họ, và ở DG2 thì dùng đáp án vàng nên không lệ thuộc embedder ạ."*

**"2026 có GPT-5 rồi còn ý nghĩa không?"** → *"Frontier vẫn bịa nút, vẫn sai thứ tự. Đóng góp của em là cách đánh giá và một lớp model-agnostic — model mạnh lên chỉ làm số đẹp hơn, không làm đề tài lỗi thời ạ."*

**"Đủ chuẩn thạc sĩ chưa?"** → *"Em có hai đóng góp, hai nhánh đánh giá, dùng dataset bình duyệt có đáp án vàng cho phần đúng-ý, cộng độ chặt phương pháp — chống vòng-lập-luận hai tầng, đăng ký trước, gộp theo app, audit người. Em khai hẹp từng claim để không overclaim ạ."*
