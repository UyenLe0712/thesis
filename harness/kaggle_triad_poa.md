# Kaggle (commit) — TRIAD-T pha POA: listener ShowUI-2B + chấm UI-Venus (action 273 §5, 4/10/2026)

**Một commit, T4 ×2, ước 4–5 h** (chưa đo; Ô 4 in `s/lời gọi` thật ngay sau 3 lời gọi đầu).

| bước | máy | việc | số lời gọi |
|---|---|---|---|
| A | GPU0 | ShowUI-2B (fp32) đọc mọi câu duy nhất của 249 click: ck500 · S1 k0…k8 · câu chuẩn (câu chuẩn **chỉ** để đo hit_disk độc lập, bộ chọn không đọc) | 1.952 |
| B | GPU0+1 | UI-Venus-Ground-7B chấm ck500 + 8 mẫu S1 (`score_run.py --grounder uivenus`, cỡ 1.272 tok như phép B) | 9 × 249 = 2.241 |

UGround **không chạy lại**: mọi câu ứng viên của POA (ck500 + k1…k8) đã được UGround chấm sẵn
(`runs/tage_val/that/score_ck500_l4_raw.jsonl`, `runs/c1/exec8/c1score/score_k*_raw.jsonl`), nên bảng POA
dưới UGround tính ở máy nhà, 0 GPU. UI-Venus chấm **mọi** ứng viên chứ không chỉ cấu hình thắng, để bộ chọn
không phải chờ và không có đường nào cho UI-Venus chen vào khâu chọn.

A chạy trước, B sau (UI-Venus 7B fp16 cần cả hai card, đặt chung với ShowUI fp32 dễ tràn bộ nhớ).

## Chuẩn bị (máy nhà → Kaggle)

1. Dataset mới **`triad-t-script`** (Private): kéo cả 11 tệp trong `_bundles/triad-t-script/`.

   | tệp | md5 |
   |---|---|
   | `triad_listener.py` | `951cc70738677c9bee5baed7d1fbae69` |
   | `calls_poa.jsonl` (1.952 lời gọi) | `b68f00675e94f8fa6bc53d7139633ab1` |
   | `pred_venus_ck500.jsonl` | `eb6162d86730a936beb5ae5a9fd6d652` |
   | `pred_venus_k1.jsonl` … `k8` | xem Ô 2 |

2. Notebook mới. *Session options*: **GPU T4 ×2**, **Internet On**.
   *Add Input*: `c1-exec8` · `thesis-val-cham` · `triad-t-script`.
   Nếu commit trước bị cắt giữa chừng: thêm **Output của commit đó** làm Input (Ô 2 tự chép phần dở về).

   ⚠️ Dùng nick thứ hai: dataset Kaggle là Private theo tài khoản ⇒ hoặc *Share* ba dataset trên cho nick kia,
   hoặc upload lại. Dataset `c1-exec8` và `thesis-val-cham` hiện nằm ở nick đã chạy TAGE.

## Ô 1 — gói

```python
import subprocess, sys, os, time
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh(f"{sys.executable} -m pip install -q -U transformers accelerate pillow 2>&1 | tail -3")
sh(f'{sys.executable} -c "import transformers, torch; print(transformers.__version__, torch.__version__, torch.cuda.device_count(), torch.cuda.get_device_name(0))"')
```

Phải thấy **2** card Tesla T4.

## Ô 2 — đường dẫn, md5, chép phần dở của commit trước

```python
import glob, json, shutil, hashlib
T0 = time.time()
TEST = True                       # chạy thử tương tác; đổi False trước khi commit
HAN = T0 + 10.5 * 3600            # quá mốc này thì dừng, chừa giờ lưu Output dưới trần 12 h
W = "/kaggle/working"
O = f"{W}/triad_poa_out"; os.makedirs(O, exist_ok=True)
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
MD = {"triad_listener.py": "951cc70738677c9bee5baed7d1fbae69", "calls_poa.jsonl": "b68f00675e94f8fa6bc53d7139633ab1",
      "pred_venus_ck500.jsonl": "eb6162d86730a936beb5ae5a9fd6d652",
      "pred_venus_k1.jsonl": "8a7aa34e171b3c4a9bf22ae8be0125b2", "pred_venus_k2.jsonl": "d8b4283a1b2e811f69a7fa40e5b6e75a",
      "pred_venus_k3.jsonl": "1561e5d4365a331d5858ccf235f65d5e", "pred_venus_k4.jsonl": "5a25c14dc411dbf567dd720727219f99",
      "pred_venus_k5.jsonl": "04cd9c21b0ef45dd11bb47a433af83ba", "pred_venus_k6.jsonl": "d8b9d2632afbc3fa30a90ce4279d2b30",
      "pred_venus_k7.jsonl": "e1646899ad26939b44654919fd6259c0", "pred_venus_k8.jsonl": "eea9a15f25fd186f4cdb75f97ba49741"}
SRC = sorted({os.path.dirname(p) for p in glob.glob("/kaggle/input/**/calls_poa.jsonl", recursive=True)
              if "triad_poa_out" not in p})
assert len(SRC) == 1, f"DỪNG: cần đúng một triad-t-script, thấy {SRC}"
for f, h in MD.items():
    shutil.copy(f"{SRC[0]}/{f}", f"{W}/{f}")
    assert md5(f"{W}/{f}") == h, f"DỪNG: {f} lệch md5"

# commit trước bị cắt: chép các tệp *.jsonl dở về (bỏ dòng ghi dở) để hai script tự nối tiếp
for p in glob.glob("/kaggle/input/**/triad_poa_out/*.jsonl", recursive=True):
    d = f"{O}/{os.path.basename(p)}"
    if not os.path.exists(d):
        ok = []
        for l in open(p, encoding="utf-8"):
            try: json.loads(l); ok.append(l)
            except ValueError: pass
        open(d, "w", encoding="utf-8").writelines(ok); print("nối tiếp:", os.path.basename(p), len(ok), "dòng")
print("SRC", SRC[0], "· TEST", TEST, flush=True)
```

## Ô 3 — dựng dữ liệu C1 (nguyên văn Ô 7 của `kaggle_tage_val.md`, bỏ phần k0)

```python
cand = sorted({os.path.dirname(p) for p in glob.glob("/kaggle/input/**/c1_picks.json", recursive=True)
               if os.path.exists(os.path.join(os.path.dirname(p), "c1_mau.jsonl"))})
assert len(cand) == 1, f"DỪNG: cần đúng một gói c1-exec8, thấy {cand}"
PK = cand[0]
assert md5(f"{PK}/c1_mau.jsonl") == "d757554326977309c3a65ae0b144c211"
WS = f"{W}/pk/thesis"
shutil.copytree(f"{PK}/thesis", WS, dirs_exist_ok=True)
sr = open(f"{WS}/harness/score_run.py", encoding="utf-8").read()
assert "--recs-file" in sr and "TỆP THÔ KHÔNG KHỚP" in sr, "DỪNG: score_run.py là bản cũ"
assert "VENUS_MIN_PIXELS" in sr[sr.index("class UIVenus"):], "DỪNG: UIVenus chưa đọc VENUS_*_PIXELS"

v600 = sorted(glob.glob("/kaggle/input/**/val_cham600.jsonl", recursive=True), key=len)
v600 = [p for p in v600 if all(os.path.exists(os.path.join(os.path.dirname(p), f))
                                for f in ("val_cham400.jsonl", "ocr.jsonl", "images"))]
assert v600, "DỪNG: không thấy thesis-val-cham đủ bộ"
BASE = os.path.dirname(v600[0])
C1 = [json.loads(l) for l in open(f"{PK}/c1_mau.jsonl", encoding="utf-8")]
assert len(C1) == 400
TAPT = ("click", "long_press")
KEYS = {(r["episode_id"], r["step_id"]) for r in C1}
VD = f"{W}/c1data"; os.makedirs(VD, exist_ok=True)
recs = {}
for f in ("val_cham400.jsonl", "val_cham600.jsonl"):
    for d in map(json.loads, open(f"{BASE}/{f}", encoding="utf-8")):
        k = (d["episode_id"], d["step_id"])
        if k in KEYS and k not in recs:
            d.setdefault("gold_instruction", d["target_instruction"]); recs[k] = d
assert len(recs) == 400, f"DỪNG: chỉ ghép được {len(recs)}/400 bước C1"
with open(f"{VD}/c1_recs.jsonl", "w", encoding="utf-8") as fo:
    for r in C1:
        fo.write(json.dumps(recs[(r["episode_id"], r["step_id"])], ensure_ascii=False) + "\n")
shutil.copy(f"{BASE}/ocr.jsonl", f"{VD}/ocr.jsonl")
if os.path.lexists(f"{VD}/images"): os.remove(f"{VD}/images")
os.symlink(f"{BASE}/images", f"{VD}/images")
taps = [d for d in recs.values() if d["action"].get("action_type") in TAPT and "x" in d["action"]]
assert len(taps) == 249 and all(os.path.exists(f"{VD}/{d['image']}") for d in taps)

CALLS = [json.loads(l) for l in open(f"{W}/calls_poa.jsonl", encoding="utf-8")]
assert len(CALLS) == 1952 and all(os.path.exists(f"{VD}/{c['image']}") for c in CALLS), "DỪNG: thiếu ảnh cho listener"
sys.path.insert(0, f"{WS}/harness")
import a11y_inventory as A11Y, score_run as SR
names = set(A11Y._zip().namelist())
co_cay = sum(A11Y.key_for(f"episode_{d['episode_id']}_screenshot_{d['step_id']}.png") in names for d in taps)
rong = sum(len(SR.buttons_of(d)) == 0 for d in taps)
print(f"cây trợ năng: {co_cay}/249 · {rong} bước rỗng nút · 1.952 lời gọi đủ ảnh", flush=True)
assert co_cay == 249 and rong == 0, "DỪNG: thiếu cây trợ năng ⇒ Voronoi chấm sai mà không báo"
```

## Ô 4 — hàm chạy có nhịp sống (2 phút, đọc dòng cuối log)

```python
def chay(cmd, log, gpus, cwd=W, env_them=None):
    """Chạy nền, stdout ra tệp; in dòng cuối log mỗi 2 phút (30 s khi TEST). Quá HAN thì dừng."""
    env = {**os.environ, "CUDA_VISIBLE_DEVICES": gpus, "TQDM_DISABLE": "1", "PYTHONUNBUFFERED": "1",
           "HF_HUB_DISABLE_PROGRESS_BARS": "1", **(env_them or {})}
    with open(log, "a") as f:
        q = subprocess.Popen(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT, env=env)
    while q.poll() is None:
        time.sleep(30 if TEST else 120)
        L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
        print(f"  {(time.time()-T0)/3600:5.2f} h · {os.path.basename(log)} · {L[-1][:140] if L else '...'}", flush=True)
        if time.time() > HAN:
            q.terminate(); print("⛔ tới mốc 10,5 h — dừng; commit sau thêm Output này làm Input để nối tiếp", flush=True)
            return False
    print(f"--- {os.path.basename(log)} · mã thoát {q.returncode}\n" + "".join(open(log, errors="ignore").readlines()[-5:]), flush=True)
    return q.returncode == 0
```

## Ô 5 — A: listener ShowUI-2B trên GPU0

```python
ok_A = chay(["python", "-u", "triad_listener.py", "--calls", "calls_poa.jsonl", "--img-root", VD,
             "--out", f"{O}/listener_showui.jsonl"] + (["--n", "10"] if TEST else []),
            f"{O}/listener_showui.log", "0")
R = [json.loads(l) for l in open(f"{O}/listener_showui.jsonl", encoding="utf-8")]
print(f"== listener: {len(R)} dòng · đọc được {sum(d['ok'] for d in R)} · "
      f"s/lời gọi trung vị {sorted(d['sec'] for d in R)[len(R)//2]:.2f}", flush=True)
for d in R[:5]: print("   ", d["nguon"], repr(d["sent"][:50]), "→", repr(d["raw"]), d["xy"], flush=True)
```

**Kiểm ở lượt thử** (gửi về đúng các dòng này): `[listener] image_processor min=200704 max=1053696 …`,
`dtype thật torch.float32`, `VRAM đỉnh`, `s/lời gọi`, và 5 dòng `raw`. `raw` phải có dạng `[0.xx, 0.yy]`.
Nếu `raw` ra số > 1 (thang khác) hoặc chữ ⇒ **dừng, gửi về** — sửa quy đổi một lần theo §5.4, không tự đoán.

## Ô 6 — B: UI-Venus chấm ck500 + k1…k8 (cả hai card, cỡ 1.272 tok)

```python
VEN = {"VENUS_MIN_PIXELS": "200704", "VENUS_MAX_PIXELS": "1003520"}   # 1.272 tok — đúng cỡ đã chốt ở phép B
ok_B = True
for ten in ["ck500"] + [f"k{i}" for i in range(1, 9)]:
    if not ok_B: break
    ok_B = chay(["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uivenus",
                 "--preds", f"{W}/pred_venus_{ten}.jsonl", "--data-root", VD, "--recs-file", "c1_recs.jsonl",
                 "--out", f"{O}/score_venus_{ten}.json"] + (["--n", "3"] if TEST else []),
                f"{O}/cham_venus_{ten}.log", "0,1", cwd=WS, env_them=VEN)
    p = f"{O}/score_venus_{ten}_raw.jsonl"
    if os.path.exists(p):
        V = [json.loads(l) for l in open(p)]
        print(f"== UI-Venus {ten}: {len(V)} bước · exec {sum(int(v['executable']) for v in V)}", flush=True)
```

Dòng `[UIVenus] xin min=200,704 max=1,003,520 → image_processor giữ min=200704 max=1003520` phải xuất hiện
trong `cham_venus_ck500.log`. Thiếu dòng đó, hoặc giá trị khác ⇒ dừng.

## Ô 7 — kiểm đủ + gói một zip

```python
n_L = sum(1 for _ in open(f"{O}/listener_showui.jsonl"))
n_V = {t: sum(1 for _ in open(f"{O}/score_venus_{t}_raw.jsonl")) if os.path.exists(f"{O}/score_venus_{t}_raw.jsonl") else 0
       for t in ["ck500"] + [f"k{i}" for i in range(1, 9)]}
du = n_L == 1952 and all(v == 249 for v in n_V.values())
print(f"listener {n_L}/1952 · UI-Venus {n_V} ⇒ {'ĐỦ' if du else 'CHƯA ĐỦ — commit sau nối tiếp'}", flush=True)
shutil.rmtree(f"{W}/pk", ignore_errors=True); shutil.rmtree(VD, ignore_errors=True)
shutil.make_archive(f"{W}/triad_poa_out", "zip", W, "triad_poa_out")
print("zip:", os.path.getsize(f"{W}/triad_poa_out.zip") // 1024, "KB ·", sorted(os.listdir(O)), flush=True)
```

## Chạy

1. **Thử tương tác** (`TEST = True`, ~15 phút): *Run All*. Gửi về output Ô 3, Ô 5 (các dòng `[listener]` + 5
   dòng raw), Ô 6 (dòng `[UIVenus] xin …` + 9 dòng `== UI-Venus`). Số của lượt thử **không đọc thành kết quả**.
2. Ổn thì: Ô 2 `TEST = False` → *Stop session* → *Save Version → Save & Run All (Commit)*.
3. Commit xong: tải `triad_poa_out.zip`, giải nén vào **`runs/triad_t/poa/`** (đặt thẳng vào thư mục phép đo).
4. Máy nhà, 0 GPU:
   ```
   python3 harness/triad_t.py --poa --listener runs/triad_t/poa/listener_showui.jsonl --name showui \
       --venus-dir runs/triad_t/poa --out runs/triad_t/poa_showui.json
   ```
   rồi đọc cổng §5.4 của action 273.
