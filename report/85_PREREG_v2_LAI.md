# PRE-REGISTRATION v2 — Phương án LAI (trục ĐÚNG chính + trung thực phụ)

> **Đăng-ký-trước:** mọi định nghĩa + ngưỡng ở file này ĐÓNG BĂNG **TRƯỚC khi train/eval chính**. `git commit` file này = dấu thời gian. **KHÔNG sửa sau commit** (trừ các ô `[...___...]` điền sau bước đo-nền, ghi rõ ở dưới — những cái đó KHÔNG lộ hướng hiệu ứng).
> **Thay `report/56`** (bản v1 lấy faithfulness làm trục chính — nay hạ xuống phụ vì K2). report/56 GIỮ làm bản ghi lịch sử, KHÔNG xoá.
> Nguồn thiết kế: report/81 (thiết kế cuối), report/84 (thước đã qua cổng bơm-lỗi), report/78/79 (quyết định + pilot). Ngày: 2026-07-19.

---

> # ⛔ BẢN VÁ 1 — 2026-07-19, sau phản biện đối kháng `report/90`
>
> **Không sửa lặng.** Bản gốc đã commit `b5a6b29` (kèm chữ `metric-gate PASSED` trong commit message — chữ đó nay SAI). Phần dưới giữ nguyên văn; bản vá này ghi rõ cái gì mất hiệu lực, vì sao, và ngày nào.
>
> **Trạng thái sau vá: file này CHƯA ĐỦ ĐIỀU KIỆN làm dấu-thời-gian cho việc train.** Phải sửa xong bốn mục dưới rồi commit lại (bản vá 2) trước khi chạy bất kỳ lệnh train nào.
>
> | # | Chỗ | Vấn đề | Trạng thái |
> |---|---|---|---|
> | V1 | §4 bảng cổng — 3 dòng `detection sai-target 1.000`, `FP paraphrase 0.000`, `AUC 1.000` | **Hằng đẳng thức, không phải phép đo.** Nhánh paraphrase của bộ bơm-lỗi gọi chính `target_of()` rồi dán lại nguyên văn output của nó (Jaccard=1 tất yếu); nhánh target_error bị ép giao-rỗng token (Jaccard=0 tất yếu). Đo lại bằng paraphrase THẬT: **AUC = 0.35, kết oan 10/10**. | ❌ RÚT — cổng chưa qua |
> | V2 | §4 dòng "(cả ca khó)" | Vòng 2 **không có code, không có file kết quả**. Ba con số (0.350 / AUC 1.0 / bge cứu nhầm 5%) không tái lập được. | ❌ GỠ SỐ |
> | V3 | §1 + §6 — `~72% ep gán được app`, `~114 app distinct`, `G ≈ 150-250`, `MDE ~9 pp` | Đếm từ **sai quần thể** (`ac_test_200ep.json` = test chung, không phải app_unseen). Trên đúng split (`ac_app_unseen_count.json`): **41% gán được, 42 app distinct/102 ep, tập trung mạnh** (Pinterest 14, Arts&Culture 8) chứ không "phần lớn singleton". → **MDE thật ≈ 12.5–14.4 pp**, không phải 8-9. Thêm: bộ gán app tách một app thành nhiều cụm (`The Washington Post` vs `Washington post`) và đẻ cụm rác (`On the Pinerest`) → **G thổi phồng, CI hẹp giả**. | ❌ TÍNH LẠI |
> | V4 | §6 ô `[MDE trục trung thực = ___ pp]` | Để trống mà vẫn commit. Mô phỏng sign-flip đầy đủ ở G=12 với SD=0.362: lực chỉ **25% @15pp, 43% @20pp**; công thức của chính file này cho **32.2 pp** → **trục trung thực RỚT ngưỡng 15-20 gấp đôi**. Một kết quả null ở trục này sẽ không đọc được gì. | ❌ PHẢI ĐIỀN TRƯỚC KHI COMMIT LẠI |
>
> **Ngoài ra, hai chỗ phải thêm chứ không chỉ sửa:**
>
> - **Nhánh Teacher-STYLE-MATCHED (bắt buộc).** Student train trên gold AC sẽ nói đúng phương ngữ annotator; Teacher zero-shot nói khác nên bị kết oan có hệ thống. Đo được: chỉ đổi lựa chọn bề mặt của thước (gộp tap/open, containment thay Jaccard, bỏ từ chỉ vị trí) làm điểm teacher nhảy **0.286 → 0.604** mà không đổi một chữ nội dung. ⇒ Δ(Student − Teacher-BASE) hiện **không diễn giải được**. Phải tách: `Student − Teacher-STYLE` = chọn đúng nút; `Teacher-STYLE − Teacher-BASE` = khớp giọng thuần. Điều này **đảo §8 rủi ro 4** — câu "thước action∧target bớt nhạy phong cách" là SAI, token-overlap là thước nhạy phong cách nhất khi từ vựng khác nhau.
> - **§8 rủi ro 2 phải đổi cách xử.** "Hiệu chỉnh backstop khi có output model thật" = chỉnh thước trên chính dữ liệu đánh giá sau khi đã đóng băng ngưỡng. Phải hiệu chỉnh trên **tập dev tách riêng** (app ngoài test split), khoá lại, ghi rõ dev nào / ngày nào / commit nào, rồi mới chạy test.
>
> **Việc trước khi commit bản vá 2:** `report/90` Giai đoạn B (dựng lại bơm-lỗi) → C (`harness/cv_study/`, construct-validity với người) → D (đếm lại G, tính lại MDE cả hai trục).

---

## 0. ĐÓNG GÓP (khung hai trụ — chốt 19/7)

1. **MODEL** — model đầu tiên **sinh hướng dẫn nhiều-bước CHO NGƯỜI ĐỌC** từ 1 ảnh + câu hỏi (mọi model GUI khác sinh action-cho-máy). Tính mới ở **tác vụ**, KHÔNG ở "3B on-device".
2. **ĐÁNH GIÁ** — cặp thước **độ ĐÚNG (gold) + độ TRUNG THỰC (no-gold, VH)** + chương đo-lường (4 kill-test K1/K2/OCR/VIỆC1).

Hai trụ ngang nhau. Kết cục null ở một trục KHÔNG kéo sập trục kia (báo cáo độc lập).

## 1. PHÂN VÙNG (đã/ sẽ khoá)

- **Trục ĐÚNG (chính):** dùng **AndroidControl app-unseen split CHÍNH THỨC = 631 episode** (từ reece124/android_control; app ở test KHÔNG xuất hiện lúc train — held-out-by-app chuẩn của bộ). Đã xác nhận 631/631 ep có file tải được ở mirror wangyuanlei.
- **Đơn vị thống kê = per-app.** Gán app mỗi ep bằng **open_app-action + trích-từ-goal** (~~phủ ~72% ep trên mẫu 200~~ ⛔ **V3 — trên đúng app_unseen split chỉ 41%**; phần còn lại gán tay/GCS lúc build). ~~**AndroidControl CỰC đa dạng app — ~114 app distinct chỉ trong 200 ep, phần lớn app 1-2 ep** → **[số app test AC ≈ 150-250, phần lớn singleton]**~~ ⛔ **V3 — đếm từ SAI quần thể.** Trên `ac_app_unseen_count.json`: **42 app distinct / 102 ep gán được, tập trung mạnh** (Pinterest 14, Arts&Culture 8, CNN 6). **[G thật = ___ , điền sau khi gán app cho cả 631 ep]**. Hệ quả: **G LỚN** (khác hẳn MobileViews G=12) → dùng **wild-cluster bootstrap**, KHÔNG exact sign-flip (xem §6).
- **KHÔNG dùng "lát gần-miền" nữa** (v1/report/81 đề xuất, nay BỎ): lát gần-miền vốn là hedge chống lệch-miền của thiết kế CROSS-dataset (report/78). Thiết kế cuối là **IN-DISTRIBUTION** (train + chấm đều trên AndroidControl app-unseen) → lệch-miền không còn → dùng thẳng **toàn bộ split chính thức 631 ep**, tránh mang tiếng cherry-pick. ("AndroidControl-Low" tự thoả vì ta dùng chính low-level step_instructions làm gold.)
- **Trục TRUNG THỰC (phụ):** MobileViews **18 train / 12 test app** (seed=20260710, `train_eval_app_split.json`, commit `3776212`) — giữ nguyên từ v1.
- **Chống leak:** app test (cả AC lẫn MV) KHÔNG xuất hiện lúc train; VH/gold chỉ vào lúc CHẤM. Student KHÔNG thấy VH bao giờ.

## 2. NGUỒN TRAIN (một model)

- **Tín hiệu CHÍNH:** gold `step_instructions` (người viết) của AndroidControl train-split → target sinh.
- **Data PHỤ (aux):** MobileViews chưng-cất (teacher gpt-4o-mini sinh nháp không thấy VH → matcher **đa-tầng** [chuỗi→VH→OCR→từ-điển-ký-hiệu, report/75/73] → lọc/viết-lại). **Ablation bắt buộc: aux MV bật/tắt** (tách "lợi từ chưng cất" khỏi "lợi từ gold AC").
- Model: Qwen2.5-VL-3B, QLoRA r=8/α=16, freeze-vision, LLaMA-Factory, 1 GPU Colab.
- **[Vá]** fallback-rewrite của MV-aux: cân nhắc BỎ (VIỆC1 cho thấy câu circular hại) — quyết trong bước build, ghi rõ.

## 3. THƯỚC TRỤC CHÍNH — độ ĐÚNG (đã qua cổng bơm-lỗi, report/84)

- Tách mỗi bước (model & gold) thành **(action, target)**: action = từ-vựng-đóng (tap/type/scroll/long_press/open/navigate); target = tên đích, chuẩn-hoá-chuỗi + backstop bge-m3 (khác họ nomic-lọc & GPT-teacher).
- **Một bước khớp ⇔ action khớp VÀ target khớp.** Gióng model↔gold bằng **phủ-tập** (tồn tại model-step khớp gold-step; không ép 1-1).
- **Headline = coverage-recall của target-khớp CÓ ĐIỀU KIỆN action-đúng** + **F1** (chống nhồi bước thừa) + **order-τ partial** (Fagin SIAM 2006 + Lapata CL 2006, KHÔNG Kendall τ-b; chỉ phạt cặp bắt-buộc suy từ gold).
- **Báo action và target RIÊNG** (chống degeneracy "luôn đoán tap").
- **Báo tách nhóm target-CHỮ vs target-ICON** (~48% click AC là icon/ảnh — report/79).
- **Điểm so:** Student vs **Teacher-BASE** (gpt-4o-mini zero-shot) cùng split cùng thước.
- **LLM-judge khác-họ** (Llama-3.x/Gemini) = cross-check hội tụ + κ-người, **KHÔNG vào headline** (Panickssery NeurIPS 2024).

## 4. CỔNG VALIDATE THƯỚC = BƠM-LỖI (đã chạy synthetic report/84, phải chạy lại trên config cuối)

Ngưỡng ĐÓNG BĂNG (Sai et al. EMNLP 2021):

| Kiểm | Ngưỡng | Kết quả synthetic (report/84) |
|---|---|---|
| detection sai-target | ≥ 0.90 | ~~1.000 ✓~~ ⛔ **V1 — hằng đẳng thức, chưa đo** |
| detection sai-action | ≥ 0.90 | (coverage tụt đúng) ✓ |
| false-positive paraphrase | ≤ 0.10 | ~~0.000 ✓~~ ⛔ **V1 — nhánh paraphrase tái dùng `target_of()`; đo thật = kết oan 10/10** |
| **tách-phân-phối sai-target vs paraphrase (chỗ K1 chết)** | **AUC ≥ 0.80** | ~~**1.000** (cả ca khó) ✓~~ ⛔ **V1+V2 — trên paraphrase thật AUC = 0.35, RỚT** |
| đảo thứ tự → order-τ tụt, coverage GIỮ | định tính | ✓ |

**Cổng cứng:** rớt AUC≥0.80 trên config cuối → **DỪNG, sửa thước, KHÔNG train**. ⛔ **Cổng này chưa bao giờ kích hoạt được** (xem V1): bộ bơm-lỗi cũ không sinh nổi ca làm AUC<1. Cổng chỉ có hiệu lực sau khi dựng lại bộ sinh — `report/90` Giai đoạn B. (Synthetic đã qua; chạy lại trên parser cuối + validate bộ-trích P/R trên tập gán-tay khi có output model.)

## 5. THƯỚC TRỤC PHỤ — độ TRUNG THỰC (no-gold, MobileViews)

- **Tier 2** (giữ từ v1, report/56 §2-3): student 3B có bịa tên nút không tồn tại không, **tắt VH lúc sinh**, đối chiếu VH bằng **matcher đa-tầng nâng cấp** (không phải nomic-đơn đã chết ở K1). f = 1 − bịa/nhắc-nút [ALOHa NAACL 2024]. Đơn vị = 12 con số per-app.
- **Tier 1** (LỌC vs THÔ) = **readout phụ gần-miễn-phí**, báo dù null (K2: nhiều khả năng null tầm thường vì teacher bịa ~0).
- Báo kèm %fallback + silent-error + tỉ-lệ-màn-0-nhắc-nút (report/56 §2 [Vá A1-2]).

## 6. THỐNG KÊ

- **Hai trục dùng hai phép khác nhau vì G khác nhau:**
  - **Trục ĐÚNG (AndroidControl, G lớn ~150-250 app):** **wild-cluster bootstrap-t Rademacher B=9999** cluster theo app (Cameron-Gelbach-Miller REStat 2008). KHÔNG dùng exact sign-flip (2^G quá lớn, và G lớn không cần exact).
  - **Trục TRUNG THỰC (MobileViews, G=12 app):** **exact sign-flip** liệt kê 2^12=4096 tổ hợp dấu (giữ từ report/56 §4; Canay-Santos-Shaikh 2021).
- Cả hai: CI 95% + Holm.
- **MDE** tính trước từ đo-nền (công thức 3.077×SD-hiệu/√G). ~~**MDE trục ĐÚNG = ~9 pp @ G=150**~~ ⛔ **V3 — G sai nên MDE sai. Tính lại với G≈60-90: MDE ≈ 12.5–14.4 pp** (vẫn dưới ngưỡng nhưng SÁT hơn nhiều, không còn dư địa). Phần "teacher 30%, không suy biến sàn-0" vẫn đứng. **Ngưỡng 15-20 pp vốn là cơ chế chữa cháy viết cho trục MobileViews G=12 (report/56:65) — trục ĐÚNG phải có ngưỡng riêng có căn cứ.** **[MDE trục trung thực MobileViews = ___ pp]** ⛔ **V4 — để trống mà vẫn commit.** Ước lượng bằng chính công thức file này ở G=12, SD=0.362: **32.2 pp** → RỚT ngưỡng gấp đôi. Mô phỏng sign-flip đầy đủ: lực 25% @15pp, 43% @20pp. **Phải điền và quyết (tăng app MV, hay hạ trục này xuống mức mô tả) TRƯỚC khi commit lại.**
- **Holm** trên family ĐÓNG BĂNG: { coverage-đúng Tier-chính, faithfulness Tier 2, phép-đo-phụ }. Thêm/bớt sau khi nhìn số = vi phạm.

## 7. NGƯỠNG ĐẬU/RỚT (3 kết cục, viết TRƯỚC khi nhìn số)

**Trục ĐÚNG (chính):**
| Kết cục | Điều kiện | Diễn giải |
|---|---|---|
| PASS | CI 95% của Δ(Student − Teacher-BASE) coverage-đúng **hoàn toàn trên 0** | Model chưng-cất đạt/vượt teacher về ĐÚNG (in-distribution) — đóng góp model đứng |
| PASS một phần | Δ > 0 có ý nghĩa nhưng nhỏ | Có giá trị, model làm được tác vụ dù chưa vượt teacher rõ |
| NULL | CI chứa 0 | Báo trung thực + MDE; model VẪN là artifact tác-vụ-mới (đóng góp model không mất) + đóng góp đánh giá đứng độc lập |

**Trục TRUNG THỰC (phụ):** như report/56 §5 (Tier 2 PASS nếu CI của Δ student-vs-teacher trên 0; Tier 1 báo dù null).

## 8. RỦI RO KHAI TRƯỚC (đưa vào luận văn)

1. Trích (action, target) từ văn tự do có thể hỏng trên guide dài → validate bộ-trích riêng.
2. Backstop bge-m3 có thể kết-oan paraphrase đổi-từ-đồng-nghĩa → ~~hiệu chỉnh khi có output model~~ ⛔ **hiệu chỉnh trên TẬP DEV TÁCH RIÊNG** (chỉnh trên dữ liệu đánh giá = phá đăng-ký-trước). Đo thật: backstop **không cứu được ca nào** — `gmail tab`↔`calendar tab` (bịa) 0.717 > `search bar`↔`magnifying glass` (thật) 0.490.
3. ~48% target là icon/ảnh → báo tách nhóm, không gộp.
4. Circular ngược (train trên gold, chấm so gold) → ~~thước action∧target bớt nhạy phong cách~~ ⛔ **CÂU NÀY SAI.** Token-overlap là thước NHẠY phong cách nhất khi từ vựng khác nhau. Đổi lựa chọn bề mặt của thước làm điểm teacher nhảy 0.286→0.604. **Bắt buộc thêm nhánh Teacher-STYLE-MATCHED** để tách khớp-giọng khỏi chọn-đúng-nút, nếu không Δ headline không diễn giải được.
5. Tính-mới mỏng ở kiến-trúc → bán bằng tác-vụ-mới + đánh-giá, không bằng size.
6. In-distribution vẫn có thể ra số nhạt nếu 3B sinh kém → vẫn đọc-được (có Teacher-BASE mốc).

## 9. QUY TRÌNH COMMIT

1. Điền `[số app test AC]` + định nghĩa lát gần-miền + chạy lại bơm-lỗi trên config cuối → **commit file này**.
2. Pilot đo-nền → điền `[MDE]` → commit lần 2.
3. SAU đó mới build data / train / eval. Mọi bước ✱ tốn API/GPU: hỏi user (trừ standing approval).

---
*Ghi chú trung thực:* con số 15.283 ep/833 app AC + 498/220 MV lấy từ ghi-chú-đã-verify dự án — verify trước khi in. Venue OS-Atlas/UGround (ICLR2025) + STaR/CapFilt/VGA — verify trước khi ghi "peer-reviewed". ⛔ ~~Metric v1 đã qua cổng synthetic (report/84)~~ — cổng không hợp lệ, xem bản vá 1. Construct-validity NGƯỜI **không chờ output model nữa**: bộ chấm đã dựng sẵn trên 91 cặp teacher có sẵn (`harness/cv_study/`, free) — `report/90` Giai đoạn C.
