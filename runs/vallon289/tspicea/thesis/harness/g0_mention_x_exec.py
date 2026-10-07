# -*- coding: utf-8 -*-
"""G0: mention (ky hieu ten/OCR, bien >= 2.9) x UGround exec. 0 GPU.

Chep nguyen tu report/183 Phu luc A (anh 07-09). Chi doi RUNS sang runs/ cua kho WSL.
Can m2_m3_compare.py va m9_khop_mem.py (dang o may Mac, CHUA co trong kho).
"""
import json, os, pickle, zipfile
import m2_m3_compare as M
from m9_khop_mem import content, score

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "..", "runs")
D = M.D
THR = 2.9

ARMS = [
    ("nguoi", "score_ceiling_human_raw.jsonl"),
    ("S1", "score_s1_seed101_raw.jsonl"),
    ("CE2", "score_ce2_s2_seed101_raw.jsonl"),
]


def load_arm(fn):
    sent, exe = {}, {}
    for line in open(os.path.join(RUNS, fn), encoding="utf-8"):
        r = json.loads(line)
        k = (int(r["episode_id"]), int(r["step_id"]))
        sent[k] = r.get("sent") or ""
        exe[k] = int(r.get("executable") or 0)
    return sent, exe


def main():
    rows = [json.loads(x) for x in open(os.path.join(M.TEST, "descriptors.jsonl"),
                                        encoding="utf-8")]
    ocr = {}
    for line in open(os.path.join(M.TEST, "ocr.jsonl"), encoding="utf-8"):
        r = json.loads(line)
        ocr[r["image"]] = r
    arms = {n: load_arm(f) for n, f in ARMS}
    ment = {n: {} for n in arms}
    with zipfile.ZipFile(M.ZIP) as z:
        for r in rows:
            k = (r["episode_id"], r["step_id"])
            key = (f"all_forest_dict/android_control_episode_"
                   f"[{r['episode_id']}]_{r['step_id']}.pkl")
            try:
                alln = M.raw_nodes(pickle.loads(z.read(key)))
            except KeyError:
                continue
            rec = ocr.get(r["image"])
            W = (rec or {}).get("w") or 1080
            H = (rec or {}).get("h") or 2400
            D.SCREEN_AREA[0] = W * H
            tb = tuple(r["box"])
            U = M.collapse(alln, tb)
            names = {}
            for e in U:
                names[id(e)], _ = D.name_of(e["b"], e["raw"], rec,
                                            M.area(e) / max(W * H, 1))
            for name, (sents, _) in arms.items():
                s = sents.get(k)
                if s is None:
                    continue
                bag = set(content(s))
                st, other = None, -1.0
                for e in U:
                    sc = score(e, names[id(e)], bag, rec)
                    if e["b"] == tb:
                        st = sc
                    elif sc > other:
                        other = sc
                if st is None:
                    continue
                ment[name][k] = 1 if (st - max(other, 0.0)) >= THR else 0

    def rate(xs):
        return 100.0 * sum(xs) / len(xs) if xs else float("nan")

    print("G0  mention (bien>=2.9)  x  UGround exec")
    print(f"{'nhanh':<8}{'n':>7}{'%ment':>8}{'exec|ment':>12}{'exec|khong':>12}"
          f"{'exec all':>10}")
    stats = {}
    for name, (_, exe) in arms.items():
        ks = [k for k in ment[name] if k in exe]
        m1 = [exe[k] for k in ks if ment[name][k] == 1]
        m0 = [exe[k] for k in ks if ment[name][k] == 0]
        pm = rate([ment[name][k] for k in ks])
        e1, e0, ea = rate(m1), rate(m0), rate([exe[k] for k in ks])
        stats[name] = (len(ks), pm, e1, e0, ea)
        print(f"{name:<8}{len(ks):7d}{pm:8.2f}{e1:12.2f}{e0:12.2f}{ea:10.2f}"
              f"   n_ment={len(m1)} n_khong={len(m0)}")
    print("\nTran suy ra = Delta(%ment) * Delta(exec|ment vs khong) / 100")
    ng = stats["nguoi"]
    for other in ("S1", "CE2"):
        ot = stats[other]
        d_ment = ng[1] - ot[1]
        d_cond = ot[2] - ot[3]
        ceiling = d_ment * d_cond / 100.0
        print(f"  nguoi vs {other}: Delta ment={d_ment:+.2f} pp  "
              f"Delta exec|ment-khong ({other})={d_cond:+.2f} pp  "
              f"tran suy ra={ceiling:+.2f} pp")
        if ceiling >= 3.0:
            print("    => PASS (>= 3.0)")
        elif ceiling < 2.0:
            print("    => FAIL (< 2.0) - rut preference")
        else:
            print("    => NAM GIUA (2.0-3.0) - G4 neu van muon DCRP")


if __name__ == "__main__":
    main()
