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

## Ô 2b — DÒ CỠ ẢNH (~15 phút, 3 lượt × 30 bước)

**Chạy ô 2c TRƯỚC.** Lượt 2b đầu tiên (20/8) cho ba cỡ ra sai số trùng tới hai chữ số thập phân
(1,57% / 28,87% cả ba) vì `min_pixels`/`max_pixels` bị `transformers` nuốt im lặng. Ô 2c đã xác
nhận vá xong: ba grid khác nhau thật — **1.272 / 2.475 / 3.354** token.

⛔ **Luật chọn cỡ, khoá trước khi nhìn:** chọn theo sai số trên **câu chuẩn của người**
(`--mode gate`). Câu chuẩn giống hệt ở mọi nhánh nên cỡ chọn kiểu này **không thể** thiên vị S1
hay S2. **CẤM** dò cỡ bằng điểm của một nhánh — đó là chỉnh dụng cụ theo kết quả.

### Ô 2b-vá — chạy TRƯỚC ô 2b

Bản `score_run.py` trên dataset Kaggle là bản working tree cũ: lớp `UIVenus` **ghi cứng**
`min_pixels=2000000, max_pixels=4800000`, chưa đọc biến môi trường. Đó là lý do ba lượt ô 2b
đầu ra trùng nhau — và cũng xác nhận lượt thăm dò 1,57% đã chạy ở **3.354 token (1092×2408)**.

⛔ **Bẫy đã cắn một lần, đừng cắn lại:** `s.index("self.proc = AutoProcessor.from_pretrained(")`
lấy lần xuất hiện **đầu tiên trong file**, mà đó là của lớp **`UGround`** (đứng trước `UIVenus`).
Vá kiểu đó sửa nhầm `UGround`; chạy `--grounder uivenus` thì `UGround.__init__` không được gọi
lần nào ⇒ không có dòng `[UIVenus]`, kết quả trùng y như cũ, **không một lỗi nào**. Ô dưới neo
tìm kiếm **trong lớp `UIVenus`** và `assert` cả hai chiều: vá phải nằm trong `UIVenus`, và
**không được** lọt sang lớp trước nó.

```python
import os, shutil, glob, ast

# ── 1. chép lại harness SẠCH từ dataset (ô vá trước đã sửa nhầm lớp UGround) ──
WS = "/kaggle/working"
mp = glob.glob("/kaggle/input/**/harness/score_run.py", recursive=True)
assert mp, "DỪNG: không thấy harness/score_run.py trong dataset"
if os.path.exists(f"{WS}/harness"):
    shutil.rmtree(f"{WS}/harness")
shutil.copytree(os.path.dirname(mp[0]), f"{WS}/harness")
SR = f"{WS}/harness/score_run.py"
print("đã chép lại harness sạch từ", mp[0])

# ── 2. vá, NEO TRONG LỚP UIVenus ────────────────────────────────────────────
s = open(SR, encoding="utf-8").read()
c = s.index("class UIVenus")
het = s.find("\ndef ", c)                      # hết lớp UIVenus
i = s.index("self.proc = AutoProcessor.from_pretrained(", c)
assert i < het, "DỪNG: không thấy from_pretrained bên trong lớp UIVenus"
j = s.index("(", i); d = 0
for k in range(j, len(s)):
    d += (s[k] == "(") - (s[k] == ")")
    if d == 0:
        j = k + 1; break
print("\n── mã CŨ trong UIVenus ──\n" + s[i:j])

moi = '''mn = int(os.environ.get("VENUS_MIN_PIXELS", 2000000))
        mx = int(os.environ.get("VENUS_MAX_PIXELS", 4800000))
        self.proc = AutoProcessor.from_pretrained(path, min_pixels=mn, max_pixels=mx)
        ip = self.proc.image_processor
        if isinstance(getattr(ip, "size", None), dict):
            ip.size = {"shortest_edge": mn, "longest_edge": mx}
        ip.min_pixels, ip.max_pixels = mn, mx
        print(f"[UIVenus] xin min={mn} max={mx} -> giu min={getattr(ip,'min_pixels',None)} "
              f"max={getattr(ip,'max_pixels',None)} size={getattr(ip,'size',None)}", flush=True)'''
open(SR, "w", encoding="utf-8").write(s[:i] + moi + s[j:])

# ── 3. kiểm: UIVenus đã đổi, UGround KHÔNG đổi ──────────────────────────────
t = open(SR, encoding="utf-8").read()
ast.parse(t)
cv = t.index("class UIVenus")
assert "VENUS_MIN_PIXELS" in t[cv:], "⛔ vá không nằm trong UIVenus"
assert "VENUS_MIN_PIXELS" not in t[:cv], "⛔ vá lọt sang lớp khác (UGround?)"
ug = t[t.index("class UGround"):t.index("class OpenAIGrounder")]
print("\nUGround giữ nguyên:", "from_pretrained(path)" in ug, "· không dính env:",
      "VENUS_" not in ug)
print("cú pháp hợp lệ ✅ — chạy lại ô 2b được rồi")
```

⚠️ Bản vá này chỉ sống trong **phiên hiện tại**. Trước lượt ô 5 chạy dài (hoặc bất kỳ lượt
commit nào), phải đưa `harness/score_run.py` bản mới lên dataset — nếu không lượt đó lại chạy
mã cũ và cỡ ảnh lại không đổi.

```python
import subprocess, os, json, time, re
WS = "/kaggle/working"; SR = f"{WS}/harness/score_run.py"

# ── vá bản đang nằm trong working (idempotent) ──────────────────────────────
s = open(SR, encoding="utf-8").read()
old = 'self.proc = AutoProcessor.from_pretrained(path, min_pixels=mn, max_pixels=mx)'
if "ip.min_pixels" not in s:
    assert old in s, "DỪNG: không khớp mã — bản score_run.py trên dataset khác bản đang có"
    open(SR, "w", encoding="utf-8").write(s.replace(old, old + '''
        ip = self.proc.image_processor
        if isinstance(getattr(ip, "size", None), dict):
            ip.size = {"shortest_edge": mn, "longest_edge": mx}
        ip.min_pixels, ip.max_pixels = mn, mx
        print(f"[UIVenus] giu min={getattr(ip,'min_pixels',None)} "
              f"max={getattr(ip,'max_pixels',None)} size={getattr(ip,'size',None)}", flush=True)''', 1))
    print("đã vá score_run.py ✅")
else:
    print("score_run.py đã vá từ trước ✅")

CO = [(200704, 1003520, "1.272 token  (672×1484)"),
      (200704, 2007040, "2.475 token  (924×2100)"),
      (2000000, 4800000, "3.354 token  (1092×2408)")]
kq = []
for mn, mx, ten in CO:
    tag = f"do_{mx//1000}k"
    for e in (f"{WS}/out/{tag}.json", f"{WS}/out/{tag}_raw.jsonl"):
        if os.path.exists(e): os.remove(e)          # cấu hình khác ⇒ KHÔNG nối tiếp
    env = {**os.environ, "VENUS_MIN_PIXELS": str(mn), "VENUS_MAX_PIXELS": str(mx)}
    t0 = time.time()
    with open(f"{WS}/out/{tag}.log", "w") as f:
        subprocess.run(["python", "-u", SR, "--mode", "gate", "--grounder", "uivenus",
                        "--n", "30", "--out", f"{WS}/out/{tag}.json"],
                       stdout=f, stderr=subprocess.STDOUT, cwd=WS, env=env)
    lg = open(f"{WS}/out/{tag}.log", encoding="utf-8", errors="ignore").read()
    bang = next((l for l in lg.splitlines() if "[UIVenus]" in l), "⛔ KHÔNG THẤY dòng [UIVenus]")
    j = json.load(open(f"{WS}/out/{tag}.json"))
    gy = (time.time() - t0 - 90) / 30
    kq.append((ten, j["median_err"], j["p75_err"], gy))
    print(f"\n{ten}\n  {bang}\n  trung vị {j['median_err']:.3%} · p75 {j['p75_err']:.3%}"
          f" · ~{gy:.1f} s/bước", flush=True)

print(f"\n{'cấu hình':<28}{'trung vị':>10}{'p75':>10}{'s/bước':>9}")
for ten, m, p75, gy in kq:
    print(f"  {ten:<26}{m:>9.3%}{p75:>10.3%}{gy:>8.1f}")
print("\n  mốc UGround trên ĐÚNG 30 bước này: trung vị 0,600% · p75 3,600% · ≤3%: 73,3%")

med = [round(r[1], 6) for r in kq]
assert len(set(med)) > 1, ("⛔ BA CỠ VẪN RA TRÙNG NHAU ⇒ cỡ ảnh vẫn không đổi thật. "
                           "Đừng đọc bảng này. Kiểm dòng [UIVenus] ở trên.")
best = min(kq, key=lambda r: r[1])
print(f"\n⇒ chọn: {best[0]} — trung vị {best[1]:.3%}, {best[3]:.1f} s/bước")
print("   Ghi lại VENUS_MIN/MAX_PIXELS của cỡ này, dùng Y HỆT cho ô 4 và ô 5.")
```

### Đọc ô 2b

· Cỡ nào cho **trung vị thấp nhất** thì lấy cỡ đó, ghi lại `VENUS_MIN/MAX_PIXELS` và **dùng
  y hệt** cho ô 4 và ô 5. Ghi vào mục sửa đổi kèm ba con số — để sau này chứng minh được cỡ
  chọn theo câu chuẩn, không theo nhánh.
· Cả ba cỡ đều kém UGround rõ rệt (trung vị > 1,5%, p75 > 20%) ⇒ **đó là kết quả**, không phải
  lỗi: UI-Venus mạnh hơn trên ScreenSpot nhưng yếu hơn trên ảnh AndroidControl. Vẫn chạy tiếp
  được, nhưng phải đọc theo mục **Bẫy pha loãng** dưới đây.
· n=30 nên đừng chốt vội trên chênh lệch nhỏ; chỉ khi một cỡ hơn hẳn (trung vị lệch > 2 lần)
  mới coi là kết luận.

---

## Ô 2c — KIỂM cỡ ảnh có thật sự đổi không (10 giây, KHÔNG cần GPU)

**Vì sao có ô này.** Lượt ô 2b đầu tiên cho ba cỡ ảnh khác nhau ra sai số **trùng tới hai chữ
số thập phân** (1,57% / 28,87% cả ba). Trùng kiểu đó nghĩa là **cùng một phép tính** — biến môi
trường không có tác dụng. `transformers` đời mới chuyển `Qwen2VLImageProcessor` sang
`size={"shortest_edge","longest_edge"}`, nên `min_pixels`/`max_pixels` truyền vào
`from_pretrained` bị **nuốt im lặng, không một dòng cảnh báo**.

Ô này chỉ nạp **bộ xử lý ảnh**, không nạp mô hình 7B, nên chạy trong vài giây và không tốn GPU.
`image_grid_thw` là sự thật cuối cùng: nó cho biết ảnh **thực sự** được đưa vào ở cỡ nào.

```python
from transformers import AutoProcessor
from PIL import Image
import glob, os
img = Image.open(sorted(glob.glob(f"{TEST}/images/*.png"))[0]).convert("RGB")
print(f"ảnh gốc {img.width}×{img.height} = {img.width*img.height/1e6:.2f} MP\n")
print(f"{'xin (max_pixels)':>18}{'grid t,h,w':>16}{'cỡ thật':>14}{'token ảnh':>11}")
for mn, mx in ((200704, 1003520), (200704, 2007040), (2000000, 4800000)):
    pr = AutoProcessor.from_pretrained("inclusionAI/UI-Venus-Ground-7B",
                                       min_pixels=mn, max_pixels=mx)
    ip = pr.image_processor
    if isinstance(getattr(ip, "size", None), dict):
        ip.size = {"shortest_edge": mn, "longest_edge": mx}
    ip.min_pixels, ip.max_pixels = mn, mx
    g = pr(text=["x"], images=[img], return_tensors="pt")["image_grid_thw"][0]
    t, h, w = int(g[0]), int(g[1]), int(g[2])
    print(f"{mx:>18,}{f'{t},{h},{w}':>16}{f'{w*14}×{h*14}':>14}{h*w//4:>11,}")
```

**Đọc:** ba dòng phải cho **ba `grid` khác nhau**. Còn giống nhau ⇒ bản `transformers` trên
Kaggle nuốt cả cách đặt thẳng; lúc đó **đừng dò cỡ nữa**, cứ chạy cỡ mặc định của mô hình và
ghi vào bài rằng cỡ ảnh chưa kiểm soát được.

Nếu ba dòng khác nhau ⇒ **chạy lại ô 2b** (mã `score_run.py` đã vá, giờ đặt thẳng lên
`image_processor` và in ra cỡ nó thật sự giữ), rồi mới đọc bảng chọn cỡ.

⚠️ Sau khi vá, **`harness/` trong `/kaggle/working` là bản CŨ** — ô 1 chỉ chép khi thư mục chưa
tồn tại. Chạy lại ô 1 sau khi đã cập nhật dataset, hoặc xoá tay:
`import shutil; shutil.rmtree("/kaggle/working/harness")` rồi chạy lại ô 1.

---

## ⚠️ BẪY PHA LOÃNG — phải đọc trước khi diễn giải bất kỳ con số nào

Đây là chỗ phép B dễ bị đọc sai nhất, và nó không tự lộ ra.

**Nếu UI-Venus là dụng cụ TỆ HƠN, thì Δ(S2−S1) sẽ tự động co về 0** — không phải vì UGround
thiên vị, mà vì thước nhiễu hơn thì mọi chênh lệch đều bị pha loãng. Nghĩa là:

> Δ ≈ 0 dưới UI-Venus **KHÔNG** chứng minh được *"UGround thiên vị văn phong AC"*.
> Nó cũng khớp hoàn toàn với *"UI-Venus đo kém hơn nên chẳng phân biệt được gì"*.

**Cách tách hai khả năng: phải có một CHỨNG NHÂN — chênh lệch đã biết là thật.** Dùng
**S1 − Base = +11,52 pp** (UGround, χ²=243, p<1e-56). Đây là hiệu lớn, chắc, không ai cãi.

| dưới UI-Venus | S1−Base | S2−S1 | kết luận |
|---|---|---|---|
| giữ ~11 pp | về ~0 | ✅ **thước cũ thiên vị thật** — phát hiện mạnh |
| giữ ~11 pp | vẫn ~−2 | ✅ **S2 thua thật**, tái lập qua hai dụng cụ |
| tụt còn ~5 pp | về ~0 | ⛔ **pha loãng** — không kết luận được gì về S2 |

⇒ **Phải chấm thêm nhánh Base trên đúng lát ấy.** Không có nó thì lượt chạy này không trả lời
được câu hỏi ban đầu. Cộng vào ô 5, xem lại ô 3 để tính giờ.

Thước phụ rẻ hơn, có sẵn từ ô 4 **không tốn thêm giây GPU nào**: chạy
`python3 harness/gate_a_ceiling.py --raw runs/venus/venus_gate_raw.jsonl` để lấy **trần của
UI-Venus** trên đúng 300 bước cổng A. Trần tụt bao nhiêu phần trăm so với 75,7% chính là mức
nén của thang đo.

---

## Ô 3 — chọn cỡ lát theo tốc độ đo được

Ba nhánh phải chấm: **S1 · S2 · Base**. Base là **chứng nhân** chống bẫy pha loãng, không
phải phần thêm cho đủ bộ — thiếu nó thì lượt chạy không trả lời được câu hỏi ban đầu.

```python
import math
GIAY = float(input("giây/bước của cỡ đã chọn ở ô 2b: ").strip())
PHIEN, QUOTA = 11.0, 30.0      # Kaggle cắt phiên ở 12 giờ · quota 30 giờ/tuần

gate = 270 * GIAY / 3600
print(f"  ô 4  cổng A (còn 270 bước)              {gate:>5.1f}h")
print(f"\n  {'lát':>6}{'lượt gọi':>10}{'giờ':>8}   ")
for m in (2532, 1266, 633):
    h = m * 3 * GIAY / 3600
    ghi = "✅ gọn một phiên" if h <= PHIEN else f"⚠️ cắt {math.ceil(h/PHIEN)} phiên"
    tot = "✅" if gate + h <= QUOTA else "⛔ quá quota tuần"
    print(f"  {m:>6}{m*3:>10}{h:>7.1f}h   {ghi}  · cả cổng A {gate+h:.1f}h {tot}")
```

**Luật chọn, khoá trước khi nhìn kết quả:** lấy **lát lớn nhất mà quota cho phép**. Lát 633 chỉ
đọc được **dấu**, không đọc được độ lớn — dùng được, nhưng phải khai đúng như vậy trong bài.

Ước lượng ở 10 s/bước (số của lượt thăm dò, ô 2b có thể hạ xuống): lát 1.266 × 3 nhánh ≈ **10,6
giờ** — vừa một phiên. Lát 2.532 × 3 ≈ 21 giờ — phải cắt hai phiên, nhưng `score_run.py` nối
tiếp được nên cắt phiên không mất gì ngoài thời gian.

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

## Ô 5 — chấm Base, S1, S2 trên lát đã chọn

Thứ tự **Base → S1 → S2** cố ý: mất phiên giữa chừng thì thứ còn lại vẫn đủ để đọc một phép so
trọn vẹn, và `score_run.py` nối tiếp được từ tệp thô ở lượt sau.

⚠️ **Đặt `VENUS_*_PIXELS` đúng cỡ đã chốt ở ô 2b.** Đổi cỡ giữa các nhánh là ba nhánh đo bằng
ba dụng cụ khác nhau — hỏng cả lượt mà không có gì báo.

```python
import subprocess, time, os
WS = "/kaggle/working"
LAT = 1266                     # ← lấy từ ô 3
MN, MX = 200704, 1003520       # ← lấy từ ô 2b
TRAN_GIO = 11.0                # giết tiến trình trước khi Kaggle cắt phiên, để tệp thô kịp lưu
env = {**os.environ, "VENUS_MIN_PIXELS": str(MN), "VENUS_MAX_PIXELS": str(MX)}

for nhanh in ("base", "s1", "s2"):
    ten = f"venus_{nhanh}_{LAT}"
    src = [c for c in P.values() if os.path.basename(c) == f"preds_{ten}.jsonl"][0]
    out, LOG = f"{WS}/out/score_{ten}.json", f"{WS}/out/{ten}.log"
    print(f"\n===== {ten} =====", flush=True)
    t0 = time.time(); f = open(LOG, "w")
    p = subprocess.Popen(["python", "-u", f"{WS}/harness/score_run.py",
                          "--mode", "score", "--grounder", "uivenus",
                          "--preds", src, "--n", str(LAT), "--out", out],
                         stdout=f, stderr=subprocess.STDOUT, cwd=WS, env=env)
    while p.poll() is None:
        time.sleep(120)
        gio = (time.time() - t0) / 3600
        n = sum(1 for _ in open(LOG)) if os.path.exists(LOG) else 0
        print(f"[{time.strftime('%H:%M:%S')}] {ten} · {gio:.2f}h · {n} dòng log", flush=True)
        if gio > TRAN_GIO:
            print("⚠️ QUÁ TRẦN GIỜ — giết tiến trình để notebook kết thúc SẠCH, "
                  "nhờ vậy tệp thô dở vẫn lưu được thành Output", flush=True)
            p.terminate(); break
    f.close()
    print(f"{ten}: mã thoát {p.returncode} · {(time.time()-t0)/3600:.2f} giờ", flush=True)
```

**Mốc đối chiếu, đo bằng UGround trên ĐÚNG các lát này** (tính sẵn, offline):

| lát | S1 − Base (UGround) | S2 − S1 (UGround, quy về 4.463) |
|---|---|---|
| 2.532 | **+10,35** pp [+8,39 · +12,40] | −1,93 pp [−3,06 · −0,75] |
| 1.266 | **+11,69** pp [+9,00 · +14,41] | *(bootstrap lại khi có số)* |
| 633 | **+11,06** pp [+7,50 · +14,73] | *(nt)* |

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
