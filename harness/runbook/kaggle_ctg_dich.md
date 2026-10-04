# CTG-GRPO — hiệu chỉnh đích `p_k` trên câu nhắc train (Kaggle T4, 4/10/2026)

Lý do: `report/278` §3. Đích khoá trước lấy trên val C1 (scroll 0,837 · type 0,813 · back 0,733), nhưng
CTG so `ĉ_k` với đích trên **câu nhắc train**. Nếu S1 ở train cao hơn đích thì λ tự tắt sớm và A3 ≈ A2.
Đo: S1 lấy 8 mẫu ở nhiệt độ 1,0 (y như lúc GRPO sinh) trên 440 câu nhắc train thuộc ba lớp
(scroll 242 · type 114 · back 84), đếm tỉ lệ câu đúng loại. Đổi đích là **đổi tham số khoá trước sau
khi thấy P0**, user đồng ý 4/10, phải khai.

T4, 0 đồng, ước **30–60 phút** [chưa đo].

## Chuẩn bị

1. Kaggle → dataset `ctg-grpo-script` → **New Version**: thay `ctg_grpo.py` bằng bản trong
   `_bundles/ctg-grpo-script/` (md5 `5be2bf98713a1ba6d76ed0a7684fe201`).
2. Dùng lại notebook P0 (cùng input), chọn version dataset mới nhất. Trong Ô 2 sửa md5 `ctg_grpo.py`
   thành `5be2bf98713a1ba6d76ed0a7684fe201`.
3. Chạy **Ô 1 → Ô 4** của `kaggle_ctg_p0.md` (gói · đường dẫn · hoà S1 · hàm `chay`). Bỏ Ô 5, Ô 6.

## Ô D1 — thử 10 câu nhắc

```python
rc = chay(["python", "ctg_grpo.py", "--do-dich", "--no-q4", "--bundle", BUNDLE, "--merged", MERGED,
           "--n-dich", "10", "--out", f"{W}/dich_thu.jsonl"], f"{W}/dich_thu.log", nhip=30)
print(open(f"{W}/dich_thu.log", errors="ignore").read()[-1500:])
print(open(f"{W}/dich_thu.jsonl").readline()[:600])
```

Phải thấy `[đích] 10 câu nhắc`, mã thoát 0, một dòng jsonl có `mau` gồm **8 câu khác nhau** (lấy mẫu
thật, không phải greedy lặp lại). Ghi lại số phút cho 10 câu ⇒ nhân 44 ra thời gian lượt đủ.

## Ô D2 — đủ 440 câu nhắc

```python
rc = chay(["python", "ctg_grpo.py", "--do-dich", "--no-q4", "--bundle", BUNDLE, "--merged", MERGED,
           "--out", f"{W}/ctg_s1.jsonl"], f"{W}/dich.log", nhip=120)
print("\n".join(l for l in open(f"{W}/dich.log", errors="ignore").read().splitlines() if l.startswith(("[đích]", "✅", "Traceback"))))
```

Ghi nối tiếp được: phiên đứt thì chạy lại Ô 1–4 và Ô D2 (nếu `ctg_s1.jsonl` còn trong `/kaggle/working`).
Lượt dài hơn ~1 h thì chạy dạng commit (*Save Version → Save & Run All*) với Ô D1 xoá đi.

Cuối log có ba dòng dạng:

```
[đích] scroll: 242 câu nhắc · đúng loại 0.xxx [lo; hi] · đích cũ (val C1) 0.837
[đích] type: 114 câu nhắc · đúng loại 0.xxx [lo; hi] · đích cũ (val C1) 0.813
[đích] navigate_back: 84 câu nhắc · đúng loại 0.xxx [lo; hi] · đích cũ (val C1) 0.733
✅ ghi /kaggle/working/ctg_s1_dich.json
```

## Ô D3 — tải về

```python
import shutil
from IPython.display import FileLink
Z = f"{W}/dich_out"; os.makedirs(Z, exist_ok=True)
for f in ("ctg_s1.jsonl", "ctg_s1_dich.json", "dich.log"):
    if os.path.exists(f"{W}/{f}"): shutil.copy(f"{W}/{f}", Z)
shutil.make_archive(Z, "zip", Z); os.chdir(W); FileLink("dich_out.zip")
```

Giải nén vào `runs/ctg/dich/`. Chép `ctg_s1_dich.json` vào `_bundles/ctg-grpo-script/` **và** lên Drive
`MyDrive/thesis/ctg/ctg-grpo-script/` (Ô C2 của `colab_ctg_train.md` bắt buộc có tệp này).
