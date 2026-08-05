# Hồ sơ trình thầy — thiết kế luận văn (cập nhật 21/7/2026)

> Tài liệu để trao đổi với thầy hướng dẫn.
> **Cách đọc:** mỗi phần viết *lời thường trước*, rồi **hộp kỹ thuật** (công thức + trích dẫn) cho phần cần chiều sâu. Thuật ngữ được giải thích ngay lần đầu xuất hiện. Cuối tài liệu là **năm câu hỏi** em cần thầy định hướng.

---

## 0. Toàn cảnh chỉ bằng một ví dụ

Hình dung một người dùng mở app mua sắm, chụp lại **màn hình đang hiện**, rồi hỏi: *"Làm sao tìm cây cờ-lê trong mục Dụng cụ?"*

Mô hình của luận văn nhận **đúng một ảnh đó + câu hỏi**, và trả về **hướng dẫn từng bước cho người tự làm**:

> 1. Chạm nút **Filter** ở góc dưới
> 2. Chọn **Tools & Hardware**
> 3. Chọn **Hand Tools**

Khác biệt với mọi mô hình giao diện hiện có: chúng sinh **thao tác cho máy tự bấm** (toạ độ, mã lệnh). Ở đây ta sinh **câu chữ cho con người đọc và tự làm theo**.

**Cái khó không nằm ở việc sinh câu — mà ở việc CHẤM.** Làm sao biết ba câu trên là *đúng* và *đáng tin*, khi:
- không có sẵn "hướng dẫn chuẩn" do người soạn để đối chiếu, và
- thầy không muốn thuê người ngồi chấm?

Đây chính là chỗ luận văn có chất nghiên cứu, và là lý do có **hai đóng góp**: (1) **mô hình** sinh hướng dẫn, và (2) **phương pháp chấm** không cần đáp án mẫu, không cần người.

---

## 1. Đề tài và điều đã thay đổi so với lần trước

**Đề tài (không đổi):** mô hình nhận ảnh màn hình + câu hỏi → sinh hướng dẫn nhiều bước cho người.

Lần trước thầy bác vì hướng cũ *chủ yếu gọi API + so chuỗi, chưa có mô hình tự huấn luyện*. Em đã chuyển hẳn sang **huấn luyện một mô hình thật**. Trong lúc chuẩn bị, em chạy vài phép thử miễn phí và chúng **lật một giả định**, nên em xin báo cáo thẳng để thầy nắm:

- **Giả định cũ:** *"mô hình lớn hay bịa tên nút → ta lọc bỏ chỗ bịa → dạy mô hình nhỏ trung thực hơn."*
- **Bị bác bằng số:** em đọc tay 80 màn do gpt-4o-mini sinh → nó **gần như không bịa (~0-2%)**. Những chỗ tưởng "bịa" thật ra là **nút có thật nhưng danh sách nút của hệ điều hành bỏ sót nhãn** (nút hình như dấu cộng, dấu tích).
- **Hệ quả:** vì mô hình gần như không bịa, "lọc bịa" không còn là đóng góp. Em **bỏ khung đó**, và chuyển trục chính sang đo **độ ĐÚNG** — hướng dẫn có dẫn tới đúng nút cần bấm không.

> **Thuật ngữ.** *View Hierarchy (VH)* = danh sách các nút thật trên màn, do Android xuất ra kèm mỗi ảnh (tên nút, vị trí). Nó là "đáp án phụ" để biết nút nào có thật — nhưng không đầy đủ.
>
> **Hộp kỹ thuật.** VH thiếu nhãn nghiêm trọng: >77% ứng dụng thiếu nhãn phần tử [Chen et al., *Distinguished Paper*, ICSE 2020]; đo trên mẫu của em, độ phủ nhãn ≈ 62%, ~20% nút là hình thuần không nhãn. Vì vậy "chỉ đối chiếu VH" không đủ để đo độ đúng → cần thêm một tín hiệu khác (toạ độ, xem Phần 4).

---

## 2. Hệ thống chạy thế nào — từ đầu đến cuối

Để thầy thấy rõ chỗ nào là "học", chỗ nào là "chấm":

**Lúc DẠY (train):** đưa mô hình từng cặp *(ảnh một bước + mục tiêu)* → *(câu hướng dẫn do người viết cho bước đó)*, để nó bắt chước cách người viết. Nguồn "người viết" lấy từ bộ **AndroidControl** (giải thích ở Phần 3).

**Lúc CHẤM (test):** đưa mô hình **một ảnh app nó CHƯA TỪNG THẤY** + mục tiêu, **không** đưa danh sách nút, **không** đưa đáp án. Nó phải tự nhìn màn hình lạ mà sinh hướng dẫn.

> **Luật vàng (chống ăn gian):** danh sách nút (VH) và đáp án chỉ dùng để **dạy** và **chấm điểm** — **không bao giờ** đưa cho mô hình lúc nó sinh. App test tách riêng khỏi app train ("held-out theo app": app dùng để kiểm không xuất hiện lúc dạy). Nhờ vậy, nếu mô hình làm đúng trên app lạ nghĩa là nó **thật sự học được kỹ năng**, không phải học thuộc.

Đây cũng là câu trả lời cho "ứng dụng thực tế": khi triển khai, mô hình chỉ cần **ảnh màn hình** — thứ luôn có sẵn.

---

## 3. Đóng góp 1 — MÔ HÌNH

Huấn luyện **Qwen2.5-VL-3B** (một mô hình ảnh-ngôn-ngữ mở, 3 tỉ tham số, chạy được offline) bằng **SFT-LoRA**.

> **Thuật ngữ.** *SFT* = học có giám sát: cho mô hình xem cặp đầu-vào/đáp-án để bắt chước. *LoRA / QLoRA* = kỹ thuật fine-tune nhẹ, chỉ chỉnh một ít tham số thêm vào (chạy được trên một GPU thuê rẻ), thay vì luyện lại cả mô hình.

Em so **ba mô hình**:

| Mô hình | Vai | Học từ đâu |
|---|---|---|
| gpt-4o-mini (không huấn luyện) | baseline NGOÀI — một mô hình lớn, mạnh, làm sẵn | không học |
| Qwen-3B SFT-trơn | baseline TRONG — bản fine-tune bình thường | gold người-viết |
| **Qwen-3B SFT + thành phần** | **đóng góp của luận văn** | gold người-viết + thành phần thêm |

Hai phép so, mỗi phép trả lời một câu hỏi của hội đồng:

- **Hơn gpt-4o-mini** → *"mô hình 3B chạy offline ngang/hơn một mô hình API lớn."* Vì sao làm được: nó được **luyện đúng miền** trên hàng nghìn hướng dẫn người-viết, còn gpt-4o-mini chỉ đoán mò (mô hình nhỏ fine-tune đúng miền thắng mô hình lớn "đoán mò" ở tác vụ hẹp là chuyện thường gặp).
- **Hơn SFT-trơn** → chứng minh **thành phần em thêm** thật sự có tác dụng, chứ không phải chỉ nhờ fine-tune nói chung. (Đây gọi là *ablation* — bật/tắt đúng một yếu tố để đo tác dụng của nó.)

> **Một cái bẫy em đã ý thức để tránh:** *không* dạy mô hình chính bằng đầu ra của gpt-4o-mini rồi lại lấy gpt-4o-mini làm baseline để vượt — "học từ ai thì cùng lắm bằng người đó" (trần bắt chước). Nên **thầy dạy = gold người-viết**, còn **gpt-4o-mini chỉ đóng vai baseline để so**.

**"Thành phần thêm" là gì?** Em **cố ý chưa chốt cứng** — sẽ chọn bằng một phép thử rẻ (Phần 6) để gắn vào **đúng chỗ mô hình còn yếu**, thay vì gắn theo cảm tính. Em đã khảo sát và sàng lọc một danh sách ứng viên (chi tiết ở ghi chú nội bộ), gom thành ba nhóm:

**Nhóm 1 (mạnh nhất) — mô hình TỰ CẢI THIỆN** bằng tín hiệu khách quan (toạ-độ đúng + danh sách nút thật, *không* dùng gpt-4o). Kỹ thuật RFT/STaR: mô hình tự sinh nhiều câu cho một màn → giữ lại chỉ câu được bộ trỏ + danh sách nút xác nhận đúng → **huấn luyện lại chính nó** trên phần đã lọc.

> **📦 Ví dụ.** Bước cần làm = chọn **Gmail** để chia sẻ. Mô hình tự sinh 8 câu; lọc bằng bộ trỏ + danh sách nút:
> | Câu tự sinh | Kiểm | Giữ? |
> |---|---|---|
> | "Tap the Gmail icon" | trỏ trúng Gmail, nút có thật | ✓ |
> | "Select Gmail to share" | trỏ trúng | ✓ |
> | "Tap the share button" | trỏ ra chỗ khác | ✗ |
> | "Tap Send" | nút không có trên màn | ✗ |
>
> Gom 2 câu ✓ → huấn luyện lại. **Vì sao hơn SFT-trơn:** gold chỉ ghi *một* câu/bước, nhưng có nhiều cách nói đúng — tự-cải-thiện bổ sung câu đúng-mà-đa-dạng mà gold thiếu. Học từ *toạ-độ-người* nên **được phép claim vượt gpt-4o**. Deploy sạch (nướng vào trọng số, lúc chạy chỉ cần ảnh).

**Nhóm 2 (rẻ, ít bẫy hơn) — dạy bằng cặp câu-đúng / câu-bịa** đúc sẵn từ danh sách nút thật (kỹ thuật DPO). Nhắm thẳng "bớt bịa nút".

> **📦 Ví dụ.** Câu ĐÚNG = "Tap **Settings**" (Settings có trên màn). Câu BỊA đúc tất định = "Tap **Preferences**" (đổi sang tên hợp lý nhưng danh sách nút cho biết màn không có). Dạy mô hình chuộng câu đúng → nó học thói quen chỉ gọi nút có thật.

**Nhóm 3 (bổ trợ) — vòng kiểm-và-sửa lúc chạy.**

> **📦 Ví dụ.** Mô hình sinh "Tap the button" (mơ hồ) → bộ trỏ lưỡng lự giữa 5 nút → hệ nhắc "nói rõ nút nào" → mô hình sửa thành "Tap the Filter button at the bottom right" → bộ trỏ trỏ trúng → giữ. Không train thêm, làm nhanh.

> **Một cạm bẫy em đã lường trước và có cách chặn** (nếu chọn nhóm tự-cải-thiện): nếu dùng bộ trỏ để *dạy* mô hình rồi lại dùng bộ trỏ để *chấm*, thì điểm lên là "dạy để thi", vô nghĩa. Cách chặn: **bộ trỏ lúc dạy phải khác bộ trỏ lúc chấm**, và thêm **một thước thứ ba độc lập** phải không tụt. (Chi tiết ở Phần 4.)
>
> **Liêm chính:** cơ chế tự-cải-thiện này (RFT/RLVR) đã có trên các mô hình GUI-agent (UI-R1, SE-GUI) nhưng cho *thao-tác-máy*, chưa ai áp cho *sinh-hướng-dẫn-người* → em kể là "áp dụng vào tác vụ mới", không nhận là phát minh máy móc mới.

---

## 4. Đóng góp 2 — PHƯƠNG PHÁP ĐÁNH GIÁ (chỗ có chất mới)

Vì thầy không muốn chấm-người, em thiết kế một **quy trình đánh giá khách quan, tự động** — **không phải chỉ hai con số**, mà là:

| Thành phần | Nội dung |
|---|---|
| **Trục ĐÚNG** | executability (test từng bước) → gộp thành **coverage** (phủ đủ bước) + **F1** (không nhồi bước thừa/bịa) + **thứ tự** |
| **Trục TRUNG THỰC** | faithfulness (bịa nút) |
| **Các khoá chống ăn gian** | lượt "không có câu" làm sàn; **thước thứ ba độc lập** (mô hình khác họ chấm "hữu ích cho người") — bắt buộc khi dùng thành phần tự-cải-thiện |
| **Cách validate chính thước** | bơm-lỗi (đã lật được thước cũ — Phần 5) |
| **Phát hiện đo-lường** | bốn phép thử K1/K2/OCR/việc-1 + "không thước so-chuỗi nào tách nổi nút icon" — bản thân đây là đóng góp |

Nói cách khác: đóng góp này là một **giao thức + các phát hiện**, không phải hai công thức. Dưới đây giải thích hai trục chính:

### Thước 1 — Executability (độ ĐÚNG: hướng dẫn có trỏ đúng chỗ không)

**Ý tưởng bằng lời:** giấu mục tiêu đi, đưa *chỉ mỗi câu hướng dẫn* cho một **bộ trỏ**, xem nó có lần ra đúng nút không. Nếu một câu đủ rõ để bộ trỏ (đóng vai người dùng) chạm trúng, thì câu đó *đúng*.

> **Thuật ngữ.** *Bộ trỏ (grounder)* = một mô hình chuyên: đưa nó **ảnh + một câu** như "chạm nút Tìm kiếm", nó chỉ ra **điểm (x, y)** trên màn nên chạm. Ta dùng nó như một "người dùng máy móc" làm theo hướng dẫn.

**📦 Ví dụ chạy tay** (màn thật — app Snapdeal, ảnh 1080×2400 pixel, bước = bấm nút **Filter**, toạ độ đúng có sẵn = **(854, 2275)**):

Ba mô hình sinh ba câu cho *cùng* bước đó:

| Mô hình | Câu sinh ra |
|---|---|
| gpt-4o-mini | "Tap the funnel-shaped filter icon at the bottom right" |
| SFT-trơn | "Tap filter" |
| Mô hình mình | "Tap the Filter button at the bottom" |

Chấm câu **"Tap filter"**:
1. Đưa bộ trỏ **ảnh + đúng câu đó** (không nói mục tiêu, không nói đáp án).
2. Bộ trỏ đoán điểm chạm → ví dụ trả về **(860, 2270)**.
3. So với đáp án **(854, 2275)**: lệch = √(6² + 5²) ≈ **7.8 pixel**. Dung sai cho phép = 14% cạnh màn ≈ **151 pixel**. 7.8 ≪ 151 → **TRÚNG**.

Ba tính chất làm thước này vững:

- **Giọng văn không ăn gian được.** "funnel icon" (teacher) và "Filter button" (mình) gọi tên *khác hẳn*, nhưng bộ trỏ hiểu cả hai đều chỉ nút Filter → cùng trỏ về ~(855, 2273) → **cùng TRÚNG**. Nên thước **không** thưởng việc nói giống chữ đáp án; nó chỉ thưởng *đủ rõ để lần ra*. → "mô hình mình hơn" nghĩa là *rõ/đúng hơn*, không phải *nói giống gold hơn*. (Đây là đòn phòng thủ quan trọng nhất, vì mô hình học trên gold nên hay nói giọng giống gold.)
- **Bắt được câu sai.** Nếu mô hình nói nhầm "Tap the search bar" → bộ trỏ lần ra ô tìm kiếm trên đỉnh (100, 200), cách đáp án rất xa → **TRẬT** (0 điểm bước đó).
- **Chống "màn quá dễ".** Có người sẽ vặn: *"màn chỉ có một nút to thì câu vớ vẩn cũng trúng."* Nên em chạy thêm một lượt **không đưa câu** (chỉ ảnh) làm **sàn**. Phần câu hướng dẫn *thật sự đóng góp* = có-câu − không-câu.

Gộp trên nhiều bước (ví dụ minh hoạ):

| | Trúng /100 bước |
|---|---|
| Mô hình mình (có câu) | 72 |
| Không có câu (sàn) | 30 |
| **→ giá trị câu đóng góp** | **72 − 30 = 42 điểm** |
| gpt-4o-mini | 61 |
| SFT-trơn | 55 |

→ Câu mình **dễ làm-theo-đúng hơn** hai baseline, bằng số khách quan, không cần ai chấm.

> **Hộp kỹ thuật.** Với câu sinh *s* trên màn có hành động đúng (x\*, y\*), bộ trỏ đông cứng *G* cho ra (x̂, ŷ) = *G*(ảnh, s). Bước *thực-thi-được* nếu khoảng cách( (x̂,ŷ), (x\*,y\*) ) ≤ τ × D, với D = kích thước màn, τ = 0.14 [ngưỡng dung sai từ AITW, NeurIPS 2023]. Đây đúng là tiêu chí *step-accuracy* của AndroidControl [Li et al., NeurIPS 2024 D&B], nhưng **áp cho câu hướng dẫn đã được nối-đất** thay vì cho toạ độ mô hình tự dự đoán. Control: chạy *G*(ảnh, ∅) làm sàn; giá trị thông tin của câu = Exec(s) − Exec(∅).

### Thước 2 — Faithfulness (độ TRUNG THỰC: có bịa nút không)

**Ý tưởng bằng lời:** mỗi tên nút mô hình nhắc tới, kiểm xem nút đó **có thật trên màn** không (đối chiếu danh sách nút thật VH).

**📦 Ví dụ chạy tay.** Màn Cài đặt, danh sách nút thật = {Settings, Notifications, Display, Sound, Battery, Search}. Mô hình sinh: *"Tap **Settings** → Tap **Preferences** → Enable **Alerts**"*.

| Nút mô hình nói | Có trong danh sách thật? |
|---|---|
| Settings | ✓ có thật |
| Preferences | ✗ **bịa** (màn chỉ có "Settings") |
| Alerts | ✗ **bịa** (đúng ra là "Notifications") |

→ nhắc 3 nút, 2 bịa → **f = 1 − 2/3 = 0.33**. Mô hình trung thực chỉ nhắc nút có thật → f = 1.0.

> **Cái bẫy phải khai (đúng phát hiện của em).** Nếu mô hình nói "Tap the **+** icon" mà danh sách nút bỏ sót nhãn của nút dấu cộng (nút hình không nhãn), thì đối chiếu ngây thơ sẽ **kết oan** nó là bịa — trong khi nút đó có thật. Nên em **loại nút hình-không-nhãn khỏi mẫu số** (chỉ chấm nút mà danh sách có nhãn tin được) + báo kèm tỉ lệ nút phải bỏ ra. Thành thật, không khoe 100%.
>
> **Hộp kỹ thuật.** f = 1 − (số nút nhắc không khớp VH) / (số nút nhắc) [tinh thần ALOHa, NAACL 2024]. Báo dạng *có-điều-kiện-recall-VH* + kèm %fallback.

### Cách tính điểm — CHI TIẾT TỪ ĐẦU ĐẾN CUỐI

**(a) Đơn vị chấm = TỪNG BƯỚC.** Mỗi tác vụ (episode) trong AndroidControl là một chuỗi bước; **mỗi bước có ảnh riêng + thao-tác đúng + toạ-độ đúng**. Mô hình chấm ở chế độ *teacher-forced*: tại bước j, nó nhận **(ảnh bước j) + (mục tiêu) + (các bước đã làm trước)** → sinh **một** câu hướng dẫn cho bước đó.

> **Vì sao chấm từng bước, không phải sinh cả hướng dẫn từ một ảnh?** Vì mỗi bước có màn hình riêng; nếu bắt mô hình sinh cả 5 bước chỉ từ ảnh màn đầu, thì bước 3-4-5 nói về những màn **chưa hiện ra** → không có ảnh để chấm công bằng. Chấm từng bước là cách đo chặt chẽ và đúng dữ liệu. (Em sẽ khai rõ điểm này — nó là một lựa chọn thiết kế, không giấu.)

**(b) Một bước tính ĐÚNG (executable) khi thoả CẢ HAI:**
1. **Thao-tác khớp:** động từ trong câu (chạm / gõ / cuộn / mở) khớp loại thao-tác gold. "Tap" mà gold là "type" → sai ngay.
2. **Đúng chỗ:** với bước *chạm*, điểm bộ trỏ nằm trong dung sai 14% của toạ-độ gold. Với *gõ* → khớp nội dung gõ; *cuộn* → khớp hướng.

**(c) Gộp điểm:**
- Điểm một episode = (số bước đúng) / (tổng số bước).
- Điểm cuối = **trung bình theo app** (mỗi app một điểm, rồi trung bình các app — để một app nhiều bước không lấn át).

---

**📦 Ví dụ 1 — chấm một episode 3 bước (mô hình của mình).** Tác vụ: *"chia sẻ bài báo qua Gmail"*.

| Bước | Màn hình | Câu mô hình sinh | Bộ trỏ trỏ đâu | Thao-tác khớp? | Kết quả |
|---|---|---|---|---|---|
| 1 | trang bài báo | "Tap the Share icon" | trúng nút Share (lệch 20px < 151) | chạm = chạm ✓ | **ĐÚNG** |
| 2 | bảng chia sẻ | "Select Gmail" | trúng biểu tượng Gmail | chạm ✓ | **ĐÚNG** |
| 3 | màn soạn thư | "Tap the Send button" | — | gold là **GÕ** địa chỉ, câu bảo **chạm** → ✗ | **SAI** |

→ Điểm episode = **2/3 = 0.67**. (Bước 3 sai vì mô hình nhảy cóc sang "gửi" trong khi bước đúng là gõ địa chỉ người nhận.)

---

**📦 Ví dụ 2 — so BA mô hình trên CÙNG episode đó** (để thấy điểm phân biệt được chất lượng):

| Bước | Mô hình mình | SFT-trơn | gpt-4o-mini |
|---|---|---|---|
| 1 (Share) | "Tap the Share icon" ✓ | "Tap share" ✓ | "Tap the share button at top" ✓ |
| 2 (Gmail) | "Select Gmail" ✓ | "Tap the app" ✗ *(mơ hồ → bộ trỏ trỏ nhầm)* | "Tap the Gmail icon" ✓ |
| 3 (gõ mail) | "Type the recipient's email" ✓ | "Tap next" ✗ | "Enter email address" ✓ |
| **Điểm** | **3/3 = 1.00** | **1/3 = 0.33** | **2/3 = 0.67** |

→ Trên cùng một tác vụ: mô hình mình 1.00, gpt-4o 0.67, SFT-trơn 0.33. Gộp trên hàng trăm episode ra ba con số headline. SFT-trơn thua vì hay viết câu **mơ hồ** ("tap the app", "tap next") mà bộ trỏ không lần ra.

---

**📦 Ví dụ 3 — control "không có câu" (chống vặn màn dễ).** Chạy lại đúng 3 màn trên nhưng **không đưa câu nào**, chỉ bảo bộ trỏ "đoán nút hợp lý nhất":
- Màn 1: có nút Share nổi bật → bộ trỏ đoán trúng → 1 điểm "free".
- Màn 2: nhiều app share ngang nhau → đoán nhầm → 0.
- Màn 3: không có câu thì không biết gõ gì → 0.

→ Sàn = **1/3 = 0.33**. Vậy *giá trị thật câu mô hình mình đóng góp* = 1.00 − 0.33 = **0.67**. Nếu một mô hình đạt 0.67 nhưng sàn cũng 0.60 thì thật ra nó chỉ hơn sàn 0.07 — con số này lộ ngay, không khoe khống được.

---

**📦 Ví dụ 4 — faithfulness, một câu TRUNG THỰC và một câu BỊA** (để đối chiếu với ví dụ f=0.33 ở trên):
- Màn có nút thật {Compose, Search, Settings, Inbox}. Mô hình A: *"Tap **Compose**, then tap **Search**"* → cả 2 nút có thật → **f = 1 − 0/2 = 1.0**.
- Mô hình B: *"Tap **New Message**, then **Find**"* → cả 2 tên đều KHÔNG có trong danh sách (đúng ra là Compose / Search) → **f = 1 − 2/2 = 0.0**. Hai câu *nghĩa gần đúng* nhưng gọi sai tên → người dùng dò không thấy nút.

---

### Vì sao cần cả hai thước

Chúng bắt hai kiểu lỗi khác nhau, dùng hai nguồn dữ liệu độc lập → **kiểm chéo được**, khó cùng sai một kiểu:

| Thước | Bắt lỗi gì | Cần dữ liệu | Chạy trên bộ |
|---|---|---|---|
| Executability | trỏ sai chỗ / mơ hồ | toạ độ đúng | AndroidControl |
| Faithfulness | bịa nút không tồn tại | danh sách nút thật (VH) | MobileViews |

### Làm sao tin hai thước này đúng

Em **không** dùng "so với người chấm" làm chuẩn (thầy không muốn, và giới nghiên cứu cũng khuyến cáo không lấy tương-quan-người làm cổng đậu/rớt). Thay vào đó em **bơm lỗi đã biết** vào rồi xem thước có bắt được không — đây là cách validate thước chuẩn mực và khách quan.

> **Hộp kỹ thuật.** Validate bằng *perturbation / error-injection* [Sai et al., EMNLP 2021]: nhét lỗi đã biết (sai nút, đảo nghĩa, thiếu bước…), đo độ nhạy + độ đặc hiệu. Không dùng human-correlation làm cổng [Clark, ACL-IJCNLP 2021], không tự-chấm bằng nhãn-LLM [Panickssery, NeurIPS 2024].

> **Một khoá quan trọng — chống "dạy để thi".** Nếu thành phần mô hình (Phần 3, nhóm tự-cải-thiện) dùng bộ trỏ để *dạy*, thì bộ trỏ để *chấm* **phải là một bộ khác** (khác họ / khác phiên bản), và phải có **một thước thứ ba độc lập** (ví dụ một mô hình ngôn ngữ khác họ chấm "câu này có hữu ích cho người không") không được tụt. Nếu thiếu khoá này, điểm executability tăng chỉ vì mô hình được luyện thẳng vào đúng cái đem ra chấm — con số đẹp nhưng vô nghĩa. Đây đúng nguyên tắc "một bộ để lọc, một bộ khác để chấm" mà luận văn theo từ đầu.

> **Vì sao đây là chỗ trống thật sự.** GuideMe / AskEase (giới HCI, CHI 2026) chấm bằng **nghiên-cứu-người**; dòng GUI-agent (Aguvis ICML 2025, OS-Genesis ACL 2025) chấm **hành-động-của-chính-mô-hình**. **Chưa ai** chấm *tính-thực-thi-được của hướng-dẫn-sinh-cho-người* bằng thước khách quan tái-lập-được. *(Thành thật: ý "thực-thi-được / round-trip" mượn từ dịch máy back-translation và code-gen chạy-qua-test; cái mới là mang nó sang sinh-hướng-dẫn-GUI.)*

---

## 5. Những chỗ em đã tự kiểm và tự sửa (minh bạch)

Em xin báo cả các chỗ hỏng đã tự tìm ra — vì nó cho thấy quy trình kiểm chứng, không phải giấu:

1. **Cách đo đầu tiên (so chuỗi) — em tự bơm-lỗi kiểm, phát hiện nó KHÔNG tách được nút hình / nút gọi bằng từ khác.** Trên 51 ca thật viết tay, khả năng phân biệt "cùng nút khác chữ" với "khác nút" chỉ đạt **0.34** (cần ≥ 0.80). Lý do bản chất: đo độ-gần-nghĩa đặt "inbox ↔ outbox" (khác nút) *gần hơn* "search ↔ magnifying glass" (cùng nút) → không ngưỡng nào tách được. → Em **bỏ** cách đo này, chuyển sang **executability** (nối-đất bằng toạ độ, né hẳn chuyện gọi tên).
2. **Thử bộ trỏ rẻ (gpt-4o-mini):** chỉ trúng **51%** trên câu đúng → chưa đủ tin → phải dùng bộ trỏ chuyên trên GPU và **validate trước khi dùng** (đó là Cổng A ở Phần 6).
3. **Số liệu lực thống kê + gán nhãn app:** em đã rà lại và đang tính lại cho đúng phần dữ liệu.

> Ý chính: em **kiểm thước trước khi tin nó**, và chấp nhận một cổng có thể rớt — chứ không tuyên bố "đã đậu" khi chưa chạy.

---

## 6. Hai cổng go/no-go (chạy TRƯỚC khi tiêu tiền huấn luyện)

Em đã dựng sẵn notebook (`harness/colab_gates.ipynb`). Hai cổng này **chỉ chạy mô hình, không huấn luyện** nên rẻ và nhanh:

- **Cổng A — bộ trỏ có đủ tốt không:** cho một bộ trỏ chuyên (OS-Atlas / UGround / Qwen bản grounding) lần vị trí từ **câu đúng**, phải trúng ~80%. **Rớt → trục executability chưa dùng được** → rẽ đường lui (Phần 7).
- **Cổng B — thành phần nên gắn đâu:** đo mô hình nền còn yếu ở đâu (bịa nút nhiều, hay trỏ kém) → quyết gắn thành phần gì cho có tác dụng.

> **Một điểm nhẹ gánh cho Cổng A:** thứ luận văn cần là **hiệu số Student − baseline, đo qua CÙNG một bộ trỏ**. Lỗi của bộ trỏ phần lớn **triệt tiêu trong hiệu số** → ngưỡng để *so sánh hai mô hình* nhẹ hơn ngưỡng để *đo tuyệt đối*. Nên kể cả bộ trỏ chỉ 70% vẫn so sánh được.

---

## 7. NĂM CÂU HỎI CẦN THẦY QUYẾT

1. **Khung đóng góp** — hai trụ (mô hình + phương pháp đánh giá) như trên: thầy chấp nhận không, và thầy coi **trụ nào là chính**?
2. **Không chấm-người** — em xác nhận lại thầy muốn tránh chấm-người → em neo độ-đúng vào **executability** (bộ trỏ + toạ độ đúng, khách quan) và validate bằng **bơm-lỗi**, để tương-quan-người ra ngoài cổng đậu/rớt. Thầy đồng ý cách thay thế này chứ?
3. **Baseline + kịch bản HOÀ** — baseline = gpt-4o-mini + Qwen-3B SFT-trơn. Nếu mô hình của em chỉ **hoà** (không vượt rõ), thầy có chấp nhận kết quả *"3B chạy offline ngang mô hình API lớn"* là đủ để bảo vệ không? (Em muốn biết trước để không bị động lúc bảo vệ.)
4. **Định vị sau GuideMe** — GuideMe (CHI 2026) đã làm tác vụ này ở mức **hệ thống** (prompt mô hình lớn + nghiên-cứu-người, không huấn luyện, không benchmark). Em định vị đóng góp = *"mô hình nhỏ mở **được huấn luyện** + bộ đánh giá định lượng tái-lập-được đầu tiên cho tác vụ này."* Thầy thấy đủ mới không?
5. **Ngưỡng đủ luận văn** — với khung này, thầy thấy đã đủ tầm một luận văn thạc sĩ của trường chưa, hay cần thêm/bớt chỗ nào?

---

## 8. Rủi ro + đường lui (không nhánh nào là ngõ cụt)

| Rủi ro | Đường lui |
|---|---|
| Bộ trỏ không đạt ~80% | chấm nhóm **nút-có-chữ** (thước chạy tốt ở đó) + khai giới hạn; "không thước tự động nào trỏ nổi nút hình" tự nó thành một phát hiện đo-lường |
| Mô hình chỉ *hoà* baseline | "3B offline ngang mô hình API lớn" vẫn bảo vệ được |
| Thành phần thêm không có tác dụng | chọn thành phần *bằng phép thử trước khi train*, gắn vào chỗ có room |
| Tính mới bị vặn | trục mới = thước executability cho hướng-dẫn-sinh, không phải "tác vụ đầu tiên" |

---

## 9. Kế hoạch + lịch

- **Ngay:** chạy 2 cổng trên Colab (Pro ~$10, chỉ chạy mô hình). Qua cổng → dựng dữ liệu → huấn luyện 3 mô hình → đo 2 thước + bơm-lỗi validate.
- **Chi phí huấn luyện:** QLoRA 3B trên Colab, ước ~$60-70 cả pha.
- **Hai bài báo:** FAIR (tiếng Anh, bài mô hình) + VCL (tiếng Việt). *(Ràng buộc của em: giữ cả hai.)*

---

### Phụ lục — trích dẫn đã dùng (venue đã đối chiếu)

AndroidControl (Li et al., **NeurIPS 2024 D&B**) · AITW ngưỡng 14% (**NeurIPS 2023**) · SeeClick (**ACL 2024**) / OS-Atlas (**ICLR 2025**) — grounding · ALOHa (**NAACL 2024**) — faithfulness · Chen et al. VH thiếu nhãn (**ICSE 2020**, Distinguished Paper) · Sai et al. perturbation (**EMNLP 2021**) · Panickssery (**NeurIPS 2024**) & Clark (**ACL-IJCNLP 2021**) — chống tự-chấm / bỏ human-correlation làm cổng · GuideMe & AskEase (**CHI 2026**) · Aguvis (**ICML 2025**) / OS-Genesis (**ACL 2025**) — phân định.

*(Việc còn hở: lấy full-text GuideMe — ACM đang chặn — để xác nhận "không huấn luyện" trước khi khoá framing.)*
