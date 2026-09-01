# 127 — CHỐT BÀI FAIR, vòng giám khảo 30/8/2026

> Vòng phản biện bốn giám khảo độc lập trên bản `paper/fair2026/main.tex` (8 trang, 0 overfull),
> rồi vá, rồi soi lại vòng hai. **Mọi đòn đều được tự kiểm lại từ mã/dữ liệu thô trước khi vá** —
> có đòn agent báo sai (xem Mục 5).
>
> Bản trước vòng này: `paper/fair2026/main_TRUOC_VONG_GIAMKHAO_30_8.tex.bak`.

## 0. Phán quyết vào vòng

Area Chair chấm **borderline-reject**, lý do không phải khoa học mà là **90 giây đầu bán sai bài**:
tiêu đề hứa một ablation, tóm tắt 382 từ dành quá nửa độ dài cho các cụm *cannot be completed ·
abandoned · inconclusive · died at its feasibility gate*. Reviewer thứ ba kết luận "không có kết
quả" trước khi tới trang 2.

## 1. Ba đòn mức CHẶN — đều tự kiểm và đều ĐÚNG

### (a) `b`/`c` bị đảo ở BA chỗ, một trong đó là đại lượng headline
Bài tự định nghĩa `b` = số bước **nhánh thấp hơn** giải được. Đếm lại từ `runs/score_*_raw.jsonl`:

| phép so | b thật | c thật | bài ghi | |
|---|---|---|---|---|
| S1−Base | 284 | 798 | b=284, c=798 | ✅ |
| S2−S1 | 254 | 340 | b=254, c=340 | ✅ |
| **MIN−CE2** | **42** | **70** | b=70, c=42 | ❌ đảo |
| **f2 bỏ tên** | **3** | **58** | b=58, c=3 | ❌ đảo |
| **p3 bỏ vị trí** | **1** | **8** | b=8, c=1 | ❌ đảo |

Giám khảo áp đúng định nghĩa của bài sẽ tính `(c−b)/n` ra **dấu âm** ở đúng con số +0,63.
**Đã vá cả ba + định nghĩa quy ước ngay tại lần dùng đầu (§V-B) thay vì để tới §VII-A.**

### (b) Trần **70,0** — con số bài TỰ TUYÊN BỐ đã rút — đang sống ở Bảng II
Hàng `Ceiling on slice` lấy từ `runs/gate_a/gate_A_ceiling.json` (**n=300**) và
`runs/venus/tran_1003k.json` (**n=300**), **không phải** lát 2.532 như caption ghi. Mà 70,0 chính
là số §V-B viết *"that number is withdrawn"*. Reviewer đọc trang 4 rồi trang 5 bắt được mâu thuẫn
trực tiếp.
**Đã vá:** đổi nhãn hàng thành `Gate ceiling ($n{=}300$)`, caption nói rõ đây là mẫu cổng A dùng để
so hai dụng cụ với nhau, và trần đủ tập là 75,7.

### (c) "Pre-registration dự báo +0,35 pp … written down before the run" — KHÔNG có trong hồ sơ
Truy `report/106`: hệ số 0,43 nằm ở mục **(x10)**, tiêu đề *"ĐIỂM EXECUTABILITY CỦA MIN-DESC/101"*,
đề ngày **25/8** — tức đo **sau** khi chạy. Mục (x11e) mà bài viện dẫn **không chứa +0,35**, và
(x11e) nói về biến thể **on-policy**, không phải MIN−CE2. Với một bài bán điểm bằng pre-registration,
đây là chỗ giám khảo xin xem hồ sơ và không thấy.
**Đã vá:** hạ cấp thành *"estimated post hoc on these same checkpoints … a consistency check, not a
registered prediction."*

## 2. Sáu đòn mức nặng khác — đã vá

| # | đòn | số tự kiểm | vá |
|---|---|---|---|
| 1 | KTC `[+0,16 · +1,10]` gán cho SE 0,38 | SE thật của cặp MIN/CE2 = **0,237**; SE 0,378 là của cặp hạt giống; SE 0,779 là của S1−Base | khai SE riêng cho từng phép so |
| 2 | Giải thích MDE 2,11 *"without that doubling"* **sai số học** | bỏ doubling cho **1,67**; 2,11 = thiết kế một-hạt-giống, hạng hạt vào theo **√2σ** | viết lại, nêu cả ba mốc 2,8 · 2,11 · 1,67 |
| 3 | *"clustered by application"* tả thiếu luật gộp | `mde_that.py:cum()` → G 1.091 = **259 cụm app + 832 cụm tác vụ**, 59,3% số bước ở cụm tác vụ | khai đủ luật |
| 4 | Luận cứ *"ô toạ độ là ô gánh"* dựa trên hai hiệu không tách khỏi 0 | bootstrap cụm tự dựng: `+1,11 [−2,48 · +4,74]` và `+0,54 [−2,79 · +4,26]` — phủ 0 và chồng nhau | đổi thành "license no verdict on either slot", thêm KTC |
| 5 | *"the same split"* ở tầng khai báo | 5,90/6,70 = **88/12**, không phải 78/22 | "a steeper split … $88/12$" |
| 6 | *"well inside the range a seed change produces"* | 57,20→55,97 là **2,7σ**, không "well inside"; cạnh dương cần **16,9σ** | nói thẳng hai con số — trung thực mà lại mạnh hơn |

Kèm: `84,3%` bị tả sai là *"against a sentence"* (thật ra là **bơm lỗi dịch điểm sang tâm phần tử
khác, 250 bước, không gọi bộ trỏ**) và trùng số với cột dung sai của câu người ở Bảng I ⇒ đã nói rõ
điều kiện và nói rõ sự trùng; Aguvis 11,4 là **hiệu tự trừ** chứ không phải số họ báo; *"three keys"*
→ **four**; Bảng II không khai rằng hàng S2−S1 đã quy về mẫu số 4.463.

## 3. Bán bài — đã đổi

- **Tiêu đề:** *…and a Diagnosis of Where It Breaks* → ***…and the Condition Under Which It Pays***.
  Tự dán nhãn negative-result ở dòng đầu là mất điểm miễn phí. (Không chọn phương án
  *"Identification Accuracy Governs…"* vì bảng 2×2 là phân tầng hậu kiểm — sẽ thành over-claim.)
- **Tóm tắt 382 → 353 từ**, đảo cấu trúc: dụng cụ đã hiệu chuẩn (trần 75,7 · sàn 12,0 · **sàn văn
  phong đúng nội dung sai 6,1**) lên trước, kết quả dương đứng trước lời thú nhận, thêm câu
  *"no positive result is being withheld"*. ⚠️ **Giữ lại 57,2 và −1,93 trong tóm tắt** — hai giám khảo
  đề nghị bỏ, nhưng bỏ chiều của kết quả khỏi tóm tắt trong khi bài bán bằng minh bạch là tự mâu thuẫn.
- **Đóng góp 3 → 4 mục**, sàn đo được lên **mục (i)** thay vì làm phụ chú sau danh sách.
- **Từ khoá:** `ablation study` → `reference-free evaluation` (từ khoá quyết định bidding; cần ít nhất
  một reviewer mảng đánh giá sinh ngôn ngữ, vì đó là chỗ bài mạnh nhất).
- **`budget` 5 lần → 2.** Nói một lần ở đúng chỗ là liêm chính; nói năm lần là mời câu reject rẻ nhất
  *"resubmit when the second seed is done"*.
- **`governed by` → `conditional on`** ở tóm tắt và kết luận (khẳng định nhân quả rút từ phân tầng
  hậu kiểm; §VIII giữ được vì lời khai nằm ngay trên).

## 4. Văn phong — đo, không phán bằng cảm giác

| mẫu | trước | sau |
|---|---|---|
| cụm sáo AI (delve/underscore/crucially/showcase/leverage…) | **0** | 0 |
| em-dash `---` trong thân bài | 55 | **31** |
| tic `", not X"` | 22 | 20 |
| câu dài nhất | **98 từ** | tách thành 5 câu |

Tầng từ vựng vốn đã sạch tuyệt đối; bài lộ ở **tầng cú pháp** — một nước tu từ `X, not Y` dùng 36 lần
và khuôn nhịp "nhồi dài → chốt cách ngôn ngắn" 15/59 đoạn. Đã hạ em-dash gần một nửa, phá các câu
chốt tự chấm điểm (*"The decomposition is the part worth carrying forward"*, *"Read together, the
three tables say more than…"*), sửa câu garden-path ở định nghĩa thước, và đặt tên `MIN`/`CE2` **trước**
lần dùng đầu (trước đây dùng ở dòng 407 và Bảng I nhưng chỉ định nghĩa ở dòng 554).

## 5. ⭐ Bài học: agent cũng phải kiểm như mọi nguồn khác

- Giám khảo D báo *"1.825 trượt / **1.570** thao tác đúng"*. Tự đo lại:
  **1.825 / 1.573 (86,2%)** — con số 1.570 của agent **sai**, `CLAUDE.md` mới đúng ở vế đó.
  (Vế kia thì `CLAUDE.md` lệch một bước: 1.824/251 → đã vá thành **1.825/252**.)
- Giám khảo A đề nghị viết *"22,0% … carry no name anywhere in the accessibility tree"* — **sai**,
  22,0% là không có tên từ **cả cây trợ năng lẫn OCR**, mạnh hơn hẳn. Đã viết đúng.
- Bốn khoảng tin cậy của bảng 2×2 **tự dựng lại bằng bootstrap cụm** (hạt 20260805) trước khi đưa vào
  bài, không lấy số agent đưa.

## 6. Trạng thái cuối

`tectonic -X compile main.tex --outdir . --keep-logs` ⇒ **8 trang, 0 overfull, 0 tham chiếu hỏng**,
28 tài liệu tham khảo, 5 từ khoá (đúng trần FAIR), tóm tắt 353 từ.

⚠️ Để về đúng 8 trang sau khi thêm các lời khai mới, đã cắt: câu BLEU/ROUGE (chính bài viết
*"we draw nothing from that agreement"*), dòng S1 thừa ở chế độ (c) của bảng ví dụ, và nén
Hạn chế + Kết luận. **Không con số nào bị đổi** — đã `diff` toàn bộ chữ số giữa hai bản để xác nhận.
Thư mục tham khảo chuẩn hoá `et al.` cho mục ≥4 tác giả (trước đây lẫn lộn).

---

## 7. VÒNG HAI — soi lại chính bản đã sửa

Hai giám khảo độc lập đọc lại bản sau khi vá. Kết quả: **mọi con số mới thêm đều truy được về
nguồn và khớp** (16 giá trị: 0,24 · 0,52 · 0,785 · 1,67 · 2,7 · 16,9 · 21,9 · 250 · 259 · 832 ·
88 · 4,3 · 4,7 · 7,0 · 12 · 59), và trần **70,0 không còn được dùng như số sống** ở bất kỳ đâu.

Nhưng vòng hai bắt được **lỗi do chính lần sửa gây ra** — đúng thứ phải soi khi đụng vào hàng chục
chỗ trong một lượt:

| # | lỗi mới | vá |
|---|---|---|
| 1 | ⛔ Caption Bảng I vừa thêm viết CE2/MIN là *"the checkpoint their branch descends from"* gắn với **S1** — SAI, hai nhánh đó nối tiếp từ **S2** (§VII-D nói rõ). Tự mâu thuẫn với thân bài. | "CE2 and MIN continue from S2/101, so they are paired against S1 at seed 101" |
| 2 | ⛔ Tóm tắt viết lại **mất nhãn *inconclusive*** cho +0,63 — chỗ đông người đọc nhất lại trình nó như một mức tăng dương không cảnh báo | trả lại "inconclusive again" |
| 3 | ⛔ Bảng ví dụ hứa ***verbatim*** nhưng lúc nén tôi cắt mất chữ trong ô khai báo (`the only icon button` thay vì `the only icon button on screen`). Chuỗi thật đã đối chiếu `runs/preds_s2_seed101.jsonl` (37 bản ghi) | trả lại nguyên văn; và trả lại luôn dòng S1 ở ví dụ (c) cho cân ba ví dụ |
| 4 | Chữ *"such"* bị nén mất ở "the other 228 **such** steps" — mất chữ đó thì 228 và 325 trông như cùng mẫu số | trả lại |
| 5 | Tóm tắt nói "one of four runs" mà chưa hề nêu thiết kế 2 nhánh × 2 hạt ⇒ không có tiền ngữ | "the second seed of that branch was never run" |
| 6 | `0,52` chỉ có ở tóm tắt, thân bài ghi `+0,5` ⇒ giám khảo bấm máy 11,5/0,5 = 23, không ra 22 | thân bài đổi thành **+0,52** (59,624 − 59,108 = 0,516) |
| 7 | `+5,90` / `+0,80` in hai chữ số thập phân nhưng suy từ bảng một chữ số (thực đo 5,93/0,84) | hạ xuống **+5,9 / +0,8**; tỉ lệ 88/12 đúng ở cả hai cách tính |

**Lý do reject mạnh nhất còn lại** (giám khảo vòng hai tự nêu): nhan đề mới hứa *"the Condition Under
Which It Pays"*, mà toàn bộ bằng chứng là **phân tầng hậu kiểm theo biến do chính phép can thiệp
sinh ra, một hạt giống**. Bài **có** phản bác — cột Base và cột trần của Bảng III không bị điều kiện
hoá, và trần ở ô hỏng vẫn **66,3%** trong khi nhánh điều trị rơi xuống 5,6 — nhưng nó nằm ở đoạn 3
của một tiểu mục, trong khi caption ngay phía trên lại tự hạ *"not a causal claim"*.
⇒ **Đã đưa manh mối phản bác vào chính caption:** *"Post-hoc stratification, bounded by the Ceil.
column rather than a causal claim."* Giữ nguyên lời tự hạ, nhưng đặt cùng chỗ với cáo buộc.

## 8. Còn để ngỏ, biết mà chấp nhận

- **σ hạt giống 0,46 không dẫn được ra từ 0,52 trong bài.** 0,52 là hiệu thô giữa hai hạt, 0,46 là
  σ đã khoá trong hồ sơ đăng ký (`report/106:1248`). Hai đại lượng khác nhau, bài dùng đúng tên,
  nhưng không có câu nào nối chúng. Nếu giám khảo hỏi thì trả lời được; chưa viết vào bài vì hết chỗ.
- **Câu BLEU/ROUGE bị cắt số** (9,7/40,3 vs 38,7/67,3). Khẳng định "xếp cùng thứ tự" nay không có số
  đỡ. Chấp nhận: chính bài viết *"we draw nothing from that"*, và đó là chỗ trả tiền trang.
- **Nhánh on-policy chết ở cổng** vẫn báo đủ ở thân bài (§VII-D: 14.000 màn → 459 cặp = 3,3% vs
  ngưỡng 25%) nhưng **đã gỡ khỏi tóm tắt và kết luận**. Cam kết (x11d) *"báo cả ba nhánh"* vẫn thoả
  — chỉ giảm độ nổi bật.
- **Đòn "3B, một dataset, một cấu hình, không so hệ thống ngoài"** không vá được bằng dữ liệu hiện
  có; §IX đã giải thích bằng lợi thế sân nhà (95,6% app tập kiểm có trong tập dạy). Sống chung.

## 9. Trạng thái chốt

**8 trang · 0 overfull · 0 tham chiếu hỏng · 28 tài liệu · 5 từ khoá (đúng trần FAIR) · tóm tắt 356 từ.**
Nhan đề: *Descriptor-First Supervision for GUI Instruction Generation: A Pre-Registered Ablation and
the Condition Under Which It Pays.*
