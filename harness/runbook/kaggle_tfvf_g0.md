# G0 của TFVF — S1/101 trên ảnh làm nét vùng đích — Kaggle T4, 0 đồng — viết 28/9/2026

Theo đúng `report/237_ACTION_TEST_TFVF_TRUOC_KHI_TRAIN_extracted.md`. Câu hỏi duy nhất: nếu vùng đích
được làm nét trực tiếp trên ảnh thì S1 có sinh câu tốt hơn không. **Không train, không A100, không
đụng test, không sửa luận văn.** GO không đạt thì dừng TFVF.

Ước lượng: 249 bước click × 3 chế độ = 747 lượt greedy, **~1–2 h T4** + ~5 phút tải Qwen2.5-VL-3B.
Script in thời gian thật mỗi 20 bước.

## Đã kiểm trên WSL trước khi lên Kaggle (0 GPU)
- 400 bước seed 20260927 trùng khoá và câu chuẩn với `runs/c1/c1_mau.jsonl` **400/400**; có
  **249 click**, toạ độ pixel, cỡ ảnh khớp `w,h` ở cả 249 bước.
- Dấu vân tay in ra phải thấy: `hash400=a044f6d060d264b0` · `hash_click=8a24abe4f7f041e0`.
- Renderer vẽ thử 5 bước (`--chi-ve`): ở ảnh G, nút đích giữ nét; ở F và C, nút đích mờ, nền vẫn
  đọc được.
- `tfvf_g0_doc.py` chạy trên dữ liệu giả (G/F/C lấy từ mẫu của C1): hàng O của bảng 400 bước tái lập
  đúng số greedy C1 (BLEU-4 59,48 · CIDEr-D 543,8 · SPICE 57,30); assert bắt được tệp thiếu bước.

## A. Dữ liệu (máy nhà → Kaggle)
1. Dataset `fgrb-p1-bundle` **đã có sẵn**, không upload lại.
2. Tải `_bundles/tfvf_g0_script.zip` (9 KB: `tfvf_g0.py` + `build_branch_data.py`) → **New Dataset**,
   tên `tfvf-g0-script`.
3. Notebook mới → Add Data: `fgrb-p1-bundle` + `tfvf-g0-script`. Settings: **GPU T4 ×1 · Internet ON**.

## B. Chạy dạng COMMIT (Save Version → Save & Run All)
Notebook chỉ có **ba ô dưới đây**, không thêm ô nào khác.

### Ô 1 — cài gói
```python
!pip install -q -U transformers peft accelerate torchao 2>&1 | tail -2
import subprocess
print(subprocess.run(["python", "-c", "import transformers, peft, torchao, torch; print(transformers.__version__, "
      "peft.__version__, torchao.__version__, torch.cuda.get_device_name(0))"],
      capture_output=True, text=True).stdout)
```

### Ô 2 — dò đường dẫn, chép script, kiểm dấu vân tay
```python
import os, shutil, glob
BUNDLE = None
for root, dirs, files in os.walk("/kaggle/input"):
    if "adapter_s1_seed101" in dirs and "images" in dirs:
        BUNDLE = root; break
assert BUNDLE, "DỪNG: chưa Add Data fgrb-p1-bundle"
src = [q for q in glob.glob("/kaggle/input/**/tfvf_g0.py", recursive=True)
       if "SAN, BIEN = 0.35, 0.65" in open(q, encoding="utf-8").read()]
assert len(src) == 1, f"DỪNG: cần đúng một bản tfvf_g0.py có dấu vân tay, thấy {src}"
d = os.path.dirname(src[0])
for f in ["tfvf_g0.py", "build_branch_data.py"]:
    shutil.copy(os.path.join(d, f), "/kaggle/working/" + f)
print("BUNDLE =", BUNDLE, "· script từ", d)
print("ảnh:", len(os.listdir(BUNDLE + "/images")), "(kỳ vọng 5567)")
```

### Ô 3 — vẽ mẫu, thử 5 bước, rồi chạy đủ
```python
import subprocess, time, os, json
W = "/kaggle/working"
env = dict(os.environ, TQDM_DISABLE="1", HF_HUB_DISABLE_PROGRESS_BARS="1")

def chay(args, log_name, out=None):
    log = open(f"{W}/{log_name}", "a")
    p = subprocess.Popen(["python", "tfvf_g0.py", "--bundle", BUNDLE] + args, cwd=W, env=env,
                         stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    t0 = time.time()
    while p.poll() is None:
        time.sleep(120)
        n = sum(1 for _ in open(out)) if out and os.path.exists(out) else 0
        print(f"[{(time.time()-t0)/60:5.1f} phút] {log_name}: {n} bước click", flush=True)
        if time.time() - t0 > 8 * 3600:
            p.terminate(); print("⛔ quá 8 h — dừng, giữ phần đã ghi", flush=True)
    log.close()
    print(open(f"{W}/{log_name}").read()[-1500:], flush=True)
    return p.returncode

# ⓪ vẽ ảnh G/F/C của 5 bước đầu (không nạp model) để xem bằng mắt ở tab Output
assert chay(["--chi-ve", f"{W}/tfvf_anh_mau", "--n", "5"], "tfvf_ve.log") == 0, "DỪNG: vẽ lỗi"

# ① thử 5 bước — hỏng là dừng cả commit
assert chay(["--out", f"{W}/tfvf_g0_thu.jsonl", "--n", "5"], "tfvf_thu.log",
            f"{W}/tfvf_g0_thu.jsonl") == 0, "DỪNG: lượt thử lỗi, xem tfvf_thu.log"
thu = [json.loads(l) for l in open(f"{W}/tfvf_g0_thu.jsonl")]
assert len(thu) == 5 and all(x["gold_focus"] and x["false_focus"] and x["center_focus"] for x in thu), \
    "DỪNG: thiếu dòng hoặc câu rỗng"
for x in thu:
    print("VÀNG:", x["gold"], "| G:", x["gold_focus"], "| F:", x["false_focus"], "| C:", x["center_focus"])

# ② chạy đủ 249 bước click
OUT = f"{W}/tfvf_g0.jsonl"
rc = chay(["--out", OUT, "--n", "400"], "tfvf_g0.log", OUT)
n = sum(1 for _ in open(OUT))
print("mã thoát", rc, "·", n, "/ 249 bước click", "✅" if n == 249 else "⚠️ CHƯA ĐỦ — commit lại, script tự nối tiếp")
```

### Trước khi bấm Save Version, kiểm bốn điều
1. Input có **`fgrb-p1-bundle`** và **`tfvf-g0-script`**.
2. Accelerator **GPU T4**, Internet **ON**.
3. Notebook chỉ có ba ô trên.
4. Save & Run All (Commit).

Xong thì tab **Output** có `tfvf_g0.jsonl`, `tfvf_g0.log`, `tfvf_g0_thu.jsonl`, `tfvf_thu.log`,
`tfvf_ve.log`, `tfvf_anh_mau/`. Tải `tfvf_g0.jsonl` + `tfvf_g0.log` về **`runs/tfvf_g0/`**.

Trong `tfvf_g0.log` kiểm ba dòng: `[renderer] M = 0.35 + 0.65…radius=8` · `[dữ liệu] … hash400=a044f6d060d264b0
· click trong 400 = 249 … hash_click=8a24abe4f7f041e0` · `[cấu hình] … greedy do_sample=False · max_new=96`.

Chưa đủ 249 (bị cắt): commit lại với `tfvf_g0.jsonl` cũ gắn làm input rồi chép vào `/kaggle/working`
trước ô 3 — script tự bỏ bước đã có.

## C. Đọc trên máy nhà (CPU + Java 8, ~3 phút)
```
~/.venvs/thesis/bin/python harness/tfvf_g0_doc.py runs/tfvf_g0/tfvf_g0.jsonl runs/c1/c1_mau.jsonl \
    --json runs/tfvf_g0/g0_doc.json
```
Luật GO (report/237 §5, ghi trước khi có số, đọc trên 249 click, thước quyết định BLEU-4 · CIDEr-D ·
SPICE): (1) G≠O ≥ 10% · (2) G>F ở ≥2/3 thước và ΔCIDEr-D ≥ 3 · (3) G>C ở ≥2/3 · (4) G≥O cả ba và
G>O ở ≥2/3. Không nới sau khi thấy số. ⛔ Số val, cấm trích ra báo hay luận văn.
Kết quả ghi vào `report/238_KET_QUA_G0_TFVF.md`, phụ lục chép nguyên mã hai script.
