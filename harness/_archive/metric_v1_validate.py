# -*- coding: utf-8 -*-
"""
Việc 3 (report/81) — BUILD + BƠM-LỖI-VALIDATE thước "so hai đoạn hướng dẫn". LÀ CỔNG.
Thước tách mỗi bước thành (action, target); khớp target = chồng-từ-nội-dung (chính) + bge-m3 (backstop).
Bơm lỗi đã-biết vào gold rồi kiểm thước có bắt được + có TÁCH được "sai-target" khỏi "paraphrase"
(AUC≥0.80 — chính chỗ K1 chết). Rớt cổng → dừng, sửa thước, KHÔNG train.

Chạy: ~/.venvs/thesis/bin/python harness/metric_v1_validate.py   (cần ollama bge-m3)
"""
import json, os, re, math, urllib.request, random

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "dataset_samples", "androidcontrol_test", "ac_test_200ep.json")
EMB_URL = "http://localhost:11434/v1/embeddings"
TAU_BGE = 0.85          # backstop cao (chỉ cứu synonym thật, không hạ thấp gây K1)
J_MATCH = 0.5           # ngưỡng chồng-từ-nội-dung
SEED = 20260719

# ---- action vocab (đóng) ----
ACTION_MAP = {
    "tap": "tap", "click": "tap", "press": "tap", "select": "tap", "choose": "tap", "touch": "tap",
    "type": "type", "enter": "type", "input": "type", "fill": "type", "write": "type",
    "scroll": "scroll", "swipe": "scroll", "drag": "scroll",
    "long": "long_press", "hold": "long_press",
    "open": "open", "launch": "open",
    "go": "navigate", "navigate": "navigate", "back": "navigate", "return": "navigate",
}
STOP = set("the a an on to of in into at for your my this that it is and or please tap click on button icon "
           "then next now with bottom top left right corner screen page field option item".split())

def canon_action(text):
    for w in re.findall(r"[a-z]+", text.lower()):
        if w in ACTION_MAP:
            return ACTION_MAP[w]
    return "tap"   # mặc định

def content_tokens(text):
    toks = re.findall(r"[a-z0-9@._]+", text.lower())
    return [t for t in toks if t not in STOP and t not in ACTION_MAP and len(t) > 1]

def target_of(text):
    # bỏ cụm vị trí đuôi, giữ phần lõi
    t = re.sub(r"\b(at|in|on)\s+the\s+(top|bottom|left|right|upper|lower)[\w\s]*", "", text.lower())
    return " ".join(content_tokens(t))

# ---- bge-m3 backstop ----
_c = {}
def emb(texts):
    miss = [t for t in dict.fromkeys(texts) if t not in _c]
    for i in range(0, len(miss), 64):
        ch = miss[i:i+64]
        data = json.dumps({"model": "bge-m3", "input": ch}).encode()
        req = urllib.request.Request(EMB_URL, data=data, headers={"Content-Type": "application/json"})
        for t, v in zip(ch, [d["embedding"] for d in json.loads(urllib.request.urlopen(req, timeout=300).read())["data"]]):
            _c[t] = v
def cos(a, b):
    d = sum(x*y for x, y in zip(a, b)); na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(y*y for y in b))
    return d/(na*nb+1e-9)

def target_score(t1, t2):
    """Điểm khớp target liên tục [0,1]: max(Jaccard-từ-nội-dung, bge-nếu-đủ-cao)."""
    s1, s2 = set(content_tokens(t1)), set(content_tokens(t2))
    j = len(s1 & s2) / len(s1 | s2) if (s1 | s2) else 0.0
    if j >= J_MATCH:
        return j
    emb([t1 or " ", t2 or " "])
    b = cos(_c[t1 or " "], _c[t2 or " "])
    return max(j, b if b >= TAU_BGE else j)   # backstop chỉ khi rất cao

def step_match(m, g):
    """(action, target) khớp? trả (bool, target_score)."""
    a_ok = canon_action(m) == canon_action(g)
    ts = target_score(target_of(m), target_of(g))
    return (a_ok and ts >= J_MATCH * 0.999) or (a_ok and ts >= TAU_BGE), ts

def coverage(model_steps, gold_steps):
    """% gold-step được phủ bởi ít nhất 1 model-step (action∧target)."""
    cov = 0
    for g in gold_steps:
        if any(step_match(m, g)[0] for m in model_steps):
            cov += 1
    return cov / len(gold_steps) if gold_steps else 1.0

# ---- bơm lỗi ----
def perturb(gold, kind, all_targets, rng):
    g = list(gold)
    if not g:
        return g
    i = rng.randrange(len(g))
    if kind == "clean":
        return g
    if kind == "target_error":
        # thay target bằng target KHÁC (khác từ-lõi) từ pool
        cur = set(content_tokens(g[i]))
        for _ in range(20):
            alt = rng.choice(all_targets)
            if set(content_tokens(alt)) and not (set(content_tokens(alt)) & cur):
                g[i] = re.sub(re.escape(target_of(g[i])), alt, g[i]) if target_of(g[i]) in g[i] else (canon_verb(g[i]) + " " + alt)
                g[i] = verb_prefix(gold[i]) + " " + alt
                break
        return g
    if kind == "action_error":
        acts = ["tap", "type", "scroll", "long_press", "open"]
        cur = canon_action(g[i]); newa = rng.choice([a for a in acts if a != cur])
        g[i] = newa + " " + target_of(g[i])
        return g
    if kind == "missing":
        del g[i]; return g
    if kind == "extra":
        g.insert(i, "tap " + rng.choice(all_targets)); return g
    if kind == "reorder":
        if len(g) >= 2:
            j = (i+1) % len(g); g[i], g[j] = g[j], g[i]
        return g
    if kind == "paraphrase":
        # giữ từ-lõi, đổi từ chức năng (thêm 'the', đổi verb đồng nghĩa)
        tgt = target_of(g[i]); v = {"tap": "Click", "type": "Enter", "scroll": "Swipe", "open": "Open", "navigate": "Go to", "long_press": "Long-press"}[canon_action(g[i])]
        g[i] = f"{v} on the {tgt}"
        return g
    return g

def verb_prefix(text):
    m = re.match(r"\s*([A-Za-z\-]+)", text or "")
    return m.group(1) if m else "Tap"
def canon_verb(text):
    return verb_prefix(text)

def auc(pos, neg):
    """AUC = P(score_pos > score_neg). pos = paraphrase (nên cao), neg = target_error (nên thấp)."""
    if not pos or not neg:
        return float("nan")
    c = 0
    for p in pos:
        for n in neg:
            c += 1 if p > n else (0.5 if p == n else 0)
    return c / (len(pos) * len(neg))

def main():
    data = json.load(open(DATA, encoding="utf-8"))
    rng = random.Random(SEED)
    episodes = [d for d in data if (d.get("step_instructions") and len(d["step_instructions"]) >= 2)]
    all_targets = []
    for d in episodes:
        for s in d["step_instructions"]:
            t = target_of(s)
            if t: all_targets.append(t)
    print("=" * 78)
    print(f"VALIDATE THƯỚC (action,target) — {len(episodes)} ep, {len(all_targets)} target pool")
    print("=" * 78)

    kinds = ["clean", "target_error", "action_error", "missing", "extra", "reorder", "paraphrase"]
    agg = {k: [] for k in kinds}
    # để tính AUC tách-phân-phối: điểm target-score per-step bị sửa
    te_scores, pp_scores = [], []
    for d in episodes:
        gold = d["step_instructions"]
        for k in kinds:
            model = perturb(gold, k, all_targets, rng)
            agg[k].append(coverage(model, gold))
        # tách-phân-phối: điểm khớp của bước-bị-sửa
        i = rng.randrange(len(gold))
        te = perturb(gold, "target_error", all_targets, rng)
        pp = perturb(gold, "paraphrase", all_targets, rng)
        # điểm target-score giữa bước sửa và gold tương ứng (lấy min qua các bước = bước bị sửa)
        te_scores.append(min(target_score(target_of(m), target_of(g)) for m, g in zip(te, gold)) if len(te)==len(gold) else 0)
        pp_scores.append(min(target_score(target_of(m), target_of(g)) for m, g in zip(pp, gold)))

    def mean(x): return sum(x)/len(x) if x else float("nan")
    print("\n  Coverage trung bình theo loại bơm-lỗi (clean nên ~1.0):")
    base = mean(agg["clean"])
    for k in kinds:
        m = mean(agg[k]); drop = base - m
        flag = ""
        if k in ("target_error","action_error","missing") and drop < 0.15: flag = "  ⚠ KHÔNG tụt đủ"
        if k == "paraphrase" and drop > 0.10: flag = "  ⚠ TỤT OAN (false-positive)"
        if k == "reorder" and drop > 0.10: flag = "  (reorder làm tụt coverage — nên tách order-τ riêng)"
        print(f"    {k:14} coverage={m:.3f}  Δ={drop:+.3f}{flag}")

    sep = auc(pp_scores, te_scores)
    print(f"\n  ★ CỔNG TÁCH-PHÂN-PHỐI (chỗ K1 chết): AUC(paraphrase > target_error) = {sep:.3f}")
    print(f"    paraphrase target-score TB = {mean(pp_scores):.3f} | target_error TB = {mean(te_scores):.3f}")
    print(f"    → {'✅ QUA CỔNG (≥0.80)' if sep>=0.80 else '❌ RỚT CỔNG (<0.80) — phải sửa thước'}")

    # detection-rate đơn giản (bước-sai bị coi là không-phủ)
    det_te = sum(1 for s in te_scores if s < J_MATCH)/len(te_scores)
    fp_pp = sum(1 for s in pp_scores if s < J_MATCH)/len(pp_scores)
    print(f"\n  detection sai-target (nên ≥0.90) = {det_te:.3f} | false-positive paraphrase (nên ≤0.10) = {fp_pp:.3f}")

    json.dump({"n_ep": len(episodes), "coverage_by_kind": {k: mean(agg[k]) for k in kinds},
               "separation_auc": sep, "paraphrase_mean": mean(pp_scores), "target_error_mean": mean(te_scores),
               "detection_target": det_te, "fp_paraphrase": fp_pp},
              open(os.path.join(HERE, "metric_v1_results.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nĐã lưu metric_v1_results.json")

if __name__ == "__main__":
    main()
