# -*- coding: utf-8 -*-
"""Phụ lục D — đổi `<desc>` thì CÂU có đổi không. Chạy từ GỐC kho, ~3 giây, 0 GPU.

    PYTHONIOENCODING=utf-8 python3 harness/phu_luc_d.py

⭐ Vì sao phụ lục này vẫn còn dù phương án ORPO tầng câu đã bị cắt: nó là bằng chứng cho việc cắt.
   Mọi lượt học ưu tiên của dự án giữ câu giống hệt nhau ở hai vế so sánh và chỉ đổi trường
   `<desc>`, mà `<desc>` bị cắt trước khi chấm. Nên hàm mất mát chưa bao giờ so hai CÂU khác nhau.

Số đi vào luận văn ch6 §sec:grpo.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
R = lambda p: os.path.join(HERE, "..", "runs", p)


def nap(p):
    o = {}
    for l in open(R(p), encoding="utf-8"):
        l = l.strip()
        if l:
            r = json.loads(l)
            o[(r["episode_id"], r["step_id"])] = r
    return o


def tach(raw):
    """Trả (desc, câu) từ trường raw. Không có khối khai báo thì desc rỗng."""
    raw = raw or ""
    m = re.search(r"(<desc>.*?</desc>)\s*\n?(.*)", raw, re.S)
    return (m.group(1).strip(), m.group(2).strip()) if m else ("", raw.strip())


def main():
    A = nap("preds_min_desc_seed101.jsonl")
    B = nap("grpo_point/preds_grpo_point_seed101.jsonl")
    K = sorted(set(A) & set(B))
    print(f"n = {len(K)}\n")

    dd = dc = dd_cgiong = dd_ckhac = diem_khac = 0
    for x in K:
        da, ca = tach(A[x].get("raw", ""))
        db, cb = tach(B[x].get("raw", ""))
        if da != db:
            dd += 1
            if ca == cb:
                dd_cgiong += 1
            else:
                dd_ckhac += 1
        if ca != cb:
            dc += 1
        pa = re.search(r"<point>(.*?)</point>", da)
        pb = re.search(r"<point>(.*?)</point>", db)
        if pa and pb and pa.group(1) != pb.group(1):
            diem_khac += 1

    print(f"  <desc> KHÁC nhau          : {dd:5d}  ({100*dd/len(K):5.2f}%)")
    print(f"  riêng ô <point> KHÁC nhau : {diem_khac:5d}  ({100*diem_khac/len(K):5.2f}%)")
    print(f"  CÂU khác nhau             : {dc:5d}  ({100*dc/len(K):5.2f}%)\n")
    print(f"  Trong {dd} bước <desc> đã khác:")
    print(f"    -> CÂU vẫn Y HỆT         : {dd_cgiong:5d}  ({100*dd_cgiong/dd:5.2f}%)")
    print(f"    -> CÂU cũng đổi theo     : {dd_ckhac:5d}  ({100*dd_ckhac/dd:5.2f}%)")

    S = nap("preds_s1_seed101.jsonl")
    KS = sorted(set(A) & set(S))
    kh = sum(1 for x in KS if tach(A[x].get("raw", ""))[1] != tach(S[x].get("raw", ""))[1])
    print(f"\n  [đối chiếu] MIN vs S1: CÂU khác nhau {kh}/{len(KS)} = {100*kh/len(KS):.2f}%")
    print("    <- hai công thức train KHÁC nhau thì câu đổi gần hết")

    print("\n⭐ Đọc cho đúng. Con số ở dòng 'CÂU vẫn Y HỆT' là *trong số bước ĐÃ đổi khai báo, bao")
    print("   nhiêu phần trăm giữ nguyên từng ký tự của câu* — KHÔNG phải 'đổi khai báo ở ngần ấy")
    print("   phần trăm số bước'. Hai bản trước của `151` ghi lẫn hai đại lượng đó.")
    print("\n⚠️ Không quy nhân quả từ bảng này: GRPO khác MIN ở TOÀN BỘ trọng số, nên số bước câu")
    print("   đổi không chứng minh là DO khai báo đổi. Phép tách sạch cần ép sẵn phần <desc> ở đầu")
    print("   chuỗi sinh trên cùng một điểm lưu, ~2-3 h T4 và không cần train gì.")


if __name__ == "__main__":
    main()
