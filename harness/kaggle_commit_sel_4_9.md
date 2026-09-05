# Kaggle — chạy dạng COMMIT (Save Version), gập máy đi ngủ được (4/9/2026)

Runbook `kaggle_infer_sel.md` viết cho **chạy tương tác**: nó có ô theo dõi vòng lặp, và ô đó
chỉ có nghĩa khi có người ngồi nhìn. Tệp này thay phần vận hành cho **commit**, giữ nguyên mọi
phép kiểm nội dung của bản cũ.

---

## §0 — ĐÊM 4/9: MỘT commit làm cả C1 và C2

Gộp được vì tổng ước **9,6 h < 12 h**, và gộp thì **khỏi phải nối output C1 sang C2** — cả hai
đọc ghi chung `/kaggle/working` trong cùng một lần chạy. Đổi lại phải có **cổng thời gian**:
xong C1 mà đã tiêu quá 5,5 h thì **bỏ C2**, để notebook kết thúc bình thường và Kaggle vẫn lưu
tệp pred. Chạy quá 12 h là bị giết giữa chừng và **mất trắng** `/kaggle/working`.

**Thứ tự dán ô, đúng bảy ô:**

| ô | lấy từ mục | việc |
|---|---|---|
| 1 | *Ô chung 0 — cài gói* | cài `peft`, `accelerate` |
| 2 | *Ô chung 1 — dựng workspace* | chọn đúng bản mã 4/9, symlink ảnh, **kiểm hai hash** |
| 3 | *Ô chung 2 — hàm chạy-và-chờ* | định nghĩa `chay_va_cho` |
| 4 | *C1*, ô đầu | tiền bay + dựng `only_rest3063.jsonl`, chốt **3.063** |
| 5 | *C1*, ô hai | suy luận 3.063 bước (~4 h) |
| 6 | *C1*, ô ba | soi tệp pred |
| 7 | **§0.1 dưới đây** | cổng giờ + gộp 4.463 + `exec` + soi |

⛔ **Ô 4b (probe 3 bước) KHÔNG dán vào notebook đem commit.** Nó là ô chạy tay, một lần, trước
khi bấm Save Version. Để lại trong notebook thì mỗi lần commit tốn thêm ~5 phút nạp mô hình vô
ích — mỗi ô gọi một tiến trình riêng nên mô hình nền được nạp lại từ đầu ở từng ô.

⛔ **Ô gỡ `torchao` phải nằm TRONG ô 1**, không phải một ô riêng đặt sau. Commit chạy lại toàn bộ
notebook trong máy ảo sạch: `pip -U peft` ở ô 1 lại kéo về peft 0.20.0, nên nếu lệnh gỡ đứng sau
ô workspace thì ô suy luận vẫn chết đúng như lần đầu.

⚠️ Ô 7 thay cho toàn bộ mục C2 khi chạy gộp. Mục C2 nguyên bản chỉ dùng nếu về sau phải chạy
`exec` thành một commit riêng.

### §0.1 — ô cuối: cổng giờ, gộp, chấm

```python
import time, json, collections, os, glob

# ── Gộp trước, bất kể còn giờ hay không: tốn vài giây, không đụng GPU, và nếu cổng giờ
#    cắt phần chấm thì commit sau đã có sẵn tệp 4.463 để chấm thẳng.
p_dev = glob.glob("/kaggle/input/**/preds_gui_sel_seed101_dev1400.jsonl", recursive=True)[0]
FULL = "/kaggle/working/preds_gui_sel_seed101_touch4463.jsonl"
with open(FULL, "w", encoding="utf-8") as o:
    for p in (p_dev, OUT):                     # OUT = tệp 3.063 của ô 5
        for line in open(p, encoding="utf-8"):
            o.write(line)

rs = [json.loads(l) for l in open(FULL, encoding="utf-8")]
kh = [(str(r["episode_id"]), str(r["step_id"])) for r in rs]
print("gộp:", len(rs), "bản ghi ← cần 4.463 · khoá trùng:", len(kh) - len(set(kh)))
print("chữ ký:", collections.Counter(r.get("run") for r in rs).most_common())
assert len(rs) == 4463 and len(kh) == len(set(kh)), "DỪNG: tệp gộp không đúng"

GIO_DA_TIEU = (time.time() - T_BAT_DAU) / 3600
print(f"đã tiêu {GIO_DA_TIEU:.2f} h cho phần suy luận")

if GIO_DA_TIEU > 5.5:
    print("⛔ BỎ phần chấm: quá 5,5 h nên không đủ đệm dưới trần 12 h của Kaggle. "
          "Hai tệp pred vẫn được lưu; chấm exec ở commit sau bằng mục C2 của runbook.")
else:
    OUTJ = "/kaggle/working/score_gui_sel_seed101.json"
    RAW  = "/kaggle/working/score_gui_sel_seed101_raw.jsonl"
    chay_va_cho(
        ["python", f"{WS}/harness/score_run.py",
         "--mode", "score", "--grounder", "uground",
         "--preds", FULL, "--out", OUTJ],
        log="/kaggle/working/c2_score.log", dich=RAW, can=4463)
    print(json.dumps(json.load(open(OUTJ)), ensure_ascii=False, indent=2)[:1200])
```

⚠️ Ô 5 đã có sẵn `T_BAT_DAU = time.time()` ngay trước lời gọi `chay_va_cho`, và đặt tên biến
`OUT` cho tệp 3.063 — ô 7 đọc lại hai tên đó, đừng đổi.

---

**Ba lượt, ba commit tách rời.** Đừng gộp: Kaggle giết session GPU ở **12 giờ**, commit vượt giờ
là **mất trắng `/kaggle/working`**, không có bản cứu.

| commit | việc | giờ ước | ra tệp |
|---|---|---|---|
| **C1** | suy luận 3.063 bước còn lại | ~4 h | `preds_gui_sel_seed101_rest3063.jsonl` |
| **C2** | `exec` trên đủ 4.463 bước | ~5,6 h | `score_gui_sel_seed101_raw.jsonl` + `.json` |
| **C3** | sequence-score lát dev 1.400 | <1 h nếu `--cache-prompt` chạy được, ~4,7 h nếu không | `seqscores_gui_sel_seed101_dev1400.jsonl` |

Quota 30 h/tuần: ba lượt cộng lại ~10–14 h, còn dư cho một lần chạy lại.

---

## Bảy khác biệt so với chạy tương tác — đọc hết trước khi bấm Save Version

1. **Commit chạy lại TOÀN BỘ notebook từ ô đầu**, trong một máy ảo sạch. Mọi ô phải chạy được
   khi không có gì sẵn trong `/kaggle/working`. Đừng để ô nào phụ thuộc thứ bạn đã gõ tay lúc
   chạy tương tác.
2. **Không có ô theo dõi.** Thay bằng vòng chờ ngay trong ô chạy: `Popen` rồi vừa chờ vừa in
   một dòng mỗi 2 phút. Không được `Popen` xong để ô kết thúc — commit sẽ đi tiếp sang ô sau
   trong khi tiến trình còn dở, rồi kết thúc notebook và **giết tiến trình**.
3. **`TQDM_DISABLE=1` vẫn bắt buộc**, và commit còn nhạy hơn tương tác: log ngập thì tiến trình
   kẹt ở lệnh ghi stdout, đã treo 7 giờ vì đúng chuyện này.
4. **Internet ON** (tải mô hình nền) và **Accelerator T4×2**. Kiểm lại trong panel trước khi bấm,
   commit chạy bằng cấu hình đang lưu của notebook chứ không phải cấu hình phiên đang mở.
5. **Nối hai commit bằng Output, không bằng `/kaggle/working`.** `/kaggle/working` của commit
   trước **không** tự có ở commit sau. C2 phải gắn output của C1 làm input: *Add Data ▸ Your
   Notebooks ▸ chọn version của C1*.
6. **Tệp ra phải nằm thẳng trong `/kaggle/working`** mới lên tab Output. Ghi vào thư mục con
   cũng được nhưng nhớ đường dẫn khi gắn lại ở commit sau.
7. **Dataset mã phải lên version mới trước khi chạy.** Bản `infer_branch.py` trong dataset hiện
   tại **chưa có bản vá fail-closed 4/9**, và **chưa có `seq_score_sel.py`**. Chạy bằng bản cũ
   thì không lỗi, không cảnh báo, chỉ là kết quả của một hệ thống khác — đúng bẫy đã trả giá
   ngày 20/8.

---

## Ô chung 0 — cài gói

```python
!pip -q install -U accelerate peft qwen-vl-utils 2>&1 | tail -2
# ⛔ GỠ torchao — bắt buộc, đo 4/9: `pip -U peft` kéo về peft 0.20.0, mà image Kaggle có
#    torchao 0.10.0. peft 0.20 gọi is_torchao_available() trong lúc dựng lớp LoRA, và hàm
#    đó RAISE ImportError khi thấy torchao dưới 0.16 thay vì trả False. Kết quả:
#    PeftModel.from_pretrained chết NGAY SAU KHI đã nạp xong mô hình nền.
#    Script không dùng torchao ở đâu cả; vắng mặt thì hàm kia trả False và mọi thứ chạy.
!pip -q uninstall -y torchao 2>&1 | tail -1
import importlib.util
print("torchao còn không:", importlib.util.find_spec("torchao") is not None, "← phải là False")

import torch, transformers, peft
print(transformers.__version__, peft.__version__, torch.cuda.get_device_name(0))
```

`| tail -2` là bắt buộc: `pip` in hàng trăm dòng, và log ngập là tiến trình kẹt.
Dòng in ra phải có tên card (`Tesla T4`); không có nghĩa là notebook đang chạy CPU, dừng lại
và sửa Accelerator trước khi làm tiếp.

---

## Ô chung 1 — dựng workspace (dán y hệt vào cả ba notebook)

Khác bản cũ đúng một chỗ: **dấu vân tay `CAN`**. Bản cũ tìm `--force-sel`, mà chuỗi đó có cả
trong bản mã cũ ngày 3/9. Bản này tìm chuỗi chỉ có trong bản vá 4/9.

```python
import os, glob, json, shutil, subprocess
WS = "/kaggle/working/ws"; os.makedirs(WS, exist_ok=True)

# dấu vân tay của bản mã 4/9 — có trong thông báo fail-closed của infer_branch.py
CAN = "fail-closed ĐẠT"
src = glob.glob("/kaggle/input/**/harness/infer_branch.py", recursive=True)
assert src, "DỪNG: chưa thấy harness/infer_branch.py trong /kaggle/input"
ok = []
for q in src:
    co = CAN in open(q, encoding="utf-8", errors="ignore").read()
    print(("  ✅ bản 4/9" if co else "  ⛔ bản cũ"), q)
    if co: ok.append(q)
assert ok, ("DỪNG: không bản nào chứa bản vá 4/9. Dataset chưa lên version mới, hoặc "
            "panel Input còn trỏ version cũ.")
PKG = os.path.dirname(ok[0])
shutil.rmtree(f"{WS}/harness", ignore_errors=True)
shutil.copytree(PKG, f"{WS}/harness")
assert os.path.isfile(f"{WS}/harness/seq_score_sel.py"), \
    "DỪNG: dataset thiếu seq_score_sel.py — upload lại version mới"
# bản vá OOM ngày 5/9: bản trước gọi .float() trên CẢ bảng logits và tràn T4 ở lô 8 span
assert "KHÔNG gọi .float() trên CẢ bảng logits" in open(
    f"{WS}/harness/seq_score_sel.py", encoding="utf-8").read(), \
    "DỪNG: seq_score_sel.py là bản TRƯỚC 5/9, sẽ tràn bộ nhớ ở đường chậm. Upload version mới."

# ảnh: symlink, không chép
best = None
for t in glob.glob("/kaggle/input/**/test_ac/images", recursive=True):
    n = len(glob.glob(os.path.join(t, "*.png")))
    print(f"  {n:5d} ảnh  {t}")
    if n >= 4400 and (best is None or n > best[1]): best = (t, n)
assert best, "DỪNG: không gói nào đủ ảnh"
dst = f"{WS}/harness/dg1_cache/test_ac/images"
if os.path.islink(dst): os.remove(dst)
elif os.path.isdir(dst): shutil.rmtree(dst)
os.symlink(best[0], dst)

AD = os.path.dirname(glob.glob("/kaggle/input/**/adapter_config.json", recursive=True)[0])
print("adapter:", AD)

# ⛔ CHỮ KÝ LƯỢT CHẠY LẤY THEO TÊN THƯ MỤC ADAPTER (infer_branch.py: sig = "lora:" +
#    basename(adapter)). Lát dev 1.400 đã sinh với chữ ký "lora:gui-sel-adapter". Đổi tên
#    thư mục là đổi chữ ký, và ô gộp 4.463 sẽ thấy HAI chữ ký rồi dừng — sau khi đã tiêu
#    4 giờ suy luận. Dùng lại đúng dataset adapter cũ, đừng upload bản mới đặt tên khác.
assert os.path.basename(AD) == "gui-sel-adapter", (
    f"DỪNG: thư mục adapter tên {os.path.basename(AD)!r}, phải là 'gui-sel-adapter' để "
    f"chữ ký trùng lát dev 1.400. Gắn lại dataset adapter cũ.")

# ⛔ artifact phải đúng bản đã pin — đối chiếu runs/sel/manifest_selA_selB_4_9.json
import hashlib
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
MONG = {
  "candidates.jsonl": "f10b69411a28e4a9b78aa309241d4a68440e8c463072788c541e887e2e1914f8",
  "adapter_model.safetensors": "8b6184798527d3fa4de76b9d2fe3b18005436de07bd51890d71bcb838dc82dfb",
}
for n, want in MONG.items():
    p = (f"{WS}/harness/dg1_cache/test_ac/{n}" if n.endswith("candidates.jsonl")
         else f"{AD}/{n}")
    got = sha(p)
    print(("OK  " if got == want else "LỆCH"), n, got[:16], "…")
    assert got == want, f"DỪNG: {n} không phải bản đã pin"
```

---

## Ô chung 2 — hàm chạy-và-chờ, dùng cho cả ba commit

```python
import subprocess, os, time

def chay_va_cho(cmd, log, dich=None, can=None, nhip=120):
    """Chạy tiến trình con, CHỜ tới khi xong, in một dòng mỗi `nhip` giây.

    Vì sao phải chờ ngay trong ô: commit chạy tuần tự và kết thúc notebook khi hết ô.
    Popen rồi để ô kết thúc là notebook đi tiếp rồi tắt máy ảo, giết luôn tiến trình.
    Vì sao vẫn phải in định kỳ: commit hỏng thì thứ duy nhất còn lại để chẩn là log.
    """
    env = {**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1",
           "HF_HUB_DISABLE_PROGRESS_BARS": "1"}
    f = open(log, "a")
    P = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT,
                         start_new_session=True, env=env, cwd=WS)
    t0 = time.time()
    while P.poll() is None:
        time.sleep(nhip)
        n = sum(1 for _ in open(dich)) if dich and os.path.exists(dich) else -1
        gio = (time.time() - t0) / 3600
        eta = (gio * (can - n) / n) if (can and n > 0) else float("nan")
        print(f"{time.strftime('%H:%M:%S')} · {gio:5.2f} h · "
              f"{n}/{can if can else '?'} · còn ~{eta:.1f} h", flush=True)
    print("mã thoát:", P.returncode, flush=True)
    print("--- 25 dòng log cuối ---", flush=True)
    print(subprocess.run(["tail", "-25", log], capture_output=True, text=True).stdout)
    assert P.returncode == 0, "DỪNG: tiến trình thoát khác 0 — đọc log ở trên"
```

`HF_HUB_DISABLE_PROGRESS_BARS` là chỗ bản cũ còn hở: `TQDM_DISABLE` không chặn thanh tiến trình
của khâu tải mô hình nền, mà commit nào cũng tải lại từ đầu vì máy ảo sạch.

---

## C1 — suy luận 3.063 bước còn lại

`--only` nhận danh sách bước **cần sinh**. Lát dev 1.400 đã có rồi, nên ô này dựng danh sách phần
bù ngay trong notebook thay vì mang thêm một tệp qua dataset.

```python
import json, ast
R = f"{WS}/harness/dg1_cache/test_ac"
recs = [json.loads(l) for l in open(f"{R}/test.jsonl", encoding="utf-8")]
dev = glob.glob("/kaggle/input/**/preds_gui_sel_seed101_dev1400.jsonl", recursive=True)
assert dev, "DỪNG: chưa gắn tệp pred lát dev vào Input"
xong = {(str(json.loads(l)["episode_id"]), str(json.loads(l)["step_id"]))
        for l in open(dev[0], encoding="utf-8")}

def la_cham(r):
    a = r["action"] if isinstance(r["action"], dict) else ast.literal_eval(str(r["action"]))
    return a.get("action_type") in ("click", "long_press") and "x" in a

con = [r for r in recs if la_cham(r) and (str(r["episode_id"]), str(r["step_id"])) not in xong]
print("bước chạm toàn tập:", sum(1 for r in recs if la_cham(r)), "← cần 4.463")
print("đã có (dev)       :", len(xong), "← cần 1.400")
print("còn phải sinh     :", len(con), "← cần 3.063")
assert len(con) == 3063, "DỪNG: phần bù không ra 3.063 — nghi lệch tệp test hoặc tệp dev"

with open("/kaggle/working/only_rest3063.jsonl", "w", encoding="utf-8") as f:
    for r in con:
        f.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"]}) + "\n")
```

### Ô 4b — PROBE 3 BƯỚC, chạy TAY trước khi bấm Save Version (⛔ không dán vào notebook commit)

Ô tiền bay ở trên không nạp mô hình, nên nó **không** bắt được lỗi ở khâu nạp adapter — đúng
chỗ hỏng ngày 4/9 (torchao). Ô này nạp mô hình thật và sinh 3 câu, mất khoảng 5 phút, chặn
đúng loại lỗi "chết sau khi đã nạp xong mô hình".

```python
chay_va_cho(
    ["python", f"{WS}/harness/infer_branch.py",
     "--adapter", AD,
     "--out", "/kaggle/working/probe3.jsonl",
     "--cands", f"{WS}/harness/dg1_cache/test_ac/candidates.jsonl",
     "--only", "/kaggle/working/only_rest3063.jsonl",
     "--limit", "3"],
    log="/kaggle/working/probe3.log", dich="/kaggle/working/probe3.jsonl", can=3, nhip=30)

import json
for r in map(json.loads, open("/kaggle/working/probe3.jsonl", encoding="utf-8")):
    print(r["episode_id"], r["step_id"], "|", (r.get("raw") or "")[:90].replace("\n", " / "))
```

Ba bản ghi phải có thẻ `<sel>` và một câu tiếng Anh phía sau. Xong thì dọn tệp probe:

```python
import os, glob
for p in glob.glob("/kaggle/working/probe*"):
    os.remove(p); print("xoá", p)
print("đã dọn tệp probe")
```

---

```python
import time
T_BAT_DAU = time.time()          # ô cuối đọc lại biến này để tính cổng giờ
OUT = "/kaggle/working/preds_gui_sel_seed101_rest3063.jsonl"
chay_va_cho(
    ["python", f"{WS}/harness/infer_branch.py",
     "--adapter", AD,
     "--out", OUT,
     "--cands", f"{WS}/harness/dg1_cache/test_ac/candidates.jsonl",
     "--only", "/kaggle/working/only_rest3063.jsonl"],
    log="/kaggle/working/c1_infer.log", dich=OUT, can=3063)
```

Ô cuối của C1 — soi tệp trước khi tin:

```python
import json, collections
rs = [json.loads(l) for l in open(OUT, encoding="utf-8")]
print("① số bản ghi      :", len(rs), "← cần 3.063")
print("② chữ ký lượt chạy:", collections.Counter(r.get("run") for r in rs).most_common())
print("③ có thẻ <sel>    :", sum(1 for r in rs if "<sel>" in (r.get("raw") or "")), "/", len(rs))
print("④ pred rỗng       :", sum(1 for r in rs if not (r.get("pred") or "").strip()))
```

⛔ Dòng ② phải ra **đúng một** chữ ký. Hai chữ ký nghĩa là tệp trộn hai lượt chạy.

---

## C2 — `exec` trên đủ 4.463 bước

Gắn output của C1 làm input, rồi nối hai tệp pred lại.

```python
import glob, shutil
p_dev = glob.glob("/kaggle/input/**/preds_gui_sel_seed101_dev1400.jsonl", recursive=True)[0]
p_res = glob.glob("/kaggle/input/**/preds_gui_sel_seed101_rest3063.jsonl", recursive=True)[0]
FULL = "/kaggle/working/preds_gui_sel_seed101_touch4463.jsonl"
with open(FULL, "w", encoding="utf-8") as o:
    for p in (p_dev, p_res):
        shutil.copyfileobj(open(p, encoding="utf-8"), o)

import json, collections
rs = [json.loads(l) for l in open(FULL, encoding="utf-8")]
kh = [(r["episode_id"], r["step_id"]) for r in rs]
print("số bản ghi:", len(rs), "← cần 4.463")
print("khoá trùng:", len(kh) - len(set(kh)), "← cần 0")
print("chữ ký    :", collections.Counter(r.get("run") for r in rs).most_common())
assert len(rs) == 4463 and len(kh) == len(set(kh)), "DỪNG: tệp gộp không đúng"
```

```python
OUTJ = "/kaggle/working/score_gui_sel_seed101.json"
RAW  = "/kaggle/working/score_gui_sel_seed101_raw.jsonl"   # score_run TỰ đặt tên này
chay_va_cho(
    ["python", f"{WS}/harness/score_run.py",
     "--mode", "score", "--grounder", "uground",
     "--preds", FULL,
     "--out", OUTJ],
    log="/kaggle/working/c2_score.log", dich=RAW, can=4463)
```

⚠️ `score_run.py` **không có cờ `--raw`**. Nó tự suy tên tệp thô từ `--out`: bỏ đuôi rồi thêm
`_raw.jsonl` (`score_run.py:476`). Nên `--out .../score_gui_sel_seed101.json` sinh ra
`.../score_gui_sel_seed101_raw.jsonl`. Cờ đầy đủ: `--mode {gate,score,noharm}` ·
`--grounder {uground,openai,uivenus}` · `--preds` · `--out` · `--n`.
`score_run` **nối tiếp được** từ tệp thô, và nó tự dừng nếu tệp thô là của nhánh khác.

⛔ **Giữ `score_*_raw.jsonl`.** Có tệp thô thì đổi luật chấm hay tính hàng nL2 về sau **không
phải gọi lại bộ trỏ** — đã cứu trọn một lượt 5,6 giờ hồi tháng 8.

---

## C3 — sequence-score lát dev 1.400

**Chạy `--probe 50` trước trong một commit riêng, hoặc chạy probe trên CPU máy nhà** (xem
`colab_keo_adapter_4_9.md`). Con số cần lấy từ probe là **giây mỗi bước**; nhân 1.400 rồi so với
trần 12 giờ trước khi phóng lượt dài.

Trước hết kiểm API bộ nhớ đệm của đúng bản `transformers` trên máy đó — Kaggle đang chạy 5.0.0
còn máy nhà 5.14.1, và `--cache-prompt` phụ thuộc `DynamicCache.crop`:

```python
from transformers import DynamicCache
import transformers
c = DynamicCache()
print("transformers", transformers.__version__,
      "| crop:", hasattr(c, "crop"), "| get_seq_length:", hasattr(c, "get_seq_length"))
```

Cả hai phải `True`. Nếu `crop` là `False` thì bỏ cờ `--cache-prompt` ở hai ô dưới; script cũng
tự dừng và báo, nhưng biết trước thì khỏi mất một lượt.

**Probe 50 bước — bắt buộc, lấy giây/bước thật:**

```python
chay_va_cho(
    ["python", f"{WS}/harness/seq_score_sel.py",
     "--adapter", AD,
     "--cands", f"{WS}/harness/dg1_cache/test_ac/candidates.jsonl",
     "--only", glob.glob("/kaggle/input/**/preds_gui_sel_seed101_dev1400.jsonl",
                         recursive=True)[0],
     "--out", "/kaggle/working/probe50_seqscore.jsonl",
     "--cache-prompt", "--probe", "50"],
    log="/kaggle/working/probe50.log", dich="/kaggle/working/probe50_seqscore.jsonl",
    can=50, nhip=60)

import json
rs = [json.loads(l) for l in open("/kaggle/working/probe50_seqscore.jsonl", encoding="utf-8")]
tok = {r["tok_none"] for r in rs}
print("số bước           :", len(rs))
print("tok_none (phải là MỘT giá trị):", tok)
print("s_none  trung bình:", sum(r["s_none"] for r in rs) / len(rs))
print("s_star  trung bình:", sum(r["s_star"] for r in rs) / len(rs))
print("margin  trung bình:", sum(r["margin"] for r in rs if r["margin"] is not None) / len(rs))
print("n_cand  trung bình:", sum(r["n_cand"] for r in rs) / len(rs))
print("có ứng viên vàng  :", sum(r["gold_in_menu"] for r in rs), "/", len(rs))
```

Bốn thứ phải đúng trước khi phóng lượt dài: ba dòng `kiểm chéo nhanh↔chậm` đều dưới `1e-3` ·
`tok_none` chỉ có **một** giá trị · `s_none` và `s_star` đều **âm và cùng cỡ** · giây mỗi bước
nhân 1.400 phải dưới 12 giờ. Xong thì xoá tệp probe.

**Lượt dài:**

```python
OUT = "/kaggle/working/seqscores_gui_sel_seed101_dev1400.jsonl"
p_dev = glob.glob("/kaggle/input/**/preds_gui_sel_seed101_dev1400.jsonl", recursive=True)[0]
chay_va_cho(
    ["python", f"{WS}/harness/seq_score_sel.py",
     "--adapter", AD,
     "--cands", f"{WS}/harness/dg1_cache/test_ac/candidates.jsonl",
     "--only", p_dev,
     "--out", OUT,
     "--cache-prompt"],
    log="/kaggle/working/c3_seqscore.log", dich=OUT, can=1400)
```

Ba dòng phải có trong log, theo thứ tự:

1. `kiểm chéo nhanh↔chậm: lệch tối đa ...` — ba lần, mỗi lần dưới `1e-3`. Script tự dừng nếu
   vượt; **đừng nới ngưỡng**.
2. `khối ứng viên: phủ 1400/1400 bước — fail-closed ĐẠT`.
3. Dòng tiến độ mỗi 20 bước, giây mỗi bước không nhảy vọt.

⛔ **Tệp này chỉ sinh điểm.** Quét τ là việc riêng, chạy trên máy nhà, **0 GPU**, theo đúng thủ
tục đã đăng ký ở `report/106` mục **(x16d)**. Và khoá τ **trước khi** nhìn `exec` của nhánh đối
chứng hoặc phần 3.062 bước.

---

## Trước khi bấm Save Version — sáu dòng phải xanh

1. Accelerator **GPU T4×2**, Internet **ON**.
2. Ba input đã gắn, và **version mới nhất** của dataset mã (có bản vá 4/9 + `seq_score_sel.py`).
3. Commit trước đã gắn làm input nếu lượt này cần (C2 cần C1; C3 cần lát dev).
4. Ô workspace chạy hết mà không `assert` nào nổ — hai hash phải in `OK`.
5. Giờ ước của lượt này **dưới 12 giờ**, có đệm.
6. Quota tuần còn đủ. Mỗi lần chạy lại là mất trọn số giờ của lượt hỏng.

Commit xong thì tệp nằm ở tab **Output** của version đó. Tải về **đặt thẳng vào thư mục của phép
đo** — `runs/sel/` — theo đúng luật đọc kết quả ở `runs/README.md`. Đã có lần bốn tệp lạc chỗ và
mất một lượt dọn.
