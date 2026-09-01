# Kịch bản trình bày bảo vệ luận văn

Sinh tự động từ `slides/build/build_baove.js`. Sửa lời dẫn trong script rồi chạy lại
`node build_baove.js && python3 make_kichban.py`, đừng sửa tay file này.

---

## Slide 1 · (bìa)  —  ~25s  (cộng dồn 0:25)

Kính thưa hội đồng, em là Lê Đoàn Phương Uyên, học viên cao học ngành Trí tuệ nhân tạo, thực hiện luận văn dưới sự hướng dẫn của thầy Nguyễn Hồng Bửu Long. Đề tài của em là sinh hướng dẫn sử dụng phần mềm từ ảnh màn hình. Bài trình bày khoảng 25 phút, em xin bắt đầu.

## Slide 2 · Nội dung trình bày  —  ~25s  (cộng dồn 0:50)

Bài trình bày đi theo sáu phần. Em xin dành phần lớn thời gian cho hai chỗ: thước đo, vì đó là phần đóng góp đã hoàn tất, và phần chẩn đoán, vì đó là chỗ luận văn nói rõ được giới hạn thật của thành phần mà em đề xuất.

## Slide 3 · 1 · Bài toán: đầu ra là câu chữ, không phải toạ độ  —  ~50s  (cộng dồn 1:40)

Bài toán bắt đầu từ một tình huống rất đời thường: đang thao tác trên điện thoại thì bí, không biết bấm gì tiếp.

Dòng nghiên cứu tác tử giao diện nhận đúng đầu vào này nhưng sinh ra toạ độ để máy tự bấm. Em đổi đầu ra: sản phẩm cuối là câu chữ cho người đọc, và câu cũng là thứ duy nhất đem chấm.

Chỗ này quan trọng vì nó quyết định cả phần đánh giá lẫn phần huấn luyện về sau. Mô hình nhắm tới cỡ ba tỉ tham số để chạy tại máy, vì ảnh màn hình là dữ liệu riêng tư.

## Slide 4 · 1 · Đổi đầu ra kéo theo hai vấn đề  —  ~60s  (cộng dồn 2:40)

Đổi đầu ra thì hai chỗ hỏng ngay.

Thứ nhất là đánh giá. Em đo mức hỏng của từng thước quen dùng chứ không nói suông: so khớp chuỗi kết oan 97,5% số câu chỉ diễn đạt khác; so vector ngữ nghĩa cho AUC 0,336, tức kém hơn đoán ngẫu nhiên, vì nó đo độ gần chủ đề chứ không đo hai câu có nói về cùng một phần tử hay không. Cặp inbox và outbox được chấm cao hơn cặp search và magnifying glass, dù cặp sau mới là cặp cùng chỉ một nút.

Thứ hai là dạng lỗi. Em đọc tay 40 trường hợp sinh sai: bịa đặt gần như không có, phần lớn là câu mơ hồ. Quan sát này đặt lại trọng tâm cải tiến cho cả luận văn.

## Slide 5 · 1 · Vị trí của luận văn so với các công trình gần nhất  —  ~40s  (cộng dồn 3:20)

Bảng này trả lời câu hỏi công trình đứng ở đâu.

Điều em muốn nói rõ ngay từ đầu là luận văn không nhận chữ &quot;đầu tiên&quot; cho ý tưởng câu phải đủ để bên kia trỏ đúng. Ý đó là của dòng sinh biểu thức quy chiếu, có từ 2016. Phần em nhận hẹp hơn nhiều: đưa ràng buộc phân biệt vào mục tiêu huấn luyện, trong miền giao diện, nơi công trình có giám sát gần nhất là Widget Captioning vẫn dùng entropy chéo thuần.

## Slide 6 · 1 · Ba đóng góp và trạng thái thật của từng đóng góp  —  ~60s  (cộng dồn 4:20)

Em xin nói trước trạng thái thật của ba đóng góp, để hội đồng theo dõi phần sau dễ hơn.

Đóng góp thứ nhất là thước đo, đã hoàn tất. Thứ hai là đường ống dữ liệu cộng một kết quả đã đăng ký trước, và em xin nói thẳng: kết quả này KHÔNG hoàn tất, vì đại lượng chính đòi trung bình hai hạt giống mà nhánh xử lý chỉ chạy được một, do ngân sách máy. Luận văn không lấy một phép so khác đã có số để thế chỗ. Thứ ba là phần chẩn đoán, đã hoàn tất, và đó là phần em thấy có giá trị nhất cho người làm tiếp. Ba phần này độc lập nhau về lập luận, nên phần chưa hoàn tất không kéo theo hai phần còn lại.

## Slide 7 · 2 · Dữ liệu: dựng bằng máy, không thuê người dán nhãn  —  ~50s  (cộng dồn 5:10)

Bộ dữ liệu gốc là AndroidControl, công bố tại NeurIPS 2024. Em ghép hai kho công khai theo khoá cặp tập phim và số bước: một kho giữ câu do người viết cùng cây trợ năng, kho kia giữ ảnh.

Phép ghép được kiểm bằng một đối chứng lệch chủ ý: nếu ghép đúng thì tỉ lệ khớp phải cao hơn hẳn bản cố tình lệch một bước, và số đo là 48 so với 20 phần trăm.

Điểm em muốn nhấn: toàn bộ nhãn dựng bằng máy, không thuê người, và cũng không lấy nhãn từ một mô hình ngôn ngữ khác, nên không có chuyện chưng cất ngầm từ một mô hình mạnh hơn.

## Slide 8 · 2 · Nhãn mô tả tự động cho phần tử người dùng đã chạm  —  ~50s  (cộng dồn 6:00)

Nhãn có bốn ô. Ô khó nhất là ô tên, vì cây trợ năng của Android tuy liệt kê rất nhiều phần tử nhưng chỉ khoảng một phần tám trong đó có tên đọc được. Em bù bằng phép trích chữ trên ảnh, cộng hai cổng lọc thêm vào sau khi đo thấy nhãn trợ năng có 14,7% là chuỗi rác.

Kết quả ở quy mô đủ: 73,6% bước có tên dùng được, 22% không có tên nào, 7,6% trùng tên với phần tử khác. Chính hai con số sau là lý do phải có ô dấu hiệu phân biệt.

Ô toạ độ thì miễn phí và sạch tuyệt đối, vì đó là chỗ người thật đã chạm.

## Slide 9 · 3 · Thành phần đề xuất: mô tả phân biệt trước, phát ngôn sau  —  ~60s  (cộng dồn 7:00)

Đây là thành phần em đề xuất. Thay vì dạy mô hình nhảy thẳng từ ảnh sang câu, em dạy nó mô tả phần tử đích trước rồi mới viết câu.

Chi tiết quan trọng nhất nằm ở dòng đỏ: lúc chấm em CẮT tầng khai báo, chỉ đưa câu cho mô hình định vị. Nếu không cắt thì mọi mức tăng đều có thể giải thích bằng việc mô hình được cho thêm thông tin lúc chấm, và đóng góp sẽ tụt xuống thành đóng góp về dữ liệu.

Về việc vì sao bước trung gian phải có toạ độ chứ không phải văn xuôi, em dựa vào cặp Shikra: cùng mô hình cùng bài kiểm, chỉ đổi dạng bước trung gian, một bên âm bảy phẩy bốn, một bên dương năm phẩy chín.

## Slide 10 · 3 · Chặng huấn luyện thứ hai: mục tiêu ưu tiên ở tầng khai báo  —  ~65s  (cộng dồn 8:05)

Nhánh khai báo để lại một chẩn đoán rõ: cơ chế không hỏng, cái hỏng là độ chính xác của ô khai báo. Học có giám sát thuần không tác động thẳng vào việc chọn phần tử, nên em thêm một chặng huấn luyện bằng mục tiêu ưu tiên.

Cặp dữ liệu được dựng tối thiểu đúng nghĩa: hai vế giống nhau từng chữ ở phần câu, chỉ khác ô khai báo. Nhờ vậy gradient rơi đúng vào việc chọn phần tử.

Và đây là chỗ em xin nhấn về mặt phương pháp: chặng thêm 800 bước tự nó đã làm mô hình đổi, nên em chạy kèm một nhánh đối chứng cùng điểm xuất phát, cùng số bước, chỉ khác ở việc có hay không có số hạng ưu tiên. Đại lượng đăng ký là hiệu giữa hai nhánh đó, chứ không phải mức tăng thô.

## Slide 11 · 4 · Thước đo executability  —  ~65s  (cộng dồn 9:10)

Đây là phần đóng góp đã hoàn tất.

Ý tưởng: đưa câu cho một mô hình định vị độc lập, nó trả về một điểm, rồi hỏi điểm đó có rơi đúng phần tử người dùng đã chạm không.

Ba điều kiện phải cùng thoả. Điều kiện thứ ba là chỗ có nội dung kỹ thuật: không chỉ đòi điểm dự đoán nằm trong dung sai, mà còn đòi trong toàn bộ phần tử trên màn, phần tử người dùng chạm phải là phần tử gần điểm dự đoán nhất. Vùng thoả tính chất đó chính là ô Voronoi trong hình bên phải.

Câu em muốn nói rõ với hội đồng: đây không phải mô hình tự chấm. Barem là toạ độ người thật đã chạm, có sẵn trong dữ liệu, và mô hình định vị không bao giờ thấy toạ độ đó.

## Slide 12 · 4 · Luật xác định trúng được chọn từ sàn mà nó đạt được  —  ~45s  (cộng dồn 9:55)

Một câu hỏi tự nhiên là vì sao không dùng luôn ngưỡng dung sai quy ước của các công trình trước.

Em trả lời bằng phép đo, không bằng lập luận: đặt trước thước một câu cố tình gọi tên sai nút, ngưỡng dung sai vẫn chấm đúng cho 84,3% số ca. Một thước như vậy gần như không phân biệt được gì. Thêm điều kiện Voronoi thì con số đó xuống 2,8%.

Ba dòng dưới là ba chỗ mà chính em từng viết sai trong bản thảo rồi phải sửa sau khi đọc lại mã, nên em nêu luôn ở đây cho chính xác.

## Slide 13 · 4 · Trần và sàn đều là đại lượng đo được  —  ~60s  (cộng dồn 10:55)

Một thước chỉ đọc được khi biết trần và sàn của nó.

Trần đo bằng cách đem chính câu do người viết đi chấm như một nhánh bình thường: 75,7%. Mọi điểm số khác đọc trên nền này.

Sàn đo bằng hai nhánh đối chứng. Thay mọi câu bằng một câu chung chung không nói phần tử nào thì mô hình định vị vẫn trúng 12%, đó là phần đoán mò được. Còn khi thay bằng câu thật của một màn hình khác, tức câu đúng văn phong đúng độ dài nhưng sai nội dung, điểm rơi xuống 6,1%, thấp hơn cả câu chung chung.

Con số thứ hai là lá chắn quan trọng nhất của thước: nếu thước thưởng cho văn phong thì nhánh đó phải được điểm cao, nhưng thực tế nó thấp nhất.

## Slide 14 · 4 · Sáu khối kiểm chứng của thước  —  ~70s  (cộng dồn 12:05)

Đây là toàn bộ phần kiểm chứng của thước, và em xin nhấn: mỗi dòng là một phép đo có số, không phải một lập luận.

Hai dòng cuối là hai dòng nặng nhất về mặt phản biện. Dòng viết lại câu trả lời câu hỏi thước có mong manh trước cách diễn đạt không: viết lại 1.139 câu của người theo ba kiểu bảo toàn nghĩa, hiệu ròng chỉ 0,35 điểm và khoảng tin cậy loại được mọi mức tụt lớn hơn 0,6 điểm. Nhưng khi bỏ hẳn mệnh đề vị trí thì thước phạt đúng, nên nó không phải là một thước bất động.

Dòng cuối trả lời đòn mạnh nhất: dụng cụ chính có dữ liệu AndroidControl trong công thức huấn luyện, nên có thể nó quen văn phong của bộ ngữ liệu. Em chấm lại bằng một mô hình định vị thứ hai không dùng bộ này, phép so đối chiếu giữ được 94% độ lớn.

## Slide 15 · 4 · Thiết kế được niêm phong trước lượt huấn luyện đầu tiên  —  ~55s  (cộng dồn 13:00)

Slide này nói về quy trình, và em nghĩ nó đáng một phút.

Toàn bộ thiết kế so sánh cùng luật đọc cho cả bốn kết cục được đưa vào kho phiên bản trước lượt huấn luyện đầu tiên, nên kiểm được bằng lịch sử phiên bản.

Ý nghĩa thực tế: khi kết quả ra ô trắng, em không phải nghĩ ra cách trình bày mới, vì cách đọc ô trắng đã viết sẵn từ khi chưa có số. Các mục sửa đổi cũng ghi kèm ngày chứ không sửa đè, và phần lớn ra đời trước điểm số đầu tiên.

Mức chênh nhỏ nhất phát hiện được là 2,2 điểm. Xin hội đồng giữ con số này trong đầu, vì mọi kết quả sau đây đọc trên nó.

## Slide 16 · 5 · Kết quả chính trên 4.463 bước chạm  —  ~55s  (cộng dồn 13:55)

Đây là bảng kết quả chính.

Đọc từ trên xuống: trần của thước là 75,7. Mô hình gốc chưa tinh chỉnh được 47,6. Sau khi tinh chỉnh trên tập giám sát dựng tự động, nó lên 59,1 và 59,6 ở hai hạt giống.

Ba nhánh dưới vạch là phần chặng hai, và cả ba mang nhãn thăm dò vì chỉ có một hạt giống. Em sẽ nói kỹ về chúng ở hai slide sau.

Một điều bản đăng ký bắt em kiểm trước tiên: nếu nhánh nền đã sát trần thì phải dừng nghiên cứu vì không còn chỗ để cải thiện. Kết quả cho thấy ba khoảng tin cậy rời nhau hoàn toàn, nên thước phân giải được cả ba mức, và vẫn còn khoảng trống thật.

## Slide 17 · 5 · So sánh ghép cặp và các cách giải thích thay thế  —  ~60s  (cộng dồn 14:55)

Vì mọi nhánh chấm trên cùng một tập bước nên phép so đúng là phép so ghép cặp.

Tinh chỉnh đáng 11,5 điểm. Con số này phải đọc kèm nhiễu dựng lại đường ống, đo bằng hai hạt giống của chính nhánh nền, là 0,52 điểm. Tín hiệu gấp 22 lần nhiễu.

Em cũng tự trừ đi phần dễ: một phần tư số bước mô hình chép lại nguyên văn câu chuẩn. Bỏ hết đi thì khoảng cách vẫn còn 8,4 điểm.

Sáu ô dưới là sáu cách giải thích thay thế mà em kiểm từng cái. Ô cuối màu đỏ là ô nặng nhất và cũng là ô đắt nhất: nó chỉ loại được sau khi chấm lại bằng một mô hình định vị thứ hai, tốn tám giờ máy.

## Slide 18 · 5 · Nhánh khai báo: một kết quả thăm dò, không kết luận được  —  ~70s  (cộng dồn 16:05)

Đây là kết quả mà em phải trình bày đúng như nó là.

Nhánh khai báo thấp hơn nhánh nền 1,93 điểm. Về mặt thống kê thì p rất nhỏ, nhưng độ lớn lại nằm dưới mức chênh nhỏ nhất mà thiết kế phát hiện được, nên theo đúng luật đã khoá, đây là ô trắng chứ không phải kết quả âm. Và vì hạt giống thứ hai bị huỷ, đại lượng chính không hoàn tất.

Phần đáng giá là chẩn đoán bên phải: 7,3% số bước gánh một phần ba chênh lệch, và đó là nhóm bước mà mô hình đoán sai luôn loại thao tác.

Đi truy tiếp thì gặp một điều không ai chờ: mô hình gốc gọi đúng loại thao tác nhiều hơn cả hai bản đã huấn luyện. Đây là cái giá của tinh chỉnh, và nguyên nhân quy được về thiết kế dữ liệu, vì tập dạy chỉ gắn khai báo cho bước chạm.

## Slide 19 · 5 · Chặng hai: điểm cao nhất, nhưng phần lớn không thuộc mục tiêu ưu tiên  —  ~75s  (cộng dồn 17:20)

Chặng hai cho điểm cao nhất trong mọi điểm lưu của đề tài: 60,0.

Nhưng em không trình con số đó như thành tích, vì có nhánh đối chứng để tách công. Đi từ S2 lên CE2 được 2,24 điểm, đó là công của việc huấn luyện thêm 800 bước bất kể mục tiêu gì. Đi tiếp từ CE2 lên MIN-DESC chỉ được 0,63 điểm, và đó mới là phần thuộc riêng mục tiêu ưu tiên. Tức 78% mức tăng thuộc về đối chứng. Đo thẳng ở tầng khai báo thì tỉ lệ ấy lặp lại, 87%.

Theo luật đã khoá từ trước, 0,63 điểm là ô trắng: có ý nghĩa trên nhiễu của thước, nhưng dưới mức phát hiện được của thiết kế, và chỉ bằng 1,4 lần độ lệch chuẩn giữa hạt giống.

Nếu không có nhánh đối chứng này thì em đã có thể trình mức tăng 2,87 điểm và nghe rất thuyết phục. Đó là lý do tồn tại của nó.

## Slide 20 · 5 · Chẩn đoán: cơ chế đúng, nhưng bị chặn bởi độ chính xác khai báo  —  ~65s  (cộng dồn 18:25)

Slide này trả lời câu hỏi vì sao một cơ chế nghe hợp lý lại chỉ cho 0,94 điểm.

Em cắt quần thể theo việc ô khai báo do chính mô hình sinh ra có trỏ đúng phần tử hay không. Trên 60,6% số bước nó khai báo đúng, và ở đó nó hơn nhánh chỉ sinh câu tới 8,83 điểm, thậm chí vượt cả trần câu người viết của nhóm ấy. Nhưng trên 39,4% còn lại, nó thua 11,12 điểm.

Tức là cơ chế hoạt động đúng như giả thuyết, nhưng nó chỉ đúng trên phần mà nó nhắm trúng, còn ở phần nhắm trượt thì nó tự làm hỏng kết quả. Hai chiều triệt tiêu nhau và cộng lại thành gần như không.

Em xin khai rõ: cách chia nhóm này là hậu kiểm, không nằm trong lát cắt đã đăng ký.

## Slide 21 · 5 · 63% dư địa còn lại nằm gọn trong một ô duy nhất  —  ~70s  (cộng dồn 19:35)

Đi sâu thêm một bậc, em phân rã toàn bộ quần thể theo trạng thái ô khai báo.

Bảng cho ba ràng buộc cho mọi thiết kế tiếp theo. Thứ nhất, ô đúng cả hai đã hết chỗ: mô hình vượt trần câu người viết trên gần một nửa số bước. Thứ hai, 63% dư địa còn lại nằm gọn trong một ô duy nhất, là ô sai cả tên lẫn toạ độ, nơi mô hình chỉ được 3,6 điểm còn nhánh nền được 25,8. Nghĩa là khai báo sai không chỉ vô ích mà còn phá hỏng câu. Thứ ba, câu người viết đạt 64,4 ngay trong ô đó nên các bước này giải được.

Em cũng đã thử né ở khâu suy luận bằng bảy bộ định tuyến khác nhau; tất cả đều nằm trong nhiễu. Kể cả một bộ định tuyến hoàn hảo cũng chỉ cho 63,5%. Kết luận: phải sửa ở khâu huấn luyện.

## Slide 22 · 6 · Hạn chế, tự khai kèm số đo  —  ~65s  (cộng dồn 20:40)

Em xin nêu hạn chế bằng số chứ không bằng lời chung chung.

Nặng nhất là một hạt giống ở mọi nhánh xử lý. Thứ hai, điều kiện không gây hại mà chính em đăng ký đã bị trượt: ở bước không chạm, lớp thao tác tụt gần 20 điểm trong khi ngưỡng khoá là 3. Executability chỉ chấm trên bước chạm nên điểm chính không bị đụng, nhưng em không viết bất kỳ phát biểu nào kiểu mô hình cuối tốt hơn mà bỏ qua điều kiện này.

Thứ ba là một lối tắt trong dữ liệu cặp, phát hiện sau khi đã huấn luyện xong, bản vá đã viết nhưng không còn lượt huấn luyện nào để gộp vào.

Bên phải là hạn chế của dụng cụ. Chỗ chưa đóng được là cả hai mô hình định vị đều cùng họ với mô hình bị chấm.

## Slide 23 · 6 · Hướng phát triển  —  ~70s  (cộng dồn 21:50)

Hướng đi tiếp không phải là tinh chỉnh thêm tương phản, vì chẩn đoán đã chỉ ra chỗ nghẽn nằm ở độ chính xác khai báo.

Hướng thứ nhất là sửa cách nhắm: thay vì để mô hình tự nghĩ ra tên phần tử, đưa cho nó danh sách ứng viên dựng sẵn từ trích chữ và cây trợ năng. Ba con số căn cứ đều đã đo được mà không tốn một giây GPU nào, và con số cuối là con số em thấy thuyết phục nhất: hai phần ba số bước mà mô hình gọi sai tên thì tên đúng đã nằm sẵn trong câu nhắc, nó chỉ không dùng được vì thiếu neo vị trí.

Hướng thứ hai là dạy mô hình lùi khi không chắc. Hướng thứ ba là chạy nốt hạt giống thứ hai, vì không có nó thì mọi số về thành phần đề xuất vẫn là thăm dò.

## Slide 24 · Kết luận  —  ~45s  (cộng dồn 22:35)

Tóm lại, luận văn để lại ba thứ.

Một thước đo có phần kiểm chứng đứng bằng phép đo chứ không bằng lập luận. Một kết quả định lượng cho thấy tinh chỉnh trên tập giám sát dựng tự động đáng 11,5 điểm và đứng vững qua sáu cách giải thích thay thế. Và một chẩn đoán chỉ đúng chỗ mà mọi can thiệp tiếp theo phải tác động vào.

Phần thành phần đề xuất cho kết cục ô trắng, và em dừng đúng ở đó theo luật đã khoá từ trước.

Hai bài báo tách từ luận văn đang trong quá trình bình duyệt.

## Slide 25 · (bìa)  —  ~0s  (cộng dồn 22:35)

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 1 · Vì sao không dùng BLEU, ROUGE hay vector ngữ nghĩa

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 2 · Chấm lại bằng UI-Venus-Ground-7B

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 3 · Độ bền của luật chấm và tính tất định

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 4 · Thước có mong manh trước cách diễn đạt không

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 5 · Sàn của thước, và gọi tên so với chỉ vị trí

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 6 · Cấu hình huấn luyện và chi phí máy

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 7 · Trạng thái cuối của bảy nhánh đã đăng ký

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 8 · Một biến thể đã đăng ký nhưng không dựng nổi dữ liệu

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 9 · Vùng mù của thước, theo cả hai chiều

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 10 · Cổng cơ học và thiệt hại ở bước không chạm

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

---

**Tổng phần trình bày: 22 phút 35 giây** ở tốc độ 135 từ mỗi phút, chưa tính thời gian chuyển slide và dừng lại chỉ bảng.

Mười slide dự phòng nằm sau slide 25, không thuộc mạch chính. Lúc trình chiếu, gõ số slide rồi Enter để mở.
