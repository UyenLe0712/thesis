# -*- coding: utf-8 -*-
"""Bảng 2×2 tên × toạ độ của ô khai báo S2, KÈM cột Base và cột trần.

Vì sao thêm hai cột đó: bảng gốc ở `report/117` Mục 1 chỉ có S1 và S2, nên đòn phản biện
mạnh nhất — *"phân tầng hậu kiểm này chỉ đang đo độ khó của bước, chứ không đo tác dụng
của ô khai báo"* — không bác được bằng chính bảng ấy. Trần (câu chuẩn do người viết) là
mốc không phụ thuộc vào bất kỳ nhánh đã huấn luyện nào, nên nếu ô "cả hai sai" chỉ là
tập hợp các bước khó thì trần ở đó phải sụp theo. Nó không sụp.

    python3 harness/phan_tich_o_khai_bao.py

Luật khớp tên và dung sai ô point lấy nguyên của `gate_desc_acc.py` (khớp lỏng: bằng nhau
hoặc chứa nhau; ±14% cạnh) để bảng này so trực tiếp được với `report/117`.

⚠️ Vẫn là phân tầng HẬU KIỂM trên biến do chính nhánh điều trị sinh ra, và vẫn chỉ một
hạt giống. Cột trần thu hẹp lời giải thích "chỉ là bước khó", không xoá được nó.
"""
import json, os, re, statistics, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GOLD = os.path.join(HERE, "dg1_cache", "test_ac", "descriptors.jsonl")
TAU = 0.14
PT = re.compile(r"<point>\s*(\d+)\s*,\s*(\d+)\s*</point>")


def chuan(s):
    s = unicodedata.normalize("NFKC", s or "").lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def nap(path, key_only=False):
    d = {}
    for l in open(path, encoding="utf-8"):
        o = json.loads(l)
        d[(o["episode_id"], o["step_id"])] = o
    return d


def main():
    gold = nap(GOLD)
    pred = nap(os.path.join(ROOT, "runs", "preds_s2_seed101.jsonl"))
    S1 = nap(os.path.join(ROOT, "runs", "score_s1_seed101_raw.jsonl"))
    S2 = nap(os.path.join(ROOT, "runs", "score_s2_seed101_raw.jsonl"))
    B = nap(os.path.join(ROOT, "runs", "score_base_raw.jsonl"))
    H = nap(os.path.join(ROOT, "runs", "score_ceiling_human_raw.jsonl"))

    cells, nodesc = {}, []
    for k, g in gold.items():
        if k not in S2 or k not in S1:
            continue
        gt = chuan(g.get("name") or "")
        if not gt or gt == "no name":
            continue                      # không có tên vàng thì không chấm được ô tên
        raw = pred.get(k, {}).get("raw", "")
        if "<desc>" not in raw:
            nodesc.append(k)
            continue
        d = raw.split("<desc>", 1)[1].split("</desc>", 1)[0]
        o = d.split("|")
        pn = chuan(o[1].strip() if len(o) >= 2 else "")
        t_ok = bool(pn) and (pn == gt or pn in gt or gt in pn)
        m = PT.search(d)
        p_ok = False
        if m and g.get("point_norm"):
            gx, gy = g["point_norm"]
            p_ok = (abs(int(m.group(1)) - gx) <= TAU * 1000
                    and abs(int(m.group(2)) - gy) <= TAU * 1000)
        cells.setdefault((t_ok, p_ok), []).append(k)

    def ty(D, ks):
        return 100 * sum(D[k].get("executable", 0) for k in ks) / len(ks)

    hdr = f"{'tên':>6}{'point':>7}{'n':>7}{'Base':>7}{'S1':>7}{'S2':>7}{'Δ':>8}{'TRẦN':>7}{'nút':>6}"
    print(hdr); print("-" * len(hdr))
    for key in [(True, True), (True, False), (False, True), (False, False)]:
        ks = cells.get(key, [])
        if not ks:
            continue
        nb = statistics.median([S2[k].get("n_buttons", 0) for k in ks])
        print(f"{'đúng' if key[0] else 'sai':>6}{'trúng' if key[1] else 'trượt':>7}"
              f"{len(ks):>7}{ty(B,ks):>7.1f}{ty(S1,ks):>7.1f}{ty(S2,ks):>7.1f}"
              f"{ty(S2,ks)-ty(S1,ks):>8.2f}{ty(H,ks):>7.1f}{nb:>6.0f}")
    if nodesc:
        print(f"{'—':>6}{'không sinh desc':>7}"[:13]
              + f"{len(nodesc):>7}{ty(B,nodesc):>7.1f}{ty(S1,nodesc):>7.1f}"
              f"{ty(S2,nodesc):>7.1f}{ty(S2,nodesc)-ty(S1,nodesc):>8.2f}{ty(H,nodesc):>7.1f}")
    print("\nĐọc: ô cả-hai-sai có TRẦN vẫn cao (câu người vẫn giải được phần lớn) trong khi "
          "S2 rơi xuống dưới cả sàn của thước ⇒ không quy hết được cho độ khó của bước.")


if __name__ == "__main__":
    main()
