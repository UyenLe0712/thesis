# 📏 METRIC ĐÁNH GIÁ — BẢN RÕ RÀNG (định nghĩa + công thức + ví dụ thật)

> **File này để làm gì?** Trình bày **rõ ràng từng thước đo**: *đo gì · tính thế nào · cần dữ liệu gì · ví dụ trên dữ liệu thật · cao/thấp nghĩa gì · nguồn*. Viết cho người chưa quen. (Bản chi tiết + đầy đủ citation: `report/01_metrics.md`; thiết kế: `report/14`.)
> **Quy ước:** mọi metric quy về **"cao = tốt"** để dễ đọc.
> **Hai nhóm:** **DG1** = chấm hướng dẫn trên **một màn**. **DG2** = chấm năng lực **nhiều màn** (xếp thứ tự + làm-theo-tới-đích).

---

## A. NHÓM DG1 — chấm hướng dẫn trên MỘT màn

Mỗi bước hướng dẫn có dạng *(động từ, tên nút, ghi chú)*, vd "Bấm **Tra cứu nghĩa vụ thuế**". Ta đối chiếu với **danh sách nút thật** của màn (View Hierarchy / accessibility tree — gọi là "đáp án bạc", chỉ dùng lúc chấm).

### A1. BỊA (Hallucination) — ⭐ trụ cột
- **Đo gì:** hướng dẫn có nhắc nút **KHÔNG tồn tại** trên màn không?
- **Cách tính:** với mỗi tên nút model viết, tìm nút thật **gần NGHĨA nhất** (matcher **ALOHa** = so vector nghĩa). Nếu độ giống < ngưỡng τ → **bịa**.
  `HER = (số bước bịa) / (tổng số bước)` → **Faithfulness = 1 − HER** (cao = tốt).
- **Vì sao dùng ALOHa, không so chuỗi:** so chuỗi sẽ **vu oan** "Thiết lập" là bịa dù màn có nút "Cài đặt" (cùng nghĩa). *(Đã chứng minh: so chuỗi báo bịa 40.7%, ALOHa còn 33.3% — 2 synonym được sửa oan.)*
- **Ví dụ thật (từ chạy thử #1, màn item2 — KHÔNG phải số headline):** model viết "Bấm **Find or create a contact**" nhưng màn chỉ có Email/First name/Last name → **bịa**; 3 bước kia khớp nút thật → HER = 1/4 → **Faithfulness = 75%** *(số headline trên 10 màn là 66.7% ALOHa — xem `15`)*.
- **Nguồn:** ALOHa (NAACL 2024); CHAIR/HER (EMNLP 2018).

### A2. ĐỦ Ý (Coverage)
- **Đo gì:** hướng dẫn có **bỏ sót** nút cần thiết không? (Chống mẹo "viết thật ít cho khỏi sai".)
- **Cách tính:** `Coverage = (số nút CẦN được nhắc) / (tổng số nút CẦN)`, **có trọng số** bước quan trọng.
- **Lưu ý quan trọng (rõ ràng):** "nút CẦN" chỉ biết chắc khi có **đáp án vàng** → **đo coverage trên AndroidControl** (có gold từng bước). Trên MobileViews (không gold) coverage chỉ là **proxy** (chia cho mọi nút actionable) → **báo riêng, không làm headline**.
- **Cao = tốt** (không bỏ sót). Báo **cặp [Faithfulness, Coverage]** cùng nhau.
- **Nguồn:** VALOR-EVAL (Findings ACL 2024).

### A3. ĐÚNG CHỖ (Grounding — point-in-bbox)
- **Đo gì:** chỗ model bảo bấm có **trúng khung nút thật** không?
- **Cách tính:** lấy toạ độ điểm bấm `(x,y)`; nếu rơi trong bbox `[l,t,r,b]` của nút → đúng.
  `Grounding = (số bước trúng) / (số bước có toạ độ)`. *(Trên AndroidControl còn so với toạ độ gold; ngưỡng dung sai 14% lấy từ AITW.)*
- **Ví dụ thật (đã chạy):** điểm `(255,1015)` rơi trong bbox `[180,935,330,1095]` của nút "8" → **TRÚNG**.
- **Cao = tốt.** **Nguồn:** SeeClick/ScreenSpot (ACL 2024); ngưỡng 14% = AITW (NeurIPS 2023).

### A4. ĐÚNG NHÃN / Rõ ràng (Clarity — label-fidelity)
- **Đo gì:** model có gọi **ĐÚNG TÊN hiển thị** của nút không? (Gọi "Thiết lập" cho nút "Cài đặt" → người dùng **khó tìm**.)
- **Cách tính:** so **CHÍNH XÁC** tên (chuẩn hoá). `Label-fidelity = (số bước đúng tên) / (tổng số bước)`.
- **Khác A1 thế nào (mấu chốt):** A1 (bịa) dùng **đồng-nghĩa-OK** (nút có tồn tại không); A4 (clarity) **đòi đúng tên** (gọi synonym → trừ clarity, **KHÔNG** tính bịa). Hai lỗi khác nhau, đo riêng.
- **Ví dụ thật (đã chạy):** 10 màn → đúng-nhãn 59.3%; 7.4% bước "nút có thật nhưng gọi sai tên" → trừ clarity, không tính bịa.
- *(Lưu ý: nút icon không có chữ → không đòi đúng-nhãn được → loại khỏi mẫu A4.)*
- **Cao = tốt.**

### A5. ĐỊNH DẠNG (Format)
- **Đo gì:** có đánh số (1,2,3)? đầu bước là động từ mệnh lệnh? mỗi bước 1 việc?
- **Cách tính:** checklist kiểm-được-bằng-máy → `Format = (số điều kiện đạt) / (tổng điều kiện)` (báo strict + loose).
- **Cao = tốt.** **Nguồn:** IFEval-style; clarity sâu hơn dùng rubric + LLM-judge (validate với người).

---

## B. NHÓM DG2 — nhiều màn (xếp thứ tự + làm-theo-tới-đích) — trên AndroidControl

### B1. XẾP THỨ TỰ (Kendall τ-b) — ⭐ trụ cột DG2
- **Đo gì:** đưa N ảnh **xáo trộn**, model xếp lại; thứ tự đó **giống thứ tự đúng** tới đâu?
- **Cách tính:** với mỗi cặp màn, đếm **xuôi** (model xếp cùng chiều đáp án) và **ngược**.
  `τ-b = (xuôi − ngược) / chuẩn-hoá` ∈ [−1,+1]. **+1 = trùng khít, 0 = như đoán bừa.**
- **Chấm "thứ-tự-bộ-phận":** chỉ **phạt cặp BẮT BUỘC** (vd đăng-nhập-trước-xem-sau); cặp **tự do** (điền email/sđt trước-sau đều được) đảo **vẫn đúng**. Nhãn cặp-bắt-buộc **suy từ đáp án vàng** (chống tự chấm).
- **Bắt buộc lọc episode trước:** bỏ episode có các màn **gần-trùng** (xáo rồi cũng không phân biệt được) → bài đo mới có nghĩa.
- **Cao = tốt.** **Nguồn:** Lapata (CL 2006) + Fagin (thứ-tự-bộ-phận).

### B2. LÀM-THEO-TỚI-ĐÍCH (Step-SR) — ⭐ chứng minh "hiệu quả thật"
- **Đo gì:** **làm theo hướng dẫn** model sinh ra thì **có tới đích** không? (Bằng chứng khó cãi nhất.)
- **Cách tính:** chuyển mỗi bước thành thao tác, so với **thao tác vàng** từng bước của AndroidControl (đúng loại + đúng chỗ trong 14%). `Step-SR = (số bước đúng) / (tổng bước)`.
- **Cần:** AndroidControl (có đáp án vàng) → **đây là phần cần Colab.**
- **Cao = tốt.** **Nguồn:** AndroidControl (NeurIPS 2024) + AITW (ngưỡng 14%).

### B3. ĐÚNG LOẠI THAO TÁC (Action-Type) — tham chiếu chuẩn ngành
- **Đo gì:** model đoán đúng **loại thao tác** (bấm/cuộn/gõ…) mỗi bước không?
- **Cách tính:** `(số bước đúng loại) / (tổng bước)`. **Cao = tốt.**

---

## C. ĐÁNH GIÁ CHÉO — metric tự động có ĐÁNG TIN không?

### C1. Khớp với người (Track B)
- **Đo gì:** điểm máy chấm có **xếp hạng giống người** không?
- **Cách làm:** người chấm ~60–80 tutorial bằng **so-đôi (BWS)** → đo **tương quan (Kendall/Spearman) + Krippendorff α** (độ đồng thuận). α≥0.8 = tin được.
- **Cao = tốt** (máy khớp người). **Nguồn:** BWS (ACL 2017); Krippendorff.

### C2. Nhạy (tín hiệu sơ bộ)
- Metric **phân biệt được model tốt/dở** = dấu hiệu metric **có-ích**. *(Sơ bộ — matcher chuỗi, 2 model: bịa 3B 40.7% vs 7B 25%.)* **Độ tin ĐẦY ĐỦ** vẫn cần C1 (Track B với người) + ALOHa + nhiều mẫu.

---

## D. BẢNG TÓM TẮT (1 trang)

| # | Metric | Đo gì | Cần gold? | Cao=tốt | Trạng thái |
|---|---|---|---|---|---|
| A1 | **Bịa / Faithfulness** | nhắc nút không tồn tại? | không (cây nút) | ✓ | ✅ đã chạy (ALOHa) |
| A2 | **Coverage** | bỏ sót nút cần? | có (đo trên AndroidControl) | ✓ | ⏳ Colab |
| A3 | **Grounding** | bấm trúng khung nút? | không | ✓ | ✅ đã chạy |
| A4 | **Đúng-nhãn / Clarity** | gọi đúng tên hiển thị? | không | ✓ | ✅ đã chạy |
| A5 | **Format** | đánh số/động từ/1-việc? | không | ✓ | ⏳ |
| B1 | **Xếp thứ tự (τ-b)** | xếp N màn đúng thứ tự? | có | ✓ | ⏳ Colab |
| B2 | **Step-SR (tới đích)** | làm theo có tới đích? | có | ✓ | ⏳ Colab |
| B3 | **Action-Type** | đúng loại thao tác? | có | ✓ | ⏳ Colab |
| C1 | **Khớp người (Track B)** | máy chấm giống người? | nhãn người | ✓ | ⏳ |

> **Một dòng:** mỗi metric đều có **định nghĩa + công thức + cao/thấp rõ ràng + nguồn**; các metric **không cần gold (A1/A3/A4)** đã **chạy thật**; các metric **cần gold (coverage/τ-b/Step-SR)** chạy trên **AndroidControl (Colab)**.
