# Chấm s1/seed202 trên Kaggle — từng bước

**Đây là đường găng.** Cặp hạt giống S1 là *null thực nghiệm*: nó cho biết hai lượt train khác
nhau bao nhiêu **khi không có can thiệp nào**. Không có con số đó thì không phân biệt được
"S2 hơn S1" với "hai lượt train vốn đã khác nhau", nên **không khoá được ngưỡng** và không train
S2 được.

· **Thời gian:** ~5,6 giờ · **Tiền:** 0 đồng · **Quota tuần này còn ~18/30 giờ.**

---

## Bước 0 — đã kiểm xong ở máy nhà, 8/8 ĐẠT

```
python3 harness/kiem_preds.py runs/preds_s1_seed202.jsonl
```

| | |
|---|---|
| 6.958 bản ghi, khớp khoá tập kiểm, 0 trùng lặp | ✔ |
| **bước bị bỏ = `(18710, 1)`, TRÙNG KHÍT seed101** | ✔ ⇒ cùng 4.462 bước, ghép cặp sạch |
| chữ ký `lora:s1_seed202`, chỉ một | ✔ ⇒ không lẫn lượt khác |
| 63,0% câu trùng nguyên văn seed101 | ✔ ⇒ đúng là mô hình khác, không phải tệp copy |
| trung vị 33 ký tự · 87,0% mở đầu bằng động từ chạm | ✔ (seed101: 33 · 87,5%) |

Đây là phép kiểm rẻ nhất trong cả quy trình: **vài giây để chặn một lỗi tốn 5,6 giờ.**

---

## Bước 1 — đưa tệp lên Kaggle

Tệp duy nhất cần upload: **`runs/preds_s1_seed202.jsonl`** (2,3 MB).

1. Mở dataset **`thesis-preds`** → **New Version**.
2. Kéo `preds_s1_seed202.jsonl` vào, **giữ nguyên các tệp cũ** (đừng xoá `kaggle_16_8/`).
3. Create. Đợi Kaggle xử lý xong (~1 phút).
4. Trong notebook, panel Input → bấm cập nhật dataset lên version mới.

⚠️ Không cần upload gì khác. Ảnh và `test.jsonl` đã nằm ở dataset `thesis-score`.

---

## Bước 2 — ô 0: kiểm GPU (5 giây)

```python
import torch, subprocess
print("có GPU:", torch.cuda.is_available(),
      "|", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "—")
assert torch.cuda.is_available(), "DỪNG: đang chạy CPU. Bật Accelerator = GPU T4 ×2."
```

Panel Accelerator hay tự trả về *None* khi mở lại notebook. 5 giây kiểm, thay vì phát hiện sau
nhiều giờ.

---

## Bước 3 — ô 1: nối dữ liệu và tìm tệp preds

```python
import os, glob, json, shutil, random

WS = "/kaggle/working"

# tìm tệp preds mới upload — dò theo TÊN, không nướng cứng đường dẫn
cand = glob.glob("/kaggle/input/**/preds_s1_seed202.jsonl", recursive=True)
assert cand, "DỪNG: chưa thấy preds_s1_seed202.jsonl. Đã cập nhật dataset lên version mới chưa?"
PREDS = cand[0]
print("preds:", PREDS)

# tìm gói mã
mp = glob.glob("/kaggle/input/**/harness/score_run.py", recursive=True)
assert mp, "DỪNG: không thấy harness/score_run.py trong dataset"
PKG = os.path.dirname(os.path.dirname(mp[0]))

# chọn gói có ĐỦ CẢ HAI: test.jsonl đủ dòng và ảnh đủ nhiều, CÙNG một chỗ
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

shutil.copytree(f"{PKG}/harness", f"{WS}/harness", dirs_exist_ok=True)
dst = f"{WS}/harness/dg1_cache/test_ac"
os.makedirs(dst, exist_ok=True)
for src, name in [(TEST_JSONL, "test.jsonl"), (os.path.join(ROOT, "images"), "images")]:
    link = os.path.join(dst, name)
    if os.path.islink(link): os.remove(link)
    elif os.path.isdir(link): shutil.rmtree(link)
    elif os.path.exists(link): os.remove(link)
    os.symlink(src, link)

# ── kiểm lại NGAY TRÊN KAGGLE, đúng ba thứ quyết định con số ──────────────────────
recs = [json.loads(l) for l in open(f"{dst}/test.jsonl", encoding="utf-8")]
taps = [r for r in recs if r["action"].get("action_type") in ("click", "long_press")
        and "x" in r["action"]]
miss = sum(1 for r in taps if not os.path.exists(os.path.join(dst, r["image"])))
assert len(taps) == 4463 and miss == 0, f"DỪNG: {len(taps)} bước chạm, thiếu {miss} ảnh"
assert "app_seen_in_train" in recs[0], "DỪNG: test.jsonl CHƯA gắn nhãn app — lát cắt phụ sẽ rỗng"

P = {}
for l in open(PREDS, encoding="utf-8"):
    o = json.loads(l); P[(o["episode_id"], o["step_id"])] = o
sig = {o.get("run") for o in P.values() if o.get("run")}
rong = [k for k in P if k in {(r["episode_id"], r["step_id"]) for r in taps}
        and not str(P[k].get("pred", "")).strip()]
assert len(P) == 6958, f"DỪNG: preds có {len(P)} bản ghi, cần 6958"
assert sig == {"lora:s1_seed202"}, f"DỪNG: chữ ký {sig}, cần đúng lora:s1_seed202"
assert rong == [(18710, 1)], f"DỪNG: bước rỗng {rong}, cần đúng [(18710, 1)] như seed101"
print(f"\npreds {len(P)} · chữ ký {sig} · bước rỗng {rong}")
print("✔ SẴN SÀNG — sẽ chấm 4.462 bước, cùng quần thể với seed101/Base/trần")
```

Ba dòng `assert` cuối là chỗ đáng giá nhất: chúng lặp lại phép kiểm ở máy nhà **trên đúng tệp
Kaggle sẽ đọc**, nên bắt được cả trường hợp upload sai tệp hay dataset version chưa cập nhật.

---

## Bước 4 — ô 2: chấm (~5,6 giờ)

```python
import os, subprocess, time, json

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"   # thủ phạm làm treo lượt 17/8
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["PYTHONUNBUFFERED"] = "1"
RAC = ("it/s", "s/it", "it]")

def chay(ten, preds, nhip=15):
    log = f"{WS}/log_{ten}.txt"
    with open(log, "w") as fw:
        p = subprocess.Popen(
            ["python", "-u", f"{WS}/harness/score_run.py", "--mode", "score",
             "--grounder", "uground", "--preds", preds,
             "--out", f"{WS}/score_{ten}.json"],
            stdout=fw, stderr=subprocess.STDOUT)   # ghi ra ĐĨA, không qua ống log Kaggle
        t0 = tlast = time.time(); dem, du = 0, ""
        with open(log) as fr:
            while True:
                *dong, du = (du + fr.read()).split("\n")
                for l in dong:
                    if any(k in l for k in RAC): continue
                    dem += 1
                    if dem <= 3000 or "bước/giây" in l:
                        print(l, flush=True); tlast = time.time()
                if p.poll() is not None: break
                if time.time() - tlast > 120:
                    print(f"  [{time.strftime('%H:%M:%S')}] {ten} · "
                          f"{(time.time()-t0)/60:.0f} phút · vẫn đang chạy", flush=True)
                    tlast = time.time()
                time.sleep(nhip)
    print(f"── {ten} xong · mã thoát {p.returncode} · {(time.time()-t0)/60:.0f} phút", flush=True)
    return p.returncode

chay("s1_seed202", PREDS)
```

**Không có `--n`** ⇒ chấm đủ 4.463 bước (bỏ 1 câu rỗng còn 4.462).

**Mốc để biết nó sống:** sau 4 phút phải có ít nhất một dòng. Tốc độ ~0,22 bước/giây ⇒ mong đợi
`x/4463` tăng đều, xong sau ~5,6 giờ.

⚠️ **Bảo hiểm cho lượt dài:** ở khoảng **giữa (~3 giờ)**, mở một ô khác và tải
`score_s1_seed202_raw.jsonl` (bản dở) về máy. `score_run.py` **ghi dần và nối tiếp được**, nên
nếu phiên chết thì đưa tệp dở đó lên dataset rồi chạy lại — nó chấm tiếp chứ không từ đầu.
Không có bản bảo hiểm này thì phiên chết ở giờ thứ 5 là mất 5 giờ quota.

---

## Bước 5 — ô 3: đọc kết quả và đối chiếu ngay

```python
r = json.load(open(f"{WS}/score_s1_seed202.json"))
e, ci = r["exec_voronoi"]*100, [c*100 for c in r["ci_voronoi"]]
print(f"s1/seed202: {e:.1f}%  KTC95 [{ci[0]:.1f} – {ci[1]:.1f}]  n={r.get('n','?')}")
print(f"s1/seed101: 59.1%      KTC95 [57.3 – 60.8]")
print(f"chênh giữa hai HẠT GIỐNG: {e-59.1:+.1f} pp  ← đây là NHIỄU, không phải hiệu ứng")
print("\nĐọc:")
print("  |chênh| < 2 pp  → nhiễu nhỏ, ngưỡng cho S2 giữ ~2,2 pp, thí nghiệm còn đọc được")
print("  |chênh| 2–4 pp  → nhiễu bằng cỡ hiệu ứng kỳ vọng ⇒ phải nâng ngưỡng, và nói rõ")
print("  |chênh| > 4 pp  → ⛔ nhiễu ăn hết dư địa; S2 một hạt giống KHÔNG kết luận được gì")
```

**Mong đợi:** quanh **59%**, chênh dưới 2 pp. Nếu ra dưới 50% hay trên 70% thì nghi hỏng đường
ống chứ không phải tính chất mô hình — 63% câu của nó trùng nguyên văn seed101, nên điểm không
thể lệch xa thế.

---

## Bước 6 — tải về và tính MDE thật

Tải **cả hai** từ panel Output vào `runs/`:

- `score_s1_seed202.json`
- `score_s1_seed202_raw.jsonl` ← quan trọng hơn: đổi luật chấm hay thêm lát cắt thì tính lại
  từ đây, **không gọi lại bộ trỏ**

Rồi ở máy nhà:

```bash
python3 harness/kiem_preds.py runs/preds_s1_seed202.jsonl   # đã 8/8, chỉ để có vết
python3 harness/phep_a_ghep_cap.py                          # phép A, không đổi
```

Việc tiếp theo sau khi có số: **MDE thật từ cặp hạt giống** → **khoá ngưỡng vào `report/106`
mục sửa đổi** → **mới** train S2. Trình tự này cứng, khoá ở `report/106` mục 5.
