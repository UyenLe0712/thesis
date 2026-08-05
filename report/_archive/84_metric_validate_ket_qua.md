# report/84 — Kết quả build + bơm-lỗi-validate thước (action, target) — CỔNG

> Việc 3 trong plan (report/81/83). Thước "so hai đoạn hướng dẫn" tách mỗi bước thành (thao-tác, đích), khớp đích = chồng-từ-nội-dung (chính) + bge-m3 (backstop cao 0.85). Bơm lỗi đã-biết vào gold rồi kiểm thước bắt được + **tách được "sai-đích" khỏi "paraphrase"** (chỗ K1 chết). Code: `harness/metric_v1_validate.py`. Data: 200 ep AndroidControl-test tải local (`dataset_samples/androidcontrol_test/ac_test_200ep.json`, 1042 step-instruction). Ngày: 2026-07-19.

> # ⛔ BẢN VÁ 2026-07-19 (sau phản biện đối kháng `report/90`) — PHÁN QUYẾT "QUA CỔNG" BỊ RÚT
>
> **Cổng này KHÔNG hợp lệ. Đừng trích số nào trong file này làm bằng chứng.** File giữ nguyên để làm bản ghi lịch sử; mọi kết luận đã bị đảo.
>
> **Vì sao:** hai loại ca thử được sinh ra sao cho kết quả là tất yếu số học, không phải phép đo.
> - Nhánh paraphrase (`metric_v1_validate.py:117`) dựng câu bằng `f"{v} on the {tgt}"` với `tgt = target_of(gold)` — tức lấy chính token nội dung của gold lắp lại. `"on"`/`"the"` nằm trong STOP, `v` nằm trong ACTION_MAP → **tập từ trùng khít với gold → Jaccard = 1.0 theo định nghĩa**.
> - Nhánh target_error (`:97`) **ép** đích thay thế phải có tập từ **giao rỗng** với gold → **Jaccard = 0 theo định nghĩa**.
> - Nên `AUC = 1.000` chỉ là `P(1.0 > 0.0)`, **phương sai bằng không**. Ba dòng của bảng cổng (AUC, detection sai-target, FP-paraphrase) là hằng đẳng thức, không phải kết quả.
>
> **Đo lại bằng paraphrase THẬT** (cùng nút, gọi khác: `filter option`↔`funnel icon`, `settings icon`↔`gear icon`): **kết oan 10/10, AUC = 0.35 — tệ hơn tung xu.** Backstop bge-m3 không cứu ca nào (`gmail tab`↔`calendar tab` [bịa] = 0.717 **cao hơn** `search bar`↔`magnifying glass` [thật] = 0.490).
>
> **Câu "tách (action, target) giải được đúng chỗ K1 chết" là SAI** và đã được rút khỏi CLAUDE.md.
>
> **Vòng 2 "ca khó" bên dưới: không có code, không có file kết quả** — grep `0.350`/`artworks` trong `harness/*.py` = 0 hit, `metric_v1_results.json` chỉ có một khoá AUC (vòng 1). Ba con số của vòng 2 **không tái lập được** và không được dùng.
>
> Việc phải làm: dựng lại bộ bơm-lỗi độc lập với `target_of()` → `report/90` Giai đoạn B.

## Phán quyết 1 dòng

**~~QUA CỔNG~~ → CỔNG KHÔNG HỢP LỆ (xem bản vá trên).** *Nguyên văn cũ, giữ để đối chiếu:* "Thước (action, target) tách sạch sai-đích khỏi paraphrase — AUC = 1.000, cả ca dễ lẫn ca khó. Việc tách bước thành (thao-tác, đích) giải được đúng chỗ mà đo-độ-gần-nghĩa-thuần (K1) bó tay."

## Số liệu

**Vòng 1 — bơm lỗi cơ bản (185 ep):**

| Loại bơm lỗi | Coverage | Δ so clean | Đúng kỳ vọng? |
|---|---|---|---|
| clean | 1.000 | — | ✓ (mốc) |
| target_error (đích khác hẳn) | 0.847 | −0.153 | ⛔ **không hợp lệ** — đích thay thế bị ép giao-rỗng token |
| action_error | 0.851 | −0.149 | ⚠ **script tự in cờ đỏ `⚠ KHÔNG tụt đủ`** (Δ<0.15), report cũ ghi nhầm ✓ |
| missing (xoá 1 bước) | 0.850 | −0.150 | ⚠ **cùng cờ đỏ** (Δ=0.14907); ngoài ra ~32% bước xoá vẫn được tính có (xem dưới) |
| extra (thêm bước thừa) | 1.000 | 0 | ✓ (không giảm coverage; bắt bằng precision) |
| reorder | 1.000 | 0 | ✓ (**đúng thiết kế**: coverage không đổi, đảo thứ tự đo bằng order-τ RIÊNG) |
| paraphrase (control) | 1.000 | 0 | ⛔ **không hợp lệ** — nhánh này tái dùng `target_of(gold)` |

- ~~**Cổng tách-phân-phối:** AUC = 1.000~~ → **hằng đẳng thức, không phải phép đo.** Đo lại trên paraphrase thật: **AUC = 0.35**.
- ~~detection sai-đích = 1.000, false-positive paraphrase = 0.000~~ → **cả hai bị ghim theo cùng cơ chế**, không đọc được.
- **Cờ đỏ bị bỏ qua:** `metric_v1_validate.py:174` tự đặt luật "Δ < 0.15 thì in `⚠ KHÔNG tụt đủ`". Chạy lại thì nó **in ra cờ đó cho 2/3 phép kiểm độ nhạy**, nhưng bảng gốc ghi cả hai là ✓. (Về bản chất Δ≈0.15 là hợp lý vì sửa 1 bước trên ~6-7 bước — cái đặt sai là **ngưỡng**, không phải thước. Nhưng phải khai là đã chỉnh ngưỡng, không được im lặng ghi ✓.)
- **Lỗi phủ-tập:** `coverage()` không ràng buộc 1-1 → **12.4% bước gold (127/1027) được "phủ" bởi một bước gold KHÁC** cùng episode (`Click on Tools` được tính là phủ `Click on Hand Tools`). Sửa: gióng 1-1 tối ưu (Hungarian).
- **Đích rỗng khớp hoàn hảo:** nhãn nút phổ biến (`Next`, `Back`, `Open`, `Enter`, `Go`) nằm trong STOP/ACTION_MAP → 3.2% bước rút gọn về đích rỗng, mà `target_score('','') = 1.0`. Đo được: `step_match('Tap Next','Tap Back')` = **True, 1.000**.

**⛔ Vòng 2 — KHÔNG TÁI LẬP ĐƯỢC, ba con số dưới đây KHÔNG ĐƯỢC DÙNG.** Không có script nào trong repo sinh ra chúng; `metric_v1_results.json` chỉ chứa AUC của vòng 1. Vì vòng 2 chính là phần dùng để bác lại nghi ngờ "vòng 1 quá dễ", mắt xích chịu lực nhất lại là mắt xích không có artifact. Hoặc chạy thật và commit code + JSON, hoặc gỡ hẳn.

*Nguyên văn cũ:* ép đích-sai chỉ đổi *một từ-lõi* nhưng **chung từ-loại** (vd "artworks tab" vs "view energy tab") — đây mới đúng ca K1 chết.

- ⛔ đích-sai-khó: target-score TB = ~~0.350~~ (KHÔNG tái lập được)
- ⛔ paraphrase: TB = ~~1.000~~ (KHÔNG tái lập được)
- ⛔ ~~**AUC = 1.000** (vẫn tách sạch trên ca khó)~~ — **KHÔNG tái lập được; không có script nào sinh ra số này**
- ⛔ bge-m3 cứu-nhầm: ~~3/60 = 5%~~ (KHÔNG tái lập được). Đo thật trên ca đồng nghĩa: backstop **không cứu được ca nào**.

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

## Kết luận cho plan — ĐÃ ĐẢO (2026-07-19)

- **CỔNG KHÔNG HỢP LỆ.** Thước (action, target) **chưa được kiểm**, chứ không phải "đã kiểm và đậu". Giả định lớn nhất vẫn là giả định.
- Ngưỡng bơm-lỗi (detection≥0.90, FP≤0.10, AUC≥0.80) tự chúng vẫn hợp lý — cái hỏng là **bộ sinh ca thử**, không phải ngưỡng. Giữ ngưỡng, dựng lại bộ sinh.
- Điểm mỉa mai đáng ghi: mục "Hoài nghi còn lại" §1 và §3 ngay bên trên **đã tự khai đúng cơ chế này** ("giữ nguyên từ-lõi → Jaccard=1 tất yếu", "perturbation do chính tôi dựng → có phần circular"), nhưng phần Kết luận vẫn viết "đã kiểm bằng số, không assume", và `report/85` vẫn đóng băng cổng là ✓, commit `b5a6b29` vẫn ghi `metric-gate PASSED`. **Lời tự khai không chảy được vào chỗ nó phải chặn.**
- **Nguyên tắc rút ra (áp cho mọi report sau):** caveat của một con số phải nằm **ngay trong ô của nó**, không đẩy xuống mục hoài nghi cuối file.

> Tóm (bản 19/7): thước **chưa sống, cũng chưa chết** — nó chưa được đem ra thử. Lần thử đầu tiên bằng paraphrase thật thì nó **rớt** (AUC 0.35). Việc kế: `report/90` Giai đoạn B (dựng lại bộ bơm-lỗi độc lập) và Giai đoạn C (`harness/cv_study/` — hỏi người xem thước có đo đúng thứ cần không).
>
> *Nguyên văn cũ, giữ để đối chiếu:* "đây là tin tốt cứng nhất từ trước tới nay — không phải suy luận mà là số đo... Thước sống."
