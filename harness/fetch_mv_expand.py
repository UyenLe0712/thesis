# -*- coding: utf-8 -*-
"""Mo rong MobileViews: lay APP MOI tu cac shard khac, bo qua app da co. Target ~+12 app moi."""
import os, re, json, glob
from datasets import load_dataset

OUT = os.path.join(os.path.dirname(__file__), "..", "dataset_samples", "mv_multiapp")
MAX_PER_APP = int(os.environ.get("MAX_PER_APP", "5"))
NEW_APPS    = int(os.environ.get("NEW_APPS", "12"))
SCAN_CAP    = int(os.environ.get("SCAN_CAP", "12000"))
MIN_ACT     = int(os.environ.get("MIN_ACT", "6"))
SHARDS = [
 "MobileViews_Screenshots_ViewHierarchies/Parquets/MobileViews_0-150000.parquet",
 "MobileViews_Screenshots_ViewHierarchies/Parquets/MobileViews_150001-291197.parquet",
]

def existing_prefixes():
    s=set()
    for f in glob.glob(os.path.join(OUT,"*.jpg")):
        b=os.path.basename(f)[:-4]
        s.add(b.rsplit("_s",1)[0])
    return s

def actionable_count(o):
    c=0
    for n in o.get("views",[]):
        if not n.get("bounds"): continue
        lab=(n.get("text") or n.get("content_description") or "").strip()
        if lab and (n.get("clickable") or n.get("editable") or n.get("long_clickable")): c+=1
    return c
def pkg_of(o):
    for n in o.get("views",[]):
        if n.get("package"): return n["package"]
    return None

def main():
    have=existing_prefixes()
    print(f"App da co: {len(have)}")
    new_per={}; saved=0
    for shard in SHARDS:
        if len(new_per)>=NEW_APPS: break
        print("SHARD:", shard.split('/')[-1])
        ds=load_dataset("mllmTeam/MobileViews", data_files=shard, streaming=True, split="train")
        scanned=0
        for row in ds:
            scanned+=1
            if scanned>SCAN_CAP: break
            try: o=json.loads(row["json_content"])
            except: continue
            pkg=pkg_of(o)
            if not pkg: continue
            pre=re.sub(r'[^a-z0-9]','',pkg.lower())[:20]
            if not pre or pre in have: continue
            if pre not in new_per and len(new_per)>=NEW_APPS: continue
            if new_per.get(pre,0)>=MAX_PER_APP: continue
            if actionable_count(o)<MIN_ACT: continue
            n=new_per.get(pre,0)+1
            name=f"{pre}_s{n}"
            open(os.path.join(OUT,name+".jpg"),"wb").write(row["image_content"])
            open(os.path.join(OUT,name+".viewhierarchy.json"),"w",encoding="utf-8").write(row["json_content"])
            new_per[pre]=n; saved+=1
            if saved%8==0: print(f"  scanned {scanned} | new apps {len(new_per)} | saved {saved}")
        print(f"  (shard done, scanned {scanned})")
    print(f"\nDONE: +{len(new_per)} app moi, +{saved} man")
    for a,c in sorted(new_per.items()): print(f"  {a}: {c}")

if __name__=="__main__": main()
