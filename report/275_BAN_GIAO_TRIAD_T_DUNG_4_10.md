# 275 — Bàn giao 4/10 tối: TRIAD-T dừng sau POB

> Tự chứa. Chi tiết POA/POB ở `report/274` (§4–5 POA, §7 POB). Mọi số trong file này là **số val C1 (249 bước
> click)**, chỉ để xếp hạng trong họ, **cấm trích vào luận văn**.

## 1. Kết luận

TRIAD-T (ck500 sinh nhiều câu → listener ShowUI đọc → bộ chọn giữ câu trỏ gần điểm của bộ định vị chỉ-ảnh) **không
nâng được exec** và dừng theo cổng §6.3 của action 273. Không chạy P1, không chấm test.

Mô hình có exec cao nhất vẫn là **GRPO thưởng SPICE ck500: 60,65 trên test** (S1/101 59,11; TAGE 60,23).

## 2. Bảng điểm trên val C1 (UGround, cùng 249 bước click)

| nhánh | đúng /249 | exec | so S1 |
|---|---|---|---|
| S1/101 greedy | 158 | 63,45 | — |
| GRPO-SPICE ck500 greedy (chấm L4) | 166 | 66,67 | +3,21 [0,00; +6,40] · cứu 12 phá 4 |
| TRIAD-T POA (mẫu S1, cấu hình theo luật) | 167 | 67,07 | net +1 so ck500 |
| **TRIAD-T POB (mẫu ck500, T=1,0, r=60, r_trust=140)** | **166** | **66,67** | **net 0 so ck500** (đổi 9 câu, cứu 0, phá 0) |
| POB không cổng tin cậy, tốt nhất (T=0,7, r=60) | 168 | 67,47 | +2 so ck500, KTC [−1,18; +2,75] |
| oracle: ít nhất một trong 8 mẫu ck500 đúng (T=1,0) | 187 | 75,10 | trần của bộ chọn, không phải mô hình |

KTC: bootstrap theo episode, 2.000 lần. ck500 chấm trên T4 (`runs/grpo_spice`) ra 165/249 (66,27), lệch L4 một bước,
đúng mức đã biết giữa hai card.

## 3. Vì sao không lên

Các mẫu có câu đúng (oracle +21 bước) nhưng bộ chọn không lấy ra được. Trong 21 bước cứu được ở T=1,0
(phân loại xấp xỉ, cửa sổ ±14% từng trục):

| khâu chặn | số bước |
|---|---|
| điểm bộ định vị chỉ-ảnh lệch phần tử vàng | 10 |
| hai bộ định vị bất đồng ⇒ cổng tin cậy chặn | 6 |
| ShowUI không đặt câu đúng nào gần điểm định vị | 2 |
| ShowUI đọc câu ck500 trúng, UGround đọc sai | 2 |
| còn đường đổi | 1 |

⇒ **16/21 bước chết ở bộ định vị**, trước khi listener góp phần. Cùng điểm nghẽn với TAGE trên test (`report/269`:
139 câu vùng cắt sai). Mọi hướng "chọn/sửa câu sau khi sinh" dựa vào bộ định vị chỉ-ảnh hiện tại đều bị trần này.

## 4. Lỗi gặp khi chạy và cách đã sửa

- Commit POB lượt 1 chết ở bước chọn C2: `nap_tat_ca` lấy mọi tệp bắt đầu bằng `listener_pob`, gồm cả
  `listener_pob_s*.log` ⇒ `JSONDecodeError`. Sửa `harness/triad_pob.py:179` (chỉ lấy `.jsonl`, md5 mới `36e8e299…`).
- Lượt nối tiếp: gắn output commit lỗi làm Input. Ô 2–3 của `harness/kaggle_triad_pob.md` nay có `ngoai()` bỏ qua
  output cũ khi glob tìm gói (nếu không sẽ thấy hai bản `triad_pob.py`). Mọi bước GPU tự bỏ qua phần đã xong.
- Bài học: sửa script xong phải chép cả sang `_bundles/<dataset>/` — lượt đầu upload nhầm bản cũ vì quên bước này.

## 5. Tệp

| tệp | nội dung |
|---|---|
| `runs/triad_t/pob/triad_pob_out/` | output đủ của commit POB (mẫu, listener, UGround theo lớp, UI-Venus) |
| `runs/triad_t/pob_ket_qua.json` | bảng lưới C1/C2, oracle, đa dạng, danh sách bước đổi câu |
| `harness/triad_pob.py` | lấy mẫu · dựng lớp · chọn · báo cáo (`--bao-cao` chạy lại 0 GPU) |
| `harness/kaggle_triad_pob.md` | runbook commit, có nối tiếp |
| `report/274` | POA + POB đầy đủ |

## 6. Việc kế (chưa quyết, user chọn)

1. Luận văn: thêm TRIAD-T vào ch6 như một hướng đã thử (báo vô điều kiện, chỉ hình dạng kết quả, không trích số val).
2. Nếu còn muốn nâng exec: điểm nghẽn là bộ định vị chỉ-ảnh, không phải listener hay độ đa dạng của mẫu.
3. Nợ cũ của ck500: tác hại ở bước không chạm (scroll 83,97 → 77,75, `report/261` §6) phải khai trong bài.
