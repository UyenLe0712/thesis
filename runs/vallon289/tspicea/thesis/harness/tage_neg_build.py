# -*- coding: utf-8 -*-
"""Dựng `tage_neg.jsonl` cho TAGE (file 265, Phụ lục C) — 0 GPU, vài giây.

    python3 harness/tage_neg_build.py [--out _bundles/tage-val-script/tage_neg.jsonl]

Nguồn: `harness/dg1_cache/train_ac/descriptors_trueD.jsonl` (41.099 bước chạm của tập dạy, mỗi bước có
phần tử vàng và phần tử lân cận cùng vai trò do `descriptor_label_build.py` chọn). Chỉ giữ các trường
TAGE dùng: tên/vai/điểm/hộp của phần tử vàng và của phần tử lân cận. Tập dạy chứa cả 1.567 bước val
của fgrb-p1-bundle (val tách từ tập dạy), nên một tệp phủ cả train lẫn val C1.
"""
import argparse, hashlib, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIU = ("episode_id", "step_id", "name", "role", "point_abs", "box",
       "name_neg", "role_neg", "point_neg_abs", "box_neg")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.join(ROOT, "harness/dg1_cache/train_ac/descriptors_trueD.jsonl"))
    ap.add_argument("--out", default=os.path.join(ROOT, "_bundles/tage-val-script/tage_neg.jsonl"))
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    n = co = 0
    with open(a.out, "w", encoding="utf-8") as fo:
        for d in map(json.loads, open(a.src, encoding="utf-8")):
            fo.write(json.dumps({k: d.get(k) for k in GIU}, ensure_ascii=False) + "\n")
            n += 1
            co += bool(d.get("point_neg_abs"))
    assert n == 41099, n
    print(f"{n} dòng · có phần tử lân cận {co} ({100*co/n:.1f}%) · md5 "
          f"{hashlib.md5(open(a.out, 'rb').read()).hexdigest()} → {a.out}")


if __name__ == "__main__":
    main()
