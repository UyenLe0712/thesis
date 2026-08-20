# -*- coding: utf-8 -*-
"""FREE · offline — dựng hai nhánh ĐỐI CHỨNG TRẦN-SÀN cho thước executability.

Bài đang đọc mọi điểm trên nền **trần 75,7%**, nhưng **chưa ai đo SÀN**. Không có sàn thì hai
câu hỏi cốt lõi về tính hợp lệ của thước không có câu trả lời:

  1. Bộ trỏ trúng bao nhiêu khi câu **không mang thông tin gì**? Nếu là 40% thì dải hữu dụng
     thật là 40→75,7, và Base 47,6% chỉ hơn "không nói gì" có 7 điểm — cách đọc đổi hẳn.
  2. Thước đo **GỌI TÊN** phần tử hay đo **CHỈ CHỖ**? `p3_nopos` cho thấy bỏ mệnh đề vị trí
     mất 3,5 pp, tức vị trí CÓ đóng góp. Câu hỏi ngược chưa hỏi: giữ vị trí, bỏ tên thì sao?

Hai nhánh:

  f1_trong    mọi bước dùng CÙNG một câu vô nội dung ("Tap the button.")
              → sàn tuyệt đối. Điểm ở đây là phần bộ trỏ đoán trúng mà KHÔNG cần câu.

  f3_lechman  lấy nguyên CÂU CHUẨN CỦA MỘT BƯỚC KHÁC (tác vụ khác) — câu thật, đúng văn
              phong, đúng độ dài, chỉ **sai màn hình**
              → đối chứng cho f1. Câu "Tap the button." lặp mọi bước là đầu vào LẠC PHÂN BỐ;
              bộ trỏ có thể hành xử bất thường vì lạ chứ không vì vô nghĩa. f3 loại đúng
              cách giải thích đó: nó bình thường về mọi mặt trừ nội dung.

  f2_khongten giữ nguyên mệnh đề vị trí của câu chuẩn, THAY tên phần tử bằng từ chung
              ("Click on the search icon at the top right corner"
               → "Click on the item at the top right corner")
              → đo phần đóng góp của việc GỌI TÊN. Đây là phép nghịch đảo của `p3_nopos`.

Cách đọc đã định TRƯỚC khi có số:

| thấy gì | nghĩa là |
|---|---|
| `f1_trong` gần 0 | thước đòi câu phải mang thông tin — dải 0→75,7 dùng được nguyên |
| `f1_trong` cao (>30%) | ⚠ phần lớn điểm là bộ trỏ tự đoán; mọi con số phải đọc trên nền SÀN, không phải 0 |
| `f2_khongten` ≈ trần | ⛔ thước đo CHỈ CHỖ chứ không đo GỌI TÊN ⇒ tên bài phải đổi |
| `f2_khongten` tụt mạnh | ✔ gọi tên là phần đóng góp chính — đúng thứ bài tuyên bố đo |
| `f3_lechman` ≈ `f1_trong` | ✔ f1 là sàn công bằng; điểm sàn không phải hiệu ứng "câu kỳ quặc" |
| `f3_lechman` **cao hơn** `f1_trong` nhiều | ⚠ bộ trỏ thưởng cho câu ĐÚNG VĂN PHONG bất kể nội dung ⇒ nhiễm văn phong có thật và đo được, phải khai |
| `f3_lechman` **thấp hơn** `f1_trong` | bộ trỏ bị câu sai dẫn đi lạc — sàn thật còn thấp hơn f1 |

⚠️ `f2_khongten` chỉ dựng được ở bước có mệnh đề vị trí (~26%), nên đọc theo **phần bị đụng**,
đừng đọc số tổng — hệ số pha loãng ~3,8× (xem `paper/fair2026/PHEP_A_DIEN_DAT_LAI.md`).

Chạy: python3 harness/make_floor.py
Ra:   runs/floor/preds_{f1_trong,f2_khongten,f3_lechman}.jsonl
"""
import os, re, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
TEST = os.path.join(HERE, "dg1_cache", "test_ac", "test.jsonl")
OUT = os.path.abspath(os.path.join(HERE, "..", "runs", "floor"))
CAU_TRONG = "Tap the button."
SEED = 20260805

# dùng LẠI nguyên hai biểu thức của make_paraphrase để hai phép kiểm so được với nhau
POS_RE = re.compile(
    r"\s*(?:,\s*)?\b((?:at|in|on|near|to)\s+the\s+"
    r"(?:top|bottom|upper|lower|left|right|middle|centre|center)[^,.]*)\.?$", re.I)
HEAD_RE = re.compile(r"^\s*(click|tap|press|select|choose|touch)\s+(on\s+|the\s+)?", re.I)
CON_LAI = re.compile(r"^\s*(click|tap|press|select|choose|touch)\s*(on)?\s*(the)?\s*$", re.I)
WIDGET = re.compile(
    r"\b(icons?|buttons?|btn|tabs?|fields?|bars?|menus?|options?|items?|images?|"
    r"photos?|links?|checkbox|arrows?|dots?|tick|toggle|switch|slider|cards?|"
    r"thumbnails?|avatar|logo)\b", re.I)


def f2_khongten(s):
    """Giữ động từ + mệnh đề vị trí, thay TÊN phần tử bằng từ chung."""
    m = POS_RE.search(s)
    if not m:
        return None
    main, pos = s[:m.start()].strip().rstrip(",").rstrip("."), m.group(1).strip()
    if CON_LAI.match(main + " ") or WIDGET.search(pos):
        return None            # cùng hai cổng chặn của make_paraphrase
    h = HEAD_RE.match(main)
    if not h:
        return None
    return f"{main[:h.end(1)]} on the item {pos}."


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = [json.loads(l) for l in open(TEST, encoding="utf-8")]
    touch = [r for r in rows
             if r["action"].get("action_type") in ("click", "long_press") and "x" in r["action"]]

    # f3: câu chuẩn của một bước thuộc TÁC VỤ KHÁC. Hạt giống cố định để tái lập.
    rng = random.Random(SEED)
    khac = {}
    for i, r in enumerate(touch):
        while True:
            o = touch[rng.randrange(len(touch))]
            if o["episode_id"] != r["episode_id"]:
                break
        khac[(r["episode_id"], r["step_id"])] = o["gold_instruction"].strip()

    for ten, fn in [("f1_trong", lambda g: CAU_TRONG),
                    ("f2_khongten", f2_khongten),
                    ("f3_lechman", None)]:
        n_ok = 0
        p = os.path.join(OUT, f"preds_{ten}.jsonl")
        with open(p, "w", encoding="utf-8") as f:
            for r in touch:
                g = r["gold_instruction"]
                new = khac[(r["episode_id"], r["step_id"])] if ten == "f3_lechman" else fn(g)
                n_ok += 1 if new else 0
                f.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"],
                                    "pred": (new if new else g).strip()},
                                   ensure_ascii=False) + "\n")
        print(f"{ten:12s}: {n_ok}/{len(touch)} bước đổi được ({n_ok/len(touch)*100:.1f}%) → {p}")

    print("\nVí dụ f2_khongten:")
    dem = 0
    for r in touch:
        v = f2_khongten(r["gold_instruction"])
        if v:
            print(f"  gốc : {r['gold_instruction'].strip()}")
            print(f"  đổi : {v}")
            dem += 1
            if dem == 4:
                break


if __name__ == "__main__":
    main()
