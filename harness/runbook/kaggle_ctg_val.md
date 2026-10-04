# CTG-GRPO — chấm val C1 cho điểm lưu (K1, K2, chọn điểm lưu), Kaggle T4 (4/10/2026)

Chép từ `kaggle_grpo_spice_pha3_ck500.md` (đường chấm đã tái lập S1 = 158/249), đổi: nhiều điểm lưu một
lượt, adapter lấy từ dataset `ctg-ckpts`. Số ra là **số val, cấm trích**. Đọc bằng `harness/ctg_doc.py`.

| lúc | chấm những tên nào |
|---|---|
| A3 và A2 cùng qua bước 250 | `A3_250`, `A2_250` (K2) |
| cùng qua 500 | `A3_500`, `A2_500` (K1, K2) |
| xong 1000 | `A3_1000`, `A2_1000` (chọn điểm lưu) |
| A4, A7 xong | `A4_500`, `A7_500` (R-CTG: đúng loại không-tap) |

Mỗi tên ~20 phút sinh + ~15 phút chấm trên T4.

## Chuẩn bị

1. Máy nhà: `ctg_ckpt_upload/<TÊN>/adapter_config.json` + `adapter_model.safetensors` (từ Drive
   `thesis/ctg/<ARM>/checkpoint-N/`). Kaggle: dataset **`ctg-ckpts`** (lần đầu *New Dataset*, sau đó
   *New Version*, kéo cả thư mục `ctg_ckpt_upload`).
2. Notebook mới, **GPU T4 ×2**, **Internet On**. *Add Input*: `fgrb-p1-bundle` · `c1-exec8` ·
   `ctg-grpo-script` · `thesis-val-cham` · `ctg-ckpts`.

### Ô 1 — gói

```python
import subprocess, sys, os, time
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes pycocoevalcap 'trl==0.29.1' 2>&1 | tail -3")
```

### Ô 2 — đường dẫn, md5, tìm các điểm lưu

```python
import os, glob, shutil, hashlib, json
TEN = ["A3_250", "A2_250"]                 # ← sửa theo bảng trên
W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "images" in d)
C1 = glob.glob("/kaggle/input/**/c1_mau.jsonl", recursive=True); assert len(C1) == 1, C1; C1 = C1[0]
assert md5(C1) == "d757554326977309c3a65ae0b144c211"
SRC = os.path.dirname(glob.glob("/kaggle/input/**/ctg_grpo.py", recursive=True)[0])
for f in ("grpo_spice.py", "build_branch_data.py"):
    shutil.copy(f"{SRC}/{f}", f"{W}/{f}")
assert md5(f"{W}/grpo_spice.py") == "07ea87b6d156d1faa391a4274dffd7cf"
MERGED = f"{W}/s1_merged"
CK = {}
for t in TEN:
    c = [os.path.dirname(f) for f in glob.glob(f"/kaggle/input/**/{t}/adapter_model.safetensors", recursive=True)]
    assert len(c) == 1, f"DỪNG: không thấy đúng một adapter {t} trong ctg-ckpts: {c}"
    CK[t] = c[0]
print(CK, flush=True)
```

### Ô 3 — hoà S1

```python
r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED],
                   cwd=W, capture_output=True, text=True)
print((r.stdout + r.stderr)[-2000:]); assert r.returncode == 0
```

### Ô 4 — sinh greedy 400 bước C1 cho mỗi điểm lưu

```python
TEST = True          # thử 5 câu; đổi False trước khi commit

def chay(cmd, log, cwd, nhip=60):
    t0 = time.time()
    with open(log, "w") as f:
        q = subprocess.Popen(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                             env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1"})
        while q.poll() is None:
            time.sleep(nhip)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"  {(time.time()-t0)/60:5.1f} phút · {os.path.basename(log)} · {L[-1][:110] if L else ''}", flush=True)
    print(f"--- {os.path.basename(log)} · mã thoát {q.returncode} · {(time.time()-t0)/60:.1f} phút ---")
    print("".join(open(log, errors="ignore").readlines()[-4:]), flush=True)

N = 5 if TEST else 400
for t, ck in CK.items():
    out = f"{W}/pred_{t}.jsonl"
    chay(["python", "grpo_spice.py", "--gen", "--no-q4", "--bundle", BUNDLE, "--merged", MERGED, "--c1", C1,
          "--ckpt", ck, "--n", str(N), "--out", out], f"{W}/gen_{t}.log", W)
    n = sum(1 for _ in open(out)); print(f"{t}: {n}/{N} câu", flush=True); assert n >= N
```

`⛔ có câu rỗng` ở cuối gen làm mã thoát ≠ 0 nhưng tệp vẫn đủ; `ctg_doc.py` đếm câu rỗng cho K3.

### Ô 5 — dựng dữ liệu chấm

Dán **nguyên văn Ô 5 (P3-B)** của `harness/runbook/kaggle_grpo_spice_pha3_ck500.md` (dựng `c1data`, `c1preds/k0..k8`,
tải UGround, kiểm 249 bước click có cây trợ năng).

### Ô 6 — chấm `exec`, kèm chấm lại greedy S1 làm phép kiểm dụng cụ

```python
M = 3 if TEST else 0
for ten, pred in [("k0_lai", f"{W}/c1preds/k0.jsonl")] + [(t, f"{W}/pred_{t}.jsonl") for t in CK]:
    cmd = ["python", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", pred,
           "--data-root", f"{W}/c1data", "--recs-file", "c1_recs.jsonl", "--out", f"{W}/score_{ten}.json"]
    if M: cmd += ["--n", str(M)]
    chay(cmd, f"{W}/cham_{ten}.log", f"{W}/pk/thesis")
    R = [json.loads(l) for l in open(f"{W}/score_{ten}_raw.jsonl")]
    print(f"== {ten}: {len(R)} bước · exec {sum(int(r['executable']) for r in R)}", flush=True)
print("KIỂM (bản đủ): k0_lai phải 249 bước, exec 158. Lệch thì gửi số về, đừng tự diễn giải.")
```

### Ô 7 — gói kết quả

```python
shutil.rmtree(MERGED, ignore_errors=True)
Z = f"{W}/ctg_val_out"; os.makedirs(Z, exist_ok=True)
for p in glob.glob(f"{W}/pred_*.jsonl") + glob.glob(f"{W}/score_*") + glob.glob(f"{W}/*.log"):
    shutil.copy(p, Z)
shutil.make_archive(Z, "zip", Z); print(sorted(os.listdir(Z)))
```

## Chạy

1. `TEST = True`, *Run All* tương tác (~25 phút). Ổn thì `TEST = False` → *Stop session* → **Save Version →
   Save & Run All**.
2. Cuối log: `k0_lai: 249 bước · exec 158` và mỗi tên `249 bước · exec …`.
3. Tải `ctg_val_out.zip`, giải nén vào **`runs/ctg/val/`**, chạy `~/.venvs/thesis/bin/python harness/ctg_doc.py`.
