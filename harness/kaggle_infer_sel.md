# Kaggle — suy luận nhánh `gui_sel` và cổng G6

Viết 3/9/2026. Dùng cho **cả sáu lượt** của sprint SOICT, và cho cổng G6 trước.
Máy: **T4×2 miễn phí**, hạn mức 30 giờ GPU/tuần. Không tiêu compute unit của Colab.

⚠️ Vì sao Kaggle chứ không Colab: suy luận không có backward pass nên không cần A100.
Sáu lượt × 6.958 bước trên A100 là ~372 compute unit; trên Kaggle là **0 đồng**.
Lượt G6 (1.400 bước, ~2,3 giờ) đóng thêm vai **phép thử rẻ cho runbook sẽ dùng sáu lần**.

## Ba Input phải gắn vào notebook

| dataset | có gì | ghi chú |
|---|---|---|
| `thesis-score` | 4.463 ảnh tập kiểm + `test.jsonl` | **đã có sẵn**, không cần làm gì |
| `thesis-sel-infer` | `_bundles/thesis_sel_infer.zip` — mã + 4 tệp jsonl (4,3 MB) | tạo mới |
| `gui-sel-adapter` | `adapter_model.safetensors` + `adapter_config.json` từ Drive | tạo mới, ~60 MB |

⛔ Adapter lấy ở **thư mục gốc** `gui_sel_seed101/`, KHÔNG lấy trong `checkpoint-*` —
thư mục gốc là bản sau đủ 4.036 bước, checkpoint là bản dở.

Settings: **Accelerator GPU T4×2** · **Internet ON** (phải tải Qwen2.5-VL-3B từ HuggingFace).

---

## Ô 0 — NHÌN THẤY GÌ TRONG INPUT, chạy đầu tiên

Không assert gì, chỉ liệt kê. Mục đích là thấy tận mắt ba dataset đã gắn đúng chưa, trước
khi bất cứ ô nào kịp báo lỗi khó hiểu.

```python
import glob, os
for d in sorted(glob.glob("/kaggle/input/*")):
    n = sum(len(f) for _, _, f in os.walk(d))
    print(f"\n■ {os.path.basename(d)}  ({n} tệp)")
    for r, _, fs in os.walk(d):
        for f in sorted(fs)[:6]:
            p = os.path.join(r, f)
            print(f"    {os.path.getsize(p)/1e6:8.2f} MB  {p.replace(d+'/', '')}")
        if len(fs) > 6:
            print(f"    … và {len(fs)-6} tệp nữa trong {r.replace(d+'/', '') or '.'}")
        break
```

Phải thấy đủ ba khối:

| khối | dấu hiệu đúng |
|---|---|
| ảnh tập kiểm | ~4.463 tệp `.png` |
| mã + jsonl | `harness/infer_branch.py`, `candidates.jsonl` ~7,9 MB |
| adapter | `adapter_model.safetensors` ~60 MB + `adapter_config.json` |

⛔ Thấy `adapter_model.safetensors` chỉ vài KB nghĩa là tải nhầm con trỏ Git LFS chứ không
phải trọng số. Tải lại từ Drive.

---

## Ô 1 — cài gói

```python
!pip -q install -U "transformers>=4.49" accelerate peft qwen-vl-utils 2>&1 | tail -2
import torch, transformers, peft
print(transformers.__version__, peft.__version__, torch.cuda.get_device_name(0))
```

---

## Ô 2 — dựng workspace

⚠️ **Kaggle TỰ GIẢI NÉN file zip khi tạo dataset** — trong `/kaggle/input` không có tệp
`.zip` nào, chỉ có cây thư mục `harness/`. Ô này tìm theo `infer_branch.py`, không tìm zip.

```python
import os, glob, json, shutil
WS = "/kaggle/working/ws"; os.makedirs(WS, exist_ok=True)

# ⛔ CÓ NHIỀU BẢN `harness/` trong /kaggle/input — `thesis-score` cũng mang một bản cũ.
#    Lấy bản đầu tiên glob trả về là ăn phải bản cũ, và lỗi chỉ lộ ra ở dòng lệnh
#    `unrecognized arguments` sau khi đã tưởng chạy xong. Chọn theo NỘI DUNG, không theo tên.
CAN = "--force-sel"        # dấu vân tay của bản mã hiện hành, đổi khi thêm cờ mới
src = glob.glob("/kaggle/input/**/harness/infer_branch.py", recursive=True)
assert src, "DỪNG: chưa thấy harness/infer_branch.py trong /kaggle/input"
ok = []
for q in src:
    co = CAN in open(q, encoding="utf-8", errors="ignore").read()
    print(("  ✅" if co else "  ⛔ bản cũ"), q)
    if co: ok.append(q)
assert ok, (f"DỪNG: không bản nào chứa {CAN!r}. Dataset chưa lên version mới, "
            "hoặc Input chưa trỏ sang version đó (panel Input ▸ chọn version mới nhất).")
PKG = os.path.dirname(ok[0])
shutil.rmtree(f"{WS}/harness", ignore_errors=True)
shutil.copytree(PKG, f"{WS}/harness")
print("mã lấy từ:", PKG, "·", len(glob.glob(f"{WS}/harness/*.py")), "tệp .py")
# in ra CỜ THẬT mà mã trong WS hiểu — đọc dòng này, đừng tin lệnh mình vừa gõ
import subprocess
u = subprocess.run(["python", f"{WS}/harness/infer_branch.py", "--help"],
                   capture_output=True, text=True).stdout
print("cờ có sẵn:", [c for c in ("--force-sel", "--only", "--cands") if c in u])

# ảnh: symlink từ thesis-score, KHÔNG chép (4.463 tệp)
best = None
for t in glob.glob("/kaggle/input/**/test_ac/images", recursive=True):
    n = len(glob.glob(os.path.join(t, "*.png")))
    print(f"  {n:5d} ảnh  {t}")
    if n >= 4400 and (best is None or n > best[1]):
        best = (t, n)
assert best, "DỪNG: không gói nào đủ 4.463 ảnh"
dst = f"{WS}/harness/dg1_cache/test_ac/images"
if os.path.islink(dst): os.remove(dst)
elif os.path.isdir(dst): shutil.rmtree(dst)
os.symlink(best[0], dst)

AD = os.path.dirname(glob.glob("/kaggle/input/**/adapter_config.json", recursive=True)[0])
print("adapter:", AD, os.path.getsize(f"{AD}/adapter_model.safetensors")/1e6, "MB")
```

---

## Ô 3 — TIỀN BAY, năm phép, chạy trước khi tiêu GPU

```python
import json, sys, os
sys.path.insert(0, f"{WS}/harness")
R = f"{WS}/harness/dg1_cache/test_ac"

recs = [json.loads(l) for l in open(f"{R}/test.jsonl", encoding="utf-8")]
cand = {}
for l in open(f"{R}/candidates.jsonl", encoding="utf-8"):
    c = json.loads(l); cand[c["image"]] = c["cands"]

print("① test.jsonl        :", len(recs), "← cần 6.958")
print("② candidates        :", len(cand), "màn")
print("③ ảnh mở được       :", os.path.exists(os.path.join(R, recs[0]["image"])))
print("④ adapter có LoRA   :", json.load(open(f"{AD}/adapter_config.json"))["r"], "rank")

# ⑤ CÂU NHẮC PHẢI CÓ KHỐI ỨNG VIÊN — quên cờ --cands là hỏng câm, 499/500 mẫu sai
import build_branch_data as BB
ocr = {}
for l in open(f"{R}/ocr.jsonl", encoding="utf-8"):
    o = json.loads(l); ocr[o["image"]] = o
r0 = recs[0]
p_co  = BB.prompt_body(r0, ocr.get(r0["image"]), cands=cand.get(r0["image"]))
p_khg = BB.prompt_body(r0, ocr.get(r0["image"]), cands=None)
print("⑤ câu nhắc CÓ menu  :", len(p_co) > len(p_khg), f"({len(p_khg)} -> {len(p_co)} ký tự)")
```

⛔ Phép ⑤ là phép quan trọng nhất. Đo 2/9: chấm `gui_sel` mà quên `--cands` thì
**499/500 mẫu dựng sai câu nhắc** — mô hình được dạy chọn từ menu, lúc chấm không thấy menu
nào. Nó vẫn sinh chữ, thước vẫn ra điểm, log không báo gì.

---

## Ô 4 — SUY LUẬN

```python
import subprocess, os
LOG = "/kaggle/working/infer_sel.log"
f = open(LOG, "a")
env = {**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1"}
P = subprocess.Popen(
    ["python", f"{WS}/harness/infer_branch.py",
     "--adapter", AD,
     "--out", "/kaggle/working/preds_gui_sel_seed101_dev1400.jsonl",
     "--cands", f"{WS}/harness/dg1_cache/test_ac/candidates.jsonl",
     "--limit", "1400"],
    stdout=f, stderr=subprocess.STDOUT, start_new_session=True, env=env, cwd=WS)
print("PID", P.pid, "· log", LOG)
```

⚠️ `TQDM_DISABLE=1` là bắt buộc trên Kaggle: `tqdm` ngoài terminal in mỗi cập nhật thành
một dòng riêng (>1.400 dòng chỉ để nạp mô hình), Kaggle chặn log khi vượt trần rồi tiến
trình **kẹt cứng ở lệnh ghi stdout**. Đã treo 7 giờ vì đúng chuyện này.

**Vì sao 1.400:** G6 cần 600 bước **có ứng viên vàng**, không phải 600 bước bất kỳ. Đếm thật
trên tập kiểm (0 GPU): 600 bước đầu chỉ cho **284**, 1.000 cho **492**, **1.400 cho 694**.

### Ô theo dõi

```python
import time, os
for _ in range(400):
    n = sum(1 for _ in open("/kaggle/working/preds_gui_sel_seed101_dev1400.jsonl")) \
        if os.path.exists("/kaggle/working/preds_gui_sel_seed101_dev1400.jsonl") else 0
    print(time.strftime("%H:%M:%S"), f"{n}/1400", flush=True)
    if n >= 1400: break
    time.sleep(120)
```

---

## Ô 4b — SOI TỆP PREDS trước khi chấm

Ba phép, mất hai giây, chặn đúng loại lỗi đã mắc 3/9.

```python
import json, collections
P = "/kaggle/working/preds_gui_sel_seed101_dev1400.jsonl"
rs = [json.loads(l) for l in open(P, encoding="utf-8")]
print("① số bản ghi        :", len(rs))
print("② chữ ký lượt chạy  :", collections.Counter(r.get("run") for r in rs).most_common())
co = sum(1 for r in rs if "<sel>" in (r.get("raw") or ""))
print(f"③ raw CÓ thẻ <sel>  : {co}/{len(rs)} = {co/len(rs):.1%}")
print("\n── một mẫu ──")
print("raw :", repr(rs[0].get("raw"))[:200])
print("pred:", repr(rs[0].get("pred"))[:200])
```

⛔ **Phép ③ là phép quan trọng nhất, và nó phải đọc `raw` chứ không phải `pred`.**
`infer_branch.strip_desc()` bóc cả `<desc>` lẫn `<sel>` khỏi `pred` — đúng như thiết kế, vì
câu đem chấm không được chứa đáp án cho bộ trỏ. Cổng G6 tìm thẻ trong `pred` sẽ ra **0,0% ở
mọi cột** và trông y hệt mô hình không học được gì. Đã mắc đúng vậy ở lượt chấm đầu tiên
ngày 3/9; đã vá trong `gate_sel_acc.py`, nhưng nếu dataset trên Kaggle còn bản cũ thì vá tại
chỗ bằng ô dưới.

```python
import re, pathlib
f = pathlib.Path(f"{WS}/harness/gate_sel_acc.py"); t = f.read_text(encoding="utf-8")
if 'r.get("raw")' not in t:
    t = t.replace('tach_sel(r.get("pred") or r.get("prediction") or "")',
                  'tach_sel(r.get("raw") or r.get("pred") or r.get("prediction") or "")')
    f.write_text(t, encoding="utf-8")
# ⛔ Không tin lệnh vừa gõ — in ra dòng THẬT trong tệp để mắt đọc
print([l.strip() for l in f.read_text(encoding="utf-8").split("\n") if "tach_sel(r.get" in l])
```

---

## Ô 5 — CỔNG G6

```python
!cd {WS} && SEL_SPLIT=test python harness/gate_sel_acc.py \
    /kaggle/working/preds_gui_sel_seed101_dev1400.jsonl
```

⛔ `SEL_SPLIT=test` là **bắt buộc**. Mặc định của script là `train`, mà `infer_branch.py`
chỉ chạy trên tập kiểm ⇒ khoá không khớp ⇒ cổng in `⛔ BỎ QUA TOÀN BỘ` và trông như dữ liệu
hỏng, trong khi thật ra chỉ là lệch split.

**Luật đọc, khoá từ `report/132` §5 trước khi train:**

| `sel_acc` | phán |
|---|---|
| **≥ 63,6%** | ĐẠT — chạy tiếp năm lượt còn lại |
| **< 63,6%** | TRƯỢT — dừng cả sprint, bài đổi thành báo cáo âm |

⛔ **Không nới ngưỡng sau khi thấy điểm.** Dự án đã tự khai hai lần làm vậy; lần thứ ba là
mất hẳn lập luận đăng ký trước.

⚠️ **Phải khai trong bài:** G6 đo trên lát 1.400 bước của **tập kiểm**, tức một lần nhìn tập
kiểm trước khi hoàn tất sprint. Giảm nhẹ được vì `sel_acc` là thước phụ (headline vẫn là
`exec`), và quyết định chỉ là dừng-hay-chạy-tiếp chứ không phải chọn điểm lưu hay dời ngưỡng.

---

## Ô 6 — PHÉP THỬ ÉP CHỌN (chẩn đoán, sau khi G6 trượt 3/9)

**Câu hỏi:** 273 bước bỏ cuộc là do mô hình *dè dặt quá mức* hay *thật sự không biết*?
Hai giả thuyết dẫn tới hai hướng chữa khác hẳn nhau, và phân biệt được bằng ~27 phút.

```python
import subprocess, os
LOG = "/kaggle/working/forcesel.log"
f = open(LOG, "a")
env = {**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1"}
P = subprocess.Popen(
    ["python", f"{WS}/harness/infer_branch.py",
     "--adapter", AD,
     "--out", "/kaggle/working/preds_gui_sel_forcesel_273.jsonl",
     "--cands", f"{WS}/harness/dg1_cache/test_ac/candidates.jsonl",
     "--only",  f"{WS}/harness/dg1_cache/test_ac/bo_cuoc_273.jsonl",
     "--force-sel"],
    stdout=f, stderr=subprocess.STDOUT, start_new_session=True, env=env, cwd=WS)
print("PID", P.pid, "· log", LOG)
```

Hai dòng phải thấy trong log, đọc chúng chứ đừng tin lệnh vừa gõ:

```
--only: 6958 -> 273 bước (danh sách có 273 khoá)
ÉP CHỌN: cấm 6 chuỗi token của 'none'
```

### Ô theo dõi ép chọn — có ETA và `sel_acc` tạm thời

```python
import time, os, sys, json
WSH = f"{WS}/harness"; sys.path.insert(0, WSH)
import build_sel_data as BS, gate_sel_acc as G
BS.D.set_split("test"); R = BS.D.ROOT

gold, cands = {}, {}
for l in open(os.path.join(R, "descriptors.jsonl"), encoding="utf-8"):
    d = json.loads(l); gold[G.kh(d)] = d
for l in open(os.path.join(R, "candidates.jsonl"), encoding="utf-8"):
    c = json.loads(l); cands[G.kh(c)] = c["cands"]

P, LOG, N = "/kaggle/working/preds_gui_sel_forcesel_273.jsonl", "/kaggle/working/forcesel.log", 273
t0, truoc, xn = None, 0, False

def cham(rs):
    """sel_acc tạm thời trên những bước ĐÃ sinh — cùng luật với cổng G6."""
    n = d = non = 0
    for r in rs:
        k = G.kh(r); g, cs = gold.get(k), cands.get(k)
        if not (g and g.get("name") and cs):
            continue
        gx, gy = g["point_norm"]; gc = BS.gold_candidate(cs, g["name"], gx, gy)
        if gc is None:
            continue
        n += 1
        ten, x, y = G.tach_sel(r.get("raw") or "")
        if ten == "none":
            non += 1; continue
        if (G.chuan(ten) == G.chuan(gc["name"]) and x is not None
                and abs(x - gc["x"]) <= G.TOL and abs(y - gc["y"]) <= G.TOL):
            d += 1
    return n, d, non

for _ in range(90):
    if not xn and os.path.exists(LOG):
        for dd in open(LOG, encoding="utf-8", errors="ignore").read().split("\n"):
            if dd[:7] in ("--only:", "ÉP CHỌN") or dd.startswith("khối ứng viên:"):
                print("  ✔", dd, flush=True); xn = True

    rs = []
    if os.path.exists(P):
        for l in open(P, encoding="utf-8"):
            try: rs.append(json.loads(l))
            except Exception: pass
    n = len(rs)
    gio = time.strftime("%H:%M:%S", time.gmtime(time.time() + 7*3600))

    if n == 0:
        print(f"{gio}  [nạp mô hình] 0/{N}", flush=True)
    else:
        # tốc độ NEO vào mốc đầu tiên rồi chia cả quãng, không dùng cửa sổ liền trước
        # (cửa sổ ngắn cho ra răng cưa: 9 rồi 12 rồi 9 s/bước, ETA nhảy hàng giờ)
        if t0 is None: t0, n0 = time.time(), n
        dt = time.time() - t0
        toc = (n - n0) / dt if dt > 0 and n > n0 else 0          # bước/giây
        if toc:
            con = int((N - n) / toc)
            sp = (f"{1/toc:5.1f}s/b  còn {con//60:>3}m  "
                  f"xong ~{time.strftime('%H:%M', time.gmtime(time.time()+7*3600+con))}")
        else:
            con, sp = 0, "    ?s/b  còn   ?m  xong ~ ?   "   # chưa đủ hai mốc để đo
        nc, du, non = cham(rs)
        print(f"{gio}  {n:>3}/{N} ({n*100//N:>2}%) +{n-truoc:<3} {sp}  │ "
              f"none {non/nc if nc else 0:5.1%}  sel_acc tạm {du}/{nc} = "
              f"{du/nc if nc else 0:5.1%}", flush=True)
        truoc = n
    if n >= N:
        print("✅ XONG", flush=True); break
    time.sleep(60)
```

Ra dạng:

```
  ✔ khối ứng viên: 6958 màn ← nhánh CÓ menu (gui_sel / gui_sft_match)
  ✔ --only: 6958 -> 273 bước (danh sách có 273 khoá)
  ✔ ÉP CHỌN: cấm 6 chuỗi token của 'none'
16:47:11  [nạp mô hình] 0/273
16:52:11   24/273 ( 8%) +24    5.9s/b  còn  24m  xong ~17:16  │ none  0.0%  sel_acc tạm 18/24 = 75.0%
```

**Sáu thứ đọc được, và hai thứ đầu quan trọng hơn cả ETA:**

| cột | phải là gì | sai thì sao |
|---|---|---|
| ba dòng `✔` | hiện trong 5 phút đầu | thiếu `ÉP CHỌN` ⇒ dataset còn mã cũ, **dừng ngay** |
| `none` | **0,0%** suốt lượt | khác 0 ⇒ ép chọn không có hiệu lực, số vô nghĩa |
| `sel_acc tạm` | hội tụ dần | đây chính là câu trả lời, thấy trước khi chạy xong |
| `+N` | ~10 bước mỗi phút | `+0` ba lần liền ⇒ nghi treo |
| `s/b` · `còn` · `xong ~` | ETA, giờ Việt Nam | — |

⚠️ Suy luận chạy theo **lô 8 ảnh** (~48 giây một lô), nên với `sleep 10` sẽ thấy bốn dòng
`+0` rồi một dòng `+8`. Đó không phải treo. Để `sleep 60` thì mỗi dòng tăng đều ~10 bước.

⚠️ `sel_acc tạm` trên vài chục bước đầu **dao động mạnh** — 24 bước thì một ca đổi chiều đã
là 4 điểm. Chỉ đọc nghiêm túc từ khoảng 150 bước trở đi.

Chấm:

```python
!cd {WS} && SEL_SPLIT=test python harness/gate_sel_acc.py \
    /kaggle/working/preds_gui_sel_forcesel_273.jsonl
```

**Đọc kết quả — cột `sel_acc` trên đúng 273 bước này:**

| `sel_acc` | nghĩa | hướng chữa |
|---|---|---|
| **≳70%** | dè dặt quá mức: nó *biết* chọn cái nào, chỉ ngưỡng quyết định lệch về `none` | chữa ở khâu sinh, **không train lại** |
| **40–70%** | pha trộn | cần cả hai |
| **≲30%** | thật sự không biết: bỏ cuộc là phản ứng đúng trước màn khó | train lại với dữ liệu cân bằng |

Mốc so là **78,9%** — tỉ lệ đúng ở nhóm nó tự nguyện chọn.

⛔ **Con số này KHÔNG so với ngưỡng 63,6%.** Ngưỡng đó đã tiêu cho thiết kế thứ nhất, và
đây là lát 273 bước khó nhất chứ không phải toàn cổng. Nó là **chẩn đoán**, không phải điểm.
⚠️ Ép chọn cũng chặn chữ "none" trong câu hướng dẫn — ca hiếm, nhưng phải khai nếu đưa vào bài.
Chữ ký lượt chạy tự đổi thành `…+forcesel` nên tệp này không thể nối tiếp nhầm vào tệp thường.

---

## Ô 7 — SINH LẠI LÁT DEV KÈM ĐIỂM TIN CẬY (`--save-conf`)

Mục đích: lấy `p(none)` tại **bước quyết định** (token đầu ngay sau thẻ `<sel>`) để dựng đường
risk–coverage và quét ngưỡng τ. Không có số này thì mô hình chỉ cho ra một quyết định cứng,
không hiệu chỉnh được gì.

⚠️ Phải ghi ra **tệp mới**. Chữ ký lượt chạy đổi thành `…+conf`, nên nối tiếp vào tệp cũ sẽ bị
`infer_branch.py` chặn với thông báo *"là của lượt chạy KHÁC"* — đó là cơ chế chống lẫn lượt,
không phải lỗi.

```python
import subprocess, os
LOG = "/kaggle/working/conf.log"
f = open(LOG, "a")
env = {**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1"}
P = subprocess.Popen(
    ["python", f"{WS}/harness/infer_branch.py",
     "--adapter", AD,
     "--out", "/kaggle/working/preds_gui_sel_dev1400_conf.jsonl",
     "--cands", f"{WS}/harness/dg1_cache/test_ac/candidates.jsonl",
     "--limit", "1400",
     "--batch", "4",          # hạ từ 8: bảng logits cho --save-conf tốn thêm ~0,5 GB
     "--save-conf"],
    stdout=f, stderr=subprocess.STDOUT, start_new_session=True, env=env, cwd=WS)
print("PID", P.pid, "· log", LOG)
```

### Ô theo dõi

```python
import time, os, json
P, LOG, N = "/kaggle/working/preds_gui_sel_dev1400_conf.jsonl", "/kaggle/working/conf.log", 1400
t0, truoc, xn = None, 0, False
for _ in range(120):
    if not xn and os.path.exists(LOG):
        for d in open(LOG, encoding="utf-8", errors="ignore").read().split("\n"):
            if d.startswith("khối ứng viên:") or d.startswith("Nạp "):
                print("  ✔", d[:90], flush=True); xn = True
    rs = []
    if os.path.exists(P):
        for l in open(P, encoding="utf-8"):
            try: rs.append(json.loads(l))
            except Exception: pass
    n = len(rs)
    gio = time.strftime("%H:%M:%S", time.gmtime(time.time() + 7*3600))
    if n == 0:
        print(f"{gio}  [nạp mô hình] 0/{N}", flush=True)
    else:
        if t0 is None: t0, n0 = time.time(), n
        dt = time.time() - t0
        toc = (n - n0) / dt if dt > 0 and n > n0 else 0
        if toc:
            con = int((N - n) / toc)
            sp = (f"{1/toc:5.1f}s/b  còn {con//60:>3}m  xong ~"
                  f"{time.strftime('%H:%M', time.gmtime(time.time()+7*3600+con))}")
        else:
            con, sp = 0, "    ?s/b  còn   ?m  xong ~ ?   "
        # cột kiểm chứng: bao nhiêu bản ghi CÓ trường conf, và p_none đọc được
        cc = [r["conf"] for r in rs if r.get("conf")]
        pn = [c["p_none"] for c in cc]
        print(f"{gio}  {n:>4}/{N} ({n*100//N:>2}%) +{n-truoc:<3} {sp}  │ "
              f"có conf {len(cc)/n:5.1%}  p_none tb {sum(pn)/len(pn) if pn else 0:5.3f}",
              flush=True)
        truoc = n
    if n >= N:
        print("✅ XONG", flush=True); break
    time.sleep(60)
```

⛔ **Cột `có conf` phải gần 100%.** Nếu nó ở mức 0% thì cờ `--save-conf` không có hiệu lực
hoặc mã trong workspace là bản cũ — dừng ngay, đừng để chạy hết một tiếng rồi mới biết.
⚠️ `p_none tb` là trung bình trên **mọi** bản ghi (gồm cả ca nên trả `none`), nên đừng đọc nó
như tỉ lệ lỗi. Nó chỉ để thấy giá trị có phân tán chứ không kẹt ở 0 hay 1.

Chậm hơn lượt trước vì hạ `--batch` xuống 4 và phải giữ bảng logits: ước **~1,5 giờ**.

### Tải về

Xong thì tải `preds_gui_sel_dev1400_conf.jsonl` về, đặt vào **`runs/sel/`** (luật `runs/README.md`).
Việc quét ngưỡng τ chạy trên máy WSL, 0 GPU.

---

## Sau khi qua G6

Suy luận đủ **6.958 bước** cho từng lượt: bỏ `--limit`, đổi `--out`. Ước ~11 giờ/lượt trên
T4 ⇒ **2 lượt một tuần** trong hạn mức 30 giờ. Nhánh `gui_s1_match` chấm **không** có `--cands`.
