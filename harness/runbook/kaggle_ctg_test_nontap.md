# CTG-GRPO — sinh câu A3_1000 và A2_1000 trên 2.495 bước KHÔNG chạm của TEST (5/10/2026)

Phép đo chính của CTG (`report/279` §4e, §6): trên bước cuộn / gõ / quay lại / chờ / mở ứng dụng của tập
kiểm, A3 (CTG bật) có giữ đúng loại thao tác tốt hơn A2 (CTG tắt) không, và có còn ngang S1 không.
Kaggle chỉ **sinh câu**; chấm ở máy nhà, **không gọi bộ trỏ**, 0 GPU.

Chép từ `kaggle_grpo_spice_nontap_ck500.md` (đường đã chạy 2/10: kiểm hoà 20/20, 2,94 s/bước), đổi ba chỗ:
- hai điểm lưu lấy từ dataset `ctg-ckpts` (cùng bản đã chấm val bước 1000);
- **chạy song song trên T4 ×2**: A3 ở GPU 0, A2 ở GPU 1, mỗi tiến trình một card ⇒ ~2,1 h thay vì ~4,2 h,
  tốn nửa hạn mức tuần;
- ô cuối đóng zip thư mục kết quả.

Điểm lưu chốt theo luật chọn trên val (279 §4e): **`checkpoint-1000` cho cả hai nhánh**. ⛔ Sinh **một lần**,
không sinh lại hay đổi điểm lưu sau khi thấy số.

## Luật đọc (279 §6, ghi trước khi có số)

| luật | đại lượng | đạt khi |
|---|---|---|
| R-CTG | scroll (755 bước), Δ(A3 − A2) | cận dưới KTC95 > 0 |
| R-noharm | scroll, Δ(A3 − S1) | Δ ≥ −3 điểm |
| R-noharm | toàn bộ 2.495 bước, Δ(A3 − S1) | cận dưới KTC95 ≥ −3 |

Mốc đã có trên đúng 2.495 bước này: S1 85,97 (scroll 83,97) · ck500 84,29 (scroll 77,75).
⚠️ Khai kèm: S1 sinh bằng `infer_branch` (LoRA chưa hoà), A3/A2/ck500 sinh trên S1 đã hoà fp16 ⇒ các cặp so
S1 lẫn biến đường sinh; cặp A3 − A2 và A3 − ck500 thì cùng đường, sạch.

## Chuẩn bị (máy nhà → Kaggle)

Không phải upload gì mới — mọi dataset đã có từ các lượt trước:

| dataset | dùng cho | đã có từ |
|---|---|---|
| `thesis-score` | `test.jsonl` · `ocr.jsonl` | mọi lượt chấm test |
| `fgrb-p1-bundle` | adapter S1/101 để hoà | lượt val CTG |
| `grpo-spice-script` | `gen_test_grpo.py` (có `--non-tap`, md5 `b18ec1aa…`) · `grpo_spice.py` · `preds_s1_seed101.jsonl` | lượt ck500 không chạm 2/10 |
| `ctg-ckpts` | `A3_1000/` · `A2_1000/` | lượt val bước 1000 |
| `thesis-nontap-images` | 2.495 ảnh không chạm | lượt ck500 không chạm 2/10 |

Notebook mới, **GPU T4 ×2**, **Internet On**, *Add Input* đủ năm dataset trên.

## Ô 1 — gói

```python
import subprocess, sys, os, time
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes pycocoevalcap 'trl==0.29.1' 2>&1 | tail -3")
sh(f'{sys.executable} -c "import torch; print(torch.cuda.device_count(), [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])"')
```

Phải in `2 ['Tesla T4', 'Tesla T4']`. Chỉ thấy 1 card thì vẫn chạy được (Ô 5 tự chạy lần lượt), lâu gấp đôi.

## Ô 2 — đường dẫn và kiểm đầu vào

```python
import os, glob, json, shutil, hashlib, tarfile
W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()

# tìm TỪNG tệp theo md5 ở mọi dataset đã gắn (không đòi chung một thư mục)
CAN = {"gen_test_grpo.py": "b18ec1aa3fd037ddffb9411db63c2a3f",
       "grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf",
       "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912",
       "preds_s1_seed101.jsonl": "bc8911912491bb97fd987b3c91a22bda"}
SRC, thieu = {}, []
for f, h in CAN.items():
    tim = glob.glob(f"/kaggle/input/**/{f}", recursive=True)
    dung = [p for p in tim if md5(p) == h]
    print(f"{f:24s} thấy {len(tim)} · đúng md5 {len(dung)}", dung[:1] or [(p, md5(p)[:8]) for p in tim], flush=True)
    if dung: SRC[f] = dung[0]
    else: thieu.append(f)
if thieu:
    print("dataset đang gắn:", sorted(os.listdir("/kaggle/input")), flush=True)
    raise SystemExit(f"DỪNG: thiếu {thieu} — gắn dataset grpo-spice-script (Add Input) rồi chạy lại Ô 2")
for f in ("grpo_spice.py", "build_branch_data.py", "gen_test_grpo.py"):
    shutil.copy(SRC[f], f"{W}/{f}")
S1P = SRC["preds_s1_seed101.jsonl"]
assert sum(1 for _ in open(S1P)) == 6958

BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d)
MERGED = f"{W}/s1_merged"

CK = {}
for t in ("A3_1000", "A2_1000"):
    c = [os.path.dirname(f) for f in glob.glob(f"/kaggle/input/**/{t}/adapter_model.safetensors", recursive=True)]
    assert len(c) == 1, f"DỪNG: cần đúng một {t} trong ctg-ckpts, thấy {c}"
    CK[t] = c[0]
    base = json.load(open(f"{c[0]}/adapter_config.json")).get("base_model_name_or_path", "")
    print(t, c[0], "· md5", md5(f"{c[0]}/adapter_model.safetensors"), "· base", base, flush=True)
assert md5(f"{CK['A3_1000']}/adapter_model.safetensors") != md5(f"{CK['A2_1000']}/adapter_model.safetensors"), \
    "DỪNG: hai nhánh cùng một adapter"

TA = next(os.path.dirname(t) for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True)
          if os.path.exists(os.path.join(os.path.dirname(t), "ocr.jsonl")))
assert md5(f"{TA}/test.jsonl") == "da58299ee551a926a21cbecb5232bf78", "DỪNG: test.jsonl lệch máy nhà"

def tim_anh():
    for d in glob.glob("/kaggle/input/**/images", recursive=True) + glob.glob(f"{W}/nontap/**/images", recursive=True):
        if "thesis-score" not in d and len(glob.glob(f"{d}/ep*_s*.png")) == 2495:
            return d
IMG = tim_anh()
if not IMG:
    tars = glob.glob("/kaggle/input/**/*.tar", recursive=True)
    assert tars, "DỪNG: không thấy ảnh không chạm lẫn tệp .tar"
    tarfile.open(tars[0]).extractall(f"{W}/nontap")
    IMG = tim_anh()
assert IMG, "DỪNG: không có thư mục đúng 2.495 ảnh không chạm"
print("SRC", SRC, "\nBUNDLE", BUNDLE, "\nTA", TA, "\nIMG", IMG, flush=True)
```

Phải thấy hai dòng `A3_1000 …` / `A2_1000 …` với hai md5 khác nhau, không có dòng DỪNG. **Chép lại hai md5**
gửi về để ghi vào report.

## Ô 3 — hoà S1 (GPU 0) + hàm chạy song song có nhịp sống

```python
TEST = True          # chạy thử tương tác 5 câu mỗi nhánh; đổi False trước khi commit
NCARD = __import__("torch").cuda.device_count()

ENV = {**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1"}

def chay_song_song(viec, nhip=120):
    """viec = [(tên, cmd, log, gpu)]; mỗi tiến trình chỉ thấy một card (device_map {'': 0} trong grpo_spice.nap)."""
    t0, Q = time.time(), {}
    for ten, cmd, log, gpu in viec:
        Q[ten] = (subprocess.Popen(cmd, cwd=W, stdout=open(log, "w"), stderr=subprocess.STDOUT,
                                   env={**ENV, "CUDA_VISIBLE_DEVICES": str(gpu)}), log)
        time.sleep(60)               # lệch giờ nạp mô hình để RAM không chạm đỉnh cùng lúc
    while any(q.poll() is None for q, _ in Q.values()):
        time.sleep(30 if TEST else nhip)
        for ten, (q, log) in Q.items():
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            st = "chạy" if q.poll() is None else f"xong mã {q.returncode}"
            print(f"  {(time.time()-t0)/3600:5.2f} h · {ten} [{st}] · {L[-1][:100] if L else 'chưa có dòng nào'}", flush=True)
    for ten, (q, log) in Q.items():
        print(f"--- {ten} · mã thoát {q.returncode} ---\n" + "".join(open(log, errors="ignore").readlines()[-4:]), flush=True)
    print(f"tổng {(time.time()-t0)/3600:.2f} h", flush=True)

r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED],
                   cwd=W, capture_output=True, text=True, env={**ENV, "CUDA_VISIBLE_DEVICES": "0"})
print((r.stdout + r.stderr)[-1500:]); assert r.returncode == 0, "DỪNG: hoà lỗi"
```

## Ô 4 — kiểm hoà trên 20 bước không chạm (S1 hoà, không gắn điểm lưu)

```python
NT_ARGS = ["--recs", f"{TA}/test.jsonl", "--ocr", f"{TA}/ocr.jsonl", "--images", IMG, "--non-tap", "--no-q4"]
out = f"{W}/kiem_hoa_nontap.jsonl"
if os.path.exists(out): os.remove(out)
chay_song_song([("kiem_hoa", ["python", "gen_test_grpo.py", "--bundle", BUNDLE, "--merged", MERGED, "--s1", S1P,
                              "--n", "20", "--out", out] + NT_ARGS, f"{W}/kiem_hoa_nontap.log", 0)])
print([l.strip() for l in open(f"{W}/kiem_hoa_nontap.log") if "[dữ liệu]" in l or "[kiểm hoà]" in l])
```

Phải có `[dữ liệu] … 20 bước · thiếu OCR 0 · thiếu ảnh 0` và `[kiểm hoà] x/20`. Lượt 2/10 ra **20/20**. x thấp
hơn thì vẫn chạy tiếp nhưng gửi số về để khai (không chặn: cặp A3 − A2 dùng chung đường sinh).

## Ô 5 — sinh 2.495 câu cho A3_1000 (GPU 0) và A2_1000 (GPU 1)

```python
duoi = "_thu" if TEST else ""
viec = []
for i, (t, ck) in enumerate(CK.items()):
    pred = f"{W}/pred_{t}_test_nontap{duoi}.jsonl"
    viec.append((t, ["python", "gen_test_grpo.py", "--bundle", BUNDLE, "--merged", MERGED, "--ckpt", ck,
                     "--out", pred] + (["--n", "5"] if TEST else []) + NT_ARGS,
                 f"{W}/gen_{t}_test_nontap{duoi}.log", i % NCARD))
if NCARD >= 2:
    chay_song_song(viec)
else:
    for v in viec:
        chay_song_song([v])

for t in CK:
    p = f"{W}/pred_{t}_test_nontap{duoi}.jsonl"
    n = sum(1 for _ in open(p)) if os.path.exists(p) else 0
    lg = open(f"{W}/gen_{t}_test_nontap{duoi}.log", errors="ignore").read()
    print(f"{t}: {n}/{5 if TEST else 2495} câu · gắn điểm lưu: {'[điểm lưu] /kaggle' in lg} · "
          f"{[l for l in lg.splitlines() if l.startswith('[xong]')]}", flush=True)
    assert n == (5 if TEST else 2495), f"DỪNG: {t} thiếu câu — chạy lại ô này (nối tiếp được), KHÔNG xoá tệp"
```

Mỗi log phải có `[điểm lưu] /kaggle/input/…/A3_1000` (hoặc `A2_1000`), không phải `KHÔNG gắn`, và dòng
`[xong] 2495 câu · rỗng …`. Hai tiến trình chạy song song nên nhịp sống in xen kẽ hai tên — bình thường.
Mất phiên giữa chừng: chạy lại Ô 2 → Ô 3 → Ô 5, `gen_test_grpo.py` tự nối tiếp từ tệp đã có.

## Ô 6 — đóng zip kết quả

```python
shutil.rmtree(MERGED, ignore_errors=True)
shutil.rmtree(f"{W}/nontap", ignore_errors=True)
Z = f"{W}/ctg_test_nontap"
os.makedirs(Z, exist_ok=True)
for p in glob.glob(f"{W}/pred_*_test_nontap*.jsonl") + glob.glob(f"{W}/*.log") + [f"{W}/kiem_hoa_nontap.jsonl"]:
    if os.path.exists(p): shutil.copy(p, Z)
shutil.make_archive(Z, "zip", Z)
print(sorted(os.listdir(Z)), os.path.getsize(Z + ".zip") // 1024, "KB", flush=True)
```

## Chạy

1. **Chạy thử tương tác** (`TEST = True`): *Run All*, ~15 phút (hoà ~5 phút · kiểm hoà ~2 phút · 5 câu mỗi
   nhánh). Gửi về output Ô 1, Ô 2, Ô 4, Ô 5.
2. Ổn thì sửa Ô 3 thành `TEST = False` → **Stop session** → **Save Version → Save & Run All**. Khoảng
   **2,2–2,5 h** với hai card (2.495 × 2,94 s ≈ 2,0 h mỗi nhánh, chạy cùng lúc). Có thể gập máy.
3. Tải `ctg_test_nontap.zip` từ Output, đặt vào **`runs/ctg/test_nontap/`**, giải nén tại chỗ (`unzip -o`).

## Đọc ở máy nhà (0 GPU, ~1 phút)

```
~/.venvs/thesis/bin/python harness/ctg_nontap_doc.py
```

In bảng S1 · ck500 · A2 · A3 theo từng loại thao tác, năm cặp Δ có KTC cụm app (A3 − A2 · A3 − S1 · A2 − S1 ·
A3 − ck500 · A2 − ck500), các dạng sai loại nhiều nhất, số câu "Search for" ở bước gõ, rồi ba dòng `[luật]`;
ghi `runs/ctg/test_nontap/ctg_nontap_doc.json`. Đã chạy khô 5/10 (`--kho`: câu S1 làm giả A3, câu ck500 làm
giả A2): A2 − S1 ra đúng bảng ck500 đã công bố (toàn bộ −1,68 [−2,76; −0,62] · scroll −6,23), A3 − S1 = 0.
