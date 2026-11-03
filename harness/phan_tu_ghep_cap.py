# -*- coding: utf-8 -*-
"""So ghép cặp trực tiếp phần đổi phần tử giữa các lượt lưới RL (report/320 mục 14.5) — 0 GPU. Hậu kiểm, chọn sau khi thấy số.

Mỗi bước, so với S1/101: phần tử = +1 nếu cứu mà S1 đúng loại, −1 nếu phá mà nhánh đúng loại; loại thao tác = phần cứu/phá còn lại.
Hai cách đọc độc lập nhau:
  qua_s1    hiệu điểm từng bước giữa hai nhánh (có S1 làm mốc); KTC bootstrap cụm app, p dấu chính xác trên bước khác nhau.
  truc_tiep exec của hai nhánh trên bước cả hai đúng loại thao tác (không qua S1); KTC bootstrap, McNemar chính xác.
Holm tính trong từng họ. Tự kiểm: tổng từng bước phải ra đúng phan_ra.json (ck500 +28/+41). Ghi runs/luoi/test_2_11/phan_tu_ghep_cap.json.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.stats import binomtest
import score_run as S

K = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "runs")
T = "luoi/test_2_11/score_%s_101_test_raw.jsonl"
N = {"ck500": "grpo_spice/score_ck500_test_raw.jsonl", "SCST + SPICE": T % "scst_spice", "GRPO + CIDEr-D": T % "grpo_cider",
     "GRPO + METEOR": T % "grpo_meteor", "GRPO + ROUGE-L": T % "grpo_rougel"}
KHAC = ["GRPO + CIDEr-D", "GRPO + METEOR", "GRPO + ROUGE-L"]
B, SEED = int(os.environ.get("B", 10000)), S.SEED
nap = lambda f: {(x["episode_id"], x["step_id"]): x for x in map(json.loads, open(os.path.join(K, f), encoding="utf-8"))}
e = lambda r: int(bool(r.get("executable", 0)))
a = lambda r: int(bool(r.get("action_ok", 0)))


def holm(ps):
    thu, kq, m = sorted(ps, key=ps.get), {}, 0.0
    for i, t in enumerate(thu):
        m = max(m, min(1.0, ps[t] * (len(thu) - i)))
        kq[t] = m
    return kq


def main():
    s1 = nap("score_s1_seed101_raw.jsonl")
    X = {t: nap(f) for t, f in N.items()}
    ks = sorted(s1)
    cum = {k: s1[k].get("app") or f"ep{k[0]}" for k in ks}
    for t in X:
        assert set(X[t]) == set(s1), t
    pt = {t: {k: (e(X[t][k]) - e(s1[k])) * (a(s1[k]) if e(X[t][k]) else a(X[t][k])) for k in ks} for t in X}
    lt = {t: {k: (e(X[t][k]) - e(s1[k])) - pt[t][k] for k in ks} for t in X}
    tong = {t: (sum(lt[t].values()), sum(pt[t].values())) for t in X}
    print("tổng (loại, phần tử):", tong, flush=True)
    if tong["ck500"] != (28, 41):
        sys.exit(f"⛔ DỪNG, không tái lập ck500 +28/+41: {tong['ck500']}")
    if os.path.exists(os.path.join(K, "luoi/test_2_11/phan_ra.json")):
        pr = json.load(open(os.path.join(K, "luoi/test_2_11/phan_ra.json"), encoding="utf-8"))
        for t in X:
            assert tong[t] == (pr[t]["rong_loai"], pr[t]["rong_phan_tu"]), (t, tong[t])
    print("✅ tái lập phân rã", flush=True)

    def bs(d, tap=None):
        q = tap if tap is not None else ks
        p, (lo, hi), _, _ = S.cluster_bootstrap([(k, d[k]) for k in q], lambda u: cum[u[0]], lambda u: u[1], B=B, seed=SEED)
        hon, kem = sum(d[k] > 0 for k in q), sum(d[k] < 0 for k in q)
        return dict(buoc_rong=round(p * len(q), 1), diem=round(100 * p, 2), lo=round(100 * lo, 2), hi=round(100 * hi, 2), hon=hon, kem=kem,
                    n=len(q), p=float(binomtest(hon, hon + kem).pvalue) if hon + kem else 1.0)

    out = dict(B=B, seed=SEED, tong=tong, qua_s1={}, truc_tiep={}, tuong_phan={})
    for ten, D in (("phan_tu", pt), ("loai", lt)):
        o = {f"ck500 − {t}": bs({k: D["ck500"][k] - D[t][k] for k in ks}) for t in N if t != "ck500"}
        for t, h in holm({t: v["p"] for t, v in o.items()}).items():
            o[t]["p_holm"] = h
        out["qua_s1"][ten] = o
        tb = {k: sum(D[t][k] for t in KHAC) / 3 for k in ks}
        out["tuong_phan"][ten] = {"ck500 − TB ba độ đo khác (cùng GRPO)": bs({k: D["ck500"][k] - tb[k] for k in ks}),
                                  "TB hai lượt SPICE − TB ba độ đo khác": bs({k: (D["ck500"][k] + D["SCST + SPICE"][k]) / 2 - tb[k] for k in ks})}
        print(ten, json.dumps(out["qua_s1"][ten], ensure_ascii=False), json.dumps(out["tuong_phan"][ten], ensure_ascii=False), flush=True)
    o = {}
    for t in N:
        if t == "ck500":
            continue
        tap = [k for k in ks if a(X["ck500"][k]) and a(X[t][k])]
        o[f"ck500 − {t}"] = bs({k: e(X["ck500"][k]) - e(X[t][k]) for k in tap}, tap)
    for t, h in holm({t: v["p"] for t, v in o.items()}).items():
        o[t]["p_holm"] = h
    out["truc_tiep"] = o
    print("trực tiếp", json.dumps(o, ensure_ascii=False), flush=True)
    json.dump(out, open(os.path.join(K, "luoi/test_2_11/phan_tu_ghep_cap.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("✅ xong", flush=True)


if __name__ == "__main__":
    main()
