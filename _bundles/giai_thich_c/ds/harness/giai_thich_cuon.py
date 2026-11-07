# -*- coding: utf-8 -*-
"""Vì sao ck500 giảm đúng loại thao tác ở bước cuộn / quay lại (report/320 mục 15–16 đã loại hai giả thuyết) — CPU + Java.

Không sinh câu mới. Dùng câu đã có: S1/101 (runs/preds_s1_seed101.jsonl) và ck500 (runs/grpo_spice/pred_ck500_test_nontap.jsonl)
trên 2.495 bước không chạm test. Loại thao tác của câu = canon_action(strict_back=True), như phép kiểm noharm.
Đo:
  1. Theo loại vàng (scroll, navigate_back, open_app, input_text, wait): phân bố loại của câu S1 và ck500; hai từ đầu của câu sai loại.
  2. Ví dụ ở bước S1 đúng loại mà ck500 sai loại.
  3. Cơ chế giả thuyết [ghi trước khi đo]: ở bước cuộn, câu chuẩn hay nhắc tên phần tử đích ("Scroll down to find X"),
     nên câu dạng chạm "Click on X" lấy được tuple đối tượng còn câu "Scroll down" thì không; khi đó thưởng SPICE
     không phạt (thậm chí thưởng) việc đổi sang câu chạm. Kiểm bằng: ở các bước S1 đúng loại mà ck500 sai loại,
     SPICE(ck500) so với SPICE(S1); tỉ lệ ck500 ≥ S1; tách theo câu chuẩn có/không tuple đối tượng ngoài từ thao tác.
     Thêm: SPICE trung bình theo loại câu (chạm vs đúng loại) ở bước vàng cuộn, gộp hai nhánh; tỉ lệ câu đúng loại có SPICE = 0.
Số mô tả, hậu kiểm, một hạt giống.

  python giai_thich_cuon.py --out ../runs/giai_thich/c/giai_thich_cuon.json [--n 200]
"""
import os, sys, json, argparse, collections, ast

H = os.path.dirname(os.path.abspath(__file__))
K = os.path.join(H, "..")
sys.path.insert(0, H)
import metric_exec as M  # noqa: E402
from h4_spice_tuple import spice_chi_tiet  # noqa: E402

TAPT = ("click", "long_press")
TU_THAO_TAC = {"scroll", "swipe", "down", "up", "left", "right", "back", "go", "screen", "page", "open", "app", "wait",
               "type", "enter", "search", "navigate", "press", "button", "the", "a", "to", "on", "of", "for", "in"}


def act(r):
    a = r.get("action")
    return ast.literal_eval(a) if isinstance(a, str) else (a or {})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=0)
    a = ap.parse_args()
    R = [json.loads(l) for l in open(f"{K}/harness/dg1_cache/test_ac/test.jsonl", encoding="utf-8")]
    key = lambda r: (str(r["episode_id"]), str(r["step_id"]))
    loai = {key(r): act(r).get("action_type", "?") for r in R}
    cham = {key(r): act(r).get("action_type") in TAPT and "x" in act(r) for r in R}
    gold = {key(r): (r.get("gold_instruction") or "").strip() for r in R}
    S1 = {(str(d["episode_id"]), str(d["step_id"])): d.get("pred") or "" for d in map(json.loads, open(f"{K}/runs/preds_s1_seed101.jsonl", encoding="utf-8"))}
    CK = {(str(d["episode_id"]), str(d["step_id"])): d.get("pred") or "" for d in map(json.loads, open(f"{K}/runs/grpo_spice/pred_ck500_test_nontap.jsonl", encoding="utf-8"))}
    ks = [key(r) for r in R if not cham[key(r)]]
    assert len(ks) == 2495 and all(k in CK and k in S1 for k in ks), (len(ks), sum(k in CK for k in ks))
    if a.n:
        ks = ks[:a.n]
    can = lambda s: M.canon_action(s, strict_back=True) if s else "rong"
    cg = {k: can(gold[k]) for k in ks}
    cs = {k: can(S1[k]) for k in ks}
    cc = {k: can(CK[k]) for k in ks}
    out = {}

    # 1. phân bố loại câu theo loại vàng
    T = {}
    for lv in ("scroll", "navigate_back", "open_app", "input_text", "wait"):
        kk = [k for k in ks if loai[k] == lv]
        if not kk:
            continue
        o = dict(n=len(kk), loai_chuan_canon=dict(collections.Counter(cg[k] for k in kk).most_common(4)))
        for ten, P, C in (("s1", S1, cs), ("ck500", CK, cc)):
            o[f"{ten}_dung"] = round(sum(C[k] == cg[k] for k in kk) / len(kk), 4)
            o[f"{ten}_loai"] = dict(collections.Counter(C[k] for k in kk).most_common(5))
            sai = [k for k in kk if C[k] != cg[k]]
            o[f"{ten}_sai_2tu"] = collections.Counter(" ".join(P[k].lower().split()[:2]) for k in sai).most_common(8)
        o["s1_dung_ck_sai"] = sum(cs[k] == cg[k] and cc[k] != cg[k] for k in kk)
        o["s1_sai_ck_dung"] = sum(cs[k] != cg[k] and cc[k] == cg[k] for k in kk)
        T[lv] = o
        print(lv, json.dumps(o, ensure_ascii=False), flush=True)
    out["phan_bo"] = T

    # 2. ví dụ
    vd = [k for k in ks if loai[k] in ("scroll", "navigate_back") and cs[k] == cg[k] and cc[k] != cg[k]]
    out["vi_du"] = [dict(buoc=k, loai=loai[k], chuan=gold[k], s1=S1[k], ck500=CK[k]) for k in vd[:15]]

    # 3. SPICE
    G = [gold[k] for k in ks]
    SG = spice_chi_tiet(G, G, "chuan_nt")
    SS = spice_chi_tiet([S1[k] for k in ks], G, "s1_nt")
    SC = spice_chi_tiet([CK[k] for k in ks], G, "ck500_nt")
    i_of = {k: i for i, k in enumerate(ks)}
    f = lambda S, k: S[i_of[k]]["scores"]["All"]["f"]
    def co_doi_tuong(k):
        return any(t.count(" | ") == 0 and t not in TU_THAO_TAC for t in SG[i_of[k]]["ref"])
    C3 = {}
    for lv in ("scroll", "navigate_back"):
        kk = [k for k in ks if loai[k] == lv]
        d = [k for k in kk if cs[k] == cg[k] and cc[k] != cg[k]]
        o = dict(n_buoc=len(kk), ti_le_chuan_co_doi_tuong=round(sum(map(co_doi_tuong, kk)) / max(1, len(kk)), 4),
                 n_s1_dung_ck_sai=len(d))
        if d:
            o["spice_s1_tb"] = round(sum(f(SS, k) for k in d) / len(d), 4)
            o["spice_ck_tb"] = round(sum(f(SC, k) for k in d) / len(d), 4)
            o["ti_le_ck_ge_s1"] = round(sum(f(SC, k) >= f(SS, k) for k in d) / len(d), 4)
            o["ti_le_ck_gt_s1"] = round(sum(f(SC, k) > f(SS, k) for k in d) / len(d), 4)
            for nh, dk in (("chuan_co_doi_tuong", True), ("chuan_khong_doi_tuong", False)):
                dd = [k for k in d if co_doi_tuong(k) == dk]
                if dd:
                    o[nh] = dict(n=len(dd), s1=round(sum(f(SS, k) for k in dd) / len(dd), 4),
                                 ck=round(sum(f(SC, k) for k in dd) / len(dd), 4),
                                 ck_ge_s1=round(sum(f(SC, k) >= f(SS, k) for k in dd) / len(dd), 4))
        # SPICE theo loại câu, gộp hai nhánh
        theo = collections.defaultdict(list)
        for S, C in ((SS, cs), (SC, cc)):
            for k in kk:
                nhom = "dung_loai" if C[k] == cg[k] else ("cau_cham" if C[k] == "tap" else "sai_khac")
                theo[nhom].append(f(S, k))
                if C[k] == cg[k]:
                    theo["dung_loai_bang_0"].append(f(S, k) == 0)
        o["spice_theo_loai_cau_gop"] = {g: (round(sum(v) / len(v), 4), len(v)) for g, v in theo.items()}
        for g in ("dung_loai", "cau_cham"):
            for dk in (True, False):
                v = [f(S, k) for S, C in ((SS, cs), (SC, cc)) for k in kk
                     if co_doi_tuong(k) == dk and ((C[k] == cg[k]) if g == "dung_loai" else (C[k] == "tap"))]
                o[f"spice_{g}_{'co' if dk else 'khong'}_doi_tuong"] = (round(sum(v) / max(1, len(v)), 4), len(v))
        C3[lv] = o
        print(lv, json.dumps(o, ensure_ascii=False), flush=True)
    out["spice_co_che"] = C3
    out["n_chay_thu"] = a.n
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=1)
    print("[xong] ghi", a.out, flush=True)


if __name__ == "__main__":
    main()
