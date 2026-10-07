# -*- coding: utf-8 -*-
"""FREE · offline — PHÂN TÍCH NHÁNH S2 từ tệp thô, KHÔNG gọi lại bộ trỏ.

Trạng thái 20/8: mới có **một** hạt giống S2. Luật đọc Δ (`report/106` mục (w)) đòi
**trung bình hai hạt giống**, nên mọi con số ở đây là **TẠM**, để chẩn đoán chứ không
để kết luận. Chạy lại y nguyên khi có hạt giống 202.

Phép quan trọng nhất là ⑤: lát cắt *thành phần có kích hoạt hay không*, **đăng ký trước
ngày 19/8** — trước khi có bất kỳ điểm S2 nào (`report/110` mục 4j-16).

    python3 harness/phan_tich_s2.py
"""
import os, json, math, random, collections

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(os.path.dirname(HERE), "runs")
SEED = 20260805                      # cùng hạt giống với score_run.cluster_bootstrap


def nap(ten):
    """Tệp thô → {(ep, step): dòng}. Dòng `bo_qua` giữ nguyên, gắn exec = 0 cho khớp
    cách score_run tính điểm headline (nó cho câu rỗng vào quần thể với exec = 0)."""
    d = {}
    for l in open(os.path.join(RUNS, ten), encoding="utf-8"):
        o = json.loads(l)
        o["exec"] = int(o.get("executable", 0))
        d[(o["episode_id"], o["step_id"])] = o
    return d


def cum(o):
    return o.get("app") or f"ep{o['episode_id']}"


def boot_hieu(cap, B=10000, seed=SEED):
    """KTC95 của HIỆU ghép cặp, bootstrap gom cụm theo app — cùng phương pháp và cùng
    hạt giống với `score_run.cluster_bootstrap`, chỉ đổi đại lượng thành hiệu từng bước."""
    cl = collections.defaultdict(list)
    for k, a, b in cap:
        cl[k].append(b - a)
    g = list(cl.values())
    if not g:
        return 0.0, (0.0, 0.0)
    pt = sum(sum(x) for x in g) / sum(len(x) for x in g)
    rnd, G, bs = random.Random(seed), len(g), []
    for _ in range(B):
        pick = [g[rnd.randrange(G)] for _ in range(G)]
        den = sum(len(x) for x in pick)
        if den:
            bs.append(sum(sum(x) for x in pick) / den)
    bs.sort()
    return pt, (bs[int(.025 * len(bs))], bs[int(.975 * len(bs))])


def mcnemar(A, B, khoa):
    """b = A đúng & B sai · c = B đúng & A sai. χ² có hiệu chỉnh liên tục + nhị thức chính xác."""
    b = sum(1 for k in khoa if A[k]["exec"] and not B[k]["exec"])
    c = sum(1 for k in khoa if B[k]["exec"] and not A[k]["exec"])
    n = b + c
    chi = (abs(b - c) - 1) ** 2 / n if n else 0.0
    p = 1.0
    if n:
        p = min(1.0, 2 * sum(math.comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n)
    return b, c, chi, p


def dong(ten, A, B, khoa, nhan_a, nhan_b):
    if not khoa:
        print(f"  {ten:<34} (rỗng)"); return
    ea = sum(A[k]["exec"] for k in khoa) / len(khoa) * 100
    eb = sum(B[k]["exec"] for k in khoa) / len(khoa) * 100
    b, c, chi, p = mcnemar(A, B, khoa)
    pt, (lo, hi) = boot_hieu([(cum(A[k]), A[k]["exec"], B[k]["exec"]) for k in khoa])
    sao = "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else "   "
    print(f"  {ten:<34} n={len(khoa):5,}  {nhan_a} {ea:5.1f}  {nhan_b} {eb:5.1f}  "
          f"Δ {pt*100:+5.2f} [{lo*100:+5.2f},{hi*100:+5.2f}]  b={b:4d} c={c:4d} p={p:.3g}{sao}")


def main():
    S2 = nap("score_s2_seed101_raw.jsonl")
    S1 = nap("score_s1_seed101_raw.jsonl")
    S1b = nap("score_s1_seed202_raw.jsonl")
    BA = nap("score_base_raw.jsonl")
    TR = nap("score_ceiling_human_raw.jsonl")
    K = sorted(set(S2) & set(S1) & set(S1b) & set(BA) & set(TR))
    print(f"① QUẦN THỂ · giao năm nhánh: {len(K):,} bước  (mỗi tệp {len(S2):,})")
    for ten, D in [("trần", TR), ("S1/202", S1b), ("S1/101", S1), ("S2/101", S2), ("Base", BA)]:
        print(f"   {ten:<7} {sum(D[k]['exec'] for k in K)/len(K)*100:5.2f}%")

    print("\n② GHÉP CẶP McNemar — ⚠️ TẠM, mới một hạt giống S2")
    dong("S2/101 vs S1/101", S1, S2, K, "S1", "S2")
    dong("S2/101 vs S1/202", S1b, S2, K, "S1", "S2")
    dong("S2/101 vs Base  ", BA, S2, K, "Ba", "S2")
    dong("S1/101 vs Base   (đối chiếu)", BA, S1, K, "Ba", "S1")
    dong("S1/202 vs S1/101 (NHIỄU hạt giống)", S1, S1b, K, "a ", "b ")

    # ── ⑤ lát cắt ĐĂNG KÝ TRƯỚC 19/8: thành phần có kích hoạt hay không ─────────
    cr = json.load(open(os.path.join(RUNS, "co_rac_s2_seed101.json"), encoding="utf-8"))
    khong = {tuple(x) for x in cr["khong_co_desc"]} | {tuple(x) for x in cr["mo_khong_dong"]}
    rac = {tuple(x) for x in cr["co_rac"]}
    kich = [k for k in K if k not in khong]
    tat = [k for k in K if k in khong]
    print(f"\n⑤ LÁT CẮT ĐĂNG KÝ TRƯỚC — thành phần có kích hoạt không "
          f"({len(kich):,} có · {len(tat):,} không)")
    dong("nhóm CÓ kích hoạt", S1, S2, kich, "S1", "S2")
    dong("nhóm KHÔNG kích hoạt", S1, S2, tat, "S1", "S2")
    dong("  trong nhóm CÓ: khai báo SẠCH", S1, S2, [k for k in kich if k not in rac], "S1", "S2")
    dong("  trong nhóm CÓ: khai báo RÁC", S1, S2, [k for k in kich if k in rac], "S1", "S2")

    print("\n⑥ LÁT CẮT KHÁC")
    dong("app đã thấy khi dạy", S1, S2, [k for k in K if S2[k].get("app_seen_in_train") is True], "S1", "S2")
    dong("app CHƯA thấy", S1, S2, [k for k in K if S2[k].get("app_seen_in_train") is False], "S1", "S2")
    dong("không gán được app", S1, S2, [k for k in K if S2[k].get("app_seen_in_train") is None], "S1", "S2")
    med = sorted(len(S2[k].get("sent", "")) for k in K)[len(K)//2]
    dong(f"câu S2 DÀI (>{med} ký tự)", S1, S2, [k for k in K if len(S2[k].get("sent",""))> med], "S1", "S2")
    dong(f"câu S2 NGẮN (≤{med})", S1, S2, [k for k in K if len(S2[k].get("sent",""))<=med], "S1", "S2")
    nb = sorted(S2[k].get("n_buttons", 0) for k in K)[len(K)//2]
    dong(f"màn NHIỀU nút (>{nb})", S1, S2, [k for k in K if S2[k].get("n_buttons",0) > nb], "S1", "S2")
    dong(f"màn ÍT nút (≤{nb})", S1, S2, [k for k in K if S2[k].get("n_buttons",0) <= nb], "S1", "S2")

    print("\n⑦ HỎNG Ở ĐÂU — phân rã ba điều kiện của thước")
    for ten, D in [("S1/101", S1), ("S2/101", S2)]:
        tr = [D[k] for k in K if not D[k]["exec"]]
        sai_tt = sum(1 for o in tr if not o.get("action_ok", 1))
        sai_to = sum(1 for o in tr if o.get("action_ok", 1) and not o.get("toggle_ok", 1))
        sai_vt = sum(1 for o in tr if o.get("action_ok", 1) and o.get("toggle_ok", 1)
                     and not o.get("hit_voronoi", 0))
        print(f"  {ten}: trượt {len(tr):,}  ·  sai thao tác {sai_tt:,} ({sai_tt/len(tr):.0%})"
              f"  ·  đảo nghĩa {sai_to:,}  ·  ĐÚNG thao tác mà trỏ trượt {sai_vt:,} ({sai_vt/len(tr):.0%})")

    print("\n⑧ SAI SỐ BỘ TRỎ (phần trăm bề ngang màn) — trung vị · p90")
    for ten, D in [("trần", TR), ("S1/101", S1), ("S2/101", S2), ("Base", BA)]:
        e = sorted(math.dist(o["pred_xy"], o["gold_xy"]) / o["wh"][0] * 100
                   for k in K for o in [D[k]] if o.get("pred_xy") and o.get("wh"))
        print(f"  {ten:<7} n={len(e):5,}  trung vị {e[len(e)//2]:5.2f}%  p90 {e[int(.9*len(e))]:6.2f}%")


if __name__ == "__main__":
    main()
