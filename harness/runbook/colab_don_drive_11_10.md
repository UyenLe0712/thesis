# Kiểm kê Drive trước khi dọn (11/10/2026)

Mục đích: liệt kê mọi thứ trong `MyDrive/thesis`, kèm dung lượng và md5 của các adapter/zip,
để đối chiếu với bản đã có trên máy WSL / GitHub Release rồi mới quyết xoá.
**Ô này CHỈ ĐỌC, không xoá gì.**

Runtime: **CPU** (Runtime → Change runtime type → CPU). Không cần GPU, 0 đơn vị.

## Ô K1 — kiểm kê

```python
import os, hashlib, time, sys
from google.colab import drive
drive.mount('/content/drive')

GOC = '/content/drive/MyDrive'
THESIS = f'{GOC}/thesis'
CAC_GOC = [THESIS, f'{GOC}/thesis_ckpt']   # thesis_ckpt = lượt LoRA tháng 7 (faithful)
OUT = f'{THESIS}/_kiem_ke_drive_11_10.tsv'

def md5(p, lim=2 * 2**30):
    if os.path.getsize(p) > lim:
        return 'BO_QUA_>2GB'
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''):
            h.update(b)
    return h.hexdigest()

# 1) cấp gốc MyDrive: chỉ tên + dung lượng, để biết có gì ngoài thư mục thesis
print('== MyDrive cấp gốc ==', flush=True)
for n in sorted(os.listdir(GOC)):
    print('  ', n, flush=True)

# 2) dung lượng theo thư mục (sâu tối đa 3 cấp dưới thesis)
tong = {}
rows = []
t0 = time.time()
for root, dirs, files in (w for g in CAC_GOC if os.path.isdir(g) for w in os.walk(g)):
    for fn in files:
        p = os.path.join(root, fn)
        try:
            st = os.stat(p)
        except OSError:
            continue
        rel = os.path.relpath(p, GOC)
        parts = rel.split('/')
        for k in range(1, min(len(parts), 3) + 1):
            key = '/'.join(parts[:k]) + ('' if k == len(parts) else '/')
            tong[key] = tong.get(key, 0) + st.st_size
        rows.append((rel, st.st_size, time.strftime('%Y-%m-%d', time.localtime(st.st_mtime))))
    if len(rows) % 2000 < len(files):
        print(f'  ... đã duyệt {len(rows)} tệp, {time.time()-t0:.0f}s', flush=True)

print(f'\n== Tổng: {sum(r[1] for r in rows)/2**30:.2f} GB, {len(rows)} tệp ==', flush=True)
print('\n== Thư mục cấp 1–2 (GB) ==', flush=True)
for k, v in sorted(tong.items(), key=lambda x: -x[1]):
    if k.count('/') <= 3 and v > 20 * 2**20:
        print(f'{v/2**30:8.2f}  {k}', flush=True)

# 3) md5 cho adapter + zip + tar (để so với bản trên máy nhà)
print('\n== md5 adapter/zip (có thể mất vài phút) ==', flush=True)
with open(OUT, 'w') as f:
    f.write('duong_dan\tbyte\tngay\tmd5\n')
    for rel, sz, ngay in sorted(rows):
        m = ''
        if rel.endswith(('adapter_model.safetensors', '.zip', '.tar', '.tar.gz')):
            m = md5(os.path.join(GOC, rel))
            print(f'{sz/2**20:9.1f} MB  {m}  {rel}', flush=True)
        f.write(f'{rel}\t{sz}\t{ngay}\t{m}\n')
print('\nĐã ghi', OUT, flush=True)
```

Gửi lại cho Claude: **toàn bộ phần in ra** của ô K1, hoặc tải tệp
`MyDrive/thesis/_kiem_ke_drive_11_10.tsv` về đặt ở `runs/don_drive/`.

---

## Ô K2 — xoá theo nhóm (mặc định CHẠY THỬ, không xoá)

Đối chiếu md5 ngày 11/10 (`runs/don_drive/md5_may_nha.txt`):
- ck500 (`491fa66…`), MIN (`906d0bc…`), GRPO-point (`74a14ed…`), S1/101 (`0c60a44…`),
  gui_sel (`92795bf…`), ba nhánh final của 288, `tage-adapters.zip`, `tage_colab.zip`,
  `thesis_val_cham.zip` **trùng md5 với bản trên máy**. `fgrb_p1_bundle.zip` trùng dung lượng byte.
- **Chỉ có trên Drive:** adapter S1/202 (`ac0cac9…`), S2/101 (`bf7f294…`), CE2-S2 (`a981765…`)
  ⇒ ô này KHÔNG đụng tới, chỉ xoá checkpoint trung gian bên trong.

Cách chạy: chạy một lần với `XOA = False`, đọc danh sách, rồi đổi `XOA = True` chạy lại.
Sau đó **dọn Thùng rác của Drive** (drive.google.com → Thùng rác), vì tệp nằm trong thùng rác
vẫn tính vào dung lượng.

```python
import os, shutil, glob
T = '/content/drive/MyDrive/thesis'
XOA = False                       # đổi True để xoá thật
NHOM = {'A', 'C', 'D'}            # thêm 'B' nếu đồng ý xoá ảnh (tar ảnh dạy/kiểm)

A = [  # nhánh đã đóng + bản trung gian, kết quả đã nằm ở runs/
    'ctg', 'tage', 'ckpt/vissft_seed101', 'tok_cache_vissft', 'pata_ck', 'k1_adapter.zip',
    'ckpt_backup', 'ckpt/s1_seed101_ep1', 'ckpt/s1_seed202_ep1', 'branches_vi_0818',
    'derived.tar.gz', 'derived_train.tar.gz', 'thesis_pata_colab.zip', 'train_images.tar',
    'probe200.tar.gz', 'thesis_rented.zip',
]
B = ['train_images_p0.tar', 'train_images_p1.tar', 'train_images_p2.tar',
     'train_images_p3.tar', 'test_images.tar']
# C: checkpoint trung gian của 288, GIỮ final/ (trùng md5 máy nhà) và ck500/
C = [p[len(T)+1:] for p in glob.glob(f'{T}/nghe288/tiep_*_101/checkpoint-*')]
# D: checkpoint trung gian trong ckpt/, GIỮ adapter ở gốc hoặc final/ (= điểm lưu cuối, md5 trùng)
D = [p[len(T)+1:] for p in glob.glob(f'{T}/ckpt/*/checkpoint-*')
     if '/vissft_seed101/' not in p]

def co(p):
    q = f'{T}/{p}'
    if os.path.isfile(q): return os.path.getsize(q)
    return sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(q) for f in fs)

# chặn: thư mục ckpt/* phải còn adapter ở gốc thì mới xoá checkpoint con
for p in D:
    d = f'{T}/{p.rsplit("/", 1)[0]}'
    assert any(os.path.exists(f'{d}/{x}adapter_model.safetensors') for x in ('', 'final/')), \
        f'thiếu adapter cuối ở {d} — dừng'
for p in C:
    fin = f'{T}/{p.rsplit("/", 1)[0]}/final/adapter_model.safetensors'
    assert os.path.exists(fin), f'thiếu {fin} — dừng'

tong = 0
for ten, ds in [('A', A), ('B', B), ('C', C), ('D', D)]:
    if ten not in NHOM: continue
    for p in sorted(ds):
        if not os.path.exists(f'{T}/{p}'): continue
        s = co(p); tong += s
        print(f'[{ten}] {s/2**30:6.2f} GB  {p}', flush=True)
        if XOA:
            q = f'{T}/{p}'
            shutil.rmtree(q) if os.path.isdir(q) else os.remove(q)
print(f'\n{"ĐÃ XOÁ" if XOA else "SẼ XOÁ (chạy thử)"}: {tong/2**30:.2f} GB', flush=True)
```
