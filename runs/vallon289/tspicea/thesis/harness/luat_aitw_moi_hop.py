# -*- coding: utf-8 -*-
"""Luật khớp chạm AitW với MỌI khung phần tử trên màn (sát mã gốc hơn) + độ chính xác định vị của
toạ độ mô hình tự khai — 0 giây GPU, chạy CPU vài chục giây.

    python3 harness/luat_aitw_moi_hop.py      # in bảng + ghi runs/luat_aitw_moi_hop.json

(1) `aitw_moi_hop`: mã gốc `android_in_the_wild/action_matching.py` coi hai lần chạm trùng khi
    ‖Δ‖ chuẩn hoá ≤ 0,14 HOẶC tồn tại MỘT khung chú thích (đã nới 1,4×) chứa CẢ HAI điểm. Mã gốc dùng
    mọi khung chú thích của màn; `luat_aitw_day_du.py` chỉ có khung phần tử vàng (cận dưới). Ở đây
    dùng khung của mọi phần tử bấm được trong cây trợ năng — đúng tập ứng viên của `som_build.py`
    (hiển thị, có CLICK/LONG_CLICK, ≤ 50% màn, gộp IoU ≥ 0,9) — CỘNG khung vàng. ∧ đúng loại thao tác.
(2) `diem_tu_khai_*`: toạ độ `<point>` mà MIN-DESC / chặng ba tự viết trong ô khai báo, chấm như một
    bộ định vị (không cần loại thao tác, vì ô khai báo không nói thao tác): trong khung vàng (luật
    ScreenSpot / D.3) và theo luật AitW khung vàng. Bước không có `<point>` tính trượt.
Sàn đo trên lát 800 bước của `runs/floor/` bằng đúng luật (1).
"""
import json, math, os, re
import luat_d3 as L
from luat_aitw_day_du import aitw_full

HERE = os.path.dirname(os.path.abspath(__file__))
SOM = {(str(r["episode_id"]), str(r["step_id"])): r["boxes"]
       for r in map(json.loads, open(os.path.join(HERE, "dg1_cache", "som", "som.jsonl"), encoding="utf-8"))}


def noi(box, w, h):
    """Nới khung đúng công thức `_resize_annotation_bounding_boxes` (toạ độ chuẩn hoá, kẹp như mã gốc)."""
    x1, y1, x2, y2 = box
    top, left, bh, bw = y1 / h, x1 / w, (y2 - y1) / h, (x2 - x1) / w
    t2, l2 = max(0, top - 0.7 * bh), max(0, left - 0.7 * bw)
    return t2, l2, t2 + min(1, bh + 1.4 * bh), l2 + min(1, bw + 1.4 * bw)


def trong(yx, k):
    return k[0] <= yx[0] <= k[2] and k[1] <= yx[1] <= k[3]


def aitw_moi_hop(r, k):
    if not (r["action_ok"] and r["toggle_ok"]) or not r.get("pred_xy"):
        return 0
    (x, y), (gx, gy), (w, h) = r["pred_xy"], r["gold_xy"], r["wh"]
    if math.hypot((x - gx) / w, (y - gy) / h) <= .14:
        return 1
    hop = list(SOM.get((str(k[0]), str(k[1])), []))
    d = L.D.get(k)
    if d and d.get("box"):
        hop.append(d["box"])
    p, g = (y / h, x / w), (gy / h, gx / w)
    return int(any(trong(p, kk) and trong(g, kk) for kk in (noi(b, w, h) for b in hop)))


def diem_tu_khai(pred_file):
    """Trả {khoá: (trong_khung_vang, aitw_khung_vang)} cho toạ độ <point> tự khai."""
    out = {}
    for o in map(json.loads, open(pred_file, encoding="utf-8")):
        k = (str(o["episode_id"]), str(o["step_id"]))
        m = re.search(r"<point>\s*(\d+)\s*,\s*(\d+)\s*</point>", o.get("raw") or "")
        d = L.D.get(k)
        if not m or not d or not d.get("box"):
            out[k] = (0, 0); continue
        out[k] = (m.group(1), m.group(2))
    return out


def main():
    res = {"n4463": {}, "lat800": {}, "diem_tu_khai": {}}
    print(f"{'nhánh':22s} {'AitW khung vàng':>16s} {'AitW mọi khung':>15s}")
    for ten, tep in L.NHANH:
        R = L.nap(os.path.join(L.RUNS, tep)); n = len(R)
        a = 100 * sum(aitw_full(r, k) for k, r in R.items()) / n
        b = 100 * sum(aitw_moi_hop(r, k) for k, r in R.items()) / n
        res["n4463"][ten] = dict(aitw_khung_vang=round(a, 2), aitw_moi_khung=round(b, 2), n=n)
        print(f"{ten:22s} {a:16.2f} {b:15.2f}")

    K = sorted(L.nap(os.path.join(L.RUNS, L.SAN[0][1])))
    print("\nLát 800:")
    for ten, tep in [("trần (câu chuẩn)", L.NHANH[0][1])] + L.SAN:
        R = L.nap(os.path.join(L.RUNS, tep))
        a = 100 * sum(aitw_full(R[k], k) for k in K) / len(K)
        b = 100 * sum(aitw_moi_hop(R[k], k) for k in K) / len(K)
        res["lat800"][ten] = dict(aitw_khung_vang=round(a, 2), aitw_moi_khung=round(b, 2))
        print(f"  {ten:28s} khung vàng {a:6.2f} · mọi khung {b:6.2f}")

    print("\nToạ độ mô hình tự khai trong <desc> (4.463 bước chạm):")
    for ten, pf, raw in [("MIN-DESC/101", "preds_min_desc_seed101.jsonl", "score_min_desc_seed101_raw.jsonl"),
                         ("GRPO-point/101", "grpo_point/preds_grpo_point_seed101.jsonl",
                          "grpo_point/score_grpo_point_seed101_raw.jsonl")]:
        R = L.nap(os.path.join(L.RUNS, raw))
        P = {}
        for o in map(json.loads, open(os.path.join(L.RUNS, pf), encoding="utf-8")):
            P[(str(o["episode_id"]), str(o["step_id"]))] = o.get("raw") or ""
        c_box = c_aitw = c_co = 0
        for k, r in R.items():
            m = re.search(r"<point>\s*(\d+)\s*,\s*(\d+)\s*</point>", P.get(k, ""))
            d = L.D.get(k)
            if not m or not d or not d.get("box"):
                continue
            c_co += 1
            (w, h), (gx, gy) = r["wh"], r["gold_xy"]
            px, py = int(m.group(1)) / 1000 * w, int(m.group(2)) / 1000 * h
            x1, y1, x2, y2 = d["box"]
            c_box += int(x1 <= px <= x2 and y1 <= py <= y2)
            kk = noi(d["box"], w, h)
            c_aitw += int(math.hypot((px - gx) / w, (py - gy) / h) <= .14 or trong((py / h, px / w), kk))
        n = len(R)
        res["diem_tu_khai"][ten] = dict(co_point=c_co, trong_khung_vang=round(100 * c_box / n, 2),
                                        aitw_khung_vang=round(100 * c_aitw / n, 2), n=n)
        print(f"  {ten:16s} có <point> {c_co} · trong khung vàng {100*c_box/n:6.2f} · AitW khung vàng {100*c_aitw/n:6.2f}")

    p = os.path.join(L.RUNS, "luat_aitw_moi_hop.json")
    json.dump(res, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", os.path.relpath(p))


if __name__ == "__main__":
    main()
