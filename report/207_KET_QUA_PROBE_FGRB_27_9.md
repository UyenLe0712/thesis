# 207 — Kết quả probe FGRB (đóng băng S1): DỪNG Ở P0 — THIẾU ADAPTER S1/101

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
