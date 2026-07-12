#!/usr/bin/env python3
"""dg3_freeze_split.py — KHOÁ phân vùng app train/test (làm ĐẦU TIÊN, trước mọi fetch/API).

Chia 30 app curated (kept_screens_final.json) thành 18 train / 12 test theo APP
(không theo màn — vì màn cùng app quá giống nhau, để lẫn = model học tủ).
Chia bằng greedy number-partitioning cân theo SỐ-MÀN/app + seed cố định → tất định,
chạy lại cho ra y hệt. Xuất harness/train_eval_app_split.json.

Sau khi chạy: REVIEW danh sách → `git add harness/train_eval_app_split.json && git commit`
để khoá cứng (dấu thời gian = bằng chứng pre-registration). KHÔNG sửa sau khi commit.

Ref: report/53 §2.1 + §5.1. Nguồn-sự-thật: report/54, report/KE_HOACH_2_BAI_BAO.
"""
import json
import random
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEPT = HERE / "kept_screens_final.json"
OUT = HERE / "train_eval_app_split.json"

SEED = 20260710          # cố định — đổi seed = đổi split, KHÔNG đổi sau khi đã chốt
N_TEST_APPS = 12         # 12 test / 18 train (60/40, KHÔNG 80/20 — xem report/53 §5.1)
N_TRAIN_APPS = 18


def app_of(screen: str) -> str:
    return screen.split("_")[0]


def main() -> None:
    data = json.loads(KEPT.read_text(encoding="utf-8"))
    kept = data["kept"]
    counts = Counter(app_of(s) for s in kept)
    apps = sorted(counts.keys())
    assert len(apps) == N_TEST_APPS + N_TRAIN_APPS, \
        f"Kỳ vọng {N_TEST_APPS + N_TRAIN_APPS} app, thấy {len(apps)}"

    # Tất định: gán mỗi app một jitter theo seed để phá hoà, rồi sort theo
    # (số-màn giảm dần, jitter) — greedy number-partitioning chuẩn cần app lớn trước.
    rng = random.Random(SEED)
    jitter = {a: rng.random() for a in apps}
    order = sorted(apps, key=lambda a: (-counts[a], jitter[a]))

    train, test = [], []
    train_scr, test_scr = 0, 0
    for a in order:
        n = counts[a]
        can_train = len(train) < N_TRAIN_APPS
        can_test = len(test) < N_TEST_APPS
        if can_train and can_test:
            # gán vào bin "nhẹ hơn" theo tải trung bình (tổng-màn / sức-chứa)
            # → cân số màn giữa 2 phía trong khi vẫn ép đúng 18/12.
            train_load = train_scr / N_TRAIN_APPS
            test_load = test_scr / N_TEST_APPS
            if test_load <= train_load:
                test.append(a); test_scr += n
            else:
                train.append(a); train_scr += n
        elif can_train:
            train.append(a); train_scr += n
        else:
            test.append(a); test_scr += n

    train.sort(); test.sort()
    assert set(train).isdisjoint(test), "train ∩ test PHẢI rỗng"
    assert len(train) == N_TRAIN_APPS and len(test) == N_TEST_APPS

    out = {
        "_note": "KHOÁ phân vùng app. KHÔNG sửa sau khi git commit (pre-registration). "
                 "Sinh bởi dg3_freeze_split.py.",
        "seed": SEED,
        "source": "kept_screens_final.json",
        "mobileviews": {
            "eval_apps_30": apps,                # cả 30 (để đối chiếu)
            "train_apps_30": train,              # 18 app clean — train + mốc đo Δ_train
            "test_apps_30": test,                # 12 app held-out — CHẤM Tier1/Tier2
            "train_pool_expanded": [],           # TODO: điền sau khi fetch pool mở rộng (~200 app),
                                                 #       disjoint tuyệt đối với test_apps_30 (cổng K-leak)
        },
        "androidcontrol": {
            "eval_apps_237": [],                 # TODO (chỉ cần cho nhánh nhiều-màn, làm sau)
            "train_apps_optional": [],
        },
        "_stats": {
            "train_apps": len(train), "train_screens": train_scr,
            "test_apps": len(test), "test_screens": test_scr,
            "total_screens": train_scr + test_scr,
        },
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"seed={SEED}  → {OUT.name}")
    print(f"TRAIN: {len(train)} app / {train_scr} màn")
    for a in train:
        print(f"   {a:24s} {counts[a]} màn")
    print(f"TEST : {len(test)} app / {test_scr} màn")
    for a in test:
        print(f"   {a:24s} {counts[a]} màn")
    print("\n→ REVIEW rồi: git add harness/train_eval_app_split.json && git commit  (khoá cứng)")


if __name__ == "__main__":
    main()
