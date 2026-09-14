# Kịch bản trình bày bảo vệ luận văn

Sinh tự động từ `slides/build/build_baove.js`. Sửa lời dẫn trong script rồi chạy lại
`node build_baove.js && python3 make_kichban.py`, đừng sửa tay file này.

---

## Slide 1 · (bìa)  —  ~26s  (cộng dồn 0:26)

Giới thiệu tên, ngành, thầy hướng dẫn, tên đề tài. Thời lượng khoảng 25 phút.

## Slide 2 · Nội dung trình bày  —  ~23s  (cộng dồn 0:49)

Sáu phần. Dành nhiều thời gian nhất cho thước đo (đóng góp đã hoàn tất) và phần phân tích lỗi (chỉ ra giới hạn thật của thành phần đề xuất).

## Slide 3 · 1 · Bài toán: đầu ra là câu chữ, không phải toạ độ  —  ~38s  (cộng dồn 1:27)

Tình huống: người dùng không biết bấm gì tiếp trên điện thoại.

Tác tử giao diện: cùng đầu vào nhưng sinh toạ độ cho máy tự bấm.

Đề tài: đầu ra là câu chữ cho người đọc, và câu là thứ duy nhất đem chấm.

Mô hình ba tỉ tham số, chạy tại máy vì ảnh màn hình là dữ liệu riêng tư.

## Slide 4 · 1 · Đổi đầu ra kéo theo hai vấn đề  —  ~47s  (cộng dồn 2:14)

Vấn đề 1, đánh giá: so khớp chuỗi loại nhầm 97,5%; vector ngữ nghĩa AUC 0,336, đo độ gần chủ đề chứ không đo cùng phần tử (inbox/outbox 0,76 cao hơn search/magnifying glass 0,55).

Vấn đề 2, dạng lỗi: đọc tay 40 ca, gần như không bịa, phần lớn là câu mơ hồ.

Kết luận: trọng tâm là tính phân biệt của câu.

## Slide 5 · 1 · Công trình liên quan  —  ~39s  (cộng dồn 2:53)

Không nhận chữ &quot;đầu tiên&quot;: ý câu phải đủ để bên kia trỏ đúng là của dòng sinh biểu thức quy chiếu từ 2016.

Phần nhận: đưa tính phân biệt vào mục tiêu huấn luyện trong miền giao diện; Widget Captioning vẫn dùng entropy chéo thuần.

## Slide 6 · 1 · Ba đóng góp và trạng thái thật của từng đóng góp  —  ~44s  (cộng dồn 3:37)

Đóng góp 1: thước đo, hoàn tất.

Đóng góp 2: quy trình dựng dữ liệu và kết quả thực nghiệm có nhánh so sánh; nhánh xử lý chỉ một hạt giống vì ngân sách máy, nên không kết luận thành phần có tác dụng hay không.

Đóng góp 3: phân tích lỗi từng bước, hoàn tất, giá trị nhất cho người làm tiếp.

## Slide 7 · 2 · Dữ liệu: dựng bằng máy, không thuê người dán nhãn  —  ~40s  (cộng dồn 4:17)

AndroidControl, NeurIPS 2024. Ghép hai kho công khai theo khoá (episode, step).

Kiểm phép ghép bằng cách so với phép ghép cố ý lệch một bước: 48% so với 20%.

Nhãn dựng bằng máy, không thuê người, không lấy từ mô hình ngôn ngữ khác.

## Slide 8 · 2 · Nhãn mô tả tự động cho phần tử người dùng đã chạm  —  ~46s  (cộng dồn 5:03)

Bốn ô nhãn. Ô tên khó nhất: cây trợ năng chỉ 12,6% phần tử có tên, bù bằng OCR, thêm hai bộ lọc (14,7% nhãn trợ năng là chuỗi không dùng được).

Quy mô đủ: 73,6% có tên dùng được, 22% không có tên, 7,6% trùng tên. Hai số sau là lý do cần ô dấu hiệu phân biệt.

Ô toạ độ lấy từ chỗ người thật đã chạm.

## Slide 9 · 3 · Thành phần đề xuất: mô tả phân biệt trước, phát ngôn sau  —  ~49s  (cộng dồn 5:52)

Thành phần đề xuất: mô tả phần tử cần chạm trước, viết câu sau.

Lúc chấm CẮT tầng khai báo, chỉ đưa câu cho mô hình định vị; nếu không cắt, mọi mức tăng có thể do được thêm thông tin lúc chấm.

Bước trung gian phải có toạ độ: cặp Shikra cho −7,4 (văn xuôi) và +5,9 (có toạ độ).

## Slide 10 · 3 · Chặng huấn luyện thứ hai: mục tiêu ưu tiên ở tầng khai báo  —  ~59s  (cộng dồn 6:51)

Phân tích lỗi từ nhánh khai báo: cơ chế đúng, điểm nghẽn là độ chính xác ô khai báo.

Chặng hai: mục tiêu ưu tiên trên cặp tối thiểu, hai vế giống nhau từng chữ ở phần câu, chỉ khác ô khai báo.

Nhánh so sánh CE2-S2: cùng điểm lưu, cùng 800 bước, chỉ bỏ số hạng ưu tiên. Đại lượng chính là hiệu giữa hai nhánh.

## Slide 11 · 4 · Thước đo executability  —  ~56s  (cộng dồn 7:47)

Ý tưởng thước: đưa câu cho mô hình định vị độc lập, hỏi điểm trả về có rơi đúng phần tử đã chạm không.

Ba điều kiện; điều kiện thứ ba đòi phần tử đã chạm là phần tử gần điểm dự đoán nhất (ô Voronoi).

Không phải mô hình tự chấm: chuẩn là toạ độ người thật đã chạm, mô hình định vị không thấy toạ độ đó.

## Slide 12 · 4 · Luật xác định trúng được chọn từ sàn mà nó đạt được  —  ~43s  (cộng dồn 8:30)

Vì sao không dùng ngưỡng dung sai quy ước: đặt câu cố tình sai nút, ngưỡng dung sai vẫn cho đúng 84,3%; thêm điều kiện Voronoi còn 2,8%.

Ba chi tiết của luật đọc thẳng từ cài đặt: vùng dung sai hình chữ nhật; hạt Voronoi là điểm chạm; Voronoi bao gồm luôn điều kiện dung sai.

## Slide 13 · 4 · Trần và sàn đều là đại lượng đo được  —  ~54s  (cộng dồn 9:24)

Trần: đem câu chuẩn đi chấm, 75,7%. Mọi điểm đọc trên nền này.

Sàn: câu chung chung 12%; câu thật của màn khác 6,1%, thấp hơn cả câu chung chung.

Số thứ hai là bằng chứng quan trọng nhất: thước không thưởng cho văn phong.

## Slide 14 · 4 · Sáu khối kiểm chứng của thước  —  ~54s  (cộng dồn 10:18)

Mỗi dòng là một phép đo có số.

Viết lại 1.139 câu bảo toàn nghĩa: hiệu ròng +0,35; bỏ mệnh đề vị trí thì thước phạt đúng.

Đổi mô hình định vị thứ hai không dùng AndroidControl: phép so đối chiếu giữ 94%.

## Slide 15 · 4 · Thiết kế so sánh và mức chênh nhỏ nhất phát hiện được  —  ~65s  (cộng dồn 11:23)

Mọi nhánh chấm trên cùng tập bước: hiệu ghép cặp.

MDE đo từ hai hạt giống của nhánh nền: sai số chuẩn ghép cặp 0,79, MDE 2,2 điểm (công thức chiếu cho 4 đến 9 vì giả định tương quan trong cụm bằng một).

Bảng bốn kết cục: dưới 2,2 không gọi là cải thiện; cận trên âm phải báo là gây hại.

## Slide 16 · 5 · Kết quả chính trên 4.463 bước chạm  —  ~46s  (cộng dồn 12:09)

Trần 75,7. Base 47,6. S1 59,1 và 59,6 ở hai hạt giống.

Năm nhánh dưới vạch chỉ một hạt giống. Điểm cao nhất là 60,07 của chặng ba, hơn chặng hai đúng 0,02 điểm, nên phải đọc hai nhánh ấy là cùng một mức chứ không phải một nhánh thắng.

Ba khoảng tin cậy của Base, S1 và trần rời nhau: thước phân giải được ba mức, còn khoảng trống cho can thiệp.

## Slide 17 · 5 · So sánh ghép cặp và các cách giải thích thay thế  —  ~45s  (cộng dồn 12:54)

Tinh chỉnh đáng 11,5 điểm; nhiễu hai hạt giống 0,52; tín hiệu gấp 22 lần nhiễu.

Bỏ một phần tư số bước chép nguyên câu chuẩn, vẫn còn 8,4.

Sáu cách giải thích thay thế; ô đỏ chỉ loại được sau khi đổi mô hình định vị thứ hai.

## Slide 18 · 5 · Nhánh khai báo: một hạt giống, không kết luận được  —  ~60s  (cộng dồn 13:54)

S2 thấp hơn nhánh nền 1,93; p nhỏ nhưng dưới MDE nên không kết luận được, không phải kết quả âm; hạt thứ hai không chạy.

Phân tích lỗi: 7,3% số bước chiếm một phần ba chênh lệch, là nhóm đoán sai loại thao tác.

Mô hình gốc gọi đúng loại thao tác nhiều hơn cả hai bản đã huấn luyện: chi phí của tinh chỉnh, do tập dạy chỉ gắn khai báo cho bước chạm.

## Slide 19 · 5 · Chặng hai: phần lớn mức tăng không thuộc mục tiêu ưu tiên  —  ~57s  (cộng dồn 14:51)

Chặng hai đạt 60,05, nhưng có nhánh so sánh để tách công.

S2 → CE2: +2,24 do huấn luyện thêm; CE2 → MIN-DESC: +0,63 riêng mục tiêu ưu tiên. 78% thuộc nhánh so sánh; ở tầng khai báo 87%.

0,63 trên nhiễu thước nhưng dưới MDE. Không có nhánh so sánh thì đã có thể trình 2,87 điểm.

## Slide 20 · 5 · Chặng ba: khai báo tăng rõ, thực thi đứng yên  —  ~55s  (cộng dồn 15:46)

Chặng ba thưởng thẳng cho ô toạ độ, nên đây là can thiệp duy nhất đặt phần thưởng ngay tại tầng mà phần phân tích lỗi chỉ ra.

Tầng khai báo tăng 2,56 điểm, p bằng 1,3 nhân 10 mũ trừ 8, khoảng tin cậy không chạm 0. Nhưng điểm thực thi chỉ nhích 0,02, khoảng [−0,59 ; +0,64].

Điều đáng nói là dự báo đã ghi trước khi chấm: lấy hệ số chuyển đổi 0,43 đo ở chặng hai thì dự báo +1,10. Giá trị thật là +0,02, tức dự báo bị bác, và hệ số ấy phụ thuộc dạng can thiệp.

Lý do trực tiếp: hai phần ba số bước có ô khai báo đổi mà câu ở đầu ra không đổi một ký tự, trong khi thước chỉ đọc câu.

Câu không bị bẻ thành chuỗi khó đọc: BLEU-4 và tỉ lệ khớp loại thao tác giữ nguyên.

## Slide 21 · 5 · Phân tích lỗi: cơ chế đúng, nhưng bị chặn bởi độ chính xác khai báo  —  ~50s  (cộng dồn 16:36)

Vì sao chỉ 0,94: cắt theo ô khai báo đúng hay sai.

Khai báo đúng (60,6%): hơn 8,83, vượt cả trần câu chuẩn của nhóm. Khai báo sai: thua 11,12.

Hai chiều triệt tiêu nhau. Cách chia là phân tích hậu kiểm.

## Slide 22 · 5 · 63% dư địa còn lại nằm gọn trong một ô duy nhất  —  ~56s  (cộng dồn 17:32)

Ba ràng buộc: ô đúng cả hai đã hết dư địa; 63% dư địa nằm trong ô sai cả tên lẫn toạ độ (3,6 so với 25,8); câu chuẩn vẫn đạt 64,4 ở đó nên giải được.

Bảy bộ định tuyến ở khâu suy luận đều trong nhiễu; định tuyến hoàn hảo chỉ 63,5. Phải sửa ở khâu huấn luyện.

## Slide 23 · 5 · Điểm nghẽn nằm ở tri giác, không ở diễn đạt  —  ~62s  (cộng dồn 18:34)

Đây là mục trả lời câu hỏi vì sao năm can thiệp đều dừng lại.

Tách đường đi từ ảnh tới câu thành hai kênh đo được riêng: kênh tri giác là ô toạ độ mô hình tự viết ra, kênh diễn đạt là điểm mà mô hình định vị trả về sau khi đọc câu. Hai kênh dùng chung một luật phán đúng sai nên so được với nhau.

Nhóm nhìn đúng chiếm 70% số bước nhưng chỉ đóng góp 9% khoảng cách so với câu chuẩn. Nhóm nhìn sai chiếm 30% mà đóng góp 91%.

Con số quan trọng nhất là 45,30: đó là phần thiếu hụt sau khi đã trừ đi độ khó của nhóm bước, vì câu chuẩn cũng giảm 28,64 điểm khi đi từ nhóm này sang nhóm kia.

## Slide 24 · 5 · Sửa được tri giác vẫn phải đi qua tầng sinh câu  —  ~58s  (cộng dồn 19:32)

Sửa được tri giác vẫn chưa đủ, vì phần sửa còn phải đi qua tầng sinh câu.

Chặng ba cho phép đo trực tiếp mức truyền ấy, do đây là can thiệp duy nhất đặt phần thưởng thẳng lên ô toạ độ: nâng kênh tri giác 1,60 điểm chỉ cho 0,045 điểm thực thi.

Bảng chéo cho biết vì sao: sửa được 184 bước với mức lợi 40 điểm mỗi bước, nhưng làm sai 113 bước với mức thiệt 54 điểm. Hai chiều gần như triệt tiêu.

Nếu hội đồng hỏi về con số 0,739 thì nói rõ: đó là tương quan giữa các nhánh, phản ánh việc nhánh mạnh thì mạnh ở cả hai kênh, chứ không đo được điều gì xảy ra khi can thiệp vào riêng một kênh.

## Slide 25 · 5 · Nhánh ứng viên: cơ chế chọn đúng, điểm nghẽn là bỏ cuộc quá mức  —  ~85s  (cộng dồn 20:57)

Nhánh cuối: danh sách tối đa 40 ứng viên của màn hình trong câu nhắc, mô hình chọn một dòng hoặc bỏ cuộc.

Không đạt ngưỡng dừng (57,5 so với 63,6); executability 56,1.

Đưa ra lựa chọn thì 71,4, kém câu chuẩn 4,3; bỏ cuộc sai ở 27,3% bước có đáp án, tái lập qua hai phép đo.

Nguyên nhân gần nhất: hơn nửa mẫu dạy mang nhãn bỏ cuộc (54,8% so với 29,1% trên bước chạm).

Không có nhánh so sánh cùng đầu vào; quan sát, chưa phải nhân quả.

## Slide 26 · 6 · Hạn chế, tự khai kèm số đo  —  ~63s  (cộng dồn 22:00)

Một hạt giống ở mọi nhánh xử lý.

Điều kiện không gây hại không đạt: giảm gần 20 điểm ở bước không chạm, ngưỡng 3.

Lối tắt trong dữ liệu cặp, phát hiện sau huấn luyện.

Nhánh ứng viên không có nhánh so sánh cùng đầu vào.

Dụng cụ: hai mô hình định vị cùng họ với mô hình bị chấm.

## Slide 27 · 6 · Hướng phát triển  —  ~55s  (cộng dồn 22:55)

Hướng 1 là hướng duy nhất chạm vào tầng mà phần phân tích lỗi định vị được: mở phần thị giác của mô hình nền, giữ mọi tham số khác để phép so vẫn một biến, mốc đối chiếu 59,11.

Nói thẳng kỳ vọng: trên năm can thiệp đã đo không cái nào vượt ngưỡng phát hiện, và mức truyền chỉ 0,028, nên xác suất vượt ngưỡng ước lượng khoảng 0,30. Đây là phép thử có căn cứ phân tích lỗi, không phải cải tiến đã hứa trước.

Hướng 2 không chạy: thủ tục ngưỡng chỉ cứu được 8 trên 1.400 bước, dưới ngưỡng đặt trước.

Hướng 3: khoảng 14,6 điểm nằm ở khâu bỏ cuộc, cần một bộ phân loại riêng vì xác suất của chính mô hình không tách được hai nhóm.

## Slide 28 · Kết luận  —  ~50s  (cộng dồn 23:45)

Ba thứ để lại: thước đo kiểm chứng bằng phép đo; tinh chỉnh đáng 11,5 điểm qua sáu cách giải thích thay thế; phần phân tích lỗi chỉ đúng chỗ phải tác động, nối dài bằng nhánh ứng viên.

Điểm cao nhất là 60,07, nhưng không can thiệp nào trong năm can thiệp đã đo vượt được mức chênh nhỏ nhất phát hiện được, và luận văn nói thẳng điều đó.

Hai bài báo đã nộp cuối tháng 8.

## Dự phòng 1 · (bìa)

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 2 · Lý do không dùng BLEU, ROUGE hay vector ngữ nghĩa

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 3 · Chấm lại bằng UI-Venus-Ground-7B

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 4 · Độ bền của luật chấm và tính tất định

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 5 · Độ bền của thước trước cách diễn đạt khác

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 6 · Sàn của thước, và gọi tên so với chỉ vị trí

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 7 · Cấu hình huấn luyện và chi phí máy

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 8 · Trạng thái cuối của các nhánh trong thiết kế

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 9 · Nội suy giữa hai bộ trọng số, và lý do không trích số trên tập chọn

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 10 · Một biến thể đã thiết kế nhưng không dựng được dữ liệu

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 11 · Vùng mù của thước, theo cả hai chiều

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 12 · Phép kiểm cơ học và thiệt hại ở bước không chạm

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 13 · Luật hộp phần tử của chính AndroidControl (Phụ lục D.3)

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 14 · Nhánh ứng viên: dấu hiệu của bỏ cuộc và thủ tục ngưỡng

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 15 · Một trần suy từ lát cắt theo hành vi mô hình thì trôi theo cách chia nhóm

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 16 · Đổi luật chấm thì kết luận thống kê cũng đổi

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

---

**Tổng phần trình bày: 23 phút 45 giây** ở tốc độ 135 từ mỗi phút, chưa tính thời gian chuyển slide và dừng lại chỉ bảng.

Mười bốn slide dự phòng nằm sau slide 28, không thuộc mạch chính. Lúc trình chiếu, gõ số slide rồi Enter để mở.
