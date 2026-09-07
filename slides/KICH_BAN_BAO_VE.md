# Kịch bản trình bày bảo vệ luận văn

Sinh tự động từ `slides/build/build_baove.js`. Sửa lời dẫn trong script rồi chạy lại
`node build_baove.js && python3 make_kichban.py`, đừng sửa tay file này.

---

## Slide 1 · (bìa)  —  ~26s  (cộng dồn 0:26)

Giới thiệu tên, ngành, thầy hướng dẫn, tên đề tài. Thời lượng khoảng 25 phút.

## Slide 2 · Nội dung trình bày  —  ~23s  (cộng dồn 0:49)

Sáu phần. Dành nhiều thời gian nhất cho thước đo (đóng góp đã hoàn tất) và phần chẩn đoán (chỉ ra giới hạn thật của thành phần đề xuất).

## Slide 3 · 1 · Bài toán: đầu ra là câu chữ, không phải toạ độ  —  ~38s  (cộng dồn 1:27)

Tình huống: người dùng không biết bấm gì tiếp trên điện thoại.

Tác tử giao diện: cùng đầu vào nhưng sinh toạ độ cho máy tự bấm.

Đề tài: đầu ra là câu chữ cho người đọc, và câu là thứ duy nhất đem chấm.

Mô hình ba tỉ tham số, chạy tại máy vì ảnh màn hình là dữ liệu riêng tư.

## Slide 4 · 1 · Đổi đầu ra kéo theo hai vấn đề  —  ~47s  (cộng dồn 2:14)

Vấn đề 1, đánh giá: so khớp chuỗi loại nhầm 97,5%; vector ngữ nghĩa AUC 0,336, đo độ gần chủ đề chứ không đo cùng phần tử (inbox/outbox 0,76 cao hơn search/magnifying glass 0,55).

Vấn đề 2, dạng lỗi: đọc tay 40 ca, gần như không bịa, phần lớn là câu mơ hồ.

Kết luận: trọng tâm là tính phân biệt của câu.

## Slide 5 · 1 · Vị trí của luận văn so với các công trình gần nhất  —  ~39s  (cộng dồn 2:53)

Không nhận chữ &quot;đầu tiên&quot;: ý câu phải đủ để bên kia trỏ đúng là của dòng sinh biểu thức quy chiếu từ 2016.

Phần nhận: đưa tính phân biệt vào mục tiêu huấn luyện trong miền giao diện; Widget Captioning vẫn dùng entropy chéo thuần.

## Slide 6 · 1 · Ba đóng góp và trạng thái thật của từng đóng góp  —  ~44s  (cộng dồn 3:37)

Đóng góp 1: thước đo, hoàn tất.

Đóng góp 2: quy trình dựng dữ liệu và kết quả thực nghiệm có nhánh so sánh; nhánh xử lý chỉ một hạt giống vì ngân sách máy, nên không kết luận thành phần có tác dụng hay không.

Đóng góp 3: chẩn đoán từng bước, hoàn tất, giá trị nhất cho người làm tiếp.

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

Chẩn đoán từ nhánh khai báo: cơ chế đúng, điểm nghẽn là độ chính xác ô khai báo.

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

## Slide 16 · 5 · Kết quả chính trên 4.463 bước chạm  —  ~41s  (cộng dồn 12:04)

Trần 75,7. Base 47,6. S1 59,1 và 59,6 ở hai hạt giống.

Bốn nhánh dưới vạch chỉ một hạt giống.

Ba khoảng tin cậy rời nhau: thước phân giải được ba mức, còn khoảng trống cho can thiệp.

## Slide 17 · 5 · So sánh ghép cặp và các cách giải thích thay thế  —  ~45s  (cộng dồn 12:49)

Tinh chỉnh đáng 11,5 điểm; nhiễu hai hạt giống 0,52; tín hiệu gấp 22 lần nhiễu.

Bỏ một phần tư số bước chép nguyên câu chuẩn, vẫn còn 8,4.

Sáu cách giải thích thay thế; ô đỏ chỉ loại được sau khi đổi mô hình định vị thứ hai.

## Slide 18 · 5 · Nhánh khai báo: một hạt giống, không kết luận được  —  ~60s  (cộng dồn 13:49)

S2 thấp hơn nhánh nền 1,93; p nhỏ nhưng dưới MDE nên không kết luận được, không phải kết quả âm; hạt thứ hai không chạy.

Chẩn đoán: 7,3% số bước chiếm một phần ba chênh lệch, là nhóm đoán sai loại thao tác.

Mô hình gốc gọi đúng loại thao tác nhiều hơn cả hai bản đã huấn luyện: chi phí của tinh chỉnh, do tập dạy chỉ gắn khai báo cho bước chạm.

## Slide 19 · 5 · Chặng hai: điểm cao nhất, nhưng phần lớn không thuộc mục tiêu ưu tiên  —  ~57s  (cộng dồn 14:46)

60,0 là điểm cao nhất, nhưng có nhánh so sánh để tách công.

S2 → CE2: +2,24 do huấn luyện thêm; CE2 → MIN-DESC: +0,63 riêng mục tiêu ưu tiên. 78% thuộc nhánh so sánh; ở tầng khai báo 87%.

0,63 trên nhiễu thước nhưng dưới MDE. Không có nhánh so sánh thì đã có thể trình 2,87 điểm.

## Slide 20 · 5 · Chẩn đoán: cơ chế đúng, nhưng bị chặn bởi độ chính xác khai báo  —  ~50s  (cộng dồn 15:36)

Vì sao chỉ 0,94: cắt theo ô khai báo đúng hay sai.

Khai báo đúng (60,6%): hơn 8,83, vượt cả trần câu chuẩn của nhóm. Khai báo sai: thua 11,12.

Hai chiều triệt tiêu nhau. Cách chia là phân tích hậu kiểm.

## Slide 21 · 5 · 63% dư địa còn lại nằm gọn trong một ô duy nhất  —  ~56s  (cộng dồn 16:32)

Ba ràng buộc: ô đúng cả hai đã hết dư địa; 63% dư địa nằm trong ô sai cả tên lẫn toạ độ (3,6 so với 25,8); câu chuẩn vẫn đạt 64,4 ở đó nên giải được.

Bảy bộ định tuyến ở khâu suy luận đều trong nhiễu; định tuyến hoàn hảo chỉ 63,5. Phải sửa ở khâu huấn luyện.

## Slide 22 · 5 · Nhánh ứng viên: cơ chế chọn đúng, điểm nghẽn là bỏ cuộc quá mức  —  ~85s  (cộng dồn 17:57)

Nhánh cuối: danh sách tối đa 40 ứng viên của màn hình trong câu nhắc, mô hình chọn một dòng hoặc bỏ cuộc.

Không đạt ngưỡng dừng (57,5 so với 63,6); executability 56,1.

Đưa ra lựa chọn thì 71,4, kém câu chuẩn 4,3; bỏ cuộc sai ở 27,3% bước có đáp án, tái lập qua hai phép đo.

Nguyên nhân gần nhất: hơn nửa mẫu dạy mang nhãn bỏ cuộc (54,8% so với 29,1% trên bước chạm).

Không có nhánh so sánh cùng đầu vào; quan sát, chưa phải nhân quả.

## Slide 23 · 6 · Hạn chế, tự khai kèm số đo  —  ~63s  (cộng dồn 19:00)

Một hạt giống ở mọi nhánh xử lý.

Điều kiện không gây hại không đạt: giảm gần 20 điểm ở bước không chạm, ngưỡng 3.

Lối tắt trong dữ liệu cặp, phát hiện sau huấn luyện.

Nhánh ứng viên không có nhánh so sánh cùng đầu vào.

Dụng cụ: hai mô hình định vị cùng họ với mô hình bị chấm.

## Slide 24 · 6 · Hướng phát triển  —  ~52s  (cộng dồn 19:52)

Hướng 1: huấn luyện lại trên 41 nghìn bước chạm, đưa nhãn bỏ cuộc từ 55% về 29%; đúng một biến đổi.

Hướng 2: thủ tục chọn ngưỡng bỏ cuộc, đang chạy; quyết định hướng 1 có chạy hay không.

Hướng 3: nhánh so sánh cùng đầu vào, rồi hạt giống thứ hai.

## Slide 25 · Kết luận  —  ~48s  (cộng dồn 20:40)

Ba thứ để lại: thước đo kiểm chứng bằng phép đo; tinh chỉnh đáng 11,5 điểm qua sáu cách giải thích thay thế; chẩn đoán chỉ đúng chỗ phải tác động, nối dài bằng nhánh ứng viên.

Thành phần đề xuất chưa kết luận được ở một hạt giống.

Hai bài báo đã nộp cuối tháng 8.

## Slide 26 · (bìa)  —  ~0s  (cộng dồn 20:40)

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 1 · Lý do không dùng BLEU, ROUGE hay vector ngữ nghĩa

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 2 · Chấm lại bằng UI-Venus-Ground-7B

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 3 · Độ bền của luật chấm và tính tất định

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 4 · Độ bền của thước trước cách diễn đạt khác

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 5 · Sàn của thước, và gọi tên so với chỉ vị trí

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 6 · Cấu hình huấn luyện và chi phí máy

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 7 · Trạng thái cuối của các nhánh trong thiết kế

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 8 · Một biến thể đã thiết kế nhưng không dựng được dữ liệu

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 9 · Vùng mù của thước, theo cả hai chiều

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 10 · Cổng cơ học và thiệt hại ở bước không chạm

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 11 · Luật hộp phần tử của chính AndroidControl (Phụ lục D.3)

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

## Dự phòng 12 · Nhánh ứng viên: dấu hiệu của bỏ cuộc và thủ tục ngưỡng

_(không có lời dẫn: slide chỉ mở khi hội đồng hỏi tới)_

---

**Tổng phần trình bày: 20 phút 40 giây** ở tốc độ 135 từ mỗi phút, chưa tính thời gian chuyển slide và dừng lại chỉ bảng.

Mười hai slide dự phòng nằm sau slide 26, không thuộc mạch chính. Lúc trình chiếu, gõ số slide rồi Enter để mở.
