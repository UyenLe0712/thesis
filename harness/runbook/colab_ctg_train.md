# CTG-GRPO — train A3 / A2 / A4 / A7 trên Colab (4/10/2026, bản 2: nhiều nhánh một GPU)

Thi hành 276 §4 bước 4–6. **Trước khi chạy, làm `harness/runbook/colab_ctg_toi_uu.md`** để chốt máy, cấu hình
lô và số nhánh chạy chung một GPU. Notebook này chạy **một hoặc nhiều nhánh cùng lúc trên một GPU**
(`ARMS` ở Ô C1), mỗi nhánh là một tiến trình riêng, thư mục riêng.

| nhánh | bước | thứ tự |
|---|---:|---|
| A3 (đề xuất) | 1000 | đợt 1 |
| A2 (tắt CTG) | 1000 | đợt 1 |
| A4 (lấy mẫu lại) | 500 | đợt 2, chỉ khi A3 qua K1/K2 ở bước 500 |
| A7 (cộng loại) | 500 | đợt 2, ⚠️ chờ user chốt dấu |

Bốn luật Colab (CLAUDE.md) áp nguyên: `start_new_session=True` · không bấm Stop ô nào khi đang train ·
theo dõi log **local** · luôn có **một ô foreground** chạy suốt lượt (Ô C6).

## Chuẩn bị Drive (một lần)

`MyDrive/thesis/ctg/` chứa `fgrb_p1_bundle.zip` (2,7 GB, từ `_bundles/`) và thư mục `ctg-grpo-script/`
(6 tệp của `_bundles/ctg-grpo-script/`, md5 ở Ô C2).

## Ô C1 — cấu hình, Drive, gói

```python
# ===== SỬA Ở ĐÂY =====
ARMS = {"A3": 1000, "A2": 1000}       # nhánh: số bước. Một nhánh/GPU: {"A3": 1000}. Đợt 2: {"A4": 500, "A7": 500}
BS, ACC, NO_GC = 4, 4, False          # chốt ở colab_ctg_toi_uu.md; BS × ACC = 16; MỌI nhánh dùng chung
SAVE = 50                             # lưu mỗi 50 bước: mất máy chỉ mất ≤ 49 bước. K2 vẫn có checkpoint-250/500
TAT_MAY = True                        # xong hết ⇒ chép Drive, flush, tự trả máy (hết tính tiền)
# =====================
import os, sys, subprocess, time, glob, json, shutil, hashlib, re
from google.colab import drive
drive.mount("/content/drive")
D = "/content/drive/MyDrive/thesis/ctg"
W = "/content/ctg"; os.makedirs(W, exist_ok=True)
assert BS * ACC == 16 and 250 % SAVE == 0
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes 'trl==0.29.1' 2>&1 | tail -3")
sh(f'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__)"')
```

Ghi lại dòng phiên bản (`trl` phải 0.29.1). Hai phiên song song phải cùng bản `transformers`.

## Ô C2 — bung dữ liệu, chép mã, md5, đích

```python
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
if not os.path.exists(f"{W}/fgrb_p1_bundle/p1_train_rows.jsonl"):
    sh(f"cp {D}/fgrb_p1_bundle.zip /content/ && unzip -q -o /content/fgrb_p1_bundle.zip -d {W} && rm /content/fgrb_p1_bundle.zip")
BUNDLE = f"{W}/fgrb_p1_bundle"
MD5 = {"ctg_grpo.py": "332765b7c3657c1117ada5bf6ea3b936", "grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf",
       "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912", "metric_exec.py": "9bf0b84145458fd55919a5e161b9766f",
       "kl_ck500_theo_buoc.json": "828ce31811540195c34ecdbdee85d863", "ctg_s1_dich.json": "24df52354e73710069be027fe9db03c6"}
for f, h in MD5.items():
    shutil.copy(f"{D}/ctg-grpo-script/{f}", f"{W}/{f}")
    assert md5(f"{W}/{f}") == h, f"DỪNG: {f} lệch bản máy nhà"
DICH = f"{W}/ctg_s1_dich.json"
print("đích:", json.load(open(DICH))["dich"])
print("ảnh:", len(os.listdir(f"{BUNDLE}/images")), "· md5 khớp")
```

## Ô C3 — hoà S1 (bf16), bỏ qua nếu đã có

```python
MERGED = "/content/s1_merged"
r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED],
                   cwd=W, capture_output=True, text=True)
print((r.stdout + r.stderr)[-1500:]); assert r.returncode == 0
```

## Ô C4 — kéo điểm lưu từ Drive (khi máy mất), rồi khởi động mọi nhánh

```python
CAN = ("trainer_state.json", "optimizer.pt", "adapter_model.safetensors", "ctg_state.json")
P, T0 = {}, time.time()
for arm, n in ARMS.items():
    out, dout, log = f"{W}/{arm}", f"{D}/{arm}", f"/content/train_{arm}.log"
    os.makedirs(out, exist_ok=True); os.makedirs(dout, exist_ok=True)
    du = [p for p in glob.glob(f"{dout}/checkpoint-*") if all(os.path.exists(f"{p}/{f}") for f in CAN)]
    for p in du:
        shutil.copytree(p, f"{out}/{os.path.basename(p)}", dirs_exist_ok=True)
    if os.path.exists(f"{dout}/ctg_log.jsonl") and not os.path.exists(f"{out}/ctg_log.jsonl"):
        shutil.copy(f"{dout}/ctg_log.jsonl", f"{out}/ctg_log.jsonl")
    print(arm, "· điểm lưu kéo về:", sorted((os.path.basename(p) for p in du), key=lambda s: int(s.split('-')[1]))[-3:])
    if os.path.exists(f"{dout}/final/adapter_model.safetensors"):
        print(arm, "· ĐÃ XONG từ trước, bỏ qua"); continue
    cmd = ["python", "ctg_grpo.py", "--train", "--arm", arm, "--no-q4", "--bundle", BUNDLE, "--merged", MERGED,
           "--out", out, "--max-steps", str(n), "--save-steps", str(SAVE), "--resume", "auto", "--dich", DICH,
           "--bs", str(BS), "--accum", str(ACC)] + (["--no-gc"] if NO_GC else [])
    P[arm] = subprocess.Popen(cmd, cwd=W, stdout=open(log, "a"), stderr=subprocess.STDOUT, start_new_session=True,
                              env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
                                   "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"})
    print(arm, "· PID", P[arm].pid, flush=True)
    time.sleep(90)          # lệch pha nạp mô hình giữa các nhánh, tránh đỉnh RAM/VRAM cùng lúc
```

## Ô C5 — chép sang Drive mỗi 5 phút (chạy nền)

```python
import threading
def chep(arm, het=False):
    out, dout, log = f"{W}/{arm}", f"{D}/{arm}", f"/content/train_{arm}.log"
    for p in glob.glob(f"{out}/checkpoint-*"):
        dst = f"{dout}/{os.path.basename(p)}"
        if all(os.path.exists(f"{p}/{f}") for f in CAN) and not os.path.exists(f"{dst}/ctg_state.json"):
            shutil.copytree(p, dst, dirs_exist_ok=True)
    for f in ("ctg_log.jsonl", "log_history.json", "prompt_keys.json"):
        if os.path.exists(f"{out}/{f}"): shutil.copy(f"{out}/{f}", f"{dout}/{f}")
    if het and os.path.isdir(f"{out}/final"):
        shutil.copytree(f"{out}/final", f"{dout}/final", dirs_exist_ok=True)
    shutil.copy(log, f"{dout}/train_{arm}_{time.strftime('%m%d')}.log")

def dong_bo():
    while any(p.poll() is None for p in P.values()):
        time.sleep(300)
        for arm in P:
            try: chep(arm)
            except Exception as e: print("⚠️ đồng bộ lỗi", arm, e, flush=True)
threading.Thread(target=dong_bo, daemon=True).start()
```

## Ô C6 — theo dõi mọi nhánh (FOREGROUND, đừng Stop), xong thì chép Drive và trả máy

```python
import ast, statistics as st
KL5 = {int(k): v for k, v in json.load(open(f"{W}/kl_ck500_theo_buoc.json"))["kl"].items()}

def doc(arm):
    log, out, n = f"/content/train_{arm}.log", f"{W}/{arm}", ARMS[arm]
    L = open(log, encoding="utf-8", errors="ignore").read().splitlines()
    it = [i for i, l in enumerate(L) if l.startswith("[tiếp từ]")]
    goc = int(re.findall(r"checkpoint-(\d+)", L[it[-1]])[0]) if it and "checkpoint-" in L[it[-1]] else 0
    D_ = []
    for l in L[it[-1] if it else 0:]:
        if l.startswith("{'loss'"):
            try: D_.append({k: float(v) for k, v in ast.literal_eval(l).items()
                            if re.match(r"^-?[\d.]+(e[-+]?\d+)?$|^nan$", str(v))})
            except Exception: pass
    cd = [l for l in L if l.startswith("[cider]") and "lần" in l][-20:]
    th = [float(re.search(r"thưởng TB (-?[\d.]+)", l).group(1)) for l in cd]
    tu = [float(re.search(r"số từ TB ([\d.]+)", l).group(1)) for l in cd]
    rong = sum(int(re.search(r"rỗng (\d+)", l).group(1)) for l in cd)
    buoc = goc + len(D_)
    m = f"[{arm}] bước {buoc}/{n} (tiếp từ {goc})"
    for pat in ("[nạp default]", "[nạp ctg_state]"):
        x = [l for l in L if l.startswith(pat)]
        if x: m += f"\n      {x[-1][:110]}"
    if D_:
        kl = st.mean(d.get("kl", 0) for d in D_[-20:])
        ref = [KL5[b] for b in range(buoc - 19, buoc + 1) if b in KL5]
        m += (f"\n      20 bước: thưởng TB {st.mean(th) if th else float('nan'):.3f} · số từ TB {st.mean(tu) if tu else float('nan'):.1f}"
              f" · rỗng {rong}/{20*16} · kl TB {kl:.4f}" + (f" (ck500 cùng đoạn {st.mean(ref):.4f})" if ref else ""))
        # ck500 ở các bước đầu có kl ≈ 0 ⇒ "gấp 3 lần" vô nghĩa; chỉ xét khi mốc ≥ 0,002 (5/10, báo động giả lượt đầu)
        if ref and st.mean(ref) >= 0.002 and kl > 3 * st.mean(ref): m += "\n      ⛔ K3: KL gấp > 3 lần ck500 cùng đoạn"
        if rong > 0.01 * 20 * 16: m += "\n      ⛔ K3: câu rỗng > 1%"
        if any(v != v for d in D_[-5:] for v in d.values()): m += "\n      ⛔ có nan"
    if os.path.exists(f"{out}/ctg_log.jsonl"):
        C = [json.loads(l) for l in open(f"{out}/ctg_log.jsonl")]
        for g in ("scroll", "type", "navigate_back"):
            x = [r for r in C if r.get("lop") == g and "lam" in r]
            if x:
                ch = 0
                for r in reversed(x):
                    if r["lam"] >= 3.0: ch += 1
                    else: break
                m += f"\n      {g}: λ {x[-1]['lam']:.2f} · ĉ {x[-1]['chat']:.3f} · {len(x)} nhóm" + \
                     (f" · ⛔ K3: λ ở trần {ch} nhóm liền" if ch > 100 else "")
    may = [l for l in L if l.startswith("[máy]")]
    if may: m += f"\n      {may[-1][:150]}"
    if any("Traceback" in l or "OutOfMemory" in l for l in L[-60:]): m += "\n      ⛔ có Traceback/OOM"
    return m

while any(p.poll() is None for p in P.values()):
    time.sleep(120)
    gpu = subprocess.run("nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader",
                         shell=True, capture_output=True, text=True).stdout.strip()
    print(f"\n{(time.time()-T0)/3600:5.2f} h · GPU {gpu} · nhánh đang chạy {[a for a, p in P.items() if p.poll() is None]}", flush=True)
    for arm in P: print(doc(arm), flush=True)

for arm, p in P.items():
    print(arm, "· mã thoát", p.returncode)
    chep(arm, het=True)
    print("\n".join(open(f"/content/train_{arm}.log", errors="ignore").read().splitlines()[-8:]))
ok = {a: os.path.exists(f"{D}/{a}/final/adapter_model.safetensors") for a in P}
print("final trên Drive:", ok)
if TAT_MAY:
    drive.flush_and_unmount()            # đẩy hết tệp lên Drive TRƯỚC khi trả máy
    print("đã flush Drive, trả máy sau 60 s …", flush=True); time.sleep(60)
    from google.colab import runtime
    runtime.unassign()
```

⚠️ Nhánh nào lỗi giữa chừng (OOM…) thì Ô C6 vẫn đợi các nhánh còn lại rồi mới trả máy; điểm lưu của nhánh
lỗi đã nằm trên Drive. Chạy lại C1 → C6 với `ARMS` chỉ gồm nhánh đó, nó tự chạy tiếp.

## Đọc 15 phút đầu (mỗi nhánh)

- `[đích] nạp từ …ctg_s1_dich.json` · `[nhánh] A3 · trl 0.29.1` · `[cider] df dựng từ 3991`
- `[lô] mỗi lượt sinh 16 câu = 2 câu nhắc × 8 · micro-batch BS × ACC · gradient checkpointing …`
- `[thưởng] … CTG cộng vào advantage: True` (A3) / `False` (A2, A4, A7; A7 có `r_loai`; A4 có `[A4] trọng số lớp`)
- Lượt đầu `[tiếp từ] None`. Nối sau mất máy: `[tiếp từ] …checkpoint-N`, `[nạp default] … → x>0`, `[nạp ctg_state] bước N`.
- Sau ~20 bước: dòng `[máy]` có s/bước và đỉnh VRAM; dòng `GPU …` cho % sử dụng toàn GPU.
- Luật tốc độ 276 §8 (> 60 s/bước thì dừng) đọc theo **s/bước ÷ số nhánh chạy chung** khi chạy nhiều nhánh.

## Khi máy mất

Mở lại notebook, chạy C1 → C6 (giữ nguyên `ARMS`). Ô C4 tự kéo điểm lưu đủ tệp từ Drive, nhánh đã xong
thì bỏ qua. ⛔ C4 in `điểm lưu kéo về: []` mà Drive đang có điểm lưu ⇒ điểm lưu thiếu `ctg_state.json`: dừng, báo.

## Sau điểm lưu 250 / 500 (K1, K2) và khi xong

1. Drive `thesis/ctg/<ARM>/checkpoint-N/` → tải `adapter_config.json` + `adapter_model.safetensors`.
2. Máy nhà: `ctg_ckpt_upload/<ARM>_<N>/` chứa hai tệp đó → Kaggle dataset `ctg-ckpts` (New Version) →
   chấm theo `harness/runbook/kaggle_ctg_val.md`.
3. Khi xong: tải `ctg_log.jsonl`, `log_history.json`, `train_<ARM>_*.log` về `runs/ctg/<ARM>/`.
4. Lưu mỗi 50 bước ⇒ ~20 điểm lưu × ~240 MB mỗi nhánh trên Drive. Xong việc thì xoá các điểm lưu không chia hết
   cho 250 cho nhẹ Drive (giữ 250/500/750/1000).
