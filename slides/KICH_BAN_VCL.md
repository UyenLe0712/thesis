# Kịch bản trình bày hội nghị VCL2026

Sinh tự động từ `slides/build/build_vcl.js`. Sửa lời dẫn trong script rồi chạy lại
`node build_vcl.js && python3 make_kichban_vcl.py`, đừng sửa tay file này.

---

## Slide 1 · HỘI THẢO QUỐC GIA LẦN 4 VỀ NGÔN NGỮ HỌC TÍNH TOÁN  -  VCL 2026  —  ~15s  (cộng dồn 0:15)

Kính thưa quý vị, tôi là Lê Đoàn Phương Uyên, Khoa Công nghệ Thông tin, Trường Đại học Khoa học Tự nhiên, Đại học Quốc gia Thành phố Hồ Chí Minh. Báo cáo này là công trình chung với thầy Nguyễn Hồng Bửu Long.

## Slide 2 · Nội dung trình bày  —  ~20s  (cộng dồn 0:35)

Bài toán ở đây là từ ảnh chụp màn hình và mục tiêu người dùng, viết ra một câu đủ để người đọc biết phải chạm vào đâu. Tôi sẽ dành nhiều thời gian nhất cho cách dựng nhãn và các kiểm định chất lượng, vì đó là hai phần mà một bộ ngữ liệu tự động cần chứng minh nhiều nhất.

## Slide 3 · 1 · Bài toán: viết câu để người khác trỏ đúng một phần tử  —  ~45s  (cộng dồn 1:20)

Một tác tử điều khiển giao diện nhận câu chỉ dẫn rồi trả về toạ độ để máy tự bấm. Chúng tôi làm chiều ngược lại: hệ thống nhận ảnh và mục tiêu, còn câu chỉ dẫn chính là thứ phải viết ra, cho người đọc chứ không cho máy.

Về mặt ngôn ngữ học, đây đúng là bài toán sinh biểu thức quy chiếu theo phát biểu của Dale và Reiter: câu sinh ra phải đủ để người nghe nhận ra đúng một đối tượng, không lẫn với những đối tượng khác cùng có mặt.

## Slide 4 · 1 · Miền giao diện đảo ngược thứ tự ưu tiên của quy chiếu  —  ~55s  (cộng dồn 2:15)

Điểm làm miền giao diện khác hẳn ảnh tự nhiên nằm ở ba con số này. Đo trên 120 màn lấy ngẫu nhiên từ 99.131 màn của cây trợ năng, chỉ 12,6% phần tử có nhãn văn bản, và 22 trong 120 màn ấy không có phần tử nào được đặt tên. Trên 41.099 nhãn đã dựng, 22% phần tử cần chạm không có tên, 7,6% trùng tên. Hai nhóm này rời nhau nên gộp lại là 29,6% số bước.

Ở ảnh tự nhiên, đối tượng nào cũng có danh từ để gọi, nên quan hệ chỉ là phương án bổ sung. Ở đây, gần một phần ba số trường hợp, quan hệ với chữ lân cận là phương tiện quy chiếu duy nhất còn lại.

## Slide 5 · 1 · Vị trí của bài so với các dòng nghiên cứu liên quan  —  ~40s  (cộng dồn 2:55)

Khung khái niệm chúng tôi dùng lại nguyên từ dòng sinh biểu thức quy chiếu, gồm cả cách mô tả bằng quan hệ của Dale và Haddock. Phần thêm vào là đo phân bố nhãn trong một miền mà phương tiện gọi tên gần như không có sẵn.

So với Widget Captioning, nhãn của chúng tôi dựng bằng quy tắc chứ không do người viết. So với chính bài AndroidControl, câu chỉ dẫn theo bước của họ là đầu vào, còn ở đây là đầu ra mong đợi. Chúng tôi không dùng chữ đầu tiên cho ý này.

## Slide 6 · 2 · Không bản phát hành nào có đủ ba thành phần cần dùng  —  ~55s  (cộng dồn 3:50)

Không bản phát hành công khai nào của AndroidControl mang đủ ba thành phần chúng tôi cần, nên phải ghép hai bản theo khoá episode và step.

Ghép lệch một bước là loại lỗi nguy hiểm nhất, vì số dòng vẫn đủ, huấn luyện vẫn hội tụ, mọi khâu vẫn chạy, trong khi mô hình học ảnh của bước này với câu của bước kia. Chúng tôi kiểm bằng cách chạy OCR ngay tại điểm chạm đáp án rồi xem chuỗi đọc được có nằm trong câu chỉ dẫn không. Ghép đúng cho 48,3%, đối chứng cố ý ghép lệch chỉ 19,6%. Bản thân 48% không nói lên điều gì; kết luận nằm ở khoảng cách giữa hai con số.

## Slide 7 · 2 · Cây trợ năng không đủ, nên chữ trên màn phải đọc bằng OCR  —  ~50s  (cộng dồn 4:40)

Cây trợ năng lẽ ra là nguồn tên tự nhiên nhất, nhưng một màn có trung vị 86 phần tử mà chỉ 12,6% có nhãn. Vì vậy toàn bộ ảnh được đưa qua OCR. Hệ quả là trong hơn 32 nghìn tên lấy được, tỉ lệ giữa cây trợ năng và OCR vào khoảng một trên hai phẩy bảy.

Chúng tôi quan sát được hai dạng sai sót. Biểu tượng bị đọc thành ký tự nguy hiểm hơn, vì sinh ra chuỗi trông như tên thật. Nguyên tắc chúng tôi theo là với dữ liệu huấn luyện, lỗi bỏ sót ít tốn kém hơn hẳn lỗi gán sai.

## Slide 8 · 2 · Dòng nhãn bốn ô, dựng hoàn toàn bằng quy tắc  —  ~65s  (cộng dồn 5:45)

Đây là dòng nhãn mà mô hình phải học để sinh ra, gồm bốn ô: vai trò, tên, toạ độ, và dấu hiệu phân biệt. Nhãn chỉ dựng cho bước chạm, và phần tử cần chạm xác định bằng hộp bao nhỏ nhất chứa điểm chạm của đáp án, vì cây trợ năng lồng nhiều tầng nên một điểm chạm nằm trong hàng chục hộp cùng lúc.

Hình dưới là một bước thật thuộc trường hợp khó, khi phần tử cần chạm không có tên. Bốn biểu tượng cùng vai trò, không cái nào có tên. Chương trình lấy chuỗi OCR gần nhất nằm ngoài hộp bao, ở đây là chữ Gmail cách tâm 114,5 px, làm mỏ neo. Đáng chú ý là câu của người chú thích cho cùng bước cũng quy chiếu qua đúng chữ đó.

## Slide 9 · 2 · Hai bộ lọc, mỗi bộ thêm vào sau khi đo thấy nhãn bị nhiễu  —  ~45s  (cộng dồn 6:30)

Hai bộ lọc này không có trong thiết kế ban đầu; chúng tôi thêm sau khi đọc tay mẫu thử và thấy nhãn bị nhiễu, nên bài nêu đúng theo thứ tự thời gian đó.

Bộ lọc thứ nhất loại những chuỗi đúng cú pháp nhưng người dùng không dựa vào được để tìm ra nút. Bộ lọc thứ hai chỉ cho lấy tên từ OCR khi hộp chiếm dưới một phần tư màn. Điểm chung là khi tên không kiểm chứng được thì để ô tên trống, chứ không điền một chuỗi phỏng đoán.

## Slide 10 · 2 · Ô dấu hiệu phân biệt: từ 7,3% lên 75,9% sau khi làm lại  —  ~55s  (cộng dồn 7:25)

Đây là phần chúng tôi phải làm lại từ đầu. Bản đầu của ô thứ tư chỉ giải quyết được 7,3% số trường hợp, còn 85,8% là mệnh đề đếm số lượng, kiểu một trong bảy phần tử cùng loại. Mệnh đề như vậy đúng về mặt sự kiện, nhưng chỉ nêu rằng có mơ hồ chứ không giúp chọn ra phần tử nào.

Chúng tôi sắp xếp lại quy tắc theo tiêu chí mệnh đề có giải quyết được mơ hồ hay không, và bổ sung mỏ neo chữ. Trên cùng mẫu thử, tỉ lệ đi từ 7,3% lên 75,9%; trên toàn bộ ngữ liệu là 75,3%. Cách dựng chỉ bảo đảm hướng đúng, chưa bảo đảm mệnh đề hữu ích.

## Slide 11 · 3 · Độ phủ của dấu hiệu lệch theo hướng bất lợi  —  ~60s  (cộng dồn 8:25)

Bảng này phân loại toàn bộ 41.099 dấu hiệu theo tầng tên của phần tử cần chạm. Dòng tổng được 75,3%, nhưng con số gộp che mất chênh lệch giữa ba tầng, và chênh lệch ấy đi theo hướng bất lợi.

Tầng tên rõ ràng, tức tầng mà bản thân cái tên đã đủ quy chiếu, đạt 80,1%. Tầng chỉ có ký hiệu, nơi dấu hiệu gần như là phương tiện duy nhất còn lại, chỉ đạt 37,5%. Nguyên nhân là cơ học: mỏ neo cần một chuỗi OCR đủ gần, mà vùng dày biểu tượng không nhãn cũng thường là vùng thưa chữ. Hướng mỏ neo lệch theo trục ngang, đó là hệ quả của quy ước bố cục Android.

## Slide 12 · 3 · Người chú thích và quy trình tự động chọn cùng một chiến lược  —  ~55s  (cộng dồn 9:20)

Câu hỏi đặt ra là việc phân biệt có phải bài toán thật hay không, và chúng tôi trả lời bằng ba số đo từ hai phía.

Phía màn hình, 55,6% số bước có sẵn ít nhất một phần tử cạnh tranh đủ gần, và 91,6% có phần tử cùng vai trò, trung vị tám phần tử một màn. Phía ngôn ngữ, trong hơn 41 nghìn câu của người chú thích, 32,5% phải dùng tới từ chỉ vị trí hoặc thứ tự, còn quy trình tự động cho 67,2% dấu hiệu là quan hệ với chữ lân cận.

Khác biệt còn lại là người chú thích nhìn thấy hình dạng của biểu tượng rồi đặt tên, còn quy trình thì chỉ đọc được chữ.

## Slide 13 · 3 · Quy mô, cách chia tập và ba điều cách chia không bảo đảm  —  ~50s  (cộng dồn 10:10)

Về quy mô, tập huấn luyện có 64.567 bước với 41.191 bước chạm, tập kiểm tra có 6.958 bước. Bộ ngữ liệu chúng tôi đặt tên là GUIRefCorpus, gồm 41.099 dòng và 4.448 dòng.

Tập chia theo tác vụ, và kiểm rò rỉ chạy trên toàn bộ ngữ liệu cho kết quả không tác vụ nào trùng. Nhưng cách chia ấy chỉ bảo đảm đúng một điều đó. Nó không tách được cách diễn đạt, không biến tập kiểm tra thành tập ứng dụng chưa từng thấy, và hơn một nửa số bước không quy được về ứng dụng nào. Chúng tôi nêu cả ba để không ai đọc kết quả rộng hơn mức dữ liệu cho phép.

## Slide 14 · 4 · Phép so với một nguồn nằm ngoài quy trình  —  ~65s  (cộng dồn 11:15)

Đây là chỗ dựa chính của bài. Một bộ ngữ liệu dựng bằng quy tắc có điểm yếu cố hữu: mọi số đo tính từ chính bộ quy tắc chỉ cho biết quy tắc chạy đúng như đã viết, chứ không cho biết nhãn có đúng hay không.

Quy trình dựng nhãn không đọc câu chỉ dẫn ở bất kỳ khâu nào, nên khi ô tên trùng chữ người chú thích dùng, đó là so sánh với nguồn bên ngoài. Trên 3.505 nhãn có tên, 53,5% ô tên xuất hiện nguyên văn trong câu của người. Đối chứng đầu có thể bị chê là quá dễ, nên chúng tôi làm chặt hơn, chỉ ghép với bước liền sau trong cùng một chuỗi thao tác, tức hai màn rất giống nhau; tỉ lệ khớp nhầm là 7,6% và tỉ số vẫn bảy lần. Con số 53,5% là một chặn dưới.

## Slide 15 · 5 · Hạn chế của bộ ngữ liệu  —  ~40s  (cộng dồn 11:55)

Ba hạn chế chúng tôi nêu rõ. Thứ nhất, 24,7% dấu hiệu vẫn chưa giải quyết được mơ hồ; nguyên nhân đã xác định được nên chỗ này sửa được, hướng trước tiên là mở rộng nguồn neo sang các phần tử cùng vai trò.

Thứ hai, so sánh với nguồn bên ngoài mới chạm được một trong bốn ô; cách kiểm đúng nhất cho ô dấu hiệu là hỏi thẳng người dùng, và chúng tôi chưa làm được. Thứ ba là hai giới hạn đến từ chính bản phát hành gốc.

## Slide 16 · 5 · Kết luận  —  ~45s  (cộng dồn 12:40)

Tóm lại, bài trình bày một quy trình hoàn toàn tự động chuyển AndroidControl thành bộ ngữ liệu GUIRefCorpus. Chữ hoàn toàn tự động nói về khâu dán nhãn: người vẫn tham gia nhưng chỉ ở khâu kiểm định, và mỗi lần thấy nhãn sai thì thứ được sửa là bộ quy tắc rồi dựng lại từ đầu.

Chỗ dựa chính là phép đối chiếu ngoại sinh, 53,5% so với 7,6% ở đối chứng khó. Và nguyên tắc chúng tôi rút ra là phải tìm cho ra cơ chế sinh ra một tỉ số bất thường trước khi lấy tỉ số ấy làm căn cứ đổi thiết kế.

## Slide 17 · Cảm ơn  —  ~12s  (cộng dồn 12:52)

Tôi xin kết thúc ở đây. Cảm ơn quý vị đã lắng nghe, và rất mong nhận được câu hỏi cùng góp ý.

## Dự phòng 1 · Chất lượng nhãn không suy giảm khi tăng quy mô

Mở khi có câu hỏi về việc chất lượng nhãn ở mẫu thử có còn giữ được khi dựng cho toàn bộ ngữ liệu hay không. Sáu chỉ số lệch không quá 1,6 điểm phần trăm giữa hai quy mô, mà mẫu thử nhỏ hơn 38 lần. Slide này cũng có tỉ lệ 1 trên 2,7 giữa hai nguồn tên.

## Dự phòng 2 · Truy nguyên một tỉ số 3,2 lần

Mở khi có câu hỏi vì sao vẫn ưu tiên cây trợ năng trước OCR, dù OCR cho nhiều tên hơn. Đây là chỗ chúng tôi suýt đổi thiết kế vì một tỉ số 3,2 lần, rồi truy ra tỉ số ấy chỉ dựng trên 6,7% mẫu thử và cơ chế sinh ra nó là chuyện lọc chuỗi, không phải chuyện thứ tự.

## Dự phòng 3 · Bốn nhánh dữ liệu và chín bất biến cấu trúc

Mở khi có câu hỏi bộ ngữ liệu được dùng như thế nào, hoặc làm sao bảo đảm bốn nhánh chỉ khác nhau đúng ở phần nhãn. Điểm cần nhấn là bất biến thứ nhất: câu được chấm giống hệt nhau từng byte ở cả bốn nhánh.

## Dự phòng 4 · Bốn lỗi bắt được lúc dựng dữ liệu

Mở khi có câu hỏi về việc dựng nhãn tự động thì làm sao biết nhãn đúng. Bốn lỗi này đều xảy ra trong lúc mọi khâu vẫn chạy bình thường, nên chỉ có kiểm định mới lộ ra được.

## Dự phòng 5 · Chuỗi mục tiêu bị cắt ngay từ bản phát hành gốc

Mở khi có câu hỏi về chất lượng đầu vào, cụ thể là chuỗi mục tiêu của tác vụ. Cần nói rõ phần thiếu mất ngay từ bản phát hành gốc, và bốn nhánh dùng chung chuỗi đã bị cắt nên không tạo chênh lệch giữa chúng.

## Dự phòng 6 · Nguồn, giấy phép và dữ liệu người dùng lẫn trong ảnh

Mở khi có câu hỏi về giấy phép, quyền riêng tư, hoặc ý nghĩa của công trình với người dùng trợ năng.

## Dự phòng 7 · Ba kiểm định nội bộ còn lại

Mở khi có câu hỏi liệu mô hình có học được lối tắt nào từ cách dựng dữ liệu hay không. Quy tắc cứ chọn vế dài hơn chỉ đoán đúng 43,2%, thấp hơn cả mức ngẫu nhiên.

## Dự phòng 8 · Phần nằm ngoài phạm vi bài này

Mở khi có câu hỏi về kết quả huấn luyện. Phần đó thuộc bài đồng hành đang bình duyệt, nên ở đây chỉ nêu một quan sát liên quan tới giả định của ô dấu hiệu phân biệt, cùng cách dựng cặp quy chiếu trong dải 80 đến 350 px.

## Dự phòng 9 · Bốn nhãn thật, đặt cạnh câu của người chú thích

Mở khi có câu hỏi nhãn trông thế nào, hoặc nhãn tự động khác câu của người ra sao. Hai trường hợp đầu là chỗ nhãn làm được việc, hai trường hợp cuối là chỗ nhãn mới chỉ báo rằng có mơ hồ.

## Dự phòng 10 · Vì sao dựng nhãn bằng quy tắc

Mở khi có câu hỏi vì sao không nhờ một mô hình sinh nhãn cho tự nhiên hơn. Lập luận chính: nhãn quy tắc dựng lại được và kiểm định lại được, còn nhãn gán sai thì dạy mô hình gọi phần tử bằng chuỗi không tồn tại. Cũng nói thẳng chỗ yếu: nghèo hơn về chất lượng ngôn ngữ, và chúng tôi chưa định lượng được khoảng cách đó.

## Dự phòng 11 · Bốn khuôn câu của ô dấu hiệu phân biệt

Mở khi có câu hỏi con số 75,3% được tính ra sao, hoặc bốn nhóm dấu hiệu là gì. Điểm cần nói rõ: phép khớp là tất định vì khuôn do chính quy tắc sinh, nhưng cũng vì vậy nó chỉ đếm loại mệnh đề chứ không xác nhận mệnh đề hữu ích.

## Dự phòng 12 · Ngôn ngữ của ngữ liệu và khả năng chuyển sang miền khác

Mở khi có câu hỏi vì sao ngữ liệu là tiếng Anh, hoặc quy trình có chuyển sang tiếng Việt được không. Phải phân định rõ phần đã kiểm là việc đổi khuôn mẫu nhãn chỉ là thay đổi từ vựng, còn phần chưa đo là chạy quy trình trên giao diện tiếng Việt.

## Dự phòng 13 · Một bản ghi của GUIRefCorpus có gì

Mở khi có câu hỏi bộ ngữ liệu gồm những trường gì, hoặc về giấy phép và ảnh đi kèm. Không hứa ngày phát hành dữ liệu.

---

**Tổng phần trình bày: 12 phút 52 giây** ở tốc độ 135 từ mỗi phút, chưa tính thời gian chuyển slide và dừng lại chỉ bảng. Slot hội nghị: 15 phút trình bày + 15 phút hỏi đáp.

13 slide dự phòng nằm sau slide 17, không thuộc mạch chính. Lúc trình chiếu, gõ số slide rồi Enter để mở.
