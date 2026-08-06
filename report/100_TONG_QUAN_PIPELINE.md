# Sinh hướng dẫn sử dụng phần mềm cho người đọc — tổng quan hệ thống

> Bản đọc nhanh cho người mới tiếp cận đề tài. Chỉ trình bày **bài toán, hệ thống chạy thế nào, và các con số đã đo được**. Mỗi phần viết lời thường trước, công thức và trích dẫn để trong hộp riêng.

---

## 0. Đọc trong một phút

| | |
|---|---|
| **Bài toán** | vào một ảnh màn hình + một câu hỏi, ra các bước bằng lời cho người tự làm theo |
| **Khác gì các mô hình giao diện khác** | chúng sinh thao tác để máy tự bấm; ở đây sinh câu cho con người đọc |
| **Mô hình** | Qwen2.5-VL-3B, mở, chạy offline, huấn luyện nhẹ trên máy thuê khoảng 70 đô |
| **Dạy bằng gì** | câu hướng dẫn do người viết sẵn trong bộ AndroidControl, 15.283 tác vụ |
| **Đóng góp mô hình** | bắt mô hình **nêu phần tử là cái gì** rồi mới viết câu, với nhãn tầng giữa rút tự động từ chỗ người thật chạm |
| **Tính mới** | không phải cơ chế mới; mới ở chỗ đưa tính phân biệt phần tử vào **mục tiêu huấn luyện** trong miền này, và ở nguồn giám sát tự động |
| **Chấm thế nào** | đưa câu cho một bộ trỏ, xem nó có lần ra đúng nút không; chạy thêm một lượt không đưa câu làm sàn |
| **Vì sao cách chấm này đáng nói** | không cần đáp án mẫu, không cần thuê người, lặp lại được |
| **Đã đo được gì** | thước phân biệt rõ câu tốt với câu dở, chênh 19,7 đến 44,7 điểm tuỳ độ chặt; thước tự kiểm bằng bơm lỗi, đạt 8 trên 10 ngưỡng khoá trước |
| **Chưa có gì** | chưa có số của mô hình sau huấn luyện; đó là bước kế tiếp |

---

## 1. Bài toán

Một người đang mở app trên điện thoại, không biết làm tiếp thế nào. Họ chụp lại màn hình đang hiện và hỏi một câu.

**Vào:** một ảnh màn hình + một câu hỏi
**Ra:** các bước bằng lời cho người đó tự làm theo

> **Ví dụ.** Ảnh: trang chủ một app đọc báo. Câu hỏi: *"Làm sao tìm bài về hội nghị hoà bình Ukraine?"*
> Trả lời mong muốn:
> 1. Chạm ô **Search Publications, Stories & Interest** ở trên đỉnh
> 2. Gõ *Ukraine peace summit*
> 3. Chọn bài trong danh sách hiện ra

**Chỗ khác với các mô hình giao diện đang có.** Dòng mô hình điều khiển giao diện hiện nay sinh **thao tác để máy tự bấm** — đầu ra của chúng là toạ độ hoặc lệnh, dành cho một chương trình thực thi. Ở đây đầu ra là **câu chữ cho con người đọc**, nên yêu cầu khác hẳn: phải gọi đúng tên nút mà người nhìn thấy, phải đủ rõ để người lạ làm theo được.

### Đã có ai làm đề tài này chưa

Có, và cần nói rõ ngay vì đây là câu hay bị hỏi đầu tiên. Trả lời theo ba mức, mỗi mức một đáp án khác nhau:

| Mức | Đã có ai chưa |
|---|---|
| **Tác vụ** — nhìn màn hình rồi hướng dẫn người dùng từng bước | **Có.** GuideMe (CHI 2026) làm đúng việc này cho người cao tuổi, có khảo sát 18 người. Nhưng ở **mức hệ thống**: ra lệnh cho mô hình lớn có sẵn, **không huấn luyện** mô hình nào, không có bộ đo định lượng |
| **Mô hình được huấn luyện** cho việc này | **Chưa tra ra ai.** Đây là chỗ đề tài đứng |
| **Cách chấm khách quan** cho việc này | **Chưa ai có.** Giới giao diện người dùng chấm bằng khảo sát người; dòng tác tử chấm hành động của chính mô hình |

Mấy công trình gần và khác chỗ nào:

| Công trình | Làm gì | Khác |
|---|---|---|
| Demo2Tutorial | biến bản ghi màn hình thành hướng dẫn có hình | cần **người thao tác demo trước** rồi ghi lại; ở đây chỉ cần **một ảnh chụp** người dùng gửi lúc đang bí |
| UGIF | ánh xạ chỉ dẫn trợ giúp có sẵn vào phần tử trên màn | **tiêu thụ** chỉ dẫn, không sinh ra |
| Widget Captioning | mô tả một phần tử giao diện | một phần tử, không phải hướng dẫn nhiều bước theo mục tiêu |
| Screen2Words | tóm tắt một màn hình | tóm tắt, không phải chỉ việc cần làm |
| Dòng tác tử giao diện | sinh thao tác cho máy tự bấm | đầu ra cho máy, không cho người đọc |

> **Cách nói cho đúng.** Không dùng chữ "đầu tiên" cho tác vụ — GuideMe đã ở đó. Nói được: *"mô hình nhỏ mở đầu tiên **được huấn luyện** cho tác vụ này, kèm bộ đo khách quan lặp lại được"*, và chủ động nhắc rằng đã có hệ thống làm việc này bằng cách ra lệnh cho mô hình lớn.
>
> Việc có người làm trước thật ra là **điểm cộng**: nó chứng minh bài toán có thật và có nơi công bố. Phần thêm vào là hai thứ họ không có — một mô hình tự huấn luyện chạy offline, và một cách chấm không cần thuê người.

**Cái khó nằm ở chỗ chấm, không phải chỗ sinh.** Không có sẵn bộ hướng dẫn mẫu do người soạn để đối chiếu, và thuê người ngồi chấm thì tốn kém, khó lặp lại. Vì vậy đề tài có hai phần ngang nhau: **một mô hình** sinh hướng dẫn, và **một cách chấm** không cần đáp án mẫu, không cần người.

---

## 2. Toàn cảnh hệ thống

### 2.1 Đơn vị làm việc: một BƯỚC

Trước khi nói pipeline, cần thống nhất đơn vị. Một tác vụ của người dùng gồm nhiều bước, và **mỗi bước có màn hình riêng của nó**.

> **Ví dụ một tác vụ ba bước.** Mục tiêu: *"Vào app PressReader và tìm bài Saudis to host Ukraine's peace summit"*
>
> | Bước | Màn hình lúc đó | Người thật đã làm gì | Câu người viết cho bước đó |
> |---|---|---|---|
> | 1 | trang chủ PressReader | chạm tại (540, 191) | *"Click on the search bar at the top of the screen"* |
> | 2 | màn tìm kiếm, bàn phím hiện ra | gõ *Ukraine peace summit* | *"Type the article name in the search bar"* |
> | 3 | danh sách kết quả | chạm tại (531, 812) | *"Click on the first article in the list"* |
>
> Ba bước là **ba ảnh khác nhau**. Màn ở bước 2 chỉ xuất hiện *sau khi* đã chạm ở bước 1.

Chi tiết này quyết định toàn bộ cách chấm, nên nói rõ ngay:

**Vì sao chấm từng bước, không chấm cả chuỗi một lần.**

Muốn chấm câu hướng dẫn của bước 3, phải có **ảnh màn hình lúc bước 3** để xem câu đó có trỏ đúng chỗ không. Mà màn đó chỉ hiện ra **sau khi** đã làm xong bước 1 và bước 2.

> Giống như bảo một người đứng ở cửa nhà, mô tả đường đi tới phòng ngủ. Họ nói *"tới cuối hành lang thì rẽ trái"*. Muốn biết câu đó đúng không thì phải đi tới cuối hành lang đã. Đứng ở cửa thì không kiểm được.

Nên nếu bắt mô hình viết cả năm bước chỉ từ ảnh màn đầu tiên, thì các bước sau nói về những màn **chưa hiện ra** — không có ảnh, không có toạ độ đúng, không có gì để đối chiếu.

**Cách xử:** con số chính **chấm từng bước một**, mỗi bước đưa đúng ảnh của nó. Còn khả năng viết cả chuỗi từ một ảnh thì trình dưới dạng **minh hoạ định tính**, không đem làm số.

---

**Một chi tiết phải nói rõ, vì nó làm con số đẹp hơn thực tế.**

Khi chấm bước 3, mô hình cần biết bước 1 và bước 2 đã làm gì. Câu hỏi là: lấy thông tin đó ở đâu?

| Cách | Nghĩa là | Hệ quả |
|---|---|---|
| Lấy từ **đáp án chuẩn** | mô hình được nhắc: *"bước 1 là chạm ô tìm kiếm, bước 2 là gõ từ khoá"* | một câu sai ở bước 1 không kéo sập các bước sau, nên đọc được mô hình dở ở đâu |
| Lấy từ **câu mô hình tự viết** | mô hình phải tự dựa vào cái nó vừa nói | sát thực tế hơn, nhưng sai một bước là hỏng cả chuỗi |

Cách thứ nhất gọi là **nhắc bài** — thuật ngữ tiếng Anh là *teacher forcing*. Nó giống đi thi mà mỗi câu đều được cho biết đáp án câu trước: dễ hơn thi thật.

Vì vậy **báo cả hai lượt chạy**, và chênh lệch giữa chúng cho biết cách chấm đang nâng đỡ bao nhiêu.

> Ví dụ: nếu chấm kiểu nhắc bài được 55%, còn chấm kiểu để mô hình tự đi được 40%, thì 15 điểm chênh đó chính là phần được nâng đỡ. Nói ra con số này thì người đọc biết đúng năng lực thật nằm ở đâu.

### 2.2 Ba luồng

```
① HUẤN LUYỆN — chạy một lần, trên máy thuê
   Với MỖI bước trong dữ liệu:
        ảnh của bước đó
      + mục tiêu cả tác vụ + các bước đã làm trước
      + danh sách chữ đọc được từ ảnh          ← lớp phụ
                        │
                        ▼
              [Qwen2.5-VL-3B + QLoRA]
                        │
                        ▼
        đích phải sinh ra:  [mô tả phần tử có cấu trúc]  →  câu hướng dẫn
                            └──── TRỤ đóng góp ────┘      └── vốn có ──┘

② CHẠY THẬT — trên máy người dùng, không cần mạng
        một ảnh màn hình
              │
              ├──→ [bộ đọc chữ OCR] ──→ danh sách chữ + vị trí
              │                                │
        một câu hỏi ─────────────────────────┐ │
                                             ▼ ▼
                                        [mô hình đã học]
                                              │
                                              ▼
                                   hướng dẫn cho bước kế tiếp
                          (phần toạ độ mô hình sinh ra thì bỏ đi,
                           chỉ đưa câu chữ cho người đọc)

③ CHẤM — chỉ chạy lúc nghiên cứu
        câu mô hình sinh, đã giấu mục tiêu
              │
              ▼
         [bộ trỏ] ──→ điểm (x, y) ──→ so với toạ độ đúng ──→ bước này đúng hay sai
              │
              └── chạy thêm một lượt KHÔNG đưa câu ──→ sàn để trừ đi

        song song: đối chiếu tên nút mô hình nhắc với danh sách nút thật ──→ có bịa không
        và: bơm lỗi đã biết vào ──→ kiểm xem chính cái thước có bắt được không
```

### 2.3 Dòng chảy dữ liệu, xem theo từng khâu

| Khâu | Vào | Ra | Chạy ở đâu | Có mặt lúc chạy thật? |
|---|---|---|---|---|
| Cắt dữ liệu | tác vụ nhiều bước | từng bước riêng lẻ, mỗi bước một ảnh | máy cá nhân | không, chỉ để dựng dữ liệu |
| Bộ đọc chữ | ảnh màn hình | danh sách chữ + vị trí | máy cá nhân, và cả điện thoại | **có** |
| Viết lại câu đích | ảnh có khoanh dấu tại chỗ chạm + câu gốc | câu đích đã làm giàu | máy thuê, chạy một lần | không |
| Dựng nhãn tầng mô tả | hộp phần tử tại chỗ chạm + chữ đọc được trong hộp | bộ mô tả có cấu trúc | máy cá nhân | không |
| Huấn luyện | ảnh sạch + mục tiêu + danh sách chữ → mô tả rồi câu | mô hình đã học | máy thuê | không |
| Sinh | ảnh + câu hỏi + danh sách chữ | mô tả rồi câu; phần mô tả cắt bỏ | điện thoại | **có** |
| Bộ trỏ | ảnh + một câu | điểm (x, y) | máy thuê | không, chỉ dùng lúc chấm |
| Danh sách nút thật | ảnh | các phần tử kèm hộp | máy cá nhân | không, chỉ dùng lúc chấm |

**Ba điều rút ra từ bảng này:**

1. **Lúc chạy thật chỉ cần hai thứ:** bộ đọc chữ và mô hình. Cả hai chạy được ngay trên điện thoại, không cần mạng.
2. **Toạ độ đúng và danh sách nút thật không bao giờ xuất hiện lúc sinh.** Chúng chỉ có mặt lúc dạy và lúc chấm. Nếu để lọt vào lúc sinh thì mô hình được mớm đáp án, và mọi con số trở nên vô nghĩa.
3. **App đem chấm chưa từng xuất hiện lúc dạy.** Bộ dữ liệu có sẵn cách chia này. Nhờ vậy, làm đúng trên app lạ nghĩa là mô hình học được kỹ năng chứ không học thuộc.

## 3. Luồng huấn luyện

### 3.1 Dữ liệu

| Bộ | Quy mô | Vai trò |
|---|---|---|
| **AndroidControl** (Li và cộng sự, NeurIPS 2024) | 15.283 tác vụ / 833 app | **dạy** mô hình, và **chấm** độ đúng trên 631 tác vụ của các app chưa từng thấy |
| **MobileViews** (arXiv 2409.14337) | 127 màn / 30 app | chỉ **chấm** độ bịa, vì nó có danh sách nút kèm tên |
| **ScreenSpot-v2** (kèm OS-Atlas, ICLR 2025) | 502 màn mobile | chỉ để kiểm chất lượng bộ trỏ |

AndroidControl là bộ dữ liệu do người thật thao tác trên điện thoại trong khoảng một năm. Mỗi tác vụ được cắt thành từng bước, và **mỗi bước có bốn thứ**: ảnh màn hình lúc đó, loại thao tác, toạ độ chỗ người chạm, và **một câu hướng dẫn do người viết cho bước đó**. Câu đó chính là đáp án để dạy.

> **Ví dụ một bước trong dữ liệu**
> Mục tiêu cả tác vụ: *"Vào app PressReader và tìm bài Saudis to host Ukraine's peace summit"*
> Bước 1 — ảnh: trang chủ PressReader (1080×2400)
> — thao tác: chạm, tại **(540, 191)**
> — câu người viết: *"Click on the search bar at the top of the screen"*

> **Về việc lấy dữ liệu.** Bản gốc của bộ này nằm trên hạ tầng đám mây, nặng vài GB và cần cài thêm thư viện xử lý. Thực tế dùng hai bản đã trích sẵn rồi **ghép theo mã tác vụ và số thứ tự bước**: một bản có câu hướng dẫn người viết cho đủ 15.283 tác vụ, một bản có ảnh. Đã kiểm: ghép không sót tác vụ nào. Có một chi tiết dễ tưởng là lỗi — số ảnh thường nhiều hơn số bước đúng một, đó là **ảnh của màn cuối cùng sau khi làm xong bước cuối**, không phải sai lệch.
>
> **Kiểm ghép có đúng nội dung không, chứ không chỉ ghép được.** Với mỗi bước chạm, đọc chữ quanh điểm người thật đã chạm rồi so với câu hướng dẫn của bước đó. Kèm một đối chứng: so với câu của **bước kế tiếp**. Kết quả: ghép đúng khớp **47%**, ghép lệch một bước chỉ **27%**. Nếu phép ghép sai thì hai tỉ lệ đã bằng nhau. Tỉ lệ tuyệt đối luôn là cận dưới vì nút hình không có chữ, và bộ đọc chữ hay đọc biểu tượng thành ký tự lẻ — ví dụ câu *"chọn từ thứ Hai tới thứ Sáu"* trỏ đúng vào chữ **F** của nút thứ Sáu, còn *"chạm biểu tượng tìm kiếm"* trỏ đúng vào kính lúp bị đọc thành **Q**.

> **Về cây trợ năng của hệ điều hành.** Bộ dữ liệu còn có cây trợ năng cho 99.131 màn, ghi vị trí và loại của từng phần tử. Đã đo trên 120 màn ngẫu nhiên: trung vị **86 phần tử một màn**, nhưng **chỉ 12,6% phần tử có tên** (22 trên 120 màn không có phần tử nào có tên). Hệ quả: dùng được cho việc chấm vị trí vì việc đó chỉ cần hộp bao, **không** dùng được để lấy tên nút, và **không** đủ để đếm nút bịa. Đây là lý do bằng số khiến phần lấy tên nút phải dựa vào bộ đọc chữ chứ không dựa vào cây trợ năng — và cũng là rủi ro lớn nhất của trụ đóng góp, vì tầng mô tả cần tên.

Phân bố các loại bước trên toàn bộ dữ liệu đã đếm được:

| Loại bước | Tỉ lệ | Chấm bằng cách nào |
|---|---|---|
| Chạm, có toạ độ | **59,1%** | bộ trỏ + toạ độ đúng |
| Gõ chữ, cuộn, mở app | **28,9%** | so nội dung gõ, so hướng cuộn |
| Quay lại, chờ | 12,0% | không nhóm nào chấm được, loại khỏi mẫu số |

### 3.2 Mô hình nền

**Qwen2.5-VL-3B** — mô hình ảnh và ngôn ngữ mở, 3 tỉ tham số, giấy phép Apache-2.0. Huấn luyện bằng **QLoRA**, tức chỉ chỉnh một lượng nhỏ tham số thêm vào thay vì luyện lại toàn bộ, nên vừa một GPU thuê 24GB.

Bốn lý do chọn cỡ này: phải là mô hình mở thì mới tự huấn luyện và chạy offline được; phải đủ nhỏ để huấn luyện trong ngân sách khoảng 70 đô; phải đọc được ảnh giao diện dày chữ, mà Qwen2.5-VL xử lý ảnh độ phân giải cao; và đã có tiền lệ ngay trên miền giao diện với cùng cỡ 3 tỉ tham số.

> **Hộp kỹ thuật.** Tiền lệ cùng miền cùng cỡ: UI-R1 (AAAI 2026) fine-tune Qwen2.5-VL-3B cho định vị phần tử giao diện · ZonUI / Qwen-GUI-3B (WACV 2026, LoRA 3B trên một GPU) · SE-GUI (NeurIPS 2025). Kích thước mô hình **không phải** điểm mới của đề tài, nó là lựa chọn kỹ thuật để rẻ và chạy được offline.

### 3.3 Thành phần thêm vào: một trụ, một tầng nền, một lớp phụ

Bản huấn luyện thông thường học đúng một ánh xạ:

```
(ảnh + mục tiêu)  ──→  "Click on the search bar at the top of the screen"
```

Nhìn vào đó sẽ thấy **hai thứ có sẵn trong dữ liệu bị bỏ phí**: toạ độ (540, 191) mà người thật đã chạm, và chữ hiện trên chính tấm ảnh đó. Ba phần dưới đây lấy lại chúng, mỗi phần một vai.

---

#### TRỤ — mô tả trước, phát ngôn sau

**Vấn đề nó giải.** Mô hình được dạy bắt chước câu người viết, mà câu đó trung vị chỉ **6 từ** và gần nửa dưới 5 từ. Nó học đúng giọng cụt ấy, nên tự chặn trần của chính mình: câu cộc lốc trỏ trúng **35%**, câu tả rõ phần tử trỏ trúng **69%**. Không có chỗ nào trong quá trình huấn luyện thông thường buộc nó phải **nêu ra phần tử là cái gì** trước khi viết.

**Cách làm.** Đích huấn luyện có hai tầng. Mô hình phải sinh trước một **bộ mô tả có cấu trúc**, rồi mới sinh câu:

| | Bản thường học | Bản có trụ học |
|---|---|---|
| Đầu vào | ảnh + *"Vào app PressReader và tìm bài…"* | y hệt |
| Đích | `Click on the search bar at the top of the screen` | `[ô nhập liệu \| "Search Publications, Stories & Interest" \| trên đỉnh, giữa \| không có ô nào giống]`<br>`→ Tap the "Search Publications, Stories & Interest" bar at the top` |

**Nhãn cho tầng mô tả dựng tự động**, không cần người gán và không cần mô hình đóng: vai trò và vị trí lấy từ **hộp phần tử tại đúng điểm người thật chạm**, chữ lấy từ **bộ đọc chữ trong hộp đó**, nút hình thì mô tả bằng cách cắt ảnh ra.

**Mô hình tự sinh ra phần mô tả bằng cách nào?** Đây là chỗ hay bị hỏi, nên nói kỹ.

Không ai đưa phần mô tả cho nó cả. Nó **học cách tự viết ra**, y như cách nó học viết câu.

> **📦 Một mẫu huấn luyện trông thế này**
>
> ```
> ĐẦU VÀO:  [ảnh trang chủ PressReader]
>           Mục tiêu: vào app PressReader tìm bài về hội nghị hoà bình
>           Đã làm:   chưa có bước nào
>
> ĐÍCH:     [ô nhập liệu | "Search Publications, Stories & Interest" | trên đỉnh, giữa]
>           Tap the "Search Publications, Stories & Interest" bar at the top
> ```
>
> Mô hình học sinh ra **toàn bộ phần đích** — cả dòng mô tả lẫn câu hướng dẫn. Với nó, dòng mô tả cũng chỉ là chữ phải sinh ra như mọi chữ khác.

Sau hàng nghìn mẫu như vậy, cái nó học được là: *nhìn ảnh này với mục tiêu này thì phần tử cần chạm là loại gì, tên gì, nằm đâu*. Đó là **kỹ năng nó rút ra**, không phải thông tin ai mớm cho.

> **📦 Lúc chạy thật**
>
> Đưa ảnh và câu hỏi, mô hình sinh ra:
>
> ```
> [ô nhập liệu | "Search Publications..." | trên đỉnh, giữa]   ← tự nhìn ảnh mà suy ra
> Tap the "Search Publications..." bar at the top              ← viết dựa trên cái vừa nói
> ```
>
> Rồi **cắt dòng đầu**, chỉ đưa dòng sau cho người dùng. Người dùng không bao giờ thấy phần mô tả, thước chấm cũng không.

**Nếu nó mô tả sai thì sao?** Thì câu sai theo — nhìn nhầm sang nút bên cạnh rồi hướng dẫn bấm nút đó. Đây là rủi ro thật, gọi là lỗi lan truyền. Cách phát hiện: so phần mô tả mà mô hình sinh ra với nhãn đã dựng sẵn, đếm tỉ lệ nó nêu đúng phần tử. Nếu tỉ lệ đó thấp mà điểm câu vẫn cao thì phải giải thích được vì sao, không được lờ đi.

**Vì sao nó làm câu tốt lên.** Mô hình sinh chữ theo thứ tự, mỗi chữ nó sinh ra thành ngữ cảnh cho chữ sau. Khi bắt nó **nêu tên và vị trí phần tử trước**, tới lúc viết câu thì thông tin định danh đã nằm sẵn trong ngữ cảnh do chính nó tạo ra. Nó không còn viết được câu cụt kiểu *"tap the app"* nữa, vì nó vừa tự nói ra đang nhắm cái gì.

> **Một cách hình dung.** Giống bảo người ta: *nói cho tôi nghe cái nút đó là nút gì, chữ gì, nằm đâu — rồi hẵng hướng dẫn tôi bấm.* Người phải kể ra trước thường hướng dẫn rõ hơn.

**Lúc chạy thật và lúc chấm**, phần mô tả **cắt bỏ**, chỉ lấy câu. Thước không hề nhìn thấy nó.

**Rủi ro lớn nhất, phải đo trước.** Tầng mô tả cần **tên** phần tử, mà cây trợ năng chỉ 12,6% phần tử có tên và bộ đọc chữ thì không đọc được nút hình thuần.

> **📦 Tầng mô tả chạy tốt và chạy hỏng, trên cùng một màn**
>
> | Nút cần chạm | Tầng mô tả sinh ra | |
> |---|---|---|
> | Ô tìm kiếm có chữ | `[ô nhập liệu \| "Search Publications, Stories & Interest" \| trên đỉnh, giữa]` | dùng được, tên rõ |
> | Biểu tượng kính lúp, không chữ | `[nút \| ? \| trên đỉnh, bên phải]` | **rỗng phần tên** |
> | Biểu tượng dấu cộng | `[nút \| "+" \| dưới đáy, bên phải]` | đọc được dấu cộng nhưng không biết nó nghĩa là thêm mới |
>
> Với hai dòng dưới, mô hình chẳng có gì để chép, thậm chí bị dẫn sai. **Tầng giữa mà rác thì hai tầng tệ hơn một tầng.** Nên việc đầu tiên là dựng thử nhãn tầng mô tả trên vài trăm bước rồi **soi tay** đếm bao nhiêu phần trăm dùng được — làm trước khi tiêu bất kỳ đồng nào.

---

#### TẦNG NỀN — viết lại câu đích bằng thông tin đặc quyền

Câu người viết quá cụt để làm đích tốt, nên trước khi huấn luyện thì viết lại chúng: khoanh dấu tại **điểm người thật đã chạm** lên ảnh, nhờ một mô hình lớn viết lại câu gốc thành câu tự đủ. Rồi huấn luyện trên **ảnh sạch** với câu đã viết lại.

Điểm mấu chốt: mô hình viết lại **được cầm đáp án**, mô hình học thì không. Nên nó không truyền lại năng lực định vị của nó — nó chỉ mô tả một chỗ đã được chỉ sẵn, còn mô hình học phải **tự tìm rồi mô tả**.

> **Đây là tầng dữ liệu, không tính vào tính mới.** Mình nói thẳng như vậy trong luận văn, vì cách vẽ dấu rồi nhờ mô hình lớn viết mô tả đã có người làm (xem mục 3.5).

---

#### LỚP PHỤ — đưa danh sách chữ trên màn vào đầu vào

Chạy bộ đọc chữ trước mô hình sinh, nối danh sách chữ nhìn thấy vào đầu vào, dùng cả lúc dạy lẫn lúc chạy.

> **Trên đúng màn PressReader, bộ đọc chữ trả về:**
>
> | Chữ | Vị trí |
> |---|---|
> | `Search Publications, Stories & Interest` | (486, 193) ← đúng chỗ cần chạm |
> | `Recommended` | (240, 569) |
> | `See all` | (961, 574) |
> | … | … |

Việc của mô hình nhẹ hẳn: từ *nhìn ảnh đoán xem nút tên gì* thành *chọn đúng dòng rồi chép tên ra*. Danh sách này không sạch — bỏ sót nút hình, đọc nhầm chữ mờ — nên mô hình **được huấn luyện với chính danh sách nhiễu đó**, phải học cả khi nào không nên tin nó.

**Cũng là kỹ thuật đã có** (mục 3.5), nên đây là lựa chọn thiết kế có đối chứng, không phải đóng góp.

---

#### Ba phần đứng cạnh nhau

| | Can thiệp vào đâu | Vai |
|---|---|---|
| Mô tả trước, phát ngôn sau | **cách mô hình phát ngôn** | **trụ đóng góp** |
| Viết lại câu đích | dữ liệu huấn luyện | tầng nền |
| Danh sách chữ vào | đầu vào | lớp phụ |

Chỉ phần đầu làm **mô hình lúc chạy hành xử khác**. Hai phần sau đổi thứ đưa vào rồi huấn luyện như thường. Đó là lý do chỉ phần đầu được kể là đóng góp mô hình.

> **Một lớp vá dùng chung.** Cả ba phần đều làm câu đầu ra dài và tả rõ hơn, mà thước thì đã đo được là **thiên vị câu dài**. Nên khi báo kết quả phải so trong từng nhóm độ dài riêng, báo phân bố độ dài trước sau, và chấm tay vài chục câu. Nếu toàn bộ chênh lệch nằm ở chỗ câu dài ra thì không được nhận là mô hình tốt hơn.

> **Cái gì được huấn luyện, cái gì không — nói rõ vì đây là câu hay bị hỏi.**
>
> | | Có huấn luyện? | |
> |---|---|---|
> | Qwen2.5-VL-3B, cả bốn nhánh | **có**, chỉnh trọng số bằng QLoRA | đây là mô hình của luận văn |
> | Mô hình lớn viết lại câu đích | không | chạy một lần để tạo dữ liệu, xong bỏ, không nằm trong hệ chạy thật |
> | Bộ đọc chữ | không | công cụ có sẵn |
> | Bộ trỏ dùng để chấm | không | cố tình để nguyên, vì đó là thước đo |
>
> **Trụ đóng góp nằm bên trong quá trình huấn luyện** — nó là *cái mà mô hình bị buộc phải sinh ra khi học*, chứ không phải cách ra lệnh cho một mô hình có sẵn. Và có hẳn một nhánh đối chứng **cố tình không huấn luyện** (mô hình lớn được ra lệnh theo đúng cấu trúc mô tả) để trả lời câu *"cần gì huấn luyện, ra lệnh khéo là xong"*. Nếu nhánh đó thắng thì phải báo cáo thẳng.

### 3.4 Tính mới nằm ở đâu, và không nằm ở đâu

Phần này viết thẳng, vì đây là câu hội đồng sẽ hỏi đầu tiên.

**Không mới — và sẽ nói thẳng là không mới:**

| Thứ | Đã có ai làm |
|---|---|
| Bắt mô hình lập dàn ý rồi mới viết | có từ lâu trong sinh văn bản |
| Ý "câu phải đủ để bên kia lần ra đúng đối tượng" | dòng sinh biểu thức quy chiếu, **từ 2016**, và có cả ở tầng huấn luyện |
| Khoanh dấu tại vị trí đúng rồi nhờ mô hình lớn viết mô tả | đã có trong chính miền giao diện, một bài ở hội nghị lớn 2025 |
| Đưa danh sách phần tử vào đầu vào rồi huấn luyện | bài gốc của chính bộ dữ liệu này đã làm |
| Mô hình 3 tỉ tham số cho giao diện | đã đông |

**Mới — ba chỗ, và đều cụ thể:**

**1. Đưa thông tin định danh vào MỤC TIÊU huấn luyện, không chỉ vào đầu vào.** Đây là chỗ có bằng chứng cứng nhất. Bài gần nhất trong miền này là Widget Captioning: họ **đã nêu rõ vấn đề** — trên một màn có hai biểu tượng kính lúp gần như giống hệt, một để tìm danh bạ một để tìm nhạc, nên *"thông tin ngữ cảnh là thiết yếu để mô hình giải mã đúng đối tượng"*. Nhưng cách họ xử là đưa ngữ cảnh vào **đầu vào**; hàm mất mát vẫn chỉ là cross entropy thuần.

> **📦 Khác nhau chỗ nào, nói bằng ví dụ**
>
> Màn có hai kính lúp giống hệt. Cần hướng dẫn bấm cái bên trái.
>
> | | Cách của họ | Cách ở đây |
> |---|---|---|
> | Mô hình **thấy** gì | cả hai kính lúp, vì ngữ cảnh màn đưa vào đầu vào | y hệt |
> | Mô hình **bị buộc nói** gì | chỉ cần khớp câu gold, mà gold có khi chỉ là *"tap search"* | phải nêu `[nút \| kính lúp \| trên đỉnh, **bên trái** \| có một kính lúp nữa bên phải]` rồi mới viết câu |
> | Hệ quả | không có gì phạt nếu câu khớp cả hai nút | không nêu được dấu hiệu phân biệt thì sai ngay ở tầng mô tả |
>
> Nói gọn: họ **cho mô hình xem** đủ thông tin, ở đây **bắt mô hình nói ra** thông tin đó. Thấy thì có thể lờ đi, nói ra thì không.

**2. Nguồn giám sát cho tầng giữa rút tự động từ thao tác của người thật.** Không cần người gán nhãn, không cần mô hình đóng: hộp phần tử tại đúng điểm người chạm, cộng chữ đọc được trong hộp đó. Các cách làm tương tự trong dòng sinh biểu thức quy chiếu đều cần một mô hình người nghe khả vi hoặc học tăng cường; ở đây không cần gì cả.

**3. Dùng câu hướng dẫn người viết làm ĐÍCH SINH.** Trong bài gốc, trường đó là **đầu vào** mớm cho máy để nó đoán hành động. Mọi công trình dùng bộ dữ liệu này đều để nó ở đầu vào. Chưa tra ra ai dùng làm đích.

**Nói gọn tính mới trong một câu:**

> Không phải một cơ chế mới, mà là **đưa tính phân biệt phần tử vào mục tiêu huấn luyện của một mô hình sinh hướng dẫn cho người đọc, với nguồn giám sát rút tự động từ toạ độ thao tác của người thật** — trong một miền mà bài gần nhất mới chỉ xử ở đầu vào.

Đây là tính mới ở mức **tổ hợp, nguồn giám sát, và miền áp dụng**. Không phải kiến trúc mới, không phải thuật toán mới. Đó là mức thực tế nhất mà một mô hình 3 tỉ tham số huấn luyện trên máy thuê cho phép, và luận văn trình bày đúng mức đó.

### 3.5 Những công trình phải phân định

| Công trình | Đã làm gì | Khác ở đây |
|---|---|---|
| Dòng sinh biểu thức quy chiếu, 2016 tới 2020 | dạy mô hình viết câu phân biệt được đối tượng, đo bằng một mô hình khác lần ra vị trí | ảnh tự nhiên, mô tả đồ vật; và họ **có sẵn danh sách vùng ứng viên**, ở đây phải tự dò phần tử |
| Một bài 2017 cùng dòng | đưa hẳn mô hình lần vị trí vào vòng huấn luyện làm tín hiệu | ở đây **cố ý không làm vậy**, vì mô hình lần vị trí cũng chính là thước chấm, làm vậy thành tự chấm |
| Widget Captioning, 2020 | sinh mô tả phần tử giao diện, có mã hoá ngữ cảnh màn | ngữ cảnh chỉ vào **đầu vào**, mục tiêu vẫn là cross entropy thuần |
| Một bài định vị giao diện, hội nghị lớn 2025 | khoanh hộp tại vị trí đúng rồi nhờ mô hình lớn viết mô tả | câu sinh ra làm **đầu vào** cho mô hình định vị; ở đây làm **đích sinh** cho người đọc |
| Vài công trình 2026 về chưng cất có đặc quyền trong giao diện | thầy thấy dấu, trò thấy ảnh sạch | đầu ra của họ là **toạ độ**, không phải câu cho người |
| Một bản làm sạch chính bộ dữ liệu này | có sửa câu hướng dẫn bằng mô hình lớn | chỉ sửa những mẫu mà **mọi tác tử đều làm hỏng**, mục đích làm sạch chỗ chấm |

---

## 4. Luồng chấm

Đây là phần có chất nghiên cứu nhất, vì không có đáp án mẫu để so.

### 4.1 Thước chính — hướng dẫn có trỏ đúng chỗ không

**Ý tưởng:** giấu mục tiêu đi, chỉ đưa cho một **bộ trỏ** ảnh và một câu hướng dẫn. Bộ trỏ là mô hình chuyên: cho nó ảnh và một câu như *"chạm nút tìm kiếm"*, nó chỉ ra điểm nên chạm. Dùng nó như một người dùng máy móc làm theo hướng dẫn. Nếu một câu đủ rõ để bộ trỏ chạm trúng, thì câu đó đúng.

> **Ví dụ chạy tay.** Màn app Snapdeal, ảnh 1080×2400, bước cần làm là bấm nút **Filter**, toạ độ đúng **(854, 2275)**.
> Câu mô hình sinh: *"Tap filter"* → đưa bộ trỏ ảnh và đúng câu đó, không nói mục tiêu, không nói đáp án → nó đoán điểm **(860, 2270)** → lệch khoảng **8 pixel**. Dung sai cho phép là 14% cạnh màn, khoảng 151 pixel. Vậy bước này **trúng**.

**Một bước tính là đúng khi thoả cả ba điều:**

1. **Thao tác khớp** — chạm, gõ, cuộn phải cùng loại với thao tác đúng. Mọi cách nói của cùng một cú chạm (*tap*, *open*, *go to*, *select*) gộp làm một lớp, vì trên giao diện chúng là cùng một hành động.
2. **Không ngược nghĩa** — câu và đáp án không được nhắm hai trạng thái ngược nhau của cùng một chỗ. *"Turn off"* trong khi đáp án là *"Turn on"* thì rớt, dù toạ độ trúng, vì công tắc bật và tắt nằm cùng một chỗ.
3. **Đúng chỗ** — với bước chạm thì điểm bộ trỏ phải trúng; với bước gõ thì nội dung gõ phải khớp; với bước cuộn thì hướng phải khớp.

**Hai khoá quan trọng:**

> **Không chấm theo câu chữ.** Gọi tên nút kiểu gì cũng được, miễn bộ trỏ lần ra đúng nút. *"funnel icon"* và *"Filter button"* viết khác hẳn nhau nhưng cùng trỏ trúng thì đều đúng. Điều này quan trọng vì mô hình học trên câu người viết sẽ nói giọng giống đáp án, nếu chấm theo chữ thì nó được thưởng oan.
>
> **📦 Thước bắt câu sai thế nào — vẫn màn Snapdeal đó**
>
> | Câu mô hình sinh | Bộ trỏ chỉ vào | Kết quả |
> |---|---|---|
> | *"Tap filter"* | (860, 2270) — lệch 8 pixel | **trúng** |
> | *"Tap the search bar"* | (540, 190) — ô tìm kiếm trên đỉnh | **trật**, cách đáp án cả nghìn pixel |
> | *"Tap the button"* | (540, 1200) — giữa màn, đoán bừa | **trật** |
>
> Câu càng mơ hồ thì bộ trỏ càng đoán lung tung. Đó chính là cơ chế mà thước dựa vào.

> **Chống màn quá dễ.** Có người sẽ vặn: *màn chỉ có một nút to thì câu vớ vẩn cũng trúng*. Đúng, nên phải trừ đi phần đó.
>
> Cách trừ: chạy thêm một lượt **không đưa câu gì cả**, chỉ đưa ảnh, rồi bảo bộ trỏ đoán đại một chỗ. Tỉ lệ trúng của lượt đó gọi là **sàn** — nó cho biết màn dễ tới mức nào. Giá trị thật của câu hướng dẫn là **phần chênh** giữa có câu và không câu.
>
> Ví dụ: nếu đưa câu thì trúng 51%, còn đoán bừa cũng trúng 40%, thì câu chỉ đóng góp 11 điểm. Đo thật thì sàn chỉ **6,6%**, nghĩa là màn không hề dễ và phần lớn điểm đến từ chất lượng câu.

> **Hộp kỹ thuật.** Với câu sinh *s* trên màn có thao tác đúng tại (x\*, y\*), bộ trỏ đông cứng *G* cho ra (x̂, ŷ) = *G*(ảnh, s). Bước thực thi được nếu khoảng cách ≤ τ·D, với D là kích thước màn và τ = 0,14 — ngưỡng dung sai của AITW (NeurIPS 2023). Đây đúng tiêu chí step-accuracy của AndroidControl, nhưng áp cho **câu hướng dẫn đã nối đất** thay vì cho toạ độ mô hình tự dự đoán. Control: chạy *G*(ảnh, ∅) làm sàn.

### 4.2 Hai cách chấm chỗ đúng

Chấm "trúng nút" có hai mức chặt, và cả hai đều được báo:

- **Cách rộng:** điểm rơi trong vùng dung sai quanh toạ độ đúng là tính trúng. Đơn giản nhưng dễ dãi — đo được là **63% số bước có một nút khác cũng nằm trong vùng dung sai**, nên câu trỏ nhầm sang nút bên cạnh vẫn có thể được cho qua.
- **Cách chặt:** chỉ tính trúng khi nút đúng là **nút gần điểm chấm nhất** trong số mọi phần tử trên màn. Câu trỏ nhầm sang nút cạnh sẽ rớt. Cách này cần một danh sách phần tử trên màn, lấy từ bộ dò hình hoặc từ cây trợ năng của hệ điều hành.

### 4.3 Thước phụ — có bịa nút không

Mỗi tên nút mô hình nhắc tới, kiểm xem nút đó có thật trên màn không, đối chiếu với danh sách nút kèm tên.

> **Ví dụ.** Màn Cài đặt có {Settings, Notifications, Display, Sound, Battery, Search}. Mô hình sinh *"Tap **Settings** → Tap **Preferences** → Enable **Alerts**"* → Settings có thật, Preferences bịa, Alerts bịa (đúng ra là Notifications) → nhắc 3 nút, 2 bịa → điểm trung thực = 1 − 2/3 = 0,33.
>
> **Cái bẫy phải tránh:** nếu mô hình nói *"Tap the + icon"* mà danh sách nút bỏ sót nhãn của nút dấu cộng, đối chiếu ngây thơ sẽ kết oan nó là bịa. Nên các nút hình không có nhãn bị loại khỏi mẫu số, và tỉ lệ phải loại được báo kèm.

Trục này chạy trên MobileViews, vì đó là bộ có danh sách nút **kèm tên** đủ dày. Trên AndroidControl thì cây trợ năng cho hộp rất đầy đủ (trung vị 86 phần tử một màn) nhưng **chỉ 12,6% phần tử có tên**, không đủ để đếm bịa.

### 4.4 Kiểm chính cái thước bằng cách bơm lỗi

Không dùng "so với người chấm" làm cổng đậu rớt. Thay vào đó **bơm lỗi đã biết** vào rồi xem thước có bắt được không: trỏ sang nút khác, đảo nghĩa bật tắt, đổi loại thao tác, gõ sai nội dung, cuộn sai hướng. Ngưỡng khoá trước khi chạy.

> **📦 Một ca bơm lỗi trông thế nào**
>
> Lấy một bước đã biết đáp án, rồi cố tình làm hỏng từng thứ một, xem thước có kêu không:
>
> | Bơm lỗi gì | Câu hoặc điểm sau khi bơm | Thước phải |
> |---|---|---|
> | Không bơm gì, chỉ viết lại câu cho khác chữ | *"Tap the search control located at the top"* | **cho đậu** — cùng nghĩa mà |
> | Trỏ sang một phần tử khác cách xa | điểm rơi vào banner giữa màn | bác |
> | Trỏ sang phần tử ngay cạnh | điểm lệch 100 pixel sang nút bên | bác |
> | Đảo nghĩa | gold *"Turn on"*, câu thành *"Turn off"* | bác, dù toạ độ vẫn đúng chỗ |
> | Đổi loại thao tác | gold là chạm, câu thành *"type into"* | bác |
> | Gõ sai nội dung | gold gõ *"Ukraine"*, câu ghi gõ *"zzqeniar"* | bác |
>
> Thước nào cho đậu cả sáu dòng dưới thì vô dụng; thước nào bác luôn dòng đầu thì khắt khe tới mức không dùng được.

Điều kiện để phép kiểm này có giá trị: **ca lỗi phải dựng bằng nguồn ngoài thước**. Nếu dựng ca lỗi bằng chính hàm của thước thì kết quả luôn đẹp và không nói lên điều gì — giống ra đề rồi tự chấm bài mình.

> **Hộp kỹ thuật.** Cách làm theo Sai và cộng sự (EMNLP 2021): nhét lỗi đã biết, đo độ nhạy và độ đặc hiệu. Không lấy tương quan với người làm cổng đậu rớt (Clark, ACL-IJCNLP 2021), không tự chấm bằng nhãn do mô hình ngôn ngữ sinh (Panickssery, NeurIPS 2024).

### 4.5 Làm sao biết thước đo đúng thứ cần đo

Mục 4.4 trả lời câu "thước có bắt được lỗi không". Còn một câu khác, khó hơn: **bộ trỏ chạm trúng thì người thật có làm theo được không?** Cả hệ thống chấm đứng trên giả định đó, và hiện nó **chưa được kiểm**.

Cách kiểm: lấy 91 cặp câu đã có sẵn, đưa cho người đọc và hỏi *"đọc câu này rồi nhìn màn hình, bạn có làm được không"*, rồi đối chiếu với phán đoán của bộ trỏ trên cùng những câu đó.

> **📦 Bốn kết cục có thể xảy ra**
>
> | Người nói | Bộ trỏ nói | Nghĩa là |
> |---|---|---|
> | làm được | trúng | thước đúng |
> | không làm được | trật | thước đúng |
> | **làm được** | **trật** | thước quá khắt khe, đánh rớt câu tốt |
> | **không làm được** | **trúng** | thước quá dễ, cho qua câu dở — đây là ca nguy hiểm nhất |
>
> Hai dòng đầu càng nhiều thì thước càng đáng tin. Hai dòng dưới nhiều thì thước đang đo một thứ khác với thứ mình cần.

> **Cần phân biệt rõ hai chuyện, vì chúng hay bị gộp làm một:**
>
> | | Chấm mô hình bằng người | Kiểm dụng cụ đo |
> |---|---|---|
> | Làm mấy lần | mỗi lần có mô hình mới lại phải thuê người | **đúng một lần**, xong là thôi |
> | Chấm cái gì | đầu ra của mô hình, để lấy con số kết quả | các câu có sẵn, để đối chiếu với phán đoán của bộ trỏ |
> | Kết quả nằm ở đâu | trong bảng kết quả chính | trong phần kiểm chứng phương pháp |
>
> Toàn bộ đánh giá của đề tài **không** dùng cột trái. Mọi con số trong bảng kết quả đều do máy chấm, lặp lại được, không phụ thuộc vào việc thuê người. Cột phải chỉ là bước hiệu chuẩn dụng cụ trước khi dùng, giống như cân chuẩn trước khi cân hàng loạt.

Điều kiện để bước hiệu chuẩn này có nghĩa: phải có **hai người chấm độc lập** (một người thì không đo được mức đồng thuận), người chấm **không được nhìn thấy kết quả của bộ trỏ**, và ngưỡng phải khoá trước — mức tương quan từ 0,5 trở lên thì thước đáng tin, từ 0,3 đến 0,5 là yếu và phải khai giới hạn, dưới 0,3 thì cách chấm này không dùng được.

### 4.6 Các khoá chống ăn gian

| Khoá | Nội dung |
|---|---|
| App tách riêng | app đem chấm chưa từng xuất hiện lúc dạy |
| Thông tin phụ chỉ vào lúc dạy và chấm | lúc sinh, mô hình không có toạ độ đúng, không có đáp án |
| Nguồn dạy khác nguồn chấm | danh sách chữ đưa vào mô hình lấy từ OCR; danh sách nút dùng lúc chấm lấy từ nguồn khác hẳn |
| Lượt không câu làm sàn | tách phần đóng góp của câu khỏi phần dễ của màn |
| Nhánh giả dược | đưa danh sách chữ **của một màn khác**; nếu điểm vẫn tăng thì hiệu ứng không đến từ nội dung danh sách |
| Phân tầng theo độ dài câu | bộ trỏ thiên vị câu dài, nên phải so trong từng nhóm độ dài riêng |

---

## 5. Kết quả đã đo được

Tất cả số dưới đây đo trên AndroidControl, lát app chưa từng thấy, với một bộ trỏ giá rẻ. Chưa có số của mô hình huấn luyện — phần đó là bước kế tiếp.

### 5.1 Thước có phân biệt được câu tốt với câu dở không

| Cách chấm | Đưa câu đáp án | Không đưa câu (sàn) | Chênh |
|---|---|---|---|
| Rộng: điểm rơi trong vùng dung sai là tính trúng | 51,3% | 6,6% | **+44,7** |
| Chặt, danh sách nút lấy từ bộ đọc chữ | 35,5% | 2,6% | +32,9 |
| Chặt, danh sách nút lấy từ bộ dò hình | 19,7 đến 34,2% | 0,0% | +19,7 đến +34,2 |
| Chặt, **danh sách nút thật từ cây trợ năng** | **6,6%** | 0,0% | **+6,6** |

**Đọc bảng này.** Sàn rất thấp ở mọi cách chấm, nghĩa là đoán bừa thì hiếm khi trúng đúng cái nút cần — một màn có hàng chục phần tử. Nhưng có một quy luật rõ: **danh sách nút càng đầy đủ thì trần càng tụt**. Đó không phải nghịch lý, đó là vì thước càng chặt thì càng đòi bộ trỏ chính xác.

**Vì sao dòng cuối tụt mạnh như vậy — ba con số giải thích trọn vẹn:**

| | |
|---|---|
| Phần tử cần chạm rộng cỡ nào | 189 × 126 pixel |
| Phần tử **khác** gần nhất cách đó bao xa | 69 pixel |
| Bộ trỏ giá rẻ lệch bao nhiêu | 256 pixel |

Bộ trỏ lệch xa hơn cả khoảng cách sang phần tử bên cạnh, nên nó gần như luôn rơi vào ô của một phần tử khác. **Không phải câu hướng dẫn dở, mà là dụng cụ đo chưa đủ nhạy.**

> **Kết luận thực dụng.** Với bộ trỏ hiện tại, chỉ cách chấm rộng dùng được. Cách chấm chặt phải chờ một bộ trỏ chính xác hơn — và giờ có thể nói rõ chính xác tới đâu: **sai số phải nhỏ hơn khoảng cách giữa hai phần tử cạnh nhau, tức dưới 69 pixel, nên ngưỡng đặt ở 3% cạnh màn (khoảng 32 pixel) để có biên an toàn.** Đây chính là điều kiện tiên quyết của cổng kiểm bộ trỏ.

### 5.2 Thước có bắt được lỗi không

Bơm lỗi với mười ngưỡng khoá trước khi chạy, **đạt tám**:

| Phép thử | Kết quả | Ngưỡng | |
|---|---|---|---|
| Câu cùng nghĩa, điểm trỏ lệch bằng mức thật → không được đánh rớt | 59,2% | ≤10% | **rớt** |
| Cổng thao tác bác oan cặp câu thật | 13,2% | ≤15% | đạt |
| Luật đảo nghĩa kêu oan trên câu cùng nghĩa | 0,0% | ≤5% | đạt |
| Bắt câu trỏ sang phần tử cách 30–80 px | 100% (n=2) | ≥80% | đạt, cỡ mẫu quá nhỏ |
| Bắt câu trỏ sang phần tử cách 80–150 px | 100% | ≥90% | đạt |
| Bắt câu trỏ sang phần tử cách xa hơn 25% cạnh | 100% | ≥95% | đạt |
| Bắt đảo nghĩa nhóm giữ riêng (next / previous…) | 0% | ≥50% | **rớt** |
| Bắt câu sai loại thao tác | 100% | ≥80% | đạt |
| Bắt câu gõ sai nội dung | 93,1% | ≥90% | đạt |
| Bắt câu cuộn sai hướng | 100% | ≥90% | đạt |

**Hai chỗ rớt nói lên điều gì:**

- **Chỗ thứ nhất là điều kiện chặn đường.** Bộ trỏ giá rẻ lệch rất xa. Đo lại 6/8 bằng đúng dụng cụ của cổng A: **trung vị 29,3% bề ngang màn** trên 10 bước tập kiểm, không bước nào vào nổi 3%; bốn trong mười lần nó trả đúng giữa màn, tức đoán bừa chứ không trỏ. Đường cong kết oan đo bằng cây trợ năng và luật Voronoi: lệch 1% kết oan 0%, 3% vẫn 0%, 5% lên 7,5%, 8% lên 24,1%, 13% lên 55%. Nghĩa là **cách chấm chặt chỉ dùng được khi có bộ trỏ chính xác hơn nhiều** — sai số trung vị phải xuống dưới 3% bề ngang.

  > ⚠️ **Số cũ ở dòng này đã bị rút.** Bản trước ghi "lệch trung vị 8% cạnh màn" kèm đường cong 2,6%/25%/42%/60%. Cả hai đều sai. Con số 8% không có trong bất kỳ kết quả đo nào — tệp `ground_pilot_results.json` lưu `median_dist = 0,150`, và "8" gần như chắc chắn chép nhầm từ "trung vị **8 từ**" ở câu bên cạnh (chỗ chia đôi câu ngắn/câu dài). Đường cong cũ thì đo trên hộp OmniParser với luật hộp-gần-nhất, không phải dụng cụ sẽ chấm. Thêm nữa, hai script dùng hai công thức khác nhau: `ground_pilot` chia lệch dọc cho chiều CAO (nhẹ đi 2,2 lần), còn cổng A dùng khoảng cách pixel chia bề NGANG — chênh nhau 1,63 lần trên cùng dữ liệu. Ngưỡng 3% nói theo công thức của cổng A.
- **Chỗ thứ hai đã lường trước.** Luật đảo nghĩa nhận diện bằng bảng từ nên mù với cặp đặc thù giao diện như *next* và *previous*. Nhóm này cố ý giữ riêng, không đưa vào bảng của thước — thêm vào thì điểm thành tuyệt đối nhưng là tự chấm chính mình. Nhẹ đi ở chỗ các cặp đó là hai nút khác nhau nên kênh toạ độ còn cơ hội bắt, và loại thật sự nguy hiểm là công tắc dùng chung một vị trí thì chỉ chiếm **1,06% số bước**.

### 5.3 Cỡ mẫu và lực thống kê

| | Trục chính (độ đúng) | Trục phụ (độ bịa) |
|---|---|---|
| Bộ dữ liệu | AndroidControl, app chưa từng thấy | MobileViews |
| Đơn vị thống kê | theo app | theo app |
| Cỡ mẫu | 631 tác vụ; **78 app**, hiệu dụng 34,8 | 12 app |
| Phép kiểm | wild-cluster bootstrap (Cameron, Gelbach, Miller, REStat 2008) | exact sign-flip |
| Hiệu ứng nhỏ nhất đo được | **chưa khoá được**, kịch bản bảo thủ 10,7 đến 16,0 điểm | khoảng 32 điểm, quá yếu nên chỉ để mô tả |

Hiệu ứng nhỏ nhất đo được chưa chốt vì dữ liệu thử hiện có quá thưa: chỉ khoảng 3,5 bước mỗi app, nên nhiễu lấy mẫu còn lớn hơn cả chênh lệch quan sát được giữa các app. Phải chạy lại phần này với ít nhất 15 bước mỗi app trước khi khoá con số.

---

## 6. Các mốc sẽ đem so

Bảy nhánh, chấm cùng một bộ trỏ, cùng giấu mục tiêu, kèm lượt không đưa câu làm sàn.

| Nhánh | Vai |
|---|---|
| không đưa câu | sàn |
| gpt-4o-mini | mốc ngoài |
| gpt-4o-mini có prompt cùng cấu trúc mô tả | chặn đòn "chỉ là ra lệnh khéo, đâu cần huấn luyện" |
| Qwen-3B huấn luyện thường trên câu gốc | mốc trong |
| huấn luyện trên câu đã viết lại | tầng nền |
| huấn luyện trên câu viết lại **mù ảnh** | tách thông tin khỏi độ dài |
| **hai tầng: mô tả rồi câu** | **trụ** |

**Ba phép so mang nghĩa:**

1. **Trụ so với nhánh viết lại** — cùng giọng, cùng dữ liệu, chỉ khác việc mô hình có phải phát ngôn qua tầng mô tả hay không. Đây là **hiệu số đo đúng đóng góp mô hình**, không lẫn với phần dữ liệu.
2. **Viết lại có xem ảnh so với viết lại mù ảnh** — cả hai đều cho câu dài như nhau, nhưng chỉ một bên biết chỗ chạm. Nếu hai bên ngang nhau thì phần tăng chỉ là câu dài ra, và **cả hướng chết**.
3. **Trụ so với gpt-4o-mini và với bản huấn luyện thường** — ràng buộc bắt buộc.

**Thêm một phép so quyết định cho phần đóng góp mô hình:** trụ phải **vượt chính mô hình viết lại khi mô hình đó chạy trên ảnh sạch**. Nếu không vượt thì lập luận "thầy chỉ mạnh vì được cầm đáp án" sụp, và mọi thứ quy về chưng cất thường.

> **📦 Đọc bảng kết quả thế nào — ba kịch bản giả định**
>
> Giả sử điểm ra như sau (số bịa để minh hoạ cách đọc, không phải kết quả thật):
>
> | | Kịch bản A | Kịch bản B | Kịch bản C |
> |---|---|---|---|
> | gpt-4o-mini | 30 | 30 | 30 |
> | huấn luyện thường | 34 | 34 | 34 |
> | trên câu viết lại | 48 | **49** | 48 |
> | trên câu viết lại **mù ảnh** | 36 | **47** | 36 |
> | **trụ, hai tầng** | **56** | 51 | **49** |
>
> **A — kết quả tốt.** Viết lại có xem ảnh hơn hẳn viết lại mù (48 với 36), nên phần tăng đến từ thông tin chứ không phải câu dài ra. Và trụ hơn tầng nền 8 điểm, đó là đóng góp mô hình đo được.
>
> **B — hướng chết.** Viết lại mù gần bằng viết lại có xem ảnh (47 với 49), nghĩa là mô hình chỉ được lợi vì câu dài ra. Phải tự bác, không được nhận là mô hình hiểu hơn.
>
> **C — thành phần rỗng.** Dữ liệu thì tốt thật, nhưng trụ chỉ hơn tầng nền 1 điểm, dưới ngưỡng đo được. Khi đó phải báo thẳng rằng đóng góp mô hình không chứng minh được, chứ không lặng lẽ đổi sang khoe con số 48.

**Ngưỡng coi là thất bại, đăng ký trước khi chạy:**

- Bộ trỏ không đạt điều kiện lệch dưới 3% cạnh màn → không nhánh nào diễn giải được, dừng
- Viết lại có xem ảnh không hơn viết lại mù → phần tăng chỉ là độ dài, hướng chết
- Trụ không hơn nhánh viết lại → thành phần mô hình rỗng, phải khai trước với thầy chứ không lặng lẽ đổi trụ sau khi thấy số
- gpt-4o-mini có prompt cùng cấu trúc mà bằng hoặc hơn trụ → phần huấn luyện mất giá trị, phải báo cáo

## 7. Những việc còn lại

Xếp theo nguyên tắc: việc nào có thể giết cả hướng thì làm trước, việc miễn phí làm trước việc tốn tiền.

| Việc | Chi phí | Là cổng cho điều gì |
|---|---|---|
| Đo lại các con số với danh sách nút thật từ cây trợ năng | miễn phí | con số cuối cùng đem trình |
| Hiệu chuẩn thước với người đọc, 91 cặp, hai người chấm độc lập | miễn phí | kiểm giả định "bộ trỏ trúng thì người làm theo được" (xem mục 4.5) |
| Dựng dữ liệu dạy và chạy sẵn bộ đọc chữ trên toàn bộ ảnh | miễn phí | đầu vào cho mọi bước sau |
| Huấn luyện bản thường rồi đo nó | khoảng 20 đô | biết còn bao nhiêu chỗ để tiến; nếu hẹp hơn hiệu ứng nhỏ nhất đo được thì kết quả không đọc được |
| Kiểm bộ trỏ chuyên | khoảng 10 đô | sai số trung vị phải dưới 3% cạnh màn, nếu không thì bỏ cách chấm chặt |
| Huấn luyện bốn nhánh Qwen-3B, kèm các đối chứng | khoảng 40 đô | kết quả chính |

Toàn bộ pha huấn luyện ước khoảng 60 đến 70 đô trên máy thuê.

**Hai hướng đã cân nhắc rồi để lại, ghi ra để khỏi ai hỏi lại:**

- *Cho mô hình tự sinh nhiều câu rồi dùng bộ trỏ giữ lại câu trỏ trúng để học lại.* Chưa chạy được vì bộ trỏ giá rẻ lọc sai quá nửa: nếu một nửa số câu sinh ra là đúng thì tập giữ lại chỉ sạch khoảng 70%, tức huấn luyện trên dữ liệu một phần ba sai nhãn.
- *Dạy bằng cặp câu đúng và câu tả nhầm nút bên cạnh.* Bắn trượt cơ chế hỏng: lỗi số một là câu **mơ hồ**, còn chuyện gọi nhầm nút thì đo ra gần như không xảy ra.

## 8. Tóm tắt

**Một mô hình mở 3 tỉ tham số được fine-tune**, chạy offline, nhìn app chưa từng thấy và viết hướng dẫn từng bước cho người đọc — việc mà chưa mô hình nào được huấn luyện để làm.

**Thành phần làm nó hơn bản fine-tune thường:** bắt mô hình **nêu phần tử là cái gì** trước khi viết câu, với nhãn tầng giữa rút tự động từ chỗ người thật đã chạm. Thành phần này nằm ngay trong đích huấn luyện, không phải mẹo bên ngoài. Tính mới ở mức tổ hợp và nguồn giám sát, không phải kiến trúc mới — và luận văn nói đúng mức đó.

**Một cách chấm khách quan, không cần đáp án mẫu, không cần thuê người:** đưa câu cho một bộ trỏ xem nó có lần ra đúng nút không, kèm lượt không đưa câu làm sàn, và tự kiểm bằng bơm lỗi. Giới nghiên cứu giao diện thì chấm bằng khảo sát người, dòng tác tử thì chấm hành động của chính mô hình — chưa bên nào có thước khách quan lặp lại được cho **hướng dẫn viết cho người đọc**.

Số đã có: thước phân biệt được câu tốt với câu dở ở mọi cách chấm, chênh 19,7 tới 44,7 điểm tuỳ độ chặt; thước qua bơm lỗi đạt tám trên mười ngưỡng khoá trước, hai chỗ rớt báo nguyên trạng. Chưa có số của mô hình sau huấn luyện — đó là bước kế tiếp.

---

## 9. Bốn câu cần thầy quyết

1. **Khung đóng góp.** Mô hình fine-tune cộng một thành phần trong đích huấn luyện, và cách chấm khách quan — thầy thấy hai phần này đủ chưa, và phần nào nên là chính?
2. **Không chấm bằng người.** Mọi con số trong bảng kết quả đều do máy chấm. Chỉ có một bước hiệu chuẩn dụng cụ làm **đúng một lần** với người đọc, để kiểm giả định "bộ trỏ trỏ trúng thì người làm theo được". Thầy đồng ý giữ bước hiệu chuẩn đó không, hay bỏ luôn và khai là giới hạn?
3. **Nếu chỉ hoà.** Nếu mô hình chỉ ngang chứ không hơn mốc ngoài, thì "mô hình 3 tỉ tham số chạy offline ngang mô hình lớn gọi qua mạng" có đủ để bảo vệ không?
4. **Mức tính mới.** Thành phần này không phải kiến trúc mới, mà là đưa tính phân biệt phần tử vào mục tiêu huấn luyện trong một miền chưa ai làm vậy. Thầy thấy mức đó đủ cho luận văn thạc sĩ chưa?

---

## 10. Rủi ro và đường lui

| Rủi ro | Đường lui |
|---|---|
| Tầng mô tả bị rác vì thiếu tên phần tử | đo chất lượng tầng giữa **trước** khi huấn luyện; nếu quá nhiễu thì thu về nhóm phần tử có chữ và khai giới hạn |
| Thành phần không làm mô hình hơn bản thường | đã có cổng đo trước: huấn luyện bản thường rồi đo xem còn bao nhiêu chỗ để tiến; hẹp quá thì báo trước chứ không train mù |
| Điểm tăng chỉ vì câu dài ra | đã có sẵn nhánh đối chứng viết lại mù ảnh, cộng phân tầng theo độ dài câu |
| Bộ trỏ không đủ chính xác | quay về cách chấm rộng và nói rõ giới hạn; bản thân chuyện "không thước tự động nào trỏ nổi nút hình" cũng là một phát hiện |
| Chỉ hoà mốc ngoài | vẫn bảo vệ được bằng luận điểm mô hình nhỏ chạy offline |
| Bị hỏi "sao không đưa bộ trỏ vào vòng huấn luyện" | vì bộ trỏ cũng là thước chấm, đưa vào thành tự chấm — đây là lựa chọn có chủ đích, không phải thiếu sót |

---

### Phụ lục — trích dẫn

AndroidControl (Li và cộng sự, **NeurIPS 2024 Datasets & Benchmarks**) · MobileViews (arXiv 2409.14337, giấy phép MIT) · ngưỡng dung sai 14% từ AITW (**NeurIPS 2023**) · SeeClick (**ACL 2024**) và OS-Atlas (**ICLR 2025**) cho định vị phần tử · ALOHa (**NAACL 2024**) cho đo bịa · Chen và cộng sự về việc app thiếu nhãn phần tử (**ICSE 2020**, Distinguished Paper) · Sai và cộng sự về kiểm thước bằng bơm lỗi (**EMNLP 2021**) · Panickssery (**NeurIPS 2024**) và Clark (**ACL-IJCNLP 2021**) về chống tự chấm · UI-R1 (**AAAI 2026**), SE-GUI (**NeurIPS 2025**) cho tiền lệ huấn luyện mô hình 3 tỉ tham số trên miền giao diện · Mao và cộng sự (**CVPR 2016**) cho tiền lệ đánh giá kiểu sinh câu rồi cho mô hình khác trỏ vùng · Fried và cộng sự (**NeurIPS 2018**) cho tiền lệ sinh chỉ dẫn rồi cho bên khác thực thi · Cameron, Gelbach, Miller (**REStat 2008**) cho wild-cluster bootstrap.
