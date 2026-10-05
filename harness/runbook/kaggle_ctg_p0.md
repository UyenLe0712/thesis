# CTG-GRPO — P0 trên Kaggle T4 (4/10/2026), chạy TRƯỚC khi thuê A100

Thi hành 276 §4 bước 3 và §8 *P0* (`harness/tai_lieu_2026-10-04/276_ACTION_CTG_GRPO_4_10.md`).
Kaggle T4, **0 đồng**, khoảng **1,5–2 h** hạn mức. Hai phép kiểm:

- **P0(a)** A3 chạy 20 bước: 10 bước → lưu `checkpoint-10` → **chạy tiếp** tới 20. Kiểm luôn việc
  `ctg_state.json` được lưu và nạp lại (thiếu thì λ âm thầm về 1,0).
- **P0(b)** log-prob động từ chạm ở token đầu, trên 75 câu nhắc C1 có lớp vàng scroll/type/back, đo
  với S1, ck250, ck500. Luật (đặt 4/10, trước khi đo): **ĐẠT** khi trên 32 câu nhắc scroll
  `ck500 > S1` và `ck250 ≥ S1 − 0,05`. Không đạt ⇒ giả thuyết "GRPO kéo câu không-chạm về câu chạm"
  sai ⇒ **dừng, không thuê A100**.

## Chuẩn bị (máy nhà, đã làm sẵn 4/10)

`_bundles/ctg-grpo-script/` gồm 5 tệp:

```
332765b7c3657c1117ada5bf6ea3b936  ctg_grpo.py
07ea87b6d156d1faa391a4274dffd7cf  grpo_spice.py
619e63e123a6dbf60086e65ee94a3912  build_branch_data.py
9bf0b84145458fd55919a5e161b9766f  metric_exec.py
828ce31811540195c34ecdbdee85d863  kl_ck500_theo_buoc.json
```

Sửa mã thì dựng lại: `cp harness/{ctg_grpo,grpo_spice,build_branch_data,metric_exec}.py runs/grpo_spice/kl_ck500_theo_buoc.json _bundles/ctg-grpo-script/`
rồi sửa md5 ở Ô 2.

## Trên Kaggle

1. *Datasets → New Dataset* → kéo **5 tệp** trong `_bundles/ctg-grpo-script/` → tên `ctg-grpo-script`, Private.
2. *Create → New Notebook*. *Session options*: **GPU T4 ×2**, **Internet On**.
3. *Add Input* (Datasets): `fgrb-p1-bundle` · `c1-exec8` · `ctg-grpo-script` · `grpo-spice-ck250` · `grpo-spice-ck500`.
4. Dán 6 ô dưới. Lượt đầu **chạy tương tác** (*Run All*), nhìn log 15 phút đầu; ổn thì để chạy hết.

### Ô 1 — gói

```python
import subprocess, sys, os, time
T_NB = time.time()
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode

sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes 'trl==0.29.1' 2>&1 | tail -3")
sh(f'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.get_device_name(0))"')
```

Không cần Java: thưởng CIDEr-D là Python thuần.

### Ô 2 — đường dẫn, md5, tìm ck250/ck500

```python
import os, glob, shutil, hashlib, json
W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "images" in d)
C1 = glob.glob("/kaggle/input/**/c1_mau.jsonl", recursive=True); assert len(C1) == 1, C1; C1 = C1[0]
assert md5(C1) == "d757554326977309c3a65ae0b144c211", "DỪNG: c1_mau.jsonl lệch"
SRC = glob.glob("/kaggle/input/**/ctg_grpo.py", recursive=True); assert len(SRC) == 1, SRC
MD5 = {"ctg_grpo.py": "332765b7c3657c1117ada5bf6ea3b936", "grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf",
       "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912", "metric_exec.py": "9bf0b84145458fd55919a5e161b9766f"}
for f, h in MD5.items():
    shutil.copy(os.path.join(os.path.dirname(SRC[0]), f), f"{W}/{f}")
    assert md5(f"{W}/{f}") == h, f"DỪNG: {f} lệch bản máy nhà, New Version dataset ctg-grpo-script"
MERGED = f"{W}/s1_merged"

# nhận diện bằng md5 adapter (Kaggle hay bỏ thư mục ngoài khi upload ⇒ không tin tên thư mục)
MD5_CK = {"1dfaa451b0e5b405132835757eb1cad4": "ck250", "491fa6677340393f1e4464c08a0cec98": "ck500"}
CK = {}
for f in glob.glob("/kaggle/input/**/adapter_model.safetensors", recursive=True):
    h = md5(f)
    print("  adapter thấy:", f, h, flush=True)
    if h in MD5_CK: CK[MD5_CK[h]] = os.path.dirname(f)
print("BUNDLE:", BUNDLE, "\nCK:", CK, "\nmd5 khớp", flush=True)
assert set(CK) == {"ck250", "ck500"}, f"DỪNG: cần đủ ck250 và ck500 (gắn dataset grpo-spice-ck250 và grpo-spice-ck500), thấy {CK}"
```

### Ô 3 — hoà S1 (fp16 trên T4)

```python
r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED],
                   cwd=W, capture_output=True, text=True)
print((r.stdout + r.stderr)[-2000:]); assert r.returncode == 0, "DỪNG: hoà lỗi"
```

### Ô 4 — hàm chạy có nhịp sống

```python
def chay(cmd, log, nhip=120):
    t0 = time.time()
    with open(log, "a") as f:
        q = subprocess.Popen(cmd, cwd=W, stdout=f, stderr=subprocess.STDOUT,
                             env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
                                  "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"})
        while q.poll() is None:
            time.sleep(nhip)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            nb = sum(l.startswith("{'loss'") for l in L)
            print(f"  {(time.time()-t0)/60:5.1f} phút · {os.path.basename(log)} · dòng loss {nb} · {L[-1][:100] if L else ''}", flush=True)
    print(f"--- {os.path.basename(log)} · mã thoát {q.returncode} · {(time.time()-t0)/60:.1f} phút ---", flush=True)
    return q.returncode
```

### Ô 5 — P0(a): A3 10 bước → lưu → chạy tiếp tới 20

```python
OUT = f"{W}/p0_a3"; LOG = f"{W}/p0a.log"
base = ["python", "ctg_grpo.py", "--train", "--arm", "A3", "--no-q4", "--gen-chunk", "8",
        "--bundle", BUNDLE, "--merged", MERGED, "--out", OUT, "--save-steps", "10", "--resume", "auto"]
rc1 = chay(base + ["--max-steps", "10"], LOG)
rc2 = chay(base + ["--max-steps", "20"], LOG)
L = open(LOG, errors="ignore").read().splitlines()
for pat in ("[nhánh]", "[cider] df", "thưởng:", "[lớp vàng", "[khớp lớp", "GRPOConfig:", "[lô]", "[thưởng]",
            "[tiếp từ]", "[nạp default]", "[nạp ctg_state]", "[ctg_state] lưu", "[xong]"):
    for l in [l for l in L if l.startswith(pat)][-2:]:
        print(l[:220])
cl = [json.loads(l) for l in open(f"{OUT}/ctg_log.jsonl")]
print(f"ctg_log: {len(cl)} nhóm · lớp {dict(__import__('collections').Counter(r['lop'] for r in cl))}")
for r in [r for r in cl if "lam" in r][-6:]: print("  ", r)
print("mã thoát", rc1, rc2, "· Traceback:", any("Traceback" in l for l in L))
```

Phải thấy, theo thứ tự:
- `[nhánh] A3 · trl 0.29.1 …` · `[cider] df dựng từ 3991 câu chuẩn` · `thưởng: [1.0, 0.0, 0.0]`
- `[lô] mỗi lượt sinh 16 câu = 2 câu nhắc × 8` · `[thưởng] ['r_cider'] · CTG cộng vào advantage: True`
- lượt 1: `[tiếp từ] None`, cuối có `[ctg_state] lưu …/checkpoint-10/ctg_state.json · λ {…}`
- lượt 2: `[tiếp từ] …/checkpoint-10` · `[nạp default] … → x` với **x > 0** · `[nạp ctg_state] bước 10 · λ {…}`
  **trùng λ của dòng `[ctg_state] lưu` lượt 1**
- `[xong] 10 bước · … s/bước · đỉnh VRAM … GiB` · mã thoát `0 0` · `Traceback: False`
- ctg_log có dòng mang `lam`, `chat`, `std_pos` (20 bước × 2 câu nhắc ⇒ ~40 nhóm, lớp scroll/type/back chiếm ~22%,
  có thể chỉ vài nhóm).

Ghi lại **s/bước** và **đỉnh VRAM** của T4: dùng để chọn máy ở bước train.

### Ô 6 — P0(b): log-prob động từ chạm, S1 / ck250 / ck500

```python
rc = chay(["python", "ctg_grpo.py", "--logp-probe", "--no-q4", "--bundle", BUNDLE, "--merged", MERGED,
           "--c1", C1, "--ckpts", f"ck250={CK['ck250']},ck500={CK['ck500']}", "--out", f"{W}/p0b.json"],
          f"{W}/p0b.log", nhip=60)
print("\n".join(l for l in open(f"{W}/p0b.log", errors="ignore").read().splitlines()
                if l.startswith(("[token", "[câu nhắc]", "[S1]", "[ck250]", "[ck500]", "[P0(b)", "✅", "⛔", "Traceback"))))
```

Dòng quyết định: `✅ P0(b) ĐẠT …` hoặc `⛔ P0(b) KHÔNG ĐẠT …`.

### Ô 7 — gói kết quả

```python
shutil.rmtree(MERGED, ignore_errors=True)
for d in glob.glob(f"{W}/p0_a3/checkpoint-*"): shutil.rmtree(d, ignore_errors=True)
shutil.make_archive(f"{W}/ctg_p0_out", "zip", W, ".")
print(os.path.getsize(f"{W}/ctg_p0_out.zip") / 2**20, "MB")
```

Tải `ctg_p0_out.zip`, giải nén vào `runs/ctg/p0/`. Gửi lại: output Ô 5 và Ô 6.

## Nếu có trục trặc

| thấy gì | làm gì |
|---|---|
| `⛔ CTG chỉ đối chiếu với mã TRL 0.29.1` | Ô 1 cài sai bản trl; chạy lại Ô 1 |
| `GRPOConfig thiếu khoá` | gửi log về (bản TRL lệch) |
| `⛔ nhóm G không liền khối` / `advantage không phải (B,)` | gửi log, không chạy tiếp: giả định về TRL sai |
| OOM | gửi log; thử lại Ô 5 với `--gen-chunk 4` |
| `[nạp ctg_state]` không có ở lượt 2 hoặc λ khác lượt 1 | gửi log: λ sẽ mất khi Colab đứt máy |
