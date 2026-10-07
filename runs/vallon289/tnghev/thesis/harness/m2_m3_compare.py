# -*- coding: utf-8 -*-
"""M2 vs M3 tren CUNG mot khong gian ung vien - hieu so moi co nghia.

Ban truoc do M3 tren tap ung vien loc theo CLASS, con M2 loc theo ROLE tren
toan bo phan tu hien thi. Hai khong gian khac nhau -> hieu so khong dung duoc.
File nay do ca hai tren cung:

  - Universe U   : moi phan tu hien thi (>=8px, bo thanh he thong), gop nut long nhau.
  - Luat duy nhat: sau khi ap bo loc, con dung MOT phan tu va do la target.
  - `<point>`    : BO khoi moi phep loc (cau cho nguoi khong chua toa do).

M2 = bo loc la (role, name, hint) cua mo ta vang hien tai.
M3 = bo loc la cac thuoc tinh do Incremental Algorithm (Dale & Reiter 1995) chon.

Chay:  python3 m2_m3_compare.py
CPU, khong GPU, khong mang.

Chep tu anh 22/9 (report/anh_183_ma_nguon_22_9). Chi doi REPO/ZIP sang kho WSL.
"""
import json
import math
import os
import pickle
import re
import sys
import zipfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TEST = os.path.join(REPO, "harness", "dg1_cache", "test_ac")
ZIP = os.environ.get("FOREST_ZIP") or os.path.expanduser(
    "~/.cache/huggingface/hub/datasets--HarrytheOrange--parsed_AndroidControl/"
    "snapshots/131de08594daf4deb1b10091d50ec4cfc576b397/all_forest_dict.zip")

sys.path.insert(0, os.path.join(REPO, "harness"))
import descriptor_label_build as D  # noqa: E402

ANCHOR_MAX_PX = D.ANCHOR_MAX_PX
ANCHOR_RE = re.compile(
    r"(just below|just above|to the right of|to the left of) the text “(.+?)”")


# ---------------------------------------------------------------- universe
def raw_nodes(obj):
    out = []
    for win in obj:
        if win.get("window_type") == 3:
            continue
        for n in win.get("tree", []):
            if not n.get("is_visible_to_user"):
                continue
            b = n.get("bounds_in_screen") or {}
            box = (b.get("left", 0), b.get("top", 0), b.get("right", 0), b.get("bottom", 0))
            if box[2] - box[0] < 8 or box[3] - box[1] < 8:
                continue
            cls = (n.get("class_name") or "").split(".")[-1]
            nm = (n.get("text") or "").strip() or (n.get("content_description") or "").strip()
            out.append({"b": box, "c": cls, "raw": nm})
    return out


def area(e):
    b = e["b"]
    return (b[2] - b[0]) * (b[3] - b[1])


def ctr(e):
    b = e["b"]
    return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)


def collapse(nodes, target_box):
    """Gop nut long nhau: mot doi tuong thi giac chi con mot ung vien.

    Giu nut nho nhat truoc (nut la mang chu), nhung LUON giu target.
    """
    kept = []
    tgt = [e for e in nodes if e["b"] == target_box]
    kept.extend(tgt[:1])
    for e in sorted((x for x in nodes if x["b"] != target_box), key=area):
        if any(D.overlapped(e["b"], k["b"]) for k in kept):
            continue
        kept.append(e)
    return kept


def role_of(cls):
    return D.ROLE.get(cls) or ("item" if cls in D.GENERIC else "element")


def anchors_for(e, name, ocr_rec):
    cx, cy = ctr(e)
    low = (name or "").strip().lower()
    out = []
    for t in (ocr_rec or {}).get("items") or []:
        tx, ty, txt = t.get("cx"), t.get("cy"), (t.get("text") or "").strip()
        if tx is None or ty is None or not txt:
            continue
        b = e["b"]
        if b[0] <= tx <= b[2] and b[1] <= ty <= b[3]:
            continue
        if txt.lower() == low or sum(ch.isalnum() for ch in txt) < 2:
            continue
        d = math.hypot(tx - cx, ty - cy)
        if d > ANCHOR_MAX_PX:
            continue
        if abs(ty - cy) >= abs(tx - cx):
            rel = "just below" if ty < cy else "just above"
        else:
            rel = "to the right of" if tx < cx else "to the left of"
        out.append((d, rel, txt))
    out.sort()
    return out


def parse_hint(hint):
    spec = {"only_role": False, "dup": None, "same_role_eq": None,
            "same_role_min": None, "anchor": None}
    m = ANCHOR_RE.search(hint)
    if m:
        spec["anchor"] = (m.group(1), m.group(2))
    if hint.startswith("the only "):
        spec["only_role"] = True
    elif re.match(r"^shares a name with (\d+) other", hint):
        spec["dup"] = int(re.match(r"^shares a name with (\d+) other", hint).group(1))
    elif re.match(r"^1 of (\d+) elements of the same kind$", hint):
        spec["same_role_eq"] = int(re.match(r"^1 of (\d+) elements", hint).group(1)) - 1
    elif hint == "many elements of the same kind on screen":
        spec["same_role_min"] = 9
    return spec


def m2_survivors(rows_spec, U, names, trole, tname, all_nodes, ocr_rec, loose):
    spec = rows_spec
    out = []
    for e in U:
        if role_of(e["c"]) != trole:
            continue
        if (names[id(e)] or "").strip().lower() != tname:
            continue
        same = [x for x in all_nodes
                if x["c"] == e["c"] and x["b"] != e["b"] and not D.overlapped(x["b"], e["b"])]
        k = len(same)
        if spec["only_role"] and k != 0:
            continue
        if spec["same_role_eq"] is not None and k != spec["same_role_eq"]:
            continue
        if spec["same_role_min"] is not None and k < spec["same_role_min"]:
            continue
        if spec["dup"] is not None:
            low = (names[id(e)] or "").strip().lower()
            dup = 0
            if low:
                for x in all_nodes:
                    if x["b"] == e["b"] or D.overlapped(x["b"], e["b"]):
                        continue
                    if (names.get(id(x)) or "").strip().lower() == low:
                        dup += 1
            if dup != spec["dup"]:
                continue
        if spec["anchor"] is not None:
            want_rel, want_txt = spec["anchor"]
            opts = anchors_for(e, names[id(e)], ocr_rec)
            if not opts:
                continue
            if loose:
                ok = any(r == want_rel and t == want_txt for _, r, t in opts)
            else:
                ok = (opts[0][1] == want_rel and opts[0][2] == want_txt)
            if not ok:
                continue
        out.append(e["b"])
    return list(dict.fromkeys(out))


def ia_unique(U, target, names, ocr_rec, allow_ordinal):
    """Incremental Algorithm: them thuoc tinh cho toi khi distractor rong."""
    alive = list(U)

    def narrow(fn):
        nonlocal alive
        tv = fn(target, alive)
        new = [e for e in alive if fn(e, alive) == tv]
        if new and len(new) < len(alive):
            alive = new
            return True
        return False

    # 1. role
    narrow(lambda e, a: role_of(e["c"]))
    if len(alive) == 1:
        return alive[0]["b"] == target["b"], "role"
    # 2. ten (chi khi target co ten)
    if (names[id(target)] or "").strip():
        narrow(lambda e, a: (names[id(e)] or "").strip().lower())
        if len(alive) == 1:
            return alive[0]["b"] == target["b"], "name"
    # 3. moc chu gan nhat
    def anch(e, a):
        o = anchors_for(e, names[id(e)], ocr_rec)
        return (o[0][1], o[0][2]) if o else None
    if anch(target, alive) is not None:
        narrow(anch)
        if len(alive) == 1:
            return alive[0]["b"] == target["b"], "anchor"
    # 4. vung 3x3 (tren tap con song)
    W = max(e["b"][2] for e in U) or 1
    H = max(e["b"][3] for e in U) or 1
    narrow(lambda e, a: min(2, int(3 * ctr(e)[0] / W)))
    narrow(lambda e, a: min(2, int(3 * ctr(e)[1] / H)))
    if len(alive) == 1:
        return alive[0]["b"] == target["b"], "zone"
    # 5. cuc tri, tinh tren tap con song
    for fn in (lambda e, a: ctr(e)[0] == min(ctr(x)[0] for x in a),
               lambda e, a: ctr(e)[0] == max(ctr(x)[0] for x in a),
               lambda e, a: ctr(e)[1] == min(ctr(x)[1] for x in a),
               lambda e, a: ctr(e)[1] == max(ctr(x)[1] for x in a),
               lambda e, a: area(e) == max(area(x) for x in a),
               lambda e, a: area(e) == min(area(x) for x in a)):
        if fn(target, alive):
            narrow(fn)
            if len(alive) == 1:
                return alive[0]["b"] == target["b"], "extremum"
    # 6. thu tu, chi khi con it ung vien
    if allow_ordinal and len(alive) <= 9:
        order = sorted(alive, key=lambda e: (ctr(e)[1], ctr(e)[0]))
        idx = {id(e): i for i, e in enumerate(order)}
        narrow(lambda e, a: idx.get(id(e)))
        if len(alive) == 1:
            return alive[0]["b"] == target["b"], "ordinal"
    return False, None


# -------------------------------------------------------------------- main
def run(rows, ocr, do_collapse):
    cnt = Counter()
    stop_at = Counter()
    usize = []

    with zipfile.ZipFile(ZIP) as z:
        for r in rows:
            key = f"all_forest_dict/android_control_episode_[{r['episode_id']}]_{r['step_id']}.pkl"
            alln = raw_nodes(pickle.loads(z.read(key)))
            ocr_rec = ocr.get(r["image"])
            w = (ocr_rec or {}).get("w") or 1080
            h = (ocr_rec or {}).get("h") or 2400
            D.SCREEN_AREA[0] = w * h

            tb = tuple(r["box"])
            U = collapse(alln, tb) if do_collapse else list(alln)
            usize.append(len(U))
            names = {}
            for e in alln + U:
                if id(e) in names:
                    continue
                a2 = area(e) / max(w * h, 1)
                nm, _ = D.name_of(e["b"], e["raw"], ocr_rec, a2)
                names[id(e)] = nm
            tgt = next((e for e in U if e["b"] == tb), None)
            if tgt is None:
                cnt["target_collapsed_away"] += 1
                continue

            spec = parse_hint(r["hint"])
            tname = (r["name"] or "").strip().lower()
            for mode, loose in (("loose", True), ("strict", False)):
                s = m2_survivors(spec, U, names, r["role"], tname, alln, ocr_rec, loose)
                cnt[f"m2_{mode}"] += (len(s) == 1 and s[0] == tb)

            for lbl, ao in (("m3_strict", False), ("m3_practical", True)):
                ok, why = ia_unique(U, tgt, names, ocr_rec, ao)
                cnt[lbl] += ok
                if lbl == "m3_practical" and ok:
                    stop_at[why] += 1

    return cnt, stop_at, usize


def main():
    rows = [json.loads(x) for x in open(os.path.join(TEST, "descriptors.jsonl"), encoding="utf-8")]
    ocr = {}
    for line in open(os.path.join(TEST, "ocr.jsonl"), encoding="utf-8"):
        r = json.loads(line)
        ocr[r["image"]] = r
    n = len(rows)

    for do_collapse in (True, False):
        lbl = "GOP nut long nhau" if do_collapse else "KHONG gop (tho)"
        cnt, stop_at, usize = run(rows, ocr, do_collapse)
        print("=" * 62)
        print(f"{lbl}   N = {n}   target bi gop mat: {cnt['target_collapsed_away']}")
        print(f"Universe: trung binh {sum(usize)/len(usize):.1f} ung vien/man, "
              f"max {max(usize)}")
        for k in ("m2_loose", "m2_strict", "m3_strict", "m3_practical"):
            print(f"  {k:<14} {cnt[k]:5}  = {100*cnt[k]/n:6.2f}%")
        print("  --- hieu so (diem) ---")
        for a in ("m3_strict", "m3_practical"):
            for b in ("m2_loose", "m2_strict"):
                print(f"  {a} - {b:<10} = {100*(cnt[a]-cnt[b])/n:+.2f}")
        print("  IA dung o thuoc tinh nao (practical):",
              ", ".join(f"{k}={v}" for k, v in stop_at.most_common()))
        print()


if __name__ == "__main__":
    main()
