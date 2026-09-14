# 151 — BẢN THI HÀNH: việc cần làm để nâng số + thước để báo — 8/9/2026

> ⚠️ **BẢN CHÉP LẠI TỪ 31 ẢNH CHỤP MÀN HÌNH** (nhận 9/9/2026, ảnh gốc ở
> `report/anh_chot_phuongphap_metric_9_9/p01.jpg` … `p31.jpg`). Bản `.md` gốc nằm trên máy khác.
> Phần văn xuôi, bảng và con số đã chép đầy đủ. **Các khối mã chép lại từ ảnh nên PHẢI đối chiếu
> đúng ảnh được trỏ ở từng khối trước khi chạy** — một ký tự sai trong mã là một lượt chạy hỏng.
> Nếu về sau lấy được bản `.md` gốc thì thay đè tệp này.

File này là bản DUY NHẤT và là toàn bộ ngữ cảnh cần ngoài kho. Bản trước dài 3.580 dòng vì nó
chứa cả biên bản phản biện và sổ ghi lỗi của chính nó. Bản này **chỉ giữ việc cần làm**; mọi con
số sai đã được áp thẳng vào thân bài — không còn mục *"đọc 0a thay vì thân bài"* nào. Bảng đối
chiếu số cũ ⇄ số đúng ở **Phụ lục E**.

**Ngân sách:** 50 h A100 (Colab, ghi ra Drive 15 GB) · T4 miễn phí (Kaggle, 30 h/tuần).

✅ **Tái lập được:** mọi con số trong file dựng lại bằng bốn script ở Phụ lục A–D, chạy trên
`runs/*.jsonl` đã commit. 0 giây GPU. ⚠️ **Ngoại lệ duy nhất:** số D.3 cần
`harness/dg1_cache/test_ac/descriptors.jsonl`, tệp này chưa có trên kho — công thức dựng lại ở
mục 6.2, và bước 0 của nó là bắt buộc.

⛔ **TRẠNG THÁI KHO:** không một file nào trong `harness/` được sửa. Mọi dòng trong file này là
**việc phải làm**, không phải việc đã xong. Đừng giả định gì đã được áp.

⚠️ **Hai quy ước số:** MDE = **2,11 pp** (chỗ nào ghi 2,2 là bản làm tròn cũ của **cùng đại
lượng**, không phải ngưỡng thứ hai). **Δ(MIN − S1) = +0,95** (60,265646 − 59,320126 = 0,9455).

---

## 1. CHECKLIST THI HÀNH — theo thứ tự, đừng đảo

### 1.1 PHASE 0 — điều kiện chặn cứng, 0 giờ GPU

⛔ Không chạm A100 trước khi xong hết Phase 0. Chạy trước là một phát bắn mù — đúng cái đã làm
hai lượt trước ra số âm (S2 −1,93 · `gui_sel` −2,98).

| # | việc | ⛔ chi tiết dễ làm sai |
|---|---|---|
| **P1** | Thêm một dòng vào `.gitignore`: `!harness/dg1_cache/test_ac/descriptors.jsonl` | ⛔⛔ **BẮT BUỘC LÀM TRƯỚC P3.** `.gitignore:111` loại cả `harness/dg1_cache/`; dòng 113–114 chỉ mở lại `test_ac/` và `test.jsonl`. Không có dòng này thì `git add` bỏ qua im lặng ⇒ làm xong P2–P3 mà D.3 vẫn không tái lập được ở remote |
| **P2** | Dựng lại cache KIỂM — **hai lệnh**, không phải một:<br>`python harness/build_test_data.py`<br>`python harness/prep_ocr_train.py --split test` | ⛔⛔ **LỆNH THỨ HAI DỄ BỊ BỎ SÓT.** `build_test_data.py` chỉ ghi `test.jsonl` (dòng 185) và `images/*.png` (dòng 167) — nó **KHÔNG** sinh `ocr.jsonl`, dù bên trong có chạy OCR. Mà `descriptor_label_build.py:298` đọc `ocr.jsonl` ⇒ thiếu lệnh hai là P3 chết. ⭐ Kiểm đúng byte — chỉ tin MỘT trong hai: `runs/sel/manifest_selA_selB_4_9.json` (đã commit) lưu sha256 của `test.jsonl` (6.958 dòng) — ✅ dùng cái này.<br>⛔ ĐỪNG hoảng nếu `ocr.jsonl` ra 6.958 chứ không phải 6.969 như manifest ghi. Đã truy: `prep_ocr_train.py` ghi một dòng mỗi BẢN GHI của `test.jsonl` (dòng 64 và 72–84), nên dựng lại sạch tất yếu ra đúng 6.958. Con số 6.969 trong manifest (và trong docstring của chính script) là di tích từ một phiên bản `test.jsonl` cũ hơn — sha256 của `ocr.jsonl` vì thế sẽ không khớp, và đó **không** phải lỗi của bạn |
| **P3** | `descriptor_label_build.py --split test` → sửa `luat_d3.py` → `luat_d3.py` → commit `descriptors.jsonl` và `runs/luat_d3.json` | sinh `descriptors.jsonl` (4.448 dòng). ⛔⛔ `luat_d3.py` **KHÔNG có GRPO** — danh sách `NHANH` (dòng 23–31) chỉ có 8 nhánh, và `runs/luat_d3.json` hiện tại cũng vậy. Phải thêm một dòng vào `NHANH`: `("GRPO-point/101", "grpo_point/score_grpo_point_seed101_raw.jsonl")`. Không thêm thì chạy bao nhiêu lần cũng **không** ra hàng GRPO, tức không ra **67,04** |
| **P3bis** | Dựng lại cache DẠY — hai lệnh, và ⛔ **ĐỪNG QUÊN `--shards 76`**:<br>`python harness/build_train_data.py --shards 76`<br>`python harness/prep_ocr_train.py --split train` | ⛔⛔ `harness/dg1_cache/train_ac/` KHÔNG TỒN TẠI trên đĩa (máy soạn file) — `dg1_cache/` chỉ còn `test_ac/`. Mà val lấy từ dữ liệu dạy ⇒ không có cây này thì P4 và V1 không chạy được. `.gitignore:44–45,111` loại nó khỏi kho nên clone về cũng không có.<br>⛔⛔ `--shards` **mặc định là 1** (dòng 187) trong khi dữ liệu dạy có 76 shard (dòng 80: `data/train-{i:05d}-of-00076.parquet`). Gõ lệnh trần là bạn dựng **1/76 dữ liệu**, ra ~850 bước thay vì 64.567, mà **không có lỗi nào báo** — mọi thứ sau đó vẫn chạy, chỉ là sai. ⭐ Kiểm ngay: `wc -l harness/dg1_cache/train_ac/train.jsonl` phải ra **64567**.<br>⚠️ Đối chiếu: `build_test_data.py` thì mặc định đã là `N_TEST_SHARDS = 9` nên **P2 gõ lệnh trần là đúng** — chỉ mỗi nhánh train có bẫy này |
| **P4** | Viết MỚI đoạn tách val theo EPISODE từ `train_ac`: **400 bước (vòng thô) + 600 bước (vòng tinh)** | ⛔ Đây là **VIẾT MÃ MỚI**, không phải "sửa một cờ". `build_train_data.py` chỉ có `--check`, `--shards`, `--n-check` (dòng 186–191) — không có cờ tách val nào.<br>⛔ Chia theo **episode**, không theo bước. ⛔ **KHÔNG** dùng lát dev 1.400: nó lấy từ tập kiểm (`report/124:739`, `report/143:213`).<br>⛔ **KHÔNG phân tầng theo `app`** — đã đo trên `test.jsonl`: trường `app` **rỗng ở 55% số bước** (3.828/6.958) và có tới **270 giá trị khác nhau** trên 1.432 episode, chia 400 bước vào 270 tầng là vô nghĩa. Phân tầng theo **`action_type`**: 8 tầng, đủ cả 8, và liên quan trực tiếp tới `exec` (chỉ `click`/`long_press` mới có con trỏ để chấm ±14%) |
| **P4bis** | ⛔⛔ **NỐI `train_tru_val.jsonl` VÀO ĐƯỜNG DỰNG DỮ LIỆU** — sửa `harness/build_branch_data.py:111`, đổi `"train.jsonl"` thành `"train_tru_val.jsonl"`, rồi chạy nó để sinh lại bộ `gui_s1` | ⛔⛔ **ĐÂY LÀ VIỆC DỄ QUÊN NHẤT VÀ HỎNG NẶNG NHẤT CỦA CẢ KẾ HOẠCH.** `build_branch_data.py:111` ghi cứng `train.jsonl`. Bỏ qua bước này thì **tập val nằm nguyên trong dữ liệu huấn luyện** — mọi số val sau đó đẹp một cách vô nghĩa, **không có lỗi nào báo**, và bạn chỉ phát hiện khi chấm test thấy giảm, tức là **sau khi đã tiêu 20–37 giờ A100**.<br>⭐ Kiểm bắt buộc: `wc -l` bộ `gui_s1` mới phải **nhỏ hơn** bộ cũ đúng bằng số bước val (≈1.004) |
| **P5** | Script chấm val, in ba số mỗi điểm lưu: **`exec` val · lật sạch · lật ngược** — đặc tả đầy đủ ở §4 | `exec` val là **tiêu chí dừng**; hai số lật là **chẩn đoán**. ⛔ **Không dừng theo mất mát** — GRPO chết đúng ở đó. ⚠️ `infer_branch.py` đọc cứng `test_ac/test.jsonl` (không có cờ đổi tệp vào) ⇒ phải thêm tham số đường dẫn thì mới suy luận được trên `val400.jsonl`. ⛔ **Đừng nhân trọng số 1,34× vào số val** — xem §4 |
| **P6** | Tải hai adapter từ Drive: `MyDrive/thesis/ckpt/grpo_point_seed101/` chứa cả `adapter_grpo_point_seed101/` (GRPO) và `adapter_ref_min/` (MIN) | ⛔ trọng số **KHÔNG có trong kho** (`.gitignore:136,140` loại `runs/*/adapter_*/`) và **không** có trên đĩa. Nguồn: `runs/grpo_point/README.md:17-18` |
| **P7** | Thêm `--alpha` vào `harness/infer_branch.py` (6 dòng, chèn **sau dòng 516**) | ⛔ không dùng `peft.add_weighted_adapter`; nhân thẳng `mod.scaling[k] *= alpha`, vì đầu ra LoRA là `scaling·B(A(x))` nên α=0 cho đúng bằng 0. ✅ đường suy diễn **không lượng tử hoá** (`infer_branch.py:512-516`) nên nội suy sạch |
| **P8** | Ghi bốn Phụ lục A–D ra tệp thật rồi commit: `harness/do_chot_cuoi.py` · `phu_luc_b.py` · `phu_luc_c.py` · `phu_luc_d.py` | Hiện chúng chỉ tồn tại dưới dạng khối mã trong file này; `_exports/` không có trên đĩa. ✅ `.gitignore` không chặn `harness/*.py`. Chạy mỗi tệp một lần, đối chiếu mục *"Kết quả mong đợi"* ngay dưới nó — lệch ⇒ **báo lại trước** khi tin số nào |

### 1.2 PHASE 1 — 0 giờ A100, ra số TRƯỚC khi tiêu tiền

| # | việc | giá | ⭐ tiêu chí đi/dừng |
|---|---|---|---|
| **V1** | Hiệu chuẩn val: chấm S1 · MIN · GRPO lên val mới | ~3 h T4 | tiêu chí đọc ở **1.2bis** — ⛔ đừng dùng dạng *"val phải xếp đúng thứ tự ba nhánh"*, phép đó vô nghĩa về thống kê |
| **V2** | Nội suy MIN ↔ GRPO, 5 mức α — đặc tả ở **§5** | ~4 h T4 | trần oracle **61,44**; kỳ vọng thật **+0,2…+0,5**, có thể 0 |
| **V3** | Soup tuyến tính đều họ `<desc>` — chỉ nếu còn hạn mức T4. ⭐ Đúng ba adapter: **MIN · GRPO · CE2-S2/101**, mỗi cái hệ số **1/3**. Dùng lại `noi_suy()` ở §5.3bis, ghép nối 3 khối ⇒ `r ×3`, `lora_alpha ×3` | ~4 h T4 | ⛔ chỉ trung bình **ĐỀU**. ⛔ không dò hệ số bằng Optuna/tiến hoá — cực đại của hàng trăm phép thử trên val SE ~1,03 pp là máy sinh số ngẫu nhiên. ⛔ không đưa S1 hay `gui_sel` vào: chúng **không sinh `<desc>`** (S1 `action_ok` = 94,35 so với 98,86 của họ `<desc>`) ⇒ định dạng đầu ra khác, trộn vào là nguy cơ sụp đổ biểu diễn. ⚠️ Nếu CE2 khác `r` với hai cái kia thì bỏ CE2, soup 2 cái |
| **V4** | Khoá một α trên val, ghi vào đăng ký, rồi chấm **test một lần** | ~5,6 h T4 | ⛔ báo vô điều kiện, kèm cả hai đầu mút. Không chấm cả 5 mức trên test rồi khoe mức cao nhất |

### 1.2bis ⛔ Tiêu chí nghiệm thu của V1 — và vì sao cách phát biểu hiển nhiên lại VÔ NGHĨA

Cách phát biểu dễ nghĩ ra nhất — *"val hợp lệ nếu nó xếp đúng thứ tự ba nhánh: S1 59,11 < MIN
60,05 < GRPO 60,07"* — **không dùng được**. Nhưng phải dùng **đúng loại sai số chuẩn** mới thấy
vì sao, và đây là chỗ rất dễ sai:

| | công thức | ở val 400 bước | dùng cho việc gì |
|---|---|---|---|
| SE không ghép cặp | √(0,6 × 0,4 / 400) | **2,45 pp** | sai số của **một con số tuyệt đối** (*"nhánh này được 60,0"*) |
| ⭐ **SE GHÉP CẶP** | đo thật, rồi co giãn × √(4437/400) | **1,03 pp** (GRPO−MIN)<br>**1,88 pp** (MIN−S1) | ⭐ sai số của **HIỆU** hai nhánh trên cùng tập bước — đây mới là cái dùng để xếp hạng |

Số ghép cặp là **đo thật, không phải ước lượng**: Phụ lục A in ra `GRPO/101 − MIN/101 = +0,02
SE=0,309` và `MIN/101 − S1/101 = +0,94 SE=0,564` trên n=4437, co giãn về n=400 ra hai số trên. Nó
nhỏ hơn 2,4 lần SE không ghép cặp, vì hai nhánh gặp đúng cùng những bước khó nên phần nhiễu chung
triệt tiêu.

⇒ Ngay cả với sai số nhỏ hơn ấy, phép kiểm xếp hạng vẫn vô vọng: khoảng cách MIN ↔ GRPO là
**0,02 pp**, tức **1/51 của một SE ghép cặp**. Nó không thể đạt hay không đạt theo bất kỳ nghĩa
nào — chỉ là tung đồng xu. Khoảng cách S1 ↔ MIN khá hơn nhưng vẫn chỉ **0,95 / 1,88 ≈ nửa SE**,
tức công suất phát hiện **dưới 10%**.

⇒ **Tiêu chí đúng — coi V1 là phép thử BẮT THẢM HOẠ, không phải phép thử xếp hạng:**

| # | kiểm | ngưỡng | ý nghĩa |
|---|---|---|---|
| 1 | ba nhánh đều rơi trong **50–70** | bắt buộc | ra ngoài dải này ⇒ đường chấm hỏng (sai prompt, sai ảnh, sai luật chấm) — đây mới là thứ V1 thật sự bắt được |
| 2 | ba nhánh **không cách nhau > 3 SE** (≈ 7 pp) | bắt buộc | cách xa bất thường ⇒ val trúng một lát lệch nặng, chia lại |
| 3 | S1 không cao hơn trung bình của MIN và GRPO quá 1 SE ghép cặp (1,88 pp) | mềm | kiểm hướng, công suất dưới 10% — đạt thì yên tâm hơn, ⛔ **không đạt cũng đừng dừng**, vì thiết kế vốn không đủ sức phát hiện |

⛔ **Và luật bất di bất dịch: KHÔNG BAO GIỜ trích một con số val nào ra báo.** Val chỉ để xếp hạng
ứng viên trong cùng một họ (điểm lưu, hoặc α) — trong đó các ứng viên ghép cặp trên đúng cùng tập
bước, nên dùng được SE 1,03 pp thay vì 2,45 pp. Đó là lý do val vẫn hữu dụng cho V2/A6 dù nó
không phân giải nổi 0,02 pp.

⚠️ Nhưng đừng đọc điều đó thành *"val chính xác tới 1 pp"*. Còn hai chỗ rò: ① ⛔ SE ghép cặp chỉ
đúng nếu val thật sự đã bị loại khỏi dữ liệu dạy — tức việc P4bis phải làm xong, nếu không mọi
con số ở đây đều vô nghĩa. ② khi chọn argmax trên 21 ứng viên, sai số hiệu dụng rộng hơn SE của
một phép so đơn lẻ, vì bạn đang lấy cực đại của nhiều biến nhiễu — đó chính là lý do có luật chọn
ở §5: chỉ rời α = 0 khi ứng viên thắng hơn ≥ 2,0 pp.

### 1.3 PHASE 2 — lượt A100 duy nhất

| # | việc | giá | ⛔ chi tiết |
|---|---|---|---|
| **A1** | Dựng `harness/train_config_vissft.yaml` | 0 | bảng sửa từng dòng ở **§3**. ⚠️ **Không sửa tại chỗ** `train_config.yaml` — nó là cấu hình của các nhánh đã niêm phong; copy ra file mới |
| **A2** | Viết bốn thứ mã ở **§4** | 0 | |
| **A3** | ⭐ Khẳng định TĨNH trước bước 1 | 0 giây | assert số tham số huấn luyện > **14.966.784** và có tensor `visual.*` với `requires_grad=True`. ⛔ Đừng dùng cổng `grad_norm` ở bước 10 — LoRA khởi tạo B = 0 nên gradient bằng 0 ở bước đầu dù dây nối đúng ⇒ báo động giả |
| **A4** | Smoke 200 bước | ~0,5 h | chặn hai bẫy âm thầm trước khi cam kết 20–37 h |
| **A5** | **Lượt VIS-SFT** | **20–37 h** | `freeze_vision_tower: false` là **cờ duy nhất** đổi so với S1/101 ⇒ phép so một biến, mốc **59,11** |
| **A6** | Chấm 5 điểm lưu từ `grid/` trên val 400, rồi 2 điểm tốt nhất trên val 600 | ~4 h T4 | successive halving (Jamieson & Talwalkar, AISTATS 2016) — có bài báo, khai được.<br>⭐ Năm điểm nào: `step01600` · `step03200` · `step04800` · `step06400` · `step08072` (cách đều trong 40 điểm, gồm cả điểm cuối). ⛔ Đừng chỉ chấm mấy điểm cuối — nếu đường cong đạt đỉnh sớm rồi thoái hoá, chấm cụm cuối sẽ không thấy đỉnh.<br>⭐ Vòng 2: lấy 2 điểm cao nhất, chấm cả hai điểm lưu kề bên mỗi cái (±200 bước) trên val 600. ⛔ Chọn theo **val 600**, không phải val 400 — val 400 đã bị dùng để lọc nên nó thiên vị lạc quan |
| **A7** | Khoá (điểm lưu, α), chấm **test** hai cấu hình: **A** = điểm lưu cuối, α=1 · **B** = argmax-val | ~11 h T4 | ⛔ khai thứ bậc **TRƯỚC** khi chấm; báo cả hai vô điều kiện |

**Tổng A100: 20,5–37,5 h** trong ngân sách 50 h. **Tổng T4 Phase 1+2: ~28 h** = vừa một tuần Kaggle.

⚠️ **Ba luật khi đọc kết quả quét:** ① ⛔ không bao giờ trích con số val — nó chỉ để xếp hạng; số
đem báo là test, chấm đúng một lần sau khi đã khoá. ② lấy **đỉnh đường cong đã LÀM TRƠN**, không
lấy gai đơn lẻ. ③ biên cổng bỏ lượt phải **một phía và RỘNG** — bỏ khi **RÕ RÀNG tệ hơn**, ⛔
không bỏ khi chỉ **CHƯA tốt hơn**.

### 1.4 PHASE 3 — chỉ khi có số tốt

| điều kiện | việc |
|---|---|
| A7 vượt **60,07** | hạt giống **202** cho **đúng nhánh đó** (~25 h A100). ⚠️ Chỉ vừa ngân sách nếu A5 rơi gần **20 h** |
| A7 không vượt | ⛔ đừng chạy 202. Ghi ngắn — *"chạy một lần không ra số tốt"* — rồi dừng. Tiêu đề vẫn **60,07** |

---

## 2. ⛔ CẮT KHỎI KẾ HOẠCH — đừng hồi sinh, TRỪ một mục ở 2.1bis

⚠️ Ba lý do cắt khác nhau, đừng gộp làm một — vì cách bảo vệ trước hội đồng cũng khác nhau:
**(a)** bất khả thi hoặc vượt ngân sách → §2.1 · **(b)** không còn áp dụng được sau khi đổi thiết
kế, bản thân hướng đi **chưa hề bị bác** → §2.1bis · **(c)** đã bị bác **bằng số** → §2.2. Chỉ
nhóm (c) mới là *"hướng này sai"*. Nhóm (b) chỉ có đúng một mục, và nó **được phép quay lại** nếu
thiết kế đổi lần nữa.

### 2.1 Cắt vì bất khả thi hoặc vượt ngân sách

| việc bị cắt | vì sao |
|---|---|
| daemon chấm bất đồng bộ trên T4 | bất khả thi: A100 ở Colab ghi vào Drive, T4 miễn phí ở Kaggle, mà `kaggle_phepB_uivenus.md:107,:658` ghi rõ Kaggle không mount được Drive ⇒ không có đĩa chung. Và không cần — ba thước của cổng là so chuỗi/số, chạy CPU vài mili giây |
| quét lưới đầy 200 ứng viên | ~390 h T4 (200 × 1,95 h) = 13 tuần hạn mức Kaggle |
| hoà checkpoint GRPO rồi train tiếp | ⚠️ KHÔNG phải vì dở, cũng KHÔNG phải vì tốn — xem **2.1bis**, đây là mục duy nhất trong cả §2 được phép hồi sinh |
| lát dev 1.400 bước | nó lấy từ tập kiểm — dùng nó là để tập kiểm lọt vào quyết định huấn luyện |
| `lora_dropout` | ⛔ đừng chi lượt A100 cho trục này — lật ngược **không** phải overfitting cổ điển |
| Qwen2.5-VL-7B | cần **hai** lượt (Base-7B + S1-7B) ≥ 46 h A100, phá toàn bộ bảng 8 nhánh |

### 2.1bis ⚠️ "Hoà checkpoint GRPO" — cắt vì ĐỔI THIẾT KẾ, không phải vì nó dở

Mục này tách riêng vì nó khác hẳn mọi mục còn lại của §2: nó **chưa bao giờ bị bác**. Nó bị cắt
vì một quyết định thiết kế ở chỗ khác làm nó **không còn chỗ đứng**.

Trước đây VIS-SFT định xuất phát từ **GRPO/101** (60,07) cho cao hơn S1 (59,11). Sau đã đổi sang
xuất phát từ **model gốc**, vì ba lý do — và không lý do nào là tiền:

| # | vì sao bỏ mốc xuất phát GRPO |
|---|---|
| 1 | **Không quy được công.** Xuất phát từ GRPO mà số lên thì **không tách được** phần nào do mở băng thị giác, phần nào do GRPO vốn đã cao hơn. Cả luận văn dựa vào một phép so **đúng MỘT biến** với S1/101 = 59,11 |
| 2 | **Bẫy PEFT.** Nạp adapter cũ rồi thêm module mới vào `lora_target`, PEFT **bỏ qua module mới trong im lặng** — lượt train chạy trơn tru, tốn đủ giờ A100, mà tầng thị giác **không hề được học**. Sai kiểu này không có thông báo lỗi nào |
| 3 | **Lệch tập dữ liệu.** GRPO sống nhờ thẻ `<desc>` (`gui_s2`), còn S1 dùng `gui_s1` không có thẻ đó. Train tiếp bằng `gui_s1` là dạy model vứt bỏ `<desc>` — vừa mất kênh theo dõi A, vừa bào mòn dần chính lợi thế của GRPO |

Chi phí (+5,6 h T4 và 7 GB Drive) chỉ là lý do phụ: đã không dùng thì không việc gì phải trả.

⭐ **Khi nào được hồi sinh:** nếu A7 (VIS-SFT từ model gốc) về **dưới 59,11**, tức mở băng thị
giác tự nó không đủ, thì xuất phát từ GRPO là phương án lùi **hợp lệ** — đánh đổi: mất khả năng
quy công sạch, đổi lấy mốc nền cao hơn 0,96 pp. Lúc đó phải làm đủ ba việc: hoà adapter bằng
`merge_and_unload` ở fp16/bf16 → **chấm lại để xác nhận ra đúng 60,07** → rồi mới train QLoRA
adapter **MỚI hoàn toàn** trên checkpoint đã hoà (⛔ không nạp chồng adapter cũ, xem lý do #2), và
đổi `dataset` sang `gui_s2` (lý do #3).

### 2.2 Đã bị bác BẰNG SỐ — mỗi hướng có một con số giết nó

| hướng | bác bằng gì |
|---|---|
| ⛔ ORPO tầng câu | trần **+4,80** là ảo do chọn mẫu: nó tính trên lát *"chỗ A(MIN) sai"*, tức lấy đúng những ca mô hình so sánh hỏng. Đổi bộ chọn sang *"chỗ A(GRPO) sai"* còn **+2,88**; trên lát định nghĩa **không dùng hành vi mô hình nào** thì **−0,65** — tức âm. Đây là **trần**, không phải kỳ vọng ⇒ phần thu thật chỉ là một phân số của nó (Phụ lục C, chạy được) |
| ⛔ `gui_sft_match` / bỏ nước đi bỏ cuộc | phản thực tế ghép cặp **59,44** — **thấp hơn 60,07**; trần 65,44 là nguỵ biện chọn mẫu (Phụ lục A mục I) |
| ⛔ OCR / cây trợ năng vào đầu vào | prompt **đã có** 24 dòng OCR; `gui_sel` = **56,13**; khối ứng viên cho **+0,58** [−0,64 · +1,77] ngay ở lát dùng nó |
| ⛔ Vá tên bằng OCR | **68,6%** tên mô hình sinh **đã là chuỗi thật** trên màn — đúng chuỗi của **sai phần tử**; copy OCR gần điểm vàng cho **64,9% < 66,3%** mô hình tự đạt |
| ⛔ GRG / chưng cất câu qua bộ trỏ thứ hai | tầng nó dạy đã **87,1** so với người **86,3** (dư địa âm); dư địa diễn đạt **+1,88** (dưới MDE) |
| ⛔ Đa nhiệm thêm đích hộp/toạ độ | S2 = **57,18** (âm 1,93); GRPO-point: khai báo **+2,56** nhưng `exec` **+0,02**, hệ số truyền **0,01** so dự báo ghi trước 0,43 |
| ⛔ RL trực tuyến | `frac_reward_zero_std` 0,515 · entropy 0,274→0,248 · suất ròng 0,0010 (z=0,07) · Venus 4 s/lượt **trong** vòng lặp ⇒ 14,52 h A100 cho một lượt 500 bước |
| ⛔ Spatial CoT / ngôn ngữ vị trí | bỏ **toàn bộ** ngôn ngữ vị trí chỉ **−1,38 pp**; đổi động từ ±0,12; đổi thứ tự **0,00** |
| ⛔ Gộp nhánh / bỏ phiếu ở **ĐẦU RA** | oracle 8 nhánh **72,80** (+12,73) nhưng **mọi bộ chọn không-oracle ≤ 60,45** |

⚠️⚠️ **ĐỪNG ĐỌC DÒNG CUỐI THÀNH "MỌI CÁCH GỘP ĐỀU BỊ BÁC".** Cái bị bác là gộp ở **ĐẦU RA**
(chọn câu của nhánh nào). Gộp ở **KHÔNG GIAN TRỌNG SỐ** là việc khác hẳn — nó tạo ra **một
checkpoint mới**, nên là đóng góp mô hình, và **chưa từng thử** (đã tra toàn kho: không khớp nào
cho `add_weighted_adapter` · `merge` · nội suy). Đó chính là việc **V2** và **V3**.

---

## 3. BẢNG SỬA CẤU HÌNH — `harness/train_config_vissft.yaml`

Copy `harness/train_config.yaml` ra file mới rồi đổi các dòng sau. Số dòng là của
`train_config.yaml` bản hiện tại. Cột *"phải thành"* đã áp mọi sửa chữa — dùng thẳng.

| dòng | hiện tại | phải thành | vì sao |
|---|---|---|---|
| 22 `model_name_or_path` | `Qwen/Qwen2.5-VL-3B-Instruct` | ✅ **GIỮ NGUYÊN** (model gốc) | mốc so là S1/101 = 59,11, và `freeze_vision_tower` là **cờ duy nhất** khác ⇒ phép so một biến. Xuất phát từ checkpoint đã hoà thì mất tính chất đó, lại dụng bẫy PEFT ở dòng dưới |
| — `adapter_name_or_path` | (không khai) | ⛔ **VẪN KHÔNG KHAI** | khai vào là PEFT đọc lại `adapter_config.json` cũ và **NUỐT** `lora_target` mới trong im lặng. `create_new_adapter: true` **vẫn** rơi vào đường resume |
| 28 `dataset` | ✅ đã có, `gui_s1` | giữ `gui_s1` | khớp với model gốc. ⛔ Nếu (và chỉ nếu) xuất phát từ checkpoint họ `<desc>` thì **bắt buộc** `gui_s2`, vì train trên `gui_s1` là dạy model bỏ khối `<desc>` |
| 30 `output_dir` | `/workspace/ckpt/s1_seed101` | `/content/drive/MyDrive/thesis/ckpt/vissft_seed101` | ⛔ đường dẫn vast.ai còn sót từ trước 11/8. Để nguyên ⇒ Colab thu hồi phiên là mất trắng. Trỏ Drive thì bỏ lượt giữa đường **không mất gì** |
| 39 `lora_dropout` | `0.05` | ✅ **GIỮ 0.05** | lật ngược **không** phải overfitting cổ điển |
| 40 `lora_target` | 7 khối ngôn ngữ | ✅ **GIỮ NGUYÊN**; muốn thêm attention thị giác thì dùng `lora_target: all` | MLP thị giác của Qwen2.5-VL dùng `gate_proj`/`up_proj`/`down_proj` — **đã có** trong danh sách ⇒ chỉ cần cờ 41 là **32 tầng MLP thị giác đã học**. ⛔ Đừng thêm `qkv,proj,fc1,fc2`: `fc1`/`fc2` là tên Qwen2-VL đời cũ ⇒ khớp rỗng, còn chuỗi trần `proj` khớp cả `q_proj`/`o_proj`/`gate_proj` theo hậu tố |
| 41 `freeze_vision_tower` | `true` | ⭐⭐ **`false`** | **đây là can thiệp duy nhất** |
| 42 `freeze_multi_modal_projector` | `true` | ✅ GIỮ `true` | đổi thành `false` là vô tác dụng dưới `finetuning_type: lora` — projector là `visual.merger.mlp.0/.2`, không khớp tên nào trong `lora_target`. Hai cờ này **độc lập** |
| 77 `save_steps` | `200` | ✅ GIỮ `200` | ⇒ **40 điểm lưu** trên 8.072 bước (`ceil(64567/16)×2`); đủ dày cho lưới (điểm lưu) × α |
| 78 `save_total_limit` | `2` | ✅ GIỮ `2` + callback copy adapter (mã ③ §4) | ⛔ nâng lên 40 tốn ~8 GB Drive (optimizer ~160 MB/bản, mà Drive miễn phí chỉ 15 GB). ⛔ `save_only_model: true` thì mất resume, mà Colab hay thu phiên. ✅ Giữ 2 + copy riêng adapter (59,9 MB) = ~2,4 GB (~3,3 GB nếu bật LoRA thị giác), resume nguyên vẹn, lưới vẫn đủ 40 điểm |
| 91 `val_size` | `0.0` | ✅ GIỮ `0.0` | ⛔ Đặt `0.1` là SAI: LLaMA-Factory chia **ngẫu nhiên theo dòng**, mà màn cùng một app na ná nhau ⇒ rò rỉ và cho điểm ảo (chính `train_config.yaml:88-90` đã cảnh báo). Val phải tách ở **khâu dựng dữ liệu**, theo **episode** — việc P4 |
| 92 `do_eval` | `false` | ✅ GIỮ `false` | `evaluate()` của Trainer tính mất mát, không tính `exec`. Ta chấm bằng callback tự sinh câu. Dừng theo mất mát là dừng theo **sai đại lượng** — đúng chỗ GRPO chết |
| — `weight_decay` | ⚠️ KHÔNG file nào khai ⇒ mặc định 0 | ⛔ **ĐỂ NGUYÊN 0** | ⛔⛔ **BẢN TRƯỚC CỦA FILE NÀY TỰ MÂU THUẪN Ở ĐÂY** — vừa bảo đặt 0.01, vừa tuyên bố A5 *"chỉ đổi một biến so với S1/101"*. Không thể cùng đúng: thêm `weight_decay` là biến thứ hai, và mọi mức tăng thu được sẽ **không tách được** phần nào do mở băng thị giác, phần nào do co chuẩn — làm hỏng đúng cái luận điểm mà A5 sinh ra để chứng minh.<br>⇒ Xử: A5 giữ `weight_decay = 0`, bảo toàn phép so một biến với mốc 59,11.<br>⭐ `0.01` vẫn là ứng viên tốt nhất cho lượt kế tiếp, nhưng chỉ chạy khi P5 báo **lật ngược cao** (train có học nhưng phá gần bằng phần sửa) — đó mới là triệu chứng mà lực co nhắm vào. Lúc đó nó là **thí nghiệm riêng**, khai riêng, mốc so là chính A5 chứ không phải S1 |
| — `additional_target` | (không khai) | ⛔⛔ **CẤM KHAI** | nó sinh `modules_to_save` — huấn luyện toàn phần **ngoài** LoRA — mà α không scale được ⇒ phá vỡ lập luận sàn |

⇒ Lỗi thật của các lượt trước **không phải** hai dòng 91–92, mà là **KHÔNG CÓ TẬP VAL NÀO CẢ**.
Sửa bằng cách dựng val riêng (P4), không phải bằng cách bật cơ chế tự chia của thư viện.

---

## 4. MÃ PHẢI VIẾT — bốn thứ, đều 0 giờ A100

| # | viết gì | đặt đâu |
|---|---|---|
| ① | Dựng val từ dữ liệu dạy, tách theo **episode** (400 + 600 bước) — ⛔ KHÔNG sửa `build_train_data.py` (nó không có cờ nào cho việc này); viết **script riêng** | `harness/tach_val.py` |
| ② | Chấm val + đếm lật sạch / lật ngược. In ba số mỗi điểm lưu: `exec` val (**tiêu chí dừng**), lật sạch, lật ngược (**chẩn đoán**). ⚠️ Đây là mã **DUY NHẤT cố ý KHÔNG viết sẵn** — nó cần nạp model, mà máy soạn file này không có GPU nên không chạy thử được; viết mã suy luận chưa từng chạy mà trông có vẻ chuẩn thì **hại hơn lợi**. Đặc tả đầy đủ ngay dưới bảng | script mới |
| ③ | `TrainerCallback`: sau mỗi lần lưu, **copy riêng file adapter** (59,9 MB) sang `grid/`, bọc `try/except`, để HF không xoá ⇒ biến **một lượt A100 thành 40 quan sát** | `harness/grid_callback.py` |
| ④ | Thêm `--alpha` vào `infer_branch.py` — chèn sau dòng 516 | `harness/infer_branch.py` |
| ⑤ | Tách val — mã đầy đủ ngay dưới, logic đã chạy thử trên `test.jsonl` | `harness/tach_val.py` |

### Đặc tả mã ② — "lật sạch / lật ngược" (⛔ hai chữ này dùng khắp file mà chưa từng được định nghĩa)

Ghép cặp theo khoá `(episode_id, step_id)` giữa nhánh MỚI và nhánh NỀN, **trên đúng cùng tập
val**. Với mỗi bước, `exec` là 0 hoặc 1 theo đúng hàm chấm test (`harness/metric_exec.py`):

| tên | định nghĩa | ý nghĩa |
|---|---|---|
| **lật sạch** | số bước có `exec_nền = 0` và `exec_mới = 1` | lượt train **sửa được** |
| **lật ngược** | số bước có `exec_nền = 1` và `exec_mới = 0` | lượt train **phá mất** |
| **Δexec** | (lật sạch − lật ngược) / n | ⭐ đây là **hằng đẳng thức**, không phải xấp xỉ: mọi thay đổi của `exec` chỉ đến từ hai loại lật này |

**Nền là gì:** bản chấm S1/101 trên chính tập val đó — tức sản phẩm của việc V1. Chấm một lần,
lưu lại, rồi dùng chung cho mọi điểm lưới. ⛔ Đừng lấy nền là điểm lưới trước đó, sẽ không so
được các điểm lưới với nhau.

**Đầu ra:** một dòng JSON mỗi điểm lưới, để về sau xếp hạng bằng `argmax`:
`{"step": 1600, "exec_val": 59.8, "lat_sach": 41, "lat_nguoc": 37, "n": 400}`

**Vì sao cần cả hai số lật chứ không chỉ `exec`:** một điểm lưới đứng yên có hai nguyên nhân hoàn
toàn khác nhau, và `exec` một mình **không phân biệt được**. Lật sạch thấp và lật ngược thấp
nghĩa là *"chưa học được gì"* — nên train thêm. Cả hai đều cao nghĩa là *"học được nhiều nhưng
phá đúng bằng đó"* — train thêm sẽ **không** cứu được, phải giảm bước đi (chính là chỗ việc V2
nội suy nhắm tới).

⛔ **Đừng tự chế trọng số.** Con số *"lật ngược đắt hơn 1,34×"* ở mục 5.1 là kết quả đo trên tập
KIỂM của riêng cặp MIN ↔ GRPO. Không đem nhân vào số val. Cứ in **hai số thô**, để người đọc tự cân.

```python
# harness/tach_val.py — mã ⑤. Chay: python3 harness/tach_val.py
# Da CHAY THU tren test.jsonl (cung luoc do): lech phan bo lon nhat 0,65 pp,
# ca 3 phep kiem ro ri deu dat. Chua chay tren train.jsonl vi cay do CHUA CO.
import os, json, random, collections

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dg1_cache", "train_ac")
SEED = 101                                   # ⛔ ghim cung, doi la mat tinh tai lap

def loai(r):
    a = r.get("action")
    return (a or {}).get("action_type", "?") if isinstance(a, dict) else "?"

def tach_val(recs, n_buoc, seed, loai_tru=frozenset()):
    """Chon EPISODE nguyen ven cho du ~n_buoc, khop phan bo LOAI THAO TAC.
    Don vi chia la EPISODE, khong phai buoc: cung episode o hai ben la RO RI."""
    theo_ep = collections.defaultdict(list)
    for r in recs:
        if str(r["episode_id"]) not in loai_tru:
            theo_ep[str(r["episode_id"])].append(r)
    eps = sorted(theo_ep)                    # sap xep truoc => tai lap duoc
    tong = collections.Counter(loai(r) for r in recs); N = sum(tong.values())
    muc_tieu = {k: v / N for k, v in tong.items()}

    rng = random.Random(seed)
    tot_nhat, diem_tot = None, float("inf")
    for _ in range(200):                     # 200 lan boc, giu lan can phan bo nhat
        thu = eps[:]; rng.shuffle(thu)
        chon, nb = [], 0
        for e in thu:
            if nb >= n_buoc: break
            chon.append(e); nb += len(theo_ep[e])
        c = collections.Counter(loai(r) for e in chon for r in theo_ep[e])
        m = sum(c.values())
        diem = sum(abs(c.get(k, 0) / m - p) for k, p in muc_tieu.items())
        if diem < diem_tot:
            diem_tot, tot_nhat = diem, chon
    return set(tot_nhat), [r for e in tot_nhat for r in theo_ep[e]]

def ghi(ten, rows):
    with open(os.path.join(ROOT, ten), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"  {ten:<22}{len(rows):>6} buoc")

if __name__ == "__main__":
    R = [json.loads(l) for l in open(os.path.join(ROOT, "train.jsonl"), encoding="utf-8")]
    print(f"quan the: {len(R)} buoc / {len({r['episode_id'] for r in R})} episode")

    ep400, v400 = tach_val(R, 400, SEED)                      # val vong THO
    ep600, v600 = tach_val(R, 600, SEED, loai_tru=ep400)      # val vong TINH
    day = [r for r in R if str(r["episode_id"]) not in (ep400 | ep600)]

    # ⛔⛔ BA PHEP KIEM — hong mot cai la moi con so val deu vo nghia
    assert not (ep400 & ep600), "RO RI: hai lat chung episode"
    assert len(v400) + len(v600) + len(day) == len(R), "MAT hoac NHAN DOI ban ghi"
    assert not ({(r["episode_id"], r["step_id"]) for r in v400}
                & {(r["episode_id"], r["step_id"]) for r in v600}), "RO RI o muc buoc"

    ghi("val400.jsonl", v400); ghi("val600.jsonl", v600)
    ghi("train_tru_val.jsonl", day)          # ⛔⛔ PHAI train tren file NAY

    P = collections.Counter(loai(r) for r in R)
    for ten, V in (("val400", v400), ("val600", v600)):
        C = collections.Counter(loai(r) for r in V)
        mx = max(abs(100 * C.get(k, 0) / len(V) - 100 * v / len(R)) for k, v in P.items())
        print(f"  {ten}: lech phan bo lon nhat {mx:.2f} pp", "OK" if mx < 3 else "KEM -> doi SEED")
```

⛔⛔ **Cái bẫy giết cả thí nghiệm:** script ghi ra `train_tru_val.jsonl`, và cấu hình huấn luyện
**phải trỏ vào tệp đó**, không phải `train.jsonl`. Quên bước này là bạn train trên chính tập val —
mọi con số val sau đó đều đẹp một cách vô nghĩa, mà không có thông báo lỗi nào, và bạn chỉ phát
hiện khi chấm test thấy giảm.

⚠️ **Vì sao phân tầng theo `action_type` chứ không theo `app`:** đã đếm trên `test.jsonl` — `app`
rỗng ở 3.828/6.958 bước (55%) và có 270 giá trị trên 1.432 episode. `action_type` thì đủ cả 8 tầng
(`click` 63,9% · `scroll` 10,9% · `wait` 7,3% · `input_text` 7,1% · `open_app` 6,7% ·
`navigate_back` 3,9% · `long_press` 0,2% · `navigate_home` 0,03%) và là biến liên quan trực tiếp
tới `exec`, vì chỉ `click`/`long_press` mới có con trỏ để chấm ±14%.

⭐ **Kết quả chạy thử** (trên `test.jsonl`, vì `train_ac/` chưa có — xem P3bis): 400 bước / 84
episode và 604 bước / 125 episode, lệch phân bố lớn nhất 0,65 pp, cả ba phép kiểm rò rỉ đạt.
⚠️ `val600` ra 604 chứ không tròn 600 vì đơn vị chia là episode — đúng như thiết kế, đừng "sửa"
cho tròn số.

```python
# harness/grid_callback.py — mã ③, du de dung thang     [đối chiếu ảnh p09–p10]
import os, glob, shutil
from transformers import TrainerCallback

class CopyAdapterToGrid(TrainerCallback):
    """Copy RIENG file adapter sang grid/ sau moi lan luu, de save_total_limit=2
    van xoa checkpoint nhu thuong ma luoi 40 diem thi con nguyen.
    ~60 MB/diem thay vi ~220 MB (khong keo theo trang thai bo toi uu)."""

    def __init__(self, grid_dir):
        self.grid = grid_dir
        os.makedirs(grid_dir, exist_ok=True)

    def on_save(self, args, state, control, **kw):
        # HF: _save_checkpoint() ghi xong VA xoay vong xong moi goi on_save,
        # nen ban vua ghi chac chan con o day.
        src = os.path.join(args.output_dir, f"checkpoint-{state.global_step}")
        dst = os.path.join(self.grid, f"step{state.global_step:05d}")
        try:
            os.makedirs(dst, exist_ok=True)
            # bat CA .safetensors (PEFT moi) LAN .bin (PEFT cu) — dung ket ten cung
            ten = glob.glob(os.path.join(src, "adapter_model.*")) \
                + glob.glob(os.path.join(src, "adapter_config.json"))
            if not ten:
                print(f"[grid] CANH BAO buoc {state.global_step}: khong thay adapter o {src}")
            for p in ten:
                shutil.copy2(p, dst)
        except Exception as e:                # ⛔ KHONG bao gio de no giet luot train
            print(f"[grid] bo qua buoc {state.global_step}: {e}")
        return control
```

⚠️ `grid_dir` phải là đường dẫn **TUYỆT ĐỐI trên Drive**, cùng cây với `output_dir` — ví dụ
`/content/drive/MyDrive/thesis/ckpt/vissft_seed101/grid`. Để đường dẫn tương đối là Colab thu hồi
phiên thì mất cả lưới. ⛔ Khối `try/except` không được bỏ: một lỗi I/O của Drive giữa lượt không
được phép giết 20–37 h A100.

⭐ **Ba điểm đã đối chiếu thẳng với mã `transformers`**, không phải suy đoán: thư mục tên đúng là
`checkpoint-{global_step}` (dòng 3087) · nó nằm thẳng dưới `args.output_dir` (dòng 3077, nhánh
không dò siêu tham số — đúng ca của ta) · `save_total_limit: 2` không xoá mất bản vừa ghi trước
khi ta copy (xoay vòng ở dòng 3142 nằm trong `_save_checkpoint`, mà `on_save` mãi dòng 2122 mới
được gọi ⇒ ta luôn copy sau khi mọi thứ đã yên).

⛔⛔ **ĐỊNH NGHĨA XONG LÀ CHƯA ĐỦ — PHẢI ĐĂNG KÝ, NẾU KHÔNG NÓ KHÔNG BAO GIỜ CHẠY.**
`llamafactory-cli train cfg.yaml` **không** tự quét thư mục tìm `grid_callback.py`, và không có
khoá YAML nào nạp callback ngoài. Lượt train sẽ chạy trơn tru, tốn đủ 20–37 giờ A100, và `grid/`
**rỗng** — tức mất trắng 40 quan sát mà bạn định dùng để quét, và không có lỗi nào báo.

⇒ Không gọi `llamafactory-cli`. Gọi bằng Python để chèn được callback vào:

```python
# chay_vissft.py — thay cho: llamafactory-cli train harness/train_config_vissft.yaml
import sys
from llamafactory.train.tuner import run_exp
from llamafactory.extras.callbacks import LogCallback
sys.path.insert(0, "harness")
from grid_callback import CopyAdapterToGrid

GRID = "/content/drive/MyDrive/thesis/ckpt/vissft_seed101/grid"   # ⛔ tuyet doi
run_exp(args="harness/train_config_vissft.yaml",
        callbacks=[LogCallback(), CopyAdapterToGrid(GRID)])
```

⚠️ `run_exp` có nhận `callbacks` hay không **tuỳ phiên bản LLaMA-Factory** — kiểm bằng
`python -c "import inspect,llamafactory.train.tuner as t; print(inspect.signature(t.run_exp))"`
**trước** khi đặt lượt A100. Nếu chữ ký không có `callbacks`, phương án lùi rẻ và chắc: cứ chạy
`llamafactory-cli` như cũ, rồi mở một ô Colab thứ hai chạy vòng lặp
`while true; do copy thư mục checkpoint-* mới xuất hiện sang grid/; sleep 300; done`. Xấu, nhưng
không phụ thuộc API.

⚠️ **Điểm CHƯA kiểm chạy được** (máy soạn file không cài `transformers`): hãy để lượt train đi
qua lần lưu đầu tiên rồi `ls` thư mục `grid/` xác nhận có `step00200/` (hay bước lưu đầu của bạn)
với đủ hai tệp, **trước khi bỏ đi ngủ**. Nếu in ra dòng `CANH BAO ...` không thấy adapter thì
LLaMA-Factory đang đặt adapter ở chỗ khác — sửa `glob` cho khớp, đừng kệ nó.

```python
# (1) KHAI THAM SO — canh cac add_argument san co (quanh dong 357, cho --no-adapter).
#     ⛔ THIEU DONG NAY LA AttributeError NGAY LAP TUC: 'Namespace' object has no
#     attribute 'alpha'. Dung bo qua vi tuong doan duoi da du.
ap.add_argument("--alpha", type=float, default=1.0)

# (2) chen NGAY SAU dong 516 (PeftModel.from_pretrained)
if args.alpha != 1.0:
    from peft.tuners.lora import LoraLayer
    for mod in model.modules():
        if isinstance(mod, LoraLayer):
            for k in mod.scaling:
                mod.scaling[k] *= args.alpha
```

⛔ **Bẫy thứ hai của ④ — kết quả cũ bị dùng lại trong im lặng.** Tên tệp đầu ra của
`infer_branch.py` **không chứa α**. Chạy 5 mức α mà để nguyên một `--out` thì hoặc bạn ghi đè lần
nhau, hoặc script thấy tệp đã có rồi bỏ qua — và bạn sẽ chấm cùng một bộ dự đoán năm lần, ra năm
con số giống hệt nhau mà tưởng là đường cong phẳng. ⇒ **Bắt buộc đặt α vào tên tệp**, ví dụ
`--out runs/noisuy/preds_alpha0.50.jsonl`.

⭐ **Phép kiểm bắt buộc cho ④:** `--alpha 0` phải khớp `--no-adapter`, `--alpha 1` phải khớp điểm
đã công bố. Lệch 0,1 pp ⇒ script sai.

⛔ **Early stopping KHÔNG cần một lượt chạy riêng** — nó là **chọn điểm lưu tốt nhất trên val**,
làm **sau** khi train, từ một lượt. Nhưng phải **còn điểm lưu để chọn**, nên mã ③ là điều kiện cần.

---

## 5. ĐẶC TẢ VIỆC V2 — nội suy MIN ↔ GRPO

### 5.1 Nó là gì, và vì sao đúng cặp này

`harness/grpo_point.py:2` ghi GRPO *"nối tiếp từ MIN-DESC/101"*. Nên GRPO **không** là một lượt
train độc lập, mà là **MIN cộng một bước đi (~500 bước) trong không gian trọng số**. Nội suy là đi
một phần bước đó:

> W ← W_gốc + (1 − α)·ΔW_MIN + α·ΔW_GRPO

α = 0 cho đúng MIN (60,05) · α = 1 cho đúng GRPO (60,07) · α = 0,5 đi nửa đường.

**Cơ chế:** bước đi trọn của GRPO sửa **184 bước** nhưng phá **113 bước**, và vì lật ngược đắt hơn
(−53,98 so +40,22) nên bù trừ chỉ còn **+0,045 pp**. Giả thuyết: hai loại thay đổi đó **không đáp
ứng giống nhau theo ĐỘ DÀI bước** — nếu việc phá cần đi xa hơn việc sửa, thì ở α ≈ 0,4–0,6 ta giữ
được phần lớn 184 chỗ sửa mà tránh một phần 113 chỗ phá. Đây là phát hiện của WiSE-FT (CVPR 2022)
/ Model Soups (ICML 2022). ⚠️ Giả thuyết **chưa đo** — đường cong có thể đơn điệu, cực đại đúng
tại α = 1, và khi đó thu được 0.

### 5.2 Con số: trần, kỳ vọng, và khoảng cách giữa hai thứ đó

Lấy GRPO làm nền, giả sử xoá sạch 113 lần lật ngược mà giữ trọn 184 lần lật sạch:

> Δ = 113 × 53,98 / 4437 = **+1,37** ⇒ 60,07 + 1,37 = **61,44**

Bản đầy đủ hơn — lấy max(MIN, GRPO) ở từng ô bảng chéo, thu thêm cả hai ô thoái hoá nhẹ:
+1,37 + 2997×0,13/4437 + 1143×0,61/4437 = **+1,62** ⇒ **61,69**.

⛔⛔ **PHÉP NỘI SUY KHÔNG THỂ ĐẠT TRẦN ĐÓ.** Trần 61,44 giả định chọn **theo từng bước**. Nội suy
chỉ có **một α áp cho toàn bộ** — một bước GRPO phá và một bước GRPO sửa dịch chuyển cùng nhau,
không tách rời được. Trần này là trần của **GIẢ THUYẾT**, không phải kỳ vọng của phép đo.

| | con số |
|---|---|
| trần oracle chọn-từng-bước | 61,44 (đủ ô: 61,69) |
| ⭐ **kỳ vọng thực tế** | **+0,2…+0,5 pp**, và có thể bằng 0 |
| sàn | ~60,05, nhưng chỉ nhờ LUẬT CHỌN ở 5.4 — ⛔ `exec` **không** tuyến tính theo trọng số, nên một điểm α giữa có thể thấp hơn **CẢ HAI** đầu mút |
| MDE 2,11 | ⛔ không vượt được, kể cả ở trần |

⚠️ Đặt kỳ vọng THẤP, và nói thẳng nghịch lý: GRPO nối tiếp từ MIN nên vector nhiệm vụ là **một
hướng ngắn duy nhất**, không có tính đa dạng mà Model Soups cần. Cặp này **dễ diễn giải nhất** (có
sẵn chẩn đoán 184/113) nhưng **ít đa dạng nhất**; còn soup nhiều nhánh (V3) thì đa dạng hơn mà
**không** có chẩn đoán cơ chế nào đỡ. ⇒ **Chạy cả hai, báo cả hai.**

### 5.3 ⛔ Ba bẫy — sai một cái là mất buổi

1. ⛔ **Trọng số không có trong kho.** `.gitignore:136,140` loại `runs/*/adapter_*/`. ✅ Cả hai
   nằm cùng một thư mục Drive: `MyDrive/thesis/ckpt/grpo_point_seed101/` (P6).
2. ⛔ **Ép cả hai adapter về `fp32` TRƯỚC khi tính ΔW.** GRPO là `bfloat16`, MIN là `float32`
   (`runs/grpo_point/README.md:9-10`). Không ép thì sai số cast ~1,65e−03 làm phép kiểm dưới đây
   lệch, và bạn sẽ đi sửa thứ không hỏng.
3. ⛔ **Bình quân riêng `lora_A` rồi riêng `lora_B` là SAI** — tích BA song tuyến:
   [(1−α)B₁ + αB₂][(1−α)A₁ + αA₂] ≠ (1−α)B₁A₁ + αB₂A₂, vế trái sinh hai số hạng chéo vô nghĩa.
   Tính ΔWᵢ = scalingᵢ · BᵢAᵢ tường minh từng module. ⛔ Cũng không dùng `peft.add_weighted_adapter`.

### 5.3bis ⛔⛔ CÁCH TRỘN — trộn thẳng A với B là SAI 65%, và phép kiểm đồng nhất KHÔNG bắt được

⛔ `--alpha` của P7 **KHÔNG** làm được việc này. Nó co giãn **một** adapter so với model gốc
(Base ↔ adapter), trong khi V2 cần Base + (1−α)·ΔW_MIN + α·ΔW_GRPO — trộn **hai** adapter. Hai
việc khác hẳn nhau. `--alpha` vẫn cần cho phép kiểm đầu mút, nhưng không dựng được điểm giữa.

⛔ Và cách hiển nhiên nhất thì sai. LoRA có ΔW = scaling·B·A, **tích** chứ không phải tổng, nên
trộn thẳng A với A và B với B **không** cho ΔW đã trộn:

| α | sai số tương đối của cách trộn thẳng A, B |
|---|---|
| 0 | 0 ✅ |
| 0,25 | 44% |
| 0,5 | ⛔ **65%** |
| 0,75 | 37% |
| 1 | 0 ✅ |

⚠️⚠️ **Chỗ hiểm: hai đầu mút vẫn đúng tuyệt đối.** Nên phép kiểm α=0 / α=1 ở bảng dưới sẽ đạt,
bạn yên tâm đi tiếp, mà mọi điểm giữa đều là model **khác** với model bạn định thử. Cả thí nghiệm
V2 sẽ trả lời một câu hỏi không ai hỏi.

⭐ **Cách đúng — GHÉP NỐI theo hạng, chính xác tới sai số máy ở MỌI α** (đã kiểm bằng số): xếp
chồng hai ma trận `A`, ghép ngang hai ma trận `B` đã nhân hệ số, rồi nhân đôi cả `r` lẫn
`lora_alpha` để giữ nguyên scaling = lora_alpha/r:

> B′ = [(1−α)B_MIN | αB_GRPO],  A′ = [A_MIN ; A_GRPO]  ⇒  B′A′ = (1−α)B_MIN A_MIN + αB_GRPO A_GRPO

```python
# harness/noi_suy.py — dung EXACT, khong xap xi. r: 16 -> 32, lora_alpha: 32 -> 64.
import json, os, torch
from safetensors.torch import load_file, save_file

def noi_suy(dir_min, dir_grpo, alpha, dir_ra):
    M = load_file(os.path.join(dir_min,  "adapter_model.safetensors"))
    G = load_file(os.path.join(dir_grpo, "adapter_model.safetensors"))
    assert set(M) == set(G), f"hai adapter khac tap module: {set(M) ^ set(G)}"
    ra = {}
    for k in M:
        a, b = M[k].float(), G[k].float()      # ⛔ ep fp32: MIN bf16, GRPO fp32
        if ".lora_A." in k:
            ra[k] = torch.cat([a, b], dim=0)                    # (2r, in)
        elif ".lora_B." in k:
            ra[k] = torch.cat([(1-alpha)*a, alpha*b], dim=1)    # (out, 2r)
        else:
            raise KeyError(f"khoa la: {k}")
    os.makedirs(dir_ra, exist_ok=True)
    save_file(ra, os.path.join(dir_ra, "adapter_model.safetensors"))
    cfg = json.load(open(os.path.join(dir_min, "adapter_config.json")))
    cfg["r"] *= 2; cfg["lora_alpha"] *= 2      # ⛔ PHAI doi ca hai, giu scaling
    json.dump(cfg, open(os.path.join(dir_ra, "adapter_config.json"), "w"), indent=2)

for al in (0.0, 0.25, 0.5, 0.75, 1.0):         # ⭐ DUNG NAM MUC NAY
    noi_suy("runs/grpo_point/adapter_ref_min",
            "runs/grpo_point/adapter_grpo_point_seed101",
            al, f"runs/noisuy/a{al:.2f}")
```

⚠️ Nếu `cfg` có `rank_pattern` hoặc `alpha_pattern` khác rỗng thì phải nhân đôi cả các giá trị
trong đó, nếu không vài module sẽ giữ scaling cũ và bạn trộn sai một phần mạng.

⭐ **Phép kiểm BẮT BUỘC — phải làm trên CÂU, không trên ĐIỂM.** MIN 60,05 và GRPO 60,07 chênh 0,02
pp ⇒ nạp lẫn hai đầu mút thì điểm không phát hiện được. `runs/grpo_point/README.md:19-20` cảnh báo
đúng bẫy này: *"chấm nhầm nó thì ra lại 60,05"*.

| kiểm | phải ra | đối chiếu với |
|---|---|---|
| α = 1 | câu sinh **trùng từng ký tự** | `runs/grpo_point/preds_grpo_point_seed101.jsonl` ✅ đã commit |
| α = 0 | câu sinh **trùng từng ký tự** | `runs/preds_min_desc_seed101.jsonl` ✅ đã commit |

Hai tệp đối chiếu miễn phí, và phép kiểm này bắt được cả việc đảo hai đầu mút.

### 5.4 ⛔ Luật khai báo — khoá TRƯỚC khi quét

1. Chọn **đúng một α** trên val, ghi vào mục đăng ký **trước khi** chấm test.
2. Chấm test cấu hình đó **VÔ ĐIỀU KIỆN** và báo cùng cả hai đầu mút. ⛔ Không chấm cả năm mức
   trên test rồi khoe mức cao nhất.
3. Nó chỉ thành **tiêu đề** nếu vượt đầu mút trên val ≥ **2,0 pp** (≈ 1,5 × SE ghép cặp). Vì kỳ
   vọng là +0,2…+0,5, gần như chắc chắn **không đạt** ⇒ tiêu đề vẫn **60,07**, và số nội suy vào
   luận văn như **một hàng bảng có thật**, không phải nhan đề.

---

## 6. THƯỚC — đã chốt, đừng mở lại

### 6.1 Chốt

| vai | thước | số của GRPO/101 |
|---|---|---|
| ⭐ **TIÊU ĐỀ** | `exec` = `action_ok` ∧ ±14% ∧ **Voronoi**, niêm `b93e85c` 5/8, trước mọi nhánh khai báo | **60,07** |
| ⭐ **BÁO KÈM** | **D.3** (AndroidControl step-wise: điểm dự đoán nằm trong hộp phần tử vàng) | **67,04** |
| BÁO KÈM | D.3 ∧ ±14% | **62,96** |
| ĐỘ NHẠY | ±14% từng trục (69,37) · AitW Euclid (68,90) · `hit_disk` thuần (69,89) | — |

⛔ **KHÔNG đổi thước tiêu đề sang luật ±14%.** Lý do quyết định là **SÀN**: trên lát 800, câu rỗng
nghĩa (`"Tap the button."`) đạt **12,00** dưới `exec` nhưng **20,50** dưới `d14` ⇒ **86%** mức
tăng của `d14` là thứ câu rỗng nghĩa cũng lấy được, và dải hữu dụng hẹp lại. Còn D.3 thì mở rộng
dải. Thêm nữa, đổi sang `d14` biến **hai phép so trước đó không có ý nghĩa thành có ý nghĩa**
(MIN−S1, GRPO−S1) — đó là đi chợ thước, và hội đồng sẽ thấy.

✅ **D.3 hợp lệ, không phải thước tự đặt:** bài gốc AndroidControl cũng phải tự suy phần tử đích,
và bằng đúng quy tắc của dự án — *"khi nhiều nút thoả, chọn nút có diện tích nhỏ nhất"* (Phụ lục
C.1/D.1 của bài gốc), khớp `harness/descriptor_label_build.py:334`.

⚠️ Khai kèm, không được lược: ⛔ cấm cộng dồn `exec` và D.3 thành một mũi tên — chúng là **hai
luật trên cùng một lượt chạy**, không phải hai mức tăng. ⛔ Cấm gọi 75,73 là *"mức người"*; nói
*"mức mà chính dụng cụ này đạt được khi nhận câu do người viết"*.

### 6.2 ⛔ Chặn cứng của D.3, và công thức dựng lại

`harness/dg1_cache/test_ac/descriptors.jsonl` không có trên kho **VÀ** không còn trên đĩa (mất khi
kho bị xoá và clone lại 7/9). Hệ quả: `exec`, `d14`, AitW, `hit_disk`, `action_ok` đều tái lập
được từ tệp đã commit, nhưng **không một con số D.3 nào tái lập được**.

0. ⛔⛔ **THÊM VÀO `.gitignore` TRƯỚC TIÊN:** `!harness/dg1_cache/test_ac/descriptors.jsonl`
1. `python harness/build_test_data.py` (dựng cache ~8 GB — dù sao cũng phải làm để chấm)
2. ⛔ `python harness/prep_ocr_train.py --split test` — bước hay bị bỏ sót nhất
3. `python harness/descriptor_label_build.py --split test`
4. ⛔ Sửa `harness/luat_d3.py`: thêm vào danh sách `NHANH` (dòng 23–31) một dòng
   `("GRPO-point/101", "grpo_point/score_grpo_point_seed101_raw.jsonl")`
5. `python harness/luat_d3.py` → ghi `runs/luat_d3.json`
6. **Commit** `descriptors.jsonl` và `runs/luat_d3.json`

⛔ Ba bước dễ trượt, mỗi bước làm cả công thức vô ích:

| bước | nếu bỏ qua thì sao |
|---|---|
| 0 | `git add` bỏ qua im lặng; bạn commit xong tưởng đã xong mà remote vẫn không có tệp |
| 2 | `build_test_data.py` chỉ ghi `test.jsonl` (dòng 185) và `images/*.png` (dòng 167) — nó **KHÔNG** sinh `ocr.jsonl`, dù bên trong có chạy OCR. Mà `descriptor_label_build.py:298` đọc `ocr.jsonl` ⇒ bước 3 ném `FileNotFoundError` |
| 4 | `NHANH` hiện chỉ có 8 nhánh và **KHÔNG** có GRPO (`runs/luat_d3.json` hiện tại cũng vậy). Chạy `luat_d3.py` bao nhiêu lần cũng **không** ra hàng GRPO ⇒ không ra 67,04 |

⚠️ Nếu KHÔNG làm được: hạ D.3 xuống **độ nhạy**, để tiêu đề 60,07 đứng một mình với tỉ lệ trần
79,3%. Mất con số 67,04 ở bảng chính, nhưng **không mất tính chính trực**. ⚠️ Thiếu tệp này không
làm sai con số D.3 nào — nó chỉ làm người khác không kiểm được.

---

## 7. SỐ NỀN — để so, và để biết khi nào là "tốt"

| nhánh | `action_ok` | `hit_voronoi` thô | `hit_disk` thô | `exec` | D.3 | D.3∧14% |
|---|---|---|---|---|---|---|
| Base | 96,46 | 48,87 | 57,63 | 47,59 | 53,60 | 49,76 |
| S2/101 | 94,85 | 58,06 | 67,44 | 57,18 | 63,63 | 59,69 |
| `gui_sel`/101 | 90,90 | 57,36 | 66,35 | 56,13 | 62,38 | 58,62 |
| CE2-S2/101 | 98,86 | 59,76 | 68,92 | 59,42 | 66,03 | 62,07 |
| ⭐ **S1/101 — MỐC SO CỦA VIS-SFT** | 94,35 | 60,18 | 69,17 | **59,11** | 65,49 | 61,73 |
| S1/202 (chỉ đổi hạt giống) | 94,58 | 60,58 | 69,77 | 59,62 | 66,10 | 62,36 |
| MIN-DESC/101 | 98,88 | 60,36 | 69,19 | 60,05 | 66,55 | 62,69 |
| ⭐ **GRPO-point/101 — TIÊU ĐỀ** | 98,86 | 60,45 | 69,89 | **60,07** | **67,04** | 62,96 |
| Câu người (trần) | 100,00 | 75,78 | 84,27 | 75,73 | 83,82 | 79,23 |

Hàng sàn (lát 800, mẫu số khác — ⛔ không so trực tiếp với bảng trên): `f1` câu rỗng nghĩa =
**12,00** Voronoi / **20,50** ±14% / **14,12** D.3 · `f3` đúng văn phong sai màn = 6,12 / 12,75 / 8,62.

**Chẩn đoán để nhắm cho đúng:** khoảng cách người − MIN là **+15,53 pp**, và **91%** của nó dồn
vào **29,9%** số bước (lát mô hình **tự khai sai đích**). Trên lát đó câu người cũng giảm
84,36 → 55,72 (−28,64) nhưng mô hình giảm **−73,94** ⇒ **thiếu hụt riêng của mô hình là +45,30 pp**.
⇒ Nút thắt là **tri giác**, không phải diễn đạt — đó là lý do chọn VIS-SFT.

⚠️ **Nhưng hệ số truyền thì nhỏ:** đo bằng chính can thiệp GRPO đã chạy, kênh A **+1,60 pp** chỉ
cho `exec` **+0,045 pp** ⇒ d(exec)/d(A) = **0,028**, thấp hơn tương quan mặt cắt ngang 0,739 **26
lần**. ⛔ Đừng dùng 0,739 làm hệ số quy đổi — đó là cái bẫy chính dự án đã mắc.

---

## 8. SỐ PHẢI KHAI TRUNG THỰC — in cạnh mọi lời hứa

| | |
|---|---|
| ⭐ **0/5** | năm can thiệp đã chi tiền và đã chấm, **không cái nào vượt MDE 2,11**: S2 −1,93 (so S1) · MIN +0,95 (so S1) · CE2 +2,24 (so S2, tổ tiên trực tiếp) · `gui_sel` −2,98 (so S1) · GRPO +0,02 (so MIN, tổ tiên trực tiếp) |
| **P(vượt MDE 2,11)** | **0,30** [0,15 · 0,45] — ⛔ không phải 0,60–0,65 |
| **sàn** | ⛔ không ghim bằng đại số. Đại số chỉ chứng minh *"tập ứng viên có chứa một model bằng đúng mốc xuất phát"*, không chứng minh *"model được chọn trên val sẽ ≥ mốc đó trên test"* — vì thủ tục là argmax trên val. Ghim bằng **LUẬT**: argmax-val chỉ được lấy nếu vượt α=0 ≥ **2,0 pp**, không đạt ⇒ khoá α=0 |
| **nếu nhánh mới ra thấp hơn** | tiêu đề vẫn **60,07**, báo nhánh mới như **kết quả âm**. ⚠️ Để câu đó hợp lệ thì phải báo con số nhánh mới **VÔ ĐIỀU KIỆN** — quyết *sau khi thấy số test* rằng khoe cái nào thì đó đúng là chọn-theo-test |
| ⭐ **luận văn đã bảo vệ được rồi** | `exec` 60,07 · D.3 67,04 · D.3∧14% 62,96 · tỉ lệ trần 79,3% · 8 hướng bị bác bằng phép đo · chẩn đoán hai kênh · hệ số truyền 0,028 so tương quan 0,739. Toàn bộ Phase 0 là 0 giờ GPU. ⇒ **Phase 2 là phần cộng thêm, KHÔNG phải phần chống đỡ** |

---

## Phụ lục A — script tái lập, chạy thẳng

Lưu thành `harness/do_chot_cuoi.py` rồi chạy `python3 do_chot_cuoi.py`, hoặc
`python3 do_chot_cuoi.py <đường_dẫn_kho>`. Chỉ đọc tệp đã commit, 0 giây GPU, ~4 phút CPU.

⛔ **BỐN PHỤ LỤC KHÔNG CÙNG QUY ƯỚC THƯ MỤC** — chạy sai chỗ là `FileNotFoundError`:

| phụ lục | chạy từ đâu | vì sao |
|---|---|---|
| **A** | thư mục **CHA** của kho — hoặc từ trong kho nhưng truyền `.`: `python3 do_chot_cuoi.py .` | dòng 415 mặc định `REPO = "thesis-master"`, tức nó tự nối thêm tên thư mục kho |
| **B · C · D** | **gốc kho** (`thesis-master/`) | chúng dựng đường dẫn tương đối từ `runs/` |

Bốn câu nó trả lời: **A.** điểm mọi nhánh dưới bốn luật chấm + cột `action_ok` · **B.** KTC ghép
cặp cho từng so sánh dưới từng luật + hiệu chỉnh Holm · **C.** phân tách hiệu ứng: bao nhiêu do
**công loại thao tác**, bao nhiêu do **định vị** · **D.** độ phân giải của từng luật (trần − sàn)
và **công trung khi đổi luật**.

> ⚠️ Mã đầy đủ của Phụ lục A ở ảnh **p15–p21**. Các khối đáng chú ý: `LUAT` gồm bốn lambda
> (`exec Voronoi (tieu de)` · `AO × ±14% từng trục` · `AO × AitW Euclid` · `hit_disk KHONG cong`);
> `NH` liệt kê 9 nhánh trỏ vào `runs/*_raw.jsonl`; `SAN` trỏ ba tệp `floor/`; bootstrap cụm tác vụ
> B=4000 + Holm; mục **F** đo lệch bộ trỏ trên màn thật; mục **G** tỉ lệ chuẩn hoá theo trần;
> mục **H** oracle trên các bản diễn đạt lại; mục **I** phép phân định phương pháp cho `gui_sel`.

### A.1 Kết quả mong đợi (đã chạy 7/9/2026)

```
Quan the n=4463 buoc / 1345 tac vu   ·   lat san n=800
  S1/101    action_ok 94.35 · exec 59.11 · AOxd14 67.24 · AOxAitW 66.91 · hit_disk 69.17
  MIN/101   action_ok 98.88 · exec 60.05 · AOxd14 68.72 · AOxAitW 68.32 · hit_disk 69.19
  GRPO/101  action_ok 98.86 · exec 60.07 · AOxd14 69.37 · AOxAitW 68.90 · hit_disk 69.89
  nguoi     action_ok 100.00 · exec 75.73 · AOxd14 84.23 · AOxAitW 84.09 · hit_disk 84.27
  MIN-S1/101    exec +0.94 p=0.0953 –   AOxd14 +1.48 p=0.0128 CO   hit_disk +0.02 p=0.9691 –
  GRPO-S1/101   exec +0.96 p=0.0864 –   AOxd14 +2.13 p=0.0003 CO   hit_disk +0.72 p=0.2138 –
  GRPO-S1/202   exec +0.45 p=0.4365 –   AOxd14 +1.46 p=0.0139 CO   hit_disk +0.11 p=0.8478 –
  S1/202-S1/101 exec +0.52 p=0.1686 –   AOxd14 +0.67 p=0.0926 –    (nhieu hat giong: VO HIEU moi luat)
  MIN-CE2       exec +0.63 p=0.0074 CO  AOxd14 +0.27 p=0.2435 –    (doi luat GIET so sanh nay)
  MIN-S1 duoi d14 +1.48 = CONG thao tac +1.41 + DINH VI +0.07
  GRPO-S1 duoi d14 +2.13 = CONG +1.37 + DINH VI +0.76 | duoi exec +0.96 = CONG +0.67 + DINH VI +0.29
  sua 218 buoc cong, hong 18; trong so da sua: ±14% 52.75%, +Voronoi 40.37%
  D. DAI DUNG DUOC: Voronoi 62.88 · d14 62.50 · AitW 62.75 · D.3 68.88 (rong nhat)
     f2 AN % DAI: Voronoi 89.07% · d14 93.40% (te nhat) · D.3 88.02% (tot nhat)
  MIN-S1 duoi d14 +1.48 = (a) cung dat Voronoi +1.32 + (b) chi nho noi luat +0.16 (10.6%)
  bo Voronoi cong khong cho S1/101: +8.13 pp
    'trong ±14% ngoai Voronoi': S1 363 buoc 8.13pp · MIN 387 8.67pp · GRPO 415 9.30pp, mat 0
    => CUNG TAP voi tran 1825 x <=24% <= 9.81 pp  => cong don la DEM MOT TAP HAI LAN
  F. lech bo tro (px, tren buoc action_ok dung ma exec truot):
    S1/101   n=1569 p25=223 tv=426 p75=867 · 76.9% NGOAI han ±14%
    MIN/101  n=1728 p25=242 tv=435 p75=835 · 77.6% NGOAI
    GRPO/101 n=1726 p25=223 tv=418 p75=818 · 76.0% NGOAI
    nguoi    n=1080 p25=138 tv=285 p75=456 · 64.9% NGOAI
  G. % TRAN DUNG CU (MIN): Voronoi 79.29 · D.3 79.39 (bat bien, trung 0.10 pp)
     d14 81.59 · hit_disk thuan 82.11  => d14 PHA tinh bat bien
  H. ORACLE dien dat 76.75 vs nguoi 74.88 => du dia +1.88 pp; cuu 15/201 = 7.46%
  I. ⭐ PHAN DINH PHUONG PHAP (ghep cap tren dung cung tap buoc):
    DAM CHON n=2590 | gui_sel 67.95 · S1 67.37 · MIN 66.80 | gui_sel-S1 = +0.58  (VO HIEU)
    BO CUOC  n=1873 | gui_sel 39.78 · S1 47.68 · MIN 50.72 | gui_sel-S1 = -7.90
    toan tap n=4463 | gui_sel 56.13 · S1 59.11 · MIN 60.05 | gui_sel-S1 = -2.98
    PHAN THUC TE gui_sft_match = 59.44  => THAP HON tran cong bo 65.44 dung 6.00 pp
    => tran 65.44 la NGUY BIEN CHON MAU. BAC phuong an. Tiet kiem 23 h A100.
```

Nếu số nào lệch, kiểm hai chỗ: (a) dòng `bo_qua` phải tính là **trượt** — mọi trường thiếu đọc
thành 0; (b) quần thể giao có đủ **4.463** bước không.

**Không tái lập được từ kho:** mọi con số D.3 cần `harness/dg1_cache/test_ac/descriptors.jsonl`,
mà đường dẫn `harness/dg1_cache/test_ac/` nằm trong `.gitignore` (~8 GB, dựng lại bằng
`harness/build_test_data.py`). Hiện chỉ còn cache `runs/luat_d3.json`, và cache đó **không có hàng
GRPO** — số 67,04 phải đọc từ `report/144:127`. ⚠️ Việc nên làm: dựng lại cache rồi chạy
`harness/luat_d3.py`, ghi hàng GRPO vào `runs/luat_d3.json` và commit nó.

---

## Phụ lục B — script tái lập các số MỚI của bản 8/9

Lưu thành `phu_luc_b.py` ở gốc kho rồi chạy `python3 phu_luc_b.py`. Chỉ cần `runs/*.jsonl` đã
commit. 0 giây GPU, ~2 phút CPU. Mục A–B dựng phần chẩn đoán ở mục 7 (khoảng cách 15,53 · 91%/29,9%
· hệ số truyền 0,028) · mục C dựng trần ORPO đã bị cắt ở mục 2.1 · mục D–E dựng lập luận SÀN giữ
thước tiêu đề ở mục 6.1 (sàn 12,00 so 20,50 · 86% · phép kiểm đi-chợ-thước).

⚠️ Tên mục bên trong docstring của script là tên của bản CŨ (2bis, 3.2bis, 6.3) — bản dài 3.580
dòng đã được rút gọn. Bảng ánh xạ: `2bis.1–2bis.3` → mục 7 · `2bis.4` → mục 7 (đoạn hệ số truyền)
· `6.3` → mục 2.1 · `3.2bis` → mục 6.1 và 6.2.

> ⚠️ Mã đầy đủ ở ảnh **p22–p26**. Điểm cần nhớ khi chép lại: `CHIA = 1000.0` (thang toạ độ tự khai
> trong `<desc>` là 0–1000, **không phải pixel**); `tu_khai()` bắt `<point>x,y</point>` từ trường
> `raw` của `runs/preds_*.jsonl`; kênh A = `d14(tu_khai(...), gold_xy, wh)`, kênh B =
> `d14(pred_xy, gold_xy, wh)`.

### B.1 Kết quả mong đợi (đã chạy 8/9/2026)

```
n = 4442
A. CHAN DOAN HAI KENH
   kenh A (mo hinh tu khai) = 70.10%      kenh B (UGround doc cau) = 69.36%
   lat            n      MIN      S1    nguoi
   A DUNG      3114    82.37   74.18    84.36
   A SAI       1328     8.43   24.47    55.72
   khoang cach nguoi - MIN toan tap = +15.53 pp, phan bo:
     lat A DUNG  ty trong 70.1%  gop  +1.40 pp (  9.0%)
     lat A SAI   ty trong 29.9%  gop +14.14 pp ( 91.0%)

B. HE SO TRUYEN NHAN QUA
   n = 4437   d(kenh A) = +1.60 pp   d(exec) = +0.045 pp
   ⭐ he so truyen THUC NGHIEM = 0.028   (so voi tuong quan mat cat ngang 0,739)
   o cheo A(MIN) x A(GRPO)     n      MIN    GRPO   chenh
   giu DUNG                 2997    83.08   82.95   -0.13
   giu SAI                  1143     6.91    6.30   -0.61
   SAI -> DUNG               184    17.93   58.15  +40.22
   DUNG -> SAI               113    62.83    8.85  -53.98
   ⭐ can 243 lan lat SACH (= 18.3% lat A-sai), KHONG kem lat nguoc, de vuot MDE 2,2
     GRPO da lat duoc 184 buoc = 13.9% lat A-sai  nhung kem 113 lan lat nguoc

C. TRAN CHO ORPO TANG CAU
   MIN/101 toan tap = 60.27
   thay S1 tren TOAN lat A-sai      =  65.06   (+4.80 pp)
   thay CAU NGUOI tren lat A-sai    =  74.40  (+14.14 pp)
   tin hieu cap :  647 buoc A-sai co MIN=0 & nguoi=1 = 14.57 pp
   rui ro xao tron: 318 buoc A-dung co MIN=1 & S1=0  =  7.16 pp

D. SAN va DO PHAN GIAI tung luat        n = 800
   luat            GRPO    tran    SAN    DAI  san/tran
   exec Voronoi   59.38   74.88  12.00  62.88     16.0%
   AO x d14       69.25   83.00  20.50  62.50     24.7%
     -> diem +9.88 pp nhung SAN +8.50 pp ==> 86% muc tang la thu CAU RONG NGHIA cung lay duoc
   AO x AitW      68.88   82.88  20.12  62.75     24.3%
     -> diem +9.50 pp nhung SAN +8.12 pp ==> 86% muc tang la thu CAU RONG NGHIA cung lay duoc

E. PHEP KIEM DI-CHO-THUOC (bootstrap ghep cap theo cum episode, B=3000)
   --- exec Voronoi ---
     MIN  - S1/101   +0.95  KTC95 [ -0.14 ·  +2.06]  TRANG
     GRPO - S1/101   +0.97  KTC95 [ -0.09 ·  +2.06]  TRANG
     GRPO - MIN      +0.02  KTC95 [ -0.62 ·  +0.59]  TRANG
   --- AO x d14 ---
     MIN  - S1/101   +1.51  KTC95 [ +0.39 ·  +2.62]  loai 0
     GRPO - S1/101   +2.16  KTC95 [ +0.99 ·  +3.32]  loai 0
     GRPO - MIN      +0.65  KTC95 [ -0.02 ·  +1.29]  TRANG
```

⚠️ **Ba chỗ dễ vấp khi tái lập:** ① điểm mô hình **tự khai** nằm ở trường `raw` của
`runs/preds_*.jsonl`, **không** có trong `runs/score_*_raw.jsonl` — phải nạp cả hai tệp và ghép
theo `(episode_id, step_id)`. ② thang toạ độ trong `<point>` là **0–1000**, không phải pixel (chia
1000 cho sai số chuẩn hoá trung vị 0,0194; coi là pixel cho 0,3478 — lệch 18 lần). ③ mục D phải
lấy **giao rộng hơn** tập của mục A–C (mục D không cần `<desc>`), nếu không n rơi xuống 796 và mọi
số lệch ~0,3 pp so với lát 800 chuẩn. Mục A–C dùng n = **4.442** (bước có `<desc>` đọc được) chứ
không phải 4.463 của bảng ở mục 7; chênh 21 bước là các bước `<desc>` hỏng hoặc thiếu `<point>`.

---

## Phụ lục C — script TỰ PHẢN BIỆN trần phương pháp

Lưu ở gốc kho, chạy `python3 phu_luc_c.py`. Chỉ cần `runs/*.jsonl` đã commit. ~5 giây.

⭐ **Đây là script quan trọng nhất về mặt phương pháp luận trong cả hồ sơ.** Nó bắt được một trần
mà chính file này vừa viết ra ở bản nháp. Trước khi tin BẤT KỲ trần nào suy từ một lát chọn theo
hành vi mô hình, hãy chạy lại nó với ít nhất một định nghĩa lát khác.

Nghi vấn: lát được định nghĩa bằng chính kênh A CỦA MIN. Kênh A và câu của MIN đến từ **CÙNG một
lượt suy luận** ⇒ chia **NHIỀU CHUNG**. Chọn bước có A(MIN) sai là chọn bước MIN *"có ngày xấu"*,
nên MIN bị thiệt một cách hệ thống khi so với S1 trên lát đó. Đây đúng là bẫy collider đã giết
`gui_sft_match` (trần 65,44 → thật 59,44).

Ba phép kiểm: ① đổi sang lát định nghĩa bằng A của **GRPO** (không phải MIN) → bớt chọn trực tiếp
· ② lát định nghĩa bằng độ khó **đọc lập với mô hình** (`n_buttons`) → không chọn theo mô hình ·
③ phép thử đối xứng: nếu chọn lát theo lỗi của S1 thì MIN có *"thắng ngược"* không?

### C.1 Kết quả mong đợi (đã chạy 8/9/2026)

```
n = 4437
  lat                                        n     MIN      S1  S1-MIN   nguoi  tran ORPO
  A(MIN) sai  [CACH DANG DUNG - nghi thien vi]  1327    8.44   24.49  +16.05   55.69     +4.80
  A(GRPO) sai [bot chon truc tiep tren MIN]     1256   11.94   22.13  +10.19   54.70     +2.88
  A(GRPO) sai VA A(MIN) DUNG [khong chon MIN do] 113   62.83   34.51  -28.32   60.18     -0.72
  30% man DONG NUT nhat [doc lap mo hinh]       1331   58.53   56.35   -2.18   73.55     -0.65

  tran ORPO dinh nghia bang A(MIN)  = 65.04  (+4.80 pp)
  tran ORPO dinh nghia bang A(GRPO) = 63.13  (+2.88 pp)
```

**Đọc kết quả:** cột `tran ORPO` giảm từ +4,80 xuống +2,88 rồi xuống âm tuỳ cách định nghĩa lát —
trong khi cột `nguoi` gần như không đổi (55,69 · 54,70 · 60,18 · 73,55, chỉ đổi mạnh ở hàng cuối
vì lát đó dễ hơn hẳn). Đó là chữ ký của hiệu ứng chọn mẫu: cái trôi theo định nghĩa lát là **ưu
thế giữa hai mô hình cùng họ**, còn **dư địa so với người thì đứng yên**.

⚠️ Phép kiểm 3 trong script (chọn lát theo kênh B) ra **0,00** cho nhánh bị chọn — đó là kết quả
tất định, không phải phát hiện: kênh B sai thì `exec` bằng 0 theo định nghĩa. Nó chỉ để minh hoạ
giới hạn cực đoan của hiệu ứng, đừng trích nó như bằng chứng.

---

## Phụ lục D — `<desc>` đổi thì CÂU có đổi không

Lưu ở gốc kho, chạy `python3 phu_luc_d.py`. Chỉ cần `runs/preds_*.jsonl` đã commit. ~3 giây.

⭐ **Vì sao phụ lục này vẫn còn dù nhánh ORPO đã bị cắt:** nó là bằng chứng cho việc cắt. Mọi lượt
học ưu tiên trước đây giữ câu giống hệt nhau ở hai vế so sánh và chỉ đổi trường `<desc>` — mà
`<desc>` bị cắt trước khi chấm. Nên hàm mất mát chưa bao giờ so hai CÂU khác nhau. Script đo trực
tiếp: đổi `<desc>` thì **66,67%** số bước câu **không nhúc nhích một ký tự**. ⇒ Nếu có ai đề nghị
*"làm học ưu tiên tầng câu"* thì đây là con số phải đọc trước, và mục 2.1 là quyết định đã chốt.

### D.1 Kết quả mong đợi (đã chạy 8/9/2026)

```
n = 4463
  <desc> KHAC nhau            :  1950  (43.69%)
  rieng o <point> KHAC nhau   :  1489  (33.36%)
  CAU khac nhau               :   961  (21.53%)

  Trong 1950 buoc <desc> da khac:
    -> CAU van Y HET          :  1300  (66.67%)
    -> CAU cung doi theo      :   650  (33.33%)

  [doi chieu] MIN vs S1: CAU khac nhau 4280/6958 = 61.51%
```

**Đọc cho đúng.** Con số 66,67% là *"trong số bước ĐÃ đổi khai báo, bao nhiêu phần trăm giữ nguyên
từng ký tự của câu"* — **không phải** *"đổi khai báo ở 66,7% số bước"*. Khai báo đổi ở **43,69%**
số bước. Hai bản trước của file này ghi lẫn hai đại lượng đó.

Ba cách đọc bảng, cả ba đều đúng và cần nói cùng lúc:

1. `<desc>` **có** ảnh hưởng tới câu — một phần ba số lần đổi khai báo thì câu đổi theo. Nói *"câu
   luôn giống nhau bất kể khai báo"* là sai.
2. Ảnh hưởng đó **yếu** — hai phần ba số lần câu không nhúc nhích một ký tự. Đối chiếu: đổi hẳn
   công thức train (MIN so S1) thì câu đổi ở **61,51%** số bước.
3. Và đây mới là điều quan trọng: **hàm mất mát chưa bao giờ so hai CÂU khác nhau.** Nó không thể
   dạy *"câu này tốt hơn câu kia"*; nó chỉ dạy *"khai báo này tốt hơn khai báo kia"*. Đây là mệnh
   đề về **cách dựng dữ liệu huấn luyện**, độc lập với việc khai báo có lái được câu hay không lúc
   suy luận.

⚠️ **Không quy nhân quả từ bảng này.** GRPO khác MIN ở **toàn bộ** trọng số, nên 650 bước câu đổi
**không** chứng minh là **do** khai báo đổi. Phép tách sạch: lấy một checkpoint duy nhất
(MIN/101), ép sẵn phần `<desc>` ở đầu chuỗi sinh — lần một ép khai báo của MIN, lần hai ép khai
báo của GRPO — rồi để model sinh nốt phần câu. Câu đổi ⇒ khai báo **có điều khiển** câu; câu không
đổi ⇒ `<desc>` chỉ là vật trang trí và mọi can thiệp tầng khai báo đều vô ích. ~2–3 h T4, 0 đồng,
và **không cần train gì**. ⚠️ Đây là việc tuỳ chọn để hiểu cơ chế — nó **không** nằm trong
checklist §1 và **không** chặn việc gì.

---

## Phụ lục E — BẢNG SỐ ĐÃ SỬA (đối chiếu nếu ai đọc bản cũ)

Bản trước file này (3.580 dòng, 7–8/9) có các số sau sai. Số đúng đã được áp thẳng vào thân bài;
bảng này chỉ để đối chiếu, ⛔ đừng chép lại cột giữa.

| chỗ | bản cũ ghi | ✅ số đúng | cách xác minh |
|---|---|---|---|
| câu người trên lát A-đúng → A-sai | 84,37 → 55,69 | **84,36 → 55,72** | Phụ lục B mục A |
| người giảm trên lát A-sai | −28,68 pp | **−28,64 pp** | 84,36 − 55,72 |
| mô hình giảm trên lát A-sai | −73,91 pp | **−73,94 pp** | 82,37 − 8,43; tự mâu thuẫn với bảng ngay trên nó ở bản cũ |
| thiếu hụt riêng của mô hình | +45,23 pp | **+45,30 pp** | 73,94 − 28,64 |
| Δ(MIN − S1) | +0,94 | **+0,95** | 60,265646 − 59,320126 = 0,9455 |
| giá chấm 200 ứng viên | ~70–110 h T4 | **~390 h T4** | 200 × 1,95 h |
| lưới 25 ứng viên | ~8–14 h T4 | **~49 h (val 1.000) / ~20 h (val 400)** | 25 × đơn giá |
| cỡ adapter | ~40 MB | **59,9 MB** (fp32 — LLaMA-Factory upcast trainable) | `report/110:772`, đã đo |
| thư mục `grid/` 40 bản | ~1,6 GB | **~2,4 GB; ~3,3 GB nếu bật LoRA thị giác** | phép nhân |
| tổng số bước | ~8.070 | **8.072** | `ceil(64567/16)×2` |
| P(vượt MDE) | 0,60–0,65 | **0,30** [0,15 · 0,45] | không hiệu chuẩn được ở mức cũ |
| P(nhánh ra thấp hơn tiêu đề) | ≈ 0 | **≈ 0,47** dưới giả thuyết không | argmax trên 21 ứng viên |
| kỳ vọng quét α | +0,5…+1,0 | **+0,2…+0,5** (có thể 0) | WiSE-FT báo lợi **dưới dịch chuyển phân phối**; đây chọn trên val cùng phân phối |
| bảng "0/5" | trộn ba mốc so, không khai mốc | **khai mốc từng hàng** (mục 8) | CE2 +0,63 cũ không khớp mốc nào — nó là MIN−CE2 |
| trần nội suy MIN↔GRPO | 61,47 | **61,44** (đủ ô: 61,69) | 113 × 53,98 / 4437 |

⚠️ Hai chỗ trông như lỗi nhưng KHÔNG phải — đừng "sửa": **55,72 so với 55,69** cả hai đúng, khác
mẫu số (mục 7 dùng n=1.328 ⇒ 55,72; Phụ lục C dùng n=1.327 ⇒ 55,69).
