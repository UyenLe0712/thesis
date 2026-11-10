#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Điểm target T của RGTC-SPICE v2 có xếp đúng 8 mẫu sinh thật không (val C1, 10/11/2026, CHỈ CPU).

Dữ liệu: 249 bước chạm của val C1, 8 mẫu S1/101 mỗi bước, kết quả exec từ reward_groups.jsonl.
Bước có T là bước active theo cấu hình no_blacklist|own|strict và qua điều kiện SPICE của gate_b_rgtc.py.
Số val, một hạt, mô hình S1 chứ không phải SFT-cont: chỉ để sàng lọc, cấm trích.

Đại lượng: độ đồng thuận trên các cặp mẫu cùng bước có exec khác nhau (hoà tính 0,5). KTC95 bootstrap cụm episode,
B = 2.000, hạt 20261110.

LUẬT KHOÁ TRƯỚC KHI CHẠY (chỉ tính trên bước active):
  Không đủ dữ liệu: dưới 30 bước active có ít nhất một cặp exec khác nhau.
  ĐẠT khi đủ cả ba:
    (a) T một mình, bỏ cặp hoà: cận dưới KTC95 > 0,5.
    (b) FULL − A2 > 0 (ước lượng điểm), tức thêm T có ích so với cùng công thức khi T trung tính.
    (c) FULL − SPICE > 0 và FULL − chrF > 0 (ước lượng điểm).
  Trượt một trong ba: RGTC dừng.
  KTC của (b), (c) phủ 0 thì chỉ được đọc là "chưa bị bác", không phải "T có ích".

Sửa 10/11 sau lượt đầu (không đổi luật): lượt đầu đọc nhầm trường số tuple nên K_g = 0 ở mọi bước, S rút về chrF; kết quả lượt đó bị bỏ.
K_g nay là tp + fn của cặp (g, g).

  python rgtc_c1_t_10_11.py --data DIR --forest all_forest_dict.zip --out OUT
"""
import argparse, itertools, json, math, pickle, re, sys, time, zipfile
from pathlib import Path

import numpy as np
from sacrebleu.metrics import CHRF

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gate_b_rgtc import classify, eval_row, parse_nodes  # noqa: E402

CFG = ("no_blacklist", "own", "strict")
words = lambda t: len(re.findall(r"[A-Za-z0-9'-]+", t))


def spice_all(pairs, batch=1500):
    """{(câu, tham chiếu): (f, số tuple của tham chiếu)}. Khoá số nguyên để SPICE trả đúng thứ tự."""
    from pycocoevalcap.spice.spice import Spice
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    eng, tk, uniq, out = Spice(), PTBTokenizer(), list(dict.fromkeys(pairs)), {}
    for st in range(0, len(uniq), batch):
        block = uniq[st:st + batch]
        gts = tk.tokenize({i: [{"caption": r}] for i, (_, r) in enumerate(block)})
        res = tk.tokenize({i: [{"caption": c}] for i, (c, _) in enumerate(block)})
        _, scores = eng.compute_score(gts, res)
        assert len(scores) == len(block)
        for p, sc in zip(block, scores):
            f = sc["All"].get("f", 0)
            f = float(f) if f is not None and math.isfinite(float(f)) else 0.0
            n = float(sc["All"]["tp"]) + float(sc["All"]["fn"])   # số tuple của tham chiếu, trường của SpiceStats
            if p[0] == p[1]:
                assert f in (0.0, 1.0), ("SPICE lệch cặp", p, f)
            out[p] = (f, n)
        print(f"[SPICE] {min(st + batch, len(uniq))}/{len(uniq)} cặp · {time.strftime('%H:%M:%S')}", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True); ap.add_argument("--forest", required=True); ap.add_argument("--out", required=True)
    a_ = ap.parse_args()
    D, OUT = Path(a_.data), Path(a_.out)
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    C = [json.loads(l) for l in open(D / "c1_mau.jsonl", encoding="utf8")]
    G = [json.loads(l) for l in open(D / "reward_groups.jsonl", encoding="utf8")]
    R = [json.loads(l) for l in open(D / "c1_recs.jsonl", encoding="utf8")]
    ocr = {o["image"]: o.get("items") or [] for o in map(json.loads, open(D / "ocr.jsonl", encoding="utf8"))}
    assert [(a["episode_id"], a["step_id"]) for a in G] == [(a["episode_id"], a["step_id"]) for a in C] == [(a["episode_id"], a["step_id"]) for a in R]
    z = zipfile.ZipFile(a_.forest)
    names = set(z.namelist())
    steps, no_tree = [], 0
    for c, g, r in zip(C, G, R):
        if g["action"] != "click":
            continue
        assert c["gold"] == r["target_instruction"]
        k = f"all_forest_dict/android_control_episode_[{r['episode_id']}]_{r['step_id']}.pkl"
        v = {"e_pre": False, "m": False, "reason": "0_no_tree"}
        if k in names:
            v = eval_row(r, parse_nodes(pickle.loads(z.read(k))), ocr.get(r["image"], []), CFG)
        else:
            no_tree += 1
        steps.append(dict(ep=c["episode_id"], st=c["step_id"], gold=c["gold"], y=c["mau"], e=g["outcomes"], r0=g["rs"]["R0_historical"],
                          neg=v.get("g_neg") if v["e_pre"] and v["m"] else None, gold_used=v.get("gold"), reason=v.get("reason") or v.get("m_reason")))
    assert len(steps) == 249
    pairs = []
    for s in steps:
        g = s["gold"]
        pairs.append((g, g))
        pairs += [(y, g) for y in s["y"] if y.strip()]
        if s["neg"]:
            n, u = s["neg"], s["gold_used"]
            pairs += [(n, n), (u, u), (u, n), (n, u)]
            pairs += [(y, u) for y in s["y"] if y.strip()] + [(y, n) for y in s["y"] if y.strip()]
    print(f"[dữ liệu] 249 bước chạm · thiếu cây {no_tree} · có cặp phản thực {sum(1 for s in steps if s['neg'])} · {len(set(pairs))} cặp SPICE", flush=True)
    sp = spice_all(pairs)
    ch = CHRF()
    for s in steps:
        g = s["gold"]
        kg = sp[(g, g)][1]
        s["kg"] = kg
        a_g = 0.8 * min(1, kg / 3)
        # chỉ dùng T khi cặp qua điều kiện SPICE, giống gate_b_rgtc.py
        act = False
        if s["neg"]:
            n, u = s["neg"], s["gold_used"]
            act = sp[(u, u)][0] == 1.0 and sp[(n, n)][0] == 1.0 and sp[(u, n)][0] < 1.0
        s["active"] = act
        arms = {k: [] for k in ("SPICE", "chrF", "A1", "A2", "T", "FULL")}
        for y, r0 in zip(s["y"], s["r0"]):
            if not y.strip():
                for v in arms.values():
                    v.append(0.0)
                continue
            d_hist = 0.02 * max(0, words(y) - words(g) - 3)
            sv = sp[(y, g)][0]
            assert abs(sv - d_hist - r0) < 1e-6, ("Không tái lập R0 8/11", y, g, sv, d_hist, r0)   # chứng minh SPICE đúng cặp
            d = min(0.05, d_hist)
            cf = ch.sentence_score(y, [g]).score / 100
            S = a_g * sv + (1 - a_g) * cf
            exp, ref, pred = "tap", classify(g), classify(y)
            A = 0.5 if ref != exp or pred is None else float(pred == exp)
            T = 0.5
            if act:
                T = min(1.0, max(0.0, 0.5 + 0.5 * (sp[(y, s["gold_used"])][0] - sp[(y, s["neg"])][0])))
            cl = lambda x: min(1.0, max(0.0, x))
            arms["SPICE"].append(sv); arms["chrF"].append(cf); arms["T"].append(T)
            arms["A1"].append(cl(.7 * S + .075 + .075 - d))
            arms["A2"].append(cl(.7 * S + .15 * A + .075 - d))
            arms["FULL"].append(cl(.7 * S + .15 * A + .15 * T - d))
        s["arms"] = arms

    def dem(s, n):
        r, e = s["arms"][n], s["e"]
        w = l = t = 0
        for i, j in itertools.combinations(range(8), 2):
            if e[i] == e[j]:
                continue
            if abs(r[i] - r[j]) < 1e-9:
                t += 1
            elif (r[i] - r[j]) * (e[i] - e[j]) > 0:
                w += 1
            else:
                l += 1
        return w, l, t

    arm_names = list(steps[0]["arms"])
    def f(tab, I, hoa):
        w, l, t = tab[I].sum(0)
        return (w + .5 * t) / max(w + l + t, 1) if hoa else w / max(w + l, 1)

    def tinh(sub, seed):
        tab = {n: np.array([dem(s, n) for s in sub]) for n in arm_names}
        all_I = np.arange(len(sub))
        eps = sorted({s["ep"] for s in sub})
        idx = {e: [i for i, s in enumerate(sub) if s["ep"] == e] for e in eps}
        rng = np.random.default_rng(seed)
        boots = [np.concatenate([idx[eps[j]] for j in rng.integers(0, len(eps), len(eps))]) for _ in range(2000)]
        out = {"n_buoc": len(sub), "n_episode": len(eps), "n_buoc_co_cap": int(sum(1 for i in all_I if tab["T"][i].sum() > 0)), "muc": {}, "so": {}}
        for n in arm_names:
            w, l, t = (int(x) for x in tab[n].sum(0))
            b = [f(tab[n], I, False) for I in boots]
            out["muc"][n] = dict(dung=w, sai=l, hoa=t, dong_thuan=round(f(tab[n], all_I, True), 4), bo_hoa=round(f(tab[n], all_I, False), 4),
                                 bo_hoa_ktc=[round(float(np.percentile(b, 2.5)), 4), round(float(np.percentile(b, 97.5)), 4)])
        for x, y in [("FULL", "A2"), ("FULL", "SPICE"), ("FULL", "chrF"), ("A2", "chrF")]:
            b = [f(tab[x], I, True) - f(tab[y], I, True) for I in boots]
            out["so"][f"{x} − {y}"] = dict(delta=round(f(tab[x], all_I, True) - f(tab[y], all_I, True), 4),
                                           lo=round(float(np.percentile(b, 2.5)), 4), hi=round(float(np.percentile(b, 97.5)), 4))
        return out

    kgs = sorted(s["kg"] for s in steps)
    assert kgs[len(kgs) // 2] >= 1, "K_g vẫn bằng 0"
    print("[K_g] trung vị", kgs[len(kgs) // 2], "· số bước K_g < 3:", sum(k < 3 for k in kgs), flush=True)
    act = [s for s in steps if s["active"]]
    rep = {"pham_vi": "val C1, 8 mẫu S1/101, một hạt; chỉ sàng lọc, cấm trích", "cau_hinh": "|".join(CFG), "thieu_cay": no_tree,
           "buoc_active": len(act), "buoc_cham": len(steps), "active": tinh(act, 20261110), "toan_bo_249": tinh(steps, 20261110)}
    a = rep["active"]
    du = a["n_buoc_co_cap"] >= 30
    ca = a["muc"]["T"]["bo_hoa_ktc"][0] > 0.5
    cb = a["so"]["FULL − A2"]["delta"] > 0
    cc = a["so"]["FULL − SPICE"]["delta"] > 0 and a["so"]["FULL − chrF"]["delta"] > 0
    rep["ket_luan"] = dict(du_du_lieu=du, a_T_co_tin_hieu=bool(ca), b_them_T_co_ich=bool(cb), c_hon_SPICE_va_chrF=bool(cc),
                           ket_qua="KHÔNG ĐỦ DỮ LIỆU" if not du else ("ĐẠT" if ca and cb and cc else "TRƯỢT"))
    json.dump(rep, open(OUT / "c1_t.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
    with open(OUT / "c1_t_buoc.jsonl", "w", encoding="utf8") as fo:
        for s in steps:
            fo.write(json.dumps({k: s.get(k) for k in ("ep", "st", "gold", "neg", "active", "reason", "kg", "e", "y", "arms")}, ensure_ascii=False) + "\n")
    print(json.dumps(rep, ensure_ascii=False, indent=0))
    print("XONG", f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
