# -*- coding: utf-8 -*-
"""
PATA C2 · P0 bước 1–4 (harness/tai_lieu_2026-09-25/204 §4.1). CHẠY TRÊN CPU, 0 GPU.

Dựng cặp (G, D) THẬT cho val400: G = phần tử vàng (hộp của bước), D = phần tử gây nhiễu do chính
labeler chọn (`nearest_other()` — cùng class, gần nhất, không lồng nhau), nay có HỘP THẬT nhờ bản vá
`descriptor_label_build.py` ghi thêm `box_neg`/`name_neg`/`cls_neg`/`point_neg_*`/`area_share_neg`.
⛔ Không dựng D bằng cỡ hộp vàng quanh <point> như `pata_swap.py`.

Tiền đề: đã chạy
    ~/.venvs/thesis/bin/python harness/descriptor_label_build.py --out descriptors_trueD.jsonl
(ghi ra tệp RIÊNG, không đè descriptors.jsonl). Script này kiểm lại, trên trọn 41.099 dòng, rằng mọi
trường cũ trùng tuyệt đối với descriptors.jsonl ⇒ bản vá chỉ thêm trường.

Kiểm bước 2 (204 §4.1): số dòng có `box_neg` phải BẰNG số dòng có `desc_neg`. ⚠️ Handoff ghi "khoảng
55,6%" — đo 25/9 thì `desc_neg` có ở 37.663/41.099 = 91,6%; 55,6% = 22.854/41.099 là tỉ lệ cặp qua
`hop_le()` của MIN-DESC. Phép kiểm đúng là BẰNG NHAU, không phải bằng 55,6%.

Luật eligible (khoá 25/9, trước khi có số nào), theo thứ tự lọc — mỗi luật đếm số bước bị loại:
  1. có box vàng và kl_ok (box hợp lệ, area_share < 0,50)            ← pata_data.py
  2. có box_neg (D thật)
  3. cùng class (cls_neg == role_class) — assert, nearest_other đã bảo đảm
  4. D hợp lệ: cắt vào màn còn cạnh ≥ 8 px, area_share_neg < 0,50
  5. không cha/con: không hộp nào chứa hộp kia, điểm chạm vàng KHÔNG nằm trong D
  6. IoU(G, D) < 0,30
  7. câu vàng không đúng cho D (proxy tự động, audit mù §4.1 bước 5 kiểm lại):
       a. tên G ≠ tên D sau chuẩn hoá (cả hai "(no name)" ⇒ loại) — đúng luật hop_le()
       b. câu vàng không nhắc tên D (≥ 3 ký tự) trong khi không nhắc tên G
  8. khoảng cách tâm 80–350 px
  9. dựng được cửa sổ R (xem dưới)

Cửa sổ crop cho P1 (§4.2 "cùng kích thước cửa sổ"): VUÔNG, cạnh
    s = clamp(1,3 · max(cạnh G, cạnh D), 0,25 · min(W,H), min(W,H))
đặt tâm tại tâm G / tâm D, đẩy vào trong màn. R = cửa sổ cùng cạnh s, tâm ngẫu nhiên (hạt theo bước)
sao cho IoU(win_R, win_G) < 0,30 và IoU(win_R, win_D) < 0,30; 500 lần bốc không được ⇒ loại bước.

Cổng bước 4: ≥ 150 cặp eligible trên val400 (mục tiêu 300) ⇒ đi tiếp audit; dưới 150 ⇒ DỪNG C2.

Ra: pata/val400_trueD.jsonl + pata/trueD_hash.json. Hạt 20260925.
    ~/.venvs/thesis/bin/python harness/pata_true_d.py
"""
import os, sys, json, random, hashlib, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_min_desc import chuan, o_ten

ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
SEED = 20260925
IOU_MAX = 0.30
AREA_MAX = 0.50
LO, HI = 80.0, 350.0
MIN_SIDE = 8
N_MIN, N_MUC_TIEU = 150, 300
NEG_KEYS = ("box_neg", "name_neg", "role_neg", "cls_neg", "point_neg_abs", "point_neg_norm",
            "area_share_neg")


def iou(a, b):
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / ua if ua > 0 else 0.0


def contains(a, b):
    return a[0] <= b[0] and a[1] <= b[1] and a[2] >= b[2] and a[3] >= b[3]


def center(b):
    return (b[0] + b[2]) / 2, (b[1] + b[3]) / 2


def window(cx, cy, s, w, h):
    """Cửa sổ vuông cạnh s tâm (cx, cy), đẩy vào trong màn."""
    x1 = min(max(0, cx - s / 2), w - s)
    y1 = min(max(0, cy - s / 2), h - s)
    return [round(x1), round(y1), round(x1) + round(s), round(y1) + round(s)]


def sha256(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def kiem_ban_va(p_new, p_old):
    """Mọi trường cũ trùng tuyệt đối; box_neg có đúng khi desc_neg có."""
    old = {}
    for l in open(p_old, encoding="utf-8"):
        d = json.loads(l)
        old[(d["episode_id"], d["step_id"])] = d
    new, lech, n_box, n_desc, sai_cap = {}, 0, 0, 0, 0
    for l in open(p_new, encoding="utf-8"):
        d = json.loads(l)
        k = (d["episode_id"], d["step_id"])
        o = old.get(k)
        assert o is not None, f"bước {k} có trong bản mới mà không có trong bản cũ"
        lech += sum(o[f] != d.get(f) for f in o)
        n_box += d["box_neg"] is not None
        n_desc += d["desc_neg"] is not None
        sai_cap += (d["box_neg"] is None) != (d["desc_neg"] is None)
        new[k] = d
    assert len(new) == len(old), f"số dòng lệch: mới {len(new)} vs cũ {len(old)}"
    assert lech == 0, f"⛔ {lech} trường cũ bị đổi — bản vá đụng logic, KHÔNG dùng"
    assert n_box == n_desc and sai_cap == 0, f"⛔ box_neg {n_box} ≠ desc_neg {n_desc} (lệch {sai_cap})"
    print(f"[bản vá] {len(new)} dòng · trường cũ lệch 0 · box_neg {n_box} = desc_neg {n_desc} "
          f"({n_box / len(new):.1%}) ✓", flush=True)
    return new, {"n": len(new), "box_neg": n_box, "desc_neg": n_desc}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="val400")
    ap.add_argument("--desc", default="descriptors_trueD.jsonl")
    a = ap.parse_args()
    desc, kiem = kiem_ban_va(os.path.join(ROOT, a.desc), os.path.join(ROOT, "descriptors.jsonl"))
    recs = [json.loads(l) for l in open(os.path.join(ROOT, "pata", f"{a.split}.jsonl"), encoding="utf-8")]

    bo = collections.Counter()
    out = []
    for r in recs:
        k = (r["episode_id"], r["step_id"])
        d = desc.get(k)
        w, h = r["w"], r["h"]
        G = r["box"]
        if not G or not r["kl_ok"] or d is None:
            bo["1_khong_box_hoac_kl_ok"] += 1; continue
        if d["box_neg"] is None:
            bo["2_khong_box_neg"] += 1; continue
        assert d["cls_neg"] == d["role_class"], f"{k}: D khác class — nearest_other sai?"
        bn = d["box_neg"]
        D = [max(0, bn[0]), max(0, bn[1]), min(w, bn[2]), min(h, bn[3])]
        if D[2] - D[0] < MIN_SIDE or D[3] - D[1] < MIN_SIDE or d["area_share_neg"] >= AREA_MAX:
            bo["4_D_khong_hop_le"] += 1; continue
        x, y = r["action"]["x"], r["action"]["y"]
        if contains(G, D) or contains(D, G) or (D[0] <= x <= D[2] and D[1] <= y <= D[3]):
            bo["5_cha_con"] += 1; continue
        if iou(G, D) >= IOU_MAX:
            bo["6_iou"] += 1; continue
        tG, tD = chuan(o_ten(d["desc"])), chuan(o_ten(d["desc_neg"]))
        if tG == tD:
            bo["7a_trung_ten"] += 1; continue
        cau = " " + chuan(r["target_instruction"]) + " "
        nD, nG = chuan(d["name_neg"] or ""), chuan(d["name"] or "")
        if len(nD) >= 3 and f" {nD} " in cau and not (len(nG) >= 3 and f" {nG} " in cau):
            bo["7b_cau_nhac_ten_D"] += 1; continue
        # khoảng cách tâm: tính lại từ hộp THÔ (chưa cắt) để đối chiếu neighbor_dist_px của labeler
        # (labeler lấy tâm hộp a11y gốc). G có thể đã bị pata_data cắt vào màn ⇒ dùng d["box"].
        (gx, gy), (dx, dy) = center(d["box"]), center(bn)
        kc = ((gx - dx) ** 2 + (gy - dy) ** 2) ** 0.5
        assert abs(kc - d["neighbor_dist_px"]) < 0.2, f"{k}: khoảng cách {kc:.1f} ≠ {d['neighbor_dist_px']}"
        if not (LO <= kc <= HI):
            bo["8_khoang_cach"] += 1; continue

        cg, cd = center(G), center(D)
        side = max(G[2] - G[0], G[3] - G[1], D[2] - D[0], D[3] - D[1])
        s = min(max(1.3 * side, 0.25 * min(w, h)), min(w, h))
        wG, wD = window(*cg, s, w, h), window(*cd, s, w, h)
        rnd = random.Random(f"{SEED}-{k[0]}-{k[1]}")
        wR = None
        for _ in range(500):
            c = window(rnd.uniform(s / 2, w - s / 2), rnd.uniform(s / 2, h - s / 2), s, w, h)
            if iou(c, wG) < IOU_MAX and iou(c, wD) < IOU_MAX:
                wR = c; break
        if wR is None:
            bo["9_khong_dung_duoc_R"] += 1; continue
        out.append({
            "episode_id": r["episode_id"], "step_id": r["step_id"], "image": r["image"],
            "goal": r["goal"], "history": r.get("history") or [],
            "target_instruction": r["target_instruction"], "action": r["action"], "w": w, "h": h,
            "box_G": G, "box_D": D, "name_G": d["name"], "name_D": d["name_neg"],
            "role": d["role"], "cls": d["role_class"], "dist_px": round(kc, 1),
            "area_G": r["area_share"], "area_D": d["area_share_neg"], "iou_GD": round(iou(G, D), 4),
            "side": round(s), "win_G": wG, "win_D": wD, "win_R": wR,
            "iou_win_GD": round(iou(wG, wD), 4),
        })

    p = os.path.join(ROOT, "pata", f"{a.split}_trueD.jsonl")
    with open(p, "w", encoding="utf-8") as f:
        for x in out:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    n = len(out)
    dat = n >= N_MIN
    meta = {"split": a.split, "n_buoc": len(recs), "n_eligible": n, "bo": dict(sorted(bo.items())),
            "cong_P0_buoc4": {"nguong": N_MIN, "muc_tieu": N_MUC_TIEU, "dat": dat},
            "ban_va": kiem, "seed": SEED, "iou_max": IOU_MAX, "area_max": AREA_MAX,
            "khoang_cach": [LO, HI],
            "sha256": {os.path.basename(p): sha256(p), a.desc: sha256(os.path.join(ROOT, a.desc)),
                       f"{a.split}.jsonl": sha256(os.path.join(ROOT, "pata", f"{a.split}.jsonl"))}}
    json.dump(meta, open(os.path.join(ROOT, "pata", "trueD_hash.json"), "w"), indent=1, ensure_ascii=False)

    print("=" * 72)
    print(f"{a.split}: {len(recs)} bước chạm → eligible {n}")
    for kk, v in sorted(bo.items()):
        print(f"  loại {kk:24} {v:4}")
    if n:
        med = lambda xs: sorted(xs)[len(xs) // 2]
        print(f"  khoảng cách tâm trung vị {med([x['dist_px'] for x in out])} px · IoU cửa sổ G/D trung vị "
              f"{med([x['iou_win_GD'] for x in out])} · số episode {len({x['episode_id'] for x in out})}")
        print(f"  class: {collections.Counter(x['cls'] for x in out).most_common(6)}")
    print("-" * 72)
    print(f"⇒ CỔNG P0 bước 4 (≥ {N_MIN}, mục tiêu {N_MUC_TIEU}): "
          + ("ĐẠT — sang audit mù (pata_audit_d.py build)" if dat else "KHÔNG ĐẠT — DỪNG C2"))
    print(f"→ {p}")


if __name__ == "__main__":
    main()
