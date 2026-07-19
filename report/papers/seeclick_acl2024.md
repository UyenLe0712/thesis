# SeeClick: Harnessing GUI Grounding for Advanced Visual GUI Agents (Cheng et al.)

- **Link:** https://aclanthology.org/2024.acl-long.505/ · arXiv: https://arxiv.org/abs/2401.10935 · ⚠ *xác nhận link anthology trước khi in*
- **Venue/năm:** ACL 2024.
- **Vai trong luận văn:** **nguồn gốc thước "bấm đúng chỗ" (point-in-bbox)** và của **benchmark ScreenSpot** — §5.3.

## 1. Bối cảnh & vấn đề
Muốn một tác nhân (agent) thao tác trên giao diện, nó phải **"grounding"**: từ một mô tả bằng lời (ví dụ "nút gửi") **chỉ ra đúng vị trí pixel** của phần tử đó trên ảnh. SeeClick tập trung nâng năng lực grounding này cho GUI, và để đo nó, họ giới thiệu **benchmark ScreenSpot**.

## 2. Ý tưởng chính (dễ hiểu)
- Huấn luyện mô hình **dự đoán toạ độ (x,y)** của phần tử từ **ảnh + mô tả**, không cần cây giao diện.
- Tạo **ScreenSpot**: tập chỉ dẫn kèm **khung pixel chuẩn** (mobile/desktop/web) để chấm grounding một cách khách quan.
- Cách chấm: điểm dự đoán được coi là **"trúng" nếu nằm trong khung đúng** (point-in-bbox).

## 3. Vì sao quan trọng với luận văn
- Đây là **định nghĩa gốc** của thước *point-in-bbox* mà ta dùng cho "bấm đúng chỗ" (§5.3).
- ScreenSpot (và bản v2 kèm OS-Atlas) là **bộ đối chứng grounding** của ta — có đáp án toạ độ chuẩn.
- Nhắc nhở thiết kế quan trọng: điểm (x,y) phải do **bộ trỏ độc lập** dự đoán từ tên+ảnh, **không** lấy tâm khung đã khớp (nếu lấy tâm → tautology 100%).

## 4. Điểm mạnh & giới hạn
- **Mạnh:** đặt chuẩn đo grounding có bình duyệt (ACL 2024).
- **Giới hạn:** grounding là **trục toạ-độ** — đang cải thiện nhanh theo đời model; KHÁC trục *trung-thực-văn-bản* (vấn đề trung tâm của ta). Ta phải trình bày hai trục tách biệt.

## 5. Dùng refer gì cho bài của tôi
- **Trụ** cho Định nghĩa 5.3 (point-in-bbox / grounding).
- Neo cho **ScreenSpot-v2** làm đối chứng (§3.3).
- Dùng để nhấn: grounding-toạ-độ ≠ faithfulness-văn-bản → tránh bị so lệch trục khi giám khảo hỏi "AI mới grounding tốt rồi".
