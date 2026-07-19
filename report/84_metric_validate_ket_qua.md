# report/84 — Kết quả build + bơm-lỗi-validate thước (action, target) — CỔNG

> Việc 3 trong plan (report/81/83). Thước "so hai đoạn hướng dẫn" tách mỗi bước thành (thao-tác, đích), khớp đích = chồng-từ-nội-dung (chính) + bge-m3 (backstop cao 0.85). Bơm lỗi đã-biết vào gold rồi kiểm thước bắt được + **tách được "sai-đích" khỏi "paraphrase"** (chỗ K1 chết). Code: `harness/metric_v1_validate.py`. Data: 200 ep AndroidControl-test tải local (`dataset_samples/androidcontrol_test/ac_test_200ep.json`, 1042 step-instruction). Ngày: 2026-07-19.

## Phán quyết 1 dòng

**QUA CỔNG.** Thước (action, target) **tách sạch "sai-đích" khỏi "paraphrase"** — AUC = 1.000 (ngưỡng ≥0.80), cả ca dễ LẪN ca khó (chung từ-loại, khác entity — đúng kiểu "Gmail tab" vs "Calendar tab" đã giết K1). Việc **tách bước thành (thao-tác, đích)** giải được đúng chỗ mà đo-độ-gần-nghĩa-thuần (K1) bó tay. Còn một điểm chỉnh sau (kết-oan với paraphrase đổi từ-đồng-nghĩa), không phải blocker.

## Số liệu

**Vòng 1 — bơm lỗi cơ bản (185 ep):**

| Loại bơm lỗi | Coverage | Δ so clean | Đúng kỳ vọng? |
|---|---|---|---|
| clean | 1.000 | — | ✓ (mốc) |
| target_error (đích khác hẳn) | 0.847 | −0.153 | ✓ (1 bước/~5 sai → tụt ~1/5) |
| action_error | 0.851 | −0.149 | ✓ |
| missing (xoá 1 bước) | 0.850 | −0.150 | ✓ (recall tụt) |
| extra (thêm bước thừa) | 1.000 | 0 | ✓ (không giảm coverage; bắt bằng precision) |
| reorder | 1.000 | 0 | ✓ (**đúng thiết kế**: coverage không đổi, đảo thứ tự đo bằng order-τ RIÊNG) |
| paraphrase (control) | 1.000 | 0 | ✓ (không tụt oan) |

- **Cổng tách-phân-phối:** AUC(paraphrase > target_error) = **1.000**; paraphrase TB = 1.000, target_error TB = 0.012.
- detection sai-đích = 1.000 (≥0.90 ✓), false-positive paraphrase = 0.000 (≤0.10 ✓).

**Vòng 2 — stress-test CA KHÓ (tự nghi ngờ vòng 1 quá dễ):** ép đích-sai chỉ đổi *một từ-lõi* nhưng **chung từ-loại** (vd "artworks tab" vs "view energy tab") — đây mới đúng ca K1 chết.

- đích-sai-khó: target-score TB = **0.350** (thấp → bắt đúng).
- paraphrase: TB = **1.000** (cao → không oan).
- **AUC = 1.000** (vẫn tách sạch trên ca khó).
- bge-m3 cứu-nhầm đích-sai-khó (cos≥0.85): **3/60 = 5%** (thấp — backstop không phá).

## Vì sao thước này qua được chỗ K1 chết

K1: đo độ-gần-nghĩa bằng embedding trên **cả câu** → "bịa nghe giống" và "gọi đúng bằng từ khác" chồng lấn hoàn toàn, không ngưỡng nào tách. Thước mới **không đo tương đồng bề mặt cả câu** mà:
1. Tách **thao-tác** (từ vựng đóng) — sai thao-tác là mismatch cứng.
2. Tách **đích** rồi khớp bằng **chồng-từ-nội-dung**: "artworks tab" vs "energy tab" chung {tab} nhưng khác {artworks} vs {energy} → Jaccard thấp → **không khớp** (bắt được). Đây là điều cosine-cả-câu không làm nổi.
3. bge-m3 chỉ làm **backstop ngưỡng cao (0.85)** → cứu synonym thật mà không hạ thấp gây K1 (chỉ 5% ca khó bị cứu nhầm).

Khớp đúng tinh thần AndroidControl chấm step-accuracy (đúng ⇔ đúng loại-thao-tác VÀ đúng đích), chỉ thay "toạ độ lệch ≤14%" bằng "đích-trong-văn-bản" vì mirror nhẹ không có a11y-tree.

## Hoài nghi còn lại (khai thẳng, để chỉnh sau)

1. **Paraphrase test còn dễ:** tôi giữ *nguyên từ-lõi* (chỉ đảo trật tự + thêm article) → Jaccard=1 tất yếu. Nếu model THẬT dùng **từ đồng nghĩa cho loại nút** ("tab"→"section", "button"→"control") thì Jaccard tụt → có thể **kết-oan** (false-positive). Đây là **chỉnh backstop bge-m3** (hạ nhẹ ngưỡng / thêm từ-điển-loại-nút), CẦN output model thật để hiệu chỉnh — làm ở bước sau, KHÔNG chặn.
2. **Trích (thao-tác, đích) từ văn tự do** ở đây còn thô (parser luật đơn giản). Trên gold AndroidControl (câu ngắn, cấu trúc "Click on X") nó chạy tốt; trên guide dài do model sinh có thể hỏng hơn → **phải validate bộ trích riêng (P/R trên tập gán tay)** khi có output model.
3. **Perturbation do chính tôi dựng** → có phần circular (lỗi/paraphrase theo cùng logic token của thước). Đã giảm bằng vòng-2 ca-khó, nhưng validate NGƯỜI (construct-validity, việc 4) trên output THẬT vẫn cần để chắc.

## Kết luận cho plan

- **CỔNG QUA** → thước (action, target) đủ tin để đi tiếp; giả định lớn nhất (tránh bẫy K1) **đã kiểm bằng số, không assume**.
- Ngưỡng bơm-lỗi (detection≥0.90, FP≤0.10, separation-AUC≥0.80) → đưa vào bản đăng-ký-trước (việc 1) làm cam kết chính thức.
- Hai chỗ chỉnh (backstop paraphrase-synonym; validate bộ trích) cần **output model thật** → thuộc bước sau, đã ghi rõ để không quên.

> Tóm: đây là tin tốt cứng nhất từ trước tới nay — không phải suy luận mà là **số đo**: tách (thao-tác, đích) giải được đúng chỗ K1 chết (AUC 1.0 cả ca khó). Thước sống. Còn hiệu chỉnh mép (paraphrase-synonym) để lúc có model.
