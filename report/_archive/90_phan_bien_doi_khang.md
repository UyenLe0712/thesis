# 90 — Phản biện đối kháng toàn bộ luận văn (19/7/2026)

> **Đây là file xấu.** Nó liệt kê chỗ hỏng, không liệt kê chỗ tốt. Đọc xong đừng hoảng: phần lớn lỗi nằm ở **bằng chứng rằng thước đo đã được kiểm**, không nằm ở xương sống thiết kế. Nhưng có một lỗ đủ nặng để phải sửa trước khi tiêu tiền GPU.
>
> **Bản nguyên văn đầy đủ** (27 đòn + 12 đòn bị bác + phán quyết từng trục, lời của chính các giám khảo, kèm số dòng code và output chạy lại): `report/90b_phu_luc_nguyen_van.md`. File bạn đang đọc là bản viết lại cho dễ hiểu.

## Cách bản phản biện này được làm ra

7 giám khảo độc lập, mỗi người một trục, chạy song song. Năm người dùng Opus 4.8 cho các trục kiểm được bằng số (thước đo, thống kê, dữ liệu, bốn phép thử, đối chiếu văn-với-số); hai người dùng Fable cho hai trục thuần phán đoán (tính mới, đóng góp có đủ ngưỡng không) — đổi họ model ở đúng chỗ mà phán đoán dễ giống nhau.

Ba luật đặt ra để bản này không thành màn tự khen:

1. **Bịt mắt.** Cấm đọc `report/88` và `CLAUDE.md` trước. Bắt đọc code và file kết quả thô trước, tự kết luận, xong mới mở prose ra đối chiếu. Lý do: hai file đó là bản tự tóm tắt do trợ lý AI viết, giọng rất tự tin, đọc trước là bị mớm khung.
2. **Phải gắn bằng chứng.** Mỗi đòn phải kèm tên file + số dòng, hoặc con số trích từ JSON, hoặc output tự chạy lại. Đòn không gắn được thì phải tự khai là suy đoán.
3. **Vòng bác bỏ.** Mọi đòn xếp mức nặng trở lên bị giao cho một giám khảo khác với nhiệm vụ *cố hết sức bác bỏ nó*. 39 đòn nặng vào vòng này, **12 chết, 27 sống**. Nên những gì còn lại dưới đây đã qua một lần đối kháng, không phải ý kiến một chiều.

Tổng cộng 64 phát hiện. Các giám khảo có chạy lại code thật (venv local + ollama, không gọi API tốn tiền) — nhiều con số dưới đây là họ tự đo được, không phải đọc lại từ report.

**Giới hạn phải khai:** cả 7 giám khảo lẫn người tổng hợp (tôi) đều là model Anthropic, cùng gu huấn luyện, nên có thể cùng mù một chỗ. Bản này **không thay thế** vòng kiểm của thầy hướng dẫn.

---

## Phần 1 — Lỗ nặng nhất: thước đo chưa hề được kiểm

Đây là chuyện lớn nhất trong cả file, và cũng là lỗi của tôi — tôi viết `harness/metric_v1_validate.py` và `report/84`.

### 1.1 Cổng kiểm thước không phải phép đo, mà là phép tính đã biết trước kết quả

Ý tưởng ban đầu đúng: muốn biết thước có tốt không thì bơm lỗi giả vào rồi xem thước có bắt được không. Vấn đề nằm ở **cách sinh ra hai loại ca thử**.

Ca "paraphrase" (viết khác nhưng cùng nghĩa, thước phải chấp nhận) được dựng ở dòng 117:

```python
tgt = target_of(g[i])          # lấy đích của gold
g[i] = f"{v} on the {tgt}"     # lắp lại thành câu mới
```

`"on"` và `"the"` đều nằm trong danh sách từ bị bỏ qua, `v` luôn nằm trong bảng động từ. Nên sau khi thước chuẩn hoá lại, **tập từ của "paraphrase" trùng khít với gold**. Jaccard = 1.0 không phải vì thước giỏi, mà vì phép thử tự chép lại đáp án.

Ca "sai đích" (thước phải bác) ở dòng 97 thì ngược lại: code **bắt buộc** đích thay thế phải có tập từ **giao rỗng** với gold. Jaccard = 0 cũng theo định nghĩa.

Hai đống điểm được xây để tách rời trước khi thước kịp chạy. `AUC = 1.000` chỉ là `P(1.0 > 0.0)` — phương sai bằng không. Không có dữ liệu nào trên đời làm nó tụt xuống dưới 1.

Hệ quả về mặt quy trình: cổng "AUC < 0.80 thì DỪNG, không train" ghi trong `report/85` **không có đường nào kích hoạt được**. Nó không phải cổng. Hai dòng khác trong cùng bảng cổng (`detection = 1.000`, `false-positive paraphrase = 0.000`) sập theo cùng một cơ chế — tức **3 trong 5 dòng của bảng cổng là hằng đẳng thức**, không phải kết quả đo.

Một giám khảo đếm lại trên dữ liệu thật: trong số các bước thật sự bị sửa, 177/177 ca paraphrase dính trần 1.0; 178/185 ca sai-đích đúng bằng 0, bảy ca còn lại cao nhất 0.25.

### 1.2 Đem paraphrase thật vào thì thước rớt, và rớt nặng

Đây mới là phần đáng sợ. Một giám khảo tự dựng 10 cặp viết-khác-cùng-nghĩa **thật** — cùng một nút, gọi bằng hai cách người ta thật sự hay gọi:

| Gold | Cách gọi khác | Thước chấm |
|---|---|---|
| `filter option` | `funnel icon` | trượt |
| `settings icon` | `gear icon` | trượt |
| `compose button` | `pencil icon` | trượt |
| `search bar` | `magnifying glass` | trượt |

**Kết oan 10/10. AUC = 0.35 — tệ hơn tung đồng xu.**

Backstop bge-m3 ngưỡng 0.85 không cứu được ca nào, vì điểm giống nhau chồng lấn đúng như K1 đã đo: `gmail tab` ↔ `calendar tab` (đây là ca **bịa**) được 0.717, trong khi `search bar` ↔ `magnifying glass` (ca **thật**) chỉ được 0.490. Ca bịa ăn điểm cao hơn ca thật. Không có ngưỡng nào tách được — đúng bức tường mà K1 đã đâm vào hồi 18/7.

Nghĩa là câu tôi viết vào CLAUDE.md — *"tách (action, target) giải được đúng chỗ K1 chết, đo bằng số không assume"* — **sai**. Việc tách action/target chỉ chứng minh thước phân biệt được hai thái cực, mà khớp-chuỗi thuần cũng làm được chuyện đó.

### 1.3 Hệ quả chí mạng: con số headline có thể chỉ đo độ khớp giọng văn

Đây là chỗ đòn này chạm vào tim luận văn, chứ không chỉ là lỗi kỹ thuật.

Trục ĐÚNG so Student với Teacher trên cùng lát AndroidControl. Student sẽ được train **trên chính gold AC**, nên nó học đúng phương ngữ của annotator AC (`Click on X`). Teacher chạy zero-shot thì diễn đạt theo cách khác (`Tap the funnel icon`). Với một thước kết oan cách-gọi-khác một cách có hệ thống, Student thắng **không phải vì hướng dẫn đúng hơn, mà vì nói giống gold hơn**.

Không phải suy luận suông. Một giám khảo lấy 91 cặp output teacher đã có sẵn trong cache pilot, tái tạo đúng điểm 0.286 của `report/86`, rồi **chỉ đổi các lựa chọn bề mặt của thước**, không đổi một chữ nội dung nào:

| Cấu hình thước | Điểm teacher |
|---|---|
| nguyên trạng (Jaccard + action chặt) | 0.286 |
| gộp tap/open/navigate thành một lớp | 0.330 |
| thay Jaccard bằng containment | 0.473 |
| cả hai + bỏ từ chỉ vị trí | **0.604** |

Điểm nhảy hơn gấp đôi chỉ vì đổi cách chuẩn hoá. Một đại lượng nhạy với lựa chọn kỹ thuật đến mức đó thì con số headline **không diễn giải được**, trừ khi tách được phần "khớp giọng" ra khỏi phần "chọn đúng nút".

Cách tách, cũng do giám khảo đề xuất và tôi thấy hợp lý: thêm nhánh **Teacher-STYLE-MATCHED** — nhét vài câu gold AC vào prompt cho teacher nói cùng phương ngữ. Khi đó:
- `Student − Teacher-STYLE` = phần "chọn đúng nút" (cái ta muốn đo)
- `Teacher-STYLE − Teacher-BASE` = phần "khớp giọng thuần" (cái nhiễu)

Rẻ, và biến một con số không diễn giải được thành hai con số diễn giải được.

### 1.4 Thước sai cả hai chiều ở vùng giữa — vùng mà bơm-lỗi chưa từng chạm

Vì bơm-lỗi chỉ sinh hai cực (trùng hết / không trùng gì), vùng giữa — nơi thước thật sự phải phân xử — chưa bao giờ được thử. Giám khảo tự dựng ca rồi chạy qua `step_match`:

**Nhận đúng trong khi sai:**

| Model nói | Gold | Điểm | Kết quả |
|---|---|---|---|
| `Turn off notifications` | `Turn on notifications` | 0.667 | **KHỚP** |
| `Scroll up` | `Scroll down` | 0.500 | **KHỚP** |
| `Set the timer to 30 minutes` | `...10 minutes` | 0.600 | **KHỚP** |
| `Click on Tools & Hardware` | `Click on Tools` | 0.500 | **KHỚP** |

Hướng dẫn **ngược nghĩa** vẫn được tính là đúng. Đây là chiều nguy hiểm hơn vì nó thổi phồng điểm.

**Bác trong khi đúng:** `Tap Log in` vs `Tap the Sign in button` → 0.000. `Tap the Trash icon` vs `Click on Delete` → 0.000. `Tap the More options icon` vs `Click on the three-dot menu` → 0.000.

Cơ chế: đích dài thì Jaccard ≥ 0.5 dung thứ một từ đảo nghĩa; đích ngắn thì một từ đồng nghĩa là trượt tuyệt đối.

Người phản-bác cắt bớt được hai điểm (ca "quantity 5 vs 2" chỉ ảnh hưởng 0.5% bước thật; ca `Tap Settings in Chrome` thước bác đúng), nhưng thêm vào một điểm nặng hơn: **hai chiều lỗi này không triệt tiêu trong hiệu-số cặp** — cả hai đều đẩy Δ về phía giả thuyết.

Ngoài ra: một ca trong bảng trên (`Click on Tools` vs `Click on Tools & Hardware`) là **văn bản có thật** trong `ac_test_200ep.json`, không phải bịa ra.

### 1.5 Đích rỗng khớp nhau hoàn hảo

Lỗi nhỏ nhưng buồn cười và nằm đúng chỗ đau. Hàm lọc từ bỏ hết từ trong danh sách bỏ qua và bảng động từ — nhưng nhiều **nhãn nút phổ biến nhất của GUI lại nằm trong hai bảng đó**: `Next`, `Back`, `Open`, `Enter`, `Go`, `Select`, `Return`.

Kết quả: 3.2% bước gold rút gọn về đích **rỗng**. Và khi cả hai bên đều rỗng, code rơi xuống backstop, gọi embedding trên hai chuỗi khoảng trắng giống hệt nhau → cos = 1.0 → **khớp hoàn hảo**.

Đo được: `step_match('Tap Next', 'Tap Back')` = **True, điểm 1.000**. `step_match('Click on the + icon', 'Click on the right arrow')` = **True, 1.000**.

Đây chính xác là lớp nút icon-only mà K2 đếm 20/40 ca và OCR nói không cứu được.

### 1.6 Một bước gold được "phủ" bởi một bước gold khác

Hàm `coverage()` là bài toán phủ-tập **không ràng buộc một-đối-một**: một bước model có thể được ghi công cho nhiều bước gold cùng lúc. Đo trên dữ liệu thật: **12.4% bước gold (127/1027) được phủ bởi một bước gold khác** trong cùng episode, văn bản khác hẳn. Ví dụ `Click on Tools` được tính là phủ cho `Click on Hand Tools`.

Người phản-bác chỉnh lại một chỗ: mô tả "thổi phồng coverage của mọi nhánh" là sai cơ chế — trần bị thổi chung sẽ **nén** hiệu-số, tức bảo thủ. Nhưng anh ta không cứu được thiết kế, vì rò rỉ này **không phải hằng số**: nó tỉ lệ với độ chung chung của văn bản, mà Teacher (dài dòng) và Student (ngắn gọn giống gold) khác nhau đúng ở chiều đó. Nên đây là thiên lệch vi sai, dấu chưa biết. Cộng với MDE đã sát ngưỡng, teo hiệu-số đủ để hỏng cả kết cục PASS lẫn kết cục NULL.

Sửa: đổi sang gióng một-đối-một tối ưu (Hungarian trên ma trận điểm), khử trùng lặp gold trước khi chấm. Khoảng mười dòng.

### 1.7 Thước đang thưởng cho câu cộc lốc và phạt hướng dẫn hữu ích hơn

Đề tài nói sinh hướng dẫn **cho người đọc**. Thước lại chấm bằng độ trùng từ với câu chú thích của crowdworker. Đo trực tiếp, gold = `Click on filter option`:

| Model sinh ra | Điểm | |
|---|---|---|
| `Tap the Filter button` (chép cộc lốc) | 1.000 | khớp |
| `Tap the funnel-shaped Filter icon` (tả hình dạng) | 0.333 | **trượt** |
| `Tap Filter to narrow the list, then choose a category` (có ngữ cảnh) | 0.250 | **trượt** |

Càng thêm thông tin hữu ích cho người, mẫu số Jaccard càng phình, càng bị trừ điểm. Trớ trêu: `report/76` kết luận điểm yếu của model chính là **không** chỉ vị trí và hình dạng — tức trục ĐÚNG đang đẩy model đi ngược hướng chất lượng mà luận văn muốn.

Người phản-bác bác được ba điểm phụ và cần ghi nhận:
- **Vị trí thì KHÔNG bị phạt** — regex có xoá cụm vị trí ở đuôi, và danh sách bỏ qua chứa top/bottom/left/right/corner/screen. Đo lại: `"at the top right of the screen"` vẫn 1.000. Chỉ **hình dạng** (`funnel-shaped`) mới bị trừ. Nửa phần mỉa mai của đòn sụp.
- "Thước không đo thứ tự" là đọc nhầm — thứ tự đo bằng order-τ tách riêng, đã đăng ký trước.
- "Không phạt bước thừa" cũng vậy — coverage là recall, phần chống nhồi bước nằm ở F1.

Nhưng lõi sống: ba con số 1.000/0.333/0.250 tái lập chính xác, và điều này chạy **cùng chiều** với giả thuyết.

Và thêm một sự thật khó chịu: nghiên cứu nhỏ đối chiếu thước với người chấm đang bị **hoãn**, trong khi PASS/NULL của luận văn đã được đăng ký trước neo lên chính thước đó. Hiện **không có một bằng chứng nào** nối thước với phán xét của người.

---

## Phần 2 — Vấn đề về tính chính trực của bản đăng ký trước

Đây là nhóm lỗi khác về bản chất: không phải làm sai, mà là **báo cáo mạnh hơn cái mình có**.

### 2.1 "Vòng 2 — stress-test ca khó" không tồn tại trong repo

`report/84` báo ba con số cho vòng 2: điểm đích-sai-khó trung bình 0.350, AUC = 1.000 trên ca khó, bge cứu nhầm 3/60 = 5%. `report/85` đóng băng dòng `1.000 (cả ca khó) ✓` làm kết quả cổng chính thức.

**Không có script nào trong repo sinh ra ba con số đó.** `metric_v1_results.json` chỉ chứa đúng một khoá AUC (của vòng 1). Grep `0.350`, grep `artworks`, grep nhánh "ca khó" trong file python đều không ra gì.

Mà vòng 2 chính là phần được dùng để bác lại nghi ngờ "vòng 1 quá dễ". Mắt xích chịu lực nhất lại là mắt xích không tái lập được.

Một bản đăng ký trước trích số không có artifact thì mất hiệu lực làm dấu thời gian. Hoặc commit code + JSON của vòng 2, hoặc gỡ con số ra và ghi rõ là chưa chạy.

### 2.2 Caveat rụng dần qua ba tầng tài liệu

`report/84` mục "Hoài nghi còn lại" tự khai **rất sòng phẳng**, đúng hai điều mà cả bản phản biện này xoay quanh:

> *"tôi giữ nguyên từ-lõi (chỉ đảo trật tự + thêm article) → **Jaccard=1 tất yếu**"*
>
> *"Perturbation do chính tôi dựng → **có phần circular**"*

Nhưng ngay trong cùng file đó, phần kết luận lại viết *"giả định lớn nhất đã kiểm bằng số, KHÔNG assume"* và *"tin tốt cứng nhất từ trước tới nay"* — mâu thuẫn nội bộ trong một file.

Sang `report/88` và `CLAUDE.md` thì chỉ còn `✅ QUA (AUC=1.0)`, và commit `b5a6b29` ghi `metric-gate PASSED`.

Người phản-bác đính chính hai chi tiết mà tôi phải ghi nhận cho công bằng:
- `report/88` **không** mất sạch caveat — dòng 140 vẫn ghi "nếu mô hình thật dùng từ đồng nghĩa cho loại nút có thể kết oan", và dòng 213 vẫn giữ việc construct-validity. Đòn cherry-pick đúng hai dòng ngay trước caveat.
- `report/85` hedge **mạnh hơn** mô tả: có ghi "kết quả synthetic", có ghi "phải chạy lại trên config cuối".

Nhưng phần lõi sống: lời tự khai **không chảy được vào chỗ nó phải chặn**. Bảng cổng vẫn ghi ✓, commit vẫn ghi PASSED. Nguyên tắc rút ra: **caveat của một con số phải nằm ngay trong ô của nó**, không được đẩy xuống mục hoài nghi cuối file.

### 2.3 Script tự in cờ đỏ, report ghi ✓

Script tự cài luật: nếu coverage tụt dưới 0.15 thì in cảnh báo `⚠ KHÔNG tụt đủ`. Chạy lại thì nó **in ra cờ đó** cho hai dòng:

```
action_error  coverage=0.851  Δ=+0.149  ⚠ KHÔNG tụt đủ
missing       coverage=0.850  Δ=+0.150  ⚠ KHÔNG tụt đủ
```

`report/84` ghi cả hai dòng là ✓ và kết luận QUA CỔNG.

Về bản chất Δ ≈ 0.15 là hợp lý (sửa một bước trên ~6-7 bước thì coverage tụt ~1/6), nên cái đặt sai là **ngưỡng**, không phải thước. Nhưng đúng quy trình thì không được im lặng bỏ qua cờ đỏ của chính mình. Phải hoặc sửa ngưỡng và khai là đã sửa kèm lý do, hoặc báo là trượt.

### 2.4 Kế hoạch "chỉnh backstop khi có output model" là chỉnh thước trên dữ liệu đánh giá

Con số 0.85 tự nó **sạch** — đặt tiên nghiệm, có lý lẽ, không dò theo kết quả. Vấn đề là kế hoạch: `report/84` và `report/85` đều ghi sẽ *"hiệu chỉnh backstop khi có output model thật"*. Đó là tinh chỉnh tham số của thước sau khi nhìn dữ liệu đánh giá, trong một thiết kế đã đóng băng ngưỡng — đúng thứ mà đăng ký trước sinh ra để ngăn. Làm vậy thì mọi CI và mọi phán quyết PASS/NULL mất hiệu lực danh nghĩa.

Sửa: hiệu chỉnh trên một tập **dev tách riêng** (app không nằm trong test split, hoặc output teacher trên train-split), khoá lại, rồi mới chạy test. Ghi rõ hiệu chỉnh trên dev nào, ngày nào, commit nào.

---

## Phần 3 — Thống kê: G đếm nhầm file, MDE sai theo

### 3.1 `G ≈ 150-250 app` lấy từ sai quần thể

Con số đó đếm từ `ac_test_200ep.json` — **test set chung**, không phải quần thể đánh giá. Quần thể thật là app_unseen split.

Đếm trên đúng file (`ac_app_unseen_count.json`):

| | report/85 ghi | Đếm lại trên đúng split |
|---|---|---|
| tỉ lệ gán được app | ~72% | **41%** (102/250 ep) |
| số app distinct | ~114 trong 200 ep | **42** trong 102 ep gán được |
| phân bố | "phần lớn singleton" | **tập trung mạnh** — Pinterest 14, Arts&Culture 8, CNN 6, Guardian 6 |

app_unseen hoá ra là một cụm app nghệ thuật/tin tức khá hẹp, không phải rừng app đa dạng.

Tính lại MDE: ngoại suy 631 ep → G gán được cỡ 60-90 → **MDE ≈ 12.5-14.4 pp**, không phải 8-9. (Một giám khảo dùng ước lượng Chao1 ra G ≈ 72 → MDE 13.1 pp — cùng vùng.) Vẫn dưới ngưỡng 15-20 nhưng **sát hơn nhiều**, không còn dư địa thoải mái như report/86 kể.

Muốn giữ G lớn thì phải đếm 59% ep không gán được thành singleton — mà làm vậy là phá thẳng giả định độc lập giữa cụm.

### 3.2 Biến cụm bị vỡ: một app bị tách thành nhiều cụm, và có cụm không phải app

Hàm gán app dùng regex bắt `"... app"` trong câu goal. Nhìn thẳng vào output của nó trong `mde_pilot_results.json`:

- Cùng một app bị tách đôi: `The Washington Post` và `Washington post`; `Arts & Culture` và `Art & Culture`; `NYTimes` và `Newyork times`; `CNN` và `Knoxville on the CNN`.
- Cụm rác không phải tên app: `Inspire in this`, `On the Pinerest`, `Video Audio`, `Artier`. Trong file đếm còn có nguyên câu `Expert Paper art & Professional Origami Designing steps`.

Hai hệ quả, đều xấu và ngược chiều nhau: **G bị thổi phồng** (làm MDE trông đẹp hơn thực), và quan sát của cùng một app thật bị rải vào nhiều cụm nên bootstrap tưởng chúng độc lập → **khoảng tin cậy hẹp giả, p-value lạc quan giả**. Đây đúng là thứ mà lựa chọn "cụm theo app" được dựng ra để tránh.

Gộp thử bí danh: G tụt 26 → 22, SD nhích 0.2561 → 0.2632.

Sửa: ưu tiên tuyệt đối `open_app.app_name`, chuẩn hoá tên (lowercase, bỏ mạo từ, bỏ dấu, gộp bí danh), rà tay danh sách cuối (~70 tên, làm được trong một buổi). Ep không gán được thì loại khỏi phân tích cụm chứ đừng để regex đoán bừa.

### 3.3 Ngưỡng 15-20 pp vốn là cơ chế chữa cháy của trục khác

Truy được nguồn: đây là luật *"nếu MDE quá tệ thì đổi split 18/12 sang 15/15"* viết trong `report/56` cho trục MobileViews G=12 cố định. Ở trục AndroidControl, biện pháp 15/15 vô nghĩa, nên ngưỡng mất hết ý nghĩa vận hành mà vẫn đang được dùng như tiêu chí hợp lệ khoa học.

Điểm cần nói rõ để thủ: ngưỡng **không** bị chọn sau khi biết MDE. `report/56` commit ngày 12/7, pilot chạy 19/7. Chỗ này sạch, cứ nói thẳng.

Nhưng phải (a) khai rằng ngưỡng vốn thuộc trục khác, (b) đặt một ngưỡng có căn cứ riêng cho trục ĐÚNG — hiệu bao nhiêu điểm phần trăm thì mới đáng gọi là đóng góp model?

### 3.4 Trục TRUNG THỰC G=12: ô MDE đang để trống, và lực thật rất yếu

`report/85` để nguyên `[MDE trục trung thực MobileViews = ___ pp]`.

Một giám khảo mô phỏng đầy đủ phép sign-flip chính xác (liệt kê cả 4096 tổ hợp dấu, α=0.05 hai phía, 400 lần lặp mỗi ô):

| Hiệu ứng thật | Lực với SD=0.362 | Lực với SD=0.20 (lạc quan) |
|---|---|---|
| 5 pp | 7% | — |
| 10 pp | 12% | 36% |
| 15 pp | 25% | 66% |
| 20 pp | 43% | — |
| 30 pp | 73% | — |

Áp chính công thức của tôi ở G=12: `3.077 × 0.362 / √12` = **32.2 pp**. Tức trục trung thực **rớt ngưỡng 15-20 gấp đôi**, và không report nào nhắc đến chuyện đó.

Nghĩa là một kết quả null ở trục trung thực sẽ **không đọc được gì** — không phân biệt được "không có hiệu ứng" với "có hiệu ứng 15 pp mà không đủ lực bắt".

Sửa: điền ô đó trước khi commit. Nếu ra ~30 pp thì hoặc tăng số app MobileViews (kích hoạt đúng cơ chế 15/15 mà report/56 đã dự trù), hoặc hạ trục trung thực xuống mức mô tả và khai thẳng là không đủ lực kiểm định — chứ đừng chạy rồi báo "null".

---

## Phần 4 — Dữ liệu: gold AC là gì thật sự

### 4.1 Gold step_instruction là nhãn thao tác ngắn, không phải văn hướng dẫn cho người

Một giám khảo đọc thẳng 1042 bước trong `ac_test_200ep.json` và đo:

- trung vị **6 từ**; 48.9% câu ≤ 5 từ; 10.3% câu ≤ 3 từ
- 60.4% bắt đầu bằng click/tap/press/select
- chỉ 749 câu distinct trên 1042
- **167/842 cặp bước liền nhau trùng y hệt** (episode "The Times Of India" có `Click on the first result podcast` hai lần liên tiếp, action thứ hai là `wait`)
- 3 bước rỗng
- câu hỏng: `Click on the top at the bottom right corner` (episode 10265, gõ nhầm chữ "cart")

`report/81` mô tả chất lượng gold là "tốt"; việc A.3 "đếm rộng chất lượng gold" không có file kết quả nào.

Train trên đây thì ra một bộ **sinh nhãn thao tác từng bước bằng ngôn ngữ tự nhiên**. Khác các bài GUI-agent chủ yếu ở chỗ output là câu chữ thay vì lời gọi hàm — không phải ở chỗ "viết cho người đọc". Khoảng cách giữa cái này và pitch "hướng dẫn nhiều bước cho người" phần lớn là **đổi nhãn đối tượng đọc**.

Phải chọn một trong hai, không có đường giữa:
- **(a)** khai thẳng target là step-instruction của AC, hạ claim xuống "sinh mô tả thao tác bằng ngôn ngữ tự nhiên"; hoặc
- **(b)** giữ claim "cho người" nhưng phải có tầng viết lại **và** một vòng đánh giá bằng người trên output thật — chính là nghiên cứu nhỏ đang bị hoãn.

Và dù chọn gì cũng phải lọc dữ liệu train: bỏ bước rỗng, gộp cặp trùng liên tiếp (~20%), nếu không model học luôn cả tật lặp.

### 4.2 Ghi chú: "vừa học vừa chấm cùng loại" — không bị bác thành công

Đòn "train trên gold AC rồi chấm trên gold AC là tầm thường" **không** bị bác, nhưng cũng không đứng ở dạng thô. Cái sống là biến thể tinh vi hơn ở mục 1.3: vấn đề không phải chấm cùng dataset (split app-unseen là hợp lệ), mà là **thước thưởng cho việc bắt chước từ vựng annotator**. Nhánh Teacher-STYLE-MATCHED là cách xử.

---

## Phần 5 — Tính mới: một quả mìn ở CHI 2026

### 5.1 GuideMe đã chiếm tác vụ ở mức khái niệm

**GuideMe** — Fang, Zhang, Ni, Hui, Wang — Proceedings of CHI 2026, DOI `10.1145/3772318.3791448`. Hệ VLM cho người cao tuổi: người dùng hỏi trong app, hệ chụp màn hình, lấy thông tin UI element, VLM phân tích, sinh **hướng dẫn từng bước** kèm highlight tại chỗ để người làm theo.

Ở **mức tác vụ**, "sinh hướng dẫn nhiều bước cho người từ ảnh + câu hỏi" đã được công bố tại venue HCI hàng đầu. `grep -i guideme report/` = **0 hit**. `report/82` từng tự khai "chưa quét CHI/UIST" — lỗ tự khai đó chứa đúng quả mìn.

Dòng CLAUDE.md *"model **đầu tiên** sinh hướng dẫn nhiều bước cho người đọc từ 1 ảnh + câu hỏi"* giờ **sai ở mức tác vụ**.

Người phản-bác hạ mức từ "nặng" xuống "vừa" với năm lý do kiểm được, và tôi thấy hợp lý:

1. Trục CHI **không phải điểm mù**: repo đã có `report/papers/askease_chi2026.md` — AskEase, **cùng proceedings CHI'26** (DOI prefix `3772318` giống hệt) — và đã tự dán nhãn "rủi ro novelty cao nhất, phải phân định". Lập luận phân định đã viết sẵn, áp nguyên xi cho GuideMe được.
2. `report/82` đã **tự cấm** claim này từ 19/7: ❌ *"Quy trình sinh hướng dẫn GUI cho người là mới hoàn toàn"*.
3. **Bản thảo nộp không chứa overclaim**: `grep -in 'first|đầu tiên' report/57` = 0 hit. Overclaim chỉ nằm ở nhật ký nội bộ CLAUDE.md.
4. Không chạm trục tính mới phòng thủ được nào: GuideMe không train model, không dataset, không metric, không đụng AndroidControl. Đóng góp của họ là **tương tác** (bong bóng nổi, highlight tại chỗ).
5. Câu định vị thật của `report/57` neo vào "no source document and no gold tutorial" — GuideMe không bác được vì nó **có** nguồn ngữ cảnh ngoài và **không** có metric faithfulness.

Việc phải làm: lấy full-text xác định là full paper hay extended abstract; sửa dòng CLAUDE.md xuống "model nhỏ mở **đầu tiên được huấn luyện** cho tác vụ này"; thêm GuideMe + Synapse (IMWUT 2022) + ExplorAR + DigitalCoach vào related work; dùng GuideMe làm **trụ biện minh nhu cầu** (HCI đã cần tác vụ này) thay vì coi là scoop.

### 5.2 Còn một mảng chưa quét

`Widget Captioning` (EMNLP 2020) và `Screen2Words` (UIST 2021) là dòng sinh-văn-cho-người trên GUI, chưa có trong related work. Dòng data-synthesis của GUI-agent (OS-Genesis, Aguvis reverse-synthesis) cũng đã sinh instruction từ trajectory — cần phân định trước khi viết câu "chưa ai dùng AC step_instruction làm target".

---

## Phần 6 — Bốn phép thử: cần chỉnh cách kể, không cần chạy lại

### 6.1 K2 — đúng là chỉ một app, nhưng kết luận vẫn đứng

Đòn: toàn bộ 80 file cache là của **một app duy nhất** (`ls harness/dg1_cache/runs | sed 's/_s[0-9]*.*//' | uniq -c` → `80 app1`). 40 ca soi tay quy về **18 chuỗi element distinct**, riêng `+` chiếm 15 ca, 13/40 dòng là bản sao y hệt. Cỡ mẫu hiệu dụng gần 1 app / vài widget, không phải 127 bước độc lập. `report/74` chỉ ghi "một-hai miền app" — nói nhẹ hơn sự thật.

**Đòn bị bác**, bằng một lập luận tôi thấy thuyết phục: con số "~¼ bịa" mà K2 lật đổ **cũng đến từ đúng bộ app1 đó** (CLAUDE.md có ghi "CI còn chạm 0, n nhỏ, 1 app cũ"). Bác một claim bằng chính mẫu đã sinh ra claim đó thì không cần tính đại diện ngoài mẫu. Thêm nữa, kết luận hành động được của K2 — VH bỏ nhãn icon nên matcher kết oan nút thật — được xác nhận **độc lập ở quy mô 30 app** (VH coverage 0.624 trên 127 màn, OCR chạy 3964 nút trên 30 app, cùng ra sàn ~20% icon vô nhãn).

Phần còn sống, mức vừa: đổi cách viết. "80 màn" → "80 màn **của 1 app**"; "40 ca" → "40 quan sát trên **~18 widget distinct**". Tỉ lệ "20/40 là icon" đã lan vào CLAUDE.md nên phải sửa ở đó.

### 6.2 K1 — mẫu nhỏ hơn tài liệu kể, và ca đại diện chọn không khéo

`report/73` mở đầu "chạy trên 127 màn thật". Chạy lại `build_pairs()`: tập thử thật chỉ từ **30 màn / 7 app**; hai lớp quyết định mỗi lớp chỉ từ 17 màn.

Nặng hơn là thành phần: `Everything` chiếm 11/40 ca paraphrase, `None` chiếm 11/40 ca bịa-gần-nghĩa. Riêng cặp neo `all` đóng góp hơn một phần tư cả hai lớp. Mà `None` vs `All` là quan hệ **trái nghĩa** — embedding nổi tiếng đặt trái nghĩa rất gần nhau, nên chọn nó làm đại diện cho "bịa gần nghĩa" là tự xếp bài để phép thử rớt.

Và κ = 0.38 tính trên tỉ lệ lớp do tôi tự đặt bằng caps (70/60). κ phụ thuộc mạnh vào tỉ lệ nền, mà tỉ lệ nền thật ngoài đời — theo chính K2 — là ~2%. Nên κ = 0.38 không nói được gì về chất lượng matcher lúc triển khai.

Sửa: đổi "127 màn" thành "30 màn / 7 app" ở mọi chỗ; giới hạn mỗi chuỗi tối đa ~3 lần; tách riêng cặp trái nghĩa; bỏ κ khỏi headline, báo AUC (bất biến với tỉ lệ nền) làm số chính.

### 6.3 OCR — đếm nhầm kiểu substring, thổi số lên ~7 lần

`report/75` khẳng định OCR đọc được `+` (23 lần), `X/x/×` (97), `<`/`>` (46), và dùng đúng đó để chốt hướng "gắn từ điển ký hiệu thẳng lên glyph OCR trả về, không cần model dò icon".

Đếm lại từ `ocr_cache.json`, glyph **đứng riêng** ở conf ≥ 0.5:

| Glyph | report/75 | Đếm lại (standalone) |
|---|---|---|
| `+` | 23 | **11** |
| `X`/`x`/`×` | 97 | **13** |
| `<`/`>` | 46 | **0** |
| `✓` | — | **0** |

Đếm kiểu substring-anywhere thì ra đúng 23 và 97 → xác nhận lỗi: mọi chuỗi chứa chữ x (`Expenses`, `Next`, `Box`) bị tính là đọc được icon X.

Hệ quả thiết kế: OCR trả về **zero mũi tên và zero dấu tích** — đúng hai loại icon mà K2 nói là nguồn kết oan chính. Tầng 4 của trọng tài đa tín hiệu **không có gì để gắn từ điển vào** cho chính các ca nó sinh ra để cứu.

Sửa: thay bảng glyph bằng số standalone; bỏ mệnh đề "không cần model dò icon"; ghi thẳng vào giới hạn rằng sàn kết oan icon hình thuần không xoá được bằng OCR.

---

## Phần 7 — Khả thi

Kiểm kê thẳng repo, ngày 19/7:

- **Không có** script train, không có config LLaMA-Factory nào
- AC train-split (nguồn tín hiệu chính, ~13k episode + ảnh) **chưa tải** — local chỉ có 200 ep test
- Matcher đa tầng cho trục TRUNG THỰC **chưa build** — mới có script phân tích
- **Chưa gặp thầy** sau ba lần đổi khung; mọi mốc "HỎI THẦY" còn treo
- `KE_HOACH_2_BAI_BAO` bản 3 (12/7): abstract FAIR vẫn nguyên văn *"training only on data whose fabricated button references have been filtered"* — tức vẫn đang bán **đóng góp đã chết từ 18/7**

Chuỗi việc còn lại trước FAIR: vá thước → build data hai nguồn → pilot xung đột phong cách → train + ablation → eval hai trục + thống kê → viết bài tiếng Anh. Trong **27 ngày**, một người, Colab Pro chưa mua.

Phán quyết: **FAIR 15/8 gần chắc trượt.** Đường lui có và đã tự khai ("bỏ FAIR giữ VCL") — đó là điểm cộng thật.

Nhưng VCL cũng không an toàn như tưởng: chấm trung thực output **tiếng Việt** đối chiếu VH **tiếng Anh** là đúng ca cross-lingual mà K1 đo được so-chuỗi kết oan **97.5%** và embedding không cứu. Cách chữa "bảo model giữ tên nút tiếng Anh" chưa có số nào chống lưng.

Đề nghị: quyết bỏ hay giữ FAIR **ngay tuần này** thay vì 1/8. Mỗi ngày giữ FAIR là một ngày mất của VCL và của luận văn.

---

## Phần 8 — Những đòn ĐÃ BỊ BÁC (để khỏi lo oan)

12 đòn chết trong vòng đối kháng. Ghi lại vì nếu ai đó nêu lại thì đã có sẵn câu trả lời:

| Đòn | Vì sao chết |
|---|---|
| K2 dựa trên 1 app nên tiền đề "teacher bịa ~0-2%" vô hiệu | Con số "~¼" bị lật cũng từ đúng mẫu đó; kiểm-lại-trong-cùng-mẫu là hợp lệ |
| Cả 4 phép thử chạy trên MobileViews nên không chuyển giao sang AC | Kết luận hành-động-được (VH thiếu nhãn icon) được xác nhận độc lập ở quy mô 30 app |
| SD = 0.256 gần như toàn nhiễu nhị thức | Phân rã phương sai không ủng hộ mức đó |
| SD của hiệu-số chưa hề được đo, √2×SD là giả định | Nhãn "bảo thủ" đứng được |
| Độ phủ nhãn app là 41% chứ không phải 72%, phần thiếu bị drop âm thầm | Trùng với đòn G/MDE đã sống ở mục 3.1, không tính hai lần |
| Pilot MDE đo tác vụ dễ hơn tác vụ sẽ eval | Không chứng minh được "dễ hơn" |
| Thước headline mới xây 1/3 (F1, order-τ chưa có code) | Đã đăng ký trước là sẽ xây, chưa đến hạn |
| "Không τ nào tách được" sai với bge-m3 | Đúng một phần, nhưng suy rộng của đòn quá tay |
| K2 không có code phân loại, bảng 6 dòng chỉ tồn tại trong văn xuôi | Trùng đòn K2 đã xử |
| Mâu thuẫn G=150-250 vs 42 app | Trùng mục 3.1 |
| Script tự in cảnh báo rớt mà report ghi ✓ | Trùng mục 2.3 (bản khác của cùng đòn đã sống) |
| G lấy từ sai population | Trùng mục 3.1 |

---

## Phần 9 — Phán quyết tổng

**Xương sống thiết kế không sập.** Tách (action, target); đo trên AC app-unseen in-distribution; so cặp Student với Teacher; hai trục đúng + trung thực. Không đòn nào giết được mấy cái đó, kể cả các giám khảo cố tình tìm cách giết.

**Cái sập là bằng chứng rằng thước đã được kiểm.** Thước chưa được kiểm. Nó vừa bị kiểm lần đầu ở đây, bằng paraphrase thật, và **rớt** (AUC 0.35, kết oan 10/10). Cổng metric-gate đã commit là cổng rỗng.

**Rủi ro lớn nhất không phải "thước hơi nhiễu" mà là "con số headline không diễn giải được":** Δ(Student − Teacher) hiện có thể chỉ đo độ khớp giọng văn annotator. Nếu không tách được phần đó ra, thì dù kết quả có dương đẹp cũng không kết luận được gì, và một giám khảo tinh ý sẽ hỏi đúng câu đó.

**Tin đỡ hơn:** mọi thứ phải sửa đều **free và sửa được trước khi train**. Không có phát hiện nào đòi đổi dataset, đổi model, hay bỏ hướng. Và nhiều lỗ đã được chính tài liệu tự khai — vấn đề là lời tự khai không chảy được vào chỗ nó phải chặn.

---

# KẾ HOẠCH — làm tuần tự, đừng nhảy cóc

Nguyên tắc xuyên suốt: **mọi việc dưới đây đều free. Không tiêu một đồng GPU hay API nào cho tới hết Giai đoạn B.**

## Giai đoạn A — Dừng chảy máu (làm trước, trong 1 ngày)

Không sửa gì về khoa học, chỉ ngừng để tài liệu nói mạnh hơn số.

**A1. Rút các câu overclaim khỏi CLAUDE.md và report/88.** Cụ thể ba câu:
- *"tách (action,target) GIẢI được đúng chỗ K1 chết, đo bằng số không assume"* → gỡ
- *"metric-gate PASSED"* → đổi thành "cổng chưa hợp lệ, đang dựng lại"
- *"model ĐẦU TIÊN sinh hướng dẫn nhiều bước cho người đọc"* → "model nhỏ mở đầu tiên **được huấn luyện** cho tác vụ này"

**A2. Ra bản vá có dấu thời gian cho report/85**, đừng sửa lặng. Ghi rõ: ba dòng cổng (AUC, detection, FP-paraphrase) không hợp lệ vì nhánh paraphrase tái dùng `target_of()`; vòng 2 "ca khó" chưa có artifact nên gỡ số; ngày và lý do vá.

**A3. Sửa số trong report/73/74/75:** "127 màn" → "30 màn / 7 app" (K1); "80 màn" → "80 màn của 1 app, ~18 widget distinct" (K2); bảng glyph OCR → số standalone, bỏ mệnh đề "không cần model dò icon".

> Vì sao làm trước: nếu gặp thầy hoặc mở lại file sau vài tuần mà mấy câu này còn nguyên, bạn sẽ tự tin sai và ra quyết định sai.

## Giai đoạn B — Dựng lại thước cho tử tế (2-4 ngày, quyết định sống chết)

**B1. Viết lại bộ bơm-lỗi cho độc lập với thước.**
- Nhánh paraphrase **không được gọi** `target_of()`. Lấy 100-150 bước gold, viết lại bằng tay hoặc bằng model khác họ, đổi đúng thứ model thật sẽ đổi: `tab`→`section`, `three lines`→`menu icon`, `filter option`→`funnel icon`.
- Nhánh sai-đích **bỏ ràng buộc giao rỗng**, lấy nút cùng màn có chồng từ (đúng ca `artworks tab` vs `energy tab`).
- Thêm bốn họ ca hiểm hiện chưa có: đảo nghĩa (on↔off, up↔down), đổi số lượng, đích cha↔con cùng cây UI, từ đồng nghĩa nhãn nút.
- Chạy, báo AUC **kèm CI bootstrap theo episode**. Chuẩn bị tinh thần nó rớt — đó là thông tin, không phải thất bại.

**B2. Vá các lỗi cơ học đã xác định** (làm cùng B1, chốt **trước** khi nhìn kết quả để khỏi thành tuning trên test):
- `coverage()` → gióng một-đối-một tối ưu (Hungarian), khử trùng lặp gold
- đích rỗng → chặn cứng, không cho match, đếm riêng thành nhóm "không phân xử được"
- tách bảng động từ khỏi bảng lọc từ — `Next`/`Back`/`Open` chỉ bị loại khi ở vị trí động từ
- bỏ dấu câu trong chuẩn hoá; cân nhắc containment thay Jaccard
- luật cứng: khác từ phủ định hoặc khác số lượng ⇒ không khớp, bất kể điểm

**B3. Chạy vòng 2 thật và commit cả code lẫn JSON.** Nếu không chạy thì gỡ hẳn ba con số khỏi report/84 và 85.

**Cổng thật ở đây:** nếu sau khi vá mà AUC trên paraphrase thật vẫn dưới ~0.80, **dừng, đừng train**. Lúc đó phải bàn lại: hoặc thêm từ điển chuẩn hoá nút/icon, hoặc đổi sang thước khác, hoặc chuyển trọng tâm luận văn sang chương đo lường. Đây là cổng có thể rớt thật — khác cổng cũ.

## Giai đoạn C — Nối thước với người (2-3 ngày, làm trước khi train chứ không phải sau)

**C1. Nghiên cứu nhỏ construct-validity.** Bạn đã có sẵn 91 cặp output teacher trong `harness/dg1_cache/mde_pilot/gen.json` — **không tốn xu nào**. Hai người chấm câu hỏi đơn giản: *"hướng dẫn này có giúp bạn bấm đúng nút không?"*. Rồi báo:
- tương quan giữa điểm người và điểm (action, target)
- κ giữa hai người chấm

**Nếu tương quan thấp thì mọi thứ phía sau đều vô nghĩa.** Biết điều đó bây giờ rẻ hơn biết sau khi đã đốt GPU. Đây là việc tôi nghĩ đáng làm nhất trong cả danh sách.

**C2. Quyết định về claim "cho người".** Sau C1 sẽ có cơ sở chọn: khai thẳng target là step-instruction của AC và hạ claim, hay giữ claim và thêm tầng viết lại. Đừng chọn trước khi có số.

## Giai đoạn D — Dọn thống kê (1-2 ngày)

**D1. Gán app cho toàn bộ 631 ep app_unseen.** Ưu tiên `open_app.app_name`; regex chỉ dùng khi có duyệt tay. Chuẩn hoá tên, gộp bí danh, rà tay ~70 tên cuối. Ep không gán được thì loại khỏi phân tích cụm, đừng đoán bừa.

**D2. Tính lại G thật và MDE** bằng phân rã phương sai (giữa app vs nhị thức trong app), không lấy SD thô của pilot. Sửa report/85 và 86.

**D3. Điền ô MDE trục trung thực.** Nếu ra ~30 pp thì quyết ngay: tăng số app MobileViews, hay hạ trục đó xuống mức mô tả và khai là không đủ lực.

**D4. Đặt một ngưỡng riêng có căn cứ cho trục ĐÚNG.** Hiệu bao nhiêu pp thì mới đáng gọi là đóng góp model? Ngưỡng 15-20 hiện đang mượn của trục khác.

## Giai đoạn E — Gặp thầy (sau D, trước khi tiêu tiền)

Mang theo: file này, kết quả B1 (thước rớt hay đậu), kết quả C1 (thước có nối được với người không), G/MDE đã tính lại.

Bốn câu cần thầy quyết, không tự quyết được:
1. Nếu thước rớt ở B1 và không vá nổi — chuyển trọng tâm sang **chương đo lường** (bốn phép thử + phát hiện về thước) có đủ ngưỡng thạc sĩ không?
2. Gold AC là nhãn thao tác ngắn. Train trên đó rồi gọi là "sinh hướng dẫn cho người" — thầy có chấp nhận khung đó không, hay bắt thêm tầng viết lại + eval người?
3. GuideMe (CHI 2026) đã chiếm tác vụ ở mức khái niệm. Đóng góp model nên định vị lại thế nào?
4. Bỏ FAIR 15/8 để cứu VCL và luận văn — thầy đồng ý không?

## Giai đoạn F — Chỉ khi A-E đã xong

**F1.** Quyết bỏ/giữ FAIR — **việc này làm ngay tuần này**, đừng đợi hết E. Nếu giữ thì cắt ngay ablation MobileViews-aux, Tier 2, ScreenSpot, chấp nhận bài chỉ có trục ĐÚNG. Và viết lại `KE_HOACH_2_BAI_BAO` §2 theo khung LAI trước khi làm gì khác — abstract hiện tại vẫn đang bán đóng góp đã chết.

**F2.** Smoke-test sinh tiếng Việt bằng Qwen local (free) trước khi tin VCL là sàn an toàn. Đặc biệt test cách "bảo model giữ tên nút tiếng Anh" — hiện chưa có số nào.

**F3.** Tải AC train-split, lọc dữ liệu (bỏ bước rỗng, gộp cặp trùng liên tiếp ~20%).

**F4.** Thêm nhánh **Teacher-STYLE-MATCHED** vào thiết kế và đăng ký trước, trước khi train. Không có nhánh này thì con số headline không diễn giải được.

**F5.** Mua Colab, train.

---

## Thứ tự rút gọn, nếu chỉ nhớ được một dòng

> Dừng overclaim (A) → dựng lại thước và chấp nhận nó có thể rớt (B) → hỏi người xem thước có đo đúng thứ cần không (C) → dọn thống kê (D) → gặp thầy (E) → mới train (F).

Bốn giai đoạn đầu **không tốn một đồng nào** và mất khoảng một tuần rưỡi. So với việc train xong mới phát hiện thước đo nhầm thứ, đây là món hời.
