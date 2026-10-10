# -*- coding: utf-8 -*-
"""304 — các luật ghép ck500 ↔ ra_k4 (0 GPU). Khoá 10/10 TRƯỚC khi có exec val của ra_k4.

Mọi luật chỉ dùng chữ (câu ra_k4, câu ck500, 4 ví dụ của khối) — không dùng bộ trỏ, không dùng câu chuẩn.
Bước nào luật nói "lấy" thì dùng câu ra_k4, còn lại giữ câu ck500.

  R0  chép                : câu ra_k4 trùng (sau tách từ) một ví dụ                       — luật `ghep` cũ (§3.3)
  R1  chép ∧ đồng thuận    : R0 và câu đó xuất hiện ở ≥ 2/4 ví dụ — LOẠI: khối k=4 đã khử trùng nên R1 lấy 0 bước (= ck500)
  R2  chép ∧ cùng phần tử  : R0 và phần lõi (bỏ động từ, hư từ, chữ chỉ vị trí/kiểu nút) giao ck500 với Jaccard ≥ 0,5
  R3  chép ∧ cùng thao tác : R0 và lớp động từ đầu câu trùng lớp của câu ck500 (chạm / nhấn giữ / gõ / cuộn / mở / quay lại …)
  R4  R2 ∧ R3

Tiêu chí chọn (khoá trước, chấm trên val lớn 1.002 click):
  trong các luật cao hơn ck500 ở ≥ 4/5 thước chữ val (BLEU-4, METEOR, ROUGE-L, CIDEr-D, chrF), chọn luật exec val cao nhất;
  hoà exec thì chọn luật đổi ít câu hơn; không luật nào đủ 4/5 thì giữ R0. Luật đã chọn áp lên test ĐÚNG MỘT LẦN.

    python3 luat_ghep_304.py dung   # ghi pred val + test cho R0..R4, in số câu đổi
"""
import json, os, re, sys

KHO = "/mnt/d/Master/Thesis"
sys.path.insert(0, f"{KHO}/_scripts/304/ra-sft-script")
import ra_exemplars as RA

S = f"{KHO}/_scripts/304/ra-sft-script/"
OUT = f"{KHO}/runs/ra304_luat"
NGUON = {
    "val": dict(ra=f"{KHO}/runs/ra304_T/pred_val_ra_k4.jsonl", ck=f"{S}pred_ck500_vallon.jsonl", ex=f"{S}ex_val_k4.jsonl"),
    "test": dict(ra=f"{KHO}/runs/ra304_G/pred_ra_k4_test.jsonl", ck=f"{S}pred_ck500_test.jsonl", ex=f"{S}ex_test_k4.jsonl"),
}
LUAT = ("R0", "R1", "R2", "R3", "R4")

STOP = set("""click tap tapped press pressed long select choose hit touch type enter input write search open launch go back
navigate scroll swipe drag move return close exit check uncheck toggle turn enable disable
on in at to the a an of for from with into onto and or then option options button buttons icon icons tab menu field box bar
text link item list section page screen app application display shown visible displayed which that this it its
top bottom left right upper lower middle center centre corner side first second third last next above below near beside
of""".split())

LOP = [("back", {"back"}), ("long", {"long"}), ("type", {"type", "enter", "input", "write"}),
       ("scroll", {"scroll", "swipe", "drag"}), ("open", {"open", "launch"}),
       ("tap", {"click", "tap", "press", "select", "choose", "hit", "touch", "check", "uncheck", "toggle", "turn"})]


def doc(p):
    return {(d["episode_id"], d["step_id"]): d for d in map(json.loads, open(p, encoding="utf-8"))}


def lop(s):
    t = RA.tok(s)
    if "go" in t[:2] and "back" in t[:3]:
        return "back"
    for w in t[:3]:
        for ten, v in LOP:
            if w in v:
                return ten
    return "khac"


def loi(s):
    return {w for w in RA.tok(s) if w not in STOP and not w.isdigit()}


def cung_phan_tu(a, b):
    A, B = loi(a), loi(b)
    if not A and not B:
        return True
    return len(A & B) / max(1, len(A | B)) >= 0.5


def quyet(ra, ck, ex):
    tr = RA.tok(ra)
    so = sum(RA.tok(e["sent"]) == tr for e in ex)
    chep = so >= 1
    r2 = chep and cung_phan_tu(ra, ck)
    r3 = chep and lop(ra) == lop(ck)
    return {"R0": chep, "R1": so >= 2, "R2": r2, "R3": r3, "R4": r2 and r3}


def dung():
    os.makedirs(OUT, exist_ok=True)
    for tap, N in NGUON.items():
        ra, ck, ex = doc(N["ra"]), doc(N["ck"]), doc(N["ex"])
        assert set(ra) == set(ck) == set(ex), tap
        Q = {k: quyet(ra[k]["pred"], ck[k]["pred"], ex[k]["exemplars"]) for k in ra}
        for L in LUAT:
            with open(f"{OUT}/pred_{L}_{tap}.jsonl", "w", encoding="utf-8") as f:
                for k in ra:
                    p = ra[k]["pred"] if Q[k][L] else ck[k]["pred"]
                    f.write(json.dumps(dict(episode_id=k[0], step_id=k[1], pred=p), ensure_ascii=False) + "\n")
        dem = {L: sum(Q[k][L] for k in ra) for L in LUAT}
        khac = {L: sum(Q[k][L] and ra[k]["pred"] != ck[k]["pred"] for k in ra) for L in LUAT}
        print(f"[{tap}] {len(ra)} bước · lấy câu ra_k4 {dem} · trong đó khác ck500 {khac}")


if __name__ == "__main__":
    dung()
