# -*- coding: utf-8 -*-
"""FREE · offline — đọc kết quả ba nhánh SÀN theo luật đã khoá TRƯỚC.

Luật đọc nằm ở `harness/make_floor.py` (viết trước khi chấm) và
`harness/kaggle_cham_san.md`. Script này chỉ **áp** luật đó, không chế thêm.

⚠️ Con số của bài là con số trên **phần bị đụng**, không phải số tổng — `f2_khongten` chỉ
viết lại được ~24% số bước, nên số tổng bị pha loãng ~4 lần (cùng bẫy đã mắc ở phép A).

Chạy: python3 harness/doc_san.py
"""
import os, json, math

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "runs"))
F = os.path.join(R, "floor")
TEST = os.path.join(os.path.dirname(__file__), "dg1_cache", "test_ac", "test.jsonl")


def nap(p):
    d = {}
    for l in open(p, encoding="utf-8"):
        o = json.loads(l)
        if "bo_qua" not in o:
            d[(o["episode_id"], o["step_id"])] = o
    return d


def mcnemar(K, A, B):
    b = sum(1 for k in K if A[k]["executable"] == 1 and B[k]["executable"] == 0)
    c = sum(1 for k in K if A[k]["executable"] == 0 and B[k]["executable"] == 1)
    n = b + c
    chi = (abs(b - c) - 1) ** 2 / n if n else 0.0
    return b, c, n, chi, (math.erfc(math.sqrt(chi / 2)) if n else 1.0)


def ty(K, d, key="executable"):
    return sum(d[k][key] for k in K) / max(len(K), 1) * 100


def main():
    G = {}
    for l in open(TEST, encoding="utf-8"):
        o = json.loads(l)
        G[(o["episode_id"], o["step_id"])] = o["gold_instruction"].strip()
    ce = nap(f"{R}/score_ceiling_human_raw.jsonl")

    co = {}
    for v in ["f1_trong", "f3_lechman", "f2_khongten"]:
        p = f"{F}/score_{v}_raw.jsonl"
        if os.path.exists(p):
            co[v] = nap(p)
        else:
            print(f"⏳ chưa có {p}")
    if not co:
        return
    lat = sorted(set.intersection(*[set(v) for v in co.values()]) & set(ce))
    print(f"lát {len(lat)} bước · trần trên lát này {ty(lat, ce):.1f}%\n")
    print("═" * 72)

    for v, d in co.items():
        doi = [k for k in lat if d[k]["sent"].strip() != G[k]]
        b, c, n, chi, p = mcnemar(doi, ce, d)
        print(f"\n{v}  ·  {len(doi)} bước bị đụng ({len(doi)/len(lat):.1%})")
        print(f"  toàn lát      trần {ty(lat, ce):5.1f}%  →  {ty(lat, d):5.1f}%  "
              f"({ty(lat, d)-ty(lat, ce):+.1f})")
        print(f"  phần bị đụng  trần {ty(doi, ce):5.1f}%  →  {ty(doi, d):5.1f}%  "
              f"({ty(doi, d)-ty(doi, ce):+.1f})   b={b} c={c} χ²={chi:.2f} p={p:.3f}")
        print(f"  chỉ định vị (Voronoi, bỏ cổng thao tác): {ty(doi, d, 'hit_voronoi'):.1f}%")

    print("\n" + "═" * 72)
    print("ĐỌC THEO LUẬT ĐÃ KHOÁ TRƯỚC")
    print("═" * 72)
    if "f1_trong" in co:
        s = ty(lat, co["f1_trong"])
        tran = ty(lat, ce)
        print(f"  SÀN = {s:.1f}%   TRẦN = {tran:.1f}%   ⇒ dải dùng được {tran-s:.1f} điểm")
        if s > 30:
            print(f"  ⚠ SÀN CAO. Mọi con số đọc trên nền {s:.1f}, KHÔNG phải 0.")
            print(f"     Base 47,6 thật ra chỉ hơn 'không nói gì' {47.6-s:.1f} điểm.")
            print(f"     Mọi câu dạng 'lấp N% dư địa' phải tính lại theo (trần − sàn).")
        else:
            print("  ✔ sàn thấp — thước đòi câu phải mang thông tin.")
    if "f1_trong" in co and "f3_lechman" in co:
        a, b_ = ty(lat, co["f1_trong"]), ty(lat, co["f3_lechman"])
        print(f"\n  f1 {a:.1f}%  vs  f3 {b_:.1f}%   (lệch {b_-a:+.1f})")
        if abs(b_ - a) < 3:
            print("  ✔ f1 là SÀN CÔNG BẰNG — điểm sàn không phải hiệu ứng 'câu kỳ quặc'.")
        elif b_ > a:
            print("  ⚠ câu ĐÚNG VĂN PHONG mà SAI NỘI DUNG vẫn ăn điểm cao hơn câu vô nghĩa")
            print("     ⇒ nhiễm văn phong CÓ THẬT và ĐO ĐƯỢC. Phải khai, và đây là con số của nó.")
        else:
            print("  câu sai dẫn bộ trỏ đi lạc ⇒ sàn thật còn thấp hơn f1.")
    if "f2_khongten" in co:
        d = co["f2_khongten"]
        doi = [k for k in lat if d[k]["sent"].strip() != G[k]]
        tut = ty(doi, ce) - ty(doi, d)
        print(f"\n  f2 (bỏ TÊN, giữ vị trí): tụt {tut:.1f} pp trên {len(doi)} bước")
        print(f"  đối chiếu p3_nopos (bỏ VỊ TRÍ, giữ tên): tụt 3,5 pp trên 198 bước")
        if tut > 10:
            print("  ✔ GỌI TÊN là kênh chính ⇒ 'Element Identification' ở nhan đề ĐÚNG,"
                  " và nay có số bảo vệ.")
        elif tut < 6:
            print("  ⛔ bỏ tên gần như không mất gì ⇒ thước đo CHỈ CHỖ, không đo GỌI TÊN.")
            print("     Nhan đề phải đổi: 'localisation' / 'target resolution'.")
            print(f"     ⚠ NHƯNG n={len(doi)} chưa phân biệt được 'tụt nhỏ' với 'không tụt' —"
                  " phải chấm lại f2 trên đủ 4.463 bước trước khi đổi nhan đề.")
        else:
            print("  vùng xám: tên có đóng góp nhưng không áp đảo vị trí. Cần f2 toàn tập.")


if __name__ == "__main__":
    main()
