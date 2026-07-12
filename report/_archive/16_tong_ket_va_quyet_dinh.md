# 📋 TỔNG KẾT ĐÃ LÀM GÌ + ƯU/NHƯỢC + ĐI TIẾP ĐƯỢC KHÔNG + QUYẾT ĐỊNH CẦN BẠN DUYỆT

> **File này để làm gì?** Đọc một file này là biết: (1) **đã làm những gì** từ đầu tới giờ, (2) pipeline đề xuất **ưu/nhược** ra sao, (3) **đi tiếp được với pipeline này không hay phải nghiên cứu cái khác**, (4) **bạn cần review + quyết gì**. Viết cho người **chưa biết gì** — mọi từ chuyên môn giải thích ngay.
> *(Chi tiết kỹ thuật: thiết kế `report/14`, kết quả chạy thử `report/15`, bản dễ hiểu toàn cảnh `report/00_DOC_TU_DAU`.)*

---

## PHẦN 1 — ĐÃ LÀM GÌ NÃY GIỜ (kể lại dễ hiểu)

**Bối cảnh:** đề tài = *từ ảnh màn hình + câu hỏi → máy viết hướng dẫn bấm từng bước*, kèm cách tự chấm điểm khi không có "bài mẫu chuẩn". Thầy đã **duyệt 3 bộ dữ liệu** (MobileViews, AndroidControl, ScreenSpot) và yêu cầu **tìm hiểu thật kỹ pipeline + cách chấm**.

Các việc đã làm, theo thứ tự:

1. **Nghiên cứu lại pipeline + metric (deep-research, nhiều "trợ lý AI" rà song song).** Phát hiện: thiết kế cũ (bắt một "bộ dò nút" chạy TRƯỚC rồi ép model chỉ được nhắc nút bộ dò thấy) **dễ lỗi** — nếu bộ dò sót nút thì hướng dẫn bị thiếu.

2. **Cập nhật kiến thức 2026 (đã có GPT-5, Gemini-3).** Kết luận quan trọng (từ bài bình duyệt): **các model mạnh nhất 2026 VẪN bịa nút, vẫn đặt sai vị trí, vẫn quá tự tin** → còn chỗ cho một "lớp làm cho trung thực".

3. **Chốt thiết kế cuối "design E"** (xem Phần 2) + 3 quyết định: dùng model có sẵn (không huấn luyện lại), bộ sinh lõi là **Qwen mở**.

4. **Chạy thử THẬT trên chính máy này — miễn phí, không cần GPU** (dùng Ollama chạy CPU). Ba lần:
   - **Lần 1 (3 màn, câu hỏi tôi tự soạn khớp màn):** faithfulness 91.7% — nhưng câu hỏi "dẫn dắt".
   - **Lần 2 (10 màn, câu hỏi CHUNG):** faithfulness tụt còn 59.3%, model bịa 40.7% → **bài học: chất lượng câu hỏi chi phối tất cả.**
   - **Lần 3 (10 màn, đổi sang model 7B):** faithfulness lên 75%, bịa giảm còn 25% → **model mạnh hơn bịa ít hơn.**
   - Mọi lần đều cho thấy: **lớp "fallback" của hệ biến mọi "lệnh bấm nút sai mà tự tin" thành mô tả trung thực (về 0%).**

> *Giải thích nhanh vài từ:* **faithfulness** = tỉ lệ không bịa (cao = tốt). **confident-wrong / lệnh-sai-tự-tin** = bước chỉ người dùng bấm một nút KHÔNG có trên màn (tệ nhất). **fallback** = khi không tìm thấy nút, hệ chuyển sang mô tả bằng lời thay vì bịa. **oracle** = bộ tra cứu đáng tin (ở đây là danh sách nút thật của màn), chỉ dùng lúc chấm.

---

## PHẦN 2 — PIPELINE ĐỀ XUẤT (design E) — nhắc gọn
"Lớp làm-cho-trung-thực, độc lập với model":
1. **Bộ viết** = model mạnh nhất, **thay được** (Qwen mở; sau này cắm GPT-5/Gemini-3) → viết hướng dẫn **gọi nút theo TÊN**.
2. **Oracle** (danh sách nút thật) đặt **bên cạnh**, kiểm "nút này có thật không, ở đâu" — **không chặn** việc viết.
3. **Fallback**: nút không khớp → mô tả bằng lời (không bỏ bước, không bịa).
4. Cách chấm: **không bịa (faithfulness) + đủ ý (coverage) + làm-theo-được (Step-SR) + (đa ảnh) xếp đúng thứ tự**.

---

## PHẦN 3 — KẾT QUẢ CHẠY THỬ (bảng) + ý nghĩa

| | Qwen 3B | Qwen 7B |
|---|---|---|
| faithfulness (không bịa) | 59.3% | **75.0%** |
| lệnh-sai-tự-tin (raw) | 40.7% | **25.0%** |
| sau khi hệ áp fallback | **0%** | **0%** |

**Ý nghĩa (quan trọng):**
- Thước đo **NHẠY** — phân biệt được model tốt/dở (3B vs 7B) → metric "có răng", đáng tin về mặt phân biệt.
- Hệ **chạy được thật, miễn phí, không GPU** → tính khả thi cao.
- Lớp fallback **có giá trị đo được** (xoá lệnh-sai-tự-tin) và **hành xử đúng lý thuyết** (model càng mạnh, fallback cứu càng ít — 40.7%→25% — nhưng không bao giờ về 0 vì model vẫn bịa).

---

## PHẦN 4 — ƯU ĐIỂM
1. ✅ **Khả thi cao:** đã chứng minh chạy được end-to-end **miễn phí trên CPU**; không bắt buộc GPU đắt.
2. ✅ **Không lỗi thời:** đóng góp nằm ở **cái lớp + cách chấm**, model là mảnh thay được → GPT-6 ra chỉ làm số đẹp hơn.
3. ✅ **Thước đo nhạy + bắt lỗi đúng + có lá chắn chống gian lận** (đo coverage để model không "viết ít cho khỏi sai").
4. ✅ **Cơ chế hệ có giá trị thật, đo được** (fallback) và khớp dự đoán nghiên cứu 2026.
5. ✅ **Nền lý thuyết vững** (bài bình duyệt 2026: frontier vẫn bịa → đề tài có đất).
6. ✅ **An toàn ("null vẫn đậu"):** kể cả kết quả không đẹp, nếu đăng ký trước thì vẫn là đóng góp.

## PHẦN 5 — NHƯỢC ĐIỂM / HẠN CHẾ (nói thẳng)
1. ⚠️ **Không phá kỷ lục thế giới** (không claim SOTA) — chấp nhận có chủ ý; thắng ở trục hẹp (trung thực/đúng-chỗ/làm-theo).
2. ⚠️ **Kết quả CỰC nhạy với chất lượng câu hỏi** (91.7% vs 59.3%) → bắt buộc đầu tư **giao thức câu hỏi tử tế**.
3. ⚠️ **Vẫn phụ thuộc oracle/danh-sách-nút** (recall): design E giảm nhẹ nhưng vẫn phải đo "bộ dò sót bao nhiêu" (cổng K1).
4. ⚠️ **Coverage trên MobileViews chỉ là tương đối** (không có "bài mẫu" để biết nút nào cần) → đo **làm-theo-được (Step-SR)** phải dựa **AndroidControl** (có đáp án vàng).
5. ⚠️ **Matcher (khớp tên) còn yếu** (đang khớp chuỗi) → con số "bịa thật" chưa chắc; cần nâng **ALOHa** + **người kiểm tay** một ít.
6. ⚠️ **Máy hiện tại không có GPU** → chạy quy mô lớn cần **GPU thật / thuê cloud / hoặc một ít tiền API**.
7. ⚠️ **Giá trị lớp bọc giảm khi model mạnh lên** (vẫn dương) → phải đóng khung trung thực, đừng overclaim.

---

## PHẦN 6 — ❓ CÂU HỎI LỚN: ĐI TIẾP VỚI PIPELINE NÀY ĐƯỢC KHÔNG, HAY PHẢI NGHIÊN CỨU CÁI KHÁC?

### ✅ TRẢ LỜI: **ĐI ĐƯỢC với pipeline đã đề xuất (design E). KHÔNG cần nghiên cứu pipeline khác.**

**Lý do (dựa trên bằng chứng vừa chạy, không phải cảm tính):**
- Pipeline **đã chạy thật end-to-end** trên dữ liệu + model thật → không có lỗi kiến trúc chí mạng.
- Thước đo **nhạy và bắt lỗi đúng** → bộ đánh giá (đóng góp chính) **hoạt động**.
- Cơ chế hệ (fallback) **cho giá trị đo được + đúng lý thuyết** → phần hệ thống **có ý nghĩa**.
- Thiết kế đã được **nghiên cứu lại theo literature 2026** (không phải bản cũ lỗi thời).
- Các nhược điểm còn lại đều là **chuyện TINH CHỈNH / MỞ RỘNG** (câu hỏi, matcher, dữ liệu, model, hạ tầng) — **KHÔNG phải lỗi thiết kế** → sửa được mà không đổi pipeline.

### Khi nào MỚI phải xem lại pipeline? (điều kiện rõ ràng, để theo dõi)
- Nếu **đã** dùng câu hỏi tốt + model mạnh + matcher ALOHa mà **vẫn KHÔNG** thấy hệ cải thiện gì so với "viết tự do" **VÀ** không đo được trật tự (τ-b) → khi đó phần "hệ thống" yếu (nhưng **đóng góp đánh giá vẫn đứng**).
- Nếu hoá ra frontier model **ground hoàn hảo, không bịa gì** → giá trị fallback ≈ 0 (nhưng bằng chứng 2026 nói **chưa** xảy ra).
→ Đây là **điều cần theo dõi**, **không phải** lý do đổi pipeline bây giờ.

> **Tóm gọn:** lần chạy thử đã **gỡ rủi ro** cho pipeline. Việc còn lại là **làm cho số đáng tin + quy mô lớn**, không phải vẽ lại pipeline.

---

## PHẦN 7 — 🟦 NHỮNG GÌ CẦN BẠN REVIEW + QUYẾT ĐỊNH

Mỗi mục có **khuyến nghị** — bạn chỉ cần đồng ý hoặc đổi.

**① Phán quyết chính:** đồng ý **đi tiếp với design E, không nghiên cứu pipeline khác**?
🔹 *Khuyến nghị: ĐỒNG Ý* (đã gỡ rủi ro qua 3 lần chạy).

**② Giao thức câu hỏi use-case** (vì câu hỏi chi phối kết quả): ai soạn, bao nhiêu câu, tiếng gì, dựa trên gì?
🔹 *Khuyến nghị:* tự soạn theo một **quy trình chuẩn** (mỗi màn 1–2 câu "làm sao để X", có người kiểm); EN làm chính, VN để demo.

**③ Nâng matcher lên ALOHa** (miễn phí qua Ollama-embedding) + **audit người** một ít, để con số "bịa" đáng tin?
🔹 *Khuyến nghị: LÀM* — đây là việc đáng giá nhất tiếp theo, khiến mọi số sau tin được.

**④ Hạ tầng chạy quy mô lớn** (máy này không có GPU): chọn **GPU thật (máy lab) / thuê cloud GPU / một ít tiền API frontier**?
🔹 *Khuyến nghị:* lõi chạy **Qwen open trên GPU thuê/cloud rẻ**; chạy thêm **một ít API GPT-5/Gemini-3** làm đối chứng "model mạnh".

**⑤ Phạm vi lần chạy chính:** bao nhiêu màn / mấy app / có chạy **AndroidControl (Step-SR + xếp thứ tự τ-b)** không?
🔹 *Khuyến nghị:* DG1 vài trăm màn nhiều app + DG2 trên AndroidControl (sau lọc episode); EN chính.

**⑥ Demo tiếng Việt** sớm hay để sau?
🔹 *Khuyến nghị:* để sau (sau khi số EN ổn), chỉ làm demo định tính.

---

## PHẦN 8 — MỘT DÒNG TÓM TẮT
**Đã chạy thử thật (miễn phí, CPU) 3 lần → chứng minh pipeline design E CHẠY ĐƯỢC, thước đo NHẠY và bắt lỗi đúng, cơ chế hệ CÓ GIÁ TRỊ đo được và đúng lý thuyết → KẾT LUẬN: ĐI TIẾP ĐƯỢC với pipeline đề xuất, KHÔNG cần nghiên cứu cái khác; việc còn lại là làm số đáng tin (câu hỏi tốt + ALOHa + audit) và chạy quy mô lớn (cần GPU/API).**
