# CTG-GRPO — train A3 / A2 / A4 / A7 trên Colab (4/10/2026)

Thi hành 276 §4 bước 4–6. **Chỉ chạy khi P0 (`harness/kaggle_ctg_p0.md`) đã ĐẠT cả (a) lẫn (b).**
Một notebook, một nhánh mỗi lượt: đổi `ARM` ở Ô C1. Thứ tự: **A3 → A2 → A4 → A7**.

| nhánh | `MAX_STEPS` | lưu mỗi | ước giờ A100 (≤ 60 s/bước) |
|---|---:|---:|---|
| A3 | 1000 | 250 | ≤ 17 h |
| A2 | 1000 | 250 | ≤ 17 h |
| A4 | 500 | 250 | ≤ 8,5 h |
| A7 | 500 | 250 | ≤ 8,5 h |

Bốn luật Colab (CLAUDE.md) áp nguyên: `start_new_session=True` · không bấm Stop ô nào khi đang train ·
theo dõi log **local** · luôn có **một ô foreground** chạy suốt lượt (Ô C6).

## Bước 0 — chọn máy (luật CLAUDE.md, 10 phút đầu)

P0 cho s/bước trên T4. Trước khi chốt A100, chạy Ô C1–C6 trên **L4** với `MAX_STEPS = 20`
(`ARM = "A3"`, thư mục ra riêng `ctg_probe_L4`), đọc s/bước ở dòng theo dõi sau ~20 bước, rồi làm lại
trên A100. **L4 / A100 ≤ 1,5× thì train trên L4.** Trên 1,5× mới dùng A100. Ở cả hai máy: trên 60 s/bước
(A100) thì **dừng và báo** (276 §8).
⚠️ L4 chưa từng chạy GRPO ở dự án này; đỉnh VRAM T4 ở P0 cho biết L4 (22 GB) có đủ hay không.

## Chuẩn bị Drive (một lần)

`MyDrive/thesis/ctg/` chứa:
- `fgrb_p1_bundle.zip` — chép từ `_bundles/fgrb_p1_bundle.zip` (2,7 GB)
- `ctg-grpo-script/` — 5 tệp của `_bundles/ctg-grpo-script/` (md5 ở `kaggle_ctg_p0.md`)

## Ô C1 — Drive, GPU, gói

```python
ARM, MAX_STEPS = "A3", 1000          # A3 1000 · A2 1000 · A4 500 · A7 500
import os, sys, subprocess, time, glob, json, shutil, hashlib
from google.colab import drive
drive.mount("/content/drive")
D = "/content/drive/MyDrive/thesis/ctg"
DOUT = f"{D}/{ARM}"                   # bản sao trên Drive
os.makedirs(DOUT, exist_ok=True)
W = "/content/ctg"; os.makedirs(W, exist_ok=True)
OUT = f"{W}/{ARM}"                    # train ghi ở đĩa local, Ô C5 chép sang Drive
LOG = f"/content/train_{ARM}.log"

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes 'trl==0.29.1' 2>&1 | tail -3")
sh(f'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__)"')
```

Ghi lại dòng phiên bản; phải trùng bản P0 (Kaggle) ở `trl` (0.29.1). `transformers` lệch bản P0 thì ghi lại để khai.

## Ô C2 — bung dữ liệu, chép mã, md5

```python
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
if not os.path.exists(f"{W}/fgrb_p1_bundle/p1_train_rows.jsonl"):
    sh(f"cp {D}/fgrb_p1_bundle.zip /content/ && unzip -q -o /content/fgrb_p1_bundle.zip -d {W} && rm /content/fgrb_p1_bundle.zip")
BUNDLE = f"{W}/fgrb_p1_bundle"
MD5 = {"ctg_grpo.py": "0294cc93004e4c8501f470c7158ad3d0", "grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf",
       "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912", "metric_exec.py": "9bf0b84145458fd55919a5e161b9766f",
       "kl_ck500_theo_buoc.json": "828ce31811540195c34ecdbdee85d863"}
for f, h in MD5.items():
    shutil.copy(f"{D}/ctg-grpo-script/{f}", f"{W}/{f}")
    assert md5(f"{W}/{f}") == h, f"DỪNG: {f} lệch bản máy nhà"
print("ảnh:", len(os.listdir(f"{BUNDLE}/images")), "· md5 khớp")
```

## Ô C3 — hoà S1 (bf16), bỏ qua nếu đã có

```python
MERGED = "/content/s1_merged"
r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED],
                   cwd=W, capture_output=True, text=True)
print((r.stdout + r.stderr)[-1500:]); assert r.returncode == 0
```

## Ô C4 — kéo điểm lưu từ Drive (khi máy mất giữa chừng), rồi train

```python
os.makedirs(OUT, exist_ok=True)
CAN = ("trainer_state.json", "optimizer.pt", "adapter_model.safetensors", "ctg_state.json")
du = [p for p in glob.glob(f"{DOUT}/checkpoint-*") if all(os.path.exists(f"{p}/{f}") for f in CAN)]
for p in du:
    shutil.copytree(p, f"{OUT}/{os.path.basename(p)}", dirs_exist_ok=True)
if os.path.exists(f"{DOUT}/ctg_log.jsonl") and not os.path.exists(f"{OUT}/ctg_log.jsonl"):
    shutil.copy(f"{DOUT}/ctg_log.jsonl", f"{OUT}/ctg_log.jsonl")
print("điểm lưu kéo về:", sorted(os.path.basename(p) for p in du))

cmd = ["python", "ctg_grpo.py", "--train", "--arm", ARM, "--no-q4", "--bundle", BUNDLE, "--merged", MERGED,
       "--out", OUT, "--max-steps", str(MAX_STEPS), "--save-steps", "250", "--resume", "auto"]
logf = open(LOG, "a")
P = subprocess.Popen(cmd, cwd=W, stdout=logf, stderr=subprocess.STDOUT, start_new_session=True,
                     env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
                          "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"})
T0 = time.time(); print("PID", P.pid, flush=True)
```

⚠️ Điểm lưu 250 bước một lần ⇒ mất máy thì mất tới 249 bước (≤ 4 h). Muốn ít rủi ro hơn thì đổi
`--save-steps` thành `50` (không đổi thuật toán; ⚠️ K2 vẫn đọc `checkpoint-250/500`, mỗi điểm lưu ~240 MB
trên Drive).

## Ô C5 — chép sang Drive mỗi 5 phút (chạy nền)

```python
import threading
def dong_bo():
    while P.poll() is None:
        time.sleep(300)
        try:
            for p in glob.glob(f"{OUT}/checkpoint-*"):
                dst = f"{DOUT}/{os.path.basename(p)}"
                if all(os.path.exists(f"{p}/{f}") for f in CAN) and not os.path.exists(f"{dst}/ctg_state.json"):
                    shutil.copytree(p, dst, dirs_exist_ok=True)
            for f in ("ctg_log.jsonl",):
                if os.path.exists(f"{OUT}/{f}"): shutil.copy(f"{OUT}/{f}", f"{DOUT}/{f}")
            shutil.copy(LOG, f"{DOUT}/train_{ARM}_{time.strftime('%m%d')}.log")
        except Exception as e:
            print("⚠️ đồng bộ lỗi:", e, flush=True)
threading.Thread(target=dong_bo, daemon=True).start()
```

## Ô C6 — theo dõi (FOREGROUND, để chạy suốt lượt, đừng Stop)

```python
import ast, re, statistics as st, collections
KL5 = {int(k): v for k, v in json.load(open(f"{W}/kl_ck500_theo_buoc.json"))["kl"].items()}

def doc():
    L = open(LOG, encoding="utf-8", errors="ignore").read().splitlines()
    tiep = [l for l in L if l.startswith("[tiếp từ]")]
    goc = int(re.findall(r"checkpoint-(\d+)", tiep[-1])[0]) if tiep and "checkpoint-" in tiep[-1] else 0
    D_ = []
    for l in L[[i for i, l in enumerate(L) if l.startswith("[tiếp từ]")][-1] if tiep else 0:]:
        if l.startswith("{'loss'"):
            try: D_.append({k: float(v) for k, v in ast.literal_eval(l).items()
                            if re.match(r"^-?[\d.]+(e[-+]?\d+)?$|^nan$", str(v))})
            except Exception: pass
    cd = [l for l in L if l.startswith("[cider]") and "lần" in l][-20:]
    th = [float(re.search(r"thưởng TB (-?[\d.]+)", l).group(1)) for l in cd]
    tu = [float(re.search(r"số từ TB ([\d.]+)", l).group(1)) for l in cd]
    rong = sum(int(re.search(r"rỗng (\d+)", l).group(1)) for l in cd)
    buoc = goc + len(D_)
    m = f"{(time.time()-T0)/3600:5.2f} h · {ARM} · bước {buoc}/{MAX_STEPS} (tiếp từ {goc})"
    for pat in ("[nạp default]", "[nạp ctg_state]"):
        x = [l for l in L if l.startswith(pat)]
        if x: m += f"\n      {x[-1][:110]}"
    if D_:
        spb = (time.time() - T0) / len(D_)
        kl = st.mean(d.get("kl", 0) for d in D_[-20:])
        ref = [KL5[b] for b in range(buoc - 19, buoc + 1) if b in KL5]
        m += (f"\n      {spb:.0f} s/bước · còn ~{(MAX_STEPS-buoc)*spb/3600:.1f} h"
              f"\n      20 bước: thưởng TB {st.mean(th) if th else float('nan'):.3f} · số từ TB {st.mean(tu) if tu else float('nan'):.1f}"
              f" · rỗng {rong}/{20*16} · kl TB {kl:.4f}" + (f" (ck500 cùng đoạn {st.mean(ref):.4f})" if ref else ""))
        if len(D_) >= 20 and spb > 60 and buoc - goc <= 25:
            m += "\n      ⛔ > 60 s/bước ở 20 bước đầu (276 §8): dừng và báo"
        if ref and st.mean(ref) > 0 and kl > 3 * st.mean(ref):
            m += "\n      ⛔ K3: KL gấp > 3 lần ck500 cùng đoạn"
        if rong > 0.01 * 20 * 16:
            m += "\n      ⛔ K3: câu rỗng > 1%"
        if any(v != v for d in D_[-5:] for v in d.values()):
            m += "\n      ⛔ có nan"
    if os.path.exists(f"{OUT}/ctg_log.jsonl"):
        C = [json.loads(l) for l in open(f"{OUT}/ctg_log.jsonl")]
        for g in ("scroll", "type", "navigate_back"):
            x = [r for r in C if r.get("lop") == g and "lam" in r]
            if x:
                chuoi = 0
                for r in reversed(x):
                    if r["lam"] >= 3.0: chuoi += 1
                    else: break
                m += f"\n      {g}: λ {x[-1]['lam']:.2f} · ĉ {x[-1]['chat']:.3f} · {len(x)} nhóm" + \
                     (f" · ⛔ K3: λ ở trần {chuoi} nhóm liền" if chuoi > 100 else "")
    if any("Traceback" in l or "OutOfMemory" in l for l in L[-60:]): m += "\n      ⛔ có Traceback/OOM"
    return m

while P.poll() is None:
    time.sleep(120)
    print(doc(), flush=True)
print("mã thoát", P.returncode)
print("\n".join(open(LOG, errors="ignore").read().splitlines()[-30:]))
for p in glob.glob(f"{OUT}/checkpoint-*") + [f"{OUT}/final", f"{OUT}/log_history.json", f"{OUT}/ctg_log.jsonl"]:
    if os.path.isdir(p): shutil.copytree(p, f"{DOUT}/{os.path.basename(p)}", dirs_exist_ok=True)
    elif os.path.exists(p): shutil.copy(p, f"{DOUT}/")
shutil.copy(LOG, f"{DOUT}/train_{ARM}_cuoi.log")
print("đã chép lên Drive:", sorted(os.listdir(DOUT)))
```

⚠️ K3 "λ ở trần liền hơn 100 lượt sinh": Ô C6 đếm theo **nhóm của lớp đó** (mỗi lượt sinh có 2 câu
nhắc, lớp hiếm nên 100 nhóm ≈ vài trăm bước). Ô C6 chỉ **báo**; dừng hay không là việc của người chạy.

## Đọc 15 phút đầu

- `[nhánh] A3 · trl 0.29.1` · `[cider] df dựng từ 3991` · `[lô] … 2 câu nhắc × 8` · `CTG cộng vào advantage: True`
  (A2/A4/A7: `False`; A7 có thêm `r_loai` trong `[thưởng]`; A4 có dòng `[A4] trọng số lớp`).
- Lượt đầu `[tiếp từ] None`. Lượt nối sau mất máy: `[tiếp từ] …checkpoint-N`, `[nạp default] … → x>0`,
  `[nạp ctg_state] bước N`.
- Sau 20 bước: s/bước ≤ 60 (A100).

## Khi máy mất

Mở lại notebook, chạy Ô C1 (giữ `ARM`) → C2 → C3 → C4 → C5 → C6. Ô C4 tự kéo điểm lưu đủ tệp từ Drive.
⛔ Nếu C4 in `điểm lưu kéo về: []` mà Drive đang có điểm lưu ⇒ điểm lưu thiếu `ctg_state.json`: dừng, báo.

## Sau mỗi điểm lưu 250 / 500 (K1, K2) và khi xong

1. Từ Drive `thesis/ctg/<ARM>/checkpoint-N/` tải **`adapter_config.json` + `adapter_model.safetensors`**.
2. Máy nhà: `ctg_ckpt_upload/<ARM>_<N>/` chứa hai tệp đó. Kaggle → dataset `ctg-ckpts` (New Version mỗi lần
   thêm). Rồi chấm theo `harness/kaggle_ctg_val.md`.
3. Khi xong: tải `ctg_log.jsonl`, `log_history.json`, `train_<ARM>_*.log` về `runs/ctg/<ARM>/`.
