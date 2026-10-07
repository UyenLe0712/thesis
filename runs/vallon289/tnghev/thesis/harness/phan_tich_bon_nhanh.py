# -*- coding: utf-8 -*-
"""FREE · 0 GPU — vắt kiệt bốn tệp thô đã chấm.

Bốn nhánh đã chấm (trần · s1/101 · s1/202 · Base) nằm trong `runs/*_raw.jsonl`, mỗi dòng một
bước với toạ độ bộ trỏ trả về. Rất nhiều câu hỏi về TÍNH HỢP LỆ của thước trả lời được từ đây
mà không cần gọi lại bộ trỏ. Script này làm tám phép, xếp theo mức đóng góp cho bài:

  A. bảng bốn nhánh, hai hạt giống                    — con số chính thức
  B. LẶP LẠI mọi lát cắt chẩn đoán ở hạt giống thứ hai — lát nào tái lập, lát nào không
  C. trần có phải trần THEO TỪNG BƯỚC không            — hay chỉ là mức tổng
  D. hợp của bốn nhánh                                  — vùng mù thật của dụng cụ
  E. bộ trỏ có ĐỌC câu không                            — xấp xỉ MIỄN PHÍ cho phép đo sàn
  F. bước mọi nhánh đều trượt                           — lõi cứng của vùng mù
  G. thiên vị độ dài, kiểm ở cả hai hạt giống
  H. thắng-hoà-thua theo cụm, cả hai hạt giống

Phép E đáng chú ý: nếu hai nhánh viết câu KHÁC HẲN nhau mà bộ trỏ trả về gần như CÙNG một
điểm, thì ở bước đó câu chữ không ảnh hưởng gì — bộ trỏ đọc màn hình chứ không đọc câu. Đếm
tỉ lệ ấy cho một **cận dưới của sàn** mà không phải chấm thêm lượt nào.

Chạy: python3 harness/phan_tich_bon_nhanh.py
"""
import os, json, math, statistics as st

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "runs"))
NHANH = {"tran": "score_ceiling_human_raw.jsonl", "s101": "score_s1_seed101_raw.jsonl",
         "s202": "score_s1_seed202_raw.jsonl", "base": "score_base_raw.jsonl"}


def nap(p):
    d = {}
    for l in open(p, encoding="utf-8"):
        o = json.loads(l)
        if "bo_qua" not in o:
            d[(o["episode_id"], o["step_id"])] = o
    return d


def err(o):
    """Sai số bộ trỏ theo công thức cổng A: khoảng cách chia BỀ NGANG, tính %."""
    dx = abs(o["pred_xy"][0] - o["gold_xy"][0]) / o["wh"][0]
    dy = abs(o["pred_xy"][1] - o["gold_xy"][1]) / o["wh"][0]
    return math.hypot(dx, dy) * 100


def mcnemar(K, A, B):
    b = sum(1 for k in K if A[k]["executable"] == 1 and B[k]["executable"] == 0)
    c = sum(1 for k in K if A[k]["executable"] == 0 and B[k]["executable"] == 1)
    n = b + c
    chi = (abs(b - c) - 1) ** 2 / n if n else 0.0
    return b, c, n, chi, (math.erfc(math.sqrt(chi / 2)) if n else 1.0)


def ty(K, d, key="executable"):
    return sum(d[k][key] for k in K) / max(len(K), 1) * 100


def main():
    D = {k: nap(os.path.join(R, v)) for k, v in NHANH.items()}
    K = sorted(set.intersection(*[set(v) for v in D.values()]))
    print(f"bốn nhánh, giao nhau {len(K)} bước\n")

    # ── A ───────────────────────────────────────────────────────────────────────────
    print("═" * 78)
    print("A. BẢNG BỐN NHÁNH")
    print("═" * 78)
    for n in ["tran", "s101", "s202", "base"]:
        print(f"  {n:6s} exec {ty(K, D[n]):5.2f}%  ·  voronoi {ty(K, D[n], 'hit_voronoi'):5.2f}%"
              f"  ·  đĩa {ty(K, D[n], 'hit_disk'):5.2f}%  ·  thao tác {ty(K, D[n], 'action_ok'):6.2f}%")
    tb = (ty(K, D["s101"]) + ty(K, D["s202"])) / 2
    print(f"\n  S1 trung bình hai hạt giống: {tb:.2f}%")
    print(f"  S1 − Base = {tb - ty(K, D['base']):+.2f} pp  ·  trần − S1 = {ty(K, D['tran']) - tb:+.2f} pp")
    print(f"  S1 đạt {tb/ty(K, D['tran'])*100:.1f}% của trần, lấp {(tb-ty(K,D['base']))/(ty(K,D['tran'])-ty(K,D['base']))*100:.0f}% khoảng Base→trần")

    # ── B ───────────────────────────────────────────────────────────────────────────
    print("\n" + "═" * 78)
    print("B. LÁT CẮT CHẨN ĐOÁN — có TÁI LẬP ở hạt giống thứ hai không?")
    print("═" * 78)
    lat = {}
    for k in K:
        o = D["s101"][k]
        a = o.get("app_seen_in_train")
        lat.setdefault("app đã thấy" if a is True else
                       ("app CHƯA thấy" if a is False else "không gán được app"), []).append(k)
        lat.setdefault("màn ít nút (<40)" if o["n_buttons"] < 40 else
                       ("màn vừa (40-80)" if o["n_buttons"] <= 80 else "màn dày (>80)"), []).append(k)
    print(f"  {'lát':22s} {'n':>5s} {'s101':>7s} {'s202':>7s} {'lệch':>6s} {'Base':>7s} "
          f"{'s101−B':>7s} {'s202−B':>7s}")
    for ten, KK in lat.items():
        e1, e2, eb = ty(KK, D["s101"]), ty(KK, D["s202"]), ty(KK, D["base"])
        print(f"  {ten:22s} {len(KK):5d} {e1:6.1f}% {e2:6.1f}% {e2-e1:+6.1f} {eb:6.1f}% "
              f"{e1-eb:+7.1f} {e2-eb:+7.1f}")
    print("  ⇒ cột 's101−B' và 's202−B' phải cùng dấu và gần nhau thì lát cắt mới tái lập")

    # ── C ───────────────────────────────────────────────────────────────────────────
    print("\n" + "═" * 78)
    print("C. TRẦN CÓ PHẢI TRẦN THEO TỪNG BƯỚC KHÔNG?")
    print("═" * 78)
    for n in ["s101", "s202", "base"]:
        v = [k for k in K if D[n][k]["executable"] == 1 and D["tran"][k]["executable"] == 0]
        print(f"  {n:5s} trúng ở bước câu NGƯỜI trượt: {len(v):4d} = {len(v)/len(K):5.2%}")
    ca = [k for k in K if D["tran"][k]["executable"] == 0
          and any(D[n][k]["executable"] == 1 for n in ["s101", "s202", "base"])]
    print(f"  ít nhất một mô hình trúng ở bước người trượt: {len(ca)} = {len(ca)/len(K):.2%}")
    print("  ⇒ trần là mức TỔNG, KHÔNG phải cận trên theo từng bước. Phải nói rõ trong bài.")

    # ── D ───────────────────────────────────────────────────────────────────────────
    print("\n" + "═" * 78)
    print("D. HỢP CỦA BỐN NHÁNH — vùng mù THẬT của dụng cụ")
    print("═" * 78)
    hop = [k for k in K if any(D[n][k]["executable"] == 1 for n in D)]
    print(f"  ít nhất một nhánh giải được : {len(hop)/len(K):5.2%}")
    print(f"  trần (chỉ câu người)        : {ty(K, D['tran']):5.2f}%")
    print(f"  ⇒ vùng mù thật {100-len(hop)/len(K)*100:.1f}%, không phải {100-ty(K,D['tran']):.1f}%")

    # ── E ───────────────────────────────────────────────────────────────────────────
    print("\n" + "═" * 78)
    print("E. PHẦN QUẦN THỂ CÓ THỂ PHÂN GIẢI ĐƯỢC")
    print("═" * 78)
    print("  Ở bước mà hai nhánh viết câu khác hẳn nhau nhưng bộ trỏ vẫn trả về CÙNG một điểm,")
    print("  bước đó KHÔNG BAO GIỜ phân biệt được hai nhánh. Nó cho CẬN TRÊN của phần quần thể")
    print("  mà thước có thể dùng để phân giải — mọi chênh lệch quan sát được dồn vào phần đó.")
    print("  ⚠ KHÔNG đọc thành 'sàn': điểm trùng phần lớn là do CẢ HAI câu đều đúng.\n")
    for a, b in [("tran", "base"), ("tran", "s101"), ("s101", "base"), ("s101", "s202")]:
        kk = [k for k in K if D[a][k]["sent"].strip() != D[b][k]["sent"].strip()]
        trung = [k for k in kk
                 if math.dist(D[a][k]["pred_xy"], D[b][k]["pred_xy"]) / D[a][k]["wh"][0] * 100 < 1.0]
        khac = [k for k in kk if k not in set(trung)]
        h = ty(K, D[a]) - ty(K, D[b])
        print(f"  {a:5s} vs {b:5s}: câu khác {len(kk):4d} · điểm TRÙNG {len(trung)/len(kk):5.1%}"
              f" (đúng {ty(trung, D[a]):4.1f}%) · điểm KHÁC {len(khac)/len(kk):5.1%}"
              f" → chênh {h:+5.1f} pp dồn vào đây thành {h/(len(khac)/len(kk)):+5.1f} pp")
    n4 = [k for k in K if len({D[n][k]["sent"].strip() for n in D}) == 4]
    g4 = [k for k in n4 if max(math.dist(D[x][k]["pred_xy"], D[y][k]["pred_xy"])
                               for x in D for y in D) / D["tran"][k]["wh"][0] * 100 < 1.0]
    print(f"\n  {len(n4)} bước cả BỐN câu khác nhau → {len(g4)} = {len(g4)/len(n4):.1%} "
          f"cho bốn điểm trùng nhau (đúng {ty(g4, D['tran']):.1f}%)")
    print(f"  ⇒ nhiều nhất {100-len(g4)/len(n4)*100:.0f}% quần thể có khả năng phân giải bốn nhánh")

    # ── F ───────────────────────────────────────────────────────────────────────────
    print("\n" + "═" * 78)
    print("F. BƯỚC MỌI NHÁNH ĐỀU TRƯỢT")
    print("═" * 78)
    rot = [k for k in K if all(D[n][k]["executable"] == 0 for n in D)]
    print(f"  {len(rot)} = {len(rot)/len(K):.1%} bước không nhánh nào giải được")
    bc = [k for k in rot if err(D["tran"][k]) > 14]
    print(f"  trong đó bộ trỏ 'bỏ cuộc' (sai > 14% bề ngang) ở nhánh trần: "
          f"{len(bc)} = {len(bc)/len(rot):.1%}")
    print(f"  số nút trung vị ở nhóm này {st.median(D['tran'][k]['n_buttons'] for k in rot):.0f}"
          f" · toàn tập {st.median(D['tran'][k]['n_buttons'] for k in K):.0f}")

    # ── G ───────────────────────────────────────────────────────────────────────────
    print("\n" + "═" * 78)
    print("G. THIÊN VỊ ĐỘ DÀI — kiểm ở CẢ HAI hạt giống")
    print("═" * 78)
    for n in ["tran", "s101", "s202", "base"]:
        m = st.median(len(D[n][k]["sent"]) for k in K)
        dai = [k for k in K if len(D[n][k]["sent"]) > m]
        ngan = [k for k in K if len(D[n][k]["sent"]) <= m]
        print(f"  {n:5s} trung vị {m:3.0f} ký tự · câu dài {ty(dai, D[n]):5.1f}% · "
              f"câu ngắn {ty(ngan, D[n]):5.1f}% · lệch {ty(dai,D[n])-ty(ngan,D[n]):+5.1f} pp")
    print("  ⇒ dấu KHÔNG giống nhau giữa các nhánh ⇒ không phải quy luật chung của thước")

    # ── H ───────────────────────────────────────────────────────────────────────────
    print("\n" + "═" * 78)
    # ⚠ khoá cụm phải TRÙNG KHÍT `score_run.py:645` — `app` nếu có, không thì mã TÁC VỤ
    # (`ep{episode_id}`), KHÔNG phải từng bước. Dùng luật khác cho ra 2.906 cụm thay vì 1.091
    # và mọi con số thắng-hoà-thua lệch hẳn.
    print("H. THẮNG-HOÀ-THUA THEO CỤM (luật đã đăng ký: app, không có thì mã tác vụ)")
    print("═" * 78)
    for n in ["s101", "s202"]:
        cl = {}
        for k in K:
            a = (D[n][k].get("app") or "") or f"ep{k[0]}"
            cl.setdefault(a, []).append(k)
        t = h = tu = 0
        for v in cl.values():
            x, y = ty(v, D[n]), ty(v, D["base"])
            t += x > y; tu += x < y; h += x == y
        print(f"  {n}: {len(cl)} cụm · thắng {t} · hoà {h} · thua {tu}")


if __name__ == "__main__":
    main()
