# 207 — Kết quả probe FGRB (đóng băng S1): P0 ĐẠT · P1 ĐẠT sát ngưỡng sau khi sửa head (§9) · **P2 TRƯỢT — FGRB DỪNG (§11)**

> ⚠️ Mục 1–7 dưới đây là lượt 27/9 (dừng ở P0 vì thiếu adapter S1/101 và ảnh train). Sau đó đã
> kéo adapter về `runs/s1_seed101/adapter_s1_seed101/` và chạy P1 trên Kaggle T4. **Kết quả P1 ở §8.**

Nguồn hướng dẫn: `harness/tai_lieu_2026-09-27/230_ACTION_PROBE_FGRB_CHO_CHAT_LAM_27_9.md` (chép từ
8 ảnh, đóng vai "chat kia" gọi trong tài liệu — tài liệu viết cho một clone khác vừa tải về, còn
ở đây ta chạy thẳng trên kho làm việc thật). Đây là file kết quả bắt buộc theo mục 6 của tài liệu
230, tự chứa đủ 7 mục yêu cầu.

## 1. Nguyên văn output Phụ lục A (P0 — kiểm nhãn, 0 GPU)

Chạy thật `python3` từ gốc kho, 27/9/2026:

```
train_jsonl 64567
train_tru_val 63000
train_hit 63000
val 1567
train_actions {'open_app': 4349, 'click': 40058, 'scroll': 7031, 'wait': 4592, 'input_text': 4523, 'navigate_back': 2293, 'long_press': 131, 'navigate_home': 23}
val_actions {'input_text': 102, 'click': 1001, 'navigate_back': 57, 'scroll': 164, 'wait': 127, 'open_app': 114, 'navigate_home': 1, 'long_press': 1}
val_click_majority 63.88
```

Đối chiếu với kỳ vọng của tài liệu (`train_jsonl` 64.567, `train_tru_val` 63.000, `train_hit`
63.000, `val` 1.567, click train 40.058, click val 1.001, majority val 63,88%): **khớp tuyệt đối
cả bảy số. P0 (kiểm nhãn) ĐẠT.**

## 2. Bảng kiểm kê đầu vào

| Thứ | Có/Thiếu | Chi tiết |
| --- | --- | --- |
| OCR train | ✅ **CÓ** | `harness/dg1_cache/train_ac/ocr.jsonl`, 64.567 dòng, đủ 1-1 với `train.jsonl`, có khoá theo `(episode_id, step_id)` |
| Ảnh train | ⚠️ **CÓ MỘT PHẦN, KHÔNG ĐỦ** | Phép kiểm nhỏ của tài liệu (`images/ep7057_s1.png` mở được) **qua**, vì đó đúng là ảnh dòng đầu `train.jsonl`. Nhưng đo trên toàn bộ: thư mục `harness/dg1_cache/train_ac/images/` chỉ có **7.625 ảnh**, tức **11,81%** của 64.567 dòng. Trên đúng tập nguồn để lấy mẫu train của P1 (`train_tru_val.jsonl`, 63.000 dòng) chỉ **6.058/63.000 = 9,62%** có ảnh. Val thì đủ: **1.567/1.567 = 100%** có ảnh (nhờ các lượt kéo ảnh val trước đây). |
| Adapter S1/101 | ❌ **THIẾU** | Tìm khắp clone (`runs/`, `_bundles/`, mọi `*.zip` ở `harness/`) bằng `find -iname adapter_config.json` và `find -iname "*s1_seed101*"`: **không có thư mục LoRA nào gắn nhãn S1/101**. Các adapter đang có trong kho (`runs/sel/adapter_gui_sel_seed101`, `runs/grpo_point/adapter_grpo_point_seed101`, `runs/grpo_point/adapter_ref_min`, `runs/noisuy/a0.00`…`a1.00`, `harness/k1_adapter.zip` → `vissft_step03200`) đều là các nhánh **sau** S1 (S2 / CE2 / MIN / GRPO / `gui_sel` / VIS-SFT), không phải bản S1 gốc. Theo `CLAUDE.md`, checkpoint S1/101 gốc từng chỉ nằm ở `MyDrive/thesis/ckpt/s1_seed101` và `/workspace/ckpt/s1_seed101` — hai nơi đó không có bản sao trong kho GitHub này. |

## 3. Phán quyết

> **CHƯA CHẠY — thiếu đầu vào.**

Lý do: adapter S1/101 thiếu tuyệt đối (không có ở đâu trong clone), và ảnh train cũng không đủ
cho tập nguồn lấy mẫu 4.000 bước của P1 (chỉ 9,62% có ảnh) dù ảnh val đủ 100%. Theo đúng mục 0 và
mục "Kiểm kê đầu vào" của tài liệu 230: **dừng tại P0**, không chạy P1, không chạy P2, không train
FGRB, không hạ ngưỡng, không tự tải GitHub Release `data-train-ac-v1`, không tự kéo Google
Drive/`/workspace`, không chạy probe bằng model gốc thay cho adapter S1.

⚠️ Ghi chú trung thực về chính phép kiểm ảnh: tiêu chí kiểm ảnh trong tài liệu 230 chỉ là "file
`images/ep7057_s1.png` mở được" — phép này **tự nó qua** (đúng, file đó tồn tại), nhưng qua đó
không có nghĩa kho ảnh đủ dùng, vì tài liệu ngầm định phép kiểm một-file chỉ là smoke-test cho
việc "đã giải nén release đầy đủ chưa". Ở đây file đó tồn tại là ngẫu nhiên (từ các lượt kéo ảnh
cục bộ trước đó phục vụ việc khác), không phải bằng chứng đã có release đầy đủ. Đã đo lại bằng số
thật (mục 2) thay vì tin phép kiểm một-file, đúng luật của dự án là không tin "đã xác minh" mà
không mở lại số.

## 4–5. P1 / P2

Không áp dụng — chưa chạy vì dừng ở P0.

## 6. Nguyên văn script đã chạy

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

Cộng script kiểm kê ảnh (không có trong tài liệu 230, viết thêm để đo mục 2 cho trung thực,
0 GPU, chỉ đọc `os.listdir` và `train.jsonl`/`train_tru_val.jsonl`):

```python
import json, os
root = "harness/dg1_cache/train_ac"
present = set(os.listdir(root + "/images"))
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
def coverage(rows, name):
    have = sum(1 for r in rows if r["image"].split("/")[-1] in present)
    print(name, len(rows), have, round(100 * have / len(rows), 2), "%")
coverage(tr, "train_tru_val")
coverage(va, "val")
```

## 7. Câu bắt buộc (mục 6.7 của tài liệu 230)

> Probe đạt không có nghĩa FGRB đã là đóng góp. Đóng góp chỉ đứng khi train đầy đủ hơn S1, hơn
> adapter cùng số tham số, hơn bottleneck không phân rã, và shuffle làm điểm giảm.

Ở lượt này câu trên còn chưa tới lượt áp dụng — **probe (P1) còn chưa chạy được**, vì thiếu đúng
cái mốc cần vượt (adapter S1/101) và thiếu phần lớn ảnh train để lấy mẫu.

## Việc cần quyết trước khi đi tiếp (không tự làm)

1. Kéo adapter S1/101 về clone — từ Drive (`MyDrive/thesis/ckpt/s1_seed101`) hoặc từ máy đã thuê
   (`/workspace/ckpt/s1_seed101`), nếu một trong hai còn giữ. Nếu cả hai đã mất, S1/101 phải train
   lại (~23 giờ A100, theo `CLAUDE.md` mục P9) trước khi probe này chạy được.
2. Kéo đủ ảnh cho `train_tru_val.jsonl` (hiện 9,62%) — theo `CLAUDE.md`, ảnh đầy đủ nằm ở GitHub
   Release `data-train-ac-v1` (6 file zip, ~3,5 GB). `harness/keo_anh_val.py` chỉ kéo ảnh val, cần
   một script/tải khác cho ảnh train.
3. Sau khi có đủ hai thứ trên, chạy lại P0 (đã đạt, không cần chạy lại) rồi P1 theo đúng khoá đã
   ghi trong `harness/tai_lieu_2026-09-27/230_ACTION_PROBE_FGRB_CHO_CHAT_LAM_27_9.md` — không đổi
   ngưỡng, không đổi seed, không đổi cỡ mẫu 4.000.

---

## 8. P1 — ĐÃ CHẠY 28/9 (Kaggle T4, `harness/p1_probe_fgrb.py`) — **P1 TRƯỢT**

Trích hidden state: train 4.000 bước mất 126,4 phút, val 1.567 bước mất 49,4 phút (~1,9 s/bước).
Cache vector ghi ra `/kaggle/working/_test5/` (nằm ngoài kho, chưa tải về).

### 8.1 Số theo mục 6 của tài liệu 230 [đo]

`n_train_probe = 4000` · `seed = 101` · val 1.567 bước, không rút mẫu · epoch chọn **29** (macro-F1
trung bình 34,76%).

| đầu | accuracy | recall trên mẫu khác NONE | macro-F1 | gold NONE | dự đoán NONE | ngưỡng | kết quả |
|---|---|---|---|---|---|---|---|
| role | 38,42% | **44,92%** (≈380/846) | 30,98% | 721 | 264 | recall ≥ 50% | ❌ **TRƯỢT** (−5,08) |
| zone | 43,40% | **20,22%** (≈55/272) | 7,39% | 1.295 | 656 | recall ≥ 30% | ❌ **TRƯỢT** (−9,78) |
| action | **80,60%** | – | – | – | – | acc ≥ 73,9% (majority 63,88) | ✅ ĐẠT |

So với baseline chữ (Naive Bayes chỉ dùng goal + history, tài liệu 230 §3): recall role 37,47 → 44,92
(+7,45), recall zone 16,18 → 20,22 (+4,04). Hidden state có ảnh của S1 **có hơn** baseline chữ, nhưng
không tới ngưỡng.

Đọc kèm (tính từ bảng, [đo]):
- **Zone gần như không đọc ra được.** Gold chỉ có 272 bước có zone, nhưng head đoán có zone ở 911 bước;
  macro-F1 7,39% ở mức ngẫu nhiên; accuracy 43,40% thấp hơn hẳn mức đoán toàn NONE (82,64%). Mức recall
  20% có được là nhờ đoán tràn, không phải nhờ đọc được vị trí.
- Role: head đoán NONE ở 264 bước trong khi gold có 721, tức cũng lệch về phía đoán có role (do trọng
  số nghịch đảo tần suất).
- 8 ví dụ sai: phần lớn là nhầm giữa hai loại gần nhau (`option`↔`section`/`image`/`icon`, `section`→`text`)
  hoặc NONE↔có role. Nguyên văn ở log bên dưới.

Phán quyết theo cổng đã khoá: **P1 TRƯỢT** ⇒ không P2, không train FGRB.

### 8.2 ⚠️ Head chưa hội tụ — phán quyết đúng thủ tục nhưng là bằng chứng yếu [đo + suy]

Đọc `p1_probe_fgrb.py:226–266`: ba `Linear` train **full-batch** bằng Adam lr 1e-3, không chuẩn hoá
đặc trưng ⇒ 30 epoch chỉ có đúng **30 bước cập nhật**. Log cho thấy bốn dấu hiệu chưa hội tụ:
1. epoch chọn là **29, tức epoch cuối**; macro-F1 vẫn đang lên (0,3255 → 0,3476 ở hai epoch cuối);
2. loss còn giảm đều ở cuối (2,29 → 2,11);
3. loss lúc đầu **14,17**, trong khi ba head khởi tạo ngẫu nhiên lẽ ra cho khoảng ln 8 + ln 22 + ln 15 ≈ 8
   ⇒ logit đầu đã quá lớn vì đặc trưng chưa chuẩn hoá;
4. loss **tăng** ở epoch 1→3 (13,33 → 15,30) ⇒ lr quá lớn so với thang đặc trưng.

Tài liệu 230 chỉ khoá "tối đa 30 epoch", không khoá cỡ lô hay chuẩn hoá; chọn full-batch là quyết định
của script, không phải của tài liệu. Vì vậy câu đúng là: *với head chỉ 30 bước cập nhật, hidden state
của S1 chưa cho thấy đủ tín hiệu role/zone*. **Chưa được viết** là *"hidden state của S1 không chứa
role/zone"*.

[suy] Role thiếu 5,08 điểm, có thể bù được bằng một head hội tụ. Zone thiếu 9,78 điểm và macro-F1
ở mức ngẫu nhiên, nên khó bù hơn. Điều này khớp với ba kết quả trước đều chỉ ra điểm nghẽn nằm ở khâu
nhận ra *vị trí* (PATA-C1 §5c · PATA-C2 ΔGD ≈ +0,004 · ECGR G0 147/958).

### 8.3 Việc có thể làm tiếp (chưa làm, chờ user quyết)

- **Khớp lại head trên CPU, 0 GPU, vài phút:** tải hai tệp cache (`hiddens_train_seed101.pt`,
  `hiddens_val_seed101.pt`, cỡ ~65 MB + ~25 MB) từ output Kaggle về máy nhà, chuẩn hoá đặc trưng,
  dùng minibatch (hoặc logistic regression) và vẫn giữ 4.000 mẫu, seed 101, tối đa 30 epoch với cùng
  ngưỡng. Phép này là **hậu kiểm sau khi thấy số**, nên phải báo kèm lượt 30 bước ở trên.
  - Zone vẫn trượt ⇒ FGRB đóng hẳn (P1 cần cả ba đầu).
  - Cả ba đầu đạt ⇒ mới tới P2 (Kaggle T4, sinh ba lần × 1.567 câu), sau đó mới xét tới lượt train
    ~45–50 h A100.
- Hoặc chấp nhận dừng FGRB và chuyển sang phương án dự phòng `report/208` (C1 đã có runbook).

### 8.4 Nguyên văn log P1 (phần kết quả)

```
train=4000 val=1567 ocr_keys=5567
epoch 00 loss 14.1726 macroF1 act/role/zone 0.1065/0.0509/0.0065 mean 0.0547
epoch 03 loss 15.3014 macroF1 act/role/zone 0.3048/0.0511/0.0094 mean 0.1218
epoch 19 loss 3.5442 macroF1 act/role/zone 0.6671/0.2459/0.0381 mean 0.3171
epoch 28 loss 2.2883 macroF1 act/role/zone 0.6267/0.2835/0.0663 mean 0.3255
epoch 29 loss 2.1106 macroF1 act/role/zone 0.6590/0.3098/0.0739 mean 0.3476
epoch chon: 29  macro-F1 trung binh: 0.3476
role: accuracy=38.42% recall_khac_NONE=44.92% macroF1=30.98% gold_NONE=721 pred_NONE=264
zone: accuracy=43.40% recall_khac_NONE=20.22% macroF1=7.39% gold_NONE=1295 pred_NONE=656
action: accuracy=80.60% majority=(click, 63.88%)
-- SAI --
  ep=7057 step=1 gold=section pred=text
  ep=14656 step=5 gold=option pred=image
  ep=2607 step=0 gold=NONE pred=image
  ep=2199 step=3 gold=NONE pred=icon
  ep=16229 step=5 gold=option pred=section
  ep=11904 step=0 gold=option pred=NONE
  ep=3668 step=10 gold=NONE pred=view
  ep=13970 step=1 gold=icon pred=option
-- DUNG --
  ep=13970 step=3 gold=option pred=option
  ep=16229 step=0 gold=icon pred=icon
  ep=9803 step=7 gold=text pred=text
  ep=2163 step=0 gold=NONE pred=NONE
  ep=14356 step=3 gold=button pred=button
  ep=1453 step=5 gold=box pred=box
  ep=13545 step=2 gold=option pred=option
  ep=960 step=2 gold=option pred=option
recall_role>=50%: TRUOT (44.92%)
recall_zone>=30%: TRUOT (20.22%)
accuracy_action>=73.9%: DAT (80.60%)
P1 = TRUOT
```
(Log đầy đủ 30 epoch nằm trong output Kaggle; ở đây chỉ trích các dòng mốc.)

Câu bắt buộc (mục 6.7 của 230) vẫn giữ: probe đạt không có nghĩa FGRB đã là đóng góp; ở đây probe còn
chưa đạt.

---

## 9. P1 CHẠY LẠI SAU KHI SỬA HEAD — 28/9, CPU máy nhà, 0 GPU

Cache hidden state tải từ output Kaggle (`harness/results (3).zip`: `_test5/hiddens_train_seed101.pt`
65,5 MB · `hiddens_val_seed101.pt` 25,7 MB). Script chạy trên Kaggle trùng từng byte với bản HEAD
`c6477ee`. Bốn thứ đã sửa trong `harness/p1_probe_fgrb.py`:

1. có cache thì **không nạp Qwen** (trước đó nạp model rồi mới kiểm cache) ⇒ chạy CPU ~10 s;
2. chuẩn hoá z-score, thống kê lấy **chỉ từ train**;
3. minibatch 64 ⇒ 1.890 bước cập nhật thay vì 30; AdamW lr 1e-4, weight decay 1e-2;
4. cố định seed khởi tạo head (`--head-seed`, mặc định 101). Lượt Kaggle **không** cố định seed này.

Không đổi: mẫu 4.000 (seed lấy mẫu 101, đọc nguyên từ bundle), val 1.567, tối đa 30 epoch, trọng số
lớp nghịch đảo tần suất, luật chọn epoch theo macro-F1 trung bình trên val, ba ngưỡng.
⚠️ Cấu hình head mới chọn **sau khi** thấy lượt đầu trượt, và chỉ thử **một** cấu hình (không dò lưới).

### 9.1 Tái lập cách train cũ trên cùng cache [đo]

`--batch-size 0 --no-standardize --lr 1e-3 --weight-decay 0`: role 45,15 · zone 24,26 · **action
72,69** (Kaggle: 44,92 · 20,22 · 80,60). Cùng dữ liệu, chỉ khác lần khởi tạo ngẫu nhiên, mà action
lệch 8 điểm và rơi dưới ngưỡng ⇒ cách train cũ **không ổn định**, phán quyết §8 phụ thuộc may rủi.

### 9.2 Cấu hình đã sửa, năm seed head + đối chứng xáo nhãn [đo]

| chạy | recall role | recall zone (31 lớp gốc) | macro-F1 zone | action | P1 |
|---|---|---|---|---|---|
| **seed 101 (mặc định)** | **51,54** | **30,51** (83/272) | 5,17 | **82,83** | **ĐẠT** |
| seed 102 | 51,18 | 29,41 | 5,22 | 82,45 | trượt (zone) |
| seed 103 | 52,84 | 30,88 | 5,13 | 82,39 | ĐẠT |
| seed 104 | 51,54 | 29,78 | 5,06 | 82,26 | trượt (zone) |
| seed 105 | 52,01 | 30,51 | 5,48 | 82,77 | ĐẠT |
| xáo nhãn train, 3 seed | 6,9–11,2 | 7,7–9,9 | 1,0–1,2 | 10–18 | trượt |

- **Role và action đạt ở cả 5 seed**, cách ngưỡng rõ (role +1,2…+2,8; action +8,4…+8,9).
- **Zone đạt 3/5 seed**, dao động 29,41–30,88 quanh ngưỡng 30 (±1–2 bước trên 272). Có tín hiệu
  thật (xáo nhãn chỉ ~9%), nhưng **qua cổng hay không là do seed**.
- Epoch chọn vẫn là epoch cuối ở 4/5 seed, nhưng macro-F1 val đã phẳng từ khoảng epoch 9
  (0,30–0,32) ⇒ không còn là chuyện chưa hội tụ như §8.

### 9.3 Vì sao zone khó: nhãn chia vụn theo cách viết [đo]

Regex zone của tài liệu 230 lấy nguyên cụm chữ ⇒ **31 lớp** trên train, 25 trên val:
`bottom of the screen` · `bottom` · `lower` · `bottom right corner` · `bottom right corner of the
screen` … là các lớp khác nhau. Head phải đoán đúng **cách viết**, không chỉ đúng vị trí.

Chẩn đoán `--zone-coarse` (gộp về lưới 3×3 + NONE = 10 lớp; **không** dùng để phán P1):

| | recall zone | macro-F1 zone |
|---|---|---|
| gộp 3×3, seed 101–105 | **44,85–48,16** | 17,0–17,9 |
| gộp 3×3, xáo nhãn | 13,24 | 3,83 |

⇒ Hidden state của S1 **có mang thông tin vùng màn** (gấp ~3,5 lần đối chứng), và phần lớn cái yếu
của zone ở §8/§9.2 là do nhãn chia vụn. [suy] Điều này hơi ngược với chuỗi PATA/ECGR (mô hình nhận vị
trí kém): ở đây chỉ là vùng thô 3×3, còn PATA đo phân biệt **phần tử lân cận**, mịn hơn nhiều.
⚠️ Accuracy zone vẫn thấp (32,8% với 31 lớp; 41,9% với 3×3) so với đoán toàn NONE 82,6% vì trọng số
nghịch đảo tần suất đẩy head đoán "có zone" ở 1.000+ bước. FGRB tiêm **phân phối mềm** nên đoán tràn
kiểu này sẽ đi thẳng vào decoder — P2 mới trả lời được nó có hại hay không.

### 9.4 Phán quyết

> **P1 ĐẠT ở cấu hình mặc định (seed 101), nhưng zone chỉ vượt ngưỡng 1 bước và không bền theo seed
> (3/5). Role và action đạt chắc.** Nhãn khi báo: "P1 đạt sát ngưỡng, sau khi sửa cách train head".

Việc kế (chờ user): P2 — sinh câu trên val 1.567 bước, ba lần (S1 không tiêm · FGRB · FGRB hoán vị
role/zone), Kaggle T4. **Mã P2 chưa viết.** Nên quyết trước khi viết: dùng zone 31 lớp như tài liệu
230 khoá, hay zone 3×3 (tín hiệu mạnh hơn hẳn, nhưng là thay đổi sau khi thấy số — phải khai).

Lệnh chạy lại: `harness/kaggle_p1_probe_fgrb.md` mục D.

---

## 10. P2 — thiết kế đã chốt 28/9, CHƯA CHẠY

User chọn zone **lưới 3×3** (*"cái nào mạnh hơn thì làm"*). Mã: `harness/p2_fgrb.py` (Kaggle) ·
`harness/p2_doc.py` (chấm, CPU máy nhà) · runbook `harness/kaggle_p2_fgrb.md` · gói
`_bundles/fgrb_p2_script.zip`.

Theo 230 mục P2, cộng các điểm tự chọn (khai rõ):
- Hook ở **đầu ra norm cuối** của mô hình ngôn ngữ — cùng không gian với đặc trưng P1
  (`hidden_states[-1]` của transformers 5.x là đầu ra sau norm, `tie_last_hidden_states=True`).
  Tiêm từ token cuối của prompt (vị trí sinh token đầu) tới hết câu.
- `z = W[P_a E_a ; P_r E_r ; P_z E_z]`, `d_c = 256`; `h' = h + sigmoid(u·h + b)·z` — thêm bias `b`
  so với công thức 230. **W khởi tạo 0** ⇒ bước 0 FGRB trùng S1; script tự kiểm (sinh 2 câu bật/tắt
  tiêm phải trùng từng ký tự) trước khi train.
- Ba head khởi tạo từ head P1 (zone 3×3, `harness/fgrb_p1_heads_zone3x3.pt`), lr 1e-4; codebook/W/u/b
  lr 1e-3 (230). Loss = CE câu + 1,0 × CE ba head (trọng số lớp như P1). 4.000 bước, 1 epoch, tích
  luỹ 8 ⇒ 500 lần cập nhật. Không chọn điểm lưu theo điểm câu.
- Hoán vị: P_role và P_zone của lượt `fgrb` hoán vị giữa các mẫu val (một hoán vị, seed 101).
- Cổng P2 như 230 (+0,3 BLEU-4 và +3 CIDEr-D so S1 không tiêm; hoán vị thấp hơn ≥0,3 BLEU-4; độ dài
  lệch ≤15%), chấm bằng bộ COCO chính thức, kèm KTC95 bootstrap theo episode.
- Chạy thử CPU máy nhà bị bỏ giữa chừng (máy yếu, user yêu cầu) ⇒ **chưa có lượt thử nào chạy hết**;
  Ô 2 của runbook (`--limit 3` trên Kaggle) là lượt thử đầu tiên.

**Chạy thử `--limit 3` trên Kaggle T4, 28/9: ĐẠT.** fp16, `tham so hoc = 1.731.621`, lớp [8, 18, 10];
kiểm đồng nhất W=0 **trùng từng ký tự** ở 2/2 câu; train ~2 s/bước, sinh ~2 s/câu ⇒ lượt thật ước
~2,2 h train + ~0,9 h mỗi chế độ sinh [suy]. Cảnh báo `requires_grad ... to a scalar` ở dòng ghi
`gate_mean` là vô hại (chỉ để in log).
⚠️ CE của S1 trên 3 câu train đầu chỉ 0,01–0,63: S1 **đã train trên cả 4.000 bước này lẫn 1.567
bước val** (S1 học trọn 64.567 bước). P2 vì vậy so FGRB với một S1 đã thấy chính câu đích ⇒ phép so
**thiên vị chống FGRB**: P2 đạt là bằng chứng mạnh, P2 trượt thì không kết luận chắc được (cùng lập
luận val của `151`/`153`). Đây là giới hạn của thiết kế 230 (cấm mở test), không sửa được trong lượt này.

---

## 11. P2 — KẾT QUẢ 28/9: **P2 TRƯỢT — không train, FGRB dừng**

Kaggle T4 ×2 commit ~4,9 h (train 129 phút; sinh `s1` 77 phút trên GPU1; `fgrb` 68 + `hoanvi` 68 phút
trên GPU0). Script trên Kaggle trùng từng byte với bản trong kho; log 0 lỗi; đủ 3 × 1.567 câu.
Tệp: `runs/fgrb_p2/` (`gen_{s1,fgrb,hoanvi}.jsonl` · `fgrb_params.pt` · `log_gpu0/1.txt` ·
`p2_doc.json`). Chấm: `harness/p2_doc.py`, bộ COCO chính thức, bootstrap 500 lần theo episode.

| | BLEU-4 | CIDEr-D | độ dài TB (từ) |
|---|---|---|---|
| S1 không tiêm | 59,06 | 518,46 | 7,21 |
| FGRB | 59,03 | 517,37 | 7,20 |
| FGRB hoán vị role/zone | 59,15 | 518,23 | 7,20 |

| điều kiện (230) | đo được | KTC95 | kết quả |
|---|---|---|---|
| ① FGRB − S1 ≥ +0,3 BLEU-4 và ≥ +3 CIDEr-D | **−0,03** BLEU-4 · **−1,09** CIDEr-D | [−0,32; +0,19] · [−3,78; +1,92] | ❌ |
| ② FGRB − hoán vị ≥ +0,3 BLEU-4 | **−0,12** | [−0,47; +0,17] | ❌ |
| ③ độ dài lệch ≤ 15% | −0,14% | – | ✅ |

⛔ Số val, **cấm trích ra báo** (val là dữ liệu S1 đã thấy; BLEU-4 val 59,06 so với test 51,56 —
lạc quan ~7,5 điểm, cùng cỡ mức thổi phồng đo ở `153`).

**Vì sao FGRB không làm gì [đo]:**
- Trong lúc train, cổng tự đóng: `gate` 0,50 → 0,27 (bước 100) → 0,03 (bước 500) → 0,05–0,12 ở cuối;
  phần tiêm chỉ bằng **0,06–0,14%** độ lớn hidden suốt lượt. CE câu không giảm (0,70 → 0,60, dao động
  0,49–0,62 cả lượt).
- Lúc sinh, cổng ở token cuối prompt **dưới 5·10⁻⁵** ở mọi câu (in ra 0,0000).
- Chỉ **62/1.567 câu (4,0%)** khác S1, phần lớn khác bề mặt: bỏ/thêm `the`, hoa/thường
  (`OK`→`ok`, `Puma`→`puma`), `search box`→`search bar`. Bản hoán vị cũng chỉ khác FGRB ở 60 câu.
- Hoán vị role/zone giữa các mẫu **không làm điểm giảm** (thậm chí cao hơn 0,12) ⇒ nội dung role/zone
  không đi vào câu.

**Đọc kết quả:** P2 TRƯỢT theo cổng khoá của 230 ⇒ không đề xuất pilot, không train FGRB đầy đủ.
⚠️ Giới hạn (đã ghi §10 trước khi có số): S1 đã train trên cả 4.000 bước train lẫn 1.567 bước val
⇒ CE của S1 trên câu đích đã thấp, gradient cho phần tiêm yếu, và phép so thiên vị chống FGRB. Vì vậy
kết luận đúng là: **"gắn FGRB lên S1 đã đóng băng, học trên dữ liệu S1 đã thấy, không làm câu thay
đổi; cổng tiêm tự đóng"**, chưa phải *"thông tin action/role/zone vô ích cho sinh câu"*. Muốn kiểm
câu sau phải train trên dữ liệu S1 chưa thấy hoặc train cùng LoRA — đều ngoài phạm vi 230 và đều cần
lượt train mới.

Chuỗi này khớp với PATA-C1 (bridge không đổi nội dung câu, `194` §5c): **hai lần liên tiếp, một kênh
gắn thêm vào S1 đã học đầy đủ bị decoder bỏ qua.**

Việc kế: phương án dự phòng `report/208` — C1 ĐẠT 28/9 (chạy song song P2), C3 ĐẠT 27/9; xem `208` §7.
