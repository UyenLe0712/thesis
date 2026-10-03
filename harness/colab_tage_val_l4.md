# TAGE trên Colab L4 — kiểm thử val C1 (file 265, 2/10/2026)

Thay cho `kaggle_tage_val.md` vì Kaggle T4 tuần này chỉ còn ~1 h. Thiết kế, ngưỡng, lý do:
`harness/tai_lieu_2026-10-02/265_ACTION_KIEM_THU_TAGE_VAL_2_10_checked.md`. **Số val — không trích.**

Máy: **L4**, bf16. V1 ước lượng ~7 h (chưa đo; lượt `TEST` in `s/mẫu` thật). Một phiên chạy trọn V1, không
phải tách commit như Kaggle. Đơn vị/giờ của L4: xem ở *Change runtime type* lúc bấm, đừng lấy số nhớ.

⛔ Bốn luật Colab (CLAUDE.md) đã cài sẵn vào các ô: tiến trình con `start_new_session=True` · **không bấm
Stop ô C5 khi đang chạy** (Stop cũng không giết tiến trình con, nhưng các pha sau sẽ không được khởi động) ·
log và kết quả ghi ở **đĩa local `/content`**, một luồng nền chép sang Drive mỗi 5 phút · ô C5 chạy
foreground suốt lượt nên Colab không ngắt vì rỗi.

## Chuẩn bị (máy nhà → Drive)

Tải lên **`MyDrive/thesis/tage/`** (tệp đã có sẵn trên Drive thì bỏ qua):

| tệp trên máy nhà | md5 | chứa gì |
|---|---|---|
| `_bundles/fgrb_p1_bundle.zip` (2,6 GB) | `b19baca508009f5c1694abcd528b297b` | adapter S1, 5.567 ảnh, OCR, hàng train/val |
| `_bundles/thesis_val_cham.zip` (0,8 GB) | `67520476d77a7257669f6511d58e959e` | bản ghi chấm val, ảnh, OCR |
| `_bundles/c1_exec8.zip` (52 KB) | `ecf255cedb25966c4a6aa33690b2bb8f` | `c1_mau.jsonl`, `c1_picks.json`, mã chấm `thesis/harness/` |
| `_bundles/tage_colab.zip` (57 MB) | `36919554b062205b98c3542087025316` | `checkpoint-500/` (ck500) + `tage-val-script/` (6 tệp) |

Colab: *Runtime → Change runtime type → **L4 GPU***.

## C1 — gắn Drive, chép về đĩa local, cài gói

```python
import os, subprocess, sys, time, hashlib, shutil, glob, json, threading
from google.colab import drive; drive.mount('/content/drive')
DR = "/content/drive/MyDrive/thesis/tage"
IN = "/content/in"
os.makedirs(IN, exist_ok=True)
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
ZIP = {"fgrb_p1_bundle.zip": "b19baca508009f5c1694abcd528b297b", "thesis_val_cham.zip": "67520476d77a7257669f6511d58e959e",
       "c1_exec8.zip": "ecf255cedb25966c4a6aa33690b2bb8f", "tage_colab.zip": "36919554b062205b98c3542087025316"}
for z, h in ZIP.items():
    if os.path.exists(f"{IN}/{z}.xong"):
        continue
    t0 = time.time()
    shutil.copy(f"{DR}/{z}", f"/content/{z}")
    assert md5(f"/content/{z}") == h, f"DỪNG: {z} lệch md5 (upload hỏng hoặc bản cũ)"
    d = f"{IN}/c1_exec8" if z == "c1_exec8.zip" else IN
    subprocess.run(["unzip", "-q", "-o", f"/content/{z}", "-d", d], check=True)
    os.remove(f"/content/{z}"); open(f"{IN}/{z}.xong", "w").close()
    print(f"{z}: chép + giải nén {time.time()-t0:.0f} s", flush=True)

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes pillow 2>&1 | tail -3")
sh(f'{sys.executable} -c "import transformers, peft, torch; print(transformers.__version__, peft.__version__, torch.__version__, torch.cuda.get_device_name(0))"')
```

Phải thấy bốn dòng `chép + giải nén` (lần đầu) và tên card **L4**. peft báo `incompatible version of torchao`
thì *Runtime → Restart session* rồi chạy từ C2.

## C2 — đường dẫn, md5, khôi phục kết quả cũ từ Drive

```python
import os, subprocess, sys, time, hashlib, shutil, glob, json, threading
TEST = True                         # chạy thử; xong thì đổi False và chạy lại C2 → C5
IN, W, DR = "/content/in", "/content/w", "/content/drive/MyDrive/thesis/tage"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
os.makedirs(W, exist_ok=True)
O = f"{W}/thu" if TEST else f"{W}/that"
OD = f"{DR}/out/{'thu' if TEST else 'that'}"
os.makedirs(O, exist_ok=True); os.makedirs(OD, exist_ok=True)

BUNDLE = f"{IN}/fgrb_p1_bundle"
assert os.path.isdir(f"{BUNDLE}/adapter_s1_seed101") and len(os.listdir(f"{BUNDLE}/images")) == 5567
PK = f"{IN}/c1_exec8"
C1_PATH = f"{PK}/c1_mau.jsonl"
assert md5(C1_PATH) == "d757554326977309c3a65ae0b144c211", "DỪNG: c1_mau.jsonl lệch"
SD = f"{IN}/tage-val-script"
MD = {"tage_val.py": "e15f9d524ab307349498f2ca3ebcbc68", "grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf",
      "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912", "tage_neg.jsonl": "75539cdc533ecaa578d6067e3fbcd8a5",
      "pred_ck500.jsonl": "eb6162d86730a936beb5ae5a9fd6d652", "score_ck500_raw.jsonl": "258ced11cad3b6729bbdb25f947dbe78"}
for f, h in MD.items():
    shutil.copy(f"{SD}/{f}", f"{W}/{f}")
    assert md5(f"{W}/{f}") == h, f"DỪNG: {f} lệch"
CK500 = f"{IN}/checkpoint-500"
assert md5(f"{CK500}/adapter_model.safetensors") == "491fa6677340393f1e4464c08a0cec98", "DỪNG: không phải ck500 đã chấm"
NEG, PRED500, MERGED = f"{W}/tage_neg.jsonl", f"{W}/pred_ck500.jsonl", f"{W}/s1_merged"

# mất máy rồi dựng lại: kéo kết quả đã đồng bộ từ Drive về (không đè tệp local đã có)
subprocess.run(["rsync", "-a", "--ignore-existing", f"{OD}/", f"{O}/"], check=True)
# bản chép có thể bắt đúng lúc một dòng đang ghi dở ⇒ cắt dòng cuối hỏng, không thì lúc nối tiếp json.loads văng lỗi
for p in glob.glob(f"{O}/**/*.jsonl", recursive=True):
    L = open(p, encoding="utf-8").read().split("\n")
    tot = []
    for l in L:
        if not l.strip():
            continue
        try: json.loads(l); tot.append(l)
        except ValueError: print(f"⚠️ bỏ dòng hỏng ở {os.path.basename(p)}: {l[:60]!r}", flush=True)
    if len(tot) != len([l for l in L if l.strip()]):
        open(p, "w", encoding="utf-8").write("\n".join(tot) + "\n")
for p in sorted(glob.glob(f"{O}/**/*.jsonl", recursive=True)):
    print(f"  {os.path.relpath(p, O)}: {sum(1 for _ in open(p))} dòng")
ck = f"{O}/ed_gold/ckpt_last/state.json"
print("điểm lưu train:", json.load(open(ck))["buoc"] if os.path.exists(ck) else "chưa có", "bước")
print("O =", O, "· có sẵn:", sorted(os.listdir(O)), flush=True)
```

## C3 — hàm chạy + luồng đồng bộ Drive

```python
def dong_bo():
    subprocess.run(["rsync", "-a", f"{O}/", f"{OD}/"])          # rsync ghi tệp tạm rồi đổi tên ⇒ Drive nhận tệp đóng trọn

def _luong():
    while True:
        time.sleep(300)
        try: dong_bo()
        except Exception as e: print("⚠️ đồng bộ lỗi:", e, flush=True)
if not any(t.name == "dongbo" for t in threading.enumerate()):
    threading.Thread(target=_luong, name="dongbo", daemon=True).start()

def chay(cmd, log, cwd=None, nhip=120):
    t0 = time.time()
    with open(log, "a") as f:
        q = subprocess.Popen(cmd, cwd=cwd or W, stdout=f, stderr=subprocess.STDOUT, start_new_session=True,
                             env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
                                  "PYTHONUNBUFFERED": "1"})
        while q.poll() is None:
            time.sleep(30 if TEST else nhip)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"  {time.strftime('%H:%M', time.gmtime(time.time()+7*3600))} VN · {(time.time()-t0)/60:6.1f} phút · "
                  f"{os.path.basename(log)} · {L[-1][:110] if L else '...'}", flush=True)
    print(f"--- {os.path.basename(log)} · mã thoát {q.returncode} · {(time.time()-t0)/60:.1f} phút ---")
    print("".join(open(log, errors="ignore").readlines()[-8:]), flush=True)
    dong_bo()
    assert q.returncode == 0, f"DỪNG: xem {log}"

T = ["python", "tage_val.py", "--bundle", BUNDLE, "--merged", MERGED, "--neg", NEG]
```

## C4 — dữ liệu chấm (Phụ lục D, chỉnh đường dẫn cho Colab)

```python
VB = f"{IN}/thesis_val_cham"
for f in ("val_cham400.jsonl", "val_cham600.jsonl", "ocr.jsonl", "images"):
    assert os.path.exists(f"{VB}/{f}"), f"DỪNG: thesis_val_cham thiếu {f}"
WS = f"{W}/pk/thesis"
shutil.copytree(f"{PK}/thesis", WS, dirs_exist_ok=True)
sr = open(f"{WS}/harness/score_run.py", encoding="utf-8").read()
assert "--recs-file" in sr and "TỆP THÔ KHÔNG KHỚP" in sr, "DỪNG: score_run.py là bản cũ"

C1 = [json.loads(l) for l in open(C1_PATH, encoding="utf-8")]
TAPT = ("click", "long_press")
KEYS = {(r["episode_id"], r["step_id"]) for r in C1}
VD = f"{W}/c1data"
os.makedirs(VD, exist_ok=True)
recs = {}
for f in ("val_cham400.jsonl", "val_cham600.jsonl"):
    for d in map(json.loads, open(f"{VB}/{f}", encoding="utf-8")):
        k = (d["episode_id"], d["step_id"])
        if k in KEYS and k not in recs:
            d.setdefault("gold_instruction", d["target_instruction"])
            recs[k] = d
assert len(recs) == 400, f"DỪNG: chỉ ghép được {len(recs)}/400 bước C1"
with open(f"{VD}/c1_recs.jsonl", "w", encoding="utf-8") as fo:
    for r in C1:
        fo.write(json.dumps(recs[(r["episode_id"], r["step_id"])], ensure_ascii=False) + "\n")
shutil.copy(f"{VB}/ocr.jsonl", f"{VD}/ocr.jsonl")
if os.path.lexists(f"{VD}/images"):
    os.remove(f"{VD}/images")
os.symlink(f"{VB}/images", f"{VD}/images")
taps = [d for d in recs.values() if d["action"].get("action_type") in TAPT and "x" in d["action"]]
assert len(taps) == 249 and all(os.path.exists(f"{VD}/{d['image']}") for d in taps)
os.makedirs(f"{W}/c1preds", exist_ok=True)
with open(f"{W}/c1preds/k0.jsonl", "w", encoding="utf-8") as fo:
    for r in C1:
        fo.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "pred": r["greedy"]},
                            ensure_ascii=False) + "\n")

from huggingface_hub import snapshot_download
print("UGround:", snapshot_download("osunlp/UGround-V1-2B"), flush=True)
sys.path.insert(0, f"{WS}/harness")
import a11y_inventory as A11Y, score_run as SR
names = set(A11Y._zip().namelist())
co_cay = sum(A11Y.key_for(f"episode_{d['episode_id']}_screenshot_{d['step_id']}.png") in names for d in taps)
rong = sum(len(SR.buttons_of(d)) == 0 for d in taps)
print(f"cây trợ năng: {co_cay}/249 bước click · {rong} bước rỗng nút", flush=True)
assert co_cay == 249 and rong == 0, "DỪNG: thiếu cây trợ năng ⇒ Voronoi chấm sai mà không báo"
```

## C5 — V1 trọn gói (ô foreground, ⛔ không bấm Stop)

Mỗi pha tự bỏ qua hoặc tự nối tiếp phần đã có, nên mất máy thì dựng lại C1 → C5 là chạy tiếp.

**Mất máy thì mất tối đa bao nhiêu:** câu nháp, sửa val, chấm ghi từng dòng ⇒ ≤ 5 phút (nhịp đồng bộ). Train lưu
`ckpt_last/` (adapter + optimizer) mỗi **20 bước tối ưu = 160 mẫu ≈ 18 phút** ⇒ ≤ ~23 phút. Cộng ~10–15 phút
dựng lại (chép + giải nén 3,4 GB từ Drive, cài gói, hoà S1 1,5 phút, nạp mô hình).

```python
DRF = f"{O}/drafts_train.jsonl"
NV = ["--n", "5"] if TEST else []
M = ["--n", "3"] if TEST else []

def cham(ten, pred):
    chay(["python", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", pred,
          "--data-root", f"{W}/c1data", "--recs-file", "c1_recs.jsonl", "--out", f"{O}/score_{ten}.json"] + M,
         f"{O}/cham_{ten}.log", cwd=WS)
    R = [json.loads(l) for l in open(f"{O}/score_{ten}_raw.jsonl")]
    print(f"== {ten}: {len(R)} bước · exec {sum(int(r['executable']) for r in R)}", flush=True)

t_bat_dau = time.time()
chay(T + ["--merge"], f"{O}/merge.log", nhip=30)
chay(T + ["--selftest", "--c1", C1_PATH, "--out", f"{O}/selftest"], f"{O}/selftest.log", nhip=10)
chay(T + ["--make-drafts", "--ckpt", CK500, "--out", DRF] + (["--n", "40"] if TEST else []), f"{O}/drafts.log")
if not os.path.exists(f"{O}/ed_gold/adapter_model.safetensors"):
    chay(T + ["--train-editor", "--drafts", DRF, "--crop", "gold", "--out", f"{O}/ed_gold", "--epochs", "1",
               "--save-every", "20"]
         + (["--max-steps", "5", "--log-every", "1"] if TEST else []), f"{O}/ed_gold.log")
for crop in ("gold", "neg"):
    chay(T + ["--edit-val", "--c1", C1_PATH, "--ck500-pred", PRED500, "--editor", f"{O}/ed_gold",
              "--crop", crop, "--out", f"{O}/pred_{crop}.jsonl"] + NV, f"{O}/edit_{crop}.log")
cham("k0_lai", f"{W}/c1preds/k0.jsonl")
for crop in ("gold", "neg"):
    cham(crop, f"{O}/pred_{crop}.jsonl")
dong_bo()
print(f"XONG V1 · {(time.time()-t_bat_dau)/3600:.2f} h · KIỂM (bản đủ): k0_lai 249 bước · exec 158", flush=True)
```

**Đọc trong log (lượt TEST gửi về các dòng này):**
- `selftest.log`: `[val C1] 400 bước · click 249 · … 233 (93.6%)` · `[train] 2554 …` · `✅ selftest ĐẠT`.
- `drafts.log`: `[nháp] N/N bước · greedy trùng câu người x%` — ghi lại x.
- `ed_gold.log`: `[mẫu đầu] nll vàng z` — **0,3–2 là đúng**, gần 0 hoặc > 5 là che nhãn sai ⇒ dừng, gửi log.
  Dòng `bước …` cho `s/mẫu` và `đỉnh VRAM`; lượt thật: nll vàng giảm dần, nll nhiễu cao hơn nll vàng sau vài
  trăm bước, không nan.
- `edit_gold.log`: `[edit-val gold] … đổi câu …% · … câu có dấu tiếng Việt 0`.
- `== k0_lai: 249 bước · exec 158` (lượt thật; L4 ra **157**, lệch ±1–2 là nhiễu T4 fp16 ↔ L4 bf16). Lệch hơn ⇒ dừng.

OOM ở train: thêm `"--accum", "16"` vào dòng `--train-editor`; vẫn OOM thì thử một lần `"--lam-ctr", "0"`.

**Chốt 2/10 sau lượt TEST (L4):** câu nháp 3,5 s/bước · train 6,7 s/mẫu · đỉnh VRAM 13,4 GiB · nll vàng mẫu
đầu 1,873. Hai epoch ra ~13,5 h ⇒ người dùng chọn **1 epoch** (PoC: chỉ để quyết có dùng TAGE không):
~2,5 h nháp + ~4,8 h train + ~1,5 h sửa val và chấm ≈ **8,5–9 h**. Bộ biên tập `none` ở C6 cũng phải 1 epoch
cho cùng số bước. V1 rơi vùng giữa thì có thể train tiếp epoch 2 từ `ed_gold/ckpt_last` (`--epochs 2`, xoá
`ed_gold/adapter_model.safetensors` ở gốc để ô không bỏ qua); khi đó lr nhảy lại vì lịch epoch 1 đã giảm về 0
— phải khai.

**Ước lượng lượt thật:** `s/mẫu` (lượt TEST) × 5.108 mẫu (2.554 × 2 epoch) cho pha train; câu nháp ≈
`s/bước` × 2.554. Tổng vượt ~10 h thì báo trợ lý trước khi chạy lượt thật.

## C5b — cổng V1 tự động + tự ngắt máy (xếp hàng sau C5, để chạy qua đêm)

Dán ô này vào một ô mới **ngay dưới C5**, bấm Shift+Enter **trong lúc C5 còn chạy**: Colab xếp hàng, C5 xong thì
tự chạy. ⛔ Không bấm Stop ô nào. Ô tính V1 đúng như `tage_doc.py` (exec gold, neg, gold+cổng với τ chọn chéo theo
episode), in một dòng `[V1 tự động] … ⇒ ĐI TIẾP / DỪNG TAGE / GIỮA HAI CỘT`, rồi **luôn** đồng bộ Drive, đẩy hết
lên cloud và **ngắt runtime** (`runtime.unassign()` = *Disconnect and delete runtime*) — kể cả khi ô lỗi. Người
dùng đọc dòng V1 rồi tự quyết có chạy C6 không (phiên mới: C1 → C4 rồi C6).

⚠️ Chỗ không tự ngắt được: **C5 lỗi** thì Colab thường huỷ ô đang xếp hàng ⇒ C5b không chạy, máy nằm không tới
khi Colab tự ngắt vì không tương tác (~90 phút theo kinh nghiệm dự án, chưa đo chính xác).

```python
import random
TAT_MAY = True    # False = giữ máy chạy, không tự ngắt

def tat_may(ly_do):
    print(f"⏹ {ly_do} — đồng bộ Drive rồi ngắt runtime" if TAT_MAY else f"⏹ {ly_do} (TAT_MAY=False, giữ máy)", flush=True)
    if not TAT_MAY:
        return
    try: dong_bo()
    except Exception as e: print("⚠️ đồng bộ lỗi:", e, flush=True)
    from google.colab import drive, runtime
    try: drive.flush_and_unmount()             # đẩy hết tệp lên cloud trước khi máy biến mất
    except Exception as e: print("⚠️ unmount lỗi:", e, flush=True)
    runtime.unassign()

def v1():
    nap = lambda p: {(d["episode_id"], d["step_id"]): d for d in map(json.loads, open(p, encoding="utf-8"))}
    C = nap(f"{W}/score_ck500_raw.jsonl"); K = sorted(C)
    ck = {k: int(C[k]["executable"]) for k in K}
    ex = {t: {k: int(v["executable"]) for k, v in nap(f"{O}/score_{t}_raw.jsonl").items()} for t in ("k0_lai", "gold", "neg")}
    assert not TEST and all(set(ex[t]) == set(K) for t in ex), "thiếu bước chấm"
    # ck500 chấm trên Kaggle T4 fp16, lượt này chấm L4 bf16 ⇒ k0_lai lệch ±1 bước là nhiễu dụng cụ (đo 3/10: 157)
    assert sum(ck.values()) == 165 and abs(sum(ex["k0_lai"].values()) - 158) <= 2, "dụng cụ chấm lệch"
    M = nap(f"{O}/pred_gold_meta.jsonl")
    g = {k: M[k]["lp_edit"] - M[k]["lp_draft"] for k in K}
    ep = sorted({k[0] for k in K}); random.Random(20261002).shuffle(ep); nua = {e: i % 2 for i, e in enumerate(ep)}
    ap_t = lambda KK, t: {k: (ex["gold"][k] if g[k] > t else ck[k]) for k in KK}
    xg = {}
    for h in (0, 1):
        chon = [k for k in K if nua[k[0]] == h]
        t = max(sorted({g[k] for k in chon} | {float("inf")}), key=lambda t: (sum(ap_t(chon, t).values()), t))
        xg.update(ap_t([k for k in K if nua[k[0]] != h], t))
    ck0, gold, neg, gc = sum(ck.values()), sum(ex["gold"].values()), sum(ex["neg"].values()), sum(xg.values())
    di = max(gold, gc) - ck0 >= 10 and gold - neg >= 10
    nhan = "ĐI TIẾP" if di else ("DỪNG TAGE" if gc <= ck0 + 2.49 else "GIỮA HAI CỘT, người dùng quyết")
    print(f"[V1 tự động] ck500 {ck0} · gold {gold} · gold+cổng {gc} · neg {neg} (trên 249) ⇒ {nhan}", flush=True)
    return di

try:
    DI_TIEP = v1()
except Exception as e:
    tat_may(f"C5b lỗi: {e!r}")
    raise
tat_may("xong V1, chờ người dùng quyết C6")     # kết quả nào cũng ngắt máy
```

## Chạy

1. `TEST = True`: chạy C1 → C5, khoảng 30–45 phút. Gửi về output C2, C5 (các dòng ở trên).
2. Ổn thì sửa C2 `TEST = False`, chạy C2 → C5 (C1 không cần chạy lại nếu chưa mất máy; `s1_merged` đã có nên
   bước hoà bỏ qua). Có thể để máy chạy, nhưng giữ tab mở — ô C5 phải sống.
3. Mất máy giữa chừng: kết nối lại → C1 → C5 với `TEST = False`. C2 kéo `that/` từ Drive về; câu nháp, train
   (điểm lưu mỗi 50 bước), sửa val và chấm đều nối tiếp.
4. Xong: tải `MyDrive/thesis/tage/out/that/` về **`runs/tage_val/that/`** trên máy nhà (bỏ thư mục `ed_gold/`,
   `selftest/` nếu muốn nhẹ). Rồi `python3 harness/tage_doc.py` → dòng `[V1] …`.
5. **Ngắt runtime** khi xong (*Runtime → Disconnect and delete runtime*) để không tốn đơn vị chạy không.

## C6 — V2 + V3 (chỉ khi V1 ĐI TIẾP)

Cùng phiên hoặc phiên mới (C1 → C4, `TEST = False`), rồi ô này (foreground). Ước lượng L4 ~7 h.

```python
import re
assert globals().get("DI_TIEP", True), "V1 không ĐI TIẾP — không chạy C6"   # phiên mới chạy tay thì bỏ qua
TAT_MAY = True    # C6 xong hoặc lỗi thì đồng bộ Drive rồi ngắt runtime; False = giữ máy

def tat_may(ly_do):
    print(f"⏹ {ly_do} — đồng bộ Drive rồi ngắt runtime" if TAT_MAY else f"⏹ {ly_do} (TAT_MAY=False, giữ máy)", flush=True)
    if not TAT_MAY:
        return
    try: dong_bo()
    except Exception as e: print("⚠️ đồng bộ lỗi:", e, flush=True)
    from google.colab import drive, runtime
    try: drive.flush_and_unmount()
    except Exception as e: print("⚠️ unmount lỗi:", e, flush=True)
    runtime.unassign()

def c6():
    LV = ["--max-steps", "5"] if TEST else []
    if not os.path.exists(f"{O}/ed_none/adapter_model.safetensors"):
        chay(T + ["--train-editor", "--drafts", DRF, "--crop", "none", "--out", f"{O}/ed_none", "--epochs", "1",
                   "--save-every", "20"] + LV,
             f"{O}/ed_none.log")
    if not os.path.exists(f"{O}/loc_g/adapter_model.safetensors"):
        chay(T + ["--train-locator", "--out", f"{O}/loc_g", "--epochs", "1", "--save-every", "20"] + LV, f"{O}/loc_g.log")
    if not os.path.exists(f"{O}/loc_d/adapter_model.safetensors"):
        chay(T + ["--train-locator", "--drafts", DRF, "--with-draft", "--out", f"{O}/loc_d", "--epochs", "1",
                   "--save-every", "20"] + LV, f"{O}/loc_d.log")
    for v, x in (("g", []), ("d", ["--with-draft"])):
        chay(T + ["--locate-val", "--c1", C1_PATH, "--ck500-pred", PRED500, "--locator", f"{O}/loc_{v}",
                  "--ck500-score", f"{W}/score_ck500_raw.jsonl", "--out", f"{O}/loc_val_{v}.jsonl"] + x + NV,
             f"{O}/loc_val_{v}.log")
    hit = {v: int(re.findall(r"trỏ sai: (\d+)", open(f"{O}/loc_val_{v}.log").read())[-1]) for v in ("g", "d")}
    LOC = f"{O}/loc_val_{max(hit, key=hit.get)}.jsonl"
    print("trúng trên 80 bước trỏ sai:", hit, "→ dùng", LOC, flush=True)
    chay(T + ["--edit-val", "--c1", C1_PATH, "--ck500-pred", PRED500, "--editor", f"{O}/ed_gold",
              "--crop", "pred", "--points", LOC, "--out", f"{O}/pred_pred.jsonl"] + NV, f"{O}/edit_pred.log")
    chay(T + ["--edit-val", "--c1", C1_PATH, "--ck500-pred", PRED500, "--editor", f"{O}/ed_none",
              "--crop", "none", "--out", f"{O}/pred_none.jsonl"] + NV, f"{O}/edit_none.log")
    cham("ck500_l4", PRED500)               # mốc ck500 chấm lại cùng môi trường L4, để so công bằng
    for ten in ("pred", "none"):
        cham(ten, f"{O}/pred_{ten}.jsonl")
    dong_bo()

try:
    c6()
except Exception as e:                       # bước nào lỗi cũng ngắt máy (Stop tay thì không)
    tat_may(f"C6 lỗi: {e!r}")
    raise
print("XONG C6", flush=True)
tat_may("XONG C6")
```

Tải lại `out/that/` về `runs/tage_val/that/`, chạy `tage_doc.py` → `[V2]`, `[V3]`.

## Dừng và gửi log khi

selftest không đạt · `k0_lai` ≠ 249 bước / exec 158 · nll vàng mẫu đầu ngoài 0,3–2 · nan · OOM sau hai lần
thử · mã thoát ≠ 0 · bộ biên tập đổi 0% hoặc > 90% câu val, câu tiếng Việt, dài bất thường, lặp · bộ định vị
không đọc được toạ độ ở > 30% bước.
