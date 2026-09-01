# 125 — TUẦN 1 THÁNG 9: mã và cổng đã chạy (29/8/2026)

> Việc của tuần 1 theo `report/123` §3 — **phần không cần §7.5**, tức không cần file gốc
> trên máy Mac. Mọi thứ dưới đây chạy trên WSL, **0 giờ GPU, 0 đồng**.
> Cái gì còn chờ §7.5: xem mục 6.

---

## 1. ⛔→✅ ĐÃ GỠ MÌN: `test_ac/descriptors.jsonl` không còn tiếng Việt

Mìn ghi ở `CLAUDE.md` mục *"Việc kế"* số 5: tệp khai báo của **tập kiểm** dựng ngày 9/8, tức
**trước** mục sửa đổi (q) ngày 14/8 đổi nhãn sang tiếng Anh. `infer_branch.py:480` nhét thẳng
tệp này vào câu nhắc cho `--ceiling gold|filler` ⇒ hai nhánh đó sẽ chạy trên nhãn tiếng Việt
trong khi mô hình được dạy bằng nhãn tiếng Anh, **không có ô 7b nào canh**.

Đã chạy `descriptor_label_build.py --split test`, giữ bản cũ ở
`test_ac/descriptors_VI_0809.bak.jsonl`.

⭐ **Phép kiểm quan trọng hơn việc dựng lại: dựng lại có làm đổi số nào đã công bố không?**
So từng bước giữa bản cũ và bản mới trên **4.448 bước**, cùng tập khoá:

| trường | số bước lệch |
|---|---|
| `name` · `point_norm` · `tier` · `name_src` · `box` · `dup_name` · `same_role` | **0** |
| `role` · `hint` (đổi ngôn ngữ — đây là thay đổi MONG ĐỢI của mục (q)) | 4.448 |

⇒ Mọi con số đã báo dựa trên tệp này **giữ nguyên**: tầng `ten_ro` 3.297 (74,1%) · `ky_hieu` 208
(4,7%) · `khong_ten` 943 (21,2%) · `co_trung_ten` 336 (7,6%) · `n_gold` 3.505 (78,8%). Không phải
sửa một số nào trong hai bài báo hay luận văn.

---

## 2. ✅ CỔNG G1 · G2 — chạy lại trên tập kiểm, tái lập đúng số của `123`

`build_candidates.py --split test --max 40`, sau khi đã gỡ mìn:

| cổng | đo được | ngưỡng | |
|---|---|---|---|
| **G1** phủ — tên vàng có trong khối | **3.390/3.505 = 96,7%** | ≥95% | ✅ ĐẠT |
| **G2** C3 — khớp tên ∧ trong ±140 | **3.198/3.505 = 91,2%** | ≥75% | ✅ ĐẠT |

· Khối: trung vị **23** ứng viên/màn · p90 40 · **1.185/4.463 màn chạm trần 40** · 40 màn không
  có ứng viên nào.
· Độ dài khối: trung vị **912** ký tự · p90 1.574 · max 2.493.
· Phủ **vô điều kiện** = 3.198/4.463 = **71,66%**, khớp con số 71,6% của `123` §2.7. (`123` viết
  3.197 do nhân ngược từ 91,2% đã làm tròn; số đếm thật là **3.198** — chênh 1 bước, không đổi
  kết luận nào.)

---

## 3. ✅ `harness/build_sel_data.py` — đã viết, đã chạy thật

Dựng hai nhánh của `123` §3.2–3.3: `gui_sel` (đích = thẻ `<sel>` + câu vàng) và
`gui_sft_match` (đích = chỉ câu vàng), **cùng câu nhắc từng byte**.

Luật khoá được chép nguyên từ `123` §3.2, không diễn giải lại: khớp tên chính xác sau
`strip().lower()` ∧ lệch ≤ **140** trên lưới 1000 ở cả hai trục, phá hoà **theo L2** chứ không
theo thứ tự đọc — lấy thứ tự đọc làm luật phá hoà chính là để thứ tự khối rò ra đáp án.
Nội dung `<sel>` đúc bằng **chính `block_str`** của `build_candidates`, nên không thể lệch định
dạng với khối nằm trong câu nhắc.

### Bảy bất biến — trượt một cái là dừng, không ghi tệp

① hai nhánh cùng số dòng, bằng số bản ghi nguồn · ② câu nhắc + ảnh trùng nhau **từng byte** ·
③ đối chứng không chứa thẻ `<sel>` nào · ④ đích SEL = thẻ + `\n` + **đúng** câu của đối chứng ·
⑤ nội dung `<sel>` có **nguyên văn** trong khối ứng viên của chính mẫu đó (chống bịa tên/toạ độ) ·
⑥ mọi bước không-chạm mang `<sel>none</sel>` · ⑦ **không tạo thêm** mẫu rỗng.

⚠️ **Bất biến ⑦ phải đổi cách phát biểu sau khi chạy thật.** Bản đầu viết *"đích không bao giờ
rỗng"* và **trượt ngay**: nguồn có sẵn bước mà `target_instruction` rỗng. Đếm lại:

| tệp | mẫu đích rỗng |
|---|---|
| lát 1.697 bước trên WSL | 1 |
| **`branches/s1.json` — bản đã dùng để TRAIN** | **122 = 0,19%** |
| `branches/s2.json` | 107 (không mẫu nào có `<desc>`) |

`123` §3.2 cấm xoá mẫu khỏi tập dạy, nên cái đáng canh là *không tạo thêm*, không phải *không
có*. Ghi lại đây vì đây là lần đầu con số 122 được đếm — nó **không** đụng số nào trong hai bài
(toàn bộ nằm ở tập dạy), nhưng nếu sau này ai đó đọc thấy mẫu rỗng trong dữ liệu thì đã có chỗ tra.

### Kết quả chạy trên lát 1.697 bước có sẵn ở WSL

| | |
|---|---|
| `<sel>` thật | **750 = 69,8% bước chạm** |
| `none` · bước không chạm | 622 |
| `none` · vàng không có tên | 252 |
| `none` · vàng không khớp ứng viên nào | 73 |

⚠️ Đây là **lát thử**, không phải số của tập dạy thật — xem mục 5.

---

## 4. ✅ CỔNG G3 · G4 — chạy ngay trong `build_sel_data.py`

**G3 rò rỉ.** Ba phép, chạy tự động:
· vị trí **tương đối** của ứng viên vàng trong khối: p25 **0,15** · trung vị **0,46** · p75 **0,80**;
  nằm trong 10% đầu khối **15,2%** ⇒ **không dồn đầu**, thứ tự khối không nói đáp án ở đâu.
· khối sắp đúng **thứ tự đọc** (y rồi x), kiểm 2.000 màn: **0 lệch**.
· số bước có tên vàng mà **không** có ứng viên khớp: **73** — con số này **phải > 0**; bằng 0 nghĩa
  là khối đang được dựng theo đáp án.
· xuất **300 mẫu ngẫu nhiên** (hạt giống 20260805) ra `branches/g3_mau300_doc_mu.txt` để **đọc mù**
  — phần người phải làm, script không thay được.

**G4 độ dài.** 200 mẫu dài nhất: trung vị **871** token · max **1.122**, cutoff 3.072 ⇒ **0/200
vượt**. ⚠️ Chưa kể **token ảnh**; số đó phụ thuộc cỡ ảnh của bộ xử lý và **phải đo bằng chính
processor sẽ train** — cutoff 2560 của lượt S1/S2 không tự chuyển sang đây.

---

## 5. ⛔ CHẶN KỸ THUẬT MỚI PHÁT HIỆN: máy WSL **không có** tập dạy đầy đủ

Đây là thứ chưa file nào ghi, và nó chặn việc dựng dữ liệu thật:

| tệp | trên WSL | cần |
|---|---|---|
| `train_ac/train.jsonl` | **1.697** bước | 64.567 |
| `train_ac/ocr.jsonl` | **1.697** màn | 64.567 |
| `train_ac/descriptors.jsonl` | ✅ 41.099 | 41.099 |
| `train_ac/branches/s1.json` … | ✅ 64.567 mẫu | — |
| `test_ac/*` | ✅ đủ | — |

`_bundles/derived_train_en.tar.gz` **không cứu được** — nó chỉ chứa `descriptors.jsonl` và thư mục
`branches/`, không có `train.jsonl` lẫn `ocr.jsonl`.

Và **không dựng ngược được từ `s1.json`**: `s1.json` chỉ giữ chuỗi OCR đã nối, trong khi
`candidates_of()` cần **hộp** của từng mục OCR để `name_of()` gán tên. Mất hộp là mất tên ứng viên.

⇒ **Việc phải làm:** kéo `train_ac/train.jsonl` và `train_ac/ocr.jsonl` bản đầy đủ từ Drive
(`derived.tar.gz`) về, ~80 MB. Sau đó toàn bộ chuỗi chạy local, **0 GPU**:
`build_candidates.py --split train` → `build_sel_data.py --split train`.
Phương án hai — chạy cả hai lệnh trên Colab CPU sau khi bung `derived.tar.gz` — cũng được nhưng
phải tải cây trợ năng về máy ảo, và mỗi lần mất máy là làm lại.

### ⚠️ Kèm một phát hiện phải nhớ khi dựng bản đầy đủ

So câu nhắc dựng lại hôm nay với **chính câu nhắc trong `s1.json` đã dùng để train**, trên 1.697
bước: **26 bước lệch (1,5%)**. Đã kiểm bằng bản mã ở `git HEAD` (chưa vá) ⇒ **không phải do bản vá
hôm nay**. Chỗ lệch nằm trong **chuỗi OCR**: `Culture & museums` vs `Culture &museums`,
`Amstel` vs `Amtel` ⇒ lát 1.697 trên WSL được OCR bằng **một lượt khác** với lượt đã dựng dữ liệu
dạy thật.

⇒ **Luật: dựng dữ liệu SEL từ đúng bộ `ocr.jsonl` đã dựng S1/S2**, không phải từ lát thử này.
Tên ứng viên đi qua `name_of()` mà `name_of()` đọc OCR ⇒ đổi lượt OCR là đổi tên ứng viên, mà
`<sel>` là bản chép nguyên tên ⇒ đổi cả nhãn `sel` lẫn `sel_acc`. Loại hỏng này **không có tiếng
động**: không lỗi, không cảnh báo, chỉ ra số khác.

---

## 6. Còn chờ gì

| chờ | chặn cái gì |
|---|---|
| `train.jsonl` + `ocr.jsonl` đầy đủ (Drive) | dựng dữ liệu SEL thật · G1/G2 trên tập dạy · G4 trên đúng 200 mẫu dài nhất thật |
| ~~**§7.5** của `123`~~ ✅ **ĐÃ CÓ 30/8** | quyết rồi: **`gui_sel` vs `gui_sft_match`, 1 epoch × 2 hạt, KHÔNG ORPO** → `report/126_TRA_LOI_MAC_30_8.md` |
| ~~**§12** của `123`~~ ✅ **ĐÃ CÓ 30/8** | nội dung khoá của mẫu (x16) ở `report/126` mục 8 — nhưng **chỉ dán sau khi có số G1/G2 TRAIN**, không dán khống |
| đọc mù 300 mẫu G3 | phần người, tệp đã xuất sẵn |
| sửa `infer_branch.py` nhận `cands` | chỉ cần khi chạy suy luận — sau khi có checkpoint |

⚠️ **Cập nhật 30/8:** backbone theo bản Mac là **Qwen3-VL-4B-Instruct**, không phải Qwen2.5-VL-3B
⇒ **G4 ở mục 4 phải đo lại bằng tokenizer/processor của Qwen3-VL**, kể cả token ảnh; cutoff mới là
**3072**. Xem `report/126` mục 13 hàng #6, và mục 12.2 (chỗ tôi không đồng ý với việc đổi backbone).

⛔ **Chưa đụng tới:** `infer_branch.py` (đường suy luận cho nhánh SEL) và `sel_acc` lúc chấm — cả
hai phải dùng **đúng** `gold_candidate()` trong `build_sel_data.py`, đừng viết bản thứ hai.
