# -*- coding: utf-8 -*-
"""
C1 — Phân tích kết quả chấm tay (report/90 Giai đoạn C).
Đọc cv_ratings_A.json + cv_ratings_B.json → đối chiếu điểm NGƯỜI với điểm THƯỚC.

Câu hỏi cần trả lời:
 1. Thước có nối được với phán xét của người không?  (tương quan)
 2. Hai người có chấm giống nhau không?               (κ — nếu thấp thì bản thân điểm người vô nghĩa)
 3. Thước kết oan / bỏ lọt bao nhiêu trên dữ liệu THẬT?
 4. Gold AndroidControl có thật sự là "hướng dẫn cho người" không?  (nhánh đối chứng ngầm)

Chạy: ~/.venvs/thesis/bin/python harness/cv_analyze.py
"""
import os, sys, json, math, itertools
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cv_study")
GOOD = 2          # điểm người >= 2 coi là "dùng được"
NBOOT = 10000
SEED = 20260719


def spearman(x, y):
    def rank(v):
        s = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(s):
            j = i
            while j + 1 < len(s) and v[s[j + 1]] == v[s[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[s[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(x), rank(y)
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else float("nan")


def kappa_weighted(a, b, K=4):
    """Cohen's κ có trọng số bậc hai — hợp cho thang thứ bậc 0-3."""
    n = len(a)
    O = [[0] * K for _ in range(K)]
    for x, y in zip(a, b):
        O[x][y] += 1
    ra = [sum(O[i]) for i in range(K)]
    cb = [sum(O[i][j] for i in range(K)) for j in range(K)]
    w = [[((i - j) / (K - 1)) ** 2 for j in range(K)] for i in range(K)]
    num = sum(w[i][j] * O[i][j] for i in range(K) for j in range(K))
    den = sum(w[i][j] * ra[i] * cb[j] / n for i in range(K) for j in range(K))
    return 1 - num / den if den else float("nan")


def boot_ci(vals, stat, nboot=NBOOT, seed=SEED):
    import random
    rng = random.Random(seed)
    n = len(vals)
    out = []
    for _ in range(nboot):
        s = [vals[rng.randrange(n)] for _ in range(n)]
        try:
            out.append(stat(s))
        except Exception:
            pass
    out.sort()
    return out[int(.025 * len(out))], out[int(.975 * len(out))]


def load():
    items = {i["id"]: i for i in json.load(open(os.path.join(OUT, "items.json"), encoding="utf-8"))["items"]}
    key = json.load(open(os.path.join(OUT, "items.json"), encoding="utf-8"))["ab_key"]
    raters = {}
    for r in ("A", "B"):
        p = os.path.join(OUT, f"cv_ratings_{r}.json")
        if not os.path.exists(p):
            print(f"⚠ CHƯA CÓ {p} — người {r} chấm xong thì để file vào đó.")
            continue
        raters[r] = json.load(open(p, encoding="utf-8"))["ratings"]
    return items, key, raters


def unblind(raters, key):
    """Đổi nhãn A/B của giao diện về teacher/gold."""
    out = {}
    for r, rat in raters.items():
        d = {}
        for iid, v in rat.items():
            if v.get("a") is None or v.get("b") is None:
                continue
            a_is = key[r][iid]
            d[iid] = {
                "teacher": v["a"] if a_is == "teacher" else v["b"],
                "gold": v["b"] if a_is == "teacher" else v["a"],
                "teacher_flag": bool(v.get("fa") if a_is == "teacher" else v.get("fb")),
                "gold_flag": bool(v.get("fb") if a_is == "teacher" else v.get("fa")),
                "diff_step": bool(v.get("diff")),
            }
        out[r] = d
    return out


def main():
    items, key, raters = load()
    if not raters:
        print("Chưa có file chấm nào. Dừng."); return
    U = unblind(raters, key)
    ids = sorted(set.intersection(*[set(d) for d in U.values()])) if len(U) > 1 else sorted(next(iter(U.values())))
    print(f"Số màn có đủ điểm: {len(ids)} / {len(items)}\n")

    # ---- 2. hai người có chấm giống nhau không ----
    if len(U) == 2:
        a = [U["A"][i]["teacher"] for i in ids] + [U["A"][i]["gold"] for i in ids]
        b = [U["B"][i]["teacher"] for i in ids] + [U["B"][i]["gold"] for i in ids]
        k = kappa_weighted(a, b)
        lo, hi = boot_ci(list(zip(a, b)), lambda s: kappa_weighted([x[0] for x in s], [x[1] for x in s]))
        print(f"[2] Đồng thuận hai người chấm: κ có trọng số = {k:.3f}  (CI95 {lo:.3f}–{hi:.3f})")
        print(f"    khớp tuyệt đối {sum(1 for x,y in zip(a,b) if x==y)/len(a):.1%} · "
              f"lệch ≤1 điểm {sum(1 for x,y in zip(a,b) if abs(x-y)<=1)/len(a):.1%}")
        if k < 0.4:
            print("    ⚠ κ thấp → chính điểm người đã nhiễu, mọi tương quan bên dưới đọc rất dè dặt.")
        print()

    # điểm người gộp (trung bình hai người nếu có đủ)
    def h(i, arm):
        v = [U[r][i][arm] for r in U]
        return sum(v) / len(v)

    ht = [h(i, "teacher") for i in ids]
    hg = [h(i, "gold") for i in ids]
    ms = [items[i]["metric"]["target_score"] for i in ids]
    mm = [1.0 if items[i]["metric"]["match"] else 0.0 for i in ids]

    # ---- 1. thước có nối với người không ----
    print("[1] THƯỚC ↔ NGƯỜI (chỉ tính trên câu của teacher — đây là câu hỏi chính)")
    r1 = spearman(ht, ms)
    r2 = spearman(ht, mm)
    lo1, hi1 = boot_ci(list(zip(ht, ms)), lambda s: spearman([x[0] for x in s], [x[1] for x in s]))
    lo2, hi2 = boot_ci(list(zip(ht, mm)), lambda s: spearman([x[0] for x in s], [x[1] for x in s]))
    print(f"    Spearman(điểm người, target_score) = {r1:+.3f}  (CI95 {lo1:+.3f}–{hi1:+.3f})")
    print(f"    Spearman(điểm người, khớp/không)   = {r2:+.3f}  (CI95 {lo2:+.3f}–{hi2:+.3f})")
    verdict = ("ĐỦ để nói thước có nối với người" if r2 >= 0.5 else
               "YẾU — thước và người nhìn hai thứ khác nhau" if r2 >= 0.3 else
               "RỚT — thước gần như không liên quan tới phán xét của người")
    print(f"    → {verdict}\n")

    # ---- 3. kết oan / bỏ lọt ----
    print("[3] THƯỚC SAI Ở ĐÂU (điểm người ≥%d = 'dùng được')" % GOOD)
    oan = [i for i in ids if h(i, "teacher") >= GOOD and not items[i]["metric"]["match"]]
    lot = [i for i in ids if h(i, "teacher") < GOOD and items[i]["metric"]["match"]]
    good = [i for i in ids if h(i, "teacher") >= GOOD]
    bad = [i for i in ids if h(i, "teacher") < GOOD]
    print(f"    KẾT OAN: {len(oan)}/{len(good)} = {len(oan)/max(len(good),1):.1%} câu người thấy dùng được nhưng thước bác")
    print(f"    BỎ LỌT: {len(lot)}/{len(bad)} = {len(lot)/max(len(bad),1):.1%} câu người thấy tệ nhưng thước cho qua")

    # tách KẾT OAN thành hai loại rất khác nhau — đây mới là con số dùng được
    def isdiff(i):
        return sum(1 for r in U if U[r][i]["diff_step"]) >= (2 if len(U) == 2 else 1)
    oan_wording = [i for i in oan if not isdiff(i)]
    oan_altstep = [i for i in oan if isdiff(i)]
    print(f"      ├─ do CÂU CHỮ (cùng một bước, thước vẫn bác): {len(oan_wording)} "
          f"= {len(oan_wording)/max(len(good),1):.1%} ← LỖI CỦA THƯỚC")
    print(f"      └─ do BƯỚC KHÁC (teacher chọn bước hợp lệ khác gold): {len(oan_altstep)} "
          f"= {len(oan_altstep)/max(len(good),1):.1%} ← giới hạn của gold-một-đáp-án")
    if len(good) and len(oan_wording) / len(good) > 0.20:
        print("      ⚠ Tỉ lệ lỗi-câu-chữ cao → đúng cơ chế thổi phồng hiệu-cặp ở report/90 §1.3.")
    print("\n    Ví dụ KẾT OAN do câu chữ (lỗi thật của thước):")
    for i in (oan_wording or oan)[:8]:
        m = items[i]["metric"]
        print(f"      oan · người={h(i,'teacher'):.1f} ts={m['target_score']:.2f} a_ok={m['a_ok']}")
        print(f"           teacher: {items[i]['teacher']}")
        print(f"           gold   : {items[i]['gold']}")
    print()

    # ---- 4. gold có phải hướng dẫn cho người không ----
    print("[4] GOLD ANDROIDCONTROL CÓ PHẢI 'HƯỚNG DẪN CHO NGƯỜI' KHÔNG (nhánh đối chứng)")
    mg, mt = sum(hg) / len(hg), sum(ht) / len(ht)
    d = [g - t for g, t in zip(hg, ht)]
    lo, hi = boot_ci(d, lambda s: sum(s) / len(s))
    print(f"    điểm người cho GOLD    = {mg:.2f}/3")
    print(f"    điểm người cho TEACHER = {mt:.2f}/3")
    print(f"    hiệu gold − teacher    = {mg-mt:+.2f}  (CI95 {lo:+.2f}–{hi:+.2f})")
    print(f"    gold bị chấm ≤1 điểm: {sum(1 for v in hg if v<=1)}/{len(hg)} = {sum(1 for v in hg if v<=1)/len(hg):.1%}")
    if mg < 2.0:
        print("    ⚠ Gold tự nó đã không đạt 'dùng được' → củng cố phát hiện 4.1 report/90:")
        print("      target train là nhãn thao tác ngắn, không phải văn hướng dẫn cho người.")
    print()

    # ---- cờ bịa ----
    ft = sum(1 for i in ids if any(U[r][i]["teacher_flag"] for r in U))
    fg = sum(1 for i in ids if any(U[r][i]["gold_flag"] for r in U))
    print(f"[5] Cờ 'chỉ vào thứ không có trên màn': teacher {ft}/{len(ids)} = {ft/len(ids):.1%} · "
          f"gold {fg}/{len(ids)} = {fg/len(ids):.1%}")

    json.dump({"n": len(ids), "spearman_ts": r1, "spearman_match": r2,
               "kappa": k if len(U) == 2 else None,
               "ket_oan": len(oan), "ket_oan_wording": len(oan_wording), "ket_oan_altstep": len(oan_altstep),
               "bo_lot": len(lot), "n_good": len(good), "n_bad": len(bad),
               "human_gold": mg, "human_teacher": mt,
               "flag_teacher": ft, "flag_gold": fg,
               "oan_ids": oan, "lot_ids": lot},
              open(os.path.join(HERE, "cv_results.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nĐã lưu harness/cv_results.json")


if __name__ == "__main__":
    main()
