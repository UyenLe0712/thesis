# Runbook Kaggle — P10: chấm `exec` val600 cho cổng cuối C1 (0 đồng, ~2–2,5 h T4 × 2)

Thuộc `harness/colab_pata_c1.md` ô P10. Chạy SAU khi Colab P9 đã sinh đủ 5 tệp preds vào
`MyDrive/thesis/pata_ck/cong_c1/`. Đọc cổng bằng `harness/pata_cong_c1.py` trên WSL (0 GPU).

| ô | việc | thời gian |
|---|---|---|
| Q0 | chuẩn bị: tải 5 preds từ Drive, upload thành dataset | 10 phút |
| Q1 | gỡ torchao, cài gói | 2 phút |
| Q2 | dựng workspace: mã · val600 · ảnh · preds | 2 phút |
| Q3 | chấm 5 tệp, song song trên 2 GPU T4 | ~2–2,5 h |
| Q4 | gom kết quả, tải về | 2 phút |

## Q0 — chuẩn bị (tay)

1. Trên Drive, thư mục `MyDrive/thesis/pata_ck/cong_c1/` phải có **5 tệp preds**:
   `preds_C1_val600_on.jsonl` · `preds_C1_val600_off.jsonl` · `preds_C1_val600_swapD.jsonl` ·
   `preds_C1_val600_swapR.jsonl` · `preds_S_val600_on.jsonl` (cùng ba tệp `diag_*_val400.json`).
   Tải **cả thư mục** về máy.
2. Kaggle → New Dataset → kéo 5 tệp preds vào → tên **`thesis-pata-preds`** → Create.
3. Notebook mới: GPU **T4 x2** · Internet **On** · Add Input: **`thesis-pata`** (gói mã, bản mới nhất —
   phải có `harness/score_run.py`) · **`thesis-val-cham`** (= `_bundles/thesis_val_cham.zip`: 1.567 ảnh +
   `val_cham600.jsonl` + `ocr.jsonl`, dựng 9/9). ⛔ **`thesis-val` cũ KHÔNG thay được**: không có
   `val_cham600.jsonl`, chỉ phủ 391/602 ảnh · **`thesis-pata-preds`**.
4. ⛔ Chạy tương tác (không Save Version lần đầu).

## Q1 — gỡ torchao, cài gói

```python
import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "-q", "torchao"])
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "bitsandbytes", "peft"], check=True)
import torch, transformers
print("torch", torch.__version__, "· transformers", transformers.__version__,
      "· GPU", [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])
assert torch.cuda.device_count() == 2, "⛔ cần GPU T4 x2"
```

## Q2 — dựng workspace

```python
import os, glob, json, shutil, zipfile
W = "/kaggle/working"
src = glob.glob("/kaggle/input/**/thesis/harness/score_run.py", recursive=True)
if src:
    shutil.copytree(os.path.dirname(os.path.dirname(os.path.dirname(src[0]))), f"{W}/pk", dirs_exist_ok=True)
else:
    zipfile.ZipFile(glob.glob("/kaggle/input/**/thesis_pata_kaggle.zip", recursive=True)[0]).extractall(f"{W}/pk")
WS = f"{W}/pk/thesis"
VD = f"{W}/valdata"; os.makedirs(VD, exist_ok=True)

# val600: bí danh gold_instruction (score_run đòi khoá này; val tách từ tập dạy nên chỉ có target_instruction)
# ⛔ SỬA 24/9 tối: mọi tệp lấy theo THƯ MỤC CỦA val_cham600.jsonl (dataset thesis-val-cham), không glob toàn
#    /kaggle/input — gói thesis-pata cũng có 440 ảnh ep*_s*.png và một ocr.jsonl, sắp xếp theo tên thì đứng
#    TRƯỚC thesis-val-cham ⇒ bản cũ trỏ nhầm thư mục ảnh. Và dataset này có ocr.jsonl, không có ocr_val.jsonl.
v600s = glob.glob("/kaggle/input/**/val_cham600.jsonl", recursive=True)
assert v600s, "⛔ thiếu dataset thesis-val-cham (thesis-val cũ KHÔNG đủ: không có val_cham600, chỉ 391/602 ảnh)"
v600 = v600s[0]; BASE = os.path.dirname(v600)
with open(v600, encoding="utf-8") as fi, open(f"{VD}/val_cham600.jsonl", "w", encoding="utf-8") as fo:
    for d in map(json.loads, fi):
        d.setdefault("gold_instruction", d["target_instruction"])
        fo.write(json.dumps(d, ensure_ascii=False) + "\n")
ocr = [p for p in (f"{BASE}/ocr.jsonl", f"{BASE}/ocr_val.jsonl") if os.path.exists(p)][0]
shutil.copy(ocr, f"{VD}/ocr.jsonl")
IMGDIR = f"{BASE}/images"
if os.path.lexists(f"{VD}/images"):
    os.remove(f"{VD}/images")
os.symlink(IMGDIR, f"{VD}/images")
cham = [d for d in map(json.loads, open(f"{VD}/val_cham600.jsonl"))
        if d["action"].get("action_type") in ("click", "long_press")]
thieu = [d["image"] for d in cham if not os.path.exists(f"{VD}/{d['image']}")]
print("dataset   :", BASE)
print("val600 bước chạm:", len(cham), "← cần 602 · ảnh thiếu:", len(thieu), "← cần 0 · ocr",
      sum(1 for _ in open(f"{VD}/ocr.jsonl")), "dòng")
assert len(cham) == 602 and not thieu, f"⛔ thiếu ảnh, vd {thieu[:3]}"

PD = os.path.dirname(glob.glob("/kaggle/input/**/preds_C1_val600_on.jsonl", recursive=True)[0])
BIEN = {"C1_on": "preds_C1_val600_on.jsonl", "C1_off": "preds_C1_val600_off.jsonl",
        "C1_swapD": "preds_C1_val600_swapD.jsonl", "C1_swapR": "preds_C1_val600_swapR.jsonl",
        "S_on": "preds_S_val600_on.jsonl"}
DEM = {}
for t, f in BIEN.items():
    DEM[t] = sum(1 for _ in open(f"{PD}/{f}"))
    print(f"  {t:9} {DEM[t]:4} dòng")
assert DEM["C1_on"] == DEM["C1_off"] == DEM["S_on"] == 602, "⛔ preds on/off/S phải đủ 602"
assert DEM["C1_swapD"] == DEM["C1_swapR"] == 546, "⛔ swapD/swapR phải đủ 546 (pata/val600_swap.jsonl)"
OUT = f"{W}/cong_c1"; os.makedirs(OUT, exist_ok=True)
```

## Q3 — chấm 5 tệp, song song trên 2 GPU (~2–2,5 h)

GPU 0 chấm C1_on → C1_swapD → S_on; GPU 1 chấm C1_off → C1_swapR. Mỗi tiến trình ghi ra tệp, nối tiếp
được (`score_run.py` đọc lại tệp thô cũ, chỉ chấm phần thiếu) ⇒ mất phiên thì chạy lại đúng ô này.

```python
import subprocess, time
def lenh(t):
    return (f"python harness/score_run.py --mode score --preds {PD}/{BIEN[t]} --data-root {VD} "
            f"--recs-file val_cham600.jsonl --out {OUT}/score_{t}.json --n {DEM[t]}")
chuoi = {0: ["C1_on", "C1_swapD", "S_on"], 1: ["C1_off", "C1_swapR"]}
env = {**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1"}
PS = []
for g, ts in chuoi.items():
    PS.append(subprocess.Popen(["bash", "-c", " && ".join(lenh(t) for t in ts)], cwd=WS,
                               env={**env, "CUDA_VISIBLE_DEVICES": str(g)}, start_new_session=True,
                               stdout=open(f"{W}/cham_gpu{g}.log", "a"), stderr=subprocess.STDOUT))
t0 = time.time()
while any(p.poll() is None for p in PS):
    time.sleep(120)
    dem = {t: (sum(1 for _ in open(f"{OUT}/score_{t}_raw.jsonl"))
               if os.path.exists(f"{OUT}/score_{t}_raw.jsonl") else 0) for t in BIEN}
    print(f"{time.strftime('%H:%M')} · {(time.time()-t0)/3600:4.2f} h · " +
          " · ".join(f"{t} {dem[t]}/{DEM[t]}" for t in BIEN), flush=True)
print("mã thoát:", [p.returncode for p in PS])
for g in (0, 1):
    print(f"--- GPU {g} ---"); print(subprocess.run(["tail", "-5", f"{W}/cham_gpu{g}.log"],
                                                     capture_output=True, text=True).stdout)
```

**Đọc:** mấy nhịp đầu in 0 là bình thường (tải UGround-V1-2B + `all_forest_dict.zip`). Không có nhịp
sống nào sau ~10 phút thì dừng, gửi mình `cham_gpu*.log`. ⛔ Internet phải ON (cây trợ năng cho
luật Voronoi tải từ HuggingFace; tắt mạng thì danh sách nút rỗng mà không báo lỗi).

## Q4 — gom kết quả

```python
os.system(f"cd {W} && zip -q -r pata_cong_c1.zip cong_c1 cham_gpu*.log")
print(os.path.getsize(f"{W}/pata_cong_c1.zip") // 1024, "KB → tải về từ cột Output")
```

**Chạy qua đêm (không ngồi canh):** bấm Run ô Q4 **ngay khi Q3 đang chạy** — nó xếp hàng `[*]` và tự chạy khi
Q3 xong. Rồi xếp hàng tiếp ô Q4b để giữ phiên sống tới sáng: phiên tương tác rỗi quá lâu có thể bị Kaggle tắt,
và tắt là mất `/kaggle/working` (chưa đo được ngưỡng rỗi — đừng đánh cược). Q4b đốt quota T4 trong lúc chờ
(tối đa 7 h) ⇒ tải zip xong thì **Stop Session** ngay.
```python
# Q4b — giữ phiên sống tối đa 7 h để sáng tải pata_cong_c1.zip
import time
for i in range(42):
    time.sleep(600)
    print(time.strftime("%H:%M"), "· giữ phiên — tải pata_cong_c1.zip ở Output rồi bấm Stop Session", flush=True)
```

Trên máy nhà: bung vào **`runs/pata/cong_c1/`**, chép thêm 5 preds + 3 `diag_*_val400.json` từ Drive vào
cùng thư mục, rồi:
```
~/.venvs/thesis/bin/python harness/pata_cong_c1.py --dir runs/pata/cong_c1
```
⛔ Ngưỡng của 5 điều kiện đã khoá trong `pata_cong_c1.py` (24/9, trước khi C1 train) — không sửa.
