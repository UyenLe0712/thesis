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
Thước chữ cho ck500/202 (XONG 25/10, kernel CPU `trangphngngc/ck500-s202-chu-cpu` v5, mức kho, `runs/text_metrics_s202.json`). Kiểm tái lập: ck500/101 khớp tuyệt đối bảy số đã in (52,36 · 37,92 · 68,36 · 430,05 · 45,79 · 62,87 · 67,07).
| thước | S1/101 | S1/202 | ck500/101 | ck500/202 |
|---|---|---|---|---|
| BLEU-4 | 51,56 | 51,66 | 52,36 | 52,94 |
| METEOR | 36,79 | 37,17 | 37,92 | 37,53 |
| ROUGE-L | 67,35 | 67,71 | 68,36 | 68,48 |
| CIDEr-D | 416,12 | 419,19 | 430,05 | 431,22 |
| SPICE | 44,37 | 44,23 | 45,79 | 45,69 |
| chrF | 61,26 | 61,92 | 62,87 | 62,37 |
| BERTScore | 66,33 | 66,75 | 67,07 | 67,12 |
Đọc: hạt GRPO thứ hai hơn cả hai hạt S1 ở cả bảy thước chữ (so S1/202: SPICE +1,46, CIDEr-D +12,03), và gần như trùng hạt thứ nhất (SPICE −0,10, CIDEr-D +1,17). Tức là phần thưởng SPICE lặp lại ổn định ở thước chữ, trong khi exec giữa hai hạt chênh 0,72. Chưa có KTC (mức kho, một lần tính). Cột S1/202 đã đối chiếu khớp `runs/text_metrics_coco.json` và Bảng 6.6 của luận văn.
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

G8. Trạng thái Kaggle 25/10 trưa (kiểm bằng CLI lúc 12:29 giờ VN; điền số khi về).
- `uyenle0712/xao101-1` COMPLETE (đầu ra ở `runs/xao101/c1b`); `uyenle0712/xao101-2` đang chạy từ khoảng 06:53 sáng 25/10, cắt ở 11 giờ. Commit 3 chưa đẩy. uyenle còn 11,86 h GPU tới 31/10, sau commit 2 sẽ không đủ cho commit 3. Chưa có số, chưa vào luận văn (xem G6).
- `trangphngngc/ck500-s202-chu-cpu` COMPLETE, số đã ghi ở G4 (bảng thước chữ).
- `trangphngngc/phiground-bc` (Phi-Ground, dụng cụ ngoài họ Qwen) COMPLETE nhưng chỉ ra một nửa. Đầu ra ở `runs/phiground/bc_25_10/`.
  · Base: exec 40,87 (hit_disk 49,24) trên 4.456 bước chạm, 1.091 cụm. Lưu ý: tệp dự đoán Base trong dataset `phiground-ck` thiếu 7/4.463 bước (score_run có in cảnh báo nhưng vì dưới 1% nên vẫn chấm). Đối chiếu dưới UGround Base là 47,59. Chưa có KTC, chưa có nhánh nào khác để ghép cặp.
  · ck500: KHÔNG có số. score_run dừng vì `preds_ck500.jsonl` trong dataset chỉ có 1.668 bước, tức đúng các bước ck500 viết khác S1 (đã kiểm: 1.668/1.668 câu trùng bản đầy đủ `runs/grpo_spice/pred_ck500_test.jsonl`). Tệp không sai; notebook gọi score_run như với nhánh đủ bước nên bị chặn. Phải chạy lại: chấm 1.668 bước rồi ghép với S1, hoặc chấm bản đầy đủ 4.463 bước.
  · S1 dưới Phi-Ground cũng chưa có số (kernel `k_s1` trong `_bundles/phiground_ck/` chưa thấy chạy trên tài khoản nào).
  · Cách viết: chưa được in số Phi-Ground nào vào luận văn khi chưa có ít nhất S1 và ck500 cùng dụng cụ; vẫn cấm "đã đóng đòn cùng họ Qwen" (G3). Chưa kiểm dữ liệu huấn luyện Phi-Ground có AndroidControl không.

G9. Phi-Ground, S1/101 đã có (kernel `trangphngngc/phiground-s1` COMPLETE, phát hiện 25/10 trưa; đầu ra `runs/phiground/s1_25_10/`). Số test, một hạt.
- S1/101 exec 46,97 trên 4.462 bước (bước câu rỗng không có trong tệp; tính trên 4.463 với câu rỗng = 0 là 46,96).
- Ghép cặp trên 4.463 bước (bước thiếu tính 0; Base thiếu 7 bước), bootstrap cụm app, McNemar chính xác: S1/101 − Base **+6,16 [+4,71; +7,64]**, b=693 c=418, p=1,4e−16. Dưới UGround cùng phép so là +11,52, dưới UI-Venus (lát 2.532) +9,68. Hướng giữ dưới dụng cụ ngoài họ Qwen, độ lớn nhỏ hơn khoảng một nửa.
- Còn thiếu để so ck500/R3: chấm 1.668 câu ck500 khác S1 và 327 câu R3 khác cả S1 lẫn ck500 (tổng 1.995 bước, ước ~1,3 h T4 [suy từ 2,95 h / 4.462 bước của lượt S1]). Cách gọi: `score_run.py --mode score --n <số dòng tệp>` (có `--n` thì không bị chặn ở phép kiểm thiếu 1%; tệp chỉ chứa các bước cần chấm), rồi ghép theo (bước, câu) như `venus_ck_doc.py`.
- Cách viết: số Base/S1 chưa đủ để nói gì về ck500. Vẫn cấm "đã đóng đòn cùng họ Qwen" cho tới khi kiểm xong dữ liệu huấn luyện của Phi-Ground (G3).

G10. Kết quả Kaggle chiều 25/10.

**Phi-Ground (bộ trỏ ngoài họ Qwen), đủ 4.463 bước** (số test, một hạt giống mỗi nhánh). Kernel `trangphngngc/phiground-cham-ck-r3` chỉ chấm câu chưa có điểm (1.668 câu ck500 khác S1, 327 câu R3 khác cả hai), ghép theo (bước, câu) với kết quả S1 của G9; đầu ra `runs/phiground/ck_r3_25_10/`. Kiểm tái lập: 40 bước S1 chấm lại trùng exec 40/40, toạ độ lệch 0. Ghép xong thiếu 0 bước. Base thiếu 7 bước tính 0 (G8).
| nhánh | exec |
|---|---|
| Base | 40,80 |
| S1/101 | 46,96 |
| ck500 | 47,75 |
| R3 (ACE) | 47,73 |
Ghép cặp (bootstrap cụm app, McNemar chính xác): ck500 − S1/101 +0,78 [+0,05; +1,51] b=146 c=111 p=0,034 · R3 − S1/101 +0,76 [+0,02; +1,49] p=0,047 · R3 − ck500 −0,02 [−0,33; +0,29] p=1 · S1/101 − Base +6,16 [+4,71; +7,64] · ck500 − Base +6,95 [+5,46; +8,45].
Cách đọc: chiều Base < S1 < ck500 ≈ R3 giữ dưới bộ trỏ thứ ba, ngoài họ Qwen; mức ck500 − S1/101 nhỏ hơn dưới UGround (+1,55) và UI-Venus (+1,55), KTC sát 0, p sát 0,05. Chưa có S1/202 dưới Phi-Ground nên chưa so được với hạt thứ hai (dưới Phi-4 và UGround, so với S1/202 thì mức tăng nhỏ hơn hẳn, xem B và G1). Cách viết: "giữ hướng dưới ba bộ trỏ (UGround, UI-Venus, Phi-Ground), mức tăng khiêm tốn"; vẫn chưa được viết "đã đóng đòn cùng họ Qwen" cho tới khi kiểm dữ liệu huấn luyện của Phi-Ground (G3).

**xao101 (GRPO thưởng xáo trộn, nhánh kiểm sàn) đã train đủ 500 bước.** Commit 1 dừng ở điểm lưu 275 (không phải ~225 như ghi chú cũ); commit 2 chạy tiếp từ `checkpoint-275` tới 500 (225 bước, 148,2 s/bước, VRAM đỉnh 12,79 GiB), không cần commit 3. Log có `[nạp default] 504 tensor · |lora_B| 0.0000 → 6.1258` nên lần chạy tiếp không bị đặt lại. kl trung bình theo cửa sổ: 0,0001 (1–100) · 0,0003 (100–200) · 0,0004 (200–250) · 0,0011 (450–500), thấp hơn ck500 gốc khoảng 10 đến 30 lần (ck500 cuối lượt ~0,03); thưởng TB 0,45 → 0,48. Đọc: thưởng xáo không có tín hiệu nhất quán nên chính sách gần như đứng yên quanh S1. Chưa có điểm test; phải chấm như `kaggle_grpo_spice_test_ck500.md` (tên ra `pred_ck500_xao101`) rồi mới đưa vào luận văn. Log ở `runs/xao101/c2/`.

**AitZ (bộ dữ liệu thứ hai, chưa có điểm mô hình nào).** Kernel CPU `trangphngngc/aitz-build-cpu` dựng xong tập kiểm (bản 2). OCR lỗi hai lần do bản `rapidocr_onnxruntime` mới trên Kaggle: bản 2 không nhận ảnh PIL, bản 3 trả độ tin cậy dạng chuỗi (sửa bằng `float(conf)`, ngưỡng 0,5 giữ nguyên); bản 4 đang chạy lại OCR. Thống kê tập test chính thức của AitZ (đo, `runs/aitz/build_v2_25_10/out/thong_ke.json`): 506 tác vụ · 4.724 bước · **2.736 bước chạm** · scroll 601 · input_text 500 · enter 118 · home 232 · back 33 · hoàn tất 504. Bốn nhóm: general 1.202 · google_apps 621 · install 1.108 · web_shopping 1.793. Cỡ ảnh đa dạng, nhỏ hơn AndroidControl nhiều (412×732 · 540×1080 · 540×1140 · 540×1170 · 270×600 · 720×1520). Điểm chạm vàng nằm trong ít nhất một khung chú thích ở 1.562/2.736 bước (57%), vì khung của AitW là khung OCR và biểu tượng chứ không phải cây trợ năng.
Phải khai khi dùng: câu mô tả từng bước do GPT-4V sinh rồi ba chuyên gia đối chiếu với thao tác vàng và sửa tay chỗ không khớp (Phụ lục A.2 bài AitZ, arXiv 2403.02713); venue "Findings of EMNLP 2024" mới lấy từ README GitHub, chưa kiểm ACL Anthology; UGround có AITZ 8K trong dữ liệu huấn luyện.

G11. Dữ liệu huấn luyện của Phi-Ground (tra 25/10 tối, tận nguồn: Phi-Ground Tech Report, arXiv 2507.23779 v1, bản HTML đọc đủ cả phụ lục). Bổ sung cho G3.
- Nguồn huấn luyện bài báo liệt kê (§3.1–3.4, Bảng 8, Bảng 11 Phụ lục A): một phần dữ liệu mở của OS-Atlas, chỉ các tập con Windows, macOS, Linux, Fineweb; dữ liệu SeeClick; E2ISynth; GUIAct; trang CommonCrawl CC-MAIN-2024-46 tự render; ảnh chụp màn hình từ Bing Image Search; 80 nghìn mẫu do người gán nhãn trên Windows và Office. Câu quy chiếu phần lớn do GPT-4o sinh.
- **Không có chỗ nào nhắc AndroidControl**, cũng không nhắc AITW, AitZ, AMEX, RICO hay Widget Captioning như nguồn huấn luyện. Bài cũng không mô tả bước khử trùng lặp với benchmark.
- Hai đường gián tiếp phải khai:
  · SeeClick có dữ liệu di động (kho Android có trước AndroidControl 6/2024). Không làm Phi-Ground thấy AndroidControl, nhưng có nghĩa Phi-Ground "đã thấy màn hình Android".
  · GUIAct có tập con smartphone lấy từ AITW-general (GUICourse, ACL 2025, 9.157 mẫu). Bài Phi-Ground không nói dùng tập con web hay cả smartphone. Việc này không ảnh hưởng phép đo trên AndroidControl, nhưng **có ảnh hưởng nếu dùng Phi-Ground chấm AitZ** (AitZ dựng trên AITW, có nhóm general).
- Venue: chỉ là arXiv preprint, chưa thấy bản bình duyệt; trích phải ghi đúng như vậy.
- Cách viết được phép: "Phi-Ground-4B dựng trên Phi-3.5-Vision (ngoài họ Qwen), theo báo cáo kỹ thuật không dùng AndroidControl để huấn luyện". Như vậy dưới Phi-Ground (G10) cả hai đòn "bộ trỏ quen văn phong AndroidControl" và "bộ trỏ cùng họ Qwen" cùng được đóng, với điều kiện ghi rõ là dựa trên khai báo của báo cáo kỹ thuật, và khai luôn mức ck500 − S1/101 chỉ +0,78 [+0,05; +1,51]. Vẫn không viết "chưa từng thấy màn hình di động".

G12. Ba lượt Kaggle đêm 25/10 (xong trước 5:00 sáng 26/10). Số test, một hạt giống mỗi nhánh, ghép cặp bằng `score_run.cluster_bootstrap` (B = 10.000), McNemar chính xác.

**xao101 (nhánh kiểm sàn: GRPO 500 bước, thưởng SPICE bị xáo).** Kernel `uyenle0712/ck500-xao101-test`, đầu ra `runs/xao101/test/` (preds 4.463 dòng, kiểm hoà 16/20 trùng S1/101 như mọi lượt trước). Bảng ghép cặp ở `runs/xao101/test/so_ghep_cap_xao101.json`.
| nhánh | exec | D.3 | AitW đầy đủ |
|---|---|---|---|
| S1/101 | 59,11 | 65,49 | 74,37 |
| xao101 | 59,11 | 65,58 | 74,59 |
| ck500 | 60,65 | 67,02 | 76,25 |
| ck500/202 | 59,94 | 66,55 | 76,23 |
| R3 (ACE) | 60,68 | 67,11 | 76,32 |
- xao101 − S1/101: exec **+0,00 [−0,41; +0,42]**, cứu 45 phá 45, p = 1 · D.3 +0,09 · AitW +0,22 (p = 0,35).
- ck500 − xao101: exec **+1,55 [+0,81; +2,30]**, cứu 163 phá 94, p = 2e−5 · D.3 +1,43 [+0,69; +2,20] · AitW +1,66 [+0,94; +2,41].
- ck500/202 − xao101: exec +0,83 [+0,02; +1,65] p = 0,033 · D.3 +0,96 p = 0,016 · AitW +1,64 p = 3e−5.
- R3 − xao101: exec +1,57 [+0,85; +2,29] p = 1e−5.
- xao101 đổi câu ở 593/4.463 bước so với S1/101 (ck500 đổi 1.668).
Cách đọc: chạy thêm 500 bước GRPO cùng cấu hình (cùng KL, cùng số mẫu, cùng câu nhắc) nhưng thưởng không mang thông tin thì không tăng gì so với S1. Vậy toàn bộ mức +1,55 của ck500 thuộc về tín hiệu SPICE, không phải việc train thêm. Đây là đòn "chưa có nhánh so sánh train thêm" (từng chưa đóng từ lượt GRPO-point 6/9), nay đã đóng cho ck500. Phải khai: kl của xao101 thấp hơn ck500 10 đến 30 lần, tức thưởng xáo làm chính sách gần như đứng yên; đó đúng là điều nhánh kiểm sàn cần cho thấy, nhưng không chứng minh mọi tín hiệu thưởng khác SPICE cũng vô ích. Hạt 202 của ck500 hơn xao101 ít hơn (+0,83, KTC sát 0).

**AitZ zero-shot (bộ dữ liệu thứ hai, không train thêm).** Kernel `trangphuongngoc/aitz-gen-s1-ck500` (bản 2), 5,6 h trên T4×2, đầu ra `runs/aitz/gen_25_10/v2/` (cả bốn nhánh đủ 2.736 câu, kiểm hoà 16/20). Cụm bootstrap = episode (506 cụm, G hiệu dụng 398). Bảng ghép cặp ở `runs/aitz/gen_25_10/v2/so_ghep_cap_aitz.json`.
| nhánh | exec | hit_disk | action_ok |
|---|---|---|---|
| Base 3B | 34,50 | 47,51 | 94,08 |
| S1/101 | 37,79 | 50,00 | 93,46 |
| ck500 | 37,28 | 49,56 | 92,40 |
| ck500/202 | 36,62 | 48,90 | 92,62 |
- S1/101 − Base: exec **+3,29 [+1,51; +5,03]** p = 4,5e−4 · ck500 − Base +2,78 [+1,02; +4,50] p = 0,003 · ck500/202 − Base +2,12 [+0,44; +3,76] p = 0,021.
- ck500 − S1/101: exec **−0,51 [−1,39; +0,36]**, cứu 81 phá 95, p = 0,33 · action_ok −1,06 [−1,72; −0,40] p = 0,002.
- ck500/202 − S1/101: exec −1,17 [−2,12; −0,22] p = 0,027.
- Trên 2.502 bước cả S1 lẫn ck500 đúng loại thao tác: S1 40,17 · ck500 40,45. Vậy phần thua của ck500 nằm ở loại thao tác, phần định vị ngang S1.
Cách đọc: tinh chỉnh trên AndroidControl chuyển được sang AitZ (cả ba nhánh hơn Base có ý nghĩa), nhưng mức tăng của GRPO thưởng SPICE **không chuyển sang miền khác**; hạt 202 còn thấp hơn S1 có ý nghĩa. Không được viết "ck500 hơn S1 trên AitZ". Cách viết đúng: "trên AitZ, ck500 ngang S1 (−0,51, KTC phủ 0); lợi ích của thưởng SPICE gắn với phân phối câu chuẩn của AndroidControl". Phải khai kèm: câu chuẩn AitZ do GPT-4V sinh rồi người duyệt (văn phong khác AndroidControl, mà SPICE thưởng đúng văn phong AndroidControl); UGround có AITZ 8K trong dữ liệu huấn luyện; ảnh AitZ nhỏ (nhiều màn 270×600); chưa có mốc câu chuẩn chấm qua UGround trên AitZ (cần một lượt ~1,3 h T4) nên chưa biết trần; ACE/R3 chưa chạy trên AitZ.

**Qwen2.5-VL-7B-Instruct prompting (mốc so bên ngoài, việc #3 của report/322).** Kernel `trangphngngc/qwen7b-test` (phiên khác đẩy, ở đây chỉ đọc), đầu ra `runs/qwen7b/test_25_10/`, chấm đủ 4.463 bước trong một commit, 0 câu rỗng. Bảng ghép cặp ở `runs/qwen7b/test_25_10/so_ghep_cap_q7b.json`.
| nhánh | exec | D.3 | AitW đầy đủ |
|---|---|---|---|
| Base 3B | 47,59 | 53,60 | 63,39 |
| 7B prompting | 51,51 [49,82; 53,15] | 57,67 | 66,79 |
| S1/101 | 59,11 | 65,49 | 74,37 |
| ck500 | 60,65 | 67,02 | 76,25 |
- 7B − Base 3B: exec +3,92 [+2,66; +5,23] p = 5e−10.
- S1/101 − 7B: exec **+7,60 [+5,95; +9,28]** · ck500 − 7B **+9,14 [+7,55; +10,75]** · R3 − 7B +9,16 [+7,57; +10,79], đều p < 1e−24, giữ ở cả D.3 và AitW.
- 7B: action_ok 96,37, câu trung vị 64 ký tự (S1 33). Tốc độ sinh 0,4 bước/giây trên T4×2 (đọc từ `infer.log`; VRAM chưa có trong log, việc #7 còn thiếu số VRAM).
Cách đọc: mô hình 3B đã tinh chỉnh hơn mô hình 7B cùng họ không tinh chỉnh khoảng 9 điểm exec, gấp đôi mức 7B hơn 3B gốc. Phải khai: cùng câu nhắc của Base (không tối ưu câu nhắc riêng cho 7B), cùng họ Qwen với mô hình và bộ trỏ, chưa kiểm 7B có thấy AndroidControl lúc huấn luyện; câu 7B dài gấp đôi, mà thước có thiên vị câu dài (+5,4) nghiêng về phía 7B, nên chiều so có lợi cho 7B chứ không bất lợi.

G13. AitZ bổ sung 26/10: trần câu chuẩn và ACE/R3. Kernel `trangphuongngoc/aitz-ace-tran` (gói `_bundles/aitz_ace/`), 3,5 h T4×2, đầu ra `runs/aitz/ace_26_10/`, bảng ghép cặp `runs/aitz/ace_26_10/so_ghep_cap_aitz_ace.json`. ra_k4 = `runs/ra304_T/ra_sft/final` (md5 f3c543b0, trùng adapter lượt test 304); kiểm ra_k4 sinh lại 20 bước AndroidControl 20/20 trùng; luật R3 trong gói tái lập pred_R3_test 4.463/4.463. Khối ví dụ dựng bằng `_bundles/aitz_ace/xuat_ex_aitz.py` (tự kiểm 30/30 trùng ex_test_k4).
| nhánh | exec AitZ (2.736 bước) |
|---|---|
| câu chuẩn (trần) | 66,26 |
| Base 3B | 34,50 |
| S1/101 | 37,79 |
| ck500 | 37,28 |
| R3 (ACE) | 37,28 |
| ra_k4 riêng | 37,02 |
- Trần − S1/101 +28,47 [+26,40; +30,51]. Trên AndroidControl trần − S1/101 là +16,6. Vị trí của S1 trong dải Base → trần: AitZ 10% ((37,79 − 34,50)/(66,26 − 34,50)), AndroidControl 41%.
- R3 − S1/101 −0,51 [−1,39; +0,36] p = 0,33 · R3 − ck500 +0,00 (cứu 1 phá 1) · ra_k4 − S1/101 −0,77 [−1,68; +0,14] p = 0,14.
- ACE gần như không hoạt động trên AitZ: ra_k4 chép đúng một câu ví dụ ở 78/2.736 bước, R3 lấy câu ra_k4 ở 75 bước, trong đó 52 câu khác ck500. Khối ví dụ (truy hồi từ tập dạy AndroidControl) không chứa đúng câu chuẩn AitZ ở bước nào (0,0%; trên tập kiểm AndroidControl ~13%).
Cách đọc: ACE dựa vào việc chép câu ví dụ của cùng văn phong; sang AitZ (câu chuẩn GPT-4V) gần như không có gì để chép, nên R3 trùng ck500. Trần 66,26 cho thấy câu chuẩn AitZ chấm qua UGround vẫn cao xa so với mọi mô hình, tức khoảng trống lớn nằm ở phía mô hình chứ không ở dụng cụ; nhưng mọi nhánh tinh chỉnh chỉ nhích 2 đến 3 điểm trên Base, nên AitZ là phép thử chuyển miền khó cho cả SFT lẫn GRPO. Viết: "ngoài miền, mức tăng của ck500 và ACE không chuyển sang; tinh chỉnh SFT vẫn hơn Base". Khai kèm như G12.

G14. Việc #5: sinh câu tuần tự, lịch sử là câu mô hình tự sinh (kernel `trangphuongngoc/tuantu-lichsu-tusinh`, gói `_bundles/tuantu/`, 5,3 h T4×2; đầu ra `runs/tuantu/out/`). Mỗi tác vụ sinh từ bước 0, câu của bước trước đưa vào ô lịch sử thay cho câu chuẩn. Số test, một hạt giống mỗi nhánh. Kiểm hoà: ck500 20/20 trùng lượt cũ, S1 16/20 (S1 hoà fp16 so với lượt công bố, như report/259).
- Câu đổi so với lượt cũ (lịch sử = câu chuẩn): S1 2.671/4.463 bước chạm · ck500 2.602/4.463. Bước 0 (lịch sử rỗng) gần như không đổi (ck500 0%, S1 10% do hoà); từ bước 1 trở đi 50–80% câu đổi, tăng dần theo vị trí bước.
- Đúng loại thao tác (`canon_action`, `strict_back`), bootstrap cụm app/episode:
| | S1 cũ | S1 tự sinh | ck500 cũ | ck500 tự sinh |
|---|---|---|---|---|
| bước chạm (4.463) | 92,54 | 89,16 | 94,42 | 92,67 |
| bước không chạm (2.495) | 85,97 | 81,32 | 84,29 | 76,83 |
  - Tự sinh − cũ: S1 chạm −3,38 [−4,83; −2,11] · ck500 chạm −1,75 [−2,88; −0,75] · S1 không chạm −4,65 [−6,05; −3,30] · ck500 không chạm −7,45 [−9,33; −5,72].
  - ck500 − S1: chạm, lịch sử cũ +1,88 [+1,42; +2,39] → tự sinh **+3,52 [+2,44; +4,69]**; không chạm, cũ −1,68 [−2,76; −0,62] → tự sinh **−4,49 [−6,48; −2,61]**; toàn bộ 6.958 bước +0,65 [−0,35; +1,70] (cũ +0,60 [+0,13; +1,08]).
- exec trên bước chạm: CHƯA CÓ. Ô chấm trong kernel đầu lỗi (`score_run` chặn tệp chỉ có 2.672/4.463 câu mới; cần `--n`), đã đẩy lại thành kernel `trangphuongngoc/tuantu-cham` (đang chạy 26/10 tối). Đọc bằng `harness/doc_tuantu.py` khi về.
Cách đọc (tạm, chưa có exec): bỏ lịch sử chuẩn làm cả hai nhánh giảm vài điểm loại thao tác. Ở bước chạm ck500 bền hơn S1, khoảng cách gần gấp đôi. Ở bước không chạm thì ngược lại, ck500 giảm mạnh hơn: tác hại không chạm đã biết của ck500 (report/261 §6, câu lệch về thao tác chạm) lớn thêm khi lịch sử là câu của chính mô hình. Phải khai cả hai chiều.

G15. Tra bộ dữ liệu thứ ba (26/10 tối, tận nguồn), để trả lời câu "sao chỉ thử AitZ". Điều kiện: có mục tiêu tác vụ + câu hướng dẫn từng bước do người viết + ảnh màn hình và điểm chạm vàng ở mỗi bước.
- GUI-Odyssey (ICCV 2025, arXiv 2406.08451): câu từng bước do GPT-4o sinh từ mục tiêu, thao tác và ảnh; bước kiểm chất lượng chỉ nói tới tác vụ và câu mục tiêu, không nói câu từng bước ⇒ kém AitZ (GPT-4V có người kiểm).
- AMEX (Findings ACL 2025, arXiv 2407.17490): mức III chỉ có câu mục tiêu + chuỗi thao tác có toạ độ, không có câu từng bước.
- MoTIF (ECCV 2022): chỉ có lệnh mức cao.
- PixelHelp (ACL 2020, bản mở trong google-research-datasets/seq2act): có cụm từ ứng với từng bước nhưng không có ảnh màn hình, chỉ đặc trưng cây giao diện.
- UGIF (arXiv 2211.07615): câu lấy từ trang hướng dẫn Pixel, một câu gồm nhiều thao tác, không gióng theo màn; bài hứa phát hành, không tìm thấy bản phát hành.
- AITW tập Single: câu do người viết nhưng chính là mục tiêu của tác vụ ngắn (chủ yếu mua sắm trên web) ⇒ bài toán thành viết lại mục tiêu.
Cách viết: ngoài AndroidControl không có bộ công khai nào có câu từng bước do người viết kèm ảnh; vì vậy kiểm tổng quát hoá bằng hai đường: phần AndroidControl mà S1 chưa thấy (ACU, cùng văn phong, report/322 #8) và AitZ (khác văn phong, câu GPT-4V có người kiểm). Không chạy GUI-Odyssey vì chỉ lặp lại loại thông tin của AitZ với câu chuẩn kém tin cậy hơn.

G16. ACU: phần AndroidControl mà S1 chưa thấy (report/322 #8). Tình trạng 26/10 tối: CHƯA CÓ SỐ exec.
- Dữ liệu: 1.484 bước dựng từ TFRecord gốc (kernel `trangphuongngoc/acu-build-cpu`). Gói ảnh nằm trên GitHub Release `data-acu-build-v1` (`acu_test.zip`). Khai kèm hai điều: 1.383/1.484 bước thuộc split train chính thức của AndroidControl (giống tập kiểm chính, report/209), và có 5 bước câu chuẩn lệch với bản HarrytheOrange.
- OCR (kernel CPU `trangphuongngoc/acu-ocr144-cpu`, 1,0 h, xong 26/10 tối): dùng đúng rapidocr_onnxruntime 1.4.4 như OCR của tập dạy và tập kiểm (Python 3.12 dựng bằng uv, vì Python 3.13 của Kaggle chỉ cài được bản 1.2.3). Kiểm trên 20 ảnh tập kiểm cũ: 20/20 trùng tuyệt đối. OCR đủ 1.484 ảnh, 0 ảnh rỗng. Khối 4 câu ví dụ của ACE chứa đúng câu chuẩn ở 8,7% bước (tập kiểm chính ~13%, AitZ 0%). md5 `ocr_acu_144.jsonl` 8b0a50cf…, `ex_acu_k4.jsonl` 619448d5…; tệp ở `runs/acu/ocr144/`, dataset `trangphuongngoc/acu-ocr144`.
- Sinh câu + chấm (kernel `trangphuongngoc/acu-gen`, T4, đẩy 21:25 26/10, dự kiến xong 6–8 h sáng 27/10): sinh s1 · ck500 · ra_k4 · base · ck500_s202; chấm UGround cho câu chuẩn, s1, ck500, R3, base, ck500_s202, ra_k4. Khi về: so ghép cặp ck500 − S1, R3 − S1, R3 − ck500 (exec, D.3, AitW; bootstrap cụm app/episode), gộp với tập kiểm chính (5.947 bước, khai là gộp), cộng thước chữ trên Kaggle CPU.

G17. Thước chữ cho các kết quả 25–26/10 (kernel CPU `trangphngngc/chu-26-10-cpu`, cùng quy trình với luận văn: bộ chấm COCO + chrF + BERTScore roberta-large L17 rescaled, câu rỗng tính 0). S1/101 chấm lại trùng tuyệt đối 7/7 thước đã công bố ⇒ các hàng dưới so được với bảng cũ. Tệp `runs/text_metrics_26_10/text_metrics_26_10.json`. Chưa có KTC.
| nhánh | n | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|---|
| S1/101 (đối chiếu) | 4.463 | 51,56 | 36,79 | 67,35 | 416,12 | 44,37 | 61,26 | 66,33 |
| ck500 (bảng cũ) | 4.463 | 52,36 | 37,92 | 68,36 | 430,05 | 45,79 | 62,87 | 67,07 |
| xao101 | 4.463 | 51,32 | 36,95 | 67,36 | 418,13 | 44,40 | 61,52 | 66,40 |
| Qwen2.5-VL-7B prompting | 4.463 | 14,48 | 21,90 | 39,79 | 100,71 | 18,74 | 36,22 | 39,70 |
| S1, lịch sử tự sinh | 4.463 | 43,44 | 31,73 | 59,78 | 331,42 | 34,97 | 53,71 | 59,11 |
| ck500, lịch sử tự sinh | 4.463 | 43,50 | 32,37 | 60,39 | 333,58 | 35,10 | 54,54 | 59,23 |
| AitZ Base | 2.736 | 18,68 | 18,56 | 39,11 | 86,98 | 15,66 | 35,24 | 38,81 |
| AitZ S1/101 | 2.736 | 21,01 | 20,83 | 46,84 | 120,24 | 15,27 | 35,66 | 49,69 |
| AitZ ck500 | 2.736 | 21,48 | 21,08 | 46,92 | 123,38 | 16,37 | 36,28 | 49,68 |
| AitZ ck500/202 | 2.736 | 19,76 | 19,99 | 45,44 | 117,26 | 15,63 | 34,43 | 48,47 |
| AitZ R3 (ACE) | 2.736 | 21,45 | 21,05 | 46,91 | 123,29 | 16,40 | 36,24 | 49,63 |
| AitZ ra_k4 | 2.736 | 19,94 | 20,04 | 45,39 | 117,42 | 15,70 | 34,24 | 48,27 |
Cách đọc:
- xao101 trùng S1 ở cả 7 thước (chênh ≤ 2 điểm CIDEr-D, ≤ 0,3 ở các thước khác), giống exec (G12). Phần ck500 hơn S1 ở thước chữ (CIDEr-D +14, SPICE +1,4) là của thưởng SPICE, không phải của việc chạy thêm 500 bước GRPO.
- 7B prompting thấp xa mọi nhánh tinh chỉnh ở mọi thước (BLEU-4 14,5 vs 51,6), cùng chiều với exec 51,51.
- Lịch sử tự sinh làm cả hai nhánh giảm mạnh (CIDEr-D S1 −85, ck500 −96; SPICE −9,4 và −10,7). ck500 vẫn nhỉnh hơn S1 ở 7/7 thước nhưng khoảng cách co lại (CIDEr-D +2,2, trước là +13,9). Đây là thước đối chiếu với câu chuẩn của bước đó nên chịu cả lỗi dây chuyền từ các bước trước.
- AitZ: ck500 hơn S1 ở 6/7 thước (BERTScore ngang, −0,01), R3 gần trùng ck500 (khớp với việc ACE gần như không kích hoạt trên AitZ, G13). ck500/202 và ra_k4 thấp hơn S1 ở 6/7 thước. Mức tăng của ck500 so với S1 trên AitZ nhỏ (CIDEr-D +3,1, SPICE +1,1) và hạt 202 đi ngược chiều ⇒ không viết "ck500 hơn S1 trên AitZ" bằng thước chữ.
