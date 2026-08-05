# -*- coding: utf-8 -*-
"""dg3_dedup_pool.py — dedup PERCEPTUAL-HASH cho pool train (cổng chống-leak K).

Chạy SAU fetch_mv_expand_train.py. Hai việc (report/54 Bước 1 + rủi ro 7, D-33/D-35):
  (A) NỘI BỘ pool: bỏ màn gần-trùng nhau về thị giác (giữ 1 đại diện/nhóm).
  (B) CROSS-CHECK pool vs 30-app-eval (mv_multiapp): màn train nào trùng thị giác
      với màn eval → LOẠI khỏi train (phòng 2 app khác tên cùng template UI = rò rỉ ngầm
      phá held-out). Dedup-theo-TÊN ở fetch không bắt được ca này.

dHash 64-bit (PIL, không cần lib ngoài); "gần-trùng" = Hamming ≤ THRESHOLD.
Màn bị loại → CHUYỂN sang mv_train_pool/_dupes/ (không xoá, review được).

Chạy:  ~/.venvs/thesis/bin/python harness/dg3_dedup_pool.py   (hoặc python3 hệ thống — chỉ cần PIL)
"""
import os, glob, shutil
from PIL import Image

HERE = os.path.dirname(__file__)
POOL = os.path.join(HERE, "..", "dataset_samples", "mv_train_pool")
EVAL = os.path.join(HERE, "..", "dataset_samples", "mv_multiapp")
DUPES = os.path.join(POOL, "_dupes")
THRESHOLD = int(os.environ.get("PHASH_THRESHOLD", "6"))   # ≤6/64 bit khác = gần-trùng


def dhash(path, size=8):
    """difference hash 64-bit: resize (size+1)×size xám, so pixel liền kề theo hàng."""
    try:
        img = Image.open(path).convert("L").resize((size + 1, size), Image.LANCZOS)
    except Exception:
        return None
    px = list(img.getdata())
    w = size + 1
    bits = 0
    i = 0
    for r in range(size):
        for c in range(size):
            left = px[r * w + c]
            right = px[r * w + c + 1]
            bits = (bits << 1) | (1 if left > right else 0)
            i += 1
    return bits


def ham(a, b):
    return bin(a ^ b).count("1")


def hashes_of(folder):
    out = {}
    for f in sorted(glob.glob(os.path.join(folder, "*.jpg"))):
        h = dhash(f)
        if h is not None:
            out[f] = h
    return out


def move_out(jpg):
    os.makedirs(DUPES, exist_ok=True)
    base = os.path.basename(jpg)[:-4]
    for ext in (".jpg", ".viewhierarchy.json"):
        src = os.path.join(POOL, base + ext)
        if os.path.exists(src):
            shutil.move(src, os.path.join(DUPES, base + ext))


def main():
    pool = hashes_of(POOL)
    ev = hashes_of(EVAL)
    print(f"Pool: {len(pool)} màn | Eval(30-app): {len(ev)} màn | ngưỡng Hamming ≤ {THRESHOLD}")

    removed = []

    # (B) CROSS: pool vs eval — ưu tiên loại trước (nguy hiểm nhất = leak)
    for pf, ph in list(pool.items()):
        for ef, eh in ev.items():
            if ham(ph, eh) <= THRESHOLD:
                removed.append((pf, "cross-eval", os.path.basename(ef)))
                move_out(pf); pool.pop(pf, None)
                break

    # (A) NỘI BỘ: giữ 1 đại diện/nhóm gần-trùng
    keys = list(pool.items())
    kept = []
    for pf, ph in keys:
        dup_of = None
        for kf, kh in kept:
            if ham(ph, kh) <= THRESHOLD:
                dup_of = kf; break
        if dup_of:
            removed.append((pf, "internal", os.path.basename(dup_of)))
            move_out(pf)
        else:
            kept.append((pf, ph))

    print(f"\n=== KẾT QUẢ === giữ {len(kept)} màn | loại {len(removed)} màn (→ _dupes/)")
    from collections import Counter
    by = Counter(r[1] for r in removed)
    print("Loại theo loại:", dict(by))
    for pf, why, ref in removed[:30]:
        print(f"   [{why}] {os.path.basename(pf)}  ~  {ref}")
    if len(removed) > 30:
        print(f"   ... +{len(removed)-30} nữa")

    # app còn lại sau dedup
    apps = set(os.path.basename(f)[:-4].rsplit("_s", 1)[0] for f, _ in kept)
    print(f"\nSau dedup: {len(kept)} màn / {len(apps)} app train.")
    print("⚠ Nếu có ca 'cross-eval' → ĐÚNG là 2 app khác tên cùng template, đã né được leak.")


if __name__ == "__main__":
    main()
