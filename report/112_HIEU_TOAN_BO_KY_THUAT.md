# 112 — HIỂU TOÀN BỘ DỰ ÁN TRONG MỘT FILE (kỹ thuật)

> Viết 16/8/2026, **cập nhật 18/8/2026**. Dành cho người mở ra mà **chưa biết gì**: đọc hết file này là nắm được
> dữ liệu dựng thế nào, mô hình huấn luyện ra sao, thước đo hoạt động bằng cơ chế gì, và
> ba con số đã đo được có ý nghĩa gì. Mọi ví dụ trong file là **dữ liệu thật lấy từ
> `runs/*.jsonl`**, không phải ví dụ minh hoạ bịa ra.
>
> Quan hệ với các file khác: `report/106` = bản đăng ký trước (thắng về *phải làm gì*) ·
> `report/108` = sổ kê khai (thắng về *đã đo được gì*) · `report/109` = bản đồ (thắng về
> *đang ở đâu*) · `report/110` = nhật ký phiên Colab (chi tiết từng lần chạy). File 112
> này **không thay** file nào — nó là bản giải thích cơ chế, để đọc một lần rồi hiểu.
>
> ## 🆕 Bản 18/8 thêm gì (đọc bản cũ rồi thì đọc bốn chỗ này)
>
> · **§5.8 mới — SÀN CỦA THƯỚC đã đo.** Câu vô nội dung được **12,0%**; câu thật nhưng của
>   màn khác được **6,1%**, thấp hơn cả câu vô nội dung. Bỏ **tên** phần tử đắt gấp **8 lần**
>   bỏ **vị trí**. Hai lỗ lớn nhất của §11.3 đóng lại nhờ mục này.
> · **§8 viết lại** — S2 đang train, và đề tài nay nộp **hai bài báo** (VCL 30/8 · FAIR 31/8).
> · **§11.3–11.5 viết lại** theo hiện trạng: (a) (b) (e) đã đóng, (c) (d) còn mở.
> · ⛔ **Con số "bộ trỏ trượt 84% khi đổi diễn đạt" đã bị rút** (§5.4, §6.7): 84% là tỉ lệ
>   thành công của một **agent đối kháng** chuyên chế câu phá mô hình, trên **desktop**.
>
> ## ⛔ Bản 16/8 có HAI KHẲNG ĐỊNH SAI, đã sửa từ bản 17/8
>
> Nếu bạn đã đọc bản cũ, hai chỗ này phải đọc lại — chúng nằm ở §5.4 và đổi cách đọc **mọi
> con số tuyệt đối** trong file:
>
> · ⛔ *"Bộ trỏ khác họ với mô hình bị chấm"* → **SAI.** UGround-V1-2B dựng trên
>   **Qwen2-VL**, cùng dòng với Qwen2.5-VL-3B đang bị chấm.
> · ⛔ *"Recipe bộ trỏ không chứa AndroidControl — đã xác minh"* → **SAI.** Bảng 1 của
>   arXiv 2410.05243 liệt kê **AndroidControl 47K phần tử nhãn người**.
>
> Cả hai từng được ghi là "đã xác minh" từ 29/7. Tra lại tận nguồn 16/8 thì cả hai sai.
> Phần còn đứng: họ lấy từ split **train**, tập kiểm của ta từ split **test** ⇒ không chồng
> lấn ở mức màn hình. Nhưng bộ trỏ **đã thấy văn phong chú thích** của kho này, mà S1 lại
> được dạy viết đúng văn phong đó. Chi tiết và hệ quả: **§5.4**.
>
> **Bài học đắt nhất của lần này:** chữ *"đã xác minh"* trong ghi chú của chính mình
> **không phải bằng chứng**. Phải tra lại tận bảng của bài gốc.

---

## Đọc file này thế nào

File dài, nhưng **không phải đọc tuần tự từ đầu tới cuối**. Ba đường đọc:

| bạn cần gì | đọc gì | mất bao lâu |
|---|---|---|
| hiểu đề tài làm gì và kết quả ra sao | **§0** → **§B** | ~15 phút |
| hiểu **hết** cơ chế kỹ thuật | **§0 → §A → §B** rồi §1 → §7 theo thứ tự | ~2 giờ |
| tra một chi tiết | mục lục ở đầu mỗi phần, hoặc §9 (bản đồ file và lệnh chạy) | — |

**Nếu bạn không làm về máy học:** đọc **§A** trước, đó là bảng giải nghĩa mười sáu chữ mà cả
file dùng đi dùng lại. Rồi đọc **§B** — nó lấy **một bước có thật** và đi hết từ ảnh chụp màn
hình tới điểm số cuối cùng. Đọc xong hai mục đó thì mọi mục còn lại chỉ là phóng to từng chặng
của §B ra mà giải thích kỹ.

**Quy ước ký hiệu trong file:**

| ký hiệu | nghĩa |
|---|---|
| ⭐ | chỗ đắt nhất, đọc kỹ |
| ⛔ | điều đã **bị rút** hoặc **cấm làm** — nếu bạn nhớ điều ngược lại thì trí nhớ đó sai |
| ⚠️ | cái bẫy, hoặc điều kiện phải nói kèm khi trích số |
| pp | *percentage point* — điểm phần trăm. 59,1% hơn 47,6% là **11,5 pp**, không viết "11,5%" |
| KTC95 | khoảng tin cậy 95% — xem §A |

---

## 0. Một trang: toàn cảnh

**Bài toán.** Cho một ảnh chụp màn hình điện thoại + mục tiêu người dùng đang theo đuổi
("đặt báo thức 1 giờ chiều") → sinh **một câu tiếng Anh** hướng dẫn bước kế tiếp
("Click on the alarm tab at the bottom"). Câu này viết **cho người đọc**, không phải lệnh
cho máy bấm.

**Vì sao khó chấm.** Không có đáp án đúng duy nhất. "Click on the search icon" và "Tap the
magnifying glass at the top" là cùng một chỉ dẫn. So chuỗi hay so embedding đều gãy — đã
đo và đã bỏ (xem §5.1). Cách giải: **không chấm câu, chấm hệ quả của câu**.

**Bốn mắt xích của hệ thống:**

```
   ảnh + mục tiêu + lịch sử + chữ OCR
              │
              ▼
   ┌──────────────────────────┐
   │ Qwen2.5-VL-3B + QLoRA    │   ← thứ mình huấn luyện
   │ (nhánh s1 / s2 / …)      │
   └──────────────────────────┘
              │  câu tiếng Anh
              ▼
   ┌──────────────────────────┐
   │ UGround-V1-2B (bộ trỏ)   │   ← KHÔNG huấn luyện, chỉ dùng làm giám khảo
   │ câu → toạ độ (x, y)      │
   └──────────────────────────┘
              │  điểm (x, y)
              ▼
   ┌──────────────────────────┐
   │ metric_exec.py           │   ← luật chấm
   │ Voronoi + thao tác + đảo │
   └──────────────────────────┘
              │
              ▼        executable = 0 hoặc 1
```

Ý tưởng của thước: **nếu câu đủ rõ để một mô hình khác — chưa từng thấy dữ liệu này — bấm
đúng nút, thì câu đó dùng được.** Gọi là **executability**.

**Ba con số đã đo** (cùng 4.462 bước chạm, cùng bộ trỏ, chấm miễn phí trên Kaggle T4):

| nhánh | executable | KTC95 | ý nghĩa |
|---|---|---|---|
| **Human** (câu người viết) | **75,7%** | [74,1 – 77,3] | **trần của thước** |
| **S1** (Qwen 3B sau QLoRA) | **59,1%** | [57,3 – 60,8] | mô hình đã dạy |
| **Base** (Qwen 3B chưa dạy) | **47,6%** | [45,9 – 49,3] | mốc so |
| **câu vô nội dung** (`"Tap the button."`) | **12,0%** | [9,7 – 14,4] | **sàn của thước** |

Đọc: dạy được **+11,5 điểm** so với chưa dạy (chắc chắn, p<0,001, đã qua năm đòn phản biện);
mô hình đạt **78,1% của trần**; còn **16,6 điểm** dư địa cho can thiệp tiếp theo.

⚠️ **Đừng đọc 59,1% trên nền 100.** Cái thước này chạy từ **12,0 tới 75,7**, không phải từ 0 tới
100. Đầu trên: 24,3% số bước ngay cả câu người viết cũng không qua được — giới hạn của **dụng cụ
đo**, không phải của ngôn ngữ. Đầu dưới: một câu đúng ngữ pháp mà rỗng nghĩa vẫn ăn 12 điểm nhờ
tiên nghiệm thị giác của bộ trỏ. Cách đo cả hai đầu: **§5.8**.

**Đã xong thêm, tính tới 18/8:**

| việc | trạng thái |
|---|---|
| train + chấm **s1/seed202** | ✅ hơn Base **+12,03 pp**, khớp hạt giống 101 (**+11,52**); nhiễu hạt giống chỉ **0,52 pp** |
| **sàn của thước** — ba nhánh đối chứng | ✅ **12,0%** · câu sai màn **6,1%** · bỏ tên đắt gấp 8 lần bỏ vị trí (**§5.8**) |
| tra tiền lệ chữ *executability* | ✅ có chủ (ACL 2024) nhưng **khác miền** ⇒ giữ tên, thêm câu phân định (`report/114`) |
| **MDE thật** | ✅ đo được **2,2 pp** (§5.6), thay con số đoán 2,7–4,5 |
| **độ bền của luật chấm** — chấm lại dưới 5 luật khác nhau | ✅ thứ tự ba nhánh **không đổi** ở luật nào (§5.7) |
| **phép diễn đạt lại** — độ nhạy diễn đạt của bộ trỏ | ✅ **đủ bốn biến thể** (§6.7): 1.139 bước viết lại, hiệu ròng **+0,35 pp** [−0,59 · +1,29], chỉ **30 bước (2,6%)** đổi chiều — quy mô 84% cần ~956. Cách nói không đổi gì; bỏ **thông tin** vị trí thì tụt −3,5 pp |
| **nhiễm bộ trỏ** | ⛔ phát hiện bộ trỏ CÓ AndroidControl và CÙNG họ mô hình (§5.4) |

**Đang chạy:** nhánh **S2** — nhánh mang đóng góp chính — hạt giống 101, dự kiến có số
22–23/8 sau khi chạy nốt hạt giống 202 và chấm cả hai.

**Còn dở:** cắt bài FAIR từ 10 xuống 8 trang · kiểm chéo bằng bộ trỏ thứ hai (giới hạn nặng nhất
còn mở) · nộp hai bài, **VCL 30/8** và **FAIR 31/8** (§8.2).

---

## A. Mười sáu chữ phải biết trước

Mỗi dòng: chữ đó nghĩa là gì nói bằng lời thường, rồi **ở bài này nó cụ thể là cái gì**.

### Về mô hình và huấn luyện

**Mô hình ngôn ngữ-thị giác (VLM).** Một mạng nơ-ron nhận **ảnh + chữ** rồi sinh ra **chữ**.
Ở đây: `Qwen2.5-VL-3B` — "3B" là **3 tỉ tham số**, tức 3 tỉ con số bên trong quyết định nó
trả lời thế nào. Cỡ này chạy được trên một card đồ hoạ thuê theo giờ, không cần siêu máy tính.

**Token.** Mô hình không đọc từng chữ cái cũng không đọc từng từ, nó đọc từng **mẩu**. `"Click"`
là một token, `"magnifying"` có thể tách thành hai. Mọi thứ đo bằng token: độ dài câu, chi phí
tính toán, giới hạn bộ nhớ. Một câu hướng dẫn ở đây dài chừng 10–20 token; cả đầu vào (ảnh +
mục tiêu + lịch sử + chữ OCR) chừng **1.500 token**.

**Tinh chỉnh (fine-tune).** Mô hình gốc đã được người khác dạy trên cả internet. Tinh chỉnh là
dạy thêm trên dữ liệu của mình để nó làm đúng việc của mình. Ở đây: dạy nó **viết câu hướng dẫn
bước kế tiếp**, thay vì trả lời chung chung.

**LoRA.** Cách tinh chỉnh rẻ: **đóng băng** toàn bộ 3 tỉ tham số gốc, chỉ gắn thêm vài ma trận
nhỏ rồi chỉ dạy mấy ma trận đó. Ở đây chỉ **14.966.784 tham số** được động vào — **0,48%** của
mô hình. Kết quả lưu ra một tệp **59,9 MB** thay vì hàng chục GB.
*Ví như không sửa lại cả cuốn từ điển, chỉ kẹp thêm mấy tờ ghi chú vào đúng vài trang.*

**QLoRA / 4-bit.** LoRA cộng thêm một mẹo nén: mỗi tham số gốc vốn chiếm 16 bit, nén còn **4
bit** để nhét vừa bộ nhớ card. Nghe như phải đánh đổi độ chính xác, nhưng ở bài này nó còn
**nhanh hơn** bản không nén (§4.2b) — một kết quả ngược trực giác đã đo chứ không đoán.

**Bước (step) và lượt duyệt (epoch).** Mô hình không học cả tập một lúc mà chia thành **lô**;
học xong một lô, chỉnh tham số một lần — đó là **một bước**. Đi hết toàn bộ dữ liệu một vòng là
**một lượt duyệt**. Ở đây: 64.567 mẫu, mỗi lô 16 mẫu ⇒ 4.036 bước một lượt, chạy **2 lượt** ⇒
**8.072 bước**, mất **~23 giờ**.

**Loss (mất mát).** Một con số đo *mô hình đang sai bao nhiêu* trên dữ liệu dạy. Càng nhỏ càng
khớp dữ liệu dạy. ⚠️ **Loss nhỏ không có nghĩa là mô hình tốt** — học thuộc lòng cũng làm loss
nhỏ. Ở đây loss dừng ở **0,4486**, không tiến về 0, và đó là **dấu hiệu tốt** (§4.1b).

**Điểm lưu (checkpoint).** Bản chụp trạng thái mô hình lúc đang học dở, ghi ra đĩa mỗi 200 bước.
Mất máy thì chạy tiếp từ đó thay vì làm lại từ đầu. Đã cứu dự án này **sáu lần** (§4.5).

**Hạt giống (seed).** Một con số ấn định mọi lựa chọn ngẫu nhiên trong lượt train (thứ tự trộn
dữ liệu, giá trị khởi tạo). Cùng hạt giống ⇒ chạy lại ra y hệt. **Đổi hạt giống rồi train lại
là cách đo xem kết quả có phải may rủi không** — ở đây hai hạt giống 101 và 202 lệch nhau
**0,52 pp**, trong khi hiệu ứng cần đo là 11,5 pp.

**Suy luận (inference).** Lúc *dùng* mô hình đã dạy để sinh câu, khác với lúc *dạy*. Rẻ hơn
dạy rất nhiều: sinh 6.958 câu mất ~1,5 giờ, còn dạy mất 23 giờ.

### Về dữ liệu và thước đo

**OCR.** Máy đọc chữ trong ảnh. Ở đây dùng để lấy **danh sách chữ hiển thị trên màn** đưa vào
đầu vào, và để **kiểm phép ghép dữ liệu** (§1.2).

**Cây trợ năng (accessibility tree).** Android tự mô tả màn hình cho phần mềm đọc màn hình dành
cho người khiếm thị: mỗi phần tử có **loại · khung bao · nhãn**. Ở đây dùng để biết **màn hình
có những nút nào và ở đâu** — vừa để dựng nhãn (§2), vừa để chấm điểm (§5.3).
⚠️ Nó không đầy đủ: trung vị 86 phần tử mỗi màn nhưng **chỉ 12,6% có tên**.

**Bộ trỏ (grounder).** Một mô hình **khác**, việc duy nhất của nó là: cho **ảnh + một câu mô tả
phần tử** → trả về **toạ độ (x, y)** của phần tử đó. Ở đây là `UGround-V1-2B`, **không huấn
luyện gì cả**, chỉ dùng làm **giám khảo**. Toàn bộ thước đo dựa trên nó — nên §5.4 dành trọn
để nói nó đáng tin tới đâu.

**KTC95 (khoảng tin cậy 95%).** Điểm đo được là 59,1%, nhưng đó là đo trên một tập kiểm cụ thể;
đo trên tập khác sẽ lệch chút ít. KTC95 `[57,3 – 60,8]` nghĩa là: **giá trị thật gần như chắc
chắn nằm trong khoảng đó**. Hai nhánh có KTC **không chồng lấn** thì chênh lệch giữa chúng
không phải may rủi.

**Ghép cặp / McNemar.** Vì mọi nhánh chấm trên **đúng cùng 4.462 bước**, ta không so hai con số
tổng mà so **từng bước một**: chỉ đếm những bước mà hai nhánh **bất đồng**. Bước cả hai cùng
đúng hoặc cùng sai thì không mang thông tin nào về việc nhánh nào hơn.
*Ví như so hai học sinh bằng cách chỉ xét những câu mà một em làm được còn em kia thì không.*
Cách này nhạy hơn hẳn: sai số chuẩn **0,64–0,75 pp** so với 0,94 pp nếu coi hai nhánh là hai
mẫu độc lập.

**Bootstrap theo cụm.** Cách ước lượng độ chắc chắn: bốc lại dữ liệu có hoàn lại hàng nghìn lần
rồi xem điểm dao động bao nhiêu. **"Theo cụm"** = bốc lại theo **ứng dụng**, không theo từng
bước lẻ — vì các màn trong cùng một app không độc lập với nhau (giống nhau, khó giống nhau),
coi chúng độc lập sẽ cho khoảng tin cậy **hẹp giả**. Ở đây: **1.091 cụm app**, cỡ mẫu hiệu dụng
chỉ còn **454,3**.

**MDE (độ chênh nhỏ nhất phát hiện được).** Với cỡ mẫu này, chênh lệch phải **lớn hơn bao
nhiêu** thì mới phân biệt được với nhiễu? Ở đây **2,2 pp**. Con số này quyết định *luật đọc kết
quả*: nếu S2 hơn S1 dưới 2,2 pp thì không được kết luận gì.

**pp (điểm phần trăm).** 59,1% so với 47,6% chênh **11,5 pp**. Không viết "chênh 11,5%" — 11,5%
của 47,6 là 5,5, con số khác hẳn.

---

## B. Theo chân MỘT bước, từ đầu tới cuối

Mục này lấy **một bước có thật** trong tập kiểm — chuỗi `18203`, bước `7` — và đi hết từ ảnh
chụp màn hình tới con số 0/1 cuối cùng. Mọi thứ dưới đây đọc thẳng từ
`harness/dg1_cache/test_ac/test.jsonl` và `runs/score_*_raw.jsonl`, không sửa gì.

### Chặng 1 — bối cảnh có sẵn trong dữ liệu

Người dùng đang muốn:

> *"I forgot to add my friend Natalie Larson's Gmail ID to the Employment Fair event, so edit
> my event and add her ID: natalie.larson1998@gmail.co"*

Bảy bước trước đó **đã làm rồi**, và câu mô tả chúng là câu **do người chú thích viết**:

```
1. click on the Three lines at the top left corner.
2. Select the first option Schedule.
3. Click on the Event "EMPLOYMENT FAIR"
4. click on the Pen Icon at the top right .
5. Click on the Tab "Add People".
6. Type Id-natalie.larson1998@gmail.com in the Input box at the top.
7. select the id.
```

Màn hình hiện tại: ảnh `ep18203_s7.png`, kích thước **1080 × 2400**. Cây trợ năng đếm được
**187 phần tử** trên màn này — một màn rất dày nút.

**Việc cần làm:** viết câu hướng dẫn cho **bước thứ 8**. Đáp án người viết là
`"click on Done at the top right corner."`, và người thật đã chạm vào điểm **(970, 219)** — góc
trên bên phải.

### Chặng 2 — đầu vào đưa cho mô hình

Mô hình **không** được thấy đáp án, cũng **không** được thấy toạ độ (970, 219). Nó chỉ nhận:

```
<image>                                    ← ảnh màn hình
Mục tiêu: I forgot to add my friend Natalie Larson's Gmail ID …
Đã làm:   … · Type Id-natalie.larson1998@gmail.com … · select the id.
Chữ trên màn: 11:04 · Add people · Done · Added guests · You · A ·
              amelia.miller2709@gmail.com · natalie.larson1998@gmail · N · .com * ·
              Some calendars cannot be shown · 88 · GIF · 2 · W · e · t · V · f · k · a · S …
Viết câu hướng dẫn cho bước tiếp theo.
```

Dòng *"Chữ trên màn"* là **OCR thật của ảnh đó**, 27 dòng, chép nguyên từ
`harness/dg1_cache/test_ac/ocr.jsonl`. Để ý phần đuôi `W · e · t · V · f · k · a · S` — đó là
**các phím của bàn phím ảo** đang mở, OCR đọc từng phím thành một dòng riêng. Đầu vào thật lẫn
nhiễu như vậy, không sạch sẽ như ví dụ trong sách. Chữ `Done` mà mô hình cần gọi tên thì nằm
ngay dòng thứ ba.

⚠️ Dòng *"Đã làm"* là câu **của người viết**, không phải câu mô hình tự sinh ở lượt trước — đây
là điều kiện phải khai kèm mọi con số trong file này, xem §1.6.

### Chặng 3 — ba nhánh trả lời khác nhau

| ai trả lời | câu sinh ra |
|---|---|
| **người** (trần) | `click on Done at the  top right corner.` |
| **S1** — Qwen 3B **đã** tinh chỉnh | `Click on the Done button at the top right corner of the screen.` |
| **Base** — Qwen 3B **chưa** tinh chỉnh | `Click on the person icon next to Natalie Larson's email address to select it.` |

⭐ **Đây là chỗ đắt nhất của cả ví dụ.** Câu của Base **không hề sai ngữ pháp, không lan man,
không bịa tên lạ** — nó nhắc đúng tên Natalie Larson có thật trong mục tiêu, và cái "person
icon" đó có thật trên màn. Vấn đề là nó **tả bước 7**, bước vừa làm xong rồi, chứ không phải
bước 8.

⇒ Thứ mà tinh chỉnh dạy được **không phải khả năng viết tiếng Anh** — mô hình gốc viết còn trôi
chảy hơn. Nó dạy **bám đúng bước hiện tại**. Đây chính là điều bảng số ở §6 nói bằng con số, và
là lý do mốc so Base được coi là mốc **sạch**: nó thua không phải vì không biết viết.

### Chặng 4 — đưa câu cho bộ trỏ

Từng câu một được đưa cho `UGround-V1-2B` cùng với **chính ảnh màn hình đó**. Bộ trỏ **không hề
biết** toạ độ đúng là gì, cũng không biết câu nào của ai.

| câu của | bộ trỏ trả về | lệch so với (970, 219) |
|---|---|---|
| người | (972, 216) | **4 px** |
| S1 | (972, 216) | **4 px** |
| Base | (851, 725) | **520 px** |

Câu của người và câu của S1 khác nhau về chữ nghĩa ("click on Done" vs "Click on the Done
button … of the screen") nhưng **dẫn tới đúng một điểm**. Đó là toàn bộ ý tưởng của thước: nó
không hỏi *câu có giống nhau không*, nó hỏi *câu có dẫn tới cùng một chỗ không*.

### Chặng 5 — luật chấm phán quyết

Ba điều kiện, phải đúng **cả ba** (§5.2):

```
executable = action_ok AND toggle_ok AND hit_voronoi
```

**Câu của S1:**

| điều kiện | kiểm gì | kết quả |
|---|---|---|
| `action_ok` | câu nói *"Click"*, thao tác thật là *click* | ✅ |
| `toggle_ok` | câu không nhắm trạng thái ngược (không có on/off, show/hide…) | ✅ |
| `hit_voronoi` | lệch 4 px, và trong 187 phần tử trên màn **không có phần tử nào gần điểm bộ trỏ hơn** nút Done | ✅ |

⇒ **executable = 1.**

**Câu của Base:** lệch (dx = −119 px, dy = +506 px). Luật dung sai quy ước xét **hai trục
riêng**, mỗi trục so với cạnh của chính nó:

```
ngang: |−119| ≤ 0,14 × 1080 = 151 px   ✅ qua
dọc  : | 506| ≤ 0,14 × 2400 = 336 px   ❌ trượt
```

⇒ trượt ngay ở luật dễ nhất, chưa cần tới Voronoi. **executable = 0.**

### Chặng 6 — cộng lại

Làm đúng như vậy cho **4.462 bước**, đếm số bước `executable = 1`, chia cho 4.462:

```
người 75,7%   ·   S1 59,1%   ·   Base 47,6%   ·   câu vô nội dung 12,0%
```

Bốn con số đó là toàn bộ kết quả của luận văn. Mọi mục còn lại trong file này trả lời một trong
ba câu hỏi về chúng: **dữ liệu ở chặng 1–2 dựng thế nào** (§1, §2, §3) · **mô hình ở chặng 3
huấn luyện ra sao** (§4) · **thước ở chặng 4–5 có đáng tin không** (§5) — và câu cuối cùng là
câu tốn công nhất, vì nếu bộ trỏ ở chặng 4 không đáng tin thì cả bốn con số vô nghĩa.

---

## 1. Dữ liệu: từ AndroidControl tới `train.jsonl`

### 1.1 Nguồn

**AndroidControl** (Li et al., Google DeepMind, **NeurIPS 2024 D&B**, giấy phép CC0) —
15.283 chuỗi thao tác người thật ghi trên Pixel trong ~1 năm. Mỗi bước có: ảnh màn hình,
loại thao tác, toạ độ chạm, và — điểm mấu chốt — **`step_instructions`: câu hướng dẫn do
người viết cho từng bước**.

⭐ **Đây là chỗ định vị của luận văn.** Trong bài gốc AndroidControl và trong mọi bài dùng
bộ này (Aguvis, UI-R1, SeeClick…), `step_instructions` nằm ở **đầu vào** — mớm cho agent
để nó đoán ra thao tác. Ở đây nó là **đích sinh**. Ngược hướng hoàn toàn.

Bản trên HuggingFace bị tách làm hai và mỗi bản thiếu một nửa:

| kho | có gì | thiếu gì |
|---|---|---|
| `HarrytheOrange/parsed_AndroidControl` | `step_instructions` đủ 15.283 chuỗi | **không có ảnh** |
| `ckg/AndroidControlParsedWithImages-20k` | ảnh | **mất `step_instructions`** |

Phải ghép hai kho theo `(episode_id, step_id)`.

### 1.2 Kiểm phép ghép có đúng không — và vì sao phải kiểm

Ghép lệch một bước thì mọi thứ phía sau vẫn chạy trơn, dữ liệu vẫn đủ số dòng, huấn luyện
vẫn hội tụ — chỉ có điều mô hình học ảnh A với câu của ảnh B. Loại lỗi này không có tiếng động.

Phép kiểm dùng: chạy OCR tại điểm chạm gold, xem chữ đọc được có xuất hiện trong câu hướng
dẫn không.

```
ghép đúng     : khớp 48%
ghép lệch 1 bước (đối chứng) : khớp 20%
                              ─────────
                              tỉ số 2,4×   (n = 400)
```

Nếu ghép sai thì hai con số phải bằng nhau. Chúng cách nhau 2,4 lần → ghép đúng.

*(Bài học đi kèm: mọi phép ghép dữ liệu phải có một đối chứng lệch chủ ý. Không có đối
chứng thì "48% nghe cũng cao đấy" là câu vô nghĩa — không biết cao so với cái gì.)*

### 1.3 Quy mô đã dựng

| | tập dạy | tập kiểm |
|---|---|---|
| bước | **64.567** | **6.958** |
| bước chạm | 41.191 (63,8%) | 4.463 (64,1%) |
| tác vụ | 12.895 | 1.432 |
| phủ OCR | 100% | 100% |

**Chia theo ỨNG DỤNG, không chia ngẫu nhiên theo dòng.** Màn hình cùng một app na ná nhau,
chia ngẫu nhiên là rò rỉ trá hình và cho điểm ảo. Đã kiểm ở quy mô đủ: **rò rỉ dạy-kiểm = 0**
tác vụ.

⚠️ **Nhưng tập kiểm KHÔNG phải "app chưa từng thấy".** 95,6% app trong tập kiểm cũng xuất
hiện ở tập dạy. Đây là **lợi thế sân nhà phải khai** — và §6.3 cho thấy nó không thành hiện
thực trong số liệu.

### 1.4 Một bản ghi thật trong `train.jsonl`

```json
{"episode_id": 5590, "step_id": 1,
 "image": "images/ep5590_s1.png",
 "goal": "Open Google maps app, Search for the nearest park to 98103 and make sure it has a rating of above 4.5 star",
 "history": [],
 "target_instruction": "Click on the search bar",
 "action": {"action_type": "click", "x": 475, "y": 219},
 "w": 1080, "h": 2400}
```

### 1.5 Đầu vào đưa cho mô hình

Ghép từ bốn mảnh, **giống hệt nhau ở mọi nhánh** (đây là điều kiện để chênh lệch điểm quy
được về can thiệp):

```
<image>
Mục tiêu: Open Google maps app, Search for the nearest park to 98103 …
Đã làm: Click on the title of this note Grocery to edit the title
Chữ đọc được trên màn: Search here · Coffee · Restaurants · Groceries · …   (tối đa 24 dòng)
Viết câu hướng dẫn cho bước tiếp theo.
```

Vì sao nhét OCR vào: cơ chế hỏng số một của mô hình là **gọi sai hoặc gọi mơ hồ tên nút**.
Đưa sẵn danh sách chữ trên màn là đánh trúng chỗ đó.

### 1.6 ⚠️ Dòng "Đã làm" là CÂU CHUẨN DO NGƯỜI VIẾT, không phải câu mô hình tự sinh

Chỗ này bản 16/8 tả sai thành *"ba thao tác gần nhất"*, và nó đổi cách đọc mọi con số.

Trường `history` chứa **`step_instructions` của các bước trước — tức câu do người chú thích
viết**. Đã kiểm: trùng nguyên văn **5.318/5.318 = 100%**.

⇒ Khâu chấm là **teacher-forced trên ngữ cảnh**: ở mỗi bước, mô hình được cho ngữ cảnh
*đúng* của các bước trước, chứ không phải ngữ cảnh do chính nó sinh ra ở lượt trước.

Hai hệ quả phải khai:

- **Mọi số tuyệt đối trong file này đọc kèm điều kiện đó.** 59,1% là điểm khi ngữ cảnh sạch,
  không phải điểm khi để mô hình chạy tự do cả chuỗi. Chạy tự do thì lỗi tích luỹ, điểm sẽ
  thấp hơn — **chưa đo**.
- **Phép SO GIỮA CÁC NHÁNH vẫn hợp lệ**, vì cả bốn nhánh nhận ngữ cảnh y hệt. Điều kiện chung
  triệt tiêu trong hiệu số.

Đây cũng là cách chuẩn của các bài dùng AndroidControl ở chế độ *step-level* (bài gốc
NeurIPS 2024 làm y vậy), nên không phải chỗ yếu — chỉ là chỗ **phải nói rõ**.

⚠️ **Không được kể phần OCR này là đóng góp.** Chính bài gốc AndroidControl đã fine-tune
với danh sách phần tử làm đầu vào (nguyên văn: *"Our agent implementation does not directly
leverage the page screenshot"*). Widget Captioning (EMNLP 2020), Screen2Words (UIST 2021),
Mind2Web (NeurIPS 2023) cũng vậy. Nó là **lựa chọn thiết kế có ablation**, không phải phát kiến.

---

## 2. Nhãn khai báo (descriptor) — trái tim của đóng góp

### 2.1 Ý tưởng

Thay vì dạy mô hình nhảy thẳng từ ảnh sang câu, dạy nó **mô tả phần tử đích trước, rồi mới
viết câu**. Đích sinh có hai tầng:

```
<desc>vai trò | tên | <point>x,y</point> | dấu hiệu phân biệt</desc>
Câu hướng dẫn
```

Lúc chấm **cắt bỏ tầng `<desc>`**, chỉ lấy câu. Nên nếu điểm tăng thì không phải vì nó được
cho thêm thông tin lúc chấm — mà vì **hành vi nội tại lúc suy luận đổi**. Đó là điều kiện
để gọi đây là đóng góp **mô hình**, không phải đóng góp **dữ liệu**.

### 2.2 Nhãn dựng TỰ ĐỘNG, không có người gán

Nguồn: cây trợ năng (accessibility tree) thật của AndroidControl — 99.131 màn, mỗi màn
trung vị 86 phần tử — ghép với OCR trong hộp tại điểm chạm gold.

Một nhãn thật (`descriptors.jsonl`):

```json
{"episode_id": 5590, "step_id": 1,
 "desc": "<desc>tappable text | Search here | <point>440,91</point> | just above the text “Coffee”</desc>",
 "desc_neg": "<desc>tappable text | Latest in Capitol Hil | <point>500,865</point> | just below the text “Park”</desc>",
 "role": "tappable text", "name": "Search here", "name_src": "ocr", "tier": "ten_ro",
 "point_abs": [475, 219], "point_norm": [440, 91],
 "box": [162, 157, 789, 283], "area_share": 0.03, "neighbor_dist_px": 1857.6,
 "dup_name": 0, "same_role": 7}
```

Bốn ô, mỗi ô có lý do tồn tại:

| ô | nội dung | vì sao có |
|---|---|---|
| vai trò | `tappable text` | phân biệt nút / ô nhập / mục danh sách |
| tên | `Search here` | chữ hiển thị — nguồn: OCR hoặc `content_description` |
| toạ độ | `<point>440,91</point>` | chuẩn hoá 0–1000. Nhãn **sạch 100%**, chi phí 0 |
| dấu hiệu | `just above the text "Coffee"` | thứ phân biệt nút này với nút giống nó |

Trường `desc_neg` = mô tả của **nút hàng xóm gần nhất**. Chưa dùng; để dành cho nhánh S3
(mất mát có khoản phạt lề) nếu cổng tuần 3 mở.

### 2.3 Chất lượng nhãn, đo ở quy mô đủ

| chỉ số | tập dạy đủ 64.567 | tham chiếu pilot |
|---|---|---|
| tên rõ | 73,6% | 73,8% |
| không có tên (chỉ icon) | 22,0% | 23,4% |
| vai trò rõ | 75,8% | — |
| trùng tên trên cùng màn | 7,6% | 6,9% |
| có hàng xóm để so | 91,6% | — |

**Cả 5 số khớp tham chiếu dưới 1 điểm** → đường ống dựng nhãn ổn định khi nhân quy mô 38 lần.

Hai lỗi từng bắt được lúc dựng, đáng ghi lại vì cùng một lớp:

1. **Cây trợ năng lồng nhau** làm "trùng tên" thổi từ 30% → thật ra 6,9%. Cùng một nút bị
   đếm nhiều lần vì nó xuất hiện ở nhiều tầng của cây.
2. **Tên class Android lọt vào nhãn** (`android.widget.TextView` thành "tên nút").

Và một cổng lọc phải thêm sau khi tranh luận: **`clean_a11y`** — 14,7% nhãn trợ năng là rác;
cộng **cổng hình học ≤25% màn** — 25 ca hộp to bằng cả màn, **0/25 khớp câu chuẩn**.

### 2.4 Một quyết định đã tranh luận rồi bác — nguồn tên

Có lúc tưởng phải đảo sang **OCR-trước** vì câu chuẩn khớp OCR gấp 3,2 lần khớp trợ năng.
Vòng phản biện bóc ra: bán kính thật chỉ **72/1074 = 6,7%** số ca; bỏ 32 ca chuỗi-số-có-sẵn
còn 40 ca lõi (OCR 12 – trợ năng 3); và **11/12 ca OCR thắng là do nhãn trợ năng RÁC**.

⇒ Ưu thế của OCR là ưu thế của **lọc rác**, không phải của **thứ tự**. Đã áp cổng lọc thay
vì đảo thứ tự. Chi tiết: `report/107`.

---

## 3. Bốn nhánh thí nghiệm

Mọi nhánh dùng **cùng đầu vào, cùng cấu hình, cùng hạt giống** — chỉ khác **đích sinh**.

Lấy đúng bước 5590/1 ở trên, đích sinh của bốn nhánh:

**s1** — SFT trơn, mốc so nội bộ:
```
Click on the search bar
```

**s2** — trụ chính, "mô tả trước, phát ngôn sau":
```
<desc>tappable text | Search here | <point>440,91</point> | just above the text “Coffee”</desc>
Click on the search bar
```

**s2r** — đối chứng, khai báo **GIẢ** lấy từ màn khác + toạ độ ngẫu nhiên:
```
<desc>item | CATEGORIES | <point>713,402</point> | to the left of the text “MEN”</desc>
Click on the search bar
```

**s2_nopoint** — bỏ ô toạ độ, giữ ba ô còn lại:
```
<desc>tappable text | Search here | just above the text “Coffee”</desc>
Click on the search bar
```

### Vì sao cần cả bốn

| cặp so | trả lời câu hỏi |
|---|---|
| s2 − s1 | thành phần có tác dụng không? (**đây là headline**) |
| s2 − s2r | tác dụng đến từ **nội dung đúng**, hay chỉ vì chuỗi đích dài thêm? |
| s2 − s2_nopoint | ô toạ độ đóng góp bao nhiêu? |

**s2r là nhánh chưa có tiền lệ nào chạy** — nó chặn đúng đòn phản biện nguy hiểm nhất
("chuỗi đích dài hơn thì mô hình học kỹ hơn, chả liên quan gì tới nội dung mô tả").

Để nó chặn được, độ dài **giả** phải sát độ dài **thật**. Cách ghép: lấy 12 bản gần nhất về
**độ dài token** (không phải ký tự — mất mát tính trên token) rồi bốc ngẫu nhiên một bản
theo hạt giống cố định 20260805.

*(Bản đầu ghép theo ký tự: trung vị lệch 0 ký tự nghe rất khít, nhưng đo lại theo token thì
chỉ 54% số cặp nằm trong 2 token, biên độ tới ±17.)*

### Phép kiểm không-gây-hại

Bước **không phải bước chạm** (cuộn, gõ, mở app — 36,2% dữ liệu) **không có khai báo**, nên
mọi nhánh giữ nguyên đích là câu. Phần dữ liệu đó **y hệt nhau ở bốn nhánh**.

⇒ Nếu s2 làm hỏng nhóm bước đó thì thấy ngay, và không đổ lỗi cho dữ liệu khác được.

---

## 4. Huấn luyện

### 4.1 Cấu hình (`harness/train_config.yaml`)

**Nói bằng lời thường trước.** Huấn luyện ở đây là: đưa cho mô hình 64.567 lượt *"đây là ảnh
màn hình và bối cảnh — câu đúng là câu này"*, mỗi lượt nó chỉnh lại một chút cho lần sau đoán
gần hơn. Đi hết 64.567 mẫu hai vòng thì dừng. Không có bước nào người can thiệp giữa chừng, và
**không có tập kiểm chứng để chọn bản tốt nhất** — đó là quyết định có chủ ý, giải thích ở §4.1b.

Cấu hình dưới đây là toàn bộ những gì quyết định lượt học đó. Đọc kèm bảng giải nghĩa ngay sau.

```yaml
model_name_or_path: Qwen/Qwen2.5-VL-3B-Instruct
finetuning_type: lora
lora_rank: 8 ; lora_alpha: 16 ; lora_dropout: 0.05
lora_target: q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj
freeze_vision_tower: true              # dạy "nói gì", không dạy "nhìn thấy gì"
freeze_multi_modal_projector: true
quantization_bit: 4                    # QLoRA, NF4
cutoff_len: 2560
per_device_train_batch_size: 4
gradient_accumulation_steps: 4         # cỡ lô hiệu dụng = 16
learning_rate: 1.0e-4 ; lr_scheduler_type: cosine ; warmup_ratio: 0.05
num_train_epochs: 2.0                  # = 8.072 bước
bf16: true ; gradient_checkpointing: true
enable_liger_kernel: true
preprocessing_num_workers: 8
save_steps: 200 ; save_total_limit: 2
seed: 101                              # và 202
```

**Từng khoá nói gì:**

| khoá | nói bằng lời thường | vì sao đặt vậy |
|---|---|---|
| `finetuning_type: lora` + `lora_rank: 8` | chỉ gắn thêm ma trận nhỏ, không sửa mô hình gốc | rẻ, và kết quả gói gọn trong tệp 59,9 MB |
| `freeze_vision_tower: true` | **đóng băng phần mắt**, chỉ dạy phần miệng | dạy *"nói gì"*, không dạy *"nhìn thấy gì"* — phần nhìn của Qwen vốn đã tốt |
| `quantization_bit: 4` | nén tham số gốc để vừa bộ nhớ card | vừa rẻ vừa **nhanh hơn** bản không nén ở bài này (§4.2b) |
| `cutoff_len: 2560` | cắt đầu vào dài quá 2.560 token | đo được: 0% mẫu bị cắt, nhưng chỉ dư 31 token nên nâng từ 2048 lên cho chắc |
| `batch_size: 4` × `grad_accum: 4` | gom 16 mẫu rồi mới chỉnh tham số một lần | card không đủ chỗ cho 16 mẫu cùng lúc, nên gom làm bốn đợt |
| `learning_rate: 1e-4` + `cosine` | bước chỉnh ban đầu to, nhỏ dần về cuối | quy ước chuẩn của LoRA; đuôi nhỏ dần nên kết thúc êm (§4.6) |
| `num_train_epochs: 2` | đi hết dữ liệu hai vòng | một vòng chưa đủ, ba vòng bắt đầu học thuộc |
| `save_steps: 200` | ghi bản chụp mỗi 200 bước ra Google Drive | mất máy thì mất tối đa 200 bước ≈ 34 phút |
| `seed: 101` (và `202`) | ấn định mọi lựa chọn ngẫu nhiên | chạy hai hạt giống để biết **nhiễu giữa hai lượt train** là bao nhiêu |

**Tham số huấn luyện được: 14.966.784** (0,48% của 3B). Đây là con số dùng làm phép kiểm cơ
học mỗi lượt — sai số này là cấu hình đã trượt.

### 4.1b Vì sao gần như không có chính quy hoá — và một suy luận SAI đã bị rút

Cấu hình chỉ có **`lora_dropout: 0.05`**. Không weight decay, không early stopping, và
`val_size: 0.0` · `do_eval: false` — tức **không có tập kiểm chứng nào**.

⛔ **Lập luận SAI, rút 18/8:** *"tỉ lệ dữ liệu/tham số ~4:1 nên đây là chế độ thiếu năng lực,
quá khớp không phải mối lo"*. Làm phép chia thì ngược hẳn: **14.966.784 tham số / 64.567 mẫu
= 232 tham số cho mỗi mẫu**. Tham số **nhiều hơn** mẫu, không phải ít. Đây là chỗ phát biểu
về năng lực mà không chia.

**Lý do thật, dựa trên số đo chứ không trên lập luận về năng lực:**

| bằng chứng | số |
|---|---|
| loss đuôi **không tiến về 0** | **0,4486** và **0,4467** ở hai hạt giống độc lập, lệch 0,4% |
| điểm **ngoài mẫu** ổn định | 59,12% và 59,64% trên 4.462 bước chưa từng thấy, chênh 0,52 pp |
| phần trọng số được động vào | **0,397%** · tháp thị giác và bộ chiếu **đóng băng** |
| số lượt duyệt | **2** |

Mô hình học thuộc thì loss huấn luyện phải tiến về 0 và hai lượt độc lập phải phân kỳ ngoài
mẫu. Cả hai đều không xảy ra. ⇒ **quá khớp không xảy ra — đó là quan sát, không phải giả định.**

**`val_size: 0.0` là quyết định có chủ ý**, khoá ở `report/106` mục sửa đổi (o): *"dùng bản
cuối 2 lượt duyệt cho mọi nhánh, CẤM chọn điểm lưu theo điểm trên tập kiểm"*. Có early
stopping thì mỗi nhánh dừng ở một bước khác nhau, và câu hỏi *"S2 hơn S1 vì thành phần hay vì
nó tình cờ dừng ở chỗ đẹp hơn?"* sẽ không trả lời được. Đánh đổi: mất chút điểm tuyệt đối,
đổi lấy **phép so sạch** — mà bài này là bài về ablation.

⚠️ **Từ đây không được đổi siêu tham số nào.** S1 đã train xong hai hạt giống bằng cấu hình
này; đổi cho S2 là hiệu `S2 − S1` lẫn cả phần do đổi cấu hình, không nhánh nào tách được. Ô
kiểm vàng (`run_on_colab.md` A.2b) sinh ra để chặn đúng điều đó.

### 4.2 Ba chốt kỹ thuật, mỗi cái từng suýt tốn tiền

**(a) `enable_liger_kernel: true` — nhanh 3%, và không đổi phép tính.**

Chứng minh bằng số chứ không bằng lập luận: cùng 200 mẫu, cùng `seed 101`, loss trùng tới
**chữ số thứ tư**:

| bước | không liger | có liger |
|---|---|---|
| 1 | 3,189 | 3,188 |
| 2 | 3,014 | 3,015 |
| 3 | 2,597 | 2,595 |
| 4 | 2,545 | 2,545 |

⇒ Bật được mà **không phải ghi mục sửa đổi vào bản đăng ký trước**.

**(b) QLoRA 4-bit NHANH HƠN bf16 ở bài này** — 10,70 vs 14,76 s/bước. Ngược trực giác.

Lý do: 3B đủ nhỏ để khâu giải nén không thành nút thắt, còn 4,3 GB tiết kiệm được lại rơi
đúng chỗ nghẽn là **activations**.

**(c) Chỗ ngốn bộ nhớ là BẢNG LOGITS, không phải trọng số.**

Bằng chứng: cấu hình P4 (bf16 + checkpointing) tràn bộ nhớ, nhưng P4 **+ liger** thì chạy được.
Liger gộp cross-entropy nên khỏi phải dựng bảng `151.936 từ vựng × ~1.500 token × 4 mẫu` ở fp32.
Đây cũng là lời giải cho việc card L4 24 GB chết ở **mọi** biến thể bf16.

**(d) `preprocessing_num_workers: 8` — mã hoá token 42 phút thay vì 2,5 giờ.**

`datasets.map` mặc định chạy **một tiến trình** (đo được `ps` cho 165% CPU trên 12 lõi).
Nhanh 3,6 lần, và **không đổi dữ liệu ra** nên cũng không phải ghi mục sửa đổi.

### 4.3 Chọn máy

| card | s/bước | một lượt | tiền/lượt |
|---|---|---|---|
| Colab **L4** 24 GB | 31,26 | 69,5 giờ | ~$11 |
| Colab **A100-SXM4-40GB** | **10,38** | **23,3 giờ** | ~$12 |

A100 nhanh 2,92× mà chỉ đắt hơn **19%** → chọn A100. Hạn nộp còn 7 tuần nên chọn theo thời gian.

⛔ L4 **kịch trần bộ nhớ**: tắt gradient checkpointing không mua được gì (31,37 vs 31,26), bỏ
4-bit thì tràn ở cả ba cách thử. OOM ở forward đầu tại **21,54/22,03 GB** — chật chỗ thật.

**Đổi card không đổi kết quả:** cùng `seed 101`, loss 20 bước trùng ba chữ số
(L4 `2,036/0,9686/0,8635/0,9553` · A100 `2,040/0,9679/0,8635/0,9547`), `total_flos` y hệt.
Dùng được cho phần "tái lập khi đổi máy".

### 4.4 Bài học đo đạc

> **Mỗi biến thể chỉ đổi MỘT thứ.** Bản thăm dò đầu ghép hai thay đổi (bỏ 4-bit + tắt
> checkpointing) nên tràn bộ nhớ trước khi trả lời được câu nào.

> **Thăm dò trên mẫu ĐẦU TẬP không kết luận được về bộ nhớ.** Cấu hình P10 chạy ngọt trên
> mẫu thường nhưng chết trên 200 mẫu **dài nhất** của s2 (2.017 token vs trung vị 1.524).
> 12 phút thăm dò cứu một lượt train 20 giờ.

Tổng thăm dò: ~3,5 đơn vị cho 10 phép đo trên 2 card. Rẻ hơn một lần chọn sai rất nhiều.

### 4.5 Thực tế chạy: sáu lần mất máy ảo

Tài khoản dùng **đơn vị trả trước, không có `background execution`** → mỗi lần trình duyệt
hoặc máy ngủ là mất máy ảo.

| lần | mất | ghi chú |
|---|---|---|
| 10/8 | **42 đơn vị + 8 giờ** | chưa có cơ chế cất Drive |
| 11/8 | 3 phút | đã có cơ chế cất |
| 12/8 ×2 | 30 + 27 phút | |
| 12/8 tối | 24 phút | phép thử "gập nắp mang máy đi" **thất bại** |
| 13/8 | 46 phút | cách đích 192 bước |

**Cộng dồn ~14 giờ, ~70 đơn vị** (~$7) trên tổng ~190 đơn vị đã tiêu.

Thiết kế cứu được: **ghi thẳng Drive, đồng bộ mỗi 5 phút, nối tiếp từ điểm lưu.** Lần đầu
mất 8 giờ; sau khi có cơ chế, lần tệ nhất mất 46 phút.

Ba chi tiết kỹ thuật của cơ chế nối tiếp:

- **Không khai `resume_from_checkpoint`.** LLaMA-Factory chỉ tự dò điểm lưu gần nhất **khi
  trường đó còn trống** (`hparams/parser.py`, điều kiện `is None`). Điền bất cứ giá trị nào,
  kể cả `"auto"`, sẽ **tắt đúng cái nó định bật**.
- **Khâu nhảy qua 1.600 lô chỉ tốn ~17 giây** (94 lô/giây) → toàn bộ giá của một lần đứt nằm
  ở **mã hoá token**, không ở khâu nhảy.
- **Kiểm bằng `grep "Resuming training from"` NGAY lúc khởi động.** Không nhận ra điểm lưu
  thì cái giá là mã hoá token lại rồi train lại từ bước 0.
  ⚠️ Nhưng grep trống ngay sau khi phóng là **báo động giả** — dòng đó in sau ~40 giây nạp
  thư viện. Hỏi ba thứ trước khi giết tiến trình: `getsize(log)` · `ps -p <PID>` · `tail -30`.

### 4.6 Hai lượt s1 đã xong — và cách chứng minh không mất bước nào

| lượt | xong | số lần mất máy ảo | `total_flos`/bước | loss đuôi-20 |
|---|---|---|---|---|
| **s1 / seed 101** | 13/8 22:43 | **6** | 513.164 GF | 0,4486 |
| **s1 / seed 202** | 17/8 00:40 | **3** | 513.229 GF | 0,4467 |

Cả hai đủ **8.072 bước / 2 lượt duyệt**. `adapter_model.safetensors` 59,9 MB.

**Phép kiểm "cả 8.072 bước chạy thật, không mất cũng không lặp":** hai lượt có **số lần đứt
khác hẳn nhau (6 vs 3)** mà `total_flos`/bước khớp **0,013%**. Nếu khâu kế toán hỏng sau mỗi
lần chạy tiếp thì hai lượt phải lệch nhau theo số lần đứt. Chúng không lệch.

⛔ **Bản 16/8 ghi `total_flos` = 3.857.778.344 GF và nói nó "khớp ngoại suy từ thăm dò trong
0,32%". SỐ ĐÓ SAI, ĐÃ RÚT.** Đọc lại `trainer_state.json` **và** `all_results.json` của lượt
101: cả hai cho **4.142.257.957 GF**. Ngoại suy từ thăm dò lệch **7,7%**, không phải 0,32% —
vì lượt thăm dò chạy `max_samples`, tức lấy **phần đầu tập chưa trộn**, nên độ dài chuỗi
không đại diện.

Kết luận cũ vẫn đứng, nhưng **bằng chứng phải đổi** sang phép so hai hạt giống ở trên. Nó
chặt hơn, và quan trọng hơn là **không vòng tròn**: bản cũ lấy thăm dò làm chuẩn để kiểm lượt
thật, trong khi thăm dò chạy trên tập con thiên lệch.

⚠️ Đính chính kèm: **`all_results.json` KHÔNG hỏng ở trường `total_flos`** — chỉ
`train_loss` / `train_runtime` / `*_per_second` hỏng sau resume (xem ngay dưới).

⛔ **Ba số trong `all_results.json` SAI sau resume, cấm trích:**
`train_loss 0,0151` (HF cộng loss chỉ từ lúc khởi động lại 272 bước rồi chia cho cả 8.072 —
số thật ≈ **0,447**, kiểm: 0,01505 × 8.072 ÷ 272), `train_runtime`, và cả hai `*_per_second`.
**Mọi số HF chia cho `elapsed` đều hỏng sau resume.** Dùng `trainer_state.json`.

Đường loss: 1,103 (200 bước đầu, học định dạng) → 0,611 (bước 2.000) → nhịp tụt đúng ranh
giới lượt duyệt 2 tại bước 4.036 → 0,455 ở đuôi. Đuôi phẳng vì `lr` đã xuống 2,28e-07, đúng
sách của lịch cosine — **không phải chững vì hỏng**.

⚠️ Nhịp tụt ở epoch 2 **không phải bằng chứng khái quát tốt hơn** — gặp lại dữ liệu lần hai
thì loss huấn luyện giảm là đương nhiên. Và **đừng ngoại suy loss**: dự báo sàn 0,548 đã bị
rút vì mới bước 5.100 đã xuống 0,465.

---

## 5. Thước đo executability

### 5.1 Vì sao không dùng cách thông thường

Đã thử và đã bỏ, có số:

| cách | kết quả | vì sao gãy |
|---|---|---|
| so chuỗi | kết oan 97,5% câu diễn đạt khác | "search bar" ≠ "magnifying glass" |
| so embedding | **AUC 0,336** trên 51 ca thật | đo gần-**chủ đề**: `inbox↔outbox` = 0,76 **cao hơn** `search↔magnifying glass` = 0,55 |
| bơm lỗi kiểu cũ | AUC 1,000 — **hằng đẳng thức** | bộ bơm gọi chính hàm của thước rồi dán lại |

Không ngưỡng nào tách được "cùng nút" khỏi "khác nút" khi tín hiệu là độ gần ngữ nghĩa.
Bài *"Do GUI Grounders Truly Understand UI Elements?"* (**Findings EACL 2026**) còn cho thấy
cho thấy độ chính xác đo trên MỘT câu tốt nhất mỗi phần tử là thổi phồng — nên đây không
phải bệnh riêng. ⛔ (Cách mô tả cũ *"đổi diễn đạt làm bộ trỏ trượt 84%"* **đã bị rút 18/8**,
xem §6.7.)

⇒ Đổi hẳn câu hỏi: **không hỏi "câu có giống câu chuẩn không", hỏi "câu có dẫn tới đúng nút không".**

### 5.2 Luật chấm (`harness/metric_exec.py`, 247 dòng)

```python
executable = action_ok AND toggle_ok AND hit_voronoi
```

**Ba điều kiện nối bằng AND, không phải ba phương án chọn một.** Chỗ này bản 16/8 tả sai:
`hit_voronoi` **không đứng thay** `hit_disk` mà **bao gồm nó** — dòng đầu của
`hit_voronoi()` là `if not hit_disk(...): return False`. Nên Voronoi là bản **siết chặt** của
luật dung sai quy ước, không phải luật đối lập. Hệ quả khi viết bài: không được trình hai
luật như hai lựa chọn ngang hàng.

**`action_ok`** — gọi đúng **loại** thao tác. Gộp mọi cách nói của cùng một cú chạm về một lớp:

```python
ACTION_MAP = {"tap","click","press","select","choose","touch",
              "open","launch","go","navigate","visit","view"   → "tap",
              "type","enter","input","fill","write"            → "type",
              "scroll","swipe","drag"                          → "scroll", …}
```

Bảng cũ tách `tap` khỏi `open`/`go to` nên **bác oan 28,6%** số cặp (đo trên 91 cặp câu thật)
— đúng bệnh của thước so chuỗi, chỉ đổi vỏ.

**`toggle_ok`** — bác câu nhắm **trạng thái ngược**. Đây là chỗ duy nhất kênh toạ độ mù: nút
"Bật thông báo" và "Tắt thông báo" **cùng một vị trí chạm**.

```python
TOGGLE_PAIRS = [("on","off"), ("enable","disable"), ("show","hide"),
                ("mute","unmute"), ("expand","collapse"),
                ("check","uncheck"), ("select","deselect"), ("start","stop")]
```

⛔ Đã thử lớp trái nghĩa **WordNet** rồi bỏ: chỉ bắt thêm 3 ca nhưng đẻ mâu thuẫn giả vì đa
nghĩa (`set↔rise`, `enter↔leave`, `top↔side`) — đến mức có **câu gold tự bác chính nó**.
Giữ bảng tay, khai thẳng phần còn mù.

**`hit_voronoi`** — phần lõi, xem dưới.

### 5.3 Voronoi: vì sao "trong đĩa 14%" là quá dễ dãi

⚠️ **Trước hết, "đĩa" là tên gọi sai — mã dựng một HÌNH CHỮ NHẬT.** Bản 16/8 tả nó là đĩa
Euclid, nhưng `hit_disk` viết thế này:

```python
return abs(pred[0]-gold[0]) <= tau*w  and  abs(pred[1]-gold[1]) <= tau*h
```

Hai trục xét **riêng**, và mỗi trục chia cho **cạnh của chính trục đó**. Trên ảnh 1080×2400
với `tau = 0,14`:

| trục | dung sai |
|---|---|
| ngang | 0,14 × 1080 = **151 px** |
| dọc | 0,14 × 2400 = **336 px** |

⇒ **Dung sai dọc rộng gấp 2,2 lần dung sai ngang.** Vùng chấp nhận là hình chữ nhật cao,
không phải hình tròn. Đây là cách AITW/AndroidControl vẫn làm (ngưỡng 14% *cạnh màn*), nên
không phải lỗi — nhưng gọi nó là "đĩa" thì tả sai dụng cụ, và trên giao diện dọc thì cái sai
đó nghiêng về phía **dễ dãi**.

Đo được: **63,2% số bước có nút KHÁC nằm trong vùng đó**. Nghĩa là câu trỏ nhầm sang nút cạnh
vẫn được cho qua.

Vá: **trúng chỉ khi nút gold là nút GẦN NHẤT với điểm bộ trỏ**, trong số mọi phần tử trên màn.

Ví dụ số thật từ phần tự kiểm của `metric_exec.py`:

```
màn 1080×2400 · gold = (854, 2275) · nút cạnh = (1010, 2275)   [cách gold 156 px]
điểm bộ trỏ  = (960, 2275)   → cách gold 106 px, cách nút cạnh 50 px

đĩa 14%  : TRÚNG   ← 106 < 151, cho qua (SAI, dễ dãi)
Voronoi  : TRẬT    ← có nút gần hơn, bác (ĐÚNG)
```

**Và đây là một ca THẬT trong tập kiểm, không phải ví dụ dựng** — bước `18195/4`, app
Decathlon, 69 phần tử trên màn, gold = (199, 623):

| | câu | bộ trỏ trả về | lệch |
|---|---|---|---|
| người | `Click on the product nature option` | (188, 624) | **11 px** |
| S1 | `Select the Gender option` | (188, 492) | **131 px** |

Câu của S1 gọi tên **một phần tử khác hẳn** — "Gender" thay vì "product nature". Hai luật phán
quyết ngược nhau:

```
đĩa 14% : |dx| = 11 ≤ 151 ✅   và   |dy| = 131 ≤ 336 ✅   → CHO QUA
Voronoi : có phần tử khác gần điểm (188, 492) hơn là nút gold  → BÁC
```

⇒ Luật dung sai quy ước sẽ **cho điểm một câu gọi sai tên nút**, chỉ vì màn hình dọc nên dung
sai dọc rộng tới 336 px — thừa sức nuốt trọn khoảng cách giữa hai dòng tuỳ chọn xếp chồng nhau.
Voronoi bác đúng. Trên toàn tập, **401 bước** rơi vào đúng tình huống này ở nhánh S1.

⚠️ Nhưng nó cắt cả hai chiều, và phải khai: cũng có ca Voronoi bác **oan**. Đo được **97 bước**
mà câu người viết qua được còn câu S1 bị Voronoi bác — trong đó có ca S1 sai thật (`18225/1`:
người nói *"to do tasks option"*, S1 nói *"send reminder option"*, lệch 278 px, bác đúng), nhưng
cũng có ca chỉ lệch một chút ở vùng nút dày. Đây là một phần lý do trần dừng ở **75,7%** chứ
không phải 100%.

Danh sách nút lấy từ cây trợ năng: mọi phần tử `is_visible_to_user`, bỏ phần tử nhỏ hơn
8×8 px, bỏ cửa sổ hệ thống. Đo trên tập kiểm: trung vị **68 nút mỗi màn**, tứ phân vị 40–117,
cao nhất 269. Màn càng dày nút thì Voronoi càng chặt.

**Một chi tiết tinh — HẠT của ô Voronoi là ĐIỂM CHẠM, không phải tâm nút.** Bản 16/8 tả
không rõ chỗ này. Toạ độ gold là **điểm người thật chạm**; mã lấy chính điểm đó làm hạt và so
khoảng cách từ điểm bộ trỏ tới nó, **không** lấy tâm của phần tử chứa nó.

Vì sao phải làm vậy: nếu so theo tâm hộp thì hộp của chính nút gold có tâm "gần hơn" điểm
chạm, và nó tự đánh rớt câu đúng — đo được **kết oan 59%** số câu cùng nghĩa. Xử đúng bản
chất: **mọi hộp CHỨA điểm gold đều là nút gold**, loại chúng khỏi danh sách đối thủ.

Đường lui khi danh sách nút chỉ có tâm mà không có hộp: xoá mọi tâm nằm trong bán kính
**24dp ≈ 63 px** quanh điểm chạm. ⚠️ Ngưỡng này ban đầu được biện minh bằng chuẩn Material
Design *"hai nút riêng phải cách nhau ≥48dp"* — **lập luận đó đã bị rút**: kiểm trên hộp thật
thì **286 cặp** hộp có tâm cách nhau dưới ngưỡng lại có IoU = 0, tức là phần tử **riêng biệt**
nằm sát nhau (phím bàn phím, dòng danh sách). Ngưỡng vẫn dùng nhưng chỉ vì kết quả ổn định
trong dải 12–28dp, **không phải vì có chuẩn thiết kế hậu thuẫn**.

**Hai giới hạn của Voronoi, đã ghi thẳng trong test:**
- inventory **nhiễu** (bộ dò trả hộp trùng lên chính nút gold) → khử trùng theo bán kính
- inventory **thiếu** (bỏ sót nút icon cạnh gold) → thước **không bác được**, câu sai vẫn lọt

⇒ *Voronoi chỉ chặt bằng đúng độ đầy đủ của bộ dò phần tử.*

### 5.4 Bộ trỏ

**UGround-V1-2B** (`osunlp/UGround-V1-2B`, ICLR 2025 Oral). Ba điều kiện **đặt ra** lúc chọn:

1. **Khác họ với mô hình bị chấm** — nếu cùng họ thì thước thiên vị
2. **Recipe huấn luyện không chứa AndroidControl** — nếu không thì giám khảo từng học đề thi
3. **Sai số trỏ phải đủ nhỏ** — đây là **cổng A**, xem §5.5

### ⛔ Điều kiện 1 và 2 KHÔNG THOẢ. Hai khẳng định cũ đã bị rút (16/8)

Từ 29/7 hồ sơ ghi cả hai là "đã xác minh". Tra lại tận nguồn thì cả hai **sai**:

| khẳng định cũ | thực tế | nguồn |
|---|---|---|
| "bộ trỏ khác họ mô hình" | UGround-V1-2B dựng trên **Qwen2-VL** — cùng dòng với Qwen2.5-VL-3B đang bị chấm | `score_run.py` nạp bằng `Qwen2VLForConditionalGeneration` |
| "recipe không có AndroidControl" | Bảng 1 liệt kê **AndroidControl 47K phần tử nhãn người**, cùng Widget Caption 41K · UIBert 16K · AITZ 8K | arXiv **2410.05243** Bảng 1 |

**Phần nào còn đứng, phần nào không:**

✅ **Không phải rò rỉ nhãn.** Họ lấy từ split **train** của AndroidControl; tập kiểm của ta
lấy từ split **test**. Hai split không chồng lấn ở mức **màn hình** — nên bộ trỏ chưa từng
thấy đúng những màn nó đang chấm.

⛔ **Nhưng còn một lời giải thích thay thế chưa loại được.** Bộ trỏ đã thấy **văn phong chú
thích** của chính kho này, mà S1 lại được dạy viết đúng văn phong đó. Một bộ trỏ giải mã văn
phong ấy dễ hơn sẽ **thổi S1 lên so với Base** vì lý do không liên quan gì tới chất lượng câu.
Sáu đòn phản biện ở §6.5 không loại được đúng đòn này.

**Cách duy nhất đóng nó:** chấm một lát ≥500 bước bằng bộ trỏ **đã xác minh sạch
AndroidControl**. Ứng viên đã tra: **UI-Venus-Ground-7B** (§7). Việc này **chưa chạy**.

⚠️ **Câu chữ khi viết bài.** Viết *"bộ trỏ không được huấn luyện trên AndroidControl"* nếu và
chỉ nếu đúng cho bộ trỏ đang nói. **Cấm** viết *"chưa từng thấy màn hình di động"* cho bất kỳ
bộ trỏ nào — chúng đều dùng Widget Captioning / UI RefExp / RICO, đều là kho Android.

> **Bài học đắt nhất của cả dự án về mặt tra cứu:** chữ *"đã xác minh"* trong ghi chú của
> chính mình **không phải bằng chứng**. Cả hai khẳng định sống 18 ngày, đi vào bản thảo bài
> báo, và bị lật bởi một lần mở đúng Bảng 1 của bài gốc.

### Chi tiết vận hành

Câu nhắc **bê nguyên văn từ thẻ mô hình chính chủ**. Tự chế câu khác (nhất là bằng tiếng Việt)
sẽ làm nó trỏ tệ đi, rồi cổng A rớt vì lý do sai và mình đổ oan cho bộ trỏ.

⚙️ **`use_cache=True` nói THẲNG, không để mặc định quyết.** `generation_config` của
UGround-V1-2B đặt `use_cache=False`, trên T4 điều đó làm 32 token mất **38,7 s** thay vì
**4,2 s** — chậm 9,3 lần cho một phép biến đổi bảo toàn kết quả. Đã kiểm chứ không suy luận:
50 bước chạy lại với cache bật cho toạ độ **trùng tuyệt đối 50/50**.

⇒ Chấm một nhánh từ **48 giờ xuống 5,6 giờ** ⇒ vừa hạn mức Kaggle T4 miễn phí ⇒ **khâu chấm
tốn 0 đồng**.

### 5.5 Cổng A — điều kiện tiên quyết của cả thước

Đường cong đo bằng dụng cụ thật (cây trợ năng + Voronoi):

| sai số bộ trỏ (% bề ngang) | tỉ lệ kết oan |
|---|---|
| 3% | **0%** |
| 5% | 7,5% |
| 8% | 24,1% |
| 13% | 55% |

⇒ Ngưỡng khoá trước: **sai số trung vị ≤ 3% bề ngang**. Không phải "trúng 80%".

**Đo thật: 0,7%** — qua cổng với biên rộng. Và xác nhận bằng dụng cụ thật: dưới 3% thì 100%
trúng Voronoi (n=188).

⚠️ **Hai công thức sai số, đừng so thẳng với nhau:**
- `ground_pilot.py`: `hypot((px−gx)/W, (py−gy)/H)` — lệch dọc chia cho H=2400 nên **nhẹ đi
  2,2 lần** so với lệch ngang
- cổng A: `dist(p,g)/W` — khoảng cách pixel thật chia bề ngang

Trên cùng dữ liệu, cách sau ra số lớn hơn **1,63 lần**. Con số "trung vị 8% cạnh" trong hồ sơ
cũ **đã bị rút** vì nó tính trên chỉ những ca bộ trỏ **đã trúng** — loại sạch mọi lần trượt.

### 5.6 Thống kê

**Câu hỏi mà cả mục này trả lời:** đo được 59,1% và 47,6% — làm sao biết chênh lệch đó là thật
chứ không phải may rủi của việc chọn tập kiểm? Bốn công cụ, đều đã giải nghĩa ở **§A**: khoảng
tin cậy · ghép cặp McNemar · bootstrap theo cụm · MDE.

- **Ước lượng điểm là micro** (`tổng đúng / tổng bước`), không phải trung bình các app
- **Chỉ khoảng tin cậy mới bootstrap theo cụm-app** — màn cùng app không độc lập
- G = **1.091 cụm**, hiệu dụng (Kish) = **454,3**
- Mọi nhánh chấm trên **cùng 4.462 bước** ⇒ phải đọc **ghép cặp (McNemar)**, không đọc hai
  mẫu độc lập. SE ghép cặp 0,64–0,75 pp vs 0,94 pp độc lập.

### MDE: số ĐOÁN là 2,7–4,5 pp, số ĐO là **2,2 pp**

MDE = độ chênh nhỏ nhất mà thí nghiệm này còn đọc được. Nó quyết định luật đọc kết quả, nên
phải là số **đo**, không phải số suy.

| | cách có | giá trị |
|---|---|---|
| ước cũ (suy) | lấy SE ghép cặp rồi **đoán** hệ số nở do cụm 1,5–2× | 2,7–4,5 pp |
| **đo thật** | bootstrap **theo cụm** trên hiệu ghép cặp, SE 0,79 pp | **2,2 pp** |

Chỗ suy sai: hệ số nở do cụm thật ra chỉ **1,10×**, không phải 1,5–2×. Lý do hợp lý — hiệu
ghép cặp *triệt tiêu* phần lớn biến thiên giữa các app, vì cùng một app xuất hiện ở cả hai
nhánh và mức khó của nó trừ đi nhau.

⚠️ **Hệ quả nghiêm trọng cho luật đã đăng ký trước.** `report/106` gọi dải **4–9 pp** là
*"không kết luận được"*. Với MDE thật 2,2 pp, luật đó sẽ **vứt bỏ một hiệu ứng thật** có
khoảng tin cậy loại trừ 0 ở p<0,001. Đã ghi **mục sửa đổi (t)** vào `report/106` **trước khi
chấm bất kỳ nhánh xử lý nào** — thứ tự đó là điều kiện để việc sửa luật không thành sửa luật
theo kết quả.

### 5.7 Luật chấm có bền không — chấm lại dưới năm luật khác nhau

Đòn phản biện hiển nhiên: *"các anh tự chọn luật chấm, đổi luật thì bảng đổi"*. Trả lời bằng
cách chấm lại **từ tệp thô** (không gọi lại bộ trỏ, nên miễn phí) dưới năm luật, trên 698 bước:

| luật chấm | trần | S1 − Base |
|---|---|---|
| chữ nhật 14% (quy ước AITW) | 80,2% | **+12,6** |
| Voronoi (luật đang dùng) | 82,2% | **+13,0** |
| chữ nhật siết còn 7% | 74,2% | **+11,7** |
| chữ nhật siết còn 3% | 56,6% | **+9,5** |
| chỉ cần đúng hộp chứa | 82,2% | **+13,0** |

**Trần trôi từ 56,6 đến 82,2 — nhưng thứ tự ba nhánh không đổi ở luật nào, và khoảng chênh
S1−Base nằm gọn trong 9,5–13,0 pp.** Nghĩa là: con số **tuyệt đối** phụ thuộc luật (phải khai),
còn **kết luận so sánh** thì không.

Đây là lá chắn mạnh nhất của chương đo lường, vì nó biến một lựa chọn thiết kế đáng ngờ thành
một dải đã đo. Mã: `harness/rule_sensitivity.py`.

---

### 5.8 Sàn của thước — đầu kia của cái thước

Trần trả lời *"điểm cao nhất một câu có thể đạt"*. Sàn trả lời câu ngược lại: **một câu KHÔNG
mang thông tin gì thì được bao nhiêu điểm?** Thiếu nó thì con số 59,1% của S1 không đọc được —
không biết nó nằm ở đâu trên một cái thước chưa biết vạch số 0 nằm chỗ nào.

**Cách đo.** Ba nhánh đối chứng dựng bằng `harness/make_floor.py`, **luật đọc khoá trước khi
chấm**, chạy trên lát 800 bước (trần trên lát này 74,9%). Kaggle, 3 giờ, 0 đồng.

| nhánh | câu bị thay thành gì | điểm | KTC95 |
|---|---|---|---|
| `f1_trong` | `"Tap the button."` ở **mọi** bước — đúng ngữ pháp, 0 thông tin | **12,0%** | [9,7 – 14,4] |
| `f3_lechman` | câu **thật do người viết**, nhưng của **bước khác** — đúng văn phong, sai màn | **6,1%** | [4,5 – 7,9] |
| `f2_khongten` | giữ mệnh đề vị trí, **xoá tên phần tử** | 68,0% toàn lát · **61,1%** phần bị đụng | — |

**① Sàn 12,0% ⇒ dải dùng được là 62,9 điểm**, không phải 74,9. Trên lát này Base đứng ở
**58,3%**, S1 ở **74,4%**. Câu *"thước không suy biến về sàn"* từ chỗ là lập luận nay có một
phép đo chống lưng.

⛔ **Một suy luận sai đã bị bác bằng số.** Phản biện dự đoán sàn ≈ 40%, suy từ chỗ **40,4% số
bước cả ba nhánh cùng trúng** kể cả mô hình chưa huấn luyện. Sàn thật là 12,0% ⇒ những bước ấy
**dễ KHI CÓ CÂU THẬT**, không dễ vô điều kiện. **Suy sàn từ tỉ lệ đồng thuận là suy sai** — hai
đại lượng khác nhau.

**② `f3` (6,1%) THẤP HƠN `f1` (12,0%), hai KTC không chồng lấn.** Đây là chỗ đắt nhất của cả
mục. Giả thuyết "nhiễm văn phong" nói bộ trỏ thưởng cho câu **đúng giọng chú thích** bất kể nội
dung — nếu vậy `f3` phải ăn **cao**, vì nó là câu người thật, văn phong hoàn hảo, độ dài khớp
(34 vs 35 ký tự). Nó ăn **thấp nhất trong mọi thứ đã đo**, dưới cả câu vô nghĩa.

Giải thích cơ học: câu **sai** dẫn bộ trỏ đi lạc sang phần khác của màn, còn câu **rỗng** để nó
rơi về tiên nghiệm thị giác yếu — lạc có định hướng tệ hơn không có định hướng. Cộng với phép
*"cùng nội dung khác văn phong"* (+0,9…+1,9 pp, không ý nghĩa) ở §6.7, giả thuyết văn phong nay
bị đánh từ **hai hướng độc lập**.

**③ Gọi tên đắt gấp 8 lần chỉ chỗ.** Hai phép cắt trên hai quần thể gần bằng nhau nên so trực
tiếp được:

| bỏ gì, giữ gì | n | McNemar | tụt |
|---|---|---|---|
| bỏ **TÊN**, giữ vị trí (`f2`) | 193 bước | b=58 c=3, χ²=47,8, **p<0,001** | **−28,5 pp** |
| bỏ **VỊ TRÍ**, giữ tên (`p3_nopos`) | 198 bước | b=8 c=1, p=0,046 | −3,5 pp |

⇒ thước **chủ yếu đo việc GỌI ĐÚNG TÊN**, không phải việc chỉ chỗ ⇒ chữ **"Element
Identification"** trong nhan đề bài là đúng. Ngưỡng khoá trước khi chấm: *tụt ≥10 pp thì n=193
thừa sức phát hiện*.

⚠️ **Con số của bài là −28,5 pp trên PHẦN BỊ ĐỤNG, không phải −6,9 pp toàn lát.** `f2` chỉ đụng
24,1% số bước (những bước mà câu chuẩn có tên để mà xoá), nên số toàn lát bị **pha loãng 4,15
lần**. Đây đúng là cái bẫy đã mắc một lần ở phép diễn đạt lại (§6.7) — hiệu ứng đo trên tập con
thì phải chia lại theo tập con.

**④ Vì sao sàn không chỉ là một con số.** Trước khi có nó, `S1 − Base` phải gánh **hai vai**:
vừa là kết quả mô hình, vừa là bằng chứng rằng thước phân giải được sự khác nhau. Một mẩu bằng
chứng không gánh nổi cả hai khi chính nó đang bị nghi ngờ. Cặp *"câu người vs câu vô nội dung"*
có **thứ tự biết trước** mà **không dính mô hình nào của ta** ⇒ chứng minh khả năng phân giải
**độc lập**, giải phóng `S1 − Base` để chỉ còn là kết quả. **Sàn là mảnh ghép tách hai đóng góp
ra khỏi nhau.**

Đọc lại số bằng `python3 harness/doc_san.py`. Chi tiết: `report/113` mục I.

---

## 6. Kết quả — đọc thế nào

### 6.1 Bảng chính

| | executable | KTC95 | hit_voronoi | action_ok | đĩa 14% |
|---|---|---|---|---|---|
| **Human (trần)** | **75,7%** | [74,1 – 77,3] | 75,8% | 100%¹ | 84,3% |
| **S1 seed 101** | **59,1%** | [57,3 – 60,8] | 60,2% | 94,4% | 69,2% |
| **Base** (chưa train) | **47,6%** | [45,9 – 49,3] | 48,9% | 96,5% | 57,6% |

¹ `pred` chính là câu chuẩn nên `action_ok` đúng theo định nghĩa; điểm rút gọn còn đúng phần
định vị. Đó là ý nghĩa của trần.

**Hạt giống thứ hai cho cùng kết luận.** S1 hạt giống 202 hơn Base **+12,03 pp** (hạt 101:
**+11,52 pp**), trung bình hai hạt **59,4%** — đây là con số dùng trong abstract bài FAIR.
Nhiễu giữa hai lượt train chỉ **0,52 pp** ⇒ tín hiệu gấp **22 lần** nhiễu.

**Hai lượt đồng ý tới đâu:** κ = **0,867** trên toàn tập. Nhưng con số đó bị thổi lên bởi những
bước mà **cả hai lượt viết câu giống nhau** — đồng ý ở đó là đương nhiên. Tính riêng **1.652
bước hai lượt viết KHÁC nhau**, κ **có điều kiện = 0,650**. ⚠️ **Luôn trình κ kèm điều kiện** —
trình mỗi 0,867 là một trong bảy lỗi câu chữ bắt được ở §11.1.

### 6.2 Cách đo trần — mẹo không tốn GPU

Trần = điểm khi đưa **chính câu người viết** cho bộ trỏ. Không cần sinh câu, nên **không cần
GPU**: dựng tệp `preds` với `pred = gold_instruction` rồi chấm như mọi nhánh.

```python
out.append({"episode_id": r["episode_id"], "step_id": r["step_id"],
            "pred": g, "raw": g, "run": "ceiling_human",
            "action": r["action"], "gold_instruction": g})
```

⛔ **Con số trần 70,0% ĐÃ BỊ RÚT.** Nó đo trên **mẫu con 300 bước**; chấm đủ 4.462 bước ra
**75,7%** — cao hơn **5,7 điểm** và **nằm ngoài mép trên** khoảng tin cậy cũ [64,5–75,3].
KTC hẹp từ ±5,4 xuống **±1,6**.

Kéo theo hai số cũng phải rút: room `485 bước / 10,9 pp` → **741 bước / 16,6 pp**;
"S1 đạt 84,4% của trần" → **78,1%**.

> **Bài học:** mẫu con 300 bước cho một điểm ước lượng lệch 5,7 điểm và một KTC không phủ
> giá trị thật. Số nào đi vào bảng chính thì đo trên **toàn tập**, nhất là khi đo lại chỉ
> tốn 5,6 giờ máy miễn phí.

### 6.3 Ghép cặp (McNemar) — đều p < 0,001

| | Δ | b | c | χ² |
|---|---|---|---|---|
| S1 − Base | **+11,5 pp** | 284 | 798 | 243,2 |
| Human − S1 | **+16,6 pp** | 102 | **843** | 579,5 |
| Human − Base | **+28,1 pp** | 102 | 1.357 | 1.077,8 |

`b` = Base trúng mà S1 trượt · `c` = S1 trúng mà Base trượt.

Dòng giữa quan trọng nhất: **843 bước mà câu người định vị được còn S1 thì không** — đó
chính là vùng nhánh S2 có thể ăn.

**MDE ghép cặp 1,8–2,1 pp** chưa hiệu chỉnh cụm; hiệu chỉnh cụm rồi thì **đo được 2,2 pp**
(§5.6 — con số "ước 2,7–4,5" là số đoán và đã bị thay). So với MDE chiếu cũ 3,9–6,6 pp thì đây
là cải thiện lớn: **S2 chỉ cần lấy khoảng 13% room** để đọc được, trước tính 40–60%.

### 6.4 SFT thực sự dạy được gì — bốn ví dụ thật

Lấy từ 798 bước S1 trúng mà Base trượt:

```
gold : Click on the profile icon at the top right of the screen
S1   : Click on the profile icon at the top right corner of the screen
Base : To set YouTube video downloads over Wi-Fi only, tap on your profile icon at the
       top right corner of the screen and select "Settings." Then navigate to the
       "Downloads" section and choose "Wi-Fi Only."
```

```
gold : Click on the filter icon at the bottom right of the screen
S1   : Click on the filter option at the bottom right corner of the screen.
Base : Click on the heart icon next to the Kalenji shoes to add them to your cart.
```

```
gold : Click on Knoxville
S1   : Click on Knoxville
Base : Click on the three dots next to Knoxville to access more options and proceed
       with reading the local news.
```

Thấy rõ hai kiểu hỏng của Base: **(a) trả lời cả kế hoạch thay vì một bước** (ví dụ 1),
**(b) lạc sang bước khác** (ví dụ 2, 3).

⇒ **Thứ SFT dạy được là "bám đúng bước hiện tại", không phải khả năng viết tiếng Anh.**
Base viết câu tiếng Anh tốt, đúng khuôn, gọi tên nút cụ thể — mốc so **sạch**, không lẫn với
chuyện "không theo khuôn".

Con số hậu thuẫn: độ dài trung vị câu **Base 70 ký tự · S1 33 · người 34**. S1 học được đúng
độ dài của người.

### 6.5 Năm đòn phản biện — không đòn nào lật được "S1 hơn Base"

| đòn | phản bác |
|---|---|
| "chỉ là bắt chước **phong cách**" | Base cũng mở đầu bằng `click` **84%** số câu; động từ chạm 86,0% vs 87,5% — gần như nhau |
| "`action_ok` gánh hết" | bỏ điều kiện đó vẫn **+11,3 pp**. Và Base gọi đúng thao tác **nhiều hơn** (96,5% vs 94,4%) |
| "chỉ thắng ở một **loại bước**" | thắng ở cả hai nhóm: **+15,0** và **+11,0** |
| "chỉ thắng ở **màn dễ**" | thắng ở cả ba mức độ khó: **+12,7 / +9,4 / +12,3** |
| "vài **app** kéo cả bảng" | theo cụm: thắng **395**, hoà 565, thua **131** |

⚠️ Đòn về **độ dài** đáng nói riêng: thước có thiên vị câu dài **+5,4 pp** — nhưng thiên vị
đó **nghiêng về Base** (Base dài 70, S1 dài 33). S1 thắng **dù chịu bất lợi** ⇒ kết luận mạnh hơn.
Và thiên vị này **không phải quy luật chung của thước**: trong Base, câu dài lại **kém hơn 1,4 pp**.
Phải đo riêng cho từng nhánh.

### 6.6 Ba lát cắt chẩn đoán

**(a) Lợi thế sân nhà KHÔNG xuất hiện.** Đây là đòn phản biện tự khai nặng nhất từ 6/8
("95,6% app tập kiểm cũng có ở tập dạy nên điểm bị thổi"):

| | S1 | n |
|---|---|---|
| app đã thấy lúc dạy | **59,1%** | 1.737 |
| app **chưa** thấy | **59,0%** | 78 |
| không gán được app | 59,2% | 2.647 |

Và SFT giúp **nhiều nhất** ở app chưa thấy (**+14,1** so với +11,9) — ngược hẳn lập luận học vẹt.

⚠️ Vẫn phải khai: 3.828/6.958 bước (55%) **không gán được app** = **không biết**, cấm đọc
thành *chưa thấy*.

**(b) Chỗ hỏng đúng chỗ S2 nhắm.** Trong 1.824 bước S1 trượt: chỉ **251 do sai thao tác**,
**1.573 (86%) là thao tác đúng mà bộ trỏ không tìm ra nút** ⇒ lỗi nằm ở **cách gọi tên / tả
phần tử**. Đo trên mô hình thật, không suy từ pilot.

Ví dụ thật:
```
gold : click on the OK option          S1: select minutes 00
gold : Click on the Sort filter        S1: Click on the Air India flight option
gold : Click on the share icon         S1: Open Recorder app
```

**(c) Thước mù 24,3%.** 1.083 bước mà **câu người cũng trượt**. Chẩn đoán:
- **72% do bộ trỏ sai > 14% bề ngang** — tức **bỏ cuộc**, không phải trỏ nhầm nút
- sai số **lưỡng cực**: khi trúng lệch 0,4%, khi trượt lệch 26,2% — không có vùng giữa
- **935 bước (21%) cả ba nhánh cùng trượt**

⇒ **Trần 75,7% là giới hạn DỤNG CỤ, không phải giới hạn của ngôn ngữ.**

Nghi ngờ "câu chuẩn hỏng làm hạ trần" **đã bị bác**: lọc riêng câu chuẩn ≤3 từ cho trần
**77,0%** — không khá hơn bao nhiêu.

### 6.7 Phép diễn đạt lại — trả lời đòn nặng nhất vào thước

**Đòn.** Jandial et al. (*Do GUI Grounders Truly Understand UI Elements?*, **Findings EACL
2026**) báo bộ trỏ GUI **nhạy với cách gọi tên phần tử**, và độ chính xác đo trên **một câu
tốt nhất cho mỗi phần tử** là thổi phồng năng lực thật. Nếu độ nhạy đó lớn, mọi con số trong
file này chỉ đo được **văn phong chú thích của AndroidControl**, không đo khả năng gọi tên.

> ⛔ **CON SỐ 84% ĐÃ BỊ RÚT (18/8) — tra tận nguồn abstract:** *"Our agent reports high success
> rate (upto 84%) in **generating instructions that fail** the state-of-the-art GUI grounding
> models."* Đó là **năng suất của một agent ĐỐI KHÁNG chuyên chế câu phá mô hình**, trên
> **desktop Windows**, không phải tỉ lệ trượt khi diễn đạt lại và không phải trên di động.
> Sai từ 29/7, sống 20 ngày, đã vào bản thảo. ⚠️ Ghi chú gốc của ta
> (`report/papers/do_gui_grounders_eacl2026.md`) **viết đúng từ đầu** — cái sai sinh ra ở khâu
> **tóm tắt ghi chú thành một câu ngắn cho tiện trích**, rồi câu ngắn đó được trích lại hàng
> chục lần mà không ai mở lại ghi chú. ⇒ phép kiểm dưới đây **đo cái chưa ai đo** (di động,
> không đối kháng), chứ không phải phòng thủ trước một tuyên bố sụp đổ.

**Vì sao bộ bơm lỗi cũ không trả lời được.** Nó **không gọi bộ trỏ lần nào** — nó đặt sẵn một
điểm tổng hợp rồi hỏi cổng chữ. Nên hàng *"paraphrase 0,0% kết oan"* trong bảng bơm lỗi chỉ
nói cổng chữ không bác câu diễn đạt khác; nó **không nói gì** về việc bộ trỏ còn tìm ra nút hay
không. Bản thảo bài từng dùng hàng đó để phản bác Jandial et al. — **đã sửa**.

**Phép kiểm đúng.** Lấy **câu chuẩn của người** (đã biết bộ trỏ giải được, trần 75,7%), viết
lại giữ nguyên nghĩa và **giữ nguyên tên phần tử**, rồi cho bộ trỏ chạy lại. Trần tụt bao
nhiêu chính là câu trả lời. Bốn biến thể, chấm trên lát 800 bước:

| biến thể | đổi gì | phần bị đụng | executability | McNemar |
|---|---|---|---|---|
| `p1_verb` | động từ thao tác (*Click*→*Tap/Press/Select*) | 725 bước (90,6%) | 76,8 → **77,0** (+0,1) | b=13 c=14, p=1,000 |
| `p2_order` | đưa mệnh đề vị trí lên đầu câu | 211 bước (26,4%) | 89,6 → **90,0** (+0,5) | b=0 c=1, p=1,000 |
| `p4_both` | `p1` + `p2` cùng lúc | 203 bước (25,4%) | 90,1 → **91,1** (+1,0) | **b=0** c=2, p=0,480 |
| `p3_nopos` | **bỏ hẳn** mệnh đề vị trí | 198 bước (24,8%) | 89,4 → **85,9** (−3,5) | b=8 c=1, **p=0,046** |

Con số gộp ba biến thể **bảo toàn nghĩa** (`p1`·`p2`·`p4`) — đây là con số đi vào bài:

| | |
|---|---|
| bước được viết lại | **1.139** |
| bước đổi chiều | **30 = 2,6%** (13 xuống · 17 lên) |
| hiệu ròng | **+0,35 pp**, KTC95 **[−0,59 · +1,29]** ⇒ loại được mọi mức tụt > **0,6 pp** |
| nếu tụt 84% (mức agent đối kháng của họ đạt trên desktop) | phải có **~956** bước đổi chiều. Thực đo **30** |

**Kết luận: cách nói không đổi được gì; lượng thông tin thì có.** Đổi động từ trên 90,6% số
bước — đứng yên. Đảo mệnh đề vị trí lên đầu — đúng **một** bước đổi chiều trong 211. **Làm cả
hai cùng lúc — xa nhất khỏi câu gốc mà vẫn giữ nghĩa — cũng đứng yên, và `0` bước trúng→trượt
trên 203.** Ghép hai phép viết lại thường là chỗ hiệu ứng cộng dồn lộ ra; ở đây nó không lộ ra
gì. Chỉ khi bỏ mệnh đề vị trí, tức bỏ **thông tin**, mới tụt thật (−3,5 pp, sát MDE 2,2).

⇒ Kết quả rơi về phía **thuận lợi cho thước**: bộ trỏ không mong manh trước diễn đạt, nó chỉ
cần đủ thông tin. Nhưng phải khai đúng phạm vi: `p1`/`p2` đổi *cách nói*, còn Jandial et al.
đổi *cách mô tả phần tử* — nặng hơn. Bằng chứng nằm ngay trong bảng: `action_ok` giữ **100%** ở
cả ba biến thể ⇒ phép viết lại này **không đụng tới phần bộ trỏ phải giải**.

#### Cơ chế: hỏng theo kiểu tất-cả-hoặc-không

Trên 198 bước `p3_nopos` đụng, **trung vị sai số bộ trỏ không nhích một chút nào** trong khi
đuôi bung ra:

| | trung vị | p75 | p90 | p95 | trung bình |
|---|---|---|---|---|---|
| câu chuẩn | 0,24 | 0,89 | 6,88 | 27,54 | 4,52 |
| bỏ vị trí | 0,23 | 1,35 | **31,09** | **61,84** | **9,84** |

Bỏ mệnh đề vị trí **không làm bộ trỏ trỏ lệch đi một chút** — nó làm một số ít bước **mất
hẳn**. Tám bước trúng→trượt có sai số nhảy từ **dưới 1% lên 26–190%**, tức sang phần khác của
màn hình. Khớp phát hiện *sai số lưỡng cực* ở §6.6c: **thước này không có vùng xám.**

⚠️ **Phần bị đụng là phần DỄ NHẤT của lát** — trần ở đó 89,4% so với 74,9% toàn lát, sai số
trỏ trung vị 0,24% so với 0,69%. Hợp lý, vì câu có mệnh đề vị trí là câu đã chỉ sẵn chỗ nhìn.
⇒ −3,5 pp đo trên **một phần tư dễ nhất**; bỏ vị trí ở câu khó có thể đắt hơn, **chưa đo**.

#### ⚠️ Con số tổng bị pha loãng 3,8 lần — luật đọc phải chốt trước

`p2/p3/p4` chỉ viết lại được câu **có mệnh đề vị trí**, tức ~26% số bước. Còn lại là câu chuẩn
y nguyên, không thể đổi kết quả. Nên con số tổng nhỏ đi gần bốn lần so với hiệu ứng thật:

| tổng tụt | phần bị đụng thật ra tụt |
|---|---|
| −1 pp | −3,8 pp |
| −3 pp | −11,4 pp |
| **−16,6 pp** | **−63 pp ≈ đúng quy mô sụp đổ Jandial et al. báo** |

⇒ Ngưỡng khoá trước khi thấy số: **`p3_nopos` tổng ≥ 70% là đủ loại quy mô 84%** (mức đối kháng). Nó ra
**74,0%** (bản v2; v1 cho 73,5%). Đọc kết quả bằng `harness/phep_a_ghep_cap.py` hoặc
`phep_a_hieu_chinh.py`, cột *phần bị đụng*; đừng đọc `score_para_*.json` trần.

#### ⚠️ Một lỗi trong bộ dựng câu, đóng góp 28% hiệu ứng thô

7/211 câu `p3_nopos` (3,3%) **không bỏ mệnh đề vị trí mà xoá luôn tên phần tử**, trơ lại `Tap.`
Nguyên nhân: từ *left/right/center* cũng nằm **trong tên phần tử** — `the left arrow icon`,
`the Right Tick icon` — nên `re.search` (khớp trái nhất) bắt đầu ngay ở *"on the left arrow
icon…"* và mệnh đề "vị trí" ngốn cả tên. Ba trong số đó nằm đúng trong 11 bước trúng→trượt.

| | phần bị đụng | McNemar |
|---|---|---|
| gồm cả 7 câu lỗi (211 bước) | −4,7 pp | b=11 c=1, **p=0,009** |
| **chỉ câu lành (204 bước)** | **−3,4 pp** | b=8 c=1, p=0,046 |

⇒ **28% hiệu ứng thô là lỗi của mình**, và con số lành nằm sát MDE ⇒ đọc là *"tụt nhỏ, ở mép
phân giải"*, **không** phải *"tụt rõ"*.

Đã vá bằng **hai cổng chặn** thay vì siết regex. Cổng A: bỏ mệnh đề xong không được trơ lại
động từ. Cổng B: mệnh đề bị bỏ không được chứa danh từ chỉ phần tử. Kiểm trên 7 ca xấu + 8 ca
lành: **0 lọt, 0 mất**. Bản vá phủ **rộng hơn mà sạch hơn**: 1.159 bước (26,0%) với 0 câu suy
biến, so với 1.113 (24,9%) với 35 câu.

*(Đã thử siết regex trước và bị loại — nó chặn hết 7 ca xấu nhưng giết cả ca lành có mệnh đề
vị trí nằm giữa câu, kiểu "… at the top right corner of the screen **to search the flight**".)*

#### ⚠️ Lỗi thứ hai của bộ dựng câu: đường lui không `.strip()`

Khi biến thể không viết lại được, mã giữ nguyên câu chuẩn — bản đầu ghi **nguyên xi**, mà
**72/589 câu chuẩn có một dấu cách ở cuối** trong khi `preds_ceiling_human.jsonl` đã strip sạch
(0/6.958). Ở đúng những bước lẽ ra phải **trùng khít lượt trần**, bộ trỏ nhận chuỗi lệch một ký
tự và trả toạ độ khác ở **6 bước**, trong đó **1 bước đổi hẳn kết luận** (lệch **1.219 px = 113%
bề ngang**).

✅ Các con số của bài **không bị ảnh hưởng** — bước đó nằm ngoài phần được viết lại, chỉ đụng con
số tổng 0,125 pp. Nhưng nó phá khả năng ghép kết quả từ tệp thô, và đó mới là cái đắt.

**Cách nó bị bắt là điều đáng ghi nhất.** Script ghép có `assert` hỏi *"bộ trỏ tất định không"*
— cùng câu cùng ảnh phải cùng toạ độ. Nó **đỏ ngay lần chạy đầu**: 6/589 lệch. Chẩn đoán đầu là
*"bộ trỏ không tất định"* — **sai**, vì chính bản `assert` đó so chuỗi bằng `.strip()`, tự tay
che mất đúng thứ nó cần thấy. ⇒ **Phép kiểm dùng chính phép biến đổi mà nó cần phát hiện thì
mù.** Nay so chuỗi nguyên xi ở cả hai phía.

#### Chấm lại bản v2 tốn bao nhiêu GPU: KHÔNG GIÂY NÀO

Bản v2 khác v1 ở hai chỗ, và **cả hai đều không sinh ra chuỗi nào chưa từng được chấm**:

| bước của v2 | câu là gì | kết quả lấy từ |
|---|---|---|
| viết lại được | y hệt câu v1 đã chấm (kiểm: `v2 \ v1 = 0`, trùng từng byte) | `score_para_<v>_raw.jsonl` |
| không viết lại được | câu chuẩn **đã strip** | `score_ceiling_human_raw.jsonl` |

`harness/phep_a_hieu_chinh.py` ghép cả bốn biến thể trong vài giây. Sáu phép kiểm cài thành
`assert`, **tất cả so byte** (không `.strip()`, vì thủ phạm chính là một dấu cách):

| # | kiểm gì | kết quả |
|---|---|---|
| 1 | câu lượt trần == `gold_instruction.strip()` từng byte | 0/6.958 · 0/4.463 lệch |
| 2 | bước v2 **viết lại**: chuỗi == chuỗi v1 đã chấm | **0/1.055** |
| 3 | chuỗi bộ trỏ **thật sự nhận** ở lượt v1 == tệp preds | 0/800 |
| 4 | bước v2 **không viết lại**: chuỗi == chuỗi lượt trần | **0/602** |
| 5 | hai lượt cùng `n_buttons` · `gold_xy` · `wh` | 0 lệch cả ba |
| 6 | **tất định**: cùng chuỗi + cùng ảnh ⇒ cùng toạ độ | **0 trên 1.625 phép so** |

⭐ **Phép 6 mạnh hơn vẻ ngoài.** Lượt trần chấm đủ **4.463** bước, mỗi lượt biến thể chỉ **800**
⇒ thứ tự và cách gom lô **khác nhau**. Cùng chuỗi mà cùng toạ độ trên 1.625 phép so (66+517+517
+525, bốn lượt độc lập đối chiếu lượt trần) ⇒ loại luôn khả năng kết quả phụ thuộc **lô hay thứ
tự**, không chỉ loại khả năng bộ trỏ ngẫu nhiên.

⇒ **Con số v2 không phải ước lượng, là kết quả chính xác** — mỗi bản ghi ứng với một lần gọi bộ
trỏ thật trên đúng chuỗi ấy, đúng ảnh ấy (198 bước từ lượt v1 · 602 bước từ lượt trần). Tiết
kiệm **1 giờ quota**, và quan trọng hơn: `p3_nopos` không còn phải *loại 7 câu sau khi thấy kết
quả* — **mã** loại chúng. Con số v2 **−3,5 pp** khớp phép loại tay **−3,4 pp**, tức việc loại
vốn có căn cứ.

⚠️ **Điều duy nhất phép ghép KHÔNG cho: một lượt độc lập.** Lượt v1 có sự cố nhất thời ở một
bước thì bản ghép thừa hưởng. Phép 6 là bằng chứng trực tiếp chống lại khả năng đó trên chính
dữ liệu này, nhưng nếu về sau cần **tái lập độc lập** thì vẫn phải trả 1 giờ.

⇒ Cùng một mẹo đã dùng để đo trần: **tệp thô là tài sản.** Giữ nó thì đổi luật chấm hay đổi tập
câu vẫn tính lại được, miễn bộ trỏ tất định và chuỗi đưa vào trùng khít.

### 6.8 Viết được gì, cấm viết gì

✅ **Viết được ngay:**
- Thước phân giải được hai hệ thống thật (S1 vs Base, +11,5 pp, p<0,001, qua 5 đòn phản biện)
- Đường ống dữ liệu tự động cho supervision đủ để mô hình 3B đạt **78,1% của trần**
- **Thứ tự ba nhánh không đổi dưới năm luật chấm khác nhau**, chênh S1−Base nằm trong
  9,5–13,0 pp (§5.7) — đây là lá chắn mạnh nhất của chương đo lường
- **MDE đo được 2,2 pp**, không còn là số đoán (§5.6)
- **Bộ trỏ bền trước việc đổi động từ và đổi trật tự câu**; tụt nhỏ khi bỏ thông tin vị trí
  (§6.7) — thay được câu tự khai *"we cannot answer it"* trong bản thảo cũ
- Chương dữ liệu · chương đo lường · phương pháp · tái lập · giới hạn

⛔ **Cấm viết:**
- *"Bộ trỏ khác họ mô hình được chấm"* hay *"recipe bộ trỏ không có AndroidControl"* — **cả
  hai đều sai**, xem §5.4. Phải khai nhiễm văn phong.
- *"Bộ trỏ bền trước diễn đạt lại"* — chỉ đo được **đổi động từ** và **đổi trật tự**. Đòn của
  Jandial et al. nhắm *cách mô tả phần tử*, chưa đo.
- Dùng hàng *"paraphrase 0,0%"* của bảng bơm lỗi để phản bác Jandial et al. — bộ bơm lỗi
  **không gọi bộ trỏ lần nào**.
- **Bảng so sánh S1 vs S2**, hay bất kỳ câu nào về hiệu quả của "mô tả trước, phát ngôn sau"
  — S2 chưa train
- Để **Base-vs-S1 thay chỗ ablation đã đăng ký** — đó là đổi câu hỏi sau khi thấy dữ liệu
- Chữ **"đầu tiên" / "novel" / "cơ chế mới"** cho cả hai lớp thành phần (dòng REG phân biệt
  đã chiếm ý từ Mao CVPR 2016)
- *"bộ trỏ chưa từng thấy màn hình di động"* — sai. Viết *"không được huấn luyện trên
  AndroidControl"*

---

## 7. Giới hạn phải khai

| giới hạn | số | trạng thái |
|---|---|---|
| ⛔ **Bộ trỏ NHIỄM văn phong + CÙNG họ mô hình** | UGround train trên **AndroidControl 47K**, dựng trên **Qwen2-VL** | **chưa đóng** — cần bộ trỏ thứ hai |
| **Chỉ một bộ trỏ** | số tuyệt đối gắn với UGround; so giữa các nhánh vẫn hợp lệ vì cùng dụng cụ | chưa đóng |
| **Thước mù 24,3%** | trần 75,7% là giới hạn dụng cụ, không phải của ngôn ngữ | đã khai kèm chẩn đoán |
| **Bộ trỏ bỏ cuộc 15,3%** số bước | không trả toạ độ dùng được | đã khai |
| **Chấm teacher-forced trên ngữ cảnh** | `history` là câu chuẩn của người, trùng 5.318/5.318 | đã khai (§1.5) |
| **Tập kiểm không phải app-unseen** | 95,6% app trùng tập dạy | §6.6a bác được ảnh hưởng |
| **55% bước không gán được app** | "không biết", cấm đọc thành "chưa thấy" | đã khai |
| **Luật đảo nghĩa mù ngoài bảng** | bảng tay 9 cặp; cặp đặc thù giao diện (next/previous) không bắt | đã khai |
| **Voronoi chỉ chặt bằng bộ dò** | bộ dò sót nút thì câu sai vẫn lọt | đã khai |
| **Dung sai dọc rộng gấp 2,2 lần dung sai ngang** | hệ quả của ngưỡng "14% cạnh màn" | đã khai (§5.3) |
| **Chưa đo được đòn diễn đạt của Jandial et al.** | chỉ đo đổi động từ + đổi trật tự; *cách mô tả phần tử* chưa đụng | phần đã đo: §6.7 |
| **Một lỗi `canon_action` giữ nguyên có chủ ý** | `go back` bị quy về *tap*, ảnh hưởng 81 bước S1 / 47 Base | xem dưới |

**Giới hạn đầu là giới hạn nghiêm trọng nhất còn mở**, và cách đóng đã tra sẵn: kiểm chéo bằng
**UI-Venus-Ground-7B** (Apache-2.0, ScreenSpot-v2 mobile 99,0/90,0 — mạnh hơn UGround
95,0/83,3, **sạch AndroidControl**, dựng trên Qwen2.5-VL nên vẫn không thoát điều kiện "khác
họ", nhưng đóng được điều kiện quan trọng hơn là nhiễm dữ liệu). Lát 500 bước, ba nhánh, ~6 giờ
Kaggle. Mốc so đã tính sẵn từ tệp thô: **73,4 / 58,8 / 47,6**, chênh **+11,2 pp**.

⛔ **Đã loại sau khi tra:** GUI-G2-3B (trùng nền Qwen2.5-VL-3B với chính mô hình bị chấm) ·
**Jedi** (CÓ AndroidControl dù tự quảng bá chỉ dữ liệu tổng hợp) · CogAgent (link chết, vĩnh
viễn không kiểm được) · Aria-UI (25,3B, không vừa máy) · SE-GUI/GUI-G1/GUI-R1/Holo1 (nhiễm
gián tiếp qua OS-Atlas). Dự phòng: **Phi-Ground-4B** (ngoài họ Qwen — nên nhớ câu *"mọi bộ trỏ
GUI mở đều dựng trên họ Qwen-VL"* là **SAI**, đã lỡ vào bản thảo và đã vá).

### Một lỗi trong `canon_action` — biết mà cố tình không sửa

`ACTION_MAP` quét từ trái sang, mà `go` → *tap* đứng trước `back` → *navigate_back*. Nên câu
*"go back"* bị quy về **tap** thay vì **navigate_back**.

Đo được cái giá: **81 bước** ở S1, **47** ở Base. Sửa lại thì điểm đổi 59,12 → **58,81** và
47,60 → **47,40** — tức chênh S1−Base gần như không nhích.

**Vì sao không sửa đè:** ba nhánh đã chấm bằng luật hiện tại; sửa đè thì mọi số cũ mất khả năng
tái lập, mà lợi ích là 0,3 điểm ở cả hai nhánh cùng chiều. Đã thêm cờ `strict_back=True` cho
lượt chấm mới, ghi **mục sửa đổi (v)** vào `report/106`, và tài liệu hoá thẳng trong docstring
của `canon_action`. **Bài học: lỗi đã đo được cái giá thì thành lựa chọn có ghi chép, không còn
là lỗi ngầm.**

---

## 8. Còn phải làm gì

### 8.1 Việc còn lại, thứ tự theo giá

| # | việc | phụ thuộc | giá | trạng thái |
|---|---|---|---|---|
| 1 | train **S2 hạt giống 101** | — | ~126 đv | 🔄 **đang chạy** (18/8, bước 2.260/8.072) |
| 2 | train **S2 hạt giống 202** | #1 | ~126 đv | ⏳ chạy ngay sau #1 |
| 3 | sinh câu + **chấm S2 ×2** | #2 | 0 đ · ~11 giờ Kaggle | ⏳ dự kiến có số 22–23/8 |
| 4 | **cắt bài FAIR 10 → 8 trang** | — | 0 đ | ⏳ chặn việc nộp |
| 5 | kiểm chéo **UI-Venus-Ground-7B**, lát 500 bước, 3 nhánh | — | 0 đ · 6 giờ Kaggle | ⏳ đóng giới hạn nặng nhất còn mở |
| 6 | nộp **VCL** (tiếng Việt) | #7 | — | ⏳ **30/8** |
| 7 | nộp **FAIR'2026** qua EDAS | #4 | — | ⏳ **31/8** |

**Đã xong, không phải làm lại:** train + chấm s1 hai hạt giống · MDE thật 2,2 pp · bốn biến thể
diễn đạt lại · chấm lại `p3_nopos` từ tệp thô (0 GPU) · **ba nhánh sàn** (§5.8) · tra tiền lệ
chữ *executability* (`report/114`).

**Trình tự cứng, không đảo** (khoá trong `report/106` mục 5): S1 ×2 hạt giống → chấm đủ → MDE
thật → khoá ngưỡng → **mới** train S2. Lý do: cặp hạt giống S1 là **null thực nghiệm** — nó cho
biết hai lượt train khác nhau bao nhiêu **khi không có can thiệp nào**. Không có con số đó thì
không phân biệt được "S2 hơn S1" với "nhiễu giữa hai lượt train". Trình tự này **đã đi đúng**.

**Ô kiểm vàng trước mỗi lượt train** (`harness/run_on_colab.md` ô A.2b): so cấu hình lượt này
với lượt tham chiếu; **chỉ 4 khoá được phép khác** (`seed` · `output_dir` · `dataset` ·
`preprocessing_num_workers`), khoá thứ năm là **dừng hẳn**. Lượt 202 đã kiểm: **38/38 khoá, chỉ
khác `seed` và `output_dir`**.

**Ràng buộc tài nguyên:** Kaggle **30 giờ GPU/tuần** (một lượt chấm 5,6 giờ ⇒ tối đa 5
lượt/tuần, đừng dồn). Đơn vị Colab thì **đếm lại trong phiên** — con số ghi trong tài liệu lỗi
thời rất nhanh.

### 8.2 Đề tài nộp HAI bài, cách nhau một ngày

| | **VCL2026** | **FAIR'2026** |
|---|---|---|
| hạn | **30/8** | **31/8** (EDAS) |
| ngôn ngữ | tiếng Việt | tiếng Anh |
| nội dung | **nhãn mô tả phần tử** — dựng nhãn tự động từ cây trợ năng + OCR (§1, §2 của file này) | **thước đo executability** (§5) + bảng kết quả (§6) |
| đóng khung | sinh **biểu thức quy chiếu** cho phần tử giao diện: gọi tên thế nào để bên kia trỏ đúng, khi 22% phần tử không tên và 7,6% trùng tên | dụng cụ đo khả năng phân giải phần tử: trần · sàn · độ bền |

**Luật chống trùng:** trần / sàn / cổng A / 5 luật chấm / diễn đạt lại / gọi-tên-vs-chỉ-chỗ /
tất định / κ **chỉ thuộc FAIR**. Ghép hai kho 2,4× / rò rỉ 0 / OCR phủ 100% / chất lượng nhãn /
hai cổng lọc / quyết định A′ bị bác / 9 bất biến **chỉ thuộc VCL**. Quy mô dữ liệu thì VCL tả
đủ, FAIR một câu rồi trích VCL. Hai bài trích chéo dạng *"đang bình duyệt"*.

**S2 không phải headline của bài nào** — khi có số nó thành **một hàng thêm** vào bảng kết quả
của FAIR. Headline của **luận văn** vẫn là S2 vs S1. Nhờ vậy hai bài không phụ thuộc vào việc
lượt train đang chạy ra kết quả gì.

⛔ `report/KE_HOACH_2_BAI_BAO.md` (bản 12/7) định VCL = *sinh hướng dẫn tiếng Việt trên
MobileViews* — **chết cả hai vế**, MobileViews đã rời khỏi đề tài và không có thí nghiệm tiếng
Việt nào. Cách chia hiện hành nằm trong `CLAUDE.md` mục *Hai bài báo*.

---

## 9. Bản đồ file

### Mã

| file | vai |
|---|---|
| `harness/build_train_data.py` | ghép hai kho HF → `train.jsonl` |
| `harness/prep_ocr_train.py` | chạy OCR (RapidOCR ONNX, CPU, miễn phí) |
| `harness/descriptor_label_build.py` | dựng nhãn khai báo từ cây trợ năng + OCR |
| `harness/build_branch_data.py` | 4 tệp nhánh, định dạng sharegpt |
| `harness/build_test_data.py` | tập kiểm 6.958 bước |
| `harness/tag_app_seen.py` | gắn nhãn `app_seen_in_train` |
| `harness/train_config.yaml` | cấu hình LLaMA-Factory, một file cho mọi nhánh |
| `harness/infer_branch.py` | sinh câu (ghi dần, nối tiếp được) |
| `harness/score_run.py` | bộ trỏ + chấm + gộp số (ghi dần, nối tiếp được) |
| `harness/metric_exec.py` | **luật chấm** — có phần tự kiểm chạy được |
| `harness/make_bundle.py` | đóng gói mang lên Colab/Kaggle |
| `harness/run_on_colab.md` | **runbook** train — chạy theo ô, đừng viết lại mã |
| `harness/rule_sensitivity.py` | chấm lại dưới 5 luật khác nhau (§5.7) — đọc từ tệp thô, miễn phí |
| `harness/make_paraphrase.py` | dựng 4 biến thể diễn đạt lại; **có hai cổng chặn**, đọc chú thích trước khi sửa |
| `harness/phep_a_ghep_cap.py` | đọc kết quả phép A **theo ghép cặp** — dùng cái này, đừng đọc `.json` trần |
| `harness/phep_a_hieu_chinh.py` | dựng kết quả bản v2 của cả bốn biến thể **từ tệp thô, 0 GPU**; có `assert` tự kiểm bộ trỏ tất định |
| `harness/rasoat_16_8.py` | bán kính gộp, sàn theo khoảng cách hàng xóm, lát cắt vùng mù |
| `harness/make_fig_voronoi.py` | dựng hình Voronoi cho bài; **tự khẳng định** bằng `assert` nên hình không thể trái mã |
| `harness/kaggle_pheA_CHAY_LAI.md` | **runbook** chấm trên Kaggle — có ô kiểm GPU và nhịp sống |

### Kết quả

Mỗi nhánh ba tệp:
- `score_<nhánh>.json` — số tổng hợp
- `score_<nhánh>_raw.jsonl` — **một dòng mỗi bước** ⇒ đổi luật chấm hay thêm lát cắt thì
  **chấm lại từ đây, không gọi lại bộ trỏ** (tiết kiệm 5,6 giờ mỗi lần)
- `preds_<nhánh>.jsonl` — câu do mô hình sinh

Ba nhánh chính ở gốc `runs/`; mỗi phép kiểm phụ một thư mục riêng. Tải từ Kaggle về thì đặt
**thẳng vào thư mục của phép đó** — ngày 17/8 bốn tệp lạc vào `report/papers/` (thư mục ghi
chú tài liệu tham khảo), mất một lượt dọn để nhận ra.

| chỗ | đựng gì |
|---|---|
| `runs/` | `score_ceiling_human` · `score_s1_seed101` · `score_base` |
| `runs/gate_a/` | vết cổng A |
| `runs/paraphrase/` | phép A — `preds_para_*` + `score_para_*` |
| `runs/venus/` | phép B (chưa chạy) |

Một dòng thô thật:
```json
{"episode_id": 18173, "step_id": 3, "app": "dailyart", "app_seen_in_train": true,
 "pred_xy": [993.6, 2157.6], "gold_xy": [994.0, 2158.0], "wh": [1080, 2400],
 "n_buttons": 163,
 "sent": "Click on the search icon at the bottom right corner of the screen",
 "gold_instruction": "Click on the search icon at the bottom right corner of the screen ",
 "action_ok": 1, "toggle_ok": 1, "hit_disk": 1, "hit_voronoi": 1, "executable": 1}
```

### Báo cáo

| file | vai |
|---|---|
| `report/106` | **bản đăng ký trước** — 6 nhánh, thước, luật đọc kết quả cho cả 4 kết cục. Sửa đổi ghi vào **cuối file**, không sửa đè |
| `report/107` | tranh luận nguồn tên (OCR vs trợ năng) |
| `report/108` | sổ kê khai — 24 lỗi đã bắt + **danh sách số đã bị rút** |
| `report/109` | bản đồ hiện tại |
| `report/110` | nhật ký phiên Colab — chi tiết từng lượt chạy |
| `report/112` | **file này** |
| `paper/fair2026/main.tex` | bài FAIR'2026, 8 trang, IEEEtran |

### Tái tạo

```bash
# gói dữ liệu chấm (1,7 GB), tải lên Kaggle làm dataset dùng lại
python harness/make_bundle.py score

# chấm một nhánh
python harness/score_run.py --mode score --grounder uground \
    --preds runs/preds_s1_seed101.jsonl --out runs/score_s1_seed101.json
```

⚠️ `test.jsonl` phải là **bản đã gắn nhãn `app_seen_in_train`** (`score_run.py:405` đọc nhãn
thẳng từ đó). Bản đúng: 6.958 dòng, nhãn 2.991 / 139 / 3.828.

Dữ liệu huấn luyện: `s1.json` md5 **641953d75d61ab192b94a559362cce9b**, 64.567 mẫu.

---

---

## 10. Mười ba điều rút ra, dùng lại được cho dự án khác

1. **Xếp thứ tự thực nghiệm theo GIÁ.** Nhánh chỉ-suy-luận (Base) tốn ~$0,8; một lượt train
   tốn ~$12. Chạy cái rẻ trước — giá trị không phải tiết kiệm tiền mà là **thông tin sớm**.
2. **Số đo trên mẫu con thì đừng đưa vào bảng chính.** Trần đo trên 300 bước lệch 5,7 điểm
   và KTC không phủ giá trị thật.
3. **Mỗi biến thể chỉ đổi MỘT thứ.** Ghép hai thay đổi thì tràn bộ nhớ trước khi trả lời
   được câu nào.
4. **Thăm dò trên mẫu đầu tập không kết luận được về bộ nhớ.** Phải thử trên nhánh nặng nhất
   với mẫu dài nhất.
5. **Mọi phép ghép dữ liệu phải có đối chứng lệch chủ ý.** "48%" là số vô nghĩa nếu không
   biết 20% là bao nhiêu.
6. **Hỏi "máy chết bây giờ thì mất bao nhiêu"** trước khi phóng bất cứ lượt chạy dài nào.
   Câu hỏi đó đáng 42 đơn vị.
7. **Suy diễn thay cho đo là nguồn sai số lớn nhất.** "7,3 mẫu/giây × 12 lõi" sai 6 lần vì
   `datasets.map` chạy một tiến trình. Giá GPU cũng vậy — phải tra tại thời điểm quyết.
8. **Ghi kết quả dần, đừng ghi một lần ở cuối.** Hai script từng ghi ở cuối ⇒ đứt máy là mất
   trắng 5 giờ.
9. **Số của thư viện chia cho `elapsed` đều hỏng sau resume.** Kiểm bằng phép nhân ngược.
10. **Khai giới hạn KÈM số bác bỏ, đừng khai suông.** "95,6% app trùng" đọc rất nặng — cho
    tới khi có bảng 59,1 / 59,0 / 59,2 bên cạnh.
11. **Chữ "đã xác minh" trong ghi chú của chính mình không phải bằng chứng.** Hai khẳng định
    về bộ trỏ sống 18 ngày, vào tới bản thảo bài báo, rồi bị lật bởi một lần mở đúng Bảng 1
    của bài gốc. Trước khi một khẳng định đi vào bài, mở lại **nguồn**, không mở lại ghi chú.
12. **Tài liệu tả thước phải đọc từ MÃ, không từ ý định.** Ba chỗ trong bài tả sai dụng cụ mà
    vẫn nghe rất hợp lý: "đĩa" thật ra là hình chữ nhật cao gấp 2,2 lần · hạt Voronoi là điểm
    chạm chứ không phải tâm nút · Voronoi **bao gồm** luật đĩa chứ không thay nó. Cách chặn:
    hình vẽ trong bài dựng bằng script có `assert` gọi thẳng hàm của thước
    (`make_fig_voronoi.py`) ⇒ hình không thể trái mã.
13. **Hiệu ứng đo trên một tập con thì phải chia lại theo tập con đó.** Ba biến thể diễn đạt
    lại chỉ đụng 26% số bước, nên con số tổng **nhỏ đi 3,8 lần** so với hiệu ứng thật. Chốt
    hệ số pha loãng **trước** khi xem kết quả, không thì "tụt 1,4 pp" đọc thành "gần như
    không đổi" trong khi thật ra là "tụt 4,7 pp trên phần bị đụng".

---

## 11. Bài còn hợp lệ tới đâu — chốt 18/8/2026

> Viết sau bốn lượt phản biện độc lập (17-18/8) và sau khi tự kiểm lại mọi khẳng định chịu
> lực bằng số của chính mình. Mục này trả lời một câu: **cái gì đứng, cái gì chưa.**

### 11.1 ⭐ Mẫu hình quan trọng nhất: lỗi nằm ở CÂU CHỮ, không ở PHÉP ĐO

Bảy lỗi bắt được trong hai ngày, **không lỗi nào ở khâu đo**:

| lỗi | ở đâu | đo có sai không |
|---|---|---|
| "bộ trỏ trượt 84% khi đổi diễn đạt" | câu mô tả tài liệu tham khảo | không |
| "bộ trỏ khác họ / sạch AndroidControl" | ghi chú tra cứu | không |
| "reference-free" trong nhan đề | nhan đề vs mã | không (bản không-tham-chiếu lệch ≤0,20 pp) |
| `hit_disk` là "đĩa" | câu mô tả thước | không |
| hạt Voronoi là "tâm phần tử" | câu mô tả thước | không |
| κ = 0,867 | cách trình bày | không (số đúng, nhưng phải kèm điều kiện) |
| đếm 14 mục sửa đổi | câu trong bài | không |

Trong khi đó phần **đo** giữ nguyên qua mọi lượt soi: `metric_exec.py` **một commit duy nhất**
từ 5/8 · tệp thô tái lập tới chữ số cuối · hai hạt giống độc lập cho **+11,5** và **+12,0** ·
sáu lát cắt chẩn đoán **lặp lại cả sáu** · thước tất định **1.625 phép so, 0 bất đồng**.

⚠️ **Nói cho chính xác về "một commit"** (soát lại 18/8, `git diff`): cây làm việc **có** một
sửa đổi chưa commit trong `metric_exec.py` — mục sửa đổi **(v)**, thêm cờ **tuỳ chọn**
`strict_back` cho `canon_action`. Nhưng nó **không đụng một điểm số nào đã chấm**, và kiểm
được bằng hai cách: (a) đường mặc định `strict_back=False` chạy **đúng mã cũ từng dòng**,
phần thêm chỉ là một nhánh `if` đứng trước; (b) `grep` toàn kho cho thấy nơi duy nhất truyền
`strict_back=True` là `score_run.py --mode noharm`, tức **quần thể bước KHÔNG-chạm** — phép
kiểm không-gây-hại, **chưa chạy lần nào**, và tách hẳn khỏi 4.462 bước chạm của bảng chính.
⇒ Câu đúng phải viết là: **luật chấm áp lên mọi nhánh đã chấm không đổi dòng nào kể từ 5/8**,
chứ không phải "tệp không đổi". Hai câu đó khác nhau, và chỉ câu sau mới kiểm được bằng
`git log`.

⇒ **Bài học vận hành:** chỗ phải soi tiếp là **văn bản**, không phải mã. Và cụ thể hơn: mọi
lỗi trên đều sinh ra ở khâu **tóm tắt một nguồn thành một câu ngắn cho tiện trích** — rồi câu
ngắn đó sống nhiều tuần vì không ai mở lại nguồn.

### 11.2 Đứng vững — không lượt phản biện nào lật được

| khẳng định | bằng chứng |
|---|---|
| SFT hơn mô hình gốc | **+11,52** và **+12,03 pp** ở hai hạt giống độc lập, KTC chồng lấn gần trọn, p<0,001 |
| chênh lệch không phải nhiễu huấn luyện | nhiễu hạt giống **0,52 pp** [−0,21 · +1,28], p=0,194 ⇒ tín hiệu gấp **22×** |
| chênh lệch không phải do văn phong | cùng nội dung khác văn phong: **+0,9…+1,9 pp, không ý nghĩa** |
| kết luận không phụ thuộc luật chấm | 5 luật, trần trôi 56,6→82,2 mà **thứ tự không đổi**, chênh 9,5–13,0 pp |
| thước không tự sinh nhiễu | 2.810 câu trùng byte → **0** khác toạ độ, **0** khác phán quyết |
| thước không nhạy với diễn đạt (di động, không đối kháng) | 1.139 câu viết lại → **+0,35 pp** [−0,59 · +1,29] |
| **thước không xếp văn máy trên văn người** | trần 75,7 > S1 59,4 > Base 47,6, bốn KTC rời nhau, thứ tự kỳ vọng **trước** khi chấm |
| không có lợi thế sân nhà | app chưa thấy **+14,1 / +14,1** ở cả hai hạt giống |
| hồ sơ đăng ký trước là thật | `git log`: `metric_exec.py` **một commit**, ngày 5/8, train đầu 12/8 |

### 11.3 Năm lỗ đã ghi 17/8 — nay ba đóng, hai còn mở

**(a) ✅ ĐÃ ĐÓNG — sàn đo được, 12,0%.** Xem **§5.8**. Câu vô nội dung ăn 12,0%, không phải
~40% như phản biện dự đoán; dải dùng được 62,9 điểm. Câu *"the metric does not collapse towards
its floor"* nay có phép đo chống lưng thay vì chỉ có lập luận.

**(b) ✅ ĐÃ ĐÓNG — thước đo GỌI TÊN, không phải chỉ chỗ.** Xem **§5.8 ③**. Bỏ tên **−28,5 pp**
so với bỏ vị trí **−3,5 pp**, hai quần thể gần bằng nhau (193 vs 198 bước) ⇒ chữ *"Element
Identification"* trong nhan đề đúng, không phải đổi thành *localisation*.

**(c) ⛔ CÒN MỞ — chưa thay dụng cụ lần nào.** Bộ trỏ **chính là** thước, mà nó nhiễm
AndroidControl và cùng họ Qwen với mô hình bị chấm (§5.4). Mọi bằng chứng độ tin cậy đều nằm
**bên trong một bộ trỏ**. Cách đóng: chấm lát 500 bước bằng **UI-Venus-Ground-7B** — việc số 5
ở §8.1, 6 giờ Kaggle, 0 đồng. **Đây là việc đáng giá nhất còn lại của cả dự án.**

**(d) ⛔ CÒN MỞ — không có neo ngoài nào.** Không người chấm (đã quyết từ đầu), không nhãn người
mượn từ nơi khác, không hệ quả hạ nguồn. Toàn bộ tính hợp lệ cấu trúc dựa trên **lập luận** cộng
với các phép đối chứng nội bộ ở §5.7, §5.8, §6.7. Lỗ này **không đóng trong mùa này**, phải khai
thẳng trong mục giới hạn.

**(e) ✅ ĐÃ ĐÓNG — chữ "executability" có chủ, nhưng ta vẫn giữ tên.** *Open Grounded Planning*,
**ACL 2024**, tr. 4982–5003 (arXiv 2406.02903) mục 3.3.2 định nghĩa hình thức: *"Executability is
the proportion of executable cases. Executable cases are actions in the plan that all exist within
the given action library."* Khác hẳn ta: của họ là **tra bảng ký hiệu trên văn bản** — không mô
hình, không màn hình, miền WikiHow/công cụ/robot, và họ tự khai *"only focuses on the planning
generation"*. Của ta là **hành vi + thị giác**. ⇒ **giữ tên**, thêm một câu phân định vào
Introduction ngay lần dùng đầu. Chi tiết: `report/114`.

### 11.4 Phán quyết

**Bài hợp lệ như một đặc trưng hoá dụng cụ đo *khả năng phân giải phần tử* trong hướng dẫn GUI
di động, trong phân bố, với một bộ trỏ.**

So với bản 17/8, hai chỗ mạnh lên: các con số **tuyệt đối** nay diễn giải được vì đã biết cả hai
đầu thước (12,0 → 75,7), và tuyên bố về **gọi đúng tên phần tử** nay có `f2_khongten` chống lưng
chứ không còn là suy đoán.

Chỗ chưa hợp lệ, phải khai thẳng: mọi con số **gắn với một bộ trỏ duy nhất**, và bộ trỏ đó đã
thấy văn phong chú thích của chính kho dữ liệu này. Câu đúng để viết là *"đo bằng UGround"*,
không phải *"đo được"*. Chừng nào việc số 5 ở §8.1 chưa chạy thì câu đó phải giữ nguyên.

### 11.5 Bài học rút ra từ chính lần tự kiểm này

**Thứ tự làm việc đã đúng, nhưng suýt sai.** Hai lỗ (a) và (b) đóng bằng **hai lượt chấm ~1
giờ, tệp đã dựng sẵn trên đĩa, 0 đồng** — trong khi chúng là hai đòn phản biện nặng nhất trong
bốn lượt soi. Chúng nằm đó nhiều ngày mà không ai nhìn ra, vì mọi sự chú ý đổ vào lượt train 24
giờ đang chạy. **Việc rẻ nhất và việc quan trọng nhất có thể là cùng một việc** — nhưng chỉ khi
đã liệt kê ra giấy mới thấy, chứ không tự lộ ra.

**Và cái đắt nhất vẫn không phải phép đo.** Bảy lỗi ở §11.1 đều là câu chữ. Lỗ (e) — chữ
*executability* có thể đã có chủ — cũng là câu chữ: nó không đụng một dòng mã nào, nhưng nếu để
nguyên thì đụng thẳng nhan đề bài báo. Chỗ phải soi tiếp vẫn là **văn bản**, không phải mã.
