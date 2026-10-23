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
- ck500 − S1 +0,69 (b=90 c=121, p=0,039); R3 − S1 +0,69 (p=0,043); ck500 − R3 0,00 (p=0,85).
- Mức tăng nhỏ, p sát 0,05: không viết là kết luận chắc chắn.
- Chưa kiểm: luận văn đã có mục người nghe Phi-4 ở ch5 (`sec:phi4`), cần xem bảng kết quả ở ch6 có chỗ thêm hai hàng này không.

**A3. Câu kết luận nên dùng (và câu cấm).**
- Nên: ck500 hơn S1 ổn định qua ba dụng cụ độc lập (UGround, UI-Venus, Phi-4), nhưng mức tăng khiêm tốn (khoảng +1,5 exec, dưới MDE 2,11) và chỉ một hạt giống.
- Nên: R3 (ACE) chỉ ngang ck500 về exec, không hơn.
- Cấm: "kết luận chắc chắn"; "đã đóng đòn cùng họ Qwen" (UI-Venus vẫn dựng trên họ Qwen, Phi-4 là dụng cụ ngoài họ nhưng là người nghe, không phải bộ trỏ).
- Cập nhật phần giới hạn ở ch7 (dòng 18 và 38 nhắc tới dụng cụ đo) cho khớp.

**A4. Lỗi quy trình đáng ghi một dòng trong phần phương pháp đo (tuỳ chọn).**
Lượt Venus đầu chỉ cho 40 đến 190 cặp bất đồng nên không đủ sức; sau khi chấm đủ cả ba nhánh trên 1.880 bước khác nhau thì Δ có ý nghĩa. Nếu hội đồng hỏi vì sao số lượt chấm không đều, đây là lời giải thích.

## B. Đang chạy, cần cập nhật khi xong

Hai lượt Kaggle đẩy chiều 23/10 (S1 hạt 202):
- `uyenle0712/som-s1-202`: Phi-4 người nghe cho S1/202, 1.652 bước viết khác S1/101.
- `trangphngngc/venus-s1-202`: UI-Venus cho S1/202, 1.319 câu chưa có kết quả.

Khi xong: tính ck500 − S1/202 và R3 − S1/202 trên cả hai dụng cụ, rồi ghi vào cùng chỗ A1 và A2. Câu hỏi cần trả lời: Δ có cùng dấu và cùng cỡ với S1/101 không. Cần mở rộng `harness/venus_ck_doc.py` thêm nhánh `s1_202` (hiện chỉ có S1/101, ck500, R3).

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
- Khi hai lượt Kaggle S1/202 xong: cập nhật mục B bằng ck500 − S1/202 và ACE − S1/202 trên Phi-4 và Venus.
