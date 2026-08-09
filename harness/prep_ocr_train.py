# -*- coding: utf-8 -*-
"""
FREE · offline — chạy sẵn bộ đọc chữ trên ảnh dữ liệu dạy, lưu kết quả để dùng cho lớp 2.

Lớp 2 nối danh sách chữ nhìn thấy vào đầu vào của mô hình. Chạy bộ đọc chữ ngay lúc huấn
luyện thì chậm, nên đọc trước một lần rồi lưu lại. Vị trí ghi theo lưới thô 3x3 để mô tả
gọn và không phụ thuộc kích thước màn.

Chạy: ~/.venvs/thesis/bin/python harness/prep_ocr_train.py [--limit N] [--split test]
"""
import os, json, argparse

# GHIM MỖI TIẾN TRÌNH VỀ MỘT LUỒNG — phải đặt TRƯỚC khi onnxruntime được nạp.
# `run_on_rented.sh` chạy song song `nproc` tiến trình. ONNX Runtime mặc định lấy hết
# số lõi cho phần tính trong một phép, nên trên máy 32 lõi sẽ thành 32 tiến trình ×
# 32 luồng = hơn 1.000 luồng tranh nhau 32 lõi. Kết quả là chậm hơn cả chạy ít tiến
# trình, mà nhìn vào chỉ thấy "OCR lâu hơn dự tính" chứ không thấy nguyên nhân — và
# lâu hơn ở đây là tiền, vì card đồ hoạ nằm không suốt lúc đó. Song song ở mức TIẾN
# TRÌNH, mỗi tiến trình một luồng, là cách chia đúng cho việc này.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "ORT_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

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


def main(limit=None, shard=0, nshard=1):
    """RapidOCR chạy một luồng, ~0,08 ảnh/giây → 6.969 ảnh mất cỡ 24 tiếng.
    Chia mảnh để chạy nhiều tiến trình song song: mỗi tiến trình ghi tệp riêng
    (ocr.part{k}.jsonl) nên không tranh nhau khoá ghi; gộp lại bằng --merge."""
    from rapidocr_onnxruntime import RapidOCR
    from PIL import Image
    # ghim thêm ở tầng thư viện, phòng khi biến môi trường bị ghi đè
    try:
        ocr = RapidOCR(intra_op_num_threads=1)
    except TypeError:
        ocr = RapidOCR()
    out_path = OUT if nshard == 1 else OUT.replace(".jsonl", f".part{shard}.jsonl")
    done = set()
    for p in ([out_path] if nshard > 1 else [OUT]):
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                for line in f:
                    done.add(json.loads(line)["image"])
    recs = [json.loads(l) for l in open(os.path.join(ROOT, _RECFILE), encoding="utf-8")]
    if limit:
        recs = recs[:limit]
    if nshard > 1:
        recs = [r for i, r in enumerate(recs) if i % nshard == shard]
    todo = [r for r in recs if r["image"] not in done]
    print(f"[mảnh {shard}/{nshard}] {len(recs)} bước · đã đọc {len(done)} · còn {len(todo)}")
    with open(out_path, "a", encoding="utf-8") as f:
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
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshard", type=int, default=1)
    ap.add_argument("--merge", action="store_true", help="gộp các tệp mảnh thành ocr.jsonl")
    a = ap.parse_args()
    if a.merge:
        import glob
        seen, n = set(), 0
        parts = sorted(glob.glob(OUT.replace(".jsonl", ".part*.jsonl")))
        with open(OUT, "a", encoding="utf-8") as w:
            for p in parts:
                for line in open(p, encoding="utf-8"):
                    k = json.loads(line)["image"]
                    if k in seen:
                        continue
                    seen.add(k); w.write(line); n += 1
        print(f"Gộp {len(parts)} mảnh → {n} bản ghi vào {OUT}")
    else:
        main(a.limit, a.shard, a.nshard)
