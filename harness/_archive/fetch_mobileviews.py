# -*- coding: utf-8 -*-
"""
Tai SUBSET DA-APP tu MobileViews (mllmTeam/MobileViews) bang STREAM parquet (khong tai 16-40GB).
Loc: moi man >= MIN_ACT nut actionable-co-nhan; cap MAX_PER_APP man/app; dung khi du TARGET_APPS + TARGET_SCREENS.
Ghi ra dataset_samples/mv_multiapp/<pkgsanitized>_s<n>.jpg + .viewhierarchy.json (khop loader dg1_scorer.load_screen).
+ _manifest.csv (name,package,n_actionable) de truy vet app.

Chay: PYTHONIOENCODING=utf-8 python fetch_mobileviews.py
Env: MV_SHARD, MAX_PER_APP=8, TARGET_APPS=12, TARGET_SCREENS=90, SCAN_CAP=6000, MIN_ACT=5
"""
import os, re, json, csv
from datasets import load_dataset

OUT = os.path.join(os.path.dirname(__file__), "..", "dataset_samples", "mv_multiapp")
os.makedirs(OUT, exist_ok=True)
SHARD = os.environ.get("MV_SHARD", "MobileViews_Screenshots_ViewHierarchies/Parquets/MobileViews_400000-522301.parquet")
MAX_PER_APP   = int(os.environ.get("MAX_PER_APP", "8"))
TARGET_APPS   = int(os.environ.get("TARGET_APPS", "12"))
TARGET_SCREENS= int(os.environ.get("TARGET_SCREENS", "90"))
SCAN_CAP      = int(os.environ.get("SCAN_CAP", "6000"))
MIN_ACT       = int(os.environ.get("MIN_ACT", "5"))

def actionable_count(o):
    c = 0
    for n in o.get("views", []):
        if not n.get("bounds"): continue
        label = (n.get("text") or n.get("content_description") or "").strip()
        if label and (n.get("clickable") or n.get("editable") or n.get("long_clickable")): c += 1
    return c

def pkg_of(o):
    for n in o.get("views", []):
        if n.get("package"): return n["package"]
    return None

def main():
    ds = load_dataset("mllmTeam/MobileViews", data_files=SHARD, streaming=True, split="train")
    per_app = {}; manifest = []; scanned = saved = 0
    for row in ds:
        scanned += 1
        if scanned > SCAN_CAP: break
        try: o = json.loads(row["json_content"])
        except Exception: continue
        pkg = pkg_of(o)
        if not pkg: continue
        prefix = re.sub(r'[^a-z0-9]', '', pkg.lower())[:20]
        if not prefix or per_app.get(prefix, 0) >= MAX_PER_APP: continue
        if actionable_count(o) < MIN_ACT: continue
        n = per_app.get(prefix, 0) + 1
        name = f"{prefix}_s{n}"
        with open(os.path.join(OUT, name + ".jpg"), "wb") as f: f.write(row["image_content"])
        with open(os.path.join(OUT, name + ".viewhierarchy.json"), "w", encoding="utf-8") as f:
            f.write(row["json_content"])
        per_app[prefix] = n; saved += 1
        manifest.append((name, pkg, actionable_count(o)))
        if saved % 10 == 0:
            print(f"  scanned {scanned} | saved {saved} | apps {len(per_app)}")
        if saved >= TARGET_SCREENS and len(per_app) >= TARGET_APPS: break
    with open(os.path.join(OUT, "_manifest.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["name", "package", "n_actionable"]); w.writerows(manifest)
    print(f"\nDONE scanned={scanned} saved={saved} apps={len(per_app)} -> {OUT}")
    for a, c in sorted(per_app.items()): print(f"  {a}: {c}")

if __name__ == "__main__":
    main()
