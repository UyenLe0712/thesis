# Chặng 4 — VIS-SFT trên Colab A100 (viết 9/9/2026) — TỰ ĐỦ, dán thẳng từng ô

Máy: **Colab A100**, trả tiền. Đây là **lượt A100 duy nhất** của cả kế hoạch.
Kế hoạch tổng: `report/152` §4. Nguồn khoa học: `report/151` §1.3 và §3.

| ô | việc | giá | dừng lại nếu |
|---|---|---|---|
| G1 | cài gói ▸ **Restart runtime** | ~6 phút | không thấy GPU · SHA sai · torch bản CPU |
| G2 | Drive, kho, dữ liệu, ảnh | ~15 phút | đường dẫn ảnh **không** bắt đầu bằng `/` · không in **63000 · 400 · 602 · 64.567** |
| G3 | tám phép tiền bay | 10 giây | bất kỳ `assert` nào đỏ |
| **G4** | **khẳng định TĨNH** — so hai lượt bật/tắt cờ | ~5 phút | hai số **bằng nhau** |
| **G4b** | bật cache mã hoá token | 5 giây | LLaMA-Factory báo không nhận khoá ⇒ gỡ dòng, chạy tiếp |
| G4c | dò `LogCallback` | 5 giây | chỉ chạy nếu G5 báo `ModuleNotFoundError` |
| **G5** | **smoke 200 bước** | **~3 h** (⚠️ đo thật 9/9: **~2,5 h mã hoá** + 33 phút train) | `grid/step00200/` không có 2 tệp |
| G6 | lượt thật, chạy nền | **20–37 h** | — |
| G7 | theo dõi, foreground suốt lượt | — | — |
| **G8** | **cắt lỗ** — hai điểm kiểm ở bước 3.200 và 4.800 | ~2 h T4, **0 đồng** | K1 thấp hơn mốc MIN quá **3,0 điểm** · K2 thấp hơn K1 quá **3,0 điểm** |

⭐ **Can thiệp duy nhất so với S1/101: `freeze_vision_tower: false`.** Mốc so là **59,11**.
⚠️ **Kỳ vọng ghi trước: P(vượt MDE 2,11) ≈ 0,30.** Bốn mắt xích giải thích đã vào luận văn rồi,
nên lượt này trắng cũng không làm chương 6 lung lay.

---

## ⛔ Bốn điều phải đọc trước

**① Dữ liệu phải là bộ ĐÃ TRỪ VAL.** `dataset_dir` trỏ `branches_tru_val` (63.000 mẫu), không
phải `branches` (64.567). Trỏ nhầm là huấn luyện trên chính tập dùng để chọn điểm lưu, mọi số val
sau đó đẹp một cách vô nghĩa, **không có gì báo lỗi**, và chỉ lộ ra khi chấm test.

**② `grid_callback.py` phải được ĐĂNG KÝ, không tự chạy.** Gọi `chay_vissft.py`, ⛔ đừng gọi
`llamafactory-cli train`. Gọi sai thì lượt chạy trơn tru, tốn đủ 20–37 h, và `grid/` **rỗng** —
mất trắng 40 quan sát dùng để chọn điểm lưu, không có lỗi nào báo.

**③ Đừng dùng `grad_norm` để kiểm cờ thị giác.** LoRA khởi tạo ma trận B bằng 0 nên gradient ở
những bước đầu bằng 0 **ngay cả khi dây nối đúng**. Dùng ô G4.

**④ `weight_decay` để nguyên 0.** Thêm nó là biến thứ hai, và mọi mức tăng thu được sẽ không tách
được phần nào do mở thị giác, phần nào do co chuẩn.

---

## Chuẩn bị ở nhà — hai tệp phải có trên `MyDrive/thesis/`

| tệp | có gì | cỡ · md5 |
|---|---|---|
| `vissft_data.tar.gz` | `branches_tru_val/` (4 nhánh × 63.000) + `val_cham400.jsonl` + `val_cham600.jsonl` | 49 MB · `dc7859c23da8` (**dựng lại 9/9 với đường dẫn ảnh tuyệt đối**) |
| `thesis_rented.zip` | gói mã, có `chay_vissft.py` · `grid_callback.py` · `khang_dinh_vissft.py` (**bản vá 9/9**) · `train_config_vissft.yaml` | 3,8 MB · ⛔ **không dùng md5** — gói chứa chính runbook này nên md5 đổi mỗi lần sửa; kiểm bằng nội dung ở ô G2 |
| `train_images_p*.tar` | ảnh dạy | ~12 GB, đã có từ lượt trước |

Và **một dataset Kaggle** cho hai ô chấm (G8 và A6), upload khi nào cần chứ không phải bây giờ:

| dataset | upload cái gì | cỡ · md5 |
|---|---|---|
| `thesis-val-cham` | `_bundles/thesis_val_cham.zip` — 1.567 ảnh + `val_cham400.jsonl` + `val_cham600.jsonl` + `ocr_val.jsonl` | 771 MB · `d28582c2d08a` |

⚠️ Đây là gói **khác** `thesis-val` của chặng 3. Gói cũ chỉ có 1.011 ảnh của val 262 bước chạm;
gói này có 1.567 ảnh của val mở rộng (400 và 602 bước chạm). Chấm A6 bằng gói cũ là chấm trên tập
nhỏ hơn và sai số lớn hơn.

---

## Ô G1 — cài gói ▸ rồi **Restart runtime**

```python
# ⭐ ĐẶT PHA TRƯỚC KHI CHẠY. Lượt này có HAI pha chạy trên HAI máy khác nhau:
#    "cpu" = pha mã hoá token (ô G5-CPU, 0 đơn vị) · "gpu" = pha train (ô G6, A100).
PHA = "cpu"          # ⬅ đổi thành "gpu" khi quay lại chạy G6

# ⛔ PHÉP RẺ NHẤT, ĐẶT TRƯỚC MỌI THỨ. Không có phép này thì lỗi "no GPU" chỉ nổ ở CUỐI ô G2,
#    tức sau khi đã bung 12 GB ảnh mất 15 phút — và đổi runtime lại xoá sạch, làm lại từ đầu.
import subprocess
r = subprocess.run("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader",
                   shell=True, capture_output=True, text=True)
print("GPU:", r.stdout.strip() or "(không có — đúng nếu PHA='cpu')")
if PHA == "gpu":
    assert r.returncode == 0 and r.stdout.strip(), (
        "⛔ DỪNG — máy ảo KHÔNG có GPU.\n"
        "   Runtime → Change runtime type → A100 → Save.\n"
        "   ⚠️ Việc đó khởi động lại máy ảo và XOÁ SẠCH /content ⇒ làm lại từ ô G1.")

!pip install -q -U "transformers>=4.49" accelerate peft bitsandbytes datasets \
    huggingface_hub pyarrow pillow pyyaml liger-kernel
# ⚠️ PIN đúng SHA đã dùng cho mọi lượt của dự án. LLaMA-Factory đổi hành vi giữa các bản
#    (một stack từng mất `loss`/`lr` khỏi trainer_log.jsonl), nên khác bản là hỏng phép so.
#    KHÔNG dùng --depth 1: bản clone nông không checkout được commit chỉ định.
!git clone https://github.com/hiyouga/LLaMA-Factory /content/LLaMA-Factory
!cd /content/LLaMA-Factory && git checkout c4e09c7cbe18844816af9e18a97fe465515edbcd
!pip install -q -e "/content/LLaMA-Factory[torch,metrics]"
!cd /content/LLaMA-Factory && git rev-parse HEAD    # phải in ĐÚNG c4e09c7cbe18…
import importlib.metadata as m, torch
print("liger-kernel:", m.version("liger_kernel"))
print("torch:", torch.__version__, "| CUDA build:", torch.version.cuda,
      "| khả dụng:", torch.cuda.is_available())
if PHA == "gpu":
    assert torch.version.cuda, (
        "⛔ DỪNG — pip vừa cài torch bản CPU-only, đè lên bản CUDA của Colab.\n"
        "   Sửa: !pip install -q -U torch --index-url https://download.pytorch.org/whl/cu124\n"
        "   rồi Restart runtime và chạy lại ô G1 từ đầu.")
```

**Kiểm bốn dòng:** `GPU:` có tên card · `git rev-parse HEAD` in đúng `c4e09c7cbe18…` ·
`liger-kernel` có số · `torch … CUDA build` **không phải None**.
⭐ **Với `PHA = "cpu"`** thì hai phép kiểm GPU được bỏ qua có chủ ý: dòng `GPU:` in `(không có)` và
`CUDA build` có thể là `None` — cả hai đều **đúng**, vì pha mã hoá không đụng GPU. Hai phép kiểm ấy
tự bật lại khi bạn đặt `PHA = "gpu"` để chạy G6.

⚠️ **Restart runtime**, rồi mới chạy ô G2.

---

## Ô G2 — Drive, kho, dữ liệu, ảnh

```python
from google.colab import drive; drive.mount('/content/drive')
import os, zipfile, glob, json, torch
D, WS = "/content/drive/MyDrive/thesis", "/content/ws"
os.makedirs(WS, exist_ok=True)
zipfile.ZipFile(f"{D}/thesis_rented.zip").extractall(WS)
REPO = f"{WS}/thesis"; os.chdir(REPO)
TR = f"{REPO}/harness/dg1_cache/train_ac"
dem = lambda d: len(os.listdir(d)) if os.path.isdir(d) else 0

# ── dữ liệu nhánh: bản CŨ trước, rồi bung ĐÈ bộ đã trừ val ────────────────────
!tar xzf {D}/derived.tar.gz -C {REPO}
assert os.path.exists(f"{D}/derived_train_en.tar.gz"), "⛔ thiếu derived_train_en.tar.gz"
!tar xzf {D}/derived_train_en.tar.gz -C {REPO}
assert os.path.exists(f"{D}/vissft_data.tar.gz"), "⛔ chưa upload vissft_data.tar.gz"
!tar xzf {D}/vissft_data.tar.gz -C {TR}

# ── ảnh dạy ──────────────────────────────────────────────────────────────────
os.makedirs(f"{TR}/images", exist_ok=True)
if dem(f"{TR}/images") >= 64567:
    print("ảnh dạy đã đủ — bỏ qua khâu bung")
else:
    for g in sorted(glob.glob(f"{D}/train_images_p*.tar")):
        !tar xf {g} -C {TR}/images

# ── gói mã phải là bản 9/9, không phải bản cũ trên Drive ──────────────────────
k = open(f"{REPO}/harness/khang_dinh_vissft.py").read()
assert "dem_tham_so" in k and "llamafactory-cli" in k, (
    "⛔ GÓI MÃ CŨ trên Drive. Bản trước của khang_dinh_vissft.py luôn báo ĐẠT kể cả khi cờ thị "
    "giác không có tác dụng. Upload lại _bundles/thesis_rented.zip rồi chạy lại ô này.")
i = open(f"{REPO}/harness/infer_branch.py").read()
assert "--data-root" in i and '"--alpha"' in i, "⛔ infer_branch.py chưa có bản vá P5/P7"
# ⛔ THÊM 9/9 SAU KHI ĐÃ LỌT MỘT LẦN: hai assert trên chỉ kiểm khang_dinh_vissft.py và
#    infer_branch.py, nên gói zip 9/9 vẫn có thể chứa chay_vissft.py BẢN CŨ — đúng chuyện đã
#    xảy ra lúc 15:03. Bản cũ import LogCallback từ đường không có ở SHA pin, và truyền CFG
#    dạng chuỗi cho run_exp. Kiểm luôn ở đây thay vì để lộ ra ở ô G6.
v = open(f"{REPO}/harness/chay_vissft.py").read()
assert "for duong in" in v and "yaml.safe_load(open(CFG" in v, (
    "⛔ chay_vissft.py BẢN CŨ. Ghi đè bằng bản 9/9 (ô %%writefile ở mục G6) rồi chạy lại ô này.")
assert "adapter_model" in open(f"{REPO}/harness/grid_callback.py").read(), (
    "⛔ grid_callback.py bản cũ hoặc thiếu")
print("gói mã   : bản 9/9 ✓ (gồm chay_vissft.py + grid_callback.py)")

# ── ĐƯỜNG DẪN ẢNH phải TUYỆT ĐỐI và mở được ─────────────────────────────────
# ⛔ Đây là chỗ đã hỏng ngày 9/9: bộ dữ liệu dựng thiếu --img-prefix nên ảnh ghi đường dẫn
#    TƯƠNG ĐỐI ("images/ep…png"). LLaMA-Factory mở ảnh theo thư mục làm việc, mà tiến trình
#    train chạy ở gốc kho ⇒ FileNotFoundError sau khi đã nạp xong model. Kiểm ở đây, 1 giây.
d0 = json.load(open(f"{TR}/branches_tru_val/s1.json"))
anh0 = d0[0]["images"][0]
print("đường dẫn ảnh:", anh0)
assert anh0.startswith("/"), (
    "⛔ ĐƯỜNG DẪN ẢNH TƯƠNG ĐỐI. Dựng lại ở máy nhà bằng:\n"
    "   python3 harness/build_branch_data.py --recs-file train_tru_val.jsonl \\\n"
    f"       --img-prefix {TR}/\n"
    "   rồi đóng gói và upload lại vissft_data.tar.gz.")
assert os.path.exists(anh0), f"⛔ ảnh đầu tiên không mở được: {anh0}"
print("ảnh mẫu   : mở được ✓")

# ── bốn con số phải đúng ──────────────────────────────────────────────────────
n = len(json.load(open(f"{TR}/branches_tru_val/s1.json")))
print("card     :", torch.cuda.get_device_name(0) if torch.cuda.is_available()
      else "CPU (đúng nếu đang chạy pha mã hoá)", "| lõi CPU:", os.cpu_count())
print("gui_s1   :", n, "← cần 63.000 (đã trừ 1.567 bước val)")
print("ảnh dạy  :", dem(f"{TR}/images"), "← cần 64.567")
for t in ("val_cham400.jsonl", "val_cham600.jsonl"):
    c = sum(1 for r in map(json.loads, open(f"{TR}/{t}", encoding="utf-8"))
            if (r.get("action") or {}).get("action_type") in ("click", "long_press"))
    print(f"  {t}: {c} bước chạm")
assert n == 63000, f"⛔ gui_s1 phải 63.000, thấy {n} — chưa bung vissft_data hoặc bung nhầm"
assert dem(f"{TR}/images") >= 64567, "⛔ thiếu ảnh dạy"
```

**Phải in:** `gói mã bản 9/9 ✓` · đường dẫn ảnh **bắt đầu bằng `/`** · `ảnh mẫu mở được ✓` · `gui_s1 63000` · `ảnh dạy 64567` · `val_cham400 400` · `val_cham600 602`.
⛔ `gui_s1` ra **64567** nghĩa là đang dùng bộ CHƯA trừ val — dừng, bung lại `vissft_data.tar.gz`.

---

## Ô G3 — tám phép tiền bay

```python
import yaml, os
CFG = f"{REPO}/harness/train_config_vissft.yaml"
c = yaml.safe_load(open(CFG))
# đường dẫn trong tệp là đường dẫn máy soạn; chốt lại theo máy này rồi ghi đè
c["dataset_dir"] = f"{TR}/branches_tru_val"
c["output_dir"]  = f"{D}/ckpt/vissft_seed101"
yaml.safe_dump(c, open(CFG, "w"), allow_unicode=True, sort_keys=False)

print("① freeze_vision_tower :", c["freeze_vision_tower"], " ← phải False")
print("② dataset             :", c["dataset"], " ← gui_s1")
print("③ dataset_dir         :", c["dataset_dir"])
print("④ weight_decay        :", c.get("weight_decay", "không khai (=0) ✓"))
print("⑤ adapter_name_or_path:", c.get("adapter_name_or_path", "không khai ✓"))
print("⑥ lora_target         :", c["lora_target"])
print("⑦ val_size / do_eval  :", c["val_size"], "/", c["do_eval"])
print("⑧ output_dir          :", c["output_dir"], "| đã có gì:",
      os.listdir(c["output_dir"]) if os.path.isdir(c["output_dir"]) else "(rỗng)")

assert c["freeze_vision_tower"] is False,       "⛔ cờ thị giác chưa mở"
assert "branches_tru_val" in c["dataset_dir"],  "⛔ phải trỏ bộ ĐÃ TRỪ VAL"
assert "weight_decay" not in c,                 "⛔ weight_decay phải để nguyên 0"
assert "adapter_name_or_path" not in c,         "⛔ không được khai adapter"
assert c["val_size"] == 0.0 and c["do_eval"] is False
assert c["quantization_bit"] == 4 and c["cutoff_len"] == 2560
print("\n✅ tám phép đạt")
```

⚠️ Ô này **ghi đè** hai đường dẫn trong tệp cấu hình cho khớp máy hiện tại; mọi khoá khác giữ
nguyên. `output_dir` trỏ thẳng Drive để mất máy giữa chừng vẫn còn điểm lưu.

---

## ⭐ Ô G4 — KHẲNG ĐỊNH TĨNH, chạy TRƯỚC bước 1 (0 bước train)

```python
!cd {REPO} && PYTHONIOENCODING=utf-8 python3 harness/khang_dinh_vissft.py
```

Ô này chạy **chính đường train thật hai lần**, một lần với cờ bật và một lần với cờ tắt, mỗi lần
đúng một bước trên tám mẫu, rồi so số tham số huấn luyện mà LLaMA-Factory tự in ra. Mất ~5 phút.

Phải in ba dòng và chữ **ĐẠT**:

```
  freeze_vision_tower = false :   xx.xxx.xxx tham số huấn luyện
  freeze_vision_tower = true  :   yy.yyy.yyy tham số huấn luyện
  chênh lệch                  :    z.zzz.zzz
```

⛔ **Hai số bằng nhau thì DỪNG HẲN.** Nghĩa là cờ không có tác dụng, và cả lượt 20–37 h sẽ chỉ
lặp lại S1 dưới một cái tên khác.

⚠️ **Phép so hai lượt này tự chứng, không cần mốc tuyệt đối nào.** Bản trước của ô G4 chỉ dựng
model bằng `get_peft_model` rồi đếm tensor `visual.*` — mà `gate_proj`/`up_proj`/`down_proj` cũng
có trong tháp thị giác nên PEFT luôn khớp chúng, và phép kiểm **luôn báo ĐẠT kể cả khi cờ không có
tác dụng**. Đó là loại lỗi nguy hiểm nhất: phép thử chưa hề diễn ra mà báo như đã diễn ra.

---

## ⭐ Ô G4b — bật cache mã hoá token (chạy TRƯỚC G5)

⛔⛔ **BÀI HỌC CHI PHÍ 9/9 — lượt sau đừng lặp lại.** Khâu mã hoá **không gọi GPU một giây nào**
(đo thật: GPU 0 %, bộ nhớ 428 MiB suốt 2,5 h) nhưng lượt 9/9 chạy nó trên **A100**, tức trả giá
bậc 3 cho việc của bậc 0. Bậc thang chọn máy của dự án đã ghi *"khâu nghẽn CPU/IO thì L4 ngang
A100"*.
⇒ **Thứ tự đúng cho mọi lượt sau** (hạt 202, hoặc bất kỳ lần đổi dữ liệu nào): chạy G1–G4b + G5
trên **T4 miễn phí hoặc runtime CPU** cho tới khi `tok_cache_vissft` nằm trên Drive, **rồi mới**
bật A100 và chạy thẳng G6. Tiết kiệm ~2,5 h A100 mỗi lần.
⚠️ Đổi giữa lượt đang chạy thì **lỗ**: phải mount lại Drive, bung lại 64.567 ảnh và mã hoá lại từ 0,
ăn hết phần định tiết kiệm. Quyết chọn máy **trước** khi bấm, đúng luật đã ghi ở `CLAUDE.md`.

⛔⛔ **KHÔNG BỎ QUA Ô NÀY.** Đo thật 9/9: khâu mã hoá mất **~2,5 h**, và lượt smoke đầu chạy khi
chưa bật G4b nên **toàn bộ 2,5 h ấy nằm ở đĩa local, mất theo máy ảo**. Hệ quả nếu để nguyên:
lượt thật trả lại 2,5 h, và **mỗi lần mất máy trong 20–37 h lại trả thêm 2,5 h nữa**.
⇒ Thứ tự đúng: **G4b trước, rồi mới G5**. Kiểm bằng một lệnh sau khi G5 đã sinh cấu hình:
`grep -i token /content/cfg_probe.yaml` — không ra dòng nào nghĩa là G4b chưa có tác dụng.

Khâu mã hoá token 63.000 mẫu mất **~2,5 h A100** — đo thật 9/9: ~420 dòng/phút, ~19,2 KB/dòng,
đích ~1,2 GB. ⚠️ Lượt tháng 8 ghi 42 phút cho 64.567 mẫu ở **cùng** `cutoff_len` 2560, nên chênh
lệch 3,5 lần này **chưa truy ra nguyên nhân** (CPU toàn máy chỉ 16 %, nghi khâu đọc ảnh nghẽn đĩa).
⛔ Đừng dùng con số 42 phút để lập kế hoạch; dùng số đo của chính lượt đang chạy. Khâu này mặc định
**lặp lại mỗi lần chạy**: smoke một
lần, lượt thật một lần, và thêm một lần cho **mỗi lần mất máy**. Lượt 20–37 h thì mất máy vài lần
là chuyện thường, nên khoản này cộng dồn có thể lên vài giờ.

LLaMA-Factory cho lưu kết quả mã hoá ra đĩa. Đặt nó **trên Drive** thì cả smoke, lượt thật và mọi
lần chạy tiếp đều dùng chung một bản.

```python
import yaml
c = yaml.safe_load(open(CFG))
c["tokenized_path"] = f"{D}/tok_cache_vissft"      # ⭐ trên Drive để sống qua mất máy
yaml.safe_dump(c, open(CFG, "w"), allow_unicode=True, sort_keys=False)
print("tokenized_path =", c["tokenized_path"])
```

✅ **Đây không phải biến khoa học** — chỉ là chỗ để bộ nhớ đệm, không đổi dữ liệu cũng không đổi
cách huấn luyện. Cấu hình vẫn lệch S1/101 đúng một biến là `freeze_vision_tower`.
⛔ **Nếu bản LLaMA-Factory đang pin không có khoá này**, nó sẽ báo lỗi ngay ở G5 — chưa tốn gì. Gỡ
dòng ấy ra rồi chạy tiếp bình thường, nhưng khi đó phải chấp nhận trả lại ~2,5 h cho mỗi lượt.
⚠️ **Bật rồi mà đổi dữ liệu thì phải xoá thư mục đệm**, nếu không nó dùng lại bản mã hoá cũ và bạn
train trên dữ liệu khác mà không có gì báo. Lượt này dữ liệu đã chốt nên không đụng tới.
⚠️ Tốn thêm **~1,2 GB** trên Drive (đo 9/9, không phải 0,5–1 GB như ước lượng ban đầu). Kiểm còn chỗ: `grid/` sẽ chiếm ~2,4 GB, điểm lưu ~0,4 GB.

---

## ⛔ Ô G4c — dò `LogCallback` (chạy nếu G5 báo `ModuleNotFoundError`)

`LogCallback` đổi chỗ giữa các bản LLaMA-Factory. Bản pin `c4e09c7cbe18` **không có**
`llamafactory.extras.callbacks`.

⭐ **Đo thật trên Colab ngày 9/9 — đường đúng là `llamafactory.train.callbacks`.** Năm mô-đun có
chữ *callback* trong bản pin: `llamafactory.train.callbacks` · `llamafactory.v1.core.utils.callback`
· `llamafactory.v1.utils.callbacks` (+ `.logging_callback`, `.trainer_callback`). Chỉ mô-đun đầu
có lớp `LogCallback`.

Ô dưới vẫn giữ để dò lại nếu đổi bản; chạy xong nó đặt biến `DUONG`.

```python
import importlib, pkgutil, llamafactory, os
tim = []
for m in pkgutil.walk_packages(llamafactory.__path__, "llamafactory."):
    if "callback" in m.name.lower():
        tim.append(m.name)
print("mô-đun có chữ 'callback':", tim)

DUONG = None
for d in tim + ["llamafactory.train.callbacks", "llamafactory.extras.misc"]:
    try:
        if hasattr(importlib.import_module(d), "LogCallback"):
            DUONG = d
            break
    except Exception:
        pass
print("⇒ LogCallback ở:", DUONG or "KHÔNG CÓ — sẽ chạy không kèm nó")
```

⚠️ `LogCallback` chỉ ghi `trainer_log.jsonl`. Không có nó thì cột `Drive` trong ô theo dõi luôn
`None`, còn tiến độ vẫn đọc được vì ô G7 lấy từ **log local**. Không ảnh hưởng kết quả huấn luyện.

⭐ `harness/chay_vissft.py` trong gói 9/9 **đã tự dò bốn đường** rồi mới quyết, nên ô G6 chạy được
mà không cần sửa gì. Chỉ `chay_probe.py` của ô G5 là phải vá, vì nó sinh ra tại chỗ:

```python
open("/content/chay_probe.py", "w").write(f'''
import sys, yaml
sys.path.insert(0, "{REPO}/harness")
from llamafactory.train.tuner import run_exp
from grid_callback import CopyAdapterToGrid
cbs = [CopyAdapterToGrid("{PROBE}/grid")]
try:
    import importlib
    cbs.append(importlib.import_module("{DUONG}").LogCallback())
except Exception as e:
    print("[LogCallback] bỏ qua:", e, flush=True)
run_exp(args=yaml.safe_load(open("/content/cfg_probe.yaml")), callbacks=cbs)
''')
print("đã vá chay_probe.py — chạy lại ô G5")
```

⚠️ Ô này cần `PROBE` và `REPO`; nếu chưa chạy ô G5 lần nào thì đặt trước:
`PROBE = "/content/probe_vissft"`.

---

## ⭐ Ô G5k — kiểm cache mã hoá TRƯỚC khi bấm G6 (10 giây, chặn 3 h A100)

Chạy sau G4b, ngay trước G6. Nếu G6 không nhận ra bản cache thì nó **mã hoá lại từ dòng 0 trên
A100** — đúng 3 giờ bậc 3 cho việc bậc 0 mà pha CPU vừa tránh được, và không có gì báo trước.

```python
import yaml, os, json
c = yaml.safe_load(open(CFG))
tp = c.get("tokenized_path")
print("tokenized_path :", tp)
assert tp, "⛔ chưa chạy G4b — thiếu khoá tokenized_path trong cfg"
assert os.path.isdir(tp), f"⛔ thư mục cache không có trên máy này: {tp}"
n = json.load(open(f"{tp}/train/dataset_info.json"))["splits"]["train"]["num_examples"]
gb = sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk(tp) for f in fs)/2**30
print("mẫu trong cache:", n, "← cần 63.000")
print("dung lượng     :", round(gb,2), "GB ← cần ~1,14")
print("tệp            :", sorted(os.listdir(f"{tp}/train")))
assert n == 63000, f"⛔ cache có {n} mẫu, không phải 63.000 — mã hoá nhầm bộ chưa trừ val"
assert os.path.exists(f"{tp}/train/state.json"), "⛔ thiếu state.json ⇒ lần lưu trước chưa trọn"
print("\n✅ cache hợp lệ, G6 sẽ bỏ qua pha mã hoá")
```

⛔⛔ **Rồi soi 3 phút đầu của G6.** Log **phải** có dòng nạp từ đĩa và **KHÔNG được** có
`Running tokenizer on dataset` hay `Converting format of dataset`. Thấy một trong hai dòng đó thì
**dừng ngay** (`pkill -f llamafactory`): nó đang mã hoá lại, mỗi phút để chạy tiếp là tiền A100 đổ
đi. Nguyên nhân thường gặp: `dataset_dir` hoặc `cutoff_len` đổi so với lúc mã hoá nên chữ ký cache
không khớp.

---

## Ô G5 — smoke 200 bước (~3 h)

⭐ **Ô này im lặng suốt phần mã hoá nếu bạn dùng bản cũ dùng `capture_output`.** Bản dưới
đây ghi ra tệp và in nhịp sống mỗi phút: `log KB` · `cache MB` · số mục trong thư mục ra. Cache
lớn dần nghĩa là đang mã hoá, chưa treo.
⭐ **Muốn soi kỹ hơn thì mở Terminal Colab và dán ô G5t bên dưới** — nó thêm cột `GPU`, tức cột duy nhất phân biệt được *đang mã hoá* với *đang train*.

⚠️ **Đừng ngạc nhiên vì nó lâu hơn 200 bước.** Khoảng **2,5 h đầu là mã hoá token** cho 63.000
mẫu, chưa train gì; sau đó mới tới 200 bước × ~10 s. Đo thật 9/9: ~420 dòng/phút, CPU toàn máy chỉ
~16 % ⇒ khâu này không nghẽn ở CPU.
⭐ **Đã bật G4b thì 2,5 h này chỉ tốn một lần**: lượt thật và mọi lần chạy tiếp đọc lại bản đã
mã hoá.
⛔ **Nhưng 200 bước train thì KHÔNG dùng lại được, và cũng không nên.** Smoke đặt `max_steps: 200`
nên Trainer trải lịch learning rate cho một lượt 200 bước, tức lr giảm gần về 0 ở cuối smoke; lượt
thật trải lịch trên 7.876 bước nên ở bước 200 lr vẫn gần đỉnh. Hai lượt đi qua lịch khác hẳn nhau,
nên trọng số sau smoke **không phải** là 200 bước đầu của lượt thật. Nối vào là hỏng đúng phép so
một biến mà lượt này sinh ra để chứng minh. Lượt thật bắt đầu từ bước 0, và ~33 phút train của
smoke là phí bảo hiểm — rẻ so với 20–37 h.
⛔ **Không giới hạn `max_samples` ở smoke.** Giới hạn thì s/bước đo được sẽ không phản ánh lượt
thật, mà con số ấy chính là thứ ô này sinh ra để đo.


```python
import shutil, yaml, subprocess, os, time
PROBE = "/content/probe_vissft"
shutil.rmtree(PROBE, ignore_errors=True)   # ⛔ KHÔNG xoá thì nó chạy tiếp từ điểm lưu cũ,
                                           #    nhảy qua 200 bước rồi chạy đúng một bước:
                                           #    log vẫn in "Training completed", trông y như đạt.
c = yaml.safe_load(open(CFG))
# ⛔⛔ CHẶN CỨNG: thiếu khoá này thì bản mã hoá nằm ở /root/.cache và MẤT THEO MÁY ẢO ⇒ lượt thật
#    lẫn mỗi lần mất máy đều trả lại ~2,5 h. Đã trả giá 9/9 (sự cố 7). Chạy ô G4b rồi quay lại.
assert "tokenized_path" in c, "⛔ CHƯA CHẠY Ô G4b — dừng, chạy G4b trước, đừng đốt 2,5 h"
c["output_dir"] = PROBE
c["max_steps"]  = 200
c["save_steps"] = 200
yaml.safe_dump(c, open("/content/cfg_probe.yaml", "w"), allow_unicode=True, sort_keys=False)

# ⚠️ KHÔNG import LogCallback thẳng: bản pin không có llamafactory.extras.callbacks.
#    Nếu ô này báo ModuleNotFoundError thì chạy ô G4c rồi quay lại.
open("/content/chay_probe.py", "w").write(f'''
import sys, yaml, importlib
sys.path.insert(0, "{REPO}/harness")
from llamafactory.train.tuner import run_exp
from grid_callback import CopyAdapterToGrid
cbs = [CopyAdapterToGrid("{PROBE}/grid")]
for d in ("llamafactory.train.callbacks", "llamafactory.extras.callbacks"):
    try:
        cbs.append(importlib.import_module(d).LogCallback()); break
    except Exception:
        pass
# run_exp nhận DICT, không nhận đường dẫn chuỗi
run_exp(args=yaml.safe_load(open("/content/cfg_probe.yaml")), callbacks=cbs)
''')

# ⛔ ĐỪNG dùng subprocess.run(capture_output=True): nó im lặng suốt ~75 phút và bạn không
#    phân biệt được "đang mã hoá" với "đã treo". Ghi ra tệp rồi in nhịp sống mỗi phút.
LOGP = "/content/probe.log"
t0 = time.time()
P = subprocess.Popen(["python3", "/content/chay_probe.py"], cwd=REPO,
                     stdout=open(LOGP, "w"), stderr=subprocess.STDOUT,
                     start_new_session=True,
                     env={**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1"})
CACHE = f"{D}/tok_cache_vissft"
while P.poll() is None:
    time.sleep(60)
    kb = os.path.getsize(LOGP) / 1024 if os.path.exists(LOGP) else 0
    nb = len(os.listdir(f"{PROBE}")) if os.path.isdir(PROBE) else 0
    ch = sum(f.stat().st_size for f in os.scandir(CACHE)) / 2**20 if os.path.isdir(CACHE) else 0
    print(f"{time.strftime('%H:%M:%S')} · {(time.time()-t0)/60:5.1f} phút · log {kb:6.0f} KB · "
          f"cache {ch:6.0f} MB · thư mục ra {nb} mục", flush=True)
TUONG = time.time() - t0        # ô dưới dùng lại làm cận trên nếu thiếu train_runtime
print("mã thoát:", P.returncode, "| tường:", f"{TUONG:.0f} s")
print(open(LOGP).read()[-2500:])
```

Rồi đọc **ba** con số, đừng đọc dòng `Training completed`:

```python
import json, os, glob
st = json.load(open(f"{PROBE}/trainer_state.json"))
lg = [h for h in st["log_history"] if "loss" in h]
# ⛔ train_runtime KHÔNG nằm ở gốc trainer_state.json. Nó ở phần tử cuối của log_history, và
#    chỉ có khi Trainer chạy xong trọn vẹn. Lấy theo thứ tự: log_history → thời gian tường đo
#    ở ô trên. Đừng dùng st.get("train_runtime", 0) — nó trả 0 rồi chia ra 0 giờ, trông như đạt.
rt = next((h["train_runtime"] for h in reversed(st["log_history"]) if "train_runtime" in h), None)
if rt is None:
    rt = TUONG          # biến này do ô trên đặt; gồm cả ~2,5 h mã hoá nên là CẬN TRÊN
    print("⚠️ không thấy train_runtime trong log_history — dùng thời gian tường, gồm cả mã hoá")
buoc = st["global_step"]
print("số bước đã chạy:", buoc, " ← phải là 200")
print("train_runtime  :", round(rt), "s")
print("s/bước         :", round(rt / max(buoc, 1), 2))
print("loss đầu → cuối:", lg[0]["loss"], "→", lg[-1]["loss"], " ← phải giảm rõ")
g = glob.glob(f"{PROBE}/grid/step00200/*")
print("grid/step00200:", [os.path.basename(x) for x in g], " ← phải có 2 tệp")
assert len(g) >= 2, "⛔ CALLBACK CHƯA CHẠY — grid/ rỗng. Sửa trước khi cam kết lượt thật."
# ⛔ 7.876 bước, KHÔNG phải 8.072: tập dạy nay 63.000 mẫu (đã trừ val), không phải 64.567.
#    ceil(63000/16) = 3.938, nhân 2 epoch = 7.876.
print("\n⇒ ước lượng lượt thật:", round(rt / max(buoc, 1) * 7876 / 3600, 1), "giờ")
```

⭐ **Con số quan trọng nhất là giờ ước lượng.** Rơi gần **20 h** thì ngân sách 50 h còn đủ cho hạt
giống 202; chạm **37 h** thì hạt 202 sẽ vỡ ngân sách, phải quyết trước khi bấm G6.

---

### ⏱ Chờ bao lâu — mốc đo thật 9/9

| chặng | bao lâu | dấu hiệu đã sang chặng sau |
|---|---|---|
| mã hoá 63.000 mẫu | **~2,5 h** | thư mục `tok_cache_vissft` trên Drive **xuất hiện** |
| ghi bản mã hoá lên Drive | ~5–15 phút (1,2 GB) | GPU rời khỏi 0 % |
| nạp model 4-bit | ~3–5 phút | log có dòng `loss` đầu tiên |
| 200 bước train | **~33 phút** | `grid/step00200/` có 2 tệp |

⇒ Tổng **~3,2 h**. ⚠️ Thư mục cache trên Drive **chỉ hiện ra khi mã hoá xong** chứ không lớn dần,
nên trong 2,5 h đầu cột `cache` của ô theo dõi vẫn trống — đó là bình thường; theo dõi bằng cột
CPU và bằng lệnh đếm dòng bên dưới.

---

## 🖥 Ô G5-CPU — mã hoá token trên runtime CPU (0 đơn vị)

Pha mã hoá không gọi GPU, nên chạy nó trên **Runtime → Change runtime type → CPU**. Máy ảo dựng
lại từ đầu, vì vậy phải chạy lại **G1 → G2 → G3 → G4b** rồi mới tới ô này.
⛔ `datasets.map` **không chạy tiếp từ giữa** — tệp `tmp…` bị vứt khi tiến trình chết, nên đổi máy
là mã hoá lại từ dòng 0.

Ô này khác ô G5 ở đúng bốn khoá, và **không khoá nào đụng tới nội dung được mã hoá** (đầu ra chỉ
gồm `input_ids` · `labels` · đường dẫn ảnh), nên bản cache dựng ở đây dùng được nguyên vẹn cho
lượt GPU:

```python
import yaml, os, subprocess, time
CFGC = "/content/cfg_tok_cpu.yaml"
c = yaml.safe_load(open(CFG))
assert "tokenized_path" in c, "⛔ chạy ô G4b trước, nếu không mã hoá xong là mất trắng"
c.pop("quantization_bit", None)        # ① 4-bit cần CUDA
c["bf16"] = False                      # ② CPU không có bf16
c["fp16"] = False
c["preprocessing_num_workers"] = 2     # ③ runtime CPU chỉ 2 lõi; 8 worker sẽ hết RAM 12,7 GB
c["output_dir"] = "/content/tok_cpu"   # ④ không đụng thư mục của lượt thật
c["max_steps"] = 1
c.pop("enable_liger_kernel", None)   # ⑤ liger là hạt nhân CUDA
yaml.safe_dump(c, open(CFGC, "w"), allow_unicode=True, sort_keys=False)
open("/content/chay_tok.py", "w").write(f'''
import yaml
from llamafactory.train.tuner import run_exp
run_exp(args=yaml.safe_load(open("{CFGC}")))
''')

LOGP = "/content/tok_cpu.log"
t0 = time.time()
P = subprocess.Popen(["python3", "/content/chay_tok.py"], cwd=REPO,
                     stdout=open(LOGP, "w"), stderr=subprocess.STDOUT,
                     start_new_session=True,
                     env={**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1"})
CACHE = f"{D}/tok_cache_vissft"
while P.poll() is None:
    time.sleep(60)
    mb = sum(f.stat().st_size for f in os.scandir(CACHE)) / 2**20 if os.path.isdir(CACHE) else 0
    print(f"{time.strftime('%H:%M:%S')} · {(time.time()-t0)/60:5.1f} phút · "
          f"log {os.path.getsize(LOGP)/1024:6.0f} KB · cache Drive {mb:6.0f} MB", flush=True)
print("mã thoát:", P.returncode)
print(open(LOGP).read()[-2000:])
```

✅ **Xong khi** thư mục `tok_cache_vissft` trên Drive đạt **~1,2 GB**. Tiến trình có thể **tự thoát
mã 0** ngay sau khi lưu (bản LLaMA-Factory in *"Please restart the training with tokenized_path"*),
hoặc **chết vì không có CUDA** lúc nạp model — **cả hai đều là thành công**, vì bản cache đã ghi
xong trước đó. Chỉ khi cache dưới 800 MB mới là hỏng thật.

Kiểm lần cuối trước khi đổi sang GPU:

```python
import os
P = f"{D}/tok_cache_vissft"
tong = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(P) for f in fs)
print(round(tong/2**30, 2), "GB ·", os.listdir(P), " ← cần ~1,2 GB")
```

⇒ Rồi đổi runtime sang GPU, chạy lại **G1 → G2 → G3 → G4b**, và vào thẳng **G6**. G6 thấy cache đã
có nên bỏ qua trọn pha mã hoá.

✅ **ĐÃ ĐO 9/9/2026 — pha mã hoá trên runtime CPU mất ~2 giờ 57 phút** (tiến trình khởi lúc
11:56, cache 1,14 GB nằm trọn trên Drive lúc 14:53), với `preprocessing_num_workers: 2` (hai worker
chạy ~100 % một lõi mỗi cái, xác nhận bằng cột `TIME` của `ps`). So mốc ~2,5 h của A100 thì tỉ số
là **~1,18×**, dưới ngưỡng 1,5× của luật chọn máy ⇒ **chạy pha này trên CPU là đúng**, tiết kiệm
trọn ~3 h A100 cho một khâu GPU đứng 0 %.
✅ Bốn phép kiểm sau khi xong, theo thứ tự tăng dần độ chắc: dung lượng ~1,2 GB → có `state.json`
trong `train/` (được ghi CUỐI CÙNG nên là bằng chứng lưu trọn vẹn) → cột đúng
`input_ids/attention_mask/labels/images` → **`num_examples` phải bằng 63.000** (phép kiểm quan
trọng nhất: 64.567 nghĩa là đã mã hoá nhầm bộ chưa trừ val, và chỉ lộ ra sau 20 đến 37 h A100).

⚠️ **Mốc cũ (giữ để đối chiếu):** Lượt A100 dùng ~1,9 lõi (CPU toàn máy 16 % trên 12 lõi) và
đạt 406 dòng/phút; runtime CPU thường có 2 lõi nên **có thể** ngang, nhưng đó là suy luận. Đo thật
bằng lệnh đếm dòng ở ô G5t sau 15 phút rồi hãy tin.

⭐ **Muốn cắt được giữa chừng ở lượt sau:** chia 63.000 mẫu thành 8 phần, mã hoá và `save_to_disk`
từng phần rồi nối lại. `datasets.map` không có điểm lưu, nên đó là cách duy nhất để một lần mất
máy không xoá sạch công.

---

## ✂️ Ô G5x — theo dõi **và tự cắt** smoke ngay khi mã hoá đã an toàn

⭐ **Vì sao cắt:** smoke sinh ra để đo s/bước, xác nhận `grid_callback` ghi được, và tránh phải mã
hoá lại nếu hỏng. Khi `tokenized_path` đã ghi lên Drive thì **cả ba lý do đều mất**: G6 cho s/bước
trong 20 dòng log đầu, `grid/step00200` xuất hiện sau ~33 phút của chính G6, và chạy lại G6 nay chỉ
tốn vài phút vì cache đã có. ⇒ Chạy nốt 200 bước của smoke là **~35 phút A100 không mua thêm gì**.

⛔ **Nhưng đừng cắt sớm.** Trước khi dừng phải chắc **hai** điều, nếu không là mất trắng 2,5 h:
① thư mục cache trên Drive **đã ≥ 800 MB** (đích ~1,2 GB, dưới ngưỡng này là đang ghi dở);
② tiến trình **đã vào train** — có dòng `loss` trong log, hoặc GPU ≥ 20 % hai lần đo liên tiếp.
Điều ② mới là bằng chứng LLaMA-Factory đã ghi xong và đóng tệp, vì nó chỉ train sau khi lưu.

Dán vào Terminal Colab. Ô này in nhịp sống mỗi phút, và **tự `pkill` đúng lúc đủ hai điều kiện**:

```bash
CACHE=/content/drive/MyDrive/thesis/tok_cache_vissft
LOG=/content/probe.log
pt=0; pi=0; ng=0
while :; do
  set -- $(awk '/^cpu /{t=0; for(i=2;i<=NF;i++) t+=$i; print t, $5}' /proc/stat)
  t=$1; i=$2
  if [ $pt -ne 0 ]; then b=$(( 100*((t-pt)-(i-pi))/(t-pt) )); else b="--"; fi
  pt=$t; pi=$i
  P=$(pgrep -f chay_probe | head -1)
  MB=$(du -sm "$CACHE" 2>/dev/null | cut -f1); MB=${MB:-0}
  L=$(grep -c "'loss'" "$LOG" 2>/dev/null); L=${L:-0}
  G=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | head -1)
  if [ "$G" -ge 20 ]; then ng=$((ng+1)); else ng=0; fi
  printf '%s · pid %-8s · CPU %3s%% · cache %6s MB · loss %3s · GPU %3s%%\n' \
    "$(date +%H:%M:%S)" "${P:-CHET}" "$b" "$MB" "$L" "$G"
  if [ "$MB" -ge 800 ] && { [ "$L" -ge 1 ] || [ "$ng" -ge 2 ]; }; then
    echo "=> DU DIEU KIEN CAT: cache $MB MB da nam tren Drive va da vao train."
    pkill -f chay_probe
    echo "=> Da dung smoke. Sang notebook chay o G6."
    break
  fi
  if [ -z "$P" ]; then
    if [ "$MB" -ge 800 ]; then
      echo "=> TIEN TRINH TU THOAT SAU KHI LUU ($MB MB) - DAY LA THANH CONG. Chay o G6."
    else
      echo "LOI: tien trinh chet ma cache moi $MB MB - xem $LOG"
    fi
    break
  fi
  sleep 60
done
```

**Đọc ba cột:** `cache` đứng 0 suốt ~2,5 h đầu là **bình thường** (thư mục chỉ hiện khi mã hoá
xong, không lớn dần) · `CPU` cao + `GPU 0` là đang mã hoá · `cache` nhảy lên vài trăm MB là đang
ghi lên Drive, **đừng đụng** · `loss` ≥ 1 là đã vào train, ô tự cắt.

⚠️⚠️ **Tiến trình tự chết sau khi lưu là CHUYỆN BÌNH THƯỜNG, không phải lỗi.** Nhiều bản
LLaMA-Factory lưu xong bản mã hoá thì `sys.exit(0)` ngay, in đại ý *"Please restart the training
with `tokenized_path`"*, chứ không train tiếp. ⇒ Luật đọc: **chết + cache trên Drive ~1,2 GB =
thành công**, chạy thẳng G6. Chỉ khi chết mà cache dưới 800 MB mới là hỏng thật, lúc đó đọc
`tail -50 /content/probe.log`. Ô trên đã phân biệt hai trường hợp này.
⚠️ Có thể còn tệp `tmp…` **của lượt trước** nằm lại trong cache cục bộ và đứng yên; lượt đang chạy
là tệp có số dòng **tăng** giữa hai lần đo. Đừng xoá nhầm.

✅ **Sau khi ô này in `Da dung smoke`:** sang notebook chạy thẳng **ô G6**. Bỏ qua phần đọc ba con
số của G5 (số bước 200 · `grid/step00200` · ước lượng giờ) — G6 trả lời cả ba trong 35 phút đầu.

---

## 👁 Ô G5t-CPU — kiểm pha mã hoá còn sống không, **từ Terminal Colab**

Dùng khi đang chạy **ô G5-CPU** và trình duyệt mất kết nối (gập máy, sập wifi, đổi mạng).
⛔ Ô G5t bên dưới viết cho lượt GPU: nó tìm tiến trình `chay_probe` và gọi `nvidia-smi`, cả hai
đều sai ở runtime CPU. Dùng khối này thay thế.

⛔ **Đừng bấm Stop ô nào, đừng chạy ô notebook mới.** Nhân Python đang bận ô G5-CPU nên mọi ô khác
chỉ **xếp hàng**, không chạy; Terminal Colab là tiến trình riêng nên nhìn được ngay.

```bash
pt=0; pi=0
while :; do
  set -- $(awk '/^cpu /{t=0; for(i=2;i<=NF;i++) t+=$i; print t, $5}' /proc/stat)
  t=$1; i=$2
  if [ $pt -ne 0 ]; then b=$(( 100*((t-pt)-(i-pi))/(t-pt) )); else b="--"; fi
  pt=$t; pi=$i
  P=$(pgrep -f chay_tok | head -1)
  MB=$(du -sm /content/drive/MyDrive/thesis/tok_cache_vissft 2>/dev/null | cut -f1)
  AR=$(du -sm /root/.cache/huggingface/datasets 2>/dev/null | cut -f1)
  printf '%s · pid %-8s · CPU %3s%% · arrow %5s MB · cache %5s MB\n' \
    "$(date +%H:%M:%S)" "${P:-CHET}" "$b" "${AR:-0}" "${MB:-0}"
  sleep 60
done
```

⚠️ Dòng đầu in `CPU --%` vì cột đó là **hiệu số giữa hai lần đo**; đọc từ dòng thứ hai trở đi.

⛔ **Cột `log` đã bị bỏ, thay bằng `arrow`.** Với `TQDM_DISABLE=1` thì `tok_cpu.log` **đứng yên
suốt cả pha mã hoá** (dòng cuối là *"Loading dataset s1.json..."*), nên nó không phải chỉ báo sống.
Chỉ báo tiến độ thật là thư mục tạm của `datasets.map` ở `/root/.cache/huggingface/datasets`: nó
**lớn dần từng phút**. Cột `cache` (trên Drive) chỉ nhảy lên MỘT LẦN ở cuối.

| pid | CPU | arrow | phán |
|---|---|---|---|
| có số | **cao** | **tăng** mỗi phút | ✅ đang mã hoá, đúng như thiết kế |
| có số | cao | đứng, `cache` bắt đầu tăng | ✅ đã map xong, đang ghi lên Drive. **Đừng đụng gì** |
| **CHET** | — | ≥ 800 MB | ✅ **thành công** — bản LLaMA-Factory pin ở đây thoát ngay sau khi lưu. Sang G6 |
| **CHET** | — | < 800 MB | ⛔ hỏng thật, đọc `tail -50 /content/tok_cpu.log` |
| có số | **≤ 2 %** hai lần liên tiếp | **đứng yên** | ⛔ treo |


⚠️ **Dòng `Setting num_proc from 2 back to 1 ... as it only contains one shard` KHÔNG có nghĩa là
mã hoá chạy đơn luồng.** Nó chỉ áp cho khâu **nạp** dataset (một tệp `s1.json` = một shard); khâu
tokenize sau đó vẫn dùng đủ `preprocessing_num_workers`. Đo thật 9/9 lúc 14:48 trên runtime CPU:

```
  PID  ELAPSED     TIME %CPU STAT
10140  02:51:57 00:01:35  0.9 Ssl   ← cha, chỉ ngồi chờ
10346  02:51:17 02:18:38 80.9 R     ← worker 1, ~100 % một lõi
10347  02:51:17 02:18:39 80.9 D     ← worker 2, ~100 % một lõi
```

⇒ **Cách kiểm ai đang làm việc: `ps -o pid,etime,time,%cpu,stat` hai lần cách 60 giây, xem cột
`TIME` của từng tiến trình.** Đo `/proc/<pid>/io` của tiến trình CHA sẽ thấy đứng yên hoàn toàn và
dễ đọc nhầm thành treo — việc thật nằm ở các tiến trình CON.
⚠️ Bài học lặp lại lần thứ n: một dòng log ngắn bị tóm tắt thành kết luận rộng. Suýt ghi vào
runbook rằng khâu này chạy một lõi, và suýt suy tiếp rằng cần chia shard mới nhanh được.

### ⏳ Biến thể có ETA — dùng khi cần biết còn bao lâu

Cột `tmp` là **tổng byte các tệp tạm của `datasets.map`** dưới `/root/.cache/huggingface/datasets`,
tức phần đang được mã hoá; nó lớn dần từng phút và là chỉ báo tiến độ duy nhất khi `TQDM_DISABLE=1`.
ETA tính từ tốc độ tăng thật kể từ lúc bật ô (cần ~3 phút mới có số), không phải từ mốc nhớ sẵn.
Ô tự dừng khi cache trên Drive ≥ 800 MB hoặc khi tiến trình hết.

```bash
DICH=1229                                   # MB, dich ~1,2 GB
CACHE=/content/drive/MyDrive/thesis/tok_cache_vissft
DS=/root/.cache/huggingface/datasets
t0=0; s0=0; pt=0; pi=0
while :; do
  now=$(date +%s)
  TMP=$(find $DS -name '*tmp*' -type f -printf '%s\n' 2>/dev/null | awk '{t+=$1} END{printf "%d", t/1048576}')
  TMP=${TMP:-0}
  MB=$(du -sm "$CACHE" 2>/dev/null | cut -f1); MB=${MB:-0}
  set -- $(awk '/^cpu /{t=0; for(i=2;i<=NF;i++) t+=$i; print t, $5}' /proc/stat)
  t=$1; i=$2
  if [ $pt -ne 0 ]; then b=$(( 100*((t-pt)-(i-pi))/(t-pt) )); else b="--"; fi
  pt=$t; pi=$i
  N=$(pgrep -c -f chay_tok); N=${N:-0}
  [ $t0 -eq 0 ] && { t0=$now; s0=$TMP; }
  d=$(( TMP - s0 )); dt=$(( now - t0 )); ETA="dang do"
  if [ $d -gt 0 ] && [ $dt -ge 180 ]; then
    con=$(( DICH - TMP )); [ $con -lt 0 ] && con=0
    ETA="$(( con * dt / d / 60 )) phut  ($(( d * 60 / dt )) MB/phut)"
  fi
  printf '%s · %s tt · CPU %3s%% · tmp %5s MB · cache %5s MB · con ~%s\n' \
    "$(date +%H:%M:%S)" "$N" "$b" "$TMP" "$MB" "$ETA"
  [ "$MB" -ge 800 ] && { echo "=> XONG: cache $MB MB da nam tren Drive. Doi runtime sang GPU, chay G1-G2-G3-G4b roi G6."; break; }
  [ "$N" -eq 0 ] && { echo "=> Tien trinh het. cache $MB MB (>=800 la thanh cong, <800 la hong: tail -50 /content/tok_cpu.log)"; break; }
  sleep 60
done
```

⚠️ **Đừng lấy mốc "406 dòng/phút" của lượt A100 để suy ra giờ cho runtime CPU.** Mốc đó đo với
`preprocessing_num_workers: 8`, còn ô G5-CPU hạ xuống **2** (RAM 12,7 GB), nên số worker khác nhau
và tỉ lệ chưa từng đo. Lấy số từ cột ETA của chính lượt đang chạy.

⛔ **Nếu Terminal cũng không mở được và trang báo mất kết nối runtime** thì máy ảo đã bị thu hồi.
Pha này chạy trên runtime CPU nên **mất 0 đơn vị**, chỉ mất thời gian; nhưng `datasets.map` không
chạy tiếp từ giữa, nên phải làm lại **G1 → G2 → G3 → G4b → G5-CPU** từ dòng 0.
⇒ Cách giữ máy khi cần rời bàn: để trang Colab **mở trên một máy còn thức** (điện thoại cũng được),
đừng gập nắp. Xem luật ④ ở đầu runbook.

## 👁 Ô G5t — theo dõi G5 **từ Terminal Colab** (không đụng vào ô đang chạy)

Ô G5 đã tự in nhịp sống mỗi phút, nhưng khi cần soi kỹ hơn (hoặc khi trình duyệt mất kết nối
hiển thị) thì mở **Terminal Colab** — tiến trình riêng, cùng máy ảo, cùng thấy `/content` và
`/content/drive`.

⛔ **Terminal chỉ để NHÌN. Đừng bấm Stop ô G5, đừng chạy ô notebook nào khác** — ô G5 là ô
foreground duy nhất giữ máy ảo khỏi bị ngắt vì không hoạt động (luật ④).

**Dán trọn khối này vào Terminal.** Nó in một dòng mỗi 60 giây, cuộn xuống, không xoá màn hình.

```bash
while :; do
  P=$(pgrep -f chay_probe | head -1)
  printf '%s · pid %-8s · log %5s · cache %5s · ra %2s mục · GPU %s\n' \
    "$(date +%H:%M:%S)" "${P:-⛔CHET}" \
    "$(du -h  /content/probe.log 2>/dev/null | cut -f1)" \
    "$(du -sh /content/drive/MyDrive/thesis/tok_cache_vissft 2>/dev/null | cut -f1)" \
    "$(ls /content/probe_vissft 2>/dev/null | wc -l)" \
    "$(nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader | tr -d '\n')"
  sleep 60
done
```

**Cột `GPU` là cột phân biệt hai giai đoạn** — đây là thứ ô G5 không cho biết:

| dấu hiệu | đang ở đâu | bình thường không |
|---|---|---|
| GPU **0 %**, bộ nhớ vài trăm MiB, `cache` lớn dần | đang **mã hoá token** | ✅ đúng, kéo ~2,5 h |
| GPU **70–100 %**, bộ nhớ ~15–25 GiB, `log` lớn dần | đang **train 200 bước** | ✅ đúng, ~33 phút |
| GPU 0 %, `cache` **đứng yên** hai lần đo liên tiếp, log không nhích | nghi treo | ⚠️ xem `tail` bên dưới |
| `pid` in ra **⛔CHET** mà ô G5 vẫn quay | tiến trình đã chết | ⛔ đây mới là hỏng thật |

⚠️ `du` trên `/content/drive` đọc qua FUSE nên số có thể nhích giật cục, đừng đọc một lần đã
kết luận; lấy **hai lần đo cách nhau 60 giây**.

### ⛔ Nếu cột `log` và `cache` trống — dùng khối theo dõi thứ hai

Đo thật 9/9: cả hai cột trống mà lượt chạy vẫn lành. Hai lý do, không lý do nào là hỏng:
· **`log` trống** — lượt đang chạy là bản G5 **cũ** dùng `capture_output=True`, không hề tạo
  `/content/probe.log`. Bản Popen chỉ có tác dụng từ lần chạy sau.
· **`cache` trống** — hoặc chưa chạy G4b, hoặc thư mục mã hoá chỉ được ghi **một lần khi mã hoá
  xong** chứ không lớn dần. Phân biệt: `grep -i token /content/cfg_probe.yaml`.

⇒ Khi ấy không còn cột nào lớn dần, và `GPU 0 %` một mình **không** phân biệt được *đang mã hoá*
với *đã treo*. Cột thay thế là **CPU toàn máy**: khâu mã hoá chạy 8 tiến trình con nên máy phải
bận rõ rệt.

```bash
pt=0; pi=0
while :; do
  set -- $(awk '/^cpu /{t=0; for(i=2;i<=NF;i++) t+=$i; print t, $5}' /proc/stat)
  t=$1; i=$2
  if [ $pt -ne 0 ]; then b=$(( 100*((t-pt)-(i-pi))/(t-pt) )); else b="--"; fi
  pt=$t; pi=$i
  P=$(pgrep -f chay_probe | head -1)
  printf '%s · pid %-8s · CPU %3s%% · arrow %6s · GPU %s\n' \
    "$(date +%H:%M:%S)" "${P:-⛔CHET}" "$b" \
    "$(du -sh /root/.cache/huggingface/datasets 2>/dev/null | cut -f1)" \
    "$(nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader | tr -d '\n')"
  sleep 60
done
```

⚠️ Dòng đầu in `CPU --%` vì cột này là **hiệu số giữa hai lần đo**; đọc từ dòng thứ hai.

| CPU | GPU | đang ở đâu |
|---|---|---|
| **cao** (vài chục đến ~100 %) | 0 % | mã hoá token — ✅ đúng |
| thấp | **70–100 %** | đã vào train — ✅ đúng, mốc này tới sau ~2,5 h |
| **≤ 2 %** hai lần đo liên tiếp | 0 % | ⛔ treo thật |

**Câu hỏi cuối cùng khi vẫn nghi** — có tệp nào vừa được ghi trong 2 phút qua không:

```bash
find /root/.cache /content /tmp -newermt '-2 minutes' -type f 2>/dev/null | head -5
```

Ra danh sách rỗng **và** CPU ≤ 2 % thì mới kết luận là treo.

### ⭐ Đọc PHẦN TRĂM thật của khâu mã hoá

Tệp Arrow đang ghi vẫn đếm được số dòng. ⛔ Tệp đang ghi tên là **`tmp…`**, không phải
`cache-*.arrow` — `datasets` chỉ đổi tên sang `cache-<hash>.arrow` **khi map xong**, nên chỉ lọc
`cache-*` là đọc nhầm sang lượt map trước đó rồi thấy 100 %.

```bash
python3 - <<'EOF'
import glob, os, pyarrow as pa
for f in sorted(glob.glob('/root/.cache/huggingface/datasets/**/*', recursive=True)):
    if not os.path.isfile(f): continue
    n = 0
    try:
        with pa.ipc.open_stream(pa.memory_map(f)) as r:
            while True:
                try: n += r.read_next_batch().num_rows
                except Exception: break
    except Exception: pass
    print(f"{os.path.getsize(f)/2**20:8.0f} MB {n:8d} dòng  {os.path.basename(f)[:52]}")
EOF
```

Đo thật 9/9, giữa lượt: `tmpur7iubxa` 500 MB / **26.000 dòng** trên 63.000 ⇒ **19,2 KB/dòng**,
đích ~1,2 GB. Chạy lệnh hai lần cách nhau 5 phút rồi lấy hiệu số dòng chia 5 là ra dòng/phút;
lượt 9/9 cho **~420 dòng/phút** ⇒ trọn khâu mã hoá **~2,5 h**, không phải 42 phút.

**Xem tiến trình đang in gì** (chạy bất cứ lúc nào, ở tab Terminal thứ hai hoặc dừng vòng lặp
bằng `Ctrl-C` — `Ctrl-C` ở Terminal **không** đụng tới tiến trình train vì G5 phóng nó bằng
`start_new_session=True`):

```bash
tail -n 30 /content/probe.log
grep -c "Traceback" /content/probe.log          # phải là 0
ls -la /content/probe_vissft/grid/ 2>/dev/null  # cuối lượt phải có step00200
```

**Một lệnh, xem một cái rồi thoát** (không vòng lặp):

```bash
echo "pid=$(pgrep -f chay_probe | head -1)"; ls -la /content/probe.log; \
du -sh /content/drive/MyDrive/thesis/tok_cache_vissft; nvidia-smi | head -12
```

⭐ **Nếu tài khoản không có Terminal**, mở **notebook thứ hai** trên cùng máy ảo rồi chạy ô này —
cùng thông tin, cùng cách đọc:

```python
import os, time, subprocess
LOGP, PROBE = "/content/probe.log", "/content/probe_vissft"
CACHE = "/content/drive/MyDrive/thesis/tok_cache_vissft"
sh = lambda c: subprocess.run(c, shell=True, capture_output=True, text=True).stdout.strip()
while True:
    pid = sh("pgrep -f chay_probe | head -1") or "⛔CHET"
    kb  = os.path.getsize(LOGP)/1024 if os.path.exists(LOGP) else 0
    mb  = sum(f.stat().st_size for f in os.scandir(CACHE))/2**20 if os.path.isdir(CACHE) else 0
    nb  = len(os.listdir(PROBE)) if os.path.isdir(PROBE) else 0
    gpu = sh("nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader")
    print(f"{time.strftime('%H:%M:%S')} · pid {pid} · log {kb:6.0f} KB · cache {mb:6.0f} MB · "
          f"ra {nb} mục · GPU {gpu}", flush=True)
    time.sleep(60)
```

⭐ **Dùng lại nguyên khối này cho lượt thật ở G6**, đổi đúng hai chỗ: `chay_probe` → `chay_vissft`
và `/content/probe.log` → `/content/train_vissft.log`. Ô G7 vẫn phải chạy foreground trong
notebook; Terminal chỉ là cửa sổ nhìn thêm, **không thay được G7** (luật ④: notebook rỗi thì
Colab ngắt máy sau ~90 phút).

---

## ⛔⛔ Ô G0-lại — BẮT BUỘC sau MỖI lần dựng lại máy ảo (mất máy, đổi runtime)

⚠️ **Mọi sửa tại chỗ trong `/content` đều biến mất theo máy ảo.** Đã mắc sáng 10/9: hôm trước ghi
đè `chay_vissft.py` bằng `%%writefile` và đặt `save_steps: 100`, mất máy lúc ~06:00, dựng lại thì
ô G2 bung zip từ Drive và **cả hai thay đổi đều về bản cũ** — không có gì báo, và nếu bấm thẳng G6
thì hoặc nổ `TypeError` hoặc chạy hết giờ A100 với `grid/` rỗng.

⇒ Sau G1→G2→G3→G4b→G5k, **trước khi bấm G6**, chạy ba lệnh này:

```python
!grep -c "for duong in" {REPO}/harness/chay_vissft.py            # cần 1
!grep -c "yaml.safe_load(open(CFG" {REPO}/harness/chay_vissft.py  # cần 1
import yaml; print("save_steps =", yaml.safe_load(open(CFG))["save_steps"])  # cần 100
```

Ra `0 · 0 · 200` thì ghi đè lại `chay_vissft.py` (ô `%%writefile` ở mục G6) và đặt lại `save_steps`.

⭐ **Cách chặn tận gốc cho lượt sau:** đóng gói lại `_bundles/thesis_rented.zip` từ bản WSL rồi
upload đè lên Drive, để zip đã chứa sẵn bản 9/9. Chừng nào chưa làm thì phải chạy ô G0-lại này
**sau mỗi lần dựng máy**.

⚠️ Nhận ra bằng dòng in của G2: bản đã vá in `gói mã : bản 9/9 ✓ (gồm chay_vissft.py +
grid_callback.py)`. In thiếu phần trong ngoặc nghĩa là notebook đang dùng ô G2 bản cũ.

---

## Ô G6 — lượt thật, chạy nền

```python
import subprocess, os
# ⛔ TQDM_DISABLE bắt buộc: stdout đang được chuyển hướng vào tệp, mà tqdm ngoài terminal in
#    MỖI cập nhật thành một dòng. Lượt 7.876 bước sẽ đẻ ra tệp log hàng GB và làm ô theo dõi
#    đọc chậm dần. Tắt nó thì vẫn còn dòng {'loss': …, 'epoch': …} mỗi 20 bước, đủ để theo dõi.
env = {**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1",
       "HF_HUB_DISABLE_PROGRESS_BARS": "1"}
P = subprocess.Popen(["python3", "harness/chay_vissft.py"],
                     stdout=open("/content/train_vissft.log", "a"),
                     stderr=subprocess.STDOUT,
                     start_new_session=True,          # ⛔⛔ THIẾU CỜ NÀY LÀ MẤT LƯỢT
                     env=env, cwd=REPO)
print("PID", P.pid, "| log: /content/train_vissft.log")
```

⛔⛔ **`start_new_session=True` không được bỏ.** Thiếu nó thì tiến trình train nằm cùng nhóm với
kernel notebook, và **mọi lần bấm Stop một ô bất kỳ** đều gửi tín hiệu dừng sang train. Lượt
`gui_sel`/101 chết ở bước 747/4036 vì đúng chuyện này.

### Trước khi chạy G6 — hai ô vá, dán theo thứ tự

**① Sửa `GRID` cho khớp `output_dir`** (chỉ cần nếu bạn đổi nó ở G3):

```python
!sed -i 's#^GRID = .*#GRID = "{D}/ckpt/vissft_seed101/grid"#' {REPO}/harness/chay_vissft.py
!grep -n "^GRID" {REPO}/harness/chay_vissft.py
```

**② Vá `LogCallback` nếu gói mã trên Drive là bản trước 9/9.** Gói 9/9 đã tự dò bốn đường nên
không cần ô này; kiểm bằng `grep`, thấy dòng `for duong in` là đã có bản vá.

```python
# hai phép kiểm, cả hai phải in 1
!grep -c "for duong in" {REPO}/harness/chay_vissft.py            # vá LogCallback
!grep -c "yaml.safe_load(open(CFG" {REPO}/harness/chay_vissft.py  # vá run_exp nhận dict
```

⛔ Phép kiểm thứ hai là chỗ đã ném `TypeError: can only concatenate list (not "str") to list` ở
giây thứ 10. In ra `0` thì gói mã trên Drive là bản trước 9/9 — upload lại, hoặc sửa tay:

```python
p = f"{REPO}/harness/chay_vissft.py"
s = open(p).read().replace("run_exp(args=CFG, callbacks=cbs)",
                           "import yaml\n    run_exp(args=yaml.safe_load(open(CFG, encoding='utf-8')), callbacks=cbs)")
open(p, "w").write(s)
!grep -n "run_exp(args" {p}
```

```python
# chỉ chạy khi lệnh trên in 0
import re
p = f"{REPO}/harness/chay_vissft.py"
s = open(p).read()
s = s.replace("    from llamafactory.extras.callbacks import LogCallback\n", "")
s = s.replace("run_exp(args=CFG, callbacks=[LogCallback(), CopyAdapterToGrid(GRID)])",
              'LogCallback = None\n'
              '    for _d in ("llamafactory.train.callbacks", "llamafactory.extras.callbacks"):\n'
              '        try:\n'
              '            LogCallback = __import__(_d, fromlist=["LogCallback"]).LogCallback\n'
              '            break\n'
              '        except Exception:\n'
              '            pass\n'
              '    import yaml\n'
              '    run_exp(args=yaml.safe_load(open(CFG, encoding="utf-8")),\n'
              '            callbacks=[CopyAdapterToGrid(GRID)]'
              ' + ([LogCallback()] if LogCallback else []))')
open(p, "w").write(s)
print(open(p).read()[-700:])
```

---

## Ô G7 — theo dõi, phải chạy FOREGROUND suốt lượt

Bấm ⏹ để dừng **ô này**; train không chết theo (nhờ `start_new_session`).

```python
import json, os, re, time
os.environ["TZ"] = "Asia/Ho_Chi_Minh"; time.tzset()   # ⚠️ Colab chạy giờ UTC, lệch 7 tiếng
OUT  = f"{D}/ckpt/vissft_seed101"
LOG  = "/content/train_vissft.log"          # ⭐ đĩa LOCAL — nguồn tiến độ CHÍNH
TL   = f"{OUT}/trainer_log.jsonl"           # trên Drive — chỉ dùng đối chiếu
NHIP, TONG, BUOC_EPOCH = 60, 7876, 3938     # ceil(63.000/16) = 3.938 bước mỗi epoch
# ⚠️ SỬA 9/9: bản pin in giá trị CÓ NHÁY — {'loss': '2.236', 'epoch': '0.005079'} — nên regex
#    cũ (chờ số ngay sau dấu cách) trượt sạch, và ô in "chưa có dòng loss nào" suốt cả lượt
#    trong khi log đầy đủ. Dấu nháy phải là tuỳ chọn.
EP = re.compile(r"'epoch':\s*'?([\d.eE+-]+)'?")
LS = re.compile(r"'loss':\s*'?([\d.eE+-]+)'?")
t0, mocb, moct, truoc, n0 = time.time(), None, None, None, 0

def thanh(p, w=30):
    k = max(0, min(w, int(round(p * w)))); return "[" + "█" * k + "░" * (w - k) + f"] {100*p:5.1f}%"

def doc_log():
    """Bước và loss lấy từ LOG LOCAL. ⛔ Không lấy từ trainer_log.jsonl trên Drive làm nguồn
    chính: FUSE có thể không đẩy nội dung mới sang, và số bước sẽ đứng yên hàng giờ dù train
    vẫn chạy — đúng lỗi đã làm mất một lượt ngày 2/9."""
    if not os.path.exists(LOG):
        return None, None
    duoi = open(LOG, "rb").read()[-200000:].decode("utf-8", "ignore")
    e = EP.findall(duoi); l = LS.findall(duoi)
    return (round(float(e[-1]) * BUOC_EPOCH) if e else None), (l[-1] if l else None)

def doc_jsonl():
    if not os.path.exists(TL):
        return None
    b = None
    for ln in open(TL, encoding="utf-8"):
        ln = ln.strip()
        if ln:
            try:
                b = json.loads(ln).get("current_steps", b)
            except Exception:
                pass
    return b

# ⭐ ba cột thêm 9/9: PID · GPU/VRAM · số điểm lưu trong grid/
import subprocess
PID = None
def con_song():
    """⛔ G7 bản đầu KHÔNG kiểm tiến trình: train chết thì ô vẫn in lại dòng cũ mãi mãi
    và không có gì báo. Đây là cột quan trọng nhất của ô này."""
    global PID
    if PID is None:
        r = subprocess.run("pgrep -f chay_vissft | head -1", shell=True,
                           capture_output=True, text=True).stdout.strip()
        PID = int(r) if r else None
    return PID is not None and os.path.exists(f"/proc/{PID}")

def gpu():
    r = subprocess.run("nvidia-smi --query-gpu=utilization.gpu,memory.used "
                       "--format=csv,noheader,nounits", shell=True,
                       capture_output=True, text=True).stdout.strip()
    return r.replace("\n", "")

while True:
    b, ls = doc_log()
    bj = doc_jsonl()
    kb = os.path.getsize(LOG) / 1024 if os.path.exists(LOG) else 0
    song = con_song()
    g = gpu()
    ng = len(os.listdir(f"{OUT}/grid")) if os.path.isdir(f"{OUT}/grid") else 0
    if not song:
        print(f"{time.strftime('%H:%M:%S')} ⛔⛔ TIẾN TRÌNH TRAIN ĐÃ CHẾT · bước cuối {b} · "
              f"đọc `tail -60 {LOG}` · chạy lại ô G6 để tiếp từ điểm lưu", flush=True)
    if b:
        if mocb is None:
            mocb, moct = b, time.time()
        sb  = (time.time() - moct) / max(b - mocb, 1) if b > mocb else float("nan")
        con = (TONG - b) * sb / 3600 if b > mocb else float("nan")
        print(f"{time.strftime('%H:%M:%S')} {thanh(b/TONG)} {b}/{TONG} · {sb:5.2f} s/bước · "
              f"còn ~{con:4.1f} h · loss {ls} · GPU {g} · grid {ng} · Drive {bj} · "
              f"log {kb:.0f} KB", flush=True)
        if truoc is not None and b < truoc:
            print("  ⚠️ số bước TỤT — phiên mới đã ghi đè, train đang chạy tiếp từ điểm lưu",
                  flush=True)
        if bj is not None and b - bj > 400:
            print("  ℹ️ cột Drive chậm hơn log local — FUSE chưa đẩy tệp, KHÔNG phải treo",
                  flush=True)
        truoc = b
    else:
        print(f"{time.strftime('%H:%M:%S')} chưa có dòng loss nào · GPU {g} · "
              f"log {kb:.0f} KB · sống: {song}", flush=True)
        # ⛔ Dấu hiệu tokenize lại là GPU 0 % LIÊN TỤC kèm VRAM vài trăm MiB, KHÔNG phải một
        #    lần lấy mẫu rơi vào lúc nhàn giữa hai bước.
        # ⚠️ SỬA 9/9: bản đầu cảnh báo ngay khi thấy "0," một lần và đã báo động giả lúc 22:27,
        #    trong khi GPU dao động 52/81/60/0/57/76 với VRAM 31 GiB, tức đang train bình thường.
        try:
            gu, vram = [int(x) for x in g.split(",")]
        except Exception:
            gu, vram = -1, -1
        n0 = (n0 + 1) if (gu == 0 and 0 <= vram < 2000) else 0
        if n0 >= 5:
            print("  ⛔ GPU 0 % và VRAM < 2 GiB suốt 5 phút — ĐANG MÃ HOÁ LẠI. "
                  "Kiểm: grep -c 'Running tokenizer' " + LOG, flush=True)
    time.sleep(NHIP)
```

⛔ **KHÔNG bấm Stop ô nào khác** khi train đang chạy; cần chạy ô khác thì mở **notebook thứ hai**.
⛔ Phải có **một** ô foreground suốt lượt, nếu không Colab ngắt máy vì không hoạt động sau ~90 phút.
⚠️ `log ... KB` phải tăng đều. Đứng yên hơn 10 phút mà số bước cũng đứng thì mới nghi treo.

**Ba cột thêm 9/9 và cách đọc:**

| cột | lành | hỏng |
|---|---|---|
| dòng `⛔⛔ TIẾN TRÌNH TRAIN ĐÃ CHẾT` | không xuất hiện | xuất hiện ⇒ chạy lại ô G6, nó tiếp từ điểm lưu gần nhất |
| `GPU` | dao động 40 đến 100 % (rơi xuống 0 một lần là bình thường), VRAM 15 đến 32 GiB | **0 %** kéo dài ⇒ đang mã hoá lại (mất tiền A100) · VRAM > 36 GiB ⇒ sát trần, nguy cơ hết bộ nhớ ở mẫu dài |
| `grid` | ≥ 1 sau ~50 phút, rồi tăng đều | **đứng 0** sau lần lưu đầu ⇒ callback không đăng ký, đang mất 39 quan sát ⇒ dừng, kiểm hai lệnh `grep` ở G6 |

⚠️ **Cột `grid` là phép kiểm sớm nhất cho bẫy ③.** Trước bản vá này, `grid/` rỗng chỉ lộ ra khi
lượt train đã xong.

---

## 📉 LOSS VAL — thiếu ở lượt này, cách lấy lại và cách làm đúng cho lượt sau

⛔ **Thiếu sót của lượt 9/9, user chỉ ra 10/9:** cấu hình đặt `val_size: 0.0` và `do_eval: false`
nên **không có đường cong loss val**, tức không biết mô hình có quá khớp hay không. Lý do gốc là
đúng (trainer tự chia val sẽ chia ngẫu nhiên theo dòng ⇒ rò rỉ; và loss không phải thước quyết
định), nhưng nó chỉ biện minh cho việc **không dùng loss để chọn**, không biện minh cho việc
**không đo loss**. Hai chuyện khác nhau: `exec` là thước để chọn và báo, loss val là thước để
**chẩn đoán**.

### Lấy lại cho lượt đang chạy — `harness/loss_val_grid.py`, Kaggle T4, 0 đồng

Không phải dừng train, và phủ được cả phần đã chạy qua vì mỗi thư mục trong `grid/` là một adapter
chấm được độc lập.

```bash
# ① ở nhà, 0 GPU — dựng nhánh val một lần (đi qua chính build_branch_data.py nên khuôn mẫu khớp)
python3 harness/build_branch_data.py --recs-file val_cham400.jsonl \
    --out harness/dg1_cache/train_ac/branches_val400 \
    --img-prefix /kaggle/working/thesis/harness/dg1_cache/train_ac/
# ⇒ 607 mẫu (val_cham400 có 607 bước, trong đó 400 là bước chạm)

# ② trên Kaggle T4 — nối tiếp được, bỏ qua bước đã chấm
python3 harness/loss_val_grid.py --grid <grid> \
    --branches harness/dg1_cache/train_ac/branches_val400 --every 500
```

⚠️ T4 là Turing, **không có bf16** ⇒ script tự đổi fp16. Mọi điểm lưu chấm cùng một cách nên so
với nhau được; ⛔ đừng đặt cạnh loss train của lượt A100 (bf16).
⚠️ Đã chạy thử phần quét lưới và dựng cấu hình trên WSL; phần `run_exp` với `eval_dataset` **chưa
chạy thật lần nào** vì máy nhà không có GPU.

**Đọc kết quả:** loss val quay đầu **tăng** ở đâu thì đó là mốc quá khớp ⇒ thu hẹp vùng cần chấm
`exec` ở A6 từ 78 điểm lưu xuống vài cái. ⛔ **Không** chọn điểm lưu cuối cùng bằng loss val, và
như mọi số val: **không trích ra báo**.
⭐ Nếu điểm lưu tốt nhất theo `exec` lệch hẳn khỏi cực tiểu loss val, đó là **một số đo mới đáng
vào bài**: bằng chứng nữa cho việc loss không thay được `exec`, cùng họ với hệ số truyền 0,028.

### Lượt sau (hạt 202, hoặc bất kỳ lượt train mới nào) — bật ngay từ đầu

⭐ Thêm bốn khoá vào cấu hình **trước khi mã hoá token**, vì đổi sau là cache mất hiệu lực:

```yaml
eval_dataset: gui_s1_val        # nhánh dựng từ val_cham400.jsonl, KHÁC dataset dạy
eval_strategy: steps
eval_steps: 400
per_device_eval_batch_size: 2
```

⛔ **Vẫn giữ `val_size: 0.0`** — việc chia val do `tach_val.py` làm, tách theo **episode** và phân
tầng theo `action_type`. Để trainer tự chia là chia ngẫu nhiên theo dòng, mà màn hình trong cùng
một tác vụ na ná nhau ⇒ rò rỉ và cho điểm ảo.
⚠️ Giá: mỗi lần eval trên 607 mẫu tốn vài phút GPU; với `eval_steps: 400` thì ~20 lần cho cả lượt.
Đó là giá đáng trả để có đường cong, nhưng phải tính vào ngân sách từ đầu.

---

## ⭐ Ô G8 — CƠ CHẾ CẮT LỖ, hai điểm kiểm (Kaggle T4, 0 đồng)

Lượt này **không có dừng sớm tự động**, và đó là cố ý. Trainer chỉ dừng được theo **mất mát**, mà
`151` cấm đúng chỗ ấy: mất mát đo việc khớp chuỗi đích, còn thứ cần đo là câu sinh ra có đủ để một
mô hình độc lập trỏ trúng nút hay không. Chặng ba đã cho thấy hai đại lượng ấy lệch nhau: nâng
tầng khai báo $2{,}56$ điểm mà điểm thực thi chỉ nhích $0{,}02$.

⛔ **Cũng không dùng early stopping theo *patience*.** Trên $400$ bước chạm, sai số chuẩn ghép cặp
là $\approx 1{,}03$ điểm. Nếu đường cong thật đang tăng đều $+0{,}3$ điểm mỗi $800$ bước — tức mô
hình đang học tốt — thì xác suất một lần đánh giá bất kỳ *trông như* giảm vẫn khoảng $38\%$. Với
`patience = 2` thì gần như chắc chắn có lúc dừng oan giữa một lượt đang lên. Muốn an toàn phải đặt
`patience` 4–5, và khi đó nó gần như không bao giờ kích hoạt, tức trả giờ A100 cho một cơ chế
không làm gì.
⭐ **Thứ thay thế nó tốt hơn đã có sẵn: 40 điểm lưới.** Chạy hết rồi chọn điểm tốt nhất là early
stopping làm *sau*, khi đã thấy toàn bộ đường cong — không bao giờ dừng oan, và nếu đường cong đạt
đỉnh giữa lượt rồi thoái hoá thì vẫn lấy được đỉnh. Chi phí thêm: **0 giờ A100**.

⇒ Vậy G8 chỉ làm đúng một việc: **cắt lỗ**. Không tìm điểm tối ưu, chỉ bắt trường hợp hỏng nặng và
trường hợp đã rõ là không lên nữa.

### Hai điểm kiểm, hai luật khác nhau — khoá TRƯỚC khi nhìn số

| | bước | câu hỏi | mốc so | ⛔ dừng nếu |
|---|---|---|---|---|
| **K1** | **3.200** (~40%) | có hỏng nặng không | **MIN-DESC** trên cùng val | thấp hơn mốc **quá 3,0 điểm** |
| **K2** | **4.800** (~60%) | còn lên nữa không | **chính K1** | thấp hơn K1 **quá 3,0 điểm** |

⭐ **Vì sao đúng hai bước này:** cả `step03200` lẫn `step04800` đều nằm trong năm điểm mà A6 sẽ
chấm sau lượt, nên công chấm ở đây **không phí** — chạy hết lượt thì đã có sẵn 2 trong 5 điểm,
tiết kiệm ngược lại ~1,5 h T4.

⭐ **Vì sao ngưỡng 3,0 điểm:** đó là $\approx 3$ lần sai số chuẩn ghép cặp trên 400 bước chạm. Đủ
rộng để nhiễu không kích hoạt, đủ chặt để bắt được sụp đổ thật.

⛔ **Không dừng khi chỉ "chưa tốt hơn".** Biên cắt lỗ phải một phía và rộng: bỏ khi **rõ ràng tệ
hơn**, không bỏ khi **chưa tốt hơn**. Mô hình có thể còn đang trong pha học.
⛔ **Không nới ngưỡng sau khi thấy số.** Dự án đã tự khai hai lần nới ngưỡng sau khi thấy điểm.
⚠️ K2 **không** dừng vì thoái hoá nhẹ — thoái hoá nhẹ là chuyện của A6, và grid đã giữ đỉnh rồi.
K2 chỉ dừng khi giảm mạnh, tức lượt đã hỏng chứ không phải đã qua đỉnh.

### ⛔ KẾT QUẢ K1 — đo 10/9/2026 ~22:00 giờ VN (Kaggle T4, n = 400 bước chạm, 132 cụm)

| | `exec` Voronoi trên `val_cham400` | KTC95 | `hit_disk` |
|---|---|---|---|
| MIN-DESC (mốc) | **67,25** | [61,6 · 73,1] | 74,25 |
| VIS-SFT `step03200` | **59,75** | [54,6 · 65,1] | 68,25 |
| **chênh** | **−7,50** | | −6,00 |

⇒ **Vượt ngưỡng dừng 3,0 điểm của K1.** Ba yếu tố làm phép so bất lợi cho VIS-SFT (mốc là MIN chứ
không phải S1 · MIN đã học qua val, val−test của MIN = +7,20 · điểm lưu mới 41% lượt, chưa hết một
lượt duyệt dữ liệu) đều có thật, nhưng **không được dùng để nới ngưỡng**. Tệp thô
`score_*_raw.jsonl` nằm ở `/kaggle/working` của phiên đó, **chưa tải về kho**.
⛔ Số val, cấm trích ra báo.

**13/9:** user kiểm Drive — `grid/` **không có `step07800`**, gốc `output_dir` không có adapter cuối ⇒ lượt **không chạy tới cuối** và **không chạy tiếp** (luật K1). Ghi trong luận văn là *dừng theo tiêu chí cắt lỗ đặt trước*, không trích số val.

### ✅ THI HÀNH 10/9 — gói dữ liệu đã dựng sẵn, chỉ còn lấy adapter và upload

**Đã làm ở nhà (0 GPU):** `_bundles/thesis_val_cham.zip` — **808 MB**

| trong gói | nội dung |
|---|---|
| `val_cham400.jsonl` · `val_cham600.jsonl` | 607 và 960 bước (400 và 602 bước chạm) |
| `ocr.jsonl` | **1.567 dòng**, lọc theo trường `image` (⛔ `train_ac/ocr.jsonl` KHÔNG có `episode_id`/`step_id`) |
| `images/` | **1.567 ảnh**, 767 MB — phủ trọn cả hai tập, dùng lại được cho A6 |

⭐ Cây trợ năng **không cần đóng gói**: `a11y_inventory` tự tải `all_forest_dict.zip` từ
HuggingFace, nên chỉ cần bật Internet cho notebook Kaggle.

**Còn phải làm — lấy hai adapter:**

① MIN đã có trong kho ở `runs/grpo_point/adapter_ref_min/` (2 tệp).
② `step03200` nằm trên Drive. Lấy bằng **Terminal Colab** (⛔ không chạy ô notebook, nhân Python
đang bận ô G7):

```bash
cd /content/drive/MyDrive/thesis/ckpt/vissft_seed101
mkdir -p /content/k1 && cp -r grid/step03200 /content/k1/vissft_step03200
ls -la /content/k1/vissft_step03200
cd /content && zip -0 -qr /content/drive/MyDrive/thesis/k1_adapter.zip k1
```

Tải `k1_adapter.zip` từ drive.google.com về máy, gộp với `adapter_ref_min/` thành **một** zip rồi
tạo dataset Kaggle mới `thesis-k1-adapters`. ⛔ Dataset MỚI, đừng "New Version".

**Chạy trên Kaggle** (dataset: `thesis-val-cham` · `thesis-k1-adapters` · `thesis-code-9-9`),
theo bốn ô đầu của `harness/kaggle_phase1_noisuy_9_9.md` (Ô 0 gỡ `torchao`, Ô 1 dựng `WS`,
Ô 2 hàm `chay_va_cho`), rồi hai lượt cho mỗi adapter:

```python
for ten, ad in [("moc_min", f"{AD}/adapter_ref_min"),
                ("vissft_3200", f"{AD}/vissft_step03200")]:
    chay_va_cho(["python", "harness/infer_branch.py", "--adapter", ad,
                 "--data-root", f"{WS}/valdata", "--recs-file", "val_cham400.jsonl",
                 "--out", f"/kaggle/working/preds_{ten}.jsonl"])
    chay_va_cho(["python", "harness/score_run.py",
                 "--preds", f"/kaggle/working/preds_{ten}.jsonl",
                 "--data-root", f"{WS}/valdata", "--recs-file", "val_cham400.jsonl",
                 "--out", f"/kaggle/working/score_{ten}.json"])
```

⚠️ **Kiểm dòng `[dữ liệu] …`** mà cả hai script in ra — đó là chỗ duy nhất xác nhận đang đọc
`val_cham400.jsonl` chứ không phải `test.jsonl`.
⚠️ **Thời gian chưa đo:** suy từ tỉ lệ với lượt 4.463 bước (5,6 h) thì 607 bước ≈ **1,2 h cho mỗi
adapter**, tức ~2,5 h T4 cho cả hai. Đây là **suy luận**, không phải số đo; chạy lượt MIN trước rồi
lấy giờ thật mà tính.

**Đọc kết quả theo luật đã khoá ở bảng trên**, và nhớ chiều thiên vị: val là dữ liệu MIN **đã
thấy** (MIN train trên trọn 64.567 bước) còn VIS-SFT train trên 63.000 đã trừ val ⇒ phép so này
**bất lợi cho VIS-SFT**. VIS-SFT vượt MIN là bằng chứng mạnh; thua thì chỉ dùng để bắt sụp đổ,
⛔ không đọc thành "VIS-SFT kém hơn".

---

### Bước 0 — chấm mốc MIN, làm bất cứ lúc nào trong 20 giờ đầu

Mốc phải đo trên **chính** `val_cham400.jsonl`, không dùng lại con số nào của chặng 3 (chặng 3
chấm trên val cũ 262 bước, khác tập). Adapter MIN đã có sẵn trong kho nên chấm được ngay.

⛔ **Trên Kaggle, phải chạy trước bốn ô của `harness/kaggle_phase1_noisuy_9_9.md`:** Ô 0 (gỡ
`torchao`), Ô 1 (dựng workspace — nó đặt `WS`), Ô 1b nếu thiếu ảnh, và **Ô 2 (hàm
`chay_va_cho`)**. Hai đoạn dưới đây dùng lại `WS` và `chay_va_cho` từ đó; chạy thẳng mà chưa có
chúng là `NameError`.
⚠️ Ô 1 của runbook ấy dò `val400.jsonl`; lượt này cần `val_cham400.jsonl` nên sửa hai chỗ dò tệp
và bỏ hai `assert` md5 với số dòng 407 (val mở rộng là **607 bước / 400 chạm**).

Rồi đổi ba chỗ:

```python
# dataset: thesis-val-cham (1.567 ảnh) + thesis-code-9-9 + thesis-adapters-noisuy
chay_va_cho(["python", "harness/infer_branch.py",
             "--adapter", f"{AD}/adapter_ref_min",
             "--data-root", f"{WS}/valdata", "--recs-file", "val_cham400.jsonl",
             "--out", "/kaggle/working/preds_moc_min.jsonl"],
            "/kaggle/working/infer_moc.log", dich="/kaggle/working/preds_moc_min.jsonl",
            can=607, nhip=120)
chay_va_cho(["python", "harness/score_run.py", "--mode", "score",
             "--preds", "/kaggle/working/preds_moc_min.jsonl",
             "--data-root", f"{WS}/valdata", "--recs-file", "val_cham400.jsonl",
             "--out", "/kaggle/working/score_moc_min.json"],
            "/kaggle/working/score_moc.log", nhip=120)
import json
MOC = 100 * json.load(open("/kaggle/working/score_moc_min.json"))["exec_voronoi"]
print(f"MỐC MIN trên val_cham400 = {MOC:.2f}  (n phải là 400)")
```

⭐ Ghi con số này lại. Nó là mốc cho cả K1 lẫn A6.

### Bước 1 — trên Colab, đóng gói điểm lưu khi tới bước cần kiểm

```python
import os, shutil, glob
GRID = f"{D}/ckpt/vissft_seed101/grid"
for b in ("step03200", "step04800"):
    src = f"{GRID}/{b}"
    if os.path.isdir(src) and not os.path.exists(f"/content/{b}.zip"):
        shutil.make_archive(f"/content/{b}", "zip", src)
        print("đã đóng gói", b, "→ tải về rồi upload thành dataset Kaggle")
print("grid hiện có:", sorted(os.path.basename(x) for x in glob.glob(f"{GRID}/step*"))[-4:])
```

### Bước 2 — trên Kaggle, chấm và đọc verdict

```python
import json, glob, os
MOC = 0.00        # ⛔ điền con số đã đo ở Bước 0, đừng để 0
K   = "step03200" # hoặc "step04800"
# dò thư mục điểm lưu vừa upload, ở BẤT KỲ độ sâu nào — đừng ghim tên dataset vào đường dẫn
c = glob.glob(f"/kaggle/input/**/{K}/adapter_config.json", recursive=True) \
    or glob.glob("/kaggle/input/**/adapter_config.json", recursive=True)
assert c, f"không thấy điểm lưu {K} trong /kaggle/input — chạy Ô 0b để xem mount gì"
CKPT_DIR = os.path.dirname(sorted(c)[0])
print("[điểm lưu]", CKPT_DIR)
chay_va_cho(["python", "harness/infer_branch.py",
             "--adapter", CKPT_DIR,
             "--data-root", f"{WS}/valdata", "--recs-file", "val_cham400.jsonl",
             "--out", f"/kaggle/working/preds_{K}.jsonl"],
            f"/kaggle/working/infer_{K}.log", dich=f"/kaggle/working/preds_{K}.jsonl",
            can=607, nhip=120)
chay_va_cho(["python", "harness/score_run.py", "--mode", "score",
             "--preds", f"/kaggle/working/preds_{K}.jsonl",
             "--data-root", f"{WS}/valdata", "--recs-file", "val_cham400.jsonl",
             "--out", f"/kaggle/working/score_{K}.json"],
            f"/kaggle/working/score_{K}.log", nhip=120)

d = json.load(open(f"/kaggle/working/score_{K}.json"))
e = 100 * d["exec_voronoi"]
assert d["n"] == 400, f"n={d['n']} ≠ 400 — chấm nhầm tập"
print(f"{K}: {e:.2f}   (mốc {MOC:.2f}, chênh {e-MOC:+.2f})")
print("⛔ DỪNG LƯỢT" if e < MOC - 3.0 else "✅ chạy tiếp — chênh chưa tới −3,0 điểm")
```

⚠️ Với **K2** thì đổi `MOC` thành điểm đã đo ở K1, không phải mốc MIN.

⚠️ **Đây là nhìn val giữa chừng.** Hợp lệ vì val vốn dùng để chọn điểm lưu và vì luật dừng đã khoá
trước, nhưng phải khai trong luận văn rằng lượt có hai điểm kiểm giữa chừng; nếu lượt bị dừng thì
nêu rõ dừng ở bước nào theo tiêu chí nào.

**Tổng chi phí G8:** ~2 h T4 miễn phí (mốc + hai điểm kiểm), **0 giờ A100**, và trả lại ~1,5 h T4
ở khâu A6 vì hai điểm đã chấm sẵn.

---

## Sau lượt — A6 chọn điểm lưu

Chấm năm điểm lưu `step01600 · step03200 · step04800 · step06400 · step07800` trên
`val_cham400.jsonl` (**400 bước chạm**), rồi hai điểm tốt nhất cùng hai điểm lưu kề bên mỗi cái
trên `val_cham600.jsonl` (**602 bước chạm**). Chạy trên **Kaggle T4 miễn phí**, dùng cờ
`--data-root` và `--recs-file` của bản vá P5.

⭐ Nếu đã chạy G8 thì **`step03200` và `step04800` đã chấm rồi** — dùng lại, chỉ còn ba điểm.
⛔ **Điểm lưới cuối là `step07800`, không phải `step08072`.** Lượt này chạy $7.876$ bước vì tập dạy
là $63.000$ mẫu đã trừ val, và `save_steps: 200` nên điểm lưới cuối rơi vào bước $7.800$. Adapter
của bước cuối cùng nằm ở **gốc** `output_dir`, không nằm trong `grid/`.

⛔ **Chọn theo val 600, không phải val 400** — val 400 đã bị dùng để lọc nên nó thiên vị lạc quan.
⛔ **Không bao giờ trích một con số val nào ra báo.** Đo được ngày 9/9: val cao hơn test ~7,5 điểm
và phóng đại khoảng cách giữa hai nhánh gần 40 lần.
⭐ Lấy **đỉnh đường cong đã làm trơn**, không lấy gai đơn lẻ.

## A7 — chấm test

Khoá điểm lưu, khai thứ bậc **trước**, rồi chấm test hai cấu hình: **A** = điểm lưu cuối ·
**B** = argmax-val. Báo **cả hai vô điều kiện**.
⇒ Nếu A7 vượt **60,07** thì chạy hạt giống 202 (~25 h A100). Không vượt thì dừng, ghi ngắn, tiêu
đề vẫn 60,07.

---

## 📓 Nhật ký sự cố — lượt 9/9/2026

Ghi lại để lượt sau khỏi mò. Cả ba lỗi đều bị chặn **trước** khâu tốn tiền.

| # | triệu chứng | nguyên nhân | cách xử |
|---|---|---|---|
| 1 | `FileNotFoundError: images/ep8690_s0.png` ở G4, sau khi đã nạp model | bộ `branches_tru_val` dựng thiếu `--img-prefix` nên trường `images` ghi đường dẫn **tương đối**; LLaMA-Factory mở ảnh theo thư mục làm việc | dựng lại với `--img-prefix {TR}/`, đóng gói và upload lại. Nay ô **G2** kiểm đường dẫn phải bắt đầu bằng `/` và mở thử ảnh mẫu |
| 2 | `ModuleNotFoundError: llamafactory.extras.callbacks` ở G5, giây thứ 10 | `LogCallback` đổi chỗ giữa các bản. Bản pin `c4e09c7cbe18` để nó ở **`llamafactory.train.callbacks`** | ô **G4c** dò; `chay_vissft.py` bản 9/9 tự dò bốn đường |
| 3 | lỗi 2 lặp lại sau khi đã vá | ô G5 **tự ghi lại** `chay_probe.py` mỗi lần chạy, nên nó xoá bản vá | dùng ô G5 bản 9/9, trong đó phần sinh `chay_probe.py` đã có vòng dò sẵn |
| 6 | ô theo dõi G5t in cột `log` và `cache` **trống**, chỉ có `GPU 0 %` | lượt đang chạy là bản G5 cũ (`capture_output`) nên không có `/content/probe.log`; còn thư mục mã hoá chỉ được ghi **một lần khi xong**, không lớn dần ⇒ không cột nào là chỉ báo sống | dùng khối thứ hai của **G5t**: cột **CPU toàn máy** (hiệu số `/proc/stat` giữa hai lần đo). Mã hoá chạy 8 tiến trình con nên CPU phải cao; CPU ≤ 2 % hai lần liên tiếp mới là treo |
| 7 | smoke chạy 45 phút mới phát hiện **chưa bật G4b** | ô G4b bị bỏ qua, `cfg_probe.yaml` không có `tokenized_path` ⇒ bản mã hoá nằm ở `/root/.cache`, **mất theo máy ảo** | dừng smoke, chạy G4b, chạy lại G5. Trả giá một lần ~1 h còn hơn để lượt thật và mỗi lần mất máy cùng trả 2,5 h. Nay G4b có cảnh báo **không bỏ qua** và một lệnh `grep` kiểm ngay sau G5 |
| 5 | ô G5 im lặng suốt, không biết còn sống hay treo | `subprocess.run(capture_output=True)` giữ toàn bộ đầu ra tới khi tiến trình kết thúc | đổi sang `Popen` ghi ra tệp + vòng in nhịp sống mỗi phút, kèm cỡ cache mã hoá |
| 4 | `TypeError: can only concatenate list (not "str") to list` ở `hf_argparser`, giây thứ 10 | `run_exp` nhận **dict**, không nhận đường dẫn chuỗi. `report/151` §4 viết `run_exp(args="…yaml")` — mẫu ấy **sai** với bản pin | `run_exp(args=yaml.safe_load(open(CFG)), callbacks=cbs)`. Đã sửa trong `chay_vissft.py` và trong ô G5 |

⭐ **Kết quả G4 trên máy thật:** đóng băng cho `14.966.784` tham số huấn luyện, mở ra cho
`18.576.384`, chênh `3.609.600` tức **+24,1%**. Con số nhánh đóng băng **khớp đúng** mốc mà
`report/151` ghi, nên phép so hai lượt vừa xác nhận cờ, vừa xác nhận mốc của tài liệu.

⚠️ **Bài học chung, đã lặp lại lần thứ ba trong dự án:** ô nào *sinh ra* tệp mã thì mỗi lần chạy
lại sẽ **ghi đè** mọi bản vá tay. Vá phải nằm trong chính ô sinh ra tệp, không nằm ở ô riêng.

---

## Bốn luật Colab (đã trả giá, đừng học lại)

1. **`start_new_session=True`** — thiếu là mọi lần bấm Stop đều giết train.
2. **KHÔNG bấm Stop ô nào** khi train chạy; cần ô khác thì mở notebook thứ hai.
3. **Ô theo dõi đọc log LOCAL**, không đọc tệp trên Drive — FUSE không cập nhật khi ghi thêm.
4. **Phải có một ô foreground suốt lượt**, nếu không Colab ngắt máy sau ~90 phút không hoạt động.
