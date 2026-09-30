# 251 — Chấm `exec` cho câu greedy và 8 mẫu S1 trên 249 bước click của C1 — Kaggle T4×2, dạng COMMIT (28/9/2026)

Không train, không sửa trọng số, không sinh câu mới. Chỉ cho UGround-V1-2B bấm theo 9 câu đã có
trên mỗi bước click (1 greedy + 8 mẫu S1 trong `runs/c1/c1_mau.jsonl`), rồi chấm đúng luật `exec`
của luận văn. **2.241 lượt bộ trỏ = 249 × 9**, ước ~1,5–2 h trên T4×2 (+5–10 phút tải model và cây
trợ năng), 0 đồng. Không đụng tập test.

Nguồn: chép từ 6 ảnh (ảnh gốc ở `harness/tai_lieu_2026-09-28/anh_goc_251/anh1.jpg … anh6.jpg`). Bản này **sắp xếp lại
để chạy commit** và sửa năm chỗ của bản chép từ ảnh, xem §0.

Thay mục 5 của `250_DEBATE_VA_CHOT_PHUONG_PHAP_28_9.md`: bản đó chỉ `--recs-file val400.jsonl`,
sai, vì `val400.jsonl` chỉ chứa 62/249 bước click của C1. 400 bước C1 lấy từ 1.567 bước val của
`thesis_val_cham` (ghép `val_cham400.jsonl` + `val_cham600.jsonl` ra đủ 400/400 bước, 249/249 click).

---

## 0. Đã sửa so với bản chép từ ảnh (kiểm trên WSL 28/9, 0 GPU)

| # | chỗ | bản ảnh | đã làm |
|---|---|---|---|
| 1 | chuỗi `PICKS` ở Ô 4 | chép tay ra **398** ký tự ⇒ `assert len(PICKS) == 400` chết sau ~2 h GPU | **tính lại trên CPU** bằng `harness/c1_oracle_spice.py` → `runs/c1/c1_picks.json`. Khớp tuyệt đối mọi số của file gốc: SPICE greedy/oracle **57,30 / 75,13** (400 bước) và **48,62 / 71,13** (249 click), đổi câu **150/400** và **119/249**. Notebook đọc chuỗi từ tệp, không chép tay nữa |
| 2 | `assert` "mọi mẫu khác rỗng" ở Ô 2 | áp cho cả 400 bước ⇒ **chết ngay**: có 5 mẫu rỗng | 5 mẫu rỗng đều ở bước **không click** (4930/0, 13390/0, 6403/0 `open_app`; 7463/0 `navigate_back`) nên không vào phép chấm. `assert` nay chỉ áp cho bước click |
| 3 | gói mã | dựa vào một dataset `thesis-pata` "bản mới nhất", không rõ có cờ `--data-root/--recs-file` chưa | đóng gói riêng `c1-exec8` gồm `score_run.py` · `metric_exec.py` · `a11y_inventory.py` bản hiện hành + `c1_mau.jsonl` + `c1_picks.json`, kèm md5 để notebook tự kiểm |
| 4 | tải model và cây trợ năng | hai tiến trình GPU cùng tải một lúc | tải **một lần** ở Ô 2, rồi kiểm cây trợ năng phủ **249/249** bước click (đo trên WSL: 249/249, trung vị 72 nút/màn, 0 bước rỗng nút). Thiếu cây thì Voronoi chấm sai mà không báo |
| 5 | `pip install -U bitsandbytes peft` | có | bỏ: UGround chỉ cần `transformers`, không dùng hai gói này. Giữ `pip uninstall torchao` như bản gốc |

Thêm cho commit: một lượt **thử 3 bước tự động** trước lượt đủ (hỏng thì commit dừng sau vài
phút, không phải sau 2 h), nhịp sống mỗi 2 phút trong chính ô chạy, và mọi điều kiện "chỉ đi tiếp
khi…" của bản gốc đổi thành `assert` để commit tự dừng.

---

## 1. Câu hỏi phải trả lời

Trên 249 bước click của C1:

1. `exec` của câu greedy S1.
2. `exec` của câu oracle SPICE chọn: trong 9 câu (greedy + 8 mẫu), câu có SPICE từng câu cao
   nhất so với câu chuẩn (hoà thì lấy greedy). Lựa chọn đã tính sẵn trên CPU ở `c1_picks.json`.
3. `exec` của từng mẫu `k = 1..8`, và tỉ lệ bước có ít nhất một câu bấm trúng.

Số đã có từ CPU (tái lập 28/9 bằng `c1_oracle_spice.py`):

| | SPICE, 400 bước | SPICE, 249 bước click |
|---|---:|---:|
| Greedy | 57,30 | 48,62 |
| Oracle SPICE | 75,13 | 71,13 |

⚠️ Đây là **val**, S1 đã thấy lúc train. **Không trích số nào ra luận văn.**

---

## 2. Máy nhà (WSL) — đóng gói, 1 lệnh

```bash
cd /mnt/d/Master/Thesis && python3 harness/make_c1_exec8.py
```

Lệnh này (0 GPU, vài giây):
- tạo `_bundles/c1_exec8.zip` (~60 KB): `c1_mau.jsonl` · `c1_picks.json` ·
  `thesis/harness/{score_run,metric_exec,a11y_inventory}.py`;
- tạo `_bundles/c1_exec8.ipynb`: notebook có đúng 5 ô ở §4, sinh thẳng từ file này (một nguồn,
  không lệch).

Kiểm dòng cuối in ra: `md5 c1_mau.jsonl = d757554326977309c3a65ae0b144c211`.

---

## 3. Kaggle — từng bước

**Bước 1. Upload dataset mới.** kaggle.com → *Datasets* → *New Dataset* → kéo `_bundles/c1_exec8.zip`
vào → tên **`c1-exec8`** → *Create*. Kaggle tự giải nén zip, không cần làm gì thêm.

**Bước 2. Tạo notebook từ tệp.** *Code* → *New Notebook* → menu *File* → *Import Notebook* → chọn
`_bundles/c1_exec8.ipynb`. Notebook phải có **đúng 5 ô code** (Ô 1 … Ô 5). Xoá mọi ô trống mặc định
nếu Kaggle tự thêm.

**Bước 3. Add Input hai dataset** (khung bên phải → *Add Input*):
- `thesis-val-cham` (đã có sẵn: `images/` 1.567 ảnh, `val_cham400.jsonl`, `val_cham600.jsonl`,
  `ocr.jsonl`). ⛔ Không dùng `thesis-val` cũ thay được: nó thiếu `val_cham600.jsonl`.
- `c1-exec8` (vừa tạo ở bước 1).

⚠️ Không gắn thêm dataset nào khác có `c1_picks.json` hay `val_cham600.jsonl` — Ô 2 đòi đúng một bản.

**Bước 4. Settings** (khung bên phải → *Session options*):
- *Accelerator* **GPU T4 x2**
- *Internet* **ON** (bắt buộc: tải UGround-V1-2B và `all_forest_dict.zip` từ HuggingFace)
- *Persistence* để mặc định.

Commit chạy theo cấu hình **đã lưu** của notebook, nên chỉnh xong mới bấm bước 5.

**Bước 5. Commit.** Góc phải trên → *Save Version* → chọn **Save & Run All (Commit)** → *Save*.
Có thể tắt máy / gập máy đi ngủ; lượt chạy nằm trên máy Kaggle.

**Bước 6. Theo dõi (không bắt buộc).** *Your Work* → notebook → version đang chạy → *Logs*.
Mốc cần thấy, theo thứ tự:

| lúc | dòng log | nếu không thấy |
|---|---|---|
| ~1 phút | `NGPU = 2` | 1 GPU vẫn chạy được, chỉ chậm gấp đôi (~3–4 h) |
| ~5–10 phút | `bước C1: 400 | click: 249 | ảnh thiếu: 0` rồi `cây trợ năng: 249/249 bước click · 0 bước rỗng nút` | commit tự dừng ở `assert` — xem §5 |
| ~10–15 phút | `THỬ 3 BƯỚC: ĐẠT` | tự dừng, gửi `thu.log` |
| từ đó, mỗi 2 phút | `HH:MM - 0.35 h - k0:40/249 k1:38/249 …` | **sau 15 phút mọi bộ đếm vẫn 0** ⇒ *Cancel* commit, xem §5 |
| ~1,5–2 h | `mã thoát: [0, 0]` rồi JSON tổng hợp | xem §5 |

**Bước 7. Tải kết quả.** Version xong (trạng thái *Complete*) → tab **Output** → tải
`c1_exec_8mau.zip` (và `c1_exec_tong.json` nếu muốn xem nhanh). Đặt vào **`runs/c1/exec8/`**
trong kho (luật đọc kết quả của `runs/README.md`: tệp Kaggle đặt thẳng vào thư mục của phép đo),
rồi giải nén tại chỗ.

**Bước 8. Gửi lại chat nhà:** nguyên JSON cuối log (chính là `c1_exec_tong.json`) + hai dòng cuối
mỗi `cham_gpu*.log` (có trong zip). Chưa tự diễn giải, chưa train gì.

---

## 4. Năm ô của notebook (commit)

`make_c1_exec8.py` chép nguyên văn năm khối code dưới đây vào `c1_exec8.ipynb`. Sửa ô nào thì sửa
ở đây rồi chạy lại lệnh §2.

### Ô 1 — gỡ torchao, kiểm GPU

```python
import os, subprocess, sys
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"   # tqdm ngoài terminal làm ngập log, từng treo commit 7 h
os.environ["TQDM_DISABLE"] = "1"
subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "-q", "torchao"])
r = subprocess.run([sys.executable, "-c",
    "import torch, transformers; print('torch', torch.__version__, '| transformers', transformers.__version__, "
    "'| GPU', [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])"],
    capture_output=True, text=True)
print(r.stdout, r.stderr[-1500:], flush=True)
import torch
NGPU = torch.cuda.device_count()
assert NGPU >= 1, "DỪNG: không thấy GPU — Settings → Accelerator → GPU T4 x2"
print("NGPU =", NGPU, flush=True)
```

### Ô 2 — gói mã, 400 bản ghi, 9 tệp câu, tải trước model + cây trợ năng

```python
import os, glob, json, shutil, hashlib, sys
W = "/kaggle/working"

# gói c1-exec8: nhận bằng cặp c1_picks.json + c1_mau.jsonl đứng cạnh nhau
cand = sorted({os.path.dirname(p) for p in glob.glob("/kaggle/input/**/c1_picks.json", recursive=True)
               if os.path.exists(os.path.join(os.path.dirname(p), "c1_mau.jsonl"))})
assert len(cand) == 1, f"DỪNG: cần đúng một gói c1-exec8, thấy {cand}"
PK = cand[0]
md5 = hashlib.md5(open(f"{PK}/c1_mau.jsonl", "rb").read()).hexdigest()
assert md5 == "d757554326977309c3a65ae0b144c211", f"DỪNG: c1_mau.jsonl lệch bản máy nhà ({md5})"
WS = f"{W}/pk/thesis"
shutil.copytree(f"{PK}/thesis", WS, dirs_exist_ok=True)
sr = open(f"{WS}/harness/score_run.py", encoding="utf-8").read()
assert "--recs-file" in sr and "TỆP THÔ KHÔNG KHỚP" in sr, "DỪNG: score_run.py là bản cũ"
PICKS = json.load(open(f"{PK}/c1_picks.json", encoding="utf-8"))["picks"]
assert len(PICKS) == 400 and set(PICKS) <= set("012345678"), len(PICKS)

# dữ liệu val: mọi tệp lấy theo thư mục của val_cham600.jsonl
# (gói mã cũng có vài ảnh ep*_s*.png; glob toàn /kaggle/input dễ trỏ nhầm)
v600 = glob.glob("/kaggle/input/**/val_cham600.jsonl", recursive=True)
assert len(v600) == 1, f"DỪNG: cần đúng một dataset thesis-val-cham, thấy {v600}"
BASE = os.path.dirname(v600[0])
assert os.path.exists(f"{BASE}/val_cham400.jsonl")

C1 = [json.loads(l) for l in open(f"{PK}/c1_mau.jsonl", encoding="utf-8")]
assert len(C1) == 400
assert [(r["episode_id"], r["step_id"]) for r in C1[:3]] == [(11948, 3), (2782, 0), (188, 8)]
TAPT = ("click", "long_press")
assert all(len(r["mau"]) == 8 for r in C1)
# 5 mẫu rỗng có thật nhưng đều ở bước không click (không vào phép chấm) ⇒ chỉ kiểm bước click
assert all(r["greedy"] and all(r["mau"]) for r in C1 if r["action_type"] in TAPT), "DỪNG: câu rỗng ở bước click"
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
thieu = [d["image"] for d in taps if not os.path.exists(f"{VD}/{d['image']}")]
print("bước C1:", len(recs), "| click:", len(taps), "(cần 249) | ảnh thiếu:", len(thieu), "(cần 0)", flush=True)
assert len(taps) == 249 and not thieu
assert {(d["episode_id"], d["step_id"]) for d in taps} == \
       {(r["episode_id"], r["step_id"]) for r in C1 if r["action_type"] in TAPT}, "DỪNG: action_type lệch"

PD = f"{W}/c1preds"
os.makedirs(PD, exist_ok=True)
for k in range(9):
    with open(f"{PD}/k{k}.jsonl", "w", encoding="utf-8") as fo:
        for r in C1:
            s = r["greedy"] if k == 0 else r["mau"][k - 1]
            fo.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "pred": s},
                                ensure_ascii=False) + "\n")
OUT = f"{W}/c1score"
os.makedirs(OUT, exist_ok=True)
print("9 tệp câu:", sorted(os.listdir(PD)), flush=True)

# tải MỘT lần ở đây, để hai tiến trình GPU không cùng tải một lúc
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

### Ô 3 — nối tiếp (nếu có) · thử 3 bước · chấm đủ 9 tệp trên 2 GPU

```python
import subprocess, time, glob, shutil
env = {**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1"}

def lenh(k, out):
    return (f"python harness/score_run.py --mode score --grounder uground "
            f"--preds {PD}/k{k}.jsonl --data-root {VD} --recs-file c1_recs.jsonl --out {out}")

# ① nối tiếp: nếu có gắn Output của một version trước làm Input thì chép tệp thô cũ sang
#    (score_run.py tự bỏ bước đã chấm, và tự dừng nếu tệp thô không khớp tệp câu)
for p in glob.glob("/kaggle/input/**/c1score/score_k*_raw.jsonl", recursive=True):
    dst = f"{OUT}/{os.path.basename(p)}"
    if not os.path.exists(dst):
        shutil.copy(p, dst)
        print("nối tiếp từ", p, sum(1 for _ in open(dst)), "bước", flush=True)

# ② thử 3 bước trên GPU 0, ra thư mục riêng — hỏng thì commit dừng ở đây sau vài phút
os.makedirs(f"{W}/thu", exist_ok=True)
with open(f"{W}/thu.log", "w") as lg:
    rc = subprocess.run(lenh(0, f"{W}/thu/score_thu.json") + " --n 3", shell=True, cwd=WS,
                        env={**env, "CUDA_VISIBLE_DEVICES": "0"}, stdout=lg, stderr=subprocess.STDOUT).returncode
tl = open(f"{W}/thu.log").read()
print(tl[-1500:], flush=True)
thu = [json.loads(l) for l in open(f"{W}/thu/score_thu_raw.jsonl")]
assert rc == 0 and len(thu) == 3, f"DỪNG: lượt thử lỗi (mã {rc}, {len(thu)} bước) — xem thu.log"
assert f"[dữ liệu] {VD}/c1_recs.jsonl" in tl and "[uground] nạp osunlp/UGround-V1-2B" in tl, \
    "DỪNG: tiến trình không đọc đúng dữ liệu hoặc đúng bộ trỏ"
assert all(o.get("pred_xy") and o.get("n_buttons", 0) > 0 for o in thu), "DỪNG: bộ trỏ không trả toạ độ hoặc 0 nút"
print("THỬ 3 BƯỚC: ĐẠT", flush=True)

# ③ lượt đủ: k chia đều cho các GPU, mỗi GPU chạy nối đuôi các tệp của mình
chuoi = {g: [k for k in range(9) if k % NGPU == g] for g in range(NGPU)}
PS = [subprocess.Popen(["bash", "-c", " && ".join(lenh(k, f"{OUT}/score_k{k}.json") for k in ks)],
                       cwd=WS, env={**env, "CUDA_VISIBLE_DEVICES": str(g)}, start_new_session=True,
                       stdout=open(f"{W}/cham_gpu{g}.log", "a"), stderr=subprocess.STDOUT)
      for g, ks in chuoi.items()]

def dem():
    return [sum(1 for _ in open(f"{OUT}/score_k{k}_raw.jsonl")) if os.path.exists(f"{OUT}/score_k{k}_raw.jsonl")
            else 0 for k in range(9)]

t0 = time.time()
while any(p.poll() is None for p in PS):
    time.sleep(120)
    print(f"{time.strftime('%H:%M')} - {(time.time()-t0)/3600:4.2f} h - "
          + " ".join(f"k{k}:{n}/249" for k, n in enumerate(dem())), flush=True)
    if time.time() - t0 > 10 * 3600:            # đệm dưới trần 12 h; tệp thô ghi dần nên giữ được phần đã xong
        for p in PS:
            p.terminate()
        print("⛔ quá 10 h — dừng, giữ phần đã ghi", flush=True)

for g in range(NGPU):
    print(f"--- GPU {g} ---\n" + subprocess.run(["tail", "-8", f"{W}/cham_gpu{g}.log"],
                                               capture_output=True, text=True).stdout, flush=True)
rcs = [p.returncode for p in PS]
print("mã thoát:", rcs, "| đếm:", dem(), flush=True)
assert rcs == [0] * NGPU and dem() == [249] * 9, "DỪNG: chưa đủ 249/249 ở mọi tệp — xem §5 (nối tiếp)"
```

### Ô 4 — gộp số

```python
import random
R = {}
for k in range(9):
    R[k] = {}
    for line in open(f"{OUT}/score_k{k}_raw.jsonl", encoding="utf-8"):
        o = json.loads(line)
        R[k][(o["episode_id"], o["step_id"])] = o
tap_keys = [(r["episode_id"], r["step_id"]) for r in C1 if (r["episode_id"], r["step_id"]) in R[0]]
assert len(tap_keys) == 249, len(tap_keys)
for k in range(9):
    assert set(R[k]) == set(tap_keys), f"k{k} thiếu bước"

def ex(k, key):
    return int(R[k][key].get("executable", 0))

def disk(k, key):
    return int(R[k][key].get("hit_disk", 0))

idx = {(r["episode_id"], r["step_id"]): i for i, r in enumerate(C1)}
pick = {key: int(PICKS[idx[key]]) for key in tap_keys}
n = len(tap_keys)

def pct(xs):
    return round(100 * sum(xs) / n, 2)

tong = {
    "n_click": n,
    "exec_greedy": pct([ex(0, q) for q in tap_keys]),
    "exec_oracle_spice": pct([ex(pick[q], q) for q in tap_keys]),
    "hit_disk_greedy": pct([disk(0, q) for q in tap_keys]),
    "hit_disk_oracle_spice": pct([disk(pick[q], q) for q in tap_keys]),
    "exec_moi_mau": {f"k{k}": pct([ex(k, q) for q in tap_keys]) for k in range(1, 9)},
    "exec_tb_8_mau": round(sum(pct([ex(k, q) for q in tap_keys]) for k in range(1, 9)) / 8, 2),
    "ti_le_co_it_nhat_1_cau_trung_trong_9": pct([max(ex(k, q) for k in range(9)) for q in tap_keys]),
    "so_buoc_oracle_doi_cau": sum(1 for q in tap_keys if pick[q] != 0),
}
doi = [q for q in tap_keys if pick[q] != 0]
tong["tren_buoc_oracle_doi_cau"] = {
    "n": len(doi),
    "exec_greedy": round(100 * sum(ex(0, q) for q in doi) / max(len(doi), 1), 2),
    "exec_oracle": round(100 * sum(ex(pick[q], q) for q in doi) / max(len(doi), 1), 2),
    "greedy_truot_oracle_trung": sum(1 for q in doi if not ex(0, q) and ex(pick[q], q)),
    "greedy_trung_oracle_truot": sum(1 for q in doi if ex(0, q) and not ex(pick[q], q)),
}
assert tong["so_buoc_oracle_doi_cau"] == 119, "DỪNG: PICKS lệch bản CPU (phải đổi câu ở 119/249 bước click)"

# KTC 95% bootstrap theo episode cho hiệu oracle − greedy
eps = sorted({q[0] for q in tap_keys})
theo_ep = {e: [q for q in tap_keys if q[0] == e] for e in eps}
rng = random.Random(101)
ds = []
for _ in range(10000):
    mau_ep = [rng.choice(eps) for _ in eps]
    qs = [q for e in mau_ep for q in theo_ep[e]]
    ds.append(100 * sum(ex(pick[q], q) - ex(0, q) for q in qs) / len(qs))
ds.sort()
tong["hieu_exec_oracle_tru_greedy"] = round(tong["exec_oracle_spice"] - tong["exec_greedy"], 2)
tong["ktc95_bootstrap_episode"] = [round(ds[249], 2), round(ds[9749], 2)]

print(json.dumps(tong, ensure_ascii=False, indent=1), flush=True)
json.dump(tong, open(f"{W}/c1_exec_tong.json", "w"), ensure_ascii=False, indent=1)
```

### Ô 5 — gói kết quả

```python
import zipfile
with zipfile.ZipFile(f"{W}/c1_exec_8mau.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(glob.glob(f"{OUT}/*") + glob.glob(f"{W}/cham_gpu*.log")
                    + [f"{W}/c1_exec_tong.json", f"{W}/thu.log"]):
        if os.path.exists(p):
            z.write(p, os.path.relpath(p, W))
print(os.path.getsize(f"{W}/c1_exec_8mau.zip") // 1024, "KB — tải ở tab Output của version", flush=True)
shutil.rmtree(f"{W}/pk", ignore_errors=True)   # gói mã chép tạm, không cần lên Output
```

---

## 5. Khi commit dừng giữa chừng

Mọi điểm dừng đều là `assert` có chữ **DỪNG** trong log. Tra theo dòng đó:

| log báo | làm gì |
|---|---|
| `cần đúng một gói c1-exec8` / `cần đúng một dataset thesis-val-cham` | thiếu Input, hoặc gắn thừa dataset có tệp trùng tên. Sửa Input, commit lại |
| `c1_mau.jsonl lệch bản máy nhà` | upload nhầm tệp. Chạy lại §2, *New Version* dataset `c1-exec8` |
| `chỉ ghép được …/400` · `ảnh thiếu` | `thesis-val-cham` trên Kaggle không phải bản đủ 1.567 ảnh. Gửi log |
| `thiếu cây trợ năng` | Internet đang OFF, hoặc HuggingFace lỗi. Bật Internet, commit lại |
| `lượt thử lỗi` | mở `thu.log` ở tab Output, gửi 30 dòng cuối |
| sau 15 phút mọi `kN` vẫn 0 | *Cancel* version, gửi `cham_gpu*.log` |
| `CUDA out of memory` · lỗi tải HuggingFace | gửi log, đừng đổi cấu hình |
| `TỆP THÔ KHÔNG KHỚP TỆP DỰ ĐOÁN` | tệp thô gắn vào để nối tiếp là của lần chạy khác. Bỏ Input đó, commit lại |
| `chưa đủ 249/249` (Kaggle cắt phiên, hoặc quá 10 h) | **nối tiếp**, xem dưới |

**Nối tiếp sau khi bị cắt:** mở notebook → *Add Input* → tab *Your Work* / *Notebook Output Files*
→ chọn **Output của version vừa dừng** (có thư mục `c1score/`) → *Save Version* → *Save & Run All*
lần nữa. Ô 3 tự chép tệp thô cũ sang và chỉ chấm phần còn thiếu. Không xoá tệp thô nào.
⚠️ Tôi chưa kiểm được việc Kaggle có giữ Output của một version **lỗi** hay không; nếu tab Output
của version đó trống thì commit lại từ đầu (mất ~2 h T4, 0 đồng).

---

## 6. Luật đọc, chốt trước khi có số

Mốc: `exec_greedy` trên 249 bước click, so với `exec_oracle_spice`. Oracle SPICE hơn greedy
**+22,51 SPICE** trên chính 249 bước này.

| kết quả | kết luận |
|---|---|
| `hieu_exec_oracle_tru_greedy ≥ +2,0` **và** cận dưới KTC > 0 | Trong mẫu S1 có câu vừa tốt SPICE vừa bấm đúng hơn. Được phép train phương pháp của file 250 (GRPO thưởng SPICE + đầu khe có cổng) |
| hiệu từ 0 đến +2,0, hoặc KTC chứa 0 | SPICE tăng không kéo `exec`. Không train. Tìm cách khác cho metric bấm |
| hiệu < 0 | SPICE cao hơn làm bấm tệ hơn: hai metric đi ngược nhau trong tập mẫu S1. Dừng hướng này |

Hai số phụ đọc kèm, **không làm cổng**:
- `ti_le_co_it_nhat_1_cau_trung_trong_9`: trần của mọi phương pháp chỉ chọn trong mẫu S1.
- `greedy_truot_oracle_trung` so với `greedy_trung_oracle_truot`: đổi câu sửa được bao nhiêu, phá bao nhiêu.

249 bước là mẫu nhỏ: sai số chuẩn của một tỉ lệ quanh 60% khoảng 3 điểm, nên hiệu +2 có thể chưa
có ý nghĩa. Vì vậy cổng đòi thêm cận dưới KTC > 0.

## 7. Không được làm

- Không train, không sinh câu mới, không đổi `temperature` hay số mẫu.
- Không chấm tập test.
- Không đổi grounder, không đổi luật `exec`.
- Không trích số val nào ra luận văn.

## Ảnh gốc

`harness/tai_lieu_2026-09-28/anh_goc_251/anh1.jpg … anh6.jpg` (tách từ bản base64 nhúng trong file cũ, 4,9 MB → file này
còn vài chục KB). Đã đối chiếu ảnh 3–5 với Ô 2–4: logic khớp, chỉ khác ở năm chỗ của §0.
