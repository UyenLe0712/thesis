# Pha 2 GRPO SPICE — chạy bằng commit Kaggle, nối 3 lượt (29/9/2026)

Runbook cho Pha 2 của `harness/tai_lieu_2026-09-29/253_ACTION_GRPO_SPICE_S1_29_9_checked.md`.
Thiết kế lượt train giữ nguyên như 253 §1. Hai chỗ đổi so với bản 253 là cách lưu và cách chạy tiếp,
không đổi thuật toán.

**Vì sao phải nối lượt:** thăm dò T4 đo **160,6 s/bước** (trên 50 câu nhắc dài nhất), đỉnh VRAM
13,22 GiB. 500 bước ≈ 22,3 h, trong khi một commit Kaggle bị cắt ở 12 h. User chọn 29/9: T4, 0 đồng,
nối ba commit.

**Hai sửa trong `grpo_spice.py` (29/9, md5 mới `d99d03c0c01718283e84ac3851ef5591`):**
1. `save_steps` 50 → **25**. Mỗi lần nối lượt mất tối đa 24 bước (~1 h) thay vì 49 bước (~2 h).
   `checkpoint-250` và `checkpoint-500` vẫn có cho Pha 3.
2. `--resume auto` chỉ nhận điểm lưu có đủ `trainer_state.json`, `optimizer.pt` và
   `adapter_model.safetensors`. Nếu tiến trình bị dừng đúng lúc đang lưu thì thư mục dở bị bỏ qua.
   Nếu có điểm lưu mà không cái nào đủ tệp thì script **dừng**, không lặng lẽ train lại từ bước 0.

## ⛔ SỰ CỐ 30/9 — commit 2 chạy tiếp SAI, đã sửa mã (md5 `d99d03c0c01718283e84ac3851ef5591`)

Commit 2 in `[tiếp từ] …/checkpoint-250` và đếm bước tiếp từ 250, nhưng `kl` tụt từ ~0,012 (cuối
commit 1) xuống ~0,001 rồi tăng lại từ đầu. Nguyên nhân đọc từ mã transformers (`trainer.py`
`_load_from_checkpoint`, nhánh `adapter_subdirs`, bản 5.14.1): điểm lưu có thư mục con `ref/` (adapter
tham chiếu KL do TRL tự tạo) thì trainer **chỉ nạp thư mục con**, **không nạp adapter `default` ở gốc**
⇒ policy quay về S1 (LoRA B = 0) mà không có lỗi nào. Optimizer, lịch lr và số bước thì vẫn nạp.
⇒ **`checkpoint-250` của commit 1 dùng được** (250 bước liền mạch từ S1). **Mọi điểm lưu 275–500 của
commit 2 KHÔNG phải mô hình 500 bước theo thiết kế**, cấm chấm như `checkpoint-500`.

Sửa: sau dòng `[tiếp từ]`, script tự nạp `adapter_model.safetensors` ở gốc vào adapter `default`, in
`[nạp default] … |lora_B| 0.0000 → x` và **dừng** nếu x = 0. Chạy tiếp đúng thì:
- dòng `[nạp default]` có x > 0;
- `kl TB` ở mấy bước đầu phải xấp xỉ mức cuối lượt trước (~0,01), **không** về ~0.

Chạy lại đoạn 250 → 500: gắn **Output commit 1** (không phải commit 2), New Version dataset
`grpo-spice-script` bằng bản sửa, rồi làm như bước 5. 250 bước × ~150 s ≈ 10,5 h + ~0,5 h dựng ⇒ chạm
mốc 11 h quanh bước ~490, lưu cuối 475 ⇒ cần thêm một commit ngắn (~1 h) cho 475 → 500.

### Thứ tự làm sau sự cố (chốt 30/9)

1. Cancel commit 2 (Output của nó không hợp lệ, cancel để tiết kiệm ~4 h hạn mức).
2. Tab *Output* của commit 1: `grpo_spice/checkpoint-250/` phải có thư mục con `ref/`, xác nhận chẩn đoán.
3. New Version dataset `grpo-spice-script` bằng `_bundles/grpo-spice-script/` (md5 mới).
4. **Pha 3 chỉ cho `checkpoint-250`** (253 §6, với hai chỗ sửa: vòng P3-A `for s in (250,)`, vòng
   P3-C bỏ dòng `ck500`). Input gắn **Output commit 1**. `PeftModel.from_pretrained` ở `--gen` nạp
   adapter gốc nên không dính lỗi chạy tiếp.
5. Có số của `checkpoint-250` rồi mới quyết có chạy lại 250 → 500 (~12 h hạn mức) hay không.

## ⚠️ SỰ CỐ 30/9 tối — lượt chạy lại 250 → 500 OOM ở bước ~443, điểm lưu cuối `checkpoint-425`

Log: `torch.OutOfMemoryError … Tried to allocate 536.00 MiB … 14.10 GiB in use` trong
`sdpa_attention_forward`, lúc 7,71 h. Trước đó 20 bước gần nhất: thưởng TB 0,537 · kl TB 0,0301 ·
rỗng 0. Ô 4 không assert mã thoát nên notebook vẫn kết thúc bình thường và Output được lưu.

Mảnh 536 MiB khớp cỡ ma trận attention của **một micro-batch 4 chuỗi** dài ~2.000 token (câu nhắc có
ảnh nặng), không khớp khâu sinh 16 chuỗi cùng lúc (sẽ ~2 GiB) [suy]. Chạy tiếp nguyên cấu hình thì
dữ liệu và RNG nạp lại từ điểm lưu, nhiều khả năng OOM lại đúng lô đó ⇒ **commit nối 425 → 500 đổi
`--bs 4 --accum 4` thành `--bs 2 --accum 8`**:
- `generation_batch_size` vẫn 16 = 2 câu nhắc × 8, `loss_type` là `dapo` (chuẩn hoá theo tổng token
  của cả lô tích luỹ) ⇒ cùng một bước cập nhật, chỉ chia nhỏ forward/backward. Không đổi thuật toán.
- Bộ lấy mẫu lặp mỗi lô `steps_per_generation` lần, nên bỏ qua 425 × 8 micro-batch vẫn đúng 425 nhóm
  câu nhắc như cấu hình cũ.
- Kiểm ở log: dòng `GRPOConfig:` phải có `per_device_train_batch_size': 2`, `gradient_accumulation_steps': 8`,
  `generation_batch_size': 16`; dòng `[lô] mỗi lượt sinh 16 câu = 2 câu nhắc × 8`.
- Chậm hơn một chút vì micro-batch nhỏ [chưa đo]. 75 bước × ~150–180 s ≈ 3,1–3,8 h.
- Phải khai khi báo: bước 426–500 chạy ở micro-batch 2 (tương đương về toán, lệch số học fp16).

### Lần 2 (1/10): `--bs 2 --accum 8` vẫn OOM ở bước ~443, cùng mảnh 536 MiB

Micro-batch giảm một nửa mà mảnh cấp phát **không đổi** ⇒ phép tràn không chạy theo micro-batch
(forward train và tính logp đều chia theo `per_device_train_batch_size`, `grpo_trainer.py:1746`).
Còn lại khâu sinh: TRL 0.29.1 gọi `generate` **một lần cho cả 16 chuỗi** (`grpo_trainer.py:1330`) [suy,
chưa thấy đầu traceback]. Lô cố định ⇒ OOM lặp lại đúng bước.
⛔ Không dùng `steps_per_generation=4` để sinh 8 câu/lần: DAPO chuẩn hoá theo số token của **một lượt
sinh** (`:1616`, `:2238`) nên hai lượt 8 câu cộng lại cho gradient ~2 lần so với một lượt 16 câu, tức
đổi thuật toán.
✅ Sửa: cờ mới **`--gen-chunk 8`** (md5 `07ea87b6d156d1faa391a4274dffd7cf`) bọc `model.generate`, sinh
từng khúc ≤ 8 chuỗi (tách `pixel_values` theo `image_grid_thw`), đệm phải bằng `pad_token_id` rồi ghép
lại. TRL vẫn nhận 16 chuỗi trong một lần gọi ⇒ lô cập nhật, sampler, chuẩn hoá DAPO không đổi. Kiểm
CPU bằng mô hình giả 16 chuỗi, ảnh khác cỡ: kết quả ghép trùng tuyệt đối bản sinh một lần.
Log phải có `[sinh theo khúc] bật …` rồi `[sinh theo khúc] 16 chuỗi → 2 khúc ≤ 8`.

#### Ô 4 cho commit nối 425 → 500 (1/10, hạn mức còn 3h59m)

Input: chỉ Output của version OOM lần 2 + ba dataset (script bản `07ea87b6…`).

```python
import subprocess, time, os, shutil, glob

log = open(f"{W}/train.log", "a")
cmd = ["python", "grpo_spice.py", "--train", "--no-q4", "--bs", "2", "--accum", "8", "--gen-chunk", "8",
       "--bundle", BUNDLE, "--merged", MERGED, "--out", OUT, "--resume", "auto"]
p = subprocess.Popen(cmd, cwd=W, stdout=log, stderr=subprocess.STDOUT, text=True,
    env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
         "PYTORCH_ALLOC_CONF": "expandable_segments:True",
         "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"})

import ast, re, statistics as st
TONG, CAT = 500, int(3600 * 3.6)    # hạn mức còn 3h59m (1/10) ⇒ dừng ở 3,6 h, chừa ~0,4 h để lưu Output

def ck_moi():
    c = sorted(glob.glob(f"{OUT}/checkpoint-*"), key=lambda s: int(s.rsplit("-", 1)[1]))
    return os.path.basename(c[-1]) if c else "chưa có"

def tinh_trang():
    L = open(f"{W}/train.log", encoding="utf-8", errors="ignore").read().splitlines()
    tiep = [l for l in L if l.startswith("[tiếp từ]")]
    goc = int(re.findall(r"checkpoint-(\d+)", tiep[-1])[0]) if tiep and "checkpoint-" in tiep[-1] else 0
    D = []
    for l in L:
        if l.startswith("{'loss'"):
            try: D.append({k: float(v) for k, v in ast.literal_eval(l).items() if re.match(r"^[-\d.e+na]+$", str(v))})
            except Exception: pass
    sp = [l for l in L if l.startswith("[spice]")][-20:]
    thuong = [float(re.search(r"thưởng TB (-?[\d.]+)", l).group(1)) for l in sp]
    tu = [float(re.search(r"số từ TB ([\d.]+)", l).group(1)) for l in sp]
    rong = sum(int(re.search(r"rỗng (\d+)", l).group(1)) for l in sp)
    buoc = goc + len(D)
    msg = f"{(time.time()-T_NB)/3600:5.2f} h · bước {buoc}/{TONG} (tiếp từ {goc}) · lưu cuối {ck_moi()}"
    nd = [l for l in L if l.startswith("[nạp default]")]
    if nd: msg += f"\n      {nd[-1][:90]}"
    if any(l.startswith("[sinh theo khúc] 16") for l in L): msg += "\n      sinh theo khúc: ĐANG CHẠY (16 → 2 khúc)"
    elif any(l.startswith("[sinh theo khúc] bật") for l in L): msg += "\n      sinh theo khúc: đã bật, chưa sinh lần nào"
    else: msg += "\n      ⚠️ chưa thấy dòng [sinh theo khúc] — kiểm md5 / cờ --gen-chunk"
    if D:
        t_tr = time.time() - T_TRAIN
        spb = t_tr / len(D)                                   # s/bước lượt này (gồm cả nạp mô hình, hơi bi quan)
        con_tong = (TONG - buoc) * spb / 3600
        dung_o = min(TONG, buoc + int(max(0, CAT - (time.time() - T_NB)) / spb))
        g0 = sum(d.get("grad_norm", 1) < 1e-3 for d in D[-20:])
        kl = [d["kl"] for d in D[-20:] if "kl" in d]
        msg += (f"\n      {spb:.0f} s/bước · còn ~{con_tong:.1f} h tới 500 · commit này dừng quanh bước {dung_o}"
                f"\n      20 bước gần nhất: thưởng TB {st.mean(thuong):.3f} · số từ TB {st.mean(tu):.1f} · rỗng {rong} · "
                f"bước grad≈0 {g0}/20 · kl TB {st.mean(kl) if kl else float('nan'):.4f}")
        if any(v != v for d in D[-5:] for v in d.values()): msg += "\n      ⚠️ có nan trong 5 bước cuối"
    if any("Traceback" in l or "OutOfMemory" in l for l in L[-80:]): msg += "\n      ⚠️ có Traceback/OOM ở cuối log"
    return msg

T_TRAIN = time.time()
while p.poll() is None:
    time.sleep(120)
    print(tinh_trang(), flush=True)
    if time.time() - T_NB > CAT and p.poll() is None:
        print(f"⛔ đã {CAT/3600:.1f} h từ đầu notebook, dừng để Output kịp lưu", flush=True)
        p.terminate(); p.wait()

print("mã thoát", p.returncode, "· điểm lưu cuối", ck_moi())
print("\n".join(open(f"{W}/train.log", encoding="utf-8", errors="ignore").read().splitlines()[-40:]))
shutil.rmtree(MERGED, ignore_errors=True)   # bỏ bản hoà ~7 GB khỏi Output
```

## Dự kiến

| commit | từ bước | tới bước (điểm lưu cuối) | giờ GPU |
|---|---|---|---|
| 1 | 0 | ~225 | ~11 h |
| 2 | 225 | ~450 | ~11 h |
| 3 | 450 | **500** | ~2,5–3 h |

Tổng ≈ **25 h** hạn mức, cộng Pha 3 ~2,5 h. Trước commit 1, xem còn bao nhiêu giờ GPU trong tuần
(kaggle.com → ảnh đại diện → *Settings* → mục *Quota*). Không đủ cho commit 3 thì để commit 3 sang
tuần sau; điểm lưu nằm yên trong Output nên không mất gì. Lượt thật có thể nhanh hơn thăm dò một chút,
vì thăm dò dùng 50 câu nhắc dài nhất.

---

## Bước 1 — trên máy nhà: dựng lại thư mục upload

Đã dựng sẵn 29/9 ở `_bundles/grpo-spice-script/` (gồm `grpo_spice.py` bản mới và
`build_branch_data.py`). Muốn dựng lại thì chạy:

```bash
cd /d/Master/Thesis
cp harness/grpo_spice.py harness/build_branch_data.py _bundles/grpo-spice-script/
md5sum _bundles/grpo-spice-script/*
# grpo_spice.py        d99d03c0c01718283e84ac3851ef5591
# build_branch_data.py 619e63e123a6dbf60086e65ee94a3912
```

## Bước 2 — trên Kaggle: cập nhật dataset `grpo-spice-script`

1. Vào kaggle.com → *Your Work* → *Datasets* → `grpo-spice-script`.
2. Bấm **New Version** (góc phải). Xoá `grpo_spice.py` cũ, kéo thả hai tệp trong
   `_bundles/grpo-spice-script/` vào.
3. Ô *Version notes* ghi `save_steps 25 + resume an toan`. Bấm **Create** rồi đợi trạng thái xong
   (khoảng một phút).

## Bước 3 — tạo notebook commit 1

1. *Create* → *New Notebook*. Đặt tên dễ nhận, ví dụ `grpo-spice-train`.
2. Cột phải → *Session options*:
   - **Accelerator: GPU T4 ×2**. Script chỉ dùng GPU 0, xem 253 §3.
   - **Internet: On**. Cần để tải Qwen và Stanford CoreNLP.
   - *Persistence*: để mặc định.
3. *Add Input* → *Datasets* → gắn đủ ba dataset:
   - `fgrb-p1-bundle`
   - `c1-exec8`
   - `grpo-spice-script` (**phiên bản mới nhất**)

   ⛔ Chưa gắn `thesis-val-cham`, dataset đó chỉ dùng ở Pha 3.
4. Xoá ô mẫu, dán **bốn ô** dưới đây theo đúng thứ tự.

### Ô 1 — gói, Java và mốc giờ

```python
import subprocess, sys, os, time
T_NB = time.time()                         # mốc đầu notebook, ô train dùng để dừng trước trần 12 h
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode

sh("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless")
sh("update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java")
sh("java -version")
sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes pycocoevalcap 'trl==0.29.1' 2>&1 | tail -3")
sh(f'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.get_device_name(0))"')
```

### Ô 2 — đường dẫn và md5

```python
import os, glob, shutil, hashlib

W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "images" in d)
C1 = glob.glob("/kaggle/input/**/c1_mau.jsonl", recursive=True); assert len(C1) == 1, C1; C1 = C1[0]
assert md5(C1) == "d757554326977309c3a65ae0b144c211", "DỪNG: c1_mau.jsonl lệch bản máy nhà"
# Output của commit trước (gắn làm input ở commit 2, 3) cũng có grpo_spice.py cạnh train.log ⇒ loại ra
SRC = [p for p in glob.glob("/kaggle/input/**/grpo_spice.py", recursive=True)
       if not os.path.exists(os.path.join(os.path.dirname(p), "train.log"))]
assert len(SRC) == 1, f"DỪNG: cần đúng một grpo_spice.py của dataset grpo-spice-script, thấy {SRC}"
for f in ("grpo_spice.py", "build_branch_data.py"):
    shutil.copy(os.path.join(os.path.dirname(SRC[0]), f), f"{W}/{f}")
assert md5(f"{W}/grpo_spice.py") == "07ea87b6d156d1faa391a4274dffd7cf", "DỪNG: grpo_spice.py trên Kaggle là bản cũ, New Version lại dataset"
assert md5(f"{W}/build_branch_data.py") == "619e63e123a6dbf60086e65ee94a3912", "DỪNG: build_branch_data.py lệch bản máy nhà"
MERGED = f"{W}/s1_merged"; OUT = f"{W}/grpo_spice"
os.makedirs(OUT, exist_ok=True)

# commit 2, 3: chép điểm lưu từ Output commit trước (commit 1 không có gì để chép)
ck = [p for p in glob.glob("/kaggle/input/**/grpo_spice/checkpoint-*", recursive=True) if os.path.isdir(p)]
for p in ck:
    shutil.copytree(p, os.path.join(OUT, os.path.basename(p)), dirs_exist_ok=True)
print("điểm lưu đã chép:", sorted((os.path.basename(p) for p in ck), key=lambda s: int(s.split("-")[1]))[-4:])
print("BUNDLE:", BUNDLE, "\nC1:", C1, "\nSRC:", SRC[0], "\nmd5 khớp", flush=True)
```

### Ô 3 — hoà S1

```python
r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED],
                   cwd=W, capture_output=True, text=True)
print((r.stdout + r.stderr)[-2000:]); assert r.returncode == 0, "DỪNG: hoà lỗi"
```

### Ô 4 — train, tự dừng ở 11 h tính từ đầu notebook

```python
import subprocess, time, os, shutil, glob

log = open(f"{W}/train.log", "a")
cmd = ["python", "grpo_spice.py", "--train", "--no-q4", "--bs", "4", "--accum", "4",
       "--bundle", BUNDLE, "--merged", MERGED, "--out", OUT, "--resume", "auto"]
p = subprocess.Popen(cmd, cwd=W, stdout=log, stderr=subprocess.STDOUT, text=True,
    env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
         "PYTORCH_ALLOC_CONF": "expandable_segments:True",
         "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"})

import ast, re, statistics as st
TONG, CAT = 500, 3600 * 11

def ck_moi():
    c = sorted(glob.glob(f"{OUT}/checkpoint-*"), key=lambda s: int(s.rsplit("-", 1)[1]))
    return os.path.basename(c[-1]) if c else "chưa có"

def tinh_trang():
    L = open(f"{W}/train.log", encoding="utf-8", errors="ignore").read().splitlines()
    tiep = [l for l in L if l.startswith("[tiếp từ]")]
    goc = int(re.findall(r"checkpoint-(\d+)", tiep[-1])[0]) if tiep and "checkpoint-" in tiep[-1] else 0
    D = []
    for l in L:
        if l.startswith("{'loss'"):
            try: D.append({k: float(v) for k, v in ast.literal_eval(l).items() if re.match(r"^[-\d.e+na]+$", str(v))})
            except Exception: pass
    sp = [l for l in L if l.startswith("[spice]")][-20:]
    thuong = [float(re.search(r"thưởng TB (-?[\d.]+)", l).group(1)) for l in sp]
    tu = [float(re.search(r"số từ TB ([\d.]+)", l).group(1)) for l in sp]
    rong = sum(int(re.search(r"rỗng (\d+)", l).group(1)) for l in sp)
    buoc = goc + len(D)
    msg = f"{(time.time()-T_NB)/3600:5.2f} h · bước {buoc}/{TONG} (tiếp từ {goc}) · lưu cuối {ck_moi()}"
    if D:
        t_tr = time.time() - T_TRAIN
        spb = t_tr / len(D)                                   # s/bước lượt này (gồm cả nạp mô hình, hơi bi quan)
        con_tong = (TONG - buoc) * spb / 3600
        dung_o = min(TONG, buoc + int(max(0, CAT - (time.time() - T_NB)) / spb))
        g0 = sum(d.get("grad_norm", 1) < 1e-3 for d in D[-20:])
        kl = [d["kl"] for d in D[-20:] if "kl" in d]
        msg += (f"\n      {spb:.0f} s/bước · còn ~{con_tong:.1f} h tới 500 · commit này dừng quanh bước {dung_o}"
                f"\n      20 bước gần nhất: thưởng TB {st.mean(thuong):.3f} · số từ TB {st.mean(tu):.1f} · rỗng {rong} · "
                f"bước grad≈0 {g0}/20 · kl TB {st.mean(kl) if kl else float('nan'):.4f}")
        if any(v != v for d in D[-5:] for v in d.values()): msg += "\n      ⚠️ có nan trong 5 bước cuối"
    if any("Traceback" in l or "OutOfMemory" in l for l in L[-80:]): msg += "\n      ⚠️ có Traceback/OOM ở cuối log"
    return msg

T_TRAIN = time.time()
while p.poll() is None:
    time.sleep(120)
    print(tinh_trang(), flush=True)
    if time.time() - T_NB > CAT and p.poll() is None:
        print("⛔ đã 11 h từ đầu notebook, dừng để Output kịp lưu", flush=True)
        p.terminate(); p.wait()

print("mã thoát", p.returncode, "· điểm lưu cuối", ck_moi())
print("\n".join(open(f"{W}/train.log", encoding="utf-8", errors="ignore").read().splitlines()[-40:]))
shutil.rmtree(MERGED, ignore_errors=True)   # bỏ bản hoà ~7 GB khỏi Output
```

5. Bấm **Save Version** (góc phải) → chọn **Save & Run All (Commit)** → *Save*. Tắt máy đi ngủ được.

### Xem tiến độ khi đang chạy

Kaggle → *Your Work* → *Code* → notebook này → bấm version đang chạy (*Running*) → phần *Logs*.
Ô 4 in ba dòng mỗi 2 phút, ví dụ:

```
 2.00 h · bước 202/500 (tiếp từ 200) · lưu cuối checkpoint-225
      160 s/bước · còn ~13.2 h tới 500 · commit này dừng quanh bước 404
      20 bước gần nhất: thưởng TB 0.52 · số từ TB 8.4 · rỗng 0 · bước grad≈0 3/20 · kl TB 0.0030
```

`s/bước` tính cả phút nạp mô hình nên ở đầu lượt hơi cao, sau khoảng 30 phút thì ổn định.

| chỉ số (20 bước gần nhất) | ổn | báo về (chưa cần dừng) | dừng ngay |
|---|---|---|---|
| s/bước | 120–170 | > 200 | - |
| thưởng TB | dao động 0,3–0,8, nhích lên dần qua hàng trăm bước | giảm đều qua > 100 bước | - |
| số từ TB | 5–12 | < 4 (câu co lại để ăn thưởng) hoặc > 15 | - |
| rỗng | 0–2 | ≥ 5 | - |
| bước grad≈0 | ≤ 5/20 | > 10/20 (đa số nhóm hoà thưởng, gần như không học) | - |
| kl TB | < 0,1, tăng chậm | > 0,3 | - |
| ⚠️ nan / Traceback / OOM | không có | - | *Cancel*, gửi log |

Thưởng lên xuống mạnh giữa hai lần in là **bình thường**, vì mỗi bước chỉ có 2 câu nhắc. Chỉ đọc xu
hướng qua vài trăm bước. Và đây mới là thưởng lúc train, **không** phải kết quả: kết quả chỉ có sau
Pha 3 (SPICE, `exec` trên val).

### Kiểm trong 15 phút đầu (mở version đang chạy → tab *Logs*)

- Ô 2 in `md5 khớp` và `điểm lưu đã chép: []` (vì commit 1 chưa có gì).
- Ô 4, dòng đầu tiên có `[tiếp từ] None`.
- Sau khoảng 4 phút đã có dòng `[spice] lần 1`.
- Không có dòng nào báo `⚠️ thấy Traceback`.

Nếu có lỗi thì *Cancel* ngay và gửi log về. Đừng để chạy tiếp tốn giờ.

## Bước 4 — commit 1 xong (~11 h)

Mở version vừa chạy xong. Cuối log phải thấy `⛔ đã 11 h …`, rồi `mã thoát …` và
`điểm lưu cuối checkpoint-2xx`. Tab *Output* phải có `grpo_spice/checkpoint-25` … `checkpoint-2xx`.

## Bước 5 — commit 2

1. Mở lại notebook (*Edit*).
2. *Add Input* → mục **Notebook Output Files** (hoặc tab *Your Work*) → chọn **chính notebook này,
   version commit 1**.
3. **Không sửa ô nào.** Ô 2 tự chép điểm lưu về, và `--resume auto` tự lấy điểm lưu cuối đủ tệp.
4. **Save Version → Save & Run All**.

Kiểm trong 15 phút đầu:
- Ô 2 in `điểm lưu đã chép: [..., 'checkpoint-2xx']`.
- Ô 4 có dòng `[tiếp từ] /kaggle/working/grpo_spice/checkpoint-2xx`.
- ⛔ Nếu dòng đó là `[tiếp từ] None` thì lượt đang train lại từ bước 0. *Cancel* ngay.

## Bước 6 — commit 3

Làm như bước 5, nhưng **bỏ input Output commit 1, chỉ gắn Output commit 2**. Output commit 2 đã chứa
đủ mọi điểm lưu từ 25 trở đi. Commit 3 chạy tới 500 thì dừng tự nhiên, không cần tới mốc 11 h. Cuối
log phải có:

```
[xong] ~50 bước · … s/bước · đỉnh VRAM … GiB · SPICE … s/lần
mã thoát 0 · điểm lưu cuối checkpoint-500
```

và Output có `grpo_spice/final/` cùng `grpo_spice/log_history.json`.

## Bước 7 — mang kết quả về

Từ Output commit 3, tải về máy nhà và đặt thẳng vào `runs/grpo_spice/` (theo luật đọc kết quả):
- `grpo_spice/checkpoint-250/`
- `grpo_spice/checkpoint-500/`
- `grpo_spice/log_history.json`
- `train.log` của **cả ba** commit, đổi tên thành `train_c1.log`, `train_c2.log`, `train_c3.log`

Rồi sang Pha 3 (253 §6), chấm val trên hai điểm lưu 250 và 500.

## Nếu có trục trặc

| thấy gì | làm gì |
|---|---|
| Ô 2 báo `grpo_spice.py trên Kaggle là bản cũ` | New Version lại dataset (bước 2), rồi đổi input sang phiên bản mới nhất |
| `OOM` trong log | Gửi log về. Thăm dò đỉnh 13,22 GiB, nhưng câu nhắc thật có thể dài hơn ở vài bước |
| `DỪNG: có n điểm lưu mà không cái nào đủ tệp` | Gửi về danh sách tệp trong một thư mục `checkpoint-*` của Output (có thể tên tệp adapter khác dự kiến) |
| `loss` nan | *Cancel*, gửi log. Không chạy tiếp |
| commit bị Kaggle cắt ở 12 h mà không có dòng `⛔ đã 11 h` | Output có thể mất. Gửi log về trước khi làm gì khác |
