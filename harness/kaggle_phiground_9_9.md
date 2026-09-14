# Đổi dụng cụ đo — hai ứng viên trên Kaggle T4 (viết 9/9/2026)

⭐⭐ **CHẠY `uground7b` TRƯỚC `phiground`.** Hai lượt trả lời hai câu hỏi khác nhau, và nếu
mục tiêu là **số cao hơn** thì lượt đầu đáng hơn hẳn:

| | `uground7b` | `phiground` |
|---|---|---|
| câu hỏi nó trả lời | **số có cao hơn không** | đòn *cùng họ Qwen* có đóng được không |
| căn cứ lạc quan | Jandial Bảng 1: 7B **bền nhất** trước cách diễn đạt (s_mean 0,3176) so với **0,6218** của 2B đang dùng | ngoài họ Qwen, sạch AndroidControl |
| mã phải viết | **0 dòng** — cùng lớp, cùng câu nhắc, cùng thang toạ độ | lớp mới, `trust_remote_code`, ghim transformers |
| chặn kỹ thuật | không có | ba chặn, xem mục dưới |
| đóng đòn phản biện | ⛔ không đóng đòn nào | ✅ đóng đòn *cùng họ* |

⛔ Cả hai đều chỉ cho **thước báo kèm**, không thay thước tiêu đề.

---

## Lượt A — `uground7b`: nâng cỡ chính bộ trỏ đang dùng

`osunlp/UGround-V1-7B`, nền Qwen2-VL-7B, Apache-2.0. Cùng lớp, cùng câu nhắc, cùng thang toạ độ
0–1000 với bản 2B đang dùng ⇒ **không thêm một dòng logic nào**, chỉ đổi đường dẫn.

⭐ Chấm trên **đúng lát 2.532 của phép B** để so thẳng ba dụng cụ cạnh nhau: UGround-2B ·
UI-Venus-7B · UGround-7B.

⚠️ **Kỳ vọng ghi trước:** chưa ai đo cỡ bộ trỏ đổi `exec` bao nhiêu ở bài này, và tiền lệ duy
nhất trong dự án đi **ngược** — UI-Venus-7B mạnh hơn trên benchmark mà chấm **thấp hơn** 2B ở
cả ba nhánh (20/8). Đây là phép thử thật, không phải điều đã biết trước.

### Chuẩn bị — một dataset mới

⛔ **Gói mã trên `thesis-score` là bản CŨ, không có lớp `UGround7B`.** Phải upload
`_bundles/harness_code_9_9b.zip` (57 KB, md5 `c6cc85226264`, 8 tệp) thành **dataset mới**
tên `thesis-code-9-9b`. ⛔ Đừng New Version của dataset cũ — nó *thêm* thư mục chứ không thay,
rồi ô dò chọn mò.

Notebook: **GPU T4×2** · **Internet ON** (nạp mô hình từ HuggingFace). Add Data: `thesis-score`,
`thesis-preds`, `thesis-code-9-9b`.

### Ô A0 — kiểm máy và kiểm gói mã có đúng bản mới không

```python
import torch, glob, os
print("card", torch.cuda.get_device_name(0), "×", torch.cuda.device_count(),
      "· capability", torch.cuda.get_device_capability(),
      "· VRAM", round(torch.cuda.get_device_properties(0).total_memory/2**30, 1), "GB")
# ⛔ Chọn gói mã theo NỘI DUNG, không theo tên dataset: chỉ bản có UGround7B mới dùng được.
CAND = [p for p in glob.glob("/kaggle/input/**/harness/score_run.py", recursive=True)
        if "uground7b" in open(p, encoding="utf-8").read()]
assert CAND, ("DỪNG: không gói mã nào có lớp UGround7B. Upload "
              "_bundles/harness_code_9_9b.zip thành dataset mới rồi Add Data.")
PKG = os.path.dirname(os.path.dirname(CAND[0]))
print("[mã] dùng", PKG)
```

Phải thấy hai card T4, `capability (7, 5)`, và một dòng `[mã] dùng …`. ⛔ `capability` bắt đầu
bằng 7 nghĩa là Turing: **không bf16** — lớp đã tự chọn fp16, đừng ép.

### Ô A1 — dựng dữ liệu (chép nguyên ô 1 của `kaggle_cham_min_desc.md`, chỉ đổi hai dòng)

```python
import os, glob, json, shutil
WS = "/kaggle/working"
TEN = ["min_desc_seed101"]            # ★ chỉ để ô kiểm preds chạy; lượt này chấm nhánh nào
                                      #   thì khai ở ô A3
best = None
for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True):
    root = os.path.dirname(t)
    rows = sum(1 for _ in open(t, encoding="utf-8"))
    nimg = len(glob.glob(os.path.join(root, "images", "*.png")))
    print(f"  {rows:5d} dòng · {nimg:5d} ảnh  {root}")
    if rows >= 6900 and nimg >= 4400 and (best is None or nimg > best[2]):
        best = (t, rows, nimg, root)
assert best, "DỪNG: không gói nào có đủ test.jsonl 6.958 dòng lẫn 4.463 ảnh"
TEST_JSONL, _, _, ROOT = best

shutil.rmtree(f"{WS}/harness", ignore_errors=True)
shutil.copytree(f"{PKG}/harness", f"{WS}/harness", dirs_exist_ok=True)
dst = f"{WS}/harness/dg1_cache/test_ac"; os.makedirs(dst, exist_ok=True)
for src, name in [(TEST_JSONL, "test.jsonl"), (os.path.join(ROOT, "images"), "images")]:
    link = os.path.join(dst, name)
    if os.path.islink(link): os.remove(link)
    elif os.path.isdir(link): shutil.rmtree(link)
    elif os.path.exists(link): os.remove(link)
    os.symlink(src, link)

recs = [json.loads(l) for l in open(f"{dst}/test.jsonl", encoding="utf-8")]
taps = [r for r in recs if r["action"].get("action_type") in ("click", "long_press")
        and "x" in r["action"]]
miss = sum(1 for r in taps if not os.path.exists(os.path.join(dst, r["image"])))
assert len(taps) == 4463 and miss == 0, f"DỪNG: {len(taps)} bước chạm, thiếu {miss} ảnh"
print(f"✔ {len(taps)} bước chạm, đủ ảnh")

PREDS = {}
for ten in TEN:
    cand = glob.glob(f"/kaggle/input/**/preds_{ten}.jsonl", recursive=True)
    assert cand, f"DỪNG: chưa thấy preds_{ten}.jsonl"
    PREDS[ten] = cand[0]; print("✔ preds", ten, "←", cand[0])
```

### Ô A2 — hàm chạy-và-chờ

```python
import subprocess, time
def chay(cmd, log, dich=None, can=None, nhip=120):
    env = {**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1",
           "HF_HUB_DISABLE_PROGRESS_BARS": "1"}
    if os.path.exists(log): os.remove(log)
    f = open(log, "a")
    P = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT,
                         start_new_session=True, env=env, cwd=WS)
    t0 = time.time()
    while P.poll() is None:
        time.sleep(nhip)
        n = sum(1 for _ in open(dich)) if dich and os.path.exists(dich) else -1
        gio = (time.time() - t0) / 3600
        eta = (gio * (can - n) / n) if (can and n > 0) else float("nan")
        print(f"{time.strftime('%H:%M:%S')} · {gio:5.2f} h · {n}/{can or '?'} · còn ~{eta:.1f} h",
              flush=True)
    print("mã thoát:", P.returncode, flush=True)
    print(subprocess.run(["tail", "-30", log], capture_output=True, text=True).stdout)
    assert P.returncode == 0, "DỪNG: tiến trình thoát khác 0 — đọc log ở trên"
```

### ⭐ Ô A3 — CỔNG: sai số trên CÂU CHUẨN, 300 bước, ~25 phút

⛔ Chạy ô này **trước** và đọc kết quả **trước** khi cam kết mấy giờ chấm. Chế độ `gate` dùng câu
do người chú thích viết — giống hệt nhau ở mọi nhánh, nên **không thể thiên vị nhánh nào**. Đây
đúng luật chọn dụng cụ đã khoá từ hồi UI-Venus: ⛔ **cấm** dò dụng cụ bằng điểm của một nhánh.

```python
chay(["python", "-u", f"{WS}/harness/score_run.py", "--mode", "gate",
      "--grounder", "uground7b", "--n", "300",
      "--out", "/kaggle/working/gate_u7b.json"],
     "/kaggle/working/gate_u7b.log", nhip=60)
```

```python
import json, statistics
d = json.load(open("/kaggle/working/gate_u7b.json"))
E = sorted(json.loads(l)["err_frac"] for l in
           open("/kaggle/working/gate_u7b_raw.jsonl", encoding="utf-8"))
q4 = statistics.quantiles(E, n=4); q10 = statistics.quantiles(E, n=10)
print(f"{'':<12}{'trung vị':>10}{'p75':>9}{'p90':>9}{'≤3%':>8}")
print(f"{'UGround-7B':<12}{100*d['median_err']:>9.2f}%{100*d['p75_err']:>8.2f}%"
      f"{100*q10[8]:>8.2f}%{100*sum(1 for e in E if e<=.03)/len(E):>7.1f}%")
print(f"{'UGround-2B':<12}{0.73:>9.2f}%{8.76:>8.2f}%{36.28:>8.2f}%{62.7:>7.1f}%   ← gate_A.json")
```

⚠️ Mốc 2B lấy từ `runs/gate_a/gate_A.json`, cùng 300 bước, cùng cách tính
`statistics.quantiles(errs, n=4)`.

| kết quả | làm gì |
|---|---|
| trung vị **< 0,73%** và p75 **< 8,76%** | ⭐ tín hiệu tốt, chạy tiếp ô A4 |
| trung vị **0,73–1,5%** | mập mờ — vẫn chạy A4, nhưng đừng kỳ vọng |
| trung vị **> 3%** | ⛔ **dừng**. Cổng A của dự án đặt ngưỡng 3%; vượt là dụng cụ không dùng được |
| lỗi OOM lúc nạp | ⛔ dừng — 7B không vừa T4×2 ở cỡ ảnh này, không có đường vòng miễn phí |

### Ô A4 — chấm hai nhánh trên lát 2.532 (~6 h)

```python
NHANH = [("grpo_point_seed101", "grpo_point/preds_grpo_point_seed101.jsonl"),
         ("base",               "preds_base.jsonl")]
for ten, rel in NHANH:
    out = f"/kaggle/working/score_u7b_{ten}_2532.json"
    if os.path.exists(out): print("bỏ qua:", ten); continue
    cand = glob.glob(f"/kaggle/input/**/{os.path.basename(rel)}", recursive=True)
    assert cand, f"DỪNG: không thấy {rel}"
    print("=" * 60, "\n", ten, flush=True)
    chay(["python", "-u", f"{WS}/harness/score_run.py", "--mode", "score",
          "--grounder", "uground7b", "--preds", cand[0], "--n", "2532", "--out", out],
         f"/kaggle/working/u7b_{ten}.log",
         dich=f"/kaggle/working/score_u7b_{ten}_2532_raw.jsonl", can=2532, nhip=120)
```

⛔ **Chấm GRPO và Base trước, không chấm hết mọi nhánh.** Hai nhánh này đủ cho cả mức tuyệt đối
lẫn **phép so đối chiếu** S1−Base kiểu phép B. Chỉ chạy tiếp nếu chúng cho tín hiệu tốt.

### Ô A5 — đóng gói tải về

```python
import zipfile, hashlib
Z = "/kaggle/working/ket_qua_u7b.zip"
with zipfile.ZipFile(Z, "w", zipfile.ZIP_DEFLATED) as z:
    for m in ("score_u7b_*.json", "score_u7b_*_raw.jsonl", "gate_u7b*", "u7b_*.log"):
        for p in sorted(glob.glob(f"/kaggle/working/{m}")): z.write(p, os.path.basename(p))
print(round(os.path.getsize(Z)/2**20, 2), "MB · md5",
      hashlib.md5(open(Z, "rb").read()).hexdigest()[:12])
```

Bung vào **`runs/uground7b/`** ở máy nhà.

### Đọc kết quả — bốn kết cục, khoá TRƯỚC khi chạy

Mốc để so, đo bằng UGround-2B trên **cùng lát 2.532** (`report/138` phụ lục 9/9):
Base **50,67** · S1 **61,41** · chênh **+10,74**.

| kết cục | đọc thế nào |
|---|---|
| GRPO **cao hơn** và chênh GRPO−Base giữ ≳ 90% | ⭐ có một hàng **báo kèm** cao hơn. ⛔ vẫn không thay thước tiêu đề |
| GRPO cao hơn nhưng chênh **co lại quá một nửa** | thang đo bị nén ⇒ mức tuyệt đối vô nghĩa, ⛔ không dùng |
| GRPO **thấp hơn** | tái lập kết quả UI-Venus lần hai: cỡ bộ trỏ không mua được điểm ở bài này. Báo thẳng |
| không qua cổng A3 | ghi *"đã thử, dụng cụ không đạt ngưỡng sai số"*, dừng |

⛔ **Cấm** chọn kết cục có lợi rồi chỉ báo cái đó. Cả bốn ô đã khoá ở đây, trước khi chạy.

---

## Lượt B — `Phi-Ground` trên Kaggle T4

Máy: **Kaggle T4×2 miễn phí, 0 đồng.** Nguồn khoa học: `report/140` mục 3 · `report/112` §11.3.
Mã: lớp `PhiGround` đã thêm vào `harness/score_run.py`, gọi bằng `--grounder phiground`.

---

## ⛔ ĐỌC TRƯỚC — kỳ vọng ghi trước, và vì sao vẫn đáng chạy

**Kỳ vọng: KHÔNG đoán được chiều.**

⚠️ **Sửa 9/9:** bản đầu của tệp này viết *"nhiều khả năng THẤP hơn"* và dẫn *"Phi-Ground 78,1
so UGround 95,0"*. **Phép so đó lệch chuẩn.** Bảng ở `report/140` mục 3 trộn hai loại cột: hàng
Phi-Ground ghi *câu ngắn / câu dài*, các hàng khác là *text / icon* của ScreenSpot-v2.

| căn cứ | chiều |
|---|---|
| số tạm so được: Phi-Ground **78,1** (câu ngắn) vs UGround **95,0** (mobile-text) | nghiêng **xuống** |
| Phi-Ground **92,4 (câu dài)** — kho **không có** số tương ứng của UGround, mà bài toán này dùng **câu sinh đầy đủ**, gần "câu dài" hơn | nghiêng **lên** |
| chính bài Phi-Ground §6.1: thứ hạng bộ trỏ **đảo** khi câu chuyển từ người viết ngắn sang máy sinh dài (OS-Atlas 71,9 → 57,4 trong khi UI-TARS **tăng**) | **không xác định** |
| tiền lệ trong dự án: UI-Venus mạnh hơn trên benchmark mà chấm **thấp hơn ở cả ba nhánh** (20/8) | nghiêng **xuống** |
| lệch tỉ lệ khung hình: mô hình nhận **1008×672 ngang** (1,50), ảnh AndroidControl **1080×2400 dọc** (0,45) | **probe quyết** |

⇒ ⛔ **Đừng đặt cược lượt này vào việc nâng số** — đó là việc của lượt A.
Giá trị chắc chắn của lượt B là đóng **đòn *cùng họ mô hình***. Giá trị của nó là đóng **đòn *cùng họ mô hình***, đòn
duy nhất còn mở sau khi phép B đóng được đòn *nhiễm dữ liệu*: UGround-2B dựng trên Qwen2-VL và
UI-Venus-7B dựng trên Qwen2.5-VL, tức **cả hai cùng họ** với mô hình đang bị chấm. Phi-Ground nền
**Phi-3.5-Vision** là ứng viên duy nhất ngoài họ đó.

⚠️ Và phải khai trước: dù nó cho số cao hơn thì đó vẫn là **hàng báo kèm**, ⛔ không thay được
thước tiêu đề — đổi bộ trỏ tiêu đề thì mọi số của hai bài báo và luận văn phải đo lại.

---

## Sự thật đã tra từ thẻ mô hình (9/9, không lấy từ trí nhớ)

| | |
|---|---|
| kho | **`microsoft/Phi-Ground`** — một mô hình ở gốc kho, **không** có thư mục con cho biến thể |
| trọng số | **chỉ `.bin`**, 2 mảnh, ~8,5 GB (`pytorch_model-0000{1,2}-of-00002.bin`) |
| mã điều khiển | có `configuration_phi3_v.py` ⇒ **bắt buộc `trust_remote_code=True`** |
| phiên bản thẻ ghim | `transformers==4.43.0` · `flash_attn==2.5.8` · `torch==2.3.0` |
| độ phân giải | **CỐ ĐỊNH 1008×672** (336×3 ngang, 336×2 dọc) |
| đầu ra | **HỘP, toạ độ TƯƠNG ĐỐI nhân 1000** — không phải pixel |
| giấy phép | **MIT** |

⭐ Nhờ toạ độ **tương đối** nên quy đổi đơn giản hơn hẳn UI-Venus: chia 1000 rồi nhân kích thước
ảnh **gốc**, ⛔ không phải lần theo `image_grid_thw`.

### ⛔⛔ Ba chặn, mỗi cái đủ giết cả lượt

**① `flash_attn` không chạy trên T4.** FlashAttention-2 đòi Ampere (sm_80); T4 là Turing (sm_75).
Lớp `PhiGround` đã ép `_attn_implementation="eager"`. ⛔ Đừng cài `flash_attn` để "cho giống thẻ
mô hình" — đúng tổ hợp này đã làm **ShowUI-2B ra NaN**.

**② Thẻ ghim transformers 4.43, Kaggle cài sẵn 5.x.** Mã điều khiển từ xa viết cho 4.43 rất dễ vỡ
trên 5.x, và lỗi sẽ nổ ở `from_pretrained` chứ không phải lúc chấm. Ô 2 in ra phiên bản thật
trước khi tải 8,5 GB.

**③ Lệch tỉ lệ khung hình — chặn tinh vi nhất, không báo lỗi.** Ảnh dọc 0,45 vào khung ngang 1,50.
· Nếu bộ xử lý **kéo giãn** thì toạ độ tương đối vẫn đúng, không sao.
· Nếu nó **đệm viền** thì toạ độ tương đối trỏ vào khung đã đệm ⇒ **sai hệ thống theo trục dọc**,
  và mọi con số sau đó vô nghĩa mà không có gì báo.
⭐ **Phân biệt được bằng probe:** tách sai số theo `dx` và `dy` riêng. Lệch **dọc** lớn hơn lệch
**ngang** nhiều lần = đang bị đệm viền ⇒ **dừng**.

---

## Lát chấm: đúng 2.532 bước của phép B

⛔ Dùng **đúng lát của phép B**, không dùng 4.463. Lý do: so được thẳng với hàng UI-Venus đã có
(`runs/venus/score_venus_*_2532_raw.jsonl`), và rẻ hơn 1,76 lần. `report/140` mục cuối đã ghi
sẵn *"chạy trên đúng lát 2.532 của phép B"*.

---

## Ô 0 — cổng probe, **~15 phút**, chạy TRƯỚC khi cam kết cả lượt

⭐ Ba cổng dưới đây tốn 15 phút và cứu được 5,6 giờ. Đừng bỏ.

```python
import subprocess, os, json, math, statistics, glob
WS = "/kaggle/working/ws"

# ── cổng ②: phiên bản, in ra TRƯỚC khi tải 8,5 GB ───────────────────────────
import transformers, torch
print("transformers", transformers.__version__, "· torch", torch.__version__,
      "· card", torch.cuda.get_device_name(0),
      "· capability", torch.cuda.get_device_capability())
print("→ capability < (8,0) nghĩa là Turing/Pascal: KHÔNG bf16, KHÔNG flash-attn 2")
```

```python
# ── cổng ①+③: chấm 40 bước ở CHẾ ĐỘ GATE (câu chuẩn), rồi soi dx và dy RIÊNG ──
# gate dùng câu do người chú thích viết, giống hệt nhau ở mọi nhánh ⇒ không thể thiên vị
# nhánh nào. Đây đúng luật chọn dụng cụ đã khoá từ hồi UI-Venus.
r = subprocess.run(["python", f"{WS}/harness/score_run.py", "--mode", "gate",
                    "--grounder", "phiground", "--n", "40",
                    "--out", "/kaggle/working/probe_phi.json"],
                   capture_output=True, text=True, cwd=WS)
print(r.stdout[-3000:]); print(r.stderr[-2000:])
```

```python
# ── đọc probe: ba cổng ──────────────────────────────────────────────────────
R = [json.loads(l) for l in open("/kaggle/working/probe_phi_raw.jsonl", encoding="utf-8")]
R = [r for r in R if r.get("pred_xy")]
dx = [abs(r["pred_xy"][0]-r["gold_xy"][0])/r["wh"][0]*100 for r in R]
dy = [abs(r["pred_xy"][1]-r["gold_xy"][1])/r["wh"][1]*100 for r in R]
med = lambda v: statistics.median(v) if v else float("nan")
print(f"n trả toạ độ: {len(R)}/40")
print(f"  lệch NGANG trung vị {med(dx):6.2f}% bề ngang")
print(f"  lệch DỌC   trung vị {med(dy):6.2f}% bề cao")
print(f"  tỉ số dọc/ngang = {med(dy)/max(med(dx),1e-9):.2f}")
print(f"  UGround-2B để so (cổng A, runs/gate_a/gate_A.json, n=300):")
print(f"     trung vị 0,73% · p75 8,76% — tính bằng statistics.quantiles(errs, n=4)")
```

| cổng | ngưỡng | không đạt thì |
|---|---|---|
| ① nạp được mô hình | không `ImportError`/`NaN`, `dtype` in ra là `torch.float16` | ⛔ **dừng**, không có đường vòng trên T4 |
| ② trả toạ độ | ≥ **36/40** bước có `pred_xy` | ⛔ dừng — mẫu câu nhắc hoặc cách đọc số sai |
| ③ **không đệm viền** | tỉ số **dọc/ngang < 3** | ⛔ dừng — đang bị đệm viền, mọi số sau vô nghĩa |
| ④ đáng chạy tiếp | lệch ngang trung vị **< 10%** | dưới ngưỡng thì vẫn chạy được nhưng ghi rõ là dụng cụ kém hẳn |

⛔ **Cổng ③ là cái không được bỏ qua.** Nó là chặn duy nhất mà kết quả sai vẫn trông như số
bình thường. Đúng dạng lỗi câm đã trả giá ngày 20/8.

---

## Ô 1 — chạy đủ lát 2.532, ba nhánh (~5,6 h)

Dùng lại **Ô 2 (hàm chạy-và-chờ)** của `harness/kaggle_phase1_noisuy_9_9.md`, không viết lại.

```python
for ten, preds in (("base", "preds_base.jsonl"),
                   ("s1",   "preds_s1_seed101.jsonl"),
                   ("s2",   "preds_s2_seed101.jsonl")):
    out = f"/kaggle/working/score_phi_{ten}_2532.json"
    if os.path.exists(out): print("bỏ qua:", ten); continue
    chay_va_cho(["python", "harness/score_run.py", "--mode", "score",
                 "--grounder", "phiground", "--preds", f"{PRED}/{preds}",
                 "--n", "2532", "--out", out],
                f"/kaggle/working/phi_{ten}.log",
                dich=f"/kaggle/working/score_phi_{ten}_2532_raw.jsonl",
                can=2532, nhip=120)
```

⚠️ `--n 2532` lấy **2.532 bước đầu** sau khi lọc bước chạm, đúng cách phép B đã lấy. Kiểm khoá
trùng với `runs/venus/score_venus_base_2532_raw.jsonl` **trước** khi đọc kết quả — xem Ô 3.

⭐ **Nếu còn hạn mức, chạy thêm `GRPO-point`** (`runs/grpo_point/preds_grpo_point_seed101.jsonl`).
Nó là nhánh tiêu đề, nên có hàng Phi-Ground cho nó thì bảng mới trọn.

---

## Ô 2 — gói kết quả

```python
import zipfile, glob, os, hashlib
Z = "/kaggle/working/ket_qua_phiground.zip"
with zipfile.ZipFile(Z, "w", zipfile.ZIP_DEFLATED) as z:
    for m in ("score_phi_*.json", "score_phi_*_raw.jsonl", "phi_*.log", "probe_phi*"):
        for p in sorted(glob.glob(f"/kaggle/working/{m}")):
            z.write(p, os.path.basename(p))
print(os.path.getsize(Z)/2**20, "MB · md5",
      hashlib.md5(open(Z,"rb").read()).hexdigest())
```

Bung vào **`runs/phiground/`**. ⛔ Đặt thẳng vào thư mục của phép đo đó.

---

## Ô 3 — đọc kết quả, ở máy nhà, 0 GPU

⛔ **Ba phép kiểm bắt buộc TRƯỚC khi đọc số:**

1. **Khoá trùng lát phép B.** Tập `(episode_id, step_id)` của `score_phi_s1_2532_raw.jsonl` phải
   **trùng khít** `runs/venus/score_venus_s1_2532_raw.jsonl`. Lệch một bước là không so được.
2. **Phép so đối chiếu S1 − Base.** Phép B đã đo: UGround **+10,35** · UI-Venus **+9,68** trên lát
   này. Nếu Phi-Ground cho chênh lệch **giữ được ≳ 90%** thì thang đo không bị nén và Δ đọc được.
   ⛔ Nếu chênh lệch **sụp về gần 0** thì dụng cụ **không phân giải nổi** ba nhánh — khi đó điểm
   tuyệt đối của nó vô nghĩa, và đó là kết quả phải báo, không phải lỗi để giấu.
3. **Thứ tự ba nhánh.** Base < S2 < S1 dưới cả hai dụng cụ cũ. Đảo thứ tự là dấu hiệu hỏng.

**Bốn kết cục, khoá TRƯỚC khi có số:**

| kết cục | đọc thế nào |
|---|---|
| chênh lệch S1−Base giữ ≳ 90%, điểm tuyệt đối **thấp hơn** | ⭐ kỳ vọng chính. **Đòn *cùng họ Qwen* ĐÓNG.** Báo như phép B: dụng cụ khác họ, cùng kết luận |
| giữ ≳ 90%, điểm tuyệt đối **cao hơn** | đòn đóng, **và** có thêm một hàng báo kèm cao hơn. ⛔ vẫn không đổi tiêu đề |
| chênh lệch **sụp về gần 0** | dụng cụ không phân giải được — báo thẳng, ⛔ đừng dùng điểm tuyệt đối của nó vào bất kỳ bảng nào |
| không qua nổi cổng probe | ghi *"đã thử, không chạy được trên T4, nêu lý do kỹ thuật"*. Đòn *cùng họ* **vẫn mở** và phải khai như một hạn chế |

⛔ **Cấm** chọn kết cục nào có lợi rồi báo mỗi cái đó. Cả bốn ô đã khoá ở đây, trước khi chạy.

---

## Bốn luật chung của lượt Kaggle

Giống hệt `kaggle_phase1_noisuy_9_9.md`: chạy tương tác trước Save Version sau · tắt thanh tiến
trình và cho tiến trình con ghi ra tệp · không có nhịp sống sau 4 phút thì dừng · kết quả trùng
nhau tới nhiều chữ số giữa các cấu hình khác nhau là dấu hiệu **hỏng**, không phải bền vững.
