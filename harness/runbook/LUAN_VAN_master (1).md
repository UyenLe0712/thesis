# Mục lục

- Lời cam đoan
- Lời cảm ơn
- Danh mục các từ viết tắt, khái niệm và thuật ngữ
- Trang thông tin luận văn
- Thesis information
- Chương 1. Giới thiệu
  - 1.1 Đặt vấn đề
  - 1.2 Động lực nghiên cứu
  - 1.3 Mục đích nghiên cứu
  - 1.4 Một số nghiên cứu liên quan
  - 1.5 Nội dung và phạm vi thực hiện đề tài
  - 1.6 Đóng góp của luận văn
- Chương 2. Tổng quan
  - 2.1 Từ học sâu tới mô hình thị giác và ngôn ngữ
  - 2.2 Tinh chỉnh hiệu quả tham số bằng LoRA và QLoRA
  - 2.3 Học tăng cường với phần thưởng tính bằng luật
  - 2.4 Định vị phần tử giao diện
  - 2.5 Bộ dữ liệu AndroidControl
  - 2.6 Giới hạn của các độ đo có sẵn
- Chương 3. Xây dựng bộ dữ liệu
  - 3.1 Nguồn dữ liệu và quá trình ghép đa nguồn
  - 3.2 Kiểm tra tính chính xác của quá trình ghép dữ liệu
  - 3.3 Quy mô, cách chia tập và kiểm tra dữ liệu đánh giá
  - 3.4 Trích xuất chữ trên màn hình
  - 3.5 Xây dựng nhãn mô tả tự động
  - 3.6 Bốn tập dữ liệu và các điều kiện cấu trúc bắt buộc
  - 3.7 Tập cặp quy chiếu tối thiểu cho giai đoạn học ưu tiên
  - 3.8 Danh sách ứng viên cho mô hình chọn ứng viên
- Chương 4. Phương pháp tiếp cận
  - 4.1 Toàn bộ quy trình
  - 4.2 Đầu vào và câu nhắc
  - 4.3 Cấu hình huấn luyện
  - 4.4 Tổng quan phương pháp đề xuất
  - 4.5 Thành phần thứ nhất: học tăng cường thưởng SPICE
  - 4.6 Thành phần thứ hai: chép câu ví dụ khi đồng thuận loại thao tác (ACE)
  - 4.7 Các mốc so sánh
  - 4.8 Cách đọc kết quả
- Chương 5. Độ đo executability
  - 5.1 Định nghĩa
  - 5.2 Luật xác định trúng và giới hạn của luật dung sai quy ước
  - 5.3 Mô hình định vị dùng làm công cụ đo
  - 5.4 Sai số của công cụ đo
  - 5.5 Ngưỡng tối đa của độ đo
  - 5.6 Ngưỡng tối thiểu của độ đo
  - 5.7 Kiểm chứng bằng cách cố ý chèn lỗi
  - 5.8 Độ bền của độ đo trước các cách diễn đạt khác
  - 5.9 Chấm lại bằng mô hình định vị thứ hai
  - 5.10 Kiểm chéo bằng một người nghe ngoài họ Qwen
  - 5.11 So sánh với độ đo dựa trên câu chuẩn
  - 5.12 Độ nhạy của kết luận với luật chấm
  - 5.13 Thống kê
- Chương 6. Thực nghiệm và kết quả
  - 6.1 Thiết lập thực nghiệm
  - 6.2 Kết quả chính
  - 6.3 Thành phần thứ nhất: học tăng cường thưởng SPICE
  - 6.4 Thành phần thứ hai: chép câu ví dụ khi đồng thuận loại thao tác (ACE)
  - 6.5 Kết quả trên nhiều độ đo
  - 6.6 So sánh ghép cặp
  - 6.7 Chênh lệch giữa hai hạt giống
  - 6.8 Bảy cách giải thích thay thế
  - 6.9 Phân bố lỗi của mô hình tinh chỉnh có giám sát
  - 6.10 Các hướng đã thử trước phương pháp đề xuất
  - 6.11 Giới hạn của độ đo trên tập kiểm tra
  - 6.12 Trạng thái các mô hình và phép thử
- Chương 7. Kết luận
  - 7.1 Đóng góp của luận văn
  - 7.2 Hạn chế
  - 7.3 Hướng phát triển
  - 7.4 Tính sẵn có của dữ liệu và mã nguồn
- Chương 8. Các công trình nghiên cứu
- Tài liệu tham khảo
- Phụ lục A. Các hướng đã thử
  - A.1 Mô tả phần tử trước khi viết câu
  - A.2 Học ưu tiên trên dòng mô tả
  - A.3 Chọn phần tử trong danh sách ứng viên
  - A.4 Giai đoạn thưởng tọa độ
  - A.5 Tách khâu nhận ra phần tử và khâu diễn đạt thành câu
  - A.6 Đưa thêm thông tin vị trí vào bộ sinh câu
  - A.7 Sửa câu theo vùng cắt quanh phần tử (TAGE)

---

ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH  
TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN

Lê Đoàn Phương Uyên

**PHÁT SINH TỰ ĐỘNG HƯỚNG DẪN SỬ DỤNG PHẦN MỀM DỰA TRÊN LLM TỪ CÁC TRƯỜNG HỢP SỬ DỤNG VÀ GIAO DIỆN NGƯỜI DÙNG**

**LUẬN VĂN THẠC SĨ**

TP. Hồ Chí Minh – Năm 2026

---

ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH  
TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN

Lê Đoàn Phương Uyên

**PHÁT SINH TỰ ĐỘNG HƯỚNG DẪN SỬ DỤNG PHẦN MỀM DỰA TRÊN LLM TỪ CÁC TRƯỜNG HỢP SỬ DỤNG VÀ GIAO DIỆN NGƯỜI DÙNG**

Ngành: **TRÍ TUỆ NHÂN TẠO**  
Mã số ngành: 8480107

**NGƯỜI HƯỚNG DẪN KHOA HỌC**  
TS. Nguyễn Hồng Bửu Long

TP. Hồ Chí Minh - Năm 2026

# Lời cam đoan

Tôi cam đoan luận văn thạc sĩ ngành Trí tuệ nhân tạo với đề tài **Phát sinh tự động hướng dẫn sử dụng phần mềm dựa trên LLM từ các trường hợp sử dụng và giao diện người dùng** là công trình do tôi thực hiện dưới sự hướng dẫn của TS. Nguyễn Hồng Bửu Long.

Các số liệu và kết quả trình bày trong luận văn là trung thực, được tính từ mã nguồn cùng các tệp kết quả đi kèm, và chưa từng được công bố trong công trình của tác giả khác. Những thí nghiệm đã lên kế hoạch nhưng chưa thực hiện đều được ghi rõ là chưa thực hiện. Các tài liệu tham khảo được trích dẫn đầy đủ.

Tôi xin chịu trách nhiệm về tính trung thực của các kết quả trình bày trong luận văn.

Học viên cao học  
Lê Đoàn Phương Uyên

# Lời cảm ơn

Tôi thực hiện luận văn này tại Khoa Công nghệ Thông tin, Trường Đại học Khoa học Tự nhiên, Đại học Quốc gia Thành phố Hồ Chí Minh, dưới sự hướng dẫn của TS. Nguyễn Hồng Bửu Long.

Trước hết, tôi xin gửi lời cảm ơn chân thành đến thầy hướng dẫn, người đã định hướng đề tài và góp ý cho tôi trong suốt quá trình thực hiện luận văn.

Tôi xin cảm ơn quý thầy cô Khoa Công nghệ Thông tin đã giảng dạy trong suốt chương trình cao học, và cảm ơn Văn phòng Khoa đã hỗ trợ các thủ tục liên quan đến luận văn.

Cuối cùng, tôi xin cảm ơn gia đình đã tạo điều kiện để tôi theo học và hoàn thành chương trình này.

Tp. Hồ Chí Minh, tháng 10 năm 2026  
Lê Đoàn Phương Uyên

# Danh mục các từ viết tắt, khái niệm và thuật ngữ

| Viết tắt | Từ đầy đủ | Tiếng Việt / giải thích |
|---|---|---|
| GUI | Graphical User Interface | Giao diện đồ họa người dùng |
| VLM | Vision-Language Model | Mô hình thị giác và ngôn ngữ |
| LLM | Large Language Model | Mô hình ngôn ngữ lớn |
| SFT | Supervised Fine-Tuning | Tinh chỉnh có giám sát |
| LoRA | Low-Rank Adaptation | Tinh chỉnh hạng thấp |
| QLoRA | Quantized LoRA | LoRA trên trọng số đã lượng tử hoá |
| NF4 | 4-bit NormalFloat | Định dạng lượng tử hoá 4 bit |
| AitW | AndroidInTheWild | Bộ dữ liệu Android quy mô lớn (NeurIPS 2023). Trong các bảng, AitW chỉ luật khoảng cách Euclid của bộ dữ liệu này |
| OCR | Optical Character Recognition | Nhận dạng chữ trong ảnh |
| KTC | Confidence Interval | Khoảng tin cậy |
| dp | density-independent pixel | Đơn vị độ dài độc lập mật độ điểm ảnh trên Android |
| pp | percentage point | Điểm phần trăm (chênh lệch tuyệt đối giữa hai tỉ lệ) |
| ORPO | Odds Ratio Preference Optimization | Mục tiêu ưu tiên gắn thẳng vào hàm mất mát có giám sát, không cần mô hình tham chiếu |
| GRPO | Group Relative Policy Optimization | Học tăng cường trên từng nhóm câu trả lời sinh cho cùng một câu nhắc, lấy điểm trung bình của nhóm làm mốc so sánh thay cho một mô hình phê bình riêng |
| KL | Kullback-Leibler divergence | Độ lệch giữa hai phân bố xác suất, dùng để giữ mô hình không trôi xa mô hình tham chiếu |
| SPICE | Semantic Propositional Image Caption Evaluation | Độ đo so câu theo đồ thị đối tượng, thuộc tính và quan hệ |

## Thuật ngữ riêng của đề tài: phương pháp đề xuất

**Phương pháp đề xuất**  
Đóng góp chính của đề tài, gồm hai thành phần nối tiếp. Thành phần thứ nhất viết câu nháp, sau đó ACE quyết định giữ câu nháp hay thay bằng một câu ví dụ truy hồi được (Mục 4.4).

**Mô hình học với thưởng SPICE**  
Đây là thành phần thứ nhất của phương pháp đề xuất, trong đó mô hình tinh chỉnh có giám sát (S1) được học tiếp bằng học tăng cường theo nhóm, với phần thưởng là điểm SPICE của câu sinh ra so với câu chuẩn (Mục 4.5).

**Câu nháp**  
Câu mà mô hình học với thưởng SPICE viết cho bước đang xét bằng giải mã tham lam. Câu này được giữ nguyên, trừ khi luật đồng thuận của ACE cho phép thay.

**ACE (chép câu ví dụ khi đồng thuận loại thao tác)**  
*Action-Consistent Exemplar copying*, thành phần thứ hai của phương pháp đề xuất. Một bộ sinh được xem bốn câu chuẩn của các bước trong tập huấn luyện giống bước đang xét nhất, gọi là câu ví dụ. Câu của bộ sinh chỉ được nhận khi câu ấy chép nguyên văn một câu ví dụ và cùng loại thao tác với câu nháp; điều kiện này gọi là luật đồng thuận (Mục 4.6).

## Thuật ngữ riêng của đề tài: độ đo và thực nghiệm

**executability (tính thực thi được)**  
Độ đo của đề tài, dùng để chấm phương pháp đề xuất và mọi mô hình khác. Một câu hướng dẫn được tính là đúng nếu, khi đưa câu đó cho một mô hình định vị độc lập, mô hình ấy trỏ trúng phần tử mà người dùng đã chạm và câu gọi đúng loại thao tác.

**Mô hình định vị phần tử (GUI grounding model)**  
Mô hình nhận một câu mô tả cùng một ảnh màn hình và trả về tọa độ của phần tử được mô tả. Trong đề tài, mô hình này chỉ được dùng làm công cụ đo và không nằm trong số các mô hình được đem ra so sánh.

**Câu chuẩn**  
Câu hướng dẫn từng bước do người chú thích của AndroidControl viết cho chính bước đó. Chúng tôi dùng câu này làm câu tham chiếu, và khi đưa chính câu này đi chấm thì được mốc ngưỡng tối đa của độ đo.

**Bước chạm**  
Bước thao tác mà người dùng chạm vào màn hình, tức bước có tọa độ đích. Toàn bộ điểm số của đề tài tính trên nhóm bước này.

**Phần tử cần chạm**  
Nút, ô nhập hoặc mục danh sách mà người dùng đã chạm ở bước đang xét, tức đối tượng mà câu hướng dẫn phải chỉ ra được.

**Ô Voronoi**  
Vùng trên màn hình gồm những điểm nằm gần phần tử cần chạm hơn bất kỳ phần tử nào khác. Chúng tôi dùng vùng này để xác định thế nào là trỏ trúng, thay cho một dung sai cố định.

**Tập bước được chấm**  
Tập này gồm 4.463 bước chạm của tập kiểm tra và được dùng chung để chấm mọi mô hình, nên hai mô hình bất kỳ luôn so được với nhau trên đúng những bước như nhau.

**Ngưỡng tối đa và ngưỡng tối thiểu của độ đo**  
Ngưỡng tối đa là điểm mà câu chuẩn đạt được khi đưa đi chấm, dùng làm mốc trên khi đọc điểm của các mô hình. Ngưỡng tối thiểu là điểm mà một câu không mang thông tin gì vẫn đạt được. Mọi điểm số nên được đọc trong khoảng giữa hai mức này.

**Mô hình gốc (Base)**  
Đây là mô hình Qwen2.5-VL-3B-Instruct khi chưa tinh chỉnh, được dùng làm một mốc so sánh và trong các bảng được gọi là Base (Mục 4.7).

**Mô hình tinh chỉnh có giám sát (S1)**  
Mô hình gốc được tinh chỉnh có giám sát để sinh thẳng câu hướng dẫn từ câu nhắc, không qua bước trung gian nào. Mô hình này được huấn luyện hai lần với hai hạt giống, 101 và 202; thành phần thứ nhất của phương pháp đề xuất học tiếp từ hạt giống 101. Trong các bảng, mô hình này được gọi là S1 (Mục 4.7).

**Mốc so sánh và mô hình có can thiệp**  
Khi đánh giá một can thiệp, mốc so sánh là mô hình không có can thiệp đó, thường là mô hình tinh chỉnh có giám sát, còn mô hình có can thiệp là mô hình được thêm đúng can thiệp ấy. Đại lượng cần đo là chênh lệch điểm giữa hai mô hình.

**Hạt giống**  
Số dùng để khởi tạo phần ngẫu nhiên của một lượt huấn luyện. Hai lượt chỉ khác hạt giống là hai lần huấn luyện lại cùng một cấu hình, nên chênh lệch giữa chúng chỉ do yếu tố ngẫu nhiên.

**Điểm lưu (checkpoint)**  
Bản trọng số mô hình được ghi ra đĩa tại một thời điểm của lượt huấn luyện.

**Cách chia nhóm, nhóm con**  
Tập bước được chấm có thể chia thành các nhóm con, ví dụ theo độ dài câu hoặc theo số phần tử trên màn hình, để xem kết quả riêng trên từng nhóm.

**Phép so sánh kiểm chứng**  
Một phép so sánh mà ta đã biết chắc bên nào hơn và hơn đủ nhiều, dùng để kiểm tra xem một cách đo mới có còn nhận ra những khác biệt thật hay không.

**Tập kiểm định nội bộ**  
Tập 1.567 bước tách từ tập huấn luyện theo tác vụ, chỉ dùng để so các biến thể với nhau, không dùng để trình bày kết quả (Mục 3.3).

## Thuật ngữ riêng của đề tài: các hướng đã thử (Phụ lục A)

**Dòng mô tả phần tử (descriptor)**  
Đây là một dòng có cấu trúc gồm bốn phần, `[vai trò | tên | tọa độ | dấu hiệu phân biệt]`, mà mô hình phải viết ra trước câu hướng dẫn, gọi tắt là dòng mô tả. Dòng này bị cắt bỏ trước khi chấm và chỉ xuất hiện ở các hướng đã thử, không có trong phương pháp đề xuất.

**Mô hình mô tả phần tử (S2)**  
Đây là hướng đã thử đầu tiên, trong đó mô hình gốc được tinh chỉnh có giám sát để viết dòng mô tả phần tử rồi mới viết câu, theo nguyên tắc mô tả phân biệt trước, phát ngôn sau (Mục A.1.1).

**Cấu hình mô tả giả và cấu hình mô tả không có tọa độ (S2r, S2-nopoint)**  
Đây là hai cấu hình đối chứng được thiết kế cho mô hình mô tả phần tử nhưng chưa được chạy. Cấu hình thứ nhất thay dòng mô tả thật bằng một dòng mô tả giả có cùng độ dài, cấu hình thứ hai bỏ tọa độ khỏi dòng mô tả (Mục A.1.2).

**Giai đoạn học ưu tiên trên dòng mô tả (MIN-DESC)**  
Đây là giai đoạn huấn luyện thứ hai, học tiếp từ mô hình mô tả phần tử và gọi tắt là giai đoạn học ưu tiên; ở giai đoạn này, mô hình học từ những cặp chuỗi chỉ khác nhau ở dòng mô tả, còn câu hướng dẫn thì giống hệt nhau (Mục A.2.1).

**Mô hình học thêm có giám sát (CE2-S2)**  
Đây là mô hình dùng để so với giai đoạn học ưu tiên, chỉ học thêm có giám sát với cùng số bước, nhờ đó tách được phần cải thiện do mục tiêu ưu tiên mang lại khỏi phần chỉ do mô hình được huấn luyện thêm (Mục A.2.1).

**Danh sách ứng viên**  
Danh sách tối đa 40 phần tử của một màn hình, mỗi dòng gồm tên và tọa độ, dựng sẵn từ cây trợ năng và chữ đọc được trên màn hình, rồi đưa vào câu nhắc của mô hình chọn ứng viên (Mục 3.8).

**Mô hình chọn ứng viên**  
Đây là hướng đã thử trong đó mô hình chọn phần tử cần chạm từ danh sách ứng viên thay vì tự viết dòng mô tả; thẻ ghi phần tử được chọn bị cắt bỏ trước khi chấm (Mục A.3.1).

**Từ chối chọn**  
Đây là trường hợp mô hình chọn ứng viên phát thẻ `none` thay vì chọn một phần tử; việc từ chối là đúng khi danh sách không chứa phần tử cần chạm, và là sai khi danh sách có chứa phần tử đó.

**Giai đoạn thưởng tọa độ (giai đoạn ba)**  
Đây là giai đoạn huấn luyện thứ ba, học tiếp từ giai đoạn học ưu tiên bằng học tăng cường, với phần thưởng chủ yếu đặt trên tọa độ ghi trong dòng mô tả chứ không đặt trên câu (Mục A.4.1).

**Bộ sửa câu theo vùng cắt (TAGE)**  
Đây là bộ sửa câu đã thử ở cùng vị trí với ACE nhưng không được giữ lại trong phương pháp đề xuất. Bộ này gồm một bộ định vị đoán điểm cần chạm, một bộ biên tập xem phóng to vùng quanh điểm ấy rồi viết lại câu nháp, và một bộ chọn quyết định có nhận câu sửa hay không (Mục A.7.1).

# Trang thông tin luận văn

## TRANG THÔNG TIN LUẬN VĂN

Tên đề tài luận văn: Phát sinh tự động hướng dẫn sử dụng phần mềm dựa trên LLM từ các trường hợp sử dụng và giao diện người dùng.  
Ngành: Trí tuệ nhân tạo  
Mã số ngành: 8480107  
Họ và tên HVCH: Lê Đoàn Phương Uyên  
Khóa đào tạo: 34  
GVHD: TS. Nguyễn Hồng Bửu Long  
Cơ sở đào tạo: Trường ĐH Khoa học Tự nhiên, ĐHQG-HCM

## 1. Tóm tắt nội dung luận văn

Các hệ thống tác tử giao diện hiện nay nhìn ảnh màn hình rồi sinh ra tọa độ để phần mềm tự thao tác, còn đề tài này thay đổi mục tiêu đầu ra: thay vì sinh ra tọa độ cho máy, mô hình sinh ra câu hướng dẫn sử dụng cho người dùng, nói rõ cần chạm vào phần tử nào trên màn hình. Đầu vào vẫn giữ nguyên, gồm trường hợp sử dụng (mục tiêu người dùng đang thực hiện cùng các bước đã làm) và giao diện người dùng (ảnh màn hình đang mở cùng chữ đọc được trên đó).

Đóng góp chính của đề tài là một phương pháp gồm hai thành phần nối tiếp. Thành phần thứ nhất học tiếp từ mô hình Qwen2.5-VL-3B tinh chỉnh có giám sát bằng học tăng cường theo nhóm, với phần thưởng là điểm SPICE của câu sinh ra so với câu chuẩn (SPICE so hai câu theo các đối tượng, thuộc tính và quan hệ mà hai câu cùng nêu ra). Mô hình thu được viết câu nháp cho mỗi bước. Thành phần thứ hai (ACE) cho mô hình tham khảo thêm bốn câu chuẩn từ các bước tương tự nhất trong tập huấn luyện, gọi là câu ví dụ. Câu nháp chỉ được thay bằng câu của bộ sinh khi câu này chép nguyên văn một câu ví dụ và cùng loại thao tác với câu nháp.

Phương pháp đề xuất đạt 60,7% theo executability, độ đo của đề tài được mô tả ở đoạn sau. Mức này hơn mô hình tinh chỉnh có giám sát 1,57 điểm (khoảng tin cậy 95% [+0,86; +2,31]). Riêng thành phần thứ nhất đạt 60,6%, cao nhất trong các mô hình đã đo khi đứng một mình. Thành phần này hơn mô hình tinh chỉnh có giám sát 1,55 điểm ([+0,80; +2,33], p < 0,001) và cũng cao hơn ở cả mười ba độ đo được trình bày. So với riêng thành phần thứ nhất, ACE giữ nguyên executability và nâng cả bảy độ đo so câu, rõ nhất ở CIDEr-D (tăng 12,0 điểm) và SPICE (tăng 1,3 điểm).

Để chấm được phương pháp, chúng tôi xây dựng và kiểm chứng độ đo executability. Câu hướng dẫn khó chấm vì cùng một nút có nhiều cách gọi tên đều đúng, ví dụ như “thanh tìm kiếm” và “biểu tượng kính lúp”, nên không thể lấy một câu chuẩn duy nhất làm đáp án. Vì vậy câu do mô hình sinh ra được đưa cho một mô hình định vị phần tử độc lập, và mô hình này không được cung cấp đáp án. Bước được tính là đúng khi mô hình định vị trỏ trúng phần tử mà người dùng đã chạm, đồng thời câu gọi đúng loại thao tác. Trước khi dùng độ đo để rút ra kết luận, chúng tôi kiểm chứng chính độ đo này. Đưa chính câu chuẩn đi chấm thì được 75,7%, và mọi điểm số khác phải được đọc trên nền ngưỡng tối đa này. Thứ tự giữa các hệ thống vẫn giữ nguyên khi chấm lại bằng hai công cụ đo khác. Công cụ thứ nhất là một mô hình định vị thứ hai, vốn không được huấn luyện trên bộ dữ liệu của đề tài. Công cụ thứ hai là một người nghe trắc nghiệm, nghĩa là một mô hình khác họ đọc câu rồi chọn phần tử đúng trong danh sách các phần tử được đánh số.

Một quy trình hoàn toàn tự động chuyển bộ dữ liệu AndroidControl thành tập huấn luyện 64.567 bước. Trên 4.463 bước chạm của tập kiểm tra, mô hình tinh chỉnh có giám sát, là điểm xuất phát của phương pháp đề xuất, đạt 59,1%, so với 47,6% của chính mô hình đó khi chưa tinh chỉnh. Theo luật hộp phần tử của AndroidControl, tính trúng khi điểm trỏ nằm trong khung của phần tử cần chạm, hai con số tương ứng là 65,5% và 53,6%. Chúng tôi đã kiểm tra bảy cách giải thích khác nhau cho khoảng cách giữa hai mô hình và loại bỏ được sáu cách.

Phương pháp đề xuất được chọn sau một chuỗi hướng đã thử (chi tiết ở Phụ lục A). Phần lớn các hướng này tác động vào một bước trung gian giữa ảnh và câu, chẳng hạn một dòng mô tả phần tử cần chạm mà mô hình phải viết ra trước câu hướng dẫn, hay thông tin vị trí đưa thêm vào bộ sinh câu. Phân tích rút ra từ các hướng này (mục 2) cho thấy thay đổi ở bước trung gian hầu như không tác động đến câu hướng dẫn ở đầu ra, nên phương pháp đề xuất đặt phần thưởng thẳng lên câu ở đầu ra.

## 2. Những kết quả mới của luận văn

- **Một phương pháp hai thành phần vượt mô hình tinh chỉnh có giám sát theo executability.** Thành phần thứ nhất học tăng cường với phần thưởng SPICE để viết câu nháp, thành phần thứ hai (ACE) sao chép một câu ví dụ lấy từ tập huấn luyện khi câu ấy cùng loại thao tác với câu nháp. Phương pháp cho executability cao hơn mô hình tinh chỉnh có giám sát với ý nghĩa thống kê, dù mô hình định vị dùng để chấm không nằm trong phần thưởng. ACE nâng cả bảy độ đo so câu mà không làm giảm executability.
- **Một độ đo không cần câu chuẩn làm đáp án, dùng để chấm phương pháp.** Luật xác định thế nào là trỏ trúng được chọn bằng phép đo thay vì theo một dung sai quy ước, theo đó luật nào chấm đúng cho nhiều câu thực ra chỉ tới một nút khác thì bị loại. Thứ tự giữa các hệ thống không đổi khi chấm lại bằng năm luật khác nhau.
- **Ngưỡng tối đa và ngưỡng tối thiểu của độ đo đều được đo trực tiếp.** Ngoài ngưỡng tối đa nêu ở mục 1, câu chung chung không nói phần tử nào chỉ được 12,0%, còn câu thật nhưng của một màn hình khác chỉ được 6,1%, thấp nhất trong mọi phép đo. Như vậy độ đo chấm theo nội dung của câu, và câu đúng văn phong mà sai nội dung không được cho điểm.
- **Một quy trình dựng dữ liệu chạy hoàn toàn tự động.** Quy trình này chuyển AndroidControl thành tập huấn luyện cho tác vụ mới, ghép hai bản phát hành công khai (một bản có câu hướng dẫn, một bản có ảnh) và kiểm tra tính chính xác của quá trình này bằng cách so với dữ liệu có ý làm lệch một bước.
- **Phân tích ở mức từng bước qua các hướng đã thử (Phụ lục A).** Dòng mô tả phần tử có tác dụng đúng như giả thuyết, nhưng tác dụng ấy không vượt quá độ chính xác của chính dòng mô tả. Phần lớn khoảng cách tới câu chuẩn dồn vào những bước mà mô hình nhìn sai phần tử ngay từ đầu, nghĩa là sai ở khâu nhận ra phần tử. Mặt khác, khi một can thiệp đã chạy giúp mô hình tự chỉ đúng phần tử ở nhiều bước hơn, executability gần như không tăng, chứng tỏ phần cải thiện ở khâu nhận ra phần tử chỉ chuyển thành rất ít điểm executability. Mô hình chọn ứng viên chọn tốt nhưng lại từ chối chọn (không chọn phần tử nào) quá thường xuyên, còn thông tin vị trí đưa thêm vào bộ sinh câu tuy học được nhưng bị phần sinh câu bỏ qua.
- **Cách đặt lại bài toán.** Trong bộ AndroidControl gốc và trong các công trình dùng bộ này, câu hướng dẫn từng bước do người chú thích viết là đầu vào của mô hình. Ở đây, mô hình phải tự viết ra câu đó, và điểm số tính trên chính câu mô hình viết.

CÁN BỘ HƯỚNG DẪN HỌC VIÊN CAO HỌC  
(Ký tên, họ tên) (Ký tên, họ tên)

XÁC NHẬN CỦA CƠ SỞ ĐÀO TẠO  
HIỆU TRƯỞNG

# Thesis information

## THESIS INFORMATION

Thesis title: LLM-Based Automatic Generation of Software User Guides from Use Cases and Front-End Structures.  
Speciality: Artificial Intelligence  
Code: 8480107  
Name: Le Doan Phuong Uyen  
Academic year: 34  
Supervisor: Dr. Nguyen Hong Buu Long  
At: VNUHCM – University of Science

## 1. Summary

GUI agent systems look at a screenshot and produce a coordinate for the software to click. We keep that input but change the output: instead of a coordinate for a machine, the model writes a short English sentence for a person, telling them which element on the screen to touch. The input consists of the use case, that is, the goal the user is pursuing together with the steps already taken, and the user interface, that is, the open screenshot together with the text readable on it.

The main contribution is a method with two stages in sequence. The first stage continues from the supervised Qwen2.5-VL-3B model with group-relative reinforcement learning, using the SPICE score of the generated sentence against the reference as its reward (SPICE compares two sentences by the objects, attributes and relations they both mention), and writes a draft sentence for each step. The second stage (ACE, Action-Consistent Exemplar copying) lets a generator see the reference sentences of the four training steps most similar to the current step, called exemplars, and replaces the draft with the generator's output only when that output copies one exemplar verbatim and names the same action type as the draft.

The proposed method reaches 60.7% executability, the measure described in the next paragraph, which is 1.57 points above the supervised baseline (95% CI [+0.86, +2.31]). The first stage alone reaches 60.6%, the highest of any single model measured, 1.55 points above the supervised baseline (95% CI [+0.80, +2.33], p < 0.001), and it improves all thirteen reported measures. Relative to the first stage alone, ACE keeps executability unchanged and raises all seven reference-based text measures, most clearly CIDEr-D (+12.0) and SPICE (+1.3).

To score the method, we build and validate a measure called executability. Such sentences are hard to score because the same button can be named correctly in several ways, for instance “the search bar” and “the magnifying glass”, so no single reference sentence can serve as the answer key. The generated sentence is therefore handed to a separate GUI grounding model that never sees the correct coordinate, and the step counts as correct when that model points at the element the user actually touched and the sentence names the right action type. The metric itself is validated before it is used: scoring the human-written references gives 75.7%, the ceiling against which every other score must be read. Re-scoring with a second grounding model not trained on this corpus, and with a multiple-choice listener from a different model family (a model that reads the sentence and picks the right element from a numbered list), preserves the ordering of systems.

A fully automatic pipeline turns AndroidControl into 64,567 training steps. Over 4,463 held-out touch steps, the supervised Qwen2.5-VL-3B, which is the starting point of the proposed method, reaches 59.1% against 47.6% for the same model untuned. Under AndroidControl's own element-box rule, which counts a hit when the predicted point falls inside the box of the target element, the two figures are 65.5% and 53.6%. Of seven alternative explanations checked for this gap, six are ruled out.

The method was chosen after a sequence of attempts (detailed in Appendix A), most of which act on an intermediate layer between the screenshot and the sentence, such as a structured element description written before the instruction, or location information fed into the sentence generator. The analysis drawn from these attempts (Section 2) shows that such changes barely reach the sentence, which is why the proposed method puts its reward directly on the output sentence.

## 2. Novelty of thesis

- **A two-stage method**, reinforcement learning rewarded by SPICE followed by action-consistent exemplar copying (ACE), that beats the supervised baseline with statistical significance under the strict executability rule, although the grounding model used for scoring plays no part in the reward. ACE raises all seven reference-based text measures without lowering executability.
- **A metric for element identification in generated GUI instructions that needs no reference sentence as the answer key**, used to score the method, with the hit rule selected from measured behaviour on wrong-element inputs rather than from a tolerance convention, and shown to preserve system ordering under five different rules.
- **A measured ceiling and floor.** Beyond the ceiling given in Section 1, one generic sentence that names no element scores 12.0%, and a real sentence describing a different screen scores 6.1%, the lowest of anything measured, so the metric responds to what a sentence says, not to how it is phrased.
- **A fully automatic pipeline converting AndroidControl into supervision for this task**, joining two public releases (one with the instructions, one with the screenshots) and validating the join against a deliberately shifted control.
- **A step-level analysis drawn from the attempts that preceded the method (Appendix A).** The element description written before the instruction works as hypothesised, but its effect is capped by the accuracy of the description itself. Most of the gap to the reference sentences falls on steps where the model looks at the wrong element from the start, that is, where it fails to recognise the target element. When an intervention we ran made the model point to the right element on more steps, executability barely moved, so gains in recognising the element turn into very few executability points. A candidate-selection model selects well but declines to choose too often, and location information fed into the generator is learnable but ignored.
- **Problem positioning.** In AndroidControl and in work built on it, the human-written per-step instruction is an input. Here it is the generation target and the only scored output.

SUPERVISOR MASTER STUDENT

CERTIFICATION  
UNIVERSITY OF SCIENCE  
PRESIDENT

# Chương 1. Giới thiệu

## 1.1 Đặt vấn đề

Khi thao tác trên điện thoại, không ít lần người dùng dừng lại giữa chừng vì chưa rõ bước tiếp theo cần làm gì. Lúc ấy, điều họ cần thường chỉ là một câu chỉ dẫn ngắn cho đúng bước cần làm, ví dụ như “Chạm vào biểu tượng chia sẻ ở góc trên bên phải màn hình”.

Những năm gần đây, dòng nghiên cứu về tác tử giao diện (GUI agent) giải một bài toán rất gần với bài toán trên, nhưng khác ở đầu ra. Với cùng một ảnh màn hình và cùng một mục tiêu, các hệ thống như SeeClick [3], OS-Atlas [4] hay Aguvis [7] trả về loại thao tác kèm tọa độ trên màn hình, dạng `click(872,141)`, để phần mềm tự thao tác thay người. Một số mô hình có viết thêm một đoạn văn bản trước khi đưa ra tọa độ, chẳng hạn mô tả thao tác sắp làm, nhưng đoạn văn bản ấy chỉ giúp mô hình tìm ra tọa độ. Khi đánh giá, các mô hình này được chấm trên thao tác và tọa độ cuối cùng, còn đoạn văn bản thì không được chấm.

Đề tài này dùng cùng loại đầu vào với các mô hình trên. Điểm khác là mô hình không trả về tọa độ để máy tự bấm, mà viết ra một câu hướng dẫn giống ví dụ ở đầu mục, và kết quả được đánh giá trên chính câu hướng dẫn ấy. Việc đổi đầu ra từ tọa độ sang câu chữ dẫn tới hai vấn đề mà các công trình trước chưa có cách giải sẵn.

Tên đề tài gọi hai thành phần của đầu vào là *trường hợp sử dụng* và *giao diện người dùng*. Trường hợp sử dụng ở đây là mục tiêu người dùng đang theo đuổi, ví dụ như đặt vé xem phim cho tối nay hay tắt thông báo của một ứng dụng, cùng với các bước đã làm trước đó. Giao diện người dùng là ảnh chụp màn hình đang mở cùng chữ đọc được trên màn; ở khâu dựng dữ liệu, chúng tôi còn dùng thêm cây trợ năng của chính màn hình ấy. Mô hình ngôn ngữ lớn được dùng là một mô hình thị giác và ngôn ngữ cỡ ba tỉ tham số, nhận hai thành phần trên và viết ra câu hướng dẫn cho bước kế tiếp.

Vấn đề thứ nhất nằm ở khâu đánh giá: một tọa độ dự đoán có thể đem so trực tiếp với tọa độ mà người dùng đã chạm, nhưng một câu thì khó so với một câu chuẩn duy nhất, bởi cùng một nút thường có nhiều cách gọi đều đúng. Ví dụ như “Click on the search bar” và “Tap the magnifying glass at the top” cùng chỉ về một phần tử, trong khi không bộ dữ liệu nào liệt kê được hết các cách diễn đạt hợp lệ.

Các độ đo quen dùng đều gặp khó ở điểm này, và chúng tôi đã đo mức hạn chế của từng độ đo. So khớp chuỗi ký tự loại nhầm tới 97,5% số câu diễn đạt khác đi. So vector ngữ nghĩa cũng không khá hơn: trên 51 trường hợp viết tay, diện tích dưới đường ROC (AUC) chỉ đạt 0,336, tức còn thấp hơn đoán ngẫu nhiên. Nguyên nhân là vector ngữ nghĩa đo độ gần về chủ đề, trong khi điều cần biết là hai câu có cùng nói về một phần tử hay không. Trong phép thử này, cặp `inbox` và `outbox` được chấm 0,76, cao hơn khá nhiều so với cặp `search` và `magnifying glass` (0,55), dù chỉ cặp sau mới cùng chỉ một nút (chi tiết ở Mục 2.6).

**Vấn đề thứ hai nằm ở dạng lỗi mà mô hình sinh câu hay mắc.** Khi đọc thủ công 40 trường hợp sinh sai, chúng tôi thấy trường hợp mô hình nêu một nút không có trên màn hình chỉ chiếm khoảng 0 đến 2%. Phần lớn lỗi còn lại là câu mơ hồ, ví dụ mô hình viết “biểu tượng tìm kiếm” trong khi màn hình có tới hai biểu tượng như vậy. Câu ấy không sai về mặt sự thật, nhưng người đọc khó dùng được, vì câu không giúp phân biệt phần tử cần chạm với những phần tử giống nó ở bên cạnh. Vì vậy, điều cần cải thiện là tính phân biệt của câu, tức câu phải giúp người đọc nhận ra đúng phần tử cần chạm giữa những phần tử trông giống nó. Còn lỗi nêu một phần tử không có trên màn hình vốn đã rất hiếm, nên dù giảm thêm thì chất lượng câu cũng không tăng được bao nhiêu.

Công việc của đề tài được chia theo hai vấn đề trên. Phần thứ nhất xây dựng và kiểm chứng một độ đo dùng được cho câu hướng dẫn. Phần thứ hai thiết kế và huấn luyện một mô hình viết ra những câu ít mơ hồ hơn. Đóng góp chính của đề tài là phương pháp đề xuất ở phần thứ hai, còn độ đo ở phần thứ nhất là công cụ để đánh giá phương pháp ấy. Mục 1.6 tóm tắt cả hai phần cùng các kết quả chính.

## 1.2 Động lực nghiên cứu

### 1.2.1 Động lực khoa học

Yêu cầu rằng một mô tả phải đủ để người tiếp nhận xác định đúng đối tượng vốn không mới. Từ năm 2016, dòng nghiên cứu sinh biểu thức quy chiếu (*referring expression generation*) trong thị giác máy tính đã đặt ra chính yêu cầu này. Mao và cộng sự [11] chấm một mô tả bằng một mô hình hiểu (*listener*), tức một mô hình nhận mô tả rồi chọn ra đối tượng được nhắc tới, và mô tả được tính là đạt khi mô hình ấy chọn đúng. Luo và Shakhnarovich [12] cùng Yu và cộng sự [13] đưa luôn mô hình hiểu ấy vào vòng huấn luyện. Đề tài kế thừa nguyên tắc này và không xem đó là đóng góp của mình.

Ở miền giao diện, yêu cầu này đã được nêu ra nhưng chưa được đưa vào mục tiêu huấn luyện. Widget Captioning [9], công trình gần nhất trong miền này, đã chỉ ra trường hợp hai phần tử trông giống hệt nhau, nhưng vẫn huấn luyện bằng hàm mất mát entropy chéo thuần, tức không có số hạng nào đẩy mô tả về phía phân biệt hơn.

Ở phía đánh giá, ALOHa [14] dựa trên nguyên tắc kiểm chứng một phát biểu bằng một nguồn có cấu trúc bên ngoài thay vì bằng chính niềm tin của mô hình sinh. Đề tài đi theo nguyên tắc đó, nhưng có một khác biệt khiến việc kiểm chứng kém chắc chắn hơn. ALOHa đối chiếu với một danh sách tĩnh, còn chúng tôi đối chiếu với kết quả của một mô hình định vị phần tử đã học, nên độ tin cậy của độ đo không thể vượt quá độ tin cậy của chính mô hình ấy. Vì vậy, một phần đáng kể của đề tài dành cho việc kiểm tra chính công cụ đo trước khi dựa vào nó để rút ra kết luận.

Jandial và cộng sự [18] đưa ra một cảnh báo liên quan trực tiếp tới độ đo đề xuất. Nhóm tác giả cho thấy các bộ chuẩn hiện nay chỉ đo độ chính xác trên một câu tốt nhất cho mỗi phần tử, nên con số công bố cao hơn năng lực thật của mô hình định vị. Trong công trình ấy, một tác tử đối kháng chuyên viết câu làm mô hình định vị trỏ sai đạt tỉ lệ thành công tới 84% trên giao diện máy tính để bàn. Con số này là tỉ lệ thành công của một quá trình chủ động tìm câu đối kháng, khác với tỉ lệ trượt khi người dùng chỉ đơn giản diễn đạt khác đi. Các tác giả cũng chưa khảo sát giao diện di động. Mục 5.8 kiểm phần cảnh báo áp dụng được cho đề tài bằng cách viết lại câu chuẩn rồi chấm lại, còn Mục 7.2 nêu những phần chưa kiểm được.

### 1.2.2 Động lực ứng dụng

Tác vụ này đã có nhu cầu thực tế, chẳng hạn GuideMe [19] là một hệ thống giúp người cao tuổi tự học dùng điện thoại thông minh: người dùng đặt câu hỏi, hệ thống nhìn màn hình rồi trả về hướng dẫn từng bước. Hệ thống gọi một mô hình thương mại cỡ lớn qua mạng, không huấn luyện thêm mô hình nào, và chất lượng được đánh giá qua một nghiên cứu người dùng với 18 người, chưa có độ đo định lượng đi kèm.

Ví dụ này cho thấy hai điều còn thiếu ở phía ứng dụng. Trước hết, hiện chưa có độ đo định lượng nào cho phép so sánh hai hệ thống sinh hướng dẫn giao diện một cách tái lập được. Ngoài ra, việc phải gửi ảnh màn hình lên dịch vụ bên ngoài là một rào cản thực tế, vì ảnh màn hình điện thoại thường chứa tin nhắn, số dư tài khoản hay danh bạ. Một mô hình cỡ ba tỉ tham số chạy được ngay trên máy người dùng giúp tránh rào cản ấy, nên chúng tôi chọn kích cỡ này thay vì mô hình lớn nhất có thể.

## 1.3 Mục đích nghiên cứu

Đề tài hướng tới một mục tiêu chính và hai mục tiêu hỗ trợ. Mục tiêu chính là phương pháp sinh câu hướng dẫn, còn hai mục tiêu hỗ trợ cung cấp cho phương pháp ấy một độ đo để đánh giá và một tập giám sát để huấn luyện.

1. Mục tiêu chính là thiết kế và huấn luyện phương pháp đề xuất trên một mô hình thị giác và ngôn ngữ cỡ nhỏ, để mô hình viết ra những câu hướng dẫn ít mơ hồ hơn. Phương pháp được so với mô hình tinh chỉnh có giám sát trên từng bước của cùng một tập kiểm tra (phép so sánh ghép cặp), và mức chênh được đặt cạnh mức dao động đo được giữa hai lần huấn luyện cùng cấu hình nhưng khác hạt giống ngẫu nhiên. Các hướng đã thử trước khi đi tới phương pháp đề xuất được phân tích chi tiết nhằm làm rõ đâu là khâu khó nhất của bài toán.
2. Mục tiêu hỗ trợ thứ nhất là xây dựng một độ đo cho bài toán sinh hướng dẫn giao diện mà không dựa vào việc so với một câu chuẩn duy nhất, và kiểm chứng độ đo ấy bằng các phép đo độc lập.
3. Mục tiêu hỗ trợ thứ hai là chuyển bộ dữ liệu AndroidControl [1] thành tập giám sát cho tác vụ này một cách hoàn toàn tự động, không thuê người gán nhãn và không dùng nhãn do mô hình khác sinh ra.

## 1.4 Một số nghiên cứu liên quan

### 1.4.1 Định vị phần tử giao diện và tác tử giao diện

AndroidControl [1] là nguồn dữ liệu của đề tài, trong đó mỗi bước có một câu hướng dẫn do chính người thao tác viết. AndroidInTheWild [2] là nguồn gốc của dung sai 0,14 trên tọa độ chuẩn hoá, vốn được dùng rộng rãi để xét một dự đoán tọa độ là trúng hay trượt; cả hai được giới thiệu chi tiết ở Chương 2.

Các mô hình định vị phần tử như SeeClick [3], OS-Atlas [4] và UGround [5] ánh xạ một biểu thức văn bản thành một điểm trên màn hình. Chúng tôi dùng một mô hình thuộc nhóm này làm công cụ đo, chứ không làm đường cơ sở để so sánh. Vì thế, trước khi dựa vào công cụ này, chúng tôi trình bày sai số đo được cùng thành phần dữ liệu huấn luyện của mô hình ấy (Mục 5.4 và Mục 7.2).

Việc đưa một danh sách phần tử có cấu trúc vào đầu vào cũng đã khá phổ biến. Chính nhóm tác giả AndroidControl tinh chỉnh mô hình với danh sách phần tử suy ra từ cây trợ năng và cho biết tác tử của họ không dùng trực tiếp ảnh màn hình [1]. Mind2Web [8] huấn luyện trên tập ứng viên có lẫn phần tử sai, còn Widget Captioning [9] và Screen2Words [10] đặt cây phần tử ở đầu vào. Vì vậy đề tài không nhận đóng góp nào ở việc đưa danh sách phần tử vào đầu vào; cách làm này chỉ được dùng trong mô hình chọn ứng viên, một trong các hướng đã thử (Phụ lục A).

### 1.4.2 Sinh mô tả có tính phân biệt

Bài toán sinh một mô tả đủ để nhận ra đúng một đối tượng giữa những đối tượng dễ gây nhầm lẫn chính là bài toán sinh biểu thức quy chiếu [11]. Các công trình tiếp theo đặt một mô hình hiểu vào vòng huấn luyện để thúc đẩy tính phân biệt [12, 13]. Trong miền giao diện, công trình có giám sát gần nhất là Widget Captioning [9], và như đã nêu, hàm mất mát ở đó vẫn là entropy chéo thuần.

Một trong các hướng đã thử là mô hình mô tả phần tử (Phụ lục A), trong đó mô hình viết một dòng mô tả phần tử cần chạm rồi mới viết câu hướng dẫn. Vì dòng nghiên cứu nêu trên đã có từ năm 2016, chúng tôi không xem đây là một cơ chế mới. Hướng này chỉ nhằm kiểm xem, với bài toán sinh hướng dẫn giao diện, việc đưa yêu cầu phân biệt vào đầu ra mẫu mà mô hình học theo, dưới dạng một dòng mô tả phần tử viết trước câu, có tác dụng ra sao.

### 1.4.3 Học tăng cường với phần thưởng là một độ đo so câu

Trong sinh chú thích ảnh, việc dùng chính độ đo đánh giá câu làm phần thưởng cho học tăng cường đã có từ trước. Rennie và cộng sự [46] tối ưu trực tiếp CIDEr bằng gradient chính sách, lấy điểm của câu giải mã tham lam làm mốc so sánh; Liu và cộng sự [48] tối ưu SPIDEr, một tổ hợp của SPICE và CIDEr. GRPO [43] thay mốc so sánh ấy bằng trung bình điểm của một nhóm câu mẫu cho cùng một đầu vào. Do đó thành phần thứ nhất của phương pháp đề xuất không nhận điểm mới ở thuật toán, cũng như ở việc chọn SPICE làm phần thưởng. Đề tài chỉ kiểm tra xem việc tối ưu một độ đo so câu với câu chuẩn có giúp câu hướng dẫn giao diện dẫn tới đúng phần tử hơn hay không. Việc chấm đúng sai do một mô hình định vị độc lập đảm nhận, và mô hình này không tham gia vào phần thưởng.

### 1.4.4 Sinh bước trung gian trước khi sinh đáp án

Ý tưởng cho mô hình sinh một biểu diễn trung gian trước khi đưa ra đáp án cuối đã được thử nhiều lần, với kết quả không cùng một chiều. Bảng 1.1 tổng hợp năm kết quả từ các công trình trước. Chúng tôi dựa vào các kết quả này khi thiết kế mô hình mô tả phần tử, một trong các hướng đã thử (Phụ lục A); các kết quả ấy không liên quan tới phương pháp đề xuất.

**Bảng 1.1.** Ảnh hưởng của bước trung gian trong các công trình trước. Số dương nghĩa là có bước trung gian thì tốt hơn.

| Công trình | Phép so | Chênh lệch |
|---|---|---:|
| Aguvis [7] | bỏ bước trung gian, đo trên chính AndroidControl mức thấp | -11,4 |
| Shikra (văn xuôi) [35] | bước trung gian viết bằng văn tự do | -7,4 |
| Shikra (có tọa độ) [35] | cùng mô hình, bước trung gian có tọa độ | +5,9 |
| GCoT [36] | huấn luyện sinh định vị trước (LLaVA-7B / 13B) | +4,5 / +5,8 |
| CogCoM [33] | bỏ 70K dữ liệu chuỗi trung gian khỏi huấn luyện | +6,6 / +0,2 / +0,9 |

Hai dòng Shikra dùng cùng một mô hình và cùng một bài kiểm, chỉ khác nhau ở dạng của bước trung gian. **Bước trung gian viết bằng văn xuôi cho kết quả âm, còn bước trung gian có kèm tọa độ cho kết quả dương.** Con số âm hay được trích của GCoT [36] được đo khi chỉ dùng câu nhắc với một mô hình chưa huấn luyện; khi huấn luyện theo thứ tự định vị trước, chính công trình đó cho kết quả dương như trong bảng.

### 1.4.5 Đánh giá không cần đáp án tham chiếu

Sai và cộng sự [15] hệ thống hoá việc kiểm chứng một độ đo bằng cách cố ý chèn lỗi có kiểm soát, tức biến đổi câu theo từng kiểu đã biết rồi xem điểm của độ đo đó có thay đổi đúng chiều hay không. Chúng tôi áp dụng lại quy trình ấy (Mục 5.7). Chúng tôi cũng lưu ý cảnh báo rằng các đại lượng tự động thay cho đánh giá của người dễ được tin quá mức [16].

## 1.5 Nội dung và phạm vi thực hiện đề tài

### 1.5.1 Nội dung nghiên cứu

- Khảo sát các mô hình thị giác và ngôn ngữ, cùng các kỹ thuật tinh chỉnh hiệu quả tham số phù hợp với điều kiện chỉ có một GPU.
- Khảo sát các độ đo hiện có cho văn bản sinh không có đáp án chuẩn, đo mức hạn chế của chúng trên dữ liệu thật, rồi từ đó thiết kế độ đo thay thế.
- Xây dựng quy trình tự động chuyển AndroidControl thành tập giám sát, gồm bốn khâu: ghép dữ liệu đa nguồn, chạy OCR, dựng nhãn mô tả từ cây trợ năng và kiểm tra trùng lặp dữ liệu đánh giá.
- Thiết kế, huấn luyện và đánh giá phương pháp đề xuất, gồm học tăng cường với phần thưởng SPICE và ACE, so với mô hình tinh chỉnh có giám sát và với các hướng đã thử (Phụ lục A).
- Phân tích lỗi trên từng bước, nêu rõ các giới hạn kèm số đo dùng để loại trừ hoặc xác nhận từng giới hạn.

### 1.5.2 Phạm vi nghiên cứu

**Về bài toán,** chúng tôi chỉ xét trường hợp một màn hình: đầu vào là một ảnh chụp màn hình kèm một mục tiêu, và đầu ra là hướng dẫn cho bước kế tiếp. Trường hợp nhiều màn hình liên tiếp nằm ngoài phạm vi.

**Về độ đo,** đề tài tập trung đánh giá một khía cạnh của câu hướng dẫn, đó là câu sinh ra có giúp người dùng xác định đúng phần tử cần chạm trên màn hình hay không. Các khía cạnh khác như độ trôi chảy của câu, độ dài câu hay mức độ hữu ích đối với người đọc chưa được độ đo này xét tới.

**Về dữ liệu,** thực nghiệm chạy trên AndroidControl với giao diện tiếng Anh. Đề tài không dựng bộ dữ liệu tiếng Việt; các câu ví dụ tiếng Việt trong bài chỉ để minh hoạ.

**Về mô hình,** mọi mô hình trong đề tài đều được tinh chỉnh từ cùng một mô hình gốc Qwen2.5-VL-3B-Instruct [34] bằng QLoRA [30] hoặc LoRA trên một GPU. Việc huấn luyện mô hình từ đầu, cũng như so sánh nhiều mô hình gốc khác nhau, nằm ngoài phạm vi.

## 1.6 Đóng góp của luận văn

Đề tài có ba đóng góp, trong đó đóng góp chính là phương pháp đề xuất, xây dựng trên một quy trình dựng dữ liệu hoàn toàn tự động và gồm hai thành phần nối tiếp, một là mô hình học với thưởng SPICE, hai là ACE. Hai đóng góp còn lại hỗ trợ cho phương pháp này. Đóng góp thứ hai thuộc về đo lường, gồm độ đo dùng để chấm phương pháp đề xuất cùng mọi mô hình khác và việc kiểm chứng chính độ đo đó. Đóng góp thứ ba là chuỗi phân tích rút ra từ những hướng đã thử trước phương pháp đề xuất; các phân tích này làm rõ nguyên nhân chính cản trở điểm số và là căn cứ để chọn phương pháp.

**Đóng góp thứ nhất, về phương pháp.** Ý tưởng của phương pháp đề xuất là tác động thẳng vào câu ở đầu ra, thay vì vào một bước trung gian giữa ảnh và câu như các hướng đã thử trước đó. Phương pháp được xây dựng trên mô hình Qwen2.5-VL-3B tinh chỉnh có giám sát (S1). Mô hình này học từ một tập giám sát 64.567 bước do chúng tôi dựng hoàn toàn tự động, có kiểm tra độ chính xác của dữ liệu đa nguồn và kiểm tra trùng lặp dữ liệu đánh giá giữa tập huấn luyện và tập kiểm tra (Chương 3). Trừ khi nói khác, các con số dưới đây đo bằng executability, độ đo của đề tài trình bày ở đóng góp thứ hai. Mô hình tinh chỉnh có giám sát đạt 59,1% theo executability, so với 47,6% của mô hình gốc (chưa tinh chỉnh).

Mỗi thành phần tận dụng một nguồn thông tin khác nhau. Thành phần thứ nhất, gọi là mô hình học với thưởng SPICE, học tiếp từ mô hình tinh chỉnh có giám sát bằng học tăng cường theo nhóm (GRPO), với phần thưởng là SPICE của câu sinh ra so với câu chuẩn. Riêng thành phần này đạt 60,6% theo executability, cao nhất trong số các cách làm chỉ dùng một mô hình sinh câu, và hơn mô hình tinh chỉnh có giám sát 1,55 điểm, với khoảng tin cậy 95% là [+0,80; +2,33]. Mức hơn vẫn đứng khi so với cả hai hạt giống của mô hình tinh chỉnh có giám sát, và xuất hiện ở cả mười ba độ đo đã dùng (sáu độ đo vị trí và bảy độ đo so câu). Các hướng đã thử trước đó chỉ hơn mô hình tinh chỉnh có giám sát có ý nghĩa thống kê dưới những luật chấm lỏng hơn, còn thành phần thứ nhất thì hơn có ý nghĩa ngay theo executability, luật chấm chặt nhất. Hơn một nửa mức tăng đến từ việc định vị đúng phần tử ở những bước cả hai mô hình đều đã gọi đúng loại thao tác.

Thành phần thứ hai, ACE (luật chép câu ví dụ khi đồng thuận loại thao tác), tận dụng hơn sáu mươi nghìn câu chuẩn của tập huấn luyện: một bộ sinh câu được cho xem bốn câu chuẩn của những bước giống nhất, gọi là câu ví dụ. Câu của bộ sinh chỉ thay câu nháp khi câu ấy chép nguyên văn một trong bốn câu ví dụ và cùng loại thao tác với câu nháp; ở các bước còn lại, câu nháp được giữ nguyên. Với cả hai thành phần, phương pháp đề xuất đạt 60,7% theo executability, hơn mô hình tinh chỉnh có giám sát 1,57 điểm [+0,86; +2,31]. So với câu nháp, phương pháp giữ nguyên mức của ba độ đo vị trí (executability, luật hộp phần tử và luật khoảng cách Euclid của AndroidInTheWild) và nâng cả bảy độ đo so câu, rõ nhất ở CIDEr-D (+11,98) và SPICE (+1,34). Điều kiện đồng thuận về loại thao tác là cần thiết, vì nếu dùng câu của bộ sinh ở mọi bước thì executability giảm có ý nghĩa (Mục 6.4). Bộ sửa câu theo vùng cắt (TAGE), một cách sửa câu khác ở cùng khâu này, cho điểm thấp hơn câu nháp trên tập kiểm tra nên không được giữ (Mục A.7.2).

**Đóng góp thứ hai, về độ đo.** Để đánh giá phương pháp đề xuất cùng mọi mô hình khác, chúng tôi đề xuất và kiểm chứng executability, một độ đo khả năng xác định phần tử của câu hướng dẫn giao diện. Phần kiểm chứng gồm sáu phép đo ở Chương 5. Sai số của mô hình định vị nhỏ hơn nhiều so với khoảng cách giữa các phần tử trên màn (Mục 5.4), và luật xác định trúng được chọn theo ngưỡng tối thiểu đo được, tức số điểm một câu sai vẫn nhận được (Mục 5.2). Ở hai đầu của dải điểm, câu chuẩn (ngưỡng tối đa) đạt 75,7%, còn câu chung chung hay câu của một màn hình khác chỉ đạt ngưỡng tối thiểu thấp (Mục 5.5 và Mục 5.6). Độ đo còn được kiểm bằng mười kiểu cố ý chèn lỗi vào câu theo phương pháp của Sai và cộng sự (Mục 5.7). Khi câu chuẩn được viết lại, độ đo giữ ổn định trước việc đổi động từ hay đảo trật tự câu nhưng vẫn giảm điểm khi mệnh đề vị trí bị lược bỏ (Mục 5.8). Khi chấm lại bằng một mô hình định vị thứ hai không dùng AndroidControl khi huấn luyện, chênh lệch giữa mô hình tinh chỉnh có giám sát và mô hình gốc vẫn giữ gần nguyên độ lớn (Mục 5.9). Ngoài ra, khi chấm bằng một mô hình ngoài họ Qwen-VL (họ của mô hình được chấm và của cả hai mô hình định vị) làm người nghe, tức đọc câu rồi chọn phần tử đúng trong một danh sách ứng viên đánh số, thứ tự xếp hạng các mô hình được chấm vẫn giữ nguyên (Mục 5.10).

**Đóng góp thứ ba, về phân tích các hướng đã thử.** Trước khi đi tới phương pháp đề xuất, chúng tôi đã thử nhiều hướng, phần lớn tác động vào một bước trung gian giữa ảnh và câu. Hướng thứ nhất là mô hình mô tả phần tử, tức cho mô hình viết một dòng mô tả phần tử cần chạm rồi mới viết câu hướng dẫn. Hai giai đoạn huấn luyện tiếp theo được xây trên mô hình này. Ở giai đoạn học ưu tiên trên dòng mô tả, mô hình học từ những cặp chuỗi chỉ khác nhau ở dòng mô tả. Ở giai đoạn thưởng tọa độ (giai đoạn ba), mô hình học tăng cường với phần thưởng đặt chủ yếu vào tọa độ ghi trong dòng mô tả. Ngoài ra còn có mô hình chọn ứng viên, tức chọn phần tử cần chạm trong một danh sách dựng sẵn từ màn hình, và bốn cách đưa thêm thông tin vị trí vào bộ sinh câu. Từ phân tích các hướng này, chúng tôi rút ra ba kết luận. Thứ nhất, những thay đổi ở bước trung gian chỉ chuyển sang câu ở đầu ra rất ít. Khi dòng mô tả do mô hình viết trỏ đúng phần tử thì câu tốt hơn rõ so với mô hình tinh chỉnh có giám sát, còn khi dòng mô tả trỏ sai thì câu kém hơn nhiều, và hai phần này gần như triệt tiêu nhau. Thứ hai, phần lớn khoảng cách executability còn lại giữa mô hình và câu chuẩn dồn vào khoảng một phần ba số bước, là những bước mà mô hình đã chọn sai phần tử ngay trong dòng mô tả, nên khâu nhận ra phần tử chính là rào cản lớn nhất. Khi gắn thêm thông tin vị trí vào bộ sinh câu, thông tin ấy được học và đọc lại được từ trạng thái ẩn của mô hình, nhưng phần sinh câu bỏ qua thông tin ấy. Thứ ba, khi ước lượng mức tăng tối đa (ngưỡng tối đa) của một can thiệp trên một nhóm bước được chọn theo hành vi của chính mô hình đang đo, cần kiểm lại với ít nhất một cách chọn nhóm khác, vì trong đề tài đã có một ngưỡng tối đa như vậy đổi dấu khi đổi cách chọn nhóm. Các kết luận này là căn cứ để phương pháp đề xuất tác động thẳng vào câu ở đầu ra. Mục 6.10 tóm tắt các hướng này trong một bảng, còn Phụ lục A trình bày thiết kế và kết quả chi tiết của từng hướng.


# Chương 2. Tổng quan

Chương này trình bày những kiến thức nền cho phần còn lại của đề tài. Lần lượt các mục sẽ giới thiệu kiến trúc mô hình được sử dụng, kỹ thuật tinh chỉnh trong điều kiện tài nguyên hạn chế, học tăng cường với phần thưởng tính bằng luật, bài toán định vị phần tử giao diện và bộ dữ liệu nguồn. Mục cuối cùng giải thích lý do các độ đo sẵn có khó dùng cho bài toán này, kèm số đo cho từng cách. Hai mục về tinh chỉnh hiệu quả tham số và về học tăng cường (GRPO với phần thưởng SPICE) là nền trực tiếp của phương pháp đề xuất ở Chương 4.

## 2.1 Từ học sâu tới mô hình thị giác và ngôn ngữ

Học sâu là một lĩnh vực của học máy, dùng mạng nơ-ron nhiều tầng để tự học biểu diễn từ dữ liệu thô. Bước tiến liên quan trực tiếp nhất tới đề tài là kiến trúc Transformer với cơ chế tự chú ý [32]. Cơ chế này cho phép mô hình ước lượng quan hệ giữa các đơn vị trong chuỗi mà không phụ thuộc vào khoảng cách vị trí, đồng thời tận dụng được tính toán song song để mở rộng quy mô tham số.

Mô hình thị giác và ngôn ngữ (*vision-language model*, VLM) ghép một bộ mã hoá ảnh vào một mô hình ngôn ngữ, thường thông qua một tầng chiếu (*projector*) đưa đặc trưng ảnh về cùng không gian với nhúng từ. Ảnh được cắt thành nhiều mảnh, mã hoá thành một dãy *token thị giác* rồi nối vào chuỗi văn bản, nhờ đó mô hình có thể sinh văn bản dựa trên cả hai phương thức.

Mô hình gốc được chọn là Qwen2.5-VL-3B-Instruct [34], với ba lý do. Trước hết, đây là mô hình mở, có thể tải trọng số về và tinh chỉnh, khác với các mô hình thương mại chỉ gọi được qua giao diện lập trình. Kế đến, cỡ ba tỉ tham số đủ nhỏ để chạy trên máy người dùng, phù hợp với động lực ứng dụng đã nêu ở Chương 1. Cuối cùng, họ Qwen-VL xử lý ảnh ở độ phân giải động thay vì ép ảnh về một kích thước cố định. Cách xử lý này đặc biệt có ích với ảnh màn hình điện thoại vốn có tỉ lệ rất dài, ví dụ như 1080 × 2400.

## 2.2 Tinh chỉnh hiệu quả tham số bằng LoRA và QLoRA

Tinh chỉnh toàn bộ ba tỉ tham số đòi hỏi bộ nhớ vượt xa khả năng của một GPU, vì ngoài trọng số còn phải lưu gradient và trạng thái của bộ tối ưu. LoRA [29] giải quyết vấn đề này bằng cách đóng băng trọng số gốc $W \in \mathbb{R}^{d \times k}$ và chỉ học thêm một số hạng hạng thấp:

$$
W' = W + \frac{\alpha}{r}BA, \qquad B \in \mathbb{R}^{d \times r},\ A \in \mathbb{R}^{r \times k},\ r \ll \min(d,k),
\tag{2.1}
$$

trong đó $r$ là hạng và $\alpha$ là hệ số tỉ lệ. Nhờ vậy, số tham số cần học giảm từ $dk$ xuống còn $r(d+k)$.

QLoRA [30] đi thêm một bước: trọng số đóng băng được lượng tử hoá xuống 4 bit theo định dạng NormalFloat (NF4), rồi các bộ chuyển đổi LoRA mới được gắn lên trên. Trọng số gốc chỉ được giải nén khi cần cho phép nhân, còn gradient chỉ đi qua hai ma trận A, B ở độ chính xác cao.

Với cấu hình ở Bảng 4.1, các bộ chuyển đổi LoRA được gắn vào bảy mô-đun ở mỗi tầng trong 36 tầng, cho tổng cộng 14.966.784 tham số học được.

## 2.3 Học tăng cường với phần thưởng tính bằng luật

Học có giám sát dạy mô hình chép lại một chuỗi đích cho trước, tức đầu ra mẫu đã có sẵn, nhưng không cho mô hình biết câu nào tốt hơn trong số những câu mà chính mô hình có thể viết ra. Học tăng cường bổ sung phần còn thiếu này: mô hình tự sinh câu trả lời, một hàm thưởng chấm từng câu, và trọng số được điều chỉnh dần về phía những câu được thưởng cao. Khi hàm thưởng là một luật tính được, chẳng hạn như so một tọa độ với đáp án hay tính một độ đo so câu, cách làm này thường được gọi là học tăng cường với phần thưởng kiểm chứng được. Công trình DeepSeek-R1 trên *Nature* [42] là bản mô tả đầy đủ nhất của hướng này đối với mô hình ngôn ngữ lớn.

Thuật toán học tăng cường dùng trong đề tài, kể cả ở thành phần thứ nhất của phương pháp đề xuất, là tối ưu chính sách tương đối theo nhóm (GRPO), do công trình DeepSeekMath [43] giới thiệu. Với mỗi câu nhắc $x$, mô hình sinh một nhóm $G$ câu trả lời $y_1, \ldots, y_G$ và nhận các điểm thưởng $r_1, \ldots, r_G$. Lợi thế của câu thứ $i$ được tính bằng cách chuẩn hoá trong nhóm,

$$
\hat{A}_i = \frac{r_i - \operatorname{mean}(r_{1:G})}{\operatorname{std}(r_{1:G})},
\tag{2.2}
$$

sau đó mỗi token của $y_i$ được cập nhật theo $\hat{A}_i$, cùng với một số hạng phạt độ lệch Kullback–Leibler (KL) so với một mô hình tham chiếu đóng băng để mô hình không trôi quá xa điểm xuất phát. Ưu điểm của cách chuẩn hoá này là không cần một mô hình phê bình riêng để ước lượng mức thưởng kỳ vọng, nhờ đó tiết kiệm bộ nhớ. Đi kèm là một hạn chế có thể thấy ngay từ công thức: khi mọi câu trong nhóm nhận cùng một điểm thì $\hat{A}_i = 0$ với mọi $i$, và nhóm đó không đóng góp gradient nào. Hiện tượng này xuất hiện lại ở Mục 6.3, khi phần thưởng là một độ đo so câu.

**SPICE.** Trong số các độ đo so câu với câu chuẩn nêu ở Mục 2.6, SPICE [24] là độ đo mà Zhao và cộng sự [37] khuyên dùng để xếp hạng các mô hình sinh chỉ dẫn khi có câu tham chiếu. Thay vì so chuỗi từ, SPICE phân tích cả hai câu thành đồ thị cảnh gồm đối tượng, thuộc tính và quan hệ, rồi tính F1 trên các bộ ba trùng nhau. Với câu hướng dẫn giao diện, đối tượng thường là tên phần tử (“search icon”) và quan hệ thường là vị trí (“at the top”), nên SPICE nhạy với tên và vị trí của phần tử hơn là với động từ hay trật tự câu. Executability, độ đo của đề tài (Chương 5), cũng quan tâm đúng hai loại thông tin này, vì độ đo ấy tính tỉ lệ câu dẫn được một mô hình định vị độc lập tới đúng phần tử cần chạm. Trong phương pháp đề xuất, SPICE được dùng làm phần thưởng cho thành phần thứ nhất, và mô hình huấn luyện theo cách này được gọi là mô hình học với thưởng SPICE (Mục 4.5). Dù vậy, mọi kết luận vẫn được đọc trên executability.

## 2.4 Định vị phần tử giao diện

Bài toán định vị phần tử giao diện (*GUI grounding*) nhận một ảnh màn hình và một biểu thức văn bản, rồi trả về vị trí của phần tử được mô tả, thường dưới dạng một điểm hoặc một khung bao. Các mô hình tiêu biểu gồm SeeClick [3], OS-Atlas [4] và UGround [5].

Quy ước chấm phổ biến bắt nguồn từ mã chấm gốc của AndroidInTheWild [2]. Theo mã ấy, một lần chạm dự đoán được coi là khớp với lần chạm đáp án khi khoảng cách giữa hai điểm, tính trên tọa độ đã chuẩn hoá theo kích thước màn hình, không vượt quá 0,14, hoặc khi cả hai điểm cùng nằm trong một khung phần tử đã được nới rộng. Chúng tôi gọi đây là *luật khoảng cách Euclid của AndroidInTheWild*. Độ đo của đề tài dùng một biến thể đơn giản hơn, với cửa sổ ±14% theo từng trục (Mục 5.1), còn luật gốc được áp lại đầy đủ ở Mục 5.12. Mục 5.2 cho thấy luật khoảng cách Euclid khá lỏng khi đối tượng được chấm là câu chữ, vì luật này vốn được đặt ra để chấm một bộ định vị.

Trong đề tài, một mô hình thuộc nhóm này chỉ được dùng làm công cụ đo, không nằm trong số các mô hình được đánh giá; ba điều kiện đặt ra cho công cụ ấy được nêu ở Mục 5.3.

## 2.5 Bộ dữ liệu AndroidControl

AndroidControl [1] do nhóm Google DeepMind công bố tại NeurIPS 2024 theo giấy phép CC0, gồm 15.283 chuỗi thao tác do người thật thực hiện trên thiết bị Pixel trong khoảng một năm. Mỗi bước lưu ảnh màn hình, loại thao tác, tọa độ chạm nếu có, và quan trọng nhất đối với đề tài là trường `step_instructions`, tức câu hướng dẫn do chính người thao tác viết cho bước đó.

> **Vị trí của đề tài so với các công trình dùng bộ dữ liệu này.** Trong bài gốc AndroidControl cũng như trong các công trình dùng bộ dữ liệu này mà chúng tôi khảo sát (Aguvis [7], SeeClick [3]), câu hướng dẫn từng bước nằm ở đầu vào, giúp tác tử suy ra thao tác cần thực hiện. Ở đề tài này, câu đó lại là đầu ra mà mô hình phải sinh, và chỉ câu này được chấm điểm, nên dữ liệu được dùng theo chiều ngược lại.

Câu chuẩn của bộ dữ liệu rất ngắn, trung vị chỉ khoảng sáu từ, có dạng như “click on OK” hay “Select the search result”. Câu càng ngắn thì mô hình định vị càng khó xác định phần tử, và đây là một lý do khiến ngưỡng tối đa đo được, tức executability của chính câu chuẩn, chỉ đạt 75,7% (Mục 5.5). Mọi kết quả của đề tài đều chịu giới hạn của ngưỡng tối đa này.

## 2.6 Giới hạn của các độ đo có sẵn

Vì bài toán đã có sẵn câu chuẩn, cách làm trực tiếp nhất là so câu sinh ra với câu chuẩn. Chúng tôi đã thử hai nhóm phương pháp theo hướng này và đo lại mức hạn chế của từng nhóm, kết quả được tóm tắt ở Bảng 2.1.

**Bảng 2.1.** Hai cách chấm dựa trên câu chuẩn, và mức độ thất bại đo được trên dữ liệu thật của bài toán.

| Cách chấm | Kết quả đo | Nguyên nhân thất bại |
|---|---|---|
| So chuỗi | loại nhầm 97,5% số câu diễn đạt khác | “search bar” và “magnifying glass” không chung từ nào |
| So vector ngữ nghĩa | AUC 0,336 trên 51 ca viết tay | do độ gần chủ đề, nên cặp `inbox` và `outbox` được 0,76, cao hơn cặp `search` và `magnifying glass` chỉ 0,55 |

Ở dòng thứ hai, diện tích dưới đường ROC (AUC) chỉ đạt 0,336, thấp hơn cả mức đoán ngẫu nhiên 0,5, và kết quả này đi ngược một trực giác khá phổ biến. Nhúng ngữ nghĩa được huấn luyện để đặt gần nhau những đoạn văn cùng chủ đề. “Hộp thư đến” và “hộp thư đi” cùng nói về thư từ nên nằm gần nhau, dù trên màn hình chúng là hai nút khác nhau. Ngược lại, “thanh tìm kiếm” và “kính lúp” nói về hai đối tượng khác nhau (một là ô nhập, một là hình vẽ), trong khi thật ra chúng là cùng một nút. Độ đo cần biết hai câu có cùng chỉ một phần tử hay không, còn nhúng ngữ nghĩa chỉ cho biết hai câu gần nhau về chủ đề đến mức nào. Hai tín hiệu này không đi cùng chiều, nên không có ngưỡng điểm nào tách được trường hợp cùng phần tử với trường hợp khác phần tử.

Vì vậy, các độ đo dựa trên tiêu chí “câu sinh ra giống câu chuẩn” khó cho kết quả đáng tin với bài toán này, và Chương 5 xây dựng một độ đo theo tiêu chí khác.

# Chương 3. Xây dựng bộ dữ liệu

Hiện chưa có bộ dữ liệu công khai nào được dựng sẵn cho tác vụ “nhìn một màn hình rồi viết một câu hướng dẫn cho người đọc”. Chương này trình bày cách chuyển bộ dữ liệu AndroidControl thành tập dữ liệu có nhãn để huấn luyện có giám sát cho tác vụ này. Toàn bộ quá trình được tự động hoá, không thuê người gán nhãn thêm và cũng không đưa vào huấn luyện nhãn do một mô hình ngôn ngữ khác sinh ra.

Để các chương sau có thể dùng thẳng tên gọi kỹ thuật mà người đọc vẫn dễ theo dõi, Bảng 3.1 nối ba khái niệm ở tên đề tài với các đối tượng cụ thể được dùng trong chương này.

**Bảng 3.1.** Ba khái niệm trong tên đề tài và dạng cụ thể của từng khái niệm khi triển khai.

| Khái niệm | Dạng cụ thể trong đề tài |
|---|---|
| Trường hợp sử dụng | Mục tiêu của cả tác vụ, ví dụ như đặt vé xem phim cho tối nay, cùng chuỗi các bước đã thực hiện trước bước đang xét |
| Giao diện người dùng | Ảnh chụp màn hình đang mở, chuỗi chữ đọc được trên màn, và ở khâu dựng dữ liệu còn có cây trợ năng của chính màn hình ấy |
| Hướng dẫn sử dụng | Câu hướng dẫn cho bước kế tiếp; các câu của cùng một tác vụ nối lại theo thứ tự bước thành hướng dẫn đầy đủ cho tác vụ đó |

Mô hình sinh câu và được chấm điểm dựa trên từng bước riêng lẻ, thay vì tạo một tài liệu hướng dẫn hoàn chỉnh, vì hai lý do. Thứ nhất, nhãn tham chiếu của AndroidControl vốn được viết theo từng bước, nên việc đối chiếu với câu chuẩn chỉ khả thi ở phạm vi này. Thứ hai, độ đo ở Chương 5 đánh giá khả năng của mỗi câu trong việc dẫn dắt một mô hình định vị độc lập tìm ra đúng phần tử cần chạm. Vì tài liệu hướng dẫn cho cả tác vụ được ghép lại từ các câu này (Bảng 3.1), chất lượng tổng thể phụ thuộc trực tiếp vào độ chính xác của từng câu riêng biệt.

Phương pháp đề xuất (Mục 4.4) sử dụng ba phần của dữ liệu được chuẩn bị ở chương này. Phần thứ nhất là tập giám sát 64.567 bước, dùng để huấn luyện mô hình tinh chỉnh có giám sát (S1), tức điểm xuất phát của phương pháp. Ở tập này, mô hình chỉ tập trung học cách sinh câu hướng dẫn. Phần thứ hai là các câu nhắc được lấy từ tập huấn luyện sau khi đã loại bỏ tập kiểm định nội bộ (Mục 3.3), dùng để dạy tăng cường cho mô hình học với thưởng SPICE. Phần thứ ba là câu chuẩn thuộc cùng tập huấn luyện trên, đóng vai trò như một kho truy hồi câu ví dụ cho ACE, tức thành phần có luật sao chép câu ví dụ khi đồng thuận loại thao tác. Nhãn mô tả, tập cặp và danh sách ứng viên, trình bày từ Mục 3.5 trở đi, là phần dữ liệu phục vụ cho các hướng đã thử và chỉ được dùng trong Phụ lục A.

## 3.1 Nguồn dữ liệu và quá trình ghép đa nguồn

Mỗi bước đều yêu cầu ba thành phần: câu hướng dẫn do người chú thích viết, ảnh chụp màn hình và cây trợ năng. Tuy nhiên, không có bản phân phối công khai nào của AndroidControl cung cấp đủ cả ba, nên chúng tôi phải ghép hai bản lại với nhau (Bảng 3.2).

**Bảng 3.2.** Hai bản phân phối trên Hugging Face và phần thiếu của mỗi bản.

| Bản phát hành | Có | Thiếu |
|---|---|---|
| `HarrytheOrange/parsed_AndroidControl` | câu hướng dẫn đủ 15.283 chuỗi | không có ảnh |
| `ckg/AndroidControlParsedWithImages-20k` | ảnh màn hình | mất câu hướng dẫn |

Hai bản phát hành được ghép theo khoá `(episode_id, step_id)`, tức cặp mã tác vụ và số thứ tự bước. Cây trợ năng của 99.131 màn được lấy từ chính bản phát hành gốc.

Có một tính chất của bản phân phối ảnh hưởng tới cách đọc kết quả. Chuỗi mục tiêu, tức câu mô tả mục tiêu chung của cả tác vụ, đã bị cắt ngay từ nguồn: 99,0% số chuỗi kết thúc giữa chừng một cụm từ, ví dụ như `...look for Calvin Kle`. Vì mọi mô hình được huấn luyện đều đọc cùng một chuỗi mục tiêu đã bị cắt, việc cắt này không thể giải thích chênh lệch giữa các mô hình. Tuy vậy, câu chuẩn được viết độc lập với chuỗi mục tiêu bị cắt, còn mô hình phải dựa vào chuỗi ấy để viết câu, nên khoảng cách giữa mô hình và câu chuẩn có phần bị ước lượng cao hơn thực tế.

## 3.2 Kiểm tra tính chính xác của quá trình ghép dữ liệu

Lỗi đáng ngại nhất của quy trình là ghép lệch một bước, khiến mô hình học ảnh của bước A với câu của bước B. Lỗi này không tự bộc lộ ở khâu nào, vì số dòng dữ liệu vẫn đủ và huấn luyện vẫn hội tụ.

Việc kiểm tra này dựa trên chữ đọc được ngay tại điểm chạm. Chúng tôi chạy nhận dạng chữ quang học (OCR) tại điểm chạm đúng của bước, rồi kiểm tra xem chuỗi chữ thu được có xuất hiện trong câu hướng dẫn hay không. Nếu quá trình ghép chính xác, tỉ lệ khớp sẽ cao hơn hẳn so với một dữ liệu ghép cố ý làm lệch đi một bước. Trên n = 400 bước lấy mẫu, hai tỉ lệ đo được như sau.

|  | Ghép đúng | Ghép lệch một bước (đối chứng) |
|---|---:|---:|
|  | 48% | 20% |
| Tỉ số | 2,4× |  |

Hai tỉ lệ cách nhau 2,4 lần và hai khoảng tin cậy không giao nhau. Tỉ lệ 48% tự nó chưa đủ để khẳng định kết quả ghép là đúng hay sai, và chỉ có ý nghĩa khi đặt cạnh mức 20% của dữ liệu ghép lệch dùng làm đối chứng. Mọi kết quả ghép về sau đều được kiểm tra theo cùng phương pháp này.

## 3.3 Quy mô, cách chia tập và kiểm tra dữ liệu đánh giá

**Bảng 3.3.** Quy mô hai tập sau khi dựng.

|  | Tập huấn luyện | Tập kiểm tra |
|---|---:|---:|
| Số bước | 64.567 | 6.958 |
| Bước chạm (tập bước được chấm) | 41.191 (63,8%) | 4.463 (64,1%) |
| Số tác vụ | 12.895 | 1.432 |
| Độ phủ OCR | 100% | 100% |
| Độ phủ nhãn mô tả trên bước chạm | - | 99,7% |

Dữ liệu được chia thành tập huấn luyện và tập kiểm tra theo tác vụ, tức mỗi bước của cùng một tác vụ đều nằm trong cùng một tập, thay vì chia ngẫu nhiên theo từng bước. Các màn hình trong cùng một tác vụ thường gần như trùng nhau, nên nếu chia ngẫu nhiên, dữ liệu huấn luyện sẽ lẫn sang tập kiểm tra và làm điểm số cao hơn thực tế. Việc kiểm tra trùng lặp dữ liệu đánh giá đối chiếu toàn bộ tác vụ của hai tập (Bảng 3.3) và không tìm thấy tác vụ nào trùng.

**Quan hệ với cách chia chính thức của AndroidControl.** Cách chia tập huấn luyện và tập kiểm tra ở đây lấy sẵn từ bản phân phối có ảnh của `ckg`, vốn là một phép chia ngẫu nhiên theo tác vụ. Cách chia này không trùng với phần kiểm tra chính thức mà nhóm tác giả AndroidControl công bố [1]. Khi đối chiếu với tệp chia chính thức, chúng tôi thấy 1.287 trong 1.432 tác vụ của tập kiểm tra, tức khoảng 90%, thuộc phần huấn luyện chính thức; chỉ 131 tác vụ thuộc phần kiểm tra và 14 tác vụ thuộc phần kiểm định. Phân bố này đúng như kỳ vọng khi tập kiểm tra được chọn ngẫu nhiên theo tác vụ. Vì tập huấn luyện và tập kiểm tra của đề tài vẫn rời nhau theo tác vụ, các phép so giữa các mô hình không bị ảnh hưởng, chỉ có tên gọi của tập kiểm tra là phải đổi. Chúng tôi gọi tập này là *tập kiểm tra giữ riêng theo tác vụ* thay vì phần kiểm tra chính thức của AndroidControl. Ảnh hưởng của việc lệch cách chia này đối với mô hình định vị dùng làm công cụ đo được xem xét ở Mục 5.3.

**Tập kiểm định nội bộ.** Để chọn điểm lưu (bản trọng số được lưu lại giữa chừng huấn luyện), chọn luật và đánh giá các biến thể với nhau mà không phải dùng đến tập kiểm tra, chúng tôi tách thêm một tập kiểm định nội bộ gồm 1.567 bước khỏi tập huấn luyện, cũng chia theo tác vụ. Điểm lưu của mô hình học với thưởng SPICE và luật chọn câu của ACE đều được quyết định dựa trên tập này (Mục 4.5 và Mục 4.6). Các phép so sánh ở Chương 6 dùng các tập con từ 400 đến 960 bước lấy từ tập kiểm định này. Các mô hình được huấn luyện sau khi tách tập này chỉ học trên 63.000 bước còn lại. Riêng mô hình tinh chỉnh có giám sát (S1) đã được học trên toàn bộ 64.567 bước. Do đó, đối với mô hình S1 và mọi mô hình học tiếp từ nó (kể cả hai thành phần của phương pháp đề xuất), tập kiểm định nội bộ là phần dữ liệu đã nhìn thấy. Vì vậy, chúng tôi chỉ dùng tập này để xếp hạng các biến thể và không dùng bất kỳ điểm tuyệt đối nào trên tập này làm kết quả chính thức; mức lạc quan của tập này so với tập kiểm tra được đo lường cụ thể ở Mục A.4.3.

Ba tính chất khác của cách chia này giới hạn phạm vi của kết luận.

**Trùng lặp cách diễn đạt giữa hai tập.** Chỉ cần so với một mẫu lấy từ tập huấn luyện, đã có 17,3% số câu chuẩn trong tập kiểm tra xuất hiện nguyên văn ở mẫu đó, và 66,5% dùng chung ít nhất một cụm bốn từ liên tiếp. Nguyên nhân là bộ dữ liệu có xu hướng lặp lại nhiều lần các cách diễn đạt như “click on the search bar”. Bước đánh giá ở Mục 6.8 tách riêng những câu mà mô hình sinh giống hệt câu chuẩn tương ứng, nhưng không loại trừ hoàn toàn được hiện tượng này. Thành phần ACE của phương pháp đề xuất chủ yếu dựa vào tính lặp lại này khi sao chép nguyên văn câu ví dụ từ tập huấn luyện (Mục 4.6).

**Mức trùng lặp ứng dụng giữa hai tập.** Trong số các bước của tập kiểm tra gán được tên ứng dụng, 95,6% (2.991/3.130 bước) thuộc về những ứng dụng đã từng xuất hiện ở tập huấn luyện. Nếu đếm theo từng ứng dụng thay vì từng bước, tỉ lệ này là 91,8% (247/269 ứng dụng). Các phép so sánh nội bộ giữa các mô hình không bị ảnh hưởng, do mọi mô hình đều sử dụng chung dữ liệu huấn luyện, mô hình gốc và tập kiểm tra. Tuy nhiên, nếu so sánh thẳng với một hệ thống bên ngoài chưa từng thấy các ứng dụng này, kết quả sẽ nghiêng về phía mô hình của đề tài. Do vậy, chúng tôi không trình bày phép so sánh nào thuộc loại này như một kết quả độc lập. Tác động cụ thể của việc trùng lặp ứng dụng sẽ được đo lường trực tiếp ở Mục 6.9.

**Các bước không thể xác định được ứng dụng.** Chỉ có 45,0% số bước trong tập kiểm tra có thể gán được tên ứng dụng (269 ứng dụng), trong khi 3.828 bước còn lại mang nhãn “không biết”. Nhãn này đơn thuần có nghĩa là không xác định được ứng dụng, khác với nhãn “chưa thấy” (ứng dụng không xuất hiện trong tập huấn luyện), nên chúng tôi không gộp hai nhóm này khi phân tích.

## 3.4 Trích xuất chữ trên màn hình

Chữ đọc được trên màn hình là nguồn thông tin thứ hai của mô hình sinh câu, sau ảnh màn hình. Kết quả OCR đóng vai trò là phần chữ trong câu nhắc, đồng thời cung cấp tên phần tử cho nhãn mô tả của các hướng đã thử (Mục 3.5).

Trung bình mỗi màn hình có 24,2 chuỗi chữ nhận dạng được ở tập kiểm tra và 23,6 ở tập huấn luyện. Giá trị trung vị ở hai tập bằng nhau, cho thấy chất lượng trích xuất chữ ở hai tập là tương đương.

Trên bộ dữ liệu này, chúng tôi quan sát được hai dạng lỗi phổ biến của OCR: biểu tượng bị nhận dạng nhầm thành ký tự, và mất khoảng trắng (ví dụ `Turnon` thay cho “Turn on”). Dạng lỗi thứ hai khiến phần tử bị xếp vào nhóm “không có tên” thay vì nhận một tên sai, nên nhãn chỉ bị thiếu sót thông tin chứ không hoàn toàn sai lệch.

## 3.5 Xây dựng nhãn mô tả tự động

Dữ liệu từ mục này trở đi, ngoại trừ tập giám sát của S1 được nhắc lại ở Mục 3.6, chỉ dành riêng cho các hướng đã thử ở Phụ lục A. Hướng đầu tiên là mô hình mô tả phần tử (Mục A.1.1). Trước khi viết câu, mô hình này được học cách viết ra một dòng có cấu trúc mô tả phần tử cần chạm, gọi là dòng mô tả phần tử. Dòng này được thiết lập hoàn toàn bằng luật, không cần sự can thiệp của con người.

Quy trình tạo dòng mô tả diễn ra như sau. Từ tọa độ chạm đáp án, chương trình tìm chọn hộp trợ năng (tức khung bao của một nút trong cây trợ năng) nhỏ nhất có chứa điểm đó. Vai trò của phần tử được trích xuất trực tiếp từ cây trợ năng. Tên phần tử cũng lấy từ cây nếu vượt qua được các bộ lọc hợp lệ mô tả ở phần dưới; nếu không, tên sẽ được lấy từ chữ OCR nằm bên trong hộp. Ô thứ ba của dòng ghi tọa độ, chính là điểm chạm đáp án sau khi quy về thang [0, 1000], còn ô thứ tư chứa một dấu hiệu phân biệt được tự động sinh ra theo luật định sẵn.

**Bảng 3.4.** Bốn ô của dòng mô tả phần tử và lý do cần có từng ô.

| Ô | Ví dụ | Lý do cần |
|---|---|---|
| Vai trò | `tappable text` | phân biệt nút, ô nhập, mục danh sách |
| Tên | `Search here` | chữ hiển thị; nguồn là OCR hoặc cây trợ năng |
| Tọa độ | `<point>440,91</point>` | nhãn sạch 100%, chi phí dựng bằng không |
| Dấu hiệu phân biệt | `just above the text “Coffee”` | mệnh đề tách phần tử này khỏi các phần tử giống nó, nhằm vào dạng lỗi “câu mơ hồ” |

**Làm sạch tên và ô dấu hiệu phân biệt.** Tên phần tử đi qua hai bộ lọc, vì nhãn trợ năng thô thường có nhiều lỗi. Bộ lọc nhãn trợ năng loại bỏ 14,7% nhãn tại các nút cần chạm, bao gồm các định danh lấy từ mã nguồn, chuỗi số dài, hậu tố dành cho trình đọc màn hình và những chuỗi chỉ báo phần tử không có nhãn, chẳng hạn như `No label specified`. Bộ lọc hình học chỉ cho phép lấy tên từ OCR khi hộp phần tử chiếm dưới 25% diện tích màn hình. Nguyên nhân là do trong số 25 trường hợp hộp chiếm gần hết màn hình được chúng tôi kiểm tra thủ công, không có trường hợp nào khớp với câu chuẩn. Ô dấu hiệu phân biệt được tạo theo các luật ưu tiên, ưu tiên cao nhất là dùng chữ làm mỏ neo, tức là tìm chuỗi OCR gần nhất nằm ngoài hộp kết hợp với vị trí tương đối. Trên mẫu thử, 75,9% số dấu hiệu được tạo ra tự thân chúng đã đủ để phân biệt phần tử cần chạm với các phần tử giống nó; 24,1% còn lại thì không thể, và tỉ lệ này được ghi nhận như một giới hạn tại Mục 7.2.

**Chất lượng nhãn ở quy mô đầy đủ.** Bảng 3.5 đối chiếu nhãn dựng cho 41.191 bước chạm với mẫu thử 1.074 nhãn dựng trước đó.

**Bảng 3.5.** Chất lượng nhãn mô tả ở quy mô đầy đủ so với mẫu thử (n = 1.074). Ở ba chỉ số có số đối chiếu, hai cột lệch nhau không quá 1,4 điểm, cho thấy quy trình không suy giảm khi mở rộng quy mô.

| Chỉ số | Quy mô đầy đủ | Mẫu thử |
|---|---:|---:|
| Tên rõ ràng | 73,6% | 73,8% |
| Chỉ có ký hiệu, không có chữ | 4,4% | - |
| Không có tên | 22,0% | 23,4% |
| Vai trò rõ ràng | 75,8% | - |
| Trùng tên trên cùng màn | 7,6% | 7,0% |
| Có phần tử cùng vai trò để so | 91,6% | - |

Trong 32.061 tên lấy được, 8.581 tên đến từ cây trợ năng và 23.480 tên đến từ OCR. Tỉ lệ này cho thấy nếu chỉ dựa vào cây trợ năng, quy trình sẽ mất khoảng ba phần tư số tên.

## 3.6 Bốn tập dữ liệu và các điều kiện cấu trúc bắt buộc

Từ cùng một đầu vào, chúng tôi dựng bốn tập dữ liệu chỉ khác nhau ở chuỗi mà mô hình phải sinh ra. Ở tập thứ nhất, chuỗi đích chỉ gồm câu hướng dẫn; đây là tập giám sát 64.567 bước dùng để huấn luyện mô hình tinh chỉnh có giám sát (S1), cũng là điểm xuất phát của phương pháp đề xuất. Ba tập còn lại chỉ phục vụ mô hình mô tả phần tử và hai cấu hình đối chứng của mô hình này ở Phụ lục A. Hai ví dụ dưới đây cùng lấy bước 1 của tác vụ mã 5590.

- **Tập của mô hình tinh chỉnh có giám sát (S1), chỉ có câu hướng dẫn**  
  `Click on the search bar`
- **Tập của mô hình mô tả phần tử (S2), dòng mô tả thật rồi mới tới câu**  
  `tappable text | Search here | 440,91 | just above the text “Coffee”`  
  `Click on the search bar`

Hai tập còn lại lấy nguyên câu của tập vừa nêu và chỉ thay dòng mô tả. Cấu hình mô tả giả (S2r) dùng dòng mô tả lấy từ một màn khác, với tọa độ ngẫu nhiên, nhằm loại trừ khả năng điểm tăng chỉ vì chuỗi đích dài hơn (Mục A.1.2); vì vậy mỗi dòng mô tả giả được chọn sao cho số token gần bằng dòng mô tả thật, và 99,9% số cặp lệch nhau không quá hai token. Cấu hình mô tả không có tọa độ (S2-nopoint) bỏ tọa độ và giữ ba ô còn lại của dòng mô tả.

**Chín điều kiện cấu trúc.** Sau mỗi lần tái cấu trúc dữ liệu, chúng tôi kiểm tra lại chín điều kiện bắt buộc mà bốn tập luôn phải thoả mãn; ở quy mô đầy đủ, cả chín điều kiện đều đạt. Ba điều kiện quan trọng nhất là: câu được chấm phải giống hệt nhau từng byte ở cả bốn tập trên 64.567 mẫu, tập của cấu hình mô tả giả chỉ khác tập của mô hình mô tả phần tử ở các dòng mô tả, và các bước không chạm phải có chuỗi đích y hệt nhau ở cả bốn tập. Bước không chạm, gồm thao tác cuộn, gõ, mở ứng dụng và quay lại, chiếm 36,2% tổng lượng dữ liệu. Nhờ điều kiện cuối cùng, nếu mô hình mô tả phần tử làm giảm chất lượng ở nhóm bước này thì sự suy giảm đó không thể quy cho khác biệt về mặt dữ liệu.

Dữ liệu của hai cấu hình mô tả giả và mô tả không có tọa độ đã được dựng đầy đủ nhưng không được huấn luyện; lý do được ghi ở Bảng 6.13.

## 3.7 Tập cặp quy chiếu tối thiểu cho giai đoạn học ưu tiên

Giai đoạn học ưu tiên trên dòng mô tả, gọi tắt là giai đoạn học ưu tiên (Mục A.2.1), học tiếp từ mô hình mô tả phần tử trên các cặp gồm vế được chọn (chuỗi mô hình nên ưu tiên) và vế bị loại (chuỗi mô hình nên tránh). Tập gồm 22.854 cặp, dựng từ các dòng mô tả đã có. Hai vế của mỗi cặp chỉ khác nhau ở dòng mô tả, còn phần câu giữ nguyên từng byte. Ở vế bị loại, dòng mô tả trỏ tới phần tử cùng vai trò nằm gần phần tử cần chạm nhất, và cặp chỉ được giữ khi hai phần tử cách nhau từ 80 đến 350 điểm ảnh và khác nhau ở cả tên lẫn tọa độ. Cận dưới loại những phần tử sát tới mức độ đo coi chúng là một nút, vì luật chấm gộp các phần tử có tâm cách nhau dưới khoảng 63 điểm ảnh (Mục 5.1); cận trên loại những phần tử quá xa, vốn rất dễ phân biệt nên ít mang lại tín hiệu cho quá trình huấn luyện. Sau khi dựng xong, chúng tôi kiểm tra lại chín điều kiện bắt buộc, trong đó quan trọng nhất là câu ở hai vế phải trùng nhau từng byte, vế bị loại không bao giờ được phép trỏ vào chính phần tử cần chạm, và tọa độ trong vế bị loại luôn là tọa độ thực của phần tử mà vế ấy nêu tên.

Tập cặp này có hai giới hạn ảnh hưởng đến mọi kết quả của giai đoạn học ưu tiên. Thứ nhất, tập chỉ chứa bước chạm, vì chỉ bước chạm mới có dòng mô tả; do đó điều kiện liên quan đến bước không chạm tại Mục 3.6 không áp dụng được, và phần sụt giảm điểm số ở bước không chạm sẽ được đánh giá riêng trong Mục A.2.2.4. Thứ hai, ở 17,4% số cặp, chuỗi `(no name)` (phần tử không có tên) chỉ xuất hiện ở một trong hai vế, nên mô hình có thể dễ dàng dựa vào chuỗi đó để phân biệt hai vế mà không cần xét đến nội dung màn hình. Hạn chế này được phát hiện sau khi mô hình đã học xong, do đó toàn bộ kết quả trình bày đều dùng dữ liệu chưa chỉnh sửa.

## 3.8 Danh sách ứng viên cho mô hình chọn ứng viên

Mô hình chọn ứng viên (Mục A.3.1) thay 24 dòng chữ OCR không kèm vị trí trong câu nhắc bằng một danh sách ứng viên gồm tối đa 40 dòng. Mỗi dòng là tên một phần tử trên màn kèm tọa độ trên lưới [0, 1000], viết đúng dạng `tên <point>x,y</point>` như cách ghi tọa độ trong dòng mô tả phần tử, để mô hình có thể chép trực tiếp sang đầu ra. Tên ứng viên được tạo bằng đúng quy tắc đặt tên của dòng mô tả ở Mục 3.5, nên mọi tên trong danh sách đều là chuỗi có thể xuất hiện trong dòng mô tả. Danh sách được sắp xếp theo thứ tự đọc tự nhiên (từ trên xuống, từ trái sang) và giới hạn ở tối đa 40 dòng. Cách sắp xếp và cắt bỏ này độc lập với phần tử cần chạm, đảm bảo danh sách không làm lộ vị trí của đáp án.

Gọi tên ghi trong dòng mô tả của một bước là **tên đúng** của bước ấy. **Ứng viên đúng** là dòng trùng tên đúng và cách điểm chạm không quá 140 đơn vị lưới (tức 14% màn) theo mỗi trục; khi nhiều dòng cùng thoả, dòng gần điểm chạm nhất được chọn. Trên tập kiểm tra, tên đúng có mặt trong danh sách ở 96,7% số bước có tên đúng, và ở 91,2% số bước ấy danh sách có một dòng vừa trùng tên đúng vừa nằm trong dung sai trên. Về khả năng lộ đáp án, trên 300 mẫu, ứng viên đúng nằm gần giữa danh sách (hạng chuẩn hoá về khoảng từ 0 đến 1 có trung bình 0,481) và chỉ đứng đầu ở 5,0% số mẫu, nên vị trí trong danh sách không tiết lộ đáp án. Mẫu dài nhất vẫn dưới giới hạn độ dài ngữ cảnh 3.072 token, nên không mẫu nào bị cắt.

Từ một câu nhắc đầu vào, chúng tôi tạo ra hai tập dữ liệu khác nhau ở chuỗi đích. Với mô hình chọn ứng viên, chuỗi đích luôn mở đầu bằng một thẻ chọn phần tử. Ngược lại, cấu hình đối chứng nhận cùng danh sách ứng viên ở đầu vào nhưng chuỗi đích chỉ chứa duy nhất câu hướng dẫn.

```text
Chọn ứng viên <sel>tên <point>x,y</point></sel> + \\ n + câu
hoặc <sel>none</sel> + \\ n + câu
Cấu hình đối chứng câu
```

Nội dung thẻ chọn là phần sao chép nguyên văn thông tin của ứng viên đúng từ danh sách. Thẻ `none` (từ chối chọn) được sử dụng cho các bước không chạm, bước chạm nhưng phần tử không có tên đúng, hoặc bước chạm có tên đúng nhưng không có dòng nào trong danh sách khớp với nó. Câu ở cả hai tập đều là câu chuẩn nguyên bản, nhằm đảm bảo chênh lệch giữa hai cấu hình chỉ đến từ cơ chế chọn. Chín điều kiện cấu trúc bắt buộc cũng được kiểm tra sau khi xây dựng và đều thoả mãn, trong đó có việc câu nhắc và ảnh của hai tập trùng nhau từng byte.

Vì mọi bước không chạm đều mang thẻ `none`, 54,78% số mẫu của tập huấn luyện mang thẻ này; nếu chỉ tính trên 41.191 bước chạm thì tỉ lệ là 29,12%. Mục A.3.2 dùng hai con số này để giải thích nguyên nhân xảy ra hiện tượng từ chối chọn, tức việc mô hình trả về thẻ `none` dù danh sách có chứa ứng viên đúng. Chúng tôi cũng chuẩn bị sẵn một tập lọc chỉ gồm 41.191 bước chạm, thoả mãn đủ chín điều kiện cấu trúc; tập này chưa được đưa vào huấn luyện, với lý do trình bày ở Mục A.3.2.

# Chương 4. Phương pháp tiếp cận

Chương này trình bày phương pháp đề xuất, là đóng góp chính của đề tài. Phương pháp gồm hai thành phần nối tiếp (Mục 4.4). Thành phần thứ nhất học tăng cường với phần thưởng SPICE và viết một câu nháp (Mục 4.5). Thành phần thứ hai, gọi là ACE (chép câu ví dụ khi đồng thuận loại thao tác), quyết định có thay câu nháp bằng một câu ví dụ truy hồi từ tập huấn luyện hay không (Mục 4.6). Trước phần phương pháp, chương trình bày quy trình chung, đầu vào và cấu hình huấn luyện chung cho mọi mô hình; sau phần phương pháp là các mốc so sánh và cách đọc kết quả. Các hướng đã thử trước phương pháp này được trình bày ở Phụ lục A. Độ đo dùng để chấm được trình bày riêng ở Chương 5.

## 4.1 Toàn bộ quy trình

*(Sơ đồ vẽ bằng TikZ, chỉ xem được trong bản PDF.)*

**Hình 4.1.** Bốn khâu của hệ thống. Chỉ khối tô xám, tức phương pháp đề xuất (Mục 4.4), được huấn luyện. Hai khối dưới thuộc phần đo lường và không được nhận tọa độ đáp án.

Hình 4.1 cũng cho thấy một thuận lợi khi triển khai. Khi đưa vào sử dụng, hệ thống chỉ cần bộ đọc chữ, mô hình đã tinh chỉnh và, với phương pháp đề xuất, kho câu chuẩn dùng để truy hồi câu ví dụ (Mục 4.6). Cây trợ năng và mô hình định vị chỉ có mặt ở khâu dựng dữ liệu và khâu chấm điểm, không tham gia vào luồng xử lý phục vụ người dùng.

## 4.2 Đầu vào và câu nhắc

Câu nhắc được ghép từ bốn phần và giống nhau đến từng ký tự ở mọi mô hình, kể cả lúc suy luận. Nhờ vậy, khi điểm của hai mô hình chênh nhau, phần chênh ấy có thể quy cho chỗ can thiệp riêng của từng bên. Riêng bộ sinh của ACE được chèn thêm khối câu ví dụ ngay trước dòng yêu cầu viết câu (Mục 4.6). Khối dưới đây minh họa cấu trúc của một câu nhắc.

```text
<image>
Mục tiêu: Open Google maps app, Search for the nearest
park to 98103 ...
Đã làm: Click on the title of this note Grocery to edit
the title
Chữ đọc được trên màn: Search here · Coffee ·
Restaurants · Groceries · ...
Viết câu hướng dẫn cho bước tiếp theo.
```

Các nhãn trường được viết bằng tiếng Việt, còn câu trả lời được yêu cầu viết bằng tiếng Anh, vì tiếng Anh là ngôn ngữ của bộ ngữ liệu nguồn và của mọi câu được chấm.

Đầu vào có thêm danh sách chữ đọc được trên màn, lấy bằng nhận dạng chữ quang học (OCR), để hạn chế một dạng lỗi đã đo được là gọi sai hoặc gọi mơ hồ tên nút. Việc đưa danh sách phần tử vào đầu vào đã có ở nhiều công trình trước (Chương 1), nên danh sách chữ OCR chỉ được xem là một lựa chọn thiết kế, không được tính là đóng góp.

Trường “Đã làm” chứa câu chuẩn của các bước trước, không lấy từ những câu mô hình đã sinh. Nhờ vậy, ở mỗi bước mô hình nhận một ngữ cảnh đúng, theo lối đánh giá thường gọi là *teacher forcing*. Đổi lại, trường này đưa văn phong của người chú thích vào đầu vào, nên các điểm số tuyệt đối cần được đọc kèm điều kiện ấy.

## 4.3 Cấu hình huấn luyện

Mọi mô hình được huấn luyện trong đề tài đều tinh chỉnh Qwen2.5-VL-3B-Instruct [34] bằng QLoRA [29, 30] trên LLaMA-Factory [31]. Bảng 4.1 ghi cấu hình của bước tinh chỉnh có giám sát từ mô hình gốc.

**Bảng 4.1.** Cấu hình tinh chỉnh có giám sát. Các mô hình tinh chỉnh từ mô hình gốc dùng chung cấu hình này và chỉ khác nhau ở tập dữ liệu và hạt giống. Hai thành phần của phương pháp đề xuất học tiếp với số bước và tốc độ học riêng (Mục 4.5 và Mục 4.6).

| Tham số | Giá trị |
|---|---|
| Mô hình gốc | Qwen2.5-VL-3B-Instruct |
| Lượng tử hoá | NF4, 4 bit |
| Hạng LoRA r / α / dropout | 8 / 16 / 0,05 |
| Mô-đun gắn bộ chuyển đổi | q, k, v, o, gate, up, down |
| Tháp thị giác, tầng chiếu đa phương thức | đóng băng |
| Độ dài ngữ cảnh | 2560 |
| Cỡ lô mỗi thiết bị / tích luỹ gradient | 4 / 4 (hiệu dụng 16) |
| Tốc độ học / lịch / tỉ lệ khởi động | 1 × 10^-4 / cosine / 0,05 |
| Số lượt duyệt | 2 (=8.072 bước) |
| Độ chính xác | bf16, có gradient checkpointing |
| Nhân tính toán hợp nhất (giảm bộ nhớ) | có bật |
| Tiến trình tiền xử lý | 8 |
| Hạt giống | 101 và 202 |
| Phần cứng | một GPU A100 |
| Tham số huấn luyện được | 14.966.784 (0,48% phần ngôn ngữ) |

**Độ dài ngữ cảnh.** Độ dài ngữ cảnh được đặt ở 2560 token để chừa biên cho mẫu dài nhất (2.017 token, thuộc mô hình mô tả phần tử ở Phụ lục A, tức mô hình viết một dòng mô tả phần tử cần chạm trước câu hướng dẫn). Chuỗi vượt giới hạn sẽ bị cắt ở cuối, mà phần cuối lại là câu mô hình cần học sinh ra.

## 4.4 Tổng quan phương pháp đề xuất

Độ đo executability chỉ chấm câu hướng dẫn ở đầu ra. Vì vậy phương pháp đề xuất tác động thẳng vào câu, chứ không vào một bước trung gian trước câu như dòng mô tả phần tử, thẻ chọn hay tọa độ ghi trong dòng mô tả, là những chỗ các hướng đã thử nhắm vào (Phụ lục A). Phương pháp dựa trên hai nguồn có thể cho câu tốt hơn. Nguồn thứ nhất là chính mô hình, vì với cùng một bước, mô hình tinh chỉnh có giám sát (S1) có thể viết nhiều câu khác nhau, và câu sinh bằng giải mã tham lam không phải lúc nào cũng là câu giúp mô hình định vị tìm đúng phần tử. Nguồn thứ hai là hơn sáu mươi nghìn câu chuẩn có sẵn trong tập huấn luyện. Khi bước đang xét giống một bước đã có câu chuẩn, câu chuẩn cũ có thể đúng hơn câu mô hình tự viết. Mỗi nguồn được khai thác bằng một thành phần, và hai thành phần chạy nối tiếp.

1. **Thành phần thứ nhất, học tăng cường thưởng SPICE (Mục 4.5).** Thành phần này dạy mô hình tự viết câu tốt hơn. Mô hình tinh chỉnh có giám sát được học tiếp bằng GRPO, một thuật toán học tăng cường so điểm thưởng giữa nhiều câu sinh cho cùng một câu nhắc (Mục 2.3). Phần thưởng là SPICE của câu sinh ra so với câu chuẩn; SPICE chấm mức trùng khớp giữa hai câu về các đối tượng, thuộc tính và quan hệ được nhắc tới. Một thử nghiệm trước khi huấn luyện cho thấy câu có SPICE cao hơn thường cũng dẫn mô hình định vị tới đúng phần tử hơn. Lúc suy luận, mô hình này viết một câu nháp bằng giải mã tham lam.
2. **Thành phần thứ hai, ACE (Mục 4.6).** Thành phần này dùng lại câu chuẩn có sẵn mà không sao chép một cách máy móc. Việc luôn sao chép câu chuẩn của bước giống nhất lại làm giảm mạnh điểm số so khớp văn bản, nên điều cần giải quyết là biết khi nào nên chép. Một bộ sinh, học tiếp từ mô hình của thành phần thứ nhất, được xem thêm bốn câu chuẩn của các bước giống nhất trong tập huấn luyện, gọi là câu ví dụ. Câu của bộ sinh chỉ thay câu nháp khi câu ấy chép nguyên văn một trong bốn câu ví dụ và cùng loại thao tác với câu nháp; ngược lại câu nháp được giữ.

Hai thành phần bổ sung cho nhau: thành phần thứ nhất viết câu từ đầu nên không dùng được các câu chuẩn có sẵn. Thành phần thứ hai chỉ thay câu nháp khi thoả cả hai điều kiện trên, nên ở phần lớn các bước câu được chấm vẫn là câu nháp. Ngoài ra, câu nháp được viết khi nhìn chính màn hình đang xét, nên loại thao tác của câu nháp giúp loại những câu ví dụ nói đúng phần tử nhưng sai thao tác.

Câu ra khỏi thành phần thứ hai là câu được chấm. Mô hình định vị dùng để chấm không xuất hiện trong phần thưởng của thành phần thứ nhất, cũng không xuất hiện trong luật chọn câu của thành phần thứ hai (gọi là luật đồng thuận). Lúc suy luận, không thành phần nào được xem trước câu chuẩn của bước đang xét. Vì vậy độ đo executability vẫn độc lập với phương pháp. Từ đây trở đi, *mô hình học với thưởng SPICE* chỉ thành phần thứ nhất chạy một mình, còn *phương pháp đề xuất* chỉ cả hai thành phần nối tiếp.

## 4.5 Thành phần thứ nhất: học tăng cường thưởng SPICE

**Căn cứ.** Độ đo chấm câu ở đầu ra, trong khi các hướng đã thử trước (Phụ lục A, từ Mục A.1.1 đến Mục A.4.1) đều tác động vào một bước trung gian trước câu, như dòng mô tả, thẻ chọn hoặc tọa độ ghi trong dòng mô tả. Kết quả ở phụ lục này cho thấy thay đổi ở những bước ấy chỉ ảnh hưởng khá yếu tới câu (Mục A.4.2 và Mục A.5), còn thông tin vị trí gắn thêm vào bộ sinh câu thì bị bộ sinh bỏ qua (Mục A.6). Từ đó, thành phần thứ nhất đặt phần thưởng thẳng lên câu, giống cách các công trình sinh chú thích ảnh đã dùng CIDEr và SPIDEr làm phần thưởng [46, 48].

Trước khi huấn luyện, chúng tôi thử nghiệm không cần huấn luyện trên tập kiểm định nội bộ (Mục 3.3). Với mỗi bước, mô hình tinh chỉnh có giám sát (S1) sinh một câu bằng giải mã tham lam và tám câu bằng lấy mẫu; câu có SPICE cao nhất so với câu chuẩn được đưa đi chấm. Cách chọn này nâng executability rõ rệt so với câu giải mã tham lam, trong khi chọn ngẫu nhiên một câu lấy mẫu thì không. Executability cũng giảm dần theo hạng SPICE của câu trong cùng một bước. Hai quan sát này cho thấy trong số những câu mô hình có thể viết, câu có SPICE cao hơn thường cũng là câu dẫn mô hình định vị tới đúng phần tử hơn. Dù vậy, thử nghiệm này cũng báo trước hai giới hạn. Thứ nhất, ở khoảng một phần ba số cặp gồm một câu dẫn mô hình định vị tới đúng phần tử và một câu không, SPICE cho hai câu điểm bằng nhau, nên phần thưởng không phân biệt được hai câu ấy; theo công thức (2.2), một nhóm mà mọi câu bằng điểm thì không đóng góp gradient. Thứ hai, mức tăng có được khi chọn câu nhờ biết trước câu chuẩn chỉ là ngưỡng tối đa; mô hình học tăng cường không thấy câu chuẩn lúc suy luận nên thường chỉ đạt được một phần mức ấy.

**Thiết kế.** Thành phần thứ nhất xuất phát từ mô hình tinh chỉnh có giám sát, hạt giống 101, chứ không từ các giai đoạn học tiếp trên mô hình mô tả phần tử, để khi so với mô hình xuất phát, hai bên chỉ còn khác nhau ở bước học tăng cường. Bộ chuyển đổi LoRA của mô hình xuất phát được hoà vào trọng số gốc, tức phần cập nhật hạng thấp được cộng thẳng vào ma trận trọng số để thu một mô hình duy nhất. Sau đó một bộ chuyển đổi LoRA mới, cùng hạng và cùng các mô-đun, được gắn lên trên với ma trận B (một trong hai ma trận hạng thấp của LoRA) khởi tạo bằng không. Nhờ vậy, ở bước đầu tiên mô hình đang học trùng với mô hình tinh chỉnh có giám sát. Bản đóng băng của mô hình tinh chỉnh có giám sát làm mô hình tham chiếu cho số hạng KL, tức độ lệch Kullback–Leibler giữ mô hình đang học không đi quá xa mô hình tham chiếu. Phần thưởng của một câu s so với câu chuẩn là

\[
r(s) = \operatorname{SPICE}(s,g) - 0,02 \cdot \max(0,\ |s|-|g|-3),
\tag{4.1}
\]

trong đó `|·|` là số từ, và câu rỗng nhận 0 điểm. Số hạng thứ hai chỉ phạt những câu dài hơn câu chuẩn quá ba từ, để mô hình không tăng SPICE bằng cách liệt kê thêm chi tiết.

Mỗi bước cập nhật lấy hai câu nhắc, và mỗi câu nhắc sinh `G = 8` câu ở nhiệt độ 1,0, tối đa 96 token. Lượt huấn luyện kéo dài 500 bước, tương ứng một lượt duyệt qua 1.000 câu nhắc lấy từ phần tập dạy đã loại tập kiểm định nội bộ. Các câu nhắc gồm mọi loại thao tác, trong đó khoảng hai phần ba là bước chạm. Tốc độ học là `10^-5` và hệ số KL là `β = 0,04`; vòng huấn luyện được tóm tắt ở Hình 4.2.

*(Sơ đồ vẽ bằng TikZ, chỉ xem được trong bản PDF.)*

**Hình 4.2.** Vòng huấn luyện của thành phần thứ nhất, học tăng cường với thưởng SPICE. Chỉ khối tô xám được cập nhật.

**Cách chọn điểm lưu.** Điểm lưu là bản trọng số được lưu lại tại một bước huấn luyện. Chúng tôi dùng hai điểm lưu ở bước 250 và bước 500 để sinh câu bằng giải mã tham lam trên tập kiểm định nội bộ. Trên tập này, mức tăng SPICE của cả hai đều nhỏ, nhưng executability tăng theo số bước. Mọi bước mà điểm lưu 250 làm đúng còn mô hình tinh chỉnh có giám sát làm sai (gọi là bước được cứu) cũng được điểm lưu 500 làm đúng. Vì vậy chúng tôi chọn điểm lưu 500, rồi sinh câu và chấm trên tập kiểm tra đúng một lần; sau khi đã thấy điểm, chúng tôi không sinh lại và không đổi điểm lưu.

**Hai giới hạn của thiết kế.** Thứ nhất, hai mô hình được so không sinh câu theo cùng một cách. Câu của mô hình tinh chỉnh có giám sát trong các bảng kết quả được sinh với bộ chuyển đổi để riêng và theo lô, còn câu của mô hình học với thưởng SPICE được sinh sau khi đã hoà bộ chuyển đổi vào trọng số, ở độ chính xác fp16 và từng câu một. Trong một đánh giá, chỉ riêng khác biệt này đã làm 4 trong 20 câu của bước chạm khác đi (ở 20 bước không chạm thì không câu nào đổi), nên một phần nhỏ của chênh lệch giữa hai mô hình có thể đến từ cách sinh câu thay vì từ học tăng cường. Thứ hai, chưa chạy cấu hình đối chứng học có giám sát thêm cùng số bước từ cùng điểm xuất phát, nên chưa tách được phần do học tăng cường khỏi phần do học thêm.

## 4.6 Thành phần thứ hai: chép câu ví dụ khi đồng thuận loại thao tác (ACE)

**Căn cứ.** Tập huấn luyện chứa hơn sáu mươi nghìn câu chuẩn, và nhiều bước của tập kiểm tra giống một bước nào đó trong tập này ở loại mục tiêu, ứng dụng và vị trí trong tác vụ. Chúng tôi đo mức giống này trước khi huấn luyện. Với mỗi bước chạm của tập kiểm tra, chúng tôi truy hồi bốn câu chuẩn của các bước giống nhất trong tập huấn luyện. Ở 15,8% số bước, một trong bốn câu ấy trùng nguyên văn câu chuẩn của chính bước đang xét. Ở 9,8% số bước, sự trùng khớp này xảy ra đúng lúc mô hình học với thưởng SPICE viết sai câu. Nếu chép đúng ở những bước ấy, BLEU-4 tính gộp trên toàn tập kiểm tra tăng được khoảng 5 điểm và CIDEr-D khoảng 65 điểm; hai độ đo này đo mức trùng cụm từ giữa câu sinh ra và câu chuẩn. Ngược lại, nếu luôn chép câu ví dụ đứng đầu thì BLEU-4 giảm từ 52,4 (câu nháp của thành phần thứ nhất) xuống 28,3. Vì vậy điều cần giải quyết là xác định khi nào nên chép. ACE (*Action-Consistent Exemplar copying*) tách việc này làm hai phần: một mô hình học cách dùng câu ví dụ, và một luật đơn giản quyết định có nhận câu của mô hình ấy hay giữ câu nháp của thành phần thứ nhất.

**Bộ sinh có câu ví dụ truy hồi.** Kho truy hồi là phần tập huấn luyện đã bỏ mọi tác vụ của tập kiểm định nội bộ, gồm 62.880 bước thuộc 12.542 tác vụ, không chứa tác vụ nào của tập kiểm tra. Phép truy hồi chỉ dùng văn bản, không dùng ảnh, và so khớp bằng TF-IDF, tức cách đánh trọng số từ theo tần suất trong câu và độ hiếm trong kho. Việc truy hồi dùng hai cách tìm, rồi gộp kết quả và bỏ các câu trùng nhau. Cách thứ nhất, theo SmallCap [47], tìm thẳng những bước có mục tiêu và câu gần nhất trong lịch sử thao tác giống với bước đang xét. Cách thứ hai tìm trước những tác vụ có mục tiêu giống nhất, rồi trong mỗi tác vụ ấy chọn bước tương ứng dựa trên câu gần nhất trong lịch sử. Bốn câu ví dụ được chèn vào câu nhắc ngay trước dòng yêu cầu viết câu.

Bộ sinh được tạo bằng cách cho bộ chuyển đổi của thành phần thứ nhất học có giám sát thêm 250 bước với tốc độ học `2 × 10^-5`, trên 3.991 bước của phần tập dạy có sẵn ảnh. Để mô hình không học cách chép câu ví dụ một cách máy móc, khối ví dụ lúc huấn luyện được biến đổi ngẫu nhiên. Số câu ví dụ được lấy ngẫu nhiên từ 2 đến 6 và thứ tự các câu bị xáo trộn; 15% câu nhắc không có khối ví dụ và 10% câu nhắc có khối ví dụ lấy ngẫu nhiên; tác vụ đang học cũng bị loại khỏi kho truy hồi. Để tách phần do truy hồi khỏi phần do học thêm, chúng tôi huấn luyện thêm một mô hình để so sánh trên cùng các bước, cùng chuỗi đích và cùng siêu tham số, chỉ khác ở chỗ câu nhắc không có khối ví dụ.

**Luật đồng thuận.** Ở mỗi bước có hai câu: câu nháp của thành phần thứ nhất và câu của bộ sinh. Câu của bộ sinh chỉ được nhận khi thoả cả hai điều kiện.

1. **Chép nguyên văn.** Sau khi tách từ, câu của bộ sinh trùng hoàn toàn với một trong bốn câu ví dụ của khối. Điều kiện này chỉ giữ lại những bước mà bộ sinh chọn đúng câu ví dụ, và bỏ những bước bộ sinh tự viết câu mới.
2. **Đồng thuận loại thao tác.** Động từ ở đầu câu của bộ sinh và động từ ở đầu câu nháp thuộc cùng một lớp thao tác (chạm, nhấn giữ, gõ, cuộn, mở ứng dụng, quay lại). Câu ví dụ đến từ một bước khác, nên có thể nói đúng phần tử nhưng sai thao tác, ví dụ bảo gõ chữ ở một bước cần chạm. Câu nháp được viết khi nhìn chính màn hình đang xét, nên được dùng để kiểm lại loại thao tác.

**Cách chọn luật.** Luật trên được chọn trên tập kiểm định nội bộ, trong bốn biến thể: chỉ dùng điều kiện chép; chép kèm đồng thuận loại thao tác; chép kèm điều kiện phần lõi của câu (phần còn lại sau khi bỏ động từ và hư từ) trùng với câu nháp ít nhất một nửa; và chép kèm cả hai điều kiện. Tiêu chí chọn được viết ra trước khi chấm executability trên tập ấy. Tiêu chí chỉ xét những biến thể không kém hơn câu nháp ở đa số độ đo so khớp văn bản với câu chuẩn, rồi chọn biến thể có executability cao nhất trong các biến thể đó. Biến thể được chọn sau đó được áp lên tập kiểm tra đúng một lần.

## 4.7 Các mốc so sánh

Mọi kết quả của phương pháp đề xuất được đặt cạnh ba mốc. Mốc thứ nhất là mô hình gốc Qwen2.5-VL-3B-Instruct khi chưa tinh chỉnh, trong các bảng gọi là Base. Mốc thứ hai là mô hình tinh chỉnh có giám sát, trong các bảng gọi là S1. Mô hình này được tinh chỉnh từ mô hình gốc với cấu hình ở Bảng 4.1 để sinh thẳng câu hướng dẫn từ câu nhắc, không qua bước trung gian nào, và được huấn luyện hai lần với hai hạt giống 101 và 202. Vì hai lượt chỉ khác hạt giống, chênh lệch giữa chúng cho biết mức dao động khi huấn luyện lại cùng một cấu hình. Thành phần thứ nhất của phương pháp đề xuất học tiếp từ lượt hạt giống 101, nên lượt này cũng là mốc so trực tiếp của phương pháp. Mốc thứ ba là chính câu chuẩn được đưa thẳng đi chấm. Điểm của mốc này là mức độ đo cho được khi nhận câu do người chú thích viết, gọi là ngưỡng tối đa (trong các bảng ghi là Trần do giới hạn không gian).

Trước khi đi tới phương pháp đề xuất, đề tài đã thử nhiều hướng khác, gồm viết trước câu một dòng mô tả phần tử cần chạm, học ưu tiên trên dòng mô tả, chọn phần tử trong một danh sách ứng viên, thưởng cho tọa độ ghi trong dòng mô tả và sửa câu theo vùng cắt quanh phần tử. Kết quả của các hướng này là căn cứ để chọn phương pháp và được tóm tắt ở Mục 6.10; thiết kế và số liệu chi tiết nằm ở Phụ lục A.

## 4.8 Cách đọc kết quả

Mọi phép so giữa hai mô hình trong đề tài, mà thường là một mô hình có can thiệp đặt cạnh mốc so sánh của nó, đều là phép so ghép cặp trên cùng 4.463 bước chạm của tập kiểm tra. Mỗi phép so được trình bày bằng ba con số đi cùng nhau: mức chênh Δ, khoảng tin cậy 95% lấy từ bootstrap gom cụm theo ứng dụng (lấy mẫu lại theo cụm ứng dụng thay vì theo từng bước, vì các bước trong cùng một ứng dụng thường giống nhau), và giá trị p của kiểm định McNemar, một kiểm định thống kê dành cho hai mô hình chấm trên cùng tập bước và chỉ dựa vào những bước mà đúng một trong hai mô hình làm đúng (Mục 5.13). Mô hình có can thiệp chỉ được coi là hơn hay kém mốc so sánh khi khoảng tin cậy nằm hoàn toàn về một phía của 0; khi khoảng tin cậy phủ 0, kết quả được ghi là chưa kết luận được, kể cả khi Δ dương.

Ngoài ba con số trên, hai đại lượng nữa được trình bày kèm để người đọc tự đánh giá độ lớn của mức chênh. Đại lượng đầu tiên là chênh lệch giữa hai hạt giống, tức độ lệch giữa hai lượt huấn luyện mô hình tinh chỉnh có giám sát chỉ khác nhau ở hạt giống, bằng 0,52 điểm (Mục 6.7). Đại lượng thứ hai là sai số chuẩn của hiệu ghép cặp, 0,79 điểm, cho biết một mức chênh cần lớn cỡ nào thì mới phân biệt được với sai số đo (Mục 5.13).

Ngoài kết quả trên toàn tập, chúng tôi còn đọc kết quả riêng trên từng nhóm con theo ba cách chia nhóm chính, là theo độ dài câu, theo độ khó của màn hình và theo nguồn của tên phần tử. Những cách chia nhóm khác được đặt ra sau khi đã có điểm số là phân tích hậu kiểm, và được ghi rõ như vậy tại chỗ chúng xuất hiện.

# Chương 5. Độ đo executability

Chương này định nghĩa độ đo executability, dùng để chấm phương pháp đề xuất và các mốc so sánh ở Chương 6. Độ đo coi một câu là đúng khi câu dẫn được tới đúng phần tử, thay vì so câu với câu chuẩn, cách chấm mà Mục 2.6 đã cho thấy là không đáng tin. Phần lớn chương kiểm chứng độ đo trước khi dùng nó để rút ra kết luận.

## 5.1 Định nghĩa

Với mỗi bước chạm, độ đo dùng năm đại lượng. `s` là câu hướng dẫn được chấm; dòng mô tả phần tử mà một số hướng đã thử sinh trước câu (Phụ lục A) được cắt bỏ trước khi chấm. `I` là ảnh màn hình, `g` là tọa độ người dùng đã chạm. `E` là tập phần tử trên màn, lấy từ cây trợ năng; các phần tử có tâm cách nhau dưới 24 dp được gộp làm một (dp là đơn vị độ dài của Android, không phụ thuộc mật độ điểm ảnh; trên thiết bị được dùng, 24 dp bằng 63 điểm ảnh). `G` là mô hình định vị phần tử: nhận ảnh và một câu, trả về tọa độ `p = G(I,s)` của phần tử mà câu chỉ tới. `G` độc lập với mô hình được chấm và không được biết `g`.

Một bước được tính là đúng khi thoả đồng thời ba điều kiện.

- **(i) Khớp loại thao tác.** Loại thao tác của `s`, sau khi chuẩn hoá, phải trùng với của câu chuẩn. Có năm loại: chạm, gõ, cuộn, nhấn giữ và quay lại; mười hai động từ (*tap, click, press, select, choose, touch, open, launch, go, navigate, visit, view*) được xếp vào loại chạm.

  Cách chuẩn hoá này có một lỗi đã biết: động từ được dò từ trái sang phải, nên *go back, navigate back* và *press the back button* bị xếp vào chạm thay vì quay lại. Sửa lỗi chỉ hạ điểm của mô hình tinh chỉnh có giám sát (S1) từ 59,12 xuống 58,81 và của mô hình gốc (Base) từ 47,60 xuống 47,40; chênh lệch giữa hai mô hình đổi từ 11,52 thành 11,41 điểm. Điểm chính giữ cách chuẩn hoá cũ để không sửa độ đo sau khi đã thấy điểm; bản đã sửa chỉ dùng ở các bước không chạm (Mục A.2.2.4), nơi quay lại là một thao tác thật.

- **(ii) Không đảo nghĩa.** `s` và câu chuẩn không được gọi tên hai trạng thái ngược nhau của cùng một điều khiển, chẳng hạn nút “bật thông báo” và “tắt thông báo”. Điều kiện (iii) không bắt được lỗi này vì hai trạng thái nằm cùng một chỗ. Danh sách lập thủ công gồm chín cặp từ trái nghĩa (*on/off, enable/disable, show/hide, mute/unmute, expand/collapse, check/uncheck, select/deselect, start/stop, enabled/disabled*).

- **(iii) Định vị đúng.** `p` nằm trong vùng dung sai quy ước quanh `g`, `|p_x-g_x| ≤ τW` và `|p_y-g_y| ≤ τH`, với `W, H` là bề ngang và chiều cao màn hình và `τ = 0,14` theo [2]; đồng thời không phần tử nào khác có tâm gần `p` hơn chính `g`:

\[
\|p-g\| < \|p-c(e)\| \quad \forall e \in E,
\tag{5.1}
\]

với `c(e)` là tâm của phần tử `e`. Vùng gồm mọi điểm như vậy là ô Voronoi của phần tử cần chạm (Hình 5.1).

Điểm executability là tỉ lệ bước chạm thoả cả ba điều kiện.

Hai chi tiết của điều kiện (iii) dễ bị hiểu nhầm. Vùng dung sai là hình chữ nhật, không phải hình tròn: trên màn 1080 × 2400, vùng rộng ±151 điểm ảnh theo chiều ngang nhưng ±336 điểm ảnh theo chiều dọc. Ô Voronoi được dựng quanh chính điểm chạm `g`, không quanh tâm hộp của phần tử chứa `g`; nếu lấy tâm hộp, luật sẽ loại nhầm 59% số câu cùng nghĩa. Mọi hộp chứa `g` đều được coi là thuộc phần tử cần chạm.

**Vai trò của mô hình định vị và phạm vi của độ đo.** Mốc đối chiếu là tọa độ người thật đã chạm. `G` không được tinh chỉnh và chỉ trả về một điểm; đúng hay sai do so điểm ấy với `g`. Độ đo chỉ xét câu có chỉ đúng phần tử hay không, không xét độ trôi chảy, độ dài hay mức hữu ích với người đọc.

## 5.2 Luật xác định trúng và giới hạn của luật dung sai quy ước

Điều kiện ô Voronoi chặt hơn luật dung sai quy ước nhưng phức tạp hơn, nên chúng tôi kiểm xem nó có cần thiết không trên 250 bước chạm (Bảng 5.1). Ở bảng này, ngưỡng tối đa là tỉ lệ cho điểm khi điểm dự đoán là điểm chạm dịch đi một độ lệch nhỏ; ngưỡng tối thiểu là tỉ lệ cho điểm khi điểm dự đoán được đặt lên phần tử khác gần nhất, giống một câu gọi sai tên nút.

**Bảng 5.1.** So sánh các luật xác định trúng. Luật càng tốt thì ngưỡng tối thiểu càng thấp.

| Luật | Ngưỡng tối đa (lệch 3%) | Ngưỡng tối thiểu (chỉ sai nút) | Biên độ |
|---|---:|---:|---:|
| Cửa sổ dung sai ± 14% theo từng trục | – | 84,3% | ≈ 16 điểm |
| Ô Voronoi | 99,7% | **2,8%** | ≈ 97 điểm |

Luật dung sai quy ước vẫn cho điểm phần lớn các câu gọi sai tên nút, vì 63,2% số bước có ít nhất một phần tử khác nằm trong vùng dung sai của phần tử cần chạm. Khoảng cách giữa ngưỡng tối đa và mức sàn vì thế quá hẹp để phân biệt câu tốt với câu kém. Luật ô Voronoi hạ ngưỡng tối thiểu gần về không mà vẫn giữ ngưỡng tối đa, nên được chọn.

Kết quả này cần đọc kèm hai lưu ý. Thứ nhất, ngưỡng tối thiểu 2,8% chỉ đúng với câu chỉ sang một phần tử khác, không đúng với điểm dịch nhẹ nhưng vẫn nằm trong ô của phần tử cần chạm (Mục 5.7). Thứ hai, phép gộp phần tử quyết định thế nào là hai phần tử khác nhau: phép gộp xoá ít nhất một tâm ở 96,3% số bước, phần lớn là tâm trùng của cùng một phần tử, nhưng ở 8,2% số bước lại xoá nhầm một phần tử khác có thật. Vì vậy điểm theo luật dung sai luôn được trình bày kèm, nhưng không dùng làm điểm chính.

**Hình 5.1.** Một bước mà hai luật chấm cho hai kết quả khác nhau. Người dùng chạm dòng *Birthday*. Câu của S1 dẫn mô hình định vị tới đúng dòng đó. Câu của mô hình gốc tả dòng *Gender* ngay phía trên, nên điểm trả về lệch 128 điểm ảnh, vẫn trong vùng dung sai quy ước. Luật dung sai cho là trúng; chỉ luật ô Voronoi phát hiện câu đang chỉ sang một dòng khác.

Kết luận này vẫn đúng với điểm do mô hình định vị thật trả về. Trên 300 bước của Mục 5.4, khi nhận câu chuẩn, luật ô Voronoi cho điểm mọi bước có sai số định vị dưới 3% bề ngang màn (`n = 188`) và không cho điểm bước nào có sai số trên 14% (`n = 63`).

## 5.3 Mô hình định vị dùng làm công cụ đo

Chúng tôi chọn UGround-V1-2B [5] làm công cụ đo. Theo chúng tôi, một công cụ đo phù hợp cần thoả ba điều kiện:

1. khác họ với mô hình bị chấm, để độ đo không thiên vị;
2. không được huấn luyện trên AndroidControl, tức chính bộ dữ liệu dùng để chấm;
3. sai số định vị đủ nhỏ so với khoảng cách giữa các phần tử (Mục 5.4).

Trong ba điều kiện này, UGround-V1-2B chỉ đáp ứng điều kiện thứ ba, vì mô hình này dựng trên Qwen2-VL, cùng dòng với Qwen2.5-VL-3B đang được chấm, và được huấn luyện trên 47 nghìn phần tử do người gán nhãn lấy từ phần huấn luyện chính thức của AndroidControl, phần chứa 90% tác vụ trong tập kiểm tra (Mục 3.3). Vì vậy công cụ đo có thể đã gặp một phần màn hình của tập kiểm tra, và gần như chắc chắn đã quen văn phong chú thích của bộ dữ liệu.

Đo trực tiếp cho thấy việc trùng dữ liệu huấn luyện không làm lệch điểm. Tách 4.463 bước chạm theo phần chia chính thức (3.994 bước thuộc phần huấn luyện, 469 bước thuộc phần kiểm tra và kiểm định), câu chuẩn đạt 75,9% và 74,0%, S1 đạt 59,1% và 59,3%, mô hình gốc đạt 47,7% và 46,7%. Khoảng tin cậy của hai phần chồng nhau ở cả ba loại câu, và không loại câu nào cao hơn ở phần công cụ có thể đã học. Với 469 bước, phép đo loại được độ lệch từ năm điểm trở lên, chưa loại được độ lệch một đến hai điểm.

Cách tách này không kiểm được thiên vị theo văn phong, vì hai phần dùng chung văn phong chú thích. Mục 5.9 kiểm khả năng này bằng một công cụ đo thứ hai không dùng AndroidControl nhưng vẫn thuộc họ Qwen (Mục 7.2); Mục 5.10 kiểm thêm bằng một mô hình ngoài họ Qwen. Câu nhắc đưa cho G được chép nguyên văn từ trang giới thiệu mô hình của nhóm tác giả.

## 5.4 Sai số của công cụ đo

Độ đo chỉ đáng tin khi `G` đáng tin, nên `G` được kiểm trước khi chấm mô hình nào. Sai số định vị cần được so với khoảng cách giữa các phần tử. Gọi biên dung sai là nửa khoảng cách từ phần tử cần chạm tới phần tử khác gần nhất sau khi gộp. Trên 1.496 bước chạm, biên dung sai có trung vị 67 điểm ảnh (6,2% bề ngang) và phân vị thứ mười là 39 điểm ảnh (3,6%), nên sai số cỡ 3% bề ngang (khoảng 32 điểm ảnh) vẫn nhỏ hơn cả phân vị thứ mười. Mức sai số này đạt được vì tọa độ chạm trong AndroidControl phần lớn là tâm phần tử (79,4% số điểm chạm cách một tâm không quá 1,5 điểm ảnh). Tỉ lệ loại nhầm là 0% ở mức sai số 3%, 7,5% ở mức 5%, 24,1% ở mức 8% và tăng mạnh lên 55% ở mức sai số 13%.

**Kết quả đo.** Trên 300 bước của tập kiểm tra, khi nhận câu chuẩn, UGround-V1-2B có sai số trung vị 0,7% bề ngang màn, và 62,7% số bước có sai số dưới 3%, nên tỉ lệ loại nhầm thực tế rất thấp. Phân bố có đuôi dài (các điểm phân vị 25, 75, 90 lần lượt là 0,2%, 8,8% và 36,3%); nguyên nhân là vì mô hình thường trỏ rất gần tâm phần tử, nhưng đôi khi lại trỏ hẳn sang một vùng khác của màn hình, khiến cho mức trung vị chưa phản ánh hết toàn bộ bức tranh. Tuy vậy, dạng lỗi này chỉ kéo điểm xuống, không làm điểm cao hơn thực tế.

## 5.5 Ngưỡng tối đa của độ đo

Sai số định vị nhỏ chưa cho biết điểm cao nhất mà độ đo có thể cho, vì độ đo chấm theo ô Voronoi chứ không theo khoảng cách. Để đo điểm này, chúng tôi đưa câu chuẩn của mọi bước chạm cho mô hình định vị rồi chấm bằng đúng luật đang dùng.

> Trên toàn bộ 4.463 bước chạm, **ngưỡng tối đa theo luật ô Voronoi là 75,7%, khoảng tin cậy 95% là [74,1; 77,3]** (cách tính ở Mục 5.13). Theo luật dung sai, ngưỡng tối đa là 84,3% [82,9; 85,6]; con số này trùng với ngưỡng tối thiểu của luật dung sai ở Mục 5.2 chỉ do tình cờ, vì đó là hai đại lượng khác nhau đo trên hai tập bước khác nhau.

Với câu chuẩn, điều kiện (i) và (ii) gần như luôn thoả (chỉ ba bước bị loại vì câu chứa cả “on” lẫn “off”, dưới 0,07%), nên ngưỡng tối đa phản ánh độ chính xác định vị. Mức 75,7% cũng chưa phải mức cao nhất trên tập kiểm tra: có 148 bước câu chuẩn trượt nhưng câu của mô hình gốc hoặc S1 trúng, nên tổng cộng 3.527 bước, tức 79,1%, được ít nhất một trong ba loại câu giải đúng.

Vì vậy điểm executability nên được đọc trên nền 75,7 thay vì 100. Chúng tôi đặt điểm của mô hình cạnh điểm của câu chuẩn; chẳng hạn S1 đạt 59,1, còn cách ngưỡng tối đa 16,6 điểm (Mục 6.9.4). Các công trình sinh chỉ dẫn điều hướng cũng trình bày như vậy; Zhao và cộng sự [37] đặt mốc người 75,1 cạnh mức 47,7 của hệ thống tốt nhất. Theo cách gọi của Nangia và Bowman [38], ngưỡng tối đa là ước lượng thận trọng về năng lực của câu chuẩn khi đo qua cùng công cụ, chưa phải năng lực của con người.

**Ý nghĩa của ngưỡng tối đa.** Ngưỡng tối đa là điểm của câu do người chú thích viết cho người khác đọc. Một mô hình được thưởng theo độ đo này có thể vượt mức ấy bằng cách viết cho mô hình định vị thay vì cho người, và thiết kế hiện tại không ngăn được điều đó. Khi một mô hình tiến sát ngưỡng tối đa, cần kiểm lại câu của nó trước khi coi đó là thành công.

## 5.6 Ngưỡng tối thiểu của độ đo

Ngưỡng tối thiểu là tỉ lệ bước mà mô hình định vị vẫn trúng khi câu không mang thông tin gì. Nếu tỉ lệ này cao, phần lớn điểm đến từ ảnh màn hình chứ không từ câu, và độ đo không còn đo chất lượng câu.

Cần đo ngưỡng tối thiểu vì có một dấu hiệu dễ gây hiểu nhầm: **40,0% trong 4.463 bước được cả câu chuẩn, S1 lẫn mô hình gốc chưa tinh chỉnh giải đúng**, nên dễ nghĩ rằng các bước ấy dễ đến mức câu nào cũng trúng và ngưỡng tối thiểu nằm quanh 40%. Chúng tôi đo ngưỡng tối thiểu bằng ba trường hợp.

- **Câu chung chung.** Mọi bước nhận cùng câu “*Tap the button.*” (“hãy chạm vào cái nút”), đúng ngữ pháp nhưng không nói phần tử nào.
- **Câu thật nhưng của màn hình khác.** Mỗi bước nhận nguyên văn câu chuẩn của một bước thuộc tác vụ khác, cùng văn phong và độ dài tương đương (trung vị 34 ký tự so với 35). Trường hợp này loại khả năng câu chung chung bị điểm thấp chỉ vì là đầu vào lạ.
- **Câu bỏ tên phần tử.** Giữ mệnh đề chỉ vị trí, thay tên phần tử bằng “the item”; chẳng hạn “Click on the Sort filter at the top right” thành “Click on the item at the top right”. Đây là chiều ngược của phép bỏ mệnh đề vị trí ở Mục 5.8.

Ba trường hợp được đo trên một mẫu ngẫu nhiên 800 bước (từ đây gọi là mẫu 800 bước), có ngưỡng tối đa 74,9%, lệch dưới một điểm so với toàn tập. Bảng dưới ghi hai trường hợp đầu; trường hợp bỏ tên phần tử nằm ở Mục 5.6.1.

| Trường hợp | Câu đưa cho mô hình định vị | Điểm | KTC 95% |
|---|---|---:|---:|
| Ngưỡng tối đa | câu chuẩn | 74,9 | – |
| S1 | mô hình đã tinh chỉnh | 58,8 | – |
| Base | mô hình chưa tinh chỉnh | 48,6 | – |
| Câu chung chung | “*Tap the button.*” | 12,0 | [9,7; 14,4] |
| Câu của màn hình khác | câu chuẩn của một bước khác | 6,1 | [4,5; 7,9] |

**Ngưỡng tối thiểu đo được.** Khoảng dùng được của độ đo, từ ngưỡng tối thiểu tới ngưỡng tối đa, là `74,9 - 12,0 = 62,9` điểm. Cách suy ngưỡng tối thiểu từ tỉ lệ đồng thuận ở đầu mục là sai: 40% số bước ấy chỉ dễ khi có câu thật chỉ đúng phần tử, và cả ba loại câu đều viết được câu như vậy. Tính theo `(điểm - ngưỡng tối thiểu)/(ngưỡng tối đa - ngưỡng tối thiểu)`, mô hình gốc đạt 58,3% khoảng này, S1 đạt 74,4%.

**Trường hợp câu thật của màn hình khác.** Đây là phép thử trực tiếp cho giả thuyết thiên vị theo văn phong ở Mục 5.3. Nếu mô hình định vị ưu ái câu đúng văn phong bất kể nội dung, loại câu này phải đạt điểm cao. Thực tế đây là trường hợp có điểm thấp nhất, thấp hơn cả câu chung chung, và hai khoảng tin cậy không chồng nhau. Như vậy mô hình định vị dựa vào nội dung câu: câu sai dẫn nó tới sai chỗ, còn câu chung chung buộc nó chỉ dựa vào ảnh màn hình, mà chỉ dựa vào ảnh thì rất hay trượt.

### 5.6.1 Vai trò của tên phần tử so với vị trí

Mỗi phép cắt dưới đây bỏ một phần thông tin của câu chuẩn; hai nhóm bước có cỡ gần bằng nhau nên so trực tiếp được.

| Phép cắt | n | Ngưỡng tối đa → sau khi cắt | Mức giảm |
|---|---:|---:|---:|
| Bỏ tên phần tử, giữ vị trí | 193 | 89,6 → 61,1 | **-28,5 pp** |
| Bỏ mệnh đề vị trí, giữ tên | 198 | 89,4 → 85,9 | **-3,5 pp** |

Với phép bỏ tên, `b = 58` bước chuyển từ trúng thành trượt và `c = 3` bước theo chiều ngược lại; kiểm định McNemar (Mục 5.13) cho `χ² = 47,8, p < 0,001`. Tính theo mức giảm điểm, tên phần tử quan trọng gấp tám lần vị trí. Kết quả này phù hợp với cách đặt bài toán, theo đó câu hướng dẫn phải giúp xác định đúng phần tử, chứ không chỉ nói đúng vị trí.

**Cách đọc con số trên phần bị tác động.** Phép bỏ tên chỉ áp dụng được cho câu có mệnh đề vị trí, tức 24,1% số bước. Trên toàn mẫu 800 bước, trường hợp này đạt 68,0%, chỉ thấp hơn mức ngưỡng tối đa 6,9 điểm, vì 607 bước còn lại giữ nguyên câu chuẩn nên mức giảm bị pha loãng 4,15 lần. Con số cần đọc là **-28,5 điểm trên phần bị tác động**; mọi phép cắt chỉ tác động lên một phần số bước đều phải đọc theo cách này.

## 5.7 Kiểm chứng bằng cách cố ý chèn lỗi

Theo cách của Sai và cộng sự [15], chúng tôi cố ý chèn mười loại lỗi đã biết vào 398 bước chạm của tập kiểm tra. Ba dòng đầu của Bảng 5.2 là tỉ lệ độ đo loại nhầm một câu đúng, bảy dòng sau là tỉ lệ độ đo bắt được một câu sai.

**Bảng 5.2.** Kiểm chứng độ đo bằng các lỗi được cố ý chèn vào có kiểm soát.

| Loại lỗi chèn vào | Đo được | n |
|---|---:|---:|
| Loại nhầm câu diễn đạt khác | 0,0% | 398 |
| Loại nhầm ở điều kiện thao tác | 0,0% | 398 |
| Loại nhầm ở luật đảo nghĩa | 0,0% | 398 |
| Bắt được phần tử kề gần | 33,1% | 121 |
| Bắt được phần tử kề xa | 99,6% | 233 |
| Bắt được phần tử rất xa | 100,0% | 397 |
| Bắt được phủ định ngoài bảng | 20,0% | 15 |
| Bắt được sai loại thao tác | 100,0% | 369 |
| Bắt được sai nội dung | 91,1% | 494 |
| Bắt được sai hướng | 100,0% | 755 |

**Cách đọc kết quả chèn lỗi.** Năm dòng đạt kết quả tốt là do chính cách tạo lỗi, chẳng hạn hai dòng “sai loại thao tác” và “sai hướng” dùng cùng một bảng tra để tạo và phát hiện lỗi, còn ở dòng “diễn đạt khác” điểm chèn chỉ cách đáp án 23 điểm ảnh. Thông tin thật nằm ở bốn dòng đặt điểm lên phần tử kề hoặc phủ định câu, trong đó hai phép thử có tỉ lệ bắt lỗi thấp.

**Phần tử kề gần.** Tỉ lệ thấp ở dòng này là hệ quả của thiết kế. Độ đo gộp các phần tử có tâm cách nhau dưới 24 dp (Mục 5.1), nên không phân biệt được các điểm đích dưới khoảng 63 điểm ảnh, gần bằng biên dung sai trung vị 67 điểm ảnh (Mục 5.4). Độ đo bắt được việc gọi tên sai phần tử, nhưng không bắt được một điểm chỉ hơi lệch bên trong chính phần tử cần chạm.

**Phủ định ngoài bảng.** Dòng này do một cơ chế dự phòng cho các từ phủ định ngoài bảng từ vựng đã liệt kê, và chỉ có 15 ca, quá ít để rút ra kết luận.

## 5.8 Độ bền của độ đo trước các cách diễn đạt khác

Nếu chỉ đổi cách nói mà điểm đã đổi thì độ đo đang đo văn phong chứ không đo nội dung. Jandial và cộng sự [18] nêu cảnh báo này sau khi tìm ra những câu khiến mô hình định vị trỏ sai trên giao diện máy tính để bàn. Chúng tôi viết lại câu chuẩn rồi chấm lại, trên mẫu 800 bước.

Bốn biến thể được dựng bằng luật, không dùng mô hình ngôn ngữ, để kiểm tra thủ công được: đổi động từ thao tác (ví dụ *click* thành *tap*), đảo trật tự hai mệnh đề, làm cả hai việc, và bỏ mệnh đề chỉ vị trí. Ba biến thể đầu giữ nguyên nghĩa; biến thể cuối cố ý bớt thông tin để làm mốc đối chiếu.

**Bảng 5.3.** Điểm khi viết lại câu chuẩn theo bốn biến thể rồi chấm lại, tính trên phần bị tác động. Ở cột McNemar, `b` là số bước chuyển từ trúng sang trượt sau khi viết lại, `c` là chiều ngược lại.

| Biến thể | Số câu viết lại | Trên phần bị tác động | McNemar |
|---|---:|---:|---|
| Đổi động từ thao tác | 725 (90,6%) | 76,8 → 77,0 | b=13, c=14, p=1,000 |
| Đảo trật tự mệnh đề | 211 (26,4%) | 89,6 → 90,0 | b=0, c=1, p=1,000 |
| Đổi động từ và đảo trật tự | 203 (25,4%) | 90,1 → 91,1 | b=0, c=2, p=0,480 |
| Bỏ mệnh đề vị trí | 198 (24,8%) | 89,4 → 85,9 | b=8, c=1, **p=0,046** |

Gộp ba biến thể giữ nghĩa, có 1.139 câu viết lại, trong đó 30 câu (2,6%) đổi kết quả chấm. Hiệu ròng là +0,35 điểm, khoảng tin cậy 95% là [-0,59; +1,29], nên loại được mọi mức giảm lớn hơn 0,6 điểm. Ngược lại, bỏ thông tin vị trí làm điểm giảm có ý nghĩa thống kê, đúng như phải xảy ra nếu công cụ đo thật sự đo nội dung. Khi đó trung vị sai số định vị đứng yên ở 0,24% bề ngang màn, chỉ phân vị 90 tăng từ 6,88% lên 31,16%.

**Phạm vi của kết luận.** Công cụ đo bền trước việc đổi động từ và đổi trật tự câu, nhưng chưa chắc bền trước mọi cách diễn đạt lại. Các phép viết lại chỉ đổi động từ trong cùng lớp thao tác (điều kiện khớp thao tác vẫn đạt ở 100% số câu của ba biến thể), không đụng tới phần mô tả phần tử như phép biến đổi của Jandial và cộng sự. Trường hợp đổi chính tên gọi phần tử chưa được kiểm và được ghi là một hạn chế (Mục 7.2).

## 5.9 Chấm lại bằng mô hình định vị thứ hai

UGround đã quen văn phong chú thích của bộ dữ liệu (Mục 5.3), mà các mô hình tinh chỉnh lại được dạy viết đúng văn phong ấy; muốn loại trừ cách giải thích này phải chấm lại bằng một công cụ khác. Công cụ đo thứ hai là UI-Venus-Ground-7B [6], chọn trong mười ứng viên vì có giấy phép mở, kết quả cao hơn UGround trên bộ chuẩn định vị di động, và không dùng AndroidControl khi huấn luyện. Phần được chấm gồm 2.532 bước mà các mô hình viết câu khác nhau; ở các bước còn lại câu trùng nhau nên không ảnh hưởng tới chênh lệch.

Hai công cụ có thang đo khác nhau, nên chúng tôi so chênh lệch giữa các mô hình dưới từng công cụ chứ không so điểm tuyệt đối. Chênh lệch giữa S1 và mô hình gốc dùng làm phép so sánh kiểm chứng, vì đủ lớn và chắc chắn dương. Nếu thang đo mới bị nén, chênh lệch này sẽ co lại rõ, và mọi chênh lệch nhỏ hơn đều không còn tin được.

**Bảng 5.4.** Chênh lệch giữa các mô hình trên cùng 2.532 bước, chấm bằng hai mô hình định vị độc lập. Chênh lệch giữa mô hình mô tả phần tử (S2, một hướng đã thử ở Phụ lục A) và S1 được quy về mẫu số 4.463 để so được với các bảng khác. Trong ngoặc vuông là khoảng tin cậy 95%.

| Phép so | UGround | UI-Venus |
|---|---:|---:|
| S1 - mô hình gốc (Base), phép so sánh kiểm chứng | +10,35 [+8,39; +12,40] | +9,68 [+7,60; +11,78] |
| Mô tả phần tử (S2) - S1 | -1,93 [-3,08; -0,78] | -1,21 [-2,30; -0,12] |
| Ngưỡng tối đa (câu chuẩn) trên mẫu | 70,0% | 69,3% |

**Kết quả của phép so sánh kiểm chứng.** Chênh lệch kiểm chứng đổi từ +10,35 dưới UGround sang +9,68 dưới UI-Venus, tức thang đo không bị nén. Mức hơn của S1 so với mô hình gốc gần như giữ nguyên dưới một công cụ chưa từng học bộ dữ liệu này, nên không phải do công cụ đo quen văn phong, cách giải thích thay thế mạnh nhất mà Chương 6 nêu ra.

**Kết quả trên một chênh lệch nhỏ.** Chênh lệch giữa mô hình mô tả phần tử (S2) và S1 nhỏ hơn nhiều nhưng vẫn âm dưới cả hai công cụ, với mép trên khoảng tin cậy đều dưới không. Dưới UI-Venus, mức thấp hơn của S2 nhỏ đi một chút (tính trên 2.532 bước, hiệu giữa hai mức chênh là +1,26 điểm [+0,04; +2,51]), một phần vì UI-Venus chấm thấp hơn UGround ở cả ba mô hình (39,1 so với 42,5 ở mô hình gốc, 48,7 so với 52,8 ở S1, 46,6 so với 49,5 ở S2) nên mọi hiệu số co lại theo tỉ lệ. Bằng chứng cho việc công cụ đo thiên vị vì vậy là yếu. Nếu thiên vị là nguyên nhân, chênh lệch dưới UI-Venus phải về không hoặc dương, trong khi chênh lệch đo được vẫn âm.

## 5.10 Kiểm chéo bằng một người nghe ngoài họ Qwen

Hai mô hình định vị ở các mục trên đều thuộc họ Qwen-VL, cùng dòng với mô hình được chấm. Vì vậy chúng tôi dùng thêm một mô hình thị giác và ngôn ngữ ngoài họ Qwen, Phi-4-multimodal-instruct [44], làm người nghe, tức bên nhận câu hướng dẫn rồi chọn đúng phần tử trong một câu hỏi trắc nghiệm. Mọi phần tử bấm được trên màn, lấy từ cây trợ năng, được vẽ khung và đánh số lên ảnh theo lối Set-of-Mark [45] (trung vị 15 ô mỗi màn). Người nghe chỉ nhận ảnh đã đánh số và câu hướng dẫn, không kèm mục tiêu tác vụ hay các bước trước; bước được tính đúng khi ô được chọn chứa điểm chạm thật. Cách chấm này tương ứng với độ chính xác hiểu (*comprehension accuracy*) trong các công trình sinh biểu thức quy chiếu [11, 12], đặt trên khung trắc nghiệm theo phần tử như Mind2Web [8]. Người nghe chưa từng học AndroidControl và không được tinh chỉnh.

**Bảng 5.5.** Tỉ lệ chọn đúng của người nghe trắc nghiệm Phi-4 trên 4.463 bước chạm. Đoán ngẫu nhiên đạt 10,1%, và 95,7% số bước có ít nhất một ô chứa điểm chạm thật. Mô hình gốc (Base) chỉ chấm được 3.566 bước vì giới hạn tính toán. Giai đoạn thưởng tọa độ là một hướng đã thử (Phụ lục A).

| Câu đưa cho người nghe | Chọn đúng | KTC 95% |
|---|---:|---:|
| Câu chuẩn | 54,9 | [53,1; 56,8] |
| Giai đoạn thưởng tọa độ (giai đoạn ba) | 45,8 | [44,1; 47,5] |
| S1 (hạt giống 101) | 44,6 | [42,9; 46,4] |
| Mô hình gốc (Base, 3.566 bước) | 38,6 | [36,7; 40,4] |
| Câu chung chung “*Tap the button.*” | 15,9 | [14,7; 17,0] |

Thứ tự trong Bảng 5.5 trùng với thứ tự dưới executability, luật hộp phần tử và luật khoảng cách Euclid (Mục 5.12). Trên dải từ mô hình gốc tới câu chuẩn, mô hình sau giai đoạn thưởng tọa độ nằm ở khoảng 45 đến 48% dải dưới cả bốn cách chấm. Mức hơn của mô hình này so với S1 hạt giống 101 dưới người nghe là +1,14 điểm [+0,23; +2,10], p = 0,020, nằm giữa +0,96 của executability và +1,55 của luật hộp phần tử.

Người nghe cho kết quả tất định (chấm lại 200 bước cho câu trả lời trùng ở mọi bước). Mức đồng thuận từng bước với UGround chỉ vừa phải, hệ số κ (mức đồng thuận đã trừ phần trùng do ngẫu nhiên) từ 0,25 đến 0,44 tuỳ mô hình, nên hai công cụ sai ở những bước khác nhau nhưng vẫn xếp cùng một thứ tự.

Thang của người nghe hẹp hơn: dải giữa câu chuẩn và câu chung chung là 39 điểm, so với 63 điểm của executability, có lẽ vì thiếu mục tiêu tác vụ nên câu chuẩn rất ngắn mất phần ngữ cảnh giúp xác định phần tử. Vì vậy người nghe chỉ dùng để kiểm thứ tự và chiều của các chênh lệch, không dùng làm số chính. Phương pháp đề xuất, S1 hạt giống 202 và mô hình sau giai đoạn học ưu tiên chưa được chấm bằng người nghe này.

## 5.11 So sánh với độ đo dựa trên câu chuẩn

Mục 2.6 đã đo giới hạn của so chuỗi và so vector ngữ nghĩa. Mục này kiểm tiếp tiền đề “một câu chuẩn duy nhất không đủ làm căn cứ để chấm” trên chính các câu ở Chương 6.

Trong những câu được executability chấp nhận, **52,8% số câu của mô hình chưa tinh chỉnh có F1 trên các từ nội dung so với câu chuẩn dưới 0,5, so với 13,9% ở mô hình đã tinh chỉnh**. Tinh chỉnh kéo cách diễn đạt về gần văn phong của người chú thích, nên độ đo dựa trên câu chuẩn phạt hai mô hình không đều nhau vì một tính chất không liên quan tới việc xác định phần tử.

Bảng 6.1 ở Chương 6 có thêm BLEU-4 [20], tính cho từng câu rồi lấy trung bình, và ROUGE-L [21], F1 của chuỗi con chung dài nhất. Với ba loại câu cách xa nhau về chất lượng (câu của mô hình gốc, của S1 và câu chuẩn), hai độ đo này và executability xếp cùng một thứ tự, nên độ đo dựa trên câu chuẩn vẫn dùng được để xếp hạng những mô hình khác nhau nhiều.

Độ đo dựa trên câu chuẩn không làm được hai việc. Thứ nhất, nó không cho biết dư địa còn lại. Câu chuẩn đạt 100 trên ROUGE-L và 96,1 trên BLEU-4 (phần thiếu hoàn toàn do 176 câu chuẩn ngắn hơn bốn token), trong khi executability của câu chuẩn là 75,7 và chỉ ra được phần còn thiếu nằm ở những bước nào. Thứ hai, nó không phân biệt được các mô hình gần nhau. Trong cụm các mô hình đã tinh chỉnh có executability từ 57,2 tới 60,0, ba độ đo cho ba thứ hạng khác nhau (Bảng 6.1). Executability xếp giai đoạn học ưu tiên cao nhất, BLEU-4 xếp mô hình này dưới cả hai hạt giống của S1, còn ROUGE-L xếp mô hình học thêm có giám sát cao nhất (hai hướng đã thử ở Phụ lục A). Đây là những khác biệt dưới hai điểm, vùng mà Zhao và cộng sự [37] chỉ ra rằng độ đo dựa trên tham chiếu không còn đáng tin.

## 5.12 Độ nhạy của kết luận với luật chấm

Luật chấm là một lựa chọn của người nghiên cứu. Chấm lại câu chuẩn, câu của S1 và câu của mô hình gốc trên **698 bước** dưới năm luật, điểm tuyệt đối dao động tới 26 điểm (Bảng 5.6), nên không con số tuyệt đối nào là thuộc tính riêng của mô hình. Thứ tự các mô hình thì không đổi, và chênh lệch giữa S1 và mô hình gốc, từ 9,5 đến 13,0 điểm, lớn hơn nhiều lần sai số chuẩn ghép cặp (Mục 5.13).

**Bảng 5.6.** Ngưỡng tối đa (câu chuẩn) và chênh lệch giữa S1 và mô hình gốc dưới năm luật chấm (698 bước): đĩa Euclid, hình chữ nhật theo từng trục, ô Voronoi, ô Voronoi lấy hạt là tâm hộp chứa `g`, và hộp gần nhất.

|  | Đĩa | Chữ nhật | Voronoi | Voronoi (hạt tâm hộp) | Hộp gần nhất |
|---|---:|---:|---:|---:|---:|
| Ngưỡng tối đa | 80,2 | 82,2 | 74,2 | 56,6 | 82,2 |
| S1 - mô hình gốc (Base) | +12,6 | +13,0 | +11,7 | +9,5 | +13,0 |

**Ảnh hưởng lên kết luận thống kê.** Đổi luật có thể đổi cả kết luận thống kê. Bảng dưới đây so mô hình sau giai đoạn thưởng tọa độ (một hướng đã thử, Phụ lục A) với S1 hạt giống 101 trên 4.463 bước, dưới ba luật cùng đòi đúng loại thao tác; giá trị p được hiệu chỉnh Holm cho ba kiểm định.

| Luật | Δ | p | Sau hiệu chỉnh Holm |
|---|---:|---:|---|
| Cửa sổ ± 14% từng trục | +2,13 | 0,0003 | giữ ý nghĩa |
| Khoảng cách Euclid (AndroidInTheWild) | +1,99 | 0,0010 | giữ ý nghĩa |
| Ô Voronoi (executability) | +0,96 | 0,0860 | mất ý nghĩa |

Kết luận khác nhau vì executability đòi câu dẫn tới đúng phần tử giữa các phần tử lân cận, còn luật dung sai nhận mọi điểm đủ gần đáp án nên có ngưỡng tối thiểu cao hơn (câu chung chung “*Tap the button.*” đạt 12,00 dưới executability, 20,50 dưới luật dung sai). Vì vậy chúng tôi đặt kết quả dưới nhiều luật cạnh nhau, với hai luật đã có tiền lệ dưới đây làm số chính bên cạnh executability.

**Luật hộp phần tử của AndroidControl.** Phụ lục D.3 của bài gốc AndroidControl [1] coi một lần chạm là trúng khi tọa độ dự đoán nằm trong hộp bao của phần tử cần chạm, vì chạm vào đâu trong phần tử thì phần tử cũng kích hoạt; chúng tôi gọi đây là luật hộp phần tử. Hộp bao có sẵn trong nhãn của tập kiểm tra, nên luật này tính được từ các điểm mô hình định vị đã trả về (Bảng 5.7).

**Bảng 5.7.** Điểm theo luật hộp phần tử (Phụ lục D.3 của AndroidControl) trên 4.463 bước, tính sau khi đã có mọi điểm. Giai đoạn học ưu tiên và mô hình chọn ứng viên là hai hướng đã thử (Phụ lục A). Cột cuối đòi thêm điểm dự đoán nằm trong cửa sổ dung sai 14%. Hai hàng ngưỡng tối thiểu đo trên mẫu 800 bước.

|  | Ô Voronoi | Hộp phần tử | Hộp phần tử ∧ cửa sổ 14% |
|---|---:|---:|---:|
| Câu chuẩn | 75,7 | 83,8 | 79,2 |
| Giai đoạn học ưu tiên (MIN-DESC) | 60,0 | 66,5 | 62,7 |
| S1 (hạt giống 101) | 59,1 | 65,5 | 61,7 |
| Mô hình chọn ứng viên (Mục A.3.2) | 56,1 | 62,4 | 58,6 |
| Mô hình gốc (Base) | 47,6 | 53,6 | 49,8 |
| Ngưỡng tối thiểu, câu chung chung (mẫu 800) | 12,0 | 14,1 | 12,1 |
| Ngưỡng tối thiểu, câu của màn hình khác (mẫu 800) | 6,1 | 8,6 | 6,6 |

Thứ tự các hàng không đổi, và chênh lệch giữa S1 và mô hình gốc là 11,9 điểm, gần bằng dưới luật ô Voronoi. Ngưỡng tối đa tăng nhiều hơn hẳn ngưỡng tối thiểu (trên mẫu 800 bước, từ 74,9 lên 83,0), vì dung sai theo cỡ phần tử; theo chiều dọc, hộp cao trung vị 5,2% màn, chặt hơn cửa sổ 14% tới năm lần.

Con số 83,8 của câu chuẩn cần đọc kèm ba lưu ý. Hộp do chúng tôi suy ra từ cây trợ năng (nút nhỏ nhất chứa điểm chạm), nên ở khoảng 48% số bước hộp nhỏ hơn phần tử thật; 78% mức tăng so với ô Voronoi đến từ các bước có hộp rộng hơn nửa màn; và luật được tính sau khi đã có mọi điểm. Vì vậy hai số được đặt song song ở mọi chỗ nêu kết quả chính. Luật hộp phần tử cũng cho thấy ô Voronoi chặt quá mức ở hàng danh sách. Trong 417 bước câu chuẩn trượt ô Voronoi nhưng đạt luật hộp, khoảng một nửa trượt vì điểm dự đoán nằm gần một mảnh chữ do bộ nhận dạng chữ (OCR) tách ra trên cùng hàng, và mảnh chữ ấy bị coi là một phần tử cạnh tranh trong `E` (Mục 7.2).

**Luật khoảng cách Euclid của AndroidInTheWild.** Luật thứ hai, gọi là luật khoảng cách Euclid, lấy từ mã chấm gốc của AndroidInTheWild [2], bộ dữ liệu điều khiển thiết bị Android được nhiều tác tử giao diện dùng. Hai lần chạm được coi là trùng khi khoảng cách Euclid giữa hai điểm, trên tọa độ chuẩn hoá về [0; 1], không vượt quá 0,14, hoặc khi cả hai điểm cùng nằm trong một khung phần tử đã nới thêm 1,4 lần chiều cao và 1,4 lần bề ngang; chúng tôi thêm điều kiện đúng loại thao tác. Mã gốc xét mọi khung chú thích trên màn, còn chúng tôi chỉ có khung của phần tử cần chạm, nên bản xấp xỉ này chỉ có thể cho điểm thấp hơn luật gốc. Trên mẫu 800 bước, dải giữa ngưỡng tối đa (90,8) và ngưỡng tối thiểu là 64,9 điểm, rộng hơn mức 62,9 của executability. Tuy vậy luật này ít phạt việc thiếu tên phần tử: câu bỏ tên giữ vị trí chỉ thấp hơn ngưỡng tối đa 4,5 điểm, so với 6,9 điểm dưới executability (Mục 5.6.1). Vì vậy luật khoảng cách Euclid luôn đi cạnh executability chứ không thay thế; điểm của từng mô hình nằm ở Bảng 6.5.

**Cận trên của luật khoảng cách Euclid.** Biến thể ngược lại cho vẽ khung xét mọi phần tử bấm được trên màn (lấy từ cây trợ năng, chiếm không quá nửa màn), nên luật gốc nằm giữa hai biến thể. Dưới cận trên, câu chuẩn đạt 96,2% nhưng câu chung chung cũng lên 41,6 (mẫu 800 bước), nên dải chỉ còn 54,3 điểm, hẹp hơn cả executability. Vì vậy kết quả theo luật khoảng cách Euclid được nêu dưới dạng khoảng giữa hai biến thể, số chính là cận dưới.

## 5.13 Thống kê

**Ước lượng điểm.** Điểm được tính theo cách vi mô, tức tổng số bước đúng chia tổng số bước, không lấy trung bình theo ứng dụng.

**Khoảng tin cậy.** Khoảng tin cậy dùng bootstrap phi tham số 10.000 lần, gom cụm theo ứng dụng: mỗi lần rút lại nguyên cả cụm có hoàn lại rồi tính lại điểm, và khoảng tin cậy là khoảng giữa hai phân vị của các giá trị thu được. Cameron và cộng sự [27] cho thấy cách tính này có độ phủ thấp hơn mức danh nghĩa khi số cụm ít, nên chúng tôi ghi số cụm cạnh mọi khoảng tin cậy.

**Luật gom cụm.** Bước không quy được về ứng dụng thì mỗi tác vụ là một cụm riêng, để không gộp các tác vụ không liên quan chỉ vì cùng thiếu nhãn ứng dụng. Tổng cộng có 1.091 cụm, cụm lớn nhất gồm 58 bước; vì cỡ cụm rất khác nhau, số cụm hiệu dụng theo công thức Kish [28] (số cụm có đều cho cùng độ chính xác) chỉ là 454,3. Cách gom cụm này không làm thay đổi kết luận: khoảng tin cậy của mức hơn giữa S1 và mô hình gốc là [+10,0; +13,1], giống hệt khi gom mọi bước theo tác vụ (1.345 cụm), và là [+10,2; +13,8] khi dồn mọi bước không nhãn vào một cụm (260 cụm). Nếu chỉ giữ 40,7% số bước quy được ứng dụng, số cụm hiệu dụng còn 107 và lực thống kê giảm mạnh.

**Sai số chuẩn ghép cặp.** Mọi mô hình được chấm trên cùng 4.463 bước nên phân tích phải ghép cặp. Hệ số nở do gom cụm (mức phóng to độ bất định do các bước cùng cụm tương quan) chỉ là 1,10. Sai số chuẩn của hiệu ghép cặp giữa S1 và mô hình gốc là 0,79 điểm, so với 1,05 điểm nếu tính như hai tỉ lệ độc lập; các cặp mô hình gần nhau hơn thường có sai số nhỏ hơn. Mỗi cặp mô hình được so bằng khoảng tin cậy ghép cặp và giá trị p của kiểm định McNemar (Mục 4.8), chỉ dựa trên các bước hai mô hình cho kết quả khác nhau, với `b` là số bước mô hình thứ nhất trúng còn mô hình thứ hai trượt và `c` là chiều ngược lại. Mức dao động khi chỉ huấn luyện lại với hạt giống khác không thuộc sai số của độ đo và được đo riêng ở Mục 6.7.

**Đánh giá ở bước không chạm.** Executability chỉ chấm bước chạm, trong khi 35,9% số bước của tập kiểm tra là bước không chạm (cuộn, chờ, gõ, mở ứng dụng, quay lại). Một mô hình có thể tăng điểm ở bước chạm nhờ thiên về câu mô tả thao tác chạm rồi kém đi ở các bước còn lại mà độ đo chính không thấy. Vì vậy các mô hình huấn luyện thêm được kiểm ở nhóm bước này bằng mức khớp loại thao tác, tính bằng chính hàm chuẩn hoá của độ đo chính. Kết quả cho các hướng đã thử nằm ở Mục A.2.2.4.

# Chương 6. Thực nghiệm và kết quả

Chương này trình bày kết quả của phương pháp đề xuất trên tập kiểm tra: kết quả chính, rồi từng thành phần (Mục 6.3 và Mục 6.4), rồi các phần kiểm độ vững của kết quả. Các hướng đã thử trước đó được tóm tắt ở Mục 6.10 và trình bày chi tiết ở Phụ lục A.

## 6.1 Thiết lập thực nghiệm

Mọi mô hình được chấm trên cùng 4.463 bước chạm của tập kiểm tra, bằng cùng một bản mã chấm. Phương pháp đề xuất gồm mô hình học với thưởng SPICE, viết câu nháp, và ACE, quyết định có thay câu nháp bằng câu ví dụ hay không (Mục 4.4 đến Mục 4.6).

Ba mốc so sánh (Mục 4.7) là mô hình gốc (**Base** trong các bảng), mô hình tinh chỉnh có giám sát ở hai hạt giống 101 và 202 (**S1** trong các bảng) và câu chuẩn đưa thẳng tới chấm, cho mức ngưỡng tối đa của độ đo. Ở một bước, S1 trả về câu rỗng; bước này được tính là không đạt và vẫn nằm trong mẫu số 4.463. Các phép so ghép cặp bỏ bước ấy, và không số nào đổi sau khi làm tròn tới một chữ số thập phân.

## 6.2 Kết quả chính

**Bảng 6.1.** Kết quả chính trên 4.463 bước chạm của tập kiểm tra. **Exec.** là executability, **KTC 95%** là khoảng tin cậy 95% của executability. **Hộp phần tử** là luật của AndroidControl, **khoảng cách Euclid** là luật của AndroidInTheWild. **BLEU-4** là trung bình theo câu, **ROUGE-L** theo F1. Số in đậm là số cao nhất của cột, không tính hàng câu chuẩn.

| Mô hình | Exec. | KTC 95% | Hộp phần tử | Khoảng cách Euclid | BLEU-4 | ROUGE-L |
|---|---:|---:|---:|---:|---:|---:|
| **Mốc so sánh** |||||||
| Mô hình gốc (Base) | 47,6 | [45,9; 49,3] | 53,6 | 63,4 | 9,9 | 40,4 |
| Tinh chỉnh có giám sát (S1), hạt giống 101 | 59,1 | [57,3; 60,8] | 65,5 | 74,4 | 38,7 | 67,3 |
| Tinh chỉnh có giám sát (S1), hạt giống 202 | 59,6 | [57,9; 61,3] | 66,1 | 75,3 | 39,0 | 67,6 |
| **Phương pháp đề xuất** |||||||
| Thành phần thứ nhất (học với thưởng SPICE) | 60,6 | [58,9; 62,4] | 67,0 | 76,2 | 40,1 | 68,3 |
| Cả hai thành phần (thưởng SPICE + ACE) | 60,7 | [58,9; 62,4] | 67,1 | 76,3 | 41,2 | 69,1 |
| **Các hướng đã thử (Phụ lục A)** |||||||
| Mô tả phần tử (S2) | 57,2 | [55,4; 58,9] | 63,6 | 73,4 | 36,4 | 65,9 |
| Học thêm có giám sát (CE2-S2) | 59,4 | [57,7; 61,1] | 66,0 | 76,1 | 38,1 | 68,6 |
| Học ưu tiên trên dòng mô tả (MIN-DESC) | 60,0 | [58,3; 61,8] | 66,5 | 76,4 | 37,9 | 68,4 |
| Thưởng tọa độ (giai đoạn ba) | 60,1 | [58,3; 61,8] | 67,0 | 77,3 | 37,8 | 68,5 |
| Chọn ứng viên† | 56,1 | [54,2; 58,0] | 62,4 | 71,2 | 34,5 | 63,0 |
| Sửa câu theo vùng cắt (TAGE) | 60,2 | [58,5; 62,0] | 66,4 | 76,1 | 40,1 | 68,4 |
| Câu chuẩn (ngưỡng tối đa) | 75,7 | [74,1; 77,3] | 83,8 | 92,1 | 96,1 | 100,0 |

† Mô hình chọn ứng viên khác các mô hình còn lại ở ba yếu tố của thiết lập (Mục A.3.1), nên chỉ so được với mô hình gốc (Mục A.3.2). Các hướng đã thử khác (mô-đun định vị, đưa vai trò và vùng của phần tử vào mô hình, làm nét ảnh, mở khoá phần thị giác) không có trong bảng vì chỉ được chấm trên tập kiểm định nội bộ (Mục A.6).

Theo Bảng 6.1, phương pháp đề xuất đạt **executability 60,7%**: ở 60,7% số bước chạm, câu viết ra gọi đúng loại thao tác và dẫn mô hình định vị tới đúng phần tử cần chạm. Mức này hơn S1, hạt giống 101, là **1,57 điểm**, với khoảng tin cậy **[+0,86; +2,31]** nằm hoàn toàn trên 0. Phương pháp cũng cao nhất bảng dưới luật hộp phần tử và ở cả hai độ đo so câu; riêng dưới luật khoảng cách Euclid, giai đoạn thưởng tọa độ cao hơn.

Phần lớn mức hơn theo executability đến từ thành phần thứ nhất; riêng mô hình học với thưởng SPICE đã đạt **60,6%** (Mục 6.3). ACE giữ nguyên executability và nâng nhóm độ đo so câu (Mục 6.4). Bảng 6.2 tách executability thành ba điều kiện (đúng ô Voronoi, đúng loại thao tác, trong cửa sổ dung sai) để thấy mức hơn của mỗi mô hình nằm ở điều kiện nào.

**Bảng 6.2.** Phân rã executability theo từng điều kiện hợp thành (tỉ lệ bước, %). **Executable**: thoả mọi điều kiện. **Chỉ ô Voronoi**: điểm định vị nằm trong cửa sổ dung sai và trong ô Voronoi của phần tử cần chạm, chưa xét loại thao tác. **Khớp thao tác**: câu gọi đúng loại thao tác. **Cửa sổ dung sai**: điểm định vị nằm trong cửa sổ ±14% theo từng trục quanh điểm chạm chuẩn.

| Mô hình | Executable | Chỉ ô Voronoi | Khớp thao tác | Cửa sổ dung sai |
|---|---:|---:|---:|---:|
| Câu chuẩn (ngưỡng tối đa) | 75,7 | 75,8 | 100,0 | 84,3 |
| Phương pháp đề xuất | 60,7 | 61,5 | 96,0 | 70,4 |
| Thành phần thứ nhất | 60,6 | 61,4 | 96,0 | 70,3 |
| Sửa câu theo vùng cắt (TAGE) | 60,2 | 61,0 | 96,6 | 70,1 |
| Thưởng tọa độ (giai đoạn ba) | 60,1 | 60,5 | 98,9 | 69,9 |
| Học ưu tiên trên dòng mô tả (MIN-DESC) | 60,0 | 60,4 | 98,9 | 69,2 |
| S1 (hạt giống 202) | 59,6 | 60,7 | 94,6 | 69,8 |
| Học thêm có giám sát (CE2-S2) | 59,4 | 59,8 | 98,9 | 68,9 |
| S1 (hạt giống 101) | 59,1 | 60,2 | 94,4 | 69,2 |
| Mô tả phần tử (S2) | 57,2 | 58,1 | 94,8 | 67,4 |
| Chọn ứng viên† | 56,1 | 57,4 | 90,9 | 66,3 |
| Mô hình gốc (Base) | 47,6 | 48,9 | 96,5 | 57,6 |

Ở hàng câu chuẩn, câu được chấm chính là câu chuẩn nên điều kiện khớp thao tác luôn thoả. Mức khớp thao tác 98,9% của giai đoạn học ưu tiên, mô hình học thêm có giám sát và giai đoạn thưởng tọa độ chỉ đo trên bước chạm, nên cần đặt cạnh mức giảm ở bước không chạm (Mục A.2.2.4). Mô hình chọn ứng viên (†) chỉ so được với mô hình gốc (Mục A.3.2); mức khớp thao tác của mô hình này thấp nhất bảng vì mô hình hay viết câu không chạm ở những bước không chọn phần tử nào trong danh sách ứng viên.

**Khoảng cách giữa các mốc.** Khoảng tin cậy của mô hình gốc, S1 và câu chuẩn không chồng lên nhau, nên độ đo phân biệt được cả ba mốc. S1 còn cách ngưỡng tối đa khá xa (Mục 5.5, Mục 6.9.4), và mọi mô hình đều nằm xa ngưỡng tối thiểu (Mục 6.6).

## 6.3 Thành phần thứ nhất: học tăng cường thưởng SPICE

Mục này xét thành phần thứ nhất khi đứng một mình (thiết kế ở Mục 4.5). Mô hình học với thưởng SPICE học tiếp từ S1, hạt giống 101, nên được so với chính mô hình ấy.

### 6.3.1 Kết quả trên bước chạm

**Bảng 6.3.** Mô hình học với thưởng SPICE so với S1, hạt giống 101, trên 4.463 bước chạm, ghép cặp theo bước. Sáu hàng trên là độ đo theo vị trí (gồm cả tỉ lệ đúng loại thao tác), bảy hàng dưới là độ đo so với câu chuẩn. Δ là điểm của mô hình học với thưởng SPICE trừ điểm của S1; KTC 95% từ bootstrap gom cụm theo ứng dụng (Mục 5.13). Cứu là số bước mô hình mới đúng còn S1 sai; phá là chiều ngược lại.

| Độ đo | S1 | Thưởng SPICE | Δ | KTC 95% | cứu / phá |
|---|---:|---:|---:|---:|---:|
| Executability | 59,11 | 60,65 | +1,55 | [+0,80; +2,33] | 159 / 90 |
| Luật hộp phần tử | 65,49 | 67,02 | +1,52 | [+0,77; +2,29] | 165 / 97 |
| Luật khoảng cách Euclid | 74,37 | 76,25 | +1,88 | [+1,17; +2,63] | 172 / 88 |
| Euclid cận trên | 81,04 | 82,90 | +1,86 | [+1,17; +2,60] | 163 / 80 |
| ±14% theo trục | 67,24 | 68,90 | +1,66 | [+0,90; +2,46] | 172 / 98 |
| Đúng loại thao tác | 94,35 | 95,97 | +1,61 | [+1,17; +2,08] | 83 / 11 |
| SPICE | 44,37 | 45,79 | +1,42 |  |  |
| BLEU-4 | 51,56 | 52,36 | +0,80 |  |  |
| METEOR | 36,79 | 37,92 | +1,13 |  |  |
| ROUGE-L | 67,35 | 68,36 | +1,01 |  |  |
| CIDEr-D | 416,12 | 430,05 | +13,93 |  |  |
| chrF | 61,26 | 62,87 | +1,61 |  |  |
| BERTScore | 66,33 | 67,07 | +0,74 |  |  |

Mô hình học với thưởng SPICE cao hơn S1 ở cả mười ba độ đo của Bảng 6.3; ở sáu độ đo vị trí, khoảng tin cậy đều nằm trên 0. Theo executability, **p = 1,6 × 10^-5** (kiểm định McNemar, Mục 6.6). Đây là mô hình đầu tiên của đề tài hơn S1 có ý nghĩa thống kê theo executability, luật chặt nhất đã dùng; các hướng đã thử trước đó chỉ hơn có ý nghĩa dưới luật lỏng hơn. Phần thưởng chỉ dùng SPICE, một độ đo so câu, và mô hình định vị không tham gia vào phần thưởng, nhưng các độ đo vị trí vẫn tăng một cỡ tương tự.

**Mức tăng đến từ đâu.** Có 36 trong 159 bước được cứu là do S1 viết sai loại thao tác, còn chỉ 8 trong 90 bước bị phá là do mô hình mới viết sai loại thao tác; phần sửa loại thao tác góp ròng 28 bước (+0,63 điểm). Phần còn lại, 41 bước (+0,92 điểm), nằm ở 4.200 bước mà cả hai mô hình đều gọi đúng loại thao tác, nơi executability đi từ 62,62 lên 63,60. Vậy hơn một nửa mức tăng đến từ việc câu chỉ đúng phần tử cần chạm hơn, khác với giai đoạn thưởng tọa độ, vốn có toàn bộ mức hơn nằm ở các bước S1 viết sai loại thao tác (Mục 6.5).

Câu của mô hình thay đổi ít so với S1: 2.795 trong 4.463 câu trùng đến từng ký tự, và số từ trung bình chỉ đi từ 7,83 lên 7,96, nên mức tăng không đến từ việc viết câu dài hơn (Hình 6.1 minh hoạ một bước được cứu).

**Hình 6.1.** Một bước được mô hình học với thưởng SPICE sửa đúng (ảnh chỉ giữ phần dưới màn hình). Cần chạm nút *Not now* ở cuối màn, trong khi một hộp thoại hỏi quyền gửi thông báo đang che màn hình. S1 gọi nút *Allow* trong hộp thoại nên mô hình định vị trượt; mô hình học với thưởng SPICE gọi đúng nút *Not now* kèm vị trí, và mô hình định vị trỏ trúng.

**So với các mô hình khác.** Mô hình vẫn hơn S1 hạt giống 202 có ý nghĩa (**p = 0,014**), nên mức hơn không phải do may rủi của riêng hạt giống 101. So với giai đoạn thưởng tọa độ và giai đoạn học ưu tiên, hai hướng đã thử có executability cao nhất, mức hơn chỉ khoảng 0,6 điểm và chưa phân biệt được với 0 (Bảng 6.8). Giai đoạn thưởng tọa độ cao hơn ở tỉ lệ đúng loại thao tác và ở ba luật vị trí lỏng hơn executability; mô hình học với thưởng SPICE cao hơn ở executability và sáu trong bảy độ đo so câu (Hình 6.2).

### 6.3.2 Giới hạn của kết quả

Hai giới hạn của thiết kế đã nêu ở Mục 4.5 vẫn áp dụng cho kết quả trên: chưa có mô hình chỉ học thêm có giám sát cùng số bước để tách phần do phần thưởng SPICE, và hai mô hình sinh câu theo hai cách khác nhau. Mức hơn giữ dấu khi so với cả hai hạt giống của S1.

## 6.4 Thành phần thứ hai: chép câu ví dụ khi đồng thuận loại thao tác (ACE)

Trên tập kiểm tra, luật đồng thuận của ACE (Mục 4.6) thay **402** trong **4.463** câu nháp (**9,0%**). Bảng 6.4 đặt ACE, tức phương pháp đề xuất, cạnh câu nháp và cạnh bộ sinh đứng một mình (dùng câu của bộ sinh ở mọi bước).

**Bảng 6.4.** ACE trên 4.463 bước chạm, so với câu nháp (của mô hình học với thưởng SPICE) và với bộ sinh đứng một mình. Ba độ đo vị trí kèm khoảng tin cậy 95% từ bootstrap gom cụm theo ứng dụng. Bảy độ đo so câu chưa có khoảng tin cậy; cột **ACE - câu nháp** lệch tối đa 0,02 so với Bảng 6.3 do chấm lại.

| Độ đo | Câu nháp | Bộ sinh một mình | ACE | ACE - câu nháp |
|---|---:|---:|---:|---:|
| Executability | 60,65 | 59,40 | 60,68 | +0,02 [-0,21; +0,26] |
| Luật hộp phần tử | 67,02 | 65,81 | 67,11 | +0,09 [-0,15; +0,33] |
| Luật khoảng cách Euclid | 76,25 | 75,02 | 76,32 | +0,07 [-0,15; +0,29] |
| BLEU-4 | 52,36 | 53,47 | 53,47 | +1,11 |
| METEOR | 37,91 | 37,79 | 38,37 | +0,46 |
| ROUGE-L | 68,34 | 68,67 | 69,08 | +0,74 |
| CIDEr-D | 430,04 | 437,54 | 442,02 | +11,98 |
| SPICE | 45,79 | 46,79 | 47,13 | +1,34 |
| chrF | 62,86 | 62,65 | 63,44 | +0,58 |
| BERTScore | 67,07 | 67,52 | 67,73 | +0,66 |

**Kết quả.** ACE cao hơn câu nháp ở cả bảy độ đo so câu, rõ nhất ở CIDEr-D và SPICE. Ở ba độ đo vị trí, khoảng tin cậy đều phủ 0, nên về định vị ACE ngang câu nháp; trong 402 câu bị thay, 15 bước được cứu và 14 bước bị phá (**p = 1,0**). Vì vậy phương pháp đề xuất giữ gần nguyên mức hơn S1 của câu nháp; theo luật hộp phần tử và luật khoảng cách Euclid, mức hơn là **1,61** và **1,95** điểm, đều với **p < 0,001**. Trong các cách làm của đề tài, chỉ ACE nâng được nhóm độ đo so câu so với thành phần thứ nhất mà không làm giảm độ đo vị trí nào, nên ACE được giữ làm thành phần thứ hai.

**Vì sao không dùng bộ sinh một mình.** Bộ sinh đứng một mình cao hơn câu nháp ở năm trong bảy độ đo so câu, nhưng thấp hơn **1,25 điểm executability** **[-2,06; -0,44]** (**p = 0,002**) và giảm tương tự dưới hai luật vị trí còn lại, vì hai loại bước cho kết quả trái ngược nhau. Ở **19,1%** số bước, bộ sinh chép nguyên văn một câu ví dụ, và **43,5%** số câu chép ấy trùng câu chuẩn, gần gấp đôi tỉ lệ của câu nháp (**22,8%**). Ở những bước bộ sinh tự viết câu mới, câu viết ra kém câu nháp, như ở mọi lượt học thêm sau mô hình học với thưởng SPICE (Phụ lục A).

**Vì sao cần điều kiện loại thao tác.** Nếu chỉ dùng điều kiện chép, luật thay **453** câu, vẫn tăng cả bảy độ đo so câu, nhưng executability thấp hơn câu nháp **0,11 điểm** (24 bước cứu, 29 bước phá). Điều kiện loại bớt **51** câu, phần lớn là câu vuốt, quay lại hoặc gõ chữ bị chép vào bước mà câu nháp dẫn tới thao tác chạm; trên 51 bước ấy, câu chép cứu 9 bước và phá 15 bước. Nhờ vậy ACE cao hơn biến thể chỉ có điều kiện chép **0,13 điểm executability** và không thấp hơn ở độ đo nào của Bảng 6.4.

**Giới hạn.** Kết quả của ACE cần được đọc kèm bốn giới hạn. Thứ nhất, luật được chọn trong bốn biến thể trên tập kiểm định nội bộ, và các biến thể ấy được nghĩ ra sau khi đã thấy kết quả của bộ sinh trên tập đó; tập kiểm tra chỉ được dùng một lần, cho biến thể đã chọn. Thứ hai, mức tăng ở độ đo so câu chưa có khoảng tin cậy, và các mức dưới một điểm (METEOR, ROUGE-L, chrF, BERTScore) chưa đủ để kết luận. Thứ ba, chưa rõ truy hồi câu ví dụ giúp được bao nhiêu, vì trên tập kiểm định nội bộ, ở đa số độ đo, bộ sinh không hơn mô hình học thêm cùng số bước mà không xem câu ví dụ. Thứ tư, phần lỗi nằm ở bề mặt câu (mức trùng từ với câu chuẩn), chưa giúp mô hình định vị tìm đúng phần tử hơn, nên ACE không khắc phục được nhược điểm đó ở khâu nhận ra phần tử (Mục A.5).

## 6.5 Kết quả trên nhiều độ đo

Ngoài executability, chúng tôi trình bày nhóm độ đo theo vị trí và nhóm độ đo so với câu chuẩn, cả hai tính lại từ bản ghi từng bước của các lượt chấm ở Bảng 6.1. Hai bảng của mục này chưa có hàng của phương pháp đề xuất; số của phương pháp nằm ở Bảng 6.1 và Bảng 6.4.

**Bảng 6.5.** Nhóm độ đo theo vị trí trên đủ 4.463 bước chạm, tính lại từ bản ghi từng bước, không gọi lại mô hình định vị. Khoảng cách Euclid là luật khoảng cách Euclid trong mã chấm gốc của AndroidInTheWild; khoảng cách Euclid cận trên là biến thể của luật ấy khi vẽ khung xét mọi phần tử bấm được trên màn (Mục 5.12). Hộp phần tử là luật khớp gốc của AndroidControl. **Exec.** là executability (Mục 5.12). **Thao tác** là tỉ lệ gọi đúng loại thao tác. Số in đậm là số cao nhất trong các mô hình ở cột đó. *Thưởng SPICE là thành phần thứ nhất của phương pháp đề xuất, học tiếp từ S1 (101) bằng GRPO với phần thưởng SPICE, TAGE là bộ sửa câu đã thử đặt sau thành phần đó (Mục 6.3 và A.7.2). Bảng chưa có hàng của phương pháp đề xuất; số của phương pháp này ở Bảng 6.4. †Mô hình chọn ứng viên lệch ba biến so với các mô hình còn lại nên chỉ đọc được so với Base.

| Mô hình | Euclid | Hộp phần tử | Exec. | ±14% trục | Euclid cận trên | Thao tác |
|---|---:|---:|---:|---:|---:|---:|
| Base | 63,4 | 53,6 | 47,6 | 55,9 | 73,4 | 96,5 |
| S1 (101) | 74,4 | 65,5 | 59,1 | 67,2 | 81,0 | 94,3 |
| S1 (202) | 75,3 | 66,1 | 59,6 | 67,9 | 81,9 | 94,6 |
| S2 | 73,4 | 63,6 | 57,2 | 65,7 | 80,8 | 94,8 |
| CE2-S2 | 76,1 | 66,0 | 59,4 | 68,5 | 83,9 | 98,9 |
| MIN-DESC | 76,4 | 66,5 | 60,0 | 68,7 | 84,4 | 98,9 |
| Giai đoạn ba | 77,3 | 67,0 | 60,1 | 69,4 | 85,0 | 98,9 |
| Thưởng SPICE* | 76,2 | 67,0 | 60,6 | 68,9 | 82,9 | 96,0 |
| TAGE | 76,1 | 66,4 | 60,2 | 68,7 | 82,7 | 96,6 |
| Chọn ứng viên† | 71,2 | 62,4 | 56,1 | 63,9 | 77,9 | 90,9 |
| Câu chuẩn | 92,1 | 83,8 | 75,7 | 84,2 | 96,2 | 100,0 |

**Bảng 6.6.** Nhóm độ đo so với câu chuẩn trên đủ 4.463 bước chạm. BLEU-4, METEOR 1.5, ROUGE-L, CIDEr-D và SPICE tính mức cho bằng bộ chấm chính thức của COCO Captions, sau khi tách từ bằng PTBTokenizer. chrF tính bằng sacreBLEU. BERTScore là F1 với **roberta-large** tầng 17, đã hiệu chỉnh theo đường cơ sở. Mỗi bước chỉ có một câu chuẩn. Số in đậm là số cao nhất trong các mô hình ở cột đó. Giai đoạn ba là giai đoạn thưởng tọa độ, học tiếp từ MIN-DESC với phần thưởng đặt trên tọa độ trong dòng mô tả. *Thành phần thứ nhất của phương pháp đề xuất; số của phương pháp đề xuất ở Bảng 6.4. Với TAGE mới tính SPICE. †Mô hình chọn ứng viên chỉ đọc được so với Base.

| Mô hình | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base | 15,3 | 24,6 | 42,3 | 88,0 | 18,5 | 40,2 | 40,1 |
| S1 (101) | 51,6 | 36,8 | 67,3 | 416,1 | 44,4 | 61,3 | 66,3 |
| S1 (202) | 51,7 | 37,2 | 67,7 | 419,2 | 44,2 | 61,9 | 66,8 |
| S2 | 48,7 | 35,8 | 66,0 | 387,7 | 41,3 | 59,9 | 65,1 |
| CE2-S2 | 50,1 | 37,3 | 68,6 | 402,2 | 42,3 | 61,9 | 66,8 |
| MIN-DESC | 49,9 | 37,3 | 68,5 | 401,0 | 42,2 | 61,8 | 66,7 |
| Giai đoạn ba | 49,9 | 37,3 | 68,5 | 402,9 | 42,5 | 61,9 | 66,8 |
| Thưởng SPICE* | 52,4 | 37,9 | 68,4 | 430,1 | 45,8 | 62,9 | 67,1 |
| TAGE | – | – | – | – | 45,7 | – | – |
| Chọn ứng viên† | 46,9 | 34,2 | 63,3 | 370,6 | 39,3 | 57,7 | 62,8 |
| Câu chuẩn | 100,0 | 100,0 | 100,0 | 988,7 | 98,6 | 100,0 | 100,0 |

**Bảng 6.7.** Khoảng tin cậy 95% của ba số chính trên 4.463 bước (trên) và phép so ghép cặp (dưới). Khoảng tin cậy lấy từ bootstrap 10.000 lần gom cụm theo ứng dụng (**G = 1.091**), giá trị p của kiểm định McNemar. **MIN** là MIN-DESC.

| Mô hình | Euclid | Hộp phần tử | Executability |
|---|---|---|---|
| Base | 63,4 [61,8; 65,0] | 53,6 [51,9; 55,3] | 47,6 [45,9; 49,3] |
| S1 (101) | 74,4 [72,8; 75,8] | 65,5 [63,8; 67,2] | 59,1 [57,3; 60,8] |
| S1 (202) | 75,3 [73,8; 76,7] | 66,1 [64,4; 67,7] | 59,6 [57,9; 61,3] |
| MIN | 76,4 [74,9; 77,8] | 66,5 [64,9; 68,2] | 60,0 [58,3; 61,8] |
| Giai đoạn ba | 77,3 [75,8; 78,8] | 67,0 [65,3; 68,7] | 60,1 [58,3; 61,8] |
| Câu chuẩn | 92,1 [91,1; 93,1] | 83,8 [82,5; 85,1] | 75,7 [74,1; 77,3] |

| Phép so | Luật | Δ | KTC 95% | p |
|---|---|---:|---:|---:|
| S1 (101) - Base | Euclid | +10,98 | [+9,44; +12,56] | <0,001 |
|  | Hộp phần tử | +11,90 | [+10,36; +13,47] | <0,001 |
|  | Exec. | +11,52 | [+10,02; +13,07] | <0,001 |
| S2 - S1 (101) | Euclid | -0,96 | [-2,18; +0,29] | 0,100 |
|  | Hộp phần tử | -1,86 | [-3,04; -0,67] | <0,001 |
|  | Exec. | -1,93 | [-3,06; -0,75] | <0,001 |
| Giai đoạn ba - S2 | Euclid | +3,90 | [+2,90; +4,90] | <0,001 |
|  | Hộp phần tử | +3,41 | [+2,37; +4,41] | <0,001 |
|  | Exec. | +2,89 | [+1,91; +3,84] | <0,001 |
| Giai đoạn ba - S1 (101) | Euclid | +2,94 | [+1,77; +4,08] | <0,001 |
|  | Hộp phần tử | +1,55 | [+0,40; +2,69] | 0,008 |
|  | Exec. | +0,96 | [-0,16; +2,11] | 0,090 |
| Giai đoạn ba - S1 (202) | Euclid | +1,99 | [+0,84; +3,13] | <0,001 |
|  | Hộp phần tử | +0,94 | [-0,17; +2,04] | 0,109 |
|  | Exec. | +0,45 | [-0,67; +1,54] | 0,450 |
| MIN - S1 (101) | Euclid | +2,04 | [+0,89; +3,20] | <0,001 |
|  | Hộp phần tử | +1,05 | [-0,11; +2,20] | 0,078 |
| Giai đoạn ba - MIN | Euclid | +0,90 | [+0,27; +1,52] | 0,007 |
|  | Hộp phần tử | +0,49 | [-0,13; +1,10] | 0,149 |
|  | Exec. | +0,02 | [-0,57; +0,61] | 1,000 |

**Hình 6.2.** Các mô hình chính dưới ba luật chấm trên 4.463 bước chạm. Cột nền xám là mốc câu chuẩn. Thứ tự gần như giữ nguyên qua ba luật; riêng giai đoạn thưởng tọa độ (giai đoạn ba) cao hơn dưới luật khoảng cách Euclid, còn mô hình học với thưởng SPICE cao hơn dưới executability.
**Nhóm độ đo theo vị trí.** Bảng 6.5 đặt cạnh nhau ba luật chấm chính (luật khoảng cách Euclid, luật hộp phần tử và executability) cùng hai biến thể ở Mục 5.12. Phương pháp đề xuất đạt 76,3% theo luật khoảng cách Euclid, so với 74,4% của S1 hạt giống 101. Trong các hướng đã thử, giai đoạn thưởng tọa độ cao nhất theo luật khoảng cách Euclid, 77,3%. Thứ tự các mô hình dưới hai luật vị trí gần như trùng với thứ tự dưới executability.

**Sai số và kết luận dưới ba luật.** Bảng 6.7 cho khoảng tin cậy dưới ba luật, tính trên cùng các mẫu bootstrap nên các cột so sánh được với nhau. Chênh lệch giữa S1 hạt giống 101 và mô hình gốc giữ gần nguyên qua ba luật, đều với p < 0,001, và phương pháp đề xuất hơn S1 có ý nghĩa dưới cả ba luật (Mục 6.4). Với các hướng đã thử, kết luận đổi tùy luật. Mô hình mô tả phần tử thấp hơn S1 có ý nghĩa theo executability (Mục A.1.3) nhưng không theo luật khoảng cách Euclid. Theo luật khoảng cách Euclid, phần lớn mức hơn của giai đoạn học ưu tiên và giai đoạn thưởng tọa độ so với mô hình mô tả phần tử có được chỉ nhờ học tiếp, vì mô hình chỉ học thêm có giám sát với cùng số bước cũng đạt phần lớn mức hơn ấy. Giai đoạn thưởng tọa độ hơn S1 có ý nghĩa theo hai luật vị trí, nhưng không theo executability.

> Toàn bộ mức hơn theo luật khoảng cách Euclid ấy nằm ở 256 bước (5,7%) mà S1 viết sai loại thao tác, chẳng hạn viết vuốt hay cuộn khi cần chạm. Nhóm này góp +3,11 điểm theo luật khoảng cách Euclid và +1,97 theo executability; so với hạt giống 202, nhóm này góp +3,09 điểm. Ở 4.189 bước cả hai cùng gọi đúng loại thao tác, tỉ lệ trúng gần như bằng nhau (79,04% so với 78,92%). Luật khoảng cách Euclid cũng không phạt những lần chạm rơi vào phần tử sát bên, còn executability thì phạt; giai đoạn thưởng tọa độ mắc lỗi này nhiều hơn, nên trên nhóm bước cùng gọi đúng loại thao tác, giai đoạn này thấp hơn S1 0,81 điểm theo executability. Vậy đóng góp của hai giai đoạn này nằm ở việc gọi đúng loại thao tác, chưa nằm ở việc định vị phần tử tốt hơn.

**Nhóm độ đo so với câu chuẩn.** Bảng 6.6 dùng các độ đo của Widget Captioning [9] và Screen2Words [10], gồm BLEU [20], METEOR [22], ROUGE-L [21], CIDEr [23] và SPICE [24], cùng chrF [25] và BERTScore [26]. BLEU-4 ở bảng này tính trên toàn tập theo bộ chấm của COCO Captions, nên khác BLEU-4 trung bình theo câu ở Bảng 6.1. Tinh chỉnh có giám sát nâng mọi độ đo trong nhóm; chẳng hạn SPICE, độ đo mà Zhao và cộng sự [37] khuyên dùng để xếp hạng các mô hình sinh chỉ dẫn khi có câu tham chiếu, tăng từ 18,5 ở mô hình gốc lên 44,4 ở S1 hạt giống 101. Phương pháp đề xuất nâng tiếp các độ đo này (Bảng 6.4). BERTScore dùng bản đã co giãn theo mức điểm nền (*baseline rescaling*), vì ở bản chưa co giãn, mọi mô hình đã tinh chỉnh đều nằm trong khoảng 93,5 đến 94,4. Câu rỗng được tính 0 điểm và vẫn nằm trong mẫu số, giống quy ước của executability.

Khi đọc nhóm độ đo này cần lưu ý hai điểm. Thứ nhất, CIDEr-D vượt quá 100 vì mỗi bước chỉ có một câu chuẩn và trọng số nghịch đảo tần suất văn bản (IDF) được ước lượng từ chính tập câu chuẩn, nên chỉ so sánh được giữa các hàng trong cùng bảng. Thứ hai, nhóm độ đo này xếp giai đoạn học ưu tiên cao hơn giai đoạn thưởng tọa độ, ngược với executability, đúng như Mục 5.11 đã chỉ ra cho những mô hình chênh nhau dưới hai điểm. Vì vậy nhóm độ đo này chỉ dùng để đặt kết quả cạnh các công trình cùng mảng; so sánh giữa các mô hình vẫn dựa trên executability.

## 6.6 So sánh ghép cặp

Mọi mô hình được chấm trên cùng một tập bước, nên chúng tôi so sánh hai mô hình theo từng cặp bước (kiểm định McNemar, Mục 5.13); Bảng 6.8 gom các phép so sánh dùng trong chương.

**Bảng 6.8.** So sánh ghép cặp trên 4.463 bước. `b` là số bước mà mô hình sau dấu trừ đạt còn mô hình trước dấu trừ không đạt, `c` là chiều ngược lại, nên Δ = (c-b)/n. Khoảng tin cậy từ bootstrap gom cụm theo tác vụ (Mục 5.13), trừ nhóm có dấu *. Base là mô hình gốc; S1/101 và S1/202 là mô hình tinh chỉnh có giám sát với hạt giống 101 và 202. Hai hàng có câu chuẩn dùng n = 4.462 vì bỏ một bước mà mô hình được đánh giá sinh câu rỗng. Thưởng SPICE là thành phần thứ nhất của phương pháp đề xuất; học ưu tiên là MIN-DESC; học thêm là mô hình chỉ học thêm có giám sát (CE2-S2); TAGE là bộ sửa câu theo vùng cắt. *Ở nhóm này, chỉ hàng thưởng SPICE - S1/101 gom cụm theo tác vụ, các hàng khác gom cụm theo ứng dụng; gom cụm theo ứng dụng cho hàng ấy khoảng gần như trùng ([+0,80; +2,33]).

| So sánh | Δ | KTC 95% | b | c | p |
|---|---:|---:|---:|---:|---:|
| **Mốc so sánh (S1 có hai hạt giống)** ||||||
| S1 - Base | +11,5 | [+10,0; +13,1] | 284 | 798 | <0,001 |
| Câu chuẩn - S1 | +16,6 | – | 102 | 843 | <0,001 |
| Câu chuẩn - Base | +28,1 | – | 102 | 1.357 | <0,001 |
| S1/202 - S1/101 (hai hạt giống) | +0,52 | [-0,22; +1,26] | 132 | 155 | 0,194 |
| **Phương pháp đề xuất và các so sánh liên quan*** ||||||
| Phương pháp đề xuất - S1/101 | +1,57 | [+0,86; +2,31] | 88 | 158 | <0,001 |
| Phương pháp đề xuất - thưởng SPICE | +0,02 | [-0,21; +0,26] | 14 | 15 | 1,00 |
| Thưởng SPICE - S1/101 | +1,55 | [+0,82; +2,28] | 90 | 159 | <0,001 |
| Thưởng SPICE - S1/202 | +1,03 | [+0,25; +1,83] | 145 | 191 | 0,014 |
| Thưởng SPICE - học ưu tiên | +0,60 | [-0,52; +1,73] | 304 | 331 | 0,30 |
| Thưởng SPICE - thưởng tọa độ | +0,58 | [-0,50; +1,69] | 286 | 312 | 0,31 |
| TAGE - thưởng SPICE | -0,43 | [-0,87; +0,02] | 67 | 48 | 0,093 |
| **Hướng đã thử (Phụ lục A)** ||||||
| Mô tả phần tử (S2) - S1/101 | -1,93 | [-3,06; -0,75] | 340 | 254 | 0,0005 |
| S2 - S1/202 | -2,44 | [-3,53; -1,34] | 353 | 244 | <0,001 |
| S2 - Base | +9,59 | [+8,16; +11,06] | 324 | 752 | <0,001 |
| Học thêm - S2 | +2,24 | [+1,41; +3,11] | 127 | 227 | <0,001 |
| Học ưu tiên - S2 | +2,87 | [+2,03; +3,76] | 130 | 258 | <0,001 |
| Học ưu tiên - học thêm | +0,63 | [+0,16; +1,10] | 42 | 70 | 0,011 |
| Học ưu tiên - S1/101 | +0,94 | [-0,09; +2,05] | 300 | 342 | 0,11 |
| Học thêm - S1/101 | +0,31 | [-0,76; +1,45] | 312 | 326 | 0,61 |
| Chọn ứng viên - Base | +8,54 | – | 350 | 731 | <0,001 |

Với hạt giống 101, tinh chỉnh có giám sát trên tập dữ liệu dựng tự động đem lại 11,5 điểm, thu hẹp 41% khoảng cách giữa mô hình gốc và câu chuẩn; phần còn lại là dư địa cải thiện bàn ở Mục 6.9.4. Tỉ lệ này cao hơn mức cải thiện thực chất, vì ở khoảng một phần tư số bước, S1 chép lại câu chuẩn. Chỉ tính 3.367 bước mà mô hình tự viết câu, mô hình gốc, S1 và câu chuẩn đạt lần lượt 44,7, 53,1 và 75,0, và phần khoảng cách thu hẹp được còn 28%.

## 6.7 Chênh lệch giữa hai hạt giống

Để đo mức dao động của điểm số khi huấn luyện lại, mô hình tinh chỉnh có giám sát (S1) được huấn luyện lần thứ hai, chỉ đổi hạt giống và giữ nguyên mọi tham số cấu hình khác (Mục A.1.2).

**Bảng 6.9.** Hai lượt huấn luyện chỉ khác hạt giống, chấm trên cùng 4.463 bước.

|  | Điểm | Δ ghép cặp | Bước bất đồng |
|---|---:|---:|---:|
| S1 hạt giống 101 | 59,11% | +0,52 pp | 287 = 6,4% |
| S1 hạt giống 202 | 59,62% |  |  |
| Phép so sánh kiểm chứng S1 - Base |  | +11,5 pp | 1.082 = 24,2% |

Chênh lệch 0,52 điểm giữa hai hạt giống không có ý nghĩa thống kê (khoảng tin cậy 95% chứa 0, p = 0,194, Bảng 6.8). Hai lượt cho kết quả khác nhau ở 6,4% số bước, so với 24,2% giữa S1 và mô hình gốc; xét độ lớn của điểm, chênh lệch giữa S1 và mô hình gốc lớn gấp 22 lần chênh lệch giữa hai hạt giống, và gấp 3,8 lần nếu xét tỉ lệ bước đổi kết quả.

Mức dao động này đến hoàn toàn từ mô hình sinh câu, không đến từ công cụ đo: trên 2.810 bước mà hai lượt viết ra hai câu giống hệt nhau, kết quả chấm trùng nhau ở mọi bước. Mức đồng thuận từng bước trên toàn tập là 93,6% (κ = 0,867, hệ số đồng thuận đã trừ phần trùng do ngẫu nhiên), nhưng con số này bị các bước viết trùng câu kéo lên; trên 1.652 bước hai lượt viết câu khác nhau, mức đồng thuận là 82,6% (κ = 0,650).

Trên hạt giống thứ hai, cả sáu cách chia nhóm ở Mục 6.9 cho chênh lệch cùng dấu với hạt giống thứ nhất và lệch nhau nhiều nhất 0,9 điểm. Trong 1.091 cụm (Mục 5.13), số cụm mà S1 hơn, bằng và kém mô hình gốc là 395/565/131 ở hạt giống 101 và 406/572/113 ở hạt giống 202.

## 6.8 Bảy cách giải thích thay thế

Chênh lệch 11,5 điểm giữa S1 và mô hình gốc có thể có cách giải thích khác ngoài tác dụng của tinh chỉnh. Chúng tôi kiểm bảy cách như vậy trên bản ghi từng bước (Bảng 6.10): sáu cách bị loại, riêng cách cho rằng S1 chỉ bắt chước văn phong của người chú thích thì chưa loại được.

**Bảng 6.10.** Bảy cách giải thích thay thế cho chênh lệch giữa S1 và Base, kèm kết quả kiểm tra.

| Cách đọc thay thế | Kết quả kiểm |
|---|---|
| Do điều kiện khớp thao tác chi phối | bỏ điều kiện đó, chấm riêng phần định vị, vẫn còn +11,3 điểm (b=272, c=777). Hơn nữa Base gọi đúng loại thao tác nhiều hơn (96,5% so với 94,4%) |
| Chỉ hơn ở một vị trí bước | bước mở đầu tác vụ +15,0 (n=593, [+11,0; +19,1]), các bước sau +11,0 ([+9,4; +12,6]). Hai khoảng giao nhau, cả hai đều dương |
| Chỉ hơn ở màn dễ | chia ba theo số phần tử trên màn cho +12,6, +9,5 và +12,4. Các khoảng giao nhau, không tầng nào đảo chiều |
| Vài ứng dụng chi phối cả bảng | trên 1.091 cụm, S1 hơn ở 395, bằng ở 565, kém ở 131 |
| Chỉ là bắt chước văn phong | không loại được, vì S1 mở đầu bằng động từ chạm nhiều hơn Base (91,0% so với 86,1%, câu chuẩn 95,1%), tức văn phong của S1 gần văn phong người chú thích hơn |
| Do công cụ đo đã quen văn phong chú thích | đã loại, vì khi chấm lại bằng UI-Venus-Ground-7B, một mô hình định vị không học AndroidControl, chênh lệch vẫn giữ 94% (Mục 5.9) |
| Do chép lại câu chuẩn | 1.095 trong 4.462 câu không rỗng của S1 lặp đúng các từ nội dung của câu chuẩn. Chấm riêng 3.367 bước mà mô hình tự viết, S1 vẫn hơn +8,4 điểm (b=264, c=547, p<0,001) |

Dòng cuối của bảng quan trọng nhất, vì một độ đo dựa trên câu chuẩn không tự phát hiện được việc mô hình chép lại câu chuẩn. Trên nhóm bước chép lại, S1 hơn mô hình gốc tới 21,1 điểm, nên một phần mức tăng do tinh chỉnh là việc lặp lại nguyên văn cách diễn đạt của người chú thích. Tuy vậy, trên các bước tự viết S1 vẫn hơn, nên thứ tự giữa hai mô hình không phụ thuộc vào phần chép lại.

Độ đo thiên vị câu dài: chia đôi câu của S1 ở độ dài trung vị 33 ký tự thì nhóm câu dài đạt 61,9%, nhóm câu ngắn đạt 56,5%. Thiên vị này có lợi cho mô hình gốc, vốn viết câu dài khoảng 70 ký tự (trung vị), nên việc S1 vẫn hơn mô hình gốc càng vững. Mức thiên vị khác nhau giữa các mô hình (ở mô hình gốc, câu dài lại kém câu ngắn 1,4 điểm), nên phải đo riêng cho từng mô hình.

## 6.9 Phân bố lỗi của mô hình tinh chỉnh có giám sát

Mục này trình bày bốn quan sát rút từ bản ghi từng bước của S1.

### 6.9.1 Ảnh hưởng của việc trùng ứng dụng giữa tập huấn luyện và tập kiểm tra

Trong các bước của tập kiểm tra gán được tên ứng dụng, 95,6% thuộc về ứng dụng cũng có trong tập huấn luyện (Mục 3.3), nên điểm số có thể cao hơn năng lực thực chất, và Bảng 6.11 đo ảnh hưởng ấy.

**Bảng 6.11.** Điểm của S1 chia theo việc ứng dụng của bước đã xuất hiện trong tập huấn luyện hay chưa.

| Nhóm | S1 | n |
|---|---:|---:|
| Ứng dụng đã thấy lúc huấn luyện | 59,1% | 1.737 |
| Ứng dụng chưa thấy | 59,0% | 78 |
| Không quy được về ứng dụng | 59,1% | 2.648 |

Ba con số gần như trùng nhau, nhưng nhóm ứng dụng chưa thấy chỉ có 78 bước nên khoảng tin cậy rất rộng; chúng tôi chỉ nói được là chưa phát hiện ảnh hưởng của việc trùng ứng dụng, chưa thể nói đã loại trừ được ảnh hưởng ấy.

### 6.9.2 Phân loại lỗi còn lại

Trong 1.824 bước S1 không đạt, chỉ 251 bước sai loại thao tác. **1.573 bước còn lại (86%)** đúng loại thao tác, nhưng từ câu S1 viết, mô hình định vị không tìm ra phần tử cần chạm, như các ví dụ nguyên văn dưới đây.

| câu chuẩn | câu S1 sinh ra |
|---|---|
| click on the OK option | select minutes 00 |
| Click on the Sort filter | Click on the Air India flight option |
| Click on the share icon | Open Recorder app |

Phần lỗi còn lại của S1 vì vậy nằm ở khâu gọi tên và mô tả phần tử.

### 6.9.3 Khác biệt hành vi giữa mô hình gốc và mô hình đã tinh chỉnh

Trên 798 bước mà S1 đúng còn mô hình gốc sai, lỗi của mô hình gốc có hai dạng.

|  | Câu |
|---|---|
| chuẩn | Click on the profile icon at the top right of the screen |
| S1 | Click on the profile icon at the top right corner of the screen |
| Base | To set YouTube video downloads over Wi-Fi only, tap on your profile icon at the top right corner of the screen and select “Settings.” Then navigate to the “Downloads” section and choose “Wi-Fi Only.” |
| chuẩn | Click on Knoxville |
| S1 | Click on Knoxville |
| Base | Click on the three dots next to Knoxville to access more options and proceed with reading the local news. |

Ở dạng thứ nhất, mô hình gốc viết cả một kế hoạch nhiều bước thay vì chỉ bước hiện tại. Ở dạng thứ hai, mô hình gốc mô tả một bước khác với bước cần làm. Câu của mô hình gốc vẫn trôi chảy, đúng khuôn và gọi tên nút cụ thể; câu này nhận điểm thấp vì không bám sát bước hiện tại chứ không vì viết sai định dạng. Điều tinh chỉnh dạy được cho mô hình chính là bám sát bước hiện tại.

### 6.9.4 Ước lượng dư địa cải thiện còn lại

Ngay cả câu chuẩn cũng không đạt ở khoảng một phần tư số bước, phần lớn do giới hạn của công cụ đo (Mục 6.11). Phần dư địa nằm ở cách diễn đạt của S1 là khoảng 16,6 điểm (741 bước) giữa câu chuẩn và S1 (Mục 5.5), lớn so với sai số chuẩn 0,79 điểm của hiệu ghép cặp. Một can thiệp chỉ cần sửa được khoảng 13% dư địa này là đã tăng hơn hai điểm, cỡ mức hiệu ứng trung vị mà các công trình đã công bố ghi nhận cho những can thiệp tương tự. Theo executability, chưa can thiệp nào của đề tài đạt tới mức đó; phương pháp đề xuất tiến gần nhất (Bảng 6.1).

## 6.10 Các hướng đã thử trước phương pháp đề xuất

Bảng 6.12 tóm tắt các hướng đã thử trước phương pháp đề xuất; chi tiết nằm ở Phụ lục A.

**Bảng 6.12.** Các hướng đã thử trước phương pháp đề xuất. Điểm là executability trên 4.463 bước chạm của tập kiểm tra, trừ khi ghi khác.

| Hướng | Ý tưởng | Kết quả | Điều rút ra |
|---|---|---|---|
| Mô tả phần tử (S2), Mục A.1.3 | viết một dòng mô tả phần tử cần chạm trước câu hướng dẫn | 57,2%, thấp hơn S1/101 1,93 điểm | mô tả trỏ đúng thì câu tốt hơn, trỏ sai thì câu kém hơn nhiều |
| Giai đoạn học ưu tiên (MIN-DESC), Mục A.2.2 | học ưu tiên trên cặp đầu ra chỉ khác ở dòng mô tả | 60,0%; 78% mức tăng so với S2 cũng có ở mô hình chỉ học thêm có giám sát | phần lớn mức tăng đến từ việc học thêm |
| Chọn ứng viên, Mục A.3.2 | chọn phần tử cần chạm trong danh sách dựng sẵn | 56,1%, chỉ so được với mô hình gốc | khi có chọn thì chọn tốt, nhưng từ chối quá nhiều |
| Giai đoạn thưởng tọa độ, Mục A.4.2 | học tăng cường, thưởng khi tọa độ trong dòng mô tả gần điểm chạm đúng | 60,1% (77,3% theo luật khoảng cách Euclid) | tọa độ chính xác hơn, nhưng câu gần như không đổi |
| Đưa thêm thông tin vị trí, Mục A.6 | cho bộ sinh câu nhận thêm thông tin vị trí (bốn cách) | dừng ở tập kiểm định nội bộ | bộ sinh câu bỏ qua thông tin này |
| Sửa câu theo vùng cắt (TAGE), Mục A.7.2 | viết lại câu nháp sau khi xem ảnh phóng to quanh phần tử | 60,2%, thấp hơn câu nháp 0,43 điểm | bộ chọn lại chủ yếu nhận câu sửa dựa trên vùng cắt sai |

Ba điều rút ra dẫn tới phương pháp đề xuất. Thứ nhất, tác động vào phần nằm giữa ảnh và câu, như dòng mô tả phần tử hay tọa độ trong dòng mô tả, chỉ làm câu ở đầu ra thay đổi rất ít (Mục A.5). Thứ hai, phần lớn khoảng cách còn lại nằm ở những bước mô hình nhìn sai phần tử ngay từ đầu, và gắn thêm thông tin vị trí vào bộ sinh câu đã học xong không làm câu thay đổi. Thứ ba, học thêm trên câu chuẩn hay câu viết lại đều có nguy cơ làm câu kém đi. Vì vậy phương pháp đề xuất đặt phần thưởng thẳng lên câu ở đầu ra, và chỉ chép câu ví dụ khi loại thao tác đồng thuận.

## 6.11 Giới hạn của độ đo trên tập kiểm tra

Câu chuẩn không đạt ở 1.083 bước. Ở 64,8% số bước ấy, mô hình định vị gần như không tìm ra phần tử: điểm trả về nằm xa ngoài vùng dung sai (sai số trung vị 26,2% bề ngang màn, so với 0,4% ở bước đạt). 381 bước còn lại nằm trong vùng dung sai nhưng bị luật ô Voronoi loại; **208 bước trong số đó có điểm trả về nằm ngay trong hộp nhỏ nhất chứa điểm chạm**, vì trên một phần tử lớn, phần tử con có thể cạnh tranh với chính phần tử cha. Luật ô Voronoi loại 10,1% số bước nằm trong vùng dung sai với câu chuẩn, 13,0% với S1 và 15,2% với mô hình gốc. Có 935 bước (21%) mà cả câu chuẩn, S1 và mô hình gốc đều không đạt, nên ngưỡng tối đa 75,7% chủ yếu phản ánh giới hạn của công cụ đo, chưa phải giới hạn của cách diễn đạt.

Chúng tôi cũng kiểm khả năng mô hình viết cho công cụ đo thay vì cho người đọc (Mục 5.5). Câu nêu tên một vùng trên màn đạt 89,5% khi vùng đó đúng, 3,3% khi vùng đó sai và 54,8% khi không nêu vùng nào, nên độ đo thưởng việc nói đúng vị trí chứ không thưởng việc nói vị trí sai. S1 dùng từ chỉ vị trí 26,8% số câu, gần bằng 26,4% của câu chuẩn, và chỉ để lại chuỗi tọa độ vào 3 trong 6.958 câu. S1 chỉ khác câu chuẩn rõ ở việc lặp khuôn câu nhiều hơn: hai mẫu câu phổ biến nhất chiếm 10,4% số bước, so với 6,5% ở câu chuẩn.

## 6.12 Trạng thái các mô hình và phép thử

Bảng 6.13 ghi trạng thái cuối của từng mô hình và phép thử, kèm lý do với những cấu hình không chạy hoặc dừng giữa chừng.

**Bảng 6.13.** Trạng thái cuối của các mô hình, cấu hình và phép thử. Điểm trong cột ghi chú là executability trên tập kiểm tra, trừ khi ghi khác.

| Mô hình hoặc phép thử | Trạng thái | Ghi chú |
|---|---|---|
| Phương pháp đề xuất (thưởng SPICE + ACE) | Hoàn tất, đã đánh giá | 60,7; hơn S1/101 +1,57 có ý nghĩa; ngang thành phần thứ nhất về vị trí, cao hơn ở cả bảy độ đo so câu (CIDEr-D +12,0); Mục 6.4 |
| Thành phần thứ nhất (thưởng SPICE) | Hoàn tất, đã đánh giá | 60,6; hơn S1/101 +1,55 có ý nghĩa, tăng ở cả mười ba độ đo; Mục 6.3 |
| Mô hình tinh chỉnh có giám sát (S1), hai hạt giống | Hoàn tất, đã đánh giá | 59,1 và 59,6; chênh lệch giữa hai hạt giống +0,52 điểm; Mục 6.7 |
| Mô tả phần tử (S2), hạt giống 101 | Hoàn tất, đã đánh giá | 57,2; thấp hơn S1/101 có ý nghĩa; Mục A.1.3 |
| Mô tả phần tử (S2), hạt giống 202 | Đã hủy bỏ | giới hạn tài nguyên tính toán |
| Mô tả giả (S2r); mô tả không có tọa độ (S2-nopoint) | Đã hủy bỏ | mô tả giả chỉ cần khi S2 cho kết quả dương; tọa độ tự nó có ích (+1,12 điểm) |
| Đưa danh sách phần tử vào S1 lúc suy luận | Không thực hiện | không mô hình nào cần tới |
| Học thêm có giám sát (CE2-S2); giai đoạn học ưu tiên (MIN-DESC) | Hoàn tất, đã đánh giá | 59,4 và 60,0; 78% mức tăng so với S2 cũng có ở mô hình học thêm; Mục A.2.2 |
| Học ưu tiên với vế sai lấy từ lỗi của chính mô hình | Dừng ở khâu tạo dữ liệu | chỉ 3,3% cặp hợp lệ; Mục A.2.2.3 |
| Giai đoạn thưởng tọa độ | Hoàn tất, đã đánh giá | 60,1; +0,02 so với giai đoạn học ưu tiên; Mục A.4.2 |
| Nội suy trọng số giữa hai giai đoạn trên | Hoàn tất | điểm đổi đơn điệu, không chấm cấu hình mới trên tập kiểm tra; Mục A.4.3 |
| Cấu hình đối chứng của giai đoạn thưởng tọa độ | Không thực hiện | mức chênh gần bằng không |
| Bước không chạm sau giai đoạn học ưu tiên | Đã đánh giá | giảm 19,75 điểm; Mục A.2.2.4 |
| Chọn ứng viên, hạt giống 101 | Hoàn tất, đã đánh giá | 56,1; độ chính xác chọn 57,5%, thấp hơn khi tự viết dòng mô tả; Mục A.3.2 |
| Năm lượt còn lại của mô hình chọn ứng viên | Đã hủy bỏ | độ chính xác chọn không vượt dòng mô tả tự viết |
| Hiệu chỉnh ngưỡng từ chối chọn | Hoàn tất | tốt nhất thêm 8 bước đúng trên 1.400 bước |
| Mở khoá phần thị giác để cùng huấn luyện | Dừng giữa chừng | bản lưu sau 41% số bước kém giai đoạn học ưu tiên rõ trên tập kiểm định nội bộ |
| Mô-đun định vị và cầu nối | Dừng sau một lượt | cầu nối không làm câu thay đổi; Mục A.6 |
| Vùng cắt làm ảnh thứ hai | Dừng ở khâu đánh giá | không phân biệt phần tử đúng với phần tử lân cận |
| Đưa thêm vai trò, vùng và loại thao tác vào mô hình | Dừng sau một lượt | hệ số trộn tự giảm về gần không; chỉ 4% số câu đổi |
| Làm nét ảnh quanh phần tử | Dừng ở khâu đánh giá | không hơn làm nét ở vị trí đối diện |
| Hai lượt viết lại có chọn lọc; bộ xếp hạng câu dùng màn kế tiếp | Dừng ở khâu sàng lọc | không đủ câu lỗi để sửa; bộ xếp hạng cho kết quả thấp hơn giải mã tham lam |
| Sửa câu theo vùng cắt (TAGE) | Hoàn tất, đã đánh giá | 60,2; thấp hơn câu nháp 0,43; Mục A.7.2 |
| Mô hình định vị thứ hai (UI-Venus) | Hoàn tất | chênh lệch S1 với mô hình gốc giữ 94%; Mục 5.9 |
| Người nghe trắc nghiệm (Phi-4) | Hoàn tất một phần | đã chấm câu chuẩn, giai đoạn thưởng tọa độ, S1/101 và 3.566 bước của mô hình gốc; Mục 5.10 |
| Chấm tay 100 câu bởi hai người | Không thực hiện | còn là một hạn chế; Mục 7.2 |


# Chương 7. Kết luận

## 7.1 Đóng góp của luận văn

Đề tài xuất phát từ quan sát rằng, với cùng một ảnh màn hình và cùng một mục tiêu, dòng nghiên cứu tác tử giao diện sinh ra tọa độ để máy tự bấm, trong khi người dùng đang dừng lại giữa chừng thì cần một câu chỉ dẫn bằng tiếng Anh cho biết phải chạm vào đâu. **Đóng góp chính của đề tài là một phương pháp sinh câu chỉ dẫn như vậy, gồm hai thành phần nối tiếp.** Hai đóng góp còn lại hỗ trợ cho phương pháp. Đóng góp thứ hai là **độ đo executability**, dùng để chấm phương pháp cùng mọi mô hình khác trong đề tài. Đóng góp thứ ba là **chuỗi phân tích rút từ các hướng đã thử**, cũng là căn cứ để chọn phương pháp.

**Về phương pháp đề xuất**

Phương pháp đề xuất (Mục 4.4) xây dựng trên mô hình tinh chỉnh có giám sát và tác động thẳng vào câu ở đầu ra: mô hình học với thưởng SPICE viết câu nháp, rồi ACE chỉ thay câu nháp bằng một câu ví dụ truy hồi từ tập huấn luyện khi câu ấy được chép nguyên văn và cùng loại thao tác với câu nháp. Mô hình định vị dùng để chấm không tham gia vào phần thưởng lẫn luật đồng thuận, nên phép đo ở đầu ra vẫn độc lập với phương pháp.

Với cả hai thành phần, phương pháp đề xuất đạt **60,7% theo executability**, so với **59,1%** của mô hình tinh chỉnh có giám sát, tức hơn **1,57 điểm** với khoảng tin cậy **[+0,86; +2,31]** và **p < 0,001**. Mức hơn này về executability đến từ thành phần thứ nhất, vì khi đứng một mình, mô hình học với thưởng SPICE đã đạt **60,6%**, cao nhất trong số các mô hình chỉ dùng một bộ sinh câu, và hơn mô hình tinh chỉnh có giám sát **1,55 điểm [+0,80; +2,33]**. Đây là mô hình đầu tiên của đề tài hơn mô hình tinh chỉnh có giám sát với ý nghĩa thống kê theo executability. Mức tăng xuất hiện ở cả mười ba độ đo được trình bày, và hơn một nửa mức tăng đến từ việc định vị phần tử tốt hơn (Mục 6.3). ACE nâng thêm cả bảy độ đo so câu sinh ra với câu chuẩn, rõ nhất ở CIDEr-D (+12,0) và SPICE (+1,3), mà không làm giảm độ đo vị trí nào. Bộ sinh có câu ví dụ khi đứng một mình lại làm executability giảm, nên phần có ích của truy hồi chỉ giữ được nhờ luật đồng thuận (Mục 6.4).

**Về độ đo**

Khi đầu ra là câu thay vì tọa độ, việc chấm trở nên khó, vì cùng một nút có nhiều tên gọi đều đúng và không bộ dữ liệu nào liệt kê hết. Độ đo **executability** đưa câu sinh ra cho một mô hình định vị phần tử độc lập, không được cung cấp tọa độ đáp án, rồi kiểm xem điểm mà mô hình định vị trả về có rơi vào ô Voronoi của phần tử người dùng đã chạm hay không. Ý tưởng này có gốc từ dòng sinh biểu thức quy chiếu; phần đóng góp của đề tài nằm ở loạt phép đo dùng để kiểm chứng độ đo (Chương 5). Sai số của công cụ đo nhỏ hơn nhiều so với khoảng cách từ phần tử cần chạm tới phần tử lân cận gần nhất (Mục 5.4), và luật ô Voronoi được chọn vì gần như không cho điểm một câu gọi sai tên nút (Mục 5.2). Hai đầu của dải điểm cũng đã được đo: khi chấm chính câu chuẩn, điểm đạt ngưỡng tối đa 75,7% (Mục 5.5), còn câu đúng văn phong nhưng sai nội dung nhận điểm thấp nhất trong mọi phép đo, cho thấy công cụ đo chấm theo nội dung câu chứ không theo văn phong (Mục 5.6). Trong mười phép cố ý chèn một lỗi đã biết để xem luật chấm có bắt được không, chỉ bốn phép (đặt điểm lên một phần tử kề và phủ định câu) thực sự kiểm được luật chấm, còn các phép khác cho kết quả tốt do chính cách dựng. Hai trong bốn phép ấy có tỉ lệ bắt lỗi thấp (Mục 5.7).

Thứ tự giữa câu chuẩn, mô hình tinh chỉnh có giám sát và mô hình gốc giữ nguyên dưới năm luật chấm khác nhau (Mục 5.12), và độ đo giữ ổn định khi câu chuẩn được viết lại bằng cách đổi động từ hay đảo trật tự câu (Mục 5.8). Khi chấm lại bằng một mô hình định vị thứ hai không dùng AndroidControl khi huấn luyện, chênh lệch giữa mô hình tinh chỉnh có giám sát và mô hình gốc, dùng làm phép so sánh kiểm chứng, vẫn giữ được 94% độ lớn (Mục 5.9). Khi chấm bằng Phi-4, một mô hình không thuộc họ Qwen làm người nghe trắc nghiệm, tức đọc câu rồi chọn phần tử đúng trong một danh sách ứng viên đánh số, thứ tự giữa các mô hình cũng giữ nguyên (Mục 5.10).

**Về dữ liệu và mô hình tinh chỉnh có giám sát**

Tập giám sát **64.567 bước** được dựng hoàn toàn bằng máy, không thuê người gắn nhãn và không đưa nhãn do một mô hình ngôn ngữ khác sinh ra vào vòng huấn luyện. Các bài kiểm tra chất lượng dữ liệu, gồm việc đánh giá quá trình ghép hai kho dữ liệu nguồn, kiểm tra cấu trúc và kiểm tra rò rỉ giữa tập huấn luyện với tập kiểm tra, đều đạt (Chương 3).

Trên 4.463 bước chạm của tập kiểm tra, mô hình tinh chỉnh có giám sát đạt **59,1%**, trong khi chính mô hình đó khi chưa tinh chỉnh (mô hình gốc) chỉ đạt **47,6%**. Cả hai con số cần đọc cạnh ngưỡng tối đa 75,7% của câu chuẩn. Theo luật hộp phần tử của AndroidControl, hai con số tương ứng là **65,5%** và **53,6%**, với ngưỡng tối đa **83,8%**. Khoảng tin cậy của mô hình gốc, mô hình tinh chỉnh có giám sát và câu chuẩn không chồng lên nhau, cho thấy công cụ đo phân biệt được hai mô hình. Chênh lệch giữa hai mô hình giữ nguyên trước các cách giải thích thay thế đã kiểm, kể cả khi bỏ những câu mà mô hình chép nguyên văn câu chuẩn. Riêng khả năng mô hình chỉ bắt chước văn phong người chú thích thì chưa loại được và vẫn được ghi lại trong bảng ở Mục 6.8.

**Về phân tích các hướng đã thử**

Đóng góp thứ ba là chuỗi phân tích ở mức từng bước, rút từ các hướng đã thử trước phương pháp đề xuất. Mục 6.10 tóm tắt chúng, còn thiết kế và kết quả chi tiết nằm ở Phụ lục A.

Hướng thử đầu tiên dạy mô hình viết một dòng mô tả phần tử cần chạm trước, rồi mới viết câu hướng dẫn. Mô hình này, gọi là **mô hình mô tả phần tử**, đạt điểm thấp hơn mô hình tinh chỉnh có giám sát (Mục A.1.3). Hai giai đoạn học tiếp theo có nâng điểm lên, nhưng phần lớn mức tăng ở giai đoạn học ưu tiên thực ra đến từ việc mô hình được học thêm có giám sát (Mục A.2.2). Ở giai đoạn thưởng tọa độ, phần hơn mô hình tinh chỉnh có giám sát, tính theo luật khoảng cách Euclid của AndroidInTheWild, nằm trọn ở những bước mà mô hình tinh chỉnh có giám sát gọi sai loại thao tác (Mục 6.5). Khi chia các bước theo dòng mô tả do chính mô hình viết ra, mô hình mô tả phần tử hơn hẳn mô hình tinh chỉnh có giám sát ở những bước dòng mô tả trỏ đúng phần tử, và kém hơn ở những bước dòng mô tả trỏ sai. Như vậy việc viết dòng mô tả trước vẫn có tác dụng, chỉ là tác dụng ấy không thể vượt qua độ chính xác của chính dòng mô tả (Mục A.2.3).

Hai phân tích tiếp theo tìm xem nguyên nhân sai tập trung ở khâu nào. Phân tích thứ nhất tách việc sinh câu thành hai khâu, khâu nhận ra phần tử (mô hình có nhìn ra đúng phần tử cần chạm hay không) và khâu diễn đạt thành câu (câu viết ra có đủ để tìm lại phần tử ấy hay không). Kết quả cho thấy phần lớn khoảng cách tới câu chuẩn dồn vào nhóm bước mà mô hình nhìn sai phần tử ngay từ đầu, nhưng khi một can thiệp giúp mô hình nhận ra đúng phần tử ở nhiều bước hơn, phần cải thiện ấy chỉ chuyển thành rất ít điểm executability (Mục A.5). Phân tích thứ hai gồm bốn phép thử đưa thêm thông tin vị trí vào bộ sinh câu. Thông tin này học được, nhưng bộ sinh câu đã học xong lại bỏ qua nó (Mục A.6). Hai kết quả này là căn cứ để phương pháp đề xuất tác động thẳng vào câu ở đầu ra, và cũng giải thích vì sao học tăng cường với thưởng SPICE là giai đoạn huấn luyện duy nhất vượt mô hình tinh chỉnh có giám sát theo executability.

Ở **mô hình chọn ứng viên**, dòng mô tả không còn được sinh tự do mà được chọn trong danh sách phần tử của chính màn hình. Bản thân việc chọn hoạt động đúng, nhưng phát sinh một rào cản mới là mô hình từ chối chọn quá nhiều, tức trả lời rằng danh sách không chứa phần tử cần chạm dù thực ra có. Yếu tố liên quan gần nhất đo được là tỉ lệ mẫu huấn luyện được gán nhãn từ chối chọn, nhưng đây mới là quan sát tương quan, chưa được xác lập thành quan hệ nhân quả (Mục A.3.2).

## 7.2 Hạn chế

Phần này liệt kê những chỗ mà kết luận của đề tài còn để ngỏ, kèm số đo cho từng chỗ khi có thể đo được.

### 7.2.1 Hạn chế của công cụ đo

- **Khả năng mô hình định vị thiên vị theo văn phong của AndroidControl đã được loại trừ; khả năng thiên vị do cùng họ mô hình mới được loại trừ một phần.** Công cụ đo chính, UGround-V1-2B, được huấn luyện trên dữ liệu có 47 nghìn phần tử do người gắn nhãn, lấy từ phần huấn luyện chính thức của AndroidControl, trong khi 90% tác vụ trong tập kiểm tra của đề tài cũng thuộc phần ấy. Tách điểm theo phần chia chính thức của AndroidControl không cho thấy chênh lệch nào giữa phần mô hình định vị có thể đã học và phần còn lại (Mục 5.3), và phép chấm lại bằng UI-Venus-Ground-7B, một mô hình không học AndroidControl, giữ được 94% độ lớn của phép so sánh kiểm chứng (Mục 5.9). Cả hai mô hình định vị đều thuộc họ Qwen-VL, cùng dòng với mô hình được chấm. Người nghe trắc nghiệm Phi-4, ngoại họ Qwen, giữ nguyên thứ tự giữa các mô hình (Mục 5.10). Tuy vậy, người nghe này mới chấm bốn mô hình, mô hình gốc chưa được chấm hết tập kiểm tra, và dải điểm của người nghe, từ câu chung chung tới câu chuẩn, hẹp hơn nhiều so với dải của executability. Vì vậy mới nói được rằng thứ tự giữa các mô hình giữ nguyên dưới một người nghe ngoài họ Qwen, chưa nói được rằng mọi phép so đã được kiểm chéo qua hai mô hình.
- **Độ bền trước cách diễn đạt khác mới chỉ được kiểm một phần.** Phép viết lại ở Mục 5.8 cho thấy độ bền trước việc đổi động từ và đảo trật tự câu (+0,35 điểm trên 1.139 câu, khoảng tin cậy loại được mọi mức giảm lớn hơn 0,6 điểm). Nhưng phép biến đổi đó không tác động đến cách mô tả phần tử, vốn là phần nặng nhất trong cảnh báo của Jandial và cộng sự [18]. Chúng tôi chưa đo trường hợp viết lại chính tên gọi và cách mô tả phần tử, nên chưa biết khi ấy mô hình định vị có còn trỏ trúng phần tử hay không. Các phép cố ý chèn lỗi (Mục 5.7) không thay được phép đo ấy, vì chúng đưa thẳng một điểm tổng hợp vào luật xác định trúng và không gọi mô hình định vị lần nào.
- **Độ đo bỏ sót lỗi theo cả hai chiều.** Theo chiều thứ nhất, độ đo bỏ qua sai lệch nhỏ. Một điểm trỏ lệch dưới khoảng 63 điểm ảnh, tức bán kính dùng để gộp các phần tử trùng nhau, thường vẫn nằm trong ô của chính phần tử cần chạm, nên độ đo bắt được việc gọi sai tên phần tử nhưng không bắt được việc trỏ hơi lệch bên trong cùng phần tử. Theo chiều thứ hai, độ đo có thể chấm trượt cả câu đúng. Trong 1.083 bước mà câu chuẩn cũng trượt, phần lớn là do giới hạn của công cụ đo, và có 935 bước (21% tổng số bước) mà cả mô hình gốc, mô hình tinh chỉnh có giám sát lẫn câu chuẩn đều trượt. Vì vậy ngưỡng tối đa 75,7% phản ánh giới hạn của công cụ đo nhiều hơn là giới hạn của bản thân câu hướng dẫn.
- **Luật ô Voronoi chỉ chặt bằng độ đầy đủ của bộ liệt kê phần tử.** Nếu cây trợ năng bỏ sót một nút biểu tượng cạnh phần tử cần chạm thì một câu sai vẫn được tính là đúng. Tương tự, phép gộp các hộp trùng lặp theo bán kính xóa nhầm một phần tử riêng biệt có thật ở 8,2% số bước. Ở chiều ngược lại, luật chặt hơn mức cần thiết trên các hàng của danh sách, vì một mảnh chữ OCR trên cùng hàng có thể bị coi là một nút riêng. Trong số bước mà câu chuẩn trượt ô Voronoi nhưng trúng luật hộp phần tử của AndroidControl (Mục 5.12), khoảng một nửa trượt chỉ vì lý do này, nên ngưỡng tối đa 75,7% đánh giá thấp năng lực của công cụ đo trên các hàng danh sách.
- **Khái niệm được đo hẹp hơn khái niệm người đọc quan tâm.** Độ đo là khả năng một mô hình định vị tìm tới đúng phần tử dựa trên câu, trong khi điều người dùng quan tâm là khả năng một người tìm tới được phần tử ấy. Dòng sinh biểu thức quy chiếu vẫn coi thành công của người nghe là bằng chứng về chất lượng mô tả [11, 12, 13], và mốc đối chiếu ở đây là tọa độ mà một người thật đã chạm. Dù vậy, hai đại lượng ấy không đồng nhất, và mức đồng thuận giữa chúng chưa được đo (Mục 7.3).

### 7.2.2 Hạn chế của kết quả về mô hình

- **Mô hình học với thưởng SPICE chưa có cấu hình đối chứng học thêm cùng số bước.** Vì vậy chúng tôi chưa tách được phần thuộc về thuật toán học tăng cường khỏi phần thuộc về việc học thêm. Ngoài ra, câu của mô hình này được sinh theo một quy trình khác với quy trình của mô hình tinh chỉnh có giám sát, và trên 20 bước chạm dùng để kiểm, riêng việc đổi quy trình sinh đã làm 4 câu khác đi (Mục 4.5).
- **ACE chưa tách được phần của truy hồi.** Trên tập kiểm định nội bộ, bộ sinh có câu ví dụ không hơn một mô hình học thêm như vậy nhưng không có câu ví dụ trong đầu vào ở đa số độ đo, nên chưa biết bao nhiêu phần lợi của ACE đến từ truy hồi. Luật đồng thuận được chọn trong bốn biến thể nghĩ ra sau khi đã thấy kết quả của bộ sinh trên tập ấy. Mức tăng ở nhóm độ đo so câu chưa có khoảng tin cậy, và nằm ở bề mặt câu, chưa giúp mô hình định vị tìm đúng phần tử hơn (Mục 6.4).
- **Các hướng đã thử thiếu cấu hình đối chứng.** Nhiều hướng thiếu cấu hình đối chứng cần để quy công cho từng thành phần. Cụ thể, chưa chạy cấu hình học thêm cùng số bước với giai đoạn thưởng tọa độ, ba cấu hình đối chứng của thiết kế ban đầu (Bảng 6.13), và cấu hình đối chứng có cùng đầu vào với mô hình chọn ứng viên. Giai đoạn thưởng tọa độ cũng chưa được chấm ở bước không chạm. Giới hạn riêng của từng hướng được nêu ở Phụ lục A, còn hạn chế của tập cặp dùng cho giai đoạn học ưu tiên được nêu ở Chương 3.
- **Phân tích nguyên nhân lỗi là hậu kiểm.** Cách chia nhóm ở Mục A.2.3 dùng chính hành vi của mô hình được đo và chỉ được xác định sau khi đã có điểm. Vì vậy con số +5,4 điểm, tức mức tăng nếu tránh được phần điểm sụt giảm ở những bước dòng mô tả trỏ sai phần tử, là một ngưỡng tối đa lý thuyết, không phải kết quả của một mô hình đã chạy. Điều tương tự cũng đúng với con số +9,3 điểm của mô hình chọn ứng viên nếu tránh được các lần từ chối chọn sai (Mục A.3.2).

### 7.2.3 Hạn chế của dữ liệu và thiết kế

- **Tập kiểm tra là tập giữ riêng theo tác vụ.** Tập kiểm tra lấy theo cách chia của một bản phân phối công khai, và 90% tác vụ của tập này thuộc phần huấn luyện chính thức của AndroidControl (Mục 3.3). Các phép so nội bộ không bị ảnh hưởng, nhưng con số tuyệt đối của đề tài không so thẳng được với các công trình báo cáo kết quả trên phần kiểm chính thức.
- **Tập kiểm tra không phải “ứng dụng chưa từng thấy”.** Trong số bước xác định được tên ứng dụng, 95,6% thuộc về ứng dụng cũng xuất hiện ở tập huấn luyện (91,8% nếu đếm theo ứng dụng riêng biệt), nên mọi phép so với một mô hình bên ngoài chỉ có giá trị tham khảo. Khi đo trên chính mô hình của đề tài, chúng tôi không thấy ảnh hưởng của việc ứng dụng đã xuất hiện ở tập huấn luyện (Bảng 6.11). Vì nhóm ứng dụng chưa thấy chỉ có 78 bước, kết luận đúng phải là “không phát hiện được ảnh hưởng”, một phát biểu yếu hơn nhiều so với “đã chặn được ảnh hưởng”.
- **Tách theo tác vụ không đồng nghĩa tách theo cách diễn đạt.** Bộ ngữ liệu lặp lại nhiều lần các cách diễn đạt phổ biến, đến mức 17,3% câu chuẩn của tập kiểm tra đã xuất hiện nguyên văn ngay trong một mẫu của tập huấn luyện.
- **Nhãn mô tả còn nhiều lỗi.** Ở bộ dữ liệu này, 24,1% dấu hiệu phân biệt không tách được phần tử cần chạm khỏi các phần tử giống nó, và 22,0% phần tử cần chạm không có tên nào để điền vào ô tên.
- **Khâu chấm cho sẵn ngữ cảnh đúng của mỗi bước.** Trường lịch sử trong câu nhắc chứa câu chuẩn ở các bước trước, không phải nhật ký thao tác của chính mô hình. Vì trường này giống nhau ở mọi mô hình nên không giải thích được chênh lệch giữa các mô hình, nhưng mọi con số tuyệt đối phải đọc kèm điều kiện này.
- **Phạm vi chung.** Chúng tôi chỉ xét một màn hình tại mỗi bước, giao diện tiếng Anh, một bộ dữ liệu, hai mô hình định vị cùng họ cộng một người nghe khác họ, và một mô hình gốc có ba tỉ tham số.

## 7.3 Hướng phát triển

Các hướng dưới đây xếp theo mức độ cần thiết đối với độ tin cậy của kết luận.

- **Hoàn tất đánh giá phương pháp đề xuất.** Với mô hình học với thưởng SPICE còn thiếu hai việc: một cấu hình đối chứng được học có giám sát thêm cùng số bước trên cùng tập câu nhắc, và sinh lại câu của mô hình tinh chỉnh có giám sát theo cùng quy trình sinh đã dùng cho mô hình học với thưởng SPICE để hai bên chỉ còn khác nhau một yếu tố. Với ACE, cần khoảng tin cậy cho nhóm độ đo so câu.
- **Một bộ chọn độc lập cho bộ sửa câu theo vùng cắt.** Bộ sửa câu theo vùng cắt (TAGE), một hướng đã thử ở cùng vị trí với ACE, cho executability thấp hơn câu nháp. Khi vùng cắt chứa đúng phần tử, bộ sửa câu có lợi nhiều hơn có hại, nhưng bộ chọn dựa trên xác suất do chính bộ sửa câu đưa ra hay nhận câu sửa ở những bước vùng cắt sai (Mục A.7.2). Bước thử rẻ nhất là một bộ chọn so điểm mà mô hình định vị trỏ tới khi đọc câu nháp với điểm dùng để đặt vùng cắt.
- **Học thông tin vị trí cùng lúc với phần sinh câu.** Bốn phép thử ở Mục A.6 đều gắn thêm thông tin vị trí vào một bộ sinh câu đã học xong, và lần nào phần sinh câu cũng bỏ qua thông tin ấy. Phép thử còn thiếu là học cả hai từ đầu, trên dữ liệu mà mô hình chưa thấy, để phần sinh câu không có sẵn một lời giải không cần tới vị trí.
- **Mở phần thị giác của mô hình nền.** Mục A.5 quy 91% khoảng cách tới câu chuẩn về nhóm bước mà mô hình nhìn sai phần tử, trong khi mọi lượt huấn luyện đều đóng băng phần thị giác. Một lượt mở phần thị giác đã dừng ở 41% số bước, khi điểm lưu còn thấp hơn giai đoạn học ưu tiên trên tập kiểm định nội bộ (Bảng 6.13). Phép so này bất lợi cho mô hình mới, vì giai đoạn học ưu tiên đã học chính tập kiểm định, nên hướng này chưa có kết luận. Kỳ vọng cần giữ ở mức khiêm tốn, vì theo phép đo đã có, mỗi điểm cải thiện ở khâu nhận ra phần tử chỉ chuyển thành khoảng 0,028 điểm executability.
- **Mô hình chọn ứng viên: tách riêng quyết định từ chối chọn và chạy cấu hình đối chứng.** Ở mô hình chọn ứng viên, xác suất do chính mô hình đưa ra không tách được bước có đáp án khỏi bước không có đáp án (Mục A.3.2). Hướng tiếp theo là một bộ phân loại riêng, đặt trước bước chọn ứng viên, chỉ quyết định danh sách ứng viên có chứa phần tử cần chạm hay không. Cấu hình đối chứng có cùng danh sách ứng viên phải được chạy trước mọi hạt giống thứ hai, vì thiếu nó thì không còn số nào cho biết bước chọn đóng góp bao nhiêu.
- **Nối độ đo với đánh giá của người.** Cần hai người độc lập chấm thủ công 100 câu rồi tính mức đồng thuận giữa điểm chấm tay và executability. Chỉ phép đo này mới kiểm được rủi ro đến từ việc người nghe của độ đo là một mô hình.
- **Đo độ bền trước phép viết lại mạnh hơn.** Hướng này viết lại chính tên gọi và cách mô tả phần tử, ngoài động từ và trật tự câu, rồi chạy lại mô hình định vị để trả lời đầy đủ cảnh báo của Jandial và cộng sự [18].
- **Cải thiện bộ liệt kê phần tử.** Luật ô Voronoi không thể chặt hơn mức đầy đủ của bộ liệt kê phần tử, nên ghép thêm một bộ phát hiện phần tử dựa trên ảnh bên cạnh cây trợ năng sẽ nâng trực tiếp độ chặt của độ đo, rõ nhất ở các nút chỉ có biểu tượng và ở hàng danh sách.
- **Mở rộng phạm vi.** Xếp theo chi phí tăng dần, các bước mở rộng gồm chấm trên phần kiểm chính thức của AndroidControl để so được với công trình khác, xét chuỗi nhiều màn hình liên tiếp, xét giao diện tiếng Việt, và thêm một bộ dữ liệu thứ hai để tách kết luận khỏi đặc thù của AndroidControl.

## 7.4 Tính sẵn có của dữ liệu và mã nguồn

Toàn bộ số liệu trong đề tài tái tạo được từ mã nguồn và tệp kết quả thô đi kèm.

**Dữ liệu nguồn** là AndroidControl [1], giấy phép CC0, lấy qua hai bản phân phối công khai trên Hugging Face đã nêu ở Bảng 3.2; ảnh màn hình không được phân phối lại.

**Mã nguồn** gồm các bước dựng dữ liệu (ghép nguồn, OCR, dựng nhãn mô tả, dựng dữ liệu cho bốn cấu hình), tệp cấu hình huấn luyện dùng chung cho mọi mô hình, chương trình sinh câu, và chương trình chấm điểm cùng phần tự kiểm chạy được của luật chấm.

**Kết quả thô** được lưu ở mức từng bước. Mỗi mô hình có một tệp câu sinh ra, một tệp điểm tổng hợp, và một tệp ghi mỗi bước một dòng kèm tọa độ mô hình định vị trả về, tọa độ đáp án, số phần tử trên màn và giá trị của cả ba điều kiện chấm. Nhờ tệp cuối, việc đổi luật chấm hay thêm một cách chia nhóm để phân tích chỉ cần tính lại từ tệp này mà không cần gọi lại mô hình định vị.

# Chương 8. Các công trình nghiên cứu

Một phần nội dung của đề tài được viết thành hai bài báo tách rời, khác nhau về đóng góp chính, về ngôn ngữ và về số liệu sử dụng.

> Lê Đoàn Phương Uyên, TS. Nguyễn Hồng Bửu Long. “Sinh hướng dẫn sử dụng phần mềm từ ảnh chụp màn hình và mục tiêu người dùng: xây dựng nhãn quy chiếu tự động khi phần tử giao diện không có tên để gọi.”

Bài viết bằng tiếng Việt, nộp ngày 30 tháng 8 năm 2026 và đã được chấp nhận tại **Hội thảo Quốc gia lần thứ tư về Ngôn ngữ học Tính toán (VCL 2026)**. Đóng góp chính của bài là phần nhãn quy chiếu và quy trình dựng dữ liệu ở Chương 3. Bài đặt bài toán vào dòng nghiên cứu sinh biểu thức quy chiếu, tức sinh mô tả đủ để người nghe nhận ra đúng một đối tượng, rồi áp vào miền giao diện. Trong miền này, 22,0% phần tử cần chạm không có tên nào để gọi và 7,6% trùng tên với một phần tử khác trên cùng màn hình.

> Lê Đoàn Phương Uyên, TS. Nguyễn Hồng Bửu Long. “Separating the Action Gate from Geometry in Execution-Based Evaluation for GUI Instruction Generation”.

Bài viết bằng tiếng Anh, nộp ngày 21 tháng 9 năm 2026 tới hội nghị **SOICT 2026 (mã bài 5577)** và đang chờ kết quả bình duyệt. Kỷ yếu của hội nghị dự kiến thuộc tùng thư CCIS. Đóng góp chính của bài thuộc về đo lường, cụ thể bài chỉ ra rằng khi chấm câu hướng dẫn bằng độ đo dựa trên thực thi, cần tách phần điểm do điều kiện đúng loại thao tác mang lại khỏi phần điểm do định vị phần tử. Lý do là dưới luật khoảng cách Euclid của AndroidInTheWild, phần điểm mà giai đoạn thưởng tọa độ (một hướng đã thử) hơn mô hình tinh chỉnh có giám sát (S1) gần như hoàn toàn đến từ nhóm bước mà S1 gọi sai loại thao tác (Mục 6.5).

Hai bài không chồng lấn về đóng góp, vì bài thứ nhất thuộc về dữ liệu còn bài thứ hai thuộc về đo lường. **Phương pháp đề xuất (Chương 4)** được thực hiện sau ngày nộp của cả hai bài, nên không thuộc bài nào.

# Tài liệu tham khảo

[1] W. Li, W. E. Bishop, A. Li, C. Rawles, F. Campbell-Ajala, D. Tyamagundlu, O. Riva, “On the effects of data scale on UI control agents,” in *Advances in Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track*, 2024.

[2] C. Rawles, A. Li, D. Rodriguez, O. Riva, T. P. Lillicrap, “AndroidInTheWild: A large-scale dataset for Android device control,” in *Advances in Neural Information Processing Systems (NeurIPS)*, 2023.

[3] K. Cheng, Q. Sun, Y. Chu, F. Xu, Y. Li, J. Zhang, Z. Wu, “SeeClick: Harnessing GUI grounding for advanced visual GUI agents,” in *Proc. Annual Meeting of the Association for Computational Linguistics (ACL)*, 2024.

[4] Z. Wu, Z. Wu, F. Xu, Y. Wang, Q. Sun, C. Jia, K. Cheng, Z. Ding, L. Chen, P. P. Liang, Y. Qiao, “OS-ATLAS: Foundation action model for generalist GUI agents,” in *Proc. International Conference on Learning Representations (ICLR)*, 2025.

[5] B. Gou, R. Wang, B. Zheng, Y. Xie, C. Chang, Y. Shu, H. Sun, Y. Su, “Navigating the digital world as humans do: Universal visual grounding for GUI agents,” in *Proc. International Conference on Learning Representations (ICLR)*, 2025 (Oral).

[6] inclusionAI, “UI-Venus technical report: Building high-performance UI agents with RFT,” arXiv:2508.10833, 2025 (bản tiền ấn phẩm).

[7] Y. Xu, Z. Wang, J. Wang, D. Lu, T. Xie, A. Saha, D. Sahoo, T. Yu, C. Xiong, “Aguvis: Unified pure vision agents for autonomous GUI interaction,” in *Proc. International Conference on Machine Learning (ICML)*, 2025.

[8] X. Deng, Y. Gu, B. Zheng, S. Chen, S. Stevens, B. Wang, H. Sun, Y. Su, “Mind2Web: Towards a generalist agent for the web,” in *Advances in Neural Information Processing Systems (NeurIPS)*, 2023.

[9] Y. Li, G. Li, L. He, J. Zheng, H. Li, Z. Guan, “Widget captioning: Generating natural language description for mobile user interface elements,” in *Proc. Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 2020.

[10] B. Wang, G. Li, X. Zhou, Z. Chen, T. Grossman, Y. Li, “Screen2Words: Automatic mobile UI summarization with multimodal learning,” in *Proc. ACM Symposium on User Interface Software and Technology (UIST)*, 2021.

[11] J. Mao, J. Huang, A. Toshev, O. Camburu, A. Yuille, K. Murphy, “Generation and comprehension of unambiguous object descriptions,” in *Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2016.

[12] R. Luo, G. Shakhnarovich, “Comprehension-guided referring expressions,” in *Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2017.

[13] L. Yu, H. Tan, M. Bansal, T. L. Berg, “A joint speaker-listener-reinforcer model for referring expressions,” in *Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2017.

[14] S. Petryk, D. Chan, A. Kachinthaya, H. Zou, J. Canny, J. Gonzalez, T. Darrell, “ALOHa: A new measure for hallucination in captioning models,” in *Proc. NAACL-HLT, Short Papers*, 2024.

[15] A. B. Sai, T. Dixit, D. Y. Sheth, S. Mohan, M. M. Khapra, “Perturbation CheckLists for evaluating NLG evaluation metrics,” in *Proc. Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 2021.

[16] E. Clark, T. August, S. Serrano, N. Haduong, S. Gururangan, N. A. Smith, “All that’s ‘human’ is not gold: Evaluating human evaluation of generated text,” in *Proc. ACL-IJCNLP*, 2021.

[17] J. Chen, C. Chen, Z. Xing, X. Xu, L. Zhu, G. Li, J. Wang, “Unblind your apps: Predicting natural-language labels for mobile GUI components by deep learning,” in *Proc. International Conference on Software Engineering (ICSE)*, 2020 (Distinguished Paper).

[18] S. Jandial, Y. Li, J. Wagle, K. Koishida, “Do GUI grounders truly understand UI elements?,” in *Findings of the Association for Computational Linguistics: EACL*, 2026.

[19] K. Fang, J. Zhang, S.-T. Ni, P. Hui, Y. Wang, “GuideMe: A VLM-based system assisting independent smartphone learning for older adults,” in *Proc. ACM Conference on Human Factors in Computing Systems (CHI)*, 2026.

[20] K. Papineni, S. Roukos, T. Ward, W.-J. Zhu, “BLEU: A method for automatic evaluation of machine translation,” in *Proc. Annual Meeting of the Association for Computational Linguistics (ACL)*, 2002.

[21] C.-Y. Lin, “ROUGE: A package for automatic evaluation of summaries,” in *Proc. Workshop on Text Summarization Branches Out, ACL*, 2004.

[22] M. Denkowski, A. Lavie, “Meteor Universal: Language specific translation evaluation for any target language,” in *Proc. Ninth Workshop on Statistical Machine Translation (WMT)*, pp. 376–380, 2014.

[23] R. Vedantam, C. L. Zitnick, D. Parikh, “CIDEr: Consensus-based image description evaluation,” in *Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, pp. 4566–4575, 2015.

[24] P. Anderson, B. Fernando, M. Johnson, S. Gould, “SPICE: Semantic propositional image caption evaluation,” in *Proc. European Conference on Computer Vision (ECCV)*, pp. 382–398, 2016.

[25] M. Popović, “chrF: Character n-gram F-score for automatic MT evaluation,” in *Proc. Tenth Workshop on Statistical Machine Translation (WMT)*, pp. 392–395, 2015.

[26] T. Zhang, V. Kishore, F. Wu, K. Q. Weinberger, Y. Artzi, “BERTScore: Evaluating text generation with BERT,” in *Proc. International Conference on Learning Representations (ICLR)*, 2020.

[27] A. C. Cameron, J. B. Gelbach, D. L. Miller, “Bootstrap-based improvements for inference with clustered errors,” *Review of Economics and Statistics*, vol. 90, no. 3, pp. 414–427, 2008.

[28] L. Kish, *Survey Sampling*. New York, NY, USA: Wiley, 1965.

[29] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen, “LoRA: Low-rank adaptation of large language models,” in *Proc. International Conference on Learning Representations (ICLR)*, 2022.

[30] T. Dettmers, A. Pagnoni, A. Holtzman, L. Zettlemoyer, “QLoRA: Efficient finetuning of quantized LLMs,” in *Advances in Neural Information Processing Systems (NeurIPS)*, 2023.

[31] Y. Zheng, R. Zhang, J. Zhang, Y. Ye, Z. Luo, “LlamaFactory: Unified efficient fine-tuning of 100+ language models,” in *Proc. ACL, System Demonstrations*, 2024.

[32] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, I. Polosukhin, “Attention is all you need,” in *Advances in Neural Information Processing Systems (NeurIPS)*, 2017.

[33] J. Qi, M. Ding, W. Wang, Y. Bai, Q. Lv, W. Hu, Z. Yang, Y. Dong, J. Tang, “CogCoM: A visual language model with chain-of-manipulations reasoning,” in *Proc. International Conference on Learning Representations (ICLR)*, 2025.

[34] S. Bai et al., “Qwen2.5-VL technical report,” arXiv:2502.13923, 2025 (bản thảo tiền ấn phẩm).

[35] K. Chen, Z. Zhang, W. Zeng, R. Zhang, F. Zhu, R. Zhao, “Shikra: Unleashing multimodal LLM’s referential dialogue magic,” arXiv:2306.15195, 2023 (bản thảo tiền ấn phẩm).

[36] Q. Wu, X. Yang, Y. Zhou, C. Fang, B. Song, X. Sun, R. Ji, “Grounded chain-of-thought for multimodal large language models,” arXiv:2503.12799, 2025 (bản thảo tiền ấn phẩm; không phải bài ICCV 2025 cùng hướng, mã số 2507.02859).

[37] M. Zhao, P. Anderson, V. Jain, S. Wang, A. Ku, J. Baldridge, E. Ie, “On the evaluation of vision-and-language navigation instructions,” in *Proc. Conference of the European Chapter of the Association for Computational Linguistics (EACL)*, pp. 1302–1316, 2021.

[38] N. Nangia, S. R. Bowman, “Human vs. Muppet: A conservative estimate of human performance on the GLUE benchmark,” in *Proc. Annual Meeting of the Association for Computational Linguistics (ACL)*, 2019.

[39] P. Rajpurkar, R. Jia, P. Liang, “Know what you don’t know: Unanswerable questions for SQuAD,” in *Proc. Annual Meeting of the Association for Computational Linguistics (ACL), Short Papers*, pp. 784–789, 2018.

[40] A. K. Menon, S. Jayasumana, A. S. Rawat, H. Jain, A. Veit, S. Kumar, “Long-tail learning via logit adjustment,” in *Proc. International Conference on Learning Representations (ICLR)*, 2021.

[41] N. F. Liu, K. Lin, J. Hewitt, A. Paranjape, M. Bevilacqua, F. Petroni, P. Liang, “Lost in the middle: How language models use long contexts,” *Transactions of the Association for Computational Linguistics*, vol. 12, pp. 157–173, 2024.

[42] D. Guo et al., “DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning,” *Nature*, vol. 645, no. 8081, pp. 633–638, 2025.

[43] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. K. Li, Y. Wu, D. Guo, “DeepSeekMath: Pushing the limits of mathematical reasoning in open language models,” bản tiền ấn phẩm arXiv:2402.03300, 2024.

[44] A. Abouelenin et al., “Phi-4-Mini technical report: Compact yet powerful multimodal language models via mixture-of-LoRAs,” bản tiền ấn phẩm arXiv:2503.01743, 2025.

[45] J. Yang, H. Zhang, F. Li, X. Zou, C. Li, J. Gao, “Set-of-Mark prompting unleashes extraordinary visual grounding in GPT-4V,” bản tiền ấn phẩm arXiv:2310.11441, 2023.

[46] S. J. Rennie, E. Marcheret, Y. Mroueh, J. Ross, V. Goel, “Self-critical sequence training for image captioning,” trong *Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR)*, 2017.

[47] R. Ramos, B. Martins, D. Elliott, Y. Kementchedjhieva, “SmallCap: Lightweight image captioning prompted with retrieval augmentation,” trong *Proc. IEEE/CVF Conf. Computer Vision and Pattern Recognition (CVPR)*, 2023.

[48] S. Liu, Z. Zhu, N. Ye, S. Guadarrama, K. Murphy, “Improved image captioning via policy gradient optimization of SPIDEr,” trong *Proc. IEEE Int. Conf. Computer Vision (ICCV)*, 2017, pp. 873–881.

# Phụ lục A. Các hướng đã thử

Phụ lục này trình bày, theo thứ tự thực hiện, các hướng đã thử trước khi chọn phương pháp đề xuất, với phần tóm tắt ở Mục 6.10. Trong các bảng, S1 là mô hình tinh chỉnh có giám sát, dùng làm mốc so sánh; S2 là mô hình mô tả phần tử; CE2-S2 là mô hình học thêm có giám sát; MIN-DESC (MIN) là mô hình sau giai đoạn học ưu tiên; Base là mô hình gốc và Trần là câu chuẩn.

## A.1 Mô tả phần tử trước khi viết câu

### A.1.1 Thiết kế

Hướng đầu tiên dạy mô hình mô tả phần tử cần chạm trước rồi mới viết câu, thay vì sinh thẳng câu từ ảnh. Mô hình được huấn luyện theo cách này gọi là mô hình mô tả phần tử. Chuỗi mà mô hình cần sinh gồm hai phần, như ở khối dưới đây.

```text
dòng mô tả phần tử <desc> vai trò | tên | <point>x,y</point>
| dấu hiệu phân biệt </desc>
phần câu câu hướng dẫn
```

Lúc chấm, dòng mô tả bị cắt bỏ và mô hình định vị chỉ nhận câu hướng dẫn, nên nếu điểm tăng thì lý do nằm ở hành vi của mô hình sinh câu. Thiết kế dựa trên ba căn cứ. Thứ nhất, dạng lỗi đã đo được chủ yếu là câu mơ hồ (Chương 1), nên dòng mô tả có một ô ghi dấu hiệu phân biệt. Thứ hai, hai dòng Shikra trong Bảng 1.1 cho kết quả âm khi bước trung gian là văn xuôi và dương khi bước trung gian có tọa độ, nên dòng mô tả gồm bốn ô cố định và bắt buộc có tọa độ. Thứ ba, tọa độ chạm của người thật có sẵn trong dữ liệu, nên nhãn tọa độ sạch 100% mà không tốn chi phí dựng. Thiết kế còn có mục thứ hai, tức phạt mô hình khi xác suất của dòng mô tả trỏ đúng phần tử không vượt xác suất của dòng mô tả trỏ sang phần tử lân cận ít nhất một khoảng lề, là phần mà Widget Captioning [9] chưa xử lý. Mục này chưa được thực hiện vì mục thứ nhất, tức bản thân dòng mô tả, chưa cho thấy tác dụng (Mục A.1.3).

### A.1.2 Các cấu hình của thiết kế so sánh ban đầu

Thiết kế so sánh ban đầu gồm bảy cấu hình, dùng chung dữ liệu, mô hình gốc, siêu tham số và tập kiểm tra (Bảng A.1).

**Bảng A.1.** Các cấu hình của thiết kế so sánh ban đầu. Ba cấu hình cuối không cần huấn luyện.

| Cấu hình | Chuỗi phải sinh ra hoặc cách chạy | Vai trò |
|---|---|---|
| Tinh chỉnh có giám sát (S1) | chỉ câu hướng dẫn (2 hạt giống) | mốc so sánh |
| Mô tả phần tử (S2) | dòng mô tả thật + câu (2 hạt giống) | phép so sánh chính của thiết kế ban đầu, kiểm tác dụng của việc mô tả phần tử trước |
| Mô tả giả (S2r) | dòng mô tả giả khớp độ dài + câu | loại trừ khả năng điểm tăng chỉ do chuỗi phải sinh ra dài thêm |
| Mô tả không có tọa độ (S2-nopoint) | dòng mô tả bỏ tọa độ + câu | tách phần đóng góp của tọa độ |
| Danh sách phần tử lúc chạy (B-infer) | trọng số S1, danh sách phần tử đưa vào đầu vào lúc chạy | so huấn luyện với việc chỉ cung cấp thông tin lúc chạy |
| Mô hình gốc (Base) | mô hình gốc, không tinh chỉnh | đo phần cải thiện do bản thân việc tinh chỉnh |
| Câu chuẩn (Trần) | câu chuẩn đưa thẳng đi chấm | ngưỡng tối đa của độ đo |

Đại lượng quan tâm là Δ = S2 − S1, tính trên trung bình hai hạt giống của mỗi mô hình. Hai lượt huấn luyện mô hình tinh chỉnh có giám sát chỉ khác nhau ở hạt giống, nên chênh lệch giữa chúng cho biết điểm số dao động bao nhiêu khi chỉ huấn luyện lại mà không có can thiệp nào. Bốn cấu hình không được chạy, gồm hạt giống thứ hai của mô hình mô tả phần tử, cấu hình mô tả giả, cấu hình mô tả không có tọa độ và cấu hình chỉ đưa danh sách phần tử vào lúc chạy (lý do ở Bảng 6.13). Do thiếu hạt giống thứ hai của mô hình mô tả phần tử, Δ không tính đủ được theo định nghĩa trên; chúng tôi giữ nguyên định nghĩa thay vì sửa cho vừa với dữ liệu có được.

### A.1.3 Kết quả

Mô hình mô tả phần tử đạt 57,2%, thấp hơn mô hình tinh chỉnh có giám sát 1,93 điểm ở hạt giống 101 và 2,44 điểm ở hạt giống 202 (Bảng 6.8); khoảng tin cậy của cả hai chênh lệch đều nằm dưới 0. Theo tiêu chí ở Mục 4.8, đây là kết quả âm, dù chưa đủ để kết luận rằng việc mô tả phần tử trước luôn gây hại. Kết quả âm này giữ nguyên khi chấm lại bằng mô hình định vị thứ hai (Mục 5.9). Mô hình vẫn hơn mô hình gốc 9,59 điểm, nên việc thêm dòng mô tả không làm mất tác dụng của việc tinh chỉnh.

Chúng tôi đã kiểm bốn cách giải thích thay thế và không cách nào giải thích được chênh lệch. Bốn cách đó là độ dài câu, nhóm ứng dụng, việc phép chuẩn hoá loại thao tác của độ đo xếp cụm *go back* vào lớp chạm, và tên ghi trong dòng mô tả bị sai do lỗi nhận dạng chữ.

#### A.1.3.1 Chia nhóm theo việc có sinh dòng mô tả hay không

**Bảng A.2.** Điểm chia theo việc mô hình mô tả phần tử (S2) có sinh dòng mô tả hay không.

| Nhóm | n | S1 | S2 | Δ |
|---|---:|---:|---:|---:|
| Có sinh dòng mô tả | 4.138 | 62,2 | 60,8 | -1,38 [-2,54; -0,19] |
| Không sinh dòng mô tả | 325 | 19,7 | 10,8 | -8,92 [-12,57; -5,25] |

Theo Bảng A.2, nhóm 325 bước mà mô hình mô tả phần tử bỏ qua dòng mô tả chỉ gồm 7,3% số bước nhưng chiếm 34% toàn bộ chênh lệch. Ở nhóm này mô hình phần lớn đoán sai loại thao tác, trong khi câu chuẩn vẫn đạt 68,3%, tức các bước này vẫn giải được. Mô hình gốc gọi đúng loại thao tác ở 83,4% số bước trong nhóm, mô hình tinh chỉnh có giám sát ở 55,1% và mô hình mô tả phần tử ở 38,8%. Như vậy chính việc tinh chỉnh đã làm lệch xu hướng chọn loại thao tác, và việc thêm dòng mô tả khuếch đại độ lệch ấy. Chúng tôi nghi đây là một lỗi tắt học từ dữ liệu, vì tập huấn luyện chỉ gắn dòng mô tả cho bước chạm, nên mô hình có thể học quy tắc “đã viết dòng mô tả thì là chạm”. Giả thuyết này chưa được kiểm vì cấu hình mô tả không có tọa độ đã bị hủy. Nhóm này được định nghĩa bằng hành vi của chính mô hình mô tả phần tử, nên việc mô hình này kém trên nhóm một phần là hệ quả của cách chia nhóm. Dù vậy, mô hình tinh chỉnh có giám sát cũng chỉ đạt 19,7% trên cùng nhóm.

#### A.1.3.2 Ảnh hưởng hai chiều của dòng mô tả

**Bảng A.3.** Điểm theo trạng thái dòng mô tả do mô hình mô tả phần tử (S2) tự sinh. Cột Trần là điểm của câu chuẩn trên chính nhóm đó.

| Tên | Tọa độ | n | Base | S1 | S2 | Trần |
|---|---|---:|---:|---:|---:|---:|
| đúng | trúng | 1.871 | 69,0 | 81,4 | 87,1 | 86,6 |
| đúng | trượt | 184 | 23,4 | 25,5 | 26,1 | 31,0 |
| sai | trúng | 452 | 41,4 | 56,4 | 57,5 | 72,8 |
| sai | trượt | 738 | 24,4 | 30,8 | 5,6 | 66,3 |
| không sinh dòng mô tả |  | 228 | 25,9 | 20,6 | 9,6 | 70,6 |

Bảng A.3 chia các bước được chấm theo việc dòng mô tả do chính mô hình mô tả phần tử sinh ra có đúng tên và tọa độ hay không. Khi đúng cả hai, mô hình đạt 87,1%, hơn mô hình tinh chỉnh có giám sát 5,7 điểm và vượt cả câu chuẩn trên nhóm đó. Khi sai cả hai, mô hình chỉ còn 5,6%, dưới cả mức ngưỡng tối thiểu của độ đo (câu chung chung không nói phần tử nào đạt 12,0%, Mục 5.6), trong khi câu chuẩn vẫn đạt 66,3% trên 738 bước ấy. Ở nhóm này mô hình đã chọn một phần tử sai rồi viết câu khẳng định về phần tử đó, còn mô hình tinh chỉnh có giám sát viết câu chung chung nên vẫn có cơ hội trúng. Dòng mô tả vì vậy khuếch đại kết quả theo cả hai chiều, và đây là căn cứ của giai đoạn học ưu tiên (Mục A.2.1).

## A.2 Học ưu tiên trên dòng mô tả

### A.2.1 Thiết kế

Kết quả của mô hình mô tả phần tử cho thấy độ chính xác của dòng mô tả đang là nguyên nhân hạn chế kết quả chung (Mục A.1.3.2), trong khi học có giám sát thuần chỉ nâng xác suất của chuỗi đúng mà không hạ xác suất của chuỗi sai gần kề. Giai đoạn học ưu tiên trên dòng mô tả (gọi tắt là giai đoạn học ưu tiên, trong bảng là MIN-DESC) vì vậy học tiếp từ trọng số đã huấn luyện của mô hình mô tả phần tử thêm 800 bước cập nhật, với một mục tiêu ưu tiên trên các cặp quy chiếu tối thiểu có dạng như sau.

```text
vế được chọn <desc>mô tả trỏ đúng phần tử</desc> + \\ n + câu
vế bị loại    <desc>mô tả trỏ sai phần tử</desc> + \\ n + đúng câu đó
```

Hai vế chỉ khác nhau ở dòng mô tả, nên số hạng ưu tiên chỉ giảm được khi mô hình chọn đúng phần tử. Dòng mô tả trỏ sai là mô tả của một phần tử có thật, cùng vai trò, nằm gần phần tử cần chạm; cách dựng 22.854 cặp nằm ở Mục 3.7. Hàm mục tiêu thuộc họ tối ưu theo ưu tiên dạng tỉ số odds (ORPO), không cần mô hình tham chiếu đóng băng.

Để tách phần của mục tiêu ưu tiên khỏi phần của việc học thêm, mô hình học thêm có giám sát (CE2-S2) học có giám sát thuần trên vế được chọn của các cặp ấy, cùng điểm xuất phát và số bước. Đại lượng chính là hiệu ghép cặp Δ_thành phần = MIN-DESC − CE2-S2, tính trên cùng các bước của tập kiểm tra (Mục 4.8). Tập cặp chỉ chứa bước chạm, nên thiệt hại ở bước không chạm được đo riêng (Mục A.2.2.4).

### A.2.2 Kết quả

#### A.2.2.1 Độ chính xác của dòng mô tả

Bảng A.4 đối chiếu thẳng dòng mô tả do mô hình tự sinh với nhãn chuẩn của tập kiểm tra, không cần gọi mô hình định vị.

**Bảng A.4.** Độ chính xác của dòng mô tả trên 3.473 bước có tên đúng để đối chiếu, chỉ tính các bước có mặt trong kết quả của cả ba mô hình.

| Mô hình | Sinh dòng mô tả | Tên đúng | Tọa độ đúng | Cả hai đúng |
|---|---:|---:|---:|---:|
| Mô tả phần tử (S2) | 93,4% | 59,2% | 66,9% | 53,9% |
| Học thêm có giám sát (CE2-S2) | 99,6% | 66,2% | 71,2% | 59,8% |
| Học ưu tiên (MIN-DESC) | 99,6% | 67,0% | 71,8% | 60,6% |

So với mô hình mô tả phần tử, tỉ lệ đúng cả tên lẫn tọa độ sau giai đoạn học ưu tiên tăng 6,77 điểm. Mô hình học thêm có giám sát cũng đạt 5,93 điểm trong mức tăng ấy, nên phần riêng của mục tiêu ưu tiên chỉ là 0,84 điểm, và 87,7% mức tăng đến từ chính việc học thêm.

#### A.2.2.2 Executability và đại lượng chính

Sau giai đoạn học ưu tiên, mô hình đạt 60,0%, còn mô hình học thêm có giám sát đạt 59,4% (Bảng 6.1). Đại lượng chính Δ_thành phần bằng +0,63 điểm, khoảng tin cậy 95% là [+0,16; +1,10] và p = 0,011 (Bảng 6.8). Khoảng tin cậy không chứa 0, nhưng mức này chỉ bằng 1,4 lần độ lệch chuẩn giữa hai hạt giống (0,46 điểm, Mục 6.7), tức chưa vượt rõ mức dao động khi chỉ huấn luyện lại với hạt giống khác. Vì vậy chúng tôi không gọi đây là tác dụng của mục tiêu ưu tiên. MIN-DESC hơn mô hình mô tả phần tử 2,87 điểm, nhưng 2,24 điểm trong đó đã có ở mô hình học thêm có giám sát, tức 78% mức tăng thuộc về bản thân việc học thêm. So với hạt giống 101 của mô hình tinh chỉnh có giám sát, MIN-DESC chỉ hơn 0,94 điểm và mô hình học thêm hơn 0,31 điểm, đều có khoảng tin cậy phủ 0. Giai đoạn học ưu tiên vì vậy chủ yếu sửa lại thiệt hại do chính dòng mô tả gây ra, rồi tăng thêm một mức nhỏ so với mô hình tinh chỉnh có giám sát.

#### A.2.2.3 Biến thể lấy vế bị loại theo chính sách

Ngoài nguồn dựng bằng luật (cửa sổ 80 đến 350 điểm ảnh quanh phần tử cần chạm), chúng tôi thử lấy vế bị loại theo chính sách (*on-policy*), tức lấy chính phần tử mà mô hình gọi nhầm. Hướng này dừng trước khi huấn luyện, vì cho mô hình sinh dòng mô tả trên 14.000 màn huấn luyện chỉ thu được 459 cặp hợp lệ, tức 3,3% số màn. Trên 3.246 bước gọi sai tên, khoảng cách từ phần tử bị gọi nhầm tới phần tử cần chạm có trung vị 351 điểm ảnh, và cửa sổ 80 đến 350 điểm ảnh loại mất 76,5% số bước này. Lỗi trong dòng mô tả vì vậy rơi vào hai cực. Mô hình hoặc gọi đúng phần tử bằng tên khác, hoặc nhìn sang hẳn một vùng khác của màn hình, và hiếm khi lẫn giữa hai nút cạnh nhau như biến thể này giả định. Vế bị loại dựng bằng luật vì thế phải tự tạo ra dạng lẫn giữa hai phần tử gần nhau mà mô hình ít khi tự mắc. Cách dựng này là nguồn còn dùng được sau phép đo trên, không phải lựa chọn thiết kế từ đầu.

#### A.2.2.4 Thiệt hại đo được ở bước không chạm

**Bảng A.5.** Khớp loại thao tác trên mẫu 400 bước không chạm (cuộn 96, chờ 86, gõ chữ 82, mở ứng dụng 81, quay lại 55), chấm với biến thể nghiêm ngặt của điều kiện khớp loại thao tác.

| Mô hình | Khớp loại thao tác | Δ so với S2 |
|---|---:|---:|
| Mô tả phần tử (S2) | 83,5% | – |
| Học thêm có giám sát (CE2-S2) | 63,0% | -20,50 |
| Học ưu tiên (MIN-DESC) | 63,8% | -19,75 |

Đánh giá ở bước không chạm (Mục 5.13) cho thấy sau giai đoạn học ưu tiên, mô hình kém đi rất nhiều ở nhóm bước này (Bảng A.5). Mức giảm tập trung ở cuộn (-43,8), quay lại (-36,4) và gõ chữ (-29,2), ba loại thao tác mà câu chuẩn không nhắc tên phần tử nào; hai loại chờ và mở ứng dụng không giảm, nhưng chỉ vì phép chuẩn hoá loại thao tác xếp động từ “mở” vào lớp chạm. Mô hình học thêm có giám sát giảm gần như ngang bảng (-20,50 so với -19,75), nên mức giảm gắn với việc học thêm trên dữ liệu chỉ gồm bước chạm, không phải với mục tiêu ưu tiên. Executability chỉ chấm bước chạm nên không thấy mức giảm này.

### A.2.3 Tìm chỗ nghẽn của cách mô tả phần tử trước

Phân tích này là hậu kiểm, vì cách chia nhóm dựa trên hành vi của chính mô hình được đo. Hai nhóm khác nhau nhiều về độ khó, nên chỉ phép so sánh ghép cặp bên trong một nhóm là hợp lệ. Bảng A.6 chia 3.473 bước có tên đúng để đối chiếu theo việc dòng mô tả của MIN-DESC trỏ đúng phần tử (tên khớp và tọa độ nằm trong dung sai 14%) hay trỏ sai.

**Bảng A.6.** Điểm của mô hình sau giai đoạn học ưu tiên (MIN-DESC) và mô hình tinh chỉnh có giám sát (S1) trên 3.473 bước có tên đúng để đối chiếu, chia theo việc dòng mô tả của MIN-DESC trỏ đúng hay trỏ sai phần tử. Cột Trần là điểm của câu chuẩn trên chính nhóm đó.

| Nhóm | n | MIN-DESC | S1 | Δ ghép cặp | Trần |
|---|---:|---:|---:|---:|---:|
| Trỏ đúng phần tử | 2.106 (60,6%) | 87,1 | 78,3 | +8,83 | 86,3 |
| Trỏ sai phần tử | 1.367 (39,4%) | 21,8 | 32,9 | -11,12 | 61,4 |

Khi dòng mô tả trỏ đúng phần tử, MIN-DESC hơn mô hình tinh chỉnh có giám sát 8,83 điểm và vượt cả ngưỡng tối đa của câu chuẩn trên nhóm đó; khi dòng mô tả trỏ sai, MIN-DESC thấp hơn 11,12 điểm. Hai chiều gần như triệt tiêu nhau, chỉ còn lại mức +0,94 điểm không có ý nghĩa thống kê (Mục A.2.2). Như vậy việc mô tả phần tử trước có tác dụng đúng như giả thuyết, nhưng chỉ trên 60,6% số bước mà dòng mô tả trỏ trúng.

**Ngưỡng tối đa lý thuyết khi bù được phần thiệt ở các bước mô tả sai.** Giả sử ở mỗi bước mà dòng mô tả trỏ sai, MIN-DESC cho đúng kết quả của mô hình tinh chỉnh có giám sát. Khi đó điểm trên 3.473 bước có tên đúng để đối chiếu sẽ là 65,8% thay vì 61,4% thực đo, tức cao hơn mô hình tinh chỉnh có giám sát 5,4 điểm. Mức này không đạt được ở khâu suy luận bằng một quy tắc chọn câu ở từng bước, tức quyết định lấy câu của MIN-DESC hay câu của mô hình tinh chỉnh có giám sát. Một quy tắc hoàn hảo, biết trước dòng mô tả trỏ đúng hay sai, cho 63,5% trên toàn bộ 4.463 bước, nhưng bảy quy tắc thực tế đã thử chỉ cho 60,0 đến 60,3%, không khác biệt rõ so với mức 60,0% của MIN-DESC. Chỗ nghẽn này vì vậy phải được sửa ở khâu huấn luyện.

**Bảng A.7.** Phân rã toàn bộ 4.463 bước theo trạng thái dòng mô tả của MIN-DESC (cột MIN). Cột cuối là phần dư địa tới mức câu chuẩn mà mỗi nhóm đóng góp, tính bằng điểm trên toàn tập bước được chấm.

| Nhóm | n | % | MIN | S1 | Trần | Dư địa |
|---|---:|---:|---:|---:|---:|---:|
| tên đúng, tọa độ đúng | 2.082 | 46,7 | 87,1 | 78,2 | 86,3 | -0,36 |
| tên đúng, tọa độ sai | 220 | 4,9 | 26,4 | 27,7 | 32,3 | +0,29 |
| tên sai, tọa độ đúng | 411 | 9,2 | 57,2 | 53,0 | 73,0 | +1,46 |
| không sinh dòng mô tả | 15 | 0,3 | 0,0 | 0,0 | 60,0 | +0,20 |
| tên sai, tọa độ sai | 745 | 16,7 | 3,6 | 25,8 | 64,4 | +10,15 |
| không có tên để đối chiếu | 990 | 22,2 | 55,3 | 54,4 | 73,0 | +3,94 |
| **Tổng** | **4.463** |  | **60,0** | **59,1** | **75,7** | **+15,7** |

Theo Bảng A.7, nhóm đúng cả tên lẫn tọa độ chiếm 46,7% số bước và không còn dư địa, vì ở nhóm này mô hình đã vượt ngưỡng tối đa của câu chuẩn. Phần lớn dư địa còn lại (63%) nằm ở nhóm sai cả tên lẫn tọa độ. Trên nhóm này MIN-DESC chỉ đạt 3,6% và mô hình tinh chỉnh có giám sát đạt 25,8%, trong khi câu chuẩn đạt 64,4%, nên đây không phải nhóm bước bất khả thi.

## A.3 Chọn phần tử trong danh sách ứng viên

### A.3.1 Thiết kế

Phân tích ở Mục A.2.3 cho thấy phần lớn dư địa còn lại của MIN-DESC nằm ở những bước mà dòng mô tả sai cả tên lẫn tọa độ. Vì vậy, thay vì để mô hình tự viết dòng mô tả, chúng tôi cho mô hình chọn phần tử trong danh sách lấy từ chính màn hình; mô hình huấn luyện theo cách này gọi là mô hình chọn ứng viên. Căn cứ là ba con số đo được trước khi huấn luyện. Tên đúng có mặt trong chữ OCR hoặc cây trợ năng ở 99,7% số bước. Ở 80,2% số bước có một ứng viên vừa khớp tên vừa nằm trong dung sai, so với 59,9% của dòng mô tả tự sinh. Ở 67,7% số bước mà MIN-DESC gọi sai tên, tên đúng đã nằm sẵn trong 24 dòng OCR của câu nhắc nhưng không kèm vị trí.

**Cách làm.** Câu nhắc thay 24 dòng OCR bằng danh sách ứng viên ở Mục 3.8. Chuỗi đích mở đầu bằng một thẻ chọn, là bản chép nguyên văn một dòng trong danh sách hoặc thẻ `none`, rồi mới tới câu; thẻ này được cắt bỏ trước khi chấm. Việc đưa danh sách phần tử vào đầu vào không được tính là đóng góp, vì lý do đã nêu cho danh sách chữ OCR ở Chương 4. Phần được đo là việc chọn tường minh, tức mô hình ghi rõ ứng viên mình chọn ngay trong chuỗi đích.

**Điều kiện thí nghiệm.** Mô hình chọn ứng viên khác mô hình tinh chỉnh có giám sát (S1) và MIN-DESC ở ba biến. Ngữ cảnh dài 3072 thay vì 2560 token để chứa danh sách ứng viên (mẫu dài nhất 2.017 token cộng danh sách dài nhất 1.012 token), số lượt duyệt chỉ còn một (4.036 bước) do giới hạn tài nguyên, và đầu vào có thêm danh sách ứng viên. Vì vậy điểm của mô hình này không thể đem trừ thẳng cho điểm của hai mô hình kia. Đại lượng hợp lệ là hiệu ghép cặp Δ_chọn với một cấu hình đối chứng nhận cùng danh sách ứng viên ở đầu vào nhưng chuỗi đích chỉ có câu, còn các tham số khác giữ như Bảng 4.1. Thiết kế ban đầu gồm sáu lượt huấn luyện (ba cấu hình, mỗi cấu hình hai hạt giống), nhưng năm lượt sau chỉ được chạy nếu lượt đầu cho độ chính xác chọn hơn rõ tỉ lệ 60,6% dòng mô tả trỏ đúng phần tử của MIN-DESC. Độ chính xác chọn là tỉ lệ thẻ chọn trúng phần tử cần chạm (tên khớp, tọa độ trong dung sai 14%) trên những bước mà danh sách có chứa phần tử ấy, tức có ứng viên đúng, đo trên 1.400 bước chạm đầu của tập kiểm tra.

### A.3.2 Kết quả

Mô hình chọn ứng viên được huấn luyện với hạt giống 101 trên 64.567 mẫu của Mục 3.8.

#### A.3.2.1 Độ chính xác chọn và executability

Trên 1.400 bước dùng làm tiêu chí, 1.008 bước có ứng viên đúng và thẻ chọn trúng ở 580 bước, cho độ chính xác chọn 57,54%, thấp hơn mức 60,6% của MIN-DESC, nên năm lượt còn lại không được chạy. Từ đây, 1.400 bước này được gọi là *mẫu phát triển*, còn 3.062 bước còn lại chỉ dùng để đọc kết quả. Độ chính xác chọn cũng không phải đại lượng tốt để ra quyết định, vì cũng như cột “có đáp án” của SQuAD 2.0 [39], đại lượng này chỉ đếm những bước có đáp án. Khi ép mô hình luôn chọn, độ chính xác chọn lên 69,05%, nhưng tỉ lệ thẻ đúng trên cả mẫu phát triển giảm từ 63,43% xuống 49,71%.

Trên 4.463 bước chạm, mô hình chọn ứng viên đạt 56,1%, khoảng tin cậy [54,2; 58,0] (bootstrap theo 1.091 cụm), với tỉ lệ khớp loại thao tác 90,9% và tỉ lệ trúng ô Voronoi thuần 57,4%. Điểm trên mẫu phát triển (55,4%) và trên phần còn lại (56,5%) gần nhau. Mô hình hơn mô hình gốc (chưa tinh chỉnh) 8,54 điểm (731 bước chỉ mô hình chọn ứng viên đúng, 350 bước chỉ mô hình gốc đúng, kiểm định McNemar cho p < 0,001), và chỉ phép so sánh này đọc được thành kết luận. Cấu hình đối chứng nhận cùng danh sách ứng viên nằm trong năm lượt không được chạy, nên không tính được Δ_chọn, và chúng tôi không phát biểu gì về đóng góp của việc chọn tường minh hay của danh sách ứng viên.

#### A.3.2.2 Hành vi chọn và từ chối chọn

**Bảng A.8.** Mô hình chọn ứng viên, chia theo việc danh sách có ứng viên đúng và việc mô hình có đưa ra lựa chọn hay không. Hàng đầu và hàng cuối là hành vi đúng, hai hàng giữa là hai dạng lỗi.

| Có ứng viên đúng | Mô hình | n | % tập | Exec. | Khớp thao tác |
|---|---|---:|---:|---:|---:|
| có | **chọn** | 2.326 | 52,1 | **71,4 [69,5; 73,2]** | 99,1 |
| có | **từ chối (sai)** | 872 | 19,5 | **23,7 [21,0; 26,7]** | 71,2 |
| không | chọn (sai) | 264 | 5,9 | 37,5 | 99,6 |
| không | **từ chối (đúng)** | 1.001 | 22,4 | 53,8 | 86,6 |

Khi danh sách có ứng viên đúng và mô hình đưa ra lựa chọn, điểm đạt 71,4%, cao hơn mọi mô hình đã huấn luyện và chỉ kém câu chuẩn 4,3 điểm, nên cơ chế chọn hoạt động đúng. Thiệt hại nằm ở hàng thứ hai, gồm 872 bước (27,3% số bước có ứng viên đúng) mà mô hình từ chối chọn dù đáp án nằm sẵn trong danh sách, và nhóm này chỉ đạt 23,7%. Tỉ lệ từ chối nhầm này lặp lại mức 27,1% đo độc lập trên mẫu phát triển. Trên toàn tập, mô hình từ chối chọn ở 41,97% số bước. Nếu nhóm từ chối nhầm đạt mức 68,0% của nhóm đưa ra lựa chọn, điểm toàn tập sẽ là 65,4%, tức +9,3 điểm; đây là ngưỡng tối đa ước lượng cùng dạng với con số +5,4 ở Mục A.2.3, không phải kết quả đã chạy.

**Dấu hiệu đi kèm việc từ chối chọn.** Câu mang động từ không phải chạm chiếm 28,3% số bước từ chối chọn, so với 0,97% ở bước đưa ra lựa chọn, giống hiện tượng lẫn loại thao tác ở Mục A.1.3.1. Sai số của mô hình định vị ở nhóm từ chối chọn có trung vị 19,9% bề ngang màn, so với 0,78% ở nhóm còn lại, tức mô hình nhìn sang vùng khác của màn như dạng lỗi lưỡng cực ở Mục A.2.2.3. Danh sách càng dài thì mô hình càng hay từ chối chọn (Bảng A.9), nhưng màn nhiều phần tử cũng là màn khó hơn, nên đây chỉ là tương quan.

**Bảng A.9.** Tỉ lệ từ chối chọn và executability theo số dòng trong danh sách, chỉ tính bước có ứng viên đúng. Đây là cách chia nhóm hậu kiểm.

| Số dòng trong danh sách | n | Từ chối chọn | Exec. |
|---|---:|---:|---:|
| 1 đến 5 | 178 | 18,5% | 70,8 |
| 6 đến 10 | 363 | 15,7% | 70,5 |
| 11 đến 20 | 826 | 25,9% | 60,3 |
| 21 đến 39 | 1.036 | 29,3% | 55,6 |
| 40 (mức tối đa) | 795 | 33,2% | 51,8 |

Tỉ lệ từ chối chọn cũng cao hơn khi ứng viên đúng nằm giữa danh sách (31,4%, so với 27,2% ở phần đầu và 24,3% ở phần cuối), giống hiện tượng Liu và cộng sự [41] mô tả cho ngữ cảnh dài. Đây là quan sát chưa qua kiểm định, và vị trí trong danh sách có tương quan với độ dài danh sách.

#### A.3.2.3 Tiên nghiệm của nhãn từ chối chọn trong tập huấn luyện

**Bảng A.10.** Tỉ lệ thẻ `none` theo bốn mẫu số. Mô hình phát `none` nhiều hơn tỉ lệ đúng trên loại bước bị chấm, và ít hơn tỉ lệ gặp trên toàn tập huấn luyện.

| Mẫu số | Tỉ lệ `none` |
|---|---:|
| Toàn bộ tập huấn luyện (64.567 mẫu) | 54,78% |
| Chỉ bước chạm của tập huấn luyện (41.191) | 29,12% |
| Bước chạm của tập kiểm tra, tỉ lệ đúng (4.463) | 28,34% |
| Tỉ lệ mô hình phát ra trên tập kiểm tra | 41,97% |

Tỉ lệ mô hình phát ra nằm giữa tỉ lệ đúng trên bước chạm và tỉ lệ trên toàn tập huấn luyện, và gần tỉ lệ toàn tập hơn. Vì mọi bước không chạm đều mang thẻ `none` (Mục 3.8), hơn một nửa số mẫu dạy mô hình phát thẻ này. Cách giải thích của chúng tôi là mô hình học tỉ lệ nền ấy, tức tiên nghiệm của nhãn, rồi mang sang bước chạm, là loại bước duy nhất được chấm. Rajpurkar và cộng sự [39] nêu hiện tượng tương tự cho SQuAD 2.0, còn Menon và cộng sự [40] chứng minh rằng dưới dạng lệch phân bố nhãn, sửa tiên nghiệm lúc huấn luyện tương đương với sửa sau huấn luyện. Tỉ lệ đúng trên bước chạm của tập huấn luyện (29,12%) và của tập kiểm tra (28,34%) chỉ chênh 0,8 điểm, nên mô hình không bị dạy sai tỉ lệ trên bước chạm; quan hệ nhân quả giữa tiên nghiệm toàn tập và mức từ chối chọn thì chưa được chứng minh.

Chúng tôi cũng đã đo và loại ba hướng sửa khác. Sửa hết lỗi loại thao tác chỉ thêm 1,21 điểm. Rút danh sách còn mười dòng hạ độ phủ ứng viên đúng từ 71,7% xuống nhiều nhất 51,7%. Nới dung sai tọa độ chỉ nâng độ phủ lên 76,0% mà lại đổi nhãn huấn luyện. Hướng còn lại là huấn luyện lại chỉ trên 41.191 bước chạm để đưa tiên nghiệm về 29,12%.

#### A.3.2.4 Ghép với giai đoạn học ưu tiên và hiệu chỉnh mức từ chối chọn

Ghép hai mô hình theo luật “bước nào mô hình chọn ứng viên từ chối chọn thì lấy câu của MIN-DESC” cho 60,7%, chỉ hơn MIN-DESC 0,67 điểm, nhỏ hơn mức chênh giữa hai hạt giống, và luật ghép được chọn sau khi đã thấy điểm. Ngay cả một quy tắc biết trước ở từng bước mô hình nào đúng cũng chỉ đạt 66,1%.

Trước khi huấn luyện lại, chúng tôi thử hiệu chỉnh mức từ chối chọn sau huấn luyện, vì theo Menon và cộng sự, nếu cách này không cứu được các bước từ chối nhầm thì huấn luyện lại cũng khó làm được. Thủ tục này chọn ứng viên có log-xác suất cao nhất khi điểm ấy hơn điểm của thẻ `none` quá một ngưỡng τ, với ngưỡng và ba biến thể cách xếp hạng được quét trên mẫu phát triển. So với hành vi hiện tại (888 trên 1.400 bước đúng), biến thể tốt nhất chỉ thêm +8 bước (khoảng tin cậy từ -11 đến +27), tức +0,6 điểm.

Khâu xếp hạng ứng viên không sai, vì theo tổng log-xác suất, ứng viên đúng đứng đầu ở 67,5% số bước có ứng viên đúng. Chỗ nghẽn nằm ở quyết định có từ chối chọn hay không. Điểm của thẻ `none` gần như trùng nhau giữa những bước từ chối chọn có và không có ứng viên đúng, với diện tích dưới đường ROC chỉ từ 0,69 đến 0,72, nên mỗi bước được cứu kéo theo gần một bước đúng bị lật thành sai. Nếu quyết định từ chối chọn luôn đúng, mẫu phát triển đạt 78,0%, tức khoảng 14,6 điểm còn thiếu nằm ở quyết định này, và không thể đọc ra quyết định ấy từ xác suất của chính mô hình. Lượt huấn luyện lại vì vậy không được chạy, và hướng chọn ứng viên dừng ở phần phân tích.

## A.4 Giai đoạn thưởng tọa độ

### A.4.1 Thiết kế

**Căn cứ và phần thưởng.** Hai giai đoạn trước chỉ học từ những chuỗi đúng sẵn. Giai đoạn thưởng tọa độ (giai đoạn ba) dùng học tăng cường theo GRPO (Mục 2.3), trong đó mô hình tự sinh nhiều câu trả lời cho một câu nhắc, mỗi câu trả lời nhận một điểm thưởng tính bằng luật, và mô hình được đẩy về phía những câu trả lời trên trung bình của nhóm. Điểm thưởng gồm 1,0 nếu tọa độ trong thẻ `<point>` nằm trong cửa sổ ±14% quanh tọa độ chuẩn, 0,2 nếu sinh đủ và đúng thứ tự các ô của dòng mô tả, và 0,1 nếu tên ghi trong dòng mô tả khớp tên chuẩn. Phần thưởng không gọi mô hình định vị nào, nên độ đo vẫn độc lập với mục tiêu huấn luyện.

**Cấu hình và giới hạn.** Giai đoạn này học tiếp từ điểm lưu của MIN-DESC với cùng lượng tử hoá bốn bit và phần thị giác đóng băng. Mỗi câu nhắc sinh bốn câu trả lời ở nhiệt độ 1,0; mô hình tham chiếu cho số hạng ràng buộc độ lệch là bản sao đóng băng của điểm lưu xuất phát. Tập thưởng gồm 2.000 bước chạm của tập huấn luyện, duyệt một lượt (500 bước cập nhật). Tập này chỉ gồm bước chạm vì chỉ bước chạm có tọa độ chuẩn; ảnh hưởng lên các bước còn lại được đo ở Mục A.2.2.4.

### A.4.2 Kết quả

Trên 4.463 bước chạm, MIN-DESC (hạt giống 101) và mô hình sau giai đoạn thưởng tọa độ đạt 60,05% và 60,07% executability, với khoảng tin cậy lần lượt [58,35; 61,79] và [58,32; 61,83]. Mức chênh ghép cặp là +0,02 điểm (98 bước chỉ mô hình giai đoạn hai đúng, 99 bước chỉ mô hình giai đoạn ba đúng, χ² = 0,00, p = 1, khoảng tin cậy [-0,59; +0,64]), nên không phân biệt được hai mô hình. Khớp loại thao tác (98,88 so với 98,86) và luật hộp phần tử của AndroidControl (66,55 so với 67,04) cũng gần như không đổi. Trước khi chấm, chúng tôi dự báo mức tăng executability bằng cách nhân mức tăng độ chính xác của dòng mô tả với hệ số chuyển đổi 0,43 đo ở giai đoạn hai (số điểm executability tăng thêm ứng với mỗi điểm tăng của dòng mô tả), được +1,10 điểm [+0,59; +1,49]. Mức đo được ứng với hệ số chỉ khoảng 0,01, nên hệ số chuyển đổi không cố định mà phụ thuộc dạng can thiệp.

**Hai chiều tác động triệt tiêu nhau.** Ở 164 bước mà giai đoạn ba sửa dòng mô tả từ sai thành đúng, executability đi từ 32,9 lên 70,7; ở 75 bước mà giai đoạn ba làm dòng mô tả từ đúng thành sai, executability rơi từ 69,3 xuống 29,3. Một bước được coi là đổi kết quả chấm khi bước ấy chuyển từ trượt sang trúng hoặc ngược lại. Đếm số bước đổi kết quả chấm (trượt thành trúng tính +1, trúng thành trượt tính -1), bốn nhóm (sửa đúng, làm sai, giữ nguyên, không có tên đối chiếu) cho +62, -30, -14 và -17, cộng lại chỉ +1. Trong 1.950 bước có dòng mô tả thay đổi, 1.300 bước (66,7%) có câu không đổi một ký tự, và toàn bộ 197 lần đổi kết quả chấm nằm trong 961 bước có câu thay đổi.

**Hệ quả.** Phần thưởng nâng được chính phần trung gian, với +2,56 điểm ở dòng mô tả (p = 1,3 × 10^-8), nhưng không có số hạng nào ràng buộc câu. Khi trọng số dịch chuyển, câu đổi cả ở những bước mà phần thưởng không có tín hiệu, và phần thiệt ở đó xoá phần lợi. Cấu hình đối chứng chỉ huấn luyện thêm có giám sát trên cùng tập thưởng không được chạy vì mức chênh executability gần bằng không, nên 2,56 điểm chưa tách được khỏi phần do việc học thêm đem lại. Phép đo dòng mô tả lại dùng đúng cửa sổ của phần thưởng, nên đại lượng độc lập còn lại chỉ là executability.

### A.4.3 Ghép hai điểm lưu trong không gian trọng số

Giai đoạn ba nối tiếp giai đoạn hai, nên hai bộ trọng số chỉ cách nhau một bước đi ngắn. Phép thử này dựng năm điểm trên đoạn nối hai bộ trọng số (kể cả hai đầu mút), bằng cách ghép các ma trận hạng thấp của hai bộ chuyển đổi LoRA ở từng mô-đun theo tỉ lệ pha trộn, rồi chấm trên tập kiểm định nội bộ. Giả thuyết là một điểm ở giữa có thể giữ phần sửa của giai đoạn ba mà tránh bớt phần làm sai. Đường cong đơn điệu, với cực đại tại đầu mút giai đoạn ba. Điểm giữa tốt nhất thấp hơn đầu mút 0,38 điểm, mọi phép so sánh ghép cặp giữa các mức đều có khoảng tin cậy phủ 0, nên không cấu hình mới nào được đưa lên tập kiểm tra. Số bước có câu khác đầu mút giai đoạn hai tăng đều theo mức pha trộn (53, 95, 127 rồi 155 trên 407 bước), cho thấy phép ghép hoạt động đúng. Dư địa vốn hẹp, vì giai đoạn ba chỉ dịch hai ma trận hạng thấp 1,39% và 6,87% so với giai đoạn hai.

**Mức lạc quan của tập kiểm định nội bộ.** Cả hai điểm lưu đều đã học trên tập này (Mục 3.3). Trên tập ấy, mức chênh giữa hai mô hình lớn gần bốn mươi lần mức chênh trên tập kiểm tra, và điểm tuyệt đối cao hơn khoảng bảy điểm rưỡi, nên tập này chỉ dùng để xếp hạng biến thể trong cùng một họ.

## A.5 Tách khâu nhận ra phần tử và khâu diễn đạt thành câu

Các hướng từ Mục A.1.3 tới đây đều chưa vượt rõ mô hình tinh chỉnh có giám sát (S1) theo executability. Mục này tìm chỗ nghẽn bằng cách tách đường đi từ ảnh tới câu thành hai khâu. Khâu nhận ra phần tử được đo bằng tọa độ mà mô hình tự viết trong dòng mô tả, cho biết mô hình nhìn vào phần tử nào trước khi viết câu. Khâu diễn đạt thành câu được đo bằng điểm mà mô hình định vị trả về sau khi đọc câu, tức đại lượng đi vào executability. Hai khâu dùng chung cửa sổ 14% quanh điểm chạm thật nên so được với nhau. Trên 4.442 bước có dòng mô tả đọc được, MIN-DESC đạt 70,10% ở khâu nhận ra phần tử và 69,36% ở khâu diễn đạt thành câu.

**Bảng A.11.** Executability chia theo việc MIN-DESC có nhận ra đúng phần tử hay không. Cột câu chuẩn là điểm của câu do người chú thích viết, đo trên cùng nhóm bước.

| Nhóm | n | MIN-DESC | S1 | Câu chuẩn |
|---|---:|---:|---:|---:|
| Nhận ra đúng phần tử | 3.114 (70,1%) | 82,37 | 74,18 | 84,36 |
| Nhận ra sai phần tử | 1.328 (29,9%) | 8,43 | 24,47 | 55,72 |

**Khoảng cách dồn vào một phần ba số bước.** Trên toàn tập bước được chấm, câu chuẩn hơn MIN-DESC 15,53 điểm. Nhóm mà mô hình nhận ra đúng phần tử (70,1% số bước) chỉ đóng góp 1,40 điểm, tức 9,0% khoảng cách. Nhóm nhận ra sai (29,9% số bước) đóng góp 14,14 điểm, tức 91,0%.

**Phần thiếu hụt thuộc riêng về mô hình.** Nhóm mà mô hình nhận ra sai phần tử khó hơn kể cả với câu chuẩn. Đi từ nhóm đúng sang nhóm sai, câu chuẩn giảm 28,64 điểm (từ 84,36 xuống 55,72), còn MIN-DESC giảm 73,94 điểm (từ 82,37 xuống 8,43). Hiệu 45,30 điểm là phần thiếu hụt không giải thích được bằng độ khó của nhóm. Khi mô hình đã nhìn sai phần tử, câu sinh ra gần như mất giá trị, còn câu chuẩn vẫn giữ được hơn một nửa số điểm.

**Cải thiện ở khâu nhận ra phần tử chuyển thành rất ít executability.** Trong các can thiệp đã chạy, chỉ giai đoạn thưởng tọa độ đặt phần thưởng thẳng lên tọa độ trong dòng mô tả, nên đây là chỗ đo trực tiếp được phần cải thiện ấy chuyển thành bao nhiêu điểm executability. Trên 4.437 bước ghép cặp được, giai đoạn này nâng tỉ lệ nhận ra đúng phần tử 1,60 điểm nhưng chỉ nâng executability 0,045 điểm, tức mỗi điểm cải thiện ở khâu nhận ra phần tử chỉ đem lại 0,028 điểm executability (tỉ số giữa hai mức tăng).

**Bảng A.12.** Bảng chéo việc nhận ra đúng hay sai phần tử giữa giai đoạn hai (MIN-DESC) và giai đoạn ba, kèm executability của mỗi mô hình trên từng nhóm.

| Nhóm | n | MIN-DESC | Giai đoạn ba | Chênh |
|---|---:|---:|---:|---:|
| giữ đúng | 2.997 | 83,08 | 82,95 | -0,13 |
| giữ sai | 1.143 | 6,91 | 6,30 | -0,61 |
| sai chuyển thành đúng | 184 | 17,93 | 58,15 | +40,22 |
| đúng chuyển thành sai | 113 | 62,83 | 8,85 | -53,98 |

Bảng A.12 cho thấy vì sao con số này nhỏ. Giai đoạn ba sửa được 184 bước với mức lợi 40,22 điểm mỗi bước nhưng làm sai 113 bước với mức thiệt 53,98 điểm mỗi bước, nên hai chiều gần như triệt tiêu.

**Tương quan giữa các mô hình không dùng được làm hệ số quy đổi.** Giữa các mô hình đã huấn luyện, tỉ lệ nhận ra đúng phần tử và executability tương quan ở mức 0,739, nhưng tỉ số đo được khi can thiệp thật chỉ là 0,028, nhỏ hơn 26 lần. Tương quan ấy phản ánh việc mô hình mạnh thường mạnh ở cả hai khâu, và không cho biết điều gì xảy ra khi can thiệp vào riêng một khâu.

**Giới hạn.** Cách chia nhóm là hậu kiểm và dựa trên hành vi của chính mô hình được đo, nên chỉ phép so sánh giữa hai mô hình bên trong một nhóm là hợp lệ. Mẫu số 4.442 nhỏ hơn 4.463 vì 21 bước có dòng mô tả thiếu hoặc sai định dạng.

### A.5.1 Độ tin cậy của ngưỡng tối đa ước lượng trên một nhóm con

Bảng A.11 gợi ra một can thiệp chỉ thay câu. Trên nhóm mà MIN-DESC nhận ra sai phần tử, thay câu của MIN-DESC bằng câu của mô hình tinh chỉnh có giám sát (S1) đưa điểm trên toàn tập bước được chấm lên 65,04 (+4,80 điểm), còn thay bằng câu chuẩn đưa lên 74,40 (+14,14 điểm). Mục này kiểm con số 4,80 và kết luận rằng con số ấy không dùng được. Nhóm được định nghĩa bằng tọa độ do chính MIN-DESC viết ra, mà tọa độ ấy và câu của mô hình này đến từ cùng một lượt sinh nên có chung nhiều yếu tố ngẫu nhiên. Chọn những bước mà MIN-DESC nhận ra sai phần tử là chọn ra những bước lượt sinh ấy gặp bất lợi, nên trên nhóm này MIN-DESC có kết quả thấp hơn một cách hệ thống so với bất kỳ mô hình nào khác.

**Bảng A.13.** Ngưỡng tối đa của một can thiệp chỉ thay câu, dưới bốn cách định nghĩa nhóm (4.437 bước ghép cặp được). Cột cuối là mức tăng trên toàn tập bước được chấm khi thay câu của MIN-DESC (cột MIN) trên nhóm đó bằng câu của S1.

| Cách định nghĩa nhóm | n | MIN | S1 | Câu chuẩn | Trần |
|---|---:|---:|---:|---:|---:|
| MIN-DESC nhận ra sai phần tử | 1.327 | 8,44 | 24,49 | 55,69 | +4,80 |
| giai đoạn ba nhận ra sai phần tử | 1.256 | 11,94 | 22,13 | 54,70 | +2,88 |
| giai đoạn ba sai mà MIN-DESC đúng | 113 | 62,83 | 34,51 | 60,18 | -0,72 |
| 30% màn đông nút nhất | 1.331 | 58,53 | 56,35 | 73,55 | -0,65 |

Bảng A.13 đổi cách định nghĩa nhóm ba lần. Khi nhóm được định nghĩa bằng tọa độ của mô hình sau giai đoạn thưởng tọa độ, tức hành vi của một mô hình khác, ngưỡng tối đa còn 2,88. Khi lấy phần giai đoạn ba sai còn MIN-DESC đúng, ngưỡng tối đa đổi dấu. Khi dùng số phần tử có thể chạm trên màn, không dựa vào hành vi của mô hình nào, ngưỡng tối đa là -0,65. Trong khi đó, cột câu chuẩn gần như đứng yên ở ba hàng đầu (55,69, 54,70 và 60,18) và chỉ cao hơn ở hàng cuối, vốn là nhóm dễ hơn. Ưu thế giữa hai mô hình cùng họ trôi theo cách chia nhóm trong khi khoảng cách tới câu chuẩn đứng yên, và đây là dấu hiệu của hiệu ứng chọn nhóm.

**Hệ quả cho phân tích.** Mọi ngưỡng tối đa ước lượng từ một nhóm định nghĩa bằng hành vi của chính mô hình được đo phải được kiểm lại với ít nhất một cách chia nhóm khác trước khi dùng làm căn cứ. Luật này áp cả cho những con số thuận lợi ở Mục A.2.3, và trong đề tài này đã ngăn một lượt huấn luyện được đề xuất trên căn cứ 4,80 điểm.

## A.6 Đưa thêm thông tin vị trí vào bộ sinh câu

Mục A.5 cho thấy chỗ nghẽn nằm ở khâu nhận ra phần tử. Chúng tôi đã thử bốn cách đưa thêm thông tin vị trí vào mô hình sinh câu, cùng hai phép sàng lọc ý tưởng không cần GPU (Bảng A.14). Phần lớn phép đo chạy trên tập kiểm định nội bộ (Mục 3.3), vốn là dữ liệu mô hình tinh chỉnh có giám sát (S1) đã học, nên mục này chỉ nêu hiệu số giữa các biến thể và các đại lượng cơ chế, không đưa điểm tuyệt đối.

**Bảng A.14.** Bốn cách đưa thông tin vị trí vào mô hình sinh câu và hai phép sàng lọc không cần GPU. Dấu * chỉ phép đo trên tập kiểm định nội bộ.

| Hướng | Cách làm | Kết quả |
|---|---|---|
| Mô-đun định vị và câu nối* | một bộ chú ý học vị trí phần tử trên các mảnh ảnh, rồi cộng đặc trưng vùng đó vào trạng thái ẩn giữa mô hình | bộ chú ý học được vị trí (trùng hộp 52,0% so với 5,3% của tiên nghiệm), nhưng tất cả câu nối chỉ đổi 15% số câu và executability chỉ lệch +0,17 điểm [-1,03; +1,33] |
| Vùng cắt làm ảnh thứ hai* | đo xác suất câu chuẩn khi cho thêm ảnh cắt quanh phần tử đúng, quanh phần tử lân cận cùng loại, hoặc quanh một vùng ngẫu nhiên | tách được vùng đúng khỏi vùng ngẫu nhiên, nhưng gần như không tách được khỏi phần tử lân cận (+0,004 nat mỗi token) |
| Tiêm vai trò, vùng, thao tác* | đọc vai trò, vùng màn và loại thao tác từ trạng thái ẩn, rồi tiêm lại qua một hệ số trộn học được | đọc được (vai trò 51,5%, thao tác 82,8%), nhưng hệ số trộn tự về gần không, chỉ 4% số câu đổi, và hoán vị thông tin giữa các bước không làm điểm giảm |
| Làm nét ảnh quanh phần tử cần chạm* | giữ S1 đóng băng, đưa ảnh được làm nét quanh phần tử cần chạm, quanh chỗ đối diện, hoặc quanh tâm màn | S1 đổi câu ở 16,9% số bước, nhưng làm nét đúng phần tử cần chạm không tốt hơn làm nét chỗ đối diện |
| Hai lượt viết lại có chọn lọc | sàng lọc trên tập kiểm tra: trong 958 câu của S1 chỉ khác câu chuẩn ở một cụm từ, đếm số câu làm mô hình định vị trỏ sai | 147/958 (15,3%), tức phần lớn lỗi sát nghĩa chỉ là khác cách nói, không phải chỉ sai phần tử |
| Bộ xếp hạng câu biết màn sau* | học chọn một trong chín câu do S1 sinh, dùng đặc trưng tính nhanh, có bản học theo một mô hình thấy được xem màn kế tiếp | kém hơn câu giải mã tham lam ở cả BLEU-4, CIDEr-D và SPICE, kể cả bản học theo mô hình thấy màn kế tiếp |

**Kết luận chung của chuỗi phép thử.** Ở cả bốn phép thử, thông tin vị trí học được và đọc được từ mô hình, nhưng câu không đổi theo vị trí được đưa vào. Ở mô-đun định vị và phép tiêm vai trò, vùng, thao tác, hệ số đưa thông tin vào trạng thái ẩn gần như đứng yên (0,119 lên 0,120) hoặc tự giảm (từ 0,50 xuống khoảng 0,03 đến 0,12). Ở hai phép đổi ảnh, mô hình phản ứng với việc ảnh thay đổi nhưng không phân biệt được phần tử cần chạm với phần tử bên cạnh hay chỗ đối diện. Giới hạn chung của cả chuỗi là phần gắn thêm chỉ nhận được tín hiệu học yếu. Phép tiêm và phép làm nét gắn lên mô hình tinh chỉnh có giám sát, vốn đã học cả dữ liệu dùng để huấn luyện và đo chúng; mô-đun định vị thì được thêm vào sau khi phần sinh câu đã học xong một lượt. Điều rút ra chỉ là gắn thêm một đường đưa thông tin vị trí vào bộ sinh câu đã học xong thì không đổi câu; chuỗi này chưa cho thấy thông tin vị trí vô ích cho việc sinh câu. Kết luận này là một căn cứ để thành phần thứ nhất của phương pháp đề xuất (Mục 6.3) tác động thẳng vào câu ở đầu ra.

## A.7 Sửa câu theo vùng cắt quanh phần tử (TAGE)

### A.7.1 Thiết kế

**Căn cứ.** Mục A.5 cho thấy phần lớn khoảng cách tới câu chuẩn nằm ở những bước mô hình nhìn sai phần tử. Bộ sửa câu theo vùng cắt (TAGE, *Type-Aware Grounded Editor*) thử tách việc nhìn khỏi việc viết. Một mô hình chỉ đoán vị trí phần tử, rồi một mô hình khác viết lại câu sau khi xem vùng ảnh quanh vị trí ấy ở dạng phóng to. Bộ sửa câu nhận câu nháp của mô hình học với thưởng SPICE và đứng ở cùng vị trí với ACE (luật chép câu ví dụ khi đồng thuận loại thao tác, Mục 4.6), nên mốc so sánh trực tiếp là chính mô hình học với thưởng SPICE. Vì cho điểm thấp hơn câu nháp trên tập kiểm tra (Mục A.7.2), bộ sửa câu không được giữ trong phương pháp đề xuất.

**Ba thành phần.** TAGE gồm ba thành phần, và Hình A.1 vẽ đường đi của một bước qua cả ba.

1. **Bộ định vị** nhận ảnh và mục tiêu rồi viết ra một điểm (x, y) trên thang 0 đến 1000. Quanh điểm ấy, một ô vuông có cạnh bằng 40% bề ngang màn hình được cắt ra và phóng lên 448 × 448 điểm ảnh.
2. **Bộ biên tập** nhận ảnh gốc, ô cắt và câu nháp rồi viết lại câu. Lúc huấn luyện, ô cắt đặt quanh điểm chạm thật, và hàm mất mát gồm entropy chéo của câu chuẩn cộng một số hạng lề

\[
\mathcal{L}=\mathrm{CE}(g\mid \text{ô đúng})+0{,}5\cdot\max\bigl(0,\,0{,}2-(\mathrm{nll}_{\text{lân cận}}-\mathrm{nll}_{\text{đúng}})\bigr),
\tag{A.1}
\]

trong đó `nll_đúng` và `nll_lân cận` là log-xác suất âm của câu chuẩn khi ô cắt đặt quanh phần tử đúng và quanh một phần tử lân cận cùng vai trò. Số hạng này buộc bộ biên tập dựa vào nội dung ô cắt thay vì chép lại câu nháp. Câu nháp lúc huấn luyện lấy từ mô hình học với thưởng SPICE, và 30% số câu nháp này bị thay tên phần tử bằng tên phần tử lân cận.
3. **Bộ chọn** nhận câu sửa khi Δlp = lp(sửa) − lp(nháp), tức hiệu log-xác suất trung bình theo token do bộ biên tập tính, lớn hơn một hằng số τ; ngược lại giữ câu nháp. Giá trị τ = 0,738 được chọn chéo trên tập kiểm định nội bộ, bằng cách chọn trên một nửa số tác vụ rồi áp lên nửa kia.

Bộ định vị và bộ biên tập là hai bộ chuyển đổi LoRA hạng 16 ở phần ngôn ngữ, gắn trên mô hình tinh chỉnh có giám sát (S1) sau khi đã cộng hẳn trọng số bộ chuyển đổi của S1 vào mô hình gốc. Mỗi bộ học một lượt trên 2.554 bước chạm của tập huấn luyện không chứa tác vụ nào của tập kiểm định nội bộ.

*(Sơ đồ vẽ bằng TikZ, chỉ xem được trong bản PDF.)*

**Hình A.1.** Đường đi của một bước trong bộ sửa câu theo vùng cắt (TAGE). Hai khối tô xám là hai bộ chuyển đổi được huấn luyện. Câu ra khỏi bộ chọn là câu được chấm.

**Cỡ mẫu khi chọn τ.** Trên tập kiểm định nội bộ, bộ chọn chỉ nhận 11 câu sửa trong 249 bước chạm, nên τ được chọn từ một mẫu rất nhỏ. Mục A.7.2 cho thấy đây là điểm yếu lớn nhất của thiết kế.

### A.7.2 Kết quả

Trên tập kiểm định nội bộ, câu sửa tốt hơn câu nháp rõ rệt khi ô cắt đặt quanh điểm chạm đúng và kém đi rõ khi ô cắt cố ý đặt quanh một phần tử lân cận, nên bộ biên tập thật sự dựa vào nội dung vùng cắt. Bộ sửa câu hoàn chỉnh cũng nhỉnh hơn câu nháp trên tập ấy, nên được chấm một lần trên tập kiểm tra.

**Bảng A.15.** Bộ sửa câu theo vùng cắt (TAGE) trên 4.463 bước chạm của tập kiểm tra, so với câu nháp của mô hình học với thưởng SPICE và với S1. Luật hộp phần tử là luật của AndroidControl, luật khoảng cách Euclid là luật của AndroidInTheWild. Ghép cặp theo bước.

| Độ đo | S1 | Câu nháp | TAGE | TAGE - câu nháp | p |
|---|---:|---:|---:|---:|---:|
| Executability | 59,11 | 60,65 | 60,23 | -0,43 [-0,87; +0,02] | 0,093 |
| Luật hộp phần tử | 65,49 | 67,02 | 66,44 | -0,58 [-1,07; -0,09] | 0,027 |
| luật khoảng cách Euclid | 74,37 | 76,25 | 76,07 | -0,18 [-0,66; +0,32] | 0,55 |
| Đúng loại thao tác | 94,35 | 95,97 | 96,64 | +0,67 [+0,44; +0,92] | <0,001 |
| SPICE | 44,37 | 45,79 | 45,74 | -0,05 [-0,38; +0,27] | – |

**Điểm trên tập kiểm tra.** Khâu sửa câu không giúp được trên tập kiểm tra (Bảng A.15). Bộ sửa câu thấp hơn câu nháp 0,43 điểm executability, chưa có ý nghĩa (p = 0,093), và thấp hơn 0,58 điểm theo luật hộp phần tử, có ý nghĩa (p = 0,027). Bộ sửa câu vẫn hơn S1 1,12 điểm [+0,31; +1,94], nhưng toàn bộ phần hơn ấy thuộc về câu nháp. Chỉ tỉ lệ đúng loại thao tác tăng, vì bộ biên tập luôn viết câu chạm, và 30 câu nháp mở đầu bằng vuốt, quay lại hay gõ chữ được đổi thành câu chạm, đúng ở cả 30 bước.

**Nguồn của mức giảm.** Bộ định vị trỏ trúng 69,5% số bước, bộ biên tập đổi câu ở 70,8% số bước, và bộ chọn nhận 219 câu sửa (4,9%). Trên 219 bước ấy, câu nháp chỉ đúng 34,7%, nên bộ chọn có nhắm vào bước câu nháp yếu, nhưng câu sửa còn đúng ít hơn (26,0%). Ở 80 bước có ô cắt đúng chỗ, câu sửa cứu 46 bước và làm sai 7. Ở 139 bước có ô cắt sai chỗ, câu sửa cứu 2 và làm sai 60, vì bộ biên tập mô tả phần tử nằm trong ô cắt và thay một câu nháp vốn đúng bằng câu về phần tử khác (Hình A.2).

**Hình A.2.** Hai bước mà bộ chọn của TAGE nhận câu sửa, cắt phần dưới màn hình. (a) Ô cắt đúng chỗ: câu nháp gọi nút *Always*, câu sửa gọi đúng *Just once*. (b) Ô cắt rơi vào thanh điều hướng ở góc dưới bên trái: câu nháp *Get help* vốn đúng bị thay bằng câu về thẻ *Home* nằm trong ô cắt.

**Tín hiệu của bộ chọn.** Theo Hình A.3, tỉ lệ ô cắt đúng chỗ giảm đều khi Δlp tăng, từ 74,0% ở nhóm thấp nhất xuống 36,5% ở nhóm được nhận. Cách đọc khả dĩ là khi ô cắt rơi vào phần tử khác, bộ biên tập viết một câu rất chắc chắn về phần tử trong ô, còn câu nháp nói về phần tử ngoài ô nên bị chấm log-xác suất thấp. Hiệu Δlp vì vậy đo mức lệch giữa câu nháp và ô cắt, và không cho biết câu nào đúng hơn. Trên tập kiểm định nội bộ, nhóm trên cùng chỉ có 11 câu và tình cờ có 8 ô cắt đúng chỗ, mà τ lại được chọn từ chính 11 câu ấy.

**Hình A.3.** Tỉ lệ ô cắt đúng chỗ (bộ định vị trỏ trong dung sai 14%) theo nhóm Δlp, trên các câu mà bộ biên tập đã đổi ở tập kiểm tra. Cột cam là nhóm được nhận. Bộ chọn càng tự tin nhận câu sửa thì ô cắt càng hay sai.

| Nhóm Δlp | Tỉ lệ ô cắt đúng chỗ | n |
|---|---:|---:|
| ≤ 0 | 74,0% | 1.214 |
| (0; 0,4] | 67,7% | 1.439 |
| (0,4; 0,74] | 45,1% | 288 |
| > 0,74 (cổng nhận) | 36,5% | 219 |

**Hệ quả cho thiết kế.** Bộ chọn dựa trên xác suất của chính bộ biên tập không độc lập với ô cắt, nên không bắt được lỗi nguy hiểm nhất của bộ sửa câu là ô cắt sai. Bộ chọn cần một tín hiệu không đi qua ô cắt, ví dụ so điểm mà mô hình định vị trỏ theo câu nháp với điểm của bộ định vị, và τ cần được chọn trên mẫu lớn hơn nhiều so với 11 câu. Nếu bộ chọn chỉ nhận câu sửa khi ô cắt đúng chỗ, bộ sửa câu được thêm 39 bước, khoảng 0,87 điểm. Đây là ngưỡng tối đa ước lượng bằng điểm chạm đúng của bước, không phải kết quả của một cấu hình đã chạy.
