# Kịch bản thuyết trình luận văn (18/11/2026)

Đi kèm `slides/LUAN_VAN_SLIDE_THUYET_TRINH.pptx`. Sinh tự động từ ghi chú trong `slides/build/build_thuyet_trinh.js`; sửa lời ở script, không sửa tay file này.

## Slide 1
- Chào hội đồng, giới thiệu đề tài, học viên, giáo viên hướng dẫn.

## Slide 2
- Sáu phần. Độ đo executability trình bày ngay trước kết quả, vì mọi con số kết quả đều đọc bằng nó.

## Slide 3
- Mô hình nhìn màn hình, biết mục tiêu và các bước đã làm, viết câu cho bước kế tiếp.
- Ảnh: một bước thật trong tập kiểm tra, người dùng chạm nút Bin.

## Slide 4
- Câu không chỉ ra phần tử nào vẫn có thể được BLEU/SPICE cho điểm khá.
- Từ đây dẫn sang executability.

## Slide 5
- Bộ gốc dùng câu hướng dẫn làm đầu vào để dự đoán thao tác; đề tài dùng câu làm đích sinh.
- Mọi số executability tính trên 4.463 bước chạm.
- Bước không chạm báo riêng vì không có điểm chạm để chấm.

## Slide 6
- S1 là nền chung của mọi nhánh, huấn luyện bằng QLoRA.
- GRPO-SPICE sinh câu ban đầu; ACE chỉ thay câu ở một phần nhỏ số bước.

## Slide 7
- BLEU đếm chữ trùng; SPICE so các đối tượng, thuộc tính và quan hệ mà câu nhắc tới.
- Điểm yếu đã đo trên câu chuẩn của tập kiểm định: đổi "Click" thành "Swipe up" SPICE vẫn cho khoảng 0,92, các độ đo khác chỉ 0,45 đến 0,79.
- Hai điểm yếu này là lý do thử thêm phần thưởng SA-SPICE-v3 ở phần so sánh.

## Slide 8
- Ví dụ thật từ tập kiểm tra.
- Trong GRPO, tám câu của cùng một bước được chấm như vậy; câu gọi đúng "Not now" có điểm cao hơn trung bình nhóm nên được khuyến khích.

## Slide 9
- GRPO không cần mô hình giá trị: mốc so là trung bình của chính nhóm tám câu.
- Không nhận điểm mới ở thuật toán hay ở việc chọn SPICE; điểm mới là áp vào bài toán này và đánh giá bằng executability.

## Slide 10
- ACE: Action-Consistent Exemplar copying.
- Quy tắc chọn trên tập kiểm định, áp lên tập kiểm tra một lần.

## Slide 11
- BLEU/SPICE so chữ với câu chuẩn; executability xem người làm theo câu có bấm đúng chỗ không.
- UGround là mô hình định vị giao diện có sẵn: nhận ảnh và câu, trả về một điểm.

## Slide 12
- Hai ô Birthday và Gender chỉ cách nhau một hàng: chỉ đo khoảng cách thì câu sai vẫn có thể được tính đúng.

## Slide 13
- Trần 75,7 là giới hạn của dụng cụ, không phải của ngôn ngữ.
- Sau tinh chỉnh, các mức chênh chỉ 1 đến 2 điểm nên luôn kèm khoảng tin cậy.

## Slide 14
- Mức số tuyệt đối khác nhau theo bộ định vị, nhưng phương pháp luôn cao hơn S1.
- Độ đo tất định: cùng câu, cùng ảnh cho cùng toạ độ.

## Slide 15
- D.3: tiêu chí gốc của AndroidControl, điểm chạm nằm trong hộp phần tử đúng.
- AitW đầy đủ: khoảng cách 14% hoặc cùng nằm trong hộp nới 1,4 lần.
- Lượt mới 17/11: cùng thưởng SPICE nhưng xuất phát từ SFT tiếp và tập câu nhắc mới, nên so công bằng là so với SFT tiếp (+0,72, có ý nghĩa).
- Lượt mới so với GRPO-SPICE từ S1: +0,22 [−0,35; +0,81], chưa tách được.

## Slide 16
- Nhánh ghép ngẫu nhiên loại khả năng mức tăng chỉ do chạy thêm vòng lặp học tăng cường.
- Trên tác vụ mới mức tăng còn lớn hơn.
- AitZ: lợi ích riêng của SPICE phụ thuộc phân phối câu chuẩn.

## Slide 17
- Hai phép so, mỗi phép chỉ đổi một yếu tố.
- Mốc "học thêm không RL" để tách công của học tăng cường với công của việc học thêm.

## Slide 18
- Đọc: cột số đầu là executability, số sau là hơn S1 bao nhiêu điểm.
- GRPO ở đây xuất phát từ mô hình học thêm, nên phần hơn S1 gồm cả công học thêm (+1,05); so với chính điểm xuất phát, GRPO hơn +0,72 [+0,24; +1,20].
- SCST hơn S1 +1,43 [+0,79; +2,10]; RLOO +0,34, khoảng tin cậy chứa 0.

## Slide 19
- Executability, D.3 và AitW là ba cách xác định câu có dẫn tới đúng phần tử; đúng loại thao tác chỉ xét động từ.
- PPO chạy 1.000 bước cập nhật để đi hết cùng 1.000 câu nhắc.
- Dr.GRPO đầy đủ (22/11): executability 60,00, thấp hơn GRPO-SPICE từ S1 0,65 điểm; chưa chấm D.3, AitW và độ đo văn bản nên chưa đưa vào bảng. A2C mới thăm dò.

## Slide 20
- Các độ đo này so câu sinh với câu chuẩn của người chú thích.
- Thứ hạng theo độ đo văn bản không trùng hẳn thứ hạng theo executability.

## Slide 21
- Hàng ghép ngẫu nhiên là phép kiểm quan trọng nhất: cùng vòng lặp GRPO, chỉ khác là phần thưởng không mang thông tin.
- SPICE, ROUGE-L, METEOR, CIDEr-D có khoảng tin cậy chồng nhau; không viết SPICE là tốt nhất.

## Slide 22
- SA-SPICE-v3 và SPICE cùng xuất phát nên so trực tiếp được: chênh 0,34 điểm, chưa có ý nghĩa.

## Slide 23
- Thưởng bằng CIDEr-D lại thấp ở chính CIDEr-D (424,52); đã kiểm cách tính IDF và tách từ, chưa giải thích được.

## Slide 24
- SA-SPICE-v3 hơn mô hình học thêm không RL 1,05 điểm [+0,46; +1,65]; SPICE hơn 0,72 [+0,24; +1,20].
- Bước quay lại giảm nên phải khai; hướng chữa nằm ngoài phần thưởng.

## Slide 25
- Khai thẳng các hạn chế kèm số đo.
- Hướng tiếp: thêm hạt giống, chữa bước không chạm; DPO trực tuyến đã huấn luyện xong, đang chờ chấm.

## Slide 26
- Ba ý chính. Mời hội đồng đặt câu hỏi.
