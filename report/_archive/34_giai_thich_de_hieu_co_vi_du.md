# 📘 PIPELINE & CÁCH CHẤM ĐIỂM — GIẢI THÍCH QUA MỘT VÍ DỤ CỤ THỂ

> File này giải thích **mọi thứ qua một ví dụ chạy thật từ đầu đến cuối**, cho người chưa biết gì. Đọc xong là hiểu: pipeline chạy ra cái gì, và mỗi thước đo ra con số thế nào.

---

## 0. Trong một phút: bài này làm gì?

Người dùng mở một app lạ và hỏi một câu, ví dụ *"làm sao thêm một khoản chi mới?"*. Mình đưa cho AI **ảnh chụp màn hình đó + câu hỏi**, và AI **tự viết ra hướng dẫn từng bước** kiểu "1. Bấm nút này, 2. Nhập ô kia...".

Vấn đề: AI hay **bịa nút không có thật** trên màn, làm người dùng bấm hụt. Mà mình lại **không có sẵn bản hướng dẫn mẫu** để so xem AI viết đúng hay sai. Nên mình phải nghĩ ra **cách tự chấm** mà không cần bản mẫu. Toàn bộ phần dưới giải thích cách làm đó, **qua một màn hình cụ thể**.

---

## 1. NGUYÊN LIỆU: một màn hình thật

Giả sử màn hình app ghi chi tiêu trông như sau. Android cho mình biết **chính xác trên màn có những nút gì** — bản kê khai này gọi là **View Hierarchy** (cây phân cấp giao diện). Với màn này, danh sách nút thật là:

```
Add expense   |   Amount   |   Category   |   Save   |   Settings   |   Back
```

Đây là điểm mấu chốt: **mình luôn biết sự thật trên màn có nút gì** (vì Android cấp sẵn). Mình sẽ lấy danh sách này làm "đáp án" để chấm — nhưng **chỉ lấy ra lúc CHẤM, tuyệt đối không đưa cho AI lúc nó đang viết**. (Nếu đưa thì AI cứ chép y theo, "không bịa" thành hiển nhiên, chấm vô nghĩa.)

**Câu hỏi người dùng:** *"Làm sao thêm một khoản chi mới?"*

---

## 2. PIPELINE CHẠY THẾ NÀO — đi từng bước trên ví dụ này

### Bước 1 — AI viết hướng dẫn (bản "thô", gọi là BASE)

Mình đưa AI **ảnh + câu hỏi** (KHÔNG đưa danh sách nút). AI nhìn ảnh rồi viết ra, ví dụ nó viết thế này:

| Bước | AI viết | |
|---|---|---|
| 1 | Bấm **Add expense** | |
| 2 | Nhập số tiền vào ô **Amount** | |
| 3 | Bấm **Submit** | |
| 4 | Bấm **Save changes** | |

Nhìn qua thì hợp lý. Nhưng để ý hai chỗ: màn **không hề có** nút tên "Submit", và cũng **không có** nút tên đúng "Save changes" — nút thật chỉ là "Save".

### Bước 2 — Đối chiếu từng bước với danh sách nút thật

Bây giờ mình lấy danh sách nút thật ra, **soi từng bước** xem nút AI nhắc tới **có thật không**. Cách soi: với mỗi tên AI viết, tìm nút **gần nghĩa nhất** trong danh sách thật, đo độ giống.

- Bước 1 "Add expense" → trùng y một nút thật → **CÓ THẬT**.
- Bước 2 "Amount" → trùng y → **CÓ THẬT**.
- Bước 3 "Submit" → nút gần nhất trong danh sách là "Save", nhưng "Submit" và "Save" **khác nghĩa đủ xa** (độ giống thấp) → **BỊA** (màn không có nút này).
- Bước 4 "Save changes" → nút gần nhất là "Save", và "Save changes" **rất gần nghĩa** với "Save" (độ giống cao) → **CÓ THẬT** (chỉ là AI gọi hơi khác tên).

> **Vì sao phải so theo NGHĨA, không so chữ cứng?** Nếu so chữ cứng, bước 4 "Save changes" ≠ "Save" → sẽ bị tính **bịa OAN**, dù nút có thật. Nên mình dùng kỹ thuật **so theo nghĩa** (biến chữ thành vector rồi đo độ gần — gọi là embedding) để khỏi vu oan các cách gọi đồng nghĩa. *(Cách này theo bài ALOHa, hội nghị NAACL 2024.)*

### Bước 3 — Lớp hậu kiểm: xử lý bước bịa

Đây là **đóng góp về phần SINH** của mình. Bước nào bị chấm là **bịa** thì thay vì để nguyên cái tên ma, mình **viết lại thành mô tả bằng lời**:

- Bước 3 "Bấm **Submit**" (nút ma) → viết lại thành: *"Tìm và bấm nút để **lưu khoản chi vừa nhập**"*.

Tức là: thay vì bắt người dùng đi tìm một nút "Submit" không tồn tại, mình **mô tả việc cần làm** để họ tự nhận ra nút đúng. Ba bước kia (có thật) thì **giữ nguyên**.

> Lưu ý quan trọng: lớp này **không sửa "Submit" thành một nút thật cụ thể** (kiểu đổi đại thành "Save"). Vì lỡ đoán sai thì còn nguy hơn (bảo người ta bấm nhầm nút). Nó chỉ **mô tả chung** — an toàn. **Cái giá** là bước đó kém cụ thể hơn.

### Bước 4 — Chấm điểm (xem mục 3).

---

## 3. CÁCH CHẤM ĐIỂM (METRIC) — chấm trên đúng ví dụ trên

Mình có vài thước đo, mỗi cái ra một con số. Chấm cho **cả bản BASE (AI viết tự do)** lẫn **bản sau lớp hậu kiểm**, rồi so.

### Thước đo 1 — TRUNG THỰC (không bịa) ⭐ quan trọng nhất
**Hỏi:** trong các bước, bao nhiêu bước trỏ tới nút **không tồn tại**?
**Công thức:** `Trung thực = 1 − (số bước bịa) / (tổng số bước)`.

Trên bản BASE: chỉ bước 3 ("Submit") là bịa → 1 bịa / 4 bước.
→ **Trung thực BASE = 1 − 1/4 = 75%.**

### Thước đo 2 — ĐÚNG-NHÃN (gọi đúng tên hiển thị)
**Hỏi:** với các bước trỏ nút có thật, AI có gọi **đúng y cái tên** hiện trên màn không? (Gọi sai tên thì người dùng khó tìm, dù nút có thật.)

- Bước 1 "Add expense" = đúng y → ✓
- Bước 2 "Amount" = đúng y → ✓
- Bước 4 "Save changes" ≠ tên thật "Save" → **gọi sai tên** → ✗

→ Trong 3 bước trỏ nút thật, đúng tên 2/3 ≈ **67%.**

> **Đây là chỗ tinh tế đáng khoe với thầy:** bước 4 **không bịa** (nút Save có thật) **nhưng gọi sai tên** → mình **trừ điểm Đúng-nhãn, KHÔNG tính bịa**. Hai loại lỗi khác nhau, đo riêng. Còn bước 3 thì **bịa hẳn** (không có nút). Tách bạch như vậy giúp con số phản ánh đúng bản chất.

### Thước đo 3 — ĐÚNG-CHỖ (bấm trúng khung nút)
Nếu AI có kèm toạ độ điểm bấm, mình kiểm điểm đó có **rơi trong khung của nút** không (Android cho biết khung mỗi nút). Trúng thì tốt. *(Theo SeeClick, ACL 2024.)* — *(Ở DG1 phần lớn AI gọi nút theo tên chứ ít cho toạ độ, nên thước đo này dùng nhiều ở phần đa-bước có đáp án vàng.)*

### Thước đo 4 — ĐỊNH DẠNG
Có đánh số 1,2,3 không? Mỗi bước có mở đầu bằng động từ ("Bấm", "Nhập") không? — kiểm tự động.

### Và sau lớp hậu kiểm thì sao?
Bản sau hậu kiểm: bước 3 "Submit" đã thành mô tả-bằng-lời → **không còn nhắc nút ma** → trung thực **tăng**. **Cái giá:** bước 3 giờ chung chung → mình báo luôn **"tỉ lệ fallback" = 1/4 = 25%** (một phần tư số bước phải mô tả chung). Mình **không giấu cái giá này**.

---

## 4. ⭐ CHỐNG "ĂN GIAN" — vì sao con số đáng tin?

Đây là chỗ một thầy khó tính sẽ soi đầu tiên, nên mình nói thẳng.

**Cái bẫy:** nếu mình dùng **cùng một công cụ** để vừa **quyết** "bước này bịa, đem mô tả lại" vừa **chấm** "còn bịa không", thì sau khi hậu kiểm điểm trung thực **đương nhiên 100%** — vì mình đã loại sạch cái mà chính công cụ đó chê. Đó là **trò chơi chữ**, không phải kết quả.

**Cách mình chống:** dùng **hai công cụ khác nhau**.
- Việc **quyết** "đem bước nào đi mô tả lại" → dùng công cụ A (embedding `nomic`).
- Việc **chấm điểm** → dùng công cụ B **khác hẳn** (`bge-m3`) **cộng thêm một bộ chấm bằng LLM thuộc họ khác** với AI viết hướng dẫn.

Và quan trọng nhất: **con số mình đem khoe KHÔNG phải là 100% sau hậu kiểm** (mình nói thẳng cái đó là "trần do thiết kế"). Con số thật mình báo là **tỉ lệ bịa của bản gốc = 25%** trong ví dụ — tức *đo độ lớn của vấn đề* mà AI mắc, chấm bằng công cụ độc lập.

> Nói với thầy một câu: *"Em không khoe điểm 100%. Em khoe rằng AI viết tự do thì bịa khoảng một phần tư số bước, và lớp của em phát hiện & xử lý được chúng — và em chấm bằng công cụ khác với công cụ đã quyết, nên không phải đẳng thức."*

---

## 5. KIỂM TRA CHÍNH THƯỚC ĐO — "perturbation" (qua ví dụ)

Làm sao tin thước đo của mình **đo đúng**? Mình **tự bơm lỗi đã biết** vào một hướng dẫn đúng rồi xem thước đo có bắt được không.

Lấy một hướng dẫn **đúng hết**: "1. Bấm Add expense, 2. Nhập Amount, 3. Bấm **Save**".
- **Bơm lỗi loại 1:** đổi "Save" → "Confirm" (nút ma). → Thước đo Trung thực **phải tụt** (bắt được bịa). Nếu nó vẫn báo 100% thì thước đo **hỏng**.
- **Bơm lỗi loại 2:** đổi "Save" → "Lưu" (đồng nghĩa, nút vẫn có thật). → Trung thực **phải GIỮ NGUYÊN** (vì nút có thật), nhưng Đúng-nhãn **phải tụt** (gọi sai tên). → kiểm tra thước đo **tách đúng hai loại lỗi**.

Vì lỗi do mình tạo nên **đáp án đúng đã biết trước** → mình đo được thước đo **nhạy tới đâu, có vu oan không**, hoàn toàn tự động, không cần ai chấm tay. *(Cách này có tiền lệ: Sai et al., EMNLP 2021.)*

---

## 6. KHI CÓ NHIỀU MÀN (DG2) — ví dụ sắp thứ tự

Phần trên là một màn. Khi việc cần làm trải qua **nhiều màn**, mình đưa AI **các ảnh đã bị xáo trộn** và bắt nó **tự suy ra thứ tự đúng** rồi mới hướng dẫn. Đây là chỗ trả lời câu hỏi của thầy: *"làm sao AI biết màn nào trước?"* — và mình **đo** được nó làm tốt cỡ nào, vì ở đây mình **có đáp án vàng** (bộ dữ liệu AndroidControl, đã bình duyệt NeurIPS 2024).

**Ví dụ:** luồng "đăng nhập rồi xem hồ sơ".
- Màn A = màn **Đăng nhập** (ô email, mật khẩu, nút Login).
- Màn B = màn **Hồ sơ** (chỉ hiện ra **sau khi** đã đăng nhập).

Đáp án vàng cho biết: A phải trước B. Và vì màn B **chỉ xuất hiện sau khi bấm Login ở A**, mình **suy ra bằng quy tắc nhân-quả**: cặp (A trước B) là **cặp BẮT BUỘC**.

Bây giờ đưa AI **2 ảnh xáo trộn**: [Hồ sơ, Đăng nhập]. AI phải xếp lại.
- Nếu AI xếp **Đăng nhập → Hồ sơ** (A→B) → **đúng** cặp bắt buộc.
- Nếu AI xếp **Hồ sơ → Đăng nhập** → **sai** cặp bắt buộc.

**Cách chấm thứ tự — hệ số Kendall tau-b:** một con số từ −1 đến +1, đo thứ tự AI xếp giống đáp án tới đâu (+1 = trùng khít, 0 = như đoán bừa). Nhưng mình **chỉ trừ điểm khi sai cặp BẮT BUỘC**. Cặp **tự do** thì đảo vẫn đúng — ví dụ trên một màn đăng ký có ô "Email" và ô "Số điện thoại", điền cái nào trước cũng được, nên nếu AI đảo thì **không bị phạt**. → mình **không phạt oan**. *(Theo Kendall 1938, Lapata CL 2006, và Fagin cho thứ-tự-bộ-phận.)*

> **Chống "tự ra đề tự chấm":** cái nhãn "cặp nào là bắt buộc" mình **suy từ đáp án vàng** (theo quy tắc nhân-quả ở trên), **KHÔNG** lấy từ chính AI → nên thước đo độc lập với cái đang chấm. Mình còn cho **người kiểm 50–80 cặp** xác nhận quy tắc khớp với cảm nhận người.

**Và quan trọng — "Step-SR" (làm-theo-tới-đích):** vì có đáp án vàng từng bước, mình kiểm: **làm theo hướng dẫn AI sinh ra thì có tới đích không?** Mỗi bước, so thao tác AI bảo làm với **thao tác vàng** (đúng loại bấm/gõ + bấm đúng chỗ trong dung sai 14%). Đếm số bước đúng / tổng = Step-SR. **Đây là bằng chứng "đúng-ý" thật sự** — cái mà phần một-màn (DG1) không đo được. Đây cũng là phần khoa-học nặng nhất của luận văn.

---

## 7. TÓM LẠI — vì sao cách này vững

1. Mình **luôn biết sự thật trên màn** (danh sách nút Android cấp) → chấm "có bịa không" mà **không cần bản mẫu của người**.
2. Mình **tách công cụ quyết và công cụ chấm** → con số không phải trò-chơi-chữ; và mình **khoe tỉ lệ bịa thật, không khoe điểm 100%**.
3. Mình **tự kiểm thước đo** bằng cách bơm lỗi đã biết (perturbation), không cần chấm tay.
4. Khi nhiều màn, mình đo **năng lực sắp thứ tự** (Kendall tau-b, chỉ phạt cặp bắt buộc, nhãn suy từ đáp án vàng) và đo **làm-theo-tới-đích (Step-SR)** trên dataset có đáp án vàng.
5. Mình **tự nêu mọi giới hạn**: DG1 chỉ đo "không bịa" chứ chưa đo "đúng-ý" (đúng-ý để DG2); danh sách nút là ảnh chụp một-trạng-thái nên nút sau-khi-cuộn mình lọc riêng; điểm 100% là trần do thiết kế.

> **Một câu chốt:** *"Em không có bản mẫu của người, nên em neo vào sự-thật-rẻ-mà-có-sẵn là danh sách nút Android cấp. Từ đó em đo được AI bịa bao nhiêu (DG1) và sắp thứ tự / làm-tới-đích đúng cỡ nào (DG2). Mọi con số em đều tách công cụ để khỏi tự-chấm, tự kiểm thước đo bằng bơm-lỗi, và tự nêu giới hạn — nên em tin nó đứng vững trước phản biện."*
