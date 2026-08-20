# Upload dataset lên Kaggle — từng bước

Khâu chấm cần **đúng bốn thứ**. Thiếu một là hoặc chết ngay, hoặc tệ hơn: chạy trơn mà ra số sai.

| cần gì | ở đâu | vì sao |
|---|---|---|
| mã `harness/` | trong gói | `score_run.py` · `metric_exec.py` · `a11y_inventory.py` |
| `test.jsonl` **đã gắn nhãn** | trong gói | `score_run.py:405` đọc `app_seen_in_train` thẳng từ đây; bản chưa gắn ⇒ lát cắt phụ rỗng |
| **4.463 ảnh** bước chạm | trong gói | mỗi bước một ảnh màn hình |
| tệp `preds_*` cần chấm | upload riêng | thứ đem đi chấm |
| **Internet = On** | panel notebook | tải UGround ~4 GB + `all_forest_dict.zip` 452 MB từ HuggingFace |

⚠️ Ảnh trong `test_ac/images` ở máy có **6.969** tệp (3,3 GB) nhưng gói chỉ lấy **4.463** ảnh
bước chạm — phần còn lại là bước gõ/cuộn, khâu chấm không đụng tới. Đừng upload cả thư mục.

---

## Bước 1 — dựng gói ở máy nhà

```bash
python harness/make_bundle.py score
```

Ra `thesis_score.zip` ở gốc kho. Kiểm trước khi upload:

```bash
python3 - <<'PY'
import zipfile, json
z = zipfile.ZipFile("thesis_score.zip")
n = z.namelist()
img = [x for x in n if x.endswith(".png")]
t = [x for x in n if x.endswith("test_ac/test.jsonl")]
print(f"{len(n)} tệp · {len(img)} ảnh (cần 4.463)")
r = [json.loads(l) for l in z.open(t[0]).read().decode().splitlines()]
print(f"test.jsonl {len(r)} dòng (cần 6.958) · có nhãn app: {'app_seen_in_train' in r[0]}")
print("score_run.py:", [x for x in n if x.endswith('score_run.py')])
PY
```

Ba dòng này bắt đúng ba lỗi đã mắc: thiếu ảnh · `test.jsonl` chưa gắn nhãn · gói mã bản cũ.

---

## Bước 2 — tạo dataset trên Kaggle

**Cách A — qua trình duyệt** (không cần cài gì):

1. Vào **kaggle.com/datasets** → **New Dataset** (nút xanh, góc trên phải).
2. Kéo `thesis_score.zip` vào ô upload. Kaggle **tự bung zip** sau khi tải xong.
3. Đặt tên: `thesis-score`. Ghi lại **slug** hiện ở URL (`<tài-khoản>/thesis-score`).
4. Để **Private**. Bấm **Create**.
5. Đợi Kaggle xử lý — 1,7 GB mất khoảng **10–25 phút** tuỳ đường truyền. Trang hiện "Processing"
   rồi mới sang "Ready".

**Cách B — qua dòng lệnh** (nhanh và nối lại được nếu đứt):

```bash
pip install kaggle
# lấy token: kaggle.com → ảnh đại diện → Settings → API → Create New Token
# tải về kaggle.json rồi:
mkdir -p ~/.kaggle && mv ~/Downloads/kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json

mkdir -p /tmp/ds && cp thesis_score.zip /tmp/ds/
cat > /tmp/ds/dataset-metadata.json <<'JSON'
{ "title": "thesis-score", "id": "TAI-KHOAN/thesis-score",
  "licenses": [{"name": "CC0-1.0"}] }
JSON
kaggle datasets create -p /tmp/ds --dir-mode zip
```

Thay `TAI-KHOAN` bằng tên tài khoản Kaggle. Cách B đáng dùng hơn cho 1,7 GB.

---

## Bước 3 — dataset thứ hai cho các tệp `preds`

Tách riêng vì nó **nhỏ và thay đổi liên tục** — mỗi lần có nhánh mới chỉ cần thêm version vài
MB, không phải tải lại 1,7 GB.

Đã đóng sẵn thành **một tệp**: `_bundles/preds_upload.zip` — 12 tệp, nén còn **805 KB**.
Kaggle tự bung zip nên kéo một tệp là đủ, khỏi chọn tay từng cái.

Dựng lại nếu cần:

```bash
mkdir -p _bundles/preds_upload
cp runs/preds_s1_seed202.jsonl runs/paraphrase/preds_para_*.jsonl \
   runs/floor/preds_f*.jsonl _bundles/preds_upload/
cd _bundles && zip -qj preds_upload.zip preds_upload/*.jsonl
```

`zip -j` đóng **phẳng**, không kèm thư mục con, nên sau khi Kaggle bung thì các tệp nằm ngay
gốc dataset — ô nối dữ liệu dò đệ quy nên kiểu nào cũng tìm ra, nhưng phẳng thì nhìn danh sách
tệp trên Kaggle dễ hơn.

**New Dataset** → tên `thesis-preds` → Private → Create. Xong trong một phút.

**Lần sau thêm tệp:** vào dataset → **New Version** → kéo tệp mới vào, **giữ nguyên tệp cũ** →
Create. Rồi trong notebook, panel **Input** bấm cập nhật lên version mới — **quên bước này là
notebook vẫn dùng bản cũ mà không báo gì.**

---

## Bước 4 — gắn vào notebook

1. Mở notebook → panel phải → **Input** → **Add Input**.
2. Tab **Datasets** → tìm `thesis-score` và `thesis-preds` → **Add** cả hai.
3. Cùng panel, đặt:
   - **Accelerator** = **GPU T4 ×2**
   - **Internet** = **On** ← thiếu cái này thì chết ở dòng nạp mô hình, sau khi đã tốn thời gian khởi động

Kiểm bằng một ô:

```python
import glob
for d in sorted(glob.glob("/kaggle/input/*")): print(d)
print("test.jsonl :", glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True))
print("ảnh        :", len(glob.glob("/kaggle/input/**/test_ac/images/*.png", recursive=True)))
print("score_run  :", glob.glob("/kaggle/input/**/harness/score_run.py", recursive=True))
print("preds sàn  :", glob.glob("/kaggle/input/**/preds_f*.jsonl", recursive=True))
```

Đủ cả bốn dòng thì sang `harness/kaggle_cham_san.md` bước 2.

---

## Ba lỗi đã mắc thật, đừng lặp lại

**1. Nối nhầm `test.jsonl` 300 dòng.** Ô nối dữ liệu bản đầu lấy `test.jsonl` **đầu tiên tìm
thấy** — hoá ra là bản 300 dòng của cổng A nằm trong dataset khác, ghép với ảnh của gói này.
Chạy trơn, ra một con số trông bình thường, nhưng chấm trên lát không so được với mốc nào.
⇒ Ô nối dữ liệu hiện tại đòi **cùng một gói** phải có **cả** ≥6.900 dòng **lẫn** ≥4.400 ảnh.

**2. Gói mã trên dataset là bản cũ.** Đã xảy ra **hai lần** (12/8 và 13/8), cả hai lần lộ ra
muộn. Bản vá đã có ở máy nhà nhưng gói upload từ trước đó ⇒ chạy bằng luật chấm cũ.
⇒ Ô 0 có `assert len(score_run.py) > 34000`.

**3. Quên bấm cập nhật version trong panel Input.** Upload version mới xong mà không cập nhật
thì notebook vẫn đọc bản cũ, **không có cảnh báo nào**.
