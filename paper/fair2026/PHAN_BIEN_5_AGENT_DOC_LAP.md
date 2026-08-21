# Năm phản biện độc lập — kết quả và phần tôi đã tự kiểm chứng (16/8/2026)

Khác với `PHAN_BIEN_5_GIAM_KHAO.md` (tôi tự đóng vai, nên thiên vị vì cùng người viết bài),
lượt này là **năm agent riêng**, mỗi agent chỉ được đọc `main.tex` + `runs/` + `harness/`,
bị cấm đọc README, report/, và hồ sơ tự chấm. Bốn trong năm đã tự chấm lại số từ dữ liệu thô.

| Phản biện | Soundness | Excitement | Phiếu |
|---|---|---|---|
| Đo lường / meta-evaluation | 3,0 | 3,0 | sát mép, nhận nếu sửa lớn |
| GUI agent | **2,5** | **2,5** | **TỪ CHỐI**, khuyến khích nộp lại |
| Thống kê | 3,5 | 3,0 | sát mép, nghiêng nhận |
| Đánh giá NLG | 3,0 | 3,0 | sát mép |
| Trưởng tiểu ban | 3,5 | — | sát mép, nghiêng nhận |

**Điểm chung của cả năm:** không ai bắt được một con số bịa. Bốn người tự tính lại tổng cộng
hơn tám mươi đại lượng (McNemar cả ba cặp kể cả hiệu chỉnh Yates, 1.824/251/1.573, 935, 741,
395/565/131, cả 14.966.784 tham số LoRA tính tay) và **gần như tất cả khớp đến chữ số cuối**.
Vấn đề của bài không nằm ở tính toán. Nó nằm ở **khoảng cách giữa những gì bài mô tả và những
gì mã thực thi**, và ở **việc chọn con số nào đưa lên tiêu đề**.

---

## A. Đã tự kiểm chứng — SAI THẬT, phải sửa

### A1. ⛔ Bộ trỏ dùng làm thước **đã được huấn luyện trên AndroidControl**

Nặng nhất trong toàn bộ lượt rà. Tra Bảng 1 của chính bài UGround (arXiv 2410.05243):

| Nguồn | Nhãn | #Elements | Nền tảng |
|---|---|---|---|
| **AndroidControl** | **Human** | **47K** | Android |
| Widget Caption | Human | 41K | Android |
| UIBert · AITZ | Human · GPT+Human | 16K · 8K | Android |

`score_run.py:79-81` chú thích khẳng định *"đã xác minh recipe huấn luyện của nó không chứa
AndroidControl"* — **khẳng định đó sai**. `CLAUDE.md` ghi "UGround SẠCH" cũng sai, phải rút.

Hệ quả phải khai, theo thứ tự nặng dần:
1. Bài áp tiêu chuẩn "phải sạch AndroidControl" cho **bộ trỏ tương lai** mà không áp cho bộ
   trỏ **đang dùng** — bất đối xứng, phản biện sẽ chỉ ra ngay.
2. Trần 75,7% đo bằng cách nạp **nguyên văn câu chuẩn AndroidControl** vào một bộ trỏ từng
   học cặp (câu AndroidControl → toạ độ). Đây là kịch bản nhiễm xấu nhất dựng được.
3. Nó là **lời giải thích thay thế thứ bảy** cho khoảng cách +11,5 pp, và sáu đòn ở §VII-B
   không phủ được: bộ trỏ quen văn phong người chú thích thì giải mã văn phong đó tốt hơn,
   mà S1 lại được đo là kéo câu về đúng văn phong ấy (24,5% lặp nguyên từ nội dung).

**Chưa biết:** 47K của UGround lấy từ split nào. Nếu chỉ là train split thì các màn của tập
kiểm chưa bị thấy, và tình thế nhẹ hẳn — nhưng phần thiên vị văn phong vẫn còn.

### A2. ⛔ Bộ trỏ **cùng họ mô hình** với hệ được chấm

`score_run.py:86` nạp UGround-V1-2B bằng `Qwen2VLForConditionalGeneration`; hệ bị chấm là
Qwen2.5-VL-3B. Cùng dòng Qwen-VL. Bài viết *"G belongs to a different model family from the
system under evaluation"* (§IV-A) — sai. Tệ hơn, §Limitations viết các ứng viên khác bị loại
vì *"most of the remainder share the backbone family of the generator under test"*, hàm ý bộ
trỏ đang dùng thì không. Hai câu đá nhau.

### A3. ⛔ `history` trong câu nhắc là **câu chuẩn do người viết**, không phải "ba thao tác gần nhất"

Kiểm trên `test.jsonl`: `history[-1]` trùng **nguyên văn** `gold_instruction` của bước trước ở
**5.318/5.318 trường hợp (100%)**. Nghĩa là lúc chấm, mô hình đọc được tới ba câu tham chiếu
cùng episode, cùng người viết, cùng văn phong mà thước đang thưởng.

Giống nhau ở mọi nhánh nên **không ảnh hưởng S2−S1**, nhưng ảnh hưởng mọi số tuyệt đối và
phép so Base-vs-S1, và mô tả trong §V-A hiện **sai sự thật**.

### A4. ⛔ Công thức luật chấm in trong bài không phải luật đang chạy — hai chỗ

| Bài viết (§IV-A) | Mã chạy |
|---|---|
| $\lVert p-g\rVert \le \tau W$ (đĩa Euclid) | `abs(dx) <= 0.14*W and abs(dy) <= 0.14*H` — **hộp chữ nhật**, dọc rộng gấp **2,2 lần** ngang |
| $\arg\min_{e\in E}\lVert c(e)-p\rVert = e^{*}$ | hạt của đích là **chính điểm chạm `g`**, không phải tâm $c(e^*)$; và **mọi tâm trong 63 px quanh `g` bị xoá trước** khi so |

Một phản biện chấm lại theo đúng công thức in trong bài: trần rơi từ 74,5 xuống **54,8** trên
lát 799 bước. Thứ tự ba nhánh không đổi ở cả năm cách chấm — đó là tin tốt và nên khoe — nhưng
con số trụ thì đổi. Với bài có đóng góp chính là *dụng cụ*, đây là lỗi ở đúng chỗ không được sai.

### A5. ⛔ "(i) và (ii) đúng theo cấu tạo" — sai

§IV-D nói với nhánh trần thì hai điều kiện đầu đúng theo cấu tạo. Đo được: `toggle_ok = 0` ở
**3 bước**, vì `POSITION_WORDS` không loại giới từ **"on"** trong khi `click on …` là cách mở
đầu phổ biến nhất của kho ngữ liệu:

```
Click on Off in the middle of the screen.
Click on the menu icon on the top left corner off the screen.
Click on the North Korea's Kim shows off banned article
```

Lệch theo nhánh: 11 câu Base chứa cả "on" lẫn "off" so với 3 câu S1 — luật phạt nhánh đang
thắng ít hơn. Độ lớn nhỏ (~0,2 pp) nhưng chiều thì có hệ thống.

### A6. ⛔ Bộ bơm lỗi **không gọi bộ trỏ một lần nào**

`exec_injection_v3.py` không nạp UGround (0 lần khớp); điểm được mô phỏng bằng
`real_ok = g + 0.03·1080·0.7`. Nên hàng "False reject, real paraphrase 0,0%" đo **cổng chữ**,
không đo *"bộ trỏ đọc câu viết khác đi có còn tới đúng ô không"*.

Nhưng Limitations lại dùng đúng hàng đó để đáp lại Jandial et al., vốn nói **bộ trỏ** trượt tới
84% khi đổi cách diễn đạt. Đòn nhắm vào $G$, phản đòn không đụng $G$ — **phòng vệ trước mối đe
doạ nguy hiểm nhất của bài về mặt cấu trúc không có hiệu lực.**

### A7. ⛔ "Wild cluster bootstrap" — mã là bootstrap gom cụm theo cặp, lấy phân vị

`cluster_bootstrap()` bốc lại nguyên cụm có hoàn lại rồi lấy phân vị. Không có trọng số
Rademacher, không có phần dư, không studentise. Luận điểm của Cameron–Gelbach–Miller chính là
bootstrap-theo-cặp **phủ thiếu** và wild bootstrap-t là cách chữa — bài đang trích họ cho đúng
thứ họ khuyên bỏ. Với G=1.091 hệ quả nhỏ, nhưng là sai mô tả phương pháp.

### A8. ⛔ Câu "73,6% có tên rõ (8.581 cây + 23.480 OCR)" gây hiểu nhầm

8.581 + 23.480 = 32.061, không ra 73,6% của bất kỳ mẫu số nào. **Số không sai, câu sai**:
32.061 là tổng nhãn có nguồn tên, gồm cả nhóm "chỉ ký hiệu" 4,4%. 73,6 + 4,4 = 78,0% × 41.099
= 32.057, lệch 4 do làm tròn.

---

## B. Đã tự kiểm chứng — lập luận phải sửa

### B1. "Trần" 75,7% bị chính ba nhánh của bài vượt qua

Hợp ba nhánh trên cùng 4.462 bước: **3.527 bước = 79,05%**, cao hơn "trần" 3,3 điểm. Và **148**
bước mà câu người viết trượt lại được S1 hoặc Base giải. Vậy tập 1.083 bước **không cố định**,
và câu *"an instrument limit and not a model deficiency"* bị chính bảng McNemar của bài bác.

Kéo theo hai đại lượng: "lấp 41% khoảng cách" (lấy mẫu số 79,05% thì còn **36,6%**) và
"room 741 bước / 16,6 pp".

### B2. MDE ghép cặp 2,7–4,5 pp không dẫn xuất ở đâu — và số thật là **2,2 pp**

Ba phản biện độc lập cùng bắt. Công thức $2{,}8\hat\sigma/\sqrt{G_{\text{eff}}}$ ngầm giả định
ICC = 1; DEFF đo được chỉ ≈ 1,5. Tôi chạy bootstrap cụm trên hiệu ghép cặp:

| | SE | MDE (80%, 5%) |
|---|---|---|
| S1−Base, **có cụm** | 0,785 pp | **2,20 pp** |
| Human−S1, có cụm | 0,759 pp | 2,12 pp |
| S1−Base, không cụm | 0,717 pp | 2,01 pp |
| ⇒ hệ số nở do cụm | | **1,10×** (không phải 1,5–2×) |

Hệ quả không phải học thuật: luật đã đăng ký gọi khoảng **4–9 pp là "không kết luận được"**.
Với MDE thật 2,2 pp, một hiệu ứng +3 pp sẽ có khoảng tin cậy loại trừ 0 với p<0,001 **mà vẫn bị
luật riêng của bài vứt đi**. Phải ghi mục sửa đổi vào `report/106` **trước** khi chấm S2.

### B3. Cổng thao tác gần như rỗng trên quần thể chấm

`canon_action` **mặc định trả `"tap"`** khi không thấy động từ nào trong bảng. Vì toàn bộ dân
số chấm là bước chạm, mọi câu không có động từ đều qua cổng (i) miễn phí. Con số 94,4% vì thế
đo "mô hình có lỡ nói scroll/type không", không đo "gọi đúng thao tác" — làm yếu chính câu chốt
*"the failures are failures of description"*.

Cùng lỗi: `ACTION_MAP` quét trái sang phải và `go`, `navigate` (→ tap) đứng trước `back`, nên
`go back` / `navigate back` / `press the back button` đều quy về **tap**. Lớp `back` mà §IV-A
liệt kê là **không thể đạt tới** bằng ba cách nói tự nhiên nhất của nó — và đó là hàm dùng cho
phép kiểm không-gây-hại đã đăng ký trước.

### B4. "8 trên 10" gồm ít nhất bốn tiêu chí không thể rớt về mặt xây dựng

- Hàng 2 (`fp_action_gate`): nhiễu sinh ra bằng cách thay Click/Tap/Select/Press → Tap, mà
  `ACTION_MAP` định nghĩa cả bốn là cùng lớp. 0,0% là **hằng đẳng thức**.
- Hàng 3 (`fp_flip_rule`): chỉ 3/4.463 câu chuẩn có thể kích hoạt. Ngưỡng 5% không có đường chạm.
- Hàng 8, 10: kiểm `canon_action` khác lớp và `direction_match` False — tất định.

Còn **bốn hàng thật sự có nội dung** (hàng xóm gần/xa/rất xa, phủ định), **rớt 2**. Thêm nữa
hàng 7 (n=15) được bài gọi là "quá ít để kết luận" nhưng vẫn nằm trong mẫu số của "8/10".

### B5. Thiên lệch bộ trỏ **không** triệt tiêu đều giữa các nhánh

Bài viết *"a residual bias in G is common to all of them and largely cancels"*. Đo tỉ lệ bộ trỏ
bỏ trục ngang (trả x đúng giữa màn trong khi gold lệch tâm): **S1 18,4% · người 15,8% · Base
19,1%** — khác nhau theo nhánh và tương quan với chất lượng nhánh.

### B6. Chống "chơi thước": hai proxy tôi thêm sáng nay đo **tần suất**, không đo **dốc thưởng**

| | S1 | Người | Base |
|---|---|---|---|
| chênh exec giữa câu **có** và **không** từ chỉ vị trí | **+15,5 pp** | +14,0 | +3,8 |
| 20 câu lặp nhiều nhất chiếm | **10,4%** | 6,5% | 3,3% |

Dốc có thật, và S1 khuôn mẫu hơn câu người. Nhưng mức khai thác dốc vị trí thì gần bằng người
(+15,5 so với +14,0), nên kết luận đúng phải là "dốc tồn tại, mô hình chưa trèo xa", không phải
"không có dấu hiệu".

Một điểm phản biện nêu thì kiểm ra **nhẹ hơn** họ nói: câu chỉ định theo thứ tự ("click the
first option") — S1 dùng 6,9%, **người dùng 6,1%** và còn được chấp nhận trên màn đông phần tử
nhiều hơn S1 (106 so với 90). Đó là tật của kho ngữ liệu, không phải mô hình học cách chơi thước.

### B7. "Lấp 41% khoảng cách" thổi lên bởi các bước tái tạo nguyên văn

Chỉ tính 3.243 bước mô hình **tự viết**: Base 44,4 → S1 52,3 → trần 75,1, tức lấp **26%**
chứ không phải 41%.

---

## C. Việc phải làm, xếp theo mức chặn

**Chặn nộp bài** (không sửa thì bài nói sai sự thật):
1. A1 — khai UGround có AndroidControl trong dữ liệu huấn luyện; sửa chú thích trong
   `score_run.py`; rút câu "UGround SẠCH" trong `CLAUDE.md`.
2. A2 — bỏ "different model family", nêu nền Qwen2-VL của UGround-V1-2B.
3. A3 — sửa mô tả câu nhắc: `history` là câu chuẩn của người, không phải nhật ký thao tác.
4. A4 — viết lại điều kiện (iii) và điều kiện đĩa cho khớp mã.
5. A5 — bỏ "hold by construction", nêu 3 ca rớt.
6. A6 — rút phản đòn Jandial hoặc chạy bộ trỏ trên câu chuẩn đã viết lại.
7. A7 — đổi tên phép bootstrap.
8. A8 — sửa câu 73,6%.

**Nên làm trước khi nộp:**
9. B2 — thay MDE ước bằng MDE đo (2,2 pp) và **sửa dải "không kết luận được" trước khi chấm S2**.
10. B1 — đổi cách gọi trần, báo hợp ba nhánh 79,05%, tính lại 41%.
11. B5, B6, B7 — sửa ba câu cho khớp số đo.
12. B4 — tách bảng bơm lỗi thành *hằng đẳng thức* / *có nội dung*, bỏ "8 of 10" khỏi tóm tắt.
13. B3 — khai giá trị mặc định của `canon_action`; sửa thứ tự quét cho `back`.

**Đáng làm nhưng cần tài nguyên:**
14. Chấm người 100 câu (0 đồng) — cả năm phản biện đều nêu.
15. Bộ trỏ thứ hai, thật sự sạch AndroidControl, lát ≥500 bước (~1,2 giờ GPU).
16. Bảng độ nhạy theo công thức chấm (đĩa L2 / hộp / Voronoi-mã / Voronoi-như-viết / nearest-box)
    — biến điểm yếu A4 thành điểm mạnh, vì thứ tự ba nhánh sống sót qua cả năm luật.

---

## D. Điều cả năm phản biện đều ghi nhận

Không ai tìm thấy số bịa. Mức tự khai (rút con số 70,0 và nói rõ vì sao, in cả hai tiêu chí rớt
kèm cỡ mẫu, in `n=15`, khai nhánh đã đăng ký mà chưa chạy, khai lỗi kiểm im lặng của bản trước)
được cả năm người nhắc tới như thứ hiếm gặp. Một người viết: *"mức trung thực này khiến tôi tin
các con số — chính vì thế các sai lệch giữa văn bản và mã cần được xử triệt để, chúng là loại
lỗi duy nhất mà thái độ trung thực không tự bù được."*

---

# VÒNG 2 (16/8, sau khi vá) — mức chấp nhận đã đổi

Cùng năm góc nhìn, cùng quy tắc độc lập, chạy trên bản đã sửa.

| Phản biện | Vòng 1 (S/E) | Vòng 2 (S/E) | Phiếu |
|---|---|---|---|
| Đo lường | 3,0 / 3,0 | **3,5 / 3,5** | sát mép → **nghiêng nhận** |
| GUI agent | 2,5 / 2,5 | **3,5** / 2,5 | **từ chối → sát mép** |
| Thống kê | 3,5 / 3,0 | **4,0 / 3,0** | sát mép → **weak accept** |
| Đánh giá NLG | 3,0 / 3,0 | 3,0 / 3,0 | sát mép → sát mép, nhận có điều kiện |
| Trưởng tiểu ban | 3,5 | **4,0** | sát mép → **NHẬN** |
| **Trung bình soundness** | **2,9** | **3,6** | không còn phiếu từ chối |

## Lỗi vòng 2 bắt được — đều đã tự kiểm và đã vá

| Lỗi | Bằng chứng | Đã xử |
|---|---|---|
| **`b`/`c` ĐẢO** ở phép kiểm học thuộc | theo định nghĩa của chính bài, `b=547` đọc thành *S1 thua 8,4 điểm* | sửa thành `b=264, c=547` |
| **BLEU 96,1 vs "100 by construction"** | 96,06% = (4463−176)/4463, đúng bằng số câu chuẩn dưới 4 token | khai lý do, bỏ khẳng định "gấp bốn lần" |
| **Hai quần thể "câu tự viết"** | 3.243 (không tái lập được) vs 3.367 | thống nhất 3.367, lấp **28%** |
| **Vùng mù báo thiếu** | 35,2% (381 bước) bị luật ô bác, bài chỉ ghi 19,2% | báo cả hai + giá theo nhánh 10,1/13,0/15,2% |
| **SE độc lập so lệch chuẩn** | 1,05 là SE **không** gom cụm; cùng điều kiện phải là **1,26** | sửa |
| **`strict_back` không được truyền** | bài nói phép kiểm không-gây-hại dùng bản vá, `noharm()` thì không | vá `score_run.py` |
| **Mục tiêu bị cắt cụt** | 99,0% goal trong mirror kết thúc giữa chừng (`...look for Calvin Kle`) | khai ở mục III + nêu trần không chịu thiệt này |
| **Nhiễm bẩn ưu ái trần nhất** | câu chuẩn *là* văn phong bộ trỏ đã học | thêm vào mục IV-A |
| **Dòng 1 bảng bơm lỗi cũng không thể rớt** | điểm bơm cách gold 23 px, trong bán kính gộp 63 px | khai, còn 3 dòng có nội dung |
| **Suy diễn trên n=78** | bài vừa nói "quá nhỏ" vừa dùng nó bác memorisation | bỏ câu đó |

## Hai chỗ phản biện sai, đã kiểm và KHÔNG sửa theo

- **"Paraphrase chỉ trượt 2,9% nên bác được Jandial et al."** — con số đó lấy ở dải
  Jaccard 0,8–1,0, tức câu gần trùng chữ. Đo dải rộng: chồng nhiều 6,6%, chồng ít
  48,5%, **không chung từ nội dung 88,7%**. Và không dải nào trả lời được, vì với câu
  mô hình ta không biết "khác chữ" là diễn đạt khác hợp lệ hay tả nhầm nút. Giữ nguyên
  cách khai "chưa trả lời được".
- **"68,8% bước người trượt là kết oan"** — dùng *hộp bất kỳ* chứa điểm chạm nên một
  hàng danh sách cũng tính. Siết về hộp nhỏ nhất + trong dung sai: **19,2%**.

## Còn nợ (không sửa được bằng cách viết)

1. **Chấm người 100 câu** — cả 5 phiếu vòng 2 đều nêu; hai phiếu nói thẳng rằng lời
   hứa lần thứ ba không còn cộng điểm.
2. **Bộ trỏ sạch AndroidControl, lát ≥500 bước** — đòn duy nhất không phiếu nào coi là
   đã đóng.
3. **Hạt giống 202** — chưa có sàn nhiễu giữa hai lượt train thì 11,5 pp chưa có mốc so.
4. Chạy bộ trỏ trên câu chuẩn đã viết lại (một lượt chấm) để trả lời Jandial et al.
