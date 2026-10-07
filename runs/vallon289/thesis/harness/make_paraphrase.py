# -*- coding: utf-8 -*-
"""FREE · offline — dựng tệp preds cho PHÉP KIỂM DIỄN ĐẠT LẠI.

Vì sao cần. Jandial et al. (Findings EACL 2026) báo bộ trỏ GUI trượt tới 84% khi đổi
cách diễn đạt. Đó là đòn bắn thẳng vào thước của bài. Bộ bơm lỗi hiện có KHÔNG trả lời
được, vì nó không gọi bộ trỏ lần nào — nó đặt sẵn một điểm tổng hợp rồi hỏi cổng chữ.
Phép kiểm đúng: lấy CÂU CHUẨN (đã biết bộ trỏ giải được, trần 75,7%), viết lại giữ
nguyên nghĩa, rồi cho bộ trỏ chạy lại. Trần tụt bao nhiêu chính là câu trả lời.

Bốn mức, mỗi mức giữ nguyên TÊN phần tử — đổi tên là đổi nghĩa, không còn là paraphrase:
  p1_verb   đổi động từ mở đầu (click → tap/press/select/choose)
  p2_order  đưa mệnh đề vị trí lên đầu câu
  p3_nopos  bỏ hẳn mệnh đề vị trí, giữ tên phần tử
  p4_both   p1 + p2 cùng lúc (xa nhất khỏi câu gốc mà vẫn giữ nghĩa)

⚠️ p3 KHÔNG bảo toàn thông tin: bỏ vị trí thì câu nghèo đi thật. Nó ở đây để tách hai
nguyên nhân — bộ trỏ nhạy với CÁCH NÓI, hay nhạy với LƯỢNG THÔNG TIN. Phải đọc riêng.

Chạy: python3 harness/make_paraphrase.py
Ra:   runs/paraphrase/preds_para_{p1_verb,p2_order,p3_nopos,p4_both}.jsonl
"""
import os, re, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
TEST = os.path.join(HERE, "dg1_cache", "test_ac", "test.jsonl")
OUT = os.path.abspath(os.path.join(HERE, "../runs/paraphrase"))
os.makedirs(OUT, exist_ok=True)
SEED = 20260805

# Hậu tố tệp ra. Đặt "_v2" từ 17/8 để KHÔNG đè lên bốn tệp đã chấm trên Kaggle bằng bản
# regex lỗi — chúng là bản ghi của lượt chấm ấy, đè đi là mất khả năng đối chiếu.
# Chỉ `p3_nopos` cần chấm lại: `p1_verb` không dùng POS_RE, còn `p2_order`/`p4_both` chỉ
# ĐẢO chỗ mệnh đề nên lỗi regex làm câu lủng củng chứ không mất chữ nào.
VER = "_v2"

VERBS = ["Tap", "Press", "Select", "Choose"]

# Mệnh đề vị trí ở cuối câu: "... at the top right corner of the screen".
#
# ⚠️ BẢN ĐẦU SAI VÀ ĐÃ ĐỔI HƯỚNG KẾT QUẢ (bắt 17/8, xem `paper/fair2026/PHEP_A_DIEN_DAT_LAI.md`).
# Bản cũ chỉ đòi `(at|in|on) the (top|bottom|left|right|…)` rồi cho `[^,.]*` chạy tới hết
# câu. Nhưng *left/right/center* cũng nằm TRONG TÊN phần tử — "the left arrow icon",
# "the Right Tick icon" — nên `re.search` (khớp trái nhất) bắt đầu ngay ở "on the left
# arrow icon …" và mệnh đề "vị trí" ngốn luôn cả tên. `p3_nopos` xoá mệnh đề đó ⇒ **7/211
# câu trơ lại "Tap."**, tức mất hẳn thứ bộ trỏ phải giải. Chạy trơn, và nó rơi đúng vào
# nhánh DUY NHẤT có hiệu ứng: hiệu ứng thô −4,7 pp, lành −3,4 pp ⇒ **28% là do lỗi này**.
#
# Vá bằng HAI CỔNG CHẶN thay vì siết regex. Siết regex (đòi đuôi kết bằng
# corner/side/of-the-screen) đã thử và bị loại: nó chặn hết 7 ca xấu nhưng giết luôn ca
# lành *"… at the top right corner of the screen to search the flight"* — mệnh đề vị trí
# nằm giữa câu nên không khớp `$`. Cổng chặn nhắm đúng cái sai mà không đụng ca lành.
POS_RE = re.compile(
    r"\s*(?:,\s*)?\b((?:at|in|on|near|to)\s+the\s+"
    r"(?:top|bottom|upper|lower|left|right|middle|centre|center)[^,.]*)\.?$",
    re.I)
HEAD_RE = re.compile(r"^\s*(click|tap|press|select|choose|touch)\s+(on\s+|the\s+)?", re.I)
# Cổng A — bỏ mệnh đề xong còn trơ động từ: không còn là phép bỏ vị trí nữa.
CON_LAI = re.compile(r"^\s*(click|tap|press|select|choose|touch)\s*(on)?\s*(the)?\s*$", re.I)
# Cổng B — mệnh đề bị bỏ có gọi tên một thứ bấm được: mệnh đề vị trí thật không làm vậy.
# Bắt ca regex ăn một PHẦN tên mà cổng A không thấy (vì phần còn lại vẫn có chữ).
# ⚠️ Chỉ DANH TỪ chỉ phần tử. Bản đầu có cả động từ chung (search/back/save/…) và chặn oan
# *"… at the top right corner of the screen to search the flight"* — chữ "search" ở đó
# thuộc mệnh đề mục đích, không phải tên nút. Cả 7 ca xấu đều đã bị cổng A bắt, nên cổng B
# chỉ cần làm lưới an toàn cho ca ăn một PHẦN tên.
WIDGET = re.compile(
    r"\b(icons?|buttons?|btn|tabs?|fields?|bars?|menus?|options?|items?|images?|"
    r"photos?|links?|checkbox|arrows?|dots?|tick|toggle|switch|slider|cards?|"
    r"thumbnails?|avatar|logo)\b", re.I)


def split_pos(s):
    """Tách câu thành (phần chính, mệnh đề vị trí) — mệnh đề rỗng nếu không có."""
    m = POS_RE.search(s)
    if not m:
        return s.strip().rstrip("."), ""
    return s[:m.start()].strip().rstrip(",").rstrip("."), m.group(1).strip()


def p1_verb(s, rng):
    m = HEAD_RE.match(s)
    if not m:
        return None
    v = rng.choice(VERBS)
    rest = s[m.end():]
    keep = (m.group(2) or "").strip()
    # "Click on the X" -> "Tap the X"; "Click on X" -> "Tap X"
    return f"{v} {('the ' if keep.lower() == 'the' else '')}{rest}".strip()


def p2_order(s, rng):
    main, pos = split_pos(s)
    if not pos or not main:
        return None
    main = main[0].lower() + main[1:]
    return f"{pos[0].upper()}{pos[1:]}, {main}."


def p3_nopos(s, rng):
    main, pos = split_pos(s)
    if not pos or not main:
        return None
    # Hai cổng chặn. Bỏ vị trí xong câu vẫn phải còn TÊN phần tử, và mệnh đề bị bỏ không
    # được chứa tên một thứ bấm được — nếu có thì regex đã ăn vào tên, không phải vị trí.
    if CON_LAI.match(main + " ") or WIDGET.search(pos):
        return None
    return main + "."


def p4_both(s, rng):
    a = p1_verb(s, rng)
    if not a:
        return None
    return p2_order(a, rng)


VARIANTS = {"p1_verb": p1_verb, "p2_order": p2_order, "p3_nopos": p3_nopos, "p4_both": p4_both}


def main():
    rows = [json.loads(l) for l in open(TEST, encoding="utf-8")]
    touch = [r for r in rows
             if r["action"].get("action_type") in ("click", "long_press") and "x" in r["action"]]
    os.makedirs(OUT, exist_ok=True)
    for name, fn in VARIANTS.items():
        rng = random.Random(SEED)
        n_ok = 0
        path = os.path.join(OUT, f"preds_para_{name}{VER}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for r in touch:
                g = r["gold_instruction"]
                new = fn(g, rng)
                # không đổi được thì giữ nguyên câu chuẩn: nhánh này phải so được với
                # trần trên CÙNG quần thể, nên không được bỏ bước nào
                #
                # ⚠️ PHẢI `.strip()` (vá 17/8). Bản đầu ghi `g` nguyên xi, mà 72/589 câu chuẩn
                # có **dấu cách ở cuối** trong khi `preds_ceiling_human.jsonl` đã strip sạch
                # (0/6.958). Hậu quả: ở những bước biến thể KHÔNG đổi được — tức lẽ ra phải
                # trùng khít lượt trần — bộ trỏ lại nhận một chuỗi khác một ký tự, và trả
                # toạ độ khác ở **6 bước**, trong đó **1 bước đổi hẳn kết luận** (lệch tới
                # 1.219 px = 113% bề ngang). Bộ trỏ tất định; chính đầu vào khác nhau.
                # Đủ nhỏ để không đổi kết luận nào (0,125 pp trên tổng, và bước đó nằm NGOÀI
                # phần được viết lại nên không đụng số ghép cặp), nhưng nó phá mất khả năng
                # ghép kết quả từ tệp thô — thứ tiết kiệm cả giờ GPU.
                out = (new if new else g).strip()
                n_ok += 1 if new else 0
                # ⚠️ khoá phải là "pred" — `score_run.load_preds` đọc đúng khoá đó và
                # trả chuỗi rỗng nếu thiếu, tức là chạy trơn mà chấm toàn câu rỗng.
                f.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"],
                                    "pred": out}, ensure_ascii=False) + "\n")
        print(f"{name:9s}: {n_ok}/{len(touch)} bước đổi được ({n_ok/len(touch)*100:.1f}%) → {path}")
    # vài ví dụ để mắt người kiểm được là paraphrase có giữ nghĩa không
    print("\nVí dụ:")
    rng = random.Random(SEED)
    for r in touch[:4]:
        g = r["gold_instruction"]
        print(f"  gốc     : {g}")
        for name, fn in VARIANTS.items():
            v = fn(g, random.Random(SEED))
            if v:
                print(f"  {name:9s}: {v}")
        print()


if __name__ == "__main__":
    main()
