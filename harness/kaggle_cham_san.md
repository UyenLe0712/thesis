# Chấm SÀN — ba nhánh, ~3 giờ, 0 đồng

Đây là phép đo **quyết định nhan đề bài** và **quyết định mọi con số tuyệt đối có diễn giải
được không**. Luật đọc đã khoá trước trong `harness/make_floor.py` — **đọc nó trước khi xem
kết quả**, đừng đọc sau.

| nhánh | câu thành gì | trả lời câu hỏi |
|---|---|---|
| `f1_trong` | `"Tap the button."` cho **mọi** bước | bộ trỏ trúng bao nhiêu khi câu **không mang tin gì** |
| `f3_lechman` | **câu chuẩn của một bước khác** — thật, đúng văn phong, sai màn | f1 có phải sàn công bằng, hay chỉ là hiệu ứng "câu kỳ quặc" |
| `f2_khongten` | giữ vị trí, **bỏ tên phần tử** | thước đo **gọi tên** hay **chỉ chỗ** |

**Vì sao có `f3`:** `"Tap the button."` lặp 800 lần là đầu vào **lạc phân bố**. Bộ trỏ có thể
hành xử bất thường vì *lạ* chứ không vì *vô nghĩa*, và ai cũng sẽ vặn đúng chỗ đó. `f3` bình
thường về mọi mặt trừ nội dung — đã kiểm: trung vị **34 ký tự** so với câu chuẩn **35**, **0**
bước lấy nhầm câu của chính nó, **0** bước lấy câu cùng tác vụ.

---

## Bước 1 — upload ba tệp

Vào dataset **`thesis-preds`** → **New Version**, kéo cả ba vào, **giữ nguyên tệp cũ**:

```
runs/floor/preds_f1_trong.jsonl
runs/floor/preds_f2_khongten.jsonl
runs/floor/preds_f3_lechman.jsonl
```

Tổng ~1,2 MB. Xong thì panel Input trong notebook bấm cập nhật lên version mới.

---

## Bước 2 — ô 0: kiểm GPU

```python
import torch
print("GPU:", torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else "—")
assert torch.cuda.is_available(), "DỪNG: đang chạy CPU. Bật Accelerator = GPU T4 ×2."
```

## Bước 3 — ô 1: nối dữ liệu + kiểm tiền bay

```python
import os, glob, json, shutil, random
WS = "/kaggle/working"

cand = glob.glob("/kaggle/input/**/preds_f1_trong.jsonl", recursive=True)
assert cand, "DỪNG: chưa thấy preds_f1_trong.jsonl — đã cập nhật dataset version chưa?"
FLOOR = os.path.dirname(cand[0]); print("nhánh sàn:", FLOOR)

mp = glob.glob("/kaggle/input/**/harness/score_run.py", recursive=True)
assert mp, "DỪNG: không thấy harness/score_run.py"
PKG = os.path.dirname(os.path.dirname(mp[0]))

best = None
for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True):
    root = os.path.dirname(t)
    rows = sum(1 for _ in open(t, encoding="utf-8"))
    nimg = len(glob.glob(os.path.join(root, "images", "*.png")))
    if rows >= 6900 and nimg >= 4400 and (best is None or nimg > best[2]):
        best = (t, rows, nimg, root)
assert best, "DỪNG: không gói nào đủ test.jsonl 6.958 dòng lẫn 4.463 ảnh"
TEST_JSONL, _, _, ROOT = best

shutil.copytree(f"{PKG}/harness", f"{WS}/harness", dirs_exist_ok=True)
dst = f"{WS}/harness/dg1_cache/test_ac"; os.makedirs(dst, exist_ok=True)
for src, name in [(TEST_JSONL, "test.jsonl"), (os.path.join(ROOT, "images"), "images")]:
    link = os.path.join(dst, name)
    if os.path.islink(link): os.remove(link)
    elif os.path.isdir(link): shutil.rmtree(link)
    elif os.path.exists(link): os.remove(link)
    os.symlink(src, link)

recs = [json.loads(l) for l in open(f"{dst}/test.jsonl", encoding="utf-8")]
taps = [r for r in recs if r["action"].get("action_type") in ("click","long_press") and "x" in r["action"]]
assert len(taps) == 4463, f"DỪNG: {len(taps)} bước chạm"
keys = [(r["episode_id"], r["step_id"]) for r in taps]
random.Random(20260805).shuffle(keys)
assert keys[:3] == [(19277, 8), (18972, 1), (18540, 1)], "DỪNG: lát khác máy nhà"

# kiểm ba tệp sàn ngay trên Kaggle
G = {(r["episode_id"], r["step_id"]): r["gold_instruction"].strip() for r in taps}
for v, cho in [("f1_trong", 800), ("f2_khongten", 193), ("f3_lechman", 800)]:
    P = {}
    for l in open(f"{FLOOR}/preds_{v}.jsonl", encoding="utf-8"):
        o = json.loads(l); P[(o["episode_id"], o["step_id"])] = o["pred"]
    assert len(P) == 4463, f"DỪNG: {v} có {len(P)} bản ghi"
    doi = sum(1 for k in keys[:800] if P[k] != G[k])
    assert doi == cho, f"DỪNG: {v} đổi {doi} bước trên lát 800, cần {cho}"
    print(f"  {v:12s} ✔ {doi}/800 bước đổi")
print("✔ SẴN SÀNG")
```

Dòng `assert doi == cho` là chỗ đáng giá nhất: nó kiểm **đúng lát 800 sẽ chấm**, nên bắt được
cả trường hợp upload nhầm bản cũ.

## Bước 4 — ô 2: chấm ba nhánh (~3 giờ)

```python
import os, subprocess, time, json
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["PYTHONUNBUFFERED"] = "1"
RAC = ("it/s", "s/it", "it]")

def chay(v, nhip=15):
    log = f"{WS}/log_{v}.txt"
    with open(log, "w") as fw:
        p = subprocess.Popen(
            ["python", "-u", f"{WS}/harness/score_run.py", "--mode", "score",
             "--grounder", "uground", "--preds", f"{FLOOR}/preds_{v}.jsonl",
             "--out", f"{WS}/score_{v}.json", "--n", "800"],
            stdout=fw, stderr=subprocess.STDOUT)
        t0 = tlast = time.time(); dem, du = 0, ""
        with open(log) as fr:
            while True:
                *dong, du = (du + fr.read()).split("\n")
                for l in dong:
                    if any(k in l for k in RAC): continue
                    dem += 1
                    if dem <= 3000 or "bước/giây" in l:
                        print(l, flush=True); tlast = time.time()
                if p.poll() is not None: break
                if time.time() - tlast > 120:
                    print(f"  [{time.strftime('%H:%M:%S')}] {v} · {(time.time()-t0)/60:.0f} phút · vẫn đang chạy", flush=True)
                    tlast = time.time()
                time.sleep(nhip)
    print(f"── {v} xong · {(time.time()-t0)/60:.0f} phút", flush=True)

for v in ["f1_trong", "f3_lechman", "f2_khongten"]:
    chay(v)
    r = json.load(open(f"{WS}/score_{v}.json"))
    print(f"★ {v}: {r['exec_voronoi']*100:.1f}%   (trần lát này 74,9%)", flush=True)
```

**Thứ tự có chủ ý:** `f1` và `f3` là một cặp — f1 vô nghĩa, f3 là đối chứng cho nó. Chạy rời
nhau thì f1 đứng một mình và bị vặn ngay. `f2` tự đứng được nên để cuối.

---

## Bước 5 — đọc theo luật đã khoá TRƯỚC

Tải ba `score_f*.json` và ba `score_f*_raw.jsonl` về `runs/floor/`, rồi:

```bash
python3 harness/doc_san.py
```

Mốc so trên đúng lát 800 này: **trần 74,9% · S1 58,8% · Base ~47%**.

| thấy gì | nghĩa là |
|---|---|
| `f1` gần 0 | thước đòi câu phải mang thông tin — dải 0→75,7 dùng được nguyên |
| **`f1` > 30%** | ⚠ phần lớn điểm là bộ trỏ tự đoán. **Mọi con số đọc trên nền SÀN, không phải 0**, và mọi câu *"lấp N% dư địa"* phải tính lại |
| `f3` ≈ `f1` | ✔ f1 là sàn công bằng, không phải hiệu ứng "câu kỳ quặc" |
| `f3` **cao hơn** `f1` nhiều | ⚠ bộ trỏ thưởng cho câu **đúng văn phong bất kể nội dung** ⇒ nhiễm văn phong có thật và **đo được** |
| `f3` thấp hơn `f1` | bộ trỏ bị câu sai dẫn đi lạc — sàn thật còn thấp hơn f1 |
| **`f2` ≈ trần** | ⛔ thước đo **CHỈ CHỖ**, không đo **GỌI TÊN** ⇒ **"Element Identification" ở nhan đề SAI**, đổi thành *localisation* / *target resolution* |
| `f2` tụt mạnh | ✔ gọi tên là phần đóng góp chính — đúng thứ bài tuyên bố đo |

⚠️ **Một dự phòng phải ghi trước:** `f2` chỉ đụng **193 bước** trên lát này. Nếu nó tụt
**< 6 pp** thì n=193 **không phân biệt được "tụt nhỏ" với "không tụt"** — lúc đó phải chấm lại
`f2` trên đủ 4.463 bước (1.021 bước bị đụng, ~5,6 giờ) trước khi kết luận về nhan đề. Nếu nó
tụt **> 10 pp** thì 193 bước là đủ, không cần chạy thêm.

---

## Quota

Đã tiêu tuần này ~17,6 giờ trong 30. Ba nhánh này ~3 giờ ⇒ còn ~9 giờ, đủ cho phép chấm
`f2` toàn tập nếu rơi vào dự phòng trên.
