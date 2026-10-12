# -*- coding: utf-8 -*-
"""308/309 — exec / D.3 / AitW đầy đủ cho một tệp câu (CW-RA) trên 4.463 bước click tập kiểm, 0 GPU.

Kaggle chỉ chấm UGround những bước có câu KHÁC ck500 (so từng byte với `sent` của tệp thô ck500); bước còn lại lấy
nguyên dòng của `runs/grpo_spice/score_ck500_test_raw.jsonl`. Cách làm y lượt 304 (doc_exec_304.py).
Tự kiểm: câu ck500 không đổi chấm lại (tệp score_cal_*_raw.jsonl) phải ra cùng tọa độ và exec với tệp thô cũ;
ck500 exec = 60,65; mọi bước câu khác ck500 phải có dòng chấm mới với đúng câu đó.

    python doc_exec_cw.py --exec-dir <thư mục chứa score_cal_*_raw.jsonl, score_cw_*_raw.jsonl> --pred pred_cw_t0.5_test.jsonl
    python doc_exec_cw.py --tu-kiem        # tái lập exec R3 = 60,68 từ tệp thô của lượt 304
"""
import argparse, glob, json, os, shutil, sys, tempfile

KHO = next(p for p in ("/mnt/d/Master/Thesis", "/Users/P836901/Documents/Self-learning/thesis/thesis-master")
           if os.path.isdir(p))
sys.path.insert(0, f"{KHO}/harness")
os.chdir(f"{KHO}/harness")
import luat_d3 as L
from luat_aitw_day_du import aitw_full
from d3_ktc import ktc, mcnemar
kh = L.kh


def doc(E, pred_path, ten="cw", out_json=None):
    CK = L.nap(f"{KHO}/runs/grpo_spice/score_ck500_test_raw.jsonl")
    S1 = L.nap(f"{KHO}/runs/score_s1_seed101_raw.jsonl")
    moi = lambda t: {kh(r): r for f in sorted(glob.glob(f"{E}/score_{t}_*_raw.jsonl")) for r in map(json.loads, open(f))}
    CAL, CW = moi("cal"), moi("cw")
    P = {kh(x): x["pred"] for x in map(json.loads, open(pred_path, encoding="utf-8"))}
    lech = [k for k in CAL if CAL[k].get("pred_xy") != CK[k].get("pred_xy") or CAL[k]["executable"] != CK[k]["executable"]]
    print(f"[hiệu chuẩn] {len(CAL)} câu ck500 chấm lại - lệch tọa độ/exec {len(lech)}", lech[:3])
    assert CAL and not lech, "⛔ dụng cụ lệch tệp thô ck500 - dừng"
    can = {k for k in P if P[k] != (CK[k].get("sent") or "")}
    thieu = sorted(can - set(CW))
    sai = [k for k in can & set(CW) if CW[k].get("sent") != P[k]]
    print(f"[{ten}] câu khác ck500 {len(can)} - có dòng chấm mới {len(can & set(CW))} - thiếu {len(thieu)} - câu lệch {len(sai)}")
    assert not thieu and not sai, (thieu[:3], sai[:3])
    R = {k: (CW[k] if k in can else CK[k]) for k in CK}
    with open(f"{E}/score_{ten}_gop_raw.jsonl", "w", encoding="utf-8") as f:
        for k in CK:
            f.write(json.dumps(R[k], ensure_ascii=False) + "\n")

    K = list(S1)
    assert set(K) == set(CK) == set(P) and len(K) == 4463
    for X in (CK, R, S1):
        for k in K:
            for c in ("executable", "action_ok", "toggle_ok", "hit_disk"):
                X[k].setdefault(c, 0)
    lu = lambda X: {k: dict(L.luat(X[k], k), aitwf=aitw_full(X[k], k)) for k in K}
    X = {"ck500": lu(CK), ten: lu(R), "S1/101": lu(S1)}
    cum = {k: S1[k].get("app") or f"ep{k[0]}" for k in K}
    TEN = {"vor": "exec", "d3": "D.3", "aitwf": "AitW"}
    out = {"ktc": {}, "so_sanh": {}, "cau_doi": len(can), "hieu_chuan": len(CAL)}
    for t in X:
        out["ktc"][t] = {}
        for c in TEN:
            p, lo, hi, _ = ktc(K, lambda k, cc: X[t][k][cc], c, cum)
            out["ktc"][t][c] = dict(diem=round(p, 2), lo=round(lo, 2), hi=round(hi, 2))
        print(f"{t:8s} " + " - ".join(f"{TEN[c]} {out['ktc'][t][c]['diem']:.2f} [{out['ktc'][t][c]['lo']:.2f}; {out['ktc'][t][c]['hi']:.2f}]" for c in TEN))
    assert abs(out["ktc"]["ck500"]["vor"]["diem"] - 60.65) < 0.01, "⛔ ck500 exec phải tái lập 60,65"
    for b in ("ck500", "S1/101"):
        for c in TEN:
            d, lo, hi, _ = ktc(K, lambda k, cc: X[ten][k][cc] - X[b][k][cc], c, cum)
            pha, cuu, _, p = mcnemar(K, X[b], X[ten], c)
            out["so_sanh"][f"{ten} - {b} - {TEN[c]}"] = dict(delta=round(d, 2), lo=round(lo, 2), hi=round(hi, 2), cuu=cuu, pha=pha, p=p)
            print(f"{ten} - {b:7s} {TEN[c]:5s} {d:+.2f} [{lo:+.2f}; {hi:+.2f}] - cứu {cuu} phá {pha} - p={p:.3g}")
    out_json = out_json or f"{E}/doc_exec_{ten}.json"
    json.dump(out, open(out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", out_json)
    return out


def tu_kiem():
    E0 = f"{KHO}/runs/ra304_G/exec_out/exec_out"
    pred = f"{KHO}/runs/ra304_luat/pred_R3_test.jsonl"
    T = tempfile.mkdtemp()
    for f in glob.glob(f"{E0}/score_cal_*_raw.jsonl"):
        shutil.copy(f, T)
    with open(f"{T}/score_cw_0_raw.jsonl", "w", encoding="utf-8") as fo:
        for f in sorted(glob.glob(f"{E0}/score_ghep_*_raw.jsonl")) + sorted(glob.glob(f"{E0}/score_ra_*_raw.jsonl")):
            fo.write(open(f, encoding="utf-8").read())
    o = doc(T, pred, "cw", out_json=f"{T}/x.json")
    assert abs(o["ktc"]["cw"]["vor"]["diem"] - 60.68) < 0.01 and abs(o["ktc"]["cw"]["d3"]["diem"] - 67.11) < 0.01 \
        and abs(o["ktc"]["cw"]["aitwf"]["diem"] - 76.32) < 0.01, o["ktc"]["cw"]
    print("[tự kiểm] ĐẠT - tái lập R3: exec 60,68 - D.3 67,11 - AitW 76,32 (khớp runs/ra304_luat/test_R3.json)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--exec-dir")
    ap.add_argument("--pred")
    ap.add_argument("--ten", default="cw")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    tu_kiem() if a.tu_kiem else doc(os.path.abspath(a.exec_dir), os.path.abspath(a.pred), a.ten)
