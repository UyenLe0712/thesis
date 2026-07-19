# report/79 — Pilot AndroidControl: cổng go/no-go cho trục ĐÚNG

> Cổng sống-chết ở report/78: trục ĐÚNG (chấm độ đúng bằng gold AndroidControl) có khả thi không. Chạy tự chủ 18/7 đêm. Code: `harness/pilot_androidcontrol.py` (+ validate local `dataset_samples/androidcontrol/`). Số: `harness/pilot_ac_results.json`. Ngày: 2026-07-18.

## Phán quyết 1 dòng

**GO — nhưng ĐỔI CƠ CHẾ.** Trục ĐÚNG khả thi, tuy nhiên cách report/78 giả định (map `gold(x,y)→accessibility-tree→TÊN nút` rồi so tên) **YẾU** (chỉ ~40-52% bước lấy được tên vì ~48% gold-click nhắm icon/ảnh không chữ; a11y-tree lại KHÔNG có ở mirror HF). Pilot tìm ra **cơ chế tốt hơn có sẵn: AndroidControl có gold `step_instructions` — hướng dẫn NGƯỜI viết từng bước** → so **hướng-dẫn-model ↔ hướng-dẫn-người** (văn bản). Cách này phủ MỌI bước, **gỡ được khe construct-validity lớn nhất của report/78** (người↔người, không phải agent-action), và không cần a11y-tree.

## Ba số pilot (100 bước click/long_press thật)

| Kiểm | Kết quả | Ý nghĩa |
|---|---|---|
| **Khung toạ độ** gold vs ảnh | **KHỚP SẠCH** | ảnh 1080×2400 & 1440×3120, gold scale đúng; "Search"/"Next"/"Airlines"/"+" trúng ngay điểm. **Giải toả rủi ro #1 của report/71** |
| **K-map qua tên nút** (OCR-tại-điểm, cận dưới) | **40% strict / 52% relaxed** | chỉ ~nửa gold-click lấy được tên |
| **Gold-click không có chữ gần** (icon/ảnh) | **~48%** | list-item, ảnh, map-pin, icon → không đặt tên được. Trần thật, khớp K1/OCR |
| **A11y-tree ở mirror HF** | **KHÔNG có** | chỉ bản gốc GCS (cần tensorflow + tải GB); "parsed" mirror đều lược |

*(40% là cận dưới: a11y-tree thật có bbox PHẦN TỬ + content_description → sẽ cao hơn OCR-chữ, nhưng ~48% icon/ảnh vẫn là trần dù có a11y.)*

## Phát hiện then chốt: AndroidControl có gold hướng-dẫn-người từng bước

AndroidControl (Li et al., NeurIPS 2024 D&B) thu thập **hai tầng**: high-level goal + **low-level step instructions** do người demo viết. Ví dụ thật (đã xác minh khi probe): goal *"locate the Spanner under Tools & Hardware"* → các bước *"Go back to the previous page"*, *"...to see category"*, *"tap the Tools & Hardware category"*...

→ Đây là **gold cho đúng loại output của luận văn** (hướng dẫn cho NGƯỜI đọc), không phải toạ-độ-thao-tác-cho-agent.

## Hai cơ chế chấm độ-đúng — so sánh (pilot quyết đổi sang cơ chế 2)

| | Cơ chế 1 (report/78): map coord→tên nút | Cơ chế 2 (pilot đề xuất): so gold step-instruction |
|---|---|---|
| Phủ được | ~40-52% bước (chỉ nút có tên) | **~100% bước** (mọi bước có instruction) |
| Cần a11y-tree | Có (không tải nhẹ được) | **Không** (có trong mirror HF) |
| Cần map toạ độ | Có (dễ lệch) | **Không** |
| Construct-validity | agent-action ≠ hướng-dẫn-người (khe report/78) | **người↔người, khớp task** |
| Cách chấm | so tên nút | so văn bản (embedding/LLM-judge/khớp-thực-thể) — tái dùng máy no-gold sẵn có |

## Trục ĐÚNG thiết kế lại (sau pilot)

- **Chính:** so **hướng-dẫn-model ↔ gold step_instruction** (văn bản). Chấm bằng bộ máy khác-họ đã có (embedding bge-m3 + LLM-judge) — **và phải validate metric này bằng bơm-lỗi** như thước trung thực (TN6), không tin trần.
- **Phụ (giữ từ report/54):** point-in-bbox grounding trên ~40-50% bước có nút-tên/toạ-độ → tín hiệu độ-đúng-vị-trí bổ sung (không headline).
- **Giữ nguyên từ report/78:** đóng khung **SO SÁNH CẶP** (Student-LỌC/THÔ/Teacher-BASE trên CÙNG lát AndroidControl → lệch-miền triệt tiêu trong hiệu-số; estimand = hiệu-cặp, không phải điểm tuyệt đối) + pre-register **lát gần-miền** (AndroidControl-Low, app-category trùng) TRƯỚC khi nhìn số.

## Cái CHƯA test (khai thẳng, không overclaim)

- **Chưa chạy model sinh trên AndroidControl** → chưa có con số Step-SR/instruction-match THỰC (cần student/teacher generate; là bước sau, cần model). Pilot này chỉ xác nhận **KHẢ THI về dữ liệu** (có gold instruction, toạ độ sạch), chưa phải "không suy biến sàn-0".
- **Chưa fetch a11y-tree** — vì cơ chế 2 không cần; nếu sau muốn dùng cơ chế 1 làm phụ thì phải tải bản gốc GCS (tensorflow, ~GB).
- **Metric so-instruction chưa định nghĩa/validate** — model sinh guide NHIỀU bước, gold là instruction TỪNG bước → cần cách gióng (align) model-step ↔ gold-step + chấm; đây là việc thiết kế + bơm-lỗi-validate, chưa làm.
- HF mirror AndroidControl **chập chờn** (wangyuanlei lỗi schema khi stream/first-rows) — khi build thật nên tải về local một lần, không stream.

## Go/no-go + việc kế

**GO** (trục ĐÚNG sống, qua cơ chế 2). Việc kế theo thứ tự:
1. Tải AndroidControl-test về local một lần (ưu tiên bản có `step_instructions` + ảnh; wangyuanlei hoặc ckg+wangyuanlei ghép), pre-register lát gần-miền.
2. Thiết kế + bơm-lỗi-validate metric so-instruction (align model-step↔gold-step).
3. Nghiên-cứu-nhỏ construct-validity: đối chiếu "instruction-match" vs "người-chấm-đúng" vài chục mẫu (đã nhẹ đi vì giờ so người↔người).
4. RỒI mới generate bằng student/teacher → đo hiệu-cặp.
5. Mang report/78+79 lên gặp thầy (khung LAI + cơ chế đúng đã sửa).

## Cập nhật — đã kiểm chất lượng gold step_instructions (rủi ro #4 gỡ)

Tải 30 episode wangyuanlei (159 step-instruction) đọc: **chất lượng tốt.** TB 7 từ, **87% có động từ thao tác, 0% ngắn-mơ-hồ**. Nêu đích danh mục tiêu ("Click on **Tools & Hardware**", "Click on the **share button**", "Click on the **Gmail tab**", "Type ...@gmail.com in the input box") và **có cả chỉ-dẫn-vị-trí** ("at the bottom left corner", "top right corner"). Đáng chú ý: gold này chứa đúng thứ mà VIỆC1 thấy fallback của mình THIẾU (chỉ vị trí/hình) → nó vừa là thước, vừa là **hình mẫu hướng dẫn tốt** để nhắm tới. → cơ chế 2 có gold đủ cụ thể để chấm; rủi ro #4 hạ.

## Rủi ro của bản pilot này

1. **Chưa có con số Step-SR thực** — "không suy biến sàn-0" mới xác nhận được sau khi có model sinh. Pilot chỉ chứng minh khả-thi-dữ-liệu.
2. **Align đa-bước↔đơn-bước** có thể rối (model gộp/tách bước khác gold) — cần luật gióng rõ, có thể là chỗ mới phát sinh nhiễu.
3. **Vẫn cross-dataset** — difference-in-differences chỉ giảm chứ không xoá lệch-miền; giả định "lệch đều mọi nhánh" vẫn không test được (report/78).
4. Cơ chế 2 dựa vào **chất lượng gold step_instructions** của AndroidControl — cần đọc-mẫu kiểm chúng đủ cụ thể (một số có thể mơ hồ "tap the item").

> Tóm: pilot **PASS về khả thi dữ liệu** và cho một **nâng cấp thiết kế**: chấm độ-đúng bằng **gold hướng-dẫn-người từng-bước** (phủ mọi bước, khớp task, không cần a11y) thay vì map-coord→tên-nút (chỉ ~40% + lệch construct). Khung LAI của report/78 đứng vững và mạnh hơn. Chưa đo Step-SR thực (cần model) — đó là bước sau khi chốt với thầy.
