# -*- coding: utf-8 -*-
"""
DG1 TRIAL #2 — nhieu man hon + matcher STRICT/LOOSE + so BASELINE(raw) vs DESIGN-E(fallback).
Chay tren mv_trace/ (10 man MobileViews trich tu mv.zip, cung 1 app). Ollama/CPU.

Y nghia so:
  - strict  : ten nut khop CHINH XAC nut that tren man (chuoi/substring).
  - loose   : chi khop mo (token overlap) -> nhieu kha nang DONG NGHIA (gioi han matcher).
  - unmatched: khong khop -> UNG VIEN BIA (confident-wrong neu giu nguyen).
  BASELINE (raw)    : giu nguyen buoc unmatched -> phat ra "lenh bam nut sai ma tu tin".
  DESIGN-E (fallback): doi buoc unmatched thanh mo ta bang loi -> 0 confident-wrong (trung thuc).
=> Gia tri design E = bien X% lenh-sai-tu-tin thanh mo ta trung thuc (do duoc).
"""
import os, sys, re, glob
sys.path.insert(0, os.path.dirname(__file__))
from dg1_scorer import load_screen
from run_dg1_trial import call_vlm, parse_steps     # tai dung API + prompt

FOLDER = os.path.join(os.path.dirname(__file__), "..", "dataset_samples", "mv_trace")
Q = ("Trên màn hình này, hãy hướng dẫn người dùng CÁC BƯỚC thao tác chính "
     "(bấm hoặc nhập vào đâu) để dùng chức năng chính của màn. "
     "Gọi ĐÚNG TÊN nút/ô hiển thị, không bịa nút không có.")

def norm(s): return re.sub(r"\s+", " ", s.lower().strip())
def toks(s): return set(re.findall(r"\w+", norm(s)))

def classify(name, elems):
    nn, nt = norm(name), toks(name)
    if not nn: return "unmatched"
    for e in elems:
        en = norm(e["label"])
        if nn == en or nn in en or en in nn:
            return "strict"
    best = 0.0
    for e in elems:
        et = toks(e["label"])
        if nt and et:
            best = max(best, len(nt & et) / len(nt | et))
    return "loose" if best >= 0.5 else "unmatched"

def main():
    for v in ("VLM_BASE_URL", "VLM_MODEL"):
        if not os.environ.get(v):
            print(f"[THIEU] {v}"); return
    vhs = sorted(glob.glob(os.path.join(FOLDER, "*.viewhierarchy.json")))
    print("=" * 80)
    print(f"DG1 TRIAL #2 | model={os.environ['VLM_MODEL']} | {len(vhs)} man | cau hoi CHUNG")
    print("=" * 80)
    T = {"strict": 0, "loose": 0, "unmatched": 0, "steps": 0, "screens": 0}
    for vh in vhs:
        sc = load_screen(vh)
        img = vh.replace(".viewhierarchy.json", ".jpg")
        try:
            steps = parse_steps(call_vlm(img, Q))
        except Exception as ex:
            print(f"  {sc['name']}: LOI {repr(ex)[:90]}"); continue
        c = {"strict": 0, "loose": 0, "unmatched": 0}
        for s in steps:
            c[classify(s.get("element", ""), sc["elems"])] += 1
        n = len(steps) or 1
        T["strict"] += c["strict"]; T["loose"] += c["loose"]; T["unmatched"] += c["unmatched"]
        T["steps"] += n; T["screens"] += 1
        print(f"  {sc['name']:>12} | {n:2d} buoc | strict {c['strict']} / loose {c['loose']} / "
              f"unmatched {c['unmatched']}  -> baseline confident-wrong = {c['unmatched']/n*100:4.0f}%")
    N = T["steps"] or 1
    print("\n" + "-" * 80)
    print(f"TONG {T['screens']} man, {T['steps']} buoc:")
    print(f"  faithfulness STRICT (chac chan dung) = {T['strict']/N*100:5.1f}%")
    print(f"  faithfulness LOOSE  (cho dong nghia) = {(T['strict']+T['loose'])/N*100:5.1f}%")
    print(f"  -> 'that su bia' nam giua 2 con tren (loose={T['loose']} buoc la vung xam matcher)")
    print(f"\n  SO SANH GIA TRI DESIGN E:")
    print(f"    BASELINE (raw)     : confident-wrong (lenh bam nut sai tu tin) = {T['unmatched']/N*100:5.1f}%")
    print(f"    DESIGN-E (fallback): confident-wrong = 0.0%  (doi {T['unmatched']} buoc thanh mo ta bang loi)")
    print("=" * 80)
    print("LUU Y: cau hoi CHUNG + 1 app + matcher chuoi -> tin hieu so bo, chua phai eval chinh thuc.")

if __name__ == "__main__":
    main()
