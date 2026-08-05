# Pipeline mô hình

> Tài liệu này chỉ nói về phần mô hình: dữ liệu vào từ đâu, qua những bước xử lý nào, huấn luyện ra sao, và lúc chạy thì diễn ra thế nào. Phần cách chấm để ở `report/100`.

---

## Toàn cảnh

Pipeline có sáu khâu nối tiếp:

```
0.  Nguyên liệu          AndroidControl: ảnh màn hình + chỗ người thật chạm + câu người viết
        ↓
1.  Đọc chữ trên ảnh     bộ đọc chữ → danh sách chữ kèm vị trí
        ↓
2.  Viết lại câu đích    khoanh dấu chỗ chạm → mô hình lớn viết lại câu cho tự đủ
        ↓
3.  Dựng nhãn mô tả      hộp phần tử tại chỗ chạm + chữ trong hộp → bộ mô tả bốn trường
        ↓
4.  Ghép thành mẫu       (ảnh + mục tiêu + danh sách chữ) → (mô tả, rồi câu)
        ↓
5.  Huấn luyện           Qwen2.5-VL-3B, QLoRA
        ↓
6.  Chạy thật            ảnh + câu hỏi → mô tả → câu; cắt phần mô tả, đưa câu cho người dùng
```

Bốn khâu đầu chạy một lần trên máy cá nhân, không tốn tiền. Khâu 5 chạy trên máy thuê. Khâu 6 chạy trên điện thoại người dùng.

---

## Những mô hình có mặt trong pipeline

Có năm mô hình, mỗi cái một vai. Ba cái chỉ chạy lúc dựng dữ liệu rồi bỏ, một cái chạy lúc chấm, chỉ một cái là mô hình của luận văn.

| Tên | Vai | Mở hay đóng | Chạy khi nào | Có mặt lúc người dùng chạy |
|---|---|---|---|---|
| **Qwen2.5-VL-3B** | mô hình sinh hướng dẫn, thứ luận văn huấn luyện | mở, Apache-2.0 | huấn luyện và chạy thật | **có** |
| **RapidOCR** | đọc chữ trên ảnh | mở, chạy ONNX trên CPU | dựng dữ liệu và chạy thật | **có** |
| **Qwen2.5-VL-72B** | viết lại câu đích cho tự đủ, và đặt tên cho nút hình | mở | chỉ lúc dựng dữ liệu, một lần | không |
| **UGround** | bộ trỏ dùng để chấm | mở | chỉ lúc chấm | không |
| **gpt-4o-mini** | mốc ngoài đem so | đóng | chỉ lúc chấm | không |

### Vì sao chọn từng cái

**Qwen2.5-VL-3B** làm mô hình sinh vì bốn ràng buộc, nói kỹ ở khâu 5.

**RapidOCR** vì nó chạy trên CPU và chạy được trên điện thoại, nên không phá vỡ chuyện hệ thống chạy offline. Nếu đổi sang dịch vụ đọc chữ trên mạng thì người dùng phải gửi ảnh màn hình lên mạng, mà ảnh màn hình thường có thông tin riêng tư.

**Qwen2.5-VL-72B** làm mô hình viết lại. Ba lý do:

- Nó **mở**, nên nói được rằng không có mô hình đóng nào tham gia vào vòng huấn luyện. Đây là điểm mạnh khi bảo vệ.
- Nó **khác hẳn gpt-4o-mini**, vốn là mốc đem so. Nếu viết lại bằng chính gpt-4o-mini rồi lại lấy gpt-4o-mini làm mốc để vượt thì người ta hỏi ngay: học từ ai thì cùng lắm bằng người đó.
- Nó **cùng dòng với mô hình sinh** nên đọc ảnh giao diện theo cùng một kiểu, câu viết ra hợp với thứ mô hình 3 tỉ tham số có thể học được.

Nếu muốn khác họ hoàn toàn thì có thể thay bằng InternVL cỡ lớn. Chưa chốt cứng, nhưng ràng buộc thì cứng: **phải là mô hình mở, và phải khác gpt-4o-mini**.

**UGround** làm bộ trỏ vì nó được huấn luyện trên ảnh web chứ không đụng vào AndroidControl. Bộ trỏ phổ biến khác là OS-Atlas thì **không dùng được**, vì nó huấn luyện thẳng trên AndroidControl nên đã thấy trước các màn đem chấm.

**gpt-4o-mini** làm mốc ngoài vì nó là mô hình lớn phổ biến, sẵn có, và đã đo được điểm trên chính lát dữ liệu này.

---

## Khâu 0. Nguyên liệu

### Bộ dữ liệu

AndroidControl gồm 15.283 tác vụ trên 833 ứng dụng, do người thật thao tác trên điện thoại Pixel trong khoảng một năm. Mỗi tác vụ được cắt thành từng bước, và mỗi bước lưu lại bốn thứ: ảnh màn hình lúc đó, loại thao tác, toạ độ chỗ người chạm, và một câu hướng dẫn do chính người thao tác viết.

Câu hướng dẫn đó là thứ mô hình sẽ học viết theo.

### Cách lấy dữ liệu về

Bản gốc nằm trên hạ tầng đám mây của Google, nặng vài GB và phải cài thư viện riêng mới đọc được. Trên HuggingFace có hai bản đã trích sẵn, mỗi bản thiếu một nửa: một bản có đủ câu hướng dẫn cho cả 15.283 tác vụ nhưng không kèm ảnh, bản kia có ảnh nhưng đã chuyển sang định dạng dành cho máy nên mất hẳn câu hướng dẫn.

Ghép hai bản theo mã tác vụ và số thứ tự bước thì được đủ cả bốn thứ cần dùng.

Một chi tiết dễ tưởng là lỗi: số ảnh của một tác vụ thường nhiều hơn số bước đúng một. Đó là ảnh màn hình cuối cùng sau khi đã làm xong bước cuối, không có câu tương ứng nên bỏ qua.

### Kiểm xem ghép có đúng không

Ghép được chưa chắc đã ghép đúng, nên phải kiểm. Cách làm: với mỗi bước chạm, đọc chữ quanh chỗ người thật chạm rồi so với câu hướng dẫn của bước đó. Kèm một đối chứng là so với câu của bước kế tiếp.

Ghép đúng khớp 47%, ghép lệch một bước chỉ khớp 27%. Nếu phép ghép sai thì hai con số đã bằng nhau.

Con số 47% nghe thấp nhưng đó là cận dưới, vì phép kiểm dựa vào chữ. Câu *"chọn từ thứ Hai tới thứ Sáu"* trỏ đúng vào chữ **F** của nút thứ Sáu nhưng bị tính là không khớp.

### Một bước sau khi ghép

```json
{
  "episode_id": 5590,
  "step_id": 1,
  "image": "images/ep5590_s1.png",
  "goal": "Open Google maps app, Search for the nearest park to 98103...",
  "history": ["Open the Google Maps app"],
  "target_instruction": "Click on the search bar",
  "action": {"action_type": "click", "x": 475, "y": 219},
  "w": 1080, "h": 2400
}
```

Hiện đã dựng 1.697 bước từ hai phần chia đầu, chiếm 833 MB. Cả 76 phần chia ước 67 GB nên chỉ giữ vài phần ở máy để phát triển, phần còn lại tải thẳng trên máy thuê lúc huấn luyện.

### Các loại bước

| Loại | Tỉ lệ | Kèm theo gì |
|---|---|---|
| Chạm | 59,1% | toạ độ |
| Cuộn | 14,5% | hướng cuộn |
| Gõ chữ | 7,3% | nội dung cần gõ |
| Mở ứng dụng | 7,1% | tên ứng dụng |
| Quay lại, chờ | 12,0% | không có gì |

---

## Khâu 1. Đọc chữ trên ảnh

### Chọn công cụ

Dùng **RapidOCR** chạy trên nền ONNX. Lý do không phải vì nó đọc chính xác nhất, mà vì nó là thứ duy nhất khớp với cách hệ thống sẽ được triển khai: chạy trên CPU nên máy không có card đồ hoạ vẫn dùng được, chạy được ngay trên điện thoại, không cần mạng, không cần khoá dịch vụ, và miễn phí.

Nếu đổi sang một dịch vụ đọc chữ trên mạng thì chữ sạch hơn thật, nhưng khi đó người dùng phải gửi ảnh màn hình của mình lên mạng. Ảnh màn hình thường có thông tin riêng tư, nên đó là cái giá quá đắt cho một chút chính xác.

### Kết quả lưu lại

Mỗi dòng chữ đọc được lưu ba thứ: chữ, toạ độ tâm, và vị trí quy về lưới ba nhân ba.

```json
{"text": "Search Publications, Stories & Interest", "cx": 486, "cy": 193,
 "zone": "trên đỉnh, giữa"}
```

Ghi vị trí theo lưới thô thay vì số pixel vì hai lẽ: mô hình ngôn ngữ xử lý mô tả kiểu này tự nhiên hơn, và nó không phụ thuộc vào kích thước màn hình cụ thể.

### Đọc được tới đâu

Đo trên 1.069 bước chạm trong dữ liệu đã dựng:

| | |
|---|---|
| Số dòng chữ mỗi màn | trung vị 22 |
| Khoảng cách từ chỗ chạm tới dòng chữ gần nhất | trung vị 115 pixel |
| Có chữ ngay tại nút, trong vòng 60 pixel | 40% |
| Có chữ gần nút, trong vòng 150 pixel | 57% |
| Không có chữ nào gần | 43% |

Chữ đọc ra cũng không sạch. Vài lỗi thật gặp trong dữ liệu: `Corn syrup .nd Jam` (chữ *and* thành `.nd`), `11:35M` (mất chữ *AM*), biểu tượng kính lúp bị đọc thành `Q`, và những dòng rác kiểu `10dS.S0O`.

Con số đáng lưu ý nhất là 43% số nút cần chạm không có chữ nào ở gần. Đó là các nút hình: dấu cộng, mũi tên, biểu tượng chia sẻ, ảnh đại diện. Chuyện này ảnh hưởng trực tiếp tới khâu 3.

Danh sách nhiễu như vậy không phải sự cố cần khắc phục. Mô hình sẽ được huấn luyện với chính danh sách nhiễu đó, nên nó học luôn cả việc khi nào không nên tin danh sách.

---

## Khâu 2. Viết lại câu đích

### Vì sao phải viết lại

Câu hướng dẫn do người thao tác viết rất cụt. Trung vị chỉ 6 từ, gần nửa số câu dưới 5 từ. Nhiều câu mơ hồ như *"Tap the app"* hay *"Click on it"*, và có cả câu hỏng hẳn: *"Click on the top at the bottom right corner"*.

Mô hình học bắt chước sẽ học đúng giọng cụt đó. Mà câu cộc lốc thì chỉ trỏ trúng 35%, trong khi câu tả rõ phần tử trỏ trúng 69%. Nói cách khác, nếu dạy bằng câu gốc thì mô hình tự chặn trần của chính nó ngay từ đầu.

### Thế nào là một câu tự đủ

Người dùng chỉ nhận được đúng câu đó, không thấy mục tiêu tổng, không biết các bước trước. Nên câu phải đứng một mình được. Cụ thể là bốn điều kiện.

**Một, phải nêu ra phần tử bằng thứ người nhìn thấy được.** Chữ trên nút, hoặc hình dạng của nó, hoặc vị trí trên màn.

**Hai, không dùng từ trỏ lửng.** Không có "nó", "cái đó", "chỗ vừa nãy".

**Ba, không dựa vào bước trước.** Không có "làm tiếp", "như trên", "rồi bấm nút bên cạnh".

**Bốn, giữ nguyên hành động.** Chạm vẫn là chạm, gõ vẫn là gõ. Viết lại chỉ làm rõ *bấm vào đâu*, không đổi *làm gì*.

### Câu gốc và câu viết lại

| Vấn đề của câu gốc | Câu gốc | Câu viết lại |
|---|---|---|
| Cụt, thiếu tên nút | *Click on the search bar* | *Tap the "Search Publications, Stories & Interest" bar at the top of the screen* |
| Mơ hồ, "app" nào cũng được | *Tap the app* | *Tap the blue Zoho Meeting icon in the second row* |
| Dùng từ trỏ lửng | *Click on it* | *Tap the "SAVE & ADD ANOTHER" button at the bottom* |
| Dựa vào bước trước | *Then pick the first one* | *Tap the first article in the list, titled "Saudis to host Ukraine's peace summit"* |
| Câu hỏng, tự mâu thuẫn | *Click on the top at the bottom right corner* | *Tap the round blue "+" button at the bottom right corner* |
| Nút hình không có chữ | *Tap share* | *Tap the share icon, the arrow pointing right, at the top right* |

Nhìn cột phải sẽ thấy quy luật: câu nào cũng trả lời được câu hỏi *"tôi phải bấm vào cái gì, nó trông thế nào, nằm chỗ nào"*.

### Cách làm

Lấy toạ độ chỗ người thật chạm, khoanh một dấu tại đúng chỗ đó lên ảnh, rồi đưa ảnh có dấu cùng câu gốc cho **Qwen2.5-VL-72B**.

Lời yêu cầu đưa cho nó đại khái thế này:

```
Đây là ảnh màn hình một ứng dụng điện thoại.
Ô đỏ đánh dấu đúng phần tử mà người dùng đã chạm.
Câu hướng dẫn gốc: "Click on the search bar"

Hãy viết lại câu này cho một người lạ đọc là làm theo được ngay,
theo các quy tắc sau:
  - nêu rõ phần tử trong ô đỏ: chữ hiển thị trên nó, hoặc hình dạng nếu không có chữ
  - nêu vị trí của nó trên màn
  - giữ nguyên hành động của câu gốc (chạm thì vẫn là chạm)
  - chỉ mô tả những gì nhìn thấy trong ảnh, không suy đoán thêm
  - một câu, không giải thích
```

Lúc huấn luyện thì dùng ảnh sạch, không có ô đỏ.

### Ba điều cấm khi viết lại

Câu viết lại **không được bịa** thứ không có trên màn. Nếu nút chỉ có biểu tượng thì tả biểu tượng, đừng đoán tên chức năng.

**Không được đổi hành động.** Gốc là chạm mà viết lại thành gõ chữ thì hỏng nhãn.

**Không được kể mục tiêu tổng vào câu.** Câu *"để tìm bài về Ukraine, hãy chạm ô tìm kiếm"* là sai, vì lúc chấm mục tiêu bị giấu đi, và người dùng thật cũng chỉ cần biết bấm đâu.

Sau khi chạy xong phải soi tay khoảng một trăm câu để đếm ba loại lỗi trên.

### Vì sao cách này không phải là chép bài của mô hình lớn

Qwen-72B được cầm sẵn đáp án, vì nó thấy dấu khoanh nên biết chắc phần tử nào. Qwen-3B thì không có dấu, phải tự nhìn ảnh mà tìm ra rồi mô tả.

Thứ được truyền lại không phải năng lực định vị của Qwen-72B. Nó chỉ mô tả một chỗ đã được chỉ sẵn.

### Ba ràng buộc khi làm khâu này

Mô hình viết lại phải khác họ với mốc đem so, nên chọn Qwen-72B chứ không dùng gpt-4o-mini. Nếu viết lại bằng gpt-4o-mini rồi lại lấy chính nó làm mốc để vượt thì câu đầu tiên người ta hỏi sẽ là *học từ ai thì cùng lắm bằng người đó*.

Phải có thêm một nhánh viết lại mù ảnh: vẫn Qwen-72B, vẫn yêu cầu viết dài hơn, nhưng không cho xem ảnh và dấu. Câu ra sẽ dài tương đương nhưng không mang thông tin gì về chỗ cần chạm. Nhánh này tách được phần *biết chỗ* khỏi phần *viết dài*.

Và phải soi tay khoảng một trăm câu viết lại để đếm xem có bao nhiêu câu bịa tên phần tử.

Khâu này là xử lý dữ liệu, không tính vào phần đóng góp. Cách khoanh dấu rồi nhờ mô hình lớn viết mô tả đã có người làm trong chính miền giao diện.

---

## Khâu 3. Dựng nhãn tầng mô tả

Đây là nguyên liệu cho phần đóng góp mô hình.

### Bộ mô tả gồm bốn trường

```
[ vai trò | chữ hoặc hình | vị trí trên màn | dấu hiệu phân biệt ]
```

### Lấy từ đâu

Vai trò lấy từ loại phần tử ghi trong cây trợ năng của hệ điều hành, tại đúng hộp bao chứa điểm người chạm. Ví dụ `EditText` thành *ô nhập liệu*.

Chữ lấy từ những dòng bộ đọc chữ trả về nằm bên trong hộp đó. Nếu hộp không có chữ nào thì phải mô tả bằng hình.

Vị trí quy hộp về lưới ba nhân ba, thành *trên đỉnh, giữa* hoặc *dưới đáy, bên phải*.

Dấu hiệu phân biệt là câu ngắn ghi lại có phần tử nào khác cùng vai trò hoặc cùng chữ nằm gần không, ví dụ *có một kính lúp nữa bên phải*.

Cây trợ năng có sẵn cho 99.131 màn, mỗi màn trung vị 62 tới 86 phần tử hiển thị, hộp bao rất đầy đủ.

### Chạy tốt và chạy hỏng

| Nút cần chạm | Bộ mô tả dựng ra | |
|---|---|---|
| Ô tìm kiếm có chữ | `[ô nhập liệu \| "Search Publications, Stories & Interest" \| trên đỉnh, giữa \| không có ô nào giống]` | dùng được |
| Kính lúp không chữ | `[nút \| ? \| trên đỉnh, bên phải \| ...]` | rỗng phần tên |
| Dấu cộng | `[nút \| "+" \| dưới đáy, bên phải \| ...]` | đọc được ký tự nhưng không biết nghĩa là thêm mới |

### Chỗ khó nhất của cả pipeline

Ghép hai con số đã đo lại với nhau:

Cây trợ năng cho hộp bao rất đầy đủ nhưng chỉ 12,6% phần tử có tên. Bộ đọc chữ thì phủ được 57% số bước chạm. Cộng lại, còn khoảng 43% số bước chạm không lấy được tên từ nguồn nào cả.

Tầng mô tả mà rỗng phần tên thì hai tầng còn tệ hơn một tầng, vì mô hình chẳng có gì để chép mà lại bị dẫn sai.

### Cách xử phần nút hình

Với những nút không có chữ, cắt vùng ảnh trong hộp đó ra rồi nhờ **Qwen2.5-VL-72B** đặt tên ngắn gọn, kiểu *biểu tượng kính lúp* hay *dấu cộng*. Việc này chạy một lần lúc dựng dữ liệu.

Phần này chưa ai kiểm nên chưa biết chạy có ổn không. Đây là việc miễn phí phải làm trước tiên: dựng thử nhãn tầng mô tả trên vài trăm bước rồi soi tay đếm xem bao nhiêu phần trăm dùng được. Nếu tỉ lệ quá thấp thì phần đóng góp không chạy được, và biết sớm vẫn hơn biết sau khi đã tiêu hết ngân sách.

---

## Khâu 4. Ghép thành mẫu huấn luyện

### Một mẫu hoàn chỉnh

```
──────── ĐẦU VÀO ────────
[ảnh màn hình của bước đó, ảnh sạch không có dấu khoanh]

Mục tiêu: Vào app PressReader và tìm bài "Saudis to host Ukraine's peace summit"
Đã làm:   chưa có bước nào
Chữ nhìn thấy trên màn:
  - "Search Publications, Stories & Interest"   (trên đỉnh, giữa)
  - "Recommended"                               (giữa màn, bên trái)
  - "See all"                                   (giữa màn, bên phải)
  - "THE WALL STREET JOURNAL."                  (giữa màn, bên trái)
  ...

Hãy viết hướng dẫn cho bước tiếp theo.

──────── ĐÍCH ────────
[ô nhập liệu | "Search Publications, Stories & Interest" | trên đỉnh, giữa | không có ô nào giống]
Tap the "Search Publications, Stories & Interest" bar at the top
```

### Ba chỗ cần để ý trong mẫu này

Ảnh là ảnh sạch. Dấu khoanh chỉ tồn tại ở khâu 2, lúc mô hình lớn viết lại câu. Mô hình học không bao giờ nhìn thấy dấu.

Phần mô tả nằm ở phía đích chứ không phải phía đầu vào. Mô hình phải tự sinh ra phần đó, không ai đưa cho nó.

Toạ độ đúng không xuất hiện ở đâu trong mẫu. Nó chỉ được dùng ở khâu 2 và khâu 3 để dựng nhãn, sau đó biến mất.

### Mô hình học được gì từ những mẫu này

Sau hàng nghìn mẫu, cái nó rút ra là: nhìn ảnh này với mục tiêu này thì phần tử cần chạm thuộc loại gì, tên gì, nằm ở đâu, và có gì dễ nhầm với nó. Đó là kỹ năng nó tự hình thành, không phải thông tin ai đưa cho.

---

## Khâu 5. Huấn luyện

### Mô hình nền

Qwen2.5-VL-3B, mô hình ảnh và ngôn ngữ mở, giấy phép Apache-2.0. Bốn ràng buộc dẫn tới lựa chọn này.

Phải là mô hình mở, vì đề tài buộc tự huấn luyện và hệ thống phải chạy được offline. Mô hình đóng thì không fine-tune được, cũng không chạy trên máy người dùng.

Phải đủ nhỏ, vì máy thuê chỉ có một card 24GB. Bản 3 tỉ tham số kết hợp QLoRA vừa khít.

Phải đọc được ảnh dày chữ. Qwen2.5-VL xử lý ảnh độ phân giải cao, chỗ mà nhiều mô hình nhỏ khác đuối vì nén ảnh làm mất chữ trên nút.

Và phải có tiền lệ cùng miền cùng cỡ, để giảm rủi ro. Nhiều mô hình giao diện gần đây dựng thẳng trên Qwen2.5-VL cỡ 3 tỉ và chạy được.

### Cách huấn luyện

Dùng QLoRA: giữ nguyên phần lớn mô hình gốc ở dạng nén, chỉ chỉnh một lượng nhỏ tham số thêm vào. Nhờ vậy vừa một card thuê rẻ.

Dự kiến đóng băng phần thị giác, chỉ chỉnh phần ngôn ngữ và lớp nối giữa hai phần. Hàm mất mát là cross entropy trên từng chữ của phần đích, tính cả phần mô tả lẫn phần câu.

### Một chuyện kỹ thuật phải quyết trước

Ảnh màn hình điện thoại rất cao, 1080 nhân 2400. Qwen2.5-VL cắt ảnh thành nhiều mảnh nhỏ để xử lý, ảnh càng lớn thì càng chiếm nhiều chỗ trong chuỗi đầu vào.

Giữ ảnh lớn thì đọc được chữ trên nút nhỏ nhưng chuỗi dài, huấn luyện chậm và tốn. Thu nhỏ ảnh thì nhanh hơn nhưng mất chữ nút, đúng chỗ tác vụ này cần nhất. Phải thử vài mức trước khi chạy thật.

### Chi phí

Một lượt huấn luyện ước 6 tới 10 giờ card A100. Bốn nhánh cộng lại khoảng 40 đô. Cổng kiểm bộ trỏ khoảng 10 đô. Phần viết lại câu đích và đặt tên nút hình ước 15 tới 40 đô, chạy một lần.

---

## Khâu 6. Lúc chạy thật

```
Người dùng đưa: một ảnh màn hình + một câu hỏi
        │
        ├──→ [bộ đọc chữ] ──→ danh sách chữ kèm vị trí
        │                            │
        └────────────────────────────┴──→ [Qwen-3B đã huấn luyện]
                                                │
                                                ▼
              [ô nhập liệu | "Search Publications..." | trên đỉnh, giữa | ...]
              Tap the "Search Publications..." bar at the top
                                                │
                                      cắt bỏ dòng mô tả
                                                ▼
                                 người dùng nhận: câu hướng dẫn
```

Trên máy người dùng chỉ cần hai thứ: bộ đọc chữ và mô hình. Không cần mạng, không phải gửi ảnh đi đâu.

Những thứ không cần lúc chạy: toạ độ đúng, cây trợ năng, Qwen-72B, UGround. Chúng chỉ tồn tại lúc dựng dữ liệu và lúc chấm.

Nếu mô hình mô tả sai thì câu cũng sai theo, kiểu nhìn nhầm sang nút bên cạnh rồi hướng dẫn bấm nút đó. Cách phát hiện là so phần mô tả mô hình sinh ra với nhãn đã dựng sẵn rồi đếm tỉ lệ nêu đúng phần tử. Nếu tỉ lệ đó thấp mà điểm câu vẫn cao thì phải giải thích được.

---

## Bốn nhánh khác nhau ở đâu

Cả bốn dùng chung mô hình nền, chung cách huấn luyện, chung dữ liệu. Chỉ khác hai chỗ: câu đích lấy từ đâu, và mô hình phải sinh ra những gì.

| Nhánh | Câu đích lấy từ | Phải sinh ra | Vai |
|---|---|---|---|
| Huấn luyện thường | câu người viết, nguyên bản | chỉ câu | mốc trong |
| Trên câu viết lại | câu viết lại có xem ảnh | chỉ câu | nền dữ liệu |
| Trên câu viết lại mù | câu viết lại không xem ảnh | chỉ câu | đối chứng độ dài |
| Hai tầng | câu viết lại có xem ảnh | mô tả rồi câu | phần đóng góp |

Phần đóng góp mô hình đo ở hiệu số giữa nhánh cuối và nhánh thứ hai. Hai nhánh đó cùng dữ liệu, cùng giọng văn, chỉ khác việc mô hình có phải nói ra phần mô tả trước khi viết câu hay không.

---

## Những chỗ chưa chốt

| Chỗ | Phải làm gì | Tốn gì |
|---|---|---|
| Chất lượng nhãn tầng mô tả | dựng thử vài trăm bước rồi soi tay | miễn phí, làm trước tiên |
| Mức thu nhỏ ảnh | thử vài mức, xem có mất chữ nút không | rẻ |
| Chốt cứng mô hình viết lại | Qwen2.5-VL-72B hay InternVL cỡ lớn, miễn là mở và khác gpt-4o-mini | chỉ là quyết định |
| Định dạng chính xác của bộ mô tả | bốn trường viết liền hay xuống dòng, ký hiệu ngăn cách | thử lúc dựng |
| Còn bao nhiêu chỗ để tiến | huấn luyện bản thường trước rồi đo | khoảng 20 đô |

---

Toàn bộ pipeline này phục vụ đúng một việc: dạy mô hình nói ra phần tử là cái gì trước khi hướng dẫn bấm nó. Năm khâu phía trước tồn tại để tạo ra nhãn cho việc dạy ấy.
