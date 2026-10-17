# Kịch bản báo cáo trước thầy: xin bảo vệ đợt này (14/10/2026)

Đi kèm `slides/LUAN_VAN_SLIDE_XIN_BAO_VE.pptx` (6 slide). Sinh bởi `slides/build/build_xin_bao_ve.js` từ phần ghi chú của từng slide; sửa lời dẫn ở script, không sửa tay file này.

## Slide 1
(20 giây)
Em chào thầy. Hôm nay em báo cáo nội dung luận văn đã hoàn chỉnh: bài toán, thước đo, phương pháp đề xuất và kết quả. Phần trình bày khoảng mười lăm phút. Cuối buổi em xin ý kiến thầy về việc bảo vệ ở đợt này.

## Slide 2
(1 phút 15)
Câu sinh ra được đưa cho UGround, một mô hình định vị không biết đáp án. UGround trả về một điểm. Bước được tính đúng khi ba điều kiện cùng đạt: câu gọi đúng loại thao tác; điểm nằm trong dung sai 0,14 quanh điểm người dùng đã chạm; và điểm rơi vào ô Voronoi của điểm chạm, tức gần điểm chạm hơn mọi phần tử bấm được khác.
Điều kiện thứ ba để loại các câu chỉ sai nút bên cạnh: với những câu đó, luật dung sai đơn thuần vẫn cho điểm 84,3% số ca, còn Voronoi chỉ còn 2,8%.
Ví dụ bên phải là màn hình thật: câu của S1 dẫn tới đúng ô Birthday, câu của mô hình gốc dẫn sang ô Gender.

## Slide 3
(1 phút 15)
Đây là sơ đồ tổng quan. Điểm xuất phát là S1. Phương pháp cải thiện câu của S1 bằng hai cách bổ sung cho nhau.
Thành phần một cho S1 học tiếp bằng học tăng cường, thưởng là điểm SPICE. Kết quả là một mô hình viết một câu nháp cho mỗi bước.
Thành phần hai tên là ACE. Tập huấn luyện có hơn sáu mươi nghìn câu chuẩn, nhiều bước mới rất giống một bước cũ. ACE tìm bốn câu chuẩn của các bước giống nhất, cho một bộ sinh xem, rồi chỉ thay câu nháp bằng câu của bộ sinh khi câu ấy chép nguyên văn một câu ví dụ và cùng loại thao tác với câu nháp. Ở phần lớn các bước câu nháp vẫn được giữ.
Hai điều cần nhớ: không thành phần nào thấy câu chuẩn của bước đang xét, và mô hình định vị dùng chấm không tham gia vào huấn luyện hay chọn câu.

## Slide 4
(1 phút)
Học có giám sát dạy mô hình chép lại câu chuẩn, nhưng không cho biết trong những câu nó có thể viết, câu nào tốt hơn. Học tăng cường bổ sung điều đó, theo cách đã dùng trong sinh chú thích ảnh với CIDEr và SPIDEr.
Bốn bước: một, với mỗi bước mô hình viết tám câu khác nhau. Hai, mỗi câu được chấm SPICE so với câu chuẩn, trừ một khoản nhỏ nếu dài hơn câu chuẩn quá ba từ để mô hình không kể thêm chi tiết thừa. Ba, so điểm từng câu với trung bình của cả nhóm tám câu: cao hơn thì được khuyến khích. Bốn, cập nhật mô hình, có thêm một số hạng phạt độ lệch KL để mô hình không đi quá xa S1.
SPICE chấm theo đối tượng, thuộc tính, quan hệ nên hai câu cùng nói tới một nút vẫn được điểm cao dù khác từ. Ví dụ bên phải: S1 gọi nút Allow, mô hình học với thưởng SPICE gọi đúng nút Not Now.
Mô hình định vị dùng để chấm không có trong phần thưởng, nên thước vẫn độc lập với mục tiêu huấn luyện. Tiền lệ là SCST và SPIDEr trong chú thích ảnh; điểm em nhận là hẹp: áp dụng và đo cho bài toán này, không nhận mới ở thuật toán.

## Slide 5
(1 phút)
Nhiều tác vụ trong bộ dữ liệu lặp lại với thay đổi nhỏ, ví dụ cùng một việc trên hai ứng dụng nhắn tin. Vì vậy câu chuẩn của một bước cũ đôi khi dùng được nguyên văn cho bước mới. Nhưng lúc nào cũng chép thì sai nhiều hơn đúng, nên ACE phải quyết định khi nào chép.
Với mỗi bước, ACE tìm bốn bước giống nhất trong tập huấn luyện, chỉ so bằng văn bản. Câu chuẩn của bốn bước ấy là bốn câu ví dụ. Bộ sinh nhận thêm khối ví dụ này. Luật đồng thuận chỉ thay câu nháp khi câu của bộ sinh chép nguyên văn một câu ví dụ và cùng loại thao tác với câu nháp.
Ví dụ một: nháp là "Click on the first image", bộ sinh chép "Select the second photo", cùng là chạm nên nhận, và câu này trùng câu chuẩn. Ví dụ hai: bộ sinh chép "Swipe up" nhưng nháp là thao tác chạm, nên giữ nháp, và nháp mới đúng.

## Slide 6
(1 phút)
Đây là các thước em dùng để đặt phương pháp cạnh S1. Nhóm trên là ba thước theo vị trí, đều do mô hình định vị chấm: executability, luật hộp phần tử gốc của AndroidControl và luật khoảng cách của AitW. Nhóm dưới là bảy thước so câu chữ với câu chuẩn mà các bài chú thích giao diện như Widget Captioning và Screen2Words vẫn dùng.
Trong ba cột này phương pháp đề xuất cao nhất ở mọi hàng. Điểm đáng nói: phần thưởng chỉ là SPICE nhưng mức tăng không dừng ở SPICE, và các thước vị trí dùng mô hình định vị không hề có trong phần thưởng cũng tăng.
Em xin khai thêm: với các mô hình chênh nhau dưới hai điểm executability, nhóm thước so câu có thể xếp thứ tự khác, nên phép so giữa các mô hình em vẫn đọc trên executability.

