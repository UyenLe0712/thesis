# Yêu cầu gửi chat trên máy Mac — bổ sung phần thiếu của `123`

> Copy nguyên khối dưới đây gửi sang chat kia.

---

**Bối cảnh:** máy WSL đã nhận 13 ảnh chụp `123_CHOT_CUOI_PIPELINE.md` và chép lại thành
`report/123_CHOT_CUOI_PIPELINE_CHEP_TU_ANH.md`. Ảnh **chỉ phủ tới §3.4**. Kho WSL **không có**
`122`, `123`, `124` (bản gốc).

**Cách rẻ nhất — làm cái này trước, nếu được thì khỏi cần chụp ảnh:**

```bash
git add report/122*.md report/123*.md report/124*.md
git commit -m "report/122-123-124: đồng bộ từ máy Mac sang WSL"
git push
```

Nếu vì lý do nào đó không push được, thì **paste nguyên văn dưới dạng text** (đừng chụp ảnh — chữ
nhỏ dễ đọc nhầm số) các mục sau, theo thứ tự ưu tiên:

---

## Ưu tiên 1 — BẮT BUỘC (không có thì không đánh giá được pipeline)

| mục | vì sao cần |
|---|---|
| **§7.5** và **§7.5b** | Chính `123` §1 tuyên bố *"§7.5 — QUYẾT ĐỊNH CUỐI. Mục này thắng mọi mục khác nếu có xung đột."* Ảnh 03 và 08 đều trỏ tới §7.5 cho phương án `gui_orpo_hard` (*"tách đúng một biến, đủ hai hạt giống trong ~40 h"*) — **đây là chỗ giải quyết rủi ro Δ rơi vào TRẮNG**, mà không đọc được. |
| **§12** | Mẫu **(x16)** phải dán vào `106` **TRƯỚC khi dựng dữ liệu**. §3.2 cảnh báo luật khớp tên đổi thì đổi cả tỉ lệ `none` lẫn `sel_acc` ⇒ phải chốt trước. |
| **§16** | Bảng kiểm toán số + **chỗ yếu tự khai** + những gì đã sửa qua 5 vòng. |

## Ưu tiên 2 — cần để viết mã

| mục | vì sao cần |
|---|---|
| **§5 và §5.1** | §5.1 = định nghĩa **khối ứng viên** (node trợ năng có tên) — §3.0 trỏ thẳng vào. §5 còn có **4 thước đồng-báo**. |
| **§7.2** | Nguồn của con số **~704 bước chuyển được** — con số chặn mục tiêu 70%. |
| **§7**, phần định nghĩa cổng | **G3** (300 mẫu mù, chống rò rỉ) · **G5b** (đo h/epoch, quyết hy sinh backbone hay không) · **G6** (`sel_acc`) · **G10** (thay cho ý ép tên đã chết ở §2.3). |

## Ưu tiên 3 — chưa biết có gì

**§4 · §6 · §8 · §9 · §10 · §11 · §13 · §14 · §15** — ảnh nhảy từ §3.4 sang trống. Chụp/paste
**mục lục** là đủ để biết có cần hay không.

---

## Kiểm chéo đã làm ở WSL (để chat kia khỏi làm lại)

Đã verify **từ mã và JSON thật**, khớp 100% với ảnh:

- `harness/descriptor_build_stats_test.json`: n=4.448 · `ten_ro` 3.297 · `ky_hieu` 208 ·
  `khong_ten` 943 · `co_trung_ten` 336 ⇒ `n_gold` = 3.505 ✅
- `harness/descriptor_build_stats.json`: n=41.099 · `ten_ro` 30.252 · `ky_hieu` 1.809 ·
  `khong_ten` 9.038 · `co_trung_ten` 3.124 ✅
- `build_candidates.py:138–148` — đúng là **chỉ đo phủ bằng `any(...)`**, không trả về ứng viên
  vàng nào, không có luật phá hoà ⇒ khẳng định của §3.2 *"phải viết mới `gold_candidate()` trong
  `build_sel_data.py`"* là **đúng**. C3 dùng ±140 hình chữ nhật trên lưới 1000. ✅
- `build_branch_data.py:39` — chữ ký hiện tại `prompt_body(r, ocr_rec)`. Mở rộng thành
  `prompt_body(r, ocr_rec, *, cands=None)` **tương thích ngược hoàn toàn**; ba chỗ gọi trong
  `infer_branch.py` (dòng 239, 316, 476) đều truyền 2 tham số nên không vỡ. ✅

**Chưa có trên WSL:** `harness/build_sel_data.py` (đúng như §3.2 nói phải viết mới) ·
`harness/calibrate_tau.py` (§3.4 đã bỏ nên **không cần nữa**).

---

## Một câu hỏi nhờ chat kia trả lời luôn

§2.7 (ảnh 08) tự khai: *"khối ứng viên có mặt ở **cả hai** nhánh, nên phần đóng góp lớn nhất
**không hiện ra trong `Δ_component`** … điểm tuyệt đối đẹp nhưng Δ rơi vào Dương yếu / TRẮNG"*.

Đây **đúng y kết cục của MIN-DESC** (60,05% cao nhất mọi nhánh, nhưng Δ so S1/101 chỉ +0,94 pp,
p=0,11 ⇒ ô TRẮNG). Câu hỏi: **§7.5 / `gui_orpo_hard` giải quyết chuyện này bằng cách nào?** Cụ thể
là tách biến nào ra khỏi nhánh đối chứng để Δ bắt được phần đóng góp của khối ứng viên?

---

## Cập nhật 29/8 — cái gì đang chặn, cái gì KHÔNG

Rà lại sau khi lên kế hoạch tháng 9. Bên WSL **không ngồi chờ** — phần dưới đây chạy được ngay
mà không cần file gốc, chat kia khỏi lo phải trả lời gấp mọi mục:

| việc tuần 1 | có chặn không | lấy định nghĩa ở đâu |
|---|---|---|
| Cổng **G1 · G2 · G3 · G4** | ❌ không chặn | `report/121` §6 đã khoá đủ ngưỡng + luật trượt |
| `harness/build_sel_data.py` | ❌ không chặn | `123` §3.2 (ảnh có phủ) đã chép nguyên văn `gold_candidate` |
| `prompt_body(..., cands=None)` + `--selftest` | ❌ không chặn | `123` §3.1 |
| Gỡ mìn `descriptor_label_build.py --split test` | ❌ không chặn | chuyện riêng của kho WSL |
| Verify model card Qwen3-VL-4B | ❌ không chặn | tra ngoài |
| Cảnh báo lát nội sinh · risk–coverage · luận văn | ❌ không chặn | số đã nằm sẵn trên kho |
| **Bấm train (72–88 h A100)** | ⛔ **CHẶN** | cần **§7.5** để biết train cặp nhánh nào |

⇒ Thứ duy nhất thật sự chặn là **§7.5**, và nó chặn ở **cuối tuần 1**, không phải hôm nay.
Ưu tiên 1 trong bảng trên vẫn giữ nguyên, chỉ là biết rõ hạn thực tế.

---

## Ba câu hỏi nữa, nhờ trả lời luôn khi mở file

**(2) §7.5 có lịch trình và điểm quyết định riêng không, hay vẫn dùng `121` §7?**
`121` §7 có lịch 9 tuần + cổng **G1–G7** + ba điểm quyết định **D1/D2/D3**. Nhưng vòng 5 của `123`
đã **bỏ G7** (dải lùi) và hạ cơ chế từ chối ⇒ **D1 không còn đối tượng để quyết**, và bảng ngân
sách của `121` (~140 h cho kịch bản đầy đủ) khác hẳn con số **72–88 h** ở §0 của `123`.
Nếu §7.5 có bảng lịch + ngân sách riêng thì paste **cả bảng**, đừng tóm tắt.

**(3) `123` có mục nào xếp thứ tự việc tháng 9 KHÔNG tốn GPU không?**
Cụ thể ba thứ đứng độc lập kể cả khi train ra ô TRẮNG: đường **risk–coverage** (§2.6 nói báo như
kết quả mô tả thứ cấp) · **cảnh báo lát nội sinh** (độ thổi −11,50 pp, KTC95 [−13,37 · −9,40]) ·
cập nhật **luận văn**. `123` có ấn định thứ tự / mức ưu tiên cho chúng không, hay để tự quyết?

**(4) Con số chi phí backbone ở §0 là ĐO hay ƯỚC LƯỢNG?**
Ảnh 03 ghi *"16–20 h/epoch lạc quan · 26–35 h/epoch bi quan, đo bằng G5b"* và luật
*"G5b > 27 h/epoch thì hy sinh backbone, ⛔ không hy sinh hạt"*. Nhưng G5b là phép đo **sẽ chạy**,
nên hai dải kia hẳn là ước lượng thiết kế. Xin xác nhận: **đã có lượt đo thật nào trên Qwen3-VL-4B
chưa**, hay ngưỡng 27 h/epoch được đặt thuần bằng lập luận ngân sách?
