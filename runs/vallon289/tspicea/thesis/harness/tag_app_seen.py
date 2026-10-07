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

⚠️ SỬA 12/8/2026 — chính lỗi vừa nói ở trên đã lọt vào đây. Bản đầu suy tên ứng dụng của
tập dạy bằng regex trên CÂU CHỮ, trong khi tập kiểm đọc thẳng trường `app_name`. Hai bên
hai nguồn thì lệch hình thức bị đọc thành lệch nội dung. Hai lỗi cụ thể: nó quét `goal`
trước lịch sử rồi `break`, nên câu mục tiêu dài lọt vào thành tên app
(`"adidas app and find local outlet stores…"`) và tên sạch trong lịch sử không bao giờ
được đọc tới; và nó không cắt dấu chấm cuối nên `"amazon app."` không khớp `amazon`.
Đo trên lát 1.697 bước: 42/129 tên suy ra là rác, và **27 ứng dụng có thật trong tập dạy
bị đếm nhầm thành chưa-thấy**, gồm `maps`, `youtube music`, `nike`, `citymapper`,
`skyscanner`, `tripadvisor`. Đây là phần lớn khoảng cách 604-vs-67 ghi ở `report/110`
mục 4b. Phần còn lại do nguồn khác: con số 67 hôm 6/8 là vá tay không có mã, đối chiếu
với split train đầy đủ của AndroidControl chứ không phải 12.895 tác vụ thật sự dựng.

`train.jsonl` HOÁ RA có sẵn `action.open_app.app_name` — cùng trường tập kiểm dùng — nên
nay lấy thẳng từ đó. Chiều lỗi cũng được chọn có chủ ý: gán nhầm thành "đã thấy" chỉ pha
loãng nhóm lớn (2.526 bước), gán nhầm thành "chưa thấy" thì bóp méo đúng nhóm nhỏ đang
xét (604 bước). Nên phần suy từ câu chữ được GIỮ làm nguồn phụ, có thống kê riêng để đọc
được nó đóng góp bao nhiêu.

Ba giá trị, phải phân biệt khi đọc kết quả:
  True   ứng dụng của bước này có mặt trong tập dạy
  False  có gán được ứng dụng, và nó KHÔNG có trong tập dạy
  None   không gán được ứng dụng → **không biết**, không phải "chưa thấy"

Chạy:
  ~/.venvs/thesis/bin/python harness/tag_app_seen.py            # gắn lại + in đối chiếu
  ~/.venvs/thesis/bin/python harness/tag_app_seen.py --dry-run  # chỉ xem, không ghi
"""
import os, sys, re, ast, json, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
TRAIN = os.path.join(HERE, "dg1_cache", "train_ac", "train.jsonl")
TEST = os.path.join(HERE, "dg1_cache", "test_ac", "test.jsonl")

RX_OPEN = re.compile(r"\s*open\s+(?:the\s+)?(.+?)(?:\s+app)?\s*$", re.I)


def norm(s):
    """Chuẩn hoá tên ứng dụng — áp CÙNG hàm cho cả hai bên, không thì lệch hình thức bị
    đọc thành lệch nội dung. Tập kiểm có ba tên mang ký tự vô hình: `audio\xadmack` (gạch
    nối mềm), `yandex\xa0maps` (khoảng trắng cứng), `contacts﻿+` (BOM) — mắt thường
    không thấy, mà so chuỗi thì trượt."""
    s = (s or "").replace("\xad", "").replace("\xa0", " ").replace("﻿", "")
    return " ".join(s.lower().split()).strip(" .")


def _act(a):
    """`action` lưu dạng dict hoặc chuỗi repr của dict tuỳ khâu dựng."""
    if isinstance(a, dict):
        return a
    try:
        return ast.literal_eval(a)
    except Exception:
        return {}


def train_apps(path):
    """Ứng dụng có mặt trong tập dạy, trả về (tập hợp, thống kê để in ra).

    Nguồn CHÍNH = `action.open_app.app_name`, đúng trường `build_test_data.app_of` dùng
    cho tập kiểm. Nguồn PHỤ = câu chuẩn dạng "Open the X app" trong lịch sử, để bắt các
    tác vụ mở ứng dụng bằng cách bấm thay vì bằng thao tác `open_app` — tập kiểm không
    gán được app cho nhóm đó, nhưng ứng dụng thì vẫn có mặt trong dữ liệu dạy.

    KHÔNG quét `goal`: câu mục tiêu dài khớp regex và đẻ ra tên rác (xem đầu tệp).
    """
    chinh, phu = set(), set()
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        a = _act(r.get("action"))
        if a.get("action_type") == "open_app" and a.get("app_name"):
            chinh.add(norm(a["app_name"]))
        for h in (r.get("history") or []):        # mọi dòng, không dừng ở dòng đầu
            m = RX_OPEN.match((h or "").strip())
            if m:
                phu.add(norm(m.group(1)))
    chinh.discard("")
    phu.discard("")
    return chinh | phu, {"chinh": len(chinh), "phu_them": len(phu - chinh)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default=TRAIN)
    ap.add_argument("--test", default=TEST)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not os.path.exists(a.train):
        sys.exit(f"Chưa có tập dạy: {a.train}. Chạy build_train_data.py trước.")
    seen, nguon = train_apps(a.train)
    recs = [json.loads(l) for l in open(a.test, encoding="utf-8")]

    old = collections.Counter(r.get("app_seen_in_train") for r in recs)
    changed = 0
    chua = collections.Counter()
    for r in recs:
        app = norm(r.get("app"))
        new = (app in seen) if app else None
        if new != r.get("app_seen_in_train"):
            changed += 1
        if new is False:
            chua[app] += 1
        r["app_seen_in_train"] = new
    new_c = collections.Counter(r.get("app_seen_in_train") for r in recs)

    print(f"Ứng dụng có trong tập dạy : {len(seen)}"
          f"  (trường app_name {nguon['chinh']} + suy từ câu chữ {nguon['phu_them']})")
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

    # In hẳn danh sách để soi bằng mắt: lát cắt phụ này nhỏ, một cái tên gán nhầm cũng
    # đủ đổi con số. Tên trông quen mà nằm ở đây thì gần như chắc là lỗi chuẩn hoá.
    if chua:
        print(f"\n{len(chua)} ứng dụng CHƯA thấy lúc dạy ({sum(chua.values())} bước):")
        for app, n in chua.most_common():
            print(f"  {n:5}  {app}")

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
