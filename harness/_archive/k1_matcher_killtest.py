# -*- coding: utf-8 -*-
"""
K1 — KILL-TEST bộ đối chiếu lọc-bịa, kiểm HAI CHIỀU (report/72 VIỆC 0).

Bộ đối chiếu (aloha_match.py) coi một tên nút model nói là "BỊA" nếu cosine tới
nhãn VH gần nhất < τ (nomic-embed, τ=0.55). K1 hỏi: cổng đó có đáng tin không?

- BỎ LỌT (false negative): bịa GẦN-NGHĨA (model nói 'Send' khi màn chỉ có 'Save';
  'Filter' khi chỉ có 'Search'...) — khác NÚT khác CHỨC NĂNG, KHÔNG có trên màn,
  nhưng embedding kéo gần → cổng cho qua = bịa lọt vào data. NGUY HIỂM NHẤT.
- KẾT OAN (false positive): nút THẬT nhưng model diễn đạt khác (dịch/đồng nghĩa:
  'Tìm kiếm' cho 'Search') → embedding không đủ gần → cổng đánh oan = mất data tốt.

Nhãn-vàng do người thiết kế gán theo CHỨC-NĂNG (dịch = cùng nút = THẬT; khác chức
năng = BỊA), instantiate trên 127 màn MobileViews THẬT.

Chạy: PYTHONIOENCODING=utf-8 python3 harness/k1_matcher_killtest.py
Cần: ollama serve (nomic-embed-text, bge-m3). Không cần GPU/API.
"""
import json, os, re, glob, math, urllib.request

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "dataset_samples", "mv_multiapp")
KEPT = os.path.join(HERE, "kept_screens_final.json")
TAU_NOMIC = 0.55                      # ngưỡng pipeline đang dùng (aloha_match.py)
EMB_URL = "http://localhost:11434/v1/embeddings"

# ---------- embedding (per-model cache, KHÔNG dùng chung cache của aloha_match) ----------
_cache = {}   # (model, text) -> vector
def _embed_batch(model, texts):
    data = json.dumps({"model": model, "input": [t or "" for t in texts]}).encode("utf-8")
    req = urllib.request.Request(EMB_URL, data=data,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=300) as r:
        return [d["embedding"] for d in json.loads(r.read().decode("utf-8"))["data"]]

def ensure(model, texts):
    miss = [t for t in dict.fromkeys(t or "" for t in texts) if (model, t) not in _cache]
    for i in range(0, len(miss), 64):
        chunk = miss[i:i+64]
        for t, v in zip(chunk, _embed_batch(model, chunk)):
            _cache[(model, t)] = v

def cos(a, b):
    d = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(y*y for y in b))
    return d / (na*nb + 1e-9)

def best_sim(model, name, labels):
    """max cosine giữa `name` và mọi nhãn VH (giống best_match nhưng trả sim)."""
    if not labels:
        return 0.0
    ensure(model, [name] + list(labels))
    e = _cache[(model, name or "")]
    return max(cos(e, _cache[(model, l or "")]) for l in labels)

# ---------- nạp nhãn VH (không cần ảnh) ----------
def vh_labels(vh):
    o = json.load(open(vh, encoding="utf-8"))
    labs, n_act, n_act_labeled = [], 0, 0
    for n in o.get("views", []):
        lab = (n.get("text") or n.get("content_description") or "").strip()
        act = bool(n.get("clickable") or n.get("editable") or n.get("long_clickable"))
        if act:
            n_act += 1
            if lab:
                n_act_labeled += 1
        if lab and (act or n.get("child_count", 0) == 0):
            labs.append(lab)
    # unique, giữ thứ tự
    seen, uniq = set(), []
    for l in labs:
        k = l.lower()
        if k not in seen:
            seen.add(k); uniq.append(l)
    return uniq, n_act, n_act_labeled

# ---------- bộ neo: gán tay theo CHỨC NĂNG ----------
# para = cùng nút (dịch/đồng nghĩa rõ) -> gold REAL ; near = khác nút gần nghĩa -> gold HALLUC
LEX = [
    {"a": "search",       "para": ["Find", "Tìm kiếm", "Buscar"],        "near": ["Filter", "Sort", "Explore"]},
    {"a": "save",         "para": ["Store", "Lưu", "Guardar"],           "near": ["Send", "Submit", "Export"]},
    {"a": "share",        "para": ["Chia sẻ", "Compartir", "Send to"],   "near": ["Copy", "Like", "Report"]},
    {"a": "home",         "para": ["Main screen", "Trang chủ", "Inicio"],"near": ["Menu", "Back", "Explore"]},
    {"a": "reply",        "para": ["Respond", "Trả lời", "Responder"],   "near": ["Forward", "React", "Report"]},
    {"a": "follow",       "para": ["Theo dõi", "Seguir"],                "near": ["Block", "Friend", "Mute"]},
    {"a": "ok",           "para": ["Confirm", "Đồng ý", "Aceptar"],      "near": ["Cancel", "Close", "Back"]},
    {"a": "back",         "para": ["Go back", "Quay lại", "Volver"],     "near": ["Cancel", "Close", "Forward"]},
    {"a": "add",          "para": ["Create", "Thêm", "Añadir"],          "near": ["Edit", "Remove", "Delete"]},
    {"a": "more options", "para": ["Additional options", "Tùy chọn"],    "near": ["Settings", "Help", "Details"]},
    {"a": "newest",       "para": ["Latest", "Mới nhất", "Recent"],      "near": ["Oldest", "Popular", "Trending"]},
    {"a": "popular",      "para": ["Trending", "Phổ biến"],              "near": ["Newest", "Recent", "Following"]},
    {"a": "all",          "para": ["Everything", "Tất cả", "Todos"],     "near": ["None", "Filter", "Select"]},
    {"a": "privacy policy","para": ["Privacy statement", "Chính sách bảo mật"], "near": ["Terms of Service", "About", "Cookie Policy"]},
    {"a": "settings",     "para": ["Configure", "Cài đặt", "Ajustes"],   "near": ["Notifications", "Account", "Help"]},
    {"a": "next",         "para": ["Continue", "Tiếp tục", "Siguiente"], "near": ["Skip", "Previous", "Back"]},
    {"a": "play",         "para": ["Phát", "Reproducir"],                "near": ["Pause", "Stop", "Download"]},
    {"a": "menu",         "para": ["Trình đơn", "Menú"],                 "near": ["Home", "Options", "List"]},
]
UNRELATED = ["Bluetooth", "Airplane mode", "Add to cart", "Scan QR code",
             "Wi-Fi settings", "Battery saver", "Boarding pass", "Checkout"]

def present(word, labels_lc):
    w = word.lower()
    return any(w == l or re.search(r"\b" + re.escape(w) + r"\b", l) for l in labels_lc)

def cand_present(cand, labels_lc):
    c = cand.lower()
    return any(c == l or c in l for l in labels_lc)

# ---------- dựng tập thử ----------
def build_pairs():
    kept = set(json.load(open(KEPT, encoding="utf-8"))["kept"])
    files = sorted(f for f in glob.glob(DATA + "/*.viewhierarchy.json")
                   if os.path.basename(f).split(".")[0] in kept)
    pairs = []             # {screen, cand, labels, gold, cat}
    cov_act, cov_act_lab = 0, 0
    caps = {"exact": 30, "paraphrase": 40, "nearsyn": 40, "unrelated": 20}
    cnt = {k: 0 for k in caps}
    for f in files:
        sid = os.path.basename(f).split(".")[0]
        labels, n_act, n_act_lab = vh_labels(f)
        cov_act += n_act; cov_act_lab += n_act_lab
        lc = [l.lower() for l in labels]
        # EXACT-REAL: nhãn actionable ngắn, distinct
        if cnt["exact"] < caps["exact"]:
            for l in labels:
                if 2 <= len(l) <= 18 and re.search(r"[A-Za-zÀ-ỹ]", l) and not l.isdigit():
                    pairs.append({"screen": sid, "cand": l, "labels": labels, "gold": "REAL", "cat": "exact"})
                    cnt["exact"] += 1; break
        # PARAPHRASE + NEARSYN theo anchor
        for e in LEX:
            if not present(e["a"], lc):
                continue
            if cnt["paraphrase"] < caps["paraphrase"]:
                for p in e["para"]:
                    if not cand_present(p, lc):
                        pairs.append({"screen": sid, "cand": p, "labels": labels, "gold": "REAL", "cat": "paraphrase", "anchor": e["a"]})
                        cnt["paraphrase"] += 1; break
            if cnt["nearsyn"] < caps["nearsyn"]:
                for nn in e["near"]:
                    if not cand_present(nn, lc):
                        pairs.append({"screen": sid, "cand": nn, "labels": labels, "gold": "HALLUC", "cat": "nearsyn", "anchor": e["a"]})
                        cnt["nearsyn"] += 1; break
        # UNRELATED-HALLUC
        if cnt["unrelated"] < caps["unrelated"]:
            for u in UNRELATED:
                if not cand_present(u, lc):
                    pairs.append({"screen": sid, "cand": u, "labels": labels, "gold": "HALLUC", "cat": "unrelated"})
                    cnt["unrelated"] += 1; break
    vh_cov = cov_act_lab / cov_act if cov_act else 0.0
    return pairs, vh_cov, len(files)

# ---------- thống kê ----------
def kappa(pred, gold):
    # 2 rater nhị phân: HALLUC/REAL
    n = len(pred)
    a = sum(1 for p, g in zip(pred, gold) if p == "HALLUC" and g == "HALLUC")
    b = sum(1 for p, g in zip(pred, gold) if p == "HALLUC" and g == "REAL")
    c = sum(1 for p, g in zip(pred, gold) if p == "REAL" and g == "HALLUC")
    d = sum(1 for p, g in zip(pred, gold) if p == "REAL" and g == "REAL")
    po = (a + d) / n
    p_h = ((a+b)/n) * ((a+c)/n); p_r = ((c+d)/n) * ((b+d)/n)
    pe = p_h + p_r
    return (po - pe) / (1 - pe) if (1 - pe) else 0.0

def evaluate(pairs, model, tau, sims):
    gold = [p["gold"] for p in pairs]
    pred = ["HALLUC" if s < tau else "REAL" for s in sims]
    TP = sum(1 for pr, g in zip(pred, gold) if pr == "HALLUC" and g == "HALLUC")
    FP = sum(1 for pr, g in zip(pred, gold) if pr == "HALLUC" and g == "REAL")
    FN = sum(1 for pr, g in zip(pred, gold) if pr == "REAL" and g == "HALLUC")
    TN = sum(1 for pr, g in zip(pred, gold) if pr == "REAL" and g == "REAL")
    prec = TP/(TP+FP) if TP+FP else float("nan")
    rec  = TP/(TP+FN) if TP+FN else float("nan")
    return {"tau": tau, "TP": TP, "FP": FP, "FN": FN, "TN": TN,
            "precision": prec, "recall": rec, "kappa": kappa(pred, gold),
            "pred": pred}

def cat_rate(pairs, pred, cat, gold_of_cat):
    idx = [i for i, p in enumerate(pairs) if p["cat"] == cat]
    if not idx:
        return None, 0
    # với cat này gold cố định; đếm tỉ lệ pred SAI
    wrong = sum(1 for i in idx if pred[i] != gold_of_cat)
    return wrong/len(idx), len(idx)

def main():
    pairs, vh_cov, nscreen = build_pairs()
    from collections import Counter
    comp = Counter((p["cat"], p["gold"]) for p in pairs)
    print("=" * 78)
    print("K1 — KILL-TEST BỘ ĐỐI CHIẾU (hai chiều) · dữ liệu: %d màn MobileViews thật" % nscreen)
    print("=" * 78)
    print("Tập thử: %d cặp (tên model nói ↔ nhãn VH màn đó)" % len(pairs))
    for (cat, gold), c in sorted(comp.items()):
        print(f"   {cat:11} gold={gold:7} : {c}")
    print(f"\nĐộ phủ nhãn VH (bối cảnh kết-oan icon-only): {vh_cov*100:.1f}% phần tử actionable CÓ nhãn text")
    print(f"   → {100-vh_cov*100:.1f}% nút actionable KHÔNG có chữ trong VH (nguồn kết-oan mà embedding không cứu được)")

    MODELS = [("nomic-embed-text", TAU_NOMIC), ("bge-m3", None)]
    results = {"n_pairs": len(pairs), "vh_label_coverage": vh_cov, "n_screens": nscreen,
               "composition": {f"{k[0]}|{k[1]}": v for k, v in comp.items()}, "models": {}}

    for model, tau_fixed in MODELS:
        print("\n" + "-" * 78)
        print(f"MÔ HÌNH EMBEDDING: {model}" + (f"  (τ pipeline = {tau_fixed})" if tau_fixed else "  (τ chưa cam kết → chỉ quét)"))
        print("-" * 78)
        sims = [best_sim(model, p["cand"], p["labels"]) for p in pairs]

        # phân bố sim: paraphrase (muốn CHẤP NHẬN) vs nearsyn (muốn TỪ CHỐI) — kiểm tách được không
        para = sorted(s for s, p in zip(sims, pairs) if p["cat"] == "paraphrase")
        near = sorted(s for s, p in zip(sims, pairs) if p["cat"] == "nearsyn")
        def med(x): return x[len(x)//2] if x else float("nan")
        print(f"  sim PARAPHRASE (gold THẬT, nên ≥τ): min={min(para):.3f} median={med(para):.3f} max={max(para):.3f}")
        print(f"  sim NEARSYN   (gold BỊA, nên <τ):  min={min(near):.3f} median={med(near):.3f} max={max(near):.3f}")
        overlap = sum(1 for s in near if s >= min(para)) if para else 0
        print(f"  → CHỒNG LẤN: {overlap}/{len(near)} ca bịa-gần-nghĩa có sim ≥ sim thấp nhất của paraphrase thật")

        model_res = {"sims_by_cat": {}, "tau_eval": {}, "sweep": []}
        # tại τ pipeline (nếu có)
        if tau_fixed:
            r = evaluate(pairs, model, tau_fixed, sims)
            pred = r["pop"] if False else r["pred"]
            print(f"\n  == Tại τ = {tau_fixed} (cổng thật của pipeline) ==")
            print(f"     Ma trận: TP(bắt đúng bịa)={r['TP']}  FN(BỎ LỌT bịa)={r['FN']}  "
                  f"FP(KẾT OAN nút thật)={r['FP']}  TN={r['TN']}")
            print(f"     Precision(bịa)={r['precision']*100:.1f}%  Recall(bịa)={r['recall']*100:.1f}%  κ={r['kappa']:.3f}")
            fn_near, n_near = cat_rate(pairs, pred, "nearsyn", "HALLUC")
            fp_para, n_para = cat_rate(pairs, pred, "paraphrase", "REAL")
            fn_unrel, n_unrel = cat_rate(pairs, pred, "unrelated", "HALLUC")
            fp_exact, n_exact = cat_rate(pairs, pred, "exact", "REAL")
            print(f"     ↳ BỎ LỌT bịa-gần-nghĩa (nearsyn):   {fn_near*100:.1f}%  ({int(fn_near*n_near)}/{n_near})  ← chiều nguy hiểm")
            print(f"     ↳ BỎ LỌT bịa-vô-quan (unrelated):   {fn_unrel*100:.1f}%  ({int(fn_unrel*n_unrel)}/{n_unrel})")
            print(f"     ↳ KẾT OAN paraphrase (dịch/đồng nghĩa): {fp_para*100:.1f}%  ({int(fp_para*n_para)}/{n_para})  ← chiều mất-data")
            print(f"     ↳ KẾT OAN nhãn y-hệt (exact):       {fp_exact*100:.1f}%  ({int(fp_exact*n_exact)}/{n_exact})")
            r.pop("pred", None)
            model_res["tau_eval"][str(tau_fixed)] = {**r, "fn_nearsyn": fn_near, "fp_paraphrase": fp_para,
                                                     "fn_unrelated": fn_unrel, "fp_exact": fp_exact}
        # quét τ
        print(f"\n  == Quét τ (tìm ngưỡng tốt nhất theo κ) ==")
        print(f"     {'τ':>5} {'prec':>6} {'recall':>7} {'κ':>6} {'BỎ-LỌT-near':>12} {'KẾT-OAN-para':>13}")
        best = None
        t = 0.40
        while t <= 0.751:
            r = evaluate(pairs, model, t, sims)
            fn_near, _ = cat_rate(pairs, pairs and r["pred"], "nearsyn", "HALLUC")
            fp_para, _ = cat_rate(pairs, r["pred"], "paraphrase", "REAL")
            row = {"tau": round(t, 3), "precision": r["precision"], "recall": r["recall"],
                   "kappa": r["kappa"], "fn_nearsyn": fn_near, "fp_paraphrase": fp_para}
            model_res["sweep"].append(row)
            mark = ""
            if best is None or r["kappa"] > best["kappa"]:
                best = {"tau": round(t, 3), "kappa": r["kappa"]};
            print(f"     {t:5.3f} {r['precision']*100:5.1f}% {r['recall']*100:6.1f}% {r['kappa']:6.3f} "
                  f"{fn_near*100:10.1f}% {fp_para*100:12.1f}%")
            t += 0.05
        print(f"     → κ cao nhất tại τ≈{best['tau']} (κ={best['kappa']:.3f})")
        model_res["best_kappa"] = best
        model_res["overlap_near_ge_minpara"] = overlap
        model_res["sim_stats"] = {"para_min": min(para), "para_med": med(para),
                                  "near_med": med(near), "near_max": max(near)}
        results["models"][model] = model_res

    out = os.path.join(HERE, "k1_results.json")
    json.dump(results, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n" + "=" * 78)
    print("Đã lưu số chi tiết:", out)
    print("=" * 78)

if __name__ == "__main__":
    main()
