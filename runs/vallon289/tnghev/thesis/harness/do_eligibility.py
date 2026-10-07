# -*- coding: utf-8 -*-
"""Đo cổng eligibility cho cặp quy chiếu tối thiểu — KHÔNG cần GPU, KHÔNG cần ảnh.

In CẢ HAI thiết kế cạnh nhau, luôn luôn, không có cờ để tắt bớt một cái. Lý do:
dự án đã hai lần nới ngưỡng sau khi thấy số, nên bất cứ thứ gì cho phép chọn cách
đo có lợi hơn đều bị bỏ khỏi mã này.

  · TẦNG CÂU     (FINAL_SOLUTION Mục 12.2) — rejected là câu người bị đổi tên phần tử.
                 Ràng buộc ngặt nhất: tên phải xuất hiện literal trong câu người.
  · TẦNG KHAI BÁO (MIN-DESC) — rejected là `desc_neg` đã dựng sẵn bởi nearest_other().
                 Câu giữ nguyên; chỉ ô <desc> đổi. Không cần tên nằm trong câu.

Cả hai đều báo CẬN TRÊN: chưa trừ audit bằng chứng OCR/a11y, parent/child,
action-compatible.
"""
import json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DESC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    HERE, "dg1_cache", "train_ac", "descriptors.jsonl")

LO, HI = 80.0, 350.0
STOP = {"the","a","an","of","to","in","on","at","for","and","or","is","it","this","that"}
PT = re.compile(r"<point>\s*(\d+)\s*,\s*(\d+)\s*</point>")


def chuan(s):
    s = unicodedata.normalize("NFKC", s or "").lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def o_ten(desc):
    """Lấy ô tên khỏi <desc>role | name | <point>..</point> | hint</desc>."""
    o = (desc or "").split("|")
    return o[1].strip() if len(o) >= 2 else ""


def khop(ten, cau, muc):
    """muc='chat': cả tên nằm trong câu. muc='noi': HỢP của chặt và luật 2-gram —
    phải là hợp, vì tên một-từ chỉ khớp được bằng luật chặt."""
    t, c = chuan(ten), chuan(cau)
    if not t or not c:
        return False
    if t in c:
        return True
    if muc == "chat":
        return False
    tu = [w for w in t.split() if w not in STOP and len(w) > 2]
    return any(f"{tu[i]} {tu[i+1]}" in c for i in range(len(tu) - 1))


def bang(ten_bang, cot, phieu, n):
    print(f"\n{ten_bang}")
    print(f"{'phễu (cộng dồn)':<34}" + "".join(f"{c:>13}" for c in cot))
    print("-" * (34 + 13 * len(cot)))
    for k, nhan in phieu:
        print(f"{nhan:<34}" + "".join(f"{d[k]:>7} {100*d[k]/n:>4.1f}%" for d in bang.dat))
    print("-" * (34 + 13 * len(cot)))


def main():
    rows = [json.loads(l) for l in open(DESC, encoding="utf-8")]
    n = len(rows)

    # ── TẦNG CÂU ──────────────────────────────────────────────────────────────
    ket_cau = {}
    for muc in ("chat", "noi"):
        d = {k: 0 for k in ("co_ten","ten_trong_cau","co_neg","kc_dung",
                            "ten_khac","khong_trung","cung_role","do_dai")}
        for r in rows:
            ten = (r.get("name") or "").strip()
            if not ten or ten == "(no name)":
                continue
            d["co_ten"] += 1
            if not khop(ten, r.get("target_instruction",""), muc):
                continue
            d["ten_trong_cau"] += 1
            tn = o_ten(r.get("desc_neg"))
            if not tn:
                continue
            d["co_neg"] += 1
            kc = r.get("neighbor_dist_px")
            if kc is None or not (LO <= float(kc) <= HI):
                continue
            d["kc_dung"] += 1
            if chuan(tn) == chuan(ten):
                continue
            d["ten_khac"] += 1
            if r.get("dup_name"):
                continue
            d["khong_trung"] += 1
            if not r.get("same_role"):
                continue
            d["cung_role"] += 1
            if abs(len(chuan(ten).split()) - len(chuan(tn).split())) > 2:
                continue
            d["do_dai"] += 1
        ket_cau[muc] = d

    # ── TẦNG KHAI BÁO ─────────────────────────────────────────────────────────
    kd = {k: 0 for k in ("co_desc","co_neg","khac_nhau","ten_khac","point_khac",
                         "kc_dung","kc_bat_ky")}
    for r in rows:
        d0, dn = r.get("desc"), r.get("desc_neg")
        if not d0:
            continue
        kd["co_desc"] += 1
        if not dn:
            continue
        kd["co_neg"] += 1
        if d0.strip() == dn.strip():
            continue
        kd["khac_nhau"] += 1
        if chuan(o_ten(d0)) == chuan(o_ten(dn)):
            continue
        kd["ten_khac"] += 1
        m0, mn = PT.search(d0), PT.search(dn)
        if not m0 or not mn or m0.group(0) == mn.group(0):
            continue
        kd["point_khac"] += 1
        kd["kc_bat_ky"] += 1
        kc = r.get("neighbor_dist_px")
        if kc is None or not (LO <= float(kc) <= HI):
            continue
        kd["kc_dung"] += 1

    # ── in ────────────────────────────────────────────────────────────────────
    print(f"Nguồn: {DESC}")
    print(f"Số bước chạm có descriptor: {n}")

    print(f"\n[A] TẦNG CÂU — FINAL_SOLUTION Mục 12.2")
    print(f"{'phễu (cộng dồn)':<34}{'chặt':>13}{'nới':>13}")
    print("-" * 60)
    for k in ("co_ten","ten_trong_cau","co_neg","kc_dung","ten_khac",
              "khong_trung","cung_role","do_dai"):
        a, b = ket_cau["chat"][k], ket_cau["noi"][k]
        print(f"{k:<34}{a:>7} {100*a/n:>4.1f}%{b:>7} {100*b/n:>4.1f}%")
    print("-" * 60)
    for muc, nhan in (("chat","chặt"), ("noi","nới")):
        v = ket_cau[muc]["do_dai"]; t = 100*v/n
        print(f"  eligibility ({nhan:>4}): {v:6d}/{n} = {t:5.2f}%  "
              f"{'ĐẠT' if t >= 25 else '⛔ DƯỚI'} cổng 25%")

    print(f"\n[B] TẦNG KHAI BÁO — MIN-DESC (desc vs desc_neg)")
    print(f"{'phễu (cộng dồn)':<34}{'n':>13}")
    print("-" * 47)
    for k in ("co_desc","co_neg","khac_nhau","ten_khac","point_khac","kc_dung"):
        print(f"{k:<34}{kd[k]:>7} {100*kd[k]/n:>4.1f}%")
    print("-" * 47)
    for k, nhan in (("kc_dung","có lọc 80–350 px"), ("kc_bat_ky","không lọc khoảng cách")):
        t = 100*kd[k]/n
        print(f"  eligibility ({nhan}): {kd[k]:6d}/{n} = {t:5.2f}%  "
              f"{'ĐẠT' if t >= 25 else '⛔ DƯỚI'} cổng 25%")

    print("\n⚠️ Cả hai là CẬN TRÊN. Ba điều kiện chưa trừ, đều chỉ làm số GIẢM:")
    print("   bằng chứng hiển thị OCR/a11y đã audit · loại parent/child và các đường")
    print("   bấm cùng hành động · negative phải action-compatible.")


if __name__ == "__main__":
    main()
