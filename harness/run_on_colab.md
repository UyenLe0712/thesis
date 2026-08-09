# Chạy trên Colab Pro — runbook dán-là-chạy

> Thay cho `run_on_rented.sh` (bản đó cho máy thuê có SSH). Cùng một trình tự, cùng một
> luật, chỉ khác cách gõ lệnh.
>
> **Máy đã đo được (9/8/2026):** A100 **80 GB** · đĩa 235,7 GB (trống ~148) ·
> local-scratch **368 GB** chưa dùng · RAM 167 GB · đốt **6,77 đơn vị/giờ**.
>
> **Nguyên tắc xuyên suốt: đồng hồ chạy là tiền chạy.** Mọi thứ nghĩ được trước thì nghĩ
> trước, đừng nghĩ lúc máy đang bật. Vì vậy runbook này chia theo PHIÊN, mỗi phiên có
> đúng một việc và một điều kiện kết thúc.

---

## 0. Trước khi bật máy

**Mua đơn vị điện toán.** Cần ước chừng **560-840 đơn vị** cho trọn kế hoạch
(82-124 giờ × 6,77). Mua dư một ít, vì hết units giữa lượt train là mất phiên.

**Chuẩn bị Drive.** Tạo thư mục `MyDrive/thesis/`. Đây là chỗ duy nhất tồn tại qua các
phiên — mọi thứ trong `/content` biến mất khi phiên chết.

**Tải lên Drive:** `thesis_rented.zip` (3,3 MB — mã, cấu hình, tập kiểm đã OCR + nhãn
khai báo). Đặt ở `MyDrive/thesis/`.

**Bật A100:** Runtime → Change runtime type → A100. Kiểm lại **mỗi phiên**, Colab hay
tụt về L4 nếu không để ý.

---

## PHIÊN 0 — dựng dữ liệu (một lần, ~4-5 giờ)

Phiên này **không dùng tới card**, toàn CPU. Nhưng vẫn phải bật A100 vì các phiên sau
cần cùng một môi trường, và tách ra chạy máy CPU không tiết kiệm được bao nhiêu
(~20 đơn vị ≈ 2 đô).

### Ô 1 — nhận diện máy, ghi lại

```python
import os, subprocess, torch
print("lõi CPU:", os.cpu_count())
print(subprocess.run(["nvidia-smi","--query-gpu=name,memory.total","--format=csv,noheader"],
                     capture_output=True, text=True).stdout.strip())
print("số card:", torch.cuda.device_count())
print(subprocess.run(["df","-h"], capture_output=True, text=True).stdout)
```

**Ba điều kiện, sai một là dừng:**

| | |
|---|---|
| số card | phải là **1**. Khác 1 thì `os.environ["CUDA_VISIBLE_DEVICES"]="0"` rồi khởi động lại |
| card | phải là **A100**. Ra L4/T4 thì đổi runtime, đừng train — cỡ lô phải giống nhau qua cả sáu lượt |
| đĩa | chọn phân vùng trống **≥100 GB** làm `WS`. Nếu `local-scratch` gắn ở đâu đó thì ưu tiên nó (NVMe, nhanh hơn) |

### Ô 2 — gắn Drive, bung mã

```python
from google.colab import drive
drive.mount('/content/drive')

import os, zipfile, shutil
D = "/content/drive/MyDrive/thesis"
WS = "/content/ws"                    # ĐỔI nếu ô 1 cho thấy phân vùng khác rộng hơn
os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_rented.zip").extractall(WS)
REPO = f"{WS}/thesis"
os.chdir(REPO)
print(len(os.listdir("harness")), "tệp trong harness")
print("OCR tập kiểm:", sum(1 for _ in open("harness/dg1_cache/test_ac/ocr.jsonl")), "ảnh")
print("nhãn tập kiểm:", sum(1 for _ in open("harness/dg1_cache/test_ac/descriptors.jsonl")))
```

### Ô 3 — cài gói

```python
!pip install -q -U "transformers>=4.49" accelerate peft bitsandbytes datasets \
    huggingface_hub pyarrow pillow rapidocr_onnxruntime pyyaml
!git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory /content/LLaMA-Factory
!pip install -q -e "/content/LLaMA-Factory[torch,metrics]"
```

Cài xong **khởi động lại phiên** (Runtime → Restart session), rồi chạy lại ô 2 (không
cần ô 3). Bỏ qua bước này thì thư viện cũ vẫn nằm trong bộ nhớ.

### Ô 4 — tải ảnh tập dạy (~67 GB)

```python
import os; os.chdir(REPO)
!python harness/build_train_data.py --shards 76
```

Mã đã xoá parquet sau mỗi shard nên đỉnh đĩa ~70 GB thay vì ~134 GB. Chừng 20-40 phút.

### Ô 5 — OCR (khâu lâu nhất)

```python
import os
NP = min(os.cpu_count(), 24)
print("dùng", NP, "tiến trình")
!cd {REPO} && for k in $(seq 0 $(({NP}-1))); do python harness/prep_ocr_train.py --shard $k --nshard {NP} & done; wait
!cd {REPO} && python harness/prep_ocr_train.py --merge
```

Với 12 lõi mất ~2,8 giờ. Mã đã ghim mỗi tiến trình về một luồng — không có chỗ này thì
12 tiến trình × 12 luồng tranh nhau 12 lõi và chậm hơn hẳn.

Chạy được nhiều lần vô hại: ảnh đã có kết quả thì bỏ qua. Phiên chết giữa chừng thì bật
lại và chạy tiếp ô này.

### Ô 6 — nhãn khai báo + dữ liệu bốn nhánh

```python
!cd {REPO} && python harness/descriptor_label_build.py
!cd {REPO} && python harness/build_branch_data.py --img-prefix "{REPO}/harness/dg1_cache/train_ac/"
!cd {REPO} && python harness/build_test_data.py --shards 9
!cd {REPO} && python harness/tag_app_seen.py
```

`build_test_data` chỉ tải ảnh tập kiểm (~3,3 GB); OCR và nhãn của tập kiểm đã có sẵn
trong gói nên không chạy lại.

### Ô 7 — cất phần đắt-dựng-rẻ-lưu lên Drive ⚠️ ĐỪNG BỎ QUA

```python
!cd {REPO} && tar czf {D}/derived.tar.gz \
    harness/dg1_cache/train_ac/ocr.jsonl \
    harness/dg1_cache/train_ac/train.jsonl \
    harness/dg1_cache/train_ac/descriptors.jsonl \
    harness/dg1_cache/train_ac/branches \
    harness/dg1_cache/test_ac/ocr.jsonl \
    harness/dg1_cache/test_ac/test.jsonl \
    harness/dg1_cache/test_ac/descriptors.jsonl
!ls -lh {D}/derived.tar.gz
```

Đây là ~2,8 giờ CPU đóng thành một tệp. Phiên sau mất máy mà không có nó là trả lại
từng ấy giờ cho đúng thứ đã có.

### Ô 8 — cất luôn ảnh lên Drive (tuỳ chọn, nhưng nên)

```python
!cd {REPO}/harness/dg1_cache/train_ac && tar cf {D}/train_images.tar images
!ls -lh {D}/train_images.tar
```

67 GB, Drive 5 TB thì thoải mái. Nén cũng vô ích vì PNG đã nén rồi, nên dùng `tar` trần
cho nhanh. Đổi lại: mỗi phiên sau chỉ cần chép một tệp lớn thay vì tải lại 76 shard —
nhanh hơn và không phụ thuộc HuggingFace.

**Điều kiện kết thúc phiên 0:** `derived.tar.gz` và `train_images.tar` đã nằm trên Drive.

---

## PHIÊN TRAIN — mỗi nhánh × mỗi hạt giống một phiên

### Ô A — khôi phục (chạy đầu mỗi phiên)

```python
from google.colab import drive; drive.mount('/content/drive')
import os, zipfile
D, WS = "/content/drive/MyDrive/thesis", "/content/ws"
os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_rented.zip").extractall(WS)
REPO = f"{WS}/thesis"; os.chdir(REPO)
!tar xzf {D}/derived.tar.gz -C {REPO}
!mkdir -p {REPO}/harness/dg1_cache/train_ac && tar xf {D}/train_images.tar -C {REPO}/harness/dg1_cache/train_ac
!python harness/build_test_data.py --shards 9
import torch, os
print("card:", torch.cuda.get_device_name(0), "| số card:", torch.cuda.device_count())
print("ảnh dạy:", len(os.listdir(f"{REPO}/harness/dg1_cache/train_ac/images")))
```

Rồi cài lại gói (ô 3 của phiên 0) và **khởi động lại phiên**, chạy lại ô A.

### Ô B — sinh cấu hình cho lượt này

```python
import yaml, os
BRANCH, SEED = "s1", 101                      # ĐỔI ĐÚNG HAI DÒNG NÀY, không đổi gì khác
OUT = f"{D}/ckpt/{BRANCH}_seed{SEED}"         # ← trỏ vào DRIVE, không phải /content
os.makedirs(OUT, exist_ok=True)

c = yaml.safe_load(open(f"{REPO}/harness/train_config.yaml", encoding="utf-8"))
c["dataset"]     = f"gui_{BRANCH}"
c["seed"]        = SEED
c["output_dir"]  = OUT
c["dataset_dir"] = f"{REPO}/harness/dg1_cache/train_ac/branches"
yaml.safe_dump(c, open("/content/cfg.yaml","w",encoding="utf-8"),
               allow_unicode=True, sort_keys=False)
print(f"nhánh {BRANCH} · hạt giống {SEED} · cỡ lô "
      f"{c['per_device_train_batch_size']}×{c['gradient_accumulation_steps']} "
      f"= {c['per_device_train_batch_size']*c['gradient_accumulation_steps']}")
```

**`output_dir` phải nằm trên Drive.** Đây là thứ chống mất phiên: LLaMA-Factory lưu điểm
mỗi 200 bước, và vì `resume_from_checkpoint` cố ý bỏ trống nên chạy lại là nó tự dò điểm
gần nhất mà nối tiếp. Để ở `/content` thì phiên chết là mất sạch.

**Cỡ lô hiệu dụng phải in ra đúng 16 ở MỌI lượt.** Khác một lượt là hỏng bảng ablation.

### Ô C — train

```python
!llamafactory-cli train /content/cfg.yaml
```

11-18 giờ. Mở thêm một tab trống và bật script chống ngủ. Phiên chết thì bật lại, chạy
ô A, ô B, ô C — nó tự tiếp từ điểm lưu gần nhất.

### Ô D — sinh câu trên tập kiểm (làm ngay, đừng để phiên sau)

```python
!cd {REPO} && python harness/infer_branch.py \
    --adapter {D}/ckpt/{BRANCH}_seed{SEED} \
    --out {D}/preds/preds_{BRANCH}_seed{SEED}.jsonl
```

Trọng số đang nằm sẵn trong bộ nhớ nên đây là lúc rẻ nhất để làm. ~1-1,5 giờ.

**Lần đầu tiên trong cả chiến dịch, chạy phép tự kiểm trước:**

```python
!cd {REPO} && python harness/infer_branch.py --selftest-batch \
    --adapter {D}/ckpt/{BRANCH}_seed{SEED} --batch 8
```

Rớt là dừng, đừng chấm.

**Điều kiện kết thúc phiên train:** thư mục `ckpt/<nhánh>_seed<hạt giống>` và tệp
`preds_...jsonl` đã nằm trên Drive. Tắt máy ngay, đừng để đồng hồ chạy.

---

## CHẤM ĐIỂM — làm trên Kaggle, MIỄN PHÍ

Đừng chấm trên Colab. Khâu chấm chỉ cần bộ trỏ UGround 2 tỉ tham số, T4 gánh được, và
Kaggle cho 30 giờ mỗi tuần không mất tiền. Một nhánh mất ~5 giờ.

Tải `preds_...jsonl` từ Drive về, gộp với gói `thesis_kaggle_gateA.zip` (đã có 300 ảnh)
hoặc dựng đủ tập kiểm trên Kaggle, rồi:

```
python harness/score_run.py --mode score --grounder uground \
    --preds preds_s1_seed101.jsonl --out score_s1_seed101.json
```

Chấm xong nhớ giữ `score_..._raw.jsonl` — nó lưu toạ độ bộ trỏ từng bước, đổi luật chấm
thì chấm lại từ đó chứ không gọi lại bộ trỏ.

---

## Trình tự cứng — không đảo (report/106 mục 5)

```
1. S1 hạt giống 101      → train + sinh câu   (1 phiên)
2. S1 hạt giống 202      → train + sinh câu   (1 phiên)
3. Chấm cả hai trên Kaggle → MDE THẬT + cỡ nhiễu hạt giống
4. KHOÁ ngưỡng đậu/rớt, ghi vào report/106 kèm ngày
5. Phép thử TRẦN trên S1  (chỉ suy luận, ~2 giờ)
6. S2 hạt giống 101, 202  → train + sinh câu  (2 phiên)
7. S2r, S2-nopoint        → train + sinh câu  (2 phiên)
8. B-infer, mô hình gốc   → chỉ suy luận      (1 phiên)
9. S3-pilot — nếu kịp viết mã hàm phạt lề
```

**Bước 3 và 4 phải xong trước bước 6.** Đảo thì ghi lý do và coi kết quả là thăm dò.

---

## Ba điều tuyệt đối không đổi giữa chừng

1. **Cỡ lô hiệu dụng = 16.** Card 80 GB có thể để `16×1` thay `4×4` cho nhanh gần gấp
   đôi (gradient y hệt về mặt toán học). Nhưng nếu có phiên nào tụt xuống A100 40 GB thì
   `16×1` không chạy nổi, mà đổi giữa chừng là hỏng bảng. **Giữ `4×4`** cho chắc, trừ
   khi bạn chắc chắn mọi phiên đều được 80 GB.
2. **`bf16: true`.** A100 có bf16 thật. Nếu phiên nào ra T4/L4 thì đừng train ở đó.
3. **Hạt giống 101 và 202**, không tự đổi.

---

## Bảng tiền

| khâu | giờ | đơn vị (6,77/giờ) |
|---|---|---|
| phiên 0: dựng dữ liệu + OCR | ~5 | 34 |
| 6 lượt train | 66-108 | 447-731 |
| 7 lượt sinh câu | ~10 | 68 |
| phép thử trần + B-infer + mô hình gốc | ~5 | 34 |
| **tổng** | **86-128** | **583-867** |

Ở $10/100 đơn vị → **$58-87**. Chấm điểm không tính vì chạy trên Kaggle.
