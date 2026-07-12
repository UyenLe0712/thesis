# GIẢI THÍCH TOÀN BỘ LUẬN VĂN — Đọc từ số 0

> **File này là gì?** Đây là bản giải thích **dễ hiểu nhất**, viết cho người **chưa biết gì** về đề tài. Mọi từ chuyên môn đều được giải thích ngay khi xuất hiện, kèm ví dụ. Đọc xong file này là bạn nắm trọn: đề tài làm gì, tại sao làm vậy, đã chốt gì, còn phải quyết gì. Các file khác (`01`–`10`) chỉ là bản chi tiết kỹ thuật của từng phần.
>
> **Cách đọc:** đọc tuần tự từ trên xuống. Mỗi mục xây trên mục trước.

---

## PHẦN 0 — Hình dung đề tài trong 1 phút

Tưởng tượng bạn mở một ứng dụng điện thoại lạ (ví dụ app thuế, app ngân hàng) và không biết bấm vào đâu. Bạn chụp lại **màn hình** đang hiện ra, rồi hỏi một câu bằng tiếng Việt bình thường:

> *"Tôi muốn kiểm tra mình đã nộp thuế chưa thì vào đâu?"*

Đề tài này xây một hệ thống dùng trí tuệ nhân tạo (AI) để **tự động viết ra hướng dẫn từng bước** trả lời câu hỏi đó, dựa đúng vào những gì có trong tấm ảnh bạn chụp. Ví dụ máy trả lời:

> 1. Bấm vào nút **"Tra cứu"** ở góc dưới bên phải.
> 2. Chọn mục **"Nghĩa vụ thuế"**.
> 3. Xem dòng **"Tình trạng: Đã nộp / Chưa nộp"**.

Đó là toàn bộ ý tưởng: **ảnh giao diện + câu hỏi → hướng dẫn từng bước cho con người đọc.**

---

## PHẦN 1 — Những từ chuyên môn cơ bản (đọc 1 lần là quen)

Trước khi đi sâu, ta thống nhất vài từ sẽ lặp lại suốt file. Đừng lo, mỗi từ chỉ là một khái niệm đơn giản.

- **AI / mô hình (model):** một chương trình máy tính đã được "học" từ rất nhiều dữ liệu, có thể tự tạo ra câu trả lời. Trong file này "model" = "cái máy AI đang làm việc".

- **LLM (Large Language Model — mô hình ngôn ngữ lớn):** loại AI chuyên về **chữ**. Bạn đưa chữ vào, nó trả chữ ra. Ví dụ nổi tiếng: ChatGPT. 

- **VLM (Vision-Language Model — mô hình thị giác-ngôn ngữ):** giống LLM nhưng **nhìn được ảnh**. Bạn đưa **ảnh + chữ** vào, nó trả **chữ** ra. Đề tài này cần VLM vì đầu vào có ảnh giao diện. Ví dụ: GPT-4o, Gemini, Qwen2.5-VL.

- **Screenshot (ảnh chụp màn hình):** tấm ảnh chụp lại đúng những gì đang hiện trên màn hình điện thoại/máy tính.

- **Giao diện người dùng (UI — User Interface):** phần màn hình mà người dùng nhìn thấy và bấm vào (các nút, ô chữ, menu...).

- **Use-case (trường hợp sử dụng):** mục đích người dùng muốn đạt được, viết bằng câu hỏi tự nhiên. Ví dụ: *"làm sao để đổi mật khẩu?"*.

- **Hướng dẫn từng bước (step-by-step tutorial):** văn bản đánh số 1, 2, 3... bảo người dùng bấm gì, nhập gì, theo thứ tự.

- **Đa phương thức (multimodal):** hệ thống xử lý **nhiều loại đầu vào cùng lúc** — ở đây là **ảnh + chữ**.

Giữ 3 từ này trong đầu là đủ: **model** (cái máy AI), **VLM** (AI nhìn được ảnh), **tutorial** (hướng dẫn từng bước).

---

## PHẦN 2 — Bài toán khó ở chỗ nào?

Nghe thì đơn giản, nhưng có **một khó khăn lớn** khiến đề tài này thành một luận văn nghiên cứu chứ không phải bài tập:

> **Không có "đáp án mẫu" để so sánh.**

Giải thích: thông thường khi dạy máy làm gì, người ta có sẵn **đáp án đúng do con người soạn** để chấm điểm. Ví dụ dịch máy: có sẵn bản dịch chuẩn của người để so. Nhưng ở đây, **không ai ngồi soạn sẵn hàng nghìn bài hướng dẫn chuẩn** cho mọi app, mọi màn hình. Tự soạn thì quá tốn công và không bao quát hết.

Vậy câu hỏi cốt lõi của luận văn trở thành:

> **"Khi máy viết ra một bài hướng dẫn, mà ta KHÔNG có đáp án mẫu để so, thì làm sao biết bài đó ĐÚNG hay SAI, TỐT hay DỞ?"**

Trả lời câu hỏi này — tức xây **một cách đánh giá đáng tin khi không có đáp án mẫu** — là **một trong HAI đóng góp NGANG NHAU** của luận văn (cập nhật 2026-06-25). **Đóng góp còn lại = chính hệ thống sinh hướng dẫn (ReOrder-Tutor) phải ra kết quả TỐT** (giảm bịa, đúng-chỗ hơn so với baseline & GPT-4o), **chứ không chỉ là "công cụ để chấm"**.

---

## PHẦN 3 — Hai chế độ sử dụng: một ảnh và nhiều ảnh

Sản phẩm nhận đầu vào ở **hai chế độ**, tùy người dùng đưa vào **bao nhiêu ảnh**:

### Chế độ A — Một ảnh (đơn bước)
Người dùng đưa **1 tấm ảnh** + 1 câu hỏi liên quan đúng màn đó. Câu trả lời nằm gọn trong màn hình đó.

> *Ví dụ:* ảnh màn hình chính của app thuế + câu hỏi *"vào đâu để tra cứu thuế?"* → máy chỉ cần nhìn 1 ảnh và chỉ đường.

### Chế độ B — Nhiều ảnh (đa bước)
Người dùng đưa **N tấm ảnh** (N nghĩa là "một số lượng nào đó", ví dụ 3, 4, 5 tấm) của **cùng một quy trình nhiều bước**, KÈM một điều quan trọng:

> **Các ảnh này bị XÁO TRỘN — không theo đúng thứ tự.**

Máy phải **tự suy ra thứ tự đúng** của các màn rồi mới viết hướng dẫn theo thứ tự đó.

> *Ví dụ:* người dùng chụp 4 màn của quy trình "chuyển tiền" nhưng đưa lộn xộn: [màn xác nhận] [màn đăng nhập] [màn nhập số tiền] [màn chọn người nhận]. Máy phải tự sắp lại đúng: đăng nhập → chọn người nhận → nhập số tiền → xác nhận, rồi viết hướng dẫn.

**Điểm cực kỳ quan trọng (bạn đã nhấn mạnh):** trong cả hai chế độ, **mọi tấm ảnh đều do người dùng cung cấp và máy đều NHÌN THẤY hết.** Không có tấm ảnh nào "bị giấu" hay "máy phải tưởng tượng ra". Việc của máy ở chế độ B chỉ là **sắp xếp lại đúng thứ tự những tấm nó đã thấy** — chứ không phải đoán ra một màn hình mà nó chưa từng thấy.

### "Bộ định tuyến đầu vào" (input router)
Đây chỉ là một câu lệnh đơn giản: **đếm số ảnh.** Nếu có 1 ảnh → chạy chế độ A. Nếu có từ 2 ảnh trở lên → chạy chế độ B (bật thêm bước sắp xếp). Cùng một hệ thống, chỉ rẽ nhánh theo số ảnh.

---

## PHẦN 4 — Câu chuyện đằng sau hai chế độ (vì sao lại đổi)

Phần này giúp bạn hiểu **lịch sử** để khỏi bối rối khi đọc các file cũ.

- **Lúc đầu (scope cũ — đã BỎ):** thầy hướng dẫn yêu cầu bài toán khó hơn: người dùng chỉ đưa **1 ảnh**, rồi máy phải **đoán ra các màn TIẾP THEO mà nó CHƯA từng thấy**. (Giống như nhìn màn đăng nhập rồi tự tưởng tượng màn kế tiếp trông thế nào.) Cách này rất khó và không có đáp án để chấm.

- **Bây giờ (scope mới — đã CHỐT, thầy đã đồng ý):** đổi thành: người dùng đưa **đủ N ảnh thật** (chỉ bị xáo trộn), máy **sắp xếp lại đúng thứ tự**. 

> ⚠️ Vì lý do lịch sử này, trong vài file cũ còn sót những cụm như *"đoán màn chưa thấy"*, *"blind-horizon"* (tạm dịch: "đoán mù phần phía trước"). **Đó là tàn dư của scope cũ và sẽ được dọn sạch.** Ở scope hiện tại, nhắc lại lần nữa: **không có màn nào chưa thấy cả.**

---

## PHẦN 5 — Hai "nhánh đánh giá": cách chấm điểm cho từng chế độ

Vì có hai chế độ (một ảnh / nhiều ảnh), nên cách **đánh giá chất lượng** cũng chia làm hai nhánh. Trong các file, hai nhánh này được gọi tắt là **DG1** và **DG2** (DG = "Đóng Góp"). Ta giải thích từng nhánh thật kỹ.

### NHÁNH 1 — Gọi là DG1: chấm hướng dẫn cho MỘT ảnh

Đây là nhánh cho chế độ A (một ảnh). Vì không có đáp án mẫu, ta chấm bài hướng dẫn theo **3 tiêu chí**, mỗi tiêu chí kiểm một khía cạnh:

**Tiêu chí 1 — "Grounding" (tạm dịch: bám đúng thực tế trên màn):**
Kiểm xem khi máy bảo *"bấm nút Tra cứu"*, thì nút "Tra cứu" có **thật sự tồn tại** ở đúng vị trí đó trên ảnh không.
- Để làm được, ta cần biết **vị trí thật** của từng nút trên ảnh. Thông tin này đến từ một thứ gọi là **view-hierarchy** (xem giải thích ở Phần 6) — nó cho ta biết "nút Tra cứu nằm trong khung chữ nhật từ tọa độ (x1,y1) đến (x2,y2)".
- Cách chấm: máy nói bấm vào điểm có tọa độ [x, y]; ta kiểm điểm đó **có nằm trong khung chữ nhật** của nút Tra cứu không. Nằm trong = đúng. Cách kiểm này gọi là **"point-in-bbox"** (điểm-nằm-trong-khung; "bbox" = bounding box = khung chữ nhật bao quanh một nút).

**Tiêu chí 2 — "Hallucination" (tạm dịch: bịa đặt):**
Kiểm xem máy có **bịa ra nút không hề tồn tại** không. Ví dụ máy bảo *"bấm nút Thanh toán nhanh"* nhưng trên màn chẳng có nút nào tên vậy → đó là "bịa". Ta đếm tỉ lệ bước bị bịa; càng ít càng tốt.

**Tiêu chí 3 — "Clarity & Format" (rõ ràng & đúng định dạng):**
Kiểm bài hướng dẫn có **viết rõ ràng, đúng kiểu hướng dẫn** không: có đánh số 1, 2, 3 không; mỗi bước có **động từ hành động** (Bấm, Nhập, Chọn...) không; có lan man không.

Gộp lại: **DG1 = chấm một bài hướng dẫn (cho 1 ảnh) trên 3 mặt: bám đúng màn (grounding), không bịa (hallucination), viết rõ (clarity) — mà không cần đáp án mẫu.**

### NHÁNH 2 — Gọi là DG2: chấm khả năng SẮP XẾP THỨ TỰ (cho nhiều ảnh)

Đây là nhánh cho chế độ B (nhiều ảnh xáo trộn). Câu hỏi đánh giá ở đây là:

> **"Máy có sắp lại đúng thứ tự các màn không?"**

Để chấm được cái này, ta cần **biết thứ tự đúng**. May mắn là có loại dữ liệu sẵn (xem Phần 7, bộ AndroidControl) trong đó mỗi quy trình **đã có sẵn thứ tự thật do người ghi lại**. Thứ tự thật này gọi là **"gold trajectory"** (tạm dịch: "lộ trình vàng" — chuỗi thao tác đúng có sẵn). Ta xáo trộn các màn, bắt máy sắp lại, rồi so với "lộ trình vàng" để chấm.

**Cách đo điểm sắp xếp — gọi là "Kendall tau-b" (đọc: ken-đôl tau-bê):**
Đây chỉ là một **công thức đo độ giống nhau giữa hai thứ tự**. Hình dung đơn giản:
- Lấy từng **cặp màn** (màn A, màn B). Hỏi: trong thứ tự máy sắp, A có đứng trước B giống như trong thứ tự đúng không?
- Nếu phần lớn các cặp đều đúng chiều → điểm cao (gần +1). Nếu lộn ngược nhiều → điểm thấp (gần −1).
- Con số này (từ −1 đến +1) là **"điểm sắp xếp"**, và là **chỉ số quan trọng nhất** (gọi là "headline" — chỉ số đầu bảng) của nhánh DG2.

**Một tinh tế quan trọng — "chấm theo thứ tự bộ phận" (partial-order):**
Không phải cặp màn nào sai thứ tự cũng là lỗi! Có hai loại cặp:
- **Cặp BẮT BUỘC:** đảo là sai thật. Ví dụ: *phải đăng nhập trước rồi mới xem được kết quả* — đảo lại là vô lý.
- **Cặp TỰ DO:** đảo vẫn đúng. Ví dụ: màn *"điền email"* và màn *"điền số điện thoại"* — điền cái nào trước cũng được, không ảnh hưởng.

→ Vậy khi chấm, ta **chỉ phạt khi máy sắp sai cặp BẮT BUỘC**; còn cặp TỰ DO thì đảo kiểu nào cũng tính đúng. Đây chính là điều bạn từng nhấn mạnh: *"điền mail hay điền số điện thoại trước cũng được thì vẫn chấm đúng."*

> **Làm sao biết cặp nào là "bắt buộc"?** Ta suy ra từ "lộ trình vàng" bằng một **quy tắc máy móc, cố định**: nếu màn B **chỉ xuất hiện sau khi đã làm xong thao tác đúng ở màn A**, thì (A trước B) là **bắt buộc**. Quan trọng: ta suy từ **lộ trình vàng có sẵn**, **KHÔNG** suy từ việc máy "tự nhận xét". Lý do: nếu để máy vừa làm vừa tự chấm mình thì thành **lý luận vòng tròn** (tự khen mình đúng) — phải tránh.

Sau khi sắp xong, mỗi màn lại được chấm chất lượng hướng dẫn **giống hệt 3 tiêu chí của DG1** (bám đúng, không bịa, rõ ràng).

---

## PHẦN 6 — "View-hierarchy" và "bbox": vì sao chấm grounding được

Phần này giải thích thứ làm cho việc chấm "bám đúng màn" khả thi.

Khi một app hiển thị màn hình, hệ điều hành điện thoại biết **chính xác** trên màn có những thành phần gì và **nằm ở đâu**. Bảng liệt kê này gọi là **view-hierarchy** (tạm dịch: "cây giao diện" — danh sách có cấu trúc các thành phần trên màn). Mỗi thành phần (nút, ô chữ...) có:
- **tên/nhãn chữ** (ví dụ: "Tra cứu"),
- **khung chữ nhật bao quanh nó** = **bbox** = 4 con số chỉ vị trí (trái, trên, phải, dưới) tính bằng **pixel** (điểm ảnh).

Nhờ có view-hierarchy + bbox, ta mới chấm được grounding: máy bảo bấm điểm [x, y], ta tra xem điểm đó rơi vào khung của nút nào, có khớp nút máy nói không.

> **Một quy ước rất quan trọng để tránh gian lận:** view-hierarchy **CHỈ dùng lúc CHẤM ĐIỂM**, **KHÔNG đưa cho máy lúc nó đang viết hướng dẫn.** Vì nếu đưa, máy chỉ việc chép lại danh sách có sẵn → không còn là "nhìn ảnh mà hiểu" nữa (gọi là **rò rỉ dữ liệu** — data leakage). Lúc viết, máy phải tự nhìn ảnh để nhận ra các nút (bằng công cụ ở Phần 8).

> **"Silver" nghĩa là gì?** View-hierarchy do máy/hệ điều hành sinh ra tự động, **đủ tin nhưng không hoàn hảo** (đôi khi thiếu hoặc sai nhãn). Loại nhãn "đủ tốt nhưng không phải vàng do người kiểm" được gọi là **"silver" (bạc)**. Nên khi nói "neo bằng VH-silver" tức là "dựa vào view-hierarchy tự động làm mốc chấm, biết rằng nó chỉ ở mức bạc chứ không phải vàng".

---

## PHẦN 7 — Dữ liệu (dataset): lấy ảnh và thứ tự đúng ở đâu?

**Dataset** = một bộ dữ liệu lớn đã thu thập sẵn để nghiên cứu. Luận văn dùng vài bộ, mỗi bộ một vai trò. Trước hết, một phân biệt quan trọng về **độ tin cậy nguồn**:

- **"Peer-reviewed" (đã bình duyệt):** công trình đã được các nhà khoa học khác trong ngành kiểm tra và chấp nhận đăng ở hội nghị/tạp chí uy tín → **đáng tin, được trích làm nền tảng.**
- **"Preprint" (bản thảo chưa bình duyệt):** bài tự đăng lên mạng (thường ở kho arXiv) **chưa qua kiểm duyệt** → chỉ nên dùng làm **công cụ kỹ thuật**, KHÔNG trình bày như thể đã được công nhận.

Luận văn theo nguyên tắc: **xương sống phương pháp chỉ dựa vào nguồn đã bình duyệt; nguồn preprint chỉ làm công cụ.**

Các bộ dữ liệu và vai trò:

- **MobileViews** — *(là preprint, dùng làm công cụ)*: kho ảnh giao diện điện thoại + view-hierarchy + bbox. **Vai trò:** cung cấp ảnh cho **chế độ một ảnh (DG1)**.

- **AndroidControl** — *(đã bình duyệt, hội nghị NeurIPS 2024)*: kho các **quy trình nhiều bước** trên điện thoại, mỗi quy trình có sẵn **thứ tự đúng (lộ trình vàng)**. **Vai trò:** dùng cho **chế độ nhiều ảnh (DG2)** — ta xáo trộn rồi bắt máy sắp lại, lấy lộ trình vàng để chấm. *Đây là bộ quan trọng nhất cho nhánh sắp xếp.*

- **ScreenSpot / ScreenSpot-v2** — *(đã bình duyệt)*: bộ chuyên để **đối chứng grounding** (kiểm riêng khả năng "điểm-nằm-trong-khung" có chính xác không).

- **AITW** — *(đã bình duyệt)*: nguồn gốc của một **con số ngưỡng kỹ thuật (14%)** dùng khi chấm. (14% là mức sai số cho phép về vị trí; chi tiết không cần nhớ.)

- **Mind2Web** — bộ về **web** (không phải điện thoại). **Để dành cho tương lai (future-work)**, chưa làm trong luận văn này.

---

## PHẦN 8 — Hệ thống đề xuất: "ReOrder-Tutor" hoạt động ra sao

Đây là **cỗ máy** thực sự sinh ra hướng dẫn. Tên gọi **ReOrder-Tutor** ghép từ "Re-Order" (sắp-lại-thứ-tự) + "Tutor" (người hướng dẫn). **Cập nhật 2026-06-25:** hệ thống này là **một đóng góp THỰC SỰ, phải ra kết quả TỐT** (ngang hàng với đóng góp đánh giá) — cụ thể **giảm bịa & tăng đúng-chỗ** so với để model viết tự do, và so cả **GPT-4o**. Nó **vẫn không phá kỷ lục bảng xếp hạng** (không "claim SOTA" — setup khác), nhưng **không còn chỉ là "công cụ để chấm"**.

Nó chạy theo các bước. Ở chế độ nhiều ảnh, có thêm **"Bước 0 — sắp xếp"** đặt trước; ở chế độ một ảnh, bỏ qua bước 0.

### Bước 0 (chỉ khi nhiều ảnh) — Sắp xếp thứ tự các màn
Làm sao máy sắp được? Cách chính gọi là **"pairwise" (so từng cặp)**:
- Đưa từng **cặp** màn cho VLM và hỏi: *"màn nào diễn ra trước?"*
- Hỏi hết mọi cặp, rồi **tổng hợp** lại thành một thứ tự chung. Cách tổng hợp dùng **"Copeland score"** — chỉ là cách đếm: màn nào "thắng" (được cho là đứng trước) nhiều cặp nhất thì xếp lên đầu.
- *Chi phí:* nếu có N màn thì số cặp phải hỏi là N×(N−1)/2. Ví dụ 8 màn = 28 lần hỏi. Càng nhiều màn càng tốn → nên giới hạn N không quá lớn.
- Có một cách thay thế gọi là **"listwise"** (đưa cả danh sách, bắt máy trả luôn thứ tự trong một lần hỏi) — dùng để **đối chứng** xem cách nào tốt hơn.

**Máy dựa vào ĐÂU trên màn để biết thứ tự?** Đây đúng là câu hỏi cốt lõi. Luận văn đặt tên **5 loại "manh mối thứ tự" (ordering cues)**:
1. **Gating (cổng chặn):** màn yêu cầu đăng nhập/cấp quyền thường đứng trước.
2. **Nav-affordance (gợi ý điều hướng):** có nút Next/Back/breadcrumb cho biết trước-sau.
3. **State-delta (thay đổi trạng thái):** ô trống → ô đã điền; nút gạt tắt → bật; con số nhỏ trên icon (badge) 0 → 1. Màn "đã điền" hợp lý đứng sau màn "còn trống".
4. **Title-progression (tiêu đề tiến triển):** tiêu đề thay đổi theo bước (Bước 1/3, Bước 2/3...).
5. **Drill-down (đi sâu vào chi tiết):** màn sau là chi tiết của mục được chọn ở màn trước.

### Các bước sinh hướng dẫn (cả hai chế độ)
Sau khi đã có thứ tự (hoặc chỉ có 1 màn), với **từng màn**:
1. **Nhận diện các thành phần trên ảnh:** dùng công cụ tên **OmniParser** *(là preprint — chỉ công cụ)* để dò ra các nút và **đánh số** chúng.
2. **Đánh dấu lên ảnh (Set-of-Mark):** vẽ các số vừa dò lên chính tấm ảnh, để VLM "nhìn thấy" và tham chiếu theo số.
3. **Sinh hướng dẫn có RÀNG BUỘC:** bắt máy **chỉ được nhắc tới các số/nút đã dò ra** — không cho phép nói tới nút không có số → chống bịa đặt ngay từ lúc viết.
4. **Bộ kiểm tra (verifier):** kiểm lại bài viết. Có 3 kiểu kiểm: V1 = mã máy kiểm "nút này có thật trong danh sách đã dò không"; V2 = một AI khác soi lại; V3 = chính máy tự đọc lại sửa.
5. **Quy về vị trí để chấm:** đổi "số nút" thành tọa độ/khung để chấm grounding.

---

## PHẦN 9 — Đã làm gì gần đây: "rà soát lại toàn bộ" (rescope)

Vì vừa đổi từ scope cũ sang scope mới, ta lo: liệu các lựa chọn dataset/cách-chấm/hệ-thống (vốn chọn cho scope cũ) **còn hợp** với scope mới không? Nên đã chạy một đợt **nghiên cứu kiểm tra lại bằng nhiều AI** (gọi là "rescope"), có tra cứu internet để kiểm từng nguồn trích dẫn là thật và đúng loại (bình duyệt hay preprint).

### Kết quả lớn nhất — **rất tích cực:**
> **Nền tảng VỮNG, không phải thay cái gì lớn.** Hơn nữa, nhiều lựa chọn cũ thật ra **HỢP HƠN** với scope mới.

Vì sao hợp hơn? Ở scope cũ (đoán màn chưa thấy), có những màn máy phải tưởng tượng → **không chấm bám-đúng được** (vì không có ảnh thật). Ở scope mới, **mọi màn đều là ảnh thật** → chấm được đầy đủ trên toàn bộ chuỗi; và điểm sắp-xếp (Kendall) giờ mới thật sự có ý nghĩa.

### Một đợt kiểm tra đối kháng (debate) tiếp theo
Sau đó, cho **4 nhóm AI "đóng vai phản biện"** (mỗi nhóm cố tìm điểm yếu): góc phương pháp, góc người thầy, góc khoa học, góc khả thi. Đồng thời **rà từng file** xem đã đồng bộ scope mới chưa.

**Kết luận:** *"phù hợp, nhưng cần sửa vài chỗ trước khi trình thầy"*. Nền tảng ổn, song còn một số lỗi câu chữ và vài lỗ hổng cần bịt. (Chi tiết ở hai mục dưới.)

---

## PHẦN 10 — Những chỗ cần sửa (giải thích bằng lời thường)

Chia theo mức ưu tiên. **P0 = phải sửa trước khi trình thầy. P1 = nên sửa. P2 = sửa nhỏ về câu chữ.**

### Nhóm P0 (quan trọng nhất)

**P0-1 — Sửa một câu tự mâu thuẫn về "cặp bắt buộc".**
Có một dòng (trong file tổng quan) lỡ viết rằng cặp bắt buộc được xác định bằng "phát hiện manh mối" — điều này **phá vỡ** nguyên tắc chống lý-luận-vòng-tròn (đã nói ở Phần 5). Phải sửa lại cho đúng: cặp bắt buộc suy từ **lộ trình vàng**, không phải từ việc máy tự phát hiện manh mối.

**P0-2 — Sửa nhãn một nguồn (OS-Atlas).**
Một nguồn tên **OS-Atlas** đang bị ghi nhầm là "preprint" (chưa bình duyệt), nhưng thực ra nó **đã được bình duyệt** (hội nghị ICLR 2025). Sửa lại sẽ làm hồ sơ **mạnh hơn**, không yếu đi. (Đây là sửa cho đúng sự thật.)

**P0-3 — Nói cho chính xác về "câu hỏi của thầy".**
Đây là chỗ liên quan thắc mắc của bạn. Vài file lỡ viết kiểu *"hệ thống trả lời THẲNG câu hỏi của thầy"*. Vì câu hỏi **gốc** của thầy (scope cũ) là về "đoán màn chưa thấy", câu này nghe như mình nhận đã giải cái khó hơn. **Cách sửa rất nhẹ — chỉ đổi câu chữ cho đúng**, ví dụ:
- ❌ "trả lời thẳng câu hỏi của thầy về việc model biết trật tự"
- ✅ "đo khả năng model **sắp đúng thứ tự các màn được cung cấp** (tất cả đều thấy) — đúng bài toán đã chốt với thầy"

→ **Không phải đi làm thêm gì khó hơn**, chỉ phát biểu đúng bài toán đang giải. (Bạn đã xác nhận: không có màn nào chưa thấy — nên đây thuần là chuyện câu chữ.)

**P0-4 — Thêm một "cổng kiểm tra" cho nhánh sắp xếp (GOAL-ONLY).**
Lo ngại: câu hỏi mục tiêu đôi khi đã tiết lộ sẵn thứ tự (ví dụ mục tiêu ghi "mở app → bấm → kéo xuống" thì đọc xong là biết thứ tự, **không cần nhìn ảnh**). Nếu vậy, nhánh sắp xếp **không thật sự đo "hiểu màn"** mà chỉ đo "đọc mục tiêu". 
→ Cách bịt: chạy thử một phép kiểm tên **GOAL-ONLY** (chỉ đưa mục tiêu, **giấu hết ảnh**) xem máy có sắp đúng không. Nếu chỉ-mục-tiêu đã sắp đúng cao → phải lọc bỏ những trường hợp đó, chỉ giữ những ca mà **bắt buộc phải nhìn ảnh** mới sắp được. Như vậy điểm số mới phản ánh đúng "máy hiểu màn".

**P0-5 — Bổ sung một trích dẫn nền cho điểm sắp-xếp (Lapata 2006).**
Hiện cách chấm thứ tự (Kendall) chưa có một nguồn bình duyệt nói rõ "dùng cách này để chấm bài sắp-thứ-tự là chuẩn". Có sẵn một bài kinh điển (**Lapata, 2006**, tạp chí uy tín) làm đúng việc đó → bổ sung vào để vững về mặt học thuật.

### Nhóm P1 (nên sửa) — tóm gọn
- Cho bước sắp xếp **đọc thẳng ảnh** thay vì đọc qua danh sách-đã-dò (tránh phụ thuộc vào công cụ dò có thể bỏ sót).
- Cam kết một **mức tối thiểu** cho nhánh nhiều-ảnh để nó không bị co lại quá nhỏ.
- Sửa lại vài câu **ghi nhầm nguồn** (ví dụ: một bài tên Sort-Story dùng công thức khác, không phải Kendall; một bài tên RankGPT là *phương pháp* chứ không phải *cách chấm*).
- Ghi rõ cách chấm "thứ tự bộ phận" là **biến thể tự đề xuất của luận văn**, không vờ là chuẩn có sẵn.

### Nhóm P2 (sửa nhỏ, câu chữ)
Dọn các cụm tàn dư scope cũ ("đoán mù", "màn chưa thấy"); sửa vài dòng tóm tắt đầu file còn ghi "1 ảnh" thành "1 hoặc N ảnh"; thêm vài trích dẫn cho đủ; ghi chú ở file lịch sử rằng nó viết trước khi đổi scope.

---

## PHẦN 11 — Hai quyết định đang chờ bạn (giải thích kỹ)

### Quyết định 1 — Cách xử lý "câu chữ về câu hỏi của thầy" (chính là P0-3)
Bạn đã làm rõ: **không có ảnh nào chưa thấy**, máy thấy hết. Vậy nên tôi đề xuất cách **nhẹ nhất**: chỉ **sửa lại vài câu cho chính xác** (như ví dụ ✅ ở P0-3), giữ nguyên scope, **không thêm việc gì**. Phần "đoán màn chưa thấy" để **một dòng "hướng phát triển tương lai"** cho ai muốn nghiên cứu tiếp.
→ *Việc bạn cần làm:* xác nhận "đồng ý sửa câu chữ cho chính xác" là đủ.

### Quyết định 2 — "Cắt bớt khối lượng" (giải thích thật chậm)

**Bối cảnh:** đợt rà soát **gợi ý thêm** nhiều thứ (thêm bộ dữ liệu phụ, thêm cách chấm, thêm phép thử). Nếu làm **HẾT**, khối lượng bằng **3–4 bài báo** → một học viên không kham nổi, và nếu cố làm thì mỗi phần bị **chia mỏng, thiếu dữ liệu, kết quả không đáng tin.**

**Nên phải xếp mọi thứ vào 2 rổ:**
- **Rổ LÕI (bắt buộc làm kỹ):** phần chính của luận văn, kết quả dựa vào đây.
- **Rổ ĐỂ SAU (làm nếu dư sức / hoặc chỉ ghi là hướng tương lai):** thiếu cũng **không sập** luận văn.

Dưới đây là từng món và đề xuất xếp rổ — mỗi món kèm "nó là gì" bằng lời thường:

| Món | Nó là gì (lời thường) | Đề xuất xếp rổ |
|---|---|---|
| **AndroidControl** | Bộ dữ liệu nhiều-bước chính, có thứ tự đúng | **LÕI** (xương sống nhánh sắp xếp) |
| **GOAL-ONLY** | Phép thử: giấu ảnh, chỉ đưa mục tiêu, xem có gian lận không | **LÕI** (cổng kiểm quan trọng) |
| **VISUAL-ONLY** | Phép thử đối xứng: giấu mục tiêu, chỉ đưa ảnh, xem ảnh một mình có đủ không | **LÕI** (cặp đôi với GOAL-ONLY) |
| **Lapata 2006** | Một trích dẫn nền cho cách chấm thứ tự | **LÕI** (chỉ là thêm 1 câu trích) |
| **GUI-Odyssey** | Bộ dữ liệu phụ, chuỗi dài hơn, để kiểm độ bền khi nhiều màn | Để sau (hoặc thêm nếu chọn mức "Vừa") |
| **AMEX** | Bộ dữ liệu nhỏ, đối chứng thêm về vị trí nút | Để sau |
| **Setwise** | Một cách sắp xếp thứ ba (ngoài pairwise & listwise) | Để sau (đối chứng phụ) |
| **CLIPScore** | Một cách chấm phụ đo khớp ảnh-chữ, nhưng **yếu** ở chi tiết nhỏ | Bỏ, hoặc chỉ thử thăm dò |
| **Tiếng Trung (ZH)** | Chạy số liệu song song cả tiếng Anh và tiếng Trung | Tiếng Anh là chính; tiếng Trung chỉ kiểm tra nhanh |
| **Độ dài chuỗi tối đa (N)** | Chuỗi dài nhất trong đường biểu diễn chính | ≤6 (gọn) hoặc ≤8 (vừa) |

**Ba mức để bạn chọn:**
- **Mức GỌN:** rổ lõi đúng như bảng trên (AndroidControl + GOAL-ONLY + VISUAL-ONLY + Lapata + cơ chế nhớ-ngữ-cảnh), chuỗi ≤6, tiếng Trung chỉ kiểm nhanh. Mọi món còn lại để sau. → *nhẹ nhất, an toàn nhất.*
- **Mức VỪA (tôi khuyến nghị):** như GỌN nhưng **thêm bộ GUI-Odyssey** để kiểm độ bền khi nhiều màn, chuỗi ≤8. → *đủ mạnh mà vẫn kiểm soát được khối lượng.*
- **Mức RỘNG:** giữ thêm cả AMEX và Setwise. → *đầy đủ nhất nhưng dễ quá tải.*

→ *Việc bạn cần làm:* chọn một trong ba mức (Gọn / Vừa / Rộng).

---

## PHẦN 12 — Đóng góp của luận văn (tóm tắt)

- **HAI đóng góp NGANG NHAU (cập nhật 2026-06-25):**
  - **A — Hệ thống ReOrder-Tutor sinh tutorial TỐT:** phải ra kết quả tốt — giảm bịa, đúng-chỗ hơn, rõ hơn so với baseline viết-tự-do và so **GPT-4o** (thắng GPT-4o toàn diện = bonus). KHÔNG claim SOTA leaderboard (setup khác).
  - **B — Cách ĐÁNH GIÁ đáng tin khi không có đáp án mẫu**, gồm hai nhánh: **DG1** (chấm hướng dẫn 1 ảnh: bám đúng + không bịa + rõ) và **DG2** (chấm sắp đúng thứ tự nhiều ảnh: Kendall, cặp bắt buộc).
- **Nguyên tắc "null vẫn đậu":** áp cho **nhánh B (đánh giá)** + phần **"đo cơ chế nào trả công"** của A — kể cả "không khác biệt" vẫn có giá trị nếu **đăng ký trước** + **đủ dữ liệu** (giữ một phần lưới an toàn). Riêng **claim mức-chắc-thắng của A** (giảm bịa/đúng-chỗ vs baseline) thì **kỳ vọng kết quả dương**.
- **Tiếng Việt:** số liệu định lượng chạy trên tiếng Anh (và một ít tiếng Trung); tiếng Việt dùng để **demo minh họa** và kiểm tra nhanh, **không có bảng số tiếng Việt** (vì thiếu dữ liệu chuẩn tiếng Việt).

---

## PHẦN 13 — Tóm tắt một đoạn (nếu chỉ đọc 10 dòng)

Luận văn xây hệ thống AI **nhìn ảnh giao diện + đọc câu hỏi → viết hướng dẫn từng bước**. Người dùng có thể đưa **một ảnh** (máy chỉ đường ngay) hoặc **nhiều ảnh bị xáo trộn của một quy trình** (máy **tự sắp lại đúng thứ tự** rồi mới viết — và **mọi ảnh máy đều thấy**, không phải đoán màn nào). Khó khăn lớn nhất: **không có đáp án mẫu** để chấm. Nên đóng góp chính là **một cách đánh giá đáng tin** gồm hai nhánh: chấm hướng dẫn-một-ảnh (bám đúng màn, không bịa, rõ ràng) và chấm khả năng-sắp-thứ-tự (đo bằng điểm Kendall, chỉ phạt khi sai cặp bắt buộc). Đợt rà soát lại gần đây kết luận **nền tảng vững, chỉ cần sửa vài câu chữ và bịt vài lỗ hổng**. Hiện chỉ còn **2 việc chờ bạn quyết**: (1) đồng ý sửa câu chữ cho chính xác về "câu hỏi của thầy", và (2) chọn mức cắt khối lượng (Gọn / Vừa / Rộng).

---

*File này là bản giải thích dễ hiểu. Khi cần chi tiết kỹ thuật + trích dẫn nguồn, xem: `09_rescope_research.md` (kết quả rà soát) và `10_audit_rescope.md` (danh sách lỗi cần sửa). Khi mâu thuẫn giữa các file, `05_final_plan.md` là bản gốc-sự-thật.*
