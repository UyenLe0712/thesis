# 258 — ACTION: chấm test một lần cho checkpoint 500 (1/10/2026)

> Extracted từ 5 ảnh trong file ZIP. Mình đã làm sạch OCR và giữ lại cấu trúc Markdown/code theo ảnh.  
> Một vài ký tự/code rất nhỏ trong ảnh có thể cần đối chiếu lại ảnh gốc trước khi chạy.

Gửi nguyên file này cho chat có GPU. File tự chứa. Không train. Không sửa trọng số. Không làm đầu khe.

Checkpoint 500 đã chấm val (file 254 mục 7, kiểm lại ở file 257). SPICE val +0,15, không đạt ngưỡng +2,0. exec val +2,81, khoảng tin cậy chạm 0. Lượt này chỉ hỏi câu đó còn đúng trên tập kiểm hay không.

Mốc S1/101 đã công bố, cùng 4.463 bước click của tập kiểm:

| Metric | S1/101 |
|---|---:|
| exec | 59,11 |
| Hộp phản từ (0.3) | 65,49 |
| A11y đầy đủ | 74,37 |
| SPICE | 44,37 |
| Đúng loại thao tác | 94,3 |

Số test của checkpoint 500 chấm một lần. Không xem số rồi sinh lại, đổi checkpoint, hay đổi nhiệt độ.

## 0. Luật đọc, khoá trước khi có số

So checkpoint 500 với S1/101 trên cùng 4.463 bước click. Ghép cặp theo `(episode_id, step_id)`.

| Kết quả | Việc |
|---|---|
| Δexec > 0 và ΔSPICE > 0, cận dưới KTC của Δexec > 0 | Giữ checkpoint 500. Được báo là hơn S1 trên cả hai metric của lượt này |
| Δexec > 0 nhưng ΔSPICE < 0 | Báo là đánh đổi: bấm hơn, câu xa câu người hơn. Không gọi là GRPO thưởng SPICE đã đạt |
| Δexec ≤ 0, hoặc KTC của Δexec chứa 0 | Không hơn S1 trên tập kiểm. Dừng. Giữ bảng luận văn hiện có |
| Bước không chạm, nếu có chấm: khớp loại thao tác của nhóm scroll thấp hơn S1 quá 3 điểm | Không dùng checkpoint này làm mô hình cuối, dù bước click có tăng |

`action_ok` trên 4.463 bước click phải in kèm. Val đã thấy 5/12 bước được cứu là đổi `"swipe"` thành `"click"`. Nếu gần hết mức tăng exec nằm ở `action_ok`, ghi đúng như vậy.

Không nối luật sau khi thấy số.

## 1. Vì sao không dùng `infer_branch.py`

Adapter checkpoint 500 học trên S1 đã hoà vào Qwen, rồi gắn LoRA mới. `infer_branch.py` gắn LoRA lên Qwen gốc. Gắn checkpoint này theo đường đó ra một mô hình khác mô hình đã chấm val.

Đường đúng, cùng đường val: hoà `adapter_s1_seed101` thành `s1_merged`, nạp checkpoint 500 lên bản hoà, fp16 (`--no-q4`), greedy, tối đa 96 token. Câu nhắc là `prompt_body + SYS` của `build_branch_data.py`, ảnh đứng trước chữ.

## 2. Đầu vào Kaggle

GPU T4 x1, Internet ON. Một card đủ. Sinh 4.463 câu khoảng 4 giờ, chấm UGround khoảng 5 giờ. Cộng nạp model, khoảng 9–10 giờ, dưới trần 12 giờ của một commit.

### Add Input

| Dataset | Phải có |
|---|---|
| `thesis-score` | `test.jsonl` 6.958 dòng, `ocr.jsonl`, 4.463 ảnh bước chạm |
| `fgrb-p1-bundle` | `adapter_s1_seed101/` |
| `grpo-spice-script` | `grpo_spice.py`, `build_branch_data.py`. md5 `grpo_spice.py` phải là `07ea87b6d156d1faa391a4274dffd7cf` |
| `grpo-spice-ck500` | `adapter_config.json` + `adapter_model.safetensors` của checkpoint 500. `base_model_name_or_path` chứa `s1_merged` |
| `thesis-preds` hoặc tên tải từ clone | `runs/preds_s1_seed101.jsonl`, để kiểm hoà |

## 3. Ô lệnh

Chạy tương tác cho tới hết ô 4, ô 5 và ô 6 mới Save & Run All.

### Ô 1 — gói

```python
import subprocess, sys, os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "-q", "torchao"])
subprocess.run([
    sys.executable, "-m", "pip", "install", "-q", "-U",
    "transformers", "peft", "accelerate", "bitsandbytes"
], check=True)

import torch
print("GPU", torch.cuda.get_device_name(0), torch.cuda.device_count())
assert torch.cuda.device_count() >= 1
```

### Ô 2 — đường dẫn

```python
import os, glob, json, shutil, hashlib

W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()

def one(pat, mo_ta):
    xs = glob.glob(pat, recursive=True)
    assert len(xs) == 1, (mo_ta, xs)
    return xs[0]

src = glob.glob("/kaggle/input/**/thesis/harness/score_run.py", recursive=True)
assert src, "thiếu gói mã"

WS = os.path.dirname(os.path.dirname(os.path.dirname(src[0])))

# WS trỏ tới thư mục chứa harness/. Nếu gói giải nén sâu hơn thì sửa một dòng này rồi đừng báo lại.
if not os.path.exists(f"{WS}/harness/score_run.py"):
    WS = os.path.dirname(os.path.dirname(src[0]))

assert os.path.exists(f"{WS}/harness/score_run.py")

# Gói mã và dataset chấm đều có thể chứa test.jsonl. Chỉ nhận bản đứng cạnh đủ ảnh.
ung = []
for vtest in glob.glob("/kaggle/input/**/test.jsonl", recursive=True):
    base = os.path.dirname(vtest)
    nrec = sum(1 for _ in open(vtest, encoding="utf-8"))
    nimg = len(glob.glob(f"{base}/images/*.png"))
    if nrec == 6958 and nimg >= 4463 and os.path.exists(f"{base}/ocr.jsonl"):
        ung.append((vtest, base, nimg))

assert len(ung) == 1, ung
vtest, BASE, nimg = ung[0]

BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d)
SRC = one("/kaggle/input/**/build_branch_data.py", "build_branch_data.py")

for f in ("grpo_spice.py", "build_branch_data.py"):
    shutil.copy(os.path.join(os.path.dirname(SRC), f), f"{W}/{f}")

assert md5(f"{W}/grpo_spice.py") == "07ea87b6d156d1faa391a4274dffd7cf"

def la_grpo(d):
    c = os.path.join(d, "adapter_config.json")
    return os.path.exists(c) and "s1_merged" in json.load(open(c, encoding="utf-8")).get("base_model_name_or_path", "")

CK = [
    os.path.dirname(f)
    for f in glob.glob("/kaggle/input/**/adapter_model.safetensors", recursive=True)
    if la_grpo(os.path.dirname(f))
]
CK = [d for d in CK if d.rstrip("/").endswith("checkpoint-500")]
assert len(CK) == 1, CK
CK500 = CK[0]

S1P = one("/kaggle/input/**/preds_s1_seed101.jsonl", "preds S1")
MERGED = f"{W}/s1_merged"

print("BASE", BASE)
print("CK500", CK500)
print("ảnh chạm", len(glob.glob(f"{BASE}/images/*.png")))
```

### Ô 3 — script sinh câu

Dán thành `/kaggle/working/gen_test.py`.

```python
# -*- coding: utf-8 -*-
"""
Sinh greedy trên tập kiểm. Không gắn LoRA lên Qwen gốc.

python gen_test.py --bundle B --merged M --recs test.jsonl --ocr ocr.jsonl --images IMG --s1 preds_s1.jsonl --n 20 --out kiem.jsonl
python gen_test.py --bundle B --merged M --ckpt CK --recs test.jsonl --ocr ocr.jsonl --images IMG --tap-only --out pred_test.jsonl
"""

import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_branch_data import prompt_body, SYS

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--merged", required=True)
    ap.add_argument("--ckpt", default=None)
    ap.add_argument("--recs", required=True)
    ap.add_argument("--ocr", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--s1", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--tap-only", action="store_true")
    ap.add_argument("--no-q4", dest="q4", action="store_false")
    a = ap.parse_args()

    a.adapter = os.path.join(a.bundle, "adapter_s1_seed101")

    import grpo_spice
    proc, model, _ = grpo_spice.map(a)

    if a.ckpt:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, a.ckpt)
        print("[điểm lưu]", a.ckpt, flush=True)

    model.eval()

    rows = [json.loads(l) for l in open(a.recs, encoding="utf-8")]
    if a.tap_only:
        rows = [r for r in rows if r["action"].get("action_type") in ("click", "long_press") and "x" in r["action"]]
        assert len(rows) == 4463, len(rows)

    if a.n:
        rows = rows[:a.n]

    ocr = {o["image"]: o for o in map(json.loads, open(a.ocr, encoding="utf-8"))}
    done = {}
    if os.path.exists(a.out):
        done = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(a.out, encoding="utf-8"))}

    fo = open(a.out, "a", encoding="utf-8")

    import torch
    from PIL import Image

    for i, r in enumerate(rows):
        k = (r["episode_id"], r["step_id"])
        if k in done:
            continue

        body = prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
        msg = [
            {"role": "system", "content": SYS},
            {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body}]},
        ]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.images, os.path.basename(r["image"]))).convert("RGB")
        inp = proc(text=[text], images=[img], return_tensors="pt").to(model.device)
        L = inp["input_ids"].shape[1]

        with torch.no_grad():
            g = model.generate(
                **inp,
                max_new_tokens=96,
                do_sample=False,
                use_cache=True,
                temperature=None,
                top_p=None,
                top_k=None,
            )

        s = proc.decode(g[0][L:], skip_special_tokens=True).strip()
        fo.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "pred": s}, ensure_ascii=False) + "\n")
        fo.flush()

        if (i + 1) % 20 == 0:
            print(f" {i+1}/{len(rows)} - {s[:60]!r}", flush=True)

    fo.close()

    if a.s1:
        S = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(a.s1, encoding="utf-8"))}
        P = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(a.out, encoding="utf-8"))}
        same = sum(P[k] == S.get(k) for k in P)
        print(f"[kiểm hoà] {same}/{len(P)} trùng preds_s1_seed101", flush=True)

if __name__ == "__main__":
    main()
```

### Ô 4 — hoà và kiểm 20 câu

```python
import subprocess

r = subprocess.run([
    "python", "grpo_spice.py", "--merge", "--bundle", BUNDLE,
    "--merged", MERGED, "--no-q4"
], cwd=W)
assert r.returncode == 0

# 20 câu đầu của test, KHÔNG gắn checkpoint. Phải gần câu S1 đã công bố.
subprocess.run([
    "python", "gen_test.py", "--bundle", BUNDLE, "--merged", MERGED, "--no-q4",
    "--recs", vtest, "--ocr", f"{BASE}/ocr.jsonl", "--images", f"{BASE}/images",
    "--s1", S1P, "--n", "20", "--out", f"{W}/kiem_hoa_test.jsonl"
], cwd=W, check=True)
```

Chỉ đi tiếp khi dòng `[kiểm hoà]` có `x >= 16` trên 20. Dưới 16: dừng, gửi log. Đừng gắn checkpoint.

### Ô 5 — sinh 4.463 câu click

Nối tiếp được. Mất phiên thì chạy lại ô này, không xoá `pred_ck500_test.jsonl`.

```python
import subprocess, time, os

log = open(f"{W}/gen_test.log", "w")
cmd = [
    "python", "gen_test.py", "--bundle", BUNDLE, "--merged", MERGED, "--no-q4",
    "--ckpt", CK500, "--recs", vtest, "--ocr", f"{BASE}/ocr.jsonl",
    "--images", f"{BASE}/images", "--tap-only", "--out", f"{W}/pred_ck500_test.jsonl"
]

p = subprocess.Popen(cmd, cwd=W, stdout=log, stderr=subprocess.STDOUT)
t0 = time.time()

while p.poll() is None:
    time.sleep(120)
    n = sum(1 for _ in open(f"{W}/pred_ck500_test.jsonl", encoding="utf-8")) if os.path.exists(f"{W}/pred_ck500_test.jsonl") else 0
    print(f"{(time.time()-t0)/3600:.2f} h + {n}/4463", flush=True)

    if time.time() - t0 > 11 * 3600:
        p.terminate()
        print("cắt vì gần trần 12 h")
        break

print("mã thoát", p.returncode)
assert sum(1 for _ in open(f"{W}/pred_ck500_test.jsonl", encoding="utf-8")) == 4463
```

### Ô 6 — chấm exec

`score_run.py` chỉ chấm bước click. Cần thấy 4.463 và grounder `osunlp/UGround-V1-2B`.

```python
import subprocess

r = subprocess.run([
    "python", "harness/score_run.py", "--mode", "score", "--grounder", "uground",
    "--preds", f"{W}/pred_ck500_test.jsonl", "--data-root", BASE,
    "--recs-file", "test.jsonl", "--out", f"{W}/score_ck500_test.json"
], cwd=WS)

print("mã thoát", r.returncode)
```

Nếu `BASE` không phải thư mục `test_ac` mà `score_run` vẫn tìm ảnh sai, dừng và gửi dòng `[dữ liệu]` trong log. Đừng sửa luật chấm.

### Ô 7 — bước không chạm, chỉ khi đủ ảnh

Đếm ảnh. Đủ 6.958 thì sinh nốt các bước không click, ghi `pred_ck500_nontap.jsonl`, cùng script nhưng bỏ `--tap-only` và trỏ `--images` tới thư mục đã gộp. Thiếu ảnh thì **CHƯA CÓ ẢNH SCROLL** và dừng phần này. Không bịa phép kiểm scroll.

## 4. Máy nhà, sau khi tải về

Đặt vào:

`/Users/P836901/Documents/Self-learning/thesis/_exports/grpo_spice_test/`

- `pred_ck500_test.jsonl`
- `score_ck500_test_raw.jsonl`
- `score_ck500_test.json`
- `gen_test.log`, `kiem_hoa_test.jsonl`
- log chấm, 30 dòng cuối
- nếu có: `pred_ck500_nontap.jsonl`

Rồi chạy phụ lục. Kỳ vọng dòng S1 in lại exec `59.11` và SPICE `44.37`. Lệch thì đường đọc sai, không đọc số checkpoint 500.

## 5. Gửi lại

1. Dòng `[kiểm hoà] x/20`.
2. JSON `score_ck500_test.json`.
3. Bảng phụ lục in ra.
4. Có hay không dòng **CHƯA CÓ ẢNH SCROLL**.

Chat GPU không diễn giải theo mục 0. Không train tiếp.

## 6. Việc người dùng quyết

1. Có bỏ khoảng 10 giờ T4 trong hạn mức tuần này hay không.
2. Ảnh 2.495 bước không chạm có được đưa lên Kaggle trong lượt này hay để sau. Không có ảnh thì chưa kết luận được nhóm scroll.
3. Sau khi có số: đọc mục 0. Không đổi checkpoint, không chấm lại.
4. Không commit, không push, không ghi vào `thesis-master/`.

## Phụ lục — đọc trên máy nhà

Gần clone `thesis-master` hiện tại và `.venv_90`. Java là Corretto 11.

```python
import json, os, random, sys
from math import comb
from pathlib import Path

JH = "/Library/Java/JavaVirtualMachines/amazon-corretto-11.jdk/Contents/Home"
os.environ["JAVA_HOME"] = JH
os.environ["PATH"] = JH + "/bin:" + os.environ["PATH"]

T = Path("/Users/P836901/Documents/Self-learning/thesis/thesis-master")
E = Path("/Users/P836901/Documents/Self-learning/thesis/_exports/grpo_spice_test")

sys.path.insert(0, str(T / "harness"))

import luat_d3 as L
import luat_a11y_day_du as A

def load(p):
    rows = [json.loads(l) for l in open(p, encoding="utf-8")]
    d = {(o["episode_id"], o["step_id"]): o for o in rows}
    assert len(d) == len(rows) == 4463, len(rows)
    return d

S1 = load(T / "runs/score_s1_seed101_raw.jsonl")
R = load(E / "score_ck500_test_raw.jsonl")
assert set(S1) == set(R)

keys = list(S1)
ex = lambda src, k: int(src[k]["executable"])

# Phần dưới của phụ lục bị khuất/cắt trong ảnh gốc.
```
