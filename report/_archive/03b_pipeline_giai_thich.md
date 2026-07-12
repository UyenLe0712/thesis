# PIPELINE — GIẢI THÍCH DỄ HIỂU (cách làm)

> Bản này giải thích pipeline ở Báo cáo 3/5 bằng **một ví dụ chạy xuyên suốt** (app eTax), ngôn ngữ đời thường.
> Đọc xong là hình dung được "làm cái gì, bằng tool nào, ra cái gì". Chi tiết kỹ thuật/khoá → xem `03_pipeline.md` + `05_final_plan.md`.
> *(Bản đồ đối chiếu tên gọi với `03_pipeline.md` đặt ở cuối mục 4½, sau khi đã hiểu 3 kiểu chạy.)*

---

## 0. Bài toán trong 1 câu + ví dụ

**Người dùng đưa vào:** 1 ảnh chụp màn hình + 1 câu hỏi. **Máy trả ra:** hướng dẫn bấm từng bước.

> **Ví dụ xuyên suốt cả bài _(ví dụ minh hoạ, KHÔNG phải record thật)_:**
> - **Ảnh:** màn hình chính app eTax (có các nút: *Khai thuế*, *Nộp thuế*, *Tra cứu nghĩa vụ thuế*, *Thông báo*, *Cá nhân*…).
> - **Câu hỏi:** "Tôi muốn kiểm tra đã nộp thuế chưa thì vào đâu?"
> - **Mong muốn ra:** *"1. Bấm 'Tra cứu nghĩa vụ thuế'. 2. Chọn kỳ tính thuế. 3. Xem trạng thái đã nộp/chưa nộp."*
>
> ⚠️ **Đây là ví dụ TỰ SOẠN để minh hoạ luồng chạy** (gọi là EX-A): app eTax **không** nằm trong bộ dữ liệu có View Hierarchy thật mà ta tải về (MobileViews/AndroidControl/ScreenSpot). Mọi con số trong ví dụ này (bbox `[270,820,540,1010]`, điểm click `(405,915)`…) là **bịa ra cho dễ hình dung cách chấm**, **không** phải bản ghi có thật trong MobileViews. Giá trị node thật của MobileViews phải tải 1 shard mới có (việc trong checklist). Dùng ví dụ này chỉ để **hình dung luồng**.

**Ràng buộc xương sống:** lúc chạy thật máy **chỉ thấy ảnh + câu hỏi**. Nó **không** được xem "cây cấu trúc UI" (View Hierarchy — danh sách chính xác mọi nút + toạ độ). Cây đó **chỉ dùng lúc chấm điểm** để biết máy đúng/sai.

> ⚠️ **Phân biệt "hợp đồng sản phẩm" và "cách đo" (rất quan trọng, đừng nhầm):**
> - **Hợp đồng sản phẩm có một CÔNG TẮC ĐẦU VÀO (input router):**
>   - **Đưa vào 1 ảnh (N=1)** → ra hướng dẫn **đơn bước/màn-0** (đúng DG1 cũ, nguyên vẹn).
>   - **Đưa vào N≥2 ảnh (XÁO TRỘN) của cùng một luồng** → bật **chế độ sắp-thứ-tự**: máy phải **(1) tự suy ra trật tự đúng của các màn, (2) sinh hướng dẫn theo trật tự đó** (đây là DG2 — **suy luận trật tự màn / Screen-Order Inference** — xem mục 4½). N=1 chỉ là trường hợp riêng (Stage-0 rỗng) → chạy về pipeline cũ. **Vẫn chỉ MỘT hệ duy nhất.**
> - **Trung thực với thầy:** chế độ N-ảnh là **bài toán ta cố tình đặt ra để ĐO năng lực suy luận trật tự màn hình** (trả lời đúng câu hỏi của thầy "làm sao model biết trật tự các màn?"), **không** khẳng định đây là nhu cầu deploy phổ biến.
> - **Khi ĐO năng lực đa bước theo chuẩn ngành (gọi là Tier A — xem mục 4½)**, ta **cố tình cho model xem màn hình thật của từng bước** (như thể có người mở sẵn màn kế cho nó). Đây chỉ là **phương pháp đo** để có một mốc tham chiếu — **không** làm đổi sản phẩm, **không** phải năng lực mà sản phẩm hứa hẹn.

---

## 1. Ý tưởng cốt lõi (giải thích bằng ẩn dụ)

Vấn đề lớn nhất: nếu cho VLM (model nhìn ảnh + viết chữ) tự do viết, nó hay **bịa nút không tồn tại** ("bấm nút Cài đặt" trong khi màn này không có nút đó).

**Mẹo:** biến bài **tự luận** thành bài **trắc nghiệm**.
- Trước tiên, một bộ dò **đánh số mọi nút thấy được trên ảnh**: ① Khai thuế, ② Nộp thuế, ③ Tra cứu nghĩa vụ thuế, ④ Thông báo, ⑤ Cá nhân…
- Rồi **ép** model chỉ được trả lời bằng cách **chỉ vào số** ("bước 1 → bấm ③"), **không được** nhắc nút nào ngoài danh sách.
- → Model **không thể bịa** nút, vì nó chỉ được chọn trong các số đã có. Đây gọi là **Set-of-Mark** (gắn nhãn số) + **sinh có ràng buộc**.

> **Vì sao "vẽ số" chứ không bắt máy tự chỉ toạ độ / đọc danh sách bbox?** Model nhìn-ảnh-viết-chữ **rất dở khi phải tự phun ra toạ độ (x,y)** — hay lệch/bịa. Cho nó *chọn một số* trong danh sách thì (a) dễ hơn nhiều, (b) **ép được** chỉ chọn nút CÓ THẬT (số là tập đóng {1..N}); còn toạ độ tự do thì rơi vào đâu cũng được, không chặn bịa được. *bbox vẫn được giữ* — nhưng để **chấm điểm** (tra số → bbox), không phải để model tự sinh.
> **Vì sao OmniParser?** Lúc chạy thật KHÔNG có cây cấu trúc (View Hierarchy), nên cần bộ **dò nút thuần từ ảnh** — OmniParser làm đúng việc đó, có sẵn, không cần huấn luyện. Nó **không hoàn hảo** (dò sót khá nhiều — xem mục 5), nên là *linh kiện thay được*, không phải lõi đề tài.

> 🔑 **Chốt cốt lõi (đừng hiểu nhầm cơ chế chính):** cái khiến model **"không bịa được"** đến từ **bước SINH bị ép trắc nghiệm** (BƯỚC 3 — chỉ được chỉ vào ID đã có trong E), **KHÔNG** phải từ bước kiểm. **Bước kiểm 3 tầng (BƯỚC 4) chỉ là lưới an toàn phía sau**, trong đó **chỉ V2 dùng "model khác"**, còn **V1 là máy tính thuần** (so khớp danh sách, không có AI). Vì sao vẫn cần V1 dù bước 3 đã chặn? — vì nó là **chốt an toàn / hậu kiểm**: bắt các trường tự do (vd phần văn bản model viết kèm, hoặc trường hợp ép sinh bị lỏng/lỗi) còn lọt số ngoài danh sách, để bảo đảm tất định 100% ở mức ID.

---

## 2. Pipeline đi từng bước (theo ví dụ)

```
ẢNH (eTax)  +  CÂU HỎI ("kiểm tra đã nộp thuế chưa?")
        │
        ▼
[BƯỚC 1] DÒ NÚT TỪ ẢNH  →  đánh số ① ② ③ ④ ⑤ … (OmniParser + OCR)
        │   ra: bảng E = { ③: (chữ "Tra cứu nghĩa vụ thuế", toạ độ ô, là-nút) , … }
        ▼
[BƯỚC 2] VẼ SỐ LÊN ẢNH  →  ảnh-có-nhãn (Set-of-Mark)
        │
        ▼
[BƯỚC 3] MODEL SINH HƯỚNG DẪN  →  nhưng CHỈ được chỉ vào số trong E (Qwen2.5-VL)
        │   ra: "1. bấm ③ | 2. chọn kỳ | 3. xem trạng thái"
        ▼
[BƯỚC 4] KIỂM TRA 3 TẦNG (chống bịa)
        │   V1: mọi số nó nhắc có trong E không?  (chắc chắn, máy tính thuần)
        │   V2: số ③ có ĐÚNG là cái cần cho câu hỏi không? (model khác kiểm)
        │   V3: nếu sai → bảo nó sửa, tối đa 2 lần
        ▼
[BƯỚC 5] ĐỔI SỐ → TOẠ ĐỘ/CHỮ  →  hướng dẫn cuối + "③ nằm ở ô toạ độ (405,915)"
        │
        └······ (CHẤM ĐIỂM, offline) so với cây UI thật của MobileViews
```

### Bước 1 — Dò nút từ ảnh (tool: **OmniParser** + OCR)
- **Làm gì:** đưa ảnh vào, nó trả về **mọi vùng bấm được** + **chữ trên đó** + **ô bao (toạ độ)**, rồi đánh số.
- **Ra:** bảng `E` = `{ ①Khai thuế, ②Nộp thuế, ③Tra cứu nghĩa vụ thuế (ô [270,820,540,1010], là-nút), ④Thông báo, ⑤Cá nhân }` *(số liệu minh hoạ — xem nhãn EX-A ở mục 0)*.
- **Vì sao quan trọng:** đây là **toàn bộ "vốn từ"** mà model được phép dùng ở bước 3. **Nút nào không dò ra ở đây thì vĩnh viễn không nhắc được** → (đây cũng là rủi ro lớn nhất, xem mục 5).
- **Tiếng Việt:** OCR mặc định **dự kiến hay rớt dấu** (kiểm ở kill-test K3) → thay bằng **Qwen2.5-VL / Vintern** đọc chữ Việt.

### Bước 2 — Vẽ số lên ảnh (tool: **Set-of-Mark**, ~30 dòng code)
- **Làm gì:** vẽ các số ① ② ③… đè lên ảnh tại đúng vị trí nút. Chỉ là vẽ hình + ghi số.
- **Vì sao:** để model "nhìn thấy" số mà chỉ vào, thay vì phải tự tả vị trí.

### Bước 3 — Model sinh hướng dẫn có ràng buộc (tool: **Qwen2.5-VL-7B** hoặc **GPT-4o**)
- **Làm gì:** đưa *ảnh-có-số + bảng E + câu hỏi* cho model; nó viết hướng dẫn, **mỗi bước phải chỉ vào 1 số trong E**.
- **"Ràng buộc" làm sao ép được:**
  - Bản **chạy máy nhà** (Qwen): dùng *constrained decoding* (Outlines/XGrammar) — chặn không cho model "nói" ra số ngoài danh sách.
  - Bản **API** (GPT-4o): dùng *Structured Outputs* — bắt nó trả JSON với trường `số` chỉ nhận giá trị trong {①..⑤}. **Cả hai đều đảm bảo 100% không nhắc SỐ/ID ngoài danh sách** (đây là rào tất định ở mức từ-vựng; **không** khử được lỗi MÔ TẢ sai ý — vd chỉ đúng số ③ nhưng diễn giải sai chức năng — đó là việc của V2).
- **Ra:** `[{bước 1, action: bấm, số: ③}, {bước 2, …}]`.

### Bước 4 — Kiểm tra 3 tầng (chống bịa)
| Tầng | Hỏi gì | Bằng cách nào | Bắt được lỗi gì |
|---|---|---|---|
| **V1** | "Số nó nhắc có trong E không?" | so khớp danh sách, **máy tính thuần, không cần AI** | nhắc số không tồn tại *(thực ra bước 3 đã chặn rồi nên V1 gần như luôn đạt — V1 chỉ là chốt an toàn)* |
| **V2** | "Số ③ có **đúng** là cái cần cho câu hỏi không?" | một **model KHÁC (≠ generator ở bước 3) đọc lại**, đối chiếu | chọn **đúng định dạng nhưng sai ý** (vd chỉ vào ② "Nộp thuế" thay vì ③ "Tra cứu") |
| **V3** | (nếu V1/V2 báo sai) | bảo model sửa, **tối đa 2 lần** rồi dừng | tự sửa lỗi |

### Bước 5 — Đổi số → toạ độ/chữ
- **Làm gì:** tra bảng `E`: số ③ → tâm ô [270,820,540,1010] = toạ độ click **(405,915)** + chữ "Tra cứu nghĩa vụ thuế".
- **Vì sao:** để (a) hiển thị hướng dẫn cho người đọc, và (b) **chấm điểm** được (so toạ độ với cây UI thật).

---

## 3. Chấm điểm thế nào (giải thích bằng ví dụ)

Lúc chấm (offline) ta **mở cây UI thật** của MobileViews (có toạ độ chuẩn mọi nút) để đối chiếu:

- **Grounding (point-in-bbox):** toạ độ của ③ mà máy chỉ, có **nằm trong ô** của nút "Tra cứu" thật không? → **trúng/trật**.
- **Hallucination (HER):** trong các nút máy nhắc, **bao nhiêu cái KHÔNG có** trong cây UI thật? → tỷ lệ bịa. *(Cao = tốt khi báo dạng 1−HER.)*
- **Coverage:** máy có **bỏ sót** nút quan trọng không? (chống kiểu "không bịa nhưng cũng chẳng nói gì").
- **Format (IFEval):** có đánh số 1,2,3? mỗi bước có động từ ("bấm", "chọn")? → kiểm bằng luật, không cần AI.
- **Clarity (G-Eval):** một model chấm điểm độ rõ ràng 1–5.

> 📐 **Mọi con số báo theo 2 cách — để tách "lỗi nhìn" (dò sót) khỏi "lỗi nghĩ" (suy luận sai):**
> - **RAW** = tính trên đúng những nút mà bộ dò bắt được (gánh cả lỗi dò sót). *Ví dụ:* màn có 40 nút, detector chỉ thấy 22 → grounding chấm trên 22 nút đó, 18 nút bị bỏ sót coi như trượt.
> - **ORACLE** = **giả định detector bắt đủ 100% nút** (cho sẵn đủ 40 nút) → đo riêng phần "suy luận" của model, không bị bộ dò kéo xuống. *Ví dụ:* vẫn 40 nút nhưng coi như đã có đủ, chỉ chấm xem model **chọn** đúng nút không.

> 🧭 **Hai loại "mỏ neo để chấm" — khác bản chất, đừng gộp:**
> - **Mỏ neo loại 1 — cây UI silver (MobileViews), cho màn-0:** cây UI được sinh tự động (gọi là *silver* — bạc, tức "khá tốt nhưng không phải chuẩn vàng do người duyệt"). Nó cho ta toạ độ mọi nút để chấm grounding/hallucination **trên một màn hình duy nhất**. Đây **không** có "đáp án từng bước do người soạn".
> - **Mỏ neo loại 2 — đáp án vàng từng bước (AndroidControl, NeurIPS 2024 D&B), cho đa bước:** mỗi *episode* (một chuỗi thao tác hoàn chỉnh từ đầu đến đích) có sẵn **thao tác đúng ở từng bước** do bộ dữ liệu cung cấp. Vì có "đáp án vàng" nên đây là **chấm có-tham-chiếu (reference-based)** — so trực tiếp thao tác máy đoán với thao tác đúng.
> - **Khác biệt cốt lõi:** loại 1 chấm *một màn* bằng cây UI bạc; loại 2 chấm *cả chuỗi bước* bằng đáp án vàng. Tier A (mục 4½) dùng loại 2.

> ✍️ **"Tự soạn câu hỏi" ≠ "bịa đáp án" (CHỐT — đừng nhầm với sinh dữ liệu tổng hợp):**
> - **Với MobileViews (dùng cho DG1 màn-0):** bộ này **chỉ có ảnh + cây UI, KHÔNG kèm câu hỏi use-case** → ta phải **tự viết phần CÂU HỎI** cho ảnh có sẵn (vd nhìn ảnh eTax rồi đặt câu "kiểm tra đã nộp thuế chưa?"). Nhưng **ĐÁP ÁN để chấm vẫn là cây UI / bbox THẬT** của dataset — ta **không** bịa đáp án.
> - **Với AndroidControl và ScreenSpot:** **cả câu hỏi (goal/instruction) lẫn đáp án (gold action / bbox) đều có sẵn** trong dataset → **không tự soạn gì cả**.
> - **Ranh giới quan trọng:** "tự soạn câu hỏi" = chỉ viết phần **INPUT** cho ảnh có sẵn; **KHÁC HẲN** "sinh dữ liệu tổng hợp" (bịa ra cả đáp án / ground-truth) — việc luận văn **TRÁNH**. Đáp án chấm luôn là dữ liệu thật từ bộ dữ liệu.

---

## 4. Làm sao biết pipeline này CÓ ÍCH? — Thí nghiệm "thang bậc"

Không so kiểu "hệ của tôi vs hệ trần trụi" (vì hệ mình thêm 4 món một lúc, thắng cũng không biết nhờ món nào). Thay vào đó **thêm từng món, đo từng nấc**:

| Nấc | Cấu hình | Trả lời câu hỏi |
|---|---|---|
| **C0** | model trần, viết thẳng | đáy thô |
| **C1** | + tự sửa (self-refine) | **đây là "baseline" để so** |
| **C2** | + vẽ số lên ảnh (chưa ép) | *vẽ số* một mình có giúp không? |
| **C3** | + ép chỉ chọn số + kiểm tra V1 | *ép từ-vựng-đóng* có giúp không? |
| **C4** | + kiểm intent V2 (= hệ đầy đủ) | *kiểm đúng-ý* có giúp không? |

→ Nhìn mức tăng/giảm **C1→C2→C3→C4** là biết **chính xác món nào trả công**. Đây là phần "khoa học" của luận văn.

> 📌 **LÕI/Gọn chỉ chạy 3 bậc {C1, C3, C4}**; **C0** (sàn thô) và **C2** (Set-of-Mark một mình) = **MỞ RỘNG/ĐỐI CHỨNG**, chạy thêm nếu ngân sách cho phép. (Bảng C0–C4 vẫn giữ nguyên ở trên.)

> ⚖️ **Công bằng:** cả các nấc dùng **cùng model nền, cùng số lần sửa, cùng cách chấm**. Và **chấm cả hai bên trên cùng cây UI thật** (không bên nào được "sân nhà").

---

## 4½. Cùng một pipeline chạy ba kiểu (vẫn chỉ MỘT hệ)

Điểm dễ hiểu lầm nhất: nhìn vào tưởng có ba hệ khác nhau. **Không** — chỉ có **một** hệ SoM-Tutor ở mục 2. Ta đem **đúng hệ đó** ra chạy **ba kiểu đo khác nhau**. Quay lại ví dụ eTax cho dễ hình dung:

### Kiểu 1 — Tutorial màn-0 (chạy 1 lần, đây là sản phẩm)
- **Làm gì:** đưa **1 ảnh màn hình chính eTax** + câu hỏi "kiểm tra đã nộp thuế chưa?". Hệ chạy 5 bước (mục 2) **một lần** → ra hướng dẫn.
- **Chấm thế nào:** dùng cây UI bạc của MobileViews (mỏ neo loại 1 ở mục 3) — grounding/hallucination/clarity trên màn-0.
- **Tên gọi:** đây là **đóng góp 1 (DG1)** — sinh hướng dẫn + chống bịa + đánh giá **mà không cần "tutorial chuẩn do người soạn"**.

### Kiểu 2 — Tier A: đo từng bước với màn THẬT dọn sẵn (chuẩn ngành)
- **Làm gì:** lấy một *episode* đa bước trong AndroidControl. Ở **mỗi bước**, bộ chấm **đưa cho model màn hình THẬT của đáp án vàng** (như thể đã có người mở sẵn đúng màn đó cho nó), rồi hỏi "bước tiếp theo bấm gì?". Model đoán → **so ngay với thao tác vàng** của bước đó. Xong bước này, lại đưa màn thật của bước kế tiếp — cứ thế.
- **Tên đời thường của cách đo này — *teacher-forcing*:** "chấm từng bước với màn thật dọn sẵn". Giống thầy giáo luôn dắt học trò về đúng màn đúng trước khi hỏi câu kế, để mỗi câu được chấm độc lập, không bị lỗi câu trước kéo theo.
- **Metric:** *Action-Type accuracy* (đoán đúng **loại** thao tác: bấm / gõ chữ / cuộn…), *Grounding@14%* (chỗ bấm coi là trúng khi **tâm nút lệch ≤14% kích thước màn** so với đích, **hoặc** rơi đúng bounding box của đích — ngưỡng 14% là chuẩn của AITW), *Step-SR* (Step Success Rate — tỷ lệ bước làm **đúng trọn vẹn**).
- **Tier A là cái gì, KHÔNG là cái gì:**
  - **LÀ một MỐC TRẦN (skyline / cận trên):** vì model được trợ giúp tối đa (luôn thấy màn thật), điểm ở đây là mức **cao nhất có thể** của hệ trong điều kiện lý tưởng. Ta dùng nó làm mốc để đo "mất bao nhiêu khi bỏ trợ giúp".
  - **KHÔNG claim ngang leaderboard:** hệ của ta dò nút từ ảnh bằng OmniParser (tỷ lệ dò **chưa công bố rõ cho UI mobile dày**, phải tự đo ở K1 — mục 5) và setup khác bảng xếp hạng công khai → ta chỉ **đặt trong cùng giao thức để tham chiếu định tính**, **không** tuyên bố "ngang điểm các hệ trên leaderboard".
- ⚠️ **Lưu ý no-leak:** việc "cho xem màn thật từng bước" ở Tier A là **dụng cụ đo cận trên có chủ đích**, **không** phải năng lực sản phẩm. Sản phẩm thật (DG1 đơn bước / DG2 sắp-thứ-tự) chỉ nhận **ảnh người dùng đưa** (1 ảnh, hoặc N ảnh xáo trộn) — **KHÔNG** được "dọn sẵn màn đúng từng bước" như Tier A.

### Kiểu 3 — DG2: suy luận trật tự màn (Screen-Order Inference — đóng góp MỚI)

> *(độ "mới" này đã được rà — kill-test KZ': KHÔNG có công trình trùng khít. Gần nhất là Sort-Story (xếp ảnh+caption xáo, EMNLP 2016 — dùng **Spearman**, KHÔNG phải τ), "Sequencing Multimodal Instructional Manuals" (xếp bước hướng dẫn xáo, ACL 2022), RankGPT (LLM sinh permutation theo query — là **phương pháp** listwise, không phải metric, EMNLP 2023). *(Tiền lệ τ-cho-ordering riêng = Lapata 2006 + Wu 2022, không phải Sort-Story.)* Cái mới của ta = (a) domain GUI màn-hình + (b) điều kiện hoá theo mục tiêu/use-case + (c) gắn ordering → SINH tutorial + (d) signal-attribution (cue nào giúp xếp đúng). Phải thừa nhận lineage 3 công trình trên, KHÔNG claim "xếp ảnh xáo là mới tinh".)*

- **Làm gì:** lấy một episode đa bước trong AndroidControl, lấy **N màn của luồng đó rồi XÁO TRỘN thứ tự** + đưa kèm mục tiêu. Model phải **(1) tự xếp lại đúng trật tự các màn, (2) sinh hướng dẫn từng bước theo trật tự đó**.
  > *Ví dụ đời thường (N màn xáo của app Đồng hồ hoặc eTax):* đưa model 4 ảnh lộn xộn — màn đăng nhập, màn danh sách, màn chi tiết, màn xác nhận. Model **nhìn manh mối trên ảnh** (nút *Next*, toggle off→on, màn đăng nhập đứng trước, màn danh sách → màn chi tiết) → **xếp lại đúng** → rồi sinh hướng dẫn theo đúng thứ tự đó.
- **Manh mối để xếp (5 ordering cue — trả lời thẳng câu hỏi của thầy "model dựa vào đâu để biết trật tự?"):** *gating* (đăng nhập/cấp quyền phải đứng trước) · *nav-affordance* (có nút Next/Back/breadcrumb) · *state-delta* (toggle off→on, ô trống→đã điền, badge 0→1) · *title-progression* (tiêu đề thay đổi theo phiếu) · *drill-down* (màn sau = chi tiết của item ở màn trước).
- **Metric HEADLINE — *Kendall τ-b*** (thước đo độ giống nhau giữa thứ tự máy xếp và thứ tự đúng; +1 = trùng khít, −1 = đảo ngược hoàn toàn; tiền lệ "dùng τ chấm ordering" = **Lapata 2006, Computational Linguistics 32(4):471–484**; nguồn gốc τ = Kendall 1938; Gao et al. NAACL 2025 ở vai meta-eval — đã có trong `01_metrics` Track B). Phụ: *pairwise-order-accuracy* + *position-accuracy@correct-place*. **Không** dùng pairwise-acc thô làm headline (dễ thành tautology). **Bỏ Exact-Order-Match** khỏi headline (N=3 thì đoán hú hoạ cũng trúng ~17%, N≥6 thì ~0%).
- **Chấm theo THỨ-TỰ-BỘ-PHẬN (partial-order-aware) — quy ước bắt buộc:** chỉ **PHẠT** khi máy đảo sai **cặp BẮT BUỘC** (cặp có quan hệ gating/drill-down — đảo là sai thật); còn **cặp TỰ-DO** (làm trước hay sau đều đúng) thì đảo **vẫn tính ĐÚNG**.
  > *Ví dụ:* điền **Email** và **SĐT** là hai ô độc lập → máy xếp ô nào trước cũng **đúng**. Nhưng **đăng nhập phải đứng trước xem kết quả** → đảo lại là **sai**. τ-b headline chỉ tính trên **cặp bắt buộc**; báo **thêm** τ-b-**thô** (so thứ tự gốc trên toàn bộ cặp) làm **"điểm sàn"** robustness.
- **Loại episode N≤2** (N=2 chỉ có 1 cặp → τ-b chỉ ra {−1, +1}, vô nghĩa). Trục N thực tế **N∈[3, ~10]** (đường-cong headline chốt trần N≤6; báo thêm tới ~8–10 nếu ngân sách); phải **tự đếm histogram độ dài episode** (việc tuần-1, cổng kill-test KN — AndroidControl mean ~5.5 step/episode, p95=13, nhưng không cho sẵn số đếm theo từng N → phải tự đếm).
- **Vì sao Kiểu 3 mạnh hơn cách đo cũ:** grounding/hallucination/format được **chấm ĐẦY ĐỦ trên mọi màn** (mọi màn đều là ảnh thật người dùng đưa, máy ĐỀU THẤY — chỉ là thứ tự bị xáo, không có màn nào "chưa thấy").

### Hiệu số quan trọng — *ordering gap*
- **Hai chế độ đo trên CÙNG bộ N màn:**
  - **ORACLE-ORDER (skyline / cận trên):** N màn **ĐÃ sắp đúng sẵn** + mục tiêu → model **chỉ phải sinh hướng dẫn**, không phải tự xếp.
  - **SELF-ORDER (thật):** N màn **xáo trộn** → model **tự xếp rồi mới sinh**.
- **Định nghĩa:** **ordering gap = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER)** = **"cái giá của việc không biết trật tự"**.
  > *Đọc đời thường:* cho sẵn thứ tự thì dễ; bắt model **tự xếp từ N ảnh xáo** mới là cái giá phải trả. Gap chính là phần chất lượng tụt đi vì máy phải tự đoán trật tự.
- **Sanity cứng:** ORACLE-ORDER **≥** SELF-ORDER **− ε** ở **mọi episode** (vượt ε = bug, vì cho sẵn thứ tự không thể tệ hơn tự xếp).
- ⚠️ **Cảnh báo floor-effect:** gap chỉ có nghĩa **nếu** metric tutorial **nhạy** với thứ tự; nếu không nhạy thì **τ-b là trục chính**, gap chỉ là phụ.

### Ví dụ ba kiểu trên một episode (app Đồng hồ — gọi là EX-B) *(ví dụ minh hoạ tự soạn — phỏng theo format action của AndroidControl, nhưng app Đồng hồ + giờ là nội dung tự dựng; record THẬT của AndroidControl là episode 'cruisedeals' — xem 02_datasets mục HỘP-THẬT)*

> Lấy một *episode* 3 bước phỏng theo format AndroidControl cho dễ thấy khác biệt. **Đáp án vàng:** *B1 màn chính Đồng hồ → bấm tab "Báo thức"; B2 màn Báo thức → bấm "+"; B3 màn đặt giờ → chọn 7:00.* Cùng MỘT hệ ở mục 2, chỉ đổi **model được thấy gì / phải làm gì với thứ tự**.

| Kiểu | Model thấy gì | Chạy ra sao | Kết quả mẫu | Nghĩa |
|---|---|---|---|---|
| **Kiểu 1 — DG1 màn-0** | chỉ màn chính Đồng hồ | chạy pipeline **1 lần** | "1. Bấm Báo thức 2. Bấm + 3. Chọn 7:00", chấm trên **màn-0** | sản phẩm thật, chỉ-1-ảnh |
| **Kiểu 2 — Tier A** | màn THẬT của **từng** bước (dọn sẵn) | chạy **từng bước**, mỗi bước so gold ngay | **3/3 đúng** (Step-SR cao) | **mốc trần chuẩn ngành** |
| **Kiểu 3 — DG2 (SELF-ORDER)** | **3 màn THẬT nhưng XÁO TRỘN** + mục tiêu | model **tự xếp** B1→B2→B3 rồi sinh tutorial | xếp đúng B1 (nav-affordance/drill-down: tab "Báo thức" → màn danh sách) trước, nhưng đảo B2/B3 → **τ-b chưa tối đa** | đúng cảnh suy luận trật tự |

> Đọc kết quả: ở Kiểu 3, mọi màn đều là **ảnh thật** (máy ĐỀU THẤY, không có màn nào "chưa thấy") — chỉ là **thứ tự bị xáo**, model phải tự dựng lại. Nếu chạy lại episode này ở chế độ **ORACLE-ORDER** (cho sẵn thứ tự đúng) thì model **chỉ phải sinh hướng dẫn**, chất lượng sẽ cao hơn; **ordering gap** chính là chênh lệch giữa hai lần chạy đó.

> 👉 **Chốt lại:** một hệ, ba kiểu đo. Kiểu 1 = sản phẩm màn-0. Kiểu 2 (Tier A) = mốc trần đo theo chuẩn ngành. Kiểu 3 (DG2) = **suy luận trật tự màn**: đưa N màn thật xáo trộn, model tự xếp rồi sinh tutorial; headline = **Kendall τ-b** chấm theo thứ-tự-bộ-phận, và **ordering gap** (ORACLE-ORDER − SELF-ORDER) cho biết **không biết trật tự thì mất bao nhiêu**. **Không có hệ thứ hai nào cả.**

> 🗺️ **Bản đồ đối chiếu tên gọi (khớp với `03_pipeline.md`)** — giờ đã hiểu 3 kiểu, đọc bảng này để khớp tên:
> - 5 bước ở mục 2 = pipeline **SoM-Tutor ⊕ GroundFirst**. Hệ đầy đủ (có thêm Stage 0 sắp-thứ-tự đặt trước 5 bước) = **ReOrder-Tutor**.
> - "Ba kiểu chạy" = **một hệ, 3 chế độ đo:** Kiểu 1 = **DG1 màn-0** · Kiểu 2 = **Tier A** · Kiểu 3 = **DG2 — suy luận trật tự màn**.

---

## 5. Một sự thật phải nhớ (rủi ro số 1)

Cả hệ **chỉ giỏi bằng bước 1 (dò nút)**. Nếu OmniParser **bỏ sót** nút "Tra cứu" → model không có ③ để chọn → **không bao giờ trả lời đúng được**, dù model có thông minh.

**Recall (tỷ lệ dò trúng) của detector trên UI mobile dày CHƯA được công bố rõ ràng** — các nguồn về OmniParser/ScreenSpot chỉ cho *grounding accuracy* (~57%), không phải recall element. **Giả thuyết làm việc (chờ K1 xác nhận):** có thể **~một nửa** nút bị bỏ sót. → **Việc đầu tiên phải làm (kill-test K1):** tự đo tỷ lệ dò trúng trên ~30–50 màn MobileViews. Mọi con số về sau phải ghi kèm *"với điều kiện tỷ lệ dò = X%"*. Nếu thấp → **đổi cách phát biểu** thành "grounding trong giới hạn khả năng dò", chứ không bỏ đề tài.

> 🚨 **Bẫy số 2 — 3 dataset dùng 3 ĐỊNH DẠNG TOẠ ĐỘ khác nhau (CHỐT-BBOX):** ngoài recall, còn một bẫy âm thầm khiến point-in-bbox sai hàng loạt nếu không cẩn thận:
> - **MobileViews:** bbox **pixel** dạng `[left, top, right, bottom]` (vd root thật `[0,0,1080,1920]`).
> - **ScreenSpot (HF):** bbox **chuẩn hoá 0–1** dạng `[x_min, y_min, x_max, y_max]` (vd `[0.948,0.144,0.994,0.207]`).
> - **AndroidControl:** **không có bbox** cho thao tác mà là **điểm click `(x, y)`** trong trường `action` (vd `{action_type: click, x:313, y:742}`).
> → **Harness phải quy đổi tất cả về cùng một hệ toạ độ TRƯỚC khi chấm** (point-in-bbox), kẻo so pixel với 0–1, hoặc so điểm click với bbox sai chuẩn → trượt hàng loạt mà tưởng model dở. Chi tiết xem `02_datasets.md` mục **CHỐT-BBOX**.

---

## 6. Bảng "mỗi bước cần gì, khó dễ ra sao"

| Bước | Tool | Khó/Dễ | Cần GPU? | Tự code? |
|---|---|---|---|---|
| 1. Dò nút | OmniParser V2 + OCR (Qwen/Vintern cho VN) | có sẵn, cài 1 buổi | nhẹ (chạy local) | gọi tool có sẵn |
| 2. Vẽ số | Set-of-Mark (PIL/cv2) | rất dễ | không | ~30 dòng |
| 3. Sinh có ràng buộc | Qwen2.5-VL-7B (1 GPU 24GB) / GPT-4o | trung bình | 24GB | prompt + bật guided/Structured Outputs |
| 4. Kiểm V1/V2/V3 | V1 thuần code; V2 model khác; V3 vòng lặp | trung bình | dùng API | tự ghép |
| 5. Đổi số→toạ độ | tra bảng | rất dễ | không | vài dòng |
| Chấm điểm | code Python so với cây UI MobileViews | phần tốn công nhất | không | tự viết harness |

**Chi phí:** 1 GPU 24GB (mua/thuê ~$0.3–0.5/h) + ~$100–300 API *(ước tính theo bảng giá tại thời điểm viết, kiểm lại trước khi cam kết)*. **Không cần train model.**

---

## 7. Tóm tắt 5 dòng
1. **Dò + đánh số** mọi nút trên ảnh → tạo "vốn từ" E.
2. **Ép** model chỉ được **chỉ vào số** trong E → không bịa được nút.
3. **Kiểm 3 tầng** (có/đúng-ý/sửa) → chốt chất lượng.
4. **Đổi số → toạ độ** → vừa hiện cho người, vừa chấm được.
5. **Thí nghiệm thang bậc C0→C4** để biết *món nào* thực sự có ích (LÕI/Gọn chỉ chạy 3 bậc {C1, C3, C4}; C0, C2 = mở rộng/đối chứng nếu ngân sách cho phép) — và mọi số kèm "tỷ lệ dò = X%".

> 🎯 **Luận văn có HAI đóng góp (đừng quên cái thứ hai):**
> - **(a) Màn-0 (DG1):** sinh hướng dẫn + chống bịa + **đánh giá mà không cần "tutorial chuẩn do người soạn"** (no-gold-tutorial), chấm bằng cây UI bạc của MobileViews.
> - **(b) Đa bước trên AndroidControl (DG2 — suy luận trật tự màn):** đưa **N màn thật xáo trộn** + mục tiêu, model **tự xếp lại đúng trật tự rồi sinh tutorial** — đóng góp **MỚI** *(đã rà KZ': không trùng khít công trình nào, nhưng thừa nhận lineage Sort-Story / "Sequencing Multimodal Instructional Manuals" / RankGPT)*. Headline = **Kendall τ-b** chấm theo **thứ-tự-bộ-phận** (chỉ phạt cặp bắt buộc), kèm **ordering gap** (ORACLE-ORDER − SELF-ORDER) = "cái giá của việc không biết trật tự". **Tier A** (teacher-forced) vẫn giữ làm **trục tham chiếu chuẩn ngành / mốc trần**, **không** còn là "đa bước chính".
