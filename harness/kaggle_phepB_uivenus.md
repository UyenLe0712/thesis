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

## Trình tự chạy — copy theo đúng thứ tự ô trong file này

| ô | việc | giờ |
|---|---|---|
| **Bước 1b** | dựng `harness_code.zip`, đưa lên Drive, share "ai có link" | 2 phút |
| **Ô 0** | kiểm máy (T4×2, 29,1 GB) | 5 giây |
| **Ô 1** | tải mã + preds từ Drive · nối ảnh bằng symlink | 30 giây |
| **Ô 4** | cổng A 300 bước × **hai** cỡ (3.354 tok đã loại vì OOM) | ~60 phút |
| **Ô 2d** | ⭐ **chọn cỡ ảnh** theo `hit_disk` + trần Voronoi — in thẳng `MN, MX` cho ô 5 | 0 giây GPU |
| **Ô S** | bật sao lưu tệp thô ra dataset riêng (cần Secrets) | 30 giây |
| **Ô 5** | chấm **Base · S1 · S2** trên lát đã chốt | ~8,4 giờ |
| **Ô 6** | gom tệp + đổi tên cổng A thành `venus_gate_raw.jsonl` | 1 phút |
| — | tại máy: giải nén vào `runs/venus/` rồi `python3 harness/phan_tich_venus.py` | 0 đồng |

⛔ **Ô 2 và ô 2b không chạy nữa** — mã trên Drive đã có sẵn phần đọc `VENUS_*_PIXELS`, và cỡ
ảnh đã dò xong ngày 20/8. Hai ô đó giữ lại chỉ để tra lịch sử.
⛔ **Ô 2d KHÔNG được bỏ qua.** Ô 5 cần `MN, MX` từ nó; đoán đại là ba nhánh có thể đo bằng cỡ
khác cổng A, hỏng cả lượt mà không có gì báo.

⛔ **Ô 5 là lượt chạy dài.** Trước nó phải đưa `harness/score_run.py` **bản mới** lên dataset —
bản vá của ô 2b chỉ sống trong phiên hiện tại. Quên là lượt đó chạy mã cũ, im lặng suốt gần 9 tiếng.

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
preds_venus_tran400.jsonl
preds_venus_base_2532.jsonl    preds_venus_s1_2532.jsonl   preds_venus_s2_2532.jsonl
preds_venus_base_1266.jsonl    preds_venus_s1_1266.jsonl   preds_venus_s2_1266.jsonl
preds_venus_base_633.jsonl     preds_venus_s1_633.jsonl    preds_venus_s2_633.jsonl
```

Ảnh và `test.jsonl` đã nằm ở dataset `thesis-score`, không cần đụng.

**Cài đặt notebook — ba thứ, thiếu cái nào cũng mất một lượt:**

| | vì sao |
|---|---|
| **Accelerator: GPU T4 ×2** | UI-Venus 7B ở fp16 chiếm **~15,2 GB**. Một T4 (16 GB) không đủ chỗ cho cả trọng số lẫn kích hoạt ⇒ **tràn**. Phải hai card để `device_map="auto"` chia ra. P100 đơn cũng **không** đủ |
| **Internet: ON** | nạp `inclusionAI/UI-Venus-Ground-7B` thẳng từ HuggingFace, **~16 GB**, mất 10–20 phút lượt đầu |
| **Input: `thesis-preds` đã lên version mới** | thiếu là ô 1 rớt `assert` ngay |

---

## Bước 1b — ⭐ MÃ + PREDS LẤY TỪ DRIVE, ảnh nối bằng symlink

**Gốc rễ của hai lỗi câm ngày 20/8** là mã nằm chung dataset với ảnh: ảnh **4,1 GB** nên ngại
upload lại, thành ra mã trên Kaggle cứ là bản cũ, phải vá bằng `s.index(...)` ngay trong
notebook — rồi vá nhầm sang lớp `UGround`, im lặng, không một dòng lỗi.

Mã chỉ **456 KB**, tệp preds **3,8 MB**. Gói cả hai lên Drive thì mỗi lần sửa mã chỉ mất vài
giây, và **chỉ còn một chỗ phải đồng bộ**.

| | để ở đâu | vì sao |
|---|---|---|
| ảnh `dg1_cache` **4,1 GB** | **dataset `thesis-score`** | gắn sẵn 0 giây, không bao giờ đổi. Qua Drive là tải lại 4,1 GB mỗi phiên, `gdown` còn hay dính giới hạn lượt tải |
| mã + preds **707 KB** | **Drive** (`harness_code.zip`) | cập nhật trong 10 giây, chia sẻ cho người khác được |

⚠️ **Kaggle KHÔNG mount được Drive** như Colab (không có `drive.mount`) — chỉ tải qua link chia
sẻ. Đó là lý do phải để chế độ **"Bất kỳ ai có đường liên kết"**.
⚠️ Link mở như vậy thì **ai có link cũng tải được**. Gói này chỉ có mã và câu dự đoán, không có
dữ liệu cá nhân — nhưng vẫn là mã luận văn chưa công bố, đừng đăng link ra chỗ công khai.

**Dựng gói tại máy:**

```
python3 harness/make_code_zip.py      →  _bundles/harness_code.zip
```

Nó in ra `sha256[:12]`. **Giữ lại con số đó** — notebook sẽ in dấu vân tay của gói nó vừa tải,
hai số khớp mới chứng minh máy kia đang chạy đúng mã này. Đọc mã trên máy mình không chứng minh
được gì về máy kia; đó đúng là bài học 20/8.

⭐ **Lần cập nhật sau: dùng "Quản lý phiên bản / Manage versions" trên Drive để THAY tệp** —
ID và link giữ nguyên, khỏi sửa `DRIVE_URL`. Xoá rồi upload mới là ID đổi, link cũ chết.

```python
# ══ Ô 1 — tải mã + preds từ Drive · nối ảnh bằng symlink · KHÔNG copy 4,1 GB ══
import os, glob, shutil, subprocess, sys, hashlib
WS = "/kaggle/working"

DRIVE_URL = "https://drive.google.com/file/d/1BnunHIMGF2l816yMU5AhD4dK1G5xuHgT/view?usp=sharing"
# ↑ link gói harness_code.zip trên Drive (đặt 20/8). Cập nhật gói bằng "Quản lý phiên bản"
#   trên Drive thì ID giữ nguyên, khỏi sửa dòng này. Để rỗng = lấy mã từ dataset (bản CŨ).

DUNG_DATASET_CU = False   # chỉ True khi CỐ Ý chạy mã cũ trên dataset (bản chưa vá)

# ⛔ 20/8: DRIVE_URL rỗng thì bản trước ÂM THẦM rơi về dataset — mã CŨ, không có preds,
#    rồi rớt assert mãi tận cuối ô. Đúng kiểu lỗi câm đã cắn hai lần. Chặn ngay dòng đầu.
assert DRIVE_URL or DUNG_DATASET_CU, (
    "DỪNG: DRIVE_URL rỗng. Dán link gói harness_code.zip vào dòng trên "
    "(đặt DUNG_DATASET_CU=True nếu cố ý chạy mã cũ trên dataset).")

HAR, BUN = f"{WS}/harness", f"{WS}/bundle"
for d in (HAR, BUN):
    if os.path.islink(d): os.remove(d)
    elif os.path.exists(d): shutil.rmtree(d)
os.makedirs(HAR); os.makedirs(BUN)
PREDS_DIR = None

# ── 1. lấy MÃ (+ preds nếu gói có) ──────────────────────────────────────────
if DRIVE_URL:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "gdown"], check=True)
    z = f"{WS}/harness_code.zip"
    if os.path.exists(z): os.remove(z)
    subprocess.run(["gdown", "--fuzzy", DRIVE_URL, "-O", z], check=True)
    assert os.path.getsize(z) > 100_000, (
        "DỪNG: tệp tải về quá nhỏ — gần như chắc chắn là trang HTML báo 'cần xin quyền', "
        "không phải zip. Đặt link ở chế độ 'Bất kỳ ai có đường liên kết'.")
    # ⭐ dấu vân tay: CHỨNG MINH máy này đang chạy đúng gói vừa dựng ở máy kia
    print("sha256[:12] =", hashlib.sha256(open(z, 'rb').read()).hexdigest()[:12],
          "  ← phải khớp số make_code_zip.py in ra")
    shutil.unpack_archive(z, BUN)
    for f in glob.glob(f"{BUN}/py/*"):
        shutil.copy(f, HAR)
    if glob.glob(f"{BUN}/preds/preds_venus_*.jsonl"):
        PREDS_DIR = f"{BUN}/preds"
    nguon = "Drive"
else:
    uv = [os.path.dirname(m) for m in
          glob.glob("/kaggle/input/**/harness/score_run.py", recursive=True)]
    assert uv, "DỪNG: không thấy score_run.py trong dataset nào"
    for f in glob.glob(f"{uv[0]}/*.py") + glob.glob(f"{uv[0]}/*.yaml"):
        shutil.copy(f, HAR)
    nguon = uv[0] + "  ⚠️ DATASET, mã có thể CŨ và KHÔNG có preds venus"
print("mã ←", nguon, "·", len(glob.glob(f"{HAR}/*.py")), "tệp .py")

# ── 2. nối ẢNH bằng symlink (KHÔNG copy 4,1 GB) ─────────────────────────────
anh = glob.glob("/kaggle/input/**/dg1_cache/test_ac/test.jsonl", recursive=True)
assert anh, "DỪNG: không thấy dg1_cache/test_ac/test.jsonl — gắn dataset thesis-score chưa?"
DG = os.path.dirname(os.path.dirname(anh[0]))       # test.jsonl → test_ac → dg1_cache
os.symlink(DG, f"{HAR}/dg1_cache")
TEST = f"{HAR}/dg1_cache/test_ac"
n_anh = len(glob.glob(f"{TEST}/images/*.png"))
assert n_anh > 4000, f"DỪNG: chỉ thấy {n_anh} ảnh"
print(f"ảnh ← symlink {DG} · {n_anh} ảnh, 0 byte copy")

# ── 3. mã đã có sẵn phần đọc VENUS_*_PIXELS chưa ────────────────────────────
t = open(f"{HAR}/score_run.py", encoding="utf-8").read()
print("VENUS_MIN_PIXELS trong UIVenus:",
      "✅ có sẵn, KHỎI VÁ" if "VENUS_MIN_PIXELS" in t[t.index("class UIVenus"):]
      else "⛔ bản CŨ — ô 4 sẽ tự vá")

# ── 4. tệp preds: ưu tiên gói Drive, không có thì tìm trong dataset ─────────
P = {}
for t_ in ("venus_tran400",
           "venus_base_2532", "venus_s1_2532", "venus_s2_2532",
           "venus_base_1266", "venus_s1_1266", "venus_s2_1266",
           "venus_base_633",  "venus_s1_633",  "venus_s2_633"):
    c = (glob.glob(f"{PREDS_DIR}/preds_{t_}.jsonl") if PREDS_DIR else []) or \
        glob.glob(f"/kaggle/input/**/preds_{t_}.jsonl", recursive=True)
    if c:
        P[t_] = c[0]
        print(f"  {t_:18s} {sum(1 for _ in open(c[0])):>5} bước")
# ⛔ 20/8: bản trước quên hẳn nhánh BASE ⇒ ô 5 rớt IndexError đúng ở nhánh chứng nhân,
#    sau khi đã tiêu vài giờ GPU cho hai nhánh kia. Chặn ngay từ đây.
for lat in (2532, 1266, 633):
    co = [n for n in ("base", "s1", "s2") if f"venus_{n}_{lat}" in P]
    print(f"  lát {lat}: {co}" + ("" if len(co) == 3 else "   ⛔ THIẾU"))
if not any(all(f"venus_{n}_{lat}" in P for n in ("base", "s1", "s2"))
           for lat in (2532, 1266, 633)):
    raise SystemExit(
        "DỪNG: không lát nào đủ ba nhánh — thiếu Base là lượt chạy vô nghĩa.\n"
        + ("   Gói Drive thiếu thư mục preds/ — dựng lại bằng "
           "`python3 harness/make_code_zip.py` rồi thay tệp trên Drive."
           if PREDS_DIR else
           "   ⚠️ Ô này đang chạy nhánh DATASET (DRIVE_URL rỗng) nên không có preds venus. "
           "Dán DRIVE_URL rồi chạy lại."))
os.makedirs(f"{WS}/out", exist_ok=True)
print("\n✅ sẵn sàng — sang ô 4 (ô 2 và ô 2b KHÔNG cần chạy lại)")
```

⚠️ Dùng ô này thì **ô 2 và ô 2b không cần chạy lại** — mã trên Drive đã có sẵn phần đọc biến môi
trường, và cỡ ảnh đã dò xong. Ô 4 và ô 5 vẫn giữ `assert` kiểm vá; chúng chỉ **xác nhận**.

⛔ Vẫn giữ luật cũ: **bắt tiến trình in ra cấu hình nó thật sự dùng** (dòng `[UIVenus]` trong
log) rồi kiểm dòng đó. Đổi nguồn mã làm lỗi khó xảy ra hơn, **không** làm phép kiểm thành thừa.

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
for t in ("venus_tran400",
          "venus_base_2532", "venus_s1_2532", "venus_s2_2532",
          "venus_base_1266", "venus_s1_1266", "venus_s2_1266",
          "venus_base_633",  "venus_s1_633",  "venus_s2_633"):
    c = glob.glob(f"/kaggle/input/**/preds_{t}.jsonl", recursive=True)
    if c:
        P[t] = c[0]
        print(f"  {t:18s} {sum(1 for _ in open(c[0])):>5} bước")
assert "venus_tran400" in P, "DỪNG: chưa thấy preds_venus_tran400.jsonl — cập nhật dataset version"
# ⛔ 20/8: bản trước quên hẳn nhánh BASE ⇒ ô 5 rớt IndexError đúng ở nhánh chứng nhân,
# sau khi đã tiêu vài giờ GPU cho hai nhánh kia. Chặn ngay từ đây.
for lat in (2532, 1266, 633):
    co = [n for n in ("base", "s1", "s2") if f"venus_{n}_{lat}" in P]
    print(f"  lát {lat}: có {co}" + ("" if len(co) == 3 else "   ⛔ THIẾU"))
assert any(all(f"venus_{n}_{lat}" in P for n in ("base", "s1", "s2"))
           for lat in (2532, 1266, 633)), \
    "DỪNG: không lát nào có ĐỦ ba nhánh base·s1·s2 — thiếu Base là lượt chạy vô nghĩa"
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

## Ô 2b — VÁ + DÒ CỠ ẢNH (một ô duy nhất, ~15 phút)

Bản `score_run.py` trên dataset Kaggle là bản working tree cũ: lớp `UIVenus` **ghi cứng**
`min_pixels=2000000, max_pixels=4800000`, chưa đọc biến môi trường. Đó là lý do lượt dò đầu ra
trùng nhau — và cũng xác nhận lượt thăm dò 1,57% chạy ở **3.354 token (1092×2408)**.

⛔ **Bẫy đã cắn một lần.** `s.index("self.proc = AutoProcessor.from_pretrained(")` lấy lần xuất
hiện **đầu tiên trong file**, mà đó là của lớp **`UGround`** đứng trước `UIVenus`. Vá kiểu đó
sửa nhầm `UGround`; chạy `--grounder uivenus` thì lớp bị vá không được gọi lần nào ⇒ không có
dòng `[UIVenus]`, ba cỡ vẫn trùng, **không một lỗi nào**. Ô dưới neo tìm kiếm **trong lớp
`UIVenus`** và `assert` hai chiều.

⛔ **Luật chọn cỡ, khoá trước khi nhìn:** chọn theo sai số trên **câu chuẩn của người**
(`--mode gate`). Câu chuẩn giống hệt ở mọi nhánh nên cỡ chọn kiểu này **không thể** thiên vị S1
hay S2. **CẤM** dò cỡ bằng điểm của một nhánh — đó là chỉnh dụng cụ theo kết quả.

```python
# ══ VÁ + DÒ CỠ ẢNH — một ô duy nhất, chạy lại nhiều lần không sao ══
import os, shutil, glob, ast, subprocess, json, time
WS = "/kaggle/working"

# ── 1. chép lại harness SẠCH từ dataset (xoá dấu vết ô vá hỏng trước đó) ────
mp = glob.glob("/kaggle/input/**/harness/score_run.py", recursive=True)
assert mp, "DỪNG: không thấy harness/score_run.py trong dataset"
if os.path.exists(f"{WS}/harness"):
    shutil.rmtree(f"{WS}/harness")
shutil.copytree(os.path.dirname(mp[0]), f"{WS}/harness")
SR = f"{WS}/harness/score_run.py"
print("① đã chép lại harness sạch từ", mp[0])

# ── 2. vá, NEO TRONG LỚP UIVenus (đừng vá nhầm UGround đứng trước nó) ───────
s = open(SR, encoding="utf-8").read()
c = s.index("class UIVenus")
het = s.find("\ndef ", c)
i = s.index("self.proc = AutoProcessor.from_pretrained(", c)
assert i < het, "DỪNG: không thấy from_pretrained bên trong lớp UIVenus"
j = s.index("(", i); d = 0
for k in range(j, len(s)):
    d += (s[k] == "(") - (s[k] == ")")
    if d == 0:
        j = k + 1; break
print("\n② mã CŨ trong UIVenus:\n" + s[i:j])
open(SR, "w", encoding="utf-8").write(s[:i] + '''mn = int(os.environ.get("VENUS_MIN_PIXELS", 2000000))
        mx = int(os.environ.get("VENUS_MAX_PIXELS", 4800000))
        self.proc = AutoProcessor.from_pretrained(path, min_pixels=mn, max_pixels=mx)
        ip = self.proc.image_processor
        if isinstance(getattr(ip, "size", None), dict):
            ip.size = {"shortest_edge": mn, "longest_edge": mx}
        ip.min_pixels, ip.max_pixels = mn, mx
        print(f"[UIVenus] xin min={mn} max={mx} -> giu min={getattr(ip,'min_pixels',None)} "
              f"max={getattr(ip,'max_pixels',None)} size={getattr(ip,'size',None)}", flush=True)''' + s[j:])

t = open(SR, encoding="utf-8").read(); ast.parse(t)
cv = t.index("class UIVenus")
assert "VENUS_MIN_PIXELS" in t[cv:], "⛔ vá không nằm trong UIVenus"
assert "VENUS_MIN_PIXELS" not in t[:cv], "⛔ vá lọt sang lớp trước UIVenus"
print("   vá nằm đúng trong UIVenus ✅ · UGround nguyên vẹn:",
      "VENUS_" not in t[t.index("class UGround"):cv])

# ── 3. dò ba cỡ ảnh ─────────────────────────────────────────────────────────
CO = [(200704, 1003520, "1.272 token  (672×1484)"),
      (200704, 2007040, "2.475 token  (924×2100)"),
      (2000000, 4800000, "3.354 token  (1092×2408)")]
os.makedirs(f"{WS}/out", exist_ok=True)
kq = []
print("\n③ dò cỡ ảnh — 3 lượt × 30 bước")
for mn, mx, ten in CO:
    tag = f"do_{mx//1000}k"
    for e in (f"{WS}/out/{tag}.json", f"{WS}/out/{tag}_raw.jsonl"):
        if os.path.exists(e): os.remove(e)        # cấu hình khác ⇒ KHÔNG nối tiếp
    env = {**os.environ, "VENUS_MIN_PIXELS": str(mn), "VENUS_MAX_PIXELS": str(mx)}
    t0 = time.time()
    with open(f"{WS}/out/{tag}.log", "w") as f:
        subprocess.run(["python", "-u", SR, "--mode", "gate", "--grounder", "uivenus",
                        "--n", "30", "--out", f"{WS}/out/{tag}.json"],
                       stdout=f, stderr=subprocess.STDOUT, cwd=WS, env=env)
    lg = open(f"{WS}/out/{tag}.log", encoding="utf-8", errors="ignore").read()
    bang = next((l for l in lg.splitlines() if "[UIVenus]" in l), "⛔ KHÔNG THẤY dòng [UIVenus]")
    jj = json.load(open(f"{WS}/out/{tag}.json"))
    gy = (time.time() - t0 - 90) / 30
    kq.append((ten, jj["median_err"], jj["p75_err"], gy))
    print(f"\n  {ten}\n    {bang}\n    trung vị {jj['median_err']:.3%} · p75 {jj['p75_err']:.3%}"
          f" · ~{gy:.1f} s/bước", flush=True)

print(f"\n{'cấu hình':<28}{'trung vị':>10}{'p75':>10}{'s/bước':>9}")
for ten, m, p75, gy in kq:
    print(f"  {ten:<26}{m:>9.3%}{p75:>10.3%}{gy:>8.1f}")
print("\n  mốc UGround trên ĐÚNG 30 bước này: trung vị 0,600% · p75 3,600% · ≤3%: 73,3%")

if len({round(r[1], 6) for r in kq}) == 1:
    print("\n⚠️ BA CỠ RA TRÙNG NHAU. Đọc ba dòng [UIVenus] ở trên:")
    print("   · min/max KHÁC nhau ở ba dòng ⇒ cỡ ảnh ĐÃ đổi thật mà sai số không đổi")
    print("     ⇒ KẾT LUẬN THẬT: cỡ ảnh không phải nguyên nhân. Chốt 3.354 token, sang ô 4.")
    print("   · min/max giống nhau, hoặc thiếu dòng ⇒ vá chưa ăn, báo lại.")
else:
    best = min(kq, key=lambda r: r[1])
    print(f"\n⇒ chọn: {best[0]} — trung vị {best[1]:.3%}, {best[3]:.1f} s/bước")
    print("   Dùng VENUS_MIN/MAX_PIXELS của cỡ này Y HỆT cho ô 4 và ô 5.")
```

### Đọc ô 2b — ⛔ ĐỪNG chọn theo trung vị

Kết quả 20/8, ba cỡ đổi thật (ba dòng `[UIVenus]` khác nhau):

| cỡ | trung vị | p75 | s/bước |
|---|---|---|---|
| 1.272 tok | 1,984% | 36,75% | **1,4** |
| 2.475 tok | **1,224%** | 36,79% | 5,2 |
| 3.354 tok | 1,568% | **28,87%** | 8,3 |

⛔ **Trung vị và p75 chỉ ngược nhau ⇒ luật "chọn trung vị thấp nhất" của bản runbook đầu là
SAI tiêu chí.** Thước là quyết định **ngưỡng**: `hit_disk` đòi `|dx| ≤ 0,14·W` và
`|dy| ≤ 0,14·H`. Trung vị 1,2% hay 1,6% đều thừa sức nằm trong dung sai — chênh lệch ở đó
**không đổi một bước nào**. Thứ quyết định điểm là **cái đuôi**: bao nhiêu bước bắn ra ngoài
14%. Chọn theo trung vị là chọn theo con số không liên quan tới đại lượng đang đo.

⇒ Chọn bằng **ô 2d**, theo `hit_disk` và trần Voronoi. Vẫn đo trên **câu chuẩn của người** nên
luật cũ giữ nguyên: không thể thiên vị S1 hay S2.

---

## Ô 2d — CHỌN CỠ THEO TRẦN (0 giây GPU)

Đọc lại ba tệp thô, tính đúng đại lượng thước dùng. **Chạy SAU ô 4**, khi mỗi tệp đã có 300 bước
— ở 30 bước KTC rộng ±15 điểm nên không quyết được gì.

Mốc UGround trên **đúng các bước ấy** (ô tự chọn hàng theo cỡ mẫu):

| n | `hit_disk` | >14% | ≤3% | trần Voronoi |
|---|---|---|---|---|
| 30 | 83,3% | 16,7% | 73,3% | 80,0% [63,3 – 93,3] |
| **300** | **81,3%** | **21,0%** | **62,7%** | **70,0% [64,5 – 75,3]** |

⚙️ **Ô 2d không cần GPU** (chỉ đọc tệp thô), nhưng phần trần Voronoi **cần Internet** để tải cây
trợ năng. Đừng đổi Accelerator để chạy nó — Kaggle khởi động lại nhân, không đáng.

⚠️ Ô tự tìm `harness` — ưu tiên bản trong `/kaggle/working`, không có thì lấy thẳng từ dataset.
Phần trần Voronoi gọi `buttons_of` nên cần cây trợ năng, lượt đầu tải từ HuggingFace mất vài
phút; phần `hit_disk` không cần gì và chạy tức thì, nên hỏng phần Voronoi vẫn chọn được.

```python
# ══ Ô 2D — CHỌN CỠ THEO TRẦN, không theo trung vị · 0 giây GPU ══
import json, os, sys, glob, subprocess
WS = "/kaggle/working"

H = next((d for d in [f"{WS}/harness"] +
          [os.path.dirname(p) for p in
           glob.glob("/kaggle/input/**/harness/metric_exec.py", recursive=True)]
          if os.path.exists(f"{d}/metric_exec.py")), None)
assert H, "DỪNG: không thấy metric_exec.py ở đâu cả"
sys.path.insert(0, H)
import metric_exec as M
print("harness →", H)

GY  = {1003: 4.0, 2007: 7.2, 4800: 8.3}     # s/bước ĐO THẬT trên 300 bước ở ô 4
PX  = {1003: (200704, 1003520), 2007: (200704, 2007040), 4800: (2000000, 4800000)}
TEN = {1003: "1.272 tok (672×1484)", 2007: "2.475 tok (924×2100)",
       4800: "3.354 tok (1092×2408)"}

print(f"\n{'cỡ ảnh':<26}{'hit_disk':>10}{'>14%':>8}{'≤3%':>8}{'trung vị':>10}"
      f"{'p75':>9}{'s/bước':>9}")
print("─" * 80)
kq, n, chi_tiet = {}, 0, {}
for k in (1003, 2007, 4800):
    p = f"{WS}/out/do_{k}k_raw.jsonl"
    if not os.path.exists(p):
        print(f"  {TEN[k]:<24} ⏳ chưa chạy (thiếu {os.path.basename(p)})"); continue
    o = [json.loads(l) for l in open(p, encoding="utf-8")]
    if len(o) < 300:
        print(f"  {TEN[k]:<24} ⏭️  bỏ qua, mới {len(o)}/300 bước — so với cỡ đủ 300 là "
              "so nhầm cỡ mẫu"); continue
    hd = sum(M.hit_disk(tuple(x["pred_xy"]), tuple(x["gold_xy"]), tuple(x["wh"]))
             for x in o if x.get("pred_xy"))
    # bản ghi của bước bộ trỏ không trả toạ độ chỉ có `bo_qua`, KHÔNG có `err_frac`
    e = sorted(x["err_frac"] for x in o if "err_frac" in x)
    hong = len(o) - len(e)
    q = lambda f: e[min(int(f * len(e)), len(e) - 1)] if e else 1.0
    kq[k], n = hd / len(o), len(o)
    chi_tiet[k] = (q(.5), q(.75), hong)
    print(f"  {TEN[k]:<24}{hd/len(o):>9.1%}{(sum(1 for v in e if v > .14)+hong)/len(o):>8.1%}"
          f"{sum(1 for v in e if v <= .03)/len(o):>8.1%}{q(.5):>9.2%}{q(.75):>9.2%}"
          f"{GY[k]:>9.1f}" + (f"   ⚠️ {hong} bước trượt khuôn" if hong else ""))

MOC = {30: (0.833, 0.167, 0.733, "80,0% [63,3–93,3]"),
       300: (0.813, 0.210, 0.627, "70,0% [64,5–75,3]")}
m = MOC.get(n, MOC[300])
print(f"  {'UGround (mốc, n=' + str(n) + ')':<24}{m[0]:>9.1%}{m[1]:>8.1%}{m[2]:>8.1%}"
      f"{0.0073:>9.2%}{0.0908:>9.2%}{'~4.5':>9}")   # p75 của UGround ở n=300 là 9,08%
                                                       # (3,60% là mốc n=30, đừng dùng lẫn)
print(f"\n  Trần Voronoi của UGround trên đúng {n} bước này: {m[3]}")
print("  ⛔ Đọc theo hit_disk và TRẦN, không theo trung vị: thước là quyết định NGƯỠNG")
print("     (|dx|≤0,14·W ∧ |dy|≤0,14·H), nên 1,2% hay 1,6% không đổi một bước nào —")
print("     thứ quyết định điểm là cái ĐUÔI, bao nhiêu bước bắn ra ngoài 14%.")

# ── trần Voronoi = thước chính; cần cây trợ năng nên lượt đầu tải vài phút ──
print(f"\n── trần Voronoi (thước chính) — mốc UGround {m[3]} ──", flush=True)
GA, tran = f"{H}/gate_a_ceiling.py", {}
for k in kq:
    r = subprocess.run([sys.executable, GA, "--raw", f"{WS}/out/do_{k}k_raw.jsonl",
                        "--out", f"{WS}/out/tran_{k}k.json"],
                       capture_output=True, text=True, cwd=os.path.dirname(H) or WS)
    try:
        j = json.load(open(f"{WS}/out/tran_{k}k.json"))
        tran[k] = (j["ceiling_voronoi"], j["ci_voronoi"])
        print(f"  {TEN[k]:<24}{j['ceiling_voronoi']:>7.1%}  KTC95 "
              f"[{j['ci_voronoi'][0]:.1%}, {j['ci_voronoi'][1]:.1%}]"
              f"   ·  đĩa {j['ceiling_disk']:.1%} · {j['n']} bước", flush=True)
    except Exception:
        print(f"  {TEN[k]:<24} ⛔ {(r.stderr or r.stdout)[-160:]}", flush=True)

# ── kết luận: chọn cỡ, in thẳng hai dòng để dán vào ô 5 ─────────────────────
print("\n" + "═" * 80)
if not kq:
    print("⛔ chưa cỡ nào đủ 300 bước — chạy ô 4 trước")
else:
    chong = (len(tran) > 1 and
             max(t[1][0] for t in tran.values()) < min(t[1][1] for t in tran.values()))
    if len(tran) > 1 and not chong:
        best = max(tran, key=lambda k: tran[k][0]); ly_do = "trần Voronoi cao nhất"
    elif len(tran) > 1:
        best = min(tran, key=lambda k: GY[k])
        ly_do = ("KTC95 của các trần CHỒNG LÊN NHAU ⇒ trần không phân biệt được ở "
                 f"n={n}, chọn cỡ NHANH NHẤT (phải khai đúng vậy trong bài)")
    elif len(kq) > 1:
        best = max(kq, key=kq.get)
        ly_do = ("⚠️ trần Voronoi KHÔNG tính được (xem lỗi ở trên — thường là chưa tải "
                 "được cây trợ năng, cần Internet ON) ⇒ tạm chọn theo hit_disk cao nhất. "
                 "Chạy lại phần trần trước khi chốt nếu còn thời gian.")
    else:
        best = max(kq, key=kq.get); ly_do = "cỡ duy nhất đủ 300 bước"
    mn, mx = PX[best]
    print(f"⇒ CHỌN {TEN[best]} — {ly_do}")
    print(f"\n   DÁN HAI DÒNG NÀY VÀO Ô 5:")
    print(f"       LAT    = 2532")
    print(f"       MN, MX = {mn}, {mx}")
    print(f"   và vào Ô 6:  CO_DA_CHON = {best}")
    print(f"\n   giá ô 5 ở cỡ này ({GY[best]} s/bước) — 3 nhánh Base·S1·S2:")
    for lat in (2532, 1266, 633):
        h = lat * 3 * GY[best] / 3600
        print(f"     lát {lat:>5}: {lat*3:>5} lượt gọi · {h:5.1f} giờ"
              f"{'  ✅ gọn một phiên' if h <= 11 else '  ⚠️ phải cắt phiên'}")
    if best in tran:
        nen = 70.0 - tran[best][0] * 100
        print(f"\n⭐ MỨC NÉN THANG ĐO (cần cho mục Bẫy pha loãng): trần UI-Venus "
              f"{tran[best][0]:.1%} vs UGround 70,0% trên đúng {n} bước ⇒ tụt {nen:.1f} điểm.")
        print("   Tụt sâu thì Δ(S2−S1) co về 0 vì lý do CƠ HỌC — bắt buộc đọc kèm chứng nhân")
        print("   S1−Base, đó là lý do ô 5 phải chấm cả nhánh Base.")
```


*(Ô 2c cũ — kiểm `image_grid_thw` bằng bộ xử lý ảnh, không cần GPU — đã xong việc và bị gỡ.
Kết quả: ảnh 1080×2400 cho grid **1.272 / 2.475 / 3.354** token ở ba mức `max_pixels`, xác nhận
cơ chế đổi cỡ hoạt động. Ô 2b nay tự in dòng `[UIVenus]` nên không cần ô kiểm riêng.)*

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

## Ô 3 — chọn cỡ lát *(nay không cần chạy — số đã đo xong)*

Ba nhánh phải chấm: **Base · S1 · S2**. Base là **chứng nhân** chống bẫy pha loãng, không phải
phần thêm cho đủ bộ — thiếu nó thì lượt chạy không trả lời được câu hỏi ban đầu.

Ô cũ hỏi `input("giây/bước")` rồi tự tính. Nay ô 4 đã đo tốc độ thật trên 300 bước nên bảng
dưới **tính sẵn**, khỏi chạy ô nào (`giờ = lát × 3 nhánh × s/bước ÷ 3600`):

| lát | lượt gọi | ở **1.272 tok** (4,0 s) | ở **2.475 tok** (7,2 s) |
|---|---|---|---|
| **2.532** (đủ) | 7.596 | **8,4 h** ✅ gọn một phiên | 15,2 h ⚠️ cắt hai phiên |
| 1.266 (½) | 3.798 | 4,2 h ✅ | 7,6 h ✅ |
| 633 (¼) | 1.899 | 2,1 h ✅ | 3,8 h ✅ |

**Luật chọn, khoá trước khi nhìn kết quả:** lấy **lát lớn nhất mà quota cho phép** ⇒ **2.532**.
Lát 633 chỉ đọc được **dấu**, không đọc được độ lớn — dùng được, nhưng phải khai đúng vậy trong bài.

⚠️ Cộng thêm ~5 phút mỗi nhánh để nạp mô hình 7B vào VRAM (ô 5 chạy ba tiến trình riêng ⇒ nạp
ba lần; trọng số đã nằm trong cache HF của phiên nên không tải lại từ mạng). Cộng cổng A ~1 giờ,
cả phép B ≈ **9,7 giờ** — trong quota 30 giờ/tuần.

### ⭐ Kết quả ô 4 + ô 2d (20/8) — cỡ đã chốt **1.272 tok**, thang đo **không bị nén**

| n=300, câu chuẩn của người | `hit_disk` | >14% | ≤3% | trung vị | p75 | trần Voronoi | s/bước |
|---|---|---|---|---|---|---|---|
| **UI-Venus 1.272 tok** ⭐ chọn | 75,0% | 26,0% | 60,7% | 1,63% | 16,35% | **69,3%** [63,8–74,8] | **4,0** |
| UI-Venus 2.475 tok | 74,7% | 26,0% | 61,7% | 1,43% | 17,73% | 68,7% [62,9–74,1] | 7,2 |
| UGround (mốc) | 81,3% | 21,0% | 62,7% | 0,73% | 3,60% | **70,0%** [64,5–75,3] | ~4,5 |

**Chọn 1.272 tok vì KTC95 hai trần chồng nhau** ⇒ trần không phân biệt được ở n=300, luật đã
khoá bảo lấy cỡ **nhanh nhất**. Phải khai đúng như vậy trong bài, đừng viết là "cỡ tốt nhất".

⭐ **Mức nén thang đo chỉ 0,7 điểm** (69,3 vs 70,0). Đây là điều kiện sống của phép B: dụng cụ
mới **không** tệ hơn đáng kể, nên Δ(S2−S1) co về 0 sẽ **không** giải thích được bằng pha loãng.
⚠️ Vẫn phải chấm Base — 0,7 điểm là hiệu **không ghép cặp** với KTC ±5,5, chưa loại được mức nén
cỡ vài điểm. `phan_tich_venus.py` so **ghép cặp từng bước** trên đúng 300 bước này nên chặt hơn
hẳn; và S1−Base là chứng nhân trực tiếp.

⭐ **Điều đáng chú ý về THƯỚC:** UI-Venus thua rõ ở *sai số khoảng cách* (trung vị 1,63% vs
0,73%, p75 16,35% vs 3,60% — gấp 4,5 lần) nhưng **trần gần y hệt**. Vì thước là quyết định
**ngưỡng** rồi mới Voronoi: lệch 1,6% hay 0,7% đều nằm sâu trong dung sai 14%, không đổi một
bước nào. Đúng lập luận đã khoá trước ở ô 2b — nay có số của một dụng cụ thứ hai chứng minh.
⛔ Nên **rút** câu cũ *"UI-Venus kém hơn UGround trên ảnh này"* (suy từ 30 bước, cỡ ảnh sai):
nói đúng là **kém hơn ở sai số khoảng cách, ngang nhau ở trần của thước**.

## Ô S — SAO LƯU tệp thô ra ngoài phiên (chạy TRƯỚC ô 4 và ô 5)

**Vì sao tệp mất.** `/kaggle/working` là đĩa **tạm của phiên**: đóng notebook, restart nhân,
hoặc hết 12 giờ là xoá sạch. Chỉ Output của một *Save Version* đã commit mới sống sót — mà
commit thì chạy lại notebook từ đầu, không cứu được lượt đang chạy.

⚠️ **Kaggle KHÔNG mount được Drive** như Colab. Lúc train trên Colab `drive.mount` ghi thẳng
điểm lưu mỗi 200 bước được; ở đây muốn ghi ra ngoài thì phải có credential. Cách nhẹ nhất là
đẩy lên **một dataset Kaggle riêng** bằng chính API token của bạn — vai trò giống hệt
"đồng bộ Drive mỗi 5 phút" của runbook Colab.

**Setup một lần, ~5 phút:**

| | làm gì |
|---|---|
| 1 | kaggle.com → ảnh đại diện → **Settings** → mục **API** → **Create New Token** → tải về `kaggle.json` |
| 2 | Mở tệp đó, lấy `username` và `key` |
| 3 | Trong notebook: **Add-ons → Secrets → Add a new secret**, tạo **hai** secret tên đúng `KAGGLE_USERNAME` và `KAGGLE_KEY`, rồi bật nút gắn chúng vào notebook này |

⛔ Không dán `kaggle.json` vào ô mã — ô mã nằm trong notebook, mà notebook chia sẻ được.
Secrets không hiện ra trong bản chia sẻ.

```python
# ══ Ô S — bật sao lưu tự động · dùng API Python (KHÔNG qua CLI) ══
# ⛔ Bản trước gọi `kaggle` CLI: tqdm của nó in thanh tiến trình ra stdout, thông điệp lỗi
#    thật bị đẩy ra khỏi 200 ký tự cuối ⇒ in ⛔ mà không biết hỏng ở đâu. Đúng bẫy log ngập
#    đã làm treo một lượt Kaggle 7 giờ. API Python có quiet=True và ném Exception rõ ràng.
import os, json, glob, shutil, sys, time, stat
WS  = "/kaggle/working"
BAK = f"{WS}/backup"
DS_SLUG  = "venus-out"          # tên dataset sao lưu, tự tạo ở lần đầu
MOI_GIAY = 1200                 # 20 phút một lần

try:
    from kaggle_secrets import UserSecretsClient
    _us = UserSecretsClient()
    USER, KEY = _us.get_secret("KAGGLE_USERNAME"), _us.get_secret("KAGGLE_KEY")
except Exception as e:
    raise SystemExit("DỪNG: chưa gắn secret KAGGLE_USERNAME / KAGGLE_KEY.\n"
                     "   Add-ons → Secrets → tạo hai secret rồi BẬT cho notebook này.\n"
                     f"   ({type(e).__name__}: {e})")

_kd = os.path.expanduser("~/.kaggle"); os.makedirs(_kd, exist_ok=True)
json.dump({"username": USER, "key": KEY}, open(f"{_kd}/kaggle.json", "w"))
os.chmod(f"{_kd}/kaggle.json", stat.S_IRUSR | stat.S_IWUSR)
os.environ["KAGGLE_USERNAME"], os.environ["KAGGLE_KEY"] = USER, KEY

from kaggle.api.kaggle_api_extended import KaggleApi
_api = KaggleApi(); _api.authenticate()
DS_ID = f"{USER}/{DS_SLUG}"
_lan_cuoi = [0.0]

def _co_dataset():
    """Dataset đã tồn tại chưa — hỏi Kaggle, đừng đoán."""
    try:
        return len(_api.dataset_list_files(DS_ID).files) >= 0
    except Exception:
        return False

def sao_luu(msg="", ep=False):
    """Đẩy tệp thô lên dataset. KHÔNG BAO GIỜ ném lỗi — sao lưu hỏng thì lượt chạy vẫn
    phải đi tiếp; mất bản sao còn hơn mất cả lượt vì một lỗi mạng."""
    if not ep and time.time() - _lan_cuoi[0] < MOI_GIAY:
        return
    _lan_cuoi[0] = time.time()
    try:
        os.makedirs(BAK, exist_ok=True)
        n = mb = 0
        for f in glob.glob(f"{WS}/out/*"):
            if os.path.isfile(f) and os.path.getsize(f) > 0:
                shutil.copy(f, BAK); n += 1; mb += os.path.getsize(f) / 2**20
        if not n:
            print("  [sao lưu] chưa có tệp nào để đẩy", flush=True); return
        json.dump({"title": "thesis venus out", "id": DS_ID,
                   "licenses": [{"name": "CC0-1.0"}]},
                  open(f"{BAK}/dataset-metadata.json", "w"))
        t0 = time.time()
        if _co_dataset():
            _api.dataset_create_version(BAK, version_notes=msg or time.strftime("%H:%M:%S"),
                                        quiet=True, dir_mode="zip")
            viec = "version mới"
        else:
            _api.dataset_create_new(BAK, public=False, quiet=True, dir_mode="zip")
            viec = "TẠO dataset"
        print(f"  [sao lưu] {viec} · {n} tệp · {mb:.1f} MB · {time.time()-t0:.0f}s "
              f"→ {DS_ID} ✅", flush=True)
    except Exception as e:
        print(f"  [sao lưu] ⛔ bỏ qua, lượt chạy VẪN TIẾP: {type(e).__name__}: "
              f"{str(e)[:200]}", flush=True)

# ── chạy thử ngay + XÁC MINH bằng cách hỏi lại Kaggle, không tin lệnh đẩy ──────
sao_luu("khoi tao", ep=True)
time.sleep(20)                      # Kaggle xử lý version mất vài giây
try:
    fs = _api.dataset_list_files(DS_ID).files
    print(f"\n✅ XÁC MINH: dataset {DS_ID} đang có {len(fs)} tệp")
    # ⚠️ tên thuộc tính kích thước đổi giữa các đời kaggle (2.0.2 KHÔNG có totalBytes)
    # ⇒ dò nhiều tên, thiếu hết thì nói "?" chứ đừng in 0 KB làm tưởng tệp rỗng
    for f in list(fs)[:8]:
        kb = next((getattr(f, k) for k in ("totalBytes", "size", "total_bytes", "fileSize")
                   if isinstance(getattr(f, k, None), (int, float))), None)
        print(f"     {f.name}  " + (f"{kb/2**10:.0f} KB" if kb else "kích thước: ?"))
    print("   (kích thước '?' là do đời thư viện, KHÔNG phải tệp rỗng — muốn chắc thì mở "
          "link dưới xem trên web)")
    print(f"   Tải về: kaggle.com/datasets/{DS_ID}")
    print(f"   ⇒ sao lưu BẬT · mỗi {MOI_GIAY//60} phút · ép đẩy mỗi khi xong một nhánh")
except Exception as e:
    print(f"\n⛔ CHƯA XÁC MINH ĐƯỢC: {type(e).__name__}: {str(e)[:300]}")
    print("   Nếu vừa TẠO dataset thì Kaggle cần ~1 phút xử lý — chạy lại ô này.")
    print("   Còn báo lỗi quyền: token hết hạn hoặc secret dán nhầm, tạo token mới.")
```


Ô 4 và ô 5 **tự gọi `sao_luu()`** trong vòng theo dõi nếu ô này đã chạy; chưa chạy ô S thì
chúng chạy bình thường, chỉ là không có bản sao. Mỗi nhánh xong là **ép** đẩy một lần.

⚠️ Lượt đầu `kaggle datasets create` mất ~30 giây và dataset ở chế độ **riêng tư**. Từ lần sau
mỗi lần đẩy là một **Version** mới — mở lịch sử version là thấy được từng mốc.

---

## Ô S2 — VÁ sao lưu khi `kaggle` bản cũ lỗi `'token'`

**Triệu chứng (gặp 20/8):** ô S in `Error while trying to load upload info:
KaggleObject.from_dict() got an unexpected keyword argument 'token'` — **một dòng cho mỗi tệp** —
rồi vẫn in `✅`. Đó là bug tương thích của `kaggle 2.0.2` (bản Kaggle cài sẵn) với API mới; nó
hỏng đúng ở khâu lấy thông tin upload từng tệp, nên **tệp có thể không được đính vào version**
trong khi hàm không ném lỗi. Kiểu hỏng câm quen thuộc: lệnh "thành công", việc không xảy ra.

⇒ Chỉ tin dòng **XÁC MINH** (hỏi lại Kaggle xem dataset có mấy tệp). Nếu nó báo **0 tệp** hoặc
lỗi, chạy ô này: nâng `kaggle` lên bản mới rồi đẩy qua **tiến trình con** — tiến trình mới nạp
bản mới nên **không cần restart nhân** (restart là mất hết tệp thô trong `/kaggle/working`).

```python
# ══ Ô S2 — nâng cấp kaggle rồi sao lưu qua tiến trình con · đè hàm sao_luu của ô S ══
import os, json, glob, shutil, sys, time, subprocess
WS, BAK = "/kaggle/working", "/kaggle/working/backup"
DS_ID = f"{os.environ['KAGGLE_USERNAME']}/venus-out"     # ô S đã đặt biến môi trường
MOI_GIAY = 1200

r = subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--upgrade", "kaggle"],
                   capture_output=True, text=True)
ver = subprocess.run(["kaggle", "--version"], capture_output=True, text=True).stdout.strip()
print("kaggle CLI:", ver or r.stderr[-200:])

def _loc(txt):
    """Bỏ thanh tiến trình và dòng Warning — thứ đã nuốt mất thông điệp lỗi thật."""
    return [l.strip() for l in txt.replace("\r", "\n").splitlines()
            if l.strip() and "%|" not in l and not l.startswith("Warning:")]

def _dem_tep():
    """Hỏi Kaggle dataset đang có mấy tệp — KHÔNG suy từ mã thoát của lệnh đẩy."""
    r = subprocess.run(["kaggle", "datasets", "files", "-d", DS_ID, "--csv"],
                       capture_output=True, text=True)
    d = [l for l in _loc(r.stdout) if "," in l and not l.startswith("name,")]
    return len(d), d[:8]

_lan_cuoi = [0.0]
def sao_luu(msg="", ep=False):
    if not ep and time.time() - _lan_cuoi[0] < MOI_GIAY: return
    _lan_cuoi[0] = time.time()
    try:
        os.makedirs(BAK, exist_ok=True)
        n = mb = 0
        for f in glob.glob(f"{WS}/out/*"):
            if os.path.isfile(f) and os.path.getsize(f) > 0:
                shutil.copy(f, BAK); n += 1; mb += os.path.getsize(f) / 2**20
        if not n:
            print("  [sao lưu] chưa có tệp nào để đẩy", flush=True); return
        json.dump({"title": "thesis venus out", "id": DS_ID,
                   "licenses": [{"name": "CC0-1.0"}]},
                  open(f"{BAK}/dataset-metadata.json", "w"))
        t0 = time.time()
        r = subprocess.run(["kaggle", "datasets", "version", "-p", BAK, "-r", "zip",
                            "-m", msg or time.strftime("%H:%M:%S")],
                           capture_output=True, text=True)
        if r.returncode != 0 and "404" in (r.stdout + r.stderr):
            r = subprocess.run(["kaggle", "datasets", "create", "-p", BAK, "-r", "zip"],
                               capture_output=True, text=True)
        cuoi = (_loc(r.stdout + r.stderr) or ["(không có output)"])[-1][:120]
        print(f"  [sao lưu] {n} tệp · {mb:.1f} MB · {time.time()-t0:.0f}s · {cuoi}", flush=True)
    except Exception as e:
        print(f"  [sao lưu] ⛔ bỏ qua, lượt chạy VẪN TIẾP: {type(e).__name__}: {str(e)[:200]}",
              flush=True)

sao_luu("va bang CLI moi", ep=True)
time.sleep(25)
n, ds = _dem_tep()
print(f"\n{'✅' if n else '⛔'} XÁC MINH: {DS_ID} đang có {n} tệp")
for d in ds: print("    ", d[:90])
if not n:
    print("⛔ VẪN 0 TỆP. Đừng chạy ô 5 mà trông vào sao lưu này — hoặc bỏ sao lưu và chấp nhận")
    print("   rủi ro, hoặc tải tay `/kaggle/working/out/*_raw.jsonl` từ panel Output sau mỗi nhánh.")
else:
    print(f"⇒ sao lưu BẬT · mỗi {MOI_GIAY//60} phút · kaggle.com/datasets/{DS_ID}")
```

⚠️ **Chạy ô S2 xong mới chạy ô 5** — ô S2 định nghĩa đè hàm `sao_luu`, ô 5 sẽ tự dùng bản mới.
⛔ **Đừng restart nhân để "cho chắc"**: tiến trình con đã nạp `kaggle` bản mới rồi, mà restart
thì mất tệp thô đang có trong `/kaggle/working`.

## Ô 4 — cổng A 300 bước cho **CẢ BA CỠ**, rồi mới chọn (~67 phút)

**Vì sao không chọn ở ô 2d.** Trần Voronoi của UGround trên đúng 30 bước ấy là **80,0%** với
KTC95 **[63,3 – 93,3]** — rộng **±15 điểm**. Ở n=30 mỗi bước đáng 3,3 điểm, nên ba cỡ chênh
nhau vài điểm là **nhiễu lấy mẫu thuần**. Ở n=300 thì KTC còn **±5,4 điểm** (đo được ở lượt
cổng A của UGround: 70,0% [64,5 – 75,3]) — phân biệt được chênh lệch từ ~7 điểm trở lên.

**Vì sao rẻ.** Ba tệp thô ô 2b đã có sẵn **30 bước mỗi cỡ**, và `--n 300` lấy đúng 300 bước đầu
của cùng danh sách xáo bằng hạt giống 20260805 ⇒ 30 bước cũ là **tập con**, `score_run.py` nối
tiếp, chỉ chấm thêm 270 bước mỗi cỡ:

| cỡ | s/bước | 270 bước |
|---|---|---|
| 1.272 tok | 1,4 | **6 phút** |
| 2.475 tok | 5,2 | 23 phút |
| 3.354 tok | 8,3 | 37 phút |

### Kết quả thật của ô 4 (chạy 20/8) — cỡ 3.354 tok **BỊ LOẠI**

| cỡ | 300 bước | s/bước thật | trung vị | p75 |
|---|---|---|---|---|
| 1.272 tok | 22 phút ✅ | **4,0** | 1,56% | **16,16%** |
| 2.475 tok | 38 phút ✅ | **7,2** | **1,43%** | 17,68% |
| 3.354 tok | ⛔ **CUDA OOM ở ~bước 100** | 8,3 | — | — |

⛔ **Cỡ 3.354 token không chạy được trên T4×2.** Xin thêm 3,41 GiB khi chỉ còn trống 3,06 GiB,
tràn trong `scaled_dot_product_attention` — ảnh to thì bảng attention của khối thị giác phình
theo **bình phương** số patch. Ô 2b sống sót ở 30 bước chỉ vì chưa gặp ảnh đủ cao; tới ~100 bước
là gặp. ⇒ Loại vì **phần cứng**, không phải vì điểm — lý do này độc lập với S1/S2 nên không đụng
luật chọn cỡ. Khai đúng như vậy trong bài. Đừng cứu bằng `expandable_segments`: phân mảnh chỉ
185 MB, mà lượt ô 5 ở cỡ này tốn **17,5 giờ** trên đúng cấu hình vừa chứng minh là tràn.

⭐ **s/bước của ô 2b là số ẢO** — công thức `(t − 90)/30` trừ khống thời gian tải mô hình. Lấy
số đo trên 300 bước: 4,0 và 7,2 s/bước. Giá ô 5 (2.532 bước × 3 nhánh): **9,3 giờ** ở 1.272 tok
(gọn một phiên) vs **15,2 giờ** ở 2.475 tok (cắt hai phiên).

⚠️ Tệp thô không mất: `score_run.py` ghi + xả đệm từng bước, `do_4800k_raw.jsonl` giữ nguyên
~100 bước đã chấm nếu sau này muốn đọc lại.

Và 300 bước đó **đúng là 300 bước cổng A của UGround** (trùng 300/300) ⇒ so hai dụng cụ **ghép
cặp hoàn hảo**, miễn phí. Lượt này vừa chọn cỡ vừa là ô 4, không tốn thêm gì.

⚠️ **Nhân Kaggle restart là mất sạch `/kaggle/working`** — cả `harness/` đã vá lẫn tệp thô. Nguy
hiểm không phải ở lỗi `FileNotFoundError` (nó kêu ngay), mà ở chỗ **`harness` tự lùi về bản trên
dataset — bản CHƯA VÁ** ⇒ ba cỡ lại chạy y hệt nhau, im lặng. Ô dưới tự dựng lại thư mục `out`,
tự chép và vá `harness`, `assert` vá đúng lớp, rồi mới chạy; mất 30 bước cũ thì nó chấm đủ 300
(thêm ~13 phút cả ba).

```python
# ══ Ô 4 — cổng A 300 bước cho CẢ BA CỠ · tự dựng lại mọi thứ sau khi nhân restart ══
import os, sys, glob, shutil, ast, json, time, subprocess
WS = "/kaggle/working"
os.makedirs(f"{WS}/out", exist_ok=True)

# ── 1. bảo đảm harness có mặt VÀ đã vá (nhân restart là mất sạch) ───────────
SR = f"{WS}/harness/score_run.py"
if not os.path.exists(SR):
    mp = glob.glob("/kaggle/input/**/harness/score_run.py", recursive=True)
    assert mp, "DỪNG: không thấy harness trong dataset"
    shutil.copytree(os.path.dirname(mp[0]), f"{WS}/harness")
    print("đã chép lại harness từ dataset")

s = open(SR, encoding="utf-8").read()
cv = s.index("class UIVenus")
if "VENUS_MIN_PIXELS" not in s[cv:]:
    i = s.index("self.proc = AutoProcessor.from_pretrained(", cv)
    j = s.index("(", i); d = 0
    for k in range(j, len(s)):
        d += (s[k] == "(") - (s[k] == ")")
        if d == 0:
            j = k + 1; break
    open(SR, "w", encoding="utf-8").write(s[:i] + '''mn = int(os.environ.get("VENUS_MIN_PIXELS", 2000000))
        mx = int(os.environ.get("VENUS_MAX_PIXELS", 4800000))
        self.proc = AutoProcessor.from_pretrained(path, min_pixels=mn, max_pixels=mx)
        ip = self.proc.image_processor
        if isinstance(getattr(ip, "size", None), dict):
            ip.size = {"shortest_edge": mn, "longest_edge": mx}
        ip.min_pixels, ip.max_pixels = mn, mx
        print(f"[UIVenus] xin min={mn} max={mx} -> giu min={getattr(ip,'min_pixels',None)} "
              f"max={getattr(ip,'max_pixels',None)} size={getattr(ip,'size',None)}", flush=True)''' + s[j:])
    print("đã vá UIVenus")
t = open(SR, encoding="utf-8").read(); ast.parse(t)
cv = t.index("class UIVenus")
assert "VENUS_MIN_PIXELS" in t[cv:], "⛔ vá không nằm trong UIVenus"
assert "VENUS_MIN_PIXELS" not in t[:cv], "⛔ vá lọt sang lớp trước UIVenus"
print("harness sẵn sàng, vá đúng lớp ✅")

# ── 2. chạy ba cỡ, nhanh trước ─────────────────────────────────────────────
PX  = {1003: (200704, 1003520), 2007: (200704, 2007040), 4800: (2000000, 4800000)}
TEN = {1003: "1.272 tok (672×1484)", 2007: "2.475 tok (924×2100)",
       4800: "3.354 tok (1092×2408)"}
GY  = {1003: 4.0, 2007: 7.2, 4800: 8.3}   # đo thật ở lượt 300 bước
# ⛔ 4800 đã BỊ LOẠI (CUDA OOM trên T4×2, xem mục trên) — không chạy lại cho phí 37 phút
for k in (1003, 2007):
    raw = f"{WS}/out/do_{k}k_raw.jsonl"
    da = sum(1 for _ in open(raw, encoding="utf-8")) if os.path.exists(raw) else 0
    print(f"\n===== {TEN[k]} → 300 bước (đã có {da}, còn {300-da}, "
          f"~{(300-da)*GY[k]/60:.0f} phút) =====", flush=True)
    if da >= 300:
        print("  xong từ trước, bỏ qua"); continue
    mn, mx = PX[k]
    env = {**os.environ, "VENUS_MIN_PIXELS": str(mn), "VENUS_MAX_PIXELS": str(mx)}
    LOG = f"{WS}/out/do_{k}k_300.log"
    t0 = time.time(); f = open(LOG, "w")
    p = subprocess.Popen([sys.executable, "-u", SR, "--mode", "gate", "--grounder", "uivenus",
                          "--n", "300", "--out", f"{WS}/out/do_{k}k.json"],
                         stdout=f, stderr=subprocess.STDOUT, cwd=WS, env=env)
    _sl = globals().get("sao_luu", lambda *a, **kw: None)   # ô S chưa chạy thì bỏ qua
    while p.poll() is None:
        time.sleep(120)
        print(f"[{time.strftime('%H:%M:%S')}] {TEN[k]} · {(time.time()-t0)/60:.0f} phút",
              flush=True)
        _sl(f"o4 {TEN[k]}")
    f.close()
    _sl(f"o4 xong {TEN[k]}", ep=True)
    lg = open(LOG, encoding="utf-8", errors="ignore").read()
    bang = next((l for l in lg.splitlines() if "[UIVenus]" in l), "⛔ THIẾU dòng [UIVenus]")
    if p.returncode != 0:
        print(f"  ⛔ mã thoát {p.returncode}\n{lg[-1500:]}"); continue
    j = json.load(open(f"{WS}/out/do_{k}k.json"))
    print(f"  {bang}")
    print(f"  xong {(time.time()-t0)/60:.0f} phút · trung vị {j['median_err']:.2%}"
          f" · p75 {j['p75_err']:.2%}", flush=True)
print("\n⇒ xong ô 4. Chạy Ô 2D (copy lại từ runbook, bản mới) để chọn cỡ theo TRẦN.")
```

Rồi **chạy lại ô 2d** — giờ nó đọc ba tệp thô 300 bước và cho trần Voronoi kèm KTC dùng được.

⛔ **Luật chọn, giữ nguyên tinh thần cũ:** chọn theo **trần trên câu chuẩn của người**, thứ
giống hệt ở mọi nhánh nên không thể thiên vị S1 hay S2. Nếu ba trần **chồng KTC lên nhau** thì
trần không phân biệt được ⇒ chọn **cỡ nhanh nhất**, và khai rõ trong bài rằng cỡ ảnh chọn theo
tốc độ vì trần không phân biệt được ở n=300.

⭐ Trần của cỡ thắng chính là **mức nén thang đo** cần cho mục *Bẫy pha loãng*: so với **75,7%**
của UGround trên toàn tập, hoặc **70,0%** trên đúng 300 bước này.

## Ô 5 — chấm Base, S1, S2 trên lát đã chọn

Thứ tự **Base → S1 → S2** cố ý: mất phiên giữa chừng thì thứ còn lại vẫn đủ để đọc một phép so
trọn vẹn, và `score_run.py` nối tiếp được từ tệp thô ở lượt sau.

⚠️ **Đặt `VENUS_*_PIXELS` đúng cỡ đã chốt ở ô 2d.** Đổi cỡ giữa các nhánh là ba nhánh đo bằng
ba dụng cụ khác nhau — hỏng cả lượt mà không có gì báo.

⛔ **Bốn thứ ô này tự canh, vì mỗi thứ đều đã từng làm hỏng một lượt dài:**
· `harness` phải **đã vá** (nhân restart là nó lùi về bản dataset chưa vá, im lặng);
· phải có **cả ba** tệp preds — bản runbook trước quên `base` nên rớt `IndexError` sau vài giờ;
· **không dùng biến `P` của ô 1** — restart nhân là `NameError`, ô này tự tìm lại tệp;
· trần giờ tính trên **TỔNG cả ba nhánh**, không phải từng nhánh: Kaggle cắt phiên ở 12 giờ
  cho cả notebook, trần-mỗi-nhánh 11 giờ không chặn được gì.

```python
# ══ Ô 5 — chấm Base · S1 · S2. Tự canh 4 thứ, không phụ thuộc ô nào chạy trước ══
import os, sys, glob, ast, json, time, shutil, subprocess
WS = "/kaggle/working"

LAT    = 2532                  # ← lát đã chọn (2532 = đủ; 8,4 giờ ở cỡ 1.272 tok)
MN, MX = 200704, 1003520       # ← cỡ ảnh ô 2d in ra. PHẢI khớp cỡ đã chạy cổng A
TRAN_GIO_TONG = 11.0           # trần cho CẢ notebook, Kaggle cắt phiên ở 12 giờ
NHIP   = 120                   # giây giữa hai dòng nhật ký

# ⛔ Mốc phải tính trên ĐÚNG LÁT đang chấm, không phải toàn tập. Lát 2.532 chỉ gồm bước
#    S1≠S2 — khó hơn hẳn: UGround ở đó chỉ 42,5/52,8/49,5 chứ không phải 47,6/59,1/57,2.
#    So với số toàn tập là tự doạ mình (đã suýt đọc "base 23% vs 47,6% ⇒ hỏng").
MOC_LAT = {2532: {"base": 42.5, "s1": 52.8, "s2": 49.5},
           4463: {"base": 47.6, "s1": 59.1, "s2": 57.2}}   # toàn tập, để tham chiếu
MOC = MOC_LAT.get(LAT, MOC_LAT[4463])

# ── 1. harness có mặt và ĐÃ VÁ chưa (ô 5 chạy mã cũ = im lặng suốt 8 tiếng) ──
SR = f"{WS}/harness/score_run.py"
assert os.path.exists(SR), "DỪNG: chưa có harness — chạy ô 1 trước"
t = open(SR, encoding="utf-8").read(); ast.parse(t)
cv = t.index("class UIVenus")
assert "VENUS_MIN_PIXELS" in t[cv:], "⛔ harness CHƯA VÁ — chạy lại ô 1 (nguồn Drive)"
assert "VENUS_MIN_PIXELS" not in t[:cv], "⛔ vá lọt sang lớp trước UIVenus"

# ── 2. tìm đủ BA tệp preds, thiếu là dừng NGAY (không phải sau vài giờ) ──────
SRC = {}
for nhanh in ("base", "s1", "s2"):
    c = (glob.glob(f"{WS}/bundle/preds/preds_venus_{nhanh}_{LAT}.jsonl") or
         glob.glob(f"/kaggle/input/**/preds_venus_{nhanh}_{LAT}.jsonl", recursive=True))
    if c: SRC[nhanh] = c[0]
assert len(SRC) == 3, (f"DỪNG: thiếu preds lát {LAT} — có {sorted(SRC)}. Nhánh BASE là "
                       "chứng nhân chống bẫy pha loãng, thiếu nó là lượt chạy vô nghĩa.")

_sl = globals().get("sao_luu", lambda *a, **kw: None)      # ô S chưa chạy thì bỏ qua
def _vram():
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total",
                            "--format=csv,noheader,nounits"], capture_output=True, text=True)
        return " · ".join(f"{l.split(', ')[0]}/{l.split(', ')[1]}MB"
                          for l in r.stdout.strip().splitlines())
    except Exception:
        return "?"
def _doc(raw):
    """Đọc tệp thô đang ghi dở → (n, exec%, hit_disk%, action_ok%, số bước bộ trỏ trượt khuôn)."""
    n = ex = hd = ao = hong = 0
    if os.path.exists(raw):
        for l in open(raw, encoding="utf-8"):
            try: o = json.loads(l)
            except Exception: continue      # dòng ghi dở lúc đang xả đệm
            n += 1
            if o.get("pred_xy") is None: hong += 1
            ex += o.get("executable", 0); hd += o.get("hit_disk", 0)
            ao += o.get("action_ok", 0)
    q = lambda v: 100.0 * v / n if n else 0.0
    return n, q(ex), q(hd), q(ao), hong

print("═" * 78)
print(f"Ô 5 · lát {LAT} · cỡ ảnh min={MN} max={MX} · trần giờ tổng {TRAN_GIO_TONG}h")
print(f"  harness đã vá ✅ · preds đủ 3 nhánh ✅ · sao lưu "
      + ("BẬT ✅" if "sao_luu" in globals() else "TẮT ⚠️ (chạy ô S nếu muốn an toàn)"))
for n_, p_ in SRC.items():
    print(f"  {n_:5s} {sum(1 for _ in open(p_)):>5} bước  ←  {os.path.basename(p_)}")
print(f"  ước tính ~{LAT*3*4.0/3600:.1f}h cả ba nhánh ở 4,0 s/bước")
print(f"  mốc UGround TRÊN ĐÚNG LÁT {LAT}: base {MOC['base']} · s1 {MOC['s1']} · s2 {MOC['s2']}"
      + ("   (toàn tập 4.463 là 47,6/59,1/57,2 — KHÁC, đừng so nhầm)" if LAT != 4463 else ""))
print("⛔ Số exec in ra dưới đây CHỈ để theo dõi. Luật đọc đã khoá trước: cấm dừng sớm,")
print("   cấm đổi lát hay đổi cỡ ảnh vì thấy số đẹp/xấu.")
print("═" * 78, flush=True)

env = {**os.environ, "VENUS_MIN_PIXELS": str(MN), "VENUS_MAX_PIXELS": str(MX)}
T0_TONG = time.time()
for nhanh in ("base", "s1", "s2"):
    ten = f"venus_{nhanh}_{LAT}"
    out = f"{WS}/out/score_{ten}.json"
    raw = f"{WS}/out/score_{ten}_raw.jsonl"
    LOG = f"{WS}/out/{ten}.log"
    da = _doc(raw)[0]
    tong_gio = (time.time() - T0_TONG) / 3600
    print(f"\n{'━'*78}\n▶ {ten} · đã có {da}/{LAT} · còn {LAT-da} · "
          f"tổng đã dùng {tong_gio:.2f}h", flush=True)
    if da >= LAT:
        n, ex, hd, ao, hong = _doc(raw)
        print(f"  ✅ xong từ trước · exec {ex:.1f}% · hit_disk {hd:.1f}% · action_ok {ao:.1f}%")
        continue
    if tong_gio > TRAN_GIO_TONG:
        print(f"  ⏹️  đã dùng {tong_gio:.1f}h — DỪNG để phiên kết thúc sạch. "
              "Chạy lại ô này ở phiên sau, nó nối tiếp từ tệp thô."); break

    t0 = time.time(); n_dau = da; f = open(LOG, "w")
    p = subprocess.Popen([sys.executable, "-u", SR, "--mode", "score",
                          "--grounder", "uivenus", "--preds", SRC[nhanh],
                          "--n", str(LAT), "--out", out],
                         stdout=f, stderr=subprocess.STDOUT, cwd=WS, env=env)
    n_truoc, t_dung_yen = da, time.time()
    while p.poll() is None:
        time.sleep(NHIP)
        n, ex, hd, ao, hong = _doc(raw)
        dt = time.time() - t0
        sp = (n - n_dau) / max(dt, 1)                      # bước/giây của LƯỢT NÀY
        con = (LAT - n) / sp / 3600 if sp > 0 else float("inf")
        tong_gio = (time.time() - T0_TONG) / 3600
        con_lai_nhanh = ["base", "s1", "s2"].index(nhanh)
        du_bao = tong_gio + con + (2 - con_lai_nhanh) * (LAT / sp / 3600 if sp > 0 else 0)
        dia = shutil.disk_usage(WS).free / 2**30
        print(f"[{time.strftime('%H:%M:%S')}] {ten} · {n}/{LAT} ({n/LAT:5.1%}) · "
              f"{1/sp if sp>0 else 0:4.1f} s/bước · nhánh {dt/3600:.2f}h · tổng {tong_gio:.2f}h",
              flush=True)
        print(f"            exec {ex:5.1f}% (mốc UGround {MOC[nhanh]}) · hit_disk {hd:5.1f}% · "
              f"action_ok {ao:5.1f}% · trượt khuôn {hong}", flush=True)
        print(f"            còn ~{con:.1f}h nhánh · dự báo cả ba xong ở {du_bao:.1f}h · "
              f"VRAM {_vram()} · đĩa còn {dia:.1f}GB", flush=True)
        # ⚠️ tiền lệ: lượt Kaggle treo 7 giờ vì log ngập, tiến trình sống mà không nhích
        if n == n_truoc:
            ket = (time.time() - t_dung_yen) / 60
            print(f"            ⚠️ KHÔNG NHÍCH {ket:.0f} phút — nếu quá 6 phút thì tiến trình "
                  f"có thể đã treo. Dòng cuối log con: "
                  + (open(LOG, encoding='utf-8', errors='ignore').read().strip()
                     .splitlines() or ["(rỗng)"])[-1][:90], flush=True)
        else:
            n_truoc, t_dung_yen = n, time.time()
        _sl(f"{ten} {n}/{LAT}")
        if tong_gio > TRAN_GIO_TONG:
            print("⚠️ QUÁ TRẦN GIỜ TỔNG — giết tiến trình để notebook kết thúc SẠCH, "
                  "nhờ vậy tệp thô dở vẫn lưu được", flush=True)
            p.terminate(); break
    f.close()
    lg = open(LOG, encoding="utf-8", errors="ignore").read()
    # dòng này CHỨNG MINH tiến trình chạy đúng cỡ ảnh — đừng tin mã nguồn, tin log
    print("  " + next((l for l in lg.splitlines() if "[UIVenus]" in l),
                      "⛔ THIẾU dòng [UIVenus] — nhánh này có thể chạy sai cấu hình!"))
    n, ex, hd, ao, hong = _doc(raw)
    print(f"  {ten}: mã thoát {p.returncode} · {(time.time()-t0)/3600:.2f}h · {n}/{LAT} bước")
    print(f"     exec {ex:.2f}%  (UGround trên lát này: {MOC[nhanh]}%) · hit_disk {hd:.2f}% · "
          f"action_ok {ao:.2f}% · bộ trỏ trượt khuôn {hong} bước")
    if hong > 0.05 * max(n, 1):
        print("     ⛔ trượt khuôn >5% — bộ trỏ trả về khuôn lạ, xem lại UIVenus.point")
    _sl(f"xong {ten}", ep=True)      # nhánh xong = mốc đáng giá nhất, ép đẩy ngay

print(f"\n{'═'*78}\n⇒ xong ô 5 sau {(time.time()-T0_TONG)/3600:.2f}h. Sang ô 6 để gom tệp.")
for nhanh in ("base", "s1", "s2"):
    n, ex, hd, ao, hong = _doc(f"{WS}/out/score_venus_{nhanh}_{LAT}_raw.jsonl")
    print(f"  {nhanh:5s} {n:>5}/{LAT} · exec {ex:6.2f}% · UGround(lát) {MOC[nhanh]:>5}%")
print("⛔ Đừng đọc hiệu S2−S1 ở đây — phải ghép cặp từng bước bằng phan_tich_venus.py,")
print("   và phải có S1−Base làm chứng nhân chống bẫy pha loãng.")
```


**Mốc đối chiếu, đo bằng UGround trên ĐÚNG các lát này** (tính sẵn, offline):

| lát | S1 − Base (UGround) | S2 − S1 (UGround, quy về 4.463) |
|---|---|---|
| 2.532 | **+10,35** pp [+8,39 · +12,40] | −1,93 pp [−3,06 · −0,75] |
| 1.266 | **+11,69** pp [+9,00 · +14,41] | *(bootstrap lại khi có số)* |
| 633 | **+11,06** pp [+7,50 · +14,73] | *(nt)* |

## Ô 6 — gom tệp mang về

⛔ **Phải đổi tên tệp cổng A của cỡ đã chốt thành `venus_gate_raw.jsonl`.** `phan_tich_venus.py`
mở đúng tên đó (dòng 38); ô 4 lại sinh tên `do_1003k_raw.jsonl`. Không đổi thì script ở máy in
`⏳ chưa có runs/venus/venus_gate_raw.jsonl` rồi **bỏ qua toàn bộ phần so hai dụng cụ** — không
lỗi, không cảnh báo, chỉ thiếu mất nửa kết quả.

```python
import shutil, glob, os
CO_DA_CHON = 1003            # ← 1003 hay 2007, theo ô 2d
os.makedirs("/kaggle/working/results", exist_ok=True)
for p in glob.glob("/kaggle/working/out/*"):
    if os.path.isfile(p):
        shutil.copy(p, "/kaggle/working/results/")

src = f"/kaggle/working/out/do_{CO_DA_CHON}k_raw.jsonl"
assert os.path.exists(src), f"DỪNG: không thấy {src} — chọn lại CO_DA_CHON"
shutil.copy(src, "/kaggle/working/results/venus_gate_raw.jsonl")
print("cổng A của cỡ đã chọn →  venus_gate_raw.jsonl "
      f"({sum(1 for _ in open(src, encoding='utf-8'))} bước)")

shutil.make_archive("/kaggle/working/venus_results", "zip", "/kaggle/working/results")
print(sorted(os.listdir("/kaggle/working/results")))
print(os.path.getsize("/kaggle/working/venus_results.zip")/2**20, "MB")

# ⭐ TẢI VỀ: dòng dưới in ra một liên kết bấm được ngay trong notebook. Panel Output bên phải
#    cũng có (Data → Output → /kaggle/working), nhưng nó chỉ làm mới sau vài giây nên hay
#    "không thấy tệp" dù tệp đã có.
from IPython.display import FileLink
display(FileLink("venus_results.zip"))     # cwd của notebook là /kaggle/working
```

⭐ **Bắt buộc mang về cả `*_raw.jsonl`.** Có tệp thô thì mọi phép đọc lại — đổi luật chấm, đổi
lát, ghép cặp với UGround — làm được **offline, 0 giây GPU**. Đã cứu trọn một lượt 5,6 giờ khi
chấm lại `p3_nopos_v2`.

**Giải nén vào đâu:** bung hết vào `runs/venus/` (luật đọc kết quả ở `runs/README.md`: tải về
đặt thẳng vào thư mục của phép đo đó). `phan_tich_venus.py` tìm ở đúng đó:

| tệp | script mở nó ở dòng |
|---|---|
| `runs/venus/venus_gate_raw.jsonl` | 38 — so cổng A hai dụng cụ |
| `runs/venus/score_venus_{base,s1,s2}_{LAT}_raw.jsonl` | 82 — Δ dưới UI-Venus |

Ba tệp đối chiếu bên UGround đã có sẵn tại máy (`runs/score_{s1,s2}_seed101_raw.jsonl`,
`runs/score_base_raw.jsonl`, `runs/gate_a/gate_A_raw.jsonl`) — đã kiểm 20/8, đủ cả bốn.

---

## Sau khi có tệp: đọc offline tại máy

```
python3 harness/phan_tich_venus.py
```

So **ghép cặp từng bước** giữa hai bộ trỏ trên đúng những bước cả hai đã chấm, trả về:
sai số trung vị hai dụng cụ (cổng A, 300 bước ghép cặp) · Δ(S2−S1) theo UI-Venus kèm KTC
bootstrap gom cụm · và bảng bốn ô ở đầu file này.
