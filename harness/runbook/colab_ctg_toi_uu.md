# CTG-GRPO — dùng hết GPU đã thuê mà vẫn đúng: hướng dẫn từng bước (4/10/2026)

Làm **trước** lượt train thật (`colab_ctg_train.md`). Tốn khoảng **1,5 h A100 + 0,5 h L4** để đo, đổi lại
chọn được phương án rẻ nhất cho ~30–60 giờ GPU phía sau.
Mã: `harness/ctg_grpo.py` md5 `332765b7c3657c1117ada5bf6ea3b936` (cờ `--no-gc`, `--dai-nhat`, dòng `[máy]`).

---

## 1. Nguyên tắc: tối ưu chỗ nào mà không đổi kết quả

### Không được đổi (đổi là đổi thuật toán)
- Mỗi bước cập nhật = **2 câu nhắc × 8 câu sinh = 16 câu**. Mã `assert bs × accum = 16`.
- G, lr, β, nhiệt độ, độ dài tối đa, số bước, đích `p_k`.
- **A3 và A2 phải cùng cấu hình máy**, vì A3 − A2 là phép so chính.

### Đổi được, kết quả toán học như nhau (đọc từ mã TRL 0.29.1)
| núm | vì sao không đổi kết quả | kỳ vọng |
|---|---|---|
| micro-batch `bs` 4 → 8 → 16 (accum 4 → 2 → 1) | loss `dapo` chia cho tổng token của cả lượt sinh 16 câu (`grpo_trainer.py:1616, 2238`); thứ tự câu nhắc và lượt sinh không đổi; chỉ lệch làm tròn bf16 | +5–20% tốc độ [suy] |
| tắt gradient checkpointing (`--no-gc`) | chỉ bỏ lần tính lại forward lúc backward | +20–30% tốc độ nếu đủ VRAM [suy] |
| **chạy 2 nhánh chung một GPU** | hai tiến trình độc lập, không chia sẻ gì ngoài GPU | tận dụng lúc GPU rỗi (lúc sinh từng token, tính thưởng, nạp ảnh); thông lượng chung kỳ vọng 1,2–1,6× [suy] |
| lưu mỗi 50 bước thay vì 250 | lưu không đụng tới phép tính | mất máy chỉ mất ≤ 49 bước (~40 phút) thay vì ≤ 249 bước (~3 h) |
| tự trả máy khi xong (`TAT_MAY`) | không đụng tới phép tính | lượt xong lúc nửa đêm không đốt tiền tới sáng |

### ✅ Đã kiểm bằng thí nghiệm (CPU, 4/10) — `harness/kiem_tuong_duong_ctg.py`

Cùng 2 bước CTG-GRPO (A3) trên mô hình tí hon, fp32, SGD, so trọng số LoRA sau train với mốc `bs4×4, có gc`:

| cấu hình | lệch tối đa so với mốc | đọc |
|---|---|---|
| `bs8×2`, có gc | 6e-9 | làm tròn số thực ⇒ cùng phép train |
| `bs16×1`, có gc | 6e-9 | như trên |
| `bs4×4`, **tắt gc** | **0** | trùng tuyệt đối |
| A2 (tắt CTG), `bs4×4` | **4,5e-3** (≈ 1/3 cỡ trọng số đã học) | CTG thật sự đổi phép train ⇒ phép kiểm đủ nhạy |

`ctg_log` (λ, ĉ, lực đẩy) trùng nhau ở mọi cấu hình A3. Giới hạn: mô hình tí hon chữ thuần, không ảnh; trên
GPU bf16 sai số làm tròn lớn hơn 6e-9 nhưng vẫn là làm tròn.

### Vì sao không làm những thứ khác
- **Thời gian nằm ở đâu** (P0): câu sinh chỉ 5–10 token, nên khâu sinh rẻ. Phần đắt là forward/backward
  trên 16 chuỗi dài ~1.000–2.000 token (ảnh + câu nhắc). 8 câu cùng câu nhắc thì ảnh và câu nhắc bị tính
  lại 8 lần. Dùng chung phần đầu đó sẽ nhanh gấp nhiều lần, nhưng phải viết lại lõi TRL, dễ sai mà không
  báo lỗi ⇒ **không làm**.
- **vLLM:** đổi đường sinh, cài trên Colab rủi ro, mà khâu sinh vốn không phải chỗ đắt.
- **RAM máy (CPU):** không phải nút cổ chai (dữ liệu 2,7 GB). Bật High-RAM chỉ để chạy 2 nhánh an toàn.
- **Flash-attention 2:** phải biên dịch trên Colab; `sdpa` mặc định đã đủ.

---

## 2. Chuẩn bị (một lần, máy nhà + Drive)

1. Kiểm `_bundles/ctg-grpo-script/` có đủ 6 tệp:
   ```
   332765b7c3657c1117ada5bf6ea3b936  ctg_grpo.py
   07ea87b6d156d1faa391a4274dffd7cf  grpo_spice.py
   619e63e123a6dbf60086e65ee94a3912  build_branch_data.py
   9bf0b84145458fd55919a5e161b9766f  metric_exec.py
   828ce31811540195c34ecdbdee85d863  kl_ck500_theo_buoc.json
   24df52354e73710069be027fe9db03c6  ctg_s1_dich.json
   ```
2. Google Drive: tạo `MyDrive/thesis/ctg/`, kéo vào cả thư mục `ctg-grpo-script/` và
   `_bundles/fgrb_p1_bundle.zip` (2,7 GB).

---

## 3. Phiên A100 dò (~1,5 h): một lần duy nhất

Mở Colab → *Runtime → Change runtime type* → **A100**, bật **High-RAM**. Dán và chạy **Ô C1, C2, C3** của
`colab_ctg_train.md` (C1 để nguyên mặc định). **Không** chạy C4–C6.

Ghi lại **số đơn vị/giờ** của A100 (góc phải → *View resources*, hoặc trang *Usage*). Đừng dùng số nhớ.

### Ô T0 — hàm chạy thử (dán một lần)

```python
import subprocess, time, shutil, os, re
def thu(ten, bs, acc, nogc, arm="A3", buoc=10, cung=None):
    """Chạy `buoc` bước trên 12 câu nhắc DÀI NHẤT (ca tốn bộ nhớ nhất). Trả (s/bước, sinh s/bước, đỉnh GiB) hoặc 'OOM'."""
    out, log = f"/content/probe_{ten}", f"/content/probe_{ten}.log"
    shutil.rmtree(out, ignore_errors=True)
    cmd = ["python", "ctg_grpo.py", "--train", "--arm", arm, "--no-q4", "--bundle", BUNDLE, "--merged", MERGED,
           "--out", out, "--max-steps", str(buoc), "--save-steps", "1000000", "--dai-nhat", "12", "--dich", DICH,
           "--bs", str(bs), "--accum", str(acc)] + (["--no-gc"] if nogc else [])
    return subprocess.Popen(cmd, cwd=W, stdout=open(log, "w"), stderr=subprocess.STDOUT, start_new_session=True,
                            env={**os.environ, "TQDM_DISABLE": "1", "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}), log

def doi(ds):
    t0 = time.time(); peak = 0
    while any(p.poll() is None for p, _ in ds.values()):
        time.sleep(30)
        g = subprocess.run("nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader,nounits",
                           shell=True, capture_output=True, text=True).stdout.split(",")
        peak = max(peak, int(g[0])); 
        print(f"  {(time.time()-t0)/60:4.1f} phút · GPU dùng {int(g[0])/1024:.1f} GiB · {g[1].strip()}% · " +
              " | ".join(f"{t}: {([l for l in open(lg, errors='ignore') if l.startswith('[máy]')] or ['…'])[-1][6:70].strip()}"
                         for t, (_, lg) in ds.items()), flush=True)
    kq = {}
    for t, (p, lg) in ds.items():
        L = open(lg, errors="ignore").read()
        m = re.findall(r"\[máy\] bước (\d+) · ([\d.]+) s/bước · sinh ([\d.]+) s/bước .*?đỉnh VRAM ([\d.]+) GiB", L)
        kq[t] = "OOM" if ("OutOfMemory" in L or "out of memory" in L) else \
                ((float(m[-1][1]), float(m[-1][2]), float(m[-1][3])) if m else f"lỗi, xem {lg}")
        shutil.rmtree(f"/content/probe_{t}", ignore_errors=True)
    print("đỉnh GPU (nvidia-smi, cả máy):", round(peak / 1024, 1), "GiB")
    return kq
```

### Ô T1 — dò cấu hình lô, mỗi lần một tiến trình (~1 h)

```python
CFG = [("bs4_acc4_gc", 4, 4, False),      # cấu hình P0, làm mốc
       ("bs8_acc2_gc", 8, 2, False),
       ("bs16_acc1_gc", 16, 1, False),
       ("bs4_acc4_nogc", 4, 4, True),
       ("bs8_acc2_nogc", 8, 2, True)]     # dễ tràn nhất, chạy sau cùng
KQ1 = {}
for ten, bs, acc, nogc in CFG:
    KQ1.update(doi({ten: thu(ten, bs, acc, nogc)}))
    print("==", ten, KQ1[ten], flush=True)
print("\ncấu hình · (s/bước bước 6–10, sinh s/bước, đỉnh VRAM GiB)")
for k, v in KQ1.items(): print(" ", k, v)
```

Mỗi cấu hình ~8–12 phút. `OOM` là kết quả, không phải lỗi; ô tự chạy cấu hình kế.

**Chọn `TOT`:** s/bước nhỏ nhất với đỉnh VRAM **≤ 36 GiB**. Nếu nhanh hơn mốc `bs4_acc4_gc` dưới 5% thì
giữ mốc (đã chạy thật ở P0, ít rủi ro). s/bước ở đây đo trên câu nhắc dài nhất nên chậm hơn lượt thật;
chỉ dùng để so với nhau.

### Ô T2 — thử 2 nhánh chung một GPU (~15 phút)

Sửa `BS, ACC, NOGC` thành cấu hình vừa chọn. Nếu đỉnh VRAM một mình của cấu hình đó > 17 GiB thì thử với
`bs4_acc4_gc` (2 tiến trình phải vừa 40 GB).

```python
BS_, ACC_, NOGC_ = 4, 4, False          # ← cấu hình TOT ở T1 (hoặc bs4_acc4_gc nếu TOT > 17 GiB)
KQ2 = doi({"chung_A3": thu("chung_A3", BS_, ACC_, NOGC_, arm="A3"),
           "chung_A2": thu("chung_A2", BS_, ACC_, NOGC_, arm="A2")})
print(KQ2)
```

### Ô T3 — tính tiền, chọn phương án

```python
DV_A100 = 0.0        # ← đơn vị/giờ của A100 đọc trên Colab lúc này
DV_L4   = 0.0        # ← đơn vị/giờ của L4 (điền sau mục 4; để 0 nếu chưa đo)
S_L4    = 0.0        # ← s/bước của L4 ở cùng cấu hình (mục 4)
BUOC = 2000          # A3 + A2 = 2 × 1000 bước

def kiem(ten, s_buoc_moi_nhanh, so_nhanh_chung, dv):
    gio_gpu = BUOC * s_buoc_moi_nhanh / so_nhanh_chung / 3600     # giờ máy phải thuê cho cả hai nhánh
    gio_tuong = BUOC / 2 * s_buoc_moi_nhanh / 3600                 # mỗi nhánh 1000 bước, hai nhánh chạy cùng lúc
    print(f"{ten:42} {gio_gpu:5.1f} h máy · {gio_gpu*dv:6.0f} đơn vị · xong sau ~{gio_tuong:4.1f} h")

tot = min((v for v in KQ1.values() if isinstance(v, tuple) and v[2] <= 36), key=lambda v: v[0])
kiem("A100, mỗi nhánh 1 phiên (2 phiên song song)", tot[0], 1, DV_A100)
if all(isinstance(v, tuple) for v in KQ2.values()):
    s2 = max(v[0] for v in KQ2.values())
    kiem("A100, 2 nhánh chung 1 phiên", s2, 2, DV_A100)
if S_L4 and DV_L4:
    kiem("L4, mỗi nhánh 1 phiên (2 phiên song song)", S_L4, 1, DV_L4)
print("⚠️ s/bước đo trên câu nhắc dài nhất ⇒ giờ thật ngắn hơn; dùng để SO phương án, không để hứa giờ.")
```

Chọn dòng **ít đơn vị nhất**. Giờ chờ chênh nhau không quá vài giờ thì ưu tiên tiền.

---

## 4. Phiên L4 dò (~30 phút)

1. Phiên mới, **L4**. Chạy Ô C1, C2, C3 của `colab_ctg_train.md`, rồi Ô T0.
2. Chạy T1 với `CFG` chỉ gồm `bs4_acc4_gc` và cấu hình `TOT` của A100 (nếu đỉnh ≤ 20 GiB).
   Ngưỡng VRAM của L4: **≤ 20 GiB** (~22,5 GB dùng được).
3. Ghi `S_L4` (s/bước nhanh nhất vừa đo) và đơn vị/giờ của L4 vào Ô T3 (chạy lại T3 ở phiên A100, hoặc
   tính tay). Luật CLAUDE.md: **L4 chậm ≤ 1,5 lần A100 thì chọn L4**; Ô T3 so luôn bằng tiền thật.
4. Không thử 2 nhánh chung trên L4: 2 × ~12 GiB đã sát 22,5 GB.

---

## 5. Chạy thật

Gửi Claude bảng T1, T2, T3 để chốt, rồi theo một trong ba cách:

| phương án | làm gì |
|---|---|
| **2 nhánh chung 1 phiên A100** | 1 notebook `colab_ctg_train.md`, Ô C1: `ARMS = {"A3": 1000, "A2": 1000}` |
| **mỗi nhánh 1 phiên** (A100 hoặc L4) | 2 notebook (*File → Save a copy*), Ô C1: một bản `ARMS = {"A3": 1000}`, bản kia `{"A2": 1000}` |
| đợt 2 (A4, A7), sau K1/K2 ở bước 500 | như trên với `{"A4": 500, "A7": 500}` |

Ở **mọi** bản: `BS, ACC, NO_GC` = cấu hình đã chốt (giống hệt nhau), `SAVE = 50`, `TAT_MAY = True`.

---

## 6. Theo dõi máy khi train

Ô C6 in mỗi 2 phút dòng `GPU <%>, <MiB dùng>, <MiB tổng>` và dòng `[máy]` của từng nhánh, ví dụ:

```
 3.20 h · GPU 92 %, 30120 MiB, 40960 MiB · nhánh đang chạy ['A3', 'A2']
[A3] bước 260/1000 (tiếp từ 0) …
      [máy] bước 260 · 41.3 s/bước · sinh 6.2 s/bước (15%) · đỉnh VRAM 13.40 GiB · đang giữ 15.02 GiB
```

| thấy | nghĩa | làm gì |
|---|---|---|
| GPU % thường < 60% khi chạy 1 nhánh | GPU rỗi nhiều | lần sau chạy 2 nhánh chung |
| `sinh` > 50% thời gian | khâu sinh là nút cổ chai (trái dự đoán) | gửi Claude |
| MiB dùng > 38.000 trên A100 | sát trần | để chạy; OOM thì xem dòng dưới |
| `⛔ có Traceback/OOM` ở một nhánh | lô nặng tràn bộ nhớ | đợi C6 kết thúc (máy tự trả), mở lại với `ARMS` chỉ nhánh đó và `BS, ACC, NO_GC = 4, 4, False`; tự chạy tiếp từ điểm lưu (≤ 49 bước mất). Ghi lại bước đổi cấu hình để khai |

Đổi cấu hình lô giữa chừng vì OOM không làm hỏng phép so A3 − A2: hai cấu hình cho cùng phép tính, chỉ
lệch làm tròn bf16.
