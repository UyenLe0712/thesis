# 238 — KẾT QUẢ G0 CỦA TFVF (28/9/2026) — ⛔ KHÔNG ĐẠT, DỪNG TFVF

Thi hành đúng `report/237_ACTION_TEST_TFVF_TRUOC_KHI_TRAIN_extracted.md`. Không train, không A100,
không đụng test, không sửa luận văn. ⛔ **Toàn bộ số dưới đây là số val (S1 đã thấy lúc dạy), cấm
trích ra báo hay luận văn.** Đây là phép Oracle để quyết định, không phải hệ thống.

## 1. Phán quyết

**G0 = DỪNG.** Trượt điều 2 (G không hơn F) và điều 4 (G không hơn O). Theo bảng bốn kết cục của
237 §5, trượt 2 rơi vào hàng *"S1 phản ứng với biến đổi ảnh nhưng không theo đúng vị trí"* ⇒ dừng
TFVF, **không train mô-đun, không viết kế hoạch pilot**.

| điều kiện (249 click) | đo được | kết luận |
|---|---|---|
| (1) câu G khác câu O ≥ 10% | 42/249 = **16,9%** | ĐẠT |
| (2) G > F ở ≥ 2/3 thước và ΔCIDEr-D(G−F) ≥ 3 | G > F chỉ ở BLEU-4 (1/3) · ΔCIDEr-D **−1,82** | **KHÔNG ĐẠT** |
| (3) G > C ở ≥ 2/3 thước | 3/3 | ĐẠT |
| (4) G ≥ O cả ba và G > O ở ≥ 2/3 | G > O chỉ ở BLEU-4; CIDEr-D và SPICE thấp hơn | **KHÔNG ĐẠT** |

## 2. Bảng số (COCO chính thức, PTBTokenizer, mức kho)

249 bước click:

| chế độ | BLEU-1 | BLEU-2 | BLEU-3 | **BLEU-4** | METEOR | ROUGE-L | **CIDEr-D** | **SPICE** |
|---|---|---|---|---|---|---|---|---|
| O ảnh gốc | 70,65 | 64,46 | 58,78 | 53,32 | 38,95 | 70,85 | 454,38 | 48,62 |
| G làm nét đích vàng | 70,57 | 64,45 | 58,93 | 53,62 | 38,94 | 70,69 | 451,83 | 48,35 |
| F làm nét chỗ đối diện | 69,62 | 63,73 | 58,30 | 53,03 | 38,55 | 70,39 | 453,65 | 49,01 |
| C làm nét tâm màn | 68,67 | 62,77 | 57,30 | 52,01 | 37,78 | 69,13 | 442,56 | 47,13 |

400 bước (bước không click giữ câu O ở mọi chế độ; chỉ để xem độ pha loãng):

| chế độ | BLEU-4 | CIDEr-D | SPICE |
|---|---|---|---|
| O | 59,48 | 543,77 | 57,30 |
| G | 59,72 | 542,43 | 57,13 |
| F | 59,32 | 543,64 | 57,54 |
| C | 58,56 | 536,67 | 56,37 |

Số bước câu khác nhau trên 249 click: G≠O **42 (16,9%)** · G≠F **49 (19,7%)** · G≠C **46 (18,5%)**.

## 3. Đọc

- Renderer có tới được câu: 17% số bước S1 đổi câu khi ảnh bị làm nét quanh đích. Kênh không bị bỏ
  qua hoàn toàn như bridge PATA hay cổng FGRB.
- Nhưng **đổi không theo đúng vị trí**: làm nét đúng đích (G) và làm nét chỗ đối diện (F) cho điểm
  ngang nhau (BLEU-4 +0,59, CIDEr-D −1,82, SPICE −0,66). Chênh ba thước đều dưới 2 điểm CIDEr-D, cỡ
  nhiễu của 249 bước. S1 phản ứng với việc ảnh bị biến đổi, không với *chỗ* được làm nét.
- G hơn C ở cả ba thước, nhưng C là chế độ thấp nhất trong bốn, kể cả thấp hơn F. Chỉ riêng điều này
  không đủ nói S1 dùng vị trí: làm nét tâm màn làm mờ cả đầu lẫn cuối màn, nơi nhiều đích nằm, nên
  điều (3) đạt mà (2) trượt là nhất quán với cách đọc *"biến đổi ảnh gây nhiễu, không mang tín hiệu vị
  trí"*.
- Focus hoàn hảo không giúp S1 so với ảnh gốc (CIDEr-D −2,55, SPICE −0,27). Như 237 đã lường, S1 chưa
  từng thấy ảnh làm nét nên điều (4) là tiêu chí chặt; nhưng điều (2) trượt độc lập với độ lệch phân
  phối (G và F chịu cùng renderer), nên không có cửa đọc thành *"train cho quen renderer là được"*.
- Cùng mẫu hình với PATA-C1 (`report/194` §5c) và FGRB P2 (`report/207` §8–11): tín hiệu vị trí đưa
  thêm vào S1 không làm câu đổi theo vị trí.

## 4. Kiểm toàn vẹn

- Tệp `tfvf_g0.py` chạy trên Kaggle **trùng byte** bản trong kho (so từ `results (6).zip`).
- Log in đúng: `hash400=a044f6d060d264b0` · `click trong 400 = 249` · `hash_click=8a24abe4f7f041e0` ·
  renderer đúng hằng số 237 · `greedy do_sample=False · max_new=96` · `dtype=torch.float16` (T4) ·
  transformers 5.17.0 · thiếu OCR 0.
- 249/249 dòng, 0 câu rỗng ở cả bốn chế độ, câu chuẩn khớp C1 tuyệt đối 249/249.
- Hàng O dùng lại câu greedy của `runs/c1/c1_mau.jsonl`, không gọi lại S1. Hàng O trên 400 bước tái lập
  đúng số greedy C1 đã ghi ở `report/233` (59,48 · 543,8 · 57,30).
- Thời gian: 249 bước × 3 chế độ trong **40,4 phút** T4 (tổng commit ~52 phút). 0 đồng.
- Kiểm trước khi chạy (0 GPU): đường đọc thử trên dữ liệu giả; renderer vẽ 5 bước xem bằng mắt.

## 5. Tệp

- Kết quả thô: `runs/tfvf_g0/tfvf_g0.jsonl` (249 dòng) · log `runs/tfvf_g0/tfvf_g0.log` · lượt thử
  `tfvf_g0_thu.jsonl`, `tfvf_thu.log`, `tfvf_ve.log` · bảng máy đọc `runs/tfvf_g0/g0_doc.json`.
- Mã: `harness/tfvf_g0.py` · `harness/tfvf_g0_doc.py` · runbook `harness/kaggle_tfvf_g0.md` · gói
  `_bundles/tfvf_g0_script.zip`.
- Chạy lại phần đọc: `~/.venvs/thesis/bin/python harness/tfvf_g0_doc.py runs/tfvf_g0/tfvf_g0.jsonl
  runs/c1/c1_mau.jsonl --json runs/tfvf_g0/g0_doc.json`
- Sai khác với 237: tệp kết quả ghi ở `report/238` trong kho thay vì đường dẫn Mac
  `/Users/P836901/...` (máy chạy là WSL); "Blur₈" hiểu là `PIL.ImageFilter.GaussianBlur(radius=8)`
  trên ảnh gốc, script in dòng này ra log.

## Phụ lục A — `harness/tfvf_g0.py`

```python
# -*- coding: utf-8 -*-
"""G0 của TFVF (report/237) — S1/101 đóng băng sinh greedy trên ảnh đã làm nét vùng đích.

Chạy trên Kaggle T4 (0 đồng) với dataset `fgrb-p1-bundle`, cùng 400 bước val của C1
(`random.Random(20260927).sample(val, 400)`). Chỉ biến đổi ảnh của bước click (249 bước). Ba chế độ:
  G  gold focus    tâm = điểm chạm vàng (x, y)
  F  false focus   tâm = ((x + W/2) mod W, (y + H/2) mod H), cùng renderer
  C  center focus  tâm = (W/2, H/2), cùng renderer
Chế độ O (ảnh gốc) KHÔNG sinh lại: dùng câu greedy của `runs/c1/c1_mau.jsonl`.

Renderer (hằng số khoá trong report/237 §3, không đổi sau khi thấy số):
  M(u,v) = 0.35 + 0.65·exp(−½((u−x)/(0.18W))² − ½((v−y)/(0.12H))²)
  I'     = M ⊙ I + (1 − M) ⊙ Blur₈(I)        Blur₈ = PIL GaussianBlur(radius=8) trên ảnh gốc
Ảnh giữ nguyên kích thước, lời nhắc dựng y hệt C1 (`build_branch_data.prompt_body` + `SYS`), cùng ngân
sách điểm ảnh và `max_new_tokens=96`. Toạ độ vàng chỉ dùng để chẩn đoán, không phải đầu vào hệ thống.

    python tfvf_g0.py --bundle <BUNDLE> --out /kaggle/working/tfvf_g0_thu.jsonl --n 5
    python tfvf_g0.py --bundle <BUNDLE> --out /kaggle/working/tfvf_g0.jsonl --n 400
    python tfvf_g0.py --bundle <BUNDLE> --chi-ve <THƯ_MỤC> --n 5     # chỉ vẽ ảnh G/F/C, không nạp model

`--n` cắt tiền tố của 400 bước đã chọn rồi mới lọc click. Ghi dần, nối tiếp được. Không mở test.
"""
import os, sys, json, time, random, argparse, hashlib

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = "Qwen/Qwen2.5-VL-3B-Instruct"
SEED_CHON = 20260927
SAN, BIEN = 0.35, 0.65          # sàn mặt nạ · biên độ
SX, SY = 0.18, 0.12             # σ theo bề ngang W và bề dọc H
BLUR = 8                        # bán kính GaussianBlur của PIL, đơn vị pixel ảnh gốc
CHE_DO = [("gold_focus", "G"), ("false_focus", "F"), ("center_focus", "C")]


def tam(mode, x, y, W, H):
    if mode == "G":
        return x, y
    if mode == "F":
        return (x + 0.5 * W) % W, (y + 0.5 * H) % H
    return 0.5 * W, 0.5 * H


def ve(img, cx, cy):
    """img: PIL RGB. Trả ảnh PIL RGB cùng cỡ, vùng quanh (cx, cy) giữ nét, ngoài vùng trộn ảnh mờ."""
    import numpy as np
    from PIL import ImageFilter, Image
    W, H = img.size
    u = np.arange(W, dtype=np.float32)[None, :]
    v = np.arange(H, dtype=np.float32)[:, None]
    M = SAN + BIEN * np.exp(-0.5 * ((u - cx) / (SX * W)) ** 2 - 0.5 * ((v - cy) / (SY * H)) ** 2)
    a = np.asarray(img, dtype=np.float32)
    b = np.asarray(img.filter(ImageFilter.GaussianBlur(radius=BLUR)), dtype=np.float32)
    o = M[..., None] * a + (1.0 - M[..., None]) * b
    return Image.fromarray(np.clip(np.rint(o), 0, 255).astype(np.uint8), "RGB")


def chon(bundle, n):
    va = [json.loads(l) for l in open(os.path.join(bundle, "p1_val_rows.jsonl"), encoding="utf-8")]
    assert len(va) == 1567, f"val phải 1.567 dòng, đang {len(va)}"
    r400 = random.Random(SEED_CHON).sample(va, 400)
    khoa = [(r["episode_id"], r["step_id"]) for r in r400]
    h400 = hashlib.sha256(json.dumps(khoa).encode()).hexdigest()[:16]
    ck = [r for r in r400[:n] if (r.get("action") or {}).get("action_type") == "click"]
    hck = hashlib.sha256(json.dumps([(r["episode_id"], r["step_id"]) for r in r400
                                     if r["action"]["action_type"] == "click"]).encode()).hexdigest()[:16]
    n_ck400 = sum(r["action"]["action_type"] == "click" for r in r400)
    print(f"[dữ liệu] val={len(va)} · 400 bước seed {SEED_CHON} · hash400={h400} · click trong 400 = "
          f"{n_ck400} (kỳ vọng 249) · hash_click={hck} · lượt này: tiền tố {n} ⇒ {len(ck)} click", flush=True)
    assert n_ck400 == 249, "DỪNG: số click trong 400 bước lệch 249"
    return ck


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--out")
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--max-new", type=int, default=96)
    ap.add_argument("--chi-ve", help="chỉ vẽ ảnh G/F/C của các bước click rồi thoát, không nạp model")
    a = ap.parse_args()
    assert os.path.isdir(os.path.join(a.bundle, "adapter_s1_seed101")), "DỪNG: thiếu adapter_s1_seed101"
    print(f"[renderer] M = {SAN} + {BIEN}·exp(−½((u−x)/({SX}W))² − ½((v−y)/({SY}H))²) · "
          f"Blur = GaussianBlur(radius={BLUR}) · F = tâm dời nửa màn (mod W,H) · C = tâm màn", flush=True)
    rows = chon(a.bundle, a.n)
    from PIL import Image

    if a.chi_ve:
        os.makedirs(a.chi_ve, exist_ok=True)
        for r in rows:
            img = Image.open(os.path.join(a.bundle, r["image"])).convert("RGB")
            W, H = img.size
            assert (W, H) == (r["w"], r["h"]), (r["image"], img.size, r["w"], r["h"])
            x, y = r["action"]["x"], r["action"]["y"]
            for _, m in CHE_DO:
                cx, cy = tam(m, x, y, W, H)
                ve(img, cx, cy).save(os.path.join(a.chi_ve, f"ep{r['episode_id']}_s{r['step_id']}_{m}.png"))
            print(f"  vẽ ep{r['episode_id']}_s{r['step_id']} · ({x},{y}) trên {W}×{H}", flush=True)
        print("XONG (chỉ vẽ)", flush=True)
        return

    assert a.out, "cần --out"
    from build_branch_data import prompt_body, SYS
    ocr = {}
    for l in open(os.path.join(a.bundle, "ocr.jsonl"), encoding="utf-8"):
        o = json.loads(l)
        ocr[o["image"]] = o
    done = set()
    if os.path.exists(a.out):
        for l in open(a.out, encoding="utf-8"):
            d = json.loads(l)
            done.add((d["episode_id"], d["step_id"]))
    todo = [r for r in rows if (r["episode_id"], r["step_id"]) not in done]
    print(f"[tiến độ] đã có {len(done)} · còn {len(todo)} · ocr_keys={len(ocr)} · "
          f"thiếu OCR {sum(r['image'] not in ocr for r in rows)}", flush=True)
    if not todo:
        print("Xong sẵn.", flush=True)
        return

    import torch
    from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
    from peft import PeftModel
    import transformers

    dt = torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16
    kw = {("dtype" if int(transformers.__version__.split(".")[0]) >= 5 else "torch_dtype"): dt}
    proc = AutoProcessor.from_pretrained(BASE, min_pixels=200704, max_pixels=1003520)
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(BASE, device_map={"": 0}, **kw)
    model = PeftModel.from_pretrained(model, os.path.join(a.bundle, "adapter_s1_seed101"))
    model.eval()
    gc = model.generation_config
    print(f"[cấu hình] dtype={dt} · greedy do_sample=False · max_new={a.max_new} · "
          f"repetition_penalty(mặc định model)={getattr(gc, 'repetition_penalty', None)} · "
          f"pixels [200704, 1003520] · transformers {transformers.__version__}", flush=True)

    out = open(a.out, "a", encoding="utf-8")
    t0 = time.time()
    for i, r in enumerate(todo):
        rr = {"goal": r["goal"], "history": r.get("history") or []}
        body = prompt_body(rr, ocr.get(r["image"]))
        msg = [{"role": "system", "content": SYS},
               {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body}]}]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.bundle, r["image"])).convert("RGB")
        W, H = img.size
        assert (W, H) == (r["w"], r["h"]), (r["image"], img.size, r["w"], r["h"])
        x, y = r["action"]["x"], r["action"]["y"]
        rec = {"episode_id": r["episode_id"], "step_id": r["step_id"], "action_type": "click",
               "gold": r["target_instruction"]}
        for ten, m in CHE_DO:
            cx, cy = tam(m, x, y, W, H)
            inp = proc(text=[text], images=[ve(img, cx, cy)], return_tensors="pt").to(model.device)
            L = inp["input_ids"].shape[1]
            with torch.no_grad():
                g = model.generate(**inp, max_new_tokens=a.max_new, use_cache=True, do_sample=False,
                                   temperature=None, top_p=None, top_k=None)
            rec[ten] = proc.decode(g[0][L:], skip_special_tokens=True).strip()
        out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        out.flush()
        if (i + 1) % 20 == 0 or i == len(todo) - 1:
            el = time.time() - t0
            print(f"  {i+1}/{len(todo)} · {el/60:.1f} phút · còn ~{el/(i+1)*(len(todo)-i-1)/60:.1f} phút · "
                  f"G: {rec['gold_focus'][:50]!r} · F: {rec['false_focus'][:50]!r}", flush=True)
    out.close()
    print("XONG", flush=True)


if __name__ == "__main__":
    main()
```

## Phụ lục B — `harness/tfvf_g0_doc.py`

```python
# -*- coding: utf-8 -*-
"""Đọc G0 của TFVF (report/237 §5) trên máy nhà, CPU + Java 8 (bộ chấm COCO chính thức).

Luật đạt ghi TRƯỚC khi có số (report/237, 28/9), đọc trên 249 bước click, ba thước quyết định là
BLEU-4 · CIDEr-D · SPICE (BLEU-1..3 không tính thành thước độc lập):
  (1) kênh có tác dụng        câu G khác câu O ở ≥ 10% số bước
  (2) đúng chỗ hơn sai chỗ    G > F ở ≥ 2/3 thước  VÀ  CIDEr-D(G) − CIDEr-D(F) ≥ 3
  (3) hơn prior tâm màn       G > C ở ≥ 2/3 thước
  (4) focus hoàn hảo có ích   G ≥ O ở cả 3 thước  VÀ  G > O ở ≥ 2/3 thước
  Đạt cả bốn ⇒ GO. Không nới sau khi thấy số.
Bảng 400 bước (bước không click giữ câu O cho mọi chế độ) chỉ để xem độ pha loãng, không dùng để quyết.
⚠️ Val là dữ liệu S1 đã thấy lúc dạy ⇒ câu O được ghi nhớ làm đẹp ⇒ điều (4) thiên vị CHỐNG lại việc
đạt. Không trích con số nào ra báo hay luận văn.

Chạy:  ~/.venvs/thesis/bin/python harness/tfvf_g0_doc.py <tfvf_g0.jsonl> [runs/c1/c1_mau.jsonl]
          [--json runs/tfvf_g0/g0_doc.json] [--bo-spice]
"""
import argparse, glob, json, os

J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
if J and "JAVA_HOME" not in os.environ:
    os.environ["JAVA_HOME"] = J[-1]
    os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.meteor.meteor import Meteor
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.cider.cider import Cider
from pycocoevalcap.spice.spice import Spice

MODES = ["O", "G", "F", "C"]
TRUONG = {"G": "gold_focus", "F": "false_focus", "C": "center_focus"}
QUYET = ["bleu4", "cider_d", "spice"]
COT = ["bleu1", "bleu2", "bleu3", "bleu4", "meteor", "rougeL", "cider_d", "spice"]


def cham(gold, hyp, bo_spice):
    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(gold)})
    c = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(hyp)})
    o = {}
    b, _ = Bleu(4).compute_score(g, c, verbose=0)
    for k in range(4):
        o[f"bleu{k+1}"] = 100 * b[k]
    o["meteor"] = 100 * Meteor().compute_score(g, c)[0]
    o["rougeL"] = 100 * Rouge().compute_score(g, c)[0]
    o["cider_d"] = 100 * Cider().compute_score(g, c)[0]
    o["spice"] = float("nan") if bo_spice else 100 * Spice().compute_score(g, c)[0]
    return o


def in_bang(ten, n, S):
    print(f"\n=== {ten} (n={n}) ===")
    print("chế độ " + " ".join(f"{c:>8s}" for c in COT))
    for m in MODES:
        print(f"{m:6s} " + " ".join(f"{S[m][c]:8.2f}" for c in COT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kq")
    ap.add_argument("c1", nargs="?", default="runs/c1/c1_mau.jsonl")
    ap.add_argument("--json")
    ap.add_argument("--bo-spice", action="store_true", help="chỉ để thử đường đọc; quyết định cần SPICE")
    a = ap.parse_args()

    C1 = [json.loads(l) for l in open(a.c1, encoding="utf-8")]
    K = [json.loads(l) for l in open(a.kq, encoding="utf-8")]
    assert len(C1) == 400 and len({(d["episode_id"], d["step_id"]) for d in C1}) == 400, "C1 phải 400 khoá riêng"
    ck = [d for d in C1 if d["action_type"] == "click"]
    assert len(ck) == 249, f"C1 phải có 249 click, thấy {len(ck)}"
    kq = {(d["episode_id"], d["step_id"]): d for d in K}
    assert len(kq) == len(K), "tệp kết quả có khoá trùng"
    thieu = [(d["episode_id"], d["step_id"]) for d in ck if (d["episode_id"], d["step_id"]) not in kq]
    assert not thieu, f"thiếu {len(thieu)}/249 bước click, ví dụ {thieu[:3]} — chạy nối tiếp cho đủ"
    assert set(kq) == {(d["episode_id"], d["step_id"]) for d in ck}, "tệp kết quả có khoá ngoài 249 click"
    for d in ck:
        r = kq[(d["episode_id"], d["step_id"])]
        assert r["gold"] == d["gold"], f"câu chuẩn lệch ở {(d['episode_id'], d['step_id'])}"
        for t in TRUONG.values():
            assert isinstance(r.get(t), str), f"thiếu trường {t} ở {(d['episode_id'], d['step_id'])}"
    print(f"[khớp] 400 khoá C1 · 249 click · kết quả {len(K)} dòng · câu chuẩn khớp tuyệt đối 249/249")

    def cau(d, m):
        if m == "O" or d["action_type"] != "click":
            return d["greedy"]
        return kq[(d["episode_id"], d["step_id"])][TRUONG[m]]

    rong = {m: sum(not cau(d, m) for d in ck) for m in MODES}
    print("câu rỗng trên 249 click:", rong)

    kqua = {}
    for ten, tap in [("249 click", ck), ("400 bước (không click giữ O)", C1)]:
        gold = [d["gold"] for d in tap]
        S = {m: cham(gold, [cau(d, m) for d in tap], a.bo_spice) for m in MODES}
        in_bang(ten, len(tap), S)
        kqua[ten] = S

    khac = {f"G≠{m}": sum(cau(d, "G") != cau(d, m) for d in ck) for m in ["O", "F", "C"]}
    print("\nsố bước câu khác nhau (249 click): " +
          " · ".join(f"{k} {v} ({100*v/249:.1f}%)" for k, v in khac.items()))

    S = kqua["249 click"]
    hon = lambda p, q: sum(S[p][c] > S[q][c] for c in QUYET)
    dk1 = khac["G≠O"] / 249 >= 0.10
    dk2 = hon("G", "F") >= 2 and S["G"]["cider_d"] - S["F"]["cider_d"] >= 3
    dk3 = hon("G", "C") >= 2
    dk4 = all(S["G"][c] >= S["O"][c] for c in QUYET) and hon("G", "O") >= 2
    print("\nĐiều kiện GO (249 click; thước quyết định BLEU-4 · CIDEr-D · SPICE):")
    print(f"  (1) G≠O ≥ 10%: {100*khac['G≠O']/249:.1f}% ⇒ {'ĐẠT' if dk1 else 'KHÔNG ĐẠT'}")
    print(f"  (2) G>F ở {hon('G','F')}/3 thước, ΔCIDEr-D(G−F) = {S['G']['cider_d']-S['F']['cider_d']:+.2f} ⇒ "
          f"{'ĐẠT' if dk2 else 'KHÔNG ĐẠT'}")
    print(f"  (3) G>C ở {hon('G','C')}/3 thước ⇒ {'ĐẠT' if dk3 else 'KHÔNG ĐẠT'}")
    print(f"  (4) G≥O cả 3: {all(S['G'][c] >= S['O'][c] for c in QUYET)} · G>O ở {hon('G','O')}/3 ⇒ "
          f"{'ĐẠT' if dk4 else 'KHÔNG ĐẠT'}")
    if dk1 and dk2 and dk3 and dk4:
        phan = "GO — TFVF phù hợp; được thiết kế pilot có train"
    elif not dk1:
        phan = "DỪNG — S1 gần như không phản ứng với renderer (trượt 1)"
    elif not (dk2 and dk3):
        phan = "DỪNG — S1 phản ứng với biến đổi ảnh nhưng không theo đúng vị trí (trượt 2 hoặc 3)"
    else:
        phan = "DỪNG — focus chứa tín hiệu nhưng lệch phân phối làm hại S1 (trượt 4); không tự mở SFT để cứu"
    print("\nG0 =", phan)
    if a.bo_spice:
        print("⚠️ chạy --bo-spice: SPICE = nan nên phán quyết trên KHÔNG hợp lệ, chỉ để thử đường đọc")

    if a.json:
        os.makedirs(os.path.dirname(a.json) or ".", exist_ok=True)
        kqua = {t: {m: {c: float(v) for c, v in s.items()} for m, s in S_.items()} for t, S_ in kqua.items()}
        json.dump({"bang": kqua, "khac": khac, "dieu_kien": [bool(x) for x in (dk1, dk2, dk3, dk4)],
                   "phan_quyet": phan,
                   "bo_spice": a.bo_spice, "nguon": [a.kq, a.c1]},
                  open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("ghi", a.json)


if __name__ == "__main__":
    main()
```
