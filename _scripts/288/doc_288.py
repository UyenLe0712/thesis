# -*- coding: utf-8 -*-
"""[cách A — dự phòng, KHÔNG dùng cho bản 4] Đọc kết quả TEST của 288 và xếp kết cục K1–K4 (B.8 của 288).

    python ../_scripts/288/doc_288.py --recs harness/dg1_cache/test_ac/test.jsonl --chinh nghev101 \
        --nhanh S1:<raw>:<nontap> --nhanh ck500:<raw>:<nontap> --nhanh nghev101:<raw>:<nontap> \
        [--venus ck500:<raw> --venus nghev101:<raw>] --out runs/goc288/doc_288_dot1.json

Tên nhánh: S1, ck500, hoặc <nghev|nghe|nghern|spicea><hạt>; nhánh chính là nghev101 (G0 giữ cổng v) hoặc nghe101.
Luật ở §6.2 và §11 (chưa đăng ký — muốn chạy cách A phải đăng ký riêng trước khi train).
Viết lại 6/10/2026 từ bản mô tả B.8 (mã gốc ở máy Mac) ⇒ md5 khác bản gốc; chưa chạy khô 7 tình huống như bản gốc.
"""
import argparse, json, os, re, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import doc_286 as L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recs", required=True)
    ap.add_argument("--nhanh", action="append", default=[])
    ap.add_argument("--venus", action="append", default=[])
    ap.add_argument("--chinh", required=True)
    ap.add_argument("--gia", action="store_true")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    recs = L.doc_jsonl(a.recs)
    assert len(recs) == 6958, f"DỪNG: test.jsonl có {len(recs)} dòng, cần 6.958"
    for r in recs:
        r["_tap"] = L.la_cham(r)
    EP = {(r["episode_id"], r["step_id"]): r["episode_id"] for r in recs}
    N = {}
    for x in a.nhanh:
        ten, raw, nontap = x.split(":", 2)
        N[ten] = L.nap(recs, raw, nontap)
    m = re.fullmatch(r"(nghev|nghe)(\d+)", a.chinh)
    assert m and m.group(2) == "101", "nhánh chính phải là nghev101 hoặc nghe101"
    for t in ("S1", "ck500", a.chinh):
        assert t in N, f"DỪNG: thiếu --nhanh {t}"
    A_, arm = a.chinh, m.group(1)
    B1 = "nghe101"
    VV = {x.split(":", 1)[0]: {(o["episode_id"], o["step_id"]): int(o.get("executable") or 0)
                               for o in L.doc_jsonl(x.split(":", 1)[1])} for x in a.venus}

    ck = sorted(set.intersection(*[set(v[0]) for v in N.values()]))
    ntk = sorted(N["S1"][1])
    gop = lambda t: {**{k: N[t][0][k] for k in ck}, **{k: N[t][1][k][0] for k in ntk}}

    def ss(x, y, loai="exec"):
        rng = np.random.default_rng(L.SEED)
        if loai == "exec":
            return L.so(N[x][0], N[y][0], ck, EP, rng)
        if loai == "nt":
            return L.so({k: N[x][1][k][0] for k in ntk}, {k: N[y][1][k][0] for k in ntk}, ntk, EP, rng)
        return L.so(gop(x), gop(y), ck + ntk, EP, rng)

    def venus(x, y):
        k = sorted(VV[x].keys() & VV[y].keys())
        return L.so(VV[x], VV[y], k, EP, np.random.default_rng(L.SEED))

    P = {}
    P[f"{A_}-ck500"], P[f"{A_}-S1"] = ss(A_, "ck500"), ss(A_, "S1")
    if "spicea101" in N:
        P[f"{A_}-spicea101"], P["spicea101-ck500"] = ss(A_, "spicea101"), ss("spicea101", "ck500")
    if A_ != B1 and B1 in N:
        P[f"{A_}-{B1}"] = ss(A_, B1)
    if "nghern101" in N:
        P[f"{A_}-nghern101"] = ss(A_, "nghern101")
    for t in ("nghev202", "nghe202"):
        if t in N:
            P[f"{t}-ck500"] = ss(t, "ck500")
    if "nghev202" in N and "nghe202" in N:
        P["nghev202-nghe202"] = ss("nghev202", "nghe202")
    if A_ in VV and "ck500" in VV:
        P[f"UI-Venus {A_}-ck500"] = venus(A_, "ck500")
    for y in ("S1", "ck500"):
        P[f"[mô tả] {A_}-{y} không chạm"] = ss(A_, y, "nt")
        P[f"[mô tả] {A_}-{y} gộp"] = ss(A_, y, "gop")

    A202 = f"{arm}202"
    tang = P[f"{A_}-ck500"]["d"] > 0
    dot2 = [t for t in ["spicea101"] + ([B1] if arm == "nghev" else []) + [A202] if t not in N]
    if not (A_ in VV and "ck500" in VV):
        dot2.append("UI-Venus ck500 + A")
    dk = {"LB(A−ck500)>0": P[f"{A_}-ck500"]["lo"] > 0, "LB(A−S1)>0": P[f"{A_}-S1"]["lo"] > 0,
          "ΔUIVenus(A−ck500)>0": f"UI-Venus {A_}-ck500" in P and P[f"UI-Venus {A_}-ck500"]["d"] > 0}
    if "spicea101" in N:
        dk["Δ(A−spicea101)>0"] = P[f"{A_}-spicea101"]["d"] > 0
    if f"{A202}-ck500" in P:
        dk["Δ(A202−ck500)>0"] = P[f"{A202}-ck500"]["d"] > 0
    vuot = all(dk.values())
    if not tang:
        kc, luat = "K1", "DỪNG"
    elif dot2:
        kc, luat = "CHỜ-ĐỢT-2", "CHẠY ĐỢT 2: " + ", ".join(dot2)
    elif not vuot:
        kc = "K2" if P[f"{A_}-ck500"]["lo"] <= 0 else "K2+ (thiếu: " + ", ".join(k for k, v in dk.items() if not v) + ")"
        luat = ""
    else:
        kc, luat = "K3", ""
        if arm == "nghev":
            v = {"LB(A−B1)>0": P.get(f"{A_}-{B1}", {}).get("lo", -1) > 0}
            if "nghern101" in N:
                v["Δ(A−nghern101)>0"] = P[f"{A_}-nghern101"]["d"] > 0
            if "nghev202-nghe202" in P:
                v["Δ(nghev202−nghe202)>0"] = P["nghev202-nghe202"]["d"] > 0
            thieu = [t for t in ["nghe202"] + (["nghern101"] if P.get(f"{A_}-{B1}", {}).get("d", 0) >= 0.5 else []) if t not in N]
            if v["LB(A−B1)>0"] and thieu:
                kc, luat = "K3 · K4-CHỜ-ĐỢT-3", "CHẠY ĐỢT 3: " + ", ".join(thieu)
            elif all(v.values()) and not thieu:
                kc = "K4"
            dk.update(v)

    nhan = "[GIẢ] " if a.gia else ""
    for k, r in P.items():
        print(nhan + L.fmt(r, k))
    print(nhan + "điều kiện: " + " · ".join(f"{k} {'✓' if v else '✗'}" for k, v in dk.items()))
    print(f"{nhan}⇒ KẾT CỤC {kc}" + (f" · luật: {luat}" if luat else ""))
    json.dump({"ket_cuc": kc, "luat": luat, "dieu_kien": dk, "so": P, "gia": a.gia},
              open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("ghi", a.out)


if __name__ == "__main__":
    main()
