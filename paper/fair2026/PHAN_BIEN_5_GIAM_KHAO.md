# Chấm bài FAIR'2026 — năm giám khảo khó tính (16/8/2026)

Bản được chấm: `main.tex` sau lượt sửa 16/8 (8 trang, 0 lỗi tràn lề).
Cách chấm: thang ACL Rolling Review — **soundness** (khẳng định có được chống đỡ
bằng bằng chứng không) và **excitement** (có đáng để cộng đồng đọc không), mỗi thang
1–5. Tôi cố tình chấm theo chuẩn hội nghị quốc tế hạng vừa, khắt khe hơn mặt bằng
FAIR, rồi quy đổi ở mục cuối.

---

## Giám khảo 1 — chuyên về đo lường và meta-evaluation

**Soundness 4,0 · Excitement 3,0 · Overall: nhận, có điều kiện**

Đây là bài hiếm hoi tự đo dụng cụ của mình trước khi dùng nó. Cổng sai số, trần
thước, đường cong độ nhạy, bơm lỗi có ngưỡng khoá trước — đủ bốn thứ mà phần lớn bài
đề xuất thước bỏ qua. Tôi cũng ghi nhận việc khai một lỗi im lặng của chính nhóm
(bản bơm lỗi cũ chấm bằng hàm không nằm trong đường chấm thật).

Ba chỗ tôi vặn:

1. **Thước đo được rằng máy trỏ tìm ra nút, chưa đo được rằng NGƯỜI tìm ra nút.**
   Bài lấy người đọc làm lý do tồn tại của tác vụ nhưng không có một phép đo nào với
   người. Truyền thống referring expression bị viện dẫn để lấp chỗ này, mà truyền
   thống ấy vẫn kiểm bằng người ở khâu cuối. *(Bài đã tự khai ở mục Limitations —
   nhưng khai không thay được đo.)*
2. **Ô Voronoi dựng trên TÂM phần tử, bỏ qua kích thước.** Một nút to nằm cạnh nút
   nhỏ thì tâm nút to có thể gần điểm trỏ hơn dù điểm ấy nằm hẳn trong nút nhỏ. Bài
   có đo phương án nearest-box và loại nó vì bác 21% câu đúng — nhưng 21% đó có thể
   là lỗi của bộ trỏ chứ không phải của luật. Lập luận loại chưa đủ chặt.
3. **Trần 75,7% được gọi là ceiling nhưng vẫn bị đọc như cận trên ở vài chỗ.** Bản
   16/8 đã sửa đúng hướng (nói rõ một hệ có thể vượt bằng cách viết cho máy trỏ).

**Đòn nguy hiểm nhất tôi sẽ viết vào review:** thước chưa có construct validity.

---

## Giám khảo 2 — chuyên về GUI agent và mô hình thị giác–ngôn ngữ

**Soundness 4,0 · Excitement 2,5 · Overall: sát mép**

Phần dữ liệu làm cẩn thận: kiểm ghép lệch một bước bằng OCR tại điểm chạm, kiểm rò
rỉ ở quy mô đủ, chín bất biến. Tôi tin số của bài.

Nhưng bài bán mình là bài dụng cụ, mà dụng cụ chỉ được thử trên **một** bộ trỏ, **một**
bộ dữ liệu, **một** mô hình nền. Mọi con số tuyệt đối vì thế gắn chặt với UGround.
Bài thừa nhận điều đó, và thừa nhận là đúng, nhưng một phép đo trên bộ trỏ thứ hai —
kể cả trên vài trăm bước — sẽ đổi hẳn sức nặng: hoặc thứ tự các nhánh giữ nguyên và
bài mạnh hơn nhiều, hoặc nó đảo và người đọc cần biết.

Điểm thứ hai: **bài về giao diện mà không có lấy một ảnh giao diện nào.** Hình duy
nhất là đồ thị. Tôi muốn thấy một màn hình thật, điểm chạm vàng, ô Voronoi, và câu
của ba nhánh đặt cạnh nhau. Với người đọc mảng GUI, một hình như thế nói nhiều hơn
nửa trang chữ.

Điểm thứ ba, thẳng thắn: **phần mô hình gần như trống.** Tên bài và mục V hứa hẹn một
ablation mà bảng VI để dấu gạch. Tôi hiểu lý do và tôn trọng việc không điền số ước,
nhưng tôi vẫn đang chấm một bài chưa có kết quả chính của chính nó.

---

## Giám khảo 3 — chuyên về thống kê và thiết kế thực nghiệm

**Soundness 4,5 · Excitement 3,0 · Overall: nhận**

Đây là phần mạnh nhất của bài. Bootstrap cụm theo ứng dụng, Kish, McNemar cho các
nhánh chấm trên cùng tập bước, MDE tính trước, ngưỡng khoá trước, luật đọc cho cả
bốn kết cục. Việc khai "một nhánh đã đăng ký nhưng chưa chạy" thay vì lặng lẽ bỏ là
thứ tôi hiếm khi thấy.

Bốn chỗ tôi soi:

1. **Quy tắc cụm quyết định lực thống kê** — 1.091 cụm so với 259 là chênh lệch lớn,
   và bài chọn quy tắc cho ra lực cao hơn. Bản 16/8 đã thêm lập luận (các tác vụ độc
   lập vì split tách theo tác vụ) và cam kết không được chọn quy tắc thuận lợi hơn
   sau khi thấy số. Chấp nhận được, nhưng tôi vẫn muốn thấy cả hai khoảng tin cậy
   khi bảng chính đầy đủ.
2. **Hằng số 2,8 trong công thức MDE** — bản trước không giải thích; nay đã ghi rõ là
   $z_{0.975}+z_{0.80}$. Đúng.
3. **Một hạt giống.** Toàn bộ mục VII dựa trên `seed 101`. Chưa có nhiễu giữa hạt
   giống thì chưa biết 11,5 điểm lớn hơn nhiễu bao nhiêu lần. Bài không được phép
   kết luận gì về S2 — và nó không kết luận — nhưng ngay cả Base-vs-S1 cũng nên có
   một cặp hạt giống mới gọi là chắc.
4. **24,5% câu của S1 trùng nguyên văn câu chuẩn.** Nếu tôi không đọc kỹ tôi đã coi
   đây là bằng chứng học thuộc. Bản 16/8 đã bổ sung đúng phép kiểm tôi định đòi: bỏ
   hết các bước đó, S1 vẫn hơn Base 8,4 điểm ($\chi^2$ = 98). Đó là câu trả lời đúng
   chuẩn.

---

## Giám khảo 4 — chuyên về đánh giá sinh ngôn ngữ

**Soundness 3,5 · Excitement 3,0 · Overall: sát mép, nghiêng nhận**

Tôi đọc bài này như một bài đề xuất thước, nên tôi hỏi câu quen thuộc: **thước mới
được so với thước nào?**

Bản trước không có câu trả lời — đó là lý do rớt của nhiều bài metric. Bản 16/8 đã
thêm mục IV-F: chấm chính những câu ấy bằng F1 trên từ nội dung, và cho thấy hơn một
nửa số câu mà thước mới chấp nhận lại bị thước tham chiếu cho dưới 0,5. Quan trọng
hơn, nó cho thấy **hai nhánh chịu thiệt không đều nhau**, nên thước tham chiếu không
chỉ ồn mà còn lệch. Đây là lập luận tôi cần và nó dùng đúng dữ liệu đã có.

Còn thiếu, và tôi sẽ ghi:

1. **Không có so sánh với chấm bằng mô hình ngôn ngữ lớn.** Bài gạt LLM-as-judge
   bằng một câu (rubric là toạ độ người chạm thật, không phải ý kiến của mô hình).
   Lập luận đúng nhưng không thay được một cột số.
2. **Thước không nhìn chất lượng câu chút nào** — ngữ pháp, độ dài, độ tự nhiên đều
   ngoài tầm. Về nguyên tắc một hệ có thể leo thước bằng câu chỉ máy đọc được. Bản
   16/8 có trả lời bằng số đo (S1 sinh chuỗi toạ độ ở 0,04% số câu, đúng bằng tỉ lệ
   của người; từ chỉ vị trí 26,8% so với 26,4%). Nó chưa chứng minh điều đó không thể
   xảy ra, nhưng cho thấy nó chưa xảy ra, và đó là điều thành thật nhất có thể nói
   khi chưa có chấm người.
3. Chuẩn của mảng vẫn là tương quan với phán đoán người. Chưa có.

---

## Giám khảo 5 — trưởng tiểu ban, đọc để quyết

**Overall: nhận với FAIR; sẽ chật vật ở hội nghị quốc tế**

Tôi đọc tóm tắt, bảng, hình, kết luận, rồi mới đọc thân bài.

Cái tôi thích: bài **không nói quá một câu nào**. Không có chữ "đầu tiên", không có
"novel", mọi con số đều có mẫu số đi kèm, hai tiêu chí bơm lỗi rớt được in ngay trong
bảng thay vì giấu trong phụ lục, và trần thước 75,7% được nhắc lại mỗi lần có điểm
số. Trong một mùa mà phần lớn bài nộp thổi phồng đóng góp, sự tiết chế này tự nó là
một lý do để nhận.

Cái tôi lo, theo đúng thứ tự tôi sẽ nêu ở tiểu ban:

1. **Bảng VI có bốn dòng gạch ngang.** Người đọc lướt sẽ kết luận "bài chưa xong".
   Nếu đến hạn nộp vẫn chưa có `seed 202`, tôi khuyên gộp bốn dòng chưa chạy thành
   một dòng duy nhất, hoặc chuyển hẳn xuống mục thiết kế, và để bảng chính chỉ còn ba
   dòng có số — ba dòng ấy đã là một kết quả đứng được.
2. **Tên bài dùng chữ "Instrument".** Đúng tinh thần bài nhưng lạ tai; "metric" là từ
   người trong ngành tìm kiếm.
3. Bài dày đặc số. Tám trang này đọc mất công gấp đôi một bài tám trang bình thường.
   Đó vừa là ưu vừa là nhược.

---

## Tổng hợp — đòn nào trùng nhau

| Đòn | Số giám khảo nêu | Vá được trước hạn không |
|---|---|---|
| **Chưa đo với người** (construct validity) | 3 (R1, R4, và R5 ngầm) | **Được — 0 đồng** |
| Chỉ một bộ trỏ | 2 (R1, R2) | Được — ~1,2 giờ GPU |
| Thiếu kết quả mô hình / bảng còn trống | 2 (R2, R5) | Một phần |
| Không có hình giao diện thật | 1 (R2) | Được — 0 đồng |
| Không so với LLM-judge | 1 (R4) | Tốn tiền API, không bắt buộc |
| Voronoi theo tâm bỏ qua kích thước | 1 (R1) | Chỉ cần một đoạn lập luận |

**Đòn nguy hiểm nhất là đòn rẻ nhất để vá.** Một lượt chấm người 100 câu, hai người
chấm độc lập, mù nhánh, hỏi đúng một câu *"đọc câu này bạn có bấm đúng nút không?"*,
rồi báo tỉ lệ đồng thuận với thước và $\kappa$ giữa hai người. Việc này không cần
GPU, không cần tiền, làm trong một buổi, và nó bịt cùng lúc ba trong năm bản review.
Ngay cả kết quả xấu cũng dùng được, vì bài đã đăng ký trước rằng đây là kiểm chéo.

## Việc nên làm, xếp theo lợi trên chi phí

| # | Việc | Giá | Đổi lại được gì |
|---|---|---|---|
| 1 | **Chấm người 100 câu, 2 người** | 0 đồng, ~3 giờ | Bịt đòn nặng nhất (3/5 review) |
| 2 | **`s1` hạt giống 202** (đang chạy) | đã trả | Nhiễu giữa hạt giống, MDE thật |
| 3 | **Hình: màn hình thật + điểm chạm + ô Voronoi + câu ba nhánh** | 0 đồng, ~1 giờ | Bịt đòn R2, và giải thích thước nhanh hơn nửa trang chữ |
| 4 | **Bộ trỏ thứ hai trên lát 500 bước** (UI-Venus) | ~1,2 giờ GPU | Bịt đòn "một dụng cụ" |
| 5 | Gộp các dòng trống của Bảng VI nếu S2 không kịp | 0 đồng | Bỏ ấn tượng "bài chưa xong" |

Việc 3 và 5 cần cắt chỗ khác vì bài đang kín đúng 8 trang. Sau lượt sửa 16/8 chỗ dễ
cắt nhất còn lại là mục III-D (nhãn khai báo — mô tả nhánh chưa có kết quả) và bảng
chọn luật chấm (bỏ dòng 5%).

## Câu thủ sẵn cho từng đòn

- *"Sao không chấm bằng người?"* — Quần thể chấm là 4.462 bước × nhiều nhánh; chấm
  người toàn tập không khả thi. Chấm người được đăng ký trước như **kiểm chéo** trên
  100 câu, không phải bản thay thế. Rubric của thước không phải ý kiến mô hình mà là
  toạ độ một người thật đã chạm.
- *"Thước có thể bị chơi."* — Đúng về nguyên tắc, và bài nói thẳng điều đó. Trong lượt
  này thì chưa: 0,04% câu chứa chuỗi toạ độ, đúng bằng tỉ lệ của câu người viết.
- *"Sao không dùng BLEU/ROUGE?"* — Mục IV-F: hơn một nửa số câu mà thước chấp nhận bị
  F1 tham chiếu cho dưới 0,5, và hai nhánh chịu thiệt không đều nhau.
- *"Điểm cao là do học thuộc câu annotator."* — Bỏ hết 1.095 bước trùng nguyên văn,
  S1 vẫn hơn Base 8,4 điểm, $\chi^2$ = 98,1.
- *"Bộ trỏ thiên vị."* — Nó thiên vị như nhau ở mọi nhánh nên phần lớn triệt tiêu
  trong hiệu số; nó khác họ mô hình được chấm, không tinh chỉnh trên dữ liệu này, và
  không thấy đáp án.
- *"Tập kiểm không phải app-unseen."* — Đo được: 59,1% ở app đã thấy so với 59,0% ở
  app chưa thấy.

## Quy đổi về FAIR'2026

FAIR là hội nghị quốc gia, kỷ yếu IEEE, phần lớn bài nộp là bài ứng dụng. Đặt cạnh
mặt bằng đó, bài này **trên trung bình rõ rệt** ở phần phương pháp đo và phần thống
kê — hai chỗ mà bài FAIR thường yếu nhất. Tôi đánh giá khả năng được nhận cao, và
phần rủi ro thật không nằm ở việc bị từ chối mà ở việc bị phản biện hỏi đúng câu
"kết quả mô hình đâu" mà không có gì để trả lời ngoài lời hứa.
