# -*- coding: utf-8 -*-
"""
CỔNG v2 — kiểm thước v2 bằng ca THẬT viết tay, ĐỘC LẬP với hàm target_of() của thước.
Sửa đúng lỗi report/90 §B1: bộ bơm-lỗi cũ dựng "paraphrase" bằng cách GỌI CHÍNH target_of()
rồi dán lại → Jaccard=1 tất yếu → AUC=1.000 là hằng đẳng thức.

Ở đây MỖI CẶP do người viết, KHÔNG suy từ thước:
 - SAME  = cùng một nút, gọi khác chữ (thước PHẢI khớp) — gồm cả ca K1-khó (không chung token).
 - DIFF  = nút khác NHƯNG có chồng token (thước PHẢI bác) — ca 'gmail tab' vs 'calendar tab'.
 - Bốn họ hiểm: TOGGLE (on/off), NUMBER (30/10), DIRECTION (up/down), CHA-CON (Tools ⊂ Tools & Hardware).

Cổng: AUC(score_SAME > score_DIFF) ≥ 0.80. Rớt = thước CHƯA tách được chỗ K1 chết → KHÔNG train.
Chạy: ~/.venvs/thesis/bin/python harness/metric_v2_validate.py   (cần ollama bge-m3)
"""
import os, json, sys
sys.path.insert(0, os.path.dirname(__file__))
from metric_v2 import target_of, target_score, step_match, J_MATCH

# ---- CA VIẾT TAY (đích đầy đủ câu, để test cả bộ trích target_of) ----
# SAME = cùng nút, khác chữ. Đánh dấu 'k1hard' cho ca KHÔNG chung token (chỗ K1 chết).
SAME = [
    ("Tap the Search bar",            "Tap the search box",                False),
    ("Tap the Search icon",           "Tap the magnifying glass",          True),
    ("Open the menu",                 "Tap the hamburger icon",            True),
    ("Tap the three lines",           "Tap the menu icon",                 True),
    ("Tap the More options",          "Tap the three-dot menu",            True),
    ("Tap Log in",                    "Tap the Sign in button",            True),
    ("Tap the Delete button",         "Tap the Trash icon",                True),
    ("Tap the Settings",              "Tap the gear icon",                 True),
    ("Tap the Compose button",        "Tap the pencil icon",               True),
    ("Tap the filter option",         "Tap the funnel icon",               True),
    ("Tap the back arrow",            "Go back",                           True),
    ("Tap the plus button",           "Tap the add icon",                  True),
    ("Tap the Notifications",         "Tap the bell icon",                 True),
    ("Tap the X",                     "Tap the close button",              True),
    ("Tap the profile picture",       "Tap the avatar",                    True),
    ("Tap the Home tab",              "Tap the Home button",               False),
    ("Tap the Share icon",            "Tap the share button",              False),
    ("Type your email",               "Enter your email address",          False),
    ("Tap the Search bar",            "Click on the search field",         False),
    ("Tap the Next button",           "Tap Continue",                      True),
    ("Tap the checkmark",             "Tap the confirm button",            True),
    ("Tap the Favorites",             "Tap the star icon",                 True),
    ("Tap the overflow menu",         "Tap the three dots",                True),
    ("Tap the Send button",           "Tap the paper plane icon",          True),
    ("Scroll down",                   "Swipe up to scroll down",           False),
]
# DIFF = nút khác, có chồng token (khó — cùng loại nút, khác thực thể). Thước PHẢI bác.
DIFF = [
    ("Tap the Gmail tab",             "Tap the Calendar tab",              "overlap"),
    ("Tap the artworks tab",          "Tap the energy tab",                "overlap"),
    ("Tap the Search bar",            "Tap the Address bar",               "overlap"),
    ("Tap the Settings menu",         "Tap the File menu",                 "overlap"),
    ("Tap the Home tab",              "Tap the Profile tab",               "overlap"),
    ("Tap the Save button",           "Tap the Cancel button",             "overlap"),
    ("Tap the Bcc field",             "Tap the Cc field",                  "overlap"),
    ("Tap the first result",          "Tap the third result",             "overlap"),
    ("Tap the Inbox",                 "Tap the Outbox",                    "overlap"),
    ("Tap the Reply button",          "Tap the Forward button",            "overlap"),
    ("Type the subject",              "Type the message body",             "overlap"),
    ("Tap the Photos tab",            "Tap the Videos tab",                "overlap"),
    ("Tap the Username field",        "Tap the Password field",            "overlap"),
    ("Tap the Add to cart",           "Tap the Buy now",                   "diff"),
    ("Tap the Volume up",             "Tap the Brightness up",             "overlap"),
]
# Bốn họ hiểm — thước PHẢI bác (đây là chỗ v1 khớp OAN)
HIEM = [
    ("Turn on notifications",         "Turn off notifications",            "toggle"),
    ("Tap Enable location",           "Tap Disable location",              "toggle"),
    ("Tap Show password",             "Tap Hide password",                 "toggle"),
    ("Scroll up",                     "Scroll down",                       "direction"),
    ("Tap Mute",                      "Tap Unmute",                        "toggle"),
    ("Set the timer to 30 minutes",   "Set the timer to 10 minutes",       "number"),
    ("Enter quantity 5",              "Enter quantity 2",                  "number"),
    ("Tap the first item",            "Tap the second item",               "ordinal"),
    ("Tap Tools",                     "Tap Tools & Hardware",              "cha-con"),
    ("Tap Settings",                  "Tap Settings & Privacy",            "cha-con"),
    ("Tap the Add button",            "Tap the Remove button",             "toggle"),
]


def auc(pos, neg):
    if not pos or not neg:
        return float("nan")
    c = sum((1 if p > n else 0.5 if p == n else 0) for p in pos for n in neg)
    return c / (len(pos) * len(neg))


def main():
    print("=" * 82)
    print("CỔNG v2 — ca THẬT viết tay, độc lập target_of()")
    print("=" * 82)

    same_sc, diff_sc, hiem_sc = [], [], []
    fp_same, k1_fail = [], []          # SAME bị bác oan
    fn_diff = []                       # DIFF bị khớp oan
    print("\n[SAME] cùng nút khác chữ — thước PHẢI khớp (score ≥ %.2f):" % J_MATCH)
    for m, g, k1hard in SAME:
        ok, sc, adj = step_match(m, g)
        same_sc.append(sc if sc >= 0 else 0.0)
        tag = "k1-khó" if k1hard else ""
        bad = "" if ok else "  ✗ BÁC OAN"
        if not ok:
            fp_same.append((m, g, sc))
            if k1hard:
                k1_fail.append((m, g, sc))
        print(f"    {sc:+.2f} {'✓' if ok else '✗'} {tag:7} | {m!r:34} ~ {g!r}{bad}")

    print("\n[DIFF] nút khác có chồng token — thước PHẢI bác (score < %.2f):" % J_MATCH)
    for m, g, why in DIFF:
        ok, sc, adj = step_match(m, g)
        diff_sc.append(sc if sc >= 0 else 0.0)
        bad = "  ✗ KHỚP OAN" if ok else ""
        if ok:
            fn_diff.append((m, g, sc))
        print(f"    {sc:+.2f} {'✗KHỚP' if ok else '✓bác'} {why:8} | {m!r:32} ~ {g!r}{bad}")

    print("\n[HIỂM] toggle/số/hướng/cha-con — thước PHẢI bác:")
    for m, g, fam in HIEM:
        ok, sc, adj = step_match(m, g)
        hiem_sc.append(sc if sc >= 0 else 0.0)
        bad = "  ✗ KHỚP OAN" if ok else ""
        if ok:
            fn_diff.append((m, g, sc))
        print(f"    {sc:+.2f} {'✗KHỚP' if ok else '✓bác'} {fam:10} | {m!r:32} ~ {g!r}{bad}")

    neg_all = diff_sc + hiem_sc
    A = auc(same_sc, neg_all)
    det = sum(1 for s in neg_all if s < J_MATCH) / len(neg_all)
    fp = len(fp_same) / len(SAME)

    print("\n" + "=" * 82)
    print(f"  SAME  TB = {sum(same_sc)/len(same_sc):.3f}  (n={len(SAME)})")
    print(f"  DIFF  TB = {sum(diff_sc)/len(diff_sc):.3f}  (n={len(DIFF)})")
    print(f"  HIỂM  TB = {sum(hiem_sc)/len(hiem_sc):.3f}  (n={len(HIEM)})")
    print(f"\n  ★ AUC(SAME > DIFF∪HIỂM) = {A:.3f}   [cổng ≥ 0.80]")
    print(f"    detection nút-khác (nên ≥0.90) = {det:.3f}")
    print(f"    false-positive SAME bị bác oan (nên ≤0.15) = {fp:.3f}  ({len(fp_same)}/{len(SAME)})")
    print(f"    trong đó ca K1-khó (không chung token) bị bác oan = {len(k1_fail)}/"
          f"{sum(1 for _,_,h in SAME if h)}")
    print(f"    DIFF/HIỂM bị khớp oan = {len(fn_diff)}")
    verdict = "✅ QUA CỔNG" if (A >= 0.80 and det >= 0.90 and fp <= 0.15) else "❌ RỚT CỔNG"
    print(f"\n  {verdict}")
    if fn_diff:
        print("\n  Khớp-oan (nút khác mà thước cho là cùng) — lỗi NGUY HIỂM (thổi phồng coverage):")
        for m, g, s in fn_diff:
            print(f"    {s:.2f} | {m!r} ~ {g!r}")
    if k1_fail:
        print("\n  Bác-oan ca K1-khó (cùng nút khác chữ, không chung token) — bge không cứu:")
        for m, g, s in k1_fail:
            print(f"    {s:.2f} | {m!r} ~ {g!r}")

    json.dump({"auc": A, "detection_diff": det, "fp_same": fp,
               "same_mean": sum(same_sc)/len(same_sc), "diff_mean": sum(diff_sc)/len(diff_sc),
               "hiem_mean": sum(hiem_sc)/len(hiem_sc),
               "n_same": len(SAME), "n_diff": len(DIFF), "n_hiem": len(HIEM),
               "k1hard_fail": len(k1_fail), "diff_matched_wrongly": len(fn_diff),
               "verdict": verdict},
              open(os.path.join(os.path.dirname(__file__), "metric_v2_results.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("\nĐã lưu metric_v2_results.json")


if __name__ == "__main__":
    main()
