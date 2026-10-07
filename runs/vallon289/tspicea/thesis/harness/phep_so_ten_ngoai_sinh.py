# -*- coding: utf-8 -*-
"""Phép so ngoại sinh: ô TÊN của nhãn tự động vs câu chỉ dẫn do người viết.

Đây là phép kiểm duy nhất của bài VCL dùng tới một nguồn nằm hẳn ngoài đường
dựng nhãn. Đường dựng nhãn không đọc `target_instruction` ở bất kỳ khâu nào
(vai trò, tên, toạ độ, dấu hiệu đều tính từ cây trợ năng, hộp bao và OCR), nên
việc ô tên trùng với chữ người viết là bằng chứng ngoại sinh, không phải tự kiểm.

Luật so (khoá lại ở đây vì bài trích con số này):
  - quần thể: các bước tập kiểm có tên, tức tier thuộc {ten_ro, ky_hieu};
  - chuẩn hoá: hạ chữ thường rồi BỎ HẾT khoảng trắng ở cả hai vế. Bỏ khoảng
    trắng là cần, vì OCR nuốt dấu cách ở một số nhãn nút ("Turnon");
  - khớp: chuỗi tên chuẩn hoá là chuỗi con của câu chuẩn hoá.

Đối chứng lệch một bước: đem đúng những cái tên ấy ghép với câu của bước liền
sau. Script in cả ba định nghĩa "bước liền sau" vì chúng không cho cùng một số,
và bài phải nêu định nghĩa nào đã dùng.

Chạy:  PYTHONIOENCODING=utf-8 python3 harness/phep_so_ten_ngoai_sinh.py
"""
import io, json, math, os, re, sys

FILE = os.path.join(os.path.dirname(__file__), "dg1_cache", "test_ac", "descriptors.jsonl")


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z / d * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return 100 * (c - h), 100 * (c + h)


def chuan_hoa(s):
    return re.sub(r"\s+", "", str(s).lower())


def khop(ten, cau):
    return chuan_hoa(ten) in chuan_hoa(cau)


def main():
    rows = [json.loads(l) for l in io.open(FILE, encoding="utf-8")]
    co_ten = [r for r in rows if r.get("name") and r["tier"] in ("ten_ro", "ky_hieu")]
    n = len(co_ten)
    assert n == 3505, "quan the doi 3.505 buoc co ten, dang co %d" % n

    k = sum(1 for r in co_ten if khop(r["name"], r["target_instruction"]))
    lo, hi = wilson(k, n)
    print("KHOP THAT      : %d/%d = %.2f%%  KTC95 [%.1f . %.1f]" % (k, n, 100 * k / n, lo, hi))
    assert abs(100 * k / n - 53.5) < 0.05, "con so 53,5%% trong bai khong tai lap duoc"

    theo_khoa = {(r["episode_id"], r["step_id"]): r for r in rows}
    vi_tri = {(r["episode_id"], r["step_id"]): i for i, r in enumerate(rows)}

    # a) dong ke tiep trong chinh quan the co ten
    a = [co_ten[(i + 1) % n]["target_instruction"] for i in range(n)]
    # b) dong ke tiep trong toan bo tep, ke ca buoc khong co ten
    b = [rows[(vi_tri[(r["episode_id"], r["step_id"])] + 1) % len(rows)]["target_instruction"]
         for r in co_ten]
    # c) dung buoc lien sau trong CUNG episode; bo qua buoc cuoi cua moi episode
    c = [(theo_khoa.get((r["episode_id"], r["step_id"] + 1)) or {}).get("target_instruction")
         for r in co_ten]

    for nhan, v in [("dong ke tiep trong quan the", a), ("dong ke tiep trong toan tep", b)]:
        kk = sum(1 for i, r in enumerate(co_ten) if khop(r["name"], v[i]))
        lo2, hi2 = wilson(kk, n)
        print("DOI CHUNG [%-28s]: %d/%d = %.2f%% [%.1f . %.1f]" % (nhan, kk, n, 100 * kk / n, lo2, hi2))
    nn = sum(1 for x in c if x)
    kk = sum(1 for i, r in enumerate(co_ten) if c[i] and khop(r["name"], c[i]))
    lo2, hi2 = wilson(kk, nn)
    print("DOI CHUNG [%-28s]: %d/%d = %.2f%% [%.1f . %.1f]" % ("buoc lien sau cung episode", kk, nn, 100 * kk / nn, lo2, hi2))

    print("\nChia theo tang ten:")
    for tang in ("ten_ro", "ky_hieu"):
        g = [r for r in co_ten if r["tier"] == tang]
        kg = sum(1 for r in g if khop(r["name"], r["target_instruction"]))
        print("  %-8s %d/%d = %.1f%%" % (tang, kg, len(g), 100 * kg / len(g)))


if __name__ == "__main__":
    main()
