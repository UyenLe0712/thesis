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

## ⛔⛔ BỐN LUẬT — vi phạm là mất tiền thật (đã mất 16 compute unit + 2 lần mất máy)

1. **`Popen` phải có `start_new_session=True`.** Thiếu ⇒ train cùng process group với kernel ⇒
   bấm Stop **ô bất kỳ** là gửi SIGINT sang train. Lượt 1 chết ở bước 747 vì đúng chuyện này.
✅ **ĐÃ KIỂM CHỨNG 3/9, 03:5x — luật ① chạy đúng như thiết kế.** Bấm Stop ô S7 rồi đo ngay:
tiến trình `llamafactory-cli` vẫn còn, `grep -c KeyboardInterrupt` = **0**, log tăng **+107
byte/phút**. ⇒ Với `start_new_session=True`, Stop một ô KHÔNG giết train. Đổi lại bằng 60
giây kiểm, không phải bằng một lượt train. ⚠️ Đo trong khâu mã hoá token; SIGINT lan theo
process group nên kết luận không phụ thuộc giai đoạn, nhưng vẫn nên hạn chế bấm Stop.

2. **KHÔNG bấm Stop ô nào khi train chạy.** Cần chạy ô khác thì mở **notebook thứ hai** hoặc
   **Terminal Colab**. Ô vòng lặp làm mọi ô khác xếp hàng — phản xạ bấm Stop chính là cái bẫy.
3. **Theo dõi bằng Terminal, không bằng ô notebook.** Và đọc đúng nguồn:

| số | lấy ở đâu | tin được? |
|---|---|---|
| bước · tốc độ · giờ còn lại | `.log` local (tqdm → stderr) | ✅ |
| loss · lr | `trainer_log.jsonl` | ✅ |
| `remaining_time` · `elapsed_time` | `trainer_log.jsonl` | ⛔ **sai sau resume** — trainer chia elapsed cho `current_steps` thay vì số bước thật của phiên |

---

**④ PHẢI có một ô notebook đang chạy suốt lượt — đó là ô S7.** S5/S6 dùng daemon thread nên
ô kết thúc ngay; theo dõi bằng Terminal thì trình duyệt không có tương tác nào. Notebook rỗi
⇒ Colab ngắt vì *inactivity* sau ~90 phút. Đêm 2–3/9 mất máy **hai lần** đúng kiểu này: máy
dựng lại ~02:00, chết trước 03:28 — chừng 88 phút. Lượt chiều 2/9 sống lâu chỉ nhờ liên tục
có người bấm ô.

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
save_steps: 100
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

⛔ **~45 phút đầu KHÔNG có thanh tiến độ nào, trông y hệt treo. Đừng dán lại ô này.**
Đo 2/9: mã hoá token **41 phút** (11:58 → 12:39), rồi nạp trọng số 4-bit thêm vài phút.
Thứ tự log, chờ đúng dòng cuối:

```
Loading dataset → Converting format → Running tokenizer (41 ph) → in một mẫu
→ Quantizing model to 4 bit → loading weights file
→ ***** Running training *****
→ Resuming training from checkpoint with epoch 0 and global step <N>   ← dòng cần thấy
→ thanh tiến độ
```

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

PING  = "https://hc-ping.com/639a0628-dc09-49d8-8d33-560edb2e497d"   # healthchecks, Period 5' Grace 10'
TOPIC = "https://ntfy.sh/soict-uyen-7k3m9x"                          # ⚠️ phải TRÙNG topic đã
                                                                     # subscribe trong app ntfy
LOG   = f"/content/train_{NHANH}_{SEED}.log"
JS    = os.path.join(OUT, "trainer_log.jsonl")
LAP, NHIP = 40, 45                            # réo tối đa 40 lần × 45 giây

def bao(tieu_de, noi_dung, uu_tien="max", tag="rotating_light"):
    # ⛔ Header HTTP chỉ nhận latin-1: emoji VÀ dấu tiếng Việt trong Title đều ném
    #    UnicodeEncodeError ⇒ cảnh báo im lặng đúng lúc cần nhất. Tiêu đề để ASCII
    #    thuần, emoji do ntfy tự render từ Tags. Body thì encode utf-8 nên thoải mái.
    try:
        urllib.request.urlopen(urllib.request.Request(
            TOPIC, data=noi_dung.encode("utf-8"),
            headers={"Title": tieu_de.encode("ascii", "ignore").decode(),
                     "Priority": uu_tien, "Tags": tag}), timeout=10)
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
                bao(f"XONG {NHANH}/{SEED}", f"Đủ {buoc}/4036 bước.", "high", "white_check_mark")
                ping("/fail", f"HOAN TAT {buoc}/4036".encode()); return
            ping("/fail", f"CHET o buoc {buoc}".encode())
            for i in range(1, LAP + 1):
                if dang_chay():
                    bao("Da chay lai", f"Tiếp từ bước {doc()[0]}", "default", "green_circle")
                    return
                bao(f"CHET {NHANH}/{SEED} ({i}/{LAP})",
                    f"Dừng ở {buoc}/4036, loss {loss}. Vào Colab chạy lại.")
                time.sleep(NHIP)
            return
        except Exception as e:
            print("canh:", e, flush=True); time.sleep(60)

threading.Thread(target=canh, daemon=True).start()
bao("Da bat canh", f"{NHANH}/{SEED} đang chạy", "low", "bell")
print("đã bật cảnh báo")
```

Free hoàn toàn: healthchecks Hobbyist (20 check · 100 log entry) + ntfy không đăng ký.
Mỗi lượt tốn ~840 ping và tối đa 42 tin. ⛔ Phone Call / SMS / WhatsApp mới mất phí.

---

## Ô S7 — GIỮ NHỊP + theo dõi ⚠️ BẮT BUỘC, để nguyên chạy tới hết lượt

⛔ **Đây là ô đã thiếu trong đêm 2–3/9 và làm mất máy hai lần.** S5 và S6 đều dùng
`daemon=True` nên ô **kết thúc ngay**; theo dõi thì lại làm bên Terminal. Kết quả: notebook
**không còn ô nào đang chạy**, trình duyệt cũng không có tương tác nào, và Colab ngắt máy vì
*inactivity* sau khoảng 90 phút. Lượt chiều 2/9 sống lâu chỉ vì lúc đó liên tục có người bấm ô.

Ô này chạy **foreground** nên kernel luôn bận. Chạy nó SAU S6 và **để nguyên**, đừng bấm gì.

```python
import time, os, re, json, glob, subprocess

LOGF = f"/content/train_{NHANH}_{SEED}.log"
TRUOC, IM, LAN = 0, 0, 0

def gio(cong=0):                               # đồng hồ máy chạy UTC, +7 ra giờ VN
    return time.strftime("%H:%M:%S", time.gmtime(time.time() + 7*3600 + cong))

def gpu():
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total,"
                            "utilization.gpu,temperature.gpu,power.draw",
                            "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=10).stdout.strip()
        u, t, g, c, w = [x.strip() for x in r.split(",")]
        return f"VRAM {int(u)/1024:.1f}/{int(t)/1024:.0f} GB · GPU {g}% · {c}°C · {float(w):.0f} W"
    except Exception as e:
        return f"nvidia-smi lỗi: {e}"

def lay(txt, mau):
    m = re.findall(mau, txt)
    return m[-1] if m else None

def so_hoc():
    """loss · lr · grad_norm · epoch — lấy từ `trainer_state.json` của checkpoint MỚI NHẤT.

    ⛔ KHÔNG lấy từ tệp `.log`. Đo 24/8 trên lượt thật: S4 phóng bằng `Popen(stdout=file)`
    nên stdout không phải terminal; HF chỉ in dict {'loss': …} QUA tqdm, mà ở chế độ đó
    tqdm không ghi dòng ấy ⇒ log **không có** số học nào, dù vẫn có thanh tiến độ.
    ⛔ Cũng KHÔNG lấy từ `trainer_log.jsonl` trên Drive: FUSE không cập nhật nội dung khi
    ghi thêm, số ở đó đứng yên hàng giờ (luật ③).
    ⚠️ Đánh đổi: checkpoint chỉ ghi mỗi `save_steps` (100 bước ≈ 21 phút) nên số học TRỄ
    hơn cột bước — vì vậy in kèm `@N` là bước mà số đó thuộc về."""
    try:
        ck = sorted(glob.glob(OUT + "/checkpoint-*"), key=lambda q: int(q.rsplit("-", 1)[1]))
        if not ck:
            return {}
        st = json.load(open(ck[-1] + "/trainer_state.json", encoding="utf-8"))
        h = [l for l in st["log_history"] if l.get("loss") is not None]
        return h[-1] if h else {}
    except Exception:
        return {}

while True:
    try:
        with open(LOGF, encoding="utf-8", errors="ignore") as f:
            f.seek(max(0, os.path.getsize(LOGF) - 300_000)); txt = f.read()
    except OSError:
        print(gio(), "chưa có log", flush=True); time.sleep(60); continue

    b = re.findall(r"(\d+)/4036", txt)
    if not b:
        cuoi = txt.replace("\r", "\n").strip().split("\n")[-1][-90:]
        print(gio(), "[khởi động]", cuoi, flush=True)
    else:
        buoc = int(b[-1])
        sit  = float(lay(txt, r"([0-9.]+)s/it") or 12.5)
        d    = so_hoc()
        f4   = lambda k, n=4: f"{d[k]:.{n}f}" if isinstance(d.get(k), (int, float)) else "?"
        lr   = f"{d['learning_rate']:.3e}" if isinstance(d.get("learning_rate"), float) else "?"
        con  = int((4036 - buoc) * sit)
        # ~16 mẫu/bước; mỗi mẫu 1.272 token ảnh + ~541 token chữ (p50 đo 2/9)
        tok  = 16 * 1813 / sit
        tien = "   —" if TRUOC == 0 else f"{buoc-TRUOC:+4d}"    # lượt đầu chưa có mốc để trừ
        print(f"{gio()}  bước {buoc:>5}/4036 ({buoc*100//4036:>2}%) {tien}  "
              f"loss {f4('loss'):<7}|g| {f4('grad_norm',3):<6}lr {lr:<10}ep {f4('epoch',3):<6}"
              f"@{int(d.get('step', 0)):<5} {sit:.1f}s/b ≈{tok:.0f}tok/s  "
              f"còn {con//3600}h{con%3600//60:02d}m  xong ~{gio(con)[:5]}", flush=True)
        if LAN % 10 == 0:                        # 10 phút một lần cho đỡ rối
            print(f"{' '*10}└ {gpu()}", flush=True)
        IM = IM + 1 if buoc == TRUOC else 0
        TRUOC = buoc; LAN += 1
        if IM >= 3:
            print("⚠️ ba lượt liền không tiến bước — mở Terminal: ps -eo args | grep llamafactory",
                  flush=True)
        if buoc >= 4036 or "train_runtime" in txt:
            print("✅ XONG — bắt đầu thủ tục đóng lượt", flush=True); break
    time.sleep(300)

# ── THỦ TỤC ĐÓNG LƯỢT — chạy không cần người ngồi canh ────────────────────────
import json
time.sleep(90)                                    # cho trainer ghi nốt adapter cuối

ad  = os.path.join(OUT, "adapter_model.safetensors")
ok  = os.path.exists(ad) and os.path.getsize(ad) > 1_000_000
tt  = os.path.join(OUT, "trainer_state.json")
st  = json.load(open(tt)) if os.path.exists(tt) else {}
tin = (f"buoc {st.get('global_step','?')} · flos {st.get('total_flos','?')} · "
       f"adapter {os.path.getsize(ad)/1e6:.1f} MB" if ok else "⛔ THIEU ADAPTER")
print("adapter:", ok, "·", tin, flush=True)

try:
    bao(f"XONG {NHANH}/{SEED}" if ok else f"LOI {NHANH}/{SEED}", tin,
        "high", "white_check_mark" if ok else "rotating_light")
except Exception as e:
    print("ntfy:", e, flush=True)

if ok:
    try:
        from google.colab import drive
        drive.flush_and_unmount()                 # ⛔ BẮT BUỘC: FUSE giữ tệp trong đệm,
        print("đã đẩy Drive lên cloud", flush=True)  # `ls` vẫn hiện tệp như thường
        time.sleep(60)
    except Exception as e:
        print("flush lỗi:", e, "— KHÔNG trả máy, vào kiểm bằng tay", flush=True)
    else:
        try:
            from google.colab import runtime
            runtime.unassign()                    # trả máy ⇒ ngừng tính compute unit
        except Exception as e:
            print("unassign lỗi:", e, "— tắt máy bằng tay ở Runtime ▸ Disconnect", flush=True)
else:
    print("⛔ KHÔNG trả máy — adapter thiếu, vào kiểm bằng tay", flush=True)
```

**Đọc sáu cột này:**

| cột | nghĩa | ngưỡng đáng ngờ |
|---|---|---|
| `+N` | bước tiến trong 60 giây | `+0` **ba lần liền** (một lần thì không) |
| `loss` | trung bình 20 bước gần nhất | tăng đều nhiều khối · nhảy hàng đơn vị · `nan` |
| `|g|` | `grad_norm`, độ lớn gradient | vọt lên hàng chục · về đúng `0` · `nan` |
| `lr` | lịch cosine đang ở đâu | không giảm dần theo bước |
| `ep` | phần epoch đã duyệt | phải bò từ 0 tới **1.0**, không hơn |
| `≈tok/s` | thông lượng **ước tính** | tụt quá nửa so với lúc đầu |

⚠️ `tok/s` là **ước tính**, không phải số trainer báo: lấy 16 mẫu/bước × (1.272 token ảnh +
541 token chữ ở p50) chia cho `s/it`. Dùng để so tương đối giữa hai thời điểm, đừng trích vào
bài. Dòng `└ VRAM …` in 10 phút một lần, lấy thẳng từ `nvidia-smi`.

⚠️ Ô này in thẳng ra notebook nên **mọi ô khác sẽ xếp hàng sau nó**. Cần chạy lệnh gì thì mở
**Terminal Colab**, đừng bấm Stop. Về lý thuyết Stop bây giờ không giết train nữa vì S4 đã có
`start_new_session=True`, nhưng điều đó **chưa được kiểm chứng lần nào** — đừng lấy lượt train
đang chạy ra làm phép thử.

---

## Theo dõi — Terminal Colab, KHÔNG dùng ô notebook

Mở **Terminal** (biểu tượng `>_` góc dưới trái Colab), dán nguyên khối:

```bash
L=/content/train_gui_sel_101.log; P=0
while true; do
  T=$(TZ=Asia/Ho_Chi_Minh date +%H:%M:%S)
  B=$(tail -c 300000 $L | grep -oE '[0-9]+/4036' | tail -1 | cut -d/ -f1)
  if [ -z "$B" ]; then
    printf "%s  [khởi động] %s\n" "$T" "$(tail -c 120 $L | tr '\r' '\n' | tail -1)"
  else
    S=$(tail -c 300000 $L | grep -oE '[0-9.]+s/it' | tail -1 | tr -d 's/it')
    LO=$(tail -c 300000 $L | grep -oE "'loss': [0-9.]+" | tail -1 | cut -d' ' -f2)
    SEC=$(python3 -c "print(int((4036-$B)*${S:-12.5}))")
    printf "%s  bước %5s/4036 (%2d%%)  +%-3s  loss %-7s  %ss/b  còn %dh%02dm  xong ~%s\n" \
      "$T" "$B" $((B*100/4036)) "$((B-P))" "${LO:-?}" "${S:-?}" \
      $((SEC/3600)) $(((SEC%3600)/60)) "$(TZ=Asia/Ho_Chi_Minh date -d "+$SEC seconds" +%H:%M)"
    P=$B
  fi
  sleep 60
done
```

Đọc bằng **cột `+N`** — số bước tiến được trong 60 giây vừa qua. Ở 12,5 s/bước thì `+4` hoặc
`+5` là bình thường. **`+0` hai lần liên tiếp mới là dấu hiệu đáng nghi**, một lần thì không.

⚠️ Ba điều đã trả giá:
· Loss lấy từ **log local**, KHÔNG từ `trainer_log.jsonl` trên Drive — FUSE không cập nhật nội
  dung khi ghi thêm, số ở đó đứng yên hàng giờ dù train vẫn chạy (luật ③).
· Con số `s/it` ngay sau resume **không tin được**: tqdm tính trung bình từ lúc khởi động, mà
  lúc đó nó tua nhanh qua các batch đã học. Đợi ~200 bước sau resume mới đúng.
· Thoát vòng lặp bằng **Ctrl+C** — an toàn, vì train nằm ở process group riêng
  (`start_new_session=True`). Nhưng **Ctrl+C trong Terminal thì được, bấm Stop ô notebook thì
  KHÔNG** — đó là chuyện đã mất 16 compute unit ngày 2/9.

### Xem curve loss từ đầu tới giờ

```bash
python3 - <<'EOF'
import json, glob
CK = "/content/drive/MyDrive/thesis/ckpt/gui_sel_seed101"
ds = sorted(glob.glob(CK + "/checkpoint-*"), key=lambda d: int(d.split("-")[-1]))
if not ds: raise SystemExit("chưa có checkpoint nào")
st = json.load(open(ds[-1] + "/trainer_state.json"))
h = [(r["step"], r["loss"]) for r in st["log_history"] if "loss" in r]
print(f"nguồn {ds[-1].split('/')[-1]} · {len(h)} mốc · bước {h[0][0]}-{h[-1][0]}\n")
G, gom = 100, {}
for s, l in h: gom.setdefault((s - 1) // G, []).append(l)
xs = [(k * G + G, sum(v) / len(v)) for k, v in sorted(gom.items())]
lo, hi = min(v for _, v in xs), max(v for _, v in xs)
for s, v in xs:
    print(f"{s:>5} {v:6.4f} {'#' * (int(38 * (v - lo) / (hi - lo + 1e-9)) + 1)}")
print(f"\ncao nhat {hi:.4f} · thap nhat {lo:.4f} · 200 buoc cuoi {sum(l for _, l in h[-10:]) / 10:.4f}")
EOF
```

Mỗi dòng là trung bình 100 bước. ⚠️ Nguồn là **điểm lưu**, nên nó dừng ở bội số của 200 —
phần sau điểm lưu cuối chưa có ở đây, phải đợi lần lưu kế. Đổi lại nó **đầy đủ từ bước 20**
và sống qua mọi lần mất máy, khác hẳn log local vốn mất theo máy ảo.

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

# mốc giờ điểm lưu cuối = lúc train thật sự dừng; log local cho biết bước cuối đã chạy
import time, glob, re
ds = sorted(glob.glob(f"{CK}/checkpoint-*"), key=lambda d: int(d.split("-")[-1]))
if ds:
    t = os.path.getmtime(ds[-1])
    print("lưu cuối   :", os.path.basename(ds[-1]), "lúc",
          time.strftime("%H:%M", time.localtime(t + 7*3600)), "(giờ VN)")
lg = "/content/train_gui_sel_101.log"
if os.path.exists(lg):
    b = re.findall(r"(\d+)/4036", open(lg, encoding="utf-8", errors="ignore").read())
    print("log local  :", f"bước cuối {b[-1]}" if b else "chưa có dòng bước",
          "⇒ mất", (int(b[-1]) - int(ds[-1].split("-")[-1])) if (b and ds) else "?", "bước")
else:
    print("log local  : ⛔ không còn (máy ảo mới)")
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

✅ **ĐÃ SỬA 3/9.** Tập kiểm từng chỉ có `candidates.jsonl` cho **4.463 bước chạm**, trong khi
tập dạy có cho **cả 64.567 bước** ⇒ 2.495 bước không chạm sẽ dựng câu nhắc **thiếu khối ứng
viên**, phá đúng điều kiện *"đầu vào lúc chấm phải giống hệt lúc dạy"*. Đã dựng lại bằng
`build_candidates.py --split test --all-steps --max 40` (0 GPU, ~8 phút).
⭐ Phép kiểm đã chạy: 4.463 bước chạm của bản mới **trùng khít bản cũ** — 0 bước thiếu, 0 khối
khác — nên dữ liệu đã train không bị ảnh hưởng; bản mới chỉ thêm 2.495 bước. Hai cổng tái lập
đúng số cũ: G1 **96,7%** · G2 **91,2%**. Bản cũ giữ ở `candidates_CHIBUOCCHAM_0902.bak.jsonl`.

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
