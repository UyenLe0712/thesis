# -*- coding: utf-8 -*-
"""Phụ lục C — TỰ PHẢN BIỆN trần phương pháp. Chạy từ GỐC kho, ~5 giây, 0 GPU.

    PYTHONIOENCODING=utf-8 python3 harness/phu_luc_c.py

⭐ Đây là script quan trọng nhất về mặt phương pháp luận trong cả hồ sơ: nó bắt được một trần mà
   chính `report/151` vừa viết ra ở bản nháp. Trước khi tin BẤT KỲ trần nào suy từ một lát chọn
   theo hành vi mô hình, hãy chạy lại nó với ít nhất một định nghĩa lát khác.

Nghi vấn: lát được định nghĩa bằng chính kênh A CỦA MIN, mà kênh A và câu của MIN đến từ cùng một
lượt sinh nên chia nhiều thành phần nhiễu chung. Chọn bước có A(MIN) sai là chọn đúng những bước
MIN gặp bất lợi, nên MIN bị thiệt một cách hệ thống khi so với nhánh khác trên lát đó. Đây đúng là
bẫy chọn mẫu đã giết phương án `gui_sft_match` (trần 65,44 so với phản thực tế 59,44).

Ba phép kiểm, mỗi cái bỏ bớt một phần của việc chọn theo hành vi MIN:
  1. đổi sang lát định nghĩa bằng A của GRPO  -> bớt chọn trực tiếp trên MIN
  2. lấy phần A(GRPO) sai mà A(MIN) đúng      -> bỏ hẳn việc chọn theo lỗi của MIN
  3. lát định nghĩa bằng độ khó ĐỌC LẬP với mô hình (số phần tử có thể chạm)

Kết quả đi vào luận văn ch6 §sec:tranlat, Bảng tab:tranlat.
"""
import json, os, re, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
R = lambda p: os.path.join(HERE, "..", "runs", p)
CHIA, DUNG_SAI = 1000.0, 0.14


def nap(p):
    o = {}
    for l in open(R(p), encoding="utf-8"):
        l = l.strip()
        if l:
            r = json.loads(l)
            o[(r["episode_id"], r["step_id"])] = r
    return o


def d14(p, g, wh):
    if not p or not g or not wh:
        return 0
    return int(abs(p[0] - g[0]) <= DUNG_SAI * wh[0] and abs(p[1] - g[1]) <= DUNG_SAI * wh[1])


def tu_khai(rp, wh):
    if not rp:
        return None
    m = re.search(r"<point>\s*([\d.]+)\s*,\s*([\d.]+)\s*</point>", rp.get("raw", "") or "")
    return None if not m else (float(m.group(1)) / CHIA * wh[0], float(m.group(2)) / CHIA * wh[1])


def main():
    D = {"MIN": nap("score_min_desc_seed101_raw.jsonl"),
         "S1": nap("score_s1_seed101_raw.jsonl"),
         "GRPO": nap("grpo_point/score_grpo_point_seed101_raw.jsonl"),
         "nguoi": nap("score_ceiling_human_raw.jsonl")}
    P = {"MIN": nap("preds_min_desc_seed101.jsonl"),
         "GRPO": nap("grpo_point/preds_grpo_point_seed101.jsonl")}
    REF = D["MIN"]
    EX = lambda n, x: int(D[n][x].get("executable", 0) or 0)

    K = [x for x in sorted(set.intersection(*[set(v) for v in D.values()]))
         if REF[x].get("gold_xy") and tu_khai(P["MIN"].get(x), REF[x]["wh"])
         and tu_khai(P["GRPO"].get(x), REF[x]["wh"])]
    G = lambda x: (REF[x]["gold_xy"], REF[x]["wh"])
    AM = {x: d14(tu_khai(P["MIN"][x], REF[x]["wh"]), *G(x)) for x in K}
    AG = {x: d14(tu_khai(P["GRPO"][x], REF[x]["wh"]), *G(x)) for x in K}
    mT = 100 * st.mean([EX("MIN", x) for x in K])
    print(f"n = {len(K)}\n")

    nb = sorted(K, key=lambda x: -(REF[x].get("n_buttons") or 0))
    LAT = [("A(MIN) sai  [CÁCH ĐANG DÙNG — nghi thiên vị]", [x for x in K if not AM[x]]),
           ("A(GRPO) sai [bớt chọn trực tiếp trên MIN]", [x for x in K if not AG[x]]),
           ("A(GRPO) sai VÀ A(MIN) đúng [không chọn theo lỗi MIN]",
            [x for x in K if not AG[x] and AM[x]]),
           ("30% màn ĐÔNG NÚT nhất [độc lập mô hình]", nb[:int(.30 * len(K))])]

    print(f"  {'lát':<52}{'n':>6}{'MIN':>8}{'S1':>8}{'S1-MIN':>9}{'người':>8}{'trần ORPO':>11}")
    for ten, L in LAT:
        if not L:
            continue
        S = set(L)
        m, s, h = (100 * st.mean([EX(n, x) for x in L]) for n in ("MIN", "S1", "nguoi"))
        tran = 100 * st.mean([EX("S1", x) if x in S else EX("MIN", x) for x in K])
        print(f"  {ten:<52}{len(L):>6}{m:>8.2f}{s:>8.2f}{s-m:>+9.2f}{h:>8.2f}{tran-mT:>+11.2f}")

    print()
    for ten, L in LAT[:2]:
        S = set(L)
        tran = 100 * st.mean([EX("S1", x) if x in S else EX("MIN", x) for x in K])
        nhan = "A(MIN)" if "A(MIN) sai " in ten else "A(GRPO)"
        print(f"  trần ORPO định nghĩa bằng {nhan:<8} = {tran:6.2f}  ({tran-mT:+.2f} pp)")

    print("\n⭐ Đọc kết quả: cột trần ORPO giảm từ +4,80 xuống +2,88 rồi đổi dấu tuỳ cách định nghĩa")
    print("   lát, trong khi cột người gần như không đổi. Đại lượng trôi theo định nghĩa lát là")
    print("   ƯU THẾ GIỮA HAI MÔ HÌNH CÙNG HỌ, còn dư địa so với người thì đứng yên. Đó là chữ ký")
    print("   của hiệu ứng chọn mẫu, và là lý do phương án ORPO tầng câu bị cắt ở `151` mục 2.1.")


if __name__ == "__main__":
    main()
