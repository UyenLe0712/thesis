# Chạy trên Kaggle — hai phép đo mà năm phản biện đòi (16/8/2026)

Cả hai đều **miễn phí** (Kaggle cho 30 giờ GPU mỗi tuần) và đều đã có mã sẵn. Chúng bịt
hai đòn khác nhau, đừng gộp làm một:

| Phép | Bịt đòn nào | GPU | Ra cái gì |
|---|---|---|---|
| **A. Diễn đạt lại** | Jandial et al. báo bộ trỏ GUI trượt tới 84% khi đổi cách nói. Bài **đang phải khai là không trả lời được**, vì bộ bơm lỗi không gọi bộ trỏ lần nào. | ~1 giờ/biến thể | trần dưới 4 kiểu viết lại, so với 75,7% |
| **B. Bộ trỏ thứ hai** | UGround có **47K phần tử AndroidControl** trong dữ liệu huấn luyện (đã tra Bảng 1, arXiv 2410.05243). Đây là lời giải thích thay thế cho chênh lệch S1−Base mà **sáu đòn phản biện chưa loại được**. | ~1,5–2 giờ/nhánh | ba nhánh chấm lại bằng dụng cụ sạch AndroidControl |

> ⚠️ **B đóng đòn nhiễm dữ liệu, KHÔNG đóng đòn cùng họ.** UI-Venus-Ground-7B dựng trên
> Qwen2.5-VL, cùng dòng với mô hình được chấm. Đừng viết trong bài rằng phép lặp này giải
> quyết cả hai. Muốn khác họ phải là Phi-Ground (nền Phi-3.5-Vision) nhưng nó yếu hẳn ở
> màn di động (78,1 trên ScreenSpot-v2) nên trần sẽ tụt vì lý do khác, không đọc được.

**Chia phiên:** A ≈ 4 giờ, B ≈ 5–6 giờ. Phiên Kaggle tối đa 12 giờ. Chạy **A trước** —
nó rẻ hơn, và nó bịt cái đòn mà bài đang phải tự khai là bỏ ngỏ.

---

## Ô 0 — môi trường (90 giây)

```python
import torch, transformers, subprocess
print("GPU:", torch.cuda.get_device_name(0), "| số card:", torch.cuda.device_count())
print("transformers:", transformers.__version__)
# Qwen2.5-VL cần transformers >= 4.49; Kaggle thường đã đủ. Chỉ cài khi thiếu.
```

⚠️ **Đừng bật `flash_attention_2`.** T4 và P100 của Kaggle là Turing/Pascal, không hỗ
trợ; mã đã đặt `attn_implementation="sdpa"`. Bật vào là chết ngay lúc nạp mô hình.

⚠️ **UI-Venus 7B ở bf16 cần ~15 GB.** T4 có 16 GB nên vừa **một** card, nhưng chật.
Kaggle cho 2×T4: `device_map="auto"` sẽ tự trải ra hai card, mã đã đặt sẵn. Nếu chọn
P100 (16 GB, một card) thì rủi ro tràn bộ nhớ — **chọn T4 ×2**.

## Ô 1 — dữ liệu (kiểm trước khi tốn giờ card)

```python
import os, json, glob
WS = "/kaggle/working"
# Dataset đã dùng cho ba nhánh trước. Sửa đường dẫn nếu tên khác.
DATA = "/kaggle/input/thesis-preds"
print("có gì:", os.listdir(DATA)[:20])

need = ["test.jsonl"]
img_dirs = glob.glob(f"{DATA}/**/images", recursive=True)
print("thư mục ảnh:", img_dirs)
n_img = len(glob.glob(f"{img_dirs[0]}/*.png")) if img_dirs else 0
print("số ảnh:", n_img, "→ cần ≥ 4.463 cho toàn tập, ≥ 900 cho lát 800")
```

⚠️ **Gói `kaggle_16_8.zip` KHÔNG chứa ảnh** — nó chỉ có mã và bốn tệp preds. Ảnh và
`test.jsonl` nằm ở phần cũ của dataset, nên ô trên sẽ báo `số ảnh: 0`. Đó là bình thường.

## Ô 1b — nối dữ liệu vào đúng chỗ mã chấm đòi (BẮT BUỘC)

`score_run.py` đọc **cứng** `<thư mục chứa nó>/dg1_cache/test_ac/{test.jsonl, images/}`.
Không nối đúng thì nó chết ở bước đầu, hoặc tệ hơn là chạy với ảnh thiếu. Dán trọn tệp
`harness/kaggle_o1b_noi_du_lieu.py` vào một ô — nó quét toàn bộ `/kaggle/input`, tìm
`test.jsonl` và thư mục ảnh đông nhất, tạo liên kết mềm (không tốn dung lượng), rồi kiểm
200 bước chạm đầu xem có mở được ảnh không. Chỉ chạy tiếp khi nó in `✔ sẵn sàng`.

**Nếu không thấy ảnh trong dataset nào:** dựng lại ngay trên Kaggle bằng
`build_test_data.py --shards 9` (~8 GB tải về, ~20 phút). Đừng chạy chấm với ảnh thiếu —
mã chỉ tự dừng khi hụt quá 1% và **không** truyền `--n`; có `--n` thì nó im lặng chấm
trên phần còn lại.

## Ô 2 — PHÉP A: diễn đạt lại (UGround, ~4 giờ cho cả bốn)

Bốn tệp `preds_para_*.jsonl` đã dựng sẵn ở máy nhà, **mang theo trong dataset**. Chúng
giữ nguyên tên phần tử — đổi tên là đổi nghĩa, không còn là paraphrase:

| biến thể | đổi gì | đổi được |
|---|---|---|
| `p1_verb` | động từ mở đầu: click → tap/press/select/choose | 91,5% số bước |
| `p2_order` | đưa mệnh đề vị trí lên đầu câu | 24,9% |
| `p3_nopos` | **bỏ** mệnh đề vị trí, giữ tên phần tử | 24,9% |
| `p4_both` | p1 + p2 cùng lúc | 23,7% |

```python
import subprocess, time
N = 800          # lát cố định: score_run xáo bằng SEED rồi cắt, nên MỌI lượt cùng lát
for v in ["p1_verb", "p2_order", "p3_nopos", "p4_both"]:
    t0 = time.time()
    subprocess.run([
        "python", f"{WS}/harness/score_run.py", "--mode", "score",
        "--grounder", "uground",
        "--preds", f"{DATA}/preds_para_{v}.jsonl",
        "--out",   f"{WS}/score_para_{v}.json",
        "--n", str(N)], check=True)
    print(f"{v}: {(time.time()-t0)/60:.0f} phút")
```

⚠️ **`p3_nopos` KHÔNG bảo toàn thông tin** — bỏ vị trí thì câu nghèo đi thật. Nó ở đây để
tách hai nguyên nhân: bộ trỏ nhạy với *cách nói*, hay nhạy với *lượng thông tin*. Đọc
riêng, đừng gộp vào một con số "độ bền trước paraphrase".

## Ô 3 — mốc so cho phép A (0 GPU, chạy ở máy nhà cũng được)

Trần 75,7% đo trên **toàn tập**; phép A chạy trên **lát 800**. Phải lấy trần trên đúng
lát đó, nếu không là so hai quần thể khác nhau:

```python
import json, random
SEED = 20260805
raw = [json.loads(l) for l in open(f"{DATA}/score_ceiling_human_raw.jsonl", encoding="utf-8")]
raw = [r for r in raw if "executable" in r]
keys = [(r["episode_id"], r["step_id"]) for r in raw]
random.Random(SEED).shuffle(keys)          # cùng phép xáo với score_run.py
lat = set(keys[:800])
sub = [r for r in raw if (r["episode_id"], r["step_id"]) in lat]
print(f"trần trên lát {len(sub)} bước: {sum(r['executable'] for r in sub)/len(sub)*100:.1f}%")
```

**Mốc so đã tính sẵn** (chạy ô 3 ở máy nhà, 0 GPU):

| lát | trần theo ô Voronoi | trần theo dung sai |
|---|---|---|
| 500 bước | **73,4%** | 83,0% |
| 800 bước | **74,9%** | 83,0% |

**Cách đọc kết quả A.** Gọi trần-trên-lát là $C$ ($74{,}9\%$ với lát 800):
- Biến thể nào cũng ≈ $C$ → bộ trỏ **bền** trước cách diễn đạt trong kho này, và bài được
  phép viết rằng con số 84% của Jandial et al. không tái hiện ở đây (kèm điều kiện: chỉ
  cho bộ trỏ này, kiểu viết lại này).
- `p1_verb` tụt mạnh → bộ trỏ nhạy với **cách nói**, đòn Jandial đứng. Phải khai, và mọi
  số tuyệt đối yếu đi.
- Chỉ `p3_nopos` tụt → bộ trỏ cần **thông tin vị trí**, không phải chuyện diễn đạt. Đây là
  kết quả khác hẳn và nhẹ hơn nhiều.

## Ô 4 — PHÉP B: bộ trỏ thứ hai (UI-Venus, ~5–6 giờ)

```python
import subprocess, time
N = 500
for arm, preds in [("human", "preds_ceiling_human.jsonl"),
                   ("s1",    "preds_s1_seed101.jsonl"),
                   ("base",  "preds_base.jsonl")]:
    t0 = time.time()
    subprocess.run([
        "python", f"{WS}/harness/score_run.py", "--mode", "score",
        "--grounder", "uivenus",
        "--preds", f"{DATA}/{preds}",
        "--out",   f"{WS}/score_venus_{arm}.json",
        "--n", str(N)], check=True)
    print(f"{arm}: {(time.time()-t0)/60:.0f} phút")
```

Lần chạy đầu tải ~16 GB trọng số, tính thêm 10–15 phút.

**Mốc so đã tính sẵn — cùng lát 500 bước, bằng UGround:**

| | Human | S1 | Base | S1−Base |
|---|---|---|---|---|
| UGround (dụng cụ cũ) | **73,4%** | **58,8%** | **47,6%** | **+11,2 pp** |
| UI-Venus (sắp chạy) | ? | ? | ? | ? |

**Cách đọc kết quả B.** Ba nhánh trên cùng lát 500 bước, bằng dụng cụ **sạch
AndroidControl**:
- Thứ tự giữ nguyên (Human > S1 > Base) → đòn nhiễm dữ liệu **đóng lại**. Đây là kết quả
  đắt giá nhất bài có thể mua bằng 6 giờ máy miễn phí.
- Thứ tự đảo, hoặc chênh lệch S1−Base co về gần 0 → **kết luận chính của bài phụ thuộc
  bộ trỏ**. Phải khai thẳng và hạ mọi khẳng định về S1-vs-Base. Đây là kết cục xấu nhưng
  biết còn hơn để phản biện tìm ra.
- Mức tuyệt đối sẽ khác 75,7/59,1/47,6 dù thế nào, vì đổi dụng cụ là đổi thang. **Chỉ đọc
  thứ tự và khoảng cách**, không đọc con số tuyệt đối.

## Ô 5 — mang về

```python
import shutil, glob
for f in glob.glob(f"{WS}/score_para_*.json") + glob.glob(f"{WS}/score_venus_*.json") \
       + glob.glob(f"{WS}/score_*_raw.jsonl"):
    print(f)   # tải xuống từ panel Output của Kaggle
```

Giữ **cả** `.json` lẫn `_raw.jsonl` — tệp thô cho phép đổi luật chấm rồi tính lại mà
không phải gọi bộ trỏ, đúng như ba nhánh trước.

---

## Việc này KHÔNG làm được, đừng nhầm

- **Không** thay được phép chấm với người. Cả A lẫn B đều là mô hình chấm mô hình. Bài đã
  đổi khung (tên bài, mục *Scope of the construct*) để không hứa thứ nó không đo.
- **Không** đóng được đòn "bộ trỏ cùng họ Qwen với mô hình được chấm" — UI-Venus cũng là
  Qwen2.5-VL.
- **Không** thay được hạt giống 202. Chừng nào chưa có cặp hạt giống thì 11,5 điểm vẫn
  chưa có sàn nhiễu giữa hai lượt train để đọc.
