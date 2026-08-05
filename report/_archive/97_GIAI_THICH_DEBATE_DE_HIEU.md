# Giải thích kết quả phản biện report/94 — dễ hiểu, kèm ví dụ

> Bản viết lại report/96 (debate về thiết kế report/94) theo hướng dễ đọc: mỗi lỗ đều có một ví dụ cụ thể để thấy VÌ SAO nó là vấn đề. Đọc lại lúc nào cũng hiểu. Ngày: 2026-07-21.

---

## Kết luận một câu

Thiết kế mới (report/94) dùng thước **"executability"** là **bước tiến thật** — nó vá được điểm yếu nặng nhất của bản trước. **Đủ hợp lý để đi tiếp, nhưng chưa "sạch":** còn 4 lỗ đo thật phải sửa, và cả trục đang treo trên một phép thử (Cổng A) chưa chạy.

---

## Nhắc lại: "executability" là gì (cho self-contained)

Thước cũ (của bản trước) so **chữ**: câu mô hình nói có trùng chữ với đáp án không. Nó hỏng vì "funnel icon" và "Filter button" khác chữ nhưng cùng là một nút.

Thước mới **executability** không so chữ, mà hỏi: *"câu này có đủ rõ để lần ra đúng nút không?"* Cách làm:
1. Đưa **chỉ câu hướng dẫn** (giấu mục tiêu) cho một **bộ trỏ** (grounder) — một mô hình nhận *ảnh + câu* rồi chỉ ra **điểm (x, y)** nên chạm.
2. So điểm đó với **toạ độ đúng** có sẵn. Cách ≤ 14% cạnh màn (~151 pixel) = **trúng**.

> **Ví dụ progress — vì sao thước mới hơn thước cũ:**
> Đáp án = "Tap the **Filter** button". Mô hình A nói *"Tap the funnel icon"*, mô hình B nói *"Tap Filter"*.
> - Thước cũ: "funnel icon" không trùng chữ "Filter button" → chấm SAI (oan).
> - Thước mới: đưa cả hai câu cho bộ trỏ → cả hai đều trỏ về ~(855, 2273) = đúng chỗ nút Filter → **cả hai ĐÚNG**.
> → Thước mới thưởng *"đủ rõ để lần ra"*, không thưởng *"nói giống chữ đáp án"*. Đây là cái vá quan trọng nhất.

---

## BỐN LỖI THẬT còn lại (mỗi lỗ một ví dụ)

### Lỗ 1 — Mù với đảo nghĩa Bật/Tắt

**Vấn đề:** nút công-tắc (toggle) chỉ có một chỗ bấm; "Bật" và "Tắt" **cùng một toạ độ**. Thước chỉ kiểm "có trỏ trúng chỗ không", nên nó chấm ĐÚNG cho cả câu ngược nghĩa.

> **Ví dụ:** màn Cài đặt có công tắc Thông báo ở điểm (500, 800).
> - Đáp án bước này = *"TẮT thông báo"*.
> - Mô hình nói nhầm = *"BẬT thông báo"*.
> - Cả "bật" lẫn "tắt" đều là *chạm vào công tắc* ở (500, 800) → bộ trỏ trỏ trúng (500,800) cho cả hai → thước chấm **cả hai ĐÚNG**.
> - Nhưng một câu là **ngược hẳn** việc cần làm. Thước không phân biệt được.
>
> **Vì sao nguy hiểm:** nó **thổi phồng điểm** (câu sai vẫn được tính đúng), và kiểu lỗi này *không tự triệt tiêu* khi so hai mô hình.
>
> **Cách vá:** với nút công-tắc, kiểm thêm *trạng thái đích* (đang bật hay tắt) chứ không chỉ toạ độ; hoặc khai thẳng "thước mù với đảo-nghĩa-toggle" + báo bao nhiêu % bước là toggle.

### Lỗ 2 — Gộp hai loại bước đo khác nhau thành một con số

**Vấn đề:** chỉ **bước CHẠM** mới chấm được bằng bộ trỏ (vì có toạ độ). Các bước **gõ chữ / cuộn / mở app** không có toạ độ → phải chấm bằng cách cũ (so loại-thao-tác + nội dung) — mà cách cũ chính là cái vừa bị chứng minh là hỏng. Nhưng báo cáo gộp tất cả thành một "% đúng" như thể đo cùng một kiểu.

> **Ví dụ:** một tác vụ 5 bước: 3 bước *chạm*, 1 bước *"gõ email"*, 1 bước *"cuộn xuống"*.
> - 3 bước chạm → chấm bằng bộ trỏ (thước mới, tốt).
> - 2 bước còn lại (gõ, cuộn) → rơi về so-khớp kiểu cũ (thước đã bị lật ở phản biện trước).
> - Con số cuối "đúng 4/5 = 80%" **trộn chung** cả hai kiểu → nửa số bước vẫn mang rủi ro của thước cũ, giấu bên trong một con số đẹp.
>
> **Con số thật:** đo trên AndroidControl, **chỉ ~53% bước là chạm** (100 bước chạm trên 188 bước quét). Nghĩa là ~nửa số bước KHÔNG được thước mới bảo chứng.
>
> **Cách vá:** **tách hai con số** — "% chạm đúng (bộ trỏ kiểm)" và "% gõ/cuộn khớp (so-khớp)" — báo riêng, đừng gộp một headline.

### Lỗ 3 — "Bộ trỏ trỏ trúng ≈ người làm theo được" mới là NIỀM TIN, chưa kiểm

**Vấn đề:** cả thước dựa trên giả định *"nếu bộ trỏ lần ra được thì người cũng làm theo được"*. Nhưng **chưa ai kiểm** giả định đó bằng số. Mà đây **đúng là sai lầm của thước cũ**: nó cũng được *khẳng định là đúng*, không kiểm, rồi bị lật. Hai cổng kiểm hiện tại (Cổng A, B) chỉ đo *bộ trỏ có chính xác không*, KHÔNG đo *bộ trỏ có đo đúng thứ người cần không*.

> **Ví dụ (ẩn dụ):** bạn chế một cái thước mới rồi bảo "cái này đo được câu-có-dễ-làm-theo-cho-người". Nhưng bạn **chưa bao giờ đưa cho một người thật** làm thử để xem thước có khớp không. Nếu chỉ tin lời, thì y hệt lúc thước cũ bị lật.
>
> **Cách vá (rẻ, làm ngay):** lấy **91 câu thật đã có sẵn**, cho một người đọc và chấm *"bạn có làm theo được không?"*, rồi so với "bộ trỏ có trỏ trúng không". Nếu hai cái khớp → thước đáng tin. **Đưa bước này VÀO CỔNG, đừng hoãn** — đây là mỏ neo duy nhất cho cả thước.

### Lỗ 4 — Dung sai 14% quá rộng, nuốt mất nửa số bước

**Vấn đề:** cho phép lệch tới 14% cạnh màn (~151 pixel). Trên màn nhiều nút san sát, 151 pixel là **rất rộng** — nút bên cạnh cũng nằm trong đó → câu vớ vẩn/trỏ nhầm nút cạnh vẫn "trúng" nhờ may.

> **Ví dụ:** một thanh công cụ có 5 icon xếp hàng, cách nhau ~100 pixel. Mô hình nói câu mơ hồ, bộ trỏ trỏ lệch 120 pixel sang nút bên cạnh — vẫn nằm trong 151 pixel của đáp án → **chấm ĐÚNG oan**.
>
> **Con số thật đo được:**
> - **55% số bước** có ít nhất một nút khác nằm trong bán kính 151 pixel (đo trên 127 màn MobileViews, dùng VH).
> - **63.2% số bước** có ≥1 nút-nhiễu trong dung sai ±14% — **đo TRỰC TIẾP trên AndroidControl** (76 bước click, nút-proxy = tâm hộp chữ OCR, `harness/ac_density_check.py` · `ac_density_results.json`, 2026-07-21). Đây là **cận DƯỚI**: OCR chỉ thấy nút-có-chữ, icon thuần (+, ✓, mũi tên) không đếm được → mật độ thật còn ≥ số này. Trung vị 24 hộp chữ/màn, 1 nút-nhiễu/bước. → lỗ #4 **không chỉ suy luận nữa; đo được, và trên AndroidControl còn nặng hơn MobileViews**.
> - Bộ trỏ rẻ (gpt-4o-mini) có **lỗi trung vị 0.150 cạnh màn > 0.14 ngưỡng** → ngay cả câu đáp-án-chuẩn cũng **trượt một nửa số lần** (hit ±14% = 51.3%, n=76, `ground_pilot_results.json`) với bộ trỏ này.
>
> **⚠️ TỰ SỬA (2026-07-21, sau khi đo sàn thật):** phần lo "sàn cao → dải động bị nén" ở trên **SAI — đo ra thì ngược lại.** Cho grounder gpt-4o-mini nhìn ảnh mà **KHÔNG đưa câu** (đoán bừa nút dễ-bấm-nhất), nó chỉ trúng ±14% gold **6.6%** số lần (không phải ~30% như report/94 giả định). Trong khi có câu gold thì trúng 51.3%. → **Dải động thật = 51.3 − 6.6 = +44.7 điểm**, RỘNG chứ không nén. Khoảng cách trung vị cũng tách sạch: 0.150 (có câu) so 0.433 (không câu). Nghĩa là câu hướng dẫn **thật sự lái** bộ trỏ từ "bừa" về "sát" — đúng thứ thước cần đo. **Con số "42 điểm" của report/94 hoá ra CÒN THẬN TRỌNG** (họ trừ sàn 30, sàn thật chỉ ~7). (`harness/ground_floor.py` · `ground_floor_results.json`.)
>
> **Vì sao mật độ 63% KHÔNG kéo sàn lên:** trên màn có ~24 hộp chữ, đoán-bừa rơi trúng đúng-CÁI-nút-gold (1 trong 24) vẫn hiếm; mật độ chỉ nói "có nút cạnh", không nói "đoán bừa hay trúng đúng nút đó".
>
> **Cái mật độ 63% VẪN cảnh báo (lỗ còn lại, nhẹ hơn):** không phải sàn, mà là **độ phân giải** — một model dở sinh câu *mơ hồ nhưng đúng hướng* có thể khiến bộ trỏ rơi vào nút-cạnh trong dung sai → được điểm oan khi phân biệt câu-tốt với câu-tàm-tạm. Đây là vấn đề tinh, không phá dải động.
>
> **Cách vá (đã hạ mức):** lỗ #4 xuống **nhẹ**. Vẫn nên (1) báo sàn Exec(∅)=6.6% cạnh hiệu số cho minh bạch (đã đo); (2) để tách câu-tốt/câu-tàm-tạm cho sắc, cân nhắc dung sai chặt hơn hoặc chấm *nút-gần-nhất-đúng* thay *đĩa 151px* — nhưng đây là tinh-chỉnh, không phải lỗi chặn.

---

## Bốn vấn đề PHỤ (nhẹ hơn nhưng nên biết)

### A. Học trò có "lợi thế sân nhà" ngoài chất lượng

Đáp án AndroidControl là câu **ngắn, một-thao-tác-một-bước** (trung bình ~6 từ). Học trò train trên đó học luôn *cách chia bước* của bộ dữ liệu. gpt-4o-mini (không train) viết câu **dài, gộp bước**.

> **Ví dụ:** bước đúng chỉ là *"Chạm Share"*. gpt-4o-mini viết *"Chạm Share rồi chọn Gmail"* (gộp 2 bước). Khi chấm từng-bước, câu gộp không khớp ranh giới một-bước → bị trừ điểm. → một phần "học trò hơn gpt-4o-mini" chỉ là *"học trò thuộc bài chia bước của benchmark"*, không phải *"hướng dẫn tốt hơn"*.
>
> **Cách vá:** dẫn kết luận chính bằng **so học-trò-trơn với học-trò-có-thành-phần** (cùng gốc, sạch); "hơn gpt-4o-mini" chỉ để phụ.

### B. Nếu dùng cơ chế "tự cải thiện" (RFT) → dễ "dạy để thi"

Cơ chế tự-cải-thiện lọc câu tự sinh bằng *"bộ trỏ có trỏ gần toạ-độ-đúng không"*. Mà thước chấm cũng là *"bộ trỏ có trỏ gần toạ-độ-đúng không"* → **cùng một phép thử**. Dạy mô hình vượt đúng cái đem ra chấm = con số đẹp nhưng vô nghĩa.

> **Cách vá:** chọn thành phần **DPO-âm-bản-từ-VH** thay vì RFT — nó train bằng *"tên nút có trong danh sách VH không"*, **khác** với chấm bằng *toạ độ* → không vòng-vo. Rẻ hơn, sạch hơn, và không cần tới hai bộ trỏ.

### C. Trục "trung thực" (faithfulness) yếu lực, đừng trưng như trục thật

Với 12 app, trục này chỉ nhìn thấy khác biệt ≥ **~32 điểm**; mà ngưỡng nguy hiểm là 15-20. Nên nếu khác biệt thật là 10 điểm, nó sẽ ra "không khác gì" — **không phải vì không có khác biệt, mà vì thước quá thô**. report/94 hạ nó xuống trục phụ (đúng) nhưng vẫn trưng công thức + ví dụ như một trục đo thật.

> **Cách vá:** khai thẳng *"trục trung thực chỉ để mô tả, lực yếu (~32 điểm), kết quả rỗng ở đây không kết luận được gì"*.

### D. Ôm quá nhiều việc so với thời gian

Giữ **cả hai bài báo** + RFT + hai bộ trỏ + 3-4 mô hình, làm một mình, ~7 tuần, mà thước vừa phải dựng lại — quá tải.

> **Cách vá:** cắt về bản khả thi — **VCL (tiếng Việt) trước**, thành phần **DPO** (một bộ trỏ), 2-3 mô hình. Quyết bỏ/giữ FAIR **ngay tuần này**.

---

## BA việc RẺ nên làm trước khi tiêu tiền huấn luyện

1. **Đưa nghiên cứu-người 91-cặp vào Cổng** (không để ở bảng, không hoãn) — nối "bộ trỏ trúng" với "người làm theo được". Mỏ neo duy nhất cho cả thước.
2. **Báo sàn Exec(∅) thật + tách con số chạm / gõ-cuộn** — đừng gộp một "% đúng".
3. **Chốt thành phần mặc định = DPO-âm-bản-từ-VH** đem trình thầy (rẻ, tất định, chống-vòng-vo sạch). Đừng bê "menu 11 ứng viên" ra hội đồng — đóng góp trung tâm không nên là một ô trống.

---

## Phần nào CHẮC (có số), phần nào mới SUY LUẬN

**Chắc — đã đo bằng số:**
- Dung sai 151px nuốt **55% số bước** (127 màn MobileViews, VH) **và 63.2% số bước trên AndroidControl** (76 bước click, OCR-proxy — cận dưới; `ac_density_check.py`).
- Bộ trỏ rẻ **lỗi trung vị 0.150 > 0.14** → nửa câu gold cũng trượt (n=76).
- **~53% bước là chạm** (pilot AndroidControl).
- **Sàn Exec(∅) = 6.6%**, dải động thật = **+44.7 điểm** (`ground_floor.py`) → lỗ #4 phần "sàn cao" bị **đo là SAI**; thước có dải động rộng, hiệu số "42 điểm" của report/94 thậm chí còn thận trọng.

**Chưa chắc — mới suy luận, cần chạy thật mới xác nhận:**
- Đảo nghĩa on/off: đúng với toggle-một-nút (phổ biến); UI tách nút riêng thì phân biệt được — chưa chạy bộ trỏ thật.
- ~~Mật độ nút 55%: đo trên MobileViews, chưa đo trực tiếp trên AndroidControl.~~ **ĐÃ ĐO (2026-07-21): 63.2% trên AndroidControl** bằng OCR-proxy (bản nhẹ thiếu bbox nên dùng tâm hộp chữ) — chuyển từ "suy luận" sang "đo được". Vẫn còn suy luận phần **icon thuần** (OCR không thấy) → mật độ thật cao hơn 63.2%; muốn số chính xác tuyệt đối phải tải bản AC gốc có a11y-tree (nặng, chưa cần).
- "Lợi thế sân nhà" cấu trúc: giả thuyết, cần một run gpt-4o-mini teacher-forced trên vài chục tác vụ AC để định lượng.
- Bộ trỏ chuyên (không phải bản rẻ) tốt/tệ ra sao trên câu dài: chưa đo.

---

## Tóm gọn để nhớ

- **Executability = đi đúng hướng**, vá được cái nặng nhất (hết nhạy giọng văn). Công nhận.
- Nhưng **4 lỗ đo còn thật:** (1) mù bật/tắt, (2) gộp chạm với gõ/cuộn, (3) chưa kiểm "bộ trỏ ≈ người", (4) dung sai rộng nuốt nửa số bước.
- **3 việc rẻ** làm executability đủ tư cách làm trụ: kiểm-người-vào-cổng · báo-sàn-thật + tách-số · chốt-DPO-làm-thành-phần.
- Chưa nên coi executability là "đã xong" — cả trục còn treo trên Cổng A (bộ trỏ chuyên) chưa chạy.
