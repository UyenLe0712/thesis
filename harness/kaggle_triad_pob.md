# Kaggle (commit) — TRIAD-T pha POB: mẫu ck500 thật → ShowUI → UGround → UI-Venus (action 273 §6, 4/10/2026)

Chạy vì POA rơi **vùng xám** (net +1, `report/274`). Bộ chọn, lưới `r × r_trust`, luật chọn cấu hình và listener
ShowUI-2B **giữ nguyên từ POA**, không chọn lại.

**Một commit, T4 ×2, ước 5–6 h** (trần commit 12 h; Ô 4 tự dừng ở 10,5 h, phần dở nối tiếp ở commit sau).

| bước | GPU | việc | ước |
|---|---|---|---|
| 0 | 0 | hoà S1 (`grpo_spice.py --merge`) | ~5 phút |
| 1 | 0 ‖ 1 | ck500 sinh 8 mẫu/bước trên 249 click: **T=0,7 ở GPU0** (kèm sinh lại greedy để kiểm dụng cụ) ‖ **T=1,0 ở GPU1**. `top_p=1`, `top_k=0`, seed = 20261004 + chỉ số bước | ~1,5 h |
| 2 | CPU | gom câu **duy nhất, khác greedy** ở mỗi bước (hai nhiệt độ chung một kho) ⇒ danh sách gọi listener + các "lớp" preds cho UGround | giây |
| 3 | 0 ‖ 1 | ShowUI-2B (fp32) đọc mọi câu mới, chia đôi theo bước | ~2 h |
| 4 | 0 ‖ 1 | UGround chấm mọi câu mới (cần cho oracle C3 và mọi ô lưới), lớp chẵn GPU0 · lớp lẻ GPU1 | ~1,3 h |
| 5 | CPU | bộ chọn C2 trên từng nhiệt độ, luật §5.3 ⇒ câu cần UI-Venus | giây |
| 6 | 0+1 | UI-Venus chấm câu được C2 tốt nhất đổi (ck500 đã có từ POA) | ~10–20 phút |
| 7 | CPU | gói `triad_pob_out.zip` | — |

Greedy ck500 không chạy lại listener/UGround/UI-Venus: đã có từ POA (`listener_showui_poa.jsonl`,
`score_ck500_l4_raw.jsonl` = mốc 166, `score_venus_ck500_raw.jsonl` = 146).

## Chuẩn bị (máy nhà → Kaggle)

1. Dataset mới **`triad-pob-script`** (Private): kéo cả 12 tệp trong `_bundles/triad-pob-script/`.
2. Notebook mới. *Session options*: **GPU T4 ×2**, **Internet On**.
   *Add Input* (5 dataset): `fgrb-p1-bundle` · `c1-exec8` · `thesis-val-cham` · `grpo-spice-ck500` · `triad-pob-script`.
   Commit trước bị cắt giữa chừng thì thêm **Output của commit đó** làm Input.

   ⚠️ **Chạy bằng nick thứ hai:** ở nick đang giữ dataset, mở từng dataset `fgrb-p1-bundle` · `c1-exec8` ·
   `thesis-val-cham` · `grpo-spice-ck500` → *Settings → Sharing* → thêm username nick thứ hai (quyền xem).
   `triad-pob-script` thì upload thẳng bằng nick thứ hai. Nếu `grpo-spice-ck500` không có ở nick nào: làm theo mục
   *Chạy bằng tài khoản Kaggle khác* của `kaggle_grpo_spice_pha3_ck500.md` (adapter md5 `491fa667…`).

## Ô 1 — gói

```python
import subprocess, sys, os, time
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes pillow 2>&1 | tail -3")
sh(f'{sys.executable} -c "import transformers, peft, torch; print(transformers.__version__, peft.__version__, torch.__version__, torch.cuda.device_count(), torch.cuda.get_device_name(0))"')
```

Phải thấy **2** card Tesla T4. Nếu peft báo `incompatible version of torchao`: *Restart session* rồi chạy từ Ô 2.

## Ô 2 — đường dẫn, md5, adapter ck500, chép phần dở

```python
import glob, json, shutil, hashlib
T0 = time.time()
TEST = True                       # chạy thử tương tác; đổi False trước khi commit
HAN = T0 + 10.5 * 3600
W = "/kaggle/working"
D = f"{W}/triad_pob_out"; os.makedirs(D, exist_ok=True)
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
MD = {"triad_pob.py": "36e8e299d15b7c630f9815a207ce666a", "triad_t.py": "21ca76081bad6e9c9c73d15c61f16066",
      "triad_listener.py": "ebc70af0d344694ef99c509d80363d4e", "metric_exec.py": "9bf0b84145458fd55919a5e161b9766f",
      "grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf", "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912",
      "pred_ck500.jsonl": "eb6162d86730a936beb5ae5a9fd6d652"}
MDD = {"score_ck500_l4_raw.jsonl": "6980d5ee119b55109d8e21dab91a66b4", "loc_val_g.jsonl": "3bf8af87e64f321f8193f373583b568c",
       "loc_val_d.jsonl": "ff950e585ae22aba614ae4f10168f176", "listener_showui_poa.jsonl": "936723712cdc876b34ad1a6e187462d7",
       "score_venus_ck500_raw.jsonl": "e741545618d72b22cef1af24435219a4"}
# output của commit trước (nếu gắn làm Input) chứa bản sao script/dữ liệu cũ ⇒ mọi glob tìm gói phải bỏ qua nó
OLD = sorted({os.path.dirname(p) for p in glob.glob("/kaggle/input/**/triad_pob_out", recursive=True)})
ngoai = lambda p: not any(p == o or p.startswith(o + "/") for o in OLD)
print("output commit trước:", OLD or "không có", flush=True)
SRC = sorted({os.path.dirname(p) for p in glob.glob("/kaggle/input/**/triad_pob.py", recursive=True) if ngoai(p)})
assert len(SRC) == 1, f"DỪNG: cần đúng một triad-pob-script, thấy {SRC}"
for f, h in MD.items():
    shutil.copy(f"{SRC[0]}/{f}", f"{W}/{f}"); assert md5(f"{W}/{f}") == h, f"DỪNG: {f} lệch md5"
for f, h in MDD.items():
    shutil.copy(f"{SRC[0]}/{f}", f"{D}/{f}"); assert md5(f"{D}/{f}") == h, f"DỪNG: {f} lệch md5"

BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "images" in d and ngoai(r))
C1M = glob.glob("/kaggle/input/**/c1_mau.jsonl", recursive=True); C1M = [p for p in C1M if "triad" not in p and ngoai(p)]
assert len(C1M) == 1 and md5(C1M[0]) == "d757554326977309c3a65ae0b144c211", f"DỪNG: c1_mau.jsonl {C1M}"
C1M = C1M[0]
def la_grpo(d):
    c = os.path.join(d, "adapter_config.json")
    return os.path.exists(c) and "s1_merged" in json.load(open(c)).get("base_model_name_or_path", "")
CK = [os.path.dirname(f) for f in glob.glob("/kaggle/input/**/adapter_model.safetensors", recursive=True) if la_grpo(os.path.dirname(f)) and ngoai(f)]
if len(CK) > 1: CK = [d for d in CK if d.rstrip("/").endswith("checkpoint-500")]
assert len(CK) == 1, f"DỪNG: cần đúng một adapter ck500, thấy {CK}"
CK500 = CK[0]
assert md5(f"{CK500}/adapter_model.safetensors") == "491fa6677340393f1e4464c08a0cec98", "DỪNG: không phải ck500 đã chấm"
MERGED = f"{W}/s1_merged"

# commit trước bị cắt: chép phần dở về (bỏ dòng ghi dở), các script tự nối tiếp
for p in glob.glob("/kaggle/input/**/triad_pob_out/**/*.jsonl", recursive=True):
    if ".ipynb_checkpoints" in p: continue
    rel = p.split("triad_pob_out/", 1)[1]; d = f"{D}/{rel}"
    if os.path.exists(d) or os.path.basename(p) in MDD: continue
    os.makedirs(os.path.dirname(d), exist_ok=True)
    ok = []
    for l in open(p, encoding="utf-8"):
        try: json.loads(l); ok.append(l)
        except ValueError: pass
    open(d, "w", encoding="utf-8").writelines(ok); print("nối tiếp:", rel, len(ok), "dòng")
print("BUNDLE", BUNDLE, "\nCK500", CK500, "\nTEST", TEST, flush=True)
```

## Ô 3 — dựng dữ liệu C1 cho listener/UGround/UI-Venus (như Ô 3 của POA)

```python
cand = sorted({os.path.dirname(p) for p in glob.glob("/kaggle/input/**/c1_picks.json", recursive=True)
               if os.path.exists(os.path.join(os.path.dirname(p), "c1_mau.jsonl")) and ngoai(p)})
assert len(cand) == 1, f"DỪNG: cần đúng một gói c1-exec8, thấy {cand}"
PK = cand[0]
WS = f"{W}/pk/thesis"
shutil.copytree(f"{PK}/thesis", WS, dirs_exist_ok=True)
sr = open(f"{WS}/harness/score_run.py", encoding="utf-8").read()
assert "--recs-file" in sr and "VENUS_MIN_PIXELS" in sr[sr.index("class UIVenus"):], "DỪNG: score_run.py là bản cũ"
v600 = sorted(glob.glob("/kaggle/input/**/val_cham600.jsonl", recursive=True), key=len)
v600 = [p for p in v600 if ngoai(p) and all(os.path.exists(os.path.join(os.path.dirname(p), f)) for f in ("val_cham400.jsonl", "ocr.jsonl", "images"))]
assert v600, "DỪNG: không thấy thesis-val-cham đủ bộ"
BASE = os.path.dirname(v600[0])
C1 = [json.loads(l) for l in open(f"{PK}/c1_mau.jsonl", encoding="utf-8")]
KEYS = {(r["episode_id"], r["step_id"]) for r in C1}
VD = f"{W}/c1data"; os.makedirs(VD, exist_ok=True)
recs = {}
for f in ("val_cham400.jsonl", "val_cham600.jsonl"):
    for d in map(json.loads, open(f"{BASE}/{f}", encoding="utf-8")):
        k = (d["episode_id"], d["step_id"])
        if k in KEYS and k not in recs:
            d.setdefault("gold_instruction", d["target_instruction"]); recs[k] = d
assert len(recs) == 400
with open(f"{VD}/c1_recs.jsonl", "w", encoding="utf-8") as fo:
    for r in C1: fo.write(json.dumps(recs[(r["episode_id"], r["step_id"])], ensure_ascii=False) + "\n")
shutil.copy(f"{VD}/c1_recs.jsonl", f"{D}/c1_recs.jsonl")
shutil.copy(f"{BASE}/ocr.jsonl", f"{VD}/ocr.jsonl")
if os.path.lexists(f"{VD}/images"): os.remove(f"{VD}/images")
os.symlink(f"{BASE}/images", f"{VD}/images")
taps = [d for d in recs.values() if d["action"].get("action_type") in ("click", "long_press") and "x" in d["action"]]
assert len(taps) == 249 and all(os.path.exists(f"{VD}/{d['image']}") for d in taps)
sys.path.insert(0, f"{WS}/harness")
import a11y_inventory as A11Y, score_run as SR
names = set(A11Y._zip().namelist())
co_cay = sum(A11Y.key_for(f"episode_{d['episode_id']}_screenshot_{d['step_id']}.png") in names for d in taps)
assert co_cay == 249 and sum(len(SR.buttons_of(d)) == 0 for d in taps) == 0, "DỪNG: thiếu cây trợ năng"
print("C1: 249 click · cây trợ năng đủ", flush=True)
```

## Ô 4 — hàm chạy song song có nhịp sống

```python
ENV = {"TQDM_DISABLE": "1", "PYTHONUNBUFFERED": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1"}
def chay2(viec):
    """viec = [(cmd, log, gpus, cwd, env_them)] chạy song song; nhịp 2 phút (30 s khi TEST); quá HAN thì dừng."""
    ps = []
    for cmd, log, gpus, cwd, ex in viec:
        f = open(log, "a")
        ps.append((subprocess.Popen(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                   env={**os.environ, **ENV, "CUDA_VISIBLE_DEVICES": gpus, **(ex or {})}), log))
    while any(q.poll() is None for q, _ in ps):
        time.sleep(30 if TEST else 120)
        for q, log in ps:
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"  {(time.time()-T0)/3600:5.2f} h · {os.path.basename(log)} · {L[-1][:130] if L else '...'}", flush=True)
        if time.time() > HAN:
            for q, _ in ps: q.terminate()
            print("⛔ tới mốc 10,5 h — dừng; commit sau thêm Output này làm Input để nối tiếp", flush=True)
            return False
    for q, log in ps:
        print(f"--- {os.path.basename(log)} · mã thoát {q.returncode}\n" + "".join(open(log, errors="ignore").readlines()[-4:]), flush=True)
    return all(q.returncode == 0 for q, _ in ps)

def lop_cmd(files, ten, gpus, grounder, ex=None):
    """Một tiến trình bash chấm lần lượt nhiều lớp preds bằng score_run.py (mỗi lớp nạp bộ trỏ một lần)."""
    lenh = " && ".join(f"python -u harness/score_run.py --mode score --grounder {grounder} --preds {p} "
                       f"--data-root {VD} --recs-file c1_recs.jsonl --out {p[:-6]}.json --n 99999" for p in files) or "true"
    return (["bash", "-c", lenh], f"{D}/{ten}.log", gpus, WS, ex)
```

`--n 99999` vì mỗi lớp chỉ chứa một phần số bước (score_run sẽ in "TỆP DỰ ĐOÁN THIẾU" — bình thường ở đây).

## Ô 5 — hoà S1 + bước 1: ck500 sinh mẫu hai nhiệt độ

```python
r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED], cwd=W, capture_output=True, text=True)
print((r.stdout + r.stderr)[-600:]); assert r.returncode == 0, "DỪNG: hoà lỗi"
NV = ["--n", "3"] if TEST else []
G = ["python", "-u", "triad_pob.py", "--sample", "--bundle", BUNDLE, "--merged", MERGED, "--ckpt", CK500, "--c1", C1M]
ok1 = chay2([(G + ["--temp", "0.7", "--out", f"{D}/mau_t07.jsonl", "--kiem-greedy", f"{W}/pred_ck500.jsonl"] + NV, f"{D}/mau_t07.log", "0", W, None),
             (G + ["--temp", "1.0", "--out", f"{D}/mau_t10.jsonl"] + NV, f"{D}/mau_t10.log", "1", W, None)])
n07 = sum(1 for _ in open(f"{D}/mau_t07.jsonl")); n10 = sum(1 for _ in open(f"{D}/mau_t10.jsonl"))
print(f"== mẫu: T=0,7 {n07}/{3 if TEST else 249} · T=1,0 {n10}/{3 if TEST else 249}", flush=True)
for l in open(f"{D}/mau_t07.jsonl").readlines()[:2]: print("   ", json.loads(l)["mau"][:4], flush=True)
```

**Kiểm ở lượt thử:** `[cấu hình lấy mẫu] {'do_sample': True, 'temperature': 0.7, … 'top_k': 0 …}` trong `mau_t07.log`,
`[điểm lưu] …checkpoint-500`, `[kiểm hoà ck500] greedy sinh lại trùng pred_ck500: 3/3` (bản đủ: kỳ vọng ≥ 240/249;
thấp hẳn thì dừng — sai mô hình hoặc sai câu nhắc). Câu mẫu phải là tiếng Anh, dạng "Click on …".

## Ô 6 — bước 2–4: lớp câu duy nhất → ShowUI → UGround

```python
du1 = (n07 == n10 == (3 if TEST else 249))
if du1:
    r = subprocess.run(["python", "triad_pob.py", "--lop", "--dir", D] + (["--thu"] if TEST else []), cwd=W, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-800:], flush=True); assert r.returncode == 0, "DỪNG: dựng lớp lỗi"
    LN = ["--n", "6"] if TEST else []
    ok3 = chay2([(["python", "-u", "triad_listener.py", "--calls", f"{D}/calls_pob.jsonl", "--img-root", VD,
                   "--out", f"{D}/listener_pob_s{s}.jsonl", "--shard", str(s), "--nshard", "2"] + LN,
                  f"{D}/listener_pob_s{s}.log", str(s), W, None) for s in (0, 1)])
    LOP = sorted(glob.glob(f"{D}/ug_lop/lop*.jsonl")); LOP = [p for p in LOP if not p.endswith("_raw.jsonl")]
    if TEST: LOP = LOP[:2]
    ok4 = ok3 and chay2([lop_cmd(LOP[0::2], "ug_gpu0", "0", "uground"), lop_cmd(LOP[1::2], "ug_gpu1", "1", "uground")])
    nL = sum(1 for s in (0, 1) for _ in open(f"{D}/listener_pob_s{s}.jsonl"))
    nU = sum(1 for p in glob.glob(f"{D}/ug_lop/*_raw.jsonl") for _ in open(p))
    nC = sum(1 for _ in open(f"{D}/calls_pob.jsonl")); nP = sum(1 for p in LOP for _ in open(p))
    print(f"== listener {nL}/{nC} · UGround {nU}/{nP} câu", flush=True)
```

**Kiểm ở lượt thử:** dòng `[lớp] … câu duy nhất khác greedy · … lớp UGround · … lời gọi listener mới`; listener
`dtype thật torch.float32`, `raw='[0.xx, 0.yy]'`; `ug_gpu0.log` có `[uground] nạp osunlp/UGround-V1-2B`.

## Ô 7 — bước 5–6: chọn C2 + UI-Venus (chỉ bản đủ)

```python
if not TEST and du1 and ok4:
    r = subprocess.run(["python", "triad_pob.py", "--chon", "--dir", D], cwd=W, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); assert r.returncode == 0, "DỪNG: chọn lỗi"
    VL = sorted(p for p in glob.glob(f"{D}/venus_lop/vlop*.jsonl") if not p.endswith("_raw.jsonl"))
    VEN = {"VENUS_MIN_PIXELS": "200704", "VENUS_MAX_PIXELS": "1003520"}      # 1.272 tok, như POA và phép B
    chay2([lop_cmd(VL, "venus", "0,1", "uivenus", VEN)])
    print(f"== UI-Venus {sum(1 for p in glob.glob(f'{D}/venus_lop/*_raw.jsonl') for _ in open(p))}/"
          f"{sum(1 for p in VL for _ in open(p))} câu", flush=True)
else:
    print("bỏ qua Ô 7 (TEST hoặc bước trước chưa đủ)", flush=True)
```

## Ô 8 — gói một zip

```python
shutil.rmtree(MERGED, ignore_errors=True); shutil.rmtree(f"{W}/pk", ignore_errors=True); shutil.rmtree(VD, ignore_errors=True)
shutil.make_archive(f"{W}/triad_pob_out", "zip", W, "triad_pob_out")
print("zip:", os.path.getsize(f"{W}/triad_pob_out.zip") // 1024, "KB ·", sorted(os.listdir(D)), flush=True)
```

## Chạy

1. **Thử tương tác** (`TEST = True`, ~25–30 phút, phần lớn là tải mô hình và hoà S1): *Run All*. Gửi về output
   Ô 2, Ô 5 (dòng `[cấu hình lấy mẫu]`, `[kiểm hoà ck500]`, 2 dòng mẫu), Ô 6 (dòng `[lớp]`, `== listener`, `== UGround`).
   Số của lượt thử **không đọc thành kết quả**.
2. Ổn thì: Ô 2 `TEST = False` → *Stop session* → *Save Version → Save & Run All (Commit)*.
3. Commit xong: tải `triad_pob_out.zip`, giải nén vào **`runs/triad_t/pob/`**.
4. Máy nhà, 0 GPU:
   ```
   python3 harness/triad_pob.py --bao-cao --dir runs/triad_t/pob/triad_pob_out --out runs/triad_t/pob_ket_qua.json
   ```
   rồi đọc cổng §6.3 của action 273.
