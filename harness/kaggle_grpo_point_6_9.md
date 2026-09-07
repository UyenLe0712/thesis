# Kaggle — suy luận + chấm `exec` nhánh GRPO `<point>`/101 (viết 6/9/2026)

Máy: **T4×2 miễn phí**, hạn mức 30 giờ GPU/tuần, **0 đồng**. Thay cho ô G7 của
`harness/colab_grpo_point.md` (bản đó chạy trên A100 trả tiền).

| commit | việc | ước thời gian | ra tệp |
|---|---|---|---|
| **C1** | suy luận **4.463 bước chạm** | ~3–5 h | `preds_grpo_point_seed101.jsonl` |
| **C2** | `exec` UGround trên đúng 4.463 bước | ~5,4 h (đo thật 0,23 bước/giây) | `score_grpo_point_seed101{_raw,}.jsonl/.json` |

Tách hai commit, đừng gộp: mỗi cái xa trần 12 h, và C1 hỏng thì không mất luôn C2.
Tổng ~8,4 h trong hạn mức 30 h/tuần.

---

## ⛔ Lệch phạm vi so với (x19e), phải khai chứ đừng lặng lẽ

(x19e) khoá *"suy luận greedy trên 6.958 bước rồi chấm trên đúng 4.463 bước chạm"*. Lượt này
chỉ sinh **4.463 bước chạm**, vì dataset `thesis-score` chỉ có 4.463 ảnh và ảnh của 2.495 bước
không chạm nằm trong `test_images.tar` trên Drive.

· **Không đổi con số headline.** `history` trong câu nhắc là **câu chuẩn của người**, không phải
  dự đoán của mô hình (trùng nguyên văn 5.318/5.318), nên mỗi bước sinh độc lập. Tập 4.463 bước
  chạm cho kết quả y hệt như khi cắt ra từ lượt 6.958.
· **Cái mất:** không có preds ở **bước không chạm** ⇒ lượt này **không đo được** GRPO có làm hỏng
  nhóm đó không. Rủi ro thật, vì tập thưởng chỉ gồm bước chạm — MIN-DESC từng lộ giá **−19,75**
  đúng ở nhóm này (luận văn §`sec:khongcham`).
· ⇒ Ghi vào `report/106` mục **(x19d) ghi 3** trước khi chạy, và khai trong mọi chỗ báo kết quả.
  Muốn bù thì upload `test_images.tar` thành một dataset nữa rồi chạy lát 2.495 bước còn lại
  (~1,7 h) — đó là **lượt thêm**, không phải điều kiện của headline.

---

## Ba Input

| dataset | có gì | ghi chú |
|---|---|---|
| `thesis-score` | 4.463 ảnh tập kiểm + `test.jsonl` | đã có sẵn |
| `thesis-sel-infer` | gói mã (`harness/`) | đã có sẵn — lượt này **không** dùng `--cands` |
| `grpo-point-adapter` | `adapter_model.safetensors` + `adapter_config.json` | **tạo mới**, ~60 MB |

⛔ **Upload đúng HAI tệp ở gốc `final/`, đừng kéo cả thư mục.** Trong `final/` có thư mục con
**`ref/`** — bản sao adapter MIN dùng làm tham chiếu KL lúc train. Nếu `ref/adapter_config.json`
cũng lên dataset thì ô dò adapter có thể bắt phải nó và **chấm nhầm MIN, không lỗi không cảnh
báo** — đúng dạng lỗi câm đã trả giá 20/8.

Settings: **Accelerator GPU T4×2** · **Internet ON** (tải Qwen2.5-VL-3B từ HuggingFace).

---

## Ô chung 0 — GỠ `torchao` (⛔ ô ĐẦU TIÊN của mọi commit, kể cả C2)

Kaggle cài sẵn `torchao 0.10.0`, còn bản `peft` ở đây đòi > 0.16 **và ném `ImportError` ngay khi
phát hiện bản cũ**, đúng lúc gắn LoRA — tức **sau** khi đã tải xong mô hình nền. Dự án không dùng
torchao lần nào (lượng tử hoá là bitsandbytes). Gỡ, đừng nâng: nâng sẽ kéo theo torch và phá bản
CUDA của máy.

```python
!pip uninstall -y -q torchao
!python -c "import importlib.util; print('torchao còn:', importlib.util.find_spec('torchao'))"
```

**Kiểm:** in ra `torchao còn: None`.

⚠️ **Phải nằm trong notebook commit, không phải chạy tay một lần.** Máy ảo của commit là máy sạch,
gói cài ở phiên tương tác không sống sang commit. Ô này rẻ (vài giây) nên cứ để đầu cả C1 lẫn C2.
✅ Không cần Restart: `infer_branch.py` và `score_run.py` chạy bằng tiến trình con `python`, đọc
lại `site-packages` từ đĩa nên không dính bản `peft` đã nạp trong kernel.

---

## Ô 0 — NHÌN THẤY GÌ TRONG INPUT (chạy khi ô chung 1 báo thiếu adapter)

Không assert gì, chỉ liệt kê. Ô chung 1 chỉ thấy input **tại thời điểm nó chạy**; thêm dataset
sau đó không làm ô cũ tự cập nhật, nên trước hết cứ chạy lại ô chung 1. Vẫn thiếu thì chạy ô này.

```python
import glob, os
for d in sorted(glob.glob("/kaggle/input/*/*/*")) or sorted(glob.glob("/kaggle/input/*")):
    print("■", d)
print("\n— mọi .safetensors và adapter_config.json thấy được —")
for pat in ("**/*.safetensors", "**/adapter_config.json"):
    for q in glob.glob(f"/kaggle/input/{pat}", recursive=True):
        print(f"  {os.path.getsize(q)/1e6:8.2f} MB  {q}")
```

Ba dạng hỏng và cách đọc:
· **không dòng nào in ra** ⇒ dataset chưa gắn thật; panel Input phải hiện tên nó, không chỉ là
  đã Create xong bên trang dataset.
· **chỉ có `.safetensors`, không có `adapter_config.json`** ⇒ upload thiếu một tệp. `peft` không
  nạp được adapter nếu thiếu config; upload nốt rồi Add Input lại.
· **có `.zip` hoặc thư mục lồng lạ** ⇒ Kaggle giữ nguyên tên tệp nén; giải nén ở máy rồi upload
  hai tệp trần.

⚠️ Kích thước phải là **~30 MB**. Thấy ~60 MB là đã upload `ref/`, tức adapter MIN.

---

## Ô chung 1 — dựng workspace, symlink ảnh, chốt adapter

```python
import os, glob, shutil, hashlib, json
WS = "/kaggle/working/ws"
os.makedirs(WS, exist_ok=True)

src = [q for q in glob.glob("/kaggle/input/**/harness/infer_branch.py", recursive=True)
       if "/kaggle/input/notebooks/" not in q]
assert src, "DỪNG: chưa thấy harness/infer_branch.py trong /kaggle/input"
for q in src: print("  mã:", q)
# ⛔ BÀI HỌC 5/9: "New Version" của Kaggle THÊM thư mục chứ không thay thế, nên nhiều gói
#    cùng tồn tại trong /kaggle/input. Chọn theo mtime là chọn mò. Lấy theo dấu vân tay
#    nội dung: bản 4/9 trở đi có khối fail-closed khối ứng viên.
CAN = "fail-closed ĐẠT"
ok = [q for q in src if CAN in open(q, encoding="utf-8", errors="ignore").read()]
for q in src: print(("  ✅ có bản vá 4/9" if q in ok else "  ⛔ bản cũ"), q)
assert ok, "DỪNG: không gói nào có bản vá fail-closed 4/9 — upload dataset mã bản mới"
PKG = os.path.dirname(sorted(ok, key=os.path.getmtime)[-1])
shutil.rmtree(f"{WS}/harness", ignore_errors=True)
shutil.copytree(PKG, f"{WS}/harness")

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

cfgs = [q for q in glob.glob("/kaggle/input/**/adapter_config.json", recursive=True)
        if "/kaggle/input/notebooks/" not in q]
for q in cfgs: print("  adapter cfg:", q)
assert cfgs, ("DỪNG: KHÔNG thấy adapter_config.json nào — dataset adapter chưa được GẮN vào "
              "notebook. Upload xong mới là bước một: mở panel Input → Add Input → tìm "
              "'grpo-point-adapter' → thêm. Dataset vừa tạo thì đợi Kaggle xử lý xong mới hiện.")
assert len(cfgs) == 1, (f"DỪNG: thấy {len(cfgs)} adapter_config.json — nghi đã upload cả thư "
                        f"mục ref/, tức mang theo cả adapter MIN. Xoá bản thừa rồi chạy lại.\n"
                        f"   {cfgs}")
AD = os.path.dirname(cfgs[0])
# ⛔ peft tìm ĐÚNG chuỗi "adapter_model.safetensors". Trình duyệt hay lưu thành
#    "adapter_model (1).safetensors" khi tải trùng tên, và tệp đó peft không nhận.
assert os.path.exists(f"{AD}/adapter_model.safetensors"), (
    f"DỪNG: {AD} có config nhưng KHÔNG có tệp đúng tên 'adapter_model.safetensors'.\n"
    f"   thấy: {sorted(os.listdir(AD))}\n"
    f"   Upload lại CẢ HAI tệp trong CÙNG một version từ "
    f"runs/grpo_point/adapter_grpo_point_seed101/ (đã đặt đúng tên sẵn).")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
print("adapter:", AD, "· tên thư mục (thành chữ ký):", os.path.basename(AD))
print("sha256 :", sha(f"{AD}/adapter_model.safetensors")[:16], "…")
print("r/alpha:", json.load(open(cfgs[0]))["r"], json.load(open(cfgs[0]))["lora_alpha"], "← 8 16")
```

**Kiểm:** đúng **một** `adapter_config.json` · ảnh ≥ 4.463 · `r/alpha = 8 16`.
⚠️ Chép lại **sha256** in ra đây — nó là thứ nối tệp trên Kaggle với adapter trên Drive.

---

## Ô chung 1b — TIỀN BAY, bảy phép kiểm 10 giây (⛔ đừng bỏ)

```python
import hashlib
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
R = f"{WS}/harness/dg1_cache/test_ac"

# ⓪ Gói mã đóng cho nhánh khối ứng viên có thể thiếu test.jsonl / ocr.jsonl. Chúng nằm sẵn
#    trong dataset thesis-score, nên vá tại chỗ thay vì upload lại rồi chờ thêm một vòng.
for t in ("test.jsonl", "ocr.jsonl"):
    if os.path.exists(f"{R}/{t}"):
        continue
    ung = [q for q in glob.glob(f"/kaggle/input/**/test_ac/{t}", recursive=True)
           if "/kaggle/input/notebooks/" not in q]
    assert ung, f"DỪNG: không input nào có test_ac/{t}"
    ung.sort(key=os.path.getsize, reverse=True)
    for q in ung: print(f"  nguồn {t}: {os.path.getsize(q)/1e6:7.2f} MB  {q}")
    os.makedirs(R, exist_ok=True)
    os.symlink(ung[0], f"{R}/{t}")
    print(f"  ⚠️ đã mượn {t} từ {ung[0]}")

# ① OCR tập kiểm — CHỖ HỞ NGUY HIỂM NHẤT
#    infer_branch.py:410 chỉ IN CẢNH BÁO khi thiếu ocr.jsonl rồi chạy tiếp: câu nhắc mất
#    hẳn phần chữ trên màn, khác lúc dạy, không gì dừng lại. Dòng cảnh báo đó trôi mất
#    trong log Kaggle. Chặn ở đây.
assert os.path.exists(f"{R}/ocr.jsonl"), (
    "DỪNG: gói mã thiếu test_ac/ocr.jsonl — câu nhắc sẽ THIẾU phần chữ đọc được và "
    "infer_branch.py KHÔNG dừng, chỉ in cảnh báo. Upload gói có ocr.jsonl.")
print("① ocr.jsonl :", sum(1 for _ in open(f"{R}/ocr.jsonl", encoding="utf-8")), "dòng")
print("② test.jsonl:", sum(1 for _ in open(f"{R}/test.jsonl", encoding="utf-8")), "← 6.958")
print("③ ảnh       :", len(glob.glob(f"{R}/images/*.png")), "← ≥ 4.463")
for t in ("infer_branch.py", "score_run.py", "metric_exec.py"):
    q = f"{WS}/harness/{t}"
    print(f"④ md5 {t:18s}", md5(q) if os.path.exists(q) else "THIẾU")
print("⑤ adapter   :", os.path.getsize(f"{AD}/adapter_model.safetensors")/1e6, "MB ← ~30")
print("⑥ đĩa trống :", round(shutil.disk_usage("/kaggle/working").free/2**30, 1), "GB")
print("⑦ GPU       :", os.popen("nvidia-smi --query-gpu=name,memory.total "
                                "--format=csv,noheader").read().strip())
```

**Đối chiếu md5 với máy nhà (đo 6/9):**

| tệp | md5 máy nhà | phán |
|---|---|---|
| `metric_exec.py` | `9bf0b84145458fd55919a5e161b9766f` | ⛔ **phải khớp** — đây là nơi chứa luật chấm |
| `infer_branch.py` | `ef76dece595808288a227d3044c4cea5` | khác thì đọc kỹ vì sao, dấu vân tay ở trên chỉ bảo đảm có bản vá 4/9 |
| `score_run.py` | `bb8386f8a5526a8f2a375990b7b821ce` | ⚠️ bản Kaggle **được biết là lệch** (bản trung gian `f837c834c8d1`); đã quyết chấp nhận vì phần khác nhau thuộc hai commit về UI-Venus và cỡ ảnh, mà lượt này chạy `--grounder uground` |

⚠️ `⑤` phải là **~30 MB** chứ không phải ~60 MB. Adapter GRPO lưu **bfloat16** (30.007.944 byte);
thấy 60 MB nghĩa là đã upload nhầm `ref/` — tức **adapter MIN**, chấm ra lại 60,05 mà không có
lỗi nào báo.

---

## Ô chung 2 — hàm chạy-và-chờ

```python
import subprocess, time

def chay_va_cho(cmd, log, dich=None, can=None, nhip=120, moi=True):
    env = {**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1",
           "HF_HUB_DISABLE_PROGRESS_BARS": "1"}
    # ⚠️ Chế độ "a" giữ log cũ, nên `tail` cuối hàm in lẫn traceback của lần chạy TRƯỚC và
    #    dễ đọc thành lỗi mới. Cắt log về rỗng mỗi lần chạy lại cùng một chặng.
    if moi and os.path.exists(log):
        os.remove(log)
    f = open(log, "a")
    P = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT,
                         start_new_session=True, env=env, cwd=WS)
    t0 = time.time()
    while P.poll() is None:
        time.sleep(nhip)
        n = sum(1 for _ in open(dich)) if dich and os.path.exists(dich) else -1
        gio = (time.time() - t0) / 3600
        eta = (gio * (can - n) / n) if (can and n > 0) else float("nan")
        print(f"{time.strftime('%H:%M:%S')} · {gio:5.2f} h · {n}/{can or '?'} · "
              f"còn ~{eta:.1f} h", flush=True)
    print("mã thoát:", P.returncode, flush=True)
    print(subprocess.run(["tail", "-25", log], capture_output=True, text=True).stdout)
    assert P.returncode == 0, "DỪNG: tiến trình thoát khác 0 — đọc log ở trên"
```

Hai biến môi trường là chỗ đã trả giá **7 giờ** ngày 17/8: `tqdm` ngoài terminal in mỗi cập nhật
thành một dòng, Kaggle chặn log khi vượt trần, tiến trình kẹt cứng ở lệnh ghi stdout.

---

## C1 — suy luận 4.463 bước chạm

### Ô C1a — dựng danh sách `--only`

```python
import ast
R = f"{WS}/harness/dg1_cache/test_ac"
recs = [json.loads(l) for l in open(f"{R}/test.jsonl", encoding="utf-8")]

def la_cham(r):
    a = r["action"] if isinstance(r["action"], dict) else ast.literal_eval(str(r["action"]))
    return a.get("action_type") in ("click", "long_press") and "x" in a

con = [r for r in recs if la_cham(r)]
print("bản ghi test:", len(recs), "← 6.958 · bước chạm:", len(con), "← 4.463")
assert len(con) == 4463, "DỪNG: không ra 4.463 — nghi lệch tệp test.jsonl"
with open("/kaggle/working/only_touch4463.jsonl", "w", encoding="utf-8") as f:
    for r in con:
        f.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"]}) + "\n")
```

### Ô C1b — PROBE 3 bước, chạy TAY trước khi bấm Save Version

⛔ Đừng dán ô này vào notebook commit. Ô C1a không nạp mô hình nên **không** bắt được lỗi ở khâu
nạp adapter — đúng chỗ hỏng ngày 5/9 (torchao). Ô này nạp thật, mất ~5 phút.

```python
chay_va_cho(["python", f"{WS}/harness/infer_branch.py",
             "--adapter", AD, "--only", "/kaggle/working/only_touch4463.jsonl",
             "--limit", "3", "--out", "/kaggle/working/probe3.jsonl"],
            log="/kaggle/working/probe3.log", dich="/kaggle/working/probe3.jsonl", can=3, nhip=30)
for l in open("/kaggle/working/probe3.jsonl", encoding="utf-8"):
    o = json.loads(l); print(o["run"], "|", o["pred"][:90])
```

**Kiểm ba thứ:** chữ ký `run` là `lora:<tên thư mục adapter>` · câu **không** còn thẻ `<desc>`
hay `<point>` sót lại · câu đọc như một câu hướng dẫn, không phải chuỗi toạ độ.
⚠️ Sót `<desc>`/`<point>` nghĩa là bộ trỏ sẽ đọc cả dòng khai báo thay vì câu — sai mà không có
tiếng động nào. Thấy sót thì **dừng**, báo trước khi tiêu 5 giờ.

### Ô C1c — lượt thật (đây là ô của commit)

```python
OUT = "/kaggle/working/preds_grpo_point_seed101.jsonl"
chay_va_cho(["python", f"{WS}/harness/infer_branch.py",
             "--adapter", AD, "--only", "/kaggle/working/only_touch4463.jsonl", "--out", OUT],
            log="/kaggle/working/c1_infer.log", dich=OUT, can=4463)
sig = {json.loads(l).get("run") for l in open(OUT, encoding="utf-8")}
rong = sum(1 for l in open(OUT, encoding="utf-8") if not json.loads(l).get("pred", "").strip())
sot = sum(1 for l in open(OUT, encoding="utf-8") if "<desc>" in json.loads(l).get("pred", ""))
print("n =", sum(1 for _ in open(OUT, encoding="utf-8")), "← 4.463 · chữ ký", sig,
      "· rỗng", rong, "· sót <desc>", sot, "← 0")
```

⛔ **Không** thêm `--cands`: nhánh này giữ câu nhắc 24 dòng OCR như MIN-DESC. Thêm khối ứng viên
là chấm một hệ thống khác.

Tải `preds_grpo_point_seed101.jsonl` từ Output về máy, đưa lên dataset `thesis-preds`
(**New Version**, giữ nguyên mọi tệp cũ) rồi mới sang C2.

---

## C2 — `exec` trên đủ 4.463 bước

⚠️ **Commit C2 chạy trên máy ảo sạch.** Notebook phải gồm đúng: **Ô chung 0 → 1 → 1b → 2 → ô
C2 dưới đây**.
⛔ **Bỏ hẳn ô C1a và C1c khỏi notebook C2.** Chúng thuộc lượt suy luận đã xong; giữ lại thì C1c
chết ngay vì `only_touch4463.jsonl` do C1a sinh ra chỉ sống trong `/kaggle/working` của phiên
trước, mà commit khởi động từ máy sạch. (Đã xảy ra 6/9, chết ở phút thứ hai.)
⛔ **Trước khi commit:** `preds_grpo_point_seed101.jsonl` phải đã lên dataset `thesis-preds`
(New Version) **và** được gắn vào Input — ô C2 tìm nó trong `/kaggle/input`, không phải trong
`/kaggle/working`.


```python
cand = [q for q in glob.glob("/kaggle/input/**/preds_grpo_point_seed101.jsonl", recursive=True)
        if "/kaggle/input/notebooks/" not in q]
for q in cand: print("  preds:", q, os.path.getsize(q)/1e6, "MB")
assert cand, ("DỪNG: chưa thấy preds_grpo_point_seed101.jsonl trong /kaggle/input — upload nó "
              "lên dataset thesis-preds (New Version) rồi Add Input trước khi commit C2.")
assert len(cand) == 1, f"DỪNG: {len(cand)} bản preds cùng tên, không biết lấy bản nào:\n   {cand}"
P = cand[0]
n_preds = sum(1 for _ in open(P, encoding="utf-8"))
print("số bản ghi preds:", n_preds, "← 4.463")
assert n_preds == 4463, "DỪNG: preds không đủ 4.463 bước — nghi gắn phải tệp của lượt khác"
RAW = "/kaggle/working/score_grpo_point_seed101_raw.jsonl"
chay_va_cho(["python", f"{WS}/harness/score_run.py", "--mode", "score",
             "--grounder", "uground", "--preds", P,
             "--out", "/kaggle/working/score_grpo_point_seed101.json"],
            log="/kaggle/working/c2_score.log", dich=RAW, can=4463)
print(json.dumps(json.load(open("/kaggle/working/score_grpo_point_seed101.json")),
                 ensure_ascii=False, indent=1)[:1200])
```

⚠️ `score_run.py` **không có cờ `--raw`** — nó tự suy tên tệp thô từ `--out`.
⚠️ **Bẫy tên trường:** `exec_disk` trong JSON là `hit_disk` **thuần**, KHÔNG gated. Hàng "chữ nhật
.14" phải tính lại từ tệp thô, đừng đọc thẳng JSON (đã nhầm 66,35 ungated với 63,86 gated).

Giữ `*_raw.jsonl` — có nó thì đổi luật chấm (D.3, nL2) tính lại được **không gọi lại bộ trỏ**.

---

## C3 — bước KHÔNG chạm (2.495 bước), theo (x20b)

Đo vô điều kiện sau C2 (chủ luận văn quyết 6/9). **Chỉ khâu suy luận cần GPU**; khâu chấm
(`--mode noharm`) so `canon_action` của câu mô hình với câu chuẩn nên **không gọi bộ trỏ** và
chạy được ở máy nhà, 0 GPU.

**Input thêm:** dataset mới `thesis-nontap-images` từ `test_images_nontap.tar` (1,54 GB, 2.495
ảnh, đã đóng sẵn ở máy — đường dẫn Windows `Downloads\test_images_nontap.tar`). Ảnh trong tar
theo cấu trúc `test_ac/images/*.png`.

### Ô C3a — gộp ảnh từ MỌI nguồn rồi dựng danh sách `--only`

⛔ Đừng dùng khối symlink của Ô chung 1 cho lượt này: nó chọn **một** thư mục ảnh và đòi ≥ 4.400
tệp, trong khi gói mới chỉ có 2.495 và các ảnh cần nằm rải ở hai dataset. Ô dưới gộp bằng symlink
từng tệp.

```python
import glob, os, json, ast, tarfile
R = f"{WS}/harness/dg1_cache/test_ac"
IMG = f"{R}/images"
if os.path.islink(IMG): os.remove(IMG)
os.makedirs(IMG, exist_ok=True)

# Kaggle có thể giữ nguyên .tar thay vì bung — xử cả hai trường hợp.
for t in glob.glob("/kaggle/input/**/*.tar", recursive=True):
    print("  bung", t)
    tarfile.open(t).extractall("/kaggle/working/nontap")

n = 0
for src in glob.glob("/kaggle/input/**/test_ac/images", recursive=True) + \
           glob.glob("/kaggle/working/nontap/**/images", recursive=True):
    for q in glob.glob(f"{src}/*.png"):
        d = f"{IMG}/{os.path.basename(q)}"
        if not os.path.exists(d):
            os.symlink(q, d); n += 1
print("ảnh gộp được:", len(glob.glob(f"{IMG}/*.png")), "← cần ≥ 6.958 (mới thêm", n, ")")
assert len(glob.glob(f"{IMG}/*.png")) >= 6958, "DỪNG: chưa đủ ảnh cho bước không chạm"

recs = [json.loads(l) for l in open(f"{R}/test.jsonl", encoding="utf-8")]
def la_cham(r):
    a = r["action"] if isinstance(r["action"], dict) else ast.literal_eval(str(r["action"]))
    return a.get("action_type") in ("click", "long_press") and "x" in a
non = [r for r in recs if not la_cham(r)]
print("bước KHÔNG chạm:", len(non), "← 2.495")
assert len(non) == 2495, "DỪNG: không ra 2.495"
with open("/kaggle/working/only_nontap2495.jsonl", "w", encoding="utf-8") as f:
    for r in non:
        f.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"]}) + "\n")
```

### Ô C3b — suy luận 2.495 bước (~1,7 h)

```python
OUT = "/kaggle/working/preds_grpo_point_seed101_nontap.jsonl"
chay_va_cho(["python", f"{WS}/harness/infer_branch.py", "--adapter", AD,
             "--only", "/kaggle/working/only_nontap2495.jsonl", "--out", OUT],
            log="/kaggle/working/c3_infer.log", dich=OUT, can=2495)
print("n =", sum(1 for _ in open(OUT, encoding="utf-8")), "← 2.495 · chữ ký",
      {json.loads(l).get("run") for l in open(OUT, encoding="utf-8")})
```

### Chấm ở MÁY NHÀ — 0 GPU

Cần cả nhánh MIN trên cùng lát để so cặp. Tệp `runs/preds_min_desc_seed101.jsonl` đã có đủ 6.958
bước nên **không phải chạy lại gì cho MIN**.

```
python3 harness/score_run.py --mode noharm \
    --preds runs/grpo_point/preds_grpo_point_seed101_nontap.jsonl \
    --baseline runs/preds_min_desc_seed101.jsonl \
    --out runs/grpo_point/noharm_grpo_point_seed101.json
```

**Đọc theo (x20b), ngưỡng lấy nguyên từ mục 3 của bản gốc — không đặt ngưỡng mới:** tỉ lệ khớp
loại thao tác của GRPO không được thấp hơn MIN quá **3 điểm phần trăm**. Thấp hơn quá mức đó
⇒ **báo là tác hại ở bước không chạm**, và mọi chỗ trình `exec` phải in kèm con số này.
⛔ Kết quả phép này **không** được dùng để đổi cách đọc `exec`, theo cả hai chiều.

---

## Đọc kết quả — theo (x19e), khoá trước, không nới

· Headline: **`exec` Voronoi gated .14 trên n=4.463**, phép so chính là **GRPO/101 − MIN/101
  (60,05)**, McNemar ghép cặp + KTC bootstrap.
· **Một hạt giống ⇒ nhãn "một hạt giống".** Chỉ gọi *tăng* khi Δ ≥ **2,2** pp và KTC loại 0;
  dưới đó là **TRẮNG dù dấu nào**. Kỳ vọng ghi trước **+2 … +4**; trên **+5** thì soi kỹ hơn
  bình thường trước khi tin.
· Thước phụ bắt buộc báo kèm: `gate_desc_acc.py` · BLEU-4/ROUGE-L theo `text_metrics.py`
  (**BLEU-4 giảm quá 1,0 so với MIN là dấu hiệu câu bị bẻ thành mật mã** — phải khai và hạ kết
  luận) · `action_ok` · D.3 và nL2 báo kèm · tỉ lệ sinh `<desc>`.
· Hạt 202 **chỉ** chạy nếu Δ ≥ 2,2, và quyết ở (x20) **trước** khi nhìn số 202.
· Báo kết quả **dù ra sao**, kể cả âm.
