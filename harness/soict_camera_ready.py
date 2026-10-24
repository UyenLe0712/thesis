# -*- coding: utf-8 -*-
"""SOICT camera-ready (GUIStep, 5590): hai phép tính cho phản biện, 0 GPU, chạy từ tệp thô.

    python3 harness/soict_camera_ready.py        # in bảng + ghi runs/soict_camera_ready.json

B2  tách bước theo việc câu chuẩn có LẶP trong tập dạy hay không, và theo app chưa thấy.
    Câu chuẩn "lặp" = sau khi hạ chữ thường, bỏ dấu câu, gộp khoảng trắng thì trùng một
    `target_instruction` của train.jsonl (64.567 bước). Số "nguyên văn" (chỉ cắt khoảng trắng
    đầu/cuối) in kèm. Thay con số 17,3% cũ trong bài vốn không có script tái lập.
B3  phép so ghép cặp bằng bootstrap gom cụm thay McNemar: cụm = app, bước không gán được app
    tự thành một cụm theo tác vụ (đúng quy ước `d3_ktc.py`). p hai phía = 2·min(P(Δ*≤0), P(Δ*≥0)).
    KTC lấy từ `score_run.cluster_bootstrap` nên phải khớp `d3_ktc.json` tuyệt đối.
Thước: D.3 (cột `d3` của `luat_d3.py`), chính là "executability" trong bài.
"""
import os, re, json, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import luat_d3 as L
import score_run as S

ROOT = os.path.join(HERE, "..")
TRAIN = os.path.join(HERE, "dg1_cache", "train_ac", "train.jsonl")
TEN = {"Base": "Base", "S": "S1/101", "D": "S2/101", "P": "MIN-DESC/101", "CE2": "CE2-S2/101"}
B = 10000
SO = [("S", "Base"), ("D", "S"), ("P", "S"), ("P", "CE2"), ("P", "D"), ("P", "Base")]


def chuan(s):
    s = re.sub(r"[^\w\s]", " ", (s or "").casefold())
    return " ".join(s.split())


def main():
    tr = [json.loads(l)["target_instruction"] for l in open(TRAIN, encoding="utf-8")]
    nguyen = {t.strip() for t in tr}
    chuan_tr = {chuan(t) for t in tr}
    nh = dict(L.NHANH)
    X = {}
    for a, t in TEN.items():
        R = L.nap(os.path.join(L.RUNS, nh[t]))
        X[a] = {k: L.luat(r, k)["d3"] for k, r in R.items()}
        if a == "Base":
            ref = R
    K = list(ref)                                   # thứ tự dòng tệp thô, như d3_ktc
    assert len(K) == 4463 and all(set(X[a]) == set(K) for a in X)
    cum = {k: ref[k].get("app") or f"ep{ref[k]['episode_id']}" for k in K}
    lap_ng = {k: ref[k]["gold_instruction"].strip() in nguyen for k in K}
    lap = {k: chuan(ref[k]["gold_instruction"]) in chuan_tr for k in K}
    seen = {k: ref[k].get("app_seen_in_train") for k in K}
    out = {"n": len(K), "lap_nguyen_van": sum(lap_ng.values()), "lap_chuan_hoa": sum(lap.values()),
           "app_chua_thay": sum(1 for k in K if seen[k] is False),
           "app_chua_thay_so_app": len({ref[k]["app"] for k in K if seen[k] is False}),
           "nhom": {}, "so_sanh": {}, "B": B, "seed": S.SEED}
    print(f"n={len(K)} · lặp nguyên văn {out['lap_nguyen_van']} ({100*out['lap_nguyen_van']/len(K):.1f}%) · "
          f"lặp sau chuẩn hoá {out['lap_chuan_hoa']} ({100*out['lap_chuan_hoa']/len(K):.1f}%) · "
          f"app chưa thấy {out['app_chua_thay']} bước / {out['app_chua_thay_so_app']} app")

    def boot_p(Ks, f):
        """p hai phía của Δ trung bình gom cụm; cùng cấu trúc cụm với cluster_bootstrap."""
        cl = {}
        for k in Ks:
            cl.setdefault(cum[k], []).append(f(k))
        num = np.array([sum(v) for v in cl.values()], float)
        den = np.array([len(v) for v in cl.values()], float)
        G = len(num)
        rng = np.random.default_rng(S.SEED)
        idx = rng.integers(0, G, size=(B, G))
        d = num[idx].sum(1) / den[idx].sum(1)
        le, ge = (d <= 0).sum(), (d >= 0).sum()
        return min(1.0, 2 * (min(le, ge) + 1) / (B + 1)), G

    def ktc(Ks, f):
        U = [(k, f(k)) for k in Ks]
        pt, (lo, hi), G, _ = S.cluster_bootstrap(U, lambda u: cum[u[0]], lambda u: u[1], B=B, seed=S.SEED)
        return 100 * pt, 100 * lo, 100 * hi, G

    nhom = {"toan_bo": K, "lap": [k for k in K if lap[k]], "chua_lap": [k for k in K if not lap[k]],
            "app_chua_thay": [k for k in K if seen[k] is False]}
    for g, Ks in nhom.items():
        print(f"\n== nhóm {g} (n={len(Ks)}) ==")
        out["nhom"][g] = {"n": len(Ks)}
        for a in TEN:
            p, lo, hi, G = ktc(Ks, lambda k: X[a][k])
            out["nhom"][g][a] = dict(diem=round(p, 2), lo=round(lo, 2), hi=round(hi, 2))
            print(f"  {a:5s} {p:6.2f} [{lo:6.2f}; {hi:6.2f}]")
        for a, b in SO:
            if g == "app_chua_thay" and False:
                continue
            f = lambda k: X[a][k] - X[b][k]
            d, lo, hi, _ = ktc(Ks, f)
            p, G = boot_p(Ks, f)
            out["so_sanh"][f"{a}-{b}|{g}"] = dict(delta=round(d, 2), lo=round(lo, 2), hi=round(hi, 2),
                                                  p_cum=round(p, 4), G=G)
            print(f"  {a}-{b:5s} {d:+6.2f} [{lo:+6.2f}; {hi:+6.2f}] p_cụm={p:.4f}")

    # tự kiểm với d3_ktc.json (KTC phải khớp tuyệt đối)
    ref_json = os.path.join(ROOT, "runs", "d3_ktc.json")
    if os.path.exists(ref_json):
        kt = json.load(open(ref_json, encoding="utf-8"))["so_sanh"]
        for a, b in (("S1/101", "Base"), ("MIN-DESC/101", "S1/101"), ("MIN-DESC/101", "CE2-S2/101"),
                     ("S2/101", "S1/101")):
            r1 = kt[f"{a} − {b} · d3"]
            ak = [x for x, t in TEN.items() if t == a][0]; bk = [x for x, t in TEN.items() if t == b][0]
            r2 = out["so_sanh"][f"{ak}-{bk}|toan_bo"]
            assert (r1["delta"], r1["lo"], r1["hi"]) == (r2["delta"], r2["lo"], r2["hi"]), (a, b, r1, r2)
        print("\n✅ tự kiểm: Δ và KTC khớp tuyệt đối runs/d3_ktc.json (4 phép so)")
    p = os.path.join(ROOT, "runs", "soict_camera_ready.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", p)


if __name__ == "__main__":
    main()
