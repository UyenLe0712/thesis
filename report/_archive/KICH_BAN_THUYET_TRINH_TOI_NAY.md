# KỊCH BẢN THUYẾT TRÌNH TỐI NAY — bám 18 slide, cho người chưa biết gì

> **File này dùng để làm gì?** Là "phao" nói trơn theo từng slide. Mạch deck (18 slide): **Đề tài → DỮ LIỆU (3 bộ, mỗi bộ có ví dụ thật) → Pipeline → Cách chấm → Khả thi**. Mục tiêu tối nay: **thuyết phục thầy DUYỆT phần dữ liệu trước**, rồi mới tới pipeline & cách chấm.
>
> File slide: `LUAN_VAN_SLIDE.pptx`. Bản giải thích đầy đủ từ số 0: `report/GIAI_THICH_TOAN_BO_DE_HIEU.md`.

---

## 0. NÓI TRONG 20 GIÂY (học thuộc)

> "Em làm hệ thống dùng AI **nhìn ảnh màn hình + đọc câu hỏi** rồi **tự viết hướng dẫn bấm từng bước**. Người dùng đưa **một ảnh**, hoặc **nhiều ảnh của một quy trình bị xáo trộn** — khi đó máy **tự sắp lại đúng thứ tự** rồi mới viết. Vì **không có sẵn bản hướng dẫn mẫu để chấm điểm**, nên **đóng góp chính của em là một CÁCH ĐÁNH GIÁ đáng tin khi không có đáp án mẫu**."

---

## 1. THÔNG ĐIỆP LẶP LẠI XUYÊN BUỔI
1. **Đóng góp chính = PHƯƠNG PHÁP ĐÁNH GIÁ** (không phải "làm một app").
2. **Hai nhánh:** một ảnh (chấm bám-đúng/không-bịa/rõ) · nhiều ảnh (sắp đúng thứ tự).
3. **Trung thực:** thước đo có nguồn bình duyệt; chỗ nào chưa chắc thì nói thẳng + có cách kiểm.

---

## 2. NÓI THEO TỪNG SLIDE (18 slide)

### • Slide 1 — Tiêu đề
> "Đề tài: sinh tự động hướng dẫn sử dụng phần mềm từ ảnh màn hình + câu hỏi, và cách đánh giá khi không có bản mẫu. Em trình theo mạch: đề tài → dữ liệu → pipeline → cách chấm → khả thi."

### • Slide 2 — Đề tài (vào / ra)
> "Người dùng đưa **1 ảnh + 1 câu hỏi** ('vào đâu để kiểm tra đã nộp thuế?'). Máy trả về **hướng dẫn bấm từng bước**, đánh số, bám đúng ảnh. Máy này là VLM — loại AI vừa nhìn ảnh vừa đọc/viết chữ."

### • Slide 3 — Vì sao là nghiên cứu (cái khó)
> "Cái khó: muốn chấm điểm máy cần **đáp án mẫu** do người soạn, nhưng không ai soạn sẵn hướng dẫn chuẩn cho mọi app. **Nên đóng góp chính của em là cách đánh giá khi không có đáp án mẫu.** Hệ có 2 chế độ: **một ảnh**, và **nhiều ảnh bị xáo trộn** (máy tự sắp lại — mọi ảnh đều thấy, không đoán màn nào)."

### • Slide 4 — Ba dataset + vai trò  ⟵ BẮT ĐẦU PHẦN XIN DUYỆT DỮ LIỆU
> "Em dùng **3 bộ dữ liệu đã công bố**. **MobileViews** cho nhánh một-ảnh. **AndroidControl** cho nhánh nhiều-ảnh (vì nó có sẵn **thứ tự đúng**). **ScreenSpot** để đối chứng. Ba slide sau em xin cho thầy xem **ví dụ thật** trích thẳng từ từng bộ."

### • Slide 5 — MobileViews: giới thiệu
> "MobileViews ~**600.000 màn Android**. Mỗi màn kèm **view-hierarchy** = bảng liệt kê mọi nút + **vị trí chính xác**. Nhờ có vị trí thật, em chấm được 'máy chỉ đúng nút không' và 'có bịa nút không' mà không cần bản mẫu."
> **Nói thẳng lưu ý:** "Bộ này là **preprint** (chưa bình duyệt) nên em chỉ dùng làm **nguồn ảnh/nhãn**, không làm xương sống phương pháp; metric của nó **đổi theo phiên bản** nên em sẽ ghi rõ bản; và em sẽ **kiểm mẫu** vì có cảnh báo lỗi dữ liệu."

### • Slide 6 — MobileViews: VÍ DỤ THẬT (2 item)
> "Đây là **2 màn thật** trích từ MobileViews: 'Add time' (đặt giờ) và 'New task' (tạo việc). **Ô đỏ** là vị trí thật của một nút (nút 'OK' và nút 'SAVE & ADD ANOTHER'), lấy từ view-hierarchy của chính màn đó. Nhờ có vị trí thật: máy bấm **trúng trong ô = ĐÚNG** (grounding); máy **nhắc nút không có trên màn = BỊA** (hallucination). **Ảnh và toạ độ là thật, em không vẽ.**"

### • Slide 7 — AndroidControl: giới thiệu
> "AndroidControl: **15.283 quy trình** thật trên 833 app, trung bình ~5,5 bước. Mỗi quy trình có **gold trajectory** = chuỗi thao tác đúng từng bước → tức **có sẵn thứ tự đúng**. Em xáo trộn các màn rồi bắt máy xếp lại, so với thứ tự đúng để chấm."
> **Lưu ý:** "Bộ này **đã bình duyệt (NeurIPS 2024)** — điểm mạnh. Toạ độ là điểm bấm nên em tự đổi sang khung; số quy trình theo từng độ dài chưa công bố nên **em tự đếm** (đó là kill-test KN)."

### • Slide 8 — AndroidControl: VÍ DỤ THẬT (1 episode)
> "Một episode thật, mã #11506, **mục tiêu: mở Clock và đặt báo thức 6:10 sáng**. Đây là **3 màn thật** + **thao tác vàng** từng bước (bấm toạ độ này, toạ độ kia). Cách dùng: em đảo lộn 3 màn → bắt máy xếp lại → so với thứ tự đúng → chấm bằng Kendall τ-b. Ngoài ra dùng nguyên thứ tự đúng làm mốc tham chiếu (Tier A)."

### • Slide 9 — ScreenSpot: giới thiệu
> "ScreenSpot ~**1.272 mẫu** trên điện thoại/máy tính/web. Mỗi mẫu: 1 ảnh + 1 yêu cầu ngắn + **vị trí đúng** của nút. Em dùng nó làm **thước chuẩn đã bình duyệt** để kiểm bộ chấm vị trí của em, và bù độ tin cho MobileViews."
> **Lưu ý:** "Bộ này **chỉ đơn-bước** → chỉ đối chứng vị trí, không thay nhánh nhiều ảnh."

### • Slide 10 — ScreenSpot: VÍ DỤ THẬT (3 item)
> "Ba màn iOS thật: yêu cầu 'invert the lens', 'start a timer', 'add an event'. Banner đen là **yêu cầu thật của item**, ô đỏ là **vị trí đúng**. Em chạy trên cả bộ để báo 'bộ chấm vị trí của em chính xác X%' — làm bằng chứng độ tin."

### • Slide 11 — Chốt phần dữ liệu  ⟵ XIN THẦY DUYỆT DATASET
> "Tóm lại: **MobileViews** lo nhánh một-ảnh, **AndroidControl** lo nhánh nhiều-ảnh (có thứ tự đúng), **ScreenSpot** làm bằng chứng độ tin. **Em xin thầy duyệt 3 bộ này.** Tiếng Việt em làm demo định tính vì chưa có bộ chuẩn tiếng Việt."
> *(Dừng ở đây để thầy hỏi/duyệt dữ liệu trước khi sang pipeline.)*

### • Slide 12 — Pipeline (4 bước)
> "Cỗ máy sinh hướng dẫn: **(1) dò nút trên ảnh & đánh số → (2) vẽ số lên ảnh → (3) bắt máy chỉ được nhắc số đã dò (chống bịa) → (4) bộ kiểm tra lại**. Em **không huấn luyện model mới** — dùng công cụ có sẵn, vì đóng góp là *cách đánh giá*, cỗ máy chỉ là phương tiện."

### • Slide 13 — Pipeline nhiều ảnh: 5 manh mối
> "Với nhiều ảnh, máy hỏi từng cặp 'màn nào trước' rồi tổng hợp. Máy dựa vào đâu? Em đặt tên **5 manh mối**: cổng chặn (đăng nhập trước), nút điều hướng, thay đổi trạng thái (ô trống→đã điền), tiêu đề tiến triển, đi sâu chi tiết. Em còn **đo riêng** manh mối nào thực sự giúp."

### • Slide 14 — Cách chấm 1 ảnh (3 tiêu chí)
> "Một ảnh chấm 3 thứ: **bám đúng nút** (điểm bấm trong ô nút thật), **không bịa** (không nhắc nút không có), **viết rõ** (đánh số, có động từ). Ba thứ này ánh xạ từ khung đánh giá trong **bài báo tham khảo** (Chim, Ive, Liakata — Computational Linguistics 2025)."

### • Slide 15 — Cách chấm nhiều ảnh (Kendall τ-b)
> "Đo độ đúng thứ tự bằng **Kendall τ-b**: xét từng cặp màn, đúng chiều thì +, sai thì −. Quan trọng: **chỉ phạt cặp BẮT BUỘC** (đăng nhập trước → xem kết quả); cặp **tự do** (điền email/số điện thoại trước cũng được) đảo vẫn đúng. 'Bắt buộc' suy từ thứ tự đúng có sẵn, không để máy tự quyết → tránh tự chấm."

### • Slide 16 — Nguồn thước đo
> "Mọi thước đo đều có **nguồn đã bình duyệt** (ACL/EMNLP/NAACL/NeurIPS/tạp chí CL). Công cụ kỹ thuật là preprint thì em chỉ coi là 'đồ nghề', không trình như đã bình duyệt. Mỗi số em báo kèm 'độ phủ bộ dò = X%'."

### • Slide 17 — Khả thi & trung thực
> "**Khả thi:** KHÔNG huấn luyện model lớn, chỉ cần 1 GPU + ~100–300 đô (dùng model rẻ, chạy theo lô). **Tuần 1** chạy kill-test: tự đo độ phủ bộ dò (K1) + đếm độ dài quy trình (KN) rồi báo thầy. **'Null vẫn đậu':** em đăng ký trước giả thuyết → dù hệ không thắng, kết quả null được giải thích cơ chế VẪN là đóng góp (vì đóng góp là CÁCH ĐÁNH GIÁ, không phải thắng-thua)."
> *(Nếu thầy hỏi về thang bậc thí nghiệm: bản gọn chạy 3 mức C1 baseline → C3 ràng buộc → C4 kiểm-ý để biết 'món nào trả công'.)*

### • Slide 18 — Kết
> "Ba thứ xin thầy duyệt: (1) **dữ liệu** 3 bộ (đã có ví dụ thật); (2) **phương pháp đánh giá** hai nhánh; (3) **khả thi** + null-vẫn-đậu. Tuần 1 em chạy kill-test rồi báo thầy chốt. Em cảm ơn thầy."

---

## 3. ⭐ CÂU HỎI THẦY CÓ THỂ HỎI + CÁCH TRẢ LỜI

> Nguyên tắc: **thừa nhận điểm yếu trước, rồi xoay về điểm mạnh (đánh giá)**.

**Q1. "Kỹ thuật chỉ là đánh số rồi prompt, mỏng quá?"**
> "Phần SINH em cố ý dùng công cụ có sẵn — nó chỉ là khung để vận hành đánh giá. **Chiều sâu nằm ở PHƯƠNG PHÁP ĐÁNH GIÁ**: chấm không cần đáp án mẫu, chấm thứ tự partial-order chống lý-luận-vòng-tròn, truy nguồn tín hiệu, thiết kế thực nghiệm chặt. Đây là luận văn về *đánh giá*, cùng thể loại với bài báo nền (Chim et al., CL 2025)."

**Q2. "Đưa sẵn các màn rồi xếp — có phải bài toán dễ?"**
> "Scope này thầy đã duyệt: cho sẵn màn, máy sắp thứ tự. Em **không khẳng định** giải bài 'đoán màn chưa thấy' — bài đó em để future-work. Việc 'máy dựa vào đâu trên màn để biết thứ tự' vẫn cần hiểu giao diện thật, nên vẫn có giá trị."

**Q3. "Sao chỉ tới 6 ảnh?"**
> "Vì chi phí hỏi-từng-cặp tăng theo số ảnh; ở 6 ảnh là 15 lần hỏi/quy trình, vừa ngân sách và đủ mẫu. Em báo thêm tới ~8–10 nếu ngân sách cho."

**Q4. "Độ phủ bộ dò nút chưa biết thì sao?"**
> "Đây là rủi ro lớn nhất, em nói thẳng. Nên **việc đầu tiên tuần 1 là TỰ ĐO** (cổng go/no-go), và mọi số grounding em đóng khung kèm 'độ phủ = X%'."

**Q5. "Thầy ưu tiên tiếng Việt mà số liệu lại tiếng Anh?"**
> "Cách chấm không phụ thuộc ngôn ngữ (chấm bằng vị trí/định dạng). Số liệu chạy trên dữ liệu chuẩn (Anh/Trung); tiếng Việt em làm demo định tính trên app Việt thật, nói rõ giới hạn."

**Q6. "Sao không tự train model cho mạnh?"**
> "Em có thể thêm fine-tune một model rồi so với bản có sẵn (một đóng góp 'huấn luyện'), nhưng không cần cho đóng góp chính (đánh giá). Em để tùy chọn nếu thầy muốn chiều sâu ML."

**Q7. "Chấm thứ tự bằng Kendall — em tự chế à?"**
> "Dùng Kendall τ chấm thứ tự là chuẩn ngành (Lapata 2006, tạp chí CL). Xếp ảnh xáo cũng có tiền lệ (Sort-Story 2016, Wu 2022). Cái mới của em ở **miền giao diện + cách đánh giá**; em thừa nhận phần đã có tiền lệ."

**Q8. "Dataset này có thật hợp với bài không?"**
> "Em vừa cho thầy xem ví dụ thật từ từng bộ: MobileViews có vị trí nút để chấm grounding; AndroidControl có thứ tự đúng để chấm sắp xếp; ScreenSpot đã bình duyệt để đối chứng. Mỗi bộ đúng một vai, không thừa."

---

## 4. TỪ ĐIỂN BỎ TÚI
| Từ | Nói cho dễ |
|---|---|
| **VLM** | AI nhìn ảnh + đọc/viết chữ |
| **Grounding (point-in-bbox)** | Điểm máy bấm có nằm trong ô của nút thật không |
| **Hallucination** | Máy bịa nút không có |
| **View-hierarchy** | Bảng liệt kê nút + vị trí thật trên màn |
| **Gold trajectory** | Chuỗi thao tác đúng có sẵn (= thứ tự đúng) |
| **Kendall τ-b** | Điểm đo 2 thứ tự giống nhau bao nhiêu (−1..+1) |
| **Cặp bắt buộc / tự do** | Bắt buộc = đảo là sai; tự do = đảo vẫn đúng |
| **Peer-reviewed / preprint** | Đã bình duyệt (tin) / chưa (chỉ dùng làm công cụ) |
| **Pre-registration / null vẫn đậu** | Đăng ký trước → kết quả "không khác biệt" vẫn có giá trị |

---

## 5. CHECKLIST TRƯỚC KHI TRÌNH
- [ ] Thuộc đoạn 20 giây + câu "đóng góp chính = phương pháp đánh giá".
- [ ] Nhớ mạch: **Đề tài → 3 Dataset (xin duyệt) → Pipeline → Cách chấm → Khả thi**.
- [ ] Tới slide 11: **dừng lại mời thầy duyệt dữ liệu** trước khi sang pipeline.
- [ ] Thủ sẵn Q1 (kỹ thuật mỏng), Q2 (bài toán dễ), Q4 (độ phủ bộ dò).
- [ ] Câu chốt: "Tuần 1 chạy kill-test rồi báo thầy chốt."

---

## 6. NẾU CHỈ CÓ 3 PHÚT
(1) Bài toán = ảnh + câu hỏi → hướng dẫn; (2) khó = không có đáp án mẫu; (3) **3 dataset đã có ví dụ thật, đủ làm 2 nhánh**; (4) đóng góp = cách đánh giá (1 ảnh: bám đúng/không bịa/rõ; nhiều ảnh: Kendall τ-b, chỉ phạt cặp bắt buộc); (5) khả thi + trung thực.
