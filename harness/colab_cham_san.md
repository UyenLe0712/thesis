# Chấm SÀN trên COLAB — thay Kaggle khi hết quota

Ba nhánh `f1_trong` · `f3_lechman` · `f2_khongten`. Luật đọc đã khoá trước ở
`harness/make_floor.py`; nội dung và thứ tự chạy giữ nguyên như `harness/kaggle_cham_san.md`.

| | |
|---|---|
| máy | **L4** (đừng lấy A100 — khâu chấm là suy luận, không cần) |
| giá | **1,54 đơn vị/giờ**, đo 11/8 |
| thời gian | ~2–2,5 giờ cho cả ba nhánh |
| **tốn** | **~3–4 đơn vị ≈ $0,30–0,40** |

⚠️ **Đừng chọn A100** (5,3 đơn vị/giờ). Nó nhanh hơn nhưng khâu chấm nghẽn ở giải mã tuần tự,
không ở tính toán — trả gấp 3,4 lần tiền để không nhanh hơn bao nhiêu.

---

## Bước 1 — đưa lên Drive

Ba tệp dự đoán (~1,2 MB):

```
runs/floor/preds_f1_trong.jsonl
runs/floor/preds_f2_khongten.jsonl
runs/floor/preds_f3_lechman.jsonl
```

→ `MyDrive/thesis/floor/`

**Và kiểm gói mã trên Drive có phải bản mới không** — `thesis_rented.zip` đã từng là bản cũ
hai lần (13/8 và 12/8), cả hai lần đều lộ ra muộn. Nếu không chắc, đóng gói lại ở máy nhà:

```bash
python harness/make_bundle.py score      # ~1,7 GB: mã + test.jsonl đã gắn nhãn + 4.463 ảnh
```

Gói `score` đã kèm sẵn ảnh bước chạm nên **không cần ô A.5c**.

---

## Bước 2 — ô 0: gắn Drive, bung gói, kiểm máy

```python
from google.colab import drive; drive.mount('/content/drive')
import os, subprocess, torch
D  = "/content/drive/MyDrive/thesis"
WS = "/content/ws"; os.makedirs(WS, exist_ok=True)

print("card:", torch.cuda.get_device_name(0))
assert torch.cuda.is_available(), "DỪNG: không có GPU"

!pip -q install transformers accelerate qwen-vl-utils 2>/dev/null
!cd {WS} && unzip -oq {D}/thesis_score.zip

r = open(f"{WS}/harness/score_run.py", encoding="utf-8").read()
print("score_run.py:", len(r), "B  ·  có chữ ký lượt chạy:", '"run"' in r)
assert len(r) > 34000, "DỪNG: score_run.py là bản CŨ — đóng gói lại ở máy nhà"
```

Dòng `assert` cuối chặn đúng lỗi đã mắc hai lần: gói trên Drive là bản trước khi vá, chạy trơn
và ra số của luật chấm cũ.

## Bước 3 — ô 1: kiểm tiền bay trên đúng lát 800

```python
import json, glob, random, shutil
FLOOR = f"{D}/floor"
dst = f"{WS}/harness/dg1_cache/test_ac"
recs = [json.loads(l) for l in open(f"{dst}/test.jsonl", encoding="utf-8")]
taps = [r for r in recs if r["action"].get("action_type") in ("click","long_press") and "x" in r["action"]]
miss = sum(1 for r in taps if not os.path.exists(os.path.join(dst, r["image"])))
assert len(taps) == 4463 and miss == 0, f"DỪNG: {len(taps)} bước chạm, thiếu {miss} ảnh"
assert "app_seen_in_train" in recs[0], "DỪNG: test.jsonl chưa gắn nhãn app"

keys = [(r["episode_id"], r["step_id"]) for r in taps]
random.Random(20260805).shuffle(keys)
assert keys[:3] == [(19277, 8), (18972, 1), (18540, 1)], "DỪNG: lát khác máy nhà"

G = {(r["episode_id"], r["step_id"]): r["gold_instruction"].strip() for r in taps}
for v, cho in [("f1_trong", 800), ("f2_khongten", 193), ("f3_lechman", 800)]:
    P = {}
    for l in open(f"{FLOOR}/preds_{v}.jsonl", encoding="utf-8"):
        o = json.loads(l); P[(o["episode_id"], o["step_id"])] = o["pred"]
    assert len(P) == 4463, f"DỪNG: {v} có {len(P)} bản ghi"
    doi = sum(1 for k in keys[:800] if P[k] != G[k])
    assert doi == cho, f"DỪNG: {v} đổi {doi} bước trên lát 800, cần {cho}"
    print(f"  {v:12s} ✔ {doi}/800")
print("✔ SẴN SÀNG")
```

## Bước 4 — ô 2: chấm, ghi thẳng Drive

```python
import time
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["PYTHONUNBUFFERED"] = "1"
os.makedirs(f"{D}/floor_out", exist_ok=True)
RAC = ("it/s", "s/it", "it]")

def chay(v, nhip=15):
    log = f"{WS}/log_{v}.txt"
    with open(log, "w") as fw:
        p = subprocess.Popen(
            ["python", "-u", f"{WS}/harness/score_run.py", "--mode", "score",
             "--grounder", "uground", "--preds", f"{FLOOR}/preds_{v}.jsonl",
             "--out", f"{D}/floor_out/score_{v}.json", "--n", "800"],
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
                    print(f"  [{time.strftime('%H:%M:%S')}] {v} · {(time.time()-t0)/60:.0f} phút · vẫn chạy", flush=True)
                    tlast = time.time()
                time.sleep(nhip)
    print(f"── {v} xong · {(time.time()-t0)/60:.0f} phút", flush=True)

for v in ["f1_trong", "f3_lechman", "f2_khongten"]:
    chay(v)
    r = json.load(open(f"{D}/floor_out/score_{v}.json"))
    print(f"★ {v}: {r['exec_voronoi']*100:.1f}%   (trần lát này 74,9%)", flush=True)
```

⭐ **Khác Kaggle một chỗ quan trọng: `--out` trỏ THẲNG vào Drive.** Mất máy ảo giữa chừng thì
tệp thô đã ghi vẫn còn, và `score_run.py` **nối tiếp được** — chạy lại là nó chấm tiếp từ đúng
chỗ. Trên Kaggle không làm được thế, phải tải tay giữa chừng.

*(Bài học 10/8: mất máy ảo khi chưa có cơ chế cất Drive = 42 đơn vị + 8 giờ; sau khi có = 3 phút.)*

## Bước 5 — đọc kết quả

Tải sáu tệp từ `MyDrive/thesis/floor_out/` về `runs/floor/`, rồi:

```bash
python3 harness/doc_san.py
```

Luật đọc + dự phòng khi `f2` tụt dưới 6 pp: xem `harness/kaggle_cham_san.md` mục 5. Không lặp
lại ở đây để chỉ có **một** bản luật, tránh hai bản trôi khỏi nhau.

---

## Nếu muốn chờ Kaggle thay vì trả Colab

Quota Kaggle là **cửa sổ trượt 30 giờ/tuần**, trang Kaggle in rõ còn bao lâu tới lúc hồi. Hạn
nộp 31/8 nên còn 13 ngày — chờ vài ngày hoàn toàn nằm trong lịch. Chọn theo cái nào tiện hơn,
không phải theo tiền: chênh lệch ở đây là **$0,40**.
