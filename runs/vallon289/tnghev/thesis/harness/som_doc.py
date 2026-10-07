# -*- coding: utf-8 -*-
"""Đọc kết quả người nghe trắc nghiệm — chạy CPU, 0 GPU.

    python3 harness/som_doc.py runs/som/chon_<backend>_<nhánh>.jsonl [...]
    python3 harness/som_doc.py --thu-muc runs/som            # đọc mọi tệp chon_*.jsonl

In cho mỗi tệp: số bước, độ chính xác chọn đúng phần tử (comprehension accuracy) và bản có điều kiện
đúng loại thao tác, KTC95 bằng CHÍNH `score_run.cluster_bootstrap` (cụm = app, G = 1.091 khi đủ 4.463 bước).
Rồi so ghép cặp McNemar giữa các nhánh CÙNG backend trên phần bước chung. Ghi runs/som/som_ket_qua.json.

Luật chọn backend (khoá 14/9 trước khi có điểm): trên lát thử 200 bước cố định, backend nào đạt độ chính
xác cao hơn với CÂU CHUẨN thì dùng cho mọi nhánh. Không dùng điểm của nhánh mô hình để chọn.
"""
import argparse, glob, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score_run as S

RUNS = os.path.join(HERE, "..", "runs")
APP = {(str(o["episode_id"]), str(o["step_id"])): (o.get("app") or f"ep{o['episode_id']}")
       for o in map(json.loads, open(os.path.join(RUNS, "score_s1_seed101_raw.jsonl"), encoding="utf-8"))}


def nap(p):
    d = {}
    for l in open(p, encoding="utf-8"):
        o = json.loads(l); d[(o["episode_id"], o["step_id"])] = o
    return d


def ktc(D, cot):
    U = list(D.items())
    pt, (lo, hi), G, _ = S.cluster_bootstrap(U, lambda u: APP[u[0]], lambda u: u[1][cot])
    return 100 * pt, 100 * lo, 100 * hi, G


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tep", nargs="*")
    ap.add_argument("--thu-muc", default="")
    a = ap.parse_args()
    teps = a.tep or sorted(glob.glob(os.path.join(a.thu_muc or os.path.join(RUNS, "som"), "chon_*.jsonl")))
    out = {"ket_qua": {}, "so_sanh": {}}
    X = {}
    print(f"{'tệp':34s} {'n':>5s} {'chọn đúng':>9s} {'KTC95':>16s} {'∧ thao tác':>10s} {'không ra số':>11s}")
    for p in teps:
        ten = os.path.basename(p)[5:-6]            # chon_<backend>_<nhánh>.jsonl
        D = nap(p); X[ten] = D
        e, lo, hi, G = ktc(D, "dung")
        g = 100 * sum(o["dung_thaotac"] for o in D.values()) / len(D)
        ns = sum(1 for o in D.values() if o["chon"] is None and o["raw"])
        out["ket_qua"][ten] = dict(n=len(D), dung=round(e, 2), lo=round(lo, 2), hi=round(hi, 2), G=G,
                                   dung_thaotac=round(g, 2), khong_ra_so=ns)
        print(f"{ten:34s} {len(D):5d} {e:9.2f} [{lo:6.2f}; {hi:6.2f}] {g:10.2f} {ns:11d}")

    print("\nSo ghép cặp (cùng backend, phần bước chung), cột 'chọn đúng':")
    ds = sorted(X)
    for i, a_ in enumerate(ds):
        for b_ in ds[i + 1:]:
            if a_.split("_")[0] != b_.split("_")[0]:
                continue
            K = sorted(set(X[a_]) & set(X[b_]))
            if len(K) < 50:
                continue
            b = sum(1 for k in K if X[b_][k]["dung"] and not X[a_][k]["dung"])
            c = sum(1 for k in K if X[a_][k]["dung"] and not X[b_][k]["dung"])
            chi = (abs(b - c) - 1) ** 2 / (b + c) if b + c else 0.0
            p = math.erfc(math.sqrt(chi / 2)) if b + c else 1.0
            d = 100 * (c - b) / len(K)
            out["so_sanh"][f"{a_} − {b_}"] = dict(n=len(K), delta=round(d, 2), b=b, c=c, p=p)
            print(f"  {a_:28s} − {b_:28s} n={len(K):5d} Δ={d:+6.2f} b={b} c={c} p={p:.2e}")
    os.makedirs(os.path.join(RUNS, "som"), exist_ok=True)
    q = os.path.join(RUNS, "som", "som_ket_qua.json")
    json.dump(out, open(q, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", os.path.relpath(q))


if __name__ == "__main__":
    main()
