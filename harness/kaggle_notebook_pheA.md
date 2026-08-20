# Notebook Kaggle — PHÉP A (diễn đạt lại), bản để COMMIT chạy nền

**Trước khi commit, bật đủ ba thứ trong panel bên phải:**

| | Đặt |
|---|---|
| Accelerator | **GPU T4 ×2** |
| Internet | **On** — bắt buộc, vì phải tải UGround (~4 GB) và `all_forest_dict.zip` (452 MB) từ HuggingFace |
| Datasets | `thesis-preds` (có `kaggle_16_8`) **và** `thesis-score` (có ảnh + `test.jsonl`) |

Thiếu Internet thì ô 2 chết ở dòng nạp mô hình, sau khi đã ngốn thời gian khởi động.
Thiếu `thesis-score` thì ô 1 dừng ngay — đó là ý của nó.

Tổng thời gian ~4 giờ. Giới hạn một lần commit là 12 giờ nên thoải mái.

---

## Ô 1 — nối dữ liệu và kiểm (30 giây)

```python
import os, glob, json, shutil, random

WS  = "/kaggle/working"
PKG = "/kaggle/input/datasets/uyenle0712/thesis-preds/kaggle_16_8"

best = None
for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True):
    root  = os.path.dirname(t)
    rows  = sum(1 for _ in open(t, encoding="utf-8"))
    n_img = len(glob.glob(os.path.join(root, "images", "*.png")))
    print(f"  {rows:5d} dòng · {n_img:5d} ảnh  {root}")
    if rows >= 6900 and n_img >= 4400 and (best is None or n_img > best[2]):
        best = (t, rows, n_img, root)
assert best, "DỪNG: không gói nào có đủ test.jsonl 6.958 dòng lẫn 4.463 ảnh"
TEST_JSONL, _, _, ROOT = best

shutil.copytree(f"{PKG}/harness", f"{WS}/harness", dirs_exist_ok=True)
dst = f"{WS}/harness/dg1_cache/test_ac"
os.makedirs(dst, exist_ok=True)
for src, name in [(TEST_JSONL, "test.jsonl"), (os.path.join(ROOT, "images"), "images")]:
    link = os.path.join(dst, name)
    if os.path.islink(link): os.remove(link)
    elif os.path.isdir(link): shutil.rmtree(link)
    elif os.path.exists(link): os.remove(link)
    os.symlink(src, link)

recs = [json.loads(l) for l in open(f"{dst}/test.jsonl", encoding="utf-8")]
taps = [r for r in recs if r["action"].get("action_type") in ("click", "long_press")
        and "x" in r["action"]]
miss = sum(1 for r in taps if not os.path.exists(os.path.join(dst, r["image"])))
keys = [(r["episode_id"], r["step_id"]) for r in taps]
random.Random(20260805).shuffle(keys)

print(f"\nbước chạm: {len(taps)} | thiếu ảnh: {miss} | nhãn app: "
      f"{'app_seen_in_train' in recs[0]}")
print("lát 800 bắt đầu:", keys[:3])
assert len(taps) == 4463 and miss == 0, "DỪNG: dữ liệu không khớp bản đã chấm ba nhánh"
assert keys[:3] == [(19277, 8), (18972, 1), (18540, 1)], "DỪNG: lát khác máy nhà"
print("✔ SẴN SÀNG")
```

Ba dòng `assert` là chỗ đáng giá nhất của ô này: chúng chặn đúng kiểu hỏng đã suýt xảy
ra — nối nhầm `test.jsonl` 300 dòng của cổng A, rồi chấm 4 giờ trên một lát không so
được với mốc nào.

## Ô 2 — chạy bốn biến thể (~4 giờ)

```python
import subprocess, time, json

DATA = "/kaggle/input/datasets/uyenle0712/thesis-preds/kaggle_16_8"
CEIL = 74.9        # trần trên đúng lát 800 này, đo ở máy nhà bằng câu chuẩn nguyên bản
out  = {}

for i, v in enumerate(["p1_verb", "p2_order", "p3_nopos", "p4_both"]):
    t0 = time.time()
    subprocess.run([
        "python", f"{WS}/harness/score_run.py", "--mode", "score",
        "--grounder", "uground",
        "--preds", f"{DATA}/preds_para_{v}.jsonl",
        "--out",   f"{WS}/score_para_{v}.json",
        "--n", "800"], check=True)
    r = json.load(open(f"{WS}/score_para_{v}.json"))
    out[v] = r["exec_voronoi"] * 100
    print(f"{v:9s} {out[v]:5.1f}%  (trần {CEIL}%, lệch {out[v]-CEIL:+.1f})  "
          f"{(time.time()-t0)/60:.0f} phút", flush=True)

    # dừng sớm nếu biến thể đầu ra con số không thể tin được: dưới 50% là lớn hơn
    # mọi thứ đã đo, nhiều khả năng hỏng đường ống chứ không phải tính chất bộ trỏ
    if i == 0 and out[v] < 50:
        raise SystemExit(f"DỪNG: p1_verb ra {out[v]:.1f}%, nghi lỗi đường ống. "
                         f"Không đốt thêm 3 giờ.")
```

`p1_verb` chạy trước có chủ ý: nó là biến thể mạnh nhất, đổi được **91,5%** số bước, ba
cái sau chỉ ~25% vì phụ thuộc câu có mệnh đề vị trí. Nếu cái này không suy chuyển thì ba
cái kia gần như chắc chắn cũng vậy.

## Ô 3 — bảng kết quả

```python
print(f"{'biến thể':10s} {'điểm':>7s} {'lệch trần':>10s}")
print(f"{'(trần)':10s} {CEIL:6.1f}%")
for v, s in out.items():
    print(f"{v:10s} {s:6.1f}% {s-CEIL:+9.1f}")

import glob
print("\nTệp mang về (panel Output):")
for f in sorted(glob.glob(f"{WS}/score_para_*")): print(" ", f)
```

Giữ **cả** `.json` lẫn `_raw.jsonl`: tệp thô cho phép đổi luật chấm rồi tính lại mà không
phải gọi bộ trỏ, đúng như ba nhánh đã chấm trước.

---

## Đọc kết quả

Mốc: **74,9%** — trần trên đúng lát 800 này, bằng câu chuẩn chưa viết lại.

| Bốn biến thể | Nghĩa là | Bài sẽ viết gì |
|---|---|---|
| đều ≈ 73–76% | bộ trỏ bền trước cách diễn đạt trong kho này | bỏ câu tự khai *"we cannot answer it"*, thay bằng số đo — kèm điều kiện chỉ đúng cho bộ trỏ này và kiểu viết lại này |
| `p1_verb` tụt mạnh | nhạy với **cách nói** → đòn Jandial et al. đứng vững | khai thẳng, và mọi số tuyệt đối yếu đi theo |
| chỉ `p3_nopos` tụt | cần **thông tin vị trí**, không phải chuyện diễn đạt | kết quả nhẹ hơn hẳn, và tách được hai nguyên nhân mà không ai tách trước đó |

Xong phép A thì phiên sau chạy phép B (UI-Venus, ~6 giờ) — đổi `--grounder uivenus`, ba
nhánh, `--n 500`, mốc so đã tính sẵn: 73,4 / 58,8 / 47,6, chênh +11,2 pp.
