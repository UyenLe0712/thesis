# S2 — dán thẳng, mười ô, theo đúng thứ tự

Bản tự đủ. Không phải mở `run_on_colab.md`. Giải thích *vì sao* nằm ở
`harness/colab_train_s2.md`; file này chỉ có việc phải làm.

**Trước khi bắt đầu:** Runtime → **A100** · kiểm **số dư đơn vị Colab ≥ 260** (một lượt ~126,
hai lượt ~252). Hết đơn vị giữa lượt 26 giờ là phải chờ mua rồi dựng lại.

---

## Ô 1 — cài gói  ▸ rồi **Restart runtime**

```python
!pip install -q -U "transformers>=4.49" accelerate peft bitsandbytes datasets \
    huggingface_hub pyarrow pillow rapidocr_onnxruntime pyyaml liger-kernel
!git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory /content/LLaMA-Factory
!pip install -q -e "/content/LLaMA-Factory[torch,metrics]"
import importlib.metadata as m
print("liger-kernel:", m.version("liger_kernel"))     # thiếu gói này là ô 6 chết ngay
```

⚠️ **Restart runtime sau ô này**, rồi mới chạy ô 2.

## Ô 2 — khôi phục dữ liệu từ Drive

```python
from google.colab import drive; drive.mount('/content/drive')
import os, zipfile, torch, glob, yaml
D, WS = "/content/drive/MyDrive/thesis", "/content/ws"
os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_rented.zip").extractall(WS)
REPO = f"{WS}/thesis"; os.chdir(REPO)
TR, TE = f"{REPO}/harness/dg1_cache/train_ac", f"{REPO}/harness/dg1_cache/test_ac"
dem = lambda d: len(os.listdir(d)) if os.path.isdir(d) else 0

!tar xzf {D}/derived.tar.gz -C {REPO}
# ⚠️ BẮT BUỘC: bung ĐÈ bản tiếng Anh lên. derived.tar.gz là bản khai báo TIẾNG VIỆT
#    (trước 14/8). Quên dòng này là train tiếp trên dữ liệu KHÁC mà log không báo gì.
if os.path.exists(f"{D}/derived_train_en.tar.gz"):
    !tar xzf {D}/derived_train_en.tar.gz -C {REPO}
    print("đã bung đè bản TIẾNG ANH ✅")
else:
    print("⛔ DỪNG — không thấy derived_train_en.tar.gz, phải chạy lại ô 5a")
os.makedirs(f"{TR}/images", exist_ok=True)
goi = sorted(glob.glob(f"{D}/train_images_p*.tar"))
if dem(f"{TR}/images") >= 64567:
    print("ảnh dạy đã đủ — bỏ qua khâu bung")
else:
    for g in goi:
        !tar xf {g} -C {TR}/images

print("card    :", torch.cuda.get_device_name(0), "| số card:", torch.cuda.device_count())
print("lõi CPU :", os.cpu_count())
print("ảnh dạy :", dem(f"{TR}/images"), "← cần 64.567")
print("cutoff  :", yaml.safe_load(open(f"{REPO}/harness/train_config.yaml",
      encoding="utf-8"))["cutoff_len"], "← phải là 2560")
```

| phải thấy | nếu không |
|---|---|
| `A100` · số card **1** | 2 card thì LLaMA-Factory tự nhân cỡ lô — **dừng** |
| ảnh dạy **64.567** | thiếu ⇒ train hỏng mà log không báo — **dừng** |
| cutoff **2560** | in 2048 ⇒ gói Drive là bản trước 11/8 — **dừng, tải gói mới** |
| `đã bung đè bản TIẾNG ANH ✅` | không thấy ⇒ khai báo còn tiếng Việt, `S2−S1` sẽ lẫn phần chuyển ngữ — **dừng** |

## Ô 3 — kiểm gói mã

```python
import os
s = open(f"{REPO}/harness/infer_branch.py", encoding="utf-8").read()
print("infer :", len(s.encode()), "B  ← PHẢI đúng 27.443")
print("chữ ký lượt chạy:", "là của lượt chạy KHÁC" in s, " ← phải True")
print("branches:", sorted(os.listdir(f"{REPO}/harness/dg1_cache/train_ac/branches")))
```

`branches` phải có **`s2.json`** và `dataset_info.json`. Thiếu `s2_long.json` thì chép lại:

```python
!cp {D}/branches_backup/*.json {REPO}/harness/dg1_cache/train_ac/branches/
```

⚠️ Nếu `branches` **thiếu `s2_long.json`** thì đó là bình thường — ô 5b dựng lại. Đừng chép
từ `branches_backup/`, bản đó cũng thiếu.

⚠️ `score_run.py` in ra **39.763 B** chứ không phải 34.610 như runbook cũ ghi — đó là bản vá
16/8, **bình thường**, và khâu train không dùng tệp này.

## Ô 4 — đặt HF_TOKEN

```python
import os; os.environ["HF_TOKEN"] = "hf_..."      # token của bạn
```

## Ô 5 — sinh cấu hình  ⚠️ **ĐÂY LÀ Ô DUY NHẤT KHÁC LƯỢT S1**

```python
import yaml, os
BRANCH, SEED = "s2", 101          # ⚠️ lượt S1 là ("s1", 101). ĐỔI ĐÚNG DÒNG NÀY.
OUT = f"{D}/ckpt/{BRANCH}_seed{SEED}"
os.makedirs(OUT, exist_ok=True)
c = yaml.safe_load(open(f"{REPO}/harness/train_config.yaml", encoding="utf-8"))
c.update({"dataset": f"gui_{BRANCH}", "seed": SEED, "output_dir": OUT,
          "dataset_dir": f"{REPO}/harness/dg1_cache/train_ac/branches",
          "preprocessing_num_workers": 8})        # 42 phút thay vì 2,5 giờ
c["enable_liger_kernel"] = True
LOG = f"/content/train_{BRANCH}_seed{SEED}.log"
for k in ("disable_gradient_checkpointing","gradient_checkpointing","max_steps","max_samples"):
    c.pop(k, None)
yaml.safe_dump(c, open("/content/cfg.yaml","w",encoding="utf-8"),
               allow_unicode=True, sort_keys=False)
print(f"nhánh {BRANCH} · hạt giống {SEED} · cỡ lô hiệu dụng",
      c["per_device_train_batch_size"] * c["gradient_accumulation_steps"], "← phải là 16")
print("liger", c.get("enable_liger_kernel"), "· 4-bit", c.get("quantization_bit"), "← True / 4")
print("khoá thăm dò còn sót:",
      [k for k in ("max_steps","max_samples") if k in c], "← phải []")
print("BÊN TRONG output_dir:", os.listdir(OUT), "← lượt MỚI phải là []")
```

⚠️ Dòng cuối bắt một lỗi im lặng: LLaMA-Factory **tự chạy tiếp** từ checkpoint còn sót trong
`output_dir`. Lượt mới mà thấy `checkpoint-*` thì xoá thư mục rồi chạy lại ô này:
```python
import shutil; shutil.rmtree(OUT, ignore_errors=True)
```

## Ô 5a — 🛑 DỰNG LẠI NHÃN KHAI BÁO SANG TIẾNG ANH  ⚠️ **BẮT BUỘC TRƯỚC KHI TRAIN**

Dữ liệu S2 trên Drive là bản **trước 14/8**, khai báo còn tiếng Việt:
`<desc>chữ bấm được | Email | <point>321,803</point> | bên phải chữ "Copy link"</desc>`

`report/106` mục sửa đổi **(q)** ngày 14/8 đã đổi sang tiếng Anh, và ghi rõ *"Việc bắt buộc
trước khi train s2: dựng lại `descriptors.jsonl` và bốn tệp nhánh ở quy mô đủ"*. Việc đó
**chưa làm**.

**Vì sao không phải chuyện chữ nghĩa.** Khai báo tiếng Việt + câu chấm tiếng Anh ⇒ S2 khác S1
ở **hai** thứ cùng lúc: có thêm dòng khai báo, **và** có thêm một lần chuyển ngữ. Hiệu
`S2 − S1` là con số headline khoá ở mục 6, và nó sẽ **lẫn cả phần do chuyển ngữ** mà **không
nhánh nào tách được** (`s2r` cũng tiếng Việt nên không giúp). Train 26 giờ ra một con số không
diễn giải được.

### Ô 5a-1 — sao lưu trước, rồi dựng lại

```python
import os, shutil, time
B = f"{REPO}/harness/dg1_cache/train_ac/branches"
BAK = f"{D}/branches_vi_{time.strftime('%m%d')}"          # bản tiếng Việt, giữ để đối chiếu
shutil.copytree(B, BAK, dirs_exist_ok=True)
print("đã sao lưu bản cũ →", BAK, sorted(os.listdir(BAK)))
```

```python
# ~10-15 phút, KHÔNG cần GPU. Chỉ dựng lại phần TẬP DẠY.
!cd {REPO} && python harness/descriptor_label_build.py 2>&1 | tail -20
```

```python
# ~5 phút. Dựng lại bốn tệp nhánh; nó tự ghép độ dài token cho s2r bằng bộ tách token Qwen.
!cd {REPO} && python harness/build_branch_data.py --img-prefix "{REPO}/harness/dg1_cache/train_ac/" 2>&1 | tail -14
```

⛔ **KHÔNG chạy `build_test_data.py` và `tag_app_seen.py`.** Ô 0.10 gốc của runbook có hai
lệnh đó, nhưng chúng **dựng lại TẬP KIỂM** — mà cả bốn nhánh đã chấm (trần · S1×2 · Base) đều
nằm trên tập kiểm hiện tại. Dựng lại là mất khả năng so sánh, và mất **im lặng**.
`descriptor_label_build.py` mặc định `--split train` nên nó không đụng tập kiểm.

### Ô 5a-2 — 🛑 BA PHÉP KIỂM, phải ĐẠT cả ba mới được train

```python
import json, re, glob
B = f"{REPO}/harness/dg1_cache/train_ac/branches"
d = {b: json.load(open(f"{B}/{b}.json", encoding="utf-8"))
     for b in ("s1","s2","s2r","s2_nopoint")}
desc = lambda x: (lambda m: m.group() if m else None)(
    re.search(r"<desc>.*?</desc>", x["messages"][-1]["content"], re.S))
cau  = lambda x: (lambda t: t.split("</desc>",1)[1].strip() if "</desc>" in t else t.strip())(
    x["messages"][-1]["content"])
n  = len(d["s1"]); nd = sum(1 for x in d["s2"] if desc(x))

# ── KIỂM 1: không còn ký tự tiếng Việt nào trong khai báo ────────────────────────
VI = re.compile(r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợ"
                r"ùúủũụưừứửữựỳýỷỹỵđ]", re.I)
xau = [x for x in d["s2"] if desc(x) and VI.search(desc(x))]
print(f"KIỂM 1  khai báo còn tiếng Việt: {len(xau)}  ← PHẢI LÀ 0")
if xau: print("   ví dụ:", desc(xau[0])[:110])
print("   mẫu  :", desc(next(x for x in d['s2'] if desc(x)))[:110])

# ── KIỂM 2: 9 bất biến của bốn nhánh ─────────────────────────────────────────────
K = [(f"câu {b} trùng s1", sum(1 for x,y in zip(d[b],d["s1"]) if cau(x)==cau(y)), n)
     for b in ("s2","s2r","s2_nopoint")]
K.append(("s1 KHÔNG có khai báo", sum(1 for x in d["s1"] if desc(x) is None), n))
K += [(f"số khai báo {b}", sum(1 for x in d[b] if desc(x)), nd)
      for b in ("s2","s2r","s2_nopoint")]
K.append(("s2_nopoint sót <point>",
          sum(1 for x in d["s2_nopoint"] if desc(x) and "<point>" in desc(x)), 0))
K.append(("s2r khác s2 ở bước có desc",
          sum(1 for x,y in zip(d["s2r"],d["s2"]) if desc(x) and desc(y) and desc(x)!=desc(y)), nd))
bad = 0
print("\nKIỂM 2  chín bất biến")
for nm, got, want in K:
    ok = got == want; bad += not ok
    print(f"   {'ĐẠT' if ok else '⛔RỚT'}  {nm:30} {got:,}" + ("" if ok else f"  ≠ {want:,}"))

# ── KIỂM 3: s2r ghép độ dài TOKEN với s2 ────────────────────────────────────────
from transformers import AutoTokenizer
tk = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-VL-3B-Instruct")
cap = [(desc(x), desc(y)) for x,y in zip(d["s2r"],d["s2"]) if desc(x) and desc(y)]
lech = [len(tk(a).input_ids) - len(tk(b).input_ids) for a,b in cap[:1500]]
trong2 = sum(1 for x in lech if abs(x) <= 2)
print(f"\nKIỂM 3  s2r vs s2, {len(lech)} cặp · trong 2 token: {trong2/len(lech):.1%}"
      f"  ← cần ≥95% (mốc cũ 99,3%)")
print(f"   biên độ {min(lech)} … {max(lech)}")

print("\n" + ("="*60))
ok_all = (len(xau)==0) and (bad==0) and (trong2/len(lech) >= 0.95)
print("✅ ĐỦ ĐIỀU KIỆN TRAIN" if ok_all else "⛔ DỪNG — chưa đạt, đừng bấm ô 8")
print(f"   {n:,} mẫu mỗi nhánh · {nd:,} khai báo")
```

| kiểm | phải thấy | không đạt thì |
|---|---|---|
| 1 · ký tự tiếng Việt | **0** | mã chưa được vá — đối chiếu `descriptor_label_build.py` với mục (q) |
| 2 · chín bất biến | tất cả **ĐẠT** | dữ liệu hỏng, **đừng train** |
| 3 · ghép token s2r | **≥95%** trong 2 token | nhánh đối chứng độ dài mất tác dụng, S2r không phản bác được đòn "chuỗi dài thêm" |

### Ô 5a-3 — cất lên Drive ngay khi đạt

```python
!cd {REPO} && tar czf {D}/derived_train_en.tar.gz \
    harness/dg1_cache/train_ac/descriptors.jsonl \
    harness/dg1_cache/train_ac/branches \
    harness/descriptor_build_stats.json
!ls -lh {D}/derived_train_en.tar.gz
```

Tên khác `derived.tar.gz` để không đè bản cũ. Máy ảo đã bị thu hồi 8 lần — cất ngay khi vừa
có, đừng đợi cuối phiên.

⚠️ **Chạy lại ô 5b** (dựng `s2_long.json`) sau bước này, vì `s2.json` vừa đổi.

## Ô 5b — dựng `s2_long.json`  ⚠️ chỉ khi `branches` chưa có nó

Ô A.3g của chiến dịch S1 từng sinh tệp này, nhưng nó **không nằm trong gói Drive** và bản sao
lưu cũng thiếu. Dựng lại tại chỗ, vài giây, không cần GPU:

```python
import json, os
B = f"{REPO}/harness/dg1_cache/train_ac/branches"
rows = json.load(open(f"{B}/s2.json", encoding="utf-8"))
print("s2.json:", len(rows), "mẫu")

# 200 mẫu DÀI NHẤT. Dùng độ dài ký tự làm đại diện cho độ dài token — đếm token thật
# cho 64.567 mẫu chính là khâu 42 phút, mà phép thăm dò này chỉ cần "chắc chắn dài".
def dai(r): return sum(len(m.get("content", "")) for m in r["messages"])
rows.sort(key=dai, reverse=True)
lon = rows[:200]
json.dump(lon, open(f"{B}/s2_long.json", "w", encoding="utf-8"), ensure_ascii=False)

info = json.load(open(f"{B}/dataset_info.json", encoding="utf-8"))
info["gui_s2_long"] = dict(info["gui_s2"], file_name="s2_long.json")   # y hệt gui_s2, khác tệp
json.dump(info, open(f"{B}/dataset_info.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("dài nhất :", dai(lon[0]), "ký tự")
print("thứ 200  :", dai(lon[-1]), "ký tự")
print("trung vị toàn tập:", dai(rows[len(rows)//2]), "ký tự")
print("khoá dataset:", sorted(info))
```

Phải thấy `gui_s2_long` trong danh sách khoá, và **mẫu thứ 200 vẫn dài hơn hẳn trung vị** —
nếu không thì phép thăm dò chạy trên mẫu thường, tức không thăm dò gì cả.

💾 Cất lên Drive để lần sau khỏi dựng lại:
```python
!cp {B}/s2_long.json {B}/dataset_info.json {D}/branches_backup/
```

## Ô 5c — SAO LƯU ĐIỂM LƯU trước khi chạy tiếp  ⚠️ ~2 phút, **chỉ khi nối tiếp một lượt dở**

```python
import os, shutil, glob
BK = f"{D}/ckpt_backup/{BRANCH}_seed{SEED}"; os.makedirs(BK, exist_ok=True)
for c in sorted(glob.glob(f"{OUT}/checkpoint-*")):
    d = f"{BK}/{os.path.basename(c)}"
    if not os.path.exists(d): shutil.copytree(c, d)
print("đã sao lưu:", sorted(os.listdir(BK)))
```

Chặn đúng một kịch bản: nếu nó **không** nhận ra điểm lưu và bắt đầu lại từ 0 thì
`save_total_limit: 2` **lặng lẽ xoá** hai bản cũ khi bản thứ ba ra đời — lúc phát hiện thì hết
đường về. 182 MB mỗi bản.

## Ô 6 — 🛑 THĂM DÒ BỘ NHỚ 12 PHÚT  ⚠️ **KHÔNG ĐƯỢC BỎ**

S2 là nhánh **nặng nhất**. Cấu hình đang dùng được chọn bằng các lượt đo trên `gui_s1`; một
cấu hình khác từng chạy ngọt trên mẫu thường rồi **tràn bộ nhớ trên 200 mẫu dài nhất của s2**.
12 phút ở đây cứu một lượt 26 giờ.

```python
import yaml, subprocess, shutil
shutil.rmtree("/content/probe_s2long", ignore_errors=True)   # ⚠️ BẮT BUỘC — xem cảnh báo dưới
c = yaml.safe_load(open("/content/cfg.yaml", encoding="utf-8"))
c.update({"dataset": "gui_s2_long", "max_steps": 20, "output_dir": "/content/probe_s2long"})
yaml.safe_dump(c, open("/content/cfg_probe.yaml","w",encoding="utf-8"),
               allow_unicode=True, sort_keys=False)
r = subprocess.run(["llamafactory-cli","train","/content/cfg_probe.yaml"],
                   capture_output=True, text=True)
print(r.stdout[-2500:]); print("--- STDERR ---"); print(r.stderr[-1500:])
```

⛔ **Không xoá `/content/probe_s2long` thì phép thăm dò KHÔNG ĐO GÌ CẢ.** LLaMA-Factory tự dò
điểm lưu khi `resume_from_checkpoint` để trống, nên nó nạp lại checkpoint của lượt thăm dò
trước, **nhảy qua** 20 bước cũ (94 lô/giây) rồi chạy đúng một bước. Log vẫn in
`Training completed`, vẫn có `total_flos`, trông y như đạt. Đã mắc thật ngày 18/8.

**Đọc bằng HAI CON SỐ, đừng đọc chữ `Training completed`:**

| phải thấy | nghĩa |
|---|---|
| `train_runtime` **≈ 200–230 s** cho 20 bước | chạy thật (~11 s/bước). Thấy ~15 s ⇒ **nó nhảy qua**, thư mục chưa sạch |
| `train_loss` **≈ 2,4** | trọng số mới. Thấy ~0,1 ⇒ **đang chạy tiếp từ lượt cũ** |

| thấy gì | làm gì |
|---|---|
| 20 bước · runtime ~220 s · loss ~2,4 | ✅ sang ô 7 |
| `CUDA out of memory` | ⛔ **DỪNG.** Hạ `per_device_train_batch_size` 4→2 **và** nâng `gradient_accumulation_steps` 4→8 (giữ cỡ lô hiệu dụng **16**), thăm dò lại. Đổi cỡ lô hiệu dụng là đổi thí nghiệm ⇒ phải ghi mục sửa đổi `report/106` |

⚠️ Xong thì **chạy lại ô 5** để quét sạch `max_steps` và `gui_s2_long` khỏi `cfg.yaml` thật.

## Ô 7 — 🛑 KIỂM VÀNG: cfg có khớp lượt S1 không

```python
import yaml
moi = yaml.safe_load(open("/content/cfg.yaml", encoding="utf-8"))
cu  = yaml.safe_load(open(f"{D}/logs/s1_seed101/cfg.yaml", encoding="utf-8"))
khac = [(k, cu.get(k), moi.get(k)) for k in sorted(set(moi)|set(cu)) if cu.get(k) != moi.get(k)]
print(f"khoá: tham chiếu {len(cu)} · lượt này {len(moi)}\nKHÁC NHAU:")
for k,a,b in khac: print(f"  {k}: {a}  →  {b}")
cho_phep = {"seed","output_dir","dataset","preprocessing_num_workers"}
print("\n✅ ĐÚNG" if {t[0] for t in khac} <= cho_phep else "\n⛔ DỪNG — có khoá lạ bị đổi")
```

Lần này phải khác đúng **`dataset`** (`gui_s1`→`gui_s2`) và `output_dir`, cộng `seed` nếu
lượt tham chiếu là 101. **Khoá thứ tư khác là dừng hẳn** — lúc đó S2 và S1 không còn so được
với nhau và cả phép ablation mất nghĩa.

## Ô 7b — 🛑 TIỀN BAY: bảy phép kiểm, 10 giây

Bảy thứ dưới đây đều có thể **giết lượt 26 giờ mà không kêu**. Kiểm hết trước khi bấm ô 8.

```python
import yaml, json, os, random, shutil

c = yaml.safe_load(open("/content/cfg.yaml", encoding="utf-8"))
B = f"{REPO}/harness/dg1_cache/train_ac/branches"
loi = []

# 1 — cfg trỏ đúng nhánh, đúng hạt giống, không sót khoá thăm dò
print("① CẤU HÌNH")
print(f"   dataset {c['dataset']} · seed {c['seed']} · epoch {c['num_train_epochs']}")
print(f"   cỡ lô hiệu dụng {c['per_device_train_batch_size']*c['gradient_accumulation_steps']}"
      f" · cutoff {c['cutoff_len']} · workers {c.get('preprocessing_num_workers')}")
sot = [k for k in ("max_steps","max_samples","disable_gradient_checkpointing") if k in c]
if c["dataset"] != "gui_s2":  loi.append(f"dataset là {c['dataset']}, cần gui_s2")
if sot:                       loi.append(f"còn khoá thăm dò {sot}")
if c["per_device_train_batch_size"]*c["gradient_accumulation_steps"] != 16:
    loi.append("cỡ lô hiệu dụng khác 16")
if c.get("preprocessing_num_workers") != 8: loi.append("thiếu preprocessing_num_workers=8")
if c["cutoff_len"] != 2560:   loi.append(f"cutoff_len {c['cutoff_len']}, cần 2560")

# 2 — thư mục đích trên Drive phải RỖNG (lượt mới)
OUT = c["output_dir"]
ben_trong = sorted(os.listdir(OUT)) if os.path.isdir(OUT) else []
print(f"\n② ĐÍCH  {OUT}\n   bên trong: {ben_trong}")
if any(x.startswith("checkpoint-") for x in ben_trong):
    loi.append("output_dir đã có checkpoint — lượt MỚI sẽ chạy tiếp từ đó, không train từ đầu")

# 3 — dữ liệu nhánh: đúng tệp, đúng số mẫu
info = json.load(open(f"{B}/dataset_info.json", encoding="utf-8"))
fn = info[c["dataset"]]["file_name"]
rows = json.load(open(f"{B}/{fn}", encoding="utf-8"))
print(f"\n③ DỮ LIỆU  {fn} · {len(rows):,} mẫu")
if len(rows) != 64567: loi.append(f"{len(rows)} mẫu, cần 64.567")

# 4 — khai báo đã là tiếng Anh (kiểm dấu RIÊNG của tiếng Việt, bỏ é/à dùng chung)
import re
VI = re.compile(r"[ăâđêôơưảãạằắẳẵặầấẩẫậẻẽẹềếểễệỉĩịỏõọồốổỗộờớởỡợủũụừứửữựỳỷỹỵ]", re.I)
d = lambda x: (lambda m: m.group(1) if m else None)(
    re.search(r"<desc>(.*?)</desc>", x["messages"][-1]["content"], re.S))
xau = 0
for x in rows:
    t = d(x)
    if not t: continue
    p = [q.strip() for q in t.split("|")]
    if len(p) >= 4 and (VI.search(p[0]) or VI.search(p[3])): xau += 1
print(f"④ KHAI BÁO  tiếng Việt ở khuôn mẫu: {xau}")
if xau: loi.append(f"{xau} khai báo còn tiếng Việt ở khuôn mẫu")

# 5 — ĐƯỜNG DẪN ẢNH có thật không (nếu sai thì chết sau khi đã mã hoá token)
mau = random.Random(0).sample(rows, 300)
thieu = [x["images"][0] for x in mau if not os.path.exists(x["images"][0])]
print(f"⑤ ẢNH  mẫu 300 · thiếu {len(thieu)}")
if thieu:
    loi.append(f"{len(thieu)}/300 ảnh không mở được, ví dụ {thieu[0]}")
else:
    print(f"   ví dụ {mau[0]['images'][0]}")

# 6 — đĩa còn chỗ cho điểm lưu và bộ đệm
t, u, f = shutil.disk_usage("/content")
print(f"\n⑥ ĐĨA  còn {f/1e9:.0f} GB / {t/1e9:.0f} GB")
if f < 20e9: loi.append(f"đĩa chỉ còn {f/1e9:.0f} GB")

# 7 — số bước dự kiến
b = len(rows) * c["num_train_epochs"] / 16
print(f"\n⑦ DỰ KIẾN  {b:,.0f} bước · ~{b*10.4/3600:.1f} giờ train + ~0,7 giờ mã hoá + ghi điểm lưu")

print("\n" + "="*62)
print("✅ SẴN SÀNG — bấm ô 8" if not loi else "⛔ DỪNG:")
for x in loi: print("   ·", x)
```

| # | kiểm | vì sao |
|---|---|---|
| ① | cfg đúng nhánh · không sót `max_steps` · cỡ lô 16 · workers 8 | sót `max_steps` ⇒ train dừng sau 20 bước |
| ② | `output_dir` trên Drive **rỗng** | có `checkpoint-*` ⇒ **chạy tiếp** thay vì train từ đầu, log không báo |
| ③ | đúng tệp nhánh · **64.567** mẫu | sai tệp ⇒ train nhầm nhánh |
| ④ | khai báo tiếng Anh, **0** ở khuôn mẫu | tiếng Việt ⇒ `S2−S1` lẫn phần chuyển ngữ, không tách được |
| ⑤ | **đường dẫn ảnh mở được** | sai prefix ⇒ chết sau khi đã mã hoá token 42 phút |
| ⑥ | đĩa còn ≥20 GB | hết đĩa giữa chừng ⇒ mất điểm lưu đang ghi |
| ⑦ | ~8.072 bước · ~23,3 giờ | lệch nhiều ⇒ có gì đó sai ở cỡ lô hoặc số mẫu |

⑤ là phép đắt nhất trong bảy: đường dẫn ảnh **nướng cứng** vào bốn tệp nhánh lúc dựng, nên
đổi `WS` khỏi `/content/ws` là hỏng — và hỏng sau khi đã trả 42 phút mã hoá token.

## Ô 8 — TRAIN, chạy nền

```python
import subprocess, os
env = dict(os.environ, PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True")
f = open(LOG, "a")                       # ⚠️ "a" chứ không phải "w"
p = subprocess.Popen(["llamafactory-cli", "train", "/content/cfg.yaml"],
                     cwd=REPO, stdout=f, stderr=subprocess.STDOUT,
                     env=env, start_new_session=True)
print("đã khởi động, PID", p.pid, "→", LOG)
```

⏳ **~42 phút đầu KHÔNG có bước train nào** — mã hoá token 64.567 mẫu. Log chỉ có
`Running tokenizer on dataset`. **Không phải treo.**

## Ô 9 — đồng bộ log lên Drive mỗi 5 phút  ⚠️ chạy ngay sau ô 8

```python
import os, threading, time, shutil
DST = f"{D}/logs/{BRANCH}_seed{SEED}"
os.makedirs(DST, exist_ok=True)
shutil.copy("/content/cfg.yaml", DST)          # bằng chứng "chỉ khác ba dòng"
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

⚠️ Bắt lỗi vào `sync.err` chứ **không nuốt bằng `2>/dev/null`** — bản phiên 0 từng nuốt và
không ai biết đồng bộ đã chết.

## Ô 10 — theo dõi (chạy lại nhiều lần, an toàn)

```python
import json, os, time, glob
lg = sorted(glob.glob("/content/train_*.log"))[-1]
tuoi = time.time() - os.path.getmtime(lg)
print(f"[{time.strftime('%H:%M:%S')}] log cập nhật {tuoi:.0f} giây trước",
      "← sống" if tuoi < 120 else "← ⚠️ IM QUÁ LÂU, chạy ô chẩn đoán")
tl = f"{OUT}/trainer_log.jsonl"
if os.path.exists(tl):
    d = [json.loads(l) for l in open(tl, encoding="utf-8")]
    x = d[-1]                                    # ⚠️ DÒNG CUỐI, đừng lọc theo ngưỡng bước
    print(f"  bước {x['current_steps']}/{x['total_steps']} · loss {x.get('loss')} "
          f"· lr {x.get('lr')}")            # ⚠️ 'lr', KHÔNG phải 'learning_rate'
    print(f"  điểm lưu: {sorted(os.path.basename(p) for p in glob.glob(f'{OUT}/checkpoint-*'))}")
else:
    print("  chưa tới bước 1 — vẫn đang mã hoá token (~42 phút)")
```

**Sáu dấu hiệu, đều học được bằng cách mắc lỗi:**

· **Đọc DÒNG CUỐI.** Tệp ghi nối thêm, nên sau khi chạy tiếp, dòng mới đầu tiên có số bước
**thấp hơn** dòng cuối cũ. 💡 **Số bước tụt xuống là dấu hiệu TỐT** — phiên mới đã ghi thật.
· Chữ **`disconnect`** trên trình duyệt **không** phải bằng chứng máy chết. Bằng chứng thật là
dòng `log cập nhật … giây trước` ở trên.
· `grep "Resuming training from"` trống ngay sau ô 8 là **báo động giả** — dòng đó in sau ~40
giây nạp thư viện.
· Mốc ngó giữa chừng: **bước 4.036** = ranh giới lượt duyệt 2. Loss tụt một nấc ở đó là **bình
thường**. ⚠️ Đừng đọc thành "khái quát tốt hơn", và **đừng ngoại suy loss**.
· Tên trường là **`lr`**, không phải `learning_rate`; **không có `grad_norm`** (trường đó chỉ ở
dòng stdout). Đọc sai tên thì ra `None` và tưởng lịch học hỏng.
· **Đừng in `remaining_time` của trainer** — nó, cùng `elapsed_time`, **hỏng sau khi chạy tiếp**
(tính từ lúc phiên này khởi động, không phải từ bước 0). Ô 10b tự tính bằng mốc neo.

## Ô 10b — THEO DÕI LIÊN TỤC (thêm 18/8)  ⚠️ dán vào ô mới sau ô 9

Ô 10 là ảnh chụp một lần, phải bấm lại mỗi lần muốn xem. Ô này chạy vòng lặp. Bấm ⏹ để dừng
**ô này**; train **không** chết theo, vì ô 8 phóng bằng `start_new_session=True` nên tiến trình
đã rời hẳn nhân Python.

```python
import json, os, time, glob, math

os.environ["TZ"] = "Asia/Ho_Chi_Minh"; time.tzset()   # ⚠️ Colab chạy giờ UTC, lệch 7 tiếng

NHIP, NHIP_IM = 60, 300      # nhịp hỏi · nhịp in lại khi bước không đổi
LR0, WARM     = 1.0e-4, 0.05 # khớp train_config.yaml: learning_rate · warmup_ratio, cosine
NGUONG_SB     = 11.5         # A100 đã đo 10,2; vượt mốc này là chậm bất thường
RANH_EPOCH    = 4036         # ranh giới lượt duyệt 2 — tb10 tụt một nấc ở đây là BÌNH THƯỜNG

tl, t0 = f"{OUT}/trainer_log.jsonl", time.time()
truoc, lan_in = None, 0
gio = lambda: time.strftime("%H:%M:%S")
hms = lambda s: f"{int(max(s,0))//3600}h{(int(max(s,0))%3600)//60:02d}m"
so  = lambda x, n=4: "—" if x is None else f"{x:.{n}f}".replace(".", ",")
sod = lambda x, n=4: "—" if x is None else f"{x:+.{n}f}".replace(".", ",")
ng  = lambda n: f"{n:,}".replace(",", ".")

def giay(t):                              # "6:24:50" · "1 day, 2:03:04" · số
    try:
        if isinstance(t, (int, float)): return float(t)
        p = str(t).split(", ")[-1].split(":")
        return sum(float(v)*m for v, m in zip(reversed(p), (1, 60, 3600)))
    except Exception: return None

def doc():
    """Chuỗi bước TĂNG NGẶT.
    trainer_log.jsonl ghi NỐI THÊM, nên sau khi chạy tiếp nó còn dòng của phiên
    cũ với số bước CAO HƠN chỗ đang chạy (phiên trước chết ở 4.740 trong khi
    điểm lưu là 4.600). Lấy max hay sort theo bước thì ô này in 4.740 đứng yên
    suốt ~24 phút, trông y hệt train đang chạy. Nên: gặp bước tụt thì VỨT mọi
    dòng ≥ nó — đó là dòng của phiên đã chết."""
    h = []
    for l in open(tl, encoding="utf-8"):
        try: r = json.loads(l)
        except Exception: continue
        if r.get("loss") is None: continue
        while h and h[-1]["current_steps"] >= r["current_steps"]: h.pop()
        h.append(r)
    return h

def toc_do(h, tran=None):
    """s/bước đọc từ elapsed_time của TRAINER, không đụng đồng hồ tường ⇒ không
    dính trễ hỏi 60 giây. Chỉ đi trong CÙNG phiên: elapsed đếm lại từ 0 sau mỗi
    lần chạy tiếp, nên chỗ nó thôi tăng chính là mốc resume. `tran` giới hạn cửa
    sổ để đo nhịp GẦN ĐÂY."""
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
    """lr mà lịch cosine LẼ RA phải cho. Đã hiệu chuẩn trên 8 điểm thật của lượt
    s2: HF dùng ceil cho warmup và ghi lr của bước b−1 ⇒ lệch 0,013% thay vì 0,10%."""
    w, b = math.ceil(WARM * tong), b - 1
    if b <= w: return LR0 * b / max(w, 1)
    return LR0 * 0.5 * (1 + math.cos(math.pi * (b - w) / (tong - w)))

print(f"[{gio()}] theo dõi {OUT} · nhịp {NHIP}s · ⏹ để dừng ô này (train KHÔNG chết theo)",
      flush=True)

while True:
    try:
        lg   = sorted(glob.glob("/content/train_*.log"))[-1]
        tuoi = time.time() - os.path.getmtime(lg)
        with open(lg, "rb") as f:                    # đuôi log, để phân biệt mã hoá token
            f.seek(max(0, os.path.getsize(lg) - 4000)); duoi = f.read().decode("utf-8", "ignore")

        h = doc() if os.path.exists(tl) else []
        if not h:
            print(f"[{gio()}] chưa có bước nào — mã hoá token ({hms(time.time()-t0)} rồi, ~42 phút)"
                  f" · log {tuoi:.0f}s trước", flush=True)
            time.sleep(NHIP); continue

        x, b, tong = h[-1], h[-1]["current_steps"], h[-1]["total_steps"]
        # Dòng cuối được ghi bao lâu rồi? Lúc train chạy, trainer ghi mỗi 20 bước
        # (~205 s). Cũ hơn 5 phút ⇒ KHÔNG có bước nào đang chạy, dù .log vẫn nhúc
        # nhích: hoặc đang mã hoá token sau khi chạy tiếp, hoặc treo. Không có phép
        # này thì ô in số bước của phiên TRƯỚC kèm giờ xong rất hợp lý — suốt 42 phút.
        tuoi_tl = time.time() - os.path.getmtime(tl)
        dung = tuoi_tl > 300
        canh = (b != truoc) or (time.time() - lan_in > NHIP_IM) \
               or (tuoi > 180 and time.time() - lan_in > 120)
        if canh:
            # ── tốc độ: hai cửa sổ, cả hai đều CHÍNH XÁC vì đọc từ elapsed_time ──
            sb, n_b   = toc_do(h)                    # cả phiên → dùng cho giờ xong
            sb_g, n_g = toc_do(h, 400)               # 400 bước gần đây → bắt chậm dần
            if dung:
                ly_do = ("⏳ đang mã hoá token (~42 phút), số dưới là của phiên TRƯỚC"
                         if "Running tokenizer" in duoi or "Converting format" in duoi
                         else "⚠️ KHÔNG ghi bước nào — nghi treo, chạy ô chẩn đoán")
                toc = f" · dòng cuối {tuoi_tl/60:.0f} phút trước · {ly_do}"
            elif sb:
                canh_bao = " ⚠️ CHẬM BẤT THƯỜNG" if sb_g and sb_g > NGUONG_SB else ""
                if sb_g and sb and sb_g > sb * 1.15: canh_bao += " ⚠️ đang chậm dần"
                toc = (f" · {so(sb,2)} s/bước trên {ng(n_b)} bước"
                       f" (gần đây {so(sb_g,2)} trên {ng(n_g)}){canh_bao or ' ✅'}"
                       f" · còn {hms((tong-b)*sb)}"
                       f" → xong ~{time.strftime('%H:%M %d/%m', time.localtime(time.time()+(tong-b)*sb))}")
            elif "Running tokenizer" in duoi or "Converting format" in duoi:
                toc = " · ⏳ đang mã hoá token, chưa có bước mới của phiên này"
            else:
                toc = " · chưa đủ hai mốc để tính tốc độ"

            # ── tb10 = 10 điểm log cuối (=200 bước). Cửa sổ 200 bước là NHIỄU ở đuôi
            #    lịch (mức trôi thật ~0,004 ≈ nhiễu của chính tb10) ⇒ phán quyết lấy
            #    từ cửa sổ 1.000 bước. ────────────────────────────────────────────
            tb  = lambda a, z: (sum(r["loss"] for r in h[a:z]) / 10) if len(h[a:z]) == 10 else None
            tb10, tb_gan, tb_xa = tb(-10, None), tb(-20, -10), tb(-60, -50)
            xu = f"· so 200 bước {sod(tb10-tb_gan) if tb_gan else '—'} (nhiễu, đừng đọc) "
            if   tb_xa is None:         xu += "· chưa đủ 1.000 bước để so"
            elif tb10 <= tb_xa + 0.010: xu += f"· so 1.000 bước {sod(tb10-tb_xa)} ✅ giảm chậm / phẳng"
            else:                       xu += f"· so 1.000 bước {sod(tb10-tb_xa)} ⚠️ TĂNG THẬT — ngó lại"

            # ── lr có bám lịch không ─────────────────────────────────────────────
            lr, lk = x.get("lr"), lr_lich(b, tong)
            dl  = abs(lr - lk) / lk * 100 if lr is not None else None
            slr = (f"{lr:.3e} · lịch {lk:.3e} · lệch {so(dl,3)}% "
                   f"{'✅' if dl < 0.2 else '⚠️ SAI LỊCH'}") if dl is not None else "— (thiếu trường lr)"

            # ── điểm lưu mới nhất: bằng chứng máy còn sống, xem được từ điện thoại ──
            ck  = sorted(glob.glob(f"{OUT}/checkpoint-*"), key=lambda q: int(q.rsplit("-",1)[1]))
            sck = "chưa có"
            if ck:
                tck = (time.time() - os.path.getmtime(ck[-1])) / 60
                sck = f"{os.path.basename(ck[-1])} ({tck:.0f} phút trước {'✅' if tck < 45 else '⚠️'})"

            ep = "\n          ⚠️ sát bước 4.036 = ranh giới lượt duyệt 2 — tb10 tụt một nấc ở đây" \
                 " là BÌNH THƯỜNG, không phải khái quát tốt hơn" if abs(b - RANH_EPOCH) <= 200 else ""
            print(f"[{gio()}] bước {ng(b)}/{ng(tong)} ({100*b/tong:.1f}%){toc}\n"
                  f"          loss {so(x['loss'])} (một lô, nhiễu ±0,10) · tb10 {so(tb10)} {xu}\n"
                  f"          lr {slr} · lưu {sck} · log {tuoi:.0f}s trước"
                  f" {'✅' if tuoi < 180 else '⚠️ IM QUÁ LÂU'}{ep}", flush=True)
            lan_in = time.time()
        truoc = b
    except Exception as e:
        print(f"[{gio()}] ⚠️ {type(e).__name__}: {e}", flush=True)
    time.sleep(NHIP)
```

**Đọc năm con số — bảng này là phần quan trọng hơn cả đoạn mã.**

| con số | mốc tốt | đọc thế nào |
|---|---|---|
| **s/bước** | **10,2–10,4** (A100) | S2 đo được 10,22 · S1 10,29–10,38. Vọt lên >12 mà vẫn A100 ⇒ có gì đó tranh card hoặc đĩa chậm, ngó lại. Thấp hơn hẳn ⇒ nghi nó **nhảy qua** lô chứ không train (94 lô/giây lúc chạy tiếp) |
| **loss** (một lô) | nhảy ±0,10 là **bình thường** | Đây là loss của **một lô 16 mẫu**, biên độ đo được **0,103**. Nhìn nó lên xuống rồi kết luận "mô hình trồi sụt" là đọc nhiễu. **Đừng quyết định gì dựa trên dòng này.** |
| **tb10** (10 điểm log cuối = 200 bước) | giảm hoặc đi ngang | Biên độ chỉ **0,0215**, hẹp hơn loss ~5 lần (đúng quy luật √10) ⇒ đây mới là đường thật. Nhích lên trong 0,02 là nhiễu; **tăng đều 3-4 nấc liên tiếp** mới đáng dừng lại xem |
| **lr** | lệch lịch cosine **<1%** | Ô tự tính lr mà lịch `cosine` + `warmup_ratio 0.05` lẽ ra phải cho ở bước đó rồi so. Đã kiểm thật ở bước 2.260: lịch 8,622e-05 · trainer ghi 8,624e-05, **lệch 0,02%**. Lệch lớn ⇒ cfg bị đổi hoặc nó đang chạy lịch của lượt khác |
| **lưu** | bản mới **< 34 phút** | `save_steps: 200` × 10,2 s = ~34 phút. Đây là **bằng chứng máy còn sống** mạnh hơn mọi thứ hiện trên trình duyệt — xem được từ Google Drive trên điện thoại |

**Bốn cách đọc sai, đều đã mắc thật:**

· ⛔ **ĐỪNG so loss của S2 với loss của S1.** S2 đang ~0,39 ở bước 2.260 trong khi S1 ~0,61 ở
bước 2.000 — **không** phải S2 học tốt hơn. Đích của S2 có thêm dòng `<desc>` dựng **bằng
luật** từ cây trợ năng + OCR, tức phần dễ đoán hơn hẳn văn tự do, nên loss thấp hơn là **tất
yếu về mặt số học**. Hai nhánh có đích khác nhau thì loss **không so được**. Câu trả lời
S2-hơn-S1 hay không chỉ đến từ **executability chấm trên câu sau khi cắt bỏ `<desc>`**, ngưỡng
đã khoá ở cuối file.
· ⛔ **Đừng ngoại suy loss.** Dự báo sàn 0,548 hồi 12/8 đã bị rút — mới tới bước 5.100 đã 0,465.
· **Bước 4.036 = ranh giới lượt duyệt 2**, tb10 tụt một nấc ở đó là bình thường (S1: 0,54–0,575
→ 0,495 → 0,465). ⚠️ Đó là *gặp lại dữ liệu lần hai*, **không** phải bằng chứng khái quát tốt
hơn. Ô tự dán cảnh báo khi tới gần.
· **Đuôi lịch phẳng là kết thúc sạch, không phải chững vì hỏng.** Từ 6.060 → 7.840 của S1, tb10
chỉ đi 0,4712 → 0,4554 trong khi lr tụt 1,61e-05 → **2,28e-07**.


**Sáu chỗ nó khác ô 10 — mỗi chỗ là một cách đọc sai đã bắt được bằng log dựng lại:**

· ⭐ **Vứt dòng của phiên đã chết.** `trainer_log.jsonl` **ghi nối thêm**, mà điểm lưu luôn đi
sau log tới 180 bước (`save_steps: 200` vs `logging_steps: 20`). Phiên trước chết ở 4.740 nhưng
chạy tiếp từ **4.600** ⇒ trong tệp có sẵn dòng 4.620…4.740 của phiên cũ, **số bước cao hơn chỗ
đang chạy thật**. Lấy `max` hay `sort` theo bước là ô in **4.740 đứng yên ~24 phút** kèm giờ
xong rất hợp lý. Nay gặp bước tụt thì **vứt mọi dòng ≥ nó**.
· ⭐ **Tốc độ đọc từ `elapsed_time` của trainer, không đụng đồng hồ tường.** Ô hỏi 60 giây/lần
còn trainer ghi mỗi 20 bước (~205 giây) ⇒ trễ ngẫu nhiên tới 60 giây ở **cả hai đầu** cửa sổ,
cho răng cưa 9,00 ↔ 10,50 s/bước và giờ xong nhảy một tiếng. Đọc từ log thì hết trễ, **có số
ngay từ dòng đầu**, và tự dò mốc resume (elapsed đếm lại từ 0). In hai cửa sổ: cả phiên (dùng
cho giờ xong) và **400 bước gần đây** (bắt chậm dần).
· ⭐ **Phân biệt *đang mã hoá token* với *treo*, bằng mtime của `trainer_log.jsonl`.** Lúc train
chạy, tệp này được ghi mỗi ~205 giây. Cũ hơn **5 phút** ⇒ không có bước nào đang chạy, dù
`.log` vẫn nhúc nhích. Không có phép này thì suốt 42 phút mã hoá token sau mỗi lần chạy tiếp,
ô in số bước của **phiên trước** kèm giờ xong đẹp đẽ.
· **`lr` so với lịch đã hiệu chuẩn.** HF dùng `ceil` cho warmup (**404** bước) và ghi `lr` của
bước **b−1**; khớp đúng hai điều đó thì lệch tụt **0,100% → 0,013%** trên 8 điểm thật ⇒ ngưỡng
cảnh báo siết được xuống **0,2%**, đủ nhạy để bắt việc chạy nhầm lịch.
· **Nhật ký cuộn, `flush=True`, CẤM `clear_output`.** In khi bước đổi, mỗi 5 phút khi đứng yên,
và **ngay lập tức** khi log im quá 3 phút.
· **Bọc `try` + đặt `TZ=Asia/Ho_Chi_Minh`.** Mất gắn Drive thì in một dòng lỗi rồi hỏi tiếp,
không chết ô. Colab chạy giờ **UTC** — không đặt múi giờ thì `xong ~08:15` sớm hơn thực tế
**7 tiếng**, vô tình trông giống lượt train chạy nhanh.

**Bản chạy từ Terminal Colab** (biểu tượng `>_` góc dưới trái) — độc lập hoàn toàn với nhân
Python, dùng khi nhân bận hoặc vừa restart:

```bash
OUT=/content/drive/MyDrive/thesis/ckpt/s2_seed101
while true; do
  printf '[%s] ' "$(date +%H:%M:%S)"
  tail -1 $OUT/trainer_log.jsonl 2>/dev/null || echo "chưa có — đang mã hoá token"
  sleep 60
done
```

💡 Rẻ nhất khi trình duyệt báo *Connecting*: mở **Google Drive trên điện thoại**, xem thư mục
`thesis/ckpt/s2_seed101` — có bản mới trong vòng **~34 phút** (200 bước × 10,2 s) là máy sống.

---

## Nếu phiên đứt giữa chừng

Chạy lại: **ô 1 → Restart → ô 2 → ô 3 → ô 4 → ô 5 → ô 5c → ô 7b → ô 8 → ô 9 → ô 10b.**
Bỏ ô 6 (đã thăm dò) và ô 7 (cfg không đổi).

⚠️ **Đừng bỏ ô 4.** Máy ảo mới thì bộ đệm HuggingFace rỗng, LLaMA-Factory phải tải lại trọng
số Qwen2.5-VL-3B; không có `HF_TOKEN` là chết ở khâu nạp mô hình. Mất 5 giây.

⚠️ **Đừng bỏ ô 7b.** Ô 2 bung `derived.tar.gz` — bản **tiếng Việt** — nên mỗi lần dựng lại máy
là dữ liệu có nguy cơ lùi về bản cũ. Ô 2 đã tự bung đè `derived_train_en.tar.gz`, và phép ④ của
ô 7b là chỗ **xác nhận bằng số** (`tiếng Việt ở khuôn mẫu: 0`). Phép ② của ô 7b sẽ kêu
*"output_dir đã có checkpoint"* — ở lần chạy tiếp thì đó là **ĐÚNG**, bỏ qua đúng dòng đó.

Ô 5 phải in `BÊN TRONG output_dir` **CÓ `checkpoint-*`** — LLaMA-Factory tự chạy tiếp từ đó.
Dòng chú thích `← lượt MỚI phải là []` **không áp cho lần chạy tiếp**; ở đây thấy rỗng mới là
hỏng. ⛔ **Đừng xoá `output_dir`** (đoạn `shutil.rmtree(OUT)` ở ô 5 chỉ dành cho lượt mới), và
⛔ **đừng điền gì vào `resume_from_checkpoint`**, kể cả `"auto"` — điền là **tắt** đúng cái nó
định bật. ⛔ **Đừng chạy lại ô 6** — nó không xoá `output_dir` nên sẽ chạy tiếp từ chính điểm
lưu này. Phần train đã làm **không mất**; giá một lần đứt là ~42 phút mã hoá token cộng phần
bước từ điểm lưu cuối tới lúc chết (≤200 bước ≈ 34 phút).

**Ô 5c nằm ở trên, ngay trước ô 6** — sao lưu `checkpoint-*` sang `ckpt_backup/`.

**Kiểm nó có chạy tiếp thật không.** Sau ô 8 khoảng 40 giây, từ Terminal Colab:
`grep -m1 "Resuming training from" /content/train_s2_seed101.log`. Trống **ngay lúc đầu** là
báo động giả (log chưa ghi gì trong ~40 giây nạp thư viện) — hỏi `ps -p <PID>` và cỡ log trước
khi kết luận. Bằng chứng chắc nhất nằm ở ô 10b: dòng đầu của phiên mới có số bước **thấp hơn**
dòng cuối cũ, vì nó bằng điểm-lưu + `logging_steps`.

---

## Xong lượt 101

1. Xem 20 câu sinh thử (ô A.7 của `run_on_colab.md`). **Nhìn `<desc>` có đúng khuôn không** —
   khai báo lệch định dạng thì khâu cắt bỏ nó lúc chấm sẽ hỏng mà không báo gì.
2. Sinh đủ 6.958 câu (ô A.8, ~1,5 giờ).
3. Lưu vết lên Drive (ô A.10) **trước khi tắt máy**.
4. Tải `preds_s2_seed101.jsonl` về máy nhà, chạy:
   `python3 harness/kiem_preds.py runs/preds_s2_seed101.jsonl`
   → phải **8/8 ĐẠT**, bước bỏ **trùng khít** `[(18710, 1)]` như S1.
5. Đổi `SEED = 202` ở ô 5, chạy lại từ ô 5.

**Chấm để cuối cùng**, sau khi có cả hai hạt giống — Kaggle 30 giờ/tuần, mỗi lượt 5,6 giờ.

## Luật đọc kết quả — đã khoá 17/8, đừng sửa sau

Δ = S2 − S1, trung bình hai hạt giống, ghép cặp (`report/106` mục sửa đổi (w)):

| Δ | kết luận |
|---|---|
| **≥ +2,8 pp**, KTC95 loại trừ 0 | **DƯƠNG** |
| +1,7 … +2,8 pp, KTC loại trừ 0 | **DƯƠNG YẾU** — không đưa vào abstract |
| −2,8 … +1,7 pp | **TRẮNG** — kết quả âm có kiểm soát |
| ≤ −2,8 pp | **ÂM** — báo thẳng |

Báo kèm bắt buộc: bốn con số riêng lẻ · tỉ lệ bước bất đồng (mốc: null **6,4%** · can thiệp
thật **24%**) · phân tầng theo độ dài câu. Hai hạt giống S2 lệch nhau **> 1,5 pp** thì **dừng
lại truy nguyên nhân** trước khi đọc Δ.
