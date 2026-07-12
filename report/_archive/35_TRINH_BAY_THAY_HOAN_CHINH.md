# BẢN TRÌNH BÀY: HỆ SINH HƯỚNG DẪN & CÁCH ĐÁNH GIÁ
### (trình thầy xin chốt hướng & cho bảo vệ — đầy đủ pipeline, metric, ví dụ, công thức)

> **Tính chất buổi này:** trình bày **hướng làm + thiết kế + kết quả sơ bộ** để xin thầy chốt cho bảo vệ. Số liệu chính đang chạy; phần này nói rõ chỗ nào đã có sơ bộ, chỗ nào đang chạy.
> **Đọc theo thứ tự:** Phần 1 (dữ liệu) → Phần 2 (pipeline + ví dụ) → Phần 3 (metric + công thức + ví dụ) → Phần 4 (vì sao tin được) → Phần 5 (đóng góp, độ mới, giới hạn). Cuối là phần dự phòng câu hỏi.

---

## MỞ ĐẦU — bài toán, đóng góp, và độ mới (nói thật)

Khi mở một phần mềm lạ, người dùng thường chỉ biết hỏi: *"muốn làm việc này thì bấm vào đâu?"*. Em muốn một AI nhìn ảnh màn hình và câu hỏi đó, rồi tự viết hướng dẫn từng bước.

Hai chỗ vướng khiến nó thành bài toán nghiên cứu. Một, AI hay bịa nút không có thật trên màn, làm người dùng tìm hoài không thấy. Hai, với mỗi phần mềm thì không ai soạn sẵn bản hướng dẫn chuẩn để mình so mà chấm điểm. Bài dịch máy có bản dịch mẫu để đối chiếu; bài này thì không có gì.

Luận văn có **hai đóng góp**:
1. Một **cách sinh hướng dẫn ít bịa hơn** (một lớp hậu kiểm gắn được vào bất kỳ model nào).
2. Một **cách tự chấm điểm khi không có bản mẫu**.

**Độ mới, em nói thẳng để khỏi bị bắt giấu:** em không phát minh việc sắp thứ tự ảnh (đã có Sort-Story, EMNLP 2016; RankGPT, EMNLP 2023) hay việc kiểm tra grounding. Cái mới là **đặt chúng vào một bài chưa ai làm** — đánh giá hướng dẫn cho người đọc khi không có bản mẫu — và **làm cho phép đo không tự chấm**: tách công cụ quyết khỏi công cụ chấm, suy nhãn từ đáp án vàng chứ không từ model, và tự bơm lỗi để kiểm chính thước đo.

Em không đua "viết văn hay" với GPT-5. Em chứng minh hai điều đo được: cách chấm của em đáng tin, và lớp của em giảm bịa, kèm cái giá phải trả minh bạch.

---
# PHẦN 1 — DỮ LIỆU & "DANH SÁCH NÚT THẬT" (đọc trước cho dễ hiểu phần sau)

Mỗi màn hình Android có sẵn một bản kê khai do hệ điều hành cấp, liệt kê mọi nút thật trên màn kèm tên và khung toạ độ. Thuật ngữ kỹ thuật là *View Hierarchy* (hoặc *accessibility tree*); **từ đây em gọi gọn là "danh sách nút thật"**. Đây là thứ giúp em chấm điểm mà không cần bản mẫu của người.

Em dùng hai bộ dữ liệu, mỗi bộ cho một nhánh:

| | **MỘT màn (MobileViews)** | **NHIỀU màn (AndroidControl)** |
|---|---|---|
| Ảnh từng màn | có | có |
| **Danh sách nút thật** + khung | có | có |
| **Đáp án vàng** (thứ tự đúng + thao tác đúng mỗi bước) | **không** → nhánh "không có đáp án mẫu" | **có** → nhánh "có đáp án vàng" |
| Vai trò | đo *không-bịa* | đo *thứ tự* và *làm-tới-đích* |

Điểm cần nhớ: với nhiều màn em **không thiếu** danh sách nút. AndroidControl (đã bình duyệt, NeurIPS 2024) có sẵn danh sách nút của từng màn, và còn giàu hơn vì có thêm đáp án vàng. *(Đối chứng grounding thêm: ScreenSpot-v2, ICLR 2025.)*

---
# PHẦN 2 — PIPELINE: HỆ THỐNG CHẠY THẾ NÀO

## 2.1. Hai pha — AI thấy gì, thuật toán dùng gì (chỗ thầy hay vặn nhất)

Đây là điểm dễ hiểu lầm nhất, nên em nói rõ ngay. **Lúc AI viết hướng dẫn, nó chỉ thấy ảnh và câu hỏi. Danh sách nút thật không bao giờ đưa vào tay AI.**

```
PHA 1 — LÚC SINH   (AI chỉ thấy ảnh + câu hỏi)
   [ ẢNH + CÂU HỎI ]  ──►  AI viết hướng dẫn  ──►  bản model-tự-viết (gọi tắt BASE)
   ▸ Danh sách nút thật KHÔNG xuất hiện ở pha này.

PHA 2 — LÚC ĐỐI CHIẾU & CHẤM   (một thuật toán, không phải AI ngôn ngữ)
   bản BASE  ──►  so với [ danh sách nút thật ]  ──►  bản sau-hậu-kiểm + điểm số
   ▸ Danh sách nút thật chỉ vào ở pha này.
```

Ba điều phải nắm (thầy sẽ vặn đúng ba điều này):

1. **AI không bao giờ thấy danh sách nút.** Cái dùng danh sách nút là một thuật toán so sánh, không phải một mô hình ngôn ngữ. Nếu cho AI thấy nút thì chuyện "không bịa" thành hiển nhiên, kết quả vô nghĩa. Đó là cái bẫy em chủ động tránh.
2. **Câu hỏi cũng không chứa tên nút.** Câu hỏi diễn đạt theo ý định người dùng (ví dụ "làm sao thêm khoản chi"), không nêu tên nút. Em kiểm độ trùng từ giữa câu hỏi và nhãn nút bằng không, và loại các câu lỡ lộ tên nút. Nên kể cả khi câu hỏi gợi từ một chức năng có thật, cái lộ ra chỉ là "chức năng đó tồn tại", chứ không phải "tên nút là gì". AI vẫn phải tự đọc ảnh để gọi tên, và đó mới là chỗ nó bịa.
3. **Em chấm cả hai bản** (bản model-tự-viết và bản sau hậu kiểm) rồi so sánh. Cái em báo cáo là *AI viết tự do thì bịa bao nhiêu*, và *lớp của em xử được bao nhiêu, với giá nào*.

Toàn dây chuyền gồm năm khối: **(0)** sắp thứ tự các màn (chỉ khi nhiều ảnh) → **(A)** AI sinh hướng dẫn → **(B)** thuật toán đối chiếu với danh sách nút → **(C)** bước trỏ nút không có thật thì viết lại thành mô tả bằng lời → **(D)** chấm cả hai bản. Em không huấn luyện lại model lõi, dùng đồ có sẵn; đóng góp nằm ở lớp hậu kiểm và cách chấm.

## 2.2. Ví dụ chạy thật — MỘT màn

Màn app ghi chi tiêu. Danh sách nút thật (nhắc lại: AI không thấy danh sách này):

```
Add expense | Amount | Category | Save | Settings | Back
```
**Câu hỏi người dùng:** *"Làm sao thêm một khoản chi mới?"*

**(A) AI chỉ nhìn ảnh + câu hỏi, viết ra:**

| Bước | AI viết |
|---|---|
| 1 | Bấm **Add expense** |
| 2 | Nhập số tiền vào ô **Amount** |
| 3 | Bấm **Submit** |
| 4 | Bấm **Save changes** |

Màn không có nút "Submit", và tên đúng là "Save" chứ không phải "Save changes".

**(B) Thuật toán đối chiếu từng bước** (tìm nút gần nghĩa nhất, đo độ giống):

| Bước AI viết | Nút thật gần nhất | Độ giống | Kết luận |
|---|---|---|---|
| Add expense | Add expense | rất cao | có thật |
| Amount | Amount | rất cao | có thật |
| Submit | Save | thấp (khác nghĩa) | **BỊA** |
| Save changes | Save | cao (gần nghĩa) | có thật (gọi hơi khác tên) |

**(C) Lớp hậu kiểm** chỉ đụng bước bịa (bước 3): "Bấm **Submit**" được viết lại thành *"Tìm và bấm nút để lưu khoản chi vừa nhập"*. Ba bước có thật giữ nguyên.

## 2.3. Ví dụ chạy thật — NHIỀU màn (khối sắp thứ tự)

Việc cần làm: *"xem hồ sơ của tôi"*, qua hai màn. Màn A là **Đăng nhập** (ô email, mật khẩu, nút Login). Màn B là **Hồ sơ**, chỉ hiện ra sau khi đã đăng nhập.

Em đưa AI hai ảnh đã xáo trộn, thứ tự nhận được là [Hồ sơ, Đăng nhập] (sai). Khối (0) hỏi AI từng cặp: "giữa hai màn này, màn nào hợp lý đứng trước?". AI nên trả lời Đăng nhập trước, vì muốn vào Hồ sơ buộc phải đăng nhập (manh mối *gating*).

Cách tổng hợp gọi là **Copeland**: đếm số "trận thắng" của mỗi màn. Ví dụ ba màn, hỏi từng cặp ra A thắng B, A thắng C, B thắng C, thì A thắng 2 trận, B thắng 1, C thắng 0, nên xếp A trước B trước C. Nếu lỡ có vòng mâu thuẫn (A trước B, B trước C, mà C lại trước A), một đoạn code phá vòng bằng cách bỏ cặp mà AI ít chắc chắn nhất.

Lưu ý cùng một luật vàng: lúc sắp thứ tự, AI chỉ thấy các ảnh (đã che đồng hồ, pin, badge để khỏi đọc lén) và mục tiêu. Đáp án vàng chỉ vào ở khâu chấm.

---
# PHẦN 3 — METRIC: CHẤM ĐIỂM THẾ NÀO (công thức + ví dụ)

## 3.0. Nền tảng chung: "khớp nút" dựa vào gì?

Mọi thước đo đều cần biết *"tên AI viết có khớp một nút thật không"*. Em không so chữ cứng, mà so theo nghĩa.

**Hình dung cho dễ:** máy quy mỗi tên nút về một "toạ độ nghĩa". Hai tên cùng nghĩa nằm gần nhau, khác nghĩa nằm xa. "Save" và "Lưu" gần nhau; "Save" và "Settings" xa nhau. Máy đo khoảng cách đó bằng một con số từ −1 đến 1, gọi là cosine *(công thức: $\cos(u,v) = \frac{u\cdot v}{\lVert u\rVert\,\lVert v\rVert}$)*. Đặt một ngưỡng τ (ví dụ 0.55): giống hơn ngưỡng thì coi là khớp nút thật, dưới ngưỡng thì coi là bịa.

Hai điều phải nói để chống bắt bẻ:
- **Vì sao không so chữ cứng?** Nếu so chữ, "Save changes" khác "Save" sẽ bị tính bịa oan dù nút có thật. So theo nghĩa thì hết oan. *(Theo ALOHa, NAACL 2024.)*
- **Ngưỡng τ là núm xoay quan trọng nhất**, nên em không chọn bằng mắt. Em hiệu chỉnh τ trên một tập 80–120 cặp gán nhãn tay, **báo cả precision lẫn recall** của matcher tại ngưỡng đã khóa, và **báo độ nhạy của mọi con số khi τ chạy trong khoảng [0.45, 0.65]**. Vì recall của matcher chưa hoàn hảo, mọi con số faithfulness/grounding em đóng khung *"có điều kiện recall đã đo"*. Khi tutorial nhắc một nút nhiều lần, em cho nút thật đó khớp được nhiều bước (không phạt oan vì lặp).

## 3.1. Chấm trên MỘT màn (dùng lại ví dụ app chi tiêu)

### Thước đo 1 — TRUNG THỰC (không bịa)
**Dựa vào:** mỗi bước *có nhắc tên một nút* thì nút đó có thật không.
$$\text{Trung thực} = 1 - \frac{\text{số bước nhắc nút KHÔNG tồn tại}}{\text{số bước CÓ nhắc tên một nút}}$$
Các bước như "Cuộn xuống", "Đọc tổng tiền" không nhắc nút nào nên không tính vào mẫu số (em báo riêng tỉ lệ này).
**Ví dụ:** bản model-tự-viết có 1 bước bịa ("Submit") trên 4 bước đều nhắc nút → $1 - \tfrac{1}{4} = \mathbf{75\%}$.

> **Một chỗ phải khai trung thực:** sau lớp hậu kiểm, điểm trung thực tăng **một cách tất yếu**, vì lớp đó gỡ chính những bước bịa ra khỏi phép đếm. Cho nên con số có ý nghĩa thật **không phải** "100% sau hậu kiểm", mà là (a) tỉ lệ bịa của bản gốc, và (b) cái giá phải trả là bao nhiêu phần trăm bước thành mô tả chung. Em **không** khẳng định lớp này làm hướng dẫn *đúng hơn* trên một màn, chỉ khẳng định nó loại bỏ tham chiếu tới nút không tồn tại, đổi lại hướng dẫn có thể mơ hồ hơn ("bấm Submit" thành "tìm nút để lưu"). Phần *đúng-ý* em đo ở nhánh nhiều màn, nơi có đáp án vàng.

### Thước đo 2 — ĐÚNG-NHÃN (gọi đúng tên hiển thị)
**Dựa vào:** trong các bước trỏ nút có thật, AI gọi đúng y tên trên màn không (so chuỗi sau khi chuẩn hoá hoa thường).
$$\text{Đúng-nhãn} = \frac{\text{số bước gọi đúng tên}}{\text{số bước trỏ nút có thật}}$$
**Ví dụ:** 3 bước trỏ nút thật (1, 2, 4); bước 4 "Save changes" khác tên thật "Save" → sai tên → $\tfrac{2}{3} \approx \mathbf{67\%}$.

> Chỗ tinh tế: bước 4 không bịa (nút có thật) nhưng gọi sai tên, nên em trừ Đúng-nhãn chứ không tính Bịa. Bước 3 thì bịa hẳn. Hai loại lỗi khác nhau, đo riêng.

### Thước đo 3 — ĐÚNG-CHỖ (grounding, khi AI có cho toạ độ)
**Dựa vào:** nếu AI kèm điểm bấm $(x,y)$, kiểm điểm đó có rơi trong khung nút đã khớp không. Khung mỗi nút là hình chữ nhật $[l,t,r,b]$. Bấm trúng nếu $l \le x \le r$ và $t \le y \le b$.
$$\text{Grounding} = \frac{\text{số bước bấm trúng khung}}{\text{số bước CÓ toạ độ}}$$
**Ví dụ:** AI bảo bấm Save kèm điểm (120, 880); khung nút Save là $[100, 850, 200, 900]$; vì $100 \le 120 \le 200$ và $850 \le 880 \le 900$ nên bấm trúng, tính 1 bước đúng-chỗ.
*(SeeClick/ScreenSpot, ACL 2024.)* Lưu ý: AI chỉ cho toạ độ khi nó tự tin, nên em **báo kèm tỉ lệ bước có toạ độ**; phần không có toạ độ em khai là "không đo được", không lặng lẽ bỏ.

**Sau lớp hậu kiểm:** bước 3 thành mô tả bằng lời nên không còn nhắc nút ma, trung thực tăng. Cái giá em báo thẳng: tỉ lệ bước phải mô tả chung là 1/4, tức **25%**.

## 3.2. Chấm NHIỀU màn (dùng lại ví dụ Đăng nhập → Hồ sơ)

### Thước đo 4 — XẾP ĐÚNG THỨ TỰ (τ thứ-tự-bộ-phận, kiểu Fagin)
**Dựa vào:** so thứ tự AI sắp với thứ tự vàng theo từng cặp màn, nhưng **chỉ tính những cặp BẮT BUỘC**. Gọi $M$ là tập cặp bắt buộc, $C$ là số cặp AI xếp đúng chiều, $D$ là số cặp xếp ngược:
$$\tau = \frac{C - D}{|M|} \in [-1, +1]$$
(+1 = trùng khít, 0 = như đoán bừa, −1 = đảo ngược.)

> **Lưu ý kỹ thuật (để metrics reviewer không bắt bẻ):** đây là **τ thứ-tự-bộ-phận** (Fagin et al.), **không phải** Kendall τ-b. τ-b hiệu chỉnh cho các cặp *hòa hạng*; ở đây không có hòa vì AI luôn sinh một thứ tự chặt. Cái em bỏ qua là các cặp *không-so-sánh-được* ở phía đáp án (cặp tự do), khác với hòa. *(Nền: Kendall 1938; Lapata, CL 2006.)*

**Ví dụ:** luồng 3 màn, vàng A < B < C; AI sắp A, C, B. Giả sử cả ba cặp đều bắt buộc:

| Cặp | Vàng | AI xếp | |
|---|---|---|---|
| (A,B) | A trước B | A trước B | thuận |
| (A,C) | A trước C | A trước C | thuận |
| (B,C) | B trước C | C trước B | **nghịch** |

$\tau = \frac{2-1}{3} = \mathbf{+0.33}$. Nếu (B,C) là cặp **tự do** (đảo cũng được), em bỏ nó ra, chỉ còn (A,B) và (A,C) đều thuận → $\tau = +1$ (AI không bị phạt oan).

> **Chống tự-ra-đề-tự-chấm — nhưng khai đúng giới hạn:** nhãn "cặp nào bắt buộc" em suy từ đáp án vàng, không lấy từ AI. Quy tắc là: màn B chỉ hiện sau thao tác vàng ở màn A thì (A trước B) bắt buộc. **Đây là quy tắc XẤP XỈ**: AndroidControl chỉ có một quỹ đạo người demo, nên "B xuất hiện sau A" chưa chắc nghĩa "B đòi hỏi A". Vì vậy em (a) cho người kiểm 50–80 cặp báo phần trăm khớp, (b) đo độ nhạy của kết quả khi gán nhãn sai 10%, (c) báo thêm τ thô trên toàn bộ cặp làm điểm sàn.

### Thước đo 5 — LÀM-THEO-TỚI-ĐÍCH (Step-SR), trục đo đúng-ý
**Dựa vào:** vì có đáp án vàng từng bước, kiểm xem làm theo hướng dẫn AI thì mỗi bước có khớp thao tác vàng không. Một bước đúng nếu đúng loại thao tác (bấm, gõ, cuộn) và điểm bấm cách toạ độ vàng không quá 14% kích thước màn, hoặc rơi cùng khung nút với đáp án vàng *(định nghĩa từ AITW, NeurIPS 2023)*.
$$\text{Step-SR} = \frac{\text{số bước làm đúng}}{\text{số bước của đáp án vàng}}$$
Em căn theo độ dài quỹ đạo vàng và phạt cả bước thiếu lẫn bước thừa, để AI không thể "ăn gian" bằng cách viết thiếu hoặc nhồi bước rác.

> **Khai đúng giới hạn:** Step-SR so với *một* quỹ đạo vàng, nên một hướng dẫn đúng nhưng đi đường khác vẫn bị tính sai. Vì vậy nó là **cận dưới** của tính dùng được, không phải chân lý tuyệt đối. Em báo rõ hai chế độ: bản *teacher-forced* (mỗi bước đưa màn vàng) làm trục tham chiếu chuẩn ngành; bản *free-rollout* (AI tự sắp rồi đi) báo riêng, để tách lỗi sắp thứ tự khỏi lỗi thao tác. Đây là phần em đặt trọng tâm cho nhánh có đáp án vàng. *(AndroidControl, NeurIPS 2024.)*

---
# PHẦN 4 — VÌ SAO TIN ĐƯỢC

## 4.1. Chống "ăn gian" (vòng lập luận) — hai tầng
Cái bẫy: nếu dùng cùng một công cụ vừa quyết "bước nào bịa, đem mô tả lại" vừa chấm "còn bịa không", thì sau hậu kiểm điểm trung thực đương nhiên 100%, vì đã loại sạch cái mà chính công cụ đó chê. Đó là trò chơi chữ.

Cách em chống. Ở nhánh một màn, việc quyết dùng một công cụ đo nghĩa A, còn việc chấm dùng một công cụ đo nghĩa B của hãng khác, huấn luyện độc lập, cộng thêm một bộ chấm bằng LLM thuộc họ khác với model viết. Và quan trọng, em không khoe điểm 100%; em khoe tỉ lệ bịa của bản gốc, tức đo độ lớn của vấn đề, chấm bằng công cụ độc lập. Ở nhánh nhiều màn, nhãn "cặp bắt buộc" suy từ đáp án vàng, không từ AI.

## 4.2. Tự kiểm chính thước đo (perturbation)
Em tự bơm lỗi đã biết vào một hướng dẫn đúng rồi xem thước đo có bắt được không. Ví dụ chèn một nút bịa rõ ràng không có trên màn (như "Export to PDF" vào màn không hề có chức năng đó) thì trung thực phải tụt. Em báo cả đường cong phát hiện theo khoảng cách nghĩa, **đặc biệt là vùng gần đồng nghĩa** (Confirm với Save), nơi thước đo dễ bắt hụt nhất. Em đo đúng chỗ khó đó để bộc lộ giới hạn của thước đo chứ không giấu.

Phải nói thẳng: perturbation chứng minh thước đo **nhạy** với lỗi (đúng/sai), chứ chưa chứng minh nó **bám phán đoán của người** về "trung thực hay hữu ích". Phần sau gọi là convergent validity. Em xử lý bằng một mẫu chuyên gia nhỏ đăng ký trước (báo độ đồng thuận và tương quan với người), và khai rõ rằng perturbation một mình là chưa đủ. *(Tiền lệ perturbation: Sai et al., EMNLP 2021.)*

## 4.3. Thống kê chặt
Em gộp theo ứng dụng khi tính khoảng tin cậy. Ví dụ 80 màn nhưng chỉ từ 5 app; 16 màn cùng một app rất giống nhau, nên thực chất chỉ có cỡ 5 mẫu độc lập, không phải 80. Nếu tính như 80 thì khoảng sai số trông hẹp giả tạo. Em còn báo độ lớn hiệu ứng kèm khoảng tin cậy 95% (không chỉ "có khác hay không"), hiệu chỉnh đa kiểm định Holm cho năm thước đo, cố định seed và lấy 10.000 lần lặp lại, và đặt ít nhất 30 episode cho mỗi mốc số-màn. Mọi giả thuyết và ngưỡng em đăng ký trước khi nhìn kết quả, theo nguyên tắc "kể cả kết quả ra không khác biệt thì vẫn là đóng góp".

---
# PHẦN 5 — ĐÓNG GÓP, ĐỘ MỚI, GIỚI HẠN

## 5.1. Hai đóng góp, và vì sao lớp sinh là NGHIÊN CỨU chứ không phải kỹ thuật
- **Đóng góp một — cách sinh ít bịa hơn.** Lớp hậu kiểm gắn được vào bất kỳ model nào. Em **không** trình nó như một mẹo. Em kiểm nó như một giả thuyết có thể sai. Phương án ngây thơ là "sửa nút bịa thành nút thật gần nhất"; em đã thử và **đo được** rằng nó gây lỗi ngầm (đổi "Submit" thành "Save" trong khi đúng phải là một nút khác). Chính vì có một phương án thay thế thất bại đo được mà em chốt phương án "chỉ mô tả, không đoán", kèm báo cái giá. Có đối chứng thất bại đo được thì đây là kết quả thực nghiệm, không phải lựa chọn tùy tiện.
- **Đóng góp hai — cách đánh giá không bản mẫu, không tự chấm.** Đây là phần phương pháp luận nặng nhất: tách công cụ quyết khỏi công cụ chấm, suy nhãn từ đáp án vàng, và tự bơm lỗi để kiểm thước đo.

Hai phần gắn liền: lớp sinh vừa hữu ích tự thân, vừa là ca thử chứng minh cách đánh giá của em đủ nhạy để bắt được khác biệt giữa hai cách sinh.

## 5.2. Kết quả sơ bộ (trung thực về trạng thái)
Em đã chạy thử quy mô nhỏ (10 màn, miễn phí) để kiểm pipeline: tỉ lệ bịa của bản gốc đáng kể (cỡ một phần tư số bước), và lớp hậu kiểm kéo điểm trung thực lên rõ ở mọi ngưỡng, **nhưng** cỡ mẫu nhỏ nên khoảng tin cậy còn chạm 0. Em đang chạy bản chính trên 90 màn của 18 ứng dụng để có bảng số và khoảng tin cậy đầy đủ. Phần nhiều màn (thứ tự + Step-SR) là trục em phát triển tiếp; buổi này em xin trình **thiết kế + sơ bộ**, chưa phải bảng số cuối.

## 5.3. Giới hạn em chủ động khai
- Nhánh một màn chỉ đo *không-bịa*, chưa đo *đúng-ý*. Đúng-ý em đo ở nhánh nhiều màn bằng Step-SR có đáp án vàng.
- Điểm trung thực 100% sau hậu kiểm là trần do thiết kế, nên em báo tỉ lệ bịa của bản gốc, không trưng 100%.
- Danh sách nút là ảnh chụp một trạng thái, nên nút sau khi cuộn có thể bị nhầm là "không có"; em lọc hoặc đánh dấu các bước đó.
- Lúc đánh giá em dùng danh sách nút có sẵn trong dataset; lúc triển khai thật chỉ từ một ảnh thì cần một bộ dò nút (có sai số), nên em tự đo độ phủ của bộ dò trước (cổng kiểm K1) và đóng khung "số có điều kiện". Vì lớp hậu kiểm đặt bên cạnh chứ không chặn khâu sinh, bộ dò sót nút chỉ hạ độ tin của phép đo, không cắt mất bước nào.
- Step-SR và nhãn cặp bắt buộc đều suy từ một quỹ đạo vàng, nên là cận dưới và xấp xỉ, không phải chân lý tuyệt đối; em audit người và báo độ nhạy khi nhãn sai.
- Chưa có bảng số tiếng Việt (thiếu dữ liệu chuẩn tiếng Việt); định lượng làm trên dữ liệu tiếng Anh, tiếng Việt làm demo.

---
# PHẦN DỰ PHÒNG — NẾU THẦY HỎI (không đọc, để thủ)

**"Vậy là cho model thấy luôn danh sách nút à?"** → Dạ không. Lúc sinh, model chỉ thấy ảnh và câu hỏi; câu hỏi cũng không chứa tên nút (em kiểm trùng từ bằng 0). Danh sách nút chỉ vào ở khâu đối chiếu và chấm, bằng thuật toán.

**"Lớp hậu kiểm chỉ là tìm-thay nút ma bằng câu mơ hồ, rồi tự khen vì hết nút ma?"** → Em không khen điểm 100% (đó là trần do thiết kế). Cái em báo là tỉ lệ bịa của bản gốc và cái giá fallback. Và lớp này là kết quả thực nghiệm: em đã đo phương án "sửa thành nút gần nhất" gây lỗi ngầm, nên mới chốt "chỉ mô tả".

**"Cái này chỉ đo không-bịa, đâu đo đúng-ý?"** → Đúng, em thừa nhận. Đúng-ý em đo ở nhánh nhiều màn bằng Step-SR trên AndroidControl có đáp án vàng. Hai nhánh bù nhau.

**"Step-SR so với một đáp án, hướng dẫn đúng kiểu khác thì sao?"** → Nên em gọi nó là cận dưới, không phải chân lý; và báo cả bản teacher-forced lẫn free-rollout để tách lỗi.

**"τ-b của em công thức không giống τ-b chuẩn?"** → Dạ em gọi đúng tên là τ thứ-tự-bộ-phận kiểu Fagin, chỉ tính cặp bắt buộc, không phải τ-b hiệu chỉnh hòa. Em đã sửa đúng nhãn.

**"AI chấm AI tin được không?"** → Em không cho AI chấm hay-dở. Em chỉ giao một phán đoán nhị phân, có sẵn tham chiếu, và đo độ chính xác của nó với nhãn người.

**"Ngưỡng τ tự chọn?"** → Em hiệu chỉnh trên tập gán nhãn người, khóa trước khi chạy, báo cả precision lẫn recall và độ nhạy theo dải ngưỡng.

**"Làm sao AI biết thứ tự, hay đọc lén đồng hồ pin?"** → Em che thanh trạng thái, đồng hồ, pin, mã hoá lại ảnh; và có kiểm tra: một bộ chỉ nhìn pixel không suy ra thứ tự tốt hơn đoán bừa.

**"2026 có GPT-5 rồi còn ý nghĩa?"** → Kể cả model mạnh nhất vẫn còn bịa một tỉ lệ, vẫn sai thứ tự. Lớp và cách đánh giá vẫn áp dụng được; và nếu một ngày model mạnh tới mức hết bịa, thì chính cách đánh giá của em là thứ chứng minh được điều đó.

**"Đủ chuẩn thạc sĩ chưa?"** → Cái khó không nằm ở code, mà ở chỗ làm sao chấm điểm một thứ không có bản mẫu mà không rơi vào tự chấm. Em giải bằng tách công cụ, suy nhãn từ đáp án vàng, và bơm lỗi kiểm thước đo. Đó là phần nghiên cứu. Cộng với hai đóng góp, hai nhánh đánh giá, dataset bình duyệt có đáp án vàng, và độ chặt thống kê.
