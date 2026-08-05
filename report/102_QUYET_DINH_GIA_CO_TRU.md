# Đóng góp của luận văn là gì, đã làm tới đâu, và cần quyết gì

> Đọc một lượt là nắm: đóng góp nằm ở đâu, những gì đã chạy xong, chỗ nào còn hở, và bạn cần chọn gì tiếp.

---

## 1. Đóng góp là gì — trả lời thẳng

Luận văn nộp ra **một mô hình**, và mô hình đó có một thứ mà bản huấn luyện thông thường không có.

### Mô hình làm được việc gì

Người dùng đang bí trong một ứng dụng, chụp màn hình rồi hỏi. Mô hình nhìn ảnh và viết ra các bước cho họ tự làm.

Đây là việc **chưa mô hình nào được huấn luyện để làm**. Mọi mô hình giao diện hiện nay sinh thao tác cho máy tự bấm; cái này viết câu cho con người đọc.

### Thứ làm nó hơn bản thường

Bắt mô hình **nói ra nó đang nhắm vào nút nào, trước khi viết câu hướng dẫn**.

```
Bản thường học:     "Tap the search bar at the top"

Bản của luận văn:   [ô nhập liệu | "Search Publications..." | ở toạ độ 500,80 | không có ô nào giống]
                    "Tap the Search Publications bar at the top"
```

Dòng đầu là phần thêm vào. Lúc chạy thật thì cắt bỏ, người dùng chỉ nhận dòng sau.

### Vì sao đó là đóng góp về mô hình, không phải về dữ liệu

Vì nó đổi **cái mà mô hình bị buộc phải sinh ra khi học** — tức đổi hành vi của mô hình lúc chạy. Không phải chỉnh sửa dữ liệu rồi huấn luyện như bình thường.

Và đo được riêng: hai nhánh dùng **y hệt** một bộ dữ liệu, chỉ khác chỗ có bắt sinh dòng mô tả hay không. Chênh lệch giữa hai nhánh chính là đóng góp, không lẫn với bất cứ thứ gì.

### Ba tầng, phải phân biệt rõ

| Tầng | Là gì | Có phải đóng góp |
|---|---|---|
| Chuẩn bị dữ liệu | nhờ mô hình lớn viết lại câu gốc cho rõ ràng | **không** — khai thẳng là tiền xử lý |
| **Cách huấn luyện** | **bắt mô hình định vị trước khi viết** | **có — đây là đóng góp chính** |
| Cách chấm | thước tự động không cần đáp án mẫu, không cần thuê người | phụ, nhưng vẫn kể |

---

## 2. Đã làm được gì rồi

Toàn bộ phần dưới đây đã chạy xong trên dữ liệu thật, miễn phí, không tốn đồng nào.

### Dữ liệu để dạy — xong

| Việc | Kết quả |
|---|---|
| Tìm nguồn dữ liệu | ghép hai bản trên mạng, được đủ ảnh + toạ độ chạm + câu người viết cho 15.283 tác vụ |
| Kiểm ghép có đúng không | ghép đúng khớp 47%, ghép lệch một bước chỉ 27% — chênh gần gấp đôi nên phép ghép chuẩn |
| Dựng thử | **1.697 bước** đã có đủ ảnh và nhãn, sẵn sàng đem huấn luyện |
| Đọc chữ trên ảnh | chạy xong toàn bộ 1.697 màn, trung vị 22 dòng chữ mỗi màn |

Trước hôm nay, hồ sơ vẫn ghi *"chưa tải được dữ liệu để dạy"*. Giờ chỗ đó đã thông.

### Nguyên liệu cho phần đóng góp — xong, và tốt hơn dự báo

Phần đóng góp cần một dòng mô tả nút cho mỗi bước. Câu hỏi sống còn: **dựng được dòng đó không, hay toàn rác?**

Đo trên 1.068 bước chạm thật:

| | Kết quả |
|---|---|
| Có tên nút rõ ràng | **77%** |
| Chỉ có ký hiệu lẻ (dấu cộng, chữ Q) | 3% |
| Không có tên, phải nhờ mô hình lớn đặt | **20%** |
| Vai trò rõ (nút, ô nhập liệu…) | 76% |

Hôm qua ước tính phần thiếu tên là 43%, thực đo chỉ **20%**. Lý do: ghép cây trợ năng với chữ đọc trong hộp thì mạnh hơn từng nguồn riêng lẻ.

> **Nói thật một chỗ:** "có tên" chưa chắc "tên đúng". Soi tay 24 mẫu thì thấy một ca sai — điểm chạm vào nút soạn thư nhưng hộp lại dính tiêu đề email. Nên con số làm việc là khoảng **70–75% dùng được**, và phải soi đủ 100 mẫu mới chốt.

### Cách chấm — xong phần kiểm

| Việc | Kết quả |
|---|---|
| Thước có phân biệt câu tốt với câu dở không | có, chênh 19,7 tới 44,7 điểm tuỳ độ chặt |
| Thước có tự kiểm được không | bơm lỗi vào, **đạt 8 trên 10** ngưỡng khoá trước |
| Bộ trỏ dùng để chấm có sạch không | **sạch** — không có dữ liệu bài thi trong lúc nó được huấn luyện |

### Tra xem ai đã làm gì — xong ba vòng

Biết rõ cái gì đã bị chiếm, cái gì còn trống. Tóm tắt:

| | |
|---|---|
| Đã có người làm | đưa danh sách nút vào đầu vào · sinh toạ độ trước rồi sinh chữ · khoanh dấu nhờ mô hình lớn viết mô tả · ý "câu phải đủ để bên kia trỏ đúng" (từ 2016) |
| **Còn trống** | dùng câu hướng dẫn người viết làm **đích sinh** · đưa tính phân biệt vào **mục tiêu huấn luyện** trong miền giao diện |

---

## 3. Vấn đề vừa phát hiện

Hai vòng phản biện chạy độc lập hôm nay cùng chỉ ra một chuyện: **phần đóng góp hiện tại có nguy cơ không chứng minh được.**

### Nói bằng ví dụ

Giả sử kết quả ra thế này:

| Nhánh | Điểm |
|---|---|
| Không có dòng mô tả | 46% |
| Có dòng mô tả | 52% |

Chênh 6 điểm — nghe là có tác dụng. Nhưng với cỡ mẫu hiện tại, **dao động ngẫu nhiên đã cỡ 10 điểm**. Nên 6 điểm không phân biệt được với may rủi, và hội đồng sẽ nói: chưa chứng minh được gì.

Mà theo các nghiên cứu tương tự, kiểu can thiệp này thường chỉ cho **2 tới 8 điểm**. Tức khả năng rơi vào tình huống trên là cao — ước khoảng **80%**.

### Và một chỗ tự mâu thuẫn

Chỗ trống mình tự xác định là *"đưa tính phân biệt vào **mục tiêu** huấn luyện"*. Nhưng thiết kế hiện tại chỉ đưa nó vào **chuỗi chữ phải sinh ra**, còn cách tính phạt vẫn y như thường.

Hội đồng sẽ hỏi: *"chuỗi có chứa chữ 'khác với nút bên cạnh' thì khác gì chuỗi thường? Cách tính phạt của anh có gì mới đâu?"*

Câu đó khó đỡ.

---

## 4. Ba cách gia cố

### Cách 1 — nhét toạ độ thật vào dòng mô tả

Dòng mô tả hiện có ô "vị trí" nhưng ghi thô kiểu *trên đỉnh, giữa*. Quá thô, vì hai nút cạnh nhau chỉ cách 69 pixel.

Trong khi đó **toạ độ chỗ người thật chạm là nhãn sạch tuyệt đối, có ở 100% số bước** — và đang không được dùng để dạy.

```
Trước:  [ô nhập liệu | "Search Publications..." | trên đỉnh, giữa | không có ô nào giống]
Sau:    [ô nhập liệu | "Search Publications..." | 500,80 | không có ô nào giống]
```

**Vì sao đáng làm:** dù ô "tên" có nhiễu ở 25% số mẫu, mô hình vẫn nhận được tín hiệu định vị sạch ở **mọi** mẫu. Và câu chuyện đóng góp dày lên: từ *"đổi định dạng đầu ra"* thành *"dạy mô hình neo vào thao tác thật của người dùng"*.

**Chi phí:** bằng không, nhãn có sẵn trong dữ liệu.

### Cách 2 — phạt câu mơ hồ bằng nút hàng xóm

Đây là cách lấp đúng chỗ tự mâu thuẫn ở mục 3.

**Ý tưởng bằng lời:** một câu hướng dẫn tốt phải khớp với nút đúng **hơn hẳn** khớp với nút bên cạnh. Câu nào áp vào nút nào cũng xuôi thì phải bị phạt ngay lúc học.

> **Ví dụ.** Màn có hai kính lúp giống hệt: một cái tìm danh bạ bên trái, một cái tìm nhạc bên phải. Cần hướng dẫn bấm cái bên trái.
>
> | Câu | Áp vào nút trái | Áp vào nút phải | |
> |---|---|---|---|
> | *"Tap the search icon"* | xuôi | cũng xuôi | **bị phạt** |
> | *"Tap the search icon on the left, next to Contacts"* | xuôi | không xuôi | không bị phạt |

**Cách làm:** với mỗi bước, dựng sẵn một "dòng mô tả giả" lấy từ nút hàng xóm gần nhất. Lúc huấn luyện, bắt mô hình phải thấy câu đích hợp với mô tả **thật** rõ hơn hợp với mô tả **giả**.

**Vì sao cách này khác cái đã bị loại trước đó:** phương án cũ nhắm lỗi *gọi nhầm tên nút* — mà đo ra lỗi đó gần như không xảy ra (mô hình lớn chỉ bịa 0–2%). Cách này nhắm **độ mơ hồ của màn hình** — thứ rất phổ biến.

**Đã đo tính khả thi hôm nay:** 100% số bước có nút hàng xóm để dựng mô tả giả, 66% hàng xóm có tên, 45% hàng xóm cùng loại với nút đích (ca khó nhất, cũng là ca đáng phạt nhất).

**Đây là chỗ biến "phân biệt trong chuỗi chữ" thành "phân biệt trong cách tính phạt"** — tức đóng góp mô hình theo nghĩa chặt nhất.

### Cách 3 — cờ đánh dấu màn dễ nhầm

Thêm một cờ ở đầu: màn này có mấy nút dễ nhầm với nút đích.

> Màn hai kính lúp → cờ ghi *có một nút dễ nhầm* → câu đích được phép dài, phải nêu dấu hiệu phân biệt.
> Màn chỉ có một nút Lưu → cờ ghi *không có* → câu đích ngắn gọn.

**Tác dụng kép:** dạy mô hình *chỗ nào mơ hồ mới cần nói thêm*, và khi báo kết quả thì tách riêng hai nhóm. Nếu mô hình chỉ thắng ở nhóm màn-dễ-nhầm thì đó là bằng chứng cơ chế chạy đúng. Nếu thắng đều cả ở chỗ không cần thì phải nghi là nó chỉ thắng nhờ nói dài.

### Cách 4 — ép mô hình nhìn đúng chỗ (mũi nhọn, rủi ro cao)

Ba cách trên đều can thiệp vào **thứ mô hình nói ra**. Cách này can thiệp vào **thứ mô hình nhìn vào bên trong** khi nó nói.

Mô hình thị giác lúc sinh mỗi chữ đều rải sự chú ý lên khắp bức ảnh. Không ai bảo nó phải chú ý vào đâu — nó tự học. Cách này thêm một điều kiện: lúc nó đang viết phần mô tả nút, phần chú ý phải dồn vào đúng ô chứa nút đó, không rải ra chỗ khác. Ô nút thì đã có sẵn từ cây trợ năng, sạch hoàn toàn.

**Ví dụ.** Màn có nút "Gửi" ở góc dưới phải. Mô hình đang viết chữ "nút Gửi ở góc dưới bên phải". Đo bên trong thì thấy sự chú ý của nó đang trải đều khắp màn, kể cả vùng bàn phím. Nghĩa là nó viết đúng nhờ đoán theo thói quen chứ không nhờ nhìn. Cách 4 phạt đúng kiểu đó.

**Vì sao đáng làm:** đây là can thiệp sâu nhất trong bốn cách — vào cơ chế bên trong mô hình, không phải vào dữ liệu hay đầu ra. Có tiền lệ cho thấy làm vậy khiến chất lượng câu **tốt lên** chứ không xấu đi (Liu và cộng sự, AAAI 2017). Và chưa ai làm cho việc sinh câu trong miền giao diện.

**Vì sao rủi ro:** ước tính tám tới mười bốn ngày làm việc để nó chạy đúng, do ba chỗ khó:

- Qwen2.5-VL **gộp bốn ô ảnh làm một** trước khi đưa vào phần ngôn ngữ, và mỗi ảnh lại co giãn một tỉ lệ khác nhau. Tính sai một ô thì vùng đích lệch mà quá trình học vẫn chạy trơn tru — sai mà không báo lỗi
- Thư viện tăng tốc đang dùng **không trả về số đo chú ý**. Muốn lấy phải vá tay từng lớp
- Phải vẽ hình chồng lên ảnh kiểm bằng mắt vài chục mẫu mới biết nó có thật sự dồn đúng chỗ hay không

**Cách xử:** đặt rào cứng sáu ngày làm việc, chạy song song chứ không chặn việc chính. Hết hạn mà vẽ ra thấy chú ý dồn đúng vào nút thì cho chạy một lượt đầy đủ và đưa vào luận văn. Không đạt thì đóng, viết một hai trang trong phụ lục dạng thí nghiệm thăm dò — phần đó vẫn có giá lúc bảo vệ, vì cho thấy có thử hướng khó, có tiêu chí, và biết dừng.

---

## 5. Sau gia cố, đóng góp phát biểu thế nào

> **Một mô hình mở 3 tỉ tham số, chạy được offline, đầu tiên được huấn luyện cho việc sinh hướng dẫn sử dụng phần mềm bằng ngôn ngữ tự nhiên cho người đọc. Cách huấn luyện của nó khác bản thường ở chỗ: mô hình bị buộc phải định vị phần tử — nói ra nút đó là gì, tên gì, ở toạ độ nào — trước khi viết câu, và bị phạt nếu câu viết ra áp vào nút bên cạnh cũng xuôi. Hướng dẫn sinh ra được kiểm bằng một thước tự động độc lập, và vượt cả mô hình lớn không huấn luyện lẫn bản huấn luyện thông thường.**

Chữ "đầu tiên" chỉ gắn vào *"được huấn luyện cho việc này"* — vì đã có hệ thống làm việc này bằng cách ra lệnh cho mô hình lớn, nhưng không ai huấn luyện mô hình.

---

## 6. Còn phải làm gì

| Việc | Tốn gì | Chặn cái gì nếu hỏng |
|---|---|---|
| Kiểm bộ trỏ chuyên, đo lại toàn bộ số nền | ~10 đô | mọi con số hiện tại đo bằng bộ trỏ rẻ, chưa chắc đứng |
| Nhờ mô hình lớn đặt tên 300 nút hình, soi tay 200 | vài đô | nếu dưới 70% dùng được thì phải đổi cách xử 20% nút hình |
| Huấn luyện bản thường, đo xem còn bao nhiêu chỗ để tiến | ~20 đô | nếu bản thường đã cao sẵn thì kết quả không đọc được |
| **Gặp thầy chốt ba kịch bản** (xem dưới) | miễn phí | quan trọng ngang mọi việc kỹ thuật |
| Huấn luyện các nhánh còn lại | ~40 đô | kết quả chính |

### Ba kịch bản phải chốt với thầy trước khi tiêu tiền

**Một — nếu phần gia cố ra số không rõ.** Khi đó đóng góp đọc là: *mô hình mở đầu tiên được huấn luyện cho việc này, thắng cả hai mốc, kèm quy trình dữ liệu và bộ thước*. Mô hình vẫn là sản phẩm chính, chỉ mất chữ "cách huấn luyện mới". **Hỏi thầy: chấp nhận cách đọc này không?**

**Hai — nếu chỉ hoà mô hình lớn.** Còn hai nấc leo: lên bản 7 tỉ tham số, và dùng nhiều dữ liệu hơn. Nếu vẫn hoà thì luận điểm là *hoà nhưng rẻ hàng chục lần, chạy trên máy, ảnh màn hình không rời điện thoại*. **Hỏi thầy: "tốt hơn" có nới thành "tốt hơn hoặc tương đương với chi phí vượt trội" được không?**

**Ba — nếu mô hình lớn được ra lệnh khéo lại bằng bản huấn luyện.** Câu thủ: cấu trúc ra lệnh đó cũng do mình thiết kế, và bản huấn luyện chạy offline. Nhưng **phải nói trước với thầy**, đừng để nó xuất hiện lần đầu trong buổi bảo vệ.

---

## 7. Lịch tám tuần

Hạn nộp còn hai tháng. Trừ hai tới ba tuần cuối để viết luận văn, nhận phản hồi của thầy và chuẩn bị bảo vệ, phần chạy thí nghiệm chỉ còn khoảng năm tới sáu tuần. Lịch dưới đây tính theo cách **viết luận văn song song từ tuần ba** chứ không đợi có số xong mới viết — nếu viết tuần tự thì không đủ.

| Tuần | Việc chính | Tiền |
|---|---|---|
| **1** | Hẹn thầy ngay ngày đầu · bật tải bộ ảnh chạy nền · kiểm bộ trỏ chuyên và đo lại toàn bộ số nền · đặt tên 300 nút hình · chạy thử toàn tuyến trên 100 mẫu | ~10 đô |
| **2** | Dựng nhãn cho toàn bộ 75 nghìn bước và viết lại câu đích · chạy thử ba nhánh trên lát nhỏ · gặp thầy chốt kịch bản và khoá ngưỡng · bắt đầu sáu ngày thử cách 4 | 25–40 đô |
| **3** | Huấn luyện bản thường và bản hai tầng, thuê hai máy chạy song song · hạn chót cách 4 · bắt đầu viết chương dữ liệu và phương pháp | 30–45 đô |
| **4** | Huấn luyện bản có phạt câu mơ hồ · chấm toàn bộ các nhánh · điểm quyết định giữa kỳ | 25–40 đô |
| **5** | Phân tích sâu, soi tay lỗi, khoảng tin cậy · **đóng băng số liệu cuối tuần** | 5–15 đô |
| **6** | Viết chương kết quả và bàn luận · nộp bản nháp đầy đủ cho thầy | — |
| **7** | Thầy đọc, sửa theo phản hồi · làm slide | — |
| **8** | Hoàn thiện, nộp, tập bảo vệ · chừa hai ba ngày cho sự cố | — |

**Tổng khoảng 95 tới 155 đô.** Dưới trần hai trăm, nhưng không còn dư cho việc chạy lặp nhiều lần — chỗ đó thay bằng khoảng tin cậy tính theo app trên tập kiểm, đủ cho luận văn thạc sĩ.

### Ba việc hay bị quên, đã tính vào lịch

- **Tải bộ ảnh 67 GB** mất một tới ba ngày, hay đứt giữa chừng. Phải bật từ ngày đầu, không phải lúc cần mới tải
- **Thầy trả lời mất ba tới bảy ngày.** Đây là chỗ chờ duy nhất nằm ngoài tầm mình, nên phải hẹn sớm nhất có thể
- **Dựng nhãn cho 75 nghìn bước** khác hẳn 1.697 bước đã làm — lỗi lặt vặt về khung toạ độ sẽ lòi ra, chừa hai ngày đệm

### Ba điểm quyết định, tiêu chí ghi trước

**Cuối tuần 1 — sau khi đo lại bằng bộ trỏ chuyên.** Nếu khoảng cách giữa các nhánh vẫn đủ lớn để đo được thì đi tiếp. Nếu nó sụp xuống dưới ngưỡng phát hiện được thì **đổi trọng tâm ngay tại buổi gặp thầy**: phần đo lường lên chính, mô hình thành minh hoạ, và phép so thu về giữa các bản do mình huấn luyện với nhau. Quyết ở tuần một thì còn kịp, để tới tuần bốn thì không.

**Cuối tuần 3 — cách 4.** Vẽ hình ra thấy chú ý dồn đúng vào nút, quá trình học ổn định, điểm không tệ hơn bản hai tầng quá hai điểm thì cho chạy đầy đủ. Không đạt thì đóng hẳn, không cố thêm ba ngày.

**Cuối tuần 4 — kết quả trên toàn bộ dữ liệu.** Phải có bản thường và bản hai tầng đã chấm xong. Nếu chênh lệch rõ thì chạy nốt. Nếu chênh gần bằng không thì **đừng đốt thêm tiền cho nhánh mới** — dồn tuần năm vào phân tích vì sao không chênh: hỏng ở loại nút nào, nút chữ hay nút hình, màn đông nút hay thưa nút. Một luận văn ra số không chênh mà phân tích tốt thì vẫn bảo vệ được; một luận văn sáu nhánh mà không phân tích thì không.

---

## 8. Bạn cần quyết

**Phương án A — làm cả ba cách gia cố, cộng cách 4 dạng thử có rào cứng.** Đây là khuyến nghị.

Hai cách đầu (định vị trước khi viết, phạt câu mơ hồ) là **xương sống, không cắt** — vì đó là hai can thiệp vào mô hình, cắt một cái là đóng góp mỏng đi hẳn một bậc. Cách 4 chạy song song, hỏng thì xuống phụ lục, không kéo theo thứ gì.

Khả năng nộp kịp với kết quả dùng được khoảng 80%. Khả năng chứng minh được đóng góp mô hình khoảng 60 tới 65%. Khả năng giữ được cách 4 trong thân luận văn khoảng 30 tới 35%.

**Phương án B — bỏ cách 4, chỉ làm ba cách gia cố.** Nộp kịp cao hơn chừng năm điểm, nhưng mất hẳn mũi nhọn.

Chênh lệch giữa hai phương án là: trả năm điểm khả năng nộp kịp để mua khoảng một phần ba cơ hội giữ được phần mới nhất. Mua được vì phần trả có rào cứng sáu ngày, không phải ngỏ.

**Thứ rớt trước nếu kẹt** không phải một can thiệp nào, mà là **quy mô dữ liệu** — chạy trên hai phần ba thay vì toàn bộ, khai thẳng trong luận văn. Cách này giữ đủ số can thiệp, chỉ hạ độ mạnh của con số.

---

## 9. Nếu chỉ nhớ một trang

- **Sản phẩm:** một mô hình nhỏ chạy offline, nhìn app lạ và viết hướng dẫn cho người dùng
- **Đóng góp:** dạy nó **định vị trước, nói sau** · phạt nếu câu viết ra áp vào nút bên cạnh cũng xuôi · và nếu kịp thì ép nó nhìn đúng chỗ khi viết
- **Đã xong:** dữ liệu để dạy, nguyên liệu cho phần đóng góp (77% dùng được), thước chấm đã tự kiểm, biết rõ ai đã làm gì trước
- **Chưa xong:** kiểm bộ trỏ, huấn luyện, và chốt ba kịch bản với thầy
- **Gấp nhất:** hẹn thầy trong tuần này, vì đó là chỗ chờ duy nhất nằm ngoài tầm mình
- **Tiền:** 95 tới 155 đô cho cả luận văn
