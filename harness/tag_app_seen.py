# -*- coding: utf-8 -*-
"""
FREE — gắn lại nhãn `app_seen_in_train` cho tập kiểm.

Vì sao phải có tệp này. Trường `app_seen_in_train` đã nằm sẵn trong `test.jsonl` và
được `score_run.py` ghi ra vết để cắt lát phụ "ứng dụng đã thấy / chưa thấy lúc dạy"
(`report/106` mục sửa đổi 6/8). Nhưng rà lại ngày 6/8 thì **không có dòng mã nào trong
repo sinh ra nó** — nó do một lượt vá tay để lại. Hai hệ quả:

  · không tái lập được, nên không kiểm được nó tính đúng hay sai;
  · nó KHÔNG tự sửa theo tập dạy thật. Đối chiếu với lát dạy đang có (2 shard, 117 ứng
    dụng) thì 2.016/3.130 bản ghi có nhãn mâu thuẫn. Nhãn cũ nhiều khả năng tính theo
    toàn bộ 15.283 tác vụ của AndroidControl — đúng NẾU cuối cùng train đủ 76 shard, sai
    nếu train ít hơn. Mà số shard thì tới lúc chạy mới biết.

Nhãn này phải là hàm của **tập dạy thật sự dùng**, nên chỗ đúng để tính nó là ngay sau
khi dựng xong dữ liệu dạy, không phải lúc dựng tập kiểm.

Luật gán ứng dụng bê nguyên `build_test_data.app_of`: chỉ lấy từ thao tác `open_app`,
không đoán từ chữ trong mục tiêu — vòng phản biện 19/7 đã bắt lỗi cách đoán đó tự đẻ ra
cụm rác và tách một app thành nhiều cụm, làm khoảng tin cậy hẹp giả.

Ba giá trị, phải phân biệt khi đọc kết quả:
  True   ứng dụng của bước này có mặt trong tập dạy
  False  có gán được ứng dụng, và nó KHÔNG có trong tập dạy
  None   không gán được ứng dụng → **không biết**, không phải "chưa thấy"

Chạy:
  ~/.venvs/thesis/bin/python harness/tag_app_seen.py            # gắn lại + in đối chiếu
  ~/.venvs/thesis/bin/python harness/tag_app_seen.py --dry-run  # chỉ xem, không ghi
"""
import os, sys, json, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
TRAIN = os.path.join(HERE, "dg1_cache", "train_ac", "train.jsonl")
TEST = os.path.join(HERE, "dg1_cache", "test_ac", "test.jsonl")


def train_apps(path):
    """Ứng dụng có mặt trong tập dạy.

    `train.jsonl` không mang sẵn trường `app`, nên suy từ lịch sử thao tác: dòng lịch sử
    đầu tiên của một tác vụ là câu chuẩn của bước `open_app`, dạng "open the X app".
    Đây là cùng một nguồn thông tin mà `build_test_data.app_of` dùng cho tập kiểm, chỉ
    khác là bên đó đọc thẳng trường `app_name` còn bên này đọc câu đã viết ra.
    """
    import re
    apps = set()
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        for h in [r.get("goal", "")] + list(r.get("history") or []):
            m = re.match(r"\s*open\s+(?:the\s+)?(.+?)(?:\s+app)?\s*$", (h or "").strip(), re.I)
            if m:
                apps.add(m.group(1).strip().lower())
                break
    return apps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default=TRAIN)
    ap.add_argument("--test", default=TEST)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not os.path.exists(a.train):
        sys.exit(f"Chưa có tập dạy: {a.train}. Chạy build_train_data.py trước.")
    seen = train_apps(a.train)
    recs = [json.loads(l) for l in open(a.test, encoding="utf-8")]

    old = collections.Counter(r.get("app_seen_in_train") for r in recs)
    changed = 0
    for r in recs:
        app = (r.get("app") or "").strip().lower()
        new = (app in seen) if app else None
        if new != r.get("app_seen_in_train"):
            changed += 1
        r["app_seen_in_train"] = new
    new_c = collections.Counter(r.get("app_seen_in_train") for r in recs)

    print(f"Ứng dụng có trong tập dạy : {len(seen)}")
    print(f"Bước của tập kiểm         : {len(recs)}")
    print(f"{'':26}{'trước':>8}{'sau':>8}")
    for k, nm in ((True, "đã thấy lúc dạy"), (False, "CHƯA thấy lúc dạy"),
                  (None, "không gán được app")):
        print(f"  {nm:24}{old.get(k, 0):8}{new_c.get(k, 0):8}")
    print(f"Số bản ghi đổi nhãn       : {changed}")

    lab = new_c.get(True, 0) + new_c.get(False, 0)
    if lab:
        print(f"\nTrong phần gán được app: {new_c.get(True,0)/lab:.1%} đã thấy lúc dạy.")
    print("⚠ Nhóm 'không gán được app' là KHÔNG BIẾT, không được đọc thành 'chưa thấy'.")

    if a.dry_run:
        print("\n--dry-run: không ghi gì.")
        return
    tmp = a.test + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, a.test)
    print(f"\nĐã ghi lại {a.test}")


if __name__ == "__main__":
    main()
