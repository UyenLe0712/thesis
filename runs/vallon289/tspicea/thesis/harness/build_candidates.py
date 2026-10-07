# -*- coding: utf-8 -*-
"""
FREE · offline — dựng KHỐI ỨNG VIÊN cho từng màn: danh sách `tên <point>x,y</point>`.

Đăng ký trước ở `report/106` mục **(x14d)** nhánh ① NHÁNH-ỨNG-VIÊN.

Vì sao cần: câu nhắc hiện chỉ nhét 24 dòng OCR **không kèm toạ độ**
(`build_branch_data.py:31`). Đo 25/8: trong số bước MIN-DESC gọi SAI tên, **67,7%** đã có
tên vàng nằm sẵn trong 24 dòng đó ⇒ thông tin có sẵn mà mô hình không dùng được vì
không có gì neo tên vào vị trí.

⛔ Luật thiết kế, đừng đổi khi thấy số:
  · Tên ứng viên phải đúc bằng **ĐÚNG** chuỗi hàm đã dựng nhãn vàng —
    `nodes_of` → `name_of` (`descriptor_label_build.py:78,131`). Dùng OCR thô sẽ đẻ ra
    chuỗi không tồn tại trong nhãn vàng, làm phủ tụt mà không phải lỗi của mô hình.
  · Gộp cha-con bằng `overlapped` — cây trợ năng lồng nhiều tầng, một ViewGroup bọc một
    TextView cùng mang một chữ.
  · Sắp theo **thứ tự đọc** (trên→dưới, trái→phải) và cắt theo thứ tự đó. Mọi cách sắp
    xếp hay cắt phụ thuộc vào phần tử đích đều là **rò rỉ**: nó nói cho mô hình biết
    đáp án nằm đâu trong danh sách.
  · Toạ độ dùng lưới [0,1000] y hệt ô `<point>` của khai báo, để mô hình chép thẳng được.

Chạy:
  ~/.venvs/thesis/bin/python harness/build_candidates.py --split train
  ~/.venvs/thesis/bin/python harness/build_candidates.py --split test
"""
import os, sys, json, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import descriptor_label_build as D

MAX_CAND = 40          # trần số ứng viên; chọn theo ngân sách token, KHÔNG theo phủ
GRID = 1000


def _norm(cx, cy, w, h):
    return max(0, min(GRID, round(cx * GRID / w))), max(0, min(GRID, round(cy * GRID / h)))


def candidates_of(rel, ocr_rec, w, h, max_cand=MAX_CAND):
    """Danh sách ứng viên của một màn: [(tên, nx, ny)], đã gộp trùng, theo thứ tự đọc."""
    nds = D.nodes_of(rel)
    if not nds:
        return []
    raw = []
    for box, cls, a11y_name in nds:
        area_share = (box[2] - box[0]) * (box[3] - box[1]) / max(1, w * h)
        nm, _src = D.name_of(box, a11y_name, ocr_rec, area_share)
        if not nm:
            continue
        raw.append((box, nm))

    # gộp: cùng tên (không phân biệt hoa thường) VÀ hai hộp lồng/chồng nhau quá nửa
    kept = []
    for box, nm in raw:
        low = nm.lower()
        dup = False
        for i, (kb, kn) in enumerate(kept):
            if kn.lower() == low and D.overlapped(box, kb):
                # giữ hộp NHỎ hơn — nó là phần tử thật, hộp to là khung bọc
                if (box[2] - box[0]) * (box[3] - box[1]) < (kb[2] - kb[0]) * (kb[3] - kb[1]):
                    kept[i] = (box, nm)
                dup = True
                break
        if not dup:
            kept.append((box, nm))

    out = []
    for box, nm in kept:
        nx, ny = _norm((box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0, w, h)
        out.append((nm, nx, ny))
    out.sort(key=lambda t: (t[2], t[1]))          # thứ tự đọc — độc lập với gold
    return out[:max_cand]


def block_str(cands):
    """Chuỗi đưa vào câu nhắc. Một dòng một ứng viên, ngắt bằng ' · ' cho gọn token."""
    return " · ".join(f"{nm} <point>{nx},{ny}</point>" for nm, nx, ny in cands)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["train", "test"], default="train")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max", type=int, default=MAX_CAND)
    ap.add_argument("--all-steps", action="store_true",
                    help="ghi MỌI bước, không chỉ bước chạm. Nhánh gui_sel cần thế vì câu nhắc "
                         "phải có khối ứng viên ở mọi bước; bước không chạm nhận khối như thường "
                         "và nhãn <sel>none</sel>. Cổng G1/G2 vẫn chỉ đo trên bước có tên vàng.")
    args = ap.parse_args()
    D.set_split(args.split)
    ROOT = D.ROOT

    ocr = {}
    with open(os.path.join(ROOT, "ocr.jsonl"), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            ocr[r["image"]] = r

    # nhãn vàng — chỉ để ĐO CỔNG, không tham gia dựng khối
    gold = {}
    gp = os.path.join(ROOT, "descriptors.jsonl")
    if os.path.exists(gp):
        with open(gp, encoding="utf-8") as f:
            for line in f:
                g = json.loads(line)
                gold[(g["episode_id"], g["step_id"])] = g

    fn = "test.jsonl" if args.split == "test" else "train.jsonl"
    recs = [json.loads(l) for l in open(os.path.join(ROOT, fn), encoding="utf-8")]
    if args.split == "test":
        from PIL import Image
        for r in recs:
            if "w" not in r:
                with Image.open(os.path.join(ROOT, r["image"])) as im:
                    r["w"], r["h"] = im.size
    if args.all_steps:
        taps = recs
    else:
        taps = [r for r in recs if r["action"].get("action_type") in ("click", "long_press")
                and "x" in r["action"]]
    if args.limit:
        taps = taps[:args.limit]

    # ⛔ --limit là chế độ THỬ: ghi ra tệp riêng, không đè tệp thật.
    # (2/9: một lượt thử --limit 30 đã đè mất bản 4.463 màn của tập kiểm.)
    outp = os.path.join(ROOT, f"candidates_thu_{args.limit}.jsonl" if args.limit
                        else "candidates.jsonl")
    st = collections.Counter()
    n_cand, phu, c3, do_dai = [], 0, 0, []
    n_gold = 0
    with open(outp, "w", encoding="utf-8") as fo:
        for i, r in enumerate(taps):
            rel = f"episode_{r['episode_id']}_screenshot_{r['step_id']}.png"
            w, h = r.get("w") or 1080, r.get("h") or 2400
            cands = candidates_of(rel, ocr.get(r["image"]), w, h, args.max)
            if not cands:
                st["khong_co_ung_vien"] += 1
            n_cand.append(len(cands))
            blk = block_str(cands)
            do_dai.append(len(blk))
            fo.write(json.dumps({"image": r["image"], "episode_id": r["episode_id"],
                                 "step_id": r["step_id"], "w": w, "h": h,
                                 "cands": [{"name": a, "x": b, "y": c} for a, b, c in cands]},
                                ensure_ascii=False) + "\n")

            g = gold.get((r["episode_id"], r["step_id"]))
            if g and g.get("name"):
                n_gold += 1
                gname = g["name"].strip().lower()
                gx, gy = g["point_norm"]
                khop = [(a, b, c) for a, b, c in cands if a.strip().lower() == gname]
                if khop:
                    phu += 1
                    # C3: có ứng viên vừa khớp tên vừa nằm trong ô dung sai 14% của hai cạnh
                    if any(abs(b - gx) <= 140 and abs(c - gy) <= 140 for _, b, c in khop):
                        c3 += 1
            if (i + 1) % 5000 == 0:
                print(f"  {i+1}/{len(taps)}", flush=True)

    n_cand.sort(); do_dai.sort()
    print("=" * 66)
    print(f"ghi {outp}: {len(n_cand)} màn"
          f"{'  (MỌI bước — --all-steps)' if args.all_steps else '  (chỉ bước chạm)'}")
    for k, v in st.most_common():
        print(f"  {k}: {v}")
    print(f"số ứng viên/màn : trung vị {n_cand[len(n_cand)//2]} · p90 {n_cand[int(.9*len(n_cand))]}"
          f" · max {n_cand[-1]} · chạm trần {args.max}: {sum(1 for x in n_cand if x >= args.max)}")
    print(f"độ dài khối (ký tự): trung vị {do_dai[len(do_dai)//2]} · p90 {do_dai[int(.9*len(do_dai))]}"
          f" · max {do_dai[-1]}")
    print("=" * 66)
    print("CỔNG (x14e) — trượt là bỏ nhánh ỨNG-VIÊN, không nới")
    print("=" * 66)
    if n_gold:
        print(f"G1 phủ  — tên vàng có trong khối : {phu}/{n_gold} = {phu/n_gold:6.1%}"
              f"   {'✅ ĐẠT (≥95%)' if phu/n_gold >= .95 else '⛔ TRƯỢT'}")
        print(f"G2 C3   — khớp tên ∧ trong ±140  : {c3}/{n_gold} = {c3/n_gold:6.1%}"
              f"   {'✅ ĐẠT (≥75%)' if c3/n_gold >= .75 else '⛔ TRƯỢT'}")
    else:
        print("⚠️ không có nhãn vàng để đo cổng — chạy descriptor_label_build.py trước")


if __name__ == "__main__":
    main()
