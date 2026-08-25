# 118 — PHẢN BIỆN HAI BÀI (FAIR + VCL), phiên 23/8/2026

> Vòng phản biện chạy ngay sau khi viết xong hai bản thảo. Bốn vai giám khảo, soi cả nội
> dung khoa học lẫn câu chữ. Mỗi đòn có **phán quyết** và **đã vá / chưa vá được**.
>
> Trạng thái bản thảo lúc phản biện: `paper/fair2026/main.tex` **8 trang, 0 overfull**;
> `paper/vcl2026/main.tex` **9 trang một cột, 0 overfull**. Cả hai dựng bằng
> `tectonic -X compile main.tex --outdir .` (đã kiểm mốc giờ `main.pdf`, không tin số
> trang từ log cũ — bài học đã trả giá ở `CLAUDE.md`).

---

## 0. Thay đổi lớn so với kế hoạch 18/8

**FAIR không còn là bài thước đo. FAIR nay là bài MÔ HÌNH.** Chủ luận văn quyết 23/8, lý
do: FAIR là venue khó hơn nên đặt đóng góp mô hình ở đó. Thước đo vẫn nằm nguyên trong
bài nhưng đổi vai — từ *đối tượng nghiên cứu* thành *dụng cụ đã hiệu chuẩn*, gói trong
một mục rưỡi thay vì hai trang rưỡi.

Hệ quả với bảng phân số ở `CLAUDE.md`: **hết hiệu lực phần "FAIR = thước đo"**. Phân chia
mới:

| số | thuộc bài |
|---|---|
| Base 47,6 · S1 59,4 · S2 57,2 · bảng 2×2 · lát kích hoạt · phép B hai bộ trỏ · trần 75,7 · sàn 12,0/6,1 · 28,5-vs-3,5 · 5 luật chấm · tất định | **FAIR** |
| ghép hai kho 2,4× · rò rỉ 0 · OCR · chất lượng nhãn 73,6/22,0/7,6 · **phân bố dấu hiệu phân biệt** · hai cổng lọc · A′ bị bác · 9 bất biến | **VCL** |
| quy mô 64.567 / 6.958 / 4.463 | cả hai — VCL tả đủ, FAIR một đoạn + trích chéo |

Trích chéo dạng *"đang bình duyệt"* ở cả hai bài (`\cite{companionvcl}`,
`\cite{companionfair}`), vì nộp cách nhau một ngày nên không bài nào có ID.

---

## 1. FAIR — Giám khảo A: thống kê và thiết kế thực nghiệm

### A1. ⛔ "Bài dựng cả một section chẩn đoán quanh một kết quả không kết luận được"
**Đòn.** Nhánh điều trị có một hạt giống, đại lượng đăng ký trước vĩnh viễn không hoàn
tất, vậy mà Mục VIII dài nhất bài. Đây là kể chuyện quanh khoảng trắng.

**Phán quyết: đòn ĐỨNG MỘT NỬA.** Không vá bằng cách bỏ mục — bỏ thì bài mất phần có giá
trị nhất. Vá bằng ba việc:
- mở đầu Mục VIII khai thẳng *exploratory, one seed*;
- hai thành phần của chẩn đoán **có** đăng ký trước (lát kích hoạt 19/8, `strict_back`
  16/8), nêu ngày ngay trong caption bảng;
- **thêm phân tích không gian kết cục** (mới): để trung bình hai hạt giống chạm dải dương
  yếu thì S2/202 phải đạt **65,0%** — cao hơn checkpoint tốt nhất từng đo **5,4 điểm**; để
  chạm dải âm thì phải **≤ 56,0%** — nằm gọn trong tầm nhiễu hạt giống. Tức không gian còn
  lại là *trắng hoặc âm*, và quyết định ngân sách đóng nó ở trắng.

⭐ Con số 65,0 / 56,0 là thứ khiến người đọc không phải tự nghi có kết quả dương bị giấu.

### A2. ⛔ "Bảng 2×2 phân tầng theo biến do chính nhánh điều trị sinh ra"
**Đòn.** Điều kiện hoá trên biến hậu-can-thiệp. Ô "cả hai sai" có thể chỉ là tập các bước
khó, và mọi kết luận về cơ chế sụp theo.

**Phán quyết: đòn MẠNH NHẤT trong cả vòng, và ĐÃ VÁ ĐƯỢC bằng số mới.** Thêm hai cột
**Base** và **trần** vào bảng — cả hai không bị điều kiện hoá theo hành vi của S2:

| tên | point | n | Base | S1 | S2 | Δ | **TRẦN** |
|---|---|---|---|---|---|---|---|
| đúng | trúng | 1.871 | 69,0 | 81,4 | **87,1** | +5,72 | 86,6 |
| đúng | trượt | 184 | 23,4 | 25,5 | 26,1 | +0,54 | **31,0** |
| sai | trúng | 452 | 41,4 | 56,4 | 57,5 | +1,11 | 72,8 |
| sai | trượt | **738** | 24,4 | 30,8 | **5,6** | **−25,20** | **66,3** |
| *(không sinh desc)* | | 228 | 25,9 | 20,6 | 9,6 | −10,96 | 70,6 |

Mã tái lập: **`harness/phan_tich_o_khai_bao.py`** (dùng nguyên luật khớp tên và dung sai
của `gate_desc_acc.py` nên so thẳng được với `report/117` Mục 1).

**Đọc ra:** ô cả-hai-sai có trần **66,3%** — thấp hơn trần toàn tập 9 điểm, tức *hơi* khó
hơn trung bình, chứ không sụp. S2 rơi xuống 5,6 ở đúng chỗ câu người vẫn giải được hai
phần ba. ⇒ độ khó **không** giải thích hết được cú sụp.
⚠️ Vẫn phải khai: trần không bị điều kiện hoá theo bất cứ thứ gì nên nó không phải nhóm
đối chứng đúng nghĩa; phép kiểm sạch cần một thước độ khó khoá trước khi chạy. Confound bị
**chặn biên**, không bị **xoá**.

⭐ Bonus bắt được: ô *"tên đúng, point trượt"* có **trần chỉ 31,0%** ⇒ đó là vùng thước
gần như mù, nên Δ≈0 ở đó phải đọc là *không có tín hiệu*, không phải *không có hiệu ứng*.
Bản thảo đã ghi đúng như vậy.

### A3. ⚠️ "Nghiên cứu thiếu công suất cho chính câu hỏi chính"
MDE ghép cặp **2,2 pp**, ngưỡng vận hành **2,8 pp**, hiệu quan sát **−1,93 pp**. Đòn đứng
và bài **không giấu**: đã ghi cả ba con số cạnh nhau. Không vá thêm được bằng số liệu hiện
có; đây là giới hạn thật của thiết kế 4.463 bước một hạt giống.

### A4. ✅ "Bootstrap gom cụm theo app mà 55% bước không gán được app"
Đã có trong bài: luật gom khoá trước, `G=1.091`, `G_eff=454,3`, hệ số nở 1,10. Đòn đổ.

### A5. ⛔ Lỗi ký hiệu — **bắt được lỗi thật**
Bài định nghĩa `b` = số bước nhánh **thấp** giải được mà nhánh cao không. Với S2−S1 thì
nhánh thấp là S2 ⇒ phải là `b=254, c=340`. Bản đầu chép từ `report/110` là `b=340, c=254`
(ghi chú đó dùng quy ước khác). **Đã sửa.**

### A6. ⛔ Mẫu số — **bắt được lỗi thật**
S1 bỏ bước `(18710,1)`, S2 bỏ bước **khác** `(20011,2)`. Bản đầu viết trần trên "4.462
bước đã trả lời". Đúng phải là: mọi tỉ lệ trên **4.463**, câu rỗng tính `exec=0`. Kiểm lại
bằng script: base 47,59 · s1/101 59,11 · s1/202 59,62 · s2 57,18 · trần 75,73 — khớp từng
số với `CLAUDE.md`. **Đã sửa + thêm một đoạn giải thích vì sao không loại bước rỗng.**

### A7. ⛔ `41%` → `42%` — lỗi số học nhỏ
`(59,4−47,6)/(75,7−47,6) = 41,9%`. Bản đầu viết 41% (số của riêng hạt 101). **Đã sửa.**

---

## 2. FAIR — Giám khảo B: đánh giá sinh ngôn ngữ

### B1. ⛔ "So 5,6% với sàn 12,0% là so lệch quần thể"
Sàn đo trên lát 800 bước (trần lát 74,9), ô cả-hai-sai nằm trên tập kiểm đủ. **Đã bỏ hẳn
câu so sánh đó** khỏi bản thảo thay vì cố biện minh.

### B2. ⚠️ "Bỏ hết thước có tham chiếu thì lấy gì bảo vệ luận điểm reference-free"
Đòn đứng. Bản rút gọn ban đầu cắt sạch mục đó. **Đã thêm lại một đoạn**: content-word F1
dưới 0,5 ở **52,8%** câu của Base so với **13,9%** của S1 ⇒ thước có tham chiếu phạt hai
nhánh không đều vì một tính chất không liên quan tới việc nhận diện. BLEU/ROUGE nêu kèm và
**không** dùng làm luận cứ đồng thuận (luật cũ ở `CLAUDE.md` vẫn giữ).

### B3. ✅ "Thước là một model khác, không có neo người"
Đã khai ở *Scope of the construct*, có trích Zhao et al. EACL 2021 đúng chiều — họ khuyên
dùng thước có tham chiếu khi **xếp hạng hệ thống**, mà toàn bộ claim của ta là mức hệ
thống. Đòn không đổ được nhưng bài không giấu.

### B4. ⚠️ "Model có thể leo thước bằng cách viết cho bộ trỏ"
Có chặn biên: câu nêu vùng màn hình đúng ăn 89,5% vs sai 3,3% vs không nêu 54,8%. Nhưng
đây là chặn, không phải loại trừ. Giữ nguyên trong Limitations.

---

## 3. FAIR — Giám khảo C: lĩnh vực GUI và tiền lệ

### C1. ⛔ "Prior gần nhất bạn trích (GCoT) không phải bài GUI"
**Đòn đứng.** Đã mở lại nguồn: arXiv 2503.12799 = *Grounded Chain-of-Thought for
Multimodal Large Language Models*, Wu et al., **preprint không venue**, miền là ảo giác
thị giác của MLLM nói chung. Bản đầu tôi ghi nhầm tên bài thành "GUI-G²". **Đã sửa tên,
tác giả, và đã gắn chữ *outside the GUI domain*.**
**Đã thêm bằng chứng gần nhà hơn:** Aguvis bỏ inner monologue → AndroidControl-Low
**−11,4** điểm, kèm phân định rằng đó là biểu diễn trung gian cho một action head chứ
không phải câu trao cho người đọc.

### C2. ⚠️ "Vì sao kết quả của bạn ngược tiền lệ?"
**Đã thêm hẳn một tiểu mục** *Why this does not simply contradict the grounding-first
prior*, nêu ba khác biệt đo được: (i) ở họ, đối tượng grounding chính là thứ câu hỏi hỏi
tới nên lỗi grounding lộ ngay ở đáp án, còn ở ta câu sai vẫn trôi chảy; (ii) khai báo của
ta bị chấm ở **thời điểm suy luận** so với nhãn vàng, không phải chỉ ở lúc train;
(iii) thước của họ có sàn gần mức ngẫu nhiên, thước của ta có sàn **12,0** và trần
**75,7**, dải dùng được 62,9 điểm nên 2 điểm là nhỏ.

### C3. ✅ "Không so với hệ thống ngoài"
Đã giải thích bằng lợi thế sân nhà + 95,6% app tập kiểm có trong tập dạy. Đòn đổ.

### C4. ⚠️ "Bạn kết luận về `s2_nopoint` mà không chạy nó"
Bài suy từ bảng 2×2 rằng ô toạ độ là ô gánh (+1,1 đứng một mình) chứ không phải ô gây
hại. Đây là **suy luận quan sát**, và bản thảo ghi đúng vậy: hai nhánh S2r và S2-nopoint
được đánh dấu *registered and not run*. Đòn còn đứng phần "chưa chứng minh"; không vá được
bằng dữ liệu hiện có.

---

## 4. FAIR — Giám khảo D: trình bày và câu chữ

| # | đòn | xử lý |
|---|---|---|
| D1 | Abstract dài quá chuẩn IEEE | **đã rút** ~25%, bỏ các mệnh đề lặp |
| D2 | Thiếu chi tiết tái lập khâu sinh câu | **đã thêm**: greedy, một câu/bước, regex tách `<desc>` cố định, prompt trùng byte giữa các nhánh, và khai `history` là câu người ⇒ teacher-forced trên ngữ cảnh |
| D3 | Câu "the honest report of it has three parts" nghe như văn nói | **đã viết lại** |
| D4 | Abstract nói "difficulty does not explain the collapse" — quá mạnh | **đã hạ** thành *difficulty alone does not account for* |
| D5 | Nhan đề ba dòng | giữ: vế sau (*and a Diagnosis of Where It Breaks*) là thứ giữ cho nhan đề không hứa quá |

---

## 5. VCL — bốn giám khảo, gộp

### V1. ⛔ "Đây là bài mô tả quy trình kỹ thuật, đóng góp NGÔN NGỮ HỌC ở đâu?"
**Đòn mạnh nhất với venue này, và đã vá bằng số mới đo tại phiên.** Thêm hẳn Mục 5.4
*Phân bố loại dấu hiệu phân biệt*, đo trên toàn bộ 41.099 nhãn bằng cách phân loại lại
theo **việc mệnh đề làm được gì**:

| tầng tên | n | mỏ neo chữ | duy nhất | nêu trùng tên | chỉ đếm |
|---|---|---|---|---|---|
| tên rõ ràng | 30.252 | **72,2%** | 7,9 | 1,7 | 18,2 |
| chỉ có ký hiệu | 1.809 | 32,7% | 4,8 | 31,3 | 31,2 |
| **không có tên** | 9.038 | **57,5%** | 9,2 | — | 33,3 |
| toàn bộ | 41.099 | 67,2% | 8,1 | 2,6 | 22,1 |

⭐ **Phát hiện tự phê bình:** nhóm cần dấu hiệu phân biệt nhất (không tên, chỉ ký hiệu)
lại là nhóm được phục vụ kém nhất. Con số gộp 75,3% che mất điều đó.
⭐ **Bất đối xứng hướng neo:** trong 27.628 mỏ neo, *just above* 8.686 và *to the right of*
7.768, còn *to the left of* chỉ **1.894** — hệ quả của bố cục danh sách dọc và nhãn văn
bản đặt bên trái phần tử thao tác.
⭐ **Mốc so từ người:** **32,5%** trong 41.084 câu chuẩn tập dạy có ít nhất một từ chỉ vị
trí/thứ tự ⇒ quy chiếu bằng vị trí là thứ người viết thật sự dùng, không phải trang trí.

### V2. ⛔ "Không có đánh giá bằng người cho nhãn"
**Đòn ĐỨNG, không vá được trong khung thời gian.** Đã nêu thẳng ở Hạn chế: mọi chỉ số chất
lượng nhãn là **nội tại**, không phải phán quyết của người đọc về việc nhãn có giúp quy
chiếu hay không. Đây là lỗ hổng lớn nhất còn lại của bài VCL.

### V3. ⛔ "Phân định với Widget Captioning quá mỏng"
**Đã viết lại thành ba điểm**, kèm một điểm **bất lợi cho mình**: nhãn của họ do người
viết, nhãn của ta dựng bằng luật ⇒ rẻ hơn nhiều bậc nhưng chắc chắn nghèo hơn về chất
lượng ngôn ngữ, và ta không có human eval để định lượng khoảng cách.

### V4. ⚠️ "Phép kiểm ghép 48% vs 20% chứng minh được gì?"
**Đã thêm một đoạn tự giới hạn:** nó bắt **lỗi ghép có hệ thống**, không xác nhận từng
dòng; lỗi lệch ngẫu nhiên vài phần trăm vẫn lọt.

### V5. ⚠️ "Bài không có ví dụ, toàn số"
**Đã thêm Bảng 3** với bốn nhãn thật lấy nguyên văn, gồm **hai ca nhãn bó tay**: nhãn ghi
`icon | (no name) | many elements of the same kind` trong khi người viết gọi thẳng
*"Right arrow key"*. Chỗ tên phải suy từ **hình vẽ** chứ không đọc được từ **chữ** thì
đường ống OCR + cây trợ năng hụt — nêu như giới hạn nguyên tắc.

### V6. ⛔ Thuật ngữ sai
Bản đầu viết *"cây trợ năng (view hierarchy)"*. Hai thứ không đồng nhất: AndroidControl
phát hành **accessibility tree** kết xuất từ view hierarchy. **Đã sửa.** (Đúng loại lỗi
`CLAUDE.md` cảnh báo: thầy là tiến sĩ AI, biết thuật ngữ.)

### V7. ⚠️ Thiếu mục giấy phép / dữ liệu cá nhân
**Đã thêm:** AndroidControl CC0, không thu thập màn hình mới; ảnh có chứa nội dung người
dùng nhập (địa chỉ thư điện tử) và chuỗi đó **đi vào ô tên của nhãn** — chính Bảng 3 có
một ví dụ. Nêu ra để người dùng lại ngữ liệu cân nhắc.

### V8. ⚠️ Số 75,9% của ghi chú cũ vs 75,3% đo lại
Ghi chú dự án ghi **75,9%** (đo trên lát pilot). Phiên này phân loại lại **toàn bộ 41.099
nhãn** cho **75,3%** (67,2 neo + 8,1 duy nhất). Bài dùng **75,3%** vì đó là số đo được
trên đủ tập và tái lập bằng script. Chênh 0,6 điểm là do luật phân loại, không phải do dữ
liệu đổi. Ghi lại đây để lần sau không tưởng là mâu thuẫn.

---

## 6. Những đòn CÒN ĐỨNG — không vá được, phải sống chung

1. **FAIR:** đại lượng đăng ký trước vĩnh viễn không hoàn tất. Không có cách nào chữa
   bằng câu chữ; bài chọn khai thẳng kèm không gian kết cục (65,0 / 56,0).
2. **FAIR:** hai bộ trỏ đều thuộc họ Qwen ⇒ đòn *cùng họ* chưa đóng. Không có neo người.
3. **FAIR:** `s2_nopoint` và `s2r` chưa chạy nên phần quy công của khai báo là suy luận
   quan sát.
4. **VCL:** không có đánh giá bằng người cho nhãn.
5. **Cả hai:** tập kiểm không phải app-unseen; và 17,3% câu chuẩn tập kiểm xuất hiện
   nguyên văn trong 2,6% tập dạy.

---

## 7. Việc còn phải làm trước khi nộp

- [ ] Tra cho ra **giới hạn trang + mẫu định dạng chính thức của VCL2026**. Bản đang có
      dùng bố cục một cột kiểu LNCS với font/giãn dòng theo hướng dẫn VCL2025 tìm được
      (Times New Roman 13, giãn 1,5). Khối `FORMAT` ở đầu `paper/vcl2026/main.tex` gom sẵn
      chỗ phải đổi.
- [ ] Tra **chính sách nộp đồng thời** của VCL — hai bài dùng chung ngữ liệu và chung mô
      hình, nộp cách nhau một ngày.
- [ ] Rà chéo lần cuối theo bảng phân số ở Mục 0 (bảng cũ trong `CLAUDE.md` đã hết hiệu lực).
- [ ] Đọc soát tiếng Việt bài VCL bằng mắt người — trợ lý không tự bắt được giọng lệch.
