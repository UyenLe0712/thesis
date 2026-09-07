# 139 — Phản biện luật D.3 (`report/140_NANG_TRAN_LUAT_D3.md`), đo lại từ tệp thô 5/9/2026

> Vai: giám khảo khó tính. Mọi số dưới đây tính lại từ `*_raw.jsonl` + `descriptors.jsonl`
> (trường `box`), 0 giây GPU. Tái lập trùng khít tám con số D.3 của `140` (83,82 · 66,55 ·
> 65,49 · 53,60 · 62,38).
> ⚠️ Tệp luật D.3 từng mang số `140` (trùng với `138_RESEARCH_NANG_SO_5_9.md`); đã đổi thành **`140`** ngày 5/9.

## Nghi ngờ (1) — hộp do nhóm tự suy, không phải nhãn gốc

**Đúng, và hệ quả phải khai rõ hơn `140` đã khai.** Luật `min(cont, key=diện tích)` trong
`descriptor_label_build.py:334` lấy **nút nhỏ nhất** chứa điểm chạm. Phân bố `role_class` của
4.448 hộp: TextView **1.357** · ImageView **775** · Button 719 · View 323 · ImageButton 224 ·
FrameLayout 216 · ViewGroup 177 · LinearLayout 174. Tức **~48% hộp là nút con không nhận
chạm** (TextView/ImageView) nằm trong một nút cha có thể nhận chạm. AndroidControl khi chấm
dùng *phần tử đích* — hầu chắc là nút nhận chạm — nên hộp của họ **rộng hơn** hộp của ta ở
nhóm này.

Hướng của sai lệch: hộp ta **chặt hơn** ở ~48% bước ⇒ 83,82 là **ước lượng thấp** so với
luật D.3 áp đúng nhãn gốc, không phải ước lượng cao. Đó là hướng an toàn cho một mốc trần.
Nhưng lập luận *"luật này không do nhóm chọn"* chỉ đúng **một nửa**: luật khớp là của họ,
**đối tượng được khớp là của ta**. Câu phải viết: *áp luật khớp của Phụ lục D.3 lên hộp
phần tử dựng từ cây trợ năng theo quy tắc nút nhỏ nhất chứa điểm chạm; quy tắc này chặt hơn
phần tử đích thật ở các nút con không nhận chạm.* `140` §1.4① đã có câu này, nhưng thiếu con
số 48% và thiếu chiều của sai lệch.

## Nghi ngờ (2) — 11,98% hộp rộng ≥90% màn: có phải thưởng ca dễ?

**Phần lớn là hàng danh sách hợp lệ; một túi nhỏ là container, và túi đó cho điểm gần như
miễn phí.** 533 bước hộp ≥90% bề ngang:

| | p10 | p50 | p90 | max |
|---|---|---|---|---|
| chiều cao hộp, % màn | 3,7 | **6,1** | **88,3** | 100 |
| diện tích hộp, % màn | — | 5,6 | 87,0 | — |

Trung vị là hàng cao 6% màn — đúng nghĩa vật lý của D.3. Nhưng p90 là 88% chiều cao: **112
bước có hộp ≥25% diện tích màn, 83 bước ≥50%**, `role_class` là FrameLayout/View/LinearLayout
/ViewGroup — điểm chạm rơi vào chỗ trống của một container và không có nút con nào chứa nó.
Trên **120 bước hộp ≥25% diện tích** (2,69% mẫu số):

| | Voronoi | D.3 |
|---|---|---|
| người | 37,5 | 85,0 |
| MIN | 23,3 | 78,3 |
| S1 | 24,2 | 75,0 |
| **Base** | 20,0 | **79,2** |

Dưới D.3, **Base ngang MIN ngang người** ở túi này ⇒ đây là điểm miễn phí đúng nghĩa. May là túi
nhỏ: loại nó khỏi mẫu số, D.3 của người **84,08**, MIN 66,45 — gần như không đổi.

Phân rã mức tăng (D.3 trúng ∧ Voronoi trượt) theo bề ngang hộp, đơn vị pp trên 4.463:

| nhánh | <25% | 25–50% | 50–90% | ≥90% | tổng tăng | tổng mất |
|---|---|---|---|---|---|---|
| người | 0,49 | 1,55 | **4,28** | **3,02** | +9,34 | −1,25 |
| MIN | 0,29 | 1,30 | 3,18 | 2,67 | +7,44 | −0,94 |
| Base | 0,22 | 1,12 | 2,55 | 2,80 | +6,70 | −0,69 |

⇒ **78% mức tăng đến từ hộp rộng hơn nửa màn.** Ở hộp nhỏ (<25%, chiếm 52% số bước) D.3 gần
như không thêm gì và còn **lấy đi** 1,25 pp của người (chặt hơn theo chiều dọc). Vậy câu đúng là:
*D.3 chặt hơn Voronoi ở phần tử nhỏ và lỏng hơn nhiều ở phần tử rộng; toàn bộ phần "trần cao
hơn" nằm ở phần tử rộng.* Người đọc phải được nói điều đó trước khi thấy 83,82.

Trong 417 bước người được cứu: |dx| trung vị **12,4% W**, p90 37,4% — tức bộ trỏ lệch ngang
cả phần tư màn mà vẫn trong hàng; |dy| trung vị 0,3%. 205/417 trượt cửa sổ 14%, 212/417 chỉ
trượt riêng Voronoi (điểm trỏ gần một "nút" khác — thường là một mảnh OCR cùng hàng). Hai nửa
này khác bản chất: nửa Voronoi là chỗ **Voronoi quá chặt** (mảnh chữ cùng hàng không phải nút
riêng); nửa 14% là chỗ **D.3 lỏng thật**.

**Phản chứng cho lo ngại "luật này pha loãng tính phân biệt":** phép bỏ-tên-giữ-vị-trí `f2`
trên 193 bước bị tác động — Voronoi: 89,6 → 61,1 (**−28,5**); D.3: 93,3 → 59,1 (**−34,2**).
D.3 phạt việc bỏ tên **nặng hơn**, không nhẹ hơn. Chữ *Element Identification* ở nhan đề không
bị luật này làm yếu đi.

## Nghi ngờ (3) — chọn sau khi thấy mọi điểm

**Trình đồng-báo là chưa đủ nếu 83,82 đứng ở chỗ nổi bật.** Ba lý do:

1. `rule_sensitivity.py` đã có luật *hộp-gần-nhất* cho trần **82,2** từ 16/8. D.3 không mang
   thông tin mới về **thứ tự nhánh**; nó chỉ mang một con số tuyệt đối đẹp hơn. Thứ tự đã bền
   qua năm luật, thêm luật thứ sáu không làm lá chắn dày hơn bao nhiêu.
2. Con số duy nhất luận văn cần bảo vệ là **MIN − S1**: Voronoi +0,94 · D.3 +1,06 · D.3 gated
   +0,96 · D.3 loại container +0,96. **Không đổi.** D.3 không mua thêm bằng chứng nào cho
   đóng góp mô hình; nó chỉ đổi cách nhìn mốc trần.
3. Mức tuyệt đối cực nhạy với cách xử hộp rộng (`140` §1.4③), nên một con số đứng một mình là
   con số dễ bị bẻ nhất.

Bảng độ nhạy của `140` xử hộp rộng bằng cách **tính trượt** thay vì **loại khỏi mẫu số** — vì
thế trần rơi 83,82 → 55,97, trông như luật sập. Loại khỏi mẫu số thì trần **84,08**. Nên đưa cả
hai cách đọc, hoặc chỉ đưa cách loại.

Biến thể chặt hơn, để có sẵn khi bị hỏi (n = 4.463):

| luật | người | MIN | S1 | Base | sel | MIN−S1 | S1−Base |
|---|---|---|---|---|---|---|---|
| Voronoi .14 (headline) | 75,73 | 60,05 | 59,11 | 47,59 | 56,13 | +0,94 | +11,52 |
| D.3 thuần | 83,82 | 66,55 | 65,49 | 53,60 | 62,38 | +1,06 | +11,89 |
| **D.3 ∧ cửa sổ 14%** | **79,23** | 62,69 | 61,73 | 49,76 | 58,62 | +0,96 | +11,97 |
| D.3, hộp ≥25% màn tính trượt | 81,54 | 64,44 | 63,48 | 51,47 | 60,45 | +0,96 | +12,01 |
| D.3 ∧ 14%, hộp ≥25% tính trượt | 78,04 | 61,82 | 60,88 | 49,00 | 57,94 | +0,94 | +11,88 |

## Phán quyết

**Không bỏ.** Nhưng cũng không dùng theo cách `140` §5 đề nghị (đưa hàng D.3 vào bảng chính).

- D.3 vào **bảng độ nhạy luật chấm**, cạnh năm luật đã có, với cột nguồn *"Phụ lục D.3,
  AndroidControl"* và cột *"tính 5/9, sau khi có điểm"*. Không vào bảng chính, không vào tóm tắt.
- Khai ba điều bằng số: 48% hộp là nút con không nhận chạm (chặt hơn nhãn gốc) · 78% mức tăng
  từ hộp rộng hơn nửa màn · 120 bước container cho điểm miễn phí, loại ra thì trần 84,08.
- Nếu muốn một con số D.3 để nói trong bảo vệ, dùng **D.3 ∧ cửa sổ 14% = 79,23** — giữ được
  luận cứ "luật gốc" ở phần hộp, giữ cửa sổ đã niêm ở phần dung sai, và không có túi miễn phí.
- Cái được thật từ lượt này là hai phát hiện phụ: (a) `f2` dưới D.3 phạt bỏ-tên **−34,2**,
  mạnh hơn Voronoi; (b) một nửa số bước Voronoi trượt-mà-D.3-trúng là do mảnh OCR cùng hàng bị
  coi là nút riêng — tức **Voronoi có một lỗi hệ thống ở hàng danh sách**, đáng một đoạn ở
  mục hạn chế của thước.

Việc **không** làm: đổi headline sang D.3; trình 83,82 như "trần mới"; bỏ cách trình theo tỉ
lệ mà không thay bằng nếp Zhao et al. (`140` §2 đúng ở điểm này).
