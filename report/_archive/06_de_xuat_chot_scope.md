# ĐỀ XUẤT CHỐT PHẠM VI LUẬN VĂN (bản trình thầy)

> Một trang tổng hợp, dễ đọc, **giải thích mọi thuật ngữ ngay khi dùng**, để chốt phạm vi với thầy.
> Chi tiết kỹ thuật: `01`–`05`; cách làm pipeline dễ hiểu: `03b`.

---

## TÓM TẮT 30 GIÂY

> *Đọc 30 giây hiểu toàn bộ luận văn. Các mục sau chỉ là giải thích kỹ hơn cho từng ý ở đây.*

- **Đề tài:** đưa vào **ảnh chụp màn hình + 1 câu hỏi**, máy tự viết ra **hướng dẫn từng bước** cho người đọc. Hệ có **bộ chọn đầu vào (input router):** **1 ảnh** → đơn bước; **N ảnh** → đa bước (giải thích ngay dưới).
  - *Ví dụ minh hoạ tự soạn — không phải record thật của dataset:* ảnh app eTax + câu hỏi *"kiểm tra đã nộp thuế chưa vào đâu?"* → máy trả *"1. Bấm 'Tra cứu nghĩa vụ thuế'…"*.
- **Cái khó:** (1) không có "tutorial mẫu" để so điểm; (2) máy hay **bịa nút không có thật**; (3) phải chạy được trên app bất kỳ.
- **Đóng góp chính = cách ĐÁNH GIÁ chất lượng khi không có đáp án mẫu** (kèm pipeline chống bịa). Hai đóng góp:
  - **DG1** — *đơn bước* (làm xong ngay trên màn đang thấy): cách chấm **không cần tutorial mẫu của người**, lấy "cây cấu trúc giao diện" (VH) làm thước đo.
  - **DG2** — *suy luận trật tự màn* (đa bước): đưa vào **N ảnh ĐÃ XÁO TRỘN** của một luồng đa bước + mục tiêu → máy phải (1) **tự suy ra thứ tự đúng** của các màn, (2) sinh hướng dẫn từng bước theo thứ tự đó. Chấm trên bộ **AndroidControl** *có sẵn chuỗi thao tác đúng*. Đây là **bài toán đặt ra ĐỂ ĐO khả năng model SẮP ĐÚNG THỨ TỰ các màn ĐƯỢC CUNG CẤP** (mọi màn đều do người dùng đưa và model đều thấy — không có màn nào "chưa thấy") — *đúng bài toán đã chốt với thầy: "làm sao model biết trật tự?"*.
- **Dữ liệu:** MobileViews (màn-0) + AndroidControl (đa bước) + ScreenSpot (đối chứng grounding).
- **Khả thi:** linh kiện có sẵn, không cần huấn luyện, 1 GPU + ~$300. **Việc tuần 1:** đo tỷ lệ máy dò trúng nút (rủi ro lớn nhất) + tự đếm độ dài episode AndroidControl.
- **Tiếng Việt / world-model tự huấn luyện / nhánh web** → để **hướng phát triển** (khách quan không có thước đo để chấm).

---

## 0. SƠ ĐỒ BỘ CHỌN ĐẦU VÀO (input router) — MỘT hệ duy nhất, hai chế độ

> *Người dùng luôn nạp ảnh + câu hỏi. Số ảnh quyết định chế độ — không phải hai hệ riêng.*

```
ẢNH (1 hoặc N) + CÂU HỎI
        │
        ├── N = 1  → CHẾ ĐỘ ĐƠN BƯỚC (DG1)
        │             • làm xong ngay trên màn đang thấy (MobileViews màn-0)
        │             • chấm: chỉ-đúng-chỗ + tỷ-lệ-bịa + định dạng (không cần tutorial mẫu)
        │
        └── N ≥ 2  → CHẾ ĐỘ SUY LUẬN TRẬT TỰ MÀN (DG2)
                      • N ảnh ĐÃ XÁO TRỘN của 1 luồng đa bước + mục tiêu
                      • Stage 0 "Screen-Ordering": máy TỰ XẾP lại đúng thứ tự
                      • rồi chạy pipeline 5 bước trên từng màn theo thứ tự đó
                      • chấm trật tự (Kendall τ-b) + chất lượng tutorial mỗi màn
```

- **N = 1 chính là Stage-0 rỗng** → quay về đúng pipeline cũ (DG1 nguyên vẹn).
- **Trung thực với thầy:** chế độ N-ảnh là **bài toán đặt ra ĐỂ ĐO** khả năng model **sắp đúng thứ tự các màn ĐƯỢC CUNG CẤP** (mọi màn đều thấy, không có màn nào "chưa thấy"), **không** khẳng định "người dùng thường nạp N ảnh" là nhu cầu deploy phổ biến. *(Phần "đoán màn CHƯA thấy" chỉ là một dòng hướng phát triển — AGENT-NSI — không phải nghĩa vụ luận văn.)*

---

## 1. Đề tài trong một câu + ví dụ

**Xây và ĐÁNH GIÁ một hệ thống dùng AI đa phương thức để tự sinh *hướng dẫn sử dụng phần mềm từng bước*, từ ảnh chụp màn hình + một câu hỏi của người dùng.**

> *Ví dụ minh hoạ tự soạn — không phải record thật của dataset:* đưa vào **ảnh màn hình app eTax** + câu hỏi *"Tôi muốn kiểm tra đã nộp thuế chưa thì vào đâu?"*
> → máy trả ra: *"1. Bấm 'Tra cứu nghĩa vụ thuế'. 2. Chọn kỳ tính thuế. 3. Xem trạng thái."*
>
> **Để khỏi hiểu nhầm — record THẬT của dataset là app tiếng Anh, không phải eTax.** Ví dụ một episode của **AndroidControl** là app *"cruisedeals"* (open_app CruiseDeals → click x:313,y:742 → swipe up); một mẫu của **ScreenSpot** là nút *"close"* với ô bao chuẩn-hoá 0–1 = `[0.948, 0.144, 0.994, 0.207]`. **eTax / "Tra cứu nghĩa vụ thuế" chỉ là ví dụ minh hoạ tự soạn để thầy dễ hình dung**, mọi con số chấm điểm về sau đều chạy trên record thật (Anh/Trung) như trên.

- **Đa phương thức (multimodal):** đầu vào gồm *cả ảnh lẫn chữ*. AI ở đây là **VLM** = *Vision-Language Model*, model vừa "nhìn" được ảnh vừa viết được chữ (ví dụ GPT-4o, Qwen2.5-VL).

> **HAI VÍ DỤ DÙNG XUYÊN SUỐT** *(cả hai đều là ví dụ minh hoạ tự soạn — không phải record thật của dataset; dùng để thầy dễ theo dõi xuyên suốt báo cáo)*:
>
> **EX-A — đơn bước (app eTax):** ảnh màn hình eTax + câu hỏi *"kiểm tra đã nộp thuế chưa thì vào đâu?"*.
> Việc làm xong **ngay trên màn hình đang thấy**, không cần mở màn khác → máy trả: *"1. Bấm 'Tra cứu nghĩa vụ thuế'…"*.
> Chống bịa: máy **chỉ được chỉ vào nút đã dò thấy** trên ảnh; **không được** tự bịa thêm nút như *"vào Cài đặt"* nếu trên ảnh không có nút đó.
>
> **EX-B — đa bước (app Đồng hồ):** câu hỏi *"đặt báo thức 7:00"* + **3 ảnh ĐÃ XÁO TRỘN** của luồng này.
> Luồng đúng gồm 3 màn: **B1** màn tab *Báo thức* → **B2** màn sau khi bấm *"+"* → **B3** màn đặt giờ *07:00* rồi *OK*. Nhưng máy nhận 3 ảnh **không theo thứ tự** (vd B2, B1, B3) → phải **tự xếp lại đúng B1→B2→B3** rồi mới sinh hướng dẫn từng bước.

## 2. Vì sao đề tài này khó (và vì sao đáng làm)

1. **Không có "đáp án mẫu" để học/để chấm.** Không tồn tại bộ dữ liệu lớn gồm hàng vạn *tutorial chuẩn do người viết* cho mọi app. → Không thể chấm điểm theo kiểu "so với đáp án".
2. **Máy hay "bịa".** VLM thường tự tin bịa ra nút bấm **không tồn tại** trên màn hình → hướng dẫn sai, người dùng làm theo không được.
3. **Phải chạy được trên app bất kỳ**, không chỉ một app huấn luyện sẵn.

→ **Bài toán cốt lõi của luận văn không chỉ là "sinh cho hay", mà là "ĐÁNH GIÁ được chất lượng khi không có đáp án mẫu".** Đây chính là chỗ luận văn đóng góp.

---

## 3. Đóng góp của luận văn (định vị để bảo vệ chắc)

> **NHẤN MẠNH (quan trọng nhất):** đóng góp **CHÍNH = PHƯƠNG PHÁP ĐÁNH GIÁ (DG1+DG2)** khi không có gold tutorial. Pipeline **ReOrder-Tutor** chỉ là **hệ tham chiếu off-the-shelf để vận hành đánh giá — KHÔNG phải đóng góp chính, KHÔNG claim SOTA**. Độ mới claim ở **TRỤC ĐÁNH GIÁ** (chống vòng-lập-luận + truy-nguồn tín hiệu một-cue + chấm thứ-tự-bộ-phận + audit người); ở **trục sắp-xếp ảnh** thì **thừa nhận prior-art** (Sort-Story EMNLP 2016, Wu ACL 2022, RankGPT EMNLP 2023). Khung đánh giá kế thừa Intrinsic+Extrinsic của **Chim, Ive, Liakata (Computational Linguistics 51(1):191–233, 2025 — tạp chí)**; headline τ-b theo tiền lệ **Lapata (Computational Linguistics 32(4):471–484, 2006)**.

Luận văn có **hai đóng góp song hành**, chia theo một câu hỏi đơn giản: **bộ dữ liệu có sẵn đáp án đúng để chấm hay không?**

### Đóng góp 1 (DG1) — Đánh giá màn-0, KHÔNG có tutorial mẫu của người

Khi câu hỏi **giải quyết được ngay trên màn hình đang thấy** (đơn bước), không tồn tại "tutorial chuẩn do người viết" để so. DG1 gồm hai phần:

> *Đây là tình huống **EX-A (eTax)** — ví dụ minh hoạ tự soạn, không phải record thật của dataset: chỉ cần bấm 1 nút trên màn đang thấy là xong, không phải mở màn khác. Ứng với chế độ N=1 của bộ chọn đầu vào.*

**(A) Một cách đánh giá *không cần tutorial mẫu*.** Thay cho tutorial mẫu, ta dùng **View Hierarchy (VH)** — *"cây cấu trúc giao diện"*: danh sách chính xác mọi nút trên màn hình (tên, loại, **toạ độ ô bao**), có sẵn miễn phí trong bộ **MobileViews**.
- VH đóng vai **thước đo**: máy bảo "bấm nút X ở chỗ này" → ta đối chiếu VH xem nút X có thật và đúng chỗ không.
  - *Như chấm bài trắc nghiệm bằng phiếu đáp án:* VH là "phiếu" liệt kê mọi nút thật + chỗ của nó. Ở **EX-A**, máy nói *"bấm 'Tra cứu nghĩa vụ thuế'"* → ta tra VH thấy nút đó **có thật** và toạ độ máy chỉ **nằm trong ô** của nút → đạt. Nếu máy bịa *"vào Cài đặt"* mà VH không có nút đó → **bắt được lỗi bịa**.
- **VH chỉ dùng lúc CHẤM, không đưa cho máy lúc sinh** (vì app thật ngoài đời không có VH).
- VH là nhãn "bạc" (do máy dò tự động), không phải đáp án "vàng" do người soạn — nên ta gọi cách chấm này là *"không cần tutorial mẫu của người"* chứ không nói suông là "không có gì để chấm".

**(B) Một thí nghiệm có kiểm soát**, trả lời câu hỏi: *cơ chế ép máy chỉ được dùng các nút đã phát hiện trên ảnh có **thực sự** làm máy bớt bịa / chỉ đúng chỗ hơn so với để máy viết tự do không — và nhờ cơ chế con nào?*

> *Ở **EX-A**: thí nghiệm này so "để máy viết tự do" (dễ bịa nút *Cài đặt*) với "ép máy chỉ được chọn trong danh sách nút đã dò" (buộc phải chọn đúng *Tra cứu nghĩa vụ thuế*) — rồi đo xem cách thứ hai có giảm bịa thật không.*

> 💡 **Vì sao framing này an toàn:** đóng góp là *phương pháp đánh giá + một câu hỏi khoa học được trả lời rõ ràng*. **Kể cả khi kết quả cho thấy cơ chế đó không giúp gì**, luận văn vẫn thành công, vì đã *đo được và giải thích được vì sao* (nói rõ ở mục 7).

### Đóng góp 2 (DG2) — Suy luận trật tự màn trên dữ liệu CÓ sẵn đáp án đúng (AndroidControl)

Khi tác vụ cần **bấm → mở màn mới → tiếp tục** (đa bước), ta dùng bộ **AndroidControl (NeurIPS 2024 D&B, đã bình duyệt)** — bộ dữ liệu *có sẵn chuỗi thao tác đúng từng bước* (đáp án vàng). **Cách đặt bài toán (đã chốt):** đưa vào **N ảnh ĐÃ XÁO TRỘN** của một luồng + mục tiêu → máy phải (1) **suy ra thứ tự đúng** của các màn, (2) sinh hướng dẫn từng bước theo thứ tự đó. Vì có đáp án để so thứ tự, đây là đánh giá có-đối-chiếu.

> *Đây là tình huống **EX-B (Đồng hồ — đặt báo thức 7:00)**: nhận 3 ảnh xáo trộn, luồng đúng là B1→B2→B3.*

**Trục chính = đo khả năng model SẮP ĐÚNG THỨ TỰ các màn ĐƯỢC CUNG CẤP** (tất cả các màn đều do người dùng đưa và model đều thấy — không có màn nào "chưa thấy") — *đúng bài toán đã chốt với thầy: "làm sao model biết trật tự?"*. Để đo "cái giá của việc không biết trật tự", ta so **hai chế độ trên cùng dữ liệu**:

- **ORACLE-ORDER (cận trên / skyline):** đưa N ảnh **ĐÃ sắp đúng** + mục tiêu → máy *chỉ phải sinh* hướng dẫn, không phải xếp.
  - *Như thi mà đề đã đánh số câu sẵn đúng thứ tự:* ở **EX-B**, máy nhận B1→B2→B3 đã đúng hàng → chỉ việc viết hướng dẫn.
- **SELF-ORDER (thật):** đưa N ảnh **xáo trộn** → máy **tự xếp** rồi mới sinh.
  - *Như thi mà các câu bị tráo, phải tự đoán câu nào trước:* ở **EX-B**, máy nhận B2,B1,B3 → tự suy ra trật tự rồi sinh.
- **ordering gap = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER)** = **"cái giá của việc không biết trật tự"**.

> **NÓI RÕ ĐỂ KHÔNG HIỂU NHẦM:**
> - **Trục chính là τ-b (đo trật tự)**; ordering gap là **trục phụ** và chỉ có nghĩa nếu metric tutorial *nhạy với thứ tự* (cảnh báo floor-effect — xem test nhạy-thứ-tự ngay dưới).
> - **Sanity cứng (đã nới):** ORACLE-ORDER **≥** SELF-ORDER **− ε** ở *mọi episode* (ε = biên nhiễu nhỏ đã định trước, không phải ≥ tuyệt đối); nếu vi phạm = **bug**, không phải phát hiện.
> - **TEST NHẠY-THỨ-TỰ (chống floor-effect, đăng ký trước):** lấy input *đã sắp đúng*, **đảo 1 cặp BẮT BUỘC**, đo **DELTA** của metric tutorial. Nếu delta < **ngưỡng tối thiểu (pre-register)** ⇒ metric tutorial **không nhạy thứ tự** ⇒ **BỎ ordering gap**, chỉ giữ **τ-b làm headline** (DG2 **KHÔNG sụp** — vì τ-b vẫn đo được trật tự độc lập với metric tutorial).
> - **Loại N ≤ 2** khỏi trục đo trật tự (N=2 chỉ có 1 cặp → τ-b chỉ nhận {−1,+1}, vô nghĩa); trục N thực tế **N ∈ [3, ~10]** (đường-cong headline **N≤6**, ≥30 episode/mốc; báo *thêm* tới ~10 nếu ngân sách cho phép).

> **CHỐNG VÒNG-LẬP-LUẬN (quan trọng):** nhãn "cặp BẮT BUỘC" dùng để chấm τ-b partial-order-aware **KHÔNG** lấy từ bộ phát-hiện cue (gating/drill-down) mà chính model + signal-attribution dùng — nếu lấy thế là **tự chấm** (model vừa đoán vừa tự ra đáp án). Thay vào đó nhãn **suy từ gold trajectory AndroidControl bằng quy tắc tất định**: màn B chỉ xuất hiện *sau khi* thực thi gold action trên màn A ⇒ (A,B) BẮT BUỘC; không có quan hệ đó = TỰ-DO. **Đăng ký trước (pre-register):** (i) tỷ lệ cặp bắt-buộc / tự-do; (ii) **audit người 50–80 cặp** kiểm quy tắc tất định có khớp đánh giá người không (báo % khớp); (iii) đo **độ nhạy của headline khi gán sai nhãn 10%**.
> **Gold trajectory / VH chỉ dùng ở KHÂU CHẤM OFFLINE — KHÔNG phải input của model lúc xếp** (lúc xếp model chỉ đọc ảnh).

> **Làm sao model biết trật tự? — 5 manh mối thứ tự (ordering cues), đặt tên rõ:**
> 1. **gating** — màn bắt buộc làm trước (đăng nhập / cấp quyền trước khi xem kết quả).
> 2. **nav-affordance** — dấu hiệu điều hướng (nút *Next/Back*, breadcrumb).
> 3. **state-delta** — trạng thái biến đổi (toggle off→on, ô trống→đã điền, badge 0→1).
> 4. **title-progression** — tiêu đề tiến theo phiếu (Bước 1/3 → 2/3…).
> 5. **drill-down** — màn sau là chi tiết của một item ở màn trước.
> *Ở EX-B, máy xếp đúng nhờ **drill-down + nav-affordance**: màn đặt giờ là chi tiết mở ra từ nút "+" ở màn danh sách.*

> **Trục tham chiếu chuẩn ngành — Tier A (teacher-forced):** vẫn giữ làm **mốc tham chiếu** (thầy expect, giống các bài GUI-agent). Mỗi bước, bộ chấm **đưa cho máy đúng màn hình thật của đáp án**, máy chỉ phải đoán thao tác kế rồi so với đáp án. Metric: **Action-Type accuracy, Grounding@14%, Step-SR** (mục 4).
> - *Như thi mà mỗi câu được xem lại đề gốc:* ở **EX-B**, trước mỗi bước máy được xem ảnh thật của màn tương ứng → đoán đúng **3/3**.
> - **Tier A KHÔNG còn là "đa bước chính"** (trục ordering mới là chính); ORACLE-ORDER là *skyline* của trục ordering.
> - **Không so ngang bảng xếp hạng** (máy ta dò nút từ ảnh, khác cách làm của leaderboard; recall detector tự đo ở K1) — chỉ "đặt cùng giao thức để tham chiếu định tính".

---

## 4. Giải thích nhanh các thuật ngữ (để thầy & người đọc nắm)

> *Lưu ý: các ví dụ EX-A (eTax) / EX-B (Đồng hồ) trong bảng dưới là **ví dụ minh hoạ tự soạn — không phải record thật của dataset**.*

| Thuật ngữ | Nghĩa đời thường |
|---|---|
| **VLM** | Model AI vừa nhìn ảnh vừa viết chữ (GPT-4o, Qwen2.5-VL). |
| **View Hierarchy (VH)** | "Cây cấu trúc giao diện" — danh sách mọi nút + toạ độ chuẩn của một màn hình. Dùng làm thước đo lúc chấm. |
| **Grounding** | "Chỉ đúng chỗ" — toạ độ máy định bấm có rơi vào đúng ô của nút thật không. *EX-A: toạ độ máy chỉ có nằm trong ô nút 'Tra cứu nghĩa vụ thuế' không.* |
| **Hallucination** | "Bịa" — máy nhắc tới nút/bước **không tồn tại**. *EX-A: máy ghi "vào Cài đặt" trong khi màn eTax không có nút Cài đặt.* |
| **Set-of-Mark** | Mẹo "đánh số" mọi nút trên ảnh để máy chỉ vào số thay vì tự tả. *EX-A: gắn ①②③ lên các nút, máy trả "bấm ①".* |
| **Constrained generation** | "Sinh có ràng buộc" — ép máy **chỉ được** chọn trong danh sách nút đã đánh số. |
| **Ablation (thang bậc)** | Thí nghiệm "thêm từng món, đo từng nấc" để biết món nào thực sự có ích. |
| **Best-Worst Scaling (BWS)** | Cách cho chuyên gia chấm: đưa 4 tutorial, chọn cái *tốt nhất* và *tệ nhất* (đáng tin hơn chấm điểm 1–5). |
| **Suy luận trật tự màn** | Đưa N ảnh **xáo trộn** của 1 luồng + mục tiêu → máy phải xếp lại đúng thứ tự rồi sinh hướng dẫn. Trục đa bước chính của DG2. |
| **Kendall τ-b** | **Metric trật tự HEADLINE** — đo độ giống nhau giữa thứ tự máy xếp và thứ tự đúng (đếm cặp xuôi/ngược, chuẩn cho cặp hoà). Càng gần +1 càng tốt; nguồn: Kendall 1938 + Gao et al. NAACL 2025. |
| **Partial-order-aware (chấm theo thứ-tự-bộ-phận)** | Chỉ **phạt khi sai cặp BẮT BUỘC** (đảo là sai thật); cặp **TỰ-DO** (vd điền Email/SĐT trước-sau đều được) đảo vẫn tính ĐÚNG. *EX: điền Email/SĐT độc lập → đảo vẫn đúng; đăng-nhập-trước-xem-kết-quả → đảo là sai.* **QUAN TRỌNG (chống tự-chấm):** nhãn "bắt buộc" **KHÔNG** lấy từ bộ phát-hiện cue (gating/drill-down) mà model dùng — lấy thế là vòng lặp tự-chấm. Nhãn này **suy từ GOLD TRAJECTORY của AndroidControl bằng quy tắc tất định**: màn B chỉ xuất hiện *sau khi* thực thi gold action trên màn A ⇒ cặp (A,B) là BẮT BUỘC (phụ thuộc nhân quả trong chuỗi vàng); cặp không có quan hệ đó = TỰ-DO. |
| **ordering cues (5 manh mối thứ tự)** | gating · nav-affordance · state-delta · title-progression · drill-down — các dấu hiệu giúp máy biết màn nào trước (xem mục 3). |
| **Signal-attribution** | Phân tích **manh mối nào giúp xếp đúng**: chỉ giữ các cặp phân biệt bởi **đúng một cue**, đo độ chính xác theo từng nhóm cue. KHÔNG che pixel (che pixel tạo artifact giả). **Caveat:** kết luận dựa trên **stratification một-cue**, KHÔNG dựa lời model tự khai (cue model tự trích chỉ là tín hiệu giải thích yếu). |
| **ORACLE-ORDER (skyline)** | Đưa N ảnh **đã sắp đúng** → máy chỉ phải sinh, không phải xếp. Là cận-trên của trục ordering. |
| **SELF-ORDER (thật)** | Đưa N ảnh **xáo trộn** → máy tự xếp rồi sinh. Là chế độ thật. |
| **ordering gap** | Hiệu **chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER)** = "cái giá của việc không biết trật tự". Là **trục phụ**; chỉ có nghĩa nếu metric tutorial nhạy với thứ tự (cảnh báo floor-effect). |
| **Tier A (mốc tham chiếu chuẩn ngành)** | Đo đa bước "có gợi ý": mỗi bước cho máy **thấy màn thật của đáp án** rồi đoán thao tác kế. Trục **tham chiếu**, **không** phải đa bước chính, **không** phải năng lực sản phẩm. |
| **Step-SR (Step Success Rate)** | Tỷ lệ bước đoán đúng cả loại thao tác lẫn chỗ bấm. **CHỈ dùng cho Tier A.** |
| **Action-Type accuracy** | Đoán đúng *loại* thao tác (bấm / nhập chữ / cuộn…), chưa xét chỗ. Càng cao càng tốt. |
| **Grounding@14%** | Điểm máy định bấm có nằm trong **~14% khoảng cách màn** quanh điểm đúng, **HOẶC cùng ô (bounding box)** với điểm đúng không (ngưỡng chuẩn từ AITW). Càng cao càng tốt. |

---

## 5. PHẠM VI ĐỀ NGHỊ CHỐT (phần thuyết phục nhất)

> Nguyên tắc: **chỉ cam kết những gì đo được; phần không đo được → để "hướng phát triển", nói rõ vì sao.**
> Đây không phải né tránh — đây là **bằng chứng đã hiểu sâu giới hạn của bài toán** (điều hội đồng đánh giá cao).

### ✅ TRONG luận văn (cam kết làm + có số liệu)

> Cả **đơn bước** (DG1) **lẫn đa bước** (DG2) đều trong phạm vi. Đa bước **KHÔNG còn là hướng phát triển** — vì ta đã có dữ liệu *có sẵn chuỗi thao tác đúng* (gold trajectory, từ AndroidControl) để chấm.

1. **DG1 — Sinh hướng dẫn trên màn hình đang thấy** (đơn bước / thao tác ngay trên ảnh).
2. Bộ **metric đánh giá không cần tutorial mẫu** cho màn-0 (chỉ-đúng-chỗ, tỷ-lệ-bịa, độ-phủ, định dạng, độ rõ).
3. **Thí nghiệm thang bậc** so hệ "grounding cấu trúc" với baseline VLM tự do.
4. **Pilot chuyên gia nhỏ** để kiểm metric tự động có khớp cảm nhận người không.
5. Dữ liệu: **MobileViews** (mobile, có VH + toạ độ chuẩn, miễn phí) cho DG1.
   - ⚠️ **Lưu ý về "tự soạn câu hỏi":** **CHỈ MobileViews** cần tự soạn câu hỏi (vì bộ này chỉ có ảnh + VH, không kèm câu hỏi); còn **AndroidControl và ScreenSpot đã có sẵn câu hỏi/tác vụ**, không phải soạn. Và "tự soạn câu hỏi" ở đây **chỉ là viết phần INPUT (câu hỏi) cho ảnh có sẵn** — *đáp án để chấm vẫn là dữ liệu thật (VH của chính ảnh đó)*. Đây **KHÁC hẳn "sinh dữ liệu tổng hợp"**: ta không bịa ảnh, không bịa đáp án, chỉ thêm câu hỏi vào ảnh thật.
6. **DG2 — suy luận trật tự màn (đóng góp đa bước chính)** trên **AndroidControl** (hợp lệ vì *có* gold trajectory): N ảnh xáo trộn → tự xếp rồi sinh tutorial; **headline = Kendall τ-b** chấm partial-order-aware (chỉ phạt cặp bắt buộc) + so **SELF-ORDER vs ORACLE-ORDER** (ordering gap) + **signal-attribution** theo nhóm ordering-cue.
7. **DG2 / Tier A — trục tham chiếu chuẩn ngành** trên **AndroidControl**: **Action-Type accuracy, Grounding@14%, Step-SR** (teacher-forced). Đóng vai mốc tham chiếu định tính, *không* phải đa bước chính, *không* so ngang leaderboard.

### 🔭 HƯỚNG PHÁT TRIỂN (nêu rõ, KHÔNG cam kết số liệu) — kèm lý do

> Nguyên tắc: **future-work = chỉ những thứ KHÔNG có dữ liệu/thước đo để chấm**, chứ không phải "việc khó nên bỏ".

| Phần | Vì sao để future-work (lý do *khách quan*, không phải vì lười) |
|---|---|
| **Chấm định lượng tiếng Việt** | **Không tồn tại** bộ dữ liệu VH/gold trajectory tiếng Việt ở bất kỳ đâu → các metric (chỉ-đúng-chỗ, tỷ-lệ-bịa, τ-b trật tự) **không tính được** bằng tiếng Việt. |
| **World-model tự huấn luyện (AGENT-NSI)** | Cần *huấn luyện model* để đoán màn kế → ngoài tầm thời gian một luận văn thạc sĩ. |
| **Nhánh web (Mind2Web)** | Mở rộng từ mobile sang web là một hướng riêng; dữ liệu web (Mind2Web) chỉ có DOM, không có bbox pixel → cần khung chấm khác. |

> **Về tiếng Việt (thầy ưu tiên) — cách dung hoà trung thực:**
> - **Số liệu định lượng** chạy trên MobileViews (Anh/Trung) — nơi *có* thước đo chuẩn.
> - **Tiếng Việt** vẫn hiện diện đúng nghĩa: (a) là **động cơ thực tế** (eTax), (b) **kiểm tra OCR đọc chữ Việt** (đo được), (c) **demo định tính** trên vài màn app Việt tự thu — *hệ vẫn sinh hướng dẫn bằng tiếng Việt được*, chỉ là **chấm điểm tự động** phải neo trên dữ liệu Anh/Trung.
> - Nên trao đổi điểm này với thầy **sớm** để thống nhất kỳ vọng (sẽ *không* có bảng số tiếng Việt — vì khách quan không có thước đo).

---

## 6. Hệ thống sẽ xây — tóm tắt 5 bước (chi tiết ở `03b`)

```
ẢNH + CÂU HỎI
   │
   ① DÒ & ĐÁNH SỐ mọi nút trên ảnh           (tool OmniParser + OCR)  → bảng nút ①②③…
   ② VẼ SỐ lên ảnh                            (Set-of-Mark)
   ③ MODEL SINH hướng dẫn, CHỈ được chỉ số    (Qwen2.5-VL / GPT-4o, có ràng buộc) → "bấm ③…"  ◀ CHỖ CHỐNG BỊA CHÍNH
   ④ KIỂM 3 TẦNG: có số? đúng-ý? sai thì sửa  (V1 code + V2 LLM khác + V3 tự sửa)
   ⑤ ĐỔI SỐ → TOẠ ĐỘ                           → hướng dẫn cuối + dữ liệu để chấm
```

**Ý tưởng cốt lõi (một câu):** biến bài *tự luận* (máy tự viết → hay bịa) thành bài *trắc nghiệm* (đánh số nút → ép máy chỉ vào số) → **máy không thể bịa nút**.

> **Chống bịa nằm ở ĐÂU — nói rõ để không hiểu nhầm:** cơ chế chống bịa **chính** là **bước ③ — SINH có ràng buộc** (ép model *chỉ được chọn trong danh sách nút đã dò ở bước ①*), **KHÔNG phải** khâu kiểm ④. Khâu ④ chỉ là lưới an toàn bắt phần sót. Trong **kiểm 3 tầng** ở bước ④:
> - **V1 — so khớp bằng code (không phải LLM):** chương trình kiểm máy móc xem số mà model trích có **thật sự nằm trong** bảng nút đã dò không. Tất định, không nhờ AI.
> - **V2 — một LLM *khác*:** một model thứ hai đọc lại để kiểm hướng dẫn có **đúng ý** câu hỏi không (critic).
> - **V3 — tự sửa:** nếu V1/V2 báo lỗi, model **viết lại** cho đúng (self-refine).

> *Chạy thử trên **EX-A (eTax)** — ví dụ minh hoạ tự soạn, không phải record thật của dataset:* ① dò ra các nút và đánh số: ①*Tra cứu nghĩa vụ thuế*, ②*Khai thuế*, ③*Nộp thuế*… → ② vẽ số ①②③ lên ảnh → ③ máy buộc phải trả lời bằng số: *"Bấm ①"* (không thể viết *"vào Cài đặt"* vì *Cài đặt* không có trong danh sách số) → ④ kiểm: số ① có thật không, có đúng ý "kiểm tra đã nộp thuế" không → ⑤ đổi ① thành câu chữ + toạ độ: *"1. Bấm 'Tra cứu nghĩa vụ thuế'."*

> **MỘT hệ, TÁI DỤNG cho các chế độ** (không xây nhiều hệ riêng) — nhờ **Stage 0 "Screen-Ordering"** đặt TRƯỚC 5 bước:
> - **(a) DG1 màn-0 (N=1)** — Stage-0 rỗng → chạy 5 bước **1 lần** trên ảnh duy nhất (*EX-A: ảnh eTax → 1 hướng dẫn*).
> - **(b) DG2 suy luận trật tự (N≥2)** — Stage 0 xếp N ảnh xáo trộn (SELF-ORDER) → rồi chạy 5 bước trên **từng màn theo thứ tự** (*EX-B: xếp B1→B2→B3 rồi sinh*). ORACLE-ORDER = bỏ qua Stage 0, nạp thứ tự đúng sẵn.
> - **(c) Tier A (tham chiếu)** — chạy **từng bước** trên màn thật của đáp án (*EX-B: chạy lại ở từng màn thật*).
>
> **Stage 0 gồm:** S0a per-screen feature (TÁI DÙNG parser của bước ① — không thêm module); S0b ordering reasoner **chính = hỏi-từng-cặp rồi tổng hợp** (mỗi cặp hỏi VLM "màn nào trước?" + bắt trích ≥1 ordering-cue → tổng hợp bằng **Copeland score**), **listwise** (1 lần ép xếp cả dãy) làm đối chứng chạy ngang chi phí; S0c verifier bằng code (không LLM), gặp chu trình mâu thuẫn → gỡ xấp xỉ bằng min-feedback-arc-set.
>
> **Chi phí Stage 0 + chạy công bằng (đăng ký trước):**
> - Hỏi-từng-cặp = **C(N,2) lần gọi LLM**: N=10 → 45 lần; ở p95 N=13 → 78 lần **mỗi episode**. ⇒ **CHỐT trần N ≤ 6** cho đường cong headline (≥30 episode/mốc; báo *thêm* tới ~10 nếu ngân sách cho phép); **tính chi phí Stage 0 vào ngân sách**.
> - **Fair-compute:** so pairwise vs listwise ở **CÙNG tổng số lần gọi LLM** (listwise dùng **self-consistency** — *gọi model nhiều lần cho cùng input rồi lấy thứ tự được bình chọn nhiều nhất* — với số mẫu = số lần gọi của pairwise) → không thiên vị bên nào do được gọi nhiều hơn.
> - **Phá hoà (tie) Copeland TẤT ĐỊNH** (vd theo chỉ số ảnh tăng dần), **tách khỏi** việc xử lý cặp tự-do.
>
> Tất cả dùng **chung một bộ đối chiếu đáp án đã cố định** (để so công bằng). Và mỗi số đều báo **hai con số để tránh tự huyễn điểm**:
> - **chấm máy tự chạy** (số thực, đúng như hệ hoạt động);
> - **chấm bao dung tối đa** (giả định khâu đổi-số-thành-toạ-độ luôn đúng, để tách riêng lỗi của khâu đó).

---

## 7. Cách kiểm chứng — thí nghiệm "thang bậc" & vì sao kết quả âm vẫn ĐẬU

Không so kiểu "hệ tôi vs hệ trần", vì hệ thêm 4 cơ chế một lúc, thắng cũng không biết nhờ cơ chế nào. Thay vào đó **thêm từng cơ chế, đo từng nấc:**

| Nấc | = | Trả lời |
|---|---|---|
| C0 | VLM viết thẳng | đáy |
| **C1** | + tự sửa | **baseline để so** |
| C2 | + đánh số nút | *đánh số* có giúp? |
| C3 | + ép chỉ chọn số + kiểm tồn tại | *ràng buộc* có giúp? |
| C4 | + kiểm đúng-ý | *kiểm ý* có giúp? |

→ Nhìn mức thay đổi **C1→C4** biết **chính xác cơ chế nào trả công**.

> **Vì sao kết quả ÂM vẫn là luận văn tốt:** trước khi chạy, ta **đăng ký giả thuyết** (pre-register — tức **cam kết câu hỏi + ngưỡng đánh giá TRƯỚC khi chạy thí nghiệm, nên không thể "thua thì đổi đề"**) cho cả DG1 lẫn DG2 — nên kết quả nào cũng là một câu trả lời khoa học hợp lệ, không phải "thua thì đổi câu hỏi".
> - **DG1:** nếu hoá ra "ràng buộc cấu trúc không cải thiện gì một khi đã kiểm soát khả năng dò nút" → đó vẫn là **phát hiện có giá trị + giải thích được vì sao** (khả năng dò nút mới là trần). Một null *có giải thích cơ chế* là đóng góp; "không thắng baseline mà không giải thích" thì không.
> - **DG2:** ta đặt trước một **giả thuyết có thể bị bác + ngưỡng cụ thể** về trục trật tự, ví dụ *"τ-b của SELF-ORDER cao hơn baseline RANDOM-ORDER một mức tối thiểu đã định, và ORACLE-ORDER ≥ SELF-ORDER − ε ở mọi episode"*, kèm **giới hạn nhiễu (độ rộng khoảng tin cậy) tối đa** để kết quả được coi là "đọc được". Nếu τ-b không vượt ngưỡng, hoặc nhiễu vượt mức → đó là **DG2 thất bại CÓ Ý NGHĨA** (kết luận: model chưa suy luận trật tự ổn định ở quy mô này). Nhờ có ngưỡng-bác-được rõ ràng, DG2 không rơi vào kiểu "kết quả nào cũng coi là phát hiện".
>   - **Ngưỡng "vượt RANDOM" = phân phối NULL thực nghiệm theo TỪNG N** (sinh nhiều hoán vị ngẫu nhiên, đo τ-b của chúng để lấy phân phối), **KHÔNG** giả định kỳ vọng τ-b ngẫu nhiên = 0 (vì với cặp bắt buộc/τ-b-b kỳ vọng null có thể lệch 0).
>   - **Baseline đối xứng tách nguồn tín hiệu:** **GOAL-ONLY** (che ảnh, chỉ đưa mục tiêu) ⊕ **VISUAL-ONLY** (che mục tiêu, chỉ đưa ảnh) ⊕ **RANDOM-ORDER** (xếp ngẫu nhiên, làm sàn null cho τ-b) → nếu GOAL-ONLY đã cao thì tín hiệu giao diện không phải nguồn chính; nếu VISUAL-ONLY đã cao thì ảnh tự đủ — hai baseline đầu **tách đóng góp của ảnh so với mục tiêu**, còn RANDOM-ORDER cho biết τ-b của SELF-ORDER có thật sự vượt mức ngẫu nhiên không.
> **Tóm lại: luận văn không phụ thuộc vào việc hệ phải thắng.**

---

## 8. Tính khả thi (đã red-team kỹ — `04`)

| Hạng mục | Thực tế |
|---|---|
| Linh kiện | **100% có sẵn, cài được, không phải tự chế** (OmniParser, Set-of-Mark, Qwen2.5-VL) |
| Dữ liệu (3 bộ, vai cố định) | **MobileViews** (v1/v3 — ghi rõ phiên bản khi trích) → màn-0 cho DG1; **AndroidControl** (NeurIPS 2024 D&B) → đa bước: Tier A (teacher-forced, trục tham chiếu chuẩn ngành) + DG2 suy luận trật tự màn (ORACLE-ORDER vs SELF-ORDER); **ScreenSpot** (gốc = SeeClick, ACL 2024) **/ ScreenSpot-v2** (OS-Atlas, ICLR 2025) → đối chứng grounding + bù credibility. *AITW (NeurIPS 2023) phân vai đôi: (a) nguồn ngưỡng 14% — trích bắt buộc; (b) dataset đối chứng — tuỳ chọn. Mind2Web = tuỳ chọn / future-work nhánh web.* |
| Huấn luyện model | **KHÔNG cần fine-tune** cho phần lõi |
| Phần cứng | **1 GPU 24GB** (RTX 4090/3090, mua hoặc thuê ~$0.3–0.5/giờ) |
| Chi phí API | **~$100–300** (dùng model rẻ cho khâu chấm + chạy theo lô) |
| Mốc kiểm tra sớm | Bộ "kill-test" ≤1 ngày/cái để loại rủi ro **trước khi** cam kết, gồm **4 cổng cứng**: **K1** (đo recall dò nút), **KN** (tự đếm histogram độ dài episode AndroidControl), **KZ'** (rà prior-art sắp-ảnh), **KB** (chống leak step-index khi xáo ảnh) — tổng 10 kill-test |

**Rủi ro lớn nhất (nói thẳng với thầy):** hệ chỉ giỏi bằng bước **dò nút**; theo ước lượng, bộ dò có thể bỏ sót **khoảng một nửa** icon trên app mobile dày — nhưng con số này **chưa được công bố rõ**, nên **việc đầu tiên (tuần 1)** là *tự đo tỷ lệ dò trúng* (kill-test K1). Mọi con số về sau ghi kèm điều kiện này. Nếu thấp → **đổi cách phát biểu** thành "đánh giá grounding *trong giới hạn khả năng dò*" (vẫn là đóng góp), **không bỏ đề tài**.

---

## 9. Thầy có thể hỏi — và câu trả lời

**H: Sao không làm đa bước?**
Đ: Em **CÓ làm đa bước**, đặt thành bài toán **suy luận trật tự màn**: đưa **N ảnh ĐÃ XÁO TRỘN** của một luồng + mục tiêu → máy phải tự xếp đúng thứ tự rồi sinh hướng dẫn. Chấm được vì bộ **AndroidControl** *có gold trajectory*. *Ví dụ EX-B (đặt báo thức 7:00): máy nhận 3 ảnh tráo thứ tự, phải tự suy ra B1→B2→B3.* Em đo bằng **Kendall τ-b** (chỉ phạt cặp bắt buộc) và so **SELF-ORDER vs ORACLE-ORDER** để biết "cái giá của việc không biết trật tự". Em vẫn giữ **Tier A** (teacher-forced, chuẩn ngành) làm trục **tham chiếu**. Chỉ còn **chấm định lượng tiếng Việt** và **world-model tự huấn luyện** là hướng phát triển — vì những thứ đó thật sự **không có dữ liệu/thước đo** để chấm. Tiếng Việt vẫn có **demo định tính**.

**H: Ai sẽ dùng tính năng nạp N ảnh trong thực tế?**
Đ: Em **trung thực** với thầy: chế độ N-ảnh **không phải** để khẳng định "người dùng thường nạp nhiều ảnh". Nó là **bài toán em ĐẶT RA để ĐO** một năng lực cụ thể — *model có biết thứ tự các màn không* — đúng câu hỏi thầy nêu. Trong sản phẩm thật, đường N=1 (1 ảnh) vẫn là trải nghiệm chính; N-ảnh là **thí nghiệm đo lường**, không phải lời hứa giao diện.

**H: Lúc deploy thì lấy đâu ra "đáp án đúng" để máy xếp — có phải máy được nhìn đáp án không?**
Đ: Không. Cần tách rõ **hai khâu khác nhau**: (1) **lúc xếp (cả khi deploy lẫn thí nghiệm)** máy **chỉ đọc ảnh** — không hề thấy gold trajectory hay View Hierarchy; cơ chế xếp hoàn toàn dựa vào manh mối trên ảnh. (2) **Gold trajectory / VH chỉ được dùng ở khâu CHẤM ĐIỂM OFFLINE** (sau khi máy đã xếp xong, em mới lấy đáp án thật ra so) — **không bao giờ là input của model**. Nói cách khác, đáp án chỉ là "thước đo của giám khảo", không phải "gợi ý cho thí sinh". Nhờ vậy năng lực đo được phản ánh đúng tình huống thật ngoài đời (nơi không có đáp án).

**H: Sắp xếp đúng 3 màn thì quá dễ, có đo được gì không?**
Đ: Em đã **khảo sơ bộ độ dài episode của AndroidControl**: trung bình **~5,5 bước/episode**, **percentile-95 = 13 bước**. Nên trục N thực tế trải dài **N ∈ [3, ~10]** (đường-cong headline **N≤6**, ≥30 episode/mốc; báo thêm tới ~10 nếu ngân sách cho phép), không chỉ N=3. Em **loại N≤2** (N=2 chỉ 1 cặp → τ-b vô nghĩa) và sẽ **tự đếm histogram chính xác** ở tuần 1 (cổng KN) để báo số episode còn lại ở mỗi mốc N. Ở N lớn (8–10 màn), xếp đúng thứ tự là bài toán thật sự khó. **Về thống kê (đăng ký trước):** vì N rời rạc, em cam kết **≥30 episode mỗi mốc N** và **hiệu chỉnh đa-kiểm-định Holm–Bonferroni** (*siết ngưỡng ý-nghĩa khi kiểm định nhiều mốc N cùng lúc — tránh false positive do thử nhiều lần*) khi so nhiều mốc N (hoặc hạ giả thuyết theo-N xuống *exploratory* nếu không đủ episode) — tránh "đãi cát tìm vàng" trên nhiều mốc.

**H: Đã có ai làm "sắp xếp ảnh" chưa — có gì mới?**
Đ: Em đã rà prior-art (cổng KZ') và **thừa nhận có dòng nghiên cứu gần**: **Sort-Story** (Agrawal et al., EMNLP 2016 — sắp ảnh+caption bị tráo), **"Sequencing Multimodal Instructional Manuals"** (Wu et al., ACL 2022 — sắp các bước hướng dẫn đa phương thức bị tráo), **RankGPT** (Sun et al., EMNLP 2023 — LLM sinh hoán vị theo truy vấn). Em **KHÔNG claim "sắp ảnh tráo là mới"**. Điểm mới của em là **kết hợp**: (a) miền **GUI màn hình**, (b) **điều kiện hoá theo mục tiêu/use-case**, (c) gắn thứ tự đã xếp → **SINH tutorial**, và (d) **signal-attribution** (chỉ ra *manh mối thứ tự* nào giúp xếp đúng).
> **Caveat về cue (nói rõ để khỏi bị bắt bẻ):** cue mà model **tự trích** chỉ là *tín hiệu giải thích yếu* (model có thể khai một đằng làm một nẻo). Kết luận "**cue nào trả công**" em rút từ **stratification một-cue** (chỉ giữ cặp phân biệt bởi đúng một cue rồi đo độ chính xác theo nhóm), **KHÔNG** dựa vào lời model tự khai.

**H: Đóng góp đủ tầm thạc sĩ chưa?**
Đ: Có: (1) một **phương pháp đánh giá không cần đáp án mẫu** áp được cho bài toán này; (2) một **thí nghiệm có kiểm soát, đăng ký giả thuyết trước** trả lời rõ một câu hỏi khoa học; (3) **pilot chuyên gia** kiểm metric. Đây là khối lượng + tính khoa học chuẩn thạc sĩ, không thổi phồng.

**H: Nếu hệ không thắng baseline thì sao?**
Đ: Vẫn đậu — vì đóng góp là *quy trình đánh giá + câu trả lời có giải thích*, không phải "hệ phải thắng" (mục 7). *Ví dụ EX-A: nếu hoá ra việc "ép máy chỉ chọn nút đã dò" không bịa ít hơn "để máy viết tự do", đó vẫn là một kết luận có ích — chứng tỏ điểm nghẽn nằm ở khâu dò nút, không ở khâu sinh chữ.*

**H: Có gì mới so với các bài đã có?**
Đ: **Em đặt độ mới ở TRỤC ĐÁNH GIÁ, KHÔNG ở trục sắp-xếp ảnh.** Đóng góp CHÍNH của luận văn là **phương pháp ĐÁNH GIÁ (DG1+DG2) khi không có gold tutorial của người** — pipeline ReOrder-Tutor chỉ là **hệ tham chiếu off-the-shelf để vận hành đánh giá, KHÔNG claim SOTA**. Cái mới nằm ở chỗ: (a) **chống vòng-lập-luận (D1)** — nhãn cặp bắt buộc suy từ gold trajectory bằng quy tắc tất định, không lấy từ chính bộ cue model dùng; (b) **truy-nguồn tín hiệu một-cue** (signal-attribution bằng stratification, không che pixel); (c) **chấm thứ-tự-bộ-phận** (τ-b partial-order-aware — *adaptation tự định nghĩa của luận văn*, chỉ phạt cặp bắt buộc); (d) **audit người** kiểm quy tắc tất định. Khung đánh giá này kế thừa khung Intrinsic+Extrinsic của **Chim, Ive, Liakata (Computational Linguistics 51(1):191–233, 2025 — tạp chí)** và dùng **Kendall τ-b** theo tiền lệ **Lapata (Computational Linguistics 32(4):471–484, 2006)** "dùng τ chấm ordering".
Ở **trục sắp-xếp ảnh** thì em **THỪA NHẬN PRIOR-ART**, KHÔNG claim "sắp ảnh tráo là mới": **Sort-Story (Agrawal et al., EMNLP 2016)** / **Wu et al. (ACL 2022)** / **RankGPT (Sun et al., EMNLP 2023)**. Phần đóng góp ở trục này chỉ là **áp dụng có hệ thống vào miền GUI + điều kiện-theo-mục-tiêu + gắn thứ tự đã xếp → SINH tutorial**. *Trước khi chốt là "mới", em đã rà related-work (KZ'); nếu trùng thì hạ tuyên bố xuống "đặt tên + áp dụng có hệ thống".* *(Lưu ý nguồn: OS-Atlas — bản làm sạch ScreenSpot-v2 — là ICLR 2025, **đã bình duyệt**.)*

**H: Em tự soạn câu hỏi thì có phải "tự chế dữ liệu", có thiên vị không?**
Đ: Không. **Chỉ MobileViews** mới cần em tự soạn câu hỏi (bộ này chỉ có ảnh + cây giao diện, không kèm câu hỏi); còn **AndroidControl và ScreenSpot đã có sẵn câu hỏi/tác vụ**. Quan trọng hơn: "tự soạn câu hỏi" = **chỉ viết phần INPUT (câu hỏi) gắn vào ảnh có sẵn** — *đáp án để chấm vẫn là dữ liệu thật (cây giao diện của chính ảnh đó)*. Em **không** bịa ảnh, **không** bịa đáp án → khác hẳn "sinh dữ liệu tổng hợp". Để tránh thiên vị, câu hỏi được soạn theo quy ước cố định (đăng ký trước) chứ không chỉnh cho hệ dễ thắng.

**H: Chắc chắn làm xong trong thời gian không?**
Đ: Linh kiện có sẵn, không train, 1 GPU + ~$300; có lộ trình 6 pha (P0, P1, P2, P2b, P3, P4) với cổng kiểm tra. Tuần 1 chạy kill-test để chốt chắc trước khi cam kết.

**H: MobileViews là preprint chưa bình duyệt, dùng có ổn không?**
Đ: Em thừa nhận điểm này; nên em **ghép thêm bộ ĐÃ bình duyệt làm mỏ neo**: **ScreenSpot (ACL 2024)** để đối chứng grounding + **AndroidControl (NeurIPS 2024 D&B)** cho phần đa bước. **MobileViews chỉ dùng như kho ảnh + VH**, còn **metric chấm điểm lấy từ paper bình duyệt** — nên xương sống phương pháp không tựa vào preprint.

**H: Thầy ưu tiên tiếng Việt, sao không có bảng số tiếng Việt?**
Đ: Vì **KHÔNG tồn tại dữ liệu View Hierarchy tiếng Việt** để chấm tự động. Hệ **VẪN sinh được hướng dẫn bằng tiếng Việt**; em giữ tiếng Việt ở dạng **động cơ thực tế (eTax)** + **kiểm OCR đọc đúng dấu** + **demo định tính**. Phần **định lượng chạy trên Anh/Trung** vì pipeline và metric vốn **độc-lập-ngôn-ngữ** (chấm bằng toạ độ / bbox / định dạng), nên kết quả số vẫn phản ánh đúng năng lực hệ.

---

## 10. ĐỀ NGHỊ THẦY DUYỆT

Em xin **chốt phạm vi luận văn** gồm **DG1 + DG2** ở mục 5: (DG1) đánh giá màn-0 không cần tutorial mẫu + thí nghiệm thang bậc trên **MobileViews**; (DG2) **suy luận trật tự màn** trên **AndroidControl** (N ảnh xáo trộn → tự xếp rồi sinh; headline Kendall τ-b + so SELF-ORDER vs ORACLE-ORDER + signal-attribution), giữ **Tier A** (teacher-forced) làm trục tham chiếu chuẩn ngành. Chỉ để **tiếng Việt định lượng / world-model tự huấn luyện / nhánh web Mind2Web** là **hướng phát triển**.

**Tuần này em sẽ chạy nhanh các kill-test (quan trọng nhất: đo tỷ lệ dò nút thật + tự đếm histogram độ dài episode)** rồi báo lại thầy để chốt cách phát biểu cuối cùng.

---

### Lộ trình 6 pha — P0, P1, P2, P2b, P3, P4 (mỗi pha có "điều kiện hoàn thành")
1. **Pha 0 (P0) — Chuẩn bị:** cài môi trường, cố định phiên bản công cụ, kiểm GPU.
2. **Pha 1 (P1) — Cổng kiểm tra (cứng):** **K1** đo tỷ lệ dò nút trên MobileViews/ScreenSpot/AndroidControl → chốt cách phát biểu; **KN** tự đếm histogram độ dài episode AndroidControl (xác nhận đủ episode ở N∈[3,~10], đường-cong headline **N≤6**, ≥30 episode/mốc); **KZ'** rà prior-art sắp-ảnh (Sort-Story/ACL 2022/RankGPT) để đóng khung độ-mới; **KB** kiểm chống leak step-index khi xáo ảnh (strip metadata + tái mã hoá ảnh + đặt tên UUID; **khi tái mã hoá còn CHE status bar / đồng hồ / pin / badge** để khỏi rò trật tự qua đồng hồ tăng dần, và **loại episode 2-ảnh trùng-pixel**; detector mù không suy ra thứ tự tốt hơn ngẫu nhiên).
3. **Pha 2 (P2) — Bộ chấm điểm DG1:** code metric DG1 trên **MobileViews** (kiểm matcher rồi đông cứng) + đối chứng resolver trên **ScreenSpot-v2**.
4. **Pha 2b (P2b) — Bộ chấm điểm DG2:** dựng bộ chấm **trật tự** (Kendall τ-b partial-order-aware + pairwise-order-accuracy + position-accuracy) cho SELF-ORDER vs ORACLE-ORDER + **Tier A** (Action-Type/Grounding@14%/Step-SR teacher-forced) trên **AndroidControl**; tái dùng matcher đã freeze.
5. **Pha 3 (P3) — Thí nghiệm thang bậc (DG1)** trên tập nhỏ 50–100 mẫu; đồng thời dựng Stage 0 ordering + đường ống **Tier A** trên **AndroidControl**.
6. **Pha 4 (P4) — Chạy đầy đủ DG1 + DG2** (SELF-ORDER vs ORACLE-ORDER + signal-attribution theo cue + Tier A tham chiếu trên AndroidControl) **+ pilot chuyên gia**, viết kết quả (kể cả null cho cả hai đóng góp).
