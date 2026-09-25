# Runbook PATA C2 · P0 → P1 (0 đồng: WSL + Kaggle T4, ~1 h máy)

Nguồn: `harness/tai_lieu_2026-09-25/204_…` §4.1–4.2. Mục đích: phân biệt **thiếu routing** hay **thiếu
pixel** trước khi viết bất kỳ kiến trúc thay thế nào (RCA hay dual-view). ⛔ Không train, không A100, không
val600, không mở test. Dừng ngay khi một cổng không đạt.

| bước | máy | việc | ai làm | dừng nếu |
|---|---|---|---|---|
| P0.1–4 | WSL | vá labeler, dựng cặp G/D thật | ✅ đã xong 25/9 | < 150 cặp |
| **P0.5** | trình duyệt | **audit mù 100 cặp** | **bạn** (~40–60 phút) | trượt 2 lần |
| P1.0 | WSL | khoá luật quyết, dựng crop, đóng gói | bạn chạy 3 lệnh | audit chưa đạt |
| P1.1 | Drive → Kaggle | đưa adapter **S/final** lên Kaggle | bạn | — |
| P1.2 | Kaggle T4 | chấm likelihood 7 nhánh × 232 cặp | bạn bấm ô | assert hỏng |
| P1.3 | WSL | bootstrap + đọc bảng chọn | bạn chạy 1 lệnh | — |

---

## Đã xong (0 GPU, 25/9)

· `descriptor_label_build.py` ghi thêm `box_neg · name_neg · role_neg · cls_neg · point_neg_abs ·
  point_neg_norm · area_share_neg`, ra tệp **riêng** `descriptors_trueD.jsonl` (cờ `--out`), không đè
  `descriptors.jsonl`. Kiểm trên đủ 41.099 dòng: **mọi trường cũ lệch 0**; `box_neg` 37.663 = `desc_neg`
  37.663 (91,6%). ⚠️ Handoff ghi "khoảng 55,6%": đó là tỉ lệ cặp qua `hop_le()` (22.854/41.099), không
  phải tỉ lệ `desc_neg`. Phép kiểm đúng là **bằng nhau**, và đã đạt.
· `pata_true_d.py` → `pata/val400_trueD.jsonl`: **232 cặp eligible / 400 bước** (101 episode), vượt ngưỡng
  150. Loại: 91 khoảng cách ngoài 80–350 px · 55 trùng tên · 16 không có D · 3 câu vàng nhắc tên D · 2 không
  box · 1 D quá lớn. 0 cặp cha/con, 0 cặp IoU ≥ 0,30 (luật `overlapped()` của labeler đã chặn trước).
· `pata_audit_d.py build` → trang audit 100 mẫu (G ở A: 51, ở B: 49).
· `pata_p1.py` chạy thử đủ đường `prep → run → doc` bằng mô hình tí hon trên CPU: mọi assert đạt, nối tiếp
  đúng, `doc` ra quyết định. (Crop và `p1_decision.json` hiện có là bản THỬ, ghi `audit_dat=false`;
  `make_bundle` sẽ từ chối đóng gói cho tới khi audit đạt và `prep` chạy lại.)

---

✅ **25/9 — P0.5 ĐẠT (lần 1, người gán Uyên):** chọn đúng G **93/100** [86,3; 96,6] · cả hai đúng **1/100** ·
D không phải widget **5/100** [2,2; 11,2]. Mẫu không chọn đúng G: 4, 8, 22, 36, 39, 57, 85 (4 "không khung
nào", 2 chọn D, 1 "cả hai"). ✅ **P1.0 xong:** `p1_decision.json` khoá sha256 **`c9b5990ad4d85689…`**,
gói `_bundles/thesis_pata_p1.zip` 130 MB (232 cặp). Việc còn: P1.1 → P1.3.

## P0.5 — audit mù (bạn làm)

1. Windows Explorer mở
   `D:\Master\Thesis\harness\dg1_cache\train_ac\pata\audit_trueD_lan1\audit.html` bằng Chrome/Edge.
2. Ô *Người gán* điền tên. Với từng mẫu, đọc **câu hướng dẫn in đậm**, trả lời:
   * **(1) Câu nhắm tới:** khung **A** (cam) hay **B** (xanh). Nếu câu mô tả khớp CẢ HAI như nhau → *Cả
     hai đều đúng*. Không khớp khung nào → *Không khung nào*. Không quyết được → *Không rõ*.
   * **(2) Không phải widget:** tick khung nào **không** phải một phần tử bấm được (ví dụ khung bao một
     vùng trống, một đoạn chữ trang trí, một ô lệch khỏi nút). Cả hai đều là nút thật thì để trống.
   * Chỉ dựa vào câu và ảnh. Đừng đoán theo màu hay theo vị trí A/B — đáp án được đảo ngẫu nhiên.
3. Nhãn tự lưu trong trình duyệt (đóng mở lại vẫn còn). Gán đủ 100 → bấm **Tải nhãn (.json)** → chép tệp
   `audit_trueD_lan1_<tên>.json` vào đúng thư mục `audit_trueD_lan1\` ở trên.
4. Đọc kết quả:
   ```
   cd /mnt/d/Master/Thesis && ~/.venvs/thesis/bin/python harness/pata_audit_d.py doc
   ```
   Cổng (khoá trước): **chọn đúng G ≥ 75% · "cả hai đều đúng" ≤ 15% · D không phải widget ≤ 10%**.
   * ĐẠT → sang P1.0.
   * KHÔNG ĐẠT lần 1 → gửi mình output (có danh sách mã mẫu sai); mình sửa `pata_true_d.py`, dựng lại,
     rồi bạn audit **100 mẫu mới** bằng `pata_audit_d.py build --lan 2`.
   * KHÔNG ĐẠT lần 2 → **dừng C2**.

## P1.0 — khoá luật, dựng crop, đóng gói (WSL, ~2 phút)

```
cd /mnt/d/Master/Thesis
~/.venvs/thesis/bin/python harness/pata_p1.py prep          # ghi đè crop thử + p1_decision.json (audit_dat=true)
~/.venvs/thesis/bin/python harness/make_bundle.py pata_p1   # → _bundles/thesis_pata_p1.zip (~100 MB)
```
Chép lại dòng `KHOÁ luật quyết: … sha256 xxxxxxxx…`. Nên **commit** `p1_decision.json` + mã trước khi
chạy GPU — đó là bằng chứng luật quyết có trước số.

## P1.1 — đưa S/final lên Kaggle (làm tay)

1. Google Drive → `MyDrive/thesis/pata_ck/S/` → tải thư mục **`final`** (Drive nén thành zip) và tệp
   **`final_sha256.json`** nằm cạnh nó.
2. Bỏ `final_sha256.json` vào trong thư mục `final` vừa giải nén (để ô Q2 kiểm hash), nén lại thành
   `pata_S_final.zip`.
3. Kaggle → *Datasets → New Dataset* → kéo `pata_S_final.zip` → tên **`pata-s-final`** → Create.
4. Kaggle → *Datasets → New Dataset* → kéo `D:\Master\Thesis\_bundles\thesis_pata_p1.zip` → tên
   **`thesis-pata-p1`** → Create.
5. *Code → New Notebook* · Accelerator **GPU T4 x2** · Internet **On** · *Add Input* hai dataset trên.
   ⛔ Chạy **tương tác** (bấm từng ô), không *Save Version*.

## Ô Q1 — cài gói

```python
import subprocess, sys, torch
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "bitsandbytes", "peft"], check=True)
import transformers, peft, bitsandbytes
print("torch", torch.__version__, "· transformers", transformers.__version__, "· peft", peft.__version__)
assert torch.cuda.is_available(), "⛔ không có GPU — bật Accelerator GPU T4 x2"
```

## Ô Q2 — mở gói, kiểm hash

```python
import os, glob, json, hashlib, zipfile, shutil
W = "/kaggle/working"
h256 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
src = glob.glob("/kaggle/input/**/thesis/harness/pata_p1.py", recursive=True)
if src:
    shutil.copytree(os.path.dirname(os.path.dirname(os.path.dirname(src[0]))), f"{W}/p1", dirs_exist_ok=True)
else:
    zipfile.ZipFile(glob.glob("/kaggle/input/**/thesis_pata_p1.zip", recursive=True)[0]).extractall(f"{W}/p1")
REPO = f"{W}/p1/thesis"; DR = f"{REPO}/harness/dg1_cache/train_ac"; os.chdir(REPO)
dec = json.load(open(f"{DR}/pata/p1_decision.json"))
print("p1_decision sha256:", h256(f"{DR}/pata/p1_decision.json")[:16], "← phải khớp dòng KHOÁ ở P1.0")
print("audit_dat:", dec["audit_dat"], "· cặp:", dec["n_cap"],
      "· crop:", len(glob.glob(f"{DR}/pata/p1_crops/*.png")), "← cần", 6 * dec["n_cap"])
assert dec["audit_dat"] and len(glob.glob(f"{DR}/pata/p1_crops/*.png")) == 6 * dec["n_cap"]
cfg = glob.glob("/kaggle/input/**/adapter_config.json", recursive=True)
cfg = [c for c in cfg if "thesis/" not in c]
assert len(cfg) == 1, f"⛔ tìm thấy {len(cfg)} adapter — cần đúng một (S/final): {cfg}"
S = os.path.dirname(cfg[0])
print("S/final:", S, sorted(os.listdir(S)))
assert not os.path.exists(f"{S}/pata_heads.pt"), "⛔ đây là điểm lưu H/J/C1, không phải S"
if os.path.exists(f"{S}/final_sha256.json"):
    ref = json.load(open(f"{S}/final_sha256.json"))
    for k, v in ref.items():
        if os.path.exists(f"{S}/{k}"):
            print(f"  {k:32}", "KHỚP" if h256(f"{S}/{k}") == v else "⛔ LỆCH"); assert h256(f"{S}/{k}") == v
else:
    print("⚠️ không có final_sha256.json — không kiểm được adapter là đúng S/final")
```

## Ô Q3 — chấm (nền, ghi log ra tệp, nhịp sống mỗi 60 s)

Ước lượng [suy, chưa đo]: ~5–10 s/cặp ⇒ 232 cặp ≈ 20–40 phút. Trước khi chấm, script tự chạy assert trên
6 cặp đầu: đổi thứ tự nhánh trong lô (≤ 1e-3 nats/token) · G=D nhân tạo cho gap 0 (≤ 1e-5) · số token khớp
trong họ L và họ H · không module nào ở chế độ train.

```python
import subprocess, time
def chay(cmd, log, tmax=4 * 3600):
    env = dict(os.environ, TQDM_DISABLE="1", HF_HUB_DISABLE_PROGRESS_BARS="1",
               PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True", PYTHONUNBUFFERED="1",
               CUDA_VISIBLE_DEVICES="0")
    with open(log, "a") as f:
        p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, env=env, start_new_session=True)
    t0 = time.time()
    while p.poll() is None and time.time() - t0 < tmax:
        time.sleep(60)
        tail = open(log).read().splitlines()[-1:] or [""]
        print(f"[{(time.time()-t0)/60:4.0f} phút] {tail[0][:160]}", flush=True)
    print(f"== mã thoát {p.returncode} ==")
    print("\n".join(l for l in open(log).read().splitlines()
                    if any(k in l for k in ("[S]", "[assert]", "kiểm", "⛔", "Error", "XONG", "[chấm]"))))
    return p.returncode

OUT = f"{W}/p1_out"
chay(["python", "harness/pata_p1.py", "run", "--adapter", S, "--data-root", DR, "--out", OUT], f"{W}/p1.log")
```

**Đọc:** phải thấy `[assert] 6 cặp: … — ĐẠT`, rồi `XONG`. Dòng `⛔` bất kỳ ⇒ **dừng**, gửi mình toàn bộ
`p1.log`. Mất phiên giữa chừng: chạy lại Q2 + Q3, script nối tiếp từ `p1_scores.jsonl` (chỉ còn nếu
`/kaggle/working` chưa bị xoá — lượt ngắn nên cứ chạy lại từ đầu cũng được).

## Ô Q3b — CHỈ khi log có `đã có N` với N > 0 ngay lần chạy đầu (hai tiến trình song song)

⛔ Đã xảy ra 25/9: ô Q3 bị bấm hai lần ⇒ hai tiến trình (tách phiên, Stop ô không giết) cùng chấm, chia GPU
(31 s/cặp) và ghi trùng cặp. Bấm **Stop** ô Q3 (tiến trình không chết), rồi dừng tiến trình **mới hơn**:
```python
import os, signal, subprocess
ps = [l.split(None, 2) for l in subprocess.run("ps -eo pid,etimes,cmd", shell=True, capture_output=True,
      text=True).stdout.splitlines() if "pata_p1.py run" in l and "grep" not in l]
ps = sorted((int(e), int(p)) for p, e, _ in ps)          # (số giây đã chạy, pid)
print("đang chạy:", ps)
if len(ps) >= 2:
    os.kill(ps[0][1], signal.SIGTERM); print("đã dừng tiến trình mới hơn:", ps[0][1])
```
Rồi theo dõi bằng Q3c (⛔ **không** chạy lại Q3). Dòng trùng trong `p1_scores.jsonl` để nguyên: `doc` tự gộp
và kiểm hai lần chấm cùng cặp ra cùng số.

## Ô Q3c — theo dõi tiến trình đang chạy (không khởi động gì mới)

```python
import time, json, subprocess
# ⛔ pgrep qua shell=True tự khớp chính dòng lệnh `sh -c "…pata_p1.py run…"` ⇒ vòng lặp không bao giờ dừng
#    (đã gặp 25/9). Gọi pgrep bằng danh sách đối số và mẫu "[p]ata" để không khớp chính nó.
while subprocess.run(["pgrep", "-f", "[p]ata_p1.py run"], capture_output=True).stdout.strip():
    ks = {(json.loads(l)["episode_id"], json.loads(l)["step_id"]) for l in open(f"{OUT}/p1_scores.jsonl")}
    print(time.strftime("%H:%M"), f"{len(ks)}/232 cặp khác nhau ·",
          open(f"{W}/p1.log").read().splitlines()[-1][:110], flush=True)
    time.sleep(120)
print("== tiến trình đã kết thúc ==", *open(f"{W}/p1.log").read().splitlines()[-2:], sep="\n")
```

## Ô Q4 — gom kết quả

```python
shutil.copy(f"{W}/p1.log", OUT)
shutil.make_archive(f"{W}/p1_out", "zip", OUT)
print(sorted(os.listdir(OUT)))     # cần p1_scores.jsonl · p1_run_meta.json · p1.log
```
Tải `p1_out.zip` ở cột *Output*.

## P1.3 — đọc (WSL, vài giây)

Bung `p1_out.zip` vào **`runs/pata/p1/`**, rồi:
```
cd /mnt/d/Master/Thesis
~/.venvs/thesis/bin/python harness/pata_p1.py doc --scores runs/pata/p1/p1_scores.jsonl
```
Script kiểm `p1_decision.json` trên máy **trùng** bản lượt chạy đã dùng, rồi in 7 hiệu số (mean · lower90)
và **một hàng** của bảng chọn khoá trước:

| kết quả | kết luận | việc kế |
|---|---|---|
| ΔL đạt, Δres không | thiếu routing | RCA `r=128`, 2 tầng |
| ΔL đạt và Δres đạt | routing + pixel | dual-view trước |
| ΔL không, ΔH + Δres đạt | thiếu pixel | dual-view predicted crop |
| G−D đạt, G−R không | artefact D/R | sửa control, chưa chọn |
| ΔL không và ΔH không | vùng không đủ | **dừng C2** |
| không khớp hàng nào | — | dừng, báo lại |

Gửi mình output của `doc`. ⛔ Không đổi ngưỡng sau khi thấy số. Bước kế (P1b predicted region, rồi P2)
chỉ viết mã sau khi có hàng này.
