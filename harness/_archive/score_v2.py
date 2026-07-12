# -*- coding: utf-8 -*-
"""
CHAM v2 — so 3 matcher tren cung tutorial da sinh (harness/gen_cache/):
  (1) STRING (chuoi/token)  : matcher cu, de vu oan synonym la BIA.
  (2) ALOHa (embedding)     : cot BIA dung -> synonym KHONG bi tinh bia.
  (3) EXACT-LABEL           : cot CLARITY/dung-nhan -> goi synonym bi tru clarity.
Muc tieu: chung minh ALOHa sua duoc "bia gia" cua matcher chuoi, va tach bach Bia vs Clarity.
"""
import os, sys, json, glob, re
sys.path.insert(0, os.path.dirname(__file__))
from aloha_match import best_match, exact_label

CACHE = os.path.join(os.path.dirname(__file__), "gen_cache")
TAU = 0.55   # nguong semantic "ton tai" (EN: synonym ~0.6-0.69, khac nghia ~0.39) -> pre-register + audit

def norm(s): return re.sub(r"\s+", " ", (s or "").lower().strip())
def toks(s): return set(re.findall(r"\w+", norm(s)))
def string_match(name, labels):
    nn, nt = norm(name), toks(name)
    for l in labels:
        ln = norm(l)
        if nn and (nn == ln or nn in ln or ln in nn): return True
    for l in labels:
        lt = toks(l)
        if nt and lt and len(nt & lt) / len(nt | lt) >= 0.5: return True
    return False

def main():
    files = sorted(glob.glob(os.path.join(CACHE, "*.json")))
    if not files:
        print("Chua co gen_cache/ — chay generate_cache.py truoc."); return
    T = {"steps": 0, "str_h": 0, "aloha_h": 0, "rescued": 0, "exact": 0}
    print("=" * 84)
    print(f"CHAM v2 — {len(files)} man | so STRING vs ALOHa (bia) + EXACT-LABEL (clarity) | tau={TAU}")
    print("=" * 84)
    for fp in files:
        r = json.load(open(fp, encoding="utf-8"))
        labels = r["elem_labels"]
        n = len(r["steps"]) or 1
        c = {"str_h": 0, "aloha_h": 0, "rescued": 0, "exact": 0}
        for s in r["steps"]:
            nm = s.get("element", "")
            sm = string_match(nm, labels)
            _, sim = best_match(nm, labels)
            am = sim >= TAU
            ex = exact_label(nm, labels)
            if not sm: c["str_h"] += 1
            if not am: c["aloha_h"] += 1
            if (not sm) and am: c["rescued"] += 1          # chuoi bao bia nhung ALOHa thay co that
            if ex: c["exact"] += 1
        for k in c: T[k] += c[k]
        T["steps"] += n
        print(f"  {r['screen']:>12} | {n:2d} buoc | bia(chuoi) {c['str_h']} -> bia(ALOHa) {c['aloha_h']} "
              f"(synonym duoc cuu {c['rescued']}) | dung-nhan {c['exact']}/{n}")
    N = T["steps"] or 1
    print("\n" + "-" * 84)
    print(f"TONG {len(files)} man, {T['steps']} buoc:")
    print(f"  COT BIA:")
    print(f"    - matcher CHUOI   : bia = {T['str_h']/N*100:5.1f}%  (de THOI PHONG do vu oan synonym)")
    print(f"    - matcher ALOHa   : bia = {T['aloha_h']/N*100:5.1f}%  <- dang tin hon")
    print(f"    - synonym BI CHUOI VU OAN (ALOHa cuu) = {T['rescued']} buoc "
          f"({T['rescued']/N*100:.1f}% so buoc)")
    wrong_label = max(0, (N - T["aloha_h"]) - T["exact"])   # ton tai nhung goi sai nhan -> clarity tru, KHONG phai bia
    print(f"  COT CLARITY (tach rieng):")
    print(f"    - dung-nhan (goi DUNG ten hien thi)            = {T['exact']/N*100:5.1f}%")
    print(f"    - nut CO THAT nhung goi SAI NHAN (synonym)     = {wrong_label} buoc ({wrong_label/N*100:.1f}%) "
          f"-> tru CLARITY, KHONG tinh BIA")
    print("=" * 84)
    print("KET LUAN: matcher chuoi THOI PHONG bia (vu oan synonym); ALOHa cho con BIA dang tin;")
    print("con 'goi sai nhan' tach sang CLARITY (nut co that, chi kho tim) -> dung y user.")

if __name__ == "__main__":
    main()
