# Phép A — bộ trỏ có nhạy với cách diễn đạt không?

**Đòn phải trả lời.** Bộ trỏ GUI bị báo là **nhạy với cách gọi tên phần tử**, và độ chính xác
đo trên **một câu tốt nhất cho mỗi phần tử** là thổi phồng năng lực thật (Jandial et al.,
Findings EACL 2026). Nếu độ nhạy đó lớn, mọi con số executability chỉ đo được văn phong chú
thích của AndroidControl chứ không đo khả năng gọi tên phần tử.

> ⛔ **CON SỐ 84% ĐÃ BỊ RÚT (18/8), tra tận nguồn.** Abstract nguyên văn: *"Our agent reports
> high success rate (upto 84%) in **generating instructions that fail** the state-of-the-art
> GUI grounding models."* ⇒ đó là **năng suất của một agent đối kháng chuyên chế câu phá mô
> hình**, trên **desktop Windows** — không phải tỉ lệ trượt khi diễn đạt lại, không phải trên
> di động. Mọi chỗ trong file này từng viết "sụp đổ 84%" phải đọc lại theo nghĩa đó.
>
> ⇒ Phép kiểm dưới đây **không còn là phòng thủ trước một tuyên bố sụp đổ**; nó **đo cái chưa
> ai đo**: độ nhạy diễn đạt của bộ trỏ ở miền **di động**, **không đối kháng**. Chính bài kia
> nói benchmark đang lệch về web/mobile và họ vá chỗ desktop — tức trường hợp của ta là chỗ
> họ để ngỏ.

Bản thảo cũ **tự khai không trả lời được** (*"We cannot answer it"*), vì bộ bơm lỗi không
gọi bộ trỏ lần nào — nó đặt sẵn một điểm tổng hợp rồi hỏi cổng chữ. Phép kiểm đúng: lấy
**câu chuẩn của người** (đã biết bộ trỏ giải được, trần 75,7%), viết lại giữ nguyên nghĩa,
rồi cho bộ trỏ chạy lại. Trần tụt bao nhiêu chính là câu trả lời.

Bốn biến thể, mọi biến thể **giữ nguyên tên phần tử** (đổi tên là đổi nghĩa, không còn là
diễn đạt lại). Dựng bằng `harness/make_paraphrase.py`, chấm trên Kaggle bằng UGround, lát
800 bước, đọc bằng `harness/phep_a_ghep_cap.py`.

| | Đổi gì | Bao nhiêu bước đổi được |
|---|---|---|
| `p1_verb` | động từ mở đầu: *Click* → *Tap / Press / Select / Choose* | 90,6% |
| `p2_order` | đưa mệnh đề vị trí lên đầu câu | ~25% (chỉ câu có mệnh đề vị trí) |
| `p3_nopos` | **bỏ hẳn** mệnh đề vị trí, giữ tên phần tử | ~25% |
| `p4_both` | `p1` + `p2` cùng lúc | ~25% |

⚠️ `p3_nopos` **không bảo toàn thông tin** — bỏ vị trí thì câu nghèo đi thật. Nó ở đây để
tách hai nguyên nhân: bộ trỏ nhạy với **cách nói**, hay nhạy với **lượng thông tin**. Phải
đọc riêng, đừng gộp vào "phép kiểm diễn đạt lại".

---

## Kết quả gộp (17/8) — tách được hai nguyên nhân

Đọc bằng `python3 harness/phep_a_ghep_cap.py`. Cột **phần bị đụng** mới là số của bài; cột
toàn lát là số Kaggle in ra, đã bị pha loãng bởi các bước câu giữ y nguyên.

**Bảng chốt — bản v2, đã vá cả hai lỗi bộ dựng câu.** Dựng bằng
`python3 harness/phep_a_hieu_chinh.py` (0 GPU, xem mục cuối).

| Biến thể | Đổi gì | Phần bị đụng | executability | McNemar |
|---|---|---|---|---|
| `p1_verb` | động từ thao tác | 725 bước (90,6%) | 76,8 → **77,0** (+0,1) | b=13 c=14, p=1,000 |
| `p2_order` | trật tự câu | 211 bước (26,4%) | 89,6 → **90,0** (+0,5) | b=0 c=1, p=1,000 |
| `p4_both` | `p1`+`p2` cùng lúc | 203 bước (25,4%) | 90,1 → **91,1** (+1,0) | b=0 c=2, p=0,480 |
| `p3_nopos` | **bỏ** mệnh đề vị trí | 198 bước (24,8%) | 89,4 → **85,9** (−3,5) | b=8 c=1, **p=0,046** |

*Bản v1 của `p3_nopos` cho −4,7 pp (b=11 c=1, p=0,009) trên 211 bước, nhưng 7 bước trong đó
là câu bị lỗi regex; loại tay ra thì được −3,4 pp. Bản v2 loại chúng **bằng mã**, cho −3,5 pp
— khớp phép loại tay, tức việc loại có căn cứ. Dùng số v2 vì nó không phải giải trình.*

### ⭐ Con số gộp — đây là con số đi vào bài

Ba biến thể **bảo toàn nghĩa** (`p1` · `p2` · `p4`) gộp lại:

| | |
|---|---|
| bước được viết lại | **1.139** |
| bước đổi chiều | **30 = 2,6%** (13 trúng→trượt · 17 trượt→trúng) |
| hiệu ròng | **+0,35 pp**, KTC95 **[−0,59 · +1,29]** |
| ⇒ mép dưới KTC | loại được mọi mức tụt lớn hơn **0,6 pp** |
| nếu tụt 84% (mức mà agent đối kháng của họ đạt được trên desktop) | phải có **~956** bước đổi chiều. Thực đo **30** |

**Cách nói không đổi được gì; lượng thông tin thì có.** Đổi động từ trên 90,6% số bước: đứng
yên. Đảo mệnh đề vị trí lên đầu: một bước đổi chiều trong 211. **Làm cả hai cùng lúc — xa
nhất khỏi câu gốc mà vẫn giữ nghĩa — cũng đứng yên, và hai bước đổi chiều đều theo chiều
TỐT LÊN, không có bước nào xấu đi.** Chỉ khi bỏ mệnh đề vị trí, tức bỏ **thông tin**, mới
tụt thật.

⭐ **`p4_both` là con số mạnh nhất trong bốn.** Ghép hai phép viết lại thì thường là chỗ hiệu
ứng cộng dồn lộ ra; ở đây nó không lộ ra gì. `0` bước trúng→trượt trên 203 bước.

Đó chính là phép tách hai nguyên nhân đã đăng ký trước, và nó rơi về phía thuận lợi cho
thước: **bộ trỏ không mong manh trước diễn đạt, nó chỉ cần đủ thông tin.**

### Cơ chế: hỏng theo kiểu tất-cả-hoặc-không

Trên 211 bước bị `p3_nopos` đụng, **trung vị sai số bộ trỏ không nhích một chút nào**
(0,24% → 0,24%) trong khi cái đuôi bung ra:

| | trung vị | p75 | p90 | p95 | trung bình |
|---|---|---|---|---|---|
| câu chuẩn | 0,24 | 0,94 | 6,88 | 27,54 | 4,74 |
| bỏ vị trí | 0,24 | 1,46 | **31,16** | **62,38** | **10,27** |

Bỏ mệnh đề vị trí **không làm bộ trỏ trỏ lệch đi một chút** — nó làm một số ít bước **mất
hẳn**. Xem 11 bước trúng→trượt thì thấy rõ: sai số nhảy từ 0,1–0,6% lên 26–190%, tức nhảy
sang phần khác của màn hình. Khớp với phát hiện *sai số lưỡng cực* đã đo hôm 15/8 (trúng
0,4% · trượt 26,2%): thước này không có vùng xám.

⚠️ **Phần bị đụng là phần DỄ NHẤT của lát.** Trần ở đó 89,6% so với 74,9% toàn lát, sai số
trỏ trung vị 0,24% so với 0,69%. Hợp lý — câu có mệnh đề vị trí là câu đã chỉ sẵn chỗ nhìn.
⇒ **−4,7 pp đo trên một phần tư dễ nhất**; bỏ vị trí ở câu khó có thể đắt hơn, và điều đó
**chưa đo**.

### ⚠️ Một lỗi trong bộ dựng câu, đã vá — nó đóng góp 28% hiệu ứng

7/211 câu `p3_nopos` (3,3%) **không bỏ mệnh đề vị trí mà xoá luôn tên phần tử**, trơ lại
`Tap.` Nguyên nhân: từ *left/right/center* cũng nằm **trong tên phần tử** — `the left arrow
icon`, `the Right Tick icon` — nên `re.search` (khớp trái nhất) bắt đầu ngay ở *"on the left
arrow icon …"* và mệnh đề "vị trí" ngốn cả tên. Ba trong số đó nằm đúng trong 11 bước
trúng→trượt.

Đó là loại lỗi **chạy trơn mà sai bản chất**, và nó rơi vào nhánh duy nhất có hiệu ứng:

| | executability phần bị đụng | McNemar |
|---|---|---|
| gồm cả 7 câu lỗi (211 bước) | −4,7 pp | b=11 c=1, p=0,009 |
| **chỉ câu lành (204 bước)** | **−3,4 pp** | b=8 c=1, p=0,046 |

⇒ **28% hiệu ứng thô là do lỗi của mình**, và con số lành **−3,4 pp** nằm sát MDE đã khoá
trước (~3,7 pp) ⇒ đọc là *"tụt nhỏ, ở mép phân giải của lát này"*, **không** phải *"tụt rõ"*.

**Đã vá** `harness/make_paraphrase.py` bằng hai cổng chặn thay vì siết regex (siết regex đã
thử: chặn hết 7 ca xấu nhưng giết cả ca lành có mệnh đề vị trí ở giữa câu). Cổng A: bỏ mệnh
đề xong không được trơ lại động từ. Cổng B: mệnh đề bị bỏ không được chứa danh từ chỉ phần
tử. Kiểm trên 7 ca xấu + 8 ca lành: **0 lọt, 0 mất**.

Bản vá **phủ rộng hơn mà sạch hơn**: **0 câu suy biến** thay vì 35. Tệp mới:
`runs/paraphrase/preds_para_*_v2.jsonl`. Bốn tệp cũ **giữ nguyên không đè** vì chúng là bản
ghi của lượt đã chấm.

### ⚠️ Lỗi thứ hai: đường lui không `.strip()` — và cách nó bị bắt

Khi biến thể không viết lại được, `make_paraphrase.py` giữ nguyên câu chuẩn. Bản đầu ghi
**nguyên xi**, mà **72/589 câu chuẩn có một dấu cách ở cuối** trong khi
`preds_ceiling_human.jsonl` đã strip sạch (0/6.958). Hậu quả: ở đúng những bước lẽ ra phải
**trùng khít lượt trần**, bộ trỏ nhận một chuỗi lệch một ký tự và trả toạ độ khác ở **6 bước**,
trong đó **1 bước đổi hẳn kết luận** — lệch tới **1.219 px = 113% bề ngang**.

✅ **Các con số của bài KHÔNG bị ảnh hưởng**: bước đó nằm **ngoài** phần được viết lại, nên nó
chỉ đụng con số tổng (0,125 pp), không đụng phép ghép cặp. Nhưng nó phá mất khả năng ghép kết
quả từ tệp thô, và đó mới là cái đắt.

**Cách nó bị bắt là điều đáng ghi nhất.** Script ghép kết quả có một `assert` hỏi *"bộ trỏ có
tất định không"* — các bước cùng câu cùng ảnh phải cho cùng toạ độ. Nó **đỏ ngay lần chạy đầu**:
6/589 lệch. Chẩn đoán đầu của tôi là *"bộ trỏ không tất định"* — **sai**, vì chính bản `assert`
đó so chuỗi bằng `.strip()`, tự tay che mất đúng thứ nó cần thấy. Bỏ `.strip()` ra thì lộ ngay:
chuỗi khác nhau thật, một dấu cách.

⇒ **Phép kiểm dùng chính phép biến đổi mà nó cần phát hiện thì mù.** Nay `tu_kiem()` so chuỗi
nguyên xi, và `make_paraphrase.py` `.strip()` ở cả hai đường.

### Cần chấm lại bao nhiêu: KHÔNG GIÂY GPU NÀO

Bản v2 khác v1 ở hai chỗ, **cả hai đều không sinh ra chuỗi nào chưa từng được chấm**:

| bước của v2 | câu là gì | kết quả lấy từ |
|---|---|---|
| viết lại được | y hệt câu v1 đã chấm (kiểm: `v2 \ v1 = 0`, trùng từng byte) | `score_para_<v>_raw.jsonl` |
| không viết lại được | câu chuẩn **đã strip** | `score_ceiling_human_raw.jsonl` |

### Sáu phép kiểm trước khi tin phép ghép — tất cả SO BYTE, không `.strip()`

Phép ghép này đứng hay đổ tuỳ vào việc chuỗi có **trùng từng byte** hay không, nên không được
kiểm bằng `.strip()`. Cả sáu đã cài thành `assert` trong `phep_a_hieu_chinh.py`, chạy lại lúc
nào cũng kiểm lại:

| # | Kiểm gì | Kết quả |
|---|---|---|
| 1 | câu lượt trần == `gold_instruction.strip()` từng byte | **0/6.958** lệch ở preds · **0/4.463** ở tệp thô |
| 2 | mọi bước v2 **viết lại**: chuỗi == chuỗi v1 đã chấm | **0/1.055** lệch |
| 3 | chuỗi bộ trỏ **thật sự nhận** ở lượt v1 == tệp preds | **0/800** lệch |
| 4 | mọi bước v2 **không viết lại**: chuỗi == chuỗi lượt trần | **0/602** lệch |
| 5 | hai lượt thấy cùng màn: `n_buttons` · `gold_xy` · `wh` | **0** lệch cả ba |
| 6 | **tất định**: cùng chuỗi + cùng ảnh ⇒ cùng toạ độ | **0** lệch trên **1.625** phép so |

⭐ **Phép kiểm 6 mạnh hơn vẻ ngoài.** Lượt trần chấm đủ **4.463** bước, mỗi lượt biến thể chỉ
**800** ⇒ thứ tự và cách gom lô **khác nhau**. Cùng chuỗi mà cùng toạ độ trên 1.625 phép so
(66 + 517 + 517 + 525, bốn lượt độc lập đối chiếu lượt trần) ⇒ loại luôn khả năng kết quả phụ
thuộc **lô hay thứ tự**, không chỉ loại khả năng bộ trỏ ngẫu nhiên.

⇒ **Con số v2 không phải ước lượng, nó là kết quả chính xác.** Mỗi bản ghi trong 800 bước ứng
với một lần gọi bộ trỏ thật, trên đúng chuỗi ấy và đúng ảnh ấy: 198 bước lấy từ lượt v1, 602
bước lấy từ lượt trần.

⚠️ **Điều duy nhất nó KHÔNG cho:** đây không phải một lượt **độc lập**. Nếu lượt v1 có sự cố
nhất thời ở một bước thì bản ghép thừa hưởng. Phép kiểm 6 là bằng chứng trực tiếp chống lại khả
năng đó trên chính dữ liệu này (1.625 phép so, 0 bất đồng), nhưng nó không thay được một lượt
chấm mới nếu sau này cần *tái lập độc lập* — lúc đó vẫn phải trả 1 giờ.

*Cùng một mẹo đã dùng để đo trần mà không cần GPU: **tệp thô là tài sản.** Giữ nó thì đổi luật
chấm hay đổi tập câu vẫn tính lại được, miễn bộ trỏ tất định và chuỗi đưa vào trùng khít.*

---

## Kết quả `p1_verb` (17/8) — không suy chuyển

800 bước ghép cặp, **725 câu (90,6%) thật sự đổi chữ**.

| Thước | Câu chuẩn | Đổi động từ | Lệch |
|---|---|---|---|
| executability | 74,9% | **75,0%** | **+0,1** |
| hit_voronoi | 74,9% | 75,0% | +0,1 |
| hit_disk | 83,0% | 83,5% | +0,5 |
| action_ok | 100,0% | 100,0% | +0,0 |
| sai số bộ trỏ trung vị | 0,69% | 0,70% | +0,01 |

**Con số quyết định không phải +0,1 mà là số bước đổi chiều.** Lệch +0,1 pp trên 800 bước
là *1 bước ròng*, và một bước ròng có thể sinh ra từ ba tình huống khác nhau hẳn: 3 bước
đổi chiều (bộ trỏ gần như bất động), 27 bước 13/14 (có nhiễu nhưng không lệch phía nào),
hay 300 bước tình cờ bù trừ (bộ trỏ rung dữ dội). Con số tổng không phân biệt được.

Đếm từ tệp thô: **trúng→trượt 13 · trượt→trúng 14 · tổng đổi chiều 27 = 3,4%**
(χ²=0,00, p=1,000). Tức là tình huống thứ hai, và biên độ nhiễu nhỏ.

**Lát 800 bước có đại diện:** trần 74,9% · S1 58,8% trên lát này, so với 75,7% · 59,1%
trên đủ 4.462 bước. Chênh dưới 1 điểm ở cả hai nhánh ⇒ đọc kết quả trên lát này được.

### Viết được gì, và cấm viết gì

Viết được: **bộ trỏ bền trước việc đổi động từ thao tác.** Đổi 90,6% số bước mà
executability đứng yên, chỉ 3,4% bước đổi chiều và đổi cân bằng hai phía, sai số trỏ trung
vị không nhích.

⛔ **Cấm viết "bền trước diễn đạt lại"** — `p1_verb` đổi *động từ thao tác*, còn Jandial et
al. đổi *cách mô tả phần tử*. Nhẹ hơn hẳn. Bằng chứng ngay trong bảng: `action_ok` giữ
100% ⇒ phép viết lại này không đụng tới phần bộ trỏ phải giải. Biến thể gần với đòn của họ
nhất là **`p3_nopos`**, và đó là con số đáng chờ nhất trong ba cái còn lại.

⛔ Cấm suy ra bộ trỏ nào cũng vậy — vẫn một bộ trỏ (UGround), một kiểu viết lại, một kho.

---

## Luật đọc — đã chốt TRƯỚC khi có số, giữ nguyên làm bản ghi

Mục này viết xong lúc `p1_verb` vừa ra và ba biến thể còn lại **chưa chấm**. Giữ nguyên
không sửa, để chứng minh cách đọc không phải dựng sau khi thấy kết quả.

### ⚠️ Con số tổng bị PHA LOÃNG 3,8 lần

`p2/p3/p4` chỉ đụng được những câu **có mệnh đề vị trí**, tức khoảng một phần tư lát.
Đếm trên đúng lát 800 đã chấm:

| Biến thể | Câu đổi được | Hệ số pha loãng |
|---|---|---|
| `p1_verb` | 725/800 = 90,6% | 1,1× |
| `p2_order` | 211/800 = 26,4% | **3,8×** |
| `p3_nopos` | 211/800 = 26,4% | **3,8×** |
| `p4_both` | 203/800 = 25,4% | **3,9×** |

⇒ Con số ô 4 in ra tính trên **cả 800 bước**, trong đó ~590 bước là câu chuẩn y nguyên.
Một cú sụt thật trên phần bị đụng hiện ra nhỏ đi gần bốn lần:

| Tổng tụt | Nghĩa là phần bị đụng tụt |
|---|---|
| −1 pp | −3,8 pp |
| −3 pp | −11,4 pp |
| −5 pp | −19 pp |
| −16,6 pp | −63 pp ≈ **đúng quy mô sụp đổ Jandial et al. báo** |

Hai hệ quả, chốt trước:

1. **Đọc số trên phần bị đụng, không đọc số tổng.** `harness/phep_a_ghep_cap.py` in sẵn
   dòng *"chỉ bước câu đổi"* — đó mới là số của bài. Số tổng chỉ để đối chiếu trần.
2. **`p3_nopos` tổng ≥ 70% là đủ loại quy mô sụp đổ 84%** (mức của tìm kiếm đối kháng) cho phép
   viết lại này. Ngưỡng này khoá trước khi thấy số.
3. **Chênh dưới ~4 pp trên phần bị đụng thì không đọc được.** Với 211 bước và mức đổi
   chiều như `p1_verb` (3,7%), sai số chuẩn ghép cặp ~1,3 pp ⇒ MDE ~3,7 pp. Tụt 2 pp trên
   phần bị đụng là nhiễu, không phải phát hiện.

Ba kết cục đã định trước, và cái nào đã xảy ra:

| Thấy gì | Kết luận | ✔ |
|---|---|---|
| cả bốn ≈ 73–76% | bộ trỏ bền trước mọi phép viết lại đã thử | **← đây là kết cục đã xảy ra** |
| `p2_order`/`p4_both` tụt | nhạy với **trật tự câu** | không |
| chỉ `p3_nopos` tụt | cần **thông tin vị trí**, không phải chuyện diễn đạt | **← cũng đúng, và tách được hai nguyên nhân** |

Hai kết cục thứ nhất và thứ ba cùng xảy ra — đó là kết quả tốt nhất trong ba, vì nó vừa loại
được đòn vào thước vừa cho một phát hiện dương về cơ chế.

---

## Chỗ phải sửa trong bài

`main.tex` đoạn *Paraphrase sensitivity* trong Limitations. Bản hiện tại **tự khai không trả
lời được** (*"We cannot answer it"*). Thay bằng số đo, và **giữ nguyên câu thừa nhận phạm
vi**: phép kiểm này đóng một cửa, không đóng cửa Jandial et al. mở ra.

Ba câu số nên vào bài, theo thứ tự mạnh dần:

1. **1.139 bước được viết lại trên ba biến thể bảo toàn nghĩa; executability đổi +0,35 pp,
   KTC95 [−0,59 · +1,29].** Mép dưới loại được mọi mức tụt lớn hơn 0,6 pp.
2. **Chỉ 30/1.139 bước (2,6%) đổi chiều**, 13 xuống và 17 lên. Quy mô 84% mà họ báo cần
   **~956** bước đổi chiều.
3. **Biến thể ghép hai phép (`p4_both`) có 0 bước trúng→trượt trên 203 bước.**

Và một câu giới hạn bắt buộc kèm theo: phép viết lại này **giữ nguyên tên phần tử**, nên nó
kiểm *cách nói* chứ không kiểm *cách mô tả phần tử* — đúng thứ Jandial et al. nhắm. Bằng
chứng để không ai đọc quá: `action_ok` giữ **100%** ở cả bốn biến thể.

⛔ Cấm suy ra bộ trỏ nào cũng vậy — vẫn một bộ trỏ (UGround), một kiểu viết lại, một kho.
