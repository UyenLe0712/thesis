# CLAUDE.md — Bối cảnh luận văn (auto-load mỗi phiên)

> ## ⚡ ĐỌC TRƯỚC TIÊN (điều hướng cho mọi phiên chat)
>
> **Nguồn-sự-thật TRẠNG THÁI HIỆN TẠI = `report/00_TONG_HOP_TAT_CA.md`** — đọc file đó ĐẦU TIÊN mỗi phiên. Nó là ảnh chụp gọn toàn bộ (đề tài · model · 2 bài FAIR/VCL · lịch · trạng thái · việc tiếp theo · bản đồ file). File CLAUDE.md này = **nhật ký quyết định + tham chiếu kỹ thuật**, KHÔNG phải trạng thái mới nhất.
>
> **1 dòng trạng thái (2026-07-12):** hướng đã chốt = **"Faithful Distillation"** (train Qwen2.5-VL-3B, SFT-LoRA, chỉ một-màn); 7 vòng debate + audit XONG → **giai đoạn THỰC THI, không research/debate thêm** trước khi có kết quả. **Split 18/12 ĐÃ commit (`3776212`); pre-register `report/56` đã vá 4 lỗ (Fable review — xem `report/58_review_fable_plan_hoan_thanh.md`) + commit.** Việc kế = pilot MDE → ✱ teacher BASE → build. Nộp 2 bài: **FAIR** (15/8, tiếng Anh, model) + **VCL** (30/8, tiếng Việt, sinh-tiếng-Việt).
>
> **Thứ tự đọc khi cần đào sâu:** `report/00` (đầu tiên) → `report/54` (pipeline/model tự-đủ) → `report/KE_HOACH_2_BAI_BAO.md` (2 bài) → `report/53` (khi bắt tay code). Log gốc `report/50/52/55/43` chỉ mở khi tra "vì sao quyết định X".
>
> **Nếu §0 (dưới) mâu thuẫn với `report/00`/`report/54` → hai file report thắng** (mới hơn). Các mục §1–§6 khung prompting cũ đã bị §0 đè — chỉ giữ để tham chiếu kỹ thuật.

> Auto-load khi làm việc trong `D:\Master\Thesis`. Trao đổi với user bằng **tiếng Việt**.
> Nội bộ gọi tắt **DG1 = một màn**, **DG2 = nhiều màn**; nhưng **trong SLIDE/thuyết trình phải nói "một màn / nhiều màn", KHÔNG dùng chữ "DG1/DG2"**.

---

## 0. ⚠️ BƯỚC NGOẶT 2026-07-08 — ĐỌC TRƯỚC TIÊN (đè lên khung cũ §2–§4 khi mâu thuẫn)

> **📍 FILE TỔNG HỢP MỚI NHẤT (2026-07-12): `report/00_TONG_HOP_TAT_CA.md`** — gộp trọn context (đề tài · model · 2 bài FAIR/VCL · lịch/chi phí · trạng thái · việc tiếp theo · bản đồ file) vào 1 file, đọc-đầu-tiên. Các bullet §0 dưới là log quyết định chi tiết theo thời gian; file 00 là ảnh chụp gọn tại 2026-07-12.

- **Thầy BÁC khung hiện tại** vì *"chủ yếu prompting (gpt-4o-mini API + so embedding), chưa thấy MODEL đâu"*. Yêu cầu cứng của thạc sĩ trường: **luận văn PHẢI có một MÔ HÌNH do học viên HUẤN LUYỆN**, không chỉ ghép công cụ qua prompting. Thầy góp ý: pipeline vẽ từng-bước-nhỏ · mỗi bước gắn một model · mục tiêu = tạo ra model.
- **ĐÃ CHỐT hướng (2026-07-09, sau 3 DEBATE + 2 deep-research):** **"FAITHFUL DISTILLATION"** — fine-tune (**SFT-LoRA, KHÔNG RL**) một VLM nhỏ **Qwen2.5-VL-3B** làm bộ **SINH hướng dẫn**, chưng cất từ teacher gpt-4o-mini nhưng **chỉ trên dữ liệu ĐÃ LỌC BỊA** (qua lớp trung-thực-hoá). Đóng góp = **quy trình lọc-faithfulness tạo data + model on-device** (KHÔNG phải "distillation" trần). **Đo bằng %fallback↓/hữu-ích + robust-khi-không-VH** (KHÔNG đo faithfulness-sau-hậu-kiểm vì bão hoà); chống vòng lặp (lọc `nomic` ≠ chấm `bge-m3`+judge+người), held-out theo APP, paired design. Ràng buộc user: **model=đóng góp chính, eval no-gold=chương phụ, <3 tháng, cắt nhiều-màn khỏi train**. → **Kiến trúc đầy đủ + trụ citation: `report/43` CHƯƠNG 0** (đã viết lại 2026-07-09); chi tiết debate + 8 điều kiện: `report/50` §9. **ĐÃ BỊ BÁC (đừng làm lại):** grounding-RLVR (§7), generator-RLVR + classifier (§8). Trụ bình-duyệt: VGA (EMNLP24), KnowAda (NAACL25), BLIP-CapFilt (ICML22), ALLaVA, LLaVA-KD (ICCV25), VLsI (CVPR25), Mind-the-Gap (ICLR25). FEWL = **preprint bổ trợ** (chưa xác nhận venue bình duyệt — verify 2026-07-12, đừng xếp chung hàng "trụ bình-duyệt" ở trên).
- **KHÔNG làm lại từ đầu:** 3 dataset + bộ thước đo no-gold + literature **GIỮ NGUYÊN** (tái dùng để train/đo model). Chỉ đổi **TRỤC trình bày** (pipeline-prompting → train-model). Mục tiêu mới ~ *"Xây dựng mô hình sinh hướng dẫn GUI bám-màn"*.
- **Compute:** user sẽ **mua Colab Pro** (đủ LoRA/QLoRA 3B-7B; KHÔNG đủ train from-scratch lớn).
- **⚠️ 2026-07-09 DEBATE VÒNG 4 (tính-mới) XONG** (`wf_0dda570e-48a`) → **`report/52_debate_tinh_moi_faithful_distillation.md`**: pipeline SỐNG nhưng **KHÔNG được nói "quy trình lọc-faithfulness MỚI"** (đã có STaR/KnowAda/CapFilt/VGA). Tính mới thu hẹp về **2 điểm**: (a) lọc bằng nguồn NGOÀI có cấu trúc (VH, không self-probe) cho hành vi rủi-ro-cao; (b) **TRỤ THỰC NGHIỆM SỐ MỘT = faithfulness khi TẮT VH lúc suy luận** (held-out theo app, có thể null thật — đây là nơi quyết định sống-chết của luận văn, phải pre-register ngưỡng trước pilot). Ablation raw-vs-filtered chỉ là điều-kiện-cần, KHÔNG phải trụ. Phải thêm citation: STaR (Zelikman 2022), FaithDial/BEGIN (Dziri TACL22), WinDOM/Trust-the-Right-Teacher/LiteGUI/CORA (dòng GUI-agent 2026). report/43 Chương 0 đã vá theo hướng này.
- **📌 FILE ĐỌC-HIỂU-TRỌN-PIPELINE — TỰ THÂN ĐẦY ĐỦ, KHÔNG CẦN MỞ FILE KHÁC (2026-07-12):** **`report/54_PIPELINE_FINAL_DOC_HIEU_TOAN_BO.md`** — gộp TOÀN BỘ nội dung từ report/50/52/53/55 vào một file: Phần 1 = giọng người-thường dễ hiểu (bối cảnh, ý tưởng, tính mới, đủ-ngưỡng-thạc-sĩ, rủi ro); Phần 2 = phụ lục kỹ thuật đầy đủ (config YAML, data schema, công thức thống kê, 11 rủi ro kỹ thuật, bảng so sánh precedent, lịch sử quyết định). report/43/50/52/53/55 giữ lại làm log gốc, KHÔNG cần đọc nữa — mọi cập nhật nội dung từ nay ưu tiên sửa thẳng vào report/54. **7 vòng debate coi như ĐỦ** — việc còn lại là THỰC THI (pilot hạ tầng + gặp thầy), không phải research thêm.
- **⚠️ 2026-07-12 AUDIT ĐỘ VỮNG PIPELINE (Fable 5, đối chiếu 64 quyết định + xác minh citation/thống kê qua web):** verdict **CẦN-VÁ → ĐÃ VÁ cùng ngày**. Thiết kế đứng vững (60/64 quyết định khớp nhất quán report/50→54, không bị nghiên cứu 2025-2026 nào scoop), nhưng phát hiện 6 lỗ tài liệu/pre-registration đã vá thẳng vào `report/54` (Phụ lục E chủ yếu) + `report/53` §5.2/§5.6: (1) định nghĩa "đủ lớn" (Δ_train) ở Tier 2 từng mâu thuẫn giữa 2 file — giờ CHỈ CÒN một định nghĩa (đo trên 18 train-apps, cùng điều kiện tắt-VH như Tier 2); (2) Tier 1 giờ có ngưỡng đậu/rớt bằng số (trước chỉ định tính); (3) công thức MDE thêm vế cận-trên thận trọng + phương án dự phòng 15/15; (4) thêm bước dedup perceptual-hash (phòng 2 app khác tên cùng template UI); (5) **UI-R1 = AAAI 2026, KHÔNG PHẢI AAAI 2025** (đã sửa ở dòng trên + report/50) — bài được AAAI chính thức chấp nhận cho kỳ 2026, hội nghị họp 1/2026; (6) khoá thứ tự thực thi (freeze split + commit pre-reg TRƯỚC bất kỳ lệnh gọi API/GPU nào, kể cả pilot). **KHÔNG có lỗi thiết kế nào phải làm lại** — chỉ vá tài liệu, tuần 1 vẫn bắt đầu bằng `dg3_freeze_split.py` như kế hoạch.
- **⚠️ 2026-07-10 DEBATE VÒNG 5 (đủ-ngưỡng-thạc-sĩ + build-plan) XONG** (`wf_a4401c9d-f93`) → **`report/53_ke_hoach_build_model.md`**: verdict **ĐỦ-CÓ-ĐIỀU-KIỆN** (chuẩn thạc sĩ KHÔNG đòi SOTA, chấp nhận đóng góp constructive/technological — Rutgers/Auckland/UIC + Thông tư 23/2021/TT-BGDĐT). **Điều kiện bắt buộc: TÁCH 2 TẦNG thực nghiệm** — Tier 1 (Student-lọc vs Student-RAW, VH vẫn có lúc suy luận, gần chắc dương = lưới an toàn) và Tier 2 (Student vs Teacher-BASE, TẮT VH lúc suy luận = trụ chính, có thể null). Báo cáo ĐỘC LẬP để null ở Tier 2 không kéo sập Tier 1. Kế hoạch build CỤ THỂ (framework LLaMA-Factory, QLoRA r=8/alpha=16 freeze-vision, split app 18/12, exact sign-flip test G=12, ngưỡng đậu/rớt pre-register) đã chốt trong report/53, kèm 11 rủi ro kỹ thuật đã rà + cách né. Việc bắt buộc trước khi chốt với thầy: pilot hạ tầng 5-10 app + nói trước khả năng null Tier 2.
- **Deep-research XONG** (`wf_ed61af89`, verify 20/25 claim) → **`report/50_deepresearch_model_centric.md`** (bản chốt: xếp hạng + khuyến nghị + chi phí). **Trụ bình duyệt neo hướng mới:** UI-R1 (arXiv 2503.21620, chấp nhận **AAAI 2026** — KHÔNG PHẢI AAAI 2025, sửa 2026-07-12; reward point-in-bbox, 136 mẫu) · SE-GUI (NeurIPS 2025) · GUI-Actor (NeurIPS 2025) · ZonUI/Qwen-GUI-3B (WACV 2026, LoRA 3B trên 1 GPU 24GB). Còn lại = preprint (verify ID trước khi trích). **Compute:** Colab Pro+ ~$100–150 cả luận văn (hoặc thuê GPU <$50). **⚠ Cảnh báo:** precedent là agent-bấm-nút CÓ gold → đóng góp model đặt ở grounding/verifier, phần sinh hướng dẫn giữ no-gold. Chi tiết: memory `advisor-pivot-must-train-model`.
- **HỆ QUẢ:** §2–§4 bên dưới (khung "hai đóng góp = hệ thống + đánh giá", pipeline prompting) là **bối cảnh CŨ đang chờ tái khung** — *nội dung kỹ thuật (dataset/metric/citation) vẫn đúng & tái dùng*, nhưng "đóng góp A = hệ thống prompting" sẽ đổi thành **"đóng góp = MÔ HÌNH train được"**. Deck v2 (22 slide) + v3 (chỉ-pipeline) + report/38/43 hiện vẫn theo khung cũ → cập nhật SAU khi chốt hướng. **KHÔNG xoá report cũ** (user định xoá nhưng đã can — phần lớn tái dùng được; nếu dọn thì ARCHIVE, không xoá).

---

## 1. Đề tài (CHỐT)

- **Tên:** Sinh tự động hướng dẫn sử dụng phần mềm bằng LLM, từ ảnh giao diện (UI screenshot) + câu hỏi use-case.
- **Hợp đồng I/O:** vào = **1 ảnh** (một màn) **hoặc N ảnh đã xáo trộn** (nhiều màn, qua input router) + 1 câu hỏi ngôn ngữ tự nhiên → ra = **hướng dẫn từng bước** cho người đọc, bám ngữ cảnh ảnh.
- **Tính chất:** multimodal (ảnh+text→text). **KHÔNG** có dataset hướng dẫn chuẩn do người soạn để làm ground truth → đó là cái khó trung tâm.
- **Bài báo neo khung đánh giá:** Chim, Ive, Liakata — *Evaluating Synthetic Data Generation from User Generated Text* (**Computational Linguistics 51(1):191–233, 2025**, tạp chí, KHÔNG phải "ACL 2025"). Ta KHÔNG kế thừa bài toán sinh (họ text→text), chỉ **kế thừa khung ĐÁNH GIÁ** (Intrinsic + Extrinsic) cho "synthetic text không có đáp án chuẩn".

---

## 2. HAI đóng góp NGANG NHAU (BẤT BIẾN — user rất kiên quyết, ĐỪNG ĐỂ TRÔI)

> **⚠️ CẬP NHẬT 2026-07-08 (§0 đè lên phần này):** thầy yêu cầu luận văn phải TRAIN MODEL thật → khung "đóng góp A = hệ thống prompting" đang được tái khung thành **"đóng góp = MÔ HÌNH train được"**. Đóng góp B (phương pháp đánh giá no-gold) GIỮ, thành *tín hiệu train + cách đo model*. Phần dưới là lý lẽ cũ (vẫn hữu ích để hiểu vì sao A không phải "chỉ engineering"), nhưng **trục chính đã đổi** — xem §0.

- **(A) HỆ THỐNG sinh hướng dẫn bám-sát-màn** = **lớp trung-thực-hoá** (đối chiếu accessibility tree/VH → bước bịa thì viết lại thành **mô tả bằng lời, KHÔNG đoán nút khác**; model-agnostic, triển khai được) **+ khối sắp thứ tự màn** (hỏi cặp → Copeland → phá vòng min-feedback-arc-set, dùng 5 cue).
- **(B) PHƯƠNG PHÁP ĐÁNH GIÁ** không-gold, không-tự-chấm (một màn + nhiều màn).
- **Trục phân định hai nhánh = "CÓ gold trajectory để chấm hay KHÔNG"** (*gold trajectory* = chuỗi thao tác đúng có sẵn trong dataset).
- ⚠️ **KHÔNG hạ A xuống "chỉ engineering".** Đòn "faithfulness by-construction" là **câu hỏi cần thủ**, không phải lý do demote. Cách thủ: (1) faithfulness tăng vì hệ ĐẠT MỤC TIÊU THIẾT KẾ; (2) báo trung thực **tỉ-lệ-bịa-bản-gốc + %fallback** (không khoe 100%); (3) A là research nhờ **đối-chứng-thất-bại đo được** (phương án "đoán nút gần nhất" → lỗi ngầm → chốt "chỉ mô tả"); (4) DG2/Step-SR cho **con số năng-lực-thật**.
- **ĐIỀU KIỆN giữ "ngang nhau": DG2/Step-SR PHẢI ra số dương thật.** Trọng lượng A đến từ **PHÁT HIỆN thực nghiệm** (đo bịa nhiều model + đối-chứng-thất-bại + DG2 sắp-thứ-tự + phân-tích-cue), KHÔNG từ độ phức tạp code.
- Vẫn **KHÔNG claim SOTA leaderboard** (setup khác: sinh hướng dẫn cho người, không phải agent bấm máy). "null vẫn đậu" áp cho nhánh B + phần đo-cơ-chế; claim chắc-thắng của A kỳ vọng DƯƠNG.
- **Tách 2 bài — CHỐT 2026-07-12 (bản 3, sau deep-research venue + trao đổi user): NỘP CẢ HAI mùa này, tách theo DỮ LIỆU/GÓC-NHÌN (không phải một-màn/nhiều-màn nữa vì nhiều-màn chưa kịp build):**
  - **FAIR (nộp TRƯỚC 15/8 · TIẾNG ANH · danh giá) = BÀI MÔ HÌNH flagship** (Faithful Distillation, Qwen2.5-VL-3B, Tier1/Tier2 định lượng trên MobileViews-English). Hợp FAIR (có track VLM). = chở yêu-cầu-train-model của thầy. **KHÓ + GẤP.**
  - **VCL (nộp SAU 30/8 · TIẾNG VIỆT · dễ hơn) = BÀI SINH-TIẾNG-VIỆT** (cho model — train English — sinh hướng dẫn BẰNG TIẾNG VIỆT trên màn MobileViews English có sẵn + đánh giá no-gold; câu hỏi = chuyển-giao Anh→Việt). **KHÔNG cần dataset tiếng Việt** (đã quét MobileViews local 231 file → chỉ 2 màn chữ Việt lẻ, không có app Việt; user không tự chụp được → góc "app Việt" bỏ). Output tiếng Việt + câu hỏi khác → phân biệt FAIR; ⚠ data nguồn dùng chung nên overlap cao hơn, bù bằng output+câu-hỏi khác. **Smoke-test tuần 1:** model sinh tiếng Việt dùng được không → nếu tệ, fallback bài "phương-pháp-đánh-giá thuần" (headline bơm-lỗi). User xác nhận VCL "miễn có chất ngôn ngữ là được" → fit OK.
  - **FALLBACK CỨNG: VCL = sàn chắc, FAIR = stretch.** FAIR 15/8 không kịp → BỎ FAIR giữ VCL, model đi venue sau. Không để FAIR làm hỏng VCL.
  - **Nhiều-màn (Copeland+min-FAS) + learned reranker (tuỳ chọn +~$10/+~5-6 ngày)** = để dành bài tiếng Anh mở rộng sau (FAIR'27/quốc tế), KHÔNG kịp mùa này.
  - **⚠ Rủi ro:** tải nặng (build+2 bài, 1 tiếng Anh, ~7 tuần); salami-slicing (chống bằng khác-data+khác-câu-hỏi+trích-chéo). **CHƯA verify (đừng bịa):** CFP/deadline VCL2026 (30/8 = user nhớ), dual-submission policy 2 venue, index/tỉ-lệ-nhận. **Nguồn venue:** deep-research `wf_ef24768f`. Chi tiết đầy đủ: `report/KE_HOACH_2_BAI_BAO.md` (bản 3, §0 = quyết định + context).

---

## 3. Pipeline (CHỐT — một hệ duy nhất, input router)

> **⚠️ KHUNG CŨ — nội dung kỹ thuật vẫn TÁI DÙNG cho hướng model** (VLM-mù → so-embedding vs VH → viết-lại là chính lớp lọc-bịa của Faithful Distillation). **DG2/nhiều-màn = HOÃN** khỏi mùa này. Bản chốt hiện tại: `report/54`.

**DG1 (một màn) = 3 HỘP:**
1. **VLM sinh MÙ** — chỉ thấy ẢNH + CÂU HỎI, **KHÔNG** thấy danh sách nút → bản BASE. (Câu hỏi cũng không chứa tên nút → model phải tự đọc ảnh, đó mới là chỗ nó bịa.)
2. **THUẬT TOÁN so-embedding** đối chiếu từng tên nút với View Hierarchy → khớp (≥τ) / bịa (<τ). Không phải LLM.
3. Bước bịa → **viết lại thành MÔ TẢ bằng lời** (KHÔNG đoán nút khác, KHÔNG tra VH gán tên). Đây là **PA2** (bỏ hẳn "correction" cũ vì correction sửa-bậy → silent error).

**DG2 (nhiều màn) = KẾ THỪA NGUYÊN DG1 + thêm STAGE-0 ở đầu:** N ảnh xáo → hỏi VLM từng CẶP "màn nào trước?" → **Copeland** (đếm cặp thắng, phá hoà tất định) → phá vòng mâu thuẫn (min-feedback-arc-set; **M2 2026-07-02: trọng số từ margin-Copeland/self-consistency/min-cardinality, KHÔNG dùng confidence VLM tự-khai vì calibrate kém**) → chuỗi đã sắp → chạy pipeline DG1 cho từng màn. **N=1 → Stage-0 rỗng → về DG1.** *(Nền peer-reviewed từng thành phần: `report/39` — pairwise Qin NAACL24 · Copeland Dwork WWW01 · min-FAS Ailon JACM08 · tác vụ Sort-Story EMNLP16 · τ Fagin SIAM06/Lapata CL06 · cue-attribution Gardner EMNLP20 [trụ khái niệm].)*

**LUẬT VÀNG (chống leakage):** VH + đáp án vàng **CHỈ vào lúc CHẤM**, không vào lúc sinh/sắp. Câu hỏi không chứa tên nút. "Chấm baseline" là bước ĐÁNH GIÁ, không phải bước trong hệ deploy (deploy = sinh→kiểm→né bịa).

**5 ORDERING CUES** (trả lời "model dựa vào đâu biết thứ tự"): gating · nav-affordance (Next/Back) · state-delta (toggle, ô trống→điền, badge) · title-progression · drill-down. Signal-attribution = **stratification một-cue** (chỉ giữ cặp phân biệt bởi đúng 1 cue), KHÔNG che pixel, KHÔNG tin lời model tự khai.

---

## 4. Metric + tính hợp lệ (CHỐT)

> **⚠️ KHUNG CŨ — metric/thống kê TÁI DÙNG để đo model** (trung-thực ALOHa · anti-circularity nomic-lọc/bge-m3-chấm · perturbation-validate · cluster-bootstrap). Đã bổ sung cho hướng model: exact **sign-flip G=12** + MDE + Tier1/Tier2. Bản chốt hiện tại: `report/54` Phụ lục E.

**DG1 (so View Hierarchy):**
- **Trung thực** = 1 − bịa/(bước-nhắc-nút) [ALOHa, NAACL 2024]. **Headline = TỈ-LỆ-BỊA BẢN GỐC** (~¼), KHÔNG phải ~100% sau sửa (trần do thiết kế). **(M4 2026-07-02: báo dạng "CÓ ĐIỀU KIỆN recall-VH" — loại nút icon-only/nhãn-chung khỏi mẫu số; ~¼ = quan sát sơ bộ 1 model, KHÔNG làm headline-phát-hiện tổng quát.)**
- **Đúng-nhãn (label fidelity)** = gọi đúng tên hiển thị [**TỰ ĐỊNH NGHĨA — khai thẳng**, khớp-chuỗi ≠ clarity].
- **Đúng-chỗ (grounding, point-in-bbox)** = (x,y) trong khung nút [SeeClick, ACL 2024; ngưỡng dung sai 14% từ AITW, NeurIPS 2023]. ⚠️ **(x,y) phải từ bộ trỏ ĐỘC LẬP kiểu ScreenSpot dự đoán từ tên+ảnh, KHÔNG lấy tâm bbox đã khớp** (nếu lấy tâm → tautology 100%). **(M1 2026-07-02: RA KHỎI headline một-màn — chỉ dùng ở DG2 [có gold-coords] hoặc đối chứng ScreenSpot-v2.)**

**DG2 (so đáp án vàng):**
- **τ thứ-tự-bộ-phận** = (C−D)/|M|, chỉ phạt **cặp bắt buộc** [**ĐÚNG TÊN = Fagin 2006 "Comparing partial rankings" + Lapata CL 2006; KHÔNG phải "Kendall τ-b"**]. Nhãn cặp-bắt-buộc **suy từ GOLD** bằng quy tắc nhân-quả (màn B chỉ hiện sau gold-action ở A), KHÔNG từ model/cue-detector (chống tự-chấm). Cặp tự-do (điền email/sđt) đảo vẫn đúng.
- **Step-SR** (teacher-forced) = bước đúng/bước-gold; bước đúng = đúng loại thao tác VÀ sai lệch ≤14% [AndroidControl, NeurIPS 2024]. Trục tham chiếu chuẩn ngành, KHÔNG claim ngang leaderboard.

**Anti-circularity:** QUYẾT matched/fallback = **nomic** (τA); CHẤM = **bge-m3 ĐỘC LẬP** (họ khác) + LLM-judge nhị phân khác-họ + token-overlap = **3 cơ chế**. (gpt-4o-mini là generator → LLM-judge KHÔNG dùng GPT-family.)

**Validate metric = PERTURBATION tự động** (bơm lỗi đã-biết ĐỘC LẬP matcher, đo detection/false-positive/đơn-điệu) [Sai et al., EMNLP 2021]. Thầy KHÔNG ưa chấm-người → human-correlation = future-work, KHÔNG trong đậu/rớt. Đóng khung "perturbation = độ nhạy = điều kiện cần, chưa phải convergent validity".

**Protocol validate matcher/judge (CHỐT — 6 nguyên tắc GIỜ ĐỀU có TRỤ peer-reviewed; chi tiết `report/27` §7 + `report/22` §7):** (1) matcher đo theo NGỮ NGHĨA + validate vs người 80–120 cặp → báo **P/R + Cohen's κ**, freeze τ [trụ: **ALOHa NAACL 2024**; bổ trợ CHAIR EMNLP 2018]; (2) gán-tay tối thiểu = few-pairwise/HITLC → giảm **~80%** [trụ: **Active Evaluation ACL 2022, Outstanding Paper** — số peer-reviewed là 80%, KHÔNG phải "89%"]; (3) judge KHÁC HỌ generator + neo người, KHÔNG validate judge bằng nhãn-LLM [trụ: **Panickssery NeurIPS 2024** + Zheng NeurIPS 2023]; (4) VH/a11y KHÔNG phải ground truth (>77% app thiếu nhãn) → biện minh hậu-kiểm+fallback [trụ: **Chen ICSE 2020** Distinguished Paper]; (5) validate metric CHÍNH = perturbation [trụ: **Sai EMNLP 2021** + Ribeiro ACL 2020]; (6) bỏ human-correlation làm cổng đậu/rớt [trụ: **Clark ACL-IJCNLP 2021**]. Preprint (Han 2510.09738 quy-trình-2-bước; Liu 2505.19176; Spiliopoulou 2508.06709) **chỉ bổ trợ**; nếu chạy 2-bước thì κ người-người **TỰ ĐO lại** (không mượn 0.801).

**Thống kê:** cluster bootstrap theo **APP** (màn cùng app không độc lập) + CI 95% + Holm (đa-metric) + seed cố định + 10k resample + pre-register ngưỡng TRƯỚC khi nhìn kết quả + ≥30 episode/mốc N.

---

## 5. Dataset (3 bộ, VAI CỐ ĐỊNH) + citation đã verify

| Bộ | Nội dung | Gold? | Vai |
|---|---|---|---|
| **MobileViews** (preprint arXiv, ghi rõ v1/v3 khi trích) | ảnh + VH + bbox | KHÔNG | **một màn / DG1** |
| **AndroidControl** (NeurIPS 2024 D&B, peer-reviewed) | episode nhiều màn + a11y tree + gold action mỗi bước | CÓ | **nhiều màn / DG2 + Step-SR** |
| **ScreenSpot-v2** (OS-Atlas, **ICLR 2025**; gốc SeeClick ACL 2024) | ảnh + bbox chuẩn | — | **đối chứng grounding** + bù credibility MobileViews |

- Cả MobileViews LẪN AndroidControl đều CÓ nguồn phần tử (VH / a11y tree). Bộ chỉ-có-ảnh-trần → cần bộ dò (recall-conditioned, **cổng K1**). Thực tiễn: on-device có a11y tree LIVE qua AccessibilityService (trợ năng).
- **AITW (NeurIPS 2023):** nguồn ngưỡng 14% = **trích bắt buộc**; làm dataset đối chứng = tuỳ chọn. **Mind2Web = future-work** (nhánh web, chỉ có DOM không bbox).
- AndroidControl để đo DG2: **episode bị xáo trộn**, model xếp lại, gold verify. Số đã verify: 15,283 episode/833 app; mean ~5.5 step; p95=13. **Chưa có count theo từng N → phải tự đếm histogram (cổng KN).**
- **Citation khác đã verify:** Chim = CL 51(1) 2025; oracle = Barr TSE 2015. Nguyên tắc: xương sống phương pháp chỉ trích peer-reviewed; preprint (OmniParser/Qwen) chỉ là hiện vật kỹ thuật.
- **DATASET đã verify sâu (2026-07-03, deep-research+debate `wf_6d07419b` → chương chuẩn luận văn `report/44`):** MobileViews = **preprint arXiv 2409.14337** (v3 đổi tên "Million-scale"; **giấy phép MIT**; BUPT+Tsinghua; thu-thập TỰ ĐỘNG bằng bot VLM-DroidBot; **paper 1,2M nhưng bản công khai = 600K**, ta dùng **127 màn/30 app** [`kept_screens_final.json`, mở rộng 2026-07-06; pilot cũ 81/17 lỗi thời]; VH schema trường `class`+`bounds`lồng`[[x1,y1],[x2,y2]]`). AndroidControl = **"On the Effects of Data Scale on UI Control Agents", Li et al. Google DeepMind, NeurIPS 2024 D&B** (arXiv 2406.03679; **CC0**; người-thật Pixel ~1 năm; 8 loại thao tác; **test=1.542 KHÔNG phải 2.855**). ScreenSpot-v2 = **kèm OS-Atlas ICLR 2025** (gốc SeeClick ACL 2024; **apache-2.0**; 1.272 chỉ dẫn = 502 mobile/334 desktop/436 web; sửa 11,32% lỗi nhãn; bbox `[x1,y1,x2,y2]`).
- **⚠ 5 ĐIỀU KIỆN CHỐT TRƯỚC KHI IN (report/44 §8):** (1) không in test "2.855"→dùng 1.542; (2) tính độ-phủ-nhãn VH (`dg1_vh_coverage.py`); (3) hiệu chỉnh khung toạ độ MobileViews (lệch width/height) TRƯỚC khi tính grounding; (4) đối chiếu tác giả OS-Atlas trên OpenReview; (5) KHÔNG khẳng định affiliation Xiaomi.
- **5 cổng cứng:** K1 (đo recall detector) · KN (histogram độ dài episode) · KZ' (prior-art sắp-ảnh — đã GO) · KB (chống leak step-index: strip metadata + tái mã hoá ảnh + che status bar/đồng hồ/pin/badge + loại episode 2-ảnh trùng-pixel) · **K-pair (M2 2026-07-02: đo acc-pairwise THÔ của VLM vs gold TRƯỚC khi tổng hợp Copeland — nếu ~0.5 thì Stage-0 vô hiệu, khai thẳng)**. KN + KZ' đã GO.
- **Prior-art phải thừa nhận** (sắp-ảnh): Sort-Story (EMNLP 2016, dùng Spearman), Wu et al. (ACL 2022), RankGPT (EMNLP 2023, listwise). Độ mới ta = miền GUI + điều-kiện-hoá mục tiêu + gắn ordering→sinh hướng dẫn + partial-order từ gold + signal-attribution. Thêm related-work: VLM-SlideEval (2510.22045), Screen-flow (2503.06067), No Free Labels (2503.05061). **+ Must-cite 2025-2026 (freshness scan `report/42`, đã verify):** FaithScore (Findings EMNLP24, reference-free faithfulness LVLM — ta khác: verify với VH có cấu trúc) · Reliability-without-Validity (2606.19544, hậu thuẫn κ-headline) · LLM-as-Meta-Judge (2603.09403, gần ý-tưởng nhánh B → phải phân định miền GUI) · Ref-free-eval survey (2501.12011) · VECTOR/What-Happens-When (2512.08979, "VLM mù thời gian" → luận cứ DG2+anti-leak) · UI-TARS (2501.12326, phân biệt setup) · GUI-Odyssey (ICCV25)/AMEX/ScreenSpot-Pro (acknowledge landscape).
- **Tiền lệ pipeline-đơn-giản-mà-đậu:** G-Eval / SelfCheckGPT / FActScore / RAGAS / ALOHa / BERTScore.

---

## 6. Trạng thái hiện tại (cập nhật 2026-07-08)

> **⛔ TRẠNG THÁI DƯỚI ĐÂY ĐÃ LỖI THỜI (mốc 2026-07-08, khung prompting).** Trạng thái MỚI NHẤT (2026-07-12) = **`report/00_TONG_HOP_TAT_CA.md` §6**. Giữ phần dưới chỉ để tham chiếu kỹ thuật kết-quả-sơ-bộ; ĐỪNG coi là việc-đang-làm.

**Giai đoạn:** đề cương/thiết kế, có kết quả SƠ BỘ. Đã qua review sâu (3 agent) → phát hiện & VÁ circularity: matcher VỪA sửa VỪA chấm → faithfulness ~100% là tautology. Vá = PA2 (chỉ matched/fallback) + chấm bằng bge-m3 độc lập. Claim DG1 thu hẹp: **DUY NHẤT = "giảm tham-chiếu-nút-không-tồn-tại, giá = %fallback"** (bỏ claim đúng-nhãn; "sửa-đúng" để dành DG2/Step-SR).

**Kết quả sơ bộ (gpt-4o-mini, mẫu nhỏ):** tỉ lệ bịa bản gốc ~¼ số bước; lớp đối chiếu nâng faithfulness ở mọi τ nhưng **CI còn chạm 0 (n nhỏ, 1 app cũ)**; fallback ~19%; label-fidelity & format đứng yên (no-harm). Bản chính (**127 màn/30 app**, `kept_screens_final.json`) **chưa chạy** (cần API).

**Deliverables trình thầy:**
- `report/36` — thuyết minh đầy đủ DG1+DG2 (người mới hiểu, ví dụ số + Q&A giám khảo) — **NGUỒN-SỰ-THẬT phần một-màn** (thay `25` cũ đã archive).
- `report/38` — **BẢN TRÌNH BÀY BẢO VỆ** (văn phong học thuật, bám slide, luận điểm + trích dẫn + phụ lục Q&A).
- `LUAN_VAN_SLIDE.pptx` — **deck v11 = 17 slide** (văn phong học thuật, đủ 3 dataset, nói "một màn/nhiều màn"). Build: `ppt_build/build.js` (pptxgenjs, ảnh thật `_img/`).

**Debate slide 2026-07-01 (5 phản biện→verify→tổng hợp; 19/32 sống): phán quyết nguyên-trạng THẤP–TB, ĐÃ VÁ 4 blocker vào deck v11 + file 38:**
1. Mâu thuẫn ví dụ Confirm/OK → S9 đổi bước-ảo-giác thành "Mở Cài đặt" (nút không tồn tại); Confirm/OK CHỈ giữ ở label-fidelity; thêm quy tắc τ.
2. Thiếu con số → THÊM slide "Kết quả sơ bộ" (nhãn trung thực: mẫu nhỏ/1 model/CI chạm 0/đang chạy 80+ màn) + hạ "ngang nhau" → có điều kiện DG2 dương.
3. Grounding tautology → nêu rõ (x,y) từ bộ trỏ độc lập, không lấy tâm bbox.
4. VH thiếu/nhiễu nhãn → khai độ-phủ-nhãn + loại nút nhãn-chung khỏi mẫu số + giới hạn.
- **CÒN LÀM (free):** tính CON SỐ độ-phủ-nhãn thật từ mv_multiapp; verify venue citation a11y-tree không đầy đủ (Ross et al.) TRƯỚC khi trích.

**Deep-research validate-metric: ✅ XONG.** (2026-07-01) 6 claim U1–U6 verify (5 SUPPORTED+1 PARTIAL, cả 6 preprint→bổ trợ) → `27` §6. **+ (2026-07-02)** tìm+xác minh **TRỤ peer-reviewed cho cả 6 nguyên tắc** (Panickssery NeurIPS24 · ALOHa NAACL24 · Active-Eval ACL22 · Sai EMNLP21 · Chen ICSE20 · Clark ACL-IJCNLP21) → `27` §7; đính chính số HITLC **89%→80%**. Protocol đầy đủ ở §4 trên + `22` §7.

**+ (2026-07-02) nền peer-reviewed pipeline DG2:** cả 6 thành phần Stage-0 đã có trụ bình-duyệt (5 trụ chính-danh + (e) cue-attribution chỉ trụ KHÁI NIỆM Gardner EMNLP20 = chỗ đóng-góp-mới, không phải lỗ hổng) → **`report/39`**. Caveat: quote Copeland (Dwork) cần đối chiếu PDF; Screen-flow 2503.06067 = preprint.

**+ (2026-07-02) DEBATE giám-khảo với PIPELINE (5 phản biện→verify→chủ-tịch, workflow chạy xong 36 đòn/12 sống): PASS-CÓ-ĐIỀU-KIỆN — KHÔNG lỗi thiết kế; rủi ro = tài liệu + chưa-có-số. 5 MAJOR phải vá (chi tiết `report/40` §4):**
  - **M1** rút point-in-bbox KHỎI metric một-màn → dời DG2 (tránh tautology tâm-bbox).
  - **M2** thêm **cổng K-pair** đo acc-pairwise THÔ vs gold (sàn >0.5) TRƯỚC khi tổng hợp; **BỎ "cắt cạnh ít-chắc-nhất"** (VLM calibrate kém) → margin-Copeland/self-consistency/min-cardinality-FAS + ablation phá-vòng.
  - **M3** thống kê: **wild-cluster bootstrap-t (Cameron-Gelbach-Miller 2008)** + báo G≈17 caveat under-coverage; **timestamp pre-reg = `git init` + commit report/22 TRƯỚC khi chạy** (repo hiện non-git!); số hiện = "exploratory".
  - **M4** tính độ-phủ-nhãn VH → tỉ-lệ-bịa dạng khoảng "có điều kiện recall-VH" + loại nút icon-only/nhãn-chung; xoá overclaim file 36 d.99 ("có sẵn khung nút nên rủi ro bị chặn" — mâu thuẫn Chen ICSE20).
  - **M5** đổi "hai ngang nhau" → **"ngang nhau CÓ ĐIỀU KIỆN (chờ DG2 dương)"** ở 36/38/slide; dời trụ chống-"chỉ-engineering" sang 3 chân ĐÃ CÓ (silent-error · tỉ-lệ-bịa-gốc · %fallback).
  - Lá chắn giữ nguyên: luật-vàng chống-leak · đối-chứng-thất-bại đo được · nền peer-reviewed đầy đủ.
  - **ĐÃ ÁP (2026-07-02, chỉ .md — user review + chạy code mai):** M1/M3/M4/M5 vào framing + pre-register (`report/22` §8) + `report/36` (bỏ overclaim "rủi ro bị chặn", grounding ra khỏi một-màn) + CLAUDE §3/§4/§5. Viết sẵn `harness/dg1_vh_coverage.py` (M4 — CHƯA chạy). **CẦN CHẠY CODE (mai):** M4 tính độ-phủ-nhãn, M3 `git init`+commit, M2 cổng K-pair khi prototype DG2. File A-Z người-mới: **`report/41`**.

**+ (2026-07-03) FRESHNESS SCAN 2025-2026 (`report/42`, `wf_3d7cdc91`): KHÔNG lỗi thời, KHÔNG bị scoop.** Không ai ghép "sinh hướng dẫn cho người + no-gold eval GUI". Chỉ cần: (a) **thêm ~8 cite định vị** vào related-work (đã liệt §5); (b) **✱ nên thêm ≥1 generator đời mới** (GPT-4.1 / Gemini-2.5-Flash / Qwen3-VL) cạnh gpt-4o-mini để bảng số không kẹt model cũ — HỎI USER. Bài gần nhất phải PHÂN ĐỊNH: LLM-as-Meta-Judge (2603.09403) [khác: miền GUI + bơm-lỗi-độc-lập-matcher]. Thiết kế lõi VỮNG 2026 (niche VH-structured-check độc nhất; perturbation-validate đang là dòng sống).

**+ (2026-07-03) DEBATE giám-khảo-2026 "pipeline+metric phù hợp 2026?" (`report/42` §6, `wf_73dfaaf9`, 25 đòn/13 sống): PHÙ-HỢP-CẦN-ĐIỀU-CHỈNH.** Không lỗi thời/scoop nhưng bằng-chứng neo 1 model đời-2024 → **3 PHẢI NÂNG (điều kiện đậu 2026):** **M1** (nguy hiểm nhất, 4/13 đòn) đo bịa trên ≥1 **frontier 2025-26 rẻ** (Gemini-2.5-Flash/GPT-4.1-mini) cạnh gpt-4o-mini → báo tỉ-lệ-bịa **đường-cong per-model** không headline "¼" tĩnh (`env VLM_MODEL` sẵn, không sửa code — ✱API); **M2** thêm **baseline listwise một-shot** (RankGPT-style) chấm cùng τ+Step-SR+cột-chi-phí, reframe pairwise = **substrate-audit** (cho stratification 1-cue + intransitivity audit + partial-order-from-gold, trích VECTOR "VLM mù thời gian"); **M3** reframe A: "model-agnostic BY CONSTRUCTION kiểm trên 3 đời model" + đẩy **niche on-device** (a11y-tree live + model nhỏ không gọi được frontier → nối AskEase CHI26), neo "A ngang B" vào DG2/Step-SR + đối-chứng-thất-bại (KHÔNG vào độ-lớn con số bịa). **ĐÒN NGUY HIỂM NHẤT + thủ sẵn:** xem `report/42` §6 (frontier "chữa bệnh sắp tự khỏi" → thủ bằng đường-cong-bịa >0 ở frontier + niche on-device).

**+ (2026-07-06) DEBATE bộ thí nghiệm (3 phản biện: thừa/trùng · clarity · thiếu/cần-thiết): KHÔNG lỗi thiết kế, KHÔNG trùng khoa học — nhưng phình đếm-số + lỗ trình bày. ĐÃ VÁ TRỌN vào `report/43` Ch.13:** tái-khung "15 TN" → **~7 cốt lõi thật** (E1+E2 = một run hai readout; E6 = mục-con validate-B; E9 = cổng; E10–E13 = contingent); thêm **E16** (kiểm-hữu-ích định tính, RQ7) + **arm "nạp VH lúc sinh"** trong E2 (đo leakage nội bộ); định nghĩa **PMR (Def 5.6)** + silent-error-rate + N_eff/wild-cluster/MDE; thêm **bảng mẫu shell** T3/T8 + ánh xạ RQ→E→T/F + ngưỡng đậu/rớt định lượng; inter-annotator κ người-người cho E5. **DATA MỞ RỘNG:** MobileViews **81/17 → 127/30** (`kept_screens_final.json`, khớp cỡ-mục-tiêu pre-reg + m̄≈4,2); ScreenSpot 501 mobile sẵn; AndroidControl **scan 1.600 ep (nguồn `smolagents/android-control` test=3.051; ckg-parsed BỎ vì 52% gap) + chọn 286 ep** (`dg2_sample.py`→`dg2_episodes.json`, KN PASS N∈{4,5,6}; re-scan app từ `goal`+`open_app` → **237 app / 1 unknown** [số cũ 96/169 lỗi thời]). **Chốt mẫu 3 bộ (GỘP, nguồn-sự-thật): `report/48_dataset_selection.md`** (đã xoá `48_chon_mau`). **G=30 một-màn (G_eff-Kish≈24) / G nhiều-màn=237-app (194 singleton) — đã vá mâu thuẫn G≈17 cũ.** **DEBATE item-selection 4-giám-khảo (2026-07-06): HỢP LÝ-CÓ-ĐIỀU-KIỆN; 3 lỗ CAO = MIN_ACT bias + cắt N≥7 + ScreenSpot iOS/demote; estimand=macro-per-app (cấm "đại diện").**

**Đã dọn file (2026-07-01, cập nhật 2026-07-08):** `report/` có **24 file lõi** (bản đồ §10 — đã thêm 44/45/47/48/49); harness dọn script cũ; mọi file cũ ở `report/_archive/` (37 file) + `harness/_archive/` (khôi phục được). **Git hygiene (2026-07-08):** thêm `.gitignore` + gỡ `ppt_build/node_modules` (353 file) & `*.pdf` khỏi git index (vẫn còn trên đĩa).

---

## 7. Môi trường + code harness

- **Máy KHÔNG-GPU** → VLM nhìn-ảnh PHẢI dùng API cloud (`gpt-4o-mini`, key ở `harness/.openai_key` — **KHÔNG in ra**). Ollama local: `nomic-embed-text`, `bge-m3` (chấm độc lập), `llama3.2`, `qwen2.5vl:3b/7b`.
- **⚠️ 2026-07-08: user sẽ MUA Colab Pro** để train/fine-tune model (LoRA/QLoRA 3B-7B) — bù cho việc máy không GPU. Đây là môi trường train chính cho hướng model mới (§0).
- Windows: chạy Python phải `$env:PYTHONIOENCODING="utf-8"`.
- **Dữ liệu:** `dataset_samples/mv_multiapp/` → lọc rác + mở rộng → **127 màn/30 app** (`harness/kept_screens_final.json`, chốt 2026-07-06; pilot cũ 81/17 lỗi thời). ScreenSpot mobile = **501 item** (290 text/211 icon, `screenspot_full/screenspot_mobile_v2.json`). AndroidControl = **đã scan 1.600 ep + chọn 286 ep** (`smolagents/android-control` test; `dg2_sample.py`→`dg2_episodes.json`, 237 app; ảnh tải sau khi chạy). app MobileViews = `screen.split("_")[0]` → cluster-by-app được. **Chốt mẫu chi tiết: `report/48_dataset_selection.md`.**
- **Harness (`harness/`):** `dg1_data.py` (lọc rác), `dg1_run.py` (sinh BASE, PA2, retry-429, resume theo tag), `dg1_pa2_score.py` (derive PA2 + cluster bootstrap + Holm + seed), `dg1_independent_score.py` (chấm bge-m3 + đo silent-error), `dg1_scorer.py` (load VH, point-in-bbox), `aloha_match.py`, `dg1_questions.py`, `dg1_filter_data.py`, `fetch_mobileviews.py`, `_http.py`/`_apikey.py`. *(Đã dọn 2026-07-01: file cũ/superseded chuyển `harness/_archive/` — dg1_score_all [circular, KHÔNG dùng], run_dg1_trial(2), score_v2, effectiveness_ab, generate_cache, trackB, gen_cache/; report cũ ở `report/_archive/`.)*

---

## 8. Việc tiếp theo + nguyên tắc

- **Free (chưa làm):** freeze τA + báo precision/recall matcher (tập gán-tay 80–120 cặp, precision≥0.95); dựng perturbation harness (lỗi bơm độc-lập matcher); module LLM-judge khác-họ; tính con số độ-phủ-nhãn VH. *(Nguồn-trụ peer-reviewed cho protocol validate: ĐÃ XONG — `report/27` §7.)*
- **✱ Tốn API ~$0.05 (HỎI USER TRƯỚC):** sinh câu hỏi affordance-seeded + cổng answerability; sinh BASE 127 màn.
- **Kill-test tuần-1:** K1 (recall) + KN (đếm histogram) + KB (chống leak) → chốt khung với thầy → harness → ablation.
- **NGUYÊN TẮC CHI TIỀN (user nhấn mạnh):** chạy MỘT lần cho đúng; mọi bước ✱ phải HỎI USER TRƯỚC; ưu tiên local/free + cache.

---

## 9. Điểm CHƯA CHỐT

- **Model open/closed:** ~~khuyến nghị bắt đầu VLM API (gpt-4o-mini) làm lõi~~ → **ĐỔI (2026-07-08, §0):** fine-tune model mở (Qwen2.5-VL 3B/7B, LoRA) giờ là **TRUNG TÂM** (không còn tuỳ chọn) vì thầy yêu cầu train model thật; gpt-4o-mini hạ vai thành **teacher để distill**. Hướng train cụ thể chốt sau deep-research (`report/50`).
- **Tiếng Việt:** thầy ưu tiên VN, nhưng dataset chuẩn là EN/ZH → định lượng chạy EN/ZH; VN = demo định tính + ~120 mẫu app VN cho chuyên gia (nói rõ với thầy: KHÔNG có bảng số VN định lượng).
- **Nhánh web (Mind2Web):** future-work.

---

## 10. Bản đồ file `report/` (biết chỗ đào chi tiết)

- **⭐ ĐỌC ĐẦU TIÊN:** `report/00_TONG_HOP_TAT_CA.md` (trạng thái hiện tại) · `report/54_PIPELINE_FINAL_DOC_HIEU_TOAN_BO.md` (pipeline/model tự-đủ) · `report/KE_HOACH_2_BAI_BAO.md` (2 bài FAIR/VCL) · `report/53_ke_hoach_build_model.md` (config/build khi code).

- **Nguồn-sự-thật / tham chiếu:** `05` (final plan — thắng khi mâu thuẫn) · `01` (metrics) · `02` (datasets) · `04` (feasibility + kill-test K1/KN/KZ'/KB) · `12` (runbook chạy thử) · `22` (pre-registration + §7 protocol validate)
- **DG1 lõi:** `36` (nguồn-sự-thật một-màn) · `26` (review 3-agent + đối-chứng-thất-bại correction→silent-error). *(`25` cũ tự-mâu-thuẫn — correction đã bỏ + bảng "100%/80 màn" circular — ĐÃ archive.)*
- **Research / debate:** `27` (deep-research validate-metric — §6 kết quả + §7 trụ peer-reviewed) · `28` (LLM-judge protocol) · `39` (nền peer-reviewed pipeline DG2) · `40` (debate giám-khảo với pipeline — **§4 phán quyết CHÍNH THỨC PASS-có-điều-kiện + 5 fix M1–M5**; §3 interim bù độ phủ) · `42` (freshness scan 2025-2026: KHÔNG lỗi thời/scoop + must-cite)
- **Người mới / thuyết phục:** `41` (giải thích A–Z) · **`43` (HỒ SƠ TOÀN DIỆN — văn phong khoa học, định nghĩa/công thức/mã giả, ví dụ chạy đầu-cuối, thủ-sẵn giám khảo)** · **`44` (CHƯƠNG DỮ LIỆU chuẩn luận văn — 3 bộ verify tận file: nguồn/venue/quy mô/giấy phép/cấu trúc/ví dụ thật/hạn chế + 5 điều kiện chốt)** · `49` (giải đáp thắc mắc theo đợt — Q&A tích luỹ khi đọc 43)
- **Thiết kế TN / dữ liệu:** `45` (verify pipeline progress) · `47` (thiết kế thí nghiệm) · **`48` (CHỐT MẪU 3 bộ — nguồn-sự-thật dataset selection)**
- **Trình bày / nộp:** `30` (abstract VCL) · `36` (thuyết minh đầy đủ) · `38` (bản bảo vệ + Q&A, có PDF font-VN qua `report/md2pdf.py`) · `LUAN_VAN_SLIDE.pptx` (deck v11, build `ppt_build/build.js`) · `LUAN_VAN_SLIDE_v2.pptx` (deck v12 từ 43, build `ppt_build/build_v2.js`)
- **Kế hoạch / sổ:** `KE_HOACH_2_BAI_BAO` · `RESEARCH_LEDGER`. File cũ/superseded ở `report/_archive/` (37 file).
- **⚠️ HƯỚNG MODEL MỚI (§0):** **`report/50_deepresearch_model_centric.md`** — deep-research chọn phương pháp train-model + 3 vòng debate chốt "Faithful Distillation". **`report/52_debate_tinh_moi_faithful_distillation.md`** — debate vòng 4 kiểm tra tính-mới (2026-07-09): CÓ-NHƯNG-CẦN-VÁ. **`report/53_ke_hoach_build_model.md`** — debate vòng 5 (2026-07-10): verdict ĐỦ-CÓ-ĐIỀU-KIỆN + kế hoạch build model đầy đủ (framework/config/data-pipeline/Colab/thống kê), xem §0 trên.
- **Tiện ích:** `report/md2pdf.py` (md→PDF font tiếng Việt DejaVu; `python3 report/md2pdf.py <số|đường-dẫn>`, mặc định 43).

---

## Ghi chú làm việc cho trợ lý
- Trao đổi bằng **tiếng Việt**.
- **Sau mọi thay đổi lớn:** cập nhật file report tương ứng + chạy multi-agent debate để kiểm chất lượng (user thích quy trình này); cập nhật CLAUDE.md khi có quyết định mới.
- Tư vấn model/giá/API Claude/Anthropic: đọc tài liệu, KHÔNG trả lời theo trí nhớ.
- Citation: chỉ trình peer-reviewed như đã bình duyệt; verify venue/năm trước khi trích.
