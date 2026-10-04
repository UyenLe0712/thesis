# Người nghe trắc nghiệm (comprehension accuracy) — Kaggle T4×2, 0 đồng — viết 14/9/2026

Mục đích: thêm một thước **có tiền lệ ở hội nghị lớn** cho số chính của luận văn. Người nghe là một mô hình
thị giác–ngôn ngữ **không thuộc họ Qwen, không học AndroidControl**, đọc ảnh đã vẽ số lên các phần tử bấm
được cùng **một câu hướng dẫn**, rồi trả lời số của phần tử cần chạm. Đúng khi ô được chọn chứa điểm chạm vàng.

- Tiền lệ: Mao et al. CVPR 2016 · Luo et al. CVPR 2017 · Seq2Act ACL 2020 · Mind2Web NeurIPS 2023 D&B.
- Người nghe **không thấy mục tiêu, không thấy các bước trước** ⇒ chỉ giải được khi câu đủ thông tin.
- Ứng viên: mọi phần tử bấm được trong cây trợ năng, trung vị **15 ô/màn** (chọn bừa ≈ 7%). Phủ đáp án
  **95,7%** (4.272/4.463) ⇒ trần lý thuyết 95,7. Chi tiết `harness/som_build.py`.
- Hai ứng viên người nghe (kiểm nguồn 14/9): **Phi-4-multimodal-instruct** (Microsoft, MIT, 5,6B, vừa 1 T4)
  và **Pixtral-12B** (Mistral, Apache-2.0, chia 2 T4).
- ⛔ **Luật chọn người nghe, khoá trước:** chạy cả hai trên **lát 200 bước cố định với CÂU CHUẨN**; mô hình nào
  cao hơn thì dùng cho mọi nhánh. Không nhìn điểm nhánh mô hình khi chọn.

| phần | việc | máy | thời gian |
|---|---|---|---|
| A | tạo dataset `thesis-som` (0,85 MB) | trình duyệt | 3 phút |
| B | Ô 0–3: cài đặt, dò đường dẫn | Kaggle | 10 phút |
| C | Ô 4–5: **Phi-4** chạy thử 8 bước rồi lát 200 (câu chuẩn + câu rỗng) | Kaggle | **đo ở Ô 4** |
| D | Ô 6–7: **Pixtral** chạy thử 8 bước rồi lát 200 câu chuẩn | Kaggle | **đo ở Ô 6** |
| E | Ô 8: đọc lát thử, **chọn người nghe** | Kaggle | 1 phút |
| F | Ô 9: chấm đủ 4.463 bước cho các nhánh, **tải kết quả về sau MỖI nhánh** | Kaggle | nhiều giờ |

---

## A. Tạo dataset (máy nhà)

1. Tải lên Kaggle tệp **`_bundles/thesis_som_v2.zip`** (dựng lại 14/9 tối: `sdpa` + bắt OOM) → **New Dataset**, tên
   **`thesis-som-v2`**. ⛔ Gỡ dataset `thesis-som` cũ khỏi notebook, nếu không `tim()` có thể nhặt mã cũ.
   ⛔ Dataset MỚI, không "New Version" dataset cũ.
2. Notebook mới → **Add Data**: `thesis-som-v2` và **`thesis-score`** (dataset ảnh 4.463 màn đã có từ tháng 8).
3. **Settings → Accelerator: GPU T4 ×2 · Internet: ON · Persistence: Files only** (nếu có).

---

## B. Cài đặt

### Ô 0 — cài thư viện (⛔ chạy ĐẦU TIÊN, rồi Restart)

```python
!pip uninstall -y -q torchao
!pip install -q transformers==4.48.2 peft==0.13.2 accelerate==1.3.0 backoff soundfile scipy
print("XONG — bấm Run ▸ Restart & clear cell outputs, rồi chạy Ô 1")
```

⚠️ Bắt buộc **Restart** sau ô này, không thì Python vẫn giữ bản transformers cũ trong bộ nhớ.
⚠️ `torchao` cài sẵn trên Kaggle làm `peft` báo lỗi lúc nạp LoRA (đã mất một buổi hôm 10/9).

### Ô 1 — kiểm phiên bản sau khi Restart

```python
import transformers, peft, torch, importlib.util
print("transformers", transformers.__version__, "← phải 4.48.2")
print("peft", peft.__version__, "← phải 0.13.2")
print("torchao còn:", importlib.util.find_spec("torchao"), "← phải None")
print("GPU:", torch.cuda.device_count(), [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])
```

Phải thấy **2 GPU Tesla T4**.

### Ô 2 — dò đường dẫn

```python
import glob, os, json
def tim(mau):
    r = sorted(glob.glob(f"/kaggle/input/**/{mau}", recursive=True))
    assert r, f"⛔ không thấy {mau} — kiểm đã Add Data chưa"
    return r[0]

SOM  = os.path.dirname(tim("som/som.jsonl"))                     # thư mục chứa som.jsonl, cau_*.jsonl
CODE = os.path.dirname(tim("som_listener.py"))              # chỉ dataset thesis-som có tệp này
IMG  = os.path.dirname(os.path.dirname(tim("test_ac/images/ep18171_s1.png")))   # <IMG>/images/ep….png
OUT  = "/kaggle/working/som"; os.makedirs(OUT, exist_ok=True)
print("SOM :", SOM); print("CODE:", CODE); print("IMG :", IMG)

rows = [json.loads(l) for l in open(f"{SOM}/som.jsonl")]
thieu = [r["image_goc"] for r in rows if not os.path.exists(os.path.join(IMG, r["image_goc"]))]
print(f"som.jsonl {len(rows)} bước ← cần 4463 · ảnh thiếu {len(thieu)} ← cần 0")
assert len(rows) == 4463 and not thieu
print(sorted(os.path.basename(p) for p in glob.glob(f"{SOM}/cau_*.jsonl")))
```

### Ô 3 — hàm chạy nền, in nhịp sống mỗi 2 phút

```python
import subprocess, time
PHI4_CROPS = 16     # ⛔ số mảnh ảnh của Phi-4. Mặc định 36 TRÀN BỘ NHỚ T4 (đo 14/9, OOM ở vision encoder).
                    # Giữ NGUYÊN cho mọi nhánh. Nếu 16 vẫn tràn thì hạ 9 và chạy lại từ Ô 4.
def chay(ten, lenh, gpu):
    """Chạy một tiến trình trên GPU chỉ định, ghi log ra tệp. Trả về Popen (không chờ)."""
    log = open(f"{OUT}/{ten}.log", "w")
    env = {**os.environ, "CUDA_VISIBLE_DEVICES": gpu, "PYTHONUNBUFFERED": "1",
           "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
           "SOM_PHI4_CROPS": str(PHI4_CROPS), "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
    print(">>", ten, "· GPU", gpu)
    return subprocess.Popen(["python", f"{CODE}/som_listener.py", *map(str, lenh)],
                            stdout=log, stderr=subprocess.STDOUT, env=env, start_new_session=True)

def cho(ds, nhip=120):
    """Chờ mọi tiến trình trong ds xong, in đuôi log mỗi `nhip` giây."""
    t0 = time.time()
    while any(p.poll() is None for _, p in ds):
        time.sleep(nhip)
        for ten, p in ds:
            duoi = open(f"{OUT}/{ten}.log").read().strip().splitlines()[-1:] or ["(chưa có dòng)"]
            print(f"{(time.time()-t0)/60:5.1f} phút · {ten}: {duoi[0][:150]}", flush=True)
    for ten, p in ds:
        print(ten, "mã thoát", p.returncode)
        print(open(f"{OUT}/{ten}.log").read()[-1500:])
```

⛔ Không bấm Stop ô `cho(...)` khi đang chạy lượt dài. Muốn xem thì mở tab **Terminal**, gõ `tail -3 /kaggle/working/som/*.log`.

---

## C. Phi-4-multimodal

### Ô 4 — chạy thử 8 bước câu chuẩn (đo tốc độ, xem câu trả lời thô)

```python
p = chay("thu_phi4", ["--backend", "phi4", "--img-root", IMG, "--som", f"{SOM}/som.jsonl",
                      "--cau", f"{SOM}/cau_chuan.jsonl", "--out", f"{OUT}/thu_phi4.jsonl",
                      "--mau", 200, "--limit", 8], gpu="0")
cho([("thu_phi4", p)], nhip=30)
for l in open(f"{OUT}/thu_phi4.jsonl"): print(l.strip())
```

**Kiểm ba thứ trong đầu ra:**
1. Log có dòng `[cấu hình] backend=phi4 · câu=cau_chuan.jsonl …` và `[mô hình] microsoft/Phi-4-multimodal-instruct`.
2. Trường `raw` là **một con số** (ví dụ `"10"`), không phải chuỗi rỗng hay chữ vô nghĩa. Nếu `raw` rỗng ở
   cả 8 bước ⇒ **dừng, dán log cho mình** (có thể tràn số fp16).
⚠️ **Đã gặp 14/9 (lần 2):** với 16 mảnh + `eager`, 8 bước chạy được nhưng lát 200 bước tràn bộ nhớ ở attention
   phần ngôn ngữ (`modeling_phi4mm.py:1157`). Bản mã `14/9-b` chuyển sang `sdpa` (lùi `eager` nếu mô hình không
   nhận) và **bắt OOM từng bước** (ghi `raw="__OOM__"`, tính trượt, chạy tiếp). Log phải in `[phi4] attn = …` và
   `[phiên bản mã] 14/9-b`.
⚠️ **Đã gặp 14/9 (lần 1):** 36 mảnh (mặc định) báo `CUDA out of memory` ở `vision_siglip_navit.py`. Ô 3 nay đặt
   `PHI4_CROPS = 16`. Log phải in `[phi4] dynamic_hd = 16`. Nếu 16 vẫn tràn: sửa Ô 3 thành 9, chạy lại Ô 3 rồi Ô 4.
3. Ghi lại **s/bước** (log in sau 25 bước; với 8 bước thì lấy tổng thời gian ở dòng "mã thoát" chia 8, trừ
   ~3–5 phút nạp mô hình lần đầu).

### Ô 5 — lát 200 bước: câu chuẩn trên GPU 0, câu rỗng trên GPU 1 (song song)

```python
ds = []
for ten, cau, gpu in [("chon_phi4_chuan_mau200", "cau_chuan", "0"), ("chon_phi4_san_mau200", "cau_san", "1")]:
    ds.append((ten, chay(ten, ["--backend", "phi4", "--img-root", IMG, "--som", f"{SOM}/som.jsonl",
                                "--cau", f"{SOM}/{cau}.jsonl", "--out", f"{OUT}/{ten}.jsonl", "--mau", 200], gpu)))
cho(ds)
```

---

## D. Pixtral-12B

### Ô 6 — chạy thử 8 bước câu chuẩn (chiếm cả hai GPU)

```python
p = chay("thu_pixtral", ["--backend", "pixtral", "--img-root", IMG, "--som", f"{SOM}/som.jsonl",
                         "--cau", f"{SOM}/cau_chuan.jsonl", "--out", f"{OUT}/thu_pixtral.jsonl",
                         "--mau", 200, "--limit", 8], gpu="0,1")
cho([("thu_pixtral", p)], nhip=30)
for l in open(f"{OUT}/thu_pixtral.jsonl"): print(l.strip())
```

Kiểm như Ô 4. Nếu báo **hết bộ nhớ (OOM)** ⇒ bỏ Pixtral, ghi lại lỗi, sang Ô 8 chỉ với Phi-4.

### Ô 7 — lát 200 bước câu chuẩn

```python
p = chay("chon_pixtral_chuan_mau200", ["--backend", "pixtral", "--img-root", IMG, "--som", f"{SOM}/som.jsonl",
         "--cau", f"{SOM}/cau_chuan.jsonl", "--out", f"{OUT}/chon_pixtral_chuan_mau200.jsonl", "--mau", 200], gpu="0,1")
cho([("chon_pixtral_chuan_mau200", p)])
```

---

## E. Ô 8 — đọc lát thử và chọn người nghe

```python
def diem(p):
    D = [json.loads(l) for l in open(p)]
    return len(D), 100 * sum(o["dung"] for o in D) / len(D), sum(1 for o in D if o["raw"] and o["chon"] is None)

for ten in ["chon_phi4_chuan_mau200", "chon_phi4_san_mau200", "chon_pixtral_chuan_mau200"]:
    f = f"{OUT}/{ten}.jsonl"
    if os.path.exists(f):
        n, e, ns = diem(f); print(f"{ten:30s} n={n:3d} · chọn đúng {e:5.1f}% · không ra số {ns}")

a = diem(f"{OUT}/chon_phi4_chuan_mau200.jsonl")[1]
b = diem(f"{OUT}/chon_pixtral_chuan_mau200.jsonl")[1] if os.path.exists(f"{OUT}/chon_pixtral_chuan_mau200.jsonl") else -1
NGUOI_NGHE = "phi4" if a >= b else "pixtral"
print("\n⇒ NGƯỜI NGHE ĐƯỢC CHỌN (luật: cao hơn trên câu chuẩn):", NGUOI_NGHE)
```

**Dán cho mình toàn bộ đầu ra Ô 8** trước khi chạy Ô 9. Cần thấy: câu chuẩn cao hơn hẳn câu rỗng (nếu câu
rỗng cũng cao gần câu chuẩn thì thước không phân biệt được, phải dừng xem lại).

---

## F. Ô 9 — chấm đủ 4.463 bước, từng nhánh một

Thứ tự ưu tiên: **grpo → chuan → san → s1_101 → base → min → s1_202**. Chạy mỗi lần **một nhánh**, xong thì
**tải tệp về** (panel phải → Output → `som/chon_…jsonl` → Download) trước khi sang nhánh kế.

```python
NHANH = "grpo"          # ← đổi lần lượt: grpo, chuan, san, s1_101, base, min, s1_202
ten = f"chon_{NGUOI_NGHE}_{NHANH}"
if NGUOI_NGHE == "phi4":        # Phi-4 vừa 1 T4 ⇒ chia đôi bước cho 2 GPU
    ds = [(f"{ten}_s{i}", chay(f"{ten}_s{i}", ["--backend", "phi4", "--img-root", IMG, "--som", f"{SOM}/som.jsonl",
           "--cau", f"{SOM}/cau_{NHANH}.jsonl", "--out", f"{OUT}/{ten}_s{i}.jsonl", "--shard", f"{i}/2"], gpu=str(i)))
          for i in (0, 1)]
else:
    ds = [(ten, chay(ten, ["--backend", "pixtral", "--img-root", IMG, "--som", f"{SOM}/som.jsonl",
           "--cau", f"{SOM}/cau_{NHANH}.jsonl", "--out", f"{OUT}/{ten}.jsonl"], gpu="0,1"))]
cho(ds)

# gộp hai nửa (nếu chạy 2 GPU) thành một tệp
with open(f"{OUT}/{ten}.jsonl", "a") as g:
    for i in (0, 1):
        f = f"{OUT}/{ten}_s{i}.jsonl"
        if os.path.exists(f):
            g.write(open(f).read())
n = sum(1 for _ in open(f"{OUT}/{ten}.jsonl"))
print(ten, n, "dòng ← cần 4463 (nhiều hơn là do gộp hai lần — mình lọc trùng ở máy nhà)")
```

⚠️ **Mất phiên giữa chừng:** tải các tệp `_s0`/`_s1` đang dở về; lần sau Add chúng thành dataset rồi copy vào
`/kaggle/working/som/` trước khi chạy lại — script tự bỏ qua bước đã chấm.
⚠️ Hạn mức 30 giờ GPU/tuần: tốc độ đo ở Ô 4 × 4.463 bước ÷ 2 GPU = giờ cho một nhánh. Rải các nhánh qua nhiều ngày.

---

## Ở máy nhà sau khi tải về

```bash
mkdir -p runs/som && mv ~/Downloads/chon_*.jsonl runs/som/
python3 harness/som_doc.py --thu-muc runs/som
```

---

## G. ⭐ CHẠY QUA ĐÊM — dạng commit (Save Version), tắt máy đi ngủ được

Dùng khi Ô 4 đã chạy ra `raw` là con số. ✅ **Đo 14/9 tối:** mã `14/9-b`, `sdpa`, 16 mảnh: **30/30 bước, OOM 0,
3,13 s/bước** trên một T4 ⇒ lát 200 ≈ 11 phút, một nhánh đủ 4.463 bước chia 2 GPU ≈ **2,1 giờ**; một đêm ≈ lát thử
+ 4 nhánh (grpo · chuan · san · s1_101) [suy từ tốc độ đo, Pixtral chưa đo]. Commit chạy trên máy chủ
Kaggle, **đóng trình duyệt vẫn chạy**, trần **12 giờ**; kết quả nằm ở tab **Output** của version.

**Cách làm:**
1. Notebook MỚI (hoặc xoá hết ô cũ), Add Data **`thesis-som-v2`** + `thesis-score` (⛔ không add `thesis-som` cũ),
   **GPU T4×2 · Internet ON**.
2. Dán **đúng một ô** dưới đây.
3. Bấm **Save Version → Save & Run All (Commit)** → đi ngủ.
4. Sáng dậy: mở version → tab **Output** → tải cả thư mục `som/` về → dán cho mình tệp `som/tom_tat.txt`.

Ô này tự làm theo thứ tự, không cần ai bấm:
- lát 200 bước: Phi-4 (câu chuẩn + câu rỗng, song song 2 GPU) → Pixtral (câu chuẩn, 2 GPU);
- **chọn người nghe theo luật khoá trước** (cao hơn trên câu chuẩn);
- **phép kiểm an toàn:** câu chuẩn phải hơn câu rỗng ≥ 20 điểm, không đạt thì DỪNG, không chấm tiếp;
- chấm đủ 4.463 bước theo thứ tự grpo → chuan → san → s1_101 → base → min → s1_202, **chỉ bắt đầu nhánh
  mới nếu ước thời gian còn đủ dưới 11 giờ**; tới 11,3 giờ thì dừng tiến trình để kịp lưu Output.

```python
import os, sys, glob, json, time, subprocess, re
T0 = time.time()
TRAN_GIO = 11.3                     # dừng cứng trước trần 12 h của commit
PHI4_CROPS = 16                     # chốt 14/9 (36 tràn bộ nhớ T4)

subprocess.run("pip uninstall -y -q torchao; pip install -q transformers==4.48.2 peft==0.13.2 "
               "accelerate==1.3.0 backoff soundfile scipy", shell=True)
# ⚠️ Không import transformers ở tiến trình chính: các tiến trình con khởi động sau khi cài nên dùng đúng bản mới.
from huggingface_hub import snapshot_download        # tải Phi-4 MỘT lần trước, tránh hai tiến trình song song cùng tải
snapshot_download("microsoft/Phi-4-multimodal-instruct")

def tim(mau):
    r = sorted(glob.glob(f"/kaggle/input/**/{mau}", recursive=True)); assert r, mau; return r[0]
SOM  = os.path.dirname(tim("som/som.jsonl"))
CODE = os.path.dirname(tim("som_listener.py"))
assert "14/9-b" in open(f"{CODE}/som_listener.py").read(), "⛔ đang dùng mã CŨ — gỡ dataset thesis-som, chỉ giữ thesis-som-v2"
IMG  = os.path.dirname(os.path.dirname(tim("test_ac/images/ep18171_s1.png")))
OUT  = "/kaggle/working/som"; os.makedirs(OUT, exist_ok=True)
TOM  = open(f"{OUT}/tom_tat.txt", "a")
def ghi(*a):
    s = f"[{(time.time()-T0)/3600:5.2f} h] " + " ".join(map(str, a)); print(s, flush=True); TOM.write(s + "\n"); TOM.flush()
ghi("SOM", SOM, "· CODE", CODE, "· IMG", IMG)

def chay(ten, backend, cau, gpu, extra=()):
    log = open(f"{OUT}/{ten}.log", "w")
    env = {**os.environ, "CUDA_VISIBLE_DEVICES": gpu, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1",
           "HF_HUB_DISABLE_PROGRESS_BARS": "1", "SOM_PHI4_CROPS": str(PHI4_CROPS),
           "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
    cmd = [sys.executable, f"{CODE}/som_listener.py", "--backend", backend, "--img-root", IMG,
           "--som", f"{SOM}/som.jsonl", "--cau", f"{SOM}/cau_{cau}.jsonl", "--out", f"{OUT}/{ten}.jsonl", *map(str, extra)]
    return subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, env=env, start_new_session=True)

def cho(ds, nhip=120):
    while any(p.poll() is None for _, p in ds):
        time.sleep(nhip)
        if (time.time() - T0) / 3600 > TRAN_GIO:
            ghi("⛔ chạm trần giờ — dừng tiến trình để kịp lưu Output")
            for _, p in ds: p.terminate()
            time.sleep(20); break
        for ten, _ in ds:
            d = open(f"{OUT}/{ten}.log").read().strip().splitlines()[-1:] or [""]
            print(f"  {(time.time()-T0)/3600:5.2f} h · {ten}: {d[0][:140]}", flush=True)
    for ten, p in ds:
        ghi(ten, "mã thoát", p.poll())

def diem(ten):
    f = f"{OUT}/{ten}.jsonl"
    if not os.path.exists(f): return 0, -1.0
    D = {}
    for l in open(f):
        try: o = json.loads(l); D[(o["episode_id"], o["step_id"])] = o
        except json.JSONDecodeError: pass
    return len(D), (100 * sum(o["dung"] for o in D.values()) / len(D) if D else -1.0)

def toc_do(ten):
    s = re.findall(r"([\d.]+) s/bước", open(f"{OUT}/{ten}.log").read())
    return float(s[-1]) if s else None

# ── 1. lát thử Phi-4 ─────────────────────────────────────────────────────────
cho([("chon_phi4_chuan_mau200", chay("chon_phi4_chuan_mau200", "phi4", "chuan", "0", ["--mau", 200])),
     ("chon_phi4_san_mau200",   chay("chon_phi4_san_mau200",   "phi4", "san",   "1", ["--mau", 200]))])
n1, a = diem("chon_phi4_chuan_mau200"); n2, s0 = diem("chon_phi4_san_mau200"); v_phi = toc_do("chon_phi4_chuan_mau200")
ghi(f"Phi-4 lát 200: câu chuẩn {a:.1f}% (n={n1}) · câu rỗng {s0:.1f}% (n={n2}) · {v_phi} s/bước")

# ── 2. lát thử Pixtral ───────────────────────────────────────────────────────
cho([("chon_pixtral_chuan_mau200", chay("chon_pixtral_chuan_mau200", "pixtral", "chuan", "0,1", ["--mau", 200]))])
n3, b = diem("chon_pixtral_chuan_mau200"); v_pix = toc_do("chon_pixtral_chuan_mau200")
ghi(f"Pixtral lát 200: câu chuẩn {b:.1f}% (n={n3}) · {v_pix} s/bước")

# ── 3. chọn người nghe theo luật khoá trước ─────────────────────────────────
NN = "phi4" if (n1 >= 190 and a >= b) or n3 < 190 else "pixtral"
ghi("⇒ NGƯỜI NGHE:", NN, "(luật: cao hơn trên câu chuẩn, lát 200)")
if NN == "pixtral":
    cho([("chon_pixtral_san_mau200", chay("chon_pixtral_san_mau200", "pixtral", "san", "0,1", ["--mau", 200]))])
    s0 = diem("chon_pixtral_san_mau200")[1]
tran = a if NN == "phi4" else b
AN_TOAN = tran - s0 >= 20
if not AN_TOAN:     # không raise: commit lỗi có thể không lưu Output
    ghi(f"⛔ DỪNG: câu chuẩn {tran:.1f} chỉ hơn câu rỗng {s0:.1f} là {tran-s0:.1f} điểm (< 20) — thước không phân biệt được")
v = v_phi if NN == "phi4" else v_pix
gio_nhanh = (4463 * v / (2 if NN == "phi4" else 1)) / 3600 * 1.1 if v else 99
ghi(f"ước một nhánh đủ 4.463 bước ≈ {gio_nhanh:.1f} h")

# ── 4. chấm đủ, từng nhánh, có cổng giờ ─────────────────────────────────────
for nh in (["grpo", "chuan", "san", "s1_101", "base", "min", "s1_202"] if AN_TOAN else []):
    con = TRAN_GIO - (time.time() - T0) / 3600
    if con < gio_nhanh * 0.5:
        ghi(f"bỏ qua {nh} và các nhánh sau: còn {con:.1f} h"); break
    ten = f"chon_{NN}_{nh}"
    if NN == "phi4":
        cho([(f"{ten}_s{i}", chay(f"{ten}_s{i}", "phi4", nh, str(i), ["--shard", f"{i}/2"])) for i in (0, 1)])
        with open(f"{OUT}/{ten}.jsonl", "w") as g:
            for i in (0, 1):
                if os.path.exists(f"{OUT}/{ten}_s{i}.jsonl"): g.write(open(f"{OUT}/{ten}_s{i}.jsonl").read())
    else:
        cho([(ten, chay(ten, "pixtral", nh, "0,1"))])
    n, e = diem(ten)
    ghi(f"{ten}: {n} bước · chọn đúng {e:.2f}%  {'(ĐỦ)' if n == 4463 else '(CHƯA ĐỦ — lần sau chạy tiếp)'}")
ghi("KẾT THÚC")
```

⚠️ Nhánh nào chưa đủ 4.463 bước (log ghi `CHƯA ĐỦ`): lần commit sau, **Add Data ▸ Your Notebooks ▸ version
này**, rồi thêm một dòng copy `som/*.jsonl` của output cũ vào `/kaggle/working/som/` ngay sau khi tạo `OUT` —
script tự bỏ qua các bước đã chấm. Mình sẽ viết sẵn dòng đó khi cần.
