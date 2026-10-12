# 310 — Kết quả CW-RA (action 309) và quyết định đóng (12/10/2026)

File bàn giao, tự chứa. Cách chạy ở `report/309_ACTION_CW_RA_KAGGLE_10_10_extracted.md`; mã ở `_scripts/308/`.

**Quyết định (user, 12/10): ĐÓNG CW-RA.** Phương pháp trong luận văn giữ nguyên là ACE (ck500 + luật ghép R3, `report/304` §4–5). CW-RA chỉ được nhắc như một hướng đã thử.

## 1. CW-RA là gì

CW-RA train tiếp từ ck500 với khối 4 câu ví dụ truy hồi. Mô hình sinh một thẻ trước câu: `[COPY i]` (chép nguyên câu ví dụ thứ i) hoặc `[WRITE]` (tự viết câu).

- Dữ liệu dạy có 3.991 hàng. 736 hàng (18,4%) học thẻ COPY, tức các hàng có câu ví dụ trùng câu chuẩn. 3.255 hàng học `[WRITE]` kèm câu greedy của chính ck500 (tự chưng cất).
- Train 250 bước trên Kaggle T4, 107 s/bước, VRAM 7,3 GiB, loss cuối khoảng 0,22–0,25.
- Lúc sinh: chép khi xác suất thẻ COPY ≥ τ. τ chọn một lần trên val lớn (1.002 bước) trong lưới 0,3 … 1,01, rồi áp lên tập kiểm.

## 2. Kết quả

### 2.1 Val lớn (1.002 bước, chỉ dùng để chọn τ)

Không mức τ nào hơn ck500 ở thước nào (0/5 thước ở mọi τ). Chép càng nhiều thì điểm càng thấp:

| τ | 0,3 | 0,4 | 0,5 | 0,7 | 0,9 | 1,01 (không chép) | ck500 |
|---|---|---|---|---|---|---|---|
| CIDEr-D | 390,3 | 402,5 | 411,0 | 413,6 | 415,4 | 415,4 | 449,0 |
| câu khác ck500 | 50,7% | 48,3% | 46,1% | 45,3% | 45,2% | 45,2% | — |

Theo luật chọn, τ chốt ở **1,01**, tức không ép chép câu nào. Đây là số val, không trích ra báo.

### 2.2 Tập kiểm, 7 thước chữ (4.463 bước click)

Phần tự kiểm tái lập đúng điểm ck500.

| | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|
| ck500 | 52,36 | 37,91 | 68,34 | 430,0 | 45,79 | 62,86 | 67,07 |
| CW (τ = 1,01) | 49,72 | 35,79 | 65,05 | 406,8 | 43,71 | 60,04 | 64,53 |

CW thua ở cả 7 thước. Một số đi kèm:

- 43,3% số câu khác ck500.
- 13,4% số câu trùng nguyên văn một câu ví dụ, dù không bị ép chép. Trong số đó chỉ 45,1% đúng câu chuẩn.

### 2.3 exec, D.3, AitW (đọc bằng `doc_exec_cw.py`, 0 GPU)

Kaggle chỉ chấm UGround cho 2.203 câu khác ck500; các bước còn lại lấy từ tệp thô ck500. Bước hiệu chuẩn chấm lại 40 câu ck500: lệch tọa độ và exec đều là 0.

| | exec | D.3 | AitW |
|---|---|---|---|
| ck500 | 60,65 [58,90; 62,38] | 67,02 | 76,25 |
| CW | 58,53 [56,73; 60,29] | 64,84 | 74,34 |
| S1/101 | 59,11 | 65,49 | 74,37 |
| **CW − ck500** | **−2,13 [−2,94; −1,31]**, cứu 116, phá 211, p = 2e−7 | −2,17, p = 2e−7 | −1,90, p = 9e−6 |
| CW − S1/101 | −0,58 [−1,51; +0,34], p = 0,21 | −0,65, p = 0,18 | −0,02, p = 1 |

CW thua ck500 có ý nghĩa dưới cả ba thước và ngang S1/101.

## 3. Đọc kết quả

- **Chỗ hỏng là nhánh viết, không phải khâu chép.** Ở τ = 1,01 không có câu nào bị ép chép, vậy mà nhánh viết vẫn đổi 43% số câu so với ck500, và đổi theo hướng xấu. Tự chưng cất bằng câu greedy của ck500 không giữ được mô hình ở lại chỗ ck500: thêm khối câu ví dụ vào đầu vào làm phần sinh câu trôi về gần mức S1.
- **Đầu chép không đủ tự tin.** Trên dữ liệu dạy có 18,4% hàng là chép, nhưng lúc sinh chỉ khoảng 3% số bước có xác suất COPY ≥ 0,5, trên cả val lẫn tập kiểm. Hạ τ để chép nhiều hơn thì điểm lại tụt, đúng chiều của `ra_k4` khi đứng một mình (exec −1,25, `report/304`).
- **Kết quả này khớp lượt 304.** Train tiếp ck500 với khối ví dụ (RA-SFT ở hai LR, rồi CW-RA) không lần nào vượt ck500. Phần lợi của khối ví dụ chỉ lấy được bằng một luật ghép có điều kiện ở tầng câu (R3/ACE), không lấy được bằng cách train.

## 4. Chạy máy và bài học

| lượt | tài khoản | việc | thời gian |
|---|---|---|---|
| T (`cw-ra-t-309`) | trang | kiểm 20 bước, sinh ck500 trên dữ liệu dạy, dựng dữ liệu, train 250 bước | — (`runs/cw309/T/`) |
| G1 (`cw-ra-g1-309`) | trang | val (2 shard) + test shard 0–3/10 | 5,75 h |
| G2 (`cw-ra-g2-309`) | uyenle | test shard 4–9/10 | **treo >16 h, không log, không output** |
| G2b (`cw-ra-g2b-309`) | trang | test shard 7–9 (chia thành 6 nửa /20) | 2,85 h |
| G3b (`cw-ra-g3b-309`) | uyenle | test shard 4–6 + gộp + chọn τ + 7 thước + exec | ~4,5 h |

- Chế độ `cw` chạy khoảng **14,4 s/bước** trên một T4.
- **G2 treo mà không để lại dấu vết.** Nó vượt trần 12 h nhưng vẫn ở trạng thái RUNNING, và CLI không huỷ được. Nghi do máy chỉ cấp 1 GPU, khiến chuỗi GPU 1 chạy trên CPU; chưa kiểm được. Cách vá đã dùng: thêm ô `assert torch.cuda.device_count() == 2` ngay trước khâu sinh, để thiếu GPU thì báo lỗi sau ~15 phút thay vì treo cả đêm. Mọi notebook hai GPU về sau nên có ô này.
- **Chia shard `k/20` và `(k+10)/20`.** Hai nửa này hợp lại đúng bằng `k/10`, nên rút ngắn được một lượt mà không phải đổi mã. Đã kiểm: 223 + 223 = 446 hàng, không trùng.

## 5. Tệp

- `runs/cw309/T/`: train (log, `cw_stats.json`, dữ liệu dạy).
- `runs/cw309/G1/`, `G2b/`, `G3b/`: shard câu sinh.
- `runs/cw309/G3b/cw_test.jsonl`, `cw_val.jsonl`: đã gộp.
- `runs/cw309/G3b/tau_chon.json`, `diem_val_cw.json`, `diem_test_cw.json`: chọn τ và 7 thước.
- `runs/cw309/G3b/ghep/pred_cw_t1.01_test.jsonl`: câu cuối.
- `runs/cw309/G3b/exec_out/`: tệp chấm thô UGround, tệp gộp và `doc_exec_cw.json`.
- Notebook và script dựng notebook: `_scripts/308/kaggle/`.
- Dataset Kaggle trung gian (`uyenle0712/cw-ra-g1-out`, `cw-ra-g2b-out`) không còn cần, xoá được.
