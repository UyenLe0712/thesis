# Kịch bản trình thầy (11/2026)

Đi kèm `slides/LUAN_VAN_SLIDE_TRINH_THAY_15_11.pptx`. Sinh tự động từ ghi chú trong `slides/build/build_trinh_thay_15_11.js`; sửa lời ở script, không sửa tay file này.

## Slide 1
Em chào thầy. Hôm nay em báo cáo hai phần. Phần đầu nhắc lại bài toán và giải thích kỹ cách em chấm điểm bằng executability, vì đây là thước chính của mọi phép so. Phần sau là việc thầy giao hôm 1/11: so phương pháp với các thuật toán học tăng cường khác và so SPICE với các độ đo thưởng khác, kèm giải thích.

## Slide 2
Bài toán: mô hình nhìn màn hình hiện tại, biết mục tiêu người dùng và các bước đã làm, rồi viết một câu hướng dẫn cho bước tiếp theo, ví dụ "Tap Not now". Đầu ra là câu cho người đọc, không phải tọa độ cho máy tự bấm.

## Slide 3
Một câu có thể đúng ngữ pháp, nghe tự nhiên, mà vẫn vô dụng. "Tap the button" trên màn hình có mười nút thì người đọc không biết bấm nút nào. Vì vậy em cần một cách chấm kiểm được chuyện câu có giúp chọn đúng phần tử hay không. Đó là executability ở phần sau.

## Slide 4
Dữ liệu là AndroidControl của Google DeepMind. Bộ dữ liệu này dùng câu hướng dẫn làm đầu vào để dự đoán thao tác; em dùng theo chiều ngược lại, câu là đích sinh. Ở mỗi bước có tọa độ người dùng đã chạm thật, và chính tọa độ này giúp chấm executability. Mọi con số exec hôm nay tính trên 4.463 bước chạm của tập kiểm tra.

## Slide 5
Em giải thích executability bằng một hình dung đơn giản. Đưa câu mô hình viết cho một người lạ, không biết đáp án, chỉ nhìn màn hình và đọc câu, rồi xem người đó bấm vào đâu. Bấm đúng nút người dùng thật đã bấm thì câu đó dùng được.
Người lạ ở đây là UGround, một mô hình định vị giao diện có sẵn: đưa vào ảnh và câu, nó trả về một điểm trên màn hình. UGround không được huấn luyện cùng mô hình của em và không biết đáp án.
Executability là tỉ lệ số bước bấm đúng. Khác BLEU hay SPICE ở chỗ: các độ đo đó so câu chữ với câu chuẩn, còn executability đo xem câu có làm được việc của nó không.

## Slide 6
Đây là màn hình thật trong tập kiểm tra. Người dùng chạm vào ô Birthday, vòng vàng. Câu của S1 là "Click on the Birthday option"; UGround đọc câu này và chạm đúng ô Birthday, vòng xanh, bước này đạt.
Câu của mô hình gốc là "Click on the Gender section to change it to Male": câu dài, đúng ngữ pháp, nhưng gọi sai phần tử. UGround chạm vào ô Gender, dấu X đỏ, bước này không đạt.
Điểm đáng chú ý: hai ô chỉ cách nhau một hàng. Nếu chỉ đo khoảng cách thì câu sai vẫn có thể được tính đúng. Slide sau giải thích cách em loại trường hợp này.

## Slide 7
Một bước được tính đúng khi đạt đồng thời ba điều kiện.
Một: câu phải nói đúng loại thao tác. Bước cần chạm mà câu bảo vuốt lên hay quay lại thì sai ngay.
Hai: điểm UGround chạm không lệch quá 14% chiều ngang và 14% chiều dọc so với điểm người dùng chạm thật. Đây là ngưỡng quen thuộc của bộ AndroidInTheWild.
Ba: điểm chạm phải gần điểm thật hơn mọi phần tử bấm được khác trên màn hình, tức nằm trong ô Voronoi, là vùng tô vàng ở ví dụ trước. Điều kiện này để loại các câu gọi nhầm nút ngay bên cạnh.
Executability là số bước đạt cả ba, chia cho 4.463 bước chạm.

## Slide 8
Tại sao phải có điều kiện ba? Em thử bằng cách dịch điểm chạm có chủ ý. Nếu dịch sang phần tử bên cạnh, cách chấm chỉ dùng dung sai 14% vẫn chấp nhận 84,3% số ca, tức gần như không phân biệt được nút đúng với nút kế bên. Thêm điều kiện ô Voronoi thì chỉ còn 2,8%. Còn các ca chạm lệch nhẹ trong cùng phần tử vẫn được giữ 99,7%. Nghĩa là điều kiện ba siết đúng chỗ cần siết, không làm khó những ca đáng được tính đúng.

## Slide 9
Slide này để đọc con số. Trần không phải 100: chính câu chuẩn do người viết, đưa cho UGround, cũng chỉ đạt 75,7%, vì UGround đôi khi chạm lệch. Sàn cũng không phải 0: câu vô nghĩa "Tap the button" cho mọi bước vẫn đạt 12%, còn câu thật nhưng lấy của màn hình khác chỉ đạt 6,1%. Điều này cho thấy UGround thật sự đọc nội dung câu, câu đúng văn phong mà sai nội dung thì điểm rất thấp.
Trên thang này, mô hình gốc đạt 47,6; tinh chỉnh có giám sát S1 lên 59,1; học tăng cường thưởng SPICE lên 60,7; và phần thưởng mới SA-SPICE-v3 lên 61,2. Các mức chênh sau tinh chỉnh nhỏ, khoảng 1 đến 2 điểm, nên em luôn kèm khoảng tin cậy khi so.

## Slide 10
Để tin thước này, em làm bốn phép kiểm. Câu càng thiếu thông tin thì điểm càng thấp. Bỏ tên phần tử khỏi câu chuẩn thì mất 28,5 điểm trên các bước bị tác động, còn bỏ mô tả vị trí chỉ mất 3,5, nghĩa là thước thưởng đúng việc gọi tên phần tử. Đổi người làm theo sang ba mô hình định vị khác, trong đó Phi-Ground và Phi-4 không thuộc họ Qwen, thì phương pháp vẫn cao hơn S1. Và chấm lại nhiều lần cho cùng kết quả.

## Slide 11
Phương pháp có hai thành phần. Xuất phát từ S1 là Qwen2.5-VL-3B đã tinh chỉnh có giám sát. Thành phần một học tăng cường bằng GRPO với thưởng SPICE. Thành phần hai là ACE, tra bốn câu ví dụ giống nhất trong tập huấn luyện và chỉ thay câu khi qua hai điều kiện. Mô hình định vị UGround chỉ dùng để chấm, không nằm trong phần thưởng, nên thước chấm độc lập với mục tiêu huấn luyện.

## Slide 12
GRPO: với mỗi mẫu, mô hình viết tám câu, mỗi câu chấm SPICE so với câu chuẩn trừ phạt độ dài. Câu nào điểm cao hơn trung bình của nhóm tám câu thì được khuyến khích, thấp hơn thì bị giảm. Có thêm phạt KL để mô hình không đi quá xa S1. SPICE chấm theo đối tượng và quan hệ nên phù hợp với việc gọi đúng phần tử. Cách dùng độ đo làm phần thưởng đã có từ SCST và SPIDEr trong chú thích ảnh.

## Slide 13
ACE dựa trên quan sát: nhiều tác vụ lặp lại với thay đổi nhỏ, nên câu chuẩn của một bước cũ đôi khi dùng được nguyên văn. ACE tìm bốn bước giống nhất, cho bộ sinh xem bốn câu đó, và chỉ thay câu ban đầu khi câu mới chép nguyên văn một câu ví dụ và cùng loại thao tác. Ở phần lớn các bước, câu ban đầu được giữ.

## Slide 14
Kết quả chính trên tập kiểm tra. GRPO-SPICE đạt 60,65 executability, hơn S1 1,55 điểm, khoảng tin cậy từ 0,80 đến 2,33, không chứa 0. Hai tiêu chí vị trí khác, hộp phần tử của AndroidControl và tiêu chí của AitW, cũng tăng cỡ đó. Thêm ACE thì exec giữ nguyên nhưng các độ đo văn bản tăng thêm.

## Slide 15
Một câu hỏi tự nhiên là: nếu đổi người làm theo thì sao. Em chấm lại cùng các câu bằng ba mô hình định vị khác. Mức số tuyệt đối khác nhau vì mỗi mô hình định vị mạnh yếu khác nhau, nhưng GRPO-SPICE luôn cao hơn S1 và cả bốn khoảng tin cậy đều trên 0.

## Slide 16
Thầy yêu cầu so với các thuật toán RL khác và so SPICE với các độ đo thưởng khác. Em dựng hai lưới, mỗi lưới chỉ đổi một yếu tố. Lưới một giữ thưởng SPICE và đổi thuật toán: GRPO, SCST là mốc kinh điển của chú thích ảnh, REINFORCE, RLOO và PPO. Lưới hai giữ GRPO và đổi phần thưởng.
Mọi thứ khác giữ nguyên. Thêm ba mốc để đọc cho đúng: SFT tiếp là học thêm có giám sát trên đúng các câu nhắc đó, không có RL, để tách công của RL với công của việc học thêm. SPICE ghép ngẫu nhiên là thưởng không mang thông tin. Và GRPO chạy lại cùng cấu hình để biết hai lần chạy lệch nhau bao nhiêu.

## Slide 17
Đây là lưới thuật toán. Mỗi chấm là mức chênh executability so với S1, vạch ngang là khoảng tin cậy 95%. Chấm nằm bên phải vạch 0 là hơn S1.
Đọc ra ba điều. Thứ nhất, mọi thuật toán đều hơn S1, từ 0,3 đến 1,6 điểm; năm trong bảy lượt có khoảng tin cậy nằm hẳn trên 0. Thứ hai, các khoảng tin cậy chồng lên nhau nhiều, nên em không kết luận được thuật toán nào hơn hẳn. GRPO và SCST nhỉnh nhất, RLOO thấp nhất. Thứ ba, chạy lại GRPO đúng cấu hình cũ chỉ được 0,63, lệch lượt chính 0,92 điểm. Tức độ dao động giữa hai lần chạy đã cỡ khoảng cách giữa các thuật toán.
Hàng cuối là SFT tiếp, không có RL, cũng hơn S1 1,05. Nghĩa là một phần mức tăng đến từ việc học thêm trên các câu nhắc này, không riêng RL.

## Slide 18
Lưới phần thưởng, cùng cách đọc. Hàng quan trọng nhất là hàng cuối: nếu điểm SPICE bị ghép ngẫu nhiên giữa các câu, tức thưởng không mang thông tin gì, thì kết quả đúng bằng S1, chênh 0,00. Các thưởng thật cho từ 0,6 đến 2,1. Vậy mức tăng đến từ nội dung của phần thưởng, không phải từ việc chạy vòng lặp RL.
Giữa bốn độ đo SPICE, ROUGE-L, METEOR, CIDEr-D thì khoảng tin cậy chồng nhau, em chưa tách được bên nào hơn. Em không viết SPICE là tốt nhất.
Hàng đầu là phần thưởng mới SA-SPICE-v3, cao nhất 2,11 so với S1. Nhưng lượt này xuất phát từ SFT tiếp, nên so công bằng phải so với SFT tiếp: hơn 1,05, có ý nghĩa. Slide sau em nói kỹ.

## Slide 19
Tại sao các phần thưởng cho exec gần nhau? Em tách số bước sửa được so với S1 làm hai phần: bước S1 sai loại thao tác mà lượt mới sửa đúng, và bước đúng loại thao tác nhưng lượt mới chọn đúng phần tử hơn.
Mọi phần thưởng thật đều sửa loại thao tác rõ; thưởng ngẫu nhiên thì gần như không sửa gì. Khác nhau ở cách phân bổ: ROUGE-L sửa loại thao tác nhiều nhất, 48 bước, nhưng phần tử chỉ 20. SPICE thì ngược lại, phần tử 41, nhiều nhất trong các thưởng. Hai phần bù nhau nên tổng exec gần bằng.
Em ghi rõ đây là dấu hiệu, chưa phải kết luận: so trực tiếp từng cặp thì không còn ý nghĩa sau hiệu chỉnh Holm, và mới có một seed. Em không viết "SPICE giúp định vị tốt hơn".

## Slide 20
Bảng các độ đo văn bản. Ô tô màu là cao nhất mỗi cột. Không phần thưởng nào thắng mọi cột: SPICE nhỉnh ở BLEU-4 và SPICE, ROUGE-L nhỉnh ở CIDEr-D, SA-SPICE-v3 nhỉnh ở METEOR, ROUGE-L và chrF. Các chênh lệch đều nhỏ. Có một điểm lạ em khai thẳng: thưởng bằng CIDEr-D nhưng lại thấp ở chính CIDEr-D; em đã kiểm cách tính IDF và cách tách từ, chưa giải thích được.

## Slide 21
Từ phân tích trước, em thử một phần thưởng mới, SA-SPICE-v3. Nó trộn SPICE với chrF, vì với câu ngắn như "Scroll down" hay "Go back", SPICE cho 0 điểm kể cả khi câu đúng nguyên văn; chrF đỡ chỗ đó. Cộng thêm thưởng khi câu đúng loại thao tác.
Kết quả exec 61,21, cao nhất trong mọi lượt em đã huấn luyện, hơn điểm xuất phát 1,05 có ý nghĩa. So với GRPO-SPICE thì hơn 0,56 nhưng chưa có ý nghĩa, nên em chưa viết là hơn.
Điểm yếu: bước cuộn tăng nhưng bước quay lại giảm từ 71 xuống 58,5. Em đang chạy nhánh SPICE thuần từ cùng điểm xuất phát để tách xem phần trộn thưởng có thật sự giúp hay không.

## Slide 22
Tóm lại cho câu hỏi của thầy. RL có giúp, và giúp nhờ nội dung phần thưởng. Giữa các thuật toán, em không tách được bên nào tốt nhất, GRPO và SCST nhỉnh nhất, nhưng nhiễu giữa hai lần chạy cỡ khoảng cách đó. Giữa các phần thưởng, SPICE và ROUGE-L ngang nhau ở exec nhưng đi hai đường khác nhau. Em giữ GRPO-SPICE vì nó thuộc nhóm dẫn đầu ở cả hai lưới, có tiền lệ rõ, và phần thưởng không dùng mô hình định vị nên thước chấm vẫn độc lập.

## Slide 23
Các việc tiếp theo. Đang chạy nhánh SPICE thuần từ cùng điểm xuất phát với SA-SPICE-v3. Sau đó em chạy thêm hai seed cho SA-SPICE-v3, thử chữa bước quay lại, thêm DPO trực tuyến vào lưới thuật toán vì đây là phương pháp ưu tiên phổ biến nhất còn thiếu, và chạy thêm vài độ đo thưởng. Cuối cùng là đưa hai lưới và phần giải thích vào luận văn. Em xin ý kiến thầy về thứ tự ưu tiên.

## Slide 24
Kết luận ba ý. Executability là cách chấm câu bằng việc làm theo, và em đã kiểm nó phản ứng đúng với nội dung câu. Học tăng cường giúp nhờ nội dung thưởng; các thuật toán và độ đo thưởng phổ biến cho mức tăng gần nhau. GRPO-SPICE thuộc nhóm dẫn đầu ở cả hai lưới. Mọi kết quả hiện là một seed, em đang chạy thêm để chắc hơn. Em cảm ơn thầy.

## Dự phòng
Bảng đủ các chỉ số cho bốn cấu hình, mở khi thầy hỏi chi tiết.

## Dự phòng
Các phép kiểm khái quát. Trên tác vụ mới mức tăng còn lớn hơn. Khi các bước trước do mô hình tự viết, mức tăng giữ nguyên. Trên AitZ thì không còn khác S1. Seed thứ hai thấp hơn seed chính 0,72 nhưng vẫn hơn S1.

## Dự phòng
Định nghĩa hình thức của executability nếu thầy cần.
