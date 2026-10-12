# 312 — ACTION: RA-GRPO trên Kaggle — tranh luận + cách chạy (12/10/2026)

File tự chứa, đọc từ đầu tới cuối là chạy được. **File này thay toàn bộ phần action của `311_DE_XUAT_RA_GRPO_VA_ACTION_12_10.md`**: cùng thiết kế, nhưng thêm thăm dò bộ nhớ trước khi train, bộ đếm chép trong lúc train, và script khoảng tin cậy thước chữ. `ra_grpo.py` đã đổi so bản trong 311, nên dùng md5 ở mục 3.

Mã nguồn nguyên văn ở Phụ lục A–E; bản trên đĩa ở `/Users/P836901/Documents/Self-learning/thesis/_scripts/311/`. Chưa chạy GPU nào, chưa commit gì.

## 0. RA-GRPO là gì (một đoạn)

Chạy lại đúng công thức ck500:

- cùng `grpo_spice.py` (md5 `07ea87b6d156d1faa391a4274dffd7cf`, trùng bản đã train ck500);
- cùng 1.000 câu nhắc train, hạt 101, G = 8, lô 16 câu sinh mỗi bước (2 câu nhắc × 8), β 0,04, lr 1e-5, 500 bước, thưởng SPICE − 0,02 × phạt câu dài;
- cùng S1 hoà làm điểm xuất phát và làm mốc KL.

**Chỉ khác một biến:** câu nhắc có thêm khối tối đa 4 câu hướng dẫn của các bước tương tự lấy từ kho train. Đó đúng là khối của lượt 304: truy hồi theo mục tiêu và câu 8 bước trước, bỏ mọi tác vụ val và chính tác vụ đang xét, chèn ngay trước dòng “Viết câu hướng dẫn cho bước tiếp theo.”. Lúc chạy, val và tập kiểm dùng khối `ex_val_k4.jsonl` / `ex_test_k4.jsonl` có sẵn.

## 1. Tranh luận

### 1.1 Có làm tăng đa số thước chữ không

**Ủng hộ:**

- Khối câu mẫu có thông tin thật cho thước chữ: R3 (hậu xử lý) 7/7 với khoảng tin cậy loại 0 (BLEU-4 +1,12 [+0,78; +1,45], CIDEr-D +12,04 [+8,72; +15,65]); `ra_k4` 5/7 trên tập kiểm.
- Trên tập kiểm, khối chứa đúng nguyên văn câu chuẩn ở 15,8% bước. Ở 9,8% bước khối có câu chuẩn mà ck500 đang sai. Trần nếu chép đúng mọi chỗ đó: BLEU-4 +5,1, CIDEr-D +65,8.
- GRPO chấm từng câu sinh ra. Câu chép đúng câu mẫu trùng câu chuẩn được SPICE = 1; câu viết lại kém bị advantage âm. Đây đúng là thứ SFT ở `ra_k4` / CW-RA thiếu.

**Phản biện:**

- (a) S1 chưa từng thấy khối, có thể bỏ qua nó. Khi đó nhóm 8 mẫu không có mẫu chép đúng, RL không có gì để thưởng. → Cổng G0 đo trước.
- (b) Khối làm câu nhắc dài hơn, thêm nhiễu. EXTRA (EACL 2023) ghi nhận 1–3 câu truy hồi còn kém hơn không truy hồi, phải đủ nhiều câu mới có lợi. → k = 4 là mức SmallCap chọn; G0 đo greedy S1 có khối so với không khối.
- (c) Mọi lượt tối ưu tiếp sau ck500 đều xuống. → RA-GRPO không tối ưu tiếp từ ck500; nó chạy song song với ck500 từ S1.
- (d) Một hạt giống, chênh dự kiến cỡ 1 điểm thước chữ. → Báo khoảng tin cậy bootstrap (`ktc_chu.py`).

**Phán:** cổng G0 đạt ~55–65%. Nếu đạt và train xong, ≥ 4/7 thước chữ hơn ck500 ~50–55%. Gộp ~30–35%. Lấy được phần lợi cỡ R3 là kịch bản tốt; mất cổng thì chỉ tốn ~1,2 h.

### 1.2 Có dễ bảo vệ nếu ra số tốt không

**Ủng hộ:**

- Phép so với ck500 khác đúng một biến, nên phần tăng quy được cho truy hồi.
- Không có luật ghép tay, thẻ hay ngưỡng chọn trên val, nên không bị hỏi “chỉnh theo số”.
- Tiền lệ có bình duyệt cho từng phần:
  - đưa câu truy hồi vào rồi tối ưu RL bằng thước câu cho sinh câu từ ảnh: EXTRA (EACL 2023), Sarto và cs. (ACM TOMM 2024), M-RAT (ACCV 2024). Ở các bài này truy hồi là đóng góp chính, RL bằng thước câu là bước huấn luyện tiêu chuẩn;
  - chèn ví dụ truy hồi từ dữ liệu train vào câu nhắc trong lúc GRPO: XRPO (ICML 2026);
  - RL khi đầu vào chính sách chứa nội dung truy hồi: Search-R1 (COLM 2025), Smart-Searcher (Findings EMNLP 2025);
  - đưa câu truy hồi vào câu nhắc dạng chữ: SmallCap (CVPR 2023);
  - GRPO trên Qwen2.5-VL-3B cho GUI di động: UI-R1 (AAAI 2026).

**Phản biện và trả lời:**

1. *“Lúc chạy dùng thêm dữ liệu train, không công bằng với ck500.”* Kho là chính dữ liệu train mô hình đã học; không thêm dữ liệu ngoài. Truy hồi là một phần của phương pháp, như kNN-MT (ICLR 2021) hay SmallCap. Tác vụ tập kiểm chung kho = 0.
2. *“Chép câu train để ăn điểm n-gram.”* Câu chép trùng câu chuẩn là câu đúng. Rủi ro thật là RL học chép câu mẫu gần đúng vì SPICE cho điểm một phần (câu mẫu của tác vụ tương tự có nhiều từ chung). Chuyện này có thể nâng thước chữ mà làm exec giảm. → `ra_grpo.py` in `[chép] x/16 câu trùng câu mẫu - trong đó trùng câu chuẩn y` mỗi bước; lúc chấm báo tỉ lệ chép và tỉ lệ chép đúng; đo exec.
3. *“Ch5 nói thước so khớp chữ không đọc được ở vùng chênh < 2 điểm.”* Cần 7/7 cùng chiều, khoảng tin cậy loại 0, exec không giảm, và sửa câu ch5 (xem 308 §11.3). RA-GRPO lợi thế hơn CW-RA vì thưởng SPICE, thước luận văn đã dẫn Zhao để biện minh.
4. *“Sao không dùng CLIP / thêm kiến trúc như các bài mô tả ảnh?”* Mô hình nền đã nhìn ảnh và đọc câu nhắc dài, nên chèn chữ đủ (như SmallCap, Search-R1, XRPO). Thêm kiến trúc làm mất phép so một biến. CLIP ở 224 px không đọc được chữ trên màn hình, luận văn đã nêu khi loại CLIPScore. Truy hồi theo ảnh để làm hướng phát triển.

**Phán:** dễ bảo vệ ở mức “thành phần truy hồi đưa vào mô hình, tối ưu bằng công thức có sẵn, so một biến với ck500”, nếu có số exec không giảm và sửa câu ch5. Không viết “đầu tiên”.

### 1.3 Có đóng góp nhiều hơn ck500 không

Có, nếu thắng. RA-GRPO chứa trọn công thức ck500 cộng thêm truy hồi. Mô hình chính đổi từ ck500 sang RA-GRPO, còn ck500 thành dòng “bỏ truy hồi” trong bảng tách thành phần. Khác CW-RA (thành phần thứ hai chồng lên ck500, chỉ nâng thước chữ), ở đây phần tăng của truy hồi được đo trên cùng công thức, và exec có cơ hội lên theo vì phần thưởng vẫn là SPICE như ck500.

### 1.4 Rủi ro kỹ thuật và cách chặn

| rủi ro | chặn bằng |
|---|---|
| S1 bỏ qua khối, RL không có tín hiệu | cổng G0 (mục 5): trần best-of-8 có khối so với không khối |
| tràn VRAM giữa lượt (ck500 đã 13,22 GiB trên T4; câu nhắc dài thêm ~10–15%) | Ô T-3a thăm dò 20 bước trên 50 câu nhắc dài nhất; tràn hoặc > 14,3 GiB thì tự lùi về `--bs 2 --accum 8 --gen-chunk 8`. Cùng 16 câu sinh mỗi bước; đổi micro-batch không đổi phép train (đã kiểm CPU & lượt CTG, report 279) |
| chạy tiếp nạp nhầm adapter (lỗi 30/9) | `grpo_spice.py` đã vá; log phải có `[nạp default] … + x > 0` |
| máy cấp 1 GPU, treo cả đêm (G2 lượt 310) | `assert torch.cuda.device_count() == 2` ở đầu mọi notebook |
| RL học chép bừa | dòng `[chép]` trong log; tỉ lệ chép đúng lúc chấm; exec |
| val và test ngược chiều | không chọn gì trên val; chấm đúng bước 500 như ck500 |
| phần vá `trl.GRPOTrainer` không ăn với trl 0.29.1 | log phải in `[RA] câu nhắc đã dựng …` ngay sau khi trainer dựng; không có thì dừng |

## 2. Tổng quan lượt chạy

| notebook | việc | máy | thời gian | điều kiện |
|---|---|---|---:|---|
| G0 | cổng: greedy + 8 mẫu S1 có/không khối trên val | T4 ×2 | ~1,2 h | luôn chạy trước |
| T1 | thăm dò bộ nhớ + train bước 0 → ~180 | T4 (1 GPU dùng) | ~10,8 h | chỉ khi G0 ĐẠT |
| T2 | train tiếp → ~380 | T4 | ~10,8 h | |
| T3 | train tiếp → 500 | T4 | ~6–7 h | |
| E | sinh val (bước 250, 500) + tập kiểm (500), chấm 7 thước, exec | T4 ×2 | ~5–6 h | |
| máy nhà | đọc exec, khoảng tin cậy | CPU | ~2 phút | |

Tổng ~45 h T4 nếu đi hết, 0 đồng. Hai tài khoản chia hạn mức 30 h/tuần mỗi tài khoản. Ước số bước mỗi lần T dựa trên 160 s/bước của ck500 × ~1,15. Lần T1 mất thêm ~1 h thăm dò và ~10 phút dựng khối.

Notebook sau cần thấy output notebook trước. Cùng tài khoản thì thêm “Notebook output” làm input. Khác tài khoản thì từ output → New Dataset, đặt công khai, rồi thêm dataset đó.

## 3. Chuẩn bị

### 3.1 Dataset mới `ra-grpo-312`

| tệp | lấy từ | md5 |
|---|---|---|
| `ra_grpo.py` | `thesis/_scripts/311/` | `7e62b2ce13100cfcac9db675864ddfab` |
| `ra_grpo_g0.py` | `thesis/_scripts/311/` | `ff0642965f672dc955f0bdd512c8a4f5` |
| `ra_grpo_g0_doc.py` | `thesis/_scripts/311/` | `3fcfed412f1e2c422093ad022370d0e7` |
| `pred_S1_vallon.jsonl` | `thesis-master/runs/vallon289/` | (câu greedy S1 hoà trên 1.002 click val, lượt 289) |

`ktc_chu.py` (`838a75868dd148f499a0415dd79249e0`) và `doc_exec_cw.py` (`94e0901a63fa6f28481aadeaed0e0d50`) chạy ở máy nhà, không cần tải lên.

### 3.2 Input dùng lại

| dataset | dùng ở | chứa |
|---|---|---|
| `trangphngngc/ra-sft-script` | mọi notebook | `grpo_spice.py` (`07ea87b6…`), `build_branch_data.py` (`619e63e1…`), `ra_exemplars.py`, `ra_gen.py`, `ra_score.py`, `train_tru_val.jsonl` (`edbb231a…`), `ex_val_k4.jsonl`, `ex_test_k4.jsonl`, `pred_ck500_vallon.jsonl`, `pred_ck500_test.jsonl` |
| `trangphngngc/fgrb-p1-bundle` | mọi notebook | `adapter_s1_seed101`, `p1_train_rows.jsonl`, `p1_val_rows.jsonl`, `ocr.jsonl`, `images/` |
| `uyenle0712/thesis-score` | E | ảnh tập kiểm + `harness/score_run.py` |
| `ra-grpo-312` | mọi notebook | 4 tệp ở 3.1 |

Đã kiểm trên máy: `pred_S1_vallon.jsonl`, `ex_val_k4.jsonl`, `pred_ck500_vallon.jsonl` cùng đúng 1.002 khoá. `pred_ck500_test.jsonl` trùng từng byte câu `sent` của tập chấm thô ck500 (4.463/4.463).

## 4. Hai ô chung của mọi notebook

Accelerator GPU T4 ×2, Internet bật.

```python
# Ô 0-1: gói (trl 0.29.1 - transformers 5.18.0 - peft 0.21.1, gỡ torchao — cùng bộ đã chạy lượt 299/304) + Java cho SPICE
import subprocess, sys, os, time, glob, json, shutil, re
T0 = time.time()
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True); print((r.stdout + r.stderr)[-1500:], flush=True); return r.returncode
sh("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless")
sh("update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java; java -version")
sh(f"{sys.executable} -m pip install -q 'transformers==5.18.0' 'peft==0.21.1' 'trl==0.29.1' accelerate bitsandbytes pycocoevalcap sacrebleu")
sh(f"{sys.executable} -m pip uninstall -y torchao")
sh(f'{sys.executable} -c "import torch, transformers, peft, trl; print(transformers.__version__, peft.__version__, trl.__version__, torch.cuda.device_count())"')
import torch
assert torch.cuda.device_count() == 2, "⛔ cần T4 x2 - đổi Accelerator rồi chạy lại"
```

```python
# Ô 0-2: đường dẫn, chép mã, hoà S1, hàm chạy nền
W = "/kaggle/working"; RA = f"{W}/ra"; M = f"{W}/s1_merged"
def tim(duoi):
    for sau in range(1, 6):
        g = glob.glob("/kaggle/input/" + "*/" * sau + duoi)
        if g: return g[0]
    raise FileNotFoundError(duoi)

SRC = os.path.dirname(tim("ra_gen.py")); D312 = os.path.dirname(tim("ra_grpo_g0.py"))
BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "images" in d)
shutil.copytree(SRC, RA, dirs_exist_ok=True)
for f in os.listdir(D312): shutil.copy(f"{D312}/{f}", RA)
print("SRC", SRC, "\nD312", D312, "\nBUNDLE", BUNDLE)
r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", M], cwd=RA, capture_output=True, text=True)
print((r.stdout + r.stderr)[-1500:]); assert r.returncode == 0
V = dict(recs=f"{BUNDLE}/p1_val_rows.jsonl", ocr=f"{BUNDLE}/ocr.jsonl", img=f"{BUNDLE}/images", ex=f"{SRC}/ex_val_k4.jsonl")
ENV = {**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1",
       "PYTORCH_ALLOC_CONF": "expandable_segments:True", "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
def chay(script, args, log, gpu):
    return subprocess.Popen(["python", f"{RA}/{script}", *args], stdout=open(log, "w"), stderr=subprocess.STDOUT,
                            env={**ENV, "CUDA_VISIBLE_DEVICES": str(gpu)}, cwd=RA, start_new_session=True)
def doi(ps, logs):
    while any(p.poll() is None for p in ps):
        time.sleep(120); print(time.strftime("%H:%M"), f"{(time.time()-T0)/3600:.2f} h", [open(l).read().splitlines()[-1:] for l in logs], flush=True)
    assert all(p.returncode == 0 for p in ps), [open(l).read()[-2000:] for l in logs]
def py(*a):
    r = subprocess.run(["python", *a], capture_output=True, text=True, cwd=RA); print(r.stdout[-5000:], r.stderr[-2000:]); assert r.returncode == 0
```

## 5. Notebook G0 — cổng (~1,2 h)

```python
# Ô G-1: sinh — greedy có khối (2 GPU), rồi 8 mẫu có khối (GPU0) song song không khối (GPU1) trên cùng 300 bước val
def lenh(mode, out, shard="0/1", khoi=True):
    a = ["--mode", mode, "--merged", M, "--recs", V["recs"], "--ocr", V["ocr"], "--images", V["img"], "--out", f"{W}/{out}", "--shard", shard]
    return a + (["--ra", V["ex"]] if khoi else [])

ps = [chay("ra_grpo_g0.py", lenh("greedy", f"g0_greedy_ra_{i}.jsonl", f"{i}/2"), f"{W}/g0_greedy_{i}.log", i) for i in (0, 1)]
doi(ps, [f"{W}/g0_greedy_{i}.log" for i in (0, 1)])
ps = [chay("ra_grpo_g0.py", lenh("mau", "g0_mau_ra.jsonl"), f"{W}/g0_mau_ra.log", 0),
      chay("ra_grpo_g0.py", lenh("mau", "g0_mau_khong.jsonl", khoi=False), f"{W}/g0_mau_khong.log", 1)]
doi(ps, [f"{W}/g0_mau_ra.log", f"{W}/g0_mau_khong.log"])
with open(f"{W}/g0_greedy_ra.jsonl", "w") as f:
    for i in (0, 1): f.write(open(f"{W}/g0_greedy_ra_{i}.jsonl").read())
print({p: sum(1 for _ in open(f"{W}/{p}")) for p in ("g0_greedy_ra.jsonl", "g0_mau_ra.jsonl", "g0_mau_khong.jsonl")})

# Ô G-2: chấm greedy và đọc cổng
S1V = tim("pred_S1_vallon.jsonl")
py(f"{RA}/ra_score.py", "--recs", V["recs"], "--pred", f"S1={S1V}", "--pred", f"S1_ra={W}/g0_greedy_ra.jsonl",
   "--pred", f"ck500={SRC}/pred_ck500_vallon.jsonl", "--base", "S1", "--ra", f"S1_ra={V['ex']}", "--no-bert", "--out", f"{W}/diem_g0_greedy.json")
py(f"{RA}/ra_grpo_g0_doc.py", "--recs", V["recs"], "--ra", V["ex"], "--mau-ra", f"{W}/g0_mau_ra.jsonl",
   "--mau-khong", f"{W}/g0_mau_khong.jsonl", "--diem-greedy", f"{W}/diem_g0_greedy.json", "--out", f"{W}/g0_ket_qua.json")
shutil.rmtree(M, ignore_errors=True); shutil.rmtree(RA, ignore_errors=True)
print(f"{(time.time()-T0)/3600:.2f} h")
```

Luật cổng (in sẵn trong `ra_grpo_g0_doc.py`):

| | điều kiện |
|---|---|
| G0-1 (trần) | best-of-8 có khối − không khối: SPICE ≥ +1,0 hoặc CIDEr-D ≥ +10 |
| G0-2 (mốc KL không hỏng) | greedy S1 có khối so không khối: CIDEr-D không thấp hơn quá 10 và SPICE không thấp hơn quá 1,0 |
| ĐẠT | chạy T1–T3 |
| G0-1 trượt, G0-2 đạt, S1 không chép được câu đúng | S1 bỏ qua khối → hỏi người dùng có làm Phương án B (RA-SFT từ S1 trước, ~8 h) không |
| còn lại | dừng RA-GRPO |

Gửi lại: dòng `→ CỔNG G0: …`, hai dòng **CÓ khối / KHÔNG khối**, bảng `ra_score` (S1, S1_ra, ck500).

## 6. Notebook T — train (3 lần, chỉ khi G0 ĐẠT)

Một notebook, commit ba lần. Lần 2 và 3 thêm output lần trước làm input. Ô 0-1, Ô 0-2 giữ nguyên.

```python
# Ô T-2: chép điểm lưu, đệm khối, cấu hình từ output lần trước (lần 1 không có gì)
OUT = f"{W}/ra_grpo"; os.makedirs(OUT, exist_ok=True)
for s in range(1, 6):
    for p in glob.glob("/kaggle/input/" + "*/" * s + "ra_grpo/checkpoint-*"):
        if os.path.isdir(p): shutil.copytree(p, f"{OUT}/{os.path.basename(p)}", dirs_exist_ok=True)
    for f in ("ra_cache.json", "cau_hinh.json"):
        for c in glob.glob("/kaggle/input/" + "*/" * s + f"ra_grpo/{f}"): shutil.copy(c, OUT)
print("trong OUT:", sorted(os.listdir(OUT))[-6:])

# Ô T-3a: (chỉ khi chưa có cau_hinh.json) thăm dò 20 bước trên 50 câu nhắc DÀI NHẤT — đo VRAM, s/bước; tràn thì lùi micro-batch
CH = f"{OUT}/cau_hinh.json"
CFG = (["--bs", "4", "--accum", "4"], ["--bs", "2", "--accum", "8", "--gen-chunk", "8"])
if not os.path.exists(CH):
    for cfg in CFG:
        shutil.rmtree(f"{W}/probe", ignore_errors=True)
        cmd = ["python", f"{RA}/ra_grpo.py", "--kho", f"{SRC}/train_tru_val.jsonl", "--gio", "3", "--",
               "--probe", "--no-q4", *cfg, "--bundle", BUNDLE, "--merged", M, "--out", f"{W}/probe"]
        r = subprocess.run(cmd, cwd=RA, stdout=open(f"{W}/probe_{cfg[1]}.log", "w"), stderr=subprocess.STDOUT,
                           env={**ENV, "CUDA_VISIBLE_DEVICES": "0"})
        L = open(f"{W}/probe_{cfg[1]}.log", errors="ignore").read()
        xong = [l for l in L.splitlines() if l.startswith("[xong]")]
        print(cfg, "mã thoát", r.returncode, xong[-1:] or L[-1500:], flush=True)
        print("\n".join(l for l in L.splitlines() if l.startswith(("[kho]", "[RA]", "[câu nhắc]", "[LoRA mới]", "[chép]")))[:3000])
        if r.returncode == 0 and xong:
            vram = float(re.search(r"đỉnh VRAM ([\d.]+)", xong[-1]).group(1)); spb = float(re.search(r"([\d.]+) s/bước", xong[-1]).group(1))
            if vram <= 14.3:
                json.dump(dict(cfg=cfg, vram=vram, s_buoc=spb), open(CH, "w")); break
    assert os.path.exists(CH), "⛔ cả hai cấu hình đều tràn hoặc lỗi — gửi probe_*.log cho chat"
    if os.path.exists(f"{W}/probe/ra_cache.json"): shutil.copy(f"{W}/probe/ra_cache.json", OUT)
    shutil.rmtree(f"{W}/probe", ignore_errors=True)
print("cấu hình:", json.load(open(CH)))
```

```python
# Ô T-3b: train — đúng lệnh train của ck500, bọc bởi ra_grpo.py, tự dừng êm trước 11 h
cfg = json.load(open(CH))["cfg"]
gio = 10.8 - (time.time() - T0) / 3600
cmd = ["python", f"{RA}/ra_grpo.py", "--kho", f"{SRC}/train_tru_val.jsonl", "--gio", f"{gio:.2f}", "--",
       "--train", "--no-q4", *cfg, "--bundle", BUNDLE, "--merged", M, "--out", OUT, "--resume", "auto"]
p = subprocess.Popen(cmd, cwd=RA, stdout=open(f"{W}/train.log", "a"), stderr=subprocess.STDOUT,
                     env={**ENV, "CUDA_VISIBLE_DEVICES": "0"}, start_new_session=True)
while p.poll() is None:
    time.sleep(300)
    L = open(f"{W}/train.log", errors="ignore").read().splitlines()
    sp = [l for l in L if l.startswith("[spice]")][-1:]; cp = [l for l in L if l.startswith("[chép]")][-20:]
    ck = sorted(glob.glob(f"{OUT}/checkpoint-*"), key=lambda s: int(s.rsplit("-", 1)[1]))
    chep = sum(int(re.search(r"(\d+)/", l).group(1)) for l in cp); dung = sum(int(re.search(r"chuẩn (\d+)", l).group(1)) for l in cp)
    print(f"{(time.time()-T0)/3600:.2f} h - lưu cuối {os.path.basename(ck[-1]) if ck else '-'} - "
          f"{sp[0][:110] if sp else (L[-1][:140] if L else '')} - chép 20 lần gần nhất {chep} (đúng {dung})", flush=True)
print("mã thoát", p.returncode)
print("\n".join(open(f"{W}/train.log", errors="ignore").read().splitlines()[-30:]))
for d in (M, RA): shutil.rmtree(d, ignore_errors=True)
```

Dòng cần thấy trong `train.log`:

| dòng | ý nghĩa |
|---|---|
| `[kho] 62880 bước - 12542 tác vụ - bỏ 346 tác vụ val` | kho đúng |
| `[câu nhắc] 1000 - bỏ {... 'rong': 9}` | cùng 1.000 câu nhắc như ck500 |
| `[RA] câu nhắc đã dựng 3991 - có khối ~3991` | phần chèn khối đã ăn (không có dòng này: dừng) |
| `[LoRA mới] tham số học 14,966,784 - S1 có 14,966,784` | cùng cỡ LoRA ck500 |
| lần 2, 3: `[tiếp từ] .../checkpoint-N` và `[nạp default] ... + x > 0` | chạy tiếp đúng adapter (thiếu hoặc x = 0: dừng) |
| `[dừng giờ] ... ở bước N` ở cuối lần 1, 2 | dừng êm, đã lưu điểm lưu |
| `[xong] ... final` ở lần 3 với bước 500 | xong |

Chỉ số theo dõi (cùng bảng runbook ck500):

| chỉ số | ổn | báo về |
|---|---|---|
| s/bước | 130–210 | > 240 |
| thưởng TB `[spice]` | 0,3–0,8, nhích dần qua hàng trăm bước | giảm đều > 100 bước |
| số từ TB | 5–12 | < 4 hoặc > 15 |
| rỗng | 0–2 | ≥ 5 |
| `[chép]` 20 lần gần nhất | tăng dần, phần lớn là chép đúng | chép tăng mà chép đúng không tăng (RL học chép bừa) |

## 7. Notebook E — chấm (~5–6 h)

Ô 0-1, Ô 0-2. Thêm input: output lần T có `ra_grpo/checkpoint-500`, output lần T có `checkpoint-250`, và `uyenle0712/thesis-score`.

```python
# Ô E-1: sinh có khối — val từ bước 250 và 500, tập kiểm từ bước 500 (2 GPU)
CK = {n: os.path.dirname(tim(f"ra_grpo/checkpoint-{n}/adapter_config.json")) for n in (250, 500)}
PKG = os.path.dirname(os.path.dirname(tim("harness/score_run.py"))); TEST = f"{PKG}/harness/dg1_cache/test_ac"
print(CK, PKG)
def sinh(ten, ck, recs, ocr, img, ex, expect):
    logs = [f"{W}/{ten}_{i}.log" for i in (0, 1)]
    ps = [chay("ra_gen.py", ["--merged", M, "--ckpt", ck, "--recs", recs, "--ocr", ocr, "--images", img,
                              *(["--ra", ex] if ex else []), "--expect", str(expect), "--out", f"{W}/{ten}_{i}.jsonl", "--shard", f"{i}/2"],
               logs[i], i) for i in (0, 1)]
    doi(ps, logs)
    with open(f"{W}/{ten}.jsonl", "w") as f:
        for i in (0, 1): f.write(open(f"{W}/{ten}_{i}.jsonl").read())

for n in (250, 500):
    sinh(f"pred_rag{n}_val", CK[n], V["recs"], V["ocr"], V["img"], V["ex"], 1002)
sinh("pred_rag500_test", CK[500], f"{TEST}/test.jsonl", f"{TEST}/ocr.jsonl", f"{TEST}/images", f"{SRC}/ex_test_k4.jsonl", 4463)

# Ô E-1b (tuỳ chọn, ~25 phút): kho rỗng — bước 500 trên val KHÔNG có khối, xem mô hình có vỡ khi không truy hồi được không
sinh("pred_rag500_val_rong", CK[500], V["recs"], V["ocr"], V["img"], None, 1002)

# Ô E-2: chấm — val (chỉ xem) và tập kiểm (7 thước, --check tái lập ck500)
vals = ["--pred", f"rag250={W}/pred_rag250_val.jsonl", "--pred", f"rag500={W}/pred_rag500_val.jsonl"]
if os.path.exists(f"{W}/pred_rag500_val_rong.jsonl"): vals += ["--pred", f"rag500_rong={W}/pred_rag500_val_rong.jsonl"]
py(f"{RA}/ra_score.py", "--recs", V["recs"], "--pred", f"ck500={SRC}/pred_ck500_vallon.jsonl", *vals,
   "--ra", f"rag500={V['ex']}", "--no-bert", "--out", f"{W}/diem_val_rag.json")
py(f"{RA}/ra_score.py", "--recs", f"{TEST}/test.jsonl", "--pred", f"ck500={SRC}/pred_ck500_test.jsonl",
   "--pred", f"rag500={W}/pred_rag500_test.jsonl", "--ra", f"rag500={SRC}/ex_test_k4.jsonl", "--check", "--out", f"{W}/diem_test_rag.json")

# Ô E-3: exec — chấm UGround câu rag500 khác ck500 + 40 câu ck500 không đổi để hiệu chuẩn (~1,5–2 h)
import random
E = f"{W}/exec_out"; os.makedirs(E, exist_ok=True)
ck = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{SRC}/pred_ck500_test.jsonl"))}
rg = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{W}/pred_rag500_test.jsonl"))}
doi_k = sorted(k for k in rg if rg[k] != ck[k])
cal = random.Random(20261010).sample(sorted(k for k in rg if rg[k] == ck[k]), 40)
print(f"câu khác ck500: {len(doi_k)} - hiệu chuẩn: {len(cal)}")
def ghi(p, ks, P):
    with open(p, "w") as f:
        for k in ks: f.write(json.dumps({"episode_id": k[0], "step_id": k[1], "pred": P[k]}, ensure_ascii=False) + "\n")
for i in (0, 1):
    ghi(f"{E}/cal_{i}.jsonl", cal[i::2], ck); ghi(f"{E}/cw_{i}.jsonl", doi_k[i::2], rg)
def cham(ten, gpu):
    return subprocess.Popen(["python", f"{PKG}/harness/score_run.py", "--mode", "score", "--preds", f"{E}/{ten}.jsonl",
                             "--out", f"{E}/score_{ten}.json"], stdout=open(f"{E}/score_{ten}.log", "w"), stderr=subprocess.STDOUT,
                            env={**ENV, "CUDA_VISIBLE_DEVICES": str(gpu)}, cwd=W, start_new_session=True)
for loai in ("cal", "cw"):
    ps = [cham(f"{loai}_{i}", i) for i in (0, 1)]
    doi(ps, [f"{E}/score_{loai}_{i}.log" for i in (0, 1)])
for d in (M, RA): shutil.rmtree(d, ignore_errors=True)
shutil.make_archive("/tmp/ket_qua_312_E", "zip", W, "."); shutil.move("/tmp/ket_qua_312_E.zip", f"{W}/ket_qua_312_E.zip")
print(sorted(os.listdir(E)), f"{(time.time()-T0)/3600:.2f} h")
```

Tên `cw_*` giữ nguyên để `doc_exec_cw.py` đọc được, như lượt 309.

## 8. Máy nhà (CPU)

Giải nén `ket_qua_312_E.zip` vào `thesis-master/runs/rag312/`, rồi:

```bash
cd /Users/P836901/Documents/Self-learning/thesis
_venv_308/bin/python _scripts/311/doc_exec_cw.py --exec-dir thesis-master/runs/rag312/exec_out \
  --pred thesis-master/runs/rag312/pred_rag500_test.jsonl --ten rag500
_venv_308/bin/python _scripts/311/ktc_chu.py --a thesis-master/runs/rag312/pred_rag500_test.jsonl \
  --b thesis-master/_scripts/304/ra-sft-script/pred_ck500_test.jsonl --ten-a rag500 --ten-b ck500 \
  --out thesis-master/runs/rag312/ktc_chu_rag500.json
```

Cả hai script đã tự kiểm trên máy, `doc_exec_cw.py` dựng lại R3 ra exec 60,68 · D.3 67,11 · AitW 76,32. `ktc_chu.py` dựng lại R3 − ck500 ra BLEU-4 +1,12 [+0,78; +1,45], ROUGE-L +0,76, CIDEr-D +12,04.

## 9. Đọc kết quả

Mốc tập kiểm: **ck500 BLEU-4 52,36 · METEOR 37,91 · ROUGE-L 68,34 · CIDEr-D 430,04 · SPICE 45,79 · chrF 62,86 · BERTScore 67,07 · exec 60,65 [58,90; 62,38].**

| rag500 trên tập kiểm | đọc |
|---|---|
| ≥ 4/7 thước chữ hơn ck500, exec không thấp hơn có ý nghĩa | RA-GRPO thành mô hình chính; ck500 là dòng “bỏ truy hồi” |
| ≥ 4/7 thước chữ, exec thấp hơn có ý nghĩa | báo được trên thước chữ nhưng phải khai exec; xem tỉ lệ chép đúng — nếu thấp thì RL đã học chép bừa |
| < 4/7 | đóng hướng truy hồi khi train; nếu cần số chữ thì báo R3, khai là hậu xử lý |

Đọc kèm:

- `chep_vi_du_pct`, `chep_dung_pct_trong_so_chep` của rag500 (trong `diem_test_rag.json`): RL có học dùng khối không. `ra_k4` là 19,1% / 43,5%.
- rag250 > rag500 trên val: xu hướng, không dùng để chọn.
- `rag500_rong` (nếu chạy): mô hình còn viết được khi không có khối.
- `ktc_chu_rag500.json`: khoảng tin cậy BLEU-4, ROUGE-L, CIDEr-D của hiệu số.

## 10. Sự cố thường gặp

| hiện tượng | làm gì |
|---|---|
| Ô 0-1 assert 2 GPU | đổi Accelerator sang T4 ×2, chạy lại |
| Ô 0-2 hoà S1 lỗi peft | Ô 0-1 chưa gỡ torchao hoặc chưa ghim peft 0.21.1 |
| Ô T-3a cả hai cấu hình tràn | gửi `probe_4.log`, `probe_2.log`. Hướng tiếp: cắt khối còn 3 câu (agent sửa) |
| không thấy `[RA] câu nhắc đã dựng` | phần vá trainer không ăn với trl đang cài; dừng, gửi 80 dòng đầu `train.log` |
| lần 2 không có `[nạp default] ... + x > 0` | dừng ngay (lỗi chạy tiếp ngày 30/9) |
| `[chép]` tăng mà chép đúng ~0 | ghi lại, vẫn chạy hết, nhưng chắc chắn đo exec ở E |
| notebook RUNNING quá 12 h, không log | huỷ; kiểm số GPU được cấp (bài học G2 lượt 310) |
| Ô E-2 `--check` báo LỆCH | bộ chấm khác lượt 304; dừng đọc A, gửi log |

## 11. Gửi lại cho chat

1. G0: dòng `→ CỔNG G0: …`, hai dòng **CÓ khối / KHÔNG khối**, bảng `ra_score`.
2. T1: `cau_hinh.json`; các dòng `[kho]`, `[câu nhắc]`, `[RA]`, `[LoRA mới]`; 20 dòng cuối `train.log`.
3. T2, T3: dòng `[tiếp từ]`, `[nạp default]`; 20 dòng cuối `train.log`.
4. E: bảng in cuối Ô E-2 (val và tập kiểm), số câu khác ck500 ở Ô E-3.
5. Máy nhà: output của `doc_exec_cw.py` và `ktc_chu.py`.

## 12. Việc agent không làm

- Không chạy Kaggle, không commit, không sửa luận văn.
- Script mới nằm ngoài `thesis-master/`. Muốn đưa vào repo thì tự chép (ví dụ `harness/ra_grpo/`) rồi: `git add harness/ra_grpo && git commit -m "RA-GRPO: cổng G0, bọc train, đọc cổng, KTC (312)" && git push`

## 13. Kiểm đã làm trên máy

- `ra_grpo.py --tu-kiem`: **ĐẠT**.
  - Khối chèn ngay trước dòng cuối, phần đầu câu nhắc giữ nguyên từng byte, 1–4 câu mẫu, không lấy bước nào của chính tác vụ.
  - Bộ đếm chép đếm đúng.
  - Bọc hàm thưởng giữ nguyên giá trị thưởng và giữ tên `r_spice`.
- `ra_grpo_g0_doc.py --tu-kiem --no-spice`: **ĐẠT** trên dữ liệu giả. SPICE chạy trên Kaggle vì Mac không có Java.
- `ra_grpo_g0.py --dry` trên 300 bước val: câu nhắc có khối đúng mẫu lượt 304.
- `ktc_chu.py --tu-kiem`, `doc_exec_cw.py --tu-kiem`: **ĐẠT** (tái lập số R3).
- `grpo_spice.py` trong `ra-sft-script` trùng md5 bản đã train ck500.
- Chưa chạy: mọi phần GPU, phần vá `trl.GRPOTrainer` với trl 0.29.1 thật, và chế độ `--probe` qua `ra_grpo.py`. Các dòng log ở mục 6 là chốt kiểm sớm.

# Phụ lục — mã nguồn nguyên văn

`grpo_spice.py`, `build_branch_data.py`, `ra_exemplars.py`, `ra_gen.py`, `ra_score.py` dùng nguyên bản trong dataset `trangphngngc/ra-sft-script` (trên đĩa: `thesis-master/_scripts/304/ra-sft-script/`), không chép lại.

## Phụ lục A — `ra_grpo.py`

```python
# -*- coding: utf-8 -*-
"""311 — RA-GRPO: chạy ĐÚNG công thức ck500 (grpo_spice.py của lượt 304, không sửa) nhưng câu nhắc có khối 4 câu mẫu.

Khác ck500 đúng một biến: `grpo_spice.body_of` được bọc để chèn khối `ra_exemplars.chen(body, Kho.cho_test(x, 4, ocr, own=tác vụ))`.
Kho = train_tru_val.jsonl bỏ mọi tác vụ của p1_val_rows. Cùng 1.000 câu nhắc, cùng hạt, cùng G/lô/B/lr/500 bước,
cùng S1 hoà làm điểm xuất phát và làm mốc KL (lúc tính KL, mốc cũng thấy khối).
Thêm: dừng êm sau --gio giờ (lưu điểm lưu rồi thoát) để nối commit Kaggle; khối của mỗi câu nhắc ghi đệm ra --out/ra_cache.json.

    python ra_grpo.py --kho train_tru_val.jsonl --gio 10.3 -- --train --bundle B --merged M --out O --resume auto --no-q4?
    (mọi đối số sau "--" chuyển nguyên cho grpo_spice.main; dùng đúng lệnh train của ck500)
    python ra_grpo.py --tu-kiem        # kiểm phần chèn khối trên CPU, không cần GPU
"""
import os, sys, json, time, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, "/kaggle/working/ra", os.path.join(HERE, "..", "..", "thesis-master", "_scripts", "304", "ra-sft-script")):
    if os.path.isdir(p):
        sys.path.insert(0, p)
import ra_exemplars as RA


def ocr_toks(o):
    return {w for it in (o or {"items": []})["items"][:24] for w in RA.tok(it.get("text", ""))}


def boc_body(goc, kho, cache, dem):
    def body_of(r, ocr):
        b = goc(r, ocr)
        key = f"{r['episode_id']}_{r['step_id']}"
        if key not in cache:
            x = dict(goal=r["goal"], history=r.get("history") or [])
            cache[key] = kho.cho_test(x, 4, ocr_toks(ocr.get(r["image"])), own=r["episode_id"])
        exs = cache[key]
        dem["n"] += 1
        dem["co_khoi"] += bool(exs)
        return RA.chen(b, exs) if exs else b
    return body_of


def dem_chep(completions, keys, golds, cache):
    """Tỉ lệ câu sinh trùng nguyên văn một câu mẫu của khối, và trong số đó tỉ lệ trùng câu chuẩn."""
    chep = dung = 0
    for c, k, g in zip(completions, keys, golds):
        s = (c[0].get("content") if isinstance(c, list) and c else c) or ""
        t = RA.tok(s)
        if t and any(RA.tok(e["sent"]) == t for e in cache.get(k, [])):
            chep += 1
            dung += t == RA.tok(g)
    return chep, dung, len(completions)


def boc_thuong(goc, cache):
    def r_spice(completions, gold, **kw):
        out = goc(completions, gold, **kw)
        try:
            chep, dung, n = dem_chep(completions, kw.get("key") or [], gold, cache)
            print(f"[chép] {chep}/{n} câu trùng câu mẫu - trong đó trùng câu chuẩn {dung}", flush=True)
        except Exception as e:
            print(f"[chép] không đếm được: {e!r}", flush=True)
        return out
    return r_spice


def tu_kiem():
    from build_branch_data import prompt_body
    KHO = "/Users/P836901/Documents/Self-learning/thesis/thesis-master"
    recs = [json.loads(l) for l in open(f"{KHO}/harness/dg1_cache/train_ac/train_tru_val.jsonl", encoding="utf-8")]
    kho = RA.Kho(recs)
    goc = lambda r, ocr: prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
    cache, dem = {}, dict(n=0, co_khoi=0)
    f = boc_body(goc, kho, cache, dem)
    r = next(t for t in kho.tr if t.get("history"))
    b = f(r, {})
    assert RA.HEADER in b and b.endswith(RA.LAST) and b.startswith(goc(r, {})[:-len(RA.LAST)]), b
    lay = cache[f"{r['episode_id']}_{r['step_id']}"]
    assert 1 <= len(lay) <= 4, lay
    cua_minh = {(t["target_instruction"].strip(), t["goal"], RA._hlast(t)) for t in kho.eps[r["episode_id"]].values()}
    assert not any((e["sent"], e["goal"], e["prev"]) in cua_minh for e in lay), "⛔ khối lấy bước của chính tác vụ"
    k = f"{r['episode_id']}_{r['step_id']}"
    c3 = [[{"content": lay[0]["sent"]}], [{"content": "something else"}], [{"content": lay[0]["sent"]}]]
    assert dem_chep(c3, [k, k, k], [lay[0]["sent"], "x", "y"], cache) == (2, 1, 3)
    thuong = boc_thuong(lambda c, g, **kw: [0.5] * len(c), cache)
    assert thuong(c3, ["a", "b", "c"], key=[k, k, k]) == [0.5, 0.5, 0.5] and thuong.__name__ == "r_spice"
    print(f"[tự kiểm] ĐẠT - khối chèn đúng chỗ, phần đầu câu nhắc giữ nguyên, {len(lay)} câu mẫu (≤ 4 sau khử trùng), "
          "bỏ chính tác vụ; bộ đếm chép đúng; bọc thưởng giữ nguyên giá trị thưởng")
    print(b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kho")
    ap.add_argument("--gio", type=float, default=10.3)
    ap.add_argument("--tu-kiem", action="store_true")
    if "--" in sys.argv:
        i = sys.argv.index("--")
        mine, rest = sys.argv[1:i], sys.argv[i + 1:]
    else:
        mine, rest = sys.argv[1:], []
    a = ap.parse_args(mine)
    if a.tu_kiem:
        return tu_kiem()

    import grpo_spice as GS
    g = argparse.ArgumentParser(add_help=False)
    g.add_argument("--bundle")
    g.add_argument("--out")
    ga, _ = g.parse_known_args(rest)
    va = [json.loads(l) for l in open(os.path.join(ga.bundle, "p1_val_rows.jsonl"), encoding="utf-8")]
    kho = RA.Kho([json.loads(l) for l in open(a.kho, encoding="utf-8")], loai_ep={r["episode_id"] for r in va})
    print(f"[kho] {len(kho.tr)} bước - {len(kho.eid)} tác vụ - bỏ {len({r['episode_id'] for r in va})} tác vụ val", flush=True)
    assert len(kho.tr) > 60000, "⛔ kho quá nhỏ - sai tệp train_tru_val?"

    cache_p = os.path.join(ga.out, "ra_cache.json") if ga.out else None
    cache = json.load(open(cache_p)) if cache_p and os.path.exists(cache_p) else {}
    dem = dict(n=0, co_khoi=0)
    GS.body_of = boc_body(GS.body_of, kho, cache, dem)
    GS.r_spice = boc_thuong(GS.r_spice, cache)

    import transformers, trl
    T0 = time.time()

    class DungGio(transformers.TrainerCallback):
        def on_step_end(self, args, state, control, **kw):
            if (time.time() - T0) / 3600 > a.gio:
                control.should_save = True
                control.should_training_stop = True
                print(f"[dừng giờ] {a.gio} h ở bước {state.global_step} - lưu điểm lưu rồi thoát; chạy lại với --resume auto",
                      flush=True)
            return control

    Goc = trl.GRPOTrainer

    class Trainer(Goc):
        def __init__(self, *x, **k):
            super().__init__(*x, **k)
            self.add_callback(DungGio())
            print(f"[RA] câu nhắc đã dựng {dem['n']} - có khối {dem['co_khoi']} - đệm {len(cache)}", flush=True)
            if cache_p:
                os.makedirs(ga.out, exist_ok=True)
                json.dump(cache, open(cache_p, "w"), ensure_ascii=False)

    trl.GRPOTrainer = Trainer
    sys.argv = [GS.__file__] + rest
    GS.main()


if __name__ == "__main__":
    main()
```

## Phụ lục B — `ra_grpo_g0.py`

```python
# -*- coding: utf-8 -*-
"""311 — cổng G0 trước RA-GRPO: S1 (hoà, KHÔNG adapter) nhìn khối 4 câu mẫu thì sinh ra sao (Kaggle T4).

Hai chế độ, cùng đường sinh S1 của lượt 289 (`s1_merged` fp16, SYS + [ảnh, "\n" + body]):
--mode greedy  : greedy 96 token cho mọi bước click của --recs, có khối (--ra) -> so với pred_S1_vallon (không khối)
--mode mau     : 8 mẫu T = 1,0 cho --n-mau bước click rút cố định (hạt 20261012), có khối (--ra) hoặc không
                 -> đo trần best-of-8 có khối so với không khối; RL chỉ học được tới chỗ mẫu đã chạm

python ra_grpo_g0.py --mode greedy --merged M --recs B/p1_val_rows.jsonl --ocr B/ocr.jsonl --images B/images --ra ex_val_k4.jsonl --out g0_greedy_ra_0.jsonl --shard 0/2
python ra_grpo_g0.py --mode mau --merged M ... --ra ex_val_k4.jsonl --out g0_mau_ra.jsonl
python ra_grpo_g0.py --mode mau --merged M ... --out g0_mau_khong.jsonl        # không khối
thêm --dry: in câu nhắc, không nạp mô hình. Nối tiếp được.
"""
import os, sys, json, time, random, argparse
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, "/kaggle/working/ra", os.path.join(HERE, "..", "..", "thesis-master", "_scripts", "304", "ra-sft-script")):
    if os.path.isdir(p):
        sys.path.insert(0, p)
from build_branch_data import prompt_body, SYS
import ra_exemplars as RA

TAPT = ("click", "long_press")
HAT_MAU = 20261012


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("greedy", "mau"), required=True)
    ap.add_argument("--merged", default="")
    ap.add_argument("--recs", required=True)
    ap.add_argument("--ocr", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--ra", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-mau", type=int, default=300)
    ap.add_argument("--g", type=int, default=8)
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    a.q4 = False

    rows = [json.loads(l) for l in open(a.recs, encoding="utf-8")]
    rows = [r for r in rows if (r.get("action") or {}).get("action_type") in TAPT and "x" in r["action"]]
    if a.mode == "mau":
        keys = sorted((r["episode_id"], r["step_id"]) for r in rows)
        chon = set(random.Random(HAT_MAU).sample(keys, min(a.n_mau, len(keys))))
        rows = [r for r in rows if (r["episode_id"], r["step_id"]) in chon]
    si, sn = map(int, a.shard.split("/"))
    rows = rows[si::sn]
    ocr = {o["image"]: o for o in map(json.loads, open(a.ocr, encoding="utf-8"))}
    EXM = None
    if a.ra:
        EXM = {(d["episode_id"], d["step_id"]): d["exemplars"] for d in map(json.loads, open(a.ra, encoding="utf-8"))}
        assert all((r["episode_id"], r["step_id"]) in EXM for r in rows), "⛔ tệp ví dụ thiếu bước"

    def body_of(r):
        b = prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
        e = EXM[(r["episode_id"], r["step_id"])] if EXM is not None else None
        return RA.chen(b, e) if e else b

    print(f"[G0] {a.mode} - khối {'CÓ' if a.ra else 'KHÔNG'} - {len(rows)} bước - [câu nhắc đầu]\n{body_of(rows[0])}", flush=True)
    if a.dry:
        return

    import torch
    from PIL import Image
    import grpo_spice as GS
    proc, model, _, _ = GS.nap(a)
    model.eval()
    print("[kiểm lưu] KHÔNG gắn - S1 hoà", flush=True)
    done = set()
    if os.path.exists(a.out):
        done = {(d["episode_id"], d["step_id"]) for d in map(json.loads, open(a.out, encoding="utf-8"))}
    fo = open(a.out, "a", encoding="utf-8")
    t0, moi = time.time(), 0
    for i, r in enumerate(rows):
        k = (r["episode_id"], r["step_id"])
        if k in done:
            continue
        msg = [{"role": "system", "content": SYS},
               {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body_of(r)}]}]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.images, os.path.basename(r["image"]))).convert("RGB")
        inp = proc(text=[text], images=[img], return_tensors="pt").to(model.device)
        L = inp["input_ids"].shape[1]
        with torch.no_grad():
            if a.mode == "greedy":
                g = model.generate(**inp, max_new_tokens=96, do_sample=False, use_cache=True,
                                   temperature=None, top_p=None, top_k=None)
                rec = {"episode_id": k[0], "step_id": k[1], "pred": proc.decode(g[0][L:], skip_special_tokens=True).strip()}
            else:
                torch.manual_seed(HAT_MAU + 1000 * int(k[0]) + int(k[1]))
                g = model.generate(**inp, max_new_tokens=96, do_sample=True, temperature=1.0, top_p=1.0, top_k=0,
                                   num_return_sequences=a.g, use_cache=True)
                rec = {"episode_id": k[0], "step_id": k[1],
                       "samples": [proc.decode(x[L:], skip_special_tokens=True).strip() for x in g]}
        fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fo.flush()
        moi += 1
        if (i + 1) % 25 == 0:
            dt = time.time() - t0
            print(f"  {i+1}/{len(rows)} - {dt/60:.1f} phút - {dt/moi:.2f} s/bước", flush=True)
    fo.close()
    print(f"[xong] {sum(1 for _ in open(a.out, encoding='utf-8'))} dòng -> {a.out}", flush=True)


if __name__ == "__main__":
    main()
```

## Phụ lục C — `ra_grpo_g0_doc.py`

```python
# -*- coding: utf-8 -*-
"""311 — đọc cổng G0 (CPU; SPICE cần Java 8 + pycocoevalcap như lúc chấm ck500).

Đọc 8 mẫu của S1 có khối và không khối trên cùng bước val, đo:
- trần best-of-8 (lấy mẫu tốt nhất theo câu chuẩn) cho SPICE, CIDEr-D (công thức pycocoevalcap, df trên câu chuẩn val)
- tỉ lệ bước có ít nhất một mẫu trùng nguyên văn câu chuẩn
- trong các bước khối chứa câu chuẩn: tỉ lệ có mẫu chép đúng câu đó
Rồi áp luật cổng (in ra, không tự chạy gì thêm).

python ra_grpo_g0_doc.py --recs B/p1_val_rows.jsonl --ra ex_val_k4.jsonl --mau-ra g0_mau_ra.jsonl --mau-khong g0_mau_khong.jsonl \
  --diem-greedy diem_g0_greedy.json --out g0_ket_qua.json
python ra_grpo_g0_doc.py --tu-kiem --no-spice
"""
import os, re, sys, json, math, argparse
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, "/kaggle/working/ra", os.path.join(HERE, "..", "..", "thesis-master", "_scripts", "304", "ra-sft-script")):
    if os.path.isdir(p):
        sys.path.insert(0, p)

PUNCT = {"''", '"', "``", "-lrb-", "-rrb-", "-lcb-", "-rcb-", ".", "?", "!", ",", ":", "-", "--", "...", ";", "'"}
TOK = re.compile(r"n't|'s|'re|'ve|'ll|'d|'m|[a-z0-9]+(?:[-./][a-z0-9]+)*|[^\sa-z0-9]")


def tok(s):
    s = (s or "").lower().replace("“", '"').replace("”", '"').replace("’", "'")
    s = re.sub(r"(\w)n't\b", r"\1 n't", s)
    return [t for t in TOK.findall(s) if t not in PUNCT and t != ""]


def ngrams(ws, n=4):
    c = defaultdict(int)
    for k in range(1, n + 1):
        for i in range(len(ws) - k + 1):
            c[tuple(ws[i:i + k])] += 1
    return c


class CiderD:
    def __init__(self, refs, n=4, sigma=6.0):
        self.n, self.sigma, self.df = n, sigma, defaultdict(float)
        for r in refs:
            for ng in set(ngrams(tok(r), n)):
                self.df[ng] += 1
        self.log_n = math.log(float(len(refs)))

    def _vec(self, s):
        cnts = ngrams(tok(s), self.n)
        vec, norm, length = [dict() for _ in range(self.n)], [0.0] * self.n, 0
        for ng, tf in cnts.items():
            k = len(ng) - 1
            w = float(tf) * (self.log_n - math.log(max(1.0, self.df.get(ng, 0.0))))
            vec[k][ng] = w
            norm[k] += w * w
            if k == 1:
                length += tf
        return vec, [math.sqrt(x) for x in norm], length

    def score(self, cand, ref):
        vh, nh, lh = self._vec(cand)
        vr, nr, lr = self._vec(ref)
        pen = math.exp(-((lh - lr) ** 2) / (2 * self.sigma ** 2))
        tot = 0.0
        for k in range(self.n):
            v = sum(min(w, vr[k].get(ng, 0.0)) * vr[k].get(ng, 0.0) for ng, w in vh[k].items())
            if nh[k] != 0 and nr[k] != 0:
                v /= nh[k] * nr[k]
            tot += v * pen
        return 10.0 * tot / self.n


def spice_mot_luot(cands, refs):
    import grpo_spice as GS
    return GS.spice_batch([c if c else "none" for c in cands], refs)


def tran(M, REF, CID, EX, dung_spice):
    keys = sorted(M)
    ca = [(k, j) for k in keys for j in range(len(M[k]))]
    cid = {(k, j): CID.score(M[k][j], REF[k]) for k, j in ca}
    sp = {}
    if dung_spice:
        vals = spice_mot_luot([M[k][j] for k, j in ca], [REF[k] for k, j in ca])
        sp = {kj: v for kj, v in zip(ca, vals)}
    eq = lambda a, b: tok(a) == tok(b)
    out = dict(n=len(keys),
               cider_best8=100 * sum(max(cid[(k, j)] for j in range(len(M[k]))) for k in keys) / len(keys),
               cider_tb=100 * sum(cid.values()) / len(ca),
               trung_chuan_bat_ky=100 * sum(any(eq(s, REF[k]) for s in M[k]) for k in keys) / len(keys))
    if sp:
        out["spice_best8"] = 100 * sum(max(sp[(k, j)] for j in range(len(M[k]))) for k in keys) / len(keys)
        out["spice_tb"] = 100 * sum(sp.values()) / len(ca)
    co = {k for k in keys if any(eq(e["sent"], REF[k]) for e in EX.get(k, []))}
    out["buoc_khoi_chua_chuan"] = len(co)
    out["chep_dung_trong_buoc_do"] = 100 * sum(any(eq(s, REF[k]) for s in M[k]) for k in co) / max(1, len(co))
    out["mau_trung_vi_du"] = 100 * sum(any(eq(s, e["sent"]) for e in EX.get(k, [])) for k in keys for s in M[k]) / len(ca)
    return out


def doc_mau(p):
    return {(d["episode_id"], d["step_id"]): d["samples"] for d in map(json.loads, open(p, encoding="utf-8"))}


def luat(ra, khong, greedy):
    ok1 = ("spice_best8" in ra) and ra["spice_best8"] - khong["spice_best8"] >= 1.0
    ok1b = ra["cider_best8"] - khong["cider_best8"] >= 10.0
    ok2 = greedy is None or (greedy["cider_d"] >= greedy["cider_d_khong"] - 10 and
                             greedy.get("spice", 0) >= greedy.get("spice_khong", 0) - 1.0)
    if (ok1 or ok1b) and ok2:
        return "ĐẠT - chạy RA-GRPO từ S1 (Phương án A)"
    if not (ok1 or ok1b) and ok2 and ra["chep_dung_trong_buoc_do"] < khong["chep_dung_trong_buoc_do"] + 5:
        return "KHÔNG ĐẠT vì S1 không dùng khối - muốn đi tiếp thì phải RA-SFT từ S1 trước (Phương án B), hỏi người dùng"
    return "KHÔNG ĐẠT - khối làm S1 kém đi hoặc không tăng trần; dừng hướng RA-GRPO"


def tu_kiem(dung_spice):
    REF = {(1, 0): "Click on the search bar", (1, 1): "Open the Clock app", (2, 0): "Tap on Save"}
    EX = {(1, 0): [{"sent": "Click on the search bar"}], (1, 1): [{"sent": "Tap on Save"}], (2, 0): [{"sent": "Open the Clock app"}]}
    M_ra = {(1, 0): ["Click on the search bar", "click search"], (1, 1): ["Open clock", "Open the Clock app"], (2, 0): ["Tap Save", "Save"]}
    M_kh = {(1, 0): ["click search", "tap bar"], (1, 1): ["Open clock", "open app"], (2, 0): ["Tap Save", "Save"]}
    CID = CiderD(list(REF.values()))
    a, b = tran(M_ra, REF, CID, EX, dung_spice), tran(M_kh, REF, CID, EX, dung_spice)
    assert a["trung_chuan_bat_ky"] > b["trung_chuan_bat_ky"] and a["cider_best8"] > b["cider_best8"], (a, b)
    assert a["buoc_khoi_chua_chuan"] == 1 and a["chep_dung_trong_buoc_do"] == 100.0, a
    print("[tự kiểm] ĐẠT", {k: round(v, 2) for k, v in a.items()})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recs")
    ap.add_argument("--ra")
    ap.add_argument("--mau-ra")
    ap.add_argument("--mau-khong")
    ap.add_argument("--diem-greedy", help="JSON của ra_score.py với nhánh S1 (không khối) và S1_ra (có khối)")
    ap.add_argument("--out")
    ap.add_argument("--no-spice", action="store_true")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        return tu_kiem(not a.no_spice)

    recs = [json.loads(l) for l in open(a.recs, encoding="utf-8")]
    REF = {(r["episode_id"], r["step_id"]): (r.get("target_instruction") or r.get("gold_instruction") or "").strip() for r in recs}
    EX = {(d["episode_id"], d["step_id"]): d["exemplars"] for d in map(json.loads, open(a.ra, encoding="utf-8"))}
    Mra, Mkh = doc_mau(a.mau_ra), doc_mau(a.mau_khong)
    assert set(Mra) == set(Mkh), "⛔ hai tệp mẫu không cùng bước"
    CID = CiderD([REF[k] for k in sorted(REF) if REF[k]])
    ra = tran(Mra, REF, CID, EX, not a.no_spice)
    kh = tran(Mkh, REF, CID, EX, not a.no_spice)
    g = None
    if a.diem_greedy:
        D = json.load(open(a.diem_greedy))["diem"]
        g = dict(cider_d=D["S1_ra"]["cider_d"], cider_d_khong=D["S1"]["cider_d"],
                 spice=D["S1_ra"].get("spice", 0), spice_khong=D["S1"].get("spice", 0),
                 bang={n: D[n] for n in D})
    kq = dict(co_khoi=ra, khong_khoi=kh, greedy=g, ket_luan=luat(ra, kh, g))
    for ten, o in (("CÓ khối", ra), ("KHÔNG khối", kh)):
        print(f"{ten:10s} " + " - ".join(f"{k} {v:.2f}" if isinstance(v, float) else f"{k} {v}" for k, v in o.items()))
    if g:
        print(f"greedy S1: CIDEr-D có khối {g['cider_d']:.2f} vs không {g['cider_d_khong']:.2f} - "
              f"SPICE {g['spice']:.2f} vs {g['spice_khong']:.2f}")
    print("→ CỔNG G0:", kq["ket_luan"])
    json.dump(kq, open(a.out, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
```

## Phụ lục D — `ktc_chu.py`

```python
# -*- coding: utf-8 -*-
"""311 — KTC95 bootstrap gom cụm theo tác vụ cho hiệu số thước chữ giữa hai tệp câu trên 4.463 bước click tập kiểm (CPU).

BLEU-4 (corpus, gộp thống kê n-gram), ROUGE-L (trung bình câu, β = 1,2), CIDEr-D (trung bình câu, df trên câu chuẩn tập kiểm),
tách từ xấp xỉ PTBTokenizer — cùng bộ đo đã tái lập Δ chính thức của ra_k4/R3 lệch ≤ 0,06 (file 308 §2.1).
Số điểm tuyệt đối lấy từ ra_score.py (bản chính thức); script này chỉ cho khoảng tin cậy của hiệu số. B = 1000, hạt 20261010.

    python ktc_chu.py --a pred_rag500_test.jsonl --b pred_ck500_test.jsonl [--ten-a rag500 --ten-b ck500]
    python ktc_chu.py --tu-kiem        # R3 - ck500 phải ra +1,12 [+0,78; +1,45] · +0,76 · +12,04 như 308 §11.1
"""
import argparse, json, math, os, random, re
from collections import Counter, defaultdict

KHO = next(p for p in ("/mnt/d/Master/Thesis", "/Users/P836901/Documents/Self-learning/thesis/thesis-master") if os.path.isdir(p))
PUNCT = {"''", '"', "``", "-lrb-", "-rrb-", "-lcb-", "-rcb-", ".", "?", "!", ",", ":", "-", "--", "...", ";", "'"}
TOK = re.compile(r"n't|'s|'re|'ve|'ll|'d|'m|[a-z0-9]+(?:[-./][a-z0-9]+)*|[^\sa-z0-9]")


def tok(s):
    s = (s or "").lower().replace("“", '"').replace("”", '"').replace("’", "'")
    s = re.sub(r"(\w)n't\b", r"\1 n't", s)
    return [t for t in TOK.findall(s) if t not in PUNCT and t != ""]


def ngrams(ws, n=4):
    c = defaultdict(int)
    for k in range(1, n + 1):
        for i in range(len(ws) - k + 1):
            c[tuple(ws[i:i + k])] += 1
    return c


class CiderD:
    def __init__(self, refs, n=4, sigma=6.0):
        self.n, self.sigma, self.df = n, sigma, defaultdict(float)
        for r in refs:
            for ng in set(ngrams(tok(r), n)):
                self.df[ng] += 1
        self.log_n = math.log(float(len(refs)))

    def _vec(self, s):
        vec, norm, length = [dict() for _ in range(self.n)], [0.0] * self.n, 0
        for ng, tf in ngrams(tok(s), self.n).items():
            k = len(ng) - 1
            w = float(tf) * (self.log_n - math.log(max(1.0, self.df.get(ng, 0.0))))
            vec[k][ng] = w
            norm[k] += w * w
            if k == 1:
                length += tf
        return vec, [math.sqrt(x) for x in norm], length

    def score(self, cand, ref):
        vh, nh, lh = self._vec(cand)
        vr, nr, lr = self._vec(ref)
        pen = math.exp(-((lh - lr) ** 2) / (2 * self.sigma ** 2))
        tot = 0.0
        for k in range(self.n):
            v = sum(min(w, vr[k].get(ng, 0.0)) * vr[k].get(ng, 0.0) for ng, w in vh[k].items())
            if nh[k] != 0 and nr[k] != 0:
                v /= nh[k] * nr[k]
            tot += v * pen
        return 10.0 * tot / self.n


def lcs(a, b):
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def rouge_l(c, r, beta=1.2):
    a, b = tok(c), tok(r)
    l = lcs(a, b)
    if l == 0:
        return 0.0
    p, rc = l / len(a), l / len(b)
    return ((1 + beta ** 2) * p * rc) / (rc + beta ** 2 * p)


def bleu_stats(h, r):
    H, R = tok(h), tok(r)
    st = [len(H), len(R)]
    for n in range(1, 5):
        hc = Counter(tuple(H[i:i + n]) for i in range(len(H) - n + 1))
        rc = Counter(tuple(R[i:i + n]) for i in range(len(R) - n + 1))
        st += [sum(min(c, rc[g]) for g, c in hc.items()), max(0, len(H) - n + 1)]
    return st


def bleu_corpus(S):
    hl = sum(s[0] for s in S); rl = sum(s[1] for s in S); lp = 0.0
    for n in range(4):
        m = sum(s[2 + 2 * n] for s in S); t = sum(s[3 + 2 * n] for s in S)
        if m == 0 or t == 0:
            return 0.0
        lp += math.log(m / t) / 4
    return 100 * (1.0 if hl > rl else math.exp(1 - rl / max(hl, 1))) * math.exp(lp)


def nap(p):
    return {(str(d["episode_id"]), str(d["step_id"])): d.get("pred") or "" for d in map(json.loads, open(p, encoding="utf-8"))}


def ktc(pa, pb, ta="A", tb="B", B=1000):
    raw = [json.loads(l) for l in open(f"{KHO}/runs/grpo_spice/score_ck500_test_raw.jsonl", encoding="utf-8")]
    REF = {(str(d["episode_id"]), str(d["step_id"])): d.get("gold_instruction") or "" for d in raw}
    K = sorted(REF)
    A, Bp = nap(pa), nap(pb)
    assert set(K) <= set(A) and set(K) <= set(Bp), "⛔ tệp câu thiếu bước click tập kiểm"
    CID = CiderD([REF[k] for k in K])
    per = {t: {k: (bleu_stats(H[k], REF[k]), rouge_l(H[k], REF[k]), CID.score(H[k], REF[k])) for k in K}
           for t, H in ((ta, A), (tb, Bp))}
    cum = defaultdict(list)
    for k in K:
        cum[k[0]].append(k)
    eps = sorted(cum)
    diem = lambda t, ks: (bleu_corpus([per[t][k][0] for k in ks]),
                          100 * sum(per[t][k][1] for k in ks) / len(ks),
                          100 * sum(per[t][k][2] for k in ks) / len(ks))
    d0 = [x - y for x, y in zip(diem(ta, K), diem(tb, K))]
    rng = random.Random(20261010)
    bs = []
    for _ in range(B):
        ks = [k for e in (rng.choice(eps) for _ in eps) for k in cum[e]]
        bs.append([x - y for x, y in zip(diem(ta, ks), diem(tb, ks))])
    out = {}
    for j, m in enumerate(("bleu4", "rougeL", "cider_d")):
        v = sorted(b[j] for b in bs)
        out[m] = dict(delta=round(d0[j], 2), lo=round(v[int(0.025 * B)], 2), hi=round(v[int(0.975 * B) - 1], 2))
    doi = sum(A[k] != Bp[k] for k in K)
    print(f"{ta} - {tb} - câu khác {doi}/{len(K)} - " + " - ".join(f"{m} {r['delta']:+.2f} [{r['lo']:+.2f}; {r['hi']:+.2f}]" for m, r in out.items()))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a"); ap.add_argument("--b")
    ap.add_argument("--ten-a", default="A"); ap.add_argument("--ten-b", default="B")
    ap.add_argument("--out")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        o = ktc(f"{KHO}/runs/ra304_luat/pred_R3_test.jsonl", f"{KHO}/_scripts/304/ra-sft-script/pred_ck500_test.jsonl", "R3", "ck500")
        assert o["bleu4"] == dict(delta=1.12, lo=0.78, hi=1.45) and o["rougeL"]["delta"] == 0.76 and o["cider_d"]["delta"] == 12.04, o
        print("[tự kiểm] ĐẠT - tái lập đúng 308 §11.1")
    else:
        o = ktc(a.a, a.b, a.ten_a, a.ten_b)
        if a.out:
            json.dump(o, open(a.out, "w"), indent=1)
```

## Phụ lục E — `doc_exec_cw.py`

```python
# -*- coding: utf-8 -*-
"""308/309 — exec / D.3 / AitW đầy đủ cho một tệp câu (CW-RA) trên 4.463 bước click tập kiểm, 0 GPU.

Kaggle chỉ chấm UGround những bước có câu KHÁC ck500 (so từng byte với `sent` của tệp thô ck500); bước còn lại lấy
nguyên dòng của `runs/grpo_spice/score_ck500_test_raw.jsonl`. Cách làm y lượt 304 (doc_exec_304.py).
Tự kiểm: câu ck500 không đổi chấm lại (tệp score_cal_*_raw.jsonl) phải ra cùng tọa độ và exec với tệp thô cũ;
ck500 exec = 60,65; mọi bước câu khác ck500 phải có dòng chấm mới với đúng câu đó.

    python doc_exec_cw.py --exec-dir <thư mục chứa score_cal_*_raw.jsonl, score_cw_*_raw.jsonl> --pred pred_cw_t0.5_test.jsonl
    python doc_exec_cw.py --tu-kiem        # tái lập exec R3 = 60,68 từ tệp thô của lượt 304
"""
import argparse, glob, json, os, shutil, sys, tempfile

KHO = next(p for p in ("/mnt/d/Master/Thesis", "/Users/P836901/Documents/Self-learning/thesis/thesis-master")
           if os.path.isdir(p))
sys.path.insert(0, f"{KHO}/harness")
os.chdir(f"{KHO}/harness")
import luat_d3 as L
from luat_aitw_day_du import aitw_full
from d3_ktc import ktc, mcnemar
kh = L.kh


def doc(E, pred_path, ten="cw", out_json=None):
    CK = L.nap(f"{KHO}/runs/grpo_spice/score_ck500_test_raw.jsonl")
    S1 = L.nap(f"{KHO}/runs/score_s1_seed101_ra.jsonl")
    moi = lambda t: {kh(r): r for f in sorted(glob.glob(f"{E}/score_{t}_*_raw.jsonl")) for r in map(json.loads, open(f))}
    CAL, CW = moi("cal"), moi("cw")
    P = {kh(x): x["pred"] for x in map(json.loads, open(pred_path, encoding="utf-8"))}
    lech = [k for k in CAL if CAL[k].get("pred_xy") != CK[k].get("pred_xy") or CAL[k]["executable"] != CK[k]["executable"]]
    print(f"[hiệu chuẩn] {len(CAL)} câu ck500 chấm lại - lệch tọa độ/exec {len(lech)}", lech[:3])
    assert CAL and not lech, "⛔ dụng cụ lệch tệp thô ck500 - dừng"
    can = {k for k in P if P[k] != (CK[k].get("sent") or "")}
    thieu = sorted(can - set(CW))
    sai = [k for k in can & set(CW) if CW[k].get("sent") != P[k]]
    print(f"[{ten}] câu khác ck500 {len(can)} - có dòng chấm mới {len(can & set(CW))} - thiếu {len(thieu)} - câu lệch {len(sai)}")
    assert not thieu and not sai, (thieu[:3], sai[:3])
    R = {k: (CW[k] if k in can else CK[k]) for k in CK}
    with open(f"{E}/score_{ten}_gop_raw.jsonl", "w", encoding="utf-8") as f:
        for k in CK:
            f.write(json.dumps(R[k], ensure_ascii=False) + "\n")

    K = list(S1)
    assert set(K) == set(CK) == set(P) and len(K) == 4463
    for X in (CK, R, S1):
        for k in K:
            for c in ("executable", "action_ok", "toggle_ok", "hit_disk"):
                X[k].setdefault(c, 0)
    lu = lambda X: {k: dict(L.luat(X[k], k), aitwf=aitw_full(X[k], k)) for k in K}
    X = {"ck500": lu(CK), ten: lu(R), "S1/101": lu(S1)}
    cum = {k: S1[k].get("app") or f"ep{k[0]}" for k in K}
    TEN = {"vor": "exec", "d3": "D.3", "aitwf": "AitW"}
    out = {"ktc": {}, "so_sanh": {}, "cau_doi": len(can), "hieu_chuan": len(CAL)}
    for t in X:
        out["ktc"][t] = {}
        for c in TEN:
            p, lo, hi, _ = ktc(K, lambda k, cc: X[t][k][cc], c, cum)
            out["ktc"][t][c] = dict(diem=round(p, 2), lo=round(lo, 2), hi=round(hi, 2))
        print(f"{t:8s} " + " - ".join(f"{TEN[c]} {out['ktc'][t][c]['diem']:.2f} [{out['ktc'][t][c]['lo']:.2f}; {out['ktc'][t][c]['hi']:.2f}]" for c in TEN))
    assert abs(out["ktc"]["ck500"]["vor"]["diem"] - 60.65) < 0.01, "⛔ ck500 exec phải tái lập 60,65"
    for b in ("ck500", "S1/101"):
        for c in TEN:
            d, lo, hi, _ = ktc(K, lambda k, cc: X[ten][k][cc] - X[b][k][cc], c, cum)
            pha, cuu, _, p = mcnemar(K, X[b], X[ten], c)
            out["so_sanh"][f"{ten} - {b} - {TEN[c]}"] = dict(delta=round(d, 2), lo=round(lo, 2), hi=round(hi, 2), cuu=cuu, pha=pha, p=p)
            print(f"{ten} - {b:7s} {TEN[c]:5s} {d:+.2f} [{lo:+.2f}; {hi:+.2f}] - cứu {cuu} phá {pha} - p={p:.3g}")
    out_json = out_json or f"{E}/doc_exec_{ten}.json"
    json.dump(out, open(out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", out_json)
    return out


def tu_kiem():
    E0 = f"{KHO}/runs/ra304_G/exec_out/exec_out"
    pred = f"{KHO}/runs/ra304_luat/pred_R3_test.jsonl"
    T = tempfile.mkdtemp()
    for f in glob.glob(f"{E0}/score_cal_*_raw.jsonl"):
        shutil.copy(f, T)
    with open(f"{T}/score_cw_0_raw.jsonl", "w", encoding="utf-8") as fo:
        for f in sorted(glob.glob(f"{E0}/score_ghep_*_raw.jsonl")) + sorted(glob.glob(f"{E0}/score_ra_*_raw.jsonl")):
            fo.write(open(f, encoding="utf-8").read())
    o = doc(T, pred, "cw", out_json=f"{T}/x.json")
    assert abs(o["ktc"]["cw"]["vor"]["diem"] - 60.68) < 0.01 and abs(o["ktc"]["cw"]["d3"]["diem"] - 67.11) < 0.01 \
        and abs(o["ktc"]["cw"]["aitwf"]["diem"] - 76.32) < 0.01, o["ktc"]["cw"]
    print("[tự kiểm] ĐẠT - tái lập R3: exec 60,68 - D.3 67,11 - AitW 76,32 (khớp runs/ra304_luat/test_R3.json)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--exec-dir")
    ap.add_argument("--pred")
    ap.add_argument("--ten", default="cw")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    tu_kiem() if a.tu_kiem else doc(os.path.abspath(a.exec_dir), os.path.abspath(a.pred), a.ten)
```
