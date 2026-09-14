# Chặng 3 — Phase 1 của `report/151`: hiệu chuẩn val, nội suy MIN↔GRPO, soup (viết 9/9/2026)

Máy: **Kaggle T4×2 miễn phí**, hạn mức 30 h GPU/tuần, **0 đồng**. Không dùng A100.
Kế hoạch tổng: `report/152` §3. Nguồn khoa học: `report/151` §5.

| bước | việc | ở đâu | giá | trạng thái |
|---|---|---|---|---|
| B1–B3 | dựng val, kéo ảnh, dựng 5 adapter nội suy | **WSL** | 0 GPU | ✅ **xong 9/9** |
| B4 | upload ba dataset | Kaggle | 0 | ⏳ **2/3** — mã ✅ · adapter ✅ · **`thesis-val` chưa lên** |
| **B5+B6** | **V1 và V2 gộp** — chấm 5 mức α trên val 400 | Kaggle | **~4 h T4** | ▶️ **việc kế, ô dán ở dưới** |
| B7 | **V3** soup ba adapter | Kaggle | ~4 h T4 | chưa |
| B8 | **V4** khoá một α, chấm test một lần | Kaggle | ~5,6 h T4 | chưa |

**Tổng còn lại ~14 h T4.** Rải hai tuần cho vừa hạn mức.
⭐ V1 gộp vào V2 vì `a0.00` chính là MIN và `a1.00` chính là GRPO — xem đầu mục B5+B6. ⚠️ Kỳ vọng ghi trước: **+0,2…+0,5 pp, có thể
bằng 0** (`151` §5.2). Đây không phải lượt để kỳ vọng đổi tiêu đề.

---

## ⛔ Bốn điều phải đọc trước, nếu không sẽ chạy ra số vô nghĩa

**① Val là dữ liệu ba mô hình ĐÃ THẤY.** S1, MIN, GRPO đều train trên trọn 64.567 bước, mà val
tách ra từ chính tập đó. Nên điểm val của chúng là điểm *train*, lạc quan có hệ thống.
· Dùng được cho: V1 (chỉ để bắt thảm hoạ) và xếp hạng α trong V2/V3 (cả 5 ứng viên lạc quan như
  nhau nên so tương đối vẫn công bằng).
· ⛔ Không dùng được cho: bất kỳ con số nào đem báo.
· ⚠️ Còn một thiên lệch tinh vi: điểm α ở giữa bị pha trọng số nên **mất phần ghi nhớ val nhanh
  hơn mất năng lực thật** ⇒ val **thiên vị chống lại** điểm giữa. Hệ quả đọc kết quả: điểm giữa
  thắng trên val là bằng chứng **mạnh**; thua thì **không kết luận được gì**.

**② Ảnh của val KHÔNG có sẵn** (✅ đã xử lý 9/9). `harness/dg1_cache/train_ac/images/` trước đó
chỉ có **1.697 ảnh** của lát thử 29/7, không phải 64.567. Đã kéo về **6.774 ảnh / 1.733 episode**
bằng `harness/keo_anh_val.py` — bước B2.

**③ ⛔⛔ ĐỪNG chạy `build_train_data.py --shards k` để lấy ảnh.** Hàm `build()` (dòng 157) **ghi
đè `train.jsonl`** và chỉ lấy `k` shard **đầu** ⇒ tệp 64.567 dòng của bạn thành ~850×k dòng, và
không có gì báo. Dùng script riêng ở B2.

**④ ⚠️ Mẫu số của `exec` là 262, KHÔNG phải 407** (đo trên WSL 9/9). `tach_val.py` chia theo
**mọi** bước, còn `score_run.py:451` chỉ chấm bước **chạm**: val400 có 262 `click` + 0
`long_press`, val600 có 391. Suy luận vẫn chạy đủ 407 bước — chỉ khâu chấm co lại.
⇒ **Ba sai số chuẩn của `151` §1.2bis phải nhân lại** theo $\sqrt{4437/262}=4{,}12$ thay cho
$\sqrt{4437/400}=3{,}33$:

| | `151` ghi (n=400) | **thật (n=262)** |
|---|---|---|
| SE không ghép cặp | 2,45 pp | **3,03 pp** |
| SE ghép cặp GRPO−MIN | 1,03 pp | **1,27 pp** |
| SE ghép cặp MIN−S1 | 1,88 pp | **2,32 pp** |

Hệ quả: ngưỡng *"không cách nhau > 3 SE"* ở Ô 7 là **≈ 9 pp**, không phải 7; kiểm mềm #3 là
**2,32 pp**, không phải 1,88. Luật chọn α **≥ 2,0 pp giữ nguyên** (nó khoá trước, không nới
theo số đo), nhưng phải biết rằng 2,0 pp nay chỉ còn **1,6 SE** chứ không phải 1,9 SE ⇒ đường
cong càng phải phẳng thì càng không được lấy điểm giữa.

---

## B1 + B2 — dựng val và kéo ảnh (một script, chạy trên WSL)

⭐ **Thứ tự ngược với trực giác:** không chọn val trước rồi đi tìm ảnh, mà **kéo ảnh của 8 shard
rải đều trước**, rồi cho `tach_val.py` chọn val **chỉ trong các episode đã có ảnh**. Lý do: val
rải trên toàn 76 shard thì phải tải gần hết 12 GB; ràng buộc vào 8 shard chỉ tốn ~1,3 GB.

⚠️ **Phải khai khi viết:** val không ngẫu nhiên trên toàn tập dạy mà ngẫu nhiên **trong 8 shard**.
Chọn shard **rải đều** (0, 10, 21, 32, 43, 54, 65, 75) chứ không phải 8 shard liền nhau, để giảm
tương quan với thứ tự thu thập dữ liệu.

### Bước B1a — sao lưu tệp không được phép mất

```bash
cd /mnt/d/Master/Thesis
cp harness/dg1_cache/train_ac/train.jsonl harness/dg1_cache/train_ac/train.jsonl.bak_9_9
md5sum harness/dg1_cache/train_ac/train.jsonl*    # ghi lại, đối chiếu ở B1d
wc -l harness/dg1_cache/train_ac/train.jsonl      # phải là 64567
```

### Bước B1b — script kéo ảnh, `harness/keo_anh_val.py`

⛔ Script này **chỉ ghi ảnh**, không đụng `train.jsonl`. Nếu bản bạn gõ ra có bất kỳ dòng nào mở
`train.jsonl` ở chế độ `"w"` thì đã chép sai.

```python
# -*- coding: utf-8 -*-
"""Keo anh tap DAY cho cac buoc nam trong 8 shard rai deu, de dung val.
   python3 harness/keo_anh_val.py           # ~1,3 GB, 10-20 phut
⛔ KHONG ghi de train.jsonl. Chi ghi anh + mot danh sach khoa.
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
IMG  = os.path.join(ROOT, "images")            # ghi chung cho vao day
SHARDS = [0, 10, 21, 32, 43, 54, 65, 75]       # rai deu tren 76
IMG_REPO = "ckg/AndroidControlParsedWithImages-20k"   # ⛔ doi chieu bien IMG_REPO
                                                      #    trong build_train_data.py

def main():
    from huggingface_hub import hf_hub_download
    import pyarrow.parquet as pq
    can = {(int(r["episode_id"]), int(r["step_id"]))
           for r in map(json.loads, open(os.path.join(ROOT, "train.jsonl"), encoding="utf-8"))}
    os.makedirs(IMG, exist_ok=True)
    co = []
    for i in SHARDS:
        p = hf_hub_download(IMG_REPO, f"data/train-{i:05d}-of-00076.parquet",
                            repo_type="dataset")
        pf = pq.ParquetFile(p)
        n = 0
        for b in pf.iter_batches(batch_size=100):
            for r in b.to_pylist():
                j = r["json"]
                if isinstance(j, (bytes, str)):
                    j = json.loads(j)
                k = (int(j["episode_id"]), int(j["step_id"]))
                if k not in can:
                    continue
                ten = f"ep{k[0]}_s{k[1]}.png"
                with open(os.path.join(IMG, ten), "wb") as f:
                    f.write(r["png"]["bytes"])
                co.append(k); n += 1
        del pf
        print(f"  shard {i:02d}: +{n} anh")
    json.dump([list(k) for k in co],
              open(os.path.join(ROOT, "khoa_co_anh.json"), "w"), indent=0)
    print(f"TONG {len(co)} anh / {len({k[0] for k in co})} episode -> khoa_co_anh.json")

if __name__ == "__main__":
    main()
```

```bash
grep -n "IMG_REPO" harness/build_train_data.py     # ⛔ đối chiếu tên kho trước khi chạy
~/.venvs/thesis/bin/python harness/keo_anh_val.py  # cần huggingface_hub + pyarrow
```

Kết quả thật 9/9: **6.774 ảnh / 1.733 episode**, ~1,3 GB tải về.

### Bước B1c — `tach_val.py` ✅ ĐÃ VIẾT VÀ ĐÃ CHẠY (9/9)

`harness/tach_val.py` đã có trong kho, đã thi hành P4 và đã chạy xong. ⚠️ Đoạn lọc theo ảnh phác
trong bản đầu của runbook này có logic sai (vòng lặp lồng, và không đúng nghĩa *"episode đủ
ảnh"*); bản trong kho dùng hàm `episode_du_anh()` chạy tuyến tính và định nghĩa đúng: một episode
đủ ảnh khi **mọi** bước của episode ấy đều có ảnh đã kéo về.

```bash
PYTHONIOENCODING=utf-8 python3 harness/tach_val.py
```

Kết quả thật, ngày 9/9:

```
train.jsonl: 64567 bước / 12895 episode
đủ ảnh:      4525 bước / 1045 episode
  val400.jsonl             407 bước /    90 episode
  val600.jsonl             604 bước /   128 episode
  train_tru_val.jsonl    63556 bước / 12677 episode
  val400: lệch phân bố lớn nhất 0.78 pp OK
  val600: lệch phân bố lớn nhất 1.14 pp OK
```

Bốn phép kiểm trong script đều đạt: hai lát không chung episode · $407+604+63.556 = 64.567$ ·
không rò rỉ ở mức bước · không trùng bước trong val. ⚠️ `val600` ra $604$ chứ không tròn $600$ vì
đơn vị chia là episode; đừng "sửa" cho tròn số.

⚠️ Con số *"đủ ảnh 4.525 bước"* nhỏ hơn 6.774 ảnh đã kéo, vì nhiều episode chỉ có một phần bước
nằm trong 8 shard, và episode như vậy bị loại khỏi vùng chọn val. Vẫn dư cho 1.011 bước val.

### Bước B1d — kiểm chưa phá gì

```bash
md5sum harness/dg1_cache/train_ac/train.jsonl harness/dg1_cache/train_ac/train.jsonl.bak_9_9
wc -l harness/dg1_cache/train_ac/{train.jsonl,val400.jsonl,val600.jsonl,train_tru_val.jsonl}
```
⛔ Hai md5 **phải trùng** (đã kiểm 9/9: `a6be1fafbe91…` cho cả hai).

---

## B3 — dựng năm adapter nội suy (WSL, 0 GPU)

### B3a — kéo adapter khỏi Drive (P6)

Hai adapter nằm cùng `MyDrive/thesis/ckpt/grpo_point_seed101/`: `adapter_grpo_point_seed101/`
(GRPO) và `adapter_ref_min/` (MIN). Đặt vào `runs/grpo_point/` đúng hai tên đó.

⛔ **Tải bằng trình duyệt thì kiểm tên tệp**: peft tìm **đúng chuỗi** `adapter_model.safetensors`;
trình duyệt hay lưu thành `adapter_model (1).safetensors` và peft **không nhận** — bài học đã ghi
ở `kaggle_grpo_point_6_9.md:142`.

```bash
ls -la runs/grpo_point/adapter_ref_min/ runs/grpo_point/adapter_grpo_point_seed101/
python3 -c "
import json
for d in ('adapter_ref_min','adapter_grpo_point_seed101'):
    c=json.load(open(f'runs/grpo_point/{d}/adapter_config.json'))
    print(d, 'r=',c['r'], 'alpha=',c['lora_alpha'], 'rank_pattern=',bool(c.get('rank_pattern')))"
```
⚠️ Nếu `rank_pattern` hoặc `alpha_pattern` khác rỗng thì `noi_suy.py` phải nhân đôi cả các giá
trị bên trong, nếu không vài module giữ `scaling` cũ và bạn trộn sai một phần mạng.

### B3b — `harness/noi_suy.py` ✅ ĐÃ VIẾT VÀ ĐÃ CHẠY (9/9)

Điểm sống còn: **ghép nối theo hạng**, không bình quân riêng `lora_A` rồi riêng `lora_B`, vì
ΔW = scaling·B·A là **tích** chứ không phải tổng.

⚠️ **Hai chỗ `151` §5.3bis ghi khác thực tế, đã đo lại 9/9:**
· `151` viết `r: 16 → 32`; bộ adapter thật có **r = 8, lora_alpha = 16**. `noi_suy.py` đọc từ
  `adapter_config.json` chứ không viết số cứng — số cứng sẽ làm sai `scaling` gấp đôi mà không
  có gì báo.
· `151` viết cách trộn thẳng sai **65%** tại α=0,5; đo thật trên cặp này chỉ **0,0163%**, vì GRPO
  học tiếp từ MIN nên chỉ dịch chuyển `lora_A` **1,39%** và `lora_B` **6,87%**, mà số hạng chéo tỉ
  lệ với tích hai độ lệch ấy. Con số 65% chỉ đúng cho hai adapter huấn luyện độc lập.
  ⭐ Vẫn dùng ghép nối vì nó đúng tới sai số máy (≤ 2,2e−07 ở mọi α) và không tốn thêm gì.
  ⭐ **Hệ quả cho V2:** hai đầu mút gần nhau tới mức đó nghĩa là đường cong theo α gần như phẳng,
  nên kỳ vọng +0,2…+0,5 pp của `151` có thể còn lạc quan.

```bash
~/.venvs/thesis/bin/python harness/noi_suy.py     # ra runs/noisuy/a0.00 … a1.00
```
Kết quả 9/9: mỗi mức 504 tensor · r 8→16 · lora_alpha 16→32 · scaling giữ nguyên 2.

### B3c — P7, `--alpha` ✅ ĐÃ VÁ (9/9)

`infer_branch.py` nay có `--alpha`, nhân thẳng vào `mod.scaling`. ⚠️ Cờ này **co giãn một adapter
so với model gốc**, nó KHÔNG dựng được điểm giữa của hai adapter — việc đó là của `noi_suy.py`.
Lượt V2 dùng adapter đã ghép sẵn ở `runs/noisuy/`, để `--alpha` nguyên giá trị mặc định 1,0.

---

## B4 — upload ba dataset Kaggle ✅ (xong 9/9)

| dataset | upload cái gì | cỡ | trạng thái |
|---|---|---|---|
| `thesis-val` | thư mục `_bundles/thesis_val/` (1.011 ảnh + `val400.jsonl` + `val600.jsonl` + `ocr_val.jsonl`) | 509 MB | ⏳ **CHƯA có trên Kaggle** — Ô 0b ngày 9/9 không thấy trong `/kaggle/input` |
| `thesis-adapters-noisuy` | `_bundles/thesis_adapters_noisuy.zip` — 7 thư mục `a0.00`…`a1.00` + `adapter_ref_min` + `adapter_grpo_point_seed101`, mỗi cái đúng 2 tệp | 657 MB | ✅ mount 9/9, đủ 7 bộ |
| `thesis-code-9-9` | `_bundles/harness_code_9_9.zip` (8 tệp, md5 `d5181238b27c`) | 53 KB | ✅ mount 9/9 |

⭐ **Nén `.zip` được, Kaggle tự bung khi tạo dataset** (chỉ `.tar` mới bị giữ nguyên — đó là chỗ
ghi chú cũ của dự án nói tới). Gói adapter nén ở chế độ *store* vì `safetensors` là dữ liệu dấu
phẩy động, nén cũng gần như không nhỏ đi, mà store thì đóng gói nhanh hơn nhiều.

⛔⛔ **Đường dẫn mount đo thật 9/9 — KHÁC hẳn điều bản trước của file này ghi.** Bản trước nói
*"zip không có tầng thư mục bọc ngoài, đường dẫn là `/kaggle/input/thesis-adapters-noisuy/a0.50/`"*.
**Sai cả hai vế.** Thật ra:

```
/kaggle/input/datasets/<user>/thesis-code-9-9/harness/infer_branch.py
/kaggle/input/datasets/<user>/thesis-adapters-noisuy/thesis_adapters_noisuy/a0.50/…
```

Có **hai** tầng phụ không đoán trước được: `datasets/<username>/` do Kaggle chèn, và một tầng
bọc ngoài trùng tên gói do bung `.zip`. ⇒ **Đừng ghim tên dataset vào đường dẫn** — Ô 1 dò theo
**tên tệp mốc** (`infer_branch.py`, `val400.jsonl`, `a0.50/adapter_config.json`) trên toàn
`/kaggle/input`, nên layout nào cũng chạy. Không thấy gì thì chạy **Ô 0b** để nhìn mount thật.

⛔ **Gói mã phải là dataset MỚI, đừng dùng New Version của `thesis-sel-infer`.** Bài học 5/9:
"New Version" của Kaggle **thêm** thư mục chứ không thay thế, nên nhiều gói cùng tồn tại trong
`/kaggle/input` và ô dò chọn theo thời gian sửa là chọn mò. Dataset mới thì không có chỗ để lẫn.

⭐ Gói mã này đã có bản vá **P5** (`--data-root`, `--recs-file` cho cả `infer_branch.py` lẫn
`score_run.py`) và **P7** (`--alpha`). Kiểm ngay sau khi mount:

```python
import glob
s = open(sorted(glob.glob("/kaggle/input/**/infer_branch.py", recursive=True))[0]).read()
assert "--data-root" in s and '"--alpha"' in s, "gói mã CŨ — upload nhầm bản"
```

✅ **Gói `thesis_val` đã dựng sẵn ở `_bundles/thesis_val/`** (1.011 bước · 1.011 ảnh · OCR đủ
1.011 dòng). Dựng lại được bằng cách lọc `val400.jsonl` + `val600.jsonl` rồi chép ảnh theo trường
`image`; ⚠️ lọc OCR phải khoá theo **`image`** chứ không phải cặp `(episode_id, step_id)`, vì
`train_ac/ocr.jsonl` không có hai trường ấy.

⛔⛔ **Mẹo symlink `test_ac` → `val_ac` của bản trước đã BỎ.** Bản trước dùng nó để né việc sửa mã,
nhưng **P5 nay đã làm thật**: cả `infer_branch.py` lẫn `score_run.py` đều nhận `--data-root` và
`--recs-file`. Dùng cờ, đừng dùng symlink — Phase 2 phải chấm val và test xen kẽ nên symlink sẽ
thành bẫy, và nó cũng che mất dòng `[dữ liệu] …` vốn là chỗ duy nhất kiểm được đang đọc tập nào.

---

## ⭐ B5 + B6 gộp làm một lượt — V1 và V2 chạy chung

⛔ **Adapter S1 không có trong kho** (chỉ nằm trên Drive), nên V1 theo đúng chữ của `151` cần thêm
một lượt tải nữa. Không cần: **`a0.00` chính là MIN và `a1.00` chính là GRPO**, nên chấm 5 mức α
đã cho luôn hai trong ba nhánh của V1. Hai phép kiểm bắt thảm hoạ ① và ② ở `151` §1.2bis đọc được
ngay trên hai đầu mút ấy. Phép kiểm ③ cần S1, nhưng nó là kiểm **mềm** với công suất dưới 10%, nên
để tuỳ chọn: nếu sau này tải adapter S1 về thì chấm thêm một lượt 407 bước là xong.

⇒ Lượt này **~4 h T4**, thay cho 3 h + 4 h của hai lượt tách rời.

### Ô 0 — gỡ `torchao` (⛔ ô ĐẦU TIÊN, kể cả khi chạy lại)

```python
!pip uninstall -y -q torchao
!python -c "import importlib.util; print('torchao còn:', importlib.util.find_spec('torchao'))"
```
Phải in `torchao còn: None`. Kaggle cài sẵn `torchao 0.10.0` còn `peft` ở đây đòi > 0.16 và ném
`ImportError` **ngay lúc gắn LoRA**, tức sau khi đã tải xong mô hình nền.

### Ô 0b — chẩn đoán: Kaggle mount những gì, ở đâu (2 giây, chạy khi Ô 1 báo không thấy tệp)

```python
import os
for r, ds, fs in os.walk("/kaggle/input"):
    print(r.replace("/kaggle/input", "") or "/", "→",
          (fs[:6] + ["…"] if len(fs) > 6 else fs))
```

⚠️ **Đường dẫn mount KHÔNG phải `/kaggle/input/<tên-dataset>/`.** Đo thật 9/9: Kaggle chèn thêm
tầng `datasets/<username>/`, và gói `.zip` bung ra **có** thư mục bọc ngoài trùng tên gói:

```
/kaggle/input/datasets/<user>/thesis-code-9-9/harness/infer_branch.py
/kaggle/input/datasets/<user>/thesis-adapters-noisuy/thesis_adapters_noisuy/a0.50/…
```

⇒ ⛔ **Đừng ghim tên dataset vào đường dẫn** — slug, tầng username và tầng bọc ngoài đều đổi
theo tài khoản lẫn theo cách Kaggle bung gói. Ô 1 dưới đây dò theo **tên tệp mốc**, nên layout
nào cũng chạy.

### Ô 1b — kéo 1.011 ảnh val thẳng từ HuggingFace (chạy MỘT lần, nếu Ô 1 báo thiếu ảnh)

⭐ **Đừng upload 531 MB từ nhà.** Kaggle đang bật Internet, ảnh vốn nằm trên HuggingFace, và
khoá của 1.011 bước đã có sẵn trong `val400/val600.jsonl` đang mount. Kéo thẳng trên Kaggle
nhanh hơn hẳn đường lên của máy nhà, và **0 đồng**. Cùng logic `harness/keo_anh_val.py` đã chạy
thật ngày 9/9 (ra 6.774 ảnh), chỉ đổi nguồn khoá và chỗ ghi.

⚠️ Tải ~1,3 GB parquet để lấy ra ~507 MB ảnh, chừng 5–10 phút. Ghi vào `/kaggle/working` nên
**sống qua Save Version**, chạy lại lần sau tự bỏ qua.

```python
import os, json, glob
IMGV = "/kaggle/working/val_images"; os.makedirs(IMGV, exist_ok=True)
if len(glob.glob(f"{IMGV}/ep*_s*.png")) >= 1011:
    print("đã đủ ảnh, bỏ qua")
else:
    from huggingface_hub import hf_hub_download
    import pyarrow.parquet as pq
    V = os.path.dirname(sorted(glob.glob("/kaggle/input/**/val400.jsonl", recursive=True))[0])
    can = set()
    for t in ("val400.jsonl", "val600.jsonl"):
        for r in map(json.loads, open(f"{V}/{t}", encoding="utf-8")):
            can.add((int(r["episode_id"]), int(r["step_id"])))
    print("cần", len(can), "ảnh")
    for i in [0, 10, 21, 32, 43, 54, 65, 75]:      # ⛔ đúng 8 shard mà val bị ràng vào
        p = hf_hub_download("ckg/AndroidControlParsedWithImages-20k",
                            f"data/train-{i:05d}-of-00076.parquet", repo_type="dataset")
        pf, n = pq.ParquetFile(p), 0
        for b in pf.iter_batches(batch_size=100):
            for r in b.to_pylist():
                j = r["json"]
                if isinstance(j, (bytes, str)):
                    j = json.loads(j)
                k = (int(j["episode_id"]), int(j["step_id"]))
                if k not in can:
                    continue
                with open(f"{IMGV}/ep{k[0]}_s{k[1]}.png", "wb") as f:
                    f.write(r["png"]["bytes"])
                n += 1
        del pf
        os.remove(p)                                # ⛔ xoá parquet ngay, đĩa Kaggle có hạn
        print(f"  shard {i:02d}: +{n}", flush=True)
    print("TỔNG", len(glob.glob(f"{IMGV}/ep*_s*.png")), "ảnh →", IMGV)
```

⛔ **`os.remove(p)` không bỏ được.** Tám shard là ~1,3 GB, cộng 507 MB ảnh; giữ hết parquet là
ăn gần 2 GB `/kaggle/working` mà chẳng dùng lại lần nào.

**Đường lùi nếu Kaggle chặn HuggingFace:** upload `_bundles/thesis_val.zip` (531 MB, 1.011 ảnh
+ 3 jsonl, dựng 9/9) thành **dataset mới**, rồi **gỡ** `thesis-val` cũ khỏi notebook để không
có hai bản `val400.jsonl` cùng lúc.

### Ô 1 — dựng workspace và kiểm đúng ba dataset

```python
import os, glob, zipfile, shutil, hashlib, json
WS = "/kaggle/working/ws"; os.makedirs(WS, exist_ok=True)

def tim(mau, gi):
    """Dò một tệp mốc ở BẤT KỲ độ sâu nào dưới /kaggle/input, trả đường dẫn đầu tiên."""
    p = sorted(glob.glob(f"/kaggle/input/**/{mau}", recursive=True))
    assert p, f"không thấy {gi} (mẫu '{mau}') trong /kaggle/input — chạy Ô 0b để xem mount gì"
    if len(p) > 1:
        print(f"  ⚠️ {gi}: {len(p)} bản, lấy {p[0]}")
    return p[0]

# ── mã ──────────────────────────────────────────────────────────────────────
c = glob.glob("/kaggle/input/**/infer_branch.py", recursive=True)
if c:
    shutil.copytree(os.path.dirname(sorted(c)[0]), f"{WS}/harness", dirs_exist_ok=True)
else:                                    # Kaggle giữ nguyên .zip
    zipfile.ZipFile(tim("*code*.zip", "gói mã")).extractall(WS)
s = open(f"{WS}/harness/infer_branch.py").read()
assert "--data-root" in s and '"--alpha"' in s, "GÓI MÃ CŨ — upload nhầm bản, dừng lại"
print("[mã] có P5 và P7 ✓")

# ── val ─────────────────────────────────────────────────────────────────────
VAL = os.path.dirname(tim("val400.jsonl", "gói val"))
r = open(f"{VAL}/val400.jsonl", "rb").read()
print(f"[val] {VAL} · {r.count(bytes(chr(10),'ascii'))} dòng · md5 {hashlib.md5(r).hexdigest()[:12]}")
assert r.count(b"\n") == 407, "val400 phải có 407 dòng"
assert hashlib.md5(r).hexdigest().startswith("8db4ed0067a4"), "val400 KHÁC bản ở máy nhà"
# infer/score đọc ảnh theo trường 'image' tương đối, nên val_ac phải có images/ ngay cạnh
os.makedirs(f"{WS}/valdata", exist_ok=True)
# ⛔ val tách từ train.jsonl nên khoá câu chuẩn tên là 'target_instruction', trong khi
#    infer_branch.py:638 và score_run.py:570 đều đòi 'gold_instruction' ⇒ KeyError ngay
#    bước đầu. Thêm bí danh lúc chép; ⛔ đừng sửa tệp gốc, md5 ở trên phải giữ nguyên.
for t in ("val400.jsonl", "val600.jsonl"):
    with open(f"{VAL}/{t}", encoding="utf-8") as fi, \
         open(f"{WS}/valdata/{t}", "w", encoding="utf-8") as fo:
        for d in map(json.loads, fi):
            d.setdefault("gold_instruction", d["target_instruction"])
            fo.write(json.dumps(d, ensure_ascii=False) + "\n")
shutil.copy(f"{VAL}/ocr_val.jsonl", f"{WS}/valdata/ocr.jsonl")   # ⭐ đổi tên: script tìm ocr.jsonl
d = json.loads(open(f"{WS}/valdata/val400.jsonl", encoding="utf-8").readline())
assert "gold_instruction" in d, "bí danh chưa được thêm — dừng lại"
# ⛔ Đừng giả định ảnh nằm ở "{VAL}/images": Kaggle có thể bỏ tầng đó, hoặc rải 1.011 png
#    thẳng vào gốc dataset. Dò theo TÊN ẢNH rồi mới nối. ⚠️ symlink hỏng thì os.path.exists
#    trả False nhưng os.symlink vẫn ném FileExistsError ⇒ phải hỏi islink trước.
lk = f"{WS}/valdata/images"
if os.path.islink(lk):
    os.remove(lk)
png = (glob.glob(f"{VAL}/**/ep*_s*.png", recursive=True)
       or glob.glob("/kaggle/input/**/ep*_s*.png", recursive=True)
       or glob.glob("/kaggle/working/val_images/ep*_s*.png"))   # ← chỗ Ô 1b ghi ra
assert png, ("không thấy ảnh val (ep*_s*.png) trong /kaggle/input lẫn /kaggle/working — "
             "gói thesis-val lên thiếu ảnh, chạy Ô 1b để kéo thẳng từ HuggingFace")
IMGDIR = os.path.dirname(sorted(png)[0])
if not os.path.exists(lk):
    os.symlink(IMGDIR, lk)
n_anh = len(glob.glob(f"{IMGDIR}/ep*_s*.png"))
print(f"[val] ảnh: {n_anh} ← {IMGDIR}")
assert n_anh == 1011, f"phải có 1.011 ảnh, thấy {n_anh} — gói val lên thiếu"

# ── adapter ─────────────────────────────────────────────────────────────────
a = glob.glob("/kaggle/input/**/a0.50/adapter_config.json", recursive=True)
if a:                                    # Kaggle đã bung — lùi HAI tầng: a0.50/ rồi thư mục cha
    AD = os.path.dirname(os.path.dirname(sorted(a)[0]))
else:                                    # Kaggle giữ nguyên .zip
    zipfile.ZipFile(tim("*adapters*.zip", "gói adapter")).extractall("/kaggle/working/adapters")
    AD = "/kaggle/working/adapters"
    if not os.path.exists(f"{AD}/a0.50"):        # zip có thư mục bọc ngoài
        AD = os.path.dirname(glob.glob(f"{AD}/**/a0.50", recursive=True)[0])
MUC = ["a0.00", "a0.25", "a0.50", "a0.75", "a1.00"]
for a in MUC:
    for t in ("adapter_config.json", "adapter_model.safetensors"):
        assert os.path.exists(f"{AD}/{a}/{t}"), f"thiếu {a}/{t}"
c = json.load(open(f"{AD}/a0.50/adapter_config.json"))
assert c["r"] == 16 and c["lora_alpha"] == 32, f"r/alpha sai: {c['r']}/{c['lora_alpha']}"
print(f"[adapter] {AD} — đủ 5 mức · r={c['r']} lora_alpha={c['lora_alpha']} (đã nhân đôi ✓)")
```

⛔ Ba `assert` ở trên là chỗ chặn duy nhất trước khi tiêu 4 giờ máy. Bài học 20/8: đọc mã chỉ
chứng minh mã trên máy này, phải bắt tiến trình **in ra cấu hình nó thật sự dùng** rồi kiểm dòng đó.

### Ô 2 — hàm chạy-và-chờ

```python
import subprocess, time

def chay_va_cho(cmd, log, dich=None, can=None, nhip=120, moi=True):
    env = {**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1",
           "HF_HUB_DISABLE_PROGRESS_BARS": "1"}
    if moi and os.path.exists(log):
        os.remove(log)
    f = open(log, "a")
    P = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT,
                         start_new_session=True, env=env, cwd=WS)
    t0 = time.time()
    while P.poll() is None:
        time.sleep(nhip)
        n = sum(1 for _ in open(dich)) if dich and os.path.exists(dich) else -1
        gio = (time.time() - t0) / 3600
        eta = (gio * (can - n) / n) if (can and n > 0) else float("nan")
        print(f"{time.strftime('%H:%M:%S')} · {gio:5.2f} h · {n}/{can or '?'} · "
              f"còn ~{eta:.1f} h", flush=True)
    print("mã thoát:", P.returncode, flush=True)
    print(subprocess.run(["tail", "-25", log], capture_output=True, text=True).stdout)
    assert P.returncode == 0, "DỪNG: tiến trình thoát khác 0 — đọc log ở trên"
```

⚠️ Hai biến môi trường là chỗ đã trả giá **7 giờ** ngày 17/8: `tqdm` ngoài terminal in mỗi cập
nhật thành một dòng, Kaggle chặn log khi vượt trần, tiến trình kẹt cứng ở lệnh ghi stdout.

### Ô 3 — probe 3 bước, chạy TRƯỚC khi cam kết cả lượt

```python
chay_va_cho(["python", "harness/infer_branch.py",
             "--adapter", f"{AD}/a0.00",
             "--data-root", f"{WS}/valdata", "--recs-file", "val400.jsonl",
             "--limit", "3", "--out", "/kaggle/working/probe.jsonl"],
            "/kaggle/working/probe.log", nhip=30)
print(open("/kaggle/working/probe.jsonl").read()[:600])
```
⭐ Đọc dòng `[dữ liệu] …` trong log: phải là `.../valdata/val400.jsonl`. Sai chỗ này thì mọi con
số sau đều là của tập khác, và không có gì báo lỗi.

### Ô 4 — suy luận 5 mức α (~1,5 h)

```python
for a in MUC:
    out = f"/kaggle/working/preds_val_{a}.jsonl"      # ⛔ α PHẢI có trong tên tệp
    if os.path.exists(out) and sum(1 for _ in open(out)) >= 407:
        print("bỏ qua, đã xong:", a); continue
    print("=" * 60, "\n", a, flush=True)
    chay_va_cho(["python", "harness/infer_branch.py",
                 "--adapter", f"{AD}/{a}",
                 "--data-root", f"{WS}/valdata", "--recs-file", "val400.jsonl",
                 "--out", out],
                f"/kaggle/working/infer_{a}.log", dich=out, can=407, nhip=120)
```
⛔ Nếu để chung một `--out` cho cả 5 mức thì hoặc ghi đè lẫn nhau, hoặc script thấy tệp đã có rồi
bỏ qua — và bạn sẽ chấm cùng một bộ dự đoán năm lần, ra năm con số giống hệt nhau mà tưởng là
đường cong phẳng.

### Ô 5 — ⭐ PHÉP KIỂM HAI ĐẦU MÚT, làm TRƯỚC khi chấm

```python
import json
def cau(p):
    return {(r["episode_id"], r["step_id"]): r.get("raw", "")
            for r in map(json.loads, open(p, encoding="utf-8"))}
a0, a1 = cau("/kaggle/working/preds_val_a0.00.jsonl"), cau("/kaggle/working/preds_val_a1.00.jsonl")
k = set(a0) & set(a1)
khac = sum(1 for i in k if a0[i] != a1[i])
print(f"n={len(k)} · số bước α=0 và α=1 sinh câu KHÁC nhau: {khac} ({100*khac/len(k):.1f}%)")
assert khac > 0, "hai đầu mút sinh câu y hệt nhau ⇒ adapter không được nạp, hoặc nạp nhầm cùng một bộ"
```
⭐ Phép kiểm này **phải làm trên CÂU, không trên điểm**: MIN và GRPO chênh `exec` chỉ 0,02 pp nên
nạp lẫn hai đầu mút thì điểm không phát hiện được. `runs/grpo_point/README.md:19-20` cảnh báo đúng
bẫy ấy.
⚠️ Bản đầy đủ của phép kiểm là so với hai tệp preds đã commit ở máy nhà
(`preds_grpo_point_seed101.jsonl` và `preds_min_desc_seed101.jsonl`). Không làm được trực tiếp ở
đây vì hai tệp ấy sinh trên **tập kiểm**, còn lượt này chạy trên **val**. Cách so đúng là tải hai
tệp preds val về máy nhà rồi đối chiếu ở đó — xem ô B6 dưới.

### Ô 6 — chấm 5 mức (~2,5 h)

```python
for a in MUC:
    out = f"/kaggle/working/score_val_{a}.json"
    if os.path.exists(out): print("bỏ qua:", a); continue
    print("=" * 60, "\n", a, flush=True)
    chay_va_cho(["python", "harness/score_run.py", "--mode", "score",
                 "--preds", f"/kaggle/working/preds_val_{a}.jsonl",
                 "--data-root", f"{WS}/valdata", "--recs-file", "val400.jsonl",
                 "--out", out],
                f"/kaggle/working/score_{a}.log",
                # ⭐ score_run.py:489 tự suy tên tệp thô từ --out và ghi dần có flush,
                #    nên đếm được. Thiếu hai tham số này thì suốt 2,5 h chỉ thấy
                #    "-1/? · còn ~nan h", tức mất tín hiệu để áp luật "4 phút không
                #    có nhịp sống thì dừng".
                dich=f"/kaggle/working/score_val_{a}_raw.jsonl", can=262, nhip=120)
```

⚠️ **Ô 6 tải thêm hai thứ lần chạy đầu:** bộ trỏ `UGround-V1-2B` và `all_forest_dict.zip` (cây
trợ năng 99.131 màn, cần cho `buttons_of` dựng danh sách nút của luật Voronoi). Vài phút, và
`dich` chưa có tệp nên mấy nhịp đầu vẫn in `-1`. Sau đó phải thấy số chạy lên tới **262**.
⛔ Mạng tắt thì `buttons_of` trả danh sách rỗng, Voronoi suy biến, mà **không có gì báo lỗi** —
giữ Internet ON.

### Ô 7 — đọc kết quả

```python
import json
# ⛔ Khoá đúng là 'exec_voronoi' và nó là TỈ LỆ 0–1, phải nhân 100.
#    'exec_disk' KHÔNG phải thước tiêu đề — đó là hit_disk THUẦN, không gated (bẫy tên trường
#    đã ghi ở CLAUDE.md; đọc thẳng nó cho 66,35 thay vì 63,86).
print(f"{'α':>6} {'exec':>8} {'n':>6}")
diem = {}
for a in MUC:
    d = json.load(open(f"/kaggle/working/score_val_{a}.json"))
    e = 100 * d["exec_voronoi"]
    diem[a] = e
    assert d["n"] == 262, f"n={d['n']} ≠ 262 bước chạm của val400 — chấm nhầm tập"
    print(f"{a:>6} {e:>8.2f} {d['n']:>6}")
lo, hi = diem["a0.00"], diem["a1.00"]
giua = max(diem[a] for a in ("a0.25", "a0.50", "a0.75"))
print(f"\nhai đầu mút: MIN {lo:.2f} · GRPO {hi:.2f}")
print(f"điểm giữa cao nhất: {giua:.2f} — hơn đầu mút tốt hơn {giua - max(lo, hi):+.2f} pp")
print("→ chỉ được lấy làm cấu hình chính nếu vượt ≥ 2,0 pp; không đạt thì khoá α=0")
```

**Đọc theo `151` §1.2bis, đây là phép thử BẮT THẢM HOẠ:**

| # | kiểm | ngưỡng | không đạt thì sao |
|---|---|---|---|
| 1 | hai đầu mút rơi trong **50–70** | bắt buộc | đường chấm hỏng — **dừng, đi sửa**, đừng chạy tiếp |
| 2 | năm mức không cách nhau > **3 SE ≈ 9 pp** (n=262, xem điều ④) | bắt buộc | val trúng lát lệch nặng — đổi `SEED` trong `tach_val.py`, chia lại |
| 3 | S1 không cao hơn trung bình MIN và GRPO quá **2,32 pp** | mềm, **cần adapter S1** | ⛔ không đạt cũng đừng dừng, công suất dưới 10% |

⚠️ **Kỳ vọng ghi trước, đọc trước khi nhìn số:** +0,2…+0,5 pp, và **có thể bằng 0**. Đo trên chính
hai adapter này, GRPO chỉ dịch chuyển `lora_A` **1,39%** và `lora_B` **6,87%** so với MIN, nên
đường cong theo α gần như phẳng và kỳ vọng ấy có thể còn lạc quan. Trên 2 pp thì phải soi kỹ hơn
bình thường trước khi tin.
⚠️ Và nhớ thiên lệch đã nêu ở đầu file: val là dữ liệu cả MIN lẫn GRPO **đã thấy**, còn điểm α ở
giữa mất phần ghi nhớ ấy nhanh hơn mất năng lực thật ⇒ val **thiên vị chống lại** điểm giữa. Điểm
giữa **thắng** là bằng chứng mạnh; **thua** thì không kết luận được gì.

### Ô 8 — đóng một gói zip rồi tải về máy nhà

⭐ Tải **một** tệp thay vì mười lăm: bấm nhầm một tệp là mất một lượt đối chiếu, mà tổng cỡ chỉ
vài MB. ⛔ Nhớ lấy cả `*_raw.jsonl` — tệp thô là tài sản, đổi luật chấm sau này tính lại được
**không gọi lại bộ trỏ** (đã cứu trọn một lượt 5,6 h hồi tháng 8).

```python
import zipfile, glob, os, hashlib
Z = "/kaggle/working/ket_qua_noisuy.zip"
mau = ["preds_val_a*.jsonl", "score_val_a*.json", "score_val_a*_raw.jsonl",
       "infer_a*.log", "score_a*.log"]
with zipfile.ZipFile(Z, "w", zipfile.ZIP_DEFLATED) as z:
    n = 0
    for m in mau:
        for p in sorted(glob.glob(f"/kaggle/working/{m}")):
            z.write(p, os.path.basename(p)); n += 1
print(f"{n} tệp → {Z} · {os.path.getsize(Z)/2**20:.1f} MB")
print("md5", hashlib.md5(open(Z, "rb").read()).hexdigest())
for i in zipfile.ZipFile(Z).infolist():
    print(f"  {i.filename:34} {i.file_size:>10,} B")
```

Tải `ket_qua_noisuy.zip` ở panel **Output** bên phải, rồi bung vào `runs/noisuy/`:

```bash
cd /mnt/d/Master/Thesis
unzip -o ~/Downloads/ket_qua_noisuy.zip -d runs/noisuy/
ls -la runs/noisuy/*.json runs/noisuy/*.jsonl | head -20
```

⛔ Đặt thẳng vào thư mục của phép đo đó, đừng để lạc chỗ khác — đã có lần bốn tệp lạc vào
`report/papers/`, mất một lượt dọn.

---

## B7 — V3: soup ba adapter (~4 h T4)

Ba adapter cùng họ `<desc>`: **MIN · GRPO · CE2-S2/101**, mỗi cái hệ số **1/3**. Dùng lại
`noi_suy()` nhưng ghép **ba** khối ⇒ `r ×3`, `lora_alpha ×3`.

⛔ **Chỉ trung bình ĐỀU.** Không dò hệ số bằng Optuna hay tiến hoá: cực đại của hàng trăm phép thử
trên val có SE ~1,03 pp là máy sinh số ngẫu nhiên.
⛔ **Không đưa S1 hay `gui_sel` vào** — chúng không sinh `<desc>` (S1 `action_ok` 94,35 so 98,86
của họ `<desc>`) nên định dạng đầu ra khác, trộn vào là nguy cơ sụp đổ biểu diễn.
⚠️ Nếu CE2 khác `r` với hai cái kia (kiểm ở B3a) thì **bỏ CE2, soup hai cái**.

---

## B8 — V4: khoá một α, chấm test một lần (~5,6 h T4)

1. Chọn **đúng một** cấu hình trên val (một α, hoặc soup).
2. Ghi vào `report/106` mục sửa đổi **TRƯỚC KHI** chấm test — ghi cả lý do chọn và số val.
3. Chấm test **một lần**, trên đủ **4.463** bước, bằng đường chấm test bình thường
   (`harness/kaggle_cham_min_desc.md`), tức để `--data-root` và `--recs-file` ở giá trị mặc định.
4. Báo **vô điều kiện**, kèm **cả hai đầu mút** (MIN 60,05 và GRPO 60,07).

⛔ Không chấm cả 5 mức trên test rồi khoe mức cao nhất.
⛔ Nó chỉ thành **tiêu đề** nếu vượt đầu mút trên val ≥ **2,0 pp**. Kỳ vọng +0,2…+0,5 nên gần như
chắc chắn không đạt ⇒ tiêu đề vẫn **60,07**, và số nội suy vào luận văn như **một hàng bảng có
thật**, không phải nhan đề.

---

## Bốn luật chung của lượt Kaggle (đã trả giá, đừng học lại)

1. **Chạy tương tác trước, Save Version sau.** Commit bị huỷ thì Kaggle không lưu `/kaggle/working`.
2. **Tắt thanh tiến trình, cho tiến trình con ghi ra tệp** (`Popen(stdout=f)`), cộng nhịp sống in
   mỗi 2 phút. `tqdm` ngoài terminal từng làm treo một commit **7 giờ**.
3. **Không có dòng nhịp sống nào sau 4 phút thì dừng ngay.**
4. **Kết quả trùng nhau tới nhiều chữ số giữa các cấu hình KHÁC nhau là dấu hiệu HỎNG**, không
   phải dấu hiệu bền vững — bắt tiến trình **in ra cấu hình nó thật sự đang dùng** rồi kiểm dòng
   đó, đừng kiểm mã nguồn.
