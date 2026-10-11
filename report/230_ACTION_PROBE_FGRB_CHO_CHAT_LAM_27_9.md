# 230 — Action cho chat kia: probe đóng băng FGRB (27/9/2026)

Đọc hết file này trước khi làm. Chat này chỉ thấy file này và repo vừa clone. Mọi số, cổng và
script cần dùng đều nằm ở đây.

## 0. Việc phải làm

Phương pháp đã chốt để thử là **GUIStep-FGRB**: thêm một thành phần vào S1, không train lại Qwen.

Việc của lượt này **không phải train FGRB**. Việc là đo xem hidden state đóng băng của S1 có dự
đoán được action, role và zone hay không. Trượt cổng thì dừng. Không đổi sang hướng khác.

Làm đúng thứ tự:

1. Chạy script kiểm nhãn, 0 GPU. Số lệch kỳ vọng thì dừng.
2. Kiểm kê adapter S1, ảnh train và OCR train. Thiếu một thứ thì dừng, ghi file kết quả, không
   tải về, không train.
3. Chỉ khi đủ ba thứ: chạy probe P1 trên mẫu đã khoá.
4. P1 trượt thì dừng. P1 đạt thì mới chạy P2 sinh câu trên validation.
5. Không đụng tập test. Không train LoRA.

## 1. Bài toán

Bài trong clone: `thesis-master/paper/soict2026/main.tex`. Hệ thống tên GUIStep.

Từ screenshot, goal, tối đa 3 câu lịch sử và tối đa 24 chuỗi OCR, model sinh một câu tiếng Anh.

- Backbone đã học: Qwen2.5-VL-3B-Instruct, QLoRA rank 8, alpha 16, dropout 0,05. Vision tower và
  projector đóng băng. Cấu hình ở `thesis-master/harness/train_config.yaml`.
- Mốc cần vượt là **S1/101**, không phải model gốc.
- Dữ liệu: AndroidControl. `train.jsonl` có 64.567 bước. `train_tru_val.jsonl` có 63.000 bước.
  Phần còn lại là validation: 1.567. Test chấm chính thức có 4.463 bước chạm. Lượt này không mở
  test.

S1/101, 4.463 bước, một câu tham chiếu:

| BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore rescale |
| --- | --- | --- | --- | --- | --- | --- |
| 51,56 | 36,79 | 67,35 | 416,12 | 44,37 | 61,26 | 66,33 |

Nguồn: `thesis-master/runs/text_metrics_coco.json` và `thesis-master/runs/text_metrics_them.json`.

Mốc đầy đủ, chỉ dùng sau này nếu P1 và P2 đều đạt và người dùng mở train thật:

- BLEU-4 ≥ 52,1
- CIDEr-D ≥ 421
- ít nhất 4/7 metric tăng
- SPICE ≥ 44,1 và BERTScore ≥ 66,0
- hơn adapter cùng số tham số ít nhất +0,3 BLEU-4 và +3 CIDEr-D

## 2. FGRB là gì

Một bottleneck mềm gắn vào S1 đã đóng băng:

```
screenshot + goal + history + OCR
        │
        ▼
 hidden state của S1, Qwen đóng băng
        │
        ▼
 gộp đặc trưng prompt
        │
   ┌────┼────┐
   ▼    ▼    ▼
P(action) P(role) P(zone)     ba head tuyến tính
   │        │        │
  E_a      E_r      E_z       codebook học được
   └────────┼────────┘
            ▼
   z = W[P_a E_a ; P_r E_r ; P_z E_z]
   h' = h + sigmoid(u^T h) · z
            │
            ▼
      sinh một câu
```

- Dùng phân phối mềm, không argmax cứng lúc tiêm.
- Một model lúc chấm. Không model thứ hai. Không box vàng. Không câu vàng trong đầu vào.
- Câu vàng chỉ được dùng làm nhãn lúc train head và làm reference lúc chấm. Không được dùng câu
  vàng để chọn câu nào sẽ sửa.
- Nhãn role và zone parse từ `target_instruction` của tập train/val. Không thu nhãn người mới.

Ba lớp:

| Biến | Giá trị |
| --- | --- |
| action | lấy `action.action_type`. Trên 63.000 bước train: click 40.058, scroll 7.031, wait 4.592, input_text 4.523, open_app 4.349, navigate_back 2.293, long_press 131, navigate_home 23 |
| role | `NONE` hoặc từ đầu tiên khớp danh sách ở script |
| zone | `NONE` hoặc cụm vị trí khớp regex ở script |

Trên toàn train, khoảng 54,1% bước có role và 16,5% có zone. NONE chiếm phần còn lại. Head dễ học
majority. Vì vậy cổng P1 chấm **recall của lớp khác NONE**, không chấm accuracy trần.

### Câu được phép viết nếu sau này số đứng

> Chúng tôi đề xuất một bottleneck hiện thực câu GUI, phân rã thành action, role và zone. Ba phân
> phối mềm được ánh xạ thành control embedding và tiêm residual vào decoder của cùng một
> Qwen2.5-VL-3B.

Phải trích ViTCAP, ControlCap, COS-Net và HS-PLAN nếu viết luận. Không viết "concept bottleneck
đầu tiên" hay "kiến trúc hoàn toàn mới".

## 3. Vì sao chỉ được probe

Đã đo hai trần, cả hai **không** mở được GPU train:

| Phép | BLEU-4 proxy trên 4.463 câu S1 | Ý nghĩa |
| --- | --- | --- |
| S1 không sửa | 51,77 | mốc proxy |
| Sửa role bằng nhãn vàng | 54,28 (+2,51) | trần, dùng câu vàng |
| Sửa zone bằng nhãn vàng | 64,22 (+12,45) | trần lạc quan |
| Sửa cả hai bằng nhãn vàng | 66,98 (+15,21) | trần, không phải kết quả model |

Naive Bayes chỉ dùng goal và history, train trên 63.000 bước, không dùng ảnh:

|  | Validation 1.567 | Test 4.463 |
| --- | --- | --- |
| role accuracy | 35,55% | 34,15% |
| recall role khác NONE | 37,47% | – |
| zone accuracy | 67,58% | 65,79% |
| recall zone khác NONE | 16,18% | – |
| BLEU-4 proxy sau khi sửa câu bằng dự đoán | – | 51,77 → 43,84 (−7,93) |

Goal và history một mình không đủ. Probe này hỏi câu khác: hidden state có ảnh của S1 có hơn
baseline chữ đó hay không.

## 4. Cổng đã khóa — không được hạ sau khi xem số

### P0 — kiểm clone, 0 GPU

Chạy Phụ lục A trong `thesis-master/`.

| Số | Kỳ vọng |
| --- | --- |
| dòng `train.jsonl` | 64.567 |
| dòng `train_tru_val.jsonl` | 63.000 |
| validation = train trừ tru_val | 1.567 |
| click trên train / val | 40.058 / 1.001 |

Lệch thì dừng. Đừng diễn giải.

### Kiểm kê đầu vào

Clone không có ba thứ sau. Chúng bị `.gitignore` loại:

| Thứ | Đường dẫn đúng nếu đã có trên máy | Ghi chú trong repo |
| --- | --- | --- |
| Ảnh train | `thesis-master/harness/dg1_cache/train_ac/images/` | khoảng 3,5 GB, GitHub Release `data-train-ac-v1`, 6 file zip |
| OCR train | `thesis-master/harness/dg1_cache/train_ac/ocr.jsonl` | khoảng 129,5 MB, cùng release, file `ocr.jsonl.gz` |
| Adapter S1/101 | thư mục LoRA có `adapter_config.json` và `adapter_model.safetensors` | từng nằm ở `MyDrive/thesis/ckpt/s1_seed101` và `/workspace/ckpt/s1_seed101` |

Việc kiểm kê:

1. Thử đúng ba đường dẫn trên.
2. Tìm thêm trong máy các thư mục tên `s1_seed101` và `train_ac/images`, không đệ quy vào
   `Library`, `node_modules`, `.git`.
3. Adapter hợp lệ khi `adapter_config.json` có `r = 8` và `lora_alpha = 16`.
4. Ảnh hợp lệ khi file `images/ep7057_s1.png` mở được. Đó là ảnh của dòng đầu `train.jsonl`.
5. OCR hợp lệ khi file tồn tại và có khoá theo `episode_id` + `step_id`.

Thiếu ảnh, hoặc thiếu OCR, hoặc thiếu adapter: **dừng tại P0**. Ghi file kết quả với phán quyết
`CHƯA CHẠY — thiếu đầu vào`. Liệt kê đường dẫn đã tìm và cái nào thiếu.

Không tự tải release. Không tự kéo Drive. Không chạy probe bằng model gốc thay cho S1. Không bỏ
OCR rồi vẫn gọi là probe của S1. Prompt S1 có OCR; bỏ OCR là đổi đầu vào.

### P1 — probe phân loại, chỉ khi P0 đủ đầu vào

Khoá trước khi train:

- Backbone: Qwen2.5-VL-3B-Instruct cộng đúng adapter S1/101. `eval()`. Mọi tham số Qwen và LoRA
  `requires_grad = False`.
- Processor: `min_pixels=200704`, `max_pixels=1003520`. Khớp `harness/infer_branch.py` và
  `harness/train_config.yaml`. Mặc định processor lệch khoảng 2,6 lần, cấm dùng.
- Prompt: cùng chữ với lúc chấm S1. System ở `harness/build_branch_data.py` biến `SYS`. Thân
  prompt là `prompt_body`. Có ảnh, goal, tối đa 3 câu history, tối đa 24 OCR. Không đưa
  `target_instruction` vào prompt.
- Đặc trưng: hidden state lớp cuối. Gộp bằng trung bình các token ảnh, nối với hidden của token
  văn bản cuối của prompt. Không gộp token của câu vàng.
- Train: 4.000 bước lấy từ 63.000 bước `train_tru_val`, seed 101, stratified theo
  `action_type × (role==NONE) × (zone==NONE)`. Thuật toán ở Phụ lục B. Không được đổi 4.000 hay
  seed sau khi thấy accuracy.
- Val: cả 1.567 bước, không rút mẫu.
- Head: ba Linear. Loss cross-entropy, trọng số lớp = nghịch đảo tần suất trong 4.000 mẫu. Tối đa
  30 epoch. Chọn epoch bằng macro-F1 trung bình của ba đầu trên val. Không chọn bằng BLEU.
- Không mở `test.jsonl`, `score_s1_seed101_raw.jsonl`, hay bất kỳ file điểm test nào trong P1.

P1 đạt chỉ khi cả ba dòng sau đúng trên 1.567 bước val:

| Đầu | Ngưỡng | Baseline đã biết |
| --- | --- | --- |
| recall role, mẫu thật sự khác NONE | ≥ 50% | Naive Bayes chữ: 37,47% |
| recall zone, mẫu thật sự khác NONE | ≥ 30% | Naive Bayes chữ: 16,18% |
| accuracy action | ≥ 73,9% | majority val là click 1.001/1.567 = 63,9%; cộng 10 điểm |

thêm: macro-F1 role và macro-F1 zone phải in ra — accuracy trần dễ đẹp vì NONE.

Thiếu một ngưỡng: **P1 TRƯỢT**. Dừng. Không chạy P2. Không train FGRB. Không hạ ngưỡng.

P1 đạt chưa phải đóng góp. Nó chỉ cho phép đo xem decoder có dùng được tín hiệu đó hay không.

### P2 — sinh câu trên val, chỉ khi P1 đạt

Cùng backbone đóng băng. Chỉ học codebook, ba head, lớp W và vector cổng u. Không học LoRA.

- Dữ liệu train: đúng 4.000 bước của P1. Một epoch. Learning rate 1e-3. Không chọn epoch bằng
  điểm câu.
- Injection: `h' = h + sigmoid(u^T h) · z`, với z tính từ ba phân phối mềm. Hook ở lớp decoder
  cuối, cộng vào mọi token văn bản lúc sinh.
- Sinh greedy trên cả 1.567 bước val, ba lần:
  1. S1 đóng băng, không injection;
  2. FGRB;
  3. FGRB nhưng hoán vị role và zone giữa các mẫu val lúc sinh. Train thì không hoán vị.
- Câu vàng chỉ là reference khi tính BLEU-4 và CIDEr. Không dùng để chọn mẫu sửa.
- Chấm bằng `harness/text_metrics_coco.py` nếu chạy được. Nếu thiếu dependency, ghi rõ proxy
  BLEU-4 của Phụ lục A trong file 229 là không có ở đây: dùng hàm `bleu` trong Phụ lục C, và ghi
  rõ đó là proxy.

P2 đạt chỉ khi đồng thời:

- FGRB hơn S1 không injection ít nhất +0,3 BLEU-4 và +3 CIDEr trên 1.567 bước val;
- bản hoán vị role/zone thấp hơn FGRB ít nhất 0,3 BLEU-4;
- độ dài câu trung bình không lệch quá 15% so với S1 không injection.

Không đạt thì phán quyết **P2 TRƯỢT — không train**. Đạt thì phán quyết **P2 ĐẠT — được phép đề
xuất pilot, chưa được train**. Vẫn không đụng test.

## 5. Không được làm

| Việc | Lý do |
| --- | --- |
| Train LoRA, train lại S1, train full FGRB, pilot 20% | Chưa có cổng. Full run ước lượng khoảng 45–50 giờ A100 |
| Mở test, chấm 4.463 bước | Test chỉ chấm một lần sau pilot, người dùng chưa cho |
| Hạ ngưỡng P1 hoặc P2 sau khi thấy số | Cổng khoá trước |
| Đổi sang fine-tune, ORPO, GRPO, retrieval, crop, OCR pointer, span edit | Các hướng đó đã bị loại |
| Dùng model gốc thay adapter S1 | Không còn là probe của mốc S1 |
| Bỏ OCR hoặc bỏ ảnh | Đổi đầu vào |
| Ghi kết quả vào `thesis-master/` | Clone sẽ bị xoá |
| Sửa `paper/soict2026/main.tex` | Ngoài việc này |

## 6. File kết quả

Ghi đúng một file:

```
/Users/P836901/Documents/Self-learning/thesis/231_KET_QUA_PROBE_FGRB.md
```

File đó phải tự chứa:

1. nguyên văn output Phụ lục A;
2. bảng kiểm kê: adapter, ảnh, OCR, có hay không, đường dẫn;
3. phán quyết một dòng: `CHƯA CHẠY — thiếu đầu vào`, hoặc `P1 TRƯỢT`, hoặc `P1 ĐẠT / P2 TRƯỢT`,
   hoặc `P1 ĐẠT / P2 ĐẠT`;
4. nếu đã chạy P1: số mẫu 4.000, seed 101, accuracy, recall khác NONE, macro-F1, confusion NONE
   và không NONE, epoch được chọn;
5. nếu đã chạy P2: BLEU và CIDEr của ba lần sinh, độ dài câu trung bình;
6. nguyên văn script đã chạy;
7. câu: probe đạt không có nghĩa FGRB đã là đóng góp. Đóng góp chỉ đứng khi train đầy đủ hơn S1,
   hơn adapter cùng số tham số, hơn bottleneck không phân rã, và shuffle làm điểm giảm.

Không tạo file thứ hai.

## Phụ lục A — kiểm nhãn, chạy ngay

Chạy từ thư mục `thesis-master/`. Chỉ dùng thư viện chuẩn.

```python
import json, collections
root = "harness/dg1_cache/train_ac"
def load(name):
    rows = []
    with open(root + "/" + name, encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    return rows
tr_keys = {(str(r["episode_id"]), str(r["step_id"])) for r in load("train_tru_val.jsonl")}
all_rows = load("train.jsonl")
tr, va = [], []
for r in all_rows:
    k = (str(r["episode_id"]), str(r["step_id"]))
    (tr if k in tr_keys else va).append(r)
def acts(rows):
    return collections.Counter((r.get("action") or {}).get("action_type", "?") for r in rows)
print("train_jsonl", len(all_rows))
print("train_tru_val", len(tr_keys))
print("train_hit", len(tr))
print("val", len(va))
print("train_actions", dict(acts(tr)))
print("val_actions", dict(acts(va)))
print("val_click_majority", round(100 * acts(va)["click"] / len(va), 2))
```

Kỳ vọng: `train_jsonl` 64.567, `train_tru_val` 63.000, `train_hit` 63.000, `val` 1.567, click
train 40.058, click val 1.001, majority val 63,88%. Lệch thì dừng.

## Phụ lục B — nhãn, mẫu 4.000, và đầu ra P1

Dùng cùng `tr` và `va` của Phụ lục A. OCR đọc từ `harness/dg1_cache/train_ac/ocr.jsonl` nếu P0 đã
xác nhận file đó tồn tại. Khoá là `(episode_id, step_id)`.

```python
import re, random, collections
ROLES = ["button","option","icon","tab","section","bar","list","item","view",
         "field","box","menu","link","card","tile","row","toggle","switch",
         "checkbox","image","text"]
ROLE_RE = re.compile(r"\b(" + "|".join(ROLES) + r")\b", re.I)
ZONE_RE = re.compile(
    r"\b(?:at|on|in) the ((?:top|bottom|middle|center|upper|lower)"
    r"(?: left| right)?(?: corner)?(?: of the (?:screen|page))?)\b", re.I)

def label(text):
    found = ROLE_RE.findall(text or "")
    zone = ZONE_RE.search(text or "")
    role = found[0].lower() if found else "NONE"
    return role, (zone.group(1).lower() if zone else "NONE")

def stratified(rows, n=4000, seed=101):
    buckets = collections.defaultdict(list)
    for r in rows:
        role, zone = label(r["target_instruction"])
        act = (r.get("action") or {}).get("action_type", "?")
        buckets[(act, role == "NONE", zone == "NONE")].append(r)
    rng = random.Random(seed)
    for v in buckets.values():
        rng.shuffle(v)
    # chia theo tỉ lệ, rồi bù phần dư theo bucket còn nhiều nhất
    picked, frac = [], {}
    total = len(rows)
    for k, v in buckets.items():
        take = int(n * len(v) / total)
        picked.extend(v[:take])
        frac[k] = take
    rest = []
    for k, v in buckets.items():
        rest.extend(v[frac[k]:])
    rng.shuffle(rest)
    picked.extend(rest[: n - len(picked)])
    assert len(picked) == n
    return picked
```

P1 phải in thêm, trên cả 1.567 bước val:

- `n_train_probe = 4000`, `seed = 101`
- với role và với zone: accuracy, recall trên mẫu gold khác NONE, macro-F1, số gold NONE, số dự
  đoán NONE
- với action: accuracy và majority
- epoch được chọn và macro-F1 trung bình lúc chọn
- 8 ví dụ val dự đoán role sai và 8 ví dụ đúng, mỗi ví dụ có `episode_id`, `step_id`, gold role,
  predicted role. Không in câu dài hơn 40 từ.

Cách lấy hidden state, bám hook có sẵn trong `harness/pata_model.py` nhưng **không** bật bridge
PATA và **không** thêm token `<TARGET>`:

1. Nạp model như `harness/infer_branch.py`: `Qwen2_5_VLForConditionalGeneration.from_pretrained`
   rồi `PeftModel.from_pretrained`.
2. Prompt không có câu đích, giống `prompt_only(..., with_target=False)`.
3. Một forward `use_cache=False`, `output_hidden_states=True`.
4. Lấy hidden lớp cuối. Token ảnh là các vị trí có id ảnh của Qwen2.5-VL. Token văn bản cuối là vị
   trí cuối không phải pad.
5. Vector mẫu = nối [trung bình token ảnh ; hidden token cuối].
6. Cache vector ra ngoài clone, ví dụ
   `/Users/P836901/Documents/Self-learning/thesis/_fgrb_probe/hiddens_seed101.pt`, để khỏi forward
   lại. File cache không thay file kết quả 231.

Ước lượng: khoảng 5.600 ảnh. Khoảng 1–2 giờ trên A100, khoảng 5–6 giờ trên T4. Không chạy 63.000
ảnh ở lượt này.

## Phụ lục C — proxy BLEU nếu chưa chấm được CIDEr

Chỉ dùng khi `harness/text_metrics_coco.py` không chạy. Ghi rõ trong file 231 là proxy, không
phải điểm COCO chính thức.

```python
import re, math, collections
def tok(s):
    return re.findall(r"\w+", (s or "").lower())
def bleu(hyps, refs):
    m = [0] * 4
    n = [0] * 4
    hl = rl = 0
    for h, r in zip(hyps, refs):
        h, r = tok(h), tok(r)
        hl += len(h)
        rl += len(r)
        for k in range(1, 5):
            hc = collections.Counter(tuple(h[i:i+k]) for i in range(len(h) - k + 1))
            rc = collections.Counter(tuple(r[i:i+k]) for i in range(len(r) - k + 1))
            m[k-1] += sum(min(v, rc[z]) for z, v in hc.items())
            n[k-1] += max(0, len(h) - k + 1)
    if min(n) == 0 or hl == 0:
        return 0.0
    bp = 1 if hl > rl else math.exp(1 - rl / max(hl, 1))
    return 100 * bp * math.exp(sum(math.log(m[i] / n[i]) for i in range(4)) / 4)
```

P2 vẫn cần CIDEr chính thức để so ngưỡng +3. Proxy BLEU một mình không đủ để ghi P2 ĐẠT. Nếu
không chấm được CIDEr, phán quyết là **P2 CHƯA ĐẠT — thiếu CIDEr**, dù proxy BLEU có tăng.
