# Luận văn — tất cả trong một

**Ngày 19/7/2026.** Tài liệu này gộp toàn bộ: đề tài là gì, đã làm được gì, vòng phản biện đối kháng vừa tìm ra chỗ nào hỏng, cái gì vẫn còn đứng, và làm gì tiếp theo. **Đọc file này là đủ, không cần mở file nào khác.**

---

## Trạng thái trong một phút

Luận văn đang ở giai đoạn chuẩn bị, **chưa huấn luyện mô hình**, chưa tiêu tiền GPU. Thiết kế đã chốt và **không sập**. Nhưng một vòng phản biện đối kháng vừa chạy hôm nay phát hiện **thước đo chưa hề được kiểm** — cái vẫn tưởng là "đã kiểm và đậu" hoá ra là một phép tính biết trước kết quả. Khi đem thước ra thử bằng dữ liệu thật thì nó **rớt**.

Tin tốt: mọi thứ phải sửa đều **miễn phí** và sửa được **trước khi** tiêu tiền. Không phát hiện nào đòi đổi dataset, đổi mô hình, hay bỏ hướng.

Việc kế: **năm giai đoạn A→E, tất cả free, khoảng một tuần rưỡi**, rồi mới gặp thầy, rồi mới huấn luyện.

---

# PHẦN 1 — ĐỀ TÀI VÀ BÀI TOÁN

## 1.1. Đề tài

Xây một mô hình trí tuệ nhân tạo nhận **một ảnh chụp màn hình ứng dụng điện thoại** cộng **một câu hỏi** của người dùng (ví dụ *"làm sao để bật thông báo cho tập podcast mới?"*), rồi trả lời bằng **các bước hướng dẫn cụ thể cho người đọc**:

> 1. Chạm vào Settings
> 2. Chạm vào Notifications
> 3. Bật New episode alerts

## 1.2. Hai cái khó cốt lõi

**Khó thứ nhất — không có đáp án mẫu để chấm.** Không tồn tại sẵn bộ "hướng dẫn chuẩn" do con người soạn cho từng màn hình. Tự soạn thì tốn hàng nghìn giờ. Nên phải nghĩ ra cách đo chất lượng mà không cần đáp án mẫu.

**Khó thứ hai — một kiểu lỗi nguy hiểm.** Mô hình có thể **bịa ra tên một nút không tồn tại** (nói "Chạm Preferences" trong khi màn hình chỉ có "Settings"). Người dùng làm theo sẽ dò không ra hoặc bấm nhầm. Lỗi này khó thấy bằng mắt vì câu văn đọc lên vẫn trơn tru.

## 1.3. Ràng buộc bắt buộc của thầy

Luận văn thạc sĩ của trường **bắt buộc phải có một mô hình do học viên tự huấn luyện** — không được chỉ ghép công cụ có sẵn qua gọi API. Ràng buộc này cứng, đã xác nhận lại. Mô hình phải là **đóng góp thật**, không phải chỉ làm nền.

---

# PHẦN 2 — VÌ SAO THIẾT KẾ RA NHƯ HIỆN TẠI

Thiết kế bây giờ là kết quả của một chuỗi kiểm chứng rồi điều chỉnh. Hiểu chuỗi này thì hiểu vì sao mọi thứ như vậy.

## 2.1. Bản đầu — bị thầy bác

Ban đầu luận văn = gọi API gpt-4o-mini đọc ảnh viết hướng dẫn, rồi dùng thuật toán so chuỗi để kiểm bịa. Thầy bác vì *"chủ yếu là gọi API và so chuỗi, chưa thấy mô hình do học viên tự huấn luyện đâu"*.

## 2.2. Hướng "chưng cất trung thực"

Để có mô hình tự huấn luyện, chuyển sang ý tưởng **thầy giáo — học trò**:

- **Thầy giáo** = gpt-4o-mini viết bản nháp hướng dẫn.
- Đối chiếu tên nút với **View Hierarchy** (VH — file do Android xuất kèm mỗi ảnh, liệt kê mọi nút thật cùng vị trí). Chỗ nào bịa thì viết lại thành câu chung chung.
- Dữ liệu đã lọc sạch → **huấn luyện học trò** = Qwen2.5-VL-3B (mô hình nhỏ, chạy được ngay trên máy).

Đóng góp dự kiến lúc đó: quy trình **lọc bỏ chỗ bịa** để tạo dữ liệu sạch, dạy học trò trung thực hơn thầy.

## 2.3. Bốn phép thử miễn phí lật đổ tiền đề — bước ngoặt

Trước khi tiêu tiền, chạy bốn phép thử miễn phí ngay trên máy để kiểm tiền đề.

**K1 — kiểm bộ đối chiếu.** Bộ đối chiếu so tên nút mô hình nói với danh sách nút thật trong VH. Kiểm hai chiều:

- *Bỏ lọt:* mô hình bịa tên **nghe giống** nút thật (nói "Send" khi màn chỉ có "Save"). Thuật toán thấy gần nghĩa nên cho qua → bịa lọt vào dữ liệu.
- *Kết oan:* mô hình gọi **đúng** nút nhưng bằng từ khác ("Tìm kiếm" cho nút "Search"). Thuật toán không nhận ra → đánh nhầm là bịa.
- **Kết quả: bỏ lọt 47,5% và kết oan 47,5%**, điểm số hai loại **chồng lên nhau hoàn toàn** → không ngưỡng nào tách được. Đổi thuật toán mạnh hơn cũng chỉ đỡ chút. Đây là hạn chế bản chất của việc đo độ gần nghĩa.

**K2 — đếm thầy giáo bịa thật bao nhiêu.** Đọc tay 80 màn mà gpt-4o-mini đã viết hướng dẫn. Kết quả gây bất ngờ: **gpt-4o-mini gần như không bịa (chỉ ~0-2%)**, không phải "khoảng một phần tư" như tưởng. Những chỗ bị đánh "bịa" thật ra là **nút CÓ THẬT nhưng VH bỏ sót nhãn** — nhất là nút hình (dấu cộng, dấu tích).

**OCR — thử đọc chữ trên ảnh bù chỗ VH thiếu.** Giúp với nút có chữ (độ phủ nhãn 74% → 80%), nhưng thua nút hình thuần; còn ~20% nút không cách nào lấy được nhãn.

**VIỆC1 — đọc tay câu chung chung.** Câu an toàn nhưng lặp lại đúng câu hỏi, không chỉ chỗ bấm → giá trị thấp; và vì K2, nó thường thay một nút thật cụ thể bằng câu mơ hồ.

**Hệ quả lớn:** tiền đề *"thầy giáo bịa nhiều, ta lọc bỏ để dạy học trò trung thực hơn"* **lung lay** — vì thầy gần như không bịa, nên chẳng có gì để lọc.

## 2.4. Chuyển sang phương án lai

Vì tiền đề lung lay, chốt hướng mới:

- **Không** lấy "lọc bịa" làm đóng góp chính.
- **Lấy độ ĐÚNG làm trục chính**, đo trên bộ dữ liệu **AndroidControl** — vì bộ này **có sẵn đáp án đúng do người thật làm**, chấm được chính xác (khác MobileViews vốn không có đáp án).

**Độ ĐÚNG** = hướng dẫn có dẫn tới việc cần làm không. Khác **độ TRUNG THỰC** vốn chỉ đo có bịa nút không.

## 2.5. Chạy thử xác nhận, và tìm được cách hay hơn

Chạy thử trên AndroidControl: **đèn xanh**. Và phát hiện thêm: AndroidControl có sẵn **hướng dẫn từng bước do người viết** (*"Bấm vào tab Gmail ở góc dưới bên trái"*). Nên thay vì mò tên nút theo toạ độ, ta **so thẳng hướng dẫn của mô hình với hướng dẫn do người viết** — văn bản với văn bản.

---

# PHẦN 3 — THIẾT KẾ CUỐI

## 3.1. Hai đóng góp ngang nhau

**Đóng góp MÔ HÌNH.** Một mô hình sinh hướng dẫn nhiều bước **cho người đọc** từ một ảnh + câu hỏi. Khác biệt: mọi mô hình giao diện hiện có (SeeClick, UI-R1, OS-Atlas, Aguvis) đều sinh **thao tác cho MÁY tự bấm** — toạ độ, mã hành động, chấm bằng tỉ lệ máy làm xong việc. Luận văn này sinh **hướng dẫn cho NGƯỜI đọc và tự làm**.

> **Không được nói "mô hình đầu tiên".** Xem Phần 5.5 — có một bài ở CHI 2026 đã chiếm chỗ này ở mức khái niệm.

**Đóng góp ĐÁNH GIÁ.** Cặp thước đo: **độ trung thực** (đối chiếu VH, không cần đáp án) và **độ đúng** (so đáp án), cộng phát hiện thực nghiệm từ bốn phép thử về vì sao cách đo ngây thơ hỏng.

Hai trụ báo cáo độc lập — một trục ra kết quả rỗng không kéo sập trục kia.

## 3.2. Huấn luyện trên dữ liệu nào

Mục tiêu: dạy Qwen2.5-VL-3B, khi nhìn một màn hình và biết mục tiêu người dùng, **tự viết câu hướng dẫn cho bước kế tiếp**, bắt chước cách người thật viết.

**Nguồn chính — AndroidControl** (bộ do Google công bố, bình duyệt NeurIPS 2024). Mỗi thao tác được một người thật ghi kèm một câu hướng dẫn. Mỗi mẫu huấn luyện:

> **Đưa vào:** ảnh màn hình tại một bước + mục tiêu tổng thể + các bước đã làm trước.
> **Dạy trả ra:** đúng câu hướng dẫn do người viết cho bước đó.

**Nguồn phụ — MobileViews chưng cất.** Bộ này chỉ có ảnh + VH, không có hướng dẫn người viết. Nên thầy giáo gpt-4o-mini sinh nháp (không cho thấy VH), rồi lọc chỗ bịa bằng bộ đối chiếu **đa tầng** (so chuỗi → VH → OCR → từ điển ký hiệu, chứ không phải bộ đơn đã chết ở K1). Vai của nó giờ là **bổ sung độ rộng** (nhiều app hơn), không còn vai "lọc bịa để dạy trung thực".

> **Bắt buộc huấn luyện hai bản để so:** một bản CÓ dữ liệu phụ, một bản KHÔNG. Chênh lệch cho biết dữ liệu phụ có đóng góp thật không. Nếu không thì thành thật báo là không.

**Cấu hình:** kỹ thuật nhẹ **QLoRA 4-bit** — thay vì dạy lại cả mô hình (rất tốn), chỉ gắn thêm ít "miếng dán" học được vào phần *nói*, và **đóng băng phần nhìn** (vì việc cần dạy là *nói gì*, không phải *nhìn thấy gì*). Chạy trên một GPU thuê của Google Colab, khung LLaMA-Factory. LoRA r=8 / alpha=16, tốc độ học ~1e-4, khoảng 3 vòng.

## 3.3. Đo ở đâu

**Trục ĐÚNG (chính):** đo ngay trên **phần app chưa từng thấy của chính AndroidControl** — học và chấm cùng một bộ nhưng khác app, để mô hình không học thuộc app rồi chấm chính nó. So **Học trò với Thầy giáo gốc** (gpt-4o-mini chưa chỉnh gì).

Cách này bỏ được một lỗ hổng của bản thiết kế trước: bản đó huấn luyện trên MobileViews nhưng chấm trên AndroidControl — hai bộ khác nhau — nên điểm thấp có thể do *khác bộ dữ liệu* chứ không phải do hướng dẫn kém.

**Trục TRUNG THỰC (phụ):** đo trên MobileViews, tắt VH lúc sinh, xem học trò có bịa nút không.

## 3.4. Thước đo "so hai đoạn hướng dẫn"

Thước tách mỗi bước thành cặp **(thao-tác, đích)**:

- **Thao-tác** = loại hành động, khớp trên từ vựng đóng (chạm/gõ/cuộn/mở/quay-lại).
- **Đích** = tên nút được gọi, khớp bằng so từ khoá là chính, embedding bge-m3 làm dự phòng ở ngưỡng cao.

Ý tưởng: "tab Gmail" và "tab Calendar" chung từ "tab" nhưng khác từ khoá → không khớp → bắt được lỗi. Điều mà đo cả câu (K1) không làm nổi.

Ba số đọc ra: **coverage** (phủ được bao nhiêu bước đúng — số chủ đạo), **F1** (chống nhồi bước thừa), **order-τ** (đúng thứ tự).

**⚠ Thước này chính là chỗ vừa phát hiện có vấn đề nặng — xem Phần 5.**

---

# PHẦN 4 — VÒNG PHẢN BIỆN ĐỐI KHÁNG ĐÃ LÀM THẾ NÀO

Ngày 19/7 chạy một vòng phản biện đối kháng lên toàn bộ luận văn. Cách làm quan trọng, vì nó quyết định kết quả có đáng tin không.

**Bảy giám khảo độc lập, mỗi người một trục**, chạy song song: thước đo · thống kê · dữ liệu và rò rỉ · bốn phép thử · tính mới và scoop · đóng góp có đủ ngưỡng · đối chiếu văn-với-số. Năm người dùng mô hình Opus 4.8 cho các trục kiểm được bằng số; hai người dùng mô hình khác họ (Fable) cho hai trục thuần phán đoán, để đổi góc nhìn ở đúng chỗ mà phán đoán dễ giống nhau.

**Ba luật đặt ra để không thành màn tự khen:**

1. **Bịt mắt.** Cấm đọc các file tóm tắt trước. Bắt đọc code và file kết quả thô trước, tự kết luận, xong mới mở phần viết ra đối chiếu. Lý do: các file tóm tắt đều do trợ lý AI viết, giọng rất tự tin, đọc trước là bị mớm khung.
2. **Phải gắn bằng chứng.** Mỗi đòn phải kèm tên file + số dòng, hoặc con số trích từ kết quả thô, hoặc output tự chạy lại. Không gắn được thì phải tự khai là suy đoán.
3. **Vòng bác bỏ.** Mọi đòn xếp mức nặng trở lên bị giao cho một giám khảo **khác** với nhiệm vụ *cố hết sức bác bỏ nó*.

**Kết quả:** 64 phát hiện, 39 đòn nặng vào vòng bác bỏ, **12 chết, 27 sống**. Những gì trình bày dưới đây đã qua một lần đối kháng, không phải ý kiến một chiều.

**Giới hạn phải khai:** cả bảy giám khảo lẫn người tổng hợp đều là mô hình cùng một nhà, cùng gu huấn luyện, nên có thể cùng mù một chỗ. Vòng này **không thay thế** vòng kiểm của thầy hướng dẫn.

---

# PHẦN 5 — CÁI GÌ HỎNG

## 5.1. Lỗ nặng nhất: thước đo chưa hề được kiểm

### Cổng kiểm thước không phải phép đo, mà là phép tính biết trước kết quả

Ý tưởng ban đầu đúng: muốn biết thước tốt không thì bơm lỗi giả vào rồi xem thước có bắt được không. Vấn đề nằm ở **cách sinh ra hai loại ca thử**.

Ca "viết khác nhưng cùng nghĩa" (thước phải chấp nhận) được dựng bằng cách **lấy chính đáp án của thước rồi lắp lại thành câu mới**. Nên tập từ của nó **trùng khít với đáp án** — điểm khớp bằng 1.0 không phải vì thước giỏi, mà vì phép thử tự chép lại đáp án.

Ca "sai đích" (thước phải bác) thì ngược lại: code **bắt buộc** đích thay thế phải **không được trùng một chữ nào** với đáp án. Nên điểm bằng 0 cũng theo định nghĩa.

Hai đống điểm được xây để tách rời **trước khi thước kịp chạy**. Con số `AUC = 1.000` từng được coi là bằng chứng lớn nhất thật ra chỉ là phép tính "xác suất 1.0 lớn hơn 0.0" — phương sai bằng không, không có dữ liệu nào trên đời làm nó tụt xuống dưới 1.

**Hệ quả về quy trình:** cổng "nếu AUC dưới 0.80 thì DỪNG, không huấn luyện" **không có đường nào kích hoạt được**. Nó không phải cổng. Hai dòng khác trong cùng bảng cổng cũng sập theo — tức **3 trong 5 dòng của bảng cổng là hằng đẳng thức**, không phải kết quả đo.

### Đem ca thật vào thì thước rớt, và rớt nặng

Một giám khảo tự dựng 10 cặp viết-khác-cùng-nghĩa **thật** — cùng một nút, gọi bằng hai cách người ta thật sự hay gọi:

| Đáp án | Cách gọi khác | Thước chấm |
|---|---|---|
| filter option | funnel icon | trượt |
| settings icon | gear icon | trượt |
| compose button | pencil icon | trượt |
| search bar | magnifying glass | trượt |

**Kết oan 10/10. AUC = 0.35 — tệ hơn tung đồng xu.**

Lớp dự phòng bge-m3 không cứu được ca nào, vì điểm giống nhau chồng lấn đúng như K1: cặp `gmail tab` ↔ `calendar tab` (đây là ca **bịa**) được 0.717, trong khi `search bar` ↔ `magnifying glass` (ca **thật**) chỉ 0.490. Ca bịa ăn điểm cao hơn ca thật.

Nghĩa là câu *"tách (thao-tác, đích) giải được đúng chỗ K1 chết"* — câu từng được coi là kết quả cứng nhất — **sai**. Việc tách chỉ chứng minh thước phân biệt được hai thái cực, mà so chuỗi thuần cũng làm được chuyện đó.

### Hệ quả nguy hiểm nhất: con số chính có thể chỉ đo độ khớp giọng văn

Đây là chỗ chạm vào tim luận văn.

Trục ĐÚNG so Học trò với Thầy giáo trên cùng dữ liệu. Học trò được huấn luyện **trên chính đáp án của AndroidControl**, nên nó học đúng phương ngữ của người viết đáp án (`Click on X`). Thầy giáo chạy không huấn luyện thì diễn đạt theo cách khác (`Tap the funnel icon`). Với một thước kết oan cách-gọi-khác một cách có hệ thống, **Học trò thắng không phải vì hướng dẫn đúng hơn, mà vì nói giống đáp án hơn**.

Không phải suy luận suông. Một giám khảo lấy 91 câu thầy giáo đã có sẵn, rồi **chỉ đổi các lựa chọn bề mặt của thước**, không đổi một chữ nội dung:

| Cấu hình thước | Điểm thầy giáo |
|---|---|
| nguyên trạng | 0.286 |
| gộp chạm/mở thành một lớp | 0.330 |
| đổi cách tính chồng-từ | 0.473 |
| cả hai + bỏ từ chỉ vị trí | **0.604** |

Điểm nhảy hơn gấp đôi chỉ vì đổi cách chuẩn hoá. Một đại lượng nhạy đến vậy thì con số chính **không diễn giải được**.

**Cách chữa:** thêm nhánh **Thầy giáo nói cùng giọng** — nhét vài câu đáp án mẫu vào lời nhắc cho thầy giáo nói cùng phương ngữ. Khi đó:

- *Học trò trừ Thầy-cùng-giọng* = phần "chọn đúng nút" (cái ta muốn đo)
- *Thầy-cùng-giọng trừ Thầy gốc* = phần "khớp giọng thuần" (cái nhiễu)

Rẻ, và biến một con số không diễn giải được thành hai con số diễn giải được.

### Thước sai cả hai chiều ở vùng giữa

Vì bơm lỗi chỉ sinh hai cực, vùng giữa — nơi thước thật sự phải phân xử — chưa bao giờ được thử. Chạy thử:

**Nhận đúng trong khi sai:**

| Mô hình nói | Đáp án | Kết quả |
|---|---|---|
| Turn **off** notifications | Turn **on** notifications | **KHỚP** |
| Scroll **up** | Scroll **down** | **KHỚP** |
| Set timer to **30** minutes | **10** minutes | **KHỚP** |

Hướng dẫn **ngược nghĩa** vẫn được tính là đúng. Đây là chiều nguy hiểm hơn vì nó thổi phồng điểm.

**Bác trong khi đúng:** `Tap Log in` với `Tap the Sign in button` → trượt. `Tap the Trash icon` với `Click on Delete` → trượt.

### Vài lỗi cơ học nữa

- **Một bước đáp án được "phủ" bởi một bước đáp án khác.** 12,4% bước bị tính là đã phủ bởi một bước hoàn toàn khác trong cùng chuỗi. Sửa bằng cách ghép một-đối-một.
- **Đích rỗng khớp nhau hoàn hảo.** Nhãn nút phổ biến (`Next`, `Back`, `Open`, `Enter`, `Go`) nằm trong danh sách từ bị bỏ qua → 3,2% bước rút gọn về đích rỗng, mà hai đích rỗng thì thước cho **khớp hoàn hảo**. Đo được: `Tap Next` và `Tap Back` được tính là **khớp, điểm 1.000**.

### Thước thưởng câu cộc lốc, phạt hướng dẫn hữu ích hơn

Đề tài nói sinh hướng dẫn **cho người đọc**. Thước lại chấm bằng độ trùng từ với câu chú thích ngắn. Đáp án là `Click on filter option`:

| Mô hình sinh ra | Điểm | |
|---|---|---|
| `Tap the Filter button` (cộc lốc) | 1.000 | khớp |
| `Tap the funnel-shaped Filter icon` (tả hình dạng) | 0.333 | **trượt** |
| `Tap Filter to narrow the list, then choose a category` (có ngữ cảnh) | 0.250 | **trượt** |

Càng thêm thông tin hữu ích cho người, càng bị trừ điểm. Trớ trêu là phép thử VIỆC1 kết luận điểm yếu của mô hình chính là **không** chỉ vị trí và hình dạng.

*Có một điểm được bác:* thước **không** phạt chi tiết chỉ **vị trí** (có bộ lọc xoá cụm vị trí). Chỉ **hình dạng** mới bị trừ.

## 5.2. Vấn đề về tính chính trực của bản đăng ký trước

**"Vòng 2 — thử ca khó" không tồn tại trong repo.** Ba con số của vòng này từng được dùng để bác lại nghi ngờ "vòng 1 quá dễ". Nhưng **không có script nào sinh ra chúng**, file kết quả chỉ chứa số của vòng 1. Mắt xích chịu lực nhất lại là mắt xích không tái lập được.

**Caveat rụng dần qua ba tầng tài liệu.** File gốc (report/84) tự khai **rất sòng phẳng**: *"tôi giữ nguyên từ lõi → điểm khớp bằng 1 là tất yếu"* và *"phép bơm lỗi do chính tôi dựng → có phần vòng vo"*. Nhưng ngay trong cùng file, phần kết luận lại viết *"đã kiểm bằng số, không phải giả định"*. Sang các file tóm tắt thì chỉ còn `✅ QUA`, và commit git ghi `metric-gate PASSED`.

**Lời tự khai không chảy được vào chỗ nó phải chặn.** Bài học: caveat của một con số phải nằm **ngay trong ô của nó**, không được đẩy xuống mục hoài nghi cuối file.

**Script tự in cờ đỏ, báo cáo ghi dấu tích.** Script tự đặt luật "nếu điểm tụt dưới 0,15 thì in cảnh báo". Chạy lại thì nó **in ra cảnh báo cho 2 trong 3 phép kiểm**, nhưng bảng trong báo cáo ghi cả hai là ✓. (Bản chất thì ngưỡng 0,15 mới là cái đặt sai, không phải thước hỏng — nhưng không được im lặng bỏ qua cờ đỏ của chính mình.)

## 5.3. Thống kê: đếm nhầm file

**Số app lấy từ sai quần thể.** Con số "khoảng 150-250 app" đếm từ tập test **chung**, không phải phần dành để chấm.

| | Từng ghi | Đếm lại trên đúng phần dữ liệu |
|---|---|---|
| tỉ lệ gán được app | ~72% | **41%** |
| số app khác nhau | ~114 trong 200 chuỗi | **42** trong 102 chuỗi |
| phân bố | "phần lớn mỗi app một chuỗi" | **tập trung mạnh** — Pinterest 14, Arts&Culture 8 |

Tính lại: **mức chênh lệch nhỏ nhất mà thí nghiệm nhìn thấy được ≈ 12,5-14,4 điểm phần trăm**, không phải 8-9. Vẫn dưới ngưỡng nguy hiểm 15-20 nhưng **sát hơn nhiều**, không còn dư địa.

**Biến nhóm bị vỡ.** Hàm gán app dùng nhận dạng mẫu trên câu mục tiêu, và kết quả cho thấy: cùng một app bị tách đôi (`The Washington Post` và `Washington post` thành hai nhóm riêng; `NYTimes` và `Newyork times` riêng), và có nhóm không phải tên app (`Inspire in this`, `On the Pinerest`).

Hai hệ quả đều xấu: số nhóm bị **thổi phồng** (làm thí nghiệm trông mạnh hơn thực), và quan sát của cùng một app bị rải vào nhiều nhóm nên phép thống kê tưởng chúng độc lập → **khoảng tin cậy hẹp giả**.

**Trục phụ thiếu lực nghiêm trọng.** Ô ghi mức chênh lệch nhỏ nhất của trục trung thực đang **để trống** mà vẫn commit. Tính ra: **32,2 điểm phần trăm** — tức trục này **rớt ngưỡng gấp đôi**. Mô phỏng đầy đủ cho thấy lực chỉ 25% ở mức chênh 15 điểm. Nghĩa là một kết quả rỗng ở trục này **không đọc được gì** — không phân biệt được "không có hiệu ứng" với "có hiệu ứng mà không đủ lực bắt".

## 5.4. Đáp án AndroidControl là gì thật sự

Đọc thẳng 1042 câu đáp án:

- trung vị **6 từ**; 48,9% câu từ 5 chữ trở xuống; 10,3% từ 3 chữ trở xuống
- 60,4% bắt đầu bằng click/tap/press/select
- chỉ 749 câu khác nhau trên 1042
- **167 cặp bước liền nhau trùng y hệt**
- có câu hỏng: `Click on the top at the bottom right corner`

Đây là **nhãn thao tác ngắn**, không phải văn hướng dẫn cho người. Huấn luyện trên đây thì ra một bộ **sinh nhãn thao tác bằng ngôn ngữ tự nhiên**. Khác các bài khác chủ yếu ở chỗ đầu ra là câu chữ thay vì lời gọi hàm — không phải ở chỗ "viết cho người đọc".

Phải chọn một trong hai, không có đường giữa:

- **(a)** khai thẳng, hạ claim xuống "sinh mô tả thao tác bằng ngôn ngữ tự nhiên"; hoặc
- **(b)** giữ claim "cho người" nhưng phải có tầng viết lại **và** một vòng đánh giá bằng người thật.

Dù chọn gì cũng phải lọc dữ liệu huấn luyện: bỏ bước rỗng, gộp cặp trùng liên tiếp (~20%), nếu không mô hình học luôn cả tật lặp.

## 5.5. Một quả mìn ở CHI 2026

**GuideMe** — Proceedings of CHI 2026, DOI 10.1145/3772318.3791448. Hệ thống cho người cao tuổi: người dùng hỏi trong app, hệ chụp màn hình, lấy thông tin nút, mô hình phân tích, sinh **hướng dẫn từng bước** kèm tô sáng tại chỗ để người làm theo.

Ở **mức tác vụ**, "sinh hướng dẫn nhiều bước cho người từ ảnh + câu hỏi" đã được công bố tại hội nghị HCI hàng đầu. Vòng kiểm scoop cũ **không có bài này** — nó từng tự khai "chưa quét CHI/UIST", và lỗ tự khai đó chứa đúng quả mìn.

Câu *"mô hình đầu tiên sinh hướng dẫn nhiều bước cho người đọc"* giờ **sai ở mức tác vụ**.

**Giảm nhẹ, và đây là phần đáng mừng:**

1. Trục CHI **không phải điểm mù** — repo đã có ghi chép về AskEase, **cùng hội nghị CHI 2026**, và đã tự dán nhãn "rủi ro tính mới cao nhất, phải phân định". Lập luận phân định đã viết sẵn, áp nguyên xi cho GuideMe được.
2. Vòng kiểm scoop **đã tự cấm** claim này từ trước.
3. **Bản thảo bài báo sạch** — không hề có chữ "first/đầu tiên". Overclaim chỉ nằm ở nhật ký nội bộ.
4. GuideMe **không huấn luyện mô hình, không có bộ dữ liệu, không có thước đo** — đóng góp của họ là phần tương tác.

**Việc phải làm:** hạ claim xuống *"mô hình nhỏ mở đầu tiên **được huấn luyện** cho tác vụ này"*, thêm GuideMe vào phần văn liệu, và dùng nó làm **trụ biện minh nhu cầu** (giới HCI đã cần tác vụ này) thay vì coi là bị chiếm chỗ.

## 5.6. Bốn phép thử: cần chỉnh cách kể, không cần chạy lại

**K2 — đúng là chỉ một app.** Toàn bộ 80 màn đều thuộc **một ứng dụng duy nhất**. 40 ca đọc tay quy về **18 tên nút khác nhau**, riêng dấu `+` chiếm 15 ca.

**Nhưng đòn này bị bác**, bằng lập luận thuyết phục: con số "khoảng một phần tư bịa" mà K2 lật đổ **cũng đến từ đúng bộ dữ liệu đó**. Bác một khẳng định bằng chính mẫu đã sinh ra nó thì không cần tính đại diện. Thêm nữa, kết luận hành động được của K2 — VH bỏ nhãn nút hình nên bộ đối chiếu kết oan nút thật — được xác nhận **độc lập ở quy mô 30 app**.

Phần còn sống: đổi cách viết. "80 màn" → "80 màn **của 1 app**"; "40 ca" → "40 quan sát trên **~18 nút khác nhau**".

**K1 — mẫu nhỏ hơn tài liệu kể.** Tài liệu ghi "chạy trên 127 màn". Thật ra tập thử chỉ từ **30 màn / 7 app**. Và thành phần lệch: một chuỗi chiếm 11/40 ca. Ca đại diện cho "bịa gần nghĩa" lại chọn cặp **trái nghĩa** (`None` với `All`) — mà embedding nổi tiếng đặt trái nghĩa rất gần nhau, nên đó là tự xếp bài để phép thử rớt.

**OCR — đếm nhầm, thổi số lên khoảng 7 lần.** Cách đếm cũ tính "chuỗi có chứa ký tự đó", nên mọi chữ chứa x (`Expenses`, `Next`, `Box`) bị tính là đọc được icon X.

| Ký hiệu | Từng ghi | Đếm lại đúng |
|---|---|---|
| `+` | 23 | **11** |
| `X` | 97 | **13** |
| mũi tên | 46 | **0** |
| dấu tích | — | **0** |

**OCR trả về không một mũi tên nào và không một dấu tích nào** — đúng hai loại nút mà K2 chỉ ra là nguồn kết oan chính. Nên tầng "từ điển ký hiệu" trong thiết kế **không có gì để gắn vào** cho chính các ca nó sinh ra để cứu.

## 5.7. Khả thi

Kiểm kê thẳng, ngày 19/7:

- **Không có** script huấn luyện, không có cấu hình nào
- Phần dữ liệu để huấn luyện (~13 nghìn chuỗi + ảnh) **chưa tải**
- Bộ đối chiếu đa tầng cho trục trung thực **chưa dựng**
- **Chưa gặp thầy** sau ba lần đổi khung
- Kế hoạch hai bài báo vẫn đang bán **đóng góp lọc-bịa đã chết từ 18/7**

Chuỗi việc còn lại trước hạn 15/8: vá thước → dựng dữ liệu → chạy thử → huấn luyện → chấm → viết bài tiếng Anh. Trong **27 ngày**, một người, Colab chưa mua.

**Phán quyết: bài tiếng Anh hạn 15/8 gần chắc trượt.** Đường lui đã có sẵn từ trước (bỏ bài tiếng Anh, giữ bài tiếng Việt) — đó là điểm cộng thật.

Nhưng bài tiếng Việt cũng không an toàn như tưởng: chấm độ trung thực của câu **tiếng Việt** đối chiếu VH **tiếng Anh** là đúng ca mà K1 đo được so chuỗi kết oan **97,5%**. Cách chữa "bảo mô hình giữ tên nút tiếng Anh" chưa có số nào chống lưng.

---

# PHẦN 6 — CÁI GÌ VẪN CÒN ĐỨNG

Phần 5 cố ý một chiều, chỉ liệt kê chỗ hỏng. Đây là phần cân bằng.

**Xương sống thiết kế không sập.** Không đòn nào giết được, kể cả khi các giám khảo cố tình tìm cách giết:

- tách bước thành (thao-tác, đích) — ý tưởng vẫn đúng, phần hiện thực mới sai
- đo trên phần app chưa từng thấy của cùng bộ dữ liệu — hợp lệ
- so cặp Học trò với Thầy giáo — hợp lệ, chỉ cần thêm nhánh cùng-giọng
- hai trục đúng + trung thực báo cáo độc lập — hợp lệ

**Những kết quả vẫn đứng:**

- Thầy giáo đạt 30% điểm đúng → **trục đo được, không suy biến về 0**. Đây là cổng lo lắng lớn nhất hồi tháng 7 và nó đã qua thật.
- Kết luận cốt lõi của K2 (VH bỏ nhãn nút hình gây kết oan) được xác nhận độc lập ở quy mô 30 app.
- Bộ dữ liệu, mô hình gốc, hướng đi — không phát hiện nào đòi đổi.
- Bản thảo phần văn liệu sạch, không chứa overclaim.

**Mười hai đòn đã bị bác** trong vòng đối kháng, gồm cả những đòn nghe rất nặng: "K2 dựa trên 1 app nên vô hiệu", "cả 4 phép thử chạy trên bộ dữ liệu khác nên không chuyển giao được", "thước chính mới xây được một phần ba". Đều không đứng vững.

**Điều quan trọng nhất:** cái sập là **bằng chứng rằng thước đã được kiểm**, không phải bản thân thiết kế. Thước chưa được kiểm — nó vừa bị đem ra thử lần đầu và rớt. Đó là thông tin, không phải thảm hoạ, miễn là biết trước khi tiêu tiền.

---

# PHẦN 7 — KẾ HOẠCH

**Nguyên tắc xuyên suốt: giai đoạn A đến D đều miễn phí. Không tiêu một đồng GPU hay API nào cho tới hết giai đoạn D.**

## Giai đoạn A — Dừng chảy máu ✅ ĐÃ XONG 19/7

Không sửa gì về khoa học, chỉ ngừng để tài liệu nói mạnh hơn số. Đã làm:

- Gỡ ba câu overclaim khỏi nhật ký và file tóm tắt
- Ra **bản vá có dấu thời gian** cho bản đăng ký trước (không sửa lặng, vì nó đã commit làm dấu thời gian)
- Sửa số trong ba file phép thử: K1 "127 màn" → 30 màn/7 app; K2 thêm "1 app"; OCR đếm lại bảng ký hiệu

## Giai đoạn B — Dựng lại thước cho tử tế (2-4 ngày)

**B1. Viết lại bộ bơm lỗi cho độc lập với thước.**

- Nhánh "viết khác cùng nghĩa" **không được gọi hàm của thước**. Lấy 100-150 câu đáp án, viết lại bằng tay hoặc bằng mô hình khác, đổi đúng thứ mô hình thật sẽ đổi: `tab`→`section`, `filter option`→`funnel icon`.
- Nhánh "sai đích" **bỏ ràng buộc không được trùng chữ nào**, lấy nút cùng màn có chồng từ.
- Thêm bốn họ ca hiểm hiện chưa có: đảo nghĩa (bật↔tắt, lên↔xuống), đổi số lượng, đích cha↔con, từ đồng nghĩa nhãn nút.
- Chạy, báo kèm khoảng tin cậy. **Chuẩn bị tinh thần nó rớt** — đó là thông tin, không phải thất bại.

**B2. Vá các lỗi cơ học** (làm cùng B1, chốt **trước** khi nhìn kết quả để khỏi thành chỉnh thước theo kết quả):

- ghép một-đối-một thay vì phủ tập
- đích rỗng → chặn cứng, không cho khớp
- tách bảng động từ khỏi bảng lọc từ (`Next`, `Back` chỉ bị loại khi ở vị trí động từ)
- luật cứng: khác từ phủ định hoặc khác số lượng thì không khớp, bất kể điểm

**B3. Chạy vòng 2 thật và commit cả code lẫn kết quả.** Hoặc gỡ hẳn ba con số khỏi báo cáo.

> **Cổng thật ở đây:** nếu sau khi vá mà thước vẫn rớt trên ca thật, **dừng, đừng huấn luyện**. Lúc đó phải bàn lại: thêm từ điển chuẩn hoá tên nút, đổi sang thước khác, hay chuyển trọng tâm luận văn sang chương đo lường. **Đây là cổng có thể rớt thật** — khác cổng cũ.

## Giai đoạn C — Nối thước với người (2-3 ngày) — **ĐÃ DỰNG SẴN, CHỈ CẦN NGỒI CHẤM**

Đây là việc **rẻ nhất mà giá trị nhất** trong cả danh sách. Bộ chấm đã dựng xong hôm nay, dùng 91 câu thầy giáo có sẵn nên **không tốn một xu**.

**Cách làm:** mở file `harness/cv_study/rate_A.html` bằng trình duyệt — không cần internet, không cần cài gì, ảnh nhúng thẳng trong file. 91 màn, mỗi màn có ảnh chụp, mục tiêu người dùng, và hai câu hướng dẫn. Chấm mỗi câu 0-3 theo câu hỏi *"nhìn màn này, câu này có giúp bạn chạm đúng chỗ không?"*. Xong bấm **Xuất kết quả**, rồi chạy `harness/cv_analyze.py`.

Khoảng 40-60 phút mỗi người. **Cần hai người** — người thứ hai không cần biết gì về luận văn, chỉ cần biết dùng điện thoại.

**Ba chỗ được thiết kế có chủ ý:**

1. **Người chấm không biết câu nào của thầy giáo, câu nào là đáp án mẫu.** Thứ tự xáo ngẫu nhiên mỗi màn.
2. **Đáp án AndroidControl bị đưa vào chấm như một thí sinh**, không phải như chuẩn mực. Nếu chính nó cũng bị chấm thấp thì phát hiện 5.4 được xác nhận, và claim "hướng dẫn cho người" phải hạ xuống. Câu hỏi đó hiện đang treo, phép thử này trả lời miễn phí.
3. **Ô tick "hai bước khác nhau"** — vì dữ liệu thật có nhiều cặp kiểu `Tap the Search bar` với `Type spiritual lounge in the search bar`. Đó không phải thước sai, đó là chuyện một màn có nhiều bước kế tiếp hợp lệ mà đáp án chỉ ghi một. Có ô tick thì tách được **lỗi câu chữ** (lỗi thật của thước) khỏi **bước khác** (giới hạn của đáp án).

**Nếu tương quan giữa điểm người và điểm thước mà thấp thì mọi thứ phía sau đều vô nghĩa.** Biết bây giờ rẻ hơn biết sau khi đã đốt GPU.

## Giai đoạn D — Dọn thống kê (1-2 ngày)

- **D1.** Gán app cho toàn bộ 631 chuỗi. Ưu tiên trường tên app có sẵn; nhận dạng mẫu chỉ dùng khi có duyệt tay. Chuẩn hoá tên, gộp bí danh, rà tay khoảng 70 tên cuối.
- **D2.** Tính lại số nhóm thật và mức chênh lệch nhỏ nhất, bằng cách tách phương sai giữa-app và trong-app.
- **D3.** **Điền ô còn trống của trục trung thực.** Nếu ra khoảng 30 điểm phần trăm thì quyết ngay: tăng số app, hay hạ trục đó xuống mức mô tả và khai thẳng là không đủ lực.
- **D4.** Đặt một ngưỡng riêng có căn cứ cho trục chính. Ngưỡng 15-20 hiện đang mượn của trục khác.

## Giai đoạn E — Gặp thầy

Mang theo: tài liệu này, kết quả B (thước rớt hay đậu), kết quả C (thước có nối được với người không), số liệu D đã tính lại.

## Giai đoạn F — Chỉ khi A-E đã xong

1. Quyết bỏ hay giữ bài tiếng Anh — **việc này làm ngay tuần này**, đừng đợi hết E.
2. Chạy thử sinh tiếng Việt bằng mô hình chạy tại máy (miễn phí) trước khi tin bài tiếng Việt là sàn an toàn.
3. Tải phần dữ liệu huấn luyện, lọc (bỏ bước rỗng, gộp cặp trùng liên tiếp).
4. **Thêm nhánh Thầy-giáo-cùng-giọng** vào thiết kế và đăng ký trước. Không có nhánh này thì con số chính không diễn giải được.
5. Mua Colab, huấn luyện.

## Thứ tự rút gọn

> Dừng overclaim (A ✅) → dựng lại thước và chấp nhận nó có thể rớt (B) → hỏi người xem thước có đo đúng thứ cần không (C) → dọn thống kê (D) → gặp thầy (E) → mới huấn luyện (F).

Bốn giai đoạn đầu **không tốn một đồng nào** và mất khoảng một tuần rưỡi. So với việc huấn luyện xong mới phát hiện thước đo nhầm thứ, đây là món hời.

---

# PHẦN 8 — BỐN QUYẾT ĐỊNH CHỈ BẠN QUYẾT ĐƯỢC

Kế hoạch trên là đề xuất. Bốn thứ sau không ai quyết thay được:

**1. Bỏ hay giữ bài tiếng Anh hạn 15/8.** Không phụ thuộc gì cả, quyết được ngay tuần này. Mỗi ngày trì hoãn là một ngày mất của bài tiếng Việt và của luận văn. Khuyến nghị: bỏ, giữ bài tiếng Việt làm sàn chắc, mô hình đi hội nghị sau.

**2. Ai chấm cùng bạn ở giai đoạn C.** Không có người thứ hai thì mất chỉ số đồng thuận, mà mất nó thì khi tương quan thấp bạn không phân biệt được "thước tệ" với "điểm người nhiễu".

**3. Nếu giai đoạn B rớt thật** — thước vá xong vẫn không tách được viết-khác-cùng-nghĩa với bịa — thì chuyển trọng tâm sang chương đo lường, đổi thước, hay hoãn? **Nên hỏi thầy, đừng tự quyết.**

**4. Claim "hướng dẫn cho người"**: khai thẳng là sinh mô tả thao tác, hay giữ claim và thêm tầng viết lại cộng đánh giá bằng người? Phụ thuộc kết quả C.

Chỉ việc 1 quyết được ngay. Ba việc còn lại nên để sau B và C — lúc đó có số, quyết đỡ mò.

---

# PHẦN 9 — BẢN ĐỒ FILE

**Đọc để hiểu:**

| File | Nội dung |
|---|---|
| **report/91** (file này) | tất cả trong một |
| report/88 | bối cảnh chi tiết (các dòng lỗi thời đã đánh dấu ⛔) |
| report/90 | bản phản biện đối kháng đầy đủ + kế hoạch |
| report/90b | nguyên văn 27 đòn, kèm số dòng code và output chạy lại |
| report/85 | bản đăng ký trước, đã có bản vá 1 ngày 19/7 |

**Bằng chứng (mở khi cần tra một con số):** report/73 (K1) · 74 (K2) · 75 (OCR) · 76 (VIỆC1) · 78 (chọn hướng lai) · 79 (chạy thử) · 81 (thiết kế cuối) · 82 (chống scoop) · 84 (⛔ cổng bị rút) · 86 (⚠ tính lại).

**Tham chiếu kỹ thuật:** report/54 (cơ chế chi tiết) · 57 (văn liệu) · 53 (cấu hình) · 44/48 (dữ liệu).

**Mã nguồn** trong `harness/`:

| Script | Việc |
|---|---|
| `cv_build_items.py` | dựng bộ chấm construct-validity (giai đoạn C) |
| `cv_analyze.py` | phân tích kết quả chấm |
| `cv_study/rate_A.html`, `rate_B.html` | **giao diện chấm — mở bằng trình duyệt** |
| `metric_v1_validate.py` | thước (action, target) — **cần dựng lại bộ bơm lỗi** |
| `mde_pilot.py` | chạy thử tính lực thống kê — **cần tính lại số nhóm** |
| `k1_matcher_killtest.py`, `k2_hallucination_types.py`, `ocr_vh_coverage.py`, `pilot_androidcontrol.py` | bốn phép thử |

---

*Tài liệu này do trợ lý AI tổng hợp từ vòng phản biện đối kháng ngày 19/7/2026. Mọi con số đều truy được về mã nguồn hoặc file kết quả trong repo; chi tiết ở report/90b. Cảnh báo trung thực: các giám khảo và người tổng hợp đều là mô hình cùng một nhà, có thể cùng mù một chỗ — tài liệu này không thay thế vòng kiểm của thầy hướng dẫn.*
