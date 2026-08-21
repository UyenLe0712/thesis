# Script trình bày với thầy — bản 12/8/2026

> Khớp với `LUAN_VAN_SLIDE.pptx` (27 slide). Thay `report/104`.
> **Buổi trình bày ĐẦU TIÊN** — thầy chưa biết gì về thiết kế này, nên script tự chứa,
> không nhắc "buổi trước", và mọi thuật ngữ đều giải nghĩa ngay lần đầu dùng.
>
> Chữ thường là lời nói. *Chữ nghiêng trong ngoặc* là ghi chú cho mình, không đọc.
>
> **Thời lượng: đọc hết là ~25 phút** (đo bằng số từ, nhịp 150 từ/phút). Nhãn giờ ở mỗi mục
> là số đo thật, không phải ước.
>
> **Nếu chỉ có 15 phút** — bỏ nguyên bốn mục này, thứ tự ưu tiên bỏ:
> mục 12 (mức 2, 1½ ph) · mục 11 (ví dụ một bước, 1 ph) · mục 15 (trình tự, ¾ ph) ·
> mục 14 rút còn hai câu (bớt 1 ph) · mục 2 rút còn GuideMe (bớt ¾ ph) ·
> mục 6 bỏ đoạn "không phải LLM-as-a-judge" (bớt 1 ph). Còn ~19 phút; bỏ thêm mục 9 và 13
> thì về ~17. Dưới nữa thì phải hy sinh nội dung thật, đừng cắt tiếp.
>
> **Giữ bằng mọi giá:** mục 4 (lỗi mơ hồ) · mục 6-7 (cách chấm + độ tin) · mục 8 (điểm cao
> nhất 70) · mục 10 (đóng góp) · mục 16 (đã làm tới đâu) · mục 17 (giới hạn) · mục 18 (ba kịch bản).

---

## Mở đầu · slide 1–2 · 45 giây

Dạ em chào thầy. Hôm nay em xin trình bày toàn bộ đề tài của em, chừng mười lăm phút ạ.

Em xin nói ngay hai điều. Thứ nhất, thầy có yêu cầu luận văn phải có một mô hình do em tự huấn luyện chứ không chỉ ghép công cụ có sẵn — em đã làm đúng như vậy, và **mô hình đang huấn luyện ngay lúc này**, sáng mai là có điểm đầu tiên. Thứ hai, cuối buổi em có một việc mong thầy quyết giúp: cách đọc kết quả cho cả ba kịch bản, chốt trước khi số về.

## 1. Bài toán · slide 3 · 60 giây

Đề tài của em là sinh hướng dẫn sử dụng phần mềm từ ảnh màn hình. Tình huống cụ thể: một người đang bí trong một ứng dụng, họ chụp màn hình rồi hỏi, ví dụ "làm sao chia sẻ playlist này cho bạn tôi". Mô hình nhìn ảnh đó và trả lời bằng một câu cho người đọc: "Chạm vào biểu tượng chia sẻ ở góc trên bên phải màn hình."

Chỗ khác biệt so với các nghiên cứu cùng mảng nằm ở đầu ra. Các mô hình giao diện bây giờ đều được huấn luyện để **tự bấm thay người** — đầu ra là toạ độ nút, dạng `click(732, 173)`. Đề tài của em thì đầu ra là **câu chữ cho người đọc**, và câu chữ là thứ duy nhất đem chấm.

## 2. Đã có ai làm chưa · slide 4 · 1 phút 15 giây

Em tra kỹ tới trang gốc từng bài, và xin phân định ba hướng.

Aguvis với UI-Ins là dòng mô hình giao diện: sinh toạ độ để máy bấm. Chúng có sinh câu ở bước trung gian, nhưng **chất lượng câu không hề được đánh giá**.

Bài gốc của bộ dữ liệu em dùng — AndroidControl, NeurIPS 2024 — có câu người viết, nhưng họ dùng câu đó làm **đầu vào** cho agent đoán thao tác. Em đảo lại, dùng làm **đích để sinh**. Theo những gì em tra được thì chưa ai làm vậy.

Bài sát nhất là GuideMe ở CHI năm nay: cũng sinh hướng dẫn cho người, nhưng làm bằng cách gọi GPT-5 qua mạng, **không huấn luyện mô hình nào**, và đánh giá bằng khảo sát người dùng chứ không có thước chấm định lượng.

Nên chữ "đầu tiên" em chỉ dám dùng ở đúng một chỗ: **mô hình mở đầu tiên được huấn luyện cho tác vụ này**. Còn các cơ chế bên trong đều có tiền lệ, mượn của ai em khai rõ người đó.

## 3. Dữ liệu · slide 5 · 30 giây

Bộ dữ liệu là AndroidControl: mười lăm nghìn tác vụ do người thật thao tác trên điện thoại Android. Mỗi bước có ba thứ — ảnh màn hình, toạ độ chỗ người đó chạm, và một câu mô tả do chính người đó viết.

Nhưng câu người viết **rất cụt**: trung vị chỉ sáu từ. Kiểu "click on OK", "Click on the screen.", "Select the search result". Con số này về sau quay lại ám cả luận văn, lát nữa em nói kỹ.

## 4. Mô hình thường sai kiểu gì · slide 6 · 1 phút 30 giây

Trước khi chọn cách can thiệp, em đo xem mô hình sinh câu thường sai kiểu gì. Cách em soi thế này ạ: em cho gpt-4o-mini sinh câu trên một trăm hai mươi bảy bước, rồi với mỗi tên nút nó nhắc tới, em đối chiếu với **cây trợ năng** của đúng màn đó — tức bản kê phần tử mà hệ điều hành xuất ra. Khớp nguyên văn được sáu mươi tám phẩy năm phần trăm. Bốn mươi ca còn lại em **mở ảnh ra soi từng ca bằng mắt**, để phân biệt hai chuyện: mô hình bịa ra nút không tồn tại, hay nút có thật mà cây trợ năng không ghi tên.

Kết quả: **không có ca bịa nào**. Ba mươi lăm trên bốn mươi ca là nút có thật nhưng cây trợ năng bỏ trống tên — hai mươi ca là biểu tượng như dấu cộng, dấu tích, mũi tên. Nên tỉ lệ bịa thật chỉ quanh **không tới hai phần trăm**.

*(Giới hạn phải khai nếu thầy hỏi cỡ mẫu: 80 màn của một ứng dụng, bốn mươi ca soi tay quy về khoảng mười tám phần tử khác nhau. Mẫu nhỏ. Và đây là đo trên gpt-4o-mini, chưa phải mô hình của em.)*

Lỗi số một hoá ra là **câu mơ hồ**: kiểu "chạm vào biểu tượng tìm kiếm" trong khi màn hình có tới hai biểu tượng tìm kiếm.

Em có một con số cho chuyện đó. Lấy ba trăm câu chuẩn của tập kiểm, chấm bằng đúng cách em sắp trình, rồi chia đôi theo độ dài câu. Nhóm câu ngắn lần ra đúng nút **sáu mươi hai phần trăm**, nhóm câu dài hơn **bảy mươi chín**.

Trung bình hai nhóm là bảy mươi — và lát nữa thầy sẽ thấy đúng con số bảy mươi đó quay lại ở phần điểm cao nhất. Hai chỗ là một phép đo, chỉ khác cách cắt.

*(Nếu thầy vặn "sao biết không phải do câu dài đi kèm nút dễ trỏ hơn": em kiểm rồi, nhiễu chạy ngược chiều — nhóm câu dài nhắm nút KHÓ hơn — nút nhỏ hơn gấp đôi, và chỉ 65% có tên so với 77% ở nhóm ngắn — mà vẫn trúng nhiều hơn mười bảy điểm. Lọc chỉ giữ nút có tên thì vẫn 59,0 so với 79,3. Nhưng khai luôn: đây là quan sát trên câu chuẩn, không phải thí nghiệm — phép thử nhân quả thật chính là phần so sánh cuối buổi.)*

## 5. Hai việc phải làm · slide 7 · 1 phút 30 giây

Từ đó ra hai câu hỏi, và phần còn lại của buổi đi đúng theo hai câu này.

Một là **chấm bằng cách nào**. Chỗ này em xin nói kỹ vì dễ hiểu nhầm. Bộ dữ liệu **có** câu chuẩn do người viết, như em vừa trình. Cái không dùng được là **cách chấm bằng so chữ với câu chuẩn**.

Em đã thử và đã rớt: trên năm mươi mốt ca viết tay, chỉ số phân biệt được có **không phẩy ba tư — tệ hơn đoán mò**. Lý do bản chất là embedding đo **độ gần chủ đề**, mà chủ đề lại đi ngược cái mình cần. Ví dụ "inbox" với "outbox" là **hai nút khác nhau** thì được không phẩy bảy sáu, trong khi "search" với "magnifying glass" — **cùng một nút**, một bên gọi tên chức năng một bên tả hình — chỉ được không phẩy năm lăm. Cùng nút trung bình sáu mươi hai, khác nút trung bình sáu mươi bảy. Không có ngưỡng nào tách được.

Nên em phải đổi câu hỏi: thay vì hỏi "câu này có giống câu chuẩn không", em hỏi **"câu này có dẫn được tới đúng nút không"**. Đó là cách chấm em sắp trình.

Hai là **dạy thế nào cho câu bớt mơ hồ** — vì dạy thẳng ra câu thì không có gì buộc mô hình phân biệt nút đích với mấy nút giống nó bên cạnh.

Em xin nói phần chấm trước, vì nếu thước hỏng thì mọi việc phía sau vô nghĩa.

## 6. Chấm bằng cách nào · slide 8 · 2 phút 45 giây

Có một thứ gọi là **bộ trỏ**, em xin giải thích luôn: đó là một mô hình chuyên làm đúng một việc — đưa cho nó một câu thì nó chỉ ra một điểm trên ảnh. Em dùng **UGround, bản hai tỉ tham số**, là mô hình mở, tải về chạy tại máy chứ không gọi dịch vụ nào.

Cách chấm: đưa câu mô hình viết cho bộ trỏ, nó trả về một điểm, rồi so điểm đó với **chỗ người thật đã chạm**. Rơi đúng nút đó thì câu tính đúng.

Lý lẽ đơn giản: câu hướng dẫn tốt là câu mà một người chưa biết đáp án vẫn lần ra đúng nút.

Ở đây em xin nói rõ một chỗ rất dễ hiểu nhầm. **Đây không phải kiểu lấy mô hình lớn ra chấm bài**, cái mà bên ngành hay gọi là LLM-as-a-judge. Kiểu đó phải có thang điểm, và mô hình chấm có thể phán bừa. Em không hỏi ý kiến mô hình nào cả — em bắt bộ trỏ **làm** một việc rồi so kết quả với toạ độ có sẵn trong dữ liệu. Barem là toạ độ người thật đã chạm: khách quan, đúng sai rạch ròi.

Thầy chắc sẽ hỏi: sao em chắc bộ trỏ nó trỏ đúng. Em không dám nói nó luôn đúng, nhưng em **đo được nó sai bao nhiêu**, và đó mới là thứ dùng được. Ba việc em đã làm.

Một, em đo sai số của nó: đưa ba trăm câu chuẩn của tập kiểm cho nó trỏ, rồi so với chỗ người thật đã chạm. Sai số trung vị **không phẩy bảy phần trăm** bề ngang màn — cỡ bảy pixel trên màn một nghìn tám. Ngưỡng em khoá trước là ba phần trăm, nên nó qua với biên rất rộng.

Hai, em kiểm công thức huấn luyện của nó **không chứa AndroidControl**, và nó **khác họ** với mô hình được chấm. Nếu không thì giám khảo đã học chính đề thi.

Ba, em biết trước nó hỏng kiểu gì và có sẵn bộ dò: khoảng **mười lăm phần trăm** số lần nó bỏ cuộc theo chiều ngang, trả về giữa màn rồi đoán chiều dọc. Em in bốn dấu hiệu đó ngay cạnh con số chính, không giấu.

Và vì em biết nó không hoàn hảo nên em không treo hết vào nó: có thêm chấm tay một trăm câu, và báo song song hai cách chấm.

## 7. Thước này có đáng tin không · slide 9 · 2 phút

Thước là em tự dựng nên em phải tự kiểm. Em theo phương pháp bơm lỗi của Sai ở EMNLP 2021: cấy mười loại lỗi biết trước vào câu, xem thước có bắt được không. **Đạt tám trên mười.** Hai tiêu chí rớt em xin khai luôn chứ không giấu.

Tiêu chí rớt thứ nhất: bộ trỏ mà lệch nhiều thì nó **kết oan câu đúng**. Em đo đường cong này bằng cách lấy một câu đúng rồi cố ý dời điểm trỏ ra xa dần, xem thước có đánh rớt oan không. Lệch ba phần trăm bề ngang màn thì kết oan **không phần trăm**; lệch tám phần trăm thì oan **hai mươi bốn phần trăm**.

Nên em biến nó thành **một cái cổng bắt buộc**: bộ trỏ phải đạt sai số dưới ba phần trăm mới được dùng. Ngày chín tháng tám em đo: **không phẩy bảy phần trăm**. Đạt, và biên rất rộng chứ không phải vừa đủ qua. Xác nhận thêm bằng dụng cụ thật: trong các ca sai số dưới ba phần trăm thì trăm phần trăm chấm đúng, trên một trăm tám mươi tám ca.

Tiêu chí rớt thứ hai: luật bắt câu **đảo nghĩa**. Ví dụ câu chuẩn là "bật thông báo" mà mô hình viết "tắt thông báo" — trỏ vẫn đúng cái công tắc đó, toạ độ không phân biệt được, nên phải có luật đọc chữ. Luật đó dò theo một bảng cặp từ soạn tay: bật/tắt, hiện/ẩn, chọn/bỏ chọn và vài cặp nữa. Cặp nào ngoài bảng thì thước không thấy. Em khai thẳng chứ không nhét thêm từ vào bảng cho điểm đẹp.

Ngoài máy chấm, khi có câu mô hình sinh em sẽ cho hai người chấm tay một trăm câu, độc lập với nhau, để đối chiếu máy với người.

## 8. Điểm cao nhất thực tế là 70 · slide 10 · 1 phút 30 giây

*(Mục quan trọng. Nói chậm — nó quyết định cách thầy đọc mọi con số về sau.)*

Em xin trình một con số **trước khi** trình kết quả, để tránh hiểu nhầm.

Quay lại con số bảy mươi em vừa nhắc. Em lấy **chính câu chuẩn do người thao tác viết** — không phải câu mô hình — đem chấm bằng đúng cách vừa nói. Bộ trỏ chỉ lần ra đúng nút **bảy mươi phần trăm** số bước. Đây chính là hai nhóm sáu mươi hai và bảy mươi chín ở slide trước gộp lại.

Nói cho dễ hình dung: đề thi này không ai được mười, vì chính đáp án mẫu đem đi chấm cũng chỉ được bảy.

Ba lý do mất ba mươi điểm đó: câu người viết cụt như em vừa nói, bộ trỏ đôi khi trỏ trượt, và màn hình có nhiều nút na ná nhau. Tức là **ba mươi điểm hụt nằm ở dụng cụ, không phải ở mô hình**.

Nên nếu mô hình của em được năm mươi lăm thì đó là năm mươi lăm **trên nền bảy mươi**, không phải trên một trăm.

Hai điều em muốn nhấn về phương pháp. Một là con số này đo xong **trước khi có bất kỳ kết quả nào**, có ghi ngày trong bản đăng ký, nên nó không phải thứ em nghĩ ra sau khi thấy điểm thấp. Hai là phép so chính của em là **hiệu số giữa hai bản**, mà hai bản chấm bằng cùng một dụng cụ, nên phần thiệt chung triệt tiêu trong hiệu.

*(Nếu thầy hỏi "vậy mô hình có thể vượt bảy mươi không": có thể, nếu nó viết câu rõ hơn cả câu người viết. Đây không phải trần toán học mà là mốc thực tế, vì mô hình học viết theo câu người. Vượt được thì đó là kết quả đáng nói và em sẽ khai rõ.)*

## 9. Toàn bộ quy trình, và đích sinh · slide 11–12 · 1 phút 30 giây

Quy trình gồm năm khâu. Ba khâu đầu là dựng dữ liệu, **tự động hoàn toàn** — không dán nhãn tay, và cũng không có nhãn nào do máy sinh. Khâu bốn là huấn luyện, đây là chỗ duy nhất hai bản khác nhau. Khâu năm là chạy thật.

Về đích sinh, em xin nói rõ vì nó vừa là điểm mạnh vừa là giới hạn.

**Đích sinh là câu do chính người thao tác viết**, lấy nguyên từ bộ dữ liệu, không qua mô hình nào. Nghĩa là trong vòng huấn luyện không có nhãn máy sinh — không ai vặn được là nhãn máy có sạch hay không.

Giá phải trả là câu người viết rất cụt: trung vị sáu từ, **bốn mươi ba phần trăm câu từ năm từ trở xuống**. Mô hình học viết cụt theo. Và đây đúng là lý do điểm cao nhất chỉ tới bảy mươi — hai chuyện đó là một.

Còn một khâu chuẩn bị nữa là **đọc chữ trên ảnh bằng OCR**, danh sách chữ nối vào đầu vào. Nút nào là hình vẽ như dấu cộng hay mũi tên thì OCR chịu. Khâu này là tiền xử lý, em khai rõ không thuộc phần đóng góp.

## 10. Đóng góp mức một · slide 13–14 · 2 phút 15 giây

Đóng góp của em quy về một ý: **buộc mô hình nói rõ nó đang nhắm nút nào, rồi mới cho viết câu**.

Cách dạy thông thường là đưa ảnh vào rồi bắt viết thẳng ra câu. Cách của em thì mô hình phải viết một **dòng khai báo bốn ô** trước đã: nút thuộc loại gì, tên gì, ở toạ độ nào, và khác gì mấy nút bên cạnh. Xong bốn ô đó mới tới câu hướng dẫn. Lúc chạy thật thì dòng khai báo bị cắt đi — người dùng chỉ nhận câu. Nó tồn tại chỉ để ép mô hình, trong lúc học, xác định xong mục tiêu rồi mới viết.

Ba điểm em muốn nhấn. Một là ô toạ độ lấy từ **đúng chỗ người thật đã chạm** — nhãn sạch tuyệt đối, có ở trăm phần trăm số bước chạm, mà cách huấn luyện thường bỏ phí hoàn toàn. Hai là dòng khai báo dựng **hoàn toàn tự động** từ cây trợ năng cộng OCR, không thuê người dán nhãn. Ba là em kiểm nó ở hai quy mô — lần đầu một nghìn bảy trăm bước, sau đó đủ bốn mươi mốt nghìn bước chạm, gấp hai mươi bốn lần — và cả năm chỉ số lệch dưới một điểm. Tức khâu dựng nhãn không hỏng khi lên quy mô.

Còn vì sao dòng khai báo phải **có cấu trúc chặt và bắt buộc có toạ độ** thì em học từ các bài trước. Aguvis ở ICML 2025 bỏ tầng trung gian đi thì độ đúng thao tác tụt mười một phẩy bốn điểm, đo trên chính AndroidControl. Chiều ngược lại mới quyết định thiết kế: Shikra cho thấy cùng một mô hình, cùng bài kiểm, để bước trung gian là **văn xuôi tự do** thì tụt bảy phẩy bốn, còn cho nó **chứa toạ độ** thì tăng năm phẩy chín.

*(Các bài này dùng thước khác nhau nên số chỉ nói lên chiều và cỡ, không so thẳng. Ba trong bốn số là hiệu tự trừ từ bảng của họ chứ không phải số in sẵn — khai luôn nếu bị vặn. Ảnh bảng gốc để ở slide dự phòng cuối bài.)*

Chỗ em khác họ: mấy bài trên sinh bước trung gian để cuối cùng ra **toạ độ**. Em sinh bước trung gian để cuối cùng ra **câu chữ cho người đọc**.

## 11. Một bước thật · slide 15–16 · 1 phút

Để thầy dễ hình dung, em lấy một bước có thật trong dữ liệu chạy qua đúng mấy khâu vừa nói.

Tác vụ là tìm áo thun đen trong app Zalando. Dữ liệu cho sẵn ba thứ: ảnh màn hình, toạ độ người dùng chạm là điểm bốn trăm chín chín, năm trăm bốn lăm, và câu người đó viết là "Tap on the colour filter".

Từ ba thứ đó em dựng thêm. Lấy toạ độ chạm tra vào cây trợ năng thì được cái hộp nhỏ nhất chứa điểm đó, biết phần tử này thuộc loại chữ bấm được, và trên màn có mười chín phần tử cùng loại. Cây trợ năng **không ghi tên**, nên OCR đọc chữ nằm trong hộp, ra chữ "Colour". Ô thứ tư lấy mốc là "bên phải chữ Brand".

Ghép lại thành nhãn dạy: dòng khai báo bốn ô, rồi mới tới câu hướng dẫn. Toàn bộ dựng tự động, không mất công dán nhãn tay.

## 12. Đóng góp mức hai · slide 17 · 1 phút 30 giây

Mức một mới dạy mô hình viết ra dấu hiệu phân biệt, nhưng chưa có gì **phạt** nếu câu cuối cùng vẫn mơ hồ. Mức hai vá đúng chỗ đó, can thiệp vào chính hàm mất mát.

Thầy hình dung màn hình có hai kính lúp giống hệt nhau. Câu "chạm biểu tượng tìm kiếm" áp vào cái nào cũng khớp — tức là câu mơ hồ. Cách xử của em: với mỗi bước, dựng sẵn một dòng khai báo **giả** lấy từ nút hàng xóm, rồi bắt mô hình so hai bên. Câu đích phải khớp với khai báo thật, và phải khớp **hơn hẳn** so với khai báo giả. Câu nào khớp cả hai bên như nhau thì bị phạt thêm.

Cơ chế phạt kiểu này có tiền lệ từ bài của Mao ở CVPR 2016, bên ảnh tự nhiên — em khai thẳng, không nhận là mới. Chỗ còn trống là ở miền giao diện: bài nền của mảng này là Widget Captioning ở EMNLP 2020, chính họ nêu ra đúng lỗi hai icon giống nhau, nhưng sáu năm nay hàm mất mát của cả dòng vẫn là cross-entropy thuần.

Em xin nói rõ: **hàm phạt này em chưa cài**. Đây là phần thiết kế, sẽ thử trên một lát dữ liệu nhỏ trước, có tín hiệu mới mở rộng.

## 13. Huấn luyện và lúc chạy thật · slide 18 · 30 giây

Phần huấn luyện không phức tạp: Qwen2.5-VL ba tỉ tham số, mô hình mở, tinh chỉnh bằng QLoRA.

Lúc chạy thật thì chỉ cần bộ đọc chữ và mô hình. Ảnh vào, mô hình sinh dòng khai báo rồi sinh câu, hệ thống cắt bỏ dòng khai báo, người dùng nhận đúng câu hướng dẫn. **Không cần cây trợ năng, không cần bộ trỏ** — hai thứ đó chỉ tồn tại lúc dựng dữ liệu và lúc chấm.

*(Nếu thầy hỏi đã chạy thử trên điện thoại chưa: chưa. Đây là đặc tính cỡ mô hình chứ chưa phải kết quả đo, khai đúng như vậy.)*

## 14. Sáu phiên bản và lực thống kê · slide 19–20 · 1 phút 15 giây

Bộ so sánh em khoá **trước khi nhìn bất kỳ kết quả nào**, và đã lưu lại có ngày giờ. Cặp chính là bản thường với bản khai báo. Kèm bốn nhánh nữa: khai báo **giả** nhưng dài đúng bằng khai báo thật, để loại khả năng thắng chỉ vì câu dài ra; khai báo **bỏ ô toạ độ**, để tách riêng phần công của toạ độ; nhánh **không huấn luyện gì**, chỉ đưa thông tin vào lúc chạy, để trả lời câu "có cần huấn luyện thật không"; và nhánh thử mức hai.

Về lực thống kê: em chấm **đủ bốn nghìn bốn trăm sáu mươi ba bước chạm** của tập kiểm, không lấy mẫu. Gom cụm theo ứng dụng thì được một nghìn không chín mươi mốt cụm, hiệu dụng bốn trăm năm mươi tư. Mức chênh nhỏ nhất còn đo được vào khoảng **bốn tới sáu điểm rưỡi**, trong khi tác dụng kỳ vọng ba tới tám điểm. Em xin lưu ý con số này là **ước chiếu** — số thật phải tính lại từ điểm của bản thường.

## 15. Trình tự chạy · slide 21 · 45 giây

Trình tự em khoá cứng, không đảo: huấn luyện bản thường trước với hai hạt giống khác nhau, chấm đủ, đo lực thống kê bằng số thật, khoá ngưỡng đậu rớt, rồi mới huấn luyện bản khai báo và các nhánh đối chứng.

Hiện em đang ở bước ba. Có ba chốt chặn, tiêu chí viết ra trước chứ không phải nhìn số rồi mới đặt: sau bản thường thì xem còn chỗ để chứng minh không; sau nhánh đối chứng thì chênh phải rõ mới chạy tiếp; trước chương kết quả thì đóng băng mọi con số.

## 16. Đã làm được tới đâu · slide 22 · 1 phút

*(Mục quan trọng. Bốn dòng, nói chậm.)*

Em xin báo bốn việc đã chạy xong, mỗi việc kèm một con số.

Một, **cổng bộ trỏ đã qua** — ngưỡng khoá trước là ba phần trăm, đo được không phẩy bảy.

Hai, **dữ liệu dạy đã dựng xong ở quy mô đủ**: sáu mươi tư nghìn năm trăm bước, gần mười ba nghìn tác vụ, khâu đọc chữ phủ trăm phần trăm, và chín trên chín phép kiểm bất biến đều đạt.

Ba, và cái này em nghĩ quan trọng nhất về mặt phương pháp: **rò rỉ giữa tập dạy và tập kiểm bằng không**. Không tác vụ nào xuất hiện ở cả hai bên. Rò rỉ là loại sai không sửa được sau khi đã huấn luyện, nên em coi đây là chốt chặn thật chứ không phải thủ tục.

Bốn, **bản thường đang huấn luyện**, hạt giống thứ nhất, xong sáng mai.

Bốn con số này em đo trên máy thật, không phải ước tính.

## 17. Giới hạn của thiết kế · slide 23–24 · 1 phút 45 giây

Em xin nói trước ba giới hạn, cả ba đều tìm ra khi chưa có kết quả và đã ghi vào bản đăng ký kèm ngày.

Thứ nhất, nặng nhất: **tập kiểm của em là tập giữ riêng theo tác vụ, không phải theo ứng dụng**. Chín mươi hai phần trăm ứng dụng trong tập kiểm cũng có mặt ở tập dạy — nghĩa là mô hình đã quen giao diện đó, chỉ là chưa từng làm bài đó. Phần **không hỏng**: phép so chính giữa hai bản vẫn đúng, vì hai bản dùng chung dữ liệu dạy, chung mô hình gốc, chung tập kiểm, chỉ khác đúng đích sinh, và không tác vụ nào trùng. Phần **phải hạ**: mốc so với gpt-4o-mini chỉ để tham khảo, vì mô hình của em được học các ứng dụng đó còn gpt-4o-mini thì không — lợi thế sân nhà, em khai ngay tại chỗ trình số.

*(Nếu thầy hỏi sao không dùng split ứng-dụng-chưa-thấy của bài gốc: bài gốc có chia, nhưng nhãn đó chỉ nằm trong bản TFRecord trên Google Cloud, cần TensorFlow; bản HuggingFace em dùng chỉ có split test chung, không kèm nhãn.)*

Thứ hai, bộ trỏ dùng để chấm có một kiểu hỏng riêng: **mười lăm phần trăm số lần nó bỏ cuộc theo chiều ngang** — trả về giữa màn rồi đoán chiều dọc. Em viết sẵn bốn dấu hiệu để dò và in ngay cạnh con số chính.

Thứ ba, nhánh "đưa sẵn lúc chạy" bị thiệt ba mặt: câu nhắc dài gấp hai phẩy bốn lần vùng mô hình từng thấy lúc học, phải cắt còn bốn mươi trong bảy mươi hai phần tử, và chỉ mười bốn phần trăm phần tử có tên. Nên nhánh này mà thua thì **không kết luận được gì**, em khai trước.

## 18. Việc xin thầy quyết · slide 25 · 1 phút 30 giây

Đây là việc quan trọng nhất của buổi hôm nay. Sáng mai em có điểm đầu tiên, và em muốn hai thầy trò thống nhất cách đọc kết quả **trước khi nhìn thấy số**.

Kịch bản một, bản khai báo **thắng rõ**, vượt ngưỡng đã khoá: đóng góp chính đứng vững.

Kịch bản hai, **chênh nhỏ hoặc ngang điểm**: luận điểm chuyển thành ngang chất lượng nhưng mô hình chỉ ba tỉ tham số, chạy tại máy người dùng, không phải gửi ảnh màn hình lên mạng. Kèm phân tích vì sao chênh nhỏ.

Kịch bản ba, **không thấy chênh**: em xin phép đọc đây là một kết quả âm nhưng làm chặt — có đăng ký trước, có đối chứng, có phân tích. Khi đó chương đo lường lên vai chính, mô hình thành phần minh hoạ.

Luận văn của em có ba phần đứng riêng được: mô hình, thành phần huấn luyện, và chương đo lường. Nên một phần không ra kết quả thì hai phần kia vẫn đứng.

Nếu thầy đồng ý cách đọc cả ba kịch bản thì về sau số ra thế nào cũng đã có cách đọc thống nhất từ trước, em không phải quay lại xin đổi cách kể giữa chừng.

## Kết · slide 26 · 15 giây

Dạ em trình bày đến đây. Mong thầy cho ý kiến về cách đọc ba kịch bản, và góp ý thêm chỗ nào em còn hở. Em cảm ơn thầy ạ.

---

## Phụ lục — câu dễ bị vặn *(liếc thôi, không đọc)*

- **"Sao điểm thấp thế?"** → Điểm cao nhất thực tế là 70 chứ không phải 100 — đo bằng chính câu người viết, có ghi ngày, trước khi có kết quả.
- **"Đóng góp chỉ là đổi định dạng dữ liệu?"** → Bộ đối chứng cô lập được vì sao nó chạy: khai báo giả cùng độ dài, bỏ toạ độ, đưa-sẵn-lúc-chạy. Cộng mức hai là công thức phạt tự viết.
- **"Bản khai báo dùng thêm dữ liệu lúc học, thắng là nhờ dữ liệu chứ?"** → Thông tin thêm chỉ có lúc học; lúc chạy hai bản nhận đầu vào y hệt. Đây là khung học-với-thông-tin-đặc-quyền của Vapnik 2009, và nhánh đưa-sẵn-lúc-chạy đo trực tiếp câu này.
- **"Train một lần thì chênh vài điểm là hên xui?"** → Dạ đúng, nên cặp chính train hai hạt giống, và chênh giữa hai lần chạy chính là cỡ nhiễu — mọi hiệu ứng công bố phải vượt nó.
- **"Mô hình được dạy sinh toạ độ, thước cũng chấm bằng toạ độ — luyện đúng bài thi à?"** → Lúc chấm cắt bỏ toàn bộ dòng khai báo kể cả toạ độ, chỉ đưa mỗi câu chữ cho bộ trỏ; mà bộ trỏ là mô hình khác họ, không dính gì tới huấn luyện.
- **"Bộ trỏ chấm dễ bị lừa?"** → Khai trước bằng chính nghiên cứu EACL 2026 (đổi cách diễn đạt làm bộ trỏ trượt tới 84%); ba lớp đỡ: chấm tay 100 câu, cắt kết quả theo độ dài, báo song song hai cách chấm.
- **"GCoT chứng minh định-vị-trước làm câu kém đi?"** → Số âm là ở chế độ ra lệnh cho mô hình chưa huấn luyện. Cùng bài đó, bảng 5, huấn luyện hẳn theo thứ tự định-vị-trước thì tăng 4,5 và 5,8.
- **"Tiếng Việt đâu?"** → Khai phạm vi từ chương một: dữ liệu chuẩn của mảng là tiếng Anh; kèm demo sinh tiếng Việt ở phụ lục.
- **"Sao không thử bản 7 tỉ?"** → Bản 3 tỉ là điểm triển khai trên máy người dùng, đó là lý do tồn tại của bài toán. Bản 7B là phương án dự phòng, chỉ dùng nếu 3B thua cả gpt-4o-mini.
- **"Đã chạy thử trên điện thoại chưa?"** → Chưa. Đây là đặc tính cỡ mô hình, không phải kết quả đo.
- **"Sáng mai có số rồi thì sao?"** → Chấm khoảng năm tiếng. Có hai điểm của hai hạt giống thì đo được cỡ nhiễu và lực thống kê thật, rồi mới khoá ngưỡng và huấn luyện bản khai báo.
