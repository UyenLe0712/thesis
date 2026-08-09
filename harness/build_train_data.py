# -*- coding: utf-8 -*-
"""
FREE — dựng dữ liệu DẠY cho phần train, bằng cách ghép hai bản đã trích sẵn.

Vì sao phải ghép: bản gốc AndroidControl nằm trên hạ tầng đám mây, nặng vài GB và cần cài
thêm thư viện xử lý. Trên HuggingFace có hai bản đã trích, mỗi bản thiếu một nửa:
  · `HarrytheOrange/parsed_AndroidControl` — có câu hướng dẫn người viết cho đủ 15.283 tác
    vụ, nhưng ảnh phải tự trích từ định dạng gốc
  · `ckg/AndroidControlParsedWithImages-20k` — có ảnh, nhưng đã chuyển sang định dạng
    thao-tác-cho-máy nên MẤT hẳn câu hướng dẫn người viết
Ghép theo (mã tác vụ, số thứ tự bước) thì được đủ cả bốn thứ cần cho một bước.

Lưu ý một chi tiết dễ tưởng là lỗi: số ảnh của một tác vụ thường NHIỀU HƠN số bước đúng một
— đó là ảnh của màn cuối cùng sau khi làm xong bước cuối, không có câu tương ứng, bỏ qua.

Kiểm chất lượng ghép: với bước chạm, đọc chữ quanh điểm gold rồi so với câu người viết. Nếu
ghép lệch bước thì chữ tại chỗ chạm sẽ không liên quan gì tới câu.

Chạy:
  ~/.venvs/thesis/bin/python harness/build_train_data.py --check      # chỉ kiểm chất lượng ghép
  ~/.venvs/thesis/bin/python harness/build_train_data.py --shards 3   # dựng thật, 3 shard
"""
import os, sys, re, json, ast, io as _io, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "dg1_cache", "train_ac")
GOLD_REPO = "HarrytheOrange/parsed_AndroidControl"
IMG_REPO = "ckg/AndroidControlParsedWithImages-20k"
STOP = {"the", "a", "an", "on", "in", "at", "to", "of", "and", "for", "click", "tap", "press",
        "select", "open", "go", "button", "icon", "screen", "top", "bottom", "left", "right",
        "corner", "then", "your", "this", "that", "it", "is", "are", "with", "from"}


def parse_list(v):
    return v if isinstance(v, list) else ast.literal_eval(v)


def load_gold():
    from huggingface_hub import hf_hub_download
    p = hf_hub_download(GOLD_REPO, "parsed_android_control.jsonl", repo_type="dataset")
    gold = {}
    with open(p, encoding="utf-8") as f:
        for line in f:
            o = json.loads(line)
            gold[int(o["episode_id"])] = {
                "goal": o["goal"],
                "steps": parse_list(o["step_instructions"]),
                "acts": parse_list(o["actions"]),
            }
    return gold


def _drop_parquet(path):
    """Xoá tệp parquet vừa dùng xong, cả liên kết lẫn khối dữ liệu thật.

    `hf_hub_download` giữ mọi shard đã tải trong cache. Với 76 shard thì parquet chiếm
    ~67 GB, mà ảnh PNG bung ra cũng ~67 GB — hai thứ cùng nằm trên đĩa là ~134 GB, chưa
    kể tập kiểm và cache mô hình. Trên máy thuê đĩa 200 GB thì đó là hết chỗ ở đúng lúc
    đang chạy dở, sau khi đã trả tiền cho mấy tiếng tải về. Mỗi shard chỉ đọc đúng một
    lần theo thứ tự nên xoá ngay sau khi đọc xong là an toàn; đỉnh đĩa hạ còn ~70 GB.

    Cache của HF là liên kết mềm trỏ vào thư mục `blobs`, nên xoá mỗi liên kết thì khối
    dữ liệu vẫn nằm nguyên đó — phải theo `realpath` mà xoá.
    """
    import os
    try:
        real = os.path.realpath(path)
        if real != path and os.path.exists(real):
            os.remove(real)
        if os.path.islink(path) or os.path.exists(path):
            os.remove(path)
    except OSError as e:
        print(f"   (không xoá được {path}: {e})")


def iter_images(n_shards, keep_parquet=False):
    from huggingface_hub import hf_hub_download
    import pyarrow.parquet as pq
    for i in range(n_shards):
        path = hf_hub_download(IMG_REPO, f"data/train-{i:05d}-of-00076.parquet", repo_type="dataset")
        pf = pq.ParquetFile(path)
        for b in pf.iter_batches(batch_size=100):
            for r in b.to_pylist():
                j = r["json"]
                if isinstance(j, (bytes, str)):
                    j = json.loads(j)
                yield j, r["png"]["bytes"]
        del pf
        if not keep_parquet:
            _drop_parquet(path)


def content_words(s):
    return {w for w in re.findall(r"[a-z']+", (s or "").lower()) if w not in STOP and len(w) > 2}


def check(n_shards=1, n_check=60):
    """Kiểm ghép ĐÚNG chứ không chỉ ghép ĐƯỢC.

    Cách đo: đọc chữ quanh điểm chạm rồi so với câu người viết. Nhưng tỉ lệ khớp tuyệt đối
    không nói lên nhiều, vì nút hình không có chữ và OCR hay đọc nhầm biểu tượng. Nên đo kèm
    ĐỐI CHỨNG: ghép lệch một bước (lấy câu của bước kế tiếp). Ghép đúng phải khớp cao hơn hẳn
    ghép lệch, nếu không thì phép ghép vô nghĩa."""
    from rapidocr_onnxruntime import RapidOCR
    from PIL import Image
    ocr = RapidOCR()
    gold = load_gold()
    hit = tot = shuf_hit = shuf_tot = 0
    examples = []
    for j, png in iter_images(n_shards, keep_parquet=True):
        eid, sid = int(j["episode_id"]), int(j["step_id"])
        g = gold.get(eid)
        if not g or sid >= len(g["steps"]):
            continue
        act = g["acts"][sid]
        if act.get("action_type") != "click" or "x" not in act:
            continue
        gx, gy = float(act["x"]), float(act["y"])
        im = Image.open(_io.BytesIO(png)).convert("RGB")
        res, _ = ocr(im)
        if not res:
            continue
        # chữ nào có hộp chứa hoặc gần điểm chạm nhất
        best, bestd = None, 1e9
        for box, txt, _conf in res:
            xs = [p[0] for p in box]; ys = [p[1] for p in box]
            dx = max(min(xs) - gx, 0, gx - max(xs)); dy = max(min(ys) - gy, 0, gy - max(ys))
            d = (dx * dx + dy * dy) ** 0.5
            if d < bestd:
                best, bestd = txt, d
        if bestd > 200:
            continue
        tot += 1
        ok = bool(content_words(best) & content_words(g["steps"][sid]))
        hit += ok
        # đối chứng: câu của bước KẾ TIẾP, đáng lẽ không liên quan tới chỗ vừa chạm
        nxt = g["steps"][sid + 1] if sid + 1 < len(g["steps"]) else None
        if nxt:
            shuf_tot += 1
            shuf_hit += bool(content_words(best) & content_words(nxt))
        if len(examples) < 6:
            examples.append((g["steps"][sid], best, round(bestd), ok))
        if tot >= n_check:
            break
    print("=" * 78)
    print(f"KIỂM GHÉP trên {tot} bước chạm có chữ gần điểm chạm:")
    print(f"  ghép ĐÚNG   : chữ tại chỗ chạm khớp câu ở {hit}/{tot} = {hit/max(tot,1):.0%}")
    print(f"  ghép LỆCH   : khớp câu của bước kế tiếp ở {shuf_hit}/{shuf_tot} = {shuf_hit/max(shuf_tot,1):.0%}  (đối chứng)")
    print("=" * 78)
    for a, b, d, ok in examples:
        print(f"  {'khớp ' if ok else 'không'} | câu: {a[:56]:56} | chữ tại chỗ chạm: {str(b)[:24]:24} (cách {d}px)")
    print("\nGhép đúng khớp cao hơn hẳn ghép lệch thì phép ghép là chuẩn. Tỉ lệ tuyệt đối luôn là")
    print("cận dưới, vì nút hình không có chữ và bộ đọc chữ hay đọc nhầm biểu tượng thành ký tự.")


def build(n_shards):
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "images"), exist_ok=True)
    gold = load_gold()
    recs, n_img = [], 0
    for j, png in iter_images(n_shards):
        eid, sid = int(j["episode_id"]), int(j["step_id"])
        g = gold.get(eid)
        if not g or sid >= len(g["steps"]):
            continue
        name = f"ep{eid}_s{sid}.png"
        with open(os.path.join(OUT, "images", name), "wb") as f:
            f.write(png)
        n_img += 1
        recs.append({
            "episode_id": eid, "step_id": sid, "image": f"images/{name}",
            "goal": g["goal"],
            "history": g["steps"][:sid],
            "target_instruction": g["steps"][sid],
            "action": g["acts"][sid],
            "w": j.get("screenshot_width"), "h": j.get("screenshot_height"),
        })
    with open(os.path.join(OUT, "train.jsonl"), "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Đã dựng {len(recs)} bước từ {n_shards} shard · {n_img} ảnh → {OUT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--shards", type=int, default=1)
    a = ap.parse_args()
    if a.check:
        check(n_shards=1)
    else:
        build(a.shards)
