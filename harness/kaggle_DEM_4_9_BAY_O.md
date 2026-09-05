# Kaggle đêm 4/9 — BẢY Ô DÁN TUẦN TỰ

Sinh tự động từ `kaggle_commit_sel_4_9.md` bằng `harness/make_7o.py`. **Đừng sửa tay tệp này** —
sửa runbook gốc rồi chạy lại lệnh sinh, nếu không hai bản sẽ lệch nhau.

Dán đúng bảy ô dưới đây, theo đúng thứ tự, mỗi khối một ô notebook. Không thêm ô nào khác.
Ô probe 3 bước là ô chạy TAY một lần trước khi commit, **không** đưa vào notebook đem commit.

Trước khi bấm: Accelerator **GPU T4 x2** · Internet **On** · ba input đã gắn
(`thesis-sel-infer` bản mới nhất · `thesis-score` · `gui-sel-adapter`).

Bấm **Save Version → Save & Run All (Commit)**.

---

## Ô 1 — cài gói và GỠ torchao

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

## Ô 2 — dựng workspace, kiểm hai hash

```python
import os, glob, json, shutil, subprocess
WS = "/kaggle/working/ws"; os.makedirs(WS, exist_ok=True)

# ⛔ BÀI HỌC 5/9: "New Version" của Kaggle THÊM thư mục chứ không thay thế, nên trong
#    /kaggle/input tồn tại song song mọi gói đã upload (kaggle_sel_4_9, kaggle_sel_5_9, …).
#    Dấu vân tay phải là chuỗi CHỈ có trong bản MỚI NHẤT, nếu không nhiều bản cùng đạt và
#    `ok[0]` lấy phải bản cũ — im lặng, không lỗi. Đã mất một lượt probe vì đúng chuyện này.
#    ⇒ Mỗi lần vá mã thì ĐỔI hai dòng dưới, và giữ assert "đúng một bản".
CAN_FILE = "seq_score_sel.py"
CAN = "ĐỆM CỦA QWEN NẰM BÊN PHẢI"                  # dấu vân tay bản 5/9 lượt 2 (vá đệm phải)
src = glob.glob(f"/kaggle/input/**/harness/{CAN_FILE}", recursive=True)
assert src, f"DỪNG: chưa thấy harness/{CAN_FILE} trong /kaggle/input"
ok = []
for q in src:
    co = CAN in open(q, encoding="utf-8", errors="ignore").read()
    print(("  ✅ bản mới" if co else "  ⛔ bản cũ"), q)
    if co: ok.append(q)
assert ok, ("DỪNG: không bản nào chứa bản vá mới nhất. Dataset chưa lên version mới, hoặc "
            "panel Input còn trỏ version cũ.")
assert len(ok) == 1, (f"DỪNG: {len(ok)} bản cùng đạt dấu vân tay — không biết lấy bản nào.\n"
                      f"   {ok}\n"
                      f"   Đổi CAN thành chuỗi chỉ có trong bản mới nhất.")
PKG = os.path.dirname(ok[0])
GOI = os.path.dirname(PKG)          # gốc gói, để lấy runs/sel/... của ĐÚNG gói này
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

## Ô 3 — hàm chạy-và-chờ

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

## Ô 4 — tiền bay + dựng danh sách 3.063 bước

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

## Ô 5 — suy luận 3.063 bước (~4 h)

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

## Ô 6 — soi tệp pred

```python
import json, collections
rs = [json.loads(l) for l in open(OUT, encoding="utf-8")]
print("① số bản ghi      :", len(rs), "← cần 3.063")
print("② chữ ký lượt chạy:", collections.Counter(r.get("run") for r in rs).most_common())
print("③ có thẻ <sel>    :", sum(1 for r in rs if "<sel>" in (r.get("raw") or "")), "/", len(rs))
print("④ pred rỗng       :", sum(1 for r in rs if not (r.get("pred") or "").strip()))
```

## Ô 7 — gộp 4.463 + cổng giờ + chấm exec (~5,6 h)

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

---

## Sáng dậy — tab Output phải có bốn tệp

| tệp | nghĩa |
|---|---|
| `preds_gui_sel_seed101_rest3063.jsonl` | 3.063 câu sinh mới |
| `preds_gui_sel_seed101_touch4463.jsonl` | gộp với lát dev, đủ mẫu số |
| `score_gui_sel_seed101.json` | **số exec** |
| `score_gui_sel_seed101_raw.jsonl` | tệp thô, giữ bằng mọi giá |

Thiếu hai tệp cuối nghĩa là cổng giờ đã cắt phần chấm. Đọc dòng `⛔ BỎ phần chấm` trong đầu ra
của ô 7, rồi chấm `exec` bằng mục **C2** của runbook gốc thành một commit riêng — tệp gộp 4.463
đã có sẵn nên commit đó chỉ còn đúng một việc.

Tải về đặt thẳng vào `runs/sel/`, đừng để lạc sang thư mục khác.
