# -*- coding: utf-8 -*-
"""Độ đo văn bản DEV-v3 lượt đầu (15/11/2026): SFT-cont · SA-SPICE-v3 ck500/ck400 · chrF ck400, greedy 2.223 bước.
CPU + Java 8 (chạy Kaggle CPU).   python -u chu_sa3_dev_15_11.py [--B 2000] [--smoke 40]  → runs/chu_sa3_dev_15_11.json

Tính trên cả 2.223 bước và tập con 1.338 bước chạm (CIDEr-D tập con dùng IDF của 2.223 bước). Bootstrap cụm theo
episode, cùng chỉ số cho mọi nhánh (ghép cặp). METEOR mức kho, không KTC. Số DEV, cấm trích.
Tự kiểm: BLEU-4/chrF tính hai đường (từ thống kê từng bước và từ sacrebleu/coco trọn kho) phải trùng."""
import argparse, json, math
from pathlib import Path
import numpy as np
import ktc_chu_27_10 as K

R = K.RUNS
NH = {"SFT-cont": "dev_sftcont.jsonl", "SA-SPICE-v3 ck500": "dev_sa_ck500.jsonl",
      "SA-SPICE-v3 ck400": "dev_sa_ck400.jsonl", "chrF ck400": "dev_chrf_ck400.jsonl"}
SO = [("SA-SPICE-v3 ck500", "SFT-cont"), ("SA-SPICE-v3 ck400", "SFT-cont"), ("chrF ck400", "SFT-cont"),
      ("SA-SPICE-v3 ck400", "chrF ck400"), ("SA-SPICE-v3 ck500", "chrF ck400"), ("SA-SPICE-v3 ck500", "SA-SPICE-v3 ck400")]
TAP = {"click", "long_press"}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=2000); ap.add_argument("--smoke", type=int, default=0)
    a = ap.parse_args()
    K.CACHE = R / ("chu_sa3_dev_cache" + ("_smoke" if a.smoke else ""))
    goc = [json.loads(l) for l in open(R / NH["SFT-cont"], encoding="utf-8")]
    if a.smoke:
        goc = goc[:a.smoke]
    thu_tu = [K.kh(r) for r in goc]
    D = {}
    for t, f in NH.items():                      # đổi về dạng hàng tung_buoc đọc (sent, gold_instruction)
        rr = {K.kh(r): r for r in map(json.loads, open(R / f, encoding="utf-8"))}
        assert set(thu_tu) <= set(rr)
        tg = R / f"_rows_{f}"
        with open(tg, "w", encoding="utf-8") as o:
            for k in thu_tu:
                r = rr[k]; assert r["gold"] == rr[k]["gold"]
                o.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "sent": r["pred"],
                                    "gold_instruction": r["gold"]}, ensure_ascii=False) + "\n")
        D[t], _ = K.tung_buoc(t, tg.name, thu_tu)
    tap = np.array([i for i, r in enumerate(goc) if r["action_type"] in TAP])
    print(f"bước {len(goc)} · chạm {len(tap)}", flush=True)
    # tự kiểm chrF / BLEU-4 trọn kho
    import sacrebleu
    for t, f in NH.items():
        rows = [json.loads(l) for l in open(R / f"_rows_{f}", encoding="utf-8")]
        c2 = sacrebleu.corpus_chrf([r["sent"].strip() for r in rows], [[r["gold_instruction"].strip() for r in rows]]).score
        c1 = K.diem(D[t])["chrf"]
        assert abs(c1 - c2) < 1e-6, (t, c1, c2)
    print("✅ tự kiểm chrF trọn kho", flush=True)
    cl = {}
    for i, r in enumerate(goc):
        cl.setdefault(r["episode_id"], []).append(i)
    cum = [np.array(v) for v in cl.values()]
    tapset = set(tap.tolist())
    G = len(cum); rng = np.random.default_rng(20261115)
    out = {"n": len(goc), "n_cham": len(tap), "cum": G}
    for phan, base in (("toan_bo", None), ("cham", tap)):
        pt = {t: K.diem(D[t], base) for t in NH}
        kq = {t: {k: [] for k in K.THUOC} for t in NH}
        for b in range(a.B):
            idx = np.concatenate([cum[j] for j in rng.integers(0, G, G)])
            if base is not None:
                idx = idx[np.isin(idx, tap)]
            for t in NH:
                p = K.diem(D[t], idx)
                for k in K.THUOC:
                    kq[t][k].append(p[k])
            if (b + 1) % 200 == 0:
                print(f"  {phan} bootstrap {b+1}/{a.B}", flush=True)
        o = {"diem": {t: {k: dict(diem=round(pt[t][k], 2), lo=round(float(np.percentile(kq[t][k], 2.5)), 2),
                                  hi=round(float(np.percentile(kq[t][k], 97.5)), 2)) for k in K.THUOC} for t in NH}, "so": {}}
        for x, y in SO:
            o["so"][f"{x} − {y}"] = {}
            for k in K.THUOC:
                dl = np.array(kq[x][k]) - np.array(kq[y][k])
                o["so"][f"{x} − {y}"][k] = dict(delta=round(pt[x][k] - pt[y][k], 2), lo=round(float(np.percentile(dl, 2.5)), 2),
                                                hi=round(float(np.percentile(dl, 97.5)), 2))
            print(f"  [{phan}] {x} − {y}: " + " · ".join(f"{k} {v['delta']:+.2f} [{v['lo']:+.2f}; {v['hi']:+.2f}]"
                                                         for k, v in o["so"][f"{x} − {y}"].items()), flush=True)
        for t in NH:
            print(f"  [{phan}] {t}: " + " · ".join(f"{k} {v['diem']:.2f}" for k, v in o["diem"][t].items()), flush=True)
        out[phan] = o
    from pycocoevalcap.meteor.meteor import Meteor
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    out["meteor"] = {}
    for t, f in NH.items():
        rows = [json.loads(l) for l in open(R / f"_rows_{f}", encoding="utf-8")]
        for phan, ids in (("toan_bo", range(len(rows))), ("cham", tap.tolist())):
            tk = PTBTokenizer()
            g = tk.tokenize({i: [{"caption": rows[i]["gold_instruction"].strip()}] for i in ids})
            h = tk.tokenize({i: [{"caption": rows[i]["sent"].strip()}] for i in ids})
            out["meteor"][f"{t} · {phan}"] = round(100 * Meteor().compute_score(g, h)[0], 2)
    print("METEOR", out["meteor"], flush=True)
    json.dump(out, open(R / ("chu_sa3_dev_15_11" + ("_smoke" if a.smoke else "") + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
