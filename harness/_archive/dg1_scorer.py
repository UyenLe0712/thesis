# -*- coding: utf-8 -*-
"""
DG1 SCORER (design E) — chạy CPU, KHÔNG cần GPU.
Chấm một tutorial (gọi nút THEO TÊN) trên một màn MobileViews thật:
  - Hallucination / faithfulness : tên nút tutorial nhắc CÓ thật trên View Hierarchy không?
  - Coverage                     : tutorial có bỏ sót nút actionable quan trọng không?
  - Grounding (point-in-bbox)    : nếu bước có toạ độ click, điểm đó có rơi trong khung nút đã khớp không?

Đây là "oracle bên cạnh" của design E: View Hierarchy chỉ dùng LÚC CHẤM (không cho model xem lúc sinh).
Matcher ở đây là bản RÚT GỌN (chuẩn hoá chuỗi + token-overlap) cho smoke-test;
bản chính thức dùng ALOHa (embedding + Hungarian) như trong report/01_metrics.md.

Bẫy dữ liệu MobileViews đã xử (verify report/12):
  - bounds = [[l,t],[r,b]] LỒNG; có thêm bound_box="l,t,r,b".
  - field width/height trong JSON là RÁC -> dùng kích thước ẢNH thật (PIL).
"""
import json, os, re, glob
from PIL import Image

DATA = os.path.join(os.path.dirname(__file__), "..", "dataset_samples", "mobileviews")

# ---------- nạp màn + trích phần tử ----------
def load_screen(vh_path):
    o = json.load(open(vh_path, encoding="utf-8"))
    img_path = vh_path.replace(".viewhierarchy.json", ".jpg")
    W, H = Image.open(img_path).size           # <-- dùng kích thước ẢNH, KHÔNG đọc field width/height (rác)
    elems = []
    for n in o["views"]:
        b = n.get("bounds")
        if not b:
            continue
        (l, t), (r, bot) = b                   # bounds lồng [[l,t],[r,b]]
        label = (n.get("text") or n.get("content_description") or "").strip()
        actionable = bool(n.get("clickable") or n.get("editable") or n.get("long_clickable"))
        leaf = n.get("child_count", 0) == 0
        if label and (actionable or leaf):
            elems.append({"label": label, "bbox": (l, t, r, bot),
                          "center": ((l + r) // 2, (t + bot) // 2),
                          "actionable": actionable})
    return {"name": os.path.basename(vh_path).split(".")[0], "W": W, "H": H, "elems": elems}

# ---------- matcher rút gọn (chuẩn hoá + token-overlap) ----------
def norm(s):
    return re.sub(r"\s+", " ", s.lower().strip())

def toks(s):
    return set(re.findall(r"\w+", norm(s)))

def match(name, elems, thr=0.5):
    """Trả về phần tử khớp nhất, hoặc None nếu coi là BỊA."""
    nn, nt = norm(name), toks(name)
    best, best_score = None, 0.0
    for e in elems:
        en, et = norm(e["label"]), toks(e["label"])
        if nn == en or nn in en or en in nn:           # khớp chuỗi
            return e, 1.0
        if nt and et:
            j = len(nt & et) / len(nt | et)             # token Jaccard
            if j > best_score:
                best, best_score = e, j
    return (best, best_score) if best_score >= thr else (None, best_score)

def in_bbox(pt, bbox):
    x, y = pt; l, t, r, b = bbox
    return l <= x <= r and t <= y <= b

# ---------- chấm 1 tutorial ----------
def score(screen, steps):
    elems = screen["elems"]
    actionable = [e for e in elems if e["actionable"]] or elems
    mentioned, hallucinated, grounded, with_click = [], [], 0, 0
    rows = []
    for s in steps:
        e, sc = match(s["name"], elems)
        if e is None:
            hallucinated.append(s["name"])
            rows.append((s["name"], "BIA (khong co tren man)", "-"))
        else:
            mentioned.append(e["label"])
            g = "-"
            if s.get("click"):
                with_click += 1
                ok = in_bbox(s["click"], e["bbox"])
                grounded += ok
                g = "TRUNG" if ok else "TRUOT"
            rows.append((s["name"], "khop: " + e["label"], g))
    total = len(steps)
    her = len(hallucinated) / total if total else 0.0
    cov = len(set(mentioned)) / len(actionable) if actionable else 0.0
    grd = grounded / with_click if with_click else None
    return {"rows": rows, "HER": her, "faithfulness": 1 - her,
            "coverage": cov, "grounding": grd,
            "n_actionable": len(actionable), "n_mentioned": len(set(mentioned))}

# ---------- demo: tạo 2 tutorial (tốt / có lỗi) cho mỗi màn ----------
def build_demo(screen):
    acts = [e for e in screen["elems"] if e["actionable"]] or screen["elems"]
    labs = [e["label"] for e in acts]
    good = [{"name": e["label"], "click": e["center"]} for e in acts[:3]]   # nhắc nút thật + click đúng tâm
    bad = []
    if labs:
        e0 = acts[0]
        off = (e0["bbox"][2] + 40, e0["bbox"][3] + 40)                      # toạ độ lệch ra ngoài nút
        bad.append({"name": labs[0], "click": off})                        # nút thật nhưng click TRƯỢT
    bad.append({"name": "Cài đặt", "click": (10, 10)})                     # nút BỊA (không có trên màn)
    return good, bad

def pct(x):
    return "--" if x is None else f"{x*100:5.1f}%"

if __name__ == "__main__":
    vhs = sorted(glob.glob(os.path.join(DATA, "*.viewhierarchy.json")))
    print("=" * 78)
    print("DG1 SMOKE-TEST (design E) — chay tren MobileViews that, CPU, khong GPU")
    print("=" * 78)
    for vh in vhs:
        sc = load_screen(vh)
        print(f"\n### MAN: {sc['name']}  | anh {sc['W']}x{sc['H']} | "
              f"{len(sc['elems'])} phan tu co nhan, {sum(e['actionable'] for e in sc['elems'])} actionable")
        labs = [e["label"] for e in sc["elems"] if e["actionable"]][:6]
        print("    nut actionable (mau):", " | ".join(labs) if labs else "(khong)")
        good, bad = build_demo(sc)
        for tag, steps in [("TUTORIAL TOT", good), ("TUTORIAL CO LOI (bia + bo sot + click truot)", bad)]:
            r = score(sc, steps)
            print(f"\n  -- {tag} ({len(steps)} buoc)")
            for nm, res, g in r["rows"]:
                print(f"       buoc '{nm}': {res}  [grounding: {g}]")
            print(f"     => faithfulness(1-HER)={pct(r['faithfulness'])}  "
                  f"coverage={pct(r['coverage'])} ({r['n_mentioned']}/{r['n_actionable']})  "
                  f"grounding={pct(r['grounding'])}")
    print("\n" + "=" * 78)
    print("KET LUAN: bo cham phan biet duoc tutorial TOT (faithfulness cao, grounding TRUNG)")
    print("vs tutorial LOI (faithfulness tut vi bia, grounding TRUOT). -> nua-cham CHAY DUOC.")
    print("=" * 78)
