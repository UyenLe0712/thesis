#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Đo độ phủ và cổng target của RGTC-SPICE (ACTION_CUOI 10/11, §6.3 và §7.2). CHỈ CPU.

Đây là phép đo THĂM DÒ trước khi khoá split: quần thể là bước chạm của pool chưa dùng ở tầng RL
(train_tru_val trừ các episode có trong prompt_keys quan sát được). Chưa phải Gate B chính thức,
vì split_manifest, canonical_roles.json và audit tay 200 cặp chưa khoá.

Chỗ file action chưa định nghĩa, phải khai khi đọc số:
  · Actionable đọc từ danh sách actions của nút (16 = CLICK, 32 = LONG_CLICK); cây không có is_clickable.
  · Cây trợ năng không có is_checked nên modifier trạng thái luôn False, đúng luật "thiếu field → False".
  · Bảng class → role và ba từ vựng modifier do script này đặt (POS/STATE/ATTR bên dưới).
  · Alias phải có ≥ 2 ký tự chữ-số, tránh token OCR một ký tự khớp lung tung.
Cấu hình chính = (role_mode=spec, alias_mode=own, span_mode=strict). Các cấu hình khác chỉ để đo độ nhạy.

  python gate_b_rgtc.py --selftest
  python gate_b_rgtc.py --root DIR --forest all_forest_dict.zip --exclude excl.json --out OUT
"""
import argparse, collections, hashlib, itertools, json, math, os, pickle, re, sys, time, unicodedata, zipfile

ROLE_SPEC = {
    "Button": "button", "ImageButton": "button", "ToggleButton": "toggle", "Switch": "toggle",
    "CheckBox": "toggle", "RadioButton": "toggle", "ImageView": "icon", "EditText": "input",
    "AutoCompleteTextView": "input", "MultiAutoCompleteTextView": "input", "Spinner": "dropdown",
    "SeekBar": "slider", "TextView": "text", "CheckedTextView": "text",
}
LAYOUT = {"RelativeLayout", "LinearLayout", "FrameLayout", "ViewGroup", "View", "RecyclerView", "ListView",
          "ScrollView", "ConstraintLayout", "CardView", "GridView", "ViewPager", "HorizontalScrollView",
          "WebView", "LinearLayoutCompat"}
BLACKLIST = {"spec": {"container", "layout", "text", "unknown"},
             "text_ok": {"container", "layout", "unknown"},
             "no_blacklist": set()}
POS = re.compile(r"\b(top|bottom|left|right|center|centre|middle|upper|lower|corner)\b")
STATE = re.compile(r"\b(turn|switch)\s+(on|off)\b|\b(enable|disable|enabled|disabled|uncheck|unchecked|checked|check|toggle)\b")
ATTR = re.compile(r"\b(red|blue|green|yellow|black|white|orange|purple|pink|grey|gray|big|small|large|first|second|third|last)\b")
TOK = re.compile(r"[^\W_]+", re.U)
CFGS = list(itertools.product(("spec", "text_ok", "no_blacklist"), ("own", "desc"), ("strict", "longest")))
PRIMARY = ("spec", "own", "strict")


def role_of(cls):
    if cls in ROLE_SPEC:
        return ROLE_SPEC[cls]
    return "container" if cls in LAYOUT else "unknown"


def toks(s):
    s = unicodedata.normalize("NFC", s or "").lower()
    return [m.group(0) for m in TOK.finditer(s)]


def norm(s):
    return " ".join(toks(s))


def good_alias(s):
    return sum(ch.isalnum() for ch in s) >= 2


def iou0(a, b):
    return a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1]


def inside(a, b):
    """a nằm trong b."""
    return a[0] >= b[0] and a[1] >= b[1] and a[2] <= b[2] and a[3] <= b[3]


def area(b):
    return max(0, b[2] - b[0]) * max(0, b[3] - b[1])


def region(b, w, h):
    return (min(2, int(3 * (b[0] + b[2]) / 2 / max(w, 1))), min(2, int(3 * (b[1] + b[3]) / 2 / max(h, 1))))


def classify(sentence):
    """Cùng logic với classify trong reward_cpu_8_11.py."""
    s = " ".join(re.findall(r"[a-z0-9']+", (sentence or "").lower()))
    if not s:
        return None
    if re.search(r"\b(go back|navigate back|return to (the )?(previous|last) screen|press (the )?back (button|key))\b", s):
        return "back"
    if re.search(r"\b(scroll|swipe)\b", s):
        return "scroll"
    if re.search(r"\b(wait|pause|let (it|the page) load)\b", s):
        return "wait"
    if re.search(r"\b(type|enter|input|fill in|write)\b", s):
        return "type"
    if re.search(r"\b(open|launch|start)\b.*\bapp\b", s):
        return "open_app"
    if re.search(r"\b(tap|click|press|select|choose|check|enable|disable|turn on|turn off|open)\b", s):
        return "tap"
    return None


def parse_nodes(forest):
    out = []
    for w in forest or []:
        if w.get("window_type") == 3:
            continue
        for n in w.get("tree", []):
            if not n.get("is_visible_to_user"):
                continue
            b = n.get("bounds_in_screen") or {}
            box = (b.get("left", 0), b.get("top", 0), b.get("right", 0), b.get("bottom", 0))
            if box[2] - box[0] < 8 or box[3] - box[1] < 8:
                continue
            acts = n.get("actions") or []
            out.append({"box": box, "cls": (n.get("class_name") or "").split(".")[-1],
                        "text": (n.get("text") or "").strip(),
                        "cd": (n.get("content_description") or "").strip(),
                        "res": (n.get("view_id_resource_name") or "").split("/")[-1].replace("_", " "),
                        "act": 16 in acts or 32 in acts, "pkg": n.get("package_name") or ""})
    return out


def ocr_in(box, items):
    return [it for it in items if box[0] <= it["cx"] <= box[2] and box[1] <= it["cy"] <= box[3]]


def aliases(node, nodes, items, mode):
    """{alias chuẩn hoá: tập nguồn}. Thứ tự nguồn theo §6.3."""
    out = collections.defaultdict(set)
    for src, s in (("a11y", node["text"]), ("a11y", node["cd"]), ("res", node["res"])):
        if s and good_alias(s):
            out[norm(s)].add(src)
    if mode == "desc":
        for n in nodes:
            if n is not node and inside(n["box"], node["box"]):
                for s in (n["text"], n["cd"]):
                    if s and good_alias(s):
                        out[norm(s)].add("a11y")
    for it in ocr_in(node["box"], items):
        t = (it.get("text") or "").strip()
        if t and good_alias(t):
            out[norm(t)].add("ocr")
    out.pop("", None)
    return out


def display_name(node, items):
    for s in (node["text"], node["cd"]):
        if s and good_alias(s) and len(s) <= 40:
            return s.split("\n")[0].strip()
    its = sorted(ocr_in(node["box"], items), key=lambda t: (t["cy"], t["cx"]))
    if its:
        t = (its[0].get("text") or "").strip()
        if t and good_alias(t):
            return t
    return None


def find_spans(gold, alias_map, span_mode):
    """Trả (spans, nguồn của span được chọn). Span tính trên ký tự của câu gốc."""
    g = unicodedata.normalize("NFC", gold or "")
    ms = list(TOK.finditer(g.lower()))
    if len(g.lower()) != len(g):       # lower() đổi độ dài thì offset không còn tin được
        return [], set()
    gt = [m.group(0) for m in ms]
    spans = collections.defaultdict(set)
    for al, src in alias_map.items():
        a = al.split()
        for i in range(len(gt) - len(a) + 1):
            if gt[i:i + len(a)] == a:
                spans[(ms[i].start(), ms[i + len(a) - 1].end())] |= src
    if span_mode == "longest" and len(spans) > 1:
        keep = {s: v for s, v in spans.items()
                if not any(o != s and o[0] <= s[0] and s[1] <= o[1] for o in spans)}
        spans = keep
    return list(spans), (spans[list(spans)[0]] if len(spans) == 1 else set())


def pick_distractor(tgt, nodes, items, role_tgt, t_alias):
    cx, cy = (tgt["box"][0] + tgt["box"][2]) / 2, (tgt["box"][1] + tgt["box"][3]) / 2
    cand = []
    for n in nodes:
        if n is tgt or not n["act"] or role_of(n["cls"]) != role_tgt or not iou0(n["box"], tgt["box"]):
            continue
        nm = display_name(n, items)
        if not nm or norm(nm) in t_alias:
            continue
        x, y = (n["box"][0] + n["box"][2]) / 2, (n["box"][1] + n["box"][3]) / 2
        cand.append((((x - cx) ** 2 + (y - cy) ** 2) ** 0.5, y, x, nm, id(n), n))
    if not cand:
        return None, None
    c = min(cand, key=lambda t: t[:5])
    return c[5], c[3]


def eval_row(rec, nodes, items, cfg):
    """Trả dict: reason (điều kiện đầu tiên trượt của e_t), e_pre, m, g_neg. e_pre chưa gồm điều kiện SPICE."""
    role_mode, alias_mode, span_mode = cfg
    res = {"e_pre": False, "m": False, "g_neg": None, "reason": None, "m_reason": None}
    g = unicodedata.normalize("NFC", rec["target_instruction"] or "")
    w, h = rec.get("w") or 1080, rec.get("h") or 2400
    x, y = float(rec["action"]["x"]), float(rec["action"]["y"])
    cont = [n for n in nodes if n["act"] and n["box"][0] <= x <= n["box"][2] and n["box"][1] <= y <= n["box"][3]]
    if not cont:
        res["reason"] = "1_no_actionable_target"
        return res
    tgt = min(cont, key=lambda n: area(n["box"]))
    al = aliases(tgt, nodes, items, alias_mode)
    if not al:
        res["reason"] = "2_no_alias"
        return res
    spans, src = find_spans(g, al, span_mode)
    if len(spans) != 1:
        res["reason"] = "3_span_none" if not spans else "3_span_many"
        return res
    s, e = spans[0]
    role = role_of(tgt["cls"])
    neg, nm = pick_distractor(tgt, nodes, items, role, set(al))
    if neg is None:
        res["reason"] = "4_no_distractor"
        return res
    gneg = g[:s] + nm + g[e:]
    assert gneg[:s] == g[:s] and gneg[s + len(nm):] == g[e:]
    rest = (g[:s] + " " + g[e:]).lower()
    if POS.search(rest) and region(tgt["box"], w, h) != region(neg["box"], w, h):
        res["reason"] = "5_position_modifier"
        return res
    if STATE.search(rest):
        res["reason"] = "6_state_modifier_no_metadata"
        return res
    if ATTR.search(rest):
        res["reason"] = "7_attribute_modifier"
        return res
    if classify(g) != classify(gneg):
        res["reason"] = "8_action_class_changed"
        return res
    res.update(e_pre=True, g_neg=gneg, gold=g)
    # m_t, không gồm SPICE
    a_span = norm(g[s:e])
    n_same = sum(1 for n in nodes if not inside(n["box"], tgt["box"]) and not inside(tgt["box"], n["box"])
                 and a_span in (norm(n["text"]), norm(n["cd"])))
    n_same += sum(1 for it in items if not ocr_in(tgt["box"], [it]) and norm(it.get("text")) == a_span)
    sa = w * h
    if role in BLACKLIST[role_mode]:
        res["m_reason"] = "m1_generic_role"
    elif n_same:
        res["m_reason"] = "m2_name_not_unique"
    elif not (src & {"a11y", "ocr"}):
        res["m_reason"] = "m3_name_source"
    elif area(tgt["box"]) / sa > 0.25:
        res["m_reason"] = "m4_target_area"
    elif area(neg["box"]) / sa > 0.25:
        res["m_reason"] = "m5_negative_area"
    else:
        res["m"] = True
    res.update(pkg=tgt["pkg"], role=role)
    return res


def spice_scores(pairs, batch):
    from pycocoevalcap.spice.spice import Spice
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    engine, tk = Spice(), PTBTokenizer()
    uniq = list(dict.fromkeys(pairs))
    out = {}
    for st in range(0, len(uniq), batch):
        block = uniq[st:st + batch]
        gts = {i: [{"caption": r}] for i, (_, r) in enumerate(block)}   # khoá số nguyên: sorted(keys) đúng thứ tự
        res = {i: [{"caption": c}] for i, (c, _) in enumerate(block)}
        gts, res = tk.tokenize(gts), tk.tokenize(res)
        _, scores = engine.compute_score(gts, res)
        assert len(scores) == len(block), "SPICE trả thiếu"
        for p, sc in zip(block, scores):
            f = sc.get("All", {}).get("f", 0)
            v = float(f) if f is not None and math.isfinite(float(f)) else 0.0   # không tuple → 0, được đếm là không parse
            assert 0.0 <= v <= 1.0, (p, v)
            if p[0] == p[1]:
                assert v in (0.0, 1.0), ("SPICE lệch cặp", p, v)
            out[p] = v
        print(f"[SPICE] {min(st + batch, len(uniq))}/{len(uniq)} cặp · {time.strftime('%H:%M:%S')}", flush=True)
    return out


def quant(xs, qs=(0.05, 0.25, 0.5, 0.75, 0.95)):
    xs = sorted(xs)
    return {str(q): round(xs[min(len(xs) - 1, int(q * len(xs)))], 4) for q in qs} if xs else {}


def selftest():
    def node(box, cls="Button", cd="", act=True, res=""):
        return {"box": box, "cls": cls, "text": "", "cd": cd, "res": res, "act": act, "pkg": "p"}
    a = node((0, 0, 100, 100), cd="Settings")
    b = node((200, 0, 300, 100), cd="Cancel")
    c = node((400, 0, 500, 100), cd="Help")
    rec = {"target_instruction": "Click on Settings", "w": 1000, "h": 2000, "action": {"x": 50, "y": 50}}
    r = eval_row(rec, [a, b, c], [], PRIMARY)
    assert r["e_pre"] and r["m"] and r["g_neg"] == "Click on Cancel", r
    # distractor gần nhất, thứ tự (khoảng cách, y, x, tên)
    assert pick_distractor(a, [a, c, b], [], "button", {"settings"})[1] == "Cancel"
    # hai span khác nhau → không eligible ở strict
    rec2 = dict(rec, target_instruction="Click Settings then Settings")
    assert eval_row(rec2, [a, b], [], PRIMARY)["reason"] == "3_span_many"
    # span lồng nhau: strict trượt, longest giữ
    d = node((0, 0, 100, 100), cd="Search bar", res="search")
    rec3 = dict(rec, target_instruction="Click the search bar")
    assert eval_row(rec3, [d, b], [], ("spec", "own", "strict"))["reason"] == "3_span_many"
    assert eval_row(rec3, [d, b], [], ("spec", "own", "longest"))["g_neg"] == "Click the Cancel"
    # thiếu state metadata → False
    assert eval_row(dict(rec, target_instruction="Enable Settings"), [a, b], [], PRIMARY)["reason"] == "6_state_modifier_no_metadata"
    # chỉ giữ phần tử actionable; không có thì ineligible
    assert eval_row(rec, [dict(a, act=False), b], [], PRIMARY)["reason"] == "1_no_actionable_target"
    # hộp distractor chồng lấn bị loại; chạm cạnh được phép
    e = node((100, 0, 200, 100), cd="Edge")
    assert iou0(a["box"], e["box"]) and not iou0(a["box"], (50, 50, 150, 150))
    # role text bị blacklist ở m_t theo spec, được nhận ở text_ok
    t = node((0, 0, 100, 100), cls="TextView", cd="Settings")
    u = node((200, 0, 300, 100), cls="TextView", cd="Cancel")
    assert eval_row(rec, [t, u], [], ("spec", "own", "strict"))["m_reason"] == "m1_generic_role"
    assert eval_row(rec, [t, u], [], ("text_ok", "own", "strict"))["m"]
    # tên xuất hiện lần nữa trên màn → m_t False
    v = node((600, 0, 700, 100), cd="Settings")
    assert eval_row(rec, [a, b, v], [], PRIMARY)["m_reason"] == "m2_name_not_unique"
    # modifier vị trí: khác vùng → loại
    far = node((800, 1800, 900, 1900), cd="Far")
    rec4 = dict(rec, target_instruction="Click on Settings at the top")
    assert eval_row(rec4, [a, far], [], PRIMARY)["reason"] == "5_position_modifier"
    # giữ nguyên ngoài span, kể cả dấu câu
    rec5 = dict(rec, target_instruction="Click on 'Settings', please.")
    assert eval_row(rec5, [a, b], [], PRIMARY)["g_neg"] == "Click on 'Cancel', please."
    print("selftest ĐẠT")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--root"); ap.add_argument("--forest"); ap.add_argument("--exclude"); ap.add_argument("--out")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--no-spice", action="store_true")
    ap.add_argument("--spice-n", type=int, default=6000)
    ap.add_argument("--batch", type=int, default=1500)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    ex = set(map(str, json.load(open(a.exclude))))
    recs = [json.loads(l) for l in open(os.path.join(a.root, "train_tru_val.jsonl"), encoding="utf8")]
    n_all, e_all = len(recs), len({r["episode_id"] for r in recs})
    pool = [r for r in recs if str(r["episode_id"]) not in ex]
    print(f"[pool] {n_all} bước/{e_all} episode → {len(pool)} bước/{len({r['episode_id'] for r in pool})} episode", flush=True)
    taps = [r for r in pool if r["action"].get("action_type") in ("click", "long_press") and "x" in r["action"]]
    if a.limit:
        taps = sorted(taps, key=lambda r: hashlib.sha256(f"gb|{r['episode_id']}|{r['step_id']}".encode()).hexdigest())[:a.limit]
    want = {r["image"] for r in taps}
    ocr = {}
    p = os.path.join(a.root, "ocr.jsonl")
    for l in (__import__("gzip").open(p + ".gz", "rt", encoding="utf8") if os.path.exists(p + ".gz") else open(p, encoding="utf8")):
        o = json.loads(l)
        if o["image"] in want:
            ocr[o["image"]] = o.get("items") or []
    print(f"[dữ liệu] bước chạm {len(taps)} · có OCR {len(ocr)} · {time.time() - t0:.0f}s", flush=True)
    z = zipfile.ZipFile(a.forest)
    nameset = set(z.namelist())
    stats = {c: collections.Counter() for c in CFGS}
    rows = []
    pkg_ok = no_tree = 0
    for i, r in enumerate(taps):
        k = f"all_forest_dict/android_control_episode_[{r['episode_id']}]_{r['step_id']}.pkl"
        if k not in nameset:
            no_tree += 1
            for c in CFGS:
                stats[c]["n"] += 1; stats[c]["r:0_no_tree"] += 1
            continue
        nodes = parse_nodes(pickle.loads(z.read(k)))
        pkg_ok += any(n["pkg"] for n in nodes)
        items = ocr.get(r["image"], [])
        row = {"episode_id": r["episode_id"], "step_id": r["step_id"], "gold": unicodedata.normalize("NFC", r["target_instruction"] or ""), "cfg": {}}
        for c in CFGS:
            v = eval_row(r, nodes, items, c)
            st = stats[c]
            st["n"] += 1
            if v["e_pre"]:
                st["e_pre"] += 1
                st["e_pre_m"] += v["m"]
                if not v["m"]:
                    st["r:" + v["m_reason"]] += 1
                row["cfg"]["|".join(c)] = {"neg": v["g_neg"], "m": v["m"]}
                row.setdefault("pkg", v.get("pkg", ""))
            else:
                st["r:" + v["reason"]] += 1
        if row["cfg"]:
            rows.append(row)
        if (i + 1) % 2000 == 0:
            s = stats[PRIMARY]
            print(f"[duyệt] {i + 1}/{len(taps)} · chính: e_pre {s['e_pre'] / s['n']:.1%} · active_pre {s['e_pre_m'] / s['n']:.1%} · {time.time() - t0:.0f}s", flush=True)
    print(f"[xong duyệt] thiếu cây {no_tree} · có package {pkg_ok}/{len(taps)}", flush=True)
    keyp = "|".join(PRIMARY)
    rep = {"pham_vi": "pool chưa khoá, thăm dò, chưa phải Gate B chính thức", "n_tap": len(taps),
           "pool_steps": len(pool), "pool_episodes": len({r["episode_id"] for r in pool}),
           "no_tree": no_tree, "package_available": pkg_ok, "configs": {}}
    order = sorted(rows, key=lambda r: hashlib.sha256(f"rgtc-gb|{r['episode_id']}|{r['step_id']}".encode()).hexdigest())
    spice = {}
    if not a.no_spice:
        sample = order[:a.spice_n]
        pairs = []
        for r in sample:
            for c, v in r["cfg"].items():
                g, n = r["gold"], v["neg"]
                pairs += [(g, g), (n, n), (g, n), (n, g)]
        print(f"[SPICE] mẫu {len(sample)} hàng, {len(set(pairs))} cặp duy nhất", flush=True)
        spice = spice_scores(pairs, a.batch)
    for c in CFGS:
        key, s = "|".join(c), stats[c]
        d = {"n": s["n"], "P_e_pre": s["e_pre"] / max(s["n"], 1), "P_m_given_e_pre": s["e_pre_m"] / max(s["e_pre"], 1),
             "active_pre": s["e_pre_m"] / max(s["n"], 1),
             "reasons": dict(sorted((k[2:], v) for k, v in s.items() if k.startswith("r:")))}
        if spice:
            ok = act = fr = neg_ok = pos_margin_n = 0
            tp, tn = [], []
            for r in order[:a.spice_n]:
                v = r["cfg"].get(key)
                if not v or not v["m"]:
                    continue
                act += 1
                g, n = r["gold"], v["neg"]
                if not (spice[(g, g)] == 1.0 and spice[(n, n)] == 1.0 and spice[(g, n)] < 1.0):
                    continue
                ok += 1
                tg = 0.5 + 0.5 * (spice[(g, g)] - spice[(g, n)])
                tb = 0.5 + 0.5 * (spice[(n, g)] - spice[(n, n)])
                tp.append(tg); tn.append(tb)
                fr += tg <= 0.5
                neg_ok += tb < 0.5
            d.update(spice_active_sample=act, spice_pass=ok, spice_pass_rate=ok / max(act, 1),
                     active_est=d["active_pre"] * ok / max(act, 1), FR_gold=fr / max(ok, 1), neg_lt_half=neg_ok / max(ok, 1),
                     T_gold_q=quant(tp), T_neg_q=quant(tn),
                     gate={"coverage>=30%": d["active_pre"] * ok / max(act, 1) >= 0.30,
                           "FR_gold<=5%": fr / max(ok, 1) <= 0.05, "neg<0.5>=95%": neg_ok / max(ok, 1) >= 0.95})
        rep["configs"][key] = d
    p = os.path.join(a.out, "gate_b_rgtc.json")
    json.dump(rep, open(p, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    # mẫu chờ audit tay: chỉ dựng, chưa chấm
    with open(os.path.join(a.out, "audit_ung_vien.jsonl"), "w", encoding="utf8") as f:
        k = 0
        for r in order:
            v = r["cfg"].get(keyp)
            if v and v["m"] and k < 400:
                f.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "pkg": r.get("pkg"), "gold": r["gold"], "neg": v["neg"]}, ensure_ascii=False) + "\n")
                k += 1
    print("=" * 76)
    for c in CFGS:
        key, d = "|".join(c), rep["configs"]["|".join(c)]
        print(f"{'*' if c == PRIMARY else ' '} {key:32s} e_pre {d['P_e_pre']:.1%} · m|e {d['P_m_given_e_pre']:.1%} · active_pre {d['active_pre']:.1%}"
              + (f" · spice_pass {d['spice_pass_rate']:.1%} · active_est {d['active_est']:.1%} · FR {d['FR_gold']:.1%} · neg {d['neg_lt_half']:.1%}" if spice else ""), flush=True)
    print(json.dumps(rep["configs"][keyp], ensure_ascii=False, indent=1))
    print("XONG", p, f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
