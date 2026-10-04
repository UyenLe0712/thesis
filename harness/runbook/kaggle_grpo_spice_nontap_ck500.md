# Sinh câu ck500 trên 2.495 bước KHÔNG chạm (report/261 §5.2, 2/10/2026)

Phép kiểm cuối cho tác dụng phụ của GRPO SPICE `checkpoint-500`: trên bước cuộn / chờ / gõ / mở ứng
dụng / quay lại, câu của ck500 có còn đúng loại thao tác như S1/101 không. Kaggle T4 chỉ **sinh câu**
(~2 h, 0 đồng); chấm ở máy nhà, **không gọi bộ trỏ**, 0 GPU.

Mốc S1/101 trên 2.495 bước này (tính lại 2/10 bằng `score_run --mode noharm`): khớp loại thao tác
**85,97** [84,5; 87,4] · scroll 83,97 (n = 755) · wait 90,69 · input_text 81,58 · open_app 96,16 ·
navigate_back 72,96.

## Luật đọc — khoá TRƯỚC khi có số

| điều kiện | ngưỡng | nguồn |
|---|---|---|
| toàn bộ 2.495 bước | cận dưới KTC95 của Δ(ck500 − S1) ≥ −3 điểm | luật noharm gốc, `report/106` mục 3, `score_run.noharm` |
| scroll (755 bước) | Δ điểm ≥ −3 | `report/261` §5.3 |

Cả hai đạt ⇒ chốt ck500 là mô hình cuối. Một trong hai rớt ⇒ khai là tác hại ở bước không chạm trong
luận văn, kể cả khi số bước chạm thắng. ⛔ Sinh **một lần**, không sinh lại sau khi thấy số.

⚠️ Khai kèm: S1 trên bước không chạm sinh bằng đường `infer_branch` (LoRA chưa hoà, theo lô), còn
ck500 sinh trên S1 đã hoà, fp16 — cùng lẫn biến đường sinh như `report/259` §5.1. Ô 4 đo cỡ của nó
trên 20 bước (chỉ để khai, không chặn), vì quyết định 2/10 là không chạy S1-hoà đủ tập.

## Chuẩn bị (máy nhà → Kaggle)

1. **Dataset mới `thesis-nontap-images`**: upload `_bundles/test_images_nontap.tar` (1,65 GB, 2.495 ảnh
   `test_ac/images/ep*_s*.png`). Kaggle có thể tự bung hoặc giữ nguyên `.tar` — Ô 2 xử cả hai.
2. **`grpo-spice-script` → New Version**: kéo lại cả 4 tệp trong `_bundles/grpo-spice-script/`.
   Chỉ `gen_test_grpo.py` đổi (thêm cờ `--non-tap`), md5 mới **`b18ec1aa3fd037ddffb9411db63c2a3f`**.
3. Notebook mới, **GPU T4**, **Internet On**. *Add Input*: `thesis-score` · `fgrb-p1-bundle` ·
   `grpo-spice-script` (bản mới) · `grpo-spice-ck500` · `thesis-nontap-images`.

## Ô 1 — gói (giống hệt lượt bước chạm)

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
import os, glob, json, shutil, hashlib, tarfile
W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()

SRC = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/gen_test_grpo.py", recursive=True)
       if all(os.path.exists(os.path.join(os.path.dirname(p), f))
              for f in ("grpo_spice.py", "build_branch_data.py", "preds_s1_seed101.jsonl"))]
assert len(SRC) == 1, f"DỪNG: cần đúng một grpo-spice-script bản mới, thấy {SRC}"
SRC = SRC[0]
for f in ("grpo_spice.py", "build_branch_data.py", "gen_test_grpo.py"):
    shutil.copy(f"{SRC}/{f}", f"{W}/{f}")
assert md5(f"{W}/grpo_spice.py") == "07ea87b6d156d1faa391a4274dffd7cf", "DỪNG: grpo_spice.py bản cũ"
assert md5(f"{W}/gen_test_grpo.py") == "b18ec1aa3fd037ddffb9411db63c2a3f", "DỪNG: gen_test_grpo.py chưa có --non-tap (New Version dataset script)"
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
assert md5(f"{CK500}/adapter_model.safetensors") == "491fa6677340393f1e4464c08a0cec98", "DỪNG: không phải ck500 đã chấm test"

# test.jsonl + ocr.jsonl lấy từ thesis-score (cùng tệp lượt bước chạm)
TA = next(os.path.dirname(t) for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True)
          if os.path.exists(os.path.join(os.path.dirname(t), "ocr.jsonl")))
assert md5(f"{TA}/test.jsonl") == "da58299ee551a926a21cbecb5232bf78", "DỪNG: test.jsonl lệch máy nhà"
print("ocr.jsonl md5", md5(f"{TA}/ocr.jsonl"), "(máy nhà 7a35f568235eef2902bd06b650abc3a7)")

# ảnh không chạm: thư mục đã bung, hoặc bung .tar vào /kaggle/working
def tim_anh():
    for d in glob.glob("/kaggle/input/**/images", recursive=True) + glob.glob(f"{W}/nontap/**/images", recursive=True):
        if "thesis-score" not in d and len(glob.glob(f"{d}/ep*_s*.png")) == 2495:
            return d
IMG = tim_anh()
if not IMG:
    tars = glob.glob("/kaggle/input/**/*.tar", recursive=True)
    assert tars, "DỪNG: không thấy ảnh không chạm lẫn tệp .tar"
    tarfile.open(tars[0]).extractall(f"{W}/nontap")
    IMG = tim_anh()
assert IMG, "DỪNG: không có thư mục đúng 2.495 ảnh không chạm"

print("SRC   ", SRC); print("BUNDLE", BUNDLE); print("CK500 ", CK500); print("TA    ", TA); print("IMG   ", IMG, flush=True)
```

Phải thấy 5 đường dẫn, không dòng DỪNG nào. Dòng md5 OCR chỉ để ghi lại (khác máy nhà cũng không sao,
Ô 4/5 tự dừng nếu thiếu OCR ở bước không chạm).

## Ô 3 — hoà S1 + hàm chạy có nhịp sống

```python
TEST = True          # chạy thử tương tác; đổi False trước khi commit

def chay(cmd, log, cwd, nhip=120):
    t0 = time.time()
    with open(log, "w") as f:
        q = subprocess.Popen(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                             env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
                                  "PYTHONUNBUFFERED": "1"})
        while q.poll() is None:
            time.sleep(nhip if not TEST else 30)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"  {(time.time()-t0)/3600:5.2f} h · {os.path.basename(log)} · {L[-1][:110] if L else 'chưa có dòng nào'}", flush=True)
    print(f"--- {os.path.basename(log)} · mã thoát {q.returncode} · {(time.time()-t0)/3600:.2f} h ---")
    print("".join(open(log, errors="ignore").readlines()[-6:]), flush=True)
    return q.returncode

r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED],
                   cwd=W, capture_output=True, text=True)
print((r.stdout + r.stderr)[-1500:]); assert r.returncode == 0, "DỪNG: hoà lỗi"
```

## Ô 4 — kiểm hoà trên 20 bước không chạm (chỉ để khai, không chặn)

```python
NT_ARGS = ["--recs", f"{TA}/test.jsonl", "--ocr", f"{TA}/ocr.jsonl", "--images", IMG, "--non-tap", "--no-q4"]
out = f"{W}/kiem_hoa_nontap.jsonl"
if os.path.exists(out): os.remove(out)
chay(["python", "gen_test_grpo.py", "--bundle", BUNDLE, "--merged", MERGED, "--s1", S1P,
      "--n", "20", "--out", out] + NT_ARGS, f"{W}/kiem_hoa_nontap.log", W)
print([l for l in open(f"{W}/kiem_hoa_nontap.log") if "[dữ liệu]" in l or "[kiểm hoà]" in l])
```

Phải có `[dữ liệu] … 2495 bước · thiếu OCR 0 · thiếu ảnh 0` rồi `[kiểm hoà] x/20`. x bao nhiêu cũng
chạy tiếp — gửi về để khai.

## Ô 5 — sinh 2.495 câu từ `checkpoint-500`

```python
PRED = f"{W}/pred_ck500_test_nontap{'_thu' if TEST else ''}.jsonl"
chay(["python", "gen_test_grpo.py", "--bundle", BUNDLE, "--merged", MERGED, "--ckpt", CK500,
      "--out", PRED] + (["--n", "5"] if TEST else []) + NT_ARGS,
     f"{W}/gen_test_nontap{'_thu' if TEST else ''}.log", W)
n = sum(1 for _ in open(PRED))
print(f"ck500 không chạm: {n}/{5 if TEST else 2495} câu", flush=True)
assert n == (5 if TEST else 2495), "DỪNG: thiếu câu — chạy lại ô này (nối tiếp được), không xoá tệp"
```

Trong log phải có `[điểm lưu] …` (không phải `KHÔNG gắn`) và dòng `[xong] 2495 câu · rỗng …`.

## Chạy

1. **Chạy thử tương tác** (`TEST = True`): *Run All*, ~10 phút. Gửi về output Ô 2, Ô 4, Ô 5.
2. Ổn thì sửa Ô 3 thành `TEST = False` → **Stop session** → **Save Version → Save & Run All**.
   Khoảng 2–2,5 h (hoà ~5 phút · kiểm hoà ~1 phút · sinh 2.495 × ~2,8 s). Có thể gập máy.
3. Tải từ Output về **`runs/grpo_spice/`**: `pred_ck500_test_nontap.jsonl` · `gen_test_nontap.log` ·
   `kiem_hoa_nontap.jsonl` · `kiem_hoa_nontap.log` (đuôi `.txt` cũng được, trợ lý đổi lại).

## Chấm ở máy nhà (0 GPU, ~20 giây)

```
python3 harness/grpo_spice_nontap_doc.py
```

In bảng toàn bộ + từng loại thao tác (S1 · ck500 · Δ · KTC cụm app · phá/cứu), rồi dòng `[luật]` theo
bảng khoá ở đầu file; ghi `runs/grpo_spice/nontap_ck500_doc.json`. Đã chạy khô 2/10 với câu S1 làm giả
ck500: Δ = 0 ở mọi nhóm, S1 85,97 khớp `score_run --mode noharm` (86,0 [84,5; 87,4]).
