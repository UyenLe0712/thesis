# C1 — độ đa dạng mẫu của S1/101 trên 400 bước val — Kaggle T4, 0 đồng — viết 27/9/2026

Cổng C1 của `report/208` §4 và §6. Câu hỏi: S1 lấy mẫu 8 câu có đủ khác nhau để một lượt học từ
phần thưởng câu (GRPO hoặc lọc mẫu) nhận được tín hiệu không. Chưa đạt thì **không đặt lượt A100 nào**.
Cổng C3 (0-GPU) đã ĐẠT 27/9 — `runs/c3_nhieu_nguoi_nghe.json`.

Ước: ~10–15 s/bước × 400 ≈ **1–1,5 h T4** + ~5 phút tải Qwen2.5-VL-3B. Không mở test.

## A. Dữ liệu (máy nhà → Kaggle)

1. Dataset `fgrb-p1-bundle` **đã có sẵn** (adapter S1/101, ảnh, OCR, 1.567 bước val) — dùng lại,
   không upload lại.
2. Tải `_bundles/c1_script.zip` (18 KB: `c1_mau_s1.py` + `build_branch_data.py`) → **New Dataset**,
   tên `c1-script`.
3. Notebook mới → Add Data: `fgrb-p1-bundle` + `c1-script`.
   Settings: **GPU T4 ×1 · Internet ON**.
   ⚠️ Nếu FGRB đang chiếm phiên GPU và Kaggle không cho phiên thứ hai thì chờ FGRB xong.

## B′. ⭐ CHẠY DẠNG COMMIT (Save Version → Save & Run All) — cách user chọn 27/9

Notebook chỉ có **ba ô dưới đây**, không thêm ô nào khác. Settings trước khi bấm: **GPU T4 ×1 ·
Internet ON** (commit chạy theo cấu hình đã lưu của notebook, không theo phiên đang mở).

Khác chạy tương tác:
- Không restart được ⇒ script chạy bằng **tiến trình Python con**, nó nạp thư viện vừa cài.
- Không có ô theo dõi ⇒ vòng chờ in nhịp sống mỗi 2 phút **ngay trong ô chạy**. Ô đó phải chờ
  tiến trình xong; ô kết thúc sớm là notebook kết thúc và tiến trình bị giết.
- Thử 3 bước **tự động** ở đầu ô 3; hỏng là `assert` dừng cả commit (mất ~5 phút, không phải 1,5 h).
- Kết quả phải nằm thẳng trong `/kaggle/working` mới lên tab Output.

### Ô 1 (commit) — cài gói
```python
!pip install -q -U transformers peft accelerate torchao 2>&1 | tail -2
import subprocess
print(subprocess.run(["python", "-c", "import transformers, peft, torchao, torch; print(transformers.__version__, "
      "peft.__version__, torchao.__version__, torch.cuda.get_device_name(0))"],
      capture_output=True, text=True).stdout)
```
`| tail -2` bắt buộc (log ngập làm treo commit). Dòng in ra là phiên bản mà **tiến trình con** thấy.

### Ô 2 (commit) — dò đường dẫn, chép script, kiểm dấu vân tay
```python
import os, shutil, glob
BUNDLE = None
for root, dirs, files in os.walk("/kaggle/input"):
    if "adapter_s1_seed101" in dirs and "images" in dirs:
        BUNDLE = root; break
assert BUNDLE, "DỪNG: chưa Add Data fgrb-p1-bundle"
src = [q for q in glob.glob("/kaggle/input/**/c1_mau_s1.py", recursive=True)
       if "SEED_CHON = 20260927" in open(q, encoding="utf-8").read()]
assert len(src) == 1, f"DỪNG: cần đúng một bản c1_mau_s1.py có dấu vân tay, thấy {src}"
d = os.path.dirname(src[0])
for f in ["c1_mau_s1.py", "build_branch_data.py"]:
    shutil.copy(os.path.join(d, f), "/kaggle/working/" + f)
print("BUNDLE =", BUNDLE, "· script từ", d)
print("ảnh:", len(os.listdir(BUNDLE + "/images")), "(kỳ vọng 5567)")
```

### Ô 3 (commit) — thử 3 bước, rồi chạy đủ 400 bước
```python
import subprocess, time, os, json
W = "/kaggle/working"
env = dict(os.environ, TQDM_DISABLE="1", HF_HUB_DISABLE_PROGRESS_BARS="1")

def chay(args, log_name):
    log = open(f"{W}/{log_name}", "a")
    p = subprocess.Popen(["python", "c1_mau_s1.py", "--bundle", BUNDLE] + args, cwd=W, env=env,
                         stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    t0 = time.time()
    while p.poll() is None:
        time.sleep(120)
        f = args[args.index("--out") + 1]
        n = sum(1 for _ in open(f)) if os.path.exists(f) else 0
        print(f"[{(time.time()-t0)/60:5.1f} phút] {log_name}: {n} bước", flush=True)
        if time.time() - t0 > 8 * 3600:          # đệm dưới trần ~12 h; tệp ghi dần nên giữ được phần đã xong
            p.terminate(); print("⛔ quá 8 h — dừng, giữ phần đã ghi", flush=True)
    log.close()
    print(open(f"{W}/{log_name}").read()[-1200:], flush=True)
    return p.returncode

# ① thử 3 bước — hỏng là dừng cả commit
assert chay(["--out", f"{W}/c1_thu.jsonl", "--n", "3"], "c1_thu.log") == 0, "DỪNG: lượt thử lỗi, xem c1_thu.log"
thu = [json.loads(l) for l in open(f"{W}/c1_thu.jsonl")]
assert len(thu) == 3 and all(x["greedy"] and len(x["mau"]) == 8 and all(x["mau"]) for x in thu), \
    "DỪNG: câu greedy hoặc mẫu rỗng"
for x in thu:
    print("VÀNG:", x["gold"], "| GREEDY:", x["greedy"]); print("   MẪU:", x["mau"][:3])

# ② chạy đủ
rc = chay(["--out", f"{W}/c1_mau.jsonl"], "c1.log")
n = sum(1 for _ in open(f"{W}/c1_mau.jsonl"))
print("mã thoát", rc, "·", n, "/ 400 bước", "✅" if n == 400 else "⚠️ CHƯA ĐỦ — commit lại, script tự nối tiếp")
```

### Trước khi bấm Save Version — kiểm bốn dòng
1. Input có **`fgrb-p1-bundle`** và **`c1-script`**.
2. Accelerator **GPU T4** (×1 là đủ), Internet **ON**.
3. Notebook chỉ có ba ô trên.
4. Save & Run All (Commit).

Xong: tab **Output** của version có `c1_mau.jsonl`, `c1.log`, `c1_thu.jsonl`, `c1_thu.log`. Tải
`c1_mau.jsonl` + `c1.log` về **`runs/c1/`**. Đọc ở mục C.
Chưa đủ 400 (bị cắt): tải `c1_mau.jsonl` về, gửi mình — sẽ thêm bước gắn Output cũ làm input để nối tiếp.

---

## B. Ô lệnh (chạy TƯƠNG TÁC — chỉ dùng nếu không commit)

### Ô 0 — cài thư viện, rồi Restart session
```
!pip install -q -U transformers peft accelerate torchao
```
Giống runbook FGRB (`torchao` bắt buộc, nếu không `peft` mới ném ImportError). **Restart session**.

### Ô 1 — dò đường dẫn, chép script
```python
import os, shutil
BUNDLE = SCRIPT_DIR = None
for root, dirs, files in os.walk("/kaggle/input"):
    if "adapter_s1_seed101" in dirs and "images" in dirs: BUNDLE = BUNDLE or root
    if "c1_mau_s1.py" in files: SCRIPT_DIR = SCRIPT_DIR or root
assert BUNDLE and SCRIPT_DIR, (BUNDLE, SCRIPT_DIR)
for f in ["c1_mau_s1.py", "build_branch_data.py"]:
    shutil.copy(os.path.join(SCRIPT_DIR, f), "/kaggle/working/" + f)
print("BUNDLE =", BUNDLE); print(sorted(os.listdir("/kaggle/working")))
```
Kỳ vọng: in đường dẫn bundle; `/kaggle/working` có hai file `.py`.

### Ô 2 — THỬ 5 bước (bắt buộc, ~5–8 phút gồm tải model)
```
!cd /kaggle/working && python c1_mau_s1.py --bundle {BUNDLE} --out /kaggle/working/c1_thu.jsonl --n 5
```
Kiểm ba dòng:
- `[dữ liệu] val=1567 · chọn 5 bước (seed 20260927) ...`
- `[cấu hình] ... lấy mẫu: {'do_sample': True, 'temperature': 1.0, 'top_p': 1.0, 'top_k': 0, 'repetition_penalty': 1.0, 'num_return_sequences': 8, ...}` — **phải thấy đúng dòng này**, không kiểm mã.
- dòng `5/5 · ... ví dụ greedy: '...'` là một câu tiếng Anh ngắn kiểu `click on ...`.

Rồi xem nhanh:
```python
import json; d=[json.loads(l) for l in open("/kaggle/working/c1_thu.jsonl")]
for x in d[:2]: print(x["gold"], "|", x["greedy"]); print("  ", x["mau"])
```
Greedy rỗng, lặp vô nghĩa, hay 8 mẫu là rác ⇒ **dừng, gửi lại output**, đừng chạy Ô 3.

### Ô 3 — chạy đủ 400 bước (chạy nền, có nhịp sống)
```python
import subprocess, time, os
log = open("/kaggle/working/c1.log", "a")
p = subprocess.Popen(["python", "c1_mau_s1.py", "--bundle", BUNDLE, "--out", "/kaggle/working/c1_mau.jsonl"],
                     cwd="/kaggle/working", stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
t0 = time.time()
while p.poll() is None:
    time.sleep(120)
    n = sum(1 for _ in open("/kaggle/working/c1_mau.jsonl")) if os.path.exists("/kaggle/working/c1_mau.jsonl") else 0
    print(f"[{(time.time()-t0)/60:5.1f} phút] {n}/400 bước", flush=True)
print("mã thoát", p.returncode); print(open("/kaggle/working/c1.log").read()[-1500:])
```
- Không thấy số bước tăng sau ~6 phút (đã qua tải model) ⇒ dừng, mở `c1.log`.
- Đứt phiên: chạy lại Ô 1 + Ô 3; script tự bỏ các bước đã có trong `c1_mau.jsonl`.

### Ô 4 — tải kết quả
Tải `/kaggle/working/c1_mau.jsonl` (và `c1.log`) về, đặt vào **`runs/c1/`** trong kho.

## C. Đọc trên máy nhà (CPU)
```
~/.venvs/thesis/bin/python harness/c1_doc.py runs/c1/c1_mau.jsonl
```
Luật đạt (ghi trong `c1_doc.py`, trước khi có số): best-of-8 CIDEr-D ≥ 1,05 × greedy **và** nhóm có
độ lệch chuẩn CIDEr bằng 0 ≤ 50%. ⛔ Val là dữ liệu S1 đã thấy ⇒ không trích số nào ra báo.
Kiểm đường đọc đã làm 27/9 trên dữ liệu giả (8 nhánh làm "8 mẫu"): chạy đúng, 21,8% nhóm giống hệt.
