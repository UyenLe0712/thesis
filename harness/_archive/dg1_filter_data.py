# -*- coding: utf-8 -*-
"""
LOC RAC mv_multiapp (free): bo man co qua it nhan-actionable-SACH; ghi kept_screens.json + manifest sach.
Chay: PYTHONIOENCODING=utf-8 python dg1_filter_data.py   (env: MIN_ACT=5)
"""
import os, sys, glob, json, csv
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from dg1_data import MV_DIR, KEPT_FP, load_labels, clean_elems, is_junk, app_of

MIN_ACT = int(os.environ.get("MIN_ACT", "5"))
OUT_CSV = os.path.join(MV_DIR, "_manifest_clean.csv")

def main():
    files = sorted(glob.glob(os.path.join(MV_DIR, "*.viewhierarchy.json")))
    kept, dropped, rows, junk_examples = [], [], [], []
    for f in files:
        name = os.path.basename(f).split(".")[0]
        elems = load_labels(f)
        clean = clean_elems(elems)
        for e in elems:
            if is_junk(e["label"]) and e["label"].strip() and len(junk_examples) < 14:
                junk_examples.append((name, e["label"][:70]))
        act_clean = sorted({e["label"] for e in clean if e["actionable"]})   # DISTINCT
        rows.append((name, app_of(name), len(elems), len(clean), len(act_clean)))
        (kept if len(act_clean) >= MIN_ACT else dropped).append(
            name if len(act_clean) >= MIN_ACT else (name, len(act_clean)))

    os.makedirs(os.path.dirname(KEPT_FP), exist_ok=True)
    json.dump(kept, open(KEPT_FP, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["screen","app","n_elem","n_clean","n_act_clean"]); w.writerows(rows)

    apps = sorted({app_of(n) for n in kept})
    print("=" * 72)
    print(f"LOC RAC mv_multiapp | MIN_ACT={MIN_ACT} (so nhan-actionable-SACH, DISTINCT, toi thieu)")
    print("=" * 72)
    print(f"Tong man: {len(files)} | GIU: {len(kept)} | BO: {len(dropped)} | so app con: {len(apps)}")
    print(f"\nMAN BI BO:")
    for n, k in dropped:
        print(f"  {n}: {k} nhan-actionable-sach")
    print(f"\nVI DU NHAN RAC bi loc (URL/param/qua-dai):")
    for n, l in junk_examples[:12]:
        print(f"  [{n}] {l}")
    c = Counter(app_of(n) for n in kept)
    print(f"\nMAN/APP sau khi giu ({len(apps)} app):")
    for a, k in sorted(c.items()):
        print(f"  {a}: {k}")
    print(f"\n-> {KEPT_FP} ({len(kept)} man) + _manifest_clean.csv")

if __name__ == "__main__":
    main()
