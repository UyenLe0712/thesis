# Colab — kéo adapter `gui_sel_seed101` về, pin hash, đóng gói cho Kaggle (4/9/2026)

Mục đích: gỡ thứ **chặn duy nhất** của mọi việc GPU còn lại. Adapter đang nằm trên Drive;
kho WSL đã có đủ mọi artifact khác (`report/134` §14).

⚠️ **Đổi runtime sang CPU trước khi chạy** (Runtime → Change runtime type → CPU). Bốn ô này chỉ
mount Drive, đọc JSON, tính hash và copy tệp — **không dòng nào chạm GPU**. Colab tính đơn vị theo
loại máy ảo, nên bật GPU để copy tệp là đốt đơn vị không đổi lấy gì, mà đơn vị đang là ràng buộc
sống còn (mục 8 của `report/134`: dưới ~120–150 đơn vị thì lượt đối chứng chết).

**Chạy tuần tự A → B → C → D.** Không ô nào chạy lâu quá vài phút nên không dính bốn luật
Colab về mất máy, nhưng vẫn **đừng bấm Stop giữa chừng** — cứ để ô chạy hết.

Sau khi xong, dán kết quả ô A và ô B vào chat để đối chiếu với
`runs/sel/manifest_selA_selB_4_9.json`.

---

## Ô A — gắn Drive, soi thư mục điểm lưu

```python
from google.colab import drive
drive.mount('/content/drive')

import os, json, glob
CK = '/content/drive/MyDrive/thesis/ckpt/gui_sel_seed101'
print('có thư mục:', os.path.isdir(CK))
print()
for p in sorted(glob.glob(CK + '/*')):
    n = os.path.basename(p)
    if os.path.isdir(p):
        print(f'[thư mục] {n}')
    else:
        print(f'          {n:38s} {os.path.getsize(p):>12,} byte')

# ⛔ Phải lấy THƯ MỤC GỐC (có adapter_model.safetensors + adapter_config.json).
#    checkpoint-* là bản dở giữa chừng; dùng nhầm là chấm một mô hình khác mà
#    không có gì báo lỗi (report/134 §0.1).
goc = os.path.isfile(CK + '/adapter_model.safetensors') and \
      os.path.isfile(CK + '/adapter_config.json')
print('\nthư mục gốc có đủ hai tệp adapter:', goc)
if not goc:
    print('⚠️ THIẾU ở đường dẫn trên. Dò khắp Drive xem nó nằm đâu:')
    for r, ds, fs in os.walk('/content/drive/MyDrive'):
        if 'adapter_model.safetensors' in fs:
            print('   ->', r)
    print('⚠️ Đừng lấy checkpoint-*. Báo lại trước khi làm tiếp.')
```

Nếu ô này in `có thư mục: False`, đoạn dò ở trên sẽ liệt kê mọi chỗ trên Drive có
`adapter_model.safetensors`. Sửa `CK` trong **cả ba ô A · B · C** cho khớp rồi chạy lại từ đầu.

## Ô B — kiểm cấu hình adapter đúng lượt train, và pin hash

```python
import json, hashlib, os
CK = '/content/drive/MyDrive/thesis/ckpt/gui_sel_seed101'

cfg = json.load(open(CK + '/adapter_config.json'))
mong_doi = {
    'base_model_name_or_path': 'Qwen/Qwen2.5-VL-3B-Instruct',   # train_config_sel.yaml:23
    'r': 8,                                                      # lora_rank
    'lora_alpha': 16,
}
for k, v in mong_doi.items():
    thuc = cfg.get(k)
    print(f'{"OK " if thuc == v else "LỆCH"} {k:28s} = {thuc!r}   (mong đợi {v!r})')
# ⚠️ ĐỪNG so target_modules với bảy tên ngắn — sẽ báo LỆCH oan.
# LLaMA-Factory bật freeze_vision_tower phải liệt kê TÊN ĐẦY ĐỦ từng layer cho ba ma
# trận mlp, vì vision tower của Qwen2.5-VL cũng có mlp.gate_proj/up_proj/down_proj và
# tên ngắn sẽ quét trúng nó. Còn q/k/v/o để tên ngắn được, vì vision tower dùng
# attn.qkv/attn.proj, không trùng tên. Phép kiểm ĐÚNG là đếm ma trận thật (ô B2).
tm = set(cfg.get('target_modules') or [])
ngan = sorted(t for t in tm if '.' not in t)
print(f'target_modules: {len(tm)} mục — {len(ngan)} tên ngắn {ngan}, '
      f'còn lại là tên đầy đủ theo layer')

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

print()
for n in ['adapter_model.safetensors', 'adapter_config.json']:
    p = os.path.join(CK, n)
    print(f'{n:32s} {os.path.getsize(p):>12,} byte  sha256 {sha256(p)}')

# lượt train đã chạy tới đâu — đối chiếu 4.036 bước của report/134
ts = os.path.join(CK, 'trainer_state.json')
if os.path.isfile(ts):
    st = json.load(open(ts))
    print(f"\nglobal_step = {st.get('global_step')}  (mong đợi 4036)")
    print(f"epoch       = {st.get('epoch')}")
else:
    print('\nkhông có trainer_state.json ở thư mục gốc')
```

## Ô B2 — đếm ma trận thật trong adapter (phép kiểm đúng)

Đọc thẳng phần header của safetensors, không nạp mô hình, nên chạy được trên CPU trong một giây.

```python
import json, struct, re
from collections import Counter, defaultdict
CK = '/content/drive/MyDrive/thesis/ckpt/gui_sel_seed101'

with open(CK + '/adapter_model.safetensors', 'rb') as f:
    hdr = json.loads(f.read(struct.unpack('<Q', f.read(8))[0]))
hdr.pop('__metadata__', None)

CAN = {'q_proj','k_proj','v_proj','o_proj','gate_proj','up_proj','down_proj'}
lay = defaultdict(set)
for k in hdr:
    m = re.search(r'layers\.(\d+)\.', k)
    p = re.search(r'(' + '|'.join(CAN) + r')', k)
    if m and p:
        lay[int(m.group(1))].add(p.group(1))
thieu = {i: sorted(CAN - v) for i, v in lay.items() if v != CAN}
vis = [k for k in hdr if 'visual' in k or 'vision' in k]

print('số tensor                :', len(hdr), '(mong đợi 504 = 36 layer × 7 × 2)')
print('số layer có LoRA         :', len(lay), f'(dải {min(lay)}-{max(lay)}, mong đợi 36)')
print('layer thiếu ma trận      :', thieu or 'không layer nào thiếu')
print('tensor thuộc vision tower:', len(vis), '(PHẢI là 0 — freeze_vision_tower)')
tp = sum(__import__('math').prod(v['shape']) for v in hdr.values())
print(f'tổng tham số LoRA        : {tp:,} (mong đợi 14.966.784)')
```

## Ô C — đóng gói

`gui-sel-adapter` là **một trong ba input** mà notebook Kaggle cần
(cùng `thesis-score` và `thesis-sel-infer`).

```python
import shutil, os
CK  = '/content/drive/MyDrive/thesis/ckpt/gui_sel_seed101'
OUT = '/content/gui_sel_seed101_adapter'
os.makedirs(OUT, exist_ok=True)

# CHỈ hai tệp của thư mục gốc; không kéo theo checkpoint-* (nặng và dễ dùng nhầm)
for n in ['adapter_model.safetensors', 'adapter_config.json']:
    shutil.copy2(os.path.join(CK, n), OUT)
# kèm theo nếu có, để truy nguyên lượt train
for n in ['trainer_state.json', 'training_args.bin', 'README.md']:
    p = os.path.join(CK, n)
    if os.path.isfile(p):
        shutil.copy2(p, OUT)

zip_path = shutil.make_archive('/content/gui_sel_seed101_adapter', 'zip', OUT)
print(zip_path, os.path.getsize(zip_path), 'byte')
print(sorted(os.listdir(OUT)))
```

## Ô D — tải về máy

```python
from google.colab import files
files.download('/content/gui_sel_seed101_adapter.zip')
```

`files.download` hay hỏng với tệp lớn hoặc mạng chập chờn, mà nó **không báo lỗi rõ** — chỉ là
trình duyệt không hiện gì. Hỏng thì dùng đường vòng qua Drive, tải bằng giao diện Drive:

```python
import shutil
shutil.copy2('/content/gui_sel_seed101_adapter.zip',
             '/content/drive/MyDrive/thesis/gui_sel_seed101_adapter.zip')
print('đã cất sang Drive — tải bằng giao diện Drive')
```

⚠️ Tải xong **kiểm kích thước tệp trên máy khớp số byte mà ô C in ra**. Tệp zip tải dở vẫn mở
được một phần, và sẽ hỏng ở đúng lúc tốn kém nhất.

Tải xong thì **giải nén vào `runs/sel/adapter_gui_sel_seed101/`** trên máy WSL (đừng để trong
`harness/`, nó không phải mã), rồi báo lại — bước kế là kiểm hash trùng với ô B và dựng dataset
Kaggle.

---

## Sau đó: ba việc GPU, theo đúng thứ tự của `report/134` mục 0

| thứ tự | việc | máy | giờ ước |
|---|---|---|---|
| 1 | suy luận nốt **3.063 bước** còn lại + `exec` đủ **4.463** | T4 | ~4 h + ~5,6 h |
| 2 | train `gui_sft_match`/101 (**song song**, không tranh GPU) | A100 | ~23–30 h |
| 3 | sequence-score lát dev 1.400 (`seq_score_sel.py`) | T4 | probe trước, xem dưới |

**Lệnh của bước 3** (chạy `--probe 50` trước, luôn):

```
python3 harness/seq_score_sel.py \
  --adapter runs/sel/adapter_gui_sel_seed101 \
  --cands harness/dg1_cache/test_ac/candidates.jsonl \
  --only runs/sel/preds_gui_sel_seed101_dev1400.jsonl \
  --out runs/sel/seqscores_gui_sel_seed101_dev1400.jsonl \
  --cache-prompt --probe 50
```

`--cache-prompt` mã hoá câu nhắc (gồm ảnh ~1.272 token) **một lần mỗi bước** thay vì mã hoá lại
cho từng lô span; rẻ hơn khoảng **5–7 lần**. Ba bước đầu **bắt buộc** tính bằng cả hai đường rồi
so, lệch quá `1e-3` là script dừng hẳn. Nếu bản `transformers` trên máy đó không cắt được bộ nhớ
đệm thì script cũng dừng và bảo chạy lại **không** có cờ này — **đừng tự sửa ngưỡng kiểm**.

Đọc `--probe 50` bằng ba dòng: `s_none` và `s_star` phải **âm và cùng cỡ** · `tok_none` phải
**bằng nhau ở mọi bước** · `n_cand` phải khớp khối ứng viên của bước đó. Nhân số giây mỗi bước với
1.400 để biết lượt dài tốn bao lâu **trước** khi phóng.

### Probe trên máy WSL không GPU — kiểm mã trước, khỏi tốn quota

Chạy được, nhưng **chỉ để kiểm mã**, không để lấy số. Đã soát môi trường ngày 4/9: venv
`~/.venvs/thesis` có torch 2.8.0+cpu và transformers 5.14.1, lớp `Qwen2_5_VLForConditionalGeneration`
còn nguyên tên, `DynamicCache` **có** `crop` nên `--cache-prompt` dùng được; ảnh tập kiểm đủ
**6.969 tệp (3,3 GB)**. Thiếu đúng hai gói và trọng số mô hình nền.

**Bước 1 — cài hai gói còn thiếu** (một lần, ~1 phút):

```
~/.venvs/thesis/bin/pip install peft accelerate
```

`peft` để nạp adapter; `accelerate` vì script gọi `device_map="auto"`.

**Bước 2 — tải trọng số mô hình nền** (~7 GB, 20–40 phút tuỳ mạng; cache HF hiện chỉ có 12 MB
metadata). Tải trước để thấy thanh tiến độ, thay vì để script tự tải rồi ngồi nhìn màn hình đứng:

```
~/.venvs/thesis/bin/python -c "
from huggingface_hub import snapshot_download
p = snapshot_download('Qwen/Qwen2.5-VL-3B-Instruct')
print('xong ->', p)"
```

**Bước 3 — chạy probe 3 bước:**

```
cd /mnt/d/Master/Thesis
~/.venvs/thesis/bin/python harness/seq_score_sel.py \
  --adapter runs/sel/adapter_gui_sel_seed101 \
  --cands harness/dg1_cache/test_ac/candidates.jsonl \
  --only runs/sel/preds_gui_sel_seed101_dev1400.jsonl \
  --out /tmp/probe_cpu.jsonl \
  --dtype bfloat16 --cache-prompt --probe 3
```

Lý do phải đặt `--dtype`: không có CUDA thì `pick_dtype()` trả `float32`, mà 3B ở float32 là
**~12,4 GB trọng số** trong khi máy có **12 GB RAM (11 GB khả dụng)** ⇒ tràn. `bfloat16` còn
~6,2 GB nên vừa.

⛔ **Điểm của lượt CPU KHÔNG so được với lượt GPU** (khác kiểu số) — script tự in cảnh báo. Giá
trị duy nhất của nó là chứng minh mã chạy đúng, nhất là **phép kiểm chéo nhanh↔chậm**, trước khi
tiêu 5,6 giờ quota Kaggle.
⚠️ Máy này là i7-1065G7, không có AMX nên bf16 không được tăng tốc phần cứng. Ước bậc thang
**3–4 phút/bước** ⇒ lát 1.400 bước là **70–90 giờ**, tức **không dùng CPU cho lượt thật**. Con số
đó là **ước, chưa đo** — chạy `--probe 3` rồi lấy giây/bước thật, đừng lên lịch theo ước.

**Ba dòng cần đọc trong đầu ra probe**, theo thứ tự quan trọng:

1. `kiểm chéo nhanh↔chậm: lệch tối đa ...` — **đây là thứ đáng tiền nhất của lượt probe.**
   Lệch cỡ `1e-6`…`1e-4` là đường nhanh đúng, lượt Kaggle được dùng `--cache-prompt` và tốn
   dưới 1 giờ thay vì ~4,7 giờ. Script tự dừng nếu lệch quá `1e-3`; **đừng nới ngưỡng đó**.
2. `khối ứng viên: phủ 3/3 bước — fail-closed ĐẠT` — bản vá 4/9 đang chạy thật.
3. `[3/3] ... s/bước` — nhân với 1.400 để biết lượt thật tốn bao lâu **trên GPU thì chia tiếp**;
   con số CPU chỉ dùng để so tương đối giữa hai đường, không dùng để lên lịch Kaggle.

Rồi soi tệp `/tmp/probe_cpu.jsonl`: `s_none` và `s_star` phải **âm và cùng cỡ**; `tok_none` phải
**bằng nhau ở mọi bước** (span `<sel>none</sel>` cố định); `n_cand` khớp số ứng viên của bước đó;
`margin` = `s_star − s_none`.

⛔ Tệp probe ghi ra `/tmp`, **không** ghi vào `runs/`. Điểm chạy ở bfloat16 trên CPU không so được
với điểm chạy trên GPU, để lẫn vào `runs/` là mời một lỗi câm.

⛔ **Khoá τ trước khi nhìn `exec` của nhánh đối chứng, và trước khi động vào phần 3.062 bước.**
Thủ tục chọn τ đã đăng ký trước ở `report/106` mục **(x16d)**; đọc lại mục đó chứ đừng chọn
ngưỡng theo cảm giác lúc nhìn số.
