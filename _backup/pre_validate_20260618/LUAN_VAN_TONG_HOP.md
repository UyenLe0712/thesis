# LUẬN VĂN — BẢN TỔNG HỢP TOÀN BỘ (đọc một file là hiểu hết)

> **Đề tài:** Sinh tự động hướng dẫn sử dụng phần mềm bằng LLM/VLM, từ **một ảnh chụp màn hình giao diện + một câu hỏi use-case**, và **khung đánh giá khi không có đáp án mẫu**.
>
> **Mục đích file này:** gộp toàn bộ các báo cáo `00`–`08` thành một tài liệu liền mạch, dễ đọc, đầy đủ — để đọc tuần tự một lần là nắm được cả đề tài, cách làm, cách chấm điểm, tính khả thi và kế hoạch. Mọi thuật ngữ chuyên ngành đều được giải thích đời thường ngay tại chỗ; mọi citation đã được kiểm chứng qua web.
>
> **Cách đọc:** Phần 0 là tóm tắt 2 phút. Các phần I–XIII đi từ "vì sao" → "làm gì" → "ví dụ" → "lưu ý". Phần XII là Q&A chuẩn bị trả lời thầy. Phần XIII là từ điển bỏ túi.

---

## MỤC LỤC

- **Phần 0** — Tóm tắt điều hành (đọc 2 phút)
- **Phần I** — Bài toán & vì sao khó
- **Phần II** — Hai đóng góp (bức tranh lớn)
- **Phần III** — Pipeline: biến "tự luận" thành "trắc nghiệm" (kèm ví dụ chạy 5 bước)
- **Phần IV** — Dữ liệu: 3 bộ chính + 2 bộ phụ
- **Phần V** — Cách chấm điểm (DG1 màn-0 + DG2 đa bước), nhiều ví dụ số
- **Phần VI** — Thí nghiệm khoa học: thang bậc C0→C4 + đối chiếu người
- **Phần VII** — Tính khả thi + kill-test tuần 1 (4 cổng cứng: K1, KN, KZ', KB)
- **Phần VIII** — Kế hoạch thực hiện: các pha có cổng
- **Phần IX** — Luận chứng nguồn (venue từng metric/dataset)
- **Phần X** — Vì sao kết quả xấu vẫn ĐẬU (pre-registration)
- **Phần XI** — Phạm vi chốt & future-work
- **Phần XII** — Hỏi–đáp chuẩn bị cho buổi bảo vệ
- **Phần XIII** — Thuật ngữ bỏ túi
- **Phụ lục** — Bảng citation (venue + tư cách)

---

# PHẦN 0 — TÓM TẮT ĐIỀU HÀNH (đọc 2 phút)

**Bài toán.** Người dùng đưa vào **1 ảnh màn hình + 1 câu hỏi** (vd app thuế eTax: *"Kiểm tra đã nộp thuế chưa thì vào đâu?"*). Máy trả ra **hướng dẫn bấm từng bước** cho người đọc (*"1. Bấm 'Tra cứu nghĩa vụ thuế'. 2. Chọn kỳ. 3. Xem trạng thái."*).

**Ba cái khó cốt lõi:** (1) **không có "đáp án mẫu"** (không ai viết sẵn tutorial chuẩn để máy học/đối chiếu); (2) **máy hay "bịa" nút** không tồn tại; (3) **đa bước** — khi có nhiều màn của một luồng, làm sao biết **trật tự đúng** giữa các màn (đúng câu hỏi của thầy: *"model dựa vào đâu để biết trật tự?"*).

**Hai đóng góp song hành** (phân biệt bằng câu hỏi: *"có sẵn đáp án đúng để so hay không?"*):
- **DG1 — đánh giá tutorial trên màn hình thấy được (màn-0), KHÔNG cần tutorial mẫu của người.** Neo vào **View Hierarchy (VH)** — cây cấu trúc UI có sẵn toạ độ mọi nút trong dataset — làm "đáp án để chấm". Đây là *đóng góp phương pháp đánh giá* mới.
- **DG2 — suy luận trật tự màn (Screen-Order Inference), CÓ đáp án (reference-based)** trên dataset AndroidControl. Input = **N ảnh ĐÃ XÁO TRỘN** của một luồng đa bước + mục tiêu → model phải (1) suy ra **THỨ TỰ đúng** của các màn, (2) sinh hướng dẫn từng bước theo thứ tự đó. Headline = **Kendall τ-b** chấm **theo thứ-tự-bộ-phận** (partial-order-aware). Giữ thêm **Tier A** (đo từng bước với màn thật — chuẩn ngành, là *mốc tham chiếu / skyline*). Đây là *bài toán đặt ra ĐỂ ĐO năng lực suy luận trật tự*, không khẳng định "N-ảnh" là nhu cầu deploy phổ biến.

**Cách chống bịa (pipeline).** Biến bài **tự luận** (máy tự viết → dễ bịa) thành bài **trắc nghiệm**: dò + **đánh số** mọi nút trên ảnh, rồi **ép** máy chỉ được "chỉ vào số" đã có → không có số thì không nhắc được → không bịa được.

**Dữ liệu (3 bộ chính):** MobileViews (màn-0/DG1), AndroidControl (đa bước/DG2), ScreenSpot (đối chứng grounding). Định lượng chạy app tiếng Anh/Trung; **tiếng Việt chỉ là động cơ + demo định tính** (vì không tồn tại dữ liệu VH tiếng Việt để chấm).

**Bảo hiểm khoa học:** đăng ký giả thuyết + ngưỡng **trước khi chạy** (pre-registration) → **kết quả null (hệ không thắng baseline) vẫn là đóng góp hợp lệ** nếu giải thích được cơ chế.

**Tính khả thi:** linh kiện có sẵn, **không cần fine-tune**, 1 GPU 24GB + ~$100–300 (ước tính). Rủi ro lớn nhất: bộ dò nút bỏ sót nhiều element → **việc đầu tiên tuần 1 là tự đo tỷ lệ dò (kill-test K1)**. Hai cổng cứng mới cho DG2: **KN** (tự đếm histogram độ dài episode) + **KZ'** (rà prior-art bài toán sắp-ảnh), cộng **KB** (chống leak step-index khi xáo trộn).

---

# PHẦN I — BÀI TOÁN & VÌ SAO KHÓ

## 1.1. Hợp đồng với người dùng

| Vào | Ra |
|---|---|
| 1 ảnh chụp màn hình UI tĩnh + 1 câu hỏi ngôn ngữ tự nhiên | Hướng dẫn bấm **từng bước** cho người đọc |

> **Ví dụ xuyên suốt #1 (gọi tắt EX-A — app eTax, đơn bước/màn-0) — ⚠️ ví dụ minh hoạ tự soạn, không phải record thật:**
> - **Ảnh:** màn hình chính eTax (có các nút *Khai thuế, Nộp thuế, Tra cứu nghĩa vụ thuế, Thông báo, Cá nhân*…).
> - **Câu hỏi:** *"Tôi muốn kiểm tra đã nộp thuế chưa thì vào đâu?"*
> - **Máy trả:** *"1. Bấm 'Tra cứu nghĩa vụ thuế'. 2. Chọn kỳ tính thuế. 3. Xem trạng thái đã/chưa nộp."*

**Quan trọng:** lúc chạy thật máy **chỉ thấy ảnh + câu hỏi**. Nó **không** được xem "cây cấu trúc UI" (View Hierarchy). Cây đó **chỉ dùng lúc chấm điểm**. Mọi xử lý bên dưới là hộp đen với người dùng.

## 1.2. Ba cái khó cốt lõi

1. **Không có "đáp án mẫu".** Không tồn tại bộ tutorial chuẩn do người viết cho từng app → phải **nghĩ ra cách chấm điểm khi thiếu đáp án mẫu** (đây là chỗ đóng góp về phương pháp).
2. **Máy hay "bịa" nút.** Mô hình nhìn-ảnh-viết-chữ (**VLM** = Vision-Language Model, như GPT-4o, Qwen2.5-VL) thường bịa ra nút không có trên màn ("bấm Cài đặt" trong khi màn này không có) → cần **cơ chế chống bịa**.
3. **Đa bước — làm sao biết trật tự màn.** Một việc gồm nhiều màn (*bấm → mở màn mới → bấm tiếp*). Khi đưa cho máy **nhiều màn của luồng nhưng bị xáo trộn**, nó phải **suy ra thứ tự đúng** rồi mới sinh hướng dẫn — đây chính là câu hỏi của thầy: *"model dựa vào đâu để biết trật tự?"*

## 1.3. Đề tài này dùng để làm gì trong thực tế?

- **Trợ lý hướng dẫn trong app / hệ thống trợ giúp** (người dùng kẹt ở màn nào → hỏi → nhận hướng dẫn).
- **Onboarding người mới**, **hỗ trợ người khiếm thị (accessibility)**, **sinh tài liệu hướng dẫn tự động** từ ảnh chụp.
- Hai kiểu triển khai khác nhau: (a) trợ lý chạy **trực tiếp trong app** (thấy từng màn thật — ứng với Tier A, mốc tham chiếu ở Phần V); (b) sinh hướng dẫn **tĩnh từ ảnh** (chatbot/tài liệu) — gồm cả màn-0 (N=1, DG1) lẫn nhiều màn cần xếp trật tự (N≥2, DG2).

---

# PHẦN II — HAI ĐÓNG GÓP (BỨC TRANH LỚN)

Luận văn tách thành 2 nhánh, phân biệt bằng một câu hỏi đơn giản: **"có sẵn đáp án đúng để so hay không?"**

| | **Đóng góp 1 (DG1)** | **Đóng góp 2 (DG2)** |
|---|---|---|
| Đo gì | Tutorial trên **màn hình thấy được (màn-0)** | **Suy luận trật tự màn** (xếp N ảnh xáo trộn rồi sinh hướng dẫn) |
| Có đáp án mẫu? | **Không** có tutorial mẫu của người → tự nghĩ cách chấm | **Có** thứ tự + đáp án từng bước (dataset AndroidControl) |
| Chấm bằng | **View Hierarchy (VH)** = cây cấu trúc UI có toạ độ mọi nút | **Kendall τ-b** (thứ tự) + grounding/hallucination từng màn so VH |
| Tính chất | Cách đánh giá **mới** khi thiếu đáp án | Bài toán **mới** (sắp trật tự GUI có điều kiện mục tiêu) + **Tier A** (chuẩn ngành, tham chiếu) |
| Là loại đóng góp | Phương pháp đánh giá | Đo lường + phân tích năng lực suy luận trật tự |

> **Lưu ý từ "reference-free":** ở DG1 ta nói "không cần đáp án mẫu" theo **nghĩa hẹp** = không có *tutorial do người viết* để so. Nhưng **vẫn có** một mỏ neo để chấm: **View Hierarchy (VH-silver)** — gọi là nhãn "bạc" vì nó do máy sinh tự động (đủ tin để chấm nhưng không hoàn hảo như nhãn "vàng" do người duyệt). Không bao giờ để cụm "reference-free" đứng trần một mình.

**Bài toán DG2 (suy luận trật tự màn) là gì?** Đưa cho model **N ảnh đã xáo trộn** của một luồng đa bước + mục tiêu → model **(1)** tự suy ra thứ tự đúng, **(2)** sinh hướng dẫn theo thứ tự đó. Đây là cách trả lời trực diện câu hỏi của thầy *"làm sao model biết trật tự"* — và **mạnh hơn** cách "đoán mù chuỗi từ 1 ảnh" cũ, vì giờ **grounding được chấm đầy đủ trên mọi màn** (không phải đoán các màn chưa thấy).

**Vì sao vẫn giữ Tier A?** Để có một **trục tham chiếu chuẩn ngành** mà thầy mong đợi:
- **Tier A (teacher-forced)** trả lời: *"Nếu mỗi bước máy được thấy màn thật của đáp án vàng, nó đoán thao tác kế đúng cỡ nào?"* → cách đánh giá agent **chuẩn ngành**, so sánh được với bài báo khác. Đây là **mốc tham chiếu / cận-trên (skyline)** — **KHÔNG phải** sản phẩm 1-ảnh, **KHÔNG** đem so bảng xếp hạng công khai. **Không còn là "đa bước chính"**; trục chính của DG2 nay là suy luận trật tự (τ-b).
- **ORACLE-ORDER vs SELF-ORDER** (xem Phần V) là skyline của riêng trục ordering: ORACLE-ORDER = đưa N ảnh đã sắp đúng (chỉ sinh hướng dẫn), SELF-ORDER = N ảnh xáo trộn (tự xếp rồi sinh). Khoảng cách giữa hai = **ordering gap** = "cái giá của việc không biết trật tự".

**Đóng góp CHÍNH = quy trình đánh giá** (không phải "hệ của tôi phải thắng"). Đây là điều giúp luận văn vững kể cả khi kết quả không đẹp (xem Phần X).

---

# PHẦN III — PIPELINE: BIẾN "TỰ LUẬN" THÀNH "TRẮC NGHIỆM"

## 3.1. Ý tưởng cốt lõi (một câu)

Nếu để VLM tự do viết, nó hay **bịa nút không tồn tại**. **Mẹo:** dò + **đánh số** mọi nút thấy trên ảnh, rồi **ép** model chỉ được trả lời bằng cách **chỉ vào số** đã có. Không có số thì không nhắc được → **không thể bịa nút**. Đây gọi là **Set-of-Mark** (gắn nhãn số) + **sinh có ràng buộc**.

Tên hệ đề xuất: **ReOrder-Tutor** = **SoM-Tutor ⊕ GroundFirst** + **Stage 0 "Screen-Ordering"** đặt TRƯỚC pipeline 5 bước. Đây là **MỘT hệ duy nhất** (không có pipeline thứ hai), có **input router**: **N=1 → đơn bước** (Stage-0 rỗng → về pipeline 5 bước cũ, màn-0/DG1 nguyên vẹn); **N≥2 → bật chế độ sắp-thứ-tự** (DG2).

## 3.2. Năm bước (kèm ví dụ EX-A chạy xuyên suốt)

```
ẢNH (eTax)  +  CÂU HỎI ("kiểm tra đã nộp thuế chưa?")
        │
        ▼
[B1] DÒ & ĐÁNH SỐ nút từ ẢNH  (OmniParser + OCR)  →  ① ② ③ ④ ⑤ …
[B2] VẼ SỐ lên ảnh  (Set-of-Mark)  →  ảnh-có-nhãn
[B3] SINH CÓ RÀNG BUỘC  (Qwen2.5-VL / GPT-4o)  →  chỉ được chỉ vào số trong danh sách  ◄ cơ chế chống-bịa CHÍNH
[B4] KIỂM 3 TẦNG  →  V1 (số có thật?) → V2 (đúng ý?) → V3 (sai thì tự sửa)
[B5] ĐỔI SỐ → TOẠ ĐỘ/CHỮ  →  hướng dẫn cuối + toạ độ để chấm
        │
        └······ (CHẤM ĐIỂM, offline) so với View Hierarchy thật
```

**B1 — Dò & đánh số (tool: OmniParser + OCR).** Đưa ảnh vào → trả về mọi vùng bấm được + chữ trên đó + ô bao (bbox), rồi đánh số. Ra **bảng E**:
```
E = { ① Khai thuế,
      ② Nộp thuế,
      ③ Tra cứu nghĩa vụ thuế  [bbox 270,820,540,1010] (minh hoạ),
      ④ Thông báo,
      ⑤ Cá nhân }
```
Đây là **toàn bộ "vốn từ"** model được phép dùng. *Nút nào không dò ra ở đây thì vĩnh viễn không nhắc được* → đây cũng là rủi ro lớn nhất (Phần VII). *Tiếng Việt:* OCR mặc định hay rớt dấu → thay bằng Qwen2.5-VL / Vintern (dự kiến, kiểm ở kill-test K3).

**B2 — Vẽ số lên ảnh (Set-of-Mark, ~30 dòng code).** Vẽ ①②③… đè lên ảnh tại đúng vị trí nút, để model "nhìn thấy số mà chỉ vào".

**B3 — Sinh có ràng buộc (Qwen2.5-VL-7B hoặc GPT-4o).** Đưa *ảnh-có-số + bảng E + câu hỏi*; model viết hướng dẫn, **mỗi bước phải chỉ vào 1 số trong E**. **Đây là cơ chế chống-bịa CHÍNH** của hệ — chặn tận gốc ngay lúc sinh (model vật lý không thể "nói" ra số/ID ngoài danh sách); lưới kiểm 3 tầng ở B4 chỉ là *lưới an toàn xếp SAU*.
- Bản chạy máy nhà (Qwen): dùng *constrained decoding* (Outlines/XGrammar, hoặc DOMINO) — chặn model "nói" ra số ngoài danh sách.
- Bản API (GPT-4o): dùng *Structured Outputs* — bắt trả JSON với trường `số` chỉ nhận giá trị trong {①..⑤}. (OpenAI giới hạn enum ~1000 giá trị / 15000 ký tự theo tài liệu tại thời điểm viết → dùng ID số ngắn.)
- **Cả hai đảm bảo 100% không nhắc SỐ/ID ngoài danh sách** (nhưng **không** khử được lỗi *mô tả sai ý* — đó là việc của V2).
- Ra: `[{bước 1, action: bấm, số: ③}, …]`.

**B4 — Kiểm 3 tầng (chống bịa):** *Đây là **lưới an toàn xếp SAU** bước sinh (B3), KHÔNG phải cơ chế chính. Trong 3 tầng, chỉ **V2 dùng một LLM khác**; **V1 là code thuần** (so khớp membership). V1 vẫn cần thiết làm chốt an toàn cho các trường hợp tự do — vd model điền trường text tự do, ghép thông tin profile, hay các bước hậu kiểm mà ràng buộc decoding không phủ hết. → **Đừng coi "verify bằng một LLM khác" là cơ chế chống-bịa chính**; cơ chế chính là sinh có ràng buộc ở B3.*

| Tầng | Hỏi gì | Cách | Bắt lỗi gì |
|---|---|---|---|
| **V1** | "Số nó nhắc có trong E không?" | so khớp danh sách, **máy tính thuần** | nhắc số không tồn tại *(B3 đã chặn rồi nên V1 gần như luôn đạt — chỉ là chốt an toàn)* |
| **V2** | "Số ③ có **đúng ý** câu hỏi không?" | một **model khác** đọc lại, đối chiếu | **đúng định dạng nhưng sai ý** |
| **V3** | (nếu V1/V2 báo sai) | bảo model sửa, **tối đa 2 lần** | tự sửa lỗi |

> **Ví dụ V2 bắt lỗi (rất quan trọng để hiểu V1 vs V2):** giả sử câu hỏi là *"kiểm tra đã nộp thuế chưa"* nhưng model lại chọn **② "Nộp thuế"** (để đi nộp) thay vì **③ "Tra cứu nghĩa vụ thuế"** (để kiểm tra). → **V1 ĐẠT** (② có thật trong E) nhưng **V2 PHÁT HIỆN SAI Ý** (câu hỏi là *kiểm tra*, không phải *nộp*) → V3 bảo sửa → ra ③. Tức **V1 chống bịa-tồn-tại, V2 chống sai-ý.**

**B5 — Đổi số → toạ độ/chữ.** Tra bảng E: số ③ → bbox [270,820,540,1010], tâm **(405, 915)** *(minh hoạ)*, chữ "Tra cứu nghĩa vụ thuế". Dùng để (a) hiển thị cho người, (b) chấm điểm (so toạ độ với VH thật).

## 3.3. Stage 0 — "Screen-Ordering" (chỉ bật khi N≥2)

Khi đầu vào là **N ảnh xáo trộn** của một luồng, trước khi chạy 5 bước trên từng màn, hệ phải **xếp lại trật tự**. Stage 0 gồm 3 phần con:

- **S0a — per-screen feature:** rút đặc trưng mỗi màn bằng cách **TÁI DÙNG parser của Stage-1/B1** (không thêm module mới).
- **S0b — ordering reasoner (CHÍNH = pairwise-then-aggregate):** với mỗi **cặp màn**, hỏi VLM *"màn nào trước?"* và bắt model **trích ≥1 ordering cue** (lý do). Tổng hợp mọi cặp thành một thứ tự bằng **Copeland score** (đếm số "trận thắng" của mỗi màn). Bản **listwise** (1 lần gọi, ép model trả thẳng một hoán vị) làm **ĐỐI CHỨNG**, chạy ở chế độ **fair-compute** (cùng ngân sách tính).
- **S0c — order verifier:** **code thuần, không LLM**. Nếu các phán đoán cặp tạo **chu trình mâu thuẫn** (A trước B, B trước C, C trước A) → gỡ bằng **min-feedback-arc-set xấp xỉ**.

**5 ORDERING CUES (đặt tên, trả lời thẳng câu hỏi thầy "model dựa vào đâu để biết trật tự"):**

| Cue | Nghĩa đời thường | Ví dụ |
|---|---|---|
| **gating** | màn bắt buộc làm trước (đăng nhập/cấp quyền) | màn đăng nhập phải đứng trước màn xem kết quả |
| **nav-affordance** | manh mối điều hướng | có nút *Next/Back/breadcrumb* |
| **state-delta** | trạng thái thay đổi | toggle off→on, ô trống→đã điền, badge 0→1 |
| **title-progression** | tiêu đề tiến triển theo phiếu/bước | "Bước 1/3" → "Bước 2/3" |
| **drill-down** | màn sau = chi tiết của item màn trước | danh sách → trang chi tiết một mục |

Chuỗi sau khi sắp xong → đưa vào **pipeline 5 bước cũ trên TỪNG màn** → grounding được chấm **đầy đủ mọi bước**. **VH chỉ dùng lúc chấm**, không vào lúc sinh.

## 3.4. Một hệ, các chế độ chạy (không có hệ thứ hai)

| Chế độ | Chạy thế nào | Phục vụ |
|---|---|---|
| **(a) Tutorial màn-0 (N=1)** | Stage-0 rỗng → chạy 5 bước **1 lần** trên ảnh đầu | DG1 |
| **(b) SELF-ORDER (N≥2)** | Stage 0 tự xếp N ảnh xáo trộn → chạy 5 bước trên từng màn | DG2 (chế độ thật) |
| **(c) ORACLE-ORDER (N≥2)** | bỏ qua S0b/S0c (đưa N ảnh đã sắp đúng) → chỉ sinh hướng dẫn | DG2 (skyline ordering) |
| **(d) Tier A** | chạy **từng bước** trên màn thật của đáp án (teacher-forced) | DG2 (tham chiếu chuẩn ngành) |

**Baseline bắt buộc cho ordering:** **GOAL-ONLY** (che hết ảnh, chỉ đưa mục tiêu + nhãn trong — nếu goal-only đã xếp đúng cao thì cue giao diện không phải nguồn tín hiệu) và **RANDOM-ORDER** (xếp ngẫu nhiên làm sàn). **Future-work:** AGENT-NSI (world-model có train).

→ Điểm mạnh: chỉ phải dựng & bảo trì **một** pipeline; không có nhánh thứ hai để thiết kế lại.

---

# PHẦN IV — DỮ LIỆU: 3 BỘ CHÍNH + 2 BỘ PHỤ

## 4.1. Ba bộ chính (vai cố định)

| Bộ | Vai | Vì sao | Tư cách |
|---|---|---|---|
| **MobileViews** | Màn-0 (DG1) | Bộ duy nhất có sẵn **bbox pixel** mọi nút trong VH → chấm grounding ngay | preprint arXiv ⚠️ |
| **AndroidControl** | Suy luận trật tự + Tier A (DG2) | Có **episode đa bước + thứ tự + đáp án (gold action) mỗi bước** | NeurIPS 2024 ✅ |
| **ScreenSpot(-v2)** | Đối chứng grounding | Bộ đã bình duyệt → bù điểm yếu "preprint" của MobileViews | gốc = SeeClick (ACL 2024); **v2 = bản làm sạch kèm OS-Atlas, ICLR 2025** ✅ |

**Chi tiết & con số (đã kiểm web):**
- **MobileViews** (Gao et al., arXiv:2409.14337): paper báo cáo **1.213.866 screen / 30.037 app**; **bản công khai dùng được là MobileViews-600K (~600K screen / ~20K app)**. So với Rico (~63K screen): bản 600K ≈ **9× screen** (full-set 1.2M mới ≈ 19× — phải ghi rõ đang so bản nào). Mỗi screen có ảnh + VH JSON (`viewClass`, `text/label`, `bounds[left,top,right,bottom]` pixel, cờ clickable/editable/scrollable).
  > *Ví dụ minh hoạ (cấu trúc thật, nội dung tự soạn):* `{viewClass:"Button", text:"Tra cứu nghĩa vụ thuế", bounds:[270,820,540,1010], clickable:true}` — đây KHÔNG phải record có thật trong MobileViews; giá trị node thật cần tải 1 shard mới có (xem HỘP-THẬT bên dưới).
- **AndroidControl** (Li et al., *"On the Effects of Data Scale on **UI Control** Agents"*, NeurIPS 2024, arXiv:2406.03679): **15.283 episode / 833 app**; split train **13.604 episode / 74.722 step**; **mean ~5.5 step/episode** (Table 1 ghi 4.8; tính lại trên train = 5.49); **percentile-5 = 1 step, percentile-95 = 13 step**. Có chỉ dẫn cả mức cao (chỉ goal) lẫn mức thấp (từng bước). ⚠️ Paper **không** cho histogram số episode theo từng độ dài N → **phải tự đếm** (việc tuần-1, cổng **KN**). So sánh độ dài liên bộ: **AndroidControl ~5.5 < AITW ~6.5 < Mind2Web ~7.3 action/task**.
  > *Ví dụ episode (EX-B):* goal "đặt báo thức 7:00 sáng" → **B1** TAP "Báo thức" → **B2** TAP "+" → **B3** TYPE "0700" + TAP "OK". *(phỏng theo format action thật của AndroidControl, nhưng app/giờ là nội dung tự dựng minh hoạ; EX-B là minh hoạ phỏng-theo-format — record episode THẬT = cruisedeals ở HỘP-THẬT bên dưới.)*
- **ScreenSpot** (Cheng et al., *SeeClick*, ACL 2024, arXiv:2401.10935): benchmark grounding (point-in-bbox). Bản **ScreenSpot-v2** (làm sạch ~11% nhãn sai) đi kèm **OS-Atlas (Wu et al., ICLR 2025, arXiv:2410.23218)**. Vai = **đối chứng đơn-vị point-in-bbox** của bước resolver; **KHÔNG** đối chứng pipeline đa bước.

> **Record THẬT (đã verify qua web — đối lập với các ví dụ minh hoạ tự soạn ở trên):** ba bản ghi dưới đây là *cấu trúc + giá trị thật* lấy từ tài liệu chính thức của từng bộ, để đối chiếu khi code harness chấm.
> - **AndroidControl — episode THẬT (gold dùng LÚC CHẤM, không đưa cho model lúc sinh):** goal *"On cruisedeals, view cruise schedules for a four-night trip from New York to Canada"* → **B1** `{action_type: open_app, app_name: "CruiseDeals"}` → **B2** `{action_type: click, x: 313, y: 742}` → **B3** `{action_type: swipe, direction: up}`. (Nguồn: Google Research `android_control` README.) Đây là **đáp án vàng từng bước** — dữ liệu thật của dataset; ta chỉ TỰ SOẠN phần câu hỏi khi dùng MobileViews, còn ở AndroidControl goal/action đã có sẵn.
> - **ScreenSpot — mẫu THẬT:** instruction `"close"`, bbox `[0.948, 0.144, 0.994, 0.207]` (**chuẩn hoá 0–1**, dạng `x_min, y_min, x_max, y_max`), `data_type: "icon"`, `source: "Windows"`. (Nguồn: `rootsautomation/ScreenSpot` trên HuggingFace.)
> - **MobileViews — schema THẬT:** mỗi screen = ảnh + `state_*.json` (View Hierarchy); mỗi node có `viewClass` / `text` / `bounds[left, top, right, bottom]` **pixel** / cờ `clickable`. Root bounds thật = `[0, 0, 1080, 1920]`. ⚠️ Giá trị `text` của các **node con** KHÔNG được in trong tài liệu công khai → **cần tải 1 shard** mới trích được (việc nằm trong checklist tuần 1).

> **CHỐT-BBOX — format toạ độ KHÁC NHAU giữa 3 bộ (rất dễ nhầm khi code chấm):**
>
> | Bộ | Format toạ độ | Đơn vị | Thứ tự trường |
> |---|---|---|---|
> | **MobileViews** | `bounds[left, top, right, bottom]` (ô bao bbox) | **pixel** | trái, trên, phải, dưới |
> | **ScreenSpot (HF)** | bbox `[x_min, y_min, x_max, y_max]` | **chuẩn hoá 0–1** | x-min, y-min, x-max, y-max |
> | **AndroidControl** | **toạ độ điểm click** `(x, y)` trong action (không phải ô bao) | pixel | x, y |
>
> ⚠️ **Cảnh báo convert ở harness (giống lưu ý 1c của `report/02_datasets.md`):** trước khi so point-in-bbox phải quy về cùng hệ — nhân/chia theo kích thước màn để đổi giữa pixel ↔ 0–1, và lưu ý AndroidControl cho **điểm** (cần so "điểm ∈ bbox") còn MobileViews/ScreenSpot cho **ô bao**. Sai bước convert này là lỗi chấm thầm lặng nguy hiểm nhất.

## 4.2. Hai bộ phụ

- **AITW — Android in the Wild** (Rawles et al., NeurIPS 2023, arXiv:2307.10088): **vai đôi** — (a) **nguồn ngưỡng 14% bắt buộc** cho metric Grounding@14% (định nghĩa gốc: tap khớp nếu "trong ~14% khoảng cách màn **HOẶC** cùng bounding box"); (b) dataset đối chứng (tùy chọn).
- **Mind2Web** (Deng et al., NeurIPS 2023 Spotlight, arXiv:2306.06070): nhánh **web**, để **future-work**. 2.350 task / 137 site / 31 domain, ~7.3 hành động/task; định vị bằng DOM (không có bbox pixel).

## 4.3. Hai điều phải nói thẳng với thầy

1. **MobileViews không có câu hỏi use-case** → ta **tự soạn câu hỏi** kiểu "làm sao để X" (ghi rõ protocol + số lượng trong luận văn). (ScreenQA chỉ là Q&A nội dung màn — "pin bao nhiêu %" — sai thể loại, không dùng làm câu hỏi thủ tục.)
   - **Phạm vi tự soạn chỉ là MobileViews/DG1** (màn-0). **AndroidControl và ScreenSpot ĐÃ có sẵn goal/instruction** nên KHÔNG cần soạn câu hỏi.
   - **"Tự soạn câu hỏi" ≠ "bịa đáp án".** Ta chỉ viết phần INPUT (câu hỏi) cho ảnh có sẵn; còn **đáp án để chấm — bbox/node trong VH (DG1) và gold action (DG2) — vẫn là dữ liệu thật của dataset**. Khác hẳn "sinh dữ liệu tổng hợp" (bịa ra đáp án/ground-truth) — đó là việc luận văn TRÁNH.
2. **Dataset định lượng đều là app tiếng Anh/Trung** → tiếng Việt chỉ là **động cơ (eTax) + kiểm OCR đọc dấu + demo định tính**, **không có bảng số tiếng Việt** (vì không tồn tại dữ liệu VH tiếng Việt để chấm). Pipeline/metric vốn độc-lập-ngôn-ngữ (chấm bằng toạ độ/bbox/format) nên validate trên dataset tiếng Anh là hợp lệ.

---

# PHẦN V — CÁCH CHẤM ĐIỂM (nhiều ví dụ số)

**Quy ước hướng điểm:** mọi metric quy về **"faithfulness", cao = tốt** (vd báo 1−HER thay vì HER), để khi đối chiếu với điểm người (Spearman/Kendall) không phải lật dấu.

## 5.1. DG1 — chấm tutorial màn-0 (ví dụ EX-A, eTax)

Máy nhìn ảnh eTax + câu hỏi → ra bước *"1. Bấm ③ Tra cứu nghĩa vụ thuế"* (③ ở tâm (405,915)). Lúc chấm, mở **cây UI thật (VH)** ra đối chiếu:

| Tiêu chí | Đo gì | Cách tính trên ví dụ | Kết quả |
|---|---|---|---|
| **UI Grounding** | chỗ máy bảo "bấm" có trúng ô nút thật? | **point-in-bbox**: (405,915) có nằm trong bbox nút "Tra cứu" [270,820,540,1010]? | ✅ trúng → 1.0 |
| **Hallucination** | máy có nhắc nút **không tồn tại**? | **HER** = (số nút nhắc mà vắng trong VH) / (số nút nhắc). Nếu nhắc 3 nút, 1 nút "Cài đặt" không có trong VH → HER = 1/3 ≈ 0.33 (faithfulness 0.67) | càng cao (1−HER) càng tốt |
| **Coverage** | có **bỏ sót** nút quan trọng? | mention-recall so với nút lá VH; vd VH có 5 nút liên quan, tutorial nhắc 2 → coverage 2/5 | chống "không bịa nhưng chẳng nói gì" |
| **Clarity/Format** | có đánh số 1,2,3? có động từ "Bấm/Chọn"? văn rõ? | **IFEval** (luật cứng: đánh số? động từ mệnh lệnh đầu bước? 1 action/bước?) + **G-Eval** (model chấm độ rõ 1–5) | — |

**Các quy tắc công bằng đã khoá (để kết quả vững):**
- **HER chấm so với VH (mỏ neo độc lập), KHÔNG so với tập E của chính detector** — nếu không, hệ SoM bị ép về HER≈0 do cấu trúc, baseline bị chuẩn khắt khe hơn → không công bằng. **Chấm cả hai nhánh trên CÙNG mỏ neo VH.**
- **Resolver (bước đổi câu chữ → toạ độ) phải đối xứng**: cùng một bộ matcher cho cả hai nhánh; ID→bbox lookup của SoM chỉ báo như một dòng "oracle upper-bound" riêng.
- **Tách "metric chấm" khỏi "verifier vận hành"**: V1 (membership) chỉ là *self-consistency của pipeline*, **không** dùng làm số hallucination headline.
- **Matcher** dùng kiểu **ALOHa** (embedding + Hungarian, không string-match ngây thơ), chạy EN và ZH riêng, **validate tay >80% rồi FREEZE** trước khi chấm.

## 5.2. DG2 — chấm suy luận trật tự màn (ví dụ EX-B, app Đồng hồ)

> *Vì sao đổi sang ví dụ đồng hồ?* eTax không nằm trong dataset có đáp án; AndroidControl (app tiếng Anh) có sẵn **thứ tự + chuỗi đáp án vàng** từng bước. Đáp án vàng (thứ tự đúng, giấu khỏi máy, chỉ để chấm): *màn B1 "Báo thức" → màn B2 "+" → màn B3 gõ 07:00 + OK.* *(phỏng theo format action thật của AndroidControl, nhưng app/giờ là nội dung tự dựng minh hoạ — record episode THẬT = cruisedeals ở HỘP-THẬT mục 4.1.)*

**Bài toán:** đưa cho máy **3 màn xáo trộn** (vd thứ tự nhận được là B2, B3, B1) + mục tiêu "đặt báo thức 7:00". Máy phải tự xếp lại đúng **B1 → B2 → B3** rồi sinh hướng dẫn theo thứ tự đó.

### 5.2.1. Headline = Kendall τ-b (đo độ khớp thứ tự), chấm theo thứ-tự-bộ-phận

- **Kendall τ-b** (Kendall 1938; dùng trong meta-eval Gao et al., NAACL 2025): so thứ tự máy xếp với thứ tự vàng theo **từng cặp** màn — đồng thuận nhiều thì τ-b gần +1, đảo lộn thì gần −1. **KHÔNG dùng pairwise-accuracy thô làm headline** (dễ thành tautology).
- **Chấm theo thứ-tự-bộ-phận (partial-order-aware) — quy ước BẮT BUỘC:** chỉ **PHẠT khi sai cặp BẮT BUỘC**; cặp **TỰ-DO** đảo vẫn tính **ĐÚNG**.
  - **Cặp bắt buộc** = quan hệ thứ tự thật sự (phát hiện qua cue **gating** / **drill-down**). *Ví dụ:* "đăng nhập trước → xem kết quả sau" — đảo là **sai thật**.
  - **Cặp tự-do** = thứ tự không quan trọng. *Ví dụ:* điền **Email** và **SĐT** độc lập — điền cái nào trước cũng được → đảo vẫn **đúng**.
  - **HEADLINE τ-b chỉ tính trên cặp bắt buộc.** Báo **THÊM τ-b-thô** (so toàn bộ thứ tự gốc trên mọi cặp) làm **"điểm sàn"** (robustness).
- **Metric phụ:** pairwise-order-accuracy + position-accuracy@correct-place. **Bỏ Exact-Order-Match khỏi headline** (N=3 thì EM ngẫu nhiên ~17%, N≥6 gần ~0% → không phân biệt được hệ).
- **Phạm vi N:** **loại N≤2** (N=2 chỉ có 1 cặp → τ-b chỉ nhận {−1,+1}, vô nghĩa). Trục N thực tế **N∈[3, ~10]**; **báo số episode còn lại ở mỗi mốc N** (lấy từ histogram tự đếm — cổng KN).

### 5.2.2. Chất lượng tutorial từng màn vẫn chấm đầy đủ

Sau khi xếp xong, mỗi màn vẫn chạy 5 bước → chấm grounding (point-in-bbox, SeeClick ACL 2024), hallucination (HER + coverage), format (IFEval). Mỗi số kèm **"recall detector = X% (K1)"** + báo **RAW vs ORACLE**. Đây là điểm **mạnh hơn cách đoán-mù cũ**: vì có ảnh thật của mọi màn, grounding chấm được trên **mọi bước**, không phải đoán màn chưa thấy.

### 5.2.3. ordering gap (ORACLE-ORDER vs SELF-ORDER)

- **ORACLE-ORDER (skyline):** N ảnh **đã sắp đúng** + mục tiêu → chỉ sinh hướng dẫn (model không phải tự xếp).
- **SELF-ORDER (thật):** N ảnh **xáo trộn** → tự xếp rồi mới sinh.
- **ordering gap** = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER) = **"cái giá của việc không biết trật tự".**
- **Sanity cứng:** ORACLE-ORDER ≥ SELF-ORDER ở **mọi episode** (vi phạm = bug).
- **Cảnh báo floor-effect:** gap chỉ có nghĩa nếu metric tutorial **NHẠY với thứ tự**; nếu không nhạy thì **τ-b là trục chính**, gap chỉ là phụ.

### 5.2.4. Tier A — trục tham chiếu chuẩn ngành (teacher-forced, skyline)

```
màn B1 thật → máy đoán bấm "Báo thức"  ✓
màn B2 thật → máy đoán bấm "+"          ✓
màn B3 thật → máy đoán gõ 07:00 + OK    ✓     →  3/3 đúng
```
Mỗi bước máy *được thấy màn thật của đáp án vàng* rồi đoán thao tác kế. Metric chuẩn ngành: **Action-Type** (đúng loại thao tác: click/gõ/cuộn?), **Grounding@14%** (điểm bấm lệch tâm nút ≤14% kích thước màn **hoặc** rơi trong cùng bbox — ngưỡng từ AITW), **Step-SR** (Step Success Rate: đúng cả loại + đích trong 1 bước).
> ⚠️ Tier A **không phải sản phẩm 1-ảnh** (nó được xem màn thật mỗi bước) → chỉ là **mốc tham chiếu / cận-trên**, **không** đem so bảng xếp hạng công khai (setup khác + recall detector chưa công bố rõ, tự đo ở K1). **KHÔNG còn là "đa bước chính"** — trục chính DG2 là suy luận trật tự (τ-b). ORACLE-ORDER là skyline của riêng trục ordering.

### 5.2.5. Signal-attribution — model dựa vào cue nào để xếp đúng?

Để trả lời câu hỏi thầy *"model dựa vào đâu để biết trật tự"* một cách **định lượng**, dùng **stratification cấp một-cue**: chỉ giữ những **cặp màn phân biệt được bởi ĐÚNG MỘT cue** (vd cặp chỉ khác nhau ở *gating*), rồi đo accuracy theo từng nhóm cue → biết cue nào model thật sự khai thác.
> ⚠️ **KHÔNG che pixel** để làm việc này (che pixel tạo artifact, model nhận ra vùng bị che). Thay vào đó dùng stratification + **phân tích lỗi mở** (đọc tay các cặp model xếp sai).

## 5.3. Quy ước báo số (chống đánh lừa)

- **Mọi số grounding/step kèm "điều kiện recall = X%"** (vì pipeline chỉ cite được nút đã dò — xem Phần VII).
- **Báo cả RAW và ORACLE:** **RAW** = số thật, gánh cả lỗi do detector bỏ sót nút (**lỗi nhìn**); **ORACLE** = giả định detector bắt đủ 100% nút (chỉ còn **lỗi nghĩ** — model suy luận sai). Chênh RAW↔ORACLE = phần do "nhìn"; phần còn lại = do "nghĩ".

## 5.4. Đối chiếu với người (validate metric tự động đáng tin)

- **Best-Worst Scaling (BWS):** đưa chuyên gia tuple 4 tutorial, chọn cái **tốt nhất & tệ nhất**; điểm = (#best − #worst)/#xuất hiện ∈ [−1,1].
- **Độ đồng thuận giữa người chấm:** Krippendorff α / Fleiss κ.
- **Tương quan auto-vs-người:** Spearman ρ **+ Kendall τ-b** (bền hơn khi N nhỏ + nhiều hạng trùng) + **bootstrap CI**.
- **Đóng khung trung thực:** pilot này là **sanity-check/feasibility** (N nhỏ → CI rộng), **không** "chứng minh metric khớp người" tuyệt đối. Phát biểu **theo hướng** ("metric & người đồng thuận thứ tự tutorial rõ-tốt vs rõ-hỏng"), không ra 1 con ρ điểm. Kỳ vọng N ≥ 60–80 item.

---

# PHẦN VI — THÍ NGHIỆM KHOA HỌC: THANG BẬC C0→C4

Không so kiểu "hệ đầy đủ vs hệ trần" một phát (vì hệ thêm nhiều món một lúc, thắng cũng không biết nhờ món nào). Thay vào đó **thêm từng món, đo từng nấc** để biết **cơ chế nào thực sự trả công**:

| Nấc | Cấu hình | Cô lập điều gì |
|---|---|---|
| **C0** | VLM trần, không tự sửa | sàn thô |
| **C1** | + tự sửa (self-refine) | **baseline/control chính** |
| **C2** | + đánh số (Set-of-Mark), chưa ép, chưa V1 | *vẽ số* một mình có ích không? |
| **C3** | + ép chỉ-chọn-số (constrained) + verifier tồn-tại V1 | đóng góp **cấu trúc/membership** |
| **C4** | + intent-critic V2 (= hệ đầy đủ) | đóng góp **intent** |

→ Báo **delta C1→C2→C3→C4**. *Ví dụ cách đọc (số giả định minh hoạ):* nếu HER giảm C1→C2 = −2 điểm (vẽ số một mình ít tác dụng), C2→C3 = −9 (ép + verifier là cơ chế trả công chính), C3→C4 = −1 (intent-critic gần như không thêm cho hallucination) → kết luận: **lợi ích đến từ bậc C3**. Đây là kiểu kết luận mà một A/B đơn không đưa ra được.

**Điều kiện công bằng (khoá nguyên văn):** cùng base VLM, cùng số lần tự sửa (K=2), cùng output schema, cùng resolver chấm; self-refine critic giống hệt giữa C1 và C4. **Ma trận chống lỗi-chung:** generator ≠ intent-critic ≠ judge-hallucination (text-only, nuốt VH, không xem ảnh) ≠ judge-G-Eval (4 họ model khác nhau). Pin **một build OmniParser** duy nhất cho cả K1 lẫn nhánh SoM.

*Lưu ý phạm vi:* delta C1→C4 thuộc **bảng DG1 (màn-0)**; đa bước có **bảng kết quả riêng (DG2)**.

---

# PHẦN VII — TÍNH KHẢ THI + KILL-TEST TUẦN 1

## 7.1. Phán quyết: 🟢 GO — nhưng THU HẸP phạm vi

Phần lõi (đánh giá neo VH cho `ảnh+câu hỏi → tutorial`, cộng ablation SoM-Tutor vs E2E) dựng hoàn toàn từ component có sẵn, **không cần fine-tune** (OmniParser V2, Set-of-Mark, Qwen2.5-VL-7B trên 1 GPU 24GB, constrained decoding / Structured Outputs, verifier membership). Chi phí sàn **~$100–300** (ước tính; đẩy judge sang gpt-4o-mini + Batch API; dev set 50–100 item, full chỉ cho bảng cuối).

## 7.2. Rủi ro số 1 (tồn vong): trần recall của bộ dò

Cả hệ **chỉ giỏi bằng bước dò nút**: nút bị bỏ sót thì model **không bao giờ cite được**, dù thông minh tới đâu.
> **Lưu ý trung thực (đã kiểm web):** recall *phát hiện element* của OmniParser trên UI mobile dày **chưa được công bố rõ**; nguồn chỉ có *grounding accuracy* ~57% trên ScreenSpot (là chỉ số KHÁC, không phải recall). **Giả thuyết làm việc:** có thể chỉ ~một nửa element được dò. → **Việc đầu tiên tuần 1 = TỰ ĐO recall (kill-test K1).** Mọi số grounding ghi kèm "điều kiện recall = X%". Nếu thấp → đổi cách phát biểu thành "grounding *trong giới hạn khả năng dò*" (vẫn là đóng góp), **không bỏ đề tài**.

## 7.3. Các kill-test (chạy ≤1 tuần trước khi chốt với thầy)

| Kill-test | Đo gì (ví dụ) | Ngưỡng đạt |
|---|---|---|
| **K1 (CỔNG CỨNG)** — recall detector | OmniParser trên 30–50 màn; vd dò 22/40 nút → recall 55% | nếu < ~80% → đổi khung "recall-conditioned" + thêm metric false-negative |
| **KN (CỔNG CỨNG)** — histogram độ dài | tự đếm số episode AndroidControl theo từng N (đã khảo sơ bộ: mean ~5.5, p95=13) | đủ episode ở N∈[3,~10] để chia mốc N; thiếu → gộp mốc / thu hẹp dải N |
| **KZ' (CỔNG CỨNG)** — prior-art sắp-ảnh | rà Scholar bài toán xếp ảnh/bước xáo (Sort-Story, ACL 2022, RankGPT) | đã khảo: GO với khung claim "domain GUI + điều kiện mục tiêu + sinh tutorial + signal-attribution" (thừa nhận lineage) |
| **KB (CỔNG CỨNG)** — chống leak step-index | khi xáo trộn: strip metadata + tái mã hoá ảnh + đặt tên UUID; CI test = detector mù nhìn pixel không suy ra thứ tự tốt hơn ngẫu nhiên | nếu xếp đúng cao bất thường khi mù → có leak, phải vá |
| **K3** — OCR tiếng Việt | Qwen2.5-VL/Vintern trên 10 ảnh app VN, kiểm dấu | đọc đúng dấu (chạy ngoài luồng chính vì VN là future-work) |
| **K4** — VRAM/tốc độ | Qwen2.5-VL-7B trên 1 RTX 4090, 10 item end-to-end | đỉnh < 22GB/24GB, < ~5s/item |
| **K5** — chi phí | full pipeline trên 20 item, bật log token, nhân theo item×ablation | dự phóng ≤ ngân sách (~$300) |
| **K6** — Structured Outputs | GPT-4o enum = ID hiện tại + 1 ID giả | ID giả không bao giờ xuất hiện |
| **K7** — matcher | chấm tay point-in-bbox + HER trên 5–20 màn, so matcher | matcher khớp > 80% |
| **K8** — pilot BWS | 3 annotator trên 10 tutorial, tính Krippendorff α | α ≥ ~0.5 *(chỉ là sanity-check pilot; Krippendorff khuyến nghị ≥0.667 để kết luận, ≥0.8 chuẩn cao)* |

Tổng ~7–9 ngày-người → vừa khít "tuần 1". **Bốn cổng go/no-go cứng: K1, KN, KZ', KB.**

## 7.4. Phần cứng / ngân sách

1 GPU 24GB (RTX 4090/3090, mua hoặc thuê ~$0.3–0.5/giờ — ước tính tùy nhà cung cấp). Qwen2.5-VL-7B FP16 ~17GB. Bỏ self-host 72B. API ~$100–300 (ước tính theo bảng giá tại thời điểm viết; gpt-4o-mini rẻ hơn nhiều + Batch API giảm chi phí — kiểm lại giá hiện hành trước khi cam kết). **Không cần train model.**

---

# PHẦN VIII — KẾ HOẠCH THỰC HIỆN: CÁC PHA CÓ CỔNG

> Pha sau **không được bắt đầu** trước khi pha trước đạt "Definition of Done" (DoD). Bốn cổng cứng = **K1, KN, KZ', KB**.

| Pha | Việc | Cổng / DoD |
|---|---|---|
| **P0 — Môi trường & pin** | dựng env; pin OmniParser (commit hash); vLLM Qwen2.5-VL-7B; xác nhận GPT-4o enum (K6); viết ma trận gán model | 7B load < 22GB (K4); enum chặn ID giả; build hash ghi lại |
| **P1 — Cổng cứng** | **K1** đo recall trên 30–50 màn; **KN** tự đếm histogram độ dài episode; **KZ'** rà prior-art sắp-ảnh; **KB** chống leak step-index | K1: có số X% (mọi caption kèm X%); KN: chốt dải N∈[3,~10] + số episode mỗi mốc; KZ': chốt khung claim "MỚI" (thừa nhận lineage Sort-Story/ACL2022/RankGPT); KB: CI no-leak đạt |
| **P2 — Harness chấm DG1 + freeze matcher** | cài point-in-bbox, HER+coverage, IFEval, G-Eval; định nghĩa lá VH chuẩn; validate matcher > 80% (K7) rồi FREEZE; nối cùng resolver vào cả 2 nhánh; soạn xong câu hỏi use-case | metric phân biệt tutorial tốt vs hỏng-cố-ý; matcher đông cứng trước khi chấm |
| **P2b — Harness chấm DG2 (suy luận trật tự)** | dựng Stage 0 (pairwise + Copeland + verifier MFAS); bộ chấm **Kendall τ-b partial-order-aware** (phát hiện cặp bắt buộc gating/drill-down) + τ-b-thô + metric phụ; **ordering gap** (ORACLE-ORDER vs SELF-ORDER); signal-attribution theo cue; giữ Tier A (Action-Type/Grounding@14%/Step-SR); báo RAW vs ORACLE | τ-b tính trên cặp bắt buộc; sanity ORACLE-ORDER ≥ SELF-ORDER mọi episode đạt; baseline GOAL-ONLY + RANDOM-ORDER chạy thông |
| **P3 — Ablation thang bậc (DEV 50–100)** | chạy C0–C4 end-to-end; chung base VLM/K/schema/resolver; K5 chiếu chi phí | 5 điều kiện chạy thông; dự phóng full sweep ≤ ~$300 |
| **P4 — Full sweep + pilot người + bảng DG2** | C0–C4 trên 500–2000 item (mọi số kèm recall=X%); pilot BWS; chạy bảng kết quả chính DG2 (τ-b theo mốc N + ordering gap + signal-attribution + Tier A) | bảng cuối DG1 + bảng ordering (τ-b/gap/cue) + Tier A + pilot đạt; chỉ VN định lượng + world-model ở future-work |

---

# PHẦN IX — LUẬN CHỨNG NGUỒN (venue từng metric/dataset)

**Khung gốc kế thừa:** Chim, Ive, Liakata, *"Evaluating Synthetic Data Generation from User Generated Text"*, **Computational Linguistics 51(1):191–233, MIT Press, 2025** (bài *tạp chí* bình duyệt — KHÔNG phải "ACL 2025"). Ta **không** kế thừa bài toán sinh (họ text→text, ta image→text) mà **kế thừa khung ĐÁNH GIÁ** (Intrinsic + Extrinsic): văn bản hướng dẫn LLM sinh ra = "synthetic text" cần đánh giá khi không có đáp án chuẩn.

**Ánh xạ Chim → 4 tiêu chí:** Meaning preservation → UI Grounding + Hallucination; Style preservation → Clarity/Format; Divergence (khoảng cách tới corpus tham chiếu) → tái diễn giải thành Diversity/chống-lặp-khuôn (hoặc nêu out-of-scope vì reference-free không có corpus tham chiếu); Extrinsic → Task Success (DG2).

**Bộ metric & venue (đã web-verify):**

| Tiêu chí | Metric chính | Nguồn (đã kiểm) | Dùng để |
|---|---|---|---|
| Grounding | Point-in-BBox | SeeClick, **ACL 2024** | điểm bấm có rơi trong bbox nút thật |
| Grounding (phụ) | IoU | PASCAL VOC (Everingham, **IJCV 2010**) | partial-credit khi model xuất box |
| Hallucination | HER (từ CHAIR) | **EMNLP 2018** | tỷ lệ nút nhắc mà vắng trong VH |
| — bù recall | Coverage (VALOR-EVAL) | **Findings of ACL 2024** | có bỏ sót nút quan trọng không |
| — khớp tên | ALOHa (embedding + Hungarian) | **NAACL 2024** | khớp đồng nghĩa, tránh dương-tính-giả |
| — quan hệ/thứ tự | FActScore | **EMNLP 2023** | claim "X nằm dưới Y" có đúng không |
| — VLM-native | FaithScore | **Findings of EMNLP 2024** | fact mô tả trung thành với ảnh |
| — triangulate | SelfCheckGPT / POPE / SummaC / FactCC / QAGS / HaluEval | EMNLP 2023 / EMNLP 2023 / **TACL 2022** / EMNLP 2020 / ACL 2020 / EMNLP 2023 | đối chiếu chéo, không cộng dồn |
| Clarity/Format | IFEval (cứng) | arXiv 2023 (chuẩn rộng) | luật định dạng kiểm bằng máy |
| Clarity (mềm) | G-Eval | **EMNLP 2023** | model chấm độ rõ (lưu ý ρ~0.514 SummEval — phải tự-validate) |
| Trật tự (headline DG2) | **Kendall τ-b** (partial-order-aware) + pairwise-order-acc + position-acc | Kendall **1938** + Gao et al. **NAACL 2025** | đo độ khớp thứ tự màn |
| Tham chiếu (Tier A) | Action-Type / Grounding@14% / Step-SR | AndroidControl **NeurIPS 2024** / OS-Atlas **ICLR 2025**; ngưỡng 14% từ AITW **NeurIPS 2023** | mốc tham chiếu chuẩn ngành |
| Validate người | BWS | **ACL 2017** (gốc Louviere & Woodworth **1990**) | xếp hạng tutorial |
| — đồng thuận | Krippendorff α / Cohen & Fleiss κ | Sage 1980/2004 / 1960 / 1971 | độ nhất quán người chấm |
| — tương quan | Spearman (1904) + Kendall τ-b | + Gao et al. **NAACL 2025** | auto vs người |

**Prior-art của bài toán "suy luận trật tự màn" (đã rà — cổng KZ'):** **không có công trình trùng khít**. Gần nhất:
- **Sort-Story** (Agrawal et al., **EMNLP 2016**): sắp ảnh + caption bị xáo thành câu chuyện đúng trật tự.
- **"Sequencing Multimodal Instructional Manuals"** (Wu et al., **ACL 2022**): sắp các bước hướng dẫn đa phương thức bị xáo.
- **RankGPT** (Sun et al., **EMNLP 2023**): LLM sinh permutation xếp hạng tài liệu theo query.
- Phụ trợ: Sentence-ordering (Gong et al., **AAAI 2018**), Screen2Vec (**CHI 2021**).

**Đóng khung độ mới (trung thực, KHÔNG claim "xếp ảnh xáo là mới"):** điểm mới = (a) **domain GUI màn-hình**; (b) **điều kiện hoá theo mục tiêu / use-case**; (c) gắn ordering **→ SINH tutorial** (không chỉ xếp); (d) **signal-attribution** (đo cue UI nào giúp xếp đúng). Luận văn **thừa nhận lineage** Sort-Story / ACL 2022 / RankGPT.

**Nguyên tắc credibility:** xương sống phương pháp chỉ trích **peer-reviewed** (ACL/EMNLP/NAACL/TACL/CL journal/NeurIPS/ICLR/AAAI/CHI). Công cụ (OmniParser arXiv:2408.00203, Qwen, Set-of-Mark arXiv:2310.11441, DOMINO/*"Guiding LLMs The Right Way"* ICML 2024) là preprint/kỹ thuật — chỉ là **hiện vật kỹ thuật**, không trình như đã bình duyệt. MobileViews là preprint → vá bằng ScreenSpot (ACL 2024 / OS-Atlas ICLR 2025) + AndroidControl (NeurIPS 2024).

---

# PHẦN X — VÌ SAO KẾT QUẢ XẤU VẪN ĐẬU (pre-registration)

Đóng góp chính là **quy trình đánh giá + câu hỏi khoa học có đăng ký trước**, không phải "hệ phải thắng baseline". **Pre-registration** = cam kết **giả thuyết + ngưỡng effect-size + quy tắc quyết định TRƯỚC khi chạy** (nên không thể "thua thì đổi đề").

- **DG1 null vẫn đậu:** nếu *"ràng buộc cấu trúc không cải thiện faithfulness một khi đã kiểm soát recall"* + giải thích cơ chế (recall detector chặn trần lợi ích) + đường cong recall-vs-grounding → **một null được mô tả cơ chế LÀ đóng góp**.
- **DG2 đổ dồn power vào MỘT trục = τ-b ordering.** Phải pre-register **giả thuyết bác được**: vd "**SELF-ORDER τ-b > RANDOM-ORDER** với effect-size ≥ ngưỡng đăng ký" và "**ordering gap > 0** (ORACLE-ORDER cao hơn SELF-ORDER)", kèm **ngưỡng CI-width tối đa**. Nếu τ-b không hơn random / gap không khác 0 trong CI → **DG2 FAIL có ý nghĩa** (kết luận: cue UI không đủ để model suy luận trật tự ở quy mô này, hoặc metric không nhạy thứ tự). Có vậy mới là null thật.

---

# PHẦN XI — PHẠM VI CHỐT & FUTURE-WORK

| ✅ Trong luận văn | 🔭 Future-work (vì KHÔNG có dữ liệu để chấm) |
|---|---|
| Grounding/hallucination/clarity màn-0 (DG1) | **Chấm định lượng tiếng Việt** (không tồn tại VH tiếng Việt) |
| **Suy luận trật tự màn (DG2): τ-b + ordering gap + Tier A** trên AndroidControl | **World-model tự huấn luyện** (AGENT-NSI: đoán màn kế bằng AI có train) |
| Ablation thang bậc C0–C4 + pilot người | Mở rộng **nhánh web** (Mind2Web) |

- **Ngôn ngữ chấm:** EN/ZH (MobileViews + AndroidControl). Tiếng Việt = động cơ + sanity-check OCR + demo định tính.
- **Model:** off-the-shelf, **không fine-tune**; Qwen2.5-VL-7B (chính) + tùy chọn slice GPT-4o.
- **Nền tảng:** mobile. Web = future-work.

**Nguyên tắc:** chỉ để future-work những thứ **không có dữ liệu để chấm** — đó là quyết định có cơ sở, không phải né tránh. **Suy luận trật tự màn (đa bước) KHÔNG còn là future-work** (đã có AndroidControl làm gold thứ tự + action).

---

# PHẦN XII — HỎI–ĐÁP CHUẨN BỊ CHO BUỔI BẢO VỆ

| Thầy có thể hỏi | Trả lời |
|---|---|
| **Có thực sự làm đa bước không?** | Có, và đã **đổi cách hỏi cho đúng câu hỏi của thầy "model dựa vào đâu để biết trật tự"**: DG2 là bài toán **suy luận trật tự màn** — đưa N ảnh xáo trộn + mục tiêu, model tự xếp đúng thứ tự rồi sinh hướng dẫn. Headline = **Kendall τ-b** chấm theo thứ-tự-bộ-phận. Vẫn giữ **Tier A** (teacher-forced) làm trục tham chiếu chuẩn ngành. |
| **Làm sao model biết trật tự? Dựa vào đâu?** | Em đặt tên **5 ordering cue**: gating (đăng nhập/cấp quyền trước), nav-affordance (Next/Back/breadcrumb), state-delta (off→on, ô trống→đã điền), title-progression (tiêu đề theo bước), drill-down (chi tiết của item). Rồi em **đo định lượng cue nào giúp xếp đúng** bằng signal-attribution (giữ cặp phân biệt bởi đúng một cue, đo acc theo nhóm). |
| **Tier A có "ăn gian" không (được thấy màn thật)?** | Em khai báo rõ Tier A là **teacher-forcing** = cách đo **chuẩn ngành**, đóng vai **mốc tham chiếu/skyline**, KHÔNG trình như sản phẩm 1-ảnh và KHÔNG so ngang bảng xếp hạng. Trục chính của DG2 là suy luận trật tự (τ-b); skyline của riêng trục đó là **ORACLE-ORDER**, và **ordering gap = ORACLE-ORDER − SELF-ORDER** chính là *cái giá của việc không biết trật tự*. |
| **Bài toán xếp ảnh xáo có mới không?** | Em **không** claim "xếp ảnh xáo là mới" — có lineage **Sort-Story (EMNLP 2016), Wu et al. (ACL 2022), RankGPT (EMNLP 2023)**. Độ mới của em = (a) domain GUI; (b) điều kiện hoá theo mục tiêu; (c) gắn ordering → **sinh tutorial**; (d) **signal-attribution** cue UI. |
| **OmniParser bỏ sót nửa số nút?** | Recall thật **chưa được công bố rõ** (nguồn chỉ có grounding accuracy ~57%) → em **tự đo ở kill-test K1** ngay tuần 1; mọi số kèm "điều kiện recall = X%" và báo **RAW vs ORACLE** để tách lỗi-nhìn khỏi lỗi-nghĩ. |
| **MobileViews là preprint?** | Đúng, em thừa nhận; nên ghép thêm bộ **đã bình duyệt** làm mỏ neo: **ScreenSpot** (SeeClick ACL 2024 / OS-Atlas ICLR 2025) + **AndroidControl** (NeurIPS 2024). MobileViews chỉ dùng như kho ảnh+VH; metric chấm lấy từ paper bình duyệt. |
| **Metric có tự chế không?** | Không — toàn bộ từ ACL/EMNLP/NAACL/TACL/CL journal/NeurIPS/ICLR. **Đóng góp của em là thiết kế đánh giá**, không phải metric. |
| **Đủ tầm thạc sĩ chưa?** | Có: (1) phương pháp đánh giá reference-free mới (DG1); (2) bài toán + khung đo **suy luận trật tự màn GUI** có điều kiện mục tiêu, headline τ-b + ordering gap + signal-attribution (DG2, mới); (3) thí nghiệm có kiểm soát (ablation thang bậc) + pilot người. |
| **Tiếng Việt sao không có bảng số?** | Vì **không tồn tại** dữ liệu View Hierarchy tiếng Việt để chấm tự động. Hệ **vẫn sinh hướng dẫn tiếng Việt được**; em giữ tiếng Việt ở dạng demo định tính + kiểm OCR. |
| **Kịp thời gian không?** | Linh kiện có sẵn, không train, 1 GPU + ~$100–300, lộ trình 6 pha có cổng (P0–P4 + P2b). Tuần 1 chạy kill-test (quan trọng nhất: đo recall) rồi báo lại thầy chốt cách phát biểu. |

---

# PHẦN XIII — THUẬT NGỮ BỎ TÚI

| Thuật ngữ | Nghĩa đời thường |
|---|---|
| **VLM** | Mô hình AI vừa "nhìn" ảnh vừa viết chữ (GPT-4o, Qwen2.5-VL) |
| **View Hierarchy (VH)** | Cây cấu trúc UI: danh sách mọi nút + chữ + toạ độ ô. Dùng làm "đáp án để chấm" |
| **bbox** | Ô chữ nhật bao quanh một nút (toạ độ trái-trên-phải-dưới) |
| **VH-silver** | VH "bạc" — nhãn do máy sinh tự động, đủ tin để chấm nhưng không hoàn hảo (khác "vàng" do người duyệt) |
| **Set-of-Mark** | Vẽ số ①②③ lên ảnh tại vị trí từng nút |
| **Sinh có ràng buộc** | Ép model chỉ được trả lời bằng cách chỉ vào số/ID đã có (constrained decoding / Structured Outputs) |
| **Grounding** | Chỗ máy bảo "bấm" có trúng đúng ô nút thật không |
| **Hallucination / HER** | Máy nhắc nút không tồn tại; HER = tỷ lệ bịa (báo dạng 1−HER, cao=tốt) |
| **Coverage** | Có bỏ sót nút quan trọng không (mention-recall) |
| **teacher-forcing** | Cách đo: mỗi bước đưa model **màn thật** của đáp án rồi mới hỏi → chấm từng bước độc lập |
| **Tier A** | Đo từng bước kiểu teacher-forcing → **mốc tham chiếu chuẩn ngành** |
| **Suy luận trật tự màn (DG2)** | Đưa N ảnh xáo trộn + mục tiêu → model tự xếp đúng thứ tự rồi sinh hướng dẫn |
| **Kendall τ-b** | Đo độ khớp thứ tự máy xếp vs vàng theo từng cặp (+1 đồng thuận, −1 đảo lộn) |
| **partial-order-aware** | Chỉ phạt khi sai **cặp bắt buộc** (gating/drill-down); cặp tự-do đảo vẫn đúng |
| **ordering cue** | Manh mối giúp biết trật tự: gating, nav-affordance, state-delta, title-progression, drill-down |
| **ORACLE-ORDER / SELF-ORDER** | Đưa ảnh đã sắp đúng (skyline) / tự xếp ảnh xáo (thật) |
| **ordering gap** | = ORACLE-ORDER − SELF-ORDER = cái giá của việc không biết trật tự |
| **signal-attribution** | Đo cue nào giúp model xếp đúng (giữ cặp phân biệt bởi đúng một cue) |
| **recall (của bộ dò)** | Trong 100 nút thật, bộ dò "thấy" được bao nhiêu |
| **RAW vs ORACLE** | Báo số có/không tính lỗi do dò sót → tách "lỗi nhìn" khỏi "lỗi nghĩ" |
| **Ablation thang bậc (C0–C4)** | Thêm từng cơ chế, đo từng nấc → biết món nào trả công |
| **pre-register** | Đăng ký giả thuyết + ngưỡng quyết định **trước** khi chạy |
| **kill-test** | Phép thử nhanh ≤1 ngày để loại rủi ro trước khi cam kết (4 cổng cứng: K1, KN, KZ', KB) |
| **skyline / mốc trần** | Mức trần lý tưởng để so (Tier A + ORACLE-ORDER đóng vai này) |

---

# PHỤ LỤC — BẢNG CITATION (venue + tư cách, đã web-verify)

| # | Công trình | Venue / Năm | Tư cách | Dùng cho |
|---|---|---|---|---|
| 1 | Chim, Ive, Liakata — Evaluating Synthetic Data Generation | **Computational Linguistics 51(1), 2025** (journal) | ✅ peer-reviewed | khung đánh giá gốc |
| 2 | SeeClick / ScreenSpot (Cheng et al.) | **ACL 2024** | ✅ | point-in-bbox grounding |
| 3 | ScreenSpot-v2 / OS-Atlas (Wu et al.) | **ICLR 2025** | ✅ | đối chứng grounding (bản làm sạch) |
| 4 | CHAIR (Rohrbach et al.) | **EMNLP 2018** | ✅ | HER (hallucination) |
| 5 | VALOR-EVAL (Qiu et al.) | **Findings of ACL 2024** | ✅ | coverage |
| 6 | ALOHa (Petryk et al.) | **NAACL 2024** | ✅ | matcher khớp tên |
| 7 | FActScore (Min et al.) | **EMNLP 2023** | ✅ | claim quan hệ/thứ tự |
| 8 | FaithScore (Jing et al.) | **Findings of EMNLP 2024** | ✅ | fact trung thành với ảnh |
| 9 | SelfCheckGPT / POPE / HaluEval (Li/Manakul et al.) | **EMNLP 2023** | ✅ | triangulate hallucination |
| 10 | SummaC (Laban et al.) | **TACL 2022** | ✅ | NLI faithfulness |
| 11 | FactCC (Kryściński et al.) | **EMNLP 2020** | ✅ | learned baseline |
| 12 | QAGS (Wang, Cho, Lewis) | **ACL 2020** | ✅ | QA-based faithfulness |
| 13 | IFEval (Zhou et al.) | arXiv 2023 | ⚠️ preprint (chuẩn rộng) | format compliance |
| 14 | G-Eval (Liu et al.) | **EMNLP 2023** | ✅ | clarity (model-judge) |
| 15 | AndroidControl (Li et al., *UI Control Agents*) | **NeurIPS 2024** | ✅ | gold thứ tự + action (ordering + Tier A) |
| 16 | AITW (Rawles et al.) | **NeurIPS 2023** | ✅ | nguồn ngưỡng 14% |
| 17 | Mind2Web (Deng et al.) | **NeurIPS 2023** (Spotlight) | ✅ | nhánh web (future-work) |
| 18 | MobileViews (Gao et al.) | arXiv:2409.14337 | ⚠️ preprint | kho ảnh + VH (màn-0) |
| 19 | BWS (Kiritchenko & Mohammad) | **ACL 2017** (gốc Louviere & Woodworth 1990) | ✅ | đối chiếu người |
| 20 | Correlation measures (Gao, Hu, Lin, Wan) | **NAACL 2025** (Main) | ✅ | Spearman/Kendall meta-eval |
| 21 | IoU / PASCAL VOC (Everingham et al.) | **IJCV 2010** | ✅ | grounding partial-credit |
| 22 | OmniParser (Lu et al.) | arXiv:2408.00203 (Microsoft) | ⚠️ preprint (công cụ) | dò nút từ ảnh |
| 23 | Set-of-Mark (Yang et al.) | arXiv:2310.11441 (Microsoft) | ⚠️ preprint (công cụ) | đánh số nút |
| 24 | DOMINO / *Guiding LLMs The Right Way* (Beurer-Kellner et al.) | **ICML 2024** | ✅ | constrained decoding |
| 25 | Sort-Story (Agrawal et al.) | **EMNLP 2016** | ✅ | prior-art sắp ảnh xáo (lineage DG2) |
| 26 | Sequencing Multimodal Instructional Manuals (Wu et al.) | **ACL 2022** | ✅ | prior-art sắp bước hướng dẫn xáo (lineage DG2) |
| 27 | RankGPT (Sun et al.) | **EMNLP 2023** | ✅ | prior-art LLM sinh permutation theo query (lineage DG2) |
| 28 | Sentence-ordering (Gong et al.) | **AAAI 2018** | ✅ | prior-art phụ (sắp câu) |
| 29 | Screen2Vec (Li et al.) | **CHI 2021** | ✅ | prior-art phụ (biểu diễn màn GUI) |
| 30 | Kendall τ-b (Kendall) | **Biometrika 1938** | ✅ | headline metric thứ tự (DG2) |

---

*Hết. File này tổng hợp các báo cáo 00–08 (đề cương luận văn) thành một bản đọc liền mạch. Mọi citation đã được kiểm chứng qua web; các con số "phải đo lúc chạy" (recall thật, giá API) đều được ghi rõ là ước tính/chờ kiểm. Chi tiết kỹ thuật sâu hơn xem các file gốc tương ứng trong thư mục `report/`.*
