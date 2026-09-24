# -*- coding: utf-8 -*-
"""
PATA · dựng hộp SWAP cho cổng cuối C1, điều kiện 5 (report/185 §8). CHẠY TRÊN CPU, 0 GPU.

Điều kiện 5: "swap sang matched distractor làm câu đổi về phía distractor nhiều hơn random-pool
control, với cận dưới KTC một phía 90% của chênh lệch > 0".

Với mỗi bước val600 có `kl_ok` và có `desc_neg` (phần tử gây nhiễu do chính labeler dựng — cùng loại,
cách 80–350 px, xem `hop_le()`), dựng hai hộp để ÉP α của bridge (thay α do localizer chọn):
  D  (matched distractor) hộp CÙNG CỠ hộp vàng, tâm tại điểm của `desc_neg`, cắt vào màn.
     ⚠️ Chỉ có ĐIỂM của phần tử gây nhiễu, không có hộp thật của nó ⇒ "cùng cỡ hộp vàng" là xấp xỉ, phải
     khai. Cùng cỡ cũng là thứ làm D "matched" với vàng về diện tích.
  R  (random-pool) hộp vàng của MỘT bước val600 khác (episode khác, hạt cố định), chuẩn hoá theo cỡ màn
     rồi đặt vào màn này — một vùng "trông như phần tử" nhưng không gắn với bước này.
Loại bước nếu D chồng hộp vàng (IoU ≥ 0,3); R được bốc lại (tối đa 50 lần) tới khi IoU(R, vàng) < 0,3 và
IoU(R, D) < 0,3.

Đọc kết quả (pata_cong_c1.py): UGround trỏ câu sinh ra; "về phía D" ⇔ điểm trỏ gần tâm D hơn tâm vàng.
Chênh lệch = P(về phía D | ép D) − P(về phía D | ép R), ghép cặp theo bước, bootstrap cụm theo episode.

Ra: pata/val600_swap.jsonl + dòng hash trong pata/swap_hash.json. Hạt 20260924.
    ~/.venvs/thesis/bin/python harness/pata_swap.py
"""
import os, re, json, random, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
SEED = 20260924
IOU_MAX = 0.3


def iou(a, b):
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / ua if ua > 0 else 0.0


def dat_hop(cx, cy, bw, bh, w, h):
    """Hộp cỡ bw×bh tâm (cx, cy), đẩy vào trong màn (giữ cỡ nếu được)."""
    bw, bh = min(bw, w), min(bh, h)
    x1 = min(max(0, cx - bw / 2), w - bw)
    y1 = min(max(0, cy - bh / 2), h - bh)
    return [round(x1), round(y1), round(x1 + bw), round(y1 + bh)]


def main():
    D = {}
    for l in open(os.path.join(ROOT, "descriptors.jsonl"), encoding="utf-8"):
        d = json.loads(l)
        D[(d["episode_id"], d["step_id"])] = d
    recs = [json.loads(l) for l in open(os.path.join(ROOT, "pata", "val600.jsonl"), encoding="utf-8")]
    pool = [r for r in recs if r["kl_ok"]]
    rnd = random.Random(SEED)
    out, bo = [], {"khong_kl_ok": 0, "khong_desc_neg": 0, "D_chong_vang": 0, "khong_boc_duoc_R": 0}
    for r in recs:
        if not r["kl_ok"]:
            bo["khong_kl_ok"] += 1; continue
        d = D.get((r["episode_id"], r["step_id"]))
        m = re.search(r"<point>(\d+),(\d+)</point>", (d or {}).get("desc_neg") or "")
        if not m:
            bo["khong_desc_neg"] += 1; continue
        w, h, g = r["w"], r["h"], r["box"]
        px, py = int(m.group(1)) / 1000 * w, int(m.group(2)) / 1000 * h
        bD = dat_hop(px, py, g[2] - g[0], g[3] - g[1], w, h)
        if iou(bD, g) >= IOU_MAX:
            bo["D_chong_vang"] += 1; continue
        bR = None
        for _ in range(50):
            o = pool[rnd.randrange(len(pool))]
            if o["episode_id"] == r["episode_id"]:
                continue
            b = o["box"]
            cand = [round(b[0] / o["w"] * w), round(b[1] / o["h"] * h),
                    round(b[2] / o["w"] * w), round(b[3] / o["h"] * h)]
            if cand[2] <= cand[0] or cand[3] <= cand[1]:
                continue
            if iou(cand, g) < IOU_MAX and iou(cand, bD) < IOU_MAX:
                bR = cand; break
        if bR is None:
            bo["khong_boc_duoc_R"] += 1; continue
        out.append({"episode_id": r["episode_id"], "step_id": r["step_id"], "w": w, "h": h,
                    "box_vang": g, "box_D": bD, "box_R": bR, "diem_D": [round(px), round(py)],
                    "iou_D_vang": round(iou(bD, g), 4), "iou_R_vang": round(iou(bR, g), 4)})
    p = os.path.join(ROOT, "pata", "val600_swap.jsonl")
    with open(p, "w", encoding="utf-8") as f:
        for x in out:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    hsh = hashlib.sha256(open(p, "rb").read()).hexdigest()
    json.dump({"val600_swap.jsonl": hsh, "seed": SEED, "iou_max": IOU_MAX, "n": len(out), "bo": bo},
              open(os.path.join(ROOT, "pata", "swap_hash.json"), "w"), indent=1)
    print(f"val600: {len(recs)} bước chạm · dùng cho swap {len(out)} · bỏ {bo}")
    print(f"→ {p}  sha256 {hsh[:16]}…")


if __name__ == "__main__":
    main()
