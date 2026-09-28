# Kết quả smoke bộ chọn câu nhận biết màn sau (report/232), 28/9: KHÔNG ĐẠT, dừng, không lên Kaggle

> Thi hành `report/232` bước 1–2. 0 GPU, không ảnh, không adapter. Script `harness/selector_man_sau.py`,
> tệp ra `runs/selector_man_sau/` (`ket_qua_smoke.json` · `chon_smoke.jsonl` · `smoke.log`).
> ⚠️ 400 bước smoke là val mà S1 đã thấy lúc train ⇒ **cấm trích số val ra báo**. Số dưới đây chỉ để quyết lượt 2.

## 1. Kết quả (400 bước `runs/c1/c1_mau.jsonl`, bộ chấm COCO chính thức, một câu tham chiếu)

| Hàng | BLEU-1 | BLEU-2 | BLEU-3 | **BLEU-4** | METEOR | ROUGE-L | **CIDEr-D** | **SPICE** | đổi khỏi greedy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1. S1 greedy | 75,06 | 69,52 | 64,41 | **59,48** | 42,83 | 75,32 | **543,77** | **57,30** | 0 |
| 2. Student không distill | 59,79 | 52,83 | 47,19 | 41,96 | 32,00 | 60,72 | 379,10 | 41,48 | 287 |
| 3. Student distill (đề xuất) | 59,03 | 51,87 | 46,08 | **40,86** | 31,21 | 59,16 | **368,09** | **41,07** | 292 |
| *chẩn đoán: teacher xem màn sau lúc chọn (không hợp lệ lúc chạy)* | 61,99 | 54,95 | 49,25 | 44,11 | 33,30 | 61,96 | 393,14 | 44,41 | 286 |

Mốc tham khảo cùng 400 bước (`harness/c1_doc.py`): **một mẫu ngẫu nhiên** trung bình CIDEr-D **406,0**; oracle best-of-8 672,2.

- Điều kiện (1) hàng 3 > hàng 1 ở cả BLEU-4, CIDEr-D, SPICE: **KHÔNG ĐẠT**, thua cả ba, mỗi thước 16–176 điểm.
- Điều kiện (2) hàng 3 > hàng 2 ở ≥2/3: **KHÔNG ĐẠT**, thua cả ba.
- ⇒ Theo `232` §0 bước 2: **dừng, ghi kết quả âm, không sinh 4.463 bước test, không lên Kaggle.**
- `exec` không tính được trên CPU (cần UGround); theo `232` không làm thêm thí nghiệm để đo.

Chạy hai lần (lần đầu hỏng ở khâu ghi JSON vì kiểu `numpy.bool_`, đã sửa): hai lần ra **trùng từng chữ số** ⇒ script tất định.

## 2. Đọc kết quả

1. **Thất bại không nằm ở khâu distill.** Chính teacher, dù được xem màn sau lúc chọn, cũng thua greedy
   xa (CIDEr-D 393 so với 544). Distill chỉ làm mất thêm một ít (379 → 368).
2. **Bộ chọn còn kém hơn chọn ngẫu nhiên một mẫu** (368–393 so với 406). Nó rời greedy ở ~72% số bước
   và chọn sai hướng, không chỉ là nhiễu.
3. **Không phải thiên vị độ dài.** Số từ trung bình: câu chuẩn 7,3 · greedy 7,2 · hàng 2 6,9 · hàng 3 7,1.
4. **Nguyên nhân khả dĩ nhất [suy, chưa đo riêng]:** lệch phân bố giữa lúc dạy và lúc chọn. Câu âm lúc dạy
   là câu chuẩn của bước click *khác* (đúng như `232` §4), toàn là câu người viết, đúng loại thao tác. Lúc
   chọn, ứng viên là mẫu S1 ở nhiệt độ 1,0, lỗi của chúng là kiểu khác hẳn: đổi thao tác (`"Swipe up"` ở một
   bước click, ví dụ bước thứ ba trong `chon_smoke.jsonl`), diễn đạt lệch, thêm bớt chi tiết. Bộ xếp hạng
   chưa từng thấy loại lỗi đó nên không có tín hiệu để phạt. Độ đúng cặp trên tập dạy cũng chỉ ~0,70
   (teacher 0,717 · hàng 2 0,699 · hàng 3 0,691) vì câu âm "khó" thường là cùng một tác vụ ở episode khác
   (ví dụ `agents.txt` ↔ `agent.txt`).
5. Theo `232` §0 bước 4 và §1.2: **không sửa thiết kế rồi chạy lại** sau khi đã thấy số. Điểm 4 chỉ là
   lời giải thích, không phải lý do để mở lại.

## 3. Những lựa chọn do tôi đặt (`232` không có phần phụ lục chứa script)

Bốn ảnh nguồn không có mã (ảnh 4 dừng ở mục "6. Cấm" bị cắt). Script viết theo đúng §3–4; các chi tiết
dưới đây `232` không quy định, đã chốt trước khi chạy và nằm ở đầu tệp script:

| Chi tiết | Giá trị |
|---|---|
| Tập dạy | bước click thuộc `train_tru_val.jsonl` có bản ghi bước kế: **30.478** bước (val bị loại; có `assert` bước smoke không lẫn vào tập dạy) |
| Đặc trưng câu | băm unigram + bigram (2^15 ô) |
| Đặc trưng ngữ cảnh student (13) | độ phủ từ nội dung của câu trên tên phần tử màn hiện tại, trên goal, trên câu history cuối; khớp trọn/khớp chuỗi con tên phần tử; từ vị trí; động từ chạm / không chạm; độ dài |
| Thêm cho teacher (6) | độ phủ trên tên màn sau, trên tên **mới xuất hiện** ở màn sau, trên tên **biến mất**; khớp tên mới |
| Mô hình | lớp 1 = EmbeddingBag(2^15→64) + Linear(dày→64), ReLU, lớp 2 Linear(64→1) |
| Câu âm | 4 bước click khác episode có nhiều tên phần tử trùng nhất (tích ma trận thưa), loại câu trùng nguyên văn câu dương |
| Train | margin 0,2 · Adam lr 2e-3 · 5 epoch · lô 256 · hạt giống 101 |
| Distill | teacher chấm 4 câu âm; mọi cặp (a, b) teacher xếp a > b thành một số hạng margin 0,2, cộng với loss dương/âm, trọng số 1:1 |
| Lúc chọn | nhóm = greedy + 8 mẫu; điểm cao nhất, hoà giữ greedy |

## 4. Việc kế

Không có lượt Kaggle nào cho hướng này. Hướng dừng ở smoke; mọi biến thể (câu âm lấy từ chính mẫu S1,
thêm đặc trưng loại thao tác, v.v.) đều là **quyết định mới** sau khi đã thấy số, phải được user quyết và
ghi như vậy.
