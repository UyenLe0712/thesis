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

## Bước 0 — đóng zip điểm lưu (Colab, runtime **CPU**, ~5 phút)

Lượt train đã tự trả máy (`TAT_MAY`), nên lấy từ Drive. Mở notebook mới, *Change runtime type → CPU*, chạy:

```python
N = 1000                                   # ← mốc cần chấm
from google.colab import drive; drive.mount("/content/drive")
import os, shutil, hashlib, zipfile
D = "/content/drive/MyDrive/thesis/ctg"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
U = f"/content/ctg_ckpt_upload"; shutil.rmtree(U, ignore_errors=True)
for A in ("A3", "A2"):
    c = f"{D}/{A}/checkpoint-{N}"
    for f in ("ctg_state.json", "adapter_config.json", "adapter_model.safetensors"):
        assert os.path.exists(f"{c}/{f}"), f"DỪNG: thiếu {c}/{f}"
    os.makedirs(f"{U}/{A}_{N}")
    for f in ("adapter_config.json", "adapter_model.safetensors"):
        shutil.copy(f"{c}/{f}", f"{U}/{A}_{N}/{f}")
    h = md5(f"{U}/{A}_{N}/adapter_model.safetensors")
    fin = f"{D}/{A}/final/adapter_model.safetensors"
    # final/ và checkpoint-1000 cùng một bước nên thường trùng; lệch thì chỉ báo, vẫn dùng checkpoint
    print(A, "md5", h, "· final/", ("trùng" if os.path.exists(fin) and md5(fin) == h else "KHÁC hoặc không có") if N == 1000 else "")
H = {A: md5(f"{U}/{A}_{N}/adapter_model.safetensors") for A in ("A3", "A2")}
assert H["A3"] != H["A2"], "DỪNG: hai nhánh cùng một adapter"
Z = f"/content/ctg_ckpt_{N}.zip"
with zipfile.ZipFile(Z, "w", zipfile.ZIP_STORED) as z:
    for A in ("A3", "A2"):
        for f in ("adapter_config.json", "adapter_model.safetensors"):
            z.write(f"{U}/{A}_{N}/{f}", f"{A}_{N}/{f}")
print(zipfile.ZipFile(Z).namelist())
shutil.copy(Z, f"{D}/ctg_ckpt_{N}.zip"); print("đã chép:", f"{D}/ctg_ckpt_{N}.zip", os.path.getsize(Z) // 2**20, "MB")
```

Kiểm: 4 tệp trong zip, hai md5 khác nhau. Tải `MyDrive/thesis/ctg/ctg_ckpt_1000.zip` về → Kaggle dataset
**`ctg-ckpts` → New Version** → kéo zip vào (Kaggle tự giải nén) → thấy `A3_1000/` và `A2_1000/`.

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
TEN = ["A3_1000", "A2_1000"]               # ← sửa theo bảng trên (đã chấm: 250, 500)
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

Chép từ Ô 5 (P3-B) của `kaggle_grpo_spice_pha3_ck500.md` (5/10: chép thẳng vào đây sau khi bỏ sót ô này làm Ô 6
báo `No such file: /kaggle/working/pk/thesis`; đổi `C1`→`C1R`, `md5`→`m5` để không đè biến của Ô 2).
Dựng `pk/thesis`, `c1data`, `c1preds/k0..k8`, tải UGround, kiểm 249 bước click có cây trợ năng.

```python
import os, glob, json, shutil, hashlib, sys
W = "/kaggle/working"

cand = sorted({os.path.dirname(p) for p in glob.glob("/kaggle/input/**/c1_picks.json", recursive=True)
               if os.path.exists(os.path.join(os.path.dirname(p), "c1_mau.jsonl"))})
assert len(cand) == 1, f"DỪNG: cần đúng một gói c1-exec8, thấy {cand}"
PK = cand[0]
m5 = hashlib.md5(open(f"{PK}/c1_mau.jsonl", "rb").read()).hexdigest()
assert m5 == "d757554326977309c3a65ae0b144c211", f"DỪNG: c1_mau.jsonl lệch bản máy nhà ({m5})"
WS = f"{W}/pk/thesis"
shutil.copytree(f"{PK}/thesis", WS, dirs_exist_ok=True)
sr = open(f"{WS}/harness/score_run.py", encoding="utf-8").read()
assert "--recs-file" in sr and "TỆP THÔ KHÔNG KHỚP" in sr, "DỪNG: score_run.py là bản cũ"
PICKS = json.load(open(f"{PK}/c1_picks.json", encoding="utf-8"))["picks"]
assert len(PICKS) == 400 and set(PICKS) <= set("012345678"), len(PICKS)

# 1/10: dataset thesis-val-cham của tài khoản thứ hai có hai bản (gốc + thư mục lồng) ⇒ chỉ lấy thư mục
# đủ bộ (val400 · ocr · images), nếu vẫn nhiều bản thì các bản phải trùng md5 rồi lấy bản đầu
v600 = sorted(glob.glob("/kaggle/input/**/val_cham600.jsonl", recursive=True), key=len)
v600 = [p for p in v600 if all(os.path.exists(os.path.join(os.path.dirname(p), f))
                                for f in ("val_cham400.jsonl", "ocr.jsonl", "images"))]
assert v600, "DỪNG: không thấy thư mục thesis-val-cham đủ bộ (val_cham400 · ocr · images)"
h = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
for f in ("val_cham400.jsonl", "val_cham600.jsonl", "ocr.jsonl"):
    assert len({h(os.path.join(os.path.dirname(p), f)) for p in v600}) == 1, f"DỪNG: các bản thesis-val-cham lệch nhau ở {f}"
BASE = os.path.dirname(v600[0])
print("thesis-val-cham:", BASE, f"({len(v600)} bản đủ bộ, trùng md5)", flush=True)

C1R = [json.loads(l) for l in open(f"{PK}/c1_mau.jsonl", encoding="utf-8")]
assert len(C1R) == 400
assert [(r["episode_id"], r["step_id"]) for r in C1R[:3]] == [(11948, 3), (2782, 0), (188, 8)]
TAPT = ("click", "long_press")
assert all(len(r["mau"]) == 8 for r in C1R)
assert all(r["greedy"] and all(r["mau"]) for r in C1R if r["action_type"] in TAPT), "DỪNG: câu rỗng ở bước click"
KEYS = {(r["episode_id"], r["step_id"]) for r in C1R}

VD = f"{W}/c1data"
os.makedirs(VD, exist_ok=True)
recs = {}
for f in ("val_cham400.jsonl", "val_cham600.jsonl"):
    for d in map(json.loads, open(f"{BASE}/{f}", encoding="utf-8")):
        k = (d["episode_id"], d["step_id"])
        if k in KEYS and k not in recs:
            d.setdefault("gold_instruction", d["target_instruction"])
            recs[k] = d
assert len(recs) == 400, f"DỪNG: chỉ ghép được {len(recs)}/400 bước C1"
with open(f"{VD}/c1_recs.jsonl", "w", encoding="utf-8") as fo:
    for r in C1R:
        fo.write(json.dumps(recs[(r["episode_id"], r["step_id"])], ensure_ascii=False) + "\n")
shutil.copy(f"{BASE}/ocr.jsonl", f"{VD}/ocr.jsonl")
if os.path.lexists(f"{VD}/images"):
    os.remove(f"{VD}/images")
os.symlink(f"{BASE}/images", f"{VD}/images")

taps = [d for d in recs.values() if d["action"].get("action_type") in TAPT and "x" in d["action"]]
thieu = [d["image"] for d in taps if not os.path.exists(f"{VD}/{d['image']}")]
print("bước C1:", len(recs), "| click:", len(taps), "(cần 249) | ảnh thiếu:", len(thieu), "(cần 0)", flush=True)
assert len(taps) == 249 and not thieu
assert {(d["episode_id"], d["step_id"]) for d in taps} == \
       {(r["episode_id"], r["step_id"]) for r in C1R if r["action_type"] in TAPT}, "DỪNG: action_type lệch"

PD = f"{W}/c1preds"
os.makedirs(PD, exist_ok=True)
for k in range(9):
    with open(f"{PD}/k{k}.jsonl", "w", encoding="utf-8") as fo:
        for r in C1R:
            s = r["greedy"] if k == 0 else r["mau"][k - 1]
            fo.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "pred": s},
                                ensure_ascii=False) + "\n")
OUT = f"{W}/c1score"
os.makedirs(OUT, exist_ok=True)
print("9 tệp câu:", sorted(os.listdir(PD)), flush=True)

from huggingface_hub import snapshot_download
print("UGround:", snapshot_download("osunlp/UGround-V1-2B"), flush=True)
sys.path.insert(0, f"{WS}/harness")
import a11y_inventory as A11Y, score_run as SR
names = set(A11Y._zip().namelist())
co_cay = sum(A11Y.key_for(f"episode_{d['episode_id']}_screenshot_{d['step_id']}.png") in names for d in taps)
rong = sum(len(SR.buttons_of(d)) == 0 for d in taps)
print(f"cây trợ năng: {co_cay}/249 bước click · {rong} bước rỗng nút", flush=True)
assert co_cay == 249 and rong == 0, "DỪNG: thiếu cây trợ năng ⇒ Voronoi chấm sai mà không báo"
```

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
3. Tải `ctg_val_out.zip`, đổi tên thành `ctg_val_out_1000.zip`, đặt vào **`runs/ctg/val/`**, giải nén tại chỗ (`unzip -o`), chạy `~/.venvs/thesis/bin/python harness/ctg_doc.py`. Gửi Claude phần in ra.
