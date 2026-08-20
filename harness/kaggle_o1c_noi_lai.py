# ── Ô 1c — NỐI LẠI cho đúng: test.jsonl và ảnh phải CÙNG một gói ─────────────
# Lỗi của ô 1b: nó lấy test.jsonl đầu tiên tìm thấy, hoá ra là bản 300 dòng của
# cổng A, trong khi ảnh lấy từ gói khác. Chạy như thế thì `--n 800` chấm trên ~192
# bước của một lát khác hẳn, và số trả về không so được với mốc đã tính. Đây đúng
# loại lỗi chạy trơn mà kết quả sai.
import os, glob, json, shutil

WS = "/kaggle/working"
PKG = "/kaggle/input/datasets/uyenle0712/thesis-preds/kaggle_16_8"

# Chọn gói nào có ĐỦ CẢ HAI: test.jsonl đủ dòng và thư mục ảnh đủ lớn.
best = None
for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True):
    root = os.path.dirname(t)
    n_rows = sum(1 for _ in open(t, encoding="utf-8"))
    n_img = len(glob.glob(os.path.join(root, "images", "*.png")))
    print(f"  {n_rows:5d} dòng · {n_img:5d} ảnh  {root}")
    if n_rows >= 6900 and n_img >= 4400 and (best is None or n_img > best[2]):
        best = (t, n_rows, n_img, root)

assert best, "Không gói nào có đủ cả test.jsonl 6.958 dòng lẫn 4.463 ảnh"
TEST_JSONL, n_rows, n_img, ROOT = best
print(f"\n→ dùng: {ROOT}  ({n_rows} dòng, {n_img} ảnh)")

# nhãn app_seen_in_train phải có, khâu chấm đọc thẳng từ đây
r0 = json.loads(open(TEST_JSONL, encoding="utf-8").readline())
print("   có nhãn app_seen_in_train:", "app_seen_in_train" in r0)

dst = f"{WS}/harness/dg1_cache/test_ac"
os.makedirs(dst, exist_ok=True)
if not os.path.exists(f"{WS}/harness/score_run.py"):
    shutil.copytree(f"{PKG}/harness", f"{WS}/harness", dirs_exist_ok=True)
for src, name in [(TEST_JSONL, "test.jsonl"), (os.path.join(ROOT, "images"), "images")]:
    link = os.path.join(dst, name)
    if os.path.islink(link):
        os.remove(link)
    elif os.path.exists(link):
        shutil.rmtree(link) if os.path.isdir(link) else os.remove(link)
    os.symlink(src, link)

# kiểm bằng chính đường mã chấm sẽ đi
recs = [json.loads(l) for l in open(f"{dst}/test.jsonl", encoding="utf-8")]
taps = [r for r in recs if r["action"].get("action_type") in ("click", "long_press")
        and "x" in r["action"]]
miss = sum(1 for r in taps if not os.path.exists(os.path.join(dst, r["image"])))
print(f"\n bản ghi: {len(recs)} | bước chạm: {len(taps)} | thiếu ảnh: {miss}")
print(" ", "✔ SẴN SÀNG" if len(taps) >= 4400 and miss == 0 else "✘ DỪNG, chưa đúng")

# lát 800 mà score_run sẽ lấy — in ra để đối chiếu với mốc so đã tính ở máy nhà
import random
keys = [(r["episode_id"], r["step_id"]) for r in taps]
random.Random(20260805).shuffle(keys)
print(f"  lát 800 bắt đầu bằng: {keys[:3]}")
