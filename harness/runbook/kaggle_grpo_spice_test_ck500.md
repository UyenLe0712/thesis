# Chấm TEST một lần cho `checkpoint-500` của GRPO SPICE (action 258, 1/10/2026)

Bản chạy được của `harness/tai_lieu_2026-10-01/258_ACTION_CHAM_TEST_CK500_extracted.md` (chép từ 5 ảnh). Luật đọc giữ
nguyên **258 §0**, khoá trước khi có số. Mốc: S1/101 trên 4.463 bước click (exec 59,11 · SPICE 44,37 ·
action_ok 94,35). ⛔ Chấm **một lần**: không xem số rồi sinh lại, đổi điểm lưu hay đổi nhiệt độ.

## Sáu chỗ sửa so với 258 (kiểm trên WSL 1/10)

| # | 258 viết | sửa | vì sao |
|---|---|---|---|
| 1 | `grpo_spice.map(a)` | `grpo_spice.nap(a)` | lỗi chép ảnh; `grpo_spice.py` không có hàm `map` ⇒ AttributeError ngay |
| 2 | `one(".../build_branch_data.py")` | lấy cạnh `grpo_spice.py` của dataset script | `thesis-score` cũng có `build_branch_data.py` ⇒ 2 kết quả, assert chết |
| 3 | `score_run.py --data-root --recs-file` | gọi `score_run.py` **bản trong `thesis-score`**, không cờ đó | bản đó cũ, không có hai cờ này (argparse lỗi); nhưng chính nó đã chấm S1 59,11 ⇒ cùng dụng cụ với mốc |
| 4 | ô 3 dán tay ~100 dòng | tệp `gen_test_grpo.py` trong dataset script | thêm in `[dữ liệu]`, kiểm thiếu ảnh, s/bước; chạy khô trên WSL đạt (4.463 bước, thiếu OCR 0, thiếu ảnh 0) |
| 5 | kiểm hoà trên 20 bản ghi đầu bất kỳ | 20 bước **click** đầu | đó là bước sẽ chấm |
| 6 | ô 5 cắt ở 11 h | cắt ở **6 h** | sinh ~3,7 h (val đo 2,95 s/bước) + chấm ~5,4 h (val đo 0,23 bước/s) ≈ 9,4 h; sinh mà quá 6 h thì không còn đủ giờ chấm |

Thêm: bảng mốc của 258 bị OCR đọc sai tên — "Hộp phản từ (0.3)" là **D.3** 65,49; "A11y đầy đủ" là
**AitW đầy đủ** 74,37; action_ok S1 tính lại từ tệp thô là 94,35. Phụ lục máy nhà của 258 bị cắt và
trỏ đường Mac ⇒ đọc bằng script WSL, viết sau khi có tệp (0 GPU).

## Chuẩn bị (máy nhà → Kaggle)

1. Dataset **`grpo-spice-script` → New Version**, kéo cả 4 tệp trong `_bundles/grpo-spice-script/`:
   `grpo_spice.py` (md5 `07ea87b6…`) · `build_branch_data.py` · **`gen_test_grpo.py`** (mới,
   md5 `9348444b6dd0ee11d53d95156a6922d2`) · **`preds_s1_seed101.jsonl`** (mới, 6.958 dòng, để kiểm hoà).
2. Notebook mới. *Session options*: **GPU T4** (×1 hay ×2 đều được, mã chỉ dùng card 0), **Internet On**.
3. *Add Input*: `thesis-score` · `fgrb-p1-bundle` · `grpo-spice-script` (bản mới) · `grpo-spice-ck500`.
   Không cần `c1-exec8`, `thesis-val-cham`.

## Ô 1 — gói (giống hệt Pha 3, để cùng môi trường với lượt val)

```python
import subprocess, sys, os, time
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode

sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes pycocoevalcap 'trl==0.29.1' 2>&1 | tail -3")
sh(f'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.get_device_name(0))"')
```

## Ô 2 — đường dẫn và kiểm đầu vào

```python
import os, glob, json, shutil, hashlib
W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()

# dataset script: chỉ nhận thư mục có đủ 4 tệp (loại grpo_spice.py nằm trong output train)
SRC = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/gen_test_grpo.py", recursive=True)
       if all(os.path.exists(os.path.join(os.path.dirname(p), f))
              for f in ("grpo_spice.py", "build_branch_data.py", "preds_s1_seed101.jsonl"))]
assert len(SRC) == 1, f"DỪNG: cần đúng một grpo-spice-script bản mới, thấy {SRC}"
SRC = SRC[0]
for f in ("grpo_spice.py", "build_branch_data.py", "gen_test_grpo.py"):
    shutil.copy(f"{SRC}/{f}", f"{W}/{f}")
assert md5(f"{W}/grpo_spice.py") == "07ea87b6d156d1faa391a4274dffd7cf", "DỪNG: grpo_spice.py bản cũ"
assert md5(f"{W}/gen_test_grpo.py") == "9348444b6dd0ee11d53d95156a6922d2", "DỪNG: gen_test_grpo.py lệch máy nhà"
S1P = f"{SRC}/preds_s1_seed101.jsonl"
assert sum(1 for _ in open(S1P)) == 6958

BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d)
MERGED = f"{W}/s1_merged"

def la_grpo(d):
    c = os.path.join(d, "adapter_config.json")
    return os.path.exists(c) and "s1_merged" in json.load(open(c)).get("base_model_name_or_path", "")
CK = [os.path.dirname(f) for f in glob.glob("/kaggle/input/**/adapter_model.safetensors", recursive=True)
      if la_grpo(os.path.dirname(f))]
assert len(CK) == 1, f"DỪNG: cần đúng một adapter GRPO, thấy {CK}"
CK500 = CK[0]
assert md5(f"{CK500}/adapter_model.safetensors") == "491fa6677340393f1e4464c08a0cec98", "DỪNG: không phải ck500 đã chấm val"

# thesis-score: gói mã cũ (score_run đã chấm S1 59,11) + test_ac đủ ảnh
best = None
for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True):
    root = os.path.dirname(t)
    nimg = len(glob.glob(f"{root}/images/*.png"))
    if sum(1 for _ in open(t)) == 6958 and nimg >= 4463 and os.path.exists(f"{root}/ocr.jsonl"):
        best = root
assert best, "DỪNG: không thấy test_ac đủ 6.958 dòng + 4.463 ảnh"
TA = best
assert md5(f"{TA}/test.jsonl") == "da58299ee551a926a21cbecb5232bf78", "DỪNG: test.jsonl lệch máy nhà"
PKG = os.path.dirname(os.path.dirname(os.path.dirname(TA)))          # …/thesis/harness/dg1_cache/test_ac → …/thesis
shutil.copytree(f"{PKG}/harness", f"{W}/thesis/harness", dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("images"))
link = f"{W}/thesis/harness/dg1_cache/test_ac/images"
if os.path.lexists(link): os.remove(link)
os.symlink(f"{TA}/images", link)
WS = f"{W}/thesis"

print("SRC   ", SRC); print("BUNDLE", BUNDLE); print("CK500 ", CK500); print("TA    ", TA)
print("có thư mục ref/ trong ck500:", os.path.isdir(f"{CK500}/ref"), flush=True)
```

Phải thấy 4 đường dẫn, không dòng DỪNG nào.

## Ô 3 — hoà S1 + hàm chạy có nhịp sống

```python
TEST = True          # chạy thử tương tác; đổi False trước khi commit

def chay(cmd, log, cwd, nhip=120, tran_gio=None):
    t0 = time.time()
    with open(log, "w") as f:
        q = subprocess.Popen(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                             env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
                                  "PYTHONUNBUFFERED": "1"})
        while q.poll() is None:
            time.sleep(nhip if not TEST else 30)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"  {(time.time()-t0)/3600:5.2f} h · {os.path.basename(log)} · {L[-1][:110] if L else 'chưa có dòng nào'}", flush=True)
            if tran_gio and time.time() - t0 > tran_gio * 3600:
                q.terminate(); print(f"⛔ cắt ở {tran_gio} h để còn giờ chấm", flush=True); break
    print(f"--- {os.path.basename(log)} · mã thoát {q.returncode} · {(time.time()-t0)/3600:.2f} h ---")
    print("".join(open(log, errors="ignore").readlines()[-6:]), flush=True)
    return q.returncode

r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED],
                   cwd=W, capture_output=True, text=True)
print((r.stdout + r.stderr)[-1500:]); assert r.returncode == 0, "DỪNG: hoà lỗi"
```

## Ô 4 — kiểm hoà: 20 bước click, KHÔNG gắn điểm lưu

```python
TA_ARGS = ["--recs", f"{TA}/test.jsonl", "--ocr", f"{TA}/ocr.jsonl", "--images", f"{TA}/images", "--tap-only", "--no-q4"]
out = f"{W}/kiem_hoa_test.jsonl"
if os.path.exists(out): os.remove(out)
chay(["python", "gen_test_grpo.py", "--bundle", BUNDLE, "--merged", MERGED, "--s1", S1P,
      "--n", "20", "--out", out] + TA_ARGS, f"{W}/kiem_hoa_test.log", W)
dong = [l for l in open(f"{W}/kiem_hoa_test.log") if "[kiểm hoà]" in l]
print(dong)
x = int(dong[-1].split("]")[1].split("/")[0])
assert x >= 16, f"DỪNG: kiểm hoà {x}/20 < 16 — đừng gắn điểm lưu, gửi log về"
```

## Ô 5 — sinh 4.463 câu click từ `checkpoint-500`

```python
PRED = f"{W}/pred_ck500_test{'_thu' if TEST else ''}.jsonl"
chay(["python", "gen_test_grpo.py", "--bundle", BUNDLE, "--merged", MERGED, "--ckpt", CK500,
      "--out", PRED] + (["--n", "5"] if TEST else []) + TA_ARGS,
     f"{W}/gen_test{'_thu' if TEST else ''}.log", W, tran_gio=6)
n = sum(1 for _ in open(PRED))
print(f"ck500 test: {n}/{5 if TEST else 4463} câu", flush=True)
assert n == (5 if TEST else 4463), "DỪNG: thiếu câu — chạy lại ô này (nối tiếp được), không xoá tệp"
```

Trong log phải có `[dữ liệu] … 4463 bước · thiếu OCR 0 · thiếu ảnh 0` và `[điểm lưu] …`.

## Ô 6 — chấm exec bằng UGround (bản `score_run` đã chấm S1)

```python
SC = f"{W}/score_ck500_test{'_thu' if TEST else ''}.json"
cmd = ["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground",
       "--preds", PRED, "--out", SC] + (["--n", "3"] if TEST else [])
chay(cmd, f"{W}/cham_test{'_thu' if TEST else ''}.log", WS)
R = [json.loads(l) for l in open(SC.replace(".json", "_raw.jsonl"))]
print(f"== ck500 test: {len(R)} bước · exec {sum(int(r.get('executable', 0)) for r in R)}", flush=True)
print("KIỂM (bản đủ): phải 4463 bước. Đừng tự diễn giải — gửi về máy nhà.")
```

## Chạy

1. **Chạy thử tương tác** (`TEST = True`): *Run All*, khoảng 15–20 phút. Gửi về output Ô 2, Ô 4, Ô 5, Ô 6.
   Ô 4 phải `[kiểm hoà] x/20` với x ≥ 16.
2. Ổn thì sửa Ô 3 thành `TEST = False` → **Stop session** → **Save Version → Save & Run All**.
   Khoảng 9,5 h (dưới trần 12 h). Có thể gập máy.
3. Kiểm cuối log commit: `[kiểm hoà] x/20` · `ck500 test: 4463/4463 câu` · `== ck500 test: 4463 bước`.
4. Tải từ Output về **`runs/grpo_spice/`** trên WSL: `pred_ck500_test.jsonl` · `score_ck500_test.json` ·
   `score_ck500_test_raw.jsonl` · `gen_test.log` · `cham_test.log` · `kiem_hoa_test.jsonl` · `kiem_hoa_test.log`.
   (Kaggle hay đổi đuôi thành `.txt` — cứ để vào, trợ lý đổi lại.)

## Không làm trong lượt này

Bước không chạm (ô 7 của 258): `thesis-score` chỉ có 4.463 ảnh click ⇒ **CHƯA CÓ ẢNH SCROLL**. Chỉ cần
khi kết quả click rơi vào hàng 1 hoặc 2 của 258 §0 (dòng 4 của bảng chỉ có nghĩa khi click tăng).
Khi đó: gói `test_images_nontap.tar` (1,54 GB) đang nằm ở scratchpad `/tmp` cũ, cần chuyển ra chỗ bền
trước khi máy khởi động lại; sinh thêm ~2 h T4, chấm `--mode noharm` trên máy nhà (0 GPU).
