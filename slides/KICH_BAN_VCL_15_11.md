# Kịch bản trình bày VCL 2026 (bản 15/11) và bộ câu hỏi dự kiến

**Bài:** *Sinh hướng dẫn sử dụng phần mềm từ ảnh chụp màn hình và mục tiêu người dùng: xây dựng
ngữ liệu quy chiếu tự động khi phần tử giao diện không có tên cụ thể*
Lê Đoàn Phương Uyên & Nguyễn Hồng Bửu Long · Hội thảo VCL 2026, HUFLIT, 27/11/2026.

**Khung giờ:** 15 phút trình bày + hỏi đáp. Lời nói dưới đây khoảng **12–13 phút** ở nhịp nói
chậm, chừa 2 phút cho lúc chỉ bảng, chuyển slide.

**Nguồn số:** mọi con số lấy từ `paper/vcl2026/main.tex` (bản đã nộp). Không thêm số nào ngoài bài
vào phần trình bày chính. Phần hỏi đáp có vài số từ bài đồng hành và luận văn, đã ghi rõ chỗ đó.

**Cách đọc tệp này:**
- *Trên slide* là thứ được in lên slide (để agent dựng slide làm theo). Chữ trên slide càng ít càng tốt.
- *Lời nói* là phần bạn nói. Không cần học thuộc, nắm ý và các con số in đậm là đủ.

---

## Slide 1 · Bìa (~15 giây)

**Trên slide:** tên bài (3 dòng) · hai tác giả · Khoa CNTT, Trường ĐH Khoa học Tự nhiên, ĐHQG-HCM ·
VCL 2026, HUFLIT, 27/11/2026.

**Lời nói:**
Kính chào quý thầy cô và các bạn. Tôi là Lê Đoàn Phương Uyên, Khoa Công nghệ Thông tin, Trường Đại học
Khoa học Tự nhiên. Đây là bài làm chung với thầy Nguyễn Hồng Bửu Long. Bài nói về cách chúng tôi
dựng một bộ ngữ liệu để dạy mô hình viết câu hướng dẫn thao tác trên điện thoại.

---

## Slide 2 · Bài toán qua một ví dụ (~50 giây)

**Trên slide:** bên trái là ảnh màn hình điện thoại (dùng ảnh `paper/vcl2026/hinh/fig_moneo.png`
hoặc cắt phần màn hình), bên phải hai hộp:
- *Đầu vào:* ảnh màn hình + mục tiêu của người dùng
- *Đầu ra:* một câu, ví dụ "Chạm vào biểu tượng bút chì ở góc trên bên phải của ghi chú"
Dòng nhỏ dưới cùng: *Tác tử giao diện: câu → toạ độ. Bài này: ảnh + mục tiêu → câu cho người đọc.*

**Lời nói:**
Các tác tử điều khiển giao diện hiện nay thường nhận một câu lệnh rồi tự tìm toạ độ để bấm. Chúng tôi
làm chiều ngược lại. Hệ thống nhận ảnh màn hình và mục tiêu của người dùng, rồi viết ra một câu để
**người** đọc biết phải chạm vào đâu. Ví dụ: "chạm vào biểu tượng bút chì ở góc trên bên phải của ghi chú".

Loại câu này có ích cho người lớn tuổi, cho người lần đầu dùng một ứng dụng, và cho người dùng trình
đọc màn hình.

Về mặt ngôn ngữ học, đây chính là bài toán **sinh biểu thức quy chiếu** theo cách Dale và Reiter phát
biểu: câu sinh ra phải đủ để người nghe nhận ra đúng một đối tượng, không lẫn với đối tượng khác cùng
có mặt.

---

## Slide 3 · Cái khó: phần tử giao diện thường không có tên (~60 giây)

**Trên slide:** ba con số lớn, mỗi số một ô:
- **12,6%** phần tử có nhãn văn bản (đo trên 120 màn ngẫu nhiên; 22/120 màn không có phần tử nào có tên)
- **22,0%** phần tử cần chạm không có tên
- **7,6%** phần tử cần chạm trùng tên với phần tử khác
Dòng dưới: *Gộp lại: 29,6% số bước, gần một phần ba.*

**Lời nói:**
Điểm làm giao diện khác ảnh tự nhiên nằm ở mấy con số này.

Mỗi màn hình Android có một cây trợ năng, tức bản liệt kê các phần tử đang hiển thị cùng nhãn chữ của
chúng. Chúng tôi lấy ngẫu nhiên 120 màn trong gần một trăm nghìn màn và đếm: chỉ **12,6%** phần tử có
nhãn chữ. Có 22 màn không có phần tử nào có tên.

Trên 41.099 bước chạm mà chúng tôi dựng nhãn, **22%** phần tử cần chạm không có tên, và **7,6%** trùng tên
với một phần tử khác trên cùng màn. Hai nhóm này không giao nhau, nên cộng lại là gần **30%** số bước.

Ở ảnh tự nhiên, con mèo thì gọi là con mèo, cái ghế thì gọi là cái ghế. Ở đây, cứ ba lần thì gần một
lần không có tên nào để gọi. Người viết câu buộc phải chỉ bằng vị trí hoặc bằng quan hệ với chữ bên
cạnh, kiểu "biểu tượng nằm ngay trên chữ Gmail".

---

## Slide 4 · Vì sao phải có dữ liệu riêng (~40 giây)

**Trên slide:** hai cột so sánh ngắn:
- *Dòng sinh biểu thức quy chiếu (Mao 2016, Luo 2017, Yu 2017):* ảnh tự nhiên, đối tượng có danh từ, quan hệ chỉ là phương án bổ sung.
- *Miền giao diện:* 22% không có tên, quan hệ với chữ lân cận thành phương tiện chính.
Dòng dưới: *Widget Captioning: nhãn do người viết, mô tả một widget tách rời. AndroidControl: câu chỉ dẫn là đầu vào. Bài này: câu chỉ dẫn là đầu ra.*

**Lời nói:**
Khung khái niệm thì chúng tôi dùng lại của dòng sinh biểu thức quy chiếu, kể cả ý mô tả bằng quan hệ
của Dale và Haddock. Chỗ khác là miền này đảo ngược thứ tự ưu tiên: ở ảnh tự nhiên quan hệ là phương án
phụ, còn ở đây nhiều khi nó là cách duy nhất.

Công trình gần nhất là Widget Captioning, nhưng nhãn của họ do người viết và mô tả một widget đứng
riêng. Còn bộ AndroidControl của Google có sẵn câu chỉ dẫn theo từng bước, nhưng họ dùng câu đó làm
đầu vào cho tác tử. Chúng tôi dùng nó làm đầu ra. Hiện chưa có bộ dữ liệu công khai nào dựng sẵn cho
đúng tác vụ này, nên phải tự dựng.

---

## Slide 5 · Ghép hai bản phát hành, và cách kiểm ghép đúng (~60 giây)

**Trên slide:** bảng nhỏ hai dòng:
| bản phát hành | có | thiếu |
|---|---|---|
| HarrytheOrange/parsed_AndroidControl | câu chỉ dẫn, cây trợ năng | ảnh |
| ckg/AndroidControlParsedWithImages-20k | ảnh | câu chỉ dẫn theo bước |
Bên dưới: *ghép theo (episode_id, step_id)* và một biểu đồ cột hai cột: **ghép đúng 48,3%** vs **cố ý ghép lệch 19,6%**.

**Lời nói:**
Không bản phát hành công khai nào của AndroidControl có đủ ba thứ chúng tôi cần: câu chỉ dẫn, ảnh và
cây trợ năng. Nên chúng tôi ghép hai bản theo mã chuỗi thao tác và mã bước.

Lỗi nguy hiểm nhất ở đây là ghép lệch một bước. Số dòng vẫn đủ, huấn luyện vẫn chạy, mọi thứ trông
bình thường, nhưng mô hình học ảnh của bước này với câu của bước kia.

Cách kiểm của chúng tôi: đọc chữ bằng OCR ngay tại điểm chạm, rồi xem chữ đó có nằm trong câu chỉ dẫn
không. Ghép đúng thì khớp **48,3%**. Để có mốc so, chúng tôi cố ý ghép lệch một bước, thì chỉ còn
**19,6%**.

Con số 48% đứng một mình không nói lên gì, vì OCR có lỗi và người viết câu không nhất thiết lặp lại chữ
trên nút. Cái đáng tin là khoảng cách giữa hai con số.

---

## Slide 6 · Cây trợ năng không đủ, nên phải đọc chữ bằng OCR (~45 giây)

**Trên slide:**
- Một màn: trung vị **86** phần tử, nhưng chỉ 12,6% có tên
- OCR (RapidOCR, chạy CPU) trên **100%** ảnh: 64.567 bản ghi huấn luyện, 6.958 bản ghi kiểm tra
- Tên lấy được: **8.581** từ cây trợ năng · **23.480** từ OCR (khoảng 1 : 2,7)
- Nguyên tắc: *để trống còn hơn ghi sai*

**Lời nói:**
Cây trợ năng lẽ ra là nguồn tên tự nhiên nhất, nhưng như vừa thấy, nó thiếu rất nhiều. Nên toàn bộ ảnh
được đưa qua OCR. Kết quả là trong hơn 32 nghìn tên lấy được, cứ một tên từ cây trợ năng thì có
khoảng 2,7 tên từ OCR.

OCR có hai kiểu sai. Kiểu thứ nhất là đọc biểu tượng thành chữ cái, sinh ra một chuỗi trông như tên thật.
Kiểu thứ hai là dính chữ, ví dụ "Turnon". Kiểu thứ nhất nguy hiểm hơn.

Nguyên tắc chúng tôi theo suốt bài: với dữ liệu huấn luyện, để trống ô tên còn đỡ hơn ghi sai. Ô trống
chỉ làm mô hình mất một mẫu học. Ô ghi sai thì dạy mô hình gọi phần tử bằng một cái tên không có trên màn.

---

## Slide 7 · Nhãn bốn ô (~60 giây)

**Trên slide:** sơ đồ bốn ô nằm ngang:
`vai trò | tên | toạ độ | dấu hiệu phân biệt`
Ví dụ in mono:
`<desc>tappable text | Search here | <point>440,91</point> | just above the text "Coffee"</desc>`
Ghi chú nhỏ: *Chỉ dựng cho bước chạm. Phần tử cần chạm = hộp bao nhỏ nhất chứa điểm chạm.*

**Lời nói:**
Đây là nhãn mà mô hình phải học để sinh ra, trước khi viết câu. Nhãn gồm bốn ô.

Ô vai trò cho biết đó là nút, ô nhập hay mục danh sách. Ô tên là chữ hiển thị, lấy từ cây trợ năng trước,
OCR sau. Ô toạ độ là điểm chạm, quy về thang 0 đến 1.000. Và ô thứ tư là dấu hiệu phân biệt, một mệnh
đề cho biết phần tử này khác các phần tử giống nó ở chỗ nào.

Để biết phần tử cần chạm là cái nào, chúng tôi lấy hộp bao **nhỏ nhất** chứa điểm chạm. Phải lấy hộp
nhỏ nhất vì cây trợ năng lồng nhiều tầng: một điểm chạm nằm trong hàng chục hộp cùng lúc, từ khung cả
màn hình cho tới cái nút thật.

Cả bốn ô đều dựng bằng quy tắc, không có ai viết tay nhãn nào.

---

## Slide 8 · Ví dụ thật: mỏ neo chữ (~55 giây)

**Trên slide:** hình `paper/vcl2026/hinh/fig_moneo.png` chiếm gần hết slide. Dưới hình:
`<desc>icon | (no name) | <point>111,903</point> | just above the text "Gmail"</desc>`
Câu của người chú thích: *"Click on the gmail option"*

**Lời nói:**
Đây là một bước thật trong tập kiểm tra, thuộc trường hợp khó. Khung xanh lá là phần tử cần chạm. Ba
khung cam là ba biểu tượng cùng loại. Cả bốn biểu tượng đều không có tên trong cây trợ năng.

Ba ô đầu của nhãn lúc này chỉ nói được "đây là một biểu tượng, không có tên". Toàn bộ việc chỉ đường
dồn vào ô thứ tư. Chương trình tìm chuỗi chữ gần nhất nằm ngoài hộp bao, ở đây là chữ "Gmail", cách tâm
114,5 pixel, và lấy nó làm **mỏ neo**: "nằm ngay trên chữ Gmail".

Điều đáng chú ý là người chú thích, khi viết câu cho đúng bước này, cũng quy chiếu qua đúng chữ đó:
"Click on the gmail option".

---

## Slide 9 · Hai bộ lọc, thêm vào sau khi thấy nhãn nhiễu (~45 giây)

**Trên slide:** hai hộp:
- **Bộ lọc nhãn trợ năng:** loại tên kiểu mã nguồn, chuỗi số dài, "No label specified", "unlabeled"… → loại **14,7%** nhãn trên mẫu thử 1.074 nhãn
- **Bộ lọc hình học:** chỉ lấy tên OCR khi hộp < **25%** màn → tác động **2,2%** số bước. Ví dụ: hộp phủ 95% màn cho chuỗi "THEFELLOWSHIPOF THE RING"

**Lời nói:**
Hai bộ lọc này không có trong thiết kế ban đầu. Chúng tôi thêm vào sau khi đọc tay một mẫu thử 1.074
nhãn và thấy nhãn bị nhiễu.

Bộ lọc thứ nhất loại những chuỗi đúng cú pháp nhưng người dùng không dựa vào được để tìm nút, ví dụ tên
biến trong mã nguồn hay chữ "unlabeled". Trên mẫu thử nó loại 14,7% nhãn.

Bộ lọc thứ hai chặn trường hợp hộp quá lớn. Có hộp phủ 95% màn hình và OCR đọc ra cả tên phim bên trong.
Chữ đó không còn chỉ về cái nút nữa. Nên chỉ khi hộp nhỏ hơn một phần tư màn thì mới lấy tên từ OCR.

Cả hai bộ lọc cùng một tinh thần: không chắc thì để trống.

---

## Slide 10 · Ô thứ tư phải làm lại: từ 7,3% lên 75,9% (~55 giây)

**Trên slide:** hai cột trước/sau:
- **Bản đầu:** 7,3% giải quyết được mơ hồ · 85,8% chỉ đếm ("một trong bảy phần tử cùng loại")
- **Bản làm lại:** 75,9% trên mẫu thử · **75,3%** trên toàn bộ 41.099 nhãn
Dòng nhỏ: *737/737 mỏ neo đúng hướng (kiểm tay). Đúng hướng chưa có nghĩa là hữu ích.*

**Lời nói:**
Đây là phần chúng tôi phải làm lại từ đầu. Bản đầu của ô thứ tư chỉ giải quyết được **7,3%** số trường
hợp. Còn tới 85,8% là câu đếm, kiểu "một trong bảy phần tử cùng loại". Câu đó đúng, nhưng chỉ báo là có
mơ hồ, chứ không giúp ai chọn được phần tử nào.

Chúng tôi sắp lại thứ tự quy tắc: ưu tiên mệnh đề nào giải quyết được mơ hồ, và thêm mỏ neo chữ như ví
dụ Gmail vừa rồi. Trên cùng mẫu thử, tỉ lệ đi từ 7,3% lên **75,9%**. Trên toàn bộ ngữ liệu là **75,3%**.

Chúng tôi kiểm tay cả 737 mỏ neo của mẫu thử, đúng hướng cả 737. Nhưng cần nói rõ: đúng hướng là do
cách tính, còn mỏ neo có thật sự giúp người dùng tìm ra nút hay không thì phải đo bằng cách khác. Phần
sau sẽ nói tới.

---

## Slide 11 · Độ phủ chưa đều: nhóm cần nhất lại được phủ kém nhất (~60 giây)

**Trên slide:** bảng rút gọn:
| tầng tên của phần tử | số nhãn | giải quyết được mơ hồ |
|---|---|---|
| tên rõ ràng | 30.252 | **80,1%** |
| không có tên | 9.038 | 66,7% |
| chỉ có ký hiệu (vd. "Q", "?") | 1.809 | **37,5%** |
| toàn bộ | 41.099 | 75,3% |

**Lời nói:**
Con số 75,3% là trung bình, và trung bình này che mất một chuyện không vui.

Nhóm phần tử có tên rõ ràng, tức nhóm mà chỉ cần gọi tên là đủ, lại được phủ tốt nhất: **80,1%**. Nhóm
không có tên được 66,7%. Còn nhóm chỉ mang một ký hiệu, ví dụ một chữ "Q" đứng lẻ, chỉ được **37,5%**.

Nguyên nhân là cơ học. Mỏ neo cần một chuỗi chữ đủ gần. Mà vùng màn hình dày biểu tượng không tên thì
thường cũng là vùng ít chữ. Nghĩa là chỗ cần dấu hiệu phân biệt nhất lại là chỗ quy tắc khó tìm được
mỏ neo nhất. Đây là hạn chế chính của bộ ngữ liệu, và chúng tôi nêu thẳng trong bài.

---

## Slide 12 · Người chú thích và quy trình tự động chọn cùng chiến lược (~50 giây)

**Trên slide:** ba con số, chia hai phía:
- *Phía màn hình:* **55,6%** số bước có phần tử cạnh tranh trong khoảng 80–350 px · **91,6%** có phần tử cùng vai trò (trung vị 8)
- *Phía ngôn ngữ:* **32,5%** câu của người dùng từ chỉ vị trí/thứ tự · **67,2%** dấu hiệu của quy trình là quan hệ với chữ lân cận

**Lời nói:**
Câu hỏi tự nhiên là: phân biệt có thật là vấn đề, hay chỉ là chúng tôi tự đặt ra?

Phía màn hình: hơn một nửa số bước, 55,6%, có ít nhất một phần tử cạnh tranh nằm khá gần phần tử cần
chạm. Và 91,6% số bước có phần tử cùng loại, trung vị tám cái một màn.

Phía ngôn ngữ: trong hơn 41 nghìn câu do người chú thích viết, khoảng một phần ba, **32,5%**, phải dùng
từ chỉ vị trí như "trên", "dưới", "góc phải", "đầu tiên". Còn quy trình của chúng tôi thì cho 67,2% dấu
hiệu là quan hệ với chữ bên cạnh.

Cả người lẫn máy đều chuyển từ gọi tên sang chỉ vị trí. Khác biệt còn lại là người nhìn thấy hình dạng
biểu tượng, như cái kính lúp, rồi gọi là "search icon". Quy trình của chúng tôi chỉ đọc được chữ.

---

## Slide 13 · Quy mô và cách chia tập (~45 giây)

**Trên slide:**
| | huấn luyện | kiểm tra |
|---|---|---|
| số bước | 64.567 | 6.958 |
| bước chạm | 41.191 | 4.463 |
| số tác vụ | 12.895 | 1.432 |
| nhãn GUIRefCorpus | 41.099 | 4.448 |
Ba dòng cảnh báo nhỏ: *chia theo tác vụ, 0 tác vụ trùng* · *không tách được cách diễn đạt* · *không phải tập ứng dụng chưa thấy (95,6% ứng dụng có ở tập huấn luyện)*

**Lời nói:**
Về quy mô: tập huấn luyện hơn 64 nghìn bước, trong đó hơn 41 nghìn bước chạm. Tập kiểm tra gần 7 nghìn
bước. Bộ nhãn chúng tôi đặt tên là **GUIRefCorpus**, 41.099 dòng cho huấn luyện và 4.448 dòng cho kiểm tra.

Tập được chia theo tác vụ, không chia ngẫu nhiên theo dòng, vì các màn trong cùng một tác vụ gần như
giống nhau. Kiểm rò rỉ trên toàn bộ dữ liệu: không có tác vụ nào trùng.

Nhưng chia theo tác vụ chỉ bảo đảm đúng một điều đó. Nó không tách được cách nói, vì người chú thích
hay lặp lại những câu như "click on the search bar". Và tập kiểm tra cũng không phải tập ứng dụng chưa
từng thấy. Chúng tôi nêu cả hai để không ai đọc kết quả rộng hơn mức dữ liệu cho phép.

---

## Slide 14 · Kiểm chất lượng bằng một nguồn nằm ngoài quy trình (~65 giây)

**Trên slide:** biểu đồ ba cột:
- ô tên xuất hiện nguyên văn trong câu của người: **53,5%** (1.875/3.505)
- ghép với câu của bước liền sau (bất kỳ): **5,4%**
- ghép với bước liền sau trong cùng chuỗi thao tác (đối chứng khó): **7,6%**
Dòng dưới: *Quy trình dựng nhãn không đọc câu chỉ dẫn ở bất kỳ bước nào. 53,5% là chặn dưới.*

**Lời nói:**
Đây là phần quan trọng nhất của bài.

Bộ ngữ liệu dựng bằng quy tắc có một điểm yếu: mọi số đo tính từ chính quy tắc chỉ cho biết quy tắc
chạy đúng như đã viết, chứ không cho biết nhãn có đúng không. Cần một nguồn nằm ngoài.

Nguồn đó là câu do người chú thích viết. Quy trình dựng nhãn của chúng tôi không đọc câu này ở bất kỳ
bước nào. Nên nếu tên mà quy trình đặt cho phần tử lại xuất hiện đúng nguyên văn trong câu của người, đó
là một sự trùng khớp từ bên ngoài, không phải tự kiểm.

Kết quả: **53,5%**. Để biết con số này cao hay thấp, chúng tôi đem đúng những cái tên đó ghép với câu
của bước kế tiếp. Chỉ khớp 5,4%. Có người sẽ nói đối chứng đó dễ quá, nên chúng tôi làm khó hơn: chỉ
ghép với bước kế tiếp trong cùng một chuỗi thao tác, tức hai màn rất giống nhau. Tỉ lệ khớp nhầm lên
**7,6%**. Vẫn thấp hơn khoảng **bảy lần**.

Và 53,5% không có nghĩa là gần một nửa số tên bị sai. Người chú thích hay gọi bằng tên loại, kiểu "the
search bar" cho ô mang chữ "Search here", mà phép so nguyên văn thì không tính trường hợp đó. Nên 53,5%
là chặn dưới.

---

## Slide 15 · Hạn chế (~40 giây)

**Trên slide:** ba gạch:
- **24,7%** dấu hiệu chưa giải quyết được mơ hồ (đã rõ nguyên nhân, sửa được)
- So với nguồn ngoài mới chạm **1/4 ô** (ô tên); ô dấu hiệu chưa được người dùng kiểm
- Bản gốc: không có nhãn chuẩn cho OCR; chuỗi mục tiêu bị cắt (99,4% không kết thúc bằng dấu câu)

**Lời nói:**
Ba hạn chế chúng tôi nêu rõ.

Một, còn 24,7% dấu hiệu chưa giải quyết được mơ hồ. Nguyên nhân đã rõ nên sửa được, hướng đầu tiên là
mở rộng nguồn neo sang các phần tử cùng vai trò, vì 91,6% số bước có sẵn những phần tử như vậy.

Hai, phép so với nguồn ngoài mới chạm được ô tên. Ô dấu hiệu phân biệt muốn kiểm đúng thì phải hỏi thẳng
người dùng xem đọc nhãn có tìm ra nút không. Chúng tôi chưa làm được.

Ba, hai giới hạn từ chính bản phát hành gốc: không có nhãn chuẩn cho OCR, và chuỗi mục tiêu của tác vụ bị
cắt cụt ngay từ nguồn.

---

## Slide 16 · Kết luận (~45 giây)

**Trên slide:** ba dòng:
- GUIRefCorpus: **41.099 + 4.448** nhãn bốn ô, dựng hoàn toàn tự động từ AndroidControl
- Ô dấu hiệu phân biệt: **7,3% → 75,3%**
- Đối chiếu ngoài quy trình: **53,5%** vs **7,6%** (đối chứng khó)
Dòng cuối nhỏ: *Phần huấn luyện mô hình: bài đồng hành.*

**Lời nói:**
Tóm lại, chúng tôi dựng một quy trình hoàn toàn tự động, biến AndroidControl thành bộ ngữ liệu
GUIRefCorpus cho bài toán sinh biểu thức quy chiếu trên giao diện. "Hoàn toàn tự động" là nói về khâu
dán nhãn. Con người vẫn tham gia, nhưng chỉ để kiểm. Mỗi lần thấy nhãn sai, chúng tôi sửa bộ quy tắc rồi
dựng lại toàn bộ, không sửa tay từng nhãn.

Ô dấu hiệu phân biệt đi từ 7,3% lên 75,3%. Và chỗ dựa chính là phép đối chiếu với câu của người chú thích:
53,5% so với 7,6% ở đối chứng khó.

Phần huấn luyện mô hình trên bộ ngữ liệu này nằm ở bài đồng hành của nhóm.

---

## Slide 17 · Cảm ơn (~10 giây)

**Trên slide:** "Cảm ơn quý thầy cô và các bạn đã lắng nghe" · email liên hệ.

**Lời nói:**
Phần trình bày của tôi đến đây là hết. Cảm ơn quý thầy cô và các bạn đã lắng nghe, tôi rất mong nhận
được câu hỏi và góp ý.

---
---

# BỘ CÂU HỎI DỰ KIẾN VÀ CÁCH TRẢ LỜI

Mẹo chung khi trả lời:
- Câu đầu tiên trả lời thẳng (có / không / con số). Giải thích sau.
- Không biết thì nói "phần này chúng tôi chưa đo", đừng đoán.
- Nếu câu hỏi đụng tới kết quả huấn luyện: trả lời ngắn, rồi nói chi tiết nằm ở bài đồng hành.
- Câu có đánh dấu ⭐ là câu khả năng bị hỏi cao nhất.

## Nhóm A. Về bài toán và đóng góp

**A1 ⭐. Đóng góp chính của bài là gì? Có phải chỉ là ghép hai bộ dữ liệu có sẵn?**
Không chỉ ghép. Có ba phần. Một là nhãn bốn ô dựng bằng quy tắc cho hơn 41 nghìn bước, trong đó ô dấu
hiệu phân biệt là phần mới về nội dung, vì AndroidControl không có. Hai là bộ kiểm định dùng lại được:
đối chứng ghép lệch, kiểm rò rỉ, chín bất biến cấu trúc, và phép đối chiếu với câu của người chú thích.
Ba là phân tích cho thấy trong miền giao diện, cả người lẫn máy đều chuyển từ gọi tên sang chỉ vị trí.
Ghép dữ liệu chỉ là bước chuẩn bị.

**A2 ⭐. Vì sao gọi đây là bài toán sinh biểu thức quy chiếu? Liên quan gì tới ngôn ngữ học tính toán?**
Vì mục tiêu của câu là giúp người nghe nhận ra đúng một đối tượng giữa nhiều đối tượng giống nó. Đó đúng là
định nghĩa của Dale và Reiter năm 1995. Phần ngôn ngữ học nằm ở ô thứ tư: chúng tôi đo được rằng khi
không có tên, cả người chú thích lẫn quy tắc đều chuyển sang mô tả bằng quan hệ, đúng loại mô tả Dale và
Haddock đề xuất năm 1991. Điểm mới là trong miền này, quan hệ không còn là phương án phụ mà thường là
phương án duy nhất.

**A3. Bài toán này khác gì so với các tác tử như SeeClick, OS-Atlas, UGround?**
Các hệ đó nhận câu rồi trả về toạ độ cho máy bấm. Chúng tôi làm chiều ngược lại: nhận ảnh và mục tiêu,
viết câu cho người đọc. Hai chiều bổ sung cho nhau. Thật ra ở bài đồng hành, chúng tôi còn dùng một mô
hình như UGround làm "người đọc" để chấm câu của mình.

**A4. Ứng dụng thực tế là gì?**
Trợ giúp người dùng bị kẹt giữa chừng một tác vụ, hỗ trợ người lớn tuổi, người dùng trình đọc màn hình,
và sinh tự động trang hướng dẫn sử dụng phần mềm. Nhóm dùng trình đọc màn hình là nhóm chịu thiệt nhiều
nhất khi phần tử không có tên, vì trình đọc chỉ đọc được 12,6% phần tử có nhãn.

## Nhóm B. Về cách dựng nhãn

**B1 ⭐. Sao không dùng một mô hình lớn (GPT-4o, Qwen-VL…) để sinh nhãn cho tự nhiên hơn?**
Ba lý do. Một, nhãn quy tắc dựng lại được y hệt và kiểm lại được, mỗi lần sửa quy tắc là dựng lại toàn
bộ trong thời gian ngắn. Hai, mô hình sinh nhãn có thể bịa ra một cái tên nghe hợp lý mà không có trên
màn hình, đúng loại lỗi chúng tôi muốn tránh nhất. Ba, chi phí. Đổi lại, nhãn quy tắc nghèo hơn về ngôn
ngữ, và chúng tôi chưa đo được khoảng cách đó. Đây là điểm yếu chúng tôi thừa nhận.

**B2. Vì sao ưu tiên cây trợ năng trước OCR, khi OCR cho nhiều tên hơn?**
Chúng tôi từng suýt đảo thứ tự, vì đo thấy câu của người khớp với OCR gấp 3,2 lần khớp với cây trợ năng.
Nhưng truy kỹ thì tỉ số đó chỉ dựng trên 72 nhãn, tức 6,7% mẫu thử. Trong 12 ca nghiêng về OCR, 11 ca là
do nhãn trợ năng ở đó là rác. Khi cả hai nguồn đều cho chuỗi dùng được, chỉ còn 1 ca nghiêng về OCR so
với 3 ca nghiêng về cây trợ năng. Vậy ưu thế của OCR là ưu thế của việc lọc rác, nên chúng tôi giữ thứ
tự và thêm bộ lọc. (Slide dự phòng nếu có.)

**B3. Ngưỡng 350 pixel và 25% màn hình lấy từ đâu? Có thử ngưỡng khác không?**
350 px là bán kính tối đa để mỏ neo còn được coi là "bên cạnh". 25% đến từ 25 ca hộp lớn trong mẫu thử,
không ca nào khớp câu của người. Chúng tôi không quét nhiều ngưỡng, và căn cứ của ngưỡng 25% chỉ dựa trên
25 ca, bài có ghi rõ. Bộ lọc này chỉ tác động 2,2% số bước, nên đổi ngưỡng không làm thay đổi nhiều kết quả.

**B4. Độ chính xác của OCR là bao nhiêu?**
Chúng tôi không công bố con số này, vì AndroidControl không có nhãn chuẩn cho chữ trên màn. Cái chúng tôi
báo là OCR chạy lại trên hai máy khác nhau cho kết quả trùng nhau, mật độ chữ đồng đều giữa hai tập (24,2
và 23,6 chuỗi mỗi màn), và hai kiểu lỗi quan sát được.

**B5. Toạ độ thang 0–1.000 có phụ thuộc độ phân giải không? Màn hình khác cỡ thì sao?**
Không. Toạ độ được chia cho chiều rộng và chiều cao ảnh rồi mới đưa về thang 1.000, nên độc lập với độ
phân giải. Ô toạ độ cũng là ô duy nhất giữ nguyên đáp án, nên ô này không thể sai.

**B6. Lấy hộp bao nhỏ nhất thì có trường hợp chọn nhầm phần tử con (ví dụ chữ nằm trong nút) không?**
Có thể. Hộp nhỏ nhất đôi khi là một nhãn chữ con bên trong nút chứ không phải cả cái nút. Về chỗ chạm
thì không sai, vì chạm vào nhãn con cũng kích hoạt nút. Về ô vai trò thì có thể ghi là "text" thay vì
"button". Chúng tôi chưa đo riêng tỉ lệ này.

**B7. Hướng mỏ neo lệch: "to the right of" nhiều gấp 4 lần "to the left of". Có phải lỗi quy tắc?**
Không phải lỗi. Nhãn tả vị trí của phần tử so với chữ neo, mà trên Android chữ mô tả thường đặt bên trái
nút bấm hoặc công tắc. Nên "phần tử nằm bên phải chữ" xuất hiện nhiều hơn. Theo chiều dọc thì hai hướng
gần cân nhau.

**B8. Có thông tin cá nhân lọt vào nhãn không?**
Có thể. Ảnh được ghi khi người thật thao tác nên có thể có email, tên riêng, và OCR sẽ đọc chúng. Chúng tôi
giữ nguyên theo bản gốc vì mọi bộ lọc tự động đều sẽ xoá nhầm chữ hợp lệ trên giao diện. AndroidControl
phát hành theo CC0 và chúng tôi không thu thập màn hình mới. Bài có mục riêng về chuyện này.

## Nhóm C. Về đánh giá chất lượng nhãn

**C1 ⭐. 53,5% có thấp không? Nghĩa là gần một nửa số tên bị sai?**
Không. Phép so là so nguyên văn. Người chú thích hay gọi bằng tên loại, ví dụ "the search bar" cho ô có chữ
"Search here", hoặc "search icon" cho cái kính lúp. Những ca đó tên vẫn đúng nhưng không khớp nguyên văn.
Nên 53,5% là chặn dưới. Ý nghĩa của nó nằm ở chỗ cao hơn đối chứng khó 7,6% khoảng bảy lần.

**C2 ⭐. Sao không cho người chấm tay chất lượng nhãn?**
Chúng tôi có đọc tay mẫu thử 1.074 nhãn để dò lỗi quy tắc và kiểm 737 mỏ neo. Nhưng chưa làm khảo sát
người dùng kiểu "đọc nhãn này, chỉ vào nút trên ảnh". Đó là cách kiểm đúng nhất cho ô dấu hiệu phân biệt và
là hạn chế thứ hai chúng tôi nêu. Lý do là nguồn lực, không phải vì nghĩ nó không cần.

**C3. Con số 75,3% đo bằng gì? Có phải tự chấm bài của mình?**
Đúng là phần này đếm trên chính quy tắc: phân loại bốn khuôn câu do quy tắc tạo ra, nên nó chỉ đếm loại
mệnh đề, chưa xác nhận mệnh đề giúp được người dùng. Bài có nói rõ điều đó. Bằng chứng từ bên ngoài là
phép so ô tên với câu người (53,5%) và tần suất người dùng từ chỉ vị trí (32,5%).

**C4. Mẫu thử 1.074 nhãn có đại diện không?**
Sáu chỉ số chất lượng trên mẫu thử và trên toàn bộ 41.099 nhãn lệch nhau không quá 1,6 điểm phần trăm, dù
mẫu thử nhỏ hơn 38 lần. Ví dụ không có tên: 23,4% trên mẫu thử, 22,0% toàn bộ.

**C5. Kiểm định ghép 48,3% so với 19,6% có đủ chặt không? Một phần nhỏ dòng ghép lệch thì sao?**
Đúng là phép kiểm này chỉ bắt lỗi ghép có hệ thống, chứ không xác nhận từng dòng. Nếu chỉ vài phần trăm
dòng bị lệch ngẫu nhiên thì nó không bắt được, bài có ghi. Chúng tôi chọn cách này vì rẻ, chạy lại được
sau mỗi lần dựng, và nhắm đúng loại lỗi có thể phá hỏng cả bộ dữ liệu mà không ai biết.

**C6. Có lối tắt nào mô hình có thể học không, ví dụ nhãn đúng luôn dài hơn?**
Đã kiểm. Quy tắc "cứ chọn nhãn dài hơn" chỉ đoán đúng 43,2%, thấp hơn mức ngẫu nhiên 50%. Nên lối tắt độ
dài không có.

## Nhóm D. Về dữ liệu và khả năng mở rộng

**D1 ⭐. Có làm được cho tiếng Việt không? Ứng dụng Việt Nam thì sao?**
Về quy trình thì được, vì các bước (cây trợ năng, OCR, quy tắc chọn hộp, mỏ neo) không phụ thuộc ngôn ngữ.
Cần OCR đọc được tiếng Việt và khuôn câu tiếng Việt cho ô thứ tư. Phần đã kiểm là việc đổi khuôn nhãn giữa
tiếng Việt và tiếng Anh chỉ là đổi từ vựng (tổng phép tính huấn luyện lệch 0,03%). Phần chưa làm là chạy
trên giao diện tiếng Việt thật, vì chưa có bộ dữ liệu ghi thao tác người dùng Việt cỡ AndroidControl.

**D2. Có chuyển sang web, iOS, máy tính được không?**
Được nếu dữ liệu có ba thứ: ảnh màn hình, điểm chạm và cây cấu trúc giao diện (DOM ở web, view hierarchy
ở iOS). Chúng tôi chưa thử.

**D3. Bộ dữ liệu có công bố không? Gồm những gì?**
Mỗi dòng là một bản ghi JSON gắn với một bước chạm: bốn ô của nhãn, nguồn của tên, tầng tên, toạ độ, hộp
bao, cờ trùng tên và trùng vai trò, nhãn của phần tử hàng xóm, và khoá (episode_id, step_id) để nối về bước
gốc. Ảnh không đi kèm vì AndroidControl đã phát hành ảnh theo CC0. Về thời điểm phát hành, chúng tôi chưa
chốt ngày nên xin không hứa ở đây.

**D4. Tập kiểm tra có phải tập test chính thức của AndroidControl không?**
Không. Cách chia đến từ bản phát hành có ảnh mà chúng tôi dùng. Kiểm sau này cho thấy phần lớn tác vụ
tập kiểm thuộc split train chính thức của AndroidControl. Điều đó không ảnh hưởng tới bài này vì bài này
dựng nhãn, không chấm mô hình, và giữa hai tập của chúng tôi không có tác vụ trùng. Nhưng ai đem so kết
quả với số báo trên split chính thức thì cần lưu ý.

**D5. 55,6% số bước có phần tử cạnh tranh trong khoảng 80–350 px. Sao lại chọn khoảng đó?**
Mốc dưới 80 px vì dưới khoảng 63 px thì khâu chấm điểm ở bài đồng hành gộp hai phần tử làm một, cộng thêm
biên an toàn. Mốc trên 350 px là bán kính của mỏ neo.

## Nhóm E. Câu hỏi về mô hình (trả lời ngắn, chuyển sang bài đồng hành)

**E1 ⭐. Mô hình huấn luyện trên bộ dữ liệu này cho kết quả thế nào?**
Phần đó nằm ở bài đồng hành. Tóm tắt một câu: chúng tôi tinh chỉnh Qwen2.5-VL-3B và chấm câu sinh ra bằng
một mô hình định vị đọc câu rồi trỏ lên màn hình. Mô hình tinh chỉnh tăng rõ so với mô hình gốc. Tuy vậy,
huấn luyện thêm nhãn bốn ô trước câu chưa cho lợi ích rõ so với chỉ học câu. Chúng tôi coi đó là kết quả
cần báo thật, không giấu.
*(Số nếu bị hỏi tiếp, đã công bố ở bài SOICT 2026: theo tiêu chí hộp phần tử D.3, mô hình gốc 53,6 · chỉ
học câu 65,5 · nhãn rồi câu 63,6 · thêm ORPO 66,5 · câu chuẩn của người 83,8.)*

**E2. Vậy nhãn bốn ô có vô ích không?**
Không hẳn. Trên các câu không lặp lại câu trong tập huấn luyện, bản có tinh chỉnh ưu tiên trên nhãn hơn bản
chỉ học câu khoảng 1,9 điểm, có ý nghĩa thống kê, nhưng đó là phân tích sau khi thấy kết quả. Một quan sát
liên quan tới bài này: khi mô hình gọi sai tên, 76,5% trường hợp phần tử nó tả nằm xa hơn 350 px. Nghĩa là
mô hình hay nhìn sang chỗ khác hẳn chứ không lẫn hai nút cạnh nhau. Chỗ khó thật là phần tử không có chữ
để gọi.

## Nhóm F. Câu hỏi khó / mang tính phê bình

**F1. Quy tắc thủ công như vậy có lỗi thời trong thời đại mô hình lớn không?**
Mô hình lớn vẫn cần dữ liệu có nhãn kiểm chứng được, đặc biệt khi cần biết nhãn có bịa không. Quy tắc ở đây
không thay mô hình, nó tạo ra nguồn giám sát rẻ và kiểm được. Và chính phân tích tầng tên cho thấy chỗ quy
tắc bất lực (tên phải suy từ hình dạng biểu tượng) là chỗ mô hình thị giác cần bổ sung. Hai cách bổ sung
cho nhau.

**F2. Nhãn tiếng Anh thì liên quan gì tới hội thảo ngôn ngữ học tính toán tiếng Việt?**
Bài là về phương pháp dựng ngữ liệu quy chiếu và phân tích chiến lược quy chiếu, những thứ không gắn với
một ngôn ngữ. Ngữ liệu gốc là tiếng Anh nên nhãn theo tiếng Anh cho khớp. Bước tiếp theo tự nhiên là áp
quy trình cho giao diện tiếng Việt, như đã nói ở câu D1.

**F3. Ba lần chữ "hoàn toàn tự động" mà vẫn có người đọc tay. Có mâu thuẫn không?**
Không. "Tự động" là nói khâu dán nhãn: không nhãn nào trong 41.099 nhãn do người viết, sửa hay chọn. Người
chỉ tham gia ở khâu kiểm. Khi thấy sai thì sửa quy tắc và dựng lại toàn bộ.

---

## Slide dự phòng nên có (agent dựng sau slide Cảm ơn)

1. Truy nguyên tỉ số 3,2 lần (cho câu B2): 72 nhãn → bỏ 32 trùng mục tiêu → 40 nhãn: 12 OCR / 3 cây / 25 không bên nào; 11/12 do nhãn trợ năng rác.
2. Bảng sáu chỉ số mẫu thử vs toàn bộ (cho câu C4).
3. Bốn nhãn thật đặt cạnh câu người chú thích (Bảng 2 của bài): Search here/Coffee · Leaf · Q trùng tên · Right arrow.
4. Bảng phân bố dấu hiệu đầy đủ theo tầng (Bảng 3 của bài, đủ bốn cột).
5. Một bản ghi GUIRefCorpus mẫu (cho câu D3).
6. Chuỗi mục tiêu bị cắt: ví dụ "...look for Calvin Kle", 99,4% không có dấu câu cuối, ít nhất 71,3% cắt giữa từ.
