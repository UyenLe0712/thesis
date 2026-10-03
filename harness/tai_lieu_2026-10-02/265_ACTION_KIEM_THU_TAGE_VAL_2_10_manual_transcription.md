# 265 — ACTION: kiểm thử TAGE trên val C1 trước khi chạy thật (2/10/2026)

> Bản chép lại thủ công từ 8 ảnh chụp màn hình trong file ZIP.
>
> Mình ưu tiên độ chính xác theo nội dung nhìn thấy trên ảnh. Những đoạn code/hash/path khó đọc được giữ nguyên theo phần nhìn rõ nhất; không tự suy đoán phần bị khuất.

Gửi nguyên file này cho chat thực thi. File tự chứa: script ở Phụ lục A–B, cách dùng bằng phần từ lệnh cần ở Phụ lục C, ô dùng để điều chỉnh ở Phụ lục D.

## 0. Trả lời ngắn

Vẫn chốt TAGE. Sau khi bỏ ràng buộc t4, TAGE vẫn đứng đầu trong tám ứng viên (8.70/10). Lượt này có thêm bằng chứng từ chính val của ck500 [mục 1], củng cố lựa chọn đó.

TAGE là gì — **Type-Aware Grounded Editor**, bộ biên tập câu được định vị vùng đích. Hệ chạy bốn bước:

1. ck500 viết câu nháp như hiện nay, ví dụ `Click on the share option`.
2. Một bộ định vị đọc ảnh màn hình, mục tiêu và lịch sử, rồi chỉ ra điểm cần chạm.
3. Cắt một vùng ảnh quanh điểm đó (crop). Một bộ biên tập (LoRA riêng trên Qwen2.5-VL-3B) nhìn cả màn hình, vùng crop và câu nháp, rồi viết lại câu. Nếu câu nháp gọi sai phần tử, bộ biên tập sửa theo vùng crop.
4. Một cổng giữ/sửa chỉ nhận câu sửa khi bộ biên tập đủ tự tin. Không thì giữ câu nháp, để không phá những câu ck500 đã đúng.

Khác PATAVFGR trước đây: tín hiệu vùng đích không phải một nhánh phụ mà decoder có thể lờ đi. Bộ biên tập được train từ đầu để đọc crop, có thêm một loss tương phản: câu đúng phải dễ sinh hơn khi crop đúng phần tử so với khi crop phần tử lân cận. UGround không dùng trong train hay suy luận, chỉ để chấm.

Phải kiểm trên val trước. Lượt này không chạy thật, chỉ trả lời ba câu hỏi theo thứ tự rẻ đến đắt:

| cổng | câu hỏi | nếu không đạt |
|---|---|---|
| V1 | Cho crop đúng tuyệt đối (điểm chạm vàng), bộ biên tập có sửa được ck500 không? Crop sai phần tử có làm nó tệ đi không? | Dừng TAGE. Crop hoàn hảo mà không giúp thì bộ định vị vô ích |
| V2 | Bộ định vị tự học có chỉ đúng phần tử ở những bước ck500 đang sai không? | Bộ định vị cần thêm dữ liệu train trước khi làm V3 |
| V3 | Ghép thật: crop dự đoán + cổng giữ/sửa có hơn ck500 không, và có hơn bộ biên tập không crop không? | Báo người dùng, chưa chạy thật |

## 1. Bối cảnh và mốc phải vượt

Luận văn sinh câu hướng dẫn một bước cho màn hình Android (AndroidControl). S1V0 là Qwen2.5-VL-3B + LoRA SFT, ck500 là S1 sau 500 bước GRPO thưởng SPICE, mốc hiện tại cần vượt. `exec` nghĩa là UGround-V1-2B đọc câu rồi bấm trúng khi đáng lẽ theo tác vụ và đúng phần tử (Voronoi, dung sai ±14%).

Val C1 là 400 bước lấy từ 1.567 bước val bằng:

```python
random.Random(20260927).sample
```

trong đó có 249 bước click.

Số dưới đây máy nhà tính ngày 2/10 từ:

- `runs/grpo_spice/score_ck500_raw.jsonl`
- `runs/c1/exec8/c1score/score_AE_raw.jsonl`

Trên 249 bước click val C1:

|  | S1 greedy | ck500 |
|---|---:|---:|
| exec | 63,45 (158) | 66,27 (165) |

84 bước ck500 sai:

| loại lỗi | số bước |
|---|---:|
| đúng loại thao tác, điểm bấm ngoài đĩa ±14% (gọi sai phần tử) | 63 |
| đúng loại thao tác, trong đĩa nhưng sai ô Voronoi (trỏ nhầm phần tử sát bên) | 17 |
| sai loại thao tác | 4 |

Thêm hai số đo:

- Trong 84 bước sai, **52 bước không có câu nào trong 9 câu của S1** (greedy + 8 mẫu nhiệt độ 1,0) thực thi được. Chọn lại câu (reranker, best-of-N) không cứu được các bước này, vì câu đúng không nằm trong phân phối. Muốn cứu phải đưa thêm thông tin, ở đây là vùng đích. Đây là lý do TAGE thắng speaker-listener reranker.
- Trần chọn câu (ck500, hoặc câu nào trong 9 câu S1 thực thi được): **79,12**. Trần này dùng câu người để chọn, không phải hệ thật.

Mốc của lượt này là **ck500 = 165/249 trên val C1**. Đây là val, S1 đã thấy val lúc SFT. Không trích số nào vào luận văn.

## 2. Thiết kế thí nghiệm

Mọi nhánh dùng cùng nền: S1 hoà vào Qwen gốc (`s1_merged`), cùng ảnh, cùng câu nhắc như lúc sinh ck500. Câu nháp ở val là đúng câu ck500 đã sinh và đã chấm (`pred_ck500.jsonl`), nên hiệu số so với ck500 là hiệu số ghép cặp.

### 2.1 Dữ liệu train

- 2.5x bước click train trong `fgrb-p1-bundle` (4.000 bước train có ảnh), không chung episode nào với val. Selftest in đúng số.
- Câu nháp train: ck500 sinh greedy + 2 mẫu nhiệt độ 1,0 cho từng bước (`--make-drafts`). S1 đã học train lúc SFT, nên câu greedy trên train thường gần câu người. Mẫu nhiệt độ 1,0 và câu làm hỏng dưới đây bù cho chuyện đó; script in tỉ lệ greedy trùng câu người.
- Câu nháp làm hỏng: với xác suất 0,3 thay tên phần tử đúng bằng tên phần tử lân cận cùng vai trò (từ `tage_neg.jsonl`). Đo trên máy nhà: khoảng **58% bước click train làm hỏng được**, nên khoảng **17% mẫu dạy sửa lỗi gọi sai phần tử**.
- Crop: hình vuông cạnh 40% bề ngang ảnh, tâm tại điểm chạm, resize 448×448 (256 token ảnh).
- Crop nhiễu cho loss tương phản: phần tử lân cận cùng vai trò (`point_neg_abs`, phủ khoảng 91% bước click train). Không có thì lấy mục OCR gần nhất nằm ngoài crop đúng.

### 2.2 Các nhánh

| nhánh | bộ biên tập train với | crop lúc chạy val | trả lời |
|---|---|---|---|
| `gold` | crop vàng + loss tương phản | vàng (điểm chạm thật) | trần của TAGE nếu bộ định vị hoàn hảo |
| `neg` | cùng bộ biên tập `gold` | phần tử lân cận gần nhất ngoài crop vàng | bộ biên tập có thật sự đọc crop không |
| `none` | không crop, cùng dữ liệu và số bước | không | lợi ích có phải chỉ do train thêm LoRA không |
| `pred` | cùng bộ biên tập `gold` | điểm do bộ định vị dự đoán | hệ thật |

Mỗi nhánh có thêm bản `+cổng`. Cổng sửa khi `lp_edit - lp_draft > τ`: hiệu log-xác suất trung bình mỗi token của câu sửa và câu nháp, dưới chính bộ biên tập. Chọn τ chéo theo episode: chọn trên nửa episode này, áp lên nửa kia, nên không tự chấm trên chỗ đã chọn. Cổng tính offline trên máy nhà, không tốn GPU.

Bộ định vị có hai bản, đều là LoRA r=16 sinh `(x, y)` thang 0–1000:

- `loc_g`: chỉ đọc ảnh, mục tiêu và lịch sử.
- `loc_d`: đọc thêm câu nháp ck500. Lúc train dùng ngẫu nhiên greedy hoặc mẫu nhiệt độ 1,0.

Lấy bản trúng nhiều hơn trên 80 bước ck500 trở sai làm điểm cho nhánh `pred`.

### 2.3 Siêu tham số mặc định (được đổi nếu cần, ghi lại khi đổi)

LoRA r = 16, alpha 32, dropout 0,05, chỉ trên tầng ngôn ngữ (không đụng tháp thị giác); lr 1e-4; warmup 30 bước; 2 epoch; b1, tích luỹ 8; λctr = 0,5; margin m = 0,2 nat/token; p_hỏng = 0,3; bf16 trên L4/A100, fp16 + GradScaler trên T4.

## 3. Ngưỡng đi tiếp

Đây không phải ngưỡng cho luận văn. Chúng chỉ để quyết có tốn thêm GPU hay không. Người dùng cho phép tối ưu tự do trên val, nên nếu muốn đổi siêu tham số rồi chạy lại thì cứ làm, nhưng ghi lại mỗi lần chạy kèm số.

| cổng | đi tiếp khi | dừng khi |
|---|---|---|
| V1 | `gold` hoặc `gold+cổng` hơn ck500 ≥ +4 điểm (≥ 10 bước ròng), và `gold` hơn `neg` ≥ +4 điểm | `gold+cổng ≤ ck500 + 1 điểm`: crop hoàn hảo không giúp, dừng TAGE |
| V2 | bộ định vị tốt hơn trúng đĩa ≥ 20/80 bước ck500 trở sai | < 10/80: cần train bộ định vị trên toàn bộ 41 nghìn bước click trước, báo người dùng |
| V3 | `pred+cổng` hơn ck500 ≥ +1,5 điểm và hơn `none+cổng` | còn lại: báo người dùng |

Giữa hai cột thì báo người dùng quyết. Với 249 bước, khoảng tin cậy 95% của một hiệu số ròng khoảng ±4–5 điểm. Vì vậy V3 đạt chỉ là tín hiệu hướng; phải xác nhận ở lượt chạy thật trên nhiều val hơn.

Trần thô để tự kiểm: nếu bộ định vị trúng `h` trong 80 bước trở sai, và bộ biên tập sửa được tỉ lệ `f` của các bước đó (đọc từ `gold`), thì `pred` cứu được khoảng `h·f` bước, trừ số bước cổng để lọt câu phá.

## 4. Chuẩn bị — người dùng làm

1. Thư mục đã dùng sẵn trên máy nhà, ngoài `thesis-master/`:

```text
/Users/P836901/Documents/Self-learning/thesis/_kaggle/tage_val/
```

| tệp | md5 | nguồn |
|---|---|---|
| `tage_val.py` | `f0aa8508228c1ed24a41dd9cc127e16b` | Phụ lục A |
| `tage_doc.py` | `85ecb7f2a82a0fcbaed93a07a347a589` | Phụ lục B, chỉ chạy trên máy nhà |
| `tage_neg.jsonl` | `35185...` | Phụ lục C, 41.099 dòng |
| `pred_ck500.jsonl` | `eb6162d86730a936beb5ae5a9fd6d652` | `runs/grpo_spice/pred_ck500.jsonl`, 400 câu ck500 trên val C1 |
| `grpo_spice.py` | `07ea87b6d156d1faa391a4274dffd7cf` | `harness/grpo_spice.py`, cùng bản dataset `grpo-spice-script` |
| `build_branch_data.py` | — | `harness/build_branch_data.py` |

> Một vài ký tự của hash trong ảnh khá nhỏ; các hash phía trên được chép theo phần nhìn rõ nhất.

Mất thư mục thì dựng lại: chép hai tệp `harness/` từ clone; chép nguyên văn Phụ lục A, B; chạy Phụ lục C; chép `runs/grpo_spice/pred_ck500.jsonl`.

2. Upload thư mục đó thành dataset **`tage-val-script` (Private)**.
3. Máy: L4 hoặc A100 thì nhanh nhất (bf16). Kaggle T4 vẫn chạy được nhờ fp16 + GradScaler, nhưng chậm khoảng 3 lần. Ô 2 tự dò đường dẫn dưới `/kaggle/input`. Trên Colab hay máy khác, đặt `ROOT` ở Ô 2 thành thư mục chứa đủ các input dưới đây.
4. Input:
   - `fgrb-p1-bundle` (adapter S1, 5.567 ảnh, `ocr.jsonl`, `p1_train_rows.jsonl`, `p1_val_rows.jsonl`)
   - `c1-exec8` (`c1_raw.jsonl`, `c1_picks.json`, gọi mã `thesis/`)
   - `thesis-val-cham` (bản ghi chấm val, ảnh, OCR)
   - `grpo-spice-ck500` (adapter `checkpoint-500`)
   - `tage-val-script` (mới)
5. Internet ON (tải Qwen2.5-VL-3B và UGround-V1-2B).

## 5. Các ô notebook

### Ô 1 — gói và Java

```python
import subprocess, sys, os, time
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode

sh("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless")
sh("update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java")
sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes pycocoevalcap pillow 'trl==0.29.1' 2>&1 | tail -3")
sh(f'{sys.executable} -c "import transformers, peft, torch; print(transformers.__version__, peft.__version__, torch.__version__, torch.cuda.get_device_name(0))"')
```

Nếu peft báo `incompatible version of torchao`: Restart session rồi chạy lại từ Ô 2.

### Ô 2 — đường dẫn, md5, tìm ck500

```python
import os, glob, shutil, hashlib, json
ROOT = "/kaggle/input"      # Colab/máy khác: đổi thành thư mục chứa các input
W = "/kaggle/working" if os.path.isdir("/kaggle/working") else os.path.abspath("tage_work")
os.makedirs(W, exist_ok=True)
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()

BUNDLE = next(r for r, d, f in os.walk(ROOT) if "adapter_s1_seed101" in d and "images" in d)
C1_PATH = [p for p in glob.glob(f"{ROOT}/**/c1_raw.jsonl", recursive=True)]
C1_PATH = sorted((md5(p), p) for p in C1_PATH).values()
assert len(C1_PATH) == 1 and md5(C1_PATH[0]) == "d757554326977309c3a65ae0b1d4c211", C1_PATH
C1_PATH = C1_PATH[0]

S = glob.glob(f"{ROOT}/**/tage_val.py", recursive=True)
assert len(S) == 1, f"DUNG: cần đúng một tage_val.py, thấy {S}"
SD = os.path.dirname(S[0])
for f in ("tage_val.py", "grpo_spice.py", "build_branch_data.py", "tage_neg.jsonl", "pred_ck500.jsonl"):
    shutil.copy(os.path.join(SD, f), f"{W}/{f}")

assert md5(f"{W}/tage_val.py") == "f0aa8508228c1ed24a41dd9cc127e16b", "DỪNG: tage_val.py lệch bản file 265"
assert md5(f"{W}/grpo_spice.py") == "07ea87b6d156d1faa391a4274dffd7cf", "DỪNG: grpo_spice.py lệch"
assert md5(f"{W}/pred_ck500.jsonl") == "eb6162d86730a936beb5ae5a9fd6d652", "DỪNG: pred_ck500 lệch"

NEG, PRED500, MERGED = f"{W}/tage_neg.jsonl", f"{W}/pred_ck500.jsonl", f"{W}/s1_merged"

def la_grpo(d):
    c = os.path.join(d, "adapter_config.json")
    return os.path.exists(c) and "s1_merged" in json.load(open(c)).get("base_model_name_or_path", "")

CK = [os.path.dirname(f) for f in glob.glob(f"{ROOT}/**/adapter_model.safetensors", recursive=True) if la_grpo(os.path.dirname(f))]
if len(CK) > 1:
    CK = [d for d in CK if d.rstrip("/").endswith("checkpoint-500")]
assert len(CK) == 1, f"DUNG: cần đúng một adapter ck500, thấy {CK}"
CK500 = CK[0]
print("BUNDLE", BUNDLE, "\nC1", C1_PATH, "\nCK500", CK500, "\nW", W, flush=True)
```

### Ô 3 — hoà S1, selftest

```python
def chay(cmd, log, cwd=None, nhip=60):
    t0 = time.time()
    with open(log, "w") as f:
        q = subprocess.Popen(
            cmd, cwd=cwd or W, stdout=f, stderr=subprocess.STDOUT,
            env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1"}
        )
        while q.poll() is None:
            time.sleep(nhip)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"  {(time.time()-t0)/60:5.1f} phút · {os.path.basename(log)} · {(L[-1][:120] if L else '...')}", flush=True)
    print(f"--- {os.path.basename(log)} · mã thoát {q.returncode} · {(time.time()-t0)/60:.1f} phút ---")
    print("".join(open(log, errors="ignore").readlines()[-8:]), flush=True)
    assert q.returncode == 0, f"DỪNG: xem {log}"

T = ["python", "tage_val.py", "--bundle", BUNDLE, "--merged", MERGED]
chay(T + ["--merge"], f"{W}/merge.log", nhip=30)
chay(T + ["--selftest", "--neg", NEG, "--c1", C1_PATH, "--out", f"{W}/selftest"], f"{W}/selftest.log", nhip=10)
```

Phải thấy `[val C1] 400 bước · click 249, có phần tử lân cận cùng vai …(>90%)` và ✅ selftest ĐẠT. Mở vài ảnh `selftest/*_gold.png`: phần tử đích phải nằm gần tâm. `*_neg.png` phải là phần tử khác.

### Ô 4 — V1: câu nháp train, bộ biên tập gold, sửa val với crop vàng và crop nhiễu

```python
TEST = True                        # chạy thử nhỏ; đổi False cho lượt thật
O = f"{W}/thu" if TEST else f"{W}/that"
os.makedirs(O, exist_ok=True)

NT = ["--n", "40"] if TEST else []        # số bước train lấy câu nháp
MS = ["--max-steps", "5"] if TEST else []
NV = ["--n", "5"] if TEST else []         # số bước click val

DR = f"{O}/drafts_train.jsonl"
chay(T + ["--make-drafts", "--ckpt", CK500, "--out", DR] + NT, f"{O}/drafts.log")
chay(T + ["--train-editor", "--neg", NEG, "--drafts", DR, "--crop", "gold", "--out", f"{O}/ed_gold"] + MS,
     f"{O}/ed_gold.log")

for crop in ("gold", "neg"):
    chay(T + ["--edit-val", "--c1", C1_PATH, "--ck500-pred", PRED500, "--editor", f"{O}/ed_gold",
              "--crop", crop, "--out", f"{O}/pred_{crop}.jsonl"] + NV,
         f"{O}/edit_{crop}.log")
```

Kiểm trong log:

- `drafts.log`: dòng `[nháp] … greedy trùng câu người x%`. Ghi lại x.
- `ed_gold.log`: `[LoRA editor/gold] r=16 · tham số học …; nll vàng giảm dần; nll nhiễu cao hơn nll vàng sau vài trăm bước; không có nan.`
- `edit_gold.log`: `[edit-val gold] 249 bước click · đổi câu …`. Đổi câu 0% hoặc 100% đều là dấu hiệu xấu, gửi về.

### Ô 5 — dùng dữ liệu chấm

Dán nguyên văn Phụ lục D (lấy từ runbook chấm ck500). Ô này đổi tên biến `C1` thành danh sách; các ô khác chỉ dùng `C1_PATH`, nên không xung đột. Ngoài Kaggle: xoá dòng `W = "/kaggle/working"` ở đầu ô và thay mọi `"/kaggle/input/**/"` bằng `f"{ROOT}/**/"`.

### Ô 6 — chấm V1

```python
M = ["--n", "3"] if TEST else []

def cham(ten, pred):
    cmd = ["python", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", pred,
           "--data-root", f"{W}/c1data", "--recs-file", "c1_recs.jsonl", "--out", f"{O}/score_{ten}.json"] + M
    chay(cmd, f"{O}/cham_{ten}.log", cwd=f"{W}/pk/thesis")
    R = [json.loads(l) for l in open(f"{O}/score_{ten}_raw.jsonl")]
    print(f"== {ten}: {len(R)} bước · exec {sum(int(r['executable']) for r in R)}", flush=True)

cham("k0_lai", f"{W}/c1preds/k0.jsonl")
for crop in ("gold", "neg"):
    cham(crop, f"{O}/pred_{crop}.jsonl")
print("KIỂM (bản đủ): k0_lai phải 249 bước · exec 158. Lệch thì dừng, gửi về.")
```

Chạy thử trước với `TEST = True`: khoảng 20–40 phút. Ổn thì đặt `TEST = False`, chạy lại Ô 4 và Ô 6. Lượt thật ghi vào `that/`, không lẫn với `thu/`.

Tải về máy nhà, đặt vào:

```text
/Users/P836901/Documents/Self-learning/thesis/_exports/tage_val/
```

Các file:

- `score_gold_raw.jsonl`
- `score_neg_raw.jsonl`
- `score_k0_lai_raw.jsonl`
- `pred_gold_meta.jsonl`
- `pred_neg_meta.jsonl`
- `pred_gold.jsonl`
- `pred_neg.jsonl`
- mọi tệp `.log`
- thư mục `ed_gold/` (adapter vài chục MB)

Đọc bằng mục 6, rồi mới chạy Ô 7.

### Ô 7 — V2 và V3: bộ biên tập none, hai bộ định vị, nhánh pred

Chỉ chạy khi V1 đạt. Cùng phiên, hoặc phiên mới chạy lại Ô 1–3, Ô 5 với `TEST = False` (`O = W + "/that"`, `drafts_train.jsonl` và `ed_gold/` đã có trong `that/`).

```python
chay(T + ["--train-editor", "--neg", NEG, "--drafts", DR, "--crop", "none", "--out", f"{O}/ed_none"] + MS,
     f"{O}/ed_none.log")

chay(T + ["--train-locator", "--out", f"{O}/loc_g"] + MS, f"{O}/loc_g.log")
chay(T + ["--train-locator", "--drafts", DR, "--with-draft", "--out", f"{O}/loc_d"] + MS,
     f"{O}/loc_d.log")

chay(T + ["--locate-val", "--c1", C1_PATH, "--ck500-pred", PRED500, "--locator", f"{O}/loc_g",
          "--out", f"{O}/loc_val_g.jsonl"] + NV, f"{O}/loc_val_g.log")

chay(T + ["--locate-val", "--c1", C1_PATH, "--ck500-pred", PRED500, "--locator", f"{O}/loc_d", "--with-draft",
          "--out", f"{O}/loc_val_d.jsonl"] + NV, f"{O}/loc_val_d.log")
```

Đọc hai dòng `[locate-val] · trúng đĩa ±14% …`. Gửi cả hai `loc_val_*.jsonl` về máy nhà và chạy `tage_doc.py` (mục 6), để chọn bộ định vị trúng nhiều hơn trên 80 bước ck500 trở sai, không phải trên toàn bộ 249 bước. Không về máy nhà được thì chọn bản trúng tổng nhiều hơn và ghi rõ đã làm vậy.

```python
LOC = f"{O}/loc_val_d.jsonl"      # hoặc loc_val_g.jsonl, theo kết quả đọc ở trên

chay(T + ["--edit-val", "--c1", C1_PATH, "--ck500-pred", PRED500, "--editor", f"{O}/ed_gold",
          "--crop", "pred", "--points", LOC, "--out", f"{O}/pred_pred.jsonl"] + NV, f"{O}/edit_pred.log")

chay(T + ["--edit-val", "--c1", C1_PATH, "--ck500-pred", PRED500, "--editor", f"{O}/ed_none",
          "--crop", "none", "--out", f"{O}/pred_none.jsonl"] + NV, f"{O}/edit_none.log")

for ten in ("pred", "none"):
    cham(ten, f"{O}/pred_{ten}.jsonl")
```

Tải về `_exports/tage_val/`: `score_pred_raw.jsonl`, `score_none_raw.jsonl`, `pred_pred_meta.jsonl`, `pred_none_meta.jsonl`, `loc_val_g.jsonl`, `loc_val_d.jsonl`, mọi `.log`, và các thư mục `ed_none/`, `loc_g/`, `loc_d/`.

## 6. Đọc kết quả trên máy nhà

Cần clone `thesis-master` mới (có `runs/grpo_spice/score_ck500_raw.jsonl`). Không cần Java hay GPU.

```bash
cd /Users/P836901/Documents/Self-learning/thesis
python3 _kaggle/tage_val/tage_doc.py \
  --ck500 thesis-master/runs/grpo_spice/score_ck500_raw.jsonl \
  --dir _exports/tage_val
```

Phải in ck500: `exec 66.27 (165/249) · sai 84 · ... trở sai phần tử 80`. Lệch thì dừng đọc sai, dừng.

Sau đó mỗi nhánh có một dòng: exec, Δ so với ck500, khoảng tin cậy bootstrap theo episode, số bước cứu và phá, số câu đổi. Nhánh có `meta.jsonl` có thêm dòng `+cổng` kèm hai ngưỡng τ chọn chéo. Bộ định vị có dòng trúng đĩa trên 249 bước, trên 84 bước sai và trên 80 bước trở sai. Số của các nhánh trong lần chạy thử là giả, không mang nghĩa gì.

`tage_doc.py` đã chạy thử trên máy nhà ngày 2/10 với dữ liệu giả lập: đường đọc ck500 ra đúng 66,27 (165/249), 84 sai, 80 trở sai. Số của các nhánh trong lần chạy thử là giả, không mang nghĩa gì.

Ghi kết quả vào một file bản giao mới, ngoài `thesis-master/`:

```text
/Users/P836901/Documents/Self-learning/thesis/266_KET_QUA_TAGE_VAL_<ngày>.md
```

File phải gồm bảng số, phán quyết theo mục 3, và log train tóm tắt (nll vàng, nll nhiễu, s/bước, VRAM).

## 7. Dừng và gửi log khi

- selftest không đạt; click val ≠ 249; hoặc phần tử lân cận phủ dưới 60%.
- `k0_lai` không ra 249 bước · exec 158 (dụng cụ chấm lệch).
- nan ở loss, CUDA out of memory (thử `--accum 16` và bỏ loss tương phản bằng `--lam-ctr 0` một lần; vẫn OOM thì gửi về), mã thoát khác 0, `AssertionError`.
- Bộ biên tập đổi 0% hoặc trên 90% câu val; câu sửa chuyển sang tiếng Việt, dài bất thường hoặc lặp.
- Bộ định vị không đọc được tọa độ ở hơn 30% bước.

## 8. Thời gian ước lượng

Chưa đo; script in s/bước. Số dưới là ước lượng thô:

| việc | A100 | L4 | T4 |
|---|---:|---:|---:|
| câu nháp train, khoảng 2.500 bước × 3 câu | 1 h | 2 h | 3–4 h |
| bộ biên tập `gold`, 2 epoch, hai lượt forward mỗi mẫu | 1,5–2 h | 3–4 h | 6–8 h |
| sửa val, mỗi nhánh 249 bước | 10–15 phút | 20–30 phút | 40–60 phút |
| chấm UGround, mỗi tệp 249 bước | 10–20 phút | như A100 | 20–30 phút |
| **V1 cộng lại** | ~4 h | ~7 h | ~12 h |
| bộ biên tập `none` + hai bộ định vị | 2–3 h | 4–6 h | 8–12 h |
| **V2 + V3 cộng lại** | ~4 h | ~7 h | ~12 h |

Kaggle cắt phiên tương tác sau 12 h. Trên T4 nên commit từng ô lớn. Script ghi dần và tự nối tiếp ở `--make-drafts` và `--edit-val`; `--train-editor` lưu adapter sau mỗi epoch.

## 9. Việc chat thực thi không tự làm

- Không chấm test. Không chạy thật trên toàn bộ train. Đó là lượt sau, người dùng quyết sau khi có V3.
- Không dùng điểm vàng làm đầu vào hệ thật. Nhánh `gold` chỉ để chẩn đoán.
- Không dùng UGround ngoài `score_run.py`.
- Không ghi vào `thesis-master/`. Không commit, không push.

Người dùng quyết:

1. Upload `tage-val-script` và chọn máy.
2. Sau V1: đi tiếp V2/V3 hay dừng.
3. Sau V3: có mở lượt chạy thật hay không. Lượt thật cần ảnh của 41 nghìn bước click train (khoảng 12 GB), adapter lớn hơn, chấm trên toàn bộ val, rồi mới chấm test một lần.

## 10. Chưa kiểm được trên máy nhà

- Đã kiểm (2/10, Python 3 + Pillow, bundle giả 4.000 dòng lấy từ train thật): `tage_val.py` biên dịch được; `--selftest` đạt; 2.523 bước click, 90,7% có phần tử lân cận cùng vai trò; crop đúng tâm khi ảnh nhỏ hơn tọa độ gốc; câu làm hỏng ra đúng dạng `(Click on the see full description option → Click on the item description from the seller option)`; bộ đọc tọa độ nhận `(512, 300)`, `512,300`. `tage_doc.py` đọc đúng ck500 lớn hơn tọa độ gốc; câu làm hỏng ra đúng dạng.
- Chưa chạy lần nào trên GPU: `--make-drafts`, `--train-editor`, `--edit-val`, `--train-locator`, `--locate-val`. Lượt TEST = True dùng để bắt lỗi trước.
- Ba chỗ dễ lỗi nhất:
  1. Che nhãn: số token câu nhắc tính bằng cách tokenize riêng phần câu nhắc. Cách này đúng khi tokenizer không gộp `\n` cuối câu nhắc với chữ đầu câu trả lời. Qwen2 tách xuống dòng riêng nên lẽ ra đúng, nhưng chưa kiểm. Kiểm nhanh: nll vàng ở bước đầu phải vào khoảng 0,3–2 nat. Gần 0 hoặc trên 5 là che nhãn sai.
  2. Hai ảnh trong một câu nhắc: `proc(text=[...], images=[[full, crop]])`. Qwen2.5-VL hỗ trợ, nhưng phiên bản transformers mới có thể đổi `images=[full, crop]`. Lỗi thì đổi đúng chỗ này trong `mau_vao`.
  3. `target_modules` đang regex cho PEFT: script assert không có tham số học nào thuộc `visual`. Ra 0 tham số học thì regex không khớp tên module; in `model.named_modules()` rồi gửi về.

# Phụ lục A — `tage_val.py`

Phần đầu file nhìn thấy trong ảnh:

```python
# -*- coding: utf-8 -*-
"""TAGE — kiểm thử trên val C1 trước khi chạy thật (file 265).

Chạy từ thư mục có grpo_spice.py và build_branch_data.py.

python tage_val.py --selftest --bundle B --neg tage_neg.jsonl --c1 C1
python tage_val.py --make-drafts --bundle B --merged M --ckpt CK500 --out drafts_train.jsonl
python tage_val.py --train-editor --bundle B --merged M --neg N --drafts D --crop gold --out ed_gold
python tage_val.py --edit-val --bundle B --merged M --c1 C1 --ck500-pred P --editor ed_gold --crop gold --out pred_gold.jsonl
python tage_val.py --train-locator --bundle B --merged M --drafts D --with-draft --out loc_d
python tage_val.py --locate-val --bundle B --merged M --c1 C1 --ck500-pred P --locator loc_d --with-draft --out loc_val.jsonl
python tage_val.py --edit-val --c1 C1 --ck500-pred P --editor ed_gold --crop pred --points loc_val.jsonl --out pred_pred.jsonl

Không đọc test. Không dùng UGround trong train hay suy luận; UGround chỉ chấm qua score_run.py.
"""

import os, re, sys, json, time, random, argparse, collections

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

> Ảnh chỉ hiển thị phần đầu của Phụ lục A; phần còn lại của file không xuất hiện trong 8 ảnh nên không thể chép chính xác hơn từ nguồn này.
