# -*- coding: utf-8 -*-
"""Thư viện đọc tệp thô test (B.9 của 288) — `doc_288.py` và `289/doc_289.py` import.

Viết lại 6/10/2026 từ bản mô tả Phụ lục B của 288 (mã gốc nằm trên máy Mac, không có ở đây) ⇒ md5
khác bản gốc. Chỉ dựng lại PHẦN THƯ VIỆN; bộ đọc riêng của 286 (giả thuyết H1…Hg1, --mau-nguoi)
không dùng cho 288 nên không viết lại.

Quyết định số: bootstrap cụm theo episode, B = 10.000, rng do NGƯỜI GỌI truyền vào và có thể được
dùng lại qua nhiều phép so liên tiếp ⇒ thứ tự các phép so ở script gọi là một phần của kết quả.
"""
import ast, json, math, re
import numpy as np

SEED = 101
B_BOOT = 10000
TAPT = ("click", "long_press")

_ANH_XA = {}
for _loai, _tu in (("tap", "tap click press select choose touch open go navigate visit view"),
                   ("type", "type enter input fill write"),
                   ("scroll", "scroll swipe drag"),
                   ("long_press", "long hold"),
                   ("navigate_back", "back return")):
    for _w in _tu.split():
        _ANH_XA[_w] = _loai

_PHU = {"scroll": {"scroll", "swipe", "slide", "drag"}, "navigate_back": {"back"},
        "input_text": {"type", "enter", "input", "write", "fill"}, "open_app": {"open", "launch", "start"},
        "wait": {"wait", "pause", "load", "loading", "loaded"}, "navigate_home": {"home"},
        "long_press": {"long", "hold"}}

def action_of(r):
    a = r.get("action")
    return ast.literal_eval(a) if isinstance(a, str) else (a or {})


def la_cham(r):
    a = action_of(r)
    return a.get("action_type") in TAPT and "x" in a


def canon(cau, strict_back=False):
    w = re.findall(r"[a-z]+", (cau or "").lower())
    if strict_back and "back" in w:
        return "navigate_back"
    for x in w:
        if x in _ANH_XA:
            return _ANH_XA[x]
    return "tap"


def phu_ok(cau, action_type):
    w = set(re.findall(r"[a-z]+", (cau or "").lower()))
    return int(bool(w & _PHU.get(action_type, set())))


def cluster_ci(d, ep, rng, q=0.025, B=B_BOOT):
    """d: hiệu theo bước (0/±1), ep: mã episode từng bước → (100·mean, 100·q, 100·(1−q))."""
    d = np.asarray(d, float)
    u, idx = np.unique(np.asarray(ep), return_inverse=True)
    E = len(u)
    tong = np.bincount(idx, weights=d, minlength=E)
    dem = np.bincount(idx, minlength=E).astype(float)
    pick = rng.integers(0, E, size=(B, E))
    m = tong[pick].sum(1) / dem[pick].sum(1)
    return 100 * d.mean(), 100 * float(np.quantile(m, q)), 100 * float(np.quantile(m, 1 - q))


def mcnemar(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def doc_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def nap(recs, raw, nontap=None):
    """recs: danh sách bản ghi test (đã gắn `_tap`); raw: tệp thô score_run; nontap: tệp dự đoán bước không chạm.
    → ex {khoá: exec}, nt {khoá: (đúng loại, phu_ok)}, sx {khoá: câu đã chấm}, snt {khoá: câu}."""
    ex, sx = {}, {}
    for o in doc_jsonl(raw):
        k = (o["episode_id"], o["step_id"])
        ex[k] = int(o.get("executable") or 0)
        sx[k] = o.get("sent")
    nt, snt = {}, {}
    if nontap:
        P = {(d["episode_id"], d["step_id"]): d.get("pred") or "" for d in doc_jsonl(nontap)}
        for r in recs:
            if r["_tap"]:
                continue
            k = (r["episode_id"], r["step_id"])
            assert k in P, f"DỪNG: {nontap} thiếu bước không chạm {k}"
            s, at = P[k], action_of(r).get("action_type") or ""
            vang = canon(r.get("target_instruction") or r.get("gold_instruction") or "", True)
            dung = int(bool(s) and canon(s, True) == vang)      # canon strict CẢ HAI phía
            nt[k] = (dung, phu_ok(s, at))
            snt[k] = s
    return ex, nt, sx, snt


def so(A, B, keys, ep, rng):
    """A, B: {khoá: 0/1}; keys: danh sách khoá đã sắp; ep: {khoá: episode}."""
    a = np.array([A[k] for k in keys], float)
    b = np.array([B[k] for k in keys], float)
    d, lo, hi = cluster_ci(a - b, [ep[k] for k in keys], rng)
    cuu = int(((a == 1) & (b == 0)).sum())
    pha = int(((a == 0) & (b == 1)).sum())
    return dict(n=len(keys), a=round(100 * a.mean(), 2), b=round(100 * b.mean(), 2), d=d, lo=lo, hi=hi,
                cuu=cuu, pha=pha, p_mcnemar=round(mcnemar(cuu, pha), 4))


def aisr(S1, ck500):
    """Nhánh ghép suy luận của 286: S1, ck500 là bộ 4 của nap(). Trả (ex, nt, số bước bỏ qua)."""
    ex1, nt1, sx1, snt1 = S1
    ex5, nt5, sx5, snt5 = ck500
    ex, bo = {}, 0
    for k in ex1.keys() & ex5.keys():
        if sx1.get(k) is None or sx5.get(k) is None:
            ex[k] = ex5[k]; bo += 1
        else:
            ex[k] = ex5[k] if canon(sx1[k]) == canon(sx5[k]) else ex1[k]
    nt = {}
    for k in nt1.keys() & nt5.keys():
        nt[k] = nt5[k] if canon(snt1[k], True) == canon(snt5[k], True) else nt1[k]
    return ex, nt, bo


def fmt(r, ten=""):
    return (f"{ten:<26} n={r['n']:>5} · {r['a']:6.2f} vs {r['b']:6.2f} · Δ {r['d']:+6.2f} "
            f"[{r['lo']:+.2f}; {r['hi']:+.2f}] · cứu {r['cuu']} phá {r['pha']} · p {r['p_mcnemar']}")


if __name__ == "__main__":
    print("doc_286.py chỉ là thư viện cho 288/289; bộ đọc riêng của 286 không được dựng lại.")
