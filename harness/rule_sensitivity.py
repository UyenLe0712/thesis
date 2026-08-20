# -*- coding: utf-8 -*-
"""FREE · offline — ba nhánh chấm lại dưới NĂM luật trúng khác nhau.

Hai phản biện độc lập (16/8) đều nêu cùng một đòn: công thức in trong bài không phải
công thức đang chạy, và bài chưa bao giờ đo xem kết luận có phụ thuộc luật hay không.
Đây là phép đo trả lời đòn đó. Nếu thứ tự ba nhánh giữ nguyên qua cả năm luật thì chỗ
yếu (mô tả lệch mã) biến thành chỗ mạnh (kết luận bền với lựa chọn luật).

Năm luật:
  disk_l2    ‖p−g‖ ≤ 0,14·W                     — đĩa Euclid, đúng như bài từng viết
  disk_rect  |dx| ≤ 0,14·W và |dy| ≤ 0,14·H     — hộp theo trục, đúng như mã chạy
  cell_code  hộp ∧ không tâm nào gần p hơn g    — luật đang triển khai (hạt = g)
  cell_text  hộp ∧ argmin‖c(e)−p‖ = e*          — đúng như bài từng viết (hạt = tâm hộp đích)
  near_box   hộp ∧ mọi hộp KHÔNG chứa g đều xa hơn — bản dùng hộp thay tâm

Chạy: ~/.venvs/thesis/bin/python harness/rule_sensitivity.py
"""
import os, sys, json, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a11y_inventory as A11Y
import metric_exec as M

RUNS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../runs"))
N = 700
SEED = 20260805


def load(p):
    return {(r["episode_id"], r["step_id"]): r
            for r in (json.loads(l) for l in open(os.path.join(RUNS, p), encoding="utf-8"))
            if "executable" in r}


def rules(p, g, boxes, cen, wh):
    """Trả phán quyết định vị của năm luật cho một bước."""
    W, H = wh
    d_l2 = math.dist(p, g) <= 0.14 * W
    d_rc = abs(p[0] - g[0]) <= 0.14 * W and abs(p[1] - g[1]) <= 0.14 * H
    out = {"disk_l2": d_l2, "disk_rect": d_rc}

    # cell_code: đúng hàm đang chạy
    out["cell_code"] = M.hit_voronoi(p, g, cen, wh)

    # cell_text: hạt của đích là TÂM hộp nhỏ nhất chứa g, không xoá gì quanh g
    scr = W * H
    inside = [b for b in boxes if M._in_box(g, b) and (b[2]-b[0])*(b[3]-b[1]) < 0.25*scr]
    if inside and d_rc:
        tgt = min(inside, key=lambda b: (b[2]-b[0])*(b[3]-b[1]))
        c_t = ((tgt[0]+tgt[2])/2, (tgt[1]+tgt[3])/2)
        dt = math.dist(p, c_t)
        out["cell_text"] = all(math.dist(p, c) >= dt for c in cen
                               if math.dist(c, c_t) > 1e-6)
    else:
        out["cell_text"] = False

    # near_box: mọi hộp KHÔNG chứa g phải xa p hơn hộp chứa g
    if d_rc:
        own = [b for b in boxes if M._in_box(g, b)]
        oth = [b for b in boxes if not M._in_box(g, b)]
        if own:
            d_own = min(M._box_dist(p, b) for b in own)
            out["near_box"] = all(M._box_dist(p, b) >= d_own for b in oth)
        else:
            out["near_box"] = False
    else:
        out["near_box"] = False
    return out


def main():
    arms = {"Human": load("score_ceiling_human_raw.jsonl"),
            "S1": load("score_s1_seed101_raw.jsonl"),
            "Base": load("score_base_raw.jsonl")}
    K = sorted(set(arms["S1"]) & set(arms["Base"]) & set(arms["Human"]))
    samp = random.Random(SEED).sample(K, N)

    names = ["disk_l2", "disk_rect", "cell_code", "cell_text", "near_box"]
    tally = {a: {r: 0 for r in names} for a in arms}
    n_ok = 0
    for k in samp:
        boxes = A11Y.elements(f"episode_{k[0]}_screenshot_{k[1]}.png")
        if not boxes:
            continue
        n_ok += 1
        cen = [((b[0]+b[2])/2, (b[1]+b[3])/2) for b in boxes]
        for a, d in arms.items():
            r = d[k]
            if not r.get("pred_xy"):
                continue
            v = rules(tuple(r["pred_xy"]), tuple(r["gold_xy"]), boxes, cen, tuple(r["wh"]))
            # điều kiện (i),(ii) giữ nguyên; chỉ đổi phần định vị
            gate = r["action_ok"] and r["toggle_ok"]
            for rn in names:
                tally[a][rn] += int(bool(gate) and v[rn])

    print(f"n = {n_ok} bước dựng lại được cây trợ năng\n")
    print(f"{'luật':<11}" + "".join(f"{a:>9}" for a in arms) + "   S1−Base")
    for rn in names:
        row = {a: tally[a][rn] / n_ok * 100 for a in arms}
        print(f"{rn:<11}" + "".join(f"{row[a]:>8.1f}%" for a in arms)
              + f"   {row['S1']-row['Base']:+6.1f}")


if __name__ == "__main__":
    main()
