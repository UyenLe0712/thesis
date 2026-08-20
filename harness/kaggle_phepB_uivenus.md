# Phép B — đổi bộ trỏ sang UI-Venus-Ground-7B (Kaggle, 0 đồng)

**Câu hỏi phải trả lời:** điểm S2 thấp hơn S1 có phải do **dụng cụ đo** không?

UGround-V1-2B có **47K phần tử AndroidControl nhãn người** trong công thức huấn luyện
(Bảng 1, arXiv 2410.05243). S1/S2 được dạy viết đúng văn phong chú thích của kho đó ⇒ còn
một lời giải thích thay thế: bộ trỏ **quen giọng** chứ không phải câu tốt hơn.
`UI-Venus-Ground-7B` (arXiv 2508.10833 mục 3.2.1) dùng Widget Captioning · UI RefExp ·
SeeClick-Web · ShowUI · OmniAct — **không có AndroidControl**.

⚠️ **Nó vẫn nền Qwen2.5-VL**, cùng họ với mô hình bị chấm. Phép này đóng đòn *nhiễm dữ liệu*,
**không** đóng đòn *cùng họ*. Đừng viết trong bài rằng nó giải quyết cả hai.

⛔ **Luật đọc khoá TRƯỚC khi chạy:** báo **cả hai bộ trỏ cạnh nhau**, không chọn bộ trỏ nào cho
số đẹp hơn. Lý do đổi dụng cụ là *nó mạnh hơn và sạch hơn* (ScreenSpot-v2 mobile 99,0/90,0 vs
95,0/83,3) — lý do đó đứng vững bất kể kết quả. Bốn kết cục:

| UGround | UI-Venus | đọc thành |
|---|---|---|
| S2 < S1 | S2 < S1 | thành phần khai báo **không có ích** — kết luận vững, bỏ nhánh S2 sạch sẽ |
| S2 < S1 | S2 ≈ S1 | UGround **thiên vị văn phong AC** — phát hiện về THƯỚC, mạnh hơn cả việc S2 thắng |
| S2 < S1 | S2 > S1 | như trên, mức nặng. Phải chạy thêm để chắc, không báo vội |
| — | trần tụt sâu | **dụng cụ không dùng được trên ảnh này**, không kết luận gì về S2 |

---

## Vì sao chỉ cần chấm 2.532 bước chứ không phải 4.463

Bộ trỏ **tất định** (0 bất đồng trên 1.625 phép so, bốn lượt độc lập). Bước nào S1 và S2 sinh
**câu y hệt nhau** thì mọi bộ trỏ cho cùng kết quả ⇒ đóng góp **đúng 0** vào hiệu ghép cặp.

Kiểm bằng dữ liệu đã có, không phải suy luận: 1.931/4.463 bước (43,3%) hai nhánh viết giống hệt,
và trên đúng 1.931 bước đó UGround cho **0 bất đồng**. Nên chấm 2.532 bước còn lại là **tái tạo
đúng** hiệu ghép cặp của cả tập, không xấp xỉ.

| cỡ lát | lượt gọi bộ trỏ | SE của Δ | nửa KTC95 | đọc được gì |
|---|---|---|---|---|
| **2.532** (đủ) | 5.064 | 0,60 pp | ±1,18 pp | phân giải được hiệu 1,9 pp |
| **1.266** (½) | 2.532 | 0,85 pp | ±1,67 pp | phân giải được hiệu 1,9 pp, sát mép |
| 633 (¼) | 1.266 | 1,20 pp | ±2,35 pp | chỉ đọc được **dấu**, không đọc được độ lớn |

*(SE đã nhân 1,10 — hệ số nở do gom cụm theo app, đo được ở `mde_that.py`.)*

Tệp đã dựng sẵn tại `runs/venus/`, dựng bằng hạt giống 20260805 (cùng hạt với `score_run.py`).

---

## Bước 1 — đưa tệp lên dataset `thesis-preds`

Mở dataset **`thesis-preds`** → **New Version** → thêm cả thư mục `runs/venus/`:

```
preds_venus_tran400.jsonl      preds_venus_s1_2532.jsonl   preds_venus_s2_2532.jsonl
preds_venus_s1_1266.jsonl      preds_venus_s2_1266.jsonl
preds_venus_s1_633.jsonl       preds_venus_s2_633.jsonl
```

Ảnh và `test.jsonl` đã nằm ở dataset `thesis-score`, không cần đụng.

**Cài đặt notebook — ba thứ, thiếu cái nào cũng mất một lượt:**

| | vì sao |
|---|---|
| **Accelerator: GPU T4 ×2** | UI-Venus 7B ở fp16 chiếm **~15,2 GB**. Một T4 (16 GB) không đủ chỗ cho cả trọng số lẫn kích hoạt ⇒ **tràn**. Phải hai card để `device_map="auto"` chia ra. P100 đơn cũng **không** đủ |
| **Internet: ON** | nạp `inclusionAI/UI-Venus-Ground-7B` thẳng từ HuggingFace, **~16 GB**, mất 10–20 phút lượt đầu |
| **Input: `thesis-preds` đã lên version mới** | thiếu là ô 1 rớt `assert` ngay |

---

## Ô 0 — kiểm máy (5 giây)

```python
import torch, subprocess
n = torch.cuda.device_count()
print("số GPU:", n)
for i in range(n):
    p = torch.cuda.get_device_properties(i)
    print(f"  [{i}] {p.name}  {p.total_memory/2**30:.1f} GB  sm_{p.major}{p.minor}")
tong = sum(torch.cuda.get_device_properties(i).total_memory for i in range(n)) / 2**30
assert n >= 1, "DỪNG: đang chạy CPU. Accelerator = GPU T4 ×2."
assert tong >= 24, (f"DỪNG: chỉ có {tong:.1f} GB VRAM. UI-Venus 7B fp16 cần ~15,2 GB trọng số "
                    "cộng kích hoạt của ~6.100 token ảnh. Chọn T4 ×2.")
print(f"tổng VRAM {tong:.1f} GB ✅")
print("fp16 (không bf16 vì T4 là Turing) — đúng như pick_dtype() sẽ chọn")
```

## Ô 1 — đường dẫn + kiểm tệp

```python
import os, glob, json, shutil
WS = "/kaggle/working"
mp = glob.glob("/kaggle/input/**/harness/score_run.py", recursive=True)
assert mp, "DỪNG: không thấy harness/score_run.py trong dataset"
SRC = os.path.dirname(os.path.dirname(mp[0]))
if not os.path.exists(f"{WS}/harness"):
    shutil.copytree(f"{SRC}/harness", f"{WS}/harness")
print("harness →", f"{WS}/harness")

TEST = f"{WS}/harness/dg1_cache/test_ac"
assert os.path.exists(f"{TEST}/test.jsonl"), "DỪNG: thiếu test.jsonl"
assert len(glob.glob(f"{TEST}/images/*.png")) > 4000, "DỪNG: thiếu ảnh tập kiểm"

P = {}
for t in ("venus_tran400", "venus_s1_2532", "venus_s2_2532",
          "venus_s1_1266", "venus_s2_1266", "venus_s1_633", "venus_s2_633"):
    c = glob.glob(f"/kaggle/input/**/preds_{t}.jsonl", recursive=True)
    if c:
        P[t] = c[0]
        print(f"  {t:18s} {sum(1 for _ in open(c[0])):>5} bước")
assert "venus_tran400" in P, "DỪNG: chưa thấy preds_venus_tran400.jsonl — cập nhật dataset version"
os.makedirs(f"{WS}/out", exist_ok=True)
```

---

## Ô 2 — THĂM DÒ 30 bước (~10–20 phút kể cả tải mô hình)

**Đây là ô cứu cả lượt chạy.** Nó trả lời ba câu bằng một lần chạy:

1. **7B có vừa hai card T4 không** — tràn thì chết ngay ở đây, không phải sau 6 giờ;
2. **giải mã toạ độ có đúng không** — UI-Venus trả **hộp** `[x1,y1,x2,y2]` theo pixel của ảnh
   *đã đổi kích thước*, phải chuẩn hoá qua `image_grid_thw × 14`. Lấy thẳng số nó trả về là sai
   hệ toạ độ, và **kiểu sai đó không báo lỗi** — chỉ làm điểm thấp đều rồi ta đổ oan cho S2;
3. **bao nhiêu giây một bước** — con số duy nhất quyết được cỡ lát ở ô 3.

`--mode gate` đưa **câu chuẩn của người** cho bộ trỏ rồi đo lệch bao nhiêu phần trăm bề ngang
màn. Đầu vào hoàn hảo ⇒ mọi sai số còn lại là của dụng cụ.

```python
import subprocess, time, os
WS = "/kaggle/working"
t0 = time.time()
with open(f"{WS}/out/probe.log", "w") as f:
    p = subprocess.run(["python", "-u", f"{WS}/harness/score_run.py",
                        "--mode", "gate", "--grounder", "uivenus", "--n", "30",
                        "--out", f"{WS}/out/venus_gate.json"],
                       stdout=f, stderr=subprocess.STDOUT, cwd=WS)
print(open(f"{WS}/out/probe.log").read()[-3000:])
print(f"\n=== mã thoát {p.returncode} · {time.time()-t0:.0f} giây kể cả tải mô hình ===")
```

### Đọc kết quả ô 2 — ba ngưỡng, cái nào rớt cũng DỪNG

| số | đạt | rớt nghĩa là gì |
|---|---|---|
| **sai số trung vị** | **≤ 3%** (UGround được 0,73%) | > 15% ⇒ gần chắc chắn **giải mã sai hệ toạ độ**, không phải bộ trỏ dở. Kiểm `parse_fail` và vài dòng `pred_xy` trong `venus_gate_raw.jsonl` trước khi kết luận |
| `parse_fail` | ~0 | mô hình trả về khuôn khác khuôn `[x1,y1,x2,y2]` ⇒ phải sửa `UIVenus.point` |
| **giây/bước** | in ở dòng `bước/giây` | đây là số đem sang ô 3 |

Không có dòng tiến độ nào sau **6 phút** kể từ khi tải xong mô hình thì dừng — đã có tiền lệ
lượt Kaggle treo 7 giờ vì log ngập.

---

## Ô 3 — chọn cỡ lát theo tốc độ đo được

```python
import json, math
GIAY = float(input("giây/bước đo được ở ô 2: ").strip())   # ví dụ 9.5
TRAN_PHIEN = 11.0     # Kaggle cắt phiên ở 12 giờ — chừa 1 giờ
QUOTA = 30.0          # giờ GPU còn lại trong tuần

print(f"\n{'việc':<34}{'lượt gọi':>9}{'giờ':>8}   ")
print("-"*56)
gate = (300-30) * GIAY / 3600
print(f"{'ô 4  cổng A đủ 300 bước':<34}{270:>9}{gate:>7.1f}h")
for m in (2532, 1266, 633):
    h = m*2*GIAY/3600
    ghi = "✅ một phiên" if h <= TRAN_PHIEN else f"⚠️ phải cắt {math.ceil(h/TRAN_PHIEN)} phiên"
    print(f"{'ô 5  S1+S2 lát '+str(m):<34}{m*2:>9}{h:>7.1f}h   {ghi}")
print(f"\nquota tuần còn {QUOTA:.0f} giờ. Cổng A + lát đủ = {gate + 2532*2*GIAY/3600:.1f} giờ")
```

**Luật chọn, khoá trước khi nhìn số:** lấy **lát lớn nhất mà quota cho phép**, không lấy theo
kết quả. Lát 633 chỉ đọc được dấu — dùng khi quota không đủ, và **phải khai trong bài** là lát
đó không phân giải được độ lớn.

---

## Ô 4 — cổng A đủ 300 bước (nối tiếp từ ô 2, không chấm lại 30 bước cũ)

`--n 300` tái lập **đúng 300 bước** mà UGround đã chạy ở cổng A (kiểm rồi: trùng 300/300, vì
`score_run.py` xáo bằng hạt giống cố định 20260805). Nên đây là phép so **ghép cặp hoàn hảo**
giữa hai dụng cụ trên cùng ảnh, cùng câu.

```python
import subprocess, time, threading, os
WS = "/kaggle/working"; LOG = f"{WS}/out/gate300.log"
t0 = time.time()
f = open(LOG, "w")
p = subprocess.Popen(["python", "-u", f"{WS}/harness/score_run.py",
                      "--mode", "gate", "--grounder", "uivenus", "--n", "300",
                      "--out", f"{WS}/out/venus_gate.json"],
                     stdout=f, stderr=subprocess.STDOUT, cwd=WS)
while p.poll() is None:
    time.sleep(120)
    n = sum(1 for _ in open(LOG)) if os.path.exists(LOG) else 0
    print(f"[{time.strftime('%H:%M:%S')}] còn sống · {(time.time()-t0)/60:.0f} phút · "
          f"{n} dòng log", flush=True)
f.close()
print("mã thoát", p.returncode)
print(open(f"{WS}/out/venus_gate.json").read())
```

## Ô 5 — chấm S1 và S2 trên lát đã chọn

Đổi `LAT` thành cỡ đã chốt ở ô 3. **Chạy S1 trước, xong mới S2** — mất phiên giữa chừng thì ít
nhất có một nhánh trọn vẹn, và `score_run.py` nối tiếp được từ tệp thô.

```python
import subprocess, time, os
WS = "/kaggle/working"
LAT = 2532                      # ← 2532 | 1266 | 633, lấy từ ô 3
TRAN_GIO = 11.0                 # giết tiến trình trước khi Kaggle cắt phiên, để tệp thô kịp lưu

for nhanh in ("s1", "s2"):
    ten = f"venus_{nhanh}_{LAT}"
    src = [c for c in P.values() if ten in c][0]
    out = f"{WS}/out/score_{ten}.json"
    LOG = f"{WS}/out/{ten}.log"
    print(f"\n===== {ten} =====", flush=True)
    t0 = time.time(); f = open(LOG, "w")
    p = subprocess.Popen(["python", "-u", f"{WS}/harness/score_run.py",
                          "--mode", "score", "--grounder", "uivenus",
                          "--preds", src, "--n", str(LAT), "--out", out],
                         stdout=f, stderr=subprocess.STDOUT, cwd=WS)
    while p.poll() is None:
        time.sleep(120)
        gio = (time.time()-t0)/3600
        n = sum(1 for _ in open(LOG)) if os.path.exists(LOG) else 0
        print(f"[{time.strftime('%H:%M:%S')}] {ten} · {gio:.2f}h · {n} dòng", flush=True)
        if gio > TRAN_GIO:
            print("⚠️ QUÁ TRẦN GIỜ — giết tiến trình để notebook kết thúc SẠCH, "
                  "nhờ vậy tệp thô dở vẫn được lưu thành Output", flush=True)
            p.terminate(); break
    f.close()
    print(f"{ten}: mã thoát {p.returncode} · {(time.time()-t0)/3600:.2f} giờ", flush=True)
```

## Ô 6 — gom tệp mang về

```python
import shutil, glob, os
os.makedirs("/kaggle/working/results", exist_ok=True)
for p in glob.glob("/kaggle/working/out/*"):
    shutil.copy(p, "/kaggle/working/results/")
shutil.make_archive("/kaggle/working/venus_results", "zip", "/kaggle/working/results")
print(os.path.getsize("/kaggle/working/venus_results.zip")/2**20, "MB")
```

⭐ **Bắt buộc mang về cả `*_raw.jsonl`.** Có tệp thô thì mọi phép đọc lại — đổi luật chấm, đổi
lát, ghép cặp với UGround — làm được **offline, 0 giây GPU**. Đã cứu trọn một lượt 5,6 giờ khi
chấm lại `p3_nopos_v2`.

---

## Sau khi có tệp: đọc offline tại máy

```
python3 harness/phan_tich_venus.py
```

So **ghép cặp từng bước** giữa hai bộ trỏ trên đúng những bước cả hai đã chấm, trả về:
sai số trung vị hai dụng cụ (cổng A, 300 bước ghép cặp) · Δ(S2−S1) theo UI-Venus kèm KTC
bootstrap gom cụm · và bảng bốn ô ở đầu file này.
