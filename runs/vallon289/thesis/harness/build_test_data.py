# -*- coding: utf-8 -*-
"""
FREE — dựng TẬP KIỂM cho khâu chấm điểm.

⚠️ Đây KHÔNG phải split app-unseen: 92% ứng dụng trong tập kiểm cũng có ở tập dạy.
   Nó là tập giữ riêng theo TÁC VỤ (0 tác vụ trùng). Chi tiết + hệ quả: report/106 mục
   sửa đổi ngày 6/8. Nhãn app_seen_in_train ghi sẵn trong mỗi bản ghi để cắt lát phụ.

Tới giờ mọi thứ đã dựng đều là tập DẠY. Tập kiểm mới là thứ cổng A (đo sai số bộ trỏ)
và toàn bộ khâu chấm cần: ảnh màn hình + toạ độ chạm thật + câu chuẩn người viết.
Kho ảnh có sẵn 9 shard `data/test-*.parquet`, ghép với câu chuẩn theo (episode, step)
đúng như đã làm cho tập dạy.

Gán ứng dụng: cần cho việc gom cụm khi tính khoảng tin cậy (report/106 mục 6). Suy từ
`open_app` trong chuỗi thao tác, không suy được thì để trống — theo quy tắc cụm-đơn đã
khoá, mỗi tác vụ không gán được app tự thành một cụm riêng, KHÔNG bị loại khỏi tập.

Chạy:
  ~/.venvs/thesis/bin/python harness/build_test_data.py --check       # 1 shard, kiểm ghép
  ~/.venvs/thesis/bin/python harness/build_test_data.py --shards 9    # dựng thật (~8GB)
"""
import os, sys, json, ast, re, io as _io, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "dg1_cache", "test_ac")
GOLD_REPO = "HarrytheOrange/parsed_AndroidControl"
IMG_REPO = "ckg/AndroidControlParsedWithImages-20k"
N_TEST_SHARDS = 9

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
    """Xoá parquet vừa đọc xong — xem chú thích cùng tên ở build_train_data.py."""
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
        path = hf_hub_download(IMG_REPO, f"data/test-{i:05d}-of-{N_TEST_SHARDS:05d}.parquet",
                               repo_type="dataset")
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


def app_of(acts, goal):
    """Ứng dụng của tác vụ: lấy từ thao tác open_app, không có thì để trống.

    KHÔNG đoán app từ chữ trong mục tiêu — vòng phản biện 19/7 đã bắt lỗi cách đoán đó
    tự đẻ ra cụm rác và tách một app thành nhiều cụm, làm khoảng tin cậy hẹp giả.
    """
    for a in acts:
        if a.get("action_type") == "open_app" and a.get("app_name"):
            return a["app_name"].strip().lower()
    return ""


def content_words(s):
    return {w for w in re.findall(r"[a-z']+", (s or "").lower()) if w not in STOP and len(w) > 2}


def check(n_shards=1, n_check=60):
    """Kiểm ghép ĐÚNG chứ không chỉ ghép ĐƯỢC — cùng cách đã dùng cho tập dạy:
    so chữ OCR quanh điểm chạm với câu chuẩn, đối chứng bằng ghép lệch một bước.
    Ghép đúng phải khớp cao hơn hẳn ghép lệch."""
    from rapidocr_onnxruntime import RapidOCR
    from PIL import Image
    ocr = RapidOCR()
    gold = load_gold()
    hit = tot = shuf_hit = shuf_tot = 0
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
        best, bestd = None, 1e9
        for box, txt, _c in res:
            xs = [p[0] for p in box]; ys = [p[1] for p in box]
            cx, cy = sum(xs) / 4, sum(ys) / 4
            d = (cx - gx) ** 2 + (cy - gy) ** 2
            if d < bestd:
                best, bestd = txt, d
        near = content_words(best)
        tot += 1
        if near & content_words(g["steps"][sid]):
            hit += 1
        if sid + 1 < len(g["steps"]):
            shuf_tot += 1
            if near & content_words(g["steps"][sid + 1]):
                shuf_hit += 1
        if tot >= n_check:
            break
    print(f"ghép đúng   : {hit}/{tot} = {hit/max(tot,1):.0%}")
    print(f"ghép lệch 1 : {shuf_hit}/{shuf_tot} = {shuf_hit/max(shuf_tot,1):.0%}   (đối chứng)")
    print("→ ghép chuẩn" if hit / max(tot, 1) > 1.4 * shuf_hit / max(shuf_tot, 1)
          else "→ NGHI NGỜ: chênh không đủ, kiểm lại trước khi dùng")


def build(n_shards):
    os.makedirs(os.path.join(OUT, "images"), exist_ok=True)
    gold = load_gold()
    recs, st = [], collections.Counter()
    apps = collections.Counter()
    n_img = 0
    for j, png in iter_images(n_shards):
        eid, sid = int(j["episode_id"]), int(j["step_id"])
        g = gold.get(eid)
        if not g or sid >= len(g["steps"]):
            st["bo_khong_co_cau_chuan"] += 1
            continue
        # Bỏ bước KHÔNG CÓ CÂU CHUẨN. Câu chuẩn rỗng mà vẫn tính vào mẫu số thì mọi
        # nhánh đều bị trừ điểm oan ở đó — không nhánh nào khớp nổi một câu rỗng.
        # Trước 7/8 luật này nằm ở một lượt vá tay chứ không nằm trong mã, nên dựng lại
        # ra 6.969 bước trong khi tệp đã khoá có 6.958 — đủ để mẫu ngẫu nhiên của cổng A
        # lệch khỏi tập đã đăng ký.
        if not (g["steps"][sid] or "").strip():
            st["bo_cau_chuan_rong"] += 1
            continue
        act = g["acts"][sid]
        rel = f"images/ep{eid}_s{sid}.png"
        with open(os.path.join(OUT, rel), "wb") as f:
            f.write(png)
        n_img += 1
        app = app_of(g["acts"], g["goal"])
        apps[app or "(không gán được)"] += 1
        st[act.get("action_type", "?")] += 1
        recs.append({
            "episode_id": eid, "step_id": sid, "image": rel,
            "goal": g["goal"], "gold_instruction": g["steps"][sid],
            "action": act, "app": app,
            "history": g["steps"][:sid],
        })
    recs.sort(key=lambda r: (r["episode_id"], r["step_id"]))
    # Nhãn app_seen_in_train là HÀM CỦA TẬP DẠY, không tính được ở đây. Để trống, rồi
    # chạy harness/tag_app_seen.py sau khi dựng xong dữ liệu dạy. Ghi sẵn khoá để bản
    # ghi có đủ trường ngay từ đầu, khỏi ai đó tưởng thiếu.
    for r in recs:
        r.setdefault("app_seen_in_train", None)
    with open(os.path.join(OUT, "test.jsonl"), "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    n = len(recs)
    eps = len({r["episode_id"] for r in recs})
    tap = sum(v for k, v in st.items() if k in ("click", "long_press"))
    gan = n - apps["(không gán được)"]
    print("=" * 74)
    print(f"TẬP KIỂM — {n} bước / {eps} tác vụ / {n_img} ảnh")
    print("=" * 74)
    print(f"  bước chạm (đem chấm)      : {tap:5} = {tap/n:5.1%}")
    for k, v in st.most_common():
        if k.startswith("bo_"):
            continue
        print(f"    {k:22} {v:5} = {v/n:5.1%}")
    print("-" * 74)
    print(f"  gán được ứng dụng         : {gan:5} = {gan/n:5.1%}  ({len(apps)-1} app)")
    print(f"  không gán được → cụm riêng: {apps['(không gán được)']:5}")
    print(f"\nĐã lưu {OUT}/test.jsonl + images/")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--shards", type=int, default=N_TEST_SHARDS)
    a = ap.parse_args()
    if a.check:
        check(n_shards=1)
    else:
        build(a.shards)
