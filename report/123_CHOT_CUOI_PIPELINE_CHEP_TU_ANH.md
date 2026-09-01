# 123 — CHỐT CUỐI: PIPELINE MÔ HÌNH THÁNG 9 (bản chép lại từ ảnh, 29/8/2026)

> ⚠️ **ĐÂY KHÔNG PHẢI FILE GỐC.** Đây là bản chép lại từ **13 ảnh chụp màn hình** máy Mac
> (`report/debate_29_8_anh/debate_01..13.jpg`, chụp lúc 15:51–15:54 ngày 29/8/2026).
> File gốc là `report/123_CHOT_CUOI_PIPELINE.md` — **chưa có trên kho WSL này**.
> Cùng cảnh ngộ: `122`, `124_GIAI_THICH_CHO_NGUOI_DOC.md` cũng chưa có.
>
> ⛔ **ẢNH CHỈ PHỦ TỚI §3.4.** File gốc còn ít nhất §5 (khối ứng viên), §7 / §7.5 (quyết định
> cuối + ngân sách), §12 (mẫu (x16) dán vào `106`), §16 (bảng kiểm toán số) — **không có ảnh
> nào chụp các mục đó**. Mọi trích dẫn §5/§7/§12/§16 dưới đây là *tham chiếu gián tiếp* mà
> ảnh nhắc tới, không phải nội dung đã đọc.
>
> ⇒ **Lấy file gốc về trước khi thi hành bất cứ thứ gì.** Đặc biệt §7.5 — chính file tự tuyên
> bố §7.5 *"thắng mọi mục khác nếu có xung đột"*, mà §7.5 **không nằm trong ảnh**.
>
> ✅ **CẬP NHẬT 30/8 — §7.5 · §7.2 · §5.1 · §7.3 · §8 · §12 · §16 + MỤC LỤC §4–§16 ĐÃ CÓ:**
> máy Mac mở file gốc và trả lời trọn vẹn ⇒ **`report/126_TRA_LOI_MAC_30_8.md`**.
> ⛔ **Mâu thuẫn thì `126` thắng file này** — `126` đọc từ bản gốc vòng 5, file này chép từ ảnh
> và ảnh chỉ phủ tới §3.4.

---

## 0. Ảnh nào ứng với mục nào

| ảnh | nội dung |
|---|---|
| 01 | tiêu đề · §0 tóm tắt một trang · điểm nền · bảng lát chọn đúng / chọn sai |
| 02 | 22 bước ẩn số · hai điều quyết định kế hoạch · độ dốc thật 0,456 · bảng mục tiêu 65/70% · mở đầu HƯỚNG CHỐT CUỐI |
| 03 | HƯỚNG CHỐT CUỐI (SEL+GEN) · `Δ_component` · đổi epoch 2→1 lấy hạt thứ hai · backbone Qwen3-VL-4B · ngân sách |
| 04 | §1 luật đọc file · §2 mở đầu · §2.1 bồi vị trí vào đích train — CHẾT |
| 05 | §2.2 bồi vị trí lúc suy luận — CHẾT · §2.3 ép TÊN nguyên văn — CHẾT · §2.4 đổi thước — CHẾT · §2.5 đầu phân loại — không khả thi · §2.6 mở đầu |
| 06 | §2.6 bảng AUC↔lợi ích · không có tín hiệu tin cậy nào dùng được · bảng câu fallback |
| 07 | §2.6 bảng nội sinh vs ngoại sinh · SafeGround/HyperClick · KẾT LUẬN VÒNG 5 hạ cơ chế từ chối |
| 08 | "Vì vậy" · §2.7 đòn chính thật sự = nâng `sel_acc` · trần cứng thứ hai: độ phủ khối ứng viên |
| 09 | truy xong 71,6% · bảng tầng tên (test/train) · vì sao 80,2 vs 91,2 không mâu thuẫn |
| 10 | §3 KIẾN TRÚC CHỐT — sơ đồ SEL+GEN |
| 11 | §3.1 câu nhắc · `prompt_body(step, ocr, *, cands=None)` · §3.2 đích sinh nhánh xử lý |
| 12 | §3.2 tiếp · `gold_candidate()` · §3.3 nhánh đối chứng |
| 13 | §3.3 tiếp · §3.4 ĐÃ BỎ (suy luận hai lượt + ngưỡng τ) — hết ảnh |

---

## 1. Luật đọc file (ảnh 04)

⭐⭐⭐ **123 là file chốt. Không đọc `122` (đã bị thay).** Trạng thái: **vòng 5, 26/8/2026**.

Thứ tự đọc bắt buộc cho chat mới, đúng thứ tự:
1. **§0** — tóm tắt một trang: điểm nền, bảng lát, độ dốc thật, hướng chốt.
2. **§7.5** — ⭐ QUYẾT ĐỊNH CUỐI. Mục này thắng mọi mục khác nếu có xung đột.
3. **§2.6 + §2.7** — vì sao cơ chế từ chối bị loại, và hai trần cứng (oracle-chọn **75,3%** · độ phủ **67,2%**).
4. **§16** — bảng kiểm toán số, chỗ yếu tự khai, những gì đã sửa qua 5 vòng.
5. **§12** — mẫu (x16) để dán vào `106` **trước khi** dựng dữ liệu.

**Thứ tự thắng giữa các file:** `123` (làm gì) > `106` (ngưỡng, luật đọc, thước) > mã `harness/`
(hệ thống đang chạy) > `121`, `122` (bối cảnh, không triển khai nguyên).

⛔ **LUẬT XUNG ĐỘT:** file đã qua 5 vòng phản biện nên có mục bị thay mà vẫn giữ lại để tra cứu.
Khi hai mục nói ngược nhau, **mục nào có nhãn "vòng 5" thì mục đó đúng**. Bốn mục sau
**KHÔNG THI HÀNH** (đều đã dán nhãn ⛔ ở đầu mục):
· §3.4 (hai lượt + τ) · §7.0 (G0 là cổng) · §7.1b (thiết kế hai giai đoạn) · và mọi chỗ nói cơ
chế từ chối là đóng góp chính.

⚠️ **Ba con số của bản nháp cũ đã bị chứng minh SAI, đừng trích lại:**
· độ dốc `0,752` → thật **0,456**
· `sel_acc` cần **73,1%** cho exec 65% → thật **77,4%**
· trần cơ chế từ chối `+5,04 pp` → thật **+0,58 pp**

⛔ **Chat thi hành:** đừng làm theo sơ đồ/lịch còn chữ τ, G7-cổng, hay "học từ chối là đóng góp
chính" nếu mục đó không có nhãn vòng 5. Bản người-đọc (`124`) viết lại dài hơn; **không sao chép
văn phong `124` vào file này**.

**Ràng buộc GVHD:** đóng góp chính phải là **MÔ HÌNH**. Thước là khung chấm, không phải đóng góp.
Mục tiêu điểm: **65% là stretch** (P ≈ 40–50%); **70% đã BỎ HẲN** — vòng 5 chứng minh không tới
được vì độ phủ khối ứng viên chặn ở ~71,6%.

---

## 2. §0 — Tóm tắt một trang (ảnh 01–03)

### Bài toán (không đổi)
Ảnh screenshot Android + mục tiêu người dùng → sinh **một câu tiếng Anh hướng dẫn cho NGƯỜI đọc**
("Tap the Search icon at the top right"). **Không sinh toạ độ.**

### Chấm (không đổi)
Câu sinh ra → `osunlp/UGround-V1-2B` (bộ định vị độc lập, **không dùng lúc train**) → trả về một
điểm. Bước ĐẠT khi loại thao tác khớp câu chuẩn **và** điểm rơi vào ô Voronoi quanh điểm chạm thật
của người. `harness/metric_exec.py`, **n = 4.463** bước chạm.

### Điểm nền
| nhánh | exec |
|---|---|
| Người (trần) | **75,73%** |
| MIN-DESC | **60,05%** |
| CE2 | **59,42%** |
| S1/101 | **59,11%** |
| S1/202 | **59,62%** |
| S2 | **57,18%** |
| Base | **47,59%** |
| sàn — câu rỗng | **12,00%** (n=800) |
| sàn — câu sai màn | **6,12%** (n=800) |

### ⭐ Chỗ nghẽn (đo lại 26/8, đã kiểm toán độc lập)

Chia theo việc mô hình **chọn đúng phần tử hay không**. Luật: **L2 ≤ 0,14W** giữa điểm mô hình tự
khai và điểm vàng. Mẫu số đầy đủ **4.463** — bước mô hình không khai được điểm thì tính là **chọn
sai** (đó là hành vi đúng: không khai được thì không chọn được).

| lát | n | % mẫu | MIN | S1 | người |
|---|---|---|---|---|---|
| **chọn đúng phần tử** | 2.970 | 66,5% | **85,2%** | 76,2% | **85,7%** |
| **chọn sai phần tử** | 1.493 | 33,5% | **10,0%** | 25,1% | **55,9%** |

✅ **22 bước từng là ẩn số đã truy xong (26/8):** `2.970 + 1.471 = 4.441` là con số của bản nháp
cũ, thiếu 22 bước gồm **1 bước câu rỗng của S1** (`episode 18710, step 1`) và **21 bước MIN không
parse được điểm** (17 bước không sinh `<desc>`; 4 bước có `<desc>` nhưng `<point>` sai định dạng —
có ca viết `941 87` thiếu dấu phẩy; phần lớn là bước *swipe / open app / type*). Nhóm này chỉ đạt
~14%, tức rất tệ. Bảng trên đã gộp chúng vào lát "chọn sai" ⇒ mẫu số khép kín ở 4.463, không còn ẩn số.

⚠️ Ghi chú *"2 bước `bo_qua`"* ở bản nháp cũ là **sai** — trường `action_ok` trong tệp thô là kiểu
bool, không có giá trị `bo_qua`; dấu hiệu thật là câu rỗng, và chỉ S1 có đúng 1 bước như vậy.

⚠️ **Bảng này dùng luật L2 trên điểm.** `106` (x10b) dùng luật khác (khớp tên ∧ point hình chữ
nhật) và ra **60,6%** thay vì 66,5%; **hai luật, hai số, đừng trộn**. Cũng vì thế lát điểm sai
(n=1.493) **không phải** ô D của `122` (tên sai ∧ điểm sai, n=745) — lát mới rộng gần gấp đôi,
nên trần oracle **65,09%** ở đây so với ~63,8% trong `122` là do **đổi định nghĩa lát**, không
phải sai số làm tròn.

### ⭐ Hai điều quyết định toàn bộ kế hoạch

1. **Lát chọn đúng đã BÃO HOÀ** — MIN 85,2% ≈ người 85,7%. Không còn gì để vắt ở đây.
2. **Toàn bộ dư địa nằm ở lát chọn sai:** so với người (55,9%), lát này còn **+15,37 pp** toàn
   cục — đây là đòn bẩy thật và **không phụ thuộc định nghĩa lát**.
   ⚠️ Trên cùng lát đó, *khai sai tự tin* (MIN 10,0%) trông tệ hơn im lặng (S1 25,1%) tới 15,1 pp,
   NHƯNG con số này **77% là artefact chọn lát nội sinh** — định nghĩa lát bằng khai báo ngoại
   sinh thì chỉ còn **3,55 pp** (§2.6 mục 4). ⛔ **Đừng dùng 15,1 pp để biện minh cơ chế từ chối.**

### Độ dốc — ⚠️ ĐÃ SỬA LẦN HAI (vòng 5), bản cũ THỔI

Công thức cũ `exec = sel_acc × 85,2% + (1 − sel_acc) × 10,0%` (⇒ dốc 0,752) **giả định bước MỚI
được chọn đúng cũng hưởng 85,2%**. Giả định đó sai: lát chọn sai là lát **KHÓ**, đo bằng thước độ
khó ngoại sinh (exec của người): **85,7%** ở lát đúng vs **55,9%** ở lát sai ⇒ tỉ số **0,653**.
Bước mới chuyển sang chỉ kỳ vọng `85,22 × 0,653 = 55,6%`, không phải 85,2%.

⇒ **Độ dốc thật ≈ 0,456 pp exec / pp `sel_acc`**, không phải 0,752. Mô hình cận biên đúng:

```
exec(x) = [2.970 × 85,22% + 1.493 × (x × 55,6% + (1−x) × 10,0%)] / 4.463
```
với `x` = tỉ lệ lát sai được cứu.

| mục tiêu | cần cứu bao nhiêu lát sai | = số bước | `sel_acc` tương đương |
|---|---|---|---|
| **65%** | 32,4% | **484** | **77,4%** |
| 70% ⛔ đã bỏ | 65,2% | 973 — nhiều hơn số bước có sẵn | 88,3% |

⛔ Con số **73,1% / 79,8%** ở bản trước là **THỔI** (và 73,5% / 80,1% ở bản trước nữa vừa thổi vừa
sai phép giải). Trần nếu `sel_acc = 100%` chỉ là **75,3%** — tức xấp xỉ đúng trần người 75,73%,
không còn 10–15 pp để xé như bản cũ ngụ ý.

---

## 3. ⭐⭐⭐ HƯỚNG CHỐT CUỐI (vòng 5, 26/8) — `SEL + GEN`, 1 epoch × 2 hạt giống (ảnh 03)

⛔⛔ **CƠ CHẾ TỪ CHỐI ĐÃ BỊ LOẠI khỏi vai trò đóng góp chính.** Đọc §2.6 trước khi làm gì.
Tóm tắt: trần thật chỉ **+0,58 pp** (không phải +5,1) khi dùng fallback có họ gần đối chứng nhất;
**77% lập luận biện minh nó là artefact chọn lát nội sinh**; cổng G7 cũ có công suất bằng 0; và từ
chối làm mất **7 pp** `action_ok`. `<sel>none</sel>` **vẫn giữ làm nhãn train** (miễn phí, cần cho
tính đúng đắn của nhãn) và đường risk–coverage báo như **kết quả mô tả thứ cấp**.

### Một mô hình, hai việc có thứ tự
1. **Chọn một dòng** trong khối ≤40 ứng viên trên màn (node trợ năng có tên — §5.1), hoặc
   `<sel>none</sel>` khi khối không chứa ứng viên vàng.
2. **Sinh câu tiếng Anh** (câu vàng nguyên bản, không viết lại).

⛔ **BỎ:** ngưỡng τ · suy luận hai lượt · biến thể một-lượt · cổng G0/G7/L4/L5.
Chưa viết dòng mã nào ⇒ bỏ tốn **0 giờ** và tiết kiệm **5,4 h Kaggle**.

### Đại lượng khoa học — đúng một biến khác nhau giữa hai nhánh

```
Δ_component = mean_2hạt[exec(SEL+GEN)] − mean_2hạt[exec(SFT−match)]
```

`SFT-match` = cùng backbone, **cùng khối ứng viên trong prompt (byte-identical)**, cùng câu đích,
chỉ **không có đầu chọn**.

### ⭐ Đổi `num_train_epochs` 2 → 1 để mua HẠT GIỐNG THỨ HAI, chạy vô điều kiện
Đây là **quyết định quan trọng nhất của vòng 5**: `106` đọc một hạt giống là **TRẮNG** không ngoại
lệ, nên kế hoạch cũ đốt 66–83 h để lấy một số **không báo cáo được**. Hạt thứ hai chỉ tốn khoảng
**+6 h**. Chi tiết và toàn bộ lý lẽ ở §7.5.

⚠️ **Mục tiêu 70% đã BỎ** — đã chứng minh không tới được: cần cứu 973 bước nhưng chỉ có **~704
bước có ứng viên vàng trong khối** (§2.7, §7.2). **Mục tiêu thực tế: 63,7–65,1%.**

### Backbone: đổi sang `Qwen/Qwen3-VL-4B-Instruct`
Apache-2.0, phát hành 11/2025. Lý do **không dựa trên điểm của chính ta**: ScreenSpot-v2
**93,08%** vs **80,9%** của Qwen2.5-VL-3B; ScreenSpot-Pro **59,50%** vs **25,9%**.
⚠️ **Số benchmark phải xác minh model card trước khi trích luận văn**; hiện được dùng làm quyết
định vận hành tạm. Chi phí không còn 31–39 h/lượt (đó là ước lượng thiết kế 2 epoch). Bàn vòng 5:
**16–20 h/epoch lạc quan · 26–35 h/epoch bi quan**, đo bằng G5b; 4 lượt × 1 epoch.
**Nếu G5b > 27 h/epoch ở 4B thì hy sinh backbone** (về Qwen2.5-VL-3B, ~46 h), ⛔ **không hy sinh hạt.**

### Thước: KHÔNG đổi headline
`hit_voronoi` giữ nguyên. Đã kiểm: nới sang luật hộp **không nâng trần** (Voronoi 82,2% = "chỉ cần
đúng hộp chứa" 82,2% trên lát 698 bước, `report/112` §5.7; luật chữ nhật 14% kiểu AITW còn thấp
hơn, 80,2%) ⇒ đổi luật **không mua được điểm nào**. Thêm 4 thước đồng-báo (§5).

### Ngân sách (bản vòng 5)
~**72–88 h A100** cho 1 epoch × 2 hạt × 2 nhánh + **15 h đệm mất máy** + ~**25 h Kaggle**.
Kỳ vọng exec **63,7–65,1%**, P(≥65%) ≈ **40–50%**.

### ⭐ Chốt vòng 5 (§7.5b)
**1 epoch × HAI hạt giống, chạy VÔ ĐIỀU KIỆN.** Bỏ thiết kế hai-giai-đoạn ở §7.1b — nó đốt 66–83 h
để lấy một hạt mà `106` đọc là TRẮNG, trong khi đổi 1 epoch lấy hạt thứ hai chỉ tốn khoảng +6 h.
Δ cuối cùng báo là **trung bình hai hạt**, chênh giữa hai hạt ≤ 1,5 pp.

---

## 4. §2 — BỐN Ý ĐÃ BỊ GIẾT TRONG VÒNG PHẢN BIỆN (ảnh 04–07)

> Mỗi ý dưới đây từng nằm trong `122` hoặc từng được đề xuất trong vòng 1. **Đều đã chết bằng số,
> không bằng cảm tính.** Ghi ở đây để chat sau không mất tuần đi lại đường cũ.

### 2.1 ⛔ Bồi mệnh đề vị trí vào đích huấn luyện (`122` §4.2b) — CHẾT

Đường suy giảm của hiệu ứng khi siết dần khống chế:

| mức khống chế | hiệu ứng |
|---|---|
| quan sát thô (có vs không từ khoá không gian), S1 | **+14,87 pp** |
| ghép cặp trong cùng hạt | ~**+7 pp** |
| ghép cặp nhân quả (`p3_nopos`, cặp bất đồng) | **+3,5 pp** |
| trên đúng quần thể sẽ được bồi (bước mà người *không* dùng vị trí) | ≈ **−2,47 pp**, KTC trùm cả vùng âm |

**Cơ chế thật:** mệnh đề vị trí **không làm mô hình chọn đúng hơn** — nó chỉ là **kết quả đọc ra**
của việc mô hình *đã biết* phần tử ở đâu. Chứng cứ: đúng ô lưới → exec **93%**; sai ô → **27,7%**.

**Và nó phá Δ.** Nếu bồi cả hai nhánh, SEL+GEN suy ô lưới từ `point` nó **vừa tự sinh trong `<sel>`**
(dùng token đã sinh làm giấy nháp), còn SFT-match phải định vị bằng thị giác. Chênh lệch độ chính
xác ô chỉ riêng khoản này đã **3,06 pp** ⇒ tự chế ra Δ ≈ +2,0 pp mà **không có cải thiện cơ chế
chọn nào**. Δ mất nghĩa.

### 2.2 ⛔ Bồi mệnh đề vị trí lúc suy luận, chỉ 4 góc (phương án cứu của vòng 2) — CHẾT
Ý cứu: không bồi vào đích train, chỉ hậu xử lý lúc suy luận từ `point` đã cam kết, và chỉ ở 4 góc
(vùng mô hình định vị chắc nhất). Vòng 2 đo: **độ chính xác góc chỉ 69,2%** — góc là vùng **yếu
nhất**, không phải mạnh nhất. Điểm hoà vốn cần > **83–85%**. Net: **−2 đến −3 pp**. Bỏ.

### 2.3 ⛔ Ép câu chứa TÊN phần tử nguyên văn — CHẾT
Tên đúng là kênh mạnh (bỏ tên khỏi câu người mất **28,50 pp**, so với vị trí chỉ 3,53 pp), nên ý
này rất hấp dẫn. Nhưng: chỉ **59,3%** câu người chứa tên nguyên văn — người tả **theo chức năng**,
không theo chuỗi ký tự. Ép nguyên văn ⇒ sinh ra câu người sẽ không viết (hại tính hợp lệ construct
của cả bài), và lại **ưu ái SEL+GEN qua kênh giấy nháp** (nó chép tên từ `<sel>`, SFT-match phải
đọc ảnh) ⇒ thổi Δ. Bỏ. **Thay bằng cổng G10 (§7)** để *phát hiện* nếu kênh chép tên tự phát sinh chênh lệch.

### 2.4 ⛔ Đổi thước headline sang `hit_nearest_box` (hoặc bất cứ luật nào) để có 65% — CHẾT
Đây là điều cần nói rõ nhất vì rất dễ bị dụ: docstring trong `harness/metric_exec.py` tự khai chấm
theo tâm *"kết oan 59% câu cùng nghĩa"*, nghe như đổi sang `near_box` là **sửa lỗi** chứ không phải
nới luật. Đã kiểm trên lát 698 bước (bảng 5 luật, `report/112` §5.7):
· trần dưới **Voronoi = 82,2%**
· dưới luật lỏng nhất ("chỉ cần đúng hộp chứa") cũng **= 82,2%** — **bằng nhau**
· ba luật chữ nhật (14% / 7% / 3%) đều **thấp hơn** (80,2% / 74,2% / 56,6%)

⇒ Voronoi **đã là luật cho trần cao nhất**; đổi luật không nâng trần, và đổi luật cũng **nâng sàn**
⇒ dải phân biệt hẹp lại. Số **"~77–78%"** từng được một agent nêu là **bịa**, không có trong repo.

Thêm: dưới `hit_disk`, MIN ≈ S1 (**69,2% vs 69,2%**) ⇒ đổi sang disk **xoá Δ**, tức tự sát trước
yêu cầu "đóng góp mô hình".

⇒ **`hit_voronoi` giữ headline. Không bàn lại.**

### 2.5 ⛔ Đầu phân loại / đầu xếp hạng 40 lớp — không khả thi trong sprint
LLaMA-Factory không hỗ trợ head tuỳ biến. Mọi cơ chế phải diễn đạt được bằng **văn bản sinh ra**
(đó là lý do dùng `<sel>…</sel>` và `<sel>none</sel>`). Đừng bỏ hai tuần viết trainer riêng.

### 2.6 ⚠️ Học TỪ CHỐI (abstain) — sống sót, nhưng ĐÃ BỊ HẠ CẤP từ "đòn chính" xuống "đòn phụ"

Vòng 3 tìm ra ý này từ bảng lát ở §0: khi mô hình chọn sai, **khai sai tự tin (MIN 10,0%) tệ hơn
im lặng (S1 25,1%)** 15,1 pp. Vòng 4 (26/8) đã đo lại và giới hạn nó rất mạnh. **Ba kết quả phải
đọc trước khi tin vào cơ chế này:**

**(1) "+5,04 pp" là trần ORACLE, không phải mức sẽ đạt.** Nó giả định mô hình biết **chính xác**
khi nào nó sai. Mô phỏng bộ phát hiện không hoàn hảo (hai phép mô phỏng độc lập, kết quả trùng nhau):

| AUC của tín hiệu tin cậy | tỉ lệ từ chối tối ưu | lợi ích | exec cuối |
|---|---|---|---|
| 0,60 | ~30% | +0,40 pp | 60,45% |
| 0,70 | ~37% | +1,16 pp | 61,21% |
| 0,80 | ~38% | +2,02 pp | 62,07% |
| 0,90 | ~37% | +3,04 pp | 63,09% |
| **1,00 (oracle)** | ~33% | **+5,04 pp** | **65,09%** |

⭐ **AUC tối thiểu để Δ vượt ngưỡng +2,8 pp của `106` là 0,878** (tại đó: từ chối 36,95%,
TPR 76,48%, FPR 17,64%).

**(2) Không có tín hiệu tin cậy nào dùng được trong dữ liệu hiện tại.** AUC đơn biến: độ dài
`<desc>` **0,517** · có trường dấu hiệu **0,500** (gần như hằng số: 4.433/4.441 mẫu đều có) ·
`n_buttons` **0,530** · `app_seen_in_train` **0,500** · điểm gần rìa màn **0,533**.
Logistic kết hợp, chia 5-fold theo episode: **OOF AUC 0,534**.

⚠️ Con số **0,682–0,702** từng được báo là **RÒ NHÃN**: đặc trưng mạnh nhất trong đó ("tên khai báo
có xuất hiện trong `gold_instruction`", AUC 0,661) dùng **chính câu người** — thứ không tồn tại lúc
suy luận. Bỏ nó ra thì còn **0,534**. Đừng lặp lại lỗi này.

**(3) Điều kiện thứ hai, độc lập và cũng khắc nghiệt: câu lúc từ chối phải ĐỦ TỐT.**
"S1 = 25,2%" là **fallback SFT lạc quan**, không phải phép đo hành vi im lặng thật. Đo các đại
diện khác trên đúng lát đó:

| câu thay thế khi từ chối | exec trên lát sai | trần oracle toàn cục |
|---|---|---|
| S1/101 (lạc quan nhất) | 25,22% | +5,04 pp |
| Base | 19,31% | +3,09 pp |
| **S2/101 — gần nhất với "mô hình đã học chọn"** | **15,91%** | **+1,97 pp** |
| **CE2-S2** | **11,69%** | **+0,58 pp** |
| câu sàn (`Tap the button.` / câu sai màn), lát 271 bước | 5,17% | âm (MIN trên cùng 271 bước: 10,33%) |

⭐ Với đại diện S2 — hợp lý nhất về mặt cơ chế — thì **ngay cả bộ phát hiện HOÀN HẢO cũng chỉ đạt
62,02%, KHÔNG vượt +2,8 pp**. Và "im lặng" theo nghĩa đen (câu chung chung) còn **tệ hơn khai sai**.
Điều kiện cần, ngay cả với detector hoàn hảo: exec của câu fallback trên lát sai phải **≥ 18,43%**.
Nên khoá cổng vận hành ở **≥ 20%**.

**(4) ⛔⛔ ĐÒN NẶNG NHẤT (vòng 5, 26/8): 77% của khoảng cách 15,1 pp là ARTEFACT CHỌN LÁT NỘI SINH.**
Lát "chọn sai" được định nghĩa bằng khai báo của **chính MIN**, nên câu "MIN khai sai ⇒ MIN chỉ
được 10,0%" gần như là **hằng đẳng thức**. Định nghĩa lại lát bằng khai báo **ngoại sinh** (của S2),
bootstrap cụm theo 260 app, 2.000 lượt:

| định nghĩa lát SAI | n | MIN | S1 | Δ(MIN − S1) |
|---|---|---|---|---|
| **nội sinh** (khai của chính MIN) | 1.493 | 10,0% | 25,1% | **−15,07 pp** |
| **ngoại sinh** (khai của S2) | 1.663 | 22,5% | 26,1% | **−3,55 pp** |
| **độ thổi do chọn lát** | | | | **−11,50 pp · KTC95 [−13,37 · −9,40]** |

KTC loại 0 ⇒ **độ thổi là thật, không phải nhiễu**. ⇒ Tiền đề *"khai sai tự tin tệ hơn im lặng"*
chỉ còn ≈ **3,5 pp**, và trần oracle của cơ chế từ chối rơi xuống ≈ **+1,3 pp**.
⚠️ S2 là **tổ tiên** của MIN nên còn tương quan dư ⇒ độ thổi thật có thể **lớn hơn**, không nhỏ hơn.

**(5) ⛔ Từ chối làm HỎNG phần MIN đang thắng.** Trên lát chọn-sai: `action_ok` của MIN **97,7%**
vs S1 **90,6%** (CE2 97,6%). Chuyển hành vi sang phía đối chứng mất **7 pp** độ chính xác loại thao
tác, trừ thẳng vào mọi khoản lợi từ việc nhắm.

**(6) Tài liệu đã đo đúng tín hiệu này và nó không đủ mạnh.** SafeGround (preprint 02/2026) định
nghĩa baseline `PC` = *"one minus the average token probability"* — **đúng công thức `conf` của
file này** — và báo AUROC phân biệt đúng/sai trên bộ định vị GUI: UI-TARS-1.5-7B **0,784** ·
Holo1.5-3B **0,758** · Holo1.5-7B **0,698** · GTA1-7B **0,611** (trung bình **0,713**).
HyperClick (preprint 10/2025) kết luận mô hình GUI *"lack self-awareness of their capability
boundaries, leading to overconfidence"*. Ở AUROC 0,713 thì Δ tốt nhất qua **mọi** τ chỉ **+1,27 pp**;
phương pháp tốt nhất của SafeGround (0,816) cần **10 mẫu ngẫu nhiên + phân bố không gian**, không
phải logprob, và **vẫn dưới mốc 0,878**.

### ⛔⛔ KẾT LUẬN VÒNG 5 — CƠ CHẾ TỪ CHỐI BỊ LOẠI KHỎI VAI TRÒ ĐÓNG GÓP CHÍNH

Sáu kết quả trên **độc lập với nhau** và **mỗi cái một mình đã đủ** để hạ cơ chế. Cộng lại:

| lớp giới hạn | trần còn lại |
|---|---|
| trần oracle với fallback S1 (giả định lạc quan nhất) | +5,04 pp |
| … thay bằng fallback CE2 (nhánh có họ gần `gui_sft_match` nhất) | **+0,58 pp** |
| … hoặc: sửa artefact chọn lát nội sinh (Δ thật ≈ 3,5 pp thay vì 15,1 pp) | ≈ +1,3 pp |
| … rồi nhân với bộ phát hiện thực tế (AUROC 0,53 trong kho · 0,71 trong tài liệu) | ≈ +0,5…+1,3 pp |
| … rồi trừ 7 pp `action_ok` bị mất trên lát từ chối | **có thể ÂM** |

Ngưỡng Dương của `106` là **+2,8 pp**. Cơ chế này **không thể** với tới, dưới bất kỳ cách đọc nào
không dùng giả định lạc quan nhất ở mọi tầng.

**Vì vậy:**
- ⛔ **KHÔNG** dùng từ chối làm đóng góp mô hình chính. **KHÔNG** đặt cược ngân sách GPU vào nó.
- ✅ **Vẫn giữ `<sel>none</sel>`** cho bước không có ứng viên vàng (miễn phí, cần cho tính đúng đắn
  của nhãn), và báo **đường risk–coverage** như **kết quả mô tả thứ cấp** — đó là phần thật mới và
  rẻ: chưa ai vẽ đường risk–coverage cho **sinh biểu thức quy chiếu chấm bằng bộ trỏ độc lập**.
- ⛔ **Bỏ hẳn chữ "cơ chế mới"**: selective prediction có tuyến kinh điển (Chow, *IEEE TIT* 1970 →
  El-Yaniv & Wiener, *JMLR* 2010 → Geifman & El-Yaniv, *NeurIPS* 2017 — bài cuối làm đúng luật τ
  của file này) và đã có tiền lệ **ngay trong miền GUI grounding** trước 9/2026 (HyperClick,
  SafeGround — dán nhãn **preprint**).
- ⭐ **Điểm phân định thật và bảo vệ được:** hai bài GUI kia từ chối để **không click sai**; ở đây
  từ chối để **đổi cách nói với con người** — hàm mất mát bất đối xứng khác hẳn, và ta **đã đo được
  nó** (lợi/hại ⇒ precision hoà vốn **37,0%** so với tỉ lệ nền lát sai **33,5%** ⇒ bộ phát hiện
  ngẫu nhiên cho Δ âm). Chưa bài nào đo đại lượng này cho REG.
- ⭐ **Đóng góp chẩn đoán mới và có giá trị:** bảng lát + phát hiện *khai báo của mô hình dự đoán
  87,7% điểm của bộ trỏ* ⇒ **cảnh báo mọi bài sau đừng đọc lát nội sinh**. Đây là kết quả phương
  pháp luận, **không tốn GPU**.
- ⇒ **Đòn chính chuyển sang nâng `sel_acc`** (§2.7), và thiết kế để đo nó nằm ở §7.5.

**Vì sao vẫn giữ G0 nhưng KHÔNG còn là cổng (§7.0):** G0 đổi vai từ *"cổng quyết định có tin cơ
chế"* thành **phép đo cho đường risk–coverage**, chạy trên checkpoint đã có, **0 giờ train**,
⛔ không chặn hay mở quyết định train nào. Nếu AUROC < 0,70 thì chỉ báo như kết quả âm.

### 2.7 ⭐ ĐÒN CHÍNH THẬT SỰ: nâng `sel_acc`, không phải từ chối (ảnh 08)

Số học ở §0 (bản đã sửa độ dốc) cho **1 pp `sel_acc` = 0,456 pp exec**. Hiện `sel_acc` ≈ **66,5%**.
Đòn này vẫn **lớn hơn** từ chối, nhưng **không** lớn như bản cũ tưởng, và nó **có trần**:
`sel_acc = 100%` chỉ cho exec **75,3%**.

| nếu `sel_acc` lên | exec kỳ vọng (dốc thật 0,456) |
|---|---|
| 70% | 61,6% |
| 75% | 63,9% |
| **77,4%** | **65,0%** |
| 80% | 66,2% |
| 88,3% | 70,0% |

So sánh trực tiếp: từ chối bị chặn ở **+5,04 pp** trong giả định lạc quan nhất và chỉ **+0,58 pp**
với fallback có họ gần nhất (§2.6); nâng `sel_acc` lên 77,4% cho **+5,0 pp** (đạt 65%).

### ⛔⛔ TRẦN CỨNG THỨ HAI vừa phát hiện (vòng 5): ĐỘ PHỦ KHỐI ỨNG VIÊN (ảnh 08–09)

Con số **G2 = 91,2%** được đo trên **3.505 bước có tên vàng**, không phải 4.463. Quy về mẫu số thật:
`91,2% × 3.505/4.463 = 71,6%`. Khoảng **22% bước không có tên vàng** (`name_of` trả rỗng, bị loại
ở `build_candidates.py`) ⇒ trên những bước đó việc "chọn trong danh sách" là **VÔ NGHĨA**, cơ chế
không thể cứu.

Ước lượng phần **thật sự chuyển được** (bước có ứng viên vàng trong khối ∧ hiện đang chọn sai)
≈ **704 bước**. Cứu hết 704 bước đó cho exec ≈ **67,2%** (một chỗ từng viết 67,3% — cùng phép, làm
tròn; dùng **67,2%** khi lập kế hoạch).

| mục tiêu | số bước cần cứu | có sẵn ~704 bước chuyển được? |
|---|---|---|
| **65%** | 484 | ✅ cần đúng **69%** số bước chuyển được — **stretch nhưng khả thi** |
| **70%** | 973 | ⛔ **KHÔNG ĐỦ BƯỚC** — không tới được bằng cơ chế chọn |

⇒ **70% phải bỏ khỏi mọi mục tiêu.** Kỳ vọng thực tế nếu train hết được 50–70% phần chuyển được:
**63,7–65,1%**.

✅✅ **ĐÃ TRUY XONG (26/8)** — con số 71,6% là **SỐ ĐO**, không phải ước lượng, và **"vênh 80,2 vs
91,2" KHÔNG PHẢI VÊNH**. Nguồn: `harness/descriptor_build_stats_test.json` +
`harness/descriptor_build_stats.json` (hai tệp này **có sẵn trên clone**, không cần Drive) và định
nghĩa trong `harness/build_candidates.py:138–148`.

| tầng | test (n = 4.448) | train (n = 41.099) | trạng thái |
|---|---|---|---|
| có tên rõ (`ten_ro`) | 3.297 = 74,1% | 30.252 = 73,6% | ✅ đã đo |
| tên là ký hiệu (`ky_hieu`) | 208 = 4,7% | 1.809 = 4,4% | ✅ đã đo |
| `n_gold` = có tên vàng (`ten_ro + ky_hieu`) | **3.505 = 78,8%** | ~32.061 = 78,0% | ✅ đã đo |
| KHÔNG có tên (`khong_ten`) | **943 = 21,2%** | 9.038 = 22,0% | ✅ đã đo — chốt con số "~22%" |
| trùng tên (`co_trung_ten`) | 336 = 7,6% | 3.124 = 7,6% | ✅ đã đo — chọn theo tên còn nhập nhằng ở nhóm này |

**Vì sao 80,2% và 91,2% không mâu thuẫn** — chúng đo trên **hai cách dựng ứng viên khác nhau**,
không phải hai lần đo cùng một thứ:
- **80,2%** (`106` x14d) đo trên **OCR ∪ a11y THÔ**, *trước* khi qua logic đặt tên + lọc + cắt
  top-40 của `build_candidates.py`.
- **91,2%** (`121` / `106` x15) đo bằng **chính script sẽ dùng** (`--split test --max 40`). Đây là
  con số đúng để lập kế hoạch.

Và `build_candidates.py:140` cho biết mẫu số chính xác: `n_gold` chỉ đếm bước mà `gold.get("name")`
khác rỗng ⇒ cả G1 (96,7%) và G2 (91,2%) đều là **tỉ lệ CÓ ĐIỀU KIỆN** trên 3.505 bước có tên,
không phải trên 4.463. Vậy:

```
C3 = 91,2% × 3.505 = 3.197 bước · phủ vô điều kiện = 3.197/4.463 = 71,6% ✅
```

⇒ Trần độ phủ **67,2%** và kết luận **70% không tới được** đứng trên **số đo**, không phải suy đoán.
Đó là lý do **khối ứng viên trong đầu vào + cơ chế chọn tường minh** phải là trung tâm, còn từ chối
là lớp bảo vệ phía sau.

⚠️ **Nhưng đây là vấn đề cấu trúc của thiết kế hiện tại:** khối ứng viên có mặt ở **cả hai** nhánh,
nên phần đóng góp lớn nhất **không hiện ra trong `Δ_component`**. Cái hiện ra trong Δ chỉ là thẻ
`<sel>` + từ chối — đúng phần có hiệu ứng nhỏ. Hệ quả rất có thể xảy ra: **điểm tuyệt đối đẹp
nhưng Δ rơi vào Dương yếu / TRẮNG**, tức vẫn bị GVHD hỏi đúng câu cũ.
⇒ Xem **§7.5** cho phương án được khuyến nghị giải đúng chỗ này (`gui_orpo_hard`: tách đúng một
biến, đủ hai hạt giống trong ~40 h). ⚠️ *(§7.5 KHÔNG có trong ảnh — phải lấy file gốc.)*

> ⛔ **CÂU TRÊN ĐÃ CHẾT — vá 30/8, xem `report/126_TRA_LOI_MAC_30_8.md` mục 2.1.** Máy Mac đã mở
> file gốc: đây là **leftover** ở cuối §2.7 mà chính §7.5 vòng 5 đã bác. `gui_orpo_hard`
> **không tách** khối ứng viên ra khỏi đối chứng (hai nhánh ORPO **cùng có** khối), và toàn bộ
> công của ORPO-khó chồng SFT **đã đo rồi = +0,63 pp exec** — muốn chạm ngưỡng Dương +2,8 phải
> gấp **4,4 lần**. Quyết định thi hành: **`gui_sel` vs `gui_sft_match`, 1 epoch × 2 hạt, không
> ORPO.**

---

## 5. §3 — KIẾN TRÚC CHỐT: SEL + GEN (ảnh 10–13)

⚠️ **Đọc §7.5 trước mục này.** Vòng 5 đã bỏ phần từ chối (τ, hai lượt) khỏi kiến trúc;
`<sel>none</sel>` chỉ còn là **nhãn train** cho bước không có ứng viên vàng, không còn cơ chế suy
luận riêng.

### 3.0 Sơ đồ

```
ảnh screenshot + mục tiêu + 3 câu history (câu NGƯỜI, teacher-forced)
    ↓
khối ≤40 ứng viên (node trợ năng có tên, §5.1), thứ tự đọc:  tên <point>x,y</point> · …
        ├─ nhánh XỬ LÝ  (gui_sel):    <sel>một dòng chép nguyên</sel>  HOẶC  <sel>none</sel>
        │                              rồi câu tiếng Anh
        └─ nhánh ĐỐI CHỨNG (gui_sft_match):  chỉ câu tiếng Anh
    ↓
suy luận MỘT LƯỢT, greedy, cả hai nhánh   (⛔ không τ, không lượt 2)
    ↓
cắt bỏ thẻ <sel>…</sel> (như đang cắt <desc>) → chỉ còn CÂU
    ↓
log `conf` = logprob trung bình của nội dung <sel>  — CHỈ để vẽ risk–coverage hậu kiểm,
                                                      ⛔ không định tuyến
    ↓
UGround-V1-2B → điểm (x,y) → action/toggle + Voronoi → exec, n = 4.463
    ↓
Δ_component = exec(gui_sel) − exec(gui_sft_match)
```

**Hai việc mô hình học, đúng thứ tự (vòng 5):** chọn một dòng (hoặc `<sel>none</sel>` khi không có
ứng viên vàng) → nói câu vàng. **Chỉ một thứ khác nhau giữa hai nhánh: có đầu chọn tường minh hay
không.** Cùng backbone, cùng ảnh, cùng khối ứng viên, cùng câu đích, cùng cutoff, cùng LoRA, cùng
epoch, cùng hạt. `<sel>none</sel>` là **nhãn train**, không phải suy luận hai lượt.

### 3.1 Câu nhắc (input) — một hàm dùng cho cả dạy và chấm

`infer_branch.py` **import** hàm dựng câu nhắc từ `build_branch_data.py`. Phá điều này là hỏng phép
so (đã ghi ở đầu `infer_branch.py`).

**Không sửa `prompt_body` tại chỗ** — nhánh cũ (S1/S2/MIN) phải giữ nguyên phân phối để bảng lịch
sử còn đọc được. Mở rộng chữ ký:

```python
prompt_body(step, ocr, *, cands=None)
# cands is None  -> giữ nguyên 24 dòng OCR (nhánh cũ, KHÔNG ĐỔI)
# cands có       -> THAY khối OCR bằng khối ứng viên
```

Thân câu nhắc khi `cands` có (khoá cứng, cả hai nhánh cặp giống nhau từng ký tự):

```
Mục tiêu: {goal}
Đã làm: {3 câu history gần nhất, nối bằng →}     # bỏ dòng này nếu không có history
Ứng viên trên màn: {block_str(cands)}             # THAY cho dòng "Chữ đọc được"
Viết câu hướng dẫn cho bước tiếp theo.
```

- **Thay** khối OCR, **không chồng** OCR + ứng viên (trùng tên, nổ token).
- `block_str`: mỗi ứng viên là `tên <point>x,y</point>`, nối bằng ` · `, toạ độ lưới [0,1000] y hệt
  ô `desc` cũ, thứ tự **đọc** (y rồi x), cắt tối đa **40**.
- Ảnh: `"<image>\n" + body` lúc dạy; lúc chấm dùng list `[{type:image},{type:text}]` như hiện tại.
- `SYS` giữ nguyên như `build_branch_data.py`.
- `--selftest` 20 bước: khẳng định chuỗi user lúc dạy **byte-identical** với lúc chấm.

⛔ **Mọi thứ tự / cắt bớt phụ thuộc phần tử đích là rò rỉ.** Không nhãn `GOLD`, không sort theo
khoảng cách tới vàng. Cổng G3 kiểm bằng 300 mẫu mù.

### 3.2 Đích sinh — nhánh XỬ LÝ (`gui_sel`)

Ba trường hợp, khoá cứng:

| loại bước | đích |
|---|---|
| chạm, **có** ứng viên vàng trong khối (C3) | `<sel>Tên nguyên văn <point>x,y</point></sel>\n` + câu vàng |
| chạm, **không** có ứng viên vàng (tên không khớp, hoặc lệch > 140, hoặc bị cắt khỏi top-40, hoặc phần tử là icon không tên) | `<sel>none</sel>\n` + câu vàng |
| không-chạm (cuộn / gõ / mở app / back) | `<sel>none</sel>\n` + câu vàng |

⭐ **Đây là điểm khác quan trọng nhất so với `122`.** `122` để bước không-C3 sinh **chỉ câu** (không
thẻ). Bây giờ chúng dạy `<sel>none</sel>`. Vì sao: đó chính là **tín hiệu giám sát cho việc từ chối**,
tức cho cơ chế mang lại +5,1 pp lý thuyết. Không có nhãn `none` thì mô hình không bao giờ học được
im lặng, và nhánh xử lý chỉ còn là SEL+GEN của `122`.

**Không rò rỉ:** nhãn `none` suy từ vàng **lúc huấn luyện** (đó là định nghĩa của học có giám sát);
**lúc kiểm mô hình tự quyết**, không ai đưa vàng vào input.

**Nội dung `<sel>` phải là bản CHÉP NGUYÊN một dòng trong khối** — không viết lại tên, không bịa
`point`. Câu là **câu vàng nguyên bản** (không bồi vị trí, không ép tên — xem §2.1–2.3).

**Luật gán nhãn vàng cho `<sel>`.** ⚠️ `build_candidates.py:141–148` **không có** hàm gán nhãn vàng
— nó chỉ đo phủ bằng `any(...)`, không trả về *ứng viên nào* là vàng, và không có luật phá hoà. Vì
vậy hàm này phải được **viết mới** trong `build_sel_data.py`, và phải khoá nguyên văn ở đây để
G6/`sel_acc` dùng **cùng một luật**:

```python
def gold_candidate(cands, gold_name, gold_nx, gold_ny):
    """Trả về ứng viên vàng, hoặc None nếu không có (-> nhãn <sel>none</sel>)."""
    gn = gold_name.strip().lower()
    hits = [c for c in cands
            if c["name"].strip().lower() == gn
            and abs(c["nx"] - gold_nx) <= 140
            and abs(c["ny"] - gold_ny) <= 140]        # lưới 1000, hình chữ nhật
    if not hits:
        return None
    # phá hoà: gần gold nhất theo L2 (không phải theo thứ tự đọc)
    return min(hits, key=lambda c: (c["nx"] - gold_nx) ** 2 + (c["ny"] - gold_ny) ** 2)
```

So khớp tên là **khớp chuỗi chính xác sau `strip().lower()`** — không bỏ dấu câu, không bỏ khoảng
trắng giữa, không so gần đúng. Nếu muốn đổi (ví dụ chuẩn hoá khoảng trắng), phải quyết **trước khi
dựng dữ liệu** và ghi vào (x16), vì nó đổi cả tỉ lệ `none` lẫn `sel_acc`.

**Không xoá mẫu nào khỏi train.** Hai file train **cùng số dòng** (~64.567). Log và báo: % bước chạm
có `<sel>` thật, % có `<sel>none</sel>`.

### 3.3 Đích sinh — nhánh ĐỐI CHỨNG (`gui_sft_match`)

- **Cùng** khối ứng viên ở input, **cùng** câu vàng ở đích, **cùng** số dòng.
- Output **chỉ câu**, không thẻ nào.
- Cùng cutoff **3072**, cùng epoch, cùng LoRA, cùng hạt.

Nếu nhánh xử lý thắng nhánh này, thắng ở **đầu chọn tường minh** (nhãn `<sel>`). Nếu hoà, thì "khối
ứng viên trong đầu vào" đã làm hết việc ⇒ **không được viết là đóng góp mô hình**. Đó là mục đích
tồn tại của nhánh đối chứng; **đừng bỏ nó để tiết kiệm GPU**.

### 3.4 ⛔ ĐÃ BỎ (vòng 5) — Suy luận hai lượt + hiệu chỉnh ngưỡng τ

⛔⛔ **KHÔNG THI HÀNH MỤC NÀY.** Vòng 5 đã bỏ hẳn tầng τ và suy luận hai lượt cùng với việc hạ cấp
cơ chế từ chối (§2.6, §7.5b). Suy luận là **một lượt**, không có τ, không có `calibrate_tau.py`,
không có biến thể một-lượt phải báo song song. Giữ mục này **chỉ để tra cứu** nếu sau này quay lại.

*(Ảnh dừng tại đây — phần "Bản cũ (không thi hành)" và toàn bộ §4 trở đi không được chụp.)*

---

## 6. Những gì ảnh KHÔNG phủ — phải lấy từ file gốc

| mục | vì sao cần |
|---|---|
| ~~**§7.5**~~ ✅ | **ĐÃ LẤY 30/8** → `report/126` mục 1–2. ⛔ Không chứa `gui_orpo_hard` như đoán ở đây — §7.5 chính là chỗ **bác** phương án đó |
| **§7.2** | nguồn của con số ~704 bước chuyển được |
| **§5 / §5.1** | định nghĩa khối ứng viên; 4 thước đồng-báo |
| **§12** | mẫu (x16) phải dán vào `106` **trước khi** dựng dữ liệu |
| **§16** | bảng kiểm toán số + chỗ yếu tự khai |
| **§7 (G10, G3, G5b, G6)** | định nghĩa các cổng còn hiệu lực |
| **§4, §6, §8–§11, §13–§15** | chưa biết có gì |

---

## 7. Trạng thái kho WSL (kiểm 29/8/2026)

| thứ | trạng thái |
|---|---|
| `report/120`, `report/121` | ✅ có |
| `report/122`, `report/123`, `report/124` | ⛔ **chưa có** — nằm trên máy Mac |
| `harness/build_candidates.py` | ✅ có (commit `fb6ce1c`) |
| `harness/descriptor_build_stats.json` · `_test.json` | ✅ có |
| `harness/build_branch_data.py` · `infer_branch.py` | ✅ có |
| `harness/build_sel_data.py` | ⛔ chưa có — đúng như §3.2 nói "phải viết mới" |
| `harness/calibrate_tau.py` | ⛔ chưa có — **và không cần nữa** (§3.4 đã bỏ) |
