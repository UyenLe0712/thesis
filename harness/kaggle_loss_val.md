# Chấm LOSS VAL cho lưới điểm lưu VIS-SFT — Kaggle T4, 0 đồng (viết 10/9/2026)

Bù cho việc lượt VIS-SFT chạy `do_eval: false` nên không có đường cong loss val. Không phải dừng
lượt A100, và phủ được cả phần đã chạy qua.

⚠️ **Loss val KHÔNG thay được `exec`** — dùng để **chẩn đoán quá khớp** và **thu hẹp vùng** cần
chấm `exec` ở A6. ⛔ Không chọn điểm lưu cuối bằng loss val. ⛔ Không trích số val ra báo.

---

## A. WSL — ✅ ĐÃ LÀM SẴN 10/9, không phải chạy lại

`_bundles/thesis_lossval.zip` (**255 MB**) đã dựng, gồm:

| trong gói | nội dung |
|---|---|
| `branches_val400/s1.json` | **607 mẫu**, dựng qua chính `build_branch_data.py` nên khuôn mẫu khớp lượt dạy |
| `branches_val400/dataset_info.json` | khai báo nhánh `gui_s1` |
| `images/` | **607 ảnh**, 253,7 MB |
| `harness/loss_val_grid.py` | script chấm |

⚠️ Đường dẫn ảnh trong `s1.json` cố tình để placeholder **`__IMG__/`** — Ô 1 thay bằng đường mount
thật của Kaggle. Đường mount Kaggle có hai tầng phụ không đoán trước được, nên đừng ghim tay.

Dựng lại (nếu cần):
```bash
python3 harness/build_branch_data.py --recs-file val_cham400.jsonl \
    --out harness/dg1_cache/train_ac/branches_val400 --img-prefix "__IMG__/"
```

---

## B. Lấy adapter khỏi Drive — làm trong **Terminal Colab**, không đụng lượt train

⛔ **Không chạy ô notebook nào** — nhân Python đang bận ô G7 nên ô mới chỉ xếp hàng, và phản xạ kế
tiếp thường là bấm Stop, đúng cái đã giết một lượt train hôm 2/9. Terminal là tiến trình riêng.

```bash
cd /content/drive/MyDrive/thesis/ckpt/vissft_seed101
du -sh grid/step*  | head -3          # xem cỡ một điểm lưu
ls grid | wc -l                        # đã có bao nhiêu
```

Chọn **bội của 500** cho nhẹ, rồi đóng gói ở chế độ *store* (safetensors nén cũng không nhỏ đi):

```bash
cd /content/drive/MyDrive/thesis/ckpt/vissft_seed101
mkdir -p /content/lv && rm -rf /content/lv/*
for d in grid/step*; do
  b=$(echo $d | grep -oE '[0-9]+$' | sed 's/^0*//')
  if [ $((b % 500)) -eq 0 ]; then cp -r "$d" /content/lv/; fi
done
ls /content/lv
cd /content && zip -0 -qr /content/drive/MyDrive/thesis/lossval_adapters.zip lv
ls -la /content/drive/MyDrive/thesis/lossval_adapters.zip
```

Rồi tải `lossval_adapters.zip` từ Google Drive về máy (qua drive.google.com, **không** qua ô Colab).

⚠️ `cp` trên Drive FUSE có thể chậm; nếu `ls /content/lv` thiếu thư mục thì chạy lại vòng lặp.

---

## C. Upload hai dataset lên Kaggle

| dataset mới | upload | cỡ |
|---|---|---|
| `thesis-lossval` | `_bundles/thesis_lossval.zip` | 255 MB |
| `thesis-lossval-adapters` | `lossval_adapters.zip` vừa tải về | tuỳ số điểm lưu |

⭐ Kaggle tự bung `.zip` khi tạo dataset.
⛔ **Tạo dataset MỚI, đừng dùng "New Version" của dataset cũ** — New Version *thêm* thư mục chứ
không thay thế, nên nhiều gói cùng tồn tại trong `/kaggle/input` và ô dò sẽ chọn mò (bài học 5/9).

Notebook: **Settings → Accelerator → GPU T4 x2**, Internet **ON** (cần tải mô hình nền).

---

## D. Notebook Kaggle — bốn ô

### Ô 0 — gỡ `torchao`, cài LLaMA-Factory (⛔ ô ĐẦU TIÊN, kể cả khi chạy lại)

```python
!pip uninstall -y -q torchao
!pip install -q -U "transformers>=4.49" accelerate peft bitsandbytes datasets pyyaml
!git clone -q https://github.com/hiyouga/LLaMA-Factory /kaggle/working/LLaMA-Factory
!cd /kaggle/working/LLaMA-Factory && git checkout -q c4e09c7cbe18844816af9e18a97fe465515edbcd
!pip install -q -e "/kaggle/working/LLaMA-Factory[torch,metrics]"
!cd /kaggle/working/LLaMA-Factory && git rev-parse HEAD
import importlib.util, torch
print("torchao còn:", importlib.util.find_spec("torchao"), "← phải None")
print("GPU:", torch.cuda.get_device_name(0), "| bf16:", torch.cuda.is_bf16_supported())
```

⚠️ `torchao 0.10.0` cài sẵn trên Kaggle làm `peft` ném `ImportError` **ngay lúc gắn LoRA**, tức sau
khi đã tải xong mô hình nền. Gỡ trước.
⚠️ `bf16: False` là **đúng** — T4 là Turing. Script tự đổi fp16.
⛔ SHA phải in đúng `c4e09c7cbe18…`, khác bản là khác hành vi.

### Ô 1 — dò mount, dựng workspace, thay `__IMG__`

```python
import glob, os, json, shutil

def tim(ten):
    r = sorted(glob.glob(f"/kaggle/input/**/{ten}", recursive=True))
    assert r, f"⛔ không thấy {ten} trong /kaggle/input — kiểm hai dataset đã Add chưa"
    return r[0]

S1   = tim("branches_val400/s1.json")
SCR  = tim("loss_val_grid.py")
IMG  = os.path.dirname(tim("images/ep18169_s1.png"))          # thư mục ảnh thật
ADP  = os.path.dirname(os.path.dirname(tim("step*/adapter_config.json")))
print("s1.json :", S1); print("script  :", SCR)
print("ảnh     :", IMG); print("adapter :", ADP)

WS = "/kaggle/working/lv"; os.makedirs(f"{WS}/branches_val400", exist_ok=True)
os.makedirs(f"{WS}/harness", exist_ok=True)
shutil.copy2(SCR, f"{WS}/harness/loss_val_grid.py")
shutil.copy2(os.path.join(os.path.dirname(S1), "dataset_info.json"),
             f"{WS}/branches_val400/dataset_info.json")

d = json.load(open(S1, encoding="utf-8"))
for r in d:
    r["images"] = [p.replace("__IMG__/images", IMG) for p in r["images"]]
json.dump(d, open(f"{WS}/branches_val400/s1.json", "w", encoding="utf-8"), ensure_ascii=False)

print("\nmẫu:", len(d), "← cần 607")
print("ảnh mẫu:", d[0]["images"][0])
assert os.path.exists(d[0]["images"][0]), "⛔ đường dẫn ảnh sai sau khi thay"
thieu = [r for r in d if not os.path.exists(r["images"][0])]
assert not thieu, f"⛔ thiếu {len(thieu)} ảnh"
print("điểm lưu:", sorted(os.listdir(ADP)))
print("\n✅ workspace sẵn sàng")
```

⛔ Phép `assert` phủ **toàn bộ 607 ảnh**, không chỉ ảnh đầu — đúng bài học của bản vá P5: hỏng
đường dẫn ảnh chỉ nổ ra **sau khi đã nạp xong mô hình**, tức muộn hàng chục phút.

### Ô 2 — chấm **một** điểm lưu trước, đừng cam kết cả lượt

```python
import subprocess, glob, os
b1 = sorted(glob.glob(f"{ADP}/step*"))[0]
print("thử điểm lưu:", b1)
!cd /kaggle/working/lv && python3 harness/loss_val_grid.py \
    --grid {ADP} --branches /kaggle/working/lv/branches_val400 \
    --every 100000 --out /kaggle/working/lossval_thu.json 2>&1 | tail -20
```

⚠️ `--every 100000` là mẹo để **không** khớp bước nào; nếu muốn thử đúng một cái thì đặt `--every`
bằng chính số bước của điểm lưu đầu (ví dụ `--every 500` khi điểm đầu là `step00500`).
Ô này cho biết **mỗi điểm lưu tốn bao lâu** ⇒ nhân lên để biết cả lượt.

### Ô 3 — chấm đủ (nối tiếp được, chạy lại là bỏ qua bước đã có)

```python
!cd /kaggle/working/lv && python3 harness/loss_val_grid.py \
    --grid {ADP} --branches /kaggle/working/lv/branches_val400 \
    --every 500 --out /kaggle/working/loss_val_grid.json 2>&1 | tail -40
```

### Ô 4 — đọc và tải về

```python
import json
kq = json.load(open("/kaggle/working/loss_val_grid.json"))
for b in sorted(kq, key=int):
    print(f"bước {int(b):5d} · loss val {kq[b]['eval_loss']:.4f}")
```

---

## E. Đọc kết quả

| hình dạng | nghĩa |
|---|---|
| giảm đều tới cuối | chưa quá khớp; vùng chấm `exec` nên nghiêng về các điểm lưu muộn |
| **quay đầu tăng** ở bước X | quá khớp từ X ⇒ chấm `exec` quanh vùng trước X |
| phẳng từ giữa | phần train về sau không thêm gì ⇒ lượt hạt 202 có thể cắt ngắn |

⭐ Nếu điểm lưu tốt nhất theo `exec` **lệch hẳn** khỏi cực tiểu loss val, đó là **số đo mới đáng vào
bài**: cùng họ với hệ số truyền 0,028, thêm bằng chứng rằng thước thay thế không dự đoán được thước
quyết định.

⚠️ **Chưa chạy thật lần nào.** Phần quét lưới và dựng cấu hình của `loss_val_grid.py` đã thử trên
WSL; phần `run_exp` với `eval_dataset` cần T4 mới xác nhận được. Ô 2 tồn tại chính vì lý do đó.
