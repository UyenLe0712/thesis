# -*- coding: utf-8 -*-
"""
FREE · offline — chạy sẵn bộ đọc chữ trên ảnh dữ liệu dạy, lưu kết quả để dùng cho lớp 2.

Lớp 2 nối danh sách chữ nhìn thấy vào đầu vào của mô hình. Chạy bộ đọc chữ ngay lúc huấn
luyện thì chậm, nên đọc trước một lần rồi lưu lại. Vị trí ghi theo lưới thô 3x3 để mô tả
gọn và không phụ thuộc kích thước màn.

Chạy: ~/.venvs/thesis/bin/python harness/prep_ocr_train.py [--limit N] [--split test]
"""
import os, json, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
# --split test  -> chạy trên tập kiểm (cùng mã, để đầu vào lúc chấm giống hệt lúc dạy)
_SPLIT = "test" if "--split" in os.sys.argv and "test" in os.sys.argv else "train"
ROOT = os.path.join(HERE, "dg1_cache", f"{_SPLIT}_ac")
OUT = os.path.join(ROOT, "ocr.jsonl")
_RECFILE = "test.jsonl" if _SPLIT == "test" else "train.jsonl"

COLS = ["bên trái", "giữa", "bên phải"]
ROWS = ["trên đỉnh", "giữa màn", "dưới đáy"]


def zone(cx, cy, w, h):
    return f"{ROWS[min(int(cy / h * 3), 2)]}, {COLS[min(int(cx / w * 3), 2)]}"


def main(limit=None):
    from rapidocr_onnxruntime import RapidOCR
    from PIL import Image
    ocr = RapidOCR()
    done = set()
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            for line in f:
                done.add(json.loads(line)["image"])
    recs = [json.loads(l) for l in open(os.path.join(ROOT, _RECFILE), encoding="utf-8")]
    if limit:
        recs = recs[:limit]
    todo = [r for r in recs if r["image"] not in done]
    print(f"{len(recs)} bước · đã đọc {len(done)} · còn {len(todo)}")
    with open(OUT, "a", encoding="utf-8") as f:
        for i, r in enumerate(todo, 1):
            im = Image.open(os.path.join(ROOT, r["image"])).convert("RGB")
            w, h = im.size
            res, _ = ocr(im)
            items = []
            for box, txt, conf in (res or []):
                xs = [p[0] for p in box]; ys = [p[1] for p in box]
                cx, cy = sum(xs) / 4, sum(ys) / 4
                t = (txt or "").strip()
                if len(t) < 1 or conf < 0.5:
                    continue
                items.append({"text": t, "cx": round(cx), "cy": round(cy), "zone": zone(cx, cy, w, h)})
            f.write(json.dumps({"image": r["image"], "w": w, "h": h, "items": items}, ensure_ascii=False) + "\n")
            f.flush()
            if i % 50 == 0:
                print(f"  ...{i}/{len(todo)}")
    print("Đã lưu", OUT)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--limit", type=int)
    ap.add_argument("--split", default="train", choices=["train", "test"])
    main(ap.parse_args().limit)
