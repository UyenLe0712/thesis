# -*- coding: utf-8 -*-
"""fetch_mv_expand_train.py — mở rộng POOL TRAIN từ 2 shard MobileViews CHƯA dùng.

Khác fetch_mv_expand.py:
  - Lấy từ 2 shard MỚI (300000-400000, 400000-522301).
  - LOẠI TRỪ toàn bộ 30 app eval (đọc từ train_eval_app_split.json) → pool train
    disjoint tuyệt đối với 12 test app (cổng K-leak, report/53 §2.1).
  - Xuất ra dataset_samples/mv_train_pool/ (TÁCH khỏi bộ eval mv_multiapp).
  - Hỗ trợ resume (bỏ qua app đã có trong pool).

CHẠY bằng venv có datasets:  ~/.venvs/thesis/bin/python harness/fetch_mv_expand_train.py
Env: NEW_APPS, MAX_PER_APP=5, MIN_ACT=6, SCAN_CAP.  Free (chỉ tốn băng thông).

⚠ Sau fetch: chạy dedup PERCEPTUAL-HASH (nội bộ pool + cross-check vs 30-app-eval) —
   bước riêng, phòng 2 app khác tên cùng template UI (report/54 Bước 1 / rủi ro 7).
"""
import os, re, json, glob, time
from datasets import load_dataset

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "dataset_samples", "mv_train_pool")
SPLIT = os.path.join(HERE, "train_eval_app_split.json")
os.makedirs(OUT, exist_ok=True)

MAX_PER_APP = int(os.environ.get("MAX_PER_APP", "5"))
NEW_APPS    = int(os.environ.get("NEW_APPS", "20"))       # mặc định = PILOT nhỏ; đặt cao khi chạy full
SCAN_CAP    = int(os.environ.get("SCAN_CAP", "5000"))
MIN_ACT     = int(os.environ.get("MIN_ACT", "6"))

BASE = "MobileViews_Screenshots_ViewHierarchies/Parquets/"
SHARDS = [                                                # 2 shard CHƯA dùng
    BASE + "MobileViews_300000-400000.parquet",
    BASE + "MobileViews_400000-522301.parquet",
]


def excluded_prefixes():
    """30 app eval (từ split) + app đã có sẵn trong pool (resume)."""
    ex = set()
    sp = json.load(open(SPLIT, encoding="utf-8"))
    for a in sp["mobileviews"]["eval_apps_30"]:
        ex.add(a)
    for f in glob.glob(os.path.join(OUT, "*.jpg")):
        ex.add(os.path.basename(f)[:-4].rsplit("_s", 1)[0])
    return ex


def actionable_count(o):
    c = 0
    for n in o.get("views", []):
        if not n.get("bounds"):
            continue
        lab = (n.get("text") or n.get("content_description") or "").strip()
        if lab and (n.get("clickable") or n.get("editable") or n.get("long_clickable")):
            c += 1
    return c


def pkg_of(o):
    for n in o.get("views", []):
        if n.get("package"):
            return n["package"]
    return None


def main():
    exclude = excluded_prefixes()
    print(f"Loại trừ {len(exclude)} app (30 eval + pool đã có). Mục tiêu: {NEW_APPS} app mới, {MAX_PER_APP} màn/app.")
    new_per = {}
    saved = 0
    t0 = time.time()
    scanned_total = 0
    for shard in SHARDS:
        if len(new_per) >= NEW_APPS:
            break
        print("SHARD:", shard.split("/")[-1])
        ds = load_dataset("mllmTeam/MobileViews", data_files=shard, streaming=True, split="train")
        scanned = 0
        for row in ds:
            scanned += 1; scanned_total += 1
            if scanned > SCAN_CAP:
                print(f"  (đạt SCAN_CAP={SCAN_CAP} cho shard này)")
                break
            if scanned % 1000 == 0:
                print(f"  ...scan {scanned} | app mới={len(new_per)} | màn lưu={saved} | {time.time()-t0:.0f}s")
            try:
                o = json.loads(row["json_content"])
            except Exception:
                continue
            pkg = pkg_of(o)
            if not pkg:
                continue
            pre = re.sub(r"[^a-z0-9]", "", pkg.lower())[:20]
            if not pre or pre in exclude:
                continue
            if pre not in new_per and len(new_per) >= NEW_APPS:
                continue
            if new_per.get(pre, 0) >= MAX_PER_APP:
                continue
            if actionable_count(o) < MIN_ACT:
                continue
            n = new_per.get(pre, 0) + 1
            name = f"{pre}_s{n}"
            with open(os.path.join(OUT, name + ".jpg"), "wb") as fh:
                fh.write(row["image_content"])
            with open(os.path.join(OUT, name + ".viewhierarchy.json"), "w", encoding="utf-8") as fh:
                fh.write(row["json_content"])
            new_per[pre] = n; saved += 1

    dt = time.time() - t0
    print(f"\n=== XONG === scan {scanned_total} rows | {len(new_per)} app mới | {saved} màn lưu | {dt:.0f}s")
    if new_per:
        avg = saved / len(new_per)
        print(f"Trung bình {avg:.1f} màn/app. Ra {OUT}")
        # gợi ý ngoại suy
        if scanned_total > 0:
            rate = len(new_per) / scanned_total
            print(f"Yield: {rate*1000:.1f} app mới / 1000 rows → để đạt N app cần ~{(1/rate):.0f} rows/app-mới")


if __name__ == "__main__":
    main()
