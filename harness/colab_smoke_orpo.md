# SMOKE ORPO — cổng kỹ thuật của MIN-DESC, dán thẳng theo thứ tự

**Mục đích:** biết ORPO đa phương thức có chạy được trên LLaMA-Factory + Qwen2.5-VL-3B QLoRA
**trước khi** tiêu 20 giờ A100. Toàn bộ file này **~1 giờ GPU, ~5 đơn vị**.

Quyết định và lý do: `report/117`. Hồ sơ đăng ký trước: `report/106` mục **(x)**.
Cổng STOP của smoke nằm ở (x6) — **đã khoá trước, không nới sau khi thấy số**.

> ⛔ **Ba luật của file này**, mỗi luật là một lần đã trả giá ở dự án này:
> 1. **Không `>/dev/null 2>&1`** trên bất kỳ lệnh nào. Lỗi `command not found` bị nuốt từng làm
>    cả một ngày báo nhầm kết quả.
> 2. **Bắt tiến trình IN RA cấu hình nó thật sự đang dùng**, rồi kiểm dòng đó — đừng kiểm mã
>    nguồn. Ngày 20/8 hai phép thử **chưa hề diễn ra** mà báo như đã diễn ra.
> 3. **Kết quả trùng nhau tới nhiều chữ số giữa hai cấu hình KHÁC nhau là dấu hiệu HỎNG**, không
>    phải dấu hiệu bền vững.

---

## Thứ tự ô — dán theo đúng dãy này

`S1` → **Restart runtime** → `S2` → `S3` → `S4` → `S5` → `S6` → `S6b` → `S7`

Mỗi mục có thể gồm **nhiều ô mã**, chạy hết theo thứ tự trong mục rồi mới sang mục sau:

| mục | số ô mã | ghi chú |
|---|---|---|
| S1 · S2 · S3 · S4 | 1 mỗi mục | Restart runtime sau S1 |
| **S5** | **2** | ô 1 chạy train · ô 2 đọc kết quả |
| **S6** | **2** | ô 1 chạy train · ô 2 đọc kết quả |
| **S6b** | **3** | ô 1 lượt A · ô 2 lượt B + kiểm · **ô 3 dọn thư mục** — đừng bỏ |
| **S6c** | 2 | **tuỳ chọn** — thử cỡ lô GPU 2, có thể giảm gần nửa thời gian train |
| **S7** | **1** | ô GỘP, đọc cả S5 lẫn S6 |

⚠️ Ô thứ ba của S6b (`shutil.rmtree(RES...)`) dọn thư mục thử nghiệm khỏi Drive. Bỏ nó thì
`_smoke_resume` nằm lẫn với checkpoint thật trong `MyDrive/thesis/ckpt/`.

---

## Mất bao lâu — ước, và cách biết mình đang chậm bất thường

| ô | việc | ước | dấu hiệu hỏng |
|---|---|---|---|
| S1 | cài gói + clone LLaMA-Factory | **5–8 phút** | quá 15 phút ⇒ mạng Colab kẹt |
| S2 | mount + bung kho + **bung 31 GB ảnh dạy** | **15–25 phút** | quá 40 phút ⇒ Drive đang bị bóp băng thông |
| S3 | dựng 22.854 cặp | **2–3 phút** | — |
| S4 | bảy phép tiền bay | vài giây | — |
| S5 | smoke 20 bước, 400 mẫu | **6–10 phút** | quá 20 phút ⇒ quên `max_samples` |
| S6 | smoke 200 cặp nặng nhất | **5–10 phút** | — |
| S6b | thử chạy tiếp sau khi mất máy | **6–10 phút** | — |
| S7 | phán quyết | vài giây | — |
| | **tổng** | **~45–65 phút · ~5 đơn vị** | |

⚠️ Ô S2 chỉ tốn ngần ấy **lần đầu trong một máy ảo**. Mất máy rồi dựng lại thì ô S2 tự bỏ qua
khâu bung ảnh nếu thư mục đã đủ 64.567 tệp — nhưng máy ảo MỚI thì phải bung lại từ đầu.

---

## Trước khi bắt đầu

- Runtime → **A100**. (L4 cũng chạy được smoke, nhưng kết luận bộ nhớ chỉ có giá trị cho đúng
  loại card sẽ dùng lúc train thật — chọn loại nào thì train bằng loại đó.)
- Số dư đơn vị Colab: smoke cần **~5**. Kiểm luôn xem có ≥ **120** để chạy tiếp lượt train đầu.
- Trên Drive phải có: `thesis_rented.zip` · `derived.tar.gz` · `derived_train_en.tar.gz` ·
  `train_images_p0..p3.tar` · `ckpt/s2_seed101/`.

---

## Ô S1 — cài gói  ▸ rồi **Restart runtime**

```python
!pip install -q -U "transformers>=4.49" accelerate peft bitsandbytes datasets \
    huggingface_hub pyarrow pillow pyyaml liger-kernel
# ⚠️ PIN đúng SHA đã dùng lúc smoke 23/8 — (x6) đòi cả bốn lượt cùng một bản.
#    KHÔNG dùng --depth 1 ở đây: bản clone nông không checkout được commit chỉ định.
!git clone https://github.com/hiyouga/LLaMA-Factory /content/LLaMA-Factory
!cd /content/LLaMA-Factory && git checkout c4e09c7cbe18844816af9e18a97fe465515edbcd
!pip install -q -e "/content/LLaMA-Factory[torch,metrics]"
!cd /content/LLaMA-Factory && git rev-parse HEAD    # phải in ra ĐÚNG c4e09c7cbe18…
import importlib.metadata as m
print("liger-kernel:", m.version("liger_kernel"))
```

**Kiểm hai dòng:** SHA của LLaMA-Factory in ra (chép vào `report/106` sau khi smoke đạt — mục
(x6) đòi pin phiên bản) · `liger-kernel` có số phiên bản.

⚠️ **Restart runtime**, rồi mới chạy ô S2.

---

## Ô S2 — Drive, kho, dữ liệu

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
# ⚠️ BẮT BUỘC: bung ĐÈ bản tiếng Anh. derived.tar.gz là bản khai báo TIẾNG VIỆT.
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
`adapter_model.safetensors` · card đúng loại định dùng.

⛔ Khai báo ra **1.074** nghĩa là gói tiếng Anh chưa bung đè — dừng, đừng chạy tiếp.

---

## Ô S3 — dựng cặp NGAY TRÊN COLAB

Không upload tệp cặp từ máy khác lên. Dựng tại chỗ từ `descriptors.jsonl` + `s2.json` để tệp
dùng lúc train chắc chắn sinh ra từ đúng dữ liệu vừa bung.

```python
!cd {REPO} && python harness/build_min_desc.py
```

**Kiểm bốn dòng in ra:**

| dòng | phải là |
|---|---|
| `cặp dựng được` | **22854** |
| `bỏ · s2_khong_khop_khai_bao` | **không xuất hiện** (0 dòng lệch) |
| bảy bất biến | **✅ cả bảy** |
| `200 cặp nặng nhất` | có in ra |

⛔ Bất biến nào ⛔ thì script tự dừng và **không ghi tệp** — đó là hành vi đúng, đừng vá để nó
chạy tiếp.

---

## Ô S4 — bảy phép tiền bay, 10 giây

```python
import json, yaml, os
from PIL import Image
BR = f"{TR}/branches"
c  = yaml.safe_load(open(f"{REPO}/harness/train_config_orpo.yaml", encoding="utf-8"))
g  = yaml.safe_load(open(f"{REPO}/harness/train_config.yaml",      encoding="utf-8"))
info = json.load(open(f"{BR}/dataset_info.json", encoding="utf-8"))
cap  = json.load(open(f"{BR}/min_desc.json",     encoding="utf-8"))

# ① chỉ 8 khoá được phép khác train_config.yaml
cho_phep = {"dataset","seed","output_dir","dataset_dir","adapter_name_or_path",
            "create_new_adapter","stage","pref_loss","pref_beta","max_steps",
            "num_train_epochs","per_device_train_batch_size","gradient_accumulation_steps",
            "enable_liger_kernel","preprocessing_num_workers","save_steps",
            "learning_rate"}     # ← stage-2 hạ còn 2e-5, xem report/106 (x3b)
khac = {k for k in set(c) | set(g) if c.get(k) != g.get(k)}
print("① khoá khác train_config.yaml:", sorted(khac))
print("   ngoài danh sách cho phép  :", sorted(khac - cho_phep), "← phải là []")

# ② không được khai cả max_steps lẫn num_train_epochs
print("② max_steps:", c.get("max_steps"), "| num_train_epochs:", c.get("num_train_epochs"),
      "← phải là 800 và None")
# ③ nối đúng adapter S2, và KHÔNG đẻ adapter mới
print("③ adapter:", c["adapter_name_or_path"], "| create_new_adapter:",
      c.get("create_new_adapter"), "← phải là False")
print("   adapter có thật:", os.path.isdir(c["adapter_name_or_path"]))
# ④ dataset_info khai đúng ranking
print("④ ranking:", info["gui_min_desc"].get("ranking"), "← phải là True |",
      "ce2 ranking:", info["gui_ce2_s2"].get("ranking"), "← phải là None")
# ⑤ output_dir NẰM TRÊN DRIVE và rỗng (lượt smoke phải là lượt MỚI)
print("⑤ output_dir:", c["output_dir"])
print("   nằm trên Drive:", c["output_dir"].startswith("/content/drive/"), "← BẮT BUỘC True")
print("   đã tồn tại    :", os.path.isdir(c["output_dir"]), "← lượt mới phải là False")
# ⑥ ĐƯỜNG DẪN ẢNH MỞ ĐƯỢC — sai prefix thì chết SAU 42 phút mã hoá token
p = cap[0]["images"][0]
print("⑥ ảnh mẫu:", p, "| mở được:", os.path.exists(p))
Image.open(p).close()
# ⑦ đĩa
v = os.statvfs('/content')
print("⑦ đĩa trống:", round(v.f_bavail*v.f_frsize/2**30, 1), "GB ← cần ≥ 20")
```

**Bảy dòng, bảy điều kiện.** Dòng ① in `[]` · ② `800` và `None` · ③ `False` và `True` ·
④ `True` và `None` · ⑤ `False` · ⑥ `True` · ⑦ ≥ 20.

⚠️ Dòng ⑥ là phép đắt nhất nếu bỏ qua: sai prefix ảnh thì lỗi chỉ nổ **sau 42 phút** mã hoá token.

---

## Ô S5 — SMOKE A: 20 bước trên tập cặp đầy đủ

```python
import shutil, os, yaml, json
PROBE = "/content/probe_orpo20"
shutil.rmtree(PROBE, ignore_errors=True)      # ⛔ BẮT BUỘC — xem cảnh báo dưới
c = yaml.safe_load(open(f"{REPO}/harness/train_config_orpo.yaml", encoding="utf-8"))
c.update({"max_steps": 20, "output_dir": PROBE, "save_steps": 1000, "logging_steps": 5,
          "max_samples": 400})     # ⚠️ smoke KHÔNG mã hoá cả 22.854 cặp — 400 mẫu là đủ để
                                   #    kiểm cơ học, và tiết kiệm ~35 phút. Lượt THẬT bỏ khoá này.
yaml.safe_dump(c, open("/content/probe20.yaml","w",encoding="utf-8"), allow_unicode=True)

# in cấu hình tiến trình THẬT SỰ dùng — không kiểm mã nguồn, kiểm dòng này
print("=== CẤU HÌNH SẼ CHẠY ===")
for k in ("stage","pref_loss","pref_beta","dataset","adapter_name_or_path",
          "create_new_adapter","per_device_train_batch_size","enable_liger_kernel",
          "gradient_accumulation_steps","max_steps","max_samples","output_dir"):
    print(f"  {k:32s} {c.get(k)}")

!cd {REPO} && llamafactory-cli train /content/probe20.yaml
```

⛔ **Không xoá `PROBE` là hỏng câm.** LLaMA-Factory sẽ chạy tiếp từ checkpoint cũ, **nhảy qua**
20 bước rồi chạy đúng một bước: log vẫn in `Training completed`, vẫn có `total_flos`, trông y
như đạt.

**Đọc bằng HAI con số, không phải một:**

```python
import json
s = json.load(open(f"{PROBE}/trainer_state.json", encoding="utf-8"))
log = [l for l in s["log_history"] if "loss" in l]
# ⚠️ train_runtime KHÔNG phải khoá cấp cao nhất của trainer_state.json — nó nằm trong
#    MỤC TÓM TẮT cuối của log_history, mà bộ lọc `if "loss" in l` ở trên loại đúng mục đó.
#    `s.get("train_runtime")` luôn trả None; đó là lỗi đọc, không phải lỗi lượt train.
tt = [l for l in s["log_history"] if "train_runtime" in l]
print("số dòng loss   :", len(log), "← phải là 4 (20 bước / logging_steps 5)")
print("loss đầu → cuối:", log[0]["loss"], "→", log[-1]["loss"])
print("train_runtime  :", tt[-1]["train_runtime"] if tt else "chưa có mục tóm tắt")
print("total_flos     :", s.get("total_flos"))
print("\ncác trường ORPO ghi trong log (⚠️ chép về cho tôi dòng này):")
print(" ", sorted(log[-1].keys()))
```

| kiểm | ĐẠT | HỎNG |
|---|---|---|
| ⭐ **danh sách trường** | có ít nhất một khoá chứa `rewards` / `accur` / `odds` | **không có khoá nào** ⇒ nó **KHÔNG chạy đường ưu tiên**, chỉ SFT thường. Lỗi câm: mọi thứ khác trông y như đạt ⇒ **STOP** |
| ⭐ **loss/`sft_loss` dòng ĐẦU** | cỡ **0,3–0,5** | **2–3** ⇒ adapter S2 **chưa nạp**, đang train adapter mới từ mô hình gốc ⇒ **STOP**, kiểm lại dòng ③ ô S4 |
| số dòng loss | **4** | 1 ⇒ đã chạy tiếp từ checkpoint cũ, xoá `PROBE` rồi làm lại |
| `train_runtime` | **≥ 60 s** | ~15 s ⇒ như trên |
| loss | cỡ **0,5–3** | `nan` ⇒ **liger không hợp đường pairwise**. Tắt `enable_liger_kernel` rồi chạy lại ô S5 MỘT lần. Vẫn `nan` ⇒ **STOP**, cổng (x6) |
| có nổ OOM không | không | có ⇒ hạ `per_device_train_batch_size` **không** giúp gì ở đây vì đã là 1 ⇒ **STOP** |

---

## Ô S6 — SMOKE B: 200 cặp NẶNG NHẤT ⚠️ đây mới là phép quyết định

Bài học P10: cấu hình chạy ngọt trên mẫu thường vẫn **chết** trên 200 mẫu dài nhất. **12 phút
thăm dò cứu một lượt train 20 giờ.** Probe trên mẫu đầu tập không kết luận được gì về bộ nhớ.

```python
import shutil, yaml
PROBE2 = "/content/probe_orpolong"
shutil.rmtree(PROBE2, ignore_errors=True)
c = yaml.safe_load(open(f"{REPO}/harness/train_config_orpo.yaml", encoding="utf-8"))
c.update({"dataset": "gui_min_desc_long", "max_steps": 20, "output_dir": PROBE2,
          "save_steps": 1000, "logging_steps": 5})
yaml.safe_dump(c, open("/content/probelong.yaml","w",encoding="utf-8"), allow_unicode=True)
print("=== dataset thật sự chạy:", c["dataset"], "===")
!cd {REPO} && llamafactory-cli train /content/probelong.yaml
```

```python
import json, torch
s = json.load(open(f"{PROBE2}/trainer_state.json", encoding="utf-8"))
log = [l for l in s["log_history"] if "loss" in l]
print("số dòng loss :", len(log), "← phải là 4")
print("loss         :", [l["loss"] for l in log])
print("train_runtime:", s.get("train_runtime"))
print("đỉnh bộ nhớ  :", round(torch.cuda.max_memory_allocated()/2**30, 1), "GB")
```

⭐ **So `total_flos` của S5 và S6.** Hai tập dữ liệu KHÁC nhau mà `total_flos` trùng tới nhiều
chữ số ⇒ **HỎNG**, một trong hai lượt không chạy đúng dataset nó khai.

---

## Ô S6b — SMOKE C: **mất máy giữa chừng có chạy tiếp được không**

(x6) đặt *"không resume/save-load đúng"* thành điều kiện STOP, nên phải thử thật chứ không tin.
Tài khoản Colab này **không có background execution** và đã mất máy ảo **8 lần trong 2 lượt S1** —
đây là tình huống sẽ xảy ra, không phải nếu.

```python
import shutil, yaml, os, json, time
RES = "/content/drive/MyDrive/thesis/ckpt/_smoke_resume"   # trên Drive, đúng như lượt thật
shutil.rmtree(RES, ignore_errors=True); os.makedirs(RES, exist_ok=True)
c = yaml.safe_load(open(f"{REPO}/harness/train_config_orpo.yaml", encoding="utf-8"))
c.update({"dataset": "gui_min_desc_long", "max_steps": 12, "output_dir": RES,
          "save_steps": 5, "logging_steps": 2})
yaml.safe_dump(c, open("/content/res_a.yaml","w",encoding="utf-8"), allow_unicode=True)
t0 = time.time()
!cd {REPO} && llamafactory-cli train /content/res_a.yaml
print("LƯỢT A xong sau", round(time.time()-t0), "giây · điểm lưu:", sorted(os.listdir(RES)))
```

```python
# LƯỢT B — KHÔNG xoá RES. Giả lập dựng lại máy: cùng output_dir, nâng max_steps lên 20.
c["max_steps"] = 20
yaml.safe_dump(c, open("/content/res_b.yaml","w",encoding="utf-8"), allow_unicode=True)
t0 = time.time()
!cd {REPO} && llamafactory-cli train /content/res_b.yaml
tB = round(time.time()-t0)

st = json.load(open(f"{RES}/trainer_state.json", encoding="utf-8"))
ck = sorted(d for d in os.listdir(RES) if d.startswith("checkpoint-"))
cuoi = f"{RES}/{ck[-1]}"
print("global_step cuối :", st["global_step"], "← phải là 20")
print("thời gian lượt B :", tB, "giây ← phải ngắn hơn lượt A rõ rệt (chỉ chạy 8 bước)")
print("điểm lưu         :", ck)
print("trong điểm lưu   :", sorted(os.listdir(cuoi)))
print("  có adapter     :", any("adapter_model" in f for f in os.listdir(cuoi)), "← True")
print("  có optimizer   :", any("optimizer" in f for f in os.listdir(cuoi)), "← True")
```

⚠️ **`grep "Resuming training from"` trống ngay sau khi khởi động là báo động giả** — dòng đó in
sau ~40 giây nạp thư viện. Đọc bằng `global_step` cuối, không bằng dòng log đầu.

| kiểm | ĐẠT | HỎNG |
|---|---|---|
| `global_step` sau lượt B | **20** | **12** ⇒ nó train lại từ đầu rồi ghi đè ⇒ **STOP** |
| thời gian lượt B | ngắn hơn A rõ rệt | bằng hoặc dài hơn ⇒ không chạy tiếp thật |
| trong điểm lưu | có **cả** `adapter_model` **và** `optimizer` | thiếu `optimizer` ⇒ chạy tiếp sẽ mất trạng thái bộ tối ưu ⇒ **STOP** |

⭐ **Phép kiểm rẻ "điểm lưu có trọn không":** ghi dở thì bản **CUỐI phải NHỎ HƠN** bản trước.
So `os.path.getsize` của hai `adapter_model.safetensors` gần nhất khi nghi ngờ.

```python
shutil.rmtree(RES, ignore_errors=True)   # dọn, đừng để lẫn với checkpoint thật trên Drive
```

---

## Ô S6c — (tuỳ chọn, ~10 phút) **thử cỡ lô GPU 2** — có thể giảm gần nửa thời gian train

Cỡ lô **hiệu dụng vẫn là 16**, chỉ đổi cách chia: `2 × tích luỹ 8` thay vì `1 × 16`. Phép tính
không đổi, chỉ tận dụng GPU tốt hơn. Chạy trên **200 cặp nặng nhất** — nếu cỡ 2 sống được ở đây
thì sống được cả lượt.

⚠️ Quyết định này phải chốt **TRƯỚC lượt đầu** và **giữ nguyên cho cả bốn lượt** — (x3) đòi bốn
lượt cùng cấu hình. Nâng giữa chừng là hỏng phép so.

```python
import shutil, yaml, json, os
PROBE3 = "/content/probe_orpo_b2"
shutil.rmtree(PROBE3, ignore_errors=True)
c = yaml.safe_load(open(f"{REPO}/harness/train_config_orpo.yaml", encoding="utf-8"))
c.update({"dataset": "gui_min_desc_long", "max_steps": 20, "output_dir": PROBE3,
          "save_steps": 1000, "logging_steps": 5,
          "per_device_train_batch_size": 2, "gradient_accumulation_steps": 8})
yaml.safe_dump(c, open("/content/probe_b2.yaml","w",encoding="utf-8"), allow_unicode=True)
print("=== cỡ lô GPU", c["per_device_train_batch_size"],
      "× tích luỹ", c["gradient_accumulation_steps"],
      "= hiệu dụng", c["per_device_train_batch_size"]*c["gradient_accumulation_steps"],
      "(phải vẫn là 16) ===")
!cd {REPO} && llamafactory-cli train /content/probe_b2.yaml
```

```python
import json, os
def rt(d):
    p = f"{d}/trainer_state.json"
    if not os.path.exists(p): return None, None
    s = json.load(open(p, encoding="utf-8"))
    tt = [l for l in s["log_history"] if "train_runtime" in l]
    return (tt[-1]["train_runtime"] if tt else None), s.get("total_flos")

r1, f1 = rt("/content/probe_orpolong")     # cỡ lô 1
r2, f2 = rt("/content/probe_orpo_b2")      # cỡ lô 2
print(f"cỡ lô 1: {r1} s · flos {f1}")
print(f"cỡ lô 2: {r2} s · flos {f2}")
if r1 and r2:
    print(f"\nnhanh hơn {100*(1-r2/r1):.0f}% → 800 bước: "
          f"{r1/20*800/3600:.1f} h  →  {r2/20*800/3600:.1f} h")
    print("⭐ flos hai bên phải GẦN BẰNG nhau — cùng phép tính, chỉ khác cách chia lô.")
    print("   Lệch nhiều ⇒ có gì đó khác ngoài cỡ lô, KHÔNG nâng.")
```

| kết quả | làm gì |
|---|---|
| **chạy xong, nhanh hơn rõ** | Sửa `per_device_train_batch_size: 2` và `gradient_accumulation_steps: 8` trong **cả hai** `train_config_orpo.yaml` và `train_config_ce2.yaml`, ghi một dòng vào `report/106` mục (x), rồi giữ nguyên cho cả bốn lượt |
| **OOM** | Giữ nguyên cỡ lô 1. Đây là kết quả bình thường, không phải lỗi — bỏ qua ô này và đi tiếp |
| **chạy được nhưng không nhanh hơn** | Giữ cỡ lô 1 cho đơn giản |

⚠️ Ô này **không** phải cổng STOP. Trượt thì chỉ mất 10 phút và train chậm hơn, không sao cả.

---

## Ô S7 — phán quyết (ô GỘP, đọc cả S5 lẫn S6)

⚠️ Ô này **thay hẳn** bản S7 cũ. Nó đọc `train_runtime` đúng chỗ, in ra tên trường của
`trainer_log.jsonl`, và so `total_flos` — ba việc trong một ô.

```python
import json, os

def doc(d, ten):
    p = f"{d}/trainer_state.json"
    if not os.path.exists(p):
        print(f"⛔ {ten}: không thấy {p}"); return None
    s = json.load(open(p, encoding="utf-8"))
    tt = [l for l in s["log_history"] if "train_runtime" in l]
    lo = [l for l in s["log_history"] if "loss" in l]
    rt = tt[-1]["train_runtime"] if tt else None
    print(f"\n=== {ten}  ({d}) ===")
    print(f"  train_runtime : {rt}")
    print(f"  total_flos    : {s.get('total_flos')}")
    print(f"  số dòng loss  : {len(lo)}  ← phải là 4")
    for l in lo:
        print("   ", {k: (round(v, 4) if isinstance(v, float) else v)
                      for k, v in l.items() if k not in ("epoch",)})
    tl = f"{d}/trainer_log.jsonl"
    print(f"  trainer_log.jsonl: {os.path.exists(tl)}")
    if os.path.exists(tl):
        e = [json.loads(x) for x in open(tl, encoding="utf-8")]
        print("   trường:", sorted(e[-1].keys()))
    return s, rt

a = doc("/content/probe_orpo20",   "S5 — 400 mẫu thường")
b = doc("/content/probe_orpolong", "S6 — 200 cặp nặng nhất")

if a and b:
    (sa, ra), (sb, rb) = a, b
    la = [l["loss"] for l in sa["log_history"] if "loss" in l]
    lb = [l["loss"] for l in sb["log_history"] if "loss" in l]
    khac_flos = sa.get("total_flos") != sb.get("total_flos")
    ok = len(la) == 4 and len(lb) == 4 and all(x == x for x in la + lb) and khac_flos
    print("\n=== PHÁN QUYẾT ===")
    print("flos S5:", sa.get("total_flos"))
    print("flos S6:", sb.get("total_flos"))
    print("  khác nhau:", khac_flos, "← BẮT BUỘC True, trùng là HỎNG")
    if rb:
        print(f"\ngiây/bước (đo trên cặp NẶNG NHẤT): {rb/20:.1f} s")
        print(f"  → 800 bước ≈ {rb/20*800/3600:.1f} giờ/lượt MIN-DESC")
    print("\n" + ("✅ QUA CỔNG S5+S6 — còn phải ĐẠT cả ba dòng của ô S6b nữa"
                  if ok else "⛔ TRƯỢT — dừng, báo lại, KHÔNG train"))
```

**Chép ba thứ này về báo lại:** `loss A` · `loss B` · `giây/bước ước`.

### Nếu QUA
Chạy `harness/colab_train_min_desc.md` (sẽ soạn sau khi có số giây/bước thật, vì lịch phụ
thuộc con số đó). Thứ tự: MIN-DESC/101 → CE2-S2/101 → cổng cơ học → 202.

### Nếu TRƯỢT
⛔ **Không fork custom trainer để cứu** — (x6) cấm. Ghi lại lỗi thật vào `report/106` và
quay về phương án dự phòng, cân nhắc theo `report/117` Mục 3.
