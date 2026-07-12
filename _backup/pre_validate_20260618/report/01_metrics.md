# BÁO CÁO 1 — METRIC ĐÁNH GIÁ

## TÓM TẮT 30 GIÂY
- File này chọn **thước đo (metric)** cụ thể cho **4 tiêu chí** đánh giá tutorial: UI Grounding, Hallucination, Clarity/Format, Task Success — mỗi metric đều có **paper nguồn đã kiểm chứng** (phần lớn bình duyệt: ACL/EMNLP/NAACL/CL journal).
- Bối cảnh bài toán: input = **1 ảnh + 1 câu hỏi** → output = **tutorial từng bước** cho người đọc.
- Bộ đánh giá tách thành **hai đóng góp**: **DG1** (chấm màn-0, không có tutorial mẫu của người) cho tiêu chí 1–3; **DG2** (đa bước, có đáp án vàng từng bước) cho tiêu chí 4.
- DG2 = **Suy luận trật tự màn (Screen-Order Inference)**: input = **N ảnh XÁO TRỘN** của 1 luồng đa bước + mục tiêu → model (1) suy ra **thứ tự đúng** rồi (2) sinh hướng dẫn từng bước theo thứ tự đó. Headline = **Kendall τ-b** trên thứ tự suy ra (đóng góp **mới**: suy luận trật tự màn GUI có điều kiện hoá theo use-case). **Tier A teacher-forced** (Action-Type / Grounding@14% / Step-SR trên AndroidControl) GIỮ làm **trục tham chiếu chuẩn ngành**, không còn là "đa bước chính".
- Một metric chỉ "đáng tin để làm anchor" sau khi qua **Track B** (so với điểm chuyên gia). Mọi số grounding đều kèm điều kiện **recall detector (cổng K1)** — recall phát hiện element trên UI mobile dày CHƯA được công bố rõ (nguồn chỉ có *grounding accuracy* ~57% trên ScreenSpot), nên **K1 = TỰ ĐO recall** là cổng cứng.

> **⚠️ LƯU Ý VỀ VÍ DỤ:** Mọi ví dụ tính bằng số trong file này (eTax / "Tra cứu nghĩa vụ thuế" / toạ độ (405,915) / bbox [270,820,540,1010] / HER=1/3 / FActScore=1/2 / app Đồng hồ…) đều là **ví dụ minh hoạ TỰ SOẠN để giải thích công thức — KHÔNG phải record thật của MobileViews/AndroidControl/ScreenSpot.** Record THẬT (đã verify) xem `02_datasets.md` mục **HỘP-THẬT** (AndroidControl episode `cruisedeals`; ScreenSpot mẫu 'close' bbox 0–1 `[0.948,0.144,0.994,0.207]`; MobileViews root `[0,0,1080,1920]`).

---

> **Mục đích:** đề xuất các thước đo (metric) cụ thể, có paper nguồn, cho 4 tiêu chí đánh giá + track validate.
> **Bối cảnh:** input = 1 ảnh + 1 câu hỏi → output = tutorial từng bước.
>
> **Khung gốc:** Chim, Ive, Liakata. *Evaluating Synthetic Data Generation from User Generated Text.*
> **Computational Linguistics 51(1):191–233, MIT Press, 2025** (bài báo *tạp chí*, KHÔNG phải ACL 2025). <https://aclanthology.org/2025.cl-1.6/>

---

## CẦU NỐI — HAI ĐÓNG GÓP ĐÁNH GIÁ (DG1 vs DG2)

**Đọc trước khi vào từng tiêu chí.** Luận văn tách bộ đánh giá thành **hai đóng góp (DG)**. Trục chính = **"có gold trajectory (đáp án vàng từng bước) để so hay không"**. Cố ý **KHÔNG** dùng trục "reference-free vs reference-based" vì DG2 (đa bước, suy luận trật tự màn) khi chấm vẫn so gold → vẫn là reference-based; lấy trục đó làm trục gốc sẽ gây mâu thuẫn.

**DG1 — màn-0, KHÔNG có tutorial gold của người.** Ánh xạ **Tiêu chí 1–3** (UI Grounding, Hallucination, Clarity/Format).
- Chấm bằng anchor cấu trúc **View Hierarchy** (VH = cây phần tử giao diện kèm bbox, đóng vai "đáp án để chấm"), gọi là **VH-silver** (silver = nhãn gần-đúng tự sinh từ dataset, không phải nhãn vàng do người viết).
- Cụm **"reference-free"** ở DG1 hiểu theo *nghĩa hẹp* = không có tutorial gold do người viết; vẫn có anchor VH-silver. Không để "reference-free" đứng trần một mình.
- VH **chỉ vào lúc chấm**, KHÔNG đưa vào model lúc sinh.

**DG2 — Suy luận trật tự màn (Screen-Order Inference), CÓ gold trajectory** (AndroidControl, NeurIPS 2024). Ánh xạ **Tiêu chí 4** (Task Success). Bài toán: đưa model **N ảnh XÁO TRỘN** của một luồng đa bước + mục tiêu → model phải **suy ra thứ tự đúng** rồi **sinh hướng dẫn từng bước** theo thứ tự đó. Đây là **bài toán đặt ra để ĐO năng lực suy luận trật tự** (trả lời câu hỏi "làm sao model biết trật tự màn"), KHÔNG khẳng định là nhu cầu deploy phổ biến.
- **Headline = Kendall τ-b** trên thứ tự model suy ra so với thứ tự gold (xem §4.4).
- **Tier A (teacher-forced) GIỮ làm trục tham chiếu chuẩn ngành** (skyline): mỗi bước bộ chấm đưa màn hình thật của đáp án vàng, model đoán thao tác kế tiếp rồi so gold. (*teacher-forcing = cho model "xem trước đáp án màn trước" để đo từng bước độc lập, theo chuẩn ngành.*)
- **Hợp đồng sản phẩm có INPUT ROUTER:** N=1 → đơn bước (DG1 màn-0 nguyên vẹn); N≥2 → bật chế độ sắp-thứ-tự (DG2). Một hệ duy nhất.

Đa bước GIỜ TRONG SCOPE chính (không còn là future-work). Ký hiệu cũ TH1/TH2 đã bỏ — dùng DG1/DG2 xuyên suốt.

---

## 0. Ánh xạ khung Chim et al. → 4 tiêu chí luận văn

Khung gốc có **3 trục Intrinsic** (Meaning / Style / Divergence) + **Extrinsic**. Ánh xạ sang bài toán image→tutorial:

| Trục gốc (Chim et al.) | Trục gốc đo gì | → Tiêu chí luận văn | Vì sao |
|---|---|---|---|
| **Meaning preservation** | giữ đúng nội dung/ý nghĩa | **UI Grounding + Hallucination** | tutorial phải "đúng nghĩa" với màn hình thật = thao tác đúng element tồn tại |
| **Style preservation** | giữ văn phong | **Clarity / Format** | không có "văn phong cá nhân" → đo định dạng/độ rõ (đánh số, động từ hành động) |
| **Divergence** (1−BLEU theo mẫu; **JSD** char-trigram theo phân phối) | khoảng cách tới *corpus tham chiếu* (proxy privacy) | **(tái diễn giải)** Diversity/anti-template | Reference-free **không có corpus tham chiếu** để "diverge" → **không bê nguyên**. Tái diễn giải thành: tránh lặp khuôn mẫu (mode collapse) giữa các tutorial. Xem §3.5. |
| **Extrinsic** (task success) | hiệu quả tác vụ downstream | **Task Success** | tutorial dẫn tới đúng màn hình đích / khớp trajectory |

> **Lưu ý trung thực:** trục **Divergence** của bản gốc đo khoảng cách phân phối tới corpus tham chiếu — **không chuyển thẳng** sang setting reference-free 1 ảnh. Luận văn **tái diễn giải** nó thành metric đa dạng/chống lặp khuôn (§3.5) hoặc **nêu rõ là out-of-scope** và giải thích lý do.

---

## CAVEAT TOÀN CỤC — "màn hình thấy được" vs "màn hình suy luận"

Input chỉ có **1 ảnh + VH của màn hình đó (màn 0)**. Tutorial đa bước mô tả cả các màn model **tưởng tượng** (màn ≥1). Hệ quả: hầu hết metric grounding/hallucination **chỉ neo được trên màn 0**. Với bước ≥1 không có VH để đối chiếu, trừ khi dùng next-screen VH từ MobileViews Complete Traces (và kể cả khi có, model *không* được xem màn đó lúc sinh).

**Chính sách chấm bắt buộc** — chia mỗi bước thành 2 loại:
- (a) **grounded-on-visible-screen** (bám màn thấy được): chấm đầy đủ.
- (b) **inferred-screen** (màn suy luận): chỉ chấm khi có next-screen VH từ trace; nếu không thì **báo riêng là "unverifiable"** (chưa kiểm chứng được), KHÔNG gọi là "hallucination".

Gộp hai loại sẽ phạt oan suy luận đa bước hợp lý. Báo cáo tách biệt: *metric trên màn thấy được* vs *metric trên màn suy luận*.

**Phân tách theo dataset** (tránh hiểu nhầm caveat này áp cho mọi dataset):
- Trạng thái "unverifiable" CHỈ đúng với **MobileViews (DG1, màn-0)** — nơi thực sự không có màn thật để đối chiếu bước ≥1.
- Ngược lại, **DG2 / AndroidControl đo được bình thường**: trong chế độ Screen-Order Inference model được đưa **N ảnh thật** (chỉ bị XÁO TRỘN thứ tự), nên mỗi màn đều có VH thật để chấm grounding đầy đủ; Tier A teacher-forced cũng có gold action + màn thật từng bước. Cả hai đều không rơi vào "unverifiable".

---

## Tổng quan: bộ metric đề xuất

> **Quy ước hướng điểm (orientation):** mọi metric hallucination/grounding quy về **"faithfulness", cao = tốt = 1 − tỷ lệ lỗi**, để nhất quán khi tương quan Spearman với điểm người.

| Tiêu chí | Metric *chính* | Metric *phụ / triangulate* |
|---|---|---|
| **UI Grounding** | Point-in-BBox Acc (SeeClick/ScreenSpot) **+ bước text→element** | Center-in-BBox; IoU (khi xuất box); Element-match Acc (khi không có tọa độ) |
| **Hallucination** | **1 metric tồn-tại chính** (HER *hoặc* grounding-existence) + FActScore (quan hệ/thứ tự) | ALOHa, FaithScore, coverage(VALOR-EVAL); POPE/SummaC/SelfCheckGPT (chỉ triangulate) |
| **Clarity/Format** | IFEval format compliance (cứng) + G-Eval (mềm, phải tự-validate) | MT-Bench pairwise; Flesch (chỉ thống kê mô tả) |
| **Task Success** (DG2) | **DG2 ordering (mới):** **Kendall τ-b** (headline, trên cặp BẮT BUỘC) + pairwise-order-accuracy + position-accuracy@correct-place (§4.4); **Tier A tham chiếu:** Action-Type acc + Grounding@14% + Step-SR (AndroidControl/OS-Atlas; ngưỡng 14% từ AITW) | AITW action matching (chạy được trên traces); Mind2Web Step SR/Element Acc/Op F1 (*tùy chọn*, định nghĩa nền) **(future-work web)** |
| **Validate metric** | BWS → **Spearman + Kendall τ-b** (auto vs human) + bootstrap CI | Krippendorff α / Fleiss κ |

---

## TIÊU CHÍ 1 — UI GROUNDING
*"Tọa độ/element tutorial định thao tác có nằm trong bbox của element thật trên VH không?"*

**Bước bắt buộc — text→element resolution (giải nghĩa: đổi câu chữ thành tọa độ).** Output là tutorial bằng ngôn ngữ tự nhiên ("bấm icon bánh răng"), thường không chứa sẵn tọa độ (x,y). Phải có bước **map bước NL → element/tọa độ ứng viên** (qua grounding model, hoặc khớp tên với label VH) TRƯỚC khi tính point-in-bbox. Bước resolver này tự nó là nguồn lỗi nên **phải validate riêng**. Nếu khớp theo tên thì metric thực chất là **Element-match / text-grounding accuracy** (xem Mind2Web Element Acc §4.5, ScreenSpot text grounding).

### 1.1. Point-in-BBox Accuracy (ScreenSpot Click/Grounding Acc) — ⭐ chính
- **Công thức:** `correct = 1 if (x_min ≤ x ≤ x_max and y_min ≤ y ≤ y_max) else 0`; `Acc = #đúng / #mẫu`.
- **Ví dụ tính bằng số (EX-A, màn-0 eTax — *ví dụ minh hoạ tự soạn, KHÔNG phải record thật của MobileViews*):** người dùng hỏi *"kiểm tra đã nộp thuế chưa thì vào đâu?"*; tutorial chỉ đến nút ③ **"Tra cứu nghĩa vụ thuế"**, model định click tại tâm `(405, 915)`; nút thật trên VH có bbox `[270, 820, 540, 1010]` (left, top, right, bottom). Kiểm tra: `270 ≤ 405 ≤ 540` ✓ và `820 ≤ 915 ≤ 1010` ✓ → điểm **nằm trong** → bước này tính **đúng** (correct = 1.0 — TRÚNG).
- **Citation (✅):** Cheng, Sun, Chu, Xu, Li, Zhang, Wu. *SeeClick.* **ACL 2024** (Long). arXiv:2401.10935. ([2024.acl-long.505](https://aclanthology.org/2024.acl-long.505/))
- **Ưu:** chuẩn de-facto, chỉ cần bbox VH. **Nhược:** nhị phân; phụ thuộc bước resolver ở trên; nhạy bbox lồng nhau.

### 1.2. Center-Point-in-BBox Accuracy — phụ (UI dày đặc/độ phân giải cao)
- **Đo:** lấy **tâm box dự đoán**, kiểm tra rơi vào bbox GT (GT = ground truth = đáp án thật). *Lưu ý:* quy tắc center-point-in-box **vốn từ ScreenSpot gốc (SeeClick)**; ScreenSpot-Pro chỉ **áp dụng cho UI chuyên nghiệp khó**, không phải người phát minh tiêu chí.
- **Ví dụ:** model xuất ra cả một box `[260,810,550,1020]` (thay vì 1 điểm) cho nút "Tra cứu nghĩa vụ thuế"; lấy tâm box = `(405, 915)`, kiểm tra rơi vào bbox GT `[270,820,540,1010]` → trúng → đúng. Hữu ích khi UI dày đặc, model hay trả về vùng thay vì điểm.
- **Citation (✅):** Li, Meng, Lin, Luo, Tian, Ma, Huang, Chua. *ScreenSpot-Pro.* arXiv:2504.07981, 2025 **(preprint — KHÔNG phải ICLR 2025)**.

### 1.3. IoU — phụ, partial-credit (chỉ khi model xuất box)
- **Công thức:** `IoU = area(pred ∩ gt) / area(pred ∪ gt)` (IoU = Intersection over Union = diện tích phần chồng nhau chia diện tích phần hợp; ngưỡng phổ biến ≥0.5 = "khít hơn nửa thì tính đúng").
- **Ví dụ:** box dự đoán `[260,810,550,1020]` và box thật `[270,820,540,1010]` chồng nhau gần hết → IoU ≈ 0.9 (rất khít) → đúng. Nhưng nếu model dự đoán cả một panel to bao quanh nút nhỏ, phần giao chỉ là nút bé → IoU thấp dù click đúng chỗ → đó là lý do IoU phạt oan (xem nhược điểm dưới).
- **⚠️ Citation:** **KHÔNG** trích UGround/SeeClick (họ *cố tình dùng point-in-bbox, không dùng IoU*). IoU là metric localization tổng quát → **Everingham et al., *PASCAL VOC Challenge*, IJCV 88(2):303–338, 2010** (gốc xa: Jaccard 1912).
- **Nhược:** điểm đúng giữa element to vẫn IoU thấp → phạt oan click đúng-nhưng-không-khít; suy biến nếu model chỉ xuất điểm.

---

## TIÊU CHÍ 2 — HALLUCINATION
*"Tutorial có nhắc element/thao tác KHÔNG có trong VH không?"* — nhánh nhiều cách đo nhất.

**Chống đếm trùng (quan trọng).** Nhiều metric dưới đây cùng trả lời 1 câu "nút này có trong VH không?" → chỉ chọn 1 làm chính, tránh phạt 1 lỗi nhiều lần. Cụ thể: HER (2.1), grounding-existence (2.3), slice tồn-tại của FActScore (2.4) và POPE (2.10) đều đo **cùng một thứ** ("element này có trong VH không"). Vì vậy: **CHỌN 1 làm chính**, các cái khác chỉ triangulate (đối chiếu chéo), KHÔNG cộng dồn vào một điểm tổng hợp. Báo **tương quan giữa chúng**, không lấy trung bình. FActScore/SAFE giữ vai trò bù trục quan hệ/thứ tự (cái mà metric tồn-tại không bắt được).

### Họ A — Đếm element bịa (trực tiếp)

**2.1. CHAIR → Hallucinated-Element-Rate (HER)** — ⭐ ứng viên metric tồn-tại chính
- `HER = #element nhắc tới vắng mặt trong VH / #element nhắc tới` (báo dạng faithfulness = 1−HER); `HER(step)` tương tự theo bước.
- **Ví dụ tính bằng số (EX-A, màn-0 eTax — *ví dụ minh hoạ tự soạn, KHÔNG phải record thật của MobileViews*):** tutorial nhắc tới **3 nút**; đối chiếu VH thấy 2 nút có thật, riêng nút **"Cài đặt"** KHÔNG tồn tại trong VH (model tự bịa) → `HER = 1/3 ≈ 0.33` (faithfulness = 1 − 0.33 ≈ 0.67). Đọc: "1 trong 3 element được nhắc là bịa".
- **Citation (✅):** Rohrbach, Hendricks, Burns, Darrell, Saenko. *Object Hallucination in Image Captioning.* **EMNLP 2018**. ([D18-1437](https://aclanthology.org/D18-1437/))
- **Nhược:** match chuỗi ngây thơ → dương tính giả (do đồng nghĩa) → dùng kèm 2.2.
- **Bù coverage (recall):** HER chỉ phạt element bịa (precision = "những gì đã nhắc có thật không"); một tutorial **bỏ sót hết element thật mà không bịa gì vẫn được điểm tuyệt đối**. Vì vậy thêm **coverage/recall** (mention-recall = "có nhắc đủ element thật không", so với node lá VH) — tham chiếu **VALOR-EVAL** (Qiu et al., **Findings of ACL 2024**; arXiv:2404.13874) tổng quát hoá CHAIR thêm coverage.
  - **Ví dụ tính bằng số (EX-A, màn-0 eTax):** màn hình có **5 nút tương tác liên quan** trong VH; tutorial chỉ nhắc tới **2** nút trong số đó → `coverage = 2/5 = 0.4`. Diễn giải: tutorial không bịa (HER có thể đẹp) nhưng **bỏ sót 3/5 nút** → coverage lộ ra điểm yếu mà HER không thấy. Cặp đôi HER (precision) + coverage (recall) cho bức tranh đầy đủ.

**2.2. ALOHa (open-vocab, LLM + Hungarian matching)** — khắc phục nhược 2.1
- Trích object bằng LLM → similarity embedding (vector ngữ nghĩa) → ghép Hungarian (thuật toán ghép cặp tối ưu); không cặp đủ giống = bịa.
- **Ví dụ:** tutorial nói "bấm nút **Thiết lập**", VH chỉ có nút "**Cài đặt**" — HER ngây thơ (2.1) báo bịa vì khác chuỗi, nhưng ALOHa thấy embedding hai từ rất giống → ghép được → KHÔNG tính bịa (tránh dương tính giả do đồng nghĩa).
- **Citation (✅):** Petryk, Chan, Kachinthaya, Zou, Canny, Gonzalez, Darrell. *ALOHa.* **NAACL 2024** (Short). ([2024.naacl-short.30](https://aclanthology.org/2024.naacl-short.30/))

**2.3. GUI-Grounding existence check** — ứng viên metric tồn-tại chính (hình học)
- Bước → tọa độ; **grounded** (bám được) nếu rơi vào 1 bbox VH. `Faithfulness = Grounded-Step-Rate` (tỷ lệ bước có tọa độ rơi trúng một element thật).
- **Ví dụ:** tutorial 4 bước; sau khi resolve thành tọa độ, 3 bước rơi trúng bbox của element trong VH, 1 bước rơi vào vùng trống (không element nào) → `Grounded-Step-Rate = 3/4 = 0.75`.
- **Mạnh:** kiểm tra hình học bằng bbox MobileViews. **Caveat:** "không cần LLM-judge" chỉ đúng ở phép kiểm containment cuối — bước resolve text→tọa độ vẫn cần grounding model (có thể tự bịa tọa độ); chỉ áp dụng cho màn 0.

**2.3b. FaithScore (faithfulness VLM fine-grained, reference-free)** — *bổ sung*
- Trích atomic descriptive facts (mệnh đề mô tả nhỏ nhất, VD "có một nút màu xanh ở góc trên") rồi verify với **ảnh** (VLM-native, không cần gold). Hợp "tutorial trung thành với screenshot".
- **Ví dụ:** tutorial mô tả "ở đầu màn hình có thanh tìm kiếm" → tách thành fact "tồn tại thanh tìm kiếm ở phía trên" → VLM nhìn ảnh xác nhận có/không; nếu ảnh không có thanh tìm kiếm → fact này bị đánh dấu unsupported.
- **Citation (✅):** Jing et al. *FaithScore: Evaluating Hallucinations in Large Vision-Language Models.* **Findings of EMNLP 2024** (peer-reviewed; arXiv:2311.01477).

### Họ B — Atomic-fact + xác minh (bù trục quan hệ/thứ tự)

**2.4. FActScore** — ⭐ cho claim quan hệ/thứ tự
- Tách output thành atomic claim (mệnh đề nhỏ nhất, kiểm chứng độc lập được) → check với VH. `FActScore = #supported / #total`.
- **Ví dụ (*ví dụ minh hoạ tự soạn, KHÔNG phải record thật của MobileViews*):** tutorial "Bấm ③ Tra cứu nghĩa vụ thuế nằm dưới nút Thanh toán" → tách 2 claim: (1) "tồn tại nút Tra cứu nghĩa vụ thuế" — VH có ✓ supported; (2) "nút này nằm DƯỚI nút Thanh toán" (quan hệ vị trí) — đối chiếu toạ độ VH thấy thực ra nằm TRÊN ✗ unsupported → `FActScore = 1/2 = 0.5`. Điểm mạnh: bắt được claim **quan hệ/thứ tự** mà metric tồn-tại (HER) bỏ qua.
- **Giới hạn về loại claim chấm được:** với 1 ảnh, VH không chứa menu xuất hiện sau khi tap → các claim kiểu "bấm Settings *mở* menu", "menu *chứa* Wi-Fi" không xác minh được trên màn 0. Vì vậy giới hạn vào **claim một-màn**: tồn tại element, label, containment trong cây đang thấy. Claim chuyển-màn chỉ check được khi có next-screen VH (trace); nếu không thì rơi về họ D (uncertainty).
- **Citation (✅):** Min, Krishna, Lyu, Lewis, Yih, Koh, Iyyer, Zettlemoyer, Hajishirzi. *FActScore.* **EMNLP 2023**. ([2023.emnlp-main.741](https://aclanthology.org/2023.emnlp-main.741/))

**2.5. SAFE → VH-Augmented** — agentic, nặng kỹ thuật nhất
- LLM-agent tách fact, lặp truy vấn VH (đặt nhiều câu hỏi con tới VH như một "trợ lý tra cứu"), tổng hợp **F1@K** (F1 tính trên K fact đầu, cân bằng đúng-và-đủ). (Cùng giới hạn chuyển-màn như 2.4.)
- **Ví dụ:** với cùng tutorial ở 2.4, agent tự đặt câu hỏi "VH có node nào tên gần 'Tra cứu nghĩa vụ thuế' không?", "vị trí tương đối so với 'Thanh toán'?" rồi tổng hợp — nặng kỹ thuật hơn FActScore nhưng xử lý được claim phức tạp hơn.
- **Citation (✅):** Wei, Yang, Song, Lu, Hu, Jie Huang, Tran, Peng, Liu, Da Huang, Du, Le. *Long-form factuality in large language models.* **NeurIPS 2024**. arXiv:2403.18802.

### Họ C — Faithfulness NLI / QA *(confidence: trung bình)*

**2.6. SummaC (NLI sentence-pair)** — *tuyến zero-shot ưu tiên* hơn FactCC
- VH-facts = source (nguồn sự thật), mỗi bước = candidate; entailment thấp (mô hình NLI thấy bước "không suy ra được" từ VH) = bịa. (*NLI = natural language inference: cho 2 câu, model phán câu B có suy ra từ câu A không.*)
- **Ví dụ:** source từ VH = "màn hình có nút Tra cứu nghĩa vụ thuế"; candidate (1 bước tutorial) = "bấm nút Đăng xuất ở góc phải" → NLI cho điểm entailment ≈ 0.05 (rất thấp, VH không hề nhắc Đăng xuất) → gắn cờ bịa.
- **Citation (✅):** Laban, Schnabel, Bennett, Hearst. *SummaC.* **TACL 2022**. ([2022.tacl-1.10](https://aclanthology.org/2022.tacl-1.10/))

**2.7. FactCC** — hạ xuống learned baseline, KHÔNG dựng riêng
- **Ví dụ:** FactCC vốn được train bằng cách tự tạo câu "lỗi" (đảo thực thể, đổi số) — VD biến "bấm nút Lưu" thành "bấm nút Xoá" rồi dạy model gắn nhãn "không nhất quán". Vấn đề: nó giỏi bắt đúng loại nhiễu lúc train, nhưng hallucination thật trong tutorial đa dạng hơn → dùng làm baseline chứ không phải tín hiệu chính.
- Không train một FactCC riêng từ VH: chi phí lớn cho 1 metric chẩn đoán, và nó chỉ bắt đúng loại nhiễu loạn dùng để train nên không tổng quát sang hallucination thật. Thay vào đó dùng FactCC như **learned baseline trong track calibrate HaluEval-UI (2.11)** trên cùng cặp (grounded, bịa); ghi nhận overlap phân phối nhiễu loạn train/test là một validity threat; ưu tiên tuyến NLI zero-shot (SummaC §2.6) làm tín hiệu chính.
- **Citation (✅):** Kryściński, McCann, Xiong, Socher. *Evaluating the Factual Consistency of Abstractive Text Summarization.* **EMNLP 2020**. ([2020.emnlp-main.750](https://aclanthology.org/2020.emnlp-main.750/))

**2.8. QAGS (QA-based)** *(trung bình)*
- Sinh câu hỏi từ tutorial → trả lời dựa trên VH; VH trả "không có" = cờ bịa.
- **Ví dụ:** tutorial nói "bấm tab Thông báo" → sinh câu hỏi "Tab nào cần bấm?" → trả lời dựa trên VH: nếu VH không có tab nào tên "Thông báo" thì câu trả lời trống/khác với tutorial → đánh dấu bịa.
- **Citation (✅):** Wang, Cho, Lewis. *QAGS: Asking and Answering Questions to Evaluate the Factual Consistency of Summaries.* **ACL 2020**. ([2020.acl-main.450](https://aclanthology.org/2020.acl-main.450/))

### Họ D — Reference-free / self-consistency *(trung bình)*

**2.9. SelfCheckGPT** — không cần cả VH; bắt được cả bước suy luận (màn ≥1)
- Sample N tutorial (sinh nhiều lần cùng câu hỏi); element xuất hiện ở ít/không sample = nghi bịa (ý: nếu thật thì model phải nói nhất quán). Dùng cho **màn suy luận** (nơi VH không có) và đối chiếu với HER.
- **Ví dụ:** sinh 5 tutorial cho cùng câu hỏi; bước "vào Cài đặt > Bảo mật" chỉ xuất hiện 1/5 lần (4 lần kia đi đường khác) → độ bất định cao → nghi model đang đoán bừa màn suy luận. Ngược lại bước "bấm Tra cứu nghĩa vụ thuế" xuất hiện 5/5 → tin cậy cao.
- **Citation (✅):** Manakul, Liusie, Gales. *SelfCheckGPT.* **EMNLP 2023**. ([2023.emnlp-main.557](https://aclanthology.org/2023.emnlp-main.557/))
- **Nhược:** đo *độ bất định*, không phải tồn tại thật.

### Bổ trợ

**2.10. POPE (probing yes/no)** — diagnostic (chẩn đoán): hỏi model câu yes/no để dò bịa. **Ví dụ:** hỏi "Trên màn hình này có nút 'Đăng xuất' không?" — nếu thực tế VH không có mà model trả "Có" → đó là tín hiệu hallucination. Li, Du, Zhou, Wang, Zhao, Wen. *POPE.* **EMNLP 2023**. ([2023.emnlp-main.20](https://aclanthology.org/2023.emnlp-main.20/))

**2.11. HaluEval-style protocol** — xây "HaluEval-UI" (cặp tutorial chuẩn/bịa từ nhiễu loạn VH) để **calibrate** (hiệu chỉnh, dò ngưỡng) metric tự động + chứa learned baseline FactCC. **Ví dụ:** lấy 1 tutorial đúng, cố ý sửa 1 bước thành sai (đổi nút thật thành nút bịa) → được cặp (đúng, bịa); chạy metric tự động trên cặp này để xem nó có phân biệt được không và ở ngưỡng nào. Li, Cheng, Zhao, Nie, Wen. *HaluEval.* **EMNLP 2023**. ([2023.emnlp-main.397](https://aclanthology.org/2023.emnlp-main.397/))

---

## TIÊU CHÍ 3 — CLARITY / FORMAT

**Caveat LLM-judge dùng chung.** Mọi metric dựa trên LLM/VLM-judge (G-Eval, ALOHa, FActScore, SAFE, SelfCheckGPT) có **rủi ro lỗi tương quan chung** nếu judge thấy *cùng ảnh* và suy luận giống như generator — nguy hiểm nhất ở hallucination (judge cũng không thấy màn 2 thì không phân xử được element bịa ở đó). Vì vậy: ưu tiên **text-only judge ăn VH đã serialize** (không cho ảnh) khi phân xử hallucination, để cắt tương quan.

### 3.1. IFEval-style Format/Structure Compliance — ⭐ xương sống (khách quan)
- Checklist ràng buộc kiểm-chứng-được-bằng-máy (đánh số? token đầu là động từ mệnh lệnh? mỗi bước có element đích? 1 action/bước?). Báo **strict** (đúng 100% mới PASS) **+ loose** (nới một chút).
- **Ví dụ checklist (3 điều kiện) (*ví dụ minh hoạ tự soạn, KHÔNG phải record thật của MobileViews*): "bước có đánh số 1,2,3?" · "động từ mệnh lệnh đầu bước?" · "mỗi bước đúng 1 action?"**
  - *Tutorial PASS:* `1. Bấm "Tra cứu nghĩa vụ thuế". 2. Chọn kỳ tính thuế. 3. Nhấn "Xem".` → có đánh số ✓, đầu mỗi bước là động từ mệnh lệnh (Bấm/Chọn/Nhấn) ✓, mỗi bước đúng 1 hành động ✓ → **PASS** (3/3).
  - *Tutorial FAIL:* `Đầu tiên bạn vào mục tra cứu rồi chọn kỳ và xem kết quả nhé.` → không đánh số ✗, không bắt đầu bằng động từ mệnh lệnh ✗, gộp 3 hành động vào 1 câu ✗ → **FAIL** (0/3).
- **Citation (✅):** Zhou, Lu, Mishra, Brahma, Basu, Luan, Zhou, Hou. *IFEval: Instruction-Following Evaluation for Large Language Models.* arXiv:2311.07911, 2023.

### 3.2. G-Eval (LLM-judge + CoT) — phần "mềm", **phải tự-validate**
- Judge LLM tự sinh bước đánh giá (chuỗi suy luận CoT) rồi chấm (1–5).
- **Ví dụ chấm 1 tutorial:** judge cho tutorial eTax điểm **4/5** về clarity, kèm lý do: "Các bước rõ ràng, đánh số đầy đủ, dùng động từ hành động; trừ 1 điểm vì bước 2 ('Chọn kỳ tính thuế') chưa nói rõ chọn ở đâu/định dạng nào nên người mới vẫn có thể lúng túng." → điểm mềm này phải qua Track B (so với người chấm) mới được tin.
- **Citation (✅):** Liu, Iter, Xu, Wang, Xu, Zhu. *G-Eval.* **EMNLP 2023**. ([2023.emnlp-main.153](https://aclanthology.org/2023.emnlp-main.153/))
- **Lưu ý:** con số tương quan với người Spearman ~0.514 là **đặc thù bộ SummEval**, không phải bảo chứng tổng quát. Coi là *trần* (giới hạn trên) chứ không phải endorsement; G-Eval phải qua Track B mới được tin.

### 3.3. MT-Bench / pairwise LLM-judge — so sánh giữa các hệ thống
- Win-rate/Elo giữa các biến thể generator (đặt 2 tutorial cạnh nhau, hỏi judge "cái nào tốt hơn"); tạo tập ứng viên cho BWS.
- **Ví dụ:** đưa judge 2 tutorial cùng câu hỏi — một do baseline E2E-VLM sinh, một do SoM-Tutor sinh — judge chọn SoM-Tutor tốt hơn ở 7/10 cặp → win-rate 70% cho SoM-Tutor.
- **Citation (✅):** Zheng, Chiang, Sheng et al. *MT-Bench & Chatbot Arena.* **NeurIPS 2023**. arXiv:2306.05685.

### 3.4. Flesch / FKGL — chỉ là **thống kê mô tả**, KHÔNG phải metric clarity headline
- `FKGL = 0.39·(words/sentences) + 11.8·(syllables/words) − 15.59` (FKGL = Flesch-Kincaid Grade Level: ước lượng "cần học lớp mấy mới đọc trôi"; số thấp = dễ đọc).
- **Ví dụ (minh hoạ, số giả định):** một câu tiếng Anh dài 20 từ với nhiều từ đa âm tiết có thể ra FKGL ≈ 12 (trình độ lớp 12); nhưng với một danh sách bước mệnh lệnh ngắn ("Tap Search.") công thức cho điểm méo → đó là lý do FKGL chỉ là thống kê mô tả, không phải metric clarity chính.
- **Citation (✅):** Kincaid, Fishburne, Rogers, Chissom, Report 8-75, 1975 (gốc Flesch, *J. Applied Psychology* 32(3):221–233, 1948).
- **Hai giới hạn:** (1) công thức hiệu chỉnh cho văn xuôi tiếng Anh — danh sách mệnh lệnh ngắn cho điểm méo; (2) với output tiếng Việt, cách đếm âm tiết và hằng số FKGL trở nên vô nghĩa. Vì vậy FKGL chỉ dùng khi đánh giá output tiếng Anh; clarity tiếng Việt dựa vào **IFEval (cấu trúc) + G-Eval**; nếu cần readability tiếng Việt thì nêu rõ proxy riêng.

### 3.5. (Tái diễn giải trục Divergence) — Diversity / chống lặp khuôn — *tuỳ chọn*
- Để "tôn trọng" trục thứ 3 của Chim et al. trong setting reference-free: đo **Distinct-1/2** (tỷ lệ unigram/bigram khác nhau; Li et al., NAACL 2016) và/hoặc **Self-BLEU** (BLEU của mỗi tutorial so với các tutorial còn lại — cao = giống nhau quá; Zhu et al., SIGIR 2018, Texygen), và/hoặc **JSD trên phân phối loại action/element** giữa các tutorial — phát hiện mode collapse (sinh ra na ná nhau) / template lặp.
- **Ví dụ:** nếu cả 50 tutorial đều mở đầu bằng đúng câu "Để thực hiện, bạn hãy làm theo các bước sau:" thì Self-BLEU rất cao / Distinct-1 thấp → cờ template lặp (model học vẹt một khuôn). **Hoặc** nêu rõ Divergence là out-of-scope (không có corpus tham chiếu).

---

## TIÊU CHÍ 4 — TASK SUCCESS (EXTRINSIC) = ĐÓNG GÓP DG2 (ĐA BƯỚC, CÓ GOLD)

*(Các mục §4.1–4.2 cũ — Mind2Web/AITW định nghĩa nền — đã gộp xuống §4.5 do hạ ưu tiên; đánh số 4.3+ giữ nguyên để khỏi xô lệch tham chiếu.)*

**TASK SUCCESS TRONG SCOPE — Suy luận trật tự màn (Screen-Order Inference), reference-based trên dataset CÓ gold.** Task Success bản chất cần **gold trajectory (chuỗi action vàng từng bước)**. Luận văn đưa Task Success vào scope qua đóng góp **DG2** trên **AndroidControl (NeurIPS 2024)** — dataset đa bước có sẵn gold action mỗi bước. Thay vì "đoán mù cả chuỗi từ 1 ảnh", DG2 đặt bài toán **suy luận trật tự**: đưa model **N ảnh XÁO TRỘN** của một luồng + mục tiêu → model phải (1) **suy ra thứ tự đúng**, (2) **sinh hướng dẫn từng bước** theo thứ tự đó. Vì model được xem **mọi màn thật** (chỉ bị xáo thứ tự), grounding chấm được ĐẦY ĐỦ ở mọi bước — mạnh hơn lối "đoán mù màn sau" trước đây.

- **Headline = thứ tự suy ra** đo bằng **Kendall τ-b** trên cặp BẮT BUỘC (§4.4 — *đóng góp mới*). Phụ: pairwise-order-accuracy + position-accuracy@correct-place.
- **Tier A — teacher-forced (skyline / trục tham chiếu chuẩn ngành):** mỗi bước bộ chấm đưa màn hình thật của đáp án vàng, model đoán thao tác kế tiếp rồi so gold. Đây là cách đo step-wise theo chuẩn ngành (mỗi bước độc lập). Metric: **Action-Type acc + Grounding@14% + Step-SR** (§4.3).

**Khai báo bắt buộc (chống đọc nhầm):**
- **Chế độ N-ảnh là BÀI TOÁN ĐẶT RA ĐỂ ĐO** năng lực suy luận trật tự (trả lời câu hỏi của thầy "làm sao model biết trật tự màn"), KHÔNG khẳng định là nhu cầu deploy phổ biến.
- **Tier A teacher-forced KHÔNG phải sản phẩm 1-ảnh.** Nó là **dụng cụ đo / cận trên (skyline)** có chủ đích cho model xem màn thật mỗi bước, để đặt kết quả trong cùng giao thức tham chiếu ĐỊNH TÍNH với ngoài. KHÔNG claim "ngang hàng leaderboard" (pipeline SoM-Tutor detect element từ ẢNH, khác setup leaderboard; recall detector chưa được công bố rõ — giả thuyết làm việc chờ K1: có thể chỉ ~một nửa element được phát hiện — kéo số xuống).
- **ORACLE-ORDER (skyline của trục ordering):** đưa model N ảnh ĐÃ SẮP ĐÚNG + mục tiêu → chỉ sinh hướng dẫn (không phải xếp). **SELF-ORDER (thật):** N ảnh xáo trộn → model tự xếp rồi mới sinh. **ordering gap = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER)** = "cái giá của việc không biết trật tự" (xem §4.4). Sanity cứng: ORACLE-ORDER ≥ SELF-ORDER mọi episode (vi phạm = bug).

### 4.3. AndroidControl — TRỤ DG2 Tier A (Action-Type + Grounding@14% + Step-SR) — ⭐ chính

Đây là trụ định lượng của DG2 Tier A (teacher-forced, đo step-wise theo chuẩn ngành). Ba metric:

- **Action-Type accuracy** = tỷ lệ bước model đoán **đúng LOẠI thao tác** (tap / swipe / type / press…) so gold.
- **Grounding@14%** = với thao tác có tọa độ, coi là **đúng vị trí** nếu điểm model đoán nằm trong bán kính ~14% kích thước màn hình quanh điểm gold, HOẶC rơi vào cùng bbox GT. (Ngưỡng 14% = "đủ gần thì tính đúng", theo khoảng cách chuẩn hoá của màn hình — quy ước gốc từ AITW, NeurIPS 2023.)
- **Step-SR (Step Success Rate)** = tỷ lệ bước **đúng CẢ loại thao tác LẪN vị trí/đối số**. Step-SR thuộc Tier A (trục tham chiếu chuẩn ngành).
- **Ví dụ tính bằng số (EX-B, app Đồng hồ — *ví dụ minh hoạ tự soạn, KHÔNG phải record thật của AndroidControl*):** goal *"đặt báo thức 7:00 sáng"*; chuỗi gold 3 bước: **B1** bấm tab "Báo thức" → **B2** bấm "+" → **B3** gõ "0700" rồi "OK". Ở Tier A, mỗi bước bộ chấm đưa **màn hình thật** của bước trước rồi cho model đoán bước kế. Model đoán đúng cả 3 → **Action-Type = 3/3** (đúng loại: tap, tap, type), **Step-SR = 3/3** (đúng cả loại lẫn vị trí/đối số). Đây là mốc skyline tham chiếu chuẩn ngành (trục ordering có skyline riêng là ORACLE-ORDER — xem §4.4).
- **Low / High:** Low = prompt có mô tả từng bước; High = chỉ cho goal, model tự lập kế hoạch → ánh xạ *đơn bước vs đa bước*.
- **Phân vai citation:** metric *gốc* của AndroidControl là step-wise accuracy + episode accuracy — trích **Li, Bishop, Li, Rawles, Campbell-Ajala, Tyamagundlu, Riva. *On the Effects of Data Scale on UI Control Agents.* NeurIPS 2024.** arXiv:2406.03679. Cách tách "Type Acc / Grounding Acc / SR" (kèm ngưỡng grounding bán kính 14%) là **giao thức của OS-Atlas** (Wu et al., *OS-Atlas*, arXiv:2410.23218 — preprint; trích như hiện vật kỹ thuật, KHÔNG trình như peer-reviewed), không phải của AndroidControl. Vậy: dùng cách tách này thì trích OS-Atlas cho *protocol* và AITW (2307.10088) cho *ngưỡng 14%*.
- **Khung điều kiện recall:** mọi số grounding ở Tier A vẫn đóng khung "có điều kiện recall=X% (cổng K1)" như DG1.

### 4.4. DG2 ordering — Metric SẮP THỨ TỰ MÀN (Kendall τ-b headline + ordering gap) — ⭐ MỚI

Đo **năng lực suy luận trật tự màn**: model nhận **N ảnh XÁO TRỘN** của một luồng + mục tiêu → tự suy ra thứ tự đúng. Headline là **Kendall τ-b** trên thứ tự model suy ra so với thứ tự gold. Đây là **đóng góp mới** của luận văn (suy luận trật tự màn GUI có điều kiện hoá theo use-case).

**4.4.1. Kendall τ-b — headline.**
- **Công thức:** với mỗi cặp màn `(i, j)`, đếm **concordant** (model xếp cùng chiều với gold) và **discordant** (ngược chiều). `τ-b = (C − D) / sqrt((C + D + T_x)·(C + D + T_y))` — trong đó C = #cặp concordant, D = #cặp discordant, `T_x`/`T_y` = #cặp bị "buộc bằng" (tie) ở thứ tự model / gold. τ-b ∈ [−1, +1]; +1 = trùng khít, 0 = ngẫu nhiên, −1 = đảo ngược hoàn toàn. (Phiên bản τ-b xử lý được ties — phù hợp khi có cặp tự-do tính như tie, xem dưới.)
- **CHẤM THEO THỨ-TỰ-BỘ-PHẬN (partial-order-aware) — QUYẾT ĐỊNH BẮT BUỘC.** Không phải mọi cặp màn đều có một thứ tự "đúng" cứng. Chia cặp làm 2 loại:
  - **Cặp BẮT BUỘC** (thứ tự ràng buộc): đảo là **sai thật**. Nhận diện bằng **ordering cue gating / drill-down** (đăng nhập trước khi xem kết quả; màn chi tiết phải sau màn danh sách). *Ví dụ:* "đăng-nhập-trước → xem-kết-quả" — đảo lại là sai.
  - **Cặp TỰ-DO** (thứ tự không ràng buộc): đảo **vẫn tính ĐÚNG**. *Ví dụ:* màn điền Email và màn điền SĐT độc lập nhau → người dùng điền cái nào trước cũng được → đảo không bị phạt.
  - **HEADLINE τ-b chỉ tính trên CẶP BẮT BUỘC.** Để biết cặp nào bắt buộc → dò gating/drill-down (trùng với ordering-cues ở pipeline). Cặp tự-do được loại khỏi C/D headline (hoặc tính như tie).
- **τ-b-THÔ (điểm sàn / robustness):** báo THÊM **τ-b tính trên TOÀN BỘ cặp theo thứ tự gốc của gold** (coi mọi cặp đều bắt buộc) làm "điểm sàn" — phòng khi việc gán nhãn cặp bắt buộc/tự-do có sai sót. Headline (cặp bắt buộc) và τ-b-thô báo song song.

**4.4.2. Metric phụ.**
- **pairwise-order-accuracy** = #cặp model xếp đúng chiều / #cặp (trên cặp bắt buộc). KHÔNG dùng làm headline (vì pairwise-acc thô dễ thành tautology với cách model được hỏi từng cặp); chỉ là số đối chiếu.
- **position-accuracy@correct-place** = tỷ lệ màn được model đặt **đúng vị trí tuyệt đối** trong chuỗi so với gold.

**4.4.3. Loại N nhỏ + cảnh báo τ-b rời rạc.**
- **Loại N≤2:** N=2 chỉ có 1 cặp → τ-b chỉ nhận `{−1, +1}` → vô nghĩa. Trục N thực tế **N ∈ [3, ~10]**. Phải **báo số episode còn lại ở mỗi mốc N** (việc tuần-1, cổng **KN** — tự đếm histogram độ dài episode AndroidControl; khảo sơ bộ: mean ~5.5, p95=13 → cần tự đếm chính xác).
- **Cảnh báo phân phối rời rạc:** với N nhỏ, τ-b chỉ nhận ÍT giá trị rời rạc (VD **N=3 chỉ có 4 giá trị khả dĩ** trên 3 cặp). Vì vậy **CI-width phải tính cho phân phối RỜI RẠC** (bootstrap trên tập episode, không giả định τ-b liên tục/chuẩn). Báo CI theo từng mốc N riêng, không gộp.

**Ví dụ tính bằng số (EX-B, app Đồng hồ — DG2 ordering — *ví dụ minh hoạ tự soạn, KHÔNG phải record thật của AndroidControl*):** luồng gold 3 màn theo thứ tự **B1** (tab "Báo thức") → **B2** (màn "+") → **B3** (màn picker giờ). Đưa model 3 ảnh XÁO TRỘN `{B2, B3, B1}` + mục tiêu "đặt báo thức 7:00". Cặp B1→B2 và B1→B3 là **bắt buộc** (phải vào tab + mở "+" trước khi tới picker — drill-down); cặp B2→B3 cũng bắt buộc (picker chỉ mở sau khi bấm "+").
- Model suy ra thứ tự `B1 → B3 → B2` (đảo B2/B3). So gold: cặp (B1,B2) concordant ✓, (B1,B3) concordant ✓, (B2,B3) discordant ✗ → C=2, D=1, không tie → `τ-b = (2−1)/sqrt(3·3) = 1/3 ≈ 0.33`.
- **pairwise-order-accuracy = 2/3 ≈ 0.67** (2 trên 3 cặp đúng chiều). **position-accuracy@correct-place:** B1 đúng chỗ (vị trí 1), B3 sai (gold ở 3, model đặt 2), B2 sai → 1/3 ≈ 0.33.
- *Lưu ý:* ví dụ trên cho 1 episode để dễ hình dung; số thật là **trung bình trên nhiều episode** ở từng mốc N, chỉ đọc được khi đạt ngưỡng CI-width pre-register (§4.6) và tính trên phân phối rời rạc.

**ORDERING GAP (skyline vs thật).**
- **ORACLE-ORDER (skyline):** đưa model N ảnh **ĐÃ SẮP ĐÚNG** + mục tiêu → chỉ sinh hướng dẫn (không phải xếp). **SELF-ORDER (thật):** N ảnh xáo trộn → model tự xếp rồi mới sinh.
- **ordering gap = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER)** = **"cái giá của việc không biết trật tự"**.
- **Sanity cứng:** ORACLE-ORDER ≥ SELF-ORDER ở **mọi episode** (vi phạm = bug).
- **Cảnh báo floor-effect:** ordering gap chỉ có nghĩa nếu metric chất-lượng-tutorial NHẠY với thứ tự. Nếu không nhạy thì **τ-b là trục chính**, gap chỉ phụ.

**Tái dùng hạ tầng (bắt buộc, để công bằng & nhất quán):**
- Dùng **cùng matcher freeze + resolver đối xứng như DG1** (cùng bộ luật khớp text→element, áp đối xứng cho model lẫn gold).
- **Báo RAW vs ORACLE cho cả ORACLE-ORDER lẫn SELF-ORDER** (RAW = chạy thật với detector; ORACLE-detector = giả định detector hoàn hảo) — phân biệt với ORACLE-ORDER ở trên (cái này nói về thứ tự, kia nói về detector).
- **Chống leak step-index (cổng KB):** khi xáo trộn PHẢI strip metadata + tái mã hoá ảnh + đặt tên UUID, để model không suy ra thứ tự từ tên file / EXIF. CI test: detector mù chỉ xem pixel không được suy ra thứ tự tốt hơn ngẫu nhiên.
- **Citation (✅):** Kendall, M.G. *A New Measure of Rank Correlation.* **Biometrika 30(1/2):81–93, 1938.** Cách dùng τ-b trong meta-evaluation NLG: Gao, Hu, Lin, Wan. *Analyzing and Evaluating Correlation Measures in NLG Meta-Evaluation.* **NAACL 2025** (arXiv:2410.16834). (Đã có trong Track B §B.3.)

### 4.5. (Tùy chọn — nền định nghĩa) Mind2Web + AITW (vai dataset đối chứng)

> Hai mục dưới hạ xuống **tùy chọn ở vai dataset**. **Ngoại lệ BẮT BUỘC:** AITW vẫn **bắt buộc** ở **vai nguồn ngưỡng 14%** (đã trích ở §4.3).

- **Mind2Web — Element Acc / Operation F1 / Step SR / Task SR** *(tùy chọn — nền định nghĩa, KHÔNG còn là "định nghĩa chính" của Task Success)*:
  **Element Acc** = #bước chọn đúng element / #bước. **Op F1** = F1 token-level trên operation+đối số. **Step SR** = đúng cả element VÀ operation. **Task SR** = mọi bước đúng (~7.3 hành động/task).
  Mind2Web cần `pos/neg candidates` (web/DOM) — **MobileViews/AndroidControl không có** → chỉ **mượn định nghĩa** khi cần, tính bằng AITW-style matching. **Mind2Web = future-work nhánh web.**
  - **Citation (✅):** Deng, Gu, Zheng, Chen, Stevens, Wang, Sun, Su. *Mind2Web.* **NeurIPS 2023** D&B (Spotlight). arXiv:2306.06070.
- **AITW — Action Matching + Partial Score** *(dataset đối chứng = tùy chọn; nhưng vai NGUỒN NGƯỠNG 14% = bắt buộc — xem §4.3)*:
  Khớp action type; tap/swipe khớp nếu điểm trong **~14% khoảng cách màn hình** HOẶC cùng bbox GT. `Partial = #bước khớp / độ dài episode`.
  - **Citation (✅):** Rawles, Li, Rodriguez, Riva, Lillicrap. *Android in the Wild (AITW).* **NeurIPS 2023** D&B. arXiv:2307.10088.

### 4.6. DG2-null — pre-register để KHÔNG thành tautology

**Cảnh báo phương pháp:** không được phát biểu kiểu "số nào cũng là phát hiện" — như thế là **tautology** (luôn đúng, vô nghĩa). Phải **đăng ký trước (pre-register)** một **giả thuyết CÓ THỂ BỊ BÁC** kèm ngưỡng, để cả khi FAIL kết quả vẫn có nghĩa. **DỒN POWER VÀO 1 TRỤC = τ-b ordering** (không pre-register nhiều trục song song).

- **Giả thuyết pre-register (có thể bị bác):**
  - (H1) **τ-b giảm đơn điệu khi N tăng** (3 → 4 → 5+): luồng càng dài, sắp đúng càng khó.
  - (H2) **τ-b(pairwise) > τ-b(listwise)** vượt CI (so dưới điều kiện FAIR-COMPUTE — cùng ngân sách gọi model): cách hỏi từng-cặp-rồi-tổng-hợp (Copeland) xếp tốt hơn cách ép-permutation-1-call.
- **Ngưỡng "đọc được":** quy định trước một **CI-width tối đa** (độ rộng khoảng tin cậy, tính trên phân phối **rời rạc** theo từng mốc N) để số τ-b được coi là "đọc được / ổn định".
- **Quy tắc quyết định:** nếu τ-b **KHÔNG giảm đơn điệu theo N** / chênh pairwise−listwise **KHÔNG vượt CI** / nhiễu vượt CI-width đã chốt → **DG2 FAIL CÓ Ý NGHĨA** (kết luận có giá trị: suy luận trật tự **không đo ổn định ở quy mô này**) — đây mới là *null thật*, không phải tautology.
- Pre-registration bao **CẢ HAI** đóng góp (giả thuyết + effect-size kỳ vọng + quy tắc quyết định, chốt **trước khi chạy**).

---

## TRACK B — VALIDATE METRIC TỰ ĐỘNG BẰNG CHUYÊN GIA
*Chứng minh metric DG1 đáng tin (tinh thần Phụ lục A.2 của Chim et al.: thu điểm người tin cậy rồi đo tương quan với metric tự động).*

### B.1. Best-Worst Scaling (BWS / MaxDiff)
- Tuple 4 item, chọn **best & worst**; `score = (#best − #worst)/#xuất hiện ∈ [−1,1]`. Cần ~1.5N–2N tuple cho N item. (*BWS / MaxDiff = thay vì chấm điểm tuyệt đối 1–5 dễ lệch, người chấm chỉ chọn "tốt nhất / tệ nhất" trong nhóm 4 — đáng tin hơn.*)
- **Ví dụ 1 tuple (4 tutorial cho cùng câu hỏi):** đưa chuyên gia tuple {T_A, T_B, T_C, T_D}; họ chọn **best = T_C**, **worst = T_A**. Giả sử mỗi tutorial xuất hiện trong **5 tuple**: nếu T_C được chọn best 4 lần và worst 0 lần → `score(T_C) = (4 − 0)/5 = +0.8`; nếu T_A best 0 lần, worst 3 lần → `score(T_A) = (0 − 3)/5 = −0.6`. Bảng score này rồi đem tương quan (Spearman/Kendall) với điểm metric tự động ở B.3.
- **Citation (✅):** Kiritchenko, Mohammad. *Best-Worst Scaling More Reliable than Rating Scales.* **ACL 2017** (gốc Louviere & Woodworth 1990). ([P17-2074](https://aclanthology.org/P17-2074/))

### B.2. Inter-Annotator Agreement — Krippendorff's α / Cohen's & Fleiss' κ
- **Đo gì:** mức **đồng thuận giữa các người chấm** (chỉnh cho sự trùng khớp ngẫu nhiên); cao = nhãn người đáng tin để làm chuẩn. Thang quen thuộc: α/κ ≥ 0.8 rất tốt, 0.67–0.8 chấp nhận được.
- **Ví dụ:** 3 chuyên gia cùng chấm 60 tutorial; nếu Krippendorff's α = 0.74 → mức đồng thuận "chấp nhận được", đủ tin để dùng làm anchor; nếu α = 0.3 → người chấm bất đồng nhiều, phải làm rõ guideline trước khi tin số.
- **Citation (✅):** Krippendorff, *Content Analysis*, Sage 1980/2004; Cohen 1960 (*EPM* 20(1):37–46); Fleiss 1971 (*Psych. Bulletin* 76:378–382).

### B.3. Spearman ρ **+ Kendall τ-b** (auto vs human) — ⭐ chốt hạ
*(Mục đích: kiểm điểm metric tự động có xếp hạng tutorial giống người không.)*
- **ρ (chi tiết kỹ thuật):** Pearson trên *hạng*. Khi có ties (hạng trùng — phổ biến ở điểm BWS) dùng định nghĩa Pearson-trên-hạng, KHÔNG dùng `1−6Σd²/(n(n²−1))` của Spearman 1904 vì công thức đó chỉ đúng khi không có hạng trùng.
- **Thực hành tốt:** báo thêm **Kendall τ-b** (bền hơn với nhiều ties / N nhỏ của annotation chuyên gia) và **bootstrap 95% CI + ý nghĩa thống kê** cho mỗi metric — một giá trị ρ đơn lẻ rất mong manh khi N nhỏ.
- **Ví dụ:** xếp hạng 60 tutorial theo điểm HER tự động, xếp hạng cũng 60 tutorial đó theo điểm BWS của người → Spearman ρ = 0.68, Kendall τ-b = 0.52, bootstrap 95% CI = [0.55, 0.79] → tương quan thuận khá mạnh và ổn định → HER **đủ tin làm anchor**. Nếu CI rộng phủ qua 0 (VD [−0.1, 0.6]) → chưa đủ bằng chứng, không được tin.
- **Cho DG2 ordering:** validate thứ tự bằng cách đo **Kendall τ-b giữa thứ tự π̂ model suy ra và thứ tự do người đánh giá sắp** (trên một slice episode mà chuyên gia tự sắp lại N màn xáo trộn) — kiểm tra τ-b tự động có khớp thứ tự người không, song song với cách validate metric tutorial ở trên.
- **Citation (✅):** Spearman 1904 (*Am. J. Psychology* 15:72–101); Gao, Hu, Lin, Wan. *Analyzing and Evaluating Correlation Measures in NLG Meta-Evaluation.* **NAACL 2025** (arXiv:2410.16834).

---

## Ghi chú độ tin cậy — phân biệt 2 nghĩa "High"
- **"Citation = real" (đã verify):** TẤT CẢ citation trong file (kể cả G-Eval, MT-Bench) đều thật.
- **"Metric đáng tin cho bài này":** KHÁC. Vài metric citation-real nhưng **độ tin dùng làm anchor chỉ trung bình** và **phải tự-validate qua track B trước khi tin**: G-Eval (ρ~0.514, rủi ro shared-error), MT-Bench (bias judge), SummaC/FactCC/QAGS/SelfCheckGPT/HaluEval (adapt sang VH còn nhiều lựa chọn thiết kế).

---

<details>
<summary><strong>Nhật ký sửa</strong> (so với bản nháp đầu, sau 2 vòng review đối kháng — bấm để mở)</summary>

1. **Chim et al.** "ACL 2025" → **Computational Linguistics 51(1):191–233, MIT Press, 2025** (journal). *[lỗi nặng, committee sẽ bắt]*
2. **AndroidControl/OS-Atlas:** giữ nguyên bản gốc (Type/GR/SR là protocol OS-Atlas) — đã verify 2 vòng; bác đề xuất đảo ngược.
3. **SAFE** thêm tác giả **Jie Huang**.
4. **IoU** ✗ UGround/SeeClick → ✓ PASCAL VOC (Everingham 2010).
5. **ScreenSpot-Pro** bỏ "(ICLR 2025)" (mâu thuẫn niên đại) → "(preprint)".
6. **Task Success:** thêm cảnh báo nổi bật "chiều duy nhất cần gold trajectory" + 2 lối đi.
7. **Caveat toàn cục** màn-thấy vs màn-suy-luận; **bước text→element** cho grounding; **chống đếm trùng** hallucination + **quy ước hướng điểm**.
8. Thêm **FaithScore** + **coverage/VALOR-EVAL**; **FactCC** hạ xuống baseline; giới hạn ví dụ claim FActScore/SAFE vào màn 0.
9. **Flesch** hạ xuống thống kê mô tả + cảnh báo tiếng Việt; **G-Eval** 0.514 là SummEval-specific; mở rộng caveat LLM-judge.
10. Thêm **mapping table Chim→4 tiêu chí** + tái diễn giải **Divergence** (§3.5); **Kendall τ-b + bootstrap CI** cho track B.
11. **ĐA BƯỚC VÀO SCOPE (theo SPEC CHỐT):** dựng đóng góp **DG2 = Task Success reference-based** trên AndroidControl, gồm **Tier A (teacher-forced)** + đóng góp mới **DG2 ordering (suy luận trật tự màn)**. Trục phân định DG1/DG2 đổi sang **"có gold hay không"** (KHÔNG còn dùng "reference-free vs reference-based" làm trục gốc); thêm **cầu nối đầu file**.
12. **Nâng AndroidControl thành trụ DG2 Tier A** (§4.3): ba metric **Action-Type + Grounding@14% + Step-SR** (giữ nguyên citation AndroidControl NeurIPS2024 + OS-Atlas[preprint, hiện vật kỹ thuật] + AITW cho ngưỡng 14%).
13. **ĐỔI TRỤC §4.4 → DG2 ordering (suy luận trật tự màn, mới):** headline **Kendall τ-b** (Kendall 1938 + Gao NAACL 2025) chấm **partial-order-aware** (chỉ phạt cặp BẮT BUỘC, báo thêm τ-b-thô làm điểm sàn) + phụ pairwise-order-accuracy + position-accuracy@correct-place; **ordering gap = ORACLE-ORDER − SELF-ORDER**; loại N≤2, CI-width tính trên phân phối rời rạc; tái dùng matcher freeze + resolver đối xứng như DG1; báo **RAW vs ORACLE**; chống leak step-index (cổng KB). *(Bỏ hẳn blind-horizon step-match@k / observability gap / k\* của bản nháp trước.)*
14. **Mind2Web + AITW hạ xuống tùy chọn (vai dataset)** (gộp vào §4.5); bỏ câu coi Mind2Web Step SR là "định nghĩa chính" Task Success. **AITW phân vai đôi:** vai nguồn ngưỡng 14% vẫn **BẮT BUỘC**.
15. **Thêm §4.6 DG2-null** (pre-register giả thuyết bác được, **dồn power 1 trục = τ-b ordering**: τ-b giảm đơn điệu khi N tăng + τ-b(pairwise) > τ-b(listwise) vượt CI dưới fair-compute + ngưỡng CI-width) để null KHÔNG thành tautology.
16. **Tinh chỉnh CAVEAT toàn cục:** "unverifiable" chỉ áp **MobileViews (DG1, màn-0)**; **AndroidControl/DG2 đo bình thường** (gold + N màn thật, chỉ bị xáo thứ tự). Khai báo **hợp đồng 1-ảnh** (Tier A là skyline/dụng cụ đo, không claim leaderboard; ordering gap = ORACLE-ORDER − SELF-ORDER, kèm cảnh báo floor-effect). **Mọi citation giữ nguyên.**

</details>

---

> **Giải thích nhanh các thuật ngữ (kèm hướng điểm):**
> - **DG1 / DG2** — hai đóng góp đánh giá; trục phân định = *có gold trajectory hay không*. DG1 = màn-0, không gold tutorial (Tiêu chí 1–3); DG2 = đa bước, có gold (Tiêu chí 4).
> - **Teacher-forcing (Tier A)** — cho model "xem đáp án màn trước" rồi đoán bước kế; đo từng bước độc lập. *Cao = tốt.*
> - **DG2 ordering (Screen-Order Inference)** — N ảnh xáo trộn → model tự suy ra thứ tự đúng rồi sinh tutorial. *Headline = Kendall τ-b, cao = tốt.*
> - **Kendall τ-b** — tương quan hạng giữa thứ tự model suy ra và thứ tự gold; chấm **partial-order-aware** chỉ trên **cặp BẮT BUỘC**; báo thêm **τ-b-thô** trên toàn cặp làm điểm sàn. *Cao = tốt (+1 trùng khít).*
> - **Cặp bắt buộc vs tự-do** — cặp bắt buộc (gating/drill-down) đảo = sai; cặp tự-do (vd điền mail/sdt) đảo vẫn đúng.
> - **pairwise-order-accuracy / position-accuracy@correct-place** — metric phụ: tỷ lệ cặp đúng chiều / tỷ lệ màn đúng vị trí tuyệt đối. *Cao = tốt.*
> - **ordering gap = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER)** — cái giá của việc không biết trật tự. *Nhỏ = tốt; chỉ có nghĩa nếu metric tutorial nhạy thứ tự.*
> - **Action-Type / Grounding@14% / Step-SR** — đúng loại thao tác / đúng vị trí trong bán kính 14% / đúng cả hai. *Cao = tốt.*

> *Lưu ý nguồn gốc lỗi MobileViews "bịa metric": đó là nhầm lẫn PHIÊN BẢN paper, không phải bịa — xem `02_datasets.md`.*
