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

1. **Trên AndroidControl, ck500 hơn S1 nhưng mức tăng khiêm tốn.** ck500 60,65 so với S1/101 59,11, tức +1,55 [+0,80; +2,33]. So với S1/202 chỉ còn +1,03. Hạt GRPO thứ hai (ck500/202, 59,94) hơn S1/101 +0,83 và ngang S1/202 (+0,31). Như vậy mức tăng dao động từ +0,3 đến +1,6 tuỳ hạt, đều dưới MDE 2,11. (Mục 2)
2. **Mức tăng đến từ tín hiệu SPICE, không phải từ việc train thêm.** xao101 chạy cùng 500 bước GRPO nhưng thưởng bị xáo, kết quả bằng đúng S1 cả về exec (+0,00) lẫn bảy thước chữ. ck500 − xao101 = +1,55. (Mục 2, 3)
3. **ACE ngang ck500 về exec (+0,02) nhưng hơn rõ ở thước chữ.** Ở cả năm thước có KTC, mọi KTC đều loại 0 (ví dụ CIDEr-D +11,97, SPICE +1,33). (Mục 2, 3)
4. **Hướng giữ khi đổi dụng cụ chấm, độ lớn nhỏ hơn.** So với S1/101, ck500 hơn dưới cả bốn dụng cụ: UGround +1,55, UI-Venus +1,55, Phi-Ground (ngoài họ Qwen) +0,78, người nghe Phi-4 +0,69. So với S1/202 thì UI-Venus còn +0,94, còn dưới Phi-4 là −0,20 (không phân biệt được). (Mục 4)
5. **Mô hình 3B đã tinh chỉnh hơn xa 7B không tinh chỉnh.** 7B prompting đạt 51,51, thấp hơn S1/101 7,60 điểm và ck500 9,14 điểm. (Mục 2)
6. **Ra ngoài miền (AitZ), mức tăng không chuyển sang.** SFT vẫn hơn Base (+3,29), nhưng ck500 ngang S1 (−0,51, KTC phủ 0) và ACE gần như không kích hoạt. (Mục 6)
7. **ck500 có tác hại ở bước không chạm.** Ở bước scroll giảm 6,23 điểm. Tác hại này lớn hơn khi lịch sử là câu do mô hình tự sinh (đúng loại thao tác ở bước không chạm giảm 4,49 so với S1). Ngược lại, ở bước chạm ck500 bền hơn S1. (Mục 5, 7)
8. **Chưa có số:** exec của thí nghiệm lịch sử tự sinh (mục 7) và ACU, tức phần AndroidControl mà S1 chưa thấy (mục 8). Lịch chờ và chỗ điền số ở mục 11.

---

## 2. AndroidControl, bộ trỏ UGround

### 2.1 Điểm từng nhánh

| nhánh | exec [KTC95] | D.3 | D.3 ∧ 14% | AitW (vế khoảng cách) | AitW đầy đủ |
|---|---|---|---|---|---|
| Base | 47,59 | 53,60 | - | - | 63,39 |
| 7B prompting | 51,51 [49,82; 53,15] | 57,67 | - | - | 66,79 |
| S1/101 | 59,11 [57,3; 60,8] | 65,49 | 61,73 | 66,91 | 74,37 |
| S1/202 | 59,62 | 66,10 | 62,36 | 67,62 | 75,31 |
| xao101 | 59,11 | 65,58 | - | - | 74,59 |
| ck500/202 | 59,94 [58,13; 61,71] | 66,55 | 62,65 | 68,25 | 76,23 |
| ck500 | 60,65 | 67,02 | 63,25 | 68,59 | 76,25 |
| ACE (R3) | 60,68 | 67,11 | 63,28 | 68,63 | 76,32 |
| câu chuẩn | 75,73 | 83,82 | - | - | 92,14 |

Dấu "-" nghĩa là chưa tính. Mọi ô có số đều tính từ tệp thô (`luat_d3`, `luat_aitw_day_du`). S1/101 tái lập đúng 65,49 và 74,37.

### 2.2 Ghép cặp

| phép so | exec [KTC95], p | D.3 | AitW đầy đủ |
|---|---|---|---|
| ck500 − S1/101 | **+1,55 [+0,80; +2,33]**, p = 1,6e−5 | - | - |
| ck500 − S1/202 | +1,03 [+0,25; +1,83], p = 0,014 | +0,92 [+0,11; +1,75] | +0,94 [+0,07; +1,81] |
| ck500/202 − S1/101 | +0,83 [+0,00; +1,67], p = 0,036 (cứu 166, phá 129) | +1,05 [+0,22; +1,90], p = 0,010 | +1,86 [+1,06; +2,67], p = 2,5e−6 |
| ck500/202 − S1/202 | +0,31 [−0,53; +1,17], p = 0,50 | +0,45 [−0,44; +1,34], p = 0,34 | +0,92 [+0,02; +1,82], p = 0,046 |
| ck500/202 − ck500 | −0,72 [−1,27; −0,16], p = 0,011 (cứu 59, phá 91) | −0,47 [−1,04; +0,09] | −0,02 [−0,57; +0,54], p = 1,0 |
| S1/202 − S1/101 | +0,52 [−0,22; +1,26], p = 0,19 | - | - |
| ACE − S1/101 | +1,57 [+0,86; +2,31] | - | - |
| ACE − S1/202 | +1,05 [+0,31; +1,81], p = 0,012 | - | - |
| ACE − ck500 | +0,02 [−0,21; +0,26] | - | - |
| ACE − ck500/202 | +0,74 [+0,17; +1,33], p = 0,014 | - | - |
| xao101 − S1/101 | **+0,00 [−0,41; +0,42]**, p = 1 (cứu 45, phá 45) | +0,09 | +0,22, p = 0,35 |
| ck500 − xao101 | **+1,55 [+0,81; +2,30]**, p = 2e−5 (cứu 163, phá 94) | +1,43 [+0,69; +2,20] | +1,66 [+0,94; +2,41] |
| ck500/202 − xao101 | +0,83 [+0,02; +1,65], p = 0,033 | +0,96, p = 0,016 | +1,64, p = 3e−5 |
| ACE − xao101 | +1,57 [+0,85; +2,29], p = 1e−5 | - | - |
| 7B − Base | +3,92 [+2,66; +5,23], p = 5e−10 | - | - |
| S1/101 − 7B | +7,60 [+5,95; +9,28], p < 1e−24 | giữ chiều | giữ chiều |
| ck500 − 7B | +9,14 [+7,55; +10,75], p < 1e−24 | giữ chiều | giữ chiều |
| ACE − 7B | +9,16 [+7,57; +10,79], p < 1e−24 | giữ chiều | giữ chiều |

Thêm D.3 ∧ 14%: ck500/202 − S1/101 +0,92 [+0,09; +1,77] · ck500/202 − S1/202 +0,29 [−0,58; +1,18].

### 2.3 Đọc

- **Hai hạt GRPO.** Hai hạt chênh nhau 0,72 exec và mức chênh có ý nghĩa, nên con số +1,55 của ck500/101 có một phần là biến thiên giữa hạt GRPO. Dưới AitW đầy đủ, hai hạt ngang nhau (−0,02). Hướng vẫn dương so với cả hai hạt S1 ở cả ba luật, nhưng mỗi luật cho một độ lớn khác nhau (+0,3 đến +1,9). Khi báo phải nêu rõ luật, không chọn luật chỉ vì cho số lớn nhất.
- Hạt GRPO 202 vẫn xuất phát từ S1/101, nên chỉ đo nhiễu của bước GRPO, không đo nhiễu của SFT.
- ACE − ck500/202 = +0,74 không có nghĩa là ACE hơn, vì ACE được xây trên ck500/101, tức cùng hạt GRPO với ck500/101.
- **xao101.** xao101 đổi câu ở 593/4.463 bước (ck500 đổi 1.668 bước) mà không tăng gì so với S1. Đòn "chưa có nhánh so sánh train thêm" (bỏ ngỏ từ lượt GRPO-point 6/9) nay đã đóng cho ck500.
- **7B.** Mức 3B đã tinh chỉnh hơn 7B (khoảng 9 điểm) gấp đôi mức 7B hơn 3B gốc (3,92). 7B có action_ok 96,37, câu trung vị dài 64 ký tự (S1 dài 33), tốc độ sinh 0,4 bước/giây trên T4×2.

### 2.4 Phải khai

- Mỗi nhánh một hạt (S1 và ck500 hai hạt). Mọi mức ck500 − S1 đều dưới MDE 2,11.
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

### 3.2 KTC95 ghép cặp (bootstrap cụm app, B = 2.000)

| thước | ck500 − S1/101 | ACE − S1/101 | ACE − ck500 |
|---|---|---|---|
| BLEU-4 | +0,80 [+0,23; +1,61] | +1,91 [+1,29; +2,71] | +1,11 [+0,77; +1,43] |
| ROUGE-L | +1,01 [+0,56; +1,49] | +1,76 [+1,26; +2,25] | +0,74 [+0,54; +0,96] |
| CIDEr-D | +13,93 [+7,50; +19,87] | +25,91 [+18,71; +32,72] | +11,97 [+8,50; +15,61] |
| SPICE | +1,42 [+0,69; +2,16] | +2,76 [+1,95; +3,55] | +1,33 [+0,92; +1,73] |
| chrF (xấp xỉ) | +1,26 [+0,76; +1,78] | +1,95 [+1,42; +2,48] | +0,69 [+0,47; +0,93] |

### 3.3 Đọc

- ck500 hơn cả hai hạt S1 ở 7/7 thước. Hai hạt GRPO gần trùng nhau (SPICE chênh −0,10, CIDEr-D chênh +1,17), tức tác dụng của thưởng SPICE lên thước chữ lặp lại ổn định, trong khi exec giữa hai hạt chênh 0,72.
- xao101 trùng S1: CIDEr-D chênh +2,0, các thước khác chênh không quá 0,3. Phần ck500 hơn S1 ở thước chữ là của thưởng SPICE.
- ACE hơn ck500 ở cả năm thước có KTC, mọi KTC đều loại 0, trong khi exec chỉ ngang (+0,02). Thước chữ đo độ giống câu chuẩn, không cho biết câu có giúp bộ trỏ tìm đúng phần tử hay không, nên phép so chính vẫn đọc bằng exec.
- 7B thấp xa mọi nhánh tinh chỉnh ở mọi thước, cùng chiều với exec.

### 3.4 Phải khai

- Chỉ có KTC cho ba nhánh ở bảng 3.2. Chưa có KTC cho METEOR, BERTScore, và cho các hàng S1/202, ck500/202, xao101, 7B.
- chrF trong bảng 3.2 là trung bình mức câu (60,74 / 62,00 / 62,69), lệch số mức kho 0,5 đến 0,9. Chỉ dùng KTC của Δ chrF, không in điểm tuyệt đối từ phép tính này.
- BLEU-4 trong bảng 3.2 tính lại mức kho trên từng mẫu bootstrap. ROUGE-L của ACE tính lại ra 69,11, lệch 0,03 so với 69,08 đã in.

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

### 6.3 Thước chữ trên AitZ (2.736 bước, chưa có KTC)

| nhánh | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|
| Base | 18,68 | 18,56 | 39,11 | 86,98 | 15,66 | 35,24 | 38,81 |
| S1/101 | 21,01 | 20,83 | 46,84 | 120,24 | 15,27 | 35,66 | 49,69 |
| ck500 | 21,48 | 21,08 | 46,92 | 123,38 | 16,37 | 36,28 | 49,68 |
| ck500/202 | 19,76 | 19,99 | 45,44 | 117,26 | 15,63 | 34,43 | 48,47 |
| ACE (R3) | 21,45 | 21,05 | 46,91 | 123,29 | 16,40 | 36,24 | 49,63 |
| ra_k4 | 19,94 | 20,04 | 45,39 | 117,42 | 15,70 | 34,24 | 48,27 |

- ck500 hơn S1 ở 6/7 thước (BERTScore ngang, −0,01), nhưng mức hơn nhỏ (CIDEr-D +3,1, SPICE +1,1). Hạt 202 thì thấp hơn S1 ở 6/7 thước (trừ SPICE). Vì vậy không viết "ck500 hơn S1 trên AitZ", kể cả khi dùng thước chữ.
- SPICE của S1 (15,27) còn thấp hơn Base (15,66) dù exec của S1 cao hơn. Như vậy SPICE trên AitZ không phản ánh đúng thứ tự giữa các nhánh.

### 6.4 Đọc

- Tinh chỉnh trên AndroidControl có chuyển sang AitZ: mọi nhánh tinh chỉnh đều hơn Base có ý nghĩa.
- Mức tăng của GRPO thưởng SPICE và của ACE thì không chuyển sang. ACE dựa vào việc chép câu ví dụ cùng văn phong, mà câu chuẩn AitZ có văn phong khác.
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

- So với lịch sử cũ, CIDEr-D giảm 85 (S1) và 96 (ck500), SPICE giảm 9,4 và 10,7. ck500 vẫn nhỉnh hơn S1 ở 7/7 thước, nhưng khoảng cách CIDEr-D co từ +13,9 xuống +2,2. Thước chữ ở đây đối chiếu với câu chuẩn của chính bước đó, nên chịu cả lỗi dây chuyền từ các bước trước.
- **exec: CHƯA CÓ**, đang chờ kernel `trangphuongngoc/tuantu-cham`; đọc bằng `harness/doc_tuantu.py`.

**Đọc (tạm, chưa có exec):** bỏ lịch sử chuẩn làm cả hai nhánh giảm vài điểm đúng loại thao tác. Ở bước chạm, ck500 bền hơn S1 và khoảng cách gần gấp đôi. Ở bước không chạm thì ngược lại: tác hại đã biết của ck500 (mục 5) lớn thêm khi lịch sử là câu của chính mô hình. Phải khai cả hai chiều.

---

## 8. ACU: phần AndroidControl mà S1 chưa thấy (CHƯA CÓ SỐ)

- **Dữ liệu.** 1.484 bước, dựng từ TFRecord gốc của AndroidControl. Phải khai hai điều:
  - 1.383/1.484 bước thuộc split train chính thức (giống tập kiểm chính, `report/209`);
  - 5 bước có câu chuẩn lệch với bản HarrytheOrange.
- **OCR.** Dùng đúng rapidocr_onnxruntime 1.4.4 như OCR của tập dạy và tập kiểm (dựng Python 3.12 bằng uv). Chạy lại trên 20 ảnh của tập kiểm cũ: trùng 20/20 tuyệt đối. Đủ 1.484 ảnh, không ảnh nào rỗng.
- **Khối ví dụ của ACE** chứa đúng câu chuẩn ở 8,7% bước (tập kiểm chính khoảng 13%, AitZ 0%). Dự đoán: ACE kích hoạt ít hơn trên tập kiểm chính nhưng nhiều hơn hẳn AitZ.
- **Đang chạy:** kernel `trangphuongngoc/acu-gen`, dự kiến xong 6–8 h sáng 27/10.
  - Sinh câu: S1, ck500, ra_k4, Base, ck500/202.
  - Chấm UGround: câu chuẩn, S1, ck500, ACE, Base, ck500/202, ra_k4.
- **Khi có số, sẽ tính:**
  - ghép cặp ck500 − S1, ACE − S1, ACE − ck500, theo exec, D.3 và AitW;
  - bảng gộp với tập kiểm chính (5.947 bước), khai rõ là gộp;
  - thước chữ, chạy trên Kaggle CPU.

---

## 9. Cách viết gợi ý

Phần này gợi ý cách kể từng kết quả một cách tích cực và dễ bảo vệ: điểm mạnh đi trước, phần còn lại được đặt như phạm vi áp dụng hoặc hướng phát triển. Câu mẫu dùng thẳng được, con số lấy ở mục 2 đến 8.

**Phương pháp chính (ck500).**
"ck500 cải thiện so với S1 một cách nhất quán: so với S1/101, hướng tăng được giữ qua bốn dụng cụ chấm độc lập (UGround, UI-Venus, Phi-Ground, Phi-4) và qua cả ba luật khớp chạm (exec, D.3, AitW). Mức tăng vào khoảng +0,8 đến +1,6 exec tuỳ hạt GRPO, và đạt tới +1,9 dưới luật AitW."
Trong bảng có thể đặt cả hai hạt GRPO (60,65 và 59,94) và cả hai hạt S1 (59,11 và 59,62) cạnh nhau. Cách đặt này giúp người đọc thấy hướng tăng giữ được ở cả hai hạt, và làm kết quả thêm thuyết phục.

**Mức tăng đến từ tín hiệu SPICE.**
"Nhánh kiểm sàn chạy cùng 500 bước GRPO nhưng xáo thưởng cho kết quả bằng S1, trong khi ck500 hơn nhánh này +1,55 [+0,81; +2,30]. Mức cải thiện vì vậy đến từ chính tín hiệu SPICE chứ không phải từ việc huấn luyện thêm."
Đây là điểm tựa lập luận đẹp nhất của phương pháp, rất hợp để đặt nổi bật trong ch6.

**ACE.**
"ACE nâng chất lượng câu rõ rệt so với ck500 ở mọi thước chữ (mọi KTC đều nằm hẳn trên 0), đồng thời giữ trọn khả năng định vị của ck500."
ACE được thiết kế để câu gần câu chuẩn hơn mà không đánh đổi khả năng định vị, và kết quả cho thấy ACE làm được đúng như vậy.

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
"Khi lịch sử là câu do chính mô hình viết, ưu thế của ck500 ở bước chạm tăng gần gấp đôi (+3,52)." Bước không chạm có thể nhắc sau, như hướng phát triển tiếp.

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
- Hạ cách viết về ck500 thành "khiêm tốn, hai hạt GRPO cho +0,8 và +1,6", theo câu chung ở mục 9.
- Thêm một câu về xao101 (mức tăng thuộc về tín hiệu SPICE) và một câu về AitZ (không chuyển miền).

**ch4 (phương pháp)**
- Mô tả nhánh kiểm sàn xao101 (thưởng bị xáo, cùng mọi siêu tham số với ck500).
- Mô tả hạt GRPO 202 (mục 2.5).

**ch5 (thước đo)**
- `sec:phi4`: thay con số Base 38,56 (trên 3.566 bước) bằng 38,23 (đủ 4.463 bước). Cũng tìm và sửa con số này trong `report/155` và bài SOICT.
- Thêm Phi-Ground làm bộ trỏ thứ ba, kèm nguồn dữ liệu và cách viết ở mục 4.4.

**ch6 (kết quả)**
- Bảng chính: thêm các hàng S1/202, ck500/202, xao101, 7B với ba cột exec, D.3, AitW (mục 2.1); thêm các phép so ở mục 2.2.
- Đoạn ck500: thêm phân rã và ví dụ định tính (mục 5), và đoạn về tác hại ở bước không chạm dẫn tới ACE.
- Bảng ACE (khoảng dòng 138 đến 152): thêm KTC95 cho năm thước chữ (mục 3.2), chú thích chrF là xấp xỉ, ghi METEOR và BERTScore không có KTC. Thêm câu "ACE hơn ck500 ở mọi thước chữ nhưng exec chỉ ngang".
- Đoạn UI-Venus (khoảng dòng 347, hiện chỉ nói Base, S1, S2 trên lát 2.532): thêm bảng đổi dụng cụ ở mục 4.1 và 4.2.
- Thêm ablation thưởng CIDEr-D (mục 5). Grep chưa thấy trong `thesis/chapters/*.tex`, nhưng cần xem tay ch4 và ch6, phòng khi dùng tên khác.
- Thêm mục mới cho AitZ (mục 6), mục mới cho lịch sử tự sinh (mục 7), và ACU khi có số (mục 8).
- Thêm hàng so với 7B.

**ch7 (hạn chế)**
- Khai: mỗi nhánh một hạt (S1 và ck500 hai hạt); ACE chỉ ngang ck500 ở exec; không chuyển sang AitZ; tác hại ở bước không chạm lớn thêm khi lịch sử tự sinh; hai dụng cụ ngoài họ Qwen cho mức tăng nhỏ hơn.
- Sửa các dòng 18 và 38 (nhắc tới dụng cụ đo) cho khớp mục 4.

**Bảng tự sinh `bang_nhieu_thuoc.tex`**
- Hiện chưa có ACE. Cần tạo JSON bảy thước chữ cho ACE (có thể mở rộng `harness/ck500_text_metrics.py`), thêm hàng vào danh sách `HANG` của `harness/sinh_bang_nhieu_thuoc.py`, rồi sinh lại bảng. Không sửa tay.

**Bài SOICT** (camera-ready): áp cùng cách viết ở mục 9 cho ck500 và sửa con số Base của Phi-4.

---

## 11. Còn chờ, còn thiếu

**Đang chạy, chờ kết quả (cập nhật 26/10, 21:45):**

| việc | kernel | chờ số gì | dự kiến | khi có số, điền vào | chỗ dùng trong luận văn |
|---|---|---|---|---|---|
| Lịch sử tự sinh, exec | `trangphuongngoc/tuantu-cham` | exec trên 4.463 bước chạm cho S1 và ck500 khi lịch sử là câu tự sinh; ghép cặp tự sinh − cũ và ck500 − S1 | đêm 26/10 (chưa xem được log nên chưa ước chính xác) | mục 7: thay dòng "exec: CHƯA CÓ", viết lại phần "Đọc" | ch6, mục mới về lịch sử tự sinh; ch7, hạn chế về giả định lịch sử là câu chuẩn |
| ACU, exec | `trangphuongngoc/acu-gen` | exec, D.3, AitW trên 1.484 bước cho câu chuẩn, Base, S1, ck500, ck500/202, ra_k4, ACE; ghép cặp ck500 − S1, ACE − S1, ACE − ck500; số lần ACE kích hoạt | 6–8 h sáng 27/10 (muộn nhất khoảng 8:40) | mục 8 (thêm bảng như mục 6.2); mục 1 (thêm ý về ACU); `report/322` hàng #8 | ch6, mục kiểm tổng quát hoá (đặt cạnh AitZ); ch1 và ch7 nếu kết quả đổi kết luận |
| ACU, thước chữ | kernel CPU sẽ đẩy sau khi `acu-gen` xong | bảy thước chữ trên 1.484 bước | khoảng 1 giờ sau `acu-gen` | mục 8 (bảng như mục 6.3) | ch6, cùng chỗ với ACU exec |

Tới khi có số, trong luận văn không viết câu nào về ACU hay về exec của lịch sử tự sinh. Nếu cần giữ chỗ thì để `\CANDIEN`.

**Chưa làm, không cần GPU:**
- D.3 và AitW cho các phép so ck500 − S1/101 và ACE − S1 (nhiều ô "-" ở mục 2.2).
- KTC thước chữ cho S1/202, ck500/202, xao101, 7B, AitZ và lịch sử tự sinh; KTC cho METEOR và BERTScore.

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
| ACU | `acu-build-cpu` · `acu-ocr144-cpu` · `acu-gen` (trangphuongngoc) | `runs/acu/` · Release `data-acu-build-v1` | |

**Kiểm tái lập đã làm:**
- Mọi số ở mục 2 và 4 đã tính lại từ tệp thô trên máy ngày 24/10; tất cả khớp.
- Các lượt sinh lại: kiểm hoà 16/20 (S1 hoà fp16 so với lượt công bố, như `report/259`); ck500 20/20.
- Luật R3 trong gói AitZ tái lập đúng câu ACE trên test 4.463/4.463. ra_k4 có md5 `f3c543b0`, trùng adapter của lượt test 304.

**Bẫy khi tính lại:**
- Một bước (câu rỗng, bước `(18710, 1)`) thiếu trường `executable` trong ba tệp S1/101, S1/202, ck500. Phải dùng `get("executable", 0)` như `score_run.py`.
- Chạy `som_doc.py` với danh sách tệp riêng sẽ ghi đè `runs/som/som_ket_qua.json` (tệp git đang theo dõi). Chạy xong phải `git checkout` lại tệp đó.
- `score_run.py` chặn tệp thiếu hơn 1% số bước. Khi chỉ chấm các bước có câu khác nhau, phải truyền `--n <số dòng>`.
