# 320 — Những chỗ cần cập nhật trong luận văn (ghi 23/10/2026)

Chỉ là ghi chú. Chưa sửa tệp nào trong `thesis/`. Mỗi mục ghi rõ đã kiểm hay chưa kiểm.

## A. Kết quả mới chưa có trong luận văn

**A1. ck500 / R3 dưới UI-Venus-Ground-7B (4.463 bước, bootstrap cụm theo app).**
Số test, một hạt giống. Đọc bằng `python3 -I harness/venus_ck_doc.py`.

| nhánh | exec |
|---|---|
| S1/101 | 54,51 |
| ck500 | 56,06 |
| R3 | 56,20 |

- ck500 − S1/101: +1,55 [+0,82; +2,30], b=153 c=84, p=8,7e−6 (trùng +1,55 đo bằng UGround).
- R3 − S1/101: +1,68 [+0,97; +2,42], p=1,4e−6.
- R3 − ck500: +0,13 [−0,11; +0,39], p=0,38.
- Chỗ cần sửa: ch6 dòng 347 hiện chỉ nói UI-Venus cho Base, S1, S2 trên lát 2.532 bước (phép B). Cần thêm đoạn nói phương pháp đề xuất (ck500, ACE) cũng giữ thứ tự dưới UI-Venus. Đã kiểm: dòng 347 chưa nhắc ck500 hay R3.

**A2. ck500 / R3 dưới Phi-4 người nghe trắc nghiệm (4.463 bước).**
- S1/101 44,63 [42,88; 46,37] · ck500 45,33 [43,59; 47,11] · R3 45,33 [43,57; 47,12].
- ck500 − S1 +0,69 (b=90 c=121, p=0,039); R3 − S1 +0,69 (p=0,043); ck500 − R3 0,00 (p=0,85 theo `som_doc.py`; p=1 theo McNemar chính xác trong `som_s1_202_doc.py`, hai script dùng kiểm định khác nhau, chọn một và ghi tên).
- Mức tăng nhỏ, p sát 0,05: không viết là kết luận chắc chắn.
- Chưa kiểm: luận văn đã có mục người nghe Phi-4 ở ch5 (`sec:phi4`), cần xem bảng kết quả ở ch6 có chỗ thêm hai hàng này không.

**A3. Câu kết luận nên dùng (và câu cấm).**
- Nên: ck500 hơn S1/101 qua ba dụng cụ độc lập (UGround, UI-Venus, Phi-4), mức tăng khiêm tốn (khoảng +1,5 exec, dưới MDE 2,11), một hạt giống. **Sửa 23/10 tối (mục B):** so với S1/202 thì chỉ còn hơn dưới UI-Venus (+0,94); dưới Phi-4 là −0,20, không có ý nghĩa. Không viết "ổn định qua ba dụng cụ" mà không kèm hạt 202.
- Nên: R3 (ACE) chỉ ngang ck500 về exec, không hơn.
- Cấm: "kết luận chắc chắn"; "đã đóng đòn cùng họ Qwen" (UI-Venus vẫn dựng trên họ Qwen, Phi-4 là dụng cụ ngoài họ nhưng là người nghe, không phải bộ trỏ).
- Cập nhật phần giới hạn ở ch7 (dòng 18 và 38 nhắc tới dụng cụ đo) cho khớp.

**A4. Lỗi quy trình đáng ghi một dòng trong phần phương pháp đo (tuỳ chọn).**
Lượt Venus đầu chỉ cho 40 đến 190 cặp bất đồng nên không đủ sức; sau khi chấm đủ cả ba nhánh trên 1.880 bước khác nhau thì Δ có ý nghĩa. Nếu hội đồng hỏi vì sao số lượt chấm không đều, đây là lời giải thích.

## B. Hạt giống 202 của S1 (XONG 23/10 tối, cả hai lượt Kaggle COMPLETE)

Số test, một hạt giống cho ck500/R3, hai hạt cho S1. Đọc bằng `python3 -I harness/venus_s1_202_doc.py` và `python3 -I harness/som_s1_202_doc.py`. Output Venus ở `runs/venus/s1_202_23_10/` (kiểm tái lập 40 bước, toạ độ lệch 0; chấm bù 1.319 câu, 1,5 h). Phi-4 ở `runs/som/chon_phi4_s1_202_diff*.jsonl` (kiểm tái lập S1/101 200 bước, lệch 0).

| nhánh | UI-Venus exec | Phi-4 chọn đúng |
|---|---|---|
| S1/101 | 54,51 | 44,63 |
| S1/202 | 55,12 | 45,53 |
| ck500 | 56,06 | 45,33 |
| R3 | 56,20 | 45,33 |

| phép so | UI-Venus Δ [KTC95], p | Phi-4 Δ [KTC95], p |
|---|---|---|
| ck500 − S1/202 | +0,94 [+0,14; +1,75], p=0,028 | **−0,20 [−0,94; +0,55], p=0,63** |
| R3 − S1/202 | +1,08 [+0,28; +1,88], p=0,012 | **−0,20 [−0,96; +0,57], p=0,64** |
| S1/202 − S1/101 | +0,60 [−0,13; +1,34], p=0,12 | +0,90 [+0,21; +1,61], p=0,010 |
| ck500 − S1/101 | +1,55 [+0,82; +2,30], p=8,7e−6 | +0,69 [+0,02; +1,40], p=0,039 |
| R3 − ck500 | +0,13 [−0,11; +0,39], p=0,38 | 0,00 [−0,24; +0,23], p=1 |

Cách đọc:
- Dưới UI-Venus, ck500 và R3 vẫn hơn S1/202 có ý nghĩa, nhưng mức tăng nhỏ hơn so với S1/101 (+0,94 so với +1,55) vì S1/202 cao hơn S1/101 0,60 điểm.
- Dưới Phi-4, S1/202 (45,53) cao hơn cả ck500 (45,33), nên ck500 − S1/202 = −0,20, không có ý nghĩa. Mức +0,69 so với S1/101 một phần là do hạt S1/101 thấp: S1/202 − S1/101 đã là +0,90, lớn hơn khoảng cách ck500 − S1/101.
- Hệ quả: câu "ck500 hơn S1 ổn định qua ba dụng cụ" chỉ đúng khi so với S1/101. So với hạt 202 thì còn đúng ở UGround (+1,03, xem G1) và UI-Venus; dưới Phi-4 không phân biệt được. Phải sửa A3 theo hướng này.
- Đã tính ở G1 cho UGround exec; còn chưa kiểm D.3/AitW. Cần tính từ `runs/score_s1_seed202_raw.jsonl` và `runs/grpo_spice/score_ck500_test_raw.jsonl` (trước đó, `report/259` chỉ so với S1/101).
- Hạn chế cần khai: S1/202 trên Phi-4 chỉ được chấm ở 1.652 bước câu khác S1/101, các bước còn lại dùng lại kết quả S1/101 (2.810 bước giống nhau).

## C. Phần thiếu đã biết từ trước

**C1. Ablation thưởng CIDEr-D (A2) chưa vào luận văn.**
- Đã chạy và chấm test xong (`report/299_KET_QUA_TEST_A2_CIDER_SO_CK500_8_10.md`, 8/10).
- A2_500 − ck500: exec −0,69 [−1,34; −0,02], p=0,04. Thưởng SPICE cho exec cao hơn CIDEr-D ở cùng 500 bước. A2_1000 − A2_500: +0,02. Cả hai A2 hơn S1/101 khoảng +0,85.
- Phân rã: A2 viết đúng loại thao tác hơn (+10 bước ròng) nhưng chọn sai phần tử nhiều hơn (−41 bước).
- Phải khai kèm: một hạt giống mỗi nhánh; Δ −0,69 chỉ lớn hơn nhiễu giữa hai hạt S1 (0,52) một chút; hai nhánh khác tập câu nhắc (1.000 so với 2.000) và máy train (T4 fp16 so với A100 bf16).
- Đã kiểm bằng grep: các tệp `thesis/chapters/*.tex` không có từ khoá "thưởng CIDEr", "A2_500" hay "CIDEr-D reward". Cần xem tay lại ch4 và ch6 trước khi thêm, phòng khi dùng tên khác.

**C2. Thước chữ của ACE và ck500 chưa có KTC.**
Ghi chú CLAUDE.md nói BLEU-4, METEOR, ROUGE-L, CIDEr-D, SPICE... của ACE chưa có khoảng tin cậy. Bootstrap cụm trên CPU là đủ. Việc này không cần GPU.

**C3. Bảng tự sinh chưa có ACE.**
`thesis/chapters/bang_nhieu_thuoc.tex` có 0 lần nhắc "ACE" (đã kiểm bằng grep). Cần sinh lại bằng `harness/sinh_bang_nhieu_thuoc.py` (không sửa tay), rồi dựng lại `thesis/main.pdf` (xem lệnh dựng trong CLAUDE.md, không dùng `>/dev/null 2>&1`).

## D. Chỗ yếu hội đồng có thể hỏi, chưa có số

- **Nhánh so sánh "train thêm không có thưởng SPICE"** để tách phần do GRPO với phần do học thêm. Chưa kiểm `report/289` và các nhánh 288 (tspicea, v.v.) xem có đóng vai trò này không, nên chưa kết luận là thiếu. Cần kiểm trước khi chạy gì.
- **Hạt giống thứ hai cho ck500.** Mọi kết luận hiện là một hạt giống và mức tăng +1,55 dưới MDE 2,11. Cần train lại GRPO trên Colab, tốn tiền; quyết định là của bạn.
- **Ví dụ định tính và phân rã theo loại thao tác / app** cho ck500 và ACE: vài câu sửa đúng, vài câu làm hỏng. Việc CPU, rẻ.
- **Khai rõ tác hại của ck500** (scroll rớt khoảng −6,2 pp, `report/261`) và nói thẳng đó là lý do có ACE.

## E. Nhắc về văn phong khi cập nhật

Theo `CLAUDE.md`: dùng "chúng tôi", không dùng "luận văn" làm chủ ngữ; không in đậm giữa câu; không dấu gạch dài; không tiêu đề dạng câu hỏi; không tên tệp hay tham số trong thân bài; gọi câu người viết là "câu chuẩn"; "nhánh so sánh" thay "đối chứng".

## F. Bổ sung chiều 23/10 (việc đã làm ở máy, chưa vào luận văn)

**F1. KTC thước chữ cho S1/101, ck500, ACE (đã xong, ghi vào `runs/ktc_thuoc_chu.json`).**
- Script `harness/ktc_thuoc_chu.py`, bootstrap cụm theo app, 2.000 lần, ghép cặp. Có BLEU-4, ROUGE-L, CIDEr-D, SPICE, chrF. Không có METEOR và BERTScore.
- Chỗ cần sửa khi có số: bảng ACE ở ch6 (khoảng dòng 138 đến 152, cột "ACE − câu ban đầu"). Các hàng BLEU-4, METEOR, ROUGE-L, CIDEr-D, SPICE, chrF, BERTScore hiện chỉ có Δ, không có KTC; chỉ ba hàng vị trí có KTC. Thêm KTC cho năm thước có số; METEOR và BERTScore phải ghi chú là không có KTC, hoặc để nguyên.
- Phải khai trong chú thích: chrF là trung bình mức câu (xấp xỉ), BLEU-4 tính lại mức kho trên mẫu bootstrap.
- Cũng cần thêm KTC cho `tab:6.6` (nhóm độ đo so với câu tham chiếu) nếu muốn so ck500 với S1.
- TRẠNG THÁI: XONG (`runs/ktc_thuoc_chu.json`, `runs/ktc_thuoc_chu.log`). Kiểm tái lập: BLEU-4, CIDEr-D, SPICE khớp số đã in tuyệt đối; ROUGE-L của ACE lệch 0,03 (69,11 so với 69,08 đã in). Số, KTC95 bootstrap cụm theo app (1.091 cụm, B = 2.000), ghép cặp:

| thước | ck500 − S1/101 | ACE − S1/101 | ACE − ck500 |
|---|---|---|---|
| BLEU-4 | +0,80 [+0,23; +1,61] | +1,91 [+1,29; +2,71] | +1,11 [+0,77; +1,43] |
| ROUGE-L | +1,01 [+0,56; +1,49] | +1,76 [+1,26; +2,25] | +0,74 [+0,54; +0,96] |
| CIDEr-D | +13,93 [+7,50; +19,87] | +25,91 [+18,71; +32,72] | +11,97 [+8,50; +15,61] |
| SPICE | +1,42 [+0,69; +2,16] | +2,76 [+1,95; +3,55] | +1,33 [+0,92; +1,73] |
| chrF (xấp xỉ) | +1,26 [+0,76; +1,78] | +1,95 [+1,42; +2,48] | +0,69 [+0,47; +0,93] |

- Cả năm thước, mọi KTC đều loại được 0, kể cả ACE − ck500. Đây là điều đáng đưa vào ch6: ACE hơn ck500 rõ ở thước chữ trong khi exec ngang (+0,02 [−0,21; +0,26]).
- Lưu ý chrF: trung bình mức câu cho 60,74 / 62,00 / 62,69, lệch số mức kho đã in (61,26 / 62,87 / 63,44) tới 0,5 đến 0,9. Chỉ dùng KTC của Δ chrF, không in điểm tuyệt đối từ đây; phải khai là xấp xỉ.
- Chưa có KTC cho METEOR và BERTScore (hai hàng này giữ nguyên Δ, ghi chú không có KTC).
- Cách đọc: thước chữ chưa cho biết câu có giúp bộ trỏ tìm đúng phần tử, nên vẫn so sánh chính bằng exec (đúng luật của luận văn).

**F2. Ví dụ định tính và phân rã (đã có, `report/321_VI_DU_DINH_TINH_CK500_ACE.md`).**
- Phân rã ck500 so với S1: câu đổi 1.668 bước (37,4%), cứu 159 (sửa loại thao tác 36), phá 90 (sai loại thao tác 8), ròng +69 = +28 từ loại thao tác và +41 từ đổi phần tử. Khớp `report/259`.
- Chỗ cần sửa: chọn vài ví dụ cứu và phá trong `report/321` để đưa vào ch6 (sau phần ck500) làm ví dụ định tính. Cần xem tay chọn ví dụ có ý nghĩa; 6 ví dụ trong file là rút ngẫu nhiên, chưa chọn lọc.
- Cần thêm một đoạn ngắn nói rõ chiều phá của ck500 (tức scroll/back, `report/261`) và dẫn tới lý do cần ACE.

**F3. Bảng tự sinh chưa có ACE (nhắc lại C3).**
- `harness/sinh_bang_nhieu_thuoc.py` có danh sách `HANG` không có ACE. Cần thêm một hàng ACE vào danh sách đó (các cột vị trí lấy từ `runs/hang_ace.json`, cột chữ cần nguồn mới vì `runs/text_metrics_coco.json` và `runs/text_metrics_them.json` chưa có ACE). Hiện chỉ có BLEU-4 mức câu và ROUGE-L trong `hang_ace.json`; bảy cột chữ mức kho của ACE (BLEU-4 53,47 · METEOR 38,37 · ROUGE-L 69,08 · CIDEr-D 442,02 · SPICE 47,13 · chrF 63,44 · BERTScore 67,73) nằm ở ch6 và `report/304` §5, chưa có tệp JSON máy đọc được.
- Việc cần làm trước khi sinh bảng: tạo JSON cho ACE (có thể mở rộng `harness/ck500_text_metrics.py`), rồi mới thêm hàng, sinh bảng, dựng lại `thesis/main.pdf`.

**F4. Chưa làm, đã cân nhắc:** hạt giống thứ hai cho ck500 và nhánh "train thêm không có thưởng SPICE" (mục D). Đều cần Colab, chưa có quyết định.

**F5. Việc cần sửa trong luận văn rút ra từ hai mục trên (gom một chỗ, chưa sửa `thesis/`).**
- ch6, bảng ACE (khoảng dòng 138 đến 152): thêm KTC95 cho năm thước chữ theo bảng F1; chú thích chrF xấp xỉ, METEOR và BERTScore không có KTC.
- ch6, đoạn ACE: thêm câu nói ACE hơn ck500 ở cả năm thước chữ (mọi KTC loại 0) nhưng exec chỉ ngang (+0,02 [−0,21; +0,26]); giải thích thước chữ chưa cho biết câu có giúp bộ trỏ hay không.
- ch6, đoạn Venus (khoảng dòng 347) và phần người nghe Phi-4: thêm kết quả ck500 và ACE dưới hai dụng cụ độc lập (mục A), viết "ổn định nhưng khiêm tốn, một hạt giống", không viết kết luận chắc chắn; nêu Venus vẫn thuộc họ Qwen.
- ch6, sau phần ck500: thêm ví dụ định tính cứu/phá (F2) và đoạn nói chiều phá ở scroll/back dẫn tới ACE.
- ch7, hạn chế: ghi rõ một hạt giống cho ck500, ACE chỉ ngang ck500 ở exec, chưa có nhánh train thêm không thưởng SPICE.
- Bảng tự sinh `bang_nhieu_thuoc.tex`: thêm hàng ACE sau khi có JSON bảy thước chữ (F3), rồi dựng lại `thesis/main.pdf`.
- Hai lượt Kaggle S1/202 đã xong (mục B): đưa bảng B vào ch6 cạnh bảng S1/101, và sửa mọi câu "ổn định qua ba dụng cụ" theo kết quả Phi-4 (ck500 − S1/202 = −0,20).

## G. Bổ sung 24 đến 25/10 (G1 có số; G4 là hạt giống 202 của ck500, đã có điểm UGround 59,94)

G1. UGround, S1/202 (số test, một hạt, tính trong terminal từ tệp thô, chưa vào bảng nào của luận văn).
exec: S1/101 59,11 · S1/202 59,62 · ck500 60,65 · R3 60,68. ck500−S1/202 +1,03 [+0,25; +1,83] p=0,014;
R3−S1/202 +1,05 [+0,31; +1,81] p=0,012; S1/202−S1/101 +0,52 [−0,22; +1,26] p=0,19.
Cần làm: thêm hàng S1/202 vào bảng dụng cụ độc lập (cùng chỗ với mục B), và sửa câu "ck500 hơn S1" thành so với cả hai hạt.

G2. Phi-4 Base 897 bước còn thiếu: lượt 1 và 2 lỗi (thiếu `som_build`; assert độ dài câu), lượt 3 lỗi
`KeyError` vì listener duyệt cả 4.463 bước; đã vá và đẩy lượt 4. Khi xong, ghép với `chon_phi4_base.jsonl`
(3.566) để có đủ 4.463 rồi tính Base so với S1/ck500 dưới Phi-4. XONG 24/10, xem G5.

G3. Phi-Ground (dụng cụ ngoài họ Qwen). Chưa có điểm nào. Bốn lượt lỗi liên tiếp: flag `--grounder`,
`DynamicCache.seen_tokens` trên transformers 5.x, rồi `ModuleNotFoundError transformers_modules.microsoft.Phi-3`
(tên repo có dấu chấm). Lượt 4 tải bản cục bộ tên không có dấu chấm. Chưa kiểm: dữ liệu huấn luyện Phi-Ground có AndroidControl không.
Luận văn: KHÔNG viết "đã đóng đòn cùng họ Qwen" cho tới khi có số Phi-Ground và kiểm xong nguồn dữ liệu.

G4. Hạt giống thứ hai của chính ck500 (GRPO seed 202), điểm xuất phát vẫn S1/101.
Huấn luyện xong 24/10 trên Colab L4, 500 bước, thưởng SPICE, G=8, lr 1e-5, β=0,04, `--seed 202`, xuất phát S1/101. Lịch sử chạy: đứt máy một lần giữa chừng (chạy tiếp từ điểm lưu 200, ghi theo phiên làm việc trước, log đó không còn để kiểm lại); Drive đầy nên điểm lưu 500 không ghi được lần đầu, máy bị ngắt, chạy tiếp từ điểm lưu 425 và chạy 75 bước cuối trong 108,9 phút (87,1 s/bước, VRAM đỉnh 11,80 GiB). Lượt gốc cũng được ghép từ nhiều đoạn và thiếu log bước 251–425, còn `log_history.json` của hạt 202 có đủ 500 bước (đã đếm: 500 dòng, bước 1 đến 500, không trùng).
Adapter: `_bundles/grpo-spice-ck500-s202/grpo_spice/checkpoint-500/adapter_model.safetensors`, md5 `57e5d2eec23278b0a2dfe7393d9fc463`, 59.941.192 byte (cùng cỡ adapter ck500 gốc). Đã kiểm lần chạy tiếp từ 425: log có `[tiếp từ] …/checkpoint-425` và `[nạp default] 504 tensor · |lora_B| 0.0000 → 9.5837 · khoá lạ 0`.
Số đo từ `log_history.json` (đọc 24/10), trung bình theo cửa sổ:
| cửa sổ bước | hạt 202: kl TB | hạt 202: thưởng TB | ck500 gốc: kl TB |
|---|---|---|---|
| 200–250 | 0,0085 | 0,525 | 0,0119 |
| 426–500 | 0,0492 (từng bước 0,0001 đến 0,2987) | 0,527 | 0,0301 (từng bước tối đa 0,1485) |
Hạt 202 có kl ở 75 bước cuối cao hơn lượt gốc khoảng 1,6 lần, và đoạn 486–500 cao nhất (TB 0,074). Không giống dấu hiệu bị reset (khi reset kl về ~0,001); chỉ cho thấy chính sách ở hạt này rời S1 xa hơn một chút. Thưởng TB cuối ngang lượt gốc (0,527 so với khoảng 0,51 đến 0,55). Đoạn 251–425 của lượt gốc không có log nên không so được.
KẾT QUẢ TEST (XONG 25/10 sáng, UGround, số test, 4.463 bước, 1.091 cụm app). Kernel `trangphngngc/ck500-s202-test`, đầu ra ở `runs/grpo_spice/s202_24_10/` (tệp thô `score_ck500_s202_test_raw.jsonl` giải từ zip). Đã kiểm: đủ 4.463 câu (1 câu rỗng), adapter gắn từ `checkpoint-500` của bộ s202, kiểm hoà 16/20 đạt, dòng `[dữ liệu]` ghi 4.463 bước, thiếu OCR 0, thiếu ảnh 0.
exec: S1/101 59,11 · S1/202 59,62 · ck500/202 **59,94** [58,13; 61,71] · ck500/101 60,65 · R3 60,68.
Ghép cặp (bootstrap cụm app, p McNemar chính xác):
· ck500/202 − S1/101 +0,83 [+0,00; +1,67], cứu 166 phá 129, p=0,036 (cận dưới sát 0)
· ck500/202 − S1/202 +0,31 [−0,53; +1,17], cứu 194 phá 180, p=0,50
· ck500/202 − ck500/101 −0,72 [−1,27; −0,16], cứu 59 phá 91, p=0,011
· ck500/202 − R3 −0,74 [−1,33; −0,17], p=0,014
· đối chiếu: ck500/101 − S1/202 +1,03 [+0,25; +1,83] p=0,014; ck500/101 − S1/101 +1,55 [+0,80; +2,33].
Cách đọc: hạt GRPO thứ hai chỉ hơn S1/101 +0,83 (KTC chạm 0) và ngang S1/202. Mức +1,55 của ck500/101 một phần là biến thiên giữa hạt GRPO (hai hạt GRPO chênh nhau 0,72, có ý nghĩa). Hướng vẫn dương so với cả hai hạt S1 nhưng độ lớn dao động +0,3 đến +1,6, dưới MDE 2,11. Đây là hạt GRPO thứ hai trên cùng S1/101, nên chỉ đo nhiễu của bước GRPO, không đo nhiễu của SFT.
Cách viết (theo nhánh "không"): ở ch6, ch7, tóm tắt và bài SOICT, hạ cách viết về ck500 thành "một hạt giống, chưa lặp lại ổn định": báo cả hai hạt GRPO (60,65 và 59,94) và cả hai hạt S1 (59,11 và 59,62) trong bảng; không giữ +1,55 làm con số tiêu đề mà không kèm +0,83; không viết "mức tăng lặp lại qua hai hạt GRPO"; không viết "kết luận chắc chắn". Cũng cần nhắc: R3 (xây trên ck500/101) hơn ck500/202 −0,74 không đồng nghĩa ACE hơn, vì R3 cùng hạt GRPO với ck500/101.
D.3 và AitW cho ck500/202 (XONG 25/10, tính trên máy từ tệp thô bằng `luat_d3` và `luat_aitw_day_du`, cùng 4.463 bước; số S1/101 tái lập 65,49 và AitW đầy đủ 74,37; không ghi đè `runs/luat_d3.json`):
| luật | S1/101 | S1/202 | ck500/101 | ck500/202 | R3 |
|---|---|---|---|---|---|
| D.3 | 65,49 | 66,10 | 67,02 | 66,55 | 67,11 |
| D.3 ∧ 14% | 61,73 | 62,36 | 63,25 | 62,65 | 63,28 |
| AitW (vế khoảng cách) | 66,91 | 67,62 | 68,59 | 68,25 | 68,63 |
| AitW đầy đủ | 74,37 | 75,31 | 76,25 | 76,23 | 76,32 |
Ghép cặp ck500/202 − S1/101: D.3 +1,05 [+0,22; +1,90] p=0,010 · D.3∧14% +0,92 [+0,09; +1,77] · AitW đầy đủ +1,86 [+1,06; +2,67] p=2,5e−6.
ck500/202 − S1/202: D.3 +0,45 [−0,44; +1,34] p=0,34 · D.3∧14% +0,29 [−0,58; +1,18] · AitW đầy đủ +0,92 [+0,02; +1,82] p=0,046.
ck500/202 − ck500/101: D.3 −0,47 [−1,04; +0,09] · AitW đầy đủ −0,02 [−0,57; +0,54] p=1,0 (hai hạt GRPO ngang nhau dưới AitW).
Đối chiếu ck500/101 − S1/202: D.3 +0,92 [+0,11; +1,75] · AitW đầy đủ +0,94 [+0,07; +1,81].
Đọc: dưới D.3 và AitW, hạt GRPO thứ hai hơn S1/101 rõ hơn dưới exec (+1,05 và +1,86 so với +0,83), và hai hạt GRPO không còn khác nhau có ý nghĩa; nhưng so với S1/202 thì vẫn không có ý nghĩa dưới D.3 (+0,45), chỉ sát ngưỡng dưới AitW (+0,92, cận dưới +0,02). Kết luận về hướng không đổi: GRPO ≥ S1 ở cả hai hạt, độ lớn khoảng +0,3 đến +1,9 tuỳ luật, dưới MDE 2,11 của exec. Ba luật khác nhau cho ba độ lớn, nên khi báo phải nêu rõ luật và không chọn luật chỉ vì cho số lớn nhất.
Thước chữ cho ck500/202 (BLEU-4, METEOR, ROUGE-L, CIDEr-D, SPICE, chrF, BERTScore): đang chạy kernel CPU `trangphngngc/ck500-s202-chu-cpu`, kết quả về `runs/text_metrics_s202.json`; chưa có số.
Chưa làm: Phi-4 và Venus cho ck500/202 (~5 h, tài khoản uyenle), user quyết tạm không chạy 25/10.

G5. Phi-4, Base đủ 4.463 bước (XONG 24/10, số test, một hạt giống mỗi nhánh).
Ghép `runs/som/chon_phi4_base.jsonl` (3.566 bước) với 897 bước mới từ `runs/som/base_rest_24_10/som/` thành `runs/som/base_rest_24_10/chon_phi4_base_du_4463.jsonl` (không trùng bước, tập bước khớp S1/101; kiểm tái lập 200 bước lệch 0). Đọc bằng `python3 -I harness/som_doc.py` trên năm tệp (Base đủ, S1/101, ck500, R3, câu chuẩn). Lưu ý: chạy `som_doc.py` với danh sách tệp riêng sẽ ghi đè `runs/som/som_ket_qua.json` (tệp đang được git theo dõi) bằng bản thiếu, phải `git checkout` lại.
Chọn đúng (KTC95 bằng bootstrap cụm app): Base 38,23 [36,53; 39,93] · S1/101 44,63 · ck500 45,33 · R3 45,33 · câu chuẩn 54,94.
Ghép cặp McNemar: Base − S1/101 −6,41 (p=3,1e−22) · Base − ck500 −7,10 (p=1,2e−26) · Base − R3 −7,10 (p=2,7e−26) · Base − câu chuẩn −16,72 (p=1,5e−110).
Cần làm: (a) thêm hàng Base vào bảng người nghe Phi-4 ở ch6 và thay con số cũ 38,56 trên 3.566 bước (nếu có chỗ nào còn in số đó, kể cả `report/155` và bài SOICT); (b) thêm một câu: dưới người nghe ngoài họ Qwen, S1 − Base là +6,41, lớn hơn nhiều mức ck500 − S1, nên thứ tự Base < S1 < ck500 = R3 < câu chuẩn khớp với UGround và Venus; (c) cột "chọn đúng" của Base khác con số 38,56 trước đây vì mẫu số nay đủ.

G6. Việc đang chạy trên Kaggle (24/10 chiều, chưa có số; điền khi về).
- ck500 hạt 202, chấm test bằng UGround: `trangphngngc/ck500-s202-test` XONG (COMPLETE), exec 59,94; xem G4.
- Run B (GRPO thưởng xáo trộn, `xao101`, T4, nhiều đoạn 11 giờ): `uyenle0712/xao101-1`; dự kiến cần khoảng 22 giờ tổng [suy từ tốc độ T4 cũ, chưa đo]. Chỉ là nhánh kiểm sàn; nếu xong, chấm test rồi mới đưa vào luận văn. Nếu bị bỏ thì không cần ghi gì.
- Phi-Ground (`phiground-probe`, lượt thứ 4): chưa có điểm; xem G3. Vẫn cấm viết "đã đóng đòn cùng họ Qwen".

G7. Đã kiểm chéo lại 24/10 (tính lại từ tệp thô trên máy, không chép từ ghi chú cũ).
- Mục A1/B (UI-Venus): chạy lại `venus_ck_doc.py` và `venus_s1_202_doc.py`; mọi số trong A1 và bảng B khớp: S1/101 54,51 · S1/202 55,12 · ck500 56,06 · R3 56,20; ck500−S1/202 +0,94 [+0,14; +1,75] p=0,028; R3−S1/202 +1,08 [+0,28; +1,88] p=0,012; S1/202−S1/101 +0,60 [−0,13; +1,34] p=0,12; ck500−S1/101 +1,55 [+0,82; +2,30] p=8,7e−6; R3−S1/101 +1,68 [+0,97; +2,42] p=1,4e−6; R3−ck500 +0,13 [−0,11; +0,39] p=0,38. Số bước 4.463, 1.880 bước có câu khác nhau giữa ba nhánh (S1/101, ck500, R3) và 2.537 khi thêm S1/202.
- Mục A2/B (Phi-4): chạy lại `som_s1_202_doc.py`; khớp S1/202 45,53; ck500−S1/202 −0,20 [−0,94; +0,55] p=0,63; R3−S1/202 −0,20 [−0,96; +0,57] p=0,64; S1/202−S1/101 +0,90 [+0,21; +1,61] p=0,010; ck500−S1/101 +0,69 [+0,02; +1,40] p=0,039.
- G1 (UGround): tính lại bằng `score_run.cluster_bootstrap` (1.091 cụm app) từ `runs/score_s1_seed101_raw.jsonl`, `score_s1_seed202_raw.jsonl`, `grpo_spice/score_ck500_test_raw.jsonl`, `ra304_luat/score_R3_test_raw.jsonl`: khớp mọi số (59,11 · 59,62 · 60,65 · 60,68; ck500−S1/202 +1,03 [+0,25; +1,83] p=0,014; R3−S1/202 +1,05 [+0,31; +1,81] p=0,012; S1/202−S1/101 +0,52 [−0,22; +1,26] p=0,19). Cũng ra ck500−S1/101 +1,55 [+0,80; +2,33] và R3−ck500 +0,02 [−0,21; +0,26], trùng F1. Lưu ý: 1 bước trong ba tệp (S1/101, S1/202, ck500) thiếu trường `executable` (bước câu rỗng); phải dùng `get("executable", 0)` như `score_run.py`, nếu không sẽ báo lỗi.
- G5 (Phi-4 Base): số lấy từ chính lượt chạy `som_doc.py` hôm 24/10; tập bước 3.566 + 897 = 4.463, giao rỗng, bằng tập bước của S1/101.
- G4: kl và thưởng tính từ `log_history.json`; md5 adapter tính lại trên tệp đã giải nén. Điểm test ck500/202 tính lại ngoài kernel bằng `score_run.cluster_bootstrap` từ tệp thô trên máy: 4.463 bước chung với bốn nhánh còn lại; các số của S1/101, S1/202, ck500/101, R3 khớp G1.
- Chưa kiểm, cần xem trước khi dùng: (a) lịch sử đứt máy ở điểm lưu 200 (không còn log); (b) mọi giờ dự kiến trong G6 (suy từ tốc độ cũ); (c) D.3 và AitW cho S1/202 và ck500/202.
