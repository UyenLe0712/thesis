# Phán quyết debate: có đổi reward SA-SPICE-v3 sau khi có số test không (15/11/2026)

Nguồn: `00_su_kien_test.md` (số test), `01_ben_giu.md`, `02_ben_doi.md`, report/334 sinh lại B = 10.000.

## Kết luận

**Không đổi reward của phương pháp chính.** Giữ SA-SPICE-v3 ck400 làm kết quả chính. Vấn đề back xử lý bằng một biến thể có tên riêng, can thiệp ở dữ liệu câu nhắc, báo cạnh lượt gốc.

## Vì sao

1. Số test ủng hộ: exec 61,21 là cao nhất mọi nhánh RL; phép so sạch nhất (cùng điểm xuất phát SFT-cont) +1,05 [+0,46; +1,65] p = 6,8e−4; so S1/101 +2,11 [+1,33; +2,89] [test].
2. Luật rẽ nhánh viết TRƯỚC test (báo cáo `reports/Reward thay thế SA SPICE v3.md`, mục phương án dự phòng): bước chạm tăng mà không chạm tụt ⇒ giữ reward, chữa ngoài reward. Test rơi đúng nhánh đó. Đổi reward lúc này là chọn theo test.
3. Hai bên cùng đo được (sàng 8 mẫu SFT-cont, [tự tính]): ở nhóm back, reward SA đã xếp câu đúng loại trên câu sai loại ~0,89 cặp; bản sửa của bên đổi chỉ nâng lên ~0,90. Trên 39 bước test bị phá, reward SA cho câu đúng 0,737 vs câu sai 0,169. Nhưng nhóm back chỉ nhận 3–4% khối gradient (39/1.000 câu nhắc) và không phép sửa reward nào tăng được tỉ phần này ⇒ điểm nghẽn là tần suất câu nhắc, không phải hàm thưởng.
4. Lý lẽ đúng của bên đổi được giữ làm biến thể phụ: với SA, 36% câu back đúng loại nhận advantage âm do nhiễu chữ ("previous screen" vs "previous page" SPICE = 0). Đây là căn cứ cho nhánh NT (back chấm theo loại thao tác) nếu phân tầng câu nhắc không đủ.

## Không được viết

- "SA-SPICE-v3 hơn GRPO + SPICE (ck500)": +0,56 [−0,05; +1,17] p = 0,069.
- "SA là tốt nhất" mà không kèm một hạt giống và biến thiên A/A 0,72–0,92.
- "Thành phần composite giúp hơn SPICE thuần": chưa có nhánh SPICE thuần từ SFT-cont.

## Việc kế, theo thứ tự

| # | việc | máy | ghi chú |
|---|---|---|---|
| 1 | độ đo văn bản test SA ck400 | Kaggle CPU ~30 phút | lấp ô trống report/334 §4 |
| 2 | SA hạt 401 + 503, công thức y hệt, chọn điểm lưu trên DEV bằng cùng tiêu chí | Kaggle T4×2, ~20 h/lượt [suy] | điểm yếu lớn nhất hiện nay |
| 3 | SPICE thuần (SPICE-MATCH) từ SFT-cont, hạt 101 | Kaggle T4, ~20 h | ablation để bảo vệ composite |
| 4 | SA + câu nhắc phân tầng (back ~8%), tên riêng | Kaggle T4, ~20 h + DEV | luật đi/dừng ghi trước khi chạy |
| 5 | tuỳ chọn: NT (back chấm theo loại) hoặc trọng số advantage theo loại | — | chỉ khi #4 không cứu back |

Luật đi tiếp cho #4 và #5 (ghi trước, trên DEV-v3): back ≥ 72/104, không chạm tụt ≤ 2 so SFT-cont, exec bước chạm ≥ SA ck400 − 0,5.

## Bổ sung: độ đo văn bản test SA ck400 (kernel `trangphngngc/chu-sa3-test-15-11-cpu`, tải về `runs/sa_spice_v3/test/chu/`)

| | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|
| SA ck400 | 51,24 | **38,90** | **69,31** | 429,12 | 45,76 | **64,40** | 67,59 |

Ghép cặp (KTC95 bootstrap, * = loại 0):
- SA − SFT tiếp: BLEU-4 −0,82* · ROUGE-L +0,76* · CIDEr-D +3,33 · SPICE +0,43 · chrF +1,77* · BERT +0,54*
- SA − ck500: BLEU-4 −1,12* · ROUGE-L +0,95* · CIDEr-D −0,93 · SPICE −0,03 · chrF +1,53* · BERT +0,52*
- SA − S1/101: BLEU-4 −0,31 · ROUGE-L +1,96* · CIDEr-D +13,01* · SPICE +1,39* · chrF +3,14* · BERT +1,26*

Đọc: SA ck400 cao nhất mọi nhánh ở METEOR, ROUGE-L, chrF; SPICE ngang ck500 và không tăng có ý nghĩa so điểm xuất phát (+0,43). Phần tăng văn bản so SFT tiếp đi qua chrF/ROUGE-L, không qua SPICE ⇒ câu "SPICE làm lõi" cần nhánh SPICE thuần từ SFT-cont để bảo vệ (việc #3). Không đổi phán quyết.
