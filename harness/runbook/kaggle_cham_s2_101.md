# Chấm s2/seed101 trên Kaggle — từng bước

Lượt chấm đầu tiên của nhánh **S2** (trụ đóng góp). · ~5,6 giờ · **0 đồng** · quota Kaggle
30 giờ/tuần, kiểm số dư trước khi bắt đầu.

> ## 🔒 Luật quyết định — đã khoá 20/8, TRƯỚC khi nhìn điểm
> **Lượt 202 vẫn chạy, bất kể điểm của s2/101 cao hay thấp.** Ngoại lệ duy nhất là **hỏng cơ
> học**, định nghĩa bằng số: `exec_voronoi` **< 12,0%** (sàn đã đo của thước) **hoặc**
> `action_ok` **< 85%** (S1 đạt 94,4%). Hai ca đó thì dừng truy lỗi. Mọi kết quả khác — **kể cả
> S2 thấp hơn S1** — vẫn chạy 202 và vẫn báo cáo.
> ⛔ **Chưa đọc Δ được ở bước này.** Luật đọc Δ đòi **trung bình hai hạt giống** (`report/106`
> mục (w)). Một hạt giống chỉ trả lời được câu "có hỏng cơ học không".

**Mốc so, lấy từ tệp thật trong `runs/`** (không phải trí nhớ):

| nhánh | exec_voronoi | KTC95 | n |
|---|---|---|---|
| trần (câu người) | **75,73%** | 74,1 – 77,3 | 4.463 |
| S1 hạt 202 | 59,62% | 57,9 – 61,3 | 4.463 |
| S1 hạt 101 | 59,11% | 57,3 – 60,8 | 4.463 |
| Base (chưa huấn luyện) | 47,59% | 45,9 – 49,3 | 4.463 |
| sàn (`f1_trong`, câu vô nội dung) | 12,0% | 9,7 – 14,4 | lát 800 |

⚠️ **Mẫu số là 4.463 cho mọi nhánh.** `score_run.py:516` cho câu rỗng vào quần thể với
`exec = 0` chứ không loại ra; nó chỉ được đánh dấu `bo_qua` trong tệp thô. Các phân tích đọc
**tệp thô** (`mde_that.py` · `doc_san.py` · `phan_tich_bon_nhanh.py`) mới bỏ dòng đó, và ở đó
S1 còn 4.462 · S2 còn 4.462 · **giao hai nhánh 4.461**.

---

## Bước 0 — kiểm ở máy nhà trước, MIỄN PHÍ

```
python3 harness/kiem_preds.py runs/preds_s2_seed101.jsonl --doi-chieu runs/preds_s1_seed101.jsonl
```

Vài giây, chặn một lỗi tốn 5,6 giờ quota.

⚠️ **Phép số 5 SẼ BÁO LỆCH — đã biết trước, không phải lỗi mới.** Nó đòi bước bị bỏ trùng khít
nhánh đối chiếu, mà s2/101 bỏ **`(20011, 2)`** còn hai lượt S1 bỏ `(18710, 1)`. Nguyên nhân đã
truy: khai báo của bước đó rơi vào vòng lặp `U+200A` tới cạn ngân sách sinh nên không đóng thẻ
`</desc>`, và `strip_desc` (`infer_branch.py:40-43`) xoá từ `<desc>` tới hết ⇒ câu rỗng.
**Bảy phép còn lại phải sạch.**

---

## Bước 1 — đưa tệp lên Kaggle

Tệp duy nhất cần upload: **`runs/preds_s2_seed101.jsonl`** (~2,3 MB).

1. Mở dataset **`thesis-preds`** → **New Version**.
2. Kéo tệp vào, **giữ nguyên mọi tệp cũ**.
3. Create → đợi Kaggle xử lý (~1 phút).
4. Trong notebook, panel **Input** → cập nhật dataset lên version mới.

Không cần upload gì khác: ảnh và `test.jsonl` đã nằm ở dataset `thesis-score`.

---

## Bước 2 — ô 0: kiểm GPU (5 giây)

```python
import torch
print("có GPU:", torch.cuda.is_available(),
      "|", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "—")
assert torch.cuda.is_available(), "DỪNG: đang chạy CPU. Bật Accelerator = GPU T4 ×2."
```

Panel Accelerator hay tự trả về *None* khi mở lại notebook.

---

## Bước 3 — ô 1: nối dữ liệu và kiểm tệp preds ngay trên Kaggle

```python
import os, glob, json, shutil

WS   = "/kaggle/working"
TEN  = "s2_seed101"
SIG  = "lora:s2_seed101"          # infer_branch.py:411 → "lora:" + tên thư mục adapter
RONG = [(20011, 2)]               # bước câu rỗng ĐÃ BIẾT của lượt này

cand = glob.glob(f"/kaggle/input/**/preds_{TEN}.jsonl", recursive=True)
assert cand, f"DỪNG: chưa thấy preds_{TEN}.jsonl. Đã cập nhật dataset lên version mới chưa?"
PREDS = cand[0]; print("preds:", PREDS)

mp = glob.glob("/kaggle/input/**/harness/score_run.py", recursive=True)
assert mp, "DỪNG: không thấy harness/score_run.py trong dataset"
PKG = os.path.dirname(os.path.dirname(mp[0]))

# chọn gói có ĐỦ CẢ HAI: test.jsonl đủ dòng và ảnh đủ nhiều, CÙNG một chỗ
best = None
for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True):
    root = os.path.dirname(t)
    rows = sum(1 for _ in open(t, encoding="utf-8"))
    nimg = len(glob.glob(os.path.join(root, "images", "*.png")))
    print(f"  {rows:5d} dòng · {nimg:5d} ảnh  {root}")
    if rows >= 6900 and nimg >= 4400 and (best is None or nimg > best[2]):
        best = (t, rows, nimg, root)
assert best, "DỪNG: không gói nào có đủ test.jsonl 6.958 dòng lẫn 4.463 ảnh"
TEST_JSONL, _, _, ROOT = best

shutil.copytree(f"{PKG}/harness", f"{WS}/harness", dirs_exist_ok=True)
dst = f"{WS}/harness/dg1_cache/test_ac"; os.makedirs(dst, exist_ok=True)
for src, name in [(TEST_JSONL, "test.jsonl"), (os.path.join(ROOT, "images"), "images")]:
    link = os.path.join(dst, name)
    if os.path.islink(link): os.remove(link)
    elif os.path.isdir(link): shutil.rmtree(link)
    elif os.path.exists(link): os.remove(link)
    os.symlink(src, link)

# ── kiểm NGAY TRÊN TỆP KAGGLE SẼ ĐỌC, đúng bốn thứ quyết định con số ──────────────
recs = [json.loads(l) for l in open(f"{dst}/test.jsonl", encoding="utf-8")]
taps = [r for r in recs if r["action"].get("action_type") in ("click", "long_press")
        and "x" in r["action"]]
miss = sum(1 for r in taps if not os.path.exists(os.path.join(dst, r["image"])))
assert len(taps) == 4463 and miss == 0, f"DỪNG: {len(taps)} bước chạm, thiếu {miss} ảnh"
assert "app_seen_in_train" in recs[0], "DỪNG: test.jsonl CHƯA gắn nhãn app — lát cắt phụ sẽ rỗng"

P = {}
for l in open(PREDS, encoding="utf-8"):
    o = json.loads(l); P[(o["episode_id"], o["step_id"])] = o
kt   = {(r["episode_id"], r["step_id"]) for r in taps}
sig  = {o.get("run") for o in P.values() if o.get("run")}
rong = sorted(k for k in P if k in kt and not str(P[k].get("pred", "")).strip())
sot  = sum(1 for o in P.values() if "<desc>" in str(o.get("pred", "")))

assert len(P) == 6958,      f"DỪNG: preds có {len(P)} bản ghi, cần 6958"
assert sig == {SIG},        f"DỪNG: chữ ký {sig}, cần đúng {SIG}"
assert rong == RONG,        f"DỪNG: bước rỗng {rong}, cần đúng {RONG}"
assert sot == 0,            f"DỪNG: {sot} câu còn sót <desc> — khâu cắt khai báo hỏng"
assert kt <= set(P),        "DỪNG: preds thiếu bước chạm so với test.jsonl"
print(f"\npreds {len(P)} · chữ ký {sig} · bước rỗng {rong} · sót <desc> {sot}")
print("✔ SẴN SÀNG — chấm đủ 4.463 bước, cùng mẫu số với S1/Base/trần")
```

Năm `assert` cuối lặp lại phép kiểm ở máy nhà **trên đúng tệp Kaggle sẽ đọc**, nên bắt được cả
trường hợp upload nhầm tệp lẫn dataset version chưa cập nhật. Riêng `sot == 0` là phép **chỉ
S2 mới cần**: sót `<desc>` nghĩa là bộ trỏ đọc cả dòng khai báo thay vì câu, điểm sẽ sai mà
không có tiếng động nào.

---

## Bước 4 — ô 2: chấm (~5,6 giờ)

```python
import os, subprocess, time

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"   # thủ phạm làm treo lượt 17/8 suốt 7 giờ
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["PYTHONUNBUFFERED"] = "1"
RAC = ("it/s", "s/it", "it]")

def chay(ten, preds, nhip=15):
    log = f"{WS}/log_{ten}.txt"
    with open(log, "w") as fw:
        p = subprocess.Popen(
            ["python", "-u", f"{WS}/harness/score_run.py", "--mode", "score",
             "--grounder", "uground", "--preds", preds,
             "--out", f"{WS}/score_{ten}.json"],
            stdout=fw, stderr=subprocess.STDOUT)   # ghi ra ĐĨA, không qua ống log Kaggle
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
                    print(f"  [{time.strftime('%H:%M:%S')}] {ten} · "
                          f"{(time.time()-t0)/60:.0f} phút · vẫn đang chạy", flush=True)
                    tlast = time.time()
                time.sleep(nhip)
    print(f"── {ten} xong · mã thoát {p.returncode} · {(time.time()-t0)/60:.0f} phút", flush=True)
    return p.returncode

chay(TEN, PREDS)
```

**Không có `--n`** ⇒ chấm đủ 4.463 bước.

· **CHẠY TƯƠNG TÁC, đừng Save Version cho lượt này** — commit bị huỷ thì Kaggle **không lưu**
`/kaggle/working`, kể cả tệp thô đã ghi dần ⇒ dừng là mất trắng.
· **Sau 4 phút phải có ít nhất một dòng.** Không có thì dừng ngay — chi phí biết mình sai giảm
từ 7 giờ xuống 4 phút. Lượt 17/8 treo 7 tiếng vì `tqdm` in mỗi cập nhật thành một dòng làm
ngập ống log Kaggle; đó là lý do có ba biến môi trường ở đầu ô và việc ghi ra đĩa.
· Tốc độ mong đợi **~0,22 bước/giây** ⇒ `x/4463` tăng đều, xong sau ~5,6 giờ.
· **Bảo hiểm cho lượt dài:** khoảng **giữa (~3 giờ)** mở một ô khác, tải `score_s2_seed101_raw.jsonl`
(bản dở) về máy. `score_run.py` **ghi dần và nối tiếp được** — phiên chết thì đưa tệp dở lên
dataset rồi chạy lại, nó chấm tiếp chứ không từ đầu.

---

## Bước 4b — CHẠY BẰNG COMMIT (khi phải tắt máy nhà)

Lượt chấm 5,6 giờ mà không ngồi canh được thì dùng **Save Version → Save & Run All (Commit)**.
Nó chạy trong môi trường lô, **không lệ thuộc trình duyệt**. Runbook cũ khuyên chạy tương tác,
nhưng lời khuyên đó dành cho **lượt ĐẦU của một đường ống chưa từng chạy** — đường chấm này
đã chạy trọn **bốn lần** (trần · s1/101 · s1/202 · Base) nên rủi ro còn lại chỉ là hạ tầng.

### Ba thiết lập PHẢI đúng, kiểm trước khi bấm Commit

| | vì sao |
|---|---|
| **Internet: ON** | `UGround.__init__` nạp `osunlp/UGround-V1-2B` **từ HuggingFace** (`score_run.py:97`). Tắt mạng là chết ở khâu nạp mô hình sau ~2 phút |
| **Accelerator: GPU T4 ×2** | panel hay tự trả về *None* khi mở lại notebook |
| **Input: dataset đã lên version mới** | thiếu bước này thì ô 1 rớt `assert` ngay, mất một lượt commit |

### Trước khi Commit: chạy tương tác ô 0 và ô 1

Hai ô đó xong trong ~1 phút và bắt gần hết các lỗi chặn. Rớt `assert` trong commit thì vẫn
biết, nhưng phải chờ hàng đợi và mất một lượt.

### Ô 2 bản commit — có ĐỒNG HỒ CHẶN

```python
import os, subprocess, time

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["PYTHONUNBUFFERED"] = "1"
RAC      = ("it/s", "s/it", "it]")
TRAN_GIO = 8.0        # mong đợi 5,6 giờ; quá 8 là có gì đó hỏng

def chay(ten, preds, nhip=15):
    log = f"{WS}/log_{ten}.txt"
    with open(log, "w") as fw:
        p = subprocess.Popen(
            ["python", "-u", f"{WS}/harness/score_run.py", "--mode", "score",
             "--grounder", "uground", "--preds", preds,
             "--out", f"{WS}/score_{ten}.json"],
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
                # ⏱ ĐỒNG HỒ CHẶN — biến "mất trắng" thành "mất một nửa"
                if time.time() - t0 > TRAN_GIO*3600:
                    print(f"⚠️ QUÁ {TRAN_GIO} GIỜ — giết tiến trình để notebook kết thúc SẠCH,"
                          " nhờ vậy tệp thô dở vẫn được lưu thành Output", flush=True)
                    p.terminate()
                    try: p.wait(120)
                    except Exception: p.kill()
                    break
                if time.time() - tlast > 120:
                    print(f"  [{time.strftime('%H:%M:%S')}] {ten} · "
                          f"{(time.time()-t0)/60:.0f} phút · vẫn đang chạy", flush=True)
                    tlast = time.time()
                time.sleep(nhip)
    print(f"── {ten} dừng · mã thoát {p.returncode} · {(time.time()-t0)/60:.0f} phút", flush=True)
    return p.returncode

chay(TEN, PREDS)
```

⭐ **Đồng hồ chặn là chỗ khác biệt duy nhất, và nó quan trọng.** Commit **thất bại** thì Kaggle
**không lưu `/kaggle/working`** — mất cả tệp thô đã ghi dần, tức mất trọn 5-8 giờ quota. Giết
tiến trình rồi để notebook **chạy hết bình thường** thì commit **thành công**, Output được lưu,
và `score_run.py` **nối tiếp được** từ tệp thô dở ở lượt sau. Đây chính là kịch bản đã cắn ngày
17/8: lượt đó treo **7 giờ** rồi mất sạch.

### Ô 3 bản commit — chịu được lượt chấm dở

```python
import json, os

fj, fr = f"{WS}/score_{TEN}.json", f"{WS}/score_{TEN}_raw.jsonl"
raw = [json.loads(l) for l in open(fr, encoding="utf-8")] if os.path.exists(fr) else []
print(f"tệp thô: {len(raw):,} / 4.463 bước")

if not os.path.exists(fj):
    print("⚠️ CHƯA XONG — không có tệp điểm. Tải score_*_raw.jsonl về, đưa lên dataset,")
    print("   chạy lại: score_run.py sẽ CHẤM TIẾP phần còn thiếu, không làm lại từ đầu.")
else:
    r  = json.load(open(fj)); e = r["exec_voronoi"]*100
    ci = [c*100 for c in r["ci_voronoi"]]
    ok = [o for o in raw if "bo_qua" not in o]
    aok = sum(o["action_ok"] for o in ok)/len(ok)*100
    print(f"s2/101 : {e:5.2f}%  KTC95 [{ci[0]:.1f} – {ci[1]:.1f}]  n={r['n']}")
    print(f"action_ok: {aok:.1f}%   (S1 đạt 94,4%)")
    print("mốc so — trần 75,73 · S1/202 59,62 · S1/101 59,11 · Base 47,59 · sàn 12,0")
    print("\n⛔ HỎNG CƠ HỌC ⇒ DỪNG" if (e < 12.0 or aok < 85.0)
          else "\n✅ KHÔNG hỏng cơ học ⇒ train hạt giống 202, bất kể con số trên")
    print("⛔ CHƯA đọc Δ — luật đòi TRUNG BÌNH HAI HẠT GIỐNG (report/106 mục w)")
```

### Sau khi Commit

Đóng trình duyệt, tắt máy thoải mái. Xem lại ở tab **Versions** của notebook; xong thì tải hai
tệp ở panel **Output**. ⚠️ Chọn **Save & Run All (Commit)**, **không** phải *Quick Save* — Quick
Save chỉ chụp lại trạng thái hiện tại, không chạy gì.

## Bước 5 — ô 3: đọc kết quả, và ÁP LUẬT ĐÃ KHOÁ

```python
import json

r  = json.load(open(f"{WS}/score_{TEN}.json"))
e  = r["exec_voronoi"]*100; ci = [c*100 for c in r["ci_voronoi"]]

raw = [json.loads(l) for l in open(f"{WS}/score_{TEN}_raw.jsonl", encoding="utf-8")]
ok  = [o for o in raw if "bo_qua" not in o]
aok = sum(o["action_ok"] for o in ok)/len(ok)*100

print(f"s2/101 : {e:5.2f}%  KTC95 [{ci[0]:.1f} – {ci[1]:.1f}]  n={r['n']}  "
      f"cụm {r['clusters']} (hiệu dụng {r['g_eff']:.1f})")
print(f"action_ok: {aok:.1f}%   (S1 đạt 94,4%)")
print(f"tệp thô  : {len(raw):,} dòng · bỏ qua {len(raw)-len(ok)}")
print("\nmốc so — trần 75,73 · S1/202 59,62 · S1/101 59,11 · Base 47,59 · sàn 12,0")

hong = e < 12.0 or aok < 85.0
print("\n" + "="*62)
if hong:
    print("⛔ HỎNG CƠ HỌC theo luật khoá 20/8 ⇒ DỪNG, truy lỗi, KHÔNG train 202")
else:
    print("✅ KHÔNG hỏng cơ học ⇒ train hạt giống 202 như đã khoá, bất kể con số trên")
print("⛔ CHƯA đọc Δ = S2 − S1 ở đây — luật đòi TRUNG BÌNH HAI HẠT GIỐNG (report/106 mục w)")
```

⚠️ **Cấm đọc Δ ở bước này** dù con số đã hiện ra. Một hạt giống không phân biệt được hiệu ứng
với nhiễu giữa các lượt train — nhiễu đó đo trên S1 là **0,52 pp**, và ngưỡng Δ khoá ở **2,8 pp**
là ngưỡng cho **trung bình hai hạt giống**.

---

## Bước 6 — tải về máy nhà

Từ panel **Output**, tải **cả hai** vào `runs/`:

- `score_s2_seed101.json`
- `score_s2_seed101_raw.jsonl` ← **quan trọng hơn**: đổi luật chấm hay thêm lát cắt thì tính
  lại từ đây, **không gọi lại bộ trỏ** (tiết kiệm 5,6 giờ mỗi lần)

Rồi ở máy nhà:

```
python3 harness/doc_diem_tam.py                 # gộp số các nhánh đã chấm
```

**Việc kế:** train hạt giống **202** (~26 giờ Colab, ~126 đơn vị) → chấm 202 → **mới** đọc Δ.

📌 Lát cắt đã đăng ký trước, đọc sau khi có cả hai hạt giống, tính từ tệp thô nên **không tốn
GPU**: phân tầng theo *thành phần có kích hoạt hay không* (**324 bước = 7,26%** không sinh
`<desc>`, danh sách đóng băng ở `Drive/thesis/preds/co_rac_s2_seed101.json`). S2 chỉ hơn ở nhóm
**có** kích hoạt ⇒ cơ chế đúng thiết kế; hơn đều cả hai nhóm ⇒ phần hơn **không đến từ thành
phần**.
