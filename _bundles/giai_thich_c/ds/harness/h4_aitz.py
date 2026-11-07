# -*- coding: utf-8 -*-
"""Kiểm giả thuyết report/320 mục 15: tuple SPICE của câu chuẩn AitZ chủ yếu đến từ phần khuôn (tuple phổ biến),
nên SPICE ít phân biệt câu trên AitZ — CPU + Java.

Dùng tệp raw đã chấm trên 2.736 bước chạm AitZ: S1/101 và ck500 (runs/aitz/gen_25_10/v2/z/out/score_*_aitz_raw.jsonl).
Đo:
  1. Tuple câu chuẩn: số tuple/câu theo loại; tuple "phổ biến" = xuất hiện ở ≥1% câu; tỉ lệ lần xuất hiện thuộc tuple phổ biến;
     top tuple. (Số đối chiếu của AndroidControl nằm trong h4_spice_tuple.json, cùng định nghĩa.)
  2. ck500 so S1 trên AitZ: Δtp theo Object/Attribute/Relation và theo phổ biến/hiếm, ΔF; đối chiếu Δexec.
Số mô tả, hậu kiểm, một hạt giống.

  python h4_aitz.py --out ../runs/giai_thich/c/h4_aitz.json [--n 200]
"""
import os, sys, json, argparse, collections

H = os.path.dirname(os.path.abspath(__file__))
K = os.path.join(H, "..")
sys.path.insert(0, H)
from h4_spice_tuple import spice_chi_tiet, gop, boot, nap_raw, LOAI, loai_tuple  # noqa: E402

D = "runs/aitz/gen_25_10/v2/z/out"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=0)
    a = ap.parse_args()
    RAW = {t: nap_raw(f"{K}/{D}/score_{t}_aitz_raw.jsonl") for t in ("s1", "ck500")}
    ks = sorted(RAW["s1"])
    assert len(ks) == 2736 and set(RAW["ck500"]) == set(ks), (len(ks), len(RAW["ck500"]))
    if a.n:
        ks = ks[:a.n]
    G = [RAW["s1"][k]["gold_instruction"] for k in ks]
    assert [RAW["ck500"][k]["gold_instruction"] for k in ks] == G
    ep = [k[0] for k in ks]
    SG = spice_chi_tiet(G, G, "chuan_aitz")
    df = collections.Counter(t for s in SG for t in set(s["ref"]))
    nguong = max(2, int(0.01 * len(ks)))
    pb = {t for t, c in df.items() if c >= nguong}
    occ = [t for s in SG for t in s["ref"]]
    theo_loai = collections.Counter(loai_tuple(t) for t in occ)
    pb_loai = collections.Counter(loai_tuple(t) for t in occ if t in pb)
    out = dict(n=len(ks), nguong_pho_bien=nguong, n_tuple_khac=len(df), n_pho_bien=len(pb),
               tuple_moi_cau=round(len(occ) / len(ks), 3),
               ti_le_lan_xuat_hien_pho_bien=round(sum(t in pb for t in occ) / max(1, len(occ)), 4),
               ti_le_pho_bien_theo_loai={c: round(pb_loai[c] / max(1, theo_loai[c]), 4) for c in LOAI},
               top15_tuple=df.most_common(15))
    print(json.dumps(out, ensure_ascii=False), flush=True)
    S = {t: spice_chi_tiet([RAW[t][k]["sent"] or "" for k in ks], G, f"{t}_aitz") for t in RAW}
    out["gop"] = {t: gop(s) for t, s in S.items()}
    s1, ck = S["s1"], S["ck500"]
    dd = {"dtp_All": out["gop"]["ck500"]["All"]["tp"] - out["gop"]["s1"]["All"]["tp"]}
    for c in LOAI:
        dd[f"dtp_{c}"] = out["gop"]["ck500"][c]["tp"] - out["gop"]["s1"][c]["tp"]
        dd[f"dR_{c}"] = round(out["gop"]["ck500"][c]["R"] - out["gop"]["s1"][c]["R"], 4)
    tpn = lambda s, nh: sum(1 for x in s for tt, ok in x["test"] if ok and ((tt in pb) == (nh == "pho_bien")))
    for nh in ("pho_bien", "hiem"):
        dd[f"dtp_{nh}"] = tpn(ck, nh) - tpn(s1, nh)
        dd[f"tp_{nh}_s1"] = tpn(s1, nh)
    dd["dF_All_ktc"] = boot(ep, lambda idx: gop(ck, idx)["All"]["F"] - gop(s1, idx)["All"]["F"], B=300)
    dd["exec_s1"] = round(sum(RAW["s1"][k]["executable"] for k in ks) / len(ks), 4)
    dd["exec_ck500"] = round(sum(RAW["ck500"][k]["executable"] for k in ks) / len(ks), 4)
    # độ phân biệt: tương quan giữa SPICE câu và exec trong từng nhánh (câu có SPICE cao có hay trúng hơn không)
    for t, s in (("s1", s1), ("ck500", ck)):
        tr = [s[i]["scores"]["All"]["f"] for i, k in enumerate(ks) if RAW[t][k]["executable"] == 1]
        tt = [s[i]["scores"]["All"]["f"] for i, k in enumerate(ks) if RAW[t][k]["executable"] == 0]
        dd[f"spice_trung_tru_truot_{t}"] = round(sum(tr) / max(1, len(tr)) - sum(tt) / max(1, len(tt)), 4)
    out["ck500_so_s1"] = dd
    print(json.dumps(dd, ensure_ascii=False), flush=True)
    out["n_chay_thu"] = a.n
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=1)
    print("[xong] ghi", a.out, flush=True)


if __name__ == "__main__":
    main()
