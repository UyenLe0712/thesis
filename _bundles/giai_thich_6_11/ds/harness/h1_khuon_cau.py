# -*- coding: utf-8 -*-
"""H1 (report/323 §8.4): câu chuẩn AndroidControl ngắn, theo khuôn, nội dung nằm ở tên phần tử — 0 GPU, chạy Kaggle CPU.

Đo trên câu chuẩn (không đụng câu mô hình), ba kho:
  AC-test   harness/dg1_cache/test_ac/test.jsonl (6.958 bước, trường gold_instruction)
  AC-train  harness/dg1_cache/train_ac/train.jsonl (64.567 bước, trường target_instruction)
  AitZ      runs/aitz/build_v3_25_10/out/test.jsonl (4.724 bước, trường gold_instruction)
Chỉ số:
  · số từ: TB, trung vị, p90
  · khuôn = hai từ đầu viết thường; số khuôn phủ 80% câu; tỉ lệ của 5 khuôn đầu
  · độ đa dạng từ: distinct-1/2 trên mẫu 2.000 câu cố định (seed 20261106), để ba kho cùng cỡ
  · tỉ lệ bước không chạm
  · AC bước chạm: tỉ lệ từ của câu nằm trong tên phần tử (descriptors.jsonl, trường name) — AitZ không có tên nên bỏ
Dự đoán ghi trước khi chạy (report/323): AC ngắn hơn và theo khuôn hơn AitZ; phần lớn từ ngoài khuôn là tên phần tử.
Số đọc được là mô tả, không có phép kiểm ý nghĩa nào ở đây.

  python h1_khuon_cau.py --out ../runs/giai_thich/h1_khuon_cau.json
"""
import os, json, re, random, argparse, collections, statistics as st

K = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TAPT = ("click", "long_press")
TU = re.compile(r"[a-z0-9]+")


def tu(s):
    return TU.findall((s or "").lower())


def hanh_dong(r):
    a = r.get("action")
    if isinstance(a, str):
        import ast
        a = ast.literal_eval(a)
    return a or {}


def la_cham(r):
    a = hanh_dong(r)
    return a.get("action_type") in TAPT and ("x" in a or "touch_yx" in a)   # AitZ ghi toạ độ bằng touch_yx


def nap(p, truong):
    R = []
    for l in open(p, encoding="utf-8"):
        r = json.loads(l)
        R.append((str(r["episode_id"]), str(r["step_id"]), (r.get(truong) or "").strip(), la_cham(r), hanh_dong(r).get("action_type", "?")))
    return R


def mo_ta(R, ten, rd):
    S = [x[2] for x in R if x[2]]
    W = [tu(s) for s in S]
    n = [len(w) for w in W]
    khuon = collections.Counter(" ".join(w[:2]) for w in W)
    tong, phu, k80 = len(W), 0, 0
    for _, c in khuon.most_common():
        phu += c; k80 += 1
        if phu >= 0.8 * tong:
            break
    mau = rd.sample(W, min(2000, len(W)))
    d1 = len({t for w in mau for t in w}) / max(1, sum(len(w) for w in mau))
    bg = [tuple(w[i:i + 2]) for w in mau for i in range(len(w) - 1)]
    d2 = len(set(bg)) / max(1, len(bg))
    loai = collections.Counter(x[4] for x in R)
    o = dict(kho=ten, n_cau=tong, n_rong=len(R) - tong,
             so_tu_tb=round(st.mean(n), 2), so_tu_trung_vi=st.median(n), so_tu_p90=sorted(n)[int(0.9 * len(n))],
             so_khuon_phu_80=k80, so_khuon=len(khuon),
             top5_khuon=[(k, round(c / tong, 4)) for k, c in khuon.most_common(5)],
             distinct1_2000=round(d1, 4), distinct2_2000=round(d2, 4),
             ti_le_khong_cham=round(sum(not x[3] for x in R) / len(R), 4),
             loai_thao_tac={k: round(v / len(R), 4) for k, v in loai.most_common(8)})
    print(json.dumps(o, ensure_ascii=False), flush=True)
    return o


def ti_le_ten(R, desc):
    """AC bước chạm: phần từ của câu chuẩn nằm trong tên phần tử vàng."""
    D = {}
    for l in open(desc, encoding="utf-8"):
        d = json.loads(l)
        m = re.match(r"<desc>[^|]*\|([^|]*)\|", d.get("desc") or "")
        D[(str(d["episode_id"]), str(d["step_id"]))] = tu(m.group(1)) if m else []
    tt, tn, co, kh = 0, 0, 0, collections.Counter()
    for e, s, g, cham, _ in R:
        if not cham or (e, s) not in D or not D[(e, s)]:
            continue
        ten = set(D[(e, s)])
        w = tu(g)
        co += 1
        tt += len(w)
        tn += sum(t in ten for t in w)
        kh[" ".join(t for t in w if t not in ten)[:40]] += 1
    o = dict(n_buoc_co_ten=co, ti_le_tu_thuoc_ten=round(tn / max(1, tt), 4),
             top8_phan_ngoai_ten=[(k, round(c / max(1, co), 4)) for k, c in kh.most_common(8)])
    print(json.dumps(o, ensure_ascii=False), flush=True)
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rd = random.Random(20261106)
    P = dict(ac_test=(f"{K}/harness/dg1_cache/test_ac/test.jsonl", "gold_instruction"),
             ac_train=(f"{K}/harness/dg1_cache/train_ac/train.jsonl", "target_instruction"),
             aitz=(f"{K}/runs/aitz/build_v3_25_10/out/test.jsonl", "gold_instruction"))
    out = {}
    for ten, (p, tr) in P.items():
        R = nap(p, tr)
        print(f"[{ten}] {p} · {len(R)} bước", flush=True)
        out[ten] = mo_ta(R, ten, rd)
        if ten == "ac_test":
            assert len(R) == 6958 and sum(x[3] for x in R) == 4463, (len(R), sum(x[3] for x in R))
            out["ac_test_ten"] = ti_le_ten(R, f"{K}/harness/dg1_cache/test_ac/descriptors.jsonl")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=1)
    print("[xong] ghi", a.out, flush=True)


if __name__ == "__main__":
    main()
