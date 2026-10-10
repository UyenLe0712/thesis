# -*- coding: utf-8 -*-
"""304 — chọn luật ghép trên val rồi áp lên test MỘT lần (0 GPU). Luật + tiêu chí khoá ở luat_ghep_304.py.

    python3 doc_luat_304.py val  <thư mục val_out của Kaggle ra-val-luat-304>   # chọn luật → runs/ra304_luat/luat_chon.json
    python3 doc_luat_304.py test                                               # áp luật đã chọn lên test (chạy MỘT lần)
"""
import json, os, sys

KHO = "/mnt/d/Master/Thesis"
sys.path.insert(0, f"{KHO}/harness")
OUT = f"{KHO}/runs/ra304_luat"
CHON = f"{OUT}/luat_chon.json"
UNG = ("R0", "R2", "R3", "R4")      # R1 loại (lấy 0 bước)
THUOC = ("bleu4", "meteor", "rougeL", "cider_d", "chrf")
nap = lambda p: [json.loads(l) for l in open(p, encoding="utf-8")]
kk = lambda d: (str(d["episode_id"]), str(d["step_id"]))


def val(E):
    os.chdir(f"{KHO}/harness")
    from d3_ktc import ktc, mcnemar
    CK = {kk(d): d for d in nap(f"{KHO}/runs/vallon289/score_ck500_vallon_raw.jsonl")}
    RA = {kk(d): d for d in nap(f"{E}/score_ra_k4_vallon_raw.jsonl")}
    CAL = nap(f"{E}/score_cal_vallon_raw.jsonl")
    lech = [kk(d) for d in CAL if d.get("pred_xy") != CK[kk(d)].get("pred_xy") or d["executable"] != CK[kk(d)]["executable"]]
    print(f"[hiệu chuẩn val] {len(CAL)} câu ck500 chấm lại · lệch {len(lech)}")
    assert len(CAL) == 20 and not lech
    assert set(RA) == set(CK) and len(CK) == 1002
    pra = {kk(d): d["pred"] for d in nap(f"{KHO}/runs/ra304_T/pred_val_ra_k4.jsonl")}
    assert all(RA[k]["sent"] == pra[k] for k in RA), "tệp thô ra_k4 val lệch câu"
    T = json.load(open(f"{OUT}/diem_val_luat.json"))
    T = T["diem"]
    K = sorted(CK); cum = {k: f"ep{k[0]}" for k in K}
    X = {"ck500": {k: {"vor": int(CK[k]["executable"] or 0)} for k in K}}
    kq = {}
    for L in UNG:
        P = {kk(d): d["pred"] for d in nap(f"{OUT}/pred_{L}_val.jsonl")}
        R = {}
        for k in K:
            if P[k] == CK[k].get("sent"):
                R[k] = CK[k]
            else:
                assert P[k] == RA[k]["sent"], (L, k)
                R[k] = RA[k]
        X[L] = {k: {"vor": int(R[k]["executable"] or 0)} for k in K}
        e = 100 * sum(X[L][k]["vor"] for k in K) / len(K)
        d, lo, hi, _ = ktc(K, lambda k, c: X[L][k][c] - X["ck500"][k][c], "vor", cum)
        pha, cuu, _, p = mcnemar(K, X["ck500"], X[L], "vor")
        hon = sum(T[L][t] > T["ck500"][t] for t in THUOC)
        doi = sum(P[k] != CK[k].get("sent") for k in K)
        kq[L] = dict(exec=round(e, 2), delta=round(d, 2), lo=round(lo, 2), hi=round(hi, 2), cuu=cuu, pha=pha, p=p, chu_hon=hon, doi_cau=doi)
        print(f"{L}: exec {e:.2f} · Δ {d:+.2f} [{lo:+.2f}; {hi:+.2f}] · cứu {cuu} phá {pha} · p={p:.3g} · chữ hơn ck500 {hon}/5 · đổi {doi} câu")
    e0 = 100 * sum(X["ck500"][k]["vor"] for k in K) / len(K)
    print(f"ck500 val exec {e0:.2f}")
    du = [L for L in UNG if kq[L]["chu_hon"] >= 4]
    chon = max(du, key=lambda L: (kq[L]["exec"], -kq[L]["doi_cau"])) if du else "R0"
    print(f"→ CHỌN {chon} (tiêu chí khoá trước: ≥ 4/5 thước chữ hơn ck500, exec val cao nhất, hoà thì đổi ít câu hơn)")
    assert not os.path.exists(CHON), "đã chọn rồi — không chọn lại"
    json.dump(dict(chon=chon, val=kq, ck500_val_exec=round(e0, 2)), open(CHON, "w"), ensure_ascii=False, indent=1)


def test():
    os.chdir(f"{KHO}/harness")
    import luat_d3 as LD
    from luat_aitw_day_du import aitw_full
    from d3_ktc import ktc, mcnemar
    chon = json.load(open(CHON))["chon"]
    ra_out = f"{OUT}/test_{chon}.json"
    assert not os.path.exists(ra_out), "đã áp lên test rồi — chỉ một lần"
    CK = LD.nap(f"{KHO}/runs/grpo_spice/score_ck500_test_raw.jsonl")
    S1 = LD.nap(f"{KHO}/runs/score_s1_seed101_raw.jsonl")
    RA = LD.nap(f"{KHO}/runs/ra304_G/exec_out/exec_out/score_ra_k4_gop_raw.jsonl")
    K = list(S1); assert set(K) == set(CK) == set(RA) and len(K) == 4463
    def ghep(L):
        P = {LD.kh(d): d["pred"] for d in nap(f"{OUT}/pred_{L}_test.jsonl")}
        R = {}
        for k in K:
            if P[k] == (CK[k].get("sent") or ""):
                R[k] = CK[k]
            else:
                assert P[k] == RA[k]["sent"], (L, k); R[k] = RA[k]
        return R, sum(P[k] != (CK[k].get("sent") or "") for k in K)
    Rc, doi = ghep(chon); R0, _ = ghep("R0")
    with open(f"{OUT}/score_{chon}_test_raw.jsonl", "w", encoding="utf-8") as f:
        for k in K: f.write(json.dumps(Rc[k], ensure_ascii=False) + "\n")
    for R in (CK, S1, Rc, R0):
        for k in K:
            for c in ("executable", "action_ok", "toggle_ok", "hit_disk"): R[k].setdefault(c, 0)
    lu = lambda R: {k: dict(LD.luat(R[k], k), aitwf=aitw_full(R[k], k)) for k in K}
    X = {"ck500": lu(CK), chon: lu(Rc), "R0 (ghep cũ)": lu(R0), "S1/101": lu(S1)}
    cum = {k: S1[k].get("app") or f"ep{k[0]}" for k in K}
    TEN = {"vor": "exec", "d3": "D.3", "aitwf": "AitW"}
    out = dict(luat=chon, doi_cau=doi, ktc={}, so_sanh={})
    print(f"[test] luật {chon} · đổi {doi} câu so ck500")
    for t in X:
        out["ktc"][t] = {}
        for c in TEN:
            p, lo, hi, _ = ktc(K, lambda k, cc: X[t][k][cc], c, cum)
            out["ktc"][t][c] = dict(diem=round(p, 2), lo=round(lo, 2), hi=round(hi, 2))
        print(f"{t:13s} " + " · ".join(f"{TEN[c]} {out['ktc'][t][c]['diem']:.2f} [{out['ktc'][t][c]['lo']:.2f}; {out['ktc'][t][c]['hi']:.2f}]" for c in TEN))
    assert abs(out["ktc"]["ck500"]["vor"]["diem"] - 60.65) < 0.01 and abs(out["ktc"]["R0 (ghep cũ)"]["vor"]["diem"] - 60.54) < 0.01
    for b in ("ck500", "S1/101", "R0 (ghep cũ)"):
        if b == chon or (chon == "R0" and b.startswith("R0")): continue
        for c in TEN:
            d, lo, hi, _ = ktc(K, lambda k, cc: X[chon][k][cc] - X[b][k][cc], c, cum)
            pha, cuu, _, p = mcnemar(K, X[b], X[chon], c)
            out["so_sanh"][f"{chon} − {b} · {TEN[c]}"] = dict(delta=round(d, 2), lo=round(lo, 2), hi=round(hi, 2), cuu=cuu, pha=pha, p=p)
            print(f"{chon} − {b:13s} {TEN[c]:5s} {d:+.2f} [{lo:+.2f}; {hi:+.2f}] · cứu {cuu} phá {pha} · p={p:.3g}")
    json.dump(out, open(ra_out, "w"), ensure_ascii=False, indent=1)
    print("→", ra_out)


if __name__ == "__main__":
    if sys.argv[1] == "val":
        val(os.path.abspath(sys.argv[2]))
    else:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        test()
