# Phép A — bản 2, sửa đúng chỗ hỏng: KHÔNG nhìn thấy tiến độ

Bản 1 chạy 4,3 giờ mà log Kaggle đứng ở giây thứ 59,8. Không biết đang chạy hay treo là
lỗi thiết kế của ô, không phải xui. Ba nguyên nhân, vá cả ba:

| Hỏng | Vì sao | Vá |
|---|---|---|
| Log ngập rác **và nhiều khả năng chính nó làm treo** | `tqdm` không chạy trong terminal thật nên in **mỗi cập nhật thành một dòng**; riêng nạp mô hình đã hơn 1.400 dòng, nhân 4 lần nạp. Kaggle chặn log khi vượt trần ⇒ tiến trình **kẹt cứng ở lệnh ghi stdout** | tắt thanh tiến trình + cho tiến trình con ghi thẳng **ra tệp**, không qua ống log của Kaggle |
| Không đọc được gì khi log nghẽn | mọi thứ đổ vào một luồng duy nhất của notebook | mỗi biến thể ghi **log riêng ra tệp**, đọc được bất cứ lúc nào |
| Dừng là mất trắng | commit bị huỷ thì Kaggle **không lưu** `/kaggle/working` | chạy **tương tác** biến thể đầu, tải tệp về, rồi mới commit phần còn lại |

---

## Bằng chứng lấy từ log bản 1 (17/8) — nó KHÔNG chạy chậm, nó ĐỨNG

Log Kaggle chỉ có hai mục: `59.8s #29` và `25560.4s #30`. **Nội dung hai mục giống hệt
nhau**, cùng dừng giữa chữ ở `Loading weights: 29% | 213/729`. Bảy tiếng trôi qua mà con
số vẫn 213/729, trong khi chính `tqdm` ước tính khâu này mất **3 giây**.

⇒ Không phải chạy chậm, cũng không phải chạy CPU (CPU vẫn nạp xong trọng số). Đây là
**tiến trình kẹt ở lệnh ghi stdout**: log vượt trần, Kaggle ngừng nhận, lệnh `write` chặn
lại vĩnh viễn, và mọi thứ đứng ngay tại dòng in dở. Mục `#30` chính là mẩu đệm cuối cùng
lọt qua được.

Đó là lý do bản 2 cho tiến trình con ghi **ra tệp** thay vì để nó in qua ống log — vá
đúng nguyên nhân, không chỉ vá phần nhìn thấy.

## Ô 0 — 5 giây, chặn nguyên nhân số một khiến bản 1 chạy quá lâu

```python
import torch, subprocess
print("có GPU:", torch.cuda.is_available(),
      "|", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "—")
print(subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total",
                      "--format=csv,noheader"], capture_output=True, text=True).stdout)
assert torch.cuda.is_available(), "DỪNG: đang chạy CPU. Bật Accelerator = GPU T4 ×2."
```

Chạy CPU thì mã **không báo lỗi**, chỉ chậm 10–20 lần — đúng triệu chứng của bản 1.
Panel Accelerator hay bị trả về *None* khi mở lại notebook hoặc khi commit; ô này bắt được
trong 5 giây thay vì sau 9 giờ.

## Ô 2 (bản mới) — chạy tương tác, mỗi biến thể một tệp log

```python
import os, subprocess, time, json, threading

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"   # tắt thanh tải mô hình
os.environ["TRANSFORMERS_VERBOSITY"] = "error"      # bớt log thư viện
os.environ["PYTHONUNBUFFERED"] = "1"                # in ra là thấy ngay

WS   = "/kaggle/working"
DATA = "/kaggle/input/datasets/uyenle0712/thesis-preds/kaggle_16_8"
CEIL = 74.9

def chay(v, n=800):
    log = f"{WS}/log_{v}.txt"
    with open(log, "w") as f:
        p = subprocess.Popen(
            ["python", "-u", f"{WS}/harness/score_run.py", "--mode", "score",
             "--grounder", "uground", "--preds", f"{DATA}/preds_para_{v}.jsonl",
             "--out", f"{WS}/score_para_{v}.json", "--n", str(n)],
            stdout=f, stderr=subprocess.STDOUT)
        t0 = time.time()
        while p.poll() is None:          # in nhịp sống mỗi 2 phút, không phụ thuộc log con
            time.sleep(120)
            try:
                dong = [l for l in open(log) if "bước/giây" in l]
                cuoi = dong[-1].strip() if dong else "(chưa tới vòng chấm)"
            except Exception:
                cuoi = "(chưa có log)"
            print(f"[{time.strftime('%H:%M:%S')}] {v} · {(time.time()-t0)/60:.0f} phút · {cuoi}",
                  flush=True)
    return p.returncode

rc = chay("p1_verb")
print("mã thoát:", rc)
r = json.load(open(f"{WS}/score_para_p1_verb.json"))
print(f"p1_verb {r['exec_voronoi']*100:.1f}%  (trần {CEIL}%, lệch {r['exec_voronoi']*100-CEIL:+.1f})")
```

Vòng `while` là chỗ đáng giá: nó in một dòng **mỗi 2 phút** từ notebook, không phụ thuộc
việc log tiến trình con có tới nơi hay không. Thấy dòng đó đều đặn là đang sống.

## Ô 2b — xem log bất cứ lúc nào (ô riêng, chạy song song)

```python
print(open("/kaggle/working/log_p1_verb.txt").read()[-3000:])
```

## Ô 2c — ba biến thể còn lại

Chạy sau khi `p1_verb` ra số hợp lý (73–76% là bình thường):

```python
for v in ["p2_order", "p3_nopos", "p4_both"]:
    chay(v)
    r = json.load(open(f"{WS}/score_para_{v}.json"))
    print(f"{v} {r['exec_voronoi']*100:.1f}%  lệch {r['exec_voronoi']*100-CEIL:+.1f}", flush=True)
```

---

## Cách chạy an toàn hơn commit

1. **Tương tác**, chạy ô 1 → ô 2 (một biến thể, ~1 giờ). Có nhịp sống mỗi 2 phút.
2. Xong thì **tải ngay** `score_para_p1_verb.json` và `score_para_p1_verb_raw.jsonl` về máy
   từ panel Data → Output. Đây là thứ commit không cho bạn: lấy kết quả ra giữa chừng.
3. Ba biến thể còn lại chạy tiếp trong cùng phiên (ô 2c), hoặc commit riêng.

Phiên tương tác của Kaggle tự tắt sau ~20 phút **không thao tác**, nhưng ô đang chạy thì
không tính là rảnh — cứ để tab mở.

## Nếu phải dừng bản đang chạy

Chấp nhận mất phần đã chạy: commit bị huỷ thì `/kaggle/working` không được lưu, kể cả tệp
thô mà `score_run.py` đã ghi dần. Đó chính là lý do bản 2 chạy tương tác trước.
