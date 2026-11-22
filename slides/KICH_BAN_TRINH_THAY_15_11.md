# Kịch bản trình thầy (11/2026)

Đi kèm `slides/LUAN_VAN_SLIDE_TRINH_THAY_15_11.pptx`. Sinh tự động từ ghi chú trong `slides/build/build_trinh_thay_15_11.js`; sửa lời ở script, không sửa tay file này.

## Slide 1
- Báo cáo hai phần.
- Phần một nhắc lại bài toán và cách chấm bằng executability, vì mọi phép so phía sau đều đọc bằng con số này.
- Phần hai là việc thầy giao ngày 1/11: so GRPO với các thuật toán RL khác, so SPICE với các độ đo thưởng khác, và giải thích vì sao.

## Slide 2
- Ví dụ đầu ra: "Tap Not now".
- Câu viết cho người đọc làm theo; mô hình không tự bấm thay người dùng.

## Slide 3
- Màn hình có mười nút thì "Tap the button" đúng ngữ pháp mà không dùng được.
- Vì vậy cần một cách chấm kiểm được câu có giúp chọn đúng phần tử hay không. Đó là executability ở phần sau.

## Slide 4
- Bộ gốc dùng câu hướng dẫn làm đầu vào để dự đoán thao tác; đề tài đi chiều ngược lại, câu là thứ cần sinh.
- Mỗi bước có toạ độ người dùng đã chạm thật, và executability chấm dựa trên toạ độ này.
- Mọi số exec hôm nay tính trên 4.463 bước chạm của tập kiểm tra.

## Slide 5
- Hình dung: đưa câu cho một người lạ không biết đáp án, chỉ nhìn màn hình và đọc câu, rồi xem họ bấm vào đâu. Bấm trúng chỗ người dùng thật đã bấm thì câu dùng được.
- Người lạ ở đây là UGround, một mô hình định vị giao diện có sẵn: nhận ảnh và câu, trả về một điểm trên màn hình.
- UGround không được huấn luyện cùng mô hình của đề tài và không biết đáp án.
- BLEU, SPICE so chữ với câu chuẩn; executability xem câu có đưa người đọc tới đúng chỗ không.

## Slide 6
- Màn hình thật trong tập kiểm tra. Người dùng chạm ô Birthday (vòng vàng).
- S1 viết "Click on the Birthday option"; UGround chạm đúng ô Birthday (vòng xanh), bước này đạt.
- Mô hình gốc viết "Click on the Gender section to change it to Male": câu dài, đúng ngữ pháp, nhưng gọi sai ô. UGround chạm ô Gender (dấu X đỏ), bước này không đạt.
- Hai ô chỉ cách nhau một hàng. Nếu chỉ đo khoảng cách, câu sai này vẫn có thể được tính đúng; slide sau nói cách loại.

## Slide 7
- Ba điều kiện phải đạt cùng lúc.
- Một: đúng loại thao tác. Bước cần chạm mà câu bảo vuốt lên hay quay lại thì sai ngay.
- Hai: điểm chạm lệch không quá 14% chiều ngang và 14% chiều dọc màn hình so với điểm thật. Ngưỡng này lấy từ bộ AndroidInTheWild.
- Ba: điểm chạm gần điểm thật hơn mọi phần tử bấm được khác, tức nằm trong ô Voronoi (vùng tô vàng ở ví dụ trước). Điều kiện này loại câu gọi nhầm nút bên cạnh.

## Slide 8
- Phép thử: cố ý dịch điểm chạm, hoặc sang phần tử bên cạnh, hoặc lệch nhẹ trong cùng phần tử.
- Chỉ dùng dung sai 14% thì 84,3% ca dịch sang nút bên cạnh vẫn được chấp nhận, gần như không phân biệt nút đúng với nút kế bên.
- Thêm điều kiện ô Voronoi thì chỉ còn 2,8%, trong khi ca lệch nhẹ trong cùng phần tử vẫn giữ 99,7%.

## Slide 9
- Trần không phải 100: đưa câu chuẩn cho UGround cũng chỉ đạt 75,7%, vì UGround đôi khi chạm lệch. Đây là giới hạn của dụng cụ đo.
- Sàn không phải 0: "Tap the button" cho mọi bước vẫn đạt 12%. Câu thật nhưng lấy từ màn hình khác chỉ đạt 6,1%, thấp hơn cả sàn, nghĩa là UGround đọc nội dung câu chứ không chấm văn phong.
- Mô hình gốc 47,6, S1 59,1, GRPO-SPICE 60,7, SA-SPICE-v3 61,2. Sau tinh chỉnh các mức chênh chỉ 1 đến 2 điểm nên phép so nào cũng kèm khoảng tin cậy.

## Slide 10
- Bỏ tên phần tử khỏi câu chuẩn thì mất 28,5 điểm trên các bước bị tác động, bỏ mô tả vị trí chỉ mất 3,5: thước thưởng việc gọi đúng tên phần tử.
- Đổi người làm theo sang ba mô hình định vị khác, phương pháp vẫn cao hơn S1. Phi-Ground và Phi-4 không thuộc họ Qwen.
- Chấm lại cùng câu cho đúng cùng kết quả.

## Slide 11
- Xuất phát từ S1: Qwen2.5-VL-3B đã tinh chỉnh có giám sát.
- Thành phần một: học tăng cường bằng GRPO, thưởng SPICE.
- Thành phần hai: ACE tra bốn câu ví dụ giống nhất trong tập huấn luyện và chỉ thay câu khi đạt hai điều kiện.
- UGround không nằm trong phần thưởng, nên thước chấm độc lập với mục tiêu huấn luyện.

## Slide 12
- Mỗi mẫu, mô hình viết tám câu; mỗi câu được chấm SPICE so với câu chuẩn, trừ phạt độ dài.
- Câu có điểm cao hơn trung bình nhóm thì được tăng xác suất, thấp hơn thì bị giảm. Mốc so là trung bình của chính nhóm, nên không cần mô hình giá trị riêng.
- Phạt KL giữ mô hình không đi quá xa S1.
- SPICE chấm theo đối tượng và quan hệ, hợp với việc gọi đúng phần tử. Dùng độ đo làm phần thưởng đã có từ SCST và SPIDEr.

## Slide 13
- Nhiều tác vụ lặp lại với khác biệt nhỏ, nên câu chuẩn của một bước cũ đôi khi dùng lại được nguyên văn.
- ACE cho bộ sinh xem câu của bốn bước giống nhất, và chỉ thay câu ban đầu khi câu mới trùng nguyên văn một câu ví dụ và cùng loại thao tác.
- Phần lớn các bước giữ câu ban đầu.

## Slide 14
- GRPO-SPICE đạt 60,65, hơn S1 1,55 điểm; khoảng tin cậy 95% từ 0,80 đến 2,33, không chứa 0.
- Hai tiêu chí vị trí khác (hộp phần tử của AndroidControl, AitW đầy đủ) cũng tăng cỡ đó.
- Thêm ACE thì exec giữ nguyên, các độ đo văn bản tăng thêm.

## Slide 15
- Chấm lại cùng các câu bằng ba mô hình định vị khác.
- Mức tuyệt đối khác nhau vì mỗi mô hình định vị mạnh yếu khác nhau.
- GRPO-SPICE luôn cao hơn S1 và cả bốn khoảng tin cậy đều trên 0.

## Slide 16
- Hai lưới, mỗi lưới chỉ đổi một yếu tố.
- Lưới 1 giữ thưởng SPICE, đổi thuật toán. SCST là mốc kinh điển của bài toán chú thích ảnh.
- Lưới 2 giữ GRPO, đổi phần thưởng.
- Ba mốc đọc kèm: SFT tiếp tách công của RL khỏi công của việc học thêm; SPICE ghép ngẫu nhiên là thưởng không mang thông tin; GRPO chạy lại cho biết hai lần chạy cùng cấu hình lệch nhau bao nhiêu.

## Slide 17
- Mỗi chấm là mức chênh exec so với S1, vạch ngang là khoảng tin cậy 95%. Chấm bên phải vạch 0 là hơn S1.
- Mọi thuật toán hơn S1 từ 0,3 đến 1,6 điểm; sáu trong tám lượt có khoảng tin cậy nằm hẳn trên 0.
- Các khoảng chồng lên nhau nhiều nên chưa kết luận được thuật toán nào hơn hẳn. GRPO và SCST nhỉnh nhất, RLOO thấp nhất.
- Chạy lại GRPO đúng cấu hình cũ chỉ được 0,63, lệch lượt chính 0,92: dao động giữa hai lần chạy đã cỡ khoảng cách giữa các thuật toán.
- Dr.GRPO (bỏ chia độ lệch chuẩn và bỏ chuẩn hoá theo độ dài) đạt 60,00: thấp hơn GRPO lượt chính 0,65 [0,19; 1,12], p = 0,009, ngang GRPO chạy lại cùng mã (+0,27, chưa có ý nghĩa). Bỏ hai phép chuẩn hoá không giúp gì ở bài này.
- SFT tiếp, không có RL, cũng hơn S1 1,05. Một phần mức tăng đến từ việc học thêm trên các câu nhắc này.

## Slide 18
- Hàng quan trọng nhất là hàng cuối: ghép điểm SPICE ngẫu nhiên giữa các câu thì kết quả đúng bằng S1, chênh 0,00. Mức tăng đến từ nội dung phần thưởng, không phải từ việc chạy vòng lặp RL.
- SPICE, ROUGE-L, METEOR, CIDEr-D có khoảng tin cậy chồng nhau, chưa tách được bên nào hơn. Không viết "SPICE tốt nhất".
- SA-SPICE-v3 cao nhất, +2,11 so với S1, nhưng xuất phát từ SFT tiếp. So công bằng với SFT tiếp thì hơn 1,05, có ý nghĩa; slide 21 nói kỹ.
- SPICE thuần từ cùng điểm xuất phát: +1,77 so với S1, +0,72 so với SFT tiếp, cũng có ý nghĩa.

## Dự phòng
- Slide chờ số, đang ẩn. Điền exec và Δ so với S1 khi có số test, rồi chép vào biểu đồ slide 17.

## Dự phòng
- Slide chờ số, đang ẩn. Điền exec và Δ so với S1 khi có số test, rồi chép vào biểu đồ slide 18 và bảng slide 20.
- Lượt chrF có KL lúc train cao hơn hẳn các lượt khác, nên đọc kèm bước không chạm.

## Slide 19
- Tách số bước sửa được so với S1 làm hai phần: bước S1 sai loại thao tác mà lượt mới sửa đúng, và bước đúng loại thao tác mà lượt mới chọn đúng phần tử hơn.
- Thưởng thật đều sửa được loại thao tác; thưởng ngẫu nhiên gần như không sửa gì.
- ROUGE-L sửa loại thao tác nhiều nhất (48 bước) nhưng phần tử chỉ 20. SPICE sửa phần tử 41 bước, nhiều nhất. Hai phần bù nhau nên tổng exec gần bằng.
- Mới là dấu hiệu: so từng cặp không còn ý nghĩa sau hiệu chỉnh Holm, và mới một seed. Không viết "SPICE giúp định vị tốt hơn".

## Slide 20
- Ô tô màu là cao nhất mỗi cột. Không phần thưởng nào thắng mọi cột, các chênh lệch đều nhỏ.
- SPICE thuần từ SFT tiếp cao nhất ở ROUGE-L, CIDEr-D và SPICE; SA-SPICE-v3 ở METEOR và chrF; GRPO chạy lại ở BLEU-4.
- Dr.GRPO ngang GRPO lượt chính ở mọi cột.
- Điểm lạ cần khai: thưởng bằng CIDEr-D mà lại thấp ở chính CIDEr-D. Đã kiểm cách tính IDF và cách tách từ, chưa giải thích được.

## Slide 21
- Với câu ngắn như "Scroll down" hay "Go back", SPICE cho 0 điểm kể cả khi câu đúng nguyên văn; chrF đỡ chỗ này. Cộng thêm điểm khi câu đúng loại thao tác.
- 61,21 là exec cao nhất trong mọi lượt đã huấn luyện, hơn điểm xuất phát 1,05 và có ý nghĩa.
- Hơn GRPO-SPICE 0,56 nhưng p = 0,069, nên chưa viết là hơn.
- Điểm yếu: bước cuộn tăng, bước quay lại giảm từ 71,1 xuống 58,5.
- SPICE thuần (cùng điểm xuất phát, bỏ chrF và điểm loại thao tác) đạt 60,88, chênh SA-SPICE-v3 0,37, p = 0,46. Ở độ đo văn bản SPICE thuần còn nhỉnh hơn, trừ chrF. Bước quay lại của nó cũng giảm, xuống 56,3.
- Vậy phần trộn thưởng chưa mua được gì rõ; vấn đề bước quay lại cần chữa ngoài phần thưởng.

## Slide 22
- RL có giúp, và giúp nhờ nội dung phần thưởng.
- Giữa các thuật toán chưa tách được bên nào tốt nhất. GRPO và SCST nhỉnh nhất, nhưng dao động giữa hai lần chạy cỡ khoảng cách đó.
- Giữa các phần thưởng, SPICE và ROUGE-L ngang nhau ở exec nhưng đi hai đường khác nhau.
- Giữ GRPO-SPICE vì nó thuộc nhóm dẫn đầu ở cả hai lưới, có tiền lệ rõ, và phần thưởng không dùng mô hình định vị.

## Slide 23
- Năm lượt đã train xong. Bản chạy thử test 20 bước đạt cả năm lượt: nạp đúng adapter, câu sinh khác nhau giữa các lượt. Test đầy đủ chạy khi hạn mức máy làm mới sau 28/11.
- DPO trực tuyến là phương pháp học theo cặp ưu tiên phổ biến nhất còn thiếu trong lưới thuật toán.
- Kết quả từng lượt sẽ điền vào hai slide chờ số đang ẩn sau slide 18.
- Xin ý kiến thầy về thứ tự ưu tiên các việc này.

## Slide 24
- Executability chấm câu bằng việc làm theo, và đã kiểm là nó phản ứng đúng với nội dung câu.
- RL giúp nhờ nội dung phần thưởng; các thuật toán và độ đo thưởng phổ biến cho mức tăng gần nhau.
- GRPO-SPICE thuộc nhóm dẫn đầu ở cả hai lưới. Mọi kết quả hiện là một seed, đang chạy thêm để chắc hơn.

## Dự phòng
- Bảng đủ các chỉ số cho bốn cấu hình, mở khi được hỏi chi tiết.

## Dự phòng
- Tác vụ chưa thấy khi huấn luyện: mức tăng lớn hơn, +4,58.
- Các bước trước do mô hình tự viết: mức tăng giữ nguyên.
- AitZ, không huấn luyện thêm: không còn khác S1.
- Seed 202 thấp hơn seed 101 0,72 điểm nhưng vẫn hơn S1.

## Dự phòng
- Định nghĩa hình thức của executability, mở khi cần.
