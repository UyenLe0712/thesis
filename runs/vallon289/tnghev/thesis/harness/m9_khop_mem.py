# -*- coding: utf-8 -*-
"""M9 - lam manh phep cham ky hieu bang KHOP MEM, khong can model nao.

M7/M8 cho thay phep cham ky hieu yeu (r = 0,19 tren nhanh nguoi) vi no chi khop
CHUOI NGUYEN VAN. Cau cua nguoi thuong dien dat lai nen bi cham la "sai" du
Phi-4 van hieu.

Duong embedding no-ron khong chay duoc: `emb_cache.json` bi .gitignore loai khoi
repo, may khong co numpy/torch/sentence-transformers, va tai model tu HuggingFace
thi bi Zscaler chan.

Thay bang KHOP MEM thuan Python, khong phu thuoc gi:
  - F1 theo tu giua ten/chu-OCR cua ung vien va cau,
  - cong khop tien to (stem tho) de bat "song"/"songs", "setting"/"settings",
  - diem co bac = 3.0 * sim, thay cho nhi phan 3.0.

Muc dich: xem `r` va do phan biet co tang so voi M7 khong. Neu tang du nhieu thi
duong (A) - phan thuong ky hieu, 0 GPU, thuoc do doc lap - manh len va nen chon.

Chay:  python3 m9_khop_mem.py

Chep tu anh 22/9 (report/anh_183_ma_nguon_22_9). Chi doi RUNS sang runs/ cua kho WSL.
"""
import json
import os
import pickle
import re
import zipfile

import m2_m3_compare as M

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "..", "runs")
SOM = os.path.join(RUNS, "som")
D = M.D

STOP = {"the", "a", "an", "on", "in", "at", "to", "of", "and", "or", "click",
        "tap", "press", "open", "select", "choose", "button", "icon", "it",
        "this", "that", "screen", "app", "then", "go", "for", "with", "your",
        "my", "is", "are", "be", "you", "please"}


def toks(s):
    return [t for t in re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).split() if t]


def stem(t):
    for suf in ("ing", "ers", "er", "es", "s"):
        if len(t) > 4 and t.endswith(suf):
            return t[: -len(suf)]
    return t


def content(s):
    return [stem(t) for t in toks(s) if t not in STOP and len(t) > 1]


def sim(text, sent_bag):
    """F1 theo tu noi dung giua `text` va cau."""
    a = set(content(text))
    if not a:
        return 0.0
    inter = len(a & sent_bag)
    if not inter:
        return 0.0
    prec = inter / len(a)
    rec = inter / max(len(sent_bag), 1)
    return 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0


def ocr_texts_in(box, ocr_rec):
    out = []
    for t in (ocr_rec or {}).get("items") or []:
        tx, ty = t.get("cx"), t.get("cy")
        if tx is None or ty is None:
            continue
        if box[0] <= tx <= box[2] and box[1] <= ty <= box[3]:
            txt = (t.get("text") or "").strip()
            if sum(c.isalnum() for c in txt) >= 2:
                out.append(txt)
    return out


def score(e, name, sent_bag, ocr_rec):
    best = sim(name, sent_bag) if name else 0.0
    for t in ocr_texts_in(e["b"], ocr_rec):
        s = sim(t, sent_bag)
        if s > best:
            best = s
    return 3.0 * best


def pearson(xs, ys):
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs) ** .5
    dy = sum((y - my) ** 2 for y in ys) ** .5
    return num / (dx * dy) if dx and dy else float("nan")


def main():
    rows = [json.loads(x) for x in open(os.path.join(M.TEST, "descriptors.jsonl"),
                                        encoding="utf-8")]
    ocr = {}
    for line in open(os.path.join(M.TEST, "ocr.jsonl"), encoding="utf-8"):
        r = json.loads(line)
        ocr[r["image"]] = r

    arms = [("nguoi / dich day", "score_ceiling_human_raw.jsonl", "chon_phi4_chuan.jsonl"),
            ("S1", "score_s1_seed101_raw.jsonl", "chon_phi4_s1_101.jsonl"),
            ("duong ong", "grpo_point/score_grpo_point_seed101_raw.jsonl",
             "chon_phi4_grpo.jsonl")]
    sents, listen = {}, {}
    for name, sf, lf in arms:
        p = os.path.join(RUNS, sf)
        if not os.path.exists(p):
            continue
        sents[name] = {}
        for line in open(p, encoding="utf-8"):
            r = json.loads(line)
            sents[name][(int(r["episode_id"]), int(r["step_id"]))] = (r.get("sent") or "")
        listen[name] = {}
        for line in open(os.path.join(SOM, lf), encoding="utf-8"):
            r = json.loads(line)
            listen[name][(int(r["episode_id"]), int(r["step_id"]))] = int(r["dung"])

    uniq = {k: {} for k in sents}
    marg = {k: {} for k in sents}
    with zipfile.ZipFile(M.ZIP) as z:
        for r in rows:
            k = (r["episode_id"], r["step_id"])
            key = (f"all_forest_dict/android_control_episode_"
                   f"[{r['episode_id']}]_{r['step_id']}.pkl")
            alln = M.raw_nodes(pickle.loads(z.read(key)))
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
            for name in sents:
                s = sents[name].get(k)
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
                other = max(other, 0.0)
                marg[name][k] = st - other
                uniq[name][k] = 1 if st > other and st > 0 else 0

    print("KHOP MEM (F1 theo tu + stem) - so voi KHOP NGUYEN VAN cua M7\n")
    print(f"{'nhanh':<18}{'ky hieu dung':>14}{'r':>8}"
          f"{'  (M7: dung / r)':>20}")
    m7 = {"nguoi / dich day": (39.01, 0.191), "S1": (33.16, 0.269),
          "duong ong": (34.76, 0.307)}
    for name in uniq:
        ks = [k for k in uniq[name] if k in listen[name]]
        a = [uniq[name][k] for k in ks]
        b = [listen[name][k] for k in ks]
        r = pearson([marg[name][k] for k in ks], b)
        o, orr = m7.get(name, (float('nan'), float('nan')))
        print(f"{name:<18}{100*sum(a)/len(a):>13.2f}%{r:>8.3f}"
              f"{f'  ({o:.2f}% / {orr:.3f})':>20}")

    print("\nPhi-4 dung | ky hieu noi duy nhat vs mo ho:")
    for name in uniq:
        ks = [k for k in uniq[name] if k in listen[name]]
        g1 = [listen[name][k] for k in ks if uniq[name][k] == 1]
        g0 = [listen[name][k] for k in ks if uniq[name][k] == 0]
        print(f"  {name:<18} duy nhat {100*sum(g1)/len(g1):5.2f}% (n={len(g1):4})"
              f"   mo ho {100*sum(g0)/len(g0):5.2f}% (n={len(g0):4})"
              f"   chenh {100*sum(g1)/len(g1)-100*sum(g0)/len(g0):+.2f}")

    print("\nPhi-4 dung theo nguu phan vi bien do mem (co don dieu chua?):")
    for name in uniq:
        ks = [k for k in marg[name] if k in listen[name]]
        ks.sort(key=lambda k: marg[name][k])
        print(f"  --- {name} ---")
        for i in range(5):
            g = ks[i * len(ks) // 5:(i + 1) * len(ks) // 5]
            lo = marg[name][g[0]]
            hi = marg[name][g[-1]]
            acc = 100 * sum(listen[name][k] for k in g) / len(g)
            print(f"    ngu phan {i+1}  bien do [{lo:+.2f} .. {hi:+.2f}]"
                  f"   Phi-4 {acc:6.2f}%   n={len(g)}")


if __name__ == "__main__":
    main()
