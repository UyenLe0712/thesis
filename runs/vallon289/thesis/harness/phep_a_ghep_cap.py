# -*- coding: utf-8 -*-
"""FREE · offline — đọc kết quả PHÉP DIỄN ĐẠT LẠI theo cách GHÉP CẶP.

Vì sao không đọc con số tổng là đủ. `p1_verb` cho 75,0% so với trần 74,9% — lệch +0,1 pp,
tức **1 bước ròng** trên 800. Nhưng "1 bước ròng" có thể là ba chuyện khác nhau hẳn:

    3 bước đổi chiều          → bộ trỏ gần như bất động trước cách diễn đạt
    27 bước đổi chiều, 13/14  → có nhiễu thật nhưng không lệch về phía nào
    300 bước đổi chiều        → bộ trỏ rung dữ dội, chỉ tình cờ bù trừ

Con số tổng không phân biệt được. Chỉ tệp thô phân biệt được, và nó miễn phí vì cả hai
lượt chấm **cùng 800 bước** — ghép cặp sạch, không phải trừ bù.

Chạy: python3 harness/phep_a_ghep_cap.py
"""
import os, json, math, statistics as st

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "runs"))
P = os.path.join(R, "paraphrase")
BIEN_THE = ["p1_verb", "p2_order", "p3_nopos", "p4_both"]


def nap(p):
    d = {}
    for l in open(p, encoding="utf-8"):
        o = json.loads(l)
        d[(o["episode_id"], o["step_id"])] = o
    return d


def sai_so(o):
    """Sai số bộ trỏ theo công thức cổng A: khoảng cách chia BỀ NGANG, tính %.

    Cả dx lẫn dy đều chia wh[0]. Không phải nhầm: `ground_pilot` chia dy cho chiều CAO
    nên nhẹ đi 2,2 lần, và số 3% của cổng A nói theo công thức này.
    """
    dx = abs(o["pred_xy"][0] - o["gold_xy"][0]) / o["wh"][0]
    dy = abs(o["pred_xy"][1] - o["gold_xy"][1]) / o["wh"][0]
    return math.hypot(dx, dy) * 100


def mcnemar(K, a, b, key="executable"):
    """b = a-trúng→b-trượt · c = a-trượt→b-trúng. Yates, hai phía."""
    nb = sum(1 for k in K if a[k][key] == 1 and b[k][key] == 0)
    nc = sum(1 for k in K if a[k][key] == 0 and b[k][key] == 1)
    n = nb + nc
    chi = (abs(nb - nc) - 1) ** 2 / n if n else 0.0
    p = math.erfc(math.sqrt(chi / 2)) if n else 1.0
    return nb, nc, n, chi, p


def main():
    ceil = nap(f"{R}/score_ceiling_human_raw.jsonl")
    s1 = nap(f"{R}/score_s1_seed101_raw.jsonl")

    for v in BIEN_THE:
        f = f"{P}/score_para_{v}_raw.jsonl"
        if not os.path.exists(f):
            print(f"\n=== {v}: chưa có tệp thô, bỏ qua ===")
            continue
        para = nap(f)
        K = [k for k in para if k in ceil]
        doi = [k for k in K if para[k]["sent"].strip() != ceil[k]["sent"].strip()]

        print(f"\n=== {v} · {len(K)} bước ghép cặp · câu thật sự đổi "
              f"{len(doi)} ({len(doi)/len(K):.1%}) · pha loãng {len(K)/max(len(doi),1):.1f}× ===")
        # Hai cột: TOÀN LÁT là số ô Kaggle in ra, đã bị pha loãng bởi các bước câu y nguyên.
        # PHẦN BỊ ĐỤNG là số của bài — chỉ những bước câu thật sự đổi mới nói được điều gì.
        for ten in ["executable", "hit_voronoi", "hit_disk", "action_ok"]:
            at = sum(ceil[k][ten] for k in K) / len(K) * 100
            bt = sum(para[k][ten] for k in K) / len(K) * 100
            ad = sum(ceil[k][ten] for k in doi) / max(len(doi), 1) * 100
            bd = sum(para[k][ten] for k in doi) / max(len(doi), 1) * 100
            print(f"  {ten:12s} toàn lát {at:5.1f}→{bt:5.1f} ({bt-at:+.1f})"
                  f"   ‖ phần bị đụng {ad:5.1f}→{bd:5.1f} ({bd-ad:+.1f})")

        for nhan, KK in [("toàn lát", K), ("phần bị đụng", doi)]:
            nb, nc, n, chi, p = mcnemar(KK, ceil, para)
            print(f"  {nhan:14s} trúng→trượt {nb:3d} · trượt→trúng {nc:3d} · "
                  f"đổi chiều {n:3d} ({n/max(len(KK),1):.1%}) · χ²={chi:.2f} p={p:.3f}")

        print(f"  sai số trỏ trung vị: toàn lát {st.median(sai_so(ceil[k]) for k in K):.2f}"
              f"→{st.median(sai_so(para[k]) for k in K):.2f}%"
              f"  ‖ phần bị đụng {st.median(sai_so(ceil[k]) for k in doi):.2f}"
              f"→{st.median(sai_so(para[k]) for k in doi):.2f}%")

        # lát 800 có đại diện cho toàn tập không — mốc toàn tập 75,7 / 59,1
        KS = [k for k in K if k in s1]
        print(f"  đối chiếu lát: trần {sum(ceil[k]['executable'] for k in KS)/len(KS)*100:.1f}%"
              f" · S1 {sum(s1[k]['executable'] for k in KS)/len(KS)*100:.1f}%"
              f"  (toàn tập 75,7 / 59,1)")


if __name__ == "__main__":
    main()
