# -*- coding: utf-8 -*-
"""SA-SPICE-v3 — sàng reward offline trên TRAIN-v3 (mức 1, report/333 §10). CPU + Java (Kaggle CPU, cần jar CoreNLP).

Vào: train_v3.jsonl · mau_0/1.jsonl (kernel 1: greedy + 8 mẫu SFT-cont) · score_k{0..8}_raw.jsonl (kernel 2: exec UGround, bước chạm).
Mỗi câu ứng viên: s = SPICE (jar -detailed, có tuple câu chuẩn ⇒ K_g), c = chrF/100, CIDEr-D/10 (df từ câu chuẩn TRAIN-v3),
ROUGE-L, d = phạt độ dài, A = verifier sa3-verify-3. Chín reward đúng protocol_freeze.json. Câu rỗng ⇒ 0. SPICE NaN/None ⇒ STOP.

Đo trên NHÓM 8 mẫu (= nhóm GRPO G=8), bước chạm:
  concordance = P(R(câu exec=1) > R(câu exec=0)) trên mọi cặp trong nhóm khác exec, hoà tính 0,5
  zero_std    = tỉ lệ nhóm 8 reward bằng nhau
  oracle_up   = exec của câu reward cao nhất (hoà ⇒ trung bình) − exec trung bình của nhóm
KTC95 bootstrap cụm theo package (2.000 lần) cho hiệu SA-SPICE-v3 − từng reward khác. Số mô tả cho quyết định đi/dừng,
KHÔNG dùng để chỉnh hệ số (memo §3).

  python sa3_reward_screen.py --data DIR --mau DIR --score DIR --out OUT.json
  python sa3_reward_screen.py --selftest
"""
import os, re, sys, json, math, random, argparse, collections, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
WORD = re.compile(r"[A-Za-z0-9'-]+")
ARMS = ("SPICE-MATCH", "Action-SPICE", "FIXED", "FIXED+A", "Sparse-SPICE", "SA-SPICE-v3", "chrF", "SPIDEr-like", "ROUGE-L")
CHINH = "SA-SPICE-v3"
clip = lambda x: min(1.0, max(0.0, x))


def nw(s):
    return len(WORD.findall(s or ""))


def penalty(y, g):
    return min(0.05, 0.02 * max(0, nw(y) - nw(g) - 3))


def k_gold(ref_tuples):
    """K_g = |T(g)|: tuple câu chuẩn, gắn nhãn O|/A|/R| theo độ dài, NFC/lowercase/gộp khoảng trắng, bỏ trùng."""
    out = set()
    for t in ref_tuples:
        parts = [re.sub(r"\s+", " ", unicodedata.normalize("NFC", p).lower()).strip() for p in t.split(" | ")]
        tag = {1: "O", 2: "A", 3: "R"}.get(len(parts), "R")
        out.add(tag + "|" + "|".join(parts))
    return len(out)


def rewards(y, g, s, c, cid, rl, A, K):
    if not (y or "").strip():
        return {a: 0.0 for a in ARMS}
    for v in (s, c, cid, rl):
        if v is None or not isinstance(v, (int, float)) or v != v or math.isinf(v):
            raise SystemExit(f"⛔ STOP: điểm không hợp lệ {v!r} cho {y!r}")
    d = penalty(y, g)
    al = 0.8 * min(1.0, K / 3.0)
    S = al * s + (1 - al) * c
    fx = 0.8 * s + 0.2 * c
    return {"SPICE-MATCH": clip(0.8 * s + 0.1 - d), "Action-SPICE": clip(0.8 * s + 0.2 * A - d),
            "FIXED": clip(0.8 * fx + 0.1 - d), "FIXED+A": clip(0.8 * fx + 0.2 * A - d),
            "Sparse-SPICE": clip(0.8 * S + 0.1 - d), "SA-SPICE-v3": clip(0.8 * S + 0.2 * A - d),
            "chrF": clip(c - d), "SPIDEr-like": clip(0.5 * s + 0.5 * cid - d), "ROUGE-L": clip(rl - d)}


def group_stats(R, E):
    """R: list 8 reward, E: list 8 exec (0/1). Trả (n_cặp, thắng, zero_std, oracle_up)."""
    pos = [r for r, e in zip(R, E) if e]; neg = [r for r, e in zip(R, E) if not e]
    win = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    zs = max(R) - min(R) < 1e-12
    m = max(R); top = [e for r, e in zip(R, E) if abs(r - m) < 1e-12]
    return len(pos) * len(neg), win, zs, sum(top) / len(top) - sum(E) / len(E)


def summarize(G, arms=ARMS, B=2000, seed=20261111):
    """G: list dict(pkg, R={arm: [8]}, E=[8])."""
    def agg(idx, arm):
        n = w = z = up = 0
        for i in idx:
            a, b, c, d = group_stats(G[i]["R"][arm], G[i]["E"])
            n += a; w += b; z += c; up += d
        return {"concordance": w / n if n else float("nan"), "zero_std": z / len(idx), "oracle_up_pp": 100 * up / len(idx), "pairs": n}
    out = {"n_groups": len(G), "arms": {a: agg(range(len(G)), a) for a in arms}}
    cl = collections.defaultdict(list)
    for i, g in enumerate(G):
        cl[g["pkg"]].append(i)
    ks = sorted(cl); rd = random.Random(seed)
    diffs = {a: {"concordance": [], "oracle_up_pp": []} for a in arms if a != CHINH}
    for _ in range(B):
        idx = [i for k in (rd.choice(ks) for _ in ks) for i in cl[k]]
        base = agg(idx, CHINH)
        for a in diffs:
            o = agg(idx, a)
            for m in diffs[a]:
                diffs[a][m].append(base[m] - o[m])
    out["n_packages"] = len(ks)
    out["SA_minus"] = {}
    for a, dd in diffs.items():
        out["SA_minus"][a] = {}
        for m, v in dd.items():
            v = sorted(x for x in v if x == x)
            pt = out["arms"][CHINH][m] - out["arms"][a][m]
            out["SA_minus"][a][m] = {"diem": pt, "ktc95": [v[int(0.025 * len(v))], v[int(0.975 * len(v)) - 1]]}
    return out


def selftest():
    assert penalty("a b c d e f g h", "a b") == 0.05 and penalty("a b c", "a b") == 0.0
    assert k_gold(["button", "button", "button | blue", "tap | on | button"]) == 3
    r = rewards("Click the OK button", "Click OK", 0.5, 0.6, 0.4, 0.7, 1.0, 1)
    al = 0.8 / 3; S = al * 0.5 + (1 - al) * 0.6
    assert abs(r["SA-SPICE-v3"] - (0.8 * S + 0.2)) < 1e-9 and abs(r["Sparse-SPICE"] - (0.8 * S + 0.1)) < 1e-9
    assert rewards("", "x", 0, 0, 0, 0, 1, 1)["SA-SPICE-v3"] == 0.0
    try:
        rewards("a", "b", float("nan"), 0, 0, 0, 1, 1); raise AssertionError("phải STOP")
    except SystemExit:
        pass
    n, w, z, up = group_stats([1, 1, 0.5, 0.5, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0])
    assert n == 12 and z is False and abs(up - (0.5 - 0.25)) < 1e-9
    G = [{"pkg": f"p{i % 5}", "R": {a: [random.random() for _ in range(8)] for a in ARMS}, "E": [i % 2, 1, 0, 0, 1, 0, 0, 0]} for i in range(40)]
    s = summarize(G, B=50)
    assert set(s["SA_minus"]) == set(ARMS) - {CHINH}
    print("selftest ĐẠT", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--data"); ap.add_argument("--mau"); ap.add_argument("--score"); ap.add_argument("--out")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    import sacrebleu
    from pycocoevalcap.rouge.rouge import Rouge
    import sa3_action_verify as V
    from grpo_luoi import CiderD, tok
    from h4_spice_tuple_7_11 import spice_chi_tiet

    rows = [json.loads(l) for l in open(os.path.join(a.data, "train_v3.jsonl"), encoding="utf-8")]
    assert len(rows) == 1000
    M = {}
    for i in (0, 1):
        for l in open(os.path.join(a.mau, f"mau_{i}.jsonl"), encoding="utf-8"):
            d = json.loads(l); M[(d["episode_id"], d["step_id"])] = d
    assert len(M) == 1000, len(M)
    EX = [{} for _ in range(9)]
    for k in range(9):
        for l in open(os.path.join(a.score, f"score_k{k}_raw.jsonl"), encoding="utf-8"):
            o = json.loads(l); EX[k][(o["episode_id"], o["step_id"])] = int(o.get("executable", 0))
    cid = CiderD([r["target_instruction"] for r in rows])
    rouge = Rouge()

    items = []
    for r in rows:
        m = M[(r["episode_id"], r["step_id"])]
        for k, y in enumerate([m["greedy"]] + m["mau"]):
            items.append((r, k, y))
    nonempty = [(i, it) for i, it in enumerate(items) if (it[2] or "").strip()]
    print(f"[câu] {len(items)} · khác rỗng {len(nonempty)}", flush=True)
    SP = {}
    B = 1500
    for st in range(0, len(nonempty), B):
        ch = nonempty[st:st + B]
        res = spice_chi_tiet([it[2] for _, it in ch], [it[0]["target_instruction"] for _, it in ch], nhan=f"spice {st}")
        for (i, _), o in zip(ch, res):
            f = o["scores"]["All"]["f"]
            if f is None or f != f:
                raise SystemExit(f"⛔ STOP: SPICE NaN ở câu {i}")
            SP[i] = (float(f), k_gold(o["ref"]))
    KG = {}
    for i, (r, k, y) in enumerate(items):
        if i in SP:
            KG.setdefault((r["episode_id"], r["step_id"]), SP[i][1])
    by = collections.defaultdict(lambda: [None] * 9)
    for i, (r, k, y) in enumerate(items):
        g = r["target_instruction"]; key = (r["episode_id"], r["step_id"])
        A, _ = V.score_action(y, g, r["action"]["action_type"])
        if (y or "").strip():
            s = SP[i][0]; c = sacrebleu.sentence_chrf(y, [g]).score / 100
            ci = cid.score(y, g) / 10; rl = rouge.calc_score([" ".join(tok(y))], [" ".join(tok(g))])
        else:
            s = c = ci = rl = 0.0
        by[key][k] = {"R": rewards(y, g, s, c, ci, rl, A, KG.get(key, 0)), "A": A}
    TAPT = ("click", "long_press")
    G = []
    for r in rows:
        key = (r["episode_id"], r["step_id"])
        if r["action"]["action_type"] in TAPT and "x" in r["action"]:
            E = [EX[k][key] for k in range(1, 9)]
            G.append({"pkg": r["package"], "E": E, "R": {arm: [by[key][k]["R"][arm] for k in range(1, 9)] for arm in ARMS}})
    out = {"spec": "report/333 §10 (sàng mức 1)", "verifier": V.VERSION, "n_steps": len(rows), "n_tap": len(G),
           "exec_greedy_tap": sum(EX[0][(r["episode_id"], r["step_id"])] for r in rows if (r["episode_id"], r["step_id"]) in EX[0]) / len(G),
           "exec_mau_tap": sum(sum(g["E"]) for g in G) / (8 * len(G)),
           "K_g_phan_bo": dict(collections.Counter(min(v, 6) for v in KG.values())),
           "A_phan_bo": dict(collections.Counter(by[k][j]["A"] for k in by for j in range(1, 9))),
           "tap": summarize(G)}
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rows_json = [{"episode_id": r["episode_id"], "step_id": r["step_id"], "R": [by[(r["episode_id"], r["step_id"])][k] for k in range(9)]} for r in rows]
    with open(a.out.replace(".json", "_buoc.jsonl"), "w", encoding="utf-8") as f:
        for x in rows_json:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    T = out["tap"]["arms"]
    for arm in ARMS:
        print(f"{arm:14s} conc {T[arm]['concordance']:.4f} · zero-std {T[arm]['zero_std']:.2%} · oracle +{T[arm]['oracle_up_pp']:.2f} pp", flush=True)


if __name__ == "__main__":
    main()
