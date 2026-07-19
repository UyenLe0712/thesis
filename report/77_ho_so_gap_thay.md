# report/77 — Hồ sơ gặp thầy: 4 kill-test free + điểm quyết định

> Gói gọn kết quả 4 phép thử miễn phí chạy 18/7 (K1/K2/OCR/VIỆC1 = report/73–76) để mang lên gặp thầy. Mục tiêu: trình bằng chứng số, nêu điểm cần thầy quyết TRƯỚC khi đổ tiền train. Ngày: 2026-07-18.

---

## 1. Một trang tóm tắt (đọc phần này trước)

Bốn phép thử *miễn phí, chạy trên máy* — làm ĐÚNG tinh thần "kiểm rẻ trước khi tiêu tiền" — cho một bức tranh nhất quán về mắt xích trung tâm của luận văn (bộ lọc-bịa dựa trên View Hierarchy):

| # | Phép thử | Phát hiện chính | File |
|---|---|---|---|
| **K1** | Kiểm bộ đối chiếu (matcher) hai chiều | Ở τ=0.55: bỏ lọt 47,5% bịa gần-nghĩa + kết oan 47,5% paraphrase; hai loại **chồng lấn hoàn toàn → không ngưỡng nào tách được** | 73 |
| **K2** | Đếm phân loại bịa THẬT (80 màn teacher) | **0 ca bịa gần-nghĩa thật**; 35/40 ca "bịa" là **NÚT THẬT bị VH bỏ nhãn**; teacher bịa **~0-2%**, không phải "¼" | 74 |
| **OCR** | Đo VH-only vs VH+OCR (127 màn) | OCR cứu nhãn text (+6 điểm, 74→80%) nhưng **thua icon thuần** (`✓`...); ~20% nút vẫn không nhãn | 75 |
| **VIỆC1** | Đọc tay 127 câu fallback | An toàn (không bịa) nhưng **circular** (80% chỉ lặp mục tiêu), 20% sượng ngữ pháp; thường thay nút-thật bằng câu mơ hồ | 76 |

**Một câu:** matcher yếu (K1), nhưng lỗi thực tế không phải "bỏ lọt bịa" mà là **"đánh oan nút thật"** (K2) vì VH thiếu nhãn — OCR vá được một nửa (OCR), còn fallback thì thay nút-thật bằng câu circular (VIỆC1). **Sửa kỹ thuật thì làm được (trọng tài đa tầng). Nhưng có một điều lớn hơn kỹ thuật cần thầy quyết.**

---

## 2. ĐIỂM QUYẾT ĐỊNH LỚN NHẤT — tiền đề "lọc bỏ bịa" có còn đứng không?

Cả thiết kế dựa trên giả định: *teacher (gpt-4o-mini) bịa nhiều (~¼ số bước), ta lọc bỏ, dạy học trò phần sạch → học trò trung thực hơn.*

**K2 cho thấy giả định này có thể sai trên dữ liệu thật:** teacher bịa **rất ít (~0-2%)**. Con số "~¼" cũ nhiều khả năng là **kết-oan** (nút thật VH thiếu nhãn) bị đọc nhầm thành bịa.

**Hệ quả nếu đúng:** teacher gần như không bịa → tập data-lọc và data-thô **gần như giống nhau** → **Tier 1 (lọc vs thô) có nguy cơ null vì lý do tầm thường** — chẳng có gì để lọc. Đây là nghi ngờ số 5 (đã ghi report/65), giờ có số.

**Ba hướng gỡ (cần thầy chọn):**
- **(a) Đo lại cho chắc:** sửa matcher (OCR) rồi đo bịa thật trên mẫu RỘNG hơn (nhiều miền app, câu hỏi khó hơn). Có thể miền khác teacher bịa nhiều hơn — chưa kết luận vội từ 80 màn một miền.
- **(b) Tăng độ khó để CÓ bịa mà lọc:** teacher yếu hơn / câu hỏi mơ hồ hơn / app lạ hơn.
- **(c) Đổi khung đóng góp:** nếu bịa vốn ít, nhấn *"giữ được độ ĐÚNG khi chưng cất xuống model 3B chạy on-device"* thay vì *"lọc bỏ bịa"*. Đây là chỗ **trục ĐÚNG (AndroidControl gold, report/71)** trở nên đáng giá — vì nó đo được cái đáng đo khi bịa không phải vấn đề chính.

---

## 3. Vấn đề kỹ thuật (sửa được, báo cáo để thầy yên tâm)

**Bộ lọc hiện tại có thể LÀM HẠI data**, không phải làm sạch: nó đánh oan ~31% bước (nút thật) thành bịa rồi viết-lại thành câu mơ hồ. Phải sửa TRƯỚC khi build data.

**Cách sửa (trọng tài đa tầng):** so-chuỗi → nhãn VH → OCR-chặt → từ-điển-ký-hiệu (`+`→add, `✓`→confirm, `✕`→close) → mới coi là bịa. Đã đo: đưa "nút thật khớp được" từ 74% lên ~80%; ~20% icon hình thuần còn lại phải khai như giới hạn.

**Fallback:** vá ngữ pháp (cắt động-từ-mệnh-lệnh dẫn đầu) + thêm chỉ-vị-trí + 10 biến thể; nhưng quan trọng nhất là **fallback ít đi** nhờ matcher tốt hơn.

---

## 4. Bốn câu hỏi cho thầy (từ report/71, giờ có số hậu thuẫn)

1. **Tiền đề "lọc bỏ bịa":** với bằng chứng teacher bịa ~0-2%, thầy muốn đi hướng (a) đo lại rộng hơn, (b) tăng độ khó, hay (c) đổi khung sang "giữ độ đúng on-device"?
2. **Trục ĐÚNG (AndroidControl gold, report/71):** có cho thêm ở vai phụ + khai exploratory không? (giờ đáng giá hơn vì nó đo được cái quan trọng khi bịa không phải vấn đề chính)
3. **Đánh giá người cho fallback:** dừng ở đọc-tay (đã làm) hay nâng thành mẫu-người-nhỏ có κ?
4. **Chấp nhận rủi ro Tier 1/Tier 2 null** và cách trình bày negative-result trung thực?

---

## 5. Việc SAU khi gặp thầy (không làm trước)

- Ghép trọng tài đa tầng (so-chuỗi + OCR + từ-điển-icon) vào bước lọc → đo lại kết-oan tụt bao nhiêu.
- Đo lại bịa thật trên mẫu rộng (quyết theo hướng thầy chọn ở câu 1).
- Rồi mới: pilot MDE → điền report/56 → build data → train.

> **Nguyên tắc giữ vững:** đừng gọi API/GPU tốn tiền để build/train TRƯỚC khi chốt với thầy hướng đi ở mục 2 — vì nếu đổi khung (hướng c) thì bộ thí nghiệm và cả pre-registration thay đổi. 4 phép thử free vừa rồi tồn tại chính để tránh đổ tiền nhầm hướng.
