# 304 — ACTION: RA-SFT từ ck500 (truy hồi bộ nhớ quỹ đạo) + phép thử kho rỗng (9/10/2026)

File tự chứa. Đọc từ đầu tới cuối là chạy được. Mọi mã nguồn nằm nguyên văn ở Phụ lục A, đồng thời đã có sẵn thành tệp trong `_scripts/304/ra-sft-script/` (ngoài clone, không mất khi xoá `thesis-master/`). Lượt này không chạy git, không ghi gì vào `thesis-master/`.

## 0. Tóm tắt một đoạn

Thành phần mới: **RA-SFT (Retrieval-Augmented SFT)**. Mỗi bước, lấy 4 câu hướng dẫn của các bước giống nhất trong kho quỹ đạo train (TF-IDF trên mục tiêu + lịch sử, không dùng ảnh, không dùng CLIP) rồi chèn vào câu nhắc ngay trước dòng `Viết câu hướng dẫn cho bước tiếp theo.`. Train tiếp chính adapter ck500 khoảng 250 bước SFT để mô hình học khi nào dùng câu mẫu. Lúc chạy: một lượt sinh + một phép truy hồi CPU.

Ba câu hỏi, một lượt test:

| câu hỏi | phép so trên test 4.463 click | đạt khi |
|---|---|---|
| chính: RA-SFT có hơn ck500 không | `ra_k4 - ck500` | `≥ 4/7 thước chữ cao hơn (chỉ xét số trung bình)` |
| kho rỗng: không có câu mẫu thì có giữ được mức ck500 không | `ra_rong - ck500` | không thước nào tụt quá nhiều nhỏ (§6) |
| quy công: lợi do truy hồi hay chỉ do SFT thêm | `ra_k4 - cont` | `ra_k4` cao hơn ở đa số thước |

Chi phí: hai notebook Kaggle T4×2, khoảng 4–6 h (train) + ~7 h (sinh test + chấm). 0 đồng.

## 1. Thiết kế

| quyết định | chọn | lý do |
|---|---|---|
| điểm xuất phát | adapter ck500 (`checkpoint-500`, md5 `491fa667...`), train tiếp trên `s1_merged` 4-bit | đúng chế độ ck500 đã được train (GRPO, q4); lúc sinh gắn lên `s1_merged` fp16 như đã sinh ck500 → chỉ đổi một biến |
| dữ liệu train | `p1_train_rows.jsonl` của `fgrb-p1-bundle` (~3.960 hàng có ảnh + OCR), mọi loại thao tác | là phần train duy nhất có ảnh trên Kaggle; không chạm tác vụ val (assert) |
| kho truy hồi | `train_tru_val.jsonl` bỏ mọi tác vụ của `p1_val_rows` ⇒ 62.880 bước / 12.542 tác vụ | tác vụ test chung kho = 0 (đã đo) |
| khoá truy hồi | R1 mức bước (mục tiêu + câu lịch sử cuối) ∪ R2 mức quỹ đạo (mục tiêu → tác vụ, căn theo câu trước) | thiết kế 296-P, đã đo hợp hai khoá tốt hơn từng khoá |
| lúc train | bỏ chính tác vụ; k ngẫu nhiên 2–6, xáo thứ tự; 15% không khối, 10% khối ngẫu nhiên | chống chép mù (kiểu RobustCap); 15% không khối là thử cho phép phép thử kho rỗng |
| lúc chạy | cố định k=4, xếp theo số lần xuất hiện → phủ OCR → hạng | 296-P |
| đối chứng | `cont`: cùng hàng, cùng thứ tự, cùng đích, cùng siêu tham số, câu nhắc không khối | tách công “truy hồi” khỏi công “SFT thêm” |
| siêu tham số | lr 2e-5, cosine, warmup 10, lô 16 (1 × tích luỹ 16), 1 epoch, clip 1,0, fp16 + GradScaler | thấp hơn S1 (1e-4) để không xoá phần lợi GRPO; được tự do đổi trên val (§5.5) |
| loss | chỉ trên token câu đích + `<|im_end|>` |  |
| sinh | greedy, 96 token, fp16, `s1_merged` + adapter, câu nhắc y hệt ck500 ngoài khối | khớp `gen_test_grpo.py` đã sinh ck500 |
| chấm | BLEU-4 · METEOR 1.5 · ROUGE-L · CIDEr-D · SPICE (pycocoevalcap + PTBTokenizer) · chrF (sacrebleu) · BERTScore rescale (câu rỗng = 0) | dùng bộ chấm đã ra số luận văn; script tự tái lập số ck500 trước khi in Δ |

Ví dụ câu nhắc:

```text
Mục tiêu: I want to play the Dimitri vegas song of Martin garrix on the Vimeo app
Đã làm: Open the vimeo app
Chữ đọc được trên màn: 7:29 (3) · ? · martin garrix music · My account · On Vimeo · … (24 dòng OCR)
Ví dụ bước tương tự từ tác vụ khác (có thể không khớp màn này):
1. Mục tiêu: I want to play the Animals song of Martin garrix on the | Bước trước: Open the YouTube app | Bước kế: swipe up for more songs
2. Mục tiêu: I was at home alone and bored, so I decided to listen | Bước trước: Open the Vimeo app | Bước kế: click on the watch tab
3. Mục tiêu: I was at home alone and bored, so I decided to listen | Bước trước: Open the Vimeo app | Bước kế: Open the Vimeo app
4. Mục tiêu: I want to listen to the song Used to Love by Martin | Bước trước: Click on the second suggestion. | Bước kế: Click on the fourth song under top songs list.
Viết câu hướng dẫn cho bước tiếp theo.
```

Kho rỗng = dùng câu nhắc trên nhưng không có khối "Ví dụ..." — tức y hệt câu nhắc của ck500.

## 2. Đã kiểm trên máy nhà (CPU, không GPU)

| kiểm | kết quả | ý nghĩa |
|---|---|---|
| `py_compile` 5 script | đạt |  |
| kho truy hồi | 62.880 bước · 12.542 tác vụ · bỏ 346 tác vụ val · tác vụ test chung kho 0 | trùng số 296-P |
| khối k=4 trên 1.002 click val chứa nguyên văn câu chuẩn | 13,3% | trùng 296-P (13,3%) ⇒ module truy hồi chạy đúng như lượt trước |
| dựng dữ liệu train thử 60 hàng (bundle giả) | có khối 86,7% · khối chứa đích 19,2% · TB 4,27 ví dụ · `ra` và `cont` cùng hàng, cùng đích | đúng thiết kế 85% có khối |
| `ex_test_k4.jsonl` | 4.463 dòng, phủ đủ bước click test (chỉ đọc mục tiêu, lịch sử, OCR; không đọc câu chuẩn test) |  |
| `ra_gen.py --dry` ba chế độ (test có khối · test kho rỗng · val có khối) | câu nhắc đúng; kho rỗng in `KHÔNG có khối — câu nhắc y hệt câu nhắc của ck500` |  |
| chrF của `pred_ck500_test.jsonl` bằng cách ghép của `ra_score.py` | 62,86 (công bố 62,87; report 261 ghi Mac ra 62,86) | ghép dự đoán ↔ câu chuẩn đúng |
| khoá 1.002 click val ↔ `pred_ck500_vallon.jsonl` | 1.002/1.002 | phép so val chạy được |

Chưa kiểm được trên máy nhà (máy không có torch, pycocoevalcap, Java): phần train, sinh thật và 6 thước còn lại. Runbook có bước chạy thử ngắn và các assert để bắt lỗi trước lượt dài:

- `ra_train.py` in `[kiểm nhãn]` và dừng nếu phần tính loss không đúng câu đích;
- `ra_train.py` dừng nếu số tham số học ≠ 14.966.784 (cỡ ck500), nếu tháp thị giác học, nếu loss không hữu hạn;
- `ra_score.py --check` tái lập 7 số test của ck500 trước khi in Δ.

## 3. Chuẩn bị (một lần, ~10 phút)

### 3.1 Tạo dataset `ra-sft-script` trên Kaggle

Kaggle → Datasets → New Dataset → tên `ra-sft-script` → kéo cả 12 tệp trong thư mục `/Users/P836901/Documents/Self-learning/thesis/_scripts/304/ra-sft-script/` vào (34 MB) → Create.

| tệp | md5 | vai trò |
|---|---|---|
| `ra_build.py` | `30bda9a22b6da576b23350d7090f10a0` | dựng dữ liệu train ra / cont |
| `ra_train.py` | `61bb6aac00c8a4d460e770589812bc89` | SFT tiếp từ ck500 |
| `ra_gen.py` | `0d361deea9a3185115034e8be08efab2` | sinh greedy, có/không khối |
| `ra_score.py` | `35435945ff99028a75d8a147914b95c` | chấm 7 thước + tự kiểm ck500 |
| `ra_exemplars.py` | `83328e340382e5d1b9b8852617955e82` | module truy hồi (y hệt bản 296-P) |
| `grpo_spice.py` | `07ea87b6d156d1faa391a4274dffd7cf` | dùng merge và nạp (bản đã train/sinh ck500) |
| `build_branch_data.py` | `619e63e123a6dbf60086e65ee94a3912` | `prompt_body`, SYS (bản đã sinh ck500) |
| `train_tru_val.jsonl` | `edbb231a58574acf6e1968a44d1fa6c6` | kho truy hồi (63.000 dòng) |
| `ex_test_k4.jsonl` | `c9e097ca92fb7b9fabaa73a27ab04c73` | 4 câu mẫu cho mỗi bước click test |
| `ex_val_k4.jsonl` | `b733bda18f04c7013b5e67fda41f0e96` | 4 câu mẫu cho mỗi bước click val |
| `pred_ck500_test.jsonl` | `328847ac96fa3104f76cd997f4091bcd` | câu ck500 trên test (mốc so) |
| `pred_ck500_vallon.jsonl` | `d092faf6f862eec5db71110e6b5963e2` | câu ck500 trên val (mốc so, tuỳ chọn) |

### 3.2 Hạn mức

Notebook T ~4–6 h, notebook G ~7 h. Trước mỗi lần bấm, mở trang hạn mức GPU: còn dưới 8 h thì đợi tuần sau.

## 4. Ô dùng chung cho cả hai notebook

**Ô 1 — gói, Java, mốc giờ**

```python
import subprocess, sys, os, time
T_NB = time.time()

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode

sh("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless")
sh("update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java")
sh("java -version")
sh(f'{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes pycocoevalcap sacrebleu bert_score 2>&1 | tail -3')
sh(f'{sys.executable} -c "import transformers, peft, torch; print(transformers.__version__, peft.__version__, torch.__version__, torch.cuda.device_count(), torch.cuda.get_device_name(0))"')
```

Dòng cuối phải in `2` ở vị trí số GPU (T4 ×2). Nếu in `1`: Session options → Accelerator → GPU T4 ×2.

**Ô 2 — đường dẫn, md5, hàm chạy song song**

```python
import os, glob, json, shutil, hashlib, subprocess, time
W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()

MD5 = {
    "ra_build.py": "30bda9a22b6da576b23350d7090f10a0", "ra_train.py": "61bb6aac00c8a4d460e770589812bc89",
    "ra_gen.py": "0d361deea9a3185115034e8be08efab2", "ra_score.py": "35435945ff99028a75d8a147914b95c",
    "ra_exemplars.py": "83328e340382e5d1b9b8852617955e82", "grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf",
    "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912", "train_tru_val.jsonl": "edbb231a58574acf6e1968a44d1fa6c6",
    "ex_test_k4.jsonl": "c9e097ca92fb7b9fabaa73a27ab04c73", "ex_val_k4.jsonl": "b733bda18f04c7013b5e67fda41f0e96",
    "pred_ck500_test.jsonl": "328847ac96fa3104f76cd997f4091bcd", "pred_ck500_vallon.jsonl": "d092faf6f862eec5db71110e6b5963e2",
}
SRC = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/ra_train.py", recursive=True)
       if os.path.exists(os.path.join(os.path.dirname(p), "train_tru_val.jsonl"))]
assert len(SRC) == 1, f"DỪNG: cần đúng một dataset ra-sft-script, thấy {SRC}"
SRC = SRC[0]
for f, h in MD5.items():
    assert md5(f"{SRC}/{f}") == h, f"DỪNG: {f} lệch md5 - tạo lại dataset từ _scripts/304/ra-sft-script/"
    if f.endswith(".py"):
        shutil.copy(f"{SRC}/{f}", f"{W}/{f}")

BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "p1_train_rows.jsonl" in f)
CK = sorted(os.path.dirname(p) for p in glob.glob("/kaggle/input/**/adapter_model.safetensors", recursive=True)
            if md5(p) == "491fa6677340393f1e4464c08a0cec98")
CK = [c for c in CK if not c.strip("/").endswith("ref")]
assert len(CK) == 1, "DỪNG: không thấy adapter ck500 (md5 491fa667...) - gắn dataset grpo-spice-ck500"
CK500 = CK[0]
MERGED = f"{W}/s1_merged"

def chay(jobs, test=False, nhip=120):
    """jobs = [(tên, lệnh, gpu)]; mỗi job một GPU, chạy song song, in dòng cuối log mỗi nhịp."""
    ps = []
    for i, (ten, cmd, gpu) in enumerate(jobs):
        if i:
            time.sleep(20 if test else 180)      # giảm đỉnh RAM lúc nạp mô hình
        f = open(f"{W}/{ten}.log", "w")
        env = {**os.environ, "CUDA_VISIBLE_DEVICES": str(gpu), "PYTHONUNBUFFERED": "1",
               "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1"}
        ps.append((ten, subprocess.Popen(cmd, cwd=W, stdout=f, stderr=subprocess.STDOUT, env=env), f))
    while any(p.poll() is None for _, p, _ in ps):
        time.sleep(30 if test else nhip)
        for ten, p, _ in ps:
            L = [l.strip() for l in open(f"{W}/{ten}.log", errors="ignore") if l.strip()]
            print(f" {(time.time() - T_NB) / 3600:5.2f} h · {ten} · {'xong' if p.poll() is not None else 'chạy'} · "
                  f"{L[-1][:110] if L else '..'}", flush=True)
    for ten, p, f in ps:
        f.close()
        print(f"--- {ten} · mã thoát {p.returncode} ---\n" +
              "".join(open(f"{W}/{ten}.log", errors="ignore").readlines()[-8:]), flush=True)
    return {ten: p.returncode for ten, p, _ in ps}

def hoa():
    r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED],
                       cwd=W, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:]); assert r.returncode == 0, "DỪNG: hoà S1 lỗi"

print("SRC   ", SRC); print("BUNDLE", BUNDLE); print("CK500 ", CK500, flush=True)
```

Phải thấy ba đường dẫn, không có chữ `DỪNG`.

## 5. Notebook T — train hai nhánh (+ val tuỳ chọn)

New Notebook → Session options: GPU T4 ×2, Internet On. Add Input: `fgrb-p1-bundle` · `grpo-spice-ck500` · `ra-sft-script`. (Không cần thesis-score.) Dán ô 1, ô 2 ở §4, rồi các ô dưới.

**Ô 3 — hoà S1, dựng dữ liệu**

```python
hoa()
DATA = f"{W}/ra_data"
r = subprocess.run(["python", "ra_build.py", "--bundle", BUNDLE, "--kho", f"{SRC}/train_tru_val.jsonl",
                    "--out", DATA, "--chi-train"], cwd=W, capture_output=True, text=True)
print((r.stdout + r.stderr)[-4000:]); assert r.returncode == 0, "DỪNG: dựng dữ liệu lỗi"
S = json.load(open(f"{DATA}/build_stats.json"))
assert S["kho_buoc"] == 62880, f"DỪNG: kho {S['kho_buoc']} bước ≠ 62.880 - p1_val_rows khác bản đã đo"
assert S["train_rows"] >= 3000, f"DỪNG: chỉ {S['train_rows']} hàng train"
assert 80 <= S["train_co_khoi_pct"] <= 91, S
N_STEP = -(-S["train_rows"] // 16)
print(f"✅ dữ liệu: {S['train_rows']} hàng · {N_STEP} bước tối ưu mỗi nhánh", flush=True)
```

Kỳ vọng: `[kho] 62880 bước · 12542 tác vụ · [train] ~3.9xx hàng · có khối ~85% · khối chứa đích ~12–20% · một ví dụ câu nhắc có khối "Ví dụ bước tương tự..."`. Ô này ~10 phút.

**Ô 4 — train ra (GPU 0) và cont (GPU 1) song song**

```python
TEST = True          # chạy thử 2 bước mỗi nhánh; đổi False trước khi commit
LR = 2e-5
tag = "thu_" if TEST else ""
jobs = []
for g, arm in enumerate(("ra", "cont")):
    cmd = ["python", "ra_train.py", "--merged", MERGED, "--ckpt", CK500, "--data", f"{DATA}/train_{arm}.jsonl",
           "--out", f"{W}/{tag}{arm}_sft", "--lr", str(LR), "--max-hours", "8"]
    if TEST:
        cmd += ["--n", "32"]
    jobs.append((f"{tag}train_{arm}", cmd, g))
rc = chay(jobs, test=TEST)
assert all(v == 0 for v in rc.values()), f"DỪNG: train lỗi {rc} - gửi hai log về"
for arm in ("ra", "cont"):
    assert os.path.exists(f"{W}/{tag}{arm}_sft/final/adapter_model.safetensors"), f"DỪNG: thiếu {tag}{arm}_sft/final"
    L = open(f"{W}/{tag}train_{arm}.log").read()
    print(arm, [l for l in L.splitlines() if "[kiểm nhãn]" in l or "[adapter]" in l][:2], flush=True)
if TEST:
    import re
    sb = max(float(m) for arm in ("ra", "cont")
             for m in re.findall(r"(\d+.) s/bước", open(f"{W}/thu_train_{arm}.log").read()))
    print(f"ƯỚC LƯỢNG lượt thật: {sb:.0f} s/bước × {N_STEP} bước ≈ {sb * N_STEP / 3600:.1f} h (hai nhánh song song)")
```

Chạy thử phải thấy, ở cả hai log:

- `[adapter] ... tham số học 14,966,784 (ck500 14,966,784);`
- `[kiểm nhãn] mẫu đầu: ... tính loss N token: '<câu đích><|im_end|>'` — phần trong nháy phải đúng câu đích;
- `bước 1/2 · loss ...` và `bước 2/2 · loss ...` với loss hữu hạn (kỳ vọng khoảng 0,2–1,0 vì ck500 đã học các câu này);
- dòng `ƯỚC LƯỢNG`.

Nếu ước lượng > 7 h: đổi `"--max-hours", "8"` giữ nguyên, script tự lưu `last/` và dừng ở 8 h; chạy lại notebook với Output cũ làm input sẽ nối tiếp (xem §8).

Ổn thì: sửa `TEST = False` → Stop session → Save Version → Save & Run All.

**Ô 5 — val tuỳ chọn (~1 h): xem chiều trước khi tốn notebook G**

```python
VAL = True
if VAL and not TEST:
    vb = ["--merged", MERGED, "--recs", f"{BUNDLE}/p1_val_rows.jsonl", "--ocr", f"{BUNDLE}/ocr.jsonl",
          "--images", f"{BUNDLE}/images", "--expect", "1002"]
    rc = chay([("val_ra_k4", ["python", "ra_gen.py", *vb, "--ckpt", f"{W}/ra_sft/final",
                              "--ra", f"{SRC}/ex_val_k4.jsonl", "--out", f"{W}/pred_val_ra_k4.jsonl"], 0),
               ("val_cont", ["python", "ra_gen.py", *vb, "--ckpt", f"{W}/cont_sft/final",
                             "--out", f"{W}/pred_val_cont.jsonl"], 1)])
    assert all(v == 0 for v in rc.values()), rc
    r = subprocess.run(["python", "ra_score.py", "--recs", f"{BUNDLE}/p1_val_rows.jsonl",
                        "--pred", f"ck500={SRC}/pred_ck500_vallon.jsonl",
                        "--pred", f"ra_k4={W}/pred_val_ra_k4.jsonl", "--pred", f"cont={W}/pred_val_cont.jsonl",
                        "--ra", f"ra_k4={SRC}/ex_val_k4.jsonl", "--no-bert", "--no-spice",
                        "--out", f"{W}/diem_val_304.json"], cwd=W, capture_output=True, text=True)
    print(r.stdout[-4000:], r.stderr[-1500:])
```

Val chỉ in 5 thước (bỏ SPICE, BERTScore cho nhanh). Val là dữ liệu S1 đã thấy lúc SFT nên chỉ dùng để xem chiều và chỉnh LR (§6.3), không trích vào luận văn.

**Ô 6 — dọn**

```python
shutil.rmtree(MERGED, ignore_errors=True)
for p in glob.glob(f"{W}/thu_*"):
    shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else os.remove(p)
print("Output giữ:", sorted(os.listdir(W)))
```

Output cần có: `ra_sft/final/`, `cont_sft/final/`, `train_ra.log`, `train_cont.log`, `ra_data/build_stats.json` (+ `diem_val_304.json`, `pred_val_*.jsonl` nếu bật val).

## 6. Notebook G — sinh test ba cấu hình + chấm 7 thước

New Notebook → GPU T4 ×2, Internet On. Add Input: `thesis-score` · `fgrb-p1-bundle` · `grpo-spice-ck500` · `ra-sft-script` · Output của notebook T (Add Input → Your Work → Notebooks → chọn notebook T). Dán ô 1, ô 2 ở §4, rồi các ô dưới.

**Ô 3 — tìm adapter mới, test, hoà S1**

```python
def mot(ten):
    L = [os.path.dirname(p) for p in glob.glob(f"/kaggle/input/**/{ten}/final/adapter_model.safetensors", recursive=True)]
    assert len(L) == 1, f"DỪNG: cần đúng một {ten}/final, thấy {L}"
    return L[0]
RA_AD, CONT_AD = mot("ra_sft"), mot("cont_sft")

TA = None
for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True):
    root = os.path.dirname(t)
    if sum(1 for _ in open(t)) == 6958 and len(glob.glob(f"{root}/images/*.png")) >= 4463 and os.path.exists(f"{root}/ocr.jsonl"):
        TA = root
assert TA, "DỪNG: không thấy test_ac đủ 6.958 dòng + 4.463 ảnh"
assert md5(f"{TA}/test.jsonl") == "da58299ee551a926a21cbecb5232bf78", "DỪNG: test.jsonl lệch"
print("RA_AD ", RA_AD); print("CONT_AD", CONT_AD); print("TA    ", TA, flush=True)
hoa()
```

**Ô 4 — sinh: GPU 0 = ra_k4 rồi nửa đầu cont · GPU 1 = ra_rong rồi nửa sau cont**

```python
TEST = True          # chạy thử 6 bước mỗi job + kiểm bộ chấm; đổi False trước khi commit
tag = "_thu" if TEST else ""
n = ["--n", "6"] if TEST else []
B = ["python", "ra_gen.py", "--merged", MERGED, "--recs", f"{TA}/test.jsonl", "--ocr", f"{TA}/ocr.jsonl",
     "--images", f"{TA}/images", "--expect", "4463", *n]
rc = chay([("gen_ra_k4"+tag, [*B, "--ckpt", RA_AD, "--ra", f"{SRC}/ex_test_k4.jsonl", "--out", f"{W}/pred_ra_k4{tag}.jsonl"], 0),
           ("gen_ra_rong"+tag, [*B, "--ckpt", RA_AD, "--out", f"{W}/pred_ra_rong{tag}.jsonl"], 1)], test=TEST)
rc.update(chay([("gen_cont_a"+tag, [*B, "--ckpt", CONT_AD, "--shard", "0/2", "--out", f"{W}/pred_cont_a{tag}.jsonl"], 0),
                ("gen_cont_b"+tag, [*B, "--ckpt", CONT_AD, "--shard", "1/2", "--out", f"{W}/pred_cont_b{tag}.jsonl"], 1)],
               test=TEST))
assert all(v == 0 for v in rc.values()), f"DỪNG: sinh lỗi {rc}"
with open(f"{W}/pred_cont{tag}.jsonl", "w") as f:
    for p in (f"{W}/pred_cont_a{tag}.jsonl", f"{W}/pred_cont_b{tag}.jsonl"):
        f.write(open(p).read())
for t in ("ra_k4", "ra_rong", "cont"):
    print(t, sum(1 for _ in open(f"{W}/pred_{t}{tag}.jsonl")), "câu", flush=True)
if TEST:
    for t in ("ra_k4", "ra_rong", "cont"):
        print(t, [json.loads(l)["pred"] for l in open(f"{W}/pred_{t}_thu.jsonl")][:3])
```

Chạy thử phải thấy: log `gen_ra_k4_thu` có `[ví dụ] ... 4463 bước · thiếu 0` và câu nhắc đầu có khối; log `gen_ra_rong_thu` có `KHÔNG có khối`; ba dòng đếm `6 · 6 · 6 câu`; câu sinh ra là câu tiếng Anh bình thường.

**Ô 5 — chấm**

```python
cmd = ["python", "ra_score.py", "--recs", f"{TA}/test.jsonl", "--pred", f"ck500={SRC}/pred_ck500_test.jsonl", "--check"]
if TEST:
    cmd += ["--out", f"{W}/diem_thu.json"]        # chỉ kiểm bộ chấm tái lập 7 số của ck500 (~15 phút)
else:
    cmd += ["--pred", f"ra_k4={W}/pred_ra_k4.jsonl", "--pred", f"ra_rong={W}/pred_ra_rong.jsonl",
            "--pred", f"cont={W}/pred_cont.jsonl", "--ra", f"ra_k4={SRC}/ex_test_k4.jsonl",
            "--out", f"{W}/diem_test_304.json"]
r = subprocess.run(cmd, cwd=W, capture_output=True, text=True)
print(r.stdout[-6000:], r.stderr[-2000:])
```

Chạy thử phải thấy `[tự kiểm] ck500 - số đã công bố: {...} → KHỚP`. Nếu LỆCH ở METEOR/SPICE (khác bản Java) mà các thước khác khớp: vẫn đi tiếp, ghi lại độ lệch; Δ giữa các nhánh vẫn so được vì cùng một bộ chấm.

Ổn thì: `TEST = False` ở Ô 4 → Stop session → Save Version → Save & Run All. Khoảng 7 h.

**Ô 6 — dọn**

```python
shutil.rmtree(MERGED, ignore_errors=True)
print(sorted(os.listdir(W)))
```

Tải về: `diem_test_304.json`, `pred_ra_k4.jsonl`, `pred_ra_rong.jsonl`, `pred_cont.jsonl`, mọi `gen_*.log`, và toàn bộ output in ra của Ô 5 (bảng + các dòng `[kết luận]`). Gửi cho chat đọc file này. Nên lưu về `/Users/P836901/Documents/Self-learning/thesis/_scripts/304/ket_qua/` (ngoài clone).

## 7. Đọc kết quả

`ra_score.py` in sẵn bảng `| thước | ck500 | ra_k4 (Δ) | ra_rong (Δ) | cont (Δ) |` và ba dòng `[kết luận]`.

| câu hỏi | đọc dòng | kết luận được viết |
|---|---|---|
| chính | `[kết luận] ra_k4: cao hơn ck500 ở X/7` | `X ≥ 4` ⇒ đạt: “RA-SFT cao hơn ck500 ở X/7 thước chữ” |
| kho rỗng | cột `ra_rong (Δ)` | mọi Δ ≥ -0,5 (BLEU/METEOR/ROUGE-L/SPICE/chrF/BERTScore) và CIDEr-D ≥ -5 ⇒ “khi không có câu mẫu, mô hình giữ mức ck500”; `ra_rong ≥ 4/7` cao hơn thì nói mạnh hơn: “không kém ck500” |
| quy công | so cột `ra_k4` với `cont` | `ra_k4 > cont` ở ≥ 4/7 ⇒ lợi chủ yếu do truy hồi; ngược lại ⇒ phải khai “phần lớn do SFT thêm” (tiền lệ CE2, report 155) |
| chẩn đoán | `[chép] ra_k4: chép nguyên văn một ví dụ ở _% bước · trong số đó đúng câu chuẩn _%` | tỉ lệ chép > 40% với độ đúng < 15% ⇒ mô hình chép mù, cần tăng tỉ lệ khối rỗng/ngẫu nhiên |

Ngưỡng “kho rỗng” là một quy ước nhẹ đặt trước, không phải kiểm định thống kê. Không có khoảng tin cậy (theo yêu cầu).

### 7.1 Nếu `ra_k4` chưa đạt 4/7

| tình huống | thử tiếp (được tự do, chọn trên val) |
|---|---|
| cả `ra_k4` lẫn `cont` đều thấp hơn ck500 rõ | SFT đang xoá phần lợi GRPO ⇒ hạ LR xuống `1e-5`, chạy lại notebook T |
| `ra_k4 ≈ ck500`, chép ít (<5%) | mô hình chưa dùng câu mẫu ⇒ tăng LR lên `5e-5` |
| `ra_k4` tốt ở CIDEr/BLEU nhưng tụt SPICE | thường do chép câu đúng kiểu viết nhưng sai phần tử ⇒ xem các câu chép sai trong `pred_ra_k4.jsonl` |

Mỗi lần đổi chỉ chạy lại notebook T (có Ô 5 val), xem val, rồi mới chạy notebook G. Ghi lại đã thử những LR nào.

## 8. Sự cố thường gặp

| hiện tượng | làm gì |
|---|---|
| `DỪNG: ... lệch md5` | tạo lại dataset `ra-sft-script` từ đúng thư mục `_scripts/304/ra-sft-script/` |
| `[kiểm nhãn]` assert chết | gửi nguyên dòng log về — chat sau sửa `ra_train.py` |
| OOM khi hai nhánh chạy song song | trong Ô 4 notebook T, chạy từng nhánh: `rc = chay([jobs[0]]); rc.update(chay([jobs[1]]))` (gấp đôi thời gian) |
| train bị dừng ở `[dừng giờ]` | Output đã có `ra_sft/last/`, `cont_sft/last/`. Notebook mới, gắn Output đó làm input, thêm ô chép `shutil.copytree(<input>/ra_sft, f"{W}/ra_sft")` (và `cont_sft`) trước Ô 4, chạy lại ⇒ script tự nối tiếp từ `last/` |
| sinh bị ngắt | `ra_gen.py` nối tiếp được: chép `pred_*.jsonl` cũ vào W rồi chạy lại đúng lệnh |
| SPICE/METEOR lỗi Java | kiểm Ô 1 in `openjdk version "1.8..."`; chạy lại Ô 5 với `--no-spice` để có 6 thước trước |

## 9. Việc người dùng tự làm

1. Tạo dataset `ra-sft-script` (§3.1).
2. Notebook T: chạy thử (`TEST = True`) → gửi output nếu có `DỪNG` → `TEST = False` → Save & Run All.
3. Notebook G: gắn Output của T, chạy thử → `TEST = False` → Save & Run All.
4. Tải output (§6 Ô 6) về `_scripts/304/ket_qua/`, gửi output Ô 5 cho chat đọc file này.
5. Không cần commit gì cho lượt này; mọi tệp nằm ngoài clone. Nếu muốn đưa script vào repo (tuỳ chọn), tự chạy: `cp _scripts/304/ra-sft-script/ra_*.py thesis-master/harness/` rồi `cd thesis-master && git add harness/ra_*.py && git commit -m "304: RA-SFT tu ck500" && git push` — các tệp này nằm trong repo sẽ mất nếu xoá clone mà chưa commit.

## 10. Việc tôi KHÔNG tự làm

- Không chạy git. Không ghi vào `thesis-master/`. Không tải gì từ Hugging Face (notebook Kaggle tự tải Qwen và roberta-large như các lượt trước).
- Không chạy được train/sinh/chấm đầy đủ trên máy nhà (không GPU, không torch, không Java) — chỉ chạy được phần dựng dữ liệu, truy hồi, dựng câu nhắc và chrF (§2).
- Không chọn hộ LR cuối cùng: `2e-5` là điểm khởi đầu, người dùng được chỉnh trên val.
- Không chấm exec (UGround, ~4,9 h mỗi nhánh). Tiêu chí lượt này là thước chữ. Nếu muốn có exec cho `ra_k4`, dùng lại runbook chấm của report 303 với `--preds pred_ra_k4.jsonl`.

## 11. Tự sửa / lệch so với các lượt trước

- So với thiết kế 296-P (debate P): 296-P đề xuất RA-SFT tiếp từ S1 rồi chạy lại RA-GRPO đúng công thức ck500 (~16 h A100). Lượt này đi tắt: SFT có truy hồi tiếp từ adapter ck500, không GRPO lại. Lý do: rẻ hơn nhiều, không lặp một vòng GRPO (mọi nhánh GRPO thêm sau ck500 đều làm thước chữ giảm), và phép so với ck500 sạch hơn. Đổi lại, rủi ro là SFT làm mất một phần lợi GRPO — nhánh `cont` đo đúng rủi ro đó.
- Dữ liệu train: 296-P định 8.000 hàng lấy từ toàn bộ `train_tru_val`; lượt này dùng ~3.960 hàng `p1_train_rows` vì chỉ phần này có ảnh sẵn trên Kaggle. Canvas “Chốt RA-SFT” của lượt trước ghi “khoảng 8.000 bước train” — số đúng cho runbook này là ~3.960 hàng ≈ 248 bước tối ưu.
- lr: 296-P dùng `5e-5` (tiếp từ S1). Lượt này `2e-5` vì xuất phát từ ck500 và muốn giữ phần lợi GRPO.
- “4 câu mẫu”: trong chat trước tôi mô tả “lấy 4 câu”. Chính xác là: lúc chạy cố định 4 câu; lúc train ngẫu nhiên 2–6 câu, 15% không có câu nào, 10% câu ngẫu nhiên.
- Ước lượng xác suất đạt ≥ 4/7 (~55–65%) ở lượt trước vẫn là ước lượng chủ quan, chưa có số mới nào đổi nó.

## Phụ lục A — mã nguồn nguyên văn

Tất cả đã có thành tệp trong `/Users/P836901/Documents/Self-learning/thesis/_scripts/304/ra-sft-script/`. `grpo_spice.py` và `build_branch_data.py` là bản y hệt `thesis-master/harness/` (md5 ở §3.1), không chép lại ở đây.

### A.1 `ra_exemplars.py` (y hệt `_scripts/296/ra_exemplars.py`)

```python
# -*- coding: utf-8 -*-
"""Truy hồi ví dụ quỹ đạo cho sinh câu hướng dẫn (RA-SFT · RA-GRPO · sinh val/test).

Đích dán đề xuất: thesis-master/harness/ra_exemplars.py (người dùng tự chép và commit).
Kho = bước train (train_tru_val.jsonl) đã loại mọi tác vụ val; truy vấn chỉ dùng mục tiêu + lịch sử (đầu vào).
Hai khoá, hợp lại rồi khử trùng câu:
  R1 mức bước (kiểu SmallCap): TF-IDF trên (mục tiêu + câu lịch sử cuối, tiền tố H_).
  R2 mức quỹ đạo (kiểu Synapse): TF-IDF trên mục tiêu → tác vụ gần nhất, căn bước theo câu-trước = câu lịch sử cuối.
Lúc dạy: bỏ chính tác vụ (leave-one-episode-out), c-sample-k + xáo thứ tự (RobustCap), k ngẫu nhiên 2..6,
15% bỏ khối, 10% ví dụ ngẫu nhiên, bỏ ví dụ trùng câu chuẩn với xác suất q để tỉ lệ khớp lúc dạy ≈ lúc chấm.
Lúc chấm: cố định, k=4, xếp theo số lần xuất hiện → độ phủ OCR → hạng.
"""
import math, re, random, heapq
from collections import Counter, defaultdict

PUNCT = {"''", '""', "``", "`", "-lrb-", "-rrb-", "-lcb-", "-rcb-", ".", "?", "!", ",", ":", "_", "--", "...", ";"}
TOK = re.compile(r"n't|'s|'re|'ve|'ll|'d|'m|[a-z0-9]+(?:[-./][a-z0-9]+)*|[^\sa-z0-9]")
FUNC = set("click tap select open press choose go type enter on the a an at of to in for and or from with by is be as "
           "into it its this that then next now please screen top bottom left right corner side middle center centre "
           "icon button option options tab bar field text page menu above below near beside under up down first "
           "second third last".split())
HEADER = "Ví dụ bước tương tự từ tác vụ khác (có thể không khớp màn này):"
LAST = "Viết câu hướng dẫn cho bước tiếp theo."

def tok(s):
    s = (s or "").lower().replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'")
    s = re.sub(r"(\w)n't\b", r"\1 n't", s)
    return [t for t in TOK.findall(s) if t not in PUNCT and t != ""]

def _tfidf(docs):
    df = Counter(w for d in docs for w in set(d))
    idf = {w: math.log(len(docs) / c) for w, c in df.items()}
    inv = defaultdict(list)
    for i, d in enumerate(docs):
        v = {w: tf * idf[w] for w, tf in Counter(d).items()}
        n = math.sqrt(sum(x * x for x in v.values())) or 1.0
        for w, x in v.items():
            inv[w].append((i, x / n))
    return idf, inv

def _q(idx, q, k):
    idf, inv = idx
    v = {w: tf * idf.get(w, 0.0) for w, tf in Counter(q).items()}
    n = math.sqrt(sum(x * x for x in v.values())) or 1.0
    sc = defaultdict(float)
    for w, x in v.items():
        for i, y in inv.get(w, ()):
            sc[i] += x / n * y
    return heapq.nlargest(k, sc.items(), key=lambda t: t[1])

def _jacc(a, b):
    a, b = set(tok(a)), set(tok(b))
    return len(a & b) / max(1, len(a | b))

def _hlast(x):
    h = x.get("history") or []
    return h[-1] if h else "<start>"

class Kho:
    def __init__(self, recs, loai_ep=()):
        bo = set(loai_ep)
        self.tr = [t for t in recs if t["episode_id"] not in bo and (t.get("target_instruction") or "").strip()]
        self.idx1 = _tfidf([self._k1(t) for t in self.tr])
        self.eps = defaultdict(dict)
        for t in self.tr:
            self.eps[t["episode_id"]][t["step_id"]] = t
        self.eid = sorted(self.eps)
        self.idx2 = _tfidf([tok(next(iter(self.eps[e].values()))["goal"]) for e in self.eid])
        self.click = [i for i, t in enumerate(self.tr) if (t.get("action") or {}).get("action_type") == "click"]

    @staticmethod
    def _k1(x):
        return tok(x["goal"]) + ["H_" + w for w in tok(_hlast(x))]

    def _e(self, t):
        return dict(sent=t["target_instruction"].strip(), goal=t["goal"], prev=_hlast(t))

    def r1(self, x, k, own):
        out = []
        for i, _ in _q(self.idx1, self._k1(x), 4 * k + 12):
            if self.tr[i]["episode_id"] != own:
                out.append(self._e(self.tr[i]))
                if len(out) == k:
                    break
        return out

    def r2(self, x, m, own):
        h, out = x.get("history") or [], []
        for i, _ in _q(self.idx2, tok(x["goal"]), m + 3):
            if self.eid[i] == own:
                continue
            st = self.eps[self.eid[i]]
            if not h:
                j = min(st)
            else:
                c = [(_jacc(st[s - 1]["target_instruction"], h[-1]), -abs(s - len(h)), s) for s in st if s - 1 in st]
                if not c:
                    continue
                j = max(c)[2]
            out.append(self._e(st[j]))
            if len(out) == m:
                break
        return out

    def pool(self, x, own=None, n1=8, n2=8):
        """Hợp R1∪R2, khử trùng theo câu đã token hoá; cnt = số lần câu xuất hiện trong hai danh sách thô."""
        seen, out = {}, []
        for r, e in enumerate(self.r1(x, n1, own) + self.r2(x, n2, own)):
            key = " ".join(tok(e["sent"]))
            if key in seen:
                seen[key]["cnt"] += 1
                continue
            seen[key] = dict(e, cnt=1, rank=r % max(n1, n2))
            out.append(seen[key])
        return out

    def cho_test(self, x, k=4, ocr_tokens=None, own=None):
        """Cố định (không ngẫu nhiên). own = tác vụ của chính câu nhắc khi dùng cho câu nhắc TRAIN (GRPO)."""
        P = self.pool(x, own, 4, 4)
        def phu(e):
            c = [w for w in tok(e["sent"]) if w not in FUNC and len(w) > 1]
            return float(bool(c) and ocr_tokens is not None and all(w in ocr_tokens for w in c))
        return sorted(P, key=lambda e: (-e["cnt"], -phu(e), e["rank"]))[:k]

    def cho_train(self, x, gold, own, rng, q_trung=0.0, kmin=2, kmax=6, N=12, p_rong=0.15, p_ngau=0.10):
        u = rng.random()
        if u < p_rong:
            return None
        k = rng.randint(kmin, kmax)
        if u < p_rong + p_ngau:
            cand = [self.tr[i] for i in rng.sample(self.click, 4 * k) if self.tr[i]["episode_id"] != own]
            return [self._e(t) for t in cand[:k]]
        P = self.pool(x, own)[:N]
        g = tok(gold)
        if q_trung and any(tok(e["sent"]) == g for e in P) and rng.random() < q_trung:
            P = [e for e in P if tok(e["sent"]) != g]
        if not P:
            return None
        out = [P[0]] + rng.sample(P[1:], min(k - 1, len(P) - 1))
        rng.shuffle(out)
        return out

def khoi(exs, goal_words=12):
    if not exs:
        return ""
    L = [HEADER]
    for i, e in enumerate(exs, 1):
        prev = "(bước đầu)" if e["prev"] == "<start>" else e["prev"].strip()
        L.append(f"{i}. Mục tiêu: {' '.join(e['goal'].split()[:goal_words])} | Bước trước: {prev} | "
                 f"Bước kế: {e['sent']}")
    return "\n".join(L)

def chen(body, exs):
    """Chèn khối ngay trước dòng cuối của prompt_body; phần trước giữ nguyên từng byte như câu nhắc của S1."""
    b = khoi(exs)
    if not b:
        return body
    assert body.endswith(LAST), "prompt_body đổi dòng cuối - sửa LAST"
    return body[:-len(LAST)] + b + "\n" + LAST
```

### A.2 `ra_build.py`

```python
# -*- coding: utf-8 -*-
"""304 — dựng dữ liệu RA-SFT từ ck500 (CPU, ~10–20 phút).

Ra trong --out:
  train_ra.jsonl    : câu nhắc S1 + khối ví dụ truy hồi (cho_train: bỏ chính tác vụ, k 2..6, 15% rỗng, 10% ngẫu nhiên)
  train_cont.jsonl  : CÙNG hàng, CÙNG thứ tự, CÙNG đích, câu nhắc S1 không khối (đối chứng "SFT thêm")
  ex_test_k4.jsonl  : 4 ví dụ cố định (cho_test) cho 4.463 bước click của test — chỉ đọc mục tiêu, lịch sử, OCR
  ex_val_k4.jsonl   : như trên cho các bước click của p1_val_rows (val lớn)
  build_stats.json

Kho truy hồi = train_tru_val.jsonl bỏ mọi tác vụ của p1_val_rows. Tác vụ test chung kho phải = 0.

  python ra_build.py --bundle B --kho train_tru_val.jsonl --test-recs T/test.jsonl --test-ocr T/ocr.jsonl --out O
  python ra_build.py ... --n-train 50          # chạy thử
"""
import os, sys, json, random, argparse, collections, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ra_exemplars as RA
from build_branch_data import prompt_body

TAPT = ("click", "long_press")


def doc(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")]


def la_cham(r):
    a = r.get("action") or {}
    return a.get("action_type") in TAPT and "x" in a


def ocr_toks(o):
    return {w for it in (o or {"items": []})["items"][:24] for w in RA.tok(it.get("text", ""))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--kho", required=True)
    ap.add_argument("--test-recs", default=None, help="bắt buộc khi không có --chi-train")
    ap.add_argument("--test-ocr", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=2026100901)
    ap.add_argument("--n-train", type=int, default=0, help="0 = mọi hàng p1_train_rows")
    ap.add_argument("--chi-train", action="store_true", help="bỏ qua xuất ex_test_k4/ex_val_k4 (đã có sẵn trong gói)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()

    tr = doc(os.path.join(a.bundle, "p1_train_rows.jsonl"))
    va = doc(os.path.join(a.bundle, "p1_val_rows.jsonl"))
    assert a.chi_train or (a.test_recs and a.test_ocr), "⛔ cần --test-recs và --test-ocr, hoặc --chi-train"
    te = doc(a.test_recs) if a.test_recs else []
    assert not te or len(te) == 6958, f"⛔ test.jsonl có {len(te)} dòng"
    vep = {r["episode_id"] for r in va}
    ocr = {o["image"]: o for o in doc(os.path.join(a.bundle, "ocr.jsonl"))}
    tocr = {o["image"]: o for o in doc(a.test_ocr)} if a.test_ocr else {}

    kho = RA.Kho(doc(a.kho), loai_ep=vep)
    tep = {r["episode_id"] for r in te}
    chung_test = len(tep & set(kho.eid)) if te else 0
    print(f"[kho] {len(kho.tr)} bước · {len(kho.eid)} tác vụ · bỏ {len(vep)} tác vụ val · "
          f"{chung_test} tác vụ test chung kho", flush=True)
    assert chung_test == 0, "⛔ kho chứa tác vụ test"
    assert len(kho.tr) > 60000, "⛔ kho quá nhỏ — sai tệp train_tru_val?"

    bo = collections.Counter()
    rows = []
    for r in tr:
        gold = (r.get("target_instruction") or "").strip()
        if not gold:
            bo["rong"] += 1
            continue
        if r["episode_id"] in vep:
            bo["trung_val"] += 1
            continue
        if not os.path.exists(os.path.join(a.bundle, r["image"])):
            bo["thieu_anh"] += 1
            continue
        if r["image"] not in ocr:
            bo["thieu_ocr"] += 1
            continue
        rows.append(r)
    assert bo["trung_val"] == 0, "⛔ p1_train_rows chạm tác vụ val"
    rng = random.Random(a.seed)
    rng.shuffle(rows)
    if a.n_train:
        rows = rows[:a.n_train]
    print(f"[train] {len(rows)} hàng · bỏ {dict(bo)} · loại thao tác "
          f"{dict(collections.Counter((r.get('action') or {}).get('action_type') for r in rows))}", flush=True)

    st = collections.Counter()
    with open(os.path.join(a.out, "train_ra.jsonl"), "w", encoding="utf-8") as fr, \
         open(os.path.join(a.out, "train_cont.jsonl"), "w", encoding="utf-8") as fc:
        for i, r in enumerate(rows):
            gold = r["target_instruction"].strip()
            body = prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
            ex = kho.cho_train(r, gold, r["episode_id"], rng)
            body_ra = RA.chen(body, ex) if ex else body
            assert body_ra.startswith(body[:-len(RA.LAST)]), "⛔ phần đầu câu nhắc RA khác câu nhắc S1"
            st["n"] += 1
            st["co_khoi"] += bool(ex)
            st["khoi_chua_dich"] += bool(ex) and any(RA.tok(e["sent"]) == RA.tok(gold) for e in ex)
            st["so_vi_du"] += len(ex) if ex else 0
            key = f"{r['episode_id']}_{r['step_id']}"
            img = os.path.join(a.bundle, r["image"])
            fr.write(json.dumps(dict(key=key, image=img, body=body_ra, gold=gold), ensure_ascii=False) + "\n")
            fc.write(json.dumps(dict(key=key, image=img, body=body, gold=gold), ensure_ascii=False) + "\n")
            if (i + 1) % 1000 == 0:
                print(f"  train {i+1}/{len(rows)} · {(time.time()-t0)/60:.1f} phút", flush=True)

    def xuat(recs, oc, path, tinh_dich):
        hit, n = 0, 0
        with open(path, "w", encoding="utf-8") as f:
            for r in recs:
                if not la_cham(r):
                    continue
                x = dict(goal=r["goal"], history=r.get("history") or [])
                ex = [dict(sent=e["sent"], goal=e["goal"], prev=e["prev"])
                      for e in kho.cho_test(x, 4, ocr_toks(oc.get(r["image"])))]
                n += 1
                if tinh_dich:
                    g = (r.get("target_instruction") or r.get("gold_instruction") or "").strip()
                    hit += any(RA.tok(e["sent"]) == RA.tok(g) for e in ex)
                f.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "exemplars": ex},
                                   ensure_ascii=False) + "\n")
        return n, hit

    nt = nv = hv = 0
    if not a.chi_train:
        nt, _ = xuat(te, tocr, os.path.join(a.out, "ex_test_k4.jsonl"), tinh_dich=False)
        assert nt == 4463, f"⛔ test có {nt} bước click"
        nv, hv = xuat(va, ocr, os.path.join(a.out, "ex_val_k4.jsonl"), tinh_dich=True)

    S = dict(
        train_rows=st["n"],
        train_co_khoi_pct=round(100 * st["co_khoi"] / max(st["n"], 1), 1),
        train_khoi_chua_dich_pct=round(100 * st["khoi_chua_dich"] / max(st["co_khoi"], 1), 1),
        train_so_vi_du_tb=round(st["so_vi_du"] / max(st["co_khoi"], 1), 2),
        test_click=nt, val_click=nv, val_khoi_chua_dich_pct=round(100 * hv / max(nv, 1), 1),
        kho_buoc=len(kho.tr), bo=dict(bo), seed=a.seed, phut=round((time.time() - t0) / 60, 1),
    )
    json.dump(S, open(os.path.join(a.out, "build_stats.json"), "w"), ensure_ascii=False, indent=1)
    print("[xong]", json.dumps(S, ensure_ascii=False), flush=True)
    vd = next(json.loads(l) for l in open(os.path.join(a.out, "train_ra.jsonl"), encoding="utf-8")
              if RA.HEADER in json.loads(l)["body"])
    print("--- ví dụ câu nhắc RA ---\n" + vd["body"] + "\n--- đích: " + vd["gold"], flush=True)


if __name__ == "__main__":
    main()
```

### A.3 `ra_train.py`

```python
# -*- coding: utf-8 -*-
"""304 — SFT ngắn TIẾP TỪ adapter ck500 (một nhánh mỗi lần gọi).

Nền: S1 đã hoà (`s1_merged`) nạp 4-bit như lúc GRPO train ck500 (grpo_spice.nap, q4).
Adapter học: CHÍNH adapter ck500 (is_trainable) → cùng cỡ LoRA, cùng chỗ gắn; lúc sinh gắn adapter mới lên
`s1_merged` fp16 đúng như đã sinh ck500 (gen_test_grpo / ra_gen).
Đích = câu chuẩn; chỉ tính loss trên token của câu đích + <|im_end|>. Tháp thị giác không học.
Câu nhắc lúc dạy dựng CÙNG cách với lúc sinh: SYS + [ảnh, "\\n" + body].

  python ra_train.py --merged M --ckpt CK500 --data train_ra.jsonl --out O/ra_sft
  python ra_train.py ... --n 32 --out O/thu_ra      # chạy thử: 2 bước tối ưu
Nối tiếp: chạy lại đúng lệnh; script tự nạp O/last nếu có.
"""
import os, sys, json, math, time, argparse

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

N_CK500 = 14966784


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--merged", required=True)
    ap.add_argument("--ckpt", required=True, help="thư mục adapter ck500")
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--accum", type=int, default=16)
    ap.add_argument("--epochs", type=float, default=1.0)
    ap.add_argument("--warmup", type=int, default=10)
    ap.add_argument("--n", type=int, default=0, help="chỉ lấy N hàng đầu (chạy thử)")
    ap.add_argument("--save-every", type=int, default=25)
    ap.add_argument("--max-hours", type=float, default=10.5)
    ap.add_argument("--seed", type=int, default=101)
    a = ap.parse_args()
    a.q4 = True

    import torch
    from PIL import Image
    from peft import PeftModel, set_peft_model_state_dict
    from safetensors.torch import load_file
    import grpo_spice as GS
    from build_branch_data import SYS

    torch.manual_seed(a.seed)
    rows = [json.loads(l) for l in open(a.data, encoding="utf-8")]
    if a.n:
        rows = rows[:a.n]
    n_step = math.ceil(len(rows) * a.epochs / a.accum)
    order = [i % len(rows) for i in range(n_step * a.accum)]
    print(f"[dữ liệu] {a.data} · {len(rows)} hàng · {n_step} bước tối ưu × lô {a.accum} · lr {a.lr}", flush=True)

    proc, model, dt = GS.nap(a)
    model.config.use_cache = False
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.enable_input_require_grads()
    model = PeftModel.from_pretrained(model, a.ckpt, is_trainable=True)

    params, ntr = [], 0
    for n, p in model.named_parameters():
        if p.requires_grad:
            if "visual" in n:
                raise SystemExit(f"⛔ tháp thị giác đang học: {n}")
            if p.dtype != torch.float32:
                p.data = p.data.float()
            params.append(p)
            ntr += p.numel()
    print(f"[adapter] {a.ckpt} · tham số học {ntr:,} (ck500 {N_CK500:,}) · dtype tính {dt}", flush=True)
    assert ntr == N_CK500, "⛔ adapter không cùng cỡ ck500 — sai thư mục --ckpt?"

    opt = torch.optim.AdamW(params, lr=a.lr, betas=(0.9, 0.999), weight_decay=0.0)

    def lam(s):
        if s < a.warmup:
            return (s + 1) / a.warmup
        return 0.5 * (1 + math.cos(math.pi * (s - a.warmup) / max(1, n_step - a.warmup)))

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lam)
    use_scaler = dt == torch.float16
    scaler = torch.amp.GradScaler("cuda", enabled=use_scaler)

    os.makedirs(a.out, exist_ok=True)
    last = os.path.join(a.out, "last")
    step = 0
    if os.path.exists(os.path.join(last, "state.pt")):
        sd = load_file(os.path.join(last, "adapter_model.safetensors"))
        kq = set_peft_model_state_dict(model, sd, adapter_name="default")
        la = [k for k in getattr(kq, "unexpected_keys", []) if "lora" in k]
        assert not la, f"⛔ nạp last lỗi: {la[:3]}"
        S = torch.load(os.path.join(last, "state.pt"), map_location="cpu", weights_only=False)
        opt.load_state_dict(S["opt"])
        sched.load_state_dict(S["sched"])
        if use_scaler and S.get("scaler"):
            scaler.load_state_dict(S["scaler"])
        step = S["step"]
        print(f"[nối tiếp] từ bước {step}/{n_step}", flush=True)

    def luu(path):
        model.save_pretrained(path)
        torch.save(dict(opt=opt.state_dict(), sched=sched.state_dict(),
                        scaler=scaler.state_dict() if use_scaler else None, step=step,
                        lr=a.lr, data=a.data), os.path.join(path, "state.pt"))

    tok_end = proc.tokenizer("<|im_end|>", add_special_tokens=False).input_ids

    def mau(r):
        msg = [{"role": "system", "content": SYS},
               {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + r["body"]}]}]
        ptext = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(r["image"]).convert("RGB")
        inp = proc(text=[ptext + r["gold"] + "<|im_end|>"], images=[img], return_tensors="pt")
        tail = proc.tokenizer(r["gold"], add_special_tokens=False).input_ids + tok_end
        ids = inp["input_ids"][0].tolist()
        if ids[-len(tail):] != tail:
            pid = proc(text=[ptext], images=[img], return_tensors="pt")["input_ids"][0].tolist()
            assert ids[:len(pid)] == pid, "⛔ token câu nhắc đổi khi nối câu đích"
            n_lab = len(ids) - len(pid)
        else:
            n_lab = len(tail)
        lab = inp["input_ids"].clone()
        lab[:, : lab.shape[1] - n_lab] = -100
        inp = {k: v.to(model.device) for k, v in inp.items()}
        if "pixel_values" in inp:
            inp["pixel_values"] = inp["pixel_values"].to(dt)
        return inp, lab.to(model.device), n_lab

    inp0, lab0, n0 = mau(rows[0])
    nhan = proc.tokenizer.decode(inp0["input_ids"][0][-n0:])
    print(f"[kiểm nhãn] mẫu đầu: {inp0['input_ids'].shape[1]} token, tính loss {n0} token: {nhan!r} · đích {rows[0]['gold']!r}",
          flush=True)
    assert nhan.replace("<|im_end|>", "").strip() == rows[0]["gold"].strip(), "⛔ nhãn không đúng câu đích"
    del inp0, lab0

    model.train()
    t0 = time.time()
    torch.cuda.reset_peak_memory_stats()
    run_loss, run_n, b0 = 0.0, 0, step
    while step < n_step:
        if (time.time() - t0) / 3600 > a.max_hours:
            luu(last)
            print(f"[dừng giờ] lưu ở bước {step}/{n_step} — chạy lại đúng lệnh để nối tiếp", flush=True)
            return
        for j in range(a.accum):
            inp, lab, n_lab = mau(rows[order[step * a.accum + j]])
            with torch.autocast("cuda", dtype=dt):
                out = model(**inp, labels=lab)
            loss = out.loss
            if not torch.isfinite(loss):
                raise SystemExit(f"⛔ loss không hữu hạn ở bước {step}, mẫu {j}")
            scaler.scale(loss / a.accum).backward()
            run_loss += loss.item()
            run_n += 1
        scaler.unscale_(opt)
        gn = torch.nn.utils.clip_grad_norm_(params, 1.0).item()
        scaler.step(opt)
        scaler.update()
        opt.zero_grad(set_to_none=True)
        sched.step()
        step += 1
        if step % 5 == 0 or step == 1 or step == n_step:
            el = time.time() - t0
            print(f"  bước {step}/{n_step} · loss {run_loss / run_n:.4f} · |g| {gn:.3f} · "
                  f"lr {sched.get_last_lr()[0]:.2e} · {el / max(step - b0, 1):.1f} s/bước · "
                  f"VRAM {torch.cuda.max_memory_allocated() / 2**30:.1f} GiB", flush=True)
            run_loss, run_n = 0.0, 0
        if step % a.save_every == 0 and step < n_step:
            luu(last)

    fin = os.path.join(a.out, "final")
    luu(fin)
    luu(last)
    print(f"[xong] {step} bước · {(time.time() - t0) / 60:.1f} phút → {fin}", flush=True)


if __name__ == "__main__":
    main()
```

### A.4 `ra_gen.py`

```python
# -*- coding: utf-8 -*-
"""304 — sinh greedy cho bước click, cùng đường đã sinh ck500 (gen_test_grpo.py): `s1_merged` fp16 + adapter,
greedy, 96 token, câu nhắc SYS + [ảnh, "\\n" + prompt_body]. Thêm một tùy chọn: --ra chèn khối ví dụ truy hồi.

# test, khối k=4:      --recs T/test.jsonl --ocr T/ocr.jsonl --images T/images --expect 4463 --ra ex_test_k4.jsonl
# test, kho rỗng:      bỏ --ra (câu nhắc y hệt câu nhắc của ck500)
# val lớn:             --recs B/p1_val_rows.jsonl --ocr B/ocr.jsonl --images B/images --expect 1002 [--ra ex_val_k4.jsonl]
# chạy khô (CPU):      thêm --dry
Nối tiếp được: chạy lại đúng lệnh, bước đã có trong --out được bỏ qua.
"""
import os, sys, json, time, argparse

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_branch_data import prompt_body, SYS

TAPT = ("click", "long_press")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--merged", required=True)
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--recs", required=True)
    ap.add_argument("--ocr", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ra", default=None)
    ap.add_argument("--expect", type=int, default=0)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--shard", default="0/1", help="i/n: chỉ sinh các bước thứ i, i+n, … (chia đôi cho hai GPU)")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    a.q4 = False

    rows = [json.loads(l) for l in open(a.recs, encoding="utf-8")]
    rows = [r for r in rows if (r.get("action") or {}).get("action_type") in TAPT and "x" in r["action"]]
    if a.expect:
        assert len(rows) == a.expect, f"⛔ {len(rows)} bước click, cần {a.expect}"
    if a.n:
        rows = rows[:a.n]
    si, sn = map(int, a.shard.split("/"))
    rows = rows[si::sn]
    ocr = {o["image"]: o for o in map(json.loads, open(a.ocr, encoding="utf-8"))}
    thieu = [r["image"] for r in rows if not os.path.exists(os.path.join(a.images, os.path.basename(r["image"])))]
    print(f"[dữ liệu] {a.recs} · {len(rows)} bước click · thiếu OCR {sum(r['image'] not in ocr for r in rows)}"
          f" · thiếu ảnh {len(thieu)}", flush=True)
    assert a.dry or not thieu, f"⛔ thiếu ảnh, ví dụ {thieu[:3]}"

    EXM = None
    if a.ra:
        import ra_exemplars as RA
        EXM = {(d["episode_id"], d["step_id"]): d["exemplars"] for d in map(json.loads, open(a.ra, encoding="utf-8"))}
        miss = sum((r["episode_id"], r["step_id"]) not in EXM for r in rows)
        print(f"[ví dụ] {a.ra} · {len(EXM)} bước · thiếu {miss}", flush=True)
        assert not miss, "⛔ tệp ví dụ không phủ đủ bước"
    else:
        print("[ví dụ] KHÔNG có khối — câu nhắc y hệt câu nhắc của ck500", flush=True)

    def body_of(r):
        b = prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
        if EXM is not None:
            b = RA.chen(b, EXM[(r["episode_id"], r["step_id"])])
        return b

    def msg_of(r):
        return [{"role": "system", "content": SYS},
                {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body_of(r)}]}]

    print("[câu nhắc bước đầu]\n" + body_of(rows[0]), flush=True)
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

    fo = open(a.out, "a", encoding="utf-8")
    t0, moi = time.time(), 0
    for i, r in enumerate(rows):
        k = (r["episode_id"], r["step_id"])
        if k in done:
            continue
        text = proc.apply_chat_template(msg_of(r), tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.images, os.path.basename(r["image"]))).convert("RGB")
        inp = proc(text=[text], images=[img], return_tensors="pt").to(model.device)
        L = inp["input_ids"].shape[1]
        with torch.no_grad():
            g = model.generate(**inp, max_new_tokens=96, do_sample=False, use_cache=True,
                               temperature=None, top_p=None, top_k=None)
        s = proc.decode(g[0][L:], skip_special_tokens=True).strip()
        fo.write(json.dumps({"episode_id": k[0], "step_id": k[1], "pred": s}, ensure_ascii=False) + "\n")
        fo.flush()
        moi += 1
        if (i + 1) % 50 == 0:
            dt = time.time() - t0
            print(f"  {i+1}/{len(rows)} · {dt/60:.1f} phút · {dt/moi:.2f} s/bước · {s[:60]!r}", flush=True)
    fo.close()
    P = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(a.out, encoding="utf-8"))}
    print(f"[xong] {len(P)} câu · rỗng {sum(not v for v in P.values())}", flush=True)


if __name__ == "__main__":
    main()
```

### A.5 `ra_score.py`

```python
# -*- coding: utf-8 -*-
"""304 — chấm 7 thước chữ trên bước click, cùng công cụ đã ra số luận văn của ck500:
BLEU-4 · METEOR 1.5 · ROUGE-L · CIDEr-D · SPICE (pycocoevalcap, PTBTokenizer, mục kho; cần Java 8)
chrF (sacrebleu mặc định) · BERTScore F1 rescale (roberta-large, câu rỗng = 0, như text_metrics_them.tinh)
So mọi nhánh với nhánh gốc (mặc định ck500). --check: ck500 phải tái lập số test đã công bố (lệch ≤ 0,06).

  python ra_score.py --recs T/test.jsonl --pred ck500=pred_ck500_test.jsonl --pred ra_k4=pred_ra_k4.jsonl \
      --pred ra_rong=pred_ra_rong.jsonl --pred cont=pred_cont.jsonl --ra ra_k4=ex_test_k4.jsonl --check --out diem.json
  python ra_score.py ... --no-bert --no-spice    # nhanh, khi chỉ cần xem chiều
"""
import os, re, sys, json, argparse, warnings

warnings.filterwarnings("ignore")
TAPT = ("click", "long_press")
CK500_TEST = dict(bleu4=52.36, meteor=37.92, rougeL=68.36, cider_d=430.05, spice=45.79, chrf=62.87, bertscore=67.07)
TEN = dict(bleu4="BLEU-4", meteor="METEOR", rougeL="ROUGE-L", cider_d="CIDEr-D", spice="SPICE", chrf="chrF",
           bertscore="BERTScore")


def tokw(s):
    return re.findall(r"\w+", (s or "").lower())


def bert_scorer():
    from bert_score import BERTScorer
    import bert_score.utils as U
    goc = U.sent_encode

    def enc(tokenizer, sent):
        if sent.strip() == "":
            return tokenizer("", add_special_tokens=True)["input_ids"]
        return goc(tokenizer, sent)

    U.sent_encode = enc
    return BERTScorer(lang="en", rescale_with_baseline=True, batch_size=64)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recs", required=True)
    ap.add_argument("--pred", action="append", required=True, help="ten=duong_dan")
    ap.add_argument("--base", default="ck500")
    ap.add_argument("--ra", action="append", default=[], help="ten=tep_vi_du — đo tỉ lệ chép nguyên văn ví dụ")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--no-bert", action="store_true")
    ap.add_argument("--no-spice", action="store_true")
    ap.add_argument("--out", default="diem_304.json")
    a = ap.parse_args()

    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    from pycocoevalcap.bleu.bleu import Bleu
    from pycocoevalcap.meteor.meteor import Meteor
    from pycocoevalcap.rouge.rouge import Rouge
    from pycocoevalcap.cider.cider import Cider
    import sacrebleu

    recs = [json.loads(l) for l in open(a.recs, encoding="utf-8")]
    recs = [r for r in recs if (r.get("action") or {}).get("action_type") in TAPT and "x" in r["action"]]
    K = [(r["episode_id"], r["step_id"]) for r in recs]
    REF = [(r.get("gold_instruction") or r.get("target_instruction") or "").strip() for r in recs]
    P = {}
    for s in a.pred:
        ten, p = s.split("=", 1)
        d = {(x["episode_id"], x["step_id"]): (x.get("pred") or "").strip()
             for x in map(json.loads, open(p, encoding="utf-8"))}
        miss = [k for k in K if k not in d]
        assert not miss, f"⛔ {ten}: thiếu {len(miss)} bước, ví dụ {miss[:3]}"
        P[ten] = [d[k] for k in K]
    assert a.base in P, f"⛔ thiếu nhánh gốc {a.base}"
    print(f"[dữ liệu] {len(K)} bước click · nhánh {list(P)}", flush=True)

    tk = PTBTokenizer()
    G = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(REF)})
    SC = None if a.no_bert else bert_scorer()
    out = {}
    for ten, H in P.items():
        C = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(H)})
        b, _ = Bleu(4).compute_score(G, C, verbose=0)
        o = dict(bleu4=100 * b[3], meteor=100 * Meteor().compute_score(G, C)[0],
                 rougeL=100 * Rouge().compute_score(G, C)[0], cider_d=100 * Cider().compute_score(G, C)[0])
        if not a.no_spice:
            from pycocoevalcap.spice.spice import Spice
            o["spice"] = 100 * Spice().compute_score(G, C)[0]
        o["chrf"] = sacrebleu.CHRF().corpus_score(H, [REF]).score
        if SC is not None:
            _, _, f2 = SC.score(H, REF)
            for i, h in enumerate(H):
                if not h:
                    f2[i] = 0.0
            o["bertscore"] = 100 * f2.mean().item()
        o = {k: round(v, 2) for k, v in o.items()}
        o["rong"] = sum(not h for h in H)
        o["doi_cau_so_goc_pct"] = round(100 * sum(tokw(h) != tokw(g) for h, g in zip(H, P[a.base])) / len(H), 1)
        o["trung_chuan_pct"] = round(100 * sum(tokw(h) == tokw(r) for h, r in zip(H, REF)) / len(H), 1)
        out[ten] = o
        print(f"{ten:10s} " + " · ".join(f"{k} {v}" for k, v in o.items()), flush=True)

    for s in a.ra:
        ten, p = s.split("=", 1)
        E = {(x["episode_id"], x["step_id"]): x["exemplars"] for x in map(json.loads, open(p, encoding="utf-8"))}
        cop = [any(tokw(e["sent"]) == tokw(h) for e in E[k]) for k, h in zip(K, P[ten])]
        dung = [c and tokw(h) == tokw(r) for c, h, r in zip(cop, P[ten], REF)]
        out[ten]["chep_vi_du_pct"] = round(100 * sum(cop) / len(K), 1)
        out[ten]["chep_dung_pct_trong_so_chep"] = round(100 * sum(dung) / max(sum(cop), 1), 1)
        print(f"[chép] {ten}: chép nguyên văn một ví dụ ở {out[ten]['chep_vi_du_pct']}% bước · "
              f"trong số đó đúng câu chuẩn {out[ten]['chep_dung_pct_trong_so_chep']}%", flush=True)

    M = [m for m in TEN if m in out[a.base]]
    tin = True
    if a.check:
        lech = {m: round(out[a.base][m] - CK500_TEST[m], 2) for m in M}
        tin = all(abs(v) <= 0.06 for v in lech.values())
        print(f"[tự kiểm] {a.base} — số đã công bố: {lech} → {'KHỚP' if tin else '⚠ LỆCH — dừng đọc Δ'}", flush=True)

    print(f"\n| thước | {a.base} | " + " | ".join(t for t in P if t != a.base) + " |")
    print("|---|---:|" + "---:|" * (len(P) - 1))
    for m in M:
        print(f"| {TEN[m]} | {out[a.base][m]:.2f} | " + " | ".join(
            f"{out[t][m]:.2f} ({out[t][m] - out[a.base][m]:+.2f})" for t in P if t != a.base) + " |")

    ket = {}
    for t in P:
        if t == a.base:
            continue
        hon = [m for m in M if out[t][m] > out[a.base][m]]
        ket[t] = dict(hon=len(hon), tong=len(M), thuoc_hon=[TEN[m] for m in hon],
                      dat=len(hon) >= (4 if len(M) == 7 else (len(M) // 2 + 1)))
        print(f"[kết luận] {t}: cao hơn {a.base} ở {len(hon)}/{len(M)} thước "
              f"({', '.join(TEN[m] for m in hon) or '—'}) · {'ĐẠT' if ket[t]['dat'] else 'chưa đạt'}", flush=True)

    json.dump(dict(diem=out, ket_luan=ket, tu_kiem_khop=tin, base=a.base, n=len(K)),
              open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", a.out)


if __name__ == "__main__":
    main()
```


## Phụ lục B — output thô của các phép kiểm trên máy nhà

`ra_build.py` trên bundle giả (60 hàng train lấy từ `train_tru_val` ngoài tác vụ val, `p1_val_rows = val_lon_recs.jsonl` 1.567 dòng, test thật), 6,7 phút CPU:

```text
[kho] 62880 bước · 12542 tác vụ · bỏ 346 tác vụ val · 0 tác vụ test chung kho
[train] 60 hàng · bỏ {} · loại thao tác {'input_text': 10, 'wait': 6, 'click': 39, 'open_app': 3, 'scroll': 2}
[xong] {"train_rows": 60, "train_co_khoi_pct": 86.7, "train_khoi_chua_dich_pct": 19.2, "train_so_vi_du_tb": 4.27, "test_click": 4463, "val_click": 1002, "val_khoi_chua_dich_pct": 13.3, "kho_buoc": 62880, "bo": {}, "seed": 2026100901, "phut": 6.7}
--- ví dụ câu nhắc RA ---
Mục tiêu: I have an upcoming dance performance on October 4th, 2023, at 1:30 p.m. and would like to create a calendar event on the calendar app with a name as as a contemporary dance performance and description contemporary dance performance at the Teatro Carignano so that I won't miss the even
Đã làm: Click on the OK button · Swipe up the screen · Click on the description section
Ví dụ bước tương tự từ tác vụ khác (có thể không khớp màn này):
1. Mục tiêu: In the To Do Reminders app, I want to create a new | Bước trước: Click on the note text box | Bước kế: Enter the note as Contemporary dance performance at the Teatro Carignano
2. Mục tiêu: I want to get new dance shoes for my dance performance, so | Bước trước: Search for dance shoes for ladies | Bước kế: Click on the first result
3. Mục tiêu: In the To Do Reminders app, I want to create a new | Bước trước: Click on the date section | Bước kế: Click on the forward arrow
4. Mục tiêu: In the To Do Reminders app, I want to create a new | Bước trước: (bước đầu) | Bước kế: Open the To Do Reminder app
Viết câu hướng dẫn cho bước tiếp theo.
--- đích: Enter the description as contemporary dance performance at the Teatro Carignano
```

Kiểm khác:

```text
ra/cont cùng hàng, cùng đích: 60 · có khối: 52
4463 chrF ck500 = 62.86 (công bố 62,87)
val click 1002 có pred ck500: 1002
[dữ liệu] test.jsonl · 2231 bước click (--shard 1/2)
```
