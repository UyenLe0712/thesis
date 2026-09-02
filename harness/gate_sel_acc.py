# -*- coding: utf-8 -*-
"""Cổng G6 của sprint `gui_sel` — đo độ chính xác thẻ `<sel>`, KHÔNG gọi bộ trỏ.

Vì sao cần: `report/132` §5 đặt G6 làm cổng sau lượt train đầu. Nó đo ĐÚNG thứ nhánh
`gui_sel` được thiết kế để làm — chọn đúng một dòng trong khối ứng viên — mà không tiêu
một giây GPU chấm nào và không đụng tới bộ trỏ.

    python3 harness/gate_sel_acc.py runs/preds_gui_sel_seed101.jsonl

⛔ LUẬT (report/132 §5, mục 14 câu 5 để ngỏ ngưỡng — đừng tự nới):
  · đo trên **600 bước DEV** có ứng viên vàng, KHÔNG dùng tập test;
  · đúng = khớp TÊN (chuẩn hoá) ∧ điểm nằm trong ±140 trên lưới [0,1000];
  · `<sel>none</sel>` tính là SAI khi bước đó CÓ ứng viên vàng;
  · ngưỡng **≥ 63,6%**. Trượt ⇒ báo thẳng là cơ chế không học được, bài đổi thành báo cáo
    âm. KHÔNG nới ngưỡng sau khi thấy điểm — dự án đã tự khai hai lần làm vậy.

⛔ `gold_candidate()` ở `build_sel_data.py:43` là BẢN DUY NHẤT. File này **import lại** nó
   chứ không chép — hai bản chép rời nhau là cách chắc chắn nhất để dựng và chấm lệch nhau
   mà không ai thấy.
"""
import json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_sel_data as BS          # dùng chung gold_candidate(), không chép lại

TOL = BS.TOL                          # 140 trên lưới [0,1000] — cùng con số cổng G2
SEL = re.compile(r"<sel>(.*?)</sel>", re.S)
PT  = re.compile(r"<point>\s*(\d+)\s*,\s*(\d+)\s*</point>")
NGUONG = 0.636


def kh(r):
    """Khoá (episode, step) chuẩn hoá về CHUỖI ở mọi phía.

    Toàn bộ pipeline hiện ghi kiểu int, nhưng khớp hụt vì lệch kiểu là lỗi CÂM: cổng sẽ bỏ
    qua sạch mọi bước rồi vẫn in ra bảng trông bình thường. Ép chuỗi hai đầu là rẻ và chặn
    hẳn loại hỏng đó."""
    return str(r["episode_id"]), str(r["step_id"])


def chuan(s):
    s = unicodedata.normalize("NFKC", s or "").lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def tach_sel(txt):
    """(tên, x, y) từ thẻ <sel>; (None,None,None) nếu none/không có thẻ."""
    m = SEL.search(txt or "")
    if not m:
        return None, None, None
    noi = m.group(1).strip()
    if chuan(noi) == "none":
        return "none", None, None
    p = PT.search(noi)
    ten = PT.sub("", noi).strip()
    return ten, (int(p.group(1)) if p else None), (int(p.group(2)) if p else None)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    split = os.environ.get("SEL_SPLIT", "train")   # DEV cắt từ train, KHÔNG dùng test
    BS.D.set_split(split)
    R = BS.D.ROOT

    gold, cands = {}, {}
    for l in open(os.path.join(R, "descriptors.jsonl"), encoding="utf-8"):
        d = json.loads(l); gold[kh(d)] = d
    for l in open(os.path.join(R, "candidates.jsonl"), encoding="utf-8"):
        c = json.loads(l); cands[kh(c)] = c["cands"]

    for path in sys.argv[1:]:
        n = dung = co_the = ra_none = ten_ok = pt_ok = 0
        bo_qua = 0
        for l in open(path, encoding="utf-8"):
            r = json.loads(l)
            k = kh(r)
            g, cs = gold.get(k), cands.get(k)
            if not (g and g.get("name") and cs):
                bo_qua += 1; continue
            gx, gy = g["point_norm"]
            gc = BS.gold_candidate(cs, g["name"], gx, gy)
            if gc is None:                      # không có ứng viên vàng ⇒ ngoài phạm vi cổng
                bo_qua += 1; continue
            n += 1
            ten, x, y = tach_sel(r.get("pred") or r.get("prediction") or "")
            if ten is None:
                continue
            if ten == "none":
                ra_none += 1; continue          # CÓ ứng viên vàng mà trả none = SAI
            co_the += 1
            t_ok = chuan(ten) == chuan(gc["name"])
            p_ok = x is not None and abs(x - gc["x"]) <= TOL and abs(y - gc["y"]) <= TOL
            ten_ok += t_ok; pt_ok += p_ok
            dung += (t_ok and p_ok)

        print("=" * 70)
        print(os.path.basename(path))
        print(f"  bỏ qua (không có ứng viên vàng)     : {bo_qua}")
        if bo_qua and n == 0:
            print("  ⛔ BỎ QUA TOÀN BỘ — gần như chắc chắn LỆCH KHOÁ, không phải dữ liệu xấu.")
            print("     So thử: khoá preds vs khoá descriptors.jsonl.")
        print(f"  n trong phạm vi cổng                : {n}")
        if not n:
            print("  ⛔ không có bước nào chấm được"); continue
        print(f"  có phát thẻ <sel> khác none         : {co_the} = {co_the/n:.1%}")
        print(f"  trả <sel>none</sel> (tính SAI)      : {ra_none} = {ra_none/n:.1%}")
        print(f"  khớp TÊN                            : {ten_ok} = {ten_ok/n:.1%}")
        print(f"  điểm trong ±{TOL}                     : {pt_ok} = {pt_ok/n:.1%}")
        print(f"  ⭐ sel_acc (tên ∧ điểm)              : {dung}/{n} = {dung/n:.1%}"
              f"   {'✅ ĐẠT' if dung/n >= NGUONG else '⛔ TRƯỢT'} (ngưỡng {NGUONG:.1%})")


if __name__ == "__main__":
    main()
