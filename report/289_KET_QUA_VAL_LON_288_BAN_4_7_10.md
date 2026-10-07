# 289 — Kết quả val lớn 288 bản 4: tspicea và tnghev (7/10/2026)

> ⛔ **Số val, chỉ để sàng. Không trích ra báo, không đưa vào luận văn.**
> Mục 5 (tnghe) còn trống, sẽ điền khi Colab chạy xong đợt 3.

## 1. Tóm tắt

- Train tiếp ck500 thêm 250 bước không làm tăng số.
  - **tspicea** (SPICE-cont, chỉ thưởng SPICE) ngang ck500 về exec: −0,20.
  - **tnghev** (SPICE + GLR, λ = 1, thêm thưởng người nghe Phi-4 có cổng) cũng ngang ck500: −0,50.
  - Mọi khoảng tin cậy đều phủ 0.
- Cả hai nhánh nhích xuống nhẹ ở cả năm thước văn bản so với ck500.
- tnghev so với tspicea chênh rất ít:
  - exec −0,30;
  - SPICE +0,11;
  - CIDEr-D +2,48.

  Thưởng người nghe chưa cho thêm gì so với chỉ train lâu hơn.
- **Luật sàng** (lên test khi Δexec(X − ck500) ≥ +0,5 và Δexec(X − tspicea) > 0): tnghev **không qua**.
- tspicea cũng không đủ điều kiện lên test một mình, vì Δ của nó so với ck500 dưới +0,5.
- ck500 vẫn là mô hình đứng đầu.

## 2. Thiết lập

| mục | giá trị |
|---|---|
| tập | val lớn 289: 1.002 bước click, 330 tác vụ (`valdata`, ngoài tập dạy của GRPO) |
| exec | `action_ok` ∧ ±14% ∧ Voronoi, bộ trỏ UGround-V1-2B, Kaggle T4 |
| văn bản | bộ chấm COCO (`pycocoevalcap`): BLEU-4 · METEOR · ROUGE-L · CIDEr-D · SPICE, một câu chuẩn mỗi bước |
| so ghép cặp | bootstrap theo tác vụ: exec 5.000 lần, SPICE/CIDEr-D 3.000 lần, seed 0 |
| nhánh | S1/101 · ck500 (GRPO-SPICE 500 bước) · tspicea · tnghev; cả hai nhánh mới train tiếp 250 bước từ adapter ck500 |

Tái lập (0 GPU, khoảng 12 phút CPU):
`~/.venvs/thesis/bin/python _scripts/289/ket_qua_vallon.py` → `runs/vallon289/ket_qua_vallon.json`.
Script tự tìm mọi nhánh có `pred_<t>_vallon.jsonl` và `score_<t>_vallon_raw.jsonl` trong `runs/vallon289/`.

## 3. Bảng số

### 3a. Điểm tuyệt đối

| nhánh | exec | action_ok | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | số từ TB | câu trùng ck500 |
|---|---|---|---|---|---|---|---|---|---|
| S1/101 | 62,18 | 95,21 | 54,13 | 38,51 | 70,20 | 449,71 | 47,34 | 7,72 | 605 |
| **ck500** | **63,37** | 97,01 | **54,81** | **39,25** | **70,52** | 448,95 | **49,22** | 7,82 | 1.002 |
| tspicea | 63,17 | 97,11 | 53,65 | 38,59 | 70,22 | 442,51 | 48,25 | 7,72 | 794 |
| tnghev | 62,87 | **97,80** | 53,76 | 38,67 | 70,25 | 444,99 | 48,36 | 7,63 | 746 |

Ghi chú:
- CIDEr-D lớn hơn 100 vì mỗi bước chỉ có một câu chuẩn. Hiện tượng này giống các bảng COCO trước đây.
- tspicea đổi câu ở 208/1.002 bước (21%) so với ck500; tnghev đổi ở 256 bước (26%).

### 3b. So ghép cặp

| phép so | Δexec [KTC95] | cứu / phá | ΔSPICE [KTC95] | ΔCIDEr-D [KTC95] |
|---|---|---|---|---|
| tspicea − ck500 | −0,20 [−1,22; +0,79] | 12 / 14 | −0,98 [−2,15; +0,16] | −6,44 [−15,53; +2,17] |
| tspicea − S1 | +1,00 [−0,61; +2,67] | 38 / 28 | +0,90 [−1,07; +2,93] | −7,20 [−21,12; +7,14] |
| tnghev − ck500 | −0,50 [−1,65; +0,66] | 15 / 20 | −0,86 [−1,96; +0,21] | −3,96 [−13,60; +5,18] |
| tnghev − tspicea | −0,30 [−1,34; +0,68] | 11 / 14 | +0,11 [−0,90; +1,14] | +2,48 [−6,11; +10,97] |
| tnghev − S1 | +0,70 [−1,01; +2,40] | 41 / 34 | +1,01 [−0,93; +2,98] | −4,72 [−19,09; +9,16] |

Ô kết luận L7 của notebook Kaggle in KTC exec hơi khác ở chữ số thứ hai (tspicea − ck500 [−1,19; +0,80]; tnghev − ck500 [−1,70; +0,63]). Lý do là thứ tự lấy mẫu bootstrap khác nhau; Δ, cứu và phá trùng tuyệt đối.

## 4. Đọc kết quả

1. **Chỉ train lâu hơn không giúp.**
   - tspicea là đối chứng "train lâu hơn": cùng thưởng, cùng 250 bước, cùng máy với các nhánh người nghe.
   - Nhánh này không hơn ck500 ở thước nào; SPICE giảm gần 1 điểm.
   - Đường val của GRPO-SPICE từng tăng từ ck250 lên ck500, nhưng không tăng tiếp tới 750 bước.
2. **Người nghe có cổng chưa thêm được gì.**
   - tnghev ngang tspicea ở mọi thước, mọi chênh lệch đều nhỏ hơn nửa KTC.
   - Riêng `action_ok` nhích lên 97,80 (so với 97,11). Đây là dấu hiệu duy nhất theo chiều tốt, nhưng exec không theo.
3. **Cả hai vẫn hơn S1 khoảng +0,7 đến +1,0 exec, KTC phủ 0.** Phần hơn này là của ck500 để lại, không phải của 250 bước train thêm.
4. **Sàng:** tnghev trượt cả hai vế; tspicea không lên test.

## 5. tnghe (SPICE + LR, λ = 1) — CHỜ

Colab đang chạy đợt 3. Khi C7 in `✅ ĐỢT 3 XONG`, làm theo các bước sau:

1. Dựng dataset Kaggle từ `tiep_nghe_101/final/`. Thư mục phải lồng thêm một cấp vì Kaggle bỏ thư mục gốc khi tải lên.
2. Chép kernel `k_vallon2` với `NHANH = ["tnghe"]`, đổi ô L7 sang tnghe, rồi push commit.
3. Tải kết quả về `runs/vallon289/nghe/`, chạy lại `_scripts/289/ket_qua_vallon.py`. Các hàng tnghe và các phép so `tnghe − ck500/tspicea/S1` và `tnghev − tnghe` sẽ tự vào JSON.
4. Điền bảng dưới đây và cập nhật mục 6.

| nhánh | exec | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE |
|---|---|---|---|---|---|---|
| tnghe | … | … | … | … | … | … |

| phép so | Δexec [KTC95] | cứu / phá | ΔSPICE | ΔCIDEr-D |
|---|---|---|---|---|
| tnghe − ck500 | … | … | … | … |
| tnghe − tspicea | … | … | … | … |
| tnghev − tnghe | … | … | … | … |

## 6. Quyết định (tạm, chờ tnghe)

- tnghev: **không lên test.**
- tspicea: **không lên test.**
- Nếu tnghe cũng không qua sàng:
  - đóng hướng người nghe Phi-4;
  - mô hình tiêu đề giữ **ck500** (test exec 60,65);
  - luận văn khai ba nhánh SPICE-cont, LR và GLR như các hướng đã thử, chỉ báo hình dạng kết quả, không trích số val.

## 7. Tệp

- `runs/vallon289/ket_qua_vallon.json`: mọi số ở mục 3.
- `runs/vallon289/spicea/`: pred, raw, log của tspicea, kèm `vallon289-spicea.log` có ô L7.
- `runs/vallon289/lo1/`: tương tự cho tnghev.
- `runs/vallon289/{pred,score}_{S1,ck500}_vallon*`: hai mốc so.
