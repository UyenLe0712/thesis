# 289 — Kết quả val lớn 288 bản 4: tspicea, tnghev và tnghe (7/10/2026)

> ⛔ **Số val, chỉ để sàng. Không trích ra báo, không đưa vào luận văn.**
> tnghe chấm xong 7/10 (Kaggle `uyenle0712/vallon289-tnghe`).

## 1. Tóm tắt

Ba nhánh train tiếp ck500 thêm 250 bước (λ = 1), chấm trên val lớn 1.002 bước:

| nhánh | thưởng | Δexec so ck500 [KTC95] | ΔSPICE so ck500 [KTC95] | sàng |
|---|---|---|---|---|
| tspicea (SPICE-cont) | chỉ SPICE | −0,20 [−1,22; +0,79] | −0,98 [−2,15; +0,16] | không qua |
| tnghev (SPICE + GLR) | SPICE + người nghe Phi-4 có cổng | −0,50 [−1,65; +0,66] | −0,86 [−1,96; +0,21] | không qua |
| **tnghe** (SPICE + LR) | SPICE + người nghe Phi-4 không cổng | **+0,30** [−0,79; +1,41] | **−1,53 [−2,83; −0,22]** | không qua |

- **Exec:** tnghe là nhánh duy nhất vượt ck500 (63,67 so 63,37; cứu 17, phá 14), hơn tspicea +0,50 và hơn tnghev +0,80. Mọi KTC exec phủ 0 ⇒ chưa nói được là hơn thật.
- **Thước văn bản:** cả ba nhánh thấp hơn ck500 ở cả năm thước; tnghe thấp nhất. SPICE của tnghe −1,53 là phép so duy nhất trong file có KTC nằm hẳn dưới 0.
- **Người nghe:** không cổng (tnghe) có hướng tốt hơn có cổng (tnghev), tnghev − tnghe = −0,80 [−1,88; +0,20]. Người nghe có cổng không cho thêm gì so với chỉ train lâu hơn (tnghev − tspicea −0,30).
- **Luật sàng** (lên test khi Δexec(X − ck500) ≥ +0,5 và Δexec(X − tspicea) > 0): **không nhánh nào qua**. tnghe đạt vế thứ hai nhưng trượt vế thứ nhất (+0,30 < +0,5).
- **ck500 vẫn là mô hình tiêu đề** (test exec 60,65).

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
| tnghe | **63,67** | 97,41 | 53,33 | 38,47 | 70,18 | 442,38 | 47,69 | 7,58 | 726 |

Ghi chú:
- CIDEr-D lớn hơn 100 vì mỗi bước chỉ có một câu chuẩn. Hiện tượng này giống các bảng COCO trước đây.
- tspicea đổi câu ở 208/1.002 bước (21%) so với ck500; tnghev đổi ở 256 bước (26%); tnghe đổi ở 276 bước (28%).

### 3b. So ghép cặp

| phép so | Δexec [KTC95] | cứu / phá | ΔSPICE [KTC95] | ΔCIDEr-D [KTC95] |
|---|---|---|---|---|
| tspicea − ck500 | −0,20 [−1,22; +0,79] | 12 / 14 | −0,98 [−2,15; +0,16] | −6,44 [−15,53; +2,17] |
| tspicea − S1 | +1,00 [−0,61; +2,67] | 38 / 28 | +0,90 [−1,07; +2,93] | −7,20 [−21,12; +7,14] |
| tnghev − ck500 | −0,50 [−1,65; +0,66] | 15 / 20 | −0,86 [−1,96; +0,21] | −3,96 [−13,60; +5,18] |
| tnghev − tspicea | −0,30 [−1,34; +0,68] | 11 / 14 | +0,11 [−0,90; +1,14] | +2,48 [−6,11; +10,97] |
| tnghev − S1 | +0,70 [−1,01; +2,40] | 41 / 34 | +1,01 [−0,93; +2,98] | −4,72 [−19,09; +9,16] |
| tnghe − ck500 | +0,30 [−0,79; +1,41] | 17 / 14 | **−1,53 [−2,83; −0,22]** | −6,57 [−18,24; +5,26] |
| tnghe − tspicea | +0,50 [−0,43; +1,50] | 14 / 9 | −0,55 [−1,76; +0,66] | −0,13 [−10,38; +10,52] |
| tnghe − S1 | +1,50 [−0,11; +3,27] | 47 / 32 | +0,35 [−1,72; +2,53] | −7,33 [−23,09; +8,55] |
| tnghev − tnghe | −0,80 [−1,88; +0,20] | 10 / 18 | +0,67 [−0,46; +1,75] | +2,61 [−6,03; +11,27] |

Ô kết luận L7 của notebook Kaggle in KTC exec hơi khác ở chữ số thứ hai (tspicea − ck500 [−1,19; +0,80]; tnghev − ck500 [−1,70; +0,63]; tnghe − ck500 [−0,79; +1,44]). Lý do là thứ tự lấy mẫu bootstrap khác nhau; Δ, cứu và phá trùng tuyệt đối.

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

## 5. tnghe (SPICE + LR, λ = 1)

Adapter `tiep_nghe_101/checkpoint-250`, md5 `63575daf…` (kernel in đúng dòng này), 1.002/1.002 câu, 1.002/1.002 bước chấm, Kaggle T4 1,29 h.

Số ở bảng 3a và 3b.

Đọc:
- tnghe đổi câu ở 276/1.002 bước so với ck500, nhiều hơn tspicea (208) và tnghev (256), câu ngắn hơn một chút (7,58 từ).
- Thứ tự exec ba nhánh train tiếp: tnghe 63,67 > tspicea 63,17 > tnghev 62,87. Người nghe **không cổng** có hướng tốt hơn người nghe có cổng (−0,80 cho tnghev, cận trên +0,20), nhưng cả chuỗi đều trong nhiễu của 1.002 bước.
- Thước văn bản đi ngược exec: tnghe thua ck500 ở cả năm thước, SPICE −1,53 [−2,83; −0,22] là phép so duy nhất trong file này có KTC loại 0. Cách giải thích khả dĩ (chưa kiểm): thưởng người nghe kéo câu xa câu chuẩn hơn, vì nó thưởng câu giúp chọn đúng phần tử chứ không thưởng câu giống câu chuẩn; phần exec thu về chưa đủ bù.
- Sàng: vế Δ(tnghe − ck500) ≥ +0,5 **không đạt**; vế Δ(tnghe − tspicea) > 0 đạt.

## 6. Quyết định

- tspicea, tnghev, tnghe: **không lên test** theo luật sàng.
- tnghe là ứng viên gần nhất, nhưng SPICE giảm có ý nghĩa so ck500 nên càng ít lý do nới luật. Nếu user muốn nới luật để thử test thì phải khai là quyết định sau khi thấy số val; với Δ +0,30 trên val (val từng phóng đại khoảng cách giữa nhánh, xem CLAUDE.md khối V2), kỳ vọng trên test là ngang ck500.
- Đề xuất: đóng hướng người nghe Phi-4 ở λ = 1; mô hình tiêu đề giữ **ck500** (test exec 60,65); luận văn khai ba nhánh SPICE-cont, LR, GLR như hướng đã thử, chỉ báo hình dạng kết quả, không trích số val.
- Hai nhánh λ = 2 (tnghem, tnghevm) chưa chạy; user quyết có chạy hay không.

## 7. Tệp

- `runs/vallon289/ket_qua_vallon.json`: mọi số ở mục 3.
- `runs/vallon289/tspicea/`: pred, raw, log của tspicea, kèm `vallon289-spicea.log` có ô L7.
- `runs/vallon289/tnghev/`: tương tự cho tnghev.
- `runs/vallon289/tnghe/`: tương tự cho tnghe, kèm `vallon289-tnghe.log`.
- `runs/vallon289/{pred,score}_{S1,ck500}_vallon*`: hai mốc so.
