# Runbook Colab — PATA-C1: Stage S → Stage H → C1 (report/185, 186, 193)

Lượt TRẢ PHÍ duy nhất của thử nghiệm C1. Mọi thứ không cần GPU đã làm xong ở WSL/Kaggle:
13/13 unit test trên 3B thật, smoke S/H/J (`runs/pata/kaggle_smoke/`), audit box, luật KL box ≥ 0,50.

| ô | việc | máy | thời gian | dừng nếu |
|---|---|---|---|---|
| P0 | chuẩn bị ở nhà | — | 5 phút | — |
| P1 | cài gói | GPU đã chọn | 3 phút | không thấy GPU |
| P2 | Drive, mã, dữ liệu, ảnh | như trên | ~15 phút | số đếm hoặc hash lệch |
| P3 | **đo máy**: 6 update S | **L4 trước**, A100 sau nếu cần | ~10 phút/máy | — |
| P4 | chạy một chặng, chạy nền | máy đã chọn | S ~? h · H ~? h · C1 ~? h | — |
| P5 | ô theo dõi + đồng bộ Drive, **chạy tiền cảnh suốt lượt** | — | suốt lượt | NaN · tràn bộ nhớ |
| P6 | chẩn đoán sau chặng S (CE_val) | cùng máy | ~10 phút | CE_val phân kỳ |
| P7 | **cổng H** trên val400 | cùng máy | ~15 phút | **không đạt ⇒ DỪNG, không chạy C1** |
| P8 | **mốc 800 của C1** | cùng máy, chạy song song | ~20 phút | **bridge không được dùng ⇒ DỪNG** |
| P9 | hết epoch C1: sinh câu val600 bật/tắt bridge | cùng máy | ~1 h | — |
| P10 | chấm `exec` val600 (UGround) | **Kaggle T4, 0 đồng** | ~1 h | — |

⛔⛔ **BỐN LUẬT COLAB (CLAUDE.md) — vi phạm là mất tiền thật:**
① `Popen(..., start_new_session=True)` · ② **không bấm Stop ô nào** khi train đang chạy (cần ô khác thì
mở notebook thứ hai hoặc Terminal Colab) · ③ theo dõi bằng log **LOCAL** `/content/pata_*.log`, không đọc
tệp trên Drive · ④ **ô P5 phải chạy tiền cảnh suốt lượt** (không có nó Colab ngắt máy sau ~90 phút rỗi).

⛔ **Mốc giờ đọc bằng `TZ='Asia/Ho_Chi_Minh' date`** (máy WSL chạy giờ UTC).

---

## Ô P0 — chuẩn bị ở nhà (0 đồng)

1. Dựng gói (đã dựng sẵn 23/9 tối — dựng lại nếu sửa mã):
   ```
   ~/.venvs/thesis/bin/python harness/make_bundle.py pata_colab
   ```
2. Upload `_bundles/thesis_pata_colab.zip` (~26 MB) lên **`MyDrive/thesis/`** (ghi đè bản cũ nếu có).
3. Ảnh dạy: dùng lại `MyDrive/thesis/train_images_p*.tar` (~12 GB, đã có từ các lượt trước; val400/val600
   cũng nằm trong đó vì val tách từ tập dạy).
4. Tra giá **tại thời điểm chạy**: Colab → Runtime → Change runtime type → xem đơn vị/giờ của L4 và A100.

## Ô P1 — cài gói

Runtime → Change runtime type → **L4** (lần đầu, để đo ở P3).

```python
import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "bitsandbytes", "peft"], check=True)
import torch, transformers, peft, bitsandbytes
print("torch", torch.__version__, "· transformers", transformers.__version__,
      "· peft", peft.__version__, "· bnb", bitsandbytes.__version__)
assert torch.cuda.is_available(), "⛔ không có GPU"
print(torch.cuda.get_device_name(0), round(torch.cuda.get_device_properties(0).total_memory / 2**30, 1), "GB")
```

Ghi lại dòng phiên bản — đưa vào manifest §11.

## Ô P2 — Drive, mã, dữ liệu, ảnh

```python
from google.colab import drive; drive.mount("/content/drive")
import os, glob, json, hashlib, zipfile, subprocess
D = "/content/drive/MyDrive/thesis"
WS = "/content/ws"; os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_pata_colab.zip").extractall(WS)
REPO = f"{WS}/thesis"; os.chdir(REPO)
DR = f"{REPO}/harness/dg1_cache/train_ac"

# ── mã phải là bản đã vá 23/9 tối (cắt gradient theo nhóm + luật KL box ≥ 0,50) ──
t = open("harness/pata_train.py").read()
assert '"name": "target"' in t and "for g_ in groups" in t, "⛔ pata_train.py BẢN CŨ — upload lại gói"
assert "AREA_KL_MAX = 0.50" in open("harness/pata_data.py").read(), "⛔ pata_data.py BẢN CŨ"
assert 'rec.get("kl_ok", True)' in open("harness/pata_model.py").read(), "⛔ pata_model.py BẢN CŨ"

# ── dữ liệu: hash phải khớp split_hash.json ──
h = json.load(open(f"{DR}/pata/split_hash.json"))
for f in ("train_proper.jsonl", "val400.jsonl", "val600.jsonl", "probe40.jsonl"):
    got = hashlib.sha256(open(f"{DR}/pata/{f}", "rb").read()).hexdigest()
    assert got == h[f], f"⛔ {f} lệch hash"
print("hash      : 4/4 khớp ✓  probe40", h["probe40.jsonl"][:12])
R = [json.loads(l) for l in open(f"{DR}/pata/train_proper.jsonl")]
n_kl = sum(r["kl_ok"] for r in R)
print("train     :", len(R), "chạm ·", n_kl, "kl_ok   ← cần 40189 · 39432")
assert (len(R), n_kl) == (40189, 39432)

# ── ảnh: bung tar vào local (không đọc ảnh từ Drive khi train — FUSE chậm) ──
IMG = f"{DR}/images"; os.makedirs(IMG, exist_ok=True)
if len(os.listdir(IMG)) < 64567:
    for g in sorted(glob.glob(f"{D}/train_images_p*.tar")):
        print("bung", os.path.basename(g), flush=True)
        subprocess.run(["tar", "xf", g, "-C", IMG], check=True)
can = {r["image"] for f in ("train_proper", "val400", "val600")
       for r in map(json.loads, open(f"{DR}/pata/{f}.jsonl"))}
thieu = [x for x in can if not os.path.exists(f"{DR}/{x}")]
print("ảnh       :", len(os.listdir(IMG)), "trên đĩa ·", len(can) - len(thieu), "/", len(can), "ảnh cần")
assert not thieu, f"⛔ thiếu {len(thieu)} ảnh, vd {thieu[:3]}"
CK = f"{D}/pata_ck"; os.makedirs(CK, exist_ok=True)       # điểm lưu trên Drive
print("Drive ck  :", CK)
```

**Phải in:** `hash 4/4 khớp` · `40189 chạm · 39432 kl_ok` · ảnh cần đủ.
⚠️ Nếu tar bung ra một tầng thư mục thừa (`images/images/…`) thì assert ảnh sẽ đỏ — báo lại để sửa đường dẫn.

## Ô P3 — đo máy (chạy trên L4 trước)

6 update Stage S, cấu hình thật (lô 4 × gộp 4 = 16). Update đầu có chi phí khởi động nên đọc `s/u` ở u6.

```python
import subprocess, time
def chay(cmd, log):
    env = dict(os.environ, TQDM_DISABLE="1", HF_HUB_DISABLE_PROGRESS_BARS="1",
               PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True", PYTHONUNBUFFERED="1")
    return subprocess.Popen(cmd, stdout=open(log, "w"), stderr=subprocess.STDOUT, env=env,
                            cwd=REPO, start_new_session=True)
p = chay(["python", "harness/pata_train.py", "--stage", "S", "--data-root", DR, "--bs", "4", "--accum", "4",
          "--max-updates", "6", "--log-steps", "1", "--save-steps", "1000", "--workers", "8",
          "--out", "/content/do_may_S"], "/content/do_may.log")
while p.poll() is None:
    time.sleep(30)
print("\n".join(l for l in open("/content/do_may.log").read().splitlines() if "u6/" in l or "Error" in l))
```

**Luật chọn máy (CLAUDE.md, user chốt 9/9):** gọi `t_L4`, `t_A100` là `s/u` ở u6.
- Chỉ đo L4 được thì ghi lại `t_L4`, rồi đổi runtime sang **A100**, chạy lại P1 → P3.
- **`t_L4 / t_A100 ≤ 1,5` ⇒ chọn L4** cho cả ba chặng. **> 1,5 ⇒ A100.**
- Chặng H forward chỉ tới block 17 và không học LoRA — nếu S phải lên A100, vẫn đo riêng H trên L4
  (thay `--stage S` bằng H cần một điểm lưu S, nên làm sau khi có S; xem P4).
- VRAM đỉnh đo trên Kaggle ≤ 5,4 GB (lô 2) ⇒ L4 22 GB thừa bộ nhớ; không cần lo tràn.

**Ước giờ theo `s/u` đo được:** S ≈ 2.512 × s/u · H ≈ 2.465 × s/u × ~0,76 · C1 ≈ 2.512 × s/u.
Ghi con số vào bảng đầu runbook trước khi bấm lượt thật.

## Ô P4 — chạy một chặng, chạy nền

Đặt `STAGE` rồi chạy. Chạy lại **đúng ô này** sau khi mất máy (sau P1 + P2) là tự nối tiếp: ô chép điểm
lưu mới nhất trên Drive về local trước khi khởi động.

```python
import shutil
STAGE = "S"          # ⬅ "S" → rồi "H" → rồi "J"  (C1 = J bridge bật)
OUT = f"/content/ck/{STAGE}"
os.makedirs(OUT, exist_ok=True)
# nối tiếp: lấy điểm lưu TRỌN (có DONE) mới nhất trên Drive nếu local chưa có
dck = sorted(glob.glob(f"{CK}/{STAGE}/ckpt-*/DONE"))
if dck and not glob.glob(f"{OUT}/ckpt-*/DONE"):
    src = os.path.dirname(dck[-1])
    shutil.copytree(src, f"{OUT}/{os.path.basename(src)}")
    print("nối tiếp từ Drive:", src)
extra = {"S": [],
         "H": ["--init-adapter", f"{CK}/S/final"],
         "J": ["--init-adapter", f"{CK}/S/final", "--init-heads", f"{CK}/H/final"]}[STAGE]
P = chay(["python", "harness/pata_train.py", "--stage", STAGE, "--data-root", DR,
          "--bs", "4", "--accum", "4", "--save-steps", "100", "--milestones", "800",
          "--log-steps", "20", "--workers", "8", "--out", OUT] + extra, f"/content/pata_{STAGE}.log")
print("PID", P.pid, "· log /content/pata_%s.log" % STAGE)
```

⛔ Chặng H và J nạp `final/` của chặng trước **từ Drive** (`{CK}/S/final`, `{CK}/H/final`) — ô P5 đẩy
`final/` lên Drive khi chặng xong. Chưa thấy `final/` trên Drive thì **đừng** chạy chặng sau.

## Ô P5 — theo dõi + đồng bộ Drive (CHẠY TIỀN CẢNH SUỐT LƯỢT, không bấm Stop)

```python
import time, datetime, shutil
def dong_bo():
    """Đẩy điểm lưu TRỌN chưa có lên Drive: chép sang tên tạm rồi đổi tên (Drive chỉ thấy tệp đã đóng)."""
    os.makedirs(f"{CK}/{STAGE}", exist_ok=True)
    for c in sorted(glob.glob(f"{OUT}/ckpt-*")) + [f"{OUT}/final"]:
        ten = os.path.basename(c)
        if not os.path.isdir(c) or c.endswith(".tmp"):
            continue
        if ten != "final" and not os.path.exists(f"{c}/DONE"):
            continue
        dst = f"{CK}/{STAGE}/{ten}"
        if os.path.exists(dst):
            continue
        shutil.copytree(c, dst + ".tmp"); os.rename(dst + ".tmp", dst)
        print("   ↑ Drive:", dst, flush=True)
    for f in (f"{OUT}/train_log.jsonl", f"{OUT}/final_sha256.json", f"/content/pata_{STAGE}.log"):
        if os.path.exists(f):
            shutil.copy(f, f"{CK}/{STAGE}/")
t_sync = 0
while P.poll() is None:
    time.sleep(60)
    L = open(f"/content/pata_{STAGE}.log").read().splitlines()
    dong = [l for l in L if l.startswith("[") and "/" in l and " u" in l]
    gio = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime("%H:%M")
    print(f"[{gio} VN] {(dong or L or [''])[-1][:230]}", flush=True)
    if any(k in l for l in L[-30:] for k in ("=nan", "NaN", "OutOfMemory", "Traceback")):
        print("⛔ LỖI trong log — xem /content/pata_%s.log" % STAGE); break
    if time.time() - t_sync > 300:
        dong_bo(); t_sync = time.time()
dong_bo()
print("== tiến trình kết thúc, mã", P.poll(), "==")
print("\n".join(L[-8:]))
```

**Đọc trong lúc chạy:**
- S: `ce=` giảm rồi ổn định; `gn lora` vài đơn vị.
- H: `kl=` giảm, `mass=` tăng; `gn lora = 0`; `tvec` có thể lớn (đã tách nhóm, không kéo nhóm khác).
- C1: `gate=` nhích lên từ 0,119; `resid=` tăng dần từ 0; `ce=` hồi về quanh mức S (smoke: TARGET làm
  CE vọt 1,12 → 2,36 rồi C1 hồi về 1,27 sau 20 update).
- ⚠️ Dòng log in lại y hệt nhiều phút là bình thường (log mỗi 20 update, ~3–5 phút/lần).

## Ô P6 — sau chặng S: CE_val trên val400 (§6 Stage S)

```python
e = chay(["python", "harness/pata_eval.py", "--ckpt", f"{CK}/S/final", "--mode", "diag",
          "--split", "val400", "--data-root", DR, "--out", f"{CK}/eval"], "/content/eval_S.log")
e.wait(); print(open("/content/eval_S.log").read()[-600:])
```
Ghi `CE_val`. Chỉ để bắt phân kỳ, không dùng làm kết quả.

## Ô P7 — CỔNG H trên val400 (quan trọng nhất trước C1)

```python
e = chay(["python", "harness/pata_eval.py", "--ckpt", f"{CK}/H/final", "--mode", "diag",
          "--split", "val400", "--no-ce", "--data-root", DR, "--out", f"{CK}/eval"], "/content/eval_H.log")
e.wait(); print(open("/content/eval_H.log").read()[-1200:])
```

**Luật (khoá trong `185` §6):** đi tiếp C1 **chỉ khi** in `⇒ CỔNG H: ĐẠT`, tức cận dưới KTC một phía
90% của cả ba hiệu > 0: mass − center prior · mass − train prior · mass(prompt đúng) − mass(prompt xáo).
⛔ **Không đạt ⇒ DỪNG**, không chạy C1, không mở test. Kết luận "futility under budget". Gửi mình
`diag_final_val400.json`.
⚠️ Smoke 20 update: xáo prompt **không** làm đổi mass — vế thứ ba là vế khó nhất, xem kỹ số này.

## Ô P8 — mốc 800 của C1 (chạy song song, không dừng train)

Khi ô P5 in `↑ Drive: …/J/ckpt-00800`, mở **Terminal Colab** (biểu tượng terminal ở thanh bên trái —
cùng máy ảo, không đụng tới ô P5 đang chạy; ⛔ không bấm Stop P5 để chạy ô mới) rồi dán:

```bash
cd /content/ws/thesis
DR=harness/dg1_cache/train_ac; CK=/content/drive/MyDrive/thesis/pata_ck
python harness/pata_eval.py --ckpt /content/ck/J/ckpt-00800 --mode diag --split val400 --data-root $DR --out $CK/eval > /content/m800_diag.log 2>&1
python harness/pata_eval.py --ckpt /content/ck/J/ckpt-00800 --mode gen --split probe40 --variants on,off --data-root $DR --out $CK/eval > /content/m800_gen.log 2>&1
tail -25 /content/m800_diag.log; tail -5 /content/m800_gen.log
```
(VRAM của train chỉ ~5 GB nên chạy song song được; train chậm lại trong ~20 phút đó.)

**Luật mốc 800 (`185` §7b, §8):** chỉ được dừng vì lỗi kỹ thuật:
1. `CE_val`, `KL_val` không phân kỳ;
2. **tắt bridge làm ≥ 30% câu probe đổi** — dòng `câu ĐỔI khi tắt bridge`. Gần như không đổi ⇒ decoder
   bỏ qua bridge ⇒ **DỪNG** C1, không tốn hết epoch;
3. xáo prompt thì mass giảm (`dung_vs_xao` dương);
4. format hợp lệ ≥ 95% (`format hợp lệ` của biến thể `on`).
Đạt ⇒ để C1 chạy hết epoch. ⛔ Không đổi λ, block, LR, gate sau khi xem mốc 800. ⛔ Không suy `exec` từ
probe 40.

## Ô P9 — hết epoch C1: sinh câu val600 (MỘT lần)

```python
for ck, tag in ((f"{CK}/J/final", "C1"), (f"{CK}/S/final", "S")):
    e = chay(["python", "harness/pata_eval.py", "--ckpt", ck, "--mode", "gen", "--split", "val600",
              "--variants", "on,off" if tag == "C1" else "on", "--data-root", DR,
              "--out", f"{CK}/eval_val600_{tag}"], f"/content/gen600_{tag}.log")
    e.wait(); print(tag, open(f"/content/gen600_{tag}.log").read()[-400:])
```
Ra ba tệp preds: C1 bật bridge · C1 tắt bridge · S (không TARGET) — đủ cho điều kiện 3 và 4 của cổng §8.
⛔ val600 là tập cổng cuối, **chỉ chạy một lần**.
⚠️ Điều kiện 5 (swap sang distractor vs random-pool) **chưa có mã** — mình viết trong lúc C1 train.

## Ô P10 — chấm `exec` val600 trên Kaggle (0 đồng)

Làm sau, khi có ba tệp preds: runbook riêng (dùng lại dataset `thesis-val-cham` + `score_run.py
--data-root … --recs-file val_cham600.jsonl`), mình viết khi C1 chạy.

---

## Sau lượt — gửi mình

`{CK}/S|H|J/train_log.jsonl` · `{CK}/eval/*.json` · ba tệp preds val600 · dòng phiên bản ở P1 · `s/u`
đo ở P3. Mình seal manifest §11 (cần SHA của `S/final`, `H/final` trong `final_sha256.json`).
