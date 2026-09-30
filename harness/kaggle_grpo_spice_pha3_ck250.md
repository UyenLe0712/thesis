# Pha 3 — chấm `checkpoint-250` của GRPO SPICE trên val C1 (30/9/2026)

Runbook tự chứa, gom từ 253 §6 (P3-A, P3-C) và 251 §4 Ô 2 (P3-B). Chỉ chấm `checkpoint-250` của
**commit 1**, vì điểm lưu 275–500 của commit 2 không hợp lệ (xem sự cố 30/9 trong
`harness/kaggle_grpo_spice_commit.md`). Số ra là số **val**, cấm trích. Luật đọc: 253 §2
(so S1 greedy SPICE 57,30 trên 400 bước, `exec` 63,45 trên 249 bước click).

Hạn mức dự kiến: chạy thử ~25 phút + commit ~1,5 h. `--gen` nạp điểm lưu bằng
`PeftModel.from_pretrained` (adapter gốc) nên không dính lỗi chạy tiếp của Pha 2.

## Chạy bằng tài khoản Kaggle khác (30/9)

Tài khoản chính đang dùng hạn mức cho lượt train 250 → 500. Muốn chấm song song bằng tài khoản thứ hai:
1. Tài khoản chính: mở version **commit 1** → *Output* → `grpo_spice/checkpoint-250/` → tải
   `adapter_config.json` và `adapter_model.safetensors` (chỉ hai tệp này là đủ cho `--gen`).
2. Máy nhà: đặt vào `ck250_upload/grpo_spice/checkpoint-250/`. Tài khoản thứ hai: *Datasets → New
   Dataset*, kéo **cả thư mục `grpo_spice`** vào, đặt tên `grpo-spice-ck250`, Private.
3. Tài khoản chính: bốn dataset `fgrb-p1-bundle` · `c1-exec8` · `grpo-spice-script` · `thesis-val-cham`
   → *Settings → Sharing* → thêm username tài khoản thứ hai (quyền xem).
4. Tài khoản thứ hai: làm như mục *Chuẩn bị* bên dưới, nhưng input `checkpoint-250` là dataset
   `grpo-spice-ck250` thay cho Notebook Output. Ô 2 tìm theo đường `grpo_spice/checkpoint-250` nên
   vẫn nhận.

## Chuẩn bị

1. Dataset `grpo-spice-script` đã **New Version** bằng `_bundles/grpo-spice-script/`
   (`grpo_spice.py` md5 `d99d03c0c01718283e84ac3851ef5591`).
2. Notebook mới. *Session options*: **GPU T4 ×2**, **Internet On**.
3. *Add Input*:
   - Datasets: `fgrb-p1-bundle`, `c1-exec8`, `grpo-spice-script` (bản mới nhất), `thesis-val-cham`
   - Notebook Output: **version commit 1** của notebook train (cái chạy tới bước ~259).
     ⛔ Không gắn Output commit 2.
4. Dán 6 ô dưới, đúng thứ tự.

### Ô 1 — gói và Java

```python
import subprocess, sys, os, time
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode

sh("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless")
sh("update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java")
sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes pycocoevalcap 'trl==0.29.1' 2>&1 | tail -3")
sh(f'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.get_device_name(0))"')
```

### Ô 2 — đường dẫn, md5, tìm `checkpoint-250`

```python
import os, glob, shutil, hashlib, json

W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "images" in d)
C1 = glob.glob("/kaggle/input/**/c1_mau.jsonl", recursive=True); assert len(C1) == 1, C1; C1 = C1[0]
assert md5(C1) == "d757554326977309c3a65ae0b144c211", "DỪNG: c1_mau.jsonl lệch bản máy nhà"
SRC = [p for p in glob.glob("/kaggle/input/**/grpo_spice.py", recursive=True)
       if not os.path.exists(os.path.join(os.path.dirname(p), "train.log"))]
assert len(SRC) == 1, f"DỪNG: cần đúng một grpo_spice.py của dataset, thấy {SRC}"
for f in ("grpo_spice.py", "build_branch_data.py"):
    shutil.copy(os.path.join(os.path.dirname(SRC[0]), f), f"{W}/{f}")
assert md5(f"{W}/grpo_spice.py") == "d99d03c0c01718283e84ac3851ef5591", "DỪNG: grpo_spice.py là bản cũ, New Version lại dataset"
MERGED = f"{W}/s1_merged"

# tìm theo tệp: Kaggle hay bỏ thư mục ngoài cùng khi upload dataset (30/9: `grpo_spice/` mất)
# loại adapter S1 của fgrb-p1-bundle; adapter GRPO có base_model_name_or_path là s1_merged
def la_grpo(d):
    c = os.path.join(d, "adapter_config.json")
    return os.path.exists(c) and "s1_merged" in json.load(open(c)).get("base_model_name_or_path", "")
CK = [os.path.dirname(f) for f in glob.glob("/kaggle/input/**/adapter_model.safetensors", recursive=True)
      if la_grpo(os.path.dirname(f))]
print("mọi adapter GRPO trong input:", CK)
if len(CK) > 1:                                  # gắn cả Output nhiều điểm lưu thì chỉ lấy checkpoint-250
    CK = [d for d in CK if d.rstrip("/").endswith("checkpoint-250")]
assert len(CK) == 1, f"DỪNG: cần đúng một adapter GRPO checkpoint-250, thấy {CK}"
CK250 = CK[0]
print("checkpoint-250:", CK250, "\n  tệp:", sorted(os.listdir(CK250)))
print("  có thư mục ref/:", os.path.isdir(os.path.join(CK250, "ref")), flush=True)
```

### Ô 3 — hoà S1

```python
r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED],
                   cwd=W, capture_output=True, text=True)
print((r.stdout + r.stderr)[-2000:]); assert r.returncode == 0, "DỪNG: hoà lỗi"
```

### Ô 4 (P3-A) — sinh greedy 400 bước C1 từ `checkpoint-250`

```python
TEST = True          # chạy thử tương tác; đổi False trước khi commit
Q4 = ["--no-q4"]

def chay(cmd, log, cwd, nhip=60):
    t0 = time.time()
    with open(log, "w") as f:
        q = subprocess.Popen(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                             env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1"})
        while q.poll() is None:
            time.sleep(nhip)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"  {(time.time()-t0)/60:5.1f} phút · {os.path.basename(log)} · {L[-1][:110] if L else 'chưa có dòng nào'}", flush=True)
    rc = q.returncode
    print(f"--- {os.path.basename(log)} · mã thoát {rc} · {(time.time()-t0)/60:.1f} phút ---")
    print("".join(open(log, errors="ignore").readlines()[-6:]), flush=True)
    return rc

N = 5 if TEST else 400
out = f"{W}/pred_ck250.jsonl"
chay(["python", "grpo_spice.py", "--gen", "--bundle", BUNDLE, "--merged", MERGED, "--c1", C1,
      "--ckpt", CK250, "--n", str(N), "--out", out] + Q4, f"{W}/gen_ck250.log", W)
n = sum(1 for _ in open(out))
print(f"ck250: {n}/{N} câu", flush=True)
assert n >= N, "DỪNG: thiếu câu, xem gen_ck250.log"
```

Phải thấy dòng `[điểm lưu] …checkpoint-250`, `[so với S1] x/N câu trùng greedy S1` và `N/N câu`.
Nếu mã thoát khác 0 vì `⛔ có câu rỗng` thì tệp vẫn đủ, cứ chạy tiếp.

### Ô 5 (P3-B) — dựng dữ liệu chấm (nguyên văn Ô 2 của 251)

```python
import os, glob, json, shutil, hashlib, sys
W = "/kaggle/working"

cand = sorted({os.path.dirname(p) for p in glob.glob("/kaggle/input/**/c1_picks.json", recursive=True)
               if os.path.exists(os.path.join(os.path.dirname(p), "c1_mau.jsonl"))})
assert len(cand) == 1, f"DỪNG: cần đúng một gói c1-exec8, thấy {cand}"
PK = cand[0]
md5 = hashlib.md5(open(f"{PK}/c1_mau.jsonl", "rb").read()).hexdigest()
assert md5 == "d757554326977309c3a65ae0b144c211", f"DỪNG: c1_mau.jsonl lệch bản máy nhà ({md5})"
WS = f"{W}/pk/thesis"
shutil.copytree(f"{PK}/thesis", WS, dirs_exist_ok=True)
sr = open(f"{WS}/harness/score_run.py", encoding="utf-8").read()
assert "--recs-file" in sr and "TỆP THÔ KHÔNG KHỚP" in sr, "DỪNG: score_run.py là bản cũ"
PICKS = json.load(open(f"{PK}/c1_picks.json", encoding="utf-8"))["picks"]
assert len(PICKS) == 400 and set(PICKS) <= set("012345678"), len(PICKS)

v600 = glob.glob("/kaggle/input/**/val_cham600.jsonl", recursive=True)
assert len(v600) == 1, f"DỪNG: cần đúng một dataset thesis-val-cham, thấy {v600}"
BASE = os.path.dirname(v600[0])
assert os.path.exists(f"{BASE}/val_cham400.jsonl")

C1 = [json.loads(l) for l in open(f"{PK}/c1_mau.jsonl", encoding="utf-8")]
assert len(C1) == 400
assert [(r["episode_id"], r["step_id"]) for r in C1[:3]] == [(11948, 3), (2782, 0), (188, 8)]
TAPT = ("click", "long_press")
assert all(len(r["mau"]) == 8 for r in C1)
assert all(r["greedy"] and all(r["mau"]) for r in C1 if r["action_type"] in TAPT), "DỪNG: câu rỗng ở bước click"
KEYS = {(r["episode_id"], r["step_id"]) for r in C1}

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
    for r in C1:
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
       {(r["episode_id"], r["step_id"]) for r in C1 if r["action_type"] in TAPT}, "DỪNG: action_type lệch"

PD = f"{W}/c1preds"
os.makedirs(PD, exist_ok=True)
for k in range(9):
    with open(f"{PD}/k{k}.jsonl", "w", encoding="utf-8") as fo:
        for r in C1:
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

### Ô 6 (P3-C) — chấm `exec`, kèm chấm lại greedy S1 làm phép kiểm

```python
M = 3 if TEST else 0
for ten, pred in (("k0_lai", f"{W}/c1preds/k0.jsonl"),
                  ("ck250", f"{W}/pred_ck250.jsonl")):
    cmd = ["python", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", pred,
           "--data-root", f"{W}/c1data", "--recs-file", "c1_recs.jsonl", "--out", f"{W}/score_{ten}.json"]
    if M:
        cmd += ["--n", str(M)]
    chay(cmd, f"{W}/cham_{ten}.log", f"{W}/pk/thesis")
    R = [json.loads(l) for l in open(f"{W}/score_{ten}_raw.jsonl")]
    print(f"== {ten}: {len(R)} bước · exec {sum(int(r['executable']) for r in R)}", flush=True)
print("KIỂM (bản đủ): k0_lai phải 249 bước, exec 158 như 251. Lệch thì gửi số về, đừng tự diễn giải.")
```

## Chạy

1. **Chạy thử tương tác** (`TEST = True`): *Run All*, khoảng 20–25 phút. Gửi về output Ô 2, Ô 4 và Ô 6.
   Ở bản thử, `ck250` có 5 câu và mỗi tệp chấm 3 bước.
2. Ổn thì sửa Ô 4 thành `TEST = False` → **tắt phiên tương tác** (*Stop session*, để không tốn hạn mức
   song song) → **Save Version → Save & Run All**. Khoảng 1,5 h.
3. Kiểm cuối log commit: `ck250: 400/400 câu` · `== k0_lai: 249 bước · exec 158` · `== ck250: 249 bước · exec …`.
4. Tải từ Output về `runs/grpo_spice/` trên máy nhà: `pred_ck250.jsonl` · `score_k0_lai_raw.jsonl` ·
   `score_ck250_raw.jsonl` · `score_k0_lai.json` · `score_ck250.json` · `gen_ck250.log` · `cham_*.log`.
   Cùng `train.log` của commit 1 (đổi tên `train_c1.log`).
