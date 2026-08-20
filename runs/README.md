# `runs/` — điểm số đã chấm

Mỗi lượt để lại hai tệp. **Giữ cả hai**, và commit vào git — đây là số đi thẳng vào luận
văn nên cần lịch sử phiên bản để truy được số nào đo lúc nào bằng mã nào.

| tệp | vai |
|---|---|
| `score_<nhánh>.json` | số tổng hợp |
| `score_<nhánh>_raw.jsonl` | **một dòng mỗi bước** — đổi luật chấm hay thêm lát cắt thì chấm lại từ đây, **không gọi lại bộ trỏ** (tiết kiệm 5,6 giờ mỗi lần) |
| `preds_<nhánh>.jsonl` | câu do mô hình sinh, đầu vào của khâu chấm |

Trường trong tệp thô: `episode_id · step_id · app · app_seen_in_train · pred_xy · gold_xy ·
wh · n_buttons · sent · gold_instruction · action_ok · toggle_ok · hit_disk · hit_voronoi ·
executable`. Bước bị bỏ mang khoá `bo_qua` thay vì các trường chấm.

## Bố cục — tệp tải từ Kaggle về ĐÂU

Ba nhánh chính nằm ngay ở `runs/`; mỗi phép kiểm phụ có thư mục riêng, vì số tệp nhân bốn
đến sáu lần cho mỗi phép và trộn chung thì không còn đọc được cái nào thuộc lượt nào.

| chỗ | đựng gì |
|---|---|
| `runs/` | ba nhánh chính: `score_ceiling_human` · `score_s1_seed101` · `score_base` |
| `runs/gate_a/` | vết cổng A (sai số bộ trỏ, trần đo trên mẫu con — đã rút) |
| `runs/paraphrase/` | phép A: bốn biến thể diễn đạt lại, `preds_para_*` + `score_para_*` |
| `runs/venus/` | phép B: bộ trỏ thứ hai UI-Venus (chưa chạy) |

⚠️ Tải từ Kaggle về thì đặt **thẳng vào thư mục của phép đó**, đừng để ở gốc kho hay
`report/`. Ngày 17/8 bốn tệp lạc vào `report/papers/` (thư mục ghi chú tài liệu tham khảo),
mất một lượt dọn để nhận ra.

`harness/phep_a_ghep_cap.py` đọc `runs/paraphrase/` — đọc kết quả phép A bằng nó, đừng đọc
`score_para_*.json` trần, vì con số tổng **bị pha loãng 3,8 lần** ở ba biến thể
`p2/p3/p4` (chúng chỉ đụng được một phần tư số bước).

## Năm lượt đã chấm — mẫu số **4.463** bước, Kaggle T4, 0 đồng

| | executable | KTC95 | hit_voronoi | action_ok | disk |
|---|---|---|---|---|---|
| **Human (trần)** | **75,7%** | [74,1 – 77,3] | 75,8% | 100%¹ | 84,3% |
| **S1 seed 202** | **59,6%** | [57,9 – 61,3] | — | — | — |
| **S1 seed 101** | **59,1%** | [57,3 – 60,8] | 60,2% | 94,4% | 69,2% |
| **S2 seed 101** *(20/8)* | **57,2%** | [55,4 – 58,9] | — | 94,9% | 67,4% |
| **Base** (`--no-adapter`) | **47,6%** | [45,9 – 49,3] | 48,9% | 96,5% | 57,6% |

⚠️ **Mẫu số là 4.463 cho mọi nhánh** — `score_run.py:516` cho câu rỗng vào quần thể với
`exec = 0` chứ không loại ra. Câu *"cùng 4.462 bước"* ở bản cũ **không chính xác**: Base và
trần có 4.463 dòng dùng được, mỗi lượt S1 và s2/101 có **một** dòng `bo_qua`, và **giao
S2∩S1 = 4.461** — chỉ các phân tích đọc **tệp thô** mới xuống con số đó.

⚠️ **S2 hạt giống 101 THẤP HƠN S1 ~2 pp.** Mới **một** hạt giống ⇒ chưa đọc Δ được
(`report/106` mục (w) đòi trung bình hai). Chẩn đoán đầy đủ: `report/110` mục **4j-18**,
mã `harness/phan_tich_s2.py`.

¹ Vì `pred` chính là `gold_instruction` nên `action_ok`/`toggle_ok` đúng theo định nghĩa;
điểm rút gọn còn đúng phần định vị. Đó là ý nghĩa của trần.

Cụm 1.091 · hiệu dụng **454,3** ở cả ba. **Đọc mọi điểm trên nền 75,7% — không phải 100.**

### Ghép cặp (McNemar, cùng bước; đều p<0,001)

| | Δ | b | c | χ² |
|---|---|---|---|---|
| S1 − Base | **+11,5 pp** | 284 | 798 | 243,2 |
| Human − S1 | **+16,6 pp** | 102 | **843** | 579,5 |
| Human − Base | **+28,1 pp** | 102 | 1.357 | 1.077,8 |

SE của hiệu ghép cặp **0,64–0,75 pp** (hai mẫu độc lập: 0,94) ⇒ **MDE ghép cặp 1,8–2,1 pp**
chưa hiệu chỉnh cụm, ước **2,7–4,5 pp có cụm**.
**Room cho can thiệp: 741 bước = 16,6 pp**; dạng ghép cặp là **843 bước** mà câu người định vị
được còn S1 thì không.

### ⛔ Số đã bị rút

**Trần 70,0% [64,5–75,3]** — đo trên mẫu con 300 bước (`gate_a_ceiling.py`, suy từ vết cổng A).
Chấm đủ 4.462 bước ra **75,7%**, cao hơn 5,7 điểm và nằm ngoài mép trên KTC cũ. Kéo theo hai
số cũng bị rút: room "485 bước / 10,9 pp" → **741 bước / 16,6 pp**, và "S1 đạt 84,4% của trần"
→ **78,1%**.

## Cách tái tạo

Gói dữ liệu chấm: `python harness/make_bundle.py score` (1,7 GB: mã + `test.jsonl` đã gắn
nhãn + `ocr` + `descriptors` + 4.463 ảnh bước chạm), tải lên Kaggle làm dataset dùng lại cho
mọi lượt. Lệnh chấm:

```bash
python harness/score_run.py --mode score --grounder uground \
    --preds <preds>.jsonl --out <score>.json
```

⚠️ `test.jsonl` phải là **bản đã gắn nhãn `app_seen_in_train`** (`score_run.py:405` đọc nhãn
thẳng từ đó). Bản đúng: 6.958 dòng, nhãn 2.991 / 139 / 3.828.

**Trần đo không cần GPU sinh câu:** dựng tệp `preds` với `pred = gold_instruction` rồi chấm
như một nhánh bình thường. `runs/preds_ceiling_human.jsonl` đã có sẵn; kiểm bằng cách đối
chiếu với `gold_instruction` trong tệp thô của một lượt khác (khớp 4.462/4.462).

Dữ liệu huấn luyện: `s1.json` md5 **641953d75d61ab192b94a559362cce9b**, 64.567 mẫu.

⚠️ **Tệp chưa tải về máy này:** `preds_base.jsonl` (6.958 câu của nhánh Base) còn nằm ở
`Drive/thesis/preds/`. Tệp thô `score_base_raw.jsonl` đã có ở đây nên mọi lát cắt tính lại
được, nhưng nếu cần chấm lại Base bằng bộ trỏ khác thì phải tải `preds_base.jsonl` về trước.
Tương tự, `preds_s1_seed202.jsonl` sẽ sinh ra sau khi lượt 202 xong.
