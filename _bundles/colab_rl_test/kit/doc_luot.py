# -*- coding: utf-8 -*-
"""Đọc một lượt test RL hoặc SFT tiếp: so với S1/101 và ck500, phân rã loại thao tác và phần tử. Tự kiểm ck500 − S1 ra +1,55 [+0,80; +2,33] và +28/+41.

  python doc_luot.py --harness H --s1 raw_s1.jsonl --ck raw_ck500.jsonl --ten REINFORCE --raw score_x_test_raw.jsonl --out doc_x.json
"""
import argparse, json, sys
from scipy.stats import binomtest

ap = argparse.ArgumentParser()
for x in ("--harness", "--s1", "--ck", "--raw", "--ten", "--out"):
    ap.add_argument(x, required=True)
ap.add_argument("--B", type=int, default=10000)
a = ap.parse_args()
sys.path.insert(0, a.harness)
import score_run as S

nap = lambda f: {(x["episode_id"], x["step_id"]): x for x in map(json.loads, open(f, encoding="utf-8"))}
e = lambda r: int(bool(r.get("executable", 0)))
t = lambda r: int(bool(r.get("action_ok", 0)))
s1, ck, sf = nap(a.s1), nap(a.ck), nap(a.raw)
assert set(s1) == set(ck) == set(sf) and len(s1) == 4463, (len(s1), len(ck), len(sf))
ks = sorted(s1)
cum = {k: s1[k].get("app") or f"ep{k[0]}" for k in ks}


def so(A, Bn, B=None):
    p, (lo, hi), _, _ = S.cluster_bootstrap([(k, e(A[k]) - e(Bn[k])) for k in ks], lambda u: cum[u[0]], lambda u: u[1], B=B or a.B, seed=S.SEED)
    hon, kem = sum(e(A[k]) > e(Bn[k]) for k in ks), sum(e(A[k]) < e(Bn[k]) for k in ks)
    return dict(delta=round(100 * p, 2), lo=round(100 * lo, 2), hi=round(100 * hi, 2), hon=hon, kem=kem, p=float(binomtest(hon, hon + kem).pvalue))


def phan_ra(X):
    pt = {k: (e(X[k]) - e(s1[k])) * (t(s1[k]) if e(X[k]) else t(X[k])) for k in ks}
    lt = {k: e(X[k]) - e(s1[k]) - pt[k] for k in ks}
    f = lambda d: dict(rong=sum(d.values()), cuu=sum(v > 0 for v in d.values()), pha=sum(v < 0 for v in d.values()),
                       p=float(binomtest(sum(v > 0 for v in d.values()), max(1, sum(v != 0 for v in d.values()))).pvalue))
    return dict(loai=f(lt), phan_tu=f(pt)), pt, lt


goc = so(ck, s1)
assert (goc["delta"], goc["lo"], goc["hi"]) == (1.55, 0.80, 2.33) or a.B != 10000, f"⛔ không tái lập ck500 − S1: {goc}"
prc, ptc, ltc = phan_ra(ck)
assert (prc["loai"]["rong"], prc["phan_tu"]["rong"]) == (28, 41), f"⛔ không tái lập +28/+41: {prc}"
print("✅ tự kiểm: ck500 − S1", goc, "· +28/+41", flush=True)
prs, pts, lts = phan_ra(sf)


def hieu(d1, d2):
    d = {k: d1[k] - d2[k] for k in ks}
    p, (lo, hi), _, _ = S.cluster_bootstrap([(k, d[k]) for k in ks], lambda u: cum[u[0]], lambda u: u[1], B=a.B, seed=S.SEED)
    hon, kem = sum(v > 0 for v in d.values()), sum(v < 0 for v in d.values())
    return dict(buoc=sum(d.values()), diem=round(100 * p, 2), lo=round(100 * lo, 2), hi=round(100 * hi, 2), hon=hon, kem=kem,
                p=float(binomtest(hon, hon + kem).pvalue) if hon + kem else 1.0)


tu = lambda R: round(sum(len((R[k].get("sent") or "").split()) for k in ks) / len(ks), 2)
out = dict(
    diem={n: dict(exec=round(100 * sum(e(R[k]) for k in ks) / len(ks), 2), dung_loai=round(100 * sum(t(R[k]) for k in ks) / len(ks), 2), so_tu=tu(R))
          for n, R in (("S1/101", s1), ("ck500", ck), (a.ten, sf))},
    x_tru_s1=so(sf, s1), ck500_tru_x=so(ck, sf), ck500_tru_s1=goc,
    phan_ra_so_s1={"ck500": prc, a.ten: prs},
    ck500_tru_x_phan_tu=hieu(ptc, pts), ck500_tru_x_loai=hieu(ltc, lts),
    cau_trung=dict(x_s1=sum((sf[k].get("sent") or "") == (s1[k].get("sent") or "") for k in ks),
                   ck500_s1=sum((ck[k].get("sent") or "") == (s1[k].get("sent") or "") for k in ks),
                   x_ck500=sum((sf[k].get("sent") or "") == (ck[k].get("sent") or "") for k in ks)))
json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1), flush=True)
