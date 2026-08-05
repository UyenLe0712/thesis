# Toàn cảnh luận văn — chi tiết, đọc một lần hiểu hết

> ⛔ **CẢNH BÁO 2026-07-19 — ĐỌC TRƯỚC KHI TIN BẤT KỲ SỐ NÀO TRONG FILE NÀY.**
> Một vòng phản biện đối kháng (7 giám khảo độc lập, có vòng bác bỏ chéo) đã **lật một số kết luận chính** của file này. Phần *kể chuyện* (đề tài, lịch sử đổi hướng, thiết kế LAI) vẫn đúng; phần *"đã kiểm bằng số, đã qua cổng"* thì **không**.
> **Ba thứ đã bị rút:** cổng kiểm thước (AUC=1.000 là hằng đẳng thức, ca thật cho 0.35) · MDE 8-9 pp (đếm sai file, thật ≈12.5-14.4) · "model đầu tiên sinh hướng dẫn cho người" (GuideMe, CHI 2026 đã chiếm ở mức tác vụ).
> **Đọc `report/90_phan_bien_doi_khang.md` ngay sau file này.** Chỗ nào mâu thuẫn → **90 thắng**. Các dòng đã lỗi thời trong file này được đánh dấu ⛔ tại chỗ.

> Tài liệu tự-đủ: bối cảnh đề tài, toàn bộ việc đã làm (kèm phát hiện), thiết kế cuối đã chốt, kế hoạch dựng dữ liệu + huấn luyện cho hướng mới, và các bước tiếp theo. Viết để đọc một lần là nắm. Ngày: 2026-07-19. ⛔ **Câu "đây là bản mới nhất" đã lỗi thời:** khi mâu thuẫn, thứ tự thắng là **report/90 > report/85 (đã vá) > file này**.

---

# PHẦN 1 — ĐỀ TÀI VÀ BÀI TOÁN

## 1.1. Đề tài

Xây một mô hình trí tuệ nhân tạo nhận **một ảnh chụp màn hình ứng dụng điện thoại** cộng **một câu hỏi** của người dùng (ví dụ *"làm sao để bật thông báo cho tập podcast mới?"*), rồi trả lời bằng **các bước hướng dẫn cụ thể cho người đọc** (kiểu *"1. Chạm vào Settings — 2. Chạm vào Notifications — 3. Bật New episode alerts"*).

## 1.2. Hai cái khó cốt lõi

**Khó thứ nhất — không có đáp án mẫu để chấm.** Không tồn tại sẵn một bộ "hướng dẫn chuẩn" do con người soạn cho từng màn hình. Tự soạn thì tốn hàng nghìn giờ. Nên phải nghĩ ra cách đo chất lượng mà không cần đáp án mẫu.

**Khó thứ hai — một kiểu lỗi nguy hiểm.** Mô hình có thể **bịa ra tên một nút bấm không tồn tại** trên màn hình (ví dụ nói "Chạm Preferences" trong khi màn hình chỉ có nút "Settings"). Người dùng làm theo sẽ dò không thấy hoặc bấm nhầm. Lỗi này khó phát hiện bằng mắt vì câu văn đọc lên vẫn trơn tru.

## 1.3. Ràng buộc bắt buộc của thầy

Luận văn thạc sĩ của trường **bắt buộc phải có một mô hình do học viên tự huấn luyện** — không được chỉ ghép các công cụ có sẵn qua việc gọi API. Ràng buộc này là cứng, đã được xác nhận lại. Mô hình phải là **một đóng góp thật**, không phải chỉ làm nền.

---

# PHẦN 2 — CÂU CHUYỆN ĐỔI HƯỚNG (VÌ SAO THIẾT KẾ THÀNH RA NHƯ HIỆN TẠI)

Thiết kế hiện tại là kết quả của một chuỗi kiểm chứng và điều chỉnh. Hiểu chuỗi này thì hiểu vì sao mọi thứ như bây giờ.

## 2.1. Bản đầu (bị thầy bác)

Ban đầu luận văn = gọi API của mô hình gpt-4o-mini để đọc ảnh viết hướng dẫn, rồi dùng thuật toán so sánh chuỗi để kiểm bịa. Thầy bác vì *"chủ yếu là gọi API và so chuỗi, chưa thấy mô hình do học viên tự huấn luyện đâu"*.

## 2.2. Hướng "chưng cất trung thực" (Faithful Distillation)

Để có mô hình tự huấn luyện, chuyển sang ý tưởng **"thầy giáo — học trò"**:
- **Thầy giáo** = gpt-4o-mini (mô hình lớn, gọi qua mạng) viết bản nháp hướng dẫn.
- Đối chiếu tên nút với **View Hierarchy** (viết tắt VH — một file do hệ điều hành Android xuất kèm mỗi ảnh, liệt kê mọi nút thật trên màn hình cùng vị trí). Chỗ nào bịa thì **viết lại thành câu mô tả chung chung** (gọi là "fallback").
- Dữ liệu đã lọc sạch → **huấn luyện học trò** = mô hình nhỏ Qwen2.5-VL-3B (chạy được ngay trên máy, không cần internet).

Đóng góp dự kiến lúc đó: quy trình **lọc bỏ chỗ bịa** để tạo dữ liệu sạch → dạy học trò trung thực hơn thầy giáo.

## 2.3. Bốn phép thử miễn phí lật đổ tiền đề (đây là bước ngoặt)

Trước khi tiêu tiền huấn luyện, chạy bốn phép thử **miễn phí, ngay trên máy** để kiểm tiền đề. Kết quả lật vài giả định quan trọng:

**Phép thử K1 — kiểm "bộ đối chiếu".** Bộ đối chiếu là thuật toán so tên nút mô hình nói với danh sách nút thật trong VH; khớp thì giữ, không khớp thì coi là bịa. K1 kiểm nó theo hai chiều:
- *Chiều bỏ lọt:* mô hình bịa một tên **nghe giống** nút thật (nói "Send" khi màn chỉ có "Save"). Vì gần nghĩa, thuật toán tưởng đúng nên cho qua → **bịa lọt vào dữ liệu**.
- *Chiều kết oan:* mô hình gọi **đúng** nút nhưng bằng từ khác ("Tìm kiếm" cho nút "Search"). Thuật toán không nhận ra → đánh nhầm là bịa.
- **Kết quả:** thuật toán **bỏ lọt 47,5% + kết oan 47,5%**, và điểm số hai loại **trùng lên nhau hoàn toàn** → **không có ngưỡng nào tách được**. Đổi sang thuật toán so nghĩa mạnh hơn (kể cả của OpenAI) cũng chỉ đỡ chút — đây là hạn chế bản chất của việc đo độ gần nghĩa.

**Phép thử K2 — đếm mô hình-thầy bịa thật bao nhiêu.** Đọc tay 80 màn hình mà gpt-4o-mini đã viết hướng dẫn từ trước. Kết quả gây bất ngờ: **gpt-4o-mini gần như KHÔNG bịa (chỉ ~0-2%)**, không phải "khoảng một phần tư" như tưởng. Những chỗ bị đánh "bịa" thật ra là **nút CÓ THẬT nhưng VH bỏ sót nhãn** — nhất là nút hình (dấu cộng để thêm, dấu tích để xác nhận).

**Phép thử OCR — thử đọc chữ trên ảnh bù chỗ VH thiếu.** Giúp được với nút có chữ (đưa độ phủ nhãn từ 74% lên 80%), nhưng thua nút hình thuần; còn ~20% nút không cách nào lấy được nhãn.

**Phép thử VIỆC1 — đọc tay câu "chung chung".** Câu an toàn nhưng **lặp lại đúng câu hỏi**, không chỉ chỗ bấm → giá trị thấp; và vì K2, nó thường thay một nút thật cụ thể bằng câu mơ hồ.

**Hệ quả lớn:** tiền đề *"thầy giáo bịa nhiều, ta lọc bỏ → dạy học trò trung thực hơn"* **lung lay** — vì thầy giáo gần như không bịa, nên chẳng có gì để lọc.

## 2.4. Chuyển sang "phương án lai" (qua debate đối kháng)

Vì tiền đề lung lay, chạy hai vòng tranh luận đối kháng để chốt hướng mới:

- **Không** lấy "lọc bịa" làm đóng góp chính (đã yếu).
- **Lấy "độ ĐÚNG" làm trục chính** — đo bằng bộ dữ liệu **AndroidControl**, vì bộ này **có sẵn đáp án đúng do người thật làm** (chấm được chính xác, khác hẳn MobileViews vốn không có đáp án).

**"Độ đúng"** = hướng dẫn có *đúng, có dẫn tới việc cần làm* không — khác với **"độ trung thực"** vốn chỉ đo *có bịa nút không*.

## 2.5. Pilot xác nhận + tìm cách hay hơn

Chạy thử (pilot) trên AndroidControl để kiểm trục ĐÚNG có khả thi không. **Đèn xanh**, và tìm được cách tốt hơn: AndroidControl có sẵn **hướng dẫn từng bước do người viết** (ví dụ *"Bấm vào tab Gmail ở góc dưới bên trái"*). → thay vì mò tên nút theo toạ độ, ta **so thẳng hướng dẫn của mô hình với hướng dẫn do người viết** (so hai đoạn văn).

---

# PHẦN 3 — THIẾT KẾ CUỐI (ĐÃ CHỐT)

## 3.1. Hai đóng góp ngang nhau

1. **Đóng góp MÔ HÌNH** — một mô hình sinh **hướng dẫn ngôn ngữ nhiều bước CHO NGƯỜI ĐỌC** từ một ảnh + câu hỏi. Điểm khác biệt: **mọi mô hình giao diện hiện có** (SeeClick, UI-R1, OS-Atlas, Aguvis...) đều sinh **thao tác cho MÁY tự bấm** (toạ độ / mã hành động, chấm bằng tỉ lệ agent làm xong việc); luận văn này sinh **hướng dẫn cho NGƯỜI đọc và tự làm**, kèm ràng buộc trung thực (không bịa nút). Tính mới nằm ở **tác vụ + cách đánh giá này**, KHÔNG ở chỗ "mô hình 3 tỉ tham số chạy trên máy" (chỗ đó đã có nhiều bài).
   > ⚠️ **KHÔNG được nói "mô hình ĐẦU TIÊN".** Vòng kiểm chống-scoop (report/82) xác nhận chỗ trống còn thật nhưng HẸP, và có vài bài lân cận phải phân định (Wang et al. CHI 2023; GUITrans2Act) — chưa đọc hết. "Đầu tiên" là claim tuyệt đối, chỉ cần một phản ví dụ là sụp. Nói an toàn: *"khác hướng chủ đạo"*, và cược tính-mới vào **tổ hợp bốn thành phần + phát hiện thực nghiệm + cặp thước**, không vào chữ "đầu tiên". Đây là điểm thoả ràng buộc train-model của thầy.
2. **Đóng góp ĐÁNH GIÁ** — cặp thước đo **độ trung thực (đối chiếu VH, không cần đáp án) + độ đúng (so đáp án)**, cộng phát hiện thực nghiệm từ bốn phép thử về vì sao cách đo ngây thơ hỏng.

Hai trụ báo cáo độc lập: một trục ra kết quả rỗng không kéo sập trục kia.

## 3.2. Huấn luyện trên dữ liệu nào (viết chi tiết)

Mục tiêu huấn luyện: dạy mô hình nhỏ (Qwen2.5-VL-3B), khi nhìn một màn hình và biết mục tiêu người dùng, **tự viết ra câu hướng dẫn cho bước kế tiếp** — bắt chước cách người thật viết. Dùng **hai nguồn dữ liệu, vai khác nhau:**

**Nguồn CHÍNH — AndroidControl (phần app dành để dạy).** AndroidControl là bộ dữ liệu do Google công bố (đã bình duyệt, NeurIPS 2024), trong đó mỗi thao tác được **một người thật ghi kèm một câu hướng dẫn từng bước** (ví dụ *"Bấm vào tab Gmail ở góc dưới bên trái"*). Mỗi mẫu huấn luyện được dựng như sau:

> **Đưa vào:** ảnh màn hình tại một bước + mục tiêu tổng thể + các bước đã làm trước đó.
> **Dạy nó trả ra:** đúng câu hướng dẫn do người viết cho bước đó.

Đây là **tín hiệu chính** vì nó chính là loại đầu ra ta muốn (hướng dẫn cho người), và có sẵn "đáp án" chất lượng do người viết. Học trên đây → khi chấm trên app khác của cùng bộ (Phần 3.3), mô hình có lợi thế "đúng loại dữ liệu".

**Nguồn PHỤ — MobileViews chưng cất (có thí nghiệm bật/tắt).** MobileViews chỉ có ảnh + View Hierarchy, **không có** hướng dẫn do người viết. Nên với bộ này, thầy giáo gpt-4o-mini sinh nháp hướng dẫn (không cho thấy View Hierarchy), rồi lọc chỗ bịa bằng **bộ đối chiếu đa tầng đã nâng cấp** (so chuỗi → View Hierarchy → OCR → từ điển ký hiệu — chứ không phải bộ đơn đã chết ở K1). Dữ liệu này **bổ sung độ rộng** (nhiều app hơn, đa dạng hơn) chứ không còn vai "lọc bịa để dạy trung thực" như tiền đề cũ (K2 đã bác tiền đề đó).

> **Bắt buộc huấn luyện HAI bản để so:** một bản CÓ dữ liệu phụ MobileViews, một bản KHÔNG. Chênh lệch giữa hai bản cho biết dữ liệu phụ có đóng góp gì thật — nếu không, ta thành thật báo là không, và chỉ giữ nguồn chính.

**Cấu hình huấn luyện:** kỹ thuật nhẹ **QLoRA** — thay vì dạy lại cả mô hình (rất tốn), chỉ gắn thêm ít "miếng dán" học được vào phần "nói" (viết câu) và **đóng băng phần "nhìn"** (hiểu ảnh), vì việc cần dạy là *nói gì*, không phải *nhìn thấy gì*. Chạy trên một GPU thuê của Google Colab, khung phần mềm LLaMA-Factory.

## 3.3. Đo ở đâu (điểm khác quan trọng so với bản trước)

- **Trục ĐÚNG (chính):** đo **ngay trên phần app chưa từng thấy của chính AndroidControl** (gọi là phần app dành để chấm (app-unseen) — học và chấm cùng một bộ dữ liệu nhưng dùng những app khác nhau, để mô hình không "học thuộc" app rồi chấm chính nó). Cách này **bỏ được một lỗ hổng** của bản thiết kế trước (report/78): bản đó huấn luyện trên MobileViews nhưng chấm trên AndroidControl — hai bộ khác nhau — nên điểm thấp có thể do *khác bộ dữ liệu* chứ không phải do hướng dẫn kém. Giờ **học và chấm trên cùng một bộ** (chỉ khác app) thì loại được nhầm lẫn đó. So sánh: **Học trò (Student) với Thầy giáo gốc (Teacher-BASE — tức gpt-4o-mini chưa chỉnh gì)**.
  > *Lưu ý phạm vi:* "app chưa từng thấy cùng một bộ" là mức khái quát hoá chuẩn ngành (held-out theo app), **chưa phải** khái quát sang bộ dữ liệu hoàn toàn khác (cross-dataset) — cái đó để dành bài mở rộng, ngoài phạm vi mùa này.
- **Trục TRUNG THỰC (phụ):** đo trên MobileViews (tắt VH lúc sinh, xem học trò có bịa nút không). Giữ vai phụ vì K2 cho thấy nó dễ ra kết quả rỗng tầm thường.
- **ScreenSpot-v2:** đối chứng grounding, không phải điểm chính.

## 3.4. Thước đo "so hai đoạn hướng dẫn" (đã kiểm bằng số)

Thước tách mỗi bước thành cặp **(thao-tác, đích)**:
- **Thao-tác** = loại hành động, khớp trên từ vựng đóng (chạm/gõ/cuộn/mở/quay-lại).
- **Đích** = tên nút/vùng được gọi, khớp bằng **so từ khoá là chính, embedding bge-m3 làm dự phòng ở ngưỡng cao**.

**Đây là chỗ vá đúng bẫy K1:** "tab Gmail" và "tab Calendar" chung từ "tab" nhưng khác từ khoá (Gmail vs Calendar) → chồng-từ thấp → **không khớp (bắt được lỗi)** — điều mà đo cả câu (K1) không làm nổi.

Ba số đọc ra: **coverage** (hướng dẫn phủ được bao nhiêu bước-đúng — số chủ đạo), **F1** (chống nhồi bước thừa/bịa), **order-τ** (đúng thứ tự). Báo **thao-tác và đích riêng**, tách nhóm **đích-chữ và đích-icon**. So Học trò với Thầy giáo gốc trên cùng bộ.

> **Một chỗ phải nói trung thực (thầy dễ hỏi):** thước này so hướng dẫn của mô hình với hướng-dẫn-**người-viết** của AndroidControl (văn bản với văn bản, không phải với thao tác cho máy). Nhưng nó chỉ đo *"bước có gọi đúng thao-tác + đúng đích không"* — đây là **proxy (đại diện) cho tính-ĐÚNG của bước**, KHÔNG trực tiếp đo *"câu hướng dẫn có dễ đọc, đủ dùng cho một người thường không"*. Cái sau (**độ hữu-ích cho người**) đo **riêng** bằng một nghiên cứu nhỏ cho người chấm vài chục câu. Hai thứ tách bạch, không lẫn — nói thẳng vậy sẽ chặn được đòn *"thước đo con máy chứ đâu đo hướng dẫn cho người"*.

---

# PHẦN 4 — ĐÃ KIỂM CHỨNG GÌ BẰNG SỐ (không phải suy luận)

Đây là phần quan trọng: mọi giả định lớn đã được **đo**, không phải đoán.

## 4.1. Thước có tránh được bẫy K1 không? → CÓ (report/84)

> **"Bẫy K1" là gì — giải thích rõ.** Phép thử K1 (Phần 2.3) phát hiện: nếu đo chất lượng bằng cách so **độ gần nghĩa của cả câu** (dùng embedding), thì có **hai loại câu trông giống nhau nhưng bản chất ngược nhau**, và không cách nào tách:
> - **Bịa nghe giống thật** — mô hình nói một nút KHÔNG có thật nhưng nghe gần: màn có "Save", mô hình bịa "Send". Embedding thấy "Send" và "Save" rất gần → tưởng đúng → **cho qua (sai, phải bắt)**.
> - **Gọi đúng nhưng khác chữ** — mô hình gọi đúng nút thật bằng từ khác: nút "Search", mô hình nói "Tìm kiếm". Embedding thấy hơi xa → tưởng bịa → **đánh oan (sai, phải nhận)**.
>
> Vì cả hai đều là "hai câu gần-gần nhau", **điểm số của chúng chồng lên nhau hoàn toàn** → dù đặt ngưỡng ở đâu cũng dính một trong hai lỗi. Đây là "bẫy": **đo độ gần nghĩa của cả câu về bản chất không thoát được.** Đổi embedding mạnh hơn (kể cả OpenAI) chỉ đỡ chút.
>
> **Cách thước mới thoát bẫy:** không đo cả câu. Tách mỗi bước thành **(thao-tác, đích)** rồi so **đích bằng từ khoá**. "tab Gmail" và "tab Calendar" chung từ "tab" nhưng **khác từ khoá** (Gmail ≠ Calendar) → không khớp → bắt được lỗi. Còn "Search" và "Tìm kiếm" thì để lớp dự phòng (bge-m3) cứu. Tức là **tách bạch "khác nút" (bắt) khỏi "khác chữ cùng nút" (tha)** — đúng cái đo cả câu không làm nổi.

Để chắc thước mới thật sự thoát bẫy (không chỉ nói suông), ta **bơm các lỗi đã biết** vào hướng dẫn gold rồi kiểm thước có bắt được + có tách được "sai-đích" khỏi "paraphrase" (viết khác nhưng cùng nghĩa). Kết quả:
- ⛔ **VÁ 19/7 (report/90): ~~AUC = 1.000~~ KHÔNG PHẢI PHÉP ĐO.** Bộ bơm-lỗi dựng ca "paraphrase" bằng cách gọi chính hàm của thước (`target_of`) rồi dán lại nguyên văn output → trùng từ 100% theo định nghĩa; ca "sai-đích" thì bị ép không được trùng từ nào → khác 100% theo định nghĩa. AUC=1.000 chỉ là `P(1.0 > 0.0)`, phương sai bằng không. **Đo lại bằng paraphrase THẬT (`filter option`↔`funnel icon`): kết oan 10/10, AUC = 0.35.** Vòng "ca khó" không có code lẫn file kết quả trong repo.
- Bắt lỗi sai = 1.000, báo động giả trên paraphrase = 0.000.
- ⛔ **VÁ 19/7: câu "tách (thao-tác, đích) giải được đúng chỗ K1 chết" đã bị RÚT.** Nó chỉ chứng minh thước phân biệt được hai thái cực — việc mà khớp-chuỗi thuần cũng làm được. Thước **chưa được kiểm**, và lần thử đầu tiên bằng ca thật thì **rớt**. Việc kế: `report/90` Giai đoạn B (dựng lại bơm-lỗi) + C (`harness/cv_study/`, hỏi người).
- *Hoài nghi còn giữ:* nếu mô hình thật dùng từ đồng nghĩa cho loại nút ("tab"→"section") có thể kết oan → chỉnh dự phòng bge-m3 khi có output mô hình. Không phải blocker.

## 4.2. Đủ lực thống kê không? → CÓ (report/86, pilot có tốn ~$0.5)

Đo độ dao động điểm-đúng của thầy giáo gpt-4o-mini trên ảnh thật AndroidControl (26 app):
- Thầy giáo điểm-đúng = **30%** → **không suy biến về 0** (trục đo được, qua đúng cổng lo lắng ở pilot).
- ⛔ **VÁ 19/7: ~~MDE ≈ 8-9 pp @ 150-200 app~~ — G đếm từ SAI FILE.** Số app lấy từ `ac_test_200ep.json` (test set CHUNG), không phải app_unseen split. Đếm trên đúng split: **41% ep gán được app** (không phải 72%), **42 app distinct**, và app **tập trung mạnh** (Pinterest 14, Arts&Culture 8) chứ không "phần lớn singleton". → **MDE thật ≈ 12.5-14.4 pp** — vẫn dưới ngưỡng 15-20 nhưng SÁT hơn nhiều. Thêm: bộ gán app tách một app thành nhiều cụm (`The Washington Post` vs `Washington post`) và đẻ cụm rác (`On the Pinerest`) → G thổi phồng, CI hẹp giả. Phải gán app lại cho cả 631 ep rồi tính lại.
- **Hướng kỳ vọng là dương:** học trò huấn luyện *trên chính* AndroidControl gold → chấm in-distribution → có lợi thế sân nhà so thầy giáo zero-shot. Nên "học trò hơn thầy giáo về độ đúng in-domain" là kết cục hợp lý.
- *Giới hạn khai thẳng:* 30% thấp một phần vì thước per-bước nghiêm (có nhiều bước hợp lệ mà đáp án chỉ ghi một) → 30% là cận dưới, số chủ đạo (coverage cả episode) sẽ cao hơn.

## 4.3. Có bị người khác làm mất (scoop) không? → KHÔNG (report/82)

Kiểm văn liệu + tải thẳng bài đối thủ gần nhất (GUITrans2Act) để xác nhận nó khác:
- Chỗ trống còn thật: không bài nào phủ đủ bốn thứ cùng lúc — người đọc là NGƯỜI + hướng dẫn nhiều bước + đánh giá kép + mô hình nhỏ.
- Tính mới **phòng thủ được:** (a) đo trung thực bằng nguồn ngoài có cấu trúc (VH) thay vì tự hỏi lại ảnh; (b) dùng hướng dẫn cho người của AndroidControl làm **đích để sinh** (chưa ai làm — mọi bài dùng bộ này đều để nó ở đầu-vào).
- **Không được claim:** "đánh giá kép là phát kiến" (đã có), "mô hình 3B trên máy" là điểm mới (đông), "sinh hướng dẫn GUI cho người là mới hoàn toàn" (phải phân định vài bài).

---

# PHẦN 5 — KẾ HOẠCH DỰNG DỮ LIỆU + HUẤN LUYỆN (cho tín hiệu AndroidControl-gold)

> Đây là phần kỹ thuật cập nhật cho hướng mới (kế hoạch cũ report/53 viết cho hướng MobileViews (chưng cất), nay đổi). Đọc khi bắt tay lên Colab.

## 5.1. Dựng dữ liệu huấn luyện

**Nguồn chính — AndroidControl (app TRAIN-split, tức KHÔNG phải 631 app-unseen dành để chấm):**
- Mỗi mẫu huấn luyện = **(ảnh màn hình tại một bước) + (mục tiêu tổng thể + các bước đã làm) → (hướng dẫn do người viết cho bước đó)**.
- Nói cách khác: dạy mô hình, khi thấy một màn hình và biết mục tiêu, sinh ra đúng câu hướng dẫn cho bước kế tiếp — bắt chước cách người thật viết trong AndroidControl.
- Tải từ mirror `wangyuanlei/android_control_test` (đã có `step_instructions` + ảnh png) cho phần test; phần train tải tương tự từ split train của AndroidControl.

**Nguồn phụ — MobileViews chưng cất (có thí nghiệm bật/tắt):**
- Thầy giáo gpt-4o-mini sinh nháp hướng dẫn trên màn MobileViews (không thấy VH).
- Bộ đối chiếu **đa tầng nâng cấp** (so-chuỗi → VH → OCR → từ-điển-ký-hiệu — chứ KHÔNG phải bộ nomic-đơn đã chết ở K1) lọc chỗ bịa.
- **Cân nhắc BỎ bước viết lại thành câu chung chung** vì VIỆC1 cho thấy câu chung chung làm hại — quyết lúc build, ghi rõ.

**Định dạng:** đóng gói thành định dạng LLaMA-Factory (mỗi mẫu là một cặp hội thoại ảnh-vào / câu trả ra). Gắn thẻ nguồn (AndroidControl vs MobileViews) trong prompt nếu pilot cho thấy hai giọng văn xung đột.

## 5.2. Cấu hình huấn luyện

- Mô hình gốc: Qwen2.5-VL-3B.
- Kỹ thuật: **QLoRA 4-bit** (chạy được GPU T4 16GB của Colab), miếng dán LoRA r=8 / alpha=16, chỉ gắn vào phần "nói" (decoder), **đóng băng phần "nhìn"** (vì việc cần dạy là *nói gì*, không phải *nhìn thấy gì*).
- Tốc độ học ~1e-4, khoảng 3 vòng qua dữ liệu (con số ước tính, cần chạy thử xác nhận).
- **Huấn luyện HAI bản:** một bản có dữ liệu phụ MobileViews, một bản không (để so — thí nghiệm bật/tắt).

## 5.3. Bẫy kỹ thuật đã biết (đề phòng trước)

- **Xuất mô hình ra định dạng chạy nhẹ (GGUF) từng lỗi với đúng dòng mô hình này** → thử xuất SỚM ngay khi có bản lưu tạm đầu tiên, đừng đợi train xong.
- **Xung đột giọng văn** khi trộn hai nguồn (văn tự do MobileViews vs câu ngắn AndroidControl) → chạy thử nhỏ trước, gắn thẻ nguồn.
- **Colab rớt phiên / hết VRAM** → lưu checkpoint thường xuyên, xếp lệnh train chạy qua đêm.

---

# PHẦN 6 — VIỆC TIẾP THEO (theo thứ tự)

## 6.1. Đã xong (khâu miễn phí + chuẩn bị)

| Việc | Trạng thái |
|---|---|
| Tải AndroidControl-test về máy | ✅ 631 episode app-unseen + 200 local |
| Build + kiểm thước (**cổng bơm-lỗi**) | ⛔ **KHÔNG QUA** — cổng cũ là hằng đẳng thức; ca thật cho AUC=0.35. Dựng lại: report/90 §B |
| Viết bản đăng ký trước mới (report/85) | ✅ đã commit git (b5a6b29) |
| Đếm app + định nghĩa split | ✅ (631 ep, bỏ "lát gần-miền") |
| Pilot đo MDE | ⚠ **tính lại** — G sai file; MDE thật ≈12.5-14.4 pp. Trục trung thực (G=12) chưa điền ô MDE, ước ~32 pp = **thiếu lực** |

## 6.2. Còn lại — PHA XÂY MÔ HÌNH (tốn tiền + Colab)

**Bước tốn tiền, làm khi sẵn sàng lên Colab:**
1. Chốt số app chính xác trong split + điền nốt bản đăng ký trước → commit lần cuối.
2. Dựng dữ liệu huấn luyện (Phần 5.1) — gọi thầy giáo cho phần MobileViews-phụ (tốn ít API).
3. **Chạy thử nhỏ 20 mẫu trên Colab** để chắc pipeline chạy được (rẻ), trước khi train full.
4. Huấn luyện hai bản mô hình (có/không dữ liệu phụ) — tốn GPU Colab, ~$60-70 cả pha.
5. Chấm: trục ĐÚNG (chính) + trục TRUNG THỰC (phụ) + thống kê.
6. Hiệu chỉnh thước với output thật (dự phòng bge-m3, validate bộ trích).
7. Nghiên cứu nhỏ kiểm thước vs người chấm (construct-validity).
8. Viết luận văn + hai bài báo.

## 6.3. Việc thuộc về thầy (không đo được, cần hỏi)

Cách kể đóng góp (mô hình-tác vụ mới + đánh-giá) có hợp gu hội đồng không — chỉ thầy/hội nghị biết. Đã chọn tự-quyết đi tiếp, sai thì chỉnh.

---

# PHẦN 7 — RỦI RO CÒN LẠI VÀ CÁCH XỬ

1. **Bộ trích (thao-tác, đích) trên guide dài mô hình sinh có thể hỏng** → validate bộ trích riêng khi có output.
2. **Dự phòng bge-m3 có thể kết oan paraphrase đổi sang từ đồng nghĩa** → chỉnh ngưỡng khi có output.
3. **~48% đích là icon/ảnh** → báo tách nhóm chữ vs icon, đừng gộp.
4. **Vòng lặp ngược** (train trên đáp án rồi chấm so đáp án) → có mốc Thầy giáo gốc + thước ưu tiên khớp thao-tác∧đích (bớt nhạy giọng văn).
5. **Tính mới mỏng ở kiến trúc** → bán bằng tác vụ mới + đánh-giá, không bằng kích thước.
6. **Tải công việc nặng** (dựng mô hình + 2 bài, một mình, ~7 tuần) → ưu tiên bài tiếng Việt làm sàn chắc.

---

# BẢN ĐỒ FILE (đã dọn gọn 19/7 — report/ giờ chỉ còn bộ đang dùng; phần cũ ở report/_archive/)

**Đọc để hiểu:**
- **File này (report/88)** = toàn cảnh chi tiết — đọc đầu tiên để nắm bối cảnh, **rồi đọc `report/90` ngay sau** (cái gì hỏng + kế hoạch A→F). Chỗ nào hai file mâu thuẫn thì **report/90 thắng**.
- **report/89** = review slide + 7 câu thủ cho chỗ thầy dễ vặn (đọc khi sắp gặp thầy).
- Slide trình thầy: **LUAN_VAN_SLIDE_v5.pptx** (mỗi slide có ghi chú người nói).

**Bằng chứng (mở khi cần tra một con số):**
- Bốn phép thử: report/73 (K1) · 74 (K2) · 75 (OCR) · 76 (VIỆC1).
- Quyết định + thiết kế: report/78 (chọn hướng lai) · 79 (pilot) · **81 (thiết kế cuối)** · 82 (chống scoop).
- Kiểm bằng số: report/84 (⛔ cổng bị rút) · 86 (⚠ MDE tính lại) · **report/90 (phản biện đối kháng — đọc kèm file này; chỗ nào mâu thuẫn thì 90 thắng)** · report/90b (nguyên văn 27 đòn).
- **Bản đăng ký trước: report/85** (đã commit b5a6b29).

**Tham chiếu kỹ thuật còn giữ:** report/54 (cơ chế pipeline chi tiết) · 56 (đăng-ký-trước cũ, làm bản ghi + chi tiết trục trung thực) · 57 (related work) · 53 (config build) · 44/48 (dữ liệu) · KE_HOACH_2_BAI_BAO · RESEARCH_LEDGER.

**Mã nguồn:** harness/ — k1_matcher_killtest · k2_hallucination_types · ocr_vh_coverage · pilot_androidcontrol · metric_v1_validate · mde_pilot · ac_test_200ep.json (data).

**Đã archive (report/_archive/, khôi phục được):** toàn bộ khung prompting cũ (00-52 phần lớn), chuỗi research pre-LAI (61-68), các bản tóm tắt/plan bị file này thay (00/70/71/72/77/80/83), slide cũ v1-v4. Nhật ký quyết định: **CLAUDE.md** §0.
