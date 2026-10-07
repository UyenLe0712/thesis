# -*- coding: utf-8 -*-
"""
PATA · cổng cuối C1 dưới NHIỀU THƯỚC (exec · D.3 · D.3∧14% · AitW đầy đủ) — 0 GPU, đọc tệp thô.

Cùng định nghĩa với `luat_d3.py` và `luat_aitw_day_du.py` (tập test), chỉ đổi nguồn hộp vàng sang
`pata/val600.jsonl` trường `box` (pixel, cùng lưới với `pred_xy`; hộp dựng bằng cùng quy tắc nút nhỏ nhất
chứa điểm chạm như `descriptors.jsonl`, rồi kẹp vào khung ảnh). Bước thiếu hộp: D.3 tính TRƯỢT, AitW chỉ
còn vế khoảng cách.
⚠️ Số val600 là số của tập cổng — không trích ra báo như điểm phương pháp.

    ~/.venvs/thesis/bin/python harness/pata_nhieu_thuoc.py --dir runs/pata/cong_c1
"""
import os, json, math, argparse
from pata_cong_c1 import boot

HERE = os.path.dirname(os.path.abspath(__file__))
TEN = ("C1_on", "C1_off", "S_on", "C1_swapD", "C1_swapR")
COT = ("exec", "d3", "d3_gate", "aitw")


def k(x):
    return (x["episode_id"], x["step_id"])


def luat(r, box):
    g = int(r.get("action_ok", 0) and r.get("toggle_ok", 0))
    out = {"exec": int(r.get("executable", 0) or 0), "d3": 0, "d3_gate": 0, "aitw": 0}
    if not g or not r.get("pred_xy"):
        return out
    (x, y), (gx, gy), (w, h) = r["pred_xy"], r["gold_xy"], r["wh"]
    if box:
        x1, y1, x2, y2 = box
        out["d3"] = int(x1 <= x <= x2 and y1 <= y <= y2)
        out["d3_gate"] = int(out["d3"] and r.get("hit_disk", 0))
    if math.hypot((x - gx) / w, (y - gy) / h) <= .14:
        out["aitw"] = 1
    elif box:
        x1, y1, x2, y2 = box
        top, left, bh, bw = y1 / h, x1 / w, (y2 - y1) / h, (x2 - x1) / w
        top2, left2 = max(0, top - 0.7 * bh), max(0, left - 0.7 * bw)
        bh2, bw2 = min(1, bh + 1.4 * bh), min(1, bw + 1.4 * bw)
        inb = lambda yy, xx: top2 <= yy <= top2 + bh2 and left2 <= xx <= left2 + bw2
        out["aitw"] = int(inb(y / h, x / w) and inb(gy / h, gx / w))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--data-root", default=os.path.join(HERE, "dg1_cache", "train_ac"))
    a = ap.parse_args()
    BOX = {k(x): x.get("box") for x in map(json.loads, open(os.path.join(a.data_root, "pata", "val600.jsonl")))}
    S = {}
    for t in TEN:
        R = {k(x): x for x in map(json.loads, open(os.path.join(a.dir, f"score_{t}_raw.jsonl"), encoding="utf-8"))}
        S[t] = {kk: luat(r, BOX.get(kk)) for kk, r in R.items()}
    kq = {"diem": {}, "hieu": {}, "n_thieu_hop": sum(1 for v in BOX.values() if not v)}
    print(f"{'biến thể':10} {'n':>4} " + " ".join(f"{c:>8}" for c in COT))
    for t in TEN:
        n = len(S[t])
        kq["diem"][t] = {c: 100 * sum(v[c] for v in S[t].values()) / n for c in COT} | {"n": n}
        print(f"{t:10} {n:4} " + " ".join(f"{kq['diem'][t][c]:8.2f}" for c in COT))
    print("\nhiệu ghép cặp (điểm %), KTC95 bootstrap cụm theo episode:")
    for a_, b_ in (("C1_on", "S_on"), ("C1_on", "C1_off"), ("C1_swapD", "C1_swapR")):
        ks = sorted(set(S[a_]) & set(S[b_]))
        kq["hieu"][f"{a_}-{b_}"] = {}
        for c in COT:
            m, lo, ci = boot([(kk[0], S[a_][kk][c] - S[b_][kk][c]) for kk in ks])
            hon = sum(S[a_][kk][c] > S[b_][kk][c] for kk in ks); kem = sum(S[a_][kk][c] < S[b_][kk][c] for kk in ks)
            kq["hieu"][f"{a_}-{b_}"][c] = {"delta": 100 * m, "ktc95": [100 * ci[0], 100 * ci[1]], "hon": hon, "kem": kem}
            print(f"  {a_:8} − {b_:8} {c:8} {100*m:+6.2f}  [{100*ci[0]:+6.2f}; {100*ci[1]:+6.2f}]  hơn {hon} / kém {kem}")
    json.dump(kq, open(os.path.join(a.dir, "nhieu_thuoc.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
