# Runbook Kaggle — PATA: 13 unit test thật + smoke S→H→J (0 đồng, ~1–1,5 h T4)

Thuộc bước **A4–A5** của `report/185` §12. Mục đích: chứng minh mã chạy đúng trên **mô hình 3B
thật** trước khi tiêu một đồng Colab, và đo đỉnh VRAM để chọn máy cho lượt train (luật chọn máy
trong CLAUDE.md: T4 → L4 → A100).

⛔ Kết quả nào ở đây cũng **không phải kết quả phương pháp**. Smoke chạy trên 400 ảnh dạy, vài
chục update — chỉ để bắt lỗi dây nối, NaN, tràn bộ nhớ.

| ô | việc | thời gian | dừng nếu |
|---|---|---|---|
| K0 | tạo notebook, gắn dataset | 5 phút | — |
| K1 | cài gói | 2 phút | không thấy 2 GPU T4 |
| K2 | mở gói, kiểm hash | 1 phút | hash lệch |
| K3 | 13 unit test `--real` | ~15–25 phút | **test 9 hoặc 10 HỎNG ⇒ cấm train dài** |
| K4 | smoke S 20 update | ~15–20 phút | NaN · tràn bộ nhớ · CE không giảm |
| K5 | smoke H 20 update | ~5–10 phút | KL không giảm |
| K6 | smoke J 20 update (C1) + chẩn đoán + sinh câu probe 40 | ~15–20 phút | lỗi bất kỳ |
| K7 | gom log, tải về | 1 phút | — |

---

## Ô K0 — chuẩn bị (làm tay, trên máy nhà + web Kaggle)

1. Trên máy nhà (WSL) dựng gói — đã dựng sẵn ngày 23/9, dựng lại nếu sửa mã:
   ```
   ~/.venvs/thesis/bin/python harness/make_bundle.py pata_kaggle
   ```
   → `_bundles/thesis_pata_kaggle.zip` (~159 MB). Trên Windows mở `D:\Master\Thesis\_bundles\`.
2. Kaggle → **Datasets → New Dataset** → kéo thả `thesis_pata_kaggle.zip` → tên **`thesis-pata`** →
   Create. (Lần sau sửa mã: *New Version* của chính dataset này.)
3. **Code → New Notebook**. Cột phải: *Accelerator* = **GPU T4 x2** · *Internet* = **On** ·
   *Add Input* → dataset `thesis-pata`.
4. ⛔ Chạy **tương tác** (bấm từng ô), đừng *Save Version* lần đầu (bài học 7 giờ treo log).

## Ô K1 — cài gói

```python
import subprocess, sys, torch
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "bitsandbytes", "peft"], check=True)
import transformers, peft, bitsandbytes
print("torch", torch.__version__, "· transformers", transformers.__version__,
      "· peft", peft.__version__, "· bnb", bitsandbytes.__version__)
print("GPU:", [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])
assert torch.cuda.is_available(), "⛔ không có GPU — bật Accelerator GPU T4 x2"
assert tuple(int(x) for x in transformers.__version__.split(".")[:2]) >= (4, 49), \
    "⛔ transformers quá cũ cho Qwen2.5-VL — chạy: pip install -U transformers, rồi Restart"
```

## Ô K2 — mở gói, kiểm hash

```python
import os, glob, json, hashlib, zipfile, shutil
W = "/kaggle/working"
src = glob.glob("/kaggle/input/**/thesis/harness/pata_model.py", recursive=True)
if src:                                    # Kaggle đã tự bung zip
    R = os.path.dirname(os.path.dirname(os.path.dirname(src[0])))
    shutil.copytree(R, f"{W}/pk", dirs_exist_ok=True)
else:
    z = glob.glob("/kaggle/input/**/thesis_pata_kaggle.zip", recursive=True)[0]
    zipfile.ZipFile(z).extractall(f"{W}/pk")
REPO = f"{W}/pk/thesis"
DR = f"{REPO}/harness/dg1_cache/train_ac"
os.chdir(REPO)
h = json.load(open(f"{DR}/pata/split_hash.json"))
for f in ("train_proper.jsonl", "val400.jsonl", "val600.jsonl", "probe40.jsonl"):
    got = hashlib.sha256(open(f"{DR}/pata/{f}", "rb").read()).hexdigest()
    print(f"{f:20} {got[:16]}…", "ĐÚNG" if got == h[f] else "⛔ LỆCH")
    assert got == h[f]
print("ảnh:", len(glob.glob(f"{DR}/images/*.png")), "← cần 440")
```

## Ô K3 — 13 unit test trên mô hình thật

Chạy nền, ghi ra tệp, in nhịp sống mỗi 60 s (không để log ngập làm treo Kaggle):

```python
import subprocess, time, os
def chay(cmd, log, tmax=3 * 3600):
    env = dict(os.environ, TQDM_DISABLE="1", HF_HUB_DISABLE_PROGRESS_BARS="1",
               PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True", PYTHONUNBUFFERED="1")
    with open(log, "w") as f:
        p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, env=env)
    t0 = time.time()
    while p.poll() is None and time.time() - t0 < tmax:
        time.sleep(60)
        tail = open(log).read().splitlines()[-1:] or [""]
        print(f"[{(time.time()-t0)/60:4.0f} phút] {tail[0][:160]}", flush=True)
    print(f"== mã thoát {p.returncode} ==")
    print("\n".join(l for l in open(log).read().splitlines()
                    if any(k in l for k in ("ĐẠT", "HỎNG", "⛔", "Error", "error", "XONG", "Dừng", "[kế", "[tham"))))
    return p.returncode

chay(["python", "harness/pata_test.py", "--real", "--data-root", DR], f"{W}/k3_test.log")
```

**Đọc:** dòng cuối phải là `13/13 ĐẠT`. Dung sai ở chế độ thật: test 3/5/10 `≤ 5e-2`, test 4
`≤ 1e-2`, test 9 `≤ 0,1` (FP16 trên T4 — không phải lỗi logic nếu vượt nhẹ; gửi mình dòng đó).
⛔ **Test 9 hoặc 10 HỎNG ⇒ dừng, không chạy K4**, gửi mình toàn bộ `k3_test.log`.

## Ô K4 — smoke Stage S (20 update, chỉ 400 ảnh có trong gói)

T4 16 GB: cỡ lô 2 × accum 8 = 16 (cỡ lô hiệu dụng không đổi so với recipe).

```python
CK = f"{W}/ck"
chay(["python", "harness/pata_train.py", "--stage", "S", "--only-local", "--data-root", DR,
      "--bs", "2", "--accum", "8", "--max-updates", "20", "--save-steps", "10", "--log-steps", "5",
      "--workers", "2", "--out", f"{CK}/S"], f"{W}/k4_S.log")
```

**Đọc (chép cho mình 3 dòng):** `s/u` (giây mỗi update) · `vram=` (đỉnh GB) · `ce=` ở u1 và u20.
CE phải giảm; `vram` là số quyết định máy cho lượt thật.

## Ô K5 — smoke Stage H (20 update, từ điểm lưu S vừa có)

```python
chay(["python", "harness/pata_train.py", "--stage", "H", "--only-local", "--data-root", DR,
      "--init-adapter", f"{CK}/S/ckpt-00020", "--bs", "2", "--accum", "8", "--max-updates", "20",
      "--save-steps", "10", "--log-steps", "5", "--workers", "2", "--out", f"{CK}/H"], f"{W}/k5_H.log")
```

**Đọc:** `kl=` giảm từ u1 tới u20 · `mass=` tăng · `gn=` có `pq`, `pv`, `tvec` khác 0 và
`lora` = 0 (LoRA S đóng băng). `s/u` phải nhỏ hơn rõ so với K4 (forward chỉ tới block 17).

## Ô K6 — smoke Stage J (C1) + chẩn đoán + sinh câu

```python
chay(["python", "harness/pata_train.py", "--stage", "J", "--only-local", "--data-root", DR,
      "--init-adapter", f"{CK}/S/ckpt-00020", "--init-heads", f"{CK}/H/ckpt-00020",
      "--bs", "2", "--accum", "8", "--max-updates", "20", "--save-steps", "10", "--log-steps", "5",
      "--workers", "2", "--out", f"{CK}/J"], f"{W}/k6_J.log")
chay(["python", "harness/pata_eval.py", "--ckpt", f"{CK}/H/ckpt-00020", "--mode", "diag",
      "--split", "probe40", "--no-ce", "--data-root", DR, "--out", f"{W}/ev"], f"{W}/k6_diagH.log")
chay(["python", "harness/pata_eval.py", "--ckpt", f"{CK}/J/ckpt-00020", "--mode", "gen",
      "--split", "probe40", "--variants", "on,off", "--data-root", DR, "--out", f"{W}/ev"], f"{W}/k6_gen.log")
```

**Đọc:** J log có `gate=` và `resid=` (resid nhỏ, cỡ 1e-4…1e-2, là đúng vì Wo mới rời 0) ·
`gn=` có `wo` khác 0 · chẩn đoán H in đủ các dòng `lift_center`, `lift_train`, `dung_vs_xao`
(sau 20 update thì **KHÔNG kỳ vọng** đạt cổng — chỉ kiểm script chạy) · sinh câu in
`format hợp lệ …` cho `on` và `off`.

## Ô K7 — gom log

```python
os.system(f"cd {W} && zip -q -r pata_kaggle_logs.zip *.log ev ck/*/train_log.jsonl")
print(os.path.getsize(f"{W}/pata_kaggle_logs.zip") // 1024, "KB → tải về từ cột Output")
```

Tải `pata_kaggle_logs.zip` về, đặt vào **`runs/pata/kaggle_smoke/`** (luật đọc kết quả: tải về
đặt thẳng vào thư mục của phép đo) rồi báo mình.

---

## Ô K9 — đo thời gian mỗi update dồn vào đâu (thêm 23/9 tối, ~15 phút T4)

Bối cảnh: Stage S trên A100 chạy **23,9 s/update** (S1 cũ 10,3), chờ dữ liệu 0%, GPU bận 30–50%, lô 16 × 1
không nhanh hơn 4 × 4. Nghi phạm: tháp thị giác tính attention **từng cửa sổ bằng vòng lặp Python**.
Ô này đo tháp thị giác / forward / backward cho hai cách (`loop` mặc định · `block` gom cửa sổ vào một lời
gọi có mặt nạ) và độ lệch số học giữa chúng. Chạy sau K1 + K2 (dùng gói `thesis-pata` bản mới).

```python
chay(["python", "harness/pata_profile.py", "--data-root", DR, "--bs", "2", "--steps", "3"],
     f"{W}/k9_profile.log")
print(open(f"{W}/k9_profile.log").read()[-6000:])
```

**Gửi mình toàn bộ phần in ra.** Mình đọc bốn số: tỉ trọng tháp thị giác trong cả bước · tăng tốc
block/loop · lệch đầu ra tháp thị giác · số lời gọi attention mỗi bước.
