# Luận văn — bản trình thầy đầy đủ

> Gộp trọn thiết kế + bằng chứng + các chỗ đã tự kiểm, để thầy đọc một mạch là nắm hết. Cập nhật **28/7/2026**.
>
> **Đợt vá 28/7 — đọc trước nếu đã đọc bản cũ.** Bốn chỗ hở của thước được đem đo bằng số thay vì chỉ nêu ra, và **một vòng phản biện độc lập đã lật lại chính bản vá đầu tiên trong ngày**, nên phần này ghi kết quả sau cùng:
>
> - **Thước đã qua bơm lỗi, nhưng bản bơm lỗi đầu tiên không hợp lệ.** Bản đầu tuyên bố "đạt 9/10 ngưỡng độc lập"; phản biện chỉ ra phần lớn nhánh của nó là hằng đẳng thức (chọn nút cạnh bằng chính hàm của thước, đặt điểm trùng tâm hộp, bơm đảo nghĩa bằng đúng bảng của thước). Đó là **đúng lỗi đã giết bộ bơm lỗi đời trước**. Bản 2 dựng lại ca lỗi bằng tiêu chí hình học độc lập → **đạt 8/10**, và hai chỗ rớt đều là chỗ đáng giá.
> - **Phát hiện nặng nhất: cách chấm chặt chưa dùng được với bộ trỏ hiện tại.** Khi điểm trỏ lệch đúng bằng mức lệch thật của bộ trỏ rẻ, thước **kết oan 59% số câu đúng**. Vậy con số "chênh 32.9" mà bản sáng đưa ra không phải bằng chứng thước tốt, mà phần lớn phản ánh **bộ trỏ chưa đủ chính xác**.
> - **Chẩn đoán "bộ dò trả nhiều hộp cho cùng một nút" là SAI.** Kiểm lại bằng hộp thật: 286 cặp hộp nằm sát nhau đều có IoU = 0, tức là phần tử riêng biệt (phím bàn phím, dòng danh sách). Nguyên nhân thật là **toạ độ gold là điểm người chạm, không phải tâm nút**. Cách vá đúng là loại hộp chứa điểm gold, và nó cho chênh **19.7** chứ không phải 32.9.
> - **Cổng thao tác đang kết oan 28.6%** cặp (câu mô hình thật, câu gold) vì tách "chạm" khỏi "mở"/"đi tới" — đúng bệnh cũ đổi vỏ. Đã gộp lại thành một lớp, còn **13.2%**.
> - **MDE chưa khoá được.** SD 0.362 không phải số đo mà là giả định; và pilot chỉ ~3.5 bước mỗi app nên nhiễu đo còn lớn hơn cả phương sai quan sát. Phải chạy pilot dày hơn trước khi đăng ký trước.
> - **G tính lại trên đúng 631 episode**: gán được 363, G = 78 app, G hiệu dụng 34.8. Tỉ lệ bước chạm đếm lại là 59.1%.
>
> Lỗ lớn nhất vẫn chưa vá được là "bộ trỏ trúng thì người có làm theo được không", vì cần người chấm.
>
> **Bổ sung 29/7 — đã chốt thành phần thêm cho mô hình.** Trước đây phần này để ngỏ ba nhóm ứng viên. Sau hai vòng phản biện độc lập, chốt **hai lớp**: (1) *trỏ trước viết sau* — bắt mô hình sinh toạ độ rồi mới sinh câu, tận dụng toạ độ có sẵn mà bản thường bỏ phí; (2) *đưa danh sách chữ đọc từ ảnh vào làm đầu vào* — một bộ đọc chữ nhẹ đứng trước mô hình sinh. Ý "tự sinh nhiều câu rồi tự lọc bằng bộ trỏ" hạ xuống lớp tuỳ chọn vì bộ trỏ hiện tại lọc sai quá nửa. Chi tiết và ví dụ ở Phần 3. **Cũng trong ngày tìm được nguồn dữ liệu gỡ hai nút thắt cũ** (câu người viết cho phần train, và cây trợ năng của 99.131 màn) — nhưng đo ra chỉ 12.6% phần tử có tên, nên nó chỉ dùng được cho việc chấm vị trí, xem hộp dữ liệu ở Phần 4.

> **Cách đọc:** mỗi phần viết *lời thường trước*, rồi **hộp kỹ thuật** (công thức + trích dẫn đúng venue) cho chỗ cần chiều sâu. Thuật ngữ giải thích ngay lần đầu.
>
> **Mạch bài:** §0 toàn cảnh một ví dụ → §1 điều đã đổi so lần trước → §2 hệ thống chạy + ba pipeline + dữ liệu (bộ nào dạy, bộ nào chấm) → §3 đóng góp mô hình (**có ví dụ chạy tay cho từng lớp thành phần**) → §4 đóng góp đánh giá (hai thước + bằng chứng số) → §5 những chỗ đã tự kiểm/tự sửa → §6 hai cổng trước khi tiêu tiền → §7 **năm câu hỏi cho thầy** → §8 rủi ro & đường lui → §9 lịch → §10 một câu tóm.

---

## 0. Toàn cảnh chỉ bằng một ví dụ

Một người mở app mua sắm, chụp lại **màn hình đang hiện**, rồi hỏi: *"Làm sao tìm cây cờ lê trong mục Dụng cụ?"*

Mô hình của luận văn nhận **đúng một ảnh đó + câu hỏi**, trả về **hướng dẫn từng bước cho người tự làm**:

> 1. Chạm nút **Filter** ở góc dưới
> 2. Chọn **Tools & Hardware**
> 3. Chọn **Hand Tools**

Điểm khác với mọi mô hình giao diện đang có: chúng sinh **thao tác cho máy tự bấm** (toạ độ, mã lệnh); ở đây ta sinh **câu chữ cho con người đọc và tự làm theo**.

**Cái khó không nằm ở việc sinh câu — mà ở việc CHẤM.** Làm sao biết ba câu trên là *đúng* và *đáng tin*, khi:
- không có sẵn "hướng dẫn chuẩn" do người soạn để đối chiếu, và
- thầy không muốn thuê người ngồi chấm?

Đây là chỗ luận văn có chất nghiên cứu, và cũng là lý do có **hai đóng góp ngang nhau**: (1) **mô hình** sinh hướng dẫn, và (2) **phương pháp chấm** không cần đáp án mẫu, không cần người. Có một điều em muốn nói ngay: gần đây em đã **đo thật** để kiểm chính cái thước chấm này. Kết quả cho thấy nó **vẫn phân biệt rõ câu tốt với câu dở** — đủ để đi tiếp; còn chuyện nó có thật sự đo đúng thứ mình cần hay không thì em đang kiểm nốt bằng khảo sát với người thật. Em xin trình cả số liệu lẫn những chỗ còn hở.

---

## 1. Đề tài và điều đã thay đổi so với lần trước

**Đề tài (không đổi):** mô hình nhận ảnh màn hình + câu hỏi → sinh hướng dẫn nhiều bước cho người.

Lần trước thầy bác vì hướng cũ *chủ yếu gọi API + so chuỗi, chưa có mô hình tự huấn luyện*. Em đã chuyển hẳn sang **huấn luyện một mô hình thật**. Trong lúc chuẩn bị, em chạy vài phép thử miễn phí và chúng **lật một giả định của chính em**, nên em xin báo thẳng:

- **Giả định cũ:** *"mô hình lớn hay bịa tên nút → ta lọc bỏ chỗ bịa → dạy mô hình nhỏ trung thực hơn."*
- **Bị bác bằng số:** em đọc tay 80 màn do gpt-4o-mini sinh → nó **gần như không bịa (~0-2%)**. Những chỗ tưởng "bịa" thật ra là **nút có thật nhưng danh sách nút của hệ điều hành bỏ sót nhãn** (nút hình như dấu cộng, dấu tích).
- **Hệ quả:** vì mô hình gần như không bịa, "lọc bịa" không còn là đóng góp. Em **bỏ khung đó**, chuyển trục chính sang đo **độ ĐÚNG** — hướng dẫn có dẫn tới đúng nút cần bấm không.

Việc em sẵn sàng bỏ một khung mình đã dày công dựng, chỉ vì số liệu nói nó sai, chính là tinh thần em muốn giữ suốt luận văn.

> **Thuật ngữ.** *View Hierarchy (VH)* = danh sách các nút thật trên màn, do Android xuất ra kèm mỗi ảnh (tên nút, vị trí). Nó là "đáp án phụ" để biết nút nào có thật — nhưng không đầy đủ.
>
> **Hộp kỹ thuật.** VH thiếu nhãn nghiêm trọng: >77% ứng dụng thiếu nhãn phần tử [Chen et al., *Distinguished Paper*, ICSE 2020]; đo trên mẫu của em, độ phủ nhãn ≈ 62%, ~20% nút là hình thuần không nhãn. Vì vậy "chỉ đối chiếu VH" không đủ để đo độ đúng → cần thêm một tín hiệu khác là toạ độ (Phần 4).

---

## 2. Hệ thống chạy thế nào — từ đầu đến cuối

Để thầy thấy rõ chỗ nào là "học", chỗ nào là "chấm":

**Lúc DẠY (train):** đưa mô hình từng cặp *(ảnh một bước + mục tiêu)* → *(câu hướng dẫn do người viết cho bước đó)*, để nó bắt chước cách người viết. Nguồn "người viết" lấy từ bộ **AndroidControl** (Phần 3).

**Lúc CHẤM (test):** đưa mô hình **một ảnh app nó CHƯA TỪNG THẤY** + mục tiêu, **không** đưa danh sách nút, **không** đưa đáp án. Nó phải tự nhìn màn hình lạ mà sinh hướng dẫn.

> **Nguyên tắc chống ăn gian.** VH và đáp án chỉ dùng để **dạy** và **chấm điểm** — **không bao giờ** đưa cho mô hình lúc nó sinh. App test tách riêng khỏi app train ("held-out theo app": app dùng để kiểm không xuất hiện lúc dạy). Nhờ vậy, nếu mô hình làm đúng trên app lạ nghĩa là nó **thật sự học được kỹ năng**, không phải học thuộc. Đây cũng là câu trả lời cho "ứng dụng thực tế": khi triển khai, mô hình chỉ cần **ảnh màn hình** — thứ luôn có sẵn.

### Luồng chạy — ba pipeline

Cả luận văn gồm ba luồng nối tiếp nhau. Em tách rõ để thấy chỗ nào là học, chỗ nào là sinh, chỗ nào là chấm.

**① Pipeline huấn luyện.** Từ AndroidControl, mỗi bước của một tác vụ cho em một mẫu học: *đầu vào* = ảnh màn hình của bước đó + mục tiêu của cả tác vụ; *đáp án* = câu hướng dẫn người thật đã viết cho bước đó. Em nạp hàng loạt cặp như vậy cho Qwen2.5-VL-3B qua QLoRA để nó học cách nói giống người viết. Nếu bật thành phần DPO (Phần 3), em đúc thêm từ VH các cặp *câu đúng / câu bịa* để dạy nó tránh gọi nút không có thật.

**② Pipeline lúc chạy (khi người dùng dùng thật).** Người dùng đưa vào một ảnh màn hình + một câu hỏi. Mô hình đọc ảnh, sinh ra bước kế tiếp (hoặc cả chuỗi hướng dẫn). Nó **không** cần VH, không cần đáp án — chỉ cần ảnh. Đây là điểm khiến mô hình dùng được ngoài đời: điện thoại nào cũng có sẵn ảnh màn hình.

**③ Pipeline chấm (đánh giá, chỉ chạy lúc nghiên cứu).** Đây là chỗ có chất mới, chi tiết ở Phần 4. Tóm luồng:

> ảnh + mục tiêu → **[mô hình]** → câu hướng dẫn
> câu (giấu mục tiêu) → **[bộ trỏ]** → toạ độ (x, y) → so toạ độ gold → **thực thi được?**
> lặp cho từng bước → gộp thành **coverage / F1 / thứ tự** (độ ĐÚNG)
> song song: đối chiếu tên nút trong câu với **VH** → **độ bịa** (độ TRUNG THỰC)
> kiểm lại chính thước bằng **bơm lỗi** (nhét lỗi đã biết, xem thước có bắt)

### Dữ liệu — bộ nào để DẠY, bộ nào chỉ để CHẤM

Nói gọn một câu: **chỉ AndroidControl được dùng để DẠY; cả ba bộ đều dùng để CHẤM, mỗi bộ một việc.** Không có bộ nào vừa dạy vừa chấm trên *cùng* dữ liệu — chỗ này em giữ rất chặt để tránh mọi nghi ngờ ăn gian.

| Bộ | Quy mô | DẠY? | Dùng để CHẤM việc gì |
|---|---|---|---|
| **AndroidControl** (Li et al., NeurIPS 2024 D&B) | 15.283 episode / 833 app | ✅ **CÓ** — train split, học từ hướng dẫn do người viết | **độ ĐÚNG** (executability), trên **test app-unseen = 631 episode** |
| ↳ *ghi chú 29/7* | cây trợ năng: 99.131 màn, trung vị 86 phần tử/màn | — | hộp thì đầy đủ nhưng **chỉ 12.6% phần tử có tên** → chỉ dùng cho chấm vị trí, không dùng đo độ bịa |
| **MobileViews** (arXiv 2409.14337, MIT) | 127 màn / 30 app | ❌ **KHÔNG** — chỉ để chấm | **độ TRUNG THỰC** (bịa nút), vì nó có **View Hierarchy** |
| **ScreenSpot-v2** (OS-Atlas, ICLR 2025) | 502 mobile / 334 desktop / 436 web | ❌ **KHÔNG** — chỉ để chấm | **đối chứng bộ trỏ** (Cổng A), vì nó có bbox chuẩn |

**Ba điểm cần nói rõ:**

1. **AndroidControl dùng cả dạy lẫn chấm, nhưng KHÔNG trùng dữ liệu.** Nó có sẵn cách chia "held-out theo app": em dạy trên các app thuộc train split, còn chấm độ đúng trên **631 episode của những app CHƯA HỀ xuất hiện lúc dạy** (app-unseen). Vậy "train và test đều là AndroidControl" nhưng **không có một màn nào bị dùng lại** — đúng chuẩn của chính bộ đó.
2. **MobileViews chỉ để chấm độ trung thực.** Mô hình (train trên AndroidControl) sinh hướng dẫn trên các màn MobileViews *lạ*, rồi em đối chiếu tên nút với View Hierarchy để đếm bịa. MobileViews **không tham gia huấn luyện**, và các app của nó cũng là app lạ với mô hình. Split 18 app / 12 app của MobileViews chỉ để phục vụ nội bộ khâu đo (đã khoá seed 20260710, đã commit).
3. **ScreenSpot-v2 chỉ để kiểm bộ trỏ ở Cổng A** — không dính gì tới huấn luyện mô hình chính.

> **Vì sao phải hai bộ cho hai trục:** AndroidControl **có toạ độ gold** nên đo được độ ĐÚNG, nhưng View Hierarchy của nó thưa. MobileViews **có View Hierarchy đầy đủ hơn** nên đo được độ bịa, nhưng lại không có đáp án chuỗi thao tác để đo độ đúng. Mỗi bộ mạnh đúng chỗ bộ kia thiếu, nên dùng chéo thì kiểm được cả hai mặt. *(Hiện đã tải về máy 200 episode / 1.042 bước AndroidControl để dựng và kiểm hạ tầng; phần còn lại tải khi build.)*

---

## 3. Đóng góp 1 — MÔ HÌNH

Huấn luyện **Qwen2.5-VL-3B** (mô hình ảnh và ngôn ngữ mở, 3 tỉ tham số, chạy được offline) bằng **SFT-LoRA**.

> **Thuật ngữ.** *SFT* = học có giám sát: cho mô hình xem cặp đầu vào/đáp án để bắt chước. *LoRA / QLoRA* = fine-tune nhẹ, chỉ chỉnh một ít tham số thêm vào (chạy được trên một GPU thuê rẻ) thay vì luyện lại cả mô hình.

**Vì sao chọn Qwen2.5-VL-3B?** Bốn ràng buộc dẫn tới lựa chọn này, không phải chọn ngẫu nhiên:

1. **Phải là mô hình MỞ.** Đề tài buộc *tự huấn luyện* + câu chuyện triển khai là *chạy offline chỉ cần ảnh*. gpt-4o / Gemini là mô hình đóng — không fine-tune được, không chạy trên máy. Nên buộc chọn một VLM mở.
2. **Phải NHỎ để train nổi trên Colab.** Máy em không có GPU, phải thuê Colab. Bản **3B + QLoRA** vừa khít một GPU 24GB, train được thật với chi phí thấp. Qwen có nhiều cỡ (3B / 7B) nên nếu 3B yếu thì nâng lên 7B mà không đổi họ mô hình.
3. **Đọc được ảnh giao diện DÀY CHỮ.** Đầu vào là ảnh đầy chữ và icon nhỏ; Qwen2.5-VL xử lý ảnh **độ phân giải cao**, chỗ mà nhiều VLM nhỏ khác đuối vì nén ảnh làm mất chữ nút.
4. **Có tiền lệ ngay trên miền GUI — giảm rủi ro lớn nhất.** Câu hỏi "3B có học nổi kỹ năng GUI không" đã có sẵn bằng chứng: nhiều mô hình GUI gần đây huấn luyện thẳng trên Qwen2.5-VL cỡ 3B và chạy được.

> **Hộp kỹ thuật.** Tiền lệ cùng miền + cùng cỡ: **UI-R1** (AAAI 2026) fine-tune Qwen2.5-VL-3B cho GUI grounding · **ZonUI / Qwen-GUI-3B** (WACV 2026, LoRA 3B trên 1 GPU) · **SE-GUI** (NeurIPS 2025) · **OS-Atlas / Aguvis** cũng dựng trên nền Qwen-VL. Bản 3B/7B giấy phép **Apache-2.0** (dùng được cả nghiên cứu lẫn thương mại). Có sẵn **bản grounding cùng họ** → tiện cho bộ trỏ (Cổng A) và cho nhánh tự cải thiện nếu chọn. *(Đối thủ đã cân nhắc: InternVL2.5-2B/4B, MiniCPM-V, Phi-3.5-vision — Qwen thắng nhờ tiền lệ GUI dày nhất + đọc ảnh phân giải cao + có bản grounding anh em + nhiều cỡ để dự phòng.)*
>
> **Cần thủ khi thầy hỏi "3B nhỏ vậy có gì mới":** chọn Qwen 3B **không phải điểm mới** (mô hình GUI nhỏ đã đông: ZonUI, UI-R1) — nó chỉ là lựa chọn kỹ thuật hợp lý để rẻ và chạy offline. Cái mới nằm ở **tác vụ** (sinh hướng dẫn cho người) + **cách đánh giá**, không ở kích thước.

Em so **ba mô hình** (kèm một mốc sàn để đối chiếu):

| Mô hình | Vai | Học từ đâu |
|---|---|---|
| Qwen-3B chưa fine-tune | mốc sàn tham chiếu | — |
| gpt-4o-mini (không huấn luyện) | baseline NGOÀI — mô hình lớn, mạnh, làm sẵn | không học |
| Qwen-3B SFT-trơn | baseline TRONG — bản fine-tune bình thường | gold người viết |
| **Qwen-3B SFT + trỏ-trước-viết-sau** | bước đóng góp thứ nhất | gold người viết + toạ độ gold |
| **Qwen-3B SFT + trỏ-trước-viết-sau + danh sách phần tử** | **đóng góp đầy đủ của luận văn** | thêm danh sách chữ trên màn (OCR) |

Hai phép so, nhưng em xin xếp rõ **cái nào là kết luận chính, cái nào chỉ là phụ** (một giám khảo tinh sẽ vặn ngay chỗ này):

- **Kết luận CHÍNH = hơn SFT-trơn** (ablation): SFT+thành phần so với SFT-trơn — **cùng một gốc, cùng dữ liệu, chỉ khác đúng một yếu tố**. Hơn ở đây chứng minh **thành phần em thêm có tác dụng thật**, sạch, không dính lợi thế nào khác. Đây là claim em đặt cược.
- **Chỉ là phụ = hơn gpt-4o-mini**: cho thấy *"3B offline ngang/hơn một mô hình API lớn"*. Nhưng em **không** dựng nó làm headline, vì so này **không sạch**: học trò train ngay trên AndroidControl nên thuộc luôn *cách chia bước* của bộ dữ liệu, lại được chấm ở chế độ teacher-forced (mớm đúng ranh giới bước gold) → nó có **lợi thế cấu trúc** ngoài chất lượng, không chỉ lợi thế "cùng miền". Nên đây là con số minh hoạ, không phải bằng chứng đóng góp.

> **Vì sao phân định vậy (thủ sẵn).** Nếu trưng "hơn gpt-4o-mini" làm headline, hội đồng sẽ hỏi "bao nhiêu phần là chất lượng, bao nhiêu là học trò thuộc benchmark?" — câu đó khó trả lời sạch. Còn ablation SFT-trơn vs SFT+thành phần thì *cùng* nhiễm lợi thế sân nhà như nhau nên nó **triệt tiêu trong hiệu số** → hiệu số đo đúng tác dụng của thành phần. *(Nếu cần khẳng định "hơn gpt-4o-mini" cho sạch, em sẽ thêm nhánh Teacher-STYLE-MATCHED: cho gpt-4o-mini vài ví dụ mẫu để nói đúng phong cách + độ dài bước của AndroidControl, rồi mới so.)*

> **Một cái bẫy em ý thức để tránh — trần bắt chước.** *Không* dạy mô hình chính bằng đầu ra của gpt-4o-mini rồi lại lấy gpt-4o-mini làm baseline để vượt — "học từ ai thì cùng lắm bằng người đó". Nên **thầy dạy = gold người viết**, còn **gpt-4o-mini chỉ đóng vai baseline để so**. Kéo theo: "thành phần thêm" cũng không nên là "chưng cất từ gpt-4o".

**"Thành phần thêm" là gì? — đã chốt ngày 29/7 sau hai vòng phản biện.** Trước đây phần này để ngỏ ba nhóm ứng viên và nghiêng về nhóm dạy bằng cặp câu đúng/câu bịa. Sau khi cho hai vòng phản biện độc lập cùng mổ xẻ, thứ tự đã đổi hẳn. Chốt lại: thành phần thêm gồm **hai lớp xếp chồng, cả hai đều dùng đúng thứ dữ liệu mà bản SFT trơn đang bỏ phí**, và cả hai đều rẻ.

**Trước khi vào chi tiết, xin lấy MỘT bước thật làm ví dụ xuyên suốt** (bước này có thật trong dữ liệu, không phải bịa để minh hoạ):

> **Mục tiêu người dùng:** *"Vào app PressReader và tìm bài Saudis to host Ukraine's peace summit"*
> **Màn đang hiện:** trang chủ PressReader, ảnh 1080×2400
> **Bước cần làm:** chạm vào ô tìm kiếm trên đỉnh màn — **toạ độ đúng ghi trong dữ liệu là (540, 191)**
> **Câu hướng dẫn người viết (đây là đáp án để dạy):** *"Click on the search bar at the top of the screen"*

Ba nhánh mô hình sẽ học từ đúng bước này theo ba cách khác nhau, và đó là toàn bộ nội dung phần dưới.

---

**Lớp 1 — trỏ trước, viết sau.**

Bản SFT trơn học ánh xạ: *(ảnh + mục tiêu) → "Click on the search bar at the top of the screen"*. Hết. Toạ độ (540, 191) nằm ngay trong dữ liệu nhưng **không ai dùng tới** — nó bị vứt đi.

Lớp 1 chỉ đổi đúng một chỗ: **đích huấn luyện gồm hai phần, toạ độ trước rồi câu chữ sau.**

> **📦 Ví dụ — đích huấn luyện trông thế nào**
>
> | | Bản SFT trơn học | Bản có lớp 1 học |
> |---|---|---|
> | Đầu vào | ảnh + *"Vào app PressReader và tìm bài…"* | y hệt |
> | Đích | `Click on the search bar at the top of the screen` | `<point>500,80</point> Click on the search bar at the top of the screen` |
>
> `500,80` là toạ độ (540, 191) quy về thang 0–1000 cho khỏi phụ thuộc kích thước màn. Lúc chấm, phần `<point>…</point>` **cắt bỏ**, chỉ lấy câu chữ đem cho bộ trỏ — nên thước không hề nhìn thấy phần toạ độ mô hình sinh ra.

**Vì sao cách này làm mô hình viết tốt hơn.** Hàm mất mát của học có giám sát chỉ nhìn văn bản, nên bản trơn **chưa bao giờ được dạy nút nằm ở đâu**. Nó chỉ học cách bắt chước lối nói. Khi bắt mô hình nói ra vị trí trước, tới lúc viết câu thì phần tử đích đã nằm sẵn trong ngữ cảnh nó vừa sinh — nó tả **đúng cái nút đó**, thay vì tả chung chung. Nói gọn: bắt cam kết trước, rồi mới cho mô tả.

> **Một cách hình dung.** Giống như bảo người ta *"chỉ tay vào nút trước đã, rồi hẵng tả nút đó cho tôi nghe"*. Người phải chỉ tay trước thường tả chính xác hơn người vừa nghĩ vừa tả.

**Vì sao lớp này an toàn nhất trước hội đồng.** Mọi thứ dùng để dạy đều là nhãn **có sẵn trong chính bộ dữ liệu**: câu người viết và toạ độ người thao tác. Không có công cụ bên ngoài nào xuất hiện ở cả phía dạy lẫn phía chấm, nên không có đường nào để vặn "anh luyện đúng vào bài thi". Chi phí gần bằng không: viết một script dựng lại đích rồi chạy một lượt huấn luyện y như bản trơn.

**Rủi ro phải nói trước.** Trên app lạ, mô hình có thể đoán sai vị trí rồi viết câu theo cái vị trí sai đó — lỗi lan truyền. Cách phát hiện: đo luôn tỉ lệ điểm mô hình tự đoán có trúng không. Nếu tỉ lệ đó thấp mà điểm câu chữ vẫn tăng thì phải giải thích được vì sao.

---

**Lớp 2 — đưa danh sách chữ trên màn vào làm đầu vào.**

Đây đúng là kiểu **thành phần đứng trước** mô hình sinh: một bộ đọc chữ (OCR) chạy trước, kết quả của nó được nối vào đầu vào cho mô hình.

> **📦 Ví dụ — vẫn màn PressReader đó, OCR đọc được gì**
>
> Chạy OCR trên ảnh, lấy chữ kèm vị trí. Mười dòng đầu:
>
> | Chữ đọc được | Ở đâu |
> |---|---|
> | `Search Publications, Stories & Interest` | (486, 193) ← **đúng chỗ cần chạm** |
> | `Recommended` | (240, 569) |
> | `See all` | (961, 574) |
> | `THE WALL STREET JOURNAL.` | (333, 681) |
> | `What's` | (103, 771) |
> | … | … |
>
> Danh sách này nối vào đầu vào, đại khái: *"Trên màn có: [Search Publications, Stories & Interest — trên đỉnh] [Recommended — giữa trái] [See all — giữa phải] …"*. Đưa cả lúc dạy **và** lúc chạy thật.

**Vì sao nó giúp.** Chỗ yếu nhất của một mô hình 3 tỉ tham số là **đọc chữ nhỏ trên ảnh giao diện**. Có danh sách rồi thì việc của nó nhẹ hẳn: từ *"nhìn ảnh rồi đoán xem nút tên gì"* thành *"chọn đúng dòng trong danh sách rồi chép tên ra"*. Chép dễ hơn nhận dạng rất nhiều.

Và đây không phải phỏng đoán — pilot của chính đề tài đã đo đúng cơ chế này: câu nói cộc lốc chỉ trỏ trúng **35%**, còn câu tả rõ phần tử trỏ trúng **69%**. Danh sách chữ chính là thứ đẩy mô hình từ nhóm đầu sang nhóm sau.

> **📦 Ba nhánh viết ra gì — cùng một bước, khác nhau ở chỗ nào**
>
> | Nhánh | Câu nó sinh ra | Bộ trỏ lần ra được không |
> |---|---|---|
> | SFT trơn | *"Tap the search bar"* | mơ hồ, dễ trỏ nhầm sang thanh khác |
> | + lớp 1 | *"Tap the search bar at the top of the screen"* | khá hơn, có vị trí |
> | + lớp 1 + lớp 2 | *"Tap the 'Search Publications, Stories & Interest' bar at the top"* | gọi đúng tên nhìn thấy trên màn nên dễ lần ra nhất |

**Khoá chống vòng vo.** Danh sách đưa vào lúc dạy lấy từ **OCR**; còn danh sách nút dùng lúc **chấm** lấy từ nguồn khác hẳn (bộ dò hình, hoặc cây trợ năng). Hai nguồn khác bản chất: OCR chỉ thấy chữ, không thấy nút hình; bộ dò hình thì ngược lại.

**Hai đối chứng bắt buộc — thiếu là bị đập ngay:**

> **(a) Nhánh "chỉ đưa lúc chạy".** Lấy chính bản SFT trơn, lúc chạy cũng đưa danh sách cho nó. Nếu bản này cũng tốt lên bằng bản được huấn luyện với danh sách, thì đóng góp không phải ở chỗ huấn luyện mà chỉ ở chỗ đưa thêm thông tin — tức là prompting, đúng thứ thầy đã bác. Phải chạy nhánh này để chứng minh **việc dạy mô hình biết dùng danh sách** mới là cái đáng giá.
>
> **(b) Nhánh giả dược.** Đưa danh sách chữ **của một màn khác** — thông tin sai hoàn toàn. Nếu điểm **vẫn** tăng thì hiệu ứng chẳng liên quan gì tới nội dung danh sách, nó chỉ đến từ việc câu dài ra và thước thì thích câu dài. Gặp trường hợp đó thì phải tự bác, không được nhận là mô hình tốt hơn.

> **Một điều thành thật về câu chuyện triển khai.** Trước đây hồ sơ nói *"lúc chạy chỉ cần ảnh màn hình"*. Với lớp 2 thì cần thêm một bước OCR chạy trước. Điều này **không phá** câu chuyện đó, vì OCR chạy được ngay trên điện thoại, không cần mạng, không cần quyền đặc biệt — bản OCR đề tài đang dùng chạy trên máy không GPU vẫn được. Nhưng phải nói rõ với thầy: hệ triển khai gồm hai phần, một bộ đọc chữ nhẹ và một mô hình sinh, chứ không phải một mô hình duy nhất.

---

**Còn ý mô hình tự sinh nhiều câu rồi tự lọc để học lại thì hạ xuống lớp tuỳ chọn.**

Ý này rất tự nhiên và em đã cân nhắc kỹ, nên xin trình bày đầy đủ cả cách làm lẫn lý do hoãn.

> **📦 Cách làm sẽ như thế này** — vẫn bước PressReader ở trên:
>
> Cho mô hình đã huấn luyện tự sinh 6 câu cho cùng một màn, rồi đưa từng câu cho một bộ trỏ xem nó lần ra chỗ nào:
>
> | Câu mô hình tự sinh | Bộ trỏ chỉ vào | Giữ lại? |
> |---|---|---|
> | *"Tap the search bar at the top"* | (530, 200) — sát chỗ đúng | ✓ |
> | *"Tap 'Search Publications, Stories & Interest'"* | (486, 193) — đúng ô | ✓ |
> | *"Tap the search icon"* | (985, 190) — kính lúp bên phải, nút khác | ✗ |
> | *"Open the menu"* | (60, 190) — nút khác hẳn | ✗ |
>
> Giữ hai câu ✓, gom lại thành bộ dữ liệu mới, huấn luyện thêm một lượt trên đó. Ý tưởng: đáp án gốc chỉ ghi **một** cách nói, nhưng thực tế có nhiều cách nói đúng — cách này bổ sung những cách nói đúng mà đáp án gốc thiếu.

**Ba lý do hoãn, đều bằng số chứ không phải cảm tính:**

**1. Người gác cổng đang hỏng.** Toàn bộ ý tưởng đứng trên giả định "bộ trỏ nói câu nào đúng thì câu đó đúng thật". Nhưng đo hôm 28/7 cho thấy bộ trỏ rẻ hiện tại **kết oan 42 đến 59% số câu đúng**, và nó trả toạ độ trên lưới thô tới mức một nấc còn rộng hơn khoảng cách giữa hai nút cạnh nhau.

> **Hệ quả tính ra được.** Giả sử một nửa số câu mô hình sinh là đúng. Bộ trỏ giữ lại khoảng một nửa số câu đúng đó, đồng thời giữ nhầm một phần số câu sai. Kết quả: cái gọi là "bộ dữ liệu đã kiểm chứng" chỉ **sạch cỡ 70%** — tức là huấn luyện lại trên dữ liệu mà **một phần ba nhãn sai**, trong khi đã **vứt đi một nửa số câu đúng**. Đó không phải chưng cất có kiểm chứng, đó là bơm nhiễu có hệ thống vào mô hình.
>
> Muốn cách này có nghĩa thì bộ trỏ phải giữ đúng gần hết câu đúng và hiếm khi giữ nhầm — cụ thể là trúng trên 85% và giữ nhầm dưới 10%, đo trên chính AndroidControl chứ không mượn số của bộ dữ liệu khác.

**2. Đắt nhất trong mọi phương án.** Phải sinh vài chục nghìn câu rồi chạy bộ trỏ trên từng câu một. Ước tính ngốn phần lớn ngân sách huấn luyện, không còn biên cho một lần chạy hỏng — mà lần chạy đầu tiên hỏng là chuyện bình thường.

**3. Mang đúng tiếng luyện đúng bài thi.** Dùng bộ trỏ để chọn dữ liệu dạy, rồi lại dùng bộ trỏ để chấm. Dù chọn hai bộ trỏ khác họ thì chúng vẫn cùng một "gu" (đều thích câu dài, câu tả vị trí). Hội đồng sẽ hỏi ngay: *điểm tăng vì mô hình viết tốt hơn, hay vì nó học cách chiều đúng cái máy sẽ chấm nó?* Câu này khoá được một phần nhưng không xoá hẳn.

> **Nếu sau này vẫn muốn chạy thì phải qua cổng riêng, ba điều kiện:** bộ trỏ dùng để lọc tự đo trên ít nhất 100 bước gán tay của chính AndroidControl, đạt trúng trên 85% và giữ nhầm dưới 10%; bộ trỏ lọc khác họ với bộ trỏ chấm; và báo kèm một thước không dùng bộ trỏ để đối chiếu. Chạy nó như **lớp thứ ba chồng lên hai lớp trên**, không phải trụ chính.

---

**Vậy thứ tự thí nghiệm sẽ là bốn mốc trên cùng một trục**, mỗi mốc thêm đúng một thứ so với mốc trước, nên đọc được đóng góp của từng phần:

| Mốc | Thêm gì so với mốc trước | Chi phí thêm |
|---|---|---|
| Qwen-3B chưa huấn luyện | — | 0 |
| SFT trơn | học câu người viết | một lượt huấn luyện |
| + lớp 1 | dùng thêm toạ độ có sẵn | gần như không |
| + lớp 2 | thêm danh sách chữ trên màn | một lượt huấn luyện + OCR chạy trên máy |

> **Một lớp vá dùng chung cho cả hai lớp.** Cả lớp 1 lẫn lớp 2 đều làm câu đầu ra **dài và tả rõ hơn**, mà thước thì đã đo được là **thiên vị câu dài** (câu ngắn trúng 35%, câu dài 69%). Nên khi báo kết quả phải: (a) **phân tầng theo độ dài câu** — so trong từng nhóm câu ngắn, vừa, dài riêng; (b) báo phân bố độ dài trước và sau; (c) chấm tay vài chục câu bằng bộ chấm người đã dựng sẵn. Nếu toàn bộ hiệu số nằm ở chỗ câu dài ra thì tự bác, không nhận là mô hình tốt hơn. Chi phí của ba việc này gần bằng không, nhưng thiếu chúng thì con số dù đẹp cũng không bảo vệ được.

---

**Quan hệ với công trình đã có — tra ngày 29/7, và kết quả buộc phải hạ giọng ở vài chỗ.**

Trước khi trình hai lớp này, em cho tra tài liệu để biết chỗ nào là mới thật, chỗ nào đã có người làm. Kết quả tóm gọn: **cả hai lớp đều có tiền lệ, nên không lớp nào được kể là phát minh.** Chỗ còn lại của em là tổ hợp và là miền áp dụng.

**Với lớp 1 (trỏ trước viết sau):**

| Công trình | Đã làm gì | Khác em chỗ nào |
|---|---|---|
| **GCoT** (preprint 2503.12799) | So thẳng hai thứ tự sinh: trả lời trước rồi mới ra toạ độ, và **định vị trước rồi mới trả lời** | Miền hỏi đáp ảnh thường, đích là câu trả lời ngắn; em ở miền giao diện, đích là câu hướng dẫn cho người và **cắt bỏ toạ độ lúc chấm** |
| **Shikra** (preprint 2306.15195) | Mô hình tự nêu toạ độ vật thể trong phần suy luận trước khi trả lời | Ảnh thường, mục tiêu là tăng độ đúng của câu trả lời |
| **CogCoM** (ICLR 2025), **Visual CoT** (NeurIPS 2024) | Sinh hộp làm bằng chứng trước rồi mới kết luận | Đa lượt, có cắt ảnh rồi mã hoá lại; em giữ một chuỗi duy nhất |
| **Aguvis** (ICML 2025), **UI-R1** (AAAI 2026) | Trong miền giao diện, đặt **chữ trước rồi toạ độ sau**. Đã mở PDF Aguvis xác nhận khuôn mẫu huấn luyện: `Thought: … / Low-level Instruction: … / Action: pyautogui…` — tức mô hình **tự sinh cả câu chỉ dẫn mức thấp**, rồi mới tới hành động | Em **đảo đúng hai vai**. Ở họ, câu chữ là bước suy luận trung gian để ra hành động cho máy, và **chất lượng câu đó không được đánh giá**; ở em câu chữ là **sản phẩm cuối cho người đọc** và là thứ duy nhất đem chấm, còn toạ độ bị cắt bỏ |

> **Một kết quả của GCoT em phải nêu vì nó ngược chiều mình.** Họ đo được rằng khi bắt định vị trước, **khả năng định vị tốt lên nhưng độ đúng của câu trả lời lại kém đi**. Nếu chuyện đó lặp lại ở đây thì lớp 1 hỏng. Hai lý do em vẫn cho là đáng thử: (a) thứ em cần cải thiện chính là phần định vị, còn "độ đúng của câu trả lời ngắn" không phải thứ em đo; (b) phép đo của họ là ra lệnh cho mô hình chưa huấn luyện, còn ở đây mô hình **được huấn luyện** với thứ tự đó. Nhưng đây là giả thuyết, và nếu số cho thấy ngược lại thì em báo đúng như vậy.

**Với lớp 2 (danh sách chữ làm đầu vào) thì nặng hơn, và em xin nói thẳng:**

> **Bài gốc của chính bộ AndroidControl đã làm chuyện tương tự.** Trong bài NeurIPS 2024, mô hình nền của họ được fine-tune với **đầu vào là danh sách phần tử trích từ cây trợ năng** (loại, chữ, mô tả, hộp bao, các cờ trạng thái) và thậm chí **không dùng ảnh màn hình**: *"Our agent implementation does not directly leverage the page screenshot."* Ngoài ra **Mind2Web** (NeurIPS 2023) đã huấn luyện mô hình sinh trên danh sách ứng viên nhiễu do một module rẻ hơn lọc ra, và **Widget Captioning** (EMNLP 2020) đã huấn luyện với cây phần tử ở đầu vào kèm ablation từng nguồn. Câu hỏi "huấn luyện với ngữ cảnh nhiễu có hơn chỉ đưa lúc chạy không" thì **RAFT** (COLM 2024) đã trả lời là có, ở miền truy hồi văn bản.
>
> **Hệ quả:** lớp 2 **không được kể là đóng góp**. Nó là một lựa chọn thiết kế có ablation đàng hoàng. Ai hỏi thì em trả lời thẳng rằng kỹ thuật này đã phổ biến, và chỉ ra ba chỗ khác: đầu ra của em là câu cho người đọc chứ không phải hành động cho máy; nguồn danh sách là chữ do bộ đọc chữ trích ra, có sai sót đo được, chứ không phải cây phần tử sạch của bộ dữ liệu; và em có nhánh giả dược mà vòng tra không tìm thấy ai làm trong miền này.

> **Một điểm phân định quan trọng vẫn đứng vững.** Trong bài gốc AndroidControl, trường `step_instructions` là **đầu vào** — chỉ dẫn mức thấp mớm cho agent để nó dự đoán hành động. Ở đây em dùng chính trường đó làm **đích phải sinh ra**. Hai hướng ngược nhau, và đây là chỗ định vị đóng góp rõ nhất so với mọi công trình dùng bộ dữ liệu này.

**Cách phát biểu em sẽ dùng, và những chữ em bỏ hẳn.** Nói: *"áp dụng thứ tự sinh định-vị-trước, vốn đã được nghiên cứu ở hỏi đáp ảnh thường, sang tác vụ sinh hướng dẫn giao diện cho người đọc, dùng nhãn toạ độ vốn bị bỏ không"*. Bỏ hẳn: *"đầu tiên"*, *"cơ chế mới"*, và bỏ luôn việc đặt tên kêu cho thứ tự sinh rồi dùng như thể đó là thuật ngữ chuẩn ngành.

**Ba đối chứng cho lớp 1** (đối xứng với hai đối chứng của lớp 2, và chỗ này vòng tra chỉ ra em còn thiếu):

> **(a) Có và không có phần toạ độ**, cùng dữ liệu, cùng số vòng huấn luyện.
> **(b) Toạ độ SAI hoặc ngẫu nhiên** đặt ở đầu. Nếu điểm vẫn tăng thì cái tăng đến từ chuỗi dài thêm chứ không phải từ việc định vị đúng. Đây là đòn đầu tiên một người phản biện tử tế sẽ đánh.
> **(c) Toạ độ cho sẵn trong đầu vào** (kiểu mô tả phần tử có bbox cho trước) làm **trần trên** — vừa là mốc so, vừa là chỗ nối vào dòng nghiên cứu đã có.
>
> Kèm một lưu ý kỹ thuật: phần toạ độ làm chuỗi dài ra và đổi phân bố mất mát trên các chữ của câu, nên hai nhánh không cùng ngân sách chữ. Nếu muốn kín kẽ thì nhánh đối chứng phải có một tiền tố giả cùng độ dài.

---

> **Liêm chính:** cơ chế tự cải thiện (RFT/RLVR-point-in-bbox) đã có trên các mô hình GUI-agent (UI-R1 AAAI 2026, SE-GUI NeurIPS 2025) nhưng cho *thao tác cho máy*, chưa ai áp cho *sinh hướng dẫn cho người* → em kể là "áp dụng vào tác vụ mới", không nhận là phát minh máy móc mới.

---

## 4. Đóng góp 2 — PHƯƠNG PHÁP ĐÁNH GIÁ (chỗ có chất mới)

Vì thầy không muốn chấm bằng người, em thiết kế một **quy trình đánh giá khách quan, tự động**. Nó không phải chỉ hai con số, mà là một giao thức gồm:

| Thành phần | Nội dung |
|---|---|
| **Trục ĐÚNG** | executability (test từng bước) → gộp thành **coverage** (phủ đủ bước) + **F1** (không nhồi bước thừa/bịa) + **thứ tự** |
| **Trục TRUNG THỰC** | faithfulness (bịa nút) — trục phụ |
| **Các khoá chống ăn gian** | lượt "không có câu" làm sàn; **thước thứ ba độc lập** (mô hình khác họ chấm "hữu ích cho người") khi dùng thành phần tự cải thiện |
| **Cách validate chính thước** | bơm lỗi (đã lật được thước cũ — Phần 5). **Đã chạy 28/7 cho thước mới, bản 2: đạt 8/10 ngưỡng khoá trước.** Bản 1 trong cùng ngày bị chính vòng phản biện bác vì phần lớn nhánh không thể rớt; hai chỗ rớt của bản 2 được báo nguyên trạng vì chúng chỉ ra đúng điều kiện chặn đường. Số: `harness/exec_injection_validate.py`. |
| **Phát hiện đo lường** | bốn phép thử K1/K2/OCR/việc-1 (giải nghĩa ngay dưới) + "không thước so chuỗi nào tách nổi nút icon" — bản thân đây là đóng góp |

> **Bốn phép thử "phát hiện đo lường" là gì** (đều miễn phí, đã chạy — chúng chính là cái dẫn em tới thiết kế này):
> - **K1** — kiểm bộ đối chiếu bằng embedding: nó **sai cả hai chiều** (bỏ lọt câu bịa nghe giống thật, lại kết oan nút gọi đúng nhưng bằng từ khác), hai loại chồng điểm nhau nên **không ngưỡng nào tách được** → lý do bỏ hẳn cách đo "so nghĩa".
> - **K2** — đọc tay 80 màn teacher sinh: **bịa thật chỉ ~0–2%**; 35/40 ca tưởng "bịa" thật ra là **nút có thật mà VH thiếu nhãn** → lật giả định "lọc bịa".
> - **OCR** — thử bù nhãn VH bằng OCR: cứu được nút có chữ (+6 điểm phủ) nhưng **không cứu nổi icon hình thuần** (+, ✓, mũi tên) → VH+OCR vẫn còn ~20% nút là sàn kết oan.
> - **Việc-1** — thử câu "fallback" chung chung: hầu hết chỉ **lặp lại mục tiêu**, làm hướng dẫn tệ đi → cách chữa là *giảm* fallback (nâng bộ đối chiếu), không phải viết câu hay hơn.

### Thước 1 — Executability (độ ĐÚNG: hướng dẫn có trỏ đúng chỗ không)

**Ý tưởng bằng lời:** giấu mục tiêu đi, đưa *chỉ mỗi câu hướng dẫn* cho một **bộ trỏ**, xem nó có lần ra đúng nút không. Nếu một câu đủ rõ để bộ trỏ (đóng vai người dùng) chạm trúng, thì câu đó *đúng*.

> **Thuật ngữ.** *Bộ trỏ (grounder)* = một mô hình chuyên: đưa nó **ảnh + một câu** như "chạm nút Tìm kiếm", nó chỉ ra **điểm (x, y)** nên chạm. Ta dùng nó như một "người dùng máy móc" làm theo hướng dẫn.

**📦 Ví dụ chạy tay** (màn thật — app Snapdeal, ảnh 1080×2400 pixel, bước = bấm nút **Filter**, toạ độ đúng = **(854, 2275)**):

| Mô hình | Câu sinh ra |
|---|---|
| gpt-4o-mini | "Tap the funnel-shaped filter icon at the bottom right" |
| SFT-trơn | "Tap filter" |
| Mô hình mình | "Tap the Filter button at the bottom" |

Chấm câu **"Tap filter"**: đưa bộ trỏ ảnh + đúng câu đó (không nói mục tiêu, không nói đáp án) → nó đoán điểm chạm, ví dụ **(860, 2270)** → lệch = √(6²+5²) ≈ **7.8 pixel**. Dung sai cho phép = 14% cạnh màn ≈ **151 pixel**. 7.8 ≪ 151 → **TRÚNG**.

Ba tính chất làm thước này vững:

- **Giọng văn ÍT ăn gian hơn so-chuỗi — nhưng KHÔNG miễn nhiễm (em nói rõ, đã đo).** Ý tưởng: "funnel icon" và "Filter button" cùng trỏ về nút Filter nên thước không thưởng trùng-chữ như so-chuỗi. NHƯNG em đo trên 76 câu gold thì bộ trỏ gpt-4o-mini **vẫn thiên vị câu DÀI**: câu ngắn trúng 35%, câu dài trúng 69% (tương quan +0.327). Mà học trò (nói cộc "Tap X") và gpt-4o-mini (nói dài) khác nhau đúng ở độ dài → so **học trò vs gpt-4o-mini** vẫn bị nhiễu giọng. **Hai hệ quả:** (a) đây là lý do em KHÔNG dựng "hơn gpt-4o-mini" làm headline (đã nói ở §3); (b) với **bộ trỏ chuyên** thì độ thiên vị này phải **đo lại ở Cổng A** (test giữ-nguyên-nghĩa-đổi-giọng) trước khi tin. Với **ablation** (học-trò-trơn vs học-trò+thành-phần) thì hai bên **cùng giọng** nên nhiễu này triệt tiêu — đó là thêm một lý do headline đặt ở ablation.
- **Bắt được câu sai.** Nếu mô hình nói nhầm "Tap the search bar" → bộ trỏ lần ra ô tìm kiếm trên đỉnh, cách đáp án rất xa → **TRẬT** (0 điểm bước đó).
- **Chống "màn quá dễ".** Có người sẽ vặn: *"màn chỉ có một nút to thì câu vớ vẩn cũng trúng."* Nên em chạy thêm một lượt **không đưa câu** (chỉ ảnh) làm **sàn**. Phần câu *thật sự đóng góp* = có câu − không câu.

> **Hộp kỹ thuật.** Với câu sinh *s* trên màn có hành động đúng (x\*, y\*), bộ trỏ đông cứng *G* cho ra (x̂, ŷ) = *G*(ảnh, s). Bước *thực thi được* nếu khoảng cách( (x̂,ŷ), (x\*,y\*) ) ≤ τ·D, với D = kích thước màn, τ = 0.14 [ngưỡng dung sai AITW, NeurIPS 2023]. Đây đúng là tiêu chí *step-accuracy* của AndroidControl [Li et al., NeurIPS 2024 D&B], nhưng áp cho **câu hướng dẫn đã nối đất** thay vì cho toạ độ mô hình tự dự đoán. Control: chạy *G*(ảnh, ∅) làm sàn; giá trị thông tin của câu = Exec(s) − Exec(∅).

### 🔬 Bằng chứng thước phân biệt được câu tốt với câu dở (mức tối thiểu)

Em xin **nói rõ ranh giới ngay để khỏi nói quá**: mấy số dưới đây chứng minh thước **có phân biệt được câu tốt với câu dở** — đó là điều tối thiểu một cái thước phải làm được. Nhưng nó **chưa** chứng minh được điều quan trọng hơn: bộ trỏ trúng thì người có thật sự làm theo được không. Cái đó em kiểm riêng bằng khảo sát 91 cặp với người thật ở Phần 5, **chưa chạy**. Em phân định kỹ vì đúng chỗ này thước *cũ* đã ngã — nó cũng từng được tin "đã kiểm" trước khi thật sự kiểm. Số đo tự động trên AndroidControl:

| Câu hỏi kiểm | Đo được | Ý nghĩa |
|---|---|---|
| Không đưa câu, bộ trỏ đoán bừa thì trúng bao nhiêu? (**sàn**) | **6.6%** | sàn THẤP → thước còn nhiều chỗ để phân biệt |
| Đưa câu đáp án chuẩn thì trúng bao nhiêu? (**trần**) | 51.3% | với bộ trỏ rẻ; bộ trỏ chuyên sẽ cao hơn |
| **Độ chênh (trần − sàn)** | **+44.7** với cách chấm đĩa · **+19.7 đến +34.2** với các cách chấm chặt | câu hướng dẫn giúp rõ hơn hẳn đoán bừa, ở mọi cách chấm |
| Khoảng cách trung vị bộ trỏ | 0.150 (có câu) → **0.433** (không câu) | câu kéo bộ trỏ từ "bừa" về "sát", rất tách bạch |

**Đọc con số này thế nào cho thầy:** em từng tự lo *"dung sai 14% rộng quá, đoán bừa cũng hay trúng → sàn cao → hiệu số chẳng còn bao nhiêu"*. Em đo thật thì **ngược lại** — sàn chỉ 6.6%. Lý do: một màn có ~24 vùng chữ, đoán bừa mà trúng đúng *cái* nút cần thì vẫn hiếm. Nghĩa là khi mô hình đạt điểm cao, phần lớn điểm đó **đến từ chất lượng câu**, không phải từ dung sai dễ dãi. Con số minh hoạ "72 − 30 = 42" mà em trình trước đây hoá ra còn *thận trọng* — sàn thật chỉ ~7.

> **Hộp kỹ thuật (tái lập được).** Sàn Exec(∅): `harness/ground_floor.py` → `ground_floor_results.json` (76 bước click app-unseen, gpt-4o-mini bản grounding, dung sai τ=0.14). Trần Exec(gold): `harness/ground_pilot.py` → hit@14%=0.513, n=76. Mật độ nút gây nhiễu (dưới đây): `harness/ac_density_check.py`.

**Một giới hạn riêng em xin nói rõ (không lấy sàn ra chống chế):** trên AndroidControl, **63.2%** số bước có ít nhất một nút *khác* nằm trong vùng dung sai (đo bằng OCR lấy tâm hộp chữ làm nút proxy — con số thật còn cao hơn, vì OCR không đọc được nút hình thuần). Đây là chuyện **khác** với sàn: sàn đo "đoán bừa không câu", còn mật độ đo "câu SAI-mà-hợp-lý có bị đĩa 151px chấm nhầm sang nút cạnh không" — hai cơ chế lỗi độc lập, con số sàn thấp **không** giải toả được cái này. Gần nửa số bước có ≥2 nút trong vùng dung sai → thước (bản đĩa) **còn dễ dãi** (câu chưa thật đúng vẫn có thể được cho qua). **Cách xử — đã CODE cơ chế, CHƯA kiểm trên dữ liệu thật** (`harness/metric_exec.py`): chấm theo *nút đúng gần nhất* (Voronoi) — điểm bộ trỏ chỉ tính TRÚNG khi nút gold là nút **gần nhất**, nên câu trỏ nhầm nút cạnh **rớt** dù lọt đĩa. Tự kiểm 4 ca (kể cả ca "trỏ nút cạnh") qua khi inventory hoàn hảo. ⚠️ **NHƯNG Voronoi cần DANH SÁCH ĐẦY ĐỦ nút trên màn — mà bản AndroidControl trên HuggingFace KHÔNG có bbox phần tử** (đã kiểm mọi mirror: wangyuanlei/reece124/ckg đều không có; a11y chỉ ở bản GCS gốc). Nếu lấy nút bằng OCR thì thủng hai chiều (bỏ nút icon + chèn hộp rác — chính report/75). → **Cách gỡ (bước data, xem hộp dưới): dùng bộ dò phần tử (OmniParser) chạy trên ảnh để lấy inventory.** **Em đã tính thử LOCAL (free) dưới ba cách chấm** — con số này rất quan trọng và em nói rõ (`harness/voronoi_recheck.py` + `voronoi_omniparser.py`, dùng bộ dò phần tử OmniParser-v2 chạy CPU):

| Cách xử lý danh sách nút | trần (câu gold) | sàn (không câu) | chênh |
|---|---|---|---|
| đĩa dung sai (không dùng danh sách nút) | 51.3% | 6.6% | +44.7 |
| tâm hộp, không xử lý gì | 13.2% | 0.0% | +13.2 |
| tâm hộp, gộp tâm sát nhau (12–32dp) | 32.9–34.2% | 0.0% | +32.9 … +34.2 |
| **hộp, loại hộp chứa điểm gold** (đúng bản chất nhất) | **19.7%** | 0.0% | **+19.7** |
| hộp lớn, loại hộp chứa điểm gold | 22.4% | 0.0% | +22.4 |
| tâm từ OCR (nguồn khác hẳn), gộp sát nhau | 35.5% | 2.6% | +32.9 |
| **cây trợ năng thật** (62 phần tử/màn), loại hộp chứa gold | **6.6%** | 0.0% | **+6.6** |

> **⚠️ Đọc bảng này rất cẩn thận — đây là chỗ em suýt nói quá hai lần trong cùng một ngày.**
>
> **Lần một:** bản trước ghi chênh 13.2 và kết luận "dải thật [13…45]". Sai, vì cách chấm đó để hộp của *chính nút đang chạm* cạnh tranh với điểm gold (toạ độ gold là chỗ người thật chạm, không phải tâm nút).
>
> **Lần hai:** bản vá buổi sáng đưa chênh lên 32.9 và giải thích rằng bộ dò "trả nhiều hộp cho cùng một nút". Giải thích đó cũng **sai**: kiểm lại bằng hộp thật thì 286 cặp hộp nằm sát nhau đều có phần chồng nhau bằng 0, tức là các phần tử riêng biệt nằm gần (phím bàn phím, dòng danh sách). Cách gộp theo bán kính vì thế **xoá nhầm cả phần tử thật**, và 32.9 là con số của một phép nới tay chứ không phải của một phép siết đúng.
>
> **Con số trung thực:** chấm đúng bản chất (loại mọi hộp chứa điểm gold, phần còn lại mới là nút khác) cho chênh **+19.7**. Dưới mọi cách xử lý chặt, chênh nằm trong khoảng **19.7 đến 34.2**, luôn dương rõ. Với n = 76, khoảng tin cậy của một tỉ lệ quanh 30% đã là ±10 điểm, nên **không nên trưng bất kỳ con số lẻ nào như thể nó chính xác tới từng điểm**. `harness/voronoi_sensitivity.py`.

> **Bổ sung 29/7 — đo với danh sách nút THẬT.** Sau khi lấy được cây trợ năng của bộ dữ liệu (62 phần tử hiển thị mỗi màn, hệ toạ độ đã kiểm là khớp ảnh: điểm gold nằm trong hộp ở **76/76** màn), trần dưới cách chấm chặt chỉ còn **6.6%**. Ba con số giải thích trọn vẹn: phần tử cần chạm rộng **189 × 126 px**, phần tử **khác** gần nhất chỉ cách **69 px**, mà bộ trỏ rẻ lệch trung vị **256 px**. Bộ trỏ lệch xa hơn cả khoảng cách sang phần tử bên cạnh nên gần như luôn rơi vào ô của phần tử khác. → **Con số thấp này đo dụng cụ, không đo câu hướng dẫn.** Và nó cho ngưỡng Cổng A một căn cứ chắc hơn: sai số bộ trỏ phải nhỏ hơn 69 px, nên đặt 3% cạnh màn (~32 px) là có biên an toàn.

**Và một giới hạn nặng hơn cả con số: cách chấm chặt hiện chưa dùng được.** Bơm lỗi cho thấy khi điểm trỏ lệch nhiều thì thước chấm theo nút gần nhất kết oan phần lớn câu đúng:

> ⛔ **Sửa 6/8 — câu này trước ghi "mức lệch thật của bộ trỏ rẻ (trung vị 87 pixel, tức 8% cạnh)". Sai, đã rút.** 87 px lấy từ `real_offsets()` (`exec_injection_validate.py:144`), hàm **chỉ tính trên những ca bộ trỏ ĐÃ trúng dung sai** — lọc bỏ hết phần trượt rồi mới lấy trung vị. Chính đoạn ngay bên trên, dòng 388, đã ghi số không lọc: **256 px**, tức 23,7% bề ngang. Hai con số chỏi nhau cách nhau hai dòng trong cùng một file. Số đúng để dùng là 256 px; đo lại 6/8 trên tập kiểm bằng đúng dụng cụ cổng A cho **29,3%** (n=10). Bảng dưới vì vậy phải đọc là "kết oan ở từng mức lệch giả định", **không** phải "mức thật là 8%".

| Điểm trỏ lệch khỏi gold | 1% cạnh | 3% | 5% | 8% (mức thật) | 13% |
|---|---|---|---|---|---|
| Thước kết oan câu đúng | 0% | 2.6% | 25.0% | **42.1%** | 60.5% |

Nghĩa là phần lớn cái gọi là "trật" dưới cách chấm chặt đến từ **bộ trỏ chưa đủ chính xác**, chứ không phải từ câu hướng dẫn dở. Cách chấm đĩa thì ngược lại: khoan dung với sai số bộ trỏ nhưng dễ dãi với nút cạnh. **Chưa có cách chấm nào vừa chặt vừa dùng được với bộ trỏ hiện tại — đây chính là phát hiện, và là lý do Cổng A quyết định sống còn:** nếu bộ trỏ chuyên đưa sai số trung vị xuống dưới ~3% cạnh thì cách chấm chặt mới có nghĩa; nếu không, phải quay về đĩa và nói rõ giới hạn nút cạnh.

> **📦 HỘP DỮ LIỆU — nút thắt "AndroidControl không có danh sách nút" đã gỡ được MỘT NỬA (đo ngày 29/7).**
>
> Trước đây phần này ghi rằng muốn có danh sách nút thì phải tải bản gốc trên Google Cloud, nặng vài GB và phải cài tensorflow, nên hoãn lại. Nay tìm được một bản đã trích sẵn trên HuggingFace (`HarrytheOrange/parsed_AndroidControl`) gồm hai thứ:
>
> - **`step_instructions` cho cả 15.283 episode** — tức nguồn dạy chính cũng lấy được cho phần train, chuyện vẫn treo từ đầu. Bản khác (`ckg/…WithImages-20k`) tuy có ảnh nhưng đã bị chuyển sang định dạng thao-tác-cho-máy và **mất hẳn trường câu người viết**, nên không dùng làm nguồn dạy được.
> - **Cây trợ năng của 99.131 màn** trong một file 452 MB, tải thẳng, không cần tensorflow. Đã kiểm: **cả 76 màn đang dùng để đo đều có** trong đó.
>
> **Nhưng phải đo trước khi mừng, và em đã đo.** Lấy ngẫu nhiên 120 màn, đếm các phần tử của app đang hiển thị:
>
> | | Kết quả |
> |---|---|
> | Số phần tử của app trên một màn | trung vị **86** (bộ dò hình chỉ ra ~24) |
> | Phần tử **có tên** (chữ hoặc mô tả) | **12.6%** |
> | Màn không có phần tử nào có tên | **22/120** |
> | Màn có quá nửa phần tử có tên | **1/120** |
>
> **Đọc con số này:** cây trợ năng cho **hộp** rất đầy đủ nhưng gần như **không cho tên**. Đúng vấn đề mà tài liệu ngành đã chỉ ra từ lâu (trên 77% app thiếu nhãn phần tử, Chen và cộng sự, ICSE 2020) — chỉ là ở đây nó còn nặng hơn con số 62% đo trên MobileViews trước đây.
>
> **Vậy dùng nó vào việc gì và không dùng vào việc gì:**
>
> - ✅ **Dùng cho việc chấm vị trí** (chấm theo nút gần nhất): việc này chỉ cần hộp, không cần tên. Và 86 phần tử một màn thì đầy đủ hơn hẳn bộ dò hình, nên bớt được một tầng nhiễu. ⚠️ Đổi lại thước sẽ **chặt hơn nhiều** vì có nhiều đối thủ cạnh tranh hơn — phải đo lại bộ tứ trước khi tin, đây là việc kế tiếp.
> - ❌ **Không dùng làm danh sách chữ đưa vào mô hình** (lớp 2): không có tên thì mô hình chẳng chép được gì. Đây là lý do **bằng số** để lớp 2 dùng OCR chứ không dùng cây trợ năng — không phải chọn cho tiện.
> - ❌ **Không dùng để đo độ trung thực** trên AndroidControl: đếm mô hình gọi tên nút có thật hay không thì cần tên, mà 12.6% thì không đủ. Trục này vẫn phải đo trên MobileViews.
>
> ⚠️ **Nguyên tắc phân tách vẫn giữ nguyên:** thứ dùng để **dạy** thì không được đồng thời làm thước **chấm**. Nên OCR đứng phía dạy, cây trợ năng đứng phía chấm.

### Thước 2 — Faithfulness (độ TRUNG THỰC: có bịa nút không) — trục PHỤ

**Ý tưởng bằng lời:** mỗi tên nút mô hình nhắc tới, kiểm xem nút đó **có thật trên màn** không (đối chiếu VH).

**📦 Ví dụ.** Màn Cài đặt, VH = {Settings, Notifications, Display, Sound, Battery, Search}. Mô hình sinh: *"Tap **Settings** → Tap **Preferences** → Enable **Alerts**"* → Settings có thật; Preferences bịa; Alerts bịa (đúng ra là "Notifications") → nhắc 3 nút, 2 bịa → **f = 1 − 2/3 = 0.33**.

> **Cái bẫy phải khai (đúng phát hiện của em).** Nếu mô hình nói "Tap the **+** icon" mà VH bỏ sót nhãn nút dấu cộng, đối chiếu ngây thơ sẽ **kết oan** nó là bịa. Nên em **loại nút hình không nhãn khỏi mẫu số** + báo kèm tỉ lệ nút phải bỏ ra. Thành thật, không khoe 100%.
>
> **Hộp kỹ thuật.** f = 1 − (số nút nhắc không khớp VH)/(số nút nhắc) [tinh thần ALOHa, NAACL 2024]. Đo trên MobileViews. **Em xin nói rõ đây là trục PHỤ, lực yếu:** với 12 app, nó chỉ thấy được khác biệt ≥ ~32 điểm — nên nếu kết quả "rỗng" thì *không kết luận được gì*, chỉ để mô tả, không dùng làm bằng chứng chính.
>
> **Đặt lại câu hỏi cho trục này cho có ích hơn:** K2 đã cho thấy mô hình sẵn bịa gần bằng 0, nên hỏi "bịa bao nhiêu" thì gần như chắc chắn ra ~0 (null tầm thường). Câu hỏi đáng giá hơn là **"thành phần thêm có LÀM TĂNG bịa không?"** — dùng faithfulness như một **phép canh chừng** trên chính câu mô hình sinh ra: nếu thành phần mới thêm vào (nhất là nhánh tự cải thiện) vô tình làm mô hình bịa nhiều hơn thì trục này bắt được. Đó mới là vai thực sự của nó.

### Cách tính điểm — chi tiết từ đầu đến cuối

**(a) Đơn vị chấm = TỪNG BƯỚC.** Mỗi tác vụ (episode) trong AndroidControl là một chuỗi bước; mỗi bước có **ảnh riêng + thao tác đúng + toạ độ đúng**. Mô hình chấm ở chế độ *teacher-forced*: tại bước j, nhận **(ảnh bước j) + (mục tiêu) + (các bước đã làm trước, lấy từ GOLD)** → sinh **một** câu cho bước đó. *(Em khai rõ "các bước trước" là GOLD, không phải output tự sinh của mô hình — nên con số per-step được "đỡ" bởi ngữ cảnh chuẩn. Em sẽ báo thêm một lần chạy nữa, trong đó mô hình phải dùng **chính câu nó sinh ở bước trước** (thay vì câu gold) — làm mức sàn; chênh lệch giữa hai lần cho biết cách chấm teacher-forced đang thổi phồng năng lực thật bao nhiêu.)*

> **Hoà giải "hướng dẫn nhiều bước cho người" (Phần 0) với "chấm từng bước" ở đây — em xin nói rõ để thầy khỏi thấy mâu thuẫn.** *Tầm nhìn sản phẩm* là mô hình sinh **cả một hướng dẫn nhiều bước** cho người đọc (như ví dụ Filter → Tools → Hand Tools ở đầu). Nhưng *cách ĐO ĐỊNH LƯỢNG chính* lại chấm **từng bước teacher-forced** — tại mỗi bước đưa đúng ảnh màn của bước đó rồi so một câu. Lý do: mỗi bước có màn riêng; nếu bắt sinh cả 5 bước chỉ từ ảnh màn đầu thì bước 3-4-5 nói về màn **chưa hiện ra** → không có ảnh + toạ độ để chấm công bằng. Vậy: **con số headline (per-step) là thước chặt, có toạ độ bảo chứng**; còn năng lực *sinh cả chuỗi* (đúng tầm nhìn) đo bằng coverage + F1 + order ở chế độ sinh tự do (mục (c)) và bằng khảo sát nhỏ với người thật. Đây là lựa chọn thiết kế có chủ đích, không phải giấu.

**(b) Một bước tính ĐÚNG khi thoả CẢ BA:** (1) *thao tác khớp* — động từ (chạm/gõ/cuộn/mở) khớp loại gold; (2) *không đảo nghĩa* — câu và gold không được ngược trạng-thái-đích (on/off, show/hide, up/down...): "Turn **off**" mà gold là "Turn **on**" → **rớt dù toạ độ trúng** (vì công tắc cùng một chỗ — executability mù với đảo nghĩa nếu chỉ xét toạ độ; luật này vá đúng lỗ đó, `harness/metric_exec.py`); (3) *đúng chỗ* — với bước *chạm*, điểm bộ trỏ trúng theo **nút-gần-nhất** (Voronoi, xem trên); với *gõ* → khớp nội dung; *cuộn* → khớp hướng.

> **Em báo RIÊNG hai con số, không gộp** (report/96 nhắc): **%exec-chạm** (qua bộ trỏ, **59.1%** số bước) và **%khớp-gõ/cuộn** (so nội dung/hướng, **28.9%**; còn 12.0% là quay lại/chờ, không chấm bằng cả hai cách) — đếm trên toàn bộ 4.066 bước của 752 episode có sẵn trong cache, `harness/ac_step_profile.py` — vì chỉ nhóm *chạm* mới được bộ trỏ bảo chứng, gộp thành một "% executable" sẽ che mất chỗ nào thật sự được kiểm bằng toạ độ.

**(c) Gộp điểm — ba thành phần của trục ĐÚNG (đây là chỗ giải nghĩa "coverage + F1 + thứ tự" ở bảng đầu Phần 4):**

- **Coverage (phủ bước)** = tỉ lệ bước gold được một câu sinh **khớp** (thao tác đúng ∧ đúng chỗ). Đây là **con số headline** — ở chế độ teacher-forced per-step nó chính là "% bước thực thi được". *Điểm episode = bước khớp / tổng bước gold; điểm cuối = trung bình theo app* (mỗi app một điểm rồi trung bình — để app nhiều bước không lấn át).
- **F1** = ghép coverage (recall) với **precision** để **phạt bước THỪA/bịa**. Chỉ có tác dụng ở chế độ *sinh cả chuỗi*; per-step thì F1 = coverage. ⚠️ **Nói rõ (debate report/99 M3):** ở chế độ sinh-cả-chuỗi, các bước 2,3,4... nói về màn *chưa hiện ra* nên **bộ trỏ không có ảnh để chấm** → coverage/F1/order ở chế độ đó **chưa có cơ chế tính khách quan** (so-văn-bản đã chết). Vậy **con số headline chỉ là per-step** ("sinh bước-kế-tiếp"); năng lực *sinh cả hướng dẫn từ một ảnh* (§0) chỉ trình dưới dạng **demo định tính**, KHÔNG phải số được chấm. Em hạ pitch cho khớp cái đo được.
- **Order-τ (thứ tự riêng phần)** = chỉ phạt **cặp bước BẮT BUỘC** phải đúng thứ tự (suy từ gold theo nhân quả: màn B chỉ hiện ra *sau* khi làm action ở A). Cặp **tự do** (điền email rồi điền tên, đảo vẫn được) **không** phạt.

> **Hộp kỹ thuật.** Order-τ = (C−D)/|M| trên tập cặp-bắt buộc M [**Fagin et al., "Comparing partial rankings", SIAM J. Discrete Math 2006** + Lapata CL 2006 — KHÔNG phải Kendall τ-b]. Coverage đúng = recall của target khớp **CÓ ĐIỀU KIỆN action đúng** (đúng tinh thần step-accuracy AndroidControl). Ba số báo riêng, headline = coverage đúng.

**📦 Ví dụ — so BA mô hình trên cùng một episode "chia sẻ bài báo qua Gmail":**

| Bước | Mô hình mình | SFT-trơn | gpt-4o-mini |
|---|---|---|---|
| 1 (Share) | "Tap the Share icon" ✓ | "Tap share" ✓ | "Tap the share button at top" ✓ |
| 2 (Gmail) | "Select Gmail" ✓ | "Tap the app" ✗ *(mơ hồ → trỏ nhầm)* | "Tap the Gmail icon" ✓ |
| 3 (gõ mail) | "Type the recipient's email" ✓ | "Tap next" ✗ | "Enter email address" ✓ |
| **Điểm** | **3/3 = 1.00** | **1/3 = 0.33** | **2/3 = 0.67** |

→ Gộp trên hàng trăm episode ra ba con số headline. SFT-trơn thua vì hay viết câu **mơ hồ** ("tap the app", "tap next") mà bộ trỏ không lần ra.

### Lực thống kê — cỡ mẫu + phép kiểm (cả hai trục)

Em pre-register phép kiểm và cỡ hiệu ứng nhỏ nhất đo được (MDE) **trước khi nhìn kết quả**, để không "chọn ngưỡng sau khi thấy số".

| | Trục ĐÚNG (chính) | Trục TRUNG THỰC (phụ) |
|---|---|---|
| Bộ | AndroidControl app-unseen | MobileViews |
| Đơn vị thống kê | per-app (cluster theo app) | per-app |
| Cỡ mẫu | 631 episode; **G = 78 app**, G hiệu dụng (Kish) **34.8** | **G = 12 app** |
| Phép kiểm | **wild-cluster bootstrap-t** Rademacher B=9999 [Cameron-Gelbach-Miller, REStat 2008] | **exact sign-flip** 2¹²=4096 tổ hợp [Canay-Santos-Shaikh 2021] |
| MDE | **chưa khoá được** — xem hộp dưới | **≈ 32 pp** |
| Đọc | đủ lực nếu hiệu ứng thật ≥ ~13 pp | **yếu** → chỉ để mô tả, null không kết luận được |

> **G đã tính lại trên đúng quần thể (28/7, `harness/ac_app_assign.py`).** Chạy bộ gán app trên **toàn bộ 631 episode** của lát app-unseen: gán được **363 ep = 57.5%** (243 ep lấy tên app thẳng từ thao tác mở app do dataset ghi, 120 ep trích từ câu mục tiêu). Kết quả **G = 78 app**, trong đó 30 app chỉ có một episode; Pinterest 26 và Artier 19 là cụm lớn nhất; **G hiệu dụng theo Kish = 34.8**. Tên app đã chuẩn hoá hoa thường và bỏ mạo từ nên không còn tách `The Washington Post` với `Washington post`. **Phải nói rõ:** G = 78 mô tả **363 episode gán được**, không phải cả 631; 268 episode còn lại phải gán tay lúc build, và chúng không rơi ngẫu nhiên (đó là các episode không có thao tác mở app và câu mục tiêu không nêu tên app).
>
> **MDE thì chưa khoá được, và đây là chỗ bản cũ nói quá (`harness/mde_recompute.py`).** Ba vấn đề: (1) con số SD 0.362 **không phải số đo** — script pilot đặt nó bằng √2 nhân độ lệch một nhánh, tức giả định hai nhánh độc lập, trong khi thiết kế là so ghép cặp trên cùng app nên độ lệch của hiệu phải nhỏ hơn; (2) pilot chỉ có **3.5 bước mỗi app**, nên khi tách phương sai ra thì **phần nhiễu do lấy mẫu còn lớn hơn cả phương sai quan sát được** — dữ liệu không đủ để nói các app khác nhau thật hay chỉ khác do ít mẫu; (3) bảng điểm pilot còn cụm rác và app bị tách đôi, dọn xong còn 20 app và SD tụt từ 0.256 xuống 0.217. Ba kịch bản: bảo thủ nhất (giữ giả định độc lập) cho MDE **10.7 pp** theo G và **16.0 pp** theo G hiệu dụng; dùng SD quan sát với thiết kế ghép cặp cho **7.6 / 11.3 pp**; còn nếu tin phần nhiễu đã tách thì MDE gần như bằng 0 — tức là **không kết luận được**. → **Phải chạy lại pilot với ít nhất 15 bước mỗi app trước khi đăng ký trước con số MDE.** Trong lúc chưa có, mọi ngưỡng phải neo vào kịch bản bảo thủ 16 pp và ghi rõ là tạm.
>
> **Chỗ chưa khoá còn lại:** (1) **Trục trung thực G=12 quá yếu**### Làm sao tin hai thước này đúng — bơm lỗi

Em **không** dùng "so với người chấm" làm chuẩn (thầy không muốn, và giới nghiên cứu cũng khuyến cáo không lấy tương quan với người làm cổng đậu/rớt). Thay vào đó em **bơm lỗi đã biết** (sai nút, đảo nghĩa, thiếu bước…) rồi xem thước có bắt được không.

> **Hộp kỹ thuật.** Validate bằng *perturbation / error-injection* [Sai et al., EMNLP 2021]: nhét lỗi đã biết, đo độ nhạy + độ đặc hiệu. Không dùng human-correlation làm cổng [Clark, ACL-IJCNLP 2021], không tự chấm bằng nhãn-LLM [Panickssery, NeurIPS 2024]. Chính phép bơm lỗi này đã **lật thước cũ** của em (Phần 5).

**Kết quả bơm lỗi cho thước MỚI (bản 2, chạy 28/7, `harness/exec_injection_validate.py`).** Bản 1 trong cùng ngày tuyên bố đạt 9/10 ngưỡng; phản biện chỉ ra phần lớn nhánh của nó **không thể rớt**: nhánh "trỏ nhầm nút cạnh" chọn nút cạnh bằng chính hàm khử trùng của thước, nhánh "trỏ nút xa" đặt điểm trùng tâm hộp, nhánh đảo nghĩa bơm bằng đúng tập con bảng của thước, và ca đúng bơm lệch 1% cạnh trong khi bán kính gộp là 5.8%. Đó đúng là kiểu hằng đẳng thức đã giết bộ bơm lỗi đời trước, chỉ đổi vỏ. Bản 2 dựng lại: ca lỗi toạ độ chọn phần tử đích bằng **tiêu chí hình học độc lập** (hộp không chứa gold, khoảng cách nằm trong dải cho trước), điểm bơm đặt lệch khỏi tâm, ca đúng bơm ở **mức lệch thật của bộ trỏ**, và nhánh bơm bằng bảng của thước bị gỡ khỏi tử số.

| Phép thử | Kết quả | Ngưỡng | |
|---|---|---|---|
| Câu cùng nghĩa, điểm trỏ lệch bằng mức thật → không được đánh rớt | **59.2%** (n=76) | ≤10% | **rớt** |
| Cổng thao tác bác oan cặp (câu mô hình thật, câu gold) | 13.2% (n=91) | ≤15% | đạt (trước khi vá: 28.6%) |
| Luật đảo nghĩa kêu oan trên câu cùng nghĩa | 0.0% (n=76) | ≤5% | đạt |
| Bắt câu trỏ sang phần tử cách gold 30–80 px | 100% (n=2) | ≥80% | đạt, **cỡ mẫu quá nhỏ** |
| Bắt câu trỏ sang phần tử cách gold 80–150 px | 100% (n=24) | ≥90% | đạt |
| Bắt câu trỏ sang phần tử cách xa hơn 25% cạnh | 100% (n=76) | ≥95% | đạt |
| Bắt đảo nghĩa nhóm giữ riêng (next/previous…) | **0%** (n=83) | ≥50% | **rớt** |
| Bắt câu sai loại thao tác | 100% (n=70) | ≥80% | đạt |
| Bắt câu gõ sai nội dung | 93.1% (n=159) | ≥90% | đạt |
| Bắt câu cuộn sai hướng | 100% (n=293) | ≥90% | đạt |

Đạt 8/10, **và hai chỗ rớt đều quan trọng hơn tám chỗ đạt**:

- **Chỗ rớt thứ nhất là chỗ chặn đường:** ở mức sai số thật của bộ trỏ, cách chấm chặt kết oan 59% câu đúng (bảng đường cong ở trên). Không vá được bằng code — phải có bộ trỏ chính xác hơn, tức là phải qua Cổng A.
- **Chỗ rớt thứ hai đã lường trước:** luật đảo nghĩa nhận diện bằng bảng từ nên mù với cặp đặc thù giao diện. Nhóm này em **cố ý giữ riêng, không đưa vào bảng của thước** — thêm vào thì thành 100% nhưng là tự chấm chính mình. Nhẹ đi ở chỗ: các cặp đó là hai nút khác nhau nên kênh toạ độ còn cơ hội bắt, và loại thật sự nguy hiểm (công tắc dùng chung một vị trí) chỉ chiếm **1.06% số bước** (43/4.066).

Một nhánh nữa cần nói rõ: **cỡ mẫu 2 ca** cho nhóm "phần tử cách gold 30–80 px" là quá nhỏ để kết luận gì. Nó nhỏ vì trên chính lát này rất hiếm phần tử nằm sát gold tới vậy — điều đó cũng có nghĩa lỗ "nút cạnh" hẹp hơn con số mật độ 63.2% gợi ra.

**Một thay đổi thiết kế do bơm lỗi ép ra.** Cổng "thao tác phải khớp" ban đầu tách `tap` khỏi `open`, `go to`, `select`. Đo trên 91 cặp (câu teacher thật, câu gold) thì nó **bác oan 28.6%**: gold viết "Go to the Menu section" còn mô hình viết "Tap the Menu icon" — cùng một cú chạm, khác cách nói. Đây đúng là bệnh của thước so chuỗi cũ mọc lại chỗ khác, và nó lệch có hệ thống theo giọng văn: mô hình nào nói giống phương ngữ người chú giải thì được lợi. Đã gộp mọi cách nói của cùng một cú chạm vào một lớp, chỉ giữ phân biệt chạm / gõ / cuộn; kết oan còn 13.2%.

> **Một khoá quan trọng — chống "luyện đúng bài thi".** Nếu thành phần mô hình (Phần 3, nhóm tự cải thiện) dùng bộ trỏ để *dạy*, thì bộ trỏ để *chấm* **phải là bộ khác** (khác họ / khác phiên bản), và phải có **một thước thứ ba độc lập** (mô hình ngôn ngữ khác họ chấm "câu này có hữu ích cho người không") không được tụt. Thiếu khoá này, điểm executability tăng chỉ vì mô hình được luyện thẳng vào đúng cái đem ra chấm — con số đẹp nhưng vô nghĩa. Đây đúng nguyên tắc "một bộ để lọc, một bộ khác để chấm" mà luận văn theo từ đầu. *(Nếu chọn thành phần DPO-âm bản-VH như em khuyến nghị, bẫy này nhẹ hơn hẳn vì tín hiệu dạy là VH còn tín hiệu chấm là toạ độ.)*

> **Vì sao đây là chỗ trống thật sự.** GuideMe / AskEase (giới HCI, CHI 2026) chấm bằng **khảo sát với người thật**; dòng GUI-agent (Aguvis ICML 2025, OS-Genesis ACL 2025) chấm **hành-động-của chính mô hình**. Trong phạm vi **hướng dẫn GUI cho người dùng** thì chưa có thước khách quan tái lập được nào cho tính thực thi được. *(Thành thật — em KHÔNG nói "chưa ai từng làm round-trip": ý "sinh chỉ dẫn → cho một bên khác thực thi → đo thành công" đã có ở **Vision-Language Navigation speaker-follower [Fried et al., NeurIPS 2018]** và ở dịch máy back-translation, code-gen chạy qua test. Cái mới của em = mang cách làm đó sang **miền GUI tĩnh một màn** (bộ trỏ point-in-bbox thay follower điều hướng) + đích human-facing + gắn với chương kill-test đo lường. Em sẽ trích và phân định VLN trong related work.)*

---

## 5. Những chỗ em đã tự kiểm và tự sửa (minh bạch)

Em xin báo cả các chỗ hỏng đã tự tìm ra — vì nó cho thấy quy trình kiểm chứng, không phải giấu.

**Chuyện lớn nhất — thước đầu tiên của em đã CHẾT, và em tự giết nó:**

Cách đo đầu tiên là **so chuỗi** (câu mô hình có trùng chữ với đáp án không). Em tự bơm lỗi kiểm, phát hiện nó KHÔNG tách được nút hình / nút gọi bằng từ khác. Trên 51 ca thật viết tay, khả năng phân biệt "cùng nút khác chữ" với "khác nút" chỉ đạt **0.34** (cần ≥ 0.80). Lý do bản chất: đo độ-gần nghĩa đặt "inbox ↔ outbox" (khác nút) *gần hơn* "search ↔ magnifying glass" (cùng nút) → không ngưỡng nào tách được. → Em **bỏ** cách đo này, chuyển sang **executability** (nối đất bằng toạ độ, né hẳn chuyện gọi tên). Chính vì em đã một lần bị số liệu lật, nên lần này em **đo executability trước khi tin nó** (số ở Phần 4).

**Các chỗ khác đã kiểm:**

| Chỗ | Phát hiện | Xử lý |
|---|---|---|
| Bộ trỏ rẻ (gpt-4o-mini) | chỉ trúng **51%** trên câu đúng → chưa đủ tin | phải dùng bộ trỏ chuyên trên GPU và **validate trước khi dùng** (Cổng A) |
| Sàn Exec(∅) | lo "sàn cao" → đo ra chỉ **6.6%** | thước còn nhiều chỗ để phân biệt — tin tốt, đã ghi vào Phần 4 |
| Mật độ nút gây nhiễu | **63.2%** bước có nút cạnh trong dung sai (AC) | đã chấm thật theo nút gần nhất: chênh **+19.7** (cách đúng bản chất), dải 19.7–34.2 tuỳ cách xử lý |
| Cách chấm chặt | **kết oan 42–59%** câu đúng ở mức sai số thật của bộ trỏ | chưa dùng được cho tới khi có bộ trỏ chính xác hơn — thành điều kiện tiên quyết của Cổng A |
| Cổng thao tác | **bác oan 28.6%** cặp (câu mô hình thật, gold) vì tách chạm khỏi mở / đi tới | ✅ gộp thành một lớp chạm, còn **13.2%** |
| Hai lần chẩn đoán sai trong cùng ngày | "13.2 là dải thật" rồi "bộ dò trả hộp trùng" | ✅ kiểm bằng hộp thật (IoU = 0 → phần tử riêng biệt); nguyên nhân thật là gold là điểm người chạm, không phải tâm nút |
| Lực thống kê + gán nhãn app | con số cũ tính trên sai quần thể | ✅ G tính lại: **78 app** (hiệu dụng 34.8) trên 363/631 ep gán được; ⏳ MDE chưa khoá được, pilot quá thưa |

> Ý chính: em **kiểm thước trước khi tin nó**, và chấp nhận một cổng có thể rớt — chứ không tuyên bố "đã đậu" khi chưa chạy.

**Bốn lỗ thước — trạng thái sau đợt vá 28/7:**

1. ✅ **Đảo nghĩa Bật/Tắt: đã vá, và đã bỏ một lớp vá hỏng.** Luật bắt hết cặp trong bảng và **không kêu oan câu nào** trong 76 ca cùng nghĩa. Trong ngày em có thử thêm một lớp trái nghĩa lấy từ từ điển WordNet cho "tổng quát hơn", rồi **bỏ đi vì đo ra là lỗ vốn**: nó chỉ bắt thêm 3 ca nhưng đẻ mâu thuẫn giả do đa nghĩa — WordNet coi `top` trái nghĩa `side`, `set` trái nghĩa `rise` — tới mức có câu gold **tự bác chính nó**. Bảng cũng được thu hẹp về đúng công tắc dùng chung một vị trí, bỏ `up/down` (từ chỉ vị trí) và `open/close`, `add/remove` (hai nút khác nhau, kênh toạ độ bắt được). Thêm một bất biến làm kiểm tự động: một câu không bao giờ được mâu thuẫn với chính nó. **Mảng còn mù:** cặp đặc thù giao diện (`next`/`previous`) — bắt 0% trên nhóm 83 ca giữ riêng; loại thật sự nguy hiểm chỉ chiếm **1.06% số bước**.
2. ✅ **Đã đếm lại: 59.1% bước là "chạm"** (2.401/4.066 bước trên 752 episode, không phải ~53% từ pilot nhỏ); gõ/cuộn/mở app 28.9%; còn 12.0% là quay lại và chờ, không nhóm nào chấm được nên loại khỏi mẫu số. Cách chấm gõ và cuộn **giờ đã có code** (`content_match`, `direction_match` trong `metric_exec.py`) và đã qua bơm lỗi: bắt gõ sai nội dung 93.1%, cuộn sai hướng 100%. Vẫn giữ nguyên nguyên tắc **báo tách hai con số**, không gộp thành một headline.
3. ⏳ **"Bộ trỏ trúng ≈ người làm theo được" vẫn chưa kiểm — lỗ lớn nhất còn lại.** Đây đúng là kiểu sai lầm đã giết thước cũ: tin mà chưa đo. Bộ chấm đã dựng sẵn (`harness/cv_study/rate_A.html` + `rate_B.html`, 91 cặp, xáo mù, không lộ kết quả bộ trỏ cho người chấm), phân tích đã viết sẵn tính Cohen κ có trọng số kèm khoảng tin cậy. **Hai điều kiện em khoá ngay từ giờ để nó là cổng thật chứ không phải nghi thức:** (a) phải có **hai người chấm độc lập**, không chỉ tác giả, nếu không κ rỗng nghĩa; (b) ngưỡng đăng ký trước: **tương quan giữa "người nói làm theo được" và "bộ trỏ trỏ trúng" đạt r ≥ 0.5 thì thước đáng tin, 0.3–0.5 là yếu phải khai giới hạn, dưới 0.3 thì trục executability rớt** và phải rẽ đường lui. Ngưỡng này trước đây chỉ nằm trong code, giờ đưa vào hồ sơ.
4. ⏳ **Dung sai 14% quá rộng: đã siết được, nhưng bản siết chưa dùng được.** Chấm theo nút gần nhất giờ chạy thật trên dữ liệu, cho chênh **+19.7** (dải 19.7–34.2 tuỳ cách xử lý danh sách nút) và bắt 100% ca trỏ nhầm sang phần tử cách gold trên 80 pixel. **Nhưng** ở mức sai số thật của bộ trỏ rẻ, nó kết oan 42–59% câu đúng, nên chưa thể dùng làm cách chấm chính. Hai giới hạn nữa đã viết thành ca kiểm chứ không giấu: thước chỉ chặt bằng đúng độ đầy đủ của bộ dò (bộ dò bỏ sót nút icon cạnh thì câu trỏ nhầm vẫn lọt — `TEST 6` trong `metric_exec.py`), và nhóm ca "phần tử nằm sát gold" chỉ có 2 mẫu nên chưa kết luận được gì. → Điều kiện tiên quyết chuyển hết sang Cổng A: sai số trỏ trung vị phải xuống dưới 3% cạnh.

---

## 6. Hai cổng go/no-go (chạy TRƯỚC khi tiêu tiền huấn luyện)

Em đã dựng sẵn notebook (`harness/colab_gates.ipynb`). Hai cổng này **chỉ chạy mô hình, không huấn luyện** nên rẻ và nhanh:

- **Cổng A — bộ trỏ có đủ tốt VÀ có sạch không.** ⚠️ **Ngưỡng viết lại ngày 28/7 sau khi bơm lỗi cho thấy điều kiện thật sự chặn đường.** Ngưỡng cũ "trúng ~80% trên câu đúng" đặt theo cách chấm đĩa, không dùng được cho cách chấm chặt. Bản sáng nay đổi sang "dải động ≥ 25 điểm" và viện lý do "gấp đôi MDE 18.9" — nhưng gấp đôi 18.9 là 37.8 chứ không phải 25, tức lập luận tự bác con số của chính nó. Nay đặt lại theo đúng thứ đã đo được:
  1. **Sai số trỏ trung vị ≤ 3% cạnh màn.** Đây là điều kiện tiên quyết, không phải điều kiện phụ: ở mức 8% của bộ trỏ rẻ, cách chấm chặt kết oan 42–59% câu đúng, còn ở mức 3% thì chỉ 2.6%. Không đạt điều kiện này thì **cách chấm chặt bỏ hẳn**, quay về đĩa và nói rõ giới hạn nút cạnh.
  2. **Dải động (trần trừ sàn) đo trên đúng cách chấm sẽ dùng, và trên câu mô hình chứ không chỉ câu gold.** Ngưỡng tạm là **≥ 20 điểm**, neo vào kịch bản MDE bảo thủ 16 pp; con số này sẽ khoá lại sau khi pilot dày hơn cho MDE thật. Em ghi thẳng đây là mức tối thiểu chấp nhận được, không giả vờ suy ra từ một công thức.
  3. **Đo thêm độ phủ của bộ dò phần tử** trên chính lát test, vì thước chỉ chặt bằng đúng độ đầy đủ của bộ dò.
  ⚠️ **Một giới hạn kỹ thuật phải khai:** bộ trỏ rẻ đang trả toạ độ trên lưới thô (một nấc bằng 108 pixel ngang), lớn hơn cả khoảng cách giữa hai nút cạnh nhau. Nên mọi con số chấm-theo-nút-gần-nhất hiện nay đứng trên một dụng cụ không đủ độ phân giải cho đúng việc nó cần làm. Chuyện này tự hết khi thay bằng bộ trỏ chuyên trả toạ độ liên tục — thêm một lý do không chốt ngưỡng nào trước Cổng A. ⚠️ **Chọn bộ trỏ SẠCH:** **OS-Atlas train THẲNG trên AndroidControl** → nhiễm, không dùng để "đối chiếu-loại-app" được (loại hết thì G→0). Đường sạch = **UGround** (train trên web Common Crawl, sang mobile là zero-shot). **Kèm một việc phải làm:** nguyên tắc chống ăn gian "app-unseen" chỉ bảo vệ *học trò*, **không** bảo vệ *bộ trỏ* — bộ trỏ chuyên được train trên kho ảnh GUI riêng, có thể đã từng thấy chính màn test. → Trước khi chấm phải **đối chiếu danh sách app của bộ trỏ với 631 ep app-unseen và loại mọi app trùng**. **Rớt → trục executability chưa dùng được** → rẽ đường lui (Phần 8).
- **Cổng B — còn bao nhiêu chỗ để tiến, và thành phần gắn vào có tác dụng không:** chạy bản SFT trơn trước rồi đo điểm của nó trên lát app lạ. Hai điều cần biết: (a) nếu bản trơn đã đạt điểm cao thì phần còn lại để tiến có thể hẹp hơn cả hiệu ứng nhỏ nhất đo được, khi đó kết quả sẽ không đọc được dù thành phần có tác dụng thật; (b) mô hình còn yếu ở đâu — nói mơ hồ hay gọi sai tên nút — để biết lớp nào trong hai lớp đáng đầu tư hơn. Cổng này phải chạy **trước** khi dựng bất cứ lớp nào.

> **Một điểm nhẹ gánh cho Cổng A:** thứ luận văn cần là **hiệu số Student − baseline, đo qua CÙNG một bộ trỏ**. Lỗi của bộ trỏ phần lớn **triệt tiêu trong hiệu số — NHƯNG chỉ khi hai mô hình cùng giọng** (đúng với ablation học-trò-trơn vs học-trò+thành-phần). Với so **khác giọng** (học trò vs gpt-4o-mini) thì lỗi bộ trỏ tương quan với giọng nên KHÔNG triệt tiêu (xem §4, đã đo: câu dài trúng cao hơn câu ngắn) → so đó chỉ để phụ. Ngưỡng ~70% đủ cho ablation cùng-giọng; so khác-giọng cần thêm bước chuẩn-hoá-giọng hoặc control STYLE-MATCHED.

---

## 7. Năm câu hỏi cần thầy quyết

1. **Khung đóng góp** — hai trụ (mô hình + phương pháp đánh giá): thầy chấp nhận không, và thầy coi **trụ nào là chính**?
2. **Không chấm bằng người** — em neo độ đúng vào **executability** (bộ trỏ + toạ độ đúng, khách quan) và validate bằng **bơm lỗi**, để tương quan với người ra ngoài cổng đậu/rớt. Thầy đồng ý cách thay thế này chứ? *(Em vẫn giữ một khảo sát nhỏ 91 cặp với người thật để kiểm chính thước, không dùng nó chấm mô hình.)*
3. **Baseline + kịch bản HOÀ** — baseline = gpt-4o-mini + Qwen-3B SFT-trơn. Nếu mô hình của em chỉ **hoà** (không vượt rõ), thầy có chấp nhận *"3B chạy offline ngang mô hình API lớn"* là đủ để bảo vệ không?
4. **Định vị sau GuideMe** — GuideMe (CHI 2026) đã làm tác vụ này ở mức **hệ thống** (prompt mô hình lớn + khảo sát với người thật, không huấn luyện, không benchmark). Em định vị đóng góp = *"mô hình nhỏ mở **được huấn luyện** + **tổ hợp** thước comprehension-based (kiểu referring-expression) áp cho hướng-dẫn-đa-bước-cho-người, validate bơm-lỗi."* Em **bỏ chữ "đầu tiên"** vì có tiền lệ đánh-giá sát: **REG comprehension-based eval** (Mao CVPR 2016) cũng "sinh câu → mô hình khác trỏ vùng → đo hit" — em phải phân định (khác: đa-bước + cho-người + trên GUI). Thầy thấy tổ hợp này đủ mới không?
5. **Ngưỡng đủ luận văn** — với khung này, thầy thấy đã đủ tầm một luận văn thạc sĩ chưa, hay cần thêm/bớt chỗ nào?

---

## 8. Rủi ro + đường lui (không nhánh nào là ngõ cụt)

| Rủi ro | Đường lui |
|---|---|
| Bộ trỏ không đạt ngưỡng cổng | chấm nhóm **nút có chữ** (thước chạy tốt ở đó) + khai giới hạn; "không thước tự động nào trỏ nổi nút hình" tự nó thành một phát hiện đo lường |
| Mô hình chỉ *hoà* baseline | "3B offline ngang mô hình API lớn" vẫn bảo vệ được |
| Lớp 1 không tác dụng (mô hình đoán sai vị trí rồi viết theo vị trí sai) | đo luôn tỉ lệ điểm mô hình tự đoán có trúng không; nếu nó thấp thì biết ngay nguyên nhân, và vẫn còn lớp 2 độc lập với nó |
| Lớp 2 tăng điểm vì lý do sai (câu dài ra chứ không phải đúng hơn) | đã có sẵn nhánh giả dược (đưa danh sách của màn khác) + phân tầng theo độ dài câu; nếu đúng vậy thì tự bác |
| Cả hai lớp đều không tác dụng | Cổng B chạy trước cho biết còn bao nhiêu chỗ để tiến; nếu hẹp quá thì đổi sang báo cáo mô tả và dồn trọng lượng sang chương đo lường |
| "Lợi thế sân nhà" bị vặn (học trò thuộc cách chia bước của benchmark) | dẫn kết luận chính bằng **học trò trơn vs học trò có thành phần** (cùng gốc, sạch); "hơn gpt-4o-mini" chỉ để phụ |
| Tính mới bị vặn (REG comprehension-eval đã có) | không claim "đầu tiên"; trục mới = **tổ hợp** REG-style-eval + step-accuracy áp cho hướng-dẫn-đa-bước-cho-người + chương phát-hiện-đo-lường; phân định REG (Mao 2016) |
| Quá tải (hai bài báo + nhiều nhánh mô hình trong 6 tuần) | bỏ lớp tự sinh tự lọc (vốn đã là tuỳ chọn), giữ hai lớp chính; VCL làm sàn chắc, quyết bỏ hay giữ FAIR sớm |

---

## 9. Việc theo thứ tự + lịch

Thứ tự dưới đây xếp theo nguyên tắc: **việc nào có thể giết cả hướng thì làm trước, và việc miễn phí làm trước việc tốn tiền.**

**Nhóm A — miễn phí, làm ngay, làm xong mới được tiêu tiền**

1. **Tải và kiểm cây trợ năng.** Đã tải và đã đo độ phủ nhãn (12.6%). Còn phải đối chiếu vài chục màn xem hộp có khớp ảnh không, rồi **đo lại bộ tứ trần / sàn / chênh với danh sách nút thật** thay cho bộ dò hình. Đây là số sẽ đem trình, nên phải có trước.
2. **Khảo sát 91 cặp với người.** Kiểm giả định lớn nhất còn lại: bộ trỏ trỏ trúng thì người có làm theo được không. Cần **hai người chấm độc lập**, ngưỡng đã khoá sẵn trong Phần 5.
3. **Dựng dữ liệu dạy.** Ghép câu người viết với ảnh cho phần train, chạy OCR sẵn trên toàn bộ ảnh để dùng cho lớp 2.

**Nhóm B — tốn tiền, nhưng mỗi bước đều là một cổng**

4. **Huấn luyện bản SFT trơn trước tiên, rồi đo nó.** Đây vừa là mốc so sánh, vừa là **Cổng B**: nếu bản trơn đã đạt điểm cao thì phần còn lại để tiến có thể hẹp hơn cả hiệu ứng nhỏ nhất đo được, khi đó dù thành phần có tác dụng thật cũng không đọc được kết quả. Và nó cho biết mô hình yếu ở đâu để biết lớp nào đáng đầu tư.
5. **Cổng bộ trỏ (Cổng A), khoảng 10 đô.** Điều kiện tiên quyết: sai số trỏ trung vị phải xuống dưới 3% cạnh màn. Không đạt thì bỏ cách chấm chặt, quay về cách chấm rộng và nói rõ giới hạn kèm theo.
6. **Gặp thầy** — chốt khung đóng góp, cách chấm, kịch bản hoà, định vị sau GuideMe.
7. **Huấn luyện lớp 1, rồi lớp 2** (mỗi lớp một lượt), kèm hai nhánh đối chứng của lớp 2.
8. **Đo hai thước + phân tầng theo độ dài câu + chấm tay vài chục câu.**
9. **Trục trung thực trên MobileViews, rồi viết.**

**Việc để dành, chỉ làm nếu còn thời gian và tiền:** lớp tự sinh rồi tự lọc, và chỉ khi bộ trỏ qua được cổng riêng của nó.

- **Chi phí:** hai cổng khoảng 10 đô; huấn luyện QLoRA 3B ước 60 đến 70 đô cho cả pha. Lớp 1 gần như không tốn thêm, lớp 2 tốn thêm một lượt huấn luyện.
- **Hai bài báo:** FAIR (tiếng Anh, bài mô hình) + VCL (tiếng Việt). *(Ràng buộc: cố giữ cả hai; nếu quá tải thì VCL là sàn chắc, FAIR là phần cố thêm.)*

---

## 10. Một câu tóm

> Luận văn = **(1)** một mô hình 3B mở, nhìn app lạ mà sinh được hướng dẫn thực thi được, luyện trên câu người viết, **hơn bản huấn luyện thường nhờ hai thứ nó tận dụng mà bản thường bỏ phí**: toạ độ có sẵn trong dữ liệu (bắt mô hình cam kết vị trí trước khi viết) và danh sách chữ đọc được từ ảnh (một bộ đọc chữ nhẹ đứng trước); **(2)** một khung đánh giá **executability + faithfulness** khách quan, không cần người, validate bằng bơm lỗi — chỗ mà HCI (chấm bằng người) lẫn dòng agent (chấm action của chính nó) đều bỏ trống cho *hướng dẫn cho người dùng*. Bằng chứng cứng nhất tới giờ: thước **phân biệt được câu tốt với câu dở** ở mọi cách chấm đã thử — chênh **+19.7 đến +44.7 điểm** tuỳ độ chặt, sàn luôn rất thấp. Thước cũng **đã qua bơm lỗi, đạt 8/10 ngưỡng khoá trước**, và hai chỗ rớt được báo nguyên trạng: cách chấm chặt còn kết oan nhiều khi bộ trỏ lệch, và luật đảo nghĩa mù với một nhóm cặp từ. Còn chuyện thước đo có đúng cái người cần không thì vẫn chưa kiểm, đang chờ khảo sát 91 cặp với người thật. Mô hình là một trụ, thước là trụ kia và là chỗ được đầu tư nhiều nhất.

---

### Phụ lục — trích dẫn đã dùng (venue đã đối chiếu)

AndroidControl (Li et al., **NeurIPS 2024 D&B**) · MobileViews (preprint arXiv 2409.14337, MIT) · AITW ngưỡng 14% (**NeurIPS 2023**) · SeeClick (**ACL 2024**) / OS-Atlas (**ICLR 2025**) — grounding · ALOHa (**NAACL 2024**) — faithfulness · Chen et al. VH thiếu nhãn (**ICSE 2020**, Distinguished Paper) · Sai et al. perturbation (**EMNLP 2021**) · Panickssery (**NeurIPS 2024**) & Clark (**ACL-IJCNLP 2021**) — chống tự chấm / bỏ human-correlation làm cổng · GuideMe & AskEase (**CHI 2026**) · Aguvis (**ICML 2025**) / OS-Genesis (**ACL 2025**) — phân định · **REG comprehension-based eval, Mao et al. (CVPR 2016)** — tiền lệ SÁT NHẤT: sinh referring expression → mô hình comprehension trỏ vùng → đo hit; phải phân định (ta: đa-bước + cho-người + GUI) · **VLN speaker-follower, Fried et al. (NeurIPS 2018)** — sinh chỉ dẫn → bên khác thực thi → đo thành công, phân định · UI-R1 (**AAAI 2026**) / SE-GUI (**NeurIPS 2025**) — RFT-point-in-bbox cho action · **Thống kê:** Fagin et al. partial-ranking (**SIAM J. Discrete Math 2006**) + Lapata (**CL 2006**) — order-τ · Cameron-Gelbach-Miller (**REStat 2008**) — wild-cluster bootstrap · Canay-Santos-Shaikh (**2021**) — exact sign-flip.

**Bổ sung sau vòng tra 29/7 (phải phân định trong related work):** **GCoT** (preprint arXiv 2503.12799) — so thẳng thứ tự định-vị-trước với trả-lời-trước · **Shikra** (preprint 2306.15195) · **CogCoM** (**ICLR 2025**) · **Visual CoT** (**NeurIPS 2024 D&B**) — cùng dòng sinh toạ độ làm bằng chứng trước khi kết luận · **Aguvis** (**ICML 2025**) và **UI-R1** — trong miền giao diện đặt chữ trước toạ độ sau, tức ngược vai với thiết kế này · **Mind2Web** (**NeurIPS 2023 D&B**) — huấn luyện trên danh sách ứng viên nhiễu · **Widget Captioning** (**EMNLP 2020**) và **Screen2Words** (**UIST 2021**) — huấn luyện với cây phần tử ở đầu vào · **RAFT** (**COLM 2024**), **RetRobust** (**ICLR 2024**), **RAAT** (**ACL 2024**) — huấn luyện để chịu ngữ cảnh phụ trợ nhiễu · **UGIF** (arXiv 2211.07615) — tiêu thụ chỉ dẫn cho người, ngược chiều · **OmniParser**, **Set-of-Mark** — đưa danh sách phần tử vào nhưng chỉ ở khâu suy luận.

*(Hai việc còn hở: lấy full-text GuideMe — ACM đang chặn — để xác nhận "không huấn luyện" trước khi khoá framing; và mở PDF Aguvis để xác nhận đúng thứ tự trong khuôn mẫu huấn luyện của họ trước khi trích.)*

⚠️ **Một điều vòng tra đính chính:** không được nói "GuideMe không đụng tới toạ độ" — mô tả công khai cho thấy hệ đó **có định vị phần tử** để tô sáng ngay trong app. Chỗ chưa biết chỉ là nó có huấn luyện mô hình hay không.

### Phụ lục — số liệu tái lập được

| Số | Giá trị | Code / file |
|---|---|---|
| Sàn Exec(∅) @14% | 6.6% (n=76) | `harness/ground_floor.py` · `ground_floor_results.json` |
| Trần Exec(gold) @14% | 51.3% (n=76) | `harness/ground_pilot.py` · `ground_pilot_results.json` |
| Độ chênh, cách chấm đĩa | +44.7 điểm | |
| **Bộ tứ dưới các cách chấm chặt** | chênh **+19.7** (hộp, loại hộp chứa gold) · +32.9 đến +34.2 (gộp tâm) · +32.9 (tâm OCR) · +13.2 (không xử lý gì, có lỗi) | `harness/voronoi_sensitivity.py` · `voronoi_sensitivity_results.json` |
| Bơm lỗi thước exec, bản 2 | đạt 8/10 ngưỡng khoá trước | `harness/exec_injection_validate.py` · `exec_injection_results.json` |
| Kết oan của cách chấm chặt theo sai số bộ trỏ | 0% @1% cạnh · 2.6% @3% · 25% @5% · **42.1% @8% (mức thật)** · 60.5% @13% | như trên |
| Cổng thao tác bác oan cặp thật | 28.6% trước khi gộp lớp → **13.2%** sau | như trên (nhánh `fp_action_gate`) |
| Kiểm chẩn đoán "hộp trùng" | 286 cặp hộp sát nhau, IoU trung vị 0.000, lồng nhau 2 ca → là phần tử riêng biệt | `harness/omni_boxes.py` + `dg1_cache/omni_box/` |
| Bước là công tắc dùng chung vị trí | 1.06% (43/4.066) | `harness/ac_step_profile.py` |
| G trên lát app-unseen | 78 app (hiệu dụng 34.8) trên 363/631 ep gán được | `harness/ac_app_assign.py` · `ac_app_assign_results.json` |
| MDE | chưa khoá được; kịch bản bảo thủ 10.7 pp (G) / 16.0 pp (G hiệu dụng); pilot 3.5 bước/app nên nhiễu lớn hơn tín hiệu | `harness/mde_recompute.py` · `mde_recompute_results.json` |
| Thước cũ (so chuỗi) tách nút | AUC 0.34 (rớt, cần ≥0.80) | `harness/metric_v1_validate.py` (bản vá report/84) |
