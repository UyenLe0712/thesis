# 205 — PATA C2: kết quả P0 + P1 (25/9/2026) ⇒ DỪNG C2 theo bảng chọn đã khoá

Nguồn kế hoạch: `harness/tai_lieu_2026-09-25/204_…` §4.1–4.2. Runbook: `harness/kaggle_pata_p1.md`.
Tệp thô: `runs/pata/p1/` (`p1_scores.jsonl` · `p1.log` · `p1_run_meta.json` · `p1_ket_qua.json`).
Chi phí: 0 A100, ~1,5 h Kaggle T4 (thêm ~40 phút vì hai tiến trình chạy song song, xem §4).

## 1. P0 — cặp G/D thật (0 GPU): ĐẠT

· `descriptor_label_build.py --out descriptors_trueD.jsonl` thêm `box_neg`… cho 41.099 dòng; **trường cũ lệch 0**,
  `box_neg` = `desc_neg` = 37.663 (91,6%). 204 ghi "≈55,6%" là nhầm với tỉ lệ `hop_le` (22.854/41.099).
· `pata_true_d.py`: **232 cặp eligible / 400 bước val400** (101 episode), ngưỡng 150 ⇒ đạt.
· Audit mù 100 cặp (người gán Uyên, `pata/audit_trueD_lan1/`): chọn đúng G **93/100** [86,3; 96,6] · cả hai đúng
  **1/100** · D không phải widget **5/100** [2,2; 11,2] ⇒ **đạt cả ba cổng lần 1**.

## 2. P1 — likelihood 7 nhánh của speaker S đóng băng (Kaggle T4)

Luật quyết khoá trước trong `pata/p1_decision.json`, sha256 `c9b5990ad4d85689…` (lượt chạy đọc đúng bản này).
Bốn assert trước khi chấm đều đạt (thứ tự lô ≤ 1e-3 · G=D nhân tạo ≤ 1e-5 · token khớp trong họ · không dropout).

| hiệu số (nats/token), n = 231 cặp | mean | lower90 |
|---|---|---|
| ΔL_GD | +0,0045 | +0,0005 |
| ΔL_GR | +0,0119 | +0,0074 |
| ΔH_GD | +0,0038 | −0,0004 |
| ΔH_GR | +0,0122 | +0,0070 |
| Δres_GD | −0,0007 | −0,0019 |
| Δres_GR | +0,0003 | −0,0009 |
| thêm ảnh 2 (H_* − O) | +0,0022 | −0,0002 |

**Directional L không đạt · H không đạt · extra-resolution không đạt ⇒ hàng "vùng không đủ" ⇒ DỪNG C2.**
Không đạt vì **mean(ΔGD) ≈ 0,004, thấp hơn ngưỡng 0,02 gần 5 lần** ở cả hai họ; không phải vì biên KTC.

## 3. Đọc kết quả

· **S phân biệt được vùng liên quan với vùng ngẫu nhiên (G−R dương, cận dưới > 0 ở cả L và H), nhưng KHÔNG phân biệt
  được phần tử đích với phần tử lân cận cùng loại (G−D ≈ 0).** Đúng loại phân biệt mà C2 cần thì không có.
· **Không có lợi ích độ phân giải:** Δres ≈ 0 ⇒ giả thuyết "thiếu pixel" không được ủng hộ; crop từ ảnh gốc không cho
  thêm gì so với crop từ bản đã resize.
· Cộng với C1 (bridge không đổi câu, `194` §5c): cả hai cách đưa thông tin vùng tới speaker (bridge một token · ảnh
  crop thứ hai) đều không đổi được likelihood câu vàng theo hướng G vs D ⇒ chuỗi chẩn đoán âm nhất quán.
· Quy mô: +0,02 nats **mỗi câu** (câu vàng trung vị 7 token) — tỉ số likelihood ~2%.

## 4. Sự cố và độ bền (không đổi quyết định)

· **1 cặp NaN** — (15877, 1) nhánh L_R, tràn fp16 trên T4; sáu nhánh kia của cặp bình thường. `doc` bỏ cả cặp ở mọi
  nhánh (ghép cặp). Không ảnh hưởng ΔGD (hai nhánh G, D của cặp đó hữu hạn).
· **Hai tiến trình chấm song song** (ô Q3 bấm hai lần) ⇒ 26 dòng trùng; hai lần chấm cùng cặp **lệch 0,00** ⇒ thêm
  bằng chứng tất định. `run` nay có khoá PID, `doc` gộp dòng trùng.
· **Lỗi builder bắt được hậu kiểm:** 20/231 cặp có cửa sổ G và D **trùng nhau** (cửa sổ cạnh = cả bề ngang bị đẩy vào
  mép màn) ⇒ đóng góp 0. Bỏ 20 cặp đó: ΔL_GD +0,0049 [+0,0007], ΔH_GD +0,0041 [−0,0004] — vẫn thấp hơn 0,02 gần 5 lần.

## 5. Hậu kiểm theo nhóm — CHỈ để hiểu, ⛔ không dùng để mở lại C2

| nhóm | n | ΔL_GD | ΔH_GD |
|---|---|---|---|
| cạnh cửa sổ ≤ 400 px | 115 | +0,0095 [+0,0023] | +0,0083 [+0,0009] |
| cạnh cửa sổ > 400 px | 116 | −0,0004 | −0,0007 |
| IoU cửa sổ G/D < 0,2 | 30 | +0,0158 [+0,0039] | +0,0106 |

Tín hiệu G−D chỉ xuất hiện ở phần tử nhỏ / cửa sổ ít chồng, và ngay ở nhóm thuận lợi nhất vẫn dưới ngưỡng 0,02. Nhóm
chọn sau khi thấy số ⇒ không phải căn cứ.

## 6. Giới hạn phải khai

P1 đo speaker S **đóng băng**, vốn chỉ được dạy với **một** ảnh; ảnh 2 là đầu vào ngoài phân phối. Kết quả nói S hiện có
không mang thông tin phân biệt G/D từ bằng chứng vùng; nó **không** chứng minh một mô hình được huấn luyện dual-view
không học được. Thiết kế 204 cố ý khoá như vậy (đo rẻ trước khi code); muốn thử dual-view có huấn luyện là một **quyết
định mới**, không phải cứu kết quả này.

## 7. Trạng thái

· Không C0-Loc, không P1b/P2, không A100, test vẫn đóng. Tiêu đề luận văn không đổi.
· Việc còn lại: đưa chuỗi chẩn đoán âm của PATA (localizer học được vị trí → bridge không đổi câu → bằng chứng vùng
  không phân biệt G/D) vào luận văn nếu user muốn.
