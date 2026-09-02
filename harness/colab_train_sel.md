# SPRINT `gui_sel` — sáu lượt train trên Colab

> Nguồn lệnh: **`report/132`** · **`report/128` §4** (cấu hình) · skill `soict-paper`.
> Cấu hình: **`harness/train_config_sel.yaml`** — khác `train_config.yaml` đúng bốn khoá
> (`cutoff_len` 2560→3072 · `num_train_epochs` 2→1 · `dataset` · `output_dir`).
> Backbone **Qwen2.5-VL-3B**, không phải Qwen3-VL-4B (`report/128` §3).

## Sáu lượt

| # | dataset | seed | vai trò |
|---|---|---|---|
| 1 | `gui_sel` | 101 | nhánh chính |
| 2 | `gui_sft_match` | 101 | đối chứng của Δ_sel |
| 3 | `gui_s1_match` | 101 | mốc dưới |
| 4–6 | như trên | **202** | |

⛔ **Không hy sinh hạt giống 202** — đòn đã hạ bài FAIR xuống borderline.
Thứ tự hy sinh nếu vỡ lịch: cắt `gui_s1_match` trước, hạt 202 cuối cùng.

---

## ⛔⛔ BA LUẬT — vi phạm là mất tiền thật (đã mất 16 compute unit ngày 2/9)

1. **`Popen` phải có `start_new_session=True`.** Thiếu ⇒ train cùng process group với kernel ⇒
   bấm Stop **ô bất kỳ** là gửi SIGINT sang train. Lượt 1 chết ở bước 747 vì đúng chuyện này.
2. **KHÔNG bấm Stop ô nào khi train chạy.** Cần chạy ô khác thì mở **notebook thứ hai** hoặc
   **Terminal Colab**. Ô vòng lặp làm mọi ô khác xếp hàng — phản xạ bấm Stop chính là cái bẫy.
3. **Theo dõi bằng Terminal, không bằng ô notebook.** Và đọc đúng nguồn:

| số | lấy ở đâu | tin được? |
|---|---|---|
| bước · tốc độ · giờ còn lại | `.log` local (tqdm → stderr) | ✅ |
| loss · lr | `trainer_log.jsonl` | ✅ |
| `remaining_time` · `elapsed_time` | `trainer_log.jsonl` | ⛔ **sai sau resume** — trainer chia elapsed cho `current_steps` thay vì số bước thật của phiên |

---

## Ô S1 — cài gói ▸ rồi **Restart runtime**

```python
import torch
assert torch.cuda.is_available(), "⛔ CHƯA BẬT GPU — Runtime ▸ Change runtime type ▸ A100"
print("card:", torch.cuda.get_device_name(0))
```

```bash
%cd /content
!git clone https://github.com/hiyouga/LLaMA-Factory.git
%cd LLaMA-Factory
!git checkout c4e09c7cbe18
!pip -q install -e ".[torch,metrics,qwen]"
!pip -q install bitsandbytes
```

```python
import importlib.metadata as md
print("bitsandbytes:", md.version("bitsandbytes"))   # phải ra số, không được ném lỗi
```

⚠️ **`bitsandbytes` phải cài RỜI.** Extras `[bitsandbytes]` không kéo được gói, và lỗi chỉ nổ ở
`configure_quantization` — tức **sau** khi đã nạp xong dữ liệu, mất 15–25 phút mới biết.

▸ **Restart runtime** rồi mới chạy ô sau.

---

## Ô S2 — dữ liệu + ảnh (15–25 phút)

```python
from google.colab import drive; drive.mount('/content/drive')
import os, zipfile, shutil, subprocess, json, torch
D, WS = "/content/drive/MyDrive/thesis", "/content/ws"
os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_rented.zip").extractall(WS)
REPO = f"{WS}/thesis"; os.chdir(REPO)
TR  = f"{REPO}/harness/dg1_cache/train_ac"
dem = lambda d: len(os.listdir(d)) if os.path.isdir(d) else 0

# ba nhánh SEL dựng sẵn trên WSL — KHÔNG dựng lại trên Colab (rủi ro lệch lượt OCR)
!tar xzf {D}/branches_sel.tar.gz -C {REPO}

# ⚠️ CHÉP tar về đĩa máy ảo rồi mới bung. Bung thẳng qua FUSE hay đứt giữa chừng
#    ("Transport endpoint is not connected") và phải làm lại từ đầu.
os.makedirs(f"{TR}/images", exist_ok=True)
if dem(f"{TR}/images") >= 64567:
    print("ảnh đã đủ — bỏ qua")
else:
    for i in range(4):
        tmp = f"/content/p{i}.tar"
        shutil.copy(f"{D}/train_images_p{i}.tar", tmp)
        subprocess.run(["tar","xf",tmp,"-C",f"{TR}/images"], check=True)
        os.remove(tmp)
        print(f"p{i} xong · {dem(f'{TR}/images'):,} ảnh")

print("\ncard    :", torch.cuda.get_device_name(0))
print("ảnh dạy :", dem(f"{TR}/images"), "← cần 64.567")
for n in ("gui_sel","gui_sft_match","gui_s1_match"):
    print(f"{n:16s}:", len(json.load(open(f"{TR}/branches/{n}.json"))), "← cần 64.567")
```

**Bốn dòng phải đúng** trước khi đi tiếp.

---

## Ô S2b — config

`thesis_rented.zip` là ảnh chụp kho ngày 25/8, cũ hơn config này, nên thường **thiếu**.

```python
import os, yaml
CFG_SRC = f"{REPO}/harness/train_config_sel.yaml"
if not os.path.exists(CFG_SRC):
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
    print("đã ghi config (thiếu trong gói)")
c = yaml.safe_load(open(CFG_SRC))
print("cutoff/epoch:", c["cutoff_len"], "/", c["num_train_epochs"], "← cần 3072 / 1.0")
```

---

## Ô S3 — chọn lượt, tiền bay

```python
import os, yaml, json

# ⚠️⚠️ HAI DÒNG DUY NHẤT ĐỔI GIỮA SÁU LƯỢT ⚠️⚠️
NHANH = "gui_sel"        # gui_sel | gui_sft_match | gui_s1_match
SEED  = 101              # 101 | 202
# ────────────────────────────────────────────

OUT = f"/content/drive/MyDrive/thesis/ckpt/{NHANH}_seed{SEED}"
cfg = yaml.safe_load(open(CFG_SRC))
cfg.update(dataset=NHANH, seed=SEED, output_dir=OUT,
           dataset_dir=f"{TR}/branches", preprocessing_num_workers=8)
CFG = "/content/cfg_sel.yaml"
yaml.safe_dump(cfg, open(CFG, "w"), sort_keys=False, allow_unicode=True)

goc = yaml.safe_load(open(CFG_SRC))
CHO_PHEP = {"dataset","seed","output_dir","dataset_dir","preprocessing_num_workers"}
khac = {k for k in set(cfg)|set(goc) if cfg.get(k) != goc.get(k)}
n     = len(json.load(open(f"{TR}/branches/{NHANH}.json")))
p_anh = json.load(open(f"{TR}/branches/{NHANH}.json"))[0]["images"][0]
ck    = sorted(d for d in os.listdir(OUT) if d.startswith("checkpoint")) if os.path.isdir(OUT) else []

print("① cfg đúng nhánh        :", cfg["dataset"] == NHANH, cfg["dataset"])
print("② chỉ khoá được phép đổi:", khac <= CHO_PHEP, sorted(khac - CHO_PHEP) or "✅")
print("③ KHÔNG sót max_steps   :", "max_steps" not in cfg)
print("④ checkpoint hiện có    :", ck or "(rỗng — lượt mới)")
print("⑤ số mẫu                :", n, "← cần 64.567")
print("⑥ cutoff / epoch        :", cfg["cutoff_len"], "/", cfg["num_train_epochs"], "← cần 3072 / 1.0")
print("⑦ ảnh mở được           :", os.path.exists(p_anh))
print("   ~ số bước            :", -(-n // 16), "← cần 4036")
```

**Đọc dòng ④ theo tình huống:**

| | ④ phải là |
|---|---|
| lượt mới | **rỗng**. Không rỗng ⇒ nó chạy tiếp checkpoint cũ, log vẫn in `Training completed` trông y như đạt |
| chạy lại sau mất máy | **có checkpoint** — đó chính là cái để tiếp tục |

---

## Ô S4 — TRAIN

```python
import subprocess, os
assert not any("llamafactory-cli" in p for p in
               subprocess.run(["bash","-lc","ps -eo args"],capture_output=True,text=True).stdout.split("\n")), \
       "⛔ ĐANG CÓ MỘT LƯỢT CHẠY — đừng phóng lần hai"
os.makedirs(OUT, exist_ok=True)
LOG = f"/content/train_{NHANH}_{SEED}.log"
f   = open(LOG, "a")

# start_new_session : tách process group, Stop ô nào cũng không giết train  (luật ①)
# PYTHONUNBUFFERED  : dòng {'loss': …} in ra stdout bị đệm 8 KB ⇒ phải ~1.600 bước mới
#                     xả một lần, nhìn tưởng loss đứng yên hàng giờ
env = {**os.environ, "PYTHONUNBUFFERED": "1"}
P = subprocess.Popen(["llamafactory-cli","train",CFG], stdout=f, stderr=subprocess.STDOUT,
                     start_new_session=True, env=env)
print("PID", P.pid, "· log", LOG)
```

⛔ **15–25 phút đầu là mã hoá token, trông y hệt treo. Đừng dán lại ô này.**

Sau ~4 phút, nếu là lượt chạy tiếp thì kiểm:

```python
import subprocess, time
time.sleep(240)
print(subprocess.run(["bash","-lc",f"tail -5 {LOG}"], capture_output=True, text=True).stdout)
```

Phải thấy `Resuming training from checkpoint with epoch 0 and global step <N>`.
Thấy `0/4036` là nó train lại từ đầu ⇒ dừng ngay.

---

## Ô S5 — đồng bộ Drive ⚠️ chạy NGAY sau S4

```python
import threading, shutil, time, os
def dongbo():
    while True:
        try:
            for fn in ("trainer_log.jsonl","trainer_state.json","all_results.json"):
                p = os.path.join(OUT, fn)
                if os.path.exists(p): shutil.copy(p, p + ".snap")
        except Exception as e: print("sync:", e, flush=True)
        time.sleep(300)
threading.Thread(target=dongbo, daemon=True).start()
print("đã bật đồng bộ 5 phút/lần")
```

Dùng daemon thread nên ô kết thúc ngay, không chiếm chỗ.

⚠️ Tệp mở chế độ `"a"` chưa đóng lần nào thì FUSE **chưa đẩy lên cloud**, và `ls` vẫn hiện tệp
như thường ⇒ mất máy là mất sạch, không có dấu hiệu báo trước. Chụp sang **tên khác** bằng `cp`
mới buộc Drive tải lên trọn vẹn.

---

## Ô S6 — cảnh báo ntfy + healthchecks (free)

```python
import threading, time, os, re, urllib.request

PING  = "https://hc-ping.com/ĐIỀN-UUID"      # healthchecks.io, Period 5' Grace 10'
TOPIC = "https://ntfy.sh/ĐIỀN-TOPIC"         # đặt tên khó đoán, app bật Override DND
LOG   = f"/content/train_{NHANH}_{SEED}.log"
JS    = os.path.join(OUT, "trainer_log.jsonl")
LAP, NHIP = 40, 45                            # réo tối đa 40 lần × 45 giây

def bao(tieu_de, noi_dung, uu_tien="max", tag="rotating_light"):
    try:
        urllib.request.urlopen(urllib.request.Request(
            TOPIC, data=noi_dung.encode(),
            headers={"Title": tieu_de, "Priority": uu_tien, "Tags": tag}), timeout=10)
    except Exception as e: print("ntfy:", e, flush=True)

def ping(duoi="", than=b""):
    try: urllib.request.urlopen(PING + duoi, data=than, timeout=10)
    except Exception as e: print("hc:", e, flush=True)

def dang_chay():
    return any("llamafactory-cli" in p for p in os.popen("ps -eo args").read().split("\n"))

def doc():
    try:
        with open(LOG, encoding="utf-8", errors="ignore") as f:
            f.seek(max(0, os.path.getsize(LOG) - 200_000)); txt = f.read()
    except OSError:
        return 0, "?", False
    b = re.findall(r"(\d+)/4036", txt)
    lo = "?"
    try:
        import json as _j
        lo = _j.loads(open(JS, encoding="utf-8").readlines()[-1]).get("loss", "?")
    except Exception: pass
    return (int(b[-1]) if b else 0), lo, ("train_runtime" in txt)

def canh():
    while True:
        try:
            buoc, loss, xong = doc()
            if dang_chay():
                ping(than=f"buoc {buoc}/4036 loss {loss}".encode())
                time.sleep(60); continue
            if xong or buoc >= 4036:
                bao(f"✅ XONG {NHANH}/{SEED}", f"Đủ {buoc}/4036 bước.", "high", "white_check_mark")
                ping("/fail", f"HOAN TAT {buoc}/4036".encode()); return
            ping("/fail", f"CHET o buoc {buoc}".encode())
            for i in range(1, LAP + 1):
                if dang_chay():
                    bao("🟢 Đã chạy lại", f"Tiếp từ bước {doc()[0]}", "default", "green_circle")
                    return
                bao(f"⛔ CHẾT {NHANH}/{SEED} ({i}/{LAP})",
                    f"Dừng ở {buoc}/4036, loss {loss}. Vào Colab chạy lại.")
                time.sleep(NHIP)
            return
        except Exception as e:
            print("canh:", e, flush=True); time.sleep(60)

threading.Thread(target=canh, daemon=True).start()
bao("🔔 Đã bật canh", f"{NHANH}/{SEED} đang chạy", "low", "bell")
print("đã bật cảnh báo")
```

Free hoàn toàn: healthchecks Hobbyist (20 check · 100 log entry) + ntfy không đăng ký.
Mỗi lượt tốn ~840 ping và tối đa 42 tin. ⛔ Phone Call / SMS / WhatsApp mới mất phí.

---

## Theo dõi — Terminal Colab, KHÔNG dùng ô notebook

```bash
L=/content/train_gui_sel_101.log
J=/content/drive/MyDrive/thesis/ckpt/gui_sel_seed101/trainer_log.jsonl
while true; do
  B=$(grep -oE '[0-9]+/4036' $L | tail -1 | cut -d/ -f1)
  S=$(grep -oE '[0-9.]+s/it' $L | tail -1 | tr -d 's/it')
  LO=$(tail -1 $J 2>/dev/null | grep -oE '"loss": [0-9.]+' | cut -d' ' -f2)
  SEC=$(python3 -c "print(int((4036-$B)*$S))" 2>/dev/null)
  printf "%s  bước %5s/4036  loss %-8s  %ss/b  còn %sh%02dm\n" \
    "$(TZ=Asia/Ho_Chi_Minh date +%H:%M)" "$B" "${LO:-?}" "$S" $((SEC/3600)) $(((SEC%3600)/60))
  sleep 180
done
```

Thoát bằng Ctrl+C — an toàn, train nằm ở process group riêng.

⚠️ Con số `s/it` ngay sau resume **không tin được**: tqdm tính trung bình từ lúc khởi động, mà
lúc đó nó tua nhanh qua các batch đã học. Đợi ~200 bước sau resume mới đúng.

---

## 🔧 MẤT MÁY — khôi phục

```python
from google.colab import drive; drive.mount('/content/drive')
import os
REPO = "/content/ws/thesis"; TR = f"{REPO}/harness/dg1_cache/train_ac"
CK   = "/content/drive/MyDrive/thesis/ckpt/gui_sel_seed101"
dem  = lambda d: len(os.listdir(d)) if os.path.isdir(d) else 0
print("kho        :", os.path.isdir(REPO))
print("ảnh dạy    :", dem(f"{TR}/images"), "← cần 64.567")
print("config     :", os.path.exists(f"{REPO}/harness/train_config_sel.yaml"))
print("checkpoint :", sorted(d for d in os.listdir(CK) if d.startswith("checkpoint")) if os.path.isdir(CK) else "⛔")
```

| kết quả | làm gì |
|---|---|
| kho **True**, ảnh **64.567** | chỉ mất kernel — chạy lại **S3 → S4 → S5 → S6**, ~2 phút |
| kho **False** hoặc ảnh thiếu | máy ảo mới — chạy lại **S1 → S2 → S2b → S3 → S4 → S5 → S6**, ~30 phút |

Checkpoint trên Drive vẫn nguyên trong cả hai trường hợp ⇒ mất tối đa **200 bước** (~42 phút).

---

## ⛔ LUẬT CHẤM — sau khi train xong

| nhánh | cờ |
|---|---|
| `gui_sel` · `gui_sft_match` | `--cands .../test_ac/candidates.jsonl` |
| `gui_s1_match` · S1 · S2 · MIN-DESC · CE2 | *(bỏ trống)* |

```bash
python harness/infer_branch.py --adapter <ckpt> --out runs/preds_gui_sel_seed101.jsonl \
    --cands harness/dg1_cache/test_ac/candidates.jsonl
```

⛔ **Quên cờ là hỏng câm** — đo 2/9: **499/500 mẫu dựng sai câu nhắc**. Mô hình được dạy chọn từ
menu, lúc chấm không thấy menu nào. Nó vẫn sinh chữ, thước vẫn ra điểm, log không báo gì.
Dòng đầu ra in rõ chế độ đang dùng — **đọc dòng đó**, đừng tin lệnh mình vừa gõ.

⚠️ Tập kiểm cần `candidates.jsonl`; bản hiện có dựng **không** kèm `--all-steps`. Chấm cả bước
không chạm thì dựng lại: `build_candidates.py --split test --all-steps --max 40` (0 GPU).

## Cổng G6 — sau lượt 1, TRƯỚC khi tiêu năm lượt còn lại

```bash
python harness/gate_sel_acc.py runs/preds_gui_sel_seed101.jsonl
```

600 bước DEV có ứng viên vàng · khớp tên ∧ point ±14% · `<sel>none</sel>` tính **sai** ·
ngưỡng **≥63,6%**. ⛔ Không dùng tập test. Trượt ⇒ **dừng cả sprint**, bài đổi thành báo cáo âm.
**Không nới ngưỡng sau khi thấy điểm** — dự án đã tự khai hai lần làm vậy.

## Sau mỗi lượt

1. **Điểm lưu trọn vẹn?** Ghi dở thì bản CUỐI nhỏ hơn bản trước — so `du -h` hai `checkpoint-*`.
2. **Ghi `total_flos` và số bước** từ `trainer_state.json`.
   ⛔ Không dùng `all_results.json`: `train_loss`, `train_runtime`, `*_per_second` **sai sau resume**.
