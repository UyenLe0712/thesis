# Tổng kết luận văn + đã làm gì + plan tiếp theo

> Một file gộp: (1) những thứ cần biết về đề tài, (2) toàn bộ việc đã làm gần đây — nhất là chuỗi kiểm chứng + quyết định lớn, (3) plan từ đây đi tiếp. Ngày: 2026-07-18. Khi cần đào sâu: mở đúng file gốc ghi ở cuối mỗi mục.

---

# PHẦN A — CẦN BIẾT VỀ PROJECT

## 1. Đề tài, nói gọn

Cho **một ảnh chụp màn hình app + một câu hỏi** ("làm sao để bật thông báo?"), hệ thống trả lời bằng **các bước cụ thể** bám đúng màn hình. Cái khó: **không có bộ hướng dẫn mẫu** để chấm, và mô hình hay **bịa tên nút không có thật** (nguy hiểm: người dùng bấm nhầm).

Yêu cầu cứng của thầy: luận văn phải có **một mô hình do học viên tự huấn luyện**, không chỉ ghép API.

## 2. Ý tưởng cốt lõi (thầy giáo → học trò)

- **Thầy giáo** = gpt-4o-mini (mô hình lớn, gọi qua mạng) viết bản nháp hướng dẫn.
- **Đối chiếu** tên nút với **View Hierarchy (VH)** = file hệ điều hành liệt kê nút thật trên màn → chỗ bịa thì **viết lại thành câu mô tả chung chung** (fallback).
- Dữ liệu đã lọc → **huấn luyện học trò** = **Qwen2.5-VL-3B** (nhỏ, chạy on-device, không cần internet).
- Lúc dùng thật: học trò chỉ cần ảnh + câu hỏi.

## 3. Pipeline (đã chốt xương sống)

```
teacher gpt-4o-mini sinh nháp (không thấy VH)
    → đối chiếu tên nút với VH (bộ đối chiếu)
    → khớp: giữ · bịa: viết lại thành mô tả chung chung
    → data-LỌC  ⇄  data-THÔ (đối chứng)
    → train 2 bản: Student-LỌC + Student-THÔ (Qwen2.5-VL-3B, QLoRA, freeze-vision)
```

Xương sống này **đã kiểm bằng "vẽ lại từ trang trắng"** (report/64) — đi lại từ đầu vẫn ra y hệt vì cấu trúc dữ liệu ép. *(Chi tiết: report/54 = thiết kế đầy đủ; report/56 = ngưỡng đã pre-register.)*

---

# PHẦN B — ĐÃ LÀM GÌ (chuỗi kiểm chứng + quyết định)

> Toàn bộ phần dưới đây là những phép thử **miễn phí, chạy ngay trên máy tính** (không tốn tiền API, không cần GPU). Mục đích: kiểm xem thiết kế có thật sự đứng vững không **trước khi bỏ tiền ra huấn luyện**. Đây là phần giá trị nhất gần đây, vì nó phát hiện được vài điều mà nếu không kiểm thì đã tiêu tiền nhầm hướng.

## 4. Bốn phép thử miễn phí (đặt tên K1, K2, OCR, VIỆC1)

### K1 — Kiểm "bộ đối chiếu" có đáng tin không (file report/73)

**"Bộ đối chiếu" là gì:** phần lõi của pipeline. Nó là một thuật toán so tên nút mà mô hình nói (ví dụ "Settings") với danh sách nút thật trên màn (lấy từ View Hierarchy). Nếu khớp thì giữ, không khớp thì kết luận là "bịa" và viết lại thành câu chung chung. Cả pipeline dựa vào nó, nên phải kiểm nó có làm việc đúng không.

**Kiểm HAI CHIỀU nghĩa là kiểm cả hai loại lỗi ngược nhau:**
- **Chiều bỏ lọt:** mô hình bịa một tên *nghe giống* nút thật (nói "Send" trong khi màn chỉ có nút "Save"). Vì "Send" và "Save" gần nghĩa, thuật toán tưởng đúng nên cho qua → **bịa lọt vào dữ liệu huấn luyện**. Đây là chiều nguy hiểm.
- **Chiều kết oan:** mô hình gọi *đúng* nút nhưng bằng từ khác (nói "Tìm kiếm" cho nút hiển thị chữ "Search"). Thuật toán không nhận ra hai từ là một → đánh nhầm là bịa → **vứt oan một bước đúng**.

**Kết quả:** ở ngưỡng đang dùng, thuật toán **bỏ lọt 47,5%** số ca bịa-gần-nghĩa VÀ **kết oan 47,5%** số ca gọi-đúng-bằng-từ-khác. Tệ hơn: điểm số của hai loại này **trùng lên nhau hoàn toàn**, nghĩa là dù có chỉnh ngưỡng cách nào cũng không tách được "bịa nghe giống" khỏi "gọi đúng bằng từ khác". Thử đổi sang thuật toán so nghĩa mạnh hơn (kể cả của OpenAI) cũng chỉ đỡ một chút, không giải quyết — vì đây là hạn chế bản chất của việc "đo độ gần nghĩa".

### K2 — Đếm xem mô hình-thầy bịa THẬT nhiều hay ít (file report/74)

Lấy 80 màn hình mà thầy giáo (gpt-4o-mini) đã viết hướng dẫn từ trước (có sẵn, không tốn tiền), rồi **đọc tay từng bước** xem chỗ nào là bịa thật.

**Kết quả gây bất ngờ:** trong các bước bị đánh "bịa", **không có ca nào là bịa-nghe-giống thật cả**; **35/40** ca thực ra là **nút CÓ THẬT nhưng bị VH bỏ sót nhãn** — phần lớn là nút hình (icon dấu `+` để thêm, dấu `✓` để xác nhận, mũi tên) mà file VH không ghi chữ. Nghĩa là **thầy giáo gpt-4o-mini gần như không bịa (~0-2%)**, chứ không phải "khoảng ¼" như con số cũ vẫn nói. Con số "¼" cũ nhiều khả năng chính là những nút thật bị đánh oan này, bị đọc nhầm thành bịa.

### OCR — Thử dùng OCR bù chỗ VH thiếu nhãn (file report/75)

Vì K2 cho thấy vấn đề là VH bỏ sót nhãn nút, thử dùng **OCR** (đọc chữ trực tiếp trên ảnh) để bù. Kết quả: OCR **giúp được với nút có chữ** (đưa độ phủ nhãn từ 74% lên 80% trên nút cỡ-nút), nhưng **không giúp được nút hình thuần** (dấu `+`, `✓` không có chữ để đọc). Sau cùng vẫn còn khoảng **20% nút không cách nào lấy được nhãn** — đó là trần không xoá hết được bằng OCR.

### VIỆC1 — Đọc tay câu "chung chung" xem có dùng được không (file report/76)

"Câu chung chung" (fallback) là câu mà pipeline viết vào thay chỗ bị coi là bịa — kiểu *"Hãy tìm tuỳ chọn phù hợp trên màn hình cho bước này."* Cả thiết kế giả định câu này vẫn có ích cho người dùng. VIỆC1 sinh ra 127 câu như vậy từ dữ liệu thật và **đọc tay đánh giá**.

**Kết quả:** câu **an toàn** (không bịa tên nút mới) nhưng **giá trị thấp** — khoảng 80% chỉ *lặp lại đúng câu hỏi* của người dùng mà không chỉ **bấm ở đâu / hình gì**, nên với người đang bí thì gần như vô dụng; khoảng 20% còn bị lặp động từ đọc sượng ("Chạm vào tuỳ chọn cho phép bạn *chạm vào*..."). Và vì K2 đã cho thấy các bước bị đánh "bịa" thật ra là nút thật, nên câu chung chung này **thường thay một nút cụ thể-đúng bằng một câu mơ hồ** — tức làm hướng dẫn tệ đi.

### Bốn phép thử này kể chung MỘT câu chuyện

Bộ đối chiếu yếu (K1), nhưng lỗi **thực tế** xảy ra không phải "bỏ lọt bịa" mà là "**đánh oan nút thật**" (K2), do VH thiếu nhãn. OCR vá được một nửa (nút có chữ), còn câu chung chung thì thay nút-thật bằng câu mơ hồ (VIỆC1). Hai kết luận quan trọng rút ra:

1. **Bộ lọc hiện tại có nguy cơ LÀM HẠI dữ liệu** (biến nút thật thành câu mơ hồ), không phải làm sạch. Cách sửa: nâng bộ đối chiếu thành **nhiều tầng** — thử so chuỗi ký tự trước, rồi tra VH, rồi OCR (đọc chữ trên ảnh), rồi một **từ-điển-ký-hiệu** (quy ước `+` = "thêm", `✓` = "xác nhận", `✕` = "đóng"...) — chỉ khi cả bốn đều trượt mới coi là bịa.
2. **Thầy giáo bịa quá ít → cả tiền đề "lọc bỏ bịa" của luận văn lung lay.** Nếu thầy giáo gần như không bịa, thì dữ liệu-đã-lọc và dữ liệu-thô gần như giống nhau → phép so "học trò học từ data lọc" vs "học từ data thô" (gọi là **Tier 1**) rất dễ ra "không khác biệt gì" vì một lý do tầm thường: chẳng có gì để lọc. Đây là điểm quyết định lớn nhất.

## 5. Quyết định lớn: chọn "phương án LAI" (file report/78)

Vì K2 làm lung lay tiền đề "lọc bịa", đã chạy một **cuộc tranh luận đối kháng** (5 tác nhân AI cãi nhau) so hai hướng:

- **Nhánh A (giữ khung cũ):** đóng góp chính = quy trình lọc bịa. Nhược: nếu thầy giáo không bịa thì phép so Tier 1 dễ ra "không khác biệt" → luận văn yếu.
- **Nhánh B (đổi khung):** đóng góp chính = huấn luyện một mô hình 3B chạy trên máy vừa **trung thực** (không bịa nút) vừa **đúng** (hướng dẫn dẫn tới đích). Thêm một cách đo mới: **"trục ĐÚNG"**.

**"Trục ĐÚNG" là gì:** một cách chấm điểm xem hướng dẫn có *đúng, có dẫn tới việc cần làm không* — khác với "trung thực" chỉ đo *có bịa nút không*. Nó dùng bộ dữ liệu **AndroidControl** — bộ này có sẵn **đáp án đúng** do người thật làm (nên chấm được chính xác, không như MobileViews không có đáp án mẫu).

**Kết quả tranh luận: chọn phương án LAI** (lấy điểm tốt của cả hai):

| Thành phần | Vai MỚI | Vì sao |
|---|---|---|
| **Trục ĐÚNG** (chấm bằng đáp án của AndroidControl) | **TRỤ CHÍNH** của luận văn | Có đáp án mẫu → chấm được sạch, **không phụ thuộc** vào chuyện thầy giáo có bịa hay không |
| **Tier 1** (so học-từ-data-lọc vs học-từ-data-thô) | tụt xuống **kết quả phụ** (vẫn báo, không phải trụ) | Vì K2 cho thấy nó dễ ra "không khác biệt" tầm thường |
| **Bốn phép thử K1/K2/OCR/VIỆC1** | gộp thành **một chương đóng-góp về đo lường** | Bản thân việc chỉ ra "đo kiểu ngây thơ không đáng tin, và đây là cách đo đúng" đã là một đóng góp khoa học |

**Hai điều quan trọng cần nhớ:**
- **Tính mới KHÔNG nằm ở "mô hình 3B chạy trên máy"** — đã có vài bài làm rồi (ZonUI-3B, UI-R1, LLaVA-KD). Chỗ chưa ai làm là: **sinh hướng dẫn nhiều bước cho NGƯỜI ĐỌC, rồi đánh giá KÉP** — vừa đo "không bịa" (không cần đáp án mẫu, dùng VH) vừa đo "đúng" (có đáp án mẫu).
- **Vẫn là bài toán MỘT MÀN.** Dùng AndroidControl ở mức *mỗi bước như một màn riêng* (không cần sắp thứ tự các màn) → **không phải** nhánh nhiều-màn. Nhánh nhiều-màn vẫn hoãn như cũ.

## 6. Pilot AndroidControl — phép thử "đèn xanh/đèn đỏ" cho trục ĐÚNG (file report/79, làm đêm qua)

Trước khi cược cả luận văn vào trục ĐÚNG, phải thử xem nó có **khả thi** không. Đây là việc chạy đêm qua. **Kết quả: đèn xanh — và còn tìm được một cách làm tốt hơn.**

Ba điều tìm được:

1. **Toạ độ khớp sạch.** Lo ngại lớn nhất trước đó (report/71) là toạ độ trong đáp án AndroidControl có thể lệch so với ảnh. Kiểm 100 bước thật: **khớp hoàn hảo** — đáp án click vào chỗ nào thì đúng chỗ đó trên ảnh ("Search", "Next", "+" đều trúng). Lo ngại này được xoá.

2. **Cách chấm mà báo cáo trước (report/78) định dùng lại YẾU.** Ý định cũ là: lấy toạ độ đáp án → tra ra tên nút ở đó → so với tên mô hình nói. Nhưng thử thấy **chỉ khoảng 40% bước lấy được tên**, vì **~48% các click nhắm vào nút hình / ảnh / ô danh sách không có chữ**. Ngoài ra, dữ liệu chứa tên-nút-theo-toạ-độ (accessibility-tree) **không có sẵn trên các bản tải nhẹ** (HuggingFace) — chỉ có ở bản gốc nặng vài GB.

3. **Phát hiện cứu bàn:** AndroidControl còn có sẵn một thứ khác — **hướng dẫn từng bước do người thật viết** (ví dụ *"Bấm vào Tools & Hardware"*, *"Bấm nút chia sẻ"*, *"Bấm tab Gmail ở góc dưới bên trái"*). Tôi tải 30 episode kiểm: **chất lượng tốt** — nêu đích danh mục tiêu, có cả **chỉ dẫn vị trí** (đúng cái mà VIỆC1 phát hiện câu chung chung của mình đang thiếu). Vậy thay vì so tên-nút-theo-toạ-độ, ta **so thẳng hướng-dẫn-của-mô-hình với hướng-dẫn-người-viết** (so hai đoạn văn).

Cách mới này tốt hơn hẳn:

| | Cách cũ (so tên nút theo toạ độ) | Cách mới (so hai đoạn hướng dẫn) |
|---|---|---|
| Chấm được bao nhiêu bước | chỉ ~40% (nút có tên) | **~100%** (mọi bước đều có hướng dẫn người viết) |
| Cần dữ liệu accessibility-tree nặng | Có | **Không** |
| Có đo đúng thứ cần đo không | Hơi lệch: đáp án là *thao-tác-cho-máy*, còn ta cần *hướng-dẫn-cho-người* ⚠ | **Khớp**: so người-viết ↔ người-viết ✓ |

**Chưa làm, nói thẳng:** mới xác nhận là **khả thi về mặt dữ liệu** (có sẵn đáp án tốt, toạ độ sạch), **chưa chạy mô hình sinh thử trên AndroidControl** nên chưa có con số điểm thật. Cách chấm "so hai đoạn hướng dẫn" cũng cần định nghĩa cụ thể + kiểm bằng bơm-lỗi (giống cách kiểm thước đo trung thực), và cần luật gióng khi mô hình gộp/tách bước khác với đáp án.

---

# PHẦN C — TRẠNG THÁI & PLAN

## 7. Đang ở đâu

- **Xương sống pipeline: đã chốt** (huấn luyện thế nào, lọc thế nào, train 2 bản để đối chứng).
- **Cách sửa bộ đối chiếu: đã chốt** (làm nhiều tầng: so chuỗi → VH → OCR → từ-điển-ký-hiệu).
- **Hướng đi: đã chốt là phương án LAI** — trục ĐÚNG làm trụ chính, Tier 1 làm phụ.
- **Cách chấm trục ĐÚNG: đã chốt cơ chế mới** (so hướng-dẫn-mô-hình với hướng-dẫn-người-viết của AndroidControl).
- **Đã có sẵn:** danh sách chia 18 app để dạy / 12 app để chấm (đã lưu vào git), bản đăng-ký-trước ngưỡng (report/56, đã lưu git), kho dữ liệu dạy mở rộng 498 màn/220 app. Bốn phép thử + tranh luận + pilot đều xong (report/73–79).
- **Cổng tiếp theo = GẶP THẦY.** **Chưa tiêu một đồng nào để train** — đây là cố ý: vì phương án LAI đổi cách kể đóng góp và đổi bản đăng-ký-trước, nên phải chốt với thầy trước khi tiêu tiền. Nếu tiêu tiền train rồi mới đổi hướng thì phí.

## 8. Plan từ đây đi tiếp — theo đúng thứ tự

### ⛳ Bước 0 — GẶP THẦY (làm TRƯỚC mọi thứ tốn tiền)

Mang ba file lên trình thầy: **`report/77`** (hồ sơ bốn phép thử + các câu hỏi), **`report/78`** (chốt phương án LAI), **`report/79`** (kết quả pilot + cách chấm mới). Cần thầy quyết ba việc:

1. Đồng ý đổi hướng sang phương án LAI (trục ĐÚNG làm trụ chính, Tier 1 làm phụ) không?
2. Đồng ý thêm trục ĐÚNG (dùng đáp án AndroidControl) không? — vì nó thêm một thí nghiệm vào bộ đã đăng-ký-trước.
3. Chấp nhận khả năng Tier 1 ra "không khác biệt" (vì thầy giáo bịa ít) và cách trình bày điều đó một cách trung thực không?

### Sau khi thầy duyệt (phần lớn miễn phí, một ít tốn tiền)

Chú thích: **✱ = bước tốn tiền** (API hoặc thuê GPU Colab). Các bước còn lại miễn phí.

| # | Việc | Tiền? | Giải thích ngắn |
|---|---|---|---|
| 1 | Tải bộ AndroidControl-test về máy (bản có hướng-dẫn-người-viết + ảnh); chọn trước và khoá lại *lát dữ liệu gần với MobileViews nhất* (các app cùng loại) | miễn phí | Tải về một lần cho ổn, đừng stream vì server chập chờn |
| 2 | Định nghĩa cách chấm "so hai đoạn hướng dẫn" + **kiểm nó bằng bơm-lỗi** (cố tình chèn lỗi vào rồi xem thước có bắt được không) | miễn phí | Không tin thước đo khi chưa kiểm |
| 3 | Nghiên cứu nhỏ kiểm "thước có đo đúng thứ cần không": so kết quả thước với người-chấm-tay trên vài chục mẫu | miễn phí | Nhẹ hơn trước vì giờ so người↔người |
| 4 | Nâng bộ đối chiếu thành nhiều tầng (so chuỗi + OCR + từ-điển-ký-hiệu) cho bước lọc dữ liệu | miễn phí | Từ kết quả K1/OCR |
| 5 | Chạy thử nhỏ 5-10 app để tính **MDE** rồi điền vào report/56, lưu git lần 2 | ✱ ~$1-2 | **MDE** = mức chênh lệch nhỏ nhất mà thí nghiệm 12-app đủ sức nhìn thấy; phải biết trước để chắc thí nghiệm không "mù" |
| 6 | Gọi thầy giáo sinh bản nháp → dựng dữ liệu huấn luyện (kèm 2 vá: thêm OCR ở bước lọc + dùng 10 câu chung chung khác nhau thay vì 1 câu) | ✱ ~$1-2 | |
| 7 | Huấn luyện 2 bản mô hình (học-từ-data-lọc và học-từ-data-thô), chạy thử 20 mẫu trước cho chắc | ✱ Colab GPU | |
| 8 | Chấm: chạy **trục ĐÚNG** (trụ chính, so trên AndroidControl) + **Tier 1** (phụ) + tính thống kê | ✱ GPU/API | |
| 9 | Viết bài (FAIR tiếng Anh + VCL tiếng Việt) | — | |

**Thứ tự cứng, không được đảo:** gặp thầy → làm (1)(2)(3)(4) miễn phí → (5) tính MDE → (6)(7) dựng data + train → (8) chấm → (9) viết. Lý do không đảo: bản đăng-ký-trước (quy tắc thắng-thua) phải khoá lại **trước** khi tiêu tiền, nếu không thì "thấy kết quả rồi mới đặt tiêu chuẩn cho vừa" — mất giá trị khoa học.

## 9. Hai bài báo (giữ nguyên kế hoạch)

- **FAIR** (hạn 15/8, tiếng Anh) = bài về mô hình, bài chính. **VCL** (hạn ~30/8, tiếng Việt) = bài sàn chắc ăn (mô hình sinh hướng dẫn bằng tiếng Việt).
- Nếu FAIR không kịp 15/8 → bỏ FAIR, giữ VCL, mô hình gửi hội nghị khác sau.
- Riêng bài VCL: nên để hướng dẫn tiếng Việt **giữ nguyên tên nút hiển thị** (ví dụ giữ "Search") thay vì dịch ("Tìm kiếm") — vừa né được điểm yếu của bộ đối chiếu (K1 đã chỉ ra), vừa hữu ích hơn cho người dùng vì họ thấy đúng chữ đó trên màn.

## 10. Rủi ro lớn nhất còn lại

1. **Chưa có con số điểm-đúng thực.** Mới xác nhận trục ĐÚNG khả thi về dữ liệu; phải chạy mô hình sinh thật mới biết điểm có ra số dùng được không (hay tất cả đều gần 0 → thước vô dụng).
2. **Vẫn là học một nơi, chấm một nơi** (học trên MobileViews, chấm trên AndroidControl). Để bớt sai lệch do khác bộ dữ liệu, ta chấm cả 3 model (học trò-lọc, học trò-thô, thầy giáo) **trên cùng một lát AndroidControl** rồi so **hiệu số** — chênh lệch do khác-bộ bị triệt tiêu bớt. Nhưng cách này dựa trên giả định "khác-bộ ảnh hưởng đều lên cả 3 model", mà giả định đó không kiểm định được → phải khai thẳng là giới hạn.
3. **Cách chấm mới (so hai đoạn hướng dẫn) + luật gióng bước** là chỗ mới, có thể phát sinh nhiễu — cần làm cẩn thận.
4. **Tải công việc nặng:** dựng mô hình + viết 2 bài (một tiếng Anh), làm một mình, trong ~7 tuần.

---

# BẢN ĐỒ FILE

**Đọc để hiểu nhanh:** file này (`report/80`) · `report/70` (all-in-one bản trước kill-test) · `report/00` (ảnh chụp cũ).
**Thiết kế/ngưỡng:** `report/54` (pipeline đầy đủ) · `report/56` (pre-registration).
**Chuỗi kill-test:** `report/73` K1 · `report/74` K2 · `report/75` OCR · `report/76` VIỆC1 · `report/77` hồ sơ gặp thầy.
**Quyết định:** `report/78` chốt nhánh LAI · `report/79` pilot AndroidControl.
**Code mới:** `harness/k1_matcher_killtest.py` · `k2_hallucination_types.py` · `ocr_vh_coverage.py` · `pilot_androidcontrol.py`.
**Kế hoạch 2 bài:** `report/KE_HOACH_2_BAI_BAO.md`. **Config train:** `report/53`.
**Nhật ký quyết định (auto-load):** `CLAUDE.md` §0 (dòng trạng thái mới nhất ở đầu).

> **Nguyên tắc:** đừng tiêu tiền (API/GPU) trước khi gặp thầy chốt khung LAI — vì đổi framing thì pre-registration đổi theo. Mọi bước ✱ hỏi trước (trừ khi đã có standing approval).
