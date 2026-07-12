# BÁO CÁO 13 — PIPELINE · METRIC · THÍ NGHIỆM (BẢN DỄ HIỂU NHẤT)

> **Cho ai đọc:** người **chưa biết gì** về đề tài, đọc một mạch là hiểu **(1) hệ thống làm gì & tại sao thiết kế vậy, (2) đo chất lượng bằng gì, (3) chạy thí nghiệm gì để chứng minh hệ thống TỐT**.
> **Đóng khung (mới, đã chốt với người hướng dẫn):** luận văn có **HAI đóng góp NGANG NHAU**:
> - **Đóng góp A — HỆ THỐNG sinh tutorial TỐT** (ReOrder-Tutor): không chỉ "chạy được" mà phải **ra kết quả tốt, thắng baseline**.
> - **Đóng góp B — CÁCH ĐÁNH GIÁ** đáng tin khi không có đáp án mẫu do người viết.
> *(Bản này thay cách nói cũ "pipeline chỉ là hệ tham chiếu". Pipeline NAY là một đóng góp thực sự.)*
> **Bạn đã hiểu dataset rồi** → file này gần như không nhắc lại dataset, chỉ tập trung pipeline + metric + thí nghiệm. Chi tiết khoá: `03_pipeline.md`, `01_metrics.md`, `05_final_plan.md`; chạy thử: `12_trial_run_runbook.md`.

> ✅ **CẬP NHẬT QUAN TRỌNG — ĐÃ CHỐT DESIGN E (2026-06-25):** mô tả pipeline trong file này (Set-of-Mark + đánh số + ràng-buộc-ID đặt TRƯỚC) là **bản CŨ — nay HẠ xuống một bậc ablation**. **Pipeline lõi đã chốt = "lớp trung-thực-hoá":** model mạnh **THAY ĐƯỢC** (Qwen mở = lõi; GPT-5/Gemini-3 đối chứng) sinh tutorial **gọi nút theo TÊN** → **oracle kiểm BÊN CẠNH** (không chặn khâu sinh) → **fallback mô tả bằng lời** khi không khớp. Metric **thêm coverage (chống gaming) + Followability/Step-SR**. → **Đọc `report/00_DOC_TU_DAU.md` (1-file dễ hiểu) + `report/14_thiet_ke_cuoi_2026.md` (spec)** thay cho phần pipeline cũ ở đây.

---

## PHẦN 0 — NẮM CẢ LUẬN VĂN TRONG 1 PHÚT

**Bài toán:** người dùng đưa **ảnh chụp màn hình + câu hỏi** → máy trả **hướng dẫn bấm từng bước** cho người đọc.
- *Ví dụ 1 ảnh:* ảnh app thuế eTax + hỏi *"kiểm tra đã nộp thuế chưa thì vào đâu?"* → máy đáp *"1. Bấm 'Tra cứu nghĩa vụ thuế'. 2. Chọn kỳ. 3. Xem trạng thái."*
- *Ví dụ nhiều ảnh:* đưa N ảnh các màn **bị xáo trộn** của một luồng → máy phải **tự xếp lại đúng thứ tự** rồi mới viết hướng dẫn.

**Hai đóng góp:**
- **A. Hệ thống tốt:** một quy trình thông minh khiến máy viết hướng dẫn **đúng nút, không bịa, rõ ràng** — và **chứng minh nó tốt hơn** cách để máy "viết tự do" (kể cả tốt hơn GPT-4o viết thẳng).
- **B. Cách đánh giá:** vì không có "hướng dẫn mẫu chuẩn" do người soạn, ta dựng một bộ thước đo + thí nghiệm để **biết chắc** hệ tốt tới đâu mà không tự lừa mình.

**Một câu:** *Ta xây một hệ viết hướng dẫn phần mềm bám sát ảnh (ít bịa, đúng chỗ bấm), và một cách đo nghiêm túc để chứng minh nó thật sự tốt.*

---

## PHẦN 1 — VẤN ĐỀ CỐT LÕI (vì sao cần "pipeline" chứ không hỏi thẳng GPT-4o)

Nếu đưa thẳng ảnh + câu hỏi cho một model nhìn-ảnh-viết-chữ (gọi là **VLM**) và bảo "viết hướng dẫn đi", nó hay mắc **3 lỗi**:

1. **Bịa nút không có thật** (gọi là *hallucination*): màn hình không có nút "Cài đặt" nhưng nó vẫn viết "bấm Cài đặt". → hướng dẫn sai, người dùng làm theo không được.
2. **Chỉ sai chỗ bấm** (*grounding kém*): nó nói "bấm góc trên phải" nhưng nút thật nằm chỗ khác. VLM **rất dở khi phải tự phun toạ độ (x,y)**.
3. **Trình bày lộn xộn**: gộp 3 việc vào 1 câu, không đánh số, không động từ hành động.

> **Đây chính là lý do phải có pipeline.** Pipeline = một chuỗi bước khéo léo **ép** model tránh 3 lỗi trên → ra hướng dẫn tốt hơn hẳn "viết tự do". **Kết quả tốt của hệ đến từ thiết kế pipeline này**, không phải từ việc model thông minh sẵn.

---

## PHẦN 2 — PIPELINE LÀM GÌ (giải thích từng bước + TẠI SAO chọn vậy)

### Ẩn dụ dễ nhớ: biến bài "tự luận" thành bài "trắc nghiệm"
- Thay vì để model **tự luận** (muốn viết gì thì viết → dễ bịa),
- ta **đánh số mọi nút thấy được trên ảnh** (① Khai thuế ② Nộp thuế ③ Tra cứu… ) rồi **ép model chỉ được "chọn số"** ("bước 1 → bấm ③").
- → Model **không thể bịa** nút, vì nó chỉ được chọn trong các số CÓ THẬT. Đây là ý tưởng trung tâm.

### Sơ đồ 5 bước (chế độ 1 ảnh) + 1 bước thêm (chế độ nhiều ảnh)

```
   ẢNH + CÂU HỎI  (lúc chạy thật chỉ có 2 thứ này)
        │
        │  (nếu NHIỀU ảnh xáo trộn → chạy BƯỚC 0 trước)
        │   BƯỚC 0: tự xếp lại thứ tự các màn  ──► chuỗi màn đúng thứ tự
        ▼
   BƯỚC 1: DÒ NÚT  — một bộ dò nhìn ảnh, khoanh mọi nút/ô bấm được
        ▼
   BƯỚC 2: ĐÁNH SỐ (Set-of-Mark) — vẽ ①②③… đè lên từng nút
        ▼
   BƯỚC 3: SINH CÓ RÀNG BUỘC — model viết hướng dẫn, CHỈ được chỉ vào số đã có
        ▼
   BƯỚC 4: KIỂM 3 TẦNG — V1 (số có thật?) → V2 (đúng nút cho mục tiêu?) → V3 (tự sửa)
        ▼
   BƯỚC 5: ĐỔI SỐ → CHỮ + TOẠ ĐỘ — "③" → "Tra cứu nghĩa vụ thuế" + vị trí để hiển thị/chấm
        ▼
   HƯỚNG DẪN TỪNG BƯỚC cho người đọc
```

### Từng bước: làm gì · TẠI SAO chọn · căn cứ

| Bước | Làm gì (đời thường) | TẠI SAO chọn cách này | Căn cứ (đã rà literature 2024–2026) |
|---|---|---|---|
| **0. Xếp thứ tự** (chỉ khi nhiều ảnh) | Hỏi từng cặp "màn nào trước?" rồi tổng hợp thành thứ tự | Hỏi từng cặp **ổn định hơn** bắt model xếp cả dãy 1 lần (cách xếp-cả-dãy tụt >50% khi đầu vào bị xáo) | Pairwise + Copeland = **PRP-Allpair (NAACL 2024)**; cách-xếp-cả-dãy = RankGPT (EMNLP 2023) làm đối chứng |
| **1. Dò nút** | Bộ dò khoanh các nút trên ảnh | Cần biết "trên màn có những nút nào" để biến thành trắc nghiệm | **OmniParser** (Microsoft) — bộ dò UI sẵn có |
| **2. Đánh số** | Vẽ ①②③ lên ảnh | Cho model "chọn số" thay vì tự phun toạ độ (dễ sai) | **Set-of-Mark** (2023). *Lưu ý trung thực:* nay có model ground toạ độ thẳng tốt hơn → ta **thêm một nhánh "ground thẳng"** để so (xem Phần 3) |
| **3. Sinh có ràng buộc** | Ép model chỉ viết bước dạng (động từ + số nút + câu chữ), số phải thuộc danh sách | **Chống bịa tận gốc**: không thể nhắc nút ngoài danh sách. Có thêm lựa chọn **"không có nút phù hợp" (abstain)** để khỏi ép bịa khi dò thiếu | constrained decoding: **XGrammar (MLSys 2025)** / OpenAI Structured Outputs |
| **4. Kiểm 3 tầng** | V1: số có trong danh sách? (code, không cần AI) · V2: **một model KHÁC** soi "số này có đúng ý câu hỏi không?" · V3: nếu sai thì tự sửa tối đa 2 lần | V1 chặn bịa-tồn-tại; **V2 chặn lỗi "đúng nút có thật nhưng sai chức năng"** (vd hỏi *xem* trạng thái mà lại chỉ nút *nộp*). Dùng **model khác** để khỏi "tự chấm tự khen" | V2 = phản hồi từ-bên-ngoài → **thoát** phê phán "model không tự sửa được" (Huang ICLR 2024; Kamoi TACL 2024) |
| **5. Đổi số→chữ+toạ độ** | Tra bảng: ③ → "Tra cứu nghĩa vụ thuế" + vị trí nút | Để hiển thị cho người đọc + để **chấm điểm** (vị trí có trúng nút thật không) | tra bảng thuần, không phải nguồn lỗi |

> **Điểm mấu chốt chống bịa nằm ở BƯỚC 3 (lúc sinh), không phải bước kiểm.** Ép cấu trúc ngay lúc viết mới là cơ chế chính; 3 tầng kiểm chỉ là lưới đỡ phía sau.

---

## PHẦN 3 — VÌ SAO PIPELINE NÀY HỢP LÝ **VÀ RA KẾT QUẢ TỐT**

> Đây là phần quan trọng nhất theo yêu cầu: **không chỉ "đóng góp cách đánh giá", mà hệ phải TỐT thật.**

### 3.1. Cơ chế khiến hệ THẮNG cách "viết tự do" (kể cả thắng GPT-4o)
- **Hết bịa nút (faithfulness cao):** vì BƯỚC 3 ép chỉ chọn nút có thật → trên màn thấy được, tỉ lệ bịa ≈ 0. GPT-4o viết tự do thì **vẫn bịa** nút → ta **đo được** hệ ta ít bịa hơn.
- **Bấm đúng chỗ hơn (grounding cao):** model chọn-số rồi tra bảng ra toạ độ chính xác của nút, thay vì tự đoán toạ độ → trúng nút thật nhiều hơn.
- **Đúng ý hơn (intent):** tầng V2 bắt lỗi "đúng nút nhưng sai chức năng" mà cách viết tự do bỏ qua.
- **Trình bày chuẩn:** ép khuôn (đánh số + động từ + 1 việc/bước) → format luôn đạt.

> **Câu chuyện kết quả tốt (trung thực):** ta **KHÔNG** tuyên bố "đứng đầu bảng xếp hạng thế giới" (đó là bài toán khác, setup khác). Ta tuyên bố điều **đo được và mạnh**: *trên cùng một model nền và cùng bộ đo, hệ có-cấu-trúc của ta sinh hướng dẫn **ít bịa hơn, bấm đúng chỗ hơn, rõ hơn** so với để chính model đó (và cả GPT-4o) viết tự do.* Đây là một kết quả tốt, có ý nghĩa thực tiễn.

### 3.2. Pipeline này có hợp lý không? (đã rà literature kỹ)
- **Hợp lý ở chỗ:** chống-bịa-bằng-ràng-buộc + kiểm-bằng-model-khác là hướng **đúng và hiện hành** (constrained decoding XGrammar MLSys 2025; external-critic CRITIC ICLR 2024).
- **Điểm phải trung thực + cách ta xử:** kỹ thuật "đánh số (Set-of-Mark)" **không còn là cách ground tốt nhất** năm 2024–2026 — các model mới (Qwen2.5-VL, UGround, OS-Atlas) **ground toạ độ thẳng tốt hơn**. → Ta **không giấu**, mà **thêm một nhánh "ground thẳng"** vào so sánh, để câu trả lời "đánh số có đáng không" là **kết quả đo được**, không phải niềm tin. Thậm chí bản mạnh nhất có thể **kết hợp**: ground thẳng (cho chính xác) + ràng buộc cite-số (cho không bịa).
- **Rủi ro lớn nhất (phải nói thẳng):** bộ dò có thể **bỏ sót nút** → nút bị sót thì không đánh số được → model không chỉ được. Ta **đo recall của bộ dò trước (cổng K1)** và mọi con số đều ghi "trong điều kiện recall = X%". Có lựa chọn **abstain** để khi sót thì model nói "không thấy nút phù hợp" thay vì bịa.

### 3.3. Vì sao tin được hệ tốt mà không tự lừa mình → cần Đóng góp B
Không có "hướng dẫn mẫu chuẩn" do người viết để so. Nên ta đo bằng **mỏ neo khách quan** = cây cấu trúc UI thật (View Hierarchy) — chỉ dùng **lúc chấm**, không cho model xem lúc viết. Đó là cầu nối sang Phần 4.

---

## PHẦN 4 — METRIC: ĐO CHẤT LƯỢNG BẰNG GÌ (dễ hiểu)

Ta chấm hướng dẫn theo **4 tiêu chí**. Mỗi tiêu chí có một thước đo + ví dụ số.

| # | Tiêu chí | Câu hỏi đời thường | Thước đo + ví dụ |
|---|---|---|---|
| 1 | **Bấm đúng chỗ (Grounding)** | "Chỗ model bảo bấm có trúng nút thật không?" | **Point-in-bbox:** toạ độ (405,915) có nằm trong khung nút thật [270,820,540,1010]? Có → tính đúng. Báo % bước trúng. *(chuẩn de-facto, SeeClick ACL 2024)* |
| 2 | **Không bịa (Hallucination)** | "Có nhắc nút không tồn tại không?" | **Đối chiếu mở (ALOHa):** model nói "Thiết lập", màn chỉ có "Cài đặt" → 2 từ nghĩa giống → **không tính bịa** (tránh phạt oan đồng nghĩa). Nếu nhắc nút thật sự không có → tính bịa. Báo **tỉ lệ bịa + độ phủ** (có bỏ sót nút quan trọng không) |
| 3 | **Rõ ràng (Clarity/Format)** | "Có đánh số, động từ hành động, 1 việc/bước không?" | **Format (IFEval-style):** kiểm máy được, đạt/không đạt từng điều kiện. **Clarity:** một model-giám-khảo chấm 1–5 + **người chấm đối chiếu** (vì máy chấm phải được người kiểm lại mới tin) |
| 4 | **Đi tới đích (Task Success)** | "Làm theo có ra đúng kết quả không?" — dùng cho nhiều bước | Trên dữ liệu có đáp án vàng (AndroidControl): đúng loại thao tác? bấm trong sai số 14%? đúng cả chuỗi? |

> **Vì sao 4 cái này?** Một hướng dẫn tốt = **đúng chỗ (1) + không bịa (2) + dễ đọc (3) + dẫn tới đích (4)**. Thiếu cái nào cũng hỏng. Phần lớn thước đo lấy từ bài đã bình duyệt (ACL/EMNLP/NAACL).

### Đo riêng cho chế độ NHIỀU ẢNH — "xếp đúng thứ tự" (Kendall τ-b)
- Đưa N màn **xáo trộn**, model xếp lại. So thứ tự model với thứ tự đúng bằng **Kendall τ-b** (= +1 nếu trùng khít, 0 nếu như đoán bừa).
- **Chỉ phạt cặp BẮT BUỘC** (vd "đăng nhập trước → xem kết quả sau": đảo là sai), **không phạt cặp tự-do** (vd điền email/sđt trước-sau đều được). *(Cách chấm thứ-tự-bộ-phận này có nguồn chuẩn: Fagin et al. 2003/2006 — ta trích, không tự nhận là mới.)*

---

## PHẦN 5 — THÍ NGHIỆM: CHỨNG MINH HỆ TỐT (trình bày dễ hiểu)

Mỗi thí nghiệm trình bày 3 ý: **Hỏi gì → Làm sao → Đọc kết quả thế nào**.

### TN1 — Cơ chế nào trong hệ thật sự "trả công"? (ablation bậc thang)
- **Hỏi:** thêm từng cơ chế (đánh số, ràng buộc, kiểm intent) có giảm bịa / tăng đúng-chỗ không, **và cơ chế NÀO** đáng công?
- **Làm sao:** chạy **3 bậc** trên cùng một model:
  - **C1** = để model viết tự do + tự sửa *(baseline — "sàn")*
  - **C3** = thêm ràng buộc-chỉ-cite-số + kiểm số-có-thật
  - **C4** = thêm kiểm đúng-ý (V2) *(= hệ đầy đủ)*
  - *(thêm tùy chọn: C0 thô, C2 chỉ đánh số, và **nhánh ground-thẳng** để xem đánh-số có đáng không)*
- **Đọc kết quả:** nhìn **mức giảm bịa qua từng bậc**. VD bịa giảm mạnh ở C1→C3 (ràng buộc là cơ chế chính), C3→C4 giảm nhẹ (kiểm intent thêm chút) → kết luận rõ "cơ chế nào tạo ra kết quả tốt". *(Một A/B đơn không nói được điều này.)*

### TN2 — Hệ có tốt hơn để GPT-4o viết thẳng không?
- **Hỏi:** hệ có-cấu-trúc của ta có **thắng** một VLM mạnh (GPT-4o/Gemini) viết tutorial tự do không?
- **Làm sao:** cùng bộ ảnh + câu hỏi, một bên là pipeline đầy đủ, một bên là GPT-4o sinh thẳng → chấm cả hai bằng **cùng bộ metric** (đúng-chỗ, bịa, format) + **người chấm so đôi (BWS)**.
- **Đọc kết quả:** kỳ vọng pipeline **ít bịa hơn + đúng chỗ hơn** rõ rệt (vì GPT-4o tự do vẫn bịa nút). Đây là bằng chứng "hệ ra kết quả tốt", không chỉ "chạy được".

### TN3 — Máy có biết tự xếp thứ tự các màn không? (đóng góp nhiều-ảnh)
- **Hỏi:** đưa N màn xáo trộn, model xếp lại đúng tới đâu? Dựa vào tín hiệu nào?
- **Làm sao:** đo **Kendall τ-b** của thứ tự model so thứ tự đúng; so với **xếp bừa (RANDOM)**, **chỉ-đọc-mục-tiêu (GOAL-ONLY)**, **chỉ-xem-ảnh (VISUAL-ONLY)**. **Lọc bỏ** các episode có các màn gần-trùng nhau (xáo trộn rồi vẫn không phân biệt được → bài vô nghĩa).
- **Đọc kết quả:** nếu τ-b **cao hơn xếp bừa** đáng kể → model **thật sự** suy được trật tự; nếu GOAL-ONLY đã cao bằng → trật tự đến từ suy đoán theo mục tiêu chứ không từ ảnh (phải nói rõ). Đặt tên **5 loại tín hiệu** (gating, nút Next/Back, trạng thái đổi, tiêu đề tiến, drill-down) để trả lời "model dựa vào đâu".

### TN4 — Nhìn tận mắt: tutorial sinh ra có đẹp/đúng không? (demo định tính)
- **Hỏi:** ngoài con số, hướng dẫn thật trông có dùng được không?
- **Làm sao:** chọn vài màn thật, in ra tutorial của pipeline vs của baseline, kèm ảnh có khoanh nút được chỉ.
- **Đọc kết quả:** cho thầy thấy trực tiếp tutorial của hệ **rõ, đúng nút, không bịa** — thuyết phục bằng mắt.

> **Cổng an toàn trước khi tin số:** đo recall bộ dò (K1), tự đếm độ dài luồng (KN), chống lộ thứ tự khi xáo ảnh (KB). Mọi con số ghi kèm "trong điều kiện recall = X%".

---

## PHẦN 6 — CÓ NÊN FINE-TUNE KHÔNG? (tư vấn — bạn còn phân vân)

**Khuyến nghị: LÕI làm off-the-shelf (không fine-tune); coi LoRA-grounding là "bậc nâng cấp tùy chọn" nếu còn thời gian.** Lý do:

| | Off-the-shelf (khuyến nghị cho lõi) | Fine-tune nhẹ (LoRA) — tùy chọn |
|---|---|---|
| **Kết quả tốt?** | **Đã đủ để thắng baseline**: kết quả tốt đến từ *thiết kế pipeline* (ràng buộc + kiểm intent), không cần train | Có thể đẩy grounding cao hơn nữa (điểm yếu nhất) |
| **Khả thi/Ngân sách** | 1 GPU 24GB + ~$100–300, nhanh, ít rủi ro | Tốn công chuẩn bị dữ liệu train + dễ phát sinh GPU/thời gian |
| **Rủi ro** | Thấp | **Cao hơn về rò rỉ** (phải tách train/test cẩn thận, không cho cây cấu trúc UI lọt vào lúc train) |
| **Câu chuyện luận văn** | Sạch: "thiết kế thông minh trên model có sẵn" | Mạnh hơn nhưng phải bảo vệ kỹ phần train |

→ **Đề xuất cụ thể:** chạy và báo cáo lõi off-the-shelf trước (đủ để có "kết quả tốt, thắng baseline + thắng GPT-4o"). **Nếu** sau khi xong lõi mà còn thời gian/ngân sách và muốn đẩy mạnh grounding, **mới** thêm **LoRA cho riêng bước ground** như một thí nghiệm nâng cấp — đóng khung "bậc nâng cao", không phải xương sống. Cách này giữ khả thi mà vẫn để ngỏ đường mạnh hơn.

*(Nếu bạn muốn fine-tune ngay từ đầu làm trọng tâm, mình sẽ phải dựng lại kế hoạch dữ liệu train + chống rò rỉ + ngân sách GPU — nói mình biết để chỉnh `05`.)*

---

## PHẦN 7 — NÓI THẲNG NHỮNG GIỚI HẠN (để không bị bắt lỗi)
- **Không claim đứng đầu bảng xếp hạng thế giới** — setup của ta khác (sinh tutorial cho người, không phải agent bấm máy). Ta claim **thắng baseline trên cùng bộ đo của ta** + thắng GPT-4o viết thẳng về độ-bám-ảnh.
- **Mọi số grounding "có điều kiện recall bộ dò"** — nếu bộ dò sót nhiều, trần kết quả bị hạ; ta đo và ghi rõ.
- **Chế độ nhiều ảnh là bài đặt ra để ĐO năng lực suy luận trật tự**, không khẳng định là nhu cầu phổ biến.
- **Máy-giám-khảo (LLM-judge) chỉ GIẢM chứ không TRIỆT thiên lệch** — nên luôn có người chấm đối chiếu.

---

## PHẦN 8 — MỘT DÒNG TÓM TẮT
**Ta xây một hệ viết hướng dẫn phần mềm bám sát ảnh — ép model chỉ chỉ vào nút có thật + kiểm đúng-ý + biết tự xếp thứ tự nhiều màn — và chứng minh bằng thí nghiệm rằng nó sinh hướng dẫn ít bịa hơn, đúng chỗ hơn, rõ hơn so với để model (kể cả GPT-4o) viết tự do; song song là một cách đánh giá đáng tin khi không có hướng dẫn mẫu của người.**
