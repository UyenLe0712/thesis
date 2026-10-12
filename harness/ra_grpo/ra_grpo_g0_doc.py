# -*- coding: utf-8 -*-
"""311 — đọc cổng G0 (CPU; SPICE cần Java 8 + pycocoevalcap như lúc chấm ck500).

Đọc 8 mẫu của S1 có khối và không khối trên cùng bước val, đo:
- trần best-of-8 (lấy mẫu tốt nhất theo câu chuẩn) cho SPICE, CIDEr-D (công thức pycocoevalcap, df trên câu chuẩn val)
- tỉ lệ bước có ít nhất một mẫu trùng nguyên văn câu chuẩn
- trong các bước khối chứa câu chuẩn: tỉ lệ có mẫu chép đúng câu đó
Rồi áp luật cổng (in ra, không tự chạy gì thêm).

python ra_grpo_g0_doc.py --recs B/p1_val_rows.jsonl --ra ex_val_k4.jsonl --mau-ra g0_mau_ra.jsonl --mau-khong g0_mau_khong.jsonl \
  --diem-greedy diem_g0_greedy.json --out g0_ket_qua.json
python ra_grpo_g0_doc.py --tu-kiem --no-spice
"""
import os, re, sys, json, math, argparse
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, "/kaggle/working/ra", os.path.join(HERE, "..", "..", "thesis-master", "_scripts", "304", "ra-sft-script"),
          os.path.join(HERE, "..", "..", "_scripts", "304", "ra-sft-script")):
    if os.path.isdir(p):
        sys.path.insert(0, p)

PUNCT = {"''", '"', "``", "-lrb-", "-rrb-", "-lcb-", "-rcb-", ".", "?", "!", ",", ":", "-", "--", "...", ";", "'"}
TOK = re.compile(r"n't|'s|'re|'ve|'ll|'d|'m|[a-z0-9]+(?:[-./][a-z0-9]+)*|[^\sa-z0-9]")


def tok(s):
    s = (s or "").lower().replace("“", '"').replace("”", '"').replace("’", "'")
    s = re.sub(r"(\w)n't\b", r"\1 n't", s)
    return [t for t in TOK.findall(s) if t not in PUNCT and t != ""]


def ngrams(ws, n=4):
    c = defaultdict(int)
    for k in range(1, n + 1):
        for i in range(len(ws) - k + 1):
            c[tuple(ws[i:i + k])] += 1
    return c


class CiderD:
    def __init__(self, refs, n=4, sigma=6.0):
        self.n, self.sigma, self.df = n, sigma, defaultdict(float)
        for r in refs:
            for ng in set(ngrams(tok(r), n)):
                self.df[ng] += 1
        self.log_n = math.log(float(len(refs)))

    def _vec(self, s):
        cnts = ngrams(tok(s), self.n)
        vec, norm, length = [dict() for _ in range(self.n)], [0.0] * self.n, 0
        for ng, tf in cnts.items():
            k = len(ng) - 1
            w = float(tf) * (self.log_n - math.log(max(1.0, self.df.get(ng, 0.0))))
            vec[k][ng] = w
            norm[k] += w * w
            if k == 1:
                length += tf
        return vec, [math.sqrt(x) for x in norm], length

    def score(self, cand, ref):
        vh, nh, lh = self._vec(cand)
        vr, nr, lr = self._vec(ref)
        pen = math.exp(-((lh - lr) ** 2) / (2 * self.sigma ** 2))
        tot = 0.0
        for k in range(self.n):
            v = sum(min(w, vr[k].get(ng, 0.0)) * vr[k].get(ng, 0.0) for ng, w in vh[k].items())
            if nh[k] != 0 and nr[k] != 0:
                v /= nh[k] * nr[k]
            tot += v * pen
        return 10.0 * tot / self.n


def spice_mot_luot(cands, refs):
    import grpo_spice as GS
    return GS.spice_batch([c if c else "none" for c in cands], refs)


def tran(M, REF, CID, EX, dung_spice):
    keys = sorted(M)
    ca = [(k, j) for k in keys for j in range(len(M[k]))]
    cid = {(k, j): CID.score(M[k][j], REF[k]) for k, j in ca}
    sp = {}
    if dung_spice:
        vals = spice_mot_luot([M[k][j] for k, j in ca], [REF[k] for k, j in ca])
        sp = {kj: v for kj, v in zip(ca, vals)}
    eq = lambda a, b: tok(a) == tok(b)
    out = dict(n=len(keys),
               cider_best8=100 * sum(max(cid[(k, j)] for j in range(len(M[k]))) for k in keys) / len(keys),
               cider_tb=100 * sum(cid.values()) / len(ca),
               trung_chuan_bat_ky=100 * sum(any(eq(s, REF[k]) for s in M[k]) for k in keys) / len(keys))
    if sp:
        out["spice_best8"] = 100 * sum(max(sp[(k, j)] for j in range(len(M[k]))) for k in keys) / len(keys)
        out["spice_tb"] = 100 * sum(sp.values()) / len(ca)
    co = {k for k in keys if any(eq(e["sent"], REF[k]) for e in EX.get(k, []))}
    out["buoc_khoi_chua_chuan"] = len(co)
    out["chep_dung_trong_buoc_do"] = 100 * sum(any(eq(s, REF[k]) for s in M[k]) for k in co) / max(1, len(co))
    out["mau_trung_vi_du"] = 100 * sum(any(eq(s, e["sent"]) for e in EX.get(k, [])) for k in keys for s in M[k]) / len(ca)
    return out


def doc_mau(p):
    return {(d["episode_id"], d["step_id"]): d["samples"] for d in map(json.loads, open(p, encoding="utf-8"))}


def luat(ra, khong, greedy):
    ok1 = ("spice_best8" in ra) and ra["spice_best8"] - khong["spice_best8"] >= 1.0
    ok1b = ra["cider_best8"] - khong["cider_best8"] >= 10.0
    ok2 = greedy is None or (greedy["cider_d"] >= greedy["cider_d_khong"] - 10 and
                             greedy.get("spice", 0) >= greedy.get("spice_khong", 0) - 1.0)
    if (ok1 or ok1b) and ok2:
        return "ĐẠT - chạy RA-GRPO từ S1 (Phương án A)"
    if not (ok1 or ok1b) and ok2 and ra["chep_dung_trong_buoc_do"] < khong["chep_dung_trong_buoc_do"] + 5:
        return "KHÔNG ĐẠT vì S1 không dùng khối - muốn đi tiếp thì phải RA-SFT từ S1 trước (Phương án B), hỏi người dùng"
    return "KHÔNG ĐẠT - khối làm S1 kém đi hoặc không tăng trần; dừng hướng RA-GRPO"


def tu_kiem(dung_spice):
    REF = {(1, 0): "Click on the search bar", (1, 1): "Open the Clock app", (2, 0): "Tap on Save"}
    EX = {(1, 0): [{"sent": "Click on the search bar"}], (1, 1): [{"sent": "Tap on Save"}], (2, 0): [{"sent": "Open the Clock app"}]}
    M_ra = {(1, 0): ["Click on the search bar", "click search"], (1, 1): ["Open clock", "Open the Clock app"], (2, 0): ["Tap Save", "Save"]}
    M_kh = {(1, 0): ["click search", "tap bar"], (1, 1): ["Open clock", "open app"], (2, 0): ["Tap Save", "Save"]}
    CID = CiderD(list(REF.values()))
    a, b = tran(M_ra, REF, CID, EX, dung_spice), tran(M_kh, REF, CID, EX, dung_spice)
    assert a["trung_chuan_bat_ky"] > b["trung_chuan_bat_ky"] and a["cider_best8"] > b["cider_best8"], (a, b)
    assert a["buoc_khoi_chua_chuan"] == 1 and a["chep_dung_trong_buoc_do"] == 100.0, a
    print("[tự kiểm] ĐẠT", {k: round(v, 2) for k, v in a.items()})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recs")
    ap.add_argument("--ra")
    ap.add_argument("--mau-ra")
    ap.add_argument("--mau-khong")
    ap.add_argument("--diem-greedy", help="JSON của ra_score.py với nhánh S1 (không khối) và S1_ra (có khối)")
    ap.add_argument("--out")
    ap.add_argument("--no-spice", action="store_true")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        return tu_kiem(not a.no_spice)

    recs = [json.loads(l) for l in open(a.recs, encoding="utf-8")]
    REF = {(r["episode_id"], r["step_id"]): (r.get("target_instruction") or r.get("gold_instruction") or "").strip() for r in recs}
    EX = {(d["episode_id"], d["step_id"]): d["exemplars"] for d in map(json.loads, open(a.ra, encoding="utf-8"))}
    Mra, Mkh = doc_mau(a.mau_ra), doc_mau(a.mau_khong)
    assert set(Mra) == set(Mkh), "⛔ hai tệp mẫu không cùng bước"
    CID = CiderD([REF[k] for k in sorted(REF) if REF[k]])
    ra = tran(Mra, REF, CID, EX, not a.no_spice)
    kh = tran(Mkh, REF, CID, EX, not a.no_spice)
    g = None
    if a.diem_greedy:
        D = json.load(open(a.diem_greedy))["diem"]
        g = dict(cider_d=D["S1_ra"]["cider_d"], cider_d_khong=D["S1"]["cider_d"],
                 spice=D["S1_ra"].get("spice", 0), spice_khong=D["S1"].get("spice", 0),
                 bang={n: D[n] for n in D})
    kq = dict(co_khoi=ra, khong_khoi=kh, greedy=g, ket_luan=luat(ra, kh, g))
    for ten, o in (("CÓ khối", ra), ("KHÔNG khối", kh)):
        print(f"{ten:10s} " + " - ".join(f"{k} {v:.2f}" if isinstance(v, float) else f"{k} {v}" for k, v in o.items()))
    if g:
        print(f"greedy S1: CIDEr-D có khối {g['cider_d']:.2f} vs không {g['cider_d_khong']:.2f} - "
              f"SPICE {g['spice']:.2f} vs {g['spice_khong']:.2f}")
    print("→ CỔNG G0:", kq["ket_luan"])
    json.dump(kq, open(a.out, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
