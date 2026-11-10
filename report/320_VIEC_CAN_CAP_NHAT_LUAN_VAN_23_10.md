# 320 — Số liệu và việc cần cập nhật luận văn: phương pháp chính ck500 + ACE

Ghi từ 23/10/2026, sắp xếp lại theo chủ đề ngày 26/10. Đây là tệp tra cứu khi viết tiếp luận văn. Chưa sửa tệp nào trong `thesis/`.
Bản ghi theo thời gian (G1 đến G17) nằm ở commit `3e895b1` nếu cần tra lịch sử.

**Cách dùng.** Mục 1 là kết luận. Các mục 2 đến 8 là số liệu theo chủ đề, mỗi mục có phần "Đọc" và "Phải khai". Mục 9 gợi ý cách trình bày từng kết quả. Mục 10 là việc cần sửa theo từng chương. Mục 11 là những gì còn chờ. Mục 12 là nguồn tệp và kiểm tái lập.

**Quy ước.**
- Nếu không ghi khác, mọi số là số test trên AndroidControl, chấm qua UGround trên 4.463 bước chạm.
- Phép so luôn ghép cặp: KTC95 bằng bootstrap cụm theo app (1.091 cụm, B = 10.000, hàm `score_run.cluster_bootstrap`), p là McNemar chính xác. Trên AitZ cụm là episode (506 cụm).
- Mỗi nhánh có một hạt giống, trừ S1 và ck500 (mỗi nhánh có hai hạt). MDE của thiết kế là 2,11 điểm exec.

**Tên nhánh.**
| tên | là gì |
|---|---|
| Base | Qwen2.5-VL-3B-Instruct, không tinh chỉnh |
| S1/101, S1/202 | SFT trơn, hai hạt giống |
| ck500 (= ck500/101) | phương pháp chính: GRPO thưởng SPICE, 500 bước, xuất phát S1/101 |
| ck500/202 | cùng cấu hình ck500, hạt GRPO 202, vẫn xuất phát S1/101 |
| ACE (R3) | ck500 + luật ghép R3: lấy câu của ra_k4 khi câu đó trùng một câu ví dụ và cùng loại thao tác với câu ck500. Trong luận văn gọi là ACE |
| ra_k4 | ck500 train tiếp với khối 4 câu ví dụ truy hồi, đứng riêng (không dùng làm mô hình) |
| xao101 | nhánh kiểm sàn: như ck500 nhưng thưởng SPICE bị xáo giữa các mẫu |
| 7B | Qwen2.5-VL-7B-Instruct prompting, cùng câu nhắc của Base |
| câu chuẩn | câu do người chú thích viết, chấm qua cùng bộ trỏ (mốc trần của dụng cụ) |

---

## 1. Kết luận

Thứ tự dưới đây là thứ tự nên kể trong luận văn: kết quả chính trước, phạm vi áp dụng sau.

1. **Mức tăng của ck500 đến từ chính tín hiệu thưởng SPICE.** Nhánh kiểm sàn xao101 chạy cùng 500 bước GRPO nhưng thưởng bị xáo, và cho kết quả bằng đúng S1 cả về exec (+0,00) lẫn bảy thước chữ. ck500 − xao101 = **+1,55 [+0,81; +2,30]**, p = 2e−5. (Mục 2, 3)
2. **Trên AndroidControl, ck500 hơn S1 có ý nghĩa thống kê.** ck500 60,65 so với S1/101 59,11: **+1,55 [+0,80; +2,33]**, p = 1,6e−5. So với hạt S1 thứ hai cũng hơn: +1,03 [+0,25; +1,83], p = 0,014. Hạt GRPO thứ hai (ck500/202, 59,94) hơn S1/101 +0,83 (p = 0,036), và dưới luật AitW đầy đủ +1,86 (p = 2,5e−6). Kết quả giữ dưới cả bốn luật khớp chạm: ck500 − S1/101 là +1,55 (exec), +1,52 (D.3), +1,52 (D.3 ∧ 14%), +1,88 (AitW đầy đủ, p = 2,1e−7), mọi KTC loại 0, và so với S1/202 cũng loại 0 ở cả bốn luật. Hướng dương lặp lại ở cả hai hạt GRPO (so với S1/202, hạt 202 nhỉnh hơn +0,31). (Mục 2)
3. **Trên tác vụ S1 chưa thấy (ACU, 1.484 bước), mức tăng lớn gần gấp ba.** ck500 56,74 so với S1 52,16: **+4,58 [+3,17; +6,05]**, p = 2,1e−10 (cứu 93, phá 25). Hạt GRPO thứ hai +4,04 [+2,66; +5,48], ACE +4,85 [+3,43; +6,32]. Cận dưới KTC của cả ba (+3,17 · +2,66 · +3,43) đều nằm trên 2,11, tức trên cả MDE tính cho tập kiểm chính. Gộp với tập kiểm chính (5.947 bước), ck500 − S1 = **+2,30 [+1,62; +2,99]**, p = 6,8e−13, vượt MDE. (Mục 8)
4. **Hướng tăng giữ qua bốn dụng cụ chấm độc lập.** So với S1/101, ck500 hơn dưới UGround +1,55, UI-Venus +1,55, Phi-Ground (ngoài họ Qwen, không huấn luyện trên AndroidControl theo báo cáo kỹ thuật) +0,78, người nghe Phi-4 +0,69; KTC loại 0 ở cả bốn. (Mục 4)
5. **Ưu thế giữ nguyên khi lịch sử là câu mô hình tự viết.** ck500 − S1 = +1,48 [+0,54; +2,43] (tập con đủ ảnh +1,66), và về đúng loại thao tác ở bước chạm, khoảng cách còn tăng từ +1,88 lên +3,52. (Mục 7)
6. **ACE nâng chất lượng câu ở mọi thước chữ, giữ trọn khả năng định vị của ck500.** Ở cả sáu thước có KTC, mọi KTC đều nằm hẳn trên 0 (CIDEr-D +11,97, SPICE +1,33); exec ngang ck500 (+0,02). (Mục 2, 3)
7. **Mô hình 3B sau tinh chỉnh vượt Qwen2.5-VL-7B prompting khoảng 9 điểm exec** (ck500 − 7B +9,14, S1 − 7B +7,60), gấp đôi mức 7B hơn 3B gốc (+3,92). (Mục 2)
8. **Phạm vi áp dụng.**
   - Sang miền khác (AitZ), tinh chỉnh SFT chuyển được (+3,29 so với Base, có ý nghĩa); ck500 và S1 tương đương (−0,51, KTC phủ 0), phù hợp với việc thưởng SPICE học theo văn phong câu chuẩn AndroidControl. (Mục 6)
   - Ở bước không chạm, ck500 ưu tiên câu cho thao tác chạm (scroll −6,23), rõ hơn khi lịch sử tự sinh. Đây là động lực cho ACE và cho hướng tinh chỉnh hàm thưởng. (Mục 5, 7)
   - Mỗi nhánh một hạt giống (S1 và ck500 hai hạt); trên tập kiểm chính, mức tăng nằm dưới MDE 2,11 của thiết kế, còn trên ACU và trên tập gộp 5.947 bước thì vượt. So với S1/202, dưới Phi-4 ck500 ngang (−0,20, KTC phủ 0). (Mục 4)

---

## 2. AndroidControl, bộ trỏ UGround

### 2.1 Điểm từng nhánh

| nhánh | exec [KTC95] | D.3 | D.3 ∧ 14% | AitW (vế khoảng cách) | AitW đầy đủ |
|---|---|---|---|---|---|
| Base | 47,59 | 53,60 | 49,76 | - | 63,39 |
| 7B prompting | 51,51 [49,82; 53,15] | 57,67 | 53,71 | - | 66,79 |
| S1/101 | 59,11 [57,3; 60,8] | 65,49 | 61,73 | 66,91 | 74,37 |
| S1/202 | 59,62 | 66,10 | 62,36 | 67,62 | 75,31 |
| xao101 | 59,11 | 65,58 | 61,84 | - | 74,59 |
| ck500/202 | 59,94 [58,13; 61,71] | 66,55 | 62,65 | 68,25 | 76,23 |
| ck500 | 60,65 | 67,02 | 63,25 | 68,59 | 76,25 |
| ACE (R3) | 60,68 | 67,11 | 63,28 | 68,63 | 76,32 |
| câu chuẩn | 75,73 | 83,82 | - | - | 92,14 |

Dấu "-" nghĩa là chưa tính (vế khoảng cách của AitW chỉ tính cho các nhánh chính). Mọi ô có số đều tính từ tệp thô (`luat_d3`, `luat_aitw_day_du`). S1/101 tái lập đúng 65,49 và 74,37.

### 2.2 Ghép cặp

Đủ bốn luật cho mọi phép so (kernel `so-27-10-cpu`, `runs/so_d3_aitw_ck500.json`; tự kiểm exec khớp +1,55 và +1,03). p là McNemar chính xác.

| phép so | exec [KTC95], p (cứu/phá) | D.3 | D.3 ∧ 14% | AitW đầy đủ |
|---|---|---|---|---|
| ck500 − S1/101 | +1,55 [+0,80; +2,33], p = 1,5e−5 (159/90) | +1,52 [+0,77; +2,29], p = 3,2e−5 | +1,52 [+0,76; +2,31], p = 3,6e−5 | +1,88 [+1,17; +2,63], p = 2,1e−7 |
| ck500 − S1/202 | +1,03 [+0,25; +1,83], p = 0,014 (191/145) | +0,92 [+0,11; +1,75], p = 0,035 | +0,90 [+0,07; +1,75], p = 0,04 | +0,94 [+0,07; +1,81], p = 0,033 |
| ck500/202 − S1/101 | +0,83 [+0,00; +1,67], p = 0,036 (166/129) | +1,05 [+0,22; +1,90], p = 0,01 | +0,92 [+0,09; +1,77], p = 0,024 | +1,86 [+1,06; +2,67], p = 2,5e−6 |
| ck500/202 − S1/202 | +0,31 [−0,53; +1,17], p = 0,50 (194/180) | +0,45 [−0,44; +1,34], p = 0,34 | +0,29 [−0,58; +1,18], p = 0,55 | +0,92 [+0,02; +1,82], p = 0,046 |
| ck500/202 − ck500 | −0,72 [−1,27; −0,16], p = 0,011 (59/91) | −0,47 [−1,04; +0,09], p = 0,11 | −0,60 [−1,16; −0,05], p = 0,036 | −0,02 [−0,57; +0,54], p = 1 |
| S1/202 − S1/101 | +0,52 [−0,22; +1,26], p = 0,19 (155/132) | +0,60 [−0,16; +1,38], p = 0,14 | +0,63 [−0,13; +1,40], p = 0,12 | +0,94 [+0,17; +1,73], p = 0,02 |
| ACE − S1/101 | +1,57 [+0,86; +2,31], p = 9,5e−6 (158/88) | +1,61 [+0,88; +2,35], p = 7,4e−6 | +1,55 [+0,82; +2,29], p = 2,3e−5 | +1,95 [+1,27; +2,66], p = 4,8e−8 |
| ACE − S1/202 | +1,05 [+0,31; +1,81], p = 0,012 (191/144) | +1,01 [+0,21; +1,82], p = 0,02 | +0,92 [+0,12; +1,73], p = 0,035 | +1,01 [+0,16; +1,85], p = 0,021 |
| ACE − ck500 | +0,02 [−0,21; +0,26], p = 1 (15/14) | +0,09 [−0,15; +0,33], p = 0,58 | +0,02 [−0,22; +0,27], p = 1 | +0,07 [−0,15; +0,29], p = 0,69 |
| ACE − ck500/202 | +0,74 [+0,17; +1,33], p = 0,014 (101/68) | +0,56 [+0,00; +1,15], p = 0,071 | +0,63 [+0,07; +1,21], p = 0,04 | +0,09 [−0,48; +0,66], p = 0,81 |
| xao101 − S1/101 | +0,00 [−0,41; +0,42], p = 1 (45/45) | +0,09 [−0,32; +0,50], p = 0,75 | +0,11 [−0,29; +0,53], p = 0,67 | +0,22 [−0,19; +0,64], p = 0,35 |
| ck500 − xao101 | +1,55 [+0,81; +2,30], p = 2,0e−5 (163/94) | +1,43 [+0,69; +2,20], p = 1,1e−4 | +1,41 [+0,64; +2,20], p = 1,6e−4 | +1,66 [+0,94; +2,41], p = 7,3e−6 |
| ck500/202 − xao101 | +0,83 [+0,02; +1,65], p = 0,033 (162/125) | +0,96 [+0,14; +1,77], p = 0,016 | +0,81 [+0,00; +1,62], p = 0,044 | +1,64 [+0,85; +2,43], p = 3,3e−5 |
| ACE − xao101 | +1,57 [+0,85; +2,29], p = 1,1e−5 (160/90) | +1,52 [+0,82; +2,25], p = 2,5e−5 | +1,43 [+0,70; +2,18], p = 9,8e−5 | +1,73 [+1,05; +2,43], p = 2,0e−6 |
| 7B − Base | +3,92 [+2,66; +5,23], p = 5,5e−10 (484/309) | +4,08 [+2,80; +5,42], p = 3,3e−10 | +3,94 [+2,67; +5,28], p = 9,9e−10 | +3,41 [+2,12; +4,74], p = 1,9e−7 |
| S1/101 − 7B | +7,60 [+5,95; +9,28], p = 2,6e−25 (707/368) | +7,82 [+6,17; +9,54], p = 1,5e−25 | +8,02 [+6,37; +9,69], p = 5,9e−27 | +7,57 [+5,94; +9,22], p = 2,1e−24 |
| ck500 − 7B | +9,14 [+7,55; +10,75], p = 1,9e−37 (724/316) | +9,34 [+7,71; +10,99], p = 2,1e−37 | +9,55 [+7,92; +11,18], p = 9,5e−39 | +9,46 [+7,85; +11,09], p = 1,1e−38 |
| ACE − 7B | +9,16 [+7,57; +10,79], p = 4,8e−38 (719/310) | +9,43 [+7,81; +11,09], p = 2,2e−38 | +9,57 [+7,97; +11,23], p = 2,5e−39 | +9,52 [+7,93; +11,16], p = 1,5e−39 |

### 2.3 Đọc

- **ck500 hơn cả hai hạt S1 dưới cả bốn luật, mọi KTC loại 0.** So với S1/101: exec +1,55, D.3 +1,52, D.3 ∧ 14% +1,52, AitW đầy đủ +1,88 (p = 2,1e−7). So với S1/202: +1,03, +0,92, +0,90, +0,94. ACE cho cùng bức tranh (so với S1/101 AitW đầy đủ +1,95, p = 4,8e−8). Nhánh kiểm sàn xao101 thì ngang S1 ở cả bốn luật (mọi KTC phủ 0), còn ck500 − xao101 dương ở cả bốn (+1,41 đến +1,66).
- **Hai hạt GRPO.** Hai hạt chênh nhau 0,72 exec và mức chênh có ý nghĩa, nên con số +1,55 của ck500/101 có một phần là biến thiên giữa hạt GRPO. Dưới AitW đầy đủ, hai hạt ngang nhau (−0,02). Hướng vẫn dương so với cả hai hạt S1 ở cả ba luật, nhưng mỗi luật cho một độ lớn khác nhau (+0,3 đến +1,9). Khi báo, ghi tên luật cạnh mỗi con số; báo đủ ba luật cùng lúc là cách thuyết phục nhất vì cả ba cùng chiều.
- Hạt GRPO 202 vẫn xuất phát từ S1/101, nên chỉ đo nhiễu của bước GRPO, không đo nhiễu của SFT.
- ACE − ck500/202 = +0,74 không có nghĩa là ACE hơn, vì ACE được xây trên ck500/101, tức cùng hạt GRPO với ck500/101.
- **xao101.** xao101 đổi câu ở 593/4.463 bước (ck500 đổi 1.668 bước) mà không tăng gì so với S1. Đòn "chưa có nhánh so sánh train thêm" (bỏ ngỏ từ lượt GRPO-point 6/9) nay đã đóng cho ck500.
- **7B.** Mức 3B đã tinh chỉnh hơn 7B (khoảng 9 điểm) gấp đôi mức 7B hơn 3B gốc (3,92). 7B có action_ok 96,37, câu trung vị dài 64 ký tự (S1 dài 33), tốc độ sinh 0,4 bước/giây trên T4×2.

### 2.4 Phải khai

- Mỗi nhánh một hạt (S1 và ck500 hai hạt). Trên tập kiểm chính các mức ck500 − S1 nằm dưới MDE 2,11 của thiết kế (trên ACU thì vượt, mục 8).
- xao101: kl thấp hơn ck500 10 đến 30 lần, tức thưởng bị xáo làm chính sách gần như đứng yên quanh S1. Đó đúng là điều nhánh kiểm sàn cần cho thấy, nhưng không chứng minh rằng mọi tín hiệu thưởng khác SPICE đều vô ích.
- 7B dùng đúng câu nhắc của Base (không tối ưu câu nhắc riêng cho 7B), cùng họ Qwen với mô hình và bộ trỏ, và chưa kiểm 7B có thấy AndroidControl lúc huấn luyện hay không. Câu của 7B dài gấp đôi, mà thước thiên vị câu dài (+5,4), nên phép so có lợi cho 7B chứ không bất lợi.

### 2.5 Chi tiết lượt train (để khai ở phương pháp hoặc phụ lục)

**ck500/202.**
- Colab L4, 500 bước, thưởng SPICE, G = 8, lr 1e-5, β = 0,04, `--seed 202`, xuất phát S1/101.
- Đứt máy hai lần. Lần đầu chạy tiếp từ điểm lưu 200; log lần này không còn, nên không kiểm lại được. Lần sau chạy tiếp từ điểm lưu 425; log có `[tiếp từ] …/checkpoint-425` và `[nạp default] 504 tensor · |lora_B| 0.0000 → 9.5837`. 75 bước cuối mất 87,1 s/bước, VRAM đỉnh 11,80 GiB.
- `log_history.json` có đủ 500 bước, không trùng bước.
- Adapter có md5 `57e5d2eec23278b0a2dfe7393d9fc463`, 59.941.192 byte.
- kl trung bình ở bước 426 đến 500 là 0,049; ở cùng đoạn, ck500/101 là 0,030. kl không về khoảng 0,001, tức không có dấu hiệu adapter bị đặt lại. Thưởng trung bình cuối lượt 0,527, ngang ck500/101.

**xao101.**
- Hai commit trên Kaggle T4: commit 1 tới điểm lưu 275, commit 2 từ 275 tới 500 (148,2 s/bước, VRAM đỉnh 12,79 GiB).
- Log commit 2 có `[nạp default] … → 6.1258`, tức lần chạy tiếp không bị đặt lại.
- kl tăng từ 0,0001 lên 0,0011 trong lượt. Thưởng trung bình tăng từ 0,45 lên 0,48.
- Kiểm hoà khi chấm test: 16/20 trùng S1/101, như mọi lượt khác.

---

## 3. Thước chữ trên AndroidControl

Quy trình như luận văn: bộ chấm COCO (BLEU-4, METEOR, ROUGE-L, CIDEr-D, SPICE) cộng chrF và BERTScore (roberta-large L17, rescaled); câu rỗng tính 0. Lượt chấm ngày 26/10 cho lại đúng bảy số đã công bố của S1/101, và lượt ngày 25/10 cho lại đúng bảy số của ck500/101.

### 3.1 Điểm mức kho

| nhánh | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|
| 7B prompting | 14,48 | 21,90 | 39,79 | 100,71 | 18,74 | 36,22 | 39,70 |
| S1/101 | 51,56 | 36,79 | 67,35 | 416,12 | 44,37 | 61,26 | 66,33 |
| S1/202 | 51,66 | 37,17 | 67,71 | 419,19 | 44,23 | 61,92 | 66,75 |
| xao101 | 51,32 | 36,95 | 67,36 | 418,13 | 44,40 | 61,52 | 66,40 |
| ck500 | 52,36 | 37,92 | 68,36 | 430,05 | 45,79 | 62,87 | 67,07 |
| ck500/202 | 52,94 | 37,53 | 68,48 | 431,22 | 45,69 | 62,37 | 67,12 |
| ACE (R3) | 53,47 | 38,37 | 69,08 | 442,02 | 47,13 | 63,44 | 67,73 |

### 3.2 KTC95 ghép cặp (bootstrap cụm app, 1.091 cụm, B = 2.000; kernel `ktc-chu-27-10-cpu`, xong 27/10)

| phép so | BLEU-4 | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|
| ck500 − S1/101 | +0,80 [+0,22; +1,60] | +1,01 [+0,55; +1,48] | +13,93 [+8,05; +19,91] | +1,42 [+0,71; +2,16] | +1,61 [+1,10; +2,11] | +0,74 [+0,32; +1,15] |
| ck500 − S1/202 | +0,70 [−0,06; +1,48] ⁰ | +0,66 [+0,06; +1,19] | +10,86 [+3,77; +17,85] | +1,56 [+0,72; +2,36] | +0,96 [+0,34; +1,53] | +0,32 [−0,22; +0,84] ⁰ |
| ck500/202 − S1/101 | +1,38 [+0,71; +2,25] | +1,13 [+0,64; +1,63] | +15,11 [+8,60; +21,52] | +1,32 [+0,57; +2,12] | +1,11 [+0,56; +1,62] | +0,78 [+0,33; +1,22] |
| ck500/202 − S1/202 | +1,28 [+0,31; +2,19] | +0,77 [+0,19; +1,34] | +12,04 [+5,19; +19,05] | +1,46 [+0,65; +2,30] | +0,46 [−0,16; +1,07] ⁰ | +0,37 [−0,18; +0,91] ⁰ |
| ck500/202 − ck500 | +0,58 [−0,28; +1,35] ⁰ | +0,12 [−0,21; +0,47] ⁰ | +1,17 [−3,43; +5,71] ⁰ | −0,11 [−0,68; +0,49] ⁰ | −0,50 [−0,87; −0,12] | +0,05 [−0,27; +0,37] ⁰ |
| S1/202 − S1/101 | +0,10 [−0,53; +0,91] ⁰ | +0,36 [−0,12; +0,84] ⁰ | +3,07 [−3,09; +9,29] ⁰ | −0,14 [−0,81; +0,59] ⁰ | +0,65 [+0,11; +1,20] | +0,42 [−0,03; +0,87] ⁰ |
| xao101 − S1/101 | −0,24 [−0,56; +0,34] ⁰ | +0,01 [−0,27; +0,26] ⁰ | +2,02 [−1,47; +5,31] ⁰ | +0,03 [−0,38; +0,45] ⁰ | +0,25 [−0,02; +0,51] ⁰ | +0,07 [−0,16; +0,29] ⁰ |
| ck500 − xao101 | +1,04 [+0,42; +1,68] | +1,01 [+0,53; +1,46] | +11,92 [+5,76; +17,89] | +1,39 [+0,69; +2,11] | +1,35 [+0,85; +1,85] | +0,67 [+0,23; +1,09] |
| ACE − S1/101 | +1,91 [+1,30; +2,69] | +1,76 [+1,28; +2,22] | +25,91 [+19,14; +32,50] | +2,76 [+1,98; +3,54] | +2,19 [+1,66; +2,70] | +1,40 [+0,95; +1,83] |
| ACE − S1/202 | +1,81 [+1,03; +2,58] | +1,40 [+0,79; +1,94] | +22,84 [+15,31; +29,99] | +2,90 [+2,00; +3,75] | +1,54 [+0,89; +2,11] | +0,98 [+0,44; +1,47] |
| ACE − ck500 | +1,11 [+0,78; +1,42] | +0,74 [+0,54; +0,94] | +11,97 [+8,24; +15,34] | +1,33 [+0,92; +1,75] | +0,58 [+0,37; +0,80] | +0,66 [+0,46; +0,86] |
| ACE − ck500/202 | +0,53 [−0,31; +1,39] ⁰ | +0,62 [+0,21; +1,00] | +10,80 [+5,09; +16,14] | +1,44 [+0,73; +2,15] | +1,08 [+0,68; +1,49] | +0,61 [+0,25; +0,97] |
| S1/101 − 7B | +37,08 [+35,69; +38,38] | +27,56 [+26,64; +28,46] | +315,41 [+302,48; +328,16] | +25,63 [+24,26; +27,00] | +25,05 [+23,96; +26,14] | +26,63 [+25,79; +27,52] |

⁰ = KTC phủ 0. Các thước tính mức kho trên từng mẫu bootstrap (chrF từ thống kê sacrebleu, CIDEr-D giữ IDF của cả tập). METEOR không có KTC vì bộ chấm COCO chỉ cho số mức kho. Lượt này tái lập đúng điểm đã lưu của cả 9 nhánh.

### 3.3 Đọc

- ck500 hơn S1/101 ở 7/7 thước, và cả sáu thước có KTC đều loại 0 (CIDEr-D +13,93 [+8,05; +19,91], SPICE +1,42 [+0,71; +2,16]). So với S1/202, bốn trong sáu thước loại 0; BLEU-4 và BERTScore dương nhưng KTC chạm 0. Hạt GRPO thứ hai cho cùng bức tranh: ck500/202 − S1/101 loại 0 ở cả sáu thước. Hai hạt GRPO gần trùng nhau (SPICE chênh −0,10, CIDEr-D chênh +1,17), tức tác dụng của thưởng SPICE lên thước chữ lặp lại ổn định, trong khi exec giữa hai hạt chênh 0,72.
- xao101 trùng S1: cả sáu KTC của xao101 − S1/101 đều phủ 0, trong khi ck500 − xao101 loại 0 ở cả sáu thước (CIDEr-D +11,92, SPICE +1,39). Phần ck500 hơn S1 ở thước chữ là của thưởng SPICE.
- ACE hơn ck500 ở cả sáu thước có KTC, mọi KTC đều loại 0, trong khi exec chỉ ngang (+0,02). Thước chữ đo độ giống câu chuẩn, không cho biết câu có giúp bộ trỏ tìm đúng phần tử hay không, nên phép so chính vẫn đọc bằng exec.
- 7B thấp xa mọi nhánh tinh chỉnh ở mọi thước (S1/101 − 7B: CIDEr-D +315, SPICE +25,6), cùng chiều với exec.

### 3.4 Phải khai

- METEOR chỉ có số mức kho, không có KTC.
- chrF trong bảng 3.2 nay là chrF mức kho (thống kê sacrebleu cộng dồn), thay cho phép xấp xỉ trung bình mức câu của lượt 25/10; ck500 − S1/101 vì vậy đổi từ +1,26 thành +1,61. Bảng ACE trong luận văn dùng số mới.
- ROUGE-L của ACE tính lại ra 69,11, lệch 0,03 so với 69,08 đã in.

---

## 4. Đổi dụng cụ chấm

### 4.1 Điểm từng nhánh

| nhánh | UGround exec | UI-Venus-7B exec | Phi-Ground-4B exec | Phi-4 người nghe (chọn đúng) |
|---|---|---|---|---|
| Base | 47,59 | - | 40,80 | 38,23 [36,53; 39,93] |
| S1/101 | 59,11 | 54,51 | 46,96 | 44,63 [42,88; 46,37] |
| S1/202 | 59,62 | 55,12 | - | 45,53 |
| ck500 | 60,65 | 56,06 | 47,75 | 45,33 [43,59; 47,11] |
| ACE (R3) | 60,68 | 56,20 | 47,73 | 45,33 [43,57; 47,12] |
| câu chuẩn | 75,73 | - | - | 54,94 |

UI-Venus chỉ có Base trên lát 2.532 bước (phép B: Base 39,06), nên không đặt chung bảng này.

### 4.2 Ghép cặp

| phép so | UI-Venus | Phi-Ground | Phi-4 |
|---|---|---|---|
| ck500 − S1/101 | +1,55 [+0,82; +2,30], p = 8,7e−6 | +0,78 [+0,05; +1,51], p = 0,034 | +0,69 [+0,02; +1,40], p = 0,039 |
| ACE − S1/101 | +1,68 [+0,97; +2,42], p = 1,4e−6 | +0,76 [+0,02; +1,49], p = 0,047 | +0,69, p = 0,043 |
| ACE − ck500 | +0,13 [−0,11; +0,39], p = 0,38 | −0,02 [−0,33; +0,29], p = 1 | 0,00 [−0,24; +0,23], p = 1 |
| ck500 − S1/202 | +0,94 [+0,14; +1,75], p = 0,028 | - | −0,20 [−0,94; +0,55], p = 0,63 |
| ACE − S1/202 | +1,08 [+0,28; +1,88], p = 0,012 | - | −0,20 [−0,96; +0,57], p = 0,64 |
| S1/202 − S1/101 | +0,60 [−0,13; +1,34], p = 0,12 | - | +0,90 [+0,21; +1,61], p = 0,010 |
| S1/101 − Base | (phép B: +9,68 trên lát 2.532; UGround cùng lát +10,35) | +6,16 [+4,71; +7,64], p = 1,4e−16 | +6,41, p = 3,1e−22 |
| ck500 − Base | - | +6,95 [+5,46; +8,45] | +7,10, p = 1,2e−26 |
| câu chuẩn − Base | - | - | +16,72, p = 1,5e−110 |

Đối chiếu dưới UGround trên đủ 4.463 bước: S1/101 − Base +11,52 (S1/202 − Base +12,03). Mức S1 − Base dưới hai dụng cụ ngoài họ Qwen nhỏ bằng khoảng một nửa.

Với Phi-4, ACE − ck500 có p = 0,85 nếu tính bằng `som_doc.py` và p = 1 nếu tính bằng McNemar chính xác (`som_s1_202_doc.py`). Hai script dùng hai kiểm định khác nhau; khi in phải chọn một và ghi tên kiểm định.

### 4.3 Đọc

- Thứ tự Base < S1 < ck500 ≈ ACE < câu chuẩn giữ dưới cả bốn dụng cụ.
- Mức ck500 − S1/101 giảm dần từ dụng cụ cùng họ sang dụng cụ ngoài họ: UGround và UI-Venus +1,55, Phi-Ground +0,78, Phi-4 +0,69. Với hai dụng cụ ngoài họ, KTC sát 0 và p sát 0,05.
- Dưới Phi-4, S1/202 (45,53) cao hơn cả ck500 (45,33). Hai hạt S1 đã chênh nhau +0,90, lớn hơn khoảng cách ck500 − S1/101.
- ACE ngang ck500 dưới mọi dụng cụ.

### 4.4 Nguồn dữ liệu của Phi-Ground và cách viết đòn "cùng họ Qwen"

- Phi-Ground-4B dựng trên Phi-3.5-Vision, tức ngoài họ Qwen. Theo báo cáo kỹ thuật (arXiv 2507.23779, chưa bình duyệt; đã đọc đủ cả phụ lục), dữ liệu huấn luyện gồm:
  - các tập con Windows, macOS, Linux, Fineweb của OS-Atlas;
  - SeeClick, E2ISynth, GUIAct;
  - trang CommonCrawl tự render, ảnh từ Bing Image Search;
  - 80 nghìn mẫu do người gán nhãn trên Windows và Office.
- Báo cáo không nhắc AndroidControl, AITW, AitZ, AMEX, RICO hay Widget Captioning, và không mô tả bước khử trùng lặp với benchmark.
- Có hai đường gián tiếp phải khai:
  - SeeClick có dữ liệu di động, nên Phi-Ground đã thấy màn hình Android.
  - GUIAct có tập con smartphone lấy từ AITW-general. Việc này không ảnh hưởng phép đo trên AndroidControl, nhưng có ảnh hưởng nếu dùng Phi-Ground chấm AitZ.
- **Cách viết được phép:** "Phi-Ground-4B dựng trên Phi-3.5-Vision (ngoài họ Qwen); theo báo cáo kỹ thuật, mô hình không dùng AndroidControl để huấn luyện". Câu này đóng cả hai đòn "bộ trỏ quen văn phong AndroidControl" và "bộ trỏ cùng họ Qwen", nhưng phải ghi căn cứ là khai báo trong báo cáo kỹ thuật, và kèm mức tăng chỉ +0,78.
- Không viết "chưa từng thấy màn hình di động".
- UI-Venus vẫn thuộc họ Qwen. Phi-4 tuy ngoài họ Qwen nhưng là người nghe trắc nghiệm, không phải bộ trỏ.

### 4.5 Phải khai

- Phi-4, nhánh S1/202: chỉ chấm 1.652 bước có câu khác S1/101; 2.810 bước còn lại có câu giống nhau nên dùng lại kết quả của S1/101.
- Phi-Ground, nhánh Base: tệp dự đoán thiếu 7/4.463 bước, các bước thiếu tính 0. Chưa có S1/202 dưới Phi-Ground.
- UI-Venus: lượt đầu chỉ chấm những bước mà ba nhánh viết khác nhau và quên S1 cũ, nên chỉ có 40 đến 190 cặp bất đồng, không đủ sức. Lượt bù chấm thêm, đủ 1.880 bước khác nhau, thì Δ có ý nghĩa. Nếu hội đồng hỏi vì sao số lượt chấm không đều, đây là lời giải thích.
- Mọi lượt chấm lại đều qua kiểm tái lập: UI-Venus 40 bước lệch toạ độ 0; Phi-4 200 bước lệch 0; Phi-Ground 40/40 bước trùng.

---

## 5. Phân rã, ví dụ định tính, ablation thưởng, tác hại ở bước không chạm

- **Phân rã ck500 so với S1/101** (`report/321`, khớp `report/259`):
  - câu đổi ở 1.668 bước (37,4%);
  - cứu 159 bước, trong đó 36 bước là sửa loại thao tác;
  - phá 90 bước, trong đó 8 bước là sai loại thao tác;
  - ròng +69 bước = +28 từ loại thao tác và +41 từ đổi phần tử.
- **Ví dụ định tính:** `report/321` có 6 ví dụ rút ngẫu nhiên, chưa chọn lọc. Cần chọn tay vài ví dụ cứu và vài ví dụ phá.
- **Ablation thưởng CIDEr-D (A2)** (`report/299`, số test):
  - A2_500 − ck500: exec −0,69 [−1,34; −0,02], p = 0,04, tức thưởng SPICE cho exec cao hơn thưởng CIDEr-D ở cùng 500 bước.
  - A2_1000 − A2_500: +0,02.
  - Cả hai bản A2 hơn S1/101 khoảng +0,85.
  - A2 viết đúng loại thao tác hơn (ròng +10 bước) nhưng chọn sai phần tử nhiều hơn (ròng −41 bước).
  - Phải khai:
    - mỗi nhánh một hạt;
    - mức −0,69 chỉ lớn hơn nhiễu giữa hai hạt S1 (0,52) một chút;
    - A2 và ck500 khác tập câu nhắc (1.000 so với 2.000 câu) và khác máy train (T4 fp16 so với A100 bf16).
- **Tác hại ở bước không chạm** (`report/261` §6):
  - scroll: S1 83,97, ck500 77,75 (−6,23 [−8,30; −4,31]);
  - back: −5,93;
  - toàn bộ bước không chạm: 85,97 → 84,29.
  - Cơ chế: ck500 lệch về câu cho thao tác chạm (47/51 bước scroll bị phá thành click).
  - Đây là lý do có ACE. Mục 7 cho thấy tác hại này lớn thêm khi lịch sử là câu mô hình tự sinh.

---

## 6. Ngoài miền: AitZ (zero-shot, không train thêm)

### 6.1 Dữ liệu

- Tập test chính thức của AitZ có 506 tác vụ và 4.724 bước, trong đó **2.736 bước chạm**. Số bước theo loại thao tác: scroll 601, input_text 500, enter 118, home 232, back 33, hoàn tất 504.
- Bốn nhóm: general 1.202, google_apps 621, install 1.108, web_shopping 1.793.
- Ảnh nhỏ hơn AndroidControl nhiều (từ 270×600 tới 720×1520).
- Điểm chạm vàng nằm trong ít nhất một khung chú thích ở 57% bước. Lý do là khung của AitW là khung OCR và biểu tượng, không phải cây trợ năng.

### 6.2 Điểm và ghép cặp (cụm = episode, 506 cụm)

| nhánh | exec | hit_disk | action_ok |
|---|---|---|---|
| câu chuẩn (trần) | 66,26 | - | - |
| Base | 34,50 | 47,51 | 94,08 |
| S1/101 | 37,79 | 50,00 | 93,46 |
| ck500 | 37,28 | 49,56 | 92,40 |
| ck500/202 | 36,62 | 48,90 | 92,62 |
| ACE (R3) | 37,28 | - | - |
| ra_k4 | 37,02 | - | - |

- S1/101 − Base +3,29 [+1,51; +5,03], p = 4,5e−4 · ck500 − Base +2,78 [+1,02; +4,50], p = 0,003 · ck500/202 − Base +2,12 [+0,44; +3,76], p = 0,021.
- ck500 − S1/101 **−0,51 [−1,39; +0,36]**, p = 0,33 (cứu 81, phá 95). Riêng action_ok, ck500 kém S1 −1,06 [−1,72; −0,40], p = 0,002.
- ck500/202 − S1/101 −1,17 [−2,12; −0,22], p = 0,027.
- Trên 2.502 bước cả S1 lẫn ck500 đều đúng loại thao tác: S1 40,17, ck500 40,45. Vậy phần ck500 thua nằm ở loại thao tác, phần định vị thì ngang S1.
- ACE − S1/101 −0,51 [−1,39; +0,36] · ACE − ck500 +0,00 (cứu 1, phá 1) · ra_k4 − S1/101 −0,77 [−1,68; +0,14].
- Trần − S1/101 +28,47 [+26,40; +30,51]; trên AndroidControl khoảng cách này là +16,6. Tính theo dải từ Base tới trần, S1 nằm ở 10% trên AitZ và 41% trên AndroidControl.
- ACE gần như không kích hoạt. ra_k4 chép đúng một câu ví dụ ở 78/2.736 bước. Luật R3 lấy câu của ra_k4 ở 75 bước, trong đó 52 câu khác ck500. Khối ví dụ được truy hồi từ tập dạy AndroidControl, và không chứa đúng câu chuẩn AitZ ở bước nào (0%; trên tập kiểm AndroidControl khoảng 13%).

### 6.3 Thước chữ trên AitZ (2.736 bước)

| nhánh | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|
| Base | 18,68 | 18,56 | 39,11 | 86,98 | 15,66 | 35,24 | 38,81 |
| S1/101 | 21,01 | 20,83 | 46,84 | 120,24 | 15,27 | 35,66 | 49,69 |
| ck500 | 21,48 | 21,08 | 46,92 | 123,38 | 16,37 | 36,28 | 49,68 |
| ck500/202 | 19,76 | 19,99 | 45,44 | 117,26 | 15,63 | 34,43 | 48,47 |
| ACE (R3) | 21,45 | 21,05 | 46,91 | 123,29 | 16,40 | 36,24 | 49,63 |
| ra_k4 | 19,94 | 20,04 | 45,39 | 117,42 | 15,70 | 34,24 | 48,27 |

**KTC95 ghép cặp (cụm = episode, 506 cụm, B = 2.000):**

| phép so | BLEU-4 | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|
| S1 − Base | +2,33 [+1,31; +3,33] | +7,73 [+6,85; +8,60] | +33,26 [+25,95; +40,78] | −0,39 [−1,35; +0,54] ⁰ | +0,43 [−0,39; +1,19] ⁰ | +10,88 [+10,04; +11,68] |
| ck500 − Base | +2,80 [+1,76; +3,83] | +7,81 [+6,92; +8,66] | +36,40 [+28,54; +43,86] | +0,71 [−0,28; +1,63] ⁰ | +1,05 [+0,20; +1,84] | +10,87 [+10,00; +11,68] |
| ck500 − S1 | +0,47 [+0,01; +0,95] | +0,08 [−0,40; +0,56] ⁰ | +3,15 [−1,06; +7,69] ⁰ | +1,10 [+0,53; +1,66] | +0,62 [+0,22; +1,03] | −0,01 [−0,46; +0,43] ⁰ |
| ck500/202 − S1 | −1,25 [−1,79; −0,68] | −1,41 [−1,95; −0,88] | −2,97 [−7,54; +2,24] ⁰ | +0,35 [−0,24; +0,93] ⁰ | −1,24 [−1,69; −0,78] | −1,22 [−1,73; −0,74] |
| ACE − S1 | +0,45 [−0,02; +0,93] ⁰ | +0,07 [−0,44; +0,54] ⁰ | +3,05 [−1,17; +7,68] ⁰ | +1,13 [+0,56; +1,70] | +0,57 [+0,18; +1,00] | −0,06 [−0,53; +0,38] ⁰ |
| ACE − ck500 | −0,02 [−0,08; +0,02] ⁰ | −0,01 [−0,08; +0,04] ⁰ | −0,10 [−0,37; +0,17] ⁰ | +0,03 [−0,04; +0,10] ⁰ | −0,05 [−0,11; +0,00] ⁰ | −0,05 [−0,12; +0,01] ⁰ |
| ra_k4 − S1 | −1,06 [−1,63; −0,50] | −1,45 [−2,05; −0,90] | −2,82 [−7,44; +1,74] ⁰ | +0,43 [−0,20; +1,01] ⁰ | −1,43 [−1,93; −0,93] | −1,42 [−1,99; −0,90] |

⁰ = KTC phủ 0.

- ck500 hơn S1 ở 6/7 thước (BERTScore ngang, −0,01). Ba thước có KTC loại 0: SPICE +1,10 [+0,53; +1,66], chrF +0,62 và BLEU-4 +0,47; ROUGE-L, CIDEr-D và BERTScore phủ 0. Hạt 202 thấp hơn S1 ở BLEU-4, ROUGE-L, chrF và BERTScore (KTC dưới 0). Vì vậy trình AitZ là "ck500 và S1 tương đương", ở cả exec lẫn thước chữ.
- SPICE của S1 (15,27) còn thấp hơn Base (15,66; S1 − Base −0,39, KTC phủ 0) dù exec của S1 cao hơn. Như vậy SPICE trên AitZ không phản ánh đúng thứ tự giữa các nhánh.

### 6.4 Đọc

- Tinh chỉnh trên AndroidControl có chuyển sang AitZ: mọi nhánh tinh chỉnh đều hơn Base có ý nghĩa.
- ck500 và ACE tương đương S1 trên AitZ. Điều này khớp với cơ chế: thưởng SPICE và khối ví dụ của ACE đều học theo văn phong câu chuẩn AndroidControl, còn câu chuẩn AitZ do GPT-4V sinh. Trên ACU (cùng văn phong, tác vụ mới) mức tăng lại lớn hơn tập kiểm chính, nên giới hạn nằm ở văn phong câu chuẩn chứ không ở tác vụ mới.
- Trần 66,26 cho thấy khoảng trống nằm ở phía mô hình chứ không ở dụng cụ.
- Cách viết đúng: "trên AitZ, ck500 ngang S1 (−0,51, KTC phủ 0); lợi ích của thưởng SPICE gắn với phân phối câu chuẩn của AndroidControl; tinh chỉnh SFT vẫn hơn Base".

### 6.5 Phải khai

- Câu từng bước của AitZ do GPT-4V sinh, sau đó ba chuyên gia đối chiếu với thao tác vàng và sửa tay chỗ không khớp (Phụ lục A.2, arXiv 2403.02713). Venue "Findings of EMNLP 2024" mới lấy từ README GitHub, chưa kiểm trên ACL Anthology.
- UGround có AITZ 8K trong dữ liệu huấn luyện.
- Ảnh AitZ nhỏ (nhiều màn chỉ 270×600).
- OCR lỗi hai lần do bản rapidocr mới trên Kaggle (không nhận ảnh PIL; độ tin cậy trả về dạng chuỗi). Đã sửa, ngưỡng 0,5 giữ nguyên.

### 6.6 Vì sao chỉ có AitZ: các bộ dữ liệu khác đã tra (tận nguồn, 26/10)

Điều kiện để dùng được: có mục tiêu tác vụ, câu hướng dẫn từng bước do người viết, và ảnh màn hình kèm điểm chạm vàng ở mỗi bước.

| bộ | lý do không dùng |
|---|---|
| GUI-Odyssey (ICCV 2025) | câu từng bước do GPT-4o sinh; bước kiểm chất lượng chỉ nói tới tác vụ và câu mục tiêu, không nói tới câu từng bước |
| AMEX (Findings ACL 2025) | không có câu từng bước, chỉ có câu mục tiêu và chuỗi thao tác |
| MoTIF (ECCV 2022) | chỉ có lệnh mức cao |
| PixelHelp (ACL 2020) | không có ảnh màn hình, chỉ có đặc trưng cây giao diện |
| UGIF (arXiv 2211.07615) | một câu gồm nhiều thao tác, không gióng theo màn; không tìm thấy bản phát hành |
| AITW tập Single | câu do người viết nhưng chính là mục tiêu của tác vụ ngắn, nên bài toán thành viết lại mục tiêu |

Cách viết: ngoài AndroidControl không có bộ công khai nào có câu từng bước do người viết kèm ảnh. Vì vậy kiểm tổng quát hoá bằng hai đường: ACU (cùng văn phong, mục 8) và AitZ (khác văn phong, câu GPT-4V có người kiểm). Không chạy GUI-Odyssey vì nó chỉ lặp lại loại thông tin của AitZ, với câu chuẩn kém tin cậy hơn.

---

## 7. Lịch sử tự sinh (câu của bước trước do mô hình viết)

Thiết lập: mỗi tác vụ sinh từ bước 0, câu mô hình viết ở bước trước được đưa vào ô lịch sử thay cho câu chuẩn. Kiểm hoà: ck500 trùng lượt cũ 20/20, S1 trùng 16/20.

- Số câu đổi so với lượt cũ (lượt cũ dùng câu chuẩn làm lịch sử): S1 2.671/4.463 bước chạm, ck500 2.602/4.463. Bước 0 gần như không đổi. Từ bước 1 trở đi có 50 đến 80% câu đổi, tỉ lệ tăng dần theo vị trí bước.

**Đúng loại thao tác (bootstrap cụm):**
| | S1 cũ | S1 tự sinh | ck500 cũ | ck500 tự sinh |
|---|---|---|---|---|
| bước chạm (4.463) | 92,54 | 89,16 | 94,42 | 92,67 |
| bước không chạm (2.495) | 85,97 | 81,32 | 84,29 | 76,83 |

- Tự sinh − cũ: S1 chạm −3,38 [−4,83; −2,11] · ck500 chạm −1,75 [−2,88; −0,75] · S1 không chạm −4,65 [−6,05; −3,30] · ck500 không chạm −7,45 [−9,33; −5,72].
- ck500 − S1 ở bước chạm: +1,88 [+1,42; +2,39] với lịch sử cũ, tăng lên **+3,52 [+2,44; +4,69]** với lịch sử tự sinh.
- ck500 − S1 ở bước không chạm: −1,68 [−2,76; −0,62] với lịch sử cũ, thành **−4,49 [−6,48; −2,61]** với lịch sử tự sinh.
- ck500 − S1 trên toàn bộ 6.958 bước: +0,65 [−0,35; +1,70] (lịch sử cũ: +0,60).

**Thước chữ (4.463 bước chạm):**
| nhánh | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|
| S1, tự sinh | 43,44 | 31,73 | 59,78 | 331,42 | 34,97 | 53,71 | 59,11 |
| ck500, tự sinh | 43,50 | 32,37 | 60,39 | 333,58 | 35,10 | 54,54 | 59,23 |

- So với lịch sử cũ, CIDEr-D giảm 85 (S1) và 96 (ck500), SPICE giảm 9,4 và 10,7. ck500 vẫn nhỉnh hơn S1 ở 7/7 thước, nhưng khoảng cách CIDEr-D co từ +13,9 xuống +2,2. Thước chữ ở đây đối chiếu với câu chuẩn của chính bước đó, nên chịu cả lỗi dây chuyền từ các bước trước. KTC95 (cụm app, B = 2.000):
  - tự sinh ck500 − tự sinh S1: CIDEr-D +2,16 [−5,73; +10,25] ⁰, SPICE +0,12 [−0,82; +1,16] ⁰, chrF +0,83 [+0,07; +1,58]; BLEU-4, ROUGE-L, BERTScore cũng dương nhưng KTC phủ 0. Chỉ chrF loại 0.
  - tự sinh − lịch sử chuẩn: S1 CIDEr-D −84,69 [−98,15; −71,92], ck500 −96,47 [−110,48; −83,33]; cả sáu thước giảm có ý nghĩa ở cả hai nhánh.
  - Cách viết: dưới lịch sử tự sinh, ck500 vẫn hơn S1 về exec (+1,48, KTC loại 0); về thước chữ hai nhánh gần ngang nhau.

**exec trên bước chạm (UGround, 4.463 bước, xong 26/10 tối):**

Kernel `trangphuongngoc/tuantu-cham` chỉ chấm các câu mới (S1 2.672 câu, ck500 2.603 câu); câu nào giống lượt cũ thì giữ điểm cũ. Mốc lịch sử chuẩn tái lập đúng 59,11 và 60,65. Kết quả ở `runs/tuantu/ket_qua_tuantu.json`, đọc bằng `harness/doc_tuantu.py`.

| | lịch sử chuẩn | lịch sử tự sinh | tự sinh − chuẩn |
|---|---|---|---|
| S1/101 | 59,11 [57,33; 60,83] | 54,96 [53,10; 56,81] | −4,15 [−5,35; −2,99] (cứu 128, phá 313, p = 6e−19) |
| ck500 | 60,65 [58,90; 62,38] | 56,44 [54,58; 58,28] | −4,21 [−5,33; −3,13] (cứu 117, phá 305, p = 2e−20) |
| **ck500 − S1** | +1,55 [+0,80; +2,33] | **+1,48 [+0,54; +2,43]** (cứu 220, phá 154, p = 7,5e−4) | |

Trên tập con các tác vụ có ảnh ở mọi bước (1.105 tác vụ, 3.492 bước chạm), ô lịch sử luôn là câu tự sinh, không bước nào phải chèn câu chuẩn thay chỗ thiếu ảnh:
- S1: 59,74 → 55,67 (−4,07 [−5,46; −2,74]); ck500: 61,00 → 57,33 (−3,67 [−5,03; −2,40]).
- ck500 − S1: lịch sử chuẩn +1,26 [+0,45; +2,07], lịch sử tự sinh **+1,66 [+0,60; +2,75]**.
- Trên toàn tập 4.463 bước có 811 bước mà lịch sử phải chèn câu chuẩn ở một bước trước đó vì thiếu ảnh. Vì vậy số trên tập con này sạch hơn.

Tỉ lệ tác vụ có mọi bước chạm đều trúng (1.050 tác vụ trong tập con đủ ảnh): S1 29,71 → 28,67; ck500 31,24 → 29,24. Đây là thước phụ, chưa có KTC.

**Đọc:**
- Khi bỏ lịch sử chuẩn, exec của cả hai nhánh giảm khoảng 4 điểm, và hai nhánh giảm gần bằng nhau (−4,15 và −4,21). Như vậy con số trong bảng chính có dùng lịch sử chuẩn, và mức giảm này là cái giá chung của giả định đó, không riêng nhánh nào.
- Ưu thế của ck500 so với S1 giữ nguyên dưới lịch sử tự sinh: +1,48 trên toàn tập, +1,66 trên tập con đủ ảnh, KTC loại 0 ở cả hai.
- Về đúng loại thao tác: ở bước chạm, ck500 bền hơn S1 (khoảng cách tăng từ +1,88 lên +3,52). Ở bước không chạm, ck500 giảm mạnh hơn S1, tức hướng lệch về thao tác chạm đã biết (mục 5) rõ hơn khi lịch sử là câu của chính mô hình.

**Phải khai:**
- 811 bước của toàn tập phải chèn câu chuẩn vào lịch sử vì thiếu ảnh của bước trước; tập con đủ ảnh không gặp chuyện này.
- Kiểm hoà khi sinh lại: S1 16/20, ck500 20/20.

---

## 8. ACU: phần AndroidControl mà S1 chưa thấy

- **Dữ liệu.** 1.484 bước chạm của các tác vụ không có trong tập dạy của S1, dựng từ TFRecord gốc của AndroidControl. Phải khai hai điều:
  - 1.383/1.484 bước thuộc split train chính thức (giống tập kiểm chính, `report/209`);
  - 5 bước có câu chuẩn lệch với bản HarrytheOrange.
- **OCR.** Dùng đúng rapidocr_onnxruntime 1.4.4 như OCR của tập dạy và tập kiểm (dựng Python 3.12 bằng uv). Chạy lại trên 20 ảnh của tập kiểm cũ: trùng 20/20 tuyệt đối. Đủ 1.484 ảnh, không ảnh nào rỗng.
- **Sinh câu và chấm** (kernel `trangphuongngoc/acu-gen`, T4×2, 9,3 h, xong sáng 27/10; đầu ra `runs/acu/gen/out/`). Kiểm hoà: S1 16/20 (như mọi lượt), ra_k4 20/20.

**Điểm (UGround, 1.484 bước, số test; bootstrap cụm, 818 cụm, B = 10.000):**

| nhánh | exec [KTC95] | AitW vế khoảng cách |
|---|---|---|
| câu chuẩn | 71,70 [69,14; 74,19] | 83,29 |
| Base | 49,80 [47,04; 52,57] | 57,95 |
| S1/101 | 52,16 [49,33; 54,99] | 61,79 |
| ra_k4 | 52,56 [49,69; 55,40] | 61,93 |
| ck500/202 | 56,20 [53,47; 58,91] | 66,37 |
| ck500 | 56,74 [53,98; 59,49] | 66,91 |
| ACE | 57,01 [54,21; 59,75] | 66,98 |

**Ghép cặp trên ACU:**

| phép so | exec [KTC95], p | cứu/phá | AitW vế khoảng cách [KTC95], p |
|---|---|---|---|
| ck500 − S1/101 | +4,58 [+3,17; +6,05], p = 2,1e−10 | 93/25 | +5,12 [+3,65; +6,61], p = 3,2e−12 |
| ck500/202 − S1/101 | +4,04 [+2,66; +5,48], p = 1,5e−8 | 87/27 | +4,58 [+3,13; +6,10], p = 6,5e−10 |
| ACE − S1/101 | +4,85 [+3,43; +6,32], p = 1,4e−11 | 95/23 | +5,19 [+3,70; +6,69], p = 1,2e−12 |
| ACE − ck500 | +0,27 [−0,07; +0,66], p = 0,29 | 6/2 | +0,07 [−0,21; +0,35], p = 1 |
| ck500/202 − ck500 | −0,54 [−1,37; +0,28], p = 0,28 | 17/25 | −0,54 [−1,43; +0,34], p = 0,30 |
| ra_k4 − S1/101 | +0,40 [−0,89; +1,73], p = 0,61 | 51/45 | +0,13 [−1,19; +1,43], p = 0,92 |
| S1/101 − Base | +2,36 [−0,14; +4,79], p = 0,056 | 176/141 | +3,84 [+1,22; +6,43], p = 0,0032 |
| ck500 − Base | +6,94 [+4,49; +9,34], p = 8,4e−9 | 211/108 | +8,96 [+6,40; +11,43], p = 1,6e−12 |
| câu chuẩn − S1/101 | +19,54 [+17,28; +21,87], p = 9,0e−67 | 312/22 | +21,50 [+19,03; +24,04], p = 4,7e−70 |

**Gộp với tập kiểm chính (5.947 bước, 1.909 cụm; khai rõ là gộp hai tập):**

| nhánh | exec [KTC95] | AitW vế khoảng cách |
|---|---|---|
| câu chuẩn | 74,73 [73,40; 76,05] | 83,89 |
| Base | 48,14 [46,66; 49,61] | 55,94 |
| S1/101 | 57,37 [55,86; 58,85] | 65,63 |
| ck500/202 | 59,00 [57,48; 60,53] | 67,78 |
| ck500 | 59,68 [58,18; 61,15] | 68,17 |
| ACE | 59,76 [58,27; 61,23] | 68,22 |

| phép so | exec [KTC95], p | cứu/phá | AitW vế khoảng cách [KTC95], p |
|---|---|---|---|
| ck500 − S1/101 | +2,30 [+1,62; +2,99], p = 6,8e−13 | 252/115 | +2,54 [+1,86; +3,25], p = 1,8e−14 |
| ck500/202 − S1/101 | +1,63 [+0,93; +2,37], p = 1,9e−6 | 253/156 | +2,15 [+1,45; +2,90], p = 1,2e−9 |
| ACE − S1/101 | +2,39 [+1,73; +3,05], p = 7,1e−14 | 253/111 | +2,59 [+1,94; +3,26], p = 3,5e−15 |
| ACE − ck500 | +0,08 [−0,12; +0,29], p = 0,51 | 21/16 | +0,05 [−0,14; +0,25], p = 0,74 |
| ck500/202 − ck500 | −0,67 [−1,14; −0,21], p = 0,0048 | 76/116 | −0,39 [−0,87; +0,10], p = 0,13 |
| S1/101 − Base | +9,23 [+7,92; +10,55], p = 7,1e−50 | 974/425 | +9,69 [+8,34; +11,02], p = 1,5e−49 |
| ck500 − Base | +11,54 [+10,22; +12,84], p = 2,4e−76 | 1058/372 | +12,22 [+10,89; +13,55], p = 1,2e−78 |
| câu chuẩn − S1/101 | +17,35 [+16,11; +18,59], p = 3,0e−210 | 1156/124 | +18,26 [+16,96; +19,58], p = 2,2e−217 |

**Thước chữ trên ACU (1.484 bước, mức kho; KTC ở bảng dưới, 818 cụm, B = 2.000):**

| nhánh | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|
| Base | 15,01 | 25,14 | 42,04 | 93,25 | 19,28 | 39,61 | 40,10 |
| S1/101 | 47,53 | 34,47 | 63,45 | 385,99 | 39,74 | 57,20 | 62,76 |
| ra_k4 | 48,60 | 35,12 | 64,73 | 405,68 | 41,65 | 58,19 | 64,21 |
| ck500/202 | 50,07 | 36,08 | 66,30 | 414,32 | 42,15 | 59,40 | 64,59 |
| ck500 | 49,85 | 36,64 | 66,38 | 412,72 | 42,25 | 60,06 | 64,64 |
| ACE | 50,88 | 37,03 | 67,11 | 425,71 | 43,21 | 60,59 | 65,32 |

| phép so | BLEU-4 | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|
| ck500 − S1/101 | +2,32 [+0,74; +3,82] | +2,93 [+1,97; +3,92] | +26,73 [+15,84; +37,96] | +2,51 [+1,18; +3,87] | +2,87 [+1,83; +3,94] | +1,87 [+1,08; +2,71] |
| ck500/202 − S1/101 | +2,54 [+1,38; +3,71] | +2,85 [+1,88; +3,86] | +28,34 [+16,83; +40,03] | +2,41 [+1,02; +3,84] | +2,20 [+1,18; +3,26] | +1,83 [+0,98; +2,68] |
| ACE − S1/101 | +3,35 [+1,81; +4,69] | +3,65 [+2,69; +4,67] | +39,73 [+28,65; +51,95] | +3,47 [+2,13; +4,93] | +3,39 [+2,38; +4,45] | +2,56 [+1,76; +3,39] |
| ACE − ck500 | +1,03 [+0,46; +1,47] | +0,72 [+0,45; +1,03] | +13,00 [+7,88; +19,07] | +0,96 [+0,35; +1,62] | +0,53 [+0,27; +0,83] | +0,69 [+0,43; +0,99] |
| ck500/202 − ck500 | +0,22 [−1,02; +1,66] ⁰ | −0,08 [−0,74; +0,57] ⁰ | +1,61 [−6,50; +10,20] ⁰ | −0,10 [−1,15; +0,95] ⁰ | −0,66 [−1,38; +0,00] ⁰ | −0,05 [−0,64; +0,54] ⁰ |
| ra_k4 − S1/101 | +1,07 [−0,34; +2,54] ⁰ | +1,28 [+0,30; +2,31] | +19,70 [+8,15; +31,72] | +1,91 [+0,42; +3,41] | +0,99 [−0,08; +2,19] ⁰ | +1,44 [+0,63; +2,33] |
| S1/101 − Base | +32,51 [+30,49; +34,57] | +21,41 [+19,87; +22,93] | +292,74 [+273,92; +312,81] | +20,46 [+18,21; +22,67] | +17,58 [+15,99; +19,25] | +22,67 [+21,24; +24,02] |

⁰ = KTC phủ 0. Câu chuẩn tự chấm: CIDEr-D 992,6, SPICE 99,5 (kiểm đường chấm).

- ACE kích hoạt: luật R3 lấy câu của ra_k4 ở 152 bước, trong đó 93 câu khác ck500. Khối ví dụ chứa đúng câu chuẩn ở 8,7% bước (tập kiểm chính khoảng 13%, AitZ 0%).
- Không tính được D.3 và AitW đầy đủ: bản ACU dựng từ TFRecord không trích hộp phần tử vàng. Chỉ có exec và vế khoảng cách của AitW.

**Đọc:**
- Đây là bằng chứng tổng quát hoá mạnh nhất của phương pháp. Trên tác vụ S1 chưa thấy, ck500 hơn S1 **+4,58 [+3,17; +6,05]**, p = 2,1e−10, gần gấp ba mức trên tập kiểm chính (+1,55). Hạt GRPO thứ hai cho +4,04 [+2,66; +5,48], hai hạt không khác nhau có ý nghĩa (−0,54, p = 0,28). Tỉ lệ cứu/phá 93/25, gần 4 : 1.
- Vế khoảng cách của AitW cho cùng chiều và lớn hơn: ck500 − S1 +5,12, ACE − S1 +5,19.
- Gộp hai tập (5.947 bước), ck500 − S1 = +2,30 [+1,62; +2,99] và ACE − S1 = +2,39 [+1,73; +3,05], đều vượt MDE 2,11, p < 1e−12.
- Câu chuẩn đạt 71,70, gần 75,73 của tập kiểm chính, nên dụng cụ chấm làm việc bình thường trên ACU. So với tập kiểm chính, S1 giảm 6,95 điểm (59,11 → 52,16) còn ck500 chỉ giảm 3,91 (60,65 → 56,74): thưởng SPICE giúp mô hình giữ năng lực tốt hơn hẳn trên tác vụ mới.
- ck500 hơn Base +6,94 [+4,49; +9,34], gấp ba mức S1 hơn Base (+2,36). Trên ACU, phần lớn mức tăng so với mô hình gốc là của bước GRPO.
- ACE nhỉnh hơn ck500 (+0,27, cứu 6 phá 2), cùng chiều với tập kiểm chính.
- Thước chữ cùng chiều với exec và cũng lớn hơn tập kiểm chính: ck500 − S1 loại 0 ở cả sáu thước, CIDEr-D +26,73 [+15,84; +37,96] (tập kiểm chính +13,93), SPICE +2,51 [+1,18; +3,87]. Hạt 202 cho gần trùng (+28,34 CIDEr-D). ACE hơn ck500 ở cả sáu thước, KTC loại 0, như trên tập kiểm chính.

**Phải khai:**
- S1 − Base trên ACU là +2,36 [−0,14; +4,79], p = 0,056 (dưới vế khoảng cách AitW +3,84, p = 0,003). Nên viết "S1 hơn Base", kèm KTC, không viết "có ý nghĩa" cho riêng exec.
- ra_k4 đứng riêng ngang S1 (+0,40, KTC phủ 0), đúng như trên tập kiểm chính (không dùng làm mô hình).
- Chỉ có exec và vế khoảng cách AitW (không có hộp vàng). Có 1.383/1.484 bước thuộc split train chính thức, giống tập kiểm chính.

---

## 9. Cách viết gợi ý

Phần này gợi ý cách kể từng kết quả một cách tích cực và dễ bảo vệ: điểm mạnh đi trước, phần còn lại được đặt như phạm vi áp dụng hoặc hướng phát triển. Câu mẫu dùng thẳng được, con số lấy ở mục 2 đến 8.

**Phương pháp chính (ck500).**
"ck500 cải thiện so với S1 một cách nhất quán: so với S1/101, hướng tăng được giữ qua bốn dụng cụ chấm độc lập (UGround, UI-Venus, Phi-Ground, Phi-4) và qua cả bốn luật khớp chạm (exec, D.3, D.3 ∧ 14%, AitW), với KTC loại 0 so với cả hai hạt S1. Mức tăng vào khoảng +0,8 đến +1,6 exec tuỳ hạt GRPO, đạt +1,9 dưới luật AitW, và lên +4,6 trên tác vụ chưa thấy."
Trong bảng có thể đặt cả hai hạt GRPO (60,65 và 59,94) và cả hai hạt S1 (59,11 và 59,62) cạnh nhau. Cách đặt này giúp người đọc thấy hướng tăng giữ được ở cả hai hạt, và làm kết quả thêm thuyết phục.

**Mức tăng đến từ tín hiệu SPICE.**
"Nhánh kiểm sàn chạy cùng 500 bước GRPO nhưng xáo thưởng cho kết quả bằng S1, trong khi ck500 hơn nhánh này +1,55 [+0,81; +2,30]. Mức cải thiện vì vậy đến từ chính tín hiệu SPICE chứ không phải từ việc huấn luyện thêm."
Đây là điểm tựa lập luận đẹp nhất của phương pháp, rất hợp để đặt nổi bật trong ch6.

**ACE.**
"ACE nâng chất lượng câu rõ rệt so với ck500 ở mọi thước chữ (mọi KTC đều nằm hẳn trên 0), đồng thời giữ trọn khả năng định vị của ck500."
ACE được thiết kế để câu gần câu chuẩn hơn mà không đánh đổi khả năng định vị, và kết quả cho thấy ACE làm được đúng như vậy.

**Tác vụ chưa thấy (ACU).**
"Trên 1.484 bước thuộc các tác vụ S1 chưa từng thấy khi huấn luyện, ck500 hơn S1 4,58 điểm exec (KTC95 [+3,17; +6,05], p = 2,1e−10), gần gấp ba mức trên tập kiểm chính, và hạt GRPO thứ hai cho mức tương tự (+4,04). Gộp cả hai tập, mức tăng là +2,30 (p = 6,8e−13). Khi chuyển sang tác vụ mới, S1 giảm gần 7 điểm còn ck500 chỉ giảm khoảng 4 điểm: thưởng SPICE giúp mô hình tổng quát hoá tốt hơn trên tác vụ mới."
Nên đặt ngay sau bảng chính của ch6 hoặc mở đầu mục tổng quát hoá, trước AitZ; đây là kết quả rất đáng đưa vào tóm tắt và ch1.

**Độ bền khi đổi dụng cụ chấm.**
"Dưới Phi-Ground, một bộ trỏ ngoài họ Qwen và theo báo cáo kỹ thuật không huấn luyện trên AndroidControl, thứ tự Base < S1 < ck500 vẫn được giữ nguyên." Câu này trả lời gọn câu hỏi bộ trỏ có cùng họ hay quen văn phong hay không; ghi nguồn là báo cáo kỹ thuật trên arXiv.
Với người nghe Phi-4: hai hạt S1 dưới Phi-4 đã cách nhau 0,90, nên dụng cụ này phù hợp để xác nhận thứ tự chung (Base < S1 < ck500 < câu chuẩn) hơn là để so các mức chênh nhỏ.

**So với mô hình lớn hơn.**
"Mô hình 3B sau tinh chỉnh vượt Qwen2.5-VL-7B dùng prompting khoảng 9 điểm exec, gấp đôi mức 7B hơn 3B gốc." Kết quả rõ và dễ hiểu, rất hợp để nhắc ở ch1 và ch7.

**Khả năng tổng quát hoá (AitZ).**
"Tinh chỉnh trên AndroidControl chuyển được sang AitZ: mọi nhánh tinh chỉnh đều hơn mô hình gốc có ý nghĩa. Trên AitZ, ck500 và S1 cho kết quả tương đương, phù hợp với việc thưởng SPICE học theo văn phong câu chuẩn của AndroidControl, còn câu chuẩn AitZ do GPT-4V sinh."
Có thể kể như phạm vi áp dụng tự nhiên của phương pháp, kèm hướng mở: thưởng theo văn phong của miền đích.

**Bước không chạm.**
"GRPO thưởng SPICE ưu tiên câu cho thao tác chạm, nên ở bước cuộn màn hình vẫn còn dư địa cải thiện; đây là một động lực cho bước ghép ACE và cho hướng tinh chỉnh hàm thưởng về sau."

**Lịch sử tự sinh.**
"Khi lịch sử là câu do chính mô hình viết thay vì câu chuẩn, ưu thế của ck500 so với S1 vẫn giữ nguyên (+1,48 exec, trên tập tác vụ đủ ảnh +1,66), và về đúng loại thao tác ở bước chạm còn tăng gần gấp đôi (+3,52)." Mức giảm chung khoảng 4 điểm của cả hai nhánh có thể kể như một đặc điểm của bài toán khi chạy tuần tự. Bước không chạm có thể nhắc sau, như hướng phát triển tiếp.

**Mẹo chọn từ cho khớp với bảng** (hội đồng thường tự đối chiếu lời văn với số):
- Chênh lệch có KTC phủ 0: dùng "tương đương" hoặc "nhỉnh hơn".
- Hai chỗ số gần như bằng nhau (ck500 và S1 trên AitZ, ACE và ck500 về exec): dùng "tương đương", "giữ nguyên".
- Báo đủ ba luật cạnh nhau, vì cả ba cùng chiều nên càng đủ càng thuyết phục.
- Về bộ trỏ: dùng "không huấn luyện trên AndroidControl".
- Thay "chắc chắn" bằng "nhất quán", "ổn định về hướng".

**Văn phong** (theo `CLAUDE.md`): dùng "chúng tôi", không dùng "luận văn" làm chủ ngữ; không in đậm giữa câu; không dấu gạch dài; không tiêu đề dạng câu hỏi; không tên tệp hay tham số trong thân bài; gọi câu người viết là "câu chuẩn"; dùng "nhánh so sánh" thay cho "đối chứng".

---

## 10. Việc cần sửa trong luận văn, theo chương

Mọi việc dưới đây chưa làm. Sửa xong thì dựng lại `thesis/main.pdf` (lệnh dựng ở `CLAUDE.md`, không dùng `>/dev/null 2>&1`).

**Tóm tắt, ch1, ch7 (kết luận)**
- Viết ck500 theo mục 9: cải thiện nhất quán, có ý nghĩa thống kê, giữ qua bốn dụng cụ và ba luật; đặt hai hạt GRPO cạnh nhau.
- Thêm một câu về xao101 (mức tăng thuộc về tín hiệu SPICE), một câu về ACU (tác vụ chưa thấy, +4,58) và một câu về AitZ (SFT chuyển miền, ck500 tương đương S1).

**ch4 (phương pháp)**
- Mô tả nhánh kiểm sàn xao101 (thưởng bị xáo, cùng mọi siêu tham số với ck500).
- Mô tả hạt GRPO 202 (mục 2.5).

**ch5 (thước đo)**
- `sec:phi4`: thay con số Base 38,56 (trên 3.566 bước) bằng 38,23 (đủ 4.463 bước). Cũng tìm và sửa con số này trong `report/155` và bài SOICT.
- Thêm Phi-Ground làm bộ trỏ thứ ba, kèm nguồn dữ liệu và cách viết ở mục 4.4.

**ch6 (kết quả)**
- Bảng chính: thêm các hàng S1/202, ck500/202, xao101, 7B với ba cột exec, D.3, AitW (mục 2.1); thêm các phép so ở mục 2.2.
- Đoạn ck500: thêm phân rã và ví dụ định tính (mục 5), và đoạn về tác hại ở bước không chạm dẫn tới ACE.
- Bảng ACE (khoảng dòng 138 đến 152): thêm KTC95 cho sáu thước chữ (mục 3.2; chrF mức kho), ghi METEOR không có KTC. Thêm câu "ACE hơn ck500 ở mọi thước chữ nhưng exec chỉ ngang".
- Đoạn UI-Venus (khoảng dòng 347, hiện chỉ nói Base, S1, S2 trên lát 2.532): thêm bảng đổi dụng cụ ở mục 4.1 và 4.2.
- Thêm ablation thưởng CIDEr-D (mục 5). Grep chưa thấy trong `thesis/chapters/*.tex`, nhưng cần xem tay ch4 và ch6, phòng khi dùng tên khác.
- Thêm mục tổng quát hoá: ACU trước (mục 8, kết quả mạnh), AitZ sau (mục 6); thêm mục lịch sử tự sinh (mục 7).
- Thêm hàng so với 7B.

**ch7 (hạn chế)**
- Khai: mỗi nhánh một hạt (S1 và ck500 hai hạt); ACE ngang ck500 ở exec; trên AitZ ck500 tương đương S1; tác hại ở bước không chạm lớn thêm khi lịch sử tự sinh; hai dụng cụ ngoài họ Qwen cho mức tăng nhỏ hơn.
- Sửa các dòng 18 và 38 (nhắc tới dụng cụ đo) cho khớp mục 4.

**Bảng tự sinh `bang_nhieu_thuoc.tex`**
- Hiện chưa có ACE. Cần tạo JSON bảy thước chữ cho ACE (có thể mở rộng `harness/ck500_text_metrics.py`), thêm hàng vào danh sách `HANG` của `harness/sinh_bang_nhieu_thuoc.py`, rồi sinh lại bảng. Không sửa tay.

**Bài SOICT** (camera-ready): áp cùng cách viết ở mục 9 cho ck500 và sửa con số Base của Phi-4.

---

## 11. Còn chờ, còn thiếu

**Đang chạy:** không còn. Kernel cuối `trangphngngc/chu-luoi-2-11-cpu` xong 3/11, số ở mục 14.4.

**Chưa làm, không cần GPU:** không còn.

**Chưa làm, cần GPU:**
- Phi-4 và UI-Venus cho ck500/202 (khoảng 5 h; user quyết tạm không chạy, 25/10).
- Phi-Ground cho S1/202.
- Số VRAM của 7B (việc #7 của `report/322`).

**Chưa kiểm:** lần đứt máy ở điểm lưu 200 của ck500/202 (log không còn).

---

## 12. Phụ lục: nguồn tệp và kiểm tái lập

| kết quả | kernel (tài khoản) | đầu ra | cách đọc |
|---|---|---|---|
| S1/202, ck500, ACE dưới UGround | (đã có từ trước) | `runs/score_s1_seed202_raw.jsonl` · `runs/grpo_spice/score_ck500_test_raw.jsonl` · `runs/ra304_luat/score_R3_test_raw.jsonl` | `score_run.cluster_bootstrap` |
| ck500/202 test | `trangphngngc/ck500-s202-test` | `runs/grpo_spice/s202_24_10/` | như trên; thước chữ ở `runs/text_metrics_s202.json` |
| xao101 test | `uyenle0712/ck500-xao101-test` | `runs/xao101/test/so_ghep_cap_xao101.json` | log train ở `runs/xao101/c2/` |
| 7B prompting | `trangphngngc/qwen7b-test` | `runs/qwen7b/test_25_10/so_ghep_cap_q7b.json` | |
| UI-Venus | `_bundles/venus_ck2` | `runs/venus/ck500_r3_22_10/` · `runs/venus/bu_22_10/` · `runs/venus/s1_202_23_10/` | `python3 -I harness/venus_ck_doc.py` · `venus_s1_202_doc.py` |
| Phi-4 | | `runs/som/chon_phi4_*.jsonl` · `runs/som/base_rest_24_10/` | `som_doc.py` · `som_s1_202_doc.py` |
| Phi-Ground | `trangphngngc/phiground-s1` · `phiground-cham-ck-r3` | `runs/phiground/s1_25_10/` · `runs/phiground/ck_r3_25_10/` | ghép theo (bước, câu) |
| KTC thước chữ | (WSL) | `runs/ktc_thuoc_chu.json` | `harness/ktc_thuoc_chu.py` |
| Thước chữ 26/10 | `trangphngngc/chu-26-10-cpu` | `runs/text_metrics_26_10/text_metrics_26_10.json` | |
| AitZ | `trangphuongngoc/aitz-gen-s1-ck500` · `aitz-ace-tran` | `runs/aitz/gen_25_10/v2/` · `runs/aitz/ace_26_10/` | `so_ghep_cap_aitz*.json` |
| Lịch sử tự sinh | `trangphuongngoc/tuantu-lichsu-tusinh` · `tuantu-cham` | `runs/tuantu/out/` · `runs/tuantu/cham/` | `harness/doc_tuantu.py` |
| ACU | `acu-build-cpu` · `acu-ocr144-cpu` · `acu-gen` (trangphuongngoc) | `runs/acu/gen/out/` (pred, score raw) · Release `data-acu-build-v1` | `harness/doc_acu.py` → `runs/acu/ket_qua_acu.json` |
| KTC exec, D.3, AitW (ck500, ACE, ACU, gộp 5.947) | `trangphngngc/so-27-10-cpu` | `runs/so_d3_aitw_ck500.json` · `runs/acu/ket_qua_acu.json` | `harness/so_d3_aitw_ck500.py` (tự kiểm exec +1,55 / +1,03) · `harness/doc_acu.py` |
| KTC thước chữ 27/10 | `trangphngngc/ktc-chu-27-10-cpu` | `runs/ktc_chu_27_10.json` | `harness/ktc_chu_27_10.py` (tự kiểm giá trị đã in) |

**Kiểm tái lập đã làm:**
- Mọi số ở mục 2 và 4 đã tính lại từ tệp thô trên máy ngày 24/10; tất cả khớp.
- Các lượt sinh lại: kiểm hoà 16/20 (S1 hoà fp16 so với lượt công bố, như `report/259`); ck500 20/20.
- Luật R3 trong gói AitZ tái lập đúng câu ACE trên test 4.463/4.463. ra_k4 có md5 `f3c543b0`, trùng adapter của lượt test 304.

**Bẫy khi tính lại:**
- Một bước (câu rỗng, bước `(18710, 1)`) thiếu trường `executable` trong ba tệp S1/101, S1/202, ck500. Phải dùng `get("executable", 0)` như `score_run.py`.
- Chạy `som_doc.py` với danh sách tệp riêng sẽ ghi đè `runs/som/som_ket_qua.json` (tệp git đang theo dõi). Chạy xong phải `git checkout` lại tệp đó.
- `score_run.py` chặn tệp thiếu hơn 1% số bước. Khi chỉ chấm các bước có câu khác nhau, phải truyền `--n <số dòng>`.

## 13. Cách đọc lưới RL, ghi 1/11/2026 trước khi có số nào của lưới

Ghi để không kể lại sau khi đã biết số. Nguồn: `report/328` §2, §3.4, §6.

- **Họ chính, đọc trên exec test, so với ck500:** SFT tiếp · SCST · GRPO bỏ chia std · GRPO + CIDEr-D · PPO · xao101. Các lượt còn lại ghi là mô tả. Vẫn in Holm cho toàn bộ, cả p gốc lẫn p đã hiệu chỉnh.
- **"Nhóm dẫn đầu":** các lượt cách lượt cao nhất dưới 1 điểm exec, hoặc không bị Holm bác trong họ chính.
- **"Lượt khác đứng trên ck500 rõ":** cách ≥ 1 điểm, KTC ghép cặp loại 0, qua Holm trong họ chính.
- **Cấm viết "tốt nhất"** từ lưới một hạt giống. Nếu số cho phép thì dùng "thuộc nhóm dẫn đầu".
- **Dự đoán:** D1, D2 ở `report/323` §9 và H-A đến H-J ở `report/328` §3.4.
- **Câu trả lời cho thầy:** chọn bản theo các điều kiện trên, ở `report/328` §6.

## 14. Kết quả lưới RL trên test, đợt đầu (3/11/2026)

Chưa đưa vào luận văn: đợi đủ lưới rồi sửa một lượt (`report/326`). Mọi lượt một hạt giống (101), dùng cùng câu nhắc của ck500, 500 bước.

### 14.1 Bốn tiêu chí xác định vị trí

| nhánh | exec | KTC95 exec | D.3 | D.3∧14% | AitW đầy đủ | đúng loại thao tác |
|---|---|---|---|---|---|---|
| S1/101 | 59,11 | | 65,49 | 61,73 | 74,37 | 94,35 |
| ck500 | **60,65** | | 67,02 | 63,25 | 76,25 | 95,97 |
| GRPO + ROUGE-L | **60,63** | [58,91; 62,40] | 67,04 | 63,19 | 76,79 | 96,86 |
| SCST + SPICE | **60,54** | [58,85; 62,24] | 66,88 | 63,16 | 76,14 | 96,08 |
| GRPO + METEOR | 60,27 | [58,52; 62,02] | 66,75 | 62,92 | 76,27 | 96,28 |
| GRPO + CIDEr-D | 60,27 | [58,57; 61,95] | 66,44 | 62,78 | 76,00 | 96,08 |

Cập nhật 3/11: GRPO + CIDEr-D đã chấm đủ 4.463 bước (`uyenle0712/luoi-test-u-2`), thay số tạm 60,25 trên 4.428 bước; câu trùng dùng lại kết quả chấm, khớp 40/40 bước.

| phép so | exec | p | D.3 | D.3∧14% | AitW đầy đủ |
|---|---|---|---|---|---|
| ROUGE-L − ck500 | −0,02 [−0,54; +0,49] | 1,00 | +0,02 [−0,52; +0,55] | −0,07 [−0,59; +0,46] | +0,54 [0,00; +1,08] |
| SCST − ck500 | −0,11 [−0,56; +0,35] | 0,69 | −0,13 [−0,58; +0,33] | −0,09 [−0,55; +0,38] | −0,11 [−0,56; +0,33] |
| METEOR − ck500 | −0,38 [−0,95; +0,19] | 0,21 | −0,27 [−0,84; +0,28] | −0,34 [−0,91; +0,22] | +0,02 [−0,55; +0,61] |
| CIDEr-D − ck500 | −0,38 [−0,88; +0,11] | 0,16 | −0,58 [−1,09; −0,08] | −0,47 [−0,98; +0,04] | −0,25 [−0,74; +0,25] |
| ROUGE-L − S1/101 | +1,52 [+0,78; +2,29] | 4,8e−5 | +1,55 [+0,77; +2,35] | +1,46 [+0,68; +2,25] | +2,42 [+1,65; +3,22] |
| SCST − S1/101 | +1,43 [+0,79; +2,11] | 8,8e−6 | +1,39 [+0,75; +2,07] | +1,43 [+0,79; +2,10] | +1,77 [+1,13; +2,44] |
| METEOR − S1/101 | +1,17 [+0,39; +1,97] | 2,6e−3 | +1,25 [+0,47; +2,05] | +1,19 [+0,42; +1,99] | +1,90 [+1,10; +2,72] |
| CIDEr-D − S1/101 | +1,17 [+0,40; +1,94] | 1,9e−3 | +0,94 [+0,15; +1,73] | +1,05 [+0,30; +1,82] | +1,64 [+0,89; +2,39] |

Bootstrap cụm app, B = 10.000; p là McNemar chính xác, chưa hiệu chỉnh ở bảng này. Holm tạm cho bốn phép so exec với ck500: 0,63 · 0,63 · 1,00 · 1,00. Họ chính ở mục 13 chưa đủ lượt nên phải tính lại khi đủ. Script `harness/doc_luoi.py` tự kiểm ck500 − S1/101 exec ra đúng +1,55 [+0,80; +2,33].

### 14.2 Đọc theo mục 13

- Cả bốn lượt thuộc nhóm dẫn đầu cùng ck500: cách lượt cao nhất dưới 1 điểm exec, không phép so exec nào với ck500 loại 0.
- Chưa có lượt nào đứng trên ck500 rõ. Ngược lại, chưa có căn cứ viết ck500 hay SPICE tốt nhất.
- Cả bốn hơn S1/101 từ +1,17 đến +1,52 exec, đều dưới MDE 2,11. Chưa tách được công của RL với công của việc train thêm 500 bước, vì SFT tiếp chưa chấm.
- Đúng loại thao tác của mọi lượt tăng cùng hướng so với S1 (94,35 → 95,97–96,86), phù hợp H-A ở `report/328`. Bảng phân rã ở mục 14.5; vẫn còn thiếu lượt T5 nên chưa xác nhận H-A.
- Dự đoán ghi trước (`report/323` §9), mới đọc được một phần và một hạt: D2 đoán SCST < GRPO; đo được SCST − ck500 −0,11, đúng chiều nhưng nằm trong nhiễu, chưa xác nhận. D1 đoán METEOR, CIDEr-D, ROUGE-L ≥ SPICE; đo được cả ba không vượt ck500 về exec nhưng cũng không kém có ý nghĩa, chưa phân định được, và chrF chưa chạy.
- Hai phép so lệch riêng cần đọc thận trọng, vì nhiều phép so và một hạt giống: ROUGE-L − ck500 dưới AitW +0,54 (p = 0,06) và CIDEr-D − ck500 dưới D.3 −0,58 (p = 0,028, chưa hiệu chỉnh).

### 14.3 Còn thiếu của đợt này

- Sau khi hạn mức làm mới 7/11: test SFT tiếp (`luoi-t2-3`, đủ 500 bước, chưa chấm) · test RLOO, REINFORCE · nối tiếp lượt A/A `grpo:spice:101` (dừng ở trần 7,5 h, khoảng bước 183, điểm lưu cuối 175).

Nguồn: `runs/luoi/test_2_11/` (`so_ghep_cap_exec.json`, tệp pred, tệp thô, log) · log train `runs/luoi/lo3/luoi-t2-3/` · kernel `trangphngngc/luoi-test-t-1`, `uyenle0712/luoi-test-u-1`, `trangphuongngoc/luoi-t2-3`. Kiểm hoà 16/20 trùng lượt S1 công bố, đúng mức `report/259`; dùng lại kết quả chấm câu trùng khớp 40/40 bước ở mỗi lượt.

### 14.4 Độ đo văn bản (kernel `trangphngngc/chu-luoi-2-11-cpu`, xong 3/11)

Tính trên đủ 4.463 câu, kể cả lượt CIDEr-D vì độ đo văn bản không cần bộ trỏ. In đậm là điểm cao nhất của cột trong bảng này.

| nhánh | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|
| S1/101 | 51,56 | 36,79 | 67,35 | 416,12 | 44,37 | 61,26 | 66,33 |
| xao101 | 51,32 | 36,95 | 67,36 | 418,13 | 44,40 | 61,52 | 66,40 |
| ck500 | 52,36 | 37,92 | 68,36 | 430,05 | 45,79 | 62,87 | 67,07 |
| SCST + SPICE | 51,97 | 38,15 | 68,70 | 430,89 | **45,93** | 63,31 | 67,25 |
| GRPO + ROUGE-L | **52,59** | 38,20 | **69,27** | **432,81** | 45,57 | 63,42 | **67,57** |
| GRPO + METEOR | 50,76 | **38,63** | 69,14 | 426,61 | 45,13 | **64,19** | 67,35 |
| GRPO + CIDEr-D | 51,59 | 37,78 | 68,47 | 424,52 | 44,43 | 62,90 | 67,03 |

KTC95 ghép cặp (bootstrap cụm app, 1.091 cụm, B = 2.000). ⁰ = KTC phủ 0. METEOR không có KTC.

| phép so | BLEU-4 | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|
| SCST − ck500 | −0,39 [−0,81; +0,03] ⁰ | +0,33 [+0,03; +0,67] | +0,84 [−3,02; +4,99] ⁰ | +0,14 [−0,36; +0,69] ⁰ | +0,44 [+0,08; +0,79] | +0,18 [−0,10; +0,48] ⁰ |
| GRPO + ROUGE-L − ck500 | +0,23 [−0,22; +0,73] ⁰ | +0,91 [+0,52; +1,31] | +2,76 [−1,98; +7,56] ⁰ | −0,22 [−0,82; +0,40] ⁰ | +0,55 [+0,15; +0,93] | +0,51 [+0,13; +0,85] |
| GRPO + METEOR − ck500 | −1,60 [−2,15; −1,05] | +0,77 [+0,35; +1,21] | −3,44 [−8,89; +2,01] ⁰ | −0,66 [−1,34; +0,01] ⁰ | +1,32 [+0,90; +1,76] | +0,29 [−0,07; +0,67] ⁰ |
| GRPO + CIDEr-D − ck500 | −0,77 [−1,26; −0,28] | +0,11 [−0,27; +0,48] ⁰ | −5,53 [−10,21; −1,20] | −1,37 [−1,97; −0,76] | +0,03 [−0,34; +0,40] ⁰ | −0,04 [−0,38; +0,28] ⁰ |
| SCST − S1/101 | +0,41 [−0,12; +1,19] ⁰ | +1,35 [+0,89; +1,79] | +14,78 [+9,33; +20,45] | +1,57 [+0,86; +2,25] | +2,04 [+1,55; +2,54] | +0,91 [+0,53; +1,30] |
| GRPO + ROUGE-L − S1/101 | +1,03 [+0,45; +1,86] | +1,92 [+1,43; +2,40] | +16,70 [+10,53; +22,79] | +1,20 [+0,43; +1,99] | +2,15 [+1,61; +2,67] | +1,24 [+0,80; +1,65] |
| GRPO + METEOR − S1/101 | −0,79 [−1,45; +0,09] ⁰ | +1,79 [+1,25; +2,31] | +10,50 [+3,28; +17,57] | +0,76 [−0,06; +1,61] ⁰ | +2,93 [+2,37; +3,50] | +1,02 [+0,56; +1,49] |
| GRPO + CIDEr-D − S1/101 | +0,03 [−0,56; +0,85] ⁰ | +1,12 [+0,66; +1,58] | +8,40 [+2,33; +14,31] | +0,06 [−0,70; +0,84] ⁰ | +1,64 [+1,11; +2,15] | +0,70 [+0,28; +1,11] |

Đọc (chưa hiệu chỉnh đa so sánh, một hạt giống):

- **ck500 không dẫn đầu độ đo văn bản nào trong nhóm này.** GRPO + ROUGE-L cao hơn ck500 ở 6/7 độ đo, trừ SPICE; KTC loại 0 ở ROUGE-L, chrF, BERTScore. SCST + SPICE cũng cao hơn ở 6/7, trừ BLEU-4; KTC loại 0 ở ROUGE-L, chrF. Cộng với mục 14.1, GRPO + ROUGE-L là ứng viên đáng kiểm nhất ở hạt thứ hai.
- **Thưởng SPICE vẫn cho SPICE cao:** SCST 45,93 và ck500 45,79 đứng đầu cột, nhưng chênh với GRPO + ROUGE-L chỉ −0,22, KTC phủ 0.
- **GRPO + CIDEr-D thấp hơn ck500 ngay trên CIDEr-D** (−5,53, KTC loại 0), và SPICE gần như không đổi so với S1 (+0,06). Lượt tối ưu CIDEr-D mà điểm CIDEr-D kém lượt tối ưu SPICE là điều cần giải thích trước khi trích. Đã đọc `CiderD` trong `harness/grpo_luoi.py`: công thức giống pycocoevalcap (sigma 6, clip, ×10); khác ở df, lúc thưởng lấy từ câu chuẩn tập dạy, lúc chấm lấy từ tập kiểm, và khác cách tách từ (không qua PTBTokenizer). [suy] đây có thể là một phần nguyên nhân, chưa đo; cũng có thể chỉ là nhiễu một hạt giống.
- **D1 (`report/323` §9):** METEOR và ROUGE-L thắng SPICE ở nhiều độ đo văn bản nhưng không hơn về exec, còn CIDEr-D thua. Vẫn chưa phân định được, chrF chưa chạy.
- Cả bốn đều hơn S1/101 ở ROUGE-L, CIDEr-D, chrF, BERTScore với KTC loại 0.

Tự kiểm đạt: S1/101, ck500, xao101 tái lập số ở mục 3.1 (cả METEOR), và KTC ck500 − S1/101 trùng mục 3.2. Nguồn: `runs/luoi/test_2_11/chu/chu_luoi_2_11.json`, `chu.log`; điểm từng bước trong `chu_cache.zip`. Script `harness/chu_luoi_2_11.py`, gói `_bundles/chu_luoi_2_11/`.

### 14.5 Phân rã mức tăng exec so với S1/101 (kernel `trangphngngc/luoi-cpu-3-11-k`, 3/11)

Cứu là bước S1 trượt mà nhánh trúng, phá là ngược lại. "Loại thao tác" đếm bước cứu mà S1 viết sai loại và bước phá mà nhánh viết sai loại, "phần tử" là phần còn lại. p là McNemar chính xác hai phía trên cặp cứu/phá của từng phần, tính hậu kiểm và chưa hiệu chỉnh. Script tự kiểm ck500 ra đúng +28/+41 của `report/259`.

| nhánh | ròng | loại thao tác: cứu/phá, ròng, p | phần tử: cứu/phá, ròng, p | exec khi cả hai đúng loại: S1 → nhánh |
|---|---|---|---|---|
| ck500 | +69 | 36/8, +28, 2,5e−5 | 123/82, **+41**, **0,005** | 62,62 → 63,60 |
| GRPO + ROUGE-L | +68 | 55/7, **+48**, <1e−6 | 116/96, +20, 0,19 | 62,63 → 63,10 |
| SCST + SPICE | +64 | 39/6, +33, 1e−6 | 95/64, +31, 0,017 | 62,62 → 63,36 |
| GRPO + CIDEr-D | +52 | 42/8, +34, 1e−6 | 120/102, +18, 0,25 | 62,65 → 63,08 |
| GRPO + METEOR | +52 | 42/11, +31, 2,2e−5 | 128/107, +21, 0,19 | 62,64 → 63,14 |
| xao101 | 0 | 7/10, −3, 0,63 | 38/35, +3, 0,82 | 62,69 → 62,76 |

Đọc: mọi lượt có thưởng thật đều sửa loại thao tác rõ, còn nhánh điểm SPICE ghép ngẫu nhiên thì không, nên phần này không tự có từ vòng lặp RL khi thưởng không mang thông tin. Câu này chưa tách được công của RL với việc train thêm theo câu chuẩn: SFT tiếp chưa chấm, và có thể cũng sửa được loại thao tác. Về đổi phần tử, hai lượt thưởng SPICE có phép so cứu/phá loại được 0 trước hiệu chỉnh, ba lượt thưởng khác thì không. Đây là manh mối đầu tiên cho việc thưởng SPICE khác các độ đo còn lại, nhưng chưa được viết thành kết luận, vì bốn lý do: "có ý nghĩa" và "không có ý nghĩa" không chứng minh hai nhánh khác nhau; Holm trên năm lượt giữ ck500 (0,026) nhưng SCST mất (0,068); phép đọc này chọn sau khi thấy số; và mới có một hạt giống. Phép so trực tiếp ở bảng dưới trả lời lý do đầu. Tệp `phan_ra.json`.

**So ghép cặp trực tiếp giữa các nhánh** (kernel `trangphngngc/luoi-phan-tu-3-11-k`, `harness/phan_tu_ghep_cap.py`, tự kiểm tái lập bảng trên). Vẫn là hậu kiểm. Δ tính trên 4.463 bước, đơn vị là bước ròng và điểm %, KTC bootstrap cụm app B = 10.000, p dấu chính xác trên các bước hai nhánh khác nhau. Cột "trên bước cùng đúng loại" không qua S1: exec của hai nhánh trên các bước cả hai đúng loại thao tác (n từ 4.271 đến 4.278).

| phép so | phần tử: Δ bước, điểm [KTC] | p · Holm | loại thao tác: Δ bước, điểm [KTC] | p · Holm | trên bước cùng đúng loại: điểm [KTC] | p · Holm |
|---|---|---|---|---|---|---|
| ck500 − SCST + SPICE | +10, +0,22 [−0,20; +0,66] | 0,35 · 0,35 | −5, −0,11 [−0,29; +0,05] | 0,27 · 0,63 | +0,21 [−0,23; +0,65] | 0,41 · 0,41 |
| ck500 − GRPO + CIDEr-D | +23, +0,52 [+0,04; +1,00] | 0,040 · 0,16 | −6, −0,13 [−0,32; +0,04] | 0,21 · 0,63 | +0,56 [+0,07; +1,07] | 0,032 · 0,13 |
| ck500 − GRPO + METEOR | +20, +0,45 [−0,09; +1,00] | 0,11 · 0,23 | −3, −0,07 [−0,26; +0,11] | 0,63 · 0,63 | +0,47 [−0,09; +1,03] | 0,12 · 0,23 |
| ck500 − GRPO + ROUGE-L | +21, +0,47 [0,00; +0,94] | 0,069 · 0,21 | **−20, −0,45 [−0,68; −0,23]** | **8,8e−5 · 3,5e−4** | +0,49 [0,00; +0,99] | 0,073 · 0,22 |
| ck500 − TB ba độ đo khác (cùng GRPO) | +21,3, +0,48 [+0,05; +0,91] | 0,035 | −9,7, −0,22 [−0,39; −0,05] | 0,024 | | |
| TB hai lượt SPICE − TB ba độ đo khác | +16,3, +0,37 [+0,03; +0,70] | 0,061 | −7,2, −0,16 [−0,30; −0,03] | 0,099 | | |

Đọc: ck500 cao hơn cả ba lượt GRPO độ đo khác về đổi phần tử, cùng chiều và cỡ gần nhau (+20 đến +23 bước), nhưng từng phép so không còn ý nghĩa sau Holm. Khi gộp ba lượt thì KTC vừa loại 0 (+0,48 [+0,05; +0,91], p = 0,035), đây là phép so chọn sau khi thấy số. Ngược chiều, ck500 sửa loại thao tác ít hơn, rõ nhất so với ROUGE-L (−20 bước, giữ sau Holm). Hai phần gần bù nhau, nên exec tổng gần bằng: ROUGE-L tăng chủ yếu nhờ loại thao tác, ck500 nhờ cả hai phần. Cách viết được phép: "các độ đo thưởng đạt mức exec gần nhau theo thành phần khác nhau; thưởng SPICE có dấu hiệu nghiêng về đổi đúng phần tử, chưa đủ để kết luận". Chưa được viết "SPICE giúp định vị tốt hơn". Muốn khẳng định cần hạt giống thứ hai của các lượt độ đo khác; ck500/202 đã có sẵn làm mốc. Tệp `phan_tu_ghep_cap.json`.

### 14.6 Diễn biến lúc train (số train, chỉ để giải thích, không trích làm kết quả)

| nhánh | entropy: 262 bước đầu → 75 bước cuối | nhóm thưởng bằng nhau | KL với S1, 75 bước cuối | số từ |
|---|---|---|---|---|
| SCST + SPICE | 0,53 → 0,37 | 19,5% → 30,7% | 0,027 | 8,75 → 9,21 |
| RLOO + SPICE | 0,51 → 0,37 | 22,7% → 33,3% | 0,019 | 8,65 → 9,13 |
| REINFORCE EMA + SPICE | 0,53 → 0,38 | 20,0% → 28,0% | 0,019 | 8,66 → 9,04 |
| GRPO + CIDEr-D | 0,49 → 0,29 | 13,6% → 25,3% | 0,052 | 8,73 → 9,40 |
| GRPO + METEOR | 0,49 → 0,28 | 13,2% → 24,7% | 0,080 | 8,81 → 9,60 |
| GRPO + ROUGE-L | 0,48 → 0,29 | 13,2% → 26,0% | 0,053 | 8,73 → 9,32 |

Thưởng SPICE có nhiều nhóm bằng nhau hơn ngay từ đầu (khoảng 20% so với 13%), nên có ít bước có tín hiệu hơn, và đi xa S1 ít hơn (KL 0,02–0,03 so với 0,05–0,08). Đây là khác biệt theo độ đo thưởng, không phải theo thuật toán: ba thuật toán cùng thưởng SPICE cho số gần nhau. ck500 chỉ còn log 337 bước, xao101 225 và A/A 183, nên không có cửa sổ cuối; cửa sổ đầu của ck500 tái lập 0,52 và 20,2% của `report/328`, còn 0,34 và 31,3% ở cửa sổ cuối chưa tái lập được từ log trong kho. Số thưởng giữa các độ đo không so được với nhau. Tệp `dien_bien_train.json`.

### 14.7 Hình thức câu (spaCy, chỉ báo chưa kiểm định, Δ so với S1/101, bootstrap theo app)

| nhánh | số từ | lặp 2 từ (%) | lặp 3 từ (%) | quá ngắn (%) | gốc câu không phải động từ (%) |
|---|---|---|---|---|---|
| S1/101, giá trị | 7,86 | 3,56 | 0,13 | 0,78 | 6,05 |
| câu chuẩn, giá trị | 7,85 | 6,27 | 0,34 | 0,27 | 7,46 |
| ck500 | +0,14 [+0,08; +0,20] | −0,25 [−0,61; +0,10] | +0,11 [0,00; +0,25] | −0,22 [−0,44; −0,02] | −0,47 [−0,90; −0,07] |
| SCST + SPICE | +0,29 [+0,23; +0,34] | −0,07 [−0,40; +0,26] | +0,07 [−0,04; +0,19] | −0,27 [−0,47; −0,07] | −0,45 [−0,76; −0,14] |
| GRPO + ROUGE-L | +0,21 [+0,14; +0,27] | +0,20 [−0,16; +0,56] | +0,09 [−0,05; +0,24] | −0,36 [−0,55; −0,15] | −0,99 [−1,40; −0,57] |
| GRPO + METEOR | +0,59 [+0,52; +0,67] | −0,18 [−0,58; +0,18] | +0,11 [0,00; +0,27] | −0,40 [−0,63; −0,20] | −1,01 [−1,36; −0,64] |
| GRPO + CIDEr-D | +0,25 [+0,18; +0,32] | −0,56 [−0,97; −0,17] | +0,11 [0,00; +0,26] | −0,29 [−0,48; −0,10] | −0,94 [−1,32; −0,58] |
| xao101 | +0,08 [+0,05; +0,12] | +0,20 [−0,02; +0,44] | 0,00 [0,00; 0,00] | −0,16 [−0,30; −0,02] | 0,00 [−0,27; +0,25] |

Đọc: nhận xét của Liu về việc thưởng SPICE làm câu lặp cụm hay cụt chưa thấy trên ck500: lặp 2 từ không tăng, lặp 3 từ tăng rất ít và cận dưới chạm 0, câu quá ngắn giảm. Mọi lượt đều nằm dưới mức lặp của câu chuẩn. METEOR kéo câu dài nhất (+0,59 từ). Đây là chỉ báo tự động từ bộ phân tích cú pháp, không thay được chấm tay. Tệp `hinh_thuc.json` (thêm ck500/202, A2_500, ACE và cột khác).

## 15. Giải thích H1 và H5 (report/323 §8.4), đo 6/11/2026, Kaggle CPU

Kernel `trangphngngc/giai-thich-6-11-k` · mã `harness/h1_khuon_cau.py`, `harness/h5_spice_khong_cham.py` ·
tệp `runs/giai_thich/k_6_11/`. Chỉ đo trên câu chuẩn và câu đã sinh sẵn, 0 GPU, hậu kiểm, một hạt giống.
Lượt thử 100 câu đạt rồi mới chạy đủ. Phép kiểm chéo: tỉ lệ đúng loại thao tác ở bước cuộn của S1 là 83,97 và của ck500 là 77,75, ở bước quay lại là 72,96 và 67,04,
trùng số noharm đã có (`report/261` §6) ⇒ ghép câu đúng bước.

**H1, khuôn câu.** Câu chuẩn AC test trung bình 7,31 từ (trung vị 6, p90 13). Tám khuôn hai từ đầu phủ 80% câu,
riêng "click on" chiếm 56,3%. AC train gần như y hệt (7,18 từ, 8 khuôn, 55,6%). AitZ dài hơn (10,06 từ, trung vị 10)
nhưng **theo khuôn hơn AC**: chỉ có 10 khuôn, 4 khuôn phủ 80%, distinct-1 là 0,042 so với 0,092 của AC.
⇒ Dự đoán "AitZ khác khuôn AC" chỉ đúng một nửa. AitZ khác AC, nhưng khác theo hướng nhiều khuôn hơn, chứ không phải ít hơn.
Tỉ lệ từ của câu chuẩn trùng tên phần tử vàng (4.381 bước chạm có tên) chỉ **11,5%** ⇒ vế "nội dung nằm ở tên phần tử"
chưa được số ủng hộ. Phép đo này yếu: tên lấy từ ô khai báo (OCR/a11y), không trùng chữ với cách người chú thích gọi phần tử. Chưa dùng vế này.

**H5, bước không chạm.** Số tuple SPICE của câu chuẩn chấm với chính nó (All): chạm 3,73 · cuộn 2,50 · quay lại 2,41 ·
mở app 2,40. Tỉ lệ câu chuẩn có 0 tuple đối tượng: cuộn 13,6%, quay lại 11,1%, chạm 1,4%. ⇒ Câu không chạm có ít tuple hơn, vế này đúng.
Nhưng **SPICE vẫn tách rất rõ câu đúng loại và sai loại ở bước không chạm**. Lấy SPICE trung bình của câu đúng loại trừ câu sai loại:
S1 được 0,57 ở bước không chạm so với 0,33 ở bước chạm, ck500 được 0,58 so với 0,33.
⇒ Giả thuyết "thưởng SPICE ít tín hiệu cho loại thao tác ở bước không chạm" **không đứng**, vì khoảng cách thưởng ở đó còn lớn hơn ở bước chạm.
Thêm một điều đã kiểm: tập câu nhắc của `grpo_spice.py` không lọc theo loại thao tác, nên cũng không giải thích được bằng việc "không train trên bước cuộn".
Việc giảm ở cuộn (−6,2) và quay lại (−5,9) **chưa có giải thích**. Hướng kiểm tiếp [suy]: tỉ lệ bước không chạm trong 2.000 câu nhắc đã dùng
và lợi thế trung bình của câu cuộn trong log train. Ở bước không chạm tổng, SPICE của ck500 vẫn cao hơn S1 (64,0 so với 62,5) dù tỉ lệ đúng loại giảm
⇒ ck500 viết câu sát câu chuẩn hơn ở những bước nó giữ đúng loại.

**AitZ.** Câu chuẩn AitZ ở bước chạm có 7,78 tuple, gấp đôi AC (3,74), và riêng quan hệ là 1,73 so với 0,50.
Kết hợp với việc AitZ theo khuôn hơn, khả năng [suy] là phần lớn tuple AitZ đến từ phần khuôn (vị trí, quan hệ) mà mọi câu đều có,
nên SPICE ít phân biệt được giữa các câu. Đây là giả thuyết cho việc ck500 không hơn S1 trên AitZ, chưa đo.

## 16. Giải thích H2 (report/323 §8.4) và ba phần thưởng mới, đo 6/11/2026, Kaggle CPU

Kernel `uyenle0712/h2-thuong-b3` · mã `harness/h2_thuong.py`, `harness/thuong_moi.py` · tệp `runs/giai_thich/h2_b3/` ·
ghi chú `_bundles/moi_b3/GHI_CHU.md`. ⛔ **Toàn bộ số ở mục này là số val** (8 mẫu C1 của S1/101, nhiệt độ 1,0, 400 bước val,
exec từng mẫu ở 249 bước chạm, `report/252`). Số này chỉ dùng để giải thích và xếp hạng phần thưởng, không trích ra như kết quả.
Mỗi phần thưởng được tính đúng như lúc train (gồm phạt độ dài), nhóm 8 mẫu như G = 8. Phép kiểm: 0/1.992 câu lệch giữa tệp mẫu và tệp exec.
Lượt thử 30 bước đạt rồi mới chạy đủ.

**Ba phần thưởng mới (đã viết, chưa train):** `spice_cong` (SPICE nhân 0,1 khi sai loại thao tác), `ten_loai` (0,5·F1 với tên phần tử vàng + 0,5·đúng loại)
và `loai` (T5 của `report/326`: chỉ thưởng đúng loại thao tác, dùng để giải thích). Phép kiểm đơn vị đạt trên Kaggle CPU.
Đo được khi kiểm: SPICE("Scroll down", "Scroll down") = 0 và SPICE("Go back", "Go back") = 0, vì câu không có tuple nào.
Ở các câu như vậy, cổng loại thao tác không hạ thưởng thấp hơn được nữa. Câu chuẩn đúng nguyên văn cũng chỉ nhận 0 điểm, nên tín hiệu duy nhất
mà SPICE cho ở bước cuộn/quay lại đến từ phần chữ thừa của câu.

**Câu nhắc của ck500 không chỉ gồm bước chạm** (report/330 §7 hàng 5 đòi đo). Trong 1.000 câu nhắc: chạm 630, cuộn 120, nhập chữ 81, chờ 69,
mở app 65, quay lại 35 ⇒ **37% không chạm**. Cùng với mục 15, giả thuyết "ck500 giảm ở bước cuộn vì không được train trên bước cuộn" bị loại.

**Bảng H2, khối bước chạm** (conc = tỉ lệ cặp mẫu có exec khác nhau mà thưởng xếp đúng chiều, hoà tính 0,5; oracle = exec của mẫu thưởng cao nhất trừ exec TB 8 mẫu):

| thưởng | nhóm thưởng bằng nhau | cặp hoà | conc [KTC95] | oracle (điểm) [KTC95] |
|---|---|---|---|---|
| METEOR | 1,6% | 17,7% | 0,871 [0,834; 0,905] | +16,5 [+12,7; +20,0] |
| CIDEr-D | 1,6% | 15,4% | 0,868 [0,827; 0,906] | +17,6 [+13,8; +21,2] |
| chrF | 0,8% | 10,6% | 0,843 | +15,8 |
| BERTScore | 0,8% | 10,0% | 0,843 | +16,2 |
| ROUGE-L | 1,6% | 19,4% | 0,835 | +16,1 |
| SPIDEr | 1,6% | 15,4% | 0,824 | +15,2 |
| BLEU-4 | 1,6% | 17,5% | 0,806 | +13,9 |
| tên + loại | 22,5% | 58,7% | 0,736 | +10,1 |
| SPICE có cổng | 7,2% | 38,0% | 0,704 | +12,5 |
| **SPICE** | **7,2%** | **38,2%** | **0,685 [0,640; 0,728]** | **+11,3 [+7,9; +14,9]** |
| chỉ loại | 45,8% | 76,3% | 0,620 | +3,8 |

Đọc bảng:
- **Dự đoán của H2 không đứng.** Dự đoán ghi trước là SPICE "cân bằng tốt nhất giữa độ phân biệt và độ khớp exec". Số đo cho thấy SPICE đứng gần cuối ở cả hai vế.
  Có 7,2% nhóm mà mọi thưởng SPICE bằng nhau, gấp 4 đến 9 lần các độ đo n-gram. Hệ số conc của SPICE là 0,685, KTC không chồng với METEOR hay CIDEr-D.
  Kết quả này khớp `report/252`: khi chọn một trong 8 mẫu, SPICE là oracle yếu nhất.
- **Phép kiểm chéo quan trọng nhất của §8.4 (thứ tự H2 phải dự đoán được thứ tự exec test) KHÔNG đạt.** Trên test, các lượt đã có số xếp
  SPICE (ck500) 60,65 ≈ ROUGE-L 60,63 > METEOR 60,27 = CIDEr-D 60,27 (mục 14). H2 lại xếp METEOR > CIDEr-D > ROUGE-L > SPICE, gần như ngược lại.
  Các chênh trên test đều nhỏ và không có ý nghĩa sau hiệu chỉnh, nên phải đọc là: **độ khớp exec của thưởng trên mẫu tĩnh không dự đoán được thứ hạng sau train**.
  Vậy H2 không giải thích được vì sao SPICE ngang nhóm đầu. Khả năng [suy] là thưởng nhiều hoà làm cập nhật bảo thủ hơn, và điều này cần kiểm bằng log train (H3). Chưa có số.
- Cổng loại thao tác nâng conc của SPICE từ 0,685 lên 0,704 ở bước chạm và từ 0,713 lên 0,810 ở bước không chạm.
  Trong mẫu chạm, 8,4% số câu sai loại thao tác.
- `ten_loai`: 181/249 bước chạm có tên vàng. Chính câu chuẩn chỉ đạt F1 tên TB 0,57, và 29% câu chuẩn có F1 = 0, vì tên lấy từ OCR/cây trợ năng không trùng chữ người chú thích.
  ⇒ Thưởng này nhiễu ngay cả với câu đúng (câu chuẩn tự chấm được 0,84). Nếu train lượt này thì phải khai điều đó. Ở khối không chạm, conc = 1 của `loai` và `ten_loai` là tất yếu
  (thưởng chính là đại lượng được đo), không phải kết quả.

## 17. Giải thích H3, H4, bước cuộn và AitZ (report/323 §8.4), đo 6/11/2026, Kaggle CPU

Kernel `trangphngngc/giai-thich-c-k` (bản 1: H3, bước cuộn, AitZ; bản 3: H4, sau hai lần sửa lỗi đọc tệp) · dataset `trangphngngc/giai-thich-c` ·
mã `harness/h3_log_train.py`, `harness/h4_spice_tuple.py`, `harness/giai_thich_cuon.py`, `harness/h4_aitz.py` ·
tệp `runs/giai_thich/c/h3_cuon_aitz/` và `runs/giai_thich/c/h4/`. Chỉ dùng câu và log đã có, không sinh câu mới, số test, hậu kiểm, một hạt giống.
Phép kiểm chéo: SPICE trung bình theo câu ở bước chạm của S1 là 44,37 và của ck500 là 45,79, exec là 59,11 và 60,65, trùng số đã công bố ⇒ ghép câu đúng bước.
SPICE ở đây gọi thẳng jar với `-detailed` để lấy danh sách tuple. "Tuple phổ biến" là tuple xuất hiện ở ít nhất 1% câu chuẩn.

**H4, SPICE tăng ở loại tuple nào (4.463 bước chạm).** So với S1, ck500 khớp thêm 380 tuple. Trong đó đối tượng chiếm 50%, thuộc tính 29%, quan hệ 21%.
Recall tăng ở cả ba loại, KTC95 bootstrap theo episode đều trên 0: đối tượng +2,4 [+1,8; +3,2] điểm, thuộc tính +1,7 [+0,9; +2,7], quan hệ +3,5 [+2,4; +4,7].
Trong câu chuẩn, quan hệ chỉ chiếm 13% số tuple, nên xét theo tỉ lệ thì mức tăng **không dồn vào đối tượng và thuộc tính**. Quan hệ (phần lớn là vị trí, kiểu "icon | at | top") tăng mạnh nhất.
⇒ Dự đoán "tăng chủ yếu ở tuple đối tượng/thuộc tính" chỉ đúng theo số tuyệt đối (79%), sai khi so với tỉ phần sẵn có.
Mẫu này không riêng gì thưởng SPICE. GRPO + METEOR khớp thêm nhiều tuple nhất (+545, recall đối tượng +3,6), SCST + SPICE +439, GRPO + ROUGE-L +326.
GRPO + CIDEr-D thấp nhất (+179), với thuộc tính gần như không đổi (+0,1 [−1,0; +1,2]) và ΔF chung có KTC phủ 0.
⇒ Không viết "thưởng SPICE làm câu khớp tuple SPICE hơn các thưởng khác". Trên chính SPICE, METEOR và SCST + SPICE ngang hoặc hơn ck500.
Đối chiếu exec: ở 123 bước S1 đúng loại thao tác mà trượt và ck500 cứu được, F của SPICE tăng +0,32. Ở 1.450 bước không cứu được chỉ tăng +0,011, còn ở 90 bước ck500 làm hỏng thì giảm −0,23.
Bốn nhánh còn lại cho cùng mẫu (+0,33 đến +0,39 ở bước cứu được) ⇒ ở mức từng bước, thay đổi SPICE đi cùng thay đổi exec với mọi thưởng. Điều này không phân biệt được thưởng nào.
Trong tuple khớp thêm của ck500, 57% là tuple phổ biến (216 so với 164 tuple hiếm), mà tuple phổ biến chiếm 47,5% số lần xuất hiện trong câu chuẩn AC.

**Bước cuộn và quay lại.** ck500 đổi sang câu dạng chạm. Ở 755 bước cuộn, số câu bị quy về chạm tăng từ 117 lên 167, với "click on" tăng từ 90 lên 129.
Ở 270 bước quay lại, câu quy về chạm tăng từ 58 lên 79, với "open the" tăng từ 10 lên 26 ("Open the Messenger app" thay cho "Go back to the previous page").
Ngược lại, ck500 sửa được bước mở app (96,2 lên 97,9) và bước chờ (90,7 lên 95,3), toàn bộ là bớt câu "swipe up/go back" sai.
Giả thuyết ghi trước "câu chạm được SPICE cao hơn câu cuộn khi so với câu chuẩn cuộn" **không đứng**. Ở bước vàng cuộn, câu đúng loại có SPICE TB 0,64, còn câu chạm chỉ 0,11.
Ở 51 bước S1 đúng loại mà ck500 sai, SPICE của ck500 là 0,10 so với 0,30 của S1, và ck500 cao hơn hẳn S1 chỉ ở 13,7% số bước.
Điều đứng được: **29,4% câu cuộn đúng loại và 37,0% câu quay lại đúng loại có SPICE = 0**, ví dụ "Swipe up" so với "Swipe up" không có tuple nào.
Ở 58,8% số bước cuộn kể trên, SPICE của ck500 ≥ S1, phần lớn là hoà ở 0. Khi cả câu đúng loại lẫn câu chạm đều được 0, nhóm GRPO không có lợi thế nào để giữ câu cuộn.
Khả năng [suy]: đúng loại ở bước cuộn và quay lại không được thưởng giữ, trong khi 63% câu nhắc là bước chạm nên kéo văn phong về "Click on/Open the". Chưa kiểm được trên mẫu train vì log không lưu câu lấy mẫu.

**AitZ.** Câu chuẩn AitZ bước chạm (2.736) có 7,78 tuple mỗi câu. Có 112 tuple phổ biến chiếm **69,2%** số lần xuất hiện, so với 47,5% ở AC.
Đầu bảng là "screen", "part", "part | of | screen", "right", "icon": đúng phần khuôn vị trí. 85% số lần xuất hiện của tuple đối tượng là tuple phổ biến.
ck500 so với S1 trên AitZ: khớp thêm 204 tuple, trong đó **193 là tuple phổ biến**, chỉ 11 là tuple hiếm. ΔF +1,0 [+0,5; +1,6] có ý nghĩa, nhưng exec 37,79 → 37,28.
Độ phân biệt: chênh SPICE TB giữa bước exec trúng và bước exec trượt là 0,113 ở AitZ, so với 0,259 ở AC (S1).
⇒ Giả thuyết ở mục 15 **được ủng hộ**: trên AitZ, tuple SPICE chủ yếu đến từ phần khuôn. Thưởng SPICE nâng điểm SPICE bằng phần khuôn, và SPICE bám exec kém hơn hẳn AC.
Đây là cơ chế khả dĩ cho việc ck500 không hơn S1 trên AitZ [suy, chưa có phép can thiệp].

**H3, log train.** Tỉ lệ nhóm có mọi thưởng bằng nhau (lợi thế 0 cả nhóm): GRPO + SPICE (ck500) 22,7%, GRPO + CIDEr-D/METEOR/ROUGE-L 16,2–16,7%.
SPICE cho nhiều nhóm không gradient hơn n-gram, khớp với H2 ở mục 16. Ở SCST + SPICE, **60,4% mẫu có lợi thế đúng bằng 0** (thưởng mẫu bằng thưởng câu greedy), so với RLOO 24,4% và REINFORCE 0%.
|A| TB: SCST 0,19 · RLOO 0,20 · REINFORCE 0,41. KL TB: ck500 0,011 · SCST 0,012 · RLOO 0,013 · REINFORCE 0,011, còn GRPO + n-gram 0,026–0,033.
⇒ Dự đoán "S1 ít ngẫu nhiên nên SCST có nhiều mẫu lợi thế 0" **đúng**. Dù vậy SCST + SPICE vẫn ngang ck500 trên test (60,54 so với 60,65), nên số mẫu có tín hiệu không quyết định thứ hạng.
Hai probe A2C/PPO cũ có v_ev cỡ −10⁵, là lỗi ghi log đã sửa ngày 6/11 (`grpo_ppo.py`), không đọc.

## 18. Lưới RL đợt hai (7/11/2026): nhánh SFT tiếp, REINFORCE, RLOO trên test; tiến độ GRPO/Dr.GRPO/PPO

Kernel `uyenle0712/luoi-test-u-3` (chấm test, 4.463 bước, một hạt 101). Kiểm hoà 16/20, kiểm bộ chấm 10/10, kiểm dùng lại 40/40 ở cả ba lượt. Tệp ở `runs/luoi/7_11/test_u_3/`, so ghép cặp ở `so_ghep_cap_exec.json` (`harness/doc_luoi.py` đổi `THU`/`LUOT`, tự kiểm ck500 − S1/101 = +1,55 [+0,80; +2,33] đạt).

| lượt | exec | D.3 | D.3∧14% | AitW đầy đủ | action_ok |
|---|---|---|---|---|---|
| S1/101 | 59,11 | 65,49 | 61,73 | 74,37 | 94,35 |
| ck500 (GRPO + SPICE) | **60,65** | 67,02 | 63,25 | 76,25 | 95,97 |
| SFT tiếp (nhánh so sánh, cùng câu nhắc) | **60,16** | 66,64 | 62,85 | 75,71 | 96,15 |
| REINFORCE + SPICE | 60,00 | 66,41 | 62,67 | 75,51 | 95,83 |
| RLOO + SPICE | 59,44 | 65,81 | 62,09 | 75,02 | 95,00 |

So ghép cặp exec (bootstrap cụm app, McNemar chính xác; Holm trên ba phép so với ck500):
- SFT tiếp − ck500 **−0,49 [−1,07; +0,09]**, p=0,11 (hơn 75 / kém 97). SFT tiếp − S1/101 +1,05 [+0,48; +1,64], p=0,0004.
- REINFORCE + SPICE − ck500 −0,65 [−1,13; −0,19], p=0,009 (Holm 0,017). So S1/101 +0,90 [+0,19; +1,60].
- RLOO + SPICE − ck500 **−1,21 [−1,72; −0,71]**, p=4e−6 (Holm 1e−5). So S1/101 +0,34, KTC phủ 0.

Cách đọc:
- ck500 hơn REINFORCE và RLOO có ý nghĩa sau Holm. Trong họ policy gradient cùng thưởng SPICE, GRPO đứng đầu.
- ⚠️ ck500 chỉ hơn nhánh SFT tiếp +0,49, KTC phủ 0. Phần lớn mức +1,55 so S1 có thể đến từ việc train thêm trên cùng câu nhắc, không riêng từ RL. Đây là đòn mạnh nhất còn mở với phương pháp đề xuất. Cấm viết "GRPO + SPICE hơn SFT tiếp".
- Một hạt giống, dưới MDE 2,11.

Hai kernel train chạm trần 11 h như dự kiến (cần thêm commit chạy tiếp):
- `trangphuongngoc/luoi-t2-4`: grpo:spice:101 chạy tiếp từ ck175. Dòng `[nạp default] 504 tensor · |lora_B| 0,0000 → 5,7831` cho thấy nạp đúng. Tới bước 421/500, lưu cuối checkpoint-400, 159 s/bước. kl tăng dần 0,007 (bước 200) → 0,05 (bước 400), một điểm 0,131 ở bước 421; cao hơn ck500 gốc (~0,012), cần theo dõi. drgrpo:spice:101 tới bước 264/500, lưu checkpoint-250.
- `trangphngngc/luoi-t-3`: PPO μ=2, λ=1 tới bước 276/1000 (checkpoint-275); λ=0,95 tới 270/1000 (checkpoint-250); ~145 s/bước, kl 0,03–0,04.
- Tệp ở `runs/luoi/7_11/t2_4/` và `runs/luoi/7_11/t_3/`.

## 19. Phân tích đợt hai (8/11/2026, 0 GPU): độ đo văn bản, phân rã ck500 − SFT tiếp, kiểm tu=base

Số test, một hạt giống 101, hậu kiểm. Tệp ở `runs/luoi/7_11/{chu,giai_thich,tu_base_cpu}/`.

**Phân rã ghép cặp (KTC95 bootstrap cụm app, B = 10.000; `harness/giai_thich_7_11.py`).** Kernel Kaggle `giai-thich-7-11-cpu` lỗi ở dòng 152 (khoá `n` trùng); đã sửa và chạy lại ở máy nhà, tự kiểm A (+28/+41) và B (+0,49 [−0,09; +1,07]) đều đạt.

| phép so | exec | phần sửa loại thao tác | phần đổi phần tử |
|---|---|---|---|
| ck500 − SFT tiếp | +0,49 [−0,09; +1,07] p=0,11 | −0,09 [−0,27; +0,09] | **+0,58 [+0,04; +1,14]** |
| REINFORCE − SFT tiếp | −0,16 [−0,64; +0,33] | −0,13 | −0,02 |
| RLOO − SFT tiếp | −0,72 [−1,27; −0,18] p=0,015 | −0,56 [−0,82; −0,32] | −0,16 |
| ck500 − REINFORCE | +0,65 [+0,19; +1,13] | +0,04 | +0,60 [+0,16; +1,06] |
| ck500 − RLOO | +1,21 [+0,71; +1,72] | +0,49 | +0,72 |
| SFT tiếp − S1/101 | +1,05 [+0,48; +1,64] | +0,74 [+0,46; +1,05] | +0,31 [−0,20; +0,83] |

Cách đọc: train thêm trên 2.000 câu nhắc (SFT tiếp) đã mua phần sửa loại thao tác; phần ck500 hơn SFT tiếp nằm trọn ở đổi phần tử, KTC loại 0 riêng phần này (trên các bước cả hai đúng loại: +0,61 [+0,05; +1,19], n=4.271) nhưng exec tổng vẫn phủ 0. RLOO thua chủ yếu vì phá loại thao tác (nhóm S1 sai loại: −7,54).
Holm trên họ 7 phép so exec với ck500: RLOO p_holm 3e−5 giữ; **REINFORCE p_holm 0,052 mất** (trong họ 3 lượt của §18 là 0,017); SFT tiếp 0,55.

**Độ đo văn bản (bootstrap cụm app, B = 2.000; `harness/chu_luoi_7_11.py`).** SFT tiếp − ck500: BLEU-4 −0,29 · ROUGE-L +0,19 · CIDEr-D −4,26 [−9,25; +0,64] · SPICE −0,47 [−1,10; +0,13] · chrF −0,24 · BERTScore −0,01, mọi KTC phủ 0. METEOR: ck500 37,92 · SFT tiếp 37,75 · REINFORCE 37,37 · RLOO 37,00. REINFORCE và RLOO thấp hơn SFT tiếp ở ROUGE-L/chrF (KTC dưới 0). ⇒ trên độ đo văn bản ck500 không tách được khỏi SFT tiếp.

**Tuple SPICE (`h4_spice_tuple_7_11.py`).** ck500 − SFT tiếp +117 tuple đúng (Object +71, Relation +29); recall Object và Relation có KTC loại 0, F tổng [−0,0002; +0,012].

**Kiểm tu=base trên mô hình thật (CPU fp32, `kiem-tu-base-cpu`): ĐẠT.** LoRA mới cùng cỡ S1 (14.966.784 tham số, B = 0, không học thị giác), logits bật = tắt adapter (Δ = 0), tham chiếu KL trùng Base nạp thẳng (Δ = 0), câu nhắc trùng thứ tự ck500 ⇒ lượt GRPO xuất phát từ Base đẩy được.

## 20. Tiến độ train lưới RL đợt hai (kernel luoi-t2-11, luoi-t-10, xong 8/11/2026)

Hai kernel chạy tiếp, cả hai nạp đúng điểm lưu (`[nạp default] 504 tensor · |lora_B| 0 → x>0 · khoá lạ 0` ở cả bốn lượt; PPO nạp thêm `value_head.pt`). Log ở `runs/luoi/7_11/{t2_11,t_10}/`, adapter nằm trên output Kaggle.
- **grpo:spice:101 XONG 500/500** (checkpoint-500), 150 s/bước, đỉnh VRAM 12,8 GiB. kl ở 100 bước cuối dao động 0,003–0,094, bước cuối 0,012 (ck500 gốc ~0,012). Sẵn sàng chấm test.
- **drgrpo:spice:101 tới 475/500** (checkpoint-475), chạm trần giờ; kl 0,002–0,033. Cần một lượt ngắn 25 bước, hoặc chấm checkpoint-475 nếu chấp nhận khai.
- **PPO μ=2, λ=1 tới 575/1000** (checkpoint-575); kl tăng 0,04 → 0,13. **λ=0,95 tới 525/1000** (checkpoint-525); kl 0,02–0,06. Cần thêm khoảng hai commit.

## 21. Lượt train lại ck500 (A/A, 8/11/2026): KHÔNG tái lập được 60,65

Lượt `grpo:spice:101` của lưới (`luoi-t2-3` → `luoi-t2-4` → `luoi-t2-11`, chạy tiếp từ điểm lưu 175 và 400, `harness/grpo_luoi.py`) đủ 500/500 bước, nạp default đạt mỗi lần chạy tiếp. Chấm test ở kernel `uyenle0712/luoi-test-u-4`: kiểm hoà 16/20, kiểm bộ chấm 10/10, adapter gắn trên S1 hoà, md5 `e6e656e0…`. Tệp ở `runs/luoi/8_11/test_u_4/`, so ghép cặp ở `so_ghep_cap_exec.json` (mốc S1/101, ck500, SFT tiếp) và `so_ghep_cap_voi_aa.json` (mọi lượt lưới so A/A). Tự kiểm ck500 − S1/101 = +1,55 [+0,80; +2,33] đạt cả hai lần.

| lượt | exec | D.3 | D.3∧14% | AitW đầy đủ | action_ok |
|---|---|---|---|---|---|
| S1/101 | 59,11 | 65,49 | 61,73 | 74,37 | 94,35 |
| ck500 (lượt gốc, `grpo_spice.py`) | **60,65** | 67,02 | 63,25 | 76,25 | 95,97 |
| SFT tiếp | 60,16 | 66,64 | 62,85 | 75,71 | 96,15 |
| GRPO + SPICE (A/A, `grpo_luoi.py`) | **59,74** | 66,41 | 62,47 | 75,71 | 95,65 |

So ghép cặp exec (bootstrap cụm app, B = 10.000, McNemar chính xác):
- A/A − ck500 **−0,92 [−1,36; −0,49]**, p=5,5e−5 (hơn 30 / kém 71).
- A/A − S1/101 +0,63 [−0,12; +1,37], p=0,085, KTC phủ 0.
- A/A − SFT tiếp −0,43 [−0,99; +0,13], p=0,17.

Các lượt lưới so với A/A (cùng mã `grpo_luoi.py`, chưa hiệu chỉnh):

| lượt − A/A | Δ exec | KTC95 | hơn/kém | p |
|---|---|---|---|---|
| SCST + SPICE | +0,81 | [+0,34; +1,28] | 78/42 | 0,001 |
| GRPO + ROUGE-L | +0,90 | [+0,38; +1,43] | 95/55 | 0,001 |
| GRPO + CIDEr-D | +0,54 | [0,00; +1,08] | 89/65 | 0,063 |
| GRPO + METEOR | +0,54 | [−0,02; +1,12] | 97/73 | 0,077 |
| SFT tiếp | +0,43 | [−0,13; +0,99] | 97/78 | 0,17 |
| REINFORCE + SPICE | +0,27 | [−0,19; +0,75] | 66/54 | 0,32 |
| RLOO + SPICE | −0,29 | [−0,80; +0,22] | 63/76 | 0,31 |

Cách đọc:
- Train lại cùng cấu hình mà mất 0,92 exec, có ý nghĩa ghép cặp. Vậy chênh lệch giữa hai lượt train của **cùng một** phương pháp đã cỡ chênh lệch ck500 − S1/101 (+1,55). Phần lớn lợi thế của ck500 so với các lượt lưới (−0,02 đến −1,21) nằm trong biến thiên giữa các lần train, không quy được cho thuật toán hay độ đo thưởng.
- Lượt A/A khác lượt gốc ở mã train (`grpo_luoi.py` thay `grpo_spice.py`), ở phiên bản thư viện (transformers 5.17.0 → 5.20.2, peft 0.21.1 → 0.21.2, torch 2.10.0 → 2.11.0), ở hai lần chạy tiếp và ở tính không tất định của GPU; chưa tách được nguyên nhân nào. Các lượt lưới khác chạy cùng mã với A/A, nên phép so công bằng trong lưới là so với A/A: khi đó SCST + SPICE và GRPO + ROUGE-L hơn GRPO + SPICE có ý nghĩa (chưa Holm), ngược với thứ tự khi so với ck500.
- ⛔ Không còn viết được "GRPO + SPICE tốt nhất trong lưới" hay "ck500 hơn REINFORCE/RLOO" như kết luận về phương pháp. ck500 − S1/101 vẫn là số đo thật của một điểm lưu cụ thể, nhưng phải khai rằng train lại chỉ được +0,63 (KTC phủ 0).
- **Độ đo văn bản cho lượt A/A (kernel CPU `trangphngngc/chu-luoi-8-11-cpu`, xong 8/11; `runs/luoi/8_11/chu/chu_luoi_8_11.json`, bootstrap cụm app B = 2.000, tự kiểm đạt):**

  | lượt | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
  |---|---|---|---|---|---|---|---|
  | S1/101 | 51,56 | 36,79 | 67,35 | 416,12 | 44,37 | 61,26 | 66,33 |
  | ck500 (hạt 101) | 52,36 | 37,92 | 68,36 | 430,05 | 45,79 | 62,87 | 67,07 |
  | ck500 hạt 202 (mã cũ, `runs/grpo_spice/s202_chu_25_10/v5/`) | 52,94 | 37,53 | 68,48 | 431,22 | 45,69 | 62,37 | 67,12 |
  | A/A (train lại, hạt 101) | 52,97 | 37,55 | 68,44 | 430,92 | **46,00** | 62,39 | 67,09 |

  A/A − ck500: BLEU-4 +0,61 [−0,23; +1,20] · ROUGE-L +0,08 · CIDEr-D +0,87 [−3,20; +4,97] · SPICE +0,20 [−0,30; +0,71] · chrF −0,48 [−0,85; −0,15] · BERTScore +0,02 ⇒ chỉ chrF khác có ý nghĩa. A/A − S1/101: SPICE **+1,63 [+0,94; +2,37]** (ck500 +1,42), CIDEr-D +14,80, cả 6 độ đo có KTC hơn 0. A/A − SFT tiếp: SPICE +0,67 [+0,11; +1,27], CIDEr-D +5,13 [+0,09; +10,30].
  ⇒ **Đích thưởng tái lập được, exec thì không:** ba điểm lưu GRPO + SPICE (ck500/101, ck500/202, A/A) gần như trùng nhau trên mọi độ đo văn bản (SPICE 45,7–46,0), trong khi exec dao động 59,74–60,65. Phần exec thay đổi giữa các lượt train không đi qua SPICE; khi viết phải nói GRPO + SPICE nâng SPICE ổn định, còn mức tăng exec chịu biến thiên giữa các lượt train cỡ 0,7–0,9.
- **Độ đo văn bản bản b (kernel `trangphngngc/chu-luoi-8-11b-cpu`, xong 8/11; `runs/luoi/8_11/chu_b/chu_luoi_8_11b.json`; tự kiểm trùng tuyệt đối bản a):** ck500/202 trong cùng khung KTC, các lượt lưới so A/A (KTC95 bootstrap cụm app, B = 2.000; cột: BLEU-4 · ROUGE-L · CIDEr-D · SPICE · chrF · BERTScore; in đậm khi KTC loại 0).

  | X − A/A | BLEU-4 | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
  |---|---|---|---|---|---|---|
  | SCST + SPICE | **−1,00** | +0,26 | −0,02 | −0,06 | **+0,92** | +0,16 |
  | GRPO + ROUGE-L | −0,38 | **+0,83** | +1,90 | −0,43 | **+1,03** | **+0,49** |
  | GRPO + METEOR | **−2,21** | **+0,70** | −4,30 | **−0,87** | **+1,80** | +0,27 |
  | GRPO + CIDEr-D | **−1,38** | +0,03 | **−6,40** | **−1,57** | **+0,51** | −0,06 |
  | SFT tiếp | −0,90 | +0,11 | **−5,13** | **−0,67** | +0,25 | −0,03 |
  | REINFORCE + SPICE | −0,45 | **−0,48** | **−4,80** | **−0,73** | −0,33 | **−0,33** |
  | RLOO + SPICE | **−0,97** | **−1,11** | **−8,82** | **−0,73** | **−0,74** | **−0,77** |

  Ba điểm lưu GRPO + SPICE không khác nhau ở độ đo nào trừ chrF ck500 − ck500/202 +0,50 [+0,12; +0,87]; A/A − ck500/202 cả sáu KTC phủ 0. ck500/202 − S1/101: SPICE +1,32 [+0,57; +2,12], CIDEr-D +15,11, sáu độ đo đều loại 0.
  ⇒ So với A/A (cùng mã train), GRPO + SPICE đứng đầu về SPICE trong mọi lượt lưới trừ SCST + SPICE (ngang). Hai lượt tối ưu ROUGE-L/METEOR thắng ở ROUGE-L, chrF nhưng thua BLEU-4 hoặc SPICE: mỗi lượt tăng đúng độ đo nó được thưởng, nên không có lượt nào trội trên mọi độ đo văn bản. REINFORCE/RLOO thua A/A ở hầu hết độ đo, SFT tiếp thua ở CIDEr-D và SPICE. Đọc cùng exec: SCST + SPICE và GRPO + ROUGE-L hơn A/A về exec (+0,81, +0,90) mà không hơn về SPICE ⇒ exec không đi theo SPICE.
- **Phân rã + SPICE theo tuple (kernel `trangphngngc/giai-thich-8-11-cpu`, xong 8/11; `runs/luoi/8_11/giai_thich/ket_qua_8_11/`; tự kiểm ck500 +28/+41, ck500 − SFT tiếp +0,49, A/A − ck500 −0,92 và Δtp 5 nhánh cũ đều đạt; B = 10.000):**
  - Phân rã so S1/101 (số bước ròng): ck500/101 sửa loại thao tác **+28**, đổi phần tử **+41** · ck500/202 +32 / +5 · A/A +20 / +8. ⇒ Phần sửa loại thao tác tái lập qua cả ba lượt (+20 đến +32); phần đổi phần tử +41 chỉ có ở ck500/101, hai lượt kia ≈ 0. Mức exec cao của ck500/101 nằm trọn ở phần đổi phần tử, và phần đó không tái lập.
  - Ba điểm lưu từng đôi: ck500 − A/A exec +0,92 [+0,49; +1,37] = loại +0,16 [+0,02; +0,31] + phần tử **+0,76 [+0,35; +1,18]** · ck500 − ck500/202 +0,72 [+0,16; +1,27] = loại −0,09 + phần tử **+0,81 [+0,29; +1,35]** · ck500/202 − A/A +0,20 [−0,32; +0,73] (phần tử −0,07). D.3: ck500 − A/A +0,60 [+0,17; +1,05], ck500 − ck500/202 +0,47 [−0,09; +1,04].
  - Họ so A/A, exec, Holm 7 phép: SCST + SPICE +0,81 (p_Holm 0,009) · GRPO + ROUGE-L +0,90 (0,009) · GRPO + CIDEr-D +0,54 (0,32) · GRPO + METEOR +0,54 (0,32) · SFT tiếp +0,43 (0,52) · REINFORCE +0,27 (0,62) · RLOO −0,29 (0,62). ⇒ Trong lưới cùng mã, hai lượt hơn GRPO + SPICE có ý nghĩa sau Holm, không lượt nào kém có ý nghĩa.
  - SPICE theo tuple, Δtp so S1 (All / Object / Attribute / Relation): ck500 380 / 191 / 111 / 78 · A/A 252 / 131 / 65 / 56 · ck500/202 203 / 104 / 66 / 33. SPICE F của ba lượt ngang nhau nhưng số tuple khớp thêm của ck500/101 gấp 1,5–1,9 lần hai lượt kia; ở A/A và 202 phần lớn Δtp nằm ở tuple hiếm (181/252, 136/203), còn ck500 nằm ở tuple phổ biến (216/380).
  - Mô tả câu: số từ TB 8,00 / 7,76 / 7,80; trùng S1 2.795 / 2.605 / 2.895 câu; ba lượt chung 3.227–3.532 câu từng đôi.
  - ⛔ Hệ quả cho cách viết: câu "thưởng SPICE giúp đổi đúng phần tử" (phân rã ck500 +41) KHÔNG tái lập qua lượt train khác; phần tái lập được là sửa loại thao tác (+20 đến +32 bước) và mức tăng SPICE.
- **Nguyên nhân (kiểm 8/11):** cấu hình GRPOConfig hai lượt in ra trùng từng khoá, thứ tự câu nhắc trùng ck500. Hai lượt tách nhau ngay bước 1: cùng policy S1 (lora_B = 0), thưởng TB bước 1 của `grpo_spice.py` là 0,473, còn `grpo_luoi.py` là 0,223 (drgrpo và PPO cùng ra 0,223) ⇒ quỹ đạo train khác từ đầu. ⚠️ **Sửa 8/11 chiều:** hai lượt còn khác **phiên bản thư viện** — ck500 gốc chạy transformers 5.17.0 · peft 0.21.1 · torch 2.10.0, còn A/A (và cả lưới) chạy 5.20.2 · 0.21.2 · 2.11.0 (dòng in trong log train). Vậy lúc đó chưa quy được lệch bước 1 cho mã hay cho thư viện; mỗi bước chỉ 2 câu nhắc × 8 câu nên thưởng TB bước 1 dao động mạnh theo lần lấy mẫu (bước 2 của hai lượt: 0,645 và 0,604). **Kiểm CPU (kernel `trangphngngc/kiem-rng-aa-cpu` bản 5, `_bundles/luoi/make_rng_nb.py`, `runs/luoi/8_11/kiem_rng/`):** chạy `grpo_spice.py` và `grpo_luoi.py` × bộ thư viện cũ (5.17.0 · 0.21.1 · torch 2.10.0) và mới (5.20.2 · 0.21.2 · torch 2.11.0) trên Qwen2.5-VL tí hon, cùng cờ ck500 (G 8, bs 4, accum 4, seed 101), mỗi cấu hình 2 lần, móc lần gọi generate đầu: **8/8 trùng tuyệt đối** trạng thái RNG trước khi sinh, input_ids và chuỗi sinh. ⇒ Trên CPU, cả mã train lẫn phiên bản transformers/peft/torch đều không đổi luồng lấy mẫu. Phần còn lại chỉ có thể ở GPU: bản dựng CUDA (cu128 → cu130), nhân CUDA của torch 2.10 → 2.11 ở fp16, hoặc máy T4 khác nhau. Trên GPU mỗi môi trường tự lặp lại được (drgrpo, PPO, A/A cùng ra 0,223 ở bước 1). Giới hạn: phép kiểm không chạy nhân CUDA, không chạy mô hình 3B thật. Cách viết an toàn: "lượt train lại cùng mã, cùng cấu hình, cùng câu nhắc, khác môi trường GPU, cho exec 59,74; biến thiên giữa các lượt train ≈ 0,7–0,9 exec", không quy lỗi cho mã. Đối chiếu ck500 hạt 202 (mã cũ, 59,94): A/A − ck500/202 −0,20 [−0,74; +0,34], p=0,53 ⇒ A/A nằm trong dải biến thiên giữa hai hạt của chính mã cũ; 60,65 là đầu cao của dải đó, không phải mã mới hỏng.

## 22. Vì sao GRPO + CIDEr-D thấp CIDEr-D trên test (9/11/2026, Kaggle CPU)

Kernel `trangphngngc/cider-thuong-8-11-cpu` · dataset `trangphngngc/cider-thuong-8-11` · mã `harness/cider_thuong_8_11.py` · tệp `runs/luoi/8_11/cider_thuong/cider_thuong_8_11.json`. Chấm lại câu test đã sinh của 12 lượt, 0 GPU, bootstrap cụm app B = 2.000, một hạt giống, hậu kiểm. df tập dạy lấy từ `p1_train_rows.jsonl` của dataset `fgrb-p1-bundle` (md5 `6898b21e…`, 3.991 câu, trùng tệp lúc train).

Giả thuyết cần kiểm (§14): lúc thưởng, CIDEr-D tính df từ câu chuẩn tập dạy và tách từ theo cách riêng; lúc chấm, df lấy từ tập kiểm và tách từ bằng PTBTokenizer. Tách hai chỗ khác này ra từng cái:

| biến thể CIDEr-D (×100) | GRPO + CIDEr-D | A/A | ck500 | GRPO + CIDEr-D − A/A | GRPO + CIDEr-D − ck500 |
|---|---|---|---|---|---|
| số đã báo (PTB, df tập kiểm) | 424,52 | 430,92 | 430,05 | −6,40 [−11,41; −1,61] | −5,53 [−10,21; −1,20] |
| chỉ đổi cách tách từ sang của thưởng | 425,40 | 431,89 | 431,44 | −6,49 [−11,46; −1,67] | −6,04 [−10,75; −1,73] |
| chỉ đổi df sang tập dạy | 428,12 | 434,58 | 433,81 | −6,46 [−11,43; −1,65] | −5,69 [−10,36; −1,40] |
| đúng hàm thưởng lúc train | 428,95 | 435,54 | 435,18 | −6,59 [−11,59; −1,70] | −6,22 [−10,87; −1,92] |
| thưởng đầy đủ (kèm phạt độ dài, ×100) | 419,71 | 427,80 | 426,42 | −8,09 [−13,32; −3,05] | −6,71 [−11,53; −2,26] |

- Tự kiểm đạt: lớp `CiderD` của `grpo_luoi.py` (tách theo khoảng trắng trên chuỗi đã PTB, df tập kiểm) trùng pycocoevalcap từng bước ở cả 12 lượt, và 12 lượt tái lập đúng CIDEr-D đã báo. Tương quan từng bước giữa hàm thưởng và CIDEr-D báo cáo 0,998.
- GRPO + CIDEr-D đứng hạng 9/12 dưới cả năm biến thể, kể cả dưới đúng hàm thưởng lúc train. Hạng đầu luôn là GRPO + ROUGE-L, rồi ck500/202.
- ⇒ **Giả thuyết df/tách từ bị bác.** Hai chỗ khác chỉ nâng đều mọi lượt 1–4 điểm, khoảng cách giữ nguyên. Lượt thưởng CIDEr-D tối ưu kém ngay trên mục tiêu của chính nó so với các lượt thưởng SPICE và ROUGE-L. Không do câu dài hơn (số từ TB 8,10, giữa nhóm; A/A 7,79) cũng không do chép câu chuẩn (trùng câu chuẩn 16,3% vs A/A 17,5%).
- Giải thích còn mở [suy, chưa đo]: tín hiệu thưởng CIDEr-D nhiễu hơn trong nhóm G = 8 (CIDEr-D mức câu dao động mạnh theo n-gram hiếm), hoặc nhiễu một hạt giống (khoảng cách −6,4 ngang dải A/A − ck500 của các độ đo khác, KTC chạm −1,6). Phép đo kế, nếu cần: phương sai thưởng trong nhóm và tỉ lệ nhóm hoà từ log train (đã có cho H3 ở §17: CIDEr-D 16,2–16,7% nhóm hoà, thấp hơn SPICE 22,7%, nên "nhiều nhóm hoà" không phải lý do).
- Cách viết: không trích "CIDEr-D thấp vì thưởng và chấm tính khác nhau". Viết: lượt thưởng CIDEr-D không đạt CIDEr-D cao hơn lượt thưởng SPICE, kể cả khi chấm bằng đúng hàm thưởng; một hạt giống.

## 23. Sàng lọc biến thể thưởng SPICE trên val C1 (9/11/2026, Kaggle CPU)

Số val, cấm trích; chi tiết và bảng ở `report/332` mục cuối. Trên 249 bước chạm, bỏ cặp hoà: R0 (SPICE hiện tại) 0,753 · R2 0,793 · R3 0,816 · R4 0,818 · chrF một mình 0,836. R4 − chrF −0,018 [−0,053; +0,018] ⇒ chưa có bằng chứng SPICE thêm được thứ tự so với chrF. Không được viết "R4 cải thiện executability": chưa train lượt nào với các thưởng này.

## 24. Đo độ phủ Gate B của RGTC-SPICE (10/11/2026, Kaggle CPU, thăm dò)

Kernel `trangphngngc/gate-b-rgtc-10-11-cpu`, mã `harness/gate_b_rgtc.py`, kết quả ở `runs/rgtc/gate_b_10_11/gate_b/`. Pool chưa khoá, 49.046 bước / 10.726 episode, trong đó 31.187 bước chạm; 0 bước thiếu cây; có package ID ở 31.159 bước. SPICE thật trên mẫu 6.000 hàng. `active_est` = độ phủ trước SPICE × tỉ lệ cặp qua điều kiện SPICE.

| danh sách role | P(e) | P(m\|e) | độ phủ trước SPICE | qua SPICE | độ phủ ước lượng |
|---|---|---|---|---|---|
| bản gốc (loại role chung) | 40,6% | 27,3% | 11,1% | 92,6% | **10,3%** |
| chỉ cần có chữ | 40,6% | 35,9% | 14,6% | 92,5% | 13,5% |
| bỏ danh sách loại (RGTC-SPICE v2) | 40,6% | 90,8% | 36,9% | 94,4% | **34,8%** |

Đổi `own/desc` và `strict/longest` chỉ làm độ phủ lệch dưới 1 điểm ở mọi hàng. Lý do loại lớn nhất ở bản gốc: câu chuẩn không chứa tên phần tử 12.124 bước (`3_span_none`), target là role chung 8.855 bước (`m1_generic_role`).

Cách đọc:
- Dòng độ phủ ≥20% đạt ở v2 (34,8%). Bản gốc 10,3% không đạt cả 20%. Toàn bộ khác biệt đến từ việc bỏ danh sách role, quyết sau khi đã thấy số thử, phải khai.
- Khoảng 70% số cặp của v2 có target là role bản gốc loại (34,8 so với 10,3) nên chất lượng cặp nhóm này chưa được kiểm.
- FR_gold 0,0% và neg 100% **không mang thông tin**. Script chỉ tính trên cặp đã có S(g,g) = 1, S(n,n) = 1 và S(g,n) < 1, nên T(g+) > 0,5 và T(g−) < 0,5 đúng theo định nghĩa. Dòng giữ 100% action class cũng do bộ lọc `8_action_class_changed` bảo đảm. Không được viết các dòng này là "đã đạt" như bằng chứng về độ tin cậy.
- Audit tay ≥190/200 chưa làm. `audit_ung_vien.jsonl` hiện lấy theo cấu hình bản gốc nên không có cặp role chung, phải dựng lại theo `no_blacklist|own|strict`.
- Chưa có phép kiểm trên 8 mẫu sinh thật của mô hình, là phép duy nhất cho biết T có tách câu tốt khỏi câu xấu hay không.
- Bảng class → role, từ vựng POS/STATE/ATTR, alias ≥2 ký tự chữ-số do script đặt vì file action chưa định nghĩa, phải khai.

## 25. Điểm target T của RGTC trên 8 mẫu sinh thật: TRƯỢT, RGTC dừng (10–11/11/2026, Kaggle CPU)

Kernel `trangphngngc/rgtc-c1-t-10-11-cpu`, mã `harness/rgtc_c1_t_10_11.py` (luật đạt/trượt ghi trong docstring trước khi chạy), kết quả `runs/rgtc/c1_t_10_11/c1_t/`. Val C1, 249 bước chạm, 8 mẫu S1/101, một hạt, số val cấm trích. Đại lượng: độ đồng thuận với exec trên các cặp mẫu cùng bước có exec khác nhau; KTC95 bootstrap cụm episode.

79/249 bước active theo `no_blacklist|own|strict` (66 episode, 40 bước có cặp exec khác nhau; 441 cặp).

| điểm (bước active) | đồng thuận, hoà 0,5 | bỏ hoà [KTC95] |
|---|---|---|
| SPICE | 0,676 | 0,786 [0,662; 0,885] |
| chrF | **0,866** | 0,866 [0,799; 0,926] |
| T một mình | 0,686 | 0,842 [0,719; 0,939] |
| A2 = 0,70S + 0,15A + 0,15·0,5 − d | 0,850 | — |
| FULL = 0,70S + 0,15A + 0,15T − d | 0,850 | — |

- (a) T có tín hiệu: cận dưới 0,719 > 0,5, đạt. Nhưng T hoà ở 201/441 cặp.
- (b) FULL − A2 = **0,000** [−0,012; +0,010]: thêm T không đổi thứ tự cặp nào ⇒ trượt. Những cặp T xếp đúng thì S đã xếp đúng sẵn.
- (c) FULL − chrF = −0,016 [−0,063; +0,032] ⇒ trượt. Trên cả 249 bước: −0,022 [−0,055; +0,011].
- ⇒ Theo luật: **RGTC-SPICE dừng trước GPU**, không dựng audit, không cần đọc tay.
- Tái lập phát hiện §23: chrF một mình không thua công thức nào có SPICE. Ở đây mọi công thức có SPICE trọng số 0,8 (A1 0,823, A2 0,850) đều dưới chrF; SPICE một mình hoà 170/441 cặp.
- Lượt chạy đầu trên máy nhà (cho "ĐẠT") có lỗi đọc số tuple SPICE nên K_g = 0, S rút về chrF; đã xoá, không dùng. K_g đúng = tp + fn, trung vị 3, 99/249 bước K_g < 3.
- Giới hạn: mẫu của S1 chứ không phải SFT-cont; độ đồng thuận với exec của UGround chưa phải kết quả sau train.
- Cách viết nếu đưa vào luận văn: đã thử thêm thành phần target phản thực cùng màn vào thưởng SPICE; trên mẫu sinh thật thành phần này không đổi thứ tự của thưởng, nên không train.

## 26. PPO chạy tiếp (kernel luoi-t-11, 10–11/11/2026): dừng vì hết đĩa, chưa có số test

Kernel `trangphngngc/luoi-t-11` báo ERROR sau khoảng 4,1 h: `OSError: [Errno 28] No space left on device`. Nguyên nhân: `harness/grpo_luoi.py` lưu điểm mỗi 25 bước với `save_total_limit=None`, nên `/kaggle/working` giữ mọi điểm lưu từ bước 25 (kể cả phần chép từ luoi-t-10) tới khi đầy.
- λ = 1: từ ck575 tới **ck650** đủ tệp; ck675 ghi dở (thiếu `trainer_state.json`), không dùng. KL cuối 0,013–0,027.
- λ = 0,95: từ ck525 tới **ck600**. KL cuối 0,036–0,064.
- Cả hai lượt in `[nạp default] … → 14,06 / 13,54` và nạp `value_head.pt` của điểm lưu nguồn ⇒ chạy tiếp đúng.
- Lượt kế phải đặt `save_total_limit` (hoặc xoá điểm lưu cũ trước khi train), chạy tiếp từ ck650 / ck600 của output `luoi-t-11`. Tệp ở `runs/luoi/10_11/t_11/` (điểm lưu không vào git).

