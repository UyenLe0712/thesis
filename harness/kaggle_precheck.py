# -*- coding: utf-8 -*-
"""
Kiểm TRƯỚC khi chạy cổng A trên máy lạ (Kaggle/Colab). Chạy vài giây, không cần mạng.

Có ba thứ có thể lệch âm thầm khi đổi máy, và cả ba đều làm con số cổng A sai mà
không báo lỗi:

  1. tập kiểm không phải bản đã khoá → mẫu 300 bước lấy ra khác tập đã đăng ký;
  2. `random.Random(SEED).shuffle` cho thứ tự khác (khác bản Python) → cũng lệch mẫu,
     nhưng lần này lệch mà tệp vẫn đúng, nên không cách nào thấy nếu không kiểm;
  3. thiếu ảnh của đúng những bước được chọn → chương trình chết giữa chừng sau khi
     đã nạp mô hình 2 tỉ tham số, mất công vô ích.

Chạy:  python harness/kaggle_precheck.py
"""
import os, sys, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
TEST = os.path.join(HERE, "dg1_cache", "test_ac")
SEED = 20260805          # khoá ở report/106 mục 10 — phải giống score_run.py

# Số đã khoá ngày 6/8 (report/106 mục sửa đổi). Lệch một bước cũng đổi mẫu ngẫu nhiên.
N_STEPS_LOCKED = 6958
N_TAPS_LOCKED = 4463
N_GATE = 300

# Ba bản ghi đầu của mẫu 300, tính trên máy đã dựng dữ liệu. Đây là phép kiểm thứ tự
# xáo — nếu bản Python trên máy mới xáo khác đi thì ba cặp này lệch ngay.
HEAD_EXPECTED = [(19277, 8), (18972, 1), (18540, 1)]
TAIL_EXPECTED = (18977, 1)

ok = True


def check(name, got, want):
    global ok
    good = got == want
    ok = ok and good
    print(f"  {'ĐẠT ' if good else 'RỚT '} {name:34} {got}" + ("" if good else f"   ≠ {want}"))
    return good


print("=" * 70)
print("KIỂM TRƯỚC KHI CHẠY CỔNG A")
print("=" * 70)

p = os.path.join(TEST, "test.jsonl")
if not os.path.exists(p):
    sys.exit(f"RỚT — không thấy {p}. Kiểm lại đã copy mã + dữ liệu ra thư mục ghi được chưa.")

recs = [json.loads(l) for l in open(p, encoding="utf-8")]
taps = [r for r in recs if r["action"].get("action_type") in ("click", "long_press")
        and "x" in r["action"]]

print("\n[1] tập kiểm có đúng bản đã khoá không")
check("tổng số bước", len(recs), N_STEPS_LOCKED)
check("số bước chạm", len(taps), N_TAPS_LOCKED)

print("\n[2] mẫu 300 bước có trùng bản đã đăng ký không")
random.Random(SEED).shuffle(taps)
sel = taps[:N_GATE]
head = [(r["episode_id"], r["step_id"]) for r in sel[:3]]
check("ba bản ghi đầu của mẫu", head, HEAD_EXPECTED)
check("bản ghi cuối của mẫu", (sel[-1]["episode_id"], sel[-1]["step_id"]), TAIL_EXPECTED)

print("\n[3] có đủ ảnh của đúng 300 bước đó không")
miss = [r["image"] for r in sel if not os.path.exists(os.path.join(TEST, r["image"]))]
check("số ảnh thiếu", len(miss), 0)
if miss:
    print("     thiếu ví dụ:", ", ".join(miss[:5]))
    print("     → dựng lại bằng: python harness/build_test_data.py --shards 9")

print("\n[4] card đồ hoạ")
try:
    import torch
    cuda = torch.cuda.is_available()
    print(f"       cuda           : {cuda}")
    if cuda:
        print(f"       card           : {torch.cuda.get_device_name(0)}")
        print(f"       bf16           : {torch.cuda.is_bf16_supported()}"
              "   (T4/P100 không có — pick_dtype tự lùi về fp16)")
        free, total = torch.cuda.mem_get_info()
        print(f"       bộ nhớ         : {total/2**30:.1f} GB, trống {free/2**30:.1f} GB")
    else:
        print("       KHÔNG THẤY GPU — bật Accelerator trong Settings rồi khởi động lại phiên.")
        ok = False
except ImportError:
    print("       chưa cài torch")
    ok = False

print("\n" + "=" * 70)
print("SẴN SÀNG — chạy cổng A được." if ok else
      "CHƯA SẴN SÀNG — sửa mục RỚT ở trên trước, đừng chạy cổng A.")
print("=" * 70)
sys.exit(0 if ok else 1)
