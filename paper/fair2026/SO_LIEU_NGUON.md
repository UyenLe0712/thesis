# Truy vết số liệu — mỗi con số trong `main.tex` lấy từ đâu

> Mục đích: khi thầy hoặc phản biện hỏi "số này ở đâu ra", mở file này là ra ngay.
> Nguyên tắc đã áp: **không con số nào lấy từ trí nhớ, không con số nào suy ra**.
> Số nào nằm trong danh sách bị rút của `report/108` mục 9 thì **không xuất hiện**
> trong bài — xem mục cuối file.

## 1. Dữ liệu (mục III của bài)

| Số trong bài | Giá trị | Nguồn |
|---|---|---|
| Bước tập dạy | 64.567 | `report/110` mục 2 |
| Bước chạm tập dạy | 41.191 (63,8%) | `report/110` mục 2 |
| Tác vụ tập dạy | 12.895 | `report/110` mục 2 |
| Ảnh thiếu | 0 | `report/110` mục 2 |
| Bước tập kiểm | 6.958 | `report/110` mục 2 + ô 0.11d |
| Bước chạm tập kiểm | 4.463 (64,1%) | `report/108` mục 2.2 · `report/110` ô 0.11d |
| Tác vụ tập kiểm | 1.432 | `report/108` mục 2.2 |
| Rò rỉ tác vụ dạy↔kiểm | 0 | `report/110` ô 0.11b — **lần đầu kiểm ở quy mô đủ** |
| Phủ OCR tập dạy | 100,00%, thiếu 0 | `report/110` mục 3 tầng 1 |
| Phủ nhãn khai báo tập dạy | 41.099/41.191 = 99,8% | `report/110` mục 4 |
| Phủ nhãn khai báo tập kiểm | 99,7% | `report/106` sửa đổi 9/8 (m) · `report/110` ô 0.11d |
| Gán được app (tập kiểm) | 45,0% · 269 app · 3.828 không gán được | `report/110` mục 2 |
| Kiểm phép ghép n=400 | 48% vs 20% = 2,4× | `report/110` ô 0.11c |
| Kiểm phép ghép n=60 | 47% vs 27% = 1,74× | `report/110` ô 0.11c |
| OCR chữ/màn kiểm chéo máy | 24,2 (kiểm) vs 23,6 (dạy), trung vị 22 cả hai, 0,1% màn rỗng | `report/110` mục 3 tầng 2 |
| Lệch OCR giữa hai máy | 2,5% | `report/110` mục 3 |
| Cây trợ năng có tên | 12,6% phần tử / 99.131 màn | `report/108` mục 7 |
| Nhãn trợ năng là rác | 14,7% tại nút đích | `report/108` mục 7 · `report/106` sửa đổi 5/8 |
| Cổng hình học OCR | 25 ca hộp >25% màn, 0/25 khớp câu chuẩn | `report/106` sửa đổi 5/8 |
| Nhãn ở quy mô đủ | tên rõ 73,6% (trợ năng 8.581 · OCR 23.480) · ký hiệu 4,4% · không tên 22,0% · vai trò rõ 75,8% · trùng tên 7,6% · có hàng xóm 91,6% | `report/110` mục 4 |
| Ô thứ tư bản đầu | 85,8% chỉ đếm · 7,3% gỡ được | `report/106` sửa đổi 6/8 (e2), đếm trên 1.074 nhãn |
| Ô thứ tư bản dùng | gỡ được 75,9% | `report/106` sửa đổi 6/8 (f1) · `report/108` mục 3.1 |
| Hướng mỏ neo | 737/737 đúng | `report/108` mục 3.1 |
| Ghép độ dài S2r | 99,3% cặp ≤2 token, biên −3/+6 | `report/106` sửa đổi 6/8 (f2) |
| 9 bất biến | 9/9 trên 64.567 mẫu/nhánh, 41.099 nhãn | `report/110` ô 0.11 |

⚠️ **Chỗ trộn hai quy mô, phải nhớ:** các số về *ô dấu hiệu phân biệt* (85,8% → 75,9%,
737/737, 14,7% rác) đo trên **lát 1.697 bước / 1.074 nhãn**; các số về phân bố nhãn
(73,6% tên rõ…) đo ở **quy mô đủ 41.191 bước**. Bài đã ghi rõ "pilot slice" ở chỗ đầu.

## 2. Thước đo (mục IV của bài)

| Số trong bài | Giá trị | Nguồn |
|---|---|---|
| Bảng chọn luật chấm (250 bước) | 0%: 100/100/100 · 3%: 100/99,7/78,6 · 5%: 100/93,3/44,6 · 8%: 100/74,4/20,3 · SÀN: 84,3/2,8/4,8 | `report/106` sửa đổi 6/8 (b) |
| Cổng A — sai số trung vị | 0,7% bề ngang, ngưỡng 3% | `report/106` sửa đổi 9/8 (a) · `report/108` mục 13.1 |
| Cổng A — phân vị | p10 0,1 · p25 0,2 · p50 0,7 · p75 9,1 · p90 36,3 · ≤3% ở 62,7% | như trên |
| Bộ trỏ, số bước | 300, hạt giống 20260805, UGround-V1-2B | như trên |
| Dấu hiệu "x giữa màn" | kêu 30,7% (ngưỡng 20%) → truy ra 15,3% số bước | `report/106` sửa đổi 9/8 (b) |
| Bảng 2×2 | chuẩn ở giữa 18,3% · 46/245 bước chuẩn-không-giữa vẫn bị trỏ giữa · ~45% số lần trượt | như trên |
| **Trần thước** | Voronoi **70,0%** KTC95 [64,5; 75,3] · đĩa 81,3% [76,6; 86,0] | `report/106` sửa đổi 9/8 (c) |
| Cụm của mẫu 300 | 239 (hiệu dụng 191,5) · trung vị 72 phần tử/màn · 0 màn thiếu cây | như trên |
| Đường cong xác nhận ngưỡng 3% | ≤3% n=188 → 100,0% · 3-5% n=21 → 66,7% · 5-8% n=16 → 43,8% · 8-14% n=12 → 8,3% · >14% n=63 → 0,0% | `report/106` sửa đổi 9/8 (d) |
| Bơm lỗi bản 3 | bảng 10 tiêu chí + cột n, 8/10 | `report/106` sửa đổi 6/8 (c) |
| Ngưỡng mù ~63 px | luật gộp 24dp; nút đích 189×126 px | `report/106` sửa đổi 6/8 (c) · `report/108` mục 7 |
| Hình học màn | nút đích 189×126 px · nút khác gần nhất cách 69 px | `report/108` mục 7 |
| Toạ độ chạm là tâm phần tử | 79,4% trong 1,5 px, trung vị 0,7 px | `report/106` sửa đổi 6/8 (i) |
| Bước không-chạm | 35,9% (cuộn 755 · chờ 505 · gõ 494 · mở app 469 · quay lại 270) | `report/106` sửa đổi 6/8 (h) |
| Luật không-gây-hại | không thấp hơn 3 điểm phần trăm | `report/106` mục 3 |
| Cụm tập kiểm đủ | G=1.091 · G hiệu dụng 454,3 · 259 app · 832 cụm-đơn · cụm lớn nhất 58 | `report/106` sửa đổi 9/8 (f) |
| Luật app-only | G=259 · G hiệu dụng 107 · MDE 12,1 pp | `report/108` mục 7.1 |
| MDE chiếu | 2,8·sd/√G_eff: 0,30→3,9 · 0,40→5,3 · 0,50→6,6 pp | `report/106` sửa đổi 9/8 (f) |
| Cam kết 4–9 pp | báo chưa kết luận được | `report/106` sửa đổi 6/8 (e1) |
| Cache khoá-giá trị | 38,65 s → 4,16 s (32 token, T4); 50/50 trùng tuyệt đối; 48h → 5h | `report/106` sửa đổi 9/8 (e) |

## 3. Mô hình và thiết lập (mục V–VI của bài)

| Số trong bài | Giá trị | Nguồn |
|---|---|---|
| Siêu tham số QLoRA | r=8 · α=16 · dropout 0,05 · 7 mô-đun · đóng băng tháp thị giác + projector · cutoff 2560 · lô 4×4=16 · lr 1e-4 · cosine · warmup 0,05 · 2 epoch · bf16 | `harness/train_config.yaml` |
| Tham số huấn luyện | 14.966.784, tính tay khớp từng chữ số | `report/106` sửa đổi 9/8 (g) · `report/110` ô A.3 |
| Nâng `cutoff_len` | 2048 → 2560, vì s2 dài nhất 2.017 token, dư 31 | `report/106` sửa đổi 11/8 (o) · `report/110` mục 4d |
| Token ảnh | 1.272 | `report/110` mục 4d |
| Độ dài chuỗi | s1 trung vị 1.498 / max 1.984 · s2 1.524 / max 2.017 | `report/110` mục 4d |
| B-infer câu nhắc | trung vị 1.149 vs 486; 85,7% ngoài vùng đã dạy; cắt 40/72 phần tử; 14,1% có tên | `report/106` sửa đổi 9/8 (j) · sửa đổi 7/8 (c) |
| Đổi card không đổi kết quả | L4 2,036/0,9686/0,8635/0,9553 vs A100 2,040/0,9679/0,8635/0,9547; `total_flos` y hệt | `report/110` mục 4h-3 (tóm ở CLAUDE.md) |
| Liger không đổi phép tính | 3.189/3.188 · 3.014/3.015 · 2.597/2.595 · 2.545/2.545 trên 200 mẫu cùng seed | `report/106` sửa đổi 11/8 (o) |
| Tự kiểm lô | 8/8 trùng nguyên văn | `report/108` mục 13.6 |
| Dựng lại dữ liệu trùng byte | so từng tệp trong thư mục tạm | `report/108` mục 12 |
| 37 lỗi loại "chạy trơn nhưng sai" | bảng đầy đủ | `report/108` mục 8 · `report/109` mục 9 |

## 4. Số nền dùng để mở bài (mục VII)

| Số | Giá trị | Điều kiện phải khai kèm |
|---|---|---|
| Câu cộc vs câu tả rõ | **32% vs 69%** | n=76 câu chuẩn, chia đôi tại trung vị 8 từ, n=38 mỗi nhánh; bộ trỏ **gpt-4o-mini** (sai số trung vị 29,3%, ngoài cổng A); dung sai 14% |
| Tương quan độ dài–trúng | +0,327 | chính là biến gây nhiễu mà S2r sinh ra để khử |

⚠️ Số cũ **35/69** đã bị rút, số đúng là **32/69** (`report/108` mục 9).

## 5. Số CẤM dùng — đã bị rút, không có trong bài và không được thêm vào

- "MDE 4,4–6,0 là số chốt" — là số ước chiếu
- "8/10 bơm lỗi" mà **không** kèm hai tiêu chí rớt và cột n
- "31 bước mỗi ứng dụng" — chia sai quần thể
- "câu cộc 35% vs 69%" — đúng là 32/69
- "bộ trỏ rẻ lệch 87 px = 8% cạnh" — trung vị chỉ tính trên ca đã trúng
- Đường cong kết oan "3%→2,6% · 5%→25% · 8%→42% · 13%→60%" — đo trên hộp OmniParser
- "tập kiểm app-unseen 631 tác vụ" — không áp dụng
- "A100 80 GB · 6,77 đơn vị/giờ · ảnh dạy 67 GB · OCR 2,8 giờ" (`report/110` mục 1)
- "GCoT chứng minh định-vị-trước làm câu kém đi" — chỉ đúng ở chế độ ra lệnh
- **"604 bước chưa thấy lúc dạy"** — tính bằng bản `tag_app_seen.py` có lỗi, đã vá 12/8;
  số thật phải chạy lại ô A.1d (`report/106` sửa đổi 12/8 (p))
- Điểm 45,0% của mô hình gốc chưa huấn luyện (n=20, KTC [23,8; 68,4]) —
  `report/108` mục 13.6 ghi rõ **không được trích như một mốc**. Bài không có số này.
