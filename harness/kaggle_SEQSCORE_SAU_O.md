# Kaggle — sequence-score lát dev 1.400 (bảy ô dán tuần tự)

Sinh tự động từ `kaggle_commit_sel_4_9.md` bằng `harness/make_7o.py`. **Đừng sửa tay tệp này.**

Lượt này sinh điểm chuẩn hoá độ dài cho từng ứng viên và cho `none`, theo hợp đồng
`report/134` §6.1, đã đăng ký trước ở `report/106` mục **(x16d)**.

⛔ Tệp này **chỉ sinh điểm**. Quét ngưỡng τ là việc riêng, chạy trên máy nhà, 0 GPU, và phải
theo đúng thủ tục đã đăng ký — cực đại **độ đúng trên toàn bộ 1.400 bước** chứ không phải trên
nhóm HasAns, luật null nằm trong lưới quét, và khoá τ **trước** khi nhìn `exec` đối chứng.

Ba input như đêm qua. Accelerator **GPU T4 x2**, Internet **On**.

## Cách chạy — hai giai đoạn

**Giai đoạn 1, chạy TAY:** dán đủ bảy ô, chạy ô 1 → ô 6. Ô 5 là probe 50 bước, mất khoảng 5–10
phút, và là chỗ duy nhất biết được `--cache-prompt` có dùng được không cùng giây-mỗi-bước thật.
Đọc bốn dòng kiểm ở cuối tệp này.

**Giai đoạn 2, đem commit:** ⛔ **xoá ô 5 và ô 6 khỏi notebook**, còn lại **năm ô** — 1 · 2 · 3
· 4 · 7. Rồi **Save Version → Save & Run All (Commit)**, gập máy.

Vì sao xoá: mỗi ô gọi một tiến trình riêng nên mô hình nền được nạp lại từ đầu ở từng ô; để ô
probe trong notebook commit là tốn thêm một lần nạp cộng 50 bước tính vô ích. Ô 4 thì giữ — nó
chỉ in một dòng và là thứ chặn lượt dài nếu bản `transformers` trên máy ảo không cắt được bộ
nhớ đệm.

⚠️ Nếu ô 4 báo `crop: False`, bỏ cờ `--cache-prompt` ở ô 7 trước khi commit; lượt dài khi đó
tốn khoảng 4,7 giờ thay vì dưới 1 giờ, vẫn nằm dưới trần 12 giờ.

---

## Ô 1 — cài gói và GỠ torchao

```python
!pip -q install -U accelerate peft qwen-vl-utils 2>&1 | tail -2
# ⛔ GỠ torchao — bắt buộc, đo 4/9: `pip -U peft` kéo về peft 0.20.0, mà image Kaggle có
#    torchao 0.10.0. peft 0.20 gọi is_torchao_available() trong lúc dựng lớp LoRA, và hàm
#    đó RAISE ImportError khi thấy torchao dưới 0.16 thay vì trả False. Kết quả:
#    PeftModel.from_pretrained chết NGAY SAU KHI đã nạp xong mô hình nền.
#    Script không dùng torchao ở đâu cả; vắng mặt thì hàm kia trả False và mọi thứ chạy.
!pip -q uninstall -y torchao 2>&1 | tail -1
import importlib.util
print("torchao còn không:", importlib.util.find_spec("torchao") is not None, "← phải là False")

import torch, transformers, peft
print(transformers.__version__, peft.__version__, torch.cuda.get_device_name(0))
```

## Ô 2 — dựng workspace, kiểm hai hash

```python
import os, glob, json, shutil, subprocess
WS = "/kaggle/working/ws"; os.makedirs(WS, exist_ok=True)

# ⛔ BÀI HỌC 5/9: "New Version" của Kaggle THÊM thư mục chứ không thay thế, nên trong
#    /kaggle/input tồn tại song song mọi gói đã upload (kaggle_sel_4_9, kaggle_sel_5_9, …).
#    Dấu vân tay phải là chuỗi CHỈ có trong bản MỚI NHẤT, nếu không nhiều bản cùng đạt và
#    `ok[0]` lấy phải bản cũ — im lặng, không lỗi. Đã mất một lượt probe vì đúng chuyện này.
#    ⇒ Mỗi lần vá mã thì ĐỔI hai dòng dưới, và giữ assert "đúng một bản".
CAN_FILE = "seq_score_sel.py"
CAN = "KHÔNG gọi .float() trên CẢ bảng logits"     # dấu vân tay bản 5/9 (vá tràn bộ nhớ)
src = glob.glob(f"/kaggle/input/**/harness/{CAN_FILE}", recursive=True)
assert src, f"DỪNG: chưa thấy harness/{CAN_FILE} trong /kaggle/input"
ok = []
for q in src:
    co = CAN in open(q, encoding="utf-8", errors="ignore").read()
    print(("  ✅ bản mới" if co else "  ⛔ bản cũ"), q)
    if co: ok.append(q)
assert ok, ("DỪNG: không bản nào chứa bản vá mới nhất. Dataset chưa lên version mới, hoặc "
            "panel Input còn trỏ version cũ.")
assert len(ok) == 1, (f"DỪNG: {len(ok)} bản cùng đạt dấu vân tay — không biết lấy bản nào.\n"
                      f"   {ok}\n"
                      f"   Đổi CAN thành chuỗi chỉ có trong bản mới nhất.")
PKG = os.path.dirname(ok[0])
GOI = os.path.dirname(PKG)          # gốc gói, để lấy runs/sel/... của ĐÚNG gói này
shutil.rmtree(f"{WS}/harness", ignore_errors=True)
shutil.copytree(PKG, f"{WS}/harness")
assert os.path.isfile(f"{WS}/harness/seq_score_sel.py"), \
    "DỪNG: dataset thiếu seq_score_sel.py — upload lại version mới"
# bản vá OOM ngày 5/9: bản trước gọi .float() trên CẢ bảng logits và tràn T4 ở lô 8 span
assert "KHÔNG gọi .float() trên CẢ bảng logits" in open(
    f"{WS}/harness/seq_score_sel.py", encoding="utf-8").read(), \
    "DỪNG: seq_score_sel.py là bản TRƯỚC 5/9, sẽ tràn bộ nhớ ở đường chậm. Upload version mới."

# ảnh: symlink, không chép
best = None
for t in glob.glob("/kaggle/input/**/test_ac/images", recursive=True):
    n = len(glob.glob(os.path.join(t, "*.png")))
    print(f"  {n:5d} ảnh  {t}")
    if n >= 4400 and (best is None or n > best[1]): best = (t, n)
assert best, "DỪNG: không gói nào đủ ảnh"
dst = f"{WS}/harness/dg1_cache/test_ac/images"
if os.path.islink(dst): os.remove(dst)
elif os.path.isdir(dst): shutil.rmtree(dst)
os.symlink(best[0], dst)

AD = os.path.dirname(glob.glob("/kaggle/input/**/adapter_config.json", recursive=True)[0])
print("adapter:", AD)

# ⛔ CHỮ KÝ LƯỢT CHẠY LẤY THEO TÊN THƯ MỤC ADAPTER (infer_branch.py: sig = "lora:" +
#    basename(adapter)). Lát dev 1.400 đã sinh với chữ ký "lora:gui-sel-adapter". Đổi tên
#    thư mục là đổi chữ ký, và ô gộp 4.463 sẽ thấy HAI chữ ký rồi dừng — sau khi đã tiêu
#    4 giờ suy luận. Dùng lại đúng dataset adapter cũ, đừng upload bản mới đặt tên khác.
assert os.path.basename(AD) == "gui-sel-adapter", (
    f"DỪNG: thư mục adapter tên {os.path.basename(AD)!r}, phải là 'gui-sel-adapter' để "
    f"chữ ký trùng lát dev 1.400. Gắn lại dataset adapter cũ.")

# ⛔ artifact phải đúng bản đã pin — đối chiếu runs/sel/manifest_selA_selB_4_9.json
import hashlib
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
MONG = {
  "candidates.jsonl": "f10b69411a28e4a9b78aa309241d4a68440e8c463072788c541e887e2e1914f8",
  "adapter_model.safetensors": "8b6184798527d3fa4de76b9d2fe3b18005436de07bd51890d71bcb838dc82dfb",
}
for n, want in MONG.items():
    p = (f"{WS}/harness/dg1_cache/test_ac/{n}" if n.endswith("candidates.jsonl")
         else f"{AD}/{n}")
    got = sha(p)
    print(("OK  " if got == want else "LỆCH"), n, got[:16], "…")
    assert got == want, f"DỪNG: {n} không phải bản đã pin"
```

## Ô 3 — hàm chạy-và-chờ

```python
import subprocess, os, time

def chay_va_cho(cmd, log, dich=None, can=None, nhip=120):
    """Chạy tiến trình con, CHỜ tới khi xong, in một dòng mỗi `nhip` giây.

    Vì sao phải chờ ngay trong ô: commit chạy tuần tự và kết thúc notebook khi hết ô.
    Popen rồi để ô kết thúc là notebook đi tiếp rồi tắt máy ảo, giết luôn tiến trình.
    Vì sao vẫn phải in định kỳ: commit hỏng thì thứ duy nhất còn lại để chẩn là log.
    """
    env = {**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1",
           "HF_HUB_DISABLE_PROGRESS_BARS": "1"}
    f = open(log, "a")
    P = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT,
                         start_new_session=True, env=env, cwd=WS)
    t0 = time.time()
    while P.poll() is None:
        time.sleep(nhip)
        n = sum(1 for _ in open(dich)) if dich and os.path.exists(dich) else -1
        gio = (time.time() - t0) / 3600
        eta = (gio * (can - n) / n) if (can and n > 0) else float("nan")
        print(f"{time.strftime('%H:%M:%S')} · {gio:5.2f} h · "
              f"{n}/{can if can else '?'} · còn ~{eta:.1f} h", flush=True)
    print("mã thoát:", P.returncode, flush=True)
    print("--- 25 dòng log cuối ---", flush=True)
    print(subprocess.run(["tail", "-25", log], capture_output=True, text=True).stdout)
    assert P.returncode == 0, "DỪNG: tiến trình thoát khác 0 — đọc log ở trên"
```

## Ô 4 — kiểm API bộ nhớ đệm (quyết định dùng được --cache-prompt hay không)

```python
from transformers import DynamicCache
import transformers
c = DynamicCache()
print("transformers", transformers.__version__,
      "| crop:", hasattr(c, "crop"), "| get_seq_length:", hasattr(c, "get_seq_length"))
```

## Ô 5 — PROBE 50 bước, đọc bốn dòng rồi mới phóng

```python
chay_va_cho(
    ["python", f"{WS}/harness/seq_score_sel.py",
     "--adapter", AD,
     "--cands", f"{WS}/harness/dg1_cache/test_ac/candidates.jsonl",
     "--only", f"{GOI}/runs/sel/preds_gui_sel_seed101_dev1400.jsonl",
     "--out", "/kaggle/working/probe50_seqscore.jsonl",
     "--cache-prompt", "--probe", "50"],
    log="/kaggle/working/probe50.log", dich="/kaggle/working/probe50_seqscore.jsonl",
    can=50, nhip=60)

import json
rs = [json.loads(l) for l in open("/kaggle/working/probe50_seqscore.jsonl", encoding="utf-8")]
tok = {r["tok_none"] for r in rs}
print("số bước           :", len(rs))
print("tok_none (phải là MỘT giá trị):", tok)
print("s_none  trung bình:", sum(r["s_none"] for r in rs) / len(rs))
print("s_star  trung bình:", sum(r["s_star"] for r in rs) / len(rs))
print("margin  trung bình:", sum(r["margin"] for r in rs if r["margin"] is not None) / len(rs))
print("n_cand  trung bình:", sum(r["n_cand"] for r in rs) / len(rs))
print("có ứng viên vàng  :", sum(r["gold_in_menu"] for r in rs), "/", len(rs))
```

## Ô 6 — dọn tệp probe

```python
import os, glob
for p in glob.glob("/kaggle/working/probe*"):
    os.remove(p); print("xoá", p)
print("đã dọn tệp probe")
```

## Ô 7 — lượt dài: 1.400 bước

```python
OUT = "/kaggle/working/seqscores_gui_sel_seed101_dev1400.jsonl"
p_dev = f"{GOI}/runs/sel/preds_gui_sel_seed101_dev1400.jsonl"   # ĐÚNG gói, không glob mù
chay_va_cho(
    ["python", f"{WS}/harness/seq_score_sel.py",
     "--adapter", AD,
     "--cands", f"{WS}/harness/dg1_cache/test_ac/candidates.jsonl",
     "--only", p_dev,
     "--out", OUT,
     "--cache-prompt"],
    log="/kaggle/working/c3_seqscore.log", dich=OUT, can=1400)
```

---

## Bốn dòng phải đúng ở ô 5 trước khi phóng lượt dài

1. Ba dòng `kiểm chéo nhanh↔chậm: lệch tối đa ...` đều **dưới 1e-3**. Đây là thứ quyết định lượt
   dài tốn dưới 1 giờ hay khoảng 4,7 giờ. Script tự dừng nếu vượt; **đừng nới ngưỡng**.
2. `tok_none` chỉ có **một** giá trị — span `<sel>none</sel>` cố định nên số token phải bằng nhau
   ở mọi bước. Nhiều hơn một giá trị nghĩa là bộ tách token đang làm gì đó khác.
3. `s_none` và `s_star` đều **âm và cùng cỡ**. Dương là sai dấu; lệch nhau vài bậc là sai chuẩn hoá.
4. Giây mỗi bước **nhân 1.400 phải dưới 12 giờ**, có đệm.

## Sau khi có tệp

Tải `seqscores_gui_sel_seed101_dev1400.jsonl` về `runs/sel/`. Mỗi dòng có điểm của **mọi** ứng
viên cùng `s_none`, `margin`, số token — nên quét lại τ về sau **không phải gọi GPU lần nữa**.
