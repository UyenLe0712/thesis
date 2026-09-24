# Runbook Colab — PATA-C1: Stage S → Stage H → C1 (report/185, 186, 193)

Lượt TRẢ PHÍ duy nhất của thử nghiệm C1. Mọi thứ không cần GPU đã làm xong ở WSL/Kaggle:
13/13 unit test trên 3B thật, smoke S/H/J (`runs/pata/kaggle_smoke/`), audit box, luật KL box ≥ 0,50.

| ô | việc | máy | thời gian | dừng nếu |
|---|---|---|---|---|
| P0 | chuẩn bị ở nhà | — | 5 phút | — |
| P1 | cài gói | GPU đã chọn | 3 phút | không thấy GPU |
| P2 | Drive, mã, dữ liệu, ảnh | như trên | ~15 phút | số đếm hoặc hash lệch |
| P3 | **đo máy**: 6 update S | **L4 trước**, A100 sau nếu cần | ~10 phút/máy | — |
| P4 | chạy một chặng, chạy nền | L4 (23/9) → A100 nếu đạt | S ≈ 35 h trên L4 (50,6 s/u) · A100 chưa đo | — |
| P5 | ô theo dõi + đồng bộ Drive, **chạy tiền cảnh suốt lượt** | — | suốt lượt | NaN · tràn bộ nhớ |
| P6 | chẩn đoán sau chặng S (CE_val) | cùng máy | ~10 phút | CE_val phân kỳ |
| P7 | **cổng H** trên val400 | cùng máy | ~15 phút | **không đạt ⇒ DỪNG, không chạy C1** |
| P8 | **mốc 800 của C1** | cùng máy, chạy song song | ~20 phút | **bridge không được dùng ⇒ DỪNG** |
| P9 | hết epoch C1: sinh câu val600 bật/tắt bridge | cùng máy | ~1 h | — |
| P10 | chấm `exec` val600 (UGround) | **Kaggle T4, 0 đồng** | ~1 h | — |

⛔⛔ **BỐN LUẬT COLAB (CLAUDE.md) — vi phạm là mất tiền thật:**
① `Popen(..., start_new_session=True)` · ② **không bấm Stop ô nào** khi train đang chạy (cần ô khác thì
mở notebook thứ hai hoặc Terminal Colab) · ③ theo dõi bằng log **LOCAL** `/content/pata_*.log`, không đọc
tệp trên Drive · ④ **ô P5 phải chạy tiền cảnh suốt lượt** (không có nó Colab ngắt máy sau ~90 phút rỗi).

⛔ **Mốc giờ đọc bằng `TZ='Asia/Ho_Chi_Minh' date`** (máy WSL chạy giờ UTC).

---

## Ô P0 — chuẩn bị ở nhà (0 đồng)

1. Dựng gói (đã dựng sẵn 23/9 tối — dựng lại nếu sửa mã):
   ```
   ~/.venvs/thesis/bin/python harness/make_bundle.py pata_colab
   ```
2. Upload `_bundles/thesis_pata_colab.zip` (~26 MB) lên **`MyDrive/thesis/`** (ghi đè bản cũ nếu có).
3. Ảnh dạy: dùng lại `MyDrive/thesis/train_images_p*.tar` (~12 GB, đã có từ các lượt trước; val400/val600
   cũng nằm trong đó vì val tách từ tập dạy).
4. Tra giá **tại thời điểm chạy**: Colab → Runtime → Change runtime type → xem đơn vị/giờ của L4 và A100.

## Ô P1 — cài gói

Runtime → Change runtime type → **L4** (lần đầu, để đo ở P3).

```python
import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "bitsandbytes", "peft"], check=True)
import torch, transformers, peft, bitsandbytes
print("torch", torch.__version__, "· transformers", transformers.__version__,
      "· peft", peft.__version__, "· bnb", bitsandbytes.__version__)
assert torch.cuda.is_available(), "⛔ không có GPU"
print(torch.cuda.get_device_name(0), round(torch.cuda.get_device_properties(0).total_memory / 2**30, 1), "GB")

# ⛔ THÊM 24/9 sau khi mất máy: VM mới báo `nvrtc: failed to open libnvrtc-builtins.so.13.0` ngay khi train
#    khởi động (Qwen gọi image_grid_thw.prod(-1) trên GPU ⇒ PyTorch biên dịch kernel tại chỗ). Kiểm ở đây,
#    trong MỘT TIẾN TRÌNH CON (giống tiến trình train), và tự vá LD_LIBRARY_PATH nếu tìm được thư viện.
import glob, os
def thu_prod():
    r = subprocess.run([sys.executable, "-c",
        "import torch; a=torch.randn(64,64,device='cuda',dtype=torch.bfloat16); "
        "print(torch.tensor([[1,2,3],[2,3,4]], device='cuda').prod(-1), float((a@a).float().abs().sum())>0)"],
        capture_output=True, text=True, env=os.environ)
    return r.returncode == 0, (r.stdout + r.stderr)[-300:]
ok, msg = thu_prod()
if not ok:
    libs = glob.glob("/usr/**/libnvrtc-builtins.so*", recursive=True) + \
           glob.glob("/usr/local/lib/python3*/dist-packages/nvidia/**/libnvrtc-builtins.so*", recursive=True)
    # CHỈ thư mục có builtins khớp ĐÚNG phiên bản CUDA của torch (vd .so.13.0 cho cu130) — đừng thêm thư mục
    # toolkit (vd cuda-13.3): LD_LIBRARY_PATH đè lên thư viện torch mang theo ⇒ có thể nạp lẫn cuBLAS/cudart.
    can = f"libnvrtc-builtins.so.{torch.version.cuda}"
    dirs = sorted({os.path.dirname(x) for x in libs if x.endswith(can) and "dist-packages" in x})
    print("thêm vào LD_LIBRARY_PATH:", dirs)
    for d in dirs:
        os.environ["LD_LIBRARY_PATH"] = d + ":" + os.environ.get("LD_LIBRARY_PATH", "")
    ok, msg = thu_prod()
print("prod trên GPU (tiến trình con):", "ĐẠT" if ok else "HỎNG", msg.strip()[-120:])
assert ok, "⛔ JIT CUDA hỏng — gửi phần in ra, ĐỪNG chạy P4"
```

Ghi lại dòng phiên bản — đưa vào manifest §11.

## Ô P2 — Drive, mã, dữ liệu, ảnh

```python
from google.colab import drive; drive.mount("/content/drive")
import os, glob, json, hashlib, zipfile, subprocess
D = "/content/drive/MyDrive/thesis"
WS = "/content/ws"; os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_pata_colab.zip").extractall(WS)
REPO = f"{WS}/thesis"; os.chdir(REPO)
DR = f"{REPO}/harness/dg1_cache/train_ac"

# ── mã phải là bản đã vá 23/9 tối (cắt gradient theo nhóm + luật KL box ≥ 0,50) ──
t = open("harness/pata_train.py").read()
assert '"name": "target"' in t and "for g_ in groups" in t, "⛔ pata_train.py BẢN CŨ — upload lại gói"
assert "_mot_luong" in t and "chờ-dữ-liệu" in t, "⛔ pata_train.py thiếu bản vá nạp dữ liệu 23/9 — upload lại gói"
assert "AREA_KL_MAX = 0.50" in open("harness/pata_data.py").read(), "⛔ pata_data.py BẢN CŨ"
assert 'rec.get("kl_ok", True)' in open("harness/pata_model.py").read(), "⛔ pata_model.py BẢN CŨ"
assert "vision_grad=False" in open("harness/pata_model.py").read(), \
    "⛔ pata_model.py thiếu bản vá 24/9 (gỡ gradient thừa qua tháp thị giác) — upload lại gói"

# ── dữ liệu: hash phải khớp split_hash.json ──
h = json.load(open(f"{DR}/pata/split_hash.json"))
for f in ("train_proper.jsonl", "val400.jsonl", "val600.jsonl", "probe40.jsonl"):
    got = hashlib.sha256(open(f"{DR}/pata/{f}", "rb").read()).hexdigest()
    assert got == h[f], f"⛔ {f} lệch hash"
print("hash      : 4/4 khớp ✓  probe40", h["probe40.jsonl"][:12])
R = [json.loads(l) for l in open(f"{DR}/pata/train_proper.jsonl")]
n_kl = sum(r["kl_ok"] for r in R)
print("train     :", len(R), "chạm ·", n_kl, "kl_ok   ← cần 40189 · 39432")
assert (len(R), n_kl) == (40189, 39432)

# ── ảnh: bung tar vào local (không đọc ảnh từ Drive khi train — FUSE chậm) ──
IMG = f"{DR}/images"; os.makedirs(IMG, exist_ok=True)
if len(os.listdir(IMG)) < 64567:
    for g in sorted(glob.glob(f"{D}/train_images_p*.tar")):
        print("bung", os.path.basename(g), flush=True)
        subprocess.run(["tar", "xf", g, "-C", IMG], check=True)
can = {r["image"] for f in ("train_proper", "val400", "val600")
       for r in map(json.loads, open(f"{DR}/pata/{f}.jsonl"))}
thieu = [x for x in can if not os.path.exists(f"{DR}/{x}")]
print("ảnh       :", len(os.listdir(IMG)), "trên đĩa ·", len(can) - len(thieu), "/", len(can), "ảnh cần")
assert not thieu, f"⛔ thiếu {len(thieu)} ảnh, vd {thieu[:3]}"
CK = f"{D}/pata_ck"; os.makedirs(CK, exist_ok=True)       # điểm lưu trên Drive
print("Drive ck  :", CK)
```

**Phải in:** `hash 4/4 khớp` · `40189 chạm · 39432 kl_ok` · ảnh cần đủ.
⚠️ Nếu tar bung ra một tầng thư mục thừa (`images/images/…`) thì assert ảnh sẽ đỏ — báo lại để sửa đường dẫn.

## Ô P3 — đo máy (chạy trên L4 trước)

6 update Stage S, cấu hình thật (lô 4 × gộp 4 = 16). Update đầu có chi phí khởi động nên đọc `s/u` ở u6.

```python
import subprocess, time
def chay(cmd, log):
    env = dict(os.environ, TQDM_DISABLE="1", HF_HUB_DISABLE_PROGRESS_BARS="1",
               PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True", PYTHONUNBUFFERED="1")
    return subprocess.Popen(cmd, stdout=open(log, "a"), stderr=subprocess.STDOUT, env=env,
                            cwd=REPO, start_new_session=True)
p = chay(["python", "harness/pata_train.py", "--stage", "S", "--data-root", DR, "--bs", "4", "--accum", "4",
          "--max-updates", "6", "--log-steps", "1", "--save-steps", "1000", "--workers", "8",
          "--out", "/content/do_may_S"], "/content/do_may.log")
while p.poll() is None:
    time.sleep(30)
print("\n".join(l for l in open("/content/do_may.log").read().splitlines() if "u6/" in l or "Error" in l))
```

**Luật chọn máy (CLAUDE.md, user chốt 9/9):** gọi `t_L4`, `t_A100` là `s/u` ở u6.
- Chỉ đo L4 được thì ghi lại `t_L4`, rồi đổi runtime sang **A100**, chạy lại P1 → P3.
- **`t_L4 / t_A100 ≤ 1,5` ⇒ chọn L4** cho cả ba chặng. **> 1,5 ⇒ A100.**
- Chặng H forward chỉ tới block 17 và không học LoRA — nếu S phải lên A100, vẫn đo riêng H trên L4
  (thay `--stage S` bằng H cần một điểm lưu S, nên làm sau khi có S; xem P4).
- VRAM đỉnh đo trên Kaggle ≤ 5,4 GB (lô 2) ⇒ L4 22 GB thừa bộ nhớ; không cần lo tràn.

**Ước giờ theo `s/u` đo được:** S ≈ 2.512 × s/u · H ≈ 2.465 × s/u × ~0,76 · C1 ≈ 2.512 × s/u.
Ghi con số vào bảng đầu runbook trước khi bấm lượt thật.

## ⭐ Đo máy thực tế + ĐỔI MÁY GIỮA LƯỢT (ghi 23/9 tối)

**L4 đo 23/9 (P3):** `u6/2512 … 50,6 s/u · vram 6,49 GB` ⇒ S ≈ 35 h trên L4 (số trung bình có gồm
update khởi động nên hơi cao). **A100 chưa đo** — tối 23/9 không kết nối được A100.
⇒ **User quyết: chạy S trên L4 trước, lưu điểm lưu như thường; hôm sau vào được A100 thì đo (P3), nếu
A100 đạt luật 1,5× thì chạy TIẾP từ điểm lưu L4 trên A100.**

Vì sao chạy tiếp được, không phải chạy lại:
- điểm lưu có adapter + optimizer + scheduler + số update + RNG (CPU, CUDA, Python); thứ tự dữ liệu là
  hoán vị cố định theo `--seed` ⇒ A100 học tiếp đúng các mẫu L4 chưa học;
- L4 và A100 đều Ampere trở lên ⇒ cùng compute BF16, cùng cấu hình NF4;
- tiền lệ dự án (11/8): L4 vs A100 cùng seed, loss 20 bước trùng ba chữ số, `total_flos` y hệt.
⚠️ Phải khai trong manifest: "Stage S chạy update 1…N trên L4, N+1…2.512 trên A100". Sai khác số học
giữa hai card ở mức làm tròn, không đổi recipe.

**Quy trình đổi máy (làm đúng thứ tự, mất ≤ 5 phút tiến độ):**
1. Chờ ô P5 in `↑ Drive: …/S/ckpt-XXXXX` của điểm lưu **mới nhất** (lưu mỗi 100 update ≈ 84 phút trên L4;
   đồng bộ mỗi 5 phút). Kiểm trên Drive thư mục đó có tệp `DONE`.
2. Ghi lại số update cuối trong log. Rồi mới Runtime → Disconnect and delete runtime.
   (Phần update sau điểm lưu cuối sẽ mất — nên ngắt ngay sau khi vừa có điểm lưu mới.)
3. Đổi runtime sang A100 → P1 → P2 → **P3 (đo, ra thư mục riêng `/content/do_may_S`, không đụng điểm
   lưu thật)** → gửi `s/u`.
4. A100 đạt luật (L4/A100 > 1,5) ⇒ **P4 với `STAGE = "S"`**: ô tự chép điểm lưu mới nhất trên Drive về và
   in `[nối tiếp] từ … — update N/2512`. Đổi `BS/ACCUM` được khi nối tiếp **miễn tích = 16** (mỗi update
   vẫn đúng 16 mẫu đó, cùng thứ tự — trainer tính vị trí nối tiếp bằng update × 16). Rồi P5.
5. A100 KHÔNG đạt luật (≤ 1,5×) ⇒ quay lại L4 và làm bước 4 trên L4.

⚠️ Colab trả trước không có background execution ⇒ để máy và trình duyệt mở, ô P5 chạy tiền cảnh. Mất
máy giữa đêm thì làm lại P1 → P2 → P4 → P5 (tự nối tiếp từ Drive).
⭐ Trong lúc L4 chạy, kiểm GPU có bị bỏ đói không: Terminal Colab →
`nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 5` (Ctrl+C sau ~1 phút). GPU < ~60%
thường xuyên ⇒ nghẽn khâu nạp ảnh CPU, A100 sẽ không nhanh hơn — báo lại để sửa trước khi đổi máy.

### A100 đo 23/9 tối (P3) — [đo]

`u6/2512 … 23,7 s/u · vram 6,49 GB` ⇒ **L4/A100 = 50,6/23,7 = 2,13 > 1,5 ⇒ chạy A100.**
⚠️ `nvidia-smi` lúc P3 chạy: GPU bận **30–50%** phần lớn thời gian, vọt 95–100% từng lúc ⇒ GPU chờ dữ
liệu. Hai số đo trên đều gồm thời gian khởi động worker (6 update quá ít). S1 cũ (LLaMA-Factory + liger)
trên A100: 10,3 s/u.
**Vá (0 đổi phép tính, CE u1–u4 trùng tuyệt đối bản trước):** mỗi worker nạp dữ liệu dùng 1 luồng torch
(`_mot_luong`); log in thêm `(gần X)` = s/u của 20 update gần nhất và `chờ-dữ-liệu Y%` = phần thời gian
vòng lặp đứng chờ lô kế. **Đọc sau ~40 update:** `chờ-dữ-liệu` > ~20% ⇒ tăng `--workers` (A100 Colab có
12 lõi) rồi chạy lại P4 — nối tiếp từ điểm lưu, số worker không đổi kết quả.

### Lượt S thật, A100, lô 4 × 4 (23/9 22:30 VN) — [đo]

`u11 … 23,0 s/u (gần 22,8) chờ-dữ-liệu 0% còn 15,8 h vram 6,49` ⇒ **nạp dữ liệu KHÔNG phải chỗ nghẽn**
(đoán cũ sai). GPU bận 30–50% + chờ dữ liệu 0% + VRAM 6,5/40 GB ⇒ nhiều khả năng GPU đói việc vì lô nhỏ
[suy]. **Đổi sang lô 16 × 1 ở điểm lưu 100** (quy trình dưới), đo lại `gần`.

**Đổi cỡ lô giữa lượt (không mất gì ngoài vài update sau điểm lưu):**
1. Chờ P5 in `↑ Drive: …/S/ckpt-00100`.
2. Terminal Colab: `pkill -f harness/pata_train.py` (P5 sẽ in "tiến trình train đã kết thúc").
3. P4 bản mới (`BS, ACCUM = "16", "1"`) → in `[nối tiếp] … update 100/2512` và `SID … ✓` → P5.
4. Sau ~20 update: đọc `(gần …)`. Tràn bộ nhớ ⇒ `"8", "2"` và làm lại bước 3.
⚠️ Khai vào manifest: "S update 1–100 lô 4 × 4, từ 101 lô 16 × 1 (tương đương toán học)".

### Lô 16 × 1 sau điểm lưu 100 (23/9 23:23 VN) — [đo]

Nối tiếp đúng `update 100/2512`. `u140 … 24,0 s/u (gần 23,9) chờ-dữ-liệu 0% vram 18,7 GB`, CE 0,64 → 0,83.
⇒ **Lô lớn KHÔNG nhanh hơn** (4 × 4: 22,8 s/u) — giả thuyết "GPU đói việc vì lô nhỏ" **bị bác**. Giữ 16 × 1
cho mọi chặng còn lại (tương đương toán học, VRAM dư) để C1 và C0-Loc cùng một cách chia lô.
S dự kiến xong ~**15:10 VN 24/9** (còn ~15,8 h). Chỗ chậm so với S1 cũ (10,3 s/u) chưa rõ — cần đo phân
rã thời gian (tháp thị giác / forward LM / backward) trên Kaggle T4 trước chặng H.

### ⭐ 24/9 — THỦ PHẠM CHẬM: gradient thừa qua tháp thị giác — đã vá, tương đương từng bit — [đo]

Kaggle K9 (T4, lô 2): tháp thị giác chỉ **14%** forward; `block` chậm hơn (0,60×) ⇒ bỏ `block`. Nhưng
**backward 6,09 s gấp đôi forward 3,05 s** và có **4.748 lời gọi backward attention mỗi bước** ⇒ tháp thị
giác nằm trong đồ thị gradient. Nguyên nhân (`transformers/modeling_utils.py:3361`):
`gradient_checkpointing_enable()` gọi `enable_input_require_grads()`, hàm này gắn hook lên embedding đầu
vào của MỌI mô hình con, kể cả tháp thị giác. **Vá** trong `pata_model.enable_gc`: gỡ các hook đó, chỉ giữ
một hook ở embedding của mô hình ngôn ngữ. Kiểm trên mô hình tí hon: bản cũ tháp thị giác có gradient,
bản mới không; CE trùng; gradient LoRA + đầu PATA lệch **0,0 trên 41.345 phần tử**. 13/13 test đạt.

**Áp cho lượt S đang chạy (không đổi kết quả, chỉ nhanh hơn):**
1. Upload `thesis_pata_colab.zip` mới lên `MyDrive/thesis/`.
2. Chờ P5 in `↑ Drive: …/S/ckpt-XXXXX` mới nhất → Terminal: `pkill -f harness/pata_train.py`.
3. **P2** (bung gói mới; ảnh đã có nên bỏ qua; dòng assert mới phải xanh) → ô `LD_LIBRARY_PATH` nếu máy
   này cần → **P4** (`STAGE="S"`, `BS, ACCUM = "16", "1"`) → **P5**.
4. Sau ~20 update đọc `(gần …)` — kỳ vọng thấp hơn rõ 23,9 [suy, chưa đo].
Khai vào manifest: "từ update N, tháp thị giác không còn trong đồ thị gradient (tương đương từng bit)".

## Ô P4 — chạy một chặng, chạy nền

Đặt `STAGE` rồi chạy. Chạy lại **đúng ô này** sau khi mất máy (sau P1 + P2) là tự nối tiếp: ô chép điểm
lưu mới nhất trên Drive về local trước khi khởi động.
⚠️ **Mất máy ≠ restart nhân Python.** Mất máy (VM mới, `/content` trống): P1 → P2 → P4 → P5. Chỉ nhân
Python restart (tiến trình train vẫn sống): chạy P2 (để có biến) → P4 (sẽ báo "ĐANG CHẠY" và dừng — đúng) →
**P5** (bám tiến trình cũ theo PID).

```python
import os, glob, shutil, subprocess
STAGE = "S"          # ⬅ "S" → rồi "H" → rồi "J"  (C1 = J bridge bật)
BS, ACCUM = "16", "1"  # cỡ lô × gộp PHẢI = 16. Đo 23/9: lô 4 × 4 chạy 22,8 s/u, chờ dữ liệu 0%, GPU bận 30–50%
                       # ⇒ GPU đói việc vì lô nhỏ. 16 × 1 tương đương toán học (cùng 16 mẫu/update, cùng thứ
                       # tự, loss chia theo cả lô); tràn bộ nhớ thì lùi "8", "2".

def chay(cmd, log):
    """Định nghĩa LẠI ngay trong ô này (không dựa vào P3): ⛔ start_new_session=True là thứ giữ train
    sống khi bấm Stop một ô bất kỳ (luật Colab ①)."""
    env = dict(os.environ, TQDM_DISABLE="1", HF_HUB_DISABLE_PROGRESS_BARS="1",
               PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True", PYTHONUNBUFFERED="1")
    return subprocess.Popen(cmd, stdout=open(log, "a"), stderr=subprocess.STDOUT, env=env,
                            cwd=REPO, start_new_session=True)
# ⛔ CHẶN CHẠY TRÙNG: nhân Python restart thì tiến trình train (start_new_session) VẪN sống. Chạy lại ô này
#    khi nó còn sống = hai trainer ghi cùng thư mục. Còn sống thì KHÔNG khởi động mới — sang thẳng ô P5.
OUT = f"/content/ck/{STAGE}"        # đặt TRƯỚC phép kiểm: ô P5 cần OUT kể cả khi phép kiểm dừng ô này
dang = subprocess.run(["pgrep", "-f", "harness/pata_train.py"], capture_output=True, text=True).stdout.split()
assert not dang, f"⛔ pata_train.py ĐANG CHẠY (PID {dang}) — đừng chạy P4, sang ô P5 (nó tự bám PID)."
os.makedirs(OUT, exist_ok=True)
# nối tiếp: lấy điểm lưu TRỌN (có DONE) mới nhất trên Drive nếu local chưa có
dck = sorted(glob.glob(f"{CK}/{STAGE}/ckpt-*/DONE"))
if dck and not glob.glob(f"{OUT}/ckpt-*/DONE"):
    src = os.path.dirname(dck[-1])
    shutil.copytree(src, f"{OUT}/{os.path.basename(src)}")
    print("nối tiếp từ Drive:", src)
extra = {"S": [],
         "H": ["--init-adapter", f"{CK}/S/final"],
         "J": ["--init-adapter", f"{CK}/S/final", "--init-heads", f"{CK}/H/final"]}[STAGE]
P = chay(["python", "harness/pata_train.py", "--stage", STAGE, "--data-root", DR,
          "--bs", BS, "--accum", ACCUM, "--save-steps", "100", "--milestones", "800",
          "--log-steps", "20", "--workers", "8", "--out", OUT] + extra, f"/content/pata_{STAGE}.log")
print("PID", P.pid, "· log /content/pata_%s.log" % STAGE)
# kiểm bằng máy, không tin mã: SID phải bằng PID ⇒ tiến trình đứng đầu phiên riêng
sid = subprocess.run(["ps", "-o", "sid=", "-p", str(P.pid)], capture_output=True, text=True).stdout.strip()
print("SID", sid, "✓ phiên riêng — Stop ô khác không giết train" if sid == str(P.pid)
      else "⛔ KHÔNG phải phiên riêng — ĐỪNG bấm Stop ô nào, báo lại")
```

⛔ Chặng H và J nạp `final/` của chặng trước **từ Drive** (`{CK}/S/final`, `{CK}/H/final`) — ô P5 đẩy
`final/` lên Drive khi chặng xong. Chưa thấy `final/` trên Drive thì **đừng** chạy chặng sau.

## Ô P5 — theo dõi + đồng bộ Drive (CHẠY TIỀN CẢNH SUỐT LƯỢT, không bấm Stop)

```python
import os, glob, time, datetime, shutil, subprocess
L = []
def dong_bo():
    """Đẩy điểm lưu TRỌN chưa có lên Drive: chép sang tên tạm rồi đổi tên (Drive chỉ thấy tệp đã đóng)."""
    os.makedirs(f"{CK}/{STAGE}", exist_ok=True)
    for c in sorted(glob.glob(f"{OUT}/ckpt-*")) + [f"{OUT}/final"]:
        ten = os.path.basename(c)
        if not os.path.isdir(c) or c.endswith(".tmp"):
            continue
        if ten != "final" and not os.path.exists(f"{c}/DONE"):
            continue
        dst = f"{CK}/{STAGE}/{ten}"
        if os.path.exists(dst):
            continue
        shutil.copytree(c, dst + ".tmp"); os.rename(dst + ".tmp", dst)
        print("   ↑ Drive:", dst, flush=True)
    for f in (f"{OUT}/train_log.jsonl", f"{OUT}/final_sha256.json", f"/content/pata_{STAGE}.log"):
        if os.path.exists(f):
            shutil.copy(f, f"{CK}/{STAGE}/")
    # chỉ giữ trên Drive: 2 điểm lưu mới nhất + mốc 800 + final (mỗi điểm lưu ~180 MB; giữ hết thì
    # ba chặng ~13 GB, dễ tràn hạn mức Drive giữa đêm)
    cu = sorted(d for d in glob.glob(f"{CK}/{STAGE}/ckpt-*") if not d.endswith(".tmp")
                and os.path.exists(f"{d}/DONE") and not d.endswith("ckpt-00800"))
    for d in cu[:-2]:
        shutil.rmtree(d, ignore_errors=True)
        print("   ✗ Drive bỏ", os.path.basename(d), flush=True)

def con_song():
    """Bám theo PID thay vì biến P — chạy lại được sau khi nhân Python restart."""
    return bool(subprocess.run(["pgrep", "-f", "harness/pata_train.py"], capture_output=True,
                               text=True).stdout.split())
t_sync = 0
while con_song():
    time.sleep(60)
    L = open(f"/content/pata_{STAGE}.log").read().splitlines()
    dong = [l for l in L if l.startswith("[") and "/" in l and " u" in l]
    gio = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).strftime("%H:%M")
    print(f"[{gio} VN] {(dong or L or [''])[-1][:230]}", flush=True)
    if any(k in l for l in L[-30:] for k in ("=nan", "NaN", "OutOfMemory", "Traceback")):
        print("⛔ LỖI trong log — xem /content/pata_%s.log" % STAGE); break
    if time.time() - t_sync > 300:
        dong_bo(); t_sync = time.time()
dong_bo()
print("== tiến trình train đã kết thúc ==")
print("\n".join(L[-8:]))
```

**Đọc trong lúc chạy:**
- S: `ce=` giảm rồi ổn định; `gn lora` vài đơn vị.
- H: `kl=` giảm, `mass=` tăng; `gn lora = 0`; `tvec` có thể lớn (đã tách nhóm, không kéo nhóm khác).
- C1: `gate=` nhích lên từ 0,119; `resid=` tăng dần từ 0; `ce=` hồi về quanh mức S (smoke: TARGET làm
  CE vọt 1,12 → 2,36 rồi C1 hồi về 1,27 sau 20 update).
- ⚠️ Dòng log in lại y hệt nhiều phút là bình thường (log mỗi 20 update, ~3–5 phút/lần).

## Ô P6 — sau chặng S: CE_val trên val400 (§6 Stage S) ✅ ĐÃ CHẠY 24/9: CE_val = 0,7295

Đã chạy trong Terminal, ghi ra `{CK}/eval/diag_final_val400.json`. **Chép sang tên chuẩn** (một lần, ô bất
kỳ lúc không có ô nào đang chạy, hoặc Terminal):
```
mkdir -p /content/drive/MyDrive/thesis/pata_ck/cong_c1
cp /content/drive/MyDrive/thesis/pata_ck/eval/diag_final_val400.json \
   /content/drive/MyDrive/thesis/pata_ck/cong_c1/diag_S_val400.json
```
⚠️ Mọi lệnh `pata_eval.py` từ đây **phải có `--tag`**: S, H, J đều tên thư mục `final` nên không có tag
thì tệp ra đè nhau.

## Ô P7 — CỔNG H trên val400 (sau khi P5 in `↑ Drive: …/H/final` và kết thúc)

Chạy trong **ô notebook** (lúc này không còn train chạy nền, P5 đã kết thúc; `chay` của P4 mang theo
`LD_LIBRARY_PATH`):
```python
e = chay(["python", "harness/pata_eval.py", "--ckpt", f"{CK}/H/final", "--mode", "diag", "--split",
          "val400", "--no-ce", "--tag", "H", "--data-root", DR, "--out", f"{CK}/cong_c1"], "/content/eval_H.log")
e.wait(); print(open("/content/eval_H.log").read()[-1500:])
```

**Luật (khoá trong `185` §6):** đi tiếp C1 **chỉ khi** in `⇒ CỔNG H: ĐẠT`, tức cận dưới KTC một phía
90% của cả ba hiệu > 0: mass − center prior · mass − train prior · mass(prompt đúng) − mass(prompt xáo).
⛔ **Không đạt ⇒ DỪNG**, không chạy C1, không mở test. Kết luận "futility under budget". Gửi mình
`cong_c1/diag_H_val400.json`.

## Ô P8 — mốc 800 của C1 (Terminal, song song với train)

Khi P5 in `↑ Drive: …/J/ckpt-00800`, dán vào **Terminal Colab** (⛔ không bấm Stop P5):
```
export LD_LIBRARY_PATH=/usr/local/lib/python3.13/dist-packages/nvidia/cu13/lib:$LD_LIBRARY_PATH
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True TQDM_DISABLE=1
cd /content/ws/thesis
DR=harness/dg1_cache/train_ac; CK=/content/drive/MyDrive/thesis/pata_ck
python harness/pata_eval.py --ckpt /content/ck/J/ckpt-00800 --mode diag --split val400 --tag J800 \
  --data-root $DR --out $CK/eval_m800 > /content/m800_diag.log 2>&1
python harness/pata_eval.py --ckpt /content/ck/J/ckpt-00800 --mode gen --split probe40 --variants on,off \
  --tag J800 --bs 8 --data-root $DR --out $CK/eval_m800 > /content/m800_gen.log 2>&1
tail -22 /content/m800_diag.log; tail -5 /content/m800_gen.log
```

**Luật mốc 800 (`185` §7b, §8):** chỉ được dừng vì lỗi kỹ thuật:
1. `CE_val`, `KL_val` không phân kỳ;
2. **tắt bridge làm ≥ 30% câu probe đổi** (dòng `câu ĐỔI khi tắt bridge`). Gần như không đổi ⇒ decoder
   bỏ qua bridge ⇒ **DỪNG** C1;
3. xáo prompt thì mass giảm (`dung_vs_xao` dương);
4. format hợp lệ ≥ 95% (dòng `on … format hợp lệ`).
Đạt ⇒ để C1 chạy hết epoch. ⛔ Không đổi λ, block, LR, gate sau khi xem mốc 800. ⛔ Không suy `exec` từ
probe 40.

## Ô P9 — hết epoch C1: chẩn đoán J + sinh câu val600 (MỘT lần, ~1–1,5 h A100)

⚠️ **Trước P9: upload lại `thesis_pata_colab.zip` bản 24/9 tối (commit sau `561d620`) rồi chạy lại P2.**
Bản này ghi preds theo kiểu mở–ghi–đóng từng lô, nên mất máy giữa P9 không mất tệp trên Drive (bản
trước mở tệp một lần cho cả biến thể ⇒ mất máy là mất trọn tệp, đã trả giá 24/8). Kiểm:
`grep -c 'with open(fp, "a"' harness/pata_eval.py` phải ra `1`.

**Mất máy giữa P9:** P1 → P2 → chạy lại đúng ô P9. Mỗi biến thể in `đã có N · còn M` rồi chỉ sinh phần
thiếu; `diag_J` chạy lại từ đầu (~10 phút).

Sau khi P5 in `↑ Drive: …/J/final` và kết thúc. Ô notebook:
```python
for cmd, log in (
    (["--ckpt", f"{CK}/J/final", "--mode", "diag", "--split", "val400", "--tag", "J"], "diag_J"),
    (["--ckpt", f"{CK}/J/final", "--mode", "gen", "--split", "val600", "--variants", "on,off,swapD,swapR",
      "--tag", "C1", "--bs", "16"], "gen_C1"),
    (["--ckpt", f"{CK}/S/final", "--mode", "gen", "--split", "val600", "--variants", "on",
      "--tag", "S", "--bs", "16"], "gen_S")):
    e = chay(["python", "harness/pata_eval.py", "--data-root", DR, "--out", f"{CK}/cong_c1"] + cmd,
             f"/content/{log}.log")
    e.wait(); print(log, open(f"/content/{log}.log").read()[-700:], flush=True)
```
Ra trong `{CK}/cong_c1/`: `diag_J_val400.json` + 5 tệp preds (`preds_C1_val600_{on,off,swapD,swapR}.jsonl`,
`preds_S_val600_on.jsonl`). Sinh câu ghi dần + nối tiếp được: mất máy thì chạy lại ô này.
⛔ val600 là tập cổng cuối, **chỉ chạy một lần**; không xem số `exec` giữa chừng.

## Ô P10 — chấm `exec` val600 (Kaggle T4 × 2, 0 đồng, ~2–2,5 h)

Runbook riêng: **`harness/kaggle_pata_cham_val600.md`** (Q0–Q4). Sau đó đọc cổng trên WSL:
```
~/.venvs/thesis/bin/python harness/pata_cong_c1.py --dir runs/pata/cong_c1
```
Năm điều kiện + ngưỡng đã **khoá trong `pata_cong_c1.py` ngày 24/9, trước khi C1 train**.

---

## Sau lượt — gửi mình

`{CK}/S|H|J/train_log.jsonl` · `{CK}/eval/*.json` · ba tệp preds val600 · dòng phiên bản ở P1 · `s/u`
đo ở P3. Mình seal manifest §11 (cần SHA của `S/final`, `H/final` trong `final_sha256.json`).
