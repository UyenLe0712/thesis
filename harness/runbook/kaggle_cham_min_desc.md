# CHẤM MIN-DESC + CE2-S2 TRÊN KAGGLE — dán thẳng, tự đủ

Chấm hai checkpoint hạt giống 101 trên đủ **4.463 bước chạm**, cùng mẫu số với S1/Base/trần.
**~10,8 giờ Kaggle · 0 đồng** — đo thật trên log lượt S2 ngày 20/8: **0,23 bước/giây** ⇒
4.463 bước = **5,4 giờ mỗi nhánh**. Quota 30 giờ/tuần nên hai lượt vừa vặn, nhưng **phải tách
làm hai commit**, xem Bước 4b.

Trạng thái nhánh: **thăm dò, một hạt giống** — `report/106` mục **(x8)**. Đọc mục đó trước khi
viết bất cứ câu nào về kết quả.

> ⛔ **Ba luật, mỗi luật là một lần đã trả giá:**
> 1. **Chạy TƯƠNG TÁC cho lượt đầu, đừng Save Version.** Commit bị huỷ thì Kaggle không lưu
>    `/kaggle/working`.
> 2. **Không để `tqdm` in ra ống log Kaggle.** Lượt 17/8 treo **7 giờ** vì log ngập: `tqdm` ngoài
>    terminal in mỗi cập nhật thành một dòng, Kaggle chặn log khi vượt trần, tiến trình kẹt cứng ở
>    lệnh ghi stdout. Ô 2 đã vá bằng biến môi trường **và** cho tiến trình con ghi ra **tệp**.
> 3. **Không có dòng nhịp sống nào sau 4 phút thì dừng ngay.** Chi phí biết mình sai: 7 giờ → 4 phút.

---

## Bước 0 — ở máy nhà, MIỄN PHÍ, trước khi đụng Kaggle

Hai tệp preds do Colab sinh nằm trên Drive: `preds_min_desc_seed101.jsonl` và
`preds_ce2_s2_seed101.jsonl`. Tải về máy, rồi kiểm:

```python
import json
for ten in ("min_desc_seed101", "ce2_s2_seed101"):
    P = {}
    for l in open(f"runs/preds_{ten}.jsonl", encoding="utf-8"):
        o = json.loads(l); P[(o["episode_id"], o["step_id"])] = o
    sig  = {o.get("run") for o in P.values() if o.get("run")}
    rong = sorted(k for k in P if not str(P[k].get("pred", "")).strip())
    sot  = sum(1 for o in P.values() if "<desc>" in str(o.get("pred", "")))
    print(f"{ten:20s} n={len(P)} ← 6958 · chữ ký {sig} · rỗng {len(rong)} · sót <desc> {sot} ← 0")
```

`n` phải là **6958**, chữ ký đúng `lora:<tên thư mục adapter>`, `sót <desc>` phải là **0**.
⚠️ Sót `<desc>` nghĩa là bộ trỏ sẽ đọc cả dòng khai báo thay vì câu — điểm sai mà không có
tiếng động nào. Đây là phép **chỉ nhánh có khai báo mới cần**.

---

## Bước 1 — đưa hai tệp lên Kaggle

1. Mở dataset **`thesis-preds`** → **New Version**
2. Kéo **cả hai** tệp vào, **giữ nguyên mọi tệp cũ**
3. Create → đợi Kaggle xử lý (~1 phút)
4. Trong notebook, panel **Input** → cập nhật `thesis-preds` lên version mới

Không cần upload gì khác: ảnh và `test.jsonl` đã nằm ở dataset `thesis-score`.

⛔ **ĐỪNG upload đè `harness/` lên dataset.** Kiểm 24/8: `score_run.py` trên Kaggle là
**39.763 byte, md5 `f837c834c8d1`** — một bản trung gian chưa commit, upload hồi làm phép B 20/8,
**không khớp commit nào**. Máy nhà đang là 41.286 byte / `bb8386f8a552`.

**Vẫn phải giữ bản Kaggle**, vì ba lẽ:
· `metric_exec.py` — nơi chứa luật chấm thật — **khớp tuyệt đối** (`9bf0b8414545`);
· chỗ lệch thuộc hai commit sau đó, cả hai đều về **UI-Venus** và cỡ ảnh, mà lượt này chạy
  `--grounder uground`;
· ⭐ **S1/101, S1/202, S2/101, Base và trần đều được chấm bằng đúng bản này.** Mọi mốc so
  (59,11 · 59,62 · 57,18 · 47,59 · 75,73) do nó sinh ra. Thay mã là chấm nhánh mới bằng thước
  khác các nhánh cũ — cùng loại sai lầm mà việc cố ý không sửa lỗi `canon_action` go-back
  đang tránh.

⇒ Ô 1a in cảnh báo `⚠️ KHÁC máy nhà` cho `score_run.py` là **bình thường và đúng**. Chỉ cần
`metric_exec.py` khớp. Nếu một ngày `metric_exec.py` lệch thì mới là dừng hẳn.

⚠️ Kaggle **không ghi đè** tệp trùng tên trong version mới — nếu bạn từng upload bản `--limit`
cùng tên thì xoá nó đi, kẻo ô 1 bắt nhầm.

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

## Bước 3 — ô 1: nối dữ liệu, và SÁU phép kiểm trên đúng tệp Kaggle sẽ đọc

```python
import os, glob, json, shutil

WS  = "/kaggle/working"
TEN = ["min_desc_seed101", "ce2_s2_seed101"]      # hai nhánh phải chấm, dùng cho ô đọc kết quả

# ★ NHÁNH CỦA COMMIT NÀY — khai ở đây, ô 1b và ô 2 đều đọc. Commit sau đổi đúng dòng này.
#   Khai ở ô 1 chứ không ở ô 2 vì ô 1b (tiền bay) chạy TRƯỚC ô 2 và cần kiểm nó.
TEN_COMMIT = ["min_desc_seed101"]                 # ★ đổi thành ["ce2_s2_seed101"] cho lượt 2

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

# ⚠️ DỌN TRƯỚC. Ô này phải chạy lại được nhiều lần: nếu {WS}/harness đã tồn tại và bên
#    trong có SYMLINK (do lần chạy trước tạo), copytree đâm vào symlink rồi gom lỗi và
#    raise shutil.Error. Đã cắn 24/8 khi chạy ô 1a tiền kiểm rồi mới chạy ô 1.
shutil.rmtree(f"{WS}/harness", ignore_errors=True)
shutil.copytree(f"{PKG}/harness", f"{WS}/harness", dirs_exist_ok=True)
dst = f"{WS}/harness/dg1_cache/test_ac"; os.makedirs(dst, exist_ok=True)
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
assert len(taps) == 4463 and miss == 0, f"DỪNG: {len(taps)} bước chạm, thiếu {miss} ảnh"
assert "app_seen_in_train" in recs[0], "DỪNG: test.jsonl CHƯA gắn nhãn app — lát cắt phụ sẽ rỗng"
kt = {(r["episode_id"], r["step_id"]) for r in taps}

PREDS = {}
for ten in TEN:
    cand = [p for p in glob.glob(f"/kaggle/input/**/preds_{ten}.jsonl", recursive=True)]
    assert cand, f"DỪNG: chưa thấy preds_{ten}.jsonl. Đã cập nhật dataset lên version mới chưa?"
    p = cand[0]
    P = {}
    for l in open(p, encoding="utf-8"):
        o = json.loads(l); P[(o["episode_id"], o["step_id"])] = o
    sig  = {o.get("run") for o in P.values() if o.get("run")}
    rong = sorted(k for k in P if k in kt and not str(P[k].get("pred", "")).strip())
    sot  = sum(1 for o in P.values() if "<desc>" in str(o.get("pred", "")))
    assert len(P) == 6958, f"DỪNG {ten}: preds có {len(P)} bản ghi, cần 6958"
    assert len(sig) == 1,  f"DỪNG {ten}: chữ ký lẫn lộn {sig}"
    assert ten in list(sig)[0], f"DỪNG {ten}: chữ ký {sig} không khớp tên nhánh"
    assert sot == 0,       f"DỪNG {ten}: {sot} câu còn sót <desc> — khâu cắt khai báo hỏng"
    assert kt <= set(P),   f"DỪNG {ten}: preds thiếu bước chạm so với test.jsonl"
    PREDS[ten] = p
    print(f"✔ {ten:20s} {len(P)} bản ghi · chữ ký {sig} · rỗng {len(rong)} · sót <desc> {sot}")
print("\n✔ SẴN SÀNG — chấm đủ 4.463 bước, cùng mẫu số với S1/Base/trần")
```

Sáu `assert` lặp lại phép kiểm ở máy nhà **trên đúng tệp Kaggle sẽ đọc**, nên bắt được cả trường
hợp upload nhầm tệp lẫn dataset version chưa cập nhật.

⚠️ **Bước rỗng không phải lỗi** — `score_run.py` tính nó là `exec = 0` và giữ trong mẫu số 4.463.
Ô chỉ in ra để bạn biết, không `assert`.

---

## Bước 4 — ô 2 bản TƯƠNG TÁC: chấm tuần tự (~10,8 giờ cho cả hai)

```python
import os, subprocess, time

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"   # thủ phạm làm treo lượt 17/8 suốt 7 giờ
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["PYTHONUNBUFFERED"] = "1"
RAC = ("it/s", "s/it", "it]")

def chay(ten, preds):
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
                time.sleep(5)
    # ⚠️ In MÃ THOÁT, đừng in "XONG" trơn. score_run.py chết sau 3 phút thì vòng lặp cũng
    #    thoát y như khi chấm xong, và bản cũ in "=== XONG sau 0.05 giờ ===" — trông như đạt.
    print(f"\n=== {ten} dừng · mã thoát {p.returncode} "
          f"({'XONG' if p.returncode == 0 else '⛔ LỖI — đọc ' + log}) · "
          f"{(time.time()-t0)/3600:.2f} giờ ===\n", flush=True)

for ten in TEN:
    chay(ten, PREDS[ten])
```

⏱ **Không có dòng nào sau 4 phút ⇒ dừng ngay**, đừng chờ. Nhịp sống in mỗi 2 phút khi im.

---

## Bước 4b — CHẠY BẰNG COMMIT, để đi ngủ

⚠️ **MỘT NHÁNH MỘT COMMIT.** Gộp cả hai là 10,8 giờ + hai lần nạp mô hình, quá sát **trần 12 giờ**
của Kaggle. Vượt trần thì commit **thất bại** và Kaggle **không lưu `/kaggle/working`** — mất cả
tệp thô đã ghi dần. Chấm `min_desc_seed101` trước, `ce2_s2_seed101` ở commit sau.

### Ba thiết lập PHẢI đúng, kiểm trước khi bấm Commit

| | vì sao |
|---|---|
| **Internet: ON** | `UGround.__init__` nạp `osunlp/UGround-V1-2B` **từ HuggingFace** (`score_run.py:97`). Tắt mạng là chết ở khâu nạp mô hình sau ~2 phút |
| **Accelerator: GPU T4 ×2** | panel hay tự trả về *None* khi mở lại notebook |
| **Input: `thesis-preds` đã lên version mới** | thiếu bước này thì ô 1 rớt `assert`, mất một lượt commit và một chỗ trong hàng đợi |

### Ô 1b — TIỀN BAY, chạy tương tác ngay trước khi bấm Commit

Ba thứ trong bảng trên là **thiết lập trên panel**, mà panel thì nói dối được. Ô này hỏi thẳng
máy, đúng nguyên tắc đã trả giá ngày 20/8: *bắt tiến trình in ra cấu hình nó THẬT SỰ đang dùng.*

```python
import torch, urllib.request, hashlib, os, glob

print("① GPU đếm được :", torch.cuda.device_count(),
      "·", [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])
print("   ← phải là 2 × T4. `get_device_name(0)` ở ô 0 chỉ in card THỨ NHẤT nên không")
print("     phân biệt được T4×1 với T4×2. Bốn nhánh đã chấm đều chạy T4×2.")

try:
    urllib.request.urlopen("https://huggingface.co", timeout=15)
    print("② Internet     : ON ✅")
except Exception as e:
    print("② Internet     : ⛔ TẮT —", e, "\n   score_run.py chết ở khâu nạp UGround sau ~2 phút")

print("③ TEN_COMMIT   :", TEN_COMMIT)
assert len(TEN_COMMIT) == 1, "⛔ commit này phải chấm ĐÚNG MỘT nhánh — xem Bước 4b"
print("④ preds nhánh  :", PREDS[TEN_COMMIT[0]])
assert TEN_COMMIT[0] in PREDS[TEN_COMMIT[0]], "⛔ đường dẫn preds không khớp tên nhánh"

# ⑤ THƯỚC — phép kiểm quan trọng nhất, và là thứ duy nhất không sửa được sau khi đã chấm.
#    Tính md5 trên bản {WS}/harness mà score_run.py SẼ THẬT SỰ import, không phải bản nằm
#    trong dataset. Nguyên tắc 20/8: đọc thứ tiến trình dùng, đừng đọc thứ mình nghĩ nó dùng.
MD5_CHUAN = {"metric_exec.py": "9bf0b84145458fd55919a5e161b9766f",   # luật chấm — PHẢI trùng
             "score_run.py":   "f837c834c8d1"}                       # bản Kaggle, 12 ký tự đầu
for ten, chuan in MD5_CHUAN.items():
    m = hashlib.md5(open(f"{WS}/harness/{ten}", "rb").read()).hexdigest()
    if ten == "metric_exec.py":
        print(f"⑤ {ten:<15}: {m}", "✅ TRÙNG" if m == chuan else "⛔ LỆCH — DỪNG HẲN")
        assert m == chuan, ("⛔ metric_exec.py KHÁC bản đã chấm S1/S2/Base/trần. Chấm nhánh mới "
                            "bằng thước khác các nhánh cũ là hỏng toàn bộ phép so.")
    else:
        print(f"  {ten:<15}: {m[:12]}",
              "(khớp bản Kaggle — bình thường, xem Bước 1)" if m.startswith(chuan)
              else "⚠️ khác bản Kaggle đã dùng — chỉ metric_exec mới là dừng hẳn")

# ⑥ Dataset nào đang gắn — bắt ca notebook SAO CHÉP bị rớt Input hoặc gắn version cũ
print("⑥ Input đang gắn:")
for d in sorted(glob.glob("/kaggle/input/*")):
    print("   ", d)

# ⑦ NIÊM PHONG nhánh. Ô 2 phải khớp giá trị này, nếu không thì nó đã gán đè TEN_COMMIT.
NHANH_CHOT = TEN_COMMIT[0]
print("⑦ niêm phong   :", NHANH_CHOT)
```

⚠️ **`device_count()` ra 1 thì đổi Accelerator sang `GPU T4 ×2`** rồi chạy lại ô 0 → ô 1 → ô 1b.
Kết quả không đổi (fp16, `device_map="auto"` chỉ chia lớp chứ không đổi phép tính), nhưng bốn
nhánh đã chấm đều chạy T4×2 — giữ nguyên dụng cụ thì khỏi phải khai thêm một lệch chuẩn.

### Ô 4 — dọn symlink, đặt CUỐI notebook

```python
import os
for n in ("test.jsonl", "images"):
    l = f"{WS}/harness/dg1_cache/test_ac/{n}"
    if os.path.islink(l): os.remove(l); print("đã gỡ symlink", l)
```

Ô 1 tạo symlink `images` → 4.463 ảnh (1,7 GB) nằm trong `/kaggle/working`, mà `/kaggle/working`
chính là thứ Kaggle đóng gói thành **Output**. Gỡ sau khi chấm xong thì Output chỉ còn tệp điểm
và tệp thô (~2 MB), tải về nhanh. Chạy ô này **sau** ô 2, không bao giờ trước.

### Chạy tương tác ô 0 và ô 1 TRƯỚC khi Commit

Hai ô đó xong trong ~1 phút và bắt gần hết lỗi chặn. Rớt `assert` trong commit thì vẫn biết,
nhưng phải chờ hàng đợi và mất một lượt.

### Ô 2 bản commit — có ĐỒNG HỒ CHẶN

```python
import os, subprocess, time

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["PYTHONUNBUFFERED"] = "1"
RAC      = ("it/s", "s/it", "it]")
TRAN_GIO = 8.0        # mong đợi 5,4 giờ; quá 8 là có gì đó hỏng, và 12 là trần Kaggle

# ⛔ MỘT NHÁNH MỘT COMMIT. Đo thật trên log Kaggle 20/8: 0,23 bước/giây ⇒ 4.463 bước =
#    5,4 giờ MỖI nhánh. Chạy `for ten in TEN` là 10,8 giờ + hai lần nạp mô hình, sát
#    trần 12 giờ tới mức không còn biên nào. Và `TRAN_GIO` là đồng hồ TỪNG NHÁNH: hai
#    nhánh × 8 giờ = 16 giờ, tức nó KHÔNG chặn được ca này. Commit vượt trần thì Kaggle
#    KHÔNG lưu /kaggle/working ⇒ mất luôn cả tệp thô đã ghi dần của nhánh đầu.
# ⛔⛔ ĐÃ CẮN NGÀY 25/8, MẤT 5,3 GIỜ QUOTA. Bản cũ của ô này có dòng
#     `TEN_COMMIT = ["min_desc_seed101"]` NGAY TẠI ĐÂY. Ô 1b chạy trước, đọc giá trị của
#     Ô 1 nên in ra ce2 — ĐÚNG; rồi ô này gán đè về min_desc và chấm nhầm nhánh suốt 5,3
#     giờ. Không lỗi, không cảnh báo, tệp điểm ra tên min_desc mà không ai nhìn cho tới
#     lúc giải nén. NẾU TRONG NOTEBOOK CỦA BẠN CÒN DÒNG GÁN ĐÓ Ở ĐÂY — XOÁ NÓ.
#     Hai `assert` dưới là chốt chặn: chúng nổ trong 1 giây, không phải sau 5,3 giờ.
assert len(TEN_COMMIT) == 1, "⛔ chạy lại Ô 1: TEN_COMMIT phải có đúng một nhánh"
assert TEN_COMMIT[0] == NHANH_CHOT, (
    f"⛔ TEN_COMMIT bị GÁN ĐÈ sau ô 1b: ô 1b niêm phong {NHANH_CHOT!r}, tới đây thành "
    f"{TEN_COMMIT[0]!r}. Xoá dòng gán TEN_COMMIT nằm trong chính ô này.")
print("▶ CHẤM NHÁNH:", TEN_COMMIT[0], "·", PREDS[TEN_COMMIT[0]], flush=True)

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

for ten in TEN_COMMIT:
    chay(ten, PREDS[ten])
```

⛔ **Xoá ô 2 bản TƯƠNG TÁC khỏi notebook trước khi Commit.** *Save & Run All* chạy **mọi ô theo
thứ tự** — để cả hai bản trong notebook thì ô tương tác chấm cả hai nhánh (10,8 giờ) rồi ô commit
chạy tiếp, chắc chắn vượt trần 12 giờ. Giữ đúng **một** ô 2.

⭐ **Đồng hồ chặn là chỗ khác biệt duy nhất, và nó quan trọng.** Commit **thất bại** thì Kaggle
**không lưu `/kaggle/working`** — mất cả tệp thô đã ghi dần, tức mất trọn 5–8 giờ quota. Giết
tiến trình rồi để notebook chạy hết bình thường thì commit **thành công**, Output được lưu, và
`score_run.py` **nối tiếp được** từ tệp thô dở ở lượt sau. Đây đúng kịch bản đã cắn ngày 17/8:
lượt đó treo 7 giờ rồi mất sạch.

### Ô 3 bản commit — chịu được lượt chấm dở

```python
import json, os, traceback
try:                       # ⛔ ô này chạy SAU ô 2 ⇒ không bao giờ được ném lỗi
 for ten in TEN:
    fj, fr = f"{WS}/score_{ten}.json", f"{WS}/score_{ten}_raw.jsonl"
    raw = [json.loads(l) for l in open(fr, encoding="utf-8")] if os.path.exists(fr) else []
    print(f"\n=== {ten} ===  tệp thô: {len(raw):,} / 4.463 bước")
    if not os.path.exists(fj):
        print("⚠️ CHƯA XONG — không có tệp điểm. Tải score_*_raw.jsonl về, đưa lên dataset,")
        print("   chạy lại: score_run.py CHẤM TIẾP phần còn thiếu, không làm lại từ đầu.")
        continue
    r  = json.load(open(fj)); e = r["exec_voronoi"]*100
    ci = [c*100 for c in r["ci_voronoi"]]
    ok = [o for o in raw if "bo_qua" not in o]
    aok = sum(o.get("action_ok", 0) for o in ok)/len(ok)*100 if ok else 0
    print(f"  exec {e:5.2f}%  KTC95 [{ci[0]:.1f} – {ci[1]:.1f}]  n={r['n']} ← phải 4463")
    print(f"  action_ok {aok:.1f}%   (S1 đạt 94,4%)")
except Exception:
 traceback.print_exc(); print("⚠️ ô đọc kết quả lỗi — KHÔNG sao, tệp thô vẫn được lưu")
print("\nmốc — trần 75,73 · S1/202 59,62 · S1/101 59,11 · S2/101 57,18 · Base 47,59 · sàn 12,0")
print("⛔ THĂM DÒ, MỘT HẠT GIỐNG — luật đọc ở report/106 mục (x8b). Cấm câu khẳng định về")
print("   phương pháp; chỉ được viết \"ở hạt giống duy nhất, … \".")
```

### Bước 4c — TRÌNH TỰ HAI COMMIT, chạy NỐI TIẾP chứ không song song

⭐ **HAI COMMIT GPU CHẠY SONG SONG ĐƯỢC — đo thật 25/8.** Hai notebook riêng (tách bằng
*Copy & Edit*), mỗi bản một nhánh, commit cách nhau ~20 phút, **cả hai cùng chạy**, đều nhận
2×T4. Trước đó tài liệu Kaggle chỉ nói phiên **tương tác** giới hạn 1 và không nói gì về commit;
câu "không nên chạy song song" ở bản runbook cũ là **suy đoán, đã bị chính phép thử này bác**.

⚠️ Nhưng cân nhắc cho đúng, song song **không** miễn phí về rủi ro:
· quota 30 giờ/tuần là **quota chung** ⇒ song song **không tiết kiệm giờ nào**, chỉ đổi 10,8 giờ
  **chờ** thành ~5,6 giờ chờ;
· lượt 1 hỏng vì lỗi cấu hình thì lượt 2 hỏng y hệt ⇒ chạy nối tiếp mất 5,4 giờ để biết mình sai,
  chạy song song mất 10,8 giờ cho **cùng một lỗi**.
⇒ Song song đáng khi ô 1b đã xanh hết và đang gấp deadline. Nối tiếp đáng khi lần đầu chạy một
  cấu hình mới. Ngày 25/8 chọn song song vì hạn nộp 30–31/8.

⛔ **Tách bằng hai NOTEBOOK riêng, đừng dùng hai version của cùng một notebook.** Hai notebook thì
chắc chắn là hai phiên; hai version của một notebook thì chưa ai thử.
⛔ **Bản sao thừa kế `TEN_COMMIT` của bản gốc** ⇒ rất dễ thành hai lượt cùng chấm một nhánh, ra
hai con số y hệt mà không có gì báo lỗi. Ô 1b dòng ③④ của **cả hai** bản phải khác nhau — kiểm
bằng cách dán cạnh nhau, đừng đọc từng cái một.

| | việc | mất bao lâu |
|---|---|---|
| 1 | Ô 1 để `TEN_COMMIT = ["min_desc_seed101"]` → chạy ô 0 · ô 1 · ô 1b → **Save & Run All** | bấm xong là xong |
| 2 | Đợi. Xem tab **Versions**, trạng thái *Running* → *Complete* | ~5,4 h |
| 3 | Panel **Output** → tải `score_min_desc_seed101.json` **và** `score_min_desc_seed101_raw.jsonl` về `runs/` | 1 phút |
| 4 | Mở lại notebook, sửa **một dòng** ở Ô 1 thành `["ce2_s2_seed101"]` → chạy lại ô 0 · ô 1 · ô 1b → **Save & Run All** | bấm xong là xong |
| 5 | Đợi, rồi tải hai tệp của CE2 về `runs/` | ~5,4 h |

⚠️ **Sửa notebook trong lúc commit đang chạy KHÔNG ảnh hưởng bản đang chạy** — Kaggle chụp lại
mã ở thời điểm bấm Commit rồi chạy bản chụp đó. Nhưng vẫn nên đợi xong hẵng sửa: để đúng một
trạng thái trong đầu, khỏi lẫn "bản đang chạy là nhánh nào".

⚠️ **Ô 1b là chốt chặn cuối.** Sửa `TEN_COMMIT` mà quên chạy lại Ô 1 thì biến trong nhân vẫn là
giá trị cũ ⇒ commit lượt 2 chấm lại **đúng nhánh của lượt 1**, ra số y hệt, và không có gì báo
lỗi. Ô 1b in dòng ④ chính là để bắt ca đó: đọc đường dẫn tệp preds, thấy đúng tên nhánh mới.

### Sau khi Commit

Chọn **Save Version → Save & Run All (Commit)**, **không** phải *Quick Save* — Quick Save chỉ
chụp trạng thái, không chạy gì. Rồi đóng trình duyệt, tắt máy thoải mái. Xem lại ở tab
**Versions**; xong thì tải tệp ở panel **Output**.

---

## Bước 5 — ô 3: đọc kết quả

```python
import json, os
# ⛔ KHOÁ ĐÚNG, đã đối chiếu tệp thật `runs/score_s2_seed101.json` do chính Kaggle sinh:
#    mode · preds · n · exec_voronoi · ci_voronoi · exec_disk · ci_disk · clusters · g_eff
#    KHÔNG có khoá `executability` lẫn `exec`. Bản trước của ô này hỏi hai khoá không tồn
#    tại, `.get()` trả None → `or 0` → in ra 0,00% và Δ −59,11 cho MỌI nhánh. Không lỗi,
#    không cảnh báo, bảng trông vẫn hoàn chỉnh — đúng kiểu hỏng đắt nhất của dự án này.
MOC = {"trần người": 75.73, "S1/202": 59.62, "S1/101": 59.11, "S2/101": 57.18, "Base": 47.59}
# ⛔ Ô này cũng đứng SAU ô 2 — không `assert`, không `raise`. Chỉ in.
print(f"{'nhánh':<18}{'n':>6}{'exec':>9}{'KTC95':>18}{'so S2/101':>11}{'so S1/101':>11}")
print("-" * 73)
for ten in TEN:
    f = f"{WS}/score_{ten}.json"
    if not os.path.exists(f):
        print(f"{ten:<18}  (chưa có tệp điểm — lượt này chưa chấm xong)"); continue
    d  = json.load(open(f, encoding="utf-8"))
    e  = d["exec_voronoi"] * 100
    ci = [c * 100 for c in d["ci_voronoi"]]
    print(f"{ten:<18}{d['n']:>6}{e:>8.2f}%   [{ci[0]:5.2f} – {ci[1]:5.2f}]"
          f"{e-57.18:>+11.2f}{e-59.11:>+11.2f}")
    # ⛔ IN CẢNH BÁO, TUYỆT ĐỐI KHÔNG `assert` Ở ĐÂY. Ô này chạy SAU 5,4 giờ chấm; một
    #    exception làm notebook kết thúc LỖI ⇒ Kaggle không lưu /kaggle/working ⇒ mất cả
    #    tệp thô. Mọi ô đứng sau ô 2 phải không-thể-ném-lỗi.
    if d["n"] != 4463:
        print(f"   ⛔ {ten}: n={d['n']} ≠ 4463 — mẫu số SAI, KHÔNG so được với các mốc dưới")
print("-" * 73)
for k, v in MOC.items(): print(f"  {k:<16}{v:>8.2f}%")
print("  sàn thước           12.00%")
print("\n⛔ THĂM DÒ, MỘT HẠT GIỐNG — report/106 mục (x8b). Cấm mọi câu khẳng định về phương pháp.")
```

### Luật đọc — đã khoá ở (x8b), đừng nới sau khi thấy số

| kết quả | được viết gì |
|---|---|
| bất kể cao thấp | *"Ở hạt giống duy nhất, MIN-DESC/101 đạt X% trên 4.463 bước. **Thăm dò, một hạt giống.**"* |
| ⛔ cấm | *"MIN-DESC làm model tốt hơn"* · *"mục tiêu ưu tiên có tác dụng"* · mọi câu khẳng định về **phương pháp** |

Muốn nói được câu khẳng định thì phải có hạt giống 202 cho **cả hai** nhánh, và khai rằng nó
được chạy **sau khi** đã thấy điểm hạt thứ nhất — cam kết ở **(x8c)**.

---

## Bước 6 — tải về máy nhà

Tải `score_min_desc_seed101.json`, `score_ce2_s2_seed101.json` và **cả hai `*_raw.jsonl`**
về `runs/`.

⭐ **Tệp thô là tài sản.** Giữ `*_raw.jsonl` thì đổi luật chấm hay thêm lát cắt vẫn tính lại được
**không gọi lại bộ trỏ** — đã tiết kiệm trọn một lượt 5,6 giờ khi chấm lại `p3_nopos_v2`.

⚠️ Đặt thẳng vào `runs/`, đúng luật ở `runs/README.md`. Đã có lần bốn tệp lạc vào `report/papers/`,
mất một lượt dọn.
