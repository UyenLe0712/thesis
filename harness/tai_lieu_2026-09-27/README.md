# Tài liệu trích xuất ngày 27/09/2026

Nguồn: `../My Documents [27-09-2026 14_51].zip` (đã xoá sau khi trích xuất), gồm 7 ảnh JPG chụp màn
hình các phần nối tiếp của một tài liệu Markdown tên `226_BRIEF_ECGR_CHO_CHAT_LAM_27_9.md`.

## Nội dung

- [Bản văn bản đã tái cấu trúc](226_BRIEF_ECGR_CHO_CHAT_LAM_27_9.md): ghép nội dung từ bảy ảnh,
  định dạng lại đề mục, bảng, công thức và script.
- `anh_goc/`: giữ nguyên tên và dữ liệu của bảy ảnh trong ZIP.
- Kết quả G0 đã chạy — bản đầy đủ (theo đúng mục 8/10 của tài liệu, ghi **ngoài clone này**) ở
  `/mnt/d/Master/ECGR_G0_27_9/ket_qua_g0_ecgr.md`; bản tóm tắt đã đưa vào kho tại
  [`report/206_BAN_GIAO_ECGR_G0_TRUOT_27_9.md`](../../report/206_BAN_GIAO_ECGR_G0_TRUOT_27_9.md)
  — **G0 TRƯỢT (147/958, ngưỡng 250), dừng ECGR ở đây, không chạy G1, không train**.

## Thứ tự đọc ảnh

| Thứ tự | Ảnh | Nội dung |
| --- | --- | --- |
| 1 | [1a8803520b3d8b63d22c1.jpg](anh_goc/1a8803520b3d8b63d22c1.jpg) | Tiêu đề; mục 0 (việc phải làm); mục 1 (bài toán); mục 2 (ràng buộc); đầu mục 3. |
| 2 | [2a42709978f6f8a8a1e72.jpg](anh_goc/2a42709978f6f8a8a1e72.jpg) | Bảng mục 3 đầy đủ (5 nhánh × 7 metric); bảng điều kiện "tăng thật"; mục 4 (MM-SeR là gì). |
| 3 | [f1a0477c4f13cf4d96023.jpg](anh_goc/f1a0477c4f13cf4d96023.jpg) | Mục 5: ECG trong ECGR — sơ đồ forward, công thức cổng $g$, hàm loss; đầu bảng ablation. |
| 4 | [63f626292e46ae18f7574.jpg](anh_goc/63f626292e46ae18f7574.jpg) | Tiếp bảng ablation; câu được phép viết; mục 6 (không đề xuất lại); đầu mục 7 (số nội bộ). |
| 5 | [95afea72e21d62433b0c5.jpg](anh_goc/95afea72e21d62433b0c5.jpg) | Tiếp mục 7; mục 8 (cổng và action cụ thể, định nghĩa G0/G1). |
| 6 | [63177ff77798f7c6ae896.jpg](anh_goc/63177ff77798f7c6ae896.jpg) | Action sau G0; mục 9 (file clone được đọc); mục 10 (không được tự làm); đầu Phụ lục A. |
| 7 | [4fd706360e598e07d7487.jpg](anh_goc/4fd706360e598e07d7487.jpg) | Phụ lục A: script G0 đầy đủ; Phụ lục B: đầu ra bắt buộc. |

## Ghi chú chuyển đổi

- Văn bản được chép từ ảnh chụp màn hình (không phải khôi phục file Markdown nguồn). Thứ tự bảy
  ảnh không trùng thứ tự tên hash trong ZIP; đã xác định lại bằng cách đọc nội dung liền mạch giữa
  các ảnh (câu cuối ảnh này khớp câu đầu ảnh kế).
- Đường dẫn trong tài liệu gốc có tiền tố `thesis-master/` (tên clone ở máy soạn tài liệu). Trong
  kho này tiền tố đó **chính là gốc kho** (`/mnt/d/Master/Thesis`), nên các đường dẫn trong bản chép
  đã bỏ tiền tố để trỏ đúng file thật, trừ trong script Phụ lục A (giữ nguyên văn để đối chiếu).
- Tài liệu tự đối chiếu bằng ba số `n=4463, exact=954, one_block=958`; đã chạy script Phụ lục A
  thật trên `runs/score_s1_seed101_raw.jsonl` và khớp cả ba số trước khi tin phần còn lại của tài
  liệu.
- Ba file ZIP "My Documents" cũ hơn (25/9, 26/9) và `harness/p1_out.zip` đã bị xoá cùng lượt dọn
  này — nội dung của chúng đã nằm sẵn trong `harness/tai_lieu_2026-09-25/anh_goc/`,
  `paper/soict2026/guistep/` và `runs/pata/p1/` (xác nhận bằng so khớp tên file/hash trước khi
  xoá). ZIP của chính ngày 27/9 cũng đã xoá sau khi trích xuất, theo đúng cách xử lý hai ZIP trước.

## Lượt thứ hai cùng ngày (17:08) — 230_ACTION_PROBE_FGRB

Nguồn: `../My Documents [27-09-2026 17_08].zip` (đã xoá sau khi trích xuất), gồm 8 ảnh JPG chụp
màn hình các phần nối tiếp của một tài liệu Markdown khác, tên
[`230_ACTION_PROBE_FGRB_CHO_CHAT_LAM_27_9.md`](230_ACTION_PROBE_FGRB_CHO_CHAT_LAM_27_9.md). Ảnh
gốc giữ ở `anh_goc_230/` (tách khỏi `anh_goc/` của lượt 226 để khỏi lẫn hai tài liệu).

Phương pháp mới được đề xuất trong tài liệu này là **GUIStep-FGRB**: một bottleneck mềm phân rã
câu GUI thành action/role/zone, tiêm residual vào decoder của S1 đã đóng băng — khác hẳn ECGR
(226). Việc bắt buộc của lượt này chỉ là **probe** (đo xem hidden state đóng băng của S1 có dự
đoán được action/role/zone hay không), qua ba cổng tuần tự P0 (kiểm nhãn, 0 GPU) → kiểm kê đầu
vào (adapter/ảnh/OCR) → P1 (probe phân loại) → P2 (sinh câu trên val). Trượt cổng nào thì dừng ở
đó, không được hạ ngưỡng, không train LoRA, không đụng tập test.

**Đã làm theo hướng dẫn tới đâu (27/9, trên chính kho làm việc, không phải clone mới):**

- Phụ lục A (P0, kiểm nhãn) đã chạy thật — khớp tuyệt đối 7/7 số kỳ vọng. **P0 ĐẠT.**
- Kiểm kê đầu vào: OCR train đủ (64.567 dòng) · ảnh train chỉ 11,81% toàn cục và 9,62% trên đúng
  tập nguồn lấy mẫu của P1 (val thì đủ 100%) · **adapter S1/101 không tìm thấy ở bất kỳ đâu trong
  clone** (chỉ có các adapter của các nhánh sau S1: `gui_sel`, `grpo_point`, `noisuy` α0–α1, VIS-SFT
  `k1`).
- **Phán quyết: `CHƯA CHẠY — thiếu đầu vào`, dừng tại P0** theo đúng luật của tài liệu (không tự
  tải Release, không tự kéo Drive, không probe bằng model gốc thay S1). Không chạy P1/P2, không
  train.
- Bản đầy đủ, tự chứa theo đúng 7 mục mà tài liệu 230 yêu cầu:
  [`report/207_KET_QUA_PROBE_FGRB_27_9.md`](../../report/207_KET_QUA_PROBE_FGRB_27_9.md).

### Thứ tự đọc 8 ảnh (230)

| Thứ tự | Ảnh | Nội dung |
| --- | --- | --- |
| 1 | [98b925c8fda77df924b61.jpg](anh_goc_230/98b925c8fda77df924b61.jpg) | Tiêu đề; mục 0 (việc phải làm); mục 1 (bài toán, bảng metric S1/101). |
| 2 | [1fc3ddb105de8580dccf2.jpg](anh_goc_230/1fc3ddb105de8580dccf2.jpg) | Mục 2: FGRB là gì — sơ đồ forward, công thức, bảng ba lớp action/role/zone. |
| 3 | [c1ca65b9bdd63d8864c73.jpg](anh_goc_230/c1ca65b9bdd63d8864c73.jpg) | Mục 3 (vì sao chỉ probe, hai bảng trần); đầu mục 4, bảng P0. |
| 4 | [a87b250efd617d3f24704.jpg](anh_goc_230/a87b250efd617d3f24704.jpg) | Kiểm kê đầu vào (bảng 3 thứ thiếu); mục P1, bảng ngưỡng bắt đầu. |
| 5 | [35b7dbc303ac83f2dabd5.jpg](anh_goc_230/35b7dbc303ac83f2dabd5.jpg) | Nốt bảng ngưỡng P1; mục P2; mục 5 (không được làm). |
| 6 | [0705eb73331cb342ea0d6.jpg](anh_goc_230/0705eb73331cb342ea0d6.jpg) | Mục 6 (file kết quả); Phụ lục A (script kiểm nhãn). |
| 7 | [5ea026dbfeb47eea27a57.jpg](anh_goc_230/5ea026dbfeb47eea27a57.jpg) | Kỳ vọng của Phụ lục A; Phụ lục B (script nhãn + lấy mẫu 4.000). |
| 8 | [5ddc0aa0d2cf52910bde8.jpg](anh_goc_230/5ddc0aa0d2cf52910bde8.jpg) | Nốt Phụ lục B (đầu ra P1 bắt buộc, cách lấy hidden state); Phụ lục C (proxy BLEU). |

Thứ tự tên hash trong ZIP không trùng thứ tự nội dung; đã xác định lại bằng cách đọc nội dung
liền mạch giữa các ảnh, giống cách làm với 226.
