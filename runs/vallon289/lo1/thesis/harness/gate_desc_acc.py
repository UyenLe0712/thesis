# -*- coding: utf-8 -*-
"""Cổng cơ học của MIN-DESC — đo độ chính xác ô KHAI BÁO, KHÔNG gọi bộ trỏ.

Vì sao cần: report/106 mục (x6) cấm dùng UGround/UI-Venus để quyết định bất cứ điều gì
trước khi mọi checkpoint đóng băng. Nhưng vẫn phải biết lượt train có đi đúng hướng không.
Ô `<desc>` mà model tự sinh có thể đối chiếu thẳng với nhãn vàng của tập kiểm — không cần
bộ trỏ, không tiêu quota Kaggle, và nó đo ĐÚNG thứ MIN-DESC được thiết kế để sửa.

    python3 harness/gate_desc_acc.py runs/preds_s2_seed101.jsonl [preds_khac.jsonl ...]

Cột `cả hai đúng` là con số phải theo dõi: bảng chẩn đoán ở report/117 Mục 1 cho thấy nhóm
đó chạy 87,1% executability, còn nhóm cả-hai-sai chỉ 5,6%. Mỗi bước kéo được từ nhóm dưới
lên nhóm trên đáng ~81 điểm cho bước đó.
"""
import json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = os.path.join(HERE, "dg1_cache", "test_ac", "descriptors.jsonl")
TAU  = 0.14                      # cùng dung sai với metric_exec.hit_disk
PT   = re.compile(r"<point>\s*(\d+)\s*,\s*(\d+)\s*</point>")


def chuan(s):
    s = unicodedata.normalize("NFKC", s or "").lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def o_ten(d):
    o = (d or "").split("|")
    return o[1].strip() if len(o) >= 2 else ""


def nap_gold():
    g = {}
    for l in open(GOLD, encoding="utf-8"):
        d = json.loads(l)
        g[(d["episode_id"], d["step_id"])] = d
    return g


def khoa_cham_duoc(path, gold):
    """Tập bước mà tệp preds này chấm được: có trong preds VÀ có tên vàng."""
    ra = set()
    for l in open(path, encoding="utf-8"):
        r = json.loads(l)
        k = (r["episode_id"], r["step_id"])
        g = gold.get(k)
        if g is None:
            continue
        gt = chuan(g.get("name") or "")
        if gt and gt != "no name":
            ra.add(k)
    return ra


def do(path, gold, chung):
    n = co_desc = ten_ok = pt_ok = ca_hai = 0
    for l in open(path, encoding="utf-8"):
        r = json.loads(l)
        k = (r["episode_id"], r["step_id"])
        if k not in chung:          # chỉ chấm trên GIAO của mọi tệp — xem ghi chú ở main()
            continue
        g = gold.get(k)
        if g is None:
            continue
        gt = chuan(g.get("name") or "")
        if not gt or gt == "no name":
            continue                       # không có tên vàng thì không chấm được ô tên
        n += 1
        raw = r.get("raw", "")
        if "<desc>" not in raw:
            continue
        co_desc += 1
        d = raw.split("<desc>", 1)[1].split("</desc>", 1)[0]
        pt_ten = chuan(o_ten(d))
        t_ok = bool(pt_ten) and (pt_ten == gt or pt_ten in gt or gt in pt_ten)
        m = PT.search(d)
        p_ok = False
        if m and g.get("point_norm"):
            gx, gy = g["point_norm"]        # hệ norm1000, cùng hệ với ô <point>
            p_ok = abs(int(m.group(1)) - gx) <= TAU*1000 and abs(int(m.group(2)) - gy) <= TAU*1000
        ten_ok += t_ok; pt_ok += p_ok; ca_hai += (t_ok and p_ok)
    return n, co_desc, ten_ok, pt_ok, ca_hai


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    gold = nap_gold()
    ton = [p for p in sys.argv[1:] if os.path.exists(p)]
    # ⚠️ GHÉP CẶP. Các tệp preds có thể phủ số bước khác nhau — ví dụ mốc S2 chấm đủ 6.958
    # bước còn checkpoint mới chỉ sinh `--limit 600`. Chấm mỗi tệp trên quần thể riêng rồi
    # trừ nhau là so hai thứ khác nhau: chênh lệch khi đó lẫn cả khác biệt độ khó giữa hai
    # lát. Nên siết về ĐÚNG GIAO của mọi tệp, để hiệu số là hiệu ghép cặp trên cùng bước.
    chung = None
    for p in ton:
        k = khoa_cham_duoc(p, gold)
        chung = k if chung is None else (chung & k)
    chung = chung or set()
    print(f"nhãn vàng: {len(gold)} bước · dung sai ô point: ±{TAU*100:.0f}% cạnh")
    print(f"GIAO của {len(ton)} tệp preds: {len(chung)} bước — mọi cột chấm trên đúng tập này\n")
    hdr = f"{'tệp preds':<34}{'n':>7}{'sinh desc':>11}{'tên đúng':>10}{'point đúng':>12}{'CẢ HAI':>9}"
    print(hdr); print("-"*len(hdr))
    mocs = []
    for p in sys.argv[1:]:
        if not os.path.exists(p):
            print(f"{os.path.basename(p):<34}  ⛔ không thấy tệp"); continue
        n, cd, t, q, ch = do(p, gold, chung)
        if n == 0:
            print(f"{os.path.basename(p):<34}  ⛔ 0 bước đối chiếu được"); continue
        mocs.append((os.path.basename(p), 100*ch/n))
        print(f"{os.path.basename(p):<34}{n:>7}{100*cd/n:>10.1f}%{100*t/n:>9.1f}%"
              f"{100*q/n:>11.1f}%{100*ch/n:>8.1f}%")
    if len(mocs) >= 2:
        (ta, va), (tb, vb) = mocs[0], mocs[-1]
        print("-"*len(hdr))
        print(f"Δ 'cả hai đúng' ({tb} − {ta}) = {vb-va:+.2f} pp")
        print("\nĐọc: DƯƠNG ⇒ MIN-DESC nhận diện phần tử tốt hơn mốc — đúng cơ chế đã đặt cược.")
        print("     ÂM    ⇒ lượt train làm hỏng khả năng nhận diện. Nghi LR quá cao (x3b);")
        print("             dừng, đừng chạy hạt giống 202, báo lại.")
    print("\n⛔ Đây KHÔNG phải executability và KHÔNG thay thế nó. Nó chỉ là cổng cơ học")
    print("   không-cần-bộ-trỏ theo (x6). Chấm 4.463 vẫn làm MỘT lần, sau khi đóng băng.")


if __name__ == "__main__":
    main()
