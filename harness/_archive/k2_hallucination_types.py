# -*- coding: utf-8 -*-
"""
K2 — Đếm phân loại kiểu BỊA THẬT trên output teacher gpt-4o-mini đã cache (report/72 VIỆC 0b).
Không gọi API mới: đọc 80 file harness/dg1_cache/runs/*.json (mỗi file: câu hỏi + nhãn VH + bước teacher).

Với mỗi bước teacher nhắc tên nút (`element`):
  - VERBATIM : khớp y-chữ/gần-chữ một nhãn VH  -> tham chiếu THẬT, không phải bịa.
  - KHÔNG verbatim: tính cosine (nomic) tới nhãn VH gần nhất:
      * sim >= τ(0.55): matcher NHẬN  -> "vùng mù": có thể paraphrase-thật HOẶC bịa-gần-nghĩa lọt.
      * sim <  τ:       matcher ĐÁNH BỊA -> bắt được (thường vô-quan).
In hết ca không-verbatim để soi tay + phân bố. Chạy: PYTHONIOENCODING=utf-8 python3 harness/k2_hallucination_types.py
"""
import json, glob, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from k1_matcher_killtest import ensure, cos, _cache

TAU = 0.55
MODEL = "nomic-embed-text"

def norm(s): return re.sub(r"\s+", " ", (s or "").lower().strip())
def toks(s): return set(re.findall(r"\w+", norm(s)))

def verbatim(el, labels):
    ne, te = norm(el), toks(el)
    for l in labels:
        nl, tl = norm(l), toks(l)
        if ne == nl or (len(ne) >= 3 and (ne in nl or nl in ne)):
            return True
        if te and tl and len(te & tl) / len(te | tl) >= 0.7:
            return True
    return False

def best_label(el, labels):
    labels = [l for l in labels if l]
    if not labels:
        return None, 0.0
    ensure(MODEL, [el] + labels)
    e = _cache[(MODEL, el or "")]
    best, arg = -1.0, None
    for l in labels:
        c = cos(e, _cache[(MODEL, l)])
        if c > best:
            best, arg = c, l
    return arg, best

def main():
    rows = []
    for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "dg1_cache", "runs", "*.json"))):
        o = json.load(open(f, encoding="utf-8"))
        labels = o.get("elem_labels") or o.get("actionable_labels") or []
        for s in o.get("base", []):
            el = s.get("element", "")
            if not el:
                continue
            rows.append({"screen": o["screen"], "el": el, "verb": s.get("verb", ""),
                         "note": s.get("note", ""), "labels": labels, "vb": verbatim(el, labels)})
    tot = len(rows)
    nonvb = [r for r in rows if not r["vb"]]
    for r in nonvb:
        r["near"], r["sim"] = best_label(r["el"], r["labels"])

    hi = [r for r in nonvb if r["sim"] >= TAU]
    lo = [r for r in nonvb if r["sim"] < TAU]
    print("=" * 82)
    print(f"K2 — PHÂN LOẠI BỊA THẬT | {tot} bước teacher gpt-4o-mini (80 màn, dữ liệu cache, FREE)")
    print("=" * 82)
    print(f"  VERBATIM (khớp y-chữ nhãn VH → tham chiếu THẬT):  {tot-len(nonvb):3}/{tot} = {(tot-len(nonvb))/tot*100:.1f}%")
    print(f"  KHÔNG verbatim (ứng viên bịa / paraphrase):       {len(nonvb):3}/{tot} = {len(nonvb)/tot*100:.1f}%")
    print(f"     ├─ sim≥{TAU}  matcher NHẬN  → VÙNG MÙ:          {len(hi):3}/{tot} = {len(hi)/tot*100:.1f}% tổng bước")
    print(f"     └─ sim<{TAU}  matcher ĐÁNH BỊA → bắt được:      {len(lo):3}/{tot} = {len(lo)/tot*100:.1f}% tổng bước")
    print()
    print("--- IN HẾT ca KHÔNG verbatim (soi tay: gần-nghĩa-thật? bịa? nút icon VH thiếu nhãn?) ---")
    print(f"    {'zone':7} {'element':26} {'sim':>5}  {'~ nhãn VH gần nhất':22} note")
    for r in sorted(nonvb, key=lambda x: -x["sim"]):
        zone = "HI(mù)" if r["sim"] >= TAU else "lo(bắt)"
        print(f"    {zone:7} {r['el'][:26]:26} {r['sim']:.3f}  {str(r['near'])[:22]:22} {r['note'][:38]}")

    out = os.path.join(os.path.dirname(__file__), "k2_results.json")
    json.dump({"total_steps": tot, "verbatim": tot-len(nonvb), "nonverbatim": len(nonvb),
               "zone_hi_blind": len(hi), "zone_lo_caught": len(lo),
               "nonvb_detail": [{"screen": r["screen"], "el": r["el"], "sim": r["sim"],
                                 "near": r["near"], "note": r["note"]} for r in nonvb]},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nĐã lưu:", out)

if __name__ == "__main__":
    main()
