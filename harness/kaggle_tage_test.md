# Kaggle (commit) — TAGE trên TẬP TEST 4.463 bước click (3/10/2026)

Mục tiêu: có **số test** cho TAGE `pred+cổng` (bộ định vị `loc_g` → vùng cắt → bộ biên tập `ed_gold` → cổng),
so S1/101 và ck500 trên đúng 4.463 bước click đã dùng cho mọi nhánh. Số val ở `report/267`.

**Thiết kế đo (không tinh chỉnh gì trên test):**
- Câu nháp = `pred_ck500_test.jsonl` (đã sinh và chấm ở lượt 259, cùng T4).
- τ cổng **chọn trên toàn bộ 249 bước val, mang nguyên sang test**: `τ_pred = 0,73767` (val: nhận sửa 11
  câu, exec 170/249) · `τ_none = −0,04327` (val: nhận sửa 108 câu, exec 172/249).
- Chỉ chấm UGround những bước cổng **nhận câu sửa** (câu khác câu nháp). Bước giữ câu nháp dùng kết quả chấm
  ck500 test đã có (`runs/grpo_spice/score_ck500_test_raw.jsonl`), cùng bản `score_run.py` trong
  `thesis-score`, cùng T4 ⇒ cùng dụng cụ. Gộp và đọc trên WSL, 0 GPU.
- Hai GPU T4 chạy song song, mỗi card một nửa số bước (`--shard 0/1 --nshard 2`).

**Commit 1** = nhánh `pred` (định vị + sửa + chấm). **Commit 2** (tuỳ chọn) = nhánh `none` (đối chứng không
vùng cắt). Thời gian T4 **chưa đo**: ước 6–9 h cho commit 1 (L4 đo được: định vị 1,8 s/bước, sửa 3,6 s/bước;
T4 chậm hơn, chia đôi nhờ 2 card). Ô 4 tự dừng sinh ở mốc 10,5 h để commit không vượt trần 12 h (vượt trần là
mất trắng output); phần dở được nối tiếp ở commit sau.

## Chuẩn bị (máy nhà → Kaggle)

1. **Adapter từ Drive** (`MyDrive/thesis/tage/out/that/`): tải **chỉ hai tệp ở gốc** của mỗi thư mục
   `ed_gold/`, `loc_g/`, `ed_none/` — `adapter_config.json` + `adapter_model.safetensors` (không lấy
   `ckpt_last/`, `epoch1/`). Tạo dataset Kaggle **`tage-adapters`** giữ nguyên ba thư mục con
   `ed_gold/`, `loc_g/`, `ed_none/`.
2. Dataset **`tage-test-script`**: kéo cả 6 tệp trong `_bundles/tage-test-script/`:

   | tệp | md5 |
   |---|---|
   | `tage_val.py` | `1ee4b561176e13397ed6b45a54ac0d71` |
   | `grpo_spice.py` | `07ea87b6d156d1faa391a4274dffd7cf` |
   | `build_branch_data.py` | `619e63e123a6dbf60086e65ee94a3912` |
   | `test_rows.jsonl` (4.463 hàng click, có w, h) | `c1b05298af0912348002b25382d9d392` |
   | `pred_ck500_test.jsonl` | `328847ac96fa3104f76cd997f4091bcd` |
   | `tage_neg.jsonl` | `75539cdc533ecaa578d6067e3fbcd8a5` |

3. Notebook mới. *Session options*: **GPU T4 ×2**, **Internet On**.
   *Add Input*: `thesis-score` · `fgrb-p1-bundle` · `tage-test-script` · `tage-adapters`.

## Ô 1 — gói

```python
import subprocess, sys, os, time, glob, json, shutil, hashlib
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes 2>&1 | tail -3")
sh(f'{sys.executable} -c "import transformers, peft, torch; print(transformers.__version__, peft.__version__, torch.__version__, torch.cuda.device_count(), torch.cuda.get_device_name(0))"')
```

Phải thấy **2** card Tesla T4.

## Ô 2 — đường dẫn, md5, dựng thư mục test, kéo phần dở của commit trước

```python
T0 = time.time()
W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
MD = {"tage_val.py": "1ee4b561176e13397ed6b45a54ac0d71", "grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf",
      "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912", "test_rows.jsonl": "c1b05298af0912348002b25382d9d392",
      "pred_ck500_test.jsonl": "328847ac96fa3104f76cd997f4091bcd", "tage_neg.jsonl": "75539cdc533ecaa578d6067e3fbcd8a5"}
SRC = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/test_rows.jsonl", recursive=True)]
assert len(SRC) == 1, f"DỪNG: cần đúng một tage-test-script, thấy {SRC}"
for f, h in MD.items():
    shutil.copy(f"{SRC[0]}/{f}", f"{W}/{f}")
    assert md5(f"{W}/{f}") == h, f"DỪNG: {f} lệch md5"

BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d)
AD = {}
for v in ("ed_gold", "loc_g", "ed_none"):
    c = [os.path.dirname(p) for p in glob.glob(f"/kaggle/input/**/{v}/adapter_model.safetensors", recursive=True)]
    assert len(c) == 1, f"DỪNG: cần đúng một {v}/adapter_model.safetensors, thấy {c}"
    AD[v] = c[0]

TA = None
for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True):
    r = os.path.dirname(t)
    if len(glob.glob(f"{r}/images/*.png")) >= 4463 and os.path.exists(f"{r}/ocr.jsonl"):
        TA = r
assert TA and md5(f"{TA}/test.jsonl") == "da58299ee551a926a21cbecb5232bf78", "DỪNG: test_ac lệch"
TB = f"{W}/testb"                                   # thư mục kiểu bundle: images + ocr.jsonl của tập test
os.makedirs(TB, exist_ok=True)
if not os.path.lexists(f"{TB}/images"): os.symlink(f"{TA}/images", f"{TB}/images")
shutil.copy(f"{TA}/ocr.jsonl", f"{TB}/ocr.jsonl")
PKG = os.path.dirname(os.path.dirname(os.path.dirname(TA)))      # gói mã cũ của thesis-score (score_run đã chấm S1, ck500)
shutil.copytree(f"{PKG}/harness", f"{W}/thesis/harness", dirs_exist_ok=True, ignore=shutil.ignore_patterns("images"))
link = f"{W}/thesis/harness/dg1_cache/test_ac/images"
if os.path.lexists(link): os.remove(link)
os.symlink(f"{TA}/images", link)
WS = f"{W}/thesis"

# commit trước bị cắt giữa chừng: thêm output của nó làm Input, các tệp *.jsonl dở được chép về để nối tiếp
for p in glob.glob("/kaggle/input/**/tage_test_out/*.jsonl", recursive=True):
    d = f"{W}/tage_test_out/{os.path.basename(p)}"
    os.makedirs(os.path.dirname(d), exist_ok=True)
    if not os.path.exists(d):
        L = [l for l in open(p, encoding="utf-8") if l.strip()]
        ok = []
        for l in L:
            try: json.loads(l); ok.append(l)
            except ValueError: pass
        open(d, "w", encoding="utf-8").writelines(ok); print("nối tiếp:", os.path.basename(p), len(ok), "dòng")
O = f"{W}/tage_test_out"; os.makedirs(O, exist_ok=True)
print("BUNDLE", BUNDLE, "\nTA", TA, "\nAD", AD, flush=True)
```

## Ô 3 — hoà S1 + hàm chạy song song có nhịp sống

```python
TEST = True            # chạy thử tương tác; đổi False trước khi commit
HAN = T0 + 10.5 * 3600 # mốc dừng sinh câu, chừa giờ chấm + lưu output dưới trần 12 h
T = ["python", "tage_val.py", "--merged", f"{W}/s1_merged", "--neg", f"{W}/tage_neg.jsonl"]

def chay2(viec):
    """viec = [(cmd, log, gpu)] chạy song song; in nhịp 2 phút; tới HAN thì dừng (phần đã ghi giữ nguyên)."""
    ps = []
    for cmd, log, gpu in viec:
        f = open(log, "a")
        ps.append((subprocess.Popen(cmd, cwd=W, stdout=f, stderr=subprocess.STDOUT,
                   env={**os.environ, "CUDA_VISIBLE_DEVICES": str(gpu), "TQDM_DISABLE": "1",
                        "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1"}), log))
    while any(q.poll() is None for q, _ in ps):
        time.sleep(30 if TEST else 120)
        for q, log in ps:
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"  {(time.time()-T0)/3600:5.2f} h · {os.path.basename(log)} · {L[-1][:100] if L else '...'}", flush=True)
        if time.time() > HAN:
            for q, _ in ps: q.terminate()
            print("⛔ tới mốc 10,5 h — dừng sinh, phần dở nối tiếp ở commit sau", flush=True)
            return False
    for q, log in ps:
        print(f"--- {os.path.basename(log)} · mã thoát {q.returncode}", flush=True)
        print("".join(open(log, errors="ignore").readlines()[-4:]), flush=True)
    return all(q.returncode == 0 for q, _ in ps)

r = subprocess.run(T + ["--merge", "--bundle", BUNDLE], cwd=W, capture_output=True, text=True)
print((r.stdout + r.stderr)[-800:]); assert r.returncode == 0, "DỪNG: hoà lỗi"
NV = ["--n", "4"] if TEST else []
ROWS = ["--bundle", TB, "--rows", f"{W}/test_rows.jsonl", "--nshard", "2"]
```

## Ô 4 — commit 1: định vị `loc_g` → sửa câu `ed_gold` (2 card song song)

```python
def gop(ten):
    """Gộp hai shard theo đúng thứ tự test_rows; trả số dòng."""
    D = {}
    for k in (0, 1):
        p = f"{O}/{ten}_s{k}.jsonl"
        if os.path.exists(p):
            for d in map(json.loads, open(p, encoding="utf-8")): D[(d["episode_id"], d["step_id"])] = d
    hang = [json.loads(l) for l in open(f"{W}/test_rows.jsonl")]
    with open(f"{O}/{ten}.jsonl", "w", encoding="utf-8") as f:
        for r in hang:
            k = (r["episode_id"], r["step_id"])
            if k in D: f.write(json.dumps(D[k], ensure_ascii=False) + "\n")
    return len(D)

ok = chay2([(T + ["--locate-val", "--locator", AD["loc_g"], "--ck500-pred", f"{W}/pred_ck500_test.jsonl",
                  "--out", f"{O}/loc_test_s{k}.jsonl", "--shard", str(k)] + ROWS + NV, f"{O}/loc_test_s{k}.log", k)
            for k in (0, 1)])
n_loc = gop("loc_test")
print(f"định vị: {n_loc}/{8 if TEST else 4463}", flush=True)
if ok and n_loc == (8 if TEST else 4463):
    ok = chay2([(T + ["--edit-val", "--editor", AD["ed_gold"], "--crop", "pred", "--points", f"{O}/loc_test.jsonl",
                      "--ck500-pred", f"{W}/pred_ck500_test.jsonl", "--out", f"{O}/pred_test_s{k}.jsonl",
                      "--shard", str(k)] + ROWS + NV, f"{O}/edit_test_s{k}.log", k) for k in (0, 1)])
D = {}
for k in (0, 1):
    p = f"{O}/pred_test_s{k}_meta.jsonl"
    if os.path.exists(p):
        for d in map(json.loads, open(p, encoding="utf-8")): D[(d["episode_id"], d["step_id"])] = d
print(f"sửa câu: {len(D)}/{8 if TEST else 4463}", flush=True)
```

`[locate-val]` cuối log mỗi shard: `không đọc được toạ độ` phải nhỏ (val: 0). `[edit-val pred]`: đổi câu
khoảng 60–75% (val 69,9%), 0 câu tiếng Việt.

## Ô 5 — cổng τ (chọn trên val) + chấm các câu được nhận sửa

```python
TAU = 0.73767
NEED = 8 if TEST else 4463
if len(D) == NEED:
    nhan = {k: d for k, d in D.items() if d["lp_edit"] - d["lp_draft"] > TAU and d["edit"] != d["draft"]}
    with open(f"{O}/pred_test_cong.jsonl", "w", encoding="utf-8") as f:
        for (e, s), d in nhan.items():
            f.write(json.dumps({"episode_id": e, "step_id": s, "pred": d["edit"]}, ensure_ascii=False) + "\n")
    print(f"cổng τ={TAU}: nhận sửa {len(nhan)}/{len(D)} câu ({100*len(nhan)/len(D):.1f}%; val 4,4%)", flush=True)
    if nhan:
        SC = f"{O}/score_pred_cong.json"
        q = subprocess.run(["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground",
                            "--preds", f"{O}/pred_test_cong.jsonl", "--out", SC, "--n", "99999"],
                           cwd=WS, capture_output=True, text=True,
                           env={**os.environ, "CUDA_VISIBLE_DEVICES": "0", "TQDM_DISABLE": "1"})
        open(f"{O}/cham_pred_cong.log", "w").write(q.stdout + q.stderr)
        print((q.stdout + q.stderr)[-900:], flush=True)
        R = [json.loads(l) for l in open(SC.replace(".json", "_raw.jsonl"))]
        print(f"== chấm {len(R)} câu nhận sửa · exec {sum(int(r['executable']) for r in R)}", flush=True)
else:
    print("⚠️ chưa đủ câu sửa — KHÔNG chấm. Commit sau: thêm output này làm Input, chạy lại Ô 1 → Ô 5.", flush=True)
print(f"XONG · {(time.time()-T0)/3600:.2f} h", flush=True)
```

`--n 99999` là để bản `score_run.py` cũ chấm một tập con có chủ ý (không có cờ này nó dừng khi thiếu > 1%
bước). Bước nào không có trong tệp thì không chấm — phần đó gộp từ ck500 test trên WSL.

## Chạy

1. **Thử tương tác** (`TEST = True`): *Run All*, khoảng 15–25 phút (hoà S1 + 8 bước định vị + 8 bước sửa
   + chấm vài câu). Gửi về output Ô 1, Ô 2, Ô 4, Ô 5. Phải thấy 2 card T4, `[hàng] … shard 0/2 … 2232` và
   `shard 1/2 … 2231`, không dòng DỪNG.
2. Ổn thì sửa Ô 3 `TEST = False` → **Stop session** → **Save Version → Save & Run All** (commit). Gập máy được.
3. Cuối log commit phải có `định vị: 4463/4463`, `sửa câu: 4463/4463`, `cổng τ=…: nhận sửa N/4463`,
   `== chấm N câu nhận sửa`, `XONG`.
4. **Bị dừng ở mốc 10,5 h** (`⛔ tới mốc 10,5 h`): mở notebook → *Add Input* → output của version vừa chạy
   (thư mục `tage_test_out/`) → Save & Run All lần nữa. Ô 2 tự chép phần dở về, `tage_val.py` bỏ qua các bước
   đã có.
5. Tải từ Output về **`runs/tage_test/`** trên WSL: cả thư mục `tage_test_out/`. Báo trợ lý để gộp với
   `score_ck500_test_raw.jsonl` và so S1/101 trên đủ 13 cột (0 GPU).

## Commit 2 (tuỳ chọn) — đối chứng `none` (sửa câu không vùng cắt)

Cùng notebook (Ô 1–3 giữ nguyên), thay Ô 4–5 bằng ô dưới. `none` không cần bộ định vị nên chỉ có pha sửa câu;
cổng nhận sửa nhiều (val 43%) nên pha chấm dài hơn (ước ~1.900 câu × 4 s ≈ 2 h).

```python
ok = chay2([(T + ["--edit-val", "--editor", AD["ed_none"], "--crop", "none",
                  "--ck500-pred", f"{W}/pred_ck500_test.jsonl", "--out", f"{O}/none_test_s{k}.jsonl",
                  "--shard", str(k)] + ROWS + NV, f"{O}/edit_none_s{k}.log", k) for k in (0, 1)])
D = {}
for k in (0, 1):
    p = f"{O}/none_test_s{k}_meta.jsonl"
    if os.path.exists(p):
        for d in map(json.loads, open(p, encoding="utf-8")): D[(d["episode_id"], d["step_id"])] = d
TAU = -0.04327
NEED = 8 if TEST else 4463
print(f"sửa câu none: {len(D)}/{NEED}", flush=True)
if len(D) == NEED:
    nhan = {k: d for k, d in D.items() if d["lp_edit"] - d["lp_draft"] > TAU and d["edit"] != d["draft"]}
    with open(f"{O}/none_test_cong.jsonl", "w", encoding="utf-8") as f:
        for (e, s), d in nhan.items():
            f.write(json.dumps({"episode_id": e, "step_id": s, "pred": d["edit"]}, ensure_ascii=False) + "\n")
    print(f"cổng τ={TAU}: nhận sửa {len(nhan)}/{len(D)}", flush=True)
    SC = f"{O}/score_none_cong.json"
    q = subprocess.run(["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground",
                        "--preds", f"{O}/none_test_cong.jsonl", "--out", SC, "--n", "99999"],
                       cwd=WS, capture_output=True, text=True, env={**os.environ, "CUDA_VISIBLE_DEVICES": "0"})
    open(f"{O}/cham_none_cong.log", "w").write(q.stdout + q.stderr); print((q.stdout + q.stderr)[-900:], flush=True)
print(f"XONG · {(time.time()-T0)/3600:.2f} h", flush=True)
```

## Dừng và gửi log khi

thiếu card thứ hai · dòng DỪNG ở Ô 2 · hoà lỗi · `không đọc được toạ độ` > 10% · `đổi câu` 0% hoặc > 90% ·
câu tiếng Việt > 0 · mã thoát ≠ 0 ở bất kỳ shard nào.

⚠️ Khác lượt val, phải khai khi báo số: S1 hoà ở **fp16 trên T4** (lượt val hoà bf16 trên L4, bộ biên tập và bộ
định vị train trên bản bf16 đó). ck500 test cũng sinh trên bản hoà fp16 T4, nên câu nháp khớp đường sinh.
