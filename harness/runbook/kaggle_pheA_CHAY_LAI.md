# Phép A — chạy lại từ đầu, từng bước

Bản 17/8 treo 7 giờ ở `Loading weights: 29% | 213/729`. Nguyên nhân và cách vá: xem
`kaggle_pheA_v2_co_log.md`. File này chỉ là trình tự bấm, dán đúng thứ tự.

**Chạy TƯƠNG TÁC, đừng Save Version.** Commit không cho lấy kết quả ra giữa chừng, và bị
huỷ thì `/kaggle/working` mất sạch — đó là bài học 7 giờ vừa rồi.

---

## Bước 0 — dựng lại phiên

1. Mở notebook `Thesis` → **Edit**.
2. Panel bên phải, kiểm đủ ba thứ:

| | Đặt |
|---|---|
| Accelerator | **GPU T4 ×2** |
| Internet | **On** (phải tải UGround ~4 GB và `all_forest_dict.zip` 452 MB) |
| Input | gắn **cả hai** dataset: `thesis-preds` và `thesis-score` |

3. Menu **Run → Factory reset** (hoặc Restart & clear) cho sạch phiên cũ.
4. **Xoá hết ô cũ**, dán bốn ô dưới đây.

---

## Ô 0 — kiểm GPU (5 giây)

```python
import torch, subprocess
print("có GPU:", torch.cuda.is_available(),
      "|", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "—")
print(subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total",
                      "--format=csv,noheader"], capture_output=True, text=True).stdout)
assert torch.cuda.is_available(), "DỪNG: đang chạy CPU. Bật Accelerator = GPU T4 ×2."
```

Không in ra `Tesla T4` thì dừng ở đây, sửa panel Accelerator rồi chạy lại ô này.

---

## Ô 1 — nối dữ liệu (30 giây)

```python
import os, glob, json, shutil, random

WS = "/kaggle/working"

# tìm gói chứa mã + preds, không nướng cứng đường dẫn
cand = glob.glob("/kaggle/input/**/preds_para_p1_verb.jsonl", recursive=True)
assert cand, "DỪNG: không thấy preds_para_*.jsonl. Gắn thiếu dataset thesis-preds."
DATA = os.path.dirname(cand[0])
PKG  = DATA
print("gói preds:", DATA)

# chọn gói có ĐỦ CẢ HAI: test.jsonl đủ dòng và thư mục ảnh đủ lớn, CÙNG một chỗ
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

print(f"\nbước chạm: {len(taps)} | thiếu ảnh: {miss}")
print("lát 800 bắt đầu:", keys[:3])
assert len(taps) == 4463 and miss == 0, "DỪNG: dữ liệu không khớp bản đã chấm ba nhánh"
assert keys[:3] == [(19277, 8), (18972, 1), (18540, 1)], "DỪNG: lát khác máy nhà"
print("✔ SẴN SÀNG")
```

Ba dòng `assert` chặn đúng kiểu hỏng đã suýt xảy ra hôm trước: nối nhầm `test.jsonl` 300
dòng của cổng A rồi chấm cả buổi trên một lát không so được với mốc nào.

---

## Ô 2 — chạy biến thể đầu (~1 giờ)

```python
import os, subprocess, time, json

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"   # ← thủ phạm làm treo bản 1
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["PYTHONUNBUFFERED"] = "1"

CEIL = 74.9        # trần trên đúng lát 800 này, đo ở máy nhà bằng câu chuẩn nguyên bản
RAC  = ("it/s", "s/it", "it]")     # dấu hiệu dòng tqdm, chặn nếu còn sót

def chay(v, n=800, nhip=10):
    """Chạy một biến thể, log hiện dần ra ô này. Không phải bấm gì thêm."""
    log = f"{WS}/log_{v}.txt"
    with open(log, "w") as fw:
        p = subprocess.Popen(
            ["python", "-u", f"{WS}/harness/score_run.py", "--mode", "score",
             "--grounder", "uground", "--preds", f"{DATA}/preds_para_{v}.jsonl",
             "--out", f"{WS}/score_para_{v}.json", "--n", str(n)],
            stdout=fw, stderr=subprocess.STDOUT)   # ghi ra ĐĨA, không qua ống log Kaggle
        t0 = tlast = time.time()
        dem, du = 0, ""
        with open(log) as fr:                      # đọc song song, đuổi theo phần mới
            while True:
                *dong, du = (du + fr.read()).split("\n")
                for l in dong:
                    if any(k in l for k in RAC):
                        continue
                    dem += 1
                    # trần 3.000 dòng: sau đó chỉ giữ dòng tiến độ, khỏi ngập lại
                    if dem <= 3000 or "bước/giây" in l:
                        print(l, flush=True)
                        tlast = time.time()
                if p.poll() is not None:
                    break
                if time.time() - tlast > 120:      # im quá 2 phút thì tự báo còn sống
                    print(f"  [{time.strftime('%H:%M:%S')}] {v} · "
                          f"{(time.time()-t0)/60:.0f} phút · vẫn đang chạy", flush=True)
                    tlast = time.time()
                time.sleep(nhip)
    print(f"── {v} xong · mã thoát {p.returncode} · {(time.time()-t0)/60:.0f} phút",
          flush=True)
    return p.returncode

chay("p1_verb")
r = json.load(open(f"{WS}/score_para_p1_verb.json"))
print(f"p1_verb {r['exec_voronoi']*100:.1f}%  (trần {CEIL}%, "
      f"lệch {r['exec_voronoi']*100-CEIL:+.1f})")
```

Ô này tự cuộn log ra, **không phải bấm lại ô nào**. Cứ 10 giây nó hớt phần mới của tệp
log và in tiếp; im quá 2 phút thì tự chèn một dòng *vẫn đang chạy*, nên lúc nào cũng phân
biệt được "đang nạp mô hình" với "đã treo".

Vì sao đọc qua tệp chứ không nối thẳng `stdout` của tiến trình con vào ô: nối thẳng là quay
lại đúng cái bẫy hôm trước — ống log Kaggle nghẽn thì lệnh ghi của tiến trình con **chặn
cứng** và cả lượt chấm đứng. Ghi ra đĩa thì không ai chặn được nó; notebook chỉ là kẻ đọc
theo sau, đọc chậm hay đứt cũng không ảnh hưởng.

**Sau 4 phút phải thấy ít nhất một dòng.** Tuần tự bình thường:

```
[14:22:10] nạp bộ trỏ uground …
[14:24:51] 20/800 =  2.5% · 0.21 bước/giây · còn ~62 phút
[14:26:33] 40/800 =  5.0% · 0.22 bước/giây · còn ~58 phút
```

Trắng trơn sau 4 phút thì dừng ngay — mất 4 phút chứ không mất 7 giờ.

---

## Ô 3 — xem lại toàn bộ log (chỉ khi cần)

Ô 2 đã cuộn log ra rồi, ô này chỉ để đọc lại từ đầu hoặc soi phần đã bị trần 3.000 dòng
cắt:

```python
print(open(f"{WS}/log_p1_verb.txt").read()[-4000:])
```

---

## Ô 4 — ba biến thể còn lại (~3 giờ)

Chỉ chạy sau khi `p1_verb` ra số hợp lý (73–76% là bình thường) **và đã tải tệp về máy**:

```python
out = {"p1_verb": json.load(open(f"{WS}/score_para_p1_verb.json"))["exec_voronoi"]*100}
for v in ["p2_order", "p3_nopos", "p4_both"]:
    chay(v)
    out[v] = json.load(open(f"{WS}/score_para_{v}.json"))["exec_voronoi"]*100
    print(f"{v} {out[v]:.1f}%  lệch {out[v]-CEIL:+.1f}", flush=True)

print(f"\n{'biến thể':10s} {'điểm':>7s} {'lệch trần':>10s}")
print(f"{'(trần)':10s} {CEIL:6.1f}%")
for v, s in out.items():
    print(f"{v:10s} {s:6.1f}% {s-CEIL:+9.1f}")
```

---

## Giữa chừng: TẢI TỆP VỀ

Xong `p1_verb` là vào panel **Output** (bên phải), tải **cả hai**:

- `score_para_p1_verb.json` — số tổng
- `score_para_p1_verb_raw.jsonl` — tệp thô, cho phép đổi luật chấm rồi tính lại **mà
  không phải gọi lại bộ trỏ**, đúng như ba nhánh đã chấm trước

Phiên tương tác tự tắt sau ~20 phút **không thao tác**, nhưng ô đang chạy không tính là
rảnh — cứ để tab mở.

---

## Đọc kết quả

Mốc: **74,9%** — trần trên đúng lát 800 này, bằng câu chuẩn chưa viết lại.

| Bốn biến thể | Nghĩa là | Bài sẽ viết gì |
|---|---|---|
| đều ≈ 73–76% | bộ trỏ bền trước cách diễn đạt trong kho này | bỏ câu tự khai *"we cannot answer it"*, thay bằng số đo — kèm điều kiện chỉ đúng cho bộ trỏ này và kiểu viết lại này |
| `p1_verb` tụt mạnh | nhạy với **cách nói** → đòn Jandial et al. đứng vững | khai thẳng, và mọi số tuyệt đối yếu đi theo |
| chỉ `p3_nopos` tụt | cần **thông tin vị trí**, không phải chuyện diễn đạt | kết quả nhẹ hơn hẳn, và tách được hai nguyên nhân mà chưa ai tách trước đó |

`p1_verb` chạy trước có chủ ý: nó đổi được **91,5%** số bước, ba cái sau chỉ ~25% vì phụ
thuộc câu có mệnh đề vị trí. Cái này không suy chuyển thì ba cái kia gần như chắc chắn
cũng vậy.

Xong phép A thì phiên sau chạy phép B (UI-Venus, ~6 giờ): đổi `--grounder uivenus`, ba
nhánh, `--n 500`, mốc so đã tính sẵn 73,4 / 58,8 / 47,6, chênh +11,2 pp.

⚠️ Quota Kaggle **30 giờ GPU/tuần**, lượt treo vừa rồi đã ăn ~7 giờ. Phép A còn ~4 giờ,
phép B ~6 giờ — vừa đủ, đừng chạy thừa.
