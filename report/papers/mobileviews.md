# MobileViews: A Large-Scale Mobile GUI Dataset

- **Link:** https://arxiv.org/abs/2409.14337
- **Venue/năm:** **preprint arXiv 2409.14337** (chưa bình duyệt; bản v3 đổi tên "Million-scale"). Giấy phép **MIT**. BUPT + Tsinghua.
- **Vai trong luận văn:** bộ dữ liệu cho **nhánh MỘT MÀN** (§3.1).

## Paper này nói gì (cho người mới)
Đây là một **kho ảnh chụp màn hình app Android** rất lớn, mỗi ảnh **đi kèm cây phân cấp giao diện (View Hierarchy)** — tức có sẵn danh sách nút thật + toạ độ. Bản công bố nêu **~1,2 triệu** cặp; bản công khai thực tế **~600 nghìn**. Dữ liệu **thu thập tự động bằng bot** (VLM điều khiển DroidBot dò app). **KHÔNG có quỹ đạo thao tác** — chỉ là màn tĩnh.

## Điểm cần biết
- Có **VH** → dùng làm "nguồn sự-thật" để đối chiếu (nhãn bạc), không có gold trajectory.
- Là **preprint + thu-thập-tự-động** → độ tin cậy thấp hơn bộ bình duyệt → ta bù bằng **ScreenSpot-v2**.
- Cấu trúc file: `width/height`, `foreground_activity`, `views` (mỗi phần tử có `class` + `bounds` `[[x1,y1],[x2,y2]]`).
- ⚠ Có **lệch khung toạ độ** ảnh↔VH → phải hiệu chỉnh trước khi tính grounding (report/44 §8).

## Dùng refer gì cho bài của tôi
- Nguồn cho **81 màn / 17 app** (lọc từ 90/18) ở nhánh một màn.
- Vì là preprint → trong bài **khai thẳng** trạng thái + lý do bù bằng bộ bình duyệt.
- Minh hoạ nút icon-only "Image" (thiếu nhãn) → nối Chen ICSE 2020.
