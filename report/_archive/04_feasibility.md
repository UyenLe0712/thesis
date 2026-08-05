# BÁO CÁO 4 — ĐÁNH GIÁ TÍNH KHẢ THI (red-team, quyết định chốt-với-thầy)

> ⚠️ **ĐỌC TRONG KHUNG DESIGN E (chốt 2026-06-25; bản hiện hành: `00_DOC_TU_DAU` + `14`):** file này (khả thi + kill-test) còn dùng khung cũ DG1/DG2 + ReOrder-Tutor + Set-of-Mark. **Khung hiện hành:** pipeline LÕI = **lớp trung-thực-hoá** (sinh-theo-tên + oracle-bên-cạnh + fallback), SoM = ablation; **HAI đóng góp NGANG NHAU** (hệ + đánh giá); **TRỌNG TÂM = AndroidControl**. *Phán quyết khả thi + cổng K1/KN/KZ'/KB dưới đây vẫn đúng.*

## TÓM TẮT 30 GIÂY

- **Phán quyết:** 🟢 **GO — NHƯNG THU HẸP PHẠM VI.** Phần lõi (đánh giá `ảnh+câu hỏi → tutorial`, neo trên View Hierarchy) dựng được hoàn toàn từ component có sẵn, không cần fine-tune, chi phí sàn ~$100–300 *(ước tính theo bảng giá tại thời điểm viết, kiểm lại trước khi cam kết)*.
- **Rủi ro số 1 (tồn vong):** recall của detector mobile (OmniParser) trên màn dày **chưa được công bố rõ** — các nguồn ~49–57% thực chất là *grounding accuracy* hoặc ước lượng, **không phải recall element**. Pipeline chỉ cite được ID đã phát hiện → element bị bỏ sót thì không bao giờ cite được, khiến chỉ số grounding/hallucination đẹp giả tạo. **Phải tự đo recall thật ở K1 ngay tuần đầu** (giả thuyết làm việc: có thể ~một nửa bị bỏ sót).
- **10 kill-test (K1, K3–K8 + KN + KZ' + KB)** chạy trong 1 tuần trước khi chốt với thầy. **BỐN cổng cứng — K1 / KN / KZ' / KB:** **K1** (đo recall detector), **KN** (tự đếm histogram độ dài episode AndroidControl — đã khảo sơ bộ GO có điều kiện), **KZ'** (rà prior-art sắp-ảnh — **đã khảo, GO** với khung claim trung thực), **KB** (chống leak step-index — strip metadata + tái mã hoá + UUID, lại CHE status bar/đồng hồ/pin/badge + loại episode 2-ảnh trùng-pixel).
- **DG2 ĐỔI TRỤC — giờ là "suy luận trật tự màn" (Screen-Order Inference):** input = N ảnh ĐÃ XÁO TRỘN của 1 luồng đa bước + mục tiêu → model phải (1) suy ra THỨ TỰ đúng, (2) sinh hướng dẫn từng bước theo thứ tự đó. Headline metric = **Kendall τ-b**. **Tier A teacher-forced** giữ lại làm **trục tham chiếu chuẩn ngành** (thầy expect), KHÔNG còn là "đa bước chính". Chỉ chấm định lượng tiếng Việt + world-model tự-train + nhánh web mới là future-work.

---

> **Câu hỏi:** một học viên cao học có **làm được** kế hoạch ở Báo cáo 1–3 không, hay sẽ sập giữa chừng?
> **Quy trình:** 5 audit khả thi (component · dữ liệu/harness · metric/track chuyên gia · compute/chi phí · phạm vi) → verify độc lập từng blocker bằng web → 1 arbiter tổng hợp.

---

## 0. PHÁN QUYẾT: 🟢 **GO — NHƯNG PHẢI THU HẸP PHẠM VI**

**Chốt với thầy hai đóng góp lõi: DG1 (màn-0) + DG2 (suy luận trật tự màn). KHÔNG chốt phần cần huấn luyện.**

**Thuật ngữ nền (giải thích lần đầu):**
- **VH (View Hierarchy)** = cây phân cấp các phần tử giao diện, dùng làm "đáp án để chấm".
- **DG1** = đóng góp 1: đánh giá trên **màn-0** (ảnh chụp đầu tiên người dùng đưa vào), không có tutorial gold do người viết.
- **DG2** = đóng góp 2: **suy luận trật tự màn** — đưa N ảnh đã xáo trộn của 1 luồng đa bước + mục tiêu, model phải tự xếp đúng thứ tự rồi sinh tutorial; chấm reference-based trên dataset có sẵn chuỗi thao tác đúng (*gold trajectory*).
- **ORACLE-ORDER / SELF-ORDER** = hai chế độ đo của DG2 (giải thích ngay dưới).
- **Tier A** = trục tham chiếu chuẩn ngành (teacher-forced) giữ lại để thầy có điểm so sánh quen thuộc.

**Vì sao GO (không phải "xem lại"):** phần lõi — *đánh giá neo trên VH cho `ảnh+câu hỏi → tutorial`, cộng ablation SoM-Tutor vs E2E* — dựng hoàn toàn từ component thật, cài được, ghép được, **không cần fine-tune** (OmniParser V2, Set-of-Mark, Qwen2.5-VL-7B trên 1 GPU 24GB, vLLM guided decoding / OpenAI Structured Outputs, verifier membership tất định). MobileViews có bbox pixel + cờ tương tác trong JSON parse được; point-in-bbox/HER chỉ tốn "cuối tuần → vài tuần" code. Chi phí sàn dưới ~$300. Lõi này đủ mới, **falsifiable** (kiểm chứng được, có thể bị bác), bảo vệ được.

**LÕI IN-SCOPE — gồm HAI đóng góp:**

- **DG1 — màn-0, KHÔNG có tutorial gold do người viết:** chấm grounding + hallucination + clarity bằng anchor cấu trúc VH (silver = nhãn "bạc", tự suy ra từ cấu trúc giao diện chứ không do người viết tutorial). Dataset: MobileViews (+ ScreenSpot đối chứng grounding).
  - *Quy ước dùng từ:* "reference-free" ở đây hiểu theo **nghĩa hẹp** = KHÔNG có tutorial gold do người viết; VẪN có anchor VH-silver để chấm. Không bao giờ để cụm "reference-free" đứng trần không kèm định nghĩa này.

- **DG2 — suy luận trật tự màn (Screen-Order Inference), reference-based** (dùng AndroidControl, NeurIPS 2024 D&B — peer-reviewed, có sẵn chuỗi thao tác đúng từng bước; thêm **AITW** (NeurIPS 2023) vai nguồn ngưỡng 14% bắt buộc + đối chứng tùy chọn). **Input = N ảnh ĐÃ XÁO TRỘN của 1 luồng + mục tiêu → model tự suy ra THỨ TỰ đúng rồi sinh tutorial từng bước theo thứ tự đó.** Hai chế độ đo:
  - **ORACLE-ORDER (skyline):** đưa N ảnh **đã sắp đúng** + mục tiêu → model chỉ phải sinh hướng dẫn (không phải tự xếp). Là **cận-trên** của trục ordering.
  - **SELF-ORDER (thật):** đưa N ảnh **xáo trộn** → model tự xếp rồi mới sinh. Đây là năng lực thật cần đo.
  - **Headline metric = Kendall τ-b** (chấm **partial-order-aware**: chỉ phạt cặp BẮT BUỘC; cặp TỰ-DO đảo vẫn tính đúng). **Nhãn cặp bắt-buộc suy từ GOLD TRAJECTORY bằng quy tắc nhân-quả tất định** (màn B chỉ xuất hiện sau gold action trên A), KHÔNG lấy từ bộ phát-hiện cue mà model dùng — tránh tự-chấm vòng lặp (D1). **ordering gap = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER) = "cái giá của việc không biết trật tự".**
  - **Tier A (teacher-forced)** giữ làm **trục tham chiếu chuẩn ngành** (thầy expect): mỗi bước đưa model MÀN THẬT của đáp án vàng rồi cho đoán thao tác kế. Metric: **Action-Type accuracy**, **Grounding@14%**, **Step-SR**. KHÔNG còn là "đa bước chính"; KHÔNG claim ngang leaderboard.

**Vì sao THU HẸP (không phải GO thẳng) — phần KHÔNG đo định lượng được, để FUTURE-WORK:**
  1. **Chấm định lượng tiếng Việt** — **KHÔNG có bất kỳ dữ liệu VH-tiếng-Việt nào tồn tại** → point-in-bbox/HER/coverage **không tính được** bằng tiếng Việt. Chỉ sống được như **sanity-check OCR + demo định tính**.
  2. **AGENT-NSI world-model** — cần train (mô hình thế giới tự huấn luyện để dự đoán màn kế) → ngoài tầm master.
  3. **Nhánh web Mind2Web** — mở rộng sang giao diện web (DOM, không có bbox pixel) để sau.

> **QUY ƯỚC SỐNG CÒN:** **Step-SR CHỈ thuộc Tier A** (trục tham chiếu). DG2 chính (suy luận trật tự) headline là **Kendall τ-b**. Đa bước KHÔNG còn là future-work.

---

## 1. RỦI RO TỒN VONG SỐ 1 (verify làm cho NẶNG hơn): trần recall của detector

> Đây là **cửa go/no-go tuần-1**. Pipeline **chỉ cite được ID đã phát hiện** → element bị miss thì vĩnh viễn không cite được.

- **Recall (độ thu hồi) là gì — nói đời thường:** trong 100 nút bấm THẬT trên màn hình, bộ dò (detector) "nhìn thấy" được bao nhiêu cái. Recall 55% nghĩa là nó bỏ sót gần một nửa số nút. Pipeline của ta **chỉ được phép trỏ vào nút đã nhìn thấy** → nút bị bỏ sót thì model không bao giờ nhắc tới được, dù người dùng cần đúng nút đó.
- **Lưu ý nguồn:** các con số **~49–57%** lan truyền quanh OmniParser/ScreenSpot thực chất là *grounding accuracy* hoặc ước lượng gián tiếp, **KHÔNG phải recall element thật**. **Recall trên UI mobile dày chưa có nguồn công bố rõ** → **CON SỐ PHẢI TỰ ĐO Ở K1**, không trích số bên thứ ba như đã biết. Giả thuyết làm việc (chờ K1): có thể bỏ sót ~một nửa nút. Microsoft **không** công bố cải thiện recall mobile cho V2.
- **VÍ DỤ MINH HOẠ (rủi ro recall, ký hiệu EX):** giả sử trên tập màn MobileViews, bộ dò OmniParser đạt recall = 55%. Nếu ta đo chỉ số "bịa-tồn-tại" (model trỏ vào nút không có thật) **trên tập nút mà chính detector đã liệt kê** thay vì trên VH gốc, thì kết quả sẽ **đẹp giả tạo**: 45% nút thật đã bị detector loại từ đầu nên model không có cơ hội "bịa" ra chúng — con số hallucination thấp KHÔNG phải vì pipeline giỏi, mà vì sân chơi đã bị thu nhỏ. Cách chữa: **luôn chấm trên VH gốc** (đầy đủ nút thật) và báo kèm "điều kiện recall = 55%".
- **Hệ quả:** ~½ element mục tiêu không cite được → **HER/CHAIR đẹp giả tạo** (thiên lệch under-reference), và recall grounding thật bị chặn cứng. **Khẳng định "loại bỏ hallucination tất định" là KHÔNG vững như đang viết.** *(HER = Hallucinated Element Rate = tỉ lệ nút model nhắc tới mà không có thật; CHAIR = chỉ số đo bịa-đặt mượn từ image-captioning. Under-reference = "nhắc thiếu" — model nói ít nút hơn thực tế nên hiếm khi bị bắt lỗi bịa.)*
- **Không lật phán quyết** vì đo được rẻ ngay tuần-1 và có thể **đóng khung lại trung thực thành "grounding có điều kiện theo recall"**. *(Recall mobile thấp là xu hướng nhất quán qua nhiều nguồn — nhưng con số chốt phải tự đo, đó cũng chính là kill-test K1.)*

---

## 1bis. VÌ SAO ĐA BƯỚC GIỜ ĐO ĐƯỢC: AndroidControl thay cho Complete-Traces

> Đây là điểm then chốt khiến đa bước chuyển từ "không falsifiable" sang "in-scope". Khác biệt nằm ở **dataset** + **đổi trục bài toán sang suy luận trật tự**.

- **Trước đây bế tắc** vì định dùng **Complete-Traces của MobileViews**: đó là DroidBot tự dò, **1 đường thẳng tuyến tính, KHÔNG có goal (mục tiêu người dùng)** → phần lớn bước suy luận **không có anchor để chấm** → không thể nói "model đoán đúng/sai".
- **AndroidControl (NeurIPS 2024 D&B, peer-reviewed)** giải quyết đúng chỗ này: mỗi **episode** (một phiên thao tác hoàn chỉnh) gắn với một **mục tiêu rõ ràng** và có **gold action mỗi bước** (thao tác đúng từng bước do người chú giải). Có gold từng bước nghĩa là MỖI bước đều **chấm được khách quan**.
- **Số liệu đã verify (Li et al., "On the Effects of Data Scale on UI Control Agents", NeurIPS 2024 D&B, arXiv 2406.03679):** AndroidControl có **15.283 episode**, **833 app**; train **13.604 episode / 74.722 step**; độ dài trung bình **~5,5 step/episode** (Table 1 ghi 4,8; tính lại từ train ra 5,49); **percentile-5 = 1 step, percentile-95 = 13 step**. So sánh độ dài: AndroidControl ~5,5 < AITW ~6,5 < Mind2Web ~7,3 action/task. **LƯU Ý:** nguồn KHÔNG có số đếm theo từng N → **phải tự đếm histogram (việc tuần-1, cổng KN).**
- **DG2 = suy luận trật tự màn (đổi trục):** DG2 lấy episode AndroidControl, **xáo trộn N ảnh** của luồng đó + đưa mục tiêu → model phải tự xếp đúng thứ tự rồi sinh tutorial theo thứ tự đó. **Mọi ảnh đều do người dùng đưa và model ĐỀU THẤY — không có màn nào "chưa thấy"**; grounding chấm ĐẦY ĐỦ mọi màn (model thấy tất cả màn, chỉ không biết thứ tự).
- **Trục N:** loại N≤2 (N=2 chỉ 1 cặp → τ-b chỉ nhận {−1,+1} vô nghĩa). Trục N thực tế **N∈[3, ~10] (chốt trần đường-cong headline N≤6; báo thêm tới ~8–10 nếu ngân sách)** (Stage-0 pairwise = C(N,2) call/episode: mốc CHỐT N=6 → 15 call; minh hoạ N=8 → 28 call, N=10 → 45 call; báo THÊM tới ~8–10 nếu ngân sách cho — D3); báo số episode còn lại mỗi mốc N (cần KN tự đếm histogram).
- **Hai chế độ đo cùng episode đó:**
  * **ORACLE-ORDER (skyline)** — N ảnh **đã sắp đúng** + mục tiêu → model chỉ sinh hướng dẫn, KHÔNG phải tự xếp. Là **cận-trên** của trục ordering.
  * **SELF-ORDER (thật)** — N ảnh **xáo trộn** → model tự xếp rồi mới sinh. Đây là năng lực thật cần đo.
- **ordering gap = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER) = "cái giá của việc không biết trật tự".** **Sanity (D2):** ORACLE-ORDER ≥ SELF-ORDER **− epsilon** ở mỗi episode (KHÔNG phải ≥ tuyệt đối; epsilon hấp thụ nhiễu đo); vi phạm vượt epsilon = bug.
- **CHỐNG FLOOR-EFFECT — pre-register TEST NHẠY-THỨ-TỰ (D2):** lấy input ĐÃ sắp đúng, **đảo 1 cặp BẮT BUỘC**, đo DELTA của metric tutorial. Nếu delta < ngưỡng tối thiểu (pre-register) ⇒ metric tutorial KHÔNG nhạy thứ tự ⇒ **BỎ ordering gap, CHỈ giữ τ-b làm headline** (DG2 KHÔNG sụp). gap chỉ có nghĩa nếu metric tutorial NHẠY với thứ tự; nếu không, **τ-b là trục chính, gap chỉ phụ**.
- **Tier A (teacher-forced) — trục tham chiếu chuẩn ngành:** giữ lại vì thầy expect một điểm so quen thuộc. Tại bước k, bộ chấm đưa **màn hình thật** của đáp án vàng tới bước k, model chỉ đoán **thao tác kế tiếp**, rồi so với gold → cho **Step-SR / Action-Type / Grounding@14%**. *Tier A đặt "trong cùng giao thức để tham chiếu định tính", KHÔNG tuyên bố ngang hàng leaderboard* (vì pipeline detect element từ ảnh bằng OmniParser, khác setup gốc + bị **trần recall thực đo ở K1** kéo số xuống). ORACLE-ORDER là skyline của trục ordering.
- **No-leak (không rò rỉ đáp án):** nguyên tắc "VH/màn thật KHÔNG vào lúc sinh" áp cho **claim về sản phẩm** (DG1 + SELF-ORDER). Khi xáo trộn ảnh, **phải strip metadata + tái mã hoá ảnh + đặt tên UUID** để model không suy ra thứ tự từ tên file / chỉ số bước (đây là cổng **KB**). Tier A và ORACLE-ORDER là thí nghiệm đo cận-trên có chủ đích — chúng là **dụng cụ đo, KHÔNG được trình như năng lực sản phẩm**.

---

## 2. BẢNG RỦI RO XẾP HẠNG

> Cột **Ví dụ** kể một tình huống cụ thể để thấy rủi ro "trông như thế nào" khi xảy ra thật.

| # | Rủi ro | Mức | Ví dụ cụ thể | Cách xử |
|---|---|---|---|---|
| **1** | **Recall detector mobile chưa rõ (tự đo K1)** → chỉ cite được ID đã phát hiện, HER bị thổi phồng, "membership tất định" không vững | **TỒN VONG** | *(ví dụ minh hoạ tự soạn — không phải record thật)* Màn eTax có 40 nút thật, detector chỉ thấy 22 (recall 55%). Câu hỏi nhắm vào nút "Tra cứu nghĩa vụ thuế" — **nếu nút này nằm trong 18 nút bị bỏ sót**, model vĩnh viễn không trỏ tới được, dù tutorial đúng phải bấm vào đó. Chỉ số grounding tụt mà KHÔNG phải lỗi generator. | **Kill-test K1 bắt buộc.** Đóng khung mọi số là "grounding *có điều kiện* recall=X%". Thêm **metric false-negative/coverage** để chỗ miss *hiện ra*, không bị giấu. Nếu recall ≪80% (rất có thể) → claim đổi sang "recall-conditioned grounding". |
| **2** | **Partial-order phạt oan** — phạt cả cặp TỰ-DO (thứ tự không bắt buộc) thì τ-b tụt giả tạo, model bị chấm sai dù tutorial đúng | **TRUNG BÌNH (đã xử lý)** | Luồng có bước "điền Email" và "điền SĐT" — hai ô độc lập, người dùng điền ô nào trước cũng được. Nếu chấm cứng theo thứ tự gold gốc, model điền SĐT trước Email bị tính SAI dù hoàn toàn hợp lệ → τ-b thấp oan. | **Chấm partial-order-aware (QUYẾT ĐỊNH USER, bắt buộc):** chỉ phạt khi sai **cặp BẮT BUỘC** (đảo là sai thật, vd "đăng nhập trước → xem kết quả"); cặp **TỰ-DO** đảo vẫn tính ĐÚNG. **CHỐNG VÒNG-LẶP-LUẬN (D1):** nhãn "cặp BẮT BUỘC" **KHÔNG** lấy từ bộ phát-hiện cue (gating/drill-down) mà chính model + signal-attribution dùng — nếu lấy sẽ thành **TỰ CHẤM** (vòng lặp). Thay vào đó **suy từ GOLD TRAJECTORY của AndroidControl bằng QUY TẮC TẤT ĐỊNH:** màn B chỉ xuất hiện SAU khi thực thi gold action trên màn A ⇒ cặp (A,B) là BẮT BUỘC (phụ thuộc nhân-quả trong chuỗi vàng); cặp không có quan hệ đó = TỰ-DO. **PRE-REGISTER:** (i) tỉ lệ cặp bắt-buộc/tự-do, (ii) AUDIT NGƯỜI 50–80 cặp kiểm quy tắc tất định khớp đánh giá người (báo % khớp), (iii) đo độ-nhạy headline khi gán-sai-nhãn 10%. Gold/VH chỉ dùng khâu **CHẤM OFFLINE**, KHÔNG phải input của model lúc xếp. **HEADLINE τ-b tính trên cặp bắt buộc**; báo THÊM **τ-b-thô** so thứ tự gốc toàn tập làm "điểm sàn" robustness. |
| **3** | **Leak step-index** — model suy ra thứ tự từ tên file / metadata / status-bar thay vì nhìn nội dung → τ-b cao giả tạo | **TRUNG BÌNH** | Ảnh xáo trộn vẫn giữ tên `step_01.png … step_05.png`, EXIF có timestamp, HOẶC đồng hồ/pin/badge trên status bar tăng dần → model "đoán" thứ tự bằng tên/metadata/status-bar, không thật sự suy luận từ giao diện. | **Cổng KB (cứng):** xáo trộn PHẢI strip metadata + tái mã hoá ảnh + đặt tên UUID ngẫu nhiên + **che status bar/đồng hồ/pin/badge** + **loại episode 2-ảnh trùng-pixel**. CI test: cho detector mù (chỉ xem pixel, không xem tên/metadata) — nếu nó **không** xếp tốt hơn ngẫu nhiên thì kênh leak đã bị bịt. |
| **4** | **Goal lộ thứ tự** — bản thân câu mục tiêu đã ngầm tiết lộ trình tự → cue giao diện không còn là nguồn tín hiệu, đo "suy luận trật tự" thành rỗng | **TRUNG BÌNH** | Mục tiêu viết "Đăng nhập rồi vào mục Thuế rồi bấm Tra cứu" — đọc goal là biết thứ tự, model khỏi cần nhìn ảnh. | **Hai baseline ĐỐI XỨNG (D4):** **GOAL-ONLY** (che hết ẢNH, chỉ goal + nhãn trong) ↔ **VISUAL-ONLY** (che MỤC TIÊU, chỉ đưa ảnh) → tách đóng góp ảnh vs goal. Nếu GOAL-ONLY đã đạt τ-b cao thì **cue giao diện KHÔNG phải nguồn tín hiệu** → viết lại goal trung tính. Thêm **RANDOM-ORDER** làm sàn dưới. **Ngưỡng "vượt RANDOM" = phân phối NULL EMPIRICAL theo TỪNG N** (sinh hoán vị ngẫu nhiên đo τ-b), KHÔNG giả định kỳ vọng τ-b random = 0. |
| **5** | **Episode quá ngắn** → N≤2 vô nghĩa, hoặc số episode N≥3 còn lại quá ít để chạy thống kê | **TRUNG BÌNH (đã khảo sơ bộ)** | Khảo sơ bộ AndroidControl: mean ~5,5 step, p95 = 13, **nhưng p5 = 1 step** → một phần episode rơi vào N≤2 phải loại. Chưa biết chính xác bao nhiêu episode còn lại ở mỗi mốc N∈[3, ~10] (đường-cong headline N≤6 — LÕI/Gọn). | **Cổng KN (tự đếm histogram độ dài episode):** đếm chính xác số episode mỗi N. Đã khảo sơ bộ (mean ~5,5 / p95=13) → **GO có điều kiện**, cần tự đếm chính xác để báo "số episode còn lại mỗi mốc N". |
| **6** | **Pairwise vs listwise fair-compute + chi phí Stage-0 bùng theo N** — so sánh hai cách ordering reasoner không công bằng về số lời gọi LLM; pairwise tốn C(N,2) call/episode | **THẤP–TRUNG BÌNH** | Stage-0 pairwise = C(N,2) call: mốc CHỐT **N=6 → 15 call**; minh hoạ **N=8 → 28 call, N=10 → 45 call, p95 N=13 → 78 call MỖI episode** → nếu không trần N, chi phí Stage-0 phình. Và pairwise (C(N,2) call) vs listwise (1 call) nếu so τ-b trực tiếp mà không khớp ngân sách thì kết luận "pairwise tốt hơn" bị nhiễu vì nó tốn nhiều gọi hơn. | **CHỐT TRẦN N≤6** cho đường cong headline (15 call ở N=6; minh hoạ 28 call ở N=8, 45 call ở N=10; báo THÊM tới ~8–10 nếu ngân sách cho); **TÍNH chi phí Stage-0 vào ngân sách**. **Fair-compute = CÙNG TỔNG SỐ LLM-CALL** giữa pairwise và listwise (listwise self-consistency số mẫu = số call pairwise) rồi mới so τ-b. **Phá tie Copeland TẤT ĐỊNH** (vd theo chỉ số ảnh tăng dần), tách khỏi tie cặp-tự-do. Listwise là ĐỐI CHỨNG, pairwise là chính. |
| **7** | **Chi phí judge nhân lên** — SelfCheckGPT N=5 × G-Eval × FActScore × items × ablation → $60 thành $1000+ | **CAO (ngân sách)** | 500 item × 5 cấu hình ablation × 3 bộ judge × (SelfCheckGPT lấy mẫu 5 lần) = ~37.500 lượt gọi LLM. Trên GPT-4o (~$0.03/lượt) là **>$1.000** — vỡ ngân sách. Chuyển sang gpt-4o-mini + Batch kéo về quanh ~$60. *(Mọi đơn giá API là ước tính theo bảng giá tại thời điểm viết, kiểm lại trước khi cam kết.)* | Đẩy judge sang **gpt-4o-mini** (rẻ ~16×) + **Batch API** (−50%); short-circuit refine khi verifier sạch; N=5 chỉ trên subset; dev set 50–100 item, full 500–2000 chỉ cho bảng cuối. |
| **8** | **Tiếng Việt không có dữ liệu VH** → point-in-bbox/HER/coverage không tính được | **BLOCKER (VN như trụ đo được)** | *(ví dụ minh hoạ tự soạn — không phải record thật)* Muốn chấm grounding một tutorial eTax tiếng Việt: cần biết tọa độ bbox pixel của từng nút để kiểm điểm-trong-hộp. Nhưng **không màn eTax nào có file VH đi kèm** → không có "đáp án" để so → point-in-bbox trả về con số rỗng. Chỉ còn chấm tay được. | VN chỉ là (a) sanity-check OCR + (b) demo eTax định tính. **Mọi metric định lượng chạy trên MobileViews EN/ZH + AndroidControl.** OCR mặc định OmniParser **rớt dấu tiếng Việt** → phải swap OCR (Qwen2.5-VL/Vintern). |
| **9** | **72B ngoài tầm** (multi-GPU, 48GB OOM, ~2 tok/s) | TRUNG BÌNH | **Bỏ self-host 72B.** Muốn 1 số 72B thì gọi API hosted ~30 item. **7B là generator chính.** |
| **10** | **Lỗi "guarantee vỡ trên GPT-4o"** trong report 03 | THẤP (dễ sửa, nhưng examiner bắt) | **Sai — đã sửa:** OpenAI **Structured Outputs** ép enum server-side (đảm bảo 100%), guarantee **vẫn còn**, chỉ là vendor lo chứ không phải sinh viên. Dùng ID số ngắn (enum cap 1000 giá trị/15000 ký tự — *theo tài liệu OpenAI tại thời điểm viết*). |
| **11** | **Matcher element↔VH + chuẩn hoá nhãn** (phần lắt léo của HER) + **SoM clutter / latency compile grammar** trên màn dày | TRUNG BÌNH / THẤP | Dùng **ID→bbox lookup** của SoM để khử lỗi resolver ở màn-0; overlay rõ không chồng; XGrammar v2 (~10ms) hoặc regex phẳng over ID. K7: validate matcher vs chấm tay trên 20 màn. | Thêm thời gian cho matcher; demo live thì K=1, tắt SelfCheckGPT. |

> **Chi tiết Rủi ro #2 + #5 (DG2 suy luận trật tự):**
> - **(a)** ordering gap (ORACLE-ORDER − SELF-ORDER) có thể **nhỏ hoặc nhiễu** → nếu metric tutorial không nhạy thứ tự thì gap mất ý nghĩa; khi đó **τ-b là trục chính, gap chỉ phụ**.
> - **(b)** **recall detector** vẫn kéo chất lượng tutorial từng màn xuống (chỉ cite được ID đã phát hiện) — áp cho cả ORACLE-ORDER lẫn SELF-ORDER.
> - **(c)** phải đảm bảo **sanity cứng** ORACLE-ORDER ≥ SELF-ORDER mọi episode; vi phạm = bug harness, không phải kết quả.

---

## 3. PHIÊN BẢN TỐI THIỂU KHẢ THI (chốt cái này làm luận văn)

**XƯƠNG SỐNG (chắc chắn làm được + bảo vệ được):** *Đánh giá neo-VH cho sinh tutorial từ ảnh, gồm DG1 (màn-0, EN/ZH bằng MobileViews) + DG2 (suy luận trật tự màn bằng AndroidControl).* Bốn sản phẩm:
1. **DG1 — Bộ metric 1 màn** — point-in-bbox grounding, HER + coverage, IFEval/G-Eval format — tính tất định từ bbox pixel MobileViews; SoM ID→bbox lookup khử lỗi resolver. **Kèm metric false-negative/coverage** để under-reference hiện ra.
2. **DG1 — Ablation lõi (3 bậc {C1, C3, C4})** — SoM-Tutor (OmniParser V2 → Set-of-Mark → constrained Qwen2.5-VL-7B/GPT-4o → verifier tồn-tại tất định → self-refine có chặn) **vs** baseline E2E-VLM+Self-Refine. Câu hỏi: *từ-vựng-đóng + verifier có giảm hallucination & tăng grounding trên màn thấy không?* **Mọi số kèm điều kiện recall đã đo.** Dương hay âm đều thú vị. **Không cần fine-tune.** *(Ghi chú thang bậc: LÕI/Gọn CHỈ chạy 3 bậc {C1, C3, C4}; **C0** (sàn thô) và **C2** (Set-of-Mark một mình) = MỞ RỘNG/ĐỐI CHỨNG, chạy thêm nếu ngân sách cho phép.)*
3. **DG2 — Suy luận trật tự màn** (tái dùng CÙNG pipeline qua **Stage 0 Screen-Ordering** đặt trước pipeline 5 bước; N=1 → Stage-0 rỗng → về pipeline cũ):
   - **Headline = Kendall τ-b** (chấm partial-order-aware, chỉ phạt cặp bắt buộc) + **τ-b-thô** làm điểm sàn. Phụ: pairwise-order-accuracy + position-accuracy@correct-place. **Bỏ Exact-Order-Match khỏi headline** (N=3 EM~17% ngẫu nhiên, N≥6 ~0).
   - **ORACLE-ORDER vs SELF-ORDER** → **ordering gap** = "cái giá của việc không biết trật tự".
   - **Signal-attribution = stratification cấp một-cue** (chỉ giữ cặp phân biệt bởi ĐÚNG MỘT cue, đo acc theo nhóm cue — KHÔNG che pixel) + phân tích lỗi mở. **5 ordering cues:** gating · nav-affordance · state-delta · title-progression · drill-down. **Caveat cue tự-báo (D5c):** cue do model tự trích chỉ là tín hiệu GIẢI THÍCH YẾU; kết luận "cue nào trả công" dựa trên STRATIFICATION một-cue, KHÔNG dựa lời model tự khai.
   - **Baseline ĐỐI XỨNG (D4):** E2E-VLM + Self-Refine; **GOAL-ONLY** (che hết ảnh) ↔ **VISUAL-ONLY** (che mục tiêu, chỉ ảnh) để tách đóng góp ảnh vs goal; **RANDOM-ORDER** làm sàn (ngưỡng "vượt RANDOM" = phân phối NULL EMPIRICAL theo TỪNG N, không giả định E[τ-b]=0).
   - **Trục tham chiếu chuẩn ngành (Tier A teacher-forced):** Action-Type / Grounding@14% / Step-SR trên AndroidControl — điểm so quen thuộc cho thầy; KHÔNG phải đa-bước-chính, KHÔNG claim ngang leaderboard.
4. **Pilot validate bằng người (nhỏ)** — BWS trên metric grounding/HER + Krippendorff α (IAA) + 1 Spearman/Kendall auto-vs-human kèm bootstrap CI.

**NHÁNH MỞ RỘNG (tách bạch rõ, ghi "future-work" — KHÔNG hứa là kết quả đo được):**
- **(A)** tiếng Việt — động cơ + sanity-check OCR + demo eTax người-chấm; nói thẳng "chấm neo-VH bằng VN là bất khả".
- **(B)** AGENT-NSI world-model (mô hình thế giới tự huấn luyện dự đoán màn kế).
- **(C)** nhánh web Mind2Web (giao diện web, DOM, không có bbox pixel).

---

## 4. CHECKLIST KILL-CRITERIA TUẦN-1 (chạy TRƯỚC khi chốt với thầy)

> Cột **Ví dụ (đo gì / con số đạt là gì)** cho thấy cụ thể một lần chạy kill-test trông ra sao và con số nào tính là PASS.

| # | Thí nghiệm rẻ | Công sức (ước) | Ví dụ (đo gì / con số đạt là gì) | Ngưỡng PASS | Nếu FAIL → |
|---|---|---|---|---|---|
| **K1 (CỬA)** | OmniParser V2 trên **30–50 màn MobileViews**; recall = (số lá VH tương tác khớp 1 box phát hiện)/(tổng lá tương tác), nhất là element mà câu hỏi nhắm tới. | 1 ngày | Chạy detector trên **40 màn MobileViews**, đếm: tổng cộng nó tìm ra **22/40** nút tương tác thật → **recall = 55%**. Vì 55% < 80% → FAIL → từ đó **mọi số grounding ghi kèm "điều kiện recall = 55%"**. (Còn nếu tìm ra ≥32/40 thì recall ≥80% → PASS.) | recall **≥ ~80%** | **Đổi khung cả luận văn sang "grounding có điều kiện recall"** + thêm metric false-negative. (Nhiều khả năng fail — chuẩn bị trước.) |
| **KN (CỔNG CỨNG)** | **Tự đếm histogram độ dài episode AndroidControl** (số episode tại mỗi N), xác nhận đủ episode N∈[3, ~10] (chốt trần đường-cong headline N≤6; báo thêm tới ~8–10 nếu ngân sách) để chạy thống kê DG2. | 0.5 ngày | Đếm histogram: nếu có ≥ vài trăm episode ở mỗi mốc N∈[3,6] → PASS. Khảo sơ bộ đã cho mean ~5,5 / p95=13 / p5=1 → GO có điều kiện. Nếu sau khi loại N≤2 mà mỗi mốc N chỉ còn vài chục episode → FAIL → gộp mốc N hoặc co trục N. **Discrete-N (D5b): pre-register ≥30 episode MỖI mốc N** + hiệu chỉnh đa-kiểm-định **Holm-Bonferroni** (hoặc hạ H2 xuống exploratory). | ≥30 episode mỗi mốc N∈[3, ~10] (đường-cong headline N≤6) để thống kê | Gộp mốc N (vd N∈{3–4,5–6,7+}) hoặc co trục; báo rõ số episode mỗi mốc. |
| **KZ' (PRIOR-ART, ngang K1)** | Rà related-work sắp-ảnh **TRƯỚC** khi gọi "suy luận trật tự màn GUI" là đóng góp: đối chiếu Sort-Story, Sequencing Multimodal Instructional Manuals, RankGPT, sentence-ordering. | 0.5–1 ngày | **ĐÃ KHẢO → GO với khung claim trung thực.** Gần nhất: **Sort-Story** (Agrawal et al., EMNLP 2016 — xếp ảnh+caption xáo, chấm bằng **Spearman** chứ không phải τ), **"Sequencing Multimodal Instructional Manuals"** (Wu et al., ACL 2022 — xếp bước hướng dẫn đa phương thức xáo), **RankGPT** (Sun et al., EMNLP 2023 — PHƯƠNG PHÁP listwise: LLM sinh permutation theo query, không phải metric); sentence-ordering (Gong AAAI 2018); Screen2Vec (CHI 2021). **Tiền lệ dùng Kendall τ chấm ordering = Lapata 2006 (Computational Linguistics 32(4):471–484)** (+ Wu 2022). KHÔNG có công trình trùng khít. | Không có công trình trùng đúng framing | **KHÔNG claim "xếp ảnh xáo là mới".** Độ mới = (a) domain GUI màn-hình + (b) điều kiện hoá theo mục tiêu/use-case + (c) gắn ordering → SINH tutorial + (d) signal-attribution. Thừa nhận lineage Sort-Story/ACL2022/RankGPT. |
| **KB (CỔNG CỨNG, chống leak)** | Xác nhận khi xáo trộn ảnh đã strip metadata + tái mã hoá + đặt tên UUID; **lại CHE status bar / đồng hồ / pin / badge** (kênh leak thị giác) + **loại episode 2-ảnh trùng-pixel**; CI test: detector mù xem pixel không suy ra thứ tự tốt hơn ngẫu nhiên. | 0.5 ngày | Cho 1 detector chỉ đọc tên file + EXIF (không xem nội dung UI) thử xếp thứ tự 20 episode xáo — PASS nếu τ-b của nó ≈ 0 (≈ ngẫu nhiên), tức không còn kênh leak. Nếu τ-b cao bất thường → còn leak (tên file/metadata HOẶC đồng hồ/pin tăng dần lộ thứ tự) → siết lại pipeline xáo. | kênh tên/metadata/status-bar leak ≈ ngẫu nhiên | Siết pipeline xáo (UUID + tái mã hoá + che status bar + loại trùng-pixel) trước khi chạy DG2 chính. |
| **K3** | Qwen2.5-VL + Vintern-1B OCR trên 10 ảnh app VN thật (eTax/bank) cỡ font UI; kiểm dấu | 0.5 ngày | *(ví dụ minh hoạ tự soạn — không phải record thật)* Cho OCR đọc nhãn nút "Nộp thuế điện tử" trên ảnh eTax. PASS nếu ra đúng "Nộp thuế điện tử"; FAIL nếu rớt dấu thành "Nop thue dien tu" → phải swap OCR sang Vintern/Qwen-VL. | đọc đúng dấu | Thu VN về chỉ-động-cơ; chốt swap OCR VN |
| **K4** | vLLM Qwen2.5-VL-7B + OmniParser trên 1 RTX 4090 thuê (~$1); 10 item end-to-end; xem VRAM+latency | 2 giờ | Chạy 10 item, đo đỉnh VRAM = 20.5GB và latency trung bình 4.2s/item → PASS (dưới ngưỡng 22GB / 5s). Nếu OOM ở 24GB hoặc >8s/item → FAIL → bật quant 4-bit. | đỉnh **<22GB**, **<~5s/item** | Quant 4-bit / staging tuần tự; kiểm tầng 16GB |
| **K5** | Full pipeline (gen+critic+ordering+N5+judges) trên **20 item** bật log token; nhân theo item × ablation | 0.5 ngày | Chạy 20 item, log ra ~12k token/item. Nhân lên 500 item × 5 ablation rồi quy ra tiền: dự phóng ~$210 → PASS (≤$300). Nếu dự phóng ~$1.000 → FAIL → đổi judge sang gpt-4o-mini. | dự phóng tổng **≤ ngân sách** | Judge sang gpt-4o-mini + Batch; cap loop |
| **K6** | GPT-4o response_format enum = ID hiện tại + 1 ID giả; xác nhận ID giả không bao giờ ra | 1 giờ | Khai báo enum hợp lệ = {1,2,3} và "gài bẫy" thêm ID giả 99 vào prompt. Chạy 50 lần — PASS nếu output **không bao giờ** chứa 99 (Structured Outputs chặn server-side). Nếu 99 lọt ra dù 1 lần → guarantee vỡ. | ID giả không xuất hiện | (Xác nhận guarantee còn; vẫn sửa wording report) |
| **K7** | Chấm tay point-in-bbox + HER trên 5–20 màn; so với matcher pass đầu | 1 ngày | Trên 20 màn, người chấm tay xác định element↔VH; matcher tự động khớp đúng **17/20** = 85% → PASS (>80%). Nếu chỉ 12/20 = 60% → FAIL → đầu tư thêm cho matcher. | matcher khớp **>80%** tay; metric phân biệt tutorial tốt/hỏng | Thêm thời gian cho matcher |
| **K8** | Pilot BWS 3 annotator trên 10 tutorial; tính Krippendorff α | 1 ngày | 3 người chấm Best-Worst 10 tutorial; tính độ đồng thuận Krippendorff α = 0.58 → PASS (≥0.5, nghĩa là 3 người nhìn chung "đồng ý" với nhau). Nếu α = 0.2 (mỗi người chấm một kiểu) → FAIL → viết lại hướng dẫn chấm. *(0.5 chỉ là ngưỡng sanity-check cho pilot; Krippendorff khuyến nghị ≥0.667 để rút kết luận, ≥0.8 là chuẩn cao.)* | α **≥ ~0.5** | Sửa guideline trước khi scale (rẻ giờ, đắt tháng-5) |
| **TỔNG** | 10 kill-test | **~7–9 ngày-người** | cộng dồn 10 dòng trên | — | *(vừa khít tuần-1, có thể tràn nhẹ sang đầu tuần-2)* |

**BỐN CỔNG CỨNG = K1 / KN / KZ' / KB.**
**K1 là cửa go/no-go cứng. Fail K1 → đổi *khung phát biểu* (không phải bỏ đề tài) trước khi chốt.**
**KN ngang tầm K1: phải tự đếm histogram độ dài episode trước khi cam kết trục N của DG2 (N∈[3, ~10], đường-cong headline N≤6) (pre-register ≥30 episode/N + Holm-Bonferroni).**
**KZ' đã khảo → GO với khung claim trung thực (thừa nhận lineage Sort-Story / ACL 2022 / RankGPT).**
**KB cứng: chống leak step-index (strip metadata + tái mã hoá + UUID + che status bar/đồng hồ/pin/badge + loại episode 2-ảnh trùng-pixel) trước khi chạy DG2 chính.**

---

## 5. ĐOẠN NÓI VỚI THẦY (gợi ý)

> Em xin chốt đề tài gồm **HAI đóng góp** quanh việc sinh hướng dẫn sử dụng từ ảnh chụp màn hình.
>
> **Đóng góp 1 (DG1) — màn-0:** đánh giá việc sinh tutorial cho **màn hình đang thấy**, dùng MobileViews (Anh/Trung, bbox pixel chính xác) làm mỏ neo chấm điểm. *(Em nói rõ: "reference-free" ở đây nghĩa hẹp là KHÔNG có tutorial gold do người viết, nhưng VẪN có anchor View Hierarchy-silver để chấm.)* Lõi falsifiable là một **ablation có kiểm soát**: pipeline từ-vựng-đóng Set-of-Mark + verifier tồn-tại tất định có **giảm hallucination & tăng grounding** so với baseline VLM end-to-end + self-refine không — **mọi số đều kèm điều kiện recall thực đo của detector**, và được **đối chiếu với một panel chuyên gia nhỏ chấm Best-Worst-Scaling**.
>
> **Đóng góp 2 (DG2) — suy luận trật tự màn:** thầy hỏi "làm sao model biết trật tự các màn?" — em trả lời thẳng câu đó bằng một bài toán đặt ra ĐỂ ĐO: em lấy episode đa bước từ **AndroidControl (NeurIPS 2024 D&B)** vốn có **gold trajectory**, **xáo trộn N ảnh** của luồng đó rồi đưa kèm mục tiêu; model phải **tự suy ra thứ tự đúng** rồi sinh tutorial từng bước theo thứ tự đó.
>   - **Headline = Kendall τ-b**, chấm **partial-order-aware** — chỉ phạt khi đảo **cặp bắt buộc** (vd "đăng nhập trước → xem kết quả"); cặp **tự do** (vd điền Email/SĐT độc lập, đảo vẫn đúng) thì không phạt oan.
>   - Em đo hai chế độ: **ORACLE-ORDER** (đưa N ảnh đã sắp đúng, model chỉ sinh — là cận-trên) và **SELF-ORDER** (xáo trộn, model tự xếp). **Hiệu số ORACLE-ORDER − SELF-ORDER (ordering gap)** chính là **"cái giá của việc không biết trật tự"**.
>   - Em còn **gọi tên 5 tín hiệu (ordering cues)** mà model dựa vào để biết trật tự — gating, nav-affordance, state-delta, title-progression, drill-down — và đo accuracy theo từng cue để biết cue nào giúp xếp đúng.
>   - Em **giữ Tier A teacher-forced (Step-SR / Action-Type / Grounding@14%)** làm **trục tham chiếu chuẩn ngành** để thầy có điểm so quen thuộc — nhưng nói rõ nó **KHÔNG phải sản phẩm 1-ảnh** và em **KHÔNG tuyên bố ngang hàng leaderboard** (setup detect-từ-ảnh + trần recall khác bản gốc).
>
> Toàn bộ component off-the-shelf, không fine-tune, tái dùng **cùng một pipeline** (Stage 0 Screen-Ordering đặt trước pipeline 5 bước; N=1 → Stage-0 rỗng → về pipeline cũ) cho cả hai đóng góp, chạy trên 1 GPU 24GB + ~$100–300 API *(ước tính theo bảng giá tại thời điểm viết)*. Em chỉ để **chấm định lượng tiếng Việt, world-model agentic tự huấn luyện, và nhánh web Mind2Web** làm **future-work**. *(Lý do đa bước dùng AndroidControl chứ không dùng traces của MobileViews: traces MobileViews là DroidBot dò tuyến tính, **không có goal nên không gold** — nên đa bước em chuyển sang AndroidControl, nơi CÓ gold từng bước.)* Trước khi chốt, em chạy ~1 tuần kill-test rẻ — quan trọng nhất là **đo recall thật của OmniParser (K1)**, **tự đếm histogram độ dài episode AndroidControl (KN)** và **rà prior-art sắp-ảnh (KZ' — đã khảo, có lineage Sort-Story/ACL 2022/RankGPT)** — và báo lại; nếu recall thấp, em đóng khung đóng góp thành "grounding có điều kiện recall".
>
> *(Chuẩn bị cho đòn "đóng góp định lượng mới cũng không có tiếng Việt":)* Em xin thừa nhận thẳng — bảng số định lượng (cả DG1 lẫn DG2) chạy trên dữ liệu Anh/Trung vì **không tồn tại** dữ liệu View Hierarchy / gold trajectory tiếng Việt. Bù lại, em giữ **demo định tính trên eTax** *(ví dụ minh hoạ tự soạn — không phải record thật)*: xáo trộn vài màn eTax thật rồi cho model xếp lại + sinh tutorial, làm **bằng chứng concept tiếng Việt** dù không có gold để chấm điểm.

---

## 6. LƯU Ý ĐẶC BIỆT VỀ TIẾNG VIỆT (thầy ưu tiên VN ↔ thực tế dữ liệu)

Có **căng thẳng cần xử khéo:** thầy ưu tiên tiếng Việt, nhưng **không tồn tại dữ liệu VH tiếng Việt** → không thể chấm định lượng (point-in-bbox/HER) bằng tiếng Việt. **Lối đi trung thực:**
- **Định lượng** (số liệu, bảng, validate metric): chạy trên **MobileViews EN/ZH + AndroidControl** — đây là nơi có ground-truth.
- **Tiếng Việt** = (a) **động cơ** thực tế (eTax "đã nộp thuế chưa" — *ví dụ minh hoạ tự soạn, không phải record thật*), (b) **sanity-check OCR** tiếng Việt (đo được, nhỏ), (c) **demo định tính** cho người đọc trên vài màn app VN tự thu.
- Nói rõ với thầy điều này **sớm** để tránh kỳ vọng "có bảng số tiếng Việt". Output tutorial **vẫn có thể bằng tiếng Việt** (Qwen2.5-VL sinh VN tốt) — chỉ là *chấm điểm tự động* phải neo trên dữ liệu EN/ZH.

> **Lưu ý ví dụ:** mọi ví dụ eTax xuyên suốt báo cáo này (Rủi ro #1/#8, K3, đoạn nói với thầy) là **ví dụ minh hoạ tự soạn — không phải record thật**. Record THẬT xem `02_datasets.md` mục HỘP-THẬT.

---

## 7. SỬA ĐÃ ÁP / CẦN ÁP vào các report khác
- **Report 03 §1, §4-item2:** sửa lỗi "guarantee vỡ trên GPT-4o" → OpenAI Structured Outputs vẫn ép enum (guarantee còn, vendor lo). *(đã sửa)*
- **Report 03:** thêm con trỏ tới phán quyết "GO-có-thu-hẹp" + đóng khung "recall-conditioned grounding". *(đã thêm)*
- **Report 01 §4 / Report 03:** đa bước & VN đã có cảnh báo; report này **đổi DG2 thành "suy luận trật tự màn" (Screen-Order Inference)** — headline **Kendall τ-b** chấm partial-order-aware, hai chế độ **ORACLE-ORDER / SELF-ORDER** với **ordering gap**, giữ **Tier A teacher-forced** làm trục tham chiếu chuẩn ngành; chỉ giữ **VN định lượng + world-model + web Mind2Web** ở future-work.

> **Giải thích thuật ngữ mới (lần đầu xuất hiện):**
> - **DG1 / DG2** = đóng góp 1 (màn-0, không tutorial gold người viết) / đóng góp 2 (suy luận trật tự màn, có gold trajectory).
> - **gold trajectory** = chuỗi thao tác ĐÚNG từng bước có sẵn trong dataset (AndroidControl), dùng làm đáp án để chấm.
> - **Screen-Order Inference** = bài toán đưa N ảnh ĐÃ XÁO TRỘN của 1 luồng + mục tiêu → model tự xếp đúng thứ tự rồi sinh tutorial theo thứ tự đó.
> - **ORACLE-ORDER** = đưa N ảnh đã sắp đúng (model chỉ sinh, không phải tự xếp) — cận-trên/skyline của trục ordering.
> - **SELF-ORDER** = đưa N ảnh xáo trộn (model tự xếp rồi sinh) — năng lực thật cần đo.
> - **ordering gap** = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER) = "cái giá của việc không biết trật tự".
> - **Kendall τ-b** = headline metric đo độ tương quan thứ hạng giữa thứ tự model xếp và thứ tự đúng; chấm **partial-order-aware** (chỉ phạt cặp bắt buộc), báo thêm **τ-b-thô** làm điểm sàn.
> - **5 ordering cues** = gating · nav-affordance · state-delta · title-progression · drill-down — các tín hiệu model dựa vào để biết trật tự.
> - **Tier A (teacher-forced)** = mỗi bước cho model thấy MÀN THẬT của đáp án vàng rồi mới cho đoán bước kế — **trục tham chiếu chuẩn ngành** (Step-SR / Action-Type / Grounding@14%); KHÔNG phải sản phẩm, KHÔNG claim ngang leaderboard.
> - **Grounding@14%** = điểm click coi là trúng khi nằm **trong ~14% khoảng cách màn HOẶC cùng bounding box** so với đích (ngưỡng AITW).

**Bất biến giữ nguyên:** **BỐN cổng cứng K1 / KN / KZ' / KB**; reference-free DG1 màn-0 nguyên vẹn; metric headline có nguồn bình duyệt; pre-registration (null vẫn đậu) — nhưng **dồn power vào 1 trục = Kendall τ-b ordering**; §6 tiếng Việt vẫn là future-work định lượng; mọi số vẫn báo **recall-conditioned + RAW vs ORACLE**; no-leak mở rộng thành cổng **KB** (strip metadata + tái mã hoá + UUID + che status bar/đồng hồ/pin/badge + loại episode 2-ảnh trùng-pixel khi xáo trộn ảnh). **Nhãn cặp-bắt-buộc suy từ GOLD TRAJECTORY tất định (KHÔNG từ bộ cue của model — chống tự-chấm vòng lặp, D1); gold/VH chỉ dùng khâu CHẤM OFFLINE.**
