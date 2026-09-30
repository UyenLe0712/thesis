# 253 — ACTION: GRPO thưởng SPICE cho S1/101, nhánh không có đầu khe (29/9/2026)

Gửi nguyên file này cho chat thực thi. File tự chứa: script nằm ở **Phụ lục A**, script đọc kết quả trên máy nhà ở **Phụ lục B**.

> **Sửa khi kiểm trên máy WSL 29/9** (bản gốc soạn cho máy Mac): ① Phụ lục A, hàm `train()` dùng biến `n_` chưa định nghĩa ⇒ `NameError` ngay trước lúc train, đã đổi thành `n` (pyflakes bắt được); ② Phụ lục B có một dòng `K0 = {o[...]}` chạy trước khi có `o` ⇒ `NameError`, đã bỏ; đường dẫn `runs/c1/exec0/` sai, đúng là `runs/c1/exec8/`; ③ val là **1.567** dòng (script assert đúng 1.567, chỉ lời văn ghi 1.667); ④ mọi đường dẫn Mac đổi sang WSL. Selftest (mục 4 Ô 3) đã chạy đạt trên CPU: thưởng `[1.0, 0.0, 0.554]`, 3.991 câu nhắc dùng được, `trung_val 0`, `trung_episode_val 0`. Bản chạy được của Phụ lục A: `harness/grpo_spice.py`; của Phụ lục B: `harness/grpo_spice_doc.py`.

> **Đo ở Pha 1 trên Kaggle 29/9 ⇒ chốt `--no-q4` cho mọi lệnh GPU trên T4.** ① Nạp 4-bit thì kiểm hoà chỉ **14/20** (ngưỡng 16). ② Nạp 4-bit thì thăm dò chết ở bước 1: `"_amp_foreach_non_finite_check_and_unscale_cuda" not implemented for 'BFloat16'`. Nguyên nhân nằm ở TRL 0.29.1 `grpo_trainer.py:362–366`: khi mô hình `is_loaded_in_4bit`, TRL tự ép tham số LoRA sang **bf16**, đè bước ép fp32 của script, mà T4 phải train fp16 (bộ scale gradient fp16 không nhận grad bf16). Lượt GRPO `<point>` chạy được vì A100 dùng bf16. Nạp fp16 đầy đủ (`--no-q4`) tránh được cả hai: kiểm hoà fp16 đạt **20/20**. Thăm dò fp16 với `--bs 8 --accum 2` **OOM** (14,54/14,56 GiB, ở forward tính loss) ⇒ thử `--bs 4 --accum 4` kèm `PYTORCH_ALLOC_CONF=expandable_segments:True`. ③ Mốc KL: khi nhận PeftModel, TRL 0.29.1 (`grpo_trainer.py:338–347`) **tự tạo adapter `ref`** chép từ adapter đang có và dùng nó làm tham chiếu (dòng ~1851). Ở đây LoRA mới có B = 0 nên `ref` = đúng S1 đã hoà. Điều này cũng có nghĩa lượt GRPO `<point>` cũ đã KL về MIN chứ không về Qwen gốc (bỏ nghi vấn ở mục 9).

## 0. Bối cảnh, đọc một lần

Luận văn sinh câu hướng dẫn một bước cho màn hình Android (AndroidControl). Mô hình nền là **S1/101: Qwen2.5-VL-3B-Instruct + LoRA r = 8, SFT trên câu người viết**. Hai metric phải hơn S1:

| Metric | Ý nghĩa | S1/101 trên test 4.463 bước |
|---|---|---:|
| `exec` | UGround-V1-2B đọc câu rồi bấm; trúng khi đúng loại thao tác, trong ±14% và đúng ô Voronoi của phần tử | 59,11 |
| SPICE | so câu sinh với câu người, bộ chấm COCO | 44,37 |

Phép kiểm cổng đã chạy xong (file 252). Trên 400 bước val C1, S1 lấy 8 mẫu, nhiệt độ 1,0. Nếu trong 9 câu (greedy + 8 mẫu) chọn câu SPICE cao nhất:

| Trên val C1 | Greedy S1 | Oracle SPICE |
|---|---:|---:|
| SPICE, 400 bước | 57,30 | 75,13 |
| SPICE, 249 bước click | 48,62 | 71,13 |
| `exec`, 249 bước click | 63,45 (158/249) | 68,67 (171/249) |

Hiệu `exec` +5,22, KTC 95% bootstrap theo episode [+1,22; +9,36]. Cổng đạt, tức được phép train. Oracle nhìn câu người, nên đây là trần chọn trong mẫu, không phải dự báo.

Phương pháp chốt (file 250) có hai phần: GRPO thưởng SPICE, và một **đầu khe** có công sửa câu. Ablation bắt buộc tắt từng phần. Lượt này chỉ làm phần GRPO, tức nhánh ablation **“S1 + GRPO, tắt đầu khe”**. Lý do làm trước: cổng vừa đạt là cổng của phần thưởng SPICE, và nhánh này tốn GPU nhất. Đầu khe là một action riêng sau khi có kết quả lượt này.

> Sửa so với file 252: 252 viết “train đúng file 250 mục 3” như một khối. Ở đây tách thành hai lượt, GRPO trước, đầu khe sau. Không đổi phương pháp, chỉ đổi thứ tự.

Không chấm test trong lượt này. Mọi số ra là val, S1 đã thấy val lúc SFT. Không trích số nào vào luận văn.

## 1. Thiết kế lượt train, đã khoá

| Mục | Giá trị | Lý do |
|---|---|---|
| Điểm xuất phát | S1/101 hoà vào Qwen gốc (`merge_and_unload`), rồi gắn LoRA mới cùng `r`, `lora_alpha`, `target_modules` với S1, dropout 0 | TRL tính KL bằng cách tắt adapter. Nếu học tiếp trên adapter S1 thì tắt adapter ra Qwen gốc, KL kéo về Qwen gốc chứ không về S1. Hoà trước thì tắt adapter ra đúng S1 |
| Phần thưởng | `r = SPICE_F(câu, câu người) - 0,02 * max(0, số từ câu - số từ câu người - 3)`; câu rỗng = 0 | Công thức file 250. `μ = 0,02` khoá ngay, không chọn trên val: trên oracle, từ 0,01 đến 0,05 cho cùng `exec` |
| Grounder trong vòng train | Không | UGround chỉ dùng để chấm |
| Tập câu nhắc | 1.000 bước lấy từ 4.000 dòng `p1_train_rows.jsonl`, seed 101, mọi loại thao tác | Có sẵn ảnh + OCR trong dataset `fgrb-p1-bundle`. Script assert không trùng bước, không trùng episode với 1.567 bước val |
| Câu nhắc | dùng `build_branch_data.prompt_body + SYS`, ảnh đặt trước chữ, `min_pixels 200704`, `max_pixels 1003520` | giống lúc SFT và lúc sinh `c1_mau.jsonl` |
| GRPO | G = 8 mẫu/câu nhắc, 2 câu nhắc/bước (16 câu/bước), 500 bước = 1 epoch trên 1.000 câu nhắc | 8 mẫu là đúng số mẫu của phép kiểm cổng |
| Sinh | nhiệt độ 1,0, `top_p 1,0`, `top_k 0`, `repetition_penalty 1,0`, tối đa 96 token | giống lúc lấy 8 mẫu C1 |
| Tối ưu | β (KL) 0,04, lr 1e-5, constant sau 10 bước warmup, `max_grad_norm 1,0` | giống lượt GRPO `<point>` đã chạy được |
| Nạp | 4-bit NF4 mặc định, fp16 trên T4, bf16 trên L4/A100 | đường 4-bit đã chạy được ở lượt GRPO `<point>` |
| Lưu | mỗi **25** bước, giữ hết (sửa 29/9, trước là 50: để nối commit mất ít bước hơn) | chấm val ở bước 250 và 500 |

## 2. Luật đọc kết quả, khoá trước khi có số

Chấm hai điểm lưu `checkpoint-250` và `checkpoint-500`. Mỗi điểm lưu sinh greedy trên đúng **400 bước C1**, rồi:

- SPICE trên 400 bước, so với S1 greedy **57,30**.
- `exec` trên 249 bước click, so với S1 greedy **63,45**, ghép cặp với tệp thô `score_k0_raw.jsonl` của 251.

| Kết quả của điểm lưu | Kết luận |
|---|---|
| ΔSPICE ≥ +2,0 và Δ`exec` ≥ 0 | **ĐẠT.** Được viết action đầu khe, rồi chấm test một lần |
| Cả hai điểm lưu: Δ`exec` ≤ −3,0, hoặc ΔSPICE < +1,0 | **DỪNG** nhánh GRPO. Báo người dùng, không chạy thêm bước |
| Còn lại | Báo người dùng quyết, không tự chạy tiếp |

Nhiều điểm lưu cùng ĐẠT thì lấy điểm có `exec` cao hơn, bằng nhau thì lấy SPICE cao hơn. Kèm hai phép kiểm lệch thưởng: số từ trung bình của câu không tăng quá 3 từ so với S1 greedy, và 0 câu rỗng.

Val thiên vị S1 (S1 đã học thuộc val), nên đòi Δ`exec` ≥ 0 là đòi chặt với GRPO. Không nới ngưỡng sau khi thấy số.

## 3. Đầu vào trên Kaggle

| Dataset | Chứa gì | Trạng thái |
|---|---|---|
| `fgrb-p1-bundle` | `adapter_s1_seed101/`, `images/` (5.567 ảnh), `ocr.jsonl`, `p1_train_rows.jsonl` (4.000), `p1_val_rows.jsonl` (1.567) | đã có |
| `c1-exec8` | `c1_mau.jsonl` (400 dòng: `greedy`, `mau`, `gold`) + `c1_picks.json` + gói mã `thesis/harness/{score_run,metric_exec,a11y_inventory}.py` | đã có từ 251. ⛔ Không gắn thêm dataset nào khác có `c1_mau.jsonl` — Ô 2 đòi đúng một bản |
| `grpo-spice-script` (mới) | `grpo_spice.py` (Phụ lục A) và `build_branch_data.py` | người dùng upload |
| `thesis-val-cham` | cho bước chấm `exec` ở mục 6 (gói mã nằm sẵn trong `c1-exec8`) | đã có từ 251, chỉ gắn ở Pha 3 |

Cách dựng `grpo-spice-script` trên máy WSL (bản Phụ lục A đã tách sẵn thành `harness/grpo_spice.py`):

```bash
cd /mnt/d/Master/Thesis
mkdir -p _bundles/grpo-spice-script
cp harness/grpo_spice.py harness/build_branch_data.py _bundles/grpo-spice-script/
```

Rồi upload thư mục đó thành Kaggle Dataset `grpo-spice-script`.

Notebook: **Internet ON** (SPICE tải Stanford CoreNLP lần đầu, và cần tải Qwen), Accelerator **GPU T4 ×2** (Kaggle không có lựa chọn T4 ×1). Script **ghim GPU 0** bằng `CUDA_VISIBLE_DEVICES=0`: nếu Trainer thấy 2 GPU thì `n_gpu = 2`, cỡ lô thật nhân đôi lệch với `generation_batch_size`, và ở nhánh `--no-q4` Trainer còn bọc `nn.DataParallel` (transformers `trainer.py`, chỉ bỏ qua khi nạp 4/8-bit). GPU 1 để trống.

## 4. Pha 1 — chạy tương tác, thăm dò (~1 h T4, 0 đồng)

### Ô 1 — gói và Java 8

```python
import subprocess, sys, os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"   # Kaggle chỉ có T4 ×2; ghim một GPU, mọi lệnh ! và Popen sau đều thừa hưởng

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:]); return r.returncode

sh("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless")
sh("update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java")
sh("java -version")
sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes pycocoevalcap 'trl==0.29.1' 2>&1 | tail -3")
sh(f'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.get_device_name(0))"')
```

`java -version` nên ra 1.8. Trên máy nhà SPICE đã chạy với Corretto 11, nên Java 11 cũng dùng được; Java 17 trở lên thì chưa thử. Nếu `trl==0.29.1` xung đột với transformers mới, giữ nguyên lỗi về, đừng tự đổi phiên bản TRL.

### Ô 2 — đường dẫn

```python
import os, glob, shutil, hashlib

W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "images" in d)
C1 = glob.glob("/kaggle/input/**/c1_mau.jsonl", recursive=True); assert len(C1) == 1, C1; C1 = C1[0]
assert md5(C1) == "d757554326977309c3a65ae0b144c211", "DỪNG: c1_mau.jsonl lệch bản máy nhà"
# Output của Pha 2 (gắn làm input ở Pha 3 / lượt chạy tiếp) cũng có grpo_spice.py nằm cạnh train.log ⇒ loại ra
SRC = [p for p in glob.glob("/kaggle/input/**/grpo_spice.py", recursive=True)
       if not os.path.exists(os.path.join(os.path.dirname(p), "train.log"))]
assert len(SRC) == 1, f"DỪNG: cần đúng một grpo_spice.py của dataset grpo-spice-script, thấy {SRC}"
for f in ("grpo_spice.py", "build_branch_data.py"):
    shutil.copy(os.path.join(os.path.dirname(SRC[0]), f), f"{W}/{f}")
assert md5(f"{W}/grpo_spice.py") == "d99d03c0c01718283e84ac3851ef5591", "DỪNG: grpo_spice.py trên Kaggle là bản cũ, upload lại"  # bản 29/9 tối (save 25 + resume an toàn)
assert md5(f"{W}/build_branch_data.py") == "619e63e123a6dbf60086e65ee94a3912", "DỪNG: build_branch_data.py lệch bản máy nhà"
MERGED = f"{W}/s1_merged"; OUT = f"{W}/grpo_spice"
print("BUNDLE:", BUNDLE, "\nC1:", C1, "\nSRC:", SRC[0], "\nmd5 khớp cả ba", flush=True)
```

### Ô 3 — selftest (CPU + Java, vài phút lần đầu vì tải CoreNLP)

```bash
!cd /kaggle/working && python grpo_spice.py --selftest --bundle {BUNDLE}
```

Phải thấy `✅ selftest ĐẠT`, tập câu nhắc ≥ 1.000 dòng, `trung_val 0`, `trung_episode_val 0`.

### Ô 4 — hoà S1 và kiểm hoà

```bash
!cd /kaggle/working && python grpo_spice.py --merge --bundle {BUNDLE} --merged {MERGED}
!cd /kaggle/working && python grpo_spice.py --gen --bundle {BUNDLE} --merged {MERGED} --c1 {C1} --n 20 --out {W}/kiem_hoa.jsonl
```

Dòng `[kiểm hoà] x/20 câu trùng greedy S1`. Cần **x ≥ 16**. Mô hình hoà rồi nạp 4-bit phải ra lại gần đúng câu của S1; nếu không, KL đang kéo về một mô hình khác S1.

Nếu x < 16: chạy lại dòng `--gen` với thêm `--no-q4` và tên tệp khác. Đạt thì mọi lệnh sau đều thêm `--no-q4`. Vẫn không đạt thì dừng, gửi log.

### Ô 5 — thăm dò 20 bước trên 50 câu nhắc dài nhất

⛔ Không chạy dạng `!… | tail` (im lặng tới lúc xong, 29/9 đã ngồi chờ >30 phút không biết treo hay chạy). Chạy nền, ghi log ra tệp, xem tiến độ bằng ô 5b. Cờ `--no-q4 --bs 4 --accum 4` là cấu hình đã chốt ở đầu file.

```python
# Ô 5a — chạy nền, trả lại ngay
import subprocess, time
logp = f"{W}/probe.log"
p = subprocess.Popen(
    ["python", "grpo_spice.py", "--probe", "--no-q4", "--bs", "4", "--accum", "4",
     "--bundle", BUNDLE, "--merged", MERGED, "--out", f"{W}/probe"],
    cwd=W, stdout=open(logp, "w"), stderr=subprocess.STDOUT,
    env={**os.environ, "TQDM_DISABLE": "1",
         "PYTORCH_ALLOC_CONF": "expandable_segments:True",
         "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"},
    start_new_session=True)   # Stop ô 5b không giết tiến trình này
t_start = time.time()
print("PID", p.pid)
```

```python
# Ô 5b — theo dõi liên tục: mỗi 60 s một dòng + các dòng log quan trọng mới; tự dừng khi tiến trình kết thúc
import time, subprocess
seen = 0
while True:
    L = open(logp, errors="ignore").read().splitlines()
    keep = [l for l in L if l.startswith(("[", "{", "Traceback", "torch.", "RuntimeError", "⚠", "GRPOConfig")) or "Error" in l]
    gpu = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,utilization.gpu", "--format=csv,noheader"],
                         capture_output=True, text=True).stdout.strip().replace("\n", " | ")
    print(f"{(time.time()-t_start)/60:5.1f} phút · bước {sum(l.startswith('[spice]') for l in L)}/20 · GPU {gpu}", flush=True)
    for l in keep[seen:]:
        print("    ", l[:220], flush=True)
    seen = len(keep)
    if p.poll() is not None:
        print(f"== tiến trình đã dừng, mã {p.returncode} ==\n" + "\n".join(L[-15:]), flush=True)
        break
    time.sleep(60)
```

Ghi lại năm thứ, gửi về chat nhà:

1. dòng `[xong] ... s/bước · đỉnh VRAM ... GiB · SPICE ... s/lần`;
2. dòng `[LoRA mới] tham số học ...` phải bằng số của S1;
3. dòng `[lô] mỗi lượt sinh 16 câu = 2 câu nhắc × 8`;
4. `loss` và `kl` trong log không có `nan`;
5. bảng câu mẫu in ra (TRL `log_completions`) là câu tiếng Anh ngắn kiểu `Click on ...` và prompt có token ảnh đứng ngay trước `Mục tiêu:`.

Chọn máy theo số đo, đừng đoán:

| Thăm dò trên T4 | Làm gì |
|---|---|
| Không OOM, không nan, ≤ 70 s/bước (500 bước ≤ ~9,7 h) | Pha 2 trên Kaggle T4, 0 đồng |
| OOM với `--bs 8 --accum 2` | Thử lại thăm dò với `--bs 4 --accum 4` (vẫn 2 câu nhắc × 8 mẫu). Hết OOM thì dùng cấu hình đó |
| Vẫn OOM, có nan, hoặc > 70 s/bước | **Dừng, gửi số về.** Người dùng quyết L4 hay A100 (tốn tiền) |

## 5. Pha 2 — train 500 bước (commit, để ngủ được)

> ⭐ **Thay bằng `harness/kaggle_grpo_spice_commit.md` (29/9 tối).** Thăm dò T4 đo **160,6 s/bước** (ngưỡng ≤ 70), đỉnh VRAM 13,22 GiB, 3/20 bước có gradient ≈ 0 do nhóm hoà thưởng. User chọn cách (a): T4 0 đồng, nối **3 commit** (~225 · ~450 · 500 bước, ~25 h hạn mức). Mã: `save_steps` 25 và `--resume auto` chỉ nhận điểm lưu đủ tệp. Ô dưới đây là bản cũ, giữ để tra.

Notebook commit chỉ gồm Ô 1, Ô 2, lệnh `--merge` của Ô 4, và ô dưới. Bấm **Save Version → Save & Run All**.

```python
import subprocess, time, os, shutil

log = open(f"{W}/train.log", "a")
cmd = ["python", "grpo_spice.py", "--train", "--bundle", BUNDLE, "--merged", MERGED,
       "--out", OUT, "--resume", "auto"]
# thêm "--bs", "4", "--accum", "4" và/hoặc "--no-q4" nếu thăm dò đã chốt như vậy

p = subprocess.Popen(
    cmd,
    cwd=W,
    stdout=log,
    stderr=subprocess.STDOUT,
    text=True,
    env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
         "PYTORCH_ALLOC_CONF": "expandable_segments:True", "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"},
)

t0 = time.time()
while p.poll() is None:
    time.sleep(120)
    tail = [r for r in open(f"{W}/train.log", encoding="utf-8", errors="ignore") if r.startswith("[spice]")]
    print(f"{(time.time()-t0)/3600:4.2f} h · {tail[-1].strip() if tail else 'chưa có bước'}", flush=True)
    if time.time() - t0 > 3600 * 11 and p.poll() is None:
        print("⛔ đã 11 h, dừng trước trần 12 h của Kaggle để Output kịp lưu; điểm lưu đã ghi mỗi 50 bước", flush=True)
        p.terminate(); p.wait()

print("mã thoát", p.returncode)
print(open(f"{W}/train.log", encoding="utf-8", errors="ignore").read()[-3000:])
shutil.rmtree(MERGED, ignore_errors=True)  # bỏ bản hoà ~7 GB khỏi Output; Pha 3 tự hoà lại
```

Nếu dừng trước bước 500 (dòng `⛔ đã 11 h`): *Edit* notebook → *Add Input* là Output của version vừa xong → thêm ô dưới đây **ngay sau Ô 2** → *Save Version* lần nữa. `--resume auto` tự lấy điểm lưu cuối.

```python
ck = [p for p in glob.glob("/kaggle/input/**/grpo_spice/checkpoint-*", recursive=True) if os.path.isdir(p)]
print("chép tiếp từ:", sorted(ck, key=lambda p: int(p.rsplit("-", 1)[1]))[-3:])
os.makedirs(OUT, exist_ok=True)
for p in ck:
    shutil.copytree(p, os.path.join(OUT, os.path.basename(p)), dirs_exist_ok=True)
```

Trong Output phải có `grpo_spice/checkpoint-250/` và `grpo_spice/checkpoint-500/`. Tải cả hai (LoRA, vài chục MB mỗi cái) về máy WSL, đặt vào `runs/grpo_spice/` (theo luật đọc kết quả: đặt thẳng vào thư mục của phép đo).

## 6. Pha 3 — sinh greedy trên val và chấm `exec` (Kaggle T4 ×2, thử tương tác rồi commit, ~2,5 h)

Notebook mới. Input: `fgrb-p1-bundle`, `c1-exec8`, `grpo-spice-script`, `thesis-val-cham`, **Output của Pha 2**. Accelerator GPU T4 ×2, Internet ON. Notebook gồm: Ô 1, Ô 2, dòng `--merge` của Ô 4 (thêm `--no-q4` nếu Pha 1 đã chốt), rồi ba ô dưới theo đúng thứ tự.

**Chạy thử tương tác trước** với `TEST = True` (5 câu mỗi điểm lưu, chấm 3 bước mỗi tệp, ~20 phút), gửi output về. Ổn thì sửa `TEST = False`, **Save Version → Save & Run All**.

### Ô P3-A — sinh greedy 400 bước C1 cho hai điểm lưu

```python
import subprocess, json

TEST = True          # chạy thử tương tác; đổi False trước khi commit
Q4 = ["--no-q4"]     # chốt ở Pha 1: T4 phải nạp fp16 đầy đủ

import time

def chay(cmd, log, cwd, nhip=60):
    # chạy con ghi log ra tệp; mỗi `nhip` giây in dòng cuối để không bao giờ im lặng
    t0 = time.time()
    with open(log, "w") as f:
        q = subprocess.Popen(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                             env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1"})
        while q.poll() is None:
            time.sleep(nhip)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"  {(time.time()-t0)/60:5.1f} phút · {os.path.basename(log)} · {L[-1][:110] if L else 'chưa có dòng nào'}", flush=True)
    rc = q.returncode
    print(f"--- {os.path.basename(log)} · mã thoát {rc} · {(time.time()-t0)/60:.1f} phút ---")
    print("".join(open(log, errors="ignore").readlines()[-6:]), flush=True)
    return rc

CK = {}
for s in (250, 500):
    c = [p for p in glob.glob(f"/kaggle/input/**/grpo_spice/checkpoint-{s}", recursive=True) if os.path.isdir(p)]
    assert len(c) == 1, f"DỪNG: cần đúng một checkpoint-{s}, thấy {c}"
    CK[s] = c[0]

N = 5 if TEST else 400
for s, ck in CK.items():
    out = f"{W}/pred_ck{s}.jsonl"
    chay(["python", "grpo_spice.py", "--gen", "--bundle", BUNDLE, "--merged", MERGED, "--c1", C1,
          "--ckpt", ck, "--n", str(N), "--out", out] + Q4, f"{W}/gen_ck{s}.log", W)
    n = sum(1 for _ in open(out))
    print(f"ck{s}: {n}/{N} câu", flush=True)
    assert n >= N, "DỪNG: thiếu câu, xem gen_ck*.log"
```

Mỗi điểm lưu phải in dòng `[so với S1] x/N câu trùng greedy S1` và `N/N câu`. Nếu mã thoát khác 0 vì `⛔ có câu rỗng` thì tệp vẫn đủ, cứ chạy tiếp, Phụ lục B sẽ đếm câu rỗng.

### Ô P3-B — dựng dữ liệu chấm

Dán **nguyên văn Ô 2 của file 251** (`harness/tai_lieu_2026-09-28/251_ACTION_GPU_EXEC_8_MAU_C1_28_9.md`, mục 4). Ô đó đọc lại `c1_mau.jsonl` vào biến `C1` và dựng `c1preds/k0.jsonl` (greedy S1). P3-A đã chạy xong nên việc ghi đè `C1` không ảnh hưởng. Phải thấy `bước C1: 400 | click: 249 … | ảnh thiếu: 0` và `cây trợ năng: 249/249 bước click · 0 bước rỗng nút`.

### Ô P3-C — chấm `exec`, kèm chấm lại greedy S1 làm phép kiểm

Môi trường ở đây đã nâng `transformers` (Ô 1), khác môi trường của 251. Vì vậy chấm lại luôn greedy S1 (`k0_lai`) trong cùng phiên. Phụ lục B ghép cặp với bản chấm lại này, nên hai bên luôn cùng dụng cụ.

```python
M = 3 if TEST else 0
for ten, pred in (("k0_lai", f"{W}/c1preds/k0.jsonl"),
                  ("ck250", f"{W}/pred_ck250.jsonl"),
                  ("ck500", f"{W}/pred_ck500.jsonl")):
    cmd = ["python", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", pred,
           "--data-root", f"{W}/c1data", "--recs-file", "c1_recs.jsonl", "--out", f"{W}/score_{ten}.json"]
    if M:
        cmd += ["--n", str(M)]
    chay(cmd, f"{W}/cham_{ten}.log", f"{W}/pk/thesis")
    R = [json.loads(l) for l in open(f"{W}/score_{ten}_raw.jsonl")]
    print(f"== {ten}: {len(R)} bước · exec {sum(int(r['executable']) for r in R)}", flush=True)
print("KIỂM (bản đủ): k0_lai phải 249 bước, exec 158 như 251. Lệch thì gửi số về, đừng tự diễn giải.")
```

Tải về `runs/grpo_spice/` trên WSL: `pred_ck250.jsonl`, `pred_ck500.jsonl`, `score_k0_lai_raw.jsonl`, `score_ck250_raw.jsonl`, `score_ck500_raw.jsonl`, `gen_ck*.log`, `cham_*.log`, cùng `train.log` của Pha 2. Rồi chạy `~/.venvs/thesis/bin/python harness/grpo_spice_doc.py`.

## 7. Dừng và gửi log khi

- selftest không đạt, hoặc tập câu nhắc trùng val;
- kiểm hoà < 16/20 cả khi `--no-q4`;
- nan ở `loss`/`kl`, CUDA out of memory ngoài lần thử `--bs 4`, AssertionError, mã thoát khác 0;
- `[spice]` không in dòng mới sau 15 phút;
- câu sinh trong lúc train dài lên, lặp từ, hoặc chuyển sang tiếng Việt.

## 8. Việc người dùng quyết, chat thực thi không tự làm

1. Upload dataset `grpo-spice-script` (mục 3).
2. Nếu thăm dò T4 không đủ: có trả tiền L4/A100 hay không.
3. Sau Pha 3: đọc bảng mục 2, quyết có viết action đầu khe hay không.
4. Chấm test: chỉ một lần, sau khi đã khoá điểm lưu và đầu khe. Không làm trong lượt này.
5. Không tự commit, không push.

## 9. Chưa kiểm được trên máy nhà

- Đã kiểm trên máy nhà ngày 29/9 (`_venv_g0`, Corretto 11): cả hai phụ lục biên dịch được. `r_spice` cho ba câu thử ra `[1.0, 0.0, 0.554]`: câu trùng câu người được 1, câu rỗng được 0, câu dài bị phạt. Hàm cũng nhận completion dạng hội thoại (`[{"role": "assistant", ...}]`). `spice_batch` trên greedy S1 của 400 bước C1 ra đúng **57,30**. Mỗi lần gọi SPICE mất 3–5 giây, tức khoảng 30–40 phút cộng thêm cho 500 bước. `prompt_body` ra đúng khuôn `Mục tiêu: …\nViết câu hướng dẫn cho bước tiếp theo.`
- Phần GPU (`--merge`, `--gen`, `--probe`, `--train`) chưa chạy lần nào. Ở 3–5 dễ bắt lỗi trước khi tốn giờ.
- Tên và mặc định của các khoá `GRPOConfig` thay theo phiên bản TRL. Script bỏ khoá không có và in ra danh sách bỏ. Nếu danh sách có `beta`, `num_generations` hoặc `temperature` thì dừng.
- Tham chiếu KL: TRL với mô hình PEFT tính log-prob tham chiếu bằng cách tắt adapter. Mã `harness/grpo_point.py` trong kho không có `add_adapter("ref")` như `CLAUDE.md` mô tả cho lượt GRPO `<point>` cũ. Lượt này né chuyện đó bằng cách hoà S1 trước. Lượt cũ có thể đã KL về Qwen gốc; chưa kiểm, không kết luận.

---

# Phụ lục A — `grpo_spice.py`

```python
# -*- coding: utf-8 -*-
"""GRPO thưởng SPICE cho S1/101 — nhánh "S1 + GRPO, tắt đầu khe" của phương pháp file 250.

python grpo_spice.py --selftest --bundle B
python grpo_spice.py --merge --bundle B --merged M
python grpo_spice.py --gen --bundle B --merged M --c1 C --n 20 --out kiem_hoa.jsonl
python grpo_spice.py --probe --bundle B --merged M --out O
python grpo_spice.py --train --bundle B --merged M --out O --resume auto
python grpo_spice.py --gen --bundle B --merged M --c1 C --ckpt O/checkpoint-250 --out p.jsonl
"""

import os, re, sys, json, time, glob, random, argparse, dataclasses, collections

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")  # T4 ×2 trên Kaggle: Trainer thấy 2 GPU thì n_gpu=2, lô lệch
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_branch_data import prompt_body, SYS  # noqa: E402

BASE = "Qwen/Qwen2.5-VL-3B-Instruct"
SEED = 101
SEED_C1 = 20260927
MU = 0.02
N_PROMPT = 1000
PIX = dict(min_pixels=200704, max_pixels=1003520)
WORD = re.compile(r"[A-Za-z0-9'-]+")
STAT = {"n": 0, "t": 0.0}


def nwords(s):
    return len(WORD.findall(s or ""))


def _text(c):
    if isinstance(c, list):
        return (c[0].get("content") if c else "") or ""
    return c or ""


def spice_batch(cands, refs):
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    from pycocoevalcap.spice.spice import Spice

    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(refs)})
    c = tk.tokenize({i: [{"caption": s}] for i, s in enumerate(cands)})
    _, sc = Spice().compute_score(g, c)

    out = []
    for x in sc:
        f = x["All"]["f"]
        out.append(0.0 if f is None or f != f else float(f))
    return out


def r_spice(completions, gold, **kw):
    t0 = time.time()
    sents = [_text(c).strip() for c in completions]
    f = spice_batch([s if s else "none" for s in sents], list(gold))
    out = [0.0 if not s else x - MU * max(0, nwords(s) - nwords(g) - 3)
           for s, g, x in zip(sents, gold, f)]
    dt = time.time() - t0
    STAT["n"] += 1
    STAT["t"] += dt
    print(f"[spice] lần {STAT['n']} · {len(sents)} câu · {dt:.1f}s · thưởng TB {sum(out)/len(out):.3f}"
          f" · số từ TB {sum(map(nwords, sents))/len(sents):.1f} · rỗng {sum(not s for s in sents)}",
          flush=True)
    return out


def nap_ocr(bundle):
    return {o["image"]: o for o in map(
        json.loads, open(os.path.join(bundle, "ocr.jsonl"), encoding="utf-8")
    )}


def body_of(r, ocr):
    return prompt_body({"goal": r["goal"], "history": r.get("history") or []},
                       ocr.get(r["image"]))


def dung_hang(bundle, n=N_PROMPT, dai_nhat=0):
    tr = [json.loads(l) for l in open(os.path.join(bundle, "p1_train_rows.jsonl"), encoding="utf-8")]
    va = [json.loads(l) for l in open(os.path.join(bundle, "p1_val_rows.jsonl"), encoding="utf-8")]
    assert len(tr) == 4000 and len(va) == 1567, (len(tr), len(va))

    kv = {(r["episode_id"], r["step_id"]) for r in va}
    ev = {r["episode_id"] for r in va}
    ocr = nap_ocr(bundle)
    rows, bo = [], collections.Counter(
        trung_val=0, trung_episode_val=0, thieu_anh=0, thieu_ocr=0, rong=0
    )

    for r in tr:
        k = (r["episode_id"], r["step_id"])
        if k in kv:
            bo["trung_val"] += 1
            continue
        if r["episode_id"] in ev:
            bo["trung_episode_val"] += 1
            continue

        p = os.path.join(bundle, r["image"])
        if not os.path.exists(p):
            bo["thieu_anh"] += 1
            continue
        if r["image"] not in ocr:
            bo["thieu_ocr"] += 1
            continue

        gold = (r.get("target_instruction") or "").strip()
        if not gold:
            bo["rong"] += 1
            continue

        body = body_of(r, ocr)
        rows.append(dict(
            key=f"{k[0]}_{k[1]}",
            image=p,
            prompt=[
                {"role": "system", "content": SYS},
                {"role": "user", "content": "\n" + body},
            ],
            gold=gold,
            action_type=(r.get("action") or {}).get("action_type") or "",
            n_char=len(body),
        ))

    assert bo["trung_val"] == 0 and bo["trung_episode_val"] == 0, f"⛔ tập câu nhắc chạm val: {dict(bo)}"

    random.Random(SEED).shuffle(rows)
    rows = sorted(rows, key=lambda r: -r["n_char"])[:dai_nhat] if dai_nhat else rows[:n]
    return rows, dict(bo)


def selftest(a):
    gold = [
        "Click on the search bar",
        "Open the Clock app",
        "Click on the Settings icon at the top right corner",
    ]
    cand = [
        "Click on the search bar",
        "",
        "Click on the Settings icon at the top right corner of the screen and then wait for it to open fully",
    ]
    r = r_spice(cand, gold)
    print("thưởng:", [round(x, 3) for x in r], "← kỳ vọng [~1.0, 0.0, < câu 1]")
    assert r[0] > 0.99 and r[1] == 0.0 and r[2] < r[0]

    rows, bo = dung_hang(a.bundle, n=10 ** 9)
    print(f"tập câu nhắc dùng được: {len(rows)} · bỏ: {bo}")
    print("loại thao tác:", dict(collections.Counter(x["action_type"] for x in rows)))
    assert len(rows) >= N_PROMPT, len(rows)
    print("ví dụ câu nhắc:", json.dumps(rows[0]["prompt"], ensure_ascii=False)[:600])
    print("vàng:", rows[0]["gold"])
    print("✅ selftest ĐẠT")


def _dtype():
    import torch
    return torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16


def _kw(dt):
    import transformers
    return {("dtype" if int(transformers.__version__.split(".")[0]) >= 5 else "torch_dtype"): dt}


def merge(a):
    if os.path.exists(os.path.join(a.merged, "config.json")):
        print("[hoà] đã có", a.merged, flush=True)
        return

    from transformers import Qwen2_5_VLForConditionalGeneration
    from peft import PeftModel

    dt = _dtype()
    m = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        BASE, device_map={"": 0}, **_kw(dt)
    )
    m = PeftModel.from_pretrained(m, a.adapter).merge_and_unload()
    m.save_pretrained(a.merged, safe_serialization=True)
    print(f"[hoà] xong → {a.merged} · dtype {dt}", flush=True)


def nap(a):
    import torch
    from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration, BitsAndBytesConfig

    dt = _dtype()
    kw = _kw(dt)

    if a.q4:
        kw["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=dt,
            bnb_4bit_use_double_quant=True,
        )

    proc = AutoProcessor.from_pretrained(BASE, **PIX)
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        a.merged, device_map={"": 0}, **kw
    )
    print(f"[nạp] {a.merged} · dtype {dt} · 4-bit {a.q4} · {torch.cuda.get_device_name(0)}",
          flush=True)
    return proc, model, dt


def gen(a):
    import torch
    from PIL import Image

    proc, model, _ = nap(a)

    if a.ckpt:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, a.ckpt)
        print("[điểm lưu]", a.ckpt, flush=True)

    model.eval()
    va = [json.loads(l) for l in open(
        os.path.join(a.bundle, "p1_val_rows.jsonl"), encoding="utf-8"
    )]
    rows = random.Random(SEED_C1).sample(va, 400)
    C1 = [json.loads(l) for l in open(a.c1, encoding="utf-8")]

    assert [(r["episode_id"], r["step_id"]) for r in rows] == \
           [(d["episode_id"], d["step_id"]) for d in C1], \
           "⛔ thứ tự 400 bước lệch c1_mau.jsonl"

    rows = C1 = rows[:a.n], C1[:a.n]
    rows, C1 = rows
    ocr = nap_ocr(a.bundle)
    done = set()

    if os.path.exists(a.out):
        done = {
            (d["episode_id"], d["step_id"])
            for d in map(json.loads, open(a.out, encoding="utf-8"))
        }

    fo = open(a.out, "a", encoding="utf-8")
    t0 = time.time()

    for i, r in enumerate(rows):
        if (r["episode_id"], r["step_id"]) in done:
            continue

        msg = [
            {"role": "system", "content": SYS},
            {"role": "user", "content": [
                {"type": "image"},
                {"type": "text", "text": "\n" + body_of(r, ocr)},
            ]},
        ]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.bundle, r["image"])).convert("RGB")
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
        fo.write(json.dumps({
            "episode_id": r["episode_id"],
            "step_id": r["step_id"],
            "pred": s,
        }, ensure_ascii=False) + "\n")
        fo.flush()

        if (i + 1) % 20 == 0:
            print(f"  {i+1}/{len(rows)} · {(time.time()-t0)/60:.1f} phút · {s[:60]!r}",
                  flush=True)

    fo.close()
    P = {
        (d["episode_id"], d["step_id"]): d["pred"]
        for d in map(json.loads, open(a.out, encoding="utf-8"))
    }
    assert all(P.get((d["episode_id"], d["step_id"])) for d in C1), "⛔ có câu rỗng hoặc thiếu bước"
    same = sum(P[(d["episode_id"], d["step_id"])] == d["greedy"] for d in C1)
    tag = "[kiểm hoà]" if not a.ckpt else "[so với S1]"
    print(f"{tag} {same}/{len(C1)} câu trùng greedy S1 của c1_mau", flush=True)


def _n_s1(adapter):
    from safetensors import safe_open
    with safe_open(os.path.join(adapter, "adapter_model.safetensors"), "pt") as f:
        return sum(f.get_tensor(k).numel() for k in f.keys())


def train(a):
    import torch, trl, transformers, peft
    from peft import LoraConfig, get_peft_model
    from trl import GRPOConfig, GRPOTrainer
    from datasets import Dataset, Image as HFImage

    print(f"trl {trl.__version__} · transformers {transformers.__version__} · "
          f"peft {peft.__version__} · torch {torch.__version__}", flush=True)

    proc, model, dt = nap(a)
    proc.tokenizer.padding_side = "left"

    s1 = json.load(open(os.path.join(a.adapter, "adapter_config.json"), encoding="utf-8"))
    lc = LoraConfig(
        r=s1["r"],
        lora_alpha=s1["lora_alpha"],
        lora_dropout=0.0,
        bias="none",
        target_modules=s1["target_modules"],
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lc)
    model.enable_input_require_grads()

    ntr = 0
    for n, p_ in model.named_parameters():
        if p_.requires_grad:
            if "visual" in n:
                raise SystemExit(f"⛔ tháp thị giác đang học: {n}")
            if p_.dtype != torch.float32:
                p_.data = p_.data.float()
            ntr += p_.numel()

    ns1 = _n_s1(a.adapter)
    print(f"[LoRA mới] tham số học {ntr:,} · S1 có {ns1:,}", flush=True)
    assert ntr == ns1, "⛔ LoRA mới không cùng cỡ S1"

    rows, bo = dung_hang(
        a.bundle,
        n=a.n_prompt,
        dai_nhat=(50 if a.probe else 0),
    )
    print(f"[câu nhắc] {len(rows)} · bỏ {bo} · n_char max {max(r['n_char'] for r in rows)}",
          flush=True)

    os.makedirs(a.out, exist_ok=True)
    json.dump(
        [r["key"] for r in rows],
        open(os.path.join(a.out, "prompt_keys.json"), "w"),
    )

    ds = Dataset.from_list(rows).cast_column("image", HFImage())

    bf = dt == torch.bfloat16
    want = dict(
        output_dir=a.out,
        seed=SEED,
        bf16=bf,
        fp16=not bf,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        num_generations=a.G,
        per_device_train_batch_size=a.bs,
        gradient_accumulation_steps=a.accum,
        max_completion_length=96,
        temperature=1.0,
        top_p=1.0,
        top_k=0,
        repetition_penalty=1.0,
        beta=a.beta,
        learning_rate=a.lr,
        lr_scheduler_type="constant_with_warmup",
        warmup_steps=10,
        max_steps=(20 if a.probe else a.max_steps),
        num_train_epochs=1,
        mask_truncated_completions=True,
        log_completions=a.probe,
        num_completions_to_print=2,
        logging_steps=1,
        save_steps=(10 ** 9 if a.probe else 50),
        save_total_limit=None,
        report_to="none",
        remove_unused_columns=False,
        dataloader_num_workers=2,
        disable_tqdm=True,
        max_grad_norm=1.0,
    )

    F = {f.name for f in dataclasses.fields(GRPOConfig)}
    thieu = sorted(set(want) - F)
    print("⚠️ GRPOConfig không có khoá (đã bỏ):", thieu, flush=True)
    assert not {"beta", "num_generations", "temperature", "max_completion_length"} & set(thieu)

    args = GRPOConfig(**{k: v for k, v in want.items() if k in F})
    gb = getattr(args, "generation_batch_size", None)

    print("GRPOConfig:", {
        k: getattr(args, k, None)
        for k in (
            "num_generations",
            "per_device_train_batch_size",
            "gradient_accumulation_steps",
            "generation_batch_size",
            "steps_per_generation",
            "max_completion_length",
            "temperature",
            "top_p",
            "top_k",
            "beta",
            "learning_rate",
            "loss_type",
            "scale_rewards",
            "max_steps",
            "bf16",
            "fp16",
        )
    }, flush=True)

    print(f"[lô] mỗi lượt sinh {gb} câu = {gb // a.G if gb else '?'} câu nhắc × {a.G}",
          flush=True)

    trainer = GRPOTrainer(
        model=model,
        reward_funcs=[r_spice],
        args=args,
        train_dataset=ds,
        processing_class=proc,
    )

    resume = a.resume
    if resume == "auto":
        ck = sorted(
            glob.glob(os.path.join(a.out, "checkpoint-*")),
            key=lambda p: int(p.rsplit("-", 1)[1]),
        )
        resume = ck[-1] if ck else None

    print("[tiếp từ]", resume, flush=True)
    torch.cuda.reset_peak_memory_stats()
    t0 = time.time()

    trainer.train(resume_from_checkpoint=resume)

    el = time.time() - t0
    buoc = max(
        trainer.state.global_step - (int(resume.rsplit("-", 1)[1]) if resume else 0),
        1,
    )

    print(
        f"[xong] {buoc} bước · {el/60:.1f} phút · {el/buoc:.1f} s/bước · "
        f"đỉnh VRAM {torch.cuda.max_memory_allocated()/2**30:.2f} GiB · "
        f"SPICE {STAT['t']/max(STAT['n'], 1):.1f} s/lần",
        flush=True,
    )

    trainer.save_model(os.path.join(a.out, "final"))
    json.dump(
        trainer.state.log_history,
        open(os.path.join(a.out, "log_history.json"), "w"),
        indent=1,
    )


def main():
    ap = argparse.ArgumentParser()

    for f in ("--selftest", "--merge", "--gen", "--probe", "--train"):
        ap.add_argument(f, action="store_true")

    ap.add_argument("--bundle", required=True)
    ap.add_argument("--merged", default="/kaggle/working/s1_merged")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--c1")
    ap.add_argument("--ckpt")
    ap.add_argument("--out")
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--n-prompt", type=int, default=N_PROMPT)
    ap.add_argument("--G", type=int, default=8)
    ap.add_argument("--bs", type=int, default=8)
    ap.add_argument("--accum", type=int, default=2)
    ap.add_argument("--beta", type=float, default=0.04)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--max-steps", type=int, default=500)
    ap.add_argument("--resume", default=None)
    ap.add_argument("--no-q4", dest="q4", action="store_false")

    a = ap.parse_args()
    a.adapter = a.adapter or os.path.join(a.bundle, "adapter_s1_seed101")

    if a.selftest:
        selftest(a)
    elif a.merge:
        merge(a)
    elif a.gen:
        assert a.c1 and a.out, "cần --c1 và --out"
        gen(a)
    elif a.probe or a.train:
        assert a.out, "cần --out"
        train(a)
    else:
        ap.error("chọn một chế độ")


if __name__ == "__main__":
    main()
```

# Phụ lục B — đọc kết quả trên máy nhà (CPU + Java)

Đặt các tệp Pha 3 vào `/mnt/d/Master/Thesis/runs/grpo_spice/`. Chạy bằng `~/.venvs/thesis/bin/python` (có `pycocoevalcap`), Java 8 ở `~/.jdk/jdk8u504-b01`.

```python
import json, os, random, re, sys
from pathlib import Path

JH = os.path.expanduser("~/.jdk/jdk8u504-b01")
os.environ["JAVA_HOME"] = JH
os.environ["PATH"] = JH + "/bin:" + os.environ["PATH"]

from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.spice.spice import Spice

T = Path("/mnt/d/Master/Thesis")
C1 = [json.loads(l) for l in open(
    T / "runs/c1/c1_mau.jsonl",
    encoding="utf-8",
)]
# greedy S1 chấm lại trong cùng phiên Pha 3 (cùng dụng cụ); chưa có thì lùi về bản của 251
K0P = T / "runs/grpo_spice/score_k0_lai_raw.jsonl"
if not K0P.exists():
    K0P = T / "runs/c1/exec8/c1score/score_k0_raw.jsonl"
K0 = {
    (o["episode_id"], o["step_id"]): o
    for o in map(json.loads, open(K0P, encoding="utf-8"))
}
EX_S1 = 100 * sum(int(o["executable"]) for o in K0.values()) / len(K0)
print(f"mốc S1: {K0P.name} · {len(K0)} bước · exec {EX_S1:.2f} (251: 63.45)")

E = T / "runs/grpo_spice"
W = re.compile(r"[A-Za-z0-9'-]+")
keys = [(d["episode_id"], d["step_id"]) for d in C1]

tk = PTBTokenizer()
g = tk.tokenize({i: [{"caption": d["gold"]}] for i, d in enumerate(C1)})


def spice(sents):
    c = tk.tokenize({i: [{"caption": s or "none"}] for i, s in enumerate(sents)})
    _, sc = Spice().compute_score(g, c)
    return [x["All"]["f"] for x in sc]


sp_s1 = spice([d["greedy"] for d in C1])
eps = sorted({k[0] for k in keys})


def boot(diff, ks):
    th = {e: [k for k in ks if k[0] == e] for e in {k[0] for k in ks}}
    E_ = sorted(th)
    rng = random.Random(101)
    ds = []

    for _ in range(10000):
        qs = [k for e in (rng.choice(E_) for _ in E_) for k in th[e]]
        ds.append(100 * sum(diff[k] for k in qs) / len(qs))

    ds.sort()
    return round(ds[249], 2), round(ds[9749], 2)


for s in (250, 500):
    P = {
        (d["episode_id"], d["step_id"]): d["pred"]
        for d in map(
            json.loads,
            open(E / f"pred_ck{s}.jsonl", encoding="utf-8"),
        )
    }
    assert set(P) == set(keys)

    sp = spice([P[k] for k in keys])
    dsp = {k: sp[i] - sp_s1[i] for i, k in enumerate(keys)}

    R = {
        (o["episode_id"], o["step_id"]): o
        for o in map(
            json.loads,
            open(E / f"score_ck{s}_raw.jsonl", encoding="utf-8"),
        )
    }

    tap = [k for k in keys if k in K0]
    assert len(tap) == 249 and set(R) == set(tap)

    dex = {
        k: int(R[k]["executable"]) - int(K0[k]["executable"])
        for k in tap
    }
    ex = 100 * sum(int(R[k]["executable"]) for k in tap) / 249

    words = sum(len(W.findall(P[k])) for k in keys) / 400
    words_s1 = sum(len(W.findall(d["greedy"])) for d in C1) / 400

    print(
        f"ck{s}: SPICE {100*sum(sp)/400:.2f} "
        f"(S1 {100*sum(sp_s1)/400:.2f}, Δ {100*sum(dsp.values())/400:+.2f}, KTC {boot(dsp, keys)})"
        f" · exec {ex:.2f} (S1 {EX_S1:.2f}, Δ {ex-EX_S1:+.2f}, KTC {boot(dex, tap)})"
        f" · cứu {sum(v == 1 for v in dex.values())} phá {sum(v == -1 for v in dex.values())}"
        f" · số từ {words:.2f} (S1 {words_s1:.2f}) · rỗng {sum(not P[k] for k in keys)}"
        f" · trùng câu S1 {sum(P[k] == C1[i]['greedy'] for i, k in enumerate(keys))}/400"
    )
```

Kỳ vọng kiểm đường: S1 SPICE in ra **57,30**. Không ra 57,30 thì đường chấm lệch, dừng trước khi đọc số GRPO.
