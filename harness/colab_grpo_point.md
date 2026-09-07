# Colab A100 — GRPO thưởng `<point>` nối tiếp từ MIN-DESC/101 (viết 5/9/2026)

> Đăng ký trước: `report/106` mục **(x19)**. Lý do: `report/143` §4. Mã: `harness/grpo_point.py`.
> File này **tự đủ**. Bốn luật Colab (CLAUDE.md §Vận hành) áp nguyên: `start_new_session=True` ·
> KHÔNG bấm Stop ô nào khi train · ô theo dõi đọc log LOCAL · ô G6 chạy foreground suốt lượt.
> ⛔ Đồng hồ máy WSL là UTC; mốc giờ ở đây đọc bằng `TZ='Asia/Ho_Chi_Minh' date`.

## Thứ tự ô

| ô | việc | mất |
|---|---|---|
| G1 | GPU + cài gói (TRL pin 0.29.1) ▸ Restart runtime | 3 phút |
| G2 | Drive, kho, dữ liệu tiếng Anh, 64.567 ảnh, adapter MIN | 15–25 phút (ảnh) |
| G3 | selftest 0 GPU + kiểm gói đã lên Drive là bản MỚI | 2 phút |
| G4 | **THĂM DÒ** 20 bước trên 50 câu nhắc dài nhất — ba tiêu chí (x19c) | 10–15 phút |
| G5 | TRAIN nền, 500 bước, điểm lưu trên Drive | 8–20 h (đo ở G4) |
| G6 | THEO DÕI foreground (bắt buộc) | suốt lượt |
| G7 | xong: kiểm toàn vẹn + suy luận 4.463 + đóng gói cho Kaggle | 2,5 h |

---

## Ô G1 — GPU + cài gói ▸ rồi **Restart runtime**

```python
import subprocess
r = subprocess.run("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader",
                   shell=True, capture_output=True, text=True)
print("GPU:", r.stdout.strip() or "⛔ KHÔNG THẤY")
assert r.returncode == 0 and "A100" in r.stdout, "⛔ DỪNG — cần A100 (Runtime → Change runtime type)."

!pip install -q -U "trl==0.29.1" "transformers>=4.56.2" accelerate peft bitsandbytes datasets \
    pillow huggingface_hub
import importlib.metadata as m, torch
for p in ("trl", "transformers", "peft", "bitsandbytes", "datasets", "accelerate"):
    print(f"{p:14s}", m.version(p))
print("torch:", torch.__version__, "| CUDA build:", torch.version.cuda, "| khả dụng:", torch.cuda.is_available())
assert m.version("trl") == "0.29.1", "⛔ trl không đúng bản pin"
assert torch.version.cuda, ("⛔ pip vừa cài torch bản CPU. Sửa: "
    "!pip install -q -U torch --index-url https://download.pytorch.org/whl/cu124 rồi Restart, chạy lại G1.")
```

**Kiểm:** `trl 0.29.1` · `torch … CUDA build` không phải None. ⚠️ **Restart runtime** rồi mới G2.

---

## Ô G2 — Drive, kho, dữ liệu, ảnh, adapter MIN

```python
from google.colab import drive; drive.mount('/content/drive')
import os, zipfile, glob, torch, json
D, WS = "/content/drive/MyDrive/thesis", "/content/ws"
os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_rented.zip").extractall(WS)     # gói mã MỚI (có harness/grpo_point.py)
REPO = f"{WS}/thesis"; os.chdir(REPO)
TR = f"{REPO}/harness/dg1_cache/train_ac"
dem = lambda d: len(os.listdir(d)) if os.path.isdir(d) else 0

!tar xzf {D}/derived.tar.gz -C {REPO}
assert os.path.exists(f"{D}/derived_train_en.tar.gz"), "⛔ thiếu derived_train_en.tar.gz"
!tar xzf {D}/derived_train_en.tar.gz -C {REPO}           # ⚠️ BẮT BUỘC bung ĐÈ bản tiếng Anh
os.makedirs(f"{TR}/images", exist_ok=True)
if dem(f"{TR}/images") < 64567:
    for g in sorted(glob.glob(f"{D}/train_images_p*.tar")):
        !tar xf {g} -C {TR}/images

AD  = f"{D}/ckpt/min_desc_seed101"                        # ĐẦU VÀO — không đụng
OUT = f"{D}/ckpt/grpo_point_seed101"                      # ĐẦU RA — TRÊN DRIVE, phải RỖNG ở lượt mới
os.makedirs(OUT, exist_ok=True)
print("ảnh dạy   :", dem(f"{TR}/images"), "← 64.567")
print("khai báo  :", sum(1 for _ in open(f"{TR}/descriptors.jsonl")), "← 41.099")
print("s2.json   :", os.path.exists(f"{TR}/branches/s2.json"))
print("grpo_point:", os.path.exists(f"{REPO}/harness/grpo_point.py"), "← False thì gói trên Drive là bản CŨ")
print("adapter MIN:", os.path.isdir(AD), sorted(os.listdir(AD))[:8] if os.path.isdir(AD) else "")
print("OUT rỗng  :", sorted(os.listdir(OUT)), "← lượt MỚI phải là []")
cfg = json.load(open(f"{AD}/adapter_config.json")); print("adapter r/alpha:", cfg["r"], cfg["lora_alpha"])
```

**Kiểm:** ảnh **64.567** · khai báo **41.099** (1.074 = gói tiếng Anh chưa bung đè) · `grpo_point True` ·
adapter có `adapter_model.safetensors` + `adapter_config.json` · `OUT rỗng []`.

⚠️ Adapter MIN nằm ở **gốc** `ckpt/min_desc_seed101` (bước 800); các `checkpoint-*` bên trong là
điểm lưu giữa chừng — dùng **gốc**, đúng như `infer_branch.py` đã dùng khi chấm 60,05.

---

## Ô G3 — selftest 0 GPU (2 phút)

```python
!cd {REPO} && python harness/grpo_point.py --selftest
```
Phải in `✅ selftest ĐẠT`, `toàn tập … 41090`, `r_point trên khai báo vàng: 500/500`.

---

## Ô G4 — THĂM DÒ, 20 bước, 50 câu nhắc DÀI NHẤT (luật P10) — ba tiêu chí (x19c)

```python
import subprocess, os, time, re
PROBE = "/content/probe_grpo"; import shutil; shutil.rmtree(PROBE, ignore_errors=True)
cmd = ["python", f"{REPO}/harness/grpo_point.py", "--probe", "--adapter", AD, "--out", PROBE,
       "--images", f"{TR}/images", "--G", "4", "--accum", "4"]
t0 = time.time()
r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True,
                   env={**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1"})
open("/content/probe_grpo.log", "w").write(r.stdout + "\n=== STDERR ===\n" + r.stderr)
print(r.stdout[-6000:]); print("mã thoát:", r.returncode, "·", round((time.time()-t0)/60, 1), "phút")
oom = "out of memory" in (r.stdout + r.stderr).lower()
print("OOM:", oom)
```

**Ba tiêu chí (x19c), đọc từ `log_history.json` trong `PROBE`:**

```python
import json, statistics as st
h = json.load(open(f"{PROBE}/log_history.json"))
h = [x for x in h if "reward" in x]
K_RP = next((k for k in h[-1] if "r_point" in k and k.endswith("mean")), None)   # tên khoá đổi theo bản TRL
print("khoá metric:", sorted(h[-1].keys())); print("khoá r_point:", K_RP)
zs = [x.get("frac_reward_zero_std") for x in h if x.get("frac_reward_zero_std") is not None]
rp = [x.get(K_RP) for x in h if K_RP and x.get(K_RP) is not None]
cl = [x.get("completions/mean_length") for x in h if x.get("completions/mean_length") is not None]
print("① OOM                      :", oom, "← phải False")
print("② nhóm ĐỒNG ĐIỂM (zero std) :", round(st.mean(zs), 2) if zs else None, "← phải ≤ 0,60; >0,60 ⇒ một lần sửa duy nhất: --temp 1.2")
print("③ r_point trung bình        :", round(st.mean(rp), 3) if rp else None, "← phải trong [0,55; 0,95] (≈74,6% là kỳ vọng; ~1,0 = phần thưởng vô dụng)")
print("   độ dài câu trả lời       :", round(st.mean(cl), 1) if cl else None, "token ← 20–120")
print("   s/bước                   : xem dòng 'xong 20 bước · … s/bước' ở trên ⇒ ước 500 bước")
```

⛔ Không đạt ① ⇒ `--accum 2` (mỗi lượt sinh 2 câu nhắc × 4 = 8 chuỗi; 1.000 bước để giữ 2.000 câu nhắc — ghi (x19d)); vẫn OOM ⇒ dừng, báo lại. ② > 0,60 ⇒ chạy lại
G4 với `--temp 1.2` **một lần**; vẫn > 0,60 ⇒ dừng (mô hình quá chắc, GRPO không có tín hiệu — ghi (x19d)).
③ ngoài dải ⇒ đọc 2 mẫu in ở `log_completions`, tìm lỗi phân tách trước khi kết luận.

---

## Ô G5 — TRAIN nền (500 bước)

```python
import subprocess, os
LOG = "/content/train_grpo_point_seed101.log"
assert sorted(os.listdir(OUT)) == [] or input("OUT không rỗng — gõ TIEP nếu đang chạy tiếp sau mất máy: ") == "TIEP"
ck = sorted([d for d in os.listdir(OUT) if d.startswith("checkpoint-")], key=lambda s: int(s.split("-")[1]))
resume = [f"--resume", f"{OUT}/{ck[-1]}"] if ck else []
cmd = ["python", f"{REPO}/harness/grpo_point.py", "--train", "--adapter", AD, "--out", OUT,
       "--images", f"{TR}/images", "--G", "4", "--accum", "4",
       "--max-steps", "500", "--beta", "0.04", "--lr", "1e-5", "--temp", "1.0"] + resume
# ⚠️ --temp 1.2 CHỈ khi G4 đã buộc đổi (ghi (x19d)); mọi số khác KHÔNG đổi sau G4.
f = open(LOG, "a")
P = subprocess.Popen(cmd, cwd=REPO, stdout=f, stderr=subprocess.STDOUT, start_new_session=True,
                     env={**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1"})
print("PID", P.pid, "· resume:", resume or "không", "· log:", LOG)
```

Điểm lưu ghi thẳng vào `OUT` trên Drive mỗi **50** bước (`save_steps=50`, giữ 3 bản). Mất máy ⇒ dựng
lại G1–G2, chạy lại **G5** (tự thấy `checkpoint-*` và nối tiếp; `--resume` trỏ đúng thư mục).

---

## Ô G6 — THEO DÕI foreground (BẮT BUỘC chạy suốt lượt, đọc log LOCAL)

```python
import time, os, re, json
t0 = time.time(); last = 0
while P.poll() is None:
    time.sleep(120)
    s = open(LOG, encoding="utf-8", errors="ignore").read()
    g = lambda k: [float(v) for v in re.findall(rf"'{k}': '?([\d.eE+-]+)'?", s)]   # TRL in giá trị trong dấu nháy
    rw, rp, zs, kl = g("reward"), g("rewards/r_point/mean"), g("frac_reward_zero_std"), g("kl")
    tb = lambda xs, n=20: f"{sum(xs[-n:])/len(xs[-n:]):.3f}" if xs else "?"          # trung bình trượt 20 bước
    print(f"{time.strftime('%H:%M:%S')} · {(time.time()-t0)/3600:5.2f} h · bước {len(rw)}/500 · log +{len(s)-last} byte"
          + (f" · r_point TB20 {tb(rp)} (bước này {rp[-1]:.2f}) · reward TB20 {tb(rw)} · zero-std TB20 {tb(zs)} · kl {kl[-1]:.4f}" if rw else ""),
          flush=True)
    last = len(s)
    if "out of memory" in s.lower() or "Traceback" in s[-4000:]:
        print("⛔ có lỗi trong log — đọc 40 dòng cuối:"); print("\n".join(s.splitlines()[-40:])); break
print("mã thoát:", P.poll())
```

**Đọc:** `r_point TB20` (trung bình trượt 20 bước; từng bước chỉ 16 mẫu nên dao động 0,3–0,9 là bình thường) phải **tăng dần** từ ~0,7; `zero-std` giữ ≤ 0,6; `kl` hữu hạn và nhỏ (β = 0,04).
`r_point` tụt dưới 0,70 trong 100 bước liên tiếp hoặc `kl` bùng ⇒ dừng, không đọc tiếp, ghi (x19d).
⚠️ Log +0 byte trong 10 phút **không** phải treo nếu đang ở bước sinh — kiểm `ps -p {P.pid}` trước.

---

## Ô G6b — đọc XU HƯỚNG bằng số (chạy song song, KHÔNG Stop G6)

Ô G6 chỉ in trung bình trượt, mắt không phân biệt được xu hướng với nhiễu: mỗi bước chỉ 16 mẫu
nên `r_point` một bước lệch chuẩn ±0,11, trung bình 20 bước vẫn ±0,026. Ô này hồi quy trên **toàn
bộ** số bước đã có và in trị số t.

**Bản Terminal Colab** (biểu tượng `>_`; notebook đang bận ô G6 nên đây là đường tiện nhất):

```bash
python3 - <<'EOF'
import re, statistics as st
s = open("/content/train_grpo_point_seed101.log", encoding="utf-8", errors="ignore").read()
rp = [float(v) for v in re.findall(r"'rewards/r_point/mean': '?([\d.eE+-]+)'?", s)]
n = len(rp); k = min(100, n // 3)
print(f"n={n} · {k} buoc dau {st.mean(rp[:k]):.3f} +- {st.stdev(rp[:k])/k**.5:.3f}"
      f" · {k} buoc cuoi {st.mean(rp[-k:]):.3f} +- {st.stdev(rp[-k:])/k**.5:.3f}"
      f" · chenh {st.mean(rp[-k:])-st.mean(rp[:k]):+.3f}")
xb = (n-1)/2; yb = st.mean(rp)
b = sum((i-xb)*(y-yb) for i, y in enumerate(rp))/sum((i-xb)**2 for i in range(n))
res = [y - (yb + b*(i-xb)) for i, y in enumerate(rp)]
se = (sum(r*r for r in res)/(n-2)/sum((i-xb)**2 for i in range(n)))**.5
print(f"do doc {b*100:+.3f} diem/100 buoc · SE {se*100:.3f} · t = {b/se:+.1f} (|t|>2 la xu huong that)")
print("theo tram buoc:", [f"{st.mean(rp[i:i+100]):.3f}" for i in range(0, n-49, 100)])
for k2 in ("kl", "frac_reward_zero_std", "completions/clipped_ratio"):
    v = [float(x) for x in re.findall(rf"'{k2}': '?([\d.eE+-]+)'?", s)]
    if v: print(f"{k2:26s} dau {st.mean(v[:k]):.4f} · cuoi {st.mean(v[-k:]):.4f}")
EOF
```

**Bản notebook** — chỉ chạy trong **notebook THỨ HAI** (notebook đang chạy G6 sẽ xếp hàng), thay
`LOG` bằng `"/content/train_grpo_point_seed101.log"` nếu biến chưa có:

```python
import re, statistics as st
s = open(LOG, encoding="utf-8", errors="ignore").read()
rp = [float(v) for v in re.findall(r"'rewards/r_point/mean': '?([\d.eE+-]+)'?", s)]
n = len(rp); k = min(100, n // 3)
print(f"n={n} · {k} bước đầu {st.mean(rp[:k]):.3f} ± {st.stdev(rp[:k])/k**.5:.3f}"
      f" · {k} bước cuối {st.mean(rp[-k:]):.3f} ± {st.stdev(rp[-k:])/k**.5:.3f}"
      f" · chênh {st.mean(rp[-k:])-st.mean(rp[:k]):+.3f}")
xb = (n-1)/2; yb = st.mean(rp)
b = sum((i-xb)*(y-yb) for i, y in enumerate(rp))/sum((i-xb)**2 for i in range(n))
res = [y - (yb + b*(i-xb)) for i, y in enumerate(rp)]
se = (sum(r*r for r in res)/(n-2)/sum((i-xb)**2 for i in range(n)))**.5
print(f"độ dốc {b*100:+.3f} điểm/100 bước · SE {se*100:.3f} · t = {b/se:+.1f} (|t|>2 là xu hướng thật)")
print("theo trăm bước:", [f"{st.mean(rp[i:i+100]):.3f}" for i in range(0, n-49, 100)])
```

**Đọc:** `|t| > 2` ⇒ xu hướng tăng là thật, không phải nhiễu. `kl` cuối vẫn ≤ 0,05 ⇒ chính sách
chưa trôi khỏi MIN. `clipped_ratio` ≈ 0 ⇒ không câu nào bị cắt ở 128 token.
⚠️ Phần thưởng này đo trên **mẫu ngẫu nhiên (nhiệt độ 1,0) của tập DẠY**; điểm cuối đo bằng **giải
mã tham lam trên tập KIỂM**. Mức tăng ở đây **không** quy đổi một-một sang `exec`, thường co lại.
Kỳ vọng ghi trước ở (x19e) vẫn là **+2 … +4 pp**, không sửa theo đường cong này.

---

## Ô G7a — đọc log ĐÚNG TÊN KHOÁ (0 GPU, 10 giây)

⛔ Ô kiểm cũ ở G7 dò khoá **chỉ trong bản ghi cuối** `h[-1]`, mà bản ghi cuối của HF Trainer là
dòng tổng kết (`train_runtime`, `train_loss`) **không mang metric thưởng** ⇒ `K_RP = None`, danh
sách rỗng, in ra `bước: 0` và `0.0 → 0.0`. Đó là **lỗi ô đọc**, không phải lượt train hỏng —
đúng dạng đã ghi ở (x19d). Ô dưới quét toàn bộ bản ghi.

```python
import json
h = json.load(open(f"{OUT}/log_history.json"))
ks = sorted({k for x in h for k in x})
print("bản ghi:", len(h), "· khoá bản ghi cuối:", sorted(h[-1]))
print("mọi khoá:", ks)
K = [k for k in ks if "point" in k.lower()]
print("khoá thưởng point:", K)
for k in K + [c for c in ks if c in ("reward", "kl", "frac_reward_zero_std")]:
    v = [x[k] for x in h if k in x]
    if not v: continue
    n = len(v) // 5 or 1
    print(f"{k:34s} n={len(v):4d} theo 5 chặng:",
          [round(sum(v[i*n:(i+1)*n]) / len(v[i*n:(i+1)*n]), 3) for i in range(5)])
```

**Kiểm:** `n` phải là **500** (hoặc sát 500). Năm chặng cho biết `r_point` **đi lên hay đi ngang** —
đây là bằng chứng duy nhất hiện có rằng GRPO học được gì, vì G4 chưa đọc được mốc xuất phát.
Ghi cả năm số vào (x19d) ghi 2 **trước khi** suy luận.

---

## Ô G7b — adapter ra có KHÁC adapter MIN không (0 GPU, 30 giây)

`final/` có thư mục con `ref` (bản sao MIN dùng làm tham chiếu KL). Phép kiểm này loại khả năng
tệp ở **gốc** `final/` lại chính là bản `ref`, tức lượt train không ghi được gì.

```python
from safetensors.torch import load_file
A = load_file(f"{OUT}/final/adapter_model.safetensors")
B = load_file(f"{AD}/adapter_model.safetensors")
norm = lambda d: sum(float(v.float().pow(2).sum()) for v in d.values()) ** 0.5
print("số tensor:", len(A), "vs MIN", len(B))
print("‖GRPO‖ =", round(norm(A), 6), "· ‖MIN‖ =", round(norm(B), 6))
```

⛔ Hai chuẩn **trùng nhau tới nhiều chữ số** là dấu hiệu HỎNG (đã trả giá 20/8 với ba cấu hình ra
số trùng hai chữ số thập phân), không phải dấu hiệu ổn định. Phải khác nhau thấy rõ.

---

## Ô G7c — vá `ImportError: incompatible version of torchao` trước khi suy luận

Ô G1 cài TRL 0.29.1 kéo theo `peft` mới, trong khi máy Colab có sẵn `torchao 0.10.0`; `peft` nay
đòi > 0.16 **và ném lỗi ngay khi phát hiện bản cũ**, dù dự án không dùng torchao lần nào (lượng
tử hoá 4-bit là bitsandbytes). Gỡ hẳn, đừng nâng — nâng torchao kéo theo torch, mà torch đang
pin đúng bản CUDA.

```python
!pip uninstall -y -q torchao
!python -c "import importlib.util; print('torchao còn:', importlib.util.find_spec('torchao'))"
```

**Kiểm:** dòng cuối in `torchao còn: None`.

✅ **KHÔNG cần Restart runtime.** `infer_branch.py` chạy bằng `!python …`, tức một **tiến trình
con mới** đọc lại `site-packages` từ đĩa, nên nó không dính bản `peft` đã nạp sẵn trong kernel.
Restart chỉ cần khi bạn gọi `peft` **ngay trong ô notebook** — mà G7 không làm thế. Giữ kernel
sống thì `D`, `OUT`, `AD`, `REPO` còn nguyên, khỏi chạy lại G2.

---

## Ô G7d — adapter đổi BAO NHIÊU so với MIN (0 GPU, 30 giây)

Chuẩn tổng ở G7b chỉ loại được khả năng tệp gốc là bản sao `ref`; hai bộ trọng số rất khác nhau
vẫn có thể cho chuẩn gần bằng nhau. Phép đo đúng là **ghép cặp theo tên tensor** rồi lấy
‖Δ‖ / ‖MIN‖.

```python
from safetensors.torch import load_file
A = load_file(f"{OUT}/final/adapter_model.safetensors")
B = load_file(f"{AD}/adapter_model.safetensors")
kA, kB = set(A), set(B)
print("khoá chỉ có ở GRPO:", len(kA - kB), "· chỉ có ở MIN:", len(kB - kA))
chung = sorted(kA & kB)
num = sum(float((A[k].float() - B[k].float()).pow(2).sum()) for k in chung) ** 0.5
den = sum(float(B[k].float().pow(2).sum()) for k in chung) ** 0.5
mx = max((float((A[k].float() - B[k].float()).abs().max()), k) for k in chung)
print("tensor ghép được:", len(chung), "/", len(kB))
print("‖Δ‖ / ‖MIN‖ =", round(num / den, 6), "· ‖Δ‖ =", round(num, 6))
print("lệch lớn nhất:", round(mx[0], 6), "tại", mx[1])
```

⚠️ **`final/` lưu bf16 còn `final/ref/` (bản sao MIN) lưu fp32** — đo thật 6/9. So thẳng hai bên
thì ~1,7e-03 của `‖Δ‖` chỉ là sai số làm tròn của phép cast, không phải trọng số dịch chuyển.
`harness/doc_grpo_local.py` in riêng ba số: thô · sàn nhiễu cast · **dịch chuyển thật** (ép bản
đối chiếu về cùng lưới số rồi mới trừ). Chỉ đọc số thứ ba.

**Cách đọc, quyết định trước khi tiêu 2,5 h A100 cho suy luận:**
· `‖Δ‖/‖MIN‖` cỡ **1e-2 trở lên** ⇒ trọng số đã dịch chuyển thật, chạy suy luận.
· cỡ **1e-4 trở xuống** ⇒ 500 bước GRPO gần như không đổi được adapter; `exec` nhiều khả năng
  trùng MIN trong khoảng nhiễu, và tiền suy luận sẽ mua về một con số không phân biệt được với
  60,05. Dừng lại đọc `kl` và `r_point` theo chặng ở G7a trước.
· ⚠️ Khoảng giữa (1e-3) thì **không đoán** — chạy suy luận và để `exec` trả lời, ghi rõ độ dịch
  chuyển này vào (x19d).

---


## Ô G7 — xong: kiểm toàn vẹn, suy luận 4.463, đóng gói Kaggle

⛔ **Ô kiểm dưới có lỗi dò khoá — dùng G7a thay thế.** Giữ lại để đối chiếu; phần suy luận bên
dưới vẫn đúng. Và tiêu đề ghi *4.463* là nói về khâu **chấm**: suy luận vẫn chạy đủ **6.958** bước,
không đặt `--limit`.

```python
import json, os
h = json.load(open(f"{OUT}/log_history.json"))
K_RP = next((k for k in h[-1] if "r_point" in k and k.endswith("mean")), None)
tr = [x for x in h if K_RP in x]
print("bước:", len(tr), "← 500 · r_point 20 bước đầu", round(sum(x[K_RP] for x in tr[:20])/20, 3),
      "→ 20 bước cuối", round(sum(x[K_RP] for x in tr[-20:])/20, 3))
print("final:", sorted(os.listdir(f"{OUT}/final")))
assert os.path.exists(f"{OUT}/final/adapter_model.safetensors")
```

Rồi **suy luận trên 6.958 bước tập kiểm** như MIN (cùng `infer_branch.py`, greedy, không đổi gì):
```python
!tar xf {D}/test_images.tar -C {REPO}/harness/dg1_cache/test_ac
!cd {REPO} && python harness/infer_branch.py --adapter {OUT}/final --out {D}/preds_grpo_point_seed101.jsonl
```
⚠️ `--out` trỏ Drive **không sống qua mất máy** (đo 24/8): mở Terminal Colab chạy vòng `cp` sang
tên khác mỗi 5 phút (ô T11/T12 của `colab_train_min_desc.md`). Chữ ký tệp phải là `lora:final` —
đổi tên thư mục `final` → `grpo_point_seed101` **trước** khi suy luận để chữ ký đọc được:
`os.rename(f"{OUT}/final", f"{OUT}/grpo_point_seed101")` rồi `--adapter {OUT}/grpo_point_seed101`.

Chấm `exec` trên Kaggle theo `harness/kaggle_cham_min_desc.md` với `ten = "grpo_point_seed101"`
(upload `preds_grpo_point_seed101.jsonl` lên dataset `thesis-preds` version mới). Đọc theo (x19e).
