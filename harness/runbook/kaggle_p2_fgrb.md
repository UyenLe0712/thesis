# P2 — FGRB sinh câu trên val — Kaggle T4 ×2, 0 đồng — viết 28/9/2026

Tài liệu gốc: `harness/tai_lieu_2026-09-27/230_ACTION_PROBE_FGRB_CHO_CHAT_LAM_27_9.md` mục P2. Kết quả
P1 và hai quyết định sau P1 (zone lưới 3×3, head khởi tạo từ P1): `report/207` §9–10.

**Lượt này làm gì:** train phần gắn thêm (ba head + codebook + W + cổng u) trên 4.000 bước P1,
Qwen và LoRA S1 đóng băng, rồi sinh câu greedy cho 1.567 bước val ở ba chế độ: `s1` (không tiêm) ·
`fgrb` · `hoanvi` (role/zone hoán vị giữa các mẫu). Không đụng test. Chấm ở máy nhà (`p2_doc.py`).

Ước lượng [suy, từ nhịp P1 1,9 s/forward]: train ~2,2 h · mỗi chế độ sinh ~1,3–1,5 h. GPU 0 làm
train → `fgrb` → `hoanvi` (~5 h); GPU 1 làm `s1` song song (~1,5 h). **Tổng ~5 h**, dưới trần commit.

## A. Chuẩn bị (máy nhà) — đã làm sẵn 28/9

`_bundles/fgrb_p2_script.zip` gồm `p2_fgrb.py`, `p1_probe_fgrb.py` (p2 import hàm từ đây) và
`fgrb_p1_heads_zone3x3.pt` (ba head P1, 0,6 MB). Bundle ảnh **dùng lại `fgrb-p1-bundle`**, không upload lại.

## B. Tạo dataset + notebook

1. Kaggle → **New Dataset**, tên `fgrb-p2-script`, upload `_bundles/fgrb_p2_script.zip`.
2. **New Notebook** → Add Data: `fgrb-p1-bundle` và `fgrb-p2-script`.
3. **Settings → Accelerator: GPU T4 ×2 · Internet: ON** (tải Qwen2.5-VL-3B từ HuggingFace).

## C. Các ô

### Ô 0 — cài thư viện, rồi Restart session

```
!pip install -q -U transformers peft accelerate torchao
```
Chạy xong bấm **Restart session** (giống P1 — thiếu `torchao` mới thì peft lỗi lúc nạp adapter).

### Ô 1 — dò đường dẫn, chép script

```python
import os, shutil
BUNDLE = SCRIPTS = None
for root, dirs, files in os.walk("/kaggle/input"):
    if "adapter_s1_seed101" in dirs and "images" in dirs:
        BUNDLE = root
    if "p2_fgrb.py" in files:
        SCRIPTS = root
assert BUNDLE and SCRIPTS, (BUNDLE, SCRIPTS)
for f in ["p2_fgrb.py", "p1_probe_fgrb.py", "fgrb_p1_heads_zone3x3.pt"]:
    shutil.copy(os.path.join(SCRIPTS, f), "/kaggle/working/" + f)
print("BUNDLE =", BUNDLE)
print("anh:", len(os.listdir(BUNDLE + "/images")), "(can 5567)")
import torch; print("GPU:", torch.cuda.device_count(), "(can 2)")
```
Kỳ vọng: 5.567 ảnh, 2 GPU. Lệch thì dừng.

### Ô 2 — THỬ NHANH trước (tương tác, ~5 phút), đừng bỏ qua

```
!cd /kaggle/working && python p2_fgrb.py --bundle {BUNDLE} --heads fgrb_p1_heads_zone3x3.pt --out /kaggle/working/p2 --limit 3 --log-every 1
```
Phải thấy, theo thứ tự:
- `FGRB: hidden=2048 d_c=256 tham so hoc=... lop=[8, 18, 10]`
- hai dòng `kiem dong nhat ...` rồi **`Kiem dong nhat DAT`** — W = 0 thì FGRB sinh trùng S1 từng ký tự.
  Không có dòng này (hoặc `AssertionError`) ⇒ **dừng, gửi log lại**, đừng commit.
- 3 dòng `train`, rồi `gen s1/fgrb/hoanvi` mỗi chế độ 3 câu, rồi `XONG`.

Số của lượt thử vô nghĩa (ghi vào `p2_limit3/`, tách khỏi lượt thật).

### Ô 3 — lượt thật: Save Version → **Save & Run All (Commit)**

Xoá hoặc comment Ô 2 trước khi commit (commit chạy lại mọi ô). Ô 3:

```python
import subprocess, time, os
os.chdir("/kaggle/working")
common = ["python", "p2_fgrb.py", "--bundle", BUNDLE, "--heads", "fgrb_p1_heads_zone3x3.pt",
          "--out", "/kaggle/working/p2"]
env0 = dict(os.environ, CUDA_VISIBLE_DEVICES="0")
env1 = dict(os.environ, CUDA_VISIBLE_DEVICES="1")
fa = open("log_gpu0.txt", "w"); fb = open("log_gpu1.txt", "w")
A = subprocess.Popen(common + ["--stage", "all", "--modes", "fgrb,hoanvi"], env=env0,
                     stdout=fa, stderr=subprocess.STDOUT)
time.sleep(120)   # để A tải model xong trước, hai tiến trình không cùng tải một lúc
B = subprocess.Popen(common + ["--stage", "gen", "--modes", "s1"], env=env1,
                     stdout=fb, stderr=subprocess.STDOUT)
def tail(p):
    try:
        return open(p).read().strip().splitlines()[-1][:160]
    except Exception:
        return "-"
while A.poll() is None or B.poll() is None:
    print(time.strftime("%H:%M"), "| GPU0:", tail("log_gpu0.txt"), "| GPU1:", tail("log_gpu1.txt"),
          flush=True)
    time.sleep(300)
print("A exit", A.returncode, "| B exit", B.returncode)
print(open("log_gpu0.txt").read()[-3000:])
print(open("log_gpu1.txt").read()[-1500:])
```

Hai tiến trình ghi log **ra tệp** (không đẩy qua stdout của notebook — bài học lượt commit treo 7
giờ vì log ngập), notebook chỉ in một dòng nhịp sống mỗi 5 phút.

## D. Sau khi commit xong

1. Mở version vừa chạy → **Output** → tải cả thư mục `p2/` (`gen_s1.jsonl`, `gen_fgrb.jsonl`,
   `gen_hoanvi.jsonl`, `fgrb_params.pt`) và `log_gpu0.txt`, `log_gpu1.txt`.
2. Đặt vào `runs/fgrb_p2/` trong kho (đúng luật đọc kết quả của `runs/README.md`).
3. Chấm ở máy nhà (CPU, cần Java 8 như `text_metrics_coco.py`, ~5–10 phút vì có bootstrap):
```
~/.venvs/thesis/bin/python harness/p2_doc.py --dir runs/fgrb_p2 --out runs/fgrb_p2/p2_doc.json
```
Hoặc gửi các tệp đó lại cho trợ lý chấm.

## Đọc log khi đang chạy

- `train i/4000 ce ... aux ... gate ... |g*z|/|h| ...`: `ce` phải quanh mức loss của S1 trên câu
  đích (vài phần mười) và **không tăng vọt**; `|g*z|/|h|` là cỡ phần tiêm so với hidden. Nếu nó vẫn
  ~0 ở cuối train thì phần tiêm không học được gì — FGRB sẽ gần như trùng S1.
- ETA in sau mỗi 100 bước. Không có dòng mới sau 15 phút ⇒ mở log xem lỗi.

## Không được làm

- Không mở `test.jsonl` / tệp điểm test. Không train LoRA. Không đổi 4.000 / seed 101.
- Không chọn điểm lưu theo điểm câu (230: một epoch, không chọn epoch bằng BLEU).
- Không trích số val của P2 ra báo — chỉ dùng để phán P2.
