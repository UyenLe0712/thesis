# BÁO CÁO 3 — ĐỀ XUẤT PIPELINE

> **Mục đích:** đề xuất pipeline sinh tutorial từ `1 HOẶC N ảnh + câu hỏi`, bám sát ràng buộc & metric của Báo cáo 1–2.
> **Ràng buộc bất biến:** deploy chỉ thấy `ảnh + câu hỏi`; **View Hierarchy (VH) KHÔNG được vào lúc sinh** (chỉ để chấm).

---

> ⚠️ **ĐỌC TRONG KHUNG DESIGN E (chốt 2026-06-25; bản hiện hành dễ hiểu: `00_DOC_TU_DAU` + `14`):** phần "ReOrder-Tutor / 5 bước / OmniParser + Set-of-Mark + ràng-buộc-ID đặt TRƯỚC" mô tả bên dưới là **thiết kế CŨ → nay HẠ xuống 1 bậc ABLATION**. **Pipeline LÕI hiện hành = "lớp trung-thực-hoá":** model **THAY ĐƯỢC** sinh **gọi nút theo TÊN** → **oracle kiểm BÊN CẠNH** (không chặn) → **fallback/sửa**. Đóng góp = **HAI đóng góp NGANG NHAU** (hệ + cách đánh giá). → đọc mô tả dưới như **chi tiết bậc ablation**.

## TÓM TẮT 30 GIÂY

- **Pipeline làm gì:** từ `ảnh màn hình + câu hỏi`, sinh **hướng dẫn từng bước** cho người dùng. Tên hệ chính: **ReOrder-Tutor** (= **SoM-Tutor ⊕ GroundFirst** + thêm **Stage 0 Screen-Ordering** ở đầu). Lõi 5 bước: (1) dò nút từ ảnh → (2) phủ nhãn số (Set-of-Mark) → (3) generator sinh có ràng buộc chỉ được trỏ vào ID đã có → (4) stack xác minh 3 tầng (V1 tồn-tại → V2 intent → V3 self-refine) → (5) đổi ID về toạ độ/nhãn để hiển thị & chấm.
- **INPUT ROUTER — một router quyết hai chế độ:** trước khi vào pipeline, một **router** đếm số ảnh N người dùng đưa vào.
  - **N = 1 → chế độ đơn-bước (DG1):** Stage 0 **rỗng**, đi thẳng vào lõi 5 bước cũ trên **màn-0** (MobileViews). Đúng nguyên vẹn DG1 cũ.
  - **N ≥ 2 → chế độ sắp-thứ-tự (DG2):** N ảnh được đưa vào **XÁO TRỘN** (không theo thứ tự gốc). Pipeline phải (1) **suy ra THỨ TỰ đúng** của các màn ở **Stage 0**, rồi (2) chạy lõi 5 bước **trên chuỗi đã sắp** để sinh hướng dẫn từng bước theo đúng thứ tự đó.
  - **MỘT hệ duy nhất, KHÔNG có pipeline thứ hai** — N=1 chỉ là trường hợp Stage 0 rỗng của cùng một hệ.
- **Chống "bịa" thế nào:** biến grounding tự do thành **trắc nghiệm chọn ID**. Generator chỉ được cite ID nằm trong tập `E` (danh sách element dò từ chính bức ảnh) → hallucination trên màn thấy được trở thành **kiểm tra membership tất định** (V1, không cần LLM, không đụng VH). **Nhấn mạnh — cột lõi chống bịa nằm ở khâu SINH** (constrained generation: ép model chỉ được cite ID∈E ngay lúc decode), **KHÔNG phải ở khâu verify**. Ba tầng verify chỉ là **lưới đỡ phía sau**: V1 = code thuần (kiểm membership, **không phải LLM**); V2 = **một LLM KHÁC** (kiểm đúng-ý/intent); V3 = tự sửa ≤2 lần. Đừng hiểu nhầm "verify bằng LLM khác (V2)" là cơ chế chính. **Vì sao VẪN cần V1 dù sinh đã ép gần 100%:** V1 là **chốt an toàn tất định** cho các tình huống ép-cấu-trúc không phủ hết — trường văn bản tự do trong tutorial, profile/model không bật được constrained decode, hoặc hậu kiểm độc lập để bắt sai sót đường ống.
- **VH chỉ vào lúc chấm**, không bao giờ là input lúc sinh.
- **Trung thực với thầy:** chế độ N-ảnh (DG2) là **bài toán ĐẶT RA ĐỂ ĐO** năng lực suy luận trật tự màn (trả lời đúng câu hỏi của thầy "làm sao model biết trật tự các màn?"), **KHÔNG** khẳng định đây là nhu cầu deploy phổ biến.

```
        người dùng đưa vào N ảnh
                   |
                   v
        +----------------------+
        |  INPUT ROUTER (đếm N) |
        +----------+-----------+
                   |
        N = 1      |      N >= 2
        (đơn bước) |      (sắp-thứ-tự)
                   |
   +---------------+----------------+
   |                                |
   v                                v
 Stage 0 RỖNG               STAGE 0: SCREEN-ORDERING
 (bỏ qua)                   | S0b ordering reasoner ĐỌC ẢNH THÔ (nhánh CHÍNH)
   |                        |     (pairwise+Copeland; listwise = đối chứng fair-compute)
   |                        | S0a per-screen feature (parser M1) = chỉ ABLATION
   |                        | S0c order verifier (code thuần, no-LLM)
   |                        +--------------+--------------------------
   |                          chuỗi màn ĐÃ SẮP (π̂)
   |                                |
   +---------------+----------------+
                   v
        LÕI 5 BƯỚC (SoM-Tutor ⊕ GroundFirst)
        chạy TRÊN TỪNG MÀN theo thứ tự
                   v
        tutorial từng bước + grounding chấm ĐẦY ĐỦ mọi màn
```

> Bản giải thích đời thường (ví dụ eTax xuyên suốt) xem `_archive/03b_pipeline_giai_thich.md`. Kế hoạch chốt cuối xem `05_final_plan.md`. **Bản dễ hiểu hiện hành: `00_DOC_TU_DAU.md`.**

---

> 🟢 **PHÁN QUYẾT KHẢ THI (xem `report/04_feasibility.md`): GO — CÓ THU HẸP.** Luận văn có **HAI đóng góp**:
> **DG1 — lõi màn-0 (screen-0)** trên EN/ZH **MobileViews** (ablation SoM-Tutor vs E2E, chấm grounding/hallucination/clarity bằng VH-silver,
> *không* cần tutorial gold do người viết); **DG2 — SUY LUẬN TRẬT TỰ MÀN (Screen-Order Inference) NẰM TRONG SCOPE** trên **AndroidControl (NeurIPS 2024 D&B)**:
> đưa model **N ảnh XÁO TRỘN** của một luồng đa bước + mục tiêu → model phải (1) **suy ra THỨ TỰ đúng** của các màn, rồi (2) **sinh hướng dẫn từng bước** theo thứ tự đó.
> Metric headline = **Kendall τ-b** (xếp đúng tới đâu), chấm **partial-order-aware** (chỉ phạt cặp BẮT BUỘC); **Tier A** (teacher-forced) vẫn giữ làm **trục tham chiếu chuẩn ngành** (Action-Type / Grounding@14% / Step-SR), KHÔNG còn là "đa bước chính". **ORACLE-ORDER** (N ảnh đã sắp đúng) là **skyline** của trục ordering; **SELF-ORDER** (N ảnh xáo trộn, model tự xếp) là năng lực thật; chênh lệch = **ordering gap**.
> **Đa bước KHÔNG còn là future-work.** Future-work chỉ còn: (1) **chấm định lượng tiếng Việt**, (2) **world-model tự huấn luyện (AGENT-NSI)**,
> (3) **nhánh web Mind2Web**. **Rủi ro tồn vong:** recall detector trên UI mobile **chưa được công bố rõ** (cái công bố là *grounding accuracy* ~57% trên ScreenSpot, KHÔNG phải recall) → mọi số grounding (DG1 *và* DG2) phải đóng khung
> **"có điều kiện recall đã đo"**, không phải "loại bỏ hallucination tất định". Đo recall là **kill-test tuần-1 (K1, cổng cứng)**.
>
> ℹ️ **Lưu ý hợp đồng sản phẩm:** Tier A cho model xem màn thật mỗi bước là **DỤNG CỤ ĐO chuẩn ngành**, *không* vi phạm
> hợp đồng — ràng buộc no-leak (VH/màn thật KHÔNG vào lúc sinh) áp cho **CLAIM VỀ SẢN PHẨM = DG1 + chế độ N-ảnh SELF-ORDER**, còn Tier A là thí nghiệm
> đo tham chiếu có chủ đích. **KHÔNG** tuyên bố "ngang hàng leaderboard" — chỉ đặt trong cùng giao thức để tham chiếu định tính. (Trên trục ordering, **ORACLE-ORDER** mới là skyline/cận-trên.)

---

## 0. KHUYẾN NGHỊ CHỐT (đọc cái này trước)

| Vai trò | Pipeline / Vai dataset | Ghi chú |
|---|---|---|
| ⭐ **Hệ chính** | **SoM-Tutor ⊕ GroundFirst** (hợp nhất) | SoM-Tutor làm xương sống; thêm constrained-decoding + nhánh đa bước của GroundFirst; thêm **intent-critic** từ E2E |
| 🧪 **Baseline bắt buộc** | **E2E-VLM + Self-Refine** **+ NATIVE-GROUNDING** (Qwen2.5-VL tự xuất toạ độ, KHÔNG OmniParser/SoM) | "sàn" + **trả lời thẳng phản biện "đã ground trực tiếp được thì cần detector+SoM làm gì"** (đính chính deep-research 2026-06-24: UGround/OS-Atlas/Qwen2.5-VL ground thẳng tốt hơn SoM-prompting) |
| 📦 **DG1 — màn-0** | **MobileViews** (+ ScreenSpot đối chứng) | ảnh + VH + bbox pixel → chấm grounding/hallucination/clarity bằng **VH-silver** (không cần tutorial gold do người viết) |
| 📦 **DG2 — suy luận trật tự màn** | **AndroidControl** (NeurIPS 2024 D&B) | N ảnh xáo trộn + mục tiêu → model tự xếp (SELF-ORDER) rồi sinh tutorial; headline **Kendall τ-b** (partial-order-aware). **ORACLE-ORDER** = skyline. **Tier A** (teacher-forced) giữ làm trục tham chiếu chuẩn ngành. **Nguồn ngưỡng 14%** = AITW (NeurIPS 2023) |
| 🔭 **Future-work** | **AGENT-NSI** (world-model có train) · **nhánh web Mind2Web** | AGENT-NSI đắt + cần fine-tune + rủi ro rò rỉ cao → chỉ làm nhánh mở rộng đa bước sâu. **Mind2Web là future-work vì thiếu bbox pixel NATIVE (chỉ có DOM) + thuộc nhánh web.** **Đa bước KHÔNG đánh đồng với future-work** — DG2 (SELF-ORDER + ORACLE-ORDER + Tier A) đều in-scope |

> **🔧 KHUNG ĐÓNG GÓP (chốt 2026-06-25 — đổi từ "hệ tham chiếu" sang ĐÓNG GÓP NGANG NHAU):** ReOrder-Tutor **KHÔNG còn là "hệ tham chiếu"** — nó là **đóng góp THỰC SỰ, phải RA KẾT QUẢ TỐT**, song song với đóng góp đánh giá. **Claim mức-CHẮC-THẮNG** (an toàn): giảm bịa & tăng đúng-chỗ so baseline viết-tự-do và so **GPT-4o E2E** về độ-bám-ảnh. **Mức-THƯỞNG** (bonus): thắng GPT-4o toàn diện. **VẪN KHÔNG claim SOTA leaderboard** (setup khác). Bản dễ hiểu: `00_DOC_TU_DAU.md`. *(Hai bullet "HAI đóng góp" dưới đây = cấu trúc DG1/DG2 của NHÁNH ĐÁNH GIÁ.)*

**Câu chuyện luận văn — HAI đóng góp:**
- **DG1 (lõi màn-0):** *"Việc thêm một bộ từ-vựng-đóng Set-of-Mark + verifier tồn-tại tất định có **giảm hallucination & tăng grounding trên màn hình thấy được** so với baseline self-refine thuần ảnh không?"* — một **ablation đo trực tiếp được** trên MobileViews, justify độ phức tạp tăng thêm. Ablation chạy theo **THANG BẬC C0→C4** (C0 trần → **C1 +self-refine = baseline chính** → C2 +Set-of-Mark → C3 +constrained+V1 → C4 +intent V2), KHÔNG phải A/B đơn lẻ. *(LÕI/Gọn CHỈ chạy 3 bậc {C1, C3, C4}; C0 (sàn thô) và C2 (Set-of-Mark một mình) = MỞ RỘNG/ĐỐI CHỨNG, chạy thêm nếu ngân sách cho phép.)* *"reference-free" ở đây hiểu theo **nghĩa hẹp** = KHÔNG có tutorial gold do người viết; VẪN có anchor **VH-silver** (cấu trúc View Hierarchy dùng làm "đáp án bạc" để chấm).*
- **DG2 (suy luận trật tự màn — đóng góp MỚI, độ-MỚI có điều kiện kill-test KZ'):** đưa model **N ảnh XÁO TRỘN** của một luồng đa bước + mục tiêu → model phải (1) **suy ra THỨ TỰ đúng** của các màn, rồi (2) **sinh hướng dẫn từng bước** theo thứ tự đó. Headline = **Kendall τ-b** chấm **partial-order-aware** (chỉ phạt cặp BẮT BUỘC). Đo **ordering gap** = chất-lượng(**ORACLE-ORDER**, N ảnh đã sắp đúng) − chất-lượng(**SELF-ORDER**, N ảnh xáo trộn tự xếp) = "cái giá của việc không biết trật tự". *Cảnh báo floor-effect: ordering gap chỉ có nghĩa nếu metric tutorial NHẠY với thứ tự; nếu không, τ-b là trục chính, gap chỉ phụ.* (Tuyên bố độ MỚI phải qua **kill-test KZ'** = rà prior-art "xếp ảnh/bước xáo trộn"; gần nhất Sort-Story (EMNLP 2016, **dùng Spearman không phải Kendall**) / "Sequencing Multimodal Instructional Manuals" (Wu ACL 2022) / RankGPT (listwise, EMNLP 2023) — và **MỚI + QUAN TRỌNG (deep-research 2026-06-24): GUI Knowledge Bench (arXiv 2510.26098, 10/2025) ĐÃ có task xáo-trộn-plan-thao-tác → hỏi-thứ-tự có điều kiện goal+screenshot** + TempVS (arXiv 2506.10415) xếp ảnh theo mô tả → **PHẢI trích-và-phân-định**. Phần giữ lại để khác biệt: xuất **hoán vị tự do** (không trắc nghiệm) + **N ảnh màn ĐẦY ĐỦ** (không phải text-step + 1 ảnh) + gắn-ordering→sinh-tutorial + τ-b partial-order + audit người. Không trùng khít, nhưng đóng khung độ-mới đúng phần GUI + điều-kiện-hoá-mục-tiêu + gắn-ordering-rồi-sinh + signal-attribution.)

> ℹ️ **Set-of-Mark (SoM):** kỹ thuật phủ **nhãn số** lên từng element UI phát hiện được, biến grounding tự do thành "trắc nghiệm chọn ID".
> **Teacher-forcing:** mỗi bước bộ chấm đưa model **màn thật của đáp án vàng** rồi mới hỏi thao tác kế (model không bị "trượt" theo lỗi của chính nó).
> **SELF-ORDER:** model nhận N ảnh **xáo trộn** → **tự xếp** thứ tự rồi mới sinh tutorial — đây là năng lực thật cần đo.
> **ORACLE-ORDER (skyline):** model nhận N ảnh **đã sắp đúng** + mục tiêu → chỉ phải sinh tutorial, không phải tự xếp — là **cận trên** của trục ordering.
> **ordering gap:** chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER) = "cái giá của việc không biết trật tự". Sanity: ORACLE-ORDER ≥ SELF-ORDER **− ε** ở **mọi episode** (vượt ε = bug).

### Bốn thiết kế đã cân nhắc — vai trò chốt
| Pipeline | Vai trò | Lý do |
|---|---|---|
| **SoM-Tutor** | **Hệ chính** | mạnh nhất cả 3 mặt: khả thi/kỹ thuật, đóng góp khoa học, thực dụng-VN |
| **E2E-VLM + Self-Refine** | **Baseline** | "sàn" tối giản (prompt-only) mà hệ chính phải vượt qua |
| **GroundFirst-Tutor** | **Hợp nhất vào hệ chính** | đóng góp nhánh constrained-decoding + đa bước (đã merge vào SoM-Tutor) |
| **AGENT-NSI** | **Future-work** | world-model tự-train: đắt, cần fine-tune, rủi ro rò rỉ cao |

---

> ✅ **ĐÃ CHỐT DESIGN E (2026-06-25; spec `report/14`, dễ hiểu `report/00_DOC_TU_DAU`):** phần "SoM-Tutor ⊕ ràng-buộc-ID đặt TRƯỚC" mô tả dưới đây **HẠ xuống một bậc ABLATION + công cụ đo recall K1**. **Pipeline LÕI đã chốt = "lớp trung-thực-hoá độc-lập-model":** (1) bộ sinh VLM **THAY ĐƯỢC** (Qwen mở lõi; GPT-5/Gemini-3 đối chứng) sinh **gọi nút theo TÊN** (không ID/pixel); (2) **oracle grounding đặt BÊN CẠNH** (KHÔNG chặn khâu sinh) → chấm + kích fallback; (3) **fallback mô tả bằng lời** khi không khớp (không bỏ bước, không bịa). *Lý do:* detector đặt-TRƯỚC chặn trần tutorial vì recall; oracle BÊN-CẠNH thì recall thấp chỉ hạ độ-tin-phép-đo. Metric thêm **coverage + Followability/Step-SR**. → Đọc mục dưới như **chi tiết bậc ablation**, trong khung design E.

## 1. HỆ CHÍNH ĐỀ XUẤT — "SoM-Tutor ⊕": sinh có ràng buộc trên từ-vựng-đóng từ ảnh

**Triết lý:** biến bài toán grounding tự do thành **trắc nghiệm**: một parser thị giác gắn **nhãn số (Set-of-Mark)** lên mọi element phát hiện từ ảnh → VLM **chỉ được tham chiếu ID đã tồn tại** → hallucination trên màn thấy được trở thành **kiểm tra membership tất định**, không cần LLM-judge, không đụng VH.

> **🔧 ĐÍNH CHÍNH (deep-research 2026-06-24):** SoM **không còn là cách grounding tốt nhất** (UGround ICLR 2025 / OS-Atlas ICLR 2025 / Qwen2.5-VL ground toạ độ trực tiếp tốt hơn SoM-prompting). → giữ SoM nhưng **đóng khung nó là "khung CHỐNG-BỊA / ràng-buộc-cite-ID"**, KHÔNG claim nó là cơ chế grounding mạnh. **Bắt buộc thêm baseline NATIVE-GROUNDING** (Qwen2.5-VL tự xuất toạ độ, không SoM) để đo xem detector+SoM có thực sự đáng công. SoM/OmniParser/Outlines đều là **preprint** → không trình như peer-reviewed.

### Sơ đồ

> *(Các mã M1a/M1b/M1c/M2/V1/V2/V3/M3/Eval trong sơ đồ được giải nghĩa từng mã ở **bảng mã module** ngay dưới mục "Module".)*

```
                 CHỈ INPUT LÚC DEPLOY
        +-----------------+   +------------------+
        | screenshot (img)|   | question (NL, VI)|
        +--------+--------+    +--------+---------+
                 |                      |
                 v                      |
   STAGE 1: VISION PARSER (KHÔNG VH)    |
   |  M1a OmniParser detector -> boxes  |
   |  M1b caption + OCR (VI) -> labels  |
   |  M1c Set-of-Mark overlay (ID 1..N) |
   +-----------------+------------------+
        marked_image + E={id:(bbox,label,interactable?)}
                       |
                       v
   STAGE 2: GENERATOR  M2  (Qwen2.5-VL / GPT-4o, SoM prompt)
   |  constrained: step = (verb, target=[#id]∈E, nl)   |
   |  PROFILE-OPEN: grammar-constrained decode (logit)  |
   |  PROFILE-API : schema + hậu kiểm ID                |
   +-----------------+----------------------------------+
                       | tutorial [{verb,[#id],nl, visible|inferred}]
                       v
   STACK XÁC MINH (3 tầng, theo thứ tự rẻ→đắt)
   | V1  EXISTENCE (tất định, LLM-free): mọi [#id]∈E ?  |
   | V2  INTENT critic (VLM khác / text-only VH-judge): |
   |     "id tồn tại NHƯNG có đúng element cho mục tiêu?"|
   | V3  Self-Refine (bounded K=2, stop-on-no-change)   |
   |     fail -> feedback "ID sai / sai intent" -> regen |
   +-----------------+----------------------------------+
            | bước INFERRED (khi thiếu gold): SelfCheckGPT N=5 (chỉ item đa bước)
            v
   ID->(bbox,label) lookup (tất định) -> tutorial + trace
                       |
        ........ EVAL ONLY (VH không bao giờ quay lại model) ........
        VH MobileViews -> point-in-bbox, HER, coverage, ...
```

### Tái dụng pipeline — MỘT hệ, 2 chế độ qua INPUT ROUTER (KHÔNG có pipeline thứ hai)
> Một **router** đếm số ảnh N rồi định tuyến. Cùng 5 bước SoM-Tutor ⊕ GroundFirst được tái dùng nguyên vẹn; chỉ thêm **Stage 0 Screen-Ordering** ở đầu cho N≥2. Tuyệt đối **không** xây pipeline thứ hai cho đa bước — N=1 chỉ là Stage-0 rỗng.

| Chế độ (router) | Đóng góp | Cách chạy | Màn hình model thấy |
|---|---|---|---|
| **N = 1 → đơn-bước** | DG1 | Stage 0 **rỗng** → chạy lõi 5 bước **1 lần** trên màn-0, sinh tutorial từng bước | chỉ màn-0 (đúng hợp đồng 1-ảnh) |
| **N ≥ 2 → sắp-thứ-tự** | DG2 | **Stage 0** suy ra thứ tự (SELF-ORDER: N ảnh xáo trộn tự xếp; ORACLE-ORDER: đã sắp sẵn) → chạy lõi 5 bước **trên từng màn theo thứ tự** | N màn của luồng (grounding chấm ĐẦY ĐỦ mọi màn) |

- **Tier A (teacher-forced) — trục tham chiếu chuẩn ngành (KHÔNG phải một chế độ router):** ngoài hai chế độ trên, bộ chấm còn chạy một thí nghiệm tham chiếu: ở **mỗi bước** cấp model **màn THẬT của đáp án vàng** rồi hỏi thao tác kế, so gold (Action-Type / Grounding@14% / Step-SR). Đây là **dụng cụ đo**, KHÔNG được trình như năng lực sản phẩm, KHÔNG claim "ngang hàng leaderboard".
- **Khai báo no-leak (bắt buộc):** ràng buộc "VH/màn thật KHÔNG vào lúc sinh" áp cho **CLAIM VỀ SẢN PHẨM = đơn-bước (DG1) + sắp-thứ-tự SELF-ORDER (DG2)**. **Tier A** cố ý cho model xem màn thật để đo tham chiếu chuẩn ngành. Trên trục ordering, **ORACLE-ORDER** là skyline.

#### Ví dụ 2 chế độ — EX-B (đa bước, app Đồng hồ) — *(ví dụ minh hoạ tự soạn — không phải record AndroidControl thật)*

> **Episode mẫu** (3 bước gold, thứ tự đúng π): *B1 màn chính Đồng hồ → bấm tab "Báo thức"; B2 màn Báo thức → bấm "+"; B3 màn đặt giờ → chọn 7:00.* Ở chế độ N≥2, model nhận **3 ảnh XÁO TRỘN** (vd thứ tự B3, B1, B2) + mục tiêu "đặt báo thức 7:00".

| Chế độ | Model nhận gì | Cách chạy | Kết quả mẫu | Đọc số |
|---|---|---|---|---|
| **N=1 — đơn-bước (DG1)** | chỉ màn-0 (màn chính Đồng hồ) | Stage-0 rỗng → lõi 5 bước **1 lần** | "1. Bấm Báo thức" — chấm grounding/format **trên màn-0** | đúng hợp đồng 1-ảnh; chỉ chấm được những gì thấy trên màn-0 |
| **N≥2 — SELF-ORDER (DG2)** | 3 ảnh **xáo trộn** {B3,B1,B2} + mục tiêu | Stage 0 tự xếp → π̂; rồi sinh tutorial theo π̂ + chấm grounding mọi màn | model xếp đúng π̂ = B1→B2→B3 (gating "vào tab Báo thức trước"); **τ-b = 1.0**; tutorial 3 bước grounded | đo năng lực suy luận trật tự thật |
| **N≥2 — ORACLE-ORDER (skyline)** | 3 ảnh **đã sắp đúng** B1→B2→B3 + mục tiêu | bỏ qua tự-xếp, chỉ sinh tutorial | tutorial 3 bước grounded (không tốn công xếp) | cận-trên; **ordering gap** = chất-lượng(đây) − chất-lượng(SELF-ORDER) |

> EX-B làm rõ: **đơn-bước** đo chất lượng tutorial trên màn thấy; **SELF-ORDER** đo năng lực tự xếp trật tự (headline τ-b); **ORACLE-ORDER** cho cận trên để tính **ordering gap** = "cái giá của việc không biết trật tự". Ở đây nếu SELF-ORDER xếp nhầm B2↔B3 (cặp BẮT BUỘC vì drill-down) thì τ-b tụt; còn nếu episode có cặp TỰ-DO (vd điền Email/SĐT) đảo thì **vẫn tính đúng**.

### Ví dụ chạy XUYÊN SUỐT 5 bước — EX-A (màn-0, app eTax) — *(EX-A — ví dụ minh hoạ tự soạn, KHÔNG phải record MobileViews thật)*

> Dùng đúng ví dụ này nhất quán với `_archive/03b_pipeline_giai_thich.md`. **Input:** 1 ảnh màn hình chính eTax + câu hỏi *"Tôi muốn kiểm tra đã nộp thuế chưa thì vào đâu?"*. Theo dõi dữ liệu chảy qua đúng các mã module M1a→M1b→M1c→M2→V1→V2→V3→Eval.

| Bước | Module | Đầu vào | Việc cụ thể | Đầu ra |
|---|---|---|---|---|
| **B1** | M1a+M1b | ảnh eTax | OmniParser dò vùng bấm + OCR/caption chữ Việt | bảng **E** = {①Khai thuế, ②Nộp thuế, ③Tra cứu nghĩa vụ thuế **[bbox 270,820,540,1010]**, ④Thông báo, ⑤Cá nhân} |
| **B2** | M1c | ảnh + E | Set-of-Mark: vẽ số ①..⑤ đè lên ảnh tại đúng vị trí nút | `marked_image` (ảnh có nhãn số) |
| **B3** | M2 | marked_image + E + câu hỏi | generator sinh có ràng buộc, **chỉ được cite ID∈E** | `"1. Bấm ③ (Tra cứu nghĩa vụ thuế)"` |
| **B4** | V1→V2→V3 | tutorial + E | kiểm 3 tầng (xem ví dụ V2 bắt lỗi bên dưới) | tutorial đã xác minh, target = ③ |
| **B5** | Eval | ③ + E | resolver ID→bbox (lookup tất định): ③ → tâm bbox | hướng dẫn cuối + toạ độ click **(405,915)** *(số minh hoạ)* + chữ "Tra cứu nghĩa vụ thuế" |

> Toạ độ (405,915) = tâm của bbox [270,820,540,1010] (trung điểm x = (270+540)/2 = 405; y = (820+1010)/2 = 915). Lúc **chấm**, VH MobileViews cho biết bbox thật của nút "Tra cứu" → kiểm (405,915) có **point-in-bbox** không.

### Ví dụ V2 bắt lỗi — V1 chống bịa-tồn-tại, V2 chống sai-ý *(số minh hoạ — thuộc EX-A tự soạn, không phải record MobileViews thật)*

> Cùng EX-A, giả sử ở B3 generator **chọn nhầm ② "Nộp thuế"** thay vì ③ "Tra cứu nghĩa vụ thuế". Đây là lỗi **đúng định dạng nhưng SAI Ý** — vì câu hỏi là *"kiểm tra đã nộp **chưa**"* (cần tra cứu trạng thái), không phải đi nộp.

| Tầng | Kết quả với output sai `② Nộp thuế` | Vì sao |
|---|---|---|
| **V1** (tồn-tại, tất định, LLM-free) | ✅ **PASS** — ②∈E (nút "Nộp thuế" có thật trên màn) | V1 chỉ kiểm membership; ② tồn tại nên V1 **không bắt được** lỗi này |
| **V2** (intent-critic, model khác đọc lại ảnh) | ❌ **FAIL** — "② tồn tại NHƯNG sai mục tiêu: câu hỏi cần *xem trạng thái đã nộp*, không phải *thực hiện nộp*" | V2 đối chiếu **ý định** câu hỏi với chức năng nút |
| **V3** (self-refine, K≤2) | feedback "sai intent → chọn nút tra cứu trạng thái" → regen → **③ Tra cứu nghĩa vụ thuế** | sửa có chặn, dừng khi sạch |

> **Bài học:** V1 và V2 bắt **hai loại lỗi khác nhau** — V1 chặn cite ID không tồn tại (bịa nút); V2 chặn cite ID có thật nhưng sai chức năng (sai ý). Ship existence-only (chỉ V1) sẽ **lọt** lỗi ② → đây là lý do bắt buộc có V2 (xem §4 mục 5).

### Module (model cụ thể + citation)

> **Bảng mã module (mỗi mã = 1 dòng nghĩa):**
> - `M1a` — **dò vùng tương tác** từ ảnh (OmniParser detector) → ra danh sách bbox.
> - `M1b` — **caption icon + OCR** đọc chữ trên từng vùng (Qwen2.5-VL/Vintern cho tiếng Việt).
> - `M1c` — **phủ nhãn số (Set-of-Mark)** vẽ ①②③… đè lên ảnh.
> - *(ba mã M1\* cùng thuộc **Stage 1 — Vision Parser**, không đụng VH.)*
> - `M2` — **generator sinh tutorial có ràng buộc** chỉ cite ID∈E (**Stage 2**).
> - `V1` — **verifier tồn-tại tất định** (membership ID∈E, không LLM).
> - `V2` — **intent-critic** (model khác hỏi "ID có thật nhưng đúng ý không?").
> - `V3` — **self-refine** sửa lặp có chặn K≤2.
> - *(V1→V2→V3 = **stack xác minh 3 tầng**, rẻ→đắt.)*
> - `M3` — **Stage 0 Screen-Ordering** (S0b ordering reasoner ĐỌC ẢNH THÔ = nhánh CHÍNH, pairwise+Copeland, listwise đối chứng / S0a per-screen feature dùng parser M1 = chỉ ablation, mọi τ-b chạy nhánh này đóng khung "conditioned on recall" / S0c order verifier code thuần).
> - `Eval` — **resolver ID→bbox** lúc chấm (lookup tất định).
> - *Các mã liên tục, không có khoảng trống.*

| Bước | Module | Phương pháp / Model | Citation | Rủi ro rò rỉ VH |
|---|---|---|---|---|
| **M1a** | Phát hiện vùng tương tác | **OmniParser** detector (YOLO-style) | Lu et al. *OmniParser.* arXiv:2408.00203 (Microsoft) | Không (pure-vision). ⚠️ **pin rõ V1 (paper) vs V2 (model card)** |
| **M1b** | Caption icon + OCR | OmniParser caption; OCR **Qwen2.5-VL / Vintern-1B** cho tiếng Việt | Doan et al. *Vintern-1B.* arXiv:2408.12480; Bai et al. *Qwen2.5-VL.* arXiv:2502.13923 | Không (từ pixel) |
| **M1c** | Phủ nhãn số | **Set-of-Mark** (dùng mark từ OmniParser thay SAM) | Yang et al. *Set-of-Mark.* arXiv:2310.11441 | Không |
| **M2** | Sinh tutorial có ràng buộc | **Qwen2.5-VL-7B/72B** (open) / **GPT-4o** (API); constrained decode **Outlines/XGrammar** | **DOMINO** — Beurer-Kellner et al. *Guiding LLMs The Right Way: Fast, Non-Invasive Constrained Generation.* **ICML 2024**, arXiv:2403.06988 | Không (ràng buộc = E từ ảnh) |
| **V1** | Verifier tồn-tại (tất định) | string membership `[#id]∈E`, **không LLM** | — (thuật toán) | Không (so với E, không VH) |
| **V2** | Intent critic | VLM **khác** đọc lại ảnh **hoặc** text-only judge nuốt VH-label *(eval)* | Yin et al. *Woodpecker.* arXiv:2310.16045; Gou et al. *CRITIC.* ICLR 2024 | Không lúc sinh |
| **V3** | Sửa lặp có chặn | **Self-Refine** K≤2, stop-on-no-change | Madaan et al. *Self-Refine.* NeurIPS 2023, arXiv:2303.17651 | Không |
| **M3** | Stage 0 Screen-Ordering (N≥2) | **S0b** ordering reasoner = **nhánh CHÍNH ĐỌC ẢNH THÔ**: **pairwise-then-aggregate** (mỗi cặp hỏi VLM "màn nào trước?" + bắt trích ≥1 ordering cue) tổng hợp bằng **Copeland score**; **listwise** (1 call ép permutation) làm ĐỐI CHỨNG chạy **fair-compute**. **S0a** per-screen feature (parser Stage-1/M1) **chỉ là ABLATION**, mọi τ-b chạy nhánh parser đóng khung **"conditioned on recall"** → **S0c** order verifier (code thuần, không LLM; chu trình mâu thuẫn → min-feedback-arc-set xấp xỉ). Tier A teacher-forced = trục tham chiếu chuẩn ngành. Khi KHÔNG có gold (next-screen VH thiếu ở MobileViews): tag `inferred` + SelfCheckGPT | Li et al. *AndroidControl.* NeurIPS 2024 D&B; Manakul et al. *SelfCheckGPT.* EMNLP 2023 | Stage 0 + sinh KHÔNG xem VH; Tier A (tham chiếu) cố ý xem màn thật |
| | *(ví dụ episode THẬT của AndroidControl — minh hoạ chuỗi gold dùng lúc CHẤM)* | goal `"On cruisedeals, view cruise schedules for a four-night trip from New York to Canada"` → B1 `{action_type: open_app, app_name: CruiseDeals}` → B2 `{action_type: click, x:313, y:742}` → B3 `{action_type: swipe, direction: up}`. **Chuỗi action này là *gold* CHỈ dùng lúc CHẤM** (so với output của model), **KHÔNG bao giờ vào lúc sinh** — giữ nguyên bất biến no-leak | Google Research *android_control* README | gold chỉ ở bước CHẤM |
| **Eval** | ID→bbox resolver | **table lookup** (resolver = lookup tất định, không phải nguồn lỗi) | Cheng et al. *SeeClick.* ACL 2024 | VH chỉ ở bridge offline |

### Xử lý đơn bước vs đa bước
- **Đơn bước (mạnh nhất):** mọi bước cite `[#id]` thật trên màn 0 → chấm đầy đủ point-in-bbox/HER, **resolver = lookup tất định** (không còn là nguồn lỗi). Đây là **lõi vững (DG1)** của luận văn.
- **Đa bước (sắp-thứ-tự) — phân biệt theo "có gold hay không" (KHÔNG vơ đũa cả nắm là unscorable):**
  - **CÓ gold (AndroidControl) → chấm ĐƯỢC đầy đủ:** model nhận N ảnh xáo trộn → **SELF-ORDER** tự xếp rồi sinh tutorial; headline **Kendall τ-b** (partial-order-aware) + **ORACLE-ORDER** làm skyline để tính ordering gap. Vì chạy lõi 5 bước trên TỪNG màn nên **grounding chấm đầy đủ mọi màn** (mạnh hơn cách đoán-mù cũ — không còn bước nào không nhìn thấy). *Tier A* (teacher-forced) giữ làm trục tham chiếu chuẩn ngành (Action-Type / Grounding@14% / Step-SR). Đây là **DG2 in-scope**, KHÔNG phải future-work.
  - **KHÔNG có gold (next-screen VH thiếu ở MobileViews) → mới dùng "unverifiable":** bước sau gắn `[#i1]` + mô tả kỳ vọng, **tag `inferred`**, **không bị tính là hallucination**; báo "unverifiable" + tín hiệu **SelfCheckGPT** (độ bất định, KHÔNG phải sự thật). Cụm "unverifiable / SelfCheckGPT" **chỉ áp cho trường hợp thiếu gold này**, không phải cho mọi đa bước.

> 📌 *Ba lựa chọn triển khai sẽ CHỐT ở pha P2b (xem báo cáo 05): (a) S0b ordering reasoner — pairwise+Copeland (chính) vs listwise (đối chứng fair-compute) chốt cấu hình so sánh; (b) cầu nối output-step (verb,[#id]) ↔ action-space AndroidControl (CLICK/TYPE/SCROLL+toạ độ) cho Tier A; (c) V2-critic đọc ảnh hay đọc text-VH đã serialize.*

### Stack chống hallucination (3 tầng + 1 cho màn suy luận)

> **Đọc đúng trọng tâm trước khi xem danh sách:** cơ chế CHÍNH chống bịa là **(1) ngăn cấu trúc lúc SINH** (constrained generation ép cite ID∈E). Các điểm **(2)(3)(4) chỉ là lưới đỡ phía sau**, không phải cơ chế chính. Trong đó **V1 (điểm 2) KHÔNG phải LLM** — chỉ là kiểm membership tất định bằng code; **V2 (điểm 3) mới là một LLM KHÁC** (intent-critic). Đừng đảo trọng số: "verify bằng LLM khác" là phòng tuyến bổ sung, không thay cho việc ép cấu trúc lúc sinh.

1. **Ngăn cấu trúc** — SoM + constrained decode: không thể cite element không có trong E. *(Đảm bảo ở CẢ hai profile: **open/local** dùng grammar-constrained decode qua logit (Outlines/XGrammar — **XGrammar = MLSys 2025 peer-reviewed; Outlines = preprint**); **API GPT-4o** dùng **OpenAI Structured Outputs** ép enum server-side, đảm bảo 100% — vendor lo, không cần điều khiển logit thủ công. Vì OpenAI giới hạn enum **tối đa 1000 giá trị / 15000 ký tự** (ước tính theo tài liệu tại thời điểm viết), nên dùng **ID số ngắn**.)* **🔧 BẮT BUỘC có giá trị `none/abstain` trong enum (đính chính deep-research):** nếu element ĐÚNG không được detector bắt (recall miss) mà enum ép phải chọn → model **bịa một click sai-nhưng-hợp-lệ** (tương tác trực tiếp với metric hallucination DG1). Phải cho phép `none` + pre-register cách xử khi model abstain.
2. **Phát hiện tất định** — V1 membership, không LLM, không VH → bắt chắc chắn hallucination **tồn-tại** trên màn thấy.
3. **Critic intent** — V2 bắt lỗi **"id có thật nhưng sai element cho mục tiêu"** (lỗ hổng lớn nhất mà V1 không thấy).
4. **Màn suy luận (khi KHÔNG có gold)** — SelfCheckGPT N=5 (chỉ fire trên item đa bước thiếu gold để kiểm soát chi phí).

### Stage 0 Screen-Ordering — định nghĩa & metric trật tự (headline = Kendall τ-b)
> Ở chế độ N≥2, model nhận N ảnh **XÁO TRỘN** + mục tiêu, phải suy ra thứ tự đúng (π̂) rồi sinh tutorial theo π̂. Vì có gold trajectory (AndroidControl) nên trật tự **chấm được**, đây là đóng góp MỚI của luận văn.

**Metric trật tự (well-defined TRƯỚC khi gọi là metric):**
- **HEADLINE = Kendall τ-b** (tiền lệ "dùng τ chấm ordering" = **Lapata 2006**, *Computational Linguistics* 32(4):471–484; nền Kendall 1938; Gao et al. NAACL 2025 ở vai meta-eval — đã có trong `01_metrics` Track B): đo độ tương đồng giữa thứ tự model π̂ và thứ tự gold π. *🔧 τ-b partial-order-aware = **Kendall trên bucket-order/partial-order của Fagin et al. (SIAM JDM 2003 optimistic p=0; 2006)** — KHÔNG phải phát minh mới (đính chính deep-research); giữ τ-b-thô (total-order) làm điểm sàn.* **KHÔNG** dùng pairwise-accuracy thô làm headline (tautology). Phụ: **pairwise-order-accuracy** + **position-accuracy@correct-place**. **Bỏ Exact-Order-Match khỏi headline** (N=3 EM ~17% ngẫu nhiên, N≥6 ~0).
- **Chấm theo thứ-tự-bộ-phận (partial-order-aware) — BẮT BUỘC:** chỉ **PHẠT khi sai cặp BẮT BUỘC** (gating / drill-down: đảo là sai thật); cặp **TỰ-DO** (vd điền Email/SĐT trước-sau đều được) đảo **vẫn tính ĐÚNG**. **HEADLINE τ-b chỉ tính trên CẶP BẮT BUỘC.** Báo THÊM **τ-b-thô** so thứ tự gốc trên toàn tập làm "điểm sàn" (robustness). *Ví dụ:* đăng-nhập-trước-xem-kết-quả → đảo là sai; điền Email/SĐT độc lập → đảo vẫn đúng.
- 🚫 **CHỐNG VÒNG-LẶP-LUẬN (D1 — quan trọng nhất):** nhãn "cặp BẮT BUỘC" để chấm partial-order-aware **TUYỆT ĐỐI KHÔNG được lấy từ bộ phát-hiện cue** (gating/drill-down) mà chính model + signal-attribution sử dụng — nếu lấy sẽ thành **tự chấm** (vòng lặp: model dùng cue X để xếp, rồi lại lấy cue X để định nghĩa "đúng"). Thay vào đó, nhãn cặp bắt buộc **SUY TỪ GOLD TRAJECTORY của AndroidControl bằng QUY TẮC TẤT ĐỊNH:** màn B chỉ xuất hiện **SAU khi thực thi gold action trên màn A** ⇒ cặp (A,B) là **BẮT BUỘC** (phụ thuộc nhân-quả trong chuỗi vàng); cặp không có quan hệ đó = **TỰ-DO**. Quy tắc này thuần code, **không** đọc cue mà model trích.
- **PRE-REGISTER 3 mục cho nhãn cặp bắt buộc:** (i) **tỉ lệ cặp bắt-buộc / tự-do** trên tập đánh giá; (ii) **AUDIT NGƯỜI 50–80 cặp** kiểm quy tắc tất định có khớp đánh giá của người không → báo **% khớp**; (iii) đo **độ NHẠY của headline khi gán nhãn sai 10%** (perturb 10% nhãn cặp, xem τ-b headline đổi bao nhiêu). Làm rõ: gold/VH chỉ dùng ở **khâu CHẤM OFFLINE**, **KHÔNG** phải input của model lúc xếp.
- **Trục N:** loại **N≤2** (N=2 chỉ 1 cặp → τ-b chỉ {−1,+1} vô nghĩa); trục thực tế **N ∈ [3, ~10]** (trần headline N≤6, xem Chi phí). Phải **TỰ ĐẾM histogram độ dài episode** AndroidControl + báo số episode còn lại mỗi mốc N (việc tuần-1, cổng **KN** — khảo sơ bộ: mean ~5.5, percentile-95 = 13 → GO có điều kiện, cần tự đếm chính xác).
- 🔴 **LỌC EPISODE DG2 — BẮT BUỘC (đính chính deep-research 2026-06-24, kiểm trên record THẬT; chi tiết `12_trial_run_runbook.md` §2):** nhiều episode có **các màn gần TRÙNG nhau** → xáo trộn rồi xếp lại là bài **SUY BIẾN** (τ-b nhiễu, không phải năng lực). *Bằng chứng:* `ep1` (sửa tiêu đề Keep Notes, 3 bước) cả 3 màn MAE pixel chỉ **0.5–0.8/255**. → trước khi đo τ-b PHẢI: (1) **loại bước `status` (terminal) + `wait`** khỏi tập màn-cần-xếp; (2) **loại episode "màn gần trùng"** bằng bộ lọc độ-phân-biệt-thị-giác (pre-register ngưỡng; sơ bộ MAE<~6/255 ảnh xám resize = gần trùng) — mở rộng cổng KB "loại 2-ảnh trùng-pixel"; (3) **đếm KN theo "N màn PHÂN BIỆT ĐƯỢC", KHÔNG theo num_steps thô** (N-xếp-được thường < num_steps → N≥5–6 có thể mỏng). **KHÔNG đo τ-b trước khi lọc.**
- **Discrete-N (D5b):** pre-register **≥30 episode mỗi mốc N**; vì đo nhiều mốc N → **hiệu chỉnh đa-kiểm-định Holm-Bonferroni** (hoặc hạ giả thuyết "τ-b biến thiên theo N" (H2) xuống **exploratory** nếu không đủ episode).
- **Chất lượng tutorial từng màn vẫn chấm đầy đủ:** grounding (point-in-bbox, SeeClick ACL 2024), hallucination (HER + coverage), format (IFEval). Mỗi số kèm "recall detector = X% (K1)" + báo **RAW vs ORACLE**.

### Ordering gap — ORACLE-ORDER vs SELF-ORDER
- **ORACLE-ORDER (skyline):** N ảnh **ĐÃ SẮP ĐÚNG** + mục tiêu → chỉ sinh hướng dẫn, không phải tự xếp. Là **cận trên**.
- **SELF-ORDER (thật):** N ảnh **xáo trộn** → model tự xếp rồi mới sinh. Là **năng lực sản phẩm cần đo**.
- **ordering gap = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER) = "cái giá của việc không biết trật tự".**
- **Sanity (sửa theo D2):** ORACLE-ORDER **≥ SELF-ORDER − ε** ở **mọi episode** (KHÔNG phải ≥ tuyệt đối — cho phép dao động nhỏ ε do nhiễu chấm; vượt quá ε = bug). Dùng **cùng matcher freeze + resolver đối xứng** như DG1; báo RAW vs ORACLE cho cả hai.
- ⚠️ **TEST NHẠY-THỨ-TỰ (D2 — pre-register, chống floor-effect):** lấy input **ĐÃ sắp đúng**, **đảo 1 cặp BẮT BUỘC**, đo **DELTA của metric tutorial**. Nếu delta **< ngưỡng tối thiểu** (pre-register) ⇒ metric tutorial **KHÔNG nhạy thứ tự** ⇒ **BỎ ordering gap**, **CHỈ giữ τ-b làm headline** (DG2 **KHÔNG sụp** — τ-b vẫn đo trực tiếp trật tự). Nếu nhạy đủ thì mới bán ordering gap như chỉ số phụ.

### 5 ORDERING CUES — model dựa vào đâu để biết trật tự (trả lời câu hỏi của thầy)
> Đặt tên 5 tín hiệu để trả lời thẳng câu hỏi "làm sao model biết trật tự các màn?". Hai cue đầu (gating, drill-down) cũng chính là căn cứ xác định **cặp BẮT BUỘC** khi chấm partial-order-aware.

1. **gating** — màn cần làm trước mới mở được màn sau (đăng nhập / cấp quyền trước). *(cặp BẮT BUỘC)*
2. **nav-affordance** — nút điều hướng Next / Back / breadcrumb chỉ chiều đi.
3. **state-delta** — trạng thái đổi giữa hai màn (toggle off→on, ô trống→đã điền, badge 0→1).
4. **title-progression** — tiêu đề tiến theo phiếu/luồng (vd "Bước 1/3" → "Bước 2/3").
5. **drill-down** — màn sau = chi tiết của item trên màn trước. *(cặp BẮT BUỘC)*

**Signal-attribution = STRATIFICATION cấp một-cue (KHÔNG che pixel):** chỉ giữ **cặp màn phân biệt được bởi ĐÚNG MỘT cue**, đo accuracy theo từng nhóm cue → biết cue nào giúp model xếp đúng. **KHÔNG che pixel** (che pixel tạo artifact). Kèm **phân tích lỗi mở** (đọc tay các cặp model xếp sai).

> ⚠️ **Caveat cue tự-báo (D5c):** cue do **model tự trích** chỉ là **tín hiệu GIẢI THÍCH YẾU** (model có thể bịa lý do). Kết luận "**cue nào trả công**" phải dựa trên **STRATIFICATION một-cue** (đo accuracy theo nhóm cặp được tách bởi đúng một cue), **KHÔNG** dựa trên lời model tự khai.

**Baseline cho Stage 0 (bắt buộc):**
- **GOAL-ONLY** — che hết ảnh, chỉ đưa mục tiêu + nhãn trong. *Nếu goal-only đã xếp cao → cue giao diện KHÔNG phải nguồn tín hiệu (model đoán theo prior ngôn ngữ).*
- **VISUAL-ONLY (D4 — đối xứng với GOAL-ONLY)** — che **MỤC TIÊU**, chỉ đưa **ảnh**. Hai baseline đối xứng giúp **tách đóng góp ảnh vs goal**: GOAL-ONLY cô lập tín hiệu ngôn ngữ; VISUAL-ONLY cô lập tín hiệu giao diện.
- **RANDOM-ORDER** — xáo ngẫu nhiên làm sàn dưới. **Ngưỡng "vượt RANDOM" (D4):** dùng **phân phối NULL EMPIRICAL theo TỪNG N** (sinh hoán vị ngẫu nhiên rồi đo τ-b để dựng phân phối), **KHÔNG giả định kỳ vọng τ-b random = 0**.
- **Future-work:** AGENT-NSI (world-model có train).

### Ánh xạ sang metric (Báo cáo 1)
- **Grounding §1:** mỗi bước có `(id→bbox)` → point-in-bbox/center-in-bbox/element-match. **Resolver là lookup → khử nguồn lỗi resolver cho màn thấy.**
- **Hallucination §2:** V1 pass/fail = grounded-step-rate; cite vs VH leaf = HER (1−HER). **⚠️ Bắt buộc báo coverage/recall (VALOR-EVAL) song song HER** — vì từ-vựng-đóng *thiên về under-reference*.
- **Format §3:** schema (đánh số + động từ + `[#id]`) → IFEval strict/loose + G-Eval. **Bỏ FKGL cho tiếng Việt.**
- **Trật tự §(DG2):** headline **Kendall τ-b** (partial-order-aware, chỉ trên cặp BẮT BUỘC) + τ-b-thô (điểm sàn) + ordering gap (ORACLE-ORDER − SELF-ORDER). N ∈ [3, ~10] (đường-cong headline N≤6).
- **Task Success §4:** phân theo "có gold hay không":
  - **AndroidControl CÓ gold → Step-SR reference-based HỢP LỆ, in-scope:** Tier A chấm **Action-Type acc / Grounding@14% / Step-SR** chuẩn ngành (ngưỡng **14%** = bán kính chấp nhận tọa độ, trích **BẮT BUỘC** từ AITW NeurIPS 2023). Đây là chấm thật (trục tham chiếu chuẩn ngành), không phải proxy.
  - **MobileViews màn-0 KHÔNG có gold-tutorial:** chỉ chấm grounding/hallucination/clarity bằng VH-silver (DG1); reachability bước cuối vs goal next-screen VH chỉ là proxy bổ sung khi Complete-Traces có.

### Tiếng Việt / Chi phí
- **VN gói gọn ở 2 điểm hoán đổi:** OCR (Qwen2.5-VL/Vintern) + ngôn ngữ Stage-2 (Qwen2.5-VL output tiếng Việt). Detector M1a language-agnostic. ⚠️ **Caption icon của OmniParser là tiếng Anh** → seam EN↔VN, nên chạy caption qua Qwen2.5-VL hoặc thêm lớp chuẩn hoá. Trích "Qwen2.5-VL hỗ trợ tiếng Việt" theo **model card**, không phải tech report.
- **Chi phí:** Stage-1 local nhẹ (~0); Stage-2 1 call/ảnh (GPT-4o ~$0.005–0.02 hoặc Qwen local free); V1 negligible; V3 ×≤2; SelfCheckGPT ×5 chỉ item đa bước. **Không cần fine-tune** cho baseline chạy được.
- **Chi phí Stage-0 (D3 — phải tính vào ngân sách):** S0b pairwise = **C(N,2) call** mỗi episode → mốc CHỐT **N=6 → C(6,2)=15 call**; minh hoạ chi phí tăng theo N: **N=8 → 28 call**, **N=10 → 45 call**; percentile-95 **N=13 → 78 call**. → **CHỐT TRẦN N≤6** cho đường cong headline (báo THÊM tới ~8–10 nếu ngân sách cho phép); chi phí Stage-0 **tính vào ngân sách tổng**.
- **Fair-compute (D3):** so pairwise vs listwise ở **CÙNG TỔNG SỐ LLM-CALL** — listwise chạy self-consistency với **số mẫu = số call pairwise** (C(N,2)) để công bằng tuyệt đối.
- **Phá tie Copeland TẤT ĐỊNH (D3):** khi hai màn đồng điểm Copeland → phá tie bằng **quy tắc tất định** (vd theo chỉ số ảnh tăng dần), **tách khỏi** cơ chế xử lý cặp TỰ-DO (hai việc khác nhau: tie Copeland = kỹ thuật tổng hợp; cặp tự-do = chấm partial-order).

### Ưu / Nhược / Rủi ro (rút gọn)
- **Ưu:** chống hallucination **cấu trúc** trên màn thấy; **không rò rỉ VH** (deploy được); **verifier tất định** rẻ/tái lập; resolver = lookup; VN hoán đổi 2 điểm; mọi component real.
- **Nhược/Rủi ro chí mạng cần xử:** (1) **trần recall của detector** — element bị miss thì không bao giờ cite được, và HER trông đẹp giả tạo; (2) **existence ≠ intent** (cần V2); (3) đa bước (sắp-thứ-tự) **chấm được đầy đủ trên AndroidControl** (τ-b + ORACLE-ORDER + Tier A tham chiếu); chỉ **unscorable khi thiếu gold** (next-screen VH thiếu ở MobileViews); (4) clutter SoM trên UI mobile dày; (5) **chưa có VH tiếng Việt**; (6) **floor-effect ordering gap** nếu metric tutorial không nhạy thứ tự → τ-b là trục chính.

---

## 2. BASELINE BẮT BUỘC — E2E-VLM + Self-Refine

1 VLM mạnh sinh thẳng tutorial từ `ảnh+câu hỏi` → **critic đọc lại CHÍNH ảnh đó** (Woodpecker-style, tín hiệu ngoài = pixel) flag element bịa → refine. Tag visible/inferred; SelfCheckGPT cho màn suy luận.
- **Citation:** Wei et al. *CoT* (NeurIPS 2022); Yin et al. *Woodpecker* (arXiv:2310.16045); Gou et al. *CRITIC* (ICLR 2024); Madaan et al. *Self-Refine* (NeurIPS 2023); Manakul et al. *SelfCheckGPT* (EMNLP 2023).
- **Vai trò:** "sàn" tối giản (prompt-only, không detector, không fine-tune) mà hệ chính phải **vượt qua** → chính là **control của thí nghiệm cốt lõi**.
- **Hạn chế:** lúc sinh là **VLM-judge-VLM** (không có membership cứng); "phòng thủ 2 tầng" thực ra 1 tầng (visible) + heuristic ổn định (inferred). Không hứa mức cải thiện cố định của Self-Refine (con số gốc đo ở task khác, không phải grounding); Reflexion không áp được vì lúc deploy không có reward môi trường.

---

## 3. FUTURE-WORK — AGENT-NSI (world-model màn kế có **TỰ TRAIN**)

> ⚠️ **Phân biệt rõ:** "đa bước" KHÔNG đánh đồng với "future-work". **Đa bước (sắp-thứ-tự: SELF-ORDER + ORACLE-ORDER + Tier A tham chiếu) đã IN-SCOPE** (xem §0, DG2). Chỉ riêng **world-model TỰ HUẤN LUYỆN (AGENT-NSI)** mới là future-work, vì nó cần fine-tune + chi phí + rủi ro rò rỉ.

ReAct planner đi từng bước; khi mở màn mới, **world-model** tưởng tượng element set màn kế (Stage-1 mô tả Δ → Stage-2 element set + confidence), tag mọi bước verifiable/inferred làm **đối tượng hạng nhất**.
- **Vì sao CHỈ phần tự-train này mới là future-work:** **cần fine-tune** world-model trên Complete Traces (đầu tư lớn nhất); **biên rò rỉ cao nhất** (train/serve split phải ép bằng code: M4 deploy chỉ nhận state từ ảnh, không nhận next-state VH); ReAct×N-rollout **đắt nhất** (~15–20 call/tutorial). *(Đa bước KHÔNG-train đã được chấm in-scope ở §0/§1 qua trục τ-b ordering.)*
- **Lấy 1 ý:** giữ ranh giới visible/inferred + **confidence hiệu chỉnh per-step**; chào world-model như nhánh mở rộng "đa bước sâu" với tuyên bố **chỉ "calibrated uncertainty"**, không phải "grounded multi-step accuracy".
- ⚠️ **Citation world-model (rất mới, 2026 — đã xác minh CÓ THẬT, nhưng là PREPRINT → chỉ dùng cho future-work, KHÔNG trình như đã bình duyệt):** MobileDreamer (arXiv:2601.04035, mobile), Computer-Using World Model (arXiv:2602.17365, **desktop — domain mismatch, bỏ cho mobile**). **Phải kiểm provenance** train của MobileDreamer vs MobileViews traces (tránh nhiễm khi dùng làm anchor).

---

## 4. DANH SÁCH "PHẢI LÀM" TRƯỚC KHI BẢO VỆ

> 🔒 **BỐN cổng cứng (D5a): K1 (recall) · KN (histogram độ dài episode) · KZ' (prior-art sắp-ảnh) · KB (chống leak step-index).** Tổng cộng **10 kill-test** (xem `04_feasibility.md`). Vượt cả bốn cổng cứng mới được chốt scope với thầy.

1. **TỰ ĐO trần recall của detector TRƯỚC TIÊN** (OmniParser+OCR vs VH leaf trên subset) — vì **recall trên UI mobile chưa công bố rõ** (cái có là *grounding accuracy* ~57% trên ScreenSpot, không phải recall; giả thuyết làm việc: có thể ~một nửa) → mọi số grounding/HER báo kèm "conditioned on detector recall = X%". Đây là **thí nghiệm đầu tiên** (kill-test **K1**, cổng cứng).
1b. **Rà prior-art sắp-ảnh TRƯỚC khi tuyên bố độ MỚI** (kill-test **KZ'**, cổng cứng ngang K1 — **ĐÃ khảo, GO** với khung claim dưới đây): gần nhất **Sort-Story** (Agrawal et al., EMNLP 2016, xếp ảnh+caption xáo — **dùng SPEARMAN, KHÔNG phải τ**), **"Sequencing Multimodal Instructional Manuals"** (Wu et al., ACL 2022, xếp bước hướng dẫn đa phương thức xáo — nguồn τ-cho-ordering cùng Lapata 2006), **RankGPT** (Sun et al., EMNLP 2023 — là **PHƯƠNG PHÁP listwise** LLM sinh permutation theo query, **KHÔNG phải metric**); cũng tham chiếu sentence-ordering (Gong AAAI 2018), Screen2Vec (CHI 2021). **🔧 BỔ SUNG (deep-research 2026-06-24): GUI Knowledge Bench (arXiv 2510.26098, 10/2025)** — đã xáo plan thao tác → hỏi thứ tự theo goal+screenshot — và **TempVS (arXiv 2506.10415)** xếp ảnh theo mô tả → **PHẢI trích-và-phân-định** (chúng là preprint). **KHÔNG có công trình trùng khít** (chúng dùng trắc-nghiệm/text-step, không phải N-ảnh-màn → hoán-vị-tự-do → sinh tutorial). Đóng khung độ-mới (trung thực): KHÔNG claim "xếp ảnh xáo là mới"; độ mới = (a) domain GUI màn-hình + (b) điều-kiện-hoá theo mục tiêu/use-case + (c) gắn ordering → **SINH** tutorial + (d) **signal-attribution** (ordering cues nào giúp xếp đúng). Phải thừa nhận lineage Sort-Story (Spearman) / Wu ACL 2022 / RankGPT (phương pháp listwise).
1c. **Tự đếm histogram độ dài episode AndroidControl** (kill-test **KN**, cổng): xác nhận đủ episode ở mỗi mốc N ∈ [3, ~10] (đường-cong headline N≤6) để trục N có nghĩa. Khảo sơ bộ: 15,283 episode, mean ~5.5 step, percentile-5 = 1, percentile-95 = 13 (Li et al. NeurIPS 2024 D&B) → **GO có điều kiện**, nhưng **chưa có sẵn số đếm theo từng N → phải TỰ ĐẾM** rồi báo số episode còn lại mỗi mốc N.
1d. **Chống leak step-index khi xáo trộn** (kill-test **KB**, cổng): xáo trộn N ảnh PHẢI **strip metadata + tái mã hoá ảnh + đặt tên file UUID** (không để lộ thứ tự gốc qua tên/EXIF/thứ tự byte). **Khi tái mã hoá CÒN PHẢI (D5d): CHE status bar / đồng hồ / pin / badge** (các chỉ báo này lộ thời gian → lộ thứ tự) **+ LOẠI episode 2-ảnh trùng-pixel** (hai màn gần như giống hệt → cặp vô nghĩa). **CI test:** **detector mù** (= **GOAL-FREE**, chỉ xem pixel, không thấy mục tiêu) KHÔNG được suy ra thứ tự tốt hơn ngẫu nhiên (nếu hơn → có leak, fail CI).
2. **"Đảm bảo cấu trúc" giữ ở CẢ hai profile** — open/local qua logit (Outlines/XGrammar), API qua **OpenAI Structured Outputs** (ép enum server-side, đảm bảo 100%). Dùng ID số ngắn vì OpenAI giới hạn enum **tối đa 1000 giá trị / 15000 ký tự** (ước tính theo tài liệu tại thời điểm viết).
3. **Dùng MODEL KHÁC NHAU** cho generator vs V2-critic vs eval-judge; **judge hallucination = text-only nuốt VH** (cắt shared-error).
4. **Báo COVERAGE/RECALL song song HER**; tách "recall trên E" vs "recall trên VH thật" (cái sau bị chặn bởi detector).
5. **Thêm intent-check (V2)** — đừng ship existence-only; nếu không, "bounded hallucination" chỉ đúng phần tồn-tại.
6. **Đa bước = suy luận trật tự màn trên AndroidControl (CÓ gold):** N ảnh xáo trộn → **SELF-ORDER** tự xếp rồi sinh; headline **Kendall τ-b chấm partial-order-aware** (chỉ phạt cặp BẮT BUỘC gating/drill-down; cặp TỰ-DO đảo vẫn đúng) + báo **τ-b-thô** toàn tập làm điểm sàn. So với **ORACLE-ORDER** (đã sắp đúng) → **ordering gap**; sanity **ORACLE ≥ SELF − ε** mọi episode (D2), và pre-register **test nhạy-thứ-tự** (đảo 1 cặp bắt buộc; delta < ngưỡng ⇒ bỏ gap, chỉ giữ τ-b). Phụ: pairwise-order-accuracy + position-accuracy@correct-place (KHÔNG dùng pairwise-acc thô làm headline; bỏ Exact-Order-Match). **S0b chạy fair-compute pairwise-vs-listwise** (cùng ngân sách call để so công bằng). Baseline **GOAL-ONLY** + **RANDOM-ORDER**. **Tier A** (Action-Type / Grounding@14% / Step-SR, ngưỡng **14% trích BẮT BUỘC từ AITW**) giữ làm **trục tham chiếu chuẩn ngành**, KHÔNG claim ngang leaderboard. Chỉ khi **thiếu gold** (MobileViews) mới rơi về track "unverifiable" + SelfCheckGPT (chỉ là confidence).
7. **Tiếng Việt:** tách "động cơ (eTax/VN)" vs "dữ liệu chấm (EN/ZH)"; tự thu **tập VN nhỏ + panel chuyên gia BWS** (cỡ theo ngân sách tuple ≈1.5N–2N, **không hứa cứng 120**); sửa seam caption EN↔VN; test OCR dấu tiếng Việt ở cỡ font UI; bỏ FKGL. **Phạm vi tự-soạn câu hỏi (CHỐT-TUSOAN):** **CHỈ MobileViews (màn-0 / DG1)** mới cần tự soạn câu hỏi use-case, vì dataset này không kèm sẵn goal/instruction; **AndroidControl và ScreenSpot ĐÃ có sẵn goal/instruction** nên KHÔNG cần (cũng KHÔNG được) tự soạn. Phân biệt rõ: "tự soạn câu hỏi" = chỉ **viết phần INPUT (câu hỏi)** cho ảnh có sẵn, **KHÔNG bịa đáp án chấm** — đáp án (VH bbox / gold action) VẪN là dữ liệu thật của dataset. Đây KHÁC HẲN "sinh dữ liệu tổng hợp" (bịa ra ground-truth) — việc luận văn TRÁNH.
8. **Chặn rò rỉ VH bằng kiến trúc** (data-plane riêng + CI fail nếu chuỗi field VH lọt vào prompt sinh) — coi đây là **một đóng góp**.
9. **Pin phiên bản OmniParser** (V1 paper vs V2 model card); **validate matcher label↔VH** như một nguồn lỗi (audit synonym leakage).
10. **Cap K=2, N=5, short-circuit** khi critic đầu sạch.
11. **Ba dataset CHỐT + AITW phân vai đôi:** **(a) MobileViews** (preprint, ghi rõ v1/v3 khi trích) → màn-0 (DG1); **(b) AndroidControl** (NeurIPS 2024, peer-reviewed) → suy luận trật tự màn / DG2 (SELF-ORDER + ORACLE-ORDER + Tier A tham chiếu); **(c) ScreenSpot(-v2)** (ACL 2024, peer-reviewed) → đối chứng grounding (CHỈ đối chứng đơn-vị point-in-bbox của resolver, KHÔNG đối chứng pipeline tutorial nhiều bước) + bù credibility MobileViews. **AITW (NeurIPS 2023) phân vai đôi:** (i) **nguồn ngưỡng 14% = trích BẮT BUỘC**, (ii) dataset đối chứng = **tùy chọn**. **Mind2Web = future-work nhánh web.** Khung điều kiện recall (mỗi số kèm "recall=X%", cổng K1) áp cho CẢ MobileViews, ScreenSpot VÀ AndroidControl (mọi màn của chuỗi sắp-thứ-tự). **⚠️ Ba bộ dùng BA định dạng toạ độ KHÁC NHAU (CHỐT-BBOX, đã verify record THẬT 2026-06-24 — xem `12_trial_run_runbook.md` §1):** **MobileViews** = bbox **pixel** dạng **`[[l,t],[r,b]]` LỒNG** (có thêm `bound_box`="l,t,r,b"); **🔧 field `width/height` trong VH JSON là RÁC** (mẫu ghi 2340×1080 nhưng ảnh thật 1080×1920) → **lấy kích thước từ chính ẢNH (PIL), KHÔNG đọc field này**. **ScreenSpot** = có sẵn cả **chuẩn hoá 0–1** lẫn **pixel** `[x1,y1,x2,y2]` (⚠️ khác nhau theo mirror HF → pin 1 mirror + assert). **AndroidControl** = **`gold_action` có tiền tố `!FUNCTIONCALL` phải strip**; toạ độ **click `(x,y)` pixel** trong **1080×2400** (`screen_w/screen_h`). → **harness chấm BẮT BUỘC convert về 1 hệ chuẩn + assert range** trước khi so point-in-bbox (nếu không sẽ chấm sai mà KHÔNG báo lỗi).

---

## 5. Citations
OmniParser arXiv:2408.00203 · Set-of-Mark arXiv:2310.11441 · SeeClick ACL 2024 / arXiv:2401.10935 · UGround ICLR 2025 / arXiv:2410.05243 · AndroidControl NeurIPS 2024 D&B · AITW (Android in the Wild) NeurIPS 2023 · ScreenSpot ACL 2024 · OS-Atlas **ICLR 2025 (peer-reviewed)** *(protocol tách Type/Grounding/SR)* · Qwen2.5-VL arXiv:2502.13923 · Vintern-1B arXiv:2408.12480 · CogAgent CVPR 2024 / arXiv:2312.08914 · Self-Refine NeurIPS 2023 / arXiv:2303.17651 · Reflexion NeurIPS 2023 / arXiv:2303.11366 · Woodpecker arXiv:2310.16045 · CRITIC ICLR 2024 / arXiv:2305.11738 · Huang "LLMs Cannot Self-Correct Reasoning Yet" ICLR 2024 / arXiv:2310.01798 · SelfCheckGPT EMNLP 2023 / arXiv:2303.08896 · CoT NeurIPS 2022 / arXiv:2201.11903 · constrained decoding **DOMINO** (Beurer-Kellner et al., *Guiding LLMs The Right Way*, ICML 2024) / arXiv:2403.06988 · VALOR-EVAL arXiv:2404.13874 · MobileDreamer arXiv:2601.04035 *(mới, kiểm provenance)* · Computer-Using World Model arXiv:2602.17365 *(desktop, bỏ cho mobile)*.

> **🔧 CITATION BỔ SUNG (deep-research 2026-06-24):** **Fagin, Kumar, Sivakumar, *Comparing Top-k Lists*, SIAM J. Discrete Math 17(1), 2003** + **Fagin et al., *Comparing Partial Rankings*, SIAM J. Discrete Math 20(3), 2006** *(nguồn chuẩn cho τ-b partial-order/bucket-order — thay claim "tự định nghĩa")* · **Qin et al., *Pairwise Ranking Prompting (PRP)*, Findings of NAACL 2024** + **Copeland (1951)** *(= pairwise+Copeland; bảo vệ bằng bất-biến-thứ-tự-đầu-vào)* · **Zhuang et al., *Setwise*, SIGIR 2024** *(đối chứng chi phí)* · **XGrammar, MLSys 2025** *(peer-reviewed; Outlines/OpenAI Structured Outputs = artifact)* · **Kamoi et al., *When Can LLMs Actually Correct Their Own Mistakes?*, TACL 2024** *(khung phê phán self-correct; V2 model-khác = external feedback nên thoát)* · **GUI Knowledge Bench arXiv:2510.26098 + TempVS arXiv:2506.10415** *(prior-art sắp-thứ-tự GUI/ảnh — trích-và-phân-định)* · **AndroidControl-Curated arXiv:2510.18488** *(phản biện nhãn AndroidControl — ĐỌC trước khi khoá DG2)* · *From Task to Tutorial* (Excel auto-tutorial, FSE Companion 2026) *(tiền lệ rubric+LLM-judge cho Clarity)*.
