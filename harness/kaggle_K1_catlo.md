# K1 — chấm thử điểm lưu VIS-SFT giữa lượt (Kaggle T4, 0 đồng) — 10/9/2026

Tự chứa, không cần mở runbook khác. Thi hành **điểm kiểm K1** của ô G8 trong
`harness/colab_vissft_9_9.md`.

## ⛔ Đọc trước — hai điều quyết định cách đọc kết quả

**① Luật đã khoá TRƯỚC khi nhìn số:** dừng lượt train **chỉ khi** VIS-SFT thấp hơn MIN-DESC
**quá 3,0 điểm** trên cùng `val_cham400`. Ngưỡng 3,0 ≈ 3 lần sai số chuẩn ghép cặp trên 400 bước
chạm. ⛔ Không dừng khi chỉ *"chưa tốt hơn"* — mô hình mới ở 41% lượt, có thể còn đang học.
⛔ Không nới ngưỡng sau khi thấy số.

**② Phép so này BẤT LỢI cho VIS-SFT.** Val là dữ liệu MIN **đã thấy** (MIN train trên trọn 64.567
bước), còn VIS-SFT train trên 63.000 đã trừ val. ⇒ VIS-SFT **vượt** MIN là bằng chứng mạnh;
**thua** thì không đọc thành *"VIS-SFT kém hơn"*, chỉ dùng để bắt sụp đổ.
⛔ Và như mọi số val: **không trích ra báo**.

---

## A. Máy nhà — ✅ ĐÃ LÀM SẴN

`_bundles/thesis_val_cham.zip` (**808 MB**): `val_cham400.jsonl` (607 bước / 400 chạm) ·
`val_cham600.jsonl` (960 / 602) · `ocr.jsonl` **1.567 dòng** · `images/` **1.567 ảnh**.
Dùng lại được cho A6 sau lượt, nên không phải đóng gói hai lần.

⭐ Cây trợ năng **không cần đóng gói** — `a11y_inventory` tự tải từ HuggingFace; chỉ cần bật
Internet cho notebook.

---

## B. Lấy `step03200` — làm trong **Terminal Colab**

⛔ **Không chạy ô notebook nào.** Nhân Python đang bận ô G7 nên ô mới chỉ xếp hàng, và phản xạ kế
tiếp thường là bấm Stop — đúng cái đã giết một lượt train hôm 2/9. Terminal là tiến trình riêng.

```bash
cd /content/drive/MyDrive/thesis/ckpt/vissft_seed101
mkdir -p /content/k1
cp -r grid/step03200 /content/k1/vissft_step03200
ls -la /content/k1/vissft_step03200          # phải có adapter_model.* + adapter_config.json
cd /content && zip -0 -qr /content/drive/MyDrive/thesis/k1_adapter.zip k1
ls -la /content/drive/MyDrive/thesis/k1_adapter.zip
```

Tải `k1_adapter.zip` từ **drive.google.com** về máy (không tải qua ô Colab).

## C. Gộp adapter ở máy nhà rồi tạo dataset

Giải nén `k1_adapter.zip`, chép thêm `runs/grpo_point/adapter_ref_min/` vào cạnh, thành cây:

```
k1_adapters/
├── adapter_ref_min/          ← 2 tệp, lấy từ runs/grpo_point/
└── vissft_step03200/         ← 2 tệp, lấy từ Drive
```

Zip lại thành `k1_adapters.zip` rồi tạo **dataset Kaggle MỚI** tên `thesis-k1-adapters`.
⛔ Dataset **mới**, đừng dùng "New Version" của dataset cũ — New Version *thêm* thư mục chứ không
thay thế, nên nhiều gói cùng tồn tại và ô dò sẽ chọn mò (bài học 5/9).

Notebook Kaggle: **Add Data** ba dataset — `thesis-val-cham` · `thesis-k1-adapters` ·
`thesis-code-9-9`. **Settings → Accelerator → GPU T4 x2**, **Internet ON**.

---

## D. Notebook Kaggle — sáu ô

### Ô 1 — gỡ `torchao` (⛔ ô ĐẦU TIÊN, kể cả khi chạy lại)

```python
!pip uninstall -y -q torchao
import importlib.util, torch
print("torchao còn:", importlib.util.find_spec("torchao"), "← phải None")
print("GPU:", torch.cuda.get_device_name(0))
```

⚠️ `torchao 0.10.0` cài sẵn trên Kaggle làm `peft` ném `ImportError` **ngay lúc gắn LoRA**, tức
sau khi đã tải xong mô hình nền — mất hàng chục phút mới thấy lỗi.

### Ô 2 — dò mount, dựng workspace

```python
import glob, os, shutil, json

def tim(mau):
    r = sorted(glob.glob(f"/kaggle/input/**/{mau}", recursive=True))
    assert r, f"⛔ không thấy {mau} — kiểm ba dataset đã Add chưa"
    return r[0]

DATA = os.path.dirname(tim("val_cham400.jsonl"))      # data-root, đọc thẳng từ input
HARN = os.path.dirname(tim("harness/score_run.py"))  # ⚠️ ĐÃ LÀ thư mục harness, đừng nối thêm
AD   = os.path.dirname(os.path.dirname(tim("adapter_ref_min/adapter_config.json")))
print("data-root :", DATA)
print("harness   :", HARN)
print("adapter   :", AD, "→", sorted(os.listdir(AD)))

WS = "/kaggle/working/k1"; shutil.rmtree(WS, ignore_errors=True)
shutil.copytree(HARN, f"{WS}/harness")
os.chdir(WS)

# gói mã phải có bản vá P5 (--data-root / --recs-file) ở CẢ HAI script
for f in ("infer_branch.py", "score_run.py"):
    s = open(f"{WS}/harness/{f}").read()
    assert "--data-root" in s and "--recs-file" in s, f"⛔ {f} chưa có bản vá P5"
print("gói mã    : có P5 ✓")

# dữ liệu phải đủ
n = sum(1 for _ in open(f"{DATA}/val_cham400.jsonl", encoding="utf-8"))
o = sum(1 for _ in open(f"{DATA}/ocr.jsonl", encoding="utf-8"))
recs = [json.loads(l) for l in open(f"{DATA}/val_cham400.jsonl", encoding="utf-8")]
thieu = [r for r in recs if not os.path.exists(os.path.join(DATA, r["image"]))]
print(f"val_cham400: {n} bước ← cần 607 · ocr {o} dòng ← cần 1567 · ảnh thiếu {len(thieu)}")
assert n == 607 and not thieu, "⛔ dữ liệu không đủ"
print("\n✅ sẵn sàng")
```

⛔ Phép kiểm ảnh phủ **cả 607 bước**, không chỉ bước đầu — hỏng đường dẫn ảnh chỉ nổ ra *sau khi
đã nạp xong mô hình*, tức muộn hàng chục phút.

### ⛔ Ô 2b — vá tên trường (bắt buộc, nếu không sẽ `KeyError` sau 2 phút)

`tach_val.py` xuất val theo khuôn của `train.jsonl` nên trường câu chuẩn tên **`target_instruction`**,
trong khi `infer_branch.py` và `score_run.py` đều đọc **`gold_instruction`** (khuôn của `test.jsonl`).
Cùng nội dung, khác tên. Vá tại chỗ, không phải upload lại 808 MB:

```python
import json, os
VD = "/kaggle/working/valdata"; os.makedirs(VD, exist_ok=True)

for t in ("val_cham400.jsonl", "val_cham600.jsonl"):
    src = f"{DATA}/{t}"
    if not os.path.exists(src):
        continue
    n = 0
    with open(f"{VD}/{t}", "w", encoding="utf-8") as f:
        for l in open(src, encoding="utf-8"):
            r = json.loads(l)
            r.setdefault("gold_instruction", r["target_instruction"])
            f.write(json.dumps(r, ensure_ascii=False) + "\n"); n += 1
    print(t, n, "bước")

for ten in ("images", "ocr.jsonl"):                # symlink, không copy 767 MB
    d = f"{VD}/{ten}"
    if not os.path.exists(d):
        os.symlink(f"{DATA}/{ten}", d)

r = json.loads(open(f"{VD}/val_cham400.jsonl", encoding="utf-8").readline())
assert "gold_instruction" in r, "⛔ chưa thêm được trường"
assert os.path.exists(os.path.join(VD, r["image"])), "⛔ symlink ảnh hỏng"
print("\n✅ valdata sẵn sàng:", VD, sorted(os.listdir(VD)))
```

⇒ **Từ ô 4 trở đi dùng `--data-root VD`**, không phải `DATA`.

⭐ **Sửa tận gốc cho lượt sau:** để `tach_val.py` ghi thêm `gold_instruction` (và `app`,
`app_seen_in_train` nếu cần lát cắt theo app) ngay lúc tách, rồi dựng lại gói. Chừng nào chưa làm
thì ô 2b này là bắt buộc.
⚠️ Khác biệt đầy đủ giữa hai khuôn: val **thiếu** `gold_instruction` · `app` · `app_seen_in_train`;
val **thừa** `target_instruction` · `w` · `h`. Hai script chỉ cần `gold_instruction`.

---

### Ô 3 — hàm chạy và in nhịp sống

```python
import subprocess, time, os

def chay(lenh, log):
    print(">>", " ".join(str(x) for x in lenh), flush=True)
    t0 = time.time()
    with open(log, "w") as f:
        p = subprocess.Popen([str(x) for x in lenh], stdout=f, stderr=subprocess.STDOUT,
                             cwd=WS, start_new_session=True,
                             env={**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1"})
        while p.poll() is None:
            time.sleep(120)
            print(f"   {(time.time()-t0)/60:5.1f} phút · log {os.path.getsize(log)/1024:.0f} KB",
                  flush=True)
    print(f"   mã thoát {p.returncode} · {(time.time()-t0)/60:.1f} phút", flush=True)
    print(open(log).read()[-1500:])
    assert p.returncode == 0, "⛔ lỗi, đọc log ở trên"
```

⛔ `start_new_session=True` bắt buộc, và ⛔ **đừng** dùng `capture_output=True`: nó im lặng hàng
giờ và bạn không phân biệt được *đang chạy* với *đã treo*.
⛔ **`tqdm` phải tắt** — ngoài terminal nó in mỗi cập nhật thành một dòng, Kaggle chặn log khi vượt
trần và tiến trình kẹt cứng (đã mất 7 giờ vì chuyện này).

### Ô 4 — probe 8 bước TRƯỚC khi cam kết cả lượt

```python
chay(["python", "harness/infer_branch.py",
      "--adapter", f"{AD}/adapter_ref_min",
      "--data-root", VD, "--recs-file", "val_cham400.jsonl",
      "--limit", 8, "--out", "/kaggle/working/probe.jsonl"],
     "/kaggle/working/probe.log")
print(open("/kaggle/working/probe.jsonl").readline()[:300])
```

⚠️ **Kiểm dòng `[dữ liệu] …`** trong log — đó là chỗ duy nhất xác nhận đang đọc `val_cham400.jsonl`
chứ không phải `test.jsonl`. Ô này cũng cho biết **mỗi bước tốn bao lâu** ⇒ nhân 607 để ước cả lượt.

### Ô 5 — chấm mốc MIN (~1,2 h, **chưa đo**, lấy giờ thật từ Ô 4 mà tính)

```python
chay(["python", "harness/infer_branch.py", "--adapter", f"{AD}/adapter_ref_min",
      "--data-root", VD, "--recs-file", "val_cham400.jsonl",
      "--out", "/kaggle/working/preds_min.jsonl"], "/kaggle/working/infer_min.log")

chay(["python", "harness/score_run.py", "--mode", "score",
      "--preds", "/kaggle/working/preds_min.jsonl",
      "--data-root", VD, "--recs-file", "val_cham400.jsonl",
      "--out", "/kaggle/working/score_min.json"], "/kaggle/working/score_min.log")
```

### Ô 6 — chấm `step03200`, rồi đọc

```python
chay(["python", "harness/infer_branch.py", "--adapter", f"{AD}/vissft_step03200",
      "--data-root", VD, "--recs-file", "val_cham400.jsonl",
      "--out", "/kaggle/working/preds_vissft3200.jsonl"], "/kaggle/working/infer_v.log")

chay(["python", "harness/score_run.py", "--mode", "score",
      "--preds", "/kaggle/working/preds_vissft3200.jsonl",
      "--data-root", VD, "--recs-file", "val_cham400.jsonl",
      "--out", "/kaggle/working/score_vissft3200.json"], "/kaggle/working/score_v.log")

import json
a = json.load(open("/kaggle/working/score_min.json"))
b = json.load(open("/kaggle/working/score_vissft3200.json"))
print("MIN-DESC        :", a)
print("VIS-SFT step3200:", b)
```

---

## E. Đọc kết quả — luật khoá trước, đừng nới

| chênh (VIS-SFT − MIN) | làm gì |
|---|---|
| **thấp hơn quá 3,0 điểm** | ⛔ **dừng lượt A100**, lượt đã hỏng |
| thấp hơn dưới 3,0 điểm | ✅ **chạy tiếp** — mới ở 41% lượt, và phép so vốn bất lợi cho VIS-SFT |
| ngang hoặc cao hơn | ✅ chạy tiếp, và đây là **bằng chứng mạnh** vì thắng dù bị thiên vị ngược |

⭐ Công chấm không phí: `step03200` nằm trong năm điểm mà A6 sẽ chấm sau lượt, nên chạy hết lượt
thì đã có sẵn 1 trong 5.
⚠️ Ước ~1,2 h mỗi adapter là **suy từ tỉ lệ** với lượt 4.463 bước (5,6 h), **chưa đo lần nào**.
Ô 4 cho số thật.
