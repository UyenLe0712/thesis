# Chạy trên Colab Pro — runbook dán-là-chạy

> Thay cho `run_on_rented.sh` (bản đó cho máy thuê có SSH). Cùng trình tự, cùng luật, chỉ
> khác cách gõ lệnh.
>
> **Máy đã đo (9/8/2026):** A100 **80 GB** · đĩa 235,7 GB (trống ~148) · local-scratch
> **368 GB** chưa dùng · RAM 167 GB · đốt **6,77 đơn vị/giờ**.

---

## Ba nguyên tắc của runbook này

**1. Việc dài chạy nền, không chạy trong ô.** Mọi khâu trên 10 phút đều khởi động bằng
`nohup … > log &` rồi theo dõi bằng một ô nhẹ. Lý do: ô chạy 3 tiếng sẽ đổ hàng vạn dòng
vào trình duyệt cho tới lúc treo tab, mà tab treo giữa lúc OCR là mất cả khâu OCR.

**2. Sau mỗi khâu có một ô KIỂM in ra con số so được với con số đã biết.** Không có ô đó
thì "chạy xong" chỉ nghĩa là "không báo lỗi", mà 35 lỗi bắt được tới nay hầu hết đều
không báo lỗi.

**3. 🛑 Ở mỗi mốc DỪNG, dán output cho mình trước khi chạy tiếp.** Mốc dừng đặt ngay
trước những khâu đắt. Sai ở khâu rẻ mà chạy tiếp sang khâu đắt là cách tiêu tiền nhanh
nhất.

Có **6 mốc dừng**. Mỗi mốc ghi rõ dán cái gì.

---

## 0. Trước khi bật máy

| | |
|---|---|
| Mua đơn vị | ước **600-900**. Mua dư — hết units giữa lượt train là mất phiên |
| Drive | tạo `MyDrive/thesis/` — chỗ duy nhất sống sót qua các phiên |
| Tải lên Drive | `thesis_rented.zip` (3,3 MB) |
| Runtime | A100. **Kiểm lại mỗi phiên**, Colab hay tụt về L4 |

---

# PHIÊN 0 — dựng dữ liệu (một lần, ~4-6 giờ, ~35 đơn vị)

Phiên này gần như không dùng card, nhưng vẫn bật A100 cho cùng môi trường với các phiên
sau. Tách ra máy CPU chỉ tiết kiệm ~2 đô, không đáng thêm một biến khác biệt.

### Ô 0.1 — nhận diện máy

```python
import os, subprocess, torch, shutil
print("lõi CPU     :", os.cpu_count())
print("card        :", subprocess.run(["nvidia-smi","--query-gpu=name,memory.total","--format=csv,noheader"],
                                       capture_output=True,text=True).stdout.strip())
print("số card     :", torch.cuda.device_count())
print("bf16 thật   :", torch.cuda.get_device_capability()[0] >= 8)
print()
print(subprocess.run(["df","-h"],capture_output=True,text=True).stdout)
for d in ("/content", "/mnt/disks/local-scratch", "/mnt/local-scratch", "/tmp"):
    if os.path.isdir(d):
        t,u,f = shutil.disk_usage(d)
        print(f"  {d:28} trống {f/2**30:6.1f} GB / {t/2**30:6.1f} GB")
```

## 🛑 MỐC DỪNG 1 — dán toàn bộ output ô 0.1

Mình cần bốn thứ để chốt trước khi bạn tải 67 GB về nhầm chỗ:

- **số card** phải là 1. Khác 1 → phải đặt `CUDA_VISIBLE_DEVICES` và khởi động lại
- **tên card** phải có chữ A100. Ra L4/T4 → đổi runtime, đừng chạy tiếp
- **số lõi CPU** → quyết định OCR mất 1 giờ hay 5 giờ, và có nên tách khâu này ra máy khác không
- **local-scratch gắn ở đâu** → nếu có và rộng, để dữ liệu ở đó (NVMe, nạp ảnh lúc train
  nhanh hơn hẳn); nếu không thì dùng `/content`

Mình trả lời xong bạn mới chạy ô 0.2.

---

### Ô 0.2 — gắn Drive, bung mã

```python
from google.colab import drive; drive.mount('/content/drive')
import os, zipfile
D  = "/content/drive/MyDrive/thesis"
WS = "/content/ws"            # ⚠️ ĐỔI theo kết luận ở mốc dừng 1
os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_rented.zip").extractall(WS)
REPO = f"{WS}/thesis"; os.chdir(REPO)

print("script         :", len([f for f in os.listdir("harness") if f.endswith(".py")]), "(chờ 28)")
print("OCR tập kiểm   :", sum(1 for _ in open("harness/dg1_cache/test_ac/ocr.jsonl")), "(chờ 6969)")
print("tập kiểm       :", sum(1 for _ in open("harness/dg1_cache/test_ac/test.jsonl")), "(chờ 6958)")
print("nhãn tập kiểm  :", sum(1 for _ in open("harness/dg1_cache/test_ac/descriptors.jsonl")), "(chờ 4448)")
```

Bốn số phải khớp. Lệch bất kỳ số nào là gói tải lên Drive hỏng — tải lại, đừng chạy tiếp.

### Ô 0.3 — cài gói

```python
!pip install -q -U "transformers>=4.49" accelerate peft bitsandbytes datasets \
    huggingface_hub pyarrow pillow rapidocr_onnxruntime pyyaml
!git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory /content/LLaMA-Factory
!pip install -q -e "/content/LLaMA-Factory[torch,metrics]"
```

Xong → **Runtime → Restart session** → chạy lại **ô 0.2** (không cần 0.3 nữa).

### Ô 0.4 — tải ảnh tập dạy, chạy NỀN

```python
import os; os.chdir(REPO)
!nohup python harness/build_train_data.py --shards 76 > /content/build.log 2>&1 &
print("đã khởi động, theo dõi bằng ô kế")
```

### Ô 0.5 — theo dõi (chạy lại ô này nhiều lần, mỗi lần vài giây)

```python
import os, subprocess, shutil, time
n = len(os.listdir(f"{REPO}/harness/dg1_cache/train_ac/images")) if os.path.isdir(f"{REPO}/harness/dg1_cache/train_ac/images") else 0
alive = "build_train_data" in subprocess.run(["ps","-eo","args"],capture_output=True,text=True).stdout
f = shutil.disk_usage(WS)[2]/2**30
print(f"ảnh: {n:,} / ~64.500   ·   đĩa trống: {f:.1f} GB   ·   tiến trình: {'đang chạy' if alive else 'ĐÃ DỪNG'}")
!tail -3 /content/build.log
```

Chừng 20-40 phút. Đĩa trống **không được xuống dưới 15 GB** — nếu tụt nhanh về đó thì
dừng lại báo mình, vì mã xoá parquet sau mỗi shard nên đỉnh lẽ ra chỉ ~70 GB.

### Ô 0.6 — kiểm dữ liệu dạy vừa dựng

```python
import json, collections
T = f"{REPO}/harness/dg1_cache/train_ac"
recs = [json.loads(l) for l in open(f"{T}/train.jsonl", encoding="utf-8")]
taps = [r for r in recs if r["action"].get("action_type") in ("click","long_press") and "x" in r["action"]]
import os
print(f"bước       : {len(recs):,}      (ước từ 2 shard: ~64.500)")
print(f"bước chạm  : {len(taps):,} = {len(taps)/len(recs):.1%}   (lát 2 shard cho 63,3%)")
print(f"tác vụ     : {len({r['episode_id'] for r in recs}):,}")
print(f"ảnh        : {len(os.listdir(f'{T}/images')):,}")
print(f"thiếu ảnh  : {sum(1 for r in recs if not os.path.exists(os.path.join(T, r['image'])))}   ← phải là 0")
```

## 🛑 MỐC DỪNG 2 — dán output ô 0.6

Trước khi bỏ 3 tiếng CPU vào OCR, mình muốn chắc dữ liệu dạy đúng. Cần xem: tổng số bước
có gần 64.500 không, tỉ lệ bước chạm có quanh 63% không (lệch xa nghĩa là ghép sai), và
thiếu ảnh phải bằng 0.

---

### Ô 0.7 — OCR, chạy NỀN

```python
import os, subprocess
NP = min(os.cpu_count(), 24)
print("dùng", NP, "tiến trình")
cmd = " ".join(f"nohup python harness/prep_ocr_train.py --shard {k} --nshard {NP} > /content/ocr{k}.log 2>&1 &"
               for k in range(NP))
subprocess.run(cmd, shell=True, cwd=REPO)
print("đã khởi động", NP, "tiến trình")
```

### Ô 0.8 — theo dõi OCR (chạy lại nhiều lần)

```python
import glob, subprocess, time, json, os
done = sum(sum(1 for _ in open(p, encoding="utf-8")) for p in glob.glob(f"{REPO}/harness/dg1_cache/train_ac/ocr.part*.jsonl"))
tot  = sum(1 for _ in open(f"{REPO}/harness/dg1_cache/train_ac/train.jsonl", encoding="utf-8"))
alive = subprocess.run(["ps","-eo","args"],capture_output=True,text=True).stdout.count("prep_ocr_train")
print(f"OCR: {done:,} / {tot:,} = {done/tot:.1%}   ·   tiến trình sống: {alive}")
```

**Nhìn cột "tiến trình sống".** Nó phải giữ nguyên bằng `NP` cho tới gần cuối. Tụt dần
giữa chừng nghĩa là có tiến trình chết (thường do thiếu RAM) — dừng lại báo mình, đừng
để chạy tiếp rồi merge ra một tệp thiếu mà không ai biết.

Với 12 lõi mất ~2,8 giờ. Chạy lại vô hại: ảnh đã có kết quả thì bỏ qua.

### Ô 0.9 — gộp và KIỂM PHỦ

```python
!cd {REPO} && python harness/prep_ocr_train.py --merge
import json
T = f"{REPO}/harness/dg1_cache/train_ac"
ocr = {json.loads(l)["image"] for l in open(f"{T}/ocr.jsonl", encoding="utf-8")}
recs = [json.loads(l) for l in open(f"{T}/train.jsonl", encoding="utf-8")]
thieu = [r["image"] for r in recs if r["image"] not in ocr]
print(f"OCR: {len(ocr):,} ảnh · phủ {len(recs)-len(thieu):,}/{len(recs):,} bước = {1-len(thieu)/len(recs):.2%}")
print(f"THIẾU: {len(thieu)}   ← phải là 0")
if thieu: print("ví dụ:", thieu[:5], "→ chạy lại ô 0.7, nó chỉ làm phần thiếu")
```

**Đây là phép kiểm quan trọng nhất của phiên 0.** Merge từ các phần rời mà một tiến
trình chết sớm thì tệp gộp vẫn hợp lệ, chỉ thiếu vài nghìn ảnh — và những bước đó sẽ vào
huấn luyện với đầu vào **thiếu dòng chữ đọc được**, khác hẳn lúc chấm. Không có ô này thì
không đường nào phát hiện.

### Ô 0.10 — nhãn khai báo + bốn nhánh + tập kiểm

```python
!cd {REPO} && python harness/descriptor_label_build.py 2>&1 | tail -25
```

```python
!cd {REPO} && python harness/build_branch_data.py --img-prefix "{REPO}/harness/dg1_cache/train_ac/" 2>&1 | tail -12
!cd {REPO} && python harness/build_test_data.py --shards 9 2>&1 | tail -12
!cd {REPO} && python harness/tag_app_seen.py 2>&1 | tail -8
```

### Ô 0.11 — KIỂM 9 BẤT BIẾN của bốn nhánh

```python
import json, re
B = f"{REPO}/harness/dg1_cache/train_ac/branches"
d = {b: json.load(open(f"{B}/{b}.json", encoding="utf-8")) for b in ("s1","s2","s2r","s2_nopoint")}
cau  = lambda x: (lambda t: t.split("</desc>",1)[1].strip() if "</desc>" in t else t.strip())(x["messages"][-1]["content"])
desc = lambda x: (lambda m: m.group() if m else None)(re.search(r"<desc>.*?</desc>", x["messages"][-1]["content"], re.S))
n = len(d["s1"]); nd = sum(1 for x in d["s2"] if desc(x))
K = []
for b in ("s2","s2r","s2_nopoint"):
    K.append((f"câu {b} trùng s1", sum(1 for x,y in zip(d[b],d["s1"]) if cau(x)==cau(y)), n))
K.append(("s1 KHÔNG có khai báo", sum(1 for x in d["s1"] if desc(x) is None), n))
for b in ("s2","s2r","s2_nopoint"):
    K.append((f"số khai báo {b}", sum(1 for x in d[b] if desc(x)), nd))
K.append(("s2_nopoint sót <point>", sum(1 for x in d["s2_nopoint"] if desc(x) and "<point>" in desc(x)), 0))
K.append(("s2r khác s2 ở bước có desc", sum(1 for x,y in zip(d["s2r"],d["s2"]) if desc(x) and desc(y) and desc(x)!=desc(y)), nd))
bad = 0
for nm, got, want in K:
    ok = got == want; bad += not ok
    print(f"  {'ĐẠT' if ok else 'RỚT'}  {nm:30} {got:,}" + ("" if ok else f"  ≠ {want:,}"))
print(f"\n{n:,} mẫu mỗi nhánh · {nd:,} khai báo · " + ("TẤT CẢ ĐẠT" if not bad else f"{bad} BẤT BIẾN RỚT"))
```

### Ô 0.11b — RÒ RỈ giữa tập dạy và tập kiểm ⚠️ ô quan trọng nhất phiên 0

```python
import json
TR = f"{REPO}/harness/dg1_cache/train_ac/train.jsonl"
TE = f"{REPO}/harness/dg1_cache/test_ac/test.jsonl"
etr = {json.loads(l)["episode_id"] for l in open(TR, encoding="utf-8")}
ete = {json.loads(l)["episode_id"] for l in open(TE, encoding="utf-8")}
chung = etr & ete
print(f"tác vụ trong tập dạy : {len(etr):,}")
print(f"tác vụ trong tập kiểm: {len(ete):,}")
print(f"TRÙNG NHAU           : {len(chung)}   ← PHẢI LÀ 0")
if chung: print("   ví dụ:", sorted(chung)[:10])
```

**Nếu ra khác 0 thì DỪNG TOÀN BỘ, đừng train.** Mô hình học đúng những tác vụ sẽ đem chấm
thì mọi con số về sau đều vô nghĩa, và đây là lỗi không có cách nào chữa sau khi đã train.

Cho tới nay "0 tác vụ trùng" mới **chỉ kiểm trên lát 2 shard**. Ở quy mô 76 shard chưa ai
kiểm. Hai tập lấy từ `train-*.parquet` và `test-*.parquet` nên *lẽ ra* rời nhau, nhưng
"lẽ ra" không phải bằng chứng — và đây là loại sai không sửa được sau khi phát hiện.

### Ô 0.11c — phép ghép ảnh ↔ câu chuẩn còn đúng ở quy mô đủ không

```python
!cd {REPO} && python harness/build_train_data.py --check 2>&1 | tail -5
```

Đọc chữ quanh điểm chạm rồi so với câu chuẩn, đối chứng bằng ghép lệch một bước. Lát 2
shard cho **47% so với 27%**. Ra chênh dưới 1,4 lần là ghép sai ở đâu đó — dừng, báo mình.

### Ô 0.11d — phân bố nhãn ứng dụng

```python
import json, collections
c = collections.Counter(json.loads(l).get("app_seen_in_train")
                        for l in open(f"{REPO}/harness/dg1_cache/test_ac/test.jsonl", encoding="utf-8"))
tot = sum(c.values())
for k, v in c.most_common():
    ten = {True: "app ĐÃ thấy lúc dạy", False: "app CHƯA thấy", None: "không gán được app"}[k]
    print(f"  {ten:22} {v:6,} = {v/tot:5.1%}")
```

Nhóm `False` chính là **lát cắt phụ đã đăng ký**. Con số này quyết định lát đó có đủ mẫu
để báo hay không — dưới ~100 bước chạm thì phải khai là quá nhỏ, không kết luận được.

## 🛑 MỐC DỪNG 3 — dán output ô 0.9, 0.10, 0.11, 0.11b, 0.11c, 0.11d

Đây là mốc **quan trọng nhất trước khi tiêu tiền thật**. Sau mốc này là 11-18 giờ train.
Mình cần đối chiếu:

- **phủ OCR** phải 100%
- **thống kê nhãn khai báo**: tên rõ ~74% · không tên ~23% · vai trò rõ ~76% · trùng tên
  ~7% · có hàng xóm ~92%. Lệch xa mấy con số này (đo trên lát 1.697 và trên tập kiểm
  4.448, hai lần đều khớp nhau) nghĩa là khâu dựng nhãn hỏng ở quy mô lớn
- **9 bất biến** phải đạt cả 9. Rớt một cái là bốn nhánh không so được với nhau
- **rò rỉ (ô 0.11b) phải bằng 0** — đây là điều kiện sống còn, sai là bỏ cả luận văn
- **phép ghép (ô 0.11c)** chênh phải trên 1,4 lần
- **phân bố `app_seen_in_train`** — quyết định lát cắt phụ có đủ mẫu để báo hay không

---

### Ô 0.12 — cất lên Drive ⚠️ ĐỪNG BỎ QUA

```python
import os
os.makedirs(f"{D}/ckpt", exist_ok=True); os.makedirs(f"{D}/preds", exist_ok=True)
!cd {REPO} && tar czf {D}/derived.tar.gz \
    harness/dg1_cache/train_ac/ocr.jsonl harness/dg1_cache/train_ac/train.jsonl \
    harness/dg1_cache/train_ac/descriptors.jsonl harness/dg1_cache/train_ac/branches \
    harness/dg1_cache/test_ac/ocr.jsonl harness/dg1_cache/test_ac/test.jsonl \
    harness/dg1_cache/test_ac/descriptors.jsonl
!cd {REPO}/harness/dg1_cache/train_ac && tar cf {D}/train_images.tar images
!cd {REPO}/harness/dg1_cache/test_ac  && tar cf {D}/test_images.tar images
!ls -lh {D}/*.tar*
```

`derived.tar.gz` là ~3 giờ CPU đóng thành một tệp. Hai tệp ảnh để các phiên sau chép một
tệp lớn thay vì tải lại 85 shard — nhanh hơn và không phụ thuộc HuggingFace còn sống.

**Điều kiện kết thúc phiên 0:** ba tệp nằm trên Drive, mốc dừng 3 đã qua. **Tắt máy.**

---

# PHIÊN TRAIN — mỗi nhánh × mỗi hạt giống một phiên

### Ô A.1 — khôi phục

```python
from google.colab import drive; drive.mount('/content/drive')
import os, zipfile, torch
D, WS = "/content/drive/MyDrive/thesis", "/content/ws"
os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_rented.zip").extractall(WS)
REPO = f"{WS}/thesis"; os.chdir(REPO)
!tar xzf {D}/derived.tar.gz -C {REPO}
!tar xf {D}/train_images.tar -C {REPO}/harness/dg1_cache/train_ac
!tar xf {D}/test_images.tar  -C {REPO}/harness/dg1_cache/test_ac
print("card :", torch.cuda.get_device_name(0), "| số card:", torch.cuda.device_count(),
      "| bf16 thật:", torch.cuda.get_device_capability()[0] >= 8)
print("ảnh dạy :", len(os.listdir(f"{REPO}/harness/dg1_cache/train_ac/images")))
print("ảnh kiểm:", len(os.listdir(f"{REPO}/harness/dg1_cache/test_ac/images")))
```

**Card không phải A100 thì DỪNG PHIÊN.** Đổi runtime hoặc chờ lúc khác. Train trên L4
với cỡ lô khác là hỏng cả bảng ablation, mà nhìn bảng không thấy.

Rồi cài gói (ô 0.3) → **Restart session** → chạy lại ô A.1.

### Ô A.2 — sinh cấu hình

```python
import yaml, os
BRANCH, SEED = "s1", 101        # ⚠️ ĐỔI ĐÚNG HAI GIÁ TRỊ NÀY, không đụng gì khác
OUT = f"{D}/ckpt/{BRANCH}_seed{SEED}"      # ← trên DRIVE, không phải /content
os.makedirs(OUT, exist_ok=True)
c = yaml.safe_load(open(f"{REPO}/harness/train_config.yaml", encoding="utf-8"))
c.update({"dataset": f"gui_{BRANCH}", "seed": SEED, "output_dir": OUT,
          "dataset_dir": f"{REPO}/harness/dg1_cache/train_ac/branches"})
yaml.safe_dump(c, open("/content/cfg.yaml","w",encoding="utf-8"), allow_unicode=True, sort_keys=False)
eff = c["per_device_train_batch_size"] * c["gradient_accumulation_steps"]
print(f"nhánh {BRANCH} · hạt giống {SEED} · cỡ lô hiệu dụng {eff}  ← phải là 16 ở MỌI lượt")
print(f"bf16 {c['bf16']} · epoch {c['num_train_epochs']} · lưu điểm mỗi {c['save_steps']} bước")
print(f"output_dir {c['output_dir']}")
```

### Ô A.3 — THĂM DÒ 20 BƯỚC trước khi cam kết 15 giờ

```python
import yaml
p = yaml.safe_load(open("/content/cfg.yaml", encoding="utf-8"))
p.update({"max_steps": 20, "output_dir": "/content/probe", "save_steps": 10000, "logging_steps": 5})
yaml.safe_dump(p, open("/content/probe.yaml","w",encoding="utf-8"), allow_unicode=True, sort_keys=False)
```
```python
!llamafactory-cli train /content/probe.yaml > /content/probe.log 2>&1; tail -25 /content/probe.log
```
```python
import re
L = open("/content/probe.log", encoding="utf-8", errors="ignore").read()
tp = re.search(r"Number of trainable parameters = ([\d,]+)", L)
bs = re.search(r"Total train batch size[^=]*= (\d+)", L)
sp = re.findall(r"([\d.]+)s/it", L) or re.findall(r"([\d.]+)it/s", L)
oom = "out of memory" in L.lower()
print("tham số huấn luyện :", tp.group(1) if tp else "KHÔNG THẤY", " ← chờ 14,966,784")
print("cỡ lô hiệu dụng    :", bs.group(1) if bs else "KHÔNG THẤY", " ← chờ 16")
print("tốc độ             :", sp[-3:] if sp else "?")
print("tràn bộ nhớ        :", "CÓ ← dừng, báo mình" if oom else "không")
```

Ô này trả lời ba câu **trước** khi đồng hồ chạy 15 tiếng:

- có tràn bộ nhớ ở cỡ lô này không
- **bao nhiêu giây mỗi bước** → nhân với tổng số bước ra thời gian thật, ra số đơn vị thật
- số tham số huấn luyện có đúng **14.966.784** không (nếu khác: LoRA gắn sai chỗ, hoặc
  tháp thị giác không được đóng băng)

## 🛑 MỐC DỪNG 4 — dán output ô A.2 và A.3

Mình tính giúp: tổng số bước = `số mẫu × 2 epoch ÷ 16`, nhân với giây-mỗi-bước ra giờ,
nhân 6,77 ra đơn vị. Nếu ra nhiều hơn số units bạn còn thì phải quyết trước — mua thêm,
hay hạ xuống 1 epoch (và ghi vào bản đăng ký) — chứ không phải phát hiện lúc đang chạy
dở giờ thứ mười.

Cũng là chỗ mình xác nhận cỡ lô hiệu dụng bằng 16 và số tham số bằng 14.966.784.

---

### Ô A.4 — train, chạy NỀN

```python
!rm -rf /content/probe /content/probe.yaml
!cd {REPO} && nohup llamafactory-cli train /content/cfg.yaml > /content/train.log 2>&1 &
print("đã khởi động")
```

### Ô A.5 — theo dõi (chạy lại nhiều lần)

```python
import subprocess, re, os, glob
alive = "llamafactory" in subprocess.run(["ps","-eo","args"],capture_output=True,text=True).stdout
log = open("/content/train.log", encoding="utf-8", errors="ignore").read()
step = re.findall(r"'epoch': '([\d.]+)'", log)
loss = re.findall(r"'loss': '([\d.]+)'", log)
ck = sorted(glob.glob(f"{D}/ckpt/{BRANCH}_seed{SEED}/checkpoint-*"))
print(f"tiến trình: {'đang chạy' if alive else 'ĐÃ DỪNG'}")
print(f"epoch: {step[-1] if step else '?'} · loss gần nhất: {loss[-5:] if loss else '?'}")
print(f"điểm lưu trên Drive: {[os.path.basename(x) for x in ck[-3:]]}")
!tail -4 /content/train.log
```

**Kiểm điểm lưu xuất hiện trên Drive** sau ~200 bước đầu. Không thấy nghĩa là `output_dir`
trỏ sai và phiên chết là mất sạch — dừng ngay, sửa, chạy lại.

Bật script chống ngủ ở một tab khác. Phiên chết thì: bật lại → ô A.1 → ô 0.3 → restart →
A.1 → A.2 → **A.4** (bỏ qua A.3) — nó tự dò điểm lưu gần nhất mà nối tiếp.

### Ô A.5b — THỬ NỐI TIẾP, chỉ làm ở lượt train ĐẦU TIÊN ⚠️

Chờ tới khi ô A.5 thấy **checkpoint-200** xuất hiện trên Drive, rồi cố ý giết tiến trình
và bật lại:

```python
import subprocess, glob, os, time
print("điểm lưu hiện có:", [os.path.basename(x) for x in sorted(glob.glob(f"{D}/ckpt/{BRANCH}_seed{SEED}/checkpoint-*"))])
subprocess.run("pkill -f llamafactory-cli", shell=True); time.sleep(5)
print("đã giết tiến trình")
```
```python
!cd {REPO} && nohup llamafactory-cli train /content/cfg.yaml > /content/resume.log 2>&1 &
```
```python
import time; time.sleep(120)
L = open("/content/resume.log", encoding="utf-8", errors="ignore").read()
import re
print("có nhận ra điểm lưu:", "Resuming" in L or "checkpoint" in L.lower())
print("bắt đầu lại từ bước:", re.findall(r"'epoch': '([\d.]+)'", L)[:3] or "chưa in")
print([l for l in L.splitlines() if "esum" in l or "heckpoint" in l][:4])
```

**Vì sao bỏ 5 phút làm chuyện này.** Một lượt train mất 11-18 giờ, mà phiên Colab gần như
chắc chắn đứt ít nhất một lần. Toàn bộ kế hoạch dựa vào chỗ LLaMA-Factory tự dò điểm lưu
gần nhất mà chạy tiếp — thứ đã cố ý dựng bằng cách **bỏ trống** `resume_from_checkpoint`
(lỗi bắt ngày 7/8: điền vào là tắt đúng cái định bật). Cơ chế đó **chưa từng được chạy thử
lần nào**. Biết nó hỏng ở phút thứ 30 thì mất 30 phút; biết ở giờ thứ 11 thì mất 11 giờ.

Nó phải in ra chỗ nhận điểm lưu và bắt đầu lại từ epoch > 0. Nếu bắt đầu lại từ 0 thì cơ
chế nối tiếp **không hoạt động** — dừng, báo mình, đừng để chạy tiếp.

### Ô A.6 — tự kiểm lô (CHỈ lần đầu tiên trong cả chiến dịch)

```python
!cd {REPO} && python harness/infer_branch.py --selftest-batch \
    --adapter {D}/ckpt/{BRANCH}_seed{SEED} --batch 8
```

Phải ra **8/8 trùng nguyên văn**. Rớt là dừng hẳn, đừng chấm.

### Ô A.7 — sinh câu thử 20 bước trước

```python
!cd {REPO} && python harness/infer_branch.py --adapter {D}/ckpt/{BRANCH}_seed{SEED} \
    --out /content/preds_smoke.jsonl --limit 20
```
```python
import json
for r in list(map(json.loads, open("/content/preds_smoke.jsonl", encoding="utf-8")))[:8]:
    print(f"[{r['episode_id']}/{r['step_id']}]\n  chuẩn: {r['gold_instruction']}\n  model: {r['pred']}\n  thô  : {r['raw'][:110]}\n")
```

## 🛑 MỐC DỪNG 5 — dán output ô A.6 và A.7

Đây là **lần đầu tiên nhìn thấy mô hình đã huấn luyện viết gì**. Cần xem: câu có ra tiếng
Anh mạch lạc không · với nhánh S2 thì phần `<desc>` có được sinh đúng khuôn và có bị cắt
bỏ sạch khỏi trường `pred` không · có bị lặp vô hạn không. Cái nào hỏng ở đây thì 1,5 giờ
sinh câu cho 6.958 bước là ném đi.

---

### Ô A.8 — sinh câu đủ tập kiểm

```python
!cd {REPO} && nohup python harness/infer_branch.py --adapter {D}/ckpt/{BRANCH}_seed{SEED} \
    --out {D}/preds/preds_{BRANCH}_seed{SEED}.jsonl > /content/infer.log 2>&1 &
```
```python
import subprocess, os
p = f"{D}/preds/preds_{BRANCH}_seed{SEED}.jsonl"
n = sum(1 for _ in open(p, encoding="utf-8")) if os.path.exists(p) else 0
alive = "infer_branch" in subprocess.run(["ps","-eo","args"],capture_output=True,text=True).stdout
print(f"{n:,} / 6.958   ·   {'đang chạy' if alive else 'ĐÃ DỪNG'}")
!tail -2 /content/infer.log
```

### Ô A.9 — kiểm tệp dự đoán trước khi tắt máy

```python
import json
R = list(map(json.loads, open(f"{D}/preds/preds_{BRANCH}_seed{SEED}.jsonl", encoding="utf-8")))
tap = [r for r in R if r["action"].get("action_type") in ("click","long_press") and "x" in r["action"]]
print(f"bản ghi : {len(R):,}   ← phải là 6.958")
print(f"bước chạm: {len(tap):,}   ← phải là 4.463")
print(f"câu rỗng : {sum(1 for r in R if not r['pred'].strip())} = {sum(1 for r in R if not r['pred'].strip())/len(R):.1%}")
print(f"còn sót <desc> trong pred: {sum(1 for r in R if '<desc>' in r['pred'])}   ← phải là 0")
print(f"độ dài câu trung vị: {sorted(len(r['pred']) for r in R)[len(R)//2]} ký tự")
```

**Điều kiện kết thúc phiên train:** `ckpt/…` và `preds_…jsonl` nằm trên Drive, ô A.9
sạch, **ô A.10 đã chạy**. Rồi mới tắt máy.

---

### Ô A.10 — LƯU VẾT lên Drive ⚠️ chạy trước khi tắt máy, mọi phiên

```python
import os, shutil, json, glob
V = f"{D}/logs/{BRANCH}_seed{SEED}"
os.makedirs(V, exist_ok=True)
for f in ("/content/cfg.yaml", "/content/train.log", "/content/probe.log",
          "/content/resume.log", "/content/infer.log", "/content/preds_smoke.jsonl"):
    if os.path.exists(f): shutil.copy(f, V)
for f in glob.glob(f"{REPO}/harness/descriptor_build_stats*.json"): shutil.copy(f, f"{D}/logs/")
# đường cong mất mát tách riêng, để vẽ hình cho luận văn mà không phải mở lại log
import re
L = open("/content/train.log", encoding="utf-8", errors="ignore").read()
pts = [{"epoch": float(e), "loss": float(l)} for e, l in
       zip(re.findall(r"'epoch': '([\d.]+)'", L), re.findall(r"'loss': '([\d.]+)'", L))]
json.dump(pts, open(f"{V}/loss_curve.json", "w"), indent=1)
print(f"{len(os.listdir(V))} tệp trong {V} · {len(pts)} điểm mất mát")
print(os.listdir(V))
```

**Vì sao phải giữ từng thứ:**

| Tệp | Dùng vào việc gì |
|---|---|
| `cfg.yaml` của TỪNG lượt | **bằng chứng** cho câu "sáu nhánh chỉ khác nhau ba dòng". Không có nó thì đó là lời khai, không phải chứng cứ |
| `train.log` + `loss_curve.json` | hình đường cong mất mát trong luận văn; và để thấy lượt nào phân kỳ |
| `probe.log` | giây-mỗi-bước, dùng cho phần báo cáo chi phí tính toán |
| `resume.log` | chứng minh cơ chế nối tiếp có chạy |
| `preds_*.jsonl` | câu mô hình viết — cần cho chấm tay, cho ví dụ định tính, cho mọi phân tích sau |
| `score_*_raw.jsonl` | toạ độ bộ trỏ **từng bước**. Đổi luật chấm hay thêm lát cắt thì tính lại từ đây, khỏi gọi lại bộ trỏ |
| `descriptor_build_stats*.json` | thống kê nhãn ở quy mô đủ, để đối chiếu với con số báo trong luận văn |
| thư mục `ckpt/` | bộ trọng số. Cần khi muốn sinh lại câu, hoặc khi hội đồng đòi chạy thử |

**Nguyên tắc: thứ gì tính lại tốn tiền hoặc tốn giờ thì phải nằm trên Drive trước khi tắt
máy.** Colab xoá sạch `/content` khi phiên chết, không hỏi lại.

---

# CHẤM ĐIỂM — trên Kaggle, MIỄN PHÍ

Đừng chấm trên Colab: chỉ cần UGround 2 tỉ tham số, T4 gánh được, Kaggle cho 30 giờ mỗi
tuần không mất gì. ~5 giờ một nhánh.

Tải `preds_…jsonl` từ Drive về máy nhà → mình gộp thành gói Kaggle (cần đủ 4.463 ảnh của
tập kiểm, khác gói cổng A chỉ có 300) → chạy:

```
python harness/score_run.py --mode score --grounder uground \
    --preds preds_s1_seed101.jsonl --out score_s1_seed101.json
```

Giữ `score_…_raw.jsonl`: nó lưu toạ độ bộ trỏ từng bước, đổi luật chấm hay thêm lát cắt
thì chấm lại từ đó chứ không gọi lại bộ trỏ.

## 🛑 MỐC DỪNG 6 — sau khi chấm xong CẢ HAI hạt giống của S1

Đây là mốc quyết định của toàn luận văn. Với hai điểm S1 mình tính:

- **cỡ nhiễu hạt giống** = |S1(101) − S1(202)| — Δ giữa S2 và S1 phải lớn hơn con số này
- **MDE THẬT** từ phương sai quan sát được, thay cho MDE chiếu 3,9-6,6 pp
- **khoảng trống còn lại** so với trần 70,0%. S1 mà đã sát 70 thì S2 không có chỗ để hơn,
  và phải bàn lại trước khi tiêu thêm tiền cho bốn lượt train nữa

Rồi mới **khoá ngưỡng đậu/rớt** vào `report/106` kèm ngày, **rồi mới train S2**.

---

# Trình tự cứng — không đảo (report/106 mục 5)

| # | Việc | Phiên | Đơn vị |
|---|---|---|---|
| 0 | dựng dữ liệu + OCR | 1 | ~35 |
| 1 | S1 hạt giống 101 → train + sinh câu | 1 | ~90-130 |
| 2 | S1 hạt giống 202 → train + sinh câu | 1 | ~90-130 |
| 3 | chấm cả hai **trên Kaggle** → MDE thật | — | 0 |
| 4 | 🛑 khoá ngưỡng vào report/106 | — | 0 |
| 5 | phép thử TRẦN trên S1 (`--ceiling gold` + `filler`) | 1 | ~20 |
| 6 | S2 hạt giống 101 và 202 | 2 | ~180-260 |
| 7 | S2r, S2-nopoint | 2 | ~180-260 |
| 8 | B-infer + mô hình gốc (chỉ suy luận) | 1 | ~20 |
| 9 | S3-pilot — **chưa có mã hàm phạt lề** | — | — |

**Bước 3 và 4 phải xong trước bước 6.** Đảo thì ghi lý do vào bản đăng ký và coi kết quả
là thăm dò.

Lệnh cho bước 5 và 8 (chạy trong phiên train, sau ô A.1):

```python
import subprocess
A = f"{D}/ckpt/s1_seed101"
jobs = [
    # phép thử TRẦN — trần là hiệu số gold − filler, KHÔNG phải gold − S1
    (f"--ceiling gold   --adapter {A}", f"{D}/preds/preds_ceiling_gold_s1_seed101.jsonl"),
    (f"--ceiling filler --adapter {A}", f"{D}/preds/preds_ceiling_filler_s1_seed101.jsonl"),
    # B-infer: trọng số S1, nhét DANH SÁCH phần tử lúc chạy (không chỉ ra cái nào là đích)
    (f"--b-infer        --adapter {A}", f"{D}/preds/preds_binfer_s1_seed101.jsonl"),
    # mốc tham chiếu: mô hình gốc, chưa huấn luyện gì
    ("--no-adapter",                    f"{D}/preds/preds_base.jsonl"),
]
for flags, out in jobs:
    print("──", out.split("/")[-1])
    r = subprocess.run(f"python harness/infer_branch.py {flags} --out {out}",
                       shell=True, cwd=REPO, capture_output=True, text=True)
    print(r.stdout[-400:] or r.stderr[-400:])
```

---

# SAU KHI CÓ ĐIỂM — bốn khâu đã đăng ký, không cần GPU, không tốn đơn vị

Bốn khâu này nằm trong bản đăng ký nên **bắt buộc có số**, nhưng không cần card. Làm ở máy
nhà hoặc trên Kaggle. Liệt ở đây để không rơi mất — đúng loại lỗi đã bắt bốn lần (script
suy luận, script chấm, thước không-gây-hại, phép thử trần: nằm trong hồ sơ, tới lúc cần
thì không có gì chạy).

**1. Thước không-gây-hại** (`report/106` mục 3, BẮT BUỘC). Trên các bước KHÔNG phải bước
chạm — cuộn, gõ, mở ứng dụng, chờ, quay lại, chiếm 35,9% tập kiểm — nhánh khai báo không
được thấp hơn nhánh nền quá **3 điểm phần trăm**. Không cần bộ trỏ nên chạy ở đâu cũng được:

```
python harness/score_run.py --mode noharm \
    --preds preds_s2_seed101.jsonl --baseline preds_s1_seed101.jsonl \
    --out noharm_s2_seed101.json
```

**2. Ba lát cắt đã đăng ký**, tính lại từ `score_…_raw.jsonl` chứ không gọi lại bộ trỏ:
toàn tập · **lát khó** (bước thuộc phần ba dưới của phân bố khoảng cách tới phần tử cùng
vai trò gần nhất) · **nhóm ứng dụng chưa thấy lúc dạy** (nhãn `app_seen_in_train`). Kỳ
vọng đã đăng ký: Δ ở lát khó **lớn hơn** Δ toàn tập; ngược lại thì phải ghi rằng cơ chế
không như giả thuyết.

**3. Chấm tay 100 câu, hai người độc lập.** Lá chắn cho đòn "thước thiên vị câu dài". Cần
dựng bộ chấm mù (không cho biết câu của nhánh nào) và báo κ giữa hai người. **Chưa có mã** —
phải viết khi có câu thật.

**4. Bản trình diễn tiếng Việt, định tính.** Vài chục màn, không có bảng số. Đã hứa trong
hồ sơ.

---

# Chấm điểm trên Kaggle — cần gì

Gói cổng A (`thesis_kaggle_gateA.zip`) chỉ có **300 ảnh**, không đủ để chấm 4.463 bước.
Cần một gói khác gồm đủ ảnh bước chạm (~1,7 GB) hoặc dựng lại tập kiểm ngay trên Kaggle
bằng `build_test_data.py --shards 9`. Mình sẽ dựng gói đó khi bạn có tệp dự đoán đầu tiên —
ghi ở đây để không quên là **nó chưa tồn tại**.

# Đối chiếu với bản đăng ký — mục nào chạy ở đâu

Bảng này để soi xem runbook có bỏ sót thứ đã cam kết không. Cột cuối là chỗ duy nhất được
phép ghi "chưa có mã", và ghi thì phải khai trong luận văn.

| Mục trong `report/106` | Chạy ở đâu trong runbook |
|---|---|
| Cổng A — sai số bộ trỏ ≤3% | ✅ **đã xong 9/8** trên Kaggle, ĐẠT 0,7%. **Đừng chạy lại**, tốn tiền vô ích |
| §5 bước 3 — S1 hai hạt giống | phiên train ×2, ô A.2 đổi `SEED` |
| §5 bước 3 — chấm đủ | Kaggle, miễn phí |
| §5 bước 4 — MDE thật + cỡ nhiễu hạt giống | mốc dừng 6 |
| §5 bước 5 — khoá ngưỡng vào `report/106` | mốc dừng 6, mình ghi |
| §5 bước 6 — phép thử TRẦN | ô cuối, `--ceiling gold` + `--ceiling filler` |
| §5 bước 7 — S2 hai hạt giống | phiên train ×2 |
| §5 bước 8 — S2r, S2-nopoint, B-infer | phiên train ×2 + ô `--b-infer` |
| Sửa đổi 9/8 (k) — mốc mô hình gốc | ô `--no-adapter` |
| §5 bước 9 — S3-pilot (khoản phạt lề) | ⛔ **CHƯA CÓ MÃ** hàm mất mát. Dữ liệu đã sửa 9/8. Không kịp thì khai *"đã đăng ký nhưng không chạy"* |
| §3 — thước không-gây-hại (BẮT BUỘC) | mục "sau khi có điểm", `--mode noharm` |
| §5 bước 10 — chấm tay 100 câu, 2 người | ⛔ **chưa có mã bộ chấm mù** |
| §5 bước 10 — demo tiếng Việt | mục "sau khi có điểm" |
| Ba lát cắt đã đăng ký | mục "sau khi có điểm", tính từ `score_*_raw.jsonl` |
| §2 — hạt giống 101/202 (303 nếu cổng kích hoạt) | ô A.2 |
| §10 — hạt giống lấy mẫu 20260805 | trong mã, không đụng vào |
| §6 — luật đọc kết quả | mốc dừng 6, đọc **trước** khi nhìn số |

**Bốn phép kiểm không nằm trong bản đăng ký nhưng runbook bắt buộc**, vì chúng chặn đúng
những kiểu hỏng đã bắt được:

| Phép | Ô | Chặn gì |
|---|---|---|
| rò rỉ tác vụ dạy ↔ kiểm | 0.11b | mô hình học đúng đề thi — không sửa được sau khi train |
| phủ OCR 100% | 0.9 | vài nghìn bước vào huấn luyện với đầu vào thiếu chữ |
| 9 bất biến bốn nhánh | 0.11 | bốn nhánh không so được với nhau |
| thử nối tiếp | A.5b | phiên đứt ở giờ thứ 11 mà không nối lại được |

---

# Bốn điều tuyệt đối không đổi giữa chừng

1. **Cỡ lô hiệu dụng = 16.** Card 80 GB cho phép `16×1` thay `4×4` (nhanh gần gấp đôi,
   gradient y hệt về mặt toán học), nhưng phiên nào tụt xuống 40 GB thì `16×1` không chạy
   nổi. **Giữ `4×4`** trừ khi chắc chắn mọi phiên đều 80 GB.
2. **`bf16: true`.** Phiên nào ra T4/L4 thì không train ở đó.
3. **Hạt giống 101 và 202.**
4. **`output_dir` luôn trên Drive.**

# Nếu hết đơn vị giữa lượt train

Điểm lưu nằm trên Drive nên không mất gì. Mua thêm rồi: ô A.1 → ô 0.3 → restart → A.1 →
A.2 → **A.4** (bỏ A.3). Nó tự dò điểm lưu gần nhất mà nối tiếp — đúng lý do
`resume_from_checkpoint` cố ý bỏ trống trong `train_config.yaml`.

# Bảng tiền

| khâu | giờ | đơn vị |
|---|---|---|
| phiên 0 | ~5 | 35 |
| 6 lượt train | 66-108 | 447-731 |
| 7 lượt sinh câu | ~10 | 68 |
| trần + B-infer + mô hình gốc | ~5 | 34 |
| **tổng** | **86-128** | **584-868** |

Ở $10/100 đơn vị → **$58-87**. Chấm điểm không tính vì chạy trên Kaggle.

**Ghi lại số đơn vị còn lại ở mỗi mốc dừng** — đó là cách duy nhất biết ước tính có đúng
không, và biết sớm trước khi hết.
