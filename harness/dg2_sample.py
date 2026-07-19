# -*- coding: utf-8 -*-
"""
dg2_sample.py — CHON MAU nhieu-man (AndroidControl) tu metadata da scan.

Vao:  dataset_samples/androidcontrol_meta.json  (do scan_androidcontrol.py sinh: episode_id, N, app, atypes)
Ra:   harness/dg2_episodes.json                  (danh sach episode DA CHON de chay DG2)

Quy trinh (bam report/48 + Ch.13 report/43):
  1. CONG KN  : in histogram do dai episode N; kiem N in {4,5,6} co >= FLOOR (41) ep/muc khong.
  2. CHON MAU : phan tang N in {4,5,6}, TOI DA HOA so app khac nhau (round-robin theo app,
                deprioritize app='unknown'), seed co dinh -> tat dinh, tai lap duoc.
  3. Xuat dg2_episodes.json + in tom tat (tong ep / #app / phan bo N / #unknown).

LUU Y: script nay chi CHON episode_id tu metadata (FREE, khong tai anh). Buoc SAU (fetch anh +
gold_action cho cac id da chon de chay pipeline) la mot script rieng, tai du lieu nang hon.

Chay:  PYTHONIOENCODING=utf-8 python harness/dg2_sample.py
Env :  DG2_TARGET (mac dinh 286)  DG2_FLOOR (41)  DG2_SEED (42)  DG2_PERAPP_CAP (0=khong gioi han)
Neu thieu meta -> chay truoc: CAP=1500 python harness/scan_androidcontrol.py
"""
import json, os, collections, random

META = "dataset_samples/androidcontrol_meta.json"
OUT  = "harness/dg2_episodes.json"
NSET = (4, 5, 6)
TARGET   = int(os.environ.get("DG2_TARGET", "286"))
FLOOR    = int(os.environ.get("DG2_FLOOR", "41"))
SEED     = int(os.environ.get("DG2_SEED", "42"))
PERAPP   = int(os.environ.get("DG2_PERAPP_CAP", "0"))   # 0 = khong cap cung (van uu tien da dang)

if not os.path.exists(META):
    raise SystemExit(f"[!] Thieu {META}. Chay truoc: CAP=1500 python harness/scan_androidcontrol.py")

meta = json.load(open(META, encoding="utf-8"))
# de-dup theo episode_id (phong khi scan lap)
seen = {}
for r in meta:
    if r.get("episode_id") is not None and r.get("N") is not None:
        seen[r["episode_id"]] = r
meta = list(seen.values())

# ---------- 1. CONG KN ----------
allN = collections.Counter(r["N"] for r in meta)
print("=" * 56)
print(f"CONG KN — histogram do dai episode (tren {len(meta)} ep da scan)")
print("=" * 56)
for n in sorted(allN):
    bar = "#" * min(allN[n], 60)
    print(f"  N={n:2d}: {allN[n]:4d}  {bar}")

poolN = {n: [r for r in meta if r["N"] == n] for n in NSET}
print(f"\nPool N in {{4,5,6}} (floor >= {FLOOR} ep/muc):")
kn_pass = True
for n in NSET:
    ok = len(poolN[n]) >= FLOOR
    kn_pass = kn_pass and ok
    print(f"  N={n}: {len(poolN[n]):4d} ep  -> {'PASS' if ok else 'FAIL'}")
apps_pool = set(r["app"] for n in NSET for r in poolN[n])
print(f"\n  #app trong pool N in {{4,5,6}}: {len(apps_pool)} (unknown co tinh la 1 nhom)")
print(f"  CONG KN: {'PASS — du de lay mau nhieu-man' if kn_pass else 'FAIL — thu hep claim nhieu-man / tang CAP scan them'}")
if not kn_pass:
    print("  [!] Mot muc N < floor. Van xuat mau nhung PHAI khai gioi han trong luan van.")

# ---------- 2. CHON MAU (toi da hoa da dang app) ----------
random.seed(SEED)
appcount = collections.Counter()
ncount   = collections.Counter()
sel, sel_ids = [], set()

def better(r):
    # nho hon = uu tien hon: (app it dung nhat, app known truoc unknown, ngau nhien tat dinh)
    return (appcount[r["app"]], 1 if r["app"] == "unknown" else 0, random.random())

# 2a. Bao dam FLOOR moi N truoc (uu tien app moi)
for n in NSET:
    for r in sorted(poolN[n], key=better):
        if ncount[n] >= FLOOR:
            break
        if r["episode_id"] in sel_ids:
            continue
        if PERAPP and appcount[r["app"]] >= PERAPP and r["app"] != "unknown":
            continue
        sel.append(r); sel_ids.add(r["episode_id"])
        appcount[r["app"]] += 1; ncount[n] += 1

# 2b. Lap day toi TARGET, moi buoc chon episode lam tang da dang app nhat
remaining = [r for n in NSET for r in poolN[n] if r["episode_id"] not in sel_ids]
while len(sel) < TARGET and remaining:
    remaining.sort(key=better)
    r = remaining.pop(0)
    if PERAPP and appcount[r["app"]] >= PERAPP and r["app"] != "unknown":
        continue
    sel.append(r); sel_ids.add(r["episode_id"])
    appcount[r["app"]] += 1; ncount[r["N"]] += 1

# ---------- 3. Xuat + tom tat ----------
sel_out = [dict(episode_id=r["episode_id"], N=r["N"], app=r["app"], atypes=r.get("atypes"))
           for r in sorted(sel, key=lambda x: (x["N"], x["app"]))]
json.dump(sel_out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

sel_apps = collections.Counter(r["app"] for r in sel)
print("\n" + "=" * 56)
print("MAU DA CHON (dg2_episodes.json)")
print("=" * 56)
print(f"  Tong episode : {len(sel)} (target {TARGET})")
print(f"  So app       : {len(sel_apps)}  (unknown: {sel_apps.get('unknown',0)} ep)")
print(f"  Phan bo N    : {{{', '.join(f'{n}:{ncount[n]}' for n in NSET)}}}")
top = sel_apps.most_common(5)
print(f"  App nhieu ep nhat: {top}")
print(f"  Seed={SEED} (tat dinh) -> {OUT}")

# ---------- 4. TANG N-DAI (bao duong-cong tau/N, chong don "giau ca kho N>=7") ----------
NLONG = (7, 8, 9, 10)
NLONG_TARGET = int(os.environ.get("DG2_NLONG", "48"))
OUT_LONG = "harness/dg2_episodes_Nlong.json"
random.seed(SEED + 1)
poolL = [r for n in NLONG for r in meta if r["N"] == n]
lapp, lN, long_sel, long_ids = collections.Counter(), collections.Counter(), [], set()
def betterL(r):
    return (lapp[r["app"]], 1 if r["app"] == "unknown" else 0, random.random())
while len(long_sel) < NLONG_TARGET and poolL:
    poolL.sort(key=betterL)
    r = poolL.pop(0)
    if r["episode_id"] in long_ids:
        continue
    long_sel.append(r); long_ids.add(r["episode_id"])
    lapp[r["app"]] += 1; lN[r["N"]] += 1
long_out = [dict(episode_id=r["episode_id"], N=r["N"], app=r["app"], atypes=r.get("atypes"))
            for r in sorted(long_sel, key=lambda x: x["N"])]
json.dump(long_out, open(OUT_LONG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\nTANG N-DAI (probe duong-cong tau/N): {len(long_sel)} ep, "
      f"N-dist {{{', '.join(f'{n}:{lN[n]}' for n in NLONG)}}}, #app {len(set(r['app'] for r in long_sel))} -> {OUT_LONG}")

print("\n  BUOC SAU (rieng, tai anh): fetch screenshot + gold_action cho cac episode_id da chon"
      " de chay pipeline DG2 (E8/E9/E14 tren 286 core + duong-cong tau/N tren tang N-dai).")
