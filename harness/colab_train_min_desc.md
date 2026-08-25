# MIN-DESC — lượt train thật, dán thẳng theo thứ tự

**Chỉ chạy file này SAU KHI `harness/colab_smoke_orpo.md` in `✅ QUA CỔNG`.** Chưa qua smoke mà
train là đốt 6–8 giờ để biết một thứ mà 1 giờ đã biết được.

Quyết định: `report/117` · Đăng ký trước: `report/106` mục **(x)**.

**Bốn lượt, theo đúng thứ tự này:**

| # | nhánh | hạt giống | cấu hình | ước |
|---|---|---|---|---|
| 1 | `min_desc` | 101 | `train_config_orpo.yaml` | 6–8 h |
| 2 | `ce2_s2` | 101 | `train_config_ce2.yaml` | 3–4 h |
| — | **cổng cơ học** — không gọi bộ trỏ | | | |
| 3 | `min_desc` | 202 | `train_config_orpo.yaml` | 6–8 h |
| 4 | `ce2_s2` | 202 | `train_config_ce2.yaml` | 3–4 h |

⛔ Cổng sau lượt 1–2 chỉ được dùng tín hiệu **không cần UGround/UI-Venus** — (x6) cấm dùng bộ trỏ
để làm điều kiện chạy hạt giống thứ hai. Xem ô T8.

> **Nếu vừa chạy smoke xong trong CÙNG máy ảo:** bỏ qua T1–T3, vào thẳng **T4**.

## Thứ tự ô — file này TỰ ĐỦ, không phải mở file nào khác

`T1` → **Restart runtime** → `T2` → `T3` → `T4` → `T5` → `T6` → `T7` → (xong lượt) `T8`

| mục | số ô mã | chạy khi nào |
|---|---|---|
| T1 · T2 · T3 | 1 mỗi mục | mọi máy ảo mới. **Restart runtime sau T1** |
| **T4** | **2** | ô 1 **luôn chạy** · ô 2 **CHỈ chạy nếu** dòng ④ báo `output_dir` đã có `checkpoint-*` **ở lượt MỚI** |
| T5 · T6 · T7 | 1 mỗi mục | T6 chạy **ngay sau** T5 · T7 là ô theo dõi, bấm ⏹ lúc nào cũng được |
| **T8** | **2** | ô 1 kiểm toàn vẹn sau mỗi lượt · ô 2 là **cổng cơ học**, chỉ chạy sau khi có **cả** MIN-DESC/101 **lẫn** CE2-S2/101 |
| T9 | 1 | chỉ khi nghi treo |

⚠️ **Ô 2 của T4 là `shutil.rmtree(OUT)` — đừng chạy theo quán tính.** Ở lượt **chạy tiếp sau khi
mất máy**, `output_dir` CÓ `checkpoint-*` là **đúng**, xoá đi là mất hết tiến độ đã train.

---

## Ô T1 — cài gói  ▸ rồi **Restart runtime**

```python
# ⛔ PHÉP RẺ NHẤT, ĐẶT TRƯỚC MỌI THỨ. Không có phép này thì lỗi "no GPU" chỉ nổ ở CUỐI ô T2,
#    tức sau khi đã bung 31 GB ảnh mất 15–25 phút — và đổi runtime lại xoá sạch, làm lại từ đầu.
import subprocess
r = subprocess.run("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader",
                   shell=True, capture_output=True, text=True)
print("GPU:", r.stdout.strip() or "⛔ KHÔNG THẤY")
assert r.returncode == 0 and r.stdout.strip(), (
    "⛔ DỪNG — máy ảo KHÔNG có GPU.\n"
    "   Runtime → Change runtime type → A100 → Save.\n"
    "   ⚠️ Việc đó khởi động lại máy ảo và XOÁ SẠCH /content ⇒ làm lại từ ô T1.")

!pip install -q -U "transformers>=4.49" accelerate peft bitsandbytes datasets \
    huggingface_hub pyarrow pillow pyyaml liger-kernel
# ⚠️ PIN đúng SHA đã dùng lúc smoke 23/8 — (x6) đòi CẢ BỐN LƯỢT cùng một bản.
#    LLaMA-Factory đã chứng minh là đổi hành vi giữa các bản (stack này mất `loss`/`lr`
#    khỏi trainer_log.jsonl so với tháng 8), nên lượt 1 và lượt 4 khác bản là hỏng phép so.
#    KHÔNG dùng --depth 1: bản clone nông không checkout được commit chỉ định.
!git clone https://github.com/hiyouga/LLaMA-Factory /content/LLaMA-Factory
!cd /content/LLaMA-Factory && git checkout c4e09c7cbe18844816af9e18a97fe465515edbcd
!pip install -q -e "/content/LLaMA-Factory[torch,metrics]"
!cd /content/LLaMA-Factory && git rev-parse HEAD    # phải in ra ĐÚNG c4e09c7cbe18…
import importlib.metadata as m, torch
print("liger-kernel:", m.version("liger_kernel"))
print("torch:", torch.__version__, "| CUDA build:", torch.version.cuda,
      "| khả dụng:", torch.cuda.is_available())
assert torch.version.cuda, (
    "⛔ DỪNG — pip vừa cài torch bản CPU-only, đè lên bản CUDA của Colab.\n"
    "   Sửa: !pip install -q -U torch --index-url https://download.pytorch.org/whl/cu124\n"
    "   rồi Restart runtime và chạy lại ô T1 từ đầu.")
```

**Kiểm bốn dòng:** `GPU:` có tên card · `git rev-parse HEAD` in đúng `c4e09c7cbe18…` ·
`liger-kernel` có số · `torch … CUDA build` **không phải None**.

⚠️ **Restart runtime**, rồi mới chạy ô T2.

---

## Ô T2 — Drive, kho, dữ liệu

```python
from google.colab import drive; drive.mount('/content/drive')
import os, zipfile, glob, torch, yaml
D, WS = "/content/drive/MyDrive/thesis", "/content/ws"
os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_rented.zip").extractall(WS)
REPO = f"{WS}/thesis"; os.chdir(REPO)
TR = f"{REPO}/harness/dg1_cache/train_ac"
dem = lambda d: len(os.listdir(d)) if os.path.isdir(d) else 0

!tar xzf {D}/derived.tar.gz -C {REPO}
# ⚠️ BẮT BUỘC: bung ĐÈ bản tiếng Anh. derived.tar.gz là bản khai báo TIẾNG VIỆT (trước 14/8).
#    Quên dòng này là train trên dữ liệu KHÁC mà log không báo gì.
assert os.path.exists(f"{D}/derived_train_en.tar.gz"), "⛔ thiếu derived_train_en.tar.gz"
!tar xzf {D}/derived_train_en.tar.gz -C {REPO}
print("đã bung đè bản TIẾNG ANH ✅")

os.makedirs(f"{TR}/images", exist_ok=True)
if dem(f"{TR}/images") >= 64567:
    print("ảnh dạy đã đủ — bỏ qua khâu bung")
else:
    for g in sorted(glob.glob(f"{D}/train_images_p*.tar")):
        !tar xf {g} -C {TR}/images

print("card    :", torch.cuda.get_device_name(0))
print("lõi CPU :", os.cpu_count())
print("ảnh dạy :", dem(f"{TR}/images"), "← cần 64.567")
print("khai báo:", sum(1 for _ in open(f"{TR}/descriptors.jsonl")), "← cần 41.099")
print("ckpt S2 :", os.path.isdir(f"{D}/ckpt/s2_seed101"),
      os.listdir(f"{D}/ckpt/s2_seed101")[:6] if os.path.isdir(f"{D}/ckpt/s2_seed101") else "")
```

**Kiểm bốn dòng:** ảnh dạy **64.567** · khai báo **41.099** · `ckpt S2` là `True` và có
`adapter_model.safetensors` · card đúng loại định dùng cho cả bốn lượt.

⛔ Khai báo ra **1.074** nghĩa là gói tiếng Anh chưa bung đè — dừng, đừng chạy tiếp.

⚠️⚠️ **`ckpt/s2_seed101` CÓ SẴN `checkpoint-8000`, `checkpoint-8072` — ĐÓ LÀ ĐÚNG, ĐỪNG DỌN.**
Thư mục đó là **ĐẦU VÀO** của MIN-DESC: adapter mà cả hai nhánh nối tiếp từ đó
(`adapter_name_or_path`). Gốc thư mục là adapter cuối (bước 8.072), hai `checkpoint-*` là điểm
lưu giữa chừng do `save_total_limit: 2` giữ lại.

| thư mục | vai trò | phải như nào |
|---|---|---|
| `ckpt/s2_seed101` | **ĐẦU VÀO** — adapter nối tiếp | **PHẢI có sẵn**, không đụng |
| `ckpt/min_desc_seed101` · `ckpt/ce2_s2_seed101` … | **ĐẦU RA** — lượt mới | **PHẢI RỖNG** ở lượt mới |

⛔ Dòng ④ của ô T4 và ô `shutil.rmtree(OUT)` **chỉ nói về cột ĐẦU RA**. Chĩa `rmtree` vào
`s2_seed101` là mất vĩnh viễn nhánh S2 — mà S2/202 đã quyết không chạy lại, nên không dựng lại được.

ℹ️ `test_images.tar` chứa **đúng 6.958 ảnh** — bằng số bản ghi `test.jsonl`, 0 ảnh thiếu.
(Thư mục gốc trên máy dựng có 6.969 vì còn 11 ảnh màn-cuối không bản ghi nào tham chiếu.)

ℹ️ Ô này **không** bung ảnh tập kiểm (3,2 GB). Chỉ cần chúng ở bước cổng cơ học sau lượt 1–2;
lúc đó chạy `!tar xf {D}/test_images.tar -C {REPO}/harness/dg1_cache/test_ac` (~3 phút).

---

## Ô T3 — dựng cặp

```python
!cd {REPO} && python harness/build_min_desc.py
```
`cặp dựng được` = **22854** · bảy bất biến **✅**.

---

## Ô T4 — chọn nhánh, sinh cấu hình, **tám phép tiền bay**

```python
import yaml, os, json, shutil
from PIL import Image

# ⚠️⚠️ ĐÂY LÀ HAI DÒNG DUY NHẤT ĐỔI GIỮA BỐN LƯỢT ⚠️⚠️
NHANH, SEED = "min_desc", 101        # lượt 2: ("ce2_s2",101) · 3: ("min_desc",202) · 4: ("ce2_s2",202)

CFG_GOC = {"min_desc": "train_config_orpo.yaml", "ce2_s2": "train_config_ce2.yaml"}[NHANH]
OUT = f"{D}/ckpt/{NHANH}_seed{SEED}"          # TRÊN DRIVE — mất máy vẫn còn
LOG = f"/content/train_{NHANH}_seed{SEED}.log"
os.makedirs(OUT, exist_ok=True)

c = yaml.safe_load(open(f"{REPO}/harness/{CFG_GOC}", encoding="utf-8"))
c.update({"seed": SEED, "output_dir": OUT,
          "dataset_dir": f"{REPO}/harness/dg1_cache/train_ac/branches"})
for k in ("max_samples",):                     # khoá của smoke, KHÔNG được sót
    c.pop(k, None)
yaml.safe_dump(c, open("/content/cfg.yaml","w",encoding="utf-8"),
               allow_unicode=True, sort_keys=False)

g = yaml.safe_load(open(f"{REPO}/harness/train_config.yaml", encoding="utf-8"))
info = json.load(open(f"{c['dataset_dir']}/dataset_info.json", encoding="utf-8"))
if c["dataset"] not in info:
    raise SystemExit(
        f"⛔ DỪNG — dataset_info.json KHÔNG có khoá '{c['dataset']}'.\n"
        "   Nguyên nhân gần như chắc chắn: ô T2 đã bung derived.tar.gz và GHI ĐÈ\n"
        "   dataset_info.json bằng bản chỉ có 4 nhánh cũ.\n"
        "   ⇒ Chạy lại ô T3 (build_min_desc.py) rồi chạy lại ô T4. Mất 2 phút.")
ds = json.load(open(f"{c['dataset_dir']}/{info[c['dataset']]['file_name']}", encoding="utf-8"))
v = os.statvfs('/content')
cho_phep = {"dataset","seed","output_dir","dataset_dir","adapter_name_or_path",
            "create_new_adapter","stage","pref_loss","pref_beta","max_steps",
            "num_train_epochs","per_device_train_batch_size","gradient_accumulation_steps",
            "enable_liger_kernel","preprocessing_num_workers","save_steps",
            "learning_rate"}     # ← stage-2 hạ còn 2e-5, xem report/106 (x3b)
khac = {k for k in set(c)|set(g) if c.get(k) != g.get(k)}

# ⓿ GÓI MỚI ĐÃ LÊN DRIVE CHƯA — kiểm trước mọi thứ. Gói cũ có LR 1e-4 và thiếu 3 tệp.
moi_du = (abs(c["learning_rate"] - 2.0e-5) < 1e-12
          and os.path.exists(f"{REPO}/harness/gate_desc_acc.py")
          and os.path.exists(f"{REPO}/harness/build_min_desc.py"))
print("⓿ learning_rate  :", c["learning_rate"], "← phải là 2e-05, KHÔNG phải 0.0001")
print("   gate_desc_acc :", os.path.exists(f"{REPO}/harness/gate_desc_acc.py"))
print("   → gói trên Drive là bản MỚI:", moi_du, "← False thì DỪNG, upload lại rồi chạy lại T2")
print("① nhánh          :", NHANH, "· hạt giống", SEED, "· dataset", c["dataset"])
print("   khoá lệch ngoài danh sách:", sorted(khac - cho_phep), "← phải là []")
print("② khoá smoke sót :", [k for k in ("max_samples",) if k in c], "← phải là []")
print("③ cỡ lô hiệu dụng:", c["per_device_train_batch_size"]*c["gradient_accumulation_steps"],
      "← phải là 16 · max_steps", c.get("max_steps"), "← 800")
print("④ output_dir     :", OUT)
print("   trên Drive    :", OUT.startswith("/content/drive/"), "← BẮT BUỘC True")
print("   bên trong     :", sorted(os.listdir(OUT)), "← lượt MỚI phải là []")
print("⑤ số mẫu         :", len(ds), "← phải là 22854")
print("   ranking       :", info[c["dataset"]].get("ranking"),
      "←", "True" if NHANH=="min_desc" else "None")
print("⑥ nối từ adapter :", c["adapter_name_or_path"], "· có thật:",
      os.path.isdir(c["adapter_name_or_path"]), "· create_new_adapter:", c.get("create_new_adapter"))
p = ds[0]["images"][0]
print("⑦ ảnh mẫu mở được:", os.path.exists(p)); Image.open(p).close()
print("⑧ đĩa trống      :", round(v.f_bavail*v.f_frsize/2**30,1), "GB ← cần ≥ 20")
print("\n   800 update × lô 16 =", 800*16, "cặp =", round(800*16/len(ds),2),
      "epoch — KHÔNG phải 1 epoch, đừng viết nhầm trong bài.")
```

**Tám dòng, tám điều kiện.** ① `[]` · ② `[]` · ③ `16` và `800` · ④ `True` và `[]` · ⑤ `22854` ·
⑥ `True`/`False` · ⑦ `True` · ⑧ ≥ 20.

⚠️ **Dòng ④ "bên trong" bắt lỗi im lặng đắt nhất:** LLaMA-Factory **tự chạy tiếp** từ
`checkpoint-*` còn sót trong `output_dir` và **không báo gì**. Lượt MỚI thấy có checkpoint thì:
```python
import shutil; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT, exist_ok=True)
```
⚠️ Nhưng khi **chạy tiếp sau khi mất máy** thì thấy `checkpoint-*` là **ĐÚNG** — bỏ qua đúng dòng
đó, **đừng xoá**.

---

## Ô T5 — TRAIN, chạy nền

```python
import subprocess, os
# ⛔ CHẶN PHÓNG HAI LẦN. 15-30 phút mã hoá token đầu trông y hệt treo, rất dễ dán lại ô này.
#    Hai tiến trình cùng ghi một output_dir là hỏng cả lượt VÀ hỏng điểm lưu trên Drive.
dang = subprocess.run(["pgrep","-af","llamafactory-cli"], capture_output=True, text=True).stdout
if "llamafactory-cli train" in dang:
    raise SystemExit("⛔ DỪNG — đã có một tiến trình train đang chạy:\n  " + dang.strip()
        + "\n   Nếu nó là lượt bạn vừa phóng: KHÔNG phóng lại, mở ô T7 mà xem."
        + "\n   Nếu thật sự cần giết: !pkill -f llamafactory-cli  rồi chạy lại ô này.")
env = dict(os.environ, PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True")
f = open(LOG, "a")                       # ⚠️ "a" chứ không phải "w" — chạy tiếp phải nối
p = subprocess.Popen(["llamafactory-cli", "train", "/content/cfg.yaml"],
                     cwd=REPO, stdout=f, stderr=subprocess.STDOUT,
                     env=env, start_new_session=True)
print("đã khởi động, PID", p.pid, "→", LOG)
```

⏳ **~15–30 phút đầu KHÔNG có bước train nào** — đang mã hoá token 22.854 mẫu (`min_desc` phải mã
hoá **cả hai vế** nên lâu gần gấp đôi `ce2_s2`). Log chỉ có `Running tokenizer on dataset`.
**Không phải treo.**

`start_new_session=True` ⇒ tiến trình rời hẳn nhân Python. Bấm ⏹ ở ô theo dõi **không** giết train.

---

## Ô T6 — đồng bộ lên Drive mỗi 5 phút  ⚠️ chạy NGAY sau T5

Điểm lưu đã nằm sẵn trên Drive (`output_dir`). Ô này đồng bộ thêm **log** và **cấu hình** — thứ
cần để chẩn đoán sau khi mất máy, và để đọc tiến độ từ điện thoại.

```python
import os, threading, time, shutil
DST = f"{D}/logs/{NHANH}_seed{SEED}"
os.makedirs(DST, exist_ok=True)
shutil.copy("/content/cfg.yaml", DST)          # bằng chứng "chỉ khác hai dòng"
def dongbo():
    while True:
        try:
            shutil.copy(LOG, DST)
            tl = f"{OUT}/trainer_log.jsonl"
            if os.path.exists(tl): shutil.copy(tl, DST)
        except Exception as e:
            open(f"{DST}/sync.err","a").write(f"{time.ctime()} {e}\n")
        time.sleep(300)
threading.Thread(target=dongbo, daemon=True).start()
print("đồng bộ mỗi 5 phút →", DST)
```

⚠️ Lỗi ghi vào `sync.err`, **không nuốt bằng `2>/dev/null`** — bản phiên 0 từng nuốt và không ai
biết đồng bộ đã chết.

⚠️ **Nhân Python restart làm rớt gắn Drive.** Thấy `FileNotFoundError` ở ô theo dõi trong khi tệp
vẫn nằm nguyên trên Drive thì chạy ô T9, **đừng chạy lại T5**.

---

## Ô T7 — THEO DÕI LIÊN TỤC, có thanh tiến độ

Bấm ⏹ để dừng **ô này**; train không chết theo.

```python
import json, os, time, glob, math, ast, re

os.environ["TZ"] = "Asia/Ho_Chi_Minh"; time.tzset()   # ⚠️ Colab chạy giờ UTC, lệch 7 tiếng

NHIP, NHIP_IM = 60, 300
LR0, WARM     = 2.0e-5, 0.05          # ⚠️ PHẢI khớp learning_rate trong cfg, xem (x3b)
# đo thật 24/8: MIN-DESC 20,6 s/bước · CE2-S2 16,0. Ngưỡng để rộng ~30%, cảnh báo chỉ nên
# kêu khi CHẬM THẬT chứ không phải khi chạm đúng số đo.
NGUONG_SB     = 27 if NHANH == "min_desc" else 21
SAVE_STEPS    = 100

# ⚠️⚠️ HAI NGUỒN, KHÔNG PHẢI MỘT — đo 23/8 trên stack transformers 5.8.0:
#   · trainer_log.jsonl CHỈ có: current_steps · total_steps · epoch · percentage ·
#     elapsed_time · remaining_time.  KHÔNG có loss, KHÔNG có lr, KHÔNG có rewards/*.
#     (Ghi chú cũ trong CLAUDE.md nói có `loss`/`lr` — đúng với stack tháng 8, SAI với bản này.
#      Lọc theo `loss` là vứt sạch mọi dòng rồi in "chưa có bước nào" suốt cả lượt train.)
#   · loss / lr / rewards/* chỉ có trong STDOUT, tức tệp LOG, mỗi logging_steps.
# Nên: tiến độ + tốc độ đọc từ jsonl · số học đọc từ LOG.

tl, t0 = f"{OUT}/trainer_log.jsonl", time.time()
truoc, lan_in = None, 0
gio = lambda: time.strftime("%H:%M:%S")
hms = lambda s: f"{int(max(s,0))//3600}h{(int(max(s,0))%3600)//60:02d}m"
so  = lambda x, n=4: "—" if x is None else f"{x:.{n}f}".replace(".", ",")
sod = lambda x, n=4: "—" if x is None else f"{x:+.{n}f}".replace(".", ",")
ng  = lambda n: f"{n:,}".replace(",", ".")
DICT = re.compile(r"\{'loss':.*?\}")

def thanh(p, w=28):
    k = int(round(p*w)); return "[" + "█"*k + "░"*(w-k) + f"] {100*p:5.1f}%"

def giay(t):
    try:
        if isinstance(t, (int, float)): return float(t)
        q = str(t).split(", ")[-1].split(":")
        return sum(float(v)*m for v, m in zip(reversed(q), (1, 60, 3600)))
    except Exception: return None

def _tia(h, khoa):
    """Vứt dòng của phiên đã chết: tệp ghi NỐI THÊM, nên sau khi chạy tiếp còn dòng cũ
    với số CAO HƠN chỗ đang chạy. Gặp giá trị tụt thì bỏ mọi dòng >= nó."""
    r = []
    for x in h:
        while r and r[-1][khoa] >= x[khoa]: r.pop()
        r.append(x)
    return r

def doc():
    """Tiến độ, từ trainer_log.jsonl."""
    h = []
    for l in open(tl, encoding="utf-8"):
        try: x = json.loads(l)
        except Exception: continue
        if x.get("current_steps") is None: continue
        h.append(x)
    return _tia(h, "current_steps")

def doc_log(lg):
    """Số học: loss · learning_rate · rewards/margins · rewards/accuracies · sft_loss.

    ⚠️ HAI NGUỒN, thử theo thứ tự. Đo 24/8 trên lượt thật:
      · STDOUT chỉ có dòng {'loss': …} khi chạy TƯƠNG TÁC (!llamafactory-cli). Ô T5 phóng
        bằng Popen(stdout=file) nên stdout KHÔNG phải terminal ⇒ tqdm tự tắt, mà HF chỉ in
        dict đó QUA tqdm ⇒ tệp .log KHÔNG có dòng nào. Smoke chạy tương tác nên có, và đó
        là lý do tôi lấy nhầm định dạng.
      · Nguồn thật lúc chạy nền: trainer_state.json TRONG CHECKPOINT MỚI NHẤT. Có đủ mọi
        trường, chỉ cập nhật mỗi save_steps (100 bước ≈ 35 phút) thay vì mỗi 20 bước.
    Lược đồ hai nguồn tương thích nhau: đều có epoch · loss · learning_rate · rewards/*."""
    h = []
    try:                                   # nguồn 1 — stdout, chỉ có khi chạy tương tác
        txt = open(lg, encoding="utf-8", errors="ignore").read()
        for m in DICT.findall(txt):
            try: d = ast.literal_eval(m)
            except Exception: continue
            e = {}
            for k, v in d.items():
                try: e[k] = float(v)
                except (TypeError, ValueError): e[k] = v
            if isinstance(e.get("epoch"), float): h.append(e)
    except Exception: pass
    if h: return _tia(h, "epoch")
    try:                                   # nguồn 2 — checkpoint mới nhất
        ck = sorted(glob.glob(f"{OUT}/checkpoint-*"), key=lambda q: int(q.rsplit("-",1)[1]))
        if not ck: return []
        st = json.load(open(f"{ck[-1]}/trainer_state.json", encoding="utf-8"))
        h = [l for l in st["log_history"] if l.get("loss") is not None]
    except Exception: return []
    return _tia(h, "epoch")

def toc_do(h, tran=None):
    """s/bước từ elapsed_time của TRAINER, không đụng đồng hồ tường."""
    i = len(h) - 1
    while i > 0:
        a, b = giay(h[i-1].get("elapsed_time")), giay(h[i].get("elapsed_time"))
        if a is None or b is None or a >= b: break
        if tran and h[-1]["current_steps"] - h[i-1]["current_steps"] > tran: break
        i -= 1
    db = h[-1]["current_steps"] - h[i]["current_steps"]
    dt = (giay(h[-1].get("elapsed_time")) or 0) - (giay(h[i].get("elapsed_time")) or 0)
    return (dt/db, db) if db > 0 and dt > 0 else (None, 0)

def lr_lich(b, tong):
    w, b = math.ceil(WARM*tong), b - 1
    if b <= w: return LR0 * b / max(w, 1)
    return LR0 * 0.5 * (1 + math.cos(math.pi * (b - w) / (tong - w)))

print(f"[{gio()}] theo dõi {NHANH}/{SEED} → {OUT}", flush=True)
print(f"          nhịp {NHIP}s · ⏹ để dừng ô này (train KHÔNG chết theo)", flush=True)

while True:
    try:
        # ⚠️ DÙNG BIẾN `LOG` của lượt NÀY, tuyệt đối không glob. Từ lượt thứ hai trở đi
        #    /content có nhiều train_*.log; sorted()[-1] chọn theo bảng chữ cái nên
        #    "min_desc" đứng sau "ce2_s2" ⇒ ô đọc nhầm log của lượt ĐÃ XONG, rồi in số học
        #    của lượt cũ kèm cảnh báo IM QUÁ LÂU và SAI LỊCH. Đã mắc thật 24/8.
        lg   = LOG
        tuoi = time.time() - os.path.getmtime(lg)
        with open(lg, "rb") as f:
            f.seek(max(0, os.path.getsize(lg)-4000)); duoi = f.read().decode("utf-8","ignore")

        h = doc() if os.path.exists(tl) else []
        if not h:
            print(f"[{gio()}] {thanh(0)} chưa có bước nào — mã hoá token "
                  f"({hms(time.time()-t0)} rồi, ~15–30 phút) · log {tuoi:.0f}s trước", flush=True)
            time.sleep(NHIP); continue

        x, b, tong = h[-1], h[-1]["current_steps"], h[-1]["total_steps"]
        m = doc_log(lg)                       # số học, có thể rỗng trong vài phút đầu
        tuoi_tl = time.time() - os.path.getmtime(tl)
        dung = tuoi_tl > 600                  # jsonl ghi mỗi logging_steps ≈ 7 phút
        canh = (b != truoc) or (time.time()-lan_in > NHIP_IM) \
               or (tuoi > 180 and time.time()-lan_in > 120)
        if canh:
            sb, n_b   = toc_do(h)
            sb_g, n_g = toc_do(h, 200)
            if b >= tong:
                # ⚠️ Ở 100% thì log IM là ĐÚNG — tiến trình đã kết thúc, không còn gì để ghi.
                #    Không có nhánh này thì ô in "nghi treo" mãi sau khi lượt đã xong sạch.
                toc = " · ✅ ĐÃ CHẠY HẾT 800 BƯỚC — chạy ô T8 để kiểm toàn vẹn"
            elif dung:
                ly_do = ("⏳ đang mã hoá token, số dưới là của phiên TRƯỚC"
                         if "Running tokenizer" in duoi or "Converting format" in duoi
                         else "⚠️ KHÔNG ghi bước nào — nghi treo, chạy ô T9")
                toc = f" · dòng cuối {tuoi_tl/60:.0f} phút trước · {ly_do}"
            elif sb:
                cb = " ⚠️ CHẬM BẤT THƯỜNG" if sb_g and sb_g > NGUONG_SB else ""
                if sb_g and sb and sb_g > sb*1.15: cb += " ⚠️ đang chậm dần"
                toc = (f" · {so(sb,2)} s/bước (gần đây {so(sb_g,2)}){cb or ' ✅'}"
                       f" · còn {hms((tong-b)*sb)} → xong ~"
                       f"{time.strftime('%H:%M %d/%m', time.localtime(time.time()+(tong-b)*sb))}")
            else:
                toc = " · chưa đủ hai mốc để tính tốc độ"

            ck  = sorted(glob.glob(f"{OUT}/checkpoint-*"), key=lambda q: int(q.rsplit("-",1)[1]))
            sck = "chưa có"
            if ck:
                tck = (time.time()-os.path.getmtime(ck[-1]))/60
                han = SAVE_STEPS*(sb or 21)/60*1.5
                sck = f"{os.path.basename(ck[-1])} ({tck:.0f}′ trước {'✅' if tck < han else '⚠️'})"

            # ── dòng số học, từ STDOUT ────────────────────────────────────────
            if m:
                y = m[-1]
                tb = lambda a, z: (sum(r["loss"] for r in m[a:z])/5) if len(m[a:z]) == 5 else None
                tb5, tb_gan = tb(-5, None), tb(-10, -5)
                # ⚠️ Số học có thể đến từ checkpoint (viết mỗi save_steps) nên nó thuộc về
                #    bước CŨ hơn bước đang chạy. Phải so lr với lịch TẠI BƯỚC ẤY, không phải
                #    tại bước hiện tại — nếu không, % lệch cứ phình lên và báo SAI LỊCH oan.
                bm = y.get("step") or b
                if bm > b:      # số học thuộc bước lớn hơn bước đang chạy ⇒ của lượt KHÁC
                    m, y, bm = [], {}, b
                lr, lk = y.get("learning_rate"), lr_lich(bm, tong)
                dl  = abs(lr-lk)/lk*100 if isinstance(lr, float) and lk else None
                slr = (f"{lr:.3e} lệch {so(dl,2)}% {'✅' if dl < 1 else '⚠️ SAI LỊCH'}"
                       ) if dl is not None else "—"
                tre = f" ⏳ chậm {b-bm} bước, bản sau ở {(bm//SAVE_STEPS+1)*SAVE_STEPS}" if bm < b else ""
                d2 = (f"\n          số học @bước {ng(bm)}{tre}"
                      f"\n          loss {so(y.get('loss'))} · tb5 {so(tb5)}"
                      f" (so 100 bước {sod(tb5-tb_gan) if tb5 and tb_gan else '—'}) · lr {slr}")
                ac, mg = y.get("rewards/accuracies"), y.get("rewards/margins")
                if isinstance(mg, float):          # nhánh MIN-DESC (stage dpo)
                    d3 = ("\n          ƯU TIÊN: "
                          + f"margin {sod(mg,4)} {'✅' if mg > 0 else '⚠️ ÂM'}"
                          + f" · acc {so(ac,3)} {'⚠️ HỎNG' if isinstance(ac,float) and ac < 0.8 else '·'}"
                          + f" · sft {so(y.get('sft_loss'),3)} · odds {so(y.get('odds_ratio_loss'),3)}")
                else:                              # nhánh CE2-S2 (stage sft) — KHÔNG có rewards/*
                    d3 = "\n          (CE2-S2 là SFT thuần — không có metric ưu tiên, đúng như thiết kế)"
            else:
                d2, d3 = "", ("\n          (chưa có số học — chờ checkpoint đầu tiên ở bước "
                              f"{SAVE_STEPS}, ~{SAVE_STEPS*(sb or 21)/60:.0f} phút sau bước 1)")

            print(f"[{gio()}] {thanh(b/tong)} bước {ng(b)}/{ng(tong)}{toc}{d2}\n"
                  f"          lưu {sck} · log {tuoi:.0f}s trước"
                  f" {'✅' if tuoi < 180 else '⚠️ IM QUÁ LÂU'}{d3}", flush=True)
            lan_in = time.time()
        truoc = b
    except Exception as e:
        print(f"[{gio()}] ⚠️ {type(e).__name__}: {e}", flush=True)
    time.sleep(NHIP)
```

### Đọc số nào — tốt hay xấu

| con số | tốt | xấu | ghi chú |
|---|---|---|---|
| **thanh tiến độ + s/bước** | MIN-DESC ~25–33 · CE2 ~13–16 | vọt >40 (MIN) / >22 (CE2) | Sửa `NGUONG_SB` cho khớp số **smoke đã đo**, đừng để số ước |
| **acc** (`rewards/accuracies`) | ~0,95 **ngay từ đầu** | < 0,8 | ⚠️ **KHÔNG phải tín hiệu tiến bộ.** Đo 23/8 trên smoke: acc đã **0,94–0,97 từ bước đầu tiên**, vì `chosen` chính là thứ S2 đã được dạy sinh ra suốt 2 epoch — nó thắng `rejected` một cách tất yếu. Chỉ dùng để phát hiện **hỏng** (tụt dưới 0,8), không dùng để nói "đang học tốt" |
| ⭐ **margin** (`rewards/margins`) | **tăng đều** so với mốc đầu ~**0,019** | phẳng hoặc **âm** | **Đây mới là tín hiệu tiến bộ thật.** Nó đo model tách hai vế ra bao xa, chứ không phải có tách được không. Âm kéo dài > 200 bước ⇒ dừng, báo lại |
| **loss** (một lô) | nhảy ±0,1 là bình thường | — | ⛔ **Đừng quyết định gì dựa trên dòng này** |
| **tb5** (5 điểm cuối = 100 bước) | giảm hoặc phẳng | tăng đều 3–4 nấc | Đường thật, hẹp hơn loss ~2,2 lần |
| **dòng ƯU TIÊN vắng ở CE2-S2** | đúng như thiết kế | — | CE2 là stage `sft`, không có `rewards/*`. Chỉ MIN-DESC mới có |
| **lr** | lệch lịch cosine **< 1%** | lệch lớn | Lệch lớn ⇒ cfg bị đổi hoặc đang chạy lịch của lượt khác |
| **lưu** | bản mới **< ~70 phút** | cũ hơn | `save_steps: 100` × ~28 s ≈ 47 phút. **Bằng chứng máy còn sống mạnh nhất** — xem được từ Drive trên điện thoại |
| **log … giây trước** | < 180 s | > 180 s | Chữ `disconnect` trên trình duyệt **không** phải bằng chứng máy chết; dòng này mới là |

**Bốn cách đọc sai — đừng mắc lại:**

- ⛔ **ĐỪNG so loss của MIN-DESC với loss của CE2.** Hai stage tính hàm mất mát khác nhau (ORPO =
  SFT + số hạng odds-ratio), nên loss **không so được**. Câu trả lời chỉ đến từ **executability
  chấm trên câu sau khi cắt `<desc>`**, ngưỡng đã khoá ở (x5).
- ⛔ **Đừng ngoại suy loss.** Dự báo sàn 0,548 hồi 12/8 đã bị rút vì đúng chuyện này.
- ⛔ **Đừng đọc `remaining_time`/`elapsed_time` của trainer** — cả hai **hỏng sau khi chạy tiếp**
  (đếm từ lúc phiên này khởi động). Ô trên tự tính bằng mốc neo.
- **Số bước TỤT XUỐNG là dấu hiệu TỐT** — nghĩa là phiên mới đã ghi thật. Không phải lỗi.
- ⚠️ **Không có ranh giới epoch** ở lượt này: 800 update = **0,56 epoch**. Thấy loss tụt một nấc
  thì đó **không** phải "gặp lại dữ liệu lần hai".

---

## Ô T8 — xong lượt: kiểm toàn vẹn + **cổng cơ học**

```python
import json, os, glob
st = json.load(open(f"{OUT}/trainer_state.json", encoding="utf-8"))
print("global_step:", st["global_step"], "← phải là 800")
print("total_flos :", st.get("total_flos"))
ck = sorted(glob.glob(f"{OUT}/checkpoint-*"), key=lambda q: int(q.rsplit("-",1)[1]))
for d in ck[-2:]:
    ad = [f for f in os.listdir(d) if "adapter_model" in f]
    print(" ", os.path.basename(d), ad, [round(os.path.getsize(f"{d}/{f}")/2**20,1) for f in ad],
          "MB · optimizer:", any("optimizer" in f for f in os.listdir(d)))
h = [json.loads(l) for l in open(f"{OUT}/trainer_log.jsonl", encoding="utf-8")]
h = [r for r in h if r.get("loss") is not None]
print("\n5 dòng log cuối:")
for r in h[-5:]:
    print("  ", {k: v for k, v in r.items() if k not in ("elapsed_time","remaining_time","percentage")})
```

⛔ **Ba số trong `all_results.json` SAI sau khi chạy tiếp, cấm trích:** `train_loss`,
`train_runtime`, `*_per_second`. `total_flos` **không** hỏng. Dùng `trainer_state.json`.

⭐ **Phép kiểm rẻ "điểm lưu có trọn không":** ghi dở thì bản **CUỐI phải NHỎ HƠN** bản trước.
Dòng in kích thước MB ở trên là để so đúng chuyện đó.

### Cổng cơ học sau lượt 1 + 2 — quyết có chạy hạt giống 202 hay không

Chạy **sau khi có cả `min_desc_seed101` lẫn `ce2_s2_seed101`**:

| kiểm | ĐẠT | TRƯỢT ⇒ dừng, không chạy 202 |
|---|---|---|
| `global_step` cả hai | **800** | khác |
| `acc` cuối của MIN-DESC | ~0,95 (bình thường) | **< 0,8** ⇒ hỏng |
| `margin` cuối | **lớn hơn mốc đầu ~0,019** | phẳng hoặc âm |
| ⭐ **`gate_desc_acc.py`** — xem dưới | **Δ dương** so với mốc S2 **53,9%** | Δ âm ⇒ train làm hỏng nhận diện |

**Cổng chính là `gate_desc_acc.py`** — nó đo thẳng thứ MIN-DESC được thiết kế để sửa, và
**không gọi bộ trỏ** nên (x6) cho phép. Sinh câu trên một lát tập kiểm bằng checkpoint mới rồi:

```python
# sinh preds bằng checkpoint MIN-DESC (một lát 600 bước là đủ cho cổng, ~10 phút)
!cd {REPO} && python harness/infer_branch.py --adapter {D}/ckpt/min_desc_seed101 \
    --out /content/preds_min_desc_101.jsonl --limit 600
# ⚠️ `runs/` KHÔNG nằm trong thesis_rented.zip (make_bundle chỉ đóng harness/ + 4 report),
#    nên mốc S2 phải upload riêng lên Drive: MyDrive/thesis/preds_s2_seed101.jsonl (2,7 MB).
!cd {REPO} && python harness/gate_desc_acc.py \
    {D}/preds_s2_seed101.jsonl /content/preds_ce2_s2_101.jsonl /content/preds_min_desc_101.jsonl
```

Ba cờ trên đã đối chiếu với mã (`infer_branch.py:349-352`): `--adapter` · `--out` · `--limit`.
Mặc định `--batch 8`, `--max-new 96`. ⚠️ Ô này cần **ảnh tập kiểm** — nếu máy ảo chưa bung thì
chạy `!tar xf {D}/test_images.tar -C {REPO}/harness/dg1_cache/test_ac` trước (3,2 GB, ~3 phút).

Mốc S2/101 đã đo 23/8 (`report/106` mục x3b), trên 3.473 bước có tên vàng:
`sinh <desc> 93,4% · tên đúng 59,2% · point đúng 66,9% · **cả hai đúng 53,9%**`.

⛔ **Cổng này KHÔNG được gọi UGround hay UI-Venus** — (x6). Chấm 4.463 chỉ làm **một lần**, sau
khi cả bốn checkpoint đã đóng băng.

---

## Ô T9 — chẩn đoán khi nghi treo

```python
import os, subprocess, time, glob
lg = sorted(glob.glob("/content/train_*.log"))[-1]
print("kích thước log:", os.path.getsize(lg), "byte ·",
      f"{time.time()-os.path.getmtime(lg):.0f} giây trước")
print(subprocess.run(["ps","-eo","pid,etime,args"], capture_output=True, text=True).stdout
      .split("llamafactory")[0][-300:] if True else "")
!ps -eo pid,etime,%cpu,%mem,args | grep -i llamafactory | grep -v grep
!nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv
!tail -25 {lg}
```

**Hỏi ba thứ trước khi `pkill`:** kích thước log có tăng không · tiến trình còn trong `ps` không ·
`tail` đang in gì. `grep "Resuming training from"` trống ngay sau T5 là **báo động giả** — dòng đó
in sau ~40 giây nạp thư viện.

---

## Nếu phiên đứt giữa chừng

1. Máy ảo mới ⇒ chạy lại **T1 → Restart → T2 → T3 → T4 → T5 → T6 → T7**.
   ⚠️ **T3 BẮT BUỘC, đừng bỏ.** `min_desc.json`, `ce2_s2.json` và `dataset_info.json` do T3 ghi
   vào `/content/ws/thesis/...` — **đĩa máy ảo**, không phải Drive. Máy chết là mất sạch, phải
   dựng lại. (Bỏ T3 thì T4 dừng ở dòng ⑤ với thông báo thiếu khoá dataset — có chốt chặn, nhưng
   đừng để nó phải bắt.)
2. Ở **T4**, dòng ④ *"bên trong"* sẽ có `checkpoint-*` — **ĐÚNG, đừng xoá**. LLaMA-Factory tự chạy
   tiếp từ đó. `resume_from_checkpoint` **cố ý không khai**: nó chỉ tự dò khi trường đó còn trống;
   điền bất cứ gì, kể cả `"auto"`, là tắt đúng cái nó định bật.
3. Giá một lần đứt, tính theo tốc độ **đo thật 24/8**: bước đã train mất tối đa một khoảng
   `save_steps` — MIN-DESC 100 × 20,6 s ≈ **34 phút**, CE2-S2 100 × 16,0 s ≈ **27 phút**. Cộng
   ~25–35 phút dựng lại máy (phần lớn là bung 31 GB ảnh dạy) + **~15–30 phút mã hoá lại token**.
   Tổng ~**1–1,5 giờ**, **không phải cả lượt**. Phần đắt nhất là mã hoá token, không phải khâu
   nhảy qua lô (1.600 lô ≈ 17 giây).
4. `MOC` phải lấy theo **dòng log cuối**, không theo số điểm lưu — `logging_steps: 20` mà
   `save_steps: 100` ⇒ log chạy trước điểm lưu tới **80 bước**.

---

## Ô T10 — "CE2 đâu rồi?" · lượt suy luận đang chạy THẬT SỰ nạp adapter nào

Dùng khi `{D}/ckpt` không thấy `ce2_s2_seed101`, hoặc nghi lượt suy luận đang chạy nhầm nhánh.
Nguyên tắc: **đọc thứ tiến trình ĐANG GHI RA, đừng đọc lệnh đã gõ** (bài học 20/8).

```python
import os, glob, json, subprocess, time
D = "/content/drive/MyDrive/thesis"

print("① TỆP PREDS ĐANG GHI DẦN — trường 'run' là chữ ký adapter thật sự nạp")
for p in sorted(glob.glob("/content/**/preds_*.jsonl", recursive=True)
                + glob.glob(f"{D}/preds_*.jsonl")):
    try:
        n  = sum(1 for _ in open(p, encoding="utf-8"))
        r  = json.loads(open(p, encoding="utf-8").readline())["run"] if n else "(rỗng)"
    except Exception as e:
        n, r = "?", f"lỗi đọc: {e}"
    print(f"   {n:>5} dòng · run={r:<24} · sửa {time.time()-os.path.getmtime(p):,.0f}s trước · {p}")

print("\n② LỆNH ĐANG CHẠY")
print(subprocess.run(["bash","-lc",
      "ps -eo pid,etime,args | grep -E 'infer_branch|llamafactory' | grep -v grep"],
      capture_output=True, text=True).stdout or "   (không có tiến trình nào)")

print("③ MỌI ADAPTER CÓ TRÊN MÁY (adapter_config.json), cả Drive lẫn đĩa máy ảo")
for g in ("/content", D):
    for f in glob.glob(f"{g}/**/adapter_config.json", recursive=True):
        d = os.path.dirname(f)
        mb = sum(os.path.getsize(os.path.join(d,x)) for x in os.listdir(d)
                 if os.path.isfile(os.path.join(d,x))) / 1e6
        tren_drive = d.startswith(D)
        print(f"   {'DRIVE ' if tren_drive else 'MÁY ẢO'} {mb:8.1f} MB  {d}")
```

**Đọc kết quả:**

| thấy gì ở ① | nghĩa là | làm gì |
|---|---|---|
| `run=lora:ce2_s2_seed101` | đúng nhánh, checkpoint **có thật** — chỉ là không nằm chỗ đang tìm | xem ③: nếu nó ở **MÁY ẢO** thì copy sang Drive **ngay**, xem ô dưới |
| `run=lora:min_desc_seed101` | đang chấm lại nhánh đã có preds ⇒ **phí trọn lượt** | dừng, sửa `--adapter`, chạy lại |
| `run=base` | `--no-adapter` lọt vào lệnh | dừng ngay |

⚠️ Adapter chỉ nằm trên **đĩa máy ảo** thì mất máy = mất trọn lượt train (CE2-S2 ~3 h). Copy sang
Drive **song song** với lượt suy luận đang chạy, không cần dừng nó:

```python
!mkdir -p {D}/ckpt/ce2_s2_seed101 && rsync -a --info=progress2 \
    <ĐƯỜNG_DẪN_MÁY_ẢO>/ {D}/ckpt/ce2_s2_seed101/
!ls -la {D}/ckpt/ce2_s2_seed101      # kiểm: có adapter_model.safetensors + adapter_config.json
```

---

## Ô T11 — lượt suy luận đang chạy mà Drive chưa có gì · chống mất máy

Tình huống: `infer_branch.py` đang chạy (6.958 bước, ~2 h), Drive trống trơn. Hai thứ đang phơi
nhiễm, **giá khác nhau một trời một vực**:

| thứ | mất thì tốn gì | ưu tiên |
|---|---|---|
| **adapter** `ce2_s2_seed101` | **~3 h train** + lượt suy luận **không nối tiếp lại được** | ① làm ngay |
| **tệp preds đang ghi dần** | chỉ phần đã sinh (≤2 h), nối tiếp được nếu tệp còn | ② làm sau |

**① Cứu adapter — chạy ngay, không cần dừng lượt suy luận** (đường dẫn thật lấy từ ô T10 mục ③):

```python
D = "/content/drive/MyDrive/thesis"
!mkdir -p {D}/ckpt/ce2_s2_seed101 && rsync -a <ĐƯỜNG_DẪN_MÁY_ẢO>/ {D}/ckpt/ce2_s2_seed101/
!ls -la {D}/ckpt/ce2_s2_seed101      # phải có adapter_model.safetensors + adapter_config.json
```

**② Đồng bộ tệp preds mỗi 5 phút, chạy nền, không chặn ô nào:**

```python
import subprocess, os
D   = "/content/drive/MyDrive/thesis"
OUT = "/content/preds_ce2_s2_seed101.jsonl"      # ⚠️ sửa cho khớp --out ĐANG dùng (ô T10 mục ②)
os.makedirs(f"{D}/preds_dang_chay", exist_ok=True)
subprocess.Popen(["bash","-lc",
    f'while true; do cp -f "{OUT}" "{D}/preds_dang_chay/" 2>/dev/null; sleep 300; done'])
print("đã bật đồng bộ 5 phút/lần →", f"{D}/preds_dang_chay/")
```

**Vì sao chép giữa lúc đang ghi vẫn an toàn:** `infer_branch.py` mở tệp ở chế độ `"a"` và
`out.flush()` **sau mỗi lô** (`infer_branch.py:503`) ⇒ mất nhiều nhất một lô 8 bước. Bản chép có
thể đứt giữa dòng cuối, nhưng lúc nối tiếp thì khối `try/except json.loads` (`:419-424`) **loại
hẳn dòng hỏng rồi ghi lại tệp sạch** — đúng ca này đã được tính từ 11/8.

**③ Nối tiếp sau khi dựng máy ảo mới:** chép cả hai về rồi gõ lại **y nguyên** dòng lệnh cũ.

```python
!mkdir -p /content && cp {D}/preds_dang_chay/preds_ce2_s2_seed101.jsonl /content/
!cd {REPO} && python harness/infer_branch.py --adapter {D}/ckpt/ce2_s2_seed101 \
    --out /content/preds_ce2_s2_seed101.jsonl
```

Dấu hiệu nối tiếp **đúng** — hai dòng phải thấy, thiếu một là sai:

```
Nối tiếp: đã có 2320 bước, còn 4638
Nạp Qwen/Qwen2.5-VL-3B-Instruct + LoRA /content/drive/MyDrive/thesis/ckpt/ce2_s2_seed101
```

⛔ Thấy `Xong sẵn 6958 bước` trong hai giây = **báo động thật, không phải mừng**: tệp `--out`
đang là của lượt khác. `infer_branch.py:429` có chốt so chữ ký `run` và sẽ `sys.exit` — nếu nó
không kêu mà vẫn in `Xong sẵn` thì kiểm lại trường `run` bằng ô T10.

⚠️ **`--out` trỏ thẳng vào Drive thì vẫn CHƯA đủ an toàn** — xem ô **T13**. Tệp hiện ngay trong
`/content/drive` nhưng đó là **bộ đệm cục bộ** của FUSE; tệp mở chế độ `"a"` và bị ghi thêm liên
tục có thể chưa đẩy xong lên cloud. Cách chắc chắn là **chụp ảnh định kỳ sang một tên khác**:
`cp` tạo tệp mới rồi đóng lại, mà đóng tệp mới là thứ buộc Drive tải lên trọn vẹn.

---

## Ô T12 — BACKUP BẰNG TERMINAL COLAB (khi nhân Python đang bận chạy suy luận)

⚠️ **Vì sao phải là Terminal, không phải ô notebook:** lượt suy luận đang chiếm **nhân Python**.
Cell nào cũng phải xếp hàng sau nó ⇒ ô T10 và T11 **không chạy được** cho tới khi lượt kia xong.
Terminal Colab (icon `>_` góc dưới trái, có ở tài khoản trả phí) là **tiến trình riêng, cùng máy
ảo, cùng thấy `/content/drive`** — nên copy được ngay mà không đụng vào lượt đang chạy.

### Bước 1 — hỏi tiến trình nó THẬT SỰ đang dùng đường dẫn nào

```bash
PID=$(pgrep -f infer_branch | head -1); echo "PID=$PID"
tr '\0' ' ' < /proc/$PID/cmdline; echo
```

Dòng thứ hai in ra **nguyên văn** `--adapter …` và `--out …`. Đây là bằng chứng duy nhất đọc được
lúc nhân đang bận — hơn hẳn việc nhớ lại lệnh đã gõ (bài học 20/8).

### Bước 2 — xem cái gì nằm ngoài Drive (tức là sẽ chết theo máy ảo)

```bash
ls -la /content/*.jsonl 2>/dev/null
find /content -maxdepth 5 -name adapter_config.json -not -path "/content/drive/*"
ls -la /content/drive/MyDrive/thesis/ckpt/
```

### Bước 3 — copy sang Drive

```bash
D=/content/drive/MyDrive/thesis
mkdir -p "$D/ckpt/ce2_s2_seed101" "$D/preds_dang_chay"
rsync -a <THƯ_MỤC_ADAPTER_Ở_BƯỚC_2>/ "$D/ckpt/ce2_s2_seed101/"     # ① đắt nhất, làm trước
cp -f <TỆP_OUT_Ở_BƯỚC_1> "$D/preds_dang_chay/"                     # ② rẻ hơn
```

### Bước 4 — đồng bộ định kỳ, sống tiếp sau khi đóng tab Terminal

```bash
nohup bash -c 'while true; do
  cp -f /content/preds_*.jsonl /content/drive/MyDrive/thesis/preds_dang_chay/ 2>/dev/null
  sleep 300
done' >/tmp/sync.log 2>&1 &
echo "đã bật, PID=$!"
```

### Bước 5 — KIỂM bản chép đã thật sự lên Drive

```bash
D=/content/drive/MyDrive/thesis
ls -la "$D/ckpt/ce2_s2_seed101/" "$D/preds_dang_chay/"
wc -l "$D/preds_dang_chay/"*.jsonl /content/preds_*.jsonl
md5sum "$D/ckpt/ce2_s2_seed101/adapter_model.safetensors" <THƯ_MỤC_ADAPTER>/adapter_model.safetensors
```

`md5sum` hai bên **phải trùng**. `wc -l` bên Drive ít hơn vài dòng là **bình thường** — bản chép
lấy ở thời điểm sớm hơn. Lệch hàng nghìn dòng, hoặc `ls` không thấy tệp, là chép **hỏng**: FUSE
của Drive nuốt lỗi im lặng khi hết dung lượng hoặc mất kết nối, `cp` vẫn trả về 0.

⚠️ Tệp hiện trên `/content/drive` **chưa chắc đã lên xong cloud**. Với adapter vài trăm MB, đợi
`ls -la` cho kích thước đứng yên, hoặc mở Google Drive trên điện thoại xem tệp đã hiện chưa —
đúng mẹo đã dùng ở bẫy ③ khi theo dõi lượt train.

---

## Ô T13 — TRƯỜNG HỢP THẬT 24/8: cả `--adapter` lẫn `--out` đều đã trỏ vào Drive

Lệnh đang chạy:

```bash
python harness/infer_branch.py --adapter {D}/ckpt/ce2_s2_seed101 \
    --out {D}/preds_ce2_s2_seed101.jsonl
```

⇒ **Adapter CE2 CÓ trên Drive.** `PeftModel.from_pretrained` (`infer_branch.py:446`) sẽ ném lỗi
ngay nếu thiếu `adapter_config.json`; lượt này đã chạy qua 2.300 bước ⇒ nó đọc được thư mục đó.
Không thấy trong giao diện Drive là **độ trễ hiển thị của Drive**, không phải mất tệp. Việc "cứu
adapter" ở ô T11/T12 bước ③ ① **không cần làm nữa**.

⇒ Còn đúng **một** lỗ: tệp preds mở chế độ `"a"`, được ghi thêm mỗi lô suốt 2 h mà **chưa đóng
lần nào**. Nó nằm trong bộ đệm FUSE; phần đã đẩy lên cloud tới đâu thì không có gì bảo đảm.

### Dán vào Terminal Colab — bốn lệnh, theo đúng thứ tự

**① Xác nhận tiến trình đang dùng đúng hai đường dẫn đó** (đọc từ tiến trình, không từ trí nhớ):

```bash
tr '\0' ' ' < /proc/$(pgrep -f infer_branch | head -1)/cmdline; echo
```

**② Xem tệp đang lớn tới đâu:**

```bash
D=/content/drive/MyDrive/thesis
ls -la "$D/preds_ce2_s2_seed101.jsonl"; wc -l "$D/preds_ce2_s2_seed101.jsonl"
```

**③ Bật chụp ảnh 5 phút/lần sang tên khác** — đây là thứ thật sự buộc Drive tải lên trọn vẹn:

```bash
mkdir -p /content/drive/MyDrive/thesis/preds_dang_chay
nohup bash -c 'D=/content/drive/MyDrive/thesis
S="$D/preds_dang_chay/preds_ce2_s2_seed101.snap.jsonl"
while true; do
  cp -f "$D/preds_ce2_s2_seed101.jsonl" "$S" 2>/dev/null
  echo "$(date +%H:%M:%S)  $(wc -l < "$S" 2>/dev/null) dòng"
  sleep 300
done' >> /content/snap.log 2>&1 &
echo "PID=$!"
```

**④ Theo dõi nó thật sự chạy** (bỏ qua bước này là quay lại đúng lỗi câm 20/8):

```bash
sleep 20; cat /content/snap.log
```

Phải thấy dòng có giờ và **số dòng tăng dần** sau mỗi 5 phút. Log trống, hoặc số dòng đứng yên
hai lượt liên tiếp trong khi ô suy luận vẫn đang in tiến độ, là chụp ảnh **hỏng** — kiểm dung
lượng Drive (`df -h /content/drive`).

### Mất máy rồi, chạy tiếp thế nào

Gõ lại **y nguyên** lệnh cũ. Nhưng **so số dòng trước, giữ bản DÀI HƠN**:

```bash
D=/content/drive/MyDrive/thesis
wc -l "$D/preds_ce2_s2_seed101.jsonl" "$D/preds_dang_chay/preds_ce2_s2_seed101.snap.jsonl"
# bản chính ngắn hơn / mất hẳn  →  mới phục hồi từ bản chụp:
cp "$D/preds_dang_chay/preds_ce2_s2_seed101.snap.jsonl" "$D/preds_ce2_s2_seed101.jsonl"
```

⛔ **Đừng chép đè bản chụp lên bản chính khi bản chính đang dài hơn** — bản chụp luôn cũ hơn tối
đa 5 phút, làm vậy là tự vứt ~270 bước đã sinh.

Rồi chạy lại lệnh cũ, phải thấy **hai dòng** này:

```
Nối tiếp: đã có <N> bước, còn <6958-N>
Nạp Qwen/Qwen2.5-VL-3B-Instruct + LoRA /content/drive/MyDrive/thesis/ckpt/ce2_s2_seed101
```

Dòng đứt giữa chừng lúc mất máy **không phải lo**: `try/except json.loads` ở `:419-424` loại hẳn
dòng hỏng rồi ghi lại tệp sạch trước khi sinh tiếp.

---

## Ô T14 — MẤT MÁY GIỮA LƯỢT SUY LUẬN: dựng lại để CHẠY TIẾP (không train, nhẹ hơn T1–T3 nhiều)

Chạy tiếp suy luận **không cần** LLaMA-Factory, không cần liger, không cần 31 GB ảnh dạy.
Chỉ cần: thư viện suy luận · kho mã · **ảnh tập kiểm** · adapter (đã có sẵn trên Drive).
Tổng ~10–15 phút, phần lâu nhất là bung 3,2 GB ảnh kiểm.

### R1 — thư viện  ▸ rồi **Restart runtime**

```python
import subprocess
r = subprocess.run("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader",
                   shell=True, capture_output=True, text=True)
print("GPU:", r.stdout.strip() or "⛔ KHÔNG THẤY")
assert r.returncode == 0 and r.stdout.strip(), "⛔ DỪNG — máy ảo KHÔNG có GPU. Đổi runtime rồi làm lại R1."

!pip install -q -U "transformers>=4.49" accelerate peft pillow pyyaml huggingface_hub
# ⛔ BẮT BUỘC — đã nổ thật 24/8. Máy ảo Colab cài sẵn torchao 0.10.0; `peft` bản mới nhất
#    `raise ImportError` ngay khi thấy torchao < 0.16 (`peft/import_utils.py:147`), chết ở
#    ĐÚNG dòng `PeftModel.from_pretrained` — tức SAU khi đã tải 7,5 GB trọng số. Gỡ hẳn thì
#    `is_torchao_available()` trả False và bộ điều phối bỏ qua nhánh đó. Không có gì ở đây
#    dùng torchao (suy luận chạy bf16/fp16 thuần, không lượng tử hoá).
#    ⚠️ Lượt trước KHÔNG dính vì ô T1 cài LLaMA-Factory, gói đó ghim peft bản cũ hơn.
!pip uninstall -y -q torchao
import torch
print("torch:", torch.__version__, "| CUDA build:", torch.version.cuda)
assert torch.version.cuda, (
    "⛔ pip vừa đè torch bản CPU-only. Sửa:\n"
    "   !pip install -q -U torch --index-url https://download.pytorch.org/whl/cu124\n"
    "   rồi Restart runtime và chạy lại R1.")
```

⚠️ **Ghi lại tên card.** Nếu khác card của nửa lượt trước thì `pick_dtype()`
(`infer_branch.py:49`) có thể đổi bf16 ↔ fp16 **giữa chừng một tệp preds** — nửa đầu sinh bằng
kiểu số này, nửa sau kiểu số kia. Không làm hỏng lượt, nhưng là **một lệch chuẩn phải khai** vào
mục sửa đổi của `report/106`. Xin lại **đúng loại card cũ** nếu chọn được.

⚠️ **Restart runtime**, rồi mới chạy R2.

### R2 — Drive, kho mã, ảnh tập kiểm

```python
from google.colab import drive; drive.mount('/content/drive')
import os, zipfile
D, WS = "/content/drive/MyDrive/thesis", "/content/ws"
os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_rented.zip").extractall(WS)
REPO = f"{WS}/thesis"; os.chdir(REPO)
TE = f"{REPO}/harness/dg1_cache/test_ac"

!tar xf {D}/test_images.tar -C {TE}          # 3,2 GB, ~3 phút

dem = lambda d: len(os.listdir(d)) if os.path.isdir(d) else 0
print("bước kiểm :", sum(1 for _ in open(f"{TE}/test.jsonl")), "← cần 6.958")
print("ocr       :", os.path.exists(f"{TE}/ocr.jsonl"), "← phải True, thiếu là câu nhắc KHÁC lúc dạy")
print("ảnh kiểm  :", dem(f"{TE}/images"))
print("adapter   :", os.path.isdir(f"{D}/ckpt/ce2_s2_seed101"),
      sorted(os.listdir(f"{D}/ckpt/ce2_s2_seed101"))[:6]
      if os.path.isdir(f"{D}/ckpt/ce2_s2_seed101") else "⛔ KHÔNG THẤY")
```

⛔ `ocr` ra `False` thì **dừng** — `infer_branch.py:392` chỉ in CẢNH BÁO rồi chạy tiếp với câu
nhắc thiếu phần chữ đọc được, tức nửa sau của tệp preds sinh bằng đầu vào **khác** nửa đầu.
Đây là lỗi câm đúng kiểu 20/8: không lỗi, không dừng, chỉ ra số khác.

### R3 — chọn bản preds DÀI HƠN rồi mới chạy tiếp

```python
import os
for p in (f"{D}/preds_ce2_s2_seed101.jsonl",
          f"{D}/preds_dang_chay/preds_ce2_s2_seed101.snap.jsonl"):
    print(sum(1 for _ in open(p, encoding="utf-8")) if os.path.exists(p) else "(không có)", p)
```

Bản chính **dài hơn hoặc bằng** ⇒ không đụng gì. Bản chính ngắn hơn / mất ⇒ mới chép đè:

```python
!cp {D}/preds_dang_chay/preds_ce2_s2_seed101.snap.jsonl {D}/preds_ce2_s2_seed101.jsonl
```

⛔ Bản chụp luôn cũ hơn tối đa 5 phút. Chép đè theo phản xạ lúc bản chính đang dài hơn là tự vứt
~270 bước đã sinh.

### R4 — chạy tiếp, **y nguyên** lệnh cũ

```python
!cd {REPO} && python3 harness/infer_branch.py \
    --adapter {D}/ckpt/ce2_s2_seed101 \
    --out {D}/preds_ce2_s2_seed101.jsonl
```

Hai dòng đầu **phải** thấy, thiếu một là sai:

```
Nối tiếp: đã có <N> bước, còn <6958-N>
Nạp Qwen/Qwen2.5-VL-3B-Instruct + LoRA /content/drive/MyDrive/thesis/ckpt/ce2_s2_seed101
```

· `Nối tiếp` **vắng** ⇒ nó không thấy tệp cũ, đang sinh lại từ số 0. Dừng, kiểm lại `--out`.
· `Xong sẵn 6958 bước` trong hai giây ⇒ tệp `--out` là của lượt khác (`:429` so chữ ký `run`).
· Thanh tiến độ in `/<6958-N>`, **không** phải `/6958` — đó là dấu hiệu nối tiếp đã ăn.

### R5 — bật lại vòng chụp ảnh (nó chết theo máy ảo cũ)

Mở **Terminal**, dán lại nguyên khối ở **ô T13 bước ③**, rồi `cat /content/snap.log` kiểm có dòng.
