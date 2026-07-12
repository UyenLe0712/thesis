# 📖 Giải thích đề tài cho người chưa biết gì (đọc từ từ là hiểu hết)

> Viết như kể cho một người bạn KHÔNG rành công nghệ. Mỗi từ khó đều được giải thích bằng ví dụ đời thường.
> Có một ví dụ chạy xuyên suốt để bạn bám theo. Phần cuối là câu trả lời cho giám khảo khó tính.
> Cập nhật 2026-07-03.

---

## PHẦN 1 — Câu chuyện: đề tài này giải quyết chuyện gì?

Tưởng tượng bạn mở một ứng dụng lạ trên điện thoại và **không biết phải bấm vào đâu**. Bạn chụp lại màn hình, gửi cho một "trợ lý thông minh" và hỏi:

> *"Làm sao để đặt giờ báo thức 8 giờ 35 tối rồi lưu lại?"*

Trợ lý nhìn ảnh, rồi viết cho bạn:

> 1. Chọn giờ "8", phút "35"
> 2. Chọn buổi "PM" (buổi tối)
> 3. Bấm nút "OK"

**Luận văn này làm ra cái "trợ lý" đó** — một chương trình đọc ảnh màn hình + câu hỏi rồi tự viết hướng dẫn từng bước. **Và quan trọng hơn: làm ra cách KIỂM TRA xem trợ lý nói đúng hay nói bậy.**

### "Trợ lý thông minh" ở đây là gì?
Là một loại **AI vừa nhìn được ảnh, vừa viết được chữ** (giới chuyên môn gọi là *VLM* — "mô hình ngôn ngữ thị giác"). Bạn cứ hình dung nó như một người rất giỏi mô tả: đưa ảnh vào, nó "nhìn" và "kể" lại bằng lời. ChatGPT có tính năng xem ảnh — đó chính là loại AI này.

---

## PHẦN 2 — Ba cái khó (vì sao đây là bài toán nghiên cứu, không phải chuyện dễ)

### Cái khó 1: AI hay "bịa"
Giống như một người kể chuyện cho có, AI đôi khi viết ra bước kiểu *"Bấm nút Cài đặt"* — **trong khi màn hình chẳng hề có nút Cài đặt nào**. Người dùng làm theo, tìm hoài không thấy → hướng dẫn thành vô dụng, thậm chí gây bực.
> Giới chuyên môn gọi hiện tượng bịa này là *"ảo giác"* (hallucination) — AI "tưởng tượng" ra thứ không có.

### Cái khó 2: không có "đáp án mẫu" để chấm
Muốn biết một học sinh làm bài đúng hay sai, thầy cô cần **đáp án**. Nhưng ở đây, **không ai soạn sẵn "bản hướng dẫn chuẩn" cho mọi ứng dụng trên đời**. Vậy làm sao biết AI viết đúng? Lấy gì mà so? Đây là cái khó lớn nhất, và cũng là chỗ đóng góp chính của luận văn.

### Cái khó 3: nhiều màn thì thứ tự nào trước?
Nhiều việc phải làm qua **nhiều màn hình liên tiếp** (mở app → chọn mục → điền thông tin → bấm lưu). Nếu ta đưa cho AI một xấp ảnh **bị xáo trộn lung tung**, nó phải **tự đoán màn nào làm trước, màn nào làm sau**. Nó dựa vào đâu để đoán? Và làm sao ta biết nó đoán đúng?

---

## PHẦN 3 — Ý tưởng cứu cánh: "bảng kê nút thật"

Ở cái khó số 2 (không có đáp án), có một cứu cánh.

Điện thoại Android **luôn giữ sẵn một "bảng kê"** liệt kê mọi nút đang có trên màn hình: nút tên gì, nằm ở đâu. (Bảng kê này vốn dùng cho người khiếm thị — để máy đọc tên nút thành tiếng.)
> Giới chuyên môn gọi bảng kê này là *View Hierarchy* (viết tắt **VH**). Bạn cứ nhớ: **VH = danh sách nút thật của màn hình.**

**Đây chính là "mỏ neo" thay cho đáp án mẫu.** Ta không có bản hướng dẫn chuẩn, nhưng ta **biết chắc màn hình có những nút gì**. Nên mỗi khi AI nhắc tới một nút, ta **tra bảng kê**: nút đó có thật không? Nếu không có → AI đang bịa.

### Một luật cực kỳ quan trọng (giám khảo hay hỏi)
Ta **KHÔNG đưa bảng kê nút cho AI lúc nó đang viết hướng dẫn.** Chỉ dùng bảng kê **lúc đi chấm**.
> *Ví von:* giống như **không cho học sinh xem đáp án trong lúc làm bài** — nếu cho xem, nó chép lại thì đâu còn đo được nó tự nghĩ đúng bao nhiêu. Ta muốn đo xem AI **tự** bịa bao nhiêu, nên phải giấu bảng kê lúc nó làm.

---

## PHẦN 4 — Hệ thống chạy thế nào? (dùng đúng ví dụ màn báo thức)

Hãy lấy màn hình đặt giờ ở đầu bài. Trên màn đó có **5 nút thật**: `giờ (hour)`, `phút (minute)`, `PM`, `OK`, `Cancel`.

### Với MỘT màn hình — làm qua 3 bước:

**Bước 1 — AI viết "mù".**
AI chỉ được nhìn **ảnh + câu hỏi**, KHÔNG được xem bảng kê nút. Nó tự viết bản nháp. Ví dụ nó viết:
> 1. Chọn giờ và phút
> 2. Chọn "PM"
> 3. Bấm **"Menu"**   ← chỗ này AI bịa, vì màn này làm gì có nút Menu

**Bước 2 — Máy đối chiếu với bảng kê nút thật.**
Đây **không phải AI**, chỉ là một phép so sánh máy móc: lấy từng tên nút AI viết, dò trong bảng kê:
- "giờ và phút" → khớp với `hour`, `minute` ✅ có thật
- "PM" → khớp `PM` ✅ có thật
- **"Menu" → dò khắp bảng kê không thấy nút nào giống → AI đang BỊA** ❌

**Bước 3 — Sửa lại bước bịa cho an toàn.**
Bước bị bịa được **thay bằng một câu mô tả chung chung**, và **tuyệt đối không đoán bừa sang nút khác**:
> `Bấm "Menu"` → viết lại thành → `Tìm và bấm nút phù hợp để mở thêm tuỳ chọn`

Kết quả: hướng dẫn không còn dẫn người ta tới "nút ma", mà những bước đúng thì giữ nguyên.

> **Vì sao chỉ "mô tả chung" mà không "đoán đại một nút thật nào đó gần gần"?**
> Vì tụi tôi **đã thử** cách "đoán nút gần nhất" và thấy nó **gây hại ngầm**: AI đổi "Submit" (Gửi) thành "Save" (Lưu) trong khi đáp án đúng là một nút khác hẳn → người dùng bấm nhầm mà **không hề biết mình đang sai**. Vì có bằng chứng tai hại đó, tụi tôi chốt cách an toàn "chỉ mô tả". Đây là một **phát hiện qua thực nghiệm**, không phải quyết định tùy hứng.

### Với NHIỀU màn hình — thêm một bước "sắp thứ tự" ở đầu:

Khi có nhiều ảnh bị xáo trộn, trước khi viết hướng dẫn, phải xếp lại đúng thứ tự. Cách làm giống một **giải đấu vòng tròn**:

1. **Đấu từng cặp:** đưa 2 màn một, hỏi AI *"màn nào làm trước?"*.
2. **Đếm số trận thắng:** màn nào thắng nhiều cặp hơn thì xếp trước.
   > *Ví dụ 3 màn A, B, C:* A thắng B, A thắng C, B thắng C → A thắng 2 trận, B thắng 1, C thắng 0 → thứ tự là **A → B → C**.
3. **Gỡ rối nếu mâu thuẫn:** thỉnh thoảng AI trả lời lộn xộn tạo vòng luẩn quẩn (A trước B, B trước C, mà C lại trước A). Khi đó ta bỏ đi ít phán đoán "kém chắc chắn" nhất để phá vòng.
4. Có thứ tự đúng rồi → chạy y như phần một-màn cho từng màn.

> AI dựa vào đâu để đoán thứ tự? Vào **các dấu hiệu trên màn**: màn đăng nhập thì phải trước; nút "Tiếp theo/Quay lại"; ô lúc đầu trống sau đã điền; tiêu đề kiểu "Bước 2/4"; màn sau là chi tiết của mục màn trước.

---

## PHẦN 5 — Chấm điểm thế nào? (kèm ví dụ số cho dễ hình dung)

### Với một màn:
- **Độ trung thực (không bịa) — thước đo QUAN TRỌNG NHẤT.**
  Cách tính: lấy 1 trừ đi tỉ lệ bước bị bịa.
  > *Ví dụ:* 3 bước có nhắc tên nút, 1 bước bịa → độ trung thực = 1 − 1/3 = **67%**.
  >
  > 📌 Con số tụi tôi **báo cáo** là *"AI bịa khoảng một phần tư (¼) số bước ngay từ bản nháp đầu"* — tức đo xem **AI tự bịa bao nhiêu**, chứ không khoe con số ~100% sau khi đã sửa (sửa xong thì đương nhiên hết bịa, có gì mà khoe).
  > ⚠️ Con số này còn **"tùy điều kiện"**: đôi khi bảng kê nút bị thiếu (nút chỉ có hình, không có chữ), khiến máy tưởng AI bịa trong khi thật ra nút có tồn tại. Nên tụi tôi **đo luôn tỉ lệ nút có tên trong bảng kê** rồi báo con số bịa kèm điều kiện đó — không nói chắc nịch "đúng ¼".

- **Độ gọi đúng tên nút.**
  > *Ví dụ:* AI viết "Đồng ý" trong khi nút thật tên "OK" → nút CÓ thật, chỉ là gọi lệch tên → tính là "sai tên" (khác với "bịa").

- **Độ bấm đúng chỗ.** *(Thước đo này tụi tôi để dành cho phần nhiều-màn, đã bỏ khỏi phần một-màn — lý do kỹ thuật ở phần cuối.)*

### Với nhiều màn:
- **Xếp đúng thứ tự chưa?** So thứ tự AI xếp với đáp án đúng, chỉ trừ điểm ở những cặp **bắt buộc** phải đúng thứ tự.
  > *Ví dụ:* đáp án đúng là A→B→C, AI xếp A→C→B → sai 1 cặp. Còn những việc **làm trước sau đều được** (như điền email rồi số điện thoại) thì đảo cũng không bị trừ.
- **Làm theo có TỚI ĐÍCH không? (Step-SR)** So từng thao tác AI đề xuất với thao tác đúng chuẩn. Đây là bằng chứng *"làm theo hướng dẫn này có thật sự xong việc không"* — điều mà phần một-màn không đo được.

---

## PHẦN 6 — Làm sao tin được mấy con số đó? (đây là chỗ ăn điểm với hội đồng)

- **Không để "vừa ra đề vừa chấm".**
  Nếu dùng cùng một công cụ để vừa QUYẾT "bước nào bịa" vừa CHẤM "còn bịa không" → kết quả đương nhiên đẹp (giống thầy tự ra đề rồi tự chấm). Nên tụi tôi dùng **công cụ khác nhau** cho hai việc, cộng thêm một "trọng tài" thứ ba. Và con số công bố là *tỉ lệ bịa của bản nháp gốc*, không phải con số 100% sau khi sửa.

- **Cố tình bỏ lỗi vào để thử "cái cân".**
  Muốn tin một cái cân, ta đặt lên đó một quả cân 1kg đã biết trước, xem nó có báo đúng 1kg không. Tương tự, tụi tôi **cố tình chèn lỗi đã biết** vào một hướng dẫn đúng (ví dụ nhét thêm một nút bịa rõ ràng) rồi xem thước đo có tụt điểm đúng như phải tụt không. Nếu không tụt → thước đo hỏng.

- **Thống kê cẩn thận.**
  Vì nhiều màn của cùng một app rất giống nhau (không "độc lập"), tụi tôi tính sai số **theo từng ứng dụng**, và **ghi ra ngưỡng đánh giá TRƯỚC khi nhìn kết quả** để khỏi bị nghi "chỉnh số cho đẹp".

> Mỗi cách làm ở trên đều **dựa trên một bài báo khoa học đã được bình duyệt** (đã kiểm tên hội nghị, năm). Không có chỗ nào tụi tôi "tự nghĩ ra rồi nói bừa".

---

## PHẦN 7 — Dữ liệu lấy từ đâu? (3 bộ có sẵn, công khai)

| Bộ dữ liệu | Nói nôm na là gì | Trong đó có gì | Dùng để |
|---|---|---|---|
| **MobileViews** | Kho ảnh màn hình app Android + bảng kê nút, cực lớn | Ảnh 1 màn + danh sách nút thật của màn đó | Phần **một màn** |
| **AndroidControl** | Kho các "quy trình nhiều bước" đã có lời giải đúng | Chuỗi nhiều màn + **thao tác đúng từng bước** (đáp án vàng) | Phần **nhiều màn** |
| **ScreenSpot** | Bộ chuẩn để kiểm "chỉ đúng vị trí nút" | Ảnh + vị trí nút chuẩn | Đối chứng |

*Vì sao chọn 3 bộ này:* MobileViews có bảng-kê-nút (làm mỏ neo); AndroidControl có **đáp án vàng** (chấm được "tới đích"); ScreenSpot là bộ đã bình duyệt để bù độ tin cậy.

---

## PHẦN 8 — Rốt cuộc luận văn đóng góp gì?

**Hai thứ, đặt ngang vai nhau:**
1. **Một hệ thống viết hướng dẫn ít bịa hơn** (lớp kiểm-tra-và-sửa + phần sắp thứ tự màn).
2. **Một cách đánh giá không cần đáp án mẫu, không tự chấm.**

> **Lưu ý trung thực:** hai đóng góp ngang nhau **có điều kiện** — với điều kiện phần nhiều-màn cho ra con số tốt thật. Nếu chưa có con số đó, đóng góp số 1 vẫn đứng vững nhờ: (a) xây được hệ đảm bảo không dẫn tới nút ma; (b) đo được tỉ lệ bịa gốc; (c) có bằng chứng thất bại của phương án "đoán bừa". **Tụi tôi không tuyên bố chắc nịch "ngang nhau" khi chưa có số** — thà khai thẳng.

---

## PHẦN 9 — Tự nhận giới hạn (khai trước, khỏi bị bắt)

- Phần một-màn mới đo được *"không bịa"*, chưa đo được *"làm có tới đích không"* → cái đó để phần nhiều-màn.
- Kết quả hiện mới là **sơ bộ** (chạy trên 1 loại AI, số mẫu nhỏ) → sẽ chạy đầy đủ hơn.
- Bảng kê nút đôi khi thiếu → tụi tôi đo và khai rõ điều kiện đó.
- Chưa có bảng số cho tiếng Việt (vì bộ dữ liệu chuẩn là tiếng Anh/Trung) → tiếng Việt làm minh hoạ.

---

## PHẦN 10 — Nếu giám khảo hỏi khó, trả lời sao? (thủ sẵn)

| Câu hỏi khó | Trả lời gọn |
|---|---|
| **"Kết quả đâu? Sao dám nói hai đóng góp ngang nhau?"** | Ngang nhau **có điều kiện**. Phần một-màn đã có số sơ bộ; phần nhiều-màn đang chạy. Nếu chưa có số, đóng góp 1 vẫn đứng nhờ hệ chạy được + bằng chứng thất bại đo được. |
| **"Sao không đưa bảng kê nút cho AI để nó viết đúng luôn?"** | Vì cần đo AI **tự** bịa bao nhiêu. Đưa bảng kê thì nó chép, hết đo được. (Lúc dùng thật có thể đưa; lúc nghiên cứu cố ý giấu.) |
| **"Bảng kê nút thiếu thì chấm oan AI à?"** | Đã lường: tụi tôi đo tỉ lệ nút có tên trong bảng kê, loại các nút không tên ra, và báo con số kèm điều kiện. |
| **"Chỉ ghép mấy công cụ có sẵn, đóng góp ở đâu?"** | Đóng góp nằm ở **phát hiện qua thí nghiệm** (đo được AI bịa bao nhiêu, chứng minh phương án đoán-bừa gây hại) và ở **cách đánh giá mới**, không phải ở độ phức tạp lập trình. Nhiều công trình nổi tiếng cũng gọn như vậy. |
| **⭐ "AI bạn dùng đời cũ rồi; AI mới 2026 giỏi hơn, đâu còn bịa — vậy hệ của bạn thừa?"** | Tụi tôi báo tỉ lệ bịa **theo nhiều đời AI, kể cả một AI mới nhất 2025-2026** — và cho thấy **AI mới VẪN bịa** (chưa hết hẳn). Ngoài ra, khi chạy ngay trên điện thoại thì chỉ dùng được AI nhỏ (không gọi được AI mạnh), nên lớp kiểm-tra vẫn luôn cần. |
| **"Sao không có số tiếng Việt?"** | Bộ dữ liệu chuẩn là tiếng Anh/Trung (vì có sẵn bảng kê nút + đáp án). Tiếng Việt làm minh hoạ + một ít mẫu app Việt cho chuyên gia xem. |

---

## PHẦN 11 — Tóm một câu để nhớ
> Tụi tôi làm một trợ lý **viết hướng dẫn dùng app từ ảnh màn hình**, và một cách **kiểm tra nó nói thật hay bịa** dù không có đáp án mẫu — bằng cách neo vào "bảng kê nút thật" mà điện thoại có sẵn, chỉ dùng lúc chấm chứ không mách cho AI lúc làm.

> *Muốn đào sâu hơn:* `report/41` (bản A–Z có ví dụ) · `report/42` (kiểm tra độ mới 2026) · `report/40` (phản biện giám khảo). Bản chi tiết-kỹ-thuật ở `report/05`, `report/36`.
