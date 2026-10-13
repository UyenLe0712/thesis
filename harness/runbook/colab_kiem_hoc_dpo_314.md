# Runbook — Phép kiểm "GA-DPO không học: do cách train hay do cặp dữ liệu" (314, 13/10/2026)

Bối cảnh: `report/314_KET_QUA_GADPO_13_10.md`. Hai lượt GA-DPO (lr 5e-6, 5e-5; 830 cặp, 1 epoch, 52 bước) đều
không dịch khỏi ref. Mỗi cặp chỉ thấy một lần và acc đo trước khi cập nhật, nên acc 0,54 không tách được hai
khả năng: (a) train quá ít bước, (b) cặp không có quy luật chung. Phép kiểm này tách hai khả năng đó.

Script: `_scripts/314/ds_gadpo314/kiem_hoc_dpo.py` (tự kiểm CPU: `python kiem_hoc_dpo.py --tu-kiem --out /tmp/x` → `ĐẠT`).

## 0. Thiết kế

- 200 cặp **đã thấy** (train) + 200 cặp **giữ riêng** (không train), tách theo câu nhắc, mỗi tập 100 cải thiện + 100 giữ, seed 101.
- Train 5 epoch trên 200 cặp: lr 5e-5, accum 8 ⇒ **125 bước optimizer** (lượt cũ 52). β 0,1, λ_nll 1,0, cosine, warmup 5%.
  Nền, LoRA, loss y như `ga_dpo.py`.
- Đo ở chế độ eval trên cả hai tập tại epoch 0 · 1 · 3 · 5: acc (tỉ lệ margin > 0), margin, log-p chosen/rejected, ‖B‖ của LoRA.
- Epoch 0 là phép kiểm nạp đúng: policy phải trùng ref (‖B‖ = 0, margin ≈ 0). Script tự dừng nếu sai.

**Luật đọc (viết trước khi chạy, script in ra dòng `[kết luận]`):**

| acc đã-thấy (epoch 5) | acc giữ-riêng | đọc là | việc kế |
|---|---|---|---|
| < 0,65 | — | khâu train có vấn đề | chạy K-4b (`--lam 0`, DPO thuần). Vẫn không lên thì có lỗi trong vòng train |
| 0,65–0,80 | — | chưa rõ | gửi log |
| ≥ 0,80 | ≥ 0,60 | cặp có tín hiệu, lượt cũ thiếu bước | đáng chạy GA-DPO đủ 830 cặp nhiều epoch rồi chấm |
| ≥ 0,80 | < 0,60 | học thuộc được nhưng cặp không có tín hiệu chung | đóng hướng, vấn đề ở cách dựng cặp (khớp RAFT) |

Nhìn thêm `acc_cai_thien` và `acc_giu` của tập giữ-riêng: cặp *giữ* (greedy vs mẫu thua mọi thước) dễ hơn, nên nếu
chỉ `acc_giu` lên mà `acc_cai_thien` ~0,5 thì mô hình chỉ học "đừng viết câu tệ", không học "viết câu tốt hơn greedy".

## 1. Máy và chi phí

- **Colab L4.** Cần bf16 nên Kaggle T4 không chạy được (`ga_dpo.py` và script này đều tự dừng trên T4).
  Không cần A100: lượt cũ cùng mô hình, cùng độ dài cặp đã chạy trên L4 không tràn.
- Thời gian [ước, chưa đo]: ref 400 cặp + 4 lượt đo × 400 cặp (chỉ forward) + 1.000 lượt cặp train (forward + backward)
  ≈ **2,5–3 giờ L4**. Mốc tham chiếu: lượt cũ 830 lượt cặp train (kèm forward ref) mất 107 phút.
- Pha bậc 0 (tải dữ liệu, hoà S1) nằm trong cùng phiên vì ngắn (~10 phút); không đáng tách.

## 2. Các ô

⭐ **Dùng notebook dựng sẵn: `_scripts/314/colab_gadpo/kiem_hoc_dpo_314_colab.ipynb`** (Colab → File → Upload notebook).
Notebook đã nhúng script ở ô K-2b (`%%writefile`), nên ở K-2 chỉ upload `~/.kaggle/uyenle/access_token`.
Các ô dưới đây là bản chép để tra; nếu chạy tay từ file này thì upload thêm `kiem_hoc_dpo.py` ở K-2.

```python
# K-1: gói + kiểm GPU
!pip -q install 'transformers==5.18.0' 'peft==0.21.1' 'kaggle==2.2.4' accelerate safetensors
!pip -q uninstall -y torchao
import torch
print(torch.cuda.get_device_name(0), torch.cuda.get_device_properties(0).total_memory / 2**30, "GiB")
assert torch.cuda.get_device_capability()[0] >= 8, "⛔ cần L4/A100 (bf16)"
```

```python
# K-1b: gắn Drive ngay từ đầu (lúc còn ngồi máy để bấm cho phép)
from google.colab import drive
import os
drive.mount("/content/drive")
DR = "/content/drive/MyDrive/thesis/gadpo314/kiem_hoc"
os.makedirs(DR, exist_ok=True)
print("[drive]", DR, sorted(os.listdir(DR)), flush=True)
```

```python
# K-2: upload HAI tệp: access_token (Kaggle uyenle) + kiem_hoc_dpo.py; rồi tải dữ liệu
from google.colab import files
up = files.upload()
ten_khoa = next(t for t in up if not t.endswith(".py"))
assert "kiem_hoc_dpo.py" in up, "⛔ chưa upload kiem_hoc_dpo.py"
os.environ["KAGGLE_API_TOKEN"] = open(ten_khoa).read().strip()   # không in khoá
os.remove(ten_khoa)
for ds, d in [("uyenle0712/gadpo-314", "/content/code"),
              ("uyenle0712/gadpo-314-cap", "/content/cap"),
              ("uyenle0712/fgrb-p1-bundle", "/content/bundle"),
              ("uyenle0712/grpo-spice-ck500", "/content/ck500")]:
    r = os.system(f"kaggle datasets download -d {ds} -p {d} --unzip -q")
    print(ds, "→", d, "OK" if r == 0 else f"LỖI {r}", flush=True)
    assert r == 0
```

```python
# K-3: đường dẫn, chép mã, hoà S1 ở fp16 (như D-3), đổi đường dẫn ảnh, tự kiểm script
import glob, shutil, subprocess, json, time
W = "/content/w"; os.makedirs(W, exist_ok=True)
M = "/content/s1_merged"
BUNDLE = next(r for r, d, f in os.walk("/content/bundle") if "adapter_s1_seed101" in d and "images" in d)
CK = next(r for r, d, f in os.walk("/content/ck500") if "adapter_config.json" in f)
CODE = os.path.dirname(next(glob.iglob("/content/code/**/ga_dpo.py", recursive=True)))
CAP = next(glob.iglob("/content/cap/**/cap_all.jsonl", recursive=True))
for f in os.listdir(CODE):
    if f.endswith(".py"): shutil.copy(f"{CODE}/{f}", W)
shutil.copy("/content/kiem_hoc_dpo.py", W)
ENV = {**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1",
       "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
def run(*a):
    r = subprocess.run(["python", *a], cwd=W, capture_output=True, text=True, env=ENV)
    print((r.stdout + r.stderr)[-3000:], flush=True); assert r.returncode == 0
run("kiem_hoc_dpo.py", "--tu-kiem", "--out", "/tmp/x")
run("-c", "import sys, argparse, torch, grpo_spice as G; G._dtype = lambda: torch.float16; "
          "G.merge(argparse.Namespace(bundle=sys.argv[1], merged=sys.argv[2], adapter=sys.argv[1] + '/adapter_s1_seed101'))",
    BUNDLE, M)
run("mau_sang_ga.py", "--vao", CAP, "--ra", f"{W}/cap_colab.jsonl", "--anh-moi", f"{BUNDLE}/images")
P = [json.loads(l) for l in open(f"{W}/cap_colab.jsonl")]
miss = [p["image"] for p in P if not os.path.exists(p["image"])]
print("cặp:", len(P), "· thiếu ảnh:", len(miss)); assert len(P) == 830 and not miss
```
Phải thấy: `[tự kiểm] ĐẠT` và `cặp: 830 · thiếu ảnh: 0`.

```python
# K-4: chạy phép kiểm (λ 1,0) — chạy nền, in tiến độ mỗi 2 phút. KHÔNG bấm Stop ô này.
def chay_kiem(out, *them):
    assert not os.path.exists(out), f"⛔ {out} đã có — xoá hoặc đổi tên"
    log = out + ".log"; T0 = time.time()
    p = subprocess.Popen(["python", "kiem_hoc_dpo.py", "--merged", M, "--ck500", CK,
                          "--cap-file", f"{W}/cap_colab.jsonl", "--out", out, *them],
                         cwd=W, env=ENV, stdout=open(log, "w"), stderr=subprocess.STDOUT, start_new_session=True)
    while p.poll() is None:
        time.sleep(120)
        dong = [l for l in open(log).read().splitlines() if l.strip()]
        print(time.strftime("%H:%M"), f"{(time.time()-T0)/60:.0f} phút", dong[-1:] if dong else "", flush=True)
        shutil.copy(log, f"{DR}/{os.path.basename(log)}")       # log sống sót nếu mất máy
    shutil.copy(log, f"{DR}/{os.path.basename(log)}")
    print("\n".join(l for l in open(log).read().splitlines() if l.startswith(("[chia]", "[cấu hình]", "[đo]", "[kết luận]", "DỪNG", "Traceback"))))
    assert p.returncode == 0, "⛔ lỗi — xem log"
    for t in os.listdir(out): shutil.copy(f"{out}/{t}", f"{DR}/{os.path.basename(out)}_{t}")
chay_kiem("/content/kiem_lam1")
```
Phải thấy dòng `[đo] epoch 0 · … marg +0.000 … ‖B‖ 0.0000` (nạp đúng), rồi ba dòng `[đo]` epoch 1, 3, 5 và dòng `[kết luận]`.

```python
# K-4b: CHỈ chạy khi K-4 kết luận "KHÂU TRAIN" — DPO thuần (λ 0) để xem phần NLL có kéo ngược không
chay_kiem("/content/kiem_lam0", "--lam", "0")
```

```python
# K-5: gói toàn bộ kết quả thành MỘT zip trên Drive
import zipfile
z = f"{DR}/ket_qua_kiem_hoc_dpo_314.zip"
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as f:
    for out in ("/content/kiem_lam1", "/content/kiem_lam0"):
        if os.path.exists(out):
            for t in os.listdir(out): f.write(f"{out}/{t}", f"{os.path.basename(out)}/{t}")
            f.write(out + ".log", os.path.basename(out) + ".log")
print(z, os.path.getsize(z), "byte")
```

## 3. Gửi lại

Zip `MyDrive/thesis/gadpo314/kiem_hoc/ket_qua_kiem_hoc_dpo_314.zip` (gồm `kiem_hoc_dpo.jsonl`, `ket_luan.json`, log).
Tải về đặt vào `runs/rd314/D/kiem_hoc/`. Tối thiểu dán các dòng `[đo]` và `[kết luận]` của K-4.

## 4. Lỗi hay gặp

| triệu chứng | xử lý |
|---|---|
| `DỪNG: ở epoch 0 policy phải trùng ref` | nền hoặc adapter nạp sai; gửi log, không chạy tiếp |
| OOM ở train | đổi runtime A100, chạy lại K-1 → K-4 (dữ liệu không lớn, ~10 phút dựng lại) |
| mất máy giữa K-4 | log đến lúc chết có ở Drive; chạy lại K-1 → K-4 từ đầu (script không nối tiếp, vì epoch đầu là phần rẻ) |
| `⛔ … đã có` | đã chạy rồi trong phiên; xoá thư mục `/content/kiem_lam1` nếu muốn chạy lại |
