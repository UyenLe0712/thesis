# 2 QUYẾT ĐỊNH CẦN CHỐT (đọc 3 phút là quyết được)

> Sau khi review toàn bộ, khung luận văn **đã vững**. Chỉ còn **2 điểm cần bạn quyết** trước khi bắt tay làm thí nghiệm (P2b/P3). Mỗi điểm dưới đây tôi giải thích từ đầu + khuyến nghị. Quyết xong nhắn tôi 1 dòng là được.

---

## QUYẾT ĐỊNH 1 — Cổng "KB" che gì trên ảnh?

### Hiểu trong 30 giây
Ở nhánh đa bước (DG2), ta đưa máy **N tấm ảnh các màn ĐÃ XÁO TRỘN** và bắt máy **xếp lại đúng thứ tự**. Để công bằng, máy phải xếp đúng nhờ **HIỂU giao diện**, chứ không phải **"đọc lén" dấu vết thứ tự còn sót trong ảnh**.

- **Ví dụ "đọc lén" (phải chặn):** ảnh còn dính **đồng hồ điện thoại** (12:01 → 12:02 → 12:03), **tên file** (step1, step2), **metadata thời gian** → máy liếc mấy thứ đó là biết thứ tự ngay, **không cần hiểu gì** → gian lận.
- **Cổng KB** = quy trình bịt mấy kẽ hở đó (xoá metadata, đổi tên ảnh ngẫu nhiên, che đồng hồ/pin trên thanh trạng thái).

### Mâu thuẫn cần gỡ
Một trong **5 manh mối hợp lệ** ta MUỐN máy dùng tên là **state-delta** = "trạng thái đổi giữa các màn": ô trống → đã điền, nút gạt off → on, **con số nhỏ (badge) 0 → 1**. (Màn có ô đã điền thì hợp lý đứng **sau** màn ô còn trống.)

Nhưng cổng KB lại ghi "che ... **badge**" → **cùng chữ "badge"**, KB vô tình xoá đúng manh mối ta cần đo. Phải phân định:
- **badge của HỆ ĐIỀU HÀNH** (số thông báo / đồng hồ / pin trên thanh trạng thái trên cùng) → **nên che** (dấu vết thời gian, không phải nội dung app).
- **badge TRONG APP** (số trên icon giỏ hàng, số tin chưa đọc trong app, ô form, toggle) → **là nội dung, là manh mối hợp lệ, KHÔNG nên che**.

### 3 lựa chọn
| | Làm gì | Được / Mất |
|---|---|---|
| **(A) Chỉ che dấu vết HỆ THỐNG** ⭐ | Che thanh trạng thái OS / đồng hồ / pin / metadata / tên file. **Giữ** mọi thay đổi nội-dung-app (ô form, toggle, badge-trong-app) làm manh mối | Giữ đủ **5 manh mối**; rủi ro "đọc lén" kiểm soát bằng phân tích riêng. **Khuyến nghị** |
| **(B) Che luôn state-delta** | Che cả thay đổi nội-dung-app | Chống leak triệt để nhưng **mất 1/5 manh mối** (còn 4) |
| **(C) Phân biệt badge-OS vs badge-trong-app** | Quy ước: badge trên thanh OS = che; badge trong app = giữ | Linh hoạt nhưng phải định nghĩa kỹ vùng "xám" |

**Khuyến nghị: (A).** Đọc sâu thêm: `report/03_pipeline.md` (mục "Ordering cues" + cổng KB) và `report/05_final_plan.md` mục 5.6.

---

## QUYẾT ĐỊNH 2 — Cắt bớt khối lượng thí nghiệm cho vừa 1 luận văn

### Hiểu trong 30 giây
Kế hoạch hiện cam kết chạy **rất nhiều** thí nghiệm:
- **DG1 (đơn bước) — "thang bậc C0→C4":** chạy hệ ở **5 mức** tăng dần để biết *món nào giúp* — C0 (trần) · C1 (thêm tự-sửa) · C2 (thêm đánh số) · C3 (thêm ép-chọn-số) · C4 (thêm kiểm-ý). Mỗi mức × 500–2000 mẫu × 2 (RAW + ORACLE).
- **DG2 (sắp thứ tự):** ≥30 episode cho **mỗi** độ dài N, N từ 3 đến ~10, × 2 chế độ × 3 baseline.
- Cộng **Tier A** + **pilot người chấm** (60–80) + **audit người** (50–80 cặp) + validate EN/ZH.

→ Tổng ≈ **khối lượng 2–3 bài hội nghị**, vượt sức 1 học viên + ngân sách ~$100–300.
→ Nếu chạy mỏng (< 30 mẫu/mốc) thì kết quả **nhiễu**, kết quả "không khác biệt" (null) **không đọc được** → phá vỡ nguyên tắc *"null vẫn đậu"* (null chỉ có giá trị khi **đủ mẫu**, gọi là **đủ power**).

### 4 lựa chọn
| | Làm gì | Đánh đổi |
|---|---|---|
| **(A) DG2 lõi + DG1 gọn 3 bậc** ⭐ | DG2 đầy đủ; DG1 rút 5→**3 bậc {C1, C3, C4}** (bỏ C0, C2); trục N chỉ **~3 mốc đủ ≥30 episode** (vd N=3,4,5), N dài hơn = thăm dò; Tier A/pilot/audit **quy mô tối thiểu** | Vừa sức + đủ power ở phần lõi. **Khuyến nghị** |
| **(B) Dồn hết vào DG2** | Giữ DG2 đầy đủ; DG1 ablation thành phụ (exploratory) | Mạnh DG2, yếu phần DG1 |
| **(C) Giữ cả hai, chỉ 1 model** | Đầy đủ DG1+DG2 nhưng chỉ chạy **1 model** (Qwen2.5-VL-7B); GPT-4o chỉ demo định tính | Giảm ~½ compute, mất so sánh "đóng vs mở" |
| **(D) Giữ nguyên** | Không cắt gì | Kéo dài thời gian / xin thêm ngân sách |

**Khuyến nghị: (A).** Đọc sâu thêm: `report/05_final_plan.md` (6 pha P0–P4 + thang bậc C0–C4) và `report/00_TONG_QUAN.md` (toàn cảnh).

---

## Bạn đọc file nào để nắm toàn cảnh (nếu muốn)?
1. **`report/00_TONG_QUAN.md`** — đọc-là-hiểu toàn bộ đề tài qua 1 ví dụ xuyên suốt (đọc đầu tiên).
2. **`report/06_de_xuat_chot_scope.md`** — bản trình thầy, giải thích mọi thuật ngữ ngay khi dùng.
3. File này — chỉ 2 quyết định cần chốt.

> Quyết xong, nhắn tôi: *"Q1 chọn A, Q2 chọn A"* (hoặc tuỳ bạn) — tôi áp vào toàn bộ file + slide ngay.
