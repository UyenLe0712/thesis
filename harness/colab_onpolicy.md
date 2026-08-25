# MIN-ONPOLICY trên Colab — dán thẳng, tự đủ

> # ⛔ NHÁNH NÀY ĐÃ ĐÓNG — 25/8/2026. ĐỪNG CHẠY LẠI.
> O1 chạy xong (14.000 màn, 4,5 h A100). **O2 trượt cổng ③: 459 cặp = 3,3%, ngưỡng 25%.**
> Phán quyết và lý do đầy đủ: `report/106` mục **(x13)**.
> ⛔ Chạy lại O1 với `--limit` lớn hơn **không cứu được** — cổng ③ là cổng **tỉ lệ**.
> Runbook giữ lại để tra cách làm, không phải để thực thi.

Biến thể đăng ký trước ở `report/106` mục **(x11)**. Đổi đúng **một** thứ so với MIN-DESC:
nguồn vế âm. Mọi khoá cấu hình khác giữ nguyên — đã `diff` xác nhận chỉ `dataset` và
`output_dir` khác.

**Tổng: ~13,5 giờ GPU Colab · 0 giờ quota Kaggle** cho tới khi qua cổng khai báo.

### Card nào

| card | O1 (sinh khai báo) | O3/O4 (train ORPO) |
|---|---|---|
| **A100 40 GB** | ✅ | ✅ đã chạy thật cho MIN-DESC, 20,6 s/bước |
| **L4 24 GB** | ✅ | ⚠️ **phải chạy O2b probe trước** — rẻ hơn nhiều nhưng bộ nhớ hẹp hơn 40% |
| **T4 16 GB** | ⚠️ chậm, và `pick_dtype()` tự rơi về fp16 | ⛔ **KHÔNG** — xem dưới |

⛔ **T4 không dùng cho O3/O4.** Cấu hình khoá `bf16: true`, mà T4 là kiến trúc Turing —
**không có bf16 chạy thật**. Đổi sang fp16 là sửa một khoá của cấu hình đã khoá ở (x3), làm
hỏng phép so với MIN-DESC. Cộng 16 GB quá hẹp cho ORPO không-liger.

✅ **L4 có bằng chứng đổi card không đổi kết quả:** `CLAUDE.md` ghi L4 vs A100 cùng `seed 101`
cho loss 20 bước **trùng ba chữ số** và `total_flos` **y hệt**. L4 là Ada (sm_89) nên bf16 chạy
thật, giữ nguyên `bf16: true`. Rủi ro duy nhất là **bộ nhớ**, và O2b đo được rủi ro đó trong 12 phút.

⚠️ Giá đơn vị Colab **phải đếm trong phiên**, đừng tin con số ghi trong file — `CLAUDE.md` đã
ghi luật này sau lần nhớ sai suýt dẫn tới thuê nhầm máy.

| ô | việc | giá | dừng được không |
|---|---|---|---|
| **O1** | S2 tự sinh khai báo trên màn tập dạy | ~3,5 h | ✅ nối tiếp được |
| **O2** | dựng cặp + **ba cổng (x11c)** | vài phút CPU | ⛔ **trượt cổng ⇒ DỪNG HẲN** |
| **O3** | train MIN-ONPOLICY | ~5 h | ✅ chạy tiếp từ checkpoint |
| **O4** | train CE2-ONPOLICY | ~3 h | ✅ |
| **O5** | sinh câu trên lát tập kiểm, hai nhánh | ~2 h | ✅ |
| **O6** | cổng khai báo `gate_desc_acc.py` | vài giây CPU | quyết có chấm Kaggle không |

---

## ⚡ O-L4 — KIỂM L4 TRƯỚC KHI TIÊU 3,5 GIỜ

Chạy **trước O1**. Dùng `min_desc_long.json` (200 cặp nặng nhất của MIN-DESC) đã có sẵn trong
gói — cặp on-policy cùng cấu trúc, cùng khuôn, cùng vế `chosen`, nên đây là phép thử thay thế
hợp lệ. Tổng ~35 phút, phần lớn là bung ảnh mà O1 đằng nào cũng cần.

### Bước 1 — chọn card

`Runtime → Change runtime type → **L4 GPU** → Save`. Việc này **khởi động lại máy ảo và xoá sạch
`/content`**, nên làm TRƯỚC mọi thứ khác.

### Bước 2 — upload gói mới lên Drive

`_bundles/thesis_rented.zip` (3,6 MB) → `MyDrive/thesis/`, **đè bản cũ**. Bản trên Drive chưa có
`sinh_desc_train.py`, `build_min_desc_onpolicy.py`, hai cấu hình `*_onpolicy.yaml`.

### Bước 3 — T1 → Restart → T2 → T3

Y nguyên `harness/colab_train_min_desc.md`. Ba dòng phải đúng ở T2: ảnh dạy **64.567** · khai báo
**41.099** · `ckpt S2 = True`. **Đừng bỏ T3.**

### Bước 4 — ô probe (12 phút)

```python
import shutil, yaml, os, subprocess, time, torch, json

cap = torch.cuda.get_device_capability()
print("card:", torch.cuda.get_device_name(0),
      f"· {torch.cuda.get_device_properties(0).total_memory/2**30:.1f} GiB",
      f"· sm_{cap[0]}{cap[1]} · bf16 THẬT:", cap[0] >= 8)
assert cap[0] >= 8, ("⛔ DỪNG — card không có bf16 chạy thật (T4/P100). Cấu hình khoá "
                     "`bf16: true` ở (x3); đổi sang fp16 là sửa cấu hình đã khoá.")

PROBE = "/content/probe_l4"
shutil.rmtree(PROBE, ignore_errors=True)   # ⛔ không xoá thì LLaMA-Factory chạy TIẾP từ
                                           #    checkpoint cũ, nhảy qua 20 bước, log vẫn
                                           #    in "Training completed" — trông y như đạt
c = yaml.safe_load(open(f"{REPO}/harness/train_config_orpo.yaml"))
c.update({"dataset": "gui_min_desc_long", "max_steps": 20, "output_dir": PROBE,
          "save_steps": 1000, "logging_steps": 1})
yaml.safe_dump(c, open("/content/probe_l4.yaml", "w"))

# lấy ĐỈNH bộ nhớ trong lúc chạy — đây là con số quyết định, không phải chữ trong log
mon = subprocess.Popen(["bash","-lc",
    "nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -l 5 "
    "> /content/vram.txt"])
t0 = time.time()
!cd {REPO} && llamafactory-cli train /content/probe_l4.yaml 2>&1 | tail -30
mon.terminate()
print(f"\n⏱ tổng ô: {(time.time()-t0)/60:.1f} phút")
```

### Bước 5 — đọc bằng BỐN con số

```python
import json, os
st = json.load(open(f"{PROBE}/trainer_state.json"))
r  = json.load(open(f"{PROBE}/all_results.json"))
lg = st["log_history"]
sb = r["train_runtime"] / max(st["global_step"], 1)
vr = [int(x) for x in open("/content/vram.txt") if x.strip().isdigit()]
tong = torch.cuda.get_device_properties(0).total_memory / 2**20

print(f"① global_step   : {st['global_step']:>8}   ← phải 20")
print(f"② train_runtime : {r['train_runtime']:>8.0f} s ← phải ~200–500, KHÔNG phải ~15")
print(f"   s/bước       : {sb:>8.1f} s  ⇒ 800 bước ≈ {sb*800/3600:.1f} giờ")
print(f"③ đỉnh VRAM     : {max(vr) if vr else -1:>8} / {tong:.0f} MiB"
      f"  ({(max(vr)/tong*100) if vr else -1:.0f}%)")
print(f"④ trường có trong log_history: {sorted(lg[-1].keys())}")
for k in ("loss", "rewards/margins", "rewards/accuracies"):
    v = [h[k] for h in lg if k in h]
    if v: print(f"   {k:<20} đầu {v[0]:.4f} → cuối {v[-1]:.4f}")
```

### Bước 6 — phán quyết

| | ĐẠT ⇒ train trên L4 | TRƯỢT ⇒ đổi A100 |
|---|---|---|
| ① `global_step` | **20** | khác 20 |
| ② `train_runtime` | **200–500 s** | ~15 s = nó nhảy qua hết, probe **không diễn ra** |
| ③ đỉnh VRAM | **< 90%** tổng | ≥ 90%, hoặc log có `CUDA out of memory` |
| ④ loss | ORPO: **0,30–0,45** và `rewards/margins` **tăng dần** | loss ~0,1 hoặc margins phẳng/âm |

⛔ **Tràn bộ nhớ thì ĐỔI CARD, đừng hạ `cutoff_len` hay tắt `gradient_checkpointing`.** Cả hai
là khoá cấu hình của (x3); sửa là biến ablation một-biến thành hai-biến, hỏng phép so với
MIN-DESC.

⚠️ ③ nằm trong dải **80–90%** là **rủi ro**, không phải đạt: probe chạy 200 mẫu nặng nhất của
MIN-DESC, còn cặp on-policy có thể nặng hơn chút. Dải đó thì chạy lại O2b sau khi có dữ liệu
thật trước khi train.

### 📊 ĐÃ ĐO THẬT — L4 ngày 25/8, ghi lại để khỏi thử lại

| | A100 40 GB (mục x3c) | **L4 22 GB (25/8)** |
|---|---|---|
| s/bước, **cùng** 200 cặp nặng nhất | ~21 | **59,0** — chậm **2,8×** |
| 800 bước một nhánh | ~4,7 h | **13,1 h** |
| đỉnh VRAM | ~21 GB / 40 = **53%** | **21,4 GB / 22,6 = 95%** |
| loss / margins 20 bước | 0,0109 → 0,0190 | 0,35 · margins 0,0141 → 0,0166 |

⛔ **L4 TRƯỢT cho khâu train.** VRAM 95% không còn biên: probe chạy trên cặp nặng nhất của
MIN-DESC, cặp on-policy đúc lại có thể dài hơn chút ⇒ OOM sẽ nổ **giữa lượt 13 giờ**, không nổ ở
probe. Cộng 2,8× chậm ⇒ hai nhánh 26 h thay vì 8 h, trong khi lịch sử dự án là 8 lần mất máy
trong hai lượt train.
✅ Lượt probe **chạy thật**: `train_runtime` 1.179 s, `rewards/margins` tăng dần cùng dáng với
smoke A100. Không phải ca nhảy-qua-bước.

⭐ Con số `s/bước` ở ② là thứ đáng giá thứ hai của ô này: nhân 800 ra **giờ thật của một nhánh**
trên L4, rồi so với **20,6 s/bước của A100** để quyết rẻ hơn hay đắt hơn. Nhớ **đếm đơn vị trong
phiên**, đừng tin giá ghi trong file.

---

## O0 — chuẩn bị máy

Chạy **y nguyên** ô **T1 → Restart → T2 → T3** của `harness/colab_train_min_desc.md`.
Không có gì mới. Ba dòng phải đúng ở T2: ảnh dạy **64.567** · khai báo **41.099** ·
`ckpt S2 = True`.

⚠️ O1 cần **ảnh tập dạy** (31 GB), đó là khâu lâu nhất của T2. Đừng bỏ.
⚠️ Sau T2 **phải chạy T3** — `derived.tar.gz` ghi đè `dataset_info.json`.

---

## O1 — S2 tự sinh khai báo trên màn tập dạy

```python
import subprocess, os
D, REPO = "/content/drive/MyDrive/thesis", "/content/ws/thesis"
OUT = "/content/desc_train_s2.jsonl"      # ⚠️ ghi vào ĐĨA MÁY ẢO, không phải Drive

# ⛔ Bài học 24/8: --out trỏ thẳng vào Drive KHÔNG sống sót qua mất máy (tệp mở chế độ "a"
#    chưa đóng lần nào thì FUSE chưa đẩy lên cloud, mà `ls` vẫn hiện tệp như thường).
#    Ghi đĩa máy ảo rồi chụp định kỳ sang Drive bằng cp — cp tạo rồi ĐÓNG tệp mới.
os.makedirs(f"{D}/onpolicy", exist_ok=True)
subprocess.Popen(["bash","-lc",
    f'while true; do cp -f {OUT} {D}/onpolicy/ 2>/dev/null; sleep 300; done'])
print("đã bật chụp Drive 5 phút/lần")

!cd {REPO} && python3 harness/sinh_desc_train.py \
    --adapter {D}/ckpt/s2_seed101 --out {OUT} --limit 14000
```

📊 **Đo thật 25/8 trên A100: 0,90 bước/giây ⇒ 14.000 bước = 4,3 giờ.** `--max-new 64` gần như
không giúp vì thời gian bị **prefill** chi phối (mỗi màn hơn 1.000 token ảnh), sinh 64 hay 96
token cũng vậy. Đừng ước tốc độ theo số token sinh ra.

⚠️ **`--limit N` KHÔNG cho ra N cặp.** Phễu: ~78% bước có tên vàng dùng được × ~41% bước S2 sai
tên × ~50% qua cổng khoảng cách 80–350 px × ~80% ánh xạ được về node ⇒ **~13–20%**. `--limit
14000` ước còn **1.800–2.900 cặp**, tức 4–7 epoch ở cấu hình `16 × 800` — **rủi ro overfit**.
⇒ Xem con số thật ở O2 rồi quyết. Thiếu thì chạy lại **y nguyên** lệnh O1 với `--limit 30000`:
cơ chế nối tiếp bỏ qua phần đã xong, chỉ sinh phần thêm, không mất giây nào của lượt trước.

· `--limit 14000` đủ cho ~12.800 mẫu mà 800 bước × tích luỹ 16 sẽ đi qua. Muốn phủ rộng hơn
  thì bỏ cờ này (41.099 bước ≈ 10 h) — nhưng **chất lượng cặp quan trọng hơn số lượng**, xem
  `report/120` Mục 1.4.
· `--max-new 64`: chỉ sinh tới hết `</desc>`, không sinh câu ⇒ rẻ hơn `infer_branch` nhiều.
· Mất máy: dựng lại máy rồi gõ **y nguyên** lệnh trên, phải thấy `Nối tiếp: đã có N bước`.
  Bản chính mất thì chép về từ `{D}/onpolicy/`, **so `wc -l` giữ bản dài hơn**.

---

## O2 — dựng cặp và ĐỌC BA CỔNG  ⛔ chốt chặn quan trọng nhất

```python
!cd {REPO} && python3 harness/build_min_desc_onpolicy.py {OUT}

# ⚠️ BA TỆP VỪA GHI NẰM TRÊN ĐĨA MÁY ẢO — mất máy là mất. Chép sang Drive ngay.
BRA = f"{REPO}/harness/dg1_cache/train_ac/branches"
!mkdir -p {D}/onpolicy/branches
!cp {BRA}/min_desc_onpolicy.json {BRA}/min_desc_onpolicy_long.json \
    {BRA}/ce2_onpolicy.json {BRA}/dataset_info.json {D}/onpolicy/branches/
!ls -la {D}/onpolicy/branches/
```

⚠️ **Dựng lại máy sau này thì chép NGƯỢC về trước khi train**, nếu không T3 sẽ ghi đè
`dataset_info.json` bằng bản chỉ có bốn nhánh cũ và mất khoá `gui_min_desc_onpolicy`:

```python
!cp {D}/onpolicy/branches/*.json {REPO}/harness/dg1_cache/train_ac/branches/
```

Lần đầu chạy sẽ tải `all_forest_dict.zip` từ HuggingFace (cây trợ năng 99.131 màn) — vài phút.

**Đọc kết quả — ba cổng của (x11c), trượt cái nào cũng DỪNG:**

| dòng in ra | ĐẠT | TRƯỢT ⇒ dừng, không train |
|---|---|---|
| `① lối tắt độ dài — luật 'vế NGẮN hơn là chosen' đoán đúng` | **< 55%** | ≥ 55% |
| `① lối tắt chuỗi — tách được bằng '(no name)'` | **0%** | khác 0 |
| `③ eligibility` | **≥ 25%** | < 25% |
| `BẤT BIẾN` — năm dòng | **tất cả ✅** | có ⛔ |

⚠️ Cổng ② (false negative) đã ép ngay lúc dựng: mọi cặp có phần tử nhầm cách gold 80–350 px và
không chồng lấn hộp gold.

⛔ **Trượt thì dừng thật, đừng nới ngưỡng.** Dự án đã tự khai hai lần nới ngưỡng sau khi thấy
số; hồ sơ (x11c) khoá con số này trước khi có dữ liệu. Trượt là một kết quả, ghi lại rồi báo.

---

## O2b — ⚠️ PROBE BỘ NHỚ, BẮT BUỘC nếu card KHÔNG phải A100 40 GB

12 phút cứu một lượt train 5 giờ. Bài học P10 (`CLAUDE.md`): cấu hình chạy ngọt trên mẫu thường
vẫn **tràn bộ nhớ trên 200 mẫu dài nhất**. Và ORPO ở stage `dpo` **không kích hoạt liger**, mà
chỗ ngốn bộ nhớ là **bảng logits** — ORPO còn tính logits cho **cả hai vế**, tức gấp đôi.

```python
import shutil, yaml, os, torch
print("card:", torch.cuda.get_device_name(0),
      "·", torch.cuda.get_device_properties(0).total_memory/2**30, "GiB")
PROBE = "/content/probe_onpolicy"
shutil.rmtree(PROBE, ignore_errors=True)   # ⛔ KHÔNG xoá thì LLaMA-Factory chạy TIẾP từ
                                           #    checkpoint cũ, nhảy qua 20 bước rồi chạy đúng
                                           #    một bước — log vẫn in "Training completed"
c = yaml.safe_load(open(f"{REPO}/harness/train_config_orpo_onpolicy.yaml"))
c.update({"dataset": "gui_min_desc_onpolicy_long", "max_steps": 20, "output_dir": PROBE,
          "save_steps": 1000, "logging_steps": 1})
yaml.safe_dump(c, open("/content/probe_onpolicy.yaml", "w"))
!cd {REPO} && llamafactory-cli train /content/probe_onpolicy.yaml 2>&1 | tail -25
```

**Đọc bằng HAI con số, không đọc chữ `Training completed`:**
· `train_runtime` phải **~200–500 s** (không phải ~15 s — 15 s nghĩa là nó nhảy qua hết)
· loss ORPO phải **0,30–0,45** và `rewards/margins` tăng dần (mốc smoke A100: 0,0109 → 0,0190)

⛔ Thấy `CUDA out of memory` ⇒ card không đủ cho ORPO ở cấu hình đã khoá. **Đừng hạ
`cutoff_len` hay tắt `gradient_checkpointing`** — cả hai đều là khoá cấu hình của (x3), sửa là
làm hỏng phép so với MIN-DESC. Đổi card.

---

## O3 · O4 — train hai nhánh

Dùng **y nguyên** ô **T4 → T7** của `colab_train_min_desc.md`, chỉ sửa hai dòng ở T4:

```python
NHANH, SEED = "min_onpolicy", 101      # O4 đổi thành ("ce2_onpolicy", 101)
CFG_GOC = {"min_desc": "train_config_orpo.yaml",
           "ce2_s2":   "train_config_ce2.yaml",
           "min_onpolicy": "train_config_orpo_onpolicy.yaml",   # ★ thêm
           "ce2_onpolicy": "train_config_ce2_onpolicy.yaml"}[NHANH]
```

Mọi cảnh báo của runbook cũ áp nguyên: `output_dir` phải RỖNG ở lượt mới · stage `dpo` **không**
ghi `loss`/`lr` vào `trainer_log.jsonl` còn stage `sft` thì có · ô theo dõi đọc **hai nguồn**.
Cổng cơ học sau train: `global_step` = **800** ở cả hai.

---

## O5 — sinh câu trên lát tập kiểm

```python
import subprocess
# ⚠️ CHỤP ĐỊNH KỲ, đừng chỉ cp sau khi xong — mất máy giữa lượt là mất trắng phần đã sinh.
subprocess.Popen(["bash","-lc",
    f'while true; do cp -f /content/preds_*onpolicy*.jsonl {D}/onpolicy/ 2>/dev/null; '
    f'sleep 300; done'])
print("đã bật chụp Drive 5 phút/lần")

for ten in ("min_onpolicy_seed101", "ce2_onpolicy_seed101"):
    !cd {REPO} && python3 harness/infer_branch.py --adapter {D}/ckpt/{ten} \
        --out /content/preds_{ten}.jsonl --limit 3000
    !cp -f /content/preds_{ten}.jsonl {D}/onpolicy/     # bản cuối, đã đóng tệp
!ls -la {D}/onpolicy/
```

⚠️ Cần **ảnh tập kiểm**: `!tar xf {D}/test_images.tar -C {REPO}/harness/dg1_cache/test_ac`
(3,2 GB, ~3 phút) nếu máy ảo chưa bung.

---

## 🛟 Ô BK — CỨU HỘ, chạy được bất cứ lúc nào

Dán vào **Terminal Colab** (tiến trình riêng, chạy được cả khi nhân Python đang bận):

```bash
D=/content/drive/MyDrive/thesis; R=/content/ws/thesis
mkdir -p $D/onpolicy/branches
cp -f /content/desc_train_s2.jsonl        $D/onpolicy/            2>/dev/null
cp -f /content/preds_*onpolicy*.jsonl     $D/onpolicy/            2>/dev/null
cp -f $R/harness/dg1_cache/train_ac/branches/*onpolicy*.json \
      $R/harness/dg1_cache/train_ac/branches/dataset_info.json \
      $D/onpolicy/branches/                                       2>/dev/null
ls -la $D/onpolicy $D/onpolicy/branches
wc -l $D/onpolicy/*.jsonl 2>/dev/null
```

**Thứ nào KHÔNG cần cứu:** `ckpt/min_onpolicy_seed101` và `ckpt/ce2_onpolicy_seed101` — chúng
đã nằm thẳng trên Drive và LLaMA-Factory ghi điểm lưu mỗi `save_steps: 100` bằng cách tạo rồi
**đóng** tệp, nên FUSE đẩy lên trọn vẹn. Khác hẳn tệp mở chế độ `"a"` của khâu sinh câu.

⚠️ Giá một lần mất máy, tính theo `save_steps: 100`: mất tối đa **100 bước × 21 s ≈ 35 phút**
train, cộng ~25–35 phút dựng lại máy và ~15–30 phút mã hoá lại token. Không phải cả lượt.

---

## O6 — cổng khai báo, và luật quyết đã khoá ở (x11d)

```python
!cd {REPO} && python3 harness/gate_desc_acc.py \
    {D}/preds_s2_seed101.jsonl \
    /content/preds_ce2_onpolicy_seed101.jsonl \
    /content/preds_min_onpolicy_seed101.jsonl
```

**Đại lượng chính:** `Δ_desc = MIN-ONPOLICY − CE2-ONPOLICY` ở cột **CẢ HAI ĐÚNG**.
Mốc so là MIN-DESC hiện tại: **MIN 60,6 − CE2 59,8 = +0,80 pp**.

| kết quả | làm gì |
|---|---|
| `Δ_desc` ≥ **+2,80** (tức hơn mốc +0,80 ít nhất 2,0) | ✅ chi 10,8 h Kaggle chấm executability |
| `Δ_desc` < +2,80 | ⛔ **KHÔNG chấm.** Ghi vào bài như một nhánh của ablation nguồn cặp |

⛔ Ngưỡng +2,0 pp khoá ở **(x11d)**, trước khi có số. Không nới.
⛔ Dù ra chiều nào cũng **báo cả ba nhánh** (heuristic · on-policy · CE2) — cam kết (x11d).

---

## Nếu O2 trượt cổng

Đó **không** phải thất bại của phiên. Nó là kết quả: *nguồn vế âm on-policy không dựng được
tập cặp hợp lệ dưới ràng buộc đã khoá*. Ghi vào `report/106` mục (x11) phần kết quả, và bài vẫn
có ablation hai nhánh (heuristic · CE2) như hiện tại. Chi phí biết mình sai: **4 giờ, không phải
13,5 giờ.**
