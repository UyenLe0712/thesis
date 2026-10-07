# -*- coding: utf-8 -*-
"""FREE · offline — các phép đo mà năm phản biện độc lập 16/8 đòi, gom một lượt.

Chạy: ~/.venvs/thesis/bin/python harness/rasoat_16_8.py
Mọi số in ra đều đi thẳng vào bài FAIR (mục IV-B, IV-C, IV-E, VIII).
"""
import os, sys, json, math, random, statistics, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a11y_inventory as A11Y
import metric_exec as M

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.abspath(os.path.join(HERE, "../runs"))
N_SAMPLE = 600          # đủ hẹp khoảng tin cậy mà không phải bung cả 4.462 màn
SEED = 20260805


def load(p):
    out = {}
    for line in open(os.path.join(RUNS, p), encoding="utf-8"):
        r = json.loads(line)
        if "executable" in r:
            out[(r["episode_id"], r["step_id"])] = r
    return out


def centres_for(ep, st):
    boxes = A11Y.elements(f"episode_{ep}_screenshot_{st}.png")
    return boxes, [((b[0] + b[2]) / 2, (b[1] + b[3]) / 2) for b in boxes]


def main():
    s1, ba, hu = load("score_s1_seed101_raw.jsonl"), load("score_base_raw.jsonl"), load("score_ceiling_human_raw.jsonl")
    K = sorted(set(s1) & set(ba) & set(hu))
    rng = random.Random(SEED)
    samp = rng.sample(K, N_SAMPLE)

    # ── 1. Bán kính gộp xoá mất gì, và sàn phụ thuộc khoảng cách hàng xóm thế nào ──
    n_merged, n_any_merged, n_distinct_inside = 0, 0, 0
    dist_bins = collections.Counter()      # khoảng cách tới hàng xóm gần nhất SAU gộp
    floor_hit = collections.Counter()      # sàn: đặt điểm vào tâm hàng xóm đó
    child_of_target = 0                    # hàng xóm là hộp CHỨA điểm chạm (bộ phận của chính đích)
    ok = 0
    for k in samp:
        r = s1[k]
        boxes, cen = centres_for(*k)
        if not cen:
            continue
        ok += 1
        g, wh = tuple(r["gold_xy"]), tuple(r["wh"])
        ms = M.min_sep_px(wh)
        removed = [c for c in cen if M._dist(c, g) < ms]
        n_merged += len(removed)
        n_any_merged += 1 if removed else 0
        # trong số tâm bị xoá, cái nào thuộc hộp KHÔNG chứa điểm chạm → phần tử riêng biệt
        for c in removed:
            owner = [b for b in boxes if abs((b[0] + b[2]) / 2 - c[0]) < .01 and abs((b[1] + b[3]) / 2 - c[1]) < .01]
            if owner and not M._in_box(g, owner[0]):
                n_distinct_inside += 1
                break
        sites = M.dedupe_buttons(cen, g, wh)
        others = [c for c in sites if M._dist(c, g) > 1e-6]
        if not others:
            continue
        nb = min(others, key=lambda c: M._dist(c, g))
        d = M._dist(nb, g)
        b = "0-63" if d < 63 else "63-100" if d < 100 else "100-150" if d < 150 else "150-250" if d < 250 else ">250"
        dist_bins[b] += 1
        if M.hit_voronoi(nb, g, cen, wh):
            floor_hit[b] += 1
        # hộp bao cả màn (gốc cây, khung nội dung) không phải "phần tử đích" theo
        # nghĩa nào cả — loại trước khi hỏi hàng xóm có phải bộ phận của đích không
        scr = wh[0] * wh[1]
        owner = [bx for bx in boxes
                 if M._in_box(nb, bx) and M._in_box(g, bx)
                 and (bx[2] - bx[0]) * (bx[3] - bx[1]) < 0.25 * scr]
        if owner:
            child_of_target += 1

    print(f"\n=== 1. Phép gộp 24 dp xoá gì (n={ok} màn dựng lại được) ===")
    print(f"  bước có ít nhất một tâm bị xoá: {n_any_merged/ok*100:.1f}%  (trung bình {n_merged/ok:.1f} tâm/bước)")
    print(f"  trong đó có tâm thuộc phần tử RIÊNG BIỆT (hộp không chứa điểm chạm): {n_distinct_inside/ok*100:.1f}% số bước")
    print(f"\n=== 2. Sàn theo khoảng cách tới hàng xóm gần nhất (sau gộp) ===")
    for b in ("63-100", "100-150", "150-250", ">250"):
        n = dist_bins[b]
        if n:
            print(f"  {b:>8} px: {n:4d} bước ({n/sum(dist_bins.values())*100:4.1f}%)  sàn = {floor_hit[b]/n*100:.1f}%")
    print(f"  hàng xóm gần nhất nằm TRONG hộp của chính đích: {child_of_target/ok*100:.1f}% số bước")

    # ── 3. Vùng mù: vì sao câu chuẩn trượt ──
    fails = [k for k in K if hu[k]["executable"] == 0]
    far = sum(1 for k in fails if not hu[k]["hit_disk"])
    near_miss = len(fails) - far
    print(f"\n=== 3. Vùng mù: {len(fails)} bước câu chuẩn trượt ===")
    print(f"  bộ trỏ ra ngoài dung sai (bỏ cuộc): {far} ({far/len(fails)*100:.1f}%)")
    print(f"  trong dung sai nhưng sai ô: {near_miss} ({near_miss/len(fails)*100:.1f}%)")

    # ── 4. Bốn quy tắc gom cụm ──
    def boot(d1, d2, keyfn, B=4000, seed=SEED):
        cl = collections.defaultdict(list)
        for k in K:
            cl[keyfn(k)].append(d1[k]["executable"] - d2[k]["executable"])
        g = list(cl.values())
        r = random.Random(seed)
        out = []
        for _ in range(B):
            s = m = 0
            for _ in range(len(g)):
                v = g[r.randrange(len(g))]
                s += sum(v); m += len(v)
            out.append(s / m * 100)
        out.sort()
        return out[int(.025 * B)], out[int(.975 * B)], len(g)

    print(f"\n=== 4. Kết quả có phụ thuộc quy tắc gom cụm không (Δ = S1 − Base) ===")
    rules = [("app, tác vụ cho unknown (bài dùng)", lambda k: ("app", s1[k]["app"]) if s1[k].get("app") else ("task", k[0])),
             ("mọi bước gom theo tác vụ", lambda k: ("task", k[0])),
             ("app, unknown gộp MỘT cụm", lambda k: ("app", s1[k]["app"]) if s1[k].get("app") else ("unk",))]
    for name, fn in rules:
        lo, hi, G = boot(s1, ba, fn)
        print(f"  {name:38s} G={G:5d}  KTC95 [{lo:+.1f}, {hi:+.1f}]")

    # ── 5. Khoảng tin cậy cho từng lát cắt ──
    def ci_slice(ks, d1, d2, B=4000):
        cl = collections.defaultdict(list)
        for k in ks:
            key = ("app", d1[k]["app"]) if d1[k].get("app") else ("task", k[0])
            cl[key].append(d1[k]["executable"] - d2[k]["executable"])
        g = list(cl.values()); r = random.Random(SEED); out = []
        for _ in range(B):
            s = m = 0
            for _ in range(len(g)):
                v = g[r.randrange(len(g))]
                s += sum(v); m += len(v)
            out.append(s / m * 100)
        out.sort()
        return sum(sum(v) for v in g) / sum(len(v) for v in g) * 100, out[int(.025 * B)], out[int(.975 * B)]

    print(f"\n=== 5. Lát cắt kèm khoảng tin cậy ===")
    thirds = sorted(K, key=lambda k: s1[k]["n_buttons"])
    t = len(thirds) // 3
    for name, ks in [("bước mở đầu (chỉ số 0)", [k for k in K if k[1] == 0]),
                     ("các bước sau", [k for k in K if k[1] != 0]),
                     ("màn ít phần tử", thirds[:t]),
                     ("màn vừa", thirds[t:2 * t]),
                     ("màn nhiều phần tử", thirds[2 * t:])]:
        d, lo, hi = ci_slice(ks, s1, ba)
        print(f"  {name:24s} n={len(ks):5d}  Δ={d:+5.1f}  KTC95 [{lo:+.1f}, {hi:+.1f}]")


if __name__ == "__main__":
    main()
