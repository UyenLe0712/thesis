# 📌 TỔNG HỢP TẤT CẢ — ĐỌC FILE NÀY ĐẦU TIÊN (cập nhật 2026-07-18)

> Một file gộp trọn context: đề tài · mô hình · kế hoạch 2 bài báo · lịch/chi phí · trạng thái · việc tiếp theo.
> Đây là **ảnh chụp tại 2026-07-18**. Chi tiết sâu vẫn ở các file gốc (bản đồ ở §9). Khi mâu thuẫn: `report/54` (pipeline) + `report/KE_HOACH_2_BAI_BAO` (2 bài) + `CLAUDE.md §0` (quyết định) là nguồn-sự-thật.
>
> **⚠️ Đổi so với bản 12/7:** loạt file `60→65` (15-17/7) mới hơn nội dung §6 cũ. Việc-tiếp-theo đã đổi: **K1 (kill-test matcher, free, local) chạy TRƯỚC pilot MDE** — lý do ở `report/65`. Đọc §6 bản mới bên dưới, đừng theo thứ tự cũ.

---

## §0. TÓM TẮT 1 PHÚT

- **Đề tài:** sinh tự động **hướng dẫn sử dụng phần mềm** từ **ảnh giao diện** + câu hỏi, bằng mô hình thị giác–ngôn ngữ. Cái khó: **không có bộ hướng dẫn mẫu** để chấm, và mô hình hay **bịa tên nút không có thật**.
- **Hướng đã chốt:** **"Faithful Distillation"** — huấn luyện (SFT-LoRA) một mô hình nhỏ **Qwen2.5-VL-3B** chạy-trên-máy, chưng cất từ teacher gpt-4o-mini nhưng **chỉ học trên dữ liệu đã lọc bịa** (đối chiếu với View Hierarchy). Đây là **mô hình do học viên tự train** — thoả yêu cầu của thầy.
- **Phạm vi:** **CHỈ một-màn** (nhiều-màn để dành làm sau). Chạy trong <3 tháng, dùng Colab.
- **2 bài báo mùa này:** **FAIR** (15/8, tiếng Anh, bài model) + **VCL** (30/8, tiếng Việt, bài model-sinh-tiếng-Việt).
- **Đang ở đâu (2026-07-18):** split 18/12 đã commit · pre-register đã viết (report/56) · pool train đã fetch+dedup (**498 màn/220 app**, K-leak sạch). Vòng tự-phản-biện 16-17/7 (`report/61→65`) tìm ra **6 nghi ngờ chưa có bằng chứng**, nặng nhất là **matcher có thể hỏng cả hai chiều** — nếu đứt thì "lọc" (đóng góp trung tâm) mất nghĩa. → Kế tiếp = **K1 kill-test matcher (free, local, làm ngay)**, xong mới tới pilot MDE rồi ✱ teacher BASE.

---

## §1. VÌ SAO ĐỔI HƯỚNG (bối cảnh)

Bản đầu của luận văn = *gọi API gpt-4o-mini + so embedding* (prompting thuần). Thầy **bác**: "chủ yếu prompting, chưa thấy MODEL đâu" — quy định thạc sĩ trường bắt buộc phải có **một mô hình do học viên tự huấn luyện**.

→ Giữ nguyên phần lõi (3 dataset, cách đo không-đáp-án-mẫu, literature), chỉ **thêm một mô hình thật** làm trung tâm. gpt-4o-mini hạ vai thành **teacher để chưng cất**. Đã qua **7 vòng debate/kiểm chứng đối kháng** + 1 vòng audit (Fable 5) — không vòng nào tìm ra lỗi phải đập đi làm lại; chỉ vá câu chữ + đo thêm.

**Đã BỊ BÁC (đừng làm lại):** (1) train model "bấm nút" grounding-RLVR; (2) model học-phát-hiện-bịa từ dữ liệu tự chế; (3) học-tăng-cường lấy điểm-trung-thực làm phần thưởng (model lách luật → mô tả mơ hồ mọi lúc).

---

## §2. MÔ HÌNH / PIPELINE MỘT-MÀN (cốt lõi luận văn)

### Ý tưởng: "thầy giáo" và "học trò"
- **Thầy giáo** = gpt-4o-mini: nhìn ảnh + câu hỏi (KHÔNG thấy danh sách nút) → viết hướng dẫn nháp → **~¼ số bước có bịa**.
- **Đối chiếu** từng tên nút với **View Hierarchy** (bản thiết kế màn hình máy-đọc-được) — bằng **thuật toán so khớp**, không phải AI.
- Bước bịa → **viết lại thành mô tả chung chung** bằng khuôn mẫu tất định (KHÔNG đoán nút khác, KHÔNG gọi LLM viết lại).
- Bộ dữ liệu đã lọc sạch → **SFT-LoRA dạy học trò** (Qwen2.5-VL-3B).
- **Lúc dùng thật:** học trò chỉ nhận ảnh + câu hỏi (KHÔNG cần VH, KHÔNG cần internet).

### Câu hỏi trung tâm
Thói quen "né bịa" có **thật sự ngấm vào trọng số** học trò không — hay chỉ là vẻ ngoài phụ thuộc bộ lọc? Trả lời bằng **2 tầng thí nghiệm tách bạch**:

| Tầng | So sánh | Điều kiện | Ý nghĩa |
|---|---|---|---|
| **Tier 1** (lưới an toàn, gần chắc dương) | Student (data lọc) vs Student-RAW (data thô) | VH **vẫn có** lúc suy luận | Chứng minh "có model tự train + việc lọc tạo khác biệt đo được" |
| **Tier 2** (trụ chính, có thể null) | Student vs Teacher-BASE | **TẮT HẲN VH** lúc suy luận, held-out theo app | Thói quen trung thực có nội-tại-hoá không (câu hỏi mới) |

**Báo cáo 2 tầng ĐỘC LẬP** để Tier 2 null không kéo sập Tier 1. Cả 3 kết cục (thắng trọn / thắng một phần / null) viết sẵn diễn giải TRƯỚC khi nhìn số.

### Cấu hình đã chốt (chi tiết: report/53 §3, report/54 Phụ lục C)
- Framework **LLaMA-Factory**; **QLoRA 4-bit** (mặc định, chạy được cả T4 16GB).
- LoRA **r=8, alpha=16**, chỉ vào phần "nói" (decoder); **freeze phần "nhìn"** (ViT).
- Freeze vision vì hành vi cần đo là *nói gì khi không chắc*, không phải *nhìn thấy gì*.
- ~1.500–3.000 mẫu train; lr 1e-4, 3 epoch (ước tính, cần smoke-test xác nhận).
- **Bắt buộc train 2 bản:** Student (data lọc) + Student-RAW (data thô) — để tách "cải thiện nhờ lọc" khỏi "cải thiện nhờ SFT nói chung".

### Đo lường (chi tiết: report/54 Phụ lục E)
- Trung thực = 1 − bịa/(bước-nhắc-nút) [ALOHa NAACL24]. **Chống tự-chấm:** lọc bằng `nomic`, chấm bằng **3 cơ chế khác họ** (bge-m3 + LLM-judge llama3.2 + token-overlap; τB hiệu chuẩn RIÊNG).
- **Kiểm định thước đo = bơm-lỗi tự động** (Sai EMNLP21) — không dùng chấm-người làm cổng đậu/rớt.
- Thống kê: **exact sign-flip test G=12** (liệt kê hết 2^12=4096 tổ hợp dấu) + MDE tính trước + pre-register ngưỡng.

### Tính mới (khi thầy hỏi "khác gì bài khác")
Công thức "sinh→lọc→train lại" KHÔNG mới (STaR/KnowAda/CapFilt/VGA đã có). Tính mới thu về **2 điểm**: (a) lọc bằng **nguồn NGOÀI có cấu trúc** (VH, không self-probe) cho hành vi **rủi ro cao** (bấm nhầm nút thật); (b) **trụ thực nghiệm số 1 = faithfulness khi TẮT VH lúc suy luận** (held-out theo app, có thể null thật).

---

## §3. DỮ LIỆU

| Bộ | Vai | Ghi chú |
|---|---|---|
| **MobileViews** (preprint arXiv, giấy phép MIT) | ảnh + VH → **train + chấm một-màn** | 127 màn/30 app clean (`kept_screens_final.json`) = bộ chấm; **pool train mở rộng đã fetch: 498 màn/220 app** (`mv_train_pool/`, dedup, K-leak sạch) |
| **AndroidControl** (NeurIPS 2024 D&B, CC0) | có gold trajectory → **nhiều-màn (làm sau)** + hiệu chuẩn matcher | test = 1.542 (KHÔNG in "2.855") |
| **ScreenSpot-v2** (OS-Atlas ICLR 2025) | đối chứng grounding | 501 mobile |

- **KHÔNG có dataset GUI tiếng Việt** (đã quét MobileViews local 231 file → chỉ 2 màn có chữ Việt lẻ, không phải app Việt). Ảnh hưởng bài VCL — xem §4.
- **Split đã khoá:** 30 app clean → **18 train / 12 test** theo app (`train_eval_app_split.json`, seed=20260710). Pool mở rộng điền sau khi fetch (disjoint tuyệt đối với 12 test).

---

## §4. KẾ HOẠCH 2 BÀI BÁO (chốt phiên này — chi tiết: report/KE_HOACH_2_BAI_BAO bản 3)

**Mục tiêu:** nộp **CẢ HAI** hội nghị → nhiều công bố = dễ ra tốt nghiệp. Không nộp trùng 1 bài 2 nơi → tách theo **ngôn ngữ output + trọng tâm**.

| | **FAIR** | **VCL** |
|---|---|---|
| Deadline | **15/8/2026** (mốc đầu, hay gia hạn) | **~30/8/2026** (⚠ user nhớ, chưa verify) |
| Ngôn ngữ | **tiếng Anh** (venue chỉ nhận Anh) | tiếng Việt |
| Độ khó | khó gấp ~2, danh giá hơn | dễ hơn |
| Venue | NC Cơ bản & Ứng dụng CNTT (lần 19, RỘNG, có track VLM) | Ngôn ngữ học Tính toán (HUFLIT, thuần NLP) |
| **Bài** | **MÔ HÌNH** (flagship): Faithful Distillation, Tier1/Tier2 trên MobileViews English | **SINH-TIẾNG-VIỆT**: cho model (train English) sinh hướng dẫn **bằng tiếng Việt** trên màn English có sẵn + đánh giá no-gold; câu hỏi = **chuyển-giao Anh→Việt** |
| Dữ liệu | MobileViews English | MobileViews English (dùng chung) — **output khác ngôn ngữ** |
| Vai | **stretch** (khó, gấp) | **sàn CHẮC** |

**Chống trùng/salami:** khác ngôn ngữ output + khác câu hỏi + trích chéo. ⚠ Data nguồn dùng chung → overlap cao hơn → phải tách headline mạnh + **đọc chính sách dual-submission 2 venue trước khi nộp**.

**Fallback cứng:** nếu FAIR 15/8 không kịp → **bỏ FAIR, giữ VCL** (sàn chắc), model đi venue quốc tế sau. **Không để canh bạc FAIR làm hỏng VCL.**

**Smoke-test tuần 1 quyết hướng VCL:** model sinh tiếng Việt dùng được không? Được → làm bài "sinh tiếng Việt". Tệ → fallback bài **phương-pháp-đánh-giá thuần** (headline = bơm-lỗi). Kiểu nào VCL cũng sống.

**Nhiều-màn + bộ sắp-thứ-tự học-được (+~$10, +~5-6 ngày)** = để dành **bài tiếng Anh quốc tế sau**, ngoài đường-găng mùa này.

---

## §5. LỊCH · CÔNG SỨC · CHI PHÍ

**Công sức (10h/ngày, chi tiết report/53 §4.4):**
- Model một-màn (data + train + eval): **~10–15 ngày lý tưởng / ~14–21 ngày thực tế**.
- Bộ sắp-thứ-tự nhiều-màn (nếu làm): +~5–6 ngày.
- Viết 1 bài (có AI hỗ trợ, không cần thầy review): **~3–5 ngày**.

### Bảng mốc — tick khi qua gate
*(rút từ `report/_archive/58` Phần B, rebase 18/7. Ký hiệu: ✱ = tốn tiền, HỎI USER trước · [GATE] = điểm quyết định.)*

| Mốc | Hạn gốc | Hạn rebase | Điều kiện qua | ✔ |
|---|---|---|---|---|
| **M0** Prereg `56` + commit | 12/7 | — | commit `2c84ce8` | ✅ |
| **M0c** K1/K2 đạt cổng ★mới | — | 20/7 | bỏ-lọt ≤20%, kết-oan ≤10% | ☐ |
| **M1** MDE điền + khoá ngưỡng (commit 2) | ~16/7 | ~22/7 | [GATE-1] | ☐ **trượt** |
| **M2** Data SFT ×2 sạch + smoke-train OK | 19/7 | ~25/7 | [GATE-1b] | ☐ |
| **M3** 2 checkpoint hội tụ + gate tiếng Việt | 26/7 | ~30/7 | [GATE-2]+[GATE-3] | ☐ |
| **M4** Bảng số Tier1/2 + perturbation | 5/8 | **5/8 giữ nguyên** | [GATE-3b] | ☐ |
| **M5** Draft FAIR → gửi thầy | 10/8 | 10/8 | — | ☐ |
| **M6** Nộp FAIR | 13–14/8 | 13–14/8 | [GATE-4] (8/8) | ☐ |
| **M7** Nộp VCL | 27–28/8 | 27–28/8 | — | ☐ |
| **M8** Luận văn chính (quyển) | sau 30/8 | — | deadline trường | ☐ |

> **Đã trượt ~6 ngày** (M1 hạn 16/7, nay 18/7 chưa chạy pilot). Phần trượt ăn vào buffer tuần 1–2; **M4 5/8 KHÔNG lùi** vì đó là gate sống-chết của FAIR. Mỗi tuần chừa ~1 ngày không gán task; việc tràn ăn vào ngày đó TRƯỚC khi ăn vào gate.

### Việc theo tuần (rút gọn — bản đầy đủ ở `report/_archive/58` Phần B)

- **18–20/7 — kill-test free, chạy trước mọi thứ tốn tiền:** **K1** matcher hai chiều + **K2** đếm phân loại bịa (`report/65`). Gộp luôn **T1.6 hiệu chuẩn τA** bằng AndroidControl (~100–120 step ngoài eval, precision ≥0.95) — cùng họ việc, cùng free. Rớt cổng → nâng trọng tài TRƯỚC khi build data (rẻ), đừng đi tiếp.
- **~20–25/7 — data + MDE + smoke-train sớm:** ✱ pilot MDE (~$0.1, 4–5 **train**-app, KHÔNG đụng 12 test) → điền `[MDE]` → **commit lần 2**. **[GATE-1]** MDE ≤15–20pp → giữ split 18/12; vượt → re-split 15/15 + chạy lại K-leak + commit lại prereg. Rồi ✱ teacher BASE full (~$1–2, đo `DG1_LIMIT=30` trước; pool-220 chạy song song được vì bất biến với re-split) → matcher + rewrite → `sft_train.json` + `sft_raw.json`. Song song: ✱ smoke-train 20 mẫu trên Colab để de-risk LLaMA-Factory (**[GATE-1b]**) — đừng chờ data mới.
- **~25/7–2/8 — train nền + dồn việc không cần checkpoint:** train Student + Student-RAW qua đêm; test **GGUF export ngay checkpoint đầu** (fail → safetensors + infer Colab); hiệu chuẩn **τB** bge-m3 (80–120 cặp, freeze); dựng perturbation harness; **viết trước Intro/Related/Method của FAIR**. **[GATE-2]** re-test tiếng Việt trên checkpoint — drift → trộn 5–10% target Việt + retrain (ghi amendment TRƯỚC) hoặc chốt VCL = bài phương-pháp. **Gặp thầy** trong tuần này.
- **2–5/8 — chỉ inference + chấm + thống kê:** infer trên 12 test-app **và** 18 train-app (cho Δ_train); chấm 3 cơ chế + %fallback + silent-error; sign-flip exact Tier1/Tier2 + Holm + đối chiếu 3-kết-cục prereg.
- **5–15/8 — điền Results + polish FAIR.** **[GATE-3b, 5/8]** bảng số chính đã đủ trong draft → đi tiếp; **chưa đủ → BỎ FAIR**, dồn VCL + luận văn. **[GATE-4, 8/8]** nhị phân: đủ số thì nộp dù văn chưa đẹp; thiếu số thì bỏ. **KHÔNG lập kế hoạch dựa trên gia hạn.**
- **16–30/8 — VCL:** Student sinh tiếng Việt trên 12 test-app → chấm no-gold (tên nút English trong câu Việt vẫn so VH) + so arm English + taxonomy lỗi → viết → nộp **27–28/8** (buffer vì 30/8 chưa verify). *FAIR bị bỏ ở gate nào → thời gian dôi chuyển thẳng sang viết chương luận văn, KHÔNG nghỉ.*
- **Sau 30/8 — quyển luận văn** ~8–15 ngày bằng tái chế: FAIR = chương Mô hình + Thực nghiệm · VCL = chương ứng dụng tiếng Việt · `report/54` = chương phương pháp.

**Đường-găng:** M0✅→K1/τA→MDE/[GATE-1]→teacher→SFT data→smoke-train→train→eval→[GATE-3b 5/8]→Results→FAIR. **VCL nằm ngoài đường-găng** (trừ khi GATE-2 rẽ retrain).

**Chi phí:** ~$70–100 tổng — ① pilot MDE ~$0.1 · ② teacher full ~$1–2 · ③ Colab Pro $10 · ④ Colab Pro+ $50 · ⑤ dự phòng inference ~$0–5 · ⑥ sinh câu hỏi qua API nếu CPU chậm ~$1 · ⑦ target Việt nếu GATE-2 rẽ ~$0.5. Bộ nhiều-màn (nếu làm sau) thêm ~$10.

---

## §6. TRẠNG THÁI HIỆN TẠI (2026-07-18)

✅ **Đã xong:**
- **Vòng tự-phản-biện 16-17/7** (`report/61`→`65`): deep-research đã verify đối kháng (`61`, dễ hiểu ở `62`) → plan nâng cấp chia nhỏ (`63`) → thiết kế-lại-từ-trang-trắng để đối chiếu (`64`) → **`65` = 6 nghi ngờ + plan kiểm chứng K/D/R**. Kết luận: **xương sống đứng vững, đi tiếp** — nhưng chỉ sau khi K1/K2 cho số đẹp. **Chưa đổi gì trong pre-reg `56`.**
- Audit độ vững pipeline (Fable 5) → 6 lỗ tài liệu đã vá (report/54/53, UI-R1→AAAI2026, FEWL→preprint).
- Deep-research venue → định danh FAIR/VCL + chốt trục 2 bài.
- Quét dataset tiếng Việt → xác nhận không có → chốt hướng VCL "sinh tiếng Việt".
- **Bước 1: khoá split 18/12 app** — `dg3_freeze_split.py` + `train_eval_app_split.json` — **đã git commit** (`3776212`).
- **Bước 2a: pre-register** — `report/56_PREREG_MODEL.md` viết xong (ngưỡng Tier1/Tier2, MDE để trống điền sau pilot). *(user commit.)*
- **Bước 4 (một phần): mở rộng pool train** — fetch 2 shard mới → dedup (name+perceptual-hash) → **498 màn / 220 app**, **K-leak verified rỗng** vs 30-eval. Scripts: `fetch_mv_expand_train.py` + `dg3_dedup_pool.py`. Đã ghi vào `train_pool_expanded`. venv `~/.venvs/thesis` (có `datasets`).

⏳ **Việc tiếp theo (thứ tự cứng — không đảo; đã đổi 18/7 theo `report/65`):**
1. ~~commit split~~ ✅ · ~~pre-register~~ ✅ (user commit report/56) · ~~mở rộng pool~~ ✅
2. **K1 — kill-test matcher hai chiều** (free, local, nomic + 127 màn có sẵn). Đo bỏ-lọt (bịa gần-nghĩa kiểu Settings→Preferences) và kết-oan (bước đúng bị đánh bịa vì VH thiếu nhãn) theo τ. **Cổng: bỏ-lọt ≤~20% và kết-oan ≤~10% ở một τ nào đó** — chốt số TRƯỚC khi nhìn kết quả. Rớt → nâng trọng tài (OCR fusion / ngưỡng kép, vòng C của `report/63`) TRƯỚC khi build data. *(Vì sao làm đầu tiên: đây là mắt xích duy nhất mà nếu đứt thì phải sửa pipeline, không phải thêm thí nghiệm.)*
3. **K2 — đếm phân loại bịa** trên kết quả BASE sơ bộ cũ (đọc tay 40-60 bước, ~2h, free). Cổng: bịa-tên-phần-tử ≥~70% → claim hiện tại đứng; dưới → thu hẹp claim + thêm luật bắt hành-động.
4. **D1/D2 debate song song** + chen **vòng A của `report/63`** (risk-coverage) NẾU K1/K2 gợi ý phải đổi thước đo — đổi thước đo thì phải sửa pre-reg `56` TRƯỚC khi gọi API/GPU, không sửa sau được.
5. **Sinh câu hỏi** — user để SAU (skip tạm).
6. **Bước 2b:** pilot baseline → tính MDE thật → điền vào report/56 §6 → commit lần 2. *(cần chạy teacher vài màn = ✱ API.)*
7. **Bước 5:** ✱ teacher gpt-4o-mini sinh BASE (~$1–2 — **HỎI USER trước**).
8. **Bước 6:** matcher + viết-lại → data SFT.
9. **Bước 7:** smoke-test train 20 mẫu trên Colab → full train 2 bản (Student + Student-RAW) → eval Tier1/Tier2.
10. **Smoke-test tiếng Việt** (~5 màn) — quyết hướng VCL.

> **Cỡ dữ liệu train hiện có:** 498 (pool) + 76 (18 app clean) = ~574 màn → ~1.700–2.870 mẫu (×3-5 câu hỏi). Cận dưới vùng đủ; muốn dày hơn thì resume `fetch_mv_expand_train.py` (free).

---

## §7. VIỆC MỞ / CẦN VERIFY (chưa có nguồn — USER tự tra, đừng bịa)
- **Deadline CFP VCL2026 thật** (30/8 mới là trí nhớ user).
- **Chính sách dual-submission / self-plagiarism** của FAIR và VCL (quan trọng vì 2 bài dùng chung data nguồn).
- Tỉ lệ chấp nhận · index Scopus/DBLP · ISBN · độ dài bài từng venue.
- FAIR có gia hạn 15/8 không.
- Mua Colab Pro (chưa cần Pro+ tới tuần train chính).

---

## §8. NGUYÊN TẮC LÀM VIỆC (đừng quên)
- **Chi tiền:** chạy MỘT lần cho đúng; mọi bước ✱ (tốn API/GPU) **HỎI USER TRƯỚC**; ưu tiên local/free.
- **Pre-registration:** freeze split + commit ngưỡng **TRƯỚC khi chạy** — gấp mấy cũng KHÔNG bỏ bước (nếu không, thiết kế 2-tầng mất giá trị).
- **Citation:** chỉ trích peer-reviewed đã verify venue/năm. Thứ-tự-bộ-phận = **Fagin 2006 + Lapata CL 2006** (KHÔNG "Kendall τ-b"). UI-R1 = **AAAI 2026** (không phải 2025).
- **Trình bày:** nói "một màn / nhiều màn", KHÔNG dùng "DG1/DG2". Trao đổi tiếng Việt.

---

## §9. BẢN ĐỒ FILE (đào chi tiết ở đâu)

**Đọc để hiểu (đủ để quyết định):**
- **`report/00_TONG_HOP_TAT_CA.md`** ← file này (tổng hợp, đọc đầu tiên).
- **`report/54_PIPELINE_FINAL_DOC_HIEU_TOAN_BO.md`** — pipeline/model tự-đủ (Phần 1 = người-thường; Phần 2 = phụ lục kỹ thuật đầy đủ).
- **`report/56_PREREG_MODEL.md`** — ngưỡng đã pre-register + commit (`2c84ce8`). Ngắn. Mọi thay đổi thước đo phải sửa file này TRƯỚC khi gọi API/GPU.
- **`report/65_phan_bien_pipeline_va_plan_kiem_chung.md`** ⭐ — mới nhất (17/7): 6 nghi ngờ chưa có bằng chứng + plan kiểm chứng chia nhỏ (K1-K3 kill-test free · D1-D3 debate · R1-R2 research). **File hành động hiện tại.**
- **`report/63_plan_deepresearch_chia_nho.md`** — 5 vòng nâng cấp độc lập (risk-coverage/AURC · template fallback · OCR fusion · DPO · so sánh). Bổ trợ 65, không trùng.
- **`report/KE_HOACH_2_BAI_BAO.md`** (bản 3) — kế hoạch 2 bài đầy đủ.
- **`CLAUDE.md §0`** — nhật ký quyết định (auto-load mỗi phiên).

**Nền của 63/65 (đọc lướt cũng đủ):**
- `report/61` — deep-research Faithful Distillation ĐÃ verify đối kháng (6 câu hỏi mở: DPO-trên-cặp-lọc · mode-collapse · risk-coverage · VH-coverage · xếp-hạng-đóng-góp). Bản dễ hiểu: `report/62`.
- `report/64` — thiết kế lại từ trang giấy trắng để đối chiếu (trùng xương sống, khác 5 điểm).
- `report/_archive/60` — export context 15/7.

**Khi bắt tay code:**
- **`report/53_ke_hoach_build_model.md`** — config YAML · data pipeline từng bước · timeline · giao thức đánh giá · 11 rủi ro kỹ thuật.

**Khi viết bài báo:**
- **`report/57_related_work.md`** — Công-trình-liên-quan: kho luận điểm theo 10 theme (citation ĐÃ verify + "ta khác gì") + 2 bản thảo tách sẵn (FAIR tiếng Anh · VCL tiếng Việt) + dự trữ nhiều-màn.

**Log gốc (chỉ mở khi tra "vì sao quyết định X"):**
- `report/50` (deep-research chọn hướng) · `report/52` (debate tính-mới) · `report/55` (stress-test thống kê) · `report/43` (hồ sơ cũ).
- `report/RESEARCH_LEDGER.md` — sổ các đợt research đã chạy (R-01→R-13).

**Code:** `harness/` — `dg3_freeze_split.py` (mới) · `train_eval_app_split.json` (mới) · các `dg1_*.py`/`aloha_match.py` tái dùng · các `dg3_*.py` cần viết (report/53 §6).
