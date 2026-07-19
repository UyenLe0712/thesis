# ScreenSpot-v2 / OS-Atlas: A Foundation Action Model for GUI Agents

- **Link:** https://arxiv.org/abs/2410.23218 (OS-Atlas; kèm ScreenSpot-v2)
- **Venue/năm:** **ICLR 2025**. Giấy phép **apache-2.0**. (Gốc ScreenSpot từ SeeClick, ACL 2024.)
- **Vai trong luận văn:** **đối chứng grounding** (định vị nút từ mô tả) + bù độ tin cậy cho MobileViews (§3.3).

## Paper này nói gì (cho người mới)
ScreenSpot-v2 là bộ chuẩn cho tác vụ **"định vị nút từ mô tả"** (grounding): cho một câu như *"invert the lens"*, mô hình phải chỉ ra **khung pixel** của nút tương ứng. Bản v2 **sửa 11,32% lỗi nhãn** của bản gốc; gồm **1.272 chỉ dẫn** (502 mobile / 334 desktop / 436 web). OS-Atlas là mô hình hành động GUI đi kèm.

## Điểm cần biết
- Có **đáp án toạ độ chuẩn** + **bình duyệt ICLR 2025** → dùng để kiểm **bộ trỏ độc lập** một cách công bằng.
- Giúp tránh **tautology tâm-bbox**: điểm bấm phải do bộ-trỏ-độc-lập dự đoán, không lấy tâm khung đã khớp.
- Chuẩn grounding 2025 = **point-in-GT-bbox** (điểm có nằm trong khung đúng không).

## Dùng refer gì cho bài của tôi
- Nguồn **đối chứng** cho thước "bấm đúng chỗ" (§5.3) — và neo bình duyệt cho chuẩn point-in-bbox.
- Bù **credibility** cho MobileViews (preprint).
- Ví dụ thật `item1` ("invert the lens", app Camera, khung (965,2105,1110,2258)) minh hoạ (§3.3, Hình 3.3).
