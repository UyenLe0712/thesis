# Chạy trên Colab Pro — runbook dán-là-chạy

> Thay cho `run_on_rented.sh` (bản đó cho máy thuê có SSH). Cùng trình tự, cùng luật, chỉ
> khác cách gõ lệnh.
>
> **Máy đo 9/8/2026:** A100 **80 GB** · đĩa 235,7 GB (trống ~148) · local-scratch
> **368 GB** chưa dùng · RAM 167 GB · đốt **6,77 đơn vị/giờ**.
>
> **⚠️ Máy đo 10/8/2026 (phiên chạy thật):** A100-SXM4-**40 GB** · 12 lõi CPU · bf16 thật ·
> **không có local-scratch** · `/content` trống **65,9 / 112,6 GB**. Hai phiên ra hai hạng card
> khác nhau ⇒ **cỡ lô phải giữ `4×4`** ở mọi lượt, và **tốc độ đốt 6,77 là số của card 80 GB,
> chưa đúng cho card này — đo lại ở mốc dừng 4.**
>
> **⚠️ "67 GB ảnh tập dạy" là SỐ SAI**, chép nhầm từ kích thước parquet. Đo thật trên lát 2
> shard đã dựng: **500 KB/ảnh × 64.500 ≈ 31 GB**. Mã xoá parquet sau mỗi shard nên **đỉnh đĩa
> ≈ 32 GB**. Mọi chỗ ghi 67 GB bên dưới (và ở `report/109`, `CLAUDE.md`) đọc là ~31 GB.

---

## Ba nguyên tắc của runbook này

**1. Việc dài chạy nền, không chạy trong ô.** Mọi khâu trên 10 phút đều khởi động bằng
`nohup … > log &` rồi theo dõi bằng một ô nhẹ. Lý do: ô chạy 3 tiếng sẽ đổ hàng vạn dòng
vào trình duyệt cho tới lúc treo tab, mà tab treo giữa lúc OCR là mất cả khâu OCR.

**2. Sau mỗi khâu có một ô KIỂM in ra con số so được với con số đã biết.** Không có ô đó
thì "chạy xong" chỉ nghĩa là "không báo lỗi", mà 35 lỗi bắt được tới nay hầu hết đều
không báo lỗi.

**3. 🛑 Ở mỗi mốc DỪNG, dán output cho mình trước khi chạy tiếp.** Mốc dừng đặt ngay
trước những khâu đắt. Sai ở khâu rẻ mà chạy tiếp sang khâu đắt là cách tiêu tiền nhanh
nhất.

Có **6 mốc dừng**. Mỗi mốc ghi rõ dán cái gì.

---

## ✅ BỐN CÂU BẮT BUỘC trước mỗi khâu tốn tiền — trả lời bằng SỐ ĐO, không bằng trí nhớ

Thêm 10/8/2026 sau khi mất 42 đơn vị. Ba trong bốn câu này, nếu hỏi buổi sáng hôm đó, đã
chặn được khoản mất.

**1. Khâu này chạy bao lâu — đo hay đoán?** Đo trên **chính máy đang chạy**, và đo **gộp
sau 10 phút song song**, đừng nhân từ tốc độ một luồng. *(Trượt: "2,8 giờ" hoá ra 8,1 giờ —
số tính cho 6.969 ảnh tập kiểm bị gán cho 64.567 ảnh tập dạy, rồi lại nhân 12 "lõi" mà thật
ra chỉ 6 lõi vật lý.)*

**2. Khâu này có dùng GPU không?** Kiểm bằng `GPU RAM` trong panel Tài nguyên lúc nó đang
chạy. Bằng 0 ⇒ **chuyển sang runtime CPU, 0 đơn vị**. Đừng nhận lý do "cho cùng môi trường".
*(Trượt: cả phiên 0 chạy trên A100 mà GPU RAM đứng yên ở 0,0/40 GB suốt 8 giờ — 43 đơn vị
trả cho một chiếc card ngồi không.)*

**3. Máy chết ngay lúc này thì mất bao nhiêu công?** Trên **9 GB dòng dưới đây**: chỉ những
gì đã nằm trên Drive mới tính là còn. Quá **15 phút** ⇒ **phải có cơ chế cất định kỳ lên
Drive TRƯỚC khi bấm chạy**, không phải cất ở cuối. *(Trượt: 8 giờ công treo trên `/content`;
runbook có sẵn câu "Colab xoá sạch `/content` khi phiên chết" mà không ai nối nó với phiên 0.)*

**4. Con số kỳ vọng in trong runbook lấy từ đâu?** Nếu là số đo trên máy khác/lần khác/tập
dữ liệu khác thì **đo lại**. *(Trượt bốn lần: 80 GB → 40 GB · 6,77 đơn vị/giờ → 5,3 · 67 GB
ảnh → 31 GB · 0,08 ảnh/giây → 0,451.)*

**Luật rút ra: soi mã đúng chưa là chưa đủ — phải soi cả giả định nằm dưới kế hoạch.** Bốn
lỗi mã bắt được sáng 10/8 (số script, cỡ ảnh, giờ OCR, merge nhân đôi) đều không cứu nổi,
vì thứ hỏng không nằm trong ô mã nào cả.

---

## 0. Trước khi bật máy

| | |
|---|---|
| Mua đơn vị | ước **600-900** (~$58-87). Mua dư — hết units giữa lượt train là mất phiên |
| Tài khoản | **bất kỳ tài khoản Google nào tiện nhất.** `drive.mount` chỉ gắn Drive của chính tài khoản chạy Colab, nên Colab và Drive phải cùng một tài khoản |
| Drive | tạo `MyDrive/thesis/` — chỗ duy nhất sống sót qua các phiên. **15 GB miễn phí là đủ** |
| Tải lên Drive | `thesis_rented.zip` (3,3 MB) — dựng bằng `python harness/make_bundle.py rented` |
| Runtime | A100. **Kiểm lại mỗi phiên**, Colab hay tụt về L4 |

**Vì sao 15 GB đủ.** Thứ phải sống qua các phiên chỉ ~3 GB: `derived.tar.gz` (~400 MB) ·
điểm lưu huấn luyện (~360 MB/lượt, `save_total_limit: 2`) · `preds_*.jsonl` (~15 MB) · log
và `cfg.yaml`. **67 GB ảnh tập dạy không lưu** — tải lại từ HuggingFace 20-40 phút ≈ 3 đơn
vị ≈ $0,3 mỗi phiên, rẻ hơn mọi cách lưu. Nếu Drive của bạn rộng thì cứ cất thêm
`train_images.tar` cho nhanh (ô 0.12), nhưng đó là tiện nghi chứ không bắt buộc.

---

# PHIÊN 0 — dựng dữ liệu (một lần, **runtime CPU, 0 đơn vị**)

> ## ⛔ VIẾT LẠI 10/8 SAU KHI MẤT MÁY ẢO — đọc trước khi chạy bất cứ ô nào
>
> **Chuyện đã xảy ra:** chạy phiên 0 trên A100 theo bản cũ, tới 90% khâu OCR (~7,9 giờ,
> **42 đơn vị**) thì Colab thu hồi máy ảo. `/content` bị xoá sạch: mất 31 GB ảnh và 58.000
> ảnh đã OCR. Thanh session vẫn xanh nên nhìn như không có chuyện gì — thực ra đã là một
> máy ảo mới, rỗng. **Không cứu lại được gì**, vì bản cũ chỉ cất lên Drive ở tận ô 0.12.
>
> **Hai lỗi thiết kế, đều đã sửa:**
>
> **1. Chín tiếng làm việc mà chỉ có một điểm cất, đặt ở cuối.** Runbook này chuyển thể từ
> `run_on_rented.sh` — máy thuê có SSH, trả tiền theo ngày, nằm đó cả tuần. Trên máy đó ghi
> vào đĩa cục bộ là an toàn. Chuyển sang Colab thì *lệnh* được đổi nhưng **giả định "đĩa cục
> bộ còn mãi" không được xét lại**. Script OCR vốn đã `flush()` sau mỗi ảnh, rất kỷ luật —
> chỉ là flush vào một cái đĩa sắp bốc hơi. ⇒ **Nay `ocr.part*.jsonl` đồng bộ lên Drive mỗi
> 5 phút** (chỉ ~120 MB). Mất máy ảo lần nữa chỉ mất ≤5 phút.
>
> **2. Bật A100 cho một phiên không đụng tới GPU.** Tải ảnh · OCR · dựng nhãn · dựng bốn
> nhánh · nén — **không khâu nào dùng card**. Lý do cũ ghi trong runbook là "cho cùng môi
> trường với các phiên sau"; cái giá của câu đó là **42 đơn vị**. ⇒ **Phiên 0 chạy trên
> runtime CPU, Colab không tính đơn vị.** Giữ A100 cho đúng thứ cần nó: train.
>
> **Đánh đổi — và bản sửa 11/8:** runtime CPU của Colab chỉ có **2 lõi**, đo ra **~45 giờ**
> OCR chia 4-5 phiên, chứ không phải 20-24 giờ như ước ban đầu. Quá đắt về thời gian khi hạn
> nộp còn 2 tháng. ⇒ **quay lại runtime có nhiều lõi, nhưng lần này CÓ đồng bộ Drive** — đó
> mới là thứ đã thiếu hôm mất máy, chứ không phải bản thân việc dùng GPU.
>
> Chọn runtime **bằng số đo, không bằng trí nhớ**: lõi lấy từ `os.cpu_count()`, giá lấy từ
> `Usage rate` ở bảng Xem tài nguyên. A100 đo được 10/8: **12 lõi (6 vật lý) · 5,3 đơn
> vị/giờ · 8,1 giờ ≈ 43 đơn vị ≈ $4,3**. Đo L4/T4 trước khi chốt, có thể rẻ hơn.
>
> **Đổi runtime giữa chừng không mất công OCR:** mảnh đã cất trên Drive được C.3 khôi phục
> lại. Đổi số tiến trình (`--nshard` 2 → 12) làm vài trăm ảnh bị đọc lại, nhưng `--merge`
> khử trùng theo tên ảnh nên kết quả vẫn đúng. Thứ phải làm lại là 31 GB ảnh, ~35 phút.
>
> ⚠️ **Chỉ được rời runtime CPU sau khi ô C.5 xác nhận mảnh đã nằm trên Drive.**

### Ô C.0 — đổi runtime

`Runtime → Change runtime type` → chọn **CPU** (không GPU) → Save. Kiểm lại `Xem tài
nguyên` phải KHÔNG hiện GPU RAM.

### Ô C.1 — gắn Drive, bung mã, nhận diện máy

```python
from google.colab import drive, userdata
drive.mount('/content/drive')
import os, zipfile, shutil
D, WS = "/content/drive/MyDrive/thesis", "/content/ws"
REPO = f"{WS}/thesis"
os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_rented.zip").extractall(WS)
os.chdir(REPO)
os.makedirs(f"{D}/ocr_parts", exist_ok=True)

# Token HuggingFace lấy từ Colab Secrets (khoá hình chìa bên trái, tên HF_TOKEN, bật
# "Notebook access"). Tải ẩn danh bị bóp băng thông và có lần treo cứng giữa chừng
# không báo lỗi — 10/8 đứng nguyên ở 409/800 MB, phải tải lại từ shard 0 vì script
# không có điểm nối lại. Đặt token là cách rẻ nhất tránh lặp lại.
os.environ["HF_TOKEN"] = userdata.get("HF_TOKEN")
print("token HF :", "có" if os.environ.get("HF_TOKEN") else "*** THIẾU ***")
print("lõi CPU  :", os.cpu_count())
print("đĩa trống:", f"{shutil.disk_usage(WS)[2]/2**30:.1f} GB   ← cần ≥ 40")
print("script   :", len([f for f in os.listdir('harness') if f.endswith('.py')]), "(chờ 29)")
print("phần OCR đã cất trên Drive:", len(os.listdir(f"{D}/ocr_parts")), "tệp")
```

### Ô C.2 — cài gói (nhẹ: KHÔNG torch, KHÔNG LLaMA-Factory)

```python
!pip install -q rapidocr_onnxruntime pillow pyarrow huggingface_hub transformers
```

Phiên 0 chỉ cần chừng đó. Cài xong **không cần restart**.

### Ô C.3 — tải ảnh (nền, ~30 phút) rồi khôi phục phần OCR đã làm

```python
import os; os.chdir(REPO)
assert os.environ.get("HF_TOKEN"), "chạy lại C.1 — thiếu token thì tải hay treo"
!nohup python harness/build_train_data.py --shards 76 > /content/build.log 2>&1 &
print("đang tải ảnh — theo dõi bằng ô 0.5, xong mới chạy C.4")
```

⚠️ **Khâu này không có điểm nối lại.** `iter_images()` luôn bắt đầu từ shard 0 và
`_drop_parquet()` xoá parquet ngay sau khi đọc, nên đứt giữa chừng là tải lại toàn bộ
(~65 phút). Ảnh đã có trên đĩa bị ghi đè y hệt nên không hỏng, chỉ mất thời gian. `train.jsonl`
cũng chỉ được ghi ở dòng cuối cùng, sau cả 76 shard.

Script **không in dòng tiến độ nào** cho tới khi xong, nên `build.log` chỉ có mỗi cảnh báo HF
suốt cả tiếng — đó là bình thường, đừng đọc nó như dấu hiệu treo. Nhìn số ảnh ở ô 0.5.

### Ô C.3b — theo dõi tải ảnh, TỰ CHẠY (thay ô 0.5, không phải bấm lại)

```python
import os, time, glob, subprocess
IM  = f"{REPO}/harness/dg1_cache/train_ac/images"
JS  = f"{REPO}/harness/dg1_cache/train_ac/train.jsonl"
inc = lambda: sum(os.path.getsize(p) for p in
                  glob.glob(os.path.expanduser("~/.cache/huggingface/**/*.incomplete"), recursive=True))
t0, dung_yen, truoc = time.time(), 0, None
print("giờ        ảnh          %     ghi/2ph   đang tải   đĩa    tốc độ      còn lại")
while True:
    now  = time.time()
    tong = len(os.listdir(IM)) if os.path.isdir(IM) else 0
    moi  = sum(1 for e in os.scandir(IM) if now - e.stat().st_mtime < 120) if tong else 0
    tai  = inc() / 2**20
    song = "build_train_data" in subprocess.run(["ps","-eo","args"],capture_output=True,text=True).stdout
    v = os.statvfs("/content"); trong = v.f_bavail*v.f_frsize/2**30
    r = tong / max(now - t0, 1)
    con = f"{(64567-tong)/r/60:5.0f} ph" if r > 0.5 else "    ?  "
    moc = (tong, round(tai))
    dung_yen = dung_yen + 1 if moc == truoc and moi == 0 else 0
    truoc = moc
    print(f"{time.strftime('%H:%M:%S')}  {tong:6,}/64.567 {tong/64567:5.1%}  {moi:6,}  "
          f"{tai:6.0f} MB  {trong:5.1f}G  {r:5.1f} ả/s  {con}"
          + ("  ⚠ ĐỨNG YÊN" if dung_yen else ""), flush=True)
    if dung_yen >= 4:
        print("*** TREO — giết rồi chạy lại C.3 ***"); break
    if os.path.exists(JS) and not song:
        print("*** XONG — chạy ô 0.6 ***"); break
    if not song:
        print("*** TIẾN TRÌNH CHẾT mà chưa có train.jsonl — dán build.log ***"); break
    time.sleep(60)
```

Tự làm mới mỗi phút, tự dừng khi xong, và tự báo khi treo 4 phút liền.

⚠️ Lúc **chạy lại** sau khi đứt, `tổng ảnh` sẽ **đứng yên suốt ~45 phút đầu** — vì script quay
về shard 0 và ghi đè lên ảnh đã có. Nhìn `ghi lại 2 phút` và `đang tải`, đừng nhìn tổng ảnh.

Xong (64.567 ảnh) thì kiểm bằng **ô 0.6**, rồi:

```python
!cp {D}/ocr_parts/*.jsonl {REPO}/harness/dg1_cache/train_ac/ 2>/dev/null
import glob
print("khôi phục", len(glob.glob(f"{REPO}/harness/dg1_cache/train_ac/ocr.part*.jsonl")), "mảnh từ Drive")
```

### Ô C.4 — OCR + ĐỒNG BỘ LÊN DRIVE ⚠️ thay hẳn ô 0.7

```python
import os, subprocess
os.makedirs(f"{D}/ocr_parts", exist_ok=True)
NP = os.cpu_count()
cmd = " ".join(f"nohup python harness/prep_ocr_train.py --shard {k} --nshard {NP} > /content/ocr{k}.log 2>&1 &"
               for k in range(NP))
subprocess.run(cmd, shell=True, cwd=REPO)

# đồng bộ mảnh OCR lên Drive mỗi 5 phút — đây là thứ đã thiếu hôm mất máy.
# CÓ NHẬT KÝ: bản đầu tiên nuốt lỗi bằng 2>/dev/null, Drive trục trặc thì im lặng
# không chép gì và chỉ lộ ra lúc mất máy — đúng kiểu hỏng đã trả giá một lần rồi.
sync = ('while true; do '
        f'cp {REPO}/harness/dg1_cache/train_ac/ocr.part*.jsonl {D}/ocr_parts/ 2>>/content/sync.err; '
        f'echo "$(date +%H:%M:%S)  $(ls {D}/ocr_parts/ | wc -l) mảnh  $(du -sh {D}/ocr_parts/ | cut -f1)"; '
        'sleep 300; done')
subprocess.run(f"nohup bash -c '{sync}' >> /content/sync.log 2>&1 &", shell=True)
print(f"đã khởi động {NP} tiến trình OCR + đồng bộ Drive (có nhật ký)")
```

### Ô C.5 — KIỂM ĐỒNG BỘ, chạy sau C.4 chừng 7 phút ⚠️ đừng bỏ qua

```python
import os
print(open("/content/sync.log").read()[-500:])
print("lỗi khi chép:", open("/content/sync.err").read()[-300:] if os.path.exists("/content/sync.err") else "(không có)")
print("trên Drive  :", sorted(os.listdir(f"{D}/ocr_parts")))
```

Phải thấy dòng nhật ký với số mảnh **> 0** và danh sách trên Drive **không rỗng**. Chưa thấy
thì **dừng, báo mình** — mất 7 phút để biết còn hơn mất 10 tiếng để biết. Cơ chế này viết
ngày 10/8 và chưa từng chạy lần nào; `report/109` đã ghi bài học "bản vá cũng phải kiểm".

### Ô C.6 — theo dõi tự chạy (thay ô 0.8, không phải bấm lại)

```python
import glob, subprocess, time, json
P = f"{REPO}/harness/dg1_cache/train_ac/ocr.part*.jsonl"
# ĐẾM ẢNH KHÁC NHAU, không đếm dòng. Đổi số tiến trình giữa chừng (2 → 12) đẻ ra bản
# trùng; ngày 11/8 có 957 dòng trùng làm ô này tưởng đã 100,5% và dừng sớm khi còn
# thiếu 559 ảnh thật — chạy trơn, không báo lỗi, chỉ ô 0.9a mới lộ ra.
count = lambda: len({json.loads(l)["image"] for p in glob.glob(P)
                     for l in open(p, encoding="utf-8", errors="ignore")})
t0, n0 = time.time(), count()
print(f"bắt đầu ở {n0:,}/64.567 = {n0/64567:.1%}")
print("giờ        đã OCR         %      tốc độ      còn lại   tiến trình")
while True:
    time.sleep(300)
    n = count()
    alive = subprocess.run(["ps","-eo","args"], capture_output=True, text=True).stdout.count("prep_ocr_train")
    r = (n - n0) / max(time.time() - t0, 1)
    con = f"{(64567-n)/r/3600:5.1f} giờ" if r > 0.01 else "   ?    "
    print(f"{time.strftime('%H:%M:%S')}  {n:6,}/64.567 {n/64567:6.1%}  {r:5.2f} ả/s  {con}   {alive}",
          flush=True)
    if n >= 64567 or alive == 0:
        print("*** DỪNG — chạy ô 0.9a rồi 0.9 ***"); break
```

Phiên đứt thì: đổi lại runtime CPU → **C.1 → C.2 → C.3 → C.4**. Nó nhặt tiếp từ chỗ Drive
giữ, mất tối đa 5 phút công OCR (ảnh phải tải lại 30 phút, nhưng miễn phí).

⚠️ **`--merge` chỉ được chạy ĐÚNG MỘT LẦN.** Nó mở `ocr.jsonl` ở chế độ nối thêm và không
đọc tệp cũ vào tập `seen`, nên merge lần hai là nhân đôi bản ghi — mà ô kiểm phủ dùng tập
hợp nên **không bắt được**. Chạy lại thì xoá `ocr.jsonl` trước.

### Ô 0.1 — nhận diện máy

```python
import os, subprocess, torch, shutil
print("lõi CPU     :", os.cpu_count())
print("card        :", subprocess.run(["nvidia-smi","--query-gpu=name,memory.total","--format=csv,noheader"],
                                       capture_output=True,text=True).stdout.strip())
print("số card     :", torch.cuda.device_count())
print("bf16 thật   :", torch.cuda.get_device_capability()[0] >= 8)
print()
print(subprocess.run(["df","-h"],capture_output=True,text=True).stdout)
for d in ("/content", "/mnt/disks/local-scratch", "/mnt/local-scratch", "/tmp"):
    if os.path.isdir(d):
        t,u,f = shutil.disk_usage(d)
        print(f"  {d:28} trống {f/2**30:6.1f} GB / {t/2**30:6.1f} GB")
```

## 🛑 MỐC DỪNG 1 — dán toàn bộ output ô 0.1

Mình cần bốn thứ để chốt trước khi bạn tải 67 GB về nhầm chỗ:

- **số card** phải là 1. Khác 1 → phải đặt `CUDA_VISIBLE_DEVICES` và khởi động lại
- **tên card** phải có chữ A100. Ra L4/T4 → đổi runtime, đừng chạy tiếp
- **số lõi CPU** → quyết định OCR mất 1 giờ hay 5 giờ, và có nên tách khâu này ra máy khác không
- **local-scratch gắn ở đâu** → nếu có và rộng, để dữ liệu ở đó (NVMe, nạp ảnh lúc train
  nhanh hơn hẳn); nếu không thì dùng `/content`

Mình trả lời xong bạn mới chạy ô 0.2.

---

### Ô 0.2 — gắn Drive, bung mã

```python
from google.colab import drive; drive.mount('/content/drive')
import os, zipfile, shutil
D  = "/content/drive/MyDrive/thesis"
WS = "/content/ws"            # chốt 10/8: máy không có local-scratch → để ở /content
os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_rented.zip").extractall(WS)
REPO = f"{WS}/thesis"; os.chdir(REPO)

print("script         :", len([f for f in os.listdir("harness") if f.endswith(".py")]), "(chờ 29)")
print("OCR tập kiểm   :", sum(1 for _ in open("harness/dg1_cache/test_ac/ocr.jsonl")), "(chờ 6969)")
print("tập kiểm       :", sum(1 for _ in open("harness/dg1_cache/test_ac/test.jsonl")), "(chờ 6958)")
print("nhãn tập kiểm  :", sum(1 for _ in open("harness/dg1_cache/test_ac/descriptors.jsonl")), "(chờ 4448)")
```

Bốn số phải khớp. Lệch bất kỳ số nào là gói tải lên Drive hỏng — tải lại, đừng chạy tiếp.

### Ô 0.2b — hạn mức Drive thật (quyết `CAT_ANH_DAY` ở ô 0.12)

```python
from google.colab import auth; auth.authenticate_user()
from googleapiclient.discovery import build
q = build('drive','v3').about().get(fields='storageQuota').execute()['storageQuota']
lim, used = int(q['limit']), int(q['usage'])
print(f"Drive: dùng {used/2**30:,.1f} GB / hạn mức {lim/2**30:,.1f} GB · trống {(lim-used)/2**30:,.1f} GB")
```

⚠️ **Đừng hỏi bằng `shutil.disk_usage("/content/drive/…")`** — hàm đó trả về đĩa của máy ảo
(112,6 GB), không phải hạn mức Drive, và nhìn ra một con số hợp lý nên rất dễ tin nhầm. Đã
mắc đúng lỗi này ngày 10/8.

Cần trống **≥ 4 GB** để chạy được (derived + ảnh kiểm + điểm lưu), **≥ 40 GB** thì mới bật
`CAT_ANH_DAY = True` cất thêm 31 GB ảnh dạy.

### Ô 0.3 — cài gói

```python
!pip install -q -U "transformers>=4.49" accelerate peft bitsandbytes datasets \
    huggingface_hub pyarrow pillow rapidocr_onnxruntime pyyaml liger-kernel
!git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory /content/LLaMA-Factory
!pip install -q -e "/content/LLaMA-Factory[torch,metrics]"
import importlib.metadata as m
print("liger-kernel:", m.version("liger_kernel"))     # ← thiếu gói này là A.4 chết ngay
```

⚠️ **`liger-kernel` bắt buộc từ 11/8** (cấu hình P9 bật `enable_liger_kernel: true`). Thiếu
nó thì `llamafactory-cli` **chết ngay lúc kiểm phụ thuộc**, trước cả khi nạp dữ liệu:
`PackageNotFoundError: The 'liger-kernel' distribution was not found`. Đã vấp đúng lỗi này
sáng 12/8 — ô 0.3 khi đó chưa có gói, còn `cfg.yaml` thì đã yêu cầu. Cài rời rồi chạy lại
A.4 là xong, **không cần restart** (LLaMA-Factory chạy ở tiến trình con nên thấy gói mới).

Xong → **Runtime → Restart session** → chạy lại **ô 0.2** (không cần 0.3 nữa).

### Ô 0.4 — tải ảnh tập dạy, chạy NỀN

```python
import os; os.chdir(REPO)
!nohup python harness/build_train_data.py --shards 76 > /content/build.log 2>&1 &
print("đã khởi động, theo dõi bằng ô kế")
```

### Ô 0.5 — theo dõi (chạy lại ô này nhiều lần, mỗi lần vài giây)

```python
import os, subprocess, shutil, time
n = len(os.listdir(f"{REPO}/harness/dg1_cache/train_ac/images")) if os.path.isdir(f"{REPO}/harness/dg1_cache/train_ac/images") else 0
alive = "build_train_data" in subprocess.run(["ps","-eo","args"],capture_output=True,text=True).stdout
f = shutil.disk_usage(WS)[2]/2**30
print(f"ảnh: {n:,} / ~64.500   ·   đĩa trống: {f:.1f} GB   ·   tiến trình: {'đang chạy' if alive else 'ĐÃ DỪNG'}")
!tail -3 /content/build.log
```

Chừng 20-40 phút. **Đỉnh đĩa lẽ ra chỉ ~32 GB** (31 GB ảnh + 1 shard parquet đang đọc), nên
với 65,9 GB trống thì cuối khâu còn phải dư ~33 GB. Tụt xuống dưới **20 GB** là dấu hiệu
parquet không được xoá — dừng lại báo mình, đừng để đầy đĩa giữa chừng.

### Ô 0.6 — kiểm dữ liệu dạy vừa dựng

```python
import json, collections
T = f"{REPO}/harness/dg1_cache/train_ac"
recs = [json.loads(l) for l in open(f"{T}/train.jsonl", encoding="utf-8")]
taps = [r for r in recs if r["action"].get("action_type") in ("click","long_press") and "x" in r["action"]]
import os
print(f"bước       : {len(recs):,}      (ước từ 2 shard: ~64.500)")
print(f"bước chạm  : {len(taps):,} = {len(taps)/len(recs):.1%}   (lát 2 shard cho 63,3%)")
print(f"tác vụ     : {len({r['episode_id'] for r in recs}):,}")
print(f"ảnh        : {len(os.listdir(f'{T}/images')):,}")
print(f"thiếu ảnh  : {sum(1 for r in recs if not os.path.exists(os.path.join(T, r['image'])))}   ← phải là 0")
```

## 🛑 MỐC DỪNG 2 — dán output ô 0.6

Trước khi bỏ 3 tiếng CPU vào OCR, mình muốn chắc dữ liệu dạy đúng. Cần xem: tổng số bước
có gần 64.500 không, tỉ lệ bước chạm có quanh 63% không (lệch xa nghĩa là ghép sai), và
thiếu ảnh phải bằng 0.

---

### Ô 0.7 — OCR, chạy NỀN

```python
import os, subprocess
NP = min(os.cpu_count(), 24)
print("dùng", NP, "tiến trình")
cmd = " ".join(f"nohup python harness/prep_ocr_train.py --shard {k} --nshard {NP} > /content/ocr{k}.log 2>&1 &"
               for k in range(NP))
subprocess.run(cmd, shell=True, cwd=REPO)
print("đã khởi động", NP, "tiến trình")
```

### Ô 0.8 — theo dõi OCR (chạy lại nhiều lần)

```python
import glob, subprocess, time, json, os
done = sum(sum(1 for _ in open(p, encoding="utf-8")) for p in glob.glob(f"{REPO}/harness/dg1_cache/train_ac/ocr.part*.jsonl"))
tot  = sum(1 for _ in open(f"{REPO}/harness/dg1_cache/train_ac/train.jsonl", encoding="utf-8"))
alive = subprocess.run(["ps","-eo","args"],capture_output=True,text=True).stdout.count("prep_ocr_train")
print(f"OCR: {done:,} / {tot:,} = {done/tot:.1%}   ·   tiến trình sống: {alive}")
```

**Nhìn cột "tiến trình sống".** Nó phải giữ nguyên bằng `NP` cho tới gần cuối. Tụt dần
giữa chừng nghĩa là có tiến trình chết (thường do thiếu RAM) — dừng lại báo mình, đừng
để chạy tiếp rồi merge ra một tệp thiếu mà không ai biết.

⛔ **"Với 12 lõi mất ~2,8 giờ" LÀ SỐ SAI — đã rút 10/8.** Nó tính trên **6.969 ảnh của tập
KIỂM**, trong khi khâu này chạy trên **64.567 ảnh tập DẠY**, gấp **9,3 lần**. Theo tốc độ
0,08 ảnh/giây/luồng ghi ở `prep_ocr_train.py:40` thì 12 tiến trình mất **~19 giờ ≈ 100 đơn
vị**, không phải 15. Đây là khâu đắt nhất phiên 0 và **card nằm không suốt thời gian đó**.

**Số ĐO THẬT trên Colab A100-40GB, 10/8/2026:** một luồng **0,451 ảnh/giây**, nhưng 12 tiến
trình chỉ cho **2,22 ảnh/giây gộp** — không phải 4,6 như phép nhân 12×0,451×0,85. Lý do:
`os.cpu_count()` báo 12 nhưng đó là **6 lõi vật lý siêu phân luồng**, hệ số đúng là ×6 chứ
không phải ×12. ⇒ **64.567 ảnh mất 8,1 giờ ≈ 43 đơn vị.**

**Bắt buộc đo tốc độ thật trước khi chạy**, và đo **gộp sau 10 phút chạy song song**, đừng
suy từ tốc độ một luồng — sai số ở đây là 2 lần.

Chạy lại vô hại: ảnh đã có kết quả thì bỏ qua (đọc `ocr.part*.jsonl` cũ), nên đứt phiên hay
hết đơn vị đều không mất phần đã làm.

### Ô 0.9a — KIỂM MẢNH TRƯỚC KHI GỘP ⚠️ chạy trước 0.9

```python
import json, glob, os
tong, bad, keys = 0, 0, {}
for p in sorted(glob.glob(f"{REPO}/harness/dg1_cache/train_ac/ocr.part*.jsonl")):
    n = 0
    with open(p, encoding="utf-8") as f:
        for i, l in enumerate(f, 1):
            try: k = json.loads(l)["image"]
            except Exception as e:
                print(f"  ⚠️ {os.path.basename(p)} dòng {i} HỎNG: {type(e).__name__}"); bad += 1; continue
            keys[k] = keys.get(k, 0) + 1; n += 1
    tong += n
    print(f"  {os.path.basename(p):22} {n:6,} dòng")
print(f"\ntổng {tong:,} dòng · {len(keys):,} ảnh khác nhau · trùng {tong-len(keys):,} · dòng HỎNG {bad}")
print("→ cần", 64567 - len(keys), "ảnh nữa" if len(keys) < 64567 else "ĐỦ")
```

Vì sao cần: máy ảo bị thu hồi **giữa lúc đang ghi** (đã xảy ra hai lần, 10/8 và 11/8). Ghi
dở một dòng thì `--merge` gặp `json.loads` sẽ **văng giữa chừng** và để lại `ocr.jsonl` ghi
được một nửa — mà ô 0.9 lại mở ở chế độ nối thêm nên chạy lại là nhân đôi. Bắt ở đây rẻ hơn.

`dòng HỎNG > 0` thì vá bằng cách lọc bỏ dòng hỏng trước khi gộp:

```python
import json, glob, os
for p in sorted(glob.glob(f"{REPO}/harness/dg1_cache/train_ac/ocr.part*.jsonl")):
    ok = []
    for l in open(p, encoding="utf-8"):
        try: json.loads(l); ok.append(l)
        except Exception: pass
    open(p, "w", encoding="utf-8").writelines(ok)
print("đã lọc xong, chạy lại 0.9a")
```

`trùng` khác 0 là bình thường nếu có đổi số tiến trình giữa chừng — `--merge` khử theo tên ảnh.

### Ô 0.9 — gộp và KIỂM PHỦ

```python
!cd {REPO} && python harness/prep_ocr_train.py --merge
import json
T = f"{REPO}/harness/dg1_cache/train_ac"
ocr = {json.loads(l)["image"] for l in open(f"{T}/ocr.jsonl", encoding="utf-8")}
recs = [json.loads(l) for l in open(f"{T}/train.jsonl", encoding="utf-8")]
thieu = [r["image"] for r in recs if r["image"] not in ocr]
print(f"OCR: {len(ocr):,} ảnh · phủ {len(recs)-len(thieu):,}/{len(recs):,} bước = {1-len(thieu)/len(recs):.2%}")
print(f"THIẾU: {len(thieu)}   ← phải là 0")
if thieu: print("ví dụ:", thieu[:5], "→ chạy lại ô 0.7, nó chỉ làm phần thiếu")
```

**Đây là phép kiểm quan trọng nhất của phiên 0.** Merge từ các phần rời mà một tiến
trình chết sớm thì tệp gộp vẫn hợp lệ, chỉ thiếu vài nghìn ảnh — và những bước đó sẽ vào
huấn luyện với đầu vào **thiếu dòng chữ đọc được**, khác hẳn lúc chấm. Không có ô này thì
không đường nào phát hiện.

### Ô 0.9b — CHẤT LƯỢNG bộ đọc chữ, không chỉ độ phủ

```python
import json, statistics as st
def tk(p):
    per = []
    for l in open(p, encoding="utf-8"):
        per.append(len(json.loads(l)["items"]))
    return len(per), st.mean(per), st.median(per), sum(1 for k in per if k == 0)/len(per)
T = f"{REPO}/harness/dg1_cache"
for ten, p in [("tập KIỂM (máy khác, 6/8)", f"{T}/test_ac/ocr.jsonl"),
               ("tập DẠY  (Colab, hôm nay)", f"{T}/train_ac/ocr.jsonl")]:
    n, m, md, z = tk(p)
    print(f"{ten:26} {n:6,} ảnh · trung bình {m:5.1f} chữ/màn · trung vị {md:4.0f} · màn rỗng {z:5.1%}")
```

Đây là **phép kiểm chéo máy** rẻ nhất có được: hai tập lấy từ cùng một nguồn ảnh, chạy cùng
một bộ đọc chữ, nhưng trên hai máy khác nhau cách nhau 5 ngày. Hai dòng phải sát nhau — lệch
quá ~15% ở "trung bình chữ/màn" hoặc "màn rỗng" nghĩa là bộ đọc chữ hành xử khác trên máy
này, và đó là loại lệch sẽ đi thẳng vào nhãn khai báo rồi ra tới điểm cuối.

⚠️ Đây **không** phải phép đo bộ đọc chữ đúng hay sai so với chữ thật trên màn — dự án chưa
bao giờ đo cái đó, và không nên nói là đã đo. Nó chỉ trả lời "máy này có đọc giống máy kia
không". Giới hạn đã biết, phải khai trong luận văn: bộ đọc chữ **đọc nhầm biểu tượng thành
ký tự** (`build_train_data.py:152` ghi rõ), nên tỉ lệ khớp tuyệt đối ở ô 0.11c luôn là cận dưới.

### Ô 0.9c — nhìn tận mắt 3 màn (tuỳ chọn, 1 phút)

```python
import json, random, os
from PIL import Image
from IPython.display import display
T = f"{REPO}/harness/dg1_cache/train_ac"
recs = [json.loads(l) for l in open(f"{T}/ocr.jsonl", encoding="utf-8")]
random.seed(20260805)
for r in random.sample(recs, 3):
    print(r["image"], "·", len(r["items"]), "cụm chữ")
    print("  ", " | ".join(i["text"] for i in r["items"][:12]))
    display(Image.open(os.path.join(T, r["image"])).resize((270, 600)))
```

Chữ in ra phải trùng với chữ nhìn thấy trên ảnh. Một phút này bắt được loại hỏng mà mọi
thống kê ở trên đều bỏ lọt: đọc đúng số lượng nhưng sai nội dung.

### Ô 0.10 — nhãn khai báo + bốn nhánh + tập kiểm

```python
!cd {REPO} && python harness/descriptor_label_build.py 2>&1 | tail -25
```

```python
!cd {REPO} && python harness/build_branch_data.py --img-prefix "{REPO}/harness/dg1_cache/train_ac/" 2>&1 | tail -12
!cd {REPO} && python harness/build_test_data.py --shards 9 2>&1 | tail -12
!cd {REPO} && python harness/tag_app_seen.py 2>&1 | tail -8
```

### Ô 0.10b — CẤT PHẦN ĐẮT NHẤT LÊN DRIVE NGAY ⚠️ đừng đợi tới 0.12

```python
!cd {REPO} && tar czf {D}/derived_train.tar.gz \
    harness/dg1_cache/train_ac/ocr.jsonl \
    harness/dg1_cache/train_ac/train.jsonl \
    harness/dg1_cache/train_ac/descriptors.jsonl \
    harness/dg1_cache/train_ac/branches \
    harness/descriptor_build_stats.json
!ls -lh {D}/derived_train.tar.gz
```

`ocr.jsonl` là **8 giờ máy** đóng thành một tệp. Ô 0.12 nằm sau cả loạt kiểm 0.11 → 0.11e,
tức còn nửa tiếng nữa mới tới — mà máy ảo đã bị thu hồi hai lần trong hai ngày, cả hai lần
đều lúc không ai ngồi trước máy. Cất ngay khi vừa có, đừng cất ở cuối.

Tên khác `derived.tar.gz` của ô 0.12 để lát nữa 0.12 không ghi đè lên bản này khi nó chưa
chắc chạy trót lọt.

### Ô 0.11 — KIỂM 9 BẤT BIẾN của bốn nhánh

```python
import json, re
B = f"{REPO}/harness/dg1_cache/train_ac/branches"
d = {b: json.load(open(f"{B}/{b}.json", encoding="utf-8")) for b in ("s1","s2","s2r","s2_nopoint")}
cau  = lambda x: (lambda t: t.split("</desc>",1)[1].strip() if "</desc>" in t else t.strip())(x["messages"][-1]["content"])
desc = lambda x: (lambda m: m.group() if m else None)(re.search(r"<desc>.*?</desc>", x["messages"][-1]["content"], re.S))
n = len(d["s1"]); nd = sum(1 for x in d["s2"] if desc(x))
K = []
for b in ("s2","s2r","s2_nopoint"):
    K.append((f"câu {b} trùng s1", sum(1 for x,y in zip(d[b],d["s1"]) if cau(x)==cau(y)), n))
K.append(("s1 KHÔNG có khai báo", sum(1 for x in d["s1"] if desc(x) is None), n))
for b in ("s2","s2r","s2_nopoint"):
    K.append((f"số khai báo {b}", sum(1 for x in d[b] if desc(x)), nd))
K.append(("s2_nopoint sót <point>", sum(1 for x in d["s2_nopoint"] if desc(x) and "<point>" in desc(x)), 0))
K.append(("s2r khác s2 ở bước có desc", sum(1 for x,y in zip(d["s2r"],d["s2"]) if desc(x) and desc(y) and desc(x)!=desc(y)), nd))
bad = 0
for nm, got, want in K:
    ok = got == want; bad += not ok
    print(f"  {'ĐẠT' if ok else 'RỚT'}  {nm:30} {got:,}" + ("" if ok else f"  ≠ {want:,}"))
print(f"\n{n:,} mẫu mỗi nhánh · {nd:,} khai báo · " + ("TẤT CẢ ĐẠT" if not bad else f"{bad} BẤT BIẾN RỚT"))
```

### Ô 0.11b — RÒ RỈ giữa tập dạy và tập kiểm ⚠️ ô quan trọng nhất phiên 0

```python
import json
TR = f"{REPO}/harness/dg1_cache/train_ac/train.jsonl"
TE = f"{REPO}/harness/dg1_cache/test_ac/test.jsonl"
etr = {json.loads(l)["episode_id"] for l in open(TR, encoding="utf-8")}
ete = {json.loads(l)["episode_id"] for l in open(TE, encoding="utf-8")}
chung = etr & ete
print(f"tác vụ trong tập dạy : {len(etr):,}")
print(f"tác vụ trong tập kiểm: {len(ete):,}")
print(f"TRÙNG NHAU           : {len(chung)}   ← PHẢI LÀ 0")
if chung: print("   ví dụ:", sorted(chung)[:10])
```

**Nếu ra khác 0 thì DỪNG TOÀN BỘ, đừng train.** Mô hình học đúng những tác vụ sẽ đem chấm
thì mọi con số về sau đều vô nghĩa, và đây là lỗi không có cách nào chữa sau khi đã train.

Cho tới nay "0 tác vụ trùng" mới **chỉ kiểm trên lát 2 shard**. Ở quy mô 76 shard chưa ai
kiểm. Hai tập lấy từ `train-*.parquet` và `test-*.parquet` nên *lẽ ra* rời nhau, nhưng
"lẽ ra" không phải bằng chứng — và đây là loại sai không sửa được sau khi phát hiện.

### Ô 0.11c — phép ghép ảnh ↔ câu chuẩn còn đúng ở quy mô đủ không

```python
!cd {REPO} && python harness/build_train_data.py --check 2>&1 | grep -E "KIỂM GHÉP|ghép ĐÚNG|ghép LỆCH"
```

⚠️ `tail -5` (bản cũ) **cắt mất đúng hai dòng số cần đọc** — nó chỉ chừa lại mấy ví dụ và
lời chú, nhìn thì tưởng có kết quả mà thật ra không có con số nào để đối chiếu. Sửa 11/8.

Đọc chữ quanh điểm chạm rồi so với câu chuẩn, đối chứng bằng ghép lệch một bước. Lát 2
shard cho **47% so với 27%**. Ra chênh dưới 1,4 lần là ghép sai ở đâu đó — dừng, báo mình.

### Ô 0.11d — tập kiểm dựng lại có khớp bản đã khoá không

```python
import json
T = f"{REPO}/harness/dg1_cache/test_ac"
recs = [json.loads(l) for l in open(f"{T}/test.jsonl", encoding="utf-8")]
taps = [r for r in recs if r["action"].get("action_type") in ("click","long_press") and "x" in r["action"]]
desc = {(json.loads(l)["episode_id"], json.loads(l)["step_id"])
        for l in open(f"{T}/descriptors.jsonl", encoding="utf-8")}
phu = sum(1 for r in taps if (r["episode_id"], r["step_id"]) in desc)
print(f"bước      : {len(recs):,}   ← phải là 6.958")
print(f"bước chạm : {len(taps):,}   ← phải là 4.463")
print(f"nhãn khai báo phủ: {phu:,}/{len(taps):,} = {phu/len(taps):.1%}   ← phải ~99,7%")
```

`build_test_data.py` ở ô 0.10 **ghi đè** `test.jsonl`, trong khi nhãn khai báo mang theo
trong gói dựng từ bản cũ. Hai bản lệch thì phép thử TRẦN lặng lẽ phủ thiếu — vẫn chạy,
vẫn ra số, chỉ là số của một tập nhỏ hơn. Đây đúng kiểu lỗi đã bắt hôm 7/8 (bộ lọc 11 bản
ghi rỗng nằm ở vá tay chứ không nằm trong mã, dựng lại ra 6.969 thay vì 6.958).

### Ô 0.11e — phân bố nhãn ứng dụng

```python
import json, collections
c = collections.Counter(json.loads(l).get("app_seen_in_train")
                        for l in open(f"{REPO}/harness/dg1_cache/test_ac/test.jsonl", encoding="utf-8"))
tot = sum(c.values())
for k, v in c.most_common():
    ten = {True: "app ĐÃ thấy lúc dạy", False: "app CHƯA thấy", None: "không gán được app"}[k]
    print(f"  {ten:22} {v:6,} = {v/tot:5.1%}")
```

Nhóm `False` chính là **lát cắt phụ đã đăng ký**. Con số này quyết định lát đó có đủ mẫu
để báo hay không — dưới ~100 bước chạm thì phải khai là quá nhỏ, không kết luận được.

## 🛑 MỐC DỪNG 3 — dán output ô 0.9, 0.10, 0.11, 0.11b → 0.11e

Đây là mốc **quan trọng nhất trước khi tiêu tiền thật**. Sau mốc này là 11-18 giờ train.
Mình cần đối chiếu:

- **phủ OCR** phải 100%
- **thống kê nhãn khai báo**: tên rõ ~74% · không tên ~23% · vai trò rõ ~76% · trùng tên
  ~7% · có hàng xóm ~92%. Lệch xa mấy con số này (đo trên lát 1.697 và trên tập kiểm
  4.448, hai lần đều khớp nhau) nghĩa là khâu dựng nhãn hỏng ở quy mô lớn
- **9 bất biến** phải đạt cả 9. Rớt một cái là bốn nhánh không so được với nhau
- **rò rỉ (ô 0.11b) phải bằng 0** — đây là điều kiện sống còn, sai là bỏ cả luận văn
- **phép ghép (ô 0.11c)** chênh phải trên 1,4 lần
- **tập kiểm (ô 0.11d)** vẫn 6.958 / 4.463, nhãn khai báo phủ ~99,7%
- **phân bố `app_seen_in_train`** — quyết định lát cắt phụ có đủ mẫu để báo hay không

---

### Ô 0.12 — cất lên Drive ⚠️ ĐỪNG BỎ QUA

```python
import os, shutil
CAT_ANH_DAY = True    # Drive 5 TB → cất luôn, khỏi tải lại 20-40 phút mỗi phiên

os.makedirs(f"{D}/ckpt", exist_ok=True); os.makedirs(f"{D}/preds", exist_ok=True)
!cd {REPO} && tar czf {D}/derived.tar.gz \
    harness/dg1_cache/train_ac/ocr.jsonl harness/dg1_cache/train_ac/train.jsonl \
    harness/dg1_cache/train_ac/descriptors.jsonl harness/dg1_cache/train_ac/branches \
    harness/dg1_cache/test_ac/ocr.jsonl harness/dg1_cache/test_ac/test.jsonl \
    harness/dg1_cache/test_ac/descriptors.jsonl
!cd {REPO}/harness/dg1_cache/test_ac  && tar cf {D}/test_images.tar images
if CAT_ANH_DAY:
    # ⚠️ KHÔNG tar 31 GB thành MỘT tệp — Drive fuse ghi vào bộ nhớ đệm CỤC BỘ trước rồi
    # mới đẩy lên, nên một tệp 30 GB đòi thêm ~30 GB đĩa trống. Ngày 11/8 việc này chết
    # với `Cannot write: No space left on device` sau khi đã chạy một lúc, trong khi
    # Drive còn 5 TB — thông báo lỗi trỏ sai chỗ hoàn toàn. Cắt 4 gói thì đỉnh đệm chỉ
    # ~8 GB. Đo được: 4 gói × 16.142 mục, tổng 64.567, 29,6 GB, mất ~12 phút.
    import os
    IM = f"{REPO}/harness/dg1_cache/train_ac/images"
    files = sorted(os.listdir(IM)); N = 4
    for k in range(N):
        open(f"/content/part{k}.txt", "w").write("\n".join(files[k::N]))
    sh = "; ".join(f"tar -C {IM} -T /content/part{k}.txt -cf {D}/train_images_p{k}.tar"
                   for k in range(N))
    os.system(f"nohup bash -c '{sh}' > /content/tar.log 2>&1 &")
    print("đang đóng 4 gói ảnh dạy — theo dõi bằng ô 0.12b")
!ls -lh {D}/*.tar*
```

Dọn chỗ trước khi chạy, cả hai thứ này đều tái tạo được:

```python
!rm -rf {REPO}/harness/dg1_cache/test_ac/images   # đã có test_images.tar trên Drive
!rm -rf /root/.cache/huggingface                  # cây trợ năng, dựng nhãn xong rồi
!df -h /content | tail -1                          # cần ≥ 12 GB trống
```

### Ô 0.12b — theo dõi đóng gói + KIỂM TAR ĐỌC ĐƯỢC

```python
import os, time, subprocess
t0 = time.time()
print("giờ        đã đóng         %     đĩa trống   tốc độ       còn lại   gói xong")
while True:
    xong = [k for k in range(4) if os.path.exists(f"{D}/train_images_p{k}.tar")]
    tong = sum(os.path.getsize(f"{D}/train_images_p{k}.tar") for k in xong)/2**30
    song = "train_images_p" in subprocess.run(["ps","-eo","args"],capture_output=True,text=True).stdout
    v = os.statvfs("/content"); trong = v.f_bavail*v.f_frsize/2**30
    r = tong / max((time.time()-t0)/60, 1)
    con = f"{(30-tong)/r:5.0f} ph" if r > 0.01 else "    ?  "
    print(f"{time.strftime('%H:%M:%S')}  {tong:5.1f}/30 GB {tong/30:6.1%}  {trong:5.1f} GB  "
          f"{r:4.2f} GB/ph  {con}   {xong}"
          + ("  ⚠ ĐĨA SẮP ĐẦY" if trong < 5 else ""), flush=True)
    if not song:
        print("--- log ---"); print(open("/content/tar.log").read()[-400:]); break
    time.sleep(60)
```

Luật canh dòng `đĩa trống`: **>10 GB** bình thường (kệ cảnh báo của Colab) · **5-10 GB** chờ
5 phút xem Drive có xả đệm không · **<5 GB** giết tiến trình, xoá gói dở, báo lại.

Rồi kiểm — `ls` KHÔNG phát hiện tar hỏng vì tar dở vẫn có kích thước:

```python
import os
for t in ["derived.tar.gz", "derived_train.tar.gz", "test_images.tar"]:
    n = !tar tf {D}/{t} 2>/dev/null | wc -l
    print(f"{t:24} {os.path.getsize(f'{D}/{t}')/2**30:6.2f} GB · {n[0]} mục")
t = 0
for k in range(4):
    n = !tar tf {D}/train_images_p{k}.tar 2>/dev/null | wc -l
    print(f"train_images_p{k}.tar     {n[0]} mục"); t += int(n[0])
print("tổng ảnh dạy:", t, "  ← phải là 64.567")
```

Số đo 11/8: `derived.tar.gz` 13 mục (đủ 7 đường dẫn) · `test_images.tar` **6.959 mục** ·
4 gói ảnh dạy **16.142 + 16.142 + 16.142 + 16.141 = 64.567**.

⛔ **Đừng dùng `shutil.disk_usage` trên thư mục Drive** — nó trả đĩa của máy ảo, không phải
hạn mức Drive, mà con số lại trông hợp lý nên không ai nghi. Muốn xem hạn mức thật thì chạy
**ô 0.2b**.

`derived.tar.gz` (~400 MB) là **~3 giờ CPU đóng thành một tệp** — đây là thứ đắt nhất trong
phiên này, mất là mất tiền thật. `test_images.tar` (~2,5 GB) cần cho mọi lượt sinh câu.

**Ảnh dạy ~30 GB** (không phải 67 GB — xem mục đo máy ở đầu file). Lý do cất **không phải để
tiết kiệm 32 phút tải mỗi phiên** — đọc lại 30 GB từ Drive chưa chắc nhanh hơn tải về. Lý do
thật có hai, và cả hai đều là chuyện chất lượng:

1. **Bỏ điểm chết đơn lẻ.** Gói mã không chứa ảnh. Không cất thì suốt 12 lượt train, mỗi
   phiên đều phụ thuộc kho `ckg/AndroidControlParsedWithImages-20k` còn sống, còn công khai,
   không đổi tên. Kho biến mất giữa chiến dịch là mất trọn phiên 0.
2. **Tránh lệch nguồn âm thầm.** Ô A.1 lấy `train.jsonl` từ Drive nhưng ảnh từ HuggingFace —
   hai nguồn cho cùng một tập. Bên kia sửa dữ liệu thì bản kê và ảnh lệch nhau mà **không ô
   kiểm nào bắt được**, vì `thiếu ảnh 0` vẫn đúng khi tên tệp không đổi. Cất tar là đóng
   băng cả hai về cùng một bản chụp.

Tài khoản Drive chỉ có 15 GB thì đặt `CAT_ANH_DAY = False`, ô A.1 tự tải lại — nhưng phải
khai hai rủi ro trên thành giới hạn đã biết, đừng coi như không có.

**Điều kiện kết thúc phiên 0:** `derived.tar.gz` + `test_images.tar` + 4 gói
`train_images_p*.tar` nằm trên Drive **và đã kiểm bằng ô 0.12b** (tar đọc được, tổng đúng
64.567), mốc dừng 3 đã qua. **Tắt máy.**

---

# PHIÊN TRAIN — mỗi nhánh × mỗi hạt giống một phiên

### ⚠️ THỨ TỰ PHIÊN TRAIN — sửa 11/8, đọc trước khi bấm

**Cài gói TRƯỚC, khôi phục dữ liệu SAU.** Bản cũ ghi `A.1 → 0.3 → Restart → A.1 lại`, mà
A.1 bung 30 GB ảnh từ Drive — chạy lại sau restart là bung lần thứ hai, mất thêm nửa tiếng
tiền card. Restart chỉ khởi động lại nhân Python, **đĩa máy ảo vẫn còn nguyên**, nên không
có lý do gì bung hai lần.

Thứ tự đúng: **0.3 (cài gói) → Restart session → A.1 → A.2 → A.3**

Ô A.1 dưới đây đã có chốt chặn: thấy đủ 64.567 ảnh thì bỏ qua khâu bung, chạy lại vô hại.

### Ô A.1 — khôi phục

```python
from google.colab import drive; drive.mount('/content/drive')
import os, zipfile, torch
D, WS = "/content/drive/MyDrive/thesis", "/content/ws"
os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_rented.zip").extractall(WS)
REPO = f"{WS}/thesis"; os.chdir(REPO)
import glob
TR = f"{REPO}/harness/dg1_cache/train_ac"
TE = f"{REPO}/harness/dg1_cache/test_ac"
dem = lambda d: len(os.listdir(d)) if os.path.isdir(d) else 0

!tar xzf {D}/derived.tar.gz -C {REPO}
if dem(f"{TE}/images") < 6958:
    !tar xf {D}/test_images.tar -C {TE}
# ⚠️ derived.tar.gz KHÔNG chứa thư mục images/, mà 4 gói ảnh đóng bằng tên tệp trần nên
# `tar -C .../images` sẽ chết với "Cannot chdir" nếu thư mục chưa có. Tạo trước.
os.makedirs(f"{TR}/images", exist_ok=True)
goi = sorted(glob.glob(f"{D}/train_images_p*.tar"))   # 4 gói cất ở ô 0.12 (11/8)
if dem(f"{TR}/images") >= 64567:
    print("ảnh dạy đã có đủ — bỏ qua khâu bung")      # chạy lại ô này vô hại
elif goi:
    for g in goi:
        !tar xf {g} -C {TR}/images
    print("đã bung", len(goi), "gói ảnh dạy")
else:                                                 # không có thì tải lại, ~32 phút
    !cd {REPO} && nohup python harness/build_train_data.py --shards 76 > {D}/redl.log 2>&1 &
    print("→ đang tải lại 31 GB ảnh dạy. Theo dõi bằng ô C.3b, xong mới chạy ô A.2.")
print("card    :", torch.cuda.get_device_name(0), "| số card:", torch.cuda.device_count(),
      "| bf16 thật:", torch.cuda.get_device_capability()[0] >= 8)
print("lõi CPU :", os.cpu_count())
print("ảnh kiểm:", dem(f"{TE}/images"), " ← 6.958")
print("ảnh dạy :", dem(f"{TR}/images"), "← 64.567")
print("cutoff  :", __import__("yaml").safe_load(
      open(f"{REPO}/harness/train_config.yaml", encoding="utf-8"))["cutoff_len"], "← phải là 2560")
```

Dòng `cutoff` là để bắt chuyện gói cũ: nếu nó in **2048** thì `thesis_rented.zip` trên Drive
vẫn là bản trước 11/8 — tải lại gói mới rồi chạy lại ô này, đừng train.

⚠️ Bốn gói đóng bằng `tar -C images -T danh_sách` nên bên trong là **tên tệp trần**, không có
thư mục `images/` bọc ngoài — vì vậy phải bung vào thẳng `train_ac/images`, khác với
`test_images.tar` (đóng cả thư mục nên bung vào `test_ac`). Bung nhầm chỗ thì ảnh nằm sai và
`thiếu ảnh` sẽ khác 0. Hai dòng đếm cuối ô này là để bắt đúng chuyện đó.

⚠️ Nhánh tải-lại chạy nền. **Chờ nó xong** (ô 0.5 in đủ số ảnh khớp `train.jsonl`) rồi mới
sang ô A.2 — bắt đầu train khi ảnh còn thiếu thì mất cả lượt mà log không báo gì.

⚠️ **Đường dẫn ảnh bị nướng CỨNG vào bốn tệp nhánh.** `build_branch_data.py` chạy với
`--img-prefix /content/ws/thesis/harness/dg1_cache/train_ac/`, nên `s1.json` … chứa đường dẫn
tuyệt đối. **Đổi `WS` khỏi `/content/ws` là mọi ảnh trỏ trượt** — LLaMA-Factory sẽ báo thiếu
tệp, hoặc tệ hơn là chạy được với ảnh rỗng tuỳ phiên bản. Giữ nguyên `WS`, hoặc dựng lại bốn
nhánh bằng `--img-prefix` mới.

⛔ **Câu "card không phải A100 thì DỪNG PHIÊN" đã RÚT (11/8).** Nó viết khi tưởng A100 là
lựa chọn duy nhất; đo ngày 11/8 cho thấy **L4 chỉ 1,54 đơn vị/giờ so với A100 5,3** — chênh
3,4 lần trên tám lượt train là vài chục đô.

Điều kiện thật **không phải là tên card**, mà là:

1. **Cỡ lô hiệu dụng = 16 ở MỌI lượt** (`per_device 4 × grad_accum 4`). Đây mới là thứ làm
   hỏng bảng ablation nếu khác nhau giữa các nhánh.
2. **Cùng một loại card cho cả tám lượt.** Không trộn A100 với L4 giữa chừng.
3. **`bf16: true`** — cả A100 lẫn L4 đều có bf16 thật, không lo.

L4 có **24 GB** so với A100 40 GB, nên rủi ro thật là **tràn bộ nhớ** ở `per_device 4` với
`image_max_pixels 1003520`. Ô A.3 đo đúng chuyện đó. Tràn thì hai đường: hạ
`image_max_pixels` xuống 602112 **trước lượt đầu tiên rồi giữ nguyên mãi**, hoặc dùng A100.
Không có đường đổi giữa chừng.

Rồi cài gói (ô 0.3) → **Restart session** → chạy lại ô A.1.

### Ô A.1b — KIỂM GÓI MÃ VỪA BUNG (thêm 11/8) ⚠️ chạy ngay sau A.1

```python
import os
s = open(f"{REPO}/harness/infer_branch.py", encoding="utf-8").read()
r = open(f"{REPO}/harness/score_run.py", encoding="utf-8").read()
print("infer  :", len(s.encode()), "B · nối tiếp", "Nối tiếp" in s, "  ← chờ 27.443 / True")
print("score  :", len(r.encode()), "B · nối tiếp", "Nối tiếp" in r, "  ← chờ 34.610 / True")
print("chữ ký lượt chạy:", "là của lượt chạy KHÁC" in s, "  ← phải True (bản vá 12/8)")
T = f"{REPO}/harness/dg1_cache/test_ac"
print("test.jsonl   :", sum(1 for _ in open(f"{T}/test.jsonl", encoding="utf-8")), " ← 6.958")
print("descriptors  :", sum(1 for _ in open(f"{T}/descriptors.jsonl", encoding="utf-8")), " ← 4.448")
print("branches     :", sorted(os.listdir(f"{REPO}/harness/dg1_cache/train_ac/branches")))
```

⚠️ **Số kỳ vọng đã đổi 15/8** (bản trước ghi 26.062 / 31.277). Gói zip được đóng lại ngày
15/8 với các bản vá 12/8: `infer_branch.py` thêm **chữ ký lượt chạy** và dời khối nối tiếp lên
**trước** lúc nạp mô hình; `score_run.py` thêm lá chắn "tệp thô không khớp tệp dự đoán" và
cảnh báo tệp dự đoán thiếu. **Luật chấm KHÔNG đổi** — `metric_exec.py` không sửa dòng nào, nên
mọi nhánh đã chấm vẫn so được với nhau. Thấy 26.062 nghĩa là gói trên Drive vẫn là bản cũ.

Hai dòng đầu bắt chuyện **gói cũ trên Drive**: ngày 11/8 gói trên Drive có `cutoff_len 2560`
nhưng `infer_branch.py` mới 24.423 B và `score_run.py` 28.023 B — tức bản **trước** khi vá
nối tiếp (mục 4f của `report/110`). Train vẫn chạy được vì LLaMA-Factory không đụng hai tệp
đó, nên lỗi này **không lộ ra cho tới tận ô A.6** — lúc đó đứt máy giữa lượt sinh câu 1,5 giờ
hoặc lượt chấm 5 giờ là mất trắng. Cỡ tệp là cách rẻ nhất để phân biệt hai bản.

Ba dòng sau vì gói `rented` **có chứa** `test.jsonl` / `ocr.jsonl` / `descriptors.jsonl` của
tập kiểm, nên bung đè lên bản vừa lấy từ `derived.tar.gz`. Hai bản lẽ ra giống nhau — nhưng
đúng loại "lẽ ra" đã sai một lần hôm 7/8 (dựng lại ra 6.969 thay vì 6.958). `branches/` thì
zip không đụng tới, dòng cuối chỉ để chắc nó còn nguyên 6 tệp.

### Ô A.1c — SAO LƯU ĐIỂM LƯU TRƯỚC KHI CHẠY TIẾP ⚠️ chỉ khi đang nối tiếp một lượt dở

```python
from google.colab import userdata
import os, shutil, json
os.environ["HF_TOKEN"] = userdata.get("HF_TOKEN"); print("token HF: có")

CK = f"{D}/ckpt/s1_seed101"                      # đổi theo nhánh/hạt giống đang chạy
cks = sorted([d for d in os.listdir(CK) if d.startswith("checkpoint-")],
             key=lambda s: int(s.split("-")[1])) if os.path.isdir(CK) else []
print("checkpoint đang có:", cks)
if cks:
    BK = f"{D}/ckpt_backup/{os.path.basename(CK)}_{cks[-1]}"
    if not os.path.isdir(BK):
        os.makedirs(f"{D}/ckpt_backup", exist_ok=True)
        shutil.copytree(f"{CK}/{cks[-1]}", BK)
    print("đã sao lưu →", BK, "·", len(os.listdir(BK)), "tệp")

# ── CHỐT MỐC CHO Ô A.5, phải làm Ở ĐÂY vì sau khi phóng A.4 là không đọc được nữa ──
TL = f"{CK}/trainer_log.jsonl"
moc = 0
if os.path.exists(TL):
    rows = [json.loads(l) for l in open(TL, encoding="utf-8") if l.strip()]
    if rows:
        moc = rows[-1].get("current_steps", 0)
open("/content/MOC.txt", "w").write(str(moc))
print(f"MOC = {moc}  (bước ở DÒNG LOG CUỐI — không phải số của điểm lưu {cks[-1] if cks else '-'})")
```

**Vì sao bắt buộc.** Có một kịch bản mất nhiều giờ mà không ô nào khác chặn: nếu vì lý do gì
đó LLaMA-Factory **không** nhận ra điểm lưu và bắt đầu lại từ bước 0, thì `save_total_limit: 2`
sẽ **lặng lẽ xoá** hai điểm lưu cũ ngay khi bản mới thứ ba ra đời. Lúc phát hiện thì không
còn đường về. Sao 182 MB mất 1-2 phút — rẻ hơn 5 giờ train.

Xoá bản sao lưu sau khi ô A.4b xác nhận `current_steps` đã đi tiếp đúng chỗ.

⚠️ **Khối `MOC` ở cuối ô là bản vá 16/8 — đừng bỏ.** Log ghi mỗi **20 bước** còn điểm lưu mỗi
**200 bước**, nên dòng log cuối luôn chạy TRƯỚC điểm lưu tới 180 bước. Lấy `MOC` theo số của
điểm lưu là đặt hụt, và ô A.5 sẽ in lại dòng cũ y như thật suốt cả quãng mã hoá token.
Đã vấp đúng thế lần 16/8: điểm lưu `checkpoint-4800` nhưng phiên chết ở bước **4.880**, đặt
`MOC = 4800` nên ô theo dõi in `4.880` ba lần liền trong khi chưa có bước mới nào — rồi
"lùi" xuống 4.820 lúc phiên mới thật sự ghi dòng đầu tiên.

Phải chốt ở ô này chứ không phải lúc chạy A.5: sau khi A.4 phóng thì log đã trộn dòng mới
với dòng cũ, không còn cách nào tách ra.

### Ô A.1d — GẮN LẠI NHÃN `app_seen_in_train` (vài giây, chạy mỗi phiên có bung dữ liệu)

```python
!cd {REPO} && python harness/tag_app_seen.py
!cp {REPO}/harness/dg1_cache/test_ac/test.jsonl {D}/test_jsonl_tagged.jsonl
```

Nhãn này là **hàm của tập dạy thật sự dùng**, nên chỗ đúng để tính là ở đây — nơi có
`train.jsonl` đủ 64.567 bước. Chạy hết vài giây, không cần card.

⚠️ **Hai chỗ dễ hụt.** (1) `derived.tar.gz` trên Drive giữ bản `test.jsonl` CŨ, nên bung lại
ở phiên sau là nhãn quay về bản cũ — vì vậy ô này chạy lại mỗi phiên, và bản đã gắn nhãn
được chép riêng ra Drive. (2) Khâu chấm chạy trên **Kaggle**, đọc `app_seen_in_train` thẳng
từ `test.jsonl` (`score_run.py:405`) — phải mang bản đã gắn nhãn sang, không thì lát cắt phụ
đọc theo nhãn sai mà không có gì báo.

Chỉ đụng lát cắt phụ "ứng dụng đã thấy / chưa thấy lúc dạy", **không** đụng phép so chính
S1-vs-S2. Bản vá 12/8 của `tag_app_seen.py` và lý do đằng sau: xem docstring của tệp đó.

### Ô A.2 — sinh cấu hình

```python
import yaml, os
BRANCH, SEED = "s1", 101        # ⚠️ ĐỔI ĐÚNG HAI GIÁ TRỊ NÀY, không đụng gì khác
OUT = f"{D}/ckpt/{BRANCH}_seed{SEED}"      # ← trên DRIVE, không phải /content
os.makedirs(OUT, exist_ok=True)
c = yaml.safe_load(open(f"{REPO}/harness/train_config.yaml", encoding="utf-8"))
c.update({"dataset": f"gui_{BRANCH}", "seed": SEED, "output_dir": OUT,
          "dataset_dir": f"{REPO}/harness/dg1_cache/train_ac/branches"})
c["enable_liger_kernel"] = True             # P9 — chốt 11/8, xem mốc dừng 4
LOG = f"/content/train_{BRANCH}_seed{SEED}.log"   # tên theo nhánh: lượt khác nhau không lẫn log
for k in ("disable_gradient_checkpointing", "gradient_checkpointing", "max_steps", "max_samples"):
    c.pop(k, None)                          # quét sạch khoá còn sót của các lượt thăm dò
yaml.safe_dump(c, open("/content/cfg.yaml","w",encoding="utf-8"), allow_unicode=True, sort_keys=False)
eff = c["per_device_train_batch_size"] * c["gradient_accumulation_steps"]
print(f"nhánh {BRANCH} · hạt giống {SEED} · cỡ lô hiệu dụng {eff}  ← phải là 16 ở MỌI lượt")
print(f"bf16 {c['bf16']} · epoch {c['num_train_epochs']} · lưu điểm mỗi {c['save_steps']} bước")
print(f"liger {c.get('enable_liger_kernel')} · quantization_bit {c.get('quantization_bit')} ← True / 4")
print(f"khoá thăm dò còn sót: {[k for k in ('max_steps','max_samples','disable_gradient_checkpointing') if k in c]}  ← phải []")
print(f"output_dir {c['output_dir']}")
print(f"log       {LOG}")
print(f"BÊN TRONG output_dir: {os.listdir(OUT)}   ← phải là [] ở lượt chạy MỚI")
```

⚠️ **Dòng cuối — `BÊN TRONG output_dir` — bắt một lỗi im lặng:** LLaMA-Factory **tự dò điểm
lưu trong `output_dir`** (cơ chế cố ý bật bằng cách bỏ trống `resume_from_checkpoint`). Nếu
thư mục đó còn sót checkpoint của lần chạy trước, lượt mới sẽ **chạy tiếp từ nó** thay vì
bắt đầu từ đầu — log vẫn trơn tru, chỉ có số bước và kết quả là của một lượt khác. Ở lượt
chạy MỚI phải là `[]`; ở lượt chạy TIẾP sau khi đứt phiên thì có `checkpoint-*` mới đúng.

Sót thì xoá cả thư mục rồi chạy lại ô A.2:
```python
import shutil; shutil.rmtree(OUT, ignore_errors=True)
```

### 🛑 Ô A.2b — KIỂM VÀNG: cfg lượt này có KHỚP lượt trước không (thêm 15/8)

⚠️ **Chạy sau A.2 và sau ô vá `preprocessing_num_workers`, TRƯỚC A.4.** Bắt buộc ở mọi lượt
từ lượt thứ hai trở đi.

```python
import yaml
moi = yaml.safe_load(open("/content/cfg.yaml", encoding="utf-8"))
cu  = yaml.safe_load(open(f"{D}/logs/s1_seed101/cfg.yaml", encoding="utf-8"))   # ← lượt tham chiếu
ks = sorted(set(moi) | set(cu))
khac = [(k, cu.get(k), moi.get(k)) for k in ks if cu.get(k) != moi.get(k)]
print(f"khoá: tham chiếu {len(cu)} · lượt này {len(moi)}")
print("KHÁC NHAU:")
for k, a, b in khac: print(f"  {k}: {a}  →  {b}")
cho_phep = {"seed", "output_dir", "dataset", "preprocessing_num_workers"}
print("\n✅ ĐÚNG" if {t[0] for t in khac} <= cho_phep
      else "\n⛔ DỪNG — có khoá ngoài danh sách cho phép bị đổi")
```

**Chỉ bốn khoá được phép khác:** `seed` (đổi hạt giống) · `output_dir` (theo nhánh+hạt giống) ·
`dataset` (khi đổi sang nhánh s2/s2r/s2_nopoint) · `preprocessing_num_workers` (chỉ đổi số
tiến trình mã hoá token, không đổi dữ liệu ra). **Khoá thứ năm xuất hiện là dừng hẳn.**

Vì sao cần: cặp hạt giống chỉ làm được **null thực nghiệm** khi mọi thứ trừ hạt giống đều y
hệt, và bảng ablation chỉ đọc được khi các nhánh chỉ khác nhau ở đích sinh. Một khoá lệch
(cỡ lô, `cutoff_len`, `bf16`, liger) là hỏng phép so mà **log vẫn chạy trơn tru**. Lượt
s1/202 ngày 15/8 kiểm ra **38/38 khoá, chỉ khác `seed` và `output_dir`** — đó là bằng chứng
bằng số, thay cho việc tin vào trí nhớ.

Kèm theo, ô kiểm dữ liệu (vài giây):

```python
import hashlib, os, json
p = f"{REPO}/harness/dg1_cache/train_ac/branches/s1.json"     # đổi tên tệp theo nhánh
print("md5", hashlib.md5(open(p,"rb").read()).hexdigest())
print("số mẫu:", len(json.load(open(p, encoding="utf-8"))), "← 64.567")
```

`s1.json` md5 = **641953d75d61ab192b94a559362cce9b** · 64.567 mẫu (ghi 15/8).

### Ô A.3 — THĂM DÒ 20 BƯỚC trước khi cam kết 15 giờ

⛔ **11/8: BỎ QUA A.3 → A.3i ở các lượt sau.** Đã đo xong trên cả L4 lẫn A100, số nằm ở mục
"📊 SỐ ĐÃ ĐO 11/8" dưới mốc dừng 4. Chạy lại là trả tiền cho thứ đã biết. Chỉ đo lại khi
**đổi card, đổi mô hình gốc, hoặc đổi siêu tham số**.

```python
import yaml
p = yaml.safe_load(open("/content/cfg.yaml", encoding="utf-8"))
# max_samples cắt bớt dữ liệu CHỈ cho lượt thăm dò: không có nó thì ô này vẫn phải mã hoá
# token cho đủ 64.567 mẫu (~25 phút) trước khi chạy 20 bước — trả tiền card để ngồi chờ.
# Không ảnh hưởng phép đo: giây-mỗi-bước và bộ nhớ đỉnh không phụ thuộc số mẫu, mà độ dài
# chuỗi thì rất đều (p99 1.675, dài nhất 2.017 — đo 11/8) nên lô nào cũng gần như nhau.
p.update({"max_steps": 20, "max_samples": 2000, "output_dir": "/content/probe",
          "save_steps": 10000, "logging_steps": 5})
yaml.safe_dump(p, open("/content/probe.yaml","w",encoding="utf-8"), allow_unicode=True, sort_keys=False)
```
```python
!llamafactory-cli train /content/probe.yaml > /content/probe.log 2>&1; tail -25 /content/probe.log
```
```python
import re
L = open("/content/probe.log", encoding="utf-8", errors="ignore").read()
tp = re.search(r"Number of trainable parameters = ([\d,]+)", L)
bs = re.search(r"Total train batch size[^=]*= (\d+)", L)
sp = re.findall(r"([\d.]+)s/it", L) or re.findall(r"([\d.]+)it/s", L)
oom = "out of memory" in L.lower()
print("tham số huấn luyện :", tp.group(1) if tp else "KHÔNG THẤY", " ← chờ 14,966,784")
print("cỡ lô hiệu dụng    :", bs.group(1) if bs else "KHÔNG THẤY", " ← chờ 16")
print("tốc độ             :", sp[-3:] if sp else "?")
print("tràn bộ nhớ        :", "CÓ ← dừng, báo mình" if oom else "không")
```

Ô này trả lời ba câu **trước** khi đồng hồ chạy 15 tiếng:

- có tràn bộ nhớ ở cỡ lô này không
- **bao nhiêu giây mỗi bước** → nhân với tổng số bước ra thời gian thật, ra số đơn vị thật
- số tham số huấn luyện có đúng **14.966.784** không (nếu khác: LoRA gắn sai chỗ, hoặc
  tháp thị giác không được đóng băng)

### Ô A.3b — ĐO BA BIẾN THỂ TĂNG TỐC (thêm 11/8 sau khi A.3 ra 31,26 s/bước)

Vì sao có ô này: A.3 trên L4 đo được **31,26 s/bước** ⇒ 8.071 bước = **69,5 giờ MỘT lượt**,
tám lượt = **556 giờ ≈ 23 ngày máy chạy liên tục**. Tiền thì chịu được (~$86), nhưng thời
gian tường thì không, khi hạn nộp còn 7 tuần và còn phải chấm điểm + viết. Bóc từ log:
`total_flos 9.527.912 GF` / 20 bước = 4,76·10¹⁴ FLOP mỗi bước ⇒ **15,2 TFLOPS hiệu dụng =
12,6% công suất bf16 của L4** — còn dư địa lớn, và cấu hình đang đánh đổi tốc độ ở hai chỗ
mà **chưa cần** đánh đổi.

```python
!pip install -q liger-kernel     # không cần restart: llamafactory chạy ở tiến trình con
```
```python
import yaml, re, os, time
BASE = yaml.safe_load(open("/content/cfg.yaml", encoding="utf-8"))
BT = [
  ("P1 tắt grad-checkpoint",   {"gradient_checkpointing": False}),
  ("P2 = P1 + bỏ 4-bit",       {"gradient_checkpointing": False, "_bo": ["quantization_bit", "quantization_method"]}),
  ("P3 = P2 + liger",          {"gradient_checkpointing": False, "_bo": ["quantization_bit", "quantization_method"],
                                "enable_liger_kernel": True}),
]
print("P0 gốc (4-bit + ckpt)      31.26 s/bước ·   69.5 giờ/lượt ·  107 đv/lượt ·  856 đv cho 8 lượt")
print("biến thể                   s/bước    giờ/lượt   đv/lượt   8 lượt: giờ / đv     lúc")
for ten, sua in BT:
    c = dict(BASE); c.update({k: v for k, v in sua.items() if k != "_bo"})
    for k in sua.get("_bo", []): c.pop(k, None)
    c.update({"max_steps": 12, "max_samples": 1000, "output_dir": "/content/probe",
              "save_steps": 10000, "logging_steps": 4})
    yaml.safe_dump(c, open("/content/p.yaml", "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)
    os.system("rm -rf /content/probe")
    os.system("llamafactory-cli train /content/p.yaml > /content/p.log 2>&1")
    L = open("/content/p.log", encoding="utf-8", errors="ignore").read()
    sp = re.findall(r"([\d.]+)s/it", L); it = re.findall(r"([\d.]+)it/s", L)
    if "out of memory" in L.lower():
        print(f"{ten:26} TRÀN BỘ NHỚ — giữ biến thể trước đó   ({time.strftime('%H:%M:%S')})", flush=True); continue
    if not (sp or it):
        print(f"{ten:26} KHÔNG CHẠY: {L.strip().splitlines()[-1][:70]}   ({time.strftime('%H:%M:%S')})", flush=True); continue
    s = float(sp[-1]) if sp else 1/float(it[-1]); g = 8071*s/3600
    print(f"{ten:26} {s:6.2f}   {g:8.1f}   {g*1.54:7.0f}   {g*8:8.0f} / {g*8*1.54:6.0f}   ({time.strftime('%H:%M:%S')})", flush=True)
```

~20 phút · ~0,6 đơn vị. Ba biến thể đo đúng ba chỗ:

| khoá | đang là | vì sao đổi |
|---|---|---|
| `gradient_checkpointing` | `true` | tính lại activation ở lượt lùi để tiết kiệm VRAM — thường **chậm 30-40%**, mà VRAM đang không thiếu (A.3 không OOM) |
| `quantization_bit` | `4` (bnb NF4) | mỗi phép nhân phải giải nén trọng số; trên card băng thông thấp đây thường là chỗ mất nhiều nhất |
| `enable_liger_kernel` | không có | kernel hợp nhất, **cùng công thức**, thường nhanh thêm 10-20% |

**Hai đòn đầu và đòn cuối không đổi thứ mô hình học** — tắt tính-lại-activation là thuần
trao đổi VRAM lấy tốc độ; liger là kernel hợp nhất. Chỉ **bỏ 4-bit là đổi thiết kế**: trọng
số chạy bf16 đầy đủ thay vì NF4 nén, tức đổi theo hướng *chính xác hơn*. Đổi được vì đổi
**trước lượt đầu tiên và cho cả tám lượt**; `report/106` chỉ khoá "mọi nhánh cùng siêu tham
số", không khoá riêng 4-bit. Nếu chọn thì **phải ghi vào mục sửa đổi của report/106**.

⚠️ Kết quả ba biến thể này **chuyển giao được sang A100** — cả ba đòn đều có lợi trên mọi
card. Nên đo trên card đang ngồi (rẻ hơn 3,4 lần) rồi mới đổi runtime, đừng đổi trước.

### Ô A.3d — TÁCH BIẾN (bài học: đừng ghép hai thay đổi vào một biến thể)

**Lỗi của bản A.3b:** biến thể "P2" ghép *hai* thay đổi cùng lúc — bỏ 4-bit **và** tắt
checkpointing. Mô hình phình 1,9 → 6,2 GB *đồng thời* activations phình mấy lần, nên nó
tràn bộ nhớ trước khi kịp trả lời câu nào. Cái đáng đo nhất (**bf16 mà vẫn giữ
checkpointing**) thì không được đo. Mỗi biến thể chỉ đổi MỘT thứ so với đường cơ sở.

Danh sách biến thể tuỳ card — dưới đây là bản cho A100 40 GB (L4 đã loại hết, xem bảng ở
mốc dừng 4):

```python
import yaml, re, os, time
BASE = yaml.safe_load(open("/content/cfg.yaml", encoding="utf-8"))
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
GIA = 5.3            # đơn vị/giờ của card đang chạy: A100 5,3 · L4 1,54
BO  = ["quantization_bit", "quantization_method"]
TAT = {"disable_gradient_checkpointing": True, "gradient_checkpointing": False}
BT = [
  ("P4 bf16, giữ ckpt, 4×4",  {"_bo": BO}),
  ("P5 = P4 + liger",         {"_bo": BO, "enable_liger_kernel": True}),
  ("P7 bf16, tắt ckpt, 4×4",  {"_bo": BO, **TAT}),
  ("P8 = P7 nhưng 8×2",       {"_bo": BO, **TAT,
                               "per_device_train_batch_size": 8, "gradient_accumulation_steps": 2}),
]
print("biến thể                   s/bước    giờ/lượt   đv/lượt   8 lượt: giờ / đv     lúc")
for ten, sua in BT:
    c = dict(BASE); c.update({k: v for k, v in sua.items() if k != "_bo"})
    for k in sua.get("_bo", []): c.pop(k, None)
    c.update({"max_steps": 12, "max_samples": 1000, "output_dir": "/content/probe",
              "save_steps": 10000, "logging_steps": 4})
    yaml.safe_dump(c, open("/content/p.yaml", "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)
    os.system("rm -rf /content/probe")
    os.system("llamafactory-cli train /content/p.yaml > /content/p.log 2>&1")
    os.system(f"cp /content/p.log /content/log_{ten.split()[0]}.log")   # sao SAU khi chạy, khỏi lệch nhịp
    L = open("/content/p.log", encoding="utf-8", errors="ignore").read()
    sp = re.findall(r"([\d.]+)s/it", L); it = re.findall(r"([\d.]+)it/s", L)
    if "outofmemory" in L.lower().replace(" ", ""):
        print(f"{ten:26} TRÀN BỘ NHỚ   ({time.strftime('%H:%M:%S')})", flush=True); continue
    if not (sp or it):
        print(f"{ten:26} KHÔNG CHẠY: {L.strip().splitlines()[-1][:70]}   ({time.strftime('%H:%M:%S')})", flush=True); continue
    s = float(sp[-1]) if sp else 1/float(it[-1]); g = 8071*s/3600
    print(f"{ten:26} {s:6.2f}   {g:8.1f}   {g*GIA:7.0f}   {g*8:8.0f} / {g*8*GIA:6.0f}   ({time.strftime('%H:%M:%S')})", flush=True)
```

### Ô A.3e — đọc log khi một biến thể TRÀN BỘ NHỚ

Phân biệt **chật chỗ** với **sai cấu hình** — nếu là sai cấu hình thì đổi card cũng dính.

```python
for ten in ("P4", "P5", "P7", "P8"):
    f = f"/content/log_{ten}.log"
    if not os.path.exists(f): continue
    L = open(f, encoding="utf-8", errors="ignore").read()
    oom = [l for l in L.splitlines() if "OutOfMemory" in l]
    ck  = [l for l in L.splitlines() if "heckpointing" in l][:1]
    print(f"=== {ten} ===")
    print("  OOM :", (oom[-1][:150] if oom else "không có"))
    print("  ckpt:", ck or "(không bật)")
    print("  chết:", [l.strip()[:90] for l in L.splitlines() if "line " in l and ".py" in l][-1:])
```

Ba thứ phải đọc: `total capacity … of which … is free` (còn vài chục MB ⇒ chật chỗ thật) ·
có dòng `Gradient checkpointing enabled` không (biết khoá có ăn không) · `dtype` là gì.
Ngày 11/8 chính ô này lật được hai suy đoán sai: dtype tưởng fp32 thật ra `bfloat16`, và
khoá tưởng bị ghi đè thật ra **có** tác dụng (activations phình lên 21,5 GB chứng minh).

## 🛑 MỐC DỪNG 4 — dán output ô A.2 và A.3

Mình tính giúp: tổng số bước = `64.567 × 2 epoch ÷ 16` = **8.071 bước**, nhân với
giây-mỗi-bước ra giờ, rồi nhân **1,54 (L4)** hoặc **5,3 (A100)** ra đơn vị — hai số này đo
được ngày 11/8. ⛔ Đừng dùng 6,77 của bản kế hoạch cũ, số đó chưa đúng với máy nào.

Nhân tiếp cho **tám lượt** (4 nhánh × 2 hạt giống) ra tổng chiến dịch. Nhiều hơn số đơn vị
đang có thì phải quyết **trước** — mua thêm, hay hạ xuống 1 epoch (và ghi vào mục sửa đổi
của report/106) — chứ không phải phát hiện lúc đang chạy dở giờ thứ mười.

Ở mốc này cũng chốt luôn **dùng L4 hay A100 cho cả tám lượt**: so giây-mỗi-bước đo được
trên hai card. L4 chậm hơn **dưới 3,4 lần** thì L4 rẻ hơn. Nhưng còn phải cân số phiên: một
lượt 30 giờ trên L4 là 3 phiên, mỗi lần đứt là một lần rủi ro — trong khi 11 giờ trên A100
có thể gọn trong một hai phiên.

Cũng là chỗ mình xác nhận cỡ lô hiệu dụng bằng 16 và số tham số bằng 14.966.784.

### 📊 SỐ ĐÃ ĐO 11/8/2026 — dùng làm chuẩn, đừng đo lại từ đầu

Cả hai card: tham số **14.966.784** ✅ · cỡ lô hiệu dụng **16** ✅ · `total_flos` **9.527.912
GF**/20 bước ở CẢ HAI ⇒ 4,76·10¹⁴ FLOP mỗi bước.

| cấu hình | L4 (22 GB dùng được) | A100-SXM4-40GB |
|---|---|---|
| **P0 gốc: 4-bit + gradient checkpointing, 4×4** | **31,26 s/bước** | **10,70 s/bước** ⬅ tốt nhất |
| P1 4-bit, **tắt** checkpointing | 31,37 (**không giúp**) | chưa đo |
| P4 bf16, giữ checkpointing, 4×4 | TRÀN | **TRÀN** |
| P5 = P4 + liger | TRÀN | **14,76** (chạy được, nhưng **chậm hơn P0**) |
| P6 bf16, tắt ckpt, 2×8 | TRÀN | — |
| P7 bf16, tắt ckpt, 4×4 | — | **TRÀN** |
| P8 bf16, tắt ckpt, 8×2 | — | **TRÀN** |
| P9 = P0 + liger | — | **10,38** (nhanh hơn P0 3%) |
| **P10 = P9, tắt checkpointing** | — | **9,03** ⬅ **NHANH NHẤT, chọn cái này** |
| hiệu suất ở P0 | 15,2 TFLOPS = **12,6%** đỉnh bf16 | 44,5 TFLOPS = **14,3%** đỉnh |

**⭐ CẤU HÌNH CHẠY CHÍNH THỨC = P9** — giữ nguyên `quantization_bit: 4`, cỡ lô `4×4` và
gradient checkpointing của `train_config.yaml`, **chỉ thêm MỘT khoá**:

```yaml
enable_liger_kernel: true
```

| | s/bước | 1 lượt | 2 lượt S1 | 8 lượt |
|---|---|---|---|---|
| P0 gốc | 10,70 | 24,0 giờ · 127 đv | 48 giờ · 254 đv | 192 giờ · 1.017 đv |
| **P9 ⬅ chọn** | **10,38** | **23,3 giờ · 123 đv** | **46,6 giờ · 246 đv ≈ $25** | 186 giờ · 987 đv |
| ~~P10 (tắt ckpt)~~ | ~~9,03~~ | ⛔ **LOẠI — tràn bộ nhớ ở chuỗi dài** | | |

⛔ **P10/P11 (tắt gradient checkpointing) ĐÃ BỊ LOẠI — đừng thử lại.** Chúng chạy 9,03
s/bước trên mẫu thường nhưng **tràn bộ nhớ trên 200 mẫu dài nhất của s2** (ô A.3g). Loại
hỏng tệ nhất có thể có: chạy trơn vài giờ rồi chết lúc vô tình gặp một lô mẫu dài, giữa đêm.
Bỏ liger cũng không cứu được (P11 cũng tràn).

✅ **Liger đã được chứng minh KHÔNG đổi phép tính** — chạy P0 và P9 trên **cùng 200 mẫu, cùng
`seed 101`, cùng thứ tự**, loss trùng tới chữ số thứ tư:

| mốc | P0 | P9 + liger |
|---|---|---|
| 1 | 3.189 | 3.188 |
| 2 | 3.014 | 3.015 |
| 3 | 2.597 | 2.595 |
| 4 | 2.545 | 2.545 |

Đây là **bằng chứng đo được**, không phải lời hứa của thư viện. ⇒ `quantization_bit: 4` và
mọi siêu tham số giữ nguyên ⇒ **không phải ghi mục sửa đổi `report/106`.**

⚠️ **Bài học phương pháp:** probe chạy trên mẫu đầu tập KHÔNG đủ để kết luận về bộ nhớ.
Chuỗi dài nhất 2.017 token so với trung vị 1.524; mẫu thường không chạm tới đỉnh. **Mọi cấu
hình đụng tới bộ nhớ đều phải thử lại trên nhánh nặng nhất (s2) với các mẫu dài nhất.** Ô
A.3g dựng `s2_long.json` (200 mẫu dài nhất) + khoá `gui_s2_long` trong `dataset_info.json`
cho đúng việc đó — hai thứ này để lại trong `branches/`, vô hại vì `cfg.yaml` trỏ `gui_s1`,
nhưng **nhớ khi đếm tệp trong `branches/` sẽ thấy 7 thay vì 6.**

⛔ **Hai kết luận ngược trực giác, đã đo, đừng thử lại:**

**1. QLoRA 4-bit NHANH HƠN bf16** trên chính máy này (10,70 vs 14,76 s/bước), chứ không
chậm hơn như vẫn tưởng. Mô hình 3B nhỏ nên khâu giải nén trọng số không phải nút thắt; đổi
lại 4-bit trả về ~4,3 GB cho activations, mà chỗ nghẽn thật nằm ở activations. ⇒ **cấu hình
đăng ký trước (`report/106`) giữ nguyên, KHÔNG cần ghi mục sửa đổi.**

**2. Chỗ ngốn bộ nhớ là BẢNG LOGITS, không phải trọng số.** Bằng chứng: P4 tràn, mà P5 =
chính P4 cộng liger thì chạy được. Liger gộp bước cross-entropy nên không phải dựng bảng
`151.936 từ vựng × ~1.500 token × 4 mẫu` nâng lên fp32 (≈3,6 GB, cộng bản sao lúc tính đạo
hàm). Đây cũng là lý do L4 chết ở **mọi** biến thể bf16 — không phải vì 6,2 GB trọng số.

| | L4 | A100 |
|---|---|---|
| 1 lượt (8.071 bước) | 69,5 giờ · 107 đv | **24,0 giờ · 127 đv** |
| 2 lượt S1 (×2 hạt giống) | 139 giờ = 5,8 ngày · 214 đv ≈ $21 | **48 giờ = 2 ngày · 254 đv ≈ $25** |
| 8 lượt | 556 giờ = 23 ngày · 856 đv ≈ $86 | 192 giờ = 8 ngày · 1.017 đv ≈ $102 |

**A100 nhanh hơn 2,92× nhưng giá gấp 3,44× ⇒ đắt hơn 19% về tiền, rẻ hơn 3 lần về thời
gian.** Với hạn nộp còn ~7 tuần, thời gian tường mới là ràng buộc ⇒ **chọn A100**.

⚠️ **L4 kịch trần: 22 GB không đủ cho bf16**, kể cả khi giữ checkpointing hoặc hạ
`per_device` xuống 2. OOM xảy ra ở forward đầu tiên với **21,54 / 22,03 GB** đã cấp — chật
chỗ thuần tuý, không phải sai cấu hình (log in `Gradient checkpointing enabled` và dtype
`bfloat16`). Nghĩa là P0 vốn đã chạy sát mép; bỏ 4-bit thêm ~4,3 GB là qua mép.

✅ **Bằng chứng đổi card không đổi kết quả:** cùng `seed 101`, loss 20 bước trùng nhau tới
ba chữ số — L4 `2,036 / 0,9686 / 0,8635 / 0,9553`, A100 `2,040 / 0,9679 / 0,8635 / 0,9547`,
`total_flos` y hệt. Dùng được cho câu "kết quả tái lập được khi đổi máy" trong luận văn,
cùng loại lập luận với phép kiểm chéo máy của bộ đọc chữ (ô 0.9b).

**Không phải cam kết 8 lượt ở mốc này.** Trình tự đã khoá: S1 × 2 hạt giống → chấm đủ →
**MDE thật** → khoá ngưỡng → *rồi mới* train S2. Nên chỉ cần đủ đơn vị cho 2 lượt đầu.

---

### Ô A.3i — THỬ GHI DRIVE + NỐI TIẾP, THU NHỎ (thêm 11/8) ⚠️ chạy trước A.4

Vì sao không đợi A.5b: A.5b chỉ thử được sau khi có `checkpoint-200`, tức **chờ 1 tiếng**.
Ô này làm cùng chuyện trong **8 phút** bằng một lượt 10 bước, và thử thêm được thứ A.5b
không đụng tới — **ghi điểm lưu lên Drive fuse**. Cho tới trước ô này, mọi lượt thăm dò đều
ghi vào `/content/probe`; ghi 180 MB qua Drive fuse là chuyện khác hẳn, và chính Drive fuse
đã làm chết một lệnh `tar` hôm 11/8 với thông báo lỗi trỏ sai chỗ.

```python
import yaml, os, re, shutil
T = f"{D}/ckpt/_test_resume"
shutil.rmtree(T, ignore_errors=True); os.makedirs(T, exist_ok=True)
c = yaml.safe_load(open("/content/cfg.yaml", encoding="utf-8"))
c.update({"output_dir": T, "max_steps": 10, "max_samples": 500,
          "save_steps": 5, "logging_steps": 5})
yaml.safe_dump(c, open("/content/t.yaml", "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
os.system("llamafactory-cli train /content/t.yaml > /content/t1.log 2>&1")
print("điểm lưu ghi được lên Drive:", sorted(os.listdir(T)))
for ck in sorted(d for d in os.listdir(T) if d.startswith("checkpoint-")):
    ff = sorted(os.listdir(f"{T}/{ck}"))
    tong = sum(os.path.getsize(f"{T}/{ck}/{x}") for x in ff) / 2**20
    print(f"  {ck}: {tong:6.1f} MB · có optimizer.pt:", "optimizer.pt" in ff,
          "· có trainer_state.json:", "trainer_state.json" in ff)
```
```python
c["max_steps"] = 20          # chạy tiếp: phải nhận ra checkpoint-10, KHÔNG bắt đầu lại từ 0
yaml.safe_dump(c, open("/content/t.yaml", "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)
os.system("llamafactory-cli train /content/t.yaml > /content/t2.log 2>&1")
L = open("/content/t2.log", encoding="utf-8", errors="ignore").read()
print("nhận ra điểm lưu :", any(k in L for k in ("Resuming", "resume", "Continuing training")))
print("dòng liên quan   :", [l.strip()[:110] for l in L.splitlines()
                             if any(k in l for k in ("Resuming","Continuing","skip the first"))][:3])
import json
st = json.load(open(f"{T}/trainer_state.json"))
print("bước cuối ghi trong trạng thái:", st["global_step"], " ← phải là 20, KHÔNG phải 10")
print("số mốc loss ghi lại:", len([x for x in st["log_history"] if "loss" in x]))
```

Xong thì dọn: `shutil.rmtree(f"{D}/ckpt/_test_resume", ignore_errors=True)`

**📊 Kết quả 11/8/2026 — đạt cả bốn:** điểm lưu ghi lên Drive **182,7 MB**/bản · **có
`optimizer.pt`** (nối tiếp khôi phục đúng trạng thái tối ưu hoá, không phải khởi động lại
từ đầu) · log in `Resuming training from /content/drive/MyDrive/...` · `global_step = 20`
chứ không quay về 10 · `trainer_state.json` giữ đủ lịch sử loss.

⇒ Cơ chế nối tiếp — thứ cả kế hoạch 8 lượt dựa vào, cố ý dựng bằng cách **bỏ trống**
`resume_from_checkpoint`, và **chưa từng chạy lần nào** — nay đã chạy thật.

**Dung lượng Drive cần cho điểm lưu:** 182,7 MB × 2 (`save_total_limit`) + bản `_ep1` + bản
cuối ở `output_dir` ≈ **0,73 GB mỗi lượt** ⇒ ~5,8 GB cho tám lượt.

### Ô A.4 — train, chạy NỀN

```python
import subprocess, os
!rm -rf /content/probe /content/probe.yaml /content/t.yaml
env = dict(os.environ, PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True")
f = open(LOG, "a")
p = subprocess.Popen(["llamafactory-cli", "train", "/content/cfg.yaml"],
                     cwd=REPO, stdout=f, stderr=subprocess.STDOUT,
                     env=env, start_new_session=True)
print("đã khởi động, PID", p.pid, "→", LOG)
```

⛔ **Đừng dùng `!cd {REPO} && … nohup … &`** (bản cũ). Sáng 12/8 nó **chạy tiền cảnh**: tiến
độ mã hoá token đổ thẳng ra ô, nhân Python bị chiếm suốt, nên **không chạy được ô A.5 lẫn ô
canh gác `_ep1`** — phải theo dõi bằng Terminal. `subprocess.Popen` với
`start_new_session=True` tách hẳn tiến trình khỏi nhân: ô trả về ngay, và tiến trình sống
sót cả khi nhân Python bị khởi động lại.

⚠️ **Hai chi tiết trong dòng lệnh, đều là lỗi đã sửa ngày 12/8:**

**`>>` chứ không phải `>`.** Phiên đứt rồi chạy lại ô này với `>` sẽ **ghi đè** log cũ, mà ô
A.4b lại đang đồng bộ tệp đó lên Drive — nên bản trên Drive cũng bị thay bằng bản cụt. Mất
đường cong mất mát của phần đã chạy, đúng thứ cần cho hình trong luận văn. Với `>>` thì mọi
lần chạy nối vào nhau, và dòng `Resuming training from …` nằm ngay trong đó làm mốc.

**Tên log mang theo nhánh và hạt giống** (`LOG` sinh ở ô A.2). Một tên `train.log` dùng chung
cho tám lượt thì nối thêm sẽ trộn lẫn các nhánh, còn ghi đè thì mất lượt trước — không có
cách nào đúng. Tách tên là hết chuyện.

`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` giảm phân mảnh bộ nhớ khi chạy liên tục
24 giờ; chính thông báo lỗi lúc thăm dò gợi ý đặt nó.

⏳ **Khoảng 2,5 GIỜ đầu KHÔNG có bước train nào** — LLaMA-Factory phải chuyển định dạng rồi
mã hoá token cho cả 64.567 mẫu trước khi vào bước 1. Log lúc đó chỉ có thanh
`Running tokenizer on dataset`, **không phải treo**.

⛔ **Con số "~25 phút" của bản cũ là SUY RA, và suy sai** (7,3 mẫu/giây trên 2 lõi × 12 lõi).
Đo thật trên A100 ngày 12/8: **7,11 mẫu/giây ⇒ 2 giờ 31 phút**, tức số lõi không giúp gì.
Lý do thấy ngay ở `ps`: tiến trình chỉ ăn **165% CPU trên 12 lõi** — `datasets.map` chạy MỘT
tiến trình vì `train_config.yaml` không khai `preprocessing_num_workers`. Đã loại ba nghi
ngờ khác bằng số đo cùng lúc: 12 lõi (bằng lượt trước), tải máy 1,93 (không ai tranh CPU),
64.567 ảnh nằm đúng `/content/ws/...` chứ không đọc qua Drive fuse.

⇒ **Hệ quả phải tính vào kế hoạch: mỗi lần đứt phiên tốn ~3 giờ dựng lại** (bung 33 GB ảnh
35 phút + mã hoá token 2,5 giờ), không phải ~1 giờ như bản cũ ghi. Phần train đã làm vẫn
không mất.

🔬 **Việc nên thử trước lượt s1 hạt giống 202** (chưa chạy tính tới 12/8): thêm
`preprocessing_num_workers: 8` vào ô A.2 rồi đo bằng một lượt thăm dò `max_samples`. Ăn thì
mỗi lượt bớt ~2 giờ, và mỗi lần đứt phiên cũng bớt ~2 giờ — với 7 lượt còn lại là cỡ 14 giờ
tường. Khoá này chỉ đổi cách chia việc lúc tiền xử lý, **không đổi dữ liệu ra**, nên không
phải ghi mục sửa đổi `report/106`. ⚠️ Nó chạy nhiều tiến trình cùng mở ảnh nên có thể ngốn
RAM — đo trên `max_samples` trước, đừng bật thẳng vào lượt 24 giờ.

Có thể tắt phần chờ này bằng `tokenized_path` để dùng lại bộ đã mã hoá giữa hai hạt giống
của cùng một nhánh (tiết kiệm ~1,7 giờ cho cả tám lượt). **Không dùng** — bộ nhớ đệm cũ mà
lệch với cấu hình mới thì nó vẫn chạy và vẫn ra số, chỉ là số của cấu hình cũ. Vừa đổi
`cutoff_len` 2048 → 2560 ngày 11/8, đúng loại thay đổi mà bộ đệm cũ sẽ nuốt mất. Đổi 1,7 giờ
lấy một rủi ro sai âm thầm là không đáng.

### Ô A.4b — CẤT LOG LÊN DRIVE + đồng bộ mỗi 5 phút ⚠️ chạy ngay sau A.4

Điểm lưu đã an toàn (`output_dir` trỏ thẳng Drive), nhưng **ba thứ khác vẫn treo trên
`/content`**: log của các lượt thăm dò (16 phép đo ngày 11/8 = **~5 đơn vị tiền card**),
`train.log` (đường cong mất mát — hình trong luận văn), và `cfg.yaml` (bằng chứng "sáu nhánh
chỉ khác ba dòng"). Ô A.10 chỉ cất ở **cuối phiên**, mà phiên có thể chết ở giờ thứ 20.

```python
import os, subprocess
os.makedirs(f"{D}/logs/probe_11_8", exist_ok=True)
os.system(f"cp /content/*.log /content/cfg.yaml /content/p.yaml {D}/logs/probe_11_8/ 2>/dev/null")
print("log thăm dò đã cất:", sorted(os.listdir(f"{D}/logs/probe_11_8")))

os.makedirs(f"{D}/branches_backup", exist_ok=True)      # hai tệp do ô A.3g sinh ra
B = f"{REPO}/harness/dg1_cache/train_ac/branches"
os.system(f"cp {B}/dataset_info.json {B}/s2_long.json {D}/branches_backup/ 2>/dev/null")

V = f"{D}/logs/{BRANCH}_seed{SEED}"; os.makedirs(V, exist_ok=True)
os.makedirs(f"{D}/preds", exist_ok=True)                # cần ở ô A.8, tạo sẵn cho chắc
sync = ('while true; do '
        f'cp {LOG} /content/cfg.yaml {V}/ 2>>/content/sync.err; '
        f'echo "$(date +%H:%M:%S)  log $(stat -c%s {LOG} 2>/dev/null) B"; '
        'sleep 300; done')
subprocess.Popen(["bash", "-c", sync], stdout=open("/content/synclog.log", "a"),
                 stderr=subprocess.STDOUT, start_new_session=True)
# canh gác bản cuối lượt duyệt 1: save_total_limit=2 sẽ xoá checkpoint-4000 sau ~70 phút.
# Điều kiện là có trainer_state.json (tệp ghi SAU CÙNG) nên không sao nhầm bản đang ghi dở.
watch = (f'CK={D}/ckpt/{BRANCH}_seed{SEED}; while true; do '
         'if [ -f $CK/checkpoint-4000/trainer_state.json ] && [ ! -d ${CK}_ep1 ]; then '
         'cp -r $CK/checkpoint-4000 ${CK}_ep1 && echo "$(date +%H:%M:%S) đã sao ep1"; fi; '
         'sleep 120; done')
subprocess.Popen(["bash", "-c", watch], stdout=open("/content/ep1watch.log", "a"),
                 stderr=subprocess.STDOUT, start_new_session=True)
print("đã bật đồng bộ log + canh gác ep1 →", V)
```

Sau **6 phút** kiểm nó chạy thật — đừng tin vào việc đã bấm:

```python
print(open("/content/synclog.log").read()[-400:])
import os
print("lỗi chép:", open("/content/sync.err").read()[-300:] if os.path.exists("/content/sync.err") else "(không có)")
print("trên Drive:", os.listdir(f"{D}/logs/{BRANCH}_seed{SEED}"))
```

⚠️ Bản đồng bộ của phiên 0 lúc đầu nuốt lỗi bằng `2>/dev/null` — Drive trục trặc thì nó im
lặng không chép gì và chỉ lộ ra đúng lúc mất máy. Ở đây lỗi được giữ trong `sync.err`.

**May mà không phải thiết kế:** mỗi checkpoint có `trainer_state.json` chứa trọn lịch sử
loss, nên kể cả mất `train.log` vẫn dựng lại được đường cong tới điểm lưu gần nhất.

### Ô A.5 — theo dõi (chạy lại nhiều lần)

```python
import subprocess, os, time, json
CK  = f"{D}/ckpt/{BRANCH}_seed{SEED}"
TL  = f"{CK}/trainer_log.jsonl"     # LLaMA-Factory tự ghi, NẰM TRÊN DRIVE
MOC = int(open("/content/MOC.txt").read()) if os.path.exists("/content/MOC.txt") else 0
                                    # ↑ ô A.1c chốt sẵn = bước ở DÒNG LOG CUỐI của phiên trước.
                                    #   Đặt tay thì cũng phải lấy số đó, KHÔNG lấy số điểm lưu.
NHIP = 60                           # 60 giây lúc đang canh; đổi 300 khi đã yên tâm
print(f"theo dõi {BRANCH} hạt giống {SEED} · nguồn: {TL} · chỉ đếm bước > {MOC}")
print("giờ        bước           %      loss      đã chạy      còn lại     điểm lưu")
while True:
    song = "llamafactory" in subprocess.run(["ps","-eo","args"],capture_output=True,text=True).stdout
    try:
        rows = [json.loads(l) for l in open(TL, encoding="utf-8", errors="ignore") if l.strip()]
    except Exception:
        rows = []
    moi = [r for r in rows if r.get("current_steps", 0) > MOC]
    ck  = sorted([d for d in os.listdir(CK) if d.startswith("checkpoint-")],
                 key=lambda s: int(s.split("-")[1])) if os.path.isdir(CK) else []
    if moi:
        r = moi[-1]
        print(f"{time.strftime('%H:%M:%S')}  {r['current_steps']:5,}/{r['total_steps']} "
              f"{r['percentage']:6.2f}%  {r['loss']:7.4f}  {r['elapsed_time']:>10}  "
              f"{r['remaining_time']:>10}   {ck[-1] if ck else '-'}"
              + ("" if song else "  ⚠ CHẾT"), flush=True)
    else:
        L = open(LOG, encoding="utf-8", errors="ignore").read()
        tk = [l for l in L.replace("\r", "\n").splitlines() if "Running tokenizer" in l]
        print(f"{time.strftime('%H:%M:%S')}  chưa có bước mới · "
              f"{(tk[-1][-45:] if tk else 'đang chuẩn bị / log còn trong bộ đệm')}"
              + ("" if song else "  ⚠ TIẾN TRÌNH CHẾT"), flush=True)
    if not song:
        print("--- 12 dòng cuối log ---")
        print("\n".join(open(LOG, encoding="utf-8", errors="ignore").read().splitlines()[-12:])); break
    if moi and moi[-1]["current_steps"] >= moi[-1]["total_steps"]:
        print("*** ĐỦ SỐ BƯỚC — chờ lưu bản cuối rồi chạy A.5c → A.6 ***")
    time.sleep(NHIP)
```

⚠️ **`MOC` là chỗ dễ đọc nhầm nhất khi chạy tiếp một lượt dở.** `trainer_log.jsonl` được
**ghi nối thêm**, nên sau khi chạy lại nó vẫn còn nguyên các dòng của lần trước. Không đặt
`MOC` = bước cuối của lần trước thì ô này in lại con số cũ y như thật, và trông hệt như
"train đang chạy" trong khi thực ra chưa có bước mới nào. Ngày 12/8 lượt s1 đứt ở **1.780**,
nên khi chạy tiếp phải đặt `MOC = 1780`.

⛔ **Và `MOC` phải lấy theo DÒNG LOG CUỐI, không theo số của ĐIỂM LƯU** (vá 16/8). Hai con số
này khác nhau vì `logging_steps: 20` còn `save_steps: 200` — log luôn chạy trước điểm lưu tới
180 bước. Lượt s1/202 ngày 16/8 có điểm lưu `checkpoint-4800` nhưng chết ở bước **4.880**;
đặt `MOC = 4800` nên bộ lọc `> MOC` không chặn được dòng cũ, và ô A.5 in `4.880` ba lần liền
(13:28 · 13:43 · 13:58) trong suốt 45 phút mã hoá token — trông hệt như train đang chạy mà
đứng yên. Ô A.1c nay tự chốt số này vào `/content/MOC.txt`.

💡 **Dấu hiệu nhận biết miễn phí:** khi phiên mới thật sự ghi dòng đầu tiên, số bước sẽ
**TỤT XUỐNG** (4.880 → 4.820), vì dòng mới đầu tiên = điểm-lưu + `logging_steps`. Thấy số
lùi là mừng, không phải lo — đó là lúc train thật sự chạy lại.

⚠️ **Dòng `Resuming training from …` in RẤT SỚM**, ngay lúc phân tích tham số
(`llamafactory.hparams.parser:144`), trước cả 2,5 giờ mã hoá token. Thấy nó **chưa** có nghĩa
là đã chạy tiếp — chỉ có nghĩa nó *định* chạy tiếp. Bằng chứng thật là `current_steps` mới
lớn hơn `MOC`.

⭐ **Nhưng phải kiểm nó NGAY, đừng đợi hết 2,5 giờ** (12/8): nếu nó không nhận ra điểm lưu
thì bạn đang trả 2,5 giờ mã hoá token để rồi train lại từ bước 0, và chỉ phát hiện ra khi
mọi thứ đã muộn. Kiểm mất 2 giây:

```bash
grep -n "Resuming\|Continuing" /content/train_s1_seed101.log | tail -3
```

Phải ra dòng `Resuming training from /content/drive/MyDrive/thesis/ckpt/<nhánh>_seed<hạt>/checkpoint-N`.
Rỗng thì dừng ngay: giết tiến trình, chạy lại ô A.2 và đọc dòng `BÊN TRONG output_dir`.

⚠️ **Nhân Python bận thì dùng TERMINAL của Colab** (biểu tượng `>_` góc dưới trái). Ô A.4
bản cũ chiếm nhân suốt, mà cả ba lệnh theo dõi đều chạy được từ Terminal, không đi qua nhân:

```bash
tail -c 300 /content/train_s1_seed101.log                                   # thanh mã hoá token
tail -1 /content/drive/MyDrive/thesis/ckpt/s1_seed101/trainer_log.jsonl     # bước train
ps -eo pcpu,rss,args --sort=-pcpu | head -5                                 # còn sống + ăn mấy lõi
```

⭐ **Nguồn tiến độ là `trainer_log.jsonl`, không phải log văn bản** (sửa 12/8). LLaMA-Factory
tự ghi tệp này vào `output_dir` mỗi `logging_steps`, mỗi dòng có sẵn `current_steps`,
`total_steps`, `percentage`, `loss`, `elapsed_time`, **`remaining_time`** — do chính nó tính,
khỏi phải ước. Bản cũ **suy** số bước từ `epoch` trong log, mà `epoch` chỉ in 2 chữ số thập
phân nên số bước nhảy từng nấc 40, và cách đó lệ thuộc dấu nháy trong log (khác nhau giữa
các phiên bản).

Lợi thế lớn hơn: tệp này **nằm trên Drive**, nên (a) mất máy ảo vẫn còn nguyên lịch sử,
(b) mở được từ máy khác hoặc phiên khác — kể cả điện thoại — chỉ cần vào Drive xem dòng cuối.

**Kiểm điểm lưu xuất hiện trên Drive** sau ~200 bước đầu. Không thấy nghĩa là `output_dir`
trỏ sai và phiên chết là mất sạch — dừng ngay, sửa, chạy lại.

Chặn tab và máy ngủ. **Phiên chết thì làm lại đúng thứ tự này** (sửa 12/8 cho khớp phần đầu
mục PHIÊN TRAIN — bản cũ ghi `A.1 → 0.3 → restart → A.1` là bung 33 GB hai lần):

```
0.3 → Restart session → A.1 → A.1b → A.1c → A.1d → HF_TOKEN → A.2 → A.4 → A.4b → A.5
```

Bỏ qua A.3 → A.3i. Ô A.4 tự dò điểm lưu gần nhất trong `output_dir` mà chạy tiếp; lúc đó
dòng `BÊN TRONG output_dir` của ô A.2 **phải** có `checkpoint-*` — khác với lượt chạy mới.

### Ô A.5b — XÁC NHẬN NỐI TIẾP Ở QUY MÔ THẬT (tuỳ chọn từ 11/8)

Chờ tới khi ô A.5 thấy **checkpoint-200** xuất hiện trên Drive, rồi cố ý giết tiến trình
và bật lại:

```python
import subprocess, glob, os, time
print("điểm lưu hiện có:", [os.path.basename(x) for x in sorted(glob.glob(f"{D}/ckpt/{BRANCH}_seed{SEED}/checkpoint-*"))])
subprocess.run("pkill -f llamafactory-cli", shell=True); time.sleep(5)
print("đã giết tiến trình")
```
```python
!cd {REPO} && PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True nohup llamafactory-cli train /content/cfg.yaml >> {LOG} 2>&1 &
```
```python
import time, re; time.sleep(150)
L = open(LOG, encoding="utf-8", errors="ignore").read()
print("có nhận ra điểm lưu:", any(k in L for k in ("Resuming", "Continuing training")))
print([l.strip()[:110] for l in L.splitlines() if "Resuming" in l or "Continuing" in l][-3:])
print("mốc epoch gần nhất :", re.findall(r"'epoch':\s*'?([\d.]+)", L)[-3:] or "chưa in")
```

⚠️ **Ghi vào CÙNG tệp `LOG`, không phải `resume.log` riêng** (sửa 12/8). Bản cũ đổ ra
`/content/resume.log`, trong khi ô A.5 vẫn đọc `train.log` — sau A.5b, ô theo dõi sẽ thấy số
bước **đứng yên vĩnh viễn** và trông hệt như treo, dù train đang chạy bình thường. Dồn về
một tệp thì ô A.5 không phải biết gì về chuyện đã khởi động lại, và dòng
`Resuming training from …` nằm ngay trong log làm mốc.

**Ô này nay là TUỲ CHỌN.** Cơ chế nối tiếp đã được chạy thật ở **ô A.3i** ngày 11/8 (lượt 10
bước ghi thẳng Drive rồi chạy tiếp lên 20: có `optimizer.pt`, log in `Resuming training
from /content/drive/…`, `global_step = 20` chứ không quay về 10). A.5b chỉ còn là xác nhận
lại ở quy mô thật — làm thì tốt, tốn ~5 phút, nhưng không còn là cửa sinh tử như trước.

Nó phải in ra chỗ nhận điểm lưu và mốc epoch > 0. Bắt đầu lại từ 0 thì **dừng, báo mình**.

### Ô A.5c — BUNG LẠI ẢNH TẬP KIỂM ⚠️ chạy trước A.6 nếu đã xoá để lấy chỗ

```python
import os
TE = f"{REPO}/harness/dg1_cache/test_ac"
n = len(os.listdir(f"{TE}/images")) if os.path.isdir(f"{TE}/images") else 0
print("ảnh kiểm đang có:", n)
if n < 6958:
    !tar xf {D}/test_images.tar -C {TE}
    print("đã bung lại:", len(os.listdir(f"{TE}/images")), "← 6.958")
```

Ảnh tập kiểm (3,2 GB) **không cần trong suốt 24 giờ train** — chỉ cần từ ô A.6 trở đi. Colab
cảnh báo đầy đĩa ở ngưỡng 80%, và đây là chỗ dọn rẻ nhất: bung lại chỉ mất ~3 phút.

Số đo 12/8: đĩa máy ảo 113 GB, dùng 91 GB = ảnh dạy 30 + ảnh kiểm 3,2 + bộ đệm HuggingFace
8,3 (mô hình 3B) + **~40 GB ảnh nền Colab** + linh tinh. ⚠️ `du -sh /content/drive` báo 40 GB
là **nội dung trên Drive**, không phải chỗ trên đĩa máy ảo — đi qua fuse nên đếm tệp ở xa,
rất dễ đọc nhầm thành thủ phạm. Checkpoint ghi thẳng Drive, **không** tích trên đĩa cục bộ.

### Ô A.6 — tự kiểm lô (CHỈ lần đầu tiên trong cả chiến dịch)

```python
!cd {REPO} && python harness/infer_branch.py --selftest-batch \
    --adapter {D}/ckpt/{BRANCH}_seed{SEED} --batch 8
```

Phải ra **8/8 trùng nguyên văn**. Rớt là dừng hẳn, đừng chấm.

### Ô A.7 — sinh câu thử 20 bước trước

```python
!cd {REPO} && python harness/infer_branch.py --adapter {D}/ckpt/{BRANCH}_seed{SEED} \
    --out /content/preds_smoke.jsonl --limit 20
```
```python
import json
for r in list(map(json.loads, open("/content/preds_smoke.jsonl", encoding="utf-8")))[:8]:
    print(f"[{r['episode_id']}/{r['step_id']}]\n  chuẩn: {r['gold_instruction']}\n  model: {r['pred']}\n  thô  : {r['raw'][:110]}\n")
```

### Ô A.7b — THỬ NỐI TIẾP KHÂU SINH CÂU ⚠️ chạy A.7 LẦN THỨ HAI, y hệt

```python
!cd {REPO} && python harness/infer_branch.py --adapter {D}/ckpt/{BRANCH}_seed{SEED} \
    --out /content/preds_smoke.jsonl --limit 20
```

Phải in **`Nối tiếp: đã có 20 bước, còn 0`** rồi **`Xong sẵn 20 bước`** và thoát trong vài
giây, không sinh lại câu nào.

⚠️ **Đổi 12/8: nay nó KHÔNG in dòng `Nạp …` nữa.** Khối nối tiếp đã dời lên trước lúc nạp
mô hình, nên lượt đã xong thoát mà không đụng tới 3 tỉ tham số. Bản runbook trước dặn
"vẫn in `Nạp …`, đừng đọc là hỏng" — câu đó nay sai, thấy `Nạp …` mới là lạ.

⭐ **Chữ ký lượt chạy (thêm 12/8).** Mỗi bản ghi nay mang trường `run` — `lora:s1_seed101`,
`+ceiling_gold`, `+binfer`, `base`. Nối tiếp một tệp của lượt khác thì nó **dừng hẳn** thay
vì in "Xong sẵn". Đây là chỗ hỏng đắt nhất mà không có tiếng động: chiến dịch có cả chục
lượt chỉ khác nhau vài cờ (2 hạt giống × 4 nhánh, trần gold/filler, B-infer, mô hình gốc),
toàn chép lại một dòng lệnh — quên đổi `--out` là nó thoát sau hai giây, trông y như vừa
chạy xong, mà thật ra chưa sinh câu nào. Thử luôn ở đây cho rẻ:

```python
!cd {REPO} && python harness/infer_branch.py --ceiling gold \
    --adapter {D}/ckpt/{BRANCH}_seed{SEED} --out /content/preds_smoke.jsonl --limit 20
```

Phải ra **`⛔ … là của lượt chạy KHÁC`** và thoát. Nếu nó chạy tiếp thì cơ chế không hoạt
động — dừng và báo lại.

Cơ chế nối tiếp của `infer_branch.py` và `score_run.py` là **mã viết ngày 11/8 và chưa từng
chạy**. Nó gánh cả chục lượt sinh câu 1,5 giờ và mấy lượt chấm 5 giờ. Bài học 10/8 nói rõ:
soi mã đúng chưa phải là chạy thử — bản đồng bộ Drive cũng "soi thì đúng", và chỉ ô kiểm 7
phút mới cho biết nó thật sự chạy. Ở đây phép thử tốn 30 giây.

In ra `Nạp …` rồi sinh lại 20 bước ⇒ cơ chế **không hoạt động**, dừng và báo lại.

## 🛑 MỐC DỪNG 5 — dán output ô A.6, A.7 và A.7b

Đây là **lần đầu tiên nhìn thấy mô hình đã huấn luyện viết gì**. Cần xem: câu có ra tiếng
Anh mạch lạc không · với nhánh S2 thì phần `<desc>` có được sinh đúng khuôn và có bị cắt
bỏ sạch khỏi trường `pred` không · có bị lặp vô hạn không. Cái nào hỏng ở đây thì 1,5 giờ
sinh câu cho 6.958 bước là ném đi.

---

### Ô A.8 — sinh câu đủ tập kiểm

```python
import subprocess, os
ILOG = f"/content/infer_{BRANCH}_seed{SEED}.log"
subprocess.Popen(["python", "harness/infer_branch.py",
                  "--adapter", f"{D}/ckpt/{BRANCH}_seed{SEED}",
                  "--out", f"{D}/preds/preds_{BRANCH}_seed{SEED}.jsonl"],
                 cwd=REPO, stdout=open(ILOG, "a"), stderr=subprocess.STDOUT,
                 start_new_session=True)
print("đã khởi động →", ILOG)
```

⛔ **Đừng dùng `!cd {REPO} && nohup … &`** (bản cũ) — đúng lỗi đã cắn hai lần ở ô A.4: nó
chạy **tiền cảnh**, chiếm nhân Python suốt 1,5 giờ nên không bấm được ô theo dõi ngay bên
dưới. `Popen(start_new_session=True)` trả về ngay và sống sót cả khi nhân bị khởi động lại.
```python
import subprocess, os
p = f"{D}/preds/preds_{BRANCH}_seed{SEED}.jsonl"
n = sum(1 for _ in open(p, encoding="utf-8")) if os.path.exists(p) else 0
alive = "infer_branch" in subprocess.run(["ps","-eo","args"],capture_output=True,text=True).stdout
print(f"{n:,} / 6.958   ·   {'đang chạy' if alive else 'ĐÃ DỪNG'}")
!tail -2 /content/infer_{BRANCH}_seed{SEED}.log
```

### Ô A.9 — kiểm tệp dự đoán trước khi tắt máy

```python
import json
R = list(map(json.loads, open(f"{D}/preds/preds_{BRANCH}_seed{SEED}.jsonl", encoding="utf-8")))
tap = [r for r in R if r["action"].get("action_type") in ("click","long_press") and "x" in r["action"]]
print(f"bản ghi : {len(R):,}   ← phải là 6.958")
print(f"bước chạm: {len(tap):,}   ← phải là 4.463")
print(f"câu rỗng : {sum(1 for r in R if not r['pred'].strip())} = {sum(1 for r in R if not r['pred'].strip())/len(R):.1%}")
print(f"còn sót <desc> trong pred: {sum(1 for r in R if '<desc>' in r['pred'])}   ← phải là 0")
print(f"độ dài câu trung vị: {sorted(len(r['pred']) for r in R)[len(R)//2]} ký tự")
```

**Điều kiện kết thúc phiên train:** `ckpt/…` và `preds_…jsonl` nằm trên Drive, ô A.9
sạch, **ô A.10 đã chạy**. Rồi mới tắt máy.

---

### Ô A.10 — LƯU VẾT lên Drive ⚠️ chạy trước khi tắt máy, mọi phiên

```python
import os, shutil, json, glob, re
V = f"{D}/logs/{BRANCH}_seed{SEED}"
os.makedirs(V, exist_ok=True)
for f in ["/content/cfg.yaml", LOG, f"/content/infer_{BRANCH}_seed{SEED}.log",
          "/content/preds_smoke.jsonl"] + glob.glob("/content/log_P*.log") + glob.glob("/content/long_*.log"):
    if os.path.exists(f): shutil.copy(f, V)
for f in glob.glob(f"{REPO}/harness/descriptor_build_stats*.json"): shutil.copy(f, f"{D}/logs/")

# Đường cong mất mát tách riêng, để vẽ hình cho luận văn mà không phải mở lại log.
# Lấy từ trainer_state.json của điểm lưu CUỐI, không phải từ log: nó là bản chính thức,
# không lệ thuộc chuyện log có bị ghi đè hay không, và có sẵn cả learning_rate lẫn grad_norm.
st = f"{D}/ckpt/{BRANCH}_seed{SEED}/trainer_state.json"
if os.path.exists(st):
    pts = [x for x in json.load(open(st))["log_history"] if "loss" in x]
else:                                   # dự phòng: bóc từ log (dấu nháy tuỳ phiên bản)
    L = open(LOG, encoding="utf-8", errors="ignore").read()
    pts = [{"epoch": float(e), "loss": float(l)} for e, l in
           zip(re.findall(r"'epoch':\s*'?([\d.]+)", L), re.findall(r"'loss':\s*'?([\d.]+)", L))]
json.dump(pts, open(f"{V}/loss_curve.json", "w"), indent=1)
print(f"{len(os.listdir(V))} tệp trong {V} · {len(pts)} điểm mất mát")
print(sorted(os.listdir(V)))
```

**Vì sao phải giữ từng thứ:**

| Tệp | Dùng vào việc gì |
|---|---|
| `cfg.yaml` của TỪNG lượt | **bằng chứng** cho câu "sáu nhánh chỉ khác nhau ba dòng". Không có nó thì đó là lời khai, không phải chứng cứ |
| `train.log` + `loss_curve.json` | hình đường cong mất mát trong luận văn; và để thấy lượt nào phân kỳ |
| `probe.log` | giây-mỗi-bước, dùng cho phần báo cáo chi phí tính toán |
| `resume.log` | chứng minh cơ chế nối tiếp có chạy |
| `preds_*.jsonl` | câu mô hình viết — cần cho chấm tay, cho ví dụ định tính, cho mọi phân tích sau |
| `score_*_raw.jsonl` | toạ độ bộ trỏ **từng bước**. Đổi luật chấm hay thêm lát cắt thì tính lại từ đây, khỏi gọi lại bộ trỏ |
| `descriptor_build_stats*.json` | thống kê nhãn ở quy mô đủ, để đối chiếu với con số báo trong luận văn |
| thư mục `ckpt/` | bộ trọng số. Cần khi muốn sinh lại câu, hoặc khi hội đồng đòi chạy thử |

**Nguyên tắc: thứ gì tính lại tốn tiền hoặc tốn giờ thì phải nằm trên Drive trước khi tắt
máy.** Colab xoá sạch `/content` khi phiên chết, không hỏi lại.

---

# CHẤM ĐIỂM — trên Kaggle, MIỄN PHÍ

Đừng chấm trên Colab: chỉ cần UGround 2 tỉ tham số, T4 gánh được, Kaggle cho 30 giờ mỗi
tuần không mất gì. ~5 giờ một nhánh.

Tải `preds_…jsonl` từ Drive về máy nhà → mình gộp thành gói Kaggle (cần đủ 4.463 ảnh của
tập kiểm, khác gói cổng A chỉ có 300) → chạy:

```
python harness/score_run.py --mode score --grounder uground \
    --preds preds_s1_seed101.jsonl --out score_s1_seed101.json
```

Giữ `score_…_raw.jsonl`: nó lưu toạ độ bộ trỏ từng bước, đổi luật chấm hay thêm lát cắt
thì chấm lại từ đó chứ không gọi lại bộ trỏ.

## 🛑 MỐC DỪNG 6 — sau khi chấm xong CẢ HAI hạt giống của S1

Đây là mốc quyết định của toàn luận văn. Với hai điểm S1 mình tính:

- **cỡ nhiễu hạt giống** = |S1(101) − S1(202)| — Δ giữa S2 và S1 phải lớn hơn con số này
- **MDE THẬT** từ phương sai quan sát được, thay cho MDE chiếu 3,9-6,6 pp
- **khoảng trống còn lại** so với trần. S1 mà đã sát trần thì S2 không có chỗ để hơn,
  và phải bàn lại trước khi tiêu thêm tiền cho bốn lượt train nữa

Rồi mới **khoá ngưỡng đậu/rớt** vào `report/106` kèm ngày, **rồi mới train S2**.

> **✅ Mốc này đã qua (17/8).** Nhiễu hạt giống **0,52 pp** · MDE thật **2,2 pp** · trần
> **75,7%** (⛔ con số 70,0 ở bản trước **đã bị rút** — nó đo trên mẫu con 300 bước) và sàn
> **12,0%** ⇒ dải dùng được **62,9 điểm**, S1 ở 74,4% của dải nên còn chỗ cho S2. Ngưỡng khoá
> **2,8 pp**, ghi ở `report/106` mục sửa đổi **(w)**. S2 hạt giống 101 train từ 18/8 —
> runbook dán thẳng: **`harness/S2_DAN_THANG.md`**.

---

# Trình tự cứng — không đảo (report/106 mục 5)

| # | Việc | Phiên | Đơn vị |
|---|---|---|---|
| 0 | dựng dữ liệu + OCR | 1 | ~35 |
| 1 | S1 hạt giống 101 → train + sinh câu | 1 | ~90-130 |
| 2 | S1 hạt giống 202 → train + sinh câu | 1 | ~90-130 |
| 3 | chấm cả hai **trên Kaggle** → MDE thật | — | 0 |
| 4 | 🛑 khoá ngưỡng vào report/106 | — | 0 |
| 5 | phép thử TRẦN trên S1 (`--ceiling gold` + `filler`) | 1 | ~20 |
| 6 | S2 hạt giống 101 và 202 | 2 | ~180-260 |
| 7 | S2r, S2-nopoint | 2 | ~180-260 |
| 8 | B-infer + mô hình gốc (chỉ suy luận) | 1 | ~20 |
| 9 | S3-pilot — **chưa có mã hàm phạt lề** | — | — |

**Bước 3 và 4 phải xong trước bước 6.** Đảo thì ghi lý do vào bản đăng ký và coi kết quả
là thăm dò.

Lệnh cho bước 5 và 8 (chạy trong phiên train, sau ô A.1):

```python
import subprocess
A = f"{D}/ckpt/s1_seed101"
jobs = [
    # phép thử TRẦN — trần là hiệu số gold − filler, KHÔNG phải gold − S1
    (f"--ceiling gold   --adapter {A}", f"{D}/preds/preds_ceiling_gold_s1_seed101.jsonl"),
    (f"--ceiling filler --adapter {A}", f"{D}/preds/preds_ceiling_filler_s1_seed101.jsonl"),
    # B-infer: trọng số S1, nhét DANH SÁCH phần tử lúc chạy (không chỉ ra cái nào là đích)
    (f"--b-infer        --adapter {A}", f"{D}/preds/preds_binfer_s1_seed101.jsonl"),
    # mốc tham chiếu: mô hình gốc, chưa huấn luyện gì
    ("--no-adapter",                    f"{D}/preds/preds_base.jsonl"),
]
for flags, out in jobs:
    print("──", out.split("/")[-1])
    r = subprocess.run(f"python harness/infer_branch.py {flags} --out {out}",
                       shell=True, cwd=REPO, capture_output=True, text=True)
    print(r.stdout[-400:] or r.stderr[-400:])
```

---

# SAU KHI CÓ ĐIỂM — bốn khâu đã đăng ký, không cần GPU, không tốn đơn vị

Bốn khâu này nằm trong bản đăng ký nên **bắt buộc có số**, nhưng không cần card. Làm ở máy
nhà hoặc trên Kaggle. Liệt ở đây để không rơi mất — đúng loại lỗi đã bắt bốn lần (script
suy luận, script chấm, thước không-gây-hại, phép thử trần: nằm trong hồ sơ, tới lúc cần
thì không có gì chạy).

**1. Thước không-gây-hại** (`report/106` mục 3, BẮT BUỘC). Trên các bước KHÔNG phải bước
chạm — cuộn, gõ, mở ứng dụng, chờ, quay lại, chiếm 35,9% tập kiểm — nhánh khai báo không
được thấp hơn nhánh nền quá **3 điểm phần trăm**. Không cần bộ trỏ nên chạy ở đâu cũng được:

```
python harness/score_run.py --mode noharm \
    --preds preds_s2_seed101.jsonl --baseline preds_s1_seed101.jsonl \
    --out noharm_s2_seed101.json
```

**2. Ba lát cắt đã đăng ký**, tính lại từ `score_…_raw.jsonl` chứ không gọi lại bộ trỏ:
toàn tập · **lát khó** (bước thuộc phần ba dưới của phân bố khoảng cách tới phần tử cùng
vai trò gần nhất) · **nhóm ứng dụng chưa thấy lúc dạy** (nhãn `app_seen_in_train`). Kỳ
vọng đã đăng ký: Δ ở lát khó **lớn hơn** Δ toàn tập; ngược lại thì phải ghi rằng cơ chế
không như giả thuyết.

**3. Chấm tay 100 câu, hai người độc lập.** Lá chắn cho đòn "thước thiên vị câu dài". Cần
dựng bộ chấm mù (không cho biết câu của nhánh nào) và báo κ giữa hai người. **Chưa có mã** —
phải viết khi có câu thật.

**4. Bản trình diễn tiếng Việt, định tính.** Vài chục màn, không có bảng số. Đã hứa trong
hồ sơ.

---

# Chấm điểm trên Kaggle — cần gì

Gói cổng A (`thesis_kaggle_gateA.zip`) chỉ có **300 ảnh**, không đủ để chấm 4.463 bước.
Cần một gói khác gồm đủ ảnh bước chạm (~1,7 GB) hoặc dựng lại tập kiểm ngay trên Kaggle
bằng `build_test_data.py --shards 9`. Mình sẽ dựng gói đó khi bạn có tệp dự đoán đầu tiên —
ghi ở đây để không quên là **nó chưa tồn tại**.

# Đối chiếu với bản đăng ký — mục nào chạy ở đâu

Bảng này để soi xem runbook có bỏ sót thứ đã cam kết không. Cột cuối là chỗ duy nhất được
phép ghi "chưa có mã", và ghi thì phải khai trong luận văn.

| Mục trong `report/106` | Chạy ở đâu trong runbook |
|---|---|
| Cổng A — sai số bộ trỏ ≤3% | ✅ **đã xong 9/8** trên Kaggle, ĐẠT 0,7%. **Đừng chạy lại**, tốn tiền vô ích |
| §5 bước 3 — S1 hai hạt giống | phiên train ×2, ô A.2 đổi `SEED` |
| §5 bước 3 — chấm đủ | Kaggle, miễn phí |
| §5 bước 4 — MDE thật + cỡ nhiễu hạt giống | mốc dừng 6 |
| §5 bước 5 — khoá ngưỡng vào `report/106` | mốc dừng 6, mình ghi |
| §5 bước 6 — phép thử TRẦN | ô cuối, `--ceiling gold` + `--ceiling filler` |
| §5 bước 7 — S2 hai hạt giống | phiên train ×2 |
| §5 bước 8 — S2r, S2-nopoint, B-infer | phiên train ×2 + ô `--b-infer` |
| Sửa đổi 9/8 (k) — mốc mô hình gốc | ô `--no-adapter` |
| §5 bước 9 — S3-pilot (khoản phạt lề) | ⛔ **CHƯA CÓ MÃ** hàm mất mát. Dữ liệu đã sửa 9/8. Không kịp thì khai *"đã đăng ký nhưng không chạy"* |
| §3 — thước không-gây-hại (BẮT BUỘC) | mục "sau khi có điểm", `--mode noharm` |
| §5 bước 10 — chấm tay 100 câu, 2 người | ⛔ **chưa có mã bộ chấm mù** |
| §5 bước 10 — demo tiếng Việt | mục "sau khi có điểm" |
| Ba lát cắt đã đăng ký | mục "sau khi có điểm", tính từ `score_*_raw.jsonl` |
| §2 — hạt giống 101/202 (303 nếu cổng kích hoạt) | ô A.2 |
| §10 — hạt giống lấy mẫu 20260805 | trong mã, không đụng vào |
| §6 — luật đọc kết quả | mốc dừng 6, đọc **trước** khi nhìn số |

**Bốn phép kiểm không nằm trong bản đăng ký nhưng runbook bắt buộc**, vì chúng chặn đúng
những kiểu hỏng đã bắt được:

| Phép | Ô | Chặn gì |
|---|---|---|
| rò rỉ tác vụ dạy ↔ kiểm | 0.11b | mô hình học đúng đề thi — không sửa được sau khi train |
| phủ OCR 100% | 0.9 | vài nghìn bước vào huấn luyện với đầu vào thiếu chữ |
| 9 bất biến bốn nhánh | 0.11 | bốn nhánh không so được với nhau |
| thử nối tiếp | A.5b | phiên đứt ở giờ thứ 11 mà không nối lại được |

---

# Bốn điều tuyệt đối không đổi giữa chừng

1. **Cỡ lô hiệu dụng = 16.** Card 80 GB cho phép `16×1` thay `4×4` (nhanh gần gấp đôi,
   gradient y hệt về mặt toán học), nhưng phiên nào tụt xuống 40 GB thì `16×1` không chạy
   nổi. **Giữ `4×4`** trừ khi chắc chắn mọi phiên đều 80 GB.
2. **`bf16: true`.** Phiên nào ra T4/L4 thì không train ở đó.
3. **Hạt giống 101 và 202.**
4. **`output_dir` luôn trên Drive.**

# Nếu hết đơn vị giữa lượt train

Điểm lưu nằm trên Drive nên không mất gì. Mua thêm rồi: ô A.1 → ô 0.3 → restart → A.1 →
A.2 → **A.4** (bỏ A.3). Nó tự dò điểm lưu gần nhất mà nối tiếp — đúng lý do
`resume_from_checkpoint` cố ý bỏ trống trong `train_config.yaml`.

# Bảng tiền

**Tốc độ đốt đo thật 10/8 trên A100-SXM4-40GB: `5,3 đơn vị/giờ`** (Colab tự in ở panel *Xem
tài nguyên*). Con số 6,77 của bản kế hoạch là của card 80 GB — **đọc lại panel mỗi phiên**,
đừng nhớ, đây đã là lần thứ ba số này khác với lần đo trước.

| khâu | giờ | đơn vị @5,3/h | tiền |
|---|---|---|---|
| phiên 0 | ~4,5-5 | 24-27 | ~$2,5 |
| 6 lượt train | 66-108 | 350-572 | $35-57 |
| 7 lượt sinh câu | ~10 | 53 | $5 |
| trần + B-infer + mô hình gốc | ~5 | 27 | $3 |
| **tổng** | **86-128** | **454-679** | **$45-68** |

Ở $9,99/100 đơn vị. Chấm điểm không tính vì chạy trên Kaggle.

⚠️ **Trạng thái ví 10/8: `not subscribed`, còn 99,79 đơn vị** — đủ trọn phiên 0 (còn dư ~73)
nhưng **không đủ một lượt train** (58-95 đơn vị). Phải mua thêm ~400-600 đơn vị trước ô A.4.
Đơn vị trả-theo-lượt hết hạn sau 90 ngày, mua một lần cho cả chiến dịch là được.

**Ghi lại số đơn vị còn lại ở mỗi mốc dừng** — đó là cách duy nhất biết ước tính có đúng
không, và biết sớm trước khi hết.
