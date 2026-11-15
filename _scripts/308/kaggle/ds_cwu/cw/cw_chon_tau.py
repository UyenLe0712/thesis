# -*- coding: utf-8 -*-
"""308 - chốt τ của CW-RA trên val lớn (CPU). Chạy MỘT lần; tệp chốt đã có thì từ chối chọn lại.

Đọc JSON của ra_score.py chấm val (nhánh ck500 + mọi cw_t{τ}). Luật:
  1. τ có nhiều thước chữ val cao hơn ck500 nhất (BLEU-4, METEOR, ROUGE-L, CIDEr-D, chrF);
  2. hoà thì CIDEr-D val cao hơn; 3. vẫn hoà thì τ lớn hơn (chép ít hơn).
τ = 1.01 (không chép) được tính như mọi τ khác.

python cw_chon_tau.py --diem diem_val_cw.json --out tau_chon.json
python cw_chon_tau.py --tu-kiem
"""
import os, json, argparse

THUOC = ("bleu4", "meteor", "rougeL", "cider_d", "chrf")


def chon(D):
    ck = D["ck500"]
    ung = []
    for ten, d in D.items():
        if not ten.startswith("cw_t"):
            continue
        tau = float(ten[4:])
        hon = sum(d[m] > ck[m] for m in THUOC)
        ung.append((hon, d["cider_d"], tau, ten))
    ung.sort(reverse=True)
    hon, cid, tau, ten = ung[0]
    return dict(tau=tau, nhanh=ten, hon_val=hon, cider_val=cid,
                bang=[dict(nhanh=u[3], hon=u[0], cider_d=u[1]) for u in ung])


def tu_kiem():
    D = {"ck500": dict(bleu4=54.8, meteor=39.2, rougeL=70.5, cider_d=449.0, chrf=64.5),
         "cw_t0.5": dict(bleu4=55.0, meteor=39.3, rougeL=70.6, cider_d=455.0, chrf=64.4),
         "cw_t0.7": dict(bleu4=55.1, meteor=39.3, rougeL=70.7, cider_d=452.0, chrf=64.6),
         "cw_t1.01": dict(bleu4=54.7, meteor=39.2, rougeL=70.5, cider_d=448.0, chrf=64.5)}
    c = chon(D)
    assert c["tau"] == 0.7 and c["hon_val"] == 5, c
    print("[tự kiểm] ĐẠT")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diem")
    ap.add_argument("--out")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        return tu_kiem()
    assert not os.path.exists(a.out), "⛔ τ đã chốt — không chọn lại"
    D = json.load(open(a.diem))["diem"]
    c = chon(D)
    json.dump(c, open(a.out, "w"), ensure_ascii=False, indent=1)
    for b in c["bang"]:
        print(f"{b['nhanh']:10s} hơn ck500 {b['hon']}/5 · CIDEr-D {b['cider_d']:.2f}")
    print(f"→ CHỐT τ = {c['tau']} ({c['nhanh']}) → {a.out}")


if __name__ == "__main__":
    main()
