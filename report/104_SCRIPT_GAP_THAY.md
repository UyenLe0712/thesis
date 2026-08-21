> ⚠️ LỖI THỜI 12/8 — thay bằng `report/111_SCRIPT_GAP_THAY_12_8.md` (slide v10). Giữ làm bản ghi.

# Script trình bày với thầy — 15 phút (bản 3, sửa 5/8 sau vòng soát độ-dễ-hiểu; theo slide v9 + report/103)

> Cách dùng: mỗi mục có [thời lượng] và [slide tương ứng]. Chữ nghiêng là ghi chú cho mình, không đọc.
> Tổng nói ~14 phút. Nếu thầy ngắt hỏi nhiều mà cháy giờ, cắt theo đúng thứ tự này: mục 10 (tiền) — mục 7 (huấn luyện) — đoạn "luyện đúng bài thi" ở mục 8. Tuyệt đối giữ mục 11, vì đó là thứ duy nhất buổi này phải chốt được.
> Nguyên tắc soạn: câu ngắn đủ một hơi thở; số quan trọng viết thành chữ cho khỏi vấp; thuật ngữ nào lần đầu xuất hiện đều kèm tên thật hoặc một mệnh đề giải nghĩa.

---

## Mở đầu — nói rõ hôm nay cần gì [30 giây]

Dạ em chào thầy. Hôm nay em xin trình bày kế hoạch cuối của luận văn, chừng mười lăm phút. Báo thầy tin chính trước: em đã chốt được phần mô hình tự huấn luyện, đúng như thầy yêu cầu từ đầu, và toàn bộ thiết kế thực nghiệm đi kèm. Phần chuẩn bị em đã làm xong rồi ạ: dữ liệu dạy đã dựng, thước chấm đã viết và đã tự kiểm bằng bơm lỗi, mấy phép đo thăm dò đã chạy. Việc còn lại là huấn luyện. Cuối buổi em có ba việc mong thầy quyết giúp: một là hướng đóng góp, hai là trình tự chạy thực nghiệm, ba là cách đọc kết quả cho từng kịch bản, kể cả kịch bản xấu. Em xin bắt đầu ạ.

*(Câu "mô hình tự huấn luyện, đúng như thầy yêu cầu" đặt ngay đầu là cố ý — thầy từng bác hướng prompting. Nói trước đích buổi gặp để thầy biết mình đến xin quyết định, không phải chỉ báo cáo.)*

## 1. Bài toán và vị trí của đề tài [2 phút — slide 3, 4, 5]

Đề tài của em là sinh hướng dẫn sử dụng phần mềm từ ảnh màn hình. Tình huống cụ thể thế này ạ: một người đang bí trong một ứng dụng, họ chụp màn hình rồi hỏi, ví dụ "làm sao chia sẻ playlist này cho bạn tôi". Mô hình nhìn bức ảnh đó và trả lời bằng một câu cho người đọc: "Chạm vào biểu tượng chia sẻ ở góc trên bên phải màn hình."

Cái khác so với các nghiên cứu cùng mảng nằm ở đầu ra. Các mô hình giao diện bây giờ, như Aguvis hay UI-TARS, đều được huấn luyện để tự bấm thay người, tức đầu ra là toạ độ nút cần bấm, dạng click mở ngoặc bảy ba hai phẩy một bảy ba. Còn đề tài của em thì đầu ra là câu chữ cho con người, và câu chữ là thứ duy nhất được đem chấm.

Trước khi đi vào chi tiết, em xin nói luôn luận văn gồm ba phần đứng riêng được. Một là mô hình: em tự huấn luyện cho một tác vụ chưa mô hình nào được dạy. Hai là thành phần huấn luyện: bắt mô hình nói rõ nó nhắm vào nút nào rồi mới cho viết câu, làm ở hai mức. Ba là chương đo lường: thước chấm em tự dựng và tự kiểm. Ba phần này không phụ thuộc nhau, nên một phần không ra kết quả thì hai phần kia vẫn đứng {D} chỗ này cuối buổi em sẽ nói kỹ.

Về tính mới, em đã tra kỹ, kiểm đến tận trang gốc từng bài. Bài sát nhất là GuideMe ở hội nghị CHI năm nay. Họ cũng sinh hướng dẫn cho người, nhưng làm bằng cách gọi GPT-5 qua mạng, không huấn luyện mô hình nào, và cũng không có thước nào chấm chất lượng câu. Vì vậy chữ "đầu tiên" em chỉ dám dùng ở đúng một chỗ: đây là mô hình mở đầu tiên được huấn luyện cho tác vụ này. Còn các cơ chế bên trong thì đều có tiền lệ, mượn của ai em khai rõ người đó.

*(GuideMe: đã đối chiếu abstract + phần toàn văn được index ngày 3/8 — hệ prompting GPT-5, đánh giá bằng khảo sát người dùng. Nếu thầy hỏi nguồn: bài open access, em đối chiếu phần phương pháp; toàn văn PDF sẽ tải bản chính thức khi ACM mở.)*

## 2. Em đo trước xem mô hình hay sai ở đâu [1 phút 20 — slide 6, 7]

Dữ liệu em dùng là AndroidControl, công bố ở NeurIPS 2024. Mười lăm nghìn tác vụ do người thật thao tác trên điện thoại. Mỗi bước có ảnh màn hình, có toạ độ chỗ người đó chạm, và có một câu mô tả do chính người đó viết.

Trước khi chọn cách can thiệp, em đo xem mô hình sinh câu thường sai kiểu gì. Em chạy trên hơn một trăm bước, tỉ lệ bịa ra nút không tồn tại chưa tới hai phần trăm. Rồi em lọc riêng bốn mươi ca đáng ngờ nhất, soi từng ca bằng tay. Kết quả là gần như không có ca bịa nào thật. Lỗi nhiều nhất hoá ra là câu mơ hồ, kiểu "chạm vào biểu tượng tìm kiếm" trong khi màn hình có tới hai biểu tượng tìm kiếm.

Em có một con số minh hoạ. Lấy bảy mươi sáu câu chuẩn do người viết, đưa cho một mô hình định vị — tiếng Anh gọi là grounding model, em xin gọi tắt là bộ trỏ — đọc câu rồi chỉ lên ảnh. Nửa câu cộc lốc chỉ trúng nút ba mươi hai phần trăm. Nửa câu tả rõ ràng thì trúng sáu mươi chín phần trăm. Mẫu này nhỏ nên em coi là dấu hiệu chỉ hướng, chưa phải bằng chứng chắc. Nhưng nó cho thấy một điều: chỗ khác nhau giữa hai nhóm câu chỉ là nhóm sau có nêu dấu hiệu phân biệt nút đó với các nút quanh nó. Vậy việc cần làm là ép mô hình tìm ra dấu hiệu đó trước khi viết câu. Đó chính là đóng góp em sắp trình bày.

## 3. Đóng góp — mức thứ nhất [2 phút 20 — slide 8, 9, 10]

Toàn bộ đóng góp của em gói trong một ý: buộc mô hình phải nói rõ được nó đang nhắm vào nút nào, rồi mới cho viết câu. Em làm điều đó ở hai mức.

Mức thứ nhất nằm ở đích huấn luyện. Cách dạy thông thường là đưa ảnh vào rồi bắt mô hình viết thẳng ra câu. Cách của em thì mô hình phải viết một dòng khai báo trước đã. Dòng đó có bốn phần. Nút thuộc loại gì. Tên gì. Nằm ở toạ độ nào. Và khác gì mấy nút bên cạnh. Viết xong bốn phần đó mới tới câu hướng dẫn. Khi chạy thật thì dòng khai báo bị cắt đi, người dùng chỉ nhận câu thôi. Dòng đó tồn tại chỉ để ép mô hình, trong lúc học, phải xác định xong mục tiêu rồi mới viết.

Ở mức này có ba điểm em muốn nhấn. Một là phần toạ độ lấy từ đúng chỗ người thật đã chạm. Đây là nhãn sạch tuyệt đối, có ở một trăm phần trăm số bước chạm, mà cách huấn luyện thông thường bỏ phí hoàn toàn. Hai là câu mô tả của người viết trong AndroidControl xưa nay chỉ được dùng làm đầu vào cho agent đoán thao tác. Em đảo lại, dùng nó làm đích để sinh. Theo những gì em tra được thì chưa ai làm vậy. Ba là nhãn khai báo được dựng hoàn toàn tự động, từ cây trợ năng — tức accessibility tree mà hệ điều hành xuất ra — cộng với OCR, không thuê người dán nhãn. Em đo thử trên hơn một nghìn bước: bảy mươi bảy phần trăm có tên rõ, phần toạ độ sạch một trăm phần trăm, còn phần tử nào không có tên thì em để trống chứ không đoán bừa.

Trước dòng khai báo còn hai khâu chuẩn bị, em xin nói nhanh. Khâu một là đọc chữ trên ảnh bằng OCR, chạy được ngay trên điện thoại; nút nào là hình vẽ như dấu cộng hay mũi tên thì OCR chịu, em xử riêng. Khâu hai là viết lại câu: em đưa ảnh đã khoanh dấu chỗ người chạm cho một mô hình lớn, nhờ nó viết câu cụt của annotator thành câu đầy đủ. Hai khâu này là tiền xử lý, em khai rõ là không thuộc phần đóng góp.

Từ đây em xin gọi tắt: cách dạy thông thường là bản thường, cách của em là bản khai báo.

## 4. Vì sao thiết kế đúng kiểu này [50 giây — slide 11]

*(Slide này giờ nằm ngay sau slide dòng khai báo — trả lời liền câu "sao lại bắt sinh toạ độ trước".)*

Bằng chứng sát nhất nằm ngay trên bộ dữ liệu em dùng. Aguvis ở ICML 2025 huấn luyện có tầng trung gian, thử trên chính AndroidControl. Khi họ bỏ tầng đó đi, độ đúng thao tác từng bước tụt mười một phẩy bốn điểm phần trăm. Em biết họ đo độ đúng thao tác chứ không đo chất lượng câu, nên em không mượn con số đó làm dự báo. Em chỉ mượn nó cho một điều: bỏ tầng trung gian đi thì hỏng. Còn với đề tài của em thì hỏng hay không, hỏng bao nhiêu, em phải tự đo.

Chiều ngược lại mới là chỗ quyết định thiết kế. Những bài cho mô hình viết bước trung gian bằng văn xuôi tự do thì đều ra kết quả âm. Rõ nhất là Shikra: cùng một mô hình, cùng một bài kiểm, để bước trung gian là văn tự do thì tụt bảy phẩy bốn, nhưng cho nó chứa toạ độ thì tăng năm phẩy chín. Hai dòng đó nói cùng một điều: bước trung gian phải có cấu trúc chặt và phải có toạ độ. Đó là lý do dòng khai báo của em có đúng bốn phần và bắt buộc có phần toạ độ — mỗi ràng buộc đều có con số đứng sau chứ không phải em chọn theo cảm tính.

Còn chỗ em khác họ: mấy bài trên sinh bước trung gian để cuối cùng cho ra toạ độ. Em sinh bước trung gian để cuối cùng cho ra câu chữ cho người đọc.

*(Nếu thầy hỏi GCoT: số âm hay được trích là ở chế độ prompting mô hình chưa huấn luyện; cũng bài đó, bảng 5, huấn luyện hẳn theo thứ tự định-vị-trước thì tăng 4,5 và 5,8. Nói thêm luôn: họ huấn luyện kèm dữ liệu quen đề nên không tách được nguyên nhân, còn phép so của em cùng một bộ dữ liệu, chỉ đổi đích sinh, nên tách được. Chỗ này em làm chặt hơn họ.)*

## 5. Một bước thật, từ dữ liệu tới nhãn dạy [45 giây — slide 12, 13]

Để thầy dễ hình dung, em xin lấy một bước thật trong bộ dữ liệu chạy qua đúng mấy khâu vừa nói.

Tác vụ này là tìm một chiếc áo thun đen trong app Zalando. Bộ dữ liệu cho sẵn ba thứ: ảnh màn hình, toạ độ người dùng đã chạm là điểm bốn trăm chín chín, năm trăm bốn lăm, và câu người đó viết là "Tap on the colour filter".

Từ ba thứ đó em dựng thêm. Lấy toạ độ chạm tra vào cây trợ năng thì được cái hộp nhỏ nhất chứa điểm đó, biết phần tử này thuộc loại chữ bấm được, và trên màn có mười chín phần tử cùng loại. Cây trợ năng không ghi tên, nên OCR đọc chữ nằm trong hộp, ra chữ Colour.

Ghép lại thành nhãn dạy: dòng khai báo gồm loại phần tử, tên Colour, toạ độ, và dấu hiệu phân biệt là một trong mười chín phần tử cùng loại. Xong dòng đó mới tới câu hướng dẫn. Toàn bộ dựng tự động, không mất công dán nhãn tay.

Ca vừa rồi là ca thuận lợi vì có chữ để đọc. Ca khó là nút hình. Ví dụ biểu tượng chia sẻ trong app Wynk Music, OCR không đọc được gì, thì em để trống ô tên, ba ô còn lại vẫn dựng bình thường. Đo trên hơn một nghìn bước thì bảy mươi bảy phần trăm có tên rõ, hai mươi phần trăm để trống, riêng ô toạ độ sạch một trăm phần trăm.

## 6. Đóng góp — mức thứ hai [1 phút 15 — slide 14]

Mức một mới chỉ dạy mô hình viết ra dấu hiệu phân biệt. Nhưng chưa có gì phạt nếu câu cuối cùng vẫn mơ hồ. Mức hai vá đúng chỗ đó, can thiệp sâu hơn, vào chính hàm mất mát.

Thầy hình dung màn hình có hai kính lúp giống hệt nhau. Câu "chạm biểu tượng tìm kiếm" áp vào cái nào cũng khớp, tức là câu mơ hồ. Cách xử của em: với mỗi bước, dựng sẵn một dòng khai báo giả lấy từ nút hàng xóm. Lúc huấn luyện em bắt mô hình so hai bên. Câu đích phải ăn khớp với khai báo thật. Và phải khớp với khai báo thật hơn hẳn so với khai báo giả. Mức khớp thì đo bằng chính xác suất mô hình gán cho câu. Câu nào khớp cả hai bên như nhau, tức là mơ hồ, thì bị phạt thêm.

Cơ chế phạt kiểu này có tiền lệ từ bài của Mao ở CVPR 2016, bên ảnh tự nhiên. Em khai thẳng, không nhận là mới. Cái còn trống là ở miền giao diện. Bài nền của mảng này là Widget Captioning, EMNLP 2020. Chính họ nêu ra đúng cái lỗi hai icon giống nhau. Nhưng sáu năm nay hàm mất mát của cả dòng vẫn là cross-entropy thuần, chưa ai đụng vào. Mức hai này em chạy thử trên một phần nhỏ dữ liệu trước, có tín hiệu thì mới mở rộng.

## 7. Huấn luyện, và lúc chạy thật thì có gì [30 giây — slide 15]

Phần huấn luyện không có gì phức tạp. Qwen2.5-VL ba tỉ tham số, dùng QLoRA nên thuê một card đồ hoạ là đủ, mỗi lượt chạy trọn bộ dữ liệu tốn mười ba đến mười sáu đô.

Còn lúc chạy thật, trên máy người dùng chỉ có hai thứ: bộ đọc chữ và mô hình. Ảnh vào, mô hình sinh dòng khai báo rồi sinh câu, hệ thống cắt bỏ dòng khai báo, người dùng nhận đúng câu hướng dẫn. Không cần mạng, không cần cây trợ năng, không cần toạ độ. Mấy thứ đắt tiền — cây trợ năng, mô hình lớn, bộ trỏ — chỉ tồn tại lúc dựng dữ liệu và lúc chấm, không theo ra máy người dùng.

## 8. Chấm điểm thế nào, và thước có đáng tin không [1 phút 45 — slide 16, 17]

Cách chấm của em như sau. Đưa câu mô hình viết cho một bộ trỏ độc lập, tức một mô hình khác họ, chưa biết đáp án, đọc câu rồi chỉ lên ảnh. Nó trỏ đúng nút người thật đã chạm thì câu được tính đúng. Lý lẽ đơn giản: câu hướng dẫn tốt là câu mà một bên thứ ba chưa biết đáp án vẫn lần ra đúng nút. Cách chấm này bên dòng referring expression — tức sinh câu mô tả sao cho người khác chỉ đúng vật — người ta dùng từ 2016 rồi ạ.

Ở đây em xin nói rõ một chỗ dễ hiểu nhầm. Đây không phải kiểu lấy một mô hình lớn ra chấm điểm bài, cái mà bên ngành hay gọi là LLM-as-a-judge. Kiểu đó phải có thang điểm, và mô hình chấm có thể phán bừa. Em không hỏi ý kiến mô hình nào cả. Em bắt bộ trỏ làm một việc — chỉ lên màn hình — rồi so chỗ nó chỉ với toạ độ người thật đã chạm. Thang điểm ở đây chính là toạ độ đó, có sẵn trong dữ liệu, khách quan, đúng sai rạch ròi. Bộ trỏ có ảo giác thì hậu quả là nó trỏ trượt, mà trỏ trượt thì thành chấm oan câu đúng — em đo hẳn mức oan đó chứ không bỏ qua.

Thước là em tự dựng, nên em phải tự kiểm nó. Em làm theo phương pháp bơm lỗi của Sai ở EMNLP 2021: cấy mười loại lỗi biết trước vào câu, xem thước có bắt được không. Kết quả đạt tám trên mười. Hai tiêu chí rớt em khai luôn chứ không giấu. Thứ nhất, nếu bộ trỏ dùng để chấm còn lệch nhiều thì nó chấm oan quá nửa số câu đúng. Vì vậy tuần đầu tiên em đặt một cổng bắt buộc: bộ trỏ chuyên — tức mô hình chỉ chuyên làm việc định vị — phải đạt sai số quanh ba phần trăm chiều rộng màn, cỡ ba mươi pixel, thì mới được dùng. Không đạt thì em có sẵn kế hoạch dự phòng, nới dần cách chấm từ chặt xuống lỏng, kèm khai tỉ lệ chấm oan ở từng mức. Thứ hai, luật bắt từ ngược nghĩa chỉ bắt được các cặp có trong bảng tay. Ngoài máy chấm, em còn cho hai người chấm tay một trăm câu, độc lập với nhau, để đối chiếu máy với người.

## 9. Thiết kế thí nghiệm và thống kê [1 phút 30 — slide 18, 19]

Bộ so sánh em khoá trước khi nhìn bất kỳ kết quả nào — bên thống kê gọi là đăng ký trước, pre-registration. Cặp chính là bản thường với bản khai báo. Kèm theo là ba nhánh đối chứng. Nhánh một: khai báo giả nhưng dài đúng bằng khai báo thật — để loại khả năng thắng chỉ vì câu dài ra. Nhánh hai: khai báo bỏ phần toạ độ — để tách riêng xem toạ độ đóng góp bao nhiêu. Nhánh ba: không huấn luyện gì cả, chỉ nhét thông tin vào đầu vào lúc chạy — để trả lời câu hỏi có cần huấn luyện thật không.

Về thống kê, em xử lý ba nguồn nhiễu. Mỗi bản chính huấn luyện hai lần với hai seed khác nhau; chênh giữa hai lần chạy chính là mức nhiễu của việc huấn luyện, và mọi hiệu ứng công bố phải vượt được mức đó. Các bước trong cùng một ứng dụng thì na ná nhau, nên khi tính khoảng tin cậy em gom theo ứng dụng. Và một trình tự cứng: huấn luyện bản thường trước, chấm đủ khoảng hai nghìn bước — tức toàn bộ bước chạm của tập kiểm chứ không lấy mẫu — đo lực thống kê bằng số thật, khoá ngưỡng đậu rớt xong xuôi, rồi mới huấn luyện bản khai báo. Em giữ đúng thứ tự đó để không ai nói được là thấy số rồi mới đặt ngưỡng.

## 10. Tiền, lịch và rủi ro [45 giây — slide 20, 21]

Về chi phí, phần chắc chắn khoảng tám mươi lăm đến một trăm mười hai đô, tình huống tốn nhất là một trăm sáu mươi hai, vẫn dưới ngân sách hai trăm. Thời gian còn khoảng tám tuần, trừ phần viết thì thực nghiệm còn năm sáu tuần. Em xếp các cổng quyết định lớn vào tuần một tuần hai, để nếu phải đổi hướng thì đổi sớm, chứ không để đến tuần cuối mới phát hiện.

Rủi ro lớn nhất là bộ trỏ không đạt cổng sai số ba phần trăm, vì cả thước chấm treo trên nó — nên em đo nó ngay tuần đầu, trước mọi khoản chi lớn, và đã có kế hoạch dự phòng ghi sẵn. Mấy rủi ro còn lại — tác dụng quá nhỏ để đo thấy, nhãn nhiễu, mô hình học vẹt cú pháp — rủi ro nào cũng có cách phát hiện sớm và đường xử lý viết sẵn từ bây giờ.

## 11. Ba kịch bản — việc em cần thầy quyết hôm nay [1 phút 20]

Cuối cùng là việc quan trọng nhất em muốn xin ý kiến thầy. Kết quả sẽ rơi vào một trong ba kịch bản, và em muốn hai thầy trò thống nhất cách đọc cả ba ngay từ bây giờ, trước khi em tiêu tiền huấn luyện.

Kịch bản một, bản khai báo thắng rõ, vượt ngưỡng: đóng góp chính đứng vững.

Kịch bản hai, chênh lệch nhỏ hoặc ngang điểm: luận điểm chuyển thành ngang chất lượng nhưng mô hình chỉ ba tỉ tham số, chạy ngay trên máy người dùng, không tốn phí gọi API và ảnh màn hình không phải gửi lên mạng. Kèm phân tích vì sao chênh nhỏ.

Kịch bản ba, không thấy chênh: em xin phép đọc đây là một kết quả âm nhưng làm chặt, có đăng ký trước, có đối chứng, có phân tích. Khi đó chương đo lường lên vai chính, mô hình thành phần minh hoạ. Luận văn em có ba phần đứng riêng được — mức một, mức hai, và chương đo lường — nên một phần không ra kết quả thì hai phần kia vẫn đứng.

Nếu thầy đồng ý cách đọc của cả ba kịch bản thì về sau số ra thế nào cũng đã có cách đọc thống nhất từ trước, em không phải quay lại xin đổi cách kể giữa chừng.

## Kết [15 giây — slide 22]

Dạ, em trình bày đến đây. Ba việc mong thầy cho ý kiến: hướng đóng góp, trình tự thực nghiệm, và cách đọc ba kịch bản kết quả. Em cảm ơn thầy ạ.

---

## Phụ lục — câu hỏi dễ gặp, ý trả lời một dòng *(không đọc, chỉ để liếc)*

- **"Đóng góp chỉ là đổi định dạng dữ liệu?"** → Trả lời bằng thiết kế thí nghiệm: bộ đối chứng cô lập được vì sao nó chạy, mức chặt mà nhiều bài đã đăng còn thiếu; cộng mức hai là công thức phạt tự viết, có mã, có số.
- **"Bản khai báo dùng thêm dữ liệu lúc học, thắng là nhờ dữ liệu chứ?"** → Thông tin thêm chỉ có lúc học, lúc chạy hai bản nhận đầu vào y hệt; đây là khung "học với thông tin đặc quyền" của Vapnik 2009; nhánh nhét-vào-đầu-vào-lúc-chạy đo trực tiếp câu này.
- **"Mỗi bản train một lần thì chênh vài điểm là hên xui?"** → Dạ đúng, nên cặp chính train hai đến ba seed, và dải chênh giữa các seed in ngay cạnh kết quả.
- **"Tiếng Việt đâu?"** → Khai phạm vi từ chương một: dữ liệu chuẩn của mảng là tiếng Anh; kèm demo sinh tiếng Việt khoảng mười màn ở phụ lục.
- **"Sao không thử bản 7 tỉ?"** → Bản 3 tỉ là điểm triển khai trên máy người dùng, đó là lý do tồn tại của bài toán; phương án dự phòng 7B khoảng ba mươi đô, chỉ dùng nếu bản 3B thua cả gpt-4o-mini.
- **"Người thật cần nhiều bước, demo trọn tác vụ đâu?"** → Khai phạm vi ở mức từng-bước; ghép chuỗi nhiều bước là hướng mở đã thiết kế sẵn.
- **"Bộ trỏ chấm dễ bị lừa?"** → Khai trước bằng chính nghiên cứu EACL 2026 (đổi cách diễn đạt làm bộ trỏ trượt tới 84%); ba lớp đỡ: chấm tay 100 câu, cắt kết quả theo độ dài, báo song song hai cách chấm.
- **"Mô hình được dạy sinh toạ độ, thước cũng chấm bằng toạ độ - luyện đúng bài thi à?"** → Lúc chấm cắt bỏ toàn bộ dòng khai báo, kể cả toạ độ, chỉ đưa mỗi câu chữ cho bộ trỏ; mà bộ trỏ là mô hình khác họ, không dính gì tới quá trình huấn luyện.
- **"GCoT chứng minh định-vị-trước làm câu kém đi?"** → Số âm là ở chế độ prompting chưa huấn luyện; bảng 5 cùng bài huấn luyện hẳn thì +4,5/+5,8; họ không tách được nguyên nhân vì train kèm dữ liệu quen đề, phép so của em tách được.
