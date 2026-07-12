# BÁO CÁO 5 — KẾ HOẠCH CHỐT CUỐI (nguồn-sự-thật để thực hiện)

## TÓM TẮT 30 GIÂY

Đây là **kế hoạch chốt cuối** — khi mâu thuẫn với report 01–04, **file 05 thắng**. Sáu điểm đã khoá:

1. **Hai đóng góp song hành:** **DG1** = quy trình đánh giá tutorial trên màn-0 (không có tutorial gold của người); **DG2** = đánh giá **suy luận trật tự màn (Screen-Order Inference)** từ N ảnh **xáo trộn** của 1 luồng đa bước trên AndroidControl. Đóng khung sao cho **kết quả ÂM vẫn ĐẬU** (nếu pre-register) ở CẢ HAI.
2. **Ba dataset chính:** **MobileViews** (màn-0, DG1) + **AndroidControl** (đa bước → suy luận trật tự, DG2) + **ScreenSpot(-v2)** (đối chứng grounding). Mind2Web (web) là future-work.
3. **Một pipeline duy nhất** (ReOrder-Tutor = SoM-Tutor ⊕ GroundFirst + Stage 0 Screen-Ordering), off-the-shelf, không fine-tune. **Input router:** **N=1** → đơn bước (DG1, MobileViews màn-0); **N≥2** → bật chế độ sắp-thứ-tự (DG2). Một hệ duy nhất, N=1 chỉ là Stage-0 rỗng.
4. **Ablation = THANG BẬC C0–C4** (không phải A/B): mỗi bậc thêm 1 cơ chế để tách "cơ chế nào thực sự trả công".
5. **6 pha có cổng (P0–P4, có P2b):** ba cổng cứng = K1 (recall), KZ′ (prior-art sắp-ảnh), KN (histogram độ dài episode). Bộ kill-test gồm K1, KN, KZ′, KB (chống leak step-index) + K3–K8.
6. **Ngân sách:** 1 GPU 24GB + ~$100–300 API. Future-work: chấm định lượng tiếng Việt + world-model tự-train.

---

> Tổng hợp sau 5 vòng multi-agent (nghiên cứu → review citation → thiết kế pipeline → red-team khả thi → review mạch lạc).
> File này **khoá** phạm vi, metric, dataset, pipeline, thứ tự làm.
> ⚠️ **THẨM QUYỀN:** File 05 (bản này — đã hợp nhất spec đa-bước-hai-tầng) là **nguồn-sự-thật**; khi mâu thuẫn với report 01–04, **file 05 thắng**.
> Trạng thái: **GO — phạm vi đã thu hẹp + đã khoá để ablation công bằng; suy luận trật tự màn (Screen-Order Inference) nay là nhánh DG2 vào scope chính.** Không vòng review nào đánh giá "broken".

---

## 1. PHÁT BIỂU LUẬN VĂN (đóng khung để kết quả ÂM vẫn ĐẬU)

> **Hai đóng góp song hành.** Trục phân định = "CÓ gold trajectory để chấm hay KHÔNG" (KHÔNG dùng trục "reference-free vs reference-based" làm trục gốc, vì DG2 vẫn so gold).
> **Thuật ngữ (giải thích đời thường):** *gold trajectory* = chuỗi thao tác đúng do dataset cung cấp; *teacher-forced* = mỗi bước cho model thấy MÀN THẬT của đáp án rồi mới đoán bước kế (Tier A — trục tham chiếu chuẩn ngành); *Screen-Order Inference* = đưa model **N ảnh đã bị XÁO TRỘN** của một luồng đa bước + mục tiêu, model phải **suy ra thứ tự đúng** rồi sinh hướng dẫn theo thứ tự đó; *ORACLE-ORDER* = cho model N ảnh ĐÃ sắp đúng (skyline của trục trật tự); *SELF-ORDER* = model tự xếp từ N ảnh xáo trộn rồi mới sinh.

### DG1 — Đánh giá tutorial trên màn-0, KHÔNG có gold tutorial của người
**"Một khung đánh giá tutorial cho `ảnh + câu hỏi → hướng dẫn từng bước trên màn hình thấy được`, *neo trên View Hierarchy (silver)*, *có điều kiện theo recall của detector*; kèm một thí nghiệm phản nghiệm có kiểm soát: cơ chế *grounding cấu trúc* (Set-of-Mark + từ-vựng-đóng + verifier tồn-tại) có **thực sự** giảm hallucination / tăng grounding so với VLM end-to-end không, và **vì sao**."**

> **Định nghĩa hẹp BẮT BUỘC (đừng để "reference-free" đứng trần):** *reference-free* ở đây CHỈ có nghĩa **KHÔNG có tutorial gold do người viết** để so. VẪN có **anchor cấu trúc VH-silver** (mỏ neo "bạc" — đúng phần lớn nhưng có nhiễu nhãn) để chấm grounding/hallucination. Mỗi lần dùng cụm "reference-free" phải kèm đúng định nghĩa hẹp này.

> **VÍ DỤ EX-A — DG1 chấm thế nào (app eTax, màn-0) (ví dụ minh hoạ tự soạn — không phải record thật):**
> - *Đầu vào:* 1 ảnh màn hình eTax + câu hỏi "Tôi muốn tra cứu đã nộp thuế chưa thì vào đâu?".
> - *Model sinh:* "1. Click nút **Tra cứu**; 2. Chọn **Nghĩa vụ thuế**; 3. Mở **Cài đặt** để xem lịch sử."
> - *Chấm grounding (point-in-bbox):* điểm model định click cho nút "Tra cứu" = **(405, 915)**. Bounding box của nút "Tra cứu" trên VH = **[270, 820, 540, 1010]**. Vì 270 ≤ 405 ≤ 540 và 820 ≤ 915 ≤ 1010 → điểm nằm trong box → **TRÚNG** (grounded = 1).
> - *Chấm hallucination (HER):* tutorial nhắc 3 nút. Hai nút ("Tra cứu", "Nghĩa vụ thuế") **có** trong VH; nút "Cài đặt" **KHÔNG hề có** trên màn này (cả ảnh lẫn VH đều không có) → đây là **bịa thật** → tính vào hallucination. **HER = 1/3 ≈ 0.33** (1−HER ≈ 0.67).
> - *Một BIÊN KHÁC (đừng nhầm với trên):* nếu model nhắc một nút **có thật trên ảnh** nhưng VH lại **thiếu nhãn** cho nút đó, thì lỗi có thể ở VH chứ không phải tutorial → **KHÔNG auto-tính hallucination**; đưa nút đó vào **subset VH đã làm sạch** (§3.8) rồi mới chấm. (Ví dụ chính ở trên là trường hợp đầu — bịa thật; biên này là trường hợp thứ hai — nghi lỗi nhãn.)

### DG2 — Đánh giá suy luận trật tự màn (Screen-Order Inference) trên AndroidControl (CÓ gold trajectory)
**"Một đánh giá năng lực *suy luận trật tự màn*: đưa model **N ảnh đã XÁO TRỘN** của một luồng đa bước trong AndroidControl (NeurIPS 2024) + mục tiêu, model phải (1) **suy ra THỨ TỰ đúng** của các màn, (2) **sinh hướng dẫn từng bước** theo thứ tự đó."** Đây là bài toán đặt ra để **đo năng lực suy luận trật tự** (trả lời thẳng câu hỏi của thầy "làm sao model biết trật tự?"), KHÔNG khẳng định là nhu cầu deploy phổ biến.

- **Headline = Kendall τ-b** (đo độ tương quan thứ tự model-suy-ra với thứ tự gold) chấm theo **thứ-tự-bộ-phận (partial-order-aware)** — đây là QUYẾT ĐỊNH đã chốt, bắt buộc: chỉ **PHẠT khi sai cặp BẮT BUỘC** (gating / drill-down: đảo là sai thật); cặp **TỰ-DO** (vd điền Email/SĐT trước-sau đều được) **đảo vẫn tính ĐÚNG**. → headline τ-b chỉ tính trên **cặp bắt buộc**. Báo THÊM **τ-b-thô** (so thứ tự gốc trên toàn tập, không phân loại cặp) làm **ĐIỂM SÀN** (robustness).
- **Phụ:** **pairwise-order-accuracy** + **position-accuracy@correct-place**. **BỎ Exact-Order-Match khỏi headline** (N=3 EM≈17% là ngẫu nhiên; N≥6 ≈0).
- **Loại N≤2** (N=2 chỉ có 1 cặp → τ-b chỉ nhận {−1,+1}, vô nghĩa). Trục N thực tế **N ∈ [3, ~10]**; phải tự đếm histogram độ dài episode để biết số episode còn lại mỗi mốc N (việc tuần-1, cổng KN).
- **Trục tham chiếu chuẩn ngành — Tier A teacher-forced (GIỮ NGUYÊN):** mỗi bước bộ chấm đưa MÀN THẬT của đáp án vàng, model đoán thao tác kế, so gold. Metric: **Action-Type accuracy**, **Grounding@14%** (điểm click đúng nếu nằm trong ngưỡng 14% kích thước màn), **Step-SR**. *(Đây là DỤNG CỤ ĐO cận-trên chuẩn ngành — thầy expect — KHÔNG còn là "đa bước chính"; KHÔNG claim ngang leaderboard.)*
- **Chất lượng tutorial vẫn chấm ĐẦY ĐỦ mỗi màn** sau khi đã sắp: grounding (point-in-bbox), hallucination (HER + coverage), format (IFEval). Vì đã sắp chuỗi rồi mới chấm từng màn (không đoán mù) nên **mạnh hơn** các thiết kế cũ đoán-mù.
- **Baseline bắt buộc:** **GOAL-ONLY** (che hết ảnh, chỉ đưa goal + nhãn trong: nếu goal-only đã xếp đúng cao thì cue giao diện KHÔNG phải nguồn tín hiệu) + **RANDOM-ORDER** (sàn ngẫu nhiên).

> **Đóng góp CHÍNH của DG1 = một quy trình ĐÁNH GIÁ** (không phải "hệ thống của tôi thắng"). DG2 bổ sung trục **suy luận trật tự màn** + Tier A chuẩn ngành làm tham chiếu.

> **VÍ DỤ EX-B — DG2 Screen-Order Inference (app Đồng hồ, goal "đặt báo thức 7:00") (ví dụ minh hoạ tự soạn — không phải record thật; phỏng theo format action thật, nội dung app/giờ tự dựng):**
> - *Gold trajectory (đáp án dataset cung cấp):* **B1** mở tab "Báo thức" → **B2** bấm nút "+" → **B3** gõ 07:00 rồi bấm OK. (3 bước)
> - *Đầu vào DG2 (xáo trộn):* model nhận 3 ảnh màn **theo thứ tự lộn xộn** {B2, B3, B1} + goal, **đã strip metadata + tái mã hoá + đặt tên UUID** (chống leak step-index — cổng KB).
> - *SELF-ORDER (thật):* model suy ra thứ tự đúng dựa vào **ordering cues** — nhận ra B1 là tab "Báo thức" (gating: phải mở danh sách trước), B2 nút "+" (nav-affordance: thêm mới), B3 form nhập giờ (drill-down: chi tiết của thao tác "+"). Model xếp **B1 → B2 → B3** → khớp gold → τ-b = +1 trên các cặp bắt buộc.
> - *Cặp bắt buộc vs tự-do:* (B1, B2) là **bắt buộc** (gating — đảo là sai); nếu app có 2 trường nhập độc lập, cặp đó là **tự-do** (đảo vẫn tính đúng).
> - *ORACLE-ORDER (skyline):* nếu cho model 3 ảnh ĐÃ sắp đúng + goal rồi chỉ việc sinh hướng dẫn → chất lượng tutorial cao hơn. **ordering gap** = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER) = "cái giá của việc không biết trật tự" (xem §5.6).
> - *Lưu ý đọc số:* nếu GOAL-ONLY cũng xếp đúng B1→B2→B3 thì việc xếp đúng đến từ **suy luận theo mục tiêu**, KHÔNG phải từ cue giao diện — phải báo cả hai (xem §5.x, §10).

- ✅ **Kết quả DƯƠNG (DG1)** → "grounding cấu trúc có ích, lượng hoá được mức ích lợi."
- ✅ **Kết quả ÂM (DG1)** → vẫn ĐẬU **nếu pre-register**: "grounding cấu trúc *không* cải thiện faithfulness đo được một khi đã kiểm soát recall — và đây là cơ chế: recall detector chặn trần lợi ích" + đường cong recall-vs-grounding. → **một null được mô tả cơ chế LÀ đóng góp**; một "không thắng baseline" không-giải-thích thì không.
- ✅ **Kết quả ÂM (DG2) — KHÔNG được là tautology:** không được phát biểu "kết quả nào cũng là phát hiện". Phải pre-register **giả thuyết CÓ THỂ BỊ BÁC + ngưỡng trên trục τ-b**: ví dụ "**τ-b (cặp bắt buộc) của SELF-ORDER cao hơn RANDOM-ORDER một mức effect-size đăng-ký-trước**", kèm **ngưỡng CI-width tối đa** để con số được coi là "đọc được". Nếu SELF-ORDER **không** vượt RANDOM-ORDER quá CI, hoặc GOAL-ONLY đã cao bằng SELF-ORDER (cue giao diện vô dụng) → **DG2 FAIL CÓ Ý NGHĨA** (kết luận: model không suy luận được trật tự từ tín hiệu màn ở quy mô này). Có vậy mới là null thật.
- **Bắt buộc (cả DG1 lẫn DG2):** nêu **giả thuyết + ngưỡng effect-size + quy tắc quyết định TRƯỚC khi chạy** (pre-registration), **dồn power vào 1 trục = τ-b ordering** cho DG2.

### Đặt tên chính xác (đừng overclaim "reference-free")
Dùng nguyên văn xuyên suốt: **"reference-free theo nghĩa hẹp = KHÔNG có tutorial gold của người; vẫn neo VH-silver cho grounding/hallucination; model-judged cho clarity/intent."** **Task Success NAY IN-SCOPE** qua **AndroidControl Tier A** (có gold, reference-based) — không còn để future-work; CHỈ phần **MobileViews màn-0 (DG1)** mới là không-gold-tutorial. Audit **nhiễu nhãn VH** trên 20 màn, báo tỷ lệ lỗi nhãn (VH là *silver*, không phải gold).

---

## 2. PHẠM VI ĐÃ KHOÁ

| | Trong luận văn (spine) | Future-work (ghi rõ, KHÔNG hứa số) |
|---|---|---|
| Màn hình | **màn-0 (DG1) + suy luận trật tự màn từ N ảnh xáo trộn trên AndroidControl (DG2); Tier A teacher-forced làm trục tham chiếu chuẩn ngành** | **world-model tự-train** (suy luận màn kế có huấn luyện) |
| Ngôn ngữ chấm | **EN/ZH (MobileViews + AndroidControl)** | tiếng Việt (chỉ động cơ + sanity-check OCR + demo định tính) |
| Model | **off-the-shelf, KHÔNG fine-tune**; Qwen2.5-VL-7B (+ tùy chọn slice GPT-4o) | AGENT-NSI world-model (cần train); 72B |
| Nền tảng | mobile: **MobileViews + AndroidControl + ScreenSpot(-v2)** (đối chứng grounding) | web (Mind2Web) |
| Task Success | **Step-SR reference-based trên AndroidControl Tier A** (có gold, trục tham chiếu) | chấm định lượng tiếng Việt |

> **INPUT ROUTER (một hệ duy nhất, hợp đồng sản phẩm):** **N=1 ảnh** → đơn bước (DG1 nguyên vẹn, MobileViews màn-0); **N≥2 ảnh** → bật chế độ sắp-thứ-tự (DG2 — Stage-0 Screen-Ordering). N=1 chính là Stage-0 rỗng → về pipeline cũ. Người dùng vẫn chỉ thấy `ảnh + câu hỏi → hướng dẫn`; chế độ N-ảnh là **bài toán đặt ra ĐỂ ĐO năng lực suy luận trật tự**, không khẳng định là nhu cầu deploy phổ biến.

---

## 3. METRIC ĐÃ KHOÁ (sửa các lỗi ăn-khớp vòng coherence)

**Quy ước hướng điểm:** mọi metric = **faithfulness, cao = tốt** (1−HER, grounded-rate, point-in-bbox acc, IFEval, G-Eval 1–5) → Spearman/Kendall không cần lật dấu.

### 3.1. Tách "metric chấm" khỏi "verifier vận hành"
> **NHẤN (chống hiểu nhầm CỐT LÕI):** cơ chế chống-bịa **CHÍNH** nằm ở khâu **SINH có ràng buộc** (constrained generation) — model bị **ép chỉ được cite ID nằm trong tập element `E`** đã phát hiện từ ảnh; nó **không thể** sinh ra một ID không có trong `E`. Ba tầng verifier **V1/V2/V3 là lưới chắn ĐẰNG SAU**, không phải cơ chế chính. Đừng để người đọc hiểu nhầm "chống bịa = nhờ một LLM khác đi verify". Cụ thể:
> - **V1 = CODE THUẦN (KHÔNG LLM)** — chỉ so khớp membership `[#id]∈E`. Vì constrained generation đã ép từ lúc sinh nên V1 gần như luôn đậu; **vẫn cần làm để chốt an toàn** cho các trường hợp lọt lưới (trường tự do/profile do model tự điền, hậu kiểm sau refine).
> - **V2 = một LLM KHÁC** (khác họ với generator) — kiểm **đúng-ý/intent**: element được cite có đúng mục tiêu câu hỏi không.
> - **V3 = tự sửa (self-refine) ≤ 2 lần.**
>
> **Đời thường:** đừng tự chấm điểm bằng chính cây thước mình đã ép. Phải chấm bằng một mỏ neo độc lập (VH).

- **V1** (kiểm tra `[#id]∈E` — ID model cite có nằm trong tập detector E không) = **cổng vận hành nội bộ**, báo riêng dưới tên *"pipeline self-consistency"*.
  - **KHÔNG phải số hallucination headline.** Vì constrained decoding đã *ép* model chỉ cite ID có trong E, nên V1 gần như **luôn ≈ 100%** → làm metric thì vô nghĩa (giống tự ra đề rồi tự chấm đậu).
- **Metric hallucination thật để báo = HER (1−HER) + coverage, so với lá VH** (mỏ neo độc lập), **KHÔNG so với E** (tập detector).
  - Chỉ HER-vs-VH mới bắt được hallucination *gốc-detector* (vd nút detector bịa ra nhưng VH không có).

### 3.2. Chấm CẢ HAI nhánh trên CÙNG mỏ neo (tránh HER vòng tròn)
- HER & coverage của **cả SoM-Tutor lẫn baseline** chấm so với **cùng một tập tham chiếu cố định = toàn bộ lá VH tương tác**, **không** so với tập E riêng của mỗi nhánh (nếu không, SoM bị ép về HER≈0 do cấu trúc, baseline bị chuẩn khắt khe hơn → không công bằng).
- **Control "detector-shared-blindspot":** báo HER **gồm và loại** các lá VH mà OmniParser không thấy → để artifact từ-vựng-đóng *hiện ra*, không bị giấu.

### 3.3. Resolver đối xứng (tránh confound grounding)
- **Cùng một resolver/matcher** (đã freeze) chấm grounding cho **cả hai** nhánh. ID→bbox lookup của SoM **chỉ báo như một dòng "oracle upper-bound" riêng**, KHÔNG phải số grounding headline của SoM (nếu không, "thắng" có thể chỉ là lỗi resolver của baseline).

### 3.4. Định nghĩa lá VH chuẩn (3 metric ngầm phụ thuộc)
**Lá = node có (`text/label` ≠ rỗng HOẶC cờ tương tác clickable/editable/scrollable) VÀ không có hậu duệ có-nhãn/tương-tác; gộp bbox lồng trùng.** Dùng **chung** cho HER (tử số mention) và coverage (mẫu số) — **không** đếm mọi node (node trang trí/container làm coverage 100% bất khả).

### 3.5. Matcher khoá & validate trước
- **Một matcher ALOHa-style (embedding + Hungarian)**, **không** string-match ngây thơ; chạy **EN và ZH riêng** (matcher ZH-aware). **Validate trên subset gán tay TRƯỚC khi báo HER/coverage** (báo tỷ lệ false-pos/neg). Luôn báo **HER & coverage thành cặp**.

### 3.6. IFEval công bằng 2 nhánh
- **Checklist trung-lập-nội-dung** (đánh số · động từ mệnh lệnh đầu bước · 1 action/bước) áp **cho cả hai nhánh** → điểm format headline. Ràng buộc "có `[#id]`" báo **riêng như thuộc tính cấu trúc của SoM**, KHÔNG vào so sánh format.

### 3.7. Intent: chọn 1
- **HOẶC** thêm metric intent-correctness có chấm (judge text-only nuốt VH, hoặc 1 chiều BWS "element có đúng mục tiêu") **HOẶC** **loại intent khỏi phát biểu phản nghiệm** và nói rõ "spine chỉ đo tồn-tại/grounding". *(Khuyến nghị: thêm 1 chiều BWS goal-appropriateness — rẻ, và làm pilot người có ích hơn.)*

### 3.8. Hai trần recall xếp chồng
Có **hai cái "trần"** giới hạn độ tin của mọi số grounding/HER — phải khai báo cả hai:
- **Trần 1 — detector không thấy hết (K1):** OmniParser chỉ phát hiện ~một phần element → mọi số đóng khung **"có điều kiện recall detector = X%"**.
- **Trần 2 — nhãn VH có thể thiếu:** đôi khi OmniParser thấy một element rõ ràng nhưng VH lại **không có** nhãn cho nó.
  - *Cách xử lý:* trường hợp này **đừng auto-tính hallucination** (vì lỗi có thể ở VH, không phải ở tutorial).
  - Đưa các element kiểu này vào **subset VH đã làm sạch** = mỏ neo tin cậy để chấm HER/coverage.
  - *Ví dụ (nối EX-A) (minh hoạ):* nút "Cài đặt" mà model nhắc — nếu OmniParser thấy nó nhưng VH thiếu nhãn, ta không kết luận ngay là bịa, mà soi vào subset đã làm sạch trước.

---

## 4. DATASET ĐÃ KHOÁ

- **MobileViews screen-0** (preprint — ghi rõ phiên bản v1/v3 khi trích), JSON VH có `viewClass`/`text-label`/`bounds[l,t,r,b]` pixel/cờ tương tác → **mọi metric DG1 tính được, không thiếu field nào** (đã xác nhận). Vai: **màn-0 (DG1)**.
- **AndroidControl (NeurIPS 2024, peer-reviewed):** episode đa bước + gold action mỗi bước → **DG2 (suy luận trật tự màn) + Tier A teacher-forced**. Đây là nguồn gold trajectory cho cả đánh giá suy luận trật tự (xáo trộn N ảnh rồi đo τ-b) lẫn trục tham chiếu chuẩn ngành (Tier A teacher-forced). **Đã khảo sơ bộ:** 15,283 episode, 833 app, train 13,604 ep / 74,722 step, mean ~5.5 step/episode (Table 1 ghi 4.8; tính lại từ train = 5.49), percentile-5 = 1 step, percentile-95 = 13 step (Li et al., "On the Effects of Data Scale on UI Control Agents", NeurIPS 2024 D&B, arXiv 2406.03679). Dataset **không** đếm sẵn số episode theo từng N → phải **tự đếm histogram** (cổng KN). Trục N thực tế **N ∈ [3, ~10]**.
  - *Record episode THẬT (gold, DÙNG LÚC CHẤM — không phải minh hoạ):* goal = "On cruisedeals, view cruise schedules for a four-night trip from New York to Canada" → **B1** `{action_type: open_app, app_name: CruiseDeals}` → **B2** `{action_type: click, x: 313, y: 742}` → **B3** `{action_type: swipe, direction: up}`. (Nguồn: Google Research `android_control` README.) Lưu ý format: action `click` lưu **toạ độ (x, y)** chứ không phải bbox.
- **ScreenSpot / ScreenSpot-v2 (đối chứng grounding):** **ScreenSpot gốc = SeeClick (ACL 2024, peer-reviewed)**; **ScreenSpot-v2 = OS-Atlas (ICLR 2025, peer-reviewed)**. Vai: **đối chứng grounding** + bù credibility cho MobileViews (preprint). ⚠️ ScreenSpot CHỈ đối chứng **đơn vị point-in-bbox accuracy của resolver**, KHÔNG đối chứng pipeline tutorial nhiều bước. (Ghi đúng venue theo bản dùng — đừng gộp "-v2" vào ACL 2024.)
  - *Mẫu THẬT (gold, không phải minh hoạ):* instruction = "close"; bbox = **[0.948, 0.144, 0.994, 0.207]** (chuẩn hoá 0–1, dạng `x_min, y_min, x_max, y_max`); `data_type` = "icon"; source = Windows (icon đóng cửa sổ). (Nguồn: `rootsautomation/ScreenSpot` trên HuggingFace.) Lưu ý format: bbox **chuẩn hoá 0–1**, khác hẳn pixel.
- **AITW (NeurIPS 2023) — PHÂN VAI ĐÔI:** (a) **NGUỒN NGƯỠNG 14%** (Grounding@14% = điểm click coi là đúng nếu nằm **trong ~14% khoảng cách màn HOẶC cùng bounding box** với điểm gold — quy ước AITW) = trích **BẮT BUỘC** (citation), KHÔNG tùy chọn; (b) **dataset đối chứng** = **TÙY CHỌN**. Ghi rõ: protocol tách Type/Grounding/SR (OS-Atlas) là **preprint** → trích như **hiện vật kỹ thuật**, không trình như peer-reviewed.
- **Mind2Web = future-work** (nhánh web), KHÔNG vào scope chính.
- **Khung điều kiện recall** (mỗi số kèm "recall=X%", cổng K1) áp cho **CẢ MobileViews, ScreenSpot VÀ AndroidControl (DG2 + Tier A)**.
- ⚠️ **CÂU HỎI USE-CASE PHẢI TỰ SOẠN:** MobileViews **không có** câu hỏi use-case; ScreenQA v1 là Q&A *nội dung màn* ("pin bao nhiêu %"), **sai thể loại** (mô tả, không phải thủ tục "làm sao để X"), lại chỉ ~13K/600K màn. → **tự viết câu hỏi thủ tục**; có thể *mồi* từ ScreenQA nhưng phải đổi sang dạng "làm sao để…". Ghi rõ trong luận văn: **câu hỏi do tự soạn**, có protocol + số lượng.
  - **Phạm vi "tự soạn" (làm rõ):** việc tự soạn câu hỏi use-case **CHỈ áp cho MobileViews (màn-0, DG1)**. **AndroidControl** đã có sẵn `goal`/`instruction` cho mỗi episode, **ScreenSpot** đã có sẵn `instruction` cho mỗi mẫu → **KHÔNG cần (và không được) tự soạn** cho hai bộ này.
  - **"Tự soạn câu hỏi" ≠ "sinh dữ liệu tổng hợp":** ta CHỈ viết phần **INPUT** (câu hỏi) cho một bức ảnh có sẵn; **đáp án để chấm** (bbox lá VH của MobileViews, gold action của AndroidControl, bbox của ScreenSpot) **vẫn là dữ liệu THẬT từ dataset** — ta không bịa ra ground-truth. Đây là việc luận văn **TRÁNH** (không tạo dữ liệu/đáp án tổng hợp).
- Giới hạn slice đánh giá vào **màn có task thủ tục hợp lý**. Dùng **subset VH đã làm sạch** làm mỏ neo HER/coverage.
- ⚠️ **BA BỘ — BA FORMAT TOẠ ĐỘ KHÁC NHAU (dễ nhầm khi code chấm):**
  - **MobileViews:** bbox **pixel** dạng `[left, top, right, bottom]` (vd root bounds thật = `[0, 0, 1080, 1920]`).
  - **ScreenSpot (HF):** bbox **chuẩn hoá 0–1** dạng `[x_min, y_min, x_max, y_max]`.
  - **AndroidControl:** action `click` lưu **toạ độ điểm (x, y)** (pixel), KHÔNG phải bbox.
  - → **Harness BẮT BUỘC convert về cùng hệ toạ độ TRƯỚC khi** chấm point-in-bbox / Grounding@14% (nếu trộn pixel với 0–1 hoặc nhầm thứ tự trục thì mọi số grounding sai mà không báo lỗi).

---

## 5. PIPELINE ĐÃ KHOÁ + ABLATION THANG BẬC

### 5.1. Ablation = THANG BẬC (factor ladder), KHÔNG phải A/B
Vì SoM-Tutor gộp 4 thay đổi cùng lúc, một A/B không quy được công cho cơ chế nào. Chạy **5 điều kiện**, mỗi bậc thêm 1 cơ chế:

| ĐK | Cấu hình | Cô lập điều gì |
|---|---|---|
| **C0** | E2E VLM, **không** refine | sàn thô |
| **C1** | E2E + self-refine | **baseline/control chính** (report 03 gọi là baseline) |
| **C2** | + Set-of-Mark overlay (mark trên ảnh, target tự do, **chưa** constrained, **chưa** V1) | mark **một mình** có ích không |
| **C3** | + constrained-decode tới ID đã phát hiện + verifier tồn-tại V1 | đóng góp **cấu trúc/membership** |
| **C4** | + intent-critic V2 (= SoM-Tutor đầy đủ) | đóng góp **intent** |

→ Báo delta **C1→C2→C3→C4**: "cơ chế nào *thực sự* trả công". Đây mới là phát biểu phản nghiệm.

*Ví dụ minh hoạ cách đọc delta (số giả định):* nếu HER giảm C1→C2 = −2 điểm (Set-of-Mark một mình ít tác dụng), C2→C3 = −9 điểm (constrained-decode + verifier tồn-tại là cơ chế trả công chính), C3→C4 = −1 điểm (intent-critic gần như không thêm gì cho hallucination) → kết luận: lợi ích đến từ **bậc C3**, không phải từ việc gắn mark. Đây là kiểu kết luận mà một A/B đơn không thể đưa ra.

### 5.2. Điều kiện công bằng (khoá nguyên văn)
- **Cùng base VLM** cả 2 nhánh (Qwen2.5-VL-7B chính; tùy chọn slice GPT-4o chạy y hệt 2 nhánh).
- **Cùng** K=2, **cùng** stop-on-no-change, **cùng** output JSON schema, **cùng** resolver chấm (đối xứng, §3.3).
- **Self-refine critic giống hệt** giữa C1 và C4 (chỉ khác sự hiện diện của SoM/V1/V2).
- **Inferred/SelfCheckGPT TẮT** khỏi đường chi phí spine.
- **Phạm vi "delta headline" (tách riêng cho rõ):** delta headline (C1→C4) **CHỈ áp cho DG1 (màn-0)**. Suy luận trật tự màn **KHÔNG bị loại khỏi đánh giá** — nó được **đo riêng** bằng metric DG2 (headline **Kendall τ-b** partial-order-aware + τ-b-thô; phụ pairwise-order-accuracy + position-accuracy@correct-place; **ordering gap** = ORACLE-ORDER − SELF-ORDER) và **Tier A teacher-forced** (Action-Type/Grounding@14%/Step-SR) làm trục tham chiếu, có bảng kết quả riêng. Tức là: delta C1→C4 thuộc bảng DG1; trật tự màn thuộc bảng DG2.

### 5.3. Ma trận gán model (chống shared-error, ép bằng assert)
`generator ≠ intent-critic(V2) ≠ judge-hallucination(text-only nuốt VH, KHÔNG ảnh) ≠ judge-G-Eval` — 4 họ model khác nhau; CI assert `id` khác nhau. Ghi ma trận vào phần phương pháp như một *control*.

### 5.4. Pin phiên bản
**Một build OmniParser V2 (commit hash) duy nhất** dùng cho **CẢ** K1 (đo recall) **VÀ** nhánh SoM ở mọi điều kiện — nếu khác version thì "recall-conditioned" vô hiệu.

### 5.5. Tái dùng pipeline cho hai chế độ (một hệ, input router N=1 / N≥2)
ReOrder-Tutor (SoM-Tutor + GroundFirst + **Stage 0 Screen-Ordering**) là **MỘT hệ duy nhất**, chạy lại ở hai chế độ qua input router:
- **(a) Màn-0 (DG1) — N=1:** Stage-0 rỗng → chạy **1 lần** pipeline 5 bước trên màn thấy được.
- **(b) Stage-0 Screen-Ordering (DG2) — N≥2:** nhận **N ảnh xáo trộn** → **S0a per-screen feature** (tái dùng parser Stage-1/M1, không thêm module) → **S0b ordering reasoner** (CHÍNH = **pairwise-then-aggregate**: mỗi cặp hỏi VLM "màn nào trước?" + bắt trích ≥1 ordering cue → tổng hợp bằng **Copeland score**; **listwise** 1-call ép permutation làm ĐỐI CHỨNG chạy fair-compute) → **S0c order verifier** (code thuần, không LLM; chu trình mâu thuẫn → min-feedback-arc-set xấp xỉ) → chuỗi đã sắp chạy **pipeline 5 bước cũ TRÊN từng màn** → grounding chấm ĐẦY ĐỦ mọi bước (mạnh hơn vì không đoán mù).
- **Trục tham chiếu — Tier A teacher-forced:** chạy **từng bước** trên màn thật của gold để đo Action-Type/Grounding@14%/Step-SR (chuẩn ngành, skyline phần thao tác).

**5 ORDERING CUES** (trả lời câu hỏi thầy "model dựa vào đâu để biết trật tự"): **gating** (đăng nhập/cấp quyền trước) · **nav-affordance** (Next/Back/breadcrumb) · **state-delta** (toggle off→on, ô trống→đã điền, badge 0→1) · **title-progression** (tiêu đề theo phiếu) · **drill-down** (màn sau = chi tiết item màn trước). **Signal-attribution = STRATIFICATION cấp một-cue** (chỉ giữ cặp phân biệt bởi ĐÚNG MỘT cue, đo acc theo nhóm cue — KHÔNG che pixel vì che pixel tạo artifact) + **phân tích lỗi mở** (đọc cặp xếp sai). Baseline **GOAL-ONLY** (che hết ảnh, chỉ goal+nhãn trong: goal-only đã cao → cue giao diện không phải nguồn tín hiệu) + **RANDOM-ORDER** (sàn ngẫu nhiên).

### 5.6. Metric suy luận trật tự (DG2) phải WELL-DEFINED
Trước khi gọi DG2 là "metric" thật, phải khoá các điều kiện sau:

- **Headline = Kendall τ-b**, chấm **partial-order-aware** (chỉ phạt cặp BẮT BUỘC = gating/drill-down; cặp TỰ-DO đảo vẫn tính ĐÚNG). Headline τ-b **chỉ tính trên cặp bắt buộc**; báo THÊM **τ-b-thô** (so thứ tự gốc trên toàn tập, không phân loại cặp) làm **ĐIỂM SÀN** robustness. **Phụ:** pairwise-order-accuracy + position-accuracy@correct-place. **KHÔNG** dùng pairwise-acc thô làm headline (tautology); **BỎ Exact-Order-Match khỏi headline**.
  - *Phân loại cặp bắt buộc/tự-do:* dựa trên phát hiện **gating/drill-down** (trùng ordering-cues). *Ví dụ (nối EX-B):* (B1 mở tab → B2 "+") là **bắt buộc** (gating); hai trường nhập độc lập (Email/SĐT) là **tự-do** (đảo vẫn đúng).
- **Loại N≤2** (N=2 chỉ 1 cặp → τ-b chỉ nhận {−1,+1}, vô nghĩa). Trục N thực tế **N ∈ [3, ~10]**, báo số episode còn lại mỗi mốc N (việc tuần-1, cổng KN).
- **Chống leak step-index (cổng KB):** ảnh xáo trộn PHẢI **strip metadata + tái mã hoá ảnh + đặt tên UUID**; CI test: detector mù chỉ xem pixel KHÔNG suy ra thứ tự tốt hơn ngẫu nhiên.
- **Tái dùng hạ tầng chấm:** chất lượng tutorial từng màn (grounding/HER/coverage/IFEval) dùng **CÙNG matcher freeze + resolver đối xứng** như DG1 (không chế bộ chấm riêng).
- **RAW vs ORACLE (báo cả hai):** RAW = số thực; ORACLE = giả định resolver hoàn hảo (bước đổi ID→toạ độ luôn đúng, để tách lỗi resolver khỏi lỗi suy luận). Báo **cả hai** cho **cả DG2 và Tier A**.

### 5.7. ORDERING GAP + sanity ORACLE ≥ SELF
- **ORACLE-ORDER (skyline):** cho model **N ảnh ĐÃ sắp đúng** + mục tiêu → chỉ sinh hướng dẫn (không phải tự xếp). Là cận-trên.
- **SELF-ORDER (thật):** **N ảnh xáo trộn** → model tự xếp rồi mới sinh.
- **ordering gap = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER)** = "**cái giá của việc không biết trật tự**".
- **Sanity cứng:** **ORACLE-ORDER ≥ SELF-ORDER ở MỌI episode** (vi phạm = bug).
- ⚠️ **Cảnh báo floor-effect:** gap chỉ có nghĩa nếu metric tutorial NHẠY với thứ tự; nếu không → **τ-b là trục chính, gap chỉ phụ**.

---

## 6. THỨ TỰ THỰC HIỆN — 6 PHA CÓ CỔNG (DAG, không phải checklist phẳng)
> Pha k+1 **không được bắt đầu** trước khi Pha k đạt "Definition of Done" (DoD).

> *Bộ kill-test đầy đủ: K1, KN, KZ′, KB + K3–K8 (chi tiết từng cái ở báo cáo 04). Cổng CỨNG: **K1** (recall), **KZ′** (prior-art sắp-ảnh), **KN** (histogram độ dài episode AndroidControl). **KB** = chống leak step-index. K3 (OCR tiếng Việt) chạy ngoài luồng chính vì tiếng Việt là future-work.*

| Pha | Việc | DoD / Cổng |
|---|---|---|
| **P0 — Môi trường & pin** | dựng env; pin OmniParser V2 (commit); vLLM Qwen2.5-VL-7B; xác nhận GPT-4o Structured-Outputs enum (K6); viết ma trận gán model | 7B load <22GB/24GB (K4); enum ép ID giả không lọt; build hash ghi lại |
| **P1 — CỔNG K1 RECALL (cứng) + KZ′ + KN** | đo recall OmniParser vs lá VH tương tác trên 30–50 màn; **đo riêng recall trên element mà câu hỏi nhắm tới**. **KZ′ (prior-art sắp-ảnh, cứng):** rà related-work gần nhất (Sort-Story EMNLP 2016 · "Sequencing Multimodal Instructional Manuals" ACL 2022 · RankGPT EMNLP 2023 · sentence-ordering Gong AAAI 2018 · Screen2Vec CHI 2021) TRƯỚC khi đóng khung độ mới. **KN (histogram độ dài episode, cứng):** TỰ ĐẾM histogram số bước/episode trên AndroidControl để biết số episode còn lại mỗi mốc N∈[3,~10] | **K1:** có 1 số X%; nếu <~80% → "recall-conditioned" + metric false-negative; **mọi caption bảng phải có X%**. **KZ′:** KHÔNG claim "xếp ảnh xáo là mới"; độ mới = (a) domain GUI màn-hình + (b) điều kiện hoá theo mục tiêu + (c) gắn ordering → SINH tutorial + (d) signal-attribution theo ordering cues; thừa nhận lineage Sort-Story/ACL2022/RankGPT. **KN:** có đủ episode N≥3 để đo τ-b (sơ bộ mean ~5.5, p95=13 → GO có điều kiện, cần đếm chính xác) |
| **P2 — Harness chấm + freeze matcher** | cài point-in-bbox, HER+coverage, IFEval, G-Eval trên bbox MobileViews; định nghĩa lá VH chuẩn; **validate matcher tay >80% (K7) rồi FREEZE**; nối **cùng** resolver vào CẢ 2 nhánh | metric phân biệt tutorial tốt vs hỏng-cố-ý; matcher đông cứng trước khi chấm bất kỳ điều kiện nào; câu hỏi use-case đã soạn xong cho dev set; xác nhận convert toạ độ 3-format đúng (test 1 mẫu/bộ) |
| **P2b — Harness chấm ordering (DG2)** | xây bộ xáo trộn N ảnh **có cổng KB** (strip metadata + tái mã hoá + UUID); bộ chấm **Kendall τ-b partial-order-aware** (phát hiện cặp bắt buộc gating/drill-down) + τ-b-thô + pairwise/position-acc; **stratification cấp một-cue** theo 5 ordering cues; hai chế độ **ORACLE-ORDER / SELF-ORDER**; baseline GOAL-ONLY + RANDOM-ORDER; thêm bộ chấm **Tier A** (Action-Type/Grounding@14%/Step-SR teacher-forced) làm tham chiếu; tái dùng matcher freeze + resolver đối xứng; báo RAW vs ORACLE | bộ xáo trộn qua CI test KB (detector mù không suy ra thứ tự); τ-b partial-order phân biệt được cặp bắt buộc/tự-do; **sanity ORACLE-ORDER ≥ SELF-ORDER mọi episode** đạt; loại N≤2 |
| **P3 — Ablation thang bậc trên DEV 50–100** | chạy C0–C4 end-to-end; chung base VLM/K/schema/resolver; K5 chiếu chi phí/item×ĐK ≤ ngân sách; short-circuit refine khi V1 sạch | 5 điều kiện chạy thông; dự phóng full sweep ≤ ~$300 |
| **P4 — Full sweep + pilot người + bảng DG2** | C0–C4 trên 500–2000 item, mọi số caption "conditioned on recall=X%"; pilot BWS (xem §7); **chạy bảng kết quả chính DG2: τ-b (SELF-ORDER vs ORACLE-ORDER) + ordering gap + signal-attribution theo cue + Tier A tham chiếu trên AndroidControl** | bảng cuối DG1 + **bảng suy luận trật tự màn (đóng góp thứ hai, KHÔNG còn là future-work)** + pilot đạt §7; chỉ VN định lượng + world-model tự-train ở mục future-work riêng |

> **VÍ DỤ đọc cổng (P1 / K1):** giả sử ở P1 ta đo recall OmniParser trên 40 màn và ra **55%** (< ngưỡng ~80%). Cổng K1 KHÔNG cho "fail dự án" — nó **chuyển khung**: trước khi sang P2, mọi caption bảng phải ghi "**conditioned on recall = 55%**", thêm metric false-negative, và phát biểu phản nghiệm đổi sang dạng "grounding cấu trúc cải thiện faithfulness *trong điều kiện recall 55%*". Chỉ khi đã đổi khung xong mới được mở Pha P2. (Tương tự, **KZ′ fail** → đóng khung độ mới theo bốn trục (a)–(d) ở P1, thừa nhận lineage Sort-Story/ACL2022/RankGPT; **KN fail** → thiếu episode N≥3 thì thu hẹp trục N hoặc gộp mốc, không bịa số.)

---

## 7. PILOT NGƯỜI — đóng khung "sanity/feasibility", KHÔNG "validate"
- N nhỏ + 3 annotator + 1 Spearman → **CI rất rộng** → KHÔNG "chứng minh metric khớp người" với độ chính xác nào.
- **Khoá:** rank tutorial từ **các hệ trong ablation** {C1, C3, C4 (±C2)} trên **M màn screen-0 cố định** (state M, vd ~40), N = M×#hệ (**N = số item**); ngân sách **số tuple T = 1.5N–2N** (**T = số tuple**, đặt tên riêng để không lẫn với N).
- Báo: **độ rộng CI bootstrap làm headline** (trung thực về độ thiếu chính xác); **Kendall τ-b** (tốt cho N nhỏ + ties) thay vì chỉ Spearman; **Krippendorff α** per-pair; **phát biểu DIRECTIONAL** ("metric & người đồng thuận thứ tự tutorial *rõ-tốt* vs *rõ-hỏng*"), KHÔNG ra 1 con ρ điểm.
- **Power:** chọn N theo nửa-độ-rộng-CI mục tiêu (kỳ vọng **≥60–80 item**, không phải 10). Nói rõ: pilot này lập **tính khả dĩ**; tương quan chặt là future-work cần panel lớn.

---

## 8. COMPUTE / NGÂN SÁCH ĐÃ KHOÁ
- **Phần cứng:** 1 GPU 24GB (RTX 4090/3090 hoặc thuê ~$0.3–0.5/h). Qwen2.5-VL-7B FP16 ~17GB. **Bỏ self-host 72B** (muốn 1 số 72B → API hosted ~30 item).
- **API:** đẩy judge sang **gpt-4o-mini** (~16× rẻ) + **Batch API** (−50%); dev set 50–100, full chỉ cho bảng cuối. **Sàn thực tế ~$100–300.** Free tier chỉ để prototype/demo.

---

## 9. NÓI GÌ VỚI THẦY (chốt)
> Em chốt **hai đóng góp song hành**. **Đóng góp thứ nhất (DG1):** **một quy trình đánh giá tutorial KHÔNG-gold-tutorial-người** (reference-free theo nghĩa hẹp = không có tutorial vàng do người viết, nhưng vẫn neo **View Hierarchy silver**, **có-điều-kiện-recall**) cho sinh hướng dẫn từ 1 ảnh **trên màn hình thấy được** (MobileViews, EN/ZH), kèm **một thí nghiệm phản nghiệm có pre-registration**: chạy **thang bậc ablation** E2E → +Set-of-Mark → +constrained-decode+verifier → +intent-critic, để tách *cơ chế nào* trong "grounding cấu trúc" thực sự giảm hallucination/tăng grounding so với baseline VLM+self-refine — **mọi số đều kèm recall thực đo của detector**, chấm cả hai nhánh trên **cùng mỏ neo VH**, đối chiếu một **panel chuyên gia BWS** (báo độ rộng CI, không hứa tương quan chặt). **Đóng góp thứ hai (DG2) — trả lời thẳng câu hỏi của thầy "làm sao model biết trật tự?":** một đánh giá **suy luận trật tự màn (Screen-Order Inference)** trên **AndroidControl (NeurIPS 2024)** — em đưa model **N ảnh ĐÃ XÁO TRỘN** của một luồng đa bước + mục tiêu, model phải **suy ra thứ tự đúng** rồi **sinh hướng dẫn theo thứ tự đó**. Headline = **Kendall τ-b** chấm **theo thứ-tự-bộ-phận** (chỉ phạt cặp **bắt buộc** như đăng-nhập-trước-xem-kết-quả; cặp **tự-do** như điền Email/SĐT đảo vẫn đúng), kèm **τ-b-thô** làm điểm sàn. Em đặt tên **5 ordering cues** (gating · nav-affordance · state-delta · title-progression · drill-down) và đo **signal-attribution** xem cue nào giúp xếp đúng. Em báo **ordering gap = ORACLE-ORDER − SELF-ORDER** ("cái giá của việc không biết trật tự"). **Tier A teacher-forced** (Action-Type/Grounding@14%/Step-SR) em giữ làm **trục tham chiếu chuẩn ngành** (skyline phần thao tác), KHÔNG trình như sản phẩm 1-ảnh, KHÔNG claim ngang leaderboard. Em **dồn power pre-registration vào 1 trục = τ-b ordering** (giả thuyết bác được: SELF-ORDER vượt RANDOM-ORDER quá CI, và GOAL-ONLY không cao bằng SELF-ORDER) nên null vẫn có ý nghĩa. **Trung thực với thầy:** chế độ N-ảnh là **bài toán em ĐẶT RA để ĐO** năng lực suy luận trật tự, sản phẩm thật vẫn `1 ảnh + câu hỏi → hướng dẫn` (input router N=1 → đơn bước). Toàn bộ off-the-shelf, không fine-tune, 1 GPU 24GB + ~$100–300. **Chỉ còn future-work:** tiếng Việt (định lượng) và world-model agentic tự-train. Trước khi finalize, em chạy 1 tuần kill-test, **quan trọng nhất là đo recall thật của OmniParser (K1)** + tự đếm histogram độ dài episode (KN) + rà prior-art sắp-ảnh (KZ′); nếu recall thấp, em đóng khung là "grounding có-điều-kiện-recall". Kể cả nếu hệ đề xuất **không** thắng baseline, kết quả null đã pre-register + giải thích cơ chế **vẫn là đóng góp**.

---

## 10. RỦI RO CÒN LẠI & cách đã chặn (gọn)
| Rủi ro | Đã chặn bằng |
|---|---|
| Recall detector UI mobile CHƯA công bố rõ (tồn vong) | Cổng K1 (tự đo, cứng) + đóng khung "recall-conditioned" + metric false-negative. *Hiện chỉ có grounding accuracy ~57% (ScreenSpot), KHÔNG phải recall; giả thuyết: recall có thể ~một nửa — K1 sẽ đo thật.* |
| Ablation confound (4 thay đổi 1 lúc) | **Thang bậc C0–C4** + điều kiện công bằng |
| HER vòng tròn (chấm trên E của chính mình) | Chấm **cả 2 nhánh trên lá VH** + control blindspot |
| Confound resolver (SoM được lookup, baseline thì không) | **Resolver đối xứng**; ID-lookup chỉ là dòng oracle riêng |
| Shared-error judge | Ma trận 4 model khác họ + judge text-only nuốt VH + assert |
| Câu hỏi use-case không có sẵn | **Tự soạn** (protocol + đếm), mồi từ ScreenQA |
| "Reference-free" overclaim | Đổi tên chính xác + audit nhiễu nhãn VH 20 màn |
| Pilot người yếu thống kê | Đóng khung sanity + CI-width headline + Kendall + N≥60–80 |
| Kết quả âm = "dự án hỏng" | Pre-register + protocol-first framing → null = pass |
| Chi phí phình | gpt-4o-mini + Batch + dev set + short-circuit |
| **Tier A bị hiểu nhầm là sản phẩm 1-ảnh / ngang leaderboard** | **Khai báo nguyên văn** ở mọi file: Tier A là **dụng cụ đo cận-trên** (teacher-forced, cho thấy màn thật), CHỈ "đặt trong cùng giao thức để tham chiếu định tính, KHÔNG ngang hàng" (setup khác + recall detector chưa rõ, K1 tự đo, kéo số xuống) |
| **Phạt oan cặp tự-do (vd Email/SĐT đảo coi là sai)** | **Chấm partial-order-aware:** headline τ-b CHỈ phạt cặp BẮT BUỘC (gating/drill-down); cặp TỰ-DO đảo vẫn đúng; báo thêm τ-b-thô làm điểm sàn |
| **Leak step-index (model đọc thứ tự từ metadata/tên file thay vì suy luận)** | **Cổng KB:** xáo trộn PHẢI strip metadata + tái mã hoá ảnh + đặt tên UUID; CI test: detector mù không suy ra thứ tự tốt hơn ngẫu nhiên |
| **Goal tiết lộ thứ tự (xếp đúng nhờ goal, KHÔNG nhờ cue giao diện)** | **Baseline GOAL-ONLY** (che hết ảnh): nếu goal-only đã xếp đúng cao → cue giao diện không phải nguồn tín hiệu; báo cả hai số |
| **Episode quá ngắn (thiếu N≥3 để đo τ-b)** | **Cổng KN:** tự đếm histogram độ dài episode AndroidControl (sơ bộ mean ~5.5, p95=13); loại N≤2; thu hẹp/gộp mốc N nếu thiếu, không bịa số |
| **DG2-null thành tautology** | Dồn power pre-register vào 1 trục τ-b ordering: giả thuyết bác được (SELF-ORDER > RANDOM-ORDER quá CI + GOAL-ONLY không cao bằng SELF-ORDER) + ngưỡng CI-width; vi phạm = FAIL có ý nghĩa |
| **ordering gap đọc sai ("gap nhỏ = tốt")** | Sanity cứng ORACLE-ORDER ≥ SELF-ORDER mọi episode; cảnh báo floor-effect: gap chỉ có nghĩa nếu metric tutorial NHẠY thứ tự, nếu không thì τ-b là trục chính, gap chỉ phụ |
| **Overclaim "xếp ảnh xáo là mới"** | KZ′ đã khảo: thừa nhận lineage Sort-Story (EMNLP 2016) / "Sequencing Multimodal Instructional Manuals" (ACL 2022) / RankGPT (EMNLP 2023); độ mới = domain GUI + điều kiện hoá mục tiêu + gắn ordering→sinh tutorial + signal-attribution |

---

## 11. TÓM TẮT MỘT DÒNG
**Làm được, đáng làm, an toàn — chốt lõi 1-màn (DG1: ablation THANG BẬC chấm 2 nhánh trên CÙNG mỏ neo VH, đóng khung quy trình-đánh-giá, null vẫn đậu), CỘNG đánh giá suy luận trật tự màn (DG2: N ảnh xáo trộn → tự xếp → sinh tutorial; headline Kendall τ-b partial-order-aware + ordering gap + signal-attribution theo 5 ordering cues; Tier A teacher-forced làm trục tham chiếu chuẩn ngành) là đóng góp thứ hai; CHỈ tiếng-Việt định lượng + world-model tự-train còn là future-work.**
