# Kịch bản buổi báo cáo tiến độ với thầy (tháng 10/2026)

Đi kèm `slides/LUAN_VAN_SLIDE.pptx` (24 slide chính, 2 slide dự phòng; dựng bằng
`slides/build/build_slide.js`). Slide chỉ trình bày nội dung luận văn. Lời đề nghị xin tốt nghiệp
nằm ở **Phần 3** của file này, nói sau khi trình xong slide.

Mọi con số dưới đây lấy từ `thesis/chapters/` bản 5/10 (153 trang) và khớp với slide.

---

## Phần 1. Chuẩn bị trước buổi gặp

**Mục tiêu buổi gặp, nói một lần ở đầu và một lần ở cuối:** thầy đồng ý rằng nội dung luận văn đã
đủ, góp ý bản thảo, và cho em hoàn tất thủ tục kịp hạn **2/11**.

Mang theo:
- bản PDF luận văn `thesis/main.pdf` (153 trang), in hoặc gửi thầy trước một hai ngày nếu được;
- deck `LUAN_VAN_SLIDE.pptx`;
- danh sách ba bài báo (slide 24) để thầy thấy phần đã công bố.

Thời lượng phần trình bày: khoảng **19 phút**, chừa thời gian cho thầy hỏi.

---

## Phần 2. Lời nói theo từng slide

### Slide 1. Bìa (20 giây)
Em chào thầy. Hôm nay em xin báo cáo tình trạng luận văn. Bản thảo đã đủ tám chương, 153 trang.
Em sẽ trình bày nhanh nội dung chính khoảng hai mươi phút, sau đó xin thầy cho ý kiến về việc hoàn
tất để kịp hạn ngày 2/11.

### Slide 2. Nội dung (15 giây)
Phần trình bày đi theo đúng thứ tự của luận văn: bài toán, thước đo, dữ liệu và mô hình nền, các
hướng đã thử, phương pháp đề xuất, rồi đóng góp và hạn chế.

### Slide 3. Bài toán (1 phút)
Các hệ thống tác tử giao diện hiện nay nhận ảnh màn hình và mục tiêu, rồi sinh toạ độ để phần mềm tự
bấm. Đề tài giữ nguyên đầu vào nhưng đổi người nhận đầu ra: mô hình viết một câu tiếng Anh cho người
dùng, nói rõ cần chạm vào phần tử nào.

Hai khái niệm trong tên đề tài ứng với hai phần của đầu vào. Trường hợp sử dụng là mục tiêu người
dùng cùng các bước đã làm. Giao diện người dùng là ảnh màn hình và chữ đọc được trên đó.

Điểm khác với bài gốc AndroidControl: ở bài gốc, câu hướng dẫn từng bước là đầu vào của tác tử. Ở đây
câu đó là thứ mô hình phải sinh ra.

### Slide 4. Khó khăn khi chấm (1 phút)
Khó nhất là chấm câu. Cùng một nút có nhiều cách gọi đều đúng, mà mỗi bước trong bộ dữ liệu chỉ có
một câu chuẩn. BLEU hay SPICE đo độ trùng từ, nên phạt cách gọi khác dù đúng phần tử, và có thể cho
điểm cao một câu gọi nhầm nút bên cạnh. Zhao và cộng sự ở EACL 2021 cũng kết luận các thước này không
hiệu quả cho câu chỉ đường gắn với môi trường.

Vì thế em đổi câu hỏi: thay vì hỏi câu giống câu chuẩn tới đâu, em kiểm xem câu có dẫn được một người
nghe độc lập tới đúng phần tử hay không. Ý tưởng người nghe đã có trong dòng sinh biểu thức quy chiếu;
phần việc của đề tài là đo và hiệu chuẩn thước ấy cho giao diện di động.

### Slide 5. Thước executability (1 phút)
Câu sinh ra được đưa cho UGround, một mô hình định vị không biết đáp án. UGround trả về một điểm.
Bước được tính đúng khi câu gọi đúng loại thao tác, điểm nằm trong dung sai 0,14 quanh điểm người dùng
đã chạm, và điểm rơi vào ô Voronoi của điểm chạm, tức gần điểm chạm hơn mọi phần tử bấm được khác.

Ví dụ bên phải: câu của S1 dẫn tới đúng ô Birthday, câu của mô hình gốc dẫn sang ô Gender ở trên.

(Nếu thầy hỏi vì sao cần Voronoi: mở dự phòng 1. Với câu chỉ sai nút, luật dung sai đơn thuần vẫn cho
điểm 84,3% số ca, Voronoi còn 2,8%.)

### Slide 6. Kiểm chứng thước (1 phút 30)
Trước khi dùng thước để kết luận, em đo chính thước. Thang ở trên cho thấy các mốc. Chấm chính câu
chuẩn được 75,7%; đó là trần, và mọi điểm khác phải đọc trên nền này chứ không phải trên nền 100. Câu
chung chung không nói phần tử nào chỉ được 12,0%, còn câu thật nhưng của màn hình khác chỉ được 6,1%,
nghĩa là văn phong đúng mà nội dung sai không được điểm.

Sáu ô bên dưới là sáu phép kiểm: sai số của mô hình định vị 0,7% bề ngang, nhỏ hơn khoảng cách giữa
các phần tử; năm luật chấm khác nhau giữ nguyên thứ tự; chấm lại bằng UI-Venus, mô hình không học
AndroidControl, giữ 94% chênh lệch; viết lại 1.139 câu chuẩn thì điểm gần như không đổi. Thêm một
người nghe trắc nghiệm Phi-4 ngoài họ Qwen cũng giữ nguyên thứ tự các nhánh.

### Slide 7. Dữ liệu (45 giây)
Không có bộ dữ liệu sẵn cho bài toán này nên em dựng từ AndroidControl, ghép hai kho trên HuggingFace,
chạy OCR và dựng nhãn mô tả phần tử. Kết quả là 64.567 bước huấn luyện, không thuê người gán nhãn. Ba
phép kiểm: phép ghép đúng 48% so với 20% của phép ghép cố ý lệch một bước, chín bất biến đều đạt, và
không có tác vụ nào trùng giữa tập dạy và tập kiểm. Phần này đã viết thành bài VCL.

### Slide 8. Mô hình nền (45 giây)
Mô hình nền là Qwen2.5-VL-3B, tinh chỉnh QLoRA. S1 đạt 59,1%, mô hình gốc 47,6%, hơn 11,5 điểm, lặp
lại ở cả hai hạt giống, nhiễu giữa hai hạt chỉ 0,46 điểm. Chênh lệch này đứng vững sau sáu cách giải
thích thay thế. S1 là mốc so của mọi nhánh phía sau.

### Slide 9. Các hướng đã thử (1 phút 30)
Trước khi tới phương pháp đề xuất, em đã thử nhiều hướng, và luận văn báo cả những hướng không cải
thiện. Đích khai báo bắt mô hình viết dòng mô tả phần tử trước câu: thấp hơn S1 1,93 điểm. Học tiếp
bằng ORPO đạt 60,0, nhưng 78% mức tăng thuộc về nhánh so sánh học có giám sát. Thưởng ô toạ độ đạt
77,3% dưới luật AitW, nhưng mức hơn đến từ những bước S1 gọi sai loại thao tác. Chọn trong danh sách
ứng viên thì bỏ cuộc quá mức. Bốn cách đưa thông tin vị trí vào bộ sinh câu đều cho cùng kết quả:
thông tin vị trí học được nhưng phần sinh câu bỏ qua.

Điểm chung của các hướng này là cùng tác động vào một tầng trung gian, và thay đổi ở tầng ấy truyền
sang câu rất yếu.

### Slide 10. Phân tích lỗi (1 phút)
Khi tách theo việc dòng khai báo đúng hay sai: khai báo đúng thì mô hình hơn S1 8,83 điểm, khai báo
sai thì kém 11,12 điểm. Cơ chế hoạt động, nhưng bị chặn bởi độ chính xác khai báo. Tách tiếp hai kênh:
91% khoảng cách tới câu chuẩn nằm ở 29,9% số bước mô hình nhìn sai phần tử ngay từ đầu. Mức truyền từ
tầng tri giác sang điểm câu chỉ 0,028.

Từ đó em rút ra thiết kế cho phương pháp đề xuất: đặt phần thưởng thẳng lên câu ở đầu ra.

### Slide 11. Phương pháp đề xuất (1 phút 30)
Phương pháp học tiếp từ S1 bằng GRPO. Với mỗi câu nhắc, mô hình sinh tám câu, mỗi câu được thưởng
bằng SPICE so với câu chuẩn, trừ một khoản phạt nhỏ nếu câu dài hơn câu chuẩn quá ba từ. Lợi thế được
chuẩn hoá trong nhóm tám câu, và có số hạng KL kéo về S1.

Em xuất phát thẳng từ S1, hoà bộ chuyển đổi rồi gắn một LoRA mới bắt đầu từ không, để phép so với S1
chỉ còn một biến là học tăng cường. Mô hình định vị dùng để chấm không có trong phần thưởng, nên thước
vẫn độc lập với mục tiêu huấn luyện. Tiền lệ là SCST và SPIDEr trong chú thích ảnh. Điểm mới em nhận là
hẹp: áp và đo cho bài toán này, không nhận mới ở thuật toán.

Lượt chạy 500 bước trên GPU T4 không thu phí, và điểm lưu 500 chỉ được chấm trên tập kiểm một lần.

### Slide 12. Kết quả chính (45 giây)
Biểu đồ đặt các nhánh chính dưới ba luật. Phương pháp đề xuất đạt 60,6% executability, cao nhất trong
mọi mô hình đã đo, và bằng chặng ba dưới luật hộp phần tử. Cột cuối là câu chuẩn, để thấy khoảng cách
còn lại.

### Slide 13. Nhóm thước theo vị trí, đủ các nhánh (1 phút)
Đây là sáu thước theo vị trí cho mọi nhánh đã chấm trên tập kiểm, tính lại từ bản ghi từng bước nên
không phải gọi lại mô hình định vị. Ngoài executability có luật khớp chạm của AitW và bản cận trên của
nó, luật hộp phần tử gốc của AndroidControl, luật dung sai 14% theo từng trục và tỉ lệ gọi đúng loại
thao tác. Ở cả năm luật vị trí, Base thấp nhất, câu chuẩn cao nhất, S1 hơn Base khoảng 11 đến 12 điểm.
Hai nhánh mạnh nhất đổi chỗ theo luật: chặng ba cao nhất dưới các luật lỏng, phương pháp đề xuất cao
nhất dưới executability, và hai nhánh bằng nhau dưới luật hộp phần tử (67,0).

### Slide 14. Nhóm thước so với câu chuẩn, đủ các nhánh (1 phút)
Bảy thước so câu chữ mà các bài cùng mảng như Widget Captioning và Screen2Words dùng: BLEU-4, METEOR,
ROUGE-L, CIDEr-D, SPICE, chrF và BERTScore. Phương pháp đề xuất cao nhất ở sáu trên bảy cột, riêng
ROUGE-L thấp hơn CE2-S2 0,2 điểm. Một điểm em khai luôn: nhóm thước này xếp S1 trên MIN-DESC và chặng
ba, ngược với executability, nên em dùng nhóm này để đặt kết quả cạnh các công trình khác, còn phép so
giữa các nhánh vẫn đọc trên executability.

### Slide 15. Phân rã executability (45 giây)
Bảng tách executability theo từng điều kiện. Tỉ lệ khớp thao tác của mọi nhánh đã ở mức 91 đến 99 trên
bước chạm, nên executability gần như bằng cột chỉ xét ô Voronoi. Nói cách khác, khoảng cách tới trần
nằm ở việc trỏ đúng phần tử, khớp với phần phân tích lỗi.

### Slide 16. Kiểm chéo bằng dụng cụ khác (1 phút)
Hai dụng cụ độc lập với UGround. Bên trái là người nghe trắc nghiệm Phi-4, ngoài họ Qwen: thứ tự các
nhánh giữ nguyên, chặng ba hơn S1 1,14 điểm có ý nghĩa, dù thang hẹp hơn vì câu chuẩn chỉ đạt 54,9.
Bên phải là UI-Venus, không học AndroidControl: chênh lệch S1 so với Base giữ 94%, và UI-Venus chấm
thấp hơn ở mọi nhánh nên đây không phải chọn dụng cụ để có số đẹp. Phương pháp đề xuất chưa được chấm
bằng hai dụng cụ này.

### Slide 17. Mười ba thước (1 phút)
Đây là toàn bộ các thước em dùng để so phương pháp đề xuất với S1, trên 4.463 bước chạm, ghép cặp
theo bước. Nhóm trên là sáu thước theo vị trí, đều chấm bằng mô hình định vị đọc câu: executability,
luật hộp phần tử của AndroidControl, luật khớp chạm của AitW và bản cận trên của nó, luật dung sai 14%
theo từng trục, và tỉ lệ gọi đúng loại thao tác. Cả sáu đều tăng, khoảng tin cậy nằm hẳn trên 0.

Nhóm dưới là bảy thước so câu chữ với câu chuẩn bằng bộ chấm COCO: SPICE, BLEU-4, METEOR, ROUGE-L,
CIDEr-D, chrF và BERTScore. Cả bảy cũng tăng. Phần thưởng chỉ là SPICE, nhưng mức tăng không dừng ở
SPICE, và các thước vị trí dùng mô hình định vị không hề có trong phần thưởng.

### Slide 18. Nguồn của mức tăng (1 phút)
Theo executability, phương pháp hơn S1 1,55 điểm, p bằng 1,6 nhân 10 mũ trừ 5, và so với hạt giống thứ
hai của S1 vẫn hơn 1,03 điểm. Đây là mô hình đầu tiên của đề tài hơn S1 có ý nghĩa thống kê ngay dưới
executability.

Quan trọng hơn là nguồn của mức tăng: 41 bước là đổi sang đúng phần tử khi cả hai mô hình đã gọi đúng
loại thao tác, tức định vị thật, còn 28 bước là sửa loại thao tác. Câu không dài thêm. Ví dụ bên phải:
S1 gọi nút Allow trong hộp thoại, phương pháp đề xuất gọi đúng nút Not Now ở cuối màn.

### Slide 19. Tác dụng phụ (45 giây)
Em cũng đo phía không chạm. Ở bước cuộn, tỉ lệ gọi đúng loại thao tác giảm 6,23 điểm, ở bước quay lại
giảm 5,93. Lý do là mô hình nghiêng về câu chạm: 47 trong 51 bước cuộn bị phá đổi từ "Swipe up" sang
"Click on". Luận văn báo tác dụng phụ này cạnh mọi số trên bước chạm, và nêu cách sửa là thêm số hạng
đúng loại thao tác vào phần thưởng.

### Slide 20. TAGE (45 giây)
Em thử thêm một bộ sửa câu đặt sau phương pháp đề xuất: cắt vùng quanh điểm do bộ định vị đoán, cho bộ
biên tập viết lại câu. Trên tập kiểm, TAGE chưa giúp, thấp hơn câu nháp 0,43 điểm. Nguyên nhân đo được:
bộ chọn nhận câu sửa đúng ở những bước vùng cắt sai chỗ. Phần này được trình bày như phần mở rộng.

### Slide 21. Đóng góp (1 phút)
Luận văn có ba đóng góp độc lập. Thứ nhất là thước executability cùng toàn bộ phép kiểm chứng. Thứ hai
là tập dữ liệu dựng tự động và phương pháp thưởng SPICE, nâng executability từ 59,1 lên 60,6 có ý
nghĩa thống kê. Thứ ba là phân tích lỗi qua các hướng đã thử, chỉ ra điểm nghẽn ở tầng tri giác, và là
căn cứ để chọn phương pháp.

### Slide 22. Hạn chế (45 giây)
Em liệt kê thẳng các hạn chế, và tất cả đã có trong chương 7 kèm số đo: các nhánh huấn luyện thêm chỉ
có một hạt giống, chưa có nhánh so sánh học có giám sát cùng số bước, mô hình định vị cùng họ Qwen,
chưa có phép chấm của người, và tác dụng phụ ở bước cuộn chưa sửa.

### Slide 23. Hướng phát triển (30 giây)
Hướng gần nhất là hoàn tất đánh giá phương pháp đề xuất: hạt giống thứ hai, nhánh so sánh, và sửa
phần thưởng cho bước cuộn. Sau đó là bộ chọn tốt hơn cho TAGE, học kênh vị trí từ đầu, chấm bằng người
và mở rộng sang dữ liệu khác.

### Slide 24. Tình trạng (45 giây)
Luận văn đủ tám chương, 153 trang, đã dựng PDF đầy đủ. Ba bài báo đã gửi: FAIR, VCL và SOICT. Hiện
em còn chạy thêm hai việc bổ sung: học tiếp với phần thưởng có người nghe Phi-4, và chấm nhánh thưởng
CIDEr-D để so hai lựa chọn phần thưởng. Hai việc này chỉ bổ sung; nếu không vượt thì mô hình chính giữ
nguyên và các kết luận trong luận văn không đổi.

---

## Phần 3. Lời đề nghị (nói sau slide 24, khoảng 2 phút)

Thưa thầy, em xin trình bày lý do em nghĩ luận văn đã đủ để hoàn tất.

**Thứ nhất, phần trả lời câu hỏi nghiên cứu đã trọn.** Bài toán được đặt lại rõ ràng, có thước đo
được kiểm chứng bằng nhiều phép đo độc lập, có dữ liệu dựng tự động, và có một phương pháp vượt mô
hình nền với ý nghĩa thống kê dưới chính thước chặt nhất. Kết quả ấy giữ được khi so với cả hai hạt
giống của mô hình nền và tăng ở cả mười ba thước.

**Thứ hai, kết quả được báo trung thực, kể cả phần không thuận lợi.** Các hướng không cải thiện, tác
dụng phụ ở bước cuộn và các hạn chế đều có trong luận văn kèm số đo, nên khi hội đồng hỏi, em có số để
trả lời thay vì phải giải thích thêm.

**Thứ ba, nội dung đã qua bình duyệt bên ngoài một phần.** Ba bài báo tách từ luận văn đã gửi FAIR,
VCL và SOICT, mỗi bài một phần đóng góp khác nhau.

**Thứ tư, phần còn lại không chặn việc hoàn tất.** Những lượt đang chạy là bổ sung. Các việc như hạt
giống thứ hai hay chấm của người đã ghi rõ là hướng phát triển, vì chi phí máy vượt khả năng của đề
tài trong thời gian còn lại.

Vì vậy em xin thầy ba việc:
1. Thầy đọc bản luận văn và cho em góp ý, ưu tiên những chỗ thầy thấy hội đồng sẽ hỏi.
2. Thầy đồng ý để em hoàn tất thủ tục kịp hạn 2/11.
3. Nếu thầy thấy cần bổ sung thí nghiệm nào trước khi nộp, thầy cho em biết sớm để em xếp lịch máy.

**Lịch đề xuất tới 2/11** (điều chỉnh theo ý thầy):

| mốc | việc |
|---|---|
| tuần 7–13/10 | gửi thầy bản PDF; nhận góp ý |
| tuần 14–20/10 | sửa luận văn theo góp ý; cập nhật số của hai lượt đang chạy nếu có kết quả |
| tuần 21–27/10 | bản cuối, kiểm trích dẫn và định dạng, chuẩn bị slide bảo vệ |
| trước 2/11 | hoàn tất hồ sơ |

---

## Phần 4. Câu thầy có thể hỏi và cách trả lời

**Mức tăng 1,55 điểm có nhỏ quá không?**
So với nhiễu giữa hai hạt giống của S1 là 0,46 điểm, mức tăng gấp hơn ba lần, và khoảng tin cậy ghép
cặp nằm hẳn trên 0, p bằng 1,6 nhân 10 mũ trừ 5. Mức tăng xuất hiện ở cả 13 thước, kể cả những thước
dùng mô hình định vị không có trong phần thưởng. Điểm số cũng phải đọc trên nền trần 75,7 của dụng cụ,
không phải 100.

**Executability 60% có thấp không?**
Trần của chính dụng cụ là 75,7, và thước này chặt hơn các thước khớp toạ độ thông thường vì câu phải đủ
để một mô hình độc lập trỏ đúng. Dưới luật khớp chạm của AitW, cùng mô hình đạt 76,2 và câu chuẩn 92,1.
Không nên so thẳng 60% với 70 đến 80% của các bài dùng thước khớp toạ độ trực tiếp.

**Vì sao thưởng SPICE mà không thưởng CIDEr như SCST?**
Zhao và cộng sự khuyên dùng SPICE khi xếp hạng hệ thống, và phép kiểm trên tập kiểm định cho thấy chọn
câu SPICE cao nhất trong chín câu của S1 nâng rõ executability. Nhánh thưởng CIDEr-D với cùng thiết lập
đã huấn luyện xong và đang được chấm trên tập kiểm, để so trực tiếp hai lựa chọn.

**Chỉ một hạt giống thì có tin được không?**
Đây là hạn chế đã khai. Mức hơn giữ dấu khi so với cả hai hạt giống của S1 (1,55 và 1,03 điểm), nhưng
chưa biết huấn luyện lại phương pháp với hạt khác có lặp lại không. Hạt thứ hai nằm đầu danh sách hướng
phát triển.

**Mô hình định vị cùng họ Qwen và đã học AndroidControl thì có thiên vị không?**
Chấm lại bằng UI-Venus, không học AndroidControl, giữ 94% chênh lệch S1 so với Base. Người nghe Phi-4
ngoài họ Qwen giữ nguyên thứ tự các nhánh. Phần chưa đóng là chưa kiểm chéo mọi phép so qua hai họ mô
hình, và luận văn ghi đúng như vậy.

**Tác dụng phụ ở bước cuộn có làm mất giá trị phương pháp không?**
Trên toàn 6.958 bước, mô hình được thêm 72 bước đúng loại thao tác ở bước chạm và mất 42 bước ở bước
không chạm. Tác dụng phụ có cơ chế rõ (nghiêng về câu chạm) và có cách sửa trực tiếp trong phần thưởng.
Luận văn báo nó cạnh mọi số trên bước chạm.

**Điểm mới của luận văn là gì?**
Đặt lại bài toán: câu hướng dẫn từng bước là đích sinh, không phải đầu vào. Thước executability cùng
khối kiểm chứng đặt bên dưới. Phương pháp thưởng theo câu áp và đo cho bài toán này, cùng phân tích lỗi
giải thích vì sao các hướng tác động vào tầng trung gian không truyền sang câu. Em không nhận mới ở
thuật toán GRPO hay ở việc chọn SPICE.

**Tập kiểm có phải phần kiểm chính thức của AndroidControl không?**
Không. Phần lớn tác vụ của tập kiểm thuộc phần huấn luyện chính thức, nhưng tập dạy và tập kiểm của đề
tài không trùng tác vụ nào, và tách điểm theo phần chia chính thức không thấy chênh lệch. Chấm trên
phần kiểm chính thức nằm trong hướng phát triển.

**Có cần chạy thêm gì trước khi nộp không?**
Hai lượt đang chạy là bổ sung và sẽ xong trong tháng 10. Nếu thầy thấy cần thêm thí nghiệm nào, em xin
biết sớm để xếp lịch máy kịp hạn.
