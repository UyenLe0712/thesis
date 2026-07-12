# PRE-REGISTRATION — Model "Faithful Distillation" (Tier 1 / Tier 2)

> **Đăng-ký-trước:** mọi định nghĩa + ngưỡng ở file này được ĐÓNG BĂNG **TRƯỚC khi chạy thí nghiệm**.
> `git commit` file này = dấu thời gian. **KHÔNG sửa sau khi commit** (trừ ô [MDE] điền sau pilot baseline — xem §6, việc này KHÔNG lộ hiệu ứng nên không phá pre-registration).
> Nguồn: report/53 §5, report/54 Phụ lục E. Split đã khoá ở commit `3776212` (`train_eval_app_split.json`, seed=20260710).

---

## 1. PHÂN VÙNG (đã khoá)
- **18 train / 12 test app** MobileViews, seed=20260710, `harness/train_eval_app_split.json` (commit `3776212`).
- Pool train mở rộng (~200 app) điền sau khi fetch; **cổng K-leak:** pool ∩ 12 test app = ∅ (dedup theo package-name + perceptual-hash). Assert rỗng + log trước khi build data SFT.
- Student **KHÔNG bao giờ thấy View Hierarchy** (cả lúc train lẫn suy luận). VH chỉ vào lúc CHẤM.

## 2. ĐỊNH NGHĨA THƯỚC ĐO (đóng băng)
- **Faithfulness mỗi màn** = 1 − (số-lần-nhắc-nút-BỊA / tổng-số-lần-nhắc-nút) [ALOHa, NAACL 2024].
- **"Bịa"** = **đa số 3 cơ chế khác họ** đồng thuận KHÔNG-khớp với nhãn VH đúng màn:
  1. **bge-m3** cosine-sim, ngưỡng **τB hiệu chuẩn RIÊNG** (80–120 cặp gán tay → báo P/R + Cohen's κ, precision ≥0.95, freeze). **KHÔNG tái dùng τA=0.55** của nomic.
  2. **LLM-judge llama3.2** (Ollama local, khác họ generator gpt-4o-mini), prompt nhị phân CÓ/KHÔNG.
  3. **token-overlap** (fuzzy match).
- **Gộp mỗi app:** `f_app` = trung bình faithfulness các màn trong app. Đơn vị thống kê = **12 con số per-app** (macro-per-app).
- Báo kèm: **%fallback** (tỉ lệ bước rơi vào câu mô tả chung chung) + **silent-error-rate**.
- **[Vá A1-2] Màn 0-nhắc-nút:** nếu một màn có **0 lần nhắc nút** thì mẫu số = 0 → f **không xác định** → **LOẠI màn đó khỏi trung bình `f_app`** (KHÔNG mặc định f=1). Đồng thời báo RIÊNG **tỉ-lệ-màn-0-nhắc-nút** cho từng arm như một **chỉ báo né-trả-lời** — vì model có thể lách metric bằng cách không nhắc nút nào (nói toàn câu chung chung). Nếu một app có **>50% màn 0-nhắc-nút**, gắn cờ cảnh báo khi diễn giải `f_app` của app đó (mẫu quá thưa).

## 3. HAI TẦNG THÍ NGHIỆM (báo cáo ĐỘC LẬP)
- **Tier 1 (lưới an toàn):** `Student(data-lọc)` vs `Student-RAW(data-thô)`, **VH VẪN CÓ** lúc suy luận, trên 12 test app.
- **Tier 2 (trụ chính):** `Student` vs `Teacher-BASE(gpt-4o-mini)`, **TẮT HẲN VH** lúc suy luận, held-out theo app (12 test app).
- Prompt câu hỏi **giống hệt** ở 3 chỗ (SFT record · eval-có-VH · eval-không-VH) — bất biến để loại nghi vấn "khác do đổi prompt". Student prompt **cố ý KHÔNG chứa** câu "don't invent buttons" (khác GEN_PROMPT teacher — điểm mấu chốt).
- **[Vá A1-1] Faithfulness `f` đo trên OUTPUT THÔ của model ở CẢ hai tầng.** `f` (§2) được chấm trên **văn bản model sinh trực tiếp, TRƯỚC lớp viết-lại-fallback hậu-kỳ**. Lý do: lớp viết-lại chữa bịa cho MỌI bản → nếu chấm `f` *sau* viết-lại thì Student và Student-RAW đều ~sạch, `Δ_f ≈ 0` (**null giả tạo**, tái phạm lỗi tautology-trần đã vá). Cụm "VH vẫn có lúc suy luận" ở Tier 1 chỉ mô tả **bối cảnh triển khai đầy đủ** (hệ deploy vẫn còn lớp viết-lại); **lợi ích của lớp viết-lại được báo RIÊNG qua %fallback + silent-error**, KHÔNG trộn vào `f`. → Setup đo `f` ở Tier 1 và Tier 2 **giống nhau** (đều trên output thô), chỉ khác **cặp so sánh** và việc có/không lớp viết-lại ngoài-metric.
- **[Vá A2-2] Bất đối xứng prompt teacher–student là CỐ Ý, thiên về BẤT LỢI cho student.** `f_teacher` (Tier 2) chấm trên output **GEN_PROMPT gốc của teacher — CÓ chứa câu "don't invent buttons"**; student eval bằng prompt **KHÔNG** có câu đó. Nghĩa là student phải thắng teacher **dù teacher được nhắc-né-bịa còn student thì không** → hướng sai lệch **an-toàn** (student thắng ⇒ kết luận càng mạnh). Khai rõ trong luận văn để chặn nghi vấn "so sánh khập khiễng do khác prompt".

## 4. PHƯƠNG PHÁP THỐNG KÊ (exact sign-flip, G=12)
```
d_j = mean_{i in app_j}(f_student_i − f_comparison_i)     # j = 1..12
t_obs = mean(d) / (std(d, ddof=1) / sqrt(12))
# EXACT: liệt kê toàn bộ 2^12 = 4096 tổ hợp dấu (không Monte Carlo)
null_stats = [ mean(s*d)/(std(s*d)/sqrt(12)) for s in product([+1,-1], repeat=12) ]
p_value = mean( abs(null_stats) >= abs(t_obs) )
# CI 95% bằng test-inversion trên chính phân phối exact đó
```
Dùng exact khi G≤~13; nếu đổi lên G lớn hơn → wild-cluster bootstrap Rademacher B=9999. Trích: Canay-Santos-Shaikh 2021; Cameron & Miller 2015.

## 5. NGƯỠNG ĐẬU/RỚT (đóng băng — 3 kết cục viết sẵn diễn giải)

**Tier 1 PASS:** CI 95% của `Δ = mean(f_student − f_studentRAW)` nằm **HOÀN TOÀN trên 0** — với `f` đo trên **output THÔ** (§3 vá A1-1). Báo kèm **%fallback** hai arm (Student-RAW kỳ vọng %fallback cao hơn khi chạy qua lớp viết-lại — đó là tín hiệu bổ sung, không thay `f`). (Không cần điều kiện (B) vì Tier 1 gần chắc dương theo tiền lệ.) Nếu Tier 1 cũng null → dừng, rà lại toàn bộ pipeline lọc trước khi diễn giải Tier 2.

**Tier 2 — hai điều kiện:**
- **(A) Ý nghĩa thống kê:** CI 95% của `Δ = mean(f_student − f_teacher)` nằm hoàn toàn trên 0.
- **(B) Ý nghĩa thực tế:** `Δ_test ≥ 0.5 × Δ_train`.
  - **Δ_train (định nghĩa DUY NHẤT):** đo bằng ĐÚNG cùng công thức + ĐÚNG cùng điều kiện **tắt-VH** như Δ_test, chỉ khác là tính trên **18 TRAIN-app** thay vì 12 TEST-app. (KHÔNG dùng "số sơ bộ trong-phân-phối" cũ.)
  - Hệ số 0.5 = tự đề xuất, khai rõ trong luận văn, không lấy từ literature.

| Kết cục | Điều kiện | Diễn giải (viết TRƯỚC khi nhìn số) |
|---|---|---|
| **PASS đầy đủ** | (A) + (B) | Nội-tại-hoá thật, tổng quát hoá đáng kể sang app mới (trong phạm vi màn giống MobileViews đã QC) |
| **PASS một phần** | (A) đúng, (B) sai | Nội-tại-hoá có ý nghĩa nhưng suy giảm mạnh — vẫn là existence-proof có giá trị |
| **NULL** | CI chứa 0 hoặc Δ_test ≤ 0 | Báo trung thực kèm MDE — giới hạn tổng quát hoá đáng công bố (khung negative-results, NeurIPS 2021 Pre-reg Workshop). KHÔNG tự động lùi về "chỉ lắp ráp công cụ" vì Tier 1 vẫn đứng độc lập |

## 6. MDE / POWER (tính TRƯỚC khi khoá ngưỡng cuối)
```
MDE = (t_{0.025,df=11} + t_{0.20,df=11}) × SD(d_j) / sqrt(12) ≈ 3.077 × SD(d_j)/sqrt(12)
```
- **SD(d_j)** = độ lệch chuẩn của **12 con số d_j ĐÃ trung bình theo app** (KHÔNG phải SD thô per-màn).
- Ước lượng bằng **cận trên thận trọng:** `SD(d) ≈ sqrt(Var(f_teacher) + Var(f_student_proxy))` (giả định độc lập).
- **Lấy SD từ pilot baseline** (chấm f_teacher trên vài app — chỉ đo phương sai nền, KHÔNG lộ hướng/độ-lớn hiệu ứng → không phá pre-registration).
- **Quy tắc:** nếu MDE thật **> 15–20 điểm phần trăm** → **tăng split lên 15/15 TRƯỚC khi khoá ngưỡng** (không sửa sau khi nhìn kết quả test).
- **[MDE = ___ pp]** ← ĐIỀN sau pilot baseline, rồi commit lần 2.

## 7. HIỆU CHỈNH ĐA-KIỂM-ĐỊNH (Holm)
Family metric đóng băng TỪ GIỜ (thêm/bớt sau khi nhìn số = vi phạm): **{ faithfulness Tier 1, faithfulness Tier 2, phép-đo-phụ hữu-ích/mạch-lạc }**. Áp Holm step-down trong family này.

## 8. 4 ĐIỂM VÁ THỐNG KÊ (ghi rõ trong luận văn)
1. SD trong MDE = SD của 12 con số **đã trung bình theo app**, không phải SD thô per-màn.
2. Công thức MDE là **xấp xỉ liên tục** (kiểu Julious), KHÔNG phải ngưỡng chính xác của exact sign-flip rời rạc.
3. Khai giả định **12 app độc lập** (không cùng công ty / UI-kit / chấm cùng lô API) như **giới hạn đã biết** — chưa kiểm chứng.
4. Kết luận Tier 2 viết đúng phạm vi: **"khái quát trong loại màn giống MobileViews đã qua QC"**, KHÔNG "mọi ứng dụng GUI".

## 9. PHÉP ĐO PHỤ (định nghĩa trước)
So riêng **độ hữu-ích/mạch-lạc** (TÁCH khỏi độ trung thực) giữa Student và Student-RAW, tập trung vào các bước từng bị viết-lại thành mô tả chung chung → trả lời "mơ-hồ-nhưng-đúng có bị chấm thấp hơn cụ-thể-nhưng-sai không".

## 10. [Vá A2-3] KIỂM ĐỊNH THƯỚC ĐO BẰNG BƠM-LỖI (perturbation — đăng-ký-trước)
Claim **C2 của bài FAIR** ("validate reference-free faithfulness metric via automatic perturbation") phải có bằng chứng — nếu không làm được thì RÚT claim, KHÔNG hứa suông. Định nghĩa TRƯỚC:
- **Bơm lỗi ĐỘC LẬP matcher** vào tập output đã-đúng, tự động chèn các loại lỗi đã-biết: (a) đổi tên nút có thật → tên nút KHÔNG có trên màn (bịa cứng); (b) đổi tên nút → nút có thật nhưng SAI màn; (c) chèn thêm bước nhắc nút bịa; (d) hoán tên nút giữa 2 màn.
- **Đo 3 tính chất:** (1) **detection-rate** = tỉ lệ lỗi-bơm bị metric bắt; (2) **false-positive-rate** = tỉ lệ bước-đúng bị chấm nhầm là bịa; (3) **đơn-điệu** = bơm càng nhiều lỗi ⇒ `f` càng giảm.
- **Ngưỡng đăng-ký-trước:** detection **≥0.80**, false-positive **≤0.10**, quan hệ đơn-điệu có ý nghĩa (Spearman < 0, p<0.05). Trích: **Sai et al. EMNLP 2021** (perturbation = kiểm định độ nhạy thước đo).
- **Phạm vi (khai thẳng):** đây là **điều kiện CẦN** (độ nhạy/sensitivity), **KHÔNG** claim convergent-validity với đánh giá của người — human-correlation là future-work, không phải cổng đậu/rớt (Clark ACL-IJCNLP 2021).
- **Nếu KHÔNG kịp dựng harness trước hạn FAIR → RÚT claim C2 khỏi abstract FAIR** (thà thiếu còn hơn hứa thứ chưa tồn tại).

---
**Quy trình commit:** (1) commit file này TRƯỚC pilot. (2) Chạy pilot baseline → điền [MDE] §6 → nếu cần đổi 15/15 thì đổi + commit lần 2. (3) SAU đó mới chạy full Tier 1 / Tier 2. Mọi bước ✱ tốn API/GPU: hỏi user trước.
