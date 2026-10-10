# -*- coding: utf-8 -*-
"""304 — exec / D.3 / AitW đầy đủ cho ra_k4 và ghep trên 4.463 bước click test, 0 GPU.

Kaggle `ra-exec-test-304` chỉ chấm UGround những bước có câu KHÁC ck500 (so từng byte); bước còn lại lấy
nguyên dòng của `runs/grpo_spice/score_ck500_test_raw.jsonl` (cùng score_run trong thesis-score, cùng T4).
Tự kiểm: 40 câu ck500 không đổi được chấm lại phải ra cùng toạ độ với tệp thô cũ; exec ck500 = 60,65.

    python3 _scripts/304/kiem/doc_exec_304.py runs/ra304_G/exec_out
"""
import glob, json, os, sys

KHO = "/mnt/d/Master/Thesis"
sys.path.insert(0, f"{KHO}/harness")
os.chdir(f"{KHO}/harness")
import luat_d3 as L
from luat_aitw_day_du import aitw_full
from d3_ktc import ktc, mcnemar
kh = L.kh   # khoá (str, str) như luat_d3

E = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else f"{KHO}/runs/ra304_G/exec_out")
CK = L.nap(f"{KHO}/runs/grpo_spice/score_ck500_test_raw.jsonl")
S1 = L.nap(f"{KHO}/runs/score_s1_seed101_raw.jsonl")
moi = lambda t: {kh(r): r for f in sorted(glob.glob(f"{E}/score_{t}_*_raw.jsonl")) for r in map(json.loads, open(f))}
CAL, GH, RA = moi("cal"), moi("ghep"), moi("ra")
P = lambda p: {kh(x): x["pred"] for x in map(json.loads, open(p, encoding="utf-8"))}
S = "/mnt/d/Master/Thesis/runs/ra304_G/"
pr, pg = P(S + "pred_ra_k4_test.jsonl"), P(S + "pred_ghep_test.jsonl")

# --- tự kiểm dụng cụ
lech = [k for k in CAL if CAL[k].get("pred_xy") != CK[k].get("pred_xy") or CAL[k]["executable"] != CK[k]["executable"]]
print(f"[hiệu chuẩn] {len(CAL)} câu ck500 chấm lại · lệch toạ độ/exec {len(lech)}", lech[:3])
assert len(CAL) == 40, "thiếu dòng hiệu chuẩn"
for ten, X, pred in (("ghep", GH, pg), ("ra", RA, pr)):
    sai = [k for k in X if X[k].get("sent") != pred[k]]
    print(f"[{ten}] {len(X)} dòng chấm mới · câu trong tệp thô khác tệp pred: {len(sai)}")
    assert not sai
can_r = {k for k in pr if pr[k] != (CK[k].get("sent") or "")}
can_g = {k for k in pg if pg[k] != (CK[k].get("sent") or "")}
assert can_g == set(GH) and can_r == set(GH) | set(RA), "tập bước đã chấm không khớp tập bước câu khác ck500"

R_ra = {k: (GH.get(k) or RA.get(k) or CK[k]) for k in CK}
R_gh = {k: (GH.get(k) or CK[k]) for k in CK}
for ten, R in (("ra_k4", R_ra), ("ghep", R_gh)):
    with open(f"{E}/score_{ten}_gop_raw.jsonl", "w", encoding="utf-8") as f:
        for k in CK:
            f.write(json.dumps(R[k], ensure_ascii=False) + "\n")

K = list(S1)
assert set(K) == set(CK) and len(K) == 4463
lu = lambda R: {k: dict(L.luat(R[k], k), aitwf=aitw_full(R[k], k)) for k in K}
for R in (CK, R_ra, R_gh, S1):
    for k in K:
        for c in ("executable", "action_ok", "toggle_ok", "hit_disk"):
            R[k].setdefault(c, 0)
X = {"ck500": lu(CK), "ra_k4": lu(R_ra), "ghep": lu(R_gh), "S1/101": lu(S1)}
cum = {k: S1[k].get("app") or f"ep{k[0]}" for k in K}
out = {"ktc": {}, "so_sanh": {}, "n_cham_moi": {"ghep": len(GH), "ra_k4": len(GH) + len(RA)}, "hieu_chuan_lech": len(lech)}
TEN = {"vor": "exec", "d3": "D.3", "aitwf": "AitW"}
for t in X:
    out["ktc"][t] = {}
    for c in TEN:
        p, lo, hi, _ = ktc(K, lambda k, cc: X[t][k][cc], c, cum)
        out["ktc"][t][c] = dict(diem=round(p, 2), lo=round(lo, 2), hi=round(hi, 2))
    print(f"{t:7s} " + " · ".join(f"{TEN[c]} {out['ktc'][t][c]['diem']:.2f} [{out['ktc'][t][c]['lo']:.2f}; {out['ktc'][t][c]['hi']:.2f}]" for c in TEN))
assert abs(out["ktc"]["ck500"]["vor"]["diem"] - 60.65) < 0.01, "ck500 exec phải tái lập 60,65"
print("[tự kiểm] ck500 exec 60,65 KHỚP\n")
for a, b in (("ra_k4", "ck500"), ("ghep", "ck500"), ("ra_k4", "S1/101"), ("ghep", "S1/101")):
    for c in TEN:
        d, lo, hi, _ = ktc(K, lambda k, cc: X[a][k][cc] - X[b][k][cc], c, cum)
        pha, cuu, chi, p = mcnemar(K, X[b], X[a], c)   # pha: gốc trúng, mới trượt
        out["so_sanh"][f"{a} − {b} · {TEN[c]}"] = dict(delta=round(d, 2), lo=round(lo, 2), hi=round(hi, 2), cuu=cuu, pha=pha, p=p)
        print(f"{a+' − '+b:16s} {TEN[c]:5s} {d:+.2f} [{lo:+.2f}; {hi:+.2f}] · cứu {cuu} phá {pha} · p={p:.3g}")
json.dump(out, open(f"{E}/doc_exec_304.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("→", f"{E}/doc_exec_304.json")
