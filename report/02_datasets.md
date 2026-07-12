# BÁO CÁO 2 — BA BỘ DATASET CHỐT + VAI

> 🔧 **CẬP NHẬT 2026-06-25 (design E):** **TRỌNG TÂM = AndroidControl** (có `goal` thật + đáp án vàng + cây accessibility mỗi màn → chở phần lớn metric: grounding/bịa/coverage từng màn + τ-b xếp thứ tự + Step-SR tới-đích). **MobileViews** = kiểm 1-màn (vai nhẹ, câu hỏi tự soạn). **ScreenSpot** = đối chứng tìm-nút. Lý do: dồn claim nặng vào dataset bình duyệt + goal thật ⇒ khỏi bị vặn "câu hỏi tự bịa". *(Cây a11y AndroidControl đã verify parse được — xem `report/14`.)* Bản dễ hiểu: `report/00_DOC_TU_DAU.md`.

## TÓM TẮT 30 GIÂY
- File này chốt **ba bộ dataset** và **vai cố định** của từng bộ: **MobileViews** (màn-0, có VH + bbox pixel) → DG1; **AndroidControl** (đa bước, gold action mỗi bước) → DG2; **ScreenSpot-v2** (đối chứng grounding peer-reviewed) → bù credibility cho DG1.
- Input của hệ luôn là **ảnh + câu hỏi**; VH / gold-trajectory chỉ dùng làm **tham chiếu chấm điểm**, không phải input lúc sinh.
- Đề tài chia **hai đóng góp**: **DG1** (không có tutorial gold của người, chấm bằng VH-silver) và **DG2 — Suy luận trật tự màn (Screen-Order Inference)**: đưa **N ảnh XÁO TRỘN** của 1 luồng đa bước + mục tiêu → model (1) suy ra **thứ tự đúng**, (2) sinh hướng dẫn từng bước theo thứ tự đó. Vẫn giữ **Tier A teacher-forced** làm trục tham chiếu chuẩn ngành; thêm hai cấu hình **ORACLE-ORDER** (đưa N ảnh đã sắp đúng) vs **SELF-ORDER** (đưa N ảnh xáo trộn, tự xếp) để đo **ordering gap**.
- Toàn bộ đo đa bước nghiêm túc dồn về **AndroidControl**; MobileViews Complete Traces chỉ là vật liệu phụ; Mind2Web đã hạ xuống future-work (nhánh web).
- Điểm cần lưu ý: cảnh báo "MobileViews bịa metric" của bản nháp **là sai** — đó chỉ là nhầm phiên bản paper (đính chính ở mục MobileViews). Mọi số grounding kèm điều kiện recall detector (cổng K1) — **recall detector trên UI mobile CHƯA được công bố rõ trong tài liệu; cái đã công bố là *grounding accuracy* ~57% trên ScreenSpot, KHÔNG phải recall. K1 = TỰ đo recall (cổng cứng); giả thuyết làm việc: có thể ~một nửa.**

> **Hai ví dụ "xương sống" dùng xuyên suốt file** (mọi nơi minh họa đều bám 2 ví dụ này; con số khác sẽ ghi rõ "(giả định)"):
> ⚠️ **CẢNH BÁO:** EX-A và EX-B dưới đây là **ví dụ minh hoạ TỰ SOẠN** để giải thích cách chấm, **KHÔNG phải record có thật** lấy ra từ dataset. Record THẬT (đã verify qua web/đọc file) được tách riêng ở **HỘP-THẬT** ngay bên dưới bảng này.
>
> | Mã | Bộ | Tình huống | 1 record trông như thế nào | "Chấm thử" minh họa |
> |---|---|---|---|---|
> | **EX-A** | MobileViews (màn-0) | App thuế eTax **(ví dụ minh hoạ, không phải record thật)** | 1 ảnh màn hình + 1 file VH JSON. Node ví dụ: `{text:"Tra cứu nghĩa vụ thuế", bounds:[270,820,540,1010], clickable:true}` | Grounding: model chỉ điểm click `(405,915)` → kiểm `(405,915) ∈ [270,820,540,1010]` → **TRÚNG** |
> | **EX-B** | AndroidControl (đa bước) | App Đồng hồ **(phỏng theo format action thật của AndroidControl — `action_type`/`TAP`/`TYPE` — nhưng app Đồng hồ + giờ `0700` là nội dung tự dựng để minh hoạ)** | 1 episode goal = "đặt báo thức 7:00" + chuỗi (ảnh mỗi bước, gold action): **B1** TAP "Báo thức" → **B2** TAP "+" → **B3** TYPE "0700" + TAP "OK" | **Tier A** (đưa màn thật mỗi bước rồi hỏi): máy đoán → so gold = **3/3**. **Suy luận trật tự (DG2):** đưa **3 ảnh XÁO TRỘN** (B3, B1, B2) + goal → model xếp lại → so thứ tự gold bằng **Kendall tau-b** (chỉ tính trên cặp BẮT BUỘC). |

### Ba record THẬT (đã verify web)

> **HỘP-THẬT (gốc canonical).** Đây là **record có thật** trích/đối chiếu trực tiếp từ tài liệu chính chủ của 3 bộ — dùng để đối chiếu khi EX-A/EX-B (minh hoạ tự soạn) gây hiểu nhầm. Khi nghi ngờ, lấy HỘP-THẬT làm chuẩn.

1. **AndroidControl — 1 episode THẬT (gold trajectory):**
   - `goal` = `"On cruisedeals, view cruise schedules for a four-night trip from New York to Canada"`
   - **B1** `{action_type: open_app, app_name: "CruiseDeals"}` → **B2** `{action_type: click, x: 313, y: 742}` → **B3** `{action_type: swipe, direction: "up"}`.
   - *Nguồn: Google Research `android_control` README.*
   - **Ghi rõ:** record gold này (goal + chuỗi action) **DÙNG LÚC CHẤM** (reference-based, so với cái model đoán), **KHÔNG phải input lúc sinh** — lúc sinh model vẫn chỉ thấy ảnh + câu hỏi.

2. **ScreenSpot (HF `rootsautomation/ScreenSpot`) — 1 mẫu THẬT:**
   - `instruction` = `"close"` ; `bbox` = `[0.948, 0.144, 0.994, 0.207]` (**chuẩn-hoá 0–1**, dạng `[x_min, y_min, x_max, y_max]`) ; `data_type` = `"icon"` ; `source` = `Windows` (icon nút Close của Windows).
   - *Nguồn: dataset `rootsautomation/ScreenSpot` trên HuggingFace.*

3. **MobileViews — schema THẬT (đã đối chiếu cấu trúc):**
   - Mỗi screen = 1 ảnh + 1 file `state_*.json` chứa View Hierarchy (VH).
   - Mỗi node có `viewClass` / `text` / `bounds` `[left, top, right, bottom]` (**pixel**) / `clickable`.
   - `bounds` của **node gốc (root)** = `[0, 0, 1080, 1920]` (kích thước màn).
   - **NÊU THẲNG:** giá trị `text`/`bounds` của các **node con** thật trong MobileViews **CHƯA mở được** ở bản report này — hiện chỉ xác nhận được **schema + bounds của root**. → Cần **tải 1 shard** mới có giá trị node con thật (việc trong checklist mục 1).

**Câu nối:** 3 record THẬT trên dùng **3 format toạ độ khác nhau** (pixel `[l,t,r,b]` / chuẩn-hoá 0–1 `[x_min,y_min,x_max,y_max]` / điểm click `(x,y)`) → xem **CHỐT-BBOX** ngay dưới đây.

### CHỐT-BBOX — ba format toạ độ KHÁC NHAU giữa 3 bộ (gốc canonical)

| Bộ | Format toạ độ | Cụ thể |
|---|---|---|
| **MobileViews** | bbox **pixel** | `[left, top, right, bottom]` (pixel tuyệt đối, vd root `[0,0,1080,1920]`) |
| **ScreenSpot (HF)** | bbox **chuẩn-hoá 0–1** | `[x_min, y_min, x_max, y_max]` (vd `"close"` → `[0.948,0.144,0.994,0.207]`) |
| **AndroidControl** | **điểm click `(x,y)`** trong action | toạ độ click nằm trong gold action (vd `click x:313 y:742`), không phải bbox |

> ⚠️ **CẢNH BÁO BUG (đưa vào checklist P2):** harness **PHẢI convert về cùng một hệ toạ độ** trước khi so point-in-bbox / Grounding@14%. Cụ thể: với ScreenSpot phải **nhân toạ độ chuẩn-hoá 0–1 với `(W, H)`** của ảnh để ra pixel; với AndroidControl so điểm click `(x,y)` vào bbox pixel của element. Trộn lẫn 3 format mà không quy đổi là **nguồn bug dễ mắc nhất** khi code chấm → phải kiểm tra rõ ràng (test 1 mẫu mỗi bộ).

---

> **Mục đích:** mô tả ba bộ dataset đã CHỐT và vai trò cố định của từng bộ. Mọi facts đã kiểm chứng đối kháng 2 vòng.

**Thuật ngữ rút gọn (giải thích đời thường):**
- **VH (View Hierarchy):** cây cấu trúc của màn hình (gồm tọa độ từng nút bấm) — dùng làm "đáp án để chấm", KHÔNG phải input lúc sinh.
- **bbox (bounding box):** khung chữ nhật pixel `[left,top,right,bottom]` bao quanh một element — để kiểm tra điểm model định click có rơi đúng nút không.
- **Tier A (teacher-forced):** mỗi bước bộ chấm đưa màn THẬT của đáp án vàng rồi hỏi model thao tác kế → đo step-wise theo chuẩn ngành; là dụng cụ đo / skyline, KHÔNG phải sản phẩm 1-ảnh.
- **Suy luận trật tự màn (Screen-Order Inference):** đưa N ảnh XÁO TRỘN của 1 luồng + mục tiêu → model tự suy ra thứ tự đúng rồi sinh hướng dẫn. Là bài toán DG2 đặt ra ĐỂ ĐO năng lực suy luận trật tự (trả lời câu hỏi "làm sao model biết trật tự"), KHÔNG khẳng định là nhu cầu deploy phổ biến.
- **ORACLE-ORDER vs SELF-ORDER:** ORACLE-ORDER = đưa N ảnh ĐÃ sắp đúng + mục tiêu → chỉ sinh hướng dẫn (skyline). SELF-ORDER = đưa N ảnh xáo trộn → tự xếp rồi sinh (thật). **ordering gap** = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER) = "cái giá của việc không biết trật tự".
- **Kendall tau-b:** hệ số tương quan hạng giữa thứ tự model xếp và thứ tự gold — HEADLINE của trục suy luận trật tự, chỉ tính trên **cặp BẮT BUỘC** (gating/drill-down); cặp tự-do (đảo vẫn đúng) không bị phạt.

---

## BA BỘ CHỐT — VAI CỐ ĐỊNH

Mỗi bộ làm đúng một việc, không chồng chéo:

| Bộ dataset | Vai cố định | Phục vụ đóng góp |
|---|---|---|
| **MobileViews** (preprint arXiv) | Ảnh + **VH** + **bbox pixel** → mỏ neo chấm grounding/hallucination/clarity trên **màn-0** | **DG1** (màn-0, không có tutorial gold người) |
| **AndroidControl** (NeurIPS 2024 D&B, peer-reviewed) | **Episode đa bước + gold action mỗi bước** → (a) Tier A teacher-forced (tham chiếu chuẩn ngành) + (b) **suy luận trật tự màn**: xáo trộn N ảnh của episode rồi đo model xếp lại | **DG2** (suy luận trật tự màn, có gold trajectory làm thứ tự vàng) |
| **ScreenSpot-v2** (bản -v2 do OS-Atlas, **ICLR 2025**; ScreenSpot gốc = SeeClick, **ACL 2024**) | **Đối chứng grounding** (point-in-bbox accuracy của resolver) + **bù credibility** cho MobileViews | Đối chứng đơn-vị cho DG1 (KHÔNG đối chứng pipeline đa bước) |

**Lưu ý vai:**
- **MobileViews Complete Traces** chỉ là **vật liệu phụ** để cung cấp **ngữ cảnh chuyển màn** minh họa cho DG1 — **đa bước ĐỊNH LƯỢNG THẬT dồn hết về AndroidControl** (vì AndroidControl có gold action chuẩn từng bước). KHÔNG tính số đa bước nghiêm túc trên MobileViews traces nữa.
- **AITW (NeurIPS 2023)** KHÔNG nằm trong "ba bộ chốt" như một dataset trục, nhưng là **nguồn ngưỡng 14% bắt buộc** phải trích (xem mục Vai trò). Vai đối chứng của AITW là **tùy chọn**.
- **Mind2Web** đã **hạ xuống future-work** (nhánh web), giữ mô tả bên dưới để tham chiếu.
- **GUI-Odyssey, AMEX** = **future-work robustness** (kiểm chứng chéo trục trật tự trên thêm bộ trajectory mobile) — **KHÔNG nằm trong lõi** scope chốt; chỉ dùng nếu mở rộng sau.

---

## Bảng so sánh nhanh

> Hai cột đầu là **bộ chốt trục** (MobileViews + AndroidControl); ScreenSpot-v2 là **đối chứng grounding**; Mind2Web để tham chiếu (đã hạ future-work).

| Khía cạnh | **MobileViews** | **AndroidControl** | **ScreenSpot-v2** | **Mind2Web** (future-work) |
|---|---|---|---|---|
| Nền tảng | **Mobile (Android)** | **Mobile (Android)** | Mobile + Desktop + Web (GUI grounding) | **Web (trình duyệt desktop)** |
| Quy mô | **Paper full-set: 1.213.866 screen / 30.037 app** *(bản tải HF nhỏ hơn — xem ghi chú)*; HuggingFace tải được hiện: **~600K cặp / ~20K app (~475GB), tức MobileViews-600K** | **15.283 episode / 14.548 unique tasks / 833 app** (train **13.604 ep / 74.722 step**), mean **~5.5 step/ep** (p5=1, p95=13) | ~1.2K mẫu instruction→element (bản v2 đã làm sạch nhãn) | **2.350 task / 137 site / 31 domain**, avg **7.3 hành động/task** |
| "Mỏ neo" cấu trúc | **View Hierarchy** (JSON Accessibility + XML uiautomator) | Gold **action mỗi bước** (loại thao tác + tọa độ/đích) + a11y tree | bbox của element đích cho mỗi instruction | **DOM/HTML** (raw + cleaned) |
| **Bounding box pixel** | ✅ **CÓ** — `bounds: [left,top,right,bottom]` pixel tuyệt đối + cờ clickable/editable/scrollable | ✅ tọa độ/đích pixel theo gold action | ✅ **CÓ** — bbox pixel của element đích | ❌ **KHÔNG** field bbox; định vị bằng `backend_node_id` + thuộc tính DOM¹ |
| Đơn/đa bước | Cặp ảnh–VH đơn lẻ **+ Complete Traces** (states/views/actions.csv) | **Đa bước** (episode đầy đủ, gold từng bước) → Tier A (teacher-forced) + **suy luận trật tự màn** (xáo trộn N ảnh, xếp lại) | **Đơn-bước** (1 instruction → 1 element) — KHÔNG đa bước | **Đa bước** (trajectory đầy đủ, teacher-forcing) |
| **Phục vụ suy luận trật tự** | — (đơn lẻ) | ✅ **episode có thứ tự vàng sẵn** → xáo trộn để đo xếp lại; mean ~5.5 step (N in [3,~10]) | — (đơn-bước) | (web, future-work) |
| Độ dài (action/task) | — | **~5.5** (NeurIPS 2024 D&B; train 74.722 step / 13.604 ep = 5.49; p5=1, p95=13) | — (đơn-bước) | **~7.3** |
| Ảnh chụp màn hình | ✅ mọi screen | ✅ mỗi bước | ✅ mỗi mẫu | ✅ có (raw dump + **Multimodal-Mind2Web**) |
| Metric "chính thức" | ⚠️ **đổi theo phiên bản** (xem cảnh báo) — v1: downstream tasks; v3: RL grounding ScreenSpot-v2/Pro | ✅ **Action-Type acc / Grounding@14% / Step-SR** (Tier A, step-wise) + **Kendall tau-b** (trục trật tự) | ✅ **point-in-bbox accuracy** (grounding) | ✅ **Element Acc / Operation F1 / Step SR / Task SR** |
| Ngôn ngữ GUI | Anh + **Trung** (**không có tiếng Việt**) | Anh (**không có tiếng Việt**) | Anh (**không có tiếng Việt**) | Anh (US-centric) |
| Splits | Không có split toàn cục sẵn (theo ID/app) | có split chuẩn (IID + unseen app/category) | theo nền tảng (mobile/desktop/web) | **cross-task / cross-website / cross-domain** (252 / 177 / 912 test) |
| License / tải | **MIT**, HuggingFace (resumable) | mở (Google Research) | mở (HuggingFace) | Data **CC-BY-4.0**, code MIT; **test set bị gate** (train mở) |
| Tình trạng | arXiv preprint (chưa peer-review xác nhận) | **NeurIPS 2024 D&B** — đã bình duyệt | **ScreenSpot gốc = SeeClick (ACL 2024)** — đã bình duyệt; **bản -v2 do OS-Atlas (ICLR 2025)** làm sạch nhãn | **NeurIPS 2023** D&B (Spotlight) — đã bình duyệt |

¹ *Bản Multimodal-Mind2Web có expose bbox chuẩn hoá [0,1] suy ra từ DOM (`bounding_box_rect`), nhưng là **DOM-derived**, không phải nhãn pixel như VH của MobileViews → điểm khác biệt cốt lõi vẫn đúng.*

**So sánh độ dài trajectory giữa các bộ (để định cỡ trục N):** AndroidControl **~5.5** < AITW **~6.5** < Mind2Web **~7.3** action/task. AndroidControl ngắn nhất nhưng đủ dải N∈[3,~10] sau khi loại N≤2 → phù hợp đo suy luận trật tự (số episode còn lại ở mỗi mốc N báo sau khi tự đếm histogram).

**Khung điều kiện recall** (áp cho MobileViews, ScreenSpot VÀ AndroidControl): mọi con số grounding/tutorial đều kèm chú "**recall = X%**" của detector trích element từ ẢNH. **Lưu ý: recall của detector trên UI mobile CHƯA được công bố rõ trong tài liệu** — cái đã công bố là *grounding accuracy* ~57% (ScreenSpot), KHÔNG phải recall. Đây là **cổng cứng K1** — **TỰ đo recall TRƯỚC** khi chốt với thầy (giả thuyết làm việc: có thể ~một nửa). Không có số grounding nào được trình "trần" mà không đóng khung recall.

---

## MobileViews — chi tiết

- **Citation (✅):** Gao, Zhang, Wang, Gao, Liu, Luan, Wang, Li, Xu. *MobileViews: A Million-scale and Diverse Mobile GUI Dataset.* arXiv:2409.14337. **Là preprint** (v1/v2 9/2024 tên "A Large-Scale…"; v3 11/2025 đổi tên "Million-scale").
- **Mỗi screen:** ảnh JPG + VH 2 biến thể gần giống (**JSON** Accessibility Service, **XML** uiautomator). **Complete Traces:** `states/` + `views/` + `actions.csv` (`from_state/to_state/action`). Annotation GPT-4o trên ~13K screen: **~13K summary, ~26K QA, ~26K caption** (✅ verify).
- **Cấu trúc VH (✅ verify):** cây lồng nhau, node có `viewClass`, `text/label`, `bounds` pixel `[left,top,right,bottom]` (vd `[0,0,1080,1920]`), cờ tương tác. Key gốc JSON `viewHierarchy`. Ghép ảnh–VH qua CSV (`Image File`/`JSON File`) hoặc Parquet (`image_content`/`json_content`). Bbox là **pixel tuyệt đối** (claim "normalize (0,1)" không có cơ sở — đã loại).

**Ví dụ một bản ghi cụ thể (EX-A — app thuế eTax) — (VÍ DỤ MINH HOẠ tự soạn, KHÔNG phải record thật):** cấu trúc node (các trường `viewClass`/`text`/`bounds`/`clickable`) là **thật**, nhưng nội dung `"Tra cứu nghĩa vụ thuế"` + toạ độ là **tự soạn** để minh hoạ; schema thật + bounds root `[0,0,1080,1920]` xem **HỘP-THẬT** ở trên. 1 screen gồm file ảnh `screen_001.jpg` (1080×1920) + file `screen_001.json` chứa cây `viewHierarchy`; trong cây có node:

```json
{ "viewClass": "Button", "text": "Tra cứu nghĩa vụ thuế",
  "bounds": [270, 820, 540, 1010], "clickable": true }
```

`bounds` đọc là `[left, top, right, bottom]` pixel: nút này nằm trong khung từ điểm trên-trái `(270,820)` tới điểm dưới-phải `(540,1010)`.

**Ví dụ "chấm thử" — nối MobileViews → metric grounding (point-in-bbox):**
- *Câu hỏi use-case (tự soạn) (ví dụ minh hoạ):* "Tôi muốn kiểm tra đã nộp thuế chưa thì vào đâu?"
- *Model trả lời:* "Bước 1: Click nút **Tra cứu nghĩa vụ thuế**" và đề xuất điểm click `(405, 915)`.
- *Chấm:* kiểm `270 ≤ 405 ≤ 540` (đúng) và `820 ≤ 915 ≤ 1010` (đúng) → điểm rơi **trong** bbox → **TRÚNG (hit)** cho tiêu chí grounding. Nếu model thay vào đó "cite" một nút không có trong VH (vd "Đăng xuất") → tính là **hallucination**. Đây chính là cách VH-silver thay cho "tutorial gold của người" mà DG1 không có.

### ĐÍNH CHÍNH QUAN TRỌNG — MobileViews KHÔNG "bịa metric" (lỗi nhầm phiên bản)
Bản nháp trước cảnh báo các metric *Tappability F1 / Element Relationship / UI Component Identification / ScreenQA / 90-10 split / "outperform Rico"* là bịa. **Kiểm chứng vòng 2 cho thấy điều đó sai — chúng CÓ THẬT, ở bản v1 (9/2024).** Sự thật:
- **v1 (Sep 2024):** đánh giá bằng **downstream tasks** — Tappability (Binary F1), Element Relationship (Binary F1), UI Component Identification (Multi-class F1, 5 lớp), ScreenQA ShortQA/ComplexQA (SQuAD F1); **split 90/10**; so Rico ở **cùng cỡ 66.1K** (MobileViews thắng tappability & element-relationship; Rico thắng UI component F1 73.08 vs 63.96).
- **v3 (revised 25/11/2025, bản arXiv HTML hiện tại):** **thay** bằng **RL-based GUI grounding (GRPO trên framework VLM-R1)** đánh giá trên **ScreenSpot-v2 (+2.2%)** và **ScreenSpot-Pro (+6.1%)** (UI-TARS-1.5).
- **Bài học:** vòng verify đầu chỉ đọc v3 nên tưởng "bịa". Khi viết luận văn phải **ghi rõ phiên bản** đang trích. Chỉ "Label-to-View Matching" là chưa xác minh được ở cả hai bản.
- **Dù dùng bản nào:** với luận văn, MobileViews vẫn dùng như **kho ảnh + VH (bbox)** để làm scoring anchor; **metric đánh giá tutorial lấy từ Báo cáo 1**, không phải bê metric nội bộ của MobileViews.

### Mạnh
- Quy mô lớn, app **2024 hiện đại**. **Bội số so Rico (~63K screen) phụ thuộc bản nào:** **~19× screen CHỈ đúng cho full-set 1.2M** (Table 1 full-paper: 1.213.866/63.370 ≈ 19×ᵃ); **vì luận văn DÙNG bản MobileViews-600K nên thực tế là ~9× screen** (600K/63.370 ≈ 9.5×). App: 30.037/9.772 ≈ 3×. **Khi trích phải ghi rõ đang so bản nào** (full 1.2M hay 600K).

ᵃ *63.370 = số **screen của Rico**, dùng làm mẫu số để so tỉ lệ; đừng nhầm với 30.037 = số **app** của MobileViews.*
- **Mọi screen có VH + bbox pixel + cờ tương tác** = đúng mỏ neo element-level.
- **Traces đa bước** (states+VH+actions) để neo chuyển màn.
- **MIT**, tải dễ; đa độ phân giải.

### Yếu
- **Không có tutorial người viết & không câu hỏi use-case** → luận văn tự soạn input + vật liệu validate.
- Traversal tự động bằng VLM → label VH **có thể nhiễu/thiếu**; traces **chưa benchmark** chất lượng task-flow.
- **Không split toàn cục**; ~475GB; preprint chưa peer-review.
- **GUI tiếng Anh + Trung, KHÔNG có tiếng Việt** (quan trọng — xem khuyến nghị).

### Áp dụng vào luận văn (DG1 — màn-0)
Mỏ neo **chính** cho grounding & hallucination trên **màn-0** (model chỉ thấy ảnh + câu hỏi; chấm bằng VH bbox). Đây chính là **DG1 — màn-0, KHÔNG có tutorial gold do người viết**: chấm bằng **VH-silver** (anchor cấu trúc, không phải tutorial-người). *Nhãn "reference-free" ở đây hiểu theo **nghĩa hẹp = KHÔNG có tutorial gold do người viết; VẪN có anchor VH-silver** — không được để cụm "reference-free" đứng trần.*

**Complete Traces = vật liệu phụ:** chỉ dùng làm **ngữ cảnh chuyển màn** minh họa (next-screen VH cho thấy màn kế trông thế nào), KHÔNG dùng để **đo đa bước định lượng**. **Toàn bộ đo đa bước nghiêm túc dồn về AndroidControl** (vì AndroidControl mới có gold action chuẩn từng bước). Việc phải tự làm: soạn câu hỏi use-case, tập chuyên gia, split riêng.

---

## AndroidControl — chi tiết (DG2: suy luận trật tự màn, có gold trajectory)

- **Citation (✅):** Li et al. *On the Effects of Data Scale on UI Control Agents.* **NeurIPS 2024 D&B** (Datasets & Benchmarks Track) — peer-reviewed. arXiv:2406.03679. Bộ gồm **15.283 episode / 14.548 unique tasks / 833 app** (train **13.604 ep / 74.722 step**) — **episode đa bước** ghi lại tác vụ điều khiển điện thoại Android thật, **mỗi bước có gold action** (loại thao tác + đích/tọa độ) → đúng vật liệu để chấm reference-based theo từng bước.
  - **Số liệu độ dài (✅ verify):** mean **~5.5 step/episode** (Table 1 ghi 4.8; tính lại từ train 74.722 step / 13.604 ep = 5.49), **percentile-5 = 1 step**, **percentile-95 = 13 step**. **KHÔNG có số đếm theo từng N** trong paper → phải **tự đếm histogram** (cổng KN).
- **Vai (CHỐT):** đây là **trục DG2 (suy luận trật tự màn)** của luận văn. Hai phần: (a) **Tier A teacher-forced** = trục tham chiếu chuẩn ngành (giữ); (b) **suy luận trật tự màn** = xáo trộn N ảnh của episode rồi đo model xếp lại (trục chính).

**Ví dụ một bản ghi cụ thể (EX-B — app Đồng hồ):** 1 episode có `goal = "đặt báo thức 7:00"` gồm 3 bước, mỗi bước có (ảnh màn hình bước đó + gold action):

| Bước | Ảnh (model thấy gì) | Gold action |
|---|---|---|
| **B1** | màn chính app Đồng hồ | `TAP "Báo thức"` |
| **B2** | tab Báo thức | `TAP "+"` (thêm báo thức) |
| **B3** | màn nhập giờ | `TYPE "0700"` + `TAP "OK"` |

Bộ chấm dùng gold action từng bước này làm tham chiếu (reference-based). Mỗi gold action gồm **loại thao tác** (TAP/TYPE/SCROLL…) + **đích** (text element hoặc tọa độ/bbox pixel).

**Ví dụ "chấm thử" — nối AndroidControl → metric (Tier A tham chiếu + suy luận trật tự):**

- **Tier A (teacher-forced — trục tham chiếu chuẩn ngành):** bộ chấm lần lượt đưa **ảnh THẬT của từng bước gold**, hỏi model "thao tác kế là gì?":
  - đưa ảnh B1 → model đoán `TAP "Báo thức"` → khớp gold ✔
  - đưa ảnh B2 → model đoán `TAP "+"` → khớp gold ✔
  - đưa ảnh B3 → model đoán `TYPE "0700" + TAP "OK"` → khớp gold ✔
  - → **Step-SR = 3/3**. (Action-Type acc: 3/3 đúng loại; Grounding@14%: điểm click rơi trong ngưỡng 14% là đúng đích.)
- **Suy luận trật tự màn (DG2 — trục chính):** bộ chấm **xáo trộn 3 ảnh** (vd thứ tự đưa vào: B3, B1, B2) + đưa goal `"đặt báo thức 7:00"` → model phải **tự xếp lại** đúng thứ tự B1→B2→B3 rồi sinh hướng dẫn. Chấm thứ tự bằng **Kendall tau-b partial-order-aware**:
  - Cặp (B1 "Báo thức", B2 "+") và (B2 "+", B3 nhập giờ) là **cặp BẮT BUỘC** (drill-down: phải mở tab Báo thức rồi mới thêm rồi mới nhập giờ) → đảo là **sai thật**, bị phạt.
  - Nếu trong một luồng khác có hai thao tác **độc lập** (vd điền Email và điền SĐT) thì đó là **cặp TỰ-DO** → model đảo trước-sau vẫn **tính ĐÚNG**, KHÔNG phạt.
  - **HEADLINE tau-b chỉ tính trên cặp BẮT BUỘC**; báo THÊM **tau-b-thô** (so toàn bộ thứ tự gốc, mọi cặp) làm "điểm sàn" robustness.

### Tier A — teacher-forced (trục tham chiếu chuẩn ngành)
- **Cách đo:** mỗi bước bộ chấm đưa màn THẬT của đáp án vàng, model đoán thao tác kế, so gold. Metric: **Action-Type acc** (đoán đúng loại thao tác: click/type/scroll…), **Grounding@14%** (điểm click rơi trong ngưỡng 14% — ngưỡng mượn từ AITW), **Step-SR** (đúng cả loại + đích trong 1 bước).
- Tier A là **đánh giá step-wise theo chuẩn ngành** (mỗi bước độc lập, teacher-forced) mà thầy expect → **giữ làm TRỤC THAM CHIẾU**, **KHÔNG còn là "đa bước chính"**. Trục chính của DG2 là **suy luận trật tự màn** (xáo trộn N ảnh, tự xếp).
- **KHÔNG tuyên bố "ngang hàng leaderboard":** pipeline SoM-Tutor (OmniParser detect element từ ảnh) khác setup leaderboard, recall detector (chưa công bố rõ — tự đo ở K1, giả thuyết ~một nửa) kéo số xuống → chỉ "đặt trong cùng giao thức để tham chiếu, KHÔNG ngang hàng".
- **Hoà giải no-leak:** nguyên tắc "VH/màn thật KHÔNG vào lúc sinh" áp cho CLAIM VỀ SẢN PHẨM (DG1 + chế độ suy luận trật tự). Tier A là thí nghiệm cho model xem màn thật mỗi bước — là **dụng cụ đo / skyline step-wise**, không được trình như năng lực sản phẩm 1-ảnh.

### Suy luận trật tự màn — XÁO TRỘN ảnh để đo sắp-thứ-tự (DG2, trục chính)
**Ý tưởng:** AndroidControl episode đã có sẵn **thứ tự vàng** (gold trajectory theo từng bước). Ta lợi dụng điều đó để dựng bài toán **sắp-thứ-tự**: lấy episode gold → tách N ảnh các bước → **xáo trộn** → đưa kèm goal cho model → model phải suy ra **thứ tự đúng** rồi sinh hướng dẫn theo thứ tự đó. Thứ tự gold làm tham chiếu chấm.

- **Quy trình dựng mẫu (chống leak step-index — cổng KB):**
  1. Lấy episode gold (thứ tự vàng có sẵn).
  2. **Strip metadata** mọi trường lộ thứ tự (số bước, timestamp, tên file `state_001/002…`).
  3. **Tái mã hoá ảnh** (re-encode lại pixel, xoá EXIF/thứ tự byte) + **đặt tên UUID ngẫu nhiên** cho từng ảnh.
  4. **Xáo trộn** thứ tự đưa vào model.
  5. Model tự xếp → đo bằng **Kendall tau-b partial-order-aware** so với thứ tự gold.
  - **CI test của KB:** một detector "mù" chỉ xem pixel **không** được suy ra thứ tự tốt hơn ngẫu nhiên (nếu có → còn rò step-index, phải sửa).
- **ORACLE-ORDER vs SELF-ORDER (đo ordering gap):**
  - **ORACLE-ORDER (skyline):** đưa N ảnh **ĐÃ sắp đúng** + goal → model chỉ sinh hướng dẫn (không phải tự xếp).
  - **SELF-ORDER (thật):** đưa N ảnh **xáo trộn** → model tự xếp rồi mới sinh.
  - **ordering gap** = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER) = **"cái giá của việc không biết trật tự"**. Sanity cứng: ORACLE-ORDER ≥ SELF-ORDER − ε ở **mọi episode** (vượt ε = bug). Cảnh báo floor-effect: gap chỉ có nghĩa nếu metric tutorial NHẠY với thứ tự; nếu không, **tau-b là trục chính**, gap chỉ phụ.
- **CẢNH BÁO KN — phải TỰ ĐẾM histogram độ dài episode TRƯỚC:** AndroidControl chỉ công bố mean ~5.5 step (p5=1, p95=13), **KHÔNG có số đếm theo từng N** → phải tự dựng histogram. **Loại N≤2** (N=2 chỉ 1 cặp → tau-b chỉ nhận {−1,+1}, vô nghĩa). Trục N thực tế N ∈ **[3, ~10]** (đường-cong headline chốt trần N≤6; báo thêm tới ~8–10 nếu ngân sách); mọi mốc N báo kèm **số episode còn lại** ở mốc đó.
- **CẢNH BÁO partial-order:** chỉ phạt khi sai **cặp BẮT BUỘC**. Cặp **TỰ-DO** (vd điền Email/SĐT độc lập) đảo trước-sau vẫn tính ĐÚNG. **Nhãn cặp BẮT BUỘC suy TỪ GOLD trajectory bằng quy tắc tất định** (màn B chỉ xuất hiện SAU khi thực thi gold-action trên màn A ⇒ cặp (A,B) bắt buộc; không có quan hệ nhân-quả đó = tự-do) — **KHÔNG suy từ bộ phát-hiện cue (gating/drill-down)** mà model dùng, để tránh tự-chấm/vòng-lập-luận. Gold chỉ vào KHÂU CHẤM OFFLINE, không phải input lúc model xếp.
- **Bộ-ba baseline đối xứng GOAL-ONLY / VISUAL-ONLY / RANDOM-ORDER:** **GOAL-ONLY** = che hết ảnh, chỉ đưa goal + nhãn trong → nếu goal-only đã xếp đúng cao thì **goal có thể tự lộ thứ tự**, cue giao diện không phải nguồn tín hiệu chính (phải báo cảnh báo này); **VISUAL-ONLY** = che goal, chỉ đưa N ảnh xáo trộn → đo phần thứ tự suy được CHỈ từ cue giao diện (đối xứng với GOAL-ONLY để tách nguồn tín hiệu); **RANDOM-ORDER** = xếp ngẫu nhiên làm sàn.

### Khai báo hợp đồng 1-ảnh / N-ảnh khi dùng AndroidControl
- **Input router:** N=1 → đơn bước (về DG1 màn-0); N≥2 → bật chế độ suy luận trật tự (DG2). Một hệ duy nhất.
- **Tier A teacher-forced = trục tham chiếu chuẩn ngành / skyline step-wise, KHÔNG phải sản phẩm 1-ảnh.**
- **Suy luận trật tự (N ảnh xáo trộn) = bài toán ĐẶT RA ĐỂ ĐO** năng lực suy luận trật tự (trả lời câu hỏi thầy "làm sao model biết trật tự"), KHÔNG khẳng định là nhu cầu deploy phổ biến.
- **ordering gap = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER)** = giá của việc không biết trật tự.
- **Khung điều kiện recall** (recall = X%, cổng K1) áp cho **cả AndroidControl**.

---

## ScreenSpot(-v2) — chi tiết (đối chứng grounding)

- **Citation (✅):** ScreenSpot **gốc** giới thiệu trong **SeeClick** (Cheng et al., **ACL 2024**) — peer-reviewed; **ScreenSpot-v2** là bản **làm sạch lại nhãn** (sửa lỗi annotation của bản gốc) do **OS-Atlas (Wu et al., ICLR 2025)** công bố — KHÔNG phải ACL 2024. Mỗi mẫu = 1 instruction ngôn ngữ tự nhiên → 1 element đích có **bbox pixel**, phủ **mobile/desktop/web**.
- **Vai (CHỐT):** **đối chứng đơn-vị** cho **point-in-bbox accuracy của resolver** — tức kiểm bộ phận "đổi ID/điểm click sang bbox" của pipeline có grounding đúng không, trên một benchmark peer-reviewed → đồng thời **bù điểm yếu credibility** của MobileViews (preprint).
- **GIỚI HẠN VAI:** ScreenSpot **CHỈ đối chứng đơn-vị point-in-bbox accuracy của resolver**, **KHÔNG đối chứng pipeline tutorial nhiều bước**. ScreenSpot là **đơn-bước** (1 instruction → 1 element), không có trajectory → không thể dùng để hợp lệ hoá phần đa bước. Phải ghi rõ giới hạn này để khỏi bị hiểu nhầm là "đã validate cả pipeline".
- **Khung điều kiện recall** cũng áp cho mọi số đo trên ScreenSpot.

**Ví dụ một bản ghi cụ thể:** 1 mẫu = instruction `"open the settings menu"` + element đích có bbox pixel `[270,820,540,1010]` "(giả định)" trên 1 ảnh. (Đơn-bước: chỉ 1 instruction → 1 element, KHÔNG có chuỗi như EX-B.) ⚠️ **Lưu ý format:** record THẬT của ScreenSpot dùng **bbox chuẩn-hoá 0–1** (vd `"close"` → `[0.948,0.144,0.994,0.207]`, xem **HỘP-THẬT**), **KHÁC** format pixel; con số `[270,820,540,1010]` ở đây là **SỐ MINH HOẠ PIXEL** đặt cho khớp với ví dụ eTax (EX-A), **không phải** mẫu ScreenSpot thật.

**Ví dụ "chấm thử" — vai đối chứng point-in-bbox:** ta đưa cùng instruction cho **resolver** (bộ phận "đổi ID/điểm click thành bbox" của pipeline). Resolver trả điểm `(405,915)` **(số minh hoạ)** → kiểm `(405,915) ∈ [270,820,540,1010]` → **trúng**. Vì **ScreenSpot gốc (SeeClick, ACL 2024) / ScreenSpot-v2 (OS-Atlas, ICLR 2025) — đều peer-reviewed**, điểm point-in-bbox đo ở đây là bằng chứng "resolver grounding đúng" trên benchmark có uy tín → **bù credibility** cho con số tương tự đo trên MobileViews (preprint). Lưu ý: đây mới chỉ chứng minh **một bộ phận** (resolver), KHÔNG chứng minh cả pipeline đa bước.

---

## Mind2Web — chi tiết (future-work, nhánh web)

**Đã hạ xuống future-work.** Giữ mô tả để tham chiếu khi mở rộng sang nhánh web về sau — KHÔNG nằm trong scope đo định lượng chính.

- **Citation (✅):** Deng, Gu, Zheng, Chen, Stevens, Wang, Sun, Su. *Mind2Web: Towards a Generalist Agent for the Web.* **NeurIPS 2023** D&B (Spotlight). arXiv:2306.06070. ([project](https://osu-nlp-group.github.io/Mind2Web/) · [code](https://github.com/OSU-NLP-Group/Mind2Web))
- **Modalities (✅ verify):** lõi **HTML/DOM** (`raw_html`+`cleaned_html`). Hành động: `action_reprs` + `actions` (operation+target). Operations **CLICK/TYPE/SELECT** (HOVER/ENTER ở `original_op`). Raw dump có screenshot base64, MHTML, HAR. **Multimodal-Mind2Web** ghép ảnh+HTML.
- **Cấu trúc (✅ verify):** DOM = "VH analogue". Mỗi bước có `pos_candidates`+`neg_candidates` (tag/attributes/`backend_node_id`). **Không bbox pixel** — định vị bằng DOM node. Trang TB **~1.135 element → ~580 sau cleaning**. **Lưu ý số 94.7%:** đây là **recall của BƯỚC CLEANING DOM trên training data** (giữ được element đích sau khi rút gọn cây) — **KHÔNG phải Recall@50 của bộ candidate**; Recall@50 candidate là **85–89%**. Đừng lẫn hai con số.
- **Metric chính thức (✅ verify):** Element Acc; Operation F1; **Step SR** (đúng cả element+operation); **Task SR** (mọi bước đúng — rất nghiêm vì ~7.3 hành động). Đánh giá **offline/teacher-forcing**.

### Mạnh
- **Website thật, đa dạng** (137 site/31 domain); **đa bước thật** với trajectory chuẩn → lý tưởng Task-Success matching.
- DOM annotation giàu (pos/neg candidates); **splits cross-task/website/domain** đo generalization.
- Bộ metric chuẩn, **nhiều paper web-agent dùng** → dễ so sánh; bản multimodal hỗ trợ VLM; license thoáng.

### Yếu
- **Không bbox pixel**; đánh giá **offline trên 1 trajectory vàng** → phạt oan đường đi hợp lệ khác; **không phải success thực thi trực tuyến** (online execution success, như WebArena — Zhou et al., 2023).
- **Task SR cực nghiêm** (gần 0); **chỉ web/DOM, tiếng Anh, US-centric**; HTML lớn (~1.135 element/trang) → tiền xử lý nặng.
- **Quan trọng:** **thiếu bbox pixel native** (định vị bằng DOM node, không có nhãn pixel như VH) → không neo grounding point-in-bbox đầy đủ như MobileViews/AndroidControl; đây là **nhánh web** riêng, không cùng nền tảng mobile của scope chính.
- Test set **bị gate**.

### Áp dụng vào luận văn
Đối trọng **phía web**: DOM + pos/neg candidates làm mỏ neo (model vẫn chỉ thấy ảnh); trajectory + Step SR/Element Acc/Op F1 cho **Task Success đa bước** (mượn **định nghĩa**); splits cho generalization.

---

## Vai trò 3 bộ đã CHỐT (+ AITW phân vai đôi)

Ba bộ trục chia vai như sau (Mind2Web hạ future-work, AITW phân vai đôi):

1. **MobileViews → DG1 (màn-0).** Trụ cột chấm là **bbox pixel của VH** → chỉ MobileViews có sẵn bbox pixel ở quy mô lớn. Vai: kho ảnh + VH-silver để chấm grounding/hallucination/clarity trên màn-0. Complete Traces chỉ là **vật liệu phụ ngữ cảnh chuyển màn** (không đo đa bước định lượng ở đây).
2. **AndroidControl → DG2 (suy luận trật tự màn, có gold trajectory làm thứ tự vàng).** Episode + gold action mỗi bước → (a) **Tier A teacher-forced** (trục tham chiếu chuẩn ngành) + (b) **suy luận trật tự màn** (xáo trộn N ảnh, đo xếp lại bằng Kendall tau-b; ORACLE-ORDER vs SELF-ORDER → ordering gap). **Toàn bộ đo đa bước nghiêm túc nằm ở đây**, không còn rải trên MobileViews traces.
3. **ScreenSpot-v2 → đối chứng grounding.** Đối chứng đơn-vị point-in-bbox accuracy của resolver + bù credibility cho MobileViews (preprint). KHÔNG đối chứng pipeline đa bước (đơn-bước).

### AITW — phân vai đôi (BẮT BUỘC ghi rõ)
- **(a) NGUỒN NGƯỠNG 14% = trích BẮT BUỘC (citation), KHÔNG tùy chọn.** Ngưỡng Grounding@14% dùng ở Tier A có gốc từ **AITW (NeurIPS 2023)** → phải trích AITW như nguồn của ngưỡng dù không dùng AITW làm dataset trục.
- **(b) dataset đối chứng = TÙY CHỌN.** Nếu cần thêm một benchmark trajectory mobile đối chiếu thì có thể dùng AITW, nhưng đây là lựa chọn không bắt buộc.
- *Ghi chú nguồn: protocol tách Action-Type/Grounding/SR được trích như **hiện vật kỹ thuật**. (OS-Atlas = **ICLR 2025, peer-reviewed** — trình đúng là đã bình duyệt.)*

### Mind2Web — đã hạ future-work
- **Mind2Web = future-work nhánh web.** Lý do hạ: **thiếu bbox pixel native** (định vị bằng DOM node, không có nhãn pixel như VH) → không neo grounding point-in-bbox đầy đủ; và là **nhánh web** riêng, khác nền tảng mobile của scope chính. Khi nào mở rộng nhánh web mới dùng, **không nằm trong scope đo định lượng chính**.

### Động cơ tiếng Việt vs dữ liệu (giữ nguyên cảnh báo)
- Ví dụ "nộp thuế"/eTax và ưu tiên tiếng Việt là **mục tiêu triển khai (deployment target)**, **nhưng cả ba bộ trục đều là GUI Anh/Trung, KHÔNG có app Việt** → đo định lượng diện rộng neo trên màn Anh/Trung; **muốn có màn tiếng Việt phải tự thu thập riêng**. Phải tách bạch "động cơ" và "dữ liệu chấm" khi trình thầy.

### Hoà giải metric ↔ dataset (điểm thầy dễ hỏi)
Vấn đề cũ: "Step-SR cần gold trajectory mà MobileViews không có". Cách giải là **phân vai dataset** (không còn vá bằng AITW-style trên MobileViews traces hay proxy reachability):
- **Step-SR reference-based ĐÃ TRONG SCOPE** — đo trực tiếp qua **AndroidControl Tier A** (vì AndroidControl **CÓ gold action mỗi bước**). Không cần chế Step-SR trên MobileViews nữa.
- **MobileViews chỉ làm màn-0 (DG1)** — đây là phần **không-gold-tutorial**, chấm bằng VH-silver, KHÔNG đòi Step-SR.
- **Suy luận trật tự màn (DG2) đo Kendall tau-b + ordering gap** — đóng góp **MỚI** trên AndroidControl. Độ mới (trung thực, không claim "xếp ảnh xáo là mới"): (a) domain GUI màn-hình + (b) điều kiện hoá theo mục tiêu/use-case + (c) gắn ordering → SINH tutorial + (d) signal-attribution (ordering cues nào giúp xếp đúng). Thừa nhận lineage **Sort-Story** (Agrawal et al., EMNLP 2016 — chấm bằng **Spearman**, KHÔNG phải Kendall τ) · **Sequencing Multimodal Instructional Manuals** (Wu et al., ACL 2022) · **RankGPT** (Sun et al., EMNLP 2023 — là **phương pháp listwise**, không phải metric). *Tiền lệ dùng **Kendall τ chấm ordering** trích từ **Lapata 2006** (Computational Linguistics 32(4):471–484); 🔧 **τ-b partial-order-aware = Kendall trên bucket-order/partial-order của Fagin et al. (SIAM JDM 2003 optimistic p=0; 2006)** — KHÔNG phải "tự-định-nghĩa/mới" (đính chính deep-research 2026-06-24), giữ τ-b-thô (total-order) làm điểm sàn.* Kill-test **KZ'** đã rà prior-art (bổ sung **GUI Knowledge Bench arXiv:2510.26098 + TempVS arXiv:2506.10415** — trích-và-phân-định) → GO với khung claim này.
- → Nhờ vậy mâu thuẫn "metric cần gold ↔ dataset không gold" **tan biến**: việc cần gold (thứ tự vàng) đẩy sang AndroidControl, việc không-gold ở lại MobileViews.

### Bù trừ điểm yếu chung
- **CHỐT-TUSOAN — phân biệt "tự soạn câu hỏi" ≠ "sinh dữ liệu tổng hợp":**
  - **"Tự soạn câu hỏi" (luận văn LÀM):** chỉ áp cho **MobileViews / màn-0 / DG1** — vì bộ này không có sẵn câu hỏi use-case. **AndroidControl** (đã có `goal`) và **ScreenSpot** (đã có `instruction`) **KHÔNG cần soạn** — dùng nguyên goal/instruction có sẵn. Nhấn mạnh: tự soạn = **chỉ viết phần INPUT (câu hỏi)** cho ảnh có sẵn; **đáp án để chấm vẫn là dữ liệu THẬT** (VH bbox của MobileViews / gold action của AndroidControl), không tự bịa.
  - **"Sinh dữ liệu tổng hợp" (luận văn TRÁNH):** = bịa ra **ground-truth / đáp án chấm**. Luận văn **không** làm việc này — đó là ranh giới giữ tính hợp lệ của đo đạc.
- Cả ba bộ trục **không có tutorial gold tiếng Việt** → đúng lý do dùng framework **reference-free *theo nghĩa hẹp* (không có tutorial gold do người viết; vẫn có anchor VH-silver)** + tự xây **tập chuyên gia tiếng Việt** (cỡ **chưa cố định ~120** — nên ước lượng theo *ngân sách tuple BWS* ≈1.5N–2N và số hệ thống so sánh rồi mới chốt, đừng hứa cứng 120 với thầy).
- MobileViews label có thể nhiễu → **lọc/validate một subset** trước khi dùng làm anchor "sạch".

---

## Việc bạn làm tuần sau (checklist khi tải về)
1. **MobileViews:** tải 1 shard nhỏ từ HuggingFace (`mllmTeam/MobileViews`); mở 1 cặp `*.jpg`+`*.json`, in cây `viewHierarchy`, **vẽ bbox `[left,top,right,bottom]` lên ảnh** xác nhận khớp. Xem 1 Complete Trace (`states/`+`actions.csv`). *(Ghi rõ đang xem bản v mấy.)* **Sau khi mở shard:** GHI LẠI giá trị `text`/`bounds` của **node con THẬT đầu tiên** để dần dần **thay ví dụ minh hoạ eTax bằng record thật** ở các bản report sau; và **xác nhận convert đúng 3 format toạ độ** (CHỐT-BBOX) — test 1 mẫu cho mỗi bộ (MobileViews pixel / ScreenSpot 0–1 / AndroidControl điểm click).
2. **AndroidControl:** tải 1 phần nhỏ; mở 1 **episode đa bước**, xem gold action mỗi bước (loại thao tác + đích) → dựng thử 1 mẫu Tier A (teacher-forced). **Đo histogram độ dài episode (cổng KN):** tự đếm phân bố số bước/episode (xác nhận mean ~5.5, p5=1, p95=13), đếm số episode còn lại sau khi loại N≤2, vẽ histogram trục N∈[3,~10]. **Thử xáo trộn 1 episode (DG2):** strip metadata + tái mã hoá ảnh + đặt tên UUID → xáo thứ tự → kiểm bằng mắt model không suy được thứ tự từ tên file/EXIF. **Kiểm KB (chống leak step-index):** xác nhận sau khi strip, một detector "mù" xem pixel không xếp tốt hơn ngẫu nhiên. **ScreenSpot-v2:** mở vài mẫu instruction→element, kiểm point-in-bbox của resolver. *(Mind2Web để future-work — chỉ xem nếu mở nhánh web.)*
3. **Trình thầy:** mỗi bộ trục 1 ví dụ record cụ thể + bảng so sánh + **vai cố định 3 bộ (DG1/DG2/đối chứng)** + **đính chính phiên bản MobileViews** (cho thấy bạn đọc kỹ).
4. **Đối chiếu metric:** với 1 cặp MobileViews, tính thử **point-in-bbox** và **HER** bằng tay trên 1 mẫu (nối sang Báo cáo 1).
