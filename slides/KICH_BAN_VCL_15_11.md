# Kịch bản trình bày VCL 2026 (bản 15/11, sắp lại cho mạch lạc) và bộ câu hỏi dự kiến

**Bài:** *Sinh hướng dẫn sử dụng phần mềm từ ảnh chụp màn hình và mục tiêu người dùng: xây dựng
ngữ liệu quy chiếu tự động khi phần tử giao diện không có tên cụ thể*
Lê Đoàn Phương Uyên & Nguyễn Hồng Bửu Long · Hội thảo VCL 2026, HUFLIT, 27/11/2026.

**Khung giờ:** 15 phút trình bày + hỏi đáp. Lời nói dưới đây khoảng **12 phút**.
**Nguồn số:** `paper/vcl2026/main.tex` (bản đã nộp).

## Mạch của bài (đọc trước khi tập nói)

Cả bài là một chuỗi nhân quả, mỗi slide trả lời câu hỏi mà slide trước để lại:

```
PHẦN 1. BÀI TOÁN
  2  Muốn máy viết câu chỉ người khác bấm vào đâu
  3  → nhưng nhiều nút không có tên
  4  → nên phải chỉ qua vật bên cạnh (người viết cũng làm vậy)
  5  → muốn dạy máy làm vậy thì cần dữ liệu, mà chưa có ⇒ bài này tạo dữ liệu đó
                                        (dàn ý 3 phần)
PHẦN 2. TẠO NHÃN
  6  Mỗi bước cần một nhãn bốn ô (đích cần đạt)
  7  → điền bằng quy trình bốn bước (bản đồ của phần 2)
  8  → bước 1: ghép dữ liệu, kiểm ghép đúng
  9  → bước 2–3: tìm nút được bấm và lấy tên
 10  → bước 4: tìm mốc chữ bên cạnh (ví dụ Gmail)
 11  → bản đầu của bước 4 làm sai, làm lại 7,3% → 75,3%
PHẦN 3. KIỂM TRA NHÃN
 12  So với câu người viết: 53,5% vs 7,6%
 13  Chỗ còn yếu: nút chỉ có ký hiệu
PHẦN 4. KẾT LUẬN
 14  Hạn chế
 15  Kết luận (nhắc lại đúng ba phần)
```

**Quy ước trên slide:** mọi slide nội dung có một **thanh tiến độ** nhỏ ở góc trên phải gồm bốn chữ
*Bài toán · Tạo nhãn · Kiểm tra · Kết luận*, phần đang trình bày tô đậm. Slide 7 có sơ đồ bốn bước, và ở các
slide 8–11 sơ đồ này xuất hiện thu nhỏ với bước đang nói được tô màu.

**Quy ước lời nói:** câu đầu mỗi slide nối với slide trước, câu cuối dẫn sang slide sau (in nghiêng trong
kịch bản để dễ nhớ). Hai câu này là thứ làm bài nghe mạch lạc, nên giữ lại dù nói tắt phần giữa.

---

## Slide 1 · Bìa (~15 giây)

**Trên slide:** tên bài (3 dòng) · hai tác giả · Khoa CNTT, Trường ĐH Khoa học Tự nhiên, ĐHQG-HCM ·
VCL 2026, HUFLIT, 27/11/2026.

**Lời nói:**
Kính chào quý thầy cô và các bạn. Tôi là Lê Đoàn Phương Uyên, Trường Đại học Khoa học Tự nhiên. Đây là bài
làm chung với thầy Nguyễn Hồng Bửu Long. *Tôi xin bắt đầu bằng một tình huống rất quen.*

---

## Slide 2 · Mục tiêu: máy viết câu chỉ cho người khác bấm vào đâu (~45 giây)

**Phần:** Bài toán
**Trên slide:** bên trái hai bong bóng hội thoại:
*"Con ơi, muốn gửi thư thì bấm vào đâu?"*
*"Mẹ bấm vào cái biểu tượng ngay trên chữ Gmail."*
Bên phải sơ đồ: `ảnh màn hình + việc người dùng muốn làm` → `mô hình` → `một câu hướng dẫn`

**Lời nói:**
Chắc ai cũng từng chỉ ba mẹ dùng điện thoại. Mẹ hỏi: muốn gửi thư thì bấm vào đâu? Mình trả lời: mẹ bấm vào
cái biểu tượng ngay trên chữ Gmail.

Chúng tôi muốn máy làm đúng việc đó: nhận ảnh màn hình và việc người dùng đang muốn làm, rồi viết ra **một
câu** để người đọc biết bấm vào đâu. Câu như vậy giúp người lớn tuổi, người mới dùng ứng dụng, người dùng
trình đọc màn hình.

*Nghe thì đơn giản, nhưng có một cái khó nằm ngay trong ví dụ này.*

---

## Slide 3 · Cái khó: nhiều nút không có tên để gọi (~50 giây)

**Phần:** Bài toán
**Trên slide:** ảnh `fig_moneo.png` (bốn biểu tượng). Bên cạnh con số lớn: **22%** · *nút cần bấm không có tên*
Dòng nhỏ: *thêm 7,6% nút trùng tên ⇒ gần 1/3 số bước không gọi đúng tên được*

**Lời nói:**
*Cái khó là thế này.* Màn hình này có bốn biểu tượng: Gmail, Drive, Messages, Chrome. Mắt người thấy rõ.
Nhưng trong thông tin ứng dụng khai báo với hệ điều hành, cả bốn đều **không có tên**. Với máy, đây chỉ là
bốn cái hình.

Chuyện này không hiếm: **22%** nút người dùng cần bấm không có tên, thêm 7,6% nút trùng tên với nút khác.
Gần một phần ba số trường hợp, không thể nói đơn giản "bấm vào nút X".

*Vậy khi không có tên thì người ta chỉ bằng cách nào?*

---

## Slide 4 · Không có tên thì phải chỉ qua vật bên cạnh (~55 giây)

**Phần:** Bài toán
**Trên slide:** hai cột:
- **Ảnh đời thường:** "con mèo đen bên trái" · *vật nào cũng có tên*
- **Màn hình điện thoại:** "biểu tượng ngay trên chữ Gmail" · *phải chỉ qua vật bên cạnh*
Một con số: **1/3** câu do người viết dùng từ chỉ vị trí ("trên", "dưới", "góc phải"…)
Dòng dưới: *Ngôn ngữ học gọi đây là sinh biểu thức quy chiếu: viết câu để người nghe nhận ra đúng một vật giữa nhiều vật giống nhau (Dale & Reiter, 1995).*

**Lời nói:**
*Câu trả lời là chỉ qua vật bên cạnh.* Trong ngôn ngữ học, việc viết câu để người nghe nhận ra đúng một vật
giữa nhiều vật giống nhau có tên là **sinh biểu thức quy chiếu**.

Trên ảnh đời thường, con mèo thì gọi là con mèo, chỉ cần thêm "màu đen", "bên trái". Trên màn hình điện thoại
thì ngược lại: nhiều thứ không có tên, nên chỉ qua vật bên cạnh, kiểu "ngay trên chữ Gmail", lại thành cách chính.

Người viết thật cũng làm vậy. Trong hơn 41 nghìn câu hướng dẫn do người viết, khoảng **một phần ba** phải dùng
từ chỉ vị trí như "trên", "dưới", "góc phải".

*Muốn máy học được cách chỉ như vậy, thì cần dữ liệu.*

---

## Slide 5 · Cần dữ liệu để dạy máy, nên bài này tạo dữ liệu đó (~55 giây)

**Phần:** Bài toán
**Trên slide:** trên: **AndroidControl** (Google, 2024): 15.283 lần người thật thao tác; mỗi bước có *ảnh · chỗ bấm · câu do người viết*. **Thiếu:** *nút được bấm tên gì, khác các nút giống nó ở đâu.*
Dưới: khung **Dàn ý** ba dòng đánh số:
1. Tạo nhãn: nhãn trông thế nào, điền tự động ra sao
2. Kiểm tra: làm sao biết nhãn đúng
3. Kết luận: còn thiếu gì

**Lời nói:**
*Muốn dạy máy thì cần nhiều ví dụ.* Google có công bố bộ AndroidControl: hơn mười lăm nghìn lần người thật làm
việc trên điện thoại, mỗi bước có ảnh, chỗ người đó bấm, và một câu hướng dẫn do người viết.

Nhưng bộ này thiếu đúng thứ chúng tôi cần: nút được bấm tên là gì, và nó khác những nút giống nó ở chỗ nào.

Bài này **tự động** bổ sung thông tin đó, không viết tay nhãn nào. Phần còn lại của bài đi theo ba câu hỏi:
nhãn trông thế nào và được điền ra sao; làm sao biết nhãn đúng; và còn thiếu gì.

*Bắt đầu với câu hỏi thứ nhất: nhãn trông thế nào.*

---

## Slide 6 · Mỗi bước cần một nhãn bốn ô (~50 giây)

**Phần:** Tạo nhãn
**Trên slide:** ảnh Gmail thu nhỏ bên trái, bên phải bảng:
| ô | ví dụ trên màn Gmail | nghĩa |
|---|---|---|
| loại | icon | nút, ô nhập hay biểu tượng |
| tên | (không có tên) | chữ hiển thị trên nút |
| vị trí | 111, 903 | chỗ bấm, thang 0 đến 1.000 |
| **dấu hiệu phân biệt** | **ngay trên chữ "Gmail"** | **khác các nút giống nó ở đâu** |

**Lời nói:**
*Đây là thứ chúng tôi muốn có cho mỗi bước:* một nhãn gồm bốn ô.

Lấy lại màn Gmail. Ô loại: đây là một biểu tượng. Ô tên: không có tên. Ô vị trí: chỗ bấm. Và ô thứ tư, quan
trọng nhất, là **dấu hiệu phân biệt**: nút này khác ba nút kia ở đâu, ở đây là "ngay trên chữ Gmail".

Khi nút có tên, ba ô đầu gần như đủ. Khi nút không có tên, mọi việc dồn vào ô thứ tư.

*Vậy máy tự điền bốn ô này thế nào?*

---

## Slide 7 · Nhãn được điền tự động qua bốn bước (~40 giây)

**Phần:** Tạo nhãn
**Trên slide:** sơ đồ bốn khối nằm ngang, đánh số, có mũi tên:
① **Ghép dữ liệu** (ảnh + câu + danh sách nút) → ② **Tìm nút được bấm** → ③ **Lấy tên nút** → ④ **Tìm dấu hiệu phân biệt**
Dưới mỗi khối một dòng nhỏ: *ghép hai bản công bố* · *khung nhỏ nhất chứa chỗ bấm* · *danh sách hệ thống, rồi đọc chữ trong ảnh* · *chữ gần nhất làm mốc*
Dòng cuối: *Toàn bộ bằng quy tắc, không viết tay nhãn nào.*

**Lời nói:**
*Bốn ô được điền qua bốn bước, hoàn toàn bằng quy tắc.*

Bước một, ghép dữ liệu cho đủ nguyên liệu. Bước hai, tìm xem nút được bấm là nút nào. Bước ba, lấy tên của
nút đó. Bước bốn, tìm dấu hiệu phân biệt.

Bước nào cũng có một chỗ dễ sai. *Tôi sẽ đi lần lượt, bắt đầu từ bước một.*

---

## Slide 8 · Bước 1: ghép hai bản dữ liệu, và kiểm là ghép đúng (~55 giây)

**Phần:** Tạo nhãn · sơ đồ bốn bước thu nhỏ, tô bước ①
**Trên slide:** dòng trên: *Bản 1: câu + danh sách nút, thiếu ảnh. Bản 2: ảnh, thiếu câu. ⇒ ghép theo mã bước.*
Biểu đồ hai cột: **ghép đúng 48%** · **cố ý ghép lệch 20%** (cột xám). Nhãn trục: *chữ ngay chỗ bấm có xuất hiện trong câu*

**Lời nói:**
*Bước một là gom đủ nguyên liệu.* Mỗi bước cần ảnh màn hình, câu do người viết, và **danh sách nút** mà ứng
dụng khai báo cho hệ điều hành, gọi là cây trợ năng. Không bản công bố nào có đủ cả ba, nên phải ghép hai bản
theo mã của từng bước.

Sợ nhất là ghép lệch một bước: ảnh bước này đi với câu bước kia mà máy không báo lỗi gì. Để kiểm, chúng tôi đọc
chữ ngay chỗ người dùng bấm rồi xem chữ đó có nằm trong câu không. Ghép đúng: **48%** có. Cố ý ghép lệch để so:
chỉ **20%**. Hai số cách xa nhau, nên ghép đúng.

*Có đủ nguyên liệu rồi, bước tiếp là tìm nút và lấy tên.*

---

## Slide 9 · Bước 2 và 3: tìm nút được bấm, rồi lấy tên của nó (~55 giây)

**Phần:** Tạo nhãn · sơ đồ thu nhỏ, tô bước ② và ③
**Trên slide:** hai hộp trái/phải:
- **Bước 2:** chọn **khung nhỏ nhất** chứa chỗ bấm *(vì các khung lồng nhau, từ cả màn hình tới cái nút)*
- **Bước 3:** chỉ **12,6%** phần tử có tên trong danh sách hệ thống ⇒ cho máy **đọc chữ trong ảnh (OCR)**
Dải màu dưới: **Không chắc thì để trống, không đoán.**

**Lời nói:**
*Bước hai là tìm xem người dùng bấm vào nút nào.* Mỗi nút có một khung chữ nhật trên màn, và các khung lồng nhau:
một chỗ bấm nằm trong hàng chục khung, từ khung cả màn hình tới đúng cái nút. Nên chúng tôi chọn **khung nhỏ nhất**.

*Bước ba là lấy tên nút.* Lẽ ra lấy từ danh sách hệ thống là xong, nhưng đếm thử thì chỉ **12,6%** phần tử có tên.
Nên chúng tôi cho máy đọc thêm chữ trong ảnh, kỹ thuật gọi là OCR.

OCR có lúc đọc nhầm, ví dụ đọc biểu tượng thành chữ cái. Nên nguyên tắc là: **không chắc thì để trống**. Để trống
thì máy chỉ mất một ví dụ. Ghi sai thì máy học gọi nút bằng một cái tên không có trên màn hình.

*Với nút như Gmail ở đây, ô tên để trống, và mọi việc chuyển sang bước bốn.*

---

## Slide 10 · Bước 4: lấy chữ gần nhất làm mốc, như khi chỉ đường (~50 giây)

**Phần:** Tạo nhãn · sơ đồ thu nhỏ, tô bước ④
**Trên slide:** ảnh `fig_moneo.png` lớn, đánh dấu nút cần bấm, ba nút giống nó, chữ "Gmail", khoảng cách 114,5 px.
Dưới: *Máy viết:* `ngay trên chữ "Gmail"` · *Người viết:* "Click on the gmail option"

**Lời nói:**
*Bước bốn làm giống cách ta chỉ đường:* "nhà ngay sau tiệm thuốc". Máy tìm dòng chữ gần nút nhất mà nằm ngoài
nút, ở đây là chữ Gmail, rồi lấy làm **mốc**, kèm hướng: trên, dưới, trái hay phải. Chúng tôi gọi đó là mỏ neo chữ.

Người chú thích, khi viết câu cho đúng bước này mà không hề biết quy tắc của chúng tôi, cũng chỉ qua đúng chữ
Gmail: "Click on the gmail option".

*Nhưng bước bốn không đúng ngay từ đầu.*

---

## Slide 11 · Bản đầu của bước 4 làm sai, phải làm lại (~50 giây)

**Phần:** Tạo nhãn · sơ đồ thu nhỏ, tô bước ④
**Trên slide:** hai cột trước/sau:
- **Bản đầu:** "một trong bảy biểu tượng cùng loại" · **7,3%** chỉ ra được đúng nút
- **Bản làm lại:** "ngay trên chữ Gmail" · **75,3%** chỉ ra được đúng nút

**Lời nói:**
*Bản đầu của bước bốn chủ yếu viết kiểu* "đây là một trong bảy biểu tượng cùng loại". Câu đó không sai, nhưng vô
ích: nó chỉ báo có bảy cái giống nhau, không nói là cái nào. Chỉ **7,3%** trường hợp chỉ ra được đúng nút.

Chúng tôi phát hiện khi đọc tay khoảng một nghìn nhãn. Sắp xếp lại quy tắc, ưu tiên mốc chữ như ví dụ Gmail, tỉ
lệ lên **75,3%** trên toàn bộ dữ liệu.

Đến đây là xong phần tạo nhãn, được hơn 41 nghìn nhãn. *Câu hỏi tiếp theo: làm sao biết các nhãn đó đúng?*

---

## Slide 12 · Kiểm nhãn bằng câu do người viết (~65 giây)

**Phần:** Kiểm tra
**Trên slide:** biểu đồ hai cột lớn:
- tên máy đặt **trùng** chữ trong câu người viết cho đúng bước đó: **53,5%**
- so với câu của bước kế tiếp (đối chứng): **7,6%** (cột xám)
Dòng dưới: *Máy không đọc câu của người khi tạo nhãn ⇒ trùng nhau là hai nguồn độc lập cùng gọi một tên.*

**Lời nói:**
*Chấm tay hơn 41 nghìn nhãn thì không làm nổi, nên chúng tôi dùng câu do người viết làm phép thử.*

Khi tạo nhãn, máy **không hề đọc** câu đó. Nên nếu tên máy đặt lại trùng với chữ người viết dùng, thì đó là hai
nguồn độc lập cùng gọi một tên. Kết quả: **53,5%** trùng nguyên văn.

Để biết số đó cao hay thấp, chúng tôi làm một **đối chứng**, tức phép so cố ý làm sai để lấy mức nền: đem chính
những cái tên đó so với câu của bước kế tiếp, trên màn rất giống. Chỉ còn **7,6%**, thấp hơn khoảng bảy lần.

53,5% không có nghĩa là gần nửa số tên sai: người viết hay gọi chung kiểu "the search bar" cho ô có chữ "Search
here", mà so nguyên văn không tính. Đây là mức thấp nhất.

*Kiểm tra cũng cho thấy nhãn chưa tốt đều ở mọi chỗ.*

---

## Slide 13 · Chỗ còn yếu: nút chỉ có một ký hiệu (~45 giây)

**Phần:** Kiểm tra
**Trên slide:** ba thanh ngang, tỉ lệ chỉ ra được đúng nút:
- nút có tên rõ ràng: **80%**
- nút không có tên: 67%
- nút chỉ có một ký hiệu (ví dụ "Q", "?"): **38%**

**Lời nói:**
*Con số 75% ở bước bốn là trung bình, và trung bình che mất một chuyện.* Nút có tên rõ ràng, vốn dễ gọi, lại được
làm tốt nhất: 80%. Nút chỉ có một ký hiệu như chữ Q đứng lẻ, chỉ 38%.

Lý do: muốn có mốc chữ thì cần chữ ở gần, mà chỗ toàn biểu tượng thì thường ít chữ. Chỗ cần dấu hiệu phân biệt
nhất lại khó tìm mốc nhất.

*Đây cũng là hạn chế đầu tiên tôi muốn nói ở phần cuối.*

---

## Slide 14 · Những gì bài này chưa làm được (~40 giây)

**Phần:** Kết luận
**Trên slide:** ba gạch:
- Khoảng **1/4** dấu hiệu chưa chỉ ra được đúng nút (đã rõ lý do)
- Chưa hỏi người dùng thật xem đọc nhãn có tìm ra nút không
- Dữ liệu gốc không có đáp án chuẩn để kiểm OCR

**Lời nói:**
*Bài còn ba chỗ chưa làm được.* Một, khoảng một phần tư dấu hiệu chưa chỉ ra được đúng nút; hướng sửa là lấy mốc
từ cả các nút cùng loại, không chỉ từ chữ. Hai, cách kiểm tốt nhất cho ô thứ tư là đưa nhãn cho người thật xem
và hỏi họ có tìm ra nút không; chúng tôi chưa làm. Ba, dữ liệu gốc không có đáp án chuẩn cho chữ trên màn, nên
chúng tôi không nói được OCR đúng bao nhiêu phần trăm.

*Tôi xin tóm lại.*

---

## Slide 15 · Kết luận (~40 giây)

**Phần:** Kết luận
**Trên slide:** ba dòng, khớp ba phần của bài:
- **Bài toán:** gần **1/3** số nút cần bấm không gọi đúng tên được ⇒ phải chỉ qua vật bên cạnh
- **Tạo nhãn:** tự động **41.099 + 4.448** nhãn bốn ô (GUIRefCorpus); dấu hiệu phân biệt **7,3% → 75,3%**
- **Kiểm tra:** **53,5%** trùng câu người viết, so với **7,6%** ở đối chứng
Dòng nhỏ: *Phần dạy mô hình bằng bộ dữ liệu này: bài đồng hành.*

**Lời nói:**
Tóm lại theo đúng ba phần vừa đi qua. Về bài toán: trên điện thoại, gần một phần ba số nút cần bấm không gọi đúng
tên được, nên câu hướng dẫn phải chỉ qua vật bên cạnh. Về tạo nhãn: chúng tôi tự động tạo hơn 45 nghìn nhãn bốn
ô, gọi là GUIRefCorpus, trong đó dấu hiệu phân biệt đi từ 7,3% lên 75,3% sau khi làm lại. Về kiểm tra: tên máy đặt
trùng câu người viết 53,5%, cao gấp bảy lần mức đối chứng.

Phần dạy mô hình bằng bộ dữ liệu này nằm ở bài đồng hành của nhóm.

---

## Slide 16 · Cảm ơn (~10 giây)

**Trên slide:** "Cảm ơn quý thầy cô và các bạn đã lắng nghe" · email.

**Lời nói:**
Phần trình bày của tôi đến đây là hết. Cảm ơn quý thầy cô và các bạn đã lắng nghe, tôi rất mong nhận được câu hỏi
và góp ý.

---
---

# BỘ CÂU HỎI DỰ KIẾN VÀ CÁCH TRẢ LỜI

Mẹo chung khi trả lời:
- Câu đầu tiên trả lời thẳng (có / không / con số). Giải thích sau.
- Không biết thì nói "phần này chúng tôi chưa đo", đừng đoán.
- Nếu câu hỏi đụng tới kết quả huấn luyện: trả lời ngắn, rồi nói chi tiết nằm ở bài đồng hành.
- Câu có đánh dấu ⭐ là câu khả năng bị hỏi cao nhất.

## Nhóm A. Về bài toán và đóng góp

**A1 ⭐. Đóng góp chính của bài là gì? Có phải chỉ là ghép hai bộ dữ liệu có sẵn?**
Không chỉ ghép. Có ba phần. Một là nhãn bốn ô dựng bằng quy tắc cho hơn 41 nghìn bước, trong đó ô dấu
hiệu phân biệt là phần mới về nội dung, vì AndroidControl không có. Hai là bộ kiểm định dùng lại được:
đối chứng ghép lệch, kiểm rò rỉ, chín bất biến cấu trúc, và phép đối chiếu với câu của người chú thích.
Ba là phân tích cho thấy trong miền giao diện, cả người lẫn máy đều chuyển từ gọi tên sang chỉ vị trí.
Ghép dữ liệu chỉ là bước chuẩn bị.

**A2 ⭐. Vì sao gọi đây là bài toán sinh biểu thức quy chiếu? Liên quan gì tới ngôn ngữ học tính toán?**
Vì mục tiêu của câu là giúp người nghe nhận ra đúng một đối tượng giữa nhiều đối tượng giống nó. Đó đúng là
định nghĩa của Dale và Reiter năm 1995. Phần ngôn ngữ học nằm ở ô thứ tư: chúng tôi đo được rằng khi
không có tên, cả người chú thích lẫn quy tắc đều chuyển sang mô tả bằng quan hệ, đúng loại mô tả Dale và
Haddock đề xuất năm 1991. Điểm mới là trong miền này, quan hệ không còn là phương án phụ mà thường là
phương án duy nhất.

**A3. Bài toán này khác gì so với các tác tử như SeeClick, OS-Atlas, UGround?**
Các hệ đó nhận câu rồi trả về toạ độ cho máy bấm. Chúng tôi làm chiều ngược lại: nhận ảnh và mục tiêu,
viết câu cho người đọc. Hai chiều bổ sung cho nhau. Thật ra ở bài đồng hành, chúng tôi còn dùng một mô
hình như UGround làm "người đọc" để chấm câu của mình.

**A4. Ứng dụng thực tế là gì?**
Trợ giúp người dùng bị kẹt giữa chừng một tác vụ, hỗ trợ người lớn tuổi, người dùng trình đọc màn hình,
và sinh tự động trang hướng dẫn sử dụng phần mềm. Nhóm dùng trình đọc màn hình là nhóm chịu thiệt nhiều
nhất khi phần tử không có tên, vì trình đọc chỉ đọc được 12,6% phần tử có nhãn.

## Nhóm B. Về cách dựng nhãn

**B1 ⭐. Sao không dùng một mô hình lớn (GPT-4o, Qwen-VL…) để sinh nhãn cho tự nhiên hơn?**
Ba lý do. Một, nhãn quy tắc dựng lại được y hệt và kiểm lại được, mỗi lần sửa quy tắc là dựng lại toàn
bộ trong thời gian ngắn. Hai, mô hình sinh nhãn có thể bịa ra một cái tên nghe hợp lý mà không có trên
màn hình, đúng loại lỗi chúng tôi muốn tránh nhất. Ba, chi phí. Đổi lại, nhãn quy tắc nghèo hơn về ngôn
ngữ, và chúng tôi chưa đo được khoảng cách đó. Đây là điểm yếu chúng tôi thừa nhận.

**B2. Vì sao ưu tiên cây trợ năng trước OCR, khi OCR cho nhiều tên hơn?**
Chúng tôi từng suýt đảo thứ tự, vì đo thấy câu của người khớp với OCR gấp 3,2 lần khớp với cây trợ năng.
Nhưng truy kỹ thì tỉ số đó chỉ dựng trên 72 nhãn, tức 6,7% mẫu thử. Trong 12 ca nghiêng về OCR, 11 ca là
do nhãn trợ năng ở đó là rác. Khi cả hai nguồn đều cho chuỗi dùng được, chỉ còn 1 ca nghiêng về OCR so
với 3 ca nghiêng về cây trợ năng. Vậy ưu thế của OCR là ưu thế của việc lọc rác, nên chúng tôi giữ thứ
tự và thêm bộ lọc. (Slide dự phòng nếu có.)

**B3. Ngưỡng 350 pixel và 25% màn hình lấy từ đâu? Có thử ngưỡng khác không?**
350 px là bán kính tối đa để mỏ neo còn được coi là "bên cạnh". 25% đến từ 25 ca hộp lớn trong mẫu thử,
không ca nào khớp câu của người. Chúng tôi không quét nhiều ngưỡng, và căn cứ của ngưỡng 25% chỉ dựa trên
25 ca, bài có ghi rõ. Bộ lọc này chỉ tác động 2,2% số bước, nên đổi ngưỡng không làm thay đổi nhiều kết quả.

**B4. Độ chính xác của OCR là bao nhiêu?**
Chúng tôi không công bố con số này, vì AndroidControl không có nhãn chuẩn cho chữ trên màn. Cái chúng tôi
báo là OCR chạy lại trên hai máy khác nhau cho kết quả trùng nhau, mật độ chữ đồng đều giữa hai tập (24,2
và 23,6 chuỗi mỗi màn), và hai kiểu lỗi quan sát được.

**B5. Toạ độ thang 0–1.000 có phụ thuộc độ phân giải không? Màn hình khác cỡ thì sao?**
Không. Toạ độ được chia cho chiều rộng và chiều cao ảnh rồi mới đưa về thang 1.000, nên độc lập với độ
phân giải. Ô toạ độ cũng là ô duy nhất giữ nguyên đáp án, nên ô này không thể sai.

**B6. Lấy hộp bao nhỏ nhất thì có trường hợp chọn nhầm phần tử con (ví dụ chữ nằm trong nút) không?**
Có thể. Hộp nhỏ nhất đôi khi là một nhãn chữ con bên trong nút chứ không phải cả cái nút. Về chỗ chạm
thì không sai, vì chạm vào nhãn con cũng kích hoạt nút. Về ô vai trò thì có thể ghi là "text" thay vì
"button". Chúng tôi chưa đo riêng tỉ lệ này.

**B7. Hướng mỏ neo lệch: "to the right of" nhiều gấp 4 lần "to the left of". Có phải lỗi quy tắc?**
Không phải lỗi. Nhãn tả vị trí của phần tử so với chữ neo, mà trên Android chữ mô tả thường đặt bên trái
nút bấm hoặc công tắc. Nên "phần tử nằm bên phải chữ" xuất hiện nhiều hơn. Theo chiều dọc thì hai hướng
gần cân nhau.

**B8. Có thông tin cá nhân lọt vào nhãn không?**
Có thể. Ảnh được ghi khi người thật thao tác nên có thể có email, tên riêng, và OCR sẽ đọc chúng. Chúng tôi
giữ nguyên theo bản gốc vì mọi bộ lọc tự động đều sẽ xoá nhầm chữ hợp lệ trên giao diện. AndroidControl
phát hành theo CC0 và chúng tôi không thu thập màn hình mới. Bài có mục riêng về chuyện này.

## Nhóm C. Về đánh giá chất lượng nhãn

**C1 ⭐. 53,5% có thấp không? Nghĩa là gần một nửa số tên bị sai?**
Không. Phép so là so nguyên văn. Người chú thích hay gọi bằng tên loại, ví dụ "the search bar" cho ô có chữ
"Search here", hoặc "search icon" cho cái kính lúp. Những ca đó tên vẫn đúng nhưng không khớp nguyên văn.
Nên 53,5% là chặn dưới. Ý nghĩa của nó nằm ở chỗ cao hơn đối chứng khó 7,6% khoảng bảy lần.

**C2 ⭐. Sao không cho người chấm tay chất lượng nhãn?**
Chúng tôi có đọc tay mẫu thử 1.074 nhãn để dò lỗi quy tắc và kiểm 737 mỏ neo. Nhưng chưa làm khảo sát
người dùng kiểu "đọc nhãn này, chỉ vào nút trên ảnh". Đó là cách kiểm đúng nhất cho ô dấu hiệu phân biệt và
là hạn chế thứ hai chúng tôi nêu. Lý do là nguồn lực, không phải vì nghĩ nó không cần.

**C3. Con số 75,3% đo bằng gì? Có phải tự chấm bài của mình?**
Đúng là phần này đếm trên chính quy tắc: phân loại bốn khuôn câu do quy tắc tạo ra, nên nó chỉ đếm loại
mệnh đề, chưa xác nhận mệnh đề giúp được người dùng. Bài có nói rõ điều đó. Bằng chứng từ bên ngoài là
phép so ô tên với câu người (53,5%) và tần suất người dùng từ chỉ vị trí (32,5%).

**C4. Mẫu thử 1.074 nhãn có đại diện không?**
Sáu chỉ số chất lượng trên mẫu thử và trên toàn bộ 41.099 nhãn lệch nhau không quá 1,6 điểm phần trăm, dù
mẫu thử nhỏ hơn 38 lần. Ví dụ không có tên: 23,4% trên mẫu thử, 22,0% toàn bộ.

**C5. Kiểm định ghép 48,3% so với 19,6% có đủ chặt không? Một phần nhỏ dòng ghép lệch thì sao?**
Đúng là phép kiểm này chỉ bắt lỗi ghép có hệ thống, chứ không xác nhận từng dòng. Nếu chỉ vài phần trăm
dòng bị lệch ngẫu nhiên thì nó không bắt được, bài có ghi. Chúng tôi chọn cách này vì rẻ, chạy lại được
sau mỗi lần dựng, và nhắm đúng loại lỗi có thể phá hỏng cả bộ dữ liệu mà không ai biết.

**C6. Có lối tắt nào mô hình có thể học không, ví dụ nhãn đúng luôn dài hơn?**
Đã kiểm. Quy tắc "cứ chọn nhãn dài hơn" chỉ đoán đúng 43,2%, thấp hơn mức ngẫu nhiên 50%. Nên lối tắt độ
dài không có.

## Nhóm D. Về dữ liệu và khả năng mở rộng

**D1 ⭐. Có làm được cho tiếng Việt không? Ứng dụng Việt Nam thì sao?**
Về quy trình thì được, vì các bước (cây trợ năng, OCR, quy tắc chọn hộp, mỏ neo) không phụ thuộc ngôn ngữ.
Cần OCR đọc được tiếng Việt và khuôn câu tiếng Việt cho ô thứ tư. Phần đã kiểm là việc đổi khuôn nhãn giữa
tiếng Việt và tiếng Anh chỉ là đổi từ vựng (tổng phép tính huấn luyện lệch 0,03%). Phần chưa làm là chạy
trên giao diện tiếng Việt thật, vì chưa có bộ dữ liệu ghi thao tác người dùng Việt cỡ AndroidControl.

**D2. Có chuyển sang web, iOS, máy tính được không?**
Được nếu dữ liệu có ba thứ: ảnh màn hình, điểm chạm và cây cấu trúc giao diện (DOM ở web, view hierarchy
ở iOS). Chúng tôi chưa thử.

**D3. Bộ dữ liệu có công bố không? Gồm những gì?**
Mỗi dòng là một bản ghi JSON gắn với một bước chạm: bốn ô của nhãn, nguồn của tên, tầng tên, toạ độ, hộp
bao, cờ trùng tên và trùng vai trò, nhãn của phần tử hàng xóm, và khoá (episode_id, step_id) để nối về bước
gốc. Ảnh không đi kèm vì AndroidControl đã phát hành ảnh theo CC0. Về thời điểm phát hành, chúng tôi chưa
chốt ngày nên xin không hứa ở đây.

**D4. Tập kiểm tra có phải tập test chính thức của AndroidControl không?**
Không. Cách chia đến từ bản phát hành có ảnh mà chúng tôi dùng. Kiểm sau này cho thấy phần lớn tác vụ
tập kiểm thuộc split train chính thức của AndroidControl. Điều đó không ảnh hưởng tới bài này vì bài này
dựng nhãn, không chấm mô hình, và giữa hai tập của chúng tôi không có tác vụ trùng. Nhưng ai đem so kết
quả với số báo trên split chính thức thì cần lưu ý.

**D5. 55,6% số bước có phần tử cạnh tranh trong khoảng 80–350 px. Sao lại chọn khoảng đó?**
Mốc dưới 80 px vì dưới khoảng 63 px thì khâu chấm điểm ở bài đồng hành gộp hai phần tử làm một, cộng thêm
biên an toàn. Mốc trên 350 px là bán kính của mỏ neo.

## Nhóm E. Câu hỏi về mô hình (trả lời ngắn, chuyển sang bài đồng hành)

**E1 ⭐. Mô hình huấn luyện trên bộ dữ liệu này cho kết quả thế nào?**
Phần đó nằm ở bài đồng hành. Tóm tắt một câu: chúng tôi tinh chỉnh Qwen2.5-VL-3B và chấm câu sinh ra bằng
một mô hình định vị đọc câu rồi trỏ lên màn hình. Mô hình tinh chỉnh tăng rõ so với mô hình gốc. Tuy vậy,
huấn luyện thêm nhãn bốn ô trước câu chưa cho lợi ích rõ so với chỉ học câu. Chúng tôi coi đó là kết quả
cần báo thật, không giấu.
*(Số nếu bị hỏi tiếp, đã công bố ở bài SOICT 2026: theo tiêu chí hộp phần tử D.3, mô hình gốc 53,6 · chỉ
học câu 65,5 · nhãn rồi câu 63,6 · thêm ORPO 66,5 · câu chuẩn của người 83,8.)*

**E2. Vậy nhãn bốn ô có vô ích không?**
Không hẳn. Trên các câu không lặp lại câu trong tập huấn luyện, bản có tinh chỉnh ưu tiên trên nhãn hơn bản
chỉ học câu khoảng 1,9 điểm, có ý nghĩa thống kê, nhưng đó là phân tích sau khi thấy kết quả. Một quan sát
liên quan tới bài này: khi mô hình gọi sai tên, 76,5% trường hợp phần tử nó tả nằm xa hơn 350 px. Nghĩa là
mô hình hay nhìn sang chỗ khác hẳn chứ không lẫn hai nút cạnh nhau. Chỗ khó thật là phần tử không có chữ
để gọi.

## Nhóm F. Câu hỏi khó / mang tính phê bình

**F1. Quy tắc thủ công như vậy có lỗi thời trong thời đại mô hình lớn không?**
Mô hình lớn vẫn cần dữ liệu có nhãn kiểm chứng được, đặc biệt khi cần biết nhãn có bịa không. Quy tắc ở đây
không thay mô hình, nó tạo ra nguồn giám sát rẻ và kiểm được. Và chính phân tích tầng tên cho thấy chỗ quy
tắc bất lực (tên phải suy từ hình dạng biểu tượng) là chỗ mô hình thị giác cần bổ sung. Hai cách bổ sung
cho nhau.

**F2. Nhãn tiếng Anh thì liên quan gì tới hội thảo ngôn ngữ học tính toán tiếng Việt?**
Bài là về phương pháp dựng ngữ liệu quy chiếu và phân tích chiến lược quy chiếu, những thứ không gắn với
một ngôn ngữ. Ngữ liệu gốc là tiếng Anh nên nhãn theo tiếng Anh cho khớp. Bước tiếp theo tự nhiên là áp
quy trình cho giao diện tiếng Việt, như đã nói ở câu D1.

**F3. Ba lần chữ "hoàn toàn tự động" mà vẫn có người đọc tay. Có mâu thuẫn không?**
Không. "Tự động" là nói khâu dán nhãn: không nhãn nào trong 41.099 nhãn do người viết, sửa hay chọn. Người
chỉ tham gia ở khâu kiểm. Khi thấy sai thì sửa quy tắc và dựng lại toàn bộ.

---

## Slide dự phòng nên có (agent dựng sau slide Cảm ơn)

1. Hai bản phát hành và phần thiếu của mỗi bản (bảng HarrytheOrange/ckg), ghép theo (episode_id, step_id); 48,3% [43,4; 53,1] trên 400 bước vs 19,6% [15,6; 24,4] trên 311 bước. Cho câu hỏi về cách ghép.
2. Hai bộ lọc: bộ lọc nhãn trợ năng (loại 14,7% trên mẫu thử 1.074 nhãn; 3,9% ứng viên trên toàn bộ) · bộ lọc hình học (hộp < 25% màn; 2,2% số bước; ví dụ hộp 95% màn "THEFELLOWSHIPOF THE RING").
3. Truy nguyên tỉ số 3,2 lần: 72 nhãn → bỏ 32 trùng mục tiêu → 40 nhãn: 12 OCR / 3 cây / 25 không bên nào; 11/12 do nhãn trợ năng rác. Cho câu B2.
4. Bảng sáu chỉ số mẫu thử vs toàn bộ. Cho câu C4.
5. Bốn nhãn thật đặt cạnh câu của người chú thích (Search here/Coffee · Leaf · Q trùng tên · Right arrow).
6. Bảng dấu hiệu phân biệt đầy đủ theo tầng tên (bốn cột: mỏ neo chữ, duy nhất, nêu trùng tên, chỉ đếm).
7. Vị trí so với các công trình liên quan: Dale & Reiter 1995, Dale & Haddock 1991, Mao 2016, Luo 2017, Yu 2017 (ảnh tự nhiên) · Widget Captioning (nhãn do người viết, một widget tách rời) · AndroidControl (câu chỉ dẫn là đầu vào; ở đây là đầu ra).
8. Quy mô chi tiết: 64.567 / 6.958 bước, 41.191 / 4.463 bước chạm, 12.895 / 1.432 tác vụ; ba điều cách chia không bảo đảm (cách diễn đạt lặp lại; 95,6% ứng dụng có ở tập huấn luyện; 55% số bước không gán được ứng dụng).
9. Một bản ghi GUIRefCorpus có gì. Cho câu D3.
10. Người và máy chọn cùng chiến lược: 32,5% câu người viết có từ chỉ vị trí · 67,2% dấu hiệu máy tạo là mốc chữ bên cạnh · 55,6% số bước có nút cạnh tranh trong khoảng 80 đến 350 px · 91,6% có nút cùng vai trò (trung vị 8).
11. Chuỗi mục tiêu bị cắt từ nguồn ("...look for Calvin Kle", 99,4% không có dấu câu cuối, ít nhất 71,3% cắt giữa từ).
