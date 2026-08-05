# 95 — Các "thành phần" ứng viên cho trụ mô hình (21/7/2026)

> Kết quả workflow đối kháng (5 góc sinh ý tưởng có web-search → gộp 12 → mỗi ứng viên bị một người phản biện cố giết theo 5 ràng buộc). 25 ý thô → 11 sống, 1 giết. Bổ sung cho 3 ứng viên đã có ở report/93. Việc CHỌN vẫn để **Cổng B** (đo mô hình yếu ở đâu) quyết.

## Phát hiện lớn nhất (quan trọng hơn bản thân danh sách)

**Họ mạnh nhất = TỰ-CẢI-THIỆN bằng tín hiệu cấu trúc (bộ-trỏ + toạ-độ gold + VH), KHÔNG bằng gpt-4o.** Đây là họ duy nhất **hợp pháp claim "vượt gpt-4o"** — vì tín hiệu học là *toạ-độ-đúng-của-người*, không phải bắt chước output gpt-4o (né được trần bắt chước). Ba biến thể: RFT/STaR (nướng offline vào trọng số), self-DPO/KTO/ORPO (preference), best-of-N (lúc suy luận).

**NHƯNG cả họ này dính CHUNG một bẫy — và mọi người phản biện đều tự chỉ ra:** **CIRCULARITY / "dạy để thi".** Nếu dùng bộ-trỏ + VH để *huấn luyện* (lọc/reward), rồi lại dùng bộ-trỏ + VH để *chấm* → con số executability lên là **hiển nhiên**, không phải năng lực thật. Hội đồng đập ngay.

> **Điều kiện SỐNG-CÒN nếu đi họ này (bắt buộc, không thương lượng):**
> 1. **Bộ-trỏ dùng để TRAIN phải KHÁC bộ-trỏ dùng để EVAL** (khác họ / khác checkpoint / khác ngưỡng) — đúng tinh thần "nomic lọc, bge-m3 chấm" mà luận văn vốn theo.
> 2. **Thêm một thước thứ ba NGOÀI reward** (LLM-judge hữu-ích khác-họ, hoặc vài chục mẫu chấm tay) — nếu executability lên mà thước này tụt thì thành phần **phản mục tiêu**.
> 3. **Đối trọng "hữu-ích-cho-người":** tối ưu executability có thể đẩy câu về dạng *nhãn-action cộc lốc* (dễ cho bộ-trỏ, tệ cho người đọc) → phải canh, vì đề tài là hướng-dẫn-cho-NGƯỜI.

Bẫy này đúng loại đã làm mình đau (thước "đậu" rồi sập). Workflow bắt được nó **trước khi** build — đó là giá trị chính.

## Bảng ứng viên sống (xếp theo điểm phản biện)

| Điểm | Tên | Nhắm | Cơ chế | Ghi chú then chốt |
|---|---|---|---|---|
| **6** | **RFT/STaR tự-lọc offline** — sinh K câu/màn, giữ câu bộ-trỏ+VH duyệt, SFT lại 1-2 vòng | cả hai | train/data | Mạnh nhất: nướng vào trọng số (deploy sạch, không cần module lúc test), né trần bắt chước. Bẫy: circularity + mode-collapse (chốt 1-2 vòng, trộn lại gold). |
| **6** | **Self-DPO** chấm bằng bộ-trỏ+gold-coord | cả hai | train | Nâng executability mạnh nhất, nhưng circularity nặng nhất + reward-hack (viết mơ hồ cho bộ-trỏ dễ khớp). |
| 5.5 | **KTO/ORPO** nhãn nhị phân, nhẹ VRAM (T4) | cả hai | train | Bản rẻ của self-DPO (~2 tuần), bỏ reference model. Cùng bẫy tautology. |
| 5.5 | **Best-of-N** rerank bằng trọng-tài ĐỘC LẬP | cả hai | inference | Thuần suy luận (~1 tuần), không train thêm. Delta phần lớn cơ học; phải thêm baseline "chọn ngẫu nhiên" để tách. |
| 5 | **Đầu phụ hồi-quy toạ-độ** (multi-task như SeeClick) | cả hai | kiến trúc | Thêm một loss lúc train. Rủi ro NULL cao (multi-task không đảm bảo cải thiện đầu-sinh-text). Phải strip toạ-độ khỏi output trước khi chấm. |
| 4.5 | **DPO âm-bản-bịa đúc tất định từ VH** | faithfulness | train | Cặp preference sinh bằng chương trình (chosen=gold, rejected=đổi tên nút thật→tên vắng mặt). Rẻ, tất định, nhắm thẳng bịa. |
| 4 | Data template-từ-VH trên màn không-gold (mở độ phủ app) | faithfulness | data | Mở rộng độ phủ, không dính gpt-4o. |
| 4 | Giải mã ràng-buộc theo OCR-màn + ép fallback khi icon | faithfulness | inference | Ép tên nút phải là chuỗi OCR thấy trên màn. |
| 4 | Sinh tự-nhất-quán — bỏ phiếu trắng tên nút thiếu đồng thuận | faithfulness | inference | Lấy K mẫu, tên nút không đồng thuận thì hạ-cấp thành mô tả. |
| 3 | Curriculum dễ→khó theo độ-khó-grounding | executability | data | Sắp data nhãn-chữ → icon → nhập-nhằng. |
| 3 | Tái cân-bằng loại-thao-tác + tăng cường icon | cả hai | data | Upsample nút icon + thao-tác-không-click (chỗ gold lệch). |

## Bị giết (1)

- **Zoom coarse-to-fine** (dự đoán vùng thô → crop → đọc tinh icon): **scoop dày** — ZoomIn/V\*/SEAL và cả loạt bài GUI 2025-26 (Zoom-in-Click-out, InnerZoom, MEGA-GUI, GUI-ARP, CropVLM) đã làm nguyên si. Chỉ khai được "áp dụng", không claim mới.

## Lưu ý scoop cho CẢ họ tự-cải-thiện (khai thẳng, đừng giấu)

Cơ chế RFT/RLVR-point-in-bbox đã có nguyên si trên GUI-agent: **UI-R1 (AAAI 2026), SE-GUI (NeurIPS 2025), GUI-R1, UI-Voyager (2603.24533)** — nhưng tất cả cho *trajectory-action / Pass@1*, **chưa ai cho sinh-hướng-dẫn-người**. → Phải kể là **"áp dụng RFT/RLVR vào TÁC VỤ MỚI (sinh hướng-dẫn-cho-người), lọc bằng executability+faithfulness"**; tính mới nằm ở *tác vụ + bộ-lọc-kép*, KHÔNG ở máy móc RFT. Giấu là mất điểm liêm chính.

## Hợp nhất với 3 ứng viên cũ + khuyến nghị

| Nếu Cổng B cho thấy | Ứng viên phù hợp |
|---|---|
| **trỏ kém / câu mơ hồ** (executability thấp) | **RFT tự-lọc (6đ)** nếu kham được bộ-trỏ-eval-độc-lập + thước-thứ-ba; hoặc **best-of-N (5.5đ)** / **vòng kiểm-sửa (cũ #1)** nếu muốn rẻ, thuần suy luận |
| **bịa nút nhiều** (faithfulness thấp) | **DPO âm-bản-bịa-từ-VH (4.5đ)** hoặc **giải mã ràng-buộc OCR (4đ)** — rẻ, nhắm thẳng, ít bẫy circularity hơn |
| cả hai yếu | RFT tự-lọc (nướng cả hai vào trọng số) — nhưng gánh đủ 3 điều kiện sống-còn ở trên |

**Khuyến nghị của tôi:** ứng viên **mạnh nhất về mặt "vượt baseline có chất"** là **RFT tự-lọc offline** — vì nó nướng vào trọng số (deploy sạch), né trần bắt chước, và tận dụng đúng chỗ gold thiếu (mỗi màn nhiều câu đúng mà gold chỉ ghi một). Nhưng nó **chỉ đáng làm nếu** chịu chi cho: bộ-trỏ-eval-độc-lập + một thước hữu-ích thứ ba. Nếu Cổng B cho thấy vấn đề chính là **bịa nút** (rẻ hơn, ít bẫy), thì đi **DPO âm-bản-VH** trước — an toàn và nhanh hơn cho lịch 7 tuần.

## Hệ quả phải dội ngược vào thiết kế (report/93/94)

Nếu chọn bất kỳ ứng viên họ tự-cải-thiện (RFT/DPO/KTO/best-of-N) → **bộ đánh giá phải có: (a) bộ-trỏ-eval TÁCH khỏi bộ-trỏ-train, (b) một thước hữu-ích thứ ba.** Đây là ràng buộc mới, phải ghi vào pre-register trước khi train.
