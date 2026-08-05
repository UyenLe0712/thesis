# report/62 — Giải thích dễ hiểu: đã làm gì, tìm ra gì (bản đầy đủ của report/61)

> Bài này viết cho người không cần đọc thuật ngữ kỹ thuật vẫn hiểu được đã làm gì và kết quả ra sao. Chi tiết/trích dẫn/link nguồn đầy đủ nằm ở `report/61`, bài này chỉ diễn giải lại.

---

## 1. Đã làm gì?

Hôm qua (15/7) đã bắt đầu một vòng "deep-research" — tức là giao cho nhiều AI đi tìm tài liệu khoa học trên mạng để trả lời 6 câu hỏi còn treo về hướng đi của luận văn (train model Qwen2.5-VL-3B để sinh hướng dẫn dùng phần mềm, có lớp lọc-bịa bằng cách đối chiếu View Hierarchy — tức danh sách nút/thành phần thật sự có trên màn hình). Nhưng hôm qua mới dừng ở bước tìm-và-đọc, **chưa kiểm tra xem những gì AI đọc được có đúng không**.

Hôm nay chạy tiếp bước quan trọng nhất: **kiểm tra chéo**. Với mỗi câu khẳng định (gọi là "claim") mà AI trích ra từ một bài báo, có **3 AI khác nhau đóng vai người phản biện**, mỗi người độc lập tìm cách bác bỏ claim đó — đọc lại đúng câu trích có nói đúng vậy không, tìm nguồn khác cãi lại, xem nguồn có đáng tin không, xem có lỗi thời không. Nếu **từ 2/3 người phản biện trở lên nói "bác bỏ"**, claim đó bị loại khỏi báo cáo cuối cùng, dù nghe có vẻ hợp lý đến đâu.

Kết quả: trong 25 claim đưa vào vòng kiểm tra, **20 claim sống sót** (cả 3 phản biện đều đồng ý là đúng), **5 claim bị loại**. Có vài claim ban đầu tưởng là tin tốt (ví dụ "đã có bài chứng minh cách chống hiện tượng model học vẹt") nhưng bị phản biện lật lại vì đọc kỹ thì bài đó không nói đúng như vậy. Đây chính là lý do phải làm bước kiểm tra chéo, không thể tin thẳng những gì AI tìm được lần đầu.

Toàn bộ báo cáo chi tiết (kèm link, trích dẫn nguyên văn) nằm ở `report/61`. Bài này chỉ diễn giải kết quả bằng lời thường.

---

## 2. Tìm ra gì? (6 câu hỏi, trả lời dễ hiểu)

### Câu 1 — Có ai "dạy" model phân biệt câu bịa/câu thật bằng cách so 2 phiên bản (một bịa, một đã lọc sạch) của cùng một câu trả lời chưa?

Ý tưởng ban đầu: mỗi lần lớp lọc phát hiện model bịa ra tên nút không có thật, ta có sẵn 2 phiên bản — bản gốc (bịa) và bản đã viết lại (an toàn). Cho model "học" từ đúng cặp này (kỹ thuật gọi là DPO) coi như được "dữ liệu học miễn phí" vì không tốn công tạo thêm gì.

**Chưa ai làm đúng như vậy trong lĩnh vực giao diện phần mềm (GUI).** Có vài bài gần giống nhưng đều khác một điểm quan trọng: hoặc cặp dữ liệu phải xây riêng công phu (không "miễn phí" như ý tưởng), hoặc dùng kỹ thuật khác (không phải DPO), hoặc nhắm vào việc bấm đúng toạ độ chứ không phải bịa tên nút.

→ Đây là **khoảng trống thật** — nghĩa là nếu làm, sẽ là cái mới. Nhưng cũng vì chưa ai làm, **không có "công thức nấu ăn" nào để tham khảo** — phải tự mò từ đầu, rủi ro thất bại kỹ thuật cao hơn.

### Câu 2 — Nếu cứ mỗi lần model bịa, ta viết đè bằng CÙNG một câu mẫu cố định, model có bị "học vẹt" câu đó không?

Đây là lo ngại: nếu luôn luôn thay câu bịa bằng đúng một câu kiểu "không xác định được, bạn tự kiểm tra trên màn hình", model có thể học thuộc lòng câu này và lặp lại nó ở khắp nơi một cách máy móc, mất đi khả năng diễn đạt tự nhiên.

Tìm được 1 bài (GEM, hội nghị ICLR 2025 — có bình duyệt) xác nhận cơ chế nền: cách huấn luyện thông thường (SFT) đúng là có xu hướng làm model học vẹt câu huấn luyện, mất đa dạng. Nhưng khi kiểm tra kỹ, **bài đó không nói thẳng đây là thuốc chữa cho đúng tình huống "học vẹt vì lặp một mẫu câu"** — claim đó bị phản biện bác. Tương tự, một bài khác (R-Tuning, NAACL 2024, giải Outstanding Paper) nói về việc dạy model "biết từ chối" đúng chỗ, nhưng cũng **không phải bằng chứng trực tiếp** cho đúng tình huống một-câu-mẫu-lặp-lại.

→ Rủi ro này **có cơ sở lo ngại thật**, nhưng **chưa ai đo được** đúng tình huống của luận văn. Nghĩa là luận văn phải tự đo cái này (ví dụ so sánh độ đa dạng câu chữ trước/sau khi train), chứ không trích được con số có sẵn.

### Câu 3 — Có cách đo tốt hơn "tỉ lệ bịa" + "tỉ lệ né tránh" (2 con số tách rời) không?

Ý tưởng: thay vì báo 2 con số rời nhau (model bịa bao nhiêu %, và model né tránh/từ chối bao nhiêu %), có khung đo nào gộp lại thành MỘT đường cong duy nhất không, thể hiện đánh đổi giữa "trả lời nhiều" và "trả lời đúng"?

Có — khung này gọi là "risk-coverage" (đường cong rủi-ro-theo-độ-phủ), đã dùng thật trong vài bài **có bình duyệt** (ví dụ CAP, hội nghị ACML 2025) cho các bài toán gần giống (model biết khi nào nên từ chối trả lời). Về mặt phương pháp, khung này **có cơ sở vững** để áp dụng.

Nhưng: **chưa ai áp dụng đúng khung này cho bài toán sinh-hướng-dẫn-GUI** như luận văn đang làm, và không có bài nào nói thẳng "khung này thay thế được cách báo 2 số rời". Nên đây là một **lựa chọn nâng cấp có căn cứ**, không phải điều bắt buộc phải đổi.

### Câu 4 — Hai cách chống bịa (lọc-dữ-liệu-rồi-train vs. ép-model-bám-sát-lúc-sinh) — có ai so sánh trực tiếp xem cách nào tốt hơn chưa?

**Chưa ai so sánh trực tiếp.** Hai cách này tồn tại như hai nhánh riêng biệt trong tài liệu khoa học, chưa từng được đặt cạnh nhau trên cùng một bài toán để xem cách nào thắng.

→ Đây cũng là khoảng trống — nếu luận văn tự làm phép so sánh nhỏ này, đó là đóng góp thật, và rủi ro thấp vì không phải "đấu" với kết quả ai đã công bố trước.

### Câu 5 — Con số "hơn 77% app thiếu nhãn accessibility" (trích từ một bài năm 2020) có còn đúng bây giờ không? Có ai kết hợp nhiều nguồn (View Hierarchy + đọc chữ trên ảnh + nhận diện icon) để bù chỗ thiếu không?

Có một bài đo lại sau đó (Fok, hội nghị CHI 2022, theo dõi 312 app suốt 16 tháng): tìm ra 55.6% các phần tử dạng hình-ảnh bị thiếu nhãn. Con số này **không đối chiếu thẳng được** với 77% của bài năm 2020 vì đo theo đơn vị khác (bài cũ đếm theo APP có-vấn-đề-hay-không, bài mới đếm theo TỪNG PHẦN TỬ) — nhưng dù đo kiểu nào, kết luận chung vẫn giống nhau: **vấn đề thiếu nhãn là có thật và không tự khỏi theo thời gian**.

Về việc kết hợp nhiều nguồn để bù thiếu: **chưa tìm thấy ai làm đúng việc này** (kết hợp View Hierarchy với công cụ đọc chữ trên ảnh và công cụ nhận diện icon, để tăng độ phủ nhãn cho đúng mục đích luận văn cần).

→ Xác nhận lại: cái mà luận văn định làm (dùng View Hierarchy làm "trọng tài" nhưng biết nó không hoàn hảo) **là một quan sát đúng và chưa ai giải quyết trọn vẹn** — không phải rủi ro luận văn tự bịa ra.

### Câu 6 — Nếu không giới hạn thời gian, hướng nào đáng làm nhất?

Xếp hạng theo mức độ mới + khả năng công bố + độ khả thi (chạy được trên 1 GPU Colab):

1. **Đo bằng đường cong risk-coverage** (câu 3) — mới nhất vì chưa ai dùng View Hierarchy làm "tín hiệu quyết định khi nào nên né tránh" theo đúng kiểu này; khả thi vì có bài khác (ZonUI-3B, hội nghị WACV 2026) đã chứng minh có thể huấn luyện trọn vẹn một model 3 tỷ tham số trên một card đồ hoạ tiêu dùng — đúng tầm Colab.
2. **Tự làm phép so sánh 2 cách chống bịa** (câu 4) — ít "gây ấn tượng" hơn nhưng an toàn, rủi ro thấp, lấp đúng khoảng trống có thật.
3. **Dạy model qua cặp câu bịa/câu đã lọc** (câu 1) — mới nhất về ý tưởng, nhưng rủi ro cao nhất vì không có ai đi trước để dựa vào.

Đây là **suy luận tổng hợp** từ những gì tìm được, không phải một kết luận đã được một bài báo nào khẳng định thẳng — nên độ tin cậy chỉ ở mức "vừa", không phải "cao" như 5 câu trên.

---

## 3. Vậy việc này có làm thay đổi kế hoạch đã chốt không?

**Không tự động thay đổi.** Kế hoạch đã "đóng băng" (pre-register ở report/56 — tức là đã cam kết trước khi chạy thực nghiệm, để tránh bị nghi ngờ chọn kết quả có lợi sau khi nhìn thấy số liệu) vẫn giữ nguyên. Kết quả hôm nay chỉ là **thông tin để tham khảo khi quyết định**, không phải lệnh phải sửa ngay.

Ba lựa chọn (không bắt buộc chọn 1, có thể trộn):

- **Giữ nguyên mọi thứ**, đi tiếp theo kế hoạch cũ (pilot đo sai số → điền vào chỗ trống trong report/56 → chạy thật). An toàn nhất cho deadline 15/8. Coi báo cáo hôm nay là tư liệu để viết phần "công trình liên quan" hoặc để trả lời khi thầy hỏi "có ai làm giống chưa".
- **Cân nhắc đổi cách đo** sang đường-cong-risk-coverage (câu 3+6). Việc đọc thêm để đánh giá không tốn tiền (không cần gọi API hay chạy GPU), nhưng nếu quyết định đổi thật thì có thể ảnh hưởng tới lịch và phải tính lại vài công thức thống kê đã chốt.
- **Chưa quyết**, để dành hỏi ý thầy hướng dẫn trước — vì đây là quyết định ảnh hưởng hướng cả luận văn, không nên tự quyết một mình.

Không có lựa chọn nào là "sai" — tuỳ mức độ chấp nhận rủi ro và thời gian còn lại tới 15/8.
