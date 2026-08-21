# 113 — Vắt kiệt bốn nhánh đã chấm (17/8/2026)

> Bốn nhánh đã có tệp thô: **trần** (câu người) · **s1/seed101** · **s1/seed202** · **Base**.
> Tất cả phân tích dưới đây **không tốn giây GPU nào** — chúng đọc lại `runs/*_raw.jsonl`.
> Mã: `harness/phan_tich_bon_nhanh.py` · `harness/mde_that.py`.
>
> ⚠️ Luật cụm dùng ở đây **trùng khít `score_run.py:645`**: `app` nếu có, không thì **mã tác
> vụ** (`ep{episode_id}`). Dùng luật khác (mỗi bước một cụm) cho ra 2.906 cụm thay vì 1.091 và
> mọi con số thắng-hoà-thua lệch hẳn — đã mắc một lần khi viết script này.

---

## A. Bảng chính thức

| nhánh | executability | Voronoi | đĩa 14% | thao tác đúng |
|---|---|---|---|---|
| **trần** (câu người) | **75,73%** | 75,77% | 84,27% | 100,00% |
| **s1 / seed 101** | 59,12% | 60,20% | 69,18% | 94,37% |
| **s1 / seed 202** | 59,64% | 60,71% | 69,79% | 94,60% |
| **Base** (chưa huấn luyện) | 47,60% | 48,88% | 57,64% | 96,46% |

**S1 trung bình hai hạt giống = 59,38%.**
· S1 − Base = **+11,78 pp** · trần − S1 = **+16,35 pp**
· S1 đạt **78,4% của trần**, lấp **42%** khoảng Base→trần.

---

## B. ⭐ Mọi lát cắt chẩn đoán đều TÁI LẬP ở hạt giống thứ hai

Đây là thứ hạt giống 202 mua được mà một hạt giống không mua nổi. Một lát cắt chỉ đáng tin nếu
nó xuất hiện ở **cả hai** lượt train độc lập.

| lát | n | s101 | s202 | s101−Base | s202−Base |
|---|---|---|---|---|---|
| app đã thấy lúc dạy | 1.737 | 59,1% | 59,2% | **+11,9** | **+12,1** |
| app **chưa** thấy | 78 | 59,0% | 59,0% | **+14,1** | **+14,1** |
| không gán được app | 2.647 | 59,2% | 59,9% | +11,2 | +11,9 |
| màn ít nút (<40) | 1.075 | 67,1% | 67,0% | +12,2 | +12,1 |
| màn vừa (40–80) | 1.495 | 58,4% | 59,1% | +10,1 | +10,8 |
| màn dày (>80) | 1.892 | 55,2% | 55,9% | +12,3 | +13,0 |

**6/6 lát cùng dấu, lệch nhau nhiều nhất 0,9 pp.** Riêng lát *app chưa thấy* trùng khít
**+14,1 / +14,1**.

⇒ Khẳng định *"không có lợi thế sân nhà"* — đòn phản biện tự khai nặng nhất từ 6/8 — nay đứng
trên **hai lượt train độc lập**, không phải một.

Thắng-hoà-thua theo cụm cũng tái lập: **395 / 565 / 131** (s101) và **406 / 572 / 113** (s202)
trên 1.091 cụm.

---

## C. ⚠️ PHẢI SỬA TRONG BÀI — trần KHÔNG phải cận trên theo từng bước

| | số bước mô hình trúng mà **câu người trượt** |
|---|---|
| s1/101 | 102 = **2,29%** |
| s1/202 | 101 = 2,26% |
| Base | 102 = 2,29% |
| **ít nhất một mô hình** | **160 = 3,59%** |

Chữ "trần" đang gợi ý một cận trên đúng ở **từng bước**. Nó không phải vậy: nó là **mức tổng**.
Có 160 bước (3,6%) mà câu người viết không giải được nhưng một mô hình nào đó giải được.

**Cách viết đúng:** *"the human-reference score is an aggregate reference level, not a per-step
upper bound: on 3.6% of steps a model resolves what the reference does not."* Không sửa chỗ này
là để hở một đòn rẻ mà giám khảo chỉ cần một phép lọc là bắt được.

---

## D. ⚠️ PHẢI SỬA — vùng mù thật là **20,7%**, không phải 24,3%

Hợp của bốn nhánh giải được **79,31%** số bước. Con số 24,3% là vùng mù **của riêng câu người**;
vùng mù **của dụng cụ** hẹp hơn.

⇒ Bài nên phân biệt hai con số: *"the references leave 24.3% unresolved; the union of all four
arms leaves 20.7%, which is the instrument's blind region."*

Ở **923 bước (20,7%) không nhánh nào giải được**: **71,3%** là bộ trỏ **bỏ cuộc** (sai > 14% bề
ngang ở nhánh trần), và màn ở đó **dày hơn** — trung vị **79 nút** so với 68 toàn tập.

---

## E. ⭐ Phần quần thể có thể phân giải được — cách diễn đạt độ lớn hiệu ứng tốt hơn

Ở bước mà hai nhánh viết câu khác hẳn nhau **nhưng bộ trỏ vẫn trả về cùng một điểm**, bước đó
**không bao giờ** phân biệt được hai nhánh. Đếm tỉ lệ ấy cho **cận trên** của phần quần thể mà
thước có thể dùng để phân giải.

| cặp | bước câu khác | điểm **trùng** | điểm **khác** | chênh tổng | chênh **trong phần phân giải được** |
|---|---|---|---|---|---|
| trần vs Base | 4.460 | 52,1% (đúng 84,1%) | 47,9% | +28,1 pp | **+58,8 pp** |
| trần vs s1/101 | 3.728 | 62,3% (đúng 82,7%) | 37,7% | +16,6 pp | **+44,1 pp** |
| s1/101 vs Base | 4.455 | 55,7% (đúng 71,7%) | 44,3% | +11,5 pp | **+26,0 pp** |
| s1/101 vs s1/202 | 1.652 | 65,1% (đúng 67,5%) | 34,9% | −0,5 pp | −1,5 pp |

Trong 1.403 bước mà **cả bốn** câu khác nhau, **31,9%** vẫn cho bốn điểm trùng nhau (và 85,7% số
đó là đúng) ⇒ **nhiều nhất 68%** quần thể có khả năng phân giải bốn nhánh.

⚠️ **KHÔNG đọc thành "sàn".** Điểm trùng phần lớn là vì **cả hai câu đều đúng** — bằng chứng:
trong nhóm trùng điểm của cặp trần-vs-Base, **84,1% là trúng**. Đây là phép đo *độ dư thừa*, không
phải phép đo *sàn*. Sàn thật vẫn cần một lượt chấm câu vô nội dung (`runs/floor/preds_f1_trong.jsonl`,
đã dựng, chưa chấm).

**Vì sao đáng đưa vào bài:** nó chặn trước đòn *"+11,5 điểm nghe nhỏ"*. Hiệu ứng bị pha loãng bởi
hơn nửa quần thể mà mọi câu đều dẫn tới cùng một chỗ; trong phần thật sự phân giải được thì nó là
**+26 pp**.

---

## F. Thiên vị độ dài — kiểm ở cả bốn nhánh

| nhánh | trung vị | câu dài | câu ngắn | lệch |
|---|---|---|---|---|
| trần | 34 | 77,7% | 73,9% | +3,9 |
| s1/101 | 33 | 61,9% | 56,5% | +5,4 |
| s1/202 | 33 | 62,0% | 57,3% | **+4,7** |
| Base | 70 | 46,9% | 48,3% | **−1,4** |

Thiên vị **tái lập** trong S1 (+5,4 → +4,7) nhưng **đổi dấu** ở Base. ⇒ nó **không phải quy luật
chung của thước**, phải đo riêng cho từng nhánh. Và vì Base mới là nhánh viết dài (trung vị 70 vs
33) mà lại không được lợi, giả thuyết *"S1 thắng nhờ hợp khẩu vị thước"* mất thêm một chân.

---

## G. Việc còn lại — hai phép rẻ đã dựng sẵn, chưa chấm

Phân tích trên **không** trả lời được hai câu hỏi về tính hợp lệ, và cả hai cần đúng một lượt
chấm mỗi cái (~1 giờ Kaggle, 0 đồng):

| nhánh | câu thành gì | trả lời |
|---|---|---|
| `runs/floor/preds_f1_trong.jsonl` | `"Tap the button."` cho **mọi** bước | **sàn** — bộ trỏ trúng bao nhiêu khi câu không mang tin |
| `runs/floor/preds_f2_khongten.jsonl` | giữ vị trí, **bỏ tên phần tử** | thước đo **gọi tên** hay **chỉ chỗ** |

`f2` nhắm thẳng vào tên bài: đã biết bỏ *vị trí* mất 3,5 pp; nếu bỏ *tên* cũng chỉ mất chừng ấy
thì chữ *"element identification"* sai, phải đổi thành *localisation*.

**Vì sao sàn quan trọng hơn một con số:** nó là mảnh ghép cho phép **tách hai đóng góp**. Hiện
`S1 − Base` gánh hai vai — vừa là kết quả mô hình, vừa là bằng chứng thước phân giải được. Cặp
*"câu người vs câu vô nội dung"* có thứ tự biết trước mà **không dính mô hình nào của ta**, nên
nếu thước tái tạo được thứ tự đó thì khả năng phân giải đã được chứng minh độc lập, và
`S1 − Base` được giải phóng để chỉ còn là kết quả.


---

## H. Bổ sung 18/8 — số từ bốn lượt phản biện, đã tự kiểm lại

Mọi số dưới đây do tôi tính lại từ `runs/*_raw.jsonl`, không phải đọc lại của agent.

### H.1 Phân tích item — 4.462 bước mua được bao nhiêu bước có phân biệt?

| | n | % |
|---|---|---|
| cả ba nhánh **trúng** | 1.784 | **40,0%** |
| cả ba nhánh **trượt** | 935 | 21,0% |
| **có phân biệt** | 1.743 | **39,1%** |

**40% qua được kể cả với mô hình chưa huấn luyện** ⇒ dấu hiệu mạnh rằng sàn **cao**, và là lý
do phép chấm `f1_trong` chuyển từ *nên làm* sang *phải làm trước khi nộp*.

### H.2 Sai số bộ trỏ theo TỪNG NHÁNH — cổng A chỉ chứng nhận cho một nhánh

| nhánh | trung vị | ≤3% |
|---|---|---|
| câu người (trần) | **0,67%** | 67,3% |
| S1 | **2,00%** | 53,7% |
| Base | **7,82%** | 43,5% |

Cổng A khoá ngưỡng ≤3% và bài báo 0,7% — nhưng 0,7% đo trên **câu chuẩn**. Base bị chấm ở chế
độ **7,82%**. ⚠️ Phần biện hộ đúng mực: sai số trên câu mô hình **một phần chính là lỗi của
câu**, mà đó là thứ thước sinh ra để đo — hai thứ không tách được. Đã in vào bài.

### H.3 ⭐ Cùng nội dung, khác văn phong — đòn "thắng nhờ văn phong" mất cơ chế chính

| ngưỡng cùng nội dung | n | S1 | Base | chênh | p |
|---|---|---|---|---|---|
| F1 ≥ 0,8 | 206 | 75,2 | 73,3 | **+1,9** | 0,22 |
| F1 ≥ 0,7 | 581 | 72,6 | 71,8 | **+0,9** | 0,46 |

Khi hai nhánh gọi **cùng tên phần tử**, khoảng chênh 11,5 pp sụp còn 0,9–1,9 pp và **mất ý
nghĩa** — dù S1 ở đó vẫn ngắn hơn 11–19 ký tự, tức vẫn "đúng văn phong". ⇒ lợi thế đến từ
**gọi đúng cái gì**, không phải **viết theo kiểu nào**.

⚠️ Đây là khống chế trên **biến sau can thiệp**, nên nó *chặn trên* chứ không *kết thúc*.

### H.4 Bản KHÔNG-THAM-CHIẾU — nhan đề vá được với giá ≤0,20 pp

Loại thao tác lấy từ trường `action.action_type` (nhãn đã ghi lúc thu dữ liệu) thay vì phân
tích câu chuẩn: trần **−0,20** · S1 **−0,09** · Base **−0,02**; chênh 11,52 → **11,45**.
⇒ phụ thuộc câu chuẩn là **danh nghĩa, không thực chất**. Mã: `harness/bien_the_khong_tham_chieu.py`.

Kèm theo: điều kiện đảo nghĩa **gần như trơ** — kêu ở **3 / 4 / 13** bước trên 4.462.

### H.5 κ bị thổi bởi câu trùng byte

| | n | đồng thuận | κ |
|---|---|---|---|
| toàn bộ | 4.462 | 93,6% | 0,867 |
| **chỉ bước hai lượt viết KHÁC nhau** | **1.652** | **82,6%** | **0,650** |

63% cặp là câu trùng từng byte, nơi một thước **tất định bắt buộc** phải đồng thuận.
**0,650 mới là số đáng trích.**

### H.6 Một khẳng định của phản biện tôi ĐÃ BÁC

Có ý kiến cho rằng luật ô Voronoi phạt nhánh yếu nặng hơn, tức **thổi** khoảng chênh. Đo lại:
bước qua dung sai đĩa mà bị luật ô bác là **8,5 / 9,0 / 9,1 / 8,8%** (trần / s101 / s202 /
Base) — **phẳng**. Nếu có lệch thì 0,2 pp **ngược** hướng đó. Đòn này chết.

Ngược lại, một lá chắn miễn phí được xác nhận: khi bộ trỏ bỏ cuộc nó trả về trục giữa màn, và
ở bước có đích gần trục giữa **Base được lợi +7,1 pp** trong khi S1 chỉ +0,8 ⇒ lỗi đó **co**
khoảng chênh, không nở.

---

## I. SÀN ĐÃ ĐO — 18/8/2026, ba nhánh, ~3 giờ Kaggle, 0 đồng

Lỗ lớn nhất của bài đã lấp. Luật đọc khoá trước ở `harness/make_floor.py`; đọc bằng
`python3 harness/doc_san.py`. Lát 800 bước, trần trên lát này **74,9%**.

| nhánh | câu thành gì | điểm | KTC95 |
|---|---|---|---|
| **trần** | câu người viết | 74,9% | — |
| S1 (seed 101) | mô hình đã dạy | 58,8% | — |
| Base | chưa huấn luyện | 48,6% | — |
| **`f1_trong`** | `"Tap the button."` mọi bước | **12,0%** | [9,7 – 14,4] |
| **`f3_lechman`** | câu **thật** của bước khác — đúng văn phong, **sai màn** | **6,1%** | [4,5 – 7,9] |
| **`f2_khongten`** | giữ vị trí, **bỏ tên** (toàn lát) | 68,0% | [64,6 – 71,4] |

### I.1 ✅ Sàn thấp — dải dùng được **62,9 điểm**

`f1` = 12,0% ⇒ luật đã khoá trước gọi đây là *"thước đòi câu phải mang thông tin"*.

⛔ **Dự đoán "sàn ≈ 40%" của phản biện BỊ BÁC.** Lập luận đó suy từ việc **40,4%** số bước cả
ba nhánh cùng trúng. Nhưng sàn thật là 12,0% ⇒ những bước ấy **dễ KHI CÓ CÂU THẬT**, không phải
dễ vô điều kiện. **Suy sàn từ tỉ lệ đồng thuận là suy sai**, và nay có số chứng minh.

Vị trí các nhánh trong dải dùng được: Base **58,3%** · S1 **74,4%** · trần 100%.
S1 − Base = 10,1 pp = **16% dải**.

### I.2 ⭐⭐ `f3` < `f1` — đòn nhiễm văn phong bị giết bằng số

**6,1% [4,5–7,9] so với 12,0% [9,7–14,4], hai KTC KHÔNG chồng lấn.**

Giả thuyết nhiễm nói: *bộ trỏ đã học văn phong chú thích AndroidControl nên thưởng cho câu viết
đúng kiểu đó bất kể nội dung.* Nếu đúng, `f3` — **văn phong hoàn hảo, độ dài khớp (34 vs 35 ký
tự), nội dung sai** — phải ăn **cao**. Nó ăn **thấp nhất trong mọi thứ đã đo**, thấp hơn cả câu
vô nghĩa.

⇒ Bộ trỏ **thật sự đọc câu**: câu sai dẫn nó đi lạc, câu rỗng để nó rơi về tiên nghiệm thị giác
yếu. Đây là hành vi của dụng cụ đang đo **nội dung**, không phải đo **phong cách**.

Cộng với phép "cùng nội dung khác văn phong" (+0,9…+1,9 pp, không ý nghĩa — mục H.3), giả
thuyết văn phong nay bị đánh từ **hai hướng độc lập**.

### I.3 ⭐⭐ GỌI TÊN đắt gấp 8 lần CHỈ CHỖ — nhan đề có số bảo vệ

| phép cắt | n | trần → sau | tụt | McNemar |
|---|---|---|---|---|
| **bỏ TÊN**, giữ vị trí (`f2_khongten`) | 193 | 89,6 → **61,1** | **−28,5 pp** | b=58 c=3, χ²=47,8, **p<0,001** |
| bỏ VỊ TRÍ, giữ tên (`p3_nopos`) | 198 | 89,4 → 85,9 | −3,5 pp | b=8 c=1, p=0,046 |

**Hai quần thể gần như bằng nhau (193 vs 198)** nên so trực tiếp được. Gọi tên đáng **gấp 8
lần** nói chỗ.

⚠️ **Con số của bài là −28,5 pp trên phần bị đụng**, KHÔNG phải −6,9 pp trên toàn lát — `f2`
chỉ viết lại được 24,1% số bước nên số tổng bị pha loãng 4,15 lần. Cùng bẫy đã mắc ở phép A.

⇒ Chữ **"Element Identification"** trong nhan đề **đúng**, và nay có phép đo bảo vệ thay vì chỉ
là mong muốn. Ngưỡng khoá trước: *tụt ≥ 10 pp ⇒ n=193 thừa sức*. Đo được 28,5.

### I.4 Ba chỗ đã sửa trong bài

Abstract thêm sàn 12,0% · 6,1% · cặp 28,5 vs 3,5. §VII thay đoạn *"floor we have not
measured"* bằng phép đo. §VIII thêm đoạn gọi-tên-vs-chỉ-chỗ ngay trước phần giới hạn.
Bài vẫn **8 trang, 0 overfull**.
