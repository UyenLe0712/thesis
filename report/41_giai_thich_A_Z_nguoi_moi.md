# 📘 Giải thích đề tài từ A–Z cho người mới bắt đầu (kèm ví dụ cụ thể)

> Đọc file này là hiểu TOÀN BỘ đề tài dù chưa biết gì về AI. Mỗi ý đều có ví dụ.
> Thuật ngữ nội bộ: **một màn = DG1**, **nhiều màn = DG2** (khi trình bày nói "một màn/nhiều màn").
> Cập nhật 2026-07-02 (đã bám phán quyết debate mới nhất — xem `report/40`).

---

## 0. Một câu tóm tắt

> Ta làm một **hệ thống** đọc **ảnh chụp màn hình phần mềm** + **câu hỏi của người dùng**, rồi **tự viết ra bản hướng dẫn bấm từng bước**; và ta làm một **cách chấm điểm** bản hướng dẫn đó **khi không có đáp án mẫu của con người**.

Hai thứ đó — **hệ sinh hướng dẫn** và **cách đánh giá** — là hai đóng góp của luận văn.

---

## 1. Bài toán: vào gì, ra gì?

**Đầu vào:**
- Một (hoặc nhiều) **ảnh chụp màn hình** của một app.
- Một **câu hỏi** bằng lời thường, ví dụ: *"Làm sao đặt giờ 8:35 tối rồi xác nhận?"*

**Đầu ra:** bản hướng dẫn **đánh số từng bước** cho người đọc làm theo.

### 🎬 Ví dụ xuyên suốt (nhớ kỹ ví dụ này — cả file dùng nó)
Ảnh là một **hộp thoại đặt giờ** có các nút: `giờ (hour)`, `phút (minute)`, `PM`, `OK`, `Cancel`.
Câu hỏi: *"Cần thao tác gì để đặt giờ 20:35 và xác nhận?"*
Đầu ra mong muốn:
```
1. Chọn giờ "8", phút "35"
2. Chọn buổi "PM"
3. Chọn "OK"
```

Đơn giản với con người. Nhưng để **máy tự viết** ra đúng như vậy, và để **biết máy viết đúng hay sai**, thì khó — đó là chỗ nghiên cứu.

---

## 2. Vì sao khó? (3 thách thức)

**① Máy hay "bịa" nút (ảo giác).**
Các AI nhìn-ảnh (gọi là **VLM** — mô hình ngôn ngữ thị giác) thường viết ra bước kiểu *"Bấm nút Settings"* trong khi **màn hình không hề có nút Settings**. Người dùng tìm hoài không thấy → hướng dẫn vô dụng.
> *Ví dụ:* với ảnh đặt giờ ở trên, máy có thể viết *"Bấm Menu"* — nhưng màn chỉ có hour/minute/PM/OK/Cancel, **không có Menu**. Đó là "bịa".

**② Không có "đáp án mẫu" để chấm.**
Muốn biết máy viết đúng không, thường phải có bản hướng dẫn chuẩn do người soạn sẵn để so. Nhưng **không ai soạn sẵn hướng dẫn cho mọi app**. Vậy lấy gì để chấm? Đây là cái khó trung tâm.

**③ Nhiều màn: thứ tự nào trước?**
Một tác vụ thật thường trải **nhiều màn** (mở app → chọn mục → điền → lưu). Nếu đưa **nhiều ảnh bị xáo trộn**, máy phải **tự đoán màn nào trước màn nào sau**. Dựa vào đâu để đoán? Và làm sao ta biết máy đoán đúng?

---

## 3. Dữ liệu: ta lấy ảnh + thông tin ở đâu?

Ta dùng **3 bộ dữ liệu công khai** (không tự chụp):

| Bộ | Có gì | Dùng để |
|---|---|---|
| **MobileViews** | ảnh 1 màn + **danh sách nút thật** của màn đó (kèm vị trí) | nhánh **một màn** |
| **AndroidControl** | chuỗi **nhiều màn** của 1 tác vụ + **thao tác đúng từng bước** (gọi là *quỹ đạo vàng*) | nhánh **nhiều màn** |
| **ScreenSpot-v2** | ảnh + toạ độ nút chuẩn | đối chứng cho phép đo "bấm đúng chỗ" |

### 🔑 Hai khái niệm quan trọng
- **Danh sách nút thật (View Hierarchy — viết tắt VH):** là "bảng kê" các nút có trên màn, do hệ điều hành Android cung cấp. *Ví dụ với màn đặt giờ, VH = {hour, minute, PM, OK, Cancel}.* Đây là **"mỏ neo"** ta dùng thay cho đáp án mẫu: không có hướng dẫn chuẩn, nhưng ta **biết màn có nút gì**, nên kiểm được máy có bịa nút không.
- **Quỹ đạo vàng (gold trajectory):** chuỗi **thao tác đúng chuẩn** do người làm thật rồi ghi lại, có sẵn trong AndroidControl. *Ví dụ: (màn 1) chạm "+", (màn 2) gõ "Grocery", (màn 3) chạm "Lưu".* Đây là **đáp án** để chấm nhánh nhiều màn.

> ⚠️ **LUẬT VÀNG (rất quan trọng):** VH và quỹ đạo vàng **CHỈ được dùng lúc CHẤM ĐIỂM**, **tuyệt đối không đưa cho máy lúc nó đang viết hướng dẫn**. Vì nếu đưa danh sách nút cho máy, nó "chép" → không còn đo được nó tự bịa bao nhiêu. (Giống như không cho học sinh xem đáp án lúc làm bài.)

---

## 4. Hệ thống chạy thế nào? (pipeline)

Ta có **một hệ duy nhất**. Nếu đầu vào 1 ảnh → chạy nhánh **một màn**. Nếu nhiều ảnh → thêm **một bước sắp thứ tự** ở đầu rồi mới chạy như một màn.

### 4A. Nhánh MỘT MÀN — 3 hộp

**Hộp 1 — Máy viết "mù".** Máy (VLM) chỉ thấy **ảnh + câu hỏi**, KHÔNG thấy danh sách nút. Nó tự viết bản nháp.
> *Ví dụ máy viết:*
> ```
> 1. Chọn giờ và phút
> 2. Chọn "PM"
> 3. Bấm "Menu"     ← chỗ này máy bịa
> ```

**Hộp 2 — Thuật toán đối chiếu.** Một **thuật toán** (không phải AI, chỉ là phép so khớp) so từng tên nút máy viết với danh sách nút thật (VH):
- "giờ/phút" → khớp `hour/minute` ✅
- "PM" → khớp `PM` ✅
- "Menu" → **không có nút nào giống** → đây là **bịa** ❌

**Hộp 3 — Viết lại bước bịa thành mô tả.** Bước bịa được **thay bằng một câu mô tả chung**, **KHÔNG đoán bừa nút khác**:
> `Bấm "Menu"` → `Tìm và bấm nút phù hợp để mở thêm tuỳ chọn`

Kết quả: hướng dẫn không còn "nút ma", các bước đúng giữ nguyên.

> **Vì sao "chỉ mô tả" mà không "đoán nút thật gần nhất"?** Ta đã THỬ phương án "đoán nút gần nhất" và thấy nó gây **lỗi ngầm**: máy thay "Submit" thành "Save" trong khi đáp án đúng là nút khác → người dùng bấm nhầm mà không biết. Vì có bằng chứng thất bại đo được này, ta **chốt** cách an toàn "chỉ mô tả". Đây là một **phát hiện thực nghiệm**, không phải chọn bừa.

### 4B. Nhánh NHIỀU MÀN — thêm bước sắp thứ tự ("Stage-0")

Khi có nhiều ảnh **xáo trộn**, trước khi viết hướng dẫn, máy phải **sắp lại thứ tự đúng**:

1. **Hỏi từng cặp:** đưa 2 màn một, hỏi máy *"màn nào trước?"*.
2. **Đếm điểm (Copeland):** màn nào "thắng" nhiều cặp hơn thì đứng trước.
   > *Ví dụ 3 màn A, B, C:* A thắng B, A thắng C, B thắng C → A thắng 2, B thắng 1, C thắng 0 → thứ tự **A < B < C**.
3. **Phá vòng mâu thuẫn:** nếu máy trả lời lộn xộn tạo vòng (A>B>C>A), ta gỡ bằng một thuật toán chuẩn (bỏ ít cặp nhất để hết vòng).
4. Có thứ tự rồi → chạy nhánh một màn cho từng màn.

> **5 "manh mối" (cue) máy dựa vào để đoán thứ tự** (trả lời câu hỏi thầy "dựa vào đâu"): (1) *gating* — màn đăng nhập phải trước; (2) *nút điều hướng* Next/Back; (3) *thay đổi trạng thái* — ô trống→đã điền; (4) *tiêu đề tiến trình* — "Bước 2/4"; (5) *đi sâu* — màn sau là chi tiết của mục màn trước.

---

## 5. Chấm điểm thế nào? (metrics) — kèm ví dụ số

### 5A. Nhánh một màn

**① Độ trung thực (không bịa)** = thước đo CHÍNH.
Công thức: `1 − (số bước nhắc nút KHÔNG tồn tại) / (số bước có nhắc tên nút)`.
> *Ví dụ:* 3 bước có nhắc nút, 1 bước bịa ("Menu") → độ trung thực = 1 − 1/3 = **67%**.
>
> 📌 **Con số ta báo là "tỉ lệ bịa của BẢN NHÁP GỐC" (~¼ số bước)** — tức máy tự bịa bao nhiêu TRƯỚC khi sửa. KHÔNG khoe con số ~100% sau khi sửa (vì sau khi sửa thì đương nhiên hết bịa — không có gì để khoe).
>
> ⚠️ **Đang làm cho trung thực hơn:** danh sách nút VH đôi khi **thiếu nút** (nút chỉ có icon, không nhãn chữ). Nếu nút thật mà thiếu trong VH, thuật toán sẽ tưởng máy "bịa" → oan. Nên ta sẽ **đo tỉ lệ nút có nhãn trong VH** rồi báo con số bịa dạng "có điều kiện" (không nói chắc ¼).

**② Độ đúng nhãn** = gọi đúng TÊN hiển thị của nút.
> *Ví dụ:* máy viết "Đồng ý" trong khi nút thật tên "OK" → nút CÓ thật nhưng gọi sai tên → tính là sai-nhãn (khác với "bịa").

**③ Độ đúng chỗ (grounding)** = điểm bấm có rơi trúng khung nút không.
> ⚠️ **Lưu ý mới (theo debate):** thước đo này ta **để dành cho nhánh nhiều màn** (nơi có sẵn toạ độ chuẩn), **không tính vào nhánh một màn**. Lý do: nếu lấy tâm khung nút đã khớp làm điểm bấm thì luôn "trúng" = vô nghĩa (100% giả). Muốn đo thật phải có một "bộ trỏ độc lập" đoán toạ độ từ tên+ảnh — cái này là hướng mở rộng.

### 5B. Nhánh nhiều màn

**① Độ đúng thứ tự (τ).** So thứ tự máy sắp với quỹ đạo vàng, **chỉ phạt những cặp BẮT BUỘC** phải đúng thứ tự.
> *Ví dụ:* vàng là A<B<C, máy sắp A,C,B → 2 cặp đúng, 1 cặp sai → τ = +0.33.
> Cặp **tự do** (ví dụ điền email rồi điền số điện thoại — trước sau đều được) thì đảo vẫn tính đúng.

**② Độ hoàn thành tác vụ (Step-SR).** So thao tác máy đề xuất với thao tác vàng từng bước: đúng loại thao tác + bấm lệch không quá 14% màn hình thì tính đúng.
> Đây là bằng chứng **"làm theo có tới đích không"** — thứ nhánh một màn không đo được.

---

## 6. Vì sao tin được các con số? (chống gian lận vô tình)

**① Chống "tự ra đề tự chấm" (vòng lặp luận lý).**
Nếu cùng một công cụ vừa QUYẾT "bước nào bịa" vừa CHẤM "còn bịa không" → luôn ra 100% (trò chơi chữ). Ta tránh bằng cách: **công cụ quyết** và **công cụ chấm** là **hai loại khác nhau**, cộng thêm một bộ thẩm định khác nữa. Và con số công bố là **tỉ lệ bịa của bản gốc**, không phải 100% sau sửa.

**② Tự kiểm thước đo bằng "bơm lỗi" (perturbation).**
Ta cố tình bỏ lỗi đã biết vào một hướng dẫn đúng rồi xem thước đo có bắt được không.
> *Ví dụ:* chèn một nút bịa rõ ràng → độ trung thực PHẢI tụt. Nếu không tụt → thước đo hỏng.

**③ Thống kê chặt.**
Vì nhiều màn cùng một app rất giống nhau (không độc lập), ta tính sai số **theo cụm ứng dụng**, báo khoảng tin cậy, và **đăng ký ngưỡng TRƯỚC khi nhìn kết quả** (chống chỉnh số cho đẹp).

> Mỗi nguyên tắc trên đều dựa một **bài báo đã bình duyệt** (ALOHa, Sai, Chen, Clark, Panickssery, Fagin, Qin, Copeland/Dwork...). Không có chỗ nào ta "tự nghĩ ra rồi nói bừa".

---

## 7. Hai đóng góp của luận văn

- **(A) Hệ thống sinh hướng dẫn ít bịa** = lớp đối chiếu + viết-lại + khối sắp thứ tự màn. Cắm được vào bất kỳ AI nào.
- **(B) Cách đánh giá không cần đáp án mẫu, không tự chấm** = bộ thước đo + cơ chế chống-vòng-lặp + tự-kiểm-bằng-bơm-lỗi.

> **"Ngang nhau" nhưng CÓ ĐIỀU KIỆN:** hai đóng góp được đặt ngang vai, với điều kiện nhánh nhiều màn (Step-SR) cho kết quả dương thật. Nếu nhánh đó chưa có số, ta khai thẳng: đóng góp A vẫn đứng vững nhờ (1) đạt mục tiêu thiết kế, (2) đo được tỉ lệ bịa + % phải mô tả chung, (3) bằng chứng thất bại đo được (đoán-nút → lỗi ngầm). **Không tuyên bố "ngang nhau" vô điều kiện khi chưa có số.**

---

## 8. Giới hạn (khai thẳng, không giấu)

1. Nhánh một màn chỉ đo **không-bịa**, chưa đo **đúng-ý** → đúng-ý đo ở nhánh nhiều màn.
2. Con số ~100% sau sửa là **trần do thiết kế** → ta báo tỉ lệ bịa của bản gốc.
3. Danh sách nút VH có thể **thiếu nút** → ta đo độ-phủ-nhãn và đóng khung "có điều kiện".
4. Máy **không có GPU** → phải dùng AI qua mạng (API), nên hiện chỉ chạy 1 model, mẫu nhỏ.
5. Chưa có **bảng số tiếng Việt** (dữ liệu chuẩn là tiếng Anh/Trung) → tiếng Việt làm minh hoạ định tính.

---

## 9. Đang ở đâu, làm gì tiếp?

- **Đã xong:** thiết kế + nền lý thuyết (mọi thành phần đều có bài báo bình duyệt) + kết quả **sơ bộ** (bịa ~¼, mô-tả-lại ~19% số bước, nhưng mẫu nhỏ nên chưa chắc về mặt thống kê).
- **Sắp làm (khi chạy thật):** chạy bản chính 81 màn; làm thử nhánh nhiều màn để có con số Step-SR; đo độ chính xác của thuật toán đối chiếu.

---

## 🧭 Phụ lục — 5 câu người ngoài hay hỏi + trả lời gọn

1. *"Sao không đưa danh sách nút cho máy để nó viết đúng luôn?"* → Vì mục tiêu là ĐO xem máy tự bịa bao nhiêu. Đưa danh sách thì nó chép, hết đo được. (Khi triển khai thật thì có thể đưa; khi nghiên cứu thì cố ý tách ra.)
2. *"Không có đáp án mẫu sao chấm?"* → Neo bằng **danh sách nút thật** (mỏ neo thay đáp án) + tự kiểm thước đo bằng bơm-lỗi.
3. *"Thực tế lấy đâu ra danh sách nút?"* → Trên điện thoại, Android cung cấp sẵn (dùng cho tính năng trợ năng). Nếu chỉ có ảnh thì cần một bộ dò nút (có sai số).
4. *"Cơ chế nghe đơn giản, đóng góp ở đâu?"* → Đóng góp ở **phát hiện thực nghiệm** (đo bịa nhiều model, bằng chứng thất bại đo được) + **cách đánh giá**, không phải ở độ phức tạp code. Nhiều bài nổi tiếng (G-Eval, FActScore, RAGAS) cũng pipeline gọn.
5. *"Kết quả đâu?"* → Một màn đã có số sơ bộ; nhiều màn đang làm. "Ngang nhau" là có điều kiện — khai thẳng chỗ nào chưa có số.
