# 309 — ACTION: chạy CW-RA trên Kaggle (10/10/2026)

File tự chứa. Đọc từ đầu tới cuối là chạy được. Mã nguồn bốn script Kaggle và script đọc exec nằm nguyên văn ở Phụ lục A–E; bản trên đĩa ở `/Users/P836901/Documents/Self-learning/thesis/_scripts/308/`.

Phần căn cứ, số đo 0 GPU và tranh luận nằm ở `308_THANH_PHAN_CW_RA_VUOT_CK500_10_10.md`. File này chỉ là cách chạy.

## 1. Mục tiêu

Train và chấm CW-RA: ck500 + khối 4 câu mẫu truy hồi + thẻ do mô hình sinh, `[COPY i]` (chép nguyên câu mẫu thứ i) hoặc `[WRITE]` rồi tự viết.

- Thẻ COPY học từ câu chuẩn: gán khi câu mẫu trùng câu chuẩn.
- Hàng còn lại học `[WRITE]` + câu greedy của chính ck500 (tự chưng cất), để nhánh viết không trôi khỏi ck500.
- Lúc chạy: chép khi xác suất thẻ COPY ≥ τ. τ chốt một lần trên val lớn.

Câu hỏi của lượt chạy: trên 4.463 bước click tập kiểm, CW-RA có cao hơn ck500 ở ≥ 4/7 thước chữ không (BLEU-4, METEOR, ROUGE-L, CIDEr-D, SPICE, chrF, BERTScore), và exec có giữ được mức ck500 không.

## 2. Tổng quan

| commit | việc | máy | thời gian ước |
| --- | --- | --- | --- |
| 1 | kiểm đường sinh 20 bước → sinh câu ck500 trên 3.991 hàng dạy (không khối) → dựng dữ liệu CW → chạy thử 2 bước → train 250 bước | T4 ×2 | ~9,5 h |
| 2 | sinh CW trên val lớn (1.002) và tập kiểm (4.463) → chốt τ trên val → chấm 7 thước tập kiểm → chấm exec câu khác ck500 | T4 ×2 | ~5 h |
| máy nhà | đọc exec, D.3, AitW bằng `doc_exec_cw.py` | CPU | ~1 phút |

Tổng ~14,5 h T4, 0 đồng. Kiểm hạn mức GPU tuần của tài khoản trước khi bấm. Hai commit nên chạy trên cùng một tài khoản để commit 2 thấy output của commit 1. Nếu phải tách tài khoản: sau commit 1, vào Output → New Dataset từ output, đặt công khai, rồi thêm dataset đó vào commit 2.

## 3. Chuẩn bị

### 3.1 Dataset mới `cw-ra-309`

Tải lên 4 tệp từ `thesis/_scripts/308/` (nguyên văn ở Phụ lục A–D):

| tệp | việc | md5 |
| --- | --- | --- |
| `cw_build.py` | dựng dữ liệu dạy CW | `46f6673fb7f4c82ef972998ba960ccde` |
| `cw_gen.py` | sinh: `--mode tu` (câu ck500 không khối) và `--mode cw` (điểm thẻ + câu viết) | `6de88e6a438a1cfe732707bcbe2cade2` |
| `cw_ghep.py` | ghép câu theo τ, CPU | `7f3ac471534234712095b93056c1c03e` |
| `cw_chon_tau.py` | chốt τ trên val, một lần | `8cf825eb5168085fb46bfd6bd3872d11` |

`doc_exec_cw.py` (md5 `04e0901a63fa6f28481aadeaed0e0d50`) chạy ở máy nhà, không cần tải lên.

### 3.2 Input dùng lại (đường dẫn in trong log lượt 304)

| biến | đường dẫn | chứa |
| --- | --- | --- |
| `SRC` | `/kaggle/input/datasets/trangphngngc/ra-sft-script` | `ra_exemplars.py`, `build_branch_data.py`, `grpo_spice.py`, `ra_train.py`, `ra_score.py`, `train_tru_val.jsonl` (md5 `edbb231a…`), `ex_val_k4.jsonl`, `ex_test_k4.jsonl`, `pred_ck500_vallon.jsonl`, `pred_ck500_test.jsonl` |
| `BUNDLE` | `/kaggle/input/datasets/trangphngngc/fgrb-p1-bundle/fgrb_p1_bundle` | `p1_train_rows.jsonl`, `p1_val_rows.jsonl`, `ocr.jsonl`, `images/` |
| `CK500` | `/kaggle/input/datasets/trangphngngc/grpo-spice-ck500` | adapter ck500 |
| `TEST` | `/kaggle/input/datasets/uyenle0712/thesis-score/thesis/harness/dg1_cache/test_ac` | `test.jsonl`, `ocr.jsonl`, `images/` (chỉ commit 2) |
| `PKG` | `/kaggle/input/datasets/uyenle0712/thesis-score/thesis` | `harness/score_run.py` để chấm exec (chỉ commit 2) |
| `CW` | `/kaggle/input/datasets/<tài khoản>/cw-ra-309` | 4 script ở 3.1 |

Đã kiểm trên máy: `pred_ck500_test.jsonl` trùng từng byte với câu `sent` trong tệp chấm thô ck500 (4.463/4.463), nên ô chấm exec so câu với tệp này là đúng.

### 3.3 Hai ô đầu lấy từ notebook cũ

Cả hai commit đều Copy & Edit notebook `trangphngngc/ra-sft-t-304`, giữ nguyên:

- Ô 1: ghim `transformers 5.18.0` · `peft 0.21.1`, gỡ `torchao`. Image Kaggle mới làm hỏng peft nếu bỏ ô này.
- Ô hoà S1: tạo `/kaggle/working/s1_merged` (log in `[hoà] xong → /kaggle/working/s1_merged · dtype torch.float16`), cùng các biến `SRC`, `BUNDLE`, `CK500`.

Xoá mọi ô còn lại của notebook cũ, rồi thêm các ô ở mục 4 hoặc 5. Accelerator: **GPU T4 ×2**. Internet: bật (commit 2 cần tải UGround và mô hình của SPICE).

## 4. Commit 1 — dữ liệu + train (~9,5 h)

Thêm input `cw-ra-309`.

```python
# Ô C1-1: chép mã, hàm chạy nền
import os, json, time, shutil, subprocess, glob
W = "/kaggle/working"; RA = f"{W}/ra"; M = f"{W}/s1_merged"

def tim(duoi):
    for sau in range(1, 6):
        g = glob.glob("/kaggle/input/" + "*/" * sau + duoi)
        if g:
            return g[0]
    raise FileNotFoundError(duoi)

CW = os.path.dirname(tim("cw_gen.py"))
shutil.copytree(SRC, RA, dirs_exist_ok=True)
for f in os.listdir(CW):
    shutil.copy(f"{CW}/{f}", RA)
print("CW", CW, sorted(os.listdir(RA)))
T0 = time.time()

def chay(script, args, log, gpu):
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(gpu), PYTHONUNBUFFERED="1")
    return subprocess.Popen(["python", f"{RA}/{script}", *args], stdout=open(log, "w"),
                            stderr=subprocess.STDOUT, env=env, cwd=RA, start_new_session=True)

def doi(ps, logs):
    while any(p.poll() is None for p in ps):
        time.sleep(120)
        print(time.strftime("%H:%M"), f"{(time.time()-T0)/3600:.2f} h",
              [open(l).read().splitlines()[-1:] for l in logs], flush=True)
    assert all(p.returncode == 0 for p in ps), [open(l).read()[-2000:] for l in logs]
```

```python
# Ô C1-2: kiểm đường sinh — 20 bước val phải trùng câu ck500 đã có (~3 phút)
p = chay("cw_gen.py", ["--mode", "tu", "--merged", M, "--ckpt", CK500, "--recs", f"{BUNDLE}/p1_val_rows.jsonl",
                         "--ocr", f"{BUNDLE}/ocr.jsonl", "--images", f"{BUNDLE}/images", "--chi-cham", "--n", "20",
                         "--out", f"{W}/kiem20.jsonl"], f"{W}/kiem20.log", 0)
doi([p], [f"{W}/kiem20.log"])
A = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{W}/kiem20.jsonl"))}
B = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{SRC}/pred_ck500_vallon.jsonl"))}
trung = sum(A[k] == B[k] for k in A)
print(f"[kiểm ck500] {trung}/{len(A)}")
assert trung >= 18, "⛔ đường sinh lệch ck500 — dừng, gửi log cho chat"
```

```python
# Ô C1-3: câu greedy ck500 trên hàng dạy, câu nhắc KHÔNG khối, hai GPU (~1,6 h)
logs = [f"{W}/tu_{i}.log" for i in (0, 1)]
ps = [chay("cw_gen.py", ["--mode", "tu", "--merged", M, "--ckpt", CK500, "--recs", f"{BUNDLE}/p1_train_rows.jsonl",
                         "--ocr", f"{BUNDLE}/ocr.jsonl", "--images", f"{BUNDLE}/images", "--out", f"{W}/tu_{i}.jsonl",
                         "--shard", f"{i}/2"], logs[i], i) for i in (0, 1)]
doi(ps, logs)
with open(f"{W}/pred_ck500_train.jsonl", "w") as f:
    for i in (0, 1):
        f.write(open(f"{W}/tu_{i}.jsonl").read())
n = sum(1 for _ in open(f"{W}/pred_ck500_train.jsonl"))
print("câu ck500 trên hàng dạy:", n)
assert n >= 3900, "⛔ thiếu câu — xem tu_0.log / tu_1.log"
```

```python
# Ô C1-4: dựng dữ liệu CW (CPU, ~15 phút)
r = subprocess.run(["python", f"{RA}/cw_build.py", "--bundle", BUNDLE, "--kho", f"{SRC}/train_tru_val.jsonl",
                    "--ck500-train", f"{W}/pred_ck500_train.jsonl", "--out", f"{W}/cw_data"],
                   capture_output=True, text=True, cwd=RA)
print(r.stdout[-3000:], r.stderr[-3000:])
assert r.returncode == 0
```

Dòng cần thấy: `[xong] {"hang": ~3.9xx, "copy": ~600-800, "copy_pct": ~15-20, ...}`. Script tự dừng nếu tỉ lệ COPY ngoài 8–25%.

```python
# Ô C1-5: chạy thử 2 bước, rồi train thật, tự dừng trước 11 h
p = chay("ra_train.py", ["--merged", M, "--ckpt", CK500, "--data", f"{W}/cw_data/train_cw.jsonl",
                         "--out", f"{W}/thu_cw", "--n", "32"], f"{W}/thu_cw.log", 0)
doi([p], [f"{W}/thu_cw.log"])
print(open(f"{W}/thu_cw.log").read()[-1500:])
con = 11.0 - (time.time()-T0) / 3600 - 0.4
print(f"còn {con:.2f} h cho train")
p = chay("ra_train.py", ["--merged", M, "--ckpt", CK500, "--data", f"{W}/cw_data/train_cw.jsonl",
                         "--out", f"{W}/cw_sft", "--max-hours", f"{con:.2f}"], f"{W}/train_cw.log", 0)
doi([p], [f"{W}/train_cw.log"])
print(open(f"{W}/train_cw.log").read()[-2500:])
```

`ra_train.py` là bản lượt 304, không sửa: tiếp từ adapter ck500, LR 2e-5, lô 16, 1 epoch ≈ 250 bước, tháp thị giác không học. Dòng `[kiểm nhãn]` của chạy thử phải in đúng đích dạng `'[COPY 2]<|im_end|>'` hoặc `'[WRITE] Click ...<|im_end|>'`.

```python
# Ô C1-6: xoá thứ nặng rồi đóng gói (zip ghi ra /tmp rồi mới chuyển vào W — tránh lỗi zip tự nén chính nó)
for d in ("thu_cw", "s1_merged", "ra"):
    shutil.rmtree(f"{W}/{d}", ignore_errors=True)
shutil.make_archive("/tmp/ket_qua_309_T", "zip", W, ".")
shutil.move("/tmp/ket_qua_309_T.zip", f"{W}/ket_qua_309_T.zip")
print(os.listdir(W), f"{(time.time()-T0)/3600:.2f} h")
assert os.path.exists(f"{W}/cw_sft/final/adapter_model.safetensors"), "⛔ chưa có cw_sft/final — xem mục 8"
```

Save Version → Save & Run All (Commit).

## 5. Commit 2 — sinh, chốt τ, chấm (~5 h)

Copy & Edit `ra-sft-t-304` thêm một lần (giữ Ô 1 + ô hoà S1). Thêm input: `cw-ra-309`, `thesis-score` (uyenle0712), và output của commit 1. Ô C1-1 giữ nguyên rồi thêm:

```python
# Ô C2-1: tìm adapter CW, đặt đường dẫn tập kiểm
CWA = os.path.dirname(tim("cw_sft/final/adapter_config.json"))
PKG = "/kaggle/input/datasets/uyenle0712/thesis-score/thesis"
if not os.path.isdir(PKG):
    PKG = os.path.dirname(os.path.dirname(tim("harness/score_run.py")))
TEST = f"{PKG}/harness/dg1_cache/test_ac"
print("CWA", CWA, "\nPKG", PKG)
assert os.path.exists(f"{TEST}/test.jsonl") and os.path.exists(f"{PKG}/harness/score_run.py")
```

```python
# Ô C2-2: sinh CW trên val lớn rồi tập kiểm, hai GPU (~3,5 h)
def sinh(ten, recs, ocr, img, ex, expect):
    logs = [f"{W}/cw_{ten}_{i}.log" for i in (0, 1)]
    ps = [chay("cw_gen.py", ["--mode", "cw", "--merged", M, "--ckpt", CWA, "--recs", recs, "--ocr", ocr,
                              "--images", img, "--ra", ex, "--chi-cham", "--expect", str(expect),
                              "--out", f"{W}/cw_{ten}_{i}.jsonl", "--shard", f"{i}/2"], logs[i], i) for i in (0, 1)]
    doi(ps, logs)
    with open(f"{W}/cw_{ten}.jsonl", "w") as f:
        for i in (0, 1):
            f.write(open(f"{W}/cw_{ten}_{i}.jsonl").read())
    print(open(logs[0]).read()[:3000])

sinh("val", f"{BUNDLE}/p1_val_rows.jsonl", f"{BUNDLE}/ocr.jsonl", f"{BUNDLE}/images", f"{SRC}/ex_val_k4.jsonl", 1002)
sinh("test", f"{TEST}/test.jsonl", f"{TEST}/ocr.jsonl", f"{TEST}/images", f"{SRC}/ex_test_k4.jsonl", 4463)
```

```python
# Ô C2-3: kiểm đầu ra của thẻ trước khi chấm
import math
for ten, n in (("val", 1002), ("test", 4463)):
    C = [json.loads(l) for l in open(f"{W}/cw_{ten}.jsonl")]
    assert len(C) == n, (ten, len(C))
    assert all(all(math.isfinite(x) and x <= 0 for x in c["lp"]) for c in C), "⛔ lp không hợp lệ"
    pc = sorted(c["p_copy"] for c in C)
    print(ten, "p_copy trung vị", round(pc[n // 2], 3), "- tỉ lệ ≥ τ:",
          {t: round(100 * sum(x >= t for x in pc) / n, 1) for t in (0.3, 0.5, 0.7, 0.9)},
          "- câu viết rỗng", sum(not c["write"] for c in C))
```

Đọc nhanh: ở τ = 0,5, tỉ lệ chép nên vào khoảng 5–25%. Ra 0% hoặc gần 100% ở mọi τ nghĩa là thẻ học hỏng; vẫn chấm tiếp, nhưng gửi số này cho chat.

```python
# Ô C2-4: cài bộ chấm — chép nguyên ô cài của notebook uyenle0712/ra-score-test-304 nếu có (bản đó đã chấm ra đúng số ck500).
# Bản dự phòng:
subprocess.run("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless > /dev/null && "
               "update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java; java -version",
               shell=True)
subprocess.run("pip -q install pycocoevalcap sacrebleu bert_score", shell=True)
```

```python
# Ô C2-5: ghép lưới τ trên val, chấm 5 thước, CHỐT τ một lần
def py(*args):
    r = subprocess.run(["python", *args], capture_output=True, text=True, cwd=RA)
    print(r.stdout[-5000:], r.stderr[-2000:]); assert r.returncode == 0

py(f"{RA}/cw_ghep.py", "--cw", f"{W}/cw_val.jsonl", "--ra", f"{SRC}/ex_val_k4.jsonl", "--out-dir", f"{W}/ghep", "--ten", "val")
LUOI = ("0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.01")
py(f"{RA}/ra_score.py", "--recs", f"{BUNDLE}/p1_val_rows.jsonl", "--pred", f"ck500={SRC}/pred_ck500_vallon.jsonl",
   *sum([["--pred", f"cw_t{t}={W}/ghep/pred_cw_t{t}_val.jsonl"] for t in LUOI], []),
   "--no-spice", "--no-bert", "--out", f"{W}/diem_val_cw.json")
py(f"{RA}/cw_chon_tau.py", "--diem", f"{W}/diem_val_cw.json", "--out", f"{W}/tau_chon.json")
```

```python
# Ô C2-6: áp τ đã chốt lên tập kiểm MỘT lần, chấm đủ 7 thước + tỉ lệ chép
tau = json.load(open(f"{W}/tau_chon.json"))["tau"]
for t in (tau, 1.01):
    py(f"{RA}/cw_ghep.py", "--cw", f"{W}/cw_test.jsonl", "--ra", f"{SRC}/ex_test_k4.jsonl",
       "--out-dir", f"{W}/ghep", "--ten", "test", "--tau", str(t))
ten_ra = [f"cw_t{tau}"] if tau == 1.01 else [f"cw_t{tau}", "cw_t1.01"]
py(f"{RA}/ra_score.py", "--recs", f"{TEST}/test.jsonl", "--pred", f"ck500={SRC}/pred_ck500_test.jsonl",
   *sum([["--pred", f"{n}={W}/ghep/pred_{n}_test.jsonl"] for n in ten_ra], []),
   "--ra", f"cw_t{tau}={SRC}/ex_test_k4.jsonl", "--check", "--out", f"{W}/diem_test_cw.json")
```

`--check` dừng đọc nếu ck500 không tái lập số đã công bố (BLEU-4 52,36 · METEOR 37,92 · ROUGE-L 68,36 · CIDEr-D 430,05 · SPICE 45,79 · chrF 62,87 · BERTScore 67,07, lệch tối đa 0,06).

```python
# Ô C2-7: exec — chỉ chấm UGround các câu cw_t{τ*} khác ck500 + 40 câu ck500 không đổi để hiệu chuẩn (~30–60 phút)
import random
E = f"{W}/exec_out"; os.makedirs(E, exist_ok=True)
ck = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{SRC}/pred_ck500_test.jsonl"))}
cw = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{W}/ghep/pred_cw_t{tau}_test.jsonl"))}
doi_k = sorted(k for k in cw if cw[k] != ck[k])
cal = random.Random(20261010).sample(sorted(k for k in cw if cw[k] == ck[k]), 40)
print(f"câu khác ck500: {len(doi_k)} · hiệu chuẩn: {len(cal)}")

def ghi(p, ks, P):
    with open(p, "w") as f:
        for k in ks:
            f.write(json.dumps({"episode_id": k[0], "step_id": k[1], "pred": P[k]}, ensure_ascii=False) + "\n")

for i in (0, 1):
    ghi(f"{E}/cal_{i}.jsonl", cal[i::2], ck)
    ghi(f"{E}/cw_{i}.jsonl", doi_k[i::2], cw)

def cham(ten, gpu):
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(gpu), PYTHONUNBUFFERED="1")
    return subprocess.Popen(["python", f"{PKG}/harness/score_run.py", "--mode", "score", "--preds", f"{E}/{ten}.jsonl",
                             "--out", f"{E}/score_{ten}.json"], stdout=open(f"{E}/score_{ten}.log", "w"),
                            stderr=subprocess.STDOUT, env=env, cwd=W, start_new_session=True)

for loai in ("cal", "cw"):
    ps = [cham(f"{loai}_{i}", i) for i in (0, 1)]
    doi(ps, [f"{E}/score_{loai}_{i}.log" for i in (0, 1)])
print(sorted(os.listdir(E)))
for d in ("s1_merged", "ra"):
    shutil.rmtree(f"{W}/{d}", ignore_errors=True)
shutil.make_archive("/tmp/ket_qua_309_G", "zip", W, ".")
shutil.move("/tmp/ket_qua_309_G.zip", f"{W}/ket_qua_309_G.zip")
print(f"{(time.time()-T0)/3600:.2f} h")
```

Save Version → Save & Run All (Commit).

## 6. Sau khi tải output về (máy nhà, CPU)

1. Giải nén `ket_qua_309_G.zip` vào `thesis-master/runs/cw309/`. Cũng chép `ket_qua_309_T.zip` (log train, `cw_stats.json`) vào cùng chỗ.
2. Đọc exec, D.3, AitW (cần repo có `harness/luat_d3.py`, `d3_ktc.py`, `score_run.py`, `runs/grpo_spice/score_ck500_test_raw.jsonl`, `runs/score_s1_seed101_raw.jsonl`):

```bash
cd /Users/P836901/Documents/Self-learning/thesis    # hoặc thư mục kho trên WSL
_venv_308/bin/python _scripts/308/doc_exec_cw.py --exec-dir thesis-master/runs/cw309/exec_out \
  --pred thesis-master/runs/cw309/ghep/pred_cw_t<τ>_test.jsonl
```

Script tự kiểm ba điều: 40 câu hiệu chuẩn trùng tọa độ và exec với tệp thô cũ; mọi câu khác ck500 có dòng chấm mới đúng câu đó; ck500 tái lập exec 60,65. Đã chạy thử trên máy: dựng lại R3 từ tệp thô lượt 304 ra exec 60,68 · D.3 67,11 · AitW 76,32, khớp `runs/ra304_luat/test_R3.json`.

## 7. Đọc kết quả

Bảng chính lấy từ `diem_test_cw.json`, so `cw_t{τ*}` với ck500:

| kết quả | làm gì |
| --- | --- |
| ≥ 4/7 thước chữ hơn ck500 và exec không thấp hơn ck500 có ý nghĩa (cận trên KTC của Δexec ≥ 0) | CW-RA dùng được làm thành phần thứ hai sau GRPO-SPICE |
| ≥ 4/7 thước chữ nhưng exec thấp hơn có ý nghĩa (như `ra_k4` −1,25) | không dùng làm thành phần; ghi vào các hướng đã thử. Có thể thử biến thể lọc cùng loại thao tác (mục 8) |
| < 4/7 | ghi vào các hướng đã thử; nếu cần số chữ cao thì báo R3, khai là hậu xử lý |

Đọc kèm:

- `cw_t1.01` (không chép) so ck500: độ trôi riêng của nhánh viết. Gần 0 ở mọi thước là tự chưng cất chạy đúng.
- `chep_vi_du_pct`, `chep_dung_pct_trong_so_chep` của `cw_t{τ*}`: tỉ lệ chép và tỉ lệ chép đúng. Mô phỏng ở 308 §2.3 cần chép đúng ≥ ~50%, `ra_k4` là 43,5%.
- `tau_chon.json`: τ đã chốt và bảng val của mọi τ, số val chỉ để chọn, không trích ra bài.

Mốc so (tập kiểm, đã công bố):

| thước | ck500 | ra_k4 | R3 (hậu xử lý) |
| --- | ---: | ---: | ---: |
| BLEU-4 | 52,36 | 53,47 | 53,47 |
| METEOR | 37,91 | 37,79 | 38,37 |
| ROUGE-L | 68,34 | 68,67 | 69,08 |
| CIDEr-D | 430,04 | 437,54 | 442,02 |
| SPICE | 45,79 | 46,79 | 47,13 |
| chrF | 62,86 | 62,65 | 63,44 |
| BERTScore | 67,07 | 67,52 | 67,73 |
| exec | 60,65 | 59,40 | 60,68 |

## 8. Sự cố thường gặp

| hiện tượng | làm gì |
| --- | --- |
| Ô C1-2 `[kiểm ck500] < 18/20` | dừng. Đường sinh lệch ck500 (thường do Ô 1 ghim phiên bản không chạy). Gửi `kiem20.log` |
| `peft` lỗi khi nạp adapter | Ô 1 chưa gỡ `torchao` hoặc chưa ghim `peft 0.21.1` |
| Ô C1-5 in `[dừng giờ]` lưu ở bước x/250 | train chưa xong vì hết giờ. Commit lại notebook chỉ với Ô 1, ô hoà S1, Ô C1-1 và lệnh train của Ô C1-5 (giữ nguyên `--out`, thêm output commit 1 làm input rồi chép `cw_sft/last` vào `W/cw_sft/last` trước khi chạy), `ra_train.py` tự nối tiếp từ `last` |
| `cw_build.py` dừng ở assert tỉ lệ COPY | gửi dòng `[xong]` cho chat. Không sửa ngưỡng |
| Ô C2-3: tỉ lệ chép ~0% ở mọi τ | thẻ COPY không học được. Vẫn chấm; `cw_t1.01` cho biết nhánh viết có giữ ck500 không |
| Ô C2-6 `--check` báo LỆCH | bộ chấm khác lượt 304. Dừng đọc Δ, gửi log |
| exec giảm có ý nghĩa | biến thể dự phòng, CPU: chỉ chép khi lớp động từ của câu mẫu trùng lớp động từ của câu `write` do chính mô hình sinh. Hỏi chat để viết script; không cần chạy lại GPU, chỉ chấm UGround lại phần câu đổi |
| zip 0 byte hoặc đầy đĩa | không xảy ra với ô ở đây (zip ghi ra `/tmp`). Nếu đầy đĩa, xoá `cw_{val,test}_{0,1}.jsonl` sau khi đã gộp |

## 9. Gửi lại cho chat

1. Commit 1: dòng `[kiểm ck500]`; dòng `[xong]` của `cw_build.py`; 10 dòng cuối `train_cw.log`.
2. Commit 2: output Ô C2-3; `tau_chon.json`; bảng in cuối Ô C2-6 hoặc tệp `diem_test_cw.json`.
3. Máy nhà: toàn bộ output của `doc_exec_cw.py`.

## 10. Việc agent không làm

- Không chạy Kaggle, không commit, không sửa luận văn.
- Script mới nằm ngoài `thesis-master/`. Muốn đưa vào repo thì tự chép (ví dụ `harness/cw_ra/`) rồi: `git add harness/cw_ra && git commit -m "CW-RA: dựng dữ liệu, sinh, ghép, chốt τ, đọc exec (309)" && git push`

## 11. Kiểm đã làm trên máy

- `cw_build.py --tu-kiem`, `cw_ghep.py --tu-kiem`, `cw_chon_tau.py --tu-kiem`: ĐẠT.
- `cw_gen.py --dry` trên 4.463 bước click tập kiểm; câu nhắc trùng câu nhắc `ra_k4` lượt 304, thẻ in đúng `[WRITE]`, `[COPY 1]` … `[COPY 4]`.
- `doc_exec_cw.py --tu-kiem`: ĐẠT (tái lập R3 tuyệt đối).
- Chưa chạy: phần nạp mô hình của `cw_gen.py` và toàn bộ GPU. Ô C1-2 và Ô C2-3 là hai chốt kiểm đặt sớm để lôi lỗi ra trước khi tốn giờ.

# Phụ lục — mã nguồn nguyên văn

`ra_exemplars.py`, `build_branch_data.py`, `grpo_spice.py`, `ra_train.py`, `ra_score.py` dùng nguyên bản lượt 304 trong dataset `trangphngngc/ra-sft-script` (và `thesis-master/_scripts/304/ra-sft-script/`), không chép lại.

## Phụ lục A — `cw_build.py`

```python
# -*- coding: utf-8 -*-
"""308 - dựng dữ liệu CW-RA (chép hay viết, có truy hồi) từ p1_train_rows (CPU, ~10-20 phút).

Mỗi hàng: câu nhắc S1 + khối k = 4 câu mẫu dựng ĐÚNG như lúc chấm (`Kho.cho_test`, bỏ chính tác vụ).
Đích:
  "[COPY i]"              nếu câu mẫu thứ i trùng nguyên văn câu chuẩn (sau tách từ) - i nhỏ nhất
  "[WRITE] " + câu ck500  còn lại; câu ck500 là câu greedy của chính ck500 trên câu nhắc KHÔNG khối (tự chưng cất)
Ra --out/train_cw.jsonl (key, image, body, gold) - đưa thẳng vào ra_train.py, không sửa gì ở ra_train.py.

  python cw_build.py --bundle B --kho train_tru_val.jsonl --ck500-train pred_ck500_train.jsonl --out O
  python cw_build.py --tu-kiem                 # kiểm logic trên dữ liệu giả, không cần gói
"""
import os, sys, json, random, argparse, collections, time

HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, "/kaggle/working/ra", os.path.join(HERE, "..", "..", "thesis-master", "_scripts", "304", "ra-sft-script")):
    if os.path.isdir(p):
        sys.path.insert(0, p)

import ra_exemplars as RA
from build_branch_data import prompt_body

TAG_W = "[WRITE]"
tag_c = lambda i: f"[COPY {i}]"


def doc(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")]


def ocr_toks(o):
    return {w for it in (o or {"items": []})["items"][:24] for w in RA.tok(it.get("text", ""))}


def nhan(gold, exs, ck):
    g = RA.tok(gold)
    for i, e in enumerate(exs, 1):
        if RA.tok(e["sent"]) == g:
            return tag_c(i), "copy"
    if not (ck or "").strip():
        return None, "ck500_rong"
    return f"{TAG_W} {ck.strip()}", "write"


def dung(rows, kho, ocr, CK, img_of, kiem_anh=True):
    out, st = [], collections.Counter()
    for r in rows:
        gold = (r.get("target_instruction") or "").strip()
        k = (r["episode_id"], r["step_id"])
        if not gold:
            st["bo_rong"] += 1
            continue
        if k not in CK:
            st["bo_thieu_ck500"] += 1
            continue
        img = img_of(r)
        if kiem_anh and not os.path.exists(img):
            st["bo_thieu_anh"] += 1
            continue
        x = dict(goal=r["goal"], history=r.get("history") or [])
        exs = kho.cho_test(x, 4, ocr_toks(ocr.get(r["image"])), own=r["episode_id"])
        body = prompt_body(x, ocr.get(r["image"]))
        body = RA.chen(body, exs) if exs else body
        lab, loai = nhan(gold, exs, CK[k])
        if lab is None:
            st["bo_" + loai] += 1
            continue
        st[loai] += 1
        st["ck500_dung_trong_write"] += loai == "write" and RA.tok(CK[k]) == RA.tok(gold)
        out.append(dict(key=f"{k[0]}_{k[1]}", image=img, body=body, gold=lab))
    return out, st


def tu_kiem():
    kho_recs = []
    for e in range(40):
        for s in range(4):
            kho_recs.append(dict(episode_id=e, step_id=s, goal=f"open app {e % 5} and buy item {e % 7}",
                                 history=[f"step {s - 1} of {e % 5}"] if s else [], image=f"x{e}_{s}.png",
                                 target_instruction=f"Click on button {e % 5} {s}", action={"action_type": "click"}))
    kho = RA.Kho(kho_recs)
    rows = kho_recs[:30]
    CK = {(r["episode_id"], r["step_id"]): ("" if i == 3 else f"Tap item {i}") for i, r in enumerate(rows)}
    out, st = dung(rows, kho, {}, CK, lambda r: r["image"], kiem_anh=False)
    print("[tự kiểm]", dict(st))
    k3 = f"{rows[3]['episode_id']}_{rows[3]['step_id']}"
    o3 = [o for o in out if o["key"] == k3]
    assert st["copy"] > 0 and st["write"] > 0, st
    assert (o3 and o3[0]["gold"].startswith("[COPY ")) or (not o3 and st["bo_ck500_rong"] == 1), (o3, st)
    for o in out:
        assert o["gold"].startswith("[COPY ") or o["gold"].startswith(TAG_W + " "), o["gold"]
        if o["gold"].startswith("[COPY "):
            i = int(o["gold"][6:-1])
            sent = [l for l in o["body"].split("\n") if l.startswith(f"{i}. ")][0].split("Bước kế: ", 1)[1]
            r = next(x for x in rows if f"{x['episode_id']}_{x['step_id']}" == o["key"])
            assert RA.tok(sent) == RA.tok(r["target_instruction"]), (sent, r["target_instruction"])
        assert o["body"].endswith(RA.LAST)
    print("[tự kiểm] ĐẠT — nhãn COPY trỏ đúng câu mẫu trùng câu chuẩn, nhãn WRITE mang câu ck500")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle")
    ap.add_argument("--kho")
    ap.add_argument("--ck500-train", help="pred greedy của ck500 trên p1_train_rows, câu nhắc không khối (cw_gen.py --mode tu)")
    ap.add_argument("--out")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        return tu_kiem()
    t0 = time.time()
    tr = doc(os.path.join(a.bundle, "p1_train_rows.jsonl"))
    va = doc(os.path.join(a.bundle, "p1_val_rows.jsonl"))
    vep = {r["episode_id"] for r in va}
    ocr = {o["image"]: o for o in doc(os.path.join(a.bundle, "ocr.jsonl"))}
    kho = RA.Kho(doc(a.kho), loai_ep=vep)
    CK = {(d["episode_id"], d["step_id"]): d["pred"] for d in doc(a.ck500_train)}
    tr = [r for r in tr if r["episode_id"] not in vep]
    random.Random(20261010).shuffle(tr)
    out, st = dung(tr, kho, ocr, CK, lambda r: os.path.join(a.bundle, r["image"]))
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "train_cw.jsonl"), "w", encoding="utf-8") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    S = dict(hang=len(out), copy=st["copy"], write=st["write"], copy_pct=round(100 * st["copy"] / max(1, len(out)), 1),
             ck500_dung_trong_write=st["ck500_dung_trong_write"], bo={k: v for k, v in st.items() if k.startswith("bo_")},
             kho_buoc=len(kho.tr), phut=round((time.time() - t0) / 60, 1))
    json.dump(S, open(os.path.join(a.out, "cw_stats.json"), "w"), ensure_ascii=False, indent=1)
    print("[xong]", json.dumps(S, ensure_ascii=False))
    assert 8 <= S["copy_pct"] <= 25, "⛔ tỉ lệ COPY lệch xa 13-16% đã đo ở val/test - kiểm lại kho hoặc own"


if __name__ == "__main__":
    main()
```

## Phụ lục B — `cw_gen.py`

```python
# -*- coding: utf-8 -*-
"""308 - sinh cho CW-RA, cùng đường sinh ck500 (`s1_merged` fp16 + adapter, greedy, 96 token, SYS + [ảnh, "\\n" + body]).

Hai chế độ:
  --mode tu : câu greedy KHÔNG khối, mọi loại thao tác (mặc định) - đích [WRITE] cho cw_build.py. Gắn --ckpt ck500.
  --mode cw : khối k = 4 (--ra ex_*.jsonl). Mỗi bước ghi:
      lp       log-xác suất của từng thẻ "[WRITE]", "[COPY 1]"..."[COPY k]" (ép từng thẻ, cộng log-prob token)
      p_copy   Σ exp(lp COPY) / Σ exp(lp mọi thẻ)
      copy_idx i của thẻ COPY có lp cao nhất
      write    câu sinh tiếp sau khi ép tiền tố "[WRITE]"
    Ghép theo ngưỡng τ làm ở cw_ghep.py (CPU), không sinh lại.

python cw_gen.py --mode tu --merged M --ckpt CK500 --recs B/p1_train_rows.jsonl --ocr B/ocr.jsonl --images B/images --out pred_ck500_train.jsonl --shard 0/2
python cw_gen.py --mode cw --merged M --ckpt CW/final --recs T/test.jsonl --ocr T/ocr.jsonl --images T/images --ra ex_test_k4.jsonl --chi-cham --expect 4463 --out cw_test.jsonl --shard 0/2
thêm --dry: chỉ in câu nhắc + thẻ, không nạp mô hình.
Nối tiếp được: chạy lại đúng lệnh, bước đã có trong --out được bỏ qua.
"""
import os, sys, json, math, time, argparse

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, "/kaggle/working/ra", os.path.join(HERE, "..", "..", "thesis-master", "_scripts", "304", "ra-sft-script")):
    if os.path.isdir(p):
        sys.path.insert(0, p)
from build_branch_data import prompt_body, SYS
import ra_exemplars as RA

TAPT = ("click", "long_press")
TAG_W = "[WRITE]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("tu", "cw"), required=True)
    ap.add_argument("--merged", default="")
    ap.add_argument("--ckpt", default="")
    ap.add_argument("--recs", required=True)
    ap.add_argument("--ocr", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ra", default=None)
    ap.add_argument("--chi-cham", action="store_true", help="chỉ bước click/long_press (val, test)")
    ap.add_argument("--expect", type=int, default=0)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    a.q4 = False
    assert a.mode == "tu" or a.ra, "⛔ --mode cw cần --ra"
    assert not (a.mode == "tu" and a.ra), "⛔ --mode tu là câu nhắc KHÔNG khối"

    rows = [json.loads(l) for l in open(a.recs, encoding="utf-8")]
    if a.chi_cham:
        rows = [r for r in rows if (r.get("action") or {}).get("action_type") in TAPT and "x" in r["action"]]
    rows = [r for r in rows if (r.get("target_instruction") or r.get("gold_instruction") or "").strip() or a.chi_cham]
    if a.expect:
        assert len(rows) == a.expect, f"⛔ {len(rows)} bước, cần {a.expect}"
    if a.n:
        rows = rows[:a.n]
    si, sn = map(int, a.shard.split("/"))
    rows = rows[si::sn]
    ocr = {o["image"]: o for o in map(json.loads, open(a.ocr, encoding="utf-8"))}
    thieu = [r["image"] for r in rows if not os.path.exists(os.path.join(a.images, os.path.basename(r["image"])))]
    print(f"[dữ liệu] {a.recs} · {len(rows)} bước · thiếu OCR {sum(r['image'] not in ocr for r in rows)} · thiếu ảnh {len(thieu)}",
          flush=True)
    assert a.dry or not thieu, f"⛔ thiếu ảnh, ví dụ {thieu[:3]}"

    EXM = None
    if a.ra:
        EXM = {(d["episode_id"], d["step_id"]): d["exemplars"] for d in map(json.loads, open(a.ra, encoding="utf-8"))}
        miss = sum((r["episode_id"], r["step_id"]) not in EXM for r in rows)
        assert not miss, f"⛔ tệp ví dụ thiếu {miss} bước"

    def exs_of(r):
        return EXM[(r["episode_id"], r["step_id"])] if EXM is not None else []

    def body_of(r):
        b = prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
        e = exs_of(r)
        return RA.chen(b, e) if e else b

    def tags_of(r):
        return [TAG_W] + [f"[COPY {i}]" for i in range(1, len(exs_of(r)) + 1)]

    def msg_of(r):
        return [{"role": "system", "content": SYS},
                {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body_of(r)}]}]

    print(f"[chế độ] {a.mode} · [câu nhắc bước đầu]\n{body_of(rows[0])}\n[thẻ] {tags_of(rows[0]) if a.mode == 'cw' else '-'}",
          flush=True)
    if a.dry:
        return

    import torch
    from PIL import Image
    from peft import PeftModel
    import grpo_spice as GS
    proc, model, _ = GS.nap(a)
    model = PeftModel.from_pretrained(model, a.ckpt)
    model.eval()
    print("[điểm lưu]", a.ckpt, flush=True)

    done = set()
    if os.path.exists(a.out):
        done = {(d["episode_id"], d["step_id"]) for d in map(json.loads, open(a.out, encoding="utf-8"))}
    print(f"[nối tiếp] đã có {len(done)}/{len(rows)}", flush=True)

    def enc(text, img):
        return proc(text=[text], images=[img], return_tensors="pt").to(model.device)

    def gen(text, img):
        inp = enc(text, img)
        L = inp["input_ids"].shape[1]
        with torch.no_grad():
            g = model.generate(**inp, max_new_tokens=96, do_sample=False, use_cache=True,
                               temperature=None, top_p=None, top_k=None)
        return proc.decode(g[0][L:], skip_special_tokens=True).strip()

    def lp_tag(base, img, L0, ids0, tag):
        inp = enc(base + tag, img)
        ids = inp["input_ids"][0]
        assert ids[:L0].tolist() == ids0, "⛔ token câu nhắc đổi khi nối thẻ"
        with torch.no_grad():
            lg = model(**inp).logits[0].float().log_softmax(-1)
        return float(sum(lg[j - 1, ids[j]] for j in range(L0, ids.shape[0])))

    fo = open(a.out, "a", encoding="utf-8")
    t0, moi = time.time(), 0
    for i, r in enumerate(rows):
        k = (r["episode_id"], r["step_id"])
        if k in done:
            continue
        base = proc.apply_chat_template(msg_of(r), tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.images, os.path.basename(r["image"]))).convert("RGB")
        if a.mode == "tu":
            rec = {"episode_id": k[0], "step_id": k[1], "pred": gen(base, img)}
        else:
            inp0 = enc(base, img)
            L0, ids0 = inp0["input_ids"].shape[1], inp0["input_ids"][0].tolist()
            T = tags_of(r)
            lp = [lp_tag(base, img, L0, ids0, t) for t in T]
            m = max(lp)
            z = sum(math.exp(x - m) for x in lp)
            p_copy = sum(math.exp(x - m) for x in lp[1:]) / z
            ci = (max(range(1, len(T)), key=lambda j: lp[j]) if len(T) > 1 else 0)
            w = gen(base + TAG_W, img)
            rec = {"episode_id": k[0], "step_id": k[1], "lp": [round(x, 4) for x in lp], "p_copy": round(p_copy, 5),
                   "copy_idx": ci, "write": w}
            if moi < 3:
                print(f"  [mẫu] thẻ {T} · lp {rec['lp']} · p_copy {p_copy:.3f} · write {w[:60]!r}", flush=True)
        fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fo.flush()
        moi += 1
        if (i + 1) % 50 == 0:
            dt = time.time() - t0
            print(f"  {i+1}/{len(rows)} · {dt/60:.1f} phút · {dt/moi:.2f} s/bước", flush=True)
    fo.close()
    n = sum(1 for _ in open(a.out, encoding="utf-8"))
    print(f"[xong] {n} dòng trong {a.out}", flush=True)


if __name__ == "__main__":
    main()
```

## Phụ lục C — `cw_ghep.py`

```python
# -*- coding: utf-8 -*-
"""308 - ghép câu CW-RA theo ngưỡng τ (CPU, vài giây). Không sinh lại, không nhìn câu chuẩn.

Bước có p_copy >= τ → câu mẫu thứ copy_idx (nguyên văn trong khối); còn lại → câu `write`.
τ = 1.01 nghĩa là không bao giờ chép (đo độ trôi của nhánh viết so ck500).

python cw_ghep.py --cw cw_val.jsonl --ra ex_val_k4.jsonl --out-dir O --ten val
# O/pred_cw_t{τ}_val.jsonl cho mọi τ trong lưới; rồi chấm bằng ra_score.py (--pred cw_t0.5=...).
python cw_ghep.py --tu-kiem
"""
import os, json, argparse

LUOI = (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.01)


def ghep(C, E, tau):
    out, chep = {}, 0
    for k, c in C.items():
        if c["copy_idx"] and c["p_copy"] >= tau:
            out[k] = E[k][c["copy_idx"] - 1]["sent"]
            chep += 1
        else:
            out[k] = c["write"]
    return out, chep


def tu_kiem():
    E = {(1, 0): [{"sent": "A"}, {"sent": "B"}], (1, 1): [{"sent": "C"}]}
    C = {(1, 0): dict(p_copy=0.7, copy_idx=2, write="w0"), (1, 1): dict(p_copy=0.2, copy_idx=1, write="w1")}
    assert ghep(C, E, 0.5) == ({(1, 0): "B", (1, 1): "w1"}, 1)
    assert ghep(C, E, 1.01) == ({(1, 0): "w0", (1, 1): "w1"}, 0)
    print("[tự kiểm] ĐẠT")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cw")
    ap.add_argument("--ra")
    ap.add_argument("--out-dir")
    ap.add_argument("--ten", default="val")
    ap.add_argument("--tau", type=float, default=None, help="chỉ ghép một τ (dùng cho test sau khi đã chốt τ trên val)")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        return tu_kiem()
    C = {(d["episode_id"], d["step_id"]): d for d in map(json.loads, open(a.cw, encoding="utf-8"))}
    E = {(d["episode_id"], d["step_id"]): d["exemplars"] for d in map(json.loads, open(a.ra, encoding="utf-8"))}
    assert set(C) == set(E), "⛔ thiếu khối ví dụ"
    os.makedirs(a.out_dir, exist_ok=True)
    for tau in ([a.tau] if a.tau is not None else LUOI):
        P, chep = ghep(C, E, tau)
        p = os.path.join(a.out_dir, f"pred_cw_t{tau}_{a.ten}.jsonl")
        with open(p, "w", encoding="utf-8") as f:
            for k, s in P.items():
                f.write(json.dumps({"episode_id": k[0], "step_id": k[1], "pred": s}, ensure_ascii=False) + "\n")
        print(f"τ={tau}: chép {chep}/{len(P)} ({100 * chep / len(P):.1f}%) → {p}")


if __name__ == "__main__":
    main()
```

## Phụ lục D — `cw_chon_tau.py`

```python
# -*- coding: utf-8 -*-
"""308 - chốt τ của CW-RA trên val lớn (CPU). Chạy MỘT lần; tệp chốt đã có thì từ chối chọn lại.

Đọc JSON của ra_score.py chấm val (nhánh ck500 + mọi cw_t{τ}). Luật:
  1. τ có nhiều thước chữ val cao hơn ck500 nhất (BLEU-4, METEOR, ROUGE-L, CIDEr-D, chrF);
  2. hoà thì CIDEr-D val cao hơn; 3. vẫn hoà thì τ lớn hơn (chép ít hơn).
τ = 1.01 (không chép) được tính như mọi τ khác.

python cw_chon_tau.py --diem diem_val_cw.json --out tau_chon.json
python cw_chon_tau.py --tu-kiem
"""
import os, json, argparse

THUOC = ("bleu4", "meteor", "rougeL", "cider_d", "chrf")


def chon(D):
    ck = D["ck500"]
    ung = []
    for ten, d in D.items():
        if not ten.startswith("cw_t"):
            continue
        tau = float(ten[4:])
        hon = sum(d[m] > ck[m] for m in THUOC)
        ung.append((hon, d["cider_d"], tau, ten))
    ung.sort(reverse=True)
    hon, cid, tau, ten = ung[0]
    return dict(tau=tau, nhanh=ten, hon_val=hon, cider_val=cid,
                bang=[dict(nhanh=u[3], hon=u[0], cider_d=u[1]) for u in ung])


def tu_kiem():
    D = {"ck500": dict(bleu4=54.8, meteor=39.2, rougeL=70.5, cider_d=449.0, chrf=64.5),
         "cw_t0.5": dict(bleu4=55.0, meteor=39.3, rougeL=70.6, cider_d=455.0, chrf=64.4),
         "cw_t0.7": dict(bleu4=55.1, meteor=39.3, rougeL=70.7, cider_d=452.0, chrf=64.6),
         "cw_t1.01": dict(bleu4=54.7, meteor=39.2, rougeL=70.5, cider_d=448.0, chrf=64.5)}
    c = chon(D)
    assert c["tau"] == 0.7 and c["hon_val"] == 5, c
    print("[tự kiểm] ĐẠT")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diem")
    ap.add_argument("--out")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        return tu_kiem()
    assert not os.path.exists(a.out), "⛔ τ đã chốt — không chọn lại"
    D = json.load(open(a.diem))["diem"]
    c = chon(D)
    json.dump(c, open(a.out, "w"), ensure_ascii=False, indent=1)
    for b in c["bang"]:
        print(f"{b['nhanh']:10s} hơn ck500 {b['hon']}/5 · CIDEr-D {b['cider_d']:.2f}")
    print(f"→ CHỐT τ = {c['tau']} ({c['nhanh']}) → {a.out}")


if __name__ == "__main__":
    main()
```

## Phụ lục E — `doc_exec_cw.py`

```python
# -*- coding: utf-8 -*-
"""308/309 - exec / D.3 / AitW đầy đủ cho một tệp câu (CW-RA) trên 4.463 bước click tập kiểm, 0 GPU.

Kaggle chỉ chấm UGround những bước có câu KHÁC ck500 (so từng byte với `sent` của tệp thô ck500); bước còn lại lấy
nguyên dòng của `runs/grpo_spice/score_ck500_test_raw.jsonl`. Cách làm y lượt 304 (doc_exec_304.py).
Tự kiểm: câu ck500 không đổi chấm lại (tệp score_cal_*_raw.jsonl) phải ra cùng tọa độ và exec với tệp thô cũ;
ck500 exec = 60,65; mọi bước câu khác ck500 phải có dòng chấm mới với đúng câu đó.

  python doc_exec_cw.py --exec-dir <thư mục chứa score_cal_*_raw.jsonl, score_cw_*_raw.jsonl> --pred pred_cw_t0.5_test.jsonl
  python doc_exec_cw.py --tu-kiem      # tái lập exec R3 = 60,68 từ tệp thô của lượt 304
"""
import argparse, glob, json, os, shutil, sys, tempfile

KHO = next(p for p in ("/mnt/d/Master/Thesis", "/Users/P836901/Documents/Self-learning/thesis/thesis-master")
           if os.path.isdir(p))
sys.path.insert(0, f"{KHO}/harness")
os.chdir(f"{KHO}/harness")
import luat_d3 as L
from luat_aitw_day_du import aitw_full
from d3_ktc import ktc, mcnemar
kh = L.kh


def doc(E, pred_path, ten="cw", out_json=None):
    CK = L.nap(f"{KHO}/runs/grpo_spice/score_ck500_test_raw.jsonl")
    S1 = L.nap(f"{KHO}/runs/score_s1_seed101_raw.jsonl")
    moi = lambda t: {kh(r): r for f in sorted(glob.glob(f"{E}/score_{t}_*_raw.jsonl")) for r in map(json.loads, open(f))}
    CAL, CW = moi("cal"), moi("cw")
    P = {kh(x): x["pred"] for x in map(json.loads, open(pred_path, encoding="utf-8"))}
    lech = [k for k in CAL if CAL[k].get("pred_xy") != CK[k].get("pred_xy") or CAL[k]["executable"] != CK[k]["executable"]]
    print(f"[hiệu chuẩn] {len(CAL)} câu ck500 chấm lại · lệch tọa độ/exec {len(lech)}", lech[:3])
    assert CAL and not lech, "⛔ dụng cụ lệch tệp thô ck500 — dừng"
    can = {k for k in P if P[k] != (CK[k].get("sent") or "")}
    thieu = sorted(can - set(CW))
    sai = [k for k in can & set(CW) if CW[k].get("sent") != P[k]]
    print(f"[{ten}] câu khác ck500 {len(can)} · có dòng chấm mới {len(can & set(CW))} · thiếu {len(thieu)} · câu lệch {len(sai)}")
    assert not thieu and not sai, (thieu[:3], sai[:3])
    R = {k: (CW[k] if k in can else CK[k]) for k in CK}
    with open(f"{E}/score_{ten}_gop_raw.jsonl", "w", encoding="utf-8") as f:
        for k in CK:
            f.write(json.dumps(R[k], ensure_ascii=False) + "\n")

    K = list(S1)
    assert set(K) == set(CK) == set(P) and len(K) == 4463
    for X in (CK, R, S1):
        for k in K:
            for c in ("executable", "action_ok", "toggle_ok", "hit_disk"):
                X[k].setdefault(c, 0)
    lu = lambda X: {k: dict(L.luat(X[k], k), aitwf=aitw_full(X[k], k)) for k in K}
    X = {"ck500": lu(CK), ten: lu(R), "S1/101": lu(S1)}
    cum = {k: S1[k].get("app") or f"ep{k[0]}" for k in K}
    TEN = {"vor": "exec", "d3": "D.3", "aitwf": "AitW"}
    out = {"ktc": {}, "so_sanh": {}, "cau_doi": len(can), "hieu_chuan": len(CAL)}
    for t in X:
        out["ktc"][t] = {}
        for c in TEN:
            p, lo, hi, _ = ktc(K, lambda k, cc: X[t][k][cc], c, cum)
            out["ktc"][t][c] = dict(diem=round(p, 2), lo=round(lo, 2), hi=round(hi, 2))
        print(f"{t:8s} " + " · ".join(f"{TEN[c]} {out['ktc'][t][c]['diem']:.2f} [{out['ktc'][t][c]['lo']:.2f}; {out['ktc'][t][c]['hi']:.2f}]" for c in TEN))
    assert abs(out["ktc"]["ck500"]["vor"]["diem"] - 60.65) < 0.01, "⛔ ck500 exec phải tái lập 60,65"
    for b in ("ck500", "S1/101"):
        for c in TEN:
            d, lo, hi, _ = ktc(K, lambda k, cc: X[ten][k][cc] - X[b][k][cc], c, cum)
            pha, cuu, _, p = mcnemar(K, X[b], X[ten], c)
            out["so_sanh"][f"{ten} - {b} - {TEN[c]}"] = dict(delta=round(d, 2), lo=round(lo, 2), hi=round(hi, 2), cuu=cuu, pha=pha, p=p)
            print(f"{ten} - {b:7s} {TEN[c]:5s} {d:+.2f} [{lo:+.2f}; {hi:+.2f}] · cứu {cuu} phá {pha} · p={p:.3g}")
    out_json = out_json or f"{E}/doc_exec_{ten}.json"
    json.dump(out, open(out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", out_json)
    return out


def tu_kiem():
    E0 = f"{KHO}/runs/ra304_G/exec_out/exec_out"
    pred = f"{KHO}/runs/ra304_luat/pred_R3_test.jsonl"
    T = tempfile.mkdtemp()
    for f in glob.glob(f"{E0}/score_cal_*_raw.jsonl"):
        shutil.copy(f, T)
    with open(f"{T}/score_cw_0_raw.jsonl", "w", encoding="utf-8") as fo:
        for f in sorted(glob.glob(f"{E0}/score_ghep_*_raw.jsonl")) + sorted(glob.glob(f"{E0}/score_ra_*_raw.jsonl")):
            fo.write(open(f, encoding="utf-8").read())
    o = doc(T, pred, "cw", out_json=f"{T}/x.json")
    assert abs(o["ktc"]["cw"]["vor"]["diem"] - 60.68) < 0.01 and abs(o["ktc"]["cw"]["d3"]["diem"] - 67.11) < 0.01 \
        and abs(o["ktc"]["cw"]["aitwf"]["diem"] - 76.32) < 0.01, o["ktc"]["cw"]
    print("[tự kiểm] ĐẠT — tái lập R3: exec 60,68 · D.3 67,11 · AitW 76,32 (khớp runs/ra304_luat/test_R3.json)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--exec-dir")
    ap.add_argument("--pred")
    ap.add_argument("--ten", default="cw")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    tu_kiem() if a.tu_kiem else doc(os.path.abspath(a.exec_dir), os.path.abspath(a.pred), a.ten)
```
