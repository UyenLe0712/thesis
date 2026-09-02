# SPRINT `gui_sel` — sáu lượt train, dán thẳng theo thứ tự

> Nguồn lệnh: **`report/132`** (kế hoạch) · **`report/128` §4** (cấu hình) · skill `soict-paper`.
> Cấu hình: **`harness/train_config_sel.yaml`** — khác `train_config.yaml` đúng **bốn khoá**
> (`cutoff_len` 2560→3072 · `num_train_epochs` 2→1 · `dataset` · `output_dir`).
>
> ⚠️ File này viết cho **Qwen2.5-VL-3B**, KHÔNG phải Qwen3-VL-4B. Quyết định giữ 3B chốt ở
> `report/128` §3, bốn lý do đo được. Đừng đổi backbone giữa chừng.

## Sáu lượt — chạy hết, không cắt

| # | dataset | seed | output_dir | vai trò |
|---|---|---|---|---|
| 1 | `gui_sel` | 101 | `ckpt/gui_sel_seed101` | nhánh chính |
| 2 | `gui_sft_match` | 101 | `ckpt/gui_sft_match_seed101` | đối chứng của Δ_sel |
| 3 | `gui_s1_match` | 101 | `ckpt/gui_s1_match_seed101` | mốc dưới |
| 4 | `gui_sel` | 202 | `ckpt/gui_sel_seed202` | |
| 5 | `gui_sft_match` | 202 | `ckpt/gui_sft_match_seed202` | |
| 6 | `gui_s1_match` | 202 | `ckpt/gui_s1_match_seed202` | |

⛔ **Không hy sinh hạt giống 202.** Đó chính là đòn đã hạ bài FAIR xuống borderline.
Thứ tự hy sinh nếu vỡ lịch: cắt `gui_s1_match` **trước**, hạt giống thứ hai **cuối cùng**.

---

## Ô S1 — cài gói ▸ rồi **Restart runtime**

```python
# ⛔ PHÉP RẺ NHẤT, ĐẶT TRƯỚC MỌI THỨ. Không có nó thì lỗi "no GPU" chỉ nổ ở CUỐI ô S2,
#    tức sau khi đã bung ~31 GB ảnh mất 15–25 phút — và đổi runtime lại xoá sạch.
import torch, sys
assert torch.cuda.is_available(), "⛔ CHƯA BẬT GPU — Runtime ▸ Change runtime type ▸ A100"
print("card:", torch.cuda.get_device_name(0))
```

```bash
%cd /content
!git clone https://github.com/hiyouga/LLaMA-Factory.git
%cd LLaMA-Factory
# ⚠️ PIN đúng SHA đã dùng cho MIN-DESC. Sáu lượt PHẢI cùng một bản: LLaMA-Factory đã
#    chứng minh là đổi hành vi giữa các bản (mất `loss`/`lr` khỏi trainer_log.jsonl).
#    KHÔNG dùng --depth 1: clone nông không checkout được commit chỉ định.
!git checkout c4e09c7cbe18
!pip -q install -e ".[torch,metrics,bitsandbytes,qwen]"
# ⛔ extras [bitsandbytes] KHÔNG phải lúc nào cũng kéo được gói về — đo 2/9: cài xong mà
#    `import bitsandbytes` vẫn thiếu metadata, và lỗi chỉ nổ ở CUỐI lượt train đầu:
#    PackageNotFoundError: No package metadata was found for bitsandbytes>=0.39.0
#    (LLaMA-Factory chỉ kiểm nó ở bước configure_quantization, tức sau khi đã nạp dữ liệu).
!pip -q install bitsandbytes
```

Kiểm ngay, đừng đợi tới lúc train:

```python
import importlib.metadata as md
print("bitsandbytes:", md.version("bitsandbytes"))   # phải ra số, không được ném lỗi
```

▸ **Restart runtime** rồi mới chạy ô sau.

---

## Ô S2 — Drive, kho, dữ liệu

```python
from google.colab import drive; drive.mount('/content/drive')
import os, zipfile, glob, torch, json
D, WS = "/content/drive/MyDrive/thesis", "/content/ws"
os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_rented.zip").extractall(WS)
REPO = f"{WS}/thesis"; os.chdir(REPO)
TR = f"{REPO}/harness/dg1_cache/train_ac"
dem = lambda d: len(os.listdir(d)) if os.path.isdir(d) else 0

# ba nhánh SEL dựng trên WSL ngày 2/9 — KHÔNG dựng lại trên Colab.
# Dựng lại là rủi ro lệch lượt OCR (report/125 §5), mà lỗi đó không có tiếng động.
assert os.path.exists(f"{D}/branches_sel.tar.gz"), "⛔ thiếu branches_sel.tar.gz — xem ô S0"
!tar xzf {D}/branches_sel.tar.gz -C {REPO}

os.makedirs(f"{TR}/images", exist_ok=True)
if dem(f"{TR}/images") >= 64567:
    print("ảnh dạy đã đủ — bỏ qua khâu bung")
else:
    for g in sorted(glob.glob(f"{D}/train_images_p*.tar")):
        !tar xf {g} -C {TR}/images

B = f"{TR}/branches"
print("card    :", torch.cuda.get_device_name(0))
print("lõi CPU :", os.cpu_count())
print("ảnh dạy :", dem(f"{TR}/images"), "← cần 64.567")
for n in ("gui_sel", "gui_sft_match", "gui_s1_match"):
    p = f"{B}/{n}.json"
    print(f"{n:16s}:", len(json.load(open(p))) if os.path.exists(p) else "⛔ THIẾU", "← cần 64.567")
print("dataset_info có:", [k for k in json.load(open(f"{B}/dataset_info.json")) if k.startswith("gui_s")])
```

**Kiểm bốn dòng:** ảnh dạy **64.567** · ba nhánh đều **64.567** · `dataset_info` có đủ ba tên ·
card đúng loại định dùng cho **cả sáu lượt** (không trộn L4 với A100).

### Ô S0 — gói `branches_sel.tar.gz` (chạy MỘT LẦN trên WSL, trước khi lên Colab)

Dựng ba nhánh (nếu chưa có), **bắt buộc kèm `--img-prefix`**:

```bash
cd /mnt/d/Master/Thesis
~/.venvs/thesis/bin/python harness/build_candidates.py --split train --all-steps --max 40
~/.venvs/thesis/bin/python harness/build_sel_data.py  --split train \
    --img-prefix /content/ws/thesis/harness/dg1_cache/train_ac/
```

Rồi đóng gói:

```bash
cd /mnt/d/Master/Thesis
tar czf /tmp/branches_sel.tar.gz \
    harness/dg1_cache/train_ac/branches/gui_sel.json \
    harness/dg1_cache/train_ac/branches/gui_sft_match.json \
    harness/dg1_cache/train_ac/branches/gui_s1_match.json \
    harness/dg1_cache/train_ac/branches/dataset_info.json
ls -lh /tmp/branches_sel.tar.gz     # rồi tải lên MyDrive/thesis/
```

---

## Ô S2b — ⚠️ CHỈ KHI `train_config_sel.yaml` KHÔNG CÓ TRONG GÓI

`thesis_rented.zip` trên Drive là ảnh chụp kho tại thời điểm đóng gói. Config của sprint này
viết ngày **2/9**, nên gói cũ hơn ngày đó sẽ **thiếu nó** và ô S3 chết với
`FileNotFoundError: .../harness/train_config_sel.yaml`.

Hai đường xử:

- **Nhanh:** chạy ô dưới để ghi thẳng config ra kho trên máy ảo.
- **Sạch:** dựng lại `thesis_rented.zip` từ WSL rồi tải lên Drive, lần sau khỏi vấp.

```python
import os, yaml
CFG_SRC = f"{REPO}/harness/train_config_sel.yaml"
if os.path.exists(CFG_SRC):
    print("đã có sẵn trong gói — bỏ qua ô này")
else:
    os.makedirs(os.path.dirname(CFG_SRC), exist_ok=True)
    open(CFG_SRC, "w", encoding="utf-8").write('''model_name_or_path: Qwen/Qwen2.5-VL-3B-Instruct
trust_remote_code: true
image_min_pixels: 200704
image_max_pixels: 1003520

dataset: gui_sel
seed: 101
output_dir: /workspace/ckpt/gui_sel_seed101
dataset_dir: /workspace/data/branches

stage: sft
do_train: true
finetuning_type: lora
lora_rank: 8
lora_alpha: 16
lora_dropout: 0.05
lora_target: q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj
freeze_vision_tower: true
freeze_multi_modal_projector: true
quantization_bit: 4
quantization_method: bnb

template: qwen2_vl
cutoff_len: 3072
train_on_prompt: false

per_device_train_batch_size: 4
gradient_accumulation_steps: 4
learning_rate: 1.0e-4
num_train_epochs: 1.0
lr_scheduler_type: cosine
warmup_ratio: 0.05
bf16: true
fp16: false
gradient_checkpointing: true

save_steps: 200
save_total_limit: 2
logging_steps: 20
report_to: none

val_size: 0.0
do_eval: false
''')
    print("đã ghi", CFG_SRC)

c = yaml.safe_load(open(CFG_SRC))
print("cutoff_len       =", c["cutoff_len"], "← cần 3072")
print("num_train_epochs =", c["num_train_epochs"], "← cần 1.0")
print("stage / 4-bit    =", c["stage"], "/", c["quantization_bit"])
```

⚠️ Bản dán trên bỏ phần chú thích cho gọn nhưng **giá trị từng khoá y hệt**
`harness/train_config_sel.yaml`. Nếu sau này sửa file gốc thì phải sửa cả đây, hoặc tốt hơn là
dựng lại gói.

---

## Ô S3 — chọn lượt, sinh cấu hình, **bảy phép tiền bay**

```python
import os, yaml, shutil, json

# ⚠️⚠️ BA DÒNG DUY NHẤT ĐỔI GIỮA SÁU LƯỢT ⚠️⚠️
NHANH = "gui_sel"        # gui_sel | gui_sft_match | gui_s1_match
SEED  = 101              # 101 | 202
# ────────────────────────────────────────────

OUT = f"/content/drive/MyDrive/thesis/ckpt/{NHANH}_seed{SEED}"
cfg = yaml.safe_load(open(f"{REPO}/harness/train_config_sel.yaml"))
cfg.update(dataset=NHANH, seed=SEED, output_dir=OUT,
           dataset_dir=f"{TR}/branches", preprocessing_num_workers=8)
CFG = "/content/cfg_sel.yaml"
yaml.safe_dump(cfg, open(CFG, "w"), sort_keys=False, allow_unicode=True)

goc = yaml.safe_load(open(f"{REPO}/harness/train_config_sel.yaml"))
CHO_PHEP = {"dataset", "seed", "output_dir", "dataset_dir",
            "preprocessing_num_workers"}
khac = {k for k in set(cfg) | set(goc) if cfg.get(k) != goc.get(k)}
n = len(json.load(open(f"{TR}/branches/{NHANH}.json")))

print("① cfg đúng nhánh        :", cfg["dataset"] == NHANH, cfg["dataset"])
print("② chỉ khoá được phép đổi:", khac <= CHO_PHEP, sorted(khac - CHO_PHEP) or "✅")
print("③ KHÔNG sót max_steps   :", "max_steps" not in cfg)
print("④ output_dir RỖNG       :", not os.path.isdir(OUT) or not os.listdir(OUT), OUT)
print("⑤ số mẫu                :", n, "← cần 64.567")
print("⑥ cutoff / epoch        :", cfg["cutoff_len"], "/", cfg["num_train_epochs"], "← cần 3072 / 1.0")
p_anh = json.load(open(f"{TR}/branches/{NHANH}.json"))[0]["images"][0]
print("⑦ đường dẫn ảnh mở được :", os.path.exists(p_anh), "|", p_anh[:64])
print("   ~ số bước ước tính   :", -(-n // 16))
```

**Bảy dòng phải xanh hết.** Riêng:

- **②** khoá thứ bảy khác là **DỪNG HẲN** — nếp ô kiểm vàng A.2b, chạy 3 lần trong ngày 16/8 đều 38/38.
- **④** `output_dir` phải **RỖNG**. Không rỗng thì LLaMA-Factory chạy tiếp từ điểm lưu cũ, **nhảy
  qua** phần lớn số bước rồi chạy đúng vài bước: log vẫn in `Training completed`, vẫn có
  `total_flos`, trông y như đạt. Đọc bằng **hai con số**: `train_runtime` và `loss` cuối.
- **⑦** sai prefix ảnh thì chết **SAU** 15–25 phút mã hoá token, không phải ngay.
  ⚠️ Trường `images` trong ba nhánh là **đường dẫn TUYỆT ĐỐI**
  `/content/ws/thesis/harness/dg1_cache/train_ac/images/…`, giống hệt nếp của `s1.json` và
  `min_desc.json`. Dựng lại dữ liệu mà quên `--img-prefix` là ra đường **tương đối**, và vì
  runbook `os.chdir(REPO)` nên nó trỏ vào `REPO/images/` — không tồn tại. Bắt được lỗi này
  ngày 2/9 trước khi lên Colab; lệnh dựng đúng nằm ở ô S0.
- Số bước ước tính: `ceil(64.567/16) = 4.036` cho **1 epoch** (nhánh cũ 2 epoch nên ra 8.072).

⛔ **`ckpt/<nhánh>_seed<seed>` là ĐẦU RA, phải rỗng.** Sprint này **không** nối tiếp từ adapter
nào — cả ba nhánh train từ backbone gốc. Đừng chĩa `rmtree` vào `ckpt/s2_seed101`: đó là đầu vào
của MIN-DESC và S2/202 đã quyết không chạy lại, mất là không dựng lại được.

---

## Ô S4 — TRAIN, chạy nền

```python
import subprocess, os
# ⛔ CHẶN PHÓNG HAI LẦN. 15–25 phút mã hoá token đầu trông y hệt treo, rất dễ dán lại ô này.
#    Hai tiến trình cùng ghi một output_dir là hỏng cả lượt VÀ hỏng điểm lưu trên Drive.
assert not any("llamafactory-cli" in p for p in
               subprocess.run(["bash","-lc","ps -eo args"],capture_output=True,text=True).stdout.split("\n")), \
       "⛔ ĐANG CÓ MỘT LƯỢT CHẠY — đừng phóng lần hai"
os.makedirs(OUT, exist_ok=True)
LOG = f"/content/train_{NHANH}_{SEED}.log"
f = open(LOG, "a")
# ⛔ start_new_session=True là BẮT BUỘC, không phải tuỳ chọn.
#    Thiếu nó thì tiến trình train nằm CÙNG process group với kernel notebook, và mọi
#    lần bấm Stop một ô bất kỳ (kể cả ô theo dõi) đều gửi SIGINT sang train.
#    Đo 2/9: mất một lượt ở bước 747 vì đúng chuyện này — log ghi KeyboardInterrupt.
P = subprocess.Popen(["llamafactory-cli","train",CFG], stdout=f, stderr=subprocess.STDOUT,
                     start_new_session=True)
print("PID", P.pid, "· log", LOG)
```

---

## Ô S5 — đồng bộ lên Drive mỗi 5 phút ⚠️ chạy NGAY sau S4

```python
import threading, shutil, time, os
def dongbo():
    while True:
        try:
            for f in ("trainer_log.jsonl","trainer_state.json","all_results.json"):
                p = os.path.join(OUT, f)
                if os.path.exists(p): shutil.copy(p, p + ".snap")
        except Exception as e: print("sync:", e, flush=True)
        time.sleep(300)
threading.Thread(target=dongbo, daemon=True).start()
print("đã bật đồng bộ 5 phút/lần")
```

⚠️ **`--out` trỏ thẳng vào Drive KHÔNG sống sót qua mất máy** — đo thật 24/8: một lượt ghi thẳng
vào Drive suốt 2 giờ, mất máy xong tệp **biến mất hoàn toàn**, chỉ bản chụp định kỳ còn.
Tệp mở chế độ `"a"` chưa đóng lần nào thì FUSE chưa đẩy lên cloud, và `ls` vẫn hiện tệp như
thường ⇒ **không có dấu hiệu nào báo trước**. Chụp sang **tên khác** bằng `cp` mới buộc Drive
tải lên trọn vẹn.

---

## Ô S6 — theo dõi

```python
import json, os, time
JS, LOG = os.path.join(OUT,"trainer_log.jsonl"), f"/content/train_{NHANH}_{SEED}.log"
while True:
    if os.path.exists(JS):
        d = [json.loads(l) for l in open(JS) if l.strip()]
        if d:
            r = d[-1]
            print(f"{r.get('current_steps')}/{r.get('total_steps')} "
                  f"· {r.get('percentage')}% · còn {r.get('remaining_time')}", flush=True)
    # số học (loss, lr) CHỈ có trong LOG, không có trong jsonl ở stage sft của stack này
    if os.path.exists(LOG):
        ls = [l for l in open(LOG) if "'loss'" in l]
        if ls: print("   ", ls[-1].strip()[:110], flush=True)
    time.sleep(120)
```

⚠️ **Tên trường trong `trainer_log.jsonl` ĐỔI THEO STAGE, phải kiểm lại mỗi lần dựng máy.**
Stage `sft` (cả sáu lượt này) **có** `loss` và `lr`; stage `dpo` thì **không**. Ô theo dõi nào
lọc dòng theo `loss` sẽ vứt sạch mọi dòng ở nhánh `dpo` rồi in "chưa có bước nào" suốt cả lượt
mà không báo lỗi.

⚠️ **"Connecting" / "Not connected to runtime" trên trình duyệt KHÔNG phải máy chết.** Bằng chứng
thật: PID còn sống, hoặc thư mục điểm lưu có bản mới trong ~34 phút. Kiểm `wc -l` hai lần cách
nhau 60 giây, **đừng đọc `ls -la`** — mtime trên `/content/drive` không cập nhật khi ghi thêm.

---

## Sau mỗi lượt — ba việc

1. **Kiểm điểm lưu trọn vẹn:** ghi dở thì bản **CUỐI** nhỏ hơn bản trước. So `du -h` hai
   `checkpoint-*` cuối.
2. **Chép adapter về Drive** (nếu chưa nằm sẵn trên Drive).
3. **Ghi lại `total_flos` và số bước** — dùng `trainer_state.json`, ⛔ **không** dùng
   `all_results.json`: ba trường `train_loss`, `train_runtime`, `*_per_second` **sai sau khi chạy
   tiếp**. `total_flos` thì không hỏng.

## ⛔ LUẬT CHẤM — đọc trước khi chạy `infer_branch.py`

Hai nhánh có menu **bắt buộc** truyền `--cands`, nhánh không menu **bắt buộc** bỏ trống:

| nhánh | cờ | vì sao |
|---|---|---|
| `gui_sel` · `gui_sft_match` | `--cands .../test_ac/candidates.jsonl` | được DẠY với khối ứng viên |
| `gui_s1_match` · S1 · S2 · MIN-DESC · CE2 | *(bỏ trống)* | giữ 24 dòng OCR |

```bash
# hai nhánh CÓ menu
python harness/infer_branch.py --adapter <ckpt> --out preds_gui_sel_seed101.jsonl \
    --cands harness/dg1_cache/test_ac/candidates.jsonl
# nhánh KHÔNG menu
python harness/infer_branch.py --adapter <ckpt> --out preds_gui_s1_match_seed101.jsonl
```

⛔ **Quên cờ là hỏng câm.** Đo 2/9: chấm `gui_sel` mà thiếu `--cands` thì **499/500 mẫu dựng
sai câu nhắc** — mô hình được dạy chọn từ menu, lúc chấm không thấy menu nào. Nó vẫn sinh chữ,
thước vẫn ra điểm, log không báo gì; chỉ là chấm một hệ thống chưa từng tồn tại.

⚠️ Tập kiểm cũng cần `candidates.jsonl` — dựng bằng
`build_candidates.py --split test --all-steps --max 40` (0 GPU). Bản hiện có trên WSL là
4.463 màn dựng **không** kèm `--all-steps`; nếu chấm cả bước không chạm thì phải dựng lại.

Dòng đầu ra của `infer_branch.py` in rõ đang ở chế độ nào — **đọc dòng đó**, đừng tin lệnh mình vừa gõ.

---

## Sau lượt 1 — cổng G6, trước khi chạy tiếp năm lượt còn lại

`sel_acc` trên **600 bước DEV** có ứng viên vàng, khớp tên ∧ point ±14%, `<sel>none</sel>` tính
**sai**, ngưỡng **≥63,6%**. ⛔ **Không dùng tập test.**
Trượt ⇒ báo thẳng là cơ chế không học được, bài đổi thành **báo cáo âm** — đừng nới ngưỡng.

⛔ `gold_candidate()` ở `build_sel_data.py:43` là **bản duy nhất** — lúc chấm phải **import lại**,
cấm viết bản thứ hai.
