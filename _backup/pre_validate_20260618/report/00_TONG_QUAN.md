# BÁO CÁO 00 — TỔNG QUAN "ĐỌC LÀ HIỂU" (đọc file này TRƯỚC)

> **Mục đích:** chỉ cần đọc file này là hiểu **toàn bộ** luận văn — đề tài, dữ liệu, cách máy chạy, cách chấm điểm — qua **một ví dụ xuyên suốt**. Mọi thuật ngữ đều được giải thích ngay tại chỗ. Chi tiết kỹ thuật + nguồn trích dẫn xem các báo cáo `01`–`08`.
>
> **Bản đồ nhanh:** muốn hiểu *pipeline dễ hiểu* → `03b`; *trình thầy* → `06`; *slide* → `08`; *kế hoạch chốt* → `05`.

---

## 1. Đề tài trong một câu (kèm ví dụ)

**Người dùng đưa vào:** 1 ảnh chụp màn hình + 1 câu hỏi. **Máy trả ra:** hướng dẫn bấm **từng bước** cho người đọc.

> **Ví dụ (app eTax):**
> - **Ảnh:** màn hình chính eTax (có các nút *Khai thuế*, *Nộp thuế*, *Tra cứu nghĩa vụ thuế*…).
> - **Câu hỏi:** *"Tôi muốn kiểm tra đã nộp thuế chưa thì vào đâu?"*
> - **Máy trả:** *"1. Bấm 'Tra cứu nghĩa vụ thuế'. 2. Chọn kỳ tính thuế. 3. Xem trạng thái đã/chưa nộp."*
>
> ⚠️ **Ví dụ eTax này là MINH HOẠ tự soạn (để dễ hình dung), KHÔNG phải record thật của bất kỳ dataset nào.** Các record thật (đã verify) — gồm cả format toạ độ/bbox đúng của từng bộ — xem `02_datasets`.

**Hợp đồng với người dùng:** chỉ `ảnh + câu hỏi → hướng dẫn`. Mọi xử lý bên dưới là hộp đen.

---

## 2. Vì sao khó (3 cái khó cốt lõi)

1. **Không có "đáp án mẫu".** Không ai ngồi viết sẵn tutorial chuẩn cho từng app để máy học/đối chiếu. → phải nghĩ ra cách **chấm điểm khi không có đáp án mẫu**.
2. **Máy hay "bịa" nút.** Mô hình nhìn-ảnh-viết-chữ (gọi là **VLM** — Vision-Language Model) thường bịa ra nút không tồn tại ("bấm Cài đặt" trong khi màn này không có). → phải có cơ chế **chống bịa**.
3. **Đa bước thì máy có biết đúng TRẬT TỰ các màn không?** Nhiều việc cần *bấm → mở màn mới → bấm tiếp*. Nếu ta đưa máy **nhiều ảnh của cùng một luồng nhưng để LỘN XỘN (xáo trộn)** kèm mục tiêu, liệu máy có **suy ra được thứ tự đúng** của các màn rồi viết hướng dẫn theo đúng thứ tự đó không? Đây chính là câu hỏi của thầy: *"làm sao model biết trật tự?"*

→ **Đóng góp của luận văn** nằm đúng ở chỗ giải 3 cái khó này: một **cách đánh giá** (giải #1) + một **pipeline chống bịa** (giải #2) + một **cách đo năng lực suy luận trật tự màn** (giải #3).

---

## 3. Bức tranh lớn: HAI đóng góp

Luận văn tách thành 2 nhánh, phân biệt bằng câu hỏi đơn giản: **"có sẵn đáp án đúng để so hay không?"**

| | **Đóng góp 1 (DG1)** | **Đóng góp 2 (DG2)** |
|---|---|---|
| Đo gì | Tutorial trên **màn hình thấy được (màn-0)** | **Suy luận trật tự màn** (Screen-Order Inference): N ảnh **xáo trộn** + mục tiêu → tự xếp thứ tự rồi sinh hướng dẫn |
| Có đáp án mẫu? | **Không** có tutorial mẫu của người → tự nghĩ cách chấm | **Có** thứ tự vàng từng bước (từ dataset AndroidControl) |
| Chấm bằng | **View Hierarchy (VH — xem §5)** = cây cấu trúc UI có sẵn toạ độ mọi nút | So thứ tự máy xếp với **thứ tự vàng**, chấm **theo thứ-tự-bộ-phận** (chỉ phạt cặp BẮT BUỘC) — xem §6 |
| Tính chất | Cách đánh giá *mới* khi thiếu đáp án | Bài toán **suy luận trật tự** (mới) + **Tier A** *chuẩn ngành* làm trục tham chiếu (xem §6) |

> **Lưu ý "reference-free":** ở DG1 ta nói "không cần đáp án mẫu" theo **nghĩa hẹp** = không có *tutorial do người viết*. Nhưng **vẫn có** một mỏ neo để chấm: **View Hierarchy (VH-silver)** — "bạc" vì nó do máy sinh tự động (đủ tin để chấm nhưng không hoàn hảo như vàng-do-người-duyệt).

---

## 4. Pipeline: biến bài "tự luận" thành "trắc nghiệm"

**Ý tưởng chống bịa (1 câu):** thay vì để máy tự do viết (dễ bịa nút), ta **đánh số mọi nút thấy trên ảnh rồi ÉP máy chỉ được "chỉ vào số"** — không có số thì không nhắc được, nên không bịa được.

> **CHỐT — cốt lõi chống bịa nằm ở bước SINH (bước 3), KHÔNG phải ở bước kiểm.** Cơ chế chính là **sinh có ràng buộc** (ép model chỉ được trỏ vào ID đã có trong danh sách nút phát hiện được). Bước kiểm (bước 4) chỉ là **chốt an toàn**: trong đó **V1 là so khớp thuần bằng CODE** (kiểm số máy nhắc có nằm trong tập ID thật không — KHÔNG dùng LLM), **chỉ V2 mới dùng MỘT LLM khác** (kiểm đúng-ý/intent). Đừng hiểu nhầm "verify bằng 1 LLM khác" là cơ chế chính — nó chỉ là tầng phụ; V1 (code thuần) vẫn cần làm để bảo đảm an toàn.

**Bộ định tuyến đầu vào (input router) — MỘT hệ duy nhất:**
- **N = 1 ảnh** → đơn bước (DG1 nguyên vẹn, MobileViews màn-0). Đây là **Stage-0 rỗng** → đi thẳng vào pipeline 5 bước cũ.
- **N ≥ 2 ảnh** (cùng một luồng nhưng xáo trộn) → bật chế độ **sắp-thứ-tự**: chạy **Stage 0 "Screen-Ordering"** TRƯỚC, xếp xong thứ tự rồi mới chạy pipeline 5 bước trên từng màn.

> **Trung thực với thầy:** chế độ N-ảnh là **bài toán ta ĐẶT RA để ĐO** năng lực suy luận trật tự (trả lời đúng câu hỏi của thầy *"làm sao model biết trật tự?"*) — **không** khẳng định "dán nhiều ảnh" là nhu cầu deploy phổ biến.

**Tên hệ đề xuất: ReOrder-Tutor** = Stage 0 (Screen-Ordering) + pipeline 5 bước hiện tại.

**Stage 0 — Screen-Ordering** (chi tiết: `03`):
- **S0a — đặc trưng từng màn:** TÁI DÙNG bộ parser của Stage-1/M1 (không thêm module mới).
- **S0b — bộ suy luận thứ tự (CHÍNH = pairwise-then-aggregate):** với mỗi cặp màn, hỏi VLM *"màn nào trước?"* + bắt máy trích **≥1 ordering cue** (xem dưới) → tổng hợp các phán quyết cặp bằng **Copeland score** ra thứ tự cuối. (Đối chứng chạy ngang-tài-nguyên: **listwise** = 1 lần gọi ép máy xuất luôn một hoán vị.)
- **S0c — bộ kiểm thứ tự (code thuần, KHÔNG LLM):** nếu các phán quyết cặp tạo **chu trình mâu thuẫn** → gỡ bằng xấp xỉ *min-feedback-arc-set*.
- **5 ORDERING CUES (đặt tên — trả lời thẳng câu hỏi thầy "máy dựa vào đâu để biết thứ tự"):** *gating* (đăng nhập/cấp quyền phải trước) · *nav-affordance* (nút Next/Back/breadcrumb) · *state-delta* (toggle off→on, ô trống→đã điền, badge 0→1) · *title-progression* (tiêu đề tiến theo phiếu) · *drill-down* (màn sau = chi tiết item màn trước).

Sau khi đã có thứ tự → chạy **pipeline 5 bước** dưới đây TRÊN TỪNG MÀN (chi tiết + ví dụ: `03b`):

```
ẢNH + CÂU HỎI
   │
   ▼
1. DÒ & ĐÁNH SỐ nút trên ảnh (OmniParser + OCR) → ① ② ③ ④ ⑤ …
2. VẼ SỐ lên ảnh (Set-of-Mark)
3. SINH CÓ RÀNG BUỘC: máy chỉ được chỉ vào số đã có (Qwen2.5-VL / GPT-4o)
4. KIỂM 3 TẦNG: V1 (số có thật?) → V2 (đúng ý chưa?) → V3 (sai thì tự sửa)
5. ĐỔI SỐ → TOẠ ĐỘ (để hiện cho người + để chấm điểm)
```

**Một hệ duy nhất, dùng cho cả 3 việc** (không có pipeline thứ hai):
- Sinh tutorial màn-0 (N=1) → Stage-0 rỗng, chạy pipeline 5 bước 1 lần trên ảnh.
- DG2 (N≥2) → Stage-0 xếp thứ tự, rồi chạy pipeline 5 bước **trên từng màn đã sắp** → grounding chấm **đầy đủ mọi bước** (không phải đoán mù màn chưa thấy).
- Tier A (trục tham chiếu chuẩn ngành) → chạy đúng hệ đó **từng bước** trên màn thật của đáp án vàng.

---

## 5. Dữ liệu: 3 bộ, mỗi bộ một vai

| Bộ | Vai | Vì sao | Tư cách |
|---|---|---|---|
| **MobileViews** | Màn-0 (DG1) | Bộ duy nhất có sẵn **toạ độ pixel** mọi nút trong VH → chấm grounding ngay | preprint ⚠️ |
| **AndroidControl** | Đa bước (DG2) | Có **episode đa bước + đáp án mỗi bước** → chấm Tier A/B | NeurIPS 2024 ✅ |
| **ScreenSpot-v2** | Đối chứng grounding | Bộ đã bình duyệt → bù điểm yếu "preprint" của MobileViews | ScreenSpot gốc = SeeClick (ACL 2024); v2 = bản làm sạch kèm OS-Atlas (ICLR 2025) ✅ |

*(AITW (NeurIPS 2023) đóng vai phụ: nguồn của ngưỡng dung sai 14% — xem §6. Mind2Web = nhánh web để future-work.)*

> **Record THẬT (đã verify) — 3 bộ, 3 format toạ độ KHÁC NHAU (dễ nhầm khi code chấm):**
> - **AndroidControl:** thao tác click ghi dạng toạ độ điểm `x:313, y:742` (gold action, dùng lúc chấm).
> - **ScreenSpot:** instruction "close", bbox **chuẩn hoá 0–1** `[0.948, 0.144, 0.994, 0.207]` (dạng `x_min,y_min,x_max,y_max`).
> - **MobileViews:** node VH có bounds **pixel**; root thật = `[0, 0, 1080, 1920]` (dạng `left,top,right,bottom`).
> → 3 format khác nhau (điểm vs bbox-0–1 vs bbox-pixel) — chi tiết + nguồn xem `02_datasets`.

> **2 điều phải nói thẳng với thầy:**
> 1. MobileViews **không có câu hỏi use-case** → ta **tự soạn câu hỏi** kiểu "làm sao để X". **CHỐT:** chỉ **MobileViews** (màn-0, DG1) cần tự soạn câu hỏi; **AndroidControl/ScreenSpot đã có sẵn goal/instruction** nên KHÔNG cần soạn. "Tự soạn" = chỉ viết phần **INPUT (câu hỏi)** cho ảnh có sẵn; **đáp án chấm (VH bbox / gold action) VẪN là dữ liệu thật từ dataset** — KHÔNG bịa đáp án (khác hẳn "sinh dữ liệu tổng hợp" mà luận văn tránh).
> 2. Dataset định lượng đều là app **tiếng Anh/Trung** → tiếng Việt chỉ là **động cơ (eTax) + demo định tính**, không có bảng số tiếng Việt (vì không tồn tại dữ liệu VH tiếng Việt để chấm).

---

## 6. Cách chấm điểm — chạy ví dụ từ đầu tới cuối

### 6a. Chấm màn-0 (DG1) — ví dụ eTax

Máy nhìn ảnh eTax + câu hỏi "kiểm tra đã nộp thuế chưa?" → ra bước *"1. Bấm ③ Tra cứu nghĩa vụ thuế"* (③ ở toạ độ tâm (405, 915) — *ví dụ minh hoạ tự soạn, không phải record thật*).
Lúc chấm, ta mở **cây UI thật (VH)** của ảnh đó ra đối chiếu:

| Tiêu chí | Cách tính trên ví dụ | Kết quả |
|---|---|---|
| **Grounding** (point-in-bbox) | Điểm (405,915) có nằm trong ô nút "Tra cứu" thật không? | ✅ trúng → 1.0 |
| **Hallucination** (1−HER) | Trong các nút máy nhắc, bao nhiêu cái **không có** trong VH? | 0 nút bịa → 1.0 |
| **Coverage** | Có bỏ sót nút quan trọng không? | (đo recall) |
| **Clarity/Format** | Có đánh số 1,2,3? Có động từ "Bấm/Chọn"? Văn rõ không? | IFEval + G-Eval |

*(Số liệu eTax trong bảng trên là **minh hoạ tự soạn**; **cách chấm là thật** — đúng quy trình point-in-bbox / HER / recall sẽ chạy trên record thật của dataset.)*

> *Nếu máy bịa:* giả sử nó viết "Bấm **Cài đặt** rồi chọn Tra cứu" — "Cài đặt" không có trong VH → HER = 1/2 = 0.5 (bịa 1 nút — *vẫn là ví dụ minh hoạ, không phải record thật*). Đây đúng là lỗi ta muốn bắt.

### 6b. Chấm đa bước (DG2) — suy luận trật tự màn, ví dụ "đặt báo thức 7h" (app Đồng hồ, AndroidControl)

> *Vì sao đổi ví dụ?* eTax không nằm trong dataset có đáp án; AndroidControl (app tiếng Anh) có sẵn **thứ tự vàng** từng bước, nên dùng để đo suy luận trật tự. Thứ tự vàng (giấu khỏi máy, chỉ để chấm):
> *B1 bấm tab "Báo thức" → B2 bấm nút "+" → B3 gõ 07:00 rồi "OK".*

DG2 đưa máy **N ảnh của luồng này nhưng ĐÃ XÁO TRỘN** (ví dụ thứ tự đầu vào là B2, B3, B1) + mục tiêu *"đặt báo thức 7h"*. Máy phải **(1) tự suy ra thứ tự đúng** rồi **(2) sinh hướng dẫn theo thứ tự đó**.

**Hai chế độ để bóc tách "biết-thứ-tự" khỏi "viết-hướng-dẫn":**

**ORACLE-ORDER — "đưa sẵn thứ tự đúng" (mốc trần / skyline):**
N ảnh **đã sắp đúng** + mục tiêu → máy chỉ phải sinh hướng dẫn, KHÔNG phải tự xếp.
```
B1 → B2 → B3 (đã đúng) → máy sinh tutorial 3 bước  →  chất lượng cao
```

**SELF-ORDER — "tự xếp rồi mới viết" (chế độ thật):**
N ảnh xáo trộn → máy tự xếp → sinh tutorial.
```
nhận {B2, B3, B1} xáo trộn → máy xếp lại: B1 → B3 → B2 (xếp sai cặp B2–B3)
                                          → tutorial theo thứ tự sai này
```

**Metric thứ tự — HEADLINE = Kendall τ-b** (nguồn: Kendall 1938 + Gao et al., NAACL 2025): đo độ tương đồng giữa thứ tự máy xếp và thứ tự vàng. KHÔNG dùng pairwise-accuracy thô làm headline (dễ thành tautology). Phụ: *pairwise-order-accuracy* + *position-accuracy@correct-place*.

**Chấm theo THỨ-TỰ-BỘ-PHẬN (partial-order-aware) — quyết định bắt buộc:** chỉ **PHẠT khi máy đảo cặp BẮT BUỘC**; cặp **TỰ-DO** (làm trước/sau đều được) đảo vẫn tính ĐÚNG. Để biết cặp nào bắt buộc → phát hiện *gating/drill-down* (trùng ordering-cues ở §4).
> *Ví dụ minh hoạ:* điền **Email** rồi **SĐT** là hai ô độc lập → đảo vẫn ĐÚNG (cặp tự-do). Nhưng *đăng nhập trước → xem kết quả sau* mà đảo thì SAI (cặp bắt buộc, do gating).

> τ-b headline **chỉ tính trên cặp bắt buộc**; báo THÊM **τ-b-thô** (so toàn bộ thứ tự gốc) làm "điểm sàn" robustness.
> **Trục N thực tế N ∈ [3, ~10]:** loại N≤2 (N=2 chỉ có 1 cặp → τ-b chỉ nhận {−1,+1}, vô nghĩa). Phải **tự đếm histogram** độ dài episode AndroidControl (việc tuần-1, cổng KN) rồi báo số episode còn lại ở mỗi mốc N.

**ordering gap = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER)** = *"cái giá của việc không biết trật tự"*.
- **Sanity cứng:** ORACLE-ORDER ≥ SELF-ORDER ở **mọi episode** (vi phạm = bug).
- **Cảnh báo floor-effect:** gap chỉ có nghĩa nếu metric tutorial NHẠY với thứ tự; nếu không, **τ-b là trục chính**, gap chỉ phụ.

**Chất lượng tutorial từng màn vẫn chấm đầy đủ** (vì SELF-ORDER xếp xong vẫn chạy pipeline 5 bước trên mọi màn): grounding (point-in-bbox, SeeClick ACL 2024), hallucination (HER + coverage), format (IFEval).

**Trục tham chiếu chuẩn ngành — Tier A (teacher-forced):** giữ làm trục thầy expect. Bộ chấm đưa **màn thật của mỗi bước** rồi hỏi máy đoán thao tác → so đáp án, dùng metric **Action-Type**, **Grounding@14%** (chỗ bấm lệch tâm nút trong 14% kích thước màn thì tính đúng — ngưỡng mượn từ AITW), **Step-SR**.
> ⚠️ Tier A **không còn là "đa bước chính"** và **không phải sản phẩm 1-ảnh** (được xem màn thật mỗi bước) → chỉ là **mốc tham chiếu**, KHÔNG đem so bảng xếp hạng (setup khác + recall detector chưa công bố rõ, tự đo ở K1). ORACLE-ORDER là skyline của trục ordering.

> **Mọi con số đều báo 2 kiểu:** **RAW** (tính cả lỗi do bộ dò bỏ sót nút) và **ORACLE** (giả định nút đã dò đúng) → tách *lỗi nhìn* (dò sót) khỏi *lỗi nghĩ* (suy luận sai). Mỗi số grounding kèm "recall detector = X% (K1)".

> **Signal-attribution (máy dựa vào cue nào để xếp đúng?):** dùng **stratification cấp một-cue** — chỉ giữ những cặp phân biệt được bởi **đúng MỘT** ordering cue, rồi đo accuracy theo từng nhóm cue (KHÔNG che pixel — che pixel tạo artifact). Kèm phân tích lỗi mở (đọc các cặp bị xếp sai). Hai baseline kiểm-soát: **GOAL-ONLY** (che hết ảnh, chỉ đưa goal + nhãn trong; nếu goal-only đã xếp cao thì cue giao diện không phải nguồn tín hiệu) và **RANDOM-ORDER**.

---

## 7. Thí nghiệm chính: "thang bậc" C0 → C4

Không so kiểu "hệ đầy đủ (C4) vs đáy thô (C0)" một phát (vì hệ thêm nhiều món một lúc, thắng cũng không biết nhờ món nào). Thay vào đó **thêm từng món, đo từng nấc** để biết *món nào thực sự có ích*:

| Nấc | Cấu hình | Trả lời câu hỏi |
|---|---|---|
| **C0** | VLM trần, viết thẳng | đáy thô |
| **C1** | + tự sửa (self-refine) | **baseline để so** |
| **C2** | + đánh số nút (Set-of-Mark) | *vẽ số* một mình có giúp không? |
| **C3** | + ép chỉ-chọn-số + kiểm tồn-tại (V1) | *ép từ-vựng-đóng* có giúp không? |
| **C4** | + kiểm đúng-ý (V2) = hệ đầy đủ | *kiểm intent* có giúp không? |

---

## 8. Rủi ro lớn nhất + "vì sao kết quả xấu vẫn ĐẬU"

- **Rủi ro sống còn:** cả hệ chỉ giỏi bằng bước **dò nút**. Tỷ lệ dò trúng (recall) của bộ dò (OmniParser) trên UI mobile dày **chưa được công bố rõ** — nguồn chỉ có *grounding accuracy* ~57% (ScreenSpot), không phải recall phát hiện element. → **Việc đầu tiên (tuần 1):** TỰ ĐO tỷ lệ dò trúng (**kill-test K1**, cổng cứng); mọi số grounding ghi kèm *"điều kiện recall = X%"*. Giả thuyết làm việc (chờ K1): có thể chỉ ~một nửa element được phát hiện.
- **Vì sao null vẫn đậu:** đóng góp chính là **quy trình đánh giá + câu hỏi khoa học đã đăng ký trước (pre-register)**, không phải "hệ phải thắng". Nếu kết quả là *"ràng buộc cấu trúc không giúp một khi đã kiểm soát recall"* — đó vẫn là **phát hiện có giải thích cơ chế** = đóng góp hợp lệ. (Tương tự, đo τ-b ordering + ordering gap là đo lường mô tả → ra kết quả dù hệ thắng hay không. Lưu ý: power dồn vào **một trục chính = τ-b ordering**.)

---

## 9. Phạm vi đã chốt

| ✅ Trong luận văn | 🔭 Future-work (vì chưa có dữ liệu để chấm) |
|---|---|
| Grounding/hallucination màn-0 (DG1) | Chấm **định lượng tiếng Việt** |
| **Suy luận trật tự màn** (DG2): SELF-ORDER vs ORACLE-ORDER + Tier A tham chiếu | **World-model tự huấn luyện** (đoán màn kế bằng AI có train) |
| Ablation thang bậc C0–C4 + pilot người | Mở rộng **nhánh web** (Mind2Web) |

---

## 10. Thuật ngữ bỏ túi

| Thuật ngữ | Nghĩa đời thường |
|---|---|
| **VLM** | Mô hình AI vừa "nhìn" ảnh vừa viết chữ (GPT-4o, Qwen2.5-VL) |
| **View Hierarchy (VH)** | Cây cấu trúc UI: danh sách mọi nút + chữ + toạ độ ô. Ta dùng làm "đáp án để chấm" |
| **bbox** | Ô chữ nhật bao quanh một nút (toạ độ trái-trên-phải-dưới) |
| **VH-silver** | VH "bạc" — nhãn do máy sinh tự động, đủ tin để chấm nhưng không hoàn hảo |
| **Set-of-Mark** | Vẽ số ①②③ lên ảnh tại vị trí từng nút |
| **Grounding** | Chỗ máy bảo "bấm" có trúng đúng ô nút thật không |
| **Hallucination / HER** | Máy nhắc nút không tồn tại; HER = tỷ lệ bịa (báo dạng 1−HER, cao=tốt) |
| **Tier A (teacher-forcing)** | Đo từng bước với **màn thật** mỗi bước → trục tham chiếu chuẩn ngành (không phải đa-bước chính) |
| **SELF-ORDER** | Đưa N ảnh **xáo trộn**, máy tự xếp thứ tự rồi sinh tutorial (chế độ thật của DG2) |
| **ORACLE-ORDER** | Đưa N ảnh **đã sắp đúng**, máy chỉ sinh tutorial → mốc trần/skyline của trục ordering |
| **Kendall τ-b** | Metric HEADLINE của DG2: độ tương đồng giữa thứ tự máy xếp và thứ tự vàng (cao=tốt) |
| **partial-order-aware** | Chấm theo thứ-tự-bộ-phận: chỉ phạt khi đảo **cặp bắt buộc**; cặp tự-do đảo vẫn đúng |
| **ordering gap** | Chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER) = cái giá của việc không biết trật tự |
| **ordering cues** | 5 manh mối giúp suy trật tự: gating · nav-affordance · state-delta · title-progression · drill-down |
| **recall (của bộ dò)** | Tỷ lệ nút thật mà bộ dò tìm ra được |
| **RAW vs ORACLE** | Báo số có/không tính lỗi do dò sót → tách "lỗi nhìn" khỏi "lỗi nghĩ" |
| **pre-register** | Đăng ký giả thuyết + ngưỡng quyết định **trước** khi chạy thí nghiệm |
| **EX-A / EX-B** | Hai ví dụ **MINH HOẠ tự soạn** trong file này (EX-A = eTax §1/§6a; EX-B = đặt báo thức §6b) — **KHÔNG phải record thật** của dataset |
| **record thật vs ví dụ minh hoạ** | *Record thật* = bản ghi có thật trong dataset (ảnh + VH/gold action + bbox đúng format), dùng để chấm; *ví dụ minh hoạ* = câu chuyện tự soạn để dễ hiểu, KHÔNG có trong dataset, không dùng làm số liệu |

---

## 11. Bản đồ tài liệu (đọc file nào khi nào)

| Cần gì | Đọc |
|---|---|
| Hiểu toàn cảnh nhanh | **file này (00)** |
| Pipeline giải thích dễ hiểu | `03b` |
| Trình bày / thuyết phục thầy | `06` (văn bản) + `08` (slide) |
| Metric + nguồn trích dẫn | `01` |
| So sánh dataset | `02` |
| Pipeline chi tiết kỹ thuật | `03` |
| Đánh giá khả thi + kill-test | `04` |
| **Kế hoạch chốt cuối (nguồn sự thật)** | `05` |
| Luận chứng sâu (venue từng metric) | `07` |
