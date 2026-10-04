# P1 — probe action/role/zone từ hidden state đóng băng của S1 — Kaggle T4, 0 đồng — viết 27/9/2026

Theo đúng tài liệu `harness/tai_lieu_2026-09-27/230_ACTION_PROBE_FGRB_CHO_CHAT_LAM_27_9.md`. Ba đầu
vào (adapter S1/101, ảnh train, OCR train) đã kiểm đủ, mẫu 4.000 (seed 101) và val 1.567 đã khoá
trước (`report/207_KET_QUA_PROBE_FGRB_27_9.md`, cập nhật sau khi P1 chạy).

**Việc của lượt này CHỈ LÀ P1**: đo xem hidden state lớp cuối của S1 (đóng băng, không sinh câu)
có dự đoán được action/role/zone không. Không train FGRB, không đụng test.

## A. Tạo dataset (máy nhà)

1. Tải lên Kaggle file `_bundles/fgrb_p1_bundle.zip` (~2,7 GB, gồm 5.567 ảnh + OCR lọc sẵn + 4.000
   dòng mẫu train + 1.567 dòng val + adapter S1/101) → **New Dataset**, tên `fgrb-p1-bundle`.
2. Tải thêm `_bundles/fgrb_p1_script.zip` (6,4 KB, chỉ chứa `p1_probe_fgrb.py`, đóng riêng để khỏi
   phải copy-paste code vào cell — tránh lỗi `%%writefile` thiếu filename đã gặp 27/9) → **New
   Dataset**, tên `fgrb-p1-script`.
3. Notebook mới → **Add Data**: cả `fgrb-p1-bundle` lẫn `fgrb-p1-script`.
4. **Settings → Accelerator: GPU T4 ×1 · Internet: ON** (cần tải Qwen2.5-VL-3B-Instruct từ
   HuggingFace, ~7 GB — không có trong bundle vì đã có sẵn trên Hub).

## B. Ô lệnh

### Ô 0 — cài thư viện, rồi Restart session

```
!pip install -q -U transformers peft accelerate torchao
```

⚠️ **`torchao` bắt buộc phải có trong lệnh này** — đo thật 27/9: nâng `peft` mà không nâng
`torchao` thì Kaggle giữ nguyên bản `torchao 0.10.0` có sẵn trong image, còn `peft` mới đòi
`torchao >= 0.16.0` ở NGAY BƯỚC NẠP ADAPTER (dù không dùng tính năng nào của torchao), ném
`ImportError: Found an incompatible version of torchao`. Sau khi chạy ô này **bắt buộc Restart
session** rồi mới chạy tiếp — cài xong mà không restart thì bản cũ vẫn còn trong bộ nhớ kernel.

### Ô 1 — dò đường dẫn dataset

⚠️ **Đã đo thật 27/9: đường dẫn KHÔNG phải `/kaggle/input/fgrb-p1-bundle`.** Notebook mới của
Kaggle mount dataset qua `/kaggle/input/datasets/<tên_kaggle_của_bạn>/<dataset-slug>/`, cộng thêm
một cấp thư mục `fgrb_p1_bundle/` từ chính cấu trúc bên trong zip. Đường dẫn thật đo được:
`/kaggle/input/datasets/trangphngngc/fgrb-p1-bundle/fgrb_p1_bundle`. Vì đường dẫn có thể đổi theo
tài khoản/phiên bản Kaggle, dùng ô tự dò sau thay vì gõ tay:

```python
import os
BUNDLE = None
for root, dirs, files in os.walk("/kaggle/input"):
    if "adapter_s1_seed101" in dirs and "images" in dirs:
        BUNDLE = root
        break
assert BUNDLE, "Khong tim thay bundle — kiem tra da Add Data dataset fgrb-p1-bundle chua"
print("BUNDLE =", BUNDLE)
for name in ["images", "ocr.jsonl", "p1_train_rows.jsonl", "p1_val_rows.jsonl",
             "adapter_s1_seed101"]:
    p = os.path.join(BUNDLE, name)
    print(name, "OK" if os.path.exists(p) else "THIEU", p)
print("so anh:", len(os.listdir(BUNDLE + "/images")))
```

Kỳ vọng: cả 5 mục đều `OK`, số ảnh = 5.567. Lệch thì dừng, đừng chạy tiếp. Dùng biến `BUNDLE` này
làm giá trị `--bundle` ở mọi ô dưới đây (không phải chuỗi cố định `/kaggle/input/fgrb-p1-bundle`).

### Ô 2 — chép script P1 vào working dir

Script tự chứa (chỉ dùng thư viện chuẩn + torch/transformers/peft/PIL, không phụ thuộc file nào
khác của harness), lấy thẳng từ dataset `fgrb-p1-script` — khỏi copy-paste code:

```python
import os, shutil
SCRIPT = None
for root, dirs, files in os.walk("/kaggle/input"):
    if "p1_probe_fgrb.py" in files:
        SCRIPT = os.path.join(root, "p1_probe_fgrb.py")
        break
assert SCRIPT, "Khong tim thay p1_probe_fgrb.py — kiem tra da Add Data dataset fgrb-p1-script chua"
shutil.copy(SCRIPT, "/kaggle/working/p1_probe_fgrb.py")
print("Da copy tu", SCRIPT)
```

⚠️ Nếu script trong `harness/p1_probe_fgrb.py` được sửa sau này, phải đóng lại
`_bundles/fgrb_p1_script.zip` và **New Version** cho dataset `fgrb-p1-script` (không phải tạo
dataset mới) rồi mới chạy lại ô này.

### Ô 2.5 — THỬ NHANH TRƯỚC, đừng bỏ qua

Chạy `--limit 5` để bắt lỗi rẻ (vài phút) trước khi cam kết 5–6 giờ GPU cho lượt thật. Dùng biến
`BUNDLE` đã dò ở Ô 1 (cú pháp `{BUNDLE}` là nội suy biến Python của Jupyter trong lệnh `!`):

```
!python p1_probe_fgrb.py --bundle {BUNDLE} --cache-out /kaggle/working/_test5 --limit 5
```

Kỳ vọng: chạy hết không lỗi, in ra dòng `⚠️ --limit 5 ĐANG BẬT`, rồi hai lượt trích hidden state
(5 dòng train, 5 dòng val), rồi 30 epoch, rồi bảng P1 (số vô nghĩa vì mẫu quá nhỏ — **bỏ qua số,
chỉ cần thấy chạy hết không crash**). Lỗi hay gặp nếu có: sai tên cột ảnh, thiếu token ảnh trong
`input_ids` (báo `RuntimeError: Khong tim thay token anh...`), hết VRAM (thử `--limit 1` xem có
qua không, nếu không thì báo lại, đừng tự ý đổi cấu hình model).

### Ô 3 — chạy P1 thật (đủ 4.000 + 1.567, không limit)

```
!python p1_probe_fgrb.py --bundle {BUNDLE} --cache-out /kaggle/working/_fgrb_probe
```

Ước lượng theo tài liệu 230: khoảng 5–6 giờ trên T4 cho 5.567 forward pass (không sinh câu, chỉ
một lần forward mỗi bước) — nhiều khả năng NHANH HƠN vì không cần vòng lặp `generate()` nhiều
bước, chỉ một forward. Script in tiến độ mỗi 200 bước kèm ETA; nếu đứt phiên, chạy lại Ô 3 —
script tự phát hiện cache `_fgrb_probe/hiddens_train_seed101.pt` và `hiddens_val_seed101.pt`, bỏ
qua bước forward nếu đã có (**đọc kỹ**: `--cache-out` mặc định trỏ `/kaggle/working`, mất khi hết
phiên nếu không tải về hoặc không dùng chế độ commit — xem mục C bên dưới).

## C. Chạy bằng "commit" (Save & Run All) — ĐƯỢC, và nên dùng cho lượt 5–6 giờ này

Có thể chạy Ô 3 bằng **Save Version → Save & Run All (Commit)** thay vì bấm từng ô tương tác, y
hệt cách đã làm ở `kaggle_commit_sel_4_9.md` trước đây — máy chạy nền, không cần giữ trình duyệt
mở, output mọi cell (kể cả log tiến độ) được lưu lại, mở lại xem khi nào xong cũng được.

Hai điều đã xử lý sẵn trong script để commit an toàn (bài học từ lượt treo 7 giờ vì log ngập,
`harness/runbook/kaggle_pheA_CHAY_LAI.md`):

- Đã tắt thanh tiến trình tqdm của HuggingFace (`HF_HUB_DISABLE_PROGRESS_BARS=1`,
  `TRANSFORMERS_VERBOSITY=error`) trước khi import transformers — nếu không, lượt tải
  Qwen2.5-VL-3B (~7 GB, vì Internet ON) sẽ in hàng nghìn dòng log tiến độ, đúng nguyên nhân từng
  làm treo một lượt commit khác.
- Script chỉ in một dòng mỗi 200 bước (không dùng tqdm ở bất kỳ đâu trong vòng lặp của chính nó).

Việc cần làm trước khi commit: **chạy Ô 2.5 (thử `--limit 5`) ở chế độ tương tác trước**, thấy
chạy hết không lỗi rồi mới Save & Run All cho Ô 3. Đừng commit thẳng lượt thật mà chưa thử —
lỗi (nếu có) chỉ lộ ra sau khi commit chạy xong hoặc time-out, tức mất vài giờ mới biết.

⚠️ Kaggle giới hạn một phiên GPU (kể cả commit) khoảng 9–12 giờ tuỳ thời điểm — ước lượng 5–6 giờ
của lượt này nằm trong giới hạn đó, nhưng nếu commit bị Kaggle cắt giữa chừng (hiếm), cache đã ghi
ở `/kaggle/working/_fgrb_probe/*.pt` **không** sống sót qua giữa hai lần commit khác nhau (mỗi
commit là một container mới, không giữ trạng thái của lần trước) — phải chạy lại Ô 3 từ đầu ở
lượt commit kế. Muốn nối tiếp thật thì tải file `.pt` về máy sau khi trích xong rồi upload lại
làm input cho lượt sau, hoặc chạy tương tác (giữ session sống) thay vì commit nếu lo bị cắt.

### Ô 4 — đọc kết quả

Output của Ô 3 tự in đủ mọi thứ mục 6 và Phụ lục B của tài liệu 230 yêu cầu:

- accuracy/recall-khác-NONE/macro-F1 của role và zone trên val;
- accuracy và majority của action;
- epoch được chọn và macro-F1 trung bình lúc chọn;
- 8 ví dụ role sai + 8 ví dụ đúng;
- phán quyết P1 ĐẠT/TRƯỢT theo ba ngưỡng đã khoá (recall role ≥50%, recall zone ≥30%, accuracy
  action ≥73,9%).

**Copy nguyên văn output của Ô 3** (từ dòng `train.jsonl` đầu tiên tới dòng `P1 = ...` cuối cùng)
gửi lại — đó là thứ cần để viết file kết quả cuối theo mục 6 của tài liệu 230.

## D. CHẠY LẠI PHẦN HEAD — sửa 28/9, KHÔNG cần GPU (dùng cache đã trích)

Lượt 27–28/9 train ba head **full-batch, không chuẩn hoá, Adam lr 1e-3** ⇒ 30 epoch chỉ có 30 bước
cập nhật, head chưa hội tụ và kết quả đổi theo lần khởi tạo ngẫu nhiên (chạy lại đúng cấu hình đó
cho action 72,69 thay vì 80,60). Script nay mặc định: **chuẩn hoá z-score theo train · minibatch 64
(1.890 bước cập nhật) · AdamW lr 1e-4, weight decay 1e-2 · seed head 101**. Mẫu 4.000, seed lấy
mẫu 101, val 1.567, tối đa 30 epoch, trọng số lớp, luật chọn epoch và ba ngưỡng **giữ nguyên**.
Chi tiết và số đo: `report/207` §9.

Có cache thì script **không nạp Qwen**, chỉ train head ⇒ chạy trên CPU khoảng 10 giây.

### D.1 Trên máy nhà (WSL) — cách khuyên dùng

```
cd /mnt/d/Master/Thesis
mkdir -p ~/fgrb_p1/bundle
unzip -o -q "harness/results (3).zip" -d ~/fgrb_p1                  # ra ~/fgrb_p1/_test5/*.pt
unzip -o -j -q _bundles/fgrb_p1_bundle.zip "*/p1_train_rows.jsonl" "*/p1_val_rows.jsonl" -d ~/fgrb_p1/bundle
PYTHONIOENCODING=utf-8 ~/.venvs/thesis/bin/python harness/p1_probe_fgrb.py \
    --bundle ~/fgrb_p1/bundle --cache-in ~/fgrb_p1/_test5 --cache-out ~/fgrb_p1/out
```

Kỳ vọng ở dòng đầu: `Dung cache co san, khoi nap model va forward lai` và
`head: standardize=True batch=64 ... => 1890 buoc cap nhat`. Không thấy hai dòng đó thì dừng
(tức là đang chạy cấu hình cũ hoặc đang đi nạp model). Kết quả seed 101: role 51,54 · zone 30,51 ·
action 82,83 · `P1 = DAT`.

Các cờ đối chứng (chạy thêm, **không** dùng để phán P1):

| cờ | để làm gì |
|---|---|
| `--head-seed 102` (103, 104, 105) | xem kết quả có bền theo seed khởi tạo head không |
| `--shuffle-labels` | xáo nhãn train ⇒ mức recall do đoán tràn, head không học được gì thật |
| `--zone-coarse` | gộp 31 cách viết zone về lưới 3×3 ⇒ đo nhận vị trí, không đo đoán đúng cách viết |
| `--batch-size 0 --no-standardize --lr 1e-3 --weight-decay 0` | tái lập cách train của lượt 27/9 |

### D.2 Trên Kaggle (nếu muốn chạy ở đó) — session **CPU**, không tốn quota GPU

1. Đóng lại script: `cd harness && zip ../_bundles/fgrb_p1_script.zip p1_probe_fgrb.py` (đã làm 28/9,
   21.128 byte) → **New Version** cho dataset `fgrb-p1-script`.
2. Notebook mới, **Accelerator: None**, Internet không cần. Add Data: `fgrb-p1-bundle`,
   `fgrb-p1-script`, và **output của notebook P1 cũ** (Add Data → Your Work → notebook đó) — output
   ấy chứa `_test5/hiddens_*.pt`.
3. Chạy Ô 1 và Ô 2 như trên, rồi:

```python
import os
CACHE = None
for root, dirs, files in os.walk("/kaggle/input"):
    if "hiddens_train_seed101.pt" in files and "hiddens_val_seed101.pt" in files:
        CACHE = root
        break
assert CACHE, "Khong thay cache — kiem tra da Add Data output cua notebook P1 cu chua"
print("CACHE =", CACHE)
```
```
!python p1_probe_fgrb.py --bundle {BUNDLE} --cache-in {CACHE} --cache-out /kaggle/working/_fgrb_probe
```

⚠️ Không cần `pip install` ở Ô 0 vì không nạp model. Nếu dòng đầu **không** in
`Dung cache co san` thì dừng ngay: script đang đi tải Qwen và trích lại 3 giờ.

## Không được làm ở lượt này

- Không mở `test.jsonl` hay bất kỳ file điểm test nào — script không đọc, đừng thêm.
- Không đổi `n_train_probe=4000` hay `seed=101` dù thấy accuracy thấp.
- Không chạy P2 (sinh câu trên val) trước khi có kết quả P1 và biết P1 ĐẠT.
- Không train LoRA, không đụng tập test.
