# 116 — Bản chép lại `FINAL_SOLUTION.md` (phiên debate đa-agent 23/8/2026)

> ⛔ **CẬP NHẬT 23/8, cùng ngày:** phần *"sẽ train gì"* của tài liệu này (Mục 10–17, phương án
> MIN-ORPO tầng câu từ S1) **đã bị `report/117` thay**. Lý do đo được: eligibility tầng câu chỉ
> **26,40%** trên đủ 41.099 bước — sát cổng 25% và đó mới là cận trên. Phương án đang chạy là
> **MIN-DESC**, cặp ở tầng khai báo, eligibility **55,61%**.
> Phần **chẩn đoán** (Mục 0–9) và **phần nền** của file này vẫn đúng và vẫn dùng.

> **Nguồn:** 27 ảnh chụp màn hình do user gửi (`Phương Uyên [23-08-2026 20_27].zip`), chụp trên
> máy Mac chạy Cursor, tài liệu gốc tên `FINAL_SOLUTION.md`, ngày chốt ghi trong file là
> **23/08/2026**. Ảnh đã sắp lại theo đúng thứ tự nội dung ở `report/anh_debate_23_8/`
> (tên `NN_gocXX.jpg`: `NN` = thứ tự tài liệu, `XX` = số thứ tự gốc trong file zip — hai thứ tự
> này **không trùng nhau**, ảnh trong zip bị xáo).
>
> ⛔ **Kho này KHÔNG có `FINAL_SOLUTION.md`, cũng không có `report/115_PHUONG_AN_TD_ROI_DA_RUT.md`.**
> Phiên debate chạy trên một bản checkout khác. File 116 này là bản chép lại duy nhất trên máy WSL.
>
> Phần **đánh giá của trợ lý** (kiểm chứng từng khẳng định bằng mã + phán quyết về hướng đi)
> nằm ở cuối file, mục **Phụ lục A**.

---

## Bản đồ ảnh → nội dung

| # | ảnh | nội dung |
|---|---|---|
| 01 | `01_goc24.jpg` | Tiêu đề · Cách đọc · Nền 1 — Bài toán |
| 02 | `02_goc25.jpg` | Nền 1 (tiếp) · Nền 2 — Model, đầu vào thật, bốn nhánh |
| 03 | `03_goc03.jpg` | Nền 2 (tiếp) · Bốn hệ được chấm · Nền 3 — Thước đo executability |
| 04 | `04_goc01.jpg` | Nền 3 (tiếp) · Ba giới hạn của thước · Nền 4 — Trạng thái |
| 05 | `05_goc07.jpg` | Điểm chính thức · Vì sao ba mẫu số · Nền 5 — Bản đồ repo |
| 06 | `06_goc05.jpg` | Tài liệu nền · Những thứ KHÔNG có trong repo · Đường khôi phục dữ liệu |
| 07 | `07_goc14.jpg` | Nền 6 — Từ vựng dùng xuyên suốt |
| 08 | `08_goc12.jpg` | Nền 7 — Phiên chốt 23/8 đã làm gì |
| 09 | `09_goc17.jpg` | Mục 0 — Kết luận · Mục 1 — Mẫu số 4.463 |
| 10 | `10_goc11.jpg` | Mục 1 (tiếp) · Mục 2 — Đại lượng đăng ký trước chưa có kết quả |
| 11 | `11_goc23.jpg` | Mục 3 — Task tuyên bố ≠ task mã đang chạy |
| 12 | `12_goc20.jpg` | Mục 4 — Những bằng chứng còn giữ được |
| 13 | `13_goc19.jpg` | Mục 5 — "Cam kết cứng" chưa được chứng minh · Mục 6 — Sparse/dense |
| 14 | `14_goc22.jpg` | Mục 6 (tiếp) · Mục 7 — Các dự báo điểm phải rút |
| 15 | `15_goc21.jpg` | Mục 8 — Metric phải mô tả chính xác · Mục 9 — Gói tối thiểu |
| 16 | `16_goc26.jpg` | Mục 9 (tiếp) · Mục 10 — Quyết định cuối sau hội đồng |
| 17 | `17_goc27.jpg` | Mục 10.2–10.3 · Mục 11 — Tại sao chọn MIN-ORPO |
| 18 | `18_goc10.jpg` | Mục 11.2–11.3 · Mục 12 — Dữ liệu cặp quy chiếu |
| 19 | `19_goc09.jpg` | Mục 12.2 (tiếp) · 12.3 Chống shortcut · 12.4 Eligibility gate |
| 20 | `20_goc04.jpg` | Mục 12.4–12.5 · Mục 13 — Objective và triển khai |
| 21 | `21_goc02.jpg` | Mục 13.2–13.3 · Mục 14 — Nhánh thí nghiệm và metric |
| 22 | `22_goc08.jpg` | Mục 14.1 Các nhánh · 14.2 Ba estimand |
| 23 | `23_goc06.jpg` | Mục 14.3 Primary metric |
| 24 | `24_goc15.jpg` | Mục 14.4 Thống kê · Mục 15 — Cổng GO/STOP, Tuần 1 |
| 25 | `25_goc13.jpg` | Tuần 2 — seed 101 · Tuần 3 — xác nhận |
| 26 | `26_goc18.jpg` | Mục 16 — Novelty và câu được phép viết |
| 27 | `27_goc16.jpg` | Mục 17 — Chỉ dẫn cho chat tiếp theo |

---

# PHẦN NỀN — bối cảnh tự chứa

## Nền 1 — Bài toán *(ảnh 01–02)*

Cho một ảnh chụp màn hình Android, một mục tiêu cấp cao và lịch sử thao tác, model phải sinh một
câu chỉ dẫn cấp thấp bằng tiếng Anh cho **người** đọc, ví dụ `Tap the Search icon at the top right`.

```
Tác tử GUI thường:  ngôn ngữ  → toạ độ
Luận văn này:       màn hình + mục tiêu → ngôn ngữ
```

Câu sinh ra tốt hay không được đo bằng cách đưa cho một **bộ trỏ độc lập** và xem nó có chạm đúng
phần tử không.

⚠️ **Tập kiểm KHÔNG phải app-unseen** — chỗ dễ hiểu sai nhất. `train_config.yaml` nói "chia theo
ứng dụng" nhưng `build_test_data.py` cảnh báo rõ: tập kiểm giữ riêng **theo tác vụ** (0 tác vụ trùng
với train), còn **92% ứng dụng trong test cũng có trong train**. Vì vậy:

- không được mô tả kết quả là "tổng quát hoá sang app chưa thấy";
- đếm trên raw: `app_seen_in_train` = `True` **1.737** bước · `False` chỉ **78** bước · `None`
  **2.648** bước. Trên 78 bước đó S1 đạt 58,97% so với 59,07% ở nhóm đã thấy — chênh lệch vô nghĩa
  ở cỡ mẫu ấy;
- gom cụm khi tính KTC dùng `episode_id` (luật chính) và `app` (sensitivity). Vì 2.648 bước không
  có app, luật `app` **phải có fallback về episode**, và điều đó phải được báo chứ không giấu.

**Quy mô:** test 6.958 bước, trong đó **4.463 bước chạm** là quần thể chấm chính thức. Train
64.567 mẫu.

## Nền 2 — Model, đầu vào thật, bốn nhánh *(ảnh 02–03)*

Model nền `Qwen/Qwen2.5-VL-3B-Instruct`, QLoRA 4-bit NF4 qua LLaMA-Factory.

| tham số | giá trị |
|---|---|
| LoRA | rank 8 · alpha 16 · dropout 0,05 · 7 proj (q,k,v,o,gate,up,down) |
| Đóng băng | vision tower + multimodal projector |
| `cutoff_len` | 2.560 token (ảnh chiếm ~1.272) |
| Batch | 4 × grad-accum 4 = 16 hiệu dụng |
| LR / epoch | 1e-4 · cosine · warmup 0,05 · 2 epoch |
| Precision | bf16, gradient checkpointing |
| Seed | 101 và 202 (mỗi nhánh hai hạt giống) |

**Đầu vào thật** (`build_branch_data.prompt_body()`, dùng lại nguyên vẹn trong `infer_branch.py`):

```
<image>
Mục tiêu: {goal}
Đã làm: {3 bước history gần nhất, nối bằng →}    # bỏ nếu history rỗng
Chữ đọc được trên màn: {tối đa 24 dòng OCR, nối bằng ·}
Viết câu hướng dẫn cho bước tiếp theo.
```

⭐ **Gold action KHÔNG nằm trong prompt.** Nó chỉ dùng để dựng nhãn, dựng toạ độ descriptor và để
chấm. Nhiều tài liệu cũ trong repo nói ngược lại — chúng sai. Hệ quả: toàn bộ lý do tồn tại của
phương án TD-ROI bị rút.

**Bốn hệ được chấm** — mọi nhánh nhận cùng một đầu vào, chỉ khác đích sinh:

| hệ | đích sinh / nguồn câu | vai trò |
|---|---|---|
| base | không tinh chỉnh | sàn |
| S1 | `câu` | baseline SFT trực tiếp |
| S2 | `<desc>…</desc>` + `\n` + `câu` | scaffold: khai báo có cấu trúc rồi mới nói |
| human | câu người viết trong AndroidControl | trần của dụng cụ đo |

Định dạng descriptor của S2: `<desc>{role} | {name hoặc "(no name)"} | <point>{x},{y}</point> | {hint}</desc>`.
Descriptor này sinh tự động từ a11y tree + OCR, **độ chính xác của nó chưa từng được đo** — một
giới hạn then chốt khi diễn giải kết quả S2. Hai nhánh nữa đã dựng dữ liệu nhưng chưa train:
`s2r` (descriptor giả, lấy từ màn khác) và `s2_nopoint` (descriptor thật, bỏ ô toạ độ).

## Nền 3 — Thước đo executability *(ảnh 03–04)*

Định nghĩa ở `harness/metric_exec.py`, hàm `score_step()`:

```
executable = action_ok AND toggle_ok AND hit_voronoi
```

| thành phần | ý nghĩa |
|---|---|
| `action_ok` | lớp thao tác của câu model khớp câu gold, sau khi quy về `tap`/`type`/`scroll`/`long_press`/`navigate_back` bằng `ACTION_MAP` |
| `toggle_ok` | câu model không đảo nghĩa so với gold (on/off, show/hide, mute/unmute…) — kênh toạ độ mù với toggle vì hai trạng thái dùng chung một nút |
| `hit_voronoi` | điểm bộ trỏ trả về phải (a) nằm trong đĩa dung sai τ=0,14 cạnh ảnh quanh gold, **và** (b) gần phần tử gold hơn mọi phần tử khác trên màn |

`hit_disk` (chỉ điều kiện (a)) vẫn ghi ra raw để minh bạch nhưng **không phải headline**: dung sai
14% quá rộng, 63,2% số bước có nút khác nằm trong đĩa, nên câu trỏ nhầm sang nút cạnh vẫn lọt.

Bộ trỏ: chính là `osunlp/UGround-V1-2B`; bộ thứ hai để kiểm chéo là `inclusionAI/UI-Venus-Ground-7B`.
Cả hai đều chưa từng thấy toạ độ đáp án của câu đang chấm.

### Ba giới hạn đã biết của thước — phải nhớ khi đọc mọi con số

1. **Vùng mù 30–80 px:** câu trỏ nhầm sang phần tử cách đích trong dải này chỉ bị thước bắt
   **33,1%** số lần (`harness/exec_injection_v3_results.json`, khoá `det_nut_canh_gan`:
   rate 0,3306, n=121, ngưỡng ≥0,80 → trượt). Để so sánh, nút cạnh xa 80–150 px bị bắt 99,6% và
   nút rất xa 100%. Nghĩa là **mọi "cải thiện" cỡ 1–2 pp đều có thể nằm gọn trong vùng mù này** —
   đó là lý do Mục 14.3 bắt buộc có strict element-identity audit làm veto.
2. **Voronoi chỉ chặt bằng độ đầy đủ của bộ dò phần tử:** bộ dò bỏ sót nút cạnh thì câu trỏ nhầm
   vẫn được cho qua.
3. **Lỗi `navigate_back` đã biết và cố ý không sửa:** `go back` / `press the back button` bị quy về
   `tap` vì `go`/`navigate` đứng trước `back` trong vòng quét. Ảnh hưởng đo được: S1 59,12 → 58,81,
   base 47,60 → 47,40, chênh lệch giữa hai nhánh gần như không đổi. Không chấm lại vì `report/106`
   khoá thước trước khi có điểm; bản vá bật bằng `strict_back=True` và **bắt buộc** dùng cho phép
   kiểm không-gây-hại trên bước không-chạm.

## Nền 4 — Trạng thái: cái gì đã chạy, cái gì chưa *(ảnh 04–05)*

| hạng mục | trạng thái | file bằng chứng |
|---|---|---|
| base, chấm đủ 4.463 | ✅ | `runs/score_base_raw.jsonl` |
| S1 seed 101 và 202 | ✅ | `runs/score_s1_seed{101,202}_raw.jsonl` |
| S2 seed 101 | ✅ | `runs/score_s2_seed101_raw.jsonl` |
| **S2 seed 202** | ❌ **chưa chạy → estimand đăng ký trước chưa hoàn tất** | — |
| Trần người | ✅ | `runs/score_ceiling_human_raw.jsonl` |
| Ba can thiệp sàn (f1 trống, f2 xoá tên, f3 lệch màn) | ✅ | `runs/floor/` |
| Lặp lại trên UI-Venus (2.532 bước) | ✅ | `runs/venus/` |
| s2r, s2_nopoint | ❌ chưa train | — |
| MIN-ORPO (kế hoạch ở Mục 10–16) | ❌ chưa có gì | — |

**Tự kiểm lại trong 5 giây, không cần GPU:**

```python
import json, glob
for f in sorted(glob.glob("runs/score_*_raw.jsonl")):
    rows = [json.loads(l) for l in open(f)]
    ok = sum(bool(r.get("executable")) for r in rows)
    print(f"{f:42s} n={len(rows):5d} exec={ok:5d} = {100*ok/len(rows):.2f}%")
```

Kết quả phải ra đúng: **human 75,73% · S1/202 59,62% · S1/101 59,11% · S2/101 57,18% · base 47,59%**.
Nếu lệch, tin raw, không tin file này.

Trên lát 2.532 bước của listener thứ hai UI-Venus: base 39,06% · S1 48,74% · S2 46,60%. Thứ tự
`S1 > S2 > base` giữ nguyên, nên dấu âm của S2 không phải đặc sản của UGround.

Mỗi dòng raw có: `pred_xy`, `gold_xy`, `wh`, `n_buttons`, `sent`, `gold_instruction`, `action_ok`,
`toggle_ok`, `hit_disk`, `hit_voronoi`, `executable`, `app`, `app_seen_in_train`.

### Vì sao có ba mẫu số 4.463 / 4.462 / 4.461

Một số dòng raw không có các trường chấm, thay vào đó có cờ `bo_qua` — bước mà pipeline chấm bỏ qua.
Cụ thể: cả hai seed S1 bỏ qua bước `(18710, 1)`, còn S2/101 bỏ qua một bước khác `(20011, 2)`.

- **4.463** = toàn bộ, `bo_qua` tính là `exec=0`. **Đây là headline.**
- 4.462 = bỏ dòng `bo_qua` của một nhánh.
- 4.461 = giao các dòng đủ trường giữa S1 và S2.

⛔ Đừng dùng 4.461/4.462 cho headline: loại bước mà chính model làm hỏng là **complete-case
analysis**, nó xoá thất bại khỏi tử số lẫn mẫu số. Mã đọc raw phải dùng `r.get("executable")` chứ
không `r["executable"]`, nếu không sẽ `KeyError` đúng ở những dòng này.

## Nền 5 — Bản đồ repo và những gì KHÔNG có trong repo *(ảnh 05–06)*

| file | vai trò |
|---|---|
| `harness/metric_exec.py` | định nghĩa thước — nguồn sự thật của mọi con số |
| `harness/score_run.py` | chạy bộ trỏ, ghi `runs/score_*_raw.jsonl` |
| `harness/build_branch_data.py` | dựng dữ liệu 4 nhánh; `prompt_body()` = contract đầu vào |
| `harness/infer_branch.py` | sinh câu lúc test; `screen_elements()`, `MAX_ELEMS=40`, cờ `--ceiling` |
| `harness/descriptor_label_build.py` | sinh descriptor tự động; `nearest_other()` là nguồn negative cho MIN-ORPO |
| `harness/make_floor.py` | khuôn dựng can thiệp trên câu người (f1/f2/f3) |
| `harness/train_config.yaml` | cấu hình QLoRA dùng chung mọi nhánh |
| `harness/mde_that.py` | tính MDE — **có lỗi cụm/complete-case**, xem Mục 14.4 |

**Tài liệu nền** (chỉ đọc khi cần kiểm chứng): `report/106_DANG_KY_TRUOC.md` (thắng file này về
estimand S1/S2 đã khoá) · `report/108`, `report/113` (nhật ký kết quả) · `report/114` (prior art) ·
`report/115_PHUONG_AN_TD_ROI_DA_RUT.md` (phương án đã loại, chỉ để audit) · `AGENT_BRIEF.md`,
`README.md`, `CLAUDE.md` (viết trước 23/08/2026, phần "S2 là đóng góp mô hình chính" đã hết hiệu lực).

### ⚠️ Những thứ KHÔNG có trong repo — đọc kỹ trước khi hứa lịch với ai

- **Không có ảnh màn hình.** `harness/dg1_cache/` chỉ còn `test_ac/test.jsonl` (3,3 MB, 6.958 bước
  metadata). Trường `image` trỏ tới `images/…png` không tồn tại ở đây.
- **Không có `ocr.jsonl`, không có `descriptors.jsonl`, không có `train_ac/`.**
- **Không có checkpoint LoRA của base/S1/S2.**

Nghĩa là bước 0 thực tế của bất kỳ chiến dịch huấn luyện nào là **khôi phục dữ liệu dẫn xuất và
xin lại checkpoint S1 từ chủ luận văn**. Nếu không có checkpoint S1 gốc thì `MIN` và `CE2` phải
khởi đi từ một S1 train lại, và điều đó phải được ghi rõ vì nó đổi mốc so sánh.

**Đường khôi phục dữ liệu, theo đúng thứ tự:**

```
python harness/build_train_data.py --check      # kiểm chất lượng ghép trước
python harness/build_train_data.py --shards 3   # → dg1_cache/train_ac/ + ảnh
python harness/build_test_data.py  --shards 9   # → dg1_cache/test_ac/  + ảnh (~8 GB)
python harness/prep_ocr_train.py                # → train_ac/ocr.jsonl
python harness/prep_ocr_train.py --split test   # → test_ac/ocr.jsonl
python harness/descriptor_label_build.py        # → train_ac/descriptors.jsonl
python harness/build_branch_data.py             # → branches/ + dataset_info.json
```

**Hai điểm dễ vấp:**
- Thiếu `ocr.jsonl` **không làm chương trình dừng**. `infer_branch.py` chỉ in cảnh báo rồi chạy
  tiếp với đầu vào thiếu hẳn phần chữ đọc được — khác lúc dạy, và điểm sẽ tụt mà không có lỗi nào
  trong log.
- Số ảnh của một tác vụ thường nhiều hơn số bước đúng một: ảnh màn cuối sau bước cuối, không có
  câu tương ứng, bỏ qua.

## Nền 6 — Từ vựng dùng xuyên suốt file *(ảnh 07)*

| thuật ngữ | nghĩa trong dự án này |
|---|---|
| executability / exec | thước chính, xem Nền 3. Mọi con số % trong file là exec trên 4.463 bước trừ khi nói khác |
| listener / bộ trỏ | mô hình grounding chấm câu: UGround-V1-2B (chính), UI-Venus-Ground-7B (kiểm chéo) |
| descriptor / scaffold | chuỗi `<desc>…</desc>` mà S2 phải sinh trước câu |
| referent | phần tử UI mà câu đang nói tới. "Gọi nhầm referent" = câu mô tả đúng ngữ pháp nhưng trỏ sang phần tử khác |
| SFT | supervised fine-tuning, học cross-entropy trên câu đích. S1 và S2 đều là SFT |
| **CE2 / CE-stage2** | tiếp tục SFT từ checkpoint S1 thêm một chặng nữa, khớp đúng số update và dữ liệu với MIN-ORPO. **Đây là control để quy công**: gain thật của component là `MIN − CE2`, không phải `MIN − S1` |
| ORPO | hàm mất mát ưu tiên theo cặp: giữ SFT trên câu `chosen`, đồng thời đẩy tỉ lệ odds của `chosen` cao hơn `rejected`. Không cần reward model, không cần reference model riêng — đó là lý do nó chạy được trong ngân sách này |
| chosen / rejected | trong một cặp: `chosen` là câu đúng, `rejected` là câu chỉ khác ở danh tính phần tử được quy chiếu |
| estimand | đại lượng cần ước lượng, định nghĩa trước khi nhìn số. Ba estimand của dự án không được trộn |
| đăng ký trước | `report/106` khoá estimand, thước và ngưỡng trước khi có điểm. Sửa thước sau khi thấy điểm là thứ hồ sơ này sinh ra để chặn |
| MDE | minimum detectable effect — ngưỡng quyết định đã khoá (1,67 / 2,78 pp), **không phải** độ phân giải vật lý của thước |
| sàn nhiễu | chênh lệch giữa hai seed của cùng một nhánh (S1/101 vs S1/202 = +0,52 pp, p=0,194). Bất kỳ hiệu ứng nào không vượt rõ sàn này đều không đọc được |
| McNemar | kiểm định cho dữ liệu bắt cặp. Nó **không chứa phương sai huấn luyện** — không thay được seed thứ hai |
| cluster bootstrap | lấy mẫu lại theo episode/app, không theo dòng, vì các bước trong cùng episode tương quan mạnh |
| eligibility gate | điều kiện một bước được phép vào tập cặp huấn luyện (Mục 12.4) |
| GO/STOP gate | điều kiện dừng đã khoá trước, Mục 15. Không được nới sau khi thấy số |
| `bo_qua` | cờ trong raw đánh dấu bước bị pipeline chấm bỏ qua; tính là `exec=0`, không được loại khỏi mẫu số |
| no-harm | phép kiểm trên bước không-chạm (cuộn, gõ, mở app) rằng can thiệp không làm hỏng phần dữ liệu vốn giống hệt nhau ở mọi nhánh. Bắt buộc chạy với `strict_back=True` |

## Nền 7 — Phiên chốt 23/08/2026 đã làm gì *(ảnh 08)*

### Đã tự kiểm số, không trích lại tài liệu

Toàn bộ số headline được tính lại trực tiếp từ `runs/*_raw.jsonl`. Tất cả đều tái lập chính xác:

| kiểm | kết quả |
|---|---|
| Điểm 5 hệ trên 4.463 | khớp đến hai chữ số thập phân |
| McNemar S2−S1/101 | `b/c = 340/254`, −1,927 pp — khớp |
| McNemar S2−S1/202 | `b/c = 353/244`, −2,442 pp — khớp |
| Sàn nhiễu hai seed S1 | `b/c = 132/155`, +0,515 pp — khớp |
| Ngân sách lỗi | 844 bước = 18,91%, tách 590 / 81 / 173 — khớp cả bốn |
| Can thiệp xoá tên | đúng 193 bước, 89,64% → 61,14%, −28,50 pp — khớp |
| Vùng mù thước | 33,06% trên n=121 — khớp |

⇒ **Phần đo lường của luận văn đứng vững. Nếu định phản biện, đừng tấn công vào số; chỗ yếu nằm ở
diễn giải và ở những gì chưa chạy.**

### Sáu phát hiện làm đổi kế hoạch

1. **Mẫu số đúng là 4.463, không phải 4.461.** Ba mẫu số sinh ra từ cờ `bo_qua`, xem Nền 4.
   Complete-case analysis xoá mất chính thất bại của model.
2. **Input contract không khớp mô tả:** nhiều tài liệu nói gold action là đầu vào, nhưng
   `prompt_body()` không hề đưa action vào prompt. Đây là phát hiện phá vỡ toàn bộ phương án TD-ROI.
3. **Estimand đăng ký trước chưa hoàn tất:** thiếu S2 seed 202, nên −2,19 pp nằm trong vùng
   **trắng**, chưa phải kết quả âm. Mục 2 liệt kê rõ câu cấm nói.
4. **Oracle forced-prefix chưa từng được cài đúng:** `--ceiling gold` nối descriptor vào *user
   prompt* chứ không ép prefix phía assistant, nên nó đo side-information chứ không đo "model chỉ
   còn việc diễn đạt". Xem Mục 5.
5. **Tập kiểm không phải app-unseen** (Nền 1) — dễ dẫn tới một claim sai.
6. **`mde_that.py` có lỗi fallback singleton theo bước và complete-case;** phải sửa trước khi phân
   tích, xem Mục 14.4.

### Quy trình đi tới MIN-ORPO

Bốn reviewer Opus 5 độc lập theo vai (kiến trúc, thống kê, triển khai, novelty), một Opus 5 chủ toạ
phản biện chéo, rồi một vòng cuối với bốn họ model khác nhau. Kết quả: **không model nào giữ
TD-ROI**. Ba họ phương án bị loại — TD-ROI (rò target hoặc đổi task), soft candidate router (recall
ứng viên chỉ ~90,6%, dưới cổng 97%), RLTS/latent slots (cần custom trainer, gần prior art). Lý do
chi tiết ở Mục 11.2; toàn văn phương án đã rút ở `report/115`.

### Đã sửa gì trong repo

- Viết lại `FINAL_SOLUTION.md` thành tài liệu tự chứa.
- Chuyển phương án TD-ROI/RLTS sang `report/115_PHUONG_AN_TD_ROI_DA_RUT.md`.
- Cập nhật `AGENT_BRIEF.md`, `README.md`, `CLAUDE.md` để trỏ về file này và đánh dấu câu
  "S2 là đóng góp mô hình chính" là **hết hiệu lực**.

**Không có checkpoint hay số mới nào được tạo trong phiên này.** Trạng thái thực nghiệm vẫn đúng
như bảng ở Nền 4.

---

# PHẦN SỐ — cái gì đứng vững, cái gì không được nói

## 0. Kết luận trong một đoạn *(ảnh 09)*

Phần đo lường và các số thô cơ bản còn đứng. Tuy nhiên, **đại lượng chính đã đăng ký trước chưa
hoàn tất**, vì mới có một seed S2 trong khi hồ sơ yêu cầu hai seed mỗi nhánh. Kết quả hiện tại chỉ
cho phép nói checkpoint `S2/101` thấp hơn hai checkpoint S1; **chưa** được nói giả thuyết chính đã
bị bác bỏ, scaffold nói chung gây hại, hay "cam kết cứng" là nguyên nhân. Có thêm một mismatch
nghiêm trọng: tài liệu mô tả gold action là đầu vào, nhưng mã vận hành không đưa action vào prompt.

Đối với mục tiêu mới — đóng góp một component huấn luyện và chứng minh model cuối tốt hơn — bản
từng chọn TD-ROI đã bị rút. Phương án cuối là **MIN-ORPO**: tiếp tục từ S1 bằng một mục tiêu ưu tiên
theo cặp quy chiếu tối thiểu, giữ nguyên input `ảnh + goal + history + OCR` và không tăng chi phí
inference. Đây là component ở tầng **mục tiêu huấn luyện**, không phải kiến trúc mới. Primary để quy
công là `MIN-ORPO − CE-stage2`; so với S1 chỉ trả lời model cuối có thực sự cho số tốt hơn.
**Không có phương án nào bảo đảm trước kết quả dương**; các cổng ở Mục 10–16 phải được khoá trước
khi xem output mới.

## 1. Sửa số quan trọng nhất: mẫu số chính là 4.463 *(ảnh 09–10)*

**Quy tắc chính thức:** hồ sơ đăng ký trước khoá đối tượng chấm là toàn bộ 4.463 bước chạm.
`score_run.py` ghi câu rỗng vào raw và tính nó là `exec=0`. Vì câu rỗng là một thất bại **do model
sinh ra**, không được loại nó bằng complete-case analysis trong headline.

| mẫu số | nghĩa |
|---|---|
| **4.463** | quần thể chính thức; câu rỗng tính là thất bại. Dùng cho headline |
| 4.462 | loại câu rỗng chung của hai seed S1. Chỉ dùng cho một số chẩn đoán S1–S1 cũ |
| 4.461 | giao các dòng có đủ trường chấm giữa S1 và S2. Chỉ là complete-case diagnostic |

**Điểm chính thức trên n = 4.463:**

| hệ | số đúng | executability |
|---|---|---|
| Human | 3.380 | **75,73%** |
| S1/101 | 2.638 | **59,11%** |
| S1/202 | 2.661 | **59,62%** |
| S2/101 | 2.552 | **57,18%** |
| Base | 2.124 | **47,59%** |

**So sánh checkpoint, vẫn trên 4.463 bước:**
- `S2/101 − S1/101 = −1,927 pp`; McNemar `b/c = 340/254`, exact `p = 0,000477`
- `S2/101 − S1/202 = −2,442 pp`; `b/c = 353/244`, exact `p = 9,35×10⁻⁶`
- Sàn seed S1: `S1/202 − S1/101 = +0,515 pp`; `b/c = 132/155`, `p = 0,194`

Các p-value trên chỉ mô tả các checkpoint đã huấn luyện. Chúng **không chứa phương sai huấn luyện
của S2** và **không thay thế seed S2 thứ hai**.

## 2. Đại lượng đăng ký trước chưa có kết quả *(ảnh 10)*

Estimand đã khoá: `Δ = mean(S2/101, S2/202) − mean(S1/101, S1/202)`.

Hiện chỉ có `S2/101`. So tạm S2/101 với trung bình hai seed S1: `57,18% − 59,37% = −2,19 pp`.

Theo sửa đổi đăng ký trước mới nhất:

| Δ trung bình hai seed mỗi nhánh | cách đọc đã khoá |
|---|---|
| ≥ +2,8 pp và KTC loại 0 | Dương |
| +1,7 … +2,8 pp và KTC loại 0 | Dương yếu |
| −2,8 … +1,7 pp | **Trắng, không kết luận được** |
| ≤ −2,8 pp | Âm |

Do đó **−2,19 pp hiện nằm trong vùng trắng, không phải kết quả âm chính thức.** S2/202 phải khoảng
**≤ 55,95%** thì trung bình S2 mới chạm ngưỡng −2,8 pp, chưa kể phải báo KTC bootstrap theo cụm.

**Câu được phép nói lúc này:**

> Với Qwen2.5-VL-3B QLoRA và pipeline nhãn tự động hiện tại, checkpoint S2/101 thấp hơn S1/101
> 1,93 điểm và thấp hơn S1/202 2,44 điểm trên toàn bộ 4.463 bước. Dấu `S1 > S2` giữ dưới UI-Venus,
> nhưng estimand chính còn chờ S2 seed 202 theo đăng ký trước.

**Câu cấm:**
- "Giả thuyết chính đã bị bác bỏ."
- "S2 gây hại theo đại lượng đăng ký trước."
- "Hiệu ứng lớn gấp 3,7 lần nhiễu nên đã kết luận."
- "McNemar p<0,001 đã bao gồm biến thiên seed."

## 3. Task tuyên bố và task mã đang chạy không giống nhau *(ảnh 11)*

Một số tài liệu mô tả đầu vào gồm ảnh, goal, history **và gold action**. Nhưng
`build_branch_data.prompt_body()` chỉ đưa `ảnh + goal + history + OCR`, và `infer_branch.py` cũng
dựng `rr = {"goal": r["goal"], "history": r.get("history") or []}`.

**Action hiện tại không đi vào prompt.** Nó chỉ được dùng để dựng supervision, descriptor point và
để chấm.

**Task vận hành thật:**
> Từ ảnh, goal, history và OCR, model vừa phải suy ra bước/phần tử tiếp theo, vừa phải diễn đạt
> thành câu.

**Nó không phải:** biết sẵn action vàng rồi verbalize action đó.

**Hệ quả:**
- S1–S2 vẫn so công bằng cho task vận hành hiện tại vì hai nhánh nhận cùng input.
- Nhưng điểm đang gộp hai năng lực: chọn đúng action/phần tử **và** gọi tên/diễn đạt phần tử.
- Human ceiling là trần của listener trên câu người, **không phải trần end-to-end của model** trong
  task hiện tại.

**Cổng quyết định:**
1. Nếu upstream thật sự cung cấp gold action/node ở inference: đổi task rõ thành `action → language`;
   đưa cùng action type + point/node vào **mọi** nhánh; dựng lại direct baseline; không so trực tiếp
   điểm mới với S1 cũ như thể chỉ thay kiến trúc.
2. Nếu upstream không cung cấp action: xoá "gold action là input" khỏi mô tả; tuyệt đối không đưa
   gold coordinate/crop vào model lúc test.

## 4. Những bằng chứng còn giữ được *(ảnh 12)*

### 4.1 UI-Venus
UI-Venus giữ thứ tự `S1 > S2 > Base`. Điều này cho thấy dấu âm không chỉ do UGround. Nhưng đây là
**lặp lại listener, không phải lặp lại huấn luyện S2**. Hai listener còn dùng cùng luật hit, nên
UI-Venus **không đóng vùng mù 30–80 px**.

### 4.2 Can thiệp xoá tên
Trên đúng 193 câu người có cả tên và mệnh đề vị trí:

```
Human nguyên bản: 173/193 = 89,64%
Xoá tên:          118/193 = 61,14%
Hiệu ứng:                  −28,50 pp
```

Đây là bằng chứng nhân quả tốt, nhưng **chỉ cho quần thể 193 bước đó**. Nhóm này rất dễ và không
đại diện cho toàn bộ bước vô danh, câu thứ tự hoặc câu không có mệnh đề vị trí.

- **Câu đúng:** "Trong các câu người có cả tên và mệnh đề vị trí, bỏ tên làm executability giảm
  28,5 điểm."
- **Câu quá mức:** "Tên là bottleneck chi phối toàn bộ task."

### 4.3 Nhãn descriptor
Thống kê hiện có chỉ đo **đầu ra của luật dựng nhãn**: 21,2% không có tên · 7,6% trùng tên · phần
lớn tên đến từ OCR · độ chính xác semantic của role/name/hint **chưa được audit**.

⛔ Không được gọi các descriptor này là "gold"; hiện chúng là **silver labels**. `point` lấy từ gold
click nhưng role/name/hint là heuristic.

### 4.4 Ngân sách lỗi
Trên quần thể chính thức, Human đúng / S1 sai là **844 bước = 18,91%**. Phân cấp kênh:
- action/toggle đúng nhưng trượt dung sai: **590 bước = 13,22 pp**
- trúng dung sai nhưng trượt Voronoi: 81 bước = 1,81 pp
- action/toggle/format/khác: 173 bước = 3,88 pp

Con số 13,22 pp cho thấy dư địa lớn nằm ở element selection/description, nhưng **không tự tách được
lỗi model khỏi lỗi listener**.

## 5. Cơ chế "cam kết cứng" chưa được chứng minh *(ảnh 13)*

Phân tầng theo descriptor đúng/sai do chính S2 sinh là **phân tầng sau xử lý**:

```
E[Y(S2)−Y(S1) | descriptor do S2 sinh đúng/sai]
```

Độ khó và confidence ẩn cùng ảnh hưởng descriptor lẫn outcome. Vì vậy các tầng này dùng được để
phân rã kế toán, **không dùng để nói descriptor sai gây ra thất bại**. Ba tầng dựa trên Human/S1
outcome cũng chỉ là ngân sách rescue, không phải CATE ngoại sinh.

**Phép phân xử đúng:** trên cùng checkpoint S2 và cùng bước, **ép assistant prefix** rồi sinh tiếp
câu, với 6 điều kiện: (1) descriptor đúng đã audit, (2) đúng tên sai point, (3) sai tên đúng point,
(4) neighbor, (5) far random, (6) filler/none cùng token budget. So ghép cặp trong cùng item. Đây
mới là can thiệp nhân quả lên prefix.

**Mã hiện tại chưa làm phép này.** `infer_branch.py --ceiling gold` nối descriptor vào **user
prompt**:

```
Khai báo phần tử đích: <desc>...</desc>
```

Nó không thay descriptor model tự sinh và không ép prefix phía assistant. Do đó nó chỉ đo **oracle
side-information trong input**, không phải "model chỉ sinh câu". Các ngưỡng tuyệt đối 64%/72% từng
được đề xuất không có nền thống kê rõ; nên dùng hiệu ghép cặp và KTC.

## 6. Sparse/dense chỉ là phát hiện thăm dò *(ảnh 13–14)*

Kết quả định tính khá bền: S2/101 mất nhiều nhất ở màn thưa và gần hoà ở màn dày. Tuy nhiên con số
chính xác thay đổi theo mẫu số 4.461 hay 4.463, cách chia tie ở ranh giới quintile, và mô hình
interaction/quy tắc gom cụm. Mật độ còn đồng biến với app, task, tên khả dụng và inventory dùng
trong metric.

- **Chỉ được nói:** "Phân tích hậu kiểm gợi ý bất lợi của S2/101 giảm khi mật độ tăng."
- **Không được nói:** "Cam kết gây hại nhất ở màn thưa" · "Scaffold là chi phí thuần ở mọi mật độ" ·
  "Tương tác mật độ đã được xác nhận."

Muốn kiểm cơ chế cần một interaction test khoá trước, hoặc tốt hơn là cùng target/task nhưng
thêm/bớt distractor có kiểm soát.

## 7. Các dự báo điểm phải rút *(ảnh 14)*

**"Chữa ô thao tác +0,4…0,65 pp"** — 0,65 pp chỉ là phần chênh S1–S2 nằm ở nhóm không có point hợp
lệ theo complete-case diagnostic. Nó không phải gain kỳ vọng của một lượt train.

**"Sửa nguồn tên +0,8…2,0 pp"** — đây là ngoại suy từ can thiệp 193 bước dễ sang nhóm không tên
rộng hơn. Chưa có bằng chứng hai quần thể trùng nhau. Trước khi train phải: audit tên; trên câu
người thử `tên mới / từ chung / tên sai cùng màn`; chấm bằng cả hai listener và strict element
identity. Tên mới không phục hồi rõ trên tầng không tên/trùng tên thì dừng.

**"Mục tiêu 60–62%"** — từ S2 chính thức 57,18%, kể cả cộng cơ học hai đầu trên chưa chạy:

```
57,18 + 0,65 + 2,00 = 59,83%
```

Hai can thiệp còn đụng cùng vùng lỗi nên **không được cộng**. 60–62% chỉ được gọi là mục tiêu kỹ
thuật, không phải dự báo, KTC hay expected result. KTC điểm đơn khoảng ±1,4–1,8 pp không phải tiêu
chuẩn quyết định cho hiệu ghép cặp; dùng KTC của paired Δ và quy tắc 2,8 pp đã khoá.

## 8. Metric phải được mô tả chính xác *(ảnh 15)*

`metric_exec.py` thực hiện:
- `gold` là **điểm chạm**, không mặc nhiên là tâm phần tử;
- `hit_disk` thực ra là **cửa sổ chữ nhật** `|dx| ≤ 0,14W AND |dy| ≤ 0,14H`;
- `hit_voronoi` còn yêu cầu nằm trong cửa sổ trên rồi mới kiểm không có tâm đối thủ được giữ lại
  gần hơn gold touch;
- độ đúng phụ thuộc độ đầy đủ và khử trùng của inventory phần tử.

Vùng 30–80 px chỉ phát hiện khoảng 33% lỗi phần tử cạnh. Vì vậy trước khi tối ưu grounding cần một
**strict element-identity validation audit**: ánh xạ prediction vào target box/equivalence set được
gán tay; tách mẫu ngẫu nhiên toàn tập và mẫu stress-test 30–80 px; hiệu chuẩn sensitivity/false-reject
trên một calibration set adjudicated; chỉ gọi đây là endpoint đã hiệu chuẩn nếu đạt các KTC ở Mục
14.3; dùng nó làm **veto gain giả**, không dùng một audit thiếu power để cứu primary.

⛔ Không đưa UGround/UI-Venus vào train, rerank hoặc chọn output.

## 9. Gói tối thiểu để bảo vệ *(ảnh 15–16)*

**Bắt buộc cho headline:**
1. Chạy S2 seed 202.
2. Báo đủ S1×2, S2×2 trên n=4.463; câu rỗng bằng 0.
3. Tính primary Δ là trung bình hai seed, KTC bootstrap theo cụm đúng quy tắc.
4. McNemar từng checkpoint chỉ là secondary, ghi "conditional on checkpoints".
5. UI-Venus, tolerance sweep và no-harm là robustness, không thay primary.

**Bắt buộc nếu muốn nói về cơ chế:**
1. `s2r` và `s2_nopoint`.
2. Audit phân tầng 200–400 descriptor, hai người, báo riêng role/name/point/hint.
3. Forced-prefix đúng kỹ thuật.
4. Strict element-identity audit cho vùng 30–80 px.

⚠️ `s2r` hiện dùng descriptor của màn khác **và** point ngẫu nhiên, nên vừa khớp độ dài vừa thêm
target nhiễu. Nó chỉ cho biết descriptor thật tốt hơn/xấu hơn descriptor giả, chưa cô lập thuần chi
phí độ dài. Muốn cô lập độ dài cần thêm prefix filler dễ dự đoán, số token đầu ra.

**Hoãn:** dose-response 0/10/25/50% (đắt, nhiều nhãn nhân tạo không giống lỗi thật; "0%" vẫn chưa
phải nhãn sạch) · hard-vs-soft đầy đủ 3–4 tuần · scale 7B · selective prediction · train sửa nguồn
tên trước khi counterfactual tên mới qua cổng.

---

# PHẦN KẾ HOẠCH — component MIN-ORPO

## 10. Quyết định cuối sau hội đồng Opus và đa-model *(ảnh 16–17)*

### 10.1 Đồng thuận và bất đồng
Vòng bổ sung gồm: bốn reviewer Opus 5 độc lập (kiến trúc, thống kê, triển khai, novelty); một Opus 5
chủ toạ phản biện chéo; vòng cuối với Claude Opus 5, Grok, Gemini và GPT.

Bốn model vòng cuối đều kết luận **MODIFY**, không model nào giữ TD-ROI nguyên trạng. Đồng thuận:
1. huỷ TD-ROI trong phạm vi luận văn;
2. không đưa gold action/point vào test;
3. giữ input contract mà S1 đang thực thi;
4. chọn preference optimization bằng cặp quy chiếu tối thiểu;
5. primary quy công phải so với CE-stage2, không phải S1;
6. kiểm eligibility, false-negative và OOM trước GPU;
7. không gọi đây là kiến trúc mới.

Điểm bất đồng lớn nhất là có dùng UI-Venus ở dev hay không. Quyết định cuối chọn phương án nghiêm
hơn: **không dùng UGround hoặc UI-Venus để chọn hyperparameter, checkpoint hay quyết định sửa
model.** UGround chỉ chấm xác nhận cuối; UI-Venus chỉ chấm robustness sau khi mọi cấu hình đã khoá.

### 10.2 Input contract vận hành

```
screenshot + goal + tối đa 3 bước history + OCR
→ đúng một câu chỉ dẫn
```

**Không có ở inference:** gold action type · gold point/node · target crop · a11y candidate list.

Gold action, point và cây a11y chỉ được dùng làm supervision hoặc dựng negative **trong train**.
Đây là contract duy nhất đã được thực thi bởi S1/S2 và có đủ raw score; xác minh lại bằng
`build_branch_data.prompt_body()` và `infer_branch.py` chứ đừng tin mô tả trong bất kỳ ghi chú nào.

Một số ghi chú thiết kế cũ, nằm ngoài repo này, từng dự tính cấp candidate a11y lúc test
(`screen_elements()` và cờ `--b-infer` trong `infer_branch.py`). Nhánh đó **chưa từng chạy**, không
có file kết quả trong `runs/`, nên không được lẫn nó với contract của estimand hiện tại.

### 10.3 Component headline

**Tên làm việc: MIN-ORPO — Minimal Referential-Pair ORPO.**

**Giả thuyết:**
> Tiếp tục huấn luyện S1 bằng các cặp chỉ dẫn cùng màn, trong đó câu bị loại chỉ đổi danh tính phần
> tử được quy chiếu, sẽ làm model ít gọi nhầm phần tử hơn so với tiếp tục huấn luyện CE trên cùng
> dữ liệu và số update.

MIN-ORPO là **training-objective component, không phải architectural module**. Nếu yêu cầu của hội
đồng là bắt buộc có một block kiến trúc mới trong forward pass, phương án này không đáp ứng; không
có block kiến trúc nào vừa novel, sạch và khả thi trong ba tuần được hội đồng bổ sung tìm thấy.

## 11. Tại sao chọn MIN-ORPO *(ảnh 17–18)*

### 11.1 Tín hiệu từ ngân sách lỗi
Ngân sách đã kiểm cho thấy Human đúng / S1 sai là 844 bước; phần action/toggle đúng nhưng trượt
định vị chiếm **590 bước = 13,22 pp**.

Một phân tích từ vựng hậu kiểm của Opus trên nhóm S1 sai gợi ý: khoảng **524/843** câu S1 sai có từ
khớp một phần tử khác; **460/524** còn trượt hẳn cửa sổ dung sai; nhóm này tương đương khoảng
**11,74 pp** toàn tập.

Đây chỉ là proxy hậu kiểm, không phải nhãn nguyên nhân: nó điều kiện hoá trên outcome S1 và phải
được audit bằng node/tên thật. Tuy nhiên nó cho phép ưu tiên một objective chống gọi nhầm referent
hơn một kiến trúc định vị mới.

### 11.2 Vì sao loại ba họ phương án

**TD-ROI** — cần target point/node ở inference trong khi contract đang chạy không có; RoIAlign/
pseudo-token gần Ferret-UI, GPT4RoI và region-conditioned MLLM; loss conditional-likelihood gần MMI
của Mao et al. 2016; Qwen2.5-VL cần xử lý M-RoPE, pseudo-token, save/load và trainer riêng; feature
ROI trên full-screen tokens có thể kém crop vì độ phân giải.

**Soft candidate router** — mã hiện cắt `MAX_ELEMS=40` và ưu tiên node có tên; ước lượng sơ bộ của
Opus: khoảng 74,8% màn có hơn 40 phần tử; recall candidate giải tích chỉ khoảng **90,6%**, dưới cổng
**97%**; giữ đủ candidate có thể vượt `cutoff_len` sau khi trừ visual tokens; chỉ được mở lại khi đo
recall thật sau mọi lọc đạt ít nhất 97%.

**RLTS/latent slots** — cần custom trainer, spatial/action heads và residual gate; gần
object-query/action-head prior art như GUI-Actor; không có bằng chứng latent commitment tốt hơn hard
commitment; rủi ro và thời gian cao hơn MIN-ORPO.

### 11.3 Điều MIN-ORPO không bảo đảm
`+2,8 pp` là khoảng **125 ca đúng ròng**. Component phải sửa được nhiều ca gọi nhầm mà không phá câu
đang đúng. S2 đã cho thấy một can thiệp có thể tạo cả rescue và regression lớn. **Không được ghi
MIN-ORPO là "expected +X pp" trước khi chạy.**

## 12. Dữ liệu cặp quy chiếu *(ảnh 18–20)*

### 12.1 Chosen
`y+` là gold instruction của người, đúng đích đã dùng cho S1. Chỉ dùng một bước để dựng cặp nếu xác
định được chắc chắn span quy chiếu trong `y+`. Việc descriptor có tên là **không đủ**; tên hoặc alias
phải thực sự xuất hiện trong câu sau chuẩn hoá.

### 12.2 Rejected
`y−` phải **đổi danh tính quy chiếu**, không chỉ thay một token trong khi giữ mệnh đề vị trí vẫn trỏ
đúng target.

**MVP chỉ nhận name-based pair, 9 điều kiện:**
1. target có tên/alias xuất hiện chắc trong `y+`;
2. chọn một phần tử khác cùng màn, actionable, action-compatible và cùng/gần role để là distractor thật;
3. khác target-equivalence set; loại parent/child và các đường bấm cùng hành động;
4. khoảng cách tâm tương đương **80–350 px** trên ảnh rộng 1080;
5. tên target và negative khác nhau sau chuẩn hoá;
6. cả hai tên có bằng chứng hiển thị từ OCR/a11y đã audit;
7. nếu câu có mệnh đề vị trí khoá vào target, thay bằng mệnh đề tương ứng của negative hoặc bỏ item;
   không để rejected vẫn trỏ target;
8. giữ nguyên action verb, toggle polarity, typed content và direction;
9. độ dài chosen/rejected lệch không quá 2 token.

**Không dùng trong MVP:** đảo trái/phải, trên/dưới bằng regex mù · negative từ màn khác làm nhánh
full · phần tử cách dưới 80 px · cặp trùng tên · target vô danh không có span quy chiếu chắc.

Target vô danh được giữ trong CE mixture, nhưng không ép tạo preference pair. On-policy rejected từ
lỗi thật của S1 là hướng dài hạn nếu eligibility quá thấp, không tự động chuyển trong cùng chiến dịch.

### 12.3 Chống shortcut
**Trước train phải:** cân bằng để một tên không chỉ xuất hiện ở vế rejected; loại cặp mà lexical
overlap với goal/history chỉ có ở một vế; chạy text-only preference probe; chạy shuffled-image/OCR
probe; kiểm một classifier chỉ dùng độ dài/geometry không phân biệt chosen-rejected; audit mù tối
thiểu 300 cặp, false-negative dưới 5%.

**Ngưỡng shortcut:**
```
text-only hoặc shuffled-image preference accuracy
không được cao hơn 55% một cách rõ ràng
```
Nếu vượt, dữ liệu cặp đang có shortcut và phải **STOP trước GPU**.

### 12.4 Eligibility gate
Đo trên train trước khi tạo model:
```
eligible_pairs / touch_steps ≥ 25%
```
Đồng thời báo coverage theo: tên OCR · tên a11y/content description · duplicate name · app ·
seen/unseen · khoảng cách negative.

Nếu dưới 25%, MIN-ORPO name-based **không có đủ support để làm headline**. Không hạ ngưỡng sau khi
biết số.

### 12.5 Giữ prior thao tác
Preference pair chủ yếu là bước chạm. Stage-2 phải trộn bước không-chạm ở dạng CE thuần theo tỷ lệ
tự nhiên của train, **giống nhau giữa MIN-ORPO và CE-stage2**. Nếu không, model có thể tiếp tục lệch
action prior như tín hiệu đã thấy ở S2.

## 13. Objective và triển khai *(ảnh 20–21)*

### 13.1 Loss
Với prompt `x`, chosen `y+`, rejected `y−`:
```
L = L_SFT(y+)
  + β · [−log σ(log_odds(y+|x) − log_odds(y−|x))]
```

**Mặc định khoá:** `pref_loss: orpo` · `β = 0,1` · một rejected mỗi chosen · stage-2 tối đa **800
optimizer updates** · final checkpoint, không chọn best checkpoint bằng listener.

Không quét β, số negative hoặc checkpoint trên test. Nếu smoke cho thấy cấu hình kỹ thuật bất khả,
sửa phải được ghi trước khi tạo output xác nhận.

### 13.2 LLaMA-Factory gate
ORPO đa phương thức chỉ được coi là khả thi sau các kiểm tra:
1. pin SHA/version LLaMA-Factory;
2. dùng `stage: dpo`, `pref_loss: orpo`, dataset `ranking: true`;
3. xác minh trường `images`, `chosen`, `rejected` sau tokenize;
4. nối từ đúng adapter/checkpoint S1; kiểm save/load ở tiến trình mới;
5. batch GPU bắt đầu bằng 1, gradient accumulation để giữ effective batch;
6. smoke 20 bước, rồi 200 cặp dài nhất;
7. kiểm NaN, OOM và việc Liger/fused loss có tương thích đường pairwise;
8. in cấu hình runtime thật: beta, số pair, số CE-only, số update;
9. `chosen != rejected` sau mọi chuẩn hoá/tokenization;
10. resume sau checkpoint phải giữ cả optimizer và adapter.

**Nếu không qua smoke 200 cặp dài nhất trên phần cứng mục tiêu: STOP.** Không fork custom
pseudo-token trainer để cứu.

### 13.3 Không dùng listener trong vòng train
Cấm dùng UGround/UI-Venus để: chọn β · chọn checkpoint · chọn negative · rerank hoặc chọn output ·
quyết định sửa câu · lặp nhiều cấu hình rồi lấy số đẹp.

Held-out stage-2 dev chỉ dùng: CE/log-odds loss · preference accuracy · action/toggle parser không
cần grounder · kiểm sinh cơ học và shortcut.

## 14. Nhánh thí nghiệm và metric *(ảnh 21–23)*

### 14.1 Các nhánh

**S1** — S1/101 và S1/202 đã có; dùng làm mốc system-level, không phải control quy công stage-2.

**CE2** — tiếp tục từ cùng checkpoint S1; CE trên chosen và cùng CE-only non-touch mixture; cùng data
support, optimizer updates, LR schedule và seed với MIN-ORPO; hai seed 101/202.

**MIN** — MIN-ORPO đầy đủ; hai seed 101/202.

**RAND** — ORPO với negative ngẫu nhiên nhưng qua cùng equivalence/filter cơ bản; khớp số pair,
eligibility, beta và update; một seed, chỉ giải thích vai trò hard/minimal negative; muốn claim thống
kê `MIN > RAND` thì phải chạy seed thứ hai.

Không cần train shuffled-screen full arm nếu text-only/shuffled probes đã bắt shortcut.

### 14.2 Ba estimand không được trộn

**Primary component attribution:**
```
Δ_component = mean_2seed(MIN − CE2)
```
Đây là con số trả lời preference component có hơn tiếp tục CE hay không.

**Secondary system gain:**
```
Δ_system = mean_2seed(MIN − S1)
```
Đây là con số trả lời model cuối có tốt hơn hệ mạnh nhất hiện có hay không. Nó gộp cả tác dụng
stage-2/extra optimization nên **không được dùng một mình để quy công cho component**.

**Mechanism:**
```
Δ_hard = MIN − RAND
```
Một seed chỉ là exploratory.

Mục tiêu của người dùng chỉ đạt khi **cả** `Δ_component` **và** `Δ_system` dương theo điều kiện ở
Mục 14.4.

### 14.3 Primary metric
Không sửa `metric_exec.py`:
```
UGround Executability@Voronoi
 = action_ok AND toggle_ok AND hit_voronoi
```
- đủ 4.463 bước chạm;
- câu rỗng/listener fail = 0;
- kiểm khoá tuyệt đối bốn tệp output có cùng `(episode_id, step_id)`;
- `strict_back=True` cho họ nhánh mới, báo riêng nếu điều này khác báo cáo cũ;
- một lần chấm sau khi checkpoint/config đã đóng băng.

**Strict element identity:** calibration bằng lỗi bơm có kiểm soát, tách khỏi outcome audit;
random-300 và hard-100 ở dải 30–80 px; hai người mù nhánh nếu có thể, nếu không, khai một người +
adjudication/intra-rater; KTC nhị thức cho sensitivity và false-reject; làm **veto gain giả**, không
dùng để cứu primary.

**UI-Venus:** chỉ chạy sau khi khoá và chấm UGround; cùng lát 2.532 đã dùng; là listener robustness,
không phải independent dataset replication; chỉ veto nếu hiệu trái dấu và KTC loại 0; trái dấu nhưng
KTC phủ 0 là **trắng**.

### 14.4 Thống kê và điều kiện thành công *(ảnh 24)*
Bootstrap ghép cặp 10.000 lượt: replicate lấy cụm một lần; giữ toàn bộ bước và mọi output của hai
seed; tính trực tiếp trung bình hai paired effects; báo luật `episode_id`; báo sensitivity theo luật
`app`, fallback episode; **không loại `bo_qua`**; mọi failure = 0.

⚠️ `mde_that.py` hiện có lỗi fallback singleton theo bước và complete-case. Phải sửa cho đúng trước
phân tích. Kiểm của Opus gợi ý sửa cụm chỉ đổi SE khoảng ≤6% và ngưỡng khoảng 0,01 pp; **phải báo số
thật, không thổi mức nghiêm trọng.**

Các dải `+1,7/+2,8 pp` được tái dùng như decision bands mới, khoá trước output MIN; **không được gọi
là preregistration của estimand MIN-ORPO**:
- mạnh: `Δ ≥ +2,8 pp`, KTC95 loại 0;
- dương yếu: `+1,7 ≤ Δ < +2,8 pp`, KTC95 loại 0;
- trắng: KTC phủ 0 hoặc `−2,8 < Δ < +1,7 pp`;
- âm: `Δ ≤ −2,8 pp` với KTC loại 0.

**Được claim "component làm tốt hơn và model cuối tốt hơn" khi:**
1. `Δ_component ≥ +1,7 pp` và KTC95 loại 0;
2. `Δ_system ≥ +1,7 pp` và KTC95 loại 0;
3. effect của hai seed cho cả hai estimand đều dương;
4. không có no-harm failure trên bước không-chạm: cận dưới `> −3 pp`;
5. strict audit không cho thấy gain chủ yếu do vùng mù;
6. UI-Venus không veto;
7. gain được phép tập trung ở lát pair-eligible/OCR-name vì đó là population component nhắm tới,
   nhưng lát không eligible phải không bị hại; claim phải giới hạn đúng population thay vì gọi là
   gain grounding tổng quát.

Nếu chỉ đạt `Δ_component` nhưng không đạt `Δ_system`, objective có hiệu ứng so với CE2 nhưng chưa tạo
model cuối tốt hơn S1. Nếu chỉ đạt `Δ_system`, không được quy công cho MIN-ORPO vì extra stage có thể
là nguyên nhân.

## 15. Cổng GO/STOP và lịch ba tuần *(ảnh 24–25)*

### Tuần 1 — không train lớn
1. khôi phục/xác minh train images, OCR và descriptors;
2. đo exact-span eligibility;
3. dựng negative theo Mục 12;
4. audit 300 cặp, false-negative `<5%`;
5. text-only/shuffled probes;
6. dựng wrong-referent counterfactual trên câu người để kiểm thước có nhạy với loại lỗi component
   nhắm tới; đây là validity gate, không dùng chọn model;
7. pin framework và smoke ORPO 20/200 cặp dài nhất;
8. khoá analysis plan, beta, updates và sample hashes.

**STOP nếu:** eligibility `<25%` · false-negative `≥5%` · shortcut probe vượt ngưỡng ·
wrong-referent counterfactual không làm executability giảm ít nhất 10 pp trên lát đủ điều kiện với
KTC ghép cặp loại 0 · ORPO OOM/NaN hoặc không resume/save-load đúng.

### Tuần 2 — seed 101
1. chạy CE2/101 và MIN/101;
2. **không chấm test 4.463**;
3. kiểm held-out pairwise margin, CE, output format và action/toggle no-harm;
4. nếu MIN không học margin tốt hơn CE2 hoặc action/toggle regress trên 3 pp: STOP;
5. nếu cơ học đạt, chạy CE2/202 và MIN/202.

Không dùng một listener score trên seed 101 làm điều kiện chạy seed 202. Điều này tốn thêm compute
nhưng loại post-selection bias khỏi estimand cuối.

### Tuần 3 — xác nhận
1. hoàn tất hai seed MIN/CE2;
2. chấm UGround đúng một lần trên 4.463 cho bốn checkpoint;
3. tính `Δ_component` và `Δ_system`;
4. chỉ khi cần giải thích cơ chế, chạy RAND/101;
5. chạy UI-Venus và strict audit sau khi verdict primary đã cố định;
6. báo tất cả output, kể cả kết quả trắng/âm.

**Nếu quota không đủ, ưu tiên theo thứ tự:** MIN×2 + CE2×2 → UGround primary → strict validity audit
→ UI-Venus → RAND mechanism. Không hy sinh seed thứ hai của primary để lấy nhiều ablation một seed.

## 16. Novelty và câu được phép viết *(ảnh 26)*

### 16.1 Phân định prior art
Phải trích và phân định ít nhất: Mao et al. CVPR 2016 (MMI/discriminative referring expression) ·
Luo & Shakhnarovich CVPR 2017 (listener/comprehension-guided REG) · Widget Captioning EMNLP 2020
(GUI widget description với CE) · ORPO (thuật toán preference optimization không reference model).

**Không claim:** phát minh ORPO · phát minh minimal pairs · kiến trúc mới · lần đầu dùng hard
negative · SOTA GUI grounding · hiệu quả cho người thật nếu chỉ chấm bằng listener.

### 16.2 Claim an toàn trước kết quả
> Luận văn thiết kế một mục tiêu ưu tiên theo cặp quy chiếu tối thiểu cho sinh chỉ dẫn GUI. Câu bị
> loại đổi danh tính phần tử trong cùng màn nhưng giữ nguyên hành động và gần khớp độ dài; model vẫn
> nhận cùng input và có cùng chi phí inference như direct SFT.

### 16.3 Claim sau kết quả dương
> So với tiếp tục huấn luyện CE cùng data support và update budget, MIN-ORPO làm executability tăng
> X điểm qua hai seed; model cuối đồng thời tăng Y điểm so với S1. Hai hiệu đều có KTC ghép cặp loại
> 0 và không bị strict audit/UI-Venus phủ quyết.

Nếu `MIN − RAND` chưa có hai seed/KTC, chỉ được nói hard-negative ablation **gợi ý**, không được nói
chứng minh.

### 16.4 Phán quyết xác suất
MIN-ORPO là phương án có expected value tốt nhất trong phạm vi ba tuần sau khi loại các phương án
leakage, prior-art gần và custom-trainer nặng. Nó **không bảo đảm đạt dải dương**. Nếu audit
eligibility hoặc test chính không qua, kết luận đúng là component không được dữ liệu hỗ trợ; không
đổi metric hoặc sinh thêm nhánh hậu kiểm để cứu.

## 17. Chỉ dẫn cho chat tiếp theo *(ảnh 26–27)*

1. Không triển khai phương án TD-ROI/RLTS trong `report/115` — nó đã bị rút.
2. Đọc Mục 10–16 và xác minh input contract **từ mã**.
3. Việc đầu tiên là **đo eligibility**, chưa train.
4. Dựng script wrong-referent counterfactual và audit pair.
5. Pin LLaMA-Factory rồi smoke ORPO trên 20/200 cặp dài nhất.
6. Tạo CE2 và MIN từ đúng cùng S1 checkpoint, update budget và data support.
7. Không gọi UGround/UI-Venus trong vòng chọn model.
8. Không chấm 4.463 sau seed 101.
9. Primary là `MIN − CE2`; `MIN − S1` là system gain bắt buộc.
10. **S2/202 vẫn cần nếu muốn hoàn tất estimand cũ**, nhưng không được trộn vào chiến dịch MIN-ORPO.

### 17.1 Thứ tự ưu tiên khi tài liệu mâu thuẫn
1. **File này** thắng về *sẽ làm gì tiếp và quy công thế nào*. `AGENT_BRIEF.md`, `README.md`,
   `CLAUDE.md` và `report/1xx` viết trước 23/08/2026 nên vẫn mô tả S2 là đóng góp mô hình chính;
   điều đó không còn là kế hoạch.
2. **Mã** thắng file này về *hệ thống đang thực sự làm gì*. Mọi con số hoặc contract trong đây phải
   kiểm lại được từ `harness/` và `runs/`.
3. **`report/106_DANG_KY_TRUOC.md`** vẫn thắng về *estimand S1/S2 đã đăng ký trước*. MIN-ORPO là
   estimand mới, không nằm trong hồ sơ đăng ký đó.

### 17.2 Nguồn phải đọc và kiểm lại
**Trạng thái và số liệu:** `runs/score_*_raw.jsonl`, `runs/floor/`, `runs/venus/` ·
`harness/score_run.py`, `harness/metric_exec.py` · `harness/mde_that.py` (có lỗi cụm/complete-case
nêu ở Mục 14.4) · `report/106`, `report/108`.

**Contract và dữ liệu cho MIN-ORPO:** `harness/build_branch_data.py` (`prompt_body()` định nghĩa
input thật) · `harness/infer_branch.py` (`screen_elements()`, `MAX_ELEMS`, `--ceiling`) ·
`harness/descriptor_label_build.py` (`nearest_other()`, nguồn negative) · `harness/make_floor.py` ·
`report/103`, `report/114`.

Trước khi chạy bất cứ thứ gì: kiểm dữ liệu dẫn xuất trong `harness/dg1_cache/` còn đủ không, vì các
bước ở Mục 15 giả định có ảnh, OCR và descriptors của cả train lẫn test.

### 17.3 Phương án đã rút
Bản TD-ROI/RLTS từng chiếm Mục 10–18 của file này đã được chuyển sang
`report/115_PHUONG_AN_TD_ROI_DA_RUT.md`. Nó chỉ là audit trail: đọc khi cần biết vì sao hai hướng đó
bị loại, **không triển khai** và không trộn điểm với MIN-ORPO.

---
---

# PHỤ LỤC A — Kiểm chứng và đánh giá của trợ lý (23/8/2026, máy WSL)

> Viết sau khi đọc hết 27 ảnh và **chạy lại số trên máy này**, không trích lại ghi chú.
> Mục tiêu: trả lời câu hỏi của user — *hướng đó có hợp lý không*.

## A.1 Kiểm chứng từng khẳng định — bằng mã, không bằng ghi chú

| # | khẳng định của tài liệu | phán quyết | bằng chứng |
|---|---|---|---|
| 1 | Điểm 5 hệ: 75,73 · 59,62 · 59,11 · 57,18 · 47,59 trên n=4.463 | ✅ **đúng tuyệt đối** | chạy lại đoạn `glob` trên `runs/score_*_raw.jsonl`, khớp đến hai chữ số |
| 2 | Gold action **không** vào prompt | ✅ **đúng** | `build_branch_data.py:50-60` — `parts` chỉ có goal, history(3), OCR, câu lệnh sinh. Không có action |
| 3 | `--ceiling gold` nối descriptor vào *user prompt*, không ép assistant prefix | ✅ **đúng** | `infer_branch.py:479-483`: `body = with_ceiling(body, …)` rồi `body` đi vào `{"role":"user"}`. Assistant prefix không hề bị đụng |
| 4 | `mde_that.py` complete-case + singleton theo bước | ✅ **đúng, và nặng hơn tài liệu nói** | `nap()` bỏ mọi dòng có `bo_qua`; `cum()` trả `__don__{episode}_{step}` |
| 5 | `app_seen_in_train`: True 1.737 · False 78 · None 2.648 | ✅ **đúng** | đếm trên raw: 2.647 bước không gán được app trên 4.462 dòng đủ trường |
| 6 | Repo không có ảnh, OCR, descriptors, checkpoint | ⚠️ **đúng với kho trên máy Mac, SAI với máy WSL này** | `harness/dg1_cache/` ở đây **4,1 GB**: `test_ac/` **đủ** (6.958 bước · 6.969 ảnh · ocr 6.969 · descriptors 4.448); `train_ac/` **chỉ có lát 1.697 bước** |
| 7 | "Nhiều tài liệu cũ trong repo nói gold action là đầu vào" | ⚠️ **không đúng với kho này** | grep `main.tex`, `thesis/chapters/*.tex`, `AGENT_BRIEF.md`, `README.md`, `report/112`: **0 lần**. `main.tex:583` mô tả đúng contract |

### A.1.1 Về lỗi cụm — tôi đo mức nghiêm trọng thật, và tài liệu nói đúng

Chỗ này tài liệu chỉ nói "lỗi fallback singleton". Thật ra sai lệch **so với hồ sơ đăng ký trước**:
`report/106` sửa đổi (e) khoá luật *"mỗi **tác vụ** không-rõ-app là một cụm"* và ghi rõ **G = 1.091**.
Mã hiện tại gom theo **bước**, cho **2.906 cụm** — nhiều gấp 2,7 lần so với luật đã khoá, tức chia
nhỏ cụm hơn hồ sơ cho phép, hướng làm **SE nhỏ đi và số đẹp lên**.

Nhưng khi đo thật (bootstrap 4.000 lượt trên cặp S1/101 vs S1/202):

| luật gom cụm | G | SE | KTC95 |
|---|---|---|---|
| theo **bước** (mã hiện tại) | 2.906 | 0,386 pp | [−0,21 · +1,28] |
| theo **tác vụ** (luật đã đăng ký) | 1.091 | 0,375 pp | [−0,22 · +1,24] |

⇒ chênh **3%**, không đổi bất kỳ kết luận nào. Đúng như tài liệu tự khai (*"chỉ đổi SE khoảng ≤6%…
phải báo số thật, không thổi mức nghiêm trọng"*). **Vẫn phải sửa** — vì đây là lệch hồ sơ đăng ký,
không phải vì nó cứu được con số nào.

### A.1.2 Mìn `test_ac/descriptors.jsonl` vẫn chưa nổ

Dòng đầu tiên của file trên máy này: `"role": "mục"`, `"hint": "ngay dưới chữ …"` — **vẫn tiếng
Việt**, đúng như `CLAUDE.md` đã cảnh báo. `infer_branch.py:480` nhét nó vào câu nhắc cho
`--ceiling gold|filler`. Chạy hai nhánh đó mà chưa dựng lại là hỏng câm.

⭐ **Phát hiện phụ có lợi:** `descriptors.jsonl` đã có sẵn trường **`desc_neg`** (`nearest_other()`).
Nghĩa là nguồn negative cho MIN-ORPO **không phải dựng từ đầu**, đã có khung sẵn — rẻ hơn tài liệu
ước tính.

## A.2 Hướng MIN-ORPO — chỗ đứng vững

1. ⭐ **Control CE-stage2 là đóng góp phương pháp thật.** Thiết kế S2 cũ so `S2 − S1` nên gộp *tác
   dụng của objective* với *tác dụng của việc train thêm*. `MIN − CE2` với cùng update budget và
   cùng data support tách được hai thứ đó. Đây đúng là câu hỏi mọi phản biện sẽ hỏi, và nó áp dụng
   được **kể cả khi bỏ MIN-ORPO** — mọi can thiệp stage-2 về sau đều nên có control này.
2. ⭐ **Nhắm đúng kênh lỗi lớn nhất, có số đỡ lưng.** 590/844 bước = **13,22 pp** là "action đúng,
   trượt định vị". Một objective phạt gọi nhầm referent đánh thẳng vào đó. S2 trước kia không có
   con số nào chỉ đích như vậy.
3. ⭐ **Không cho listener vào vòng train/chọn model.** Nếu dùng UGround để chọn checkpoint thì
   thước biến thành mục tiêu huấn luyện và mọi con số sau đó vô nghĩa. Tài liệu cấm rõ ở 13.3 và
   giữ nguyên ở 17.7.
4. ⭐ **Cổng khoá trước GPU.** Eligibility, shortcut probe, audit 300 cặp, smoke 200 cặp dài nhất —
   dùng lại đúng bài học P10 đã trả giá (probe trên mẫu đầu tập không kết luận được về bộ nhớ).
5. ⭐ **Trung thực về S2.** −2,19 pp nằm trong dải trắng vì thiếu seed 202; danh sách "câu cấm nói"
   khớp đúng luật `report/106`. Không có chỗ nào cố nặn kết quả âm thành phát hiện.
6. **ORPO là lựa chọn rẻ đúng chỗ** — không reward model, không reference model riêng, có sẵn
   trong LLaMA-Factory, chạy được trong ngân sách này.

## A.3 Chỗ không đứng vững — sáu điểm

### ① ⛔ Tài liệu không nhắc một chữ nào về hai bài báo. Đây là lỗ hổng lớn nhất.
Lịch của nó là **ba tuần** → kết thúc ~13/9. VCL hạn **30/8**, FAIR hạn **31/8** — còn **7 và 8
ngày**. Toàn bộ 27 ảnh không có chữ "FAIR", "VCL", "nộp" hay "hạn" nào.

⇒ Đây là kế hoạch cho **luận văn**, không phải cho hai bài. Làm theo nguyên văn từ hôm nay là bỏ cả
hai venue. Hai đồng hồ này phải tách ra, và tài liệu tách hộ bằng cách im lặng — đó là chỗ nguy hiểm.

### ② ⛔ Ngân sách compute không khép trong ba tuần
MIN×2 + CE2×2 = **4 lượt train** × ~23 h A100 ≈ **92 giờ**, ~**500 đơn vị** Colab. Chấm 4 checkpoint
× 5,6 h = **22,4 h Kaggle** trong khi quota là **30 h/tuần**. Cộng UI-Venus 8,15 h, cộng RAND/101.
Và kho này có tiền sử **8 lần mất máy ảo trong 2 lượt S1** (~18 giờ, ~85 đơn vị). "Ba tuần" chỉ
đúng nếu không hỏng gì — điều chưa từng xảy ra ở dự án này.

Tài liệu có danh sách ưu tiên khi thiếu quota (Mục 15), đó là điểm cộng, nhưng nó không sửa được
việc dòng tiêu đề hứa ba tuần.

### ③ ⚠️ Bước 0 rẻ hơn tài liệu nói ở một nửa, đắt hơn ở nửa kia
- **Test: đã đủ trên máy này.** 6.958 bước, 6.969 ảnh, OCR đủ. Không phải dựng lại gì.
- **Train: chỉ có lát 1.697/64.567 bước.** Toàn bộ tập dạy + ảnh phải dựng lại từ HuggingFace trên
  máy **không GPU**, rồi chạy OCR toàn tập trên CPU. Đây mới là chi phí thật của "Tuần 1 — không
  train lớn", và tài liệu không định lượng nó.

### ④ ⚠️ Cổng eligibility ≥25% là chỗ dễ trượt nhất, và trượt thì mất trắng một tuần
Điều kiện giao của 9 luật ở Mục 12.2 khá hẹp: tên phải **xuất hiện literal** trong câu người, có
distractor cùng màn 80–350 px cùng/gần role, tên khác nhau sau chuẩn hoá, cả hai có bằng chứng
OCR/a11y, độ dài lệch ≤2 token. Đối chiếu thống kê nhãn của chính dự án — **21,2% không có tên**,
**7,6% trùng tên**, phần lớn tên đến từ OCR sau khi đã lọc 14,7% nhãn rác — giao của ngần ấy điều
kiện rất có thể rơi dưới 25%.

Tài liệu xử lý đúng (đặt cổng ở tuần 1, STOP nếu trượt) và trung thực (*"không có phương án nào bảo
đảm trước kết quả dương"*). Nhưng phương án B duy nhất nó nêu — on-policy rejected từ lỗi thật của
S1 — lại được ghi là "hướng dài hạn, không tự động chuyển trong cùng chiến dịch". Tức là trượt cổng
= hết đường trong phạm vi ba tuần.

### ⑤ ⚠️ Một mâu thuẫn nội bộ mà tài liệu không thấy: điều kiện (7) của Mục 12.2 va vào phép diễn đạt lại
Điều kiện (7) cho phép **thay mệnh đề vị trí của target bằng mệnh đề của negative**. Nhưng phép A đã
đo trên chính câu người: bỏ mệnh đề vị trí làm executability **−3,5 pp**, và quan trọng hơn, nó làm
**đuôi sai số bung** — p90 từ 6,88 lên **31,16**, p95 từ 27,54 lên **62,38**.

⇒ Mệnh đề vị trí **không trung tính**. Cặp gọi là "tối thiểu" khi đó khác nhau ở **hai chiều** (danh
tính + vị trí), nên objective có thể học *"đừng nói sai toạ độ"* thay vì *"đừng gọi nhầm phần tử"* —
đúng thứ mà cả bài báo lẫn luận văn đang muốn claim.

Hai probe chống shortcut ở 12.3 **không bắt được** chuyện này: text-only và shuffled-image đều so
hai chuỗi chữ, mà cả hai vế đều là chữ hợp lệ. **Đề xuất vá:** tách hai tầng và báo riêng —
(a) cặp chỉ đổi **tên**, giữ nguyên mệnh đề vị trí; (b) cặp đổi cả hai. Nếu (a) đủ số lượng thì
headline phải đứng trên (a).

### ⑥ ⚠️ Novelty mỏng, và đây là lần pivot thứ ba
Mục 16.1 tự cấm gần hết: không phát minh ORPO, không phát minh minimal pairs, không kiến trúc mới,
không lần đầu dùng hard negative. Còn lại là *"áp một objective ưu tiên có sẵn vào miền GUI với cặp
quy chiếu tối thiểu"*. Với luận văn có chương đo lường mạnh thì đủ. Với bài báo thì incremental —
và về mặt rủi ro, nó **cùng hình dạng** với claim S2 vừa trắng. Nếu MIN cũng trắng, luận văn có hai
đóng góp mô hình không kết luận được mà **chưa giải thích được cái nào**.

## A.4 Điều tài liệu bỏ sót và tôi cho là quan trọng hơn MIN-ORPO

**`s2_nopoint` bị xếp nhầm chỗ.** Tài liệu để nó ở Mục 9 "bắt buộc nếu muốn nói về cơ chế", rồi lịch
ba tuần không có chỗ cho nó. Nhưng:

- Chẩn đoán 4j-18 chỉ thẳng vào nó: **Base gọi đúng loại thao tác nhiều hơn CẢ HAI bản đã huấn
  luyện** (83,4% vs S1 55,1% vs S2 38,8%). Giả thuyết: tập dạy chỉ gắn khai báo cho bước **chạm**
  nên model học tắt *"có khai báo ⇔ là chạm"*. `s2_nopoint` tách *"có khai báo"* khỏi *"có toạ độ"*
  — đúng chỗ chẩn đoán chỉ ra.
- **Dữ liệu đã dựng sẵn** (`branches/s2_nopoint.json` có trên máy này), chi phí **một** lượt train
  ~26 h thay vì **bốn**.
- Nó trả lời câu hỏi luận văn **bắt buộc** phải trả lời — *vì sao S2 âm* — bất kể có component mới
  hay không. Một luận văn giải thích tốt một kết quả âm thì bảo vệ được; hai kết quả âm không giải
  thích được thì không.

## A.5 Phán quyết

**Hướng MIN-ORPO là hợp lý về mặt khoa học, nhưng sai về mặt lịch, và bị xếp sai thứ tự ưu tiên.**

Chẩn đoán của phiên debate **đúng và kiểm được** — tôi chạy lại toàn bộ, không tìm ra số nào sai.
Ba phát hiện (mẫu số 4.463 · gold action không vào prompt · `--ceiling` không phải forced prefix)
là đóng góp thật. Control CE-stage2 nên **giữ vĩnh viễn** kể cả nếu bỏ MIN-ORPO.

Nhưng tài liệu được viết như thể chỉ có một đồng hồ. Thực tế có hai, và cái gấp hơn không được nhắc
tới lần nào.

### Đề nghị: tách theo hai đồng hồ

**A. 23–31/8 — đồng hồ bài báo. Không tiêu một giờ GPU nào cho hướng mới.**

| # | việc | chi phí | vì sao bây giờ |
|---|---|---|---|
| 1 | **Bật train S2/202 trên Colab ngay hôm nay** | ~26 h A100, ~126 đơn vị — chạy nền trong lúc viết bài | Đóng estimand đã đăng ký. Xong ~25/8, chấm 5,6 h Kaggle → 26/8, kịp thêm một hàng vào bảng FAIR đúng lịch `CLAUDE.md` đã định. Cả tài liệu debate (17.10) lẫn `report/106` đều đòi nó |
| 2 | Sửa `mde_that.cum()` về fallback **episode** + bỏ complete-case; ghi thành mục sửa đổi mới ở `report/106` | 0 đồng, ~30 phút | Lệch hồ sơ đăng ký theo hướng làm số đẹp lên. Báo kèm số thật: SE 0,386 → 0,375, ~3%, không đổi kết luận nào |
| 3 | Rà bản thảo xem có câu nào mô tả `--ceiling gold` như forced prefix | 0 đồng | Nếu có, sửa thành *oracle side-information trong input*. Contract đầu vào thì **không phải sửa** — `main.tex:583` đã đúng |
| 4 | Viết VCL từ `ch3` · cắt §III của FAIR | như kế hoạch cũ | Không đổi |

**B. Sau 31/8 — đồng hồ luận văn. Theo thứ tự này, không đảo.**

1. **`s2_nopoint`** — 1 lượt train, dữ liệu sẵn. Giải thích vì sao S2 âm. *(Xem A.4.)*
2. **Đo eligibility MIN-ORPO** — 0 đồng GPU, chạy trên tập train sau khi dựng lại. Nếu `<25%` thì
   biết sớm mà không mất gì. `desc_neg` đã có sẵn nên rẻ hơn tài liệu ước.
3. **Chỉ khi (1) và (2) đều xong** mới cam kết 4 lượt train MIN/CE2 — và khi đó áp nguyên bộ cổng ở
   Mục 12–15, chúng viết tốt.

**Nếu ngân sách chỉ đủ một trong hai: chọn `s2_nopoint` trước.** Không phải vì nó hay hơn, mà vì nó
rẻ hơn bốn lần và trả lời câu hỏi luận văn không được phép bỏ trống.

### Ba việc phải làm dù chọn hướng nào
- ⛔ Dựng lại `test_ac/descriptors.jsonl` bằng `descriptor_label_build.py --split test` **trước** khi
  chạy bất kỳ nhánh `--ceiling` nào — file trên máy này vẫn tiếng Việt.
- ⛔ Đồng bộ hai kho: máy WSL không có `FINAL_SOLUTION.md` lẫn `report/115`. Lấy về, nếu không mọi
  tham chiếu trong file 116 này đều chết.
- ⛔ Giữ `CE-stage2` làm control cho **mọi** can thiệp stage-2 về sau, kể cả `s2_nopoint`.
