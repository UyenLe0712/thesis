# -*- coding: utf-8 -*-
"""Luật khớp chạm ĐẦY ĐỦ của Android in the Wild (Rawles et al., NeurIPS 2023 D&B) — 0 giây GPU.

    python3 harness/luat_aitw_day_du.py      # in bảng + ghi runs/luat_aitw_day_du.json

Chép từ mã gốc `google-research/android_in_the_wild/action_matching.py` (đọc 14/9/2026):
  _check_tap_actions_match = both_in_box  OR  ‖tap1 − tap2‖ ≤ 0,14   (toạ độ yx chuẩn hoá về [0,1])
  _resize_annotation_bounding_boxes: nới hộp 1,4 lần chiều cao và chiều rộng mỗi phía tổng cộng
    top′ = max(0, top − 0,7·h) · left′ = max(0, left − 0,7·w) · h′ = min(1, h + 1,4·h) · w′ = min(1, w + 1,4·w)
    (giữ nguyên cả cách kẹp của mã gốc: kẹp CHIỀU CAO về 1, không kẹp mép dưới)
  và điều kiện loại thao tác phải trùng (ở đây: action_ok ∧ toggle_ok, như mọi cột khác).

Cột `aitw` cũ trong `luat_d3.py` chỉ là vế khoảng cách. Cột mới `aitw_full` thêm vế hộp.
⚠️ Xấp xỉ phải khai: AitW xét MỌI hộp chú thích trên màn (hai điểm cùng nằm trong một hộp nào đó);
ở đây chỉ có hộp phần tử vàng trong `descriptors.jsonl` ⇒ vế hộp = điểm dự đoán nằm trong hộp vàng đã
nới (điểm vàng luôn nằm trong hộp vàng). Cách xấp xỉ này chỉ có thể cho điểm THẤP hơn luật gốc.
Bước thiếu hộp chỉ còn vế khoảng cách.
"""
import json, math, os
import luat_d3 as L


def aitw_full(r, k):
    g = int(r["action_ok"] and r["toggle_ok"])
    if not g or not r.get("pred_xy"):
        return 0
    (x, y), (gx, gy), (w, h) = r["pred_xy"], r["gold_xy"], r["wh"]
    if math.hypot((x - gx) / w, (y - gy) / h) <= .14:
        return 1
    d = L.D.get(k)
    if not d or not d.get("box"):
        return 0
    x1, y1, x2, y2 = d["box"]
    top, left, bh, bw = y1 / h, x1 / w, (y2 - y1) / h, (x2 - x1) / w
    top2, left2 = max(0, top - 0.7 * bh), max(0, left - 0.7 * bw)
    bh2, bw2 = min(1, bh + 1.4 * bh), min(1, bw + 1.4 * bw)
    py, px, gy_, gx_ = y / h, x / w, gy / h, gx / w
    inb = lambda yy, xx: top2 <= yy <= top2 + bh2 and left2 <= xx <= left2 + bw2
    return int(inb(py, px) and inb(gy_, gx_))


def main():
    out = {"n4463": {}, "lat800": {}}
    print(f"{'nhánh':22s} {'AitW khoảng cách':>17s} {'AitW đầy đủ':>12s} {'D.3':>7s} {'exec':>7s}")
    for ten, tep in L.NHANH:
        R = L.nap(os.path.join(L.RUNS, tep))
        n = len(R)
        a = sum(L.luat(r, k)["aitw"] for k, r in R.items()) / n * 100
        f = sum(aitw_full(r, k) for k, r in R.items()) / n * 100
        d3 = sum(L.luat(r, k)["d3"] for k, r in R.items()) / n * 100
        e = sum(int(r["executable"]) for r in R.values()) / n * 100
        out["n4463"][ten] = dict(aitw=round(a, 2), aitw_full=round(f, 2), d3=round(d3, 2), vor=round(e, 2), n=n)
        print(f"{ten:22s} {a:17.2f} {f:12.2f} {d3:7.2f} {e:7.2f}")

    f1 = L.nap(os.path.join(L.RUNS, L.SAN[0][1])); K = sorted(f1)
    print(f"\nLát 800 (sàn):")
    for ten, tep in [("trần (câu chuẩn)", L.NHANH[0][1])] + L.SAN:
        R = L.nap(os.path.join(L.RUNS, tep))
        f = sum(aitw_full(R[k], k) for k in K) / len(K) * 100
        a = sum(L.luat(R[k], k)["aitw"] for k in K) / len(K) * 100
        out["lat800"][ten] = dict(aitw=round(a, 2), aitw_full=round(f, 2))
        print(f"  {ten:28s} AitW khoảng cách {a:6.2f} · AitW đầy đủ {f:6.2f}")
    p = os.path.join(L.RUNS, "luat_aitw_day_du.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", os.path.relpath(p))


if __name__ == "__main__":
    main()
