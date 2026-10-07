# 299 — ACTION: chấm TEST bước chạm cho GRPO thưởng CIDEr-D (A2), so với ck500 (7/10/2026)

File tự chứa. Đọc từ đầu tới cuối là chạy được, không cần mở file nào khác.

## 1. Mục đích

Luận văn đang nhận phương pháp đề xuất là **GRPO thưởng SPICE (`ck500`)**. Câu hội đồng dễ hỏi nhất: *vì sao thưởng SPICE mà không thưởng CIDEr như các bài trước* (SCST, CVPR 2017; bài GRPO cho chú thích ảnh, arXiv 2503.01333). Dự án đã train sẵn đúng nhánh trả lời câu này: A2 của đợt CTG, là GRPO thưởng CIDEr-D, học tiếp từ S1/101, có điểm lưu ở bước 500 và 1000. A2 mới có điểm test ở bước không chạm; ở bước chạm (4.463 bước, nơi tính executability) thì chưa.

Lượt này: sinh câu và chấm executability trên 4.463 bước chạm cho `A2_500` và `A2_1000`, cùng đường sinh, cùng dụng cụ chấm đã cho ck500 60,65. Một commit Kaggle T4 x2, 0 đồng, khoảng 9 đến 10 giờ.

## 2. Ba nhánh khác nhau ở đâu

|  | ck500 (đang là phương pháp đề xuất) | A2_500 (phép so chính) | A2_1000 (đọc thêm) |
|---|---|---|---|
| phần thưởng | SPICE - 0,02 × phạt câu dài | CIDEr-D/10 - 0,02 × phạt câu dài | như A2_500 |
| điểm xuất phát, LoRA, tham chiếu KL | S1/101 hoà, LoRA mới cùng cỡ S1, KL về S1 | như ck500 | như ck500 |
| G · câu nhắc mỗi bước · lô · β · lr · loss | 8 · 2 · 4×4 · 0,04 · 1e-5 · dapo, chuẩn hoá theo nhóm | như ck500 | như ck500 |
| số bước cập nhật | 500 | 500 | 1.000 |
| tập câu nhắc | 1.000 câu (đầu danh sách xáo hạt 101) | 2.000 câu (gồm trọn 1.000 câu của ck500) | như A2_500 |
| đã duyệt | 1 lượt trên 1.000 câu | nửa lượt trên 2.000 câu | 1 lượt trên 2.000 câu |
| máy và kiểu số lúc train | Kaggle T4, fp16 | Colab A100, bf16 | như A2_500 |
| CTG | không có | tính và ghi log, không cộng vào advantage (mã có `assert`) | như A2_500 |
| sinh câu test | S1 hoà fp16, gắn điểm lưu, greedy, 96 token, T4 | như ck500 | như ck500 |

Nguồn: `harness/grpo_spice.py` (`N_PROMPT` 1000, cấu hình in trong `runs/grpo_spice/train_c1.log`), `harness/ctg_grpo.py` (`N_PROMPT` 2000, cấu hình in trong `runs/ctg/train/A2/train_A2_den_b360.log`). Hai tệp dùng chung hàm `dung_hang` và hạt 101 nên tập 2.000 câu chứa tập 1.000 câu.

Vì sao `A2_500` là phép so chính: cùng số bước cập nhật và cùng số câu nhắc đã duyệt (1.000) với ck500, nên khác biệt còn lại chủ yếu là phần thưởng. `A2_1000` vừa đổi phần thưởng vừa train gấp đôi, nên chỉ đọc thêm.

## 3. Số đã có

### 3a. ck500 và S1 trên test, 4.463 bước chạm (đã công bố, trích được)

| thước | S1/101 | ck500 | Δ | KTC95 |
|---|---:|---:|---:|---|
| Executability | 59,11 | 60,65 | +1,55 | [+0,80; +2,33] |
| Hộp phần tử (D.3) | 65,49 | 67,02 | +1,52 | [+0,77; +2,29] |
| AitW | 74,37 | 76,25 | +1,88 | [+1,17; +2,63] |
| AitW cận trên | 81,04 | 82,90 | +1,86 | [+1,17; +2,60] |
| +14% theo trục | 67,24 | 68,90 | +1,66 | [+0,90; +2,46] |
| Đúng loại thao tác | 94,35 | 95,97 | +1,61 | [+1,17; +2,08] |
| SPICE | 44,37 | 45,79 | +1,42 | [+0,69; +2,16] |
| CIDEr-D | 416,12 | 430,05 | +13,93 |  |

### 3b. A2_1000 trên test, 2.495 bước KHÔNG chạm (đã có, trích được)

| nhóm | n | S1 | ck500 | A2_1000 |
|---|---:|---:|---:|---:|
| toàn bộ | 2.495 | 85,97 | 84,29 | 84,45 |
| cuộn | 755 | 83,97 | 77,75 | 77,62 |
| quay lại | 270 | 72,96 | 67,04 | 65,56 |

`A2_1000 - ck500` ở bước cuộn: -0,13 [-1,77; +1,51]. Đổi SPICE sang CIDEr-D không gỡ được tác hại ở bước cuộn.

### 3c. Tập kiểm định C1, 249 bước chạm (⛔ số val, chỉ để đoán trước, cấm trích)

| nhánh | exec (số bước trúng / 249) |
|---|---:|
| S1 | 158 (63,45) |
| ck500 | 165 (66,27) |
| A2_500 | 163 (65,46) |
| A2_1000 | 164 (65,86) |

Đoán trước: trên test, A2 và ck500 nhiều khả năng không tách được.

**Sửa lỗi trong chat:** chat trước nói “A2 thấp hơn ck500 khoảng 0,4 điểm exec trên val”. Con số đó là của `A2_1000` (164 so với 165). `A2_500`, nhánh dùng làm phép so chính, thấp hơn 2 bước, tức 0,80 điểm. Dự đoán vẫn như cũ: nhiều khả năng hoà.

## 4. Luật đọc — chốt TRƯỚC khi có số

Câu hỏi của người dùng: *“nếu GRPO thưởng CIDEr hơn thì mình lấy cái đó hả?”* Trả lời: không tự động. Chọn phương pháp theo điểm test sau khi đã xem số là chọn trên tập kiểm. Vì vậy luật dưới đây chốt trước, và chỉ đọc trên một phép so: `A2_500 - ck500`, executability, 4.463 bước, KTC95 bootstrap gom cụm theo ứng dụng (cùng hàm đã sinh mọi KTC trong luận văn).

| hàng | điều kiện | làm gì |
|---|---|---|
| S | cận trên KTC < 0 | Giữ ck500. Thêm vào luận văn: ở cùng 500 bước, thưởng SPICE hơn thưởng CIDEr-D. Đây là căn cứ cho việc chọn SPICE. |
| H | KTC chứa 0 | Giữ ck500 làm phương pháp đề xuất. A2_500 vào luận văn như phép so phần thưởng. Câu đóng góp hẹp lại thành “thưởng bằng một thước so câu với câu chuẩn”; SPICE và CIDEr-D cho mức tương đương. |
| C | cận dưới KTC > 0 | A2_500 hơn ck500 có ý nghĩa. Đề xuất đổi phương pháp đề xuất sang GRPO thưởng CIDEr-D, nhưng chỉ sau khi người dùng duyệt mục 8, vì kéo theo nhiều việc. |

Ba ghi chú cho mọi hàng:

- `A2_1000` không đổi hàng, kể cả khi `A2_1000` hơn ck500 có ý nghĩa: nhánh này khác ck500 cả phần thưởng lẫn số bước, nên không quy được phần hơn cho phần thưởng.
- Cả ck500 lẫn A2 đều một hạt giống. KTC ghép cặp chỉ phủ nhiễu của tập kiểm, không phủ nhiễu giữa hai lần train. Hai hạt của S1 đã chênh nhau 0,52 điểm exec (59,11 so với 59,62), nên ở hàng C mà Δ dưới khoảng 1 điểm thì luận văn phải ghi rõ mức chênh này vẫn nằm trong cỡ nhiễu giữa hai hạt giống.
- Thước chữ (SPICE, CIDEr-D...) chỉ để mô tả. A2 được thưởng CIDEr-D nên gần như chắc chắn cao hơn ở CIDEr-D, và ck500 cao hơn ở SPICE. Đó không phải căn cứ để đổi hàng.

## 5. Chạy trên Kaggle

### 5.0. Chuẩn bị (không phải upload gì mới)

Notebook mới, **GPU T4 x2, Internet On**. *Add Input* năm dataset, tất cả đã có từ các lượt trước:

| dataset | dùng cho | đã dùng ở lượt |
|---|---|---|
| `thesis-score` | `test.jsonl` · `ocr.jsonl` · 4.463 ảnh chạm · gói `harness/` có `score_run.py` đã chấm S1 59,11 và ck500 60,65 | mọi lượt chấm test |
| `fgrb-p1-bundle` | adapter S1/101 để hoà | ck500 test, CTG |
| `grpo-spice-script` (bản mới nhất) | `gen_test_grpo.py` md5 `b18ec1aa...` · `grpo_spice.py` `07ea87b6...` · `build_branch_data.py` `619e63e1...` | CTG không chạm 6/10 |
| `ctg-ckpts` | `ctg_ckpt_500/A2_500/` · `ctg_ckpt_1000/A2_1000/` | CTG val bước 500 và 1000, CTG không chạm |
| `grpo-spice-ck500` | adapter ck500 md5 `491fa667...`, cho bước kiểm tái lập ở Ô 4 | ck500 test 2/10 |

Hạn mức Kaggle: lượt này tốn khoảng 10 giờ trong 30 giờ mỗi tuần. Tuần này còn dưới 11 giờ thì đợi tuần sau.

### 5.1. Nếu `ctg-ckpts` bản mới nhất không còn `A2_500`

Ô 2 sẽ dừng với dòng `DỪNG: cần đúng một thư mục A2_500`. Khi đó có hai cách:

1. Mở trang dataset `ctg-ckpts`, tab **Versions**, tìm bản có `ctg_ckpt_500`. Tải `ctg_ckpt_500/A2_500/` về máy.
2. Hoặc lấy `checkpoint-500` của nhánh A2 trên Drive (`MyDrive/thesis/ctg/…/A2/checkpoint-500`).

Dựng dataset mới tên `ctg-a2-500`, bên trong là một thư mục tên đúng `A2_500`, chỉ chứa `adapter_config.json` và `adapter_model.safetensors` (bỏ `optimizer.pt`, `ref/`...). Gắn dataset đó cùng `ctg-ckpts`, rồi chạy lại Ô 2.

### Ô 1 — gói

```python
import subprocess, sys, os, time
T_NB = time.time()                    # mốc đầu notebook; Ô 3 dừng hai chuỗi trước trần 12 h tính từ đây

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode

sh(f"{sys.executable} -m pip install -q -U transformers peft accelerate torchao bitsandbytes pycocoevalcap 'trl==0.29.1' 2>&1 | tail -3")
sh(f'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.device_count(), [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])"')
```

Phải thấy `2 ['Tesla T4', 'Tesla T4']`. Chỉ một card thì vẫn chạy được, nhưng lâu gấp đôi và sẽ vượt 12 giờ: khi đó chạy hai commit theo mục 5.3.

### Ô 2 — đường dẫn và kiểm đầu vào

```python
import glob, json, shutil, hashlib, shlex, signal
W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()

CAN = {"gen_test_grpo.py": "b18ec1aa3fd037ddffb9411db63c2a3f",
       "grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf",
       "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912"}
for f, h in CAN.items():
    dung = [p for p in glob.glob(f"/kaggle/input/**/{f}", recursive=True) if md5(p) == h]
    assert dung, f"DỪNG: không thấy {f} đúng md5 {h[:8]}... — gắn grpo-spice-script bản mới nhất"
    shutil.copy(dung[0], f"{W}/{f}")

BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d)
MERGED = f"{W}/s1_merged"

DIRS = sorted({os.path.dirname(f) for f in glob.glob("/kaggle/input/**/adapter_model.safetensors", recursive=True)})
H = {d: md5(f"{d}/adapter_model.safetensors") for d in DIRS}
CK500 = next((d for d in DIRS if H[d] == "491fa6677340393f1e4464c08a0cec98"), None)
assert CK500, "DỪNG: không thấy adapter ck500 (md5 491fa667...) — gắn dataset grpo-spice-ck500"
CK = {}
for t in ("A2_500", "A2_1000"):
    c = [d for d in DIRS if os.path.basename(d) == t]
    assert len(c) == 1, f"DỪNG: cần đúng một thư mục {t}, thấy {c} — xem mục 5.1 của file 299"
    CK[t] = c[0]
    base = json.load(open(f"{c[0]}/adapter_config.json")).get("base_model_name_or_path", "")
    print(f"{t}: {c[0]} · md5 {H[c[0]]} · base {base}", flush=True)
assert H[CK["A2_500"]] != H[CK["A2_1000"]], "DỪNG: hai điểm lưu A2 trùng nhau"

TA = None
for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True):
    r = os.path.dirname(t)
    if sum(1 for _ in open(t)) == 6958 and len(glob.glob(f"{r}/images/*.png")) >= 4463 and os.path.exists(f"{r}/ocr.jsonl"):
        TA = r
assert TA, "DỪNG: không thấy test_ac đủ 6.958 dòng + 4.463 ảnh (dataset thesis-score)"
assert md5(f"{TA}/test.jsonl") == "da58299ee551a926a21cbecb5232bf78", "DỪNG: test.jsonl lệch máy nhà"
PKG = os.path.dirname(os.path.dirname(os.path.dirname(TA)))      # .../thesis/harness/dg1_cache/test_ac → .../thesis
WS = f"{W}/thesis"
shutil.copytree(f"{PKG}/harness", f"{WS}/harness", dirs_exist_ok=True, ignore=shutil.ignore_patterns("images"))
link = f"{WS}/harness/dg1_cache/test_ac/images"
if os.path.lexists(link): os.remove(link)
os.symlink(f"{TA}/images", link)

# nối tiếp (mục 5.3): nếu gắn Output của commit 299 trước làm input thì chép tệp dở về
for p in glob.glob("/kaggle/input/**/a2_test_299/pred_A2_*_test.jsonl", recursive=True) + \
         glob.glob("/kaggle/input/**/a2_test_299/score_A2_*_test_raw.jsonl", recursive=True):
    q = f"{W}/{os.path.basename(p)}"
    if not os.path.exists(q):
        shutil.copy(p, q); print("[nối tiếp] chép", os.path.basename(p), sum(1 for _ in open(q)), "dòng", flush=True)
print("BUNDLE", BUNDLE, "\nCK500", CK500, "\nTA   ", TA, "\nWS   ", WS, flush=True)
```

Phải thấy hai dòng `A2_500: ...` và `A2_1000: ...` với hai md5 khác nhau, không có dòng DỪNG. Chép hai md5 gửi về.

### Ô 3 — hoà S1, tải UGround, hàm chạy có nhịp sống

```python
TEST = True        # chạy thử tương tác; đổi False trước khi commit
GIO_CAT = 11.2     # giờ tính từ đầu notebook; quá mốc này thì dừng hai chuỗi để kịp lưu Output
ENV = {**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1"}
NCARD = __import__("torch").cuda.device_count()

def chay(viec, nhip=120):
    """viec = [(tên, lệnh bash, [các log theo thứ tự], gpu)]; mỗi chuỗi một card, một nhóm tiến trình riêng."""
    Q = {}
    for ten, lenh, logs, gpu in viec:
        Q[ten] = (subprocess.Popen(["bash", "-c", lenh], start_new_session=True,
                                   env={**ENV, "CUDA_VISIBLE_DEVICES": str(gpu)}), logs)
        time.sleep(60 if len(viec) > 1 else 1)      # lệch giờ nạp mô hình để RAM không chạm đỉnh cùng lúc
    while any(q.poll() is None for q, _ in Q.values()):
        time.sleep(30 if TEST else nhip)
        for ten, (q, logs) in Q.items():
            lg = next((l for l in reversed(logs) if os.path.exists(l)), None)
            L = [x.strip() for x in open(lg, errors="ignore") if x.strip()] if lg else []
            st = "chạy" if q.poll() is None else f"xong mã {q.returncode}"
            print(f"  {(time.time()-T_NB)/3600:5.2f} h · {ten} [{st}] · {os.path.basename(lg) if lg else '-'} · "
                  f"{L[-1][:90] if L else 'chưa có dòng nào'}", flush=True)
        if (time.time() - T_NB) / 3600 > GIO_CAT:
            for q, _ in Q.values():
                if q.poll() is None:
                    os.killpg(q.pid, signal.SIGTERM)
            print(f"🔴 đã tới {GIO_CAT} h — dừng để kịp lưu Output. Làm theo mục 5.3, tệp tự nối tiếp.", flush=True)
            break
    for ten, (q, logs) in Q.items():
        for lg in logs:
            if os.path.exists(lg):
                print(f"--- {ten} · {os.path.basename(lg)} ---\n" + "".join(open(lg, errors="ignore").readlines()[-4:]), flush=True)

r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED],
                   cwd=W, capture_output=True, text=True, env={**ENV, "CUDA_VISIBLE_DEVICES": "0"})
print((r.stdout + r.stderr)[-1500:]); assert r.returncode == 0, "DỪNG: hoà lỗi"

from huggingface_hub import snapshot_download             # tải trước để hai tiến trình chấm không cùng tải một lúc
print("UGround:", snapshot_download("osunlp/UGround-V1-2B"), flush=True)
```

### Ô 4 — kiểm tái lập ck500 trên 20 bước chạm đầu

Sinh lại 20 câu của ck500 bằng môi trường hôm nay, so với câu của lượt 2/10. Trùng ≥ 19/20 thì môi trường đủ giống để phép so A2 - ck500 không lẫn biến môi trường.

```python
TA_ARGS = ["--recs", f"{TA}/test.jsonl", "--ocr", f"{TA}/ocr.jsonl", "--images", f"{TA}/images", "--tap-only", "--no-q4"]
KY = {   # 20 dòng đầu của runs/grpo_spice/pred_ck500_test.jsonl (lượt 2/10, md5 tệp 328847ac...)
    (18171, 1): 'Open the Dimitri vegas song of Martin garrix',
    (18173, 1): 'click on the search bar at the top of the screen',
    (18173, 3): 'Click on the search icon at the bottom right corner of the screen',
    (18175, 1): 'Search for Venice',
    (18175, 3): 'Click on the search icon',
    (18176, 1): 'Click on the Flights icon at the top of the screen.',
    (18176, 2): 'Click on the One-way tab.',
    (18176, 3): 'Click on the first input box.',
    (18176, 5): 'Click on the tab Toronto Pearson International.',
    (18176, 6): 'Click on the Second input box.',
    (18176, 8): 'Select the tab Vancouver International.',
    (18176, 9): 'Click on the date section.',
    (18176, 10): 'Select the date 15 december.',
    (18176, 11): 'Click on the Confirm tab at the bottom right corner of the screen.',
    (18176, 12): 'Click on the tab "First Class" to select the class of the flight.',
    (18176, 13): 'Select the tab Economy.',
    (18176, 14): 'Click on the Done tab at the bottom of the screen.',
    (18176, 15): 'Click on the search icon.',
    (18178, 1): 'Click on the Cruise Search tab at the bottom of the screen.',
    (18178, 2): 'Click on the sail months option.',
}
out = f"{W}/kiem_ck500_299.jsonl"
if os.path.exists(out): os.remove(out)
g = ["python", "gen_test_grpo.py", "--bundle", BUNDLE, "--merged", MERGED, "--ckpt", CK500,
     "--n", "20", "--out", out] + TA_ARGS
chay([("kiem_ck500", f"cd {W} && {shlex.join(g)} > {W}/kiem_ck500_299.log 2>&1", [f"{W}/kiem_ck500_299.log"], 0)])
P = {(o["episode_id"], o["step_id"]): o["pred"].strip() for o in map(json.loads, open(out))}
x = sum(P.get(k) == v for k, v in KY.items())
for k, v in KY.items():
    if P.get(k) != v:
        print(f"  {k}: 2/10  {v!r}\n  {' ' * len(str(k))} hôm nay {P.get(k)!r}", flush=True)
print(f"[kiểm ck500] {x}/20 câu trùng lượt 2/10", flush=True)
assert x >= 19, "DỪNG: môi trường hôm nay không tái lập ck500 — đừng chạy A2, gửi output Ô 1 và Ô 4 về"
```

### Ô 5 — hai chuỗi song song: sinh rồi chấm (A2_500 ở GPU 0, A2_1000 ở GPU 1)

```python
duoi = "_thu" if TEST else ""
viec = []
for i, t in enumerate(("A2_500", "A2_1000")):
    pred, sc = f"{W}/pred_{t}_test{duoi}.jsonl", f"{W}/score_{t}_test{duoi}.json"
    g = ["python", "gen_test_grpo.py", "--bundle", BUNDLE, "--merged", MERGED, "--ckpt", CK[t],
         "--out", pred] + (["--n", "5"] if TEST else []) + TA_ARGS
    c = ["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground",
         "--preds", pred, "--out", sc] + (["--n", "3"] if TEST else [])
    lg, lc = f"{W}/gen_{t}_test{duoi}.log", f"{W}/cham_{t}_test{duoi}.log"
    viec.append((t, f"cd {W} && {shlex.join(g)} > {lg} 2>&1 && cd {WS} && {shlex.join(c)} > {lc} 2>&1",
                 [lg, lc], i % NCARD))
if NCARD >= 2:
    chay(viec)
else:
    for v in viec:
        chay([v])

for t in ("A2_500", "A2_1000"):
    pred, sc = f"{W}/pred_{t}_test{duoi}.jsonl", f"{W}/score_{t}_test{duoi}.json"
    raw = sc.replace(".json", "_raw.jsonl")
    n = sum(1 for _ in open(pred)) if os.path.exists(pred) else 0
    m = sum(1 for _ in open(raw)) if os.path.exists(raw) else 0
    lg = f"{W}/gen_{t}_test{duoi}.log"
    dong = [l for l in open(lg, errors="ignore").read().splitlines()
            if l.startswith(("[dữ liệu]", "[điểm lưu]", "[xong]"))] if os.path.exists(lg) else []
    print(f"{t}: câu {n}/{5 if TEST else 4463} · đã chấm {m}/{3 if TEST else 4463} · {dong}", flush=True)
print("Đủ cả hai thì sang Ô 6. Thiếu thì vẫn chạy Ô 6 rồi làm theo mục 5.3. Đừng tự đọc số exec ở đây.")
```

Mỗi log sinh phải có `[dữ liệu] ... 4463 bước · thiếu OCR 0 · thiếu ảnh 0`, `[điểm lưu] .../A2_500` (hoặc `A2_1000`), `[xong] 4463 câu · rỗng ...`. Nhịp sống in xen kẽ hai tên là bình thường.

### Ô 6 — đóng zip, dọn Output

```python
shutil.rmtree(MERGED, ignore_errors=True)                 # bản hoà ~7 GB, không được nằm trong Output
Z = f"{W}/a2_test_299"
os.makedirs(Z, exist_ok=True)
for p in glob.glob(f"{W}/pred_A2_*") + glob.glob(f"{W}/score_A2_*") + glob.glob(f"{W}/*.log") + glob.glob(f"{W}/kiem_ck500_299.*"):
    shutil.copy(p, Z)
shutil.make_archive(Z, "zip", Z)
shutil.rmtree(WS, ignore_errors=True)                     # bỏ bản sao harness và liên kết tới thư mục ảnh
print(sorted(os.listdir(Z)), os.path.getsize(Z + ".zip") // 1024, "KB", flush=True)
```

### 5.2. Trình tự bấm

1. **Chạy thử tương tác** (`TEST = True`): *Run All*, khoảng 20–25 phút. Gửi về output Ô 1, Ô 2, Ô 4, Ô 6. Ô 4 phải `[kiểm ck500] x/20` với x ≥ 19.
2. Ổn thì sửa Ô 3 thành `TEST = False` → **Stop session → Save Version → Save & Run All**. Khoảng 9–10 giờ (sinh ~3,5 h ở 2,5–2,8 s/bước, chấm ~5 h ở 0,25 bước/s; hai chuỗi chạy cùng lúc). Có thể gặp máy.
3. Kiểm cuối log commit: `[kiểm ck500] x/20` với x ≥ 19, và hai dòng `A2_...: câu 4463/4463 · đã chấm 4463/4463`.
4. Tải `a2_test_299.zip` từ Output, giải nén vào `/Users/P836901/Documents/Self-Learning/thesis/_kaggle_out/299/` (ngoài `thesis-master/` để không mất khi clone lại). Trong thư mục phải có trực tiếp `pred_A2_500_test.jsonl`, `score_A2_500_test.json`, `score_A2_500_test_raw.jsonl`, ba tệp tương ứng của `A2_1000`, các log, `kiem_ck500_299.jsonl`. Kaggle hay đổi đuôi `.jsonl` thành `.txt`; sửa tên đổi lại.

### 5.3. Nếu commit bị dừng ở 11,2 giờ

Ô 5 in 🔴 `đã tới 11.2 h`, Ô 6 vẫn đóng zip. Tạo commit mới cùng notebook: **Add Input** thêm chính Output của commit vừa rồi (có thư mục `a2_test_299/`), giữ `TEST = False`, *Save & Run All*. Ô 2 chép tệp dở về; sinh và chấm đều tự nối tiếp từ dòng cuối, Ô 4 chạy lại mất khoảng 2 phút.

## 6. Đọc ở máy nhà (0 GPU)

Chép nguyên văn Phụ lục A vào `/Users/P836901/Documents/Self-Learning/thesis/_scripts/299/doc_299.py`.

Mac (thước vị trí: exec, D.3, AitW, AitW cận trên, ±14% theo trục, đúng loại thao tác):

```bash
cd /Users/P836901/Documents/Self-Learning/thesis
_scripts/_venv/bin/python _scripts/299/doc_299.py --kho thesis-master --a2 _kaggle_out/299
```

WSL (thêm thước chữ: BLEU-4, METEOR, ROUGE-L, CIDEr-D, SPICE, chrF; cần Java 8 ở `~/.jdk`, khoảng 30–40 phút):

```bash
cd <gốc kho trên WSL>
~/.venvs/thesis/bin/python doc_299.py --kho . --a2 <thư mục đã chép a2_test_299> --chu
# thêm --bert nếu muốn cột BERTScore (thêm 15–30 phút mỗi nhánh trên CPU)
```

Script tự kiểm trước khi in số A2, lệch thì dừng:

- S1 và ck500 ra đúng sáu số vị trí đã công bố (bảng 3a);
- ck500 - S1 exec ra +1,55 [+0,80; +2,33];
- KTC exec của từng nhánh khớp tệp json Kaggle; câu trong tệp thô trùng tệp dự đoán;
- với `--chu`: S1 và ck500 ra đúng bảy số chữ đã lưu (±0,025).

Script in bảng điểm, sáu phép so ghép cặp, phân rã cứu/phá theo loại thao tác, và một dòng `[luật 299 §4] hàng ...`. Kết quả ghi vào `_kaggle_out/299/doc_299.json`.

Đã chạy khô 7/10 trên Mac (`--gia`: câu ck500 giả làm A2_500, câu S1 giả làm A2_1000), tự kiểm đạt, ra đúng `A2_500 - ck500 = 0` và `A2_500 - S1 = +1,55 [+0,80; +2,33]` (mục 9).

## 7. Sau khi có số: đoạn dán vào luận văn (hàng S hoặc H)

⚠️ Tệp đích nằm trong repo, sẽ mất nếu xoá clone. Sửa xong **phải commit trước khi clone lại**:

```bash
git add thesis/chapters/ch6_thucnghiem.tex && git commit -m "ch6: thêm phép so thưởng SPICE với thưởng CIDEr-D" && git push
```

Đích: `thesis-master/thesis/chapters/ch6_thucnghiem.tex`, dán ngay sau đoạn `\paragraph{So với các nhánh khác.}` (kết thúc bằng câu *... đặt các nhánh chính cạnh nhau dưới ba luật.*). Thay bốn chỗ `(…)` bằng số trong `doc_299.json`, mục `so["A2_500 - ck500"]["Executability"]` và `diem["Executability"]["A2_500"]`, viết dấu phẩy thập phân.

```tex
\paragraph{Thưởng SPICE so với thưởng CIDEr-D.} Để kiểm việc chọn SPICE, chúng tôi so với một nhánh cùng
thuật toán, cùng điểm xuất phát S1 hạt giống $101$, cùng kích thước nhóm, hệ số KL và tốc độ học, chỉ thay
phần thưởng bằng CIDEr-D~\cite{cider}, phần thưởng mà SCST~\cite{scst} đã dùng. Ở cùng $500$ bước cập nhật,
nhánh thưởng CIDEr-D đạt executability $(A2\_500)$, chênh $(\Delta)$ điểm so với nhánh thưởng SPICE, khoảng tin
cậy $[(\lo); (\hi)]$. (CÂU THEO HÀNG) Hai nhánh còn khác nhau ở tập câu nhắc ($2.000$ so với $1.000$ câu, tập lớn
chứa tập nhỏ) và ở máy huấn luyện, và cả hai đều chỉ có một hạt giống.
```

**(CÂU THEO HÀNG):**

- **hàng H:** Khoảng tin cậy chứa $0$, nên trên bài toán này việc chọn SPICE hay CIDEr-D không làm đổi kết quả; phần đề tài nhận là việc thưởng bằng một thước so câu với câu chuẩn, không phải riêng SPICE.
- **hàng S:** Khoảng tin cậy nằm hẳn dưới $0$, tức trong hai phần thưởng có tiền lệ, SPICE cho câu dẫn tới đúng phần tử thường xuyên hơn.
- **hàng C:** không dán, sang mục 8.

Câu 8 ch1 (*“phương pháp đề xuất không nhận điểm mới ở thuật toán, cũng như ở việc chọn SPICE làm phần thưởng”*) khớp với cả hai hàng S và H, không cần sửa.

## 8. Việc người dùng phải tự làm hoặc tự quyết

1. Chạy Kaggle (mục 5) và tải kết quả về. Trợ lý không chạy được Kaggle.
2. Giữ hay đổi phép so chính **trước khi có số**. File này chọn `A2_500 - ck500`. Muốn dùng `A2_1000` thì phải đổi ngay bây giờ, không đổi sau khi đã thấy số.
3. Nếu ra hàng C, quyết có đổi phương pháp đề xuất sang thưởng CIDEr-D không. Đổi thì kéo theo:
   - chấm bước không chạm cho `A2_500`: dùng runbook `harness/runbook/kaggle_ctg_test_nontap.md`, thay `A3_1000/A2_1000` bằng `A2_500`, khoảng 2 giờ T4;
   - làm lại RAF (`298_ACTION_CHOT_RAF_7_10.md`), vì RAF chọn giữa S1 và ck500;
   - sửa ch1, ch4 (`sec:grpospicethietke`), ch6 (`sec:grpospice`, `tab:chinh`, `tab:grpospice`, hai bảng nhiều thước sinh tự động, hình bước không chạm), ch7, tóm tắt VI/EN, slide;
   - ghi trong luận văn rằng phương pháp được chọn sau khi xem tập kiểm, giữa hai ứng viên. Khuyến nghị: chỉ đổi khi ra hàng C và Δ ≥ khoảng 1 điểm. Nếu Δ nhỏ hơn thì giữ ck500, báo A2 hơn nhẹ.
4. Dán đoạn luận văn ở mục 7 và commit. Trợ lý không chạy git.
5. Có thêm cột BERTScore cho A2 hay không (cờ `--bert`, chỉ chạy được trên WSL).

## 9. Đã kiểm gì, chưa kiểm gì (7/10)

Đã chạy khô script đọc trên Mac (`--gia`: câu ck500 giả làm A2_500, câu S1 giả làm A2_1000), chạy thẳng từ khối mã ở Phụ lục A, khoảng 1,5 phút. Các dòng chính in ra:

```text
[tự kiểm] ck500 - S1 exec +1.55 [+0.80; +2.33] · công bố +1,55 [+0,80; +2,33]
[tự kiểm] S1/101   exec 59.11 [57.33; 60.83] · json [57.33; 60.83] · câu lệch tệp dự đoán 0 · rỗng 1 · G 1091
[tự kiểm] ck500    exec 60.65 [58.90; 62.38] · json [58.90; 62.38] · câu lệch tệp dự đoán 0 · rỗng 1 · G 1091
✅ tự kiểm đạt
| A2_500 - ck500 | Executability | +0.00 | [+0.00; +0.00] | 0 / 0 | 1 |
| A2_500 - S1/101 | Executability | +1.55 | [+0.80; +2.33] | 159 / 90 | 1.6e-05 |
[phân rã A2_1000 - ck500] cứu 90 (ck500 sai loại thao tác 8) · phá 159 (A2_1000 sai loại thao tác 36) · ròng từ loại thao tác -28 · ròng từ đổi phần tử -41
[luật 299 §4] A2_500 - ck500 exec +0.00 [+0.00; +0.00] → hàng H
```

Sáu thước vị trí của S1 và ck500 ra đúng bảng 3a. Cứu/phá 159/90 và phân rã +28/+41 (lấy ngược dấu ở dòng A2_1000 giả) khớp `report/259`.

Chưa kiểm:

- Phần `--chu` chưa chạy được trên Mac (không có Java, không có `pycocoevalcap`). Mã chép từ `harness/ck500_text_metrics.py` và `harness/grpo_spice_test_doc.py`, hai tệp đã sinh số chữ 45,79 và 430,05 của ck500. Script tự dừng nếu S1 hoặc ck500 không tái lập số đã lưu.
- Sáu ô Kaggle mới chỉ qua kiểm cú pháp, chưa chạy. Ô 1, Ô 3 và Ô 6 chép từ hai runbook đã chạy được (`kaggle_grpo_spice_test_ck500.md` 2/10, `kaggle_ctg_test_nontap.md` 6/10). Phần mới là hai chuỗi sinh rồi chấm chạy song song, mốc dừng 11,2 giờ, và bước kiểm tái lập ck500. Lượt chạy thử `TEST = True` ở mục 5.2 là để bắt lỗi ở những phần này trước khi commit.

## Phụ lục A — `doc_299.py` (nguyên văn)

```python
# -*- coding: utf-8 -*-
"""299 - đọc kết quả chấm TEST bước chạm của A2 (GRPO thưởng CIDEr-D) so với ck500 (GRPO thưởng SPICE) và S1/101.

0 GPU. Thước vị trí chạy được trên Mac (_scripts/_venv) lẫn WSL. Thước chữ (--chu) cần pycocoevalcap + Java 8.
  python doc_299.py --kho <thesis-master> --a2 <thư mục kết quả Kaggle>          # thước vị trí
  python doc_299.py --kho <thesis-master> --a2 <thư mục kết quả Kaggle> --chu    # thêm thước chữ
  python doc_299.py --kho <thesis-master> --gia                                  # chạy khô: ck500 giả làm A2_500, S1 giả làm A2_1000
Tự kiểm trước khi in số A2 (lệch là dừng): S1 và ck500 ra đúng sáu số vị trí đã công bố; ck500 - S1 exec ra
+1,55 [+0,80; +2,33]; KTC exec từng nhánh khớp tệp json của Kaggle; câu trong tệp thô trùng tệp dự đoán.
"""
import argparse, glob, json, os, sys

ap = argparse.ArgumentParser()
ap.add_argument("--kho", default=None, help="thư mục kho thesis-master (có harness/ và runs/)")
ap.add_argument("--a2", default=None, help="thư mục chứa tệp Kaggle của lượt 299 (đã giải nén)")
ap.add_argument("--chu", action="store_true", help="tính thêm thước chữ (cần pycocoevalcap + Java 8)")
ap.add_argument("--bert", action="store_true", help="cùng --chu: thêm BERTScore (chậm)")
ap.add_argument("--gia", action="store_true", help="chạy khô bằng tệp đã có")
a = ap.parse_args()

KHO = a.kho or next((p for p in ("thesis-master", ".", "..") if os.path.isdir(os.path.join(p, "harness"))), None)
assert KHO and os.path.isdir(os.path.join(KHO, "harness")), "🔴 không thấy kho: truyền --kho <thư mục có harness/ và runs/>"
KHO = os.path.abspath(KHO)
RUNS = os.path.join(KHO, "runs")
sys.path.insert(0, os.path.join(KHO, "harness"))
J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
if J and "JAVA_HOME" not in os.environ:
    os.environ["JAVA_HOME"] = J[-1]
    os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]

import luat_d3 as L
from d3_ktc import ktc, mcnemar                    # đúng hàm bootstrap cụm app đã sinh mọi KTC trong luận văn
from luat_aitw_day_du import aitw_full
from luat_aitw_moi_hop import aitw_moi_hop

GOC = {"S1/101": ("score_s1_seed101_raw.jsonl", "score_s1_seed101.json", "preds_s1_seed101.jsonl"),
       "ck500": ("grpo_spice/score_ck500_test_raw.jsonl", "grpo_spice/score_ck500_test.json",
                 "grpo_spice/pred_ck500_test.jsonl")}
TEP = {t: tuple(os.path.join(RUNS, x) for x in v) for t, v in GOC.items()}
A2 = None
if a.gia:
    TEP["A2_500"], TEP["A2_1000"] = TEP["ck500"], TEP["S1/101"]
else:
    A2 = os.path.abspath(a.a2 or os.path.join(os.path.dirname(KHO), "_kaggle_out", "299"))
    for t in ("A2_500", "A2_1000"):
        TEP[t] = (f"{A2}/score_{t}_test_raw.jsonl", f"{A2}/score_{t}_test.json", f"{A2}/pred_{t}_test.jsonl")
    thieu = [p for t in ("A2_500", "A2_1000") for p in TEP[t] if not os.path.exists(p)]
    assert not thieu, f"🔴 thiếu tệp Kaggle: {thieu}"

NH = ["S1/101", "ck500", "A2_500", "A2_1000"]
MOC = {"S1/101": dict(vor=59.11, d3=65.49, aitwf=74.37, moi=81.04, d14_truc=67.24, aok=94.35),
       "ck500": dict(vor=60.65, d3=67.02, aitwf=76.25, moi=82.90, d14_truc=68.90, aok=95.97)}
COT = [("vor", "Executability"), ("d3", "Hộp phần tử (D.3)"), ("aitwf", "AitW"), ("moi", "AitW cận trên"),
       ("d14_truc", "+14% theo trục"), ("aok", "Đúng loại thao tác")]
SO = [("A2_500", "ck500"), ("A2_1000", "ck500"), ("A2_500", "S1/101"), ("A2_1000", "S1/101"),
      ("A2_1000", "A2_500"), ("ck500", "S1/101")]

def nap(t):
    R = L.nap(TEP[t][0])
    return {k: dict(L.luat(r, k), aitwf=aitw_full(r, k), moi=aitw_moi_hop(r, k), aok=int(bool(r.get("action_ok"))),
                    sent=(r.get("sent") or "").strip(), gold=(r.get("gold_instruction") or "").strip(),
                    cum=r.get("app") or f"ep{r['episode_id']}") for k, r in R.items()}

X = {t: nap(t) for t in NH}
K = list(X["S1/101"])                         # thứ tự dòng tệp thô S1: tái lập đúng mọi KTC ghép cặp đã công bố
cum = {k: X["S1/101"][k]["cum"] for k in K}
pct = lambda t, c: 100 * sum(X[t][k][c] for k in K) / len(K)
loi = []
assert len(K) == 4463, len(K)
for t in NH:
    if len(X[t]) != 4463 or set(X[t]) != set(K):
        loi.append(f"{t}: quần thể khác 4.463 bước chung")

# — tự kiểm —
for t, m in MOC.items():
    for c, ten in COT:
        if abs(pct(t, c) - m[c]) > 0.006:
            loi.append(f"{t} {ten} {pct(t, c):.2f} ≠ công bố {m[c]}")
d, lo, hi, _ = ktc(K, lambda k, c: X["ck500"][k][c] - X["S1/101"][k][c], "vor", cum)
print(f"[tự kiểm] ck500 - S1 exec {d:+.2f} [{lo:+.2f}; {hi:+.2f}] · công bố +1,55 [+0,80; +2,33]")
if abs(d - 1.55) > 0.006 or abs(lo - 0.80) > 0.006 or abs(hi - 2.33) > 0.006:
    loi.append("ck500 - S1 exec không ra +1,55 [+0,80; +2,33]")
for t in NH:
    raw, js, pred = TEP[t]
    p, lo, hi, g = ktc(list(X[t]), lambda k, c: X[t][k][c], "vor", cum)
    ci = json.load(open(js, encoding="utf-8"))["ci_voronoi"]
    P = {(str(o["episode_id"]), str(o["step_id"])): (o.get("pred") or "").strip()
         for o in map(json.loads, open(pred, encoding="utf-8"))}
    lech = sum(P.get(k) != X[t][k]["sent"] for k in K)
    print(f"[tự kiểm] {t:8s} exec {p:.2f} [{lo:.2f}; {hi:.2f}] · json [{100*ci[0]:.2f}; {100*ci[1]:.2f}] · "
          f"câu lệch tệp dự đoán {lech} · rỗng {sum(not X[t][k]['sent'] for k in K)} · G {g}")
    if abs(lo - 100 * ci[0]) > 0.006 or abs(hi - 100 * ci[1]) > 0.006:
        loi.append(f"{t}: KTC exec lệch {os.path.basename(js)}")
    if lech:
        loi.append(f"{t}: {lech} câu trong tệp thô khác tệp dự đoán")
if loi:
    sys.exit("🔴 DỪNG, đường đọc sai — KHÔNG đọc số A2: " + " · ".join(loi))
print("✅ tự kiểm đạt\n")

# — điểm —
out = {"diem": {}, "so": {}, "phan_ra": {}, "mo_ta": {}}
print("## Điểm trên 4.463 bước chạm\n")
print("| thước | " + " | ".join(NH) + " |")
print("|---|" + "---:|" * len(NH))
for c, ten in COT:
    out["diem"][ten] = {t: round(pct(t, c), 2) for t in NH}
    print(f"| {ten} | " + " | ".join(f"{pct(t, c):.2f}" for t in NH) + " |")
for t in NH:
    out["mo_ta"][t] = dict(so_tu_tb=round(sum(len(X[t][k]["sent"].split()) for k in K) / len(K), 2),
                            trung_ck500=sum(X[t][k]["sent"] == X["ck500"][k]["sent"] for k in K),
                            trung_S1=sum(X[t][k]["sent"] == X["S1/101"][k]["sent"] for k in K),
                            rong=sum(not X[t][k]["sent"] for k in K))
for m, ten in (("so_tu_tb", "số từ TB"), ("trung_ck500", "câu trùng ck500"), ("trung_S1", "câu trùng S1"), ("rong", "câu rỗng")):
    print(f"| {ten} | " + " | ".join(str(out["mo_ta"][t][m]) for t in NH) + " |")

# — so ghép cặp —
print("\n## So ghép cặp (KTC95 bootstrap cụm app, B = 10.000 · cứu = nhánh trái đúng mà nhánh phải sai, phá = ngược lại)\n")
print("| phép so | thước | Δ | KTC95 | cứu / phá | p McNemar |")
print("|---|---|---:|---|---:|---:|")
for x, y in SO:
    o = out["so"][f"{x} - {y}"] = {}
    for c, ten in COT:
        d, lo, hi, _ = ktc(K, lambda k, cc: X[x][k][cc] - X[y][k][cc], c, cum)
        b, cu, _, p = mcnemar(K, X[y], X[x], c)
        o[ten] = dict(delta=round(d, 2), lo=round(lo, 2), hi=round(hi, 2), cuu=cu, pha=b, p=p)
        print(f"| {x} - {y} | {ten} | {d:+.2f} | [{lo:+.2f}; {hi:+.2f}] | {cu} / {b} | {p:.2g} |")

# — phân rã cứu/phá so với ck500 theo loại thao tác —
print()
for x in ("A2_500", "A2_1000"):
    y = "ck500"
    cuu = [k for k in K if X[y][k]["vor"] == 0 and X[x][k]["vor"] == 1]
    pha = [k for k in K if X[y][k]["vor"] == 1 and X[x][k]["vor"] == 0]
    cuu_aok = sum(X[y][k]["aok"] == 0 for k in cuu)
    pha_aok = sum(X[x][k]["aok"] == 0 for k in pha)
    r_aok, r_dv = cuu_aok - pha_aok, (len(cuu) - cuu_aok) - (len(pha) - pha_aok)
    out["phan_ra"][f"{x} - {y}"] = dict(cuu=len(cuu), pha=len(pha), cuu_aok=cuu_aok, pha_aok=pha_aok,
                                            rong_aok=r_aok, rong_dinh_vi=r_dv)
    print(f"[phân rã {x} - ck500] cứu {len(cuu)} (ck500 sai loại thao tác {cuu_aok}) · phá {len(pha)} "
          f"({x} sai loại thao tác {pha_aok}) · ròng từ loại thao tác {r_aok:+d} · ròng từ đổi phần tử {r_dv:+d}")

# — luật 299 §4 (chốt trước khi có số) —
e = out["so"]["A2_500 - ck500"]["Executability"]
hang = "C" if e["lo"] > 0 else ("S" if e["hi"] < 0 else "H")
TXT = {"S": "cận trên < 0 → giữ ck500; ghi: ở cùng 500 bước, thưởng SPICE hơn thưởng CIDEr-D.",
       "H": "KTC chứa 0 → giữ ck500; A2_500 vào luận văn như phép so phần thưởng; câu đóng góp: thưởng bằng một thước so câu.",
       "C": "cận dưới > 0 → A2_500 hơn ck500 có ý nghĩa; DỪNG, người dùng quyết theo mục 8 (đổi phương pháp kéo theo nhiều việc)."}
out["hang"] = hang
print(f"\n[luật 299 §4] A2_500 - ck500 exec {e['delta']:+.2f} [{e['lo']:+.2f}; {e['hi']:+.2f}] → hàng {hang}: {TXT[hang]}")
print("  A2_1000 chỉ đọc thêm, không đổi hàng.")

# — thước chữ (WSL, cần Java 8) —
if a.chu:
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    from pycocoevalcap.bleu.bleu import Bleu
    from pycocoevalcap.meteor.meteor import Meteor
    from pycocoevalcap.rouge.rouge import Rouge
    from pycocoevalcap.cider.cider import Cider
    from pycocoevalcap.spice.spice import Spice
    import text_metrics_them as TM
    REF = json.load(open(os.path.join(RUNS, "grpo_spice", "text_metrics_ck500.json"), encoding="utf-8"))
    CH = ["bleu4", "meteor15", "rougeL", "cider_d", "spice", "chrf"] + (["bertscore_f1_rescaled"] if a.bert else [])
    chu = {}
    print("\n[thước chữ] chạy Java, vài phút mỗi nhánh ...", flush=True)
    for t in NH:
        hyp, ref = [X[t][k]["sent"] for k in K], [X[t][k]["gold"] for k in K]
        tk = PTBTokenizer()
        g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(ref)})
        c = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(hyp)})
        b, _ = Bleu(4).compute_score(g, c, verbose=0)
        sp, ds = Spice().compute_score(g, c)
        o = dict(bleu4=round(100 * b[3], 2), meteor15=round(100 * Meteor().compute_score(g, c)[0], 2),
                 rougeL=round(100 * Rouge().compute_score(g, c)[0], 2),
                 cider_d=round(100 * Cider().compute_score(g, c)[0], 2), spice=round(100 * sp, 2))
        tm = TM.tinh(hyp, ref, bert=a.bert)
        o["chrf"] = tm["chrf"]
        if a.bert:
            o["bertscore_f1_rescaled"] = tm["bertscore_f1_rescaled"]
        for k, dd in zip(K, ds):
            f = dd["All"]["f"]
            X[t][k]["spice"] = 0.0 if f is None or f != f else float(f)
        chu[t] = o
        print(f"  {t:8s} " + " · ".join(f"{m} {o[m]}" for m in CH), flush=True)
        if t in REF:
            for m in CH:
                if m in REF[t] and abs(o[m] - REF[t][m]) > 0.025:
                    loi.append(f"{t} {m} {o[m]} ≠ đã lưu {REF[t][m]}")
    if loi:
        sys.exit("🔴 DỪNG, thước chữ không tái lập S1/ck500 — KHÔNG dùng số chữ của A2: " + " · ".join(loi))
    print("✅ S1 và ck500 tái lập số chữ đã lưu (±0,025)\n")
    out["chu"] = chu
    print("| thước | " + " | ".join(NH) + " | A2_500 - ck500 | A2_1000 - ck500 |")
    print("|---|" + "---:|" * (len(NH) + 2))
    for m in CH:
        print(f"| {m} | " + " | ".join(f"{chu[t][m]:.2f}" for t in NH)
              + f" | {chu['A2_500'][m] - chu['ck500'][m]:+.2f} | {chu['A2_1000'][m] - chu['ck500'][m]:+.2f} |")
    out["so_spice"] = {}
    for x, y in SO:
        d, lo, hi, _ = ktc(K, lambda k, cc: X[x][k][cc] - X[y][k][cc], "spice", cum)
        out["so_spice"][f"{x} - {y}"] = dict(delta=round(d, 2), lo=round(lo, 2), hi=round(hi, 2))
        print(f"  ΔSPICE {x} - {y}: {d:+.2f} [{lo:+.2f}; {hi:+.2f}]")

if A2:
    p = os.path.join(A2, "doc_299.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n→", p)
```
