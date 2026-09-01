# -*- coding: utf-8 -*-
"""Hai con số mà bảng chéo 2x2 KHÔNG in ra — dựng cho vòng phản biện FAIR 31/8.

Bảng 2x2 ở `phan_tich_o_khai_bao.py` chỉ chấm được trên bước **có tên vàng**, nên nó
lặng lẽ bỏ ra ngoài hai nhóm. Giám khảo thống kê đợt C bắt đúng chỗ đó
(`report/129` mục A4 lỗi số 1 và 4). Script này in ra cả hai:

  (1) Ô bị loại: bước CÓ descriptor nhưng KHÔNG có tên vàng để đối chiếu.
      Bảng chéo không chứa được, mà nhóm này đi NGƯỢC dấu headline.
  (2) Phần bù của ô "cả hai đúng": tức toàn bộ phần "không nhận diện trọn vẹn".
      Bài từng viết nhầm phần bù này là -25,2 (đó là con số của riêng ô "cả hai sai").

    python3 harness/o_bi_loai_khoi_bang_cheo.py

Luật khớp tên và dung sai point lấy nguyên của `gate_desc_acc.py` / `phan_tich_o_khai_bao.py`
(khớp lỏng: bằng nhau hoặc chứa nhau; +-14% cạnh) để so trực tiếp được với bảng đang in.

Kết quả 31/8/2026, tái lập bốn ô của bảng chéo trùng khít bài
(+5,72 / +0,54 / +1,11 / -25,20):

  ô bị loại (có desc, không tên vàng)  n=881   Delta = +1,48 pp  KTC95 [-1,16 · +4,10]
  phần bù ô "cả hai đúng"              n=1374  Delta = -13,10 pp KTC95 [-15,39 · -10,77]

Cả hai đã vào `paper/fair2026/main.tex`. Vẫn là phân tầng HẬU KIỂM trên biến do chính
nhánh điều trị sinh ra, và vẫn một hạt giống.
"""
import json, os, random, re, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GOLD = os.path.join(HERE, "dg1_cache", "test_ac", "descriptors.jsonl")
TAU = 0.14
SEED = 20260805
NBOOT = 10000
PT = re.compile(r"<point>\s*(\d+)\s*,\s*(\d+)\s*</point>")


def chuan(s):
    s = unicodedata.normalize("NFKC", s or "").lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def nap(path):
    d = {}
    for l in open(path, encoding="utf-8"):
        o = json.loads(l)
        d[(o["episode_id"], o["step_id"])] = o
    return d


def ex(D, k):
    # score_run.py bỏ trường này ở bước câu rỗng; luật đã khoá là tính exec = 0.
    return D[k].get("executable", 0)


def boot(ks, S2, S1):
    """Bootstrap cụm theo episode — cùng luật với `mde_that.py`."""
    byep = {}
    for k in ks:
        byep.setdefault(k[0], []).append(k)
    eps = list(byep)
    rng = random.Random(SEED)
    out = []
    for _ in range(NBOOT):
        kk = [k for e in (rng.choice(eps) for _ in eps) for k in byep[e]]
        out.append(100 * sum(ex(S2, k) - ex(S1, k) for k in kk) / len(kk))
    out.sort()
    return out[int(0.025 * NBOOT)], out[int(0.975 * NBOOT)]


def main():
    gold = nap(GOLD)
    pred = nap(os.path.join(ROOT, "runs", "preds_s2_seed101.jsonl"))
    S1 = nap(os.path.join(ROOT, "runs", "score_s1_seed101_raw.jsonl"))
    S2 = nap(os.path.join(ROOT, "runs", "score_s2_seed101_raw.jsonl"))

    cells, loai = {}, []
    for k, g in gold.items():
        if k not in S2 or k not in S1:
            continue
        gt = chuan(g.get("name") or "")
        co_ten = bool(gt) and gt != "no name"
        raw = pred.get(k, {}).get("raw", "")
        if "<desc>" not in raw:
            continue                      # nhóm không phát descriptor, đã có mục riêng
        if not co_ten:
            loai.append(k)                # (1) ô bị loại khỏi bảng chéo
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

    def bao(ten, ks):
        n = len(ks)
        d = 100 * (sum(ex(S2, k) for k in ks) - sum(ex(S1, k) for k in ks)) / n
        lo, hi = boot(ks, S2, S1)
        print(f"{ten:42s} n={n:5d}  Delta={d:+7.2f} pp  KTC95 [{lo:+.2f} · {hi:+.2f}]")

    print("Bốn ô của bảng chéo (phải trùng bài):")
    for (t, p), nhan in [((True, True), "tên đúng, point đúng"),
                         ((True, False), "tên đúng, point sai"),
                         ((False, True), "tên sai, point đúng"),
                         ((False, False), "tên sai, point sai")]:
        ks = cells[(t, p)]
        n = len(ks)
        d = 100 * (sum(ex(S2, k) for k in ks) - sum(ex(S1, k) for k in ks)) / n
        print(f"  {nhan:34s} n={n:5d}  Delta={d:+7.2f} pp")

    print("\nHai con số bảng chéo không in ra:")
    bao("  ô bị loại (có desc, không tên vàng)", loai)
    bao("  phần bù ô 'cả hai đúng'",
        [k for key, v in cells.items() if key != (True, True) for k in v])


if __name__ == "__main__":
    main()
