# TAGE — kiểm thử trên val C1 (file 265, 2/10/2026)

Thiết kế, ngưỡng và lý do: `harness/tai_lieu_2026-10-02/265_ACTION_KIEM_THU_TAGE_VAL_2_10_checked.md`.
Runbook này chỉ là các ô chạy. ⚠️ Lượt 2/10 chạy bằng **`harness/colab_tage_val_l4.md`** (Kaggle hết hạn
mức); bản này giữ cho lượt sau. **Số ra là số val — không trích vào luận văn.**

## Máy (thủ tục chọn máy, CLAUDE.md)

| pha | việc | máy | ước lượng T4 (chưa đo) |
|---|---|---|---|
| selftest · `tage_neg.jsonl` · `tage_doc.py` | không gọi GPU | CPU / máy nhà | giây |
| A `nhap` | câu nháp ck500 cho ~2.554 bước click train (greedy + 2 mẫu) | **Kaggle T4, 0 đồng** | 3–4 h |
| B `bientap` | train bộ biên tập `gold`, 2 epoch, hai lượt forward/mẫu | Kaggle T4 | 6–8 h |
| C `suaval` | sửa 249 bước val (gold, neg) + chấm UGround 3 tệp | Kaggle T4 | ~2 h |

Ba pha cộng lại vượt trần 12 h của một phiên ⇒ **ba commit nối nhau**, mỗi commit gắn Output của commit
trước làm input (Ô 2 tự chép sang). Lượt `TEST = True` in `s/mẫu` và `s/bước` thật — nếu B đo ra > 10 h
trên T4 thì báo trợ lý trước khi bấm, cân L4 theo luật 1,5×.

## Chuẩn bị (máy nhà → Kaggle)

1. Dataset mới **`tage-val-script`** (Private): kéo cả 6 tệp trong `_bundles/tage-val-script/`.

   | tệp | md5 |
   |---|---|
   | `tage_val.py` | `e15f9d524ab307349498f2ca3ebcbc68` |
   | `grpo_spice.py` | `07ea87b6d156d1faa391a4274dffd7cf` |
   | `build_branch_data.py` | `619e63e123a6dbf60086e65ee94a3912` |
   | `tage_neg.jsonl` (41.099 dòng, dựng bằng `harness/tage_neg_build.py`) | `75539cdc533ecaa578d6067e3fbcd8a5` |
   | `pred_ck500.jsonl` (400 câu ck500 trên val C1) | `eb6162d86730a936beb5ae5a9fd6d652` |
   | `score_ck500_raw.jsonl` (để bộ định vị in số trên 80 bước trỏ sai) | `258ced11cad3b6729bbdb25f947dbe78` |

2. Notebook mới, **GPU T4** (một card là đủ), **Internet On**. *Add Input*: `fgrb-p1-bundle` · `c1-exec8` ·
   `thesis-val-cham` · `grpo-spice-ck500` · `tage-val-script`. Từ commit thứ hai: thêm **Output của commit
   trước**.

## Ô 1 — gói

```python
import subprocess, sys, os, time
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode

sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes pillow 2>&1 | tail -3")
sh(f'{sys.executable} -c "import transformers, peft, torch; print(transformers.__version__, peft.__version__, torch.__version__, torch.cuda.get_device_name(0))"')
```

Nếu peft báo `incompatible version of torchao`: *Restart session* rồi chạy từ Ô 2.

## Ô 2 — đường dẫn, md5, chép kết quả commit trước

```python
import os, glob, shutil, hashlib, json
TEST = True                    # chạy thử tương tác; đổi False trước khi commit
PHA = ["nhap"]                 # commit 1: ["nhap"] · commit 2: ["bientap"] · commit 3: ["suaval"]
                               # TEST = True thì chạy cả ba bản nhỏ trong một phiên

W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
if TEST:
    PHA = ["nhap", "bientap", "suaval"]
O = f"{W}/thu" if TEST else f"{W}/that"
os.makedirs(O, exist_ok=True)

BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "images" in d)
C1_PATH = [p for p in glob.glob("/kaggle/input/**/c1_mau.jsonl", recursive=True)]
assert len(C1_PATH) == 1 and md5(C1_PATH[0]) == "d757554326977309c3a65ae0b144c211", f"DỪNG: c1_mau.jsonl {C1_PATH}"
C1_PATH = C1_PATH[0]

S = glob.glob("/kaggle/input/**/tage_val.py", recursive=True)
assert len(S) == 1, f"DỪNG: cần đúng một tage_val.py, thấy {S}"
SD = os.path.dirname(S[0])
MD = {"tage_val.py": "e15f9d524ab307349498f2ca3ebcbc68", "grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf",
      "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912", "tage_neg.jsonl": "75539cdc533ecaa578d6067e3fbcd8a5",
      "pred_ck500.jsonl": "eb6162d86730a936beb5ae5a9fd6d652", "score_ck500_raw.jsonl": "258ced11cad3b6729bbdb25f947dbe78"}
for f, h in MD.items():
    shutil.copy(os.path.join(SD, f), f"{W}/{f}")
    assert md5(f"{W}/{f}") == h, f"DỪNG: {f} lệch bản máy nhà (New Version dataset tage-val-script)"
NEG, PRED500, MERGED = f"{W}/tage_neg.jsonl", f"{W}/pred_ck500.jsonl", f"{W}/s1_merged"

def la_grpo(d):
    c = os.path.join(d, "adapter_config.json")
    return os.path.exists(c) and "s1_merged" in json.load(open(c)).get("base_model_name_or_path", "")
CK = [os.path.dirname(f) for f in glob.glob("/kaggle/input/**/adapter_model.safetensors", recursive=True)
      if la_grpo(os.path.dirname(f)) and "/that/" not in f and "/thu/" not in f]
if len(CK) > 1:
    CK = [d for d in CK if d.rstrip("/").endswith("checkpoint-500")]
assert len(CK) == 1, f"DỪNG: cần đúng một adapter ck500, thấy {CK}"
CK500 = CK[0]
assert md5(f"{CK500}/adapter_model.safetensors") == "491fa6677340393f1e4464c08a0cec98", "DỪNG: không phải ck500 đã chấm"

# commit trước: Output có thư mục that/ ⇒ chép vào O (không đè tệp đã có)
if not TEST:
    for p in glob.glob("/kaggle/input/**/that/drafts_train.jsonl", recursive=True):
        shutil.copytree(os.path.dirname(p), O, dirs_exist_ok=True)
        print("chép kết quả commit trước từ", os.path.dirname(p))
print("có sẵn trong", O, ":", sorted(os.listdir(O)))
print("BUNDLE", BUNDLE, "\nC1", C1_PATH, "\nCK500", CK500, "\nPHA", PHA, "· TEST", TEST, flush=True)
```

Phải thấy đủ đường dẫn, không dòng `DỪNG`. Ở commit 2 và 3, dòng `có sẵn` phải liệt kê `drafts_train.jsonl`
(commit 3 thêm `ed_gold`).

## Ô 3 — hàm chạy có nhịp sống, hoà S1, selftest

```python
def chay(cmd, log, cwd=None, nhip=120):
    t0 = time.time()
    with open(log, "a") as f:
        q = subprocess.Popen(cmd, cwd=cwd or W, stdout=f, stderr=subprocess.STDOUT,
                             env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
                                  "PYTHONUNBUFFERED": "1"})
        while q.poll() is None:
            time.sleep(30 if TEST else nhip)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"  {(time.time()-t0)/60:6.1f} phút · {os.path.basename(log)} · {L[-1][:120] if L else '...'}", flush=True)
    print(f"--- {os.path.basename(log)} · mã thoát {q.returncode} · {(time.time()-t0)/60:.1f} phút ---")
    print("".join(open(log, errors="ignore").readlines()[-8:]), flush=True)
    assert q.returncode == 0, f"DỪNG: xem {log}"

T = ["python", "tage_val.py", "--bundle", BUNDLE, "--merged", MERGED, "--neg", NEG]
chay(T + ["--merge"], f"{O}/merge.log", nhip=30)
chay(T + ["--selftest", "--c1", C1_PATH, "--out", f"{O}/selftest"], f"{O}/selftest.log", nhip=10)
```

Phải thấy `[val C1] 400 bước · click 249 · có phần tử lân cận cùng vai 233 (93.6%)`,
`[train] 2554 bước click …` và `✅ selftest ĐẠT`. Mở vài ảnh `selftest/*_gold.png`: phần tử đích ở tâm;
`*_neg.png` là phần tử khác.

## Ô 4 — pha A `nhap`: câu nháp train

```python
DR = f"{O}/drafts_train.jsonl"
if "nhap" in PHA:
    chay(T + ["--make-drafts", "--ckpt", CK500, "--out", DR] + (["--n", "40"] if TEST else []), f"{O}/drafts.log")
```

Kiểm `drafts.log`: dòng `[nháp] N/N bước · greedy trùng câu người x% · greedy rỗng …` — ghi lại x.
Nối tiếp được: commit bị cắt thì commit sau chạy lại ô này, tự bỏ bước đã có.

## Ô 5 — pha B `bientap`: bộ biên tập `gold`

```python
if "bientap" in PHA:
    chay(T + ["--train-editor", "--drafts", DR, "--crop", "gold", "--out", f"{O}/ed_gold"]
         + (["--max-steps", "5", "--log-every", "1"] if TEST else []), f"{O}/ed_gold.log")
```

Kiểm `ed_gold.log`:
- `[LoRA editor/gold] r=16 · tham số học …` (khác 0; script tự dừng nếu tháp thị giác học).
- `[epoch 0] … câu nháp làm hỏng y%` — kỳ vọng quanh 0,3 × tỉ lệ làm hỏng được (selftest đo trên câu người
  là 43,8% ⇒ ~13%).
- `[mẫu đầu] nll vàng z nat/token` — **0,3–2 là đúng**; gần 0 hoặc > 5 là che nhãn sai ⇒ dừng, gửi log.
- các dòng `bước …`: nll vàng giảm dần; nll nhiễu cao hơn nll vàng sau vài trăm bước; không nan.
  Ghi lại `s/mẫu` và `đỉnh VRAM` ở dòng cuối.

Lưu `ckpt_last/` mỗi 50 bước (kèm optimizer) ⇒ commit bị cắt thì commit sau chạy lại ô này, tự tiếp.
OOM: thêm `"--accum", "16"`, vẫn OOM thì thử một lần `"--lam-ctr", "0"`, vẫn OOM thì gửi về.

## Ô 6 — pha C `suaval`: sửa val với vùng vàng và vùng nhiễu

```python
NV = ["--n", "5"] if TEST else []
if "suaval" in PHA:
    for crop in ("gold", "neg"):
        chay(T + ["--edit-val", "--c1", C1_PATH, "--ck500-pred", PRED500, "--editor", f"{O}/ed_gold",
                  "--crop", crop, "--out", f"{O}/pred_{crop}.jsonl"] + NV, f"{O}/edit_{crop}.log")
```

Kiểm `edit_gold.log`: `[edit-val gold] 249 bước click · đổi câu …% · số từ trung vị … · câu có dấu tiếng
Việt 0`. Đổi 0% hoặc > 90% câu, câu tiếng Việt, câu dài bất thường ⇒ dừng, gửi về.

## Ô 7 — dựng dữ liệu chấm (nguyên văn Ô 5 của `kaggle_grpo_spice_pha3_ck500.md`)

```python
import os, glob, json, shutil, hashlib, sys
cand = sorted({os.path.dirname(p) for p in glob.glob("/kaggle/input/**/c1_picks.json", recursive=True)
               if os.path.exists(os.path.join(os.path.dirname(p), "c1_mau.jsonl"))})
assert len(cand) == 1, f"DỪNG: cần đúng một gói c1-exec8, thấy {cand}"
PK = cand[0]
assert hashlib.md5(open(f"{PK}/c1_mau.jsonl", "rb").read()).hexdigest() == "d757554326977309c3a65ae0b144c211"
WS = f"{W}/pk/thesis"
shutil.copytree(f"{PK}/thesis", WS, dirs_exist_ok=True)
sr = open(f"{WS}/harness/score_run.py", encoding="utf-8").read()
assert "--recs-file" in sr and "TỆP THÔ KHÔNG KHỚP" in sr, "DỪNG: score_run.py là bản cũ"

v600 = sorted(glob.glob("/kaggle/input/**/val_cham600.jsonl", recursive=True), key=len)
v600 = [p for p in v600 if all(os.path.exists(os.path.join(os.path.dirname(p), f))
                                for f in ("val_cham400.jsonl", "ocr.jsonl", "images"))]
assert v600, "DỪNG: không thấy thư mục thesis-val-cham đủ bộ (val_cham400 · ocr · images)"
h = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
for f in ("val_cham400.jsonl", "val_cham600.jsonl", "ocr.jsonl"):
    assert len({h(os.path.join(os.path.dirname(p), f)) for p in v600}) == 1, f"DỪNG: các bản thesis-val-cham lệch nhau ở {f}"
BASE = os.path.dirname(v600[0])

C1 = [json.loads(l) for l in open(f"{PK}/c1_mau.jsonl", encoding="utf-8")]
assert len(C1) == 400
TAPT = ("click", "long_press")
KEYS = {(r["episode_id"], r["step_id"]) for r in C1}
VD = f"{W}/c1data"
os.makedirs(VD, exist_ok=True)
recs = {}
for f in ("val_cham400.jsonl", "val_cham600.jsonl"):
    for d in map(json.loads, open(f"{BASE}/{f}", encoding="utf-8")):
        k = (d["episode_id"], d["step_id"])
        if k in KEYS and k not in recs:
            d.setdefault("gold_instruction", d["target_instruction"])
            recs[k] = d
assert len(recs) == 400, f"DỪNG: chỉ ghép được {len(recs)}/400 bước C1"
with open(f"{VD}/c1_recs.jsonl", "w", encoding="utf-8") as fo:
    for r in C1:
        fo.write(json.dumps(recs[(r["episode_id"], r["step_id"])], ensure_ascii=False) + "\n")
shutil.copy(f"{BASE}/ocr.jsonl", f"{VD}/ocr.jsonl")
if os.path.lexists(f"{VD}/images"):
    os.remove(f"{VD}/images")
os.symlink(f"{BASE}/images", f"{VD}/images")
taps = [d for d in recs.values() if d["action"].get("action_type") in TAPT and "x" in d["action"]]
assert len(taps) == 249 and all(os.path.exists(f"{VD}/{d['image']}") for d in taps)

PD = f"{W}/c1preds"
os.makedirs(PD, exist_ok=True)
with open(f"{PD}/k0.jsonl", "w", encoding="utf-8") as fo:
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

## Ô 8 — chấm V1

```python
M = ["--n", "3"] if TEST else []

def cham(ten, pred):
    cmd = ["python", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", pred,
           "--data-root", f"{W}/c1data", "--recs-file", "c1_recs.jsonl", "--out", f"{O}/score_{ten}.json"] + M
    chay(cmd, f"{O}/cham_{ten}.log", cwd=f"{W}/pk/thesis")
    R = [json.loads(l) for l in open(f"{O}/score_{ten}_raw.jsonl")]
    print(f"== {ten}: {len(R)} bước · exec {sum(int(r['executable']) for r in R)}", flush=True)

if "suaval" in PHA:
    cham("k0_lai", f"{W}/c1preds/k0.jsonl")
    for crop in ("gold", "neg"):
        cham(crop, f"{O}/pred_{crop}.jsonl")
    print("KIỂM (bản đủ): k0_lai phải 249 bước · exec 158. Lệch thì dừng, gửi về.")
```

## Ô cuối — dọn trước khi commit kết thúc

```python
import shutil
for d in (MERGED, f"{W}/pk", f"{W}/c1data"):      # s1_merged ~7 GB: không để vào Output, commit sau hoà lại (~5 phút)
    shutil.rmtree(d, ignore_errors=True)
print("Output:", sorted(os.listdir(W)), "·", O, sorted(os.listdir(O)), flush=True)
```

## Chạy

1. **Thử tương tác** (`TEST = True`): *Run All*, khoảng 30–45 phút. Gửi về output Ô 2, 3, 5, 6, 8 (đặc biệt
   dòng `[mẫu đầu] nll vàng`, `s/mẫu`, `s/bước`, `đỉnh VRAM`).
2. Ổn thì commit 1: Ô 2 `TEST = False`, `PHA = ["nhap"]` → *Stop session* → *Save Version → Save & Run All*.
3. Commit 2: thêm input = Output commit 1; `PHA = ["bientap"]`. Commit 3: thêm Output commit 2 (Output này đã
   chứa lại mọi thứ của commit 1); `PHA = ["suaval"]`.
4. Tải `that/` của commit 3 về **`runs/tage_val/that/`**: `score_{k0_lai,gold,neg}_raw.jsonl` ·
   `pred_{gold,neg}.jsonl` · `pred_{gold,neg}_meta.jsonl` · mọi `.log` · `drafts_train.jsonl`. Thư mục
   `ed_gold/` (adapter ~70 MB) giữ trên Kaggle, chỉ tải khi đi tiếp V2/V3.
5. Máy nhà: `python3 harness/tage_doc.py` → dòng `[V1] …`. **Chỉ chạy Ô 9 khi V1 ĐI TIẾP** (hoặc người dùng
   quyết đi tiếp ở vùng giữa).

## Ô 9 — V2 + V3 (sau V1): bộ biên tập `none`, hai bộ định vị, nhánh `pred`

Một commit mới (input: Output commit 3), chạy Ô 1–3 và Ô 7, rồi ô này. Ước lượng T4 8–12 h ⇒ nếu dòng
`s/mẫu` của pha B cho thấy vượt 11 h thì tách làm hai commit (bộ biên tập `none` riêng).

```python
chay(T + ["--train-editor", "--drafts", DR, "--crop", "none", "--out", f"{O}/ed_none"]
     + (["--max-steps", "5"] if TEST else []), f"{O}/ed_none.log")
chay(T + ["--train-locator", "--out", f"{O}/loc_g"] + (["--max-steps", "5"] if TEST else []), f"{O}/loc_g.log")
chay(T + ["--train-locator", "--drafts", DR, "--with-draft", "--out", f"{O}/loc_d"]
     + (["--max-steps", "5"] if TEST else []), f"{O}/loc_d.log")
for v, x in (("g", []), ("d", ["--with-draft"])):
    chay(T + ["--locate-val", "--c1", C1_PATH, "--ck500-pred", PRED500, "--locator", f"{O}/loc_{v}",
              "--ck500-score", f"{W}/score_ck500_raw.jsonl", "--out", f"{O}/loc_val_{v}.jsonl"] + x + NV,
         f"{O}/loc_val_{v}.log")

# chọn bộ định vị trúng nhiều hơn trên 80 bước ck500 trỏ sai (dòng [locate-val] … trỏ sai: n)
import re
hit = {v: int(re.findall(r"trỏ sai: (\d+)", open(f"{O}/loc_val_{v}.log").read())[-1]) for v in ("g", "d")}
LOC = f"{O}/loc_val_{max(hit, key=hit.get)}.jsonl"
print("trúng trên bước trỏ sai:", hit, "→ dùng", LOC, flush=True)

chay(T + ["--edit-val", "--c1", C1_PATH, "--ck500-pred", PRED500, "--editor", f"{O}/ed_gold",
          "--crop", "pred", "--points", LOC, "--out", f"{O}/pred_pred.jsonl"] + NV, f"{O}/edit_pred.log")
chay(T + ["--edit-val", "--c1", C1_PATH, "--ck500-pred", PRED500, "--editor", f"{O}/ed_none",
          "--crop", "none", "--out", f"{O}/pred_none.jsonl"] + NV, f"{O}/edit_none.log")
for ten in ("pred", "none"):
    cham(ten, f"{O}/pred_{ten}.jsonl")
```

Tải thêm về `runs/tage_val/that/`: `score_{pred,none}_raw.jsonl` · `pred_{pred,none}_meta.jsonl` ·
`loc_val_{g,d}.jsonl` · mọi `.log`. Máy nhà chạy lại `tage_doc.py` → dòng `[V2]`, `[V3]`.

## Dừng và gửi log khi

- selftest không đạt; click val ≠ 249; phần tử lân cận phủ < 60%.
- `k0_lai` không ra 249 bước · exec 158.
- `nll vàng` mẫu đầu ngoài 0,3–2; nan; OOM sau hai lần thử ở Ô 5; mã thoát ≠ 0; `AssertionError`.
- Bộ biên tập đổi 0% hoặc > 90% câu val; câu tiếng Việt, dài bất thường, lặp.
- Bộ định vị không đọc được toạ độ ở > 30% bước (script tự dừng).
