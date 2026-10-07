# ── Ô 1b — TÌM dữ liệu rồi NỐI vào đúng chỗ mã chấm đòi ──────────────────────
# score_run.py đọc cứng <thư mục chứa nó>/dg1_cache/test_ac/{test.jsonl, images/}.
# Gói vừa tải chỉ có mã + preds; ảnh và test.jsonl nằm ở phần cũ của dataset.
import os, glob, json, shutil

WS = "/kaggle/working"
PKG = "/kaggle/input/datasets/uyenle0712/thesis-preds/kaggle_16_8"   # gói vừa tải

# 1) quét TOÀN BỘ /kaggle/input, không chỉ trong gói
print("=== các dataset đang gắn ===")
for d in sorted(glob.glob("/kaggle/input/*")):
    print(" ", d)

print("\n=== tìm test.jsonl ===")
tests = glob.glob("/kaggle/input/**/test.jsonl", recursive=True)
for t in tests:
    print(" ", t, f"({sum(1 for _ in open(t, encoding='utf-8'))} dòng)")

print("\n=== tìm thư mục ảnh ===")
cands = {}
for p in glob.glob("/kaggle/input/**/*.png", recursive=True):
    d = os.path.dirname(p)
    cands[d] = cands.get(d, 0) + 1
for d, n in sorted(cands.items(), key=lambda x: -x[1])[:8]:
    print(f"  {n:6d} ảnh  {d}")

print("\n=== tìm tệp preds đã có ===")
for p in sorted(glob.glob("/kaggle/input/**/preds_*.jsonl", recursive=True)):
    print(" ", p)
for p in sorted(glob.glob("/kaggle/input/**/score_*_raw.jsonl", recursive=True)):
    print(" ", p)

# 2) dựng cây thư mục mã chấm đòi, bằng liên kết mềm (không tốn dung lượng)
TEST_JSONL = tests[0] if tests else None
IMG_DIR = max(cands, key=cands.get) if cands else None

if TEST_JSONL and IMG_DIR:
    dst = f"{WS}/harness/dg1_cache/test_ac"
    os.makedirs(dst, exist_ok=True)
    if not os.path.exists(f"{WS}/harness/score_run.py"):
        shutil.copytree(f"{PKG}/harness", f"{WS}/harness", dirs_exist_ok=True)
    for src, name in [(TEST_JSONL, "test.jsonl"), (IMG_DIR, "images")]:
        link = os.path.join(dst, name)
        if os.path.islink(link) or os.path.exists(link):
            os.remove(link) if os.path.islink(link) else None
        if not os.path.exists(link):
            os.symlink(src, link)
    print("\n=== đã nối ===")
    print(" test.jsonl →", os.path.realpath(f"{dst}/test.jsonl"))
    print(" images     →", os.path.realpath(f"{dst}/images"),
          f"({len(glob.glob(f'{dst}/images/*.png'))} ảnh)")

    # 3) phép kiểm rẻ nhất: mã chấm có mở được đúng ảnh của bước đầu tiên không
    recs = [json.loads(l) for l in open(f"{dst}/test.jsonl", encoding="utf-8")]
    taps = [r for r in recs if r["action"].get("action_type") in ("click", "long_press")
            and "x" in r["action"]]
    miss = sum(1 for r in taps[:200] if not os.path.exists(os.path.join(dst, r["image"])))
    print(f"\n 200 bước chạm đầu: thiếu {miss} ảnh", "✔ sẵn sàng" if miss == 0 else "✘ DỪNG")
else:
    print("\n✘ Không thấy test.jsonl hoặc thư mục ảnh trong /kaggle/input.")
    print("  → gắn thêm dataset chứa ảnh tập kiểm, hoặc dựng lại bằng build_test_data.py")
