# 314 — ACTION: RAFT (T4) và GA-DPO (Colab L4/A100) trên cùng một bộ mẫu, lấy nhánh ra số cao hơn (12/10/2026)

File tự chứa, đọc từ đầu tới cuối là chạy được. File này thay phần action của `313_DE_XUAT_RAFT_VA_ACTION_12_10.md`. Phần căn cứ và tranh luận chi tiết nằm ở 313 (mục CHỐT, 0b, 1, 2) và 295 (§2.5, §4). Mã nguồn nguyên văn ở Phụ lục A–G; trên đĩa ở `/Users/P836901/Documents/Self-learning/thesis/_scripts/313/`. Chưa chạy GPU nào, chưa commit gì.

## 0. Quyết định

Người dùng: *"Cái nào khả năng ra số cao thì làm."*

RAFT và GA-DPO có khả năng gần bằng nhau (ước có điều kiện ~45% và ~50%). Cả hai dùng chung dữ liệu và chung luật chọn. Vậy cách có xác suất ra số cao nhất là lấy mẫu một lần, train cả hai nhánh, chấm cả hai trên tập kiểm, lấy nhánh tốt hơn. Gộp lại ước ~40% có ít nhất một nhánh hơn ck500 ở ≥ 4/7 thước chờ, so với ~30% nếu chỉ chạy một.

| nhánh | học gì | máy | mã |
|---|---|---|---|
| RAFT | SFT tiếp adapter ck500 trên câu đích = mẫu trội greedy (không có thì giữ greedy) | Kaggle T4 | `raft_chon.py` + `ra_train.py` (đã chạy ở 304/309) |
| GA-DPO | DPO + NLL, cặp (mẫu trội greedy, greedy) + cặp giữ (greedy, mẫu thua mọi thước), LoRA mới trên S1 + ck500 hoà ở fp32 | Colab L4 (rẻ hơn) hoặc A100; cần bf16 | `ga_dpo.py` của file 295, chưa chạy lần nào |

Luật chọn chung, theo 295 §4: mẫu y thay câu greedy g khi SPICE(y) ≥ SPICE(g) + 0,05, CIDEr-D(y) ≥ CIDEr-D(g), chrF(y) ≥ chrF(g), và |số từ(y) − số từ(câu chuẩn)| ≤ 3.

Dữ liệu: ck500 sinh greedy + 8 mẫu ở T = 0,7 trên 2.000 câu nhắc train ck500 chưa thấy trong GRPO (hàng [1000, 3000) theo thứ tự `grpo_spice.dung_hang`).

**Cổng chung:** < 15% câu nhắc có mẫu trội greedy thì dừng cả hai nhánh.

**Chọn nhánh để báo:** chấm cả hai trên tập kiểm. Lấy nhánh hơn ck500 ở nhiều thước chấm hơn; hoà thì lấy SPICE cao hơn. Theo chỉ đạo của người dùng (bỏ các ràng buộc "chọn sau khi thấy số"). Khi viết bài, nên khai rằng hai nhánh đều đã chấm trên tập kiểm và báo cả hai. Hai nhánh cạnh nhau cũng là một bảng tách thành phần có ích ("bắt chước câu tốt" so với "học ưu tiên").

## 1. Tổng quan

| notebook | máy | việc | thời gian ước |
|---|---|---|---|
| R | Kaggle T4 ×2 | lấy mẫu → chọn đích RAFT + cổng → dựng cặp DPO → SFT RAFT | ~8 h |
| D | Colab L4 (hoặc A100) | tải dữ liệu → hoà S1 → train GA-DPO → ghép adapter với ck500 → đẩy lên Kaggle | ~3–4 h trên L4 (~2 h A100) [ước] |
| E | Kaggle T4 ×2 | sinh val + tập kiểm cho hai nhánh, chấm 7 thước + exec | ~7 h |
| máy nhà | CPU | exec, D.3, AitW, khoảng tin cậy | vài phút |

R xong mới chạy D. D và phần RAFT của E chạy song song được.

## 2. Chuẩn bị

### 2.1 Dataset mới `raft-313` (Kaggle)

| tệp | md5 |
|---|---|
| `raft_mau.py` | `0e8024f68deeea03f1aaa61f5024c12f` |
| `raft_chon.py` | `9067f4213c6a9137a15039305ca0ee20` |
| `mau_sang_ga.py` | `febf4423d5a379fa56a5003d67384ee1` |
| `ga_dpo.py` | `69a3dd3e379b0995e8068a5e179aaeba` *(nguyên bản file 295)* |
| `tron_adapter.py` | `b354985a197cdb7e7c13fbc567eae1d0` *(nguyên bản file 295)* |

Tất cả trong `thesis/_scripts/313/`. `ktc_chu.py` (`838a7586…`) và `doc_exec_cw.py` (`04e0901a…`) chạy ở máy nhà.

### 2.2 Input dùng lại

- `trangphngngc/ra-sft-script` (`SRC`): `grpo_spice.py` md5 `07ea87b6…`, `build_branch_data.py`, `ra_train.py`, `ra_gen.py`, `ra_score.py`, `pred_ck500_vallon.jsonl`, `pred_ck500_test.jsonl`.
- `trangphngngc/fgrb-p1-bundle` (`BUNDLE`).
- `trangphngngc/grpo-spice-ck500` (`CK500`).
- `uyenle0712/thesis-score`: chỉ notebook E.

### 2.3 Hai ô chung cho notebook Kaggle (R và E) — T4 ×2, Internet bật

```python
# ô 0-1: gói (trl 0.29.1 · transformers 5.18.0 · peft 0.21.1, gỡ torchao) + Java cho SPICE + assert 2 GPU
import subprocess, sys, os, time, glob, json, shutil, re, random
T0 = time.time()

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True)
    return r.returncode

sh("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless")
sh("update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java; java -version")
sh(f"{sys.executable} -m pip install -q 'transformers==5.18.0' 'peft==0.21.1' 'trl==0.29.1' accelerate bitsandbytes pycocoevalcap sacrebleu")
sh(f"{sys.executable} -m pip uninstall -y torchao")

import torch
assert torch.cuda.device_count() == 2, "⛔ cần T4 ×2"
```

```python
# ô 0-2: đường dẫn, chép mã, hoà S1, hàm chạy nền
W = "/kaggle/working"
RA = f"{W}/ra"
M = f"{W}/s1_merged"

def tim(duoi):
    for sau in range(1, 6):
        g = glob.glob("/kaggle/input/" + "*/" * sau + duoi)
        if g:
            return g[0]
    raise FileNotFoundError(duoi)

SRC = os.path.dirname(tim("ra_gen.py"))
D313 = os.path.dirname(tim("raft_mau.py"))
BUNDLE = next(r for r, d, f in os.walk("/kaggle/input")
              if "adapter_s1_seed101" in d and "images" in d)
CK500 = next(r for r, d, f in os.walk("/kaggle/input")
             if "grpo-spice-ck500" in r and "adapter_config.json" in f)

shutil.copytree(SRC, RA, dirs_exist_ok=True)
for f in os.listdir(D313):
    shutil.copy(f"{D313}/{f}", RA)

print("SRC", SRC, "\nBUNDLE", BUNDLE, "\nCK500", CK500)

r = subprocess.run(
    ["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", M],
    cwd=RA, capture_output=True, text=True
)
print((r.stdout + r.stderr)[-1500:])
assert r.returncode == 0

ENV = {
    **os.environ,
    "TQDM_DISABLE": "1",
    "HF_HUB_DISABLE_PROGRESS_BARS": "1",
    "PYTHONUNBUFFERED": "1",
    "PYTORCH_ALLOC_CONF": "expandable_segments:True",
    "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True",
}

def chay(script, args, log, gpu):
    return subprocess.Popen(
        ["python", f"{RA}/{script}", *args],
        stdout=open(log, "w"),
        stderr=subprocess.STDOUT,
        env={**ENV, "CUDA_VISIBLE_DEVICES": str(gpu)},
        cwd=RA,
        start_new_session=True,
    )

def doi(ps, logs):
    while any(p.poll() is None for p in ps):
        time.sleep(120)
        print(
            time.strftime("%H:%M"),
            f"{(time.time()-T0)/3600:.2f} h",
            [open(l).read().splitlines()[-1:] for l in logs],
            flush=True,
        )
    assert all(p.returncode == 0 for p in ps), [
        open(l).read()[-2000:] for l in logs
    ]

def py(*a):
    r = subprocess.run(["python", *a], capture_output=True, text=True, cwd=RA)
    print(r.stdout[-5000:], r.stderr[-2000:])
    return r.returncode
```

## 3. Notebook R — Kaggle T4 ×2 (~8 h, một commit)

Thêm input: `raft-313`, `ra-sft-script`, `fgrb-p1-bundle`, `grpo-spice-ck500`. Chạy ô 0-1, ô 0-2, rồi:

```python
# ô R-1: ck500 sinh greedy + 8 mẫu (T = 0,7) trên 2.000 câu nhắc mới, hai GPU (~3,6 h)
logs = [f"{W}/mau_{i}.log" for i in (0, 1)]
ps = [
    chay(
        "raft_mau.py",
        ["--bundle", BUNDLE, "--merged", M, "--ckpt", CK500,
         "--out", f"{W}/raft_mau_{i}.jsonl",
         "--shard", f"{i}/2"],
        logs[i],
        i,
    )
    for i in (0, 1)
]
doi(ps, logs)
print(open(logs[0]).read()[:1500])
```

```python
# ô R-2: chọn đích RAFT + CỔNG; dựng cặp GA-DPO trên cùng mẫu
# (SPICE chạy 2 lượt, ~20–40 phút mỗi lượt)
rc = py(
    f"{RA}/raft_chon.py",
    "--vao", f"{W}/raft_mau_0.jsonl", f"{W}/raft_mau_1.jsonl",
    "--out", f"{W}/train_raft.jsonl",
    "--bao", f"{W}/raft_chon.json",
)
print(json.load(open(f"{W}/raft_chon.json")))

assert rc == 0, (
    "⛔ CỔNG KHÔNG ĐẠT — dưới 15% câu nhắc có mẫu trội greedy; "
    "dừng cả RAFT lẫn GA-DPO. Gửi raft_chon.json"
)

assert py(
    f"{RA}/mau_sang_ga.py",
    "--vao", f"{W}/raft_mau_0.jsonl", f"{W}/raft_mau_1.jsonl",
    "--ra", f"{W}/mau_ga.jsonl",
) == 0

assert py(
    f"{RA}/ga_dpo.py",
    "--cap",
    "--mau-file", f"{W}/mau_ga.jsonl",
    "--out", f"{W}/cap_all.jsonl",
) == 0
```

```python
# ô R-3: RAFT — chạy thử 2 bước rồi SFT thật
# (tiếp adapter ck500, LR 1e-5), tự dừng trước 11 h
p = chay(
    "ra_train.py",
    ["--merged", M, "--ckpt", CK500, "--data", f"{W}/train_raft.jsonl",
     "--lr", "1e-5", "--out", f"{W}/thu_raft", "--n", "32"],
    f"{W}/thu_raft.log",
    0,
)
doi([p], [f"{W}/thu_raft.log"])
print(open(f"{W}/thu_raft.log").read()[-1200:])

con = 11.0 - (time.time() - T0) / 3600 - 0.4

p = chay(
    "ra_train.py",
    ["--merged", M, "--ckpt", CK500, "--data", f"{W}/train_raft.jsonl",
     "--lr", "1e-5", "--out", f"{W}/raft_sft",
     "--max-hours", f"{con:.2f}"],
    f"{W}/train_raft.log",
    0,
)
doi([p], [f"{W}/train_raft.log"])
print(open(f"{W}/train_raft.log").read()[-2000:])

for d in (f"{W}/thu_raft", M, RA):
    shutil.rmtree(d, ignore_errors=True)

assert os.path.exists(f"{W}/raft_sft/final/adapter_model.safetensors"), (
    "⛔ chưa có raft_sft/final — xem mục 7"
)

print(sorted(os.listdir(W)), f"{(time.time()-T0)/3600:.2f} h")
```

Dòng cần thấy:

- R-1: `[câu nhắc] hàng [1000, 3000) trên 3991 · shard 0/2: 1000` và `[điểm lưu] …grpo-spice-ck500`.
- R-2: `[RAFT chọn] {… "ty_le_doi": …}` → `CỔNG RAFT: ĐẠT`; từ `ga_dpo.py`: `[cặp] 2000 câu nhắc · cặp cải thiện N (x%) · cặp giữ …` và `CỔNG G1: … ĐẠT`. Hai tỉ lệ phải gần nhau (cùng luật; chrF hai script tính hơi khác).
- R-3: `[adapter] … tham số học 14,966,784 (ck500 14,966,784)`, `[kiểm nhãn]` in đúng một câu đích, `[xong] … → …/raft_sft/final`.

Sau commit: Output → New Dataset, tên `raft-313-out` (chứa `raft_mau_*.jsonl`, `cap_all.jsonl`, `train_raft.jsonl`, `raft_chon.json`, `raft_sft/`, log). Notebook D và E đọc dataset này.

## 4. Notebook D — Colab L4 (hoặc A100), GA-DPO

Runtime: L4 trước (rẻ hơn, 24 GB, có bf16). Chỉ chuyển A100 nếu L4 tràn bộ nhớ hoặc chậm hơn A100 quá 1,5 lần (thì tự chọn máy của dự án). `ga_dpo.py` tự dừng nếu GPU không có bf16 (T4 không chạy được).

Cần file `kaggle.json` (Kaggle → Settings → API → Create New Token) của tài khoản thấy được các dataset ở 2.2 và `raft-313-out`.

```python
# ô D-1: gói + kiểm GPU
!pip -q install 'transformers==5.18.0' 'peft==0.21.1' accelerate kaggle safetensors
!pip -q uninstall -y torchao

import torch
print(torch.cuda.get_device_name(0))
assert torch.cuda.get_device_capability()[0] >= 8, "⛔ cần L4/A100 (bf16)"
```

```python
# ô D-2: tải dữ liệu từ Kaggle
from google.colab import files
files.upload()  # chọn kaggle.json

!mkdir -p ~/.kaggle && mv kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json

TK = "<tài khoản Kaggle chứa raft-313 và raft-313-out>"

!kaggle datasets download -d trangphngngc/ra-sft-script -p /content/src --unzip -q
!kaggle datasets download -d trangphngngc/fgrb-p1-bundle -p /content/bundle --unzip -q
!kaggle datasets download -d trangphngngc/grpo-spice-ck500 -p /content/ck500 --unzip -q
!kaggle datasets download -d {TK}/raft-313 -p /content/code313 --unzip -q
!kaggle datasets download -d {TK}/raft-313-out -p /content/r313 --unzip -q
```

```python
# ô D-3: đường dẫn, chép mã, hoà S1, đổi đường dẫn ảnh trong tệp cặp
import os, glob, shutil, subprocess, json

W = "/content/w"
os.makedirs(W, exist_ok=True)
M = "/content/s1_merged"

BUNDLE = next(
    r for r, d, f in os.walk("/content/bundle")
    if "adapter_s1_seed101" in d and "images" in d
)
CK = next(
    r for r, d, f in os.walk("/content/ck500")
    if "adapter_config.json" in f
)
SRC = os.path.dirname(
    next(glob.iglob("/content/src/**/grpo_spice.py", recursive=True))
)
C313 = os.path.dirname(
    next(glob.iglob("/content/code313/**/ga_dpo.py", recursive=True))
)
CAP = next(glob.iglob("/content/r313/**/cap_all.jsonl", recursive=True))

for f in ("grpo_spice.py", "build_branch_data.py"):
    shutil.copy(f"{SRC}/{f}", W)
for f in ("ga_dpo.py", "tron_adapter.py", "mau_sang_ga.py"):
    shutil.copy(f"{C313}/{f}", W)

def run(*a):
    r = subprocess.run(["python", *a], cwd=W, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-3000:])
    assert r.returncode == 0

run("grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", M)
run(
    "mau_sang_ga.py",
    "--vao", CAP,
    "--ra", f"{W}/cap_colab.jsonl",
    "--anh-moi", f"{BUNDLE}/images",
)

miss = [
    json.loads(l)["image"]
    for l in open(f"{W}/cap_colab.jsonl")
    if not os.path.exists(json.loads(l)["image"])
]
print(
    "cặp:", sum(1 for _ in open(f"{W}/cap_colab.jsonl")),
    "· thiếu ảnh:", len(miss)
)
assert not miss
```

```python
# ô D-4: train GA-DPO
# (DPO + NLL, β 0,1, λ 1, lr 5e-6, tích luỹ 16 cặp, 1 lượt)
run(
    "ga_dpo.py",
    "--train",
    "--merged", M,
    "--ck500", CK,
    "--cap-file", f"{W}/cap_colab.jsonl",
    "--out", "/content/dpo",
    "--kieu", "dpo",
)
```

Dòng cần thấy: `[kiểm] token trả lời: '…<|im_end|>'` (đúng câu chosen); các dòng `bước k/N · marg … · acc … · lp_c …`; cuối cùng `[xong] … log-p/token câu chosen: đầu … → cuối …`. Nếu in `⚠ log-p câu chosen giảm > 10%` thì chạy lại ô D-4 với thêm `--lam 2`.

```python
# ô D-5: ghép adapter DPO với ck500 thành MỘT adapter trên S1 hoà
# (ghép hạng, chính xác), rồi đẩy lên Kaggle
cfg_ck = json.load(open(f"{CK}/adapter_config.json"))

p = "/content/dpo/final/adapter_config.json"
c = json.load(open(p))
c["base_model_name_or_path"] = cfg_ck.get("base_model_name_or_path")
json.dump(c, open(p, "w"), indent=2)

run(
    "tron_adapter.py",
    "--vao", f"{CK}:1",
    "--vao", "/content/dpo/final:1",
    "--ra", "/content/ck500_dpo",
)

json.dump(
    {
        "title": "gadpo-313-adapter",
        "id": f"{TK}/gadpo-313-adapter",
        "licenses": [{"name": "CC0-1.0"}],
    },
    open("/content/ck500_dpo/dataset-metadata.json", "w"),
)

!kaggle datasets create -p /content/ck500_dpo -q
```

Và `base_model_name_or_path` là bắt buộc: `tron_adapter.py` dừng nếu hai adapter khác trường này, mà adapter DPO train trên Colab sẽ ghi đường dẫn Colab. Hai adapter cùng nền thật (S1 hoà), chỉ khác chuỗi đường dẫn; `tron_adapter.py` tự kiểm lệch tương đối < `1e-5` rồi mới ghi.

## 5. Notebook E — Kaggle T4 ×2, chấm hai nhánh (~7 h)

Thêm input: `raft-313`, `ra-sft-script`, `fgrb-p1-bundle`, `grpo-spice-ck500`, `raft-313-out`, `gadpo-313-adapter`, `uyenle0712/thesis-score`. Chạy ô 0-1, ô 0-2, rồi:

```python
# ô E-1: tìm hai adapter, sinh greedy (không khởi, như ck500)
# trên val và tập kiểm cho mỗi nhánh
NHANH = {
    "raft": os.path.dirname(tim("raft_sft/final/adapter_config.json"))
}

try:
    NHANH["dpo"] = os.path.dirname(
        next(
            p
            for s in range(1, 6)
            for p in glob.glob("/kaggle/input/" + "*/" * s + "adapter_config.json")
            if "gadpo-313-adapter" in p
        )
    )
except StopIteration:
    print("⚠ chưa có gadpo-313-adapter - chỉ chấm RAFT")

PKG = os.path.dirname(os.path.dirname(tim("harness/score_run.py")))
TEST = f"{PKG}/harness/dg1_cache/test_ac"
print(NHANH, PKG)

def sinh(ten, ck, recs, ocr, img, expect):
    logs = [f"{W}/{ten}_{i}.log" for i in (0, 1)]
    ps = [
        chay(
            "ra_gen.py",
            ["--merged", M, "--ckpt", ck, "--recs", recs, "--ocr", ocr,
             "--images", img, "--expect", str(expect),
             "--out", f"{W}/{ten}_{i}.jsonl", "--shard", f"{i}/2"],
            logs[i],
            i,
        )
        for i in (0, 1)
    ]
    doi(ps, logs)
    with open(f"{W}/{ten}.jsonl", "w") as f:
        for i in (0, 1):
            f.write(open(f"{W}/{ten}_{i}.jsonl").read())

for n, ck in NHANH.items():
    sinh(
        f"pred_{n}_val",
        ck,
        f"{BUNDLE}/p1_val_rows.jsonl",
        f"{BUNDLE}/ocr.jsonl",
        f"{BUNDLE}/images",
        1002,
    )
    sinh(
        f"pred_{n}_test",
        ck,
        f"{TEST}/test.jsonl",
        f"{TEST}/ocr.jsonl",
        f"{TEST}/images",
        4463,
    )
```

```python
# ô E-2: chấm — val (chỉ xem) và tập kiểm
# (7 thước, --check tái lập ck500)
pv = sum(
    [["--pred", f"{n}={W}/pred_{n}_val.jsonl"] for n in NHANH],
    [],
)
pt = sum(
    [["--pred", f"{n}={W}/pred_{n}_test.jsonl"] for n in NHANH],
    [],
)

assert py(
    f"{RA}/ra_score.py",
    "--recs", f"{BUNDLE}/p1_val_rows.jsonl",
    "--pred", f"ck500={SRC}/pred_ck500_vallon.jsonl",
    *pv,
    "--no-bert",
    "--out", f"{W}/diem_val_314.json",
) == 0

assert py(
    f"{RA}/ra_score.py",
    "--recs", f"{TEST}/test.jsonl",
    "--pred", f"ck500={SRC}/pred_ck500_test.jsonl",
    *pt,
    "--check",
    "--out", f"{W}/diem_test_314.json",
) == 0
```

```python
# ô E-3: exec cho mỗi nhánh
# chấm UGround câu khác ck500 + 40 câu ck500 không đổi để hiệu chuẩn
ck = {
    (d["episode_id"], d["step_id"]): d["pred"]
    for d in map(json.loads, open(f"{SRC}/pred_ck500_test.jsonl"))
}

def ghi(p, ks, P):
    with open(p, "w") as f:
        for k in ks:
            f.write(
                json.dumps(
                    {"episode_id": k[0], "step_id": k[1], "pred": P[k]},
                    ensure_ascii=False,
                )
                + "\n"
            )

def cham(E, ten, gpu):
    return subprocess.Popen(
        [
            "python", f"{PKG}/harness/score_run.py",
            "--mode", "score",
            "--preds", f"{E}/{ten}.jsonl",
            "--out", f"{E}/score_{ten}.json",
        ],
        stdout=open(f"{E}/score_{ten}.log", "w"),
        stderr=subprocess.STDOUT,
        env={**ENV, "CUDA_VISIBLE_DEVICES": str(gpu)},
        cwd=W,
        start_new_session=True,
    )

for n in NHANH:
    E = f"{W}/exec_{n}"
    os.makedirs(E, exist_ok=True)

    P = {
        (d["episode_id"], d["step_id"]): d["pred"]
        for d in map(json.loads, open(f"{W}/pred_{n}_test.jsonl"))
    }

    doi_k = sorted(k for k in P if P[k] != ck[k])
    cal = random.Random(20261010).sample(
        sorted(k for k in P if P[k] == ck[k]),
        40,
    )

    print(
        f"[{n}] câu khác ck500: {len(doi_k)} · hiệu chuẩn: {len(cal)}",
        flush=True,
    )

    for i in (0, 1):
        ghi(f"{E}/cal_{i}.jsonl", cal[i::2], ck)
        ghi(f"{E}/cw_{i}.jsonl", doi_k[i::2], P)

    for loai in ("cal", "cw"):
        ps = [cham(E, f"{loai}_{i}", i) for i in (0, 1)]
        doi(ps, [f"{E}/score_{loai}_{i}.log" for i in (0, 1)])

for d in (M, RA):
    shutil.rmtree(d, ignore_errors=True)

shutil.make_archive("/tmp/ket_qua_314_E", "zip", W, ".")
shutil.move("/tmp/ket_qua_314_E.zip", f"{W}/ket_qua_314_E.zip")
print(f"{(time.time()-T0)/3600:.2f} h")
```

Nếu GA-DPO chưa xong khi chạy E: E vẫn chấm RAFT. Khi có `gadpo-313-adapter`, chạy lại E (nó chỉ cần nhánh `dpo`; muốn tiết kiệm thì sửa `NHANH` chỉ còn `dpo`).

## 6. Chấm trên máy nhà và quyết định

> Tiêu đề mục 6 không nằm trong khung ảnh; phần dưới đây được nối theo nội dung nhìn thấy.

Giải nén `ket_qua_314_E.zip` vào `thesis-master/runs/rd314/`, rồi với mỗi nhánh `n ∈ {raft, dpo}`:

```bash
cd /Users/P836901/Documents/Self-learning/thesis

_venv_308/bin/python _scripts/313/doc_exec_cw.py \
  --exec-dir thesis-master/runs/rd314/exec_$n \
  --pred thesis-master/runs/rd314/pred_${n}_test.jsonl \
  --ten $n

_venv_308/bin/python _scripts/313/ktc_chu.py \
  --a thesis-master/runs/rd314/pred_${n}_test.jsonl \
  --b thesis-master/_scripts/304/ra-sft-script/pred_ck500_test.jsonl \
  --ten-a $n \
  --ten-b ck500 \
  --out thesis-master/runs/rd314/ktc_$n.json
```

Mốc tập kiểm: ck500 BLEU-4 **52,36** · METEOR **37,91** · ROUGE-L **68,34** · CIDEr-D **430,04** · SPICE **45,79** · chrF **62,86** · BERTScore **67,07** · exec **60,65 [58,90; 62,38]**.

| kết quả | làm gì |
|---|---|
| cổng R-2 trượt | dừng cả hai nhánh; mẫu ck500 trên câu nhắc train không trội greedy đủ nhiều |
| ít nhất một nhánh ≥ 4/7 thước chữ hơn ck500 | lấy nhánh tốt hơn làm thành phần thứ hai sau GRPO-SPICE; báo cả hai nhánh cạnh nhau |
| nhánh tốt hơn ≥ 4/7 nhưng exec thấp hơn có ý nghĩa | báo được trên thước chữ, phải khai exec |
| cả hai < 4/7 | ghi vào các hướng đã thử; giữ ck500 (+ R3 nếu cần số chữ) |

Nếu một nhánh thắng, nên chạy thêm đối chứng `gold`: `ga_dpo.py --train --kieu gold` trên Colab, cùng cặp, chỉ học câu chuẩn. Đối chứng này trả lời câu “có phải chỉ do thêm dữ liệu”. Agent viết action riêng khi cần.

## 7. Sự cố thường gặp

| hiện tượng | làm gì |
|---|---|
| assert 2 GPU (Kaggle) | đổi Accelerator sang T4 ×2 |
| R-1 không in hàng `[1000, 3000)` trên 3991 | bundle khác; dừng, gửi log |
| R-2 `CỔNG … KHÔNG ĐẠT` | đúng thiết kế; gửi `raft_chon.json` và 4 dòng `[cặp]` của `ga_dpo` |
| SPICE ở R-2 lâu hoặc lỗi bộ nhớ Java | `ga_dpo.py --cap` tự chia khúc 2.000 câu; `raft_chon.py` chạy một lượt. Lỗi bộ nhớ thì gửi log để chia khúc |
| R-3 `[dừng giờ]` | commit lại với `raft-313-out` làm input, chép `raft_sft/last` vào `W/raft_sft/last`, chạy lại lệnh train |
| D-4 tràn bộ nhớ trên L4 | chuyển A100 |
| D-4 cảnh báo log-p giảm > 10% | chạy lại với `--lam 2` |
| D-5 `tron_adapter` báo khác khoá | adapter DPO và ck500 khác tên module (khác phiên bản transformers/peft). Gửi lỗi, agent sửa |
| E-2 `--check` LỆCH | bộ chấm khác lượt 304; dừng đọc Δ |

## 8. Gửi lại cho chat

1. R: `raft_chon.json`; 4 dòng `[cặp]` + `CỔNG G1` của `ga_dpo`; 15 dòng cuối `train_raft.log`.
2. D: dòng `[kiểm] token trả lời`, 5 dòng `bước …` cuối, dòng `[xong]` của `ga_dpo`, output `tron_adapter`.
3. E: bảng cuối ô E-2 (val và tập kiểm), số câu khác ck500 mỗi nhánh ở ô E-3.
4. Máy nhà: output `doc_exec_cw.py` và `ktc_chu.py` cho từng nhánh.

## 9. Việc agent không làm

- Không chạy Kaggle/Colab, **không commit, không sửa luận văn**.
- Script nằm ngoài `thesis-master/`. Muốn đưa vào repo thì tự chép (ví dụ `harness/raft_gadpo/`) rồi: `git add harness/raft_gadpo && git commit -m "RAFT + GA-DPO trên cùng mẫu (314)" && git push`.

## 10. Kiểm đã làm trên máy

- `raft_mau.py --tu-kiem`: ĐẠT. Lấy đúng hàng `[1000, 3000)`, không lẫn 1.000 câu nhắc ck500, hai shard ghép đủ 2.000.
- `raft_chon.py --tu-kiem`: ĐẠT với SPICE giả. Chọn mẫu trội greedy trên ba thước; giữ greedy khi không có; loại mẫu lệch độ dài > 3 từ. chrF thật (sacrebleu) chạy được.
- `mau_sang_ga.py --tu-kiem`: ĐẠT.
- Tệp mẫu sau khi đổi định dạng chạy qua `ga_dpo.cap` (SPICE giả): ra đúng cặp “cải thiện” (mẫu trội, greedy) và cặp “giữ” (greedy, mẫu thua mọi thước), in đủ dòng `[cặp]` và `CỔNG G1`.
- `ktc_chu.py`, `doc_exec_cw.py`: tái lập số R3 (lượt 312).
- Chưa chạy: mọi phần GPU; `ga_dpo.py --train` và `tron_adapter.py` chưa chạy lần nào kể từ khi viết ở lượt 295.

# Phụ lục — mã nguồn nguyên văn

`grpo_spice.py`, `build_branch_data.py`, `ra_train.py`, `ra_gen.py`, `ra_score.py` dùng nguyên bản trong `trangphngngc/ra-sft-script` (trên đĩa: `thesis-master/_scripts/304/ra-sft-script/`).

## Phụ lục A — `raft_mau.py`

> Ảnh chỉ hiển thị phần đầu của file; phần tiếp theo nằm ngoài khung ảnh.

```python
# -*- coding: utf-8 -*-
"""313 - RAFT bước 1: ck500 sinh greedy + G mẫu (mặc định T = 0,7) trên câu nhắc train MỚI (Kaggle T4).

Câu nhắc lấy bằng đúng `grpo_spice.dung_hang` (cùng thứ tự xáo hạt 101 như lúc train ck500). ck500 đã dùng
hàng [0, 1000); lượt này lấy hàng [--tu, --den) - mặc định [1000, 3000), tức 2.000 câu nhắc ck500 CHƯA thấy trong GRPO.
Đường sinh giống ck500 lúc chấm (`s1_merged` fp16 + adapter, SYS + [ảnh, "\n" + body]).

    python raft_mau.py --bundle B --merged M --ckpt CK500 --out raft_mau_0.jsonl --shard 0/2
    python raft_mau.py --tu-kiem    # kiểm cắt hàng + định dạng trên dữ liệu giả, không cần GPU

Mỗi dòng ra: {key, image, body, gold, greedy, samples[G]}. Nối tiếp được.
"""

import os, sys, json, time, argparse

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
HRF = os.path.dirname(os.path.abspath(__file__))

# [phần tiếp theo của file nằm ngoài khung ảnh]
```
