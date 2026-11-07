# -*- coding: utf-8 -*-
"""
Thước executability — bản VÁ lỗ density (report/96 #4, report/98 §4). Dùng lúc chấm trên Colab.

Vấn đề: dung sai đĩa 14% (~151px) quá rộng — 63.2% bước có nút KHÁC nằm trong đĩa
(ac_density_check) → câu trỏ nhầm sang nút cạnh vẫn được cho qua (thước dễ dãi).

Vá:
 1. Chấm theo NÚT-ĐÚNG-GẦN-NHẤT (Voronoi): điểm bộ trỏ tính TRÚNG chỉ khi nút gold là
    nút GẦN NHẤT với nó (trong số mọi nút trên màn), KHÔNG chỉ "nằm trong đĩa".
    → câu trỏ gần một nút-cạnh-khác thì TRẬT, dù vẫn lọt đĩa quanh gold.
 2. Báo CẢ HAI (đĩa + Voronoi) để minh bạch; headline dùng Voronoi (chặt hơn).
 3. Luật cứng ĐẢO NGHĨA (report/96 #1): câu và gold khác trạng-thái-đích (on/off, show/hide,
    up/down...) → TRẬT bất kể toạ độ (executability mù với toggle nếu chỉ xét toạ độ).

Đầu vào một bước: điểm bộ trỏ (px,py) · toạ-độ gold (gx,gy) · danh sách tâm-nút trên màn
(từ VH hoặc OCR) · câu mô hình + câu gold (để xét thao-tác & đảo-nghĩa).
"""
import re, math

# CHỈ giữ cặp trạng thái dùng CHUNG một vị trí chạm — đó là chỗ duy nhất kênh toạ độ mù,
# nên cũng là chỗ duy nhất cần luật câu chữ. Đã bỏ khỏi bảng cũ: up/down và các từ chỉ vị
# trí (không phải trạng thái), add/remove và open/close (hai nút khác nhau — kênh toạ độ
# bắt được, mà "open" giờ là một cách nói của chạm nên giữ lại sẽ kết oan).
TOGGLE_PAIRS = [("on", "off"), ("enable", "disable"), ("enabled", "disabled"),
                ("show", "hide"), ("mute", "unmute"), ("expand", "collapse"),
                ("check", "uncheck"), ("select", "deselect"), ("start", "stop")]
_TOG = {}
for _a, _b in TOGGLE_PAIRS:
    _TOG[_a] = _b; _TOG[_b] = _a

# Gộp mọi cách nói của cùng MỘT cú chạm vào một lớp. Đo trên 91 cặp (câu teacher thật, câu
# gold) cho thấy bảng cũ tách "tap" khỏi "open"/"go to"/"select" nên bác oan 28.6% số cặp —
# đúng bệnh của thước so chuỗi cũ, chỉ đổi vỏ. Trên giao diện, "tap X", "open X", "go to X"
# đều là chạm vào X; phân biệt thật chỉ nằm ở chạm / gõ / cuộn.
ACTION_MAP = {
    "tap": "tap", "click": "tap", "press": "tap", "select": "tap", "choose": "tap", "touch": "tap",
    "open": "tap", "launch": "tap", "go": "tap", "navigate": "tap", "visit": "tap", "view": "tap",
    "type": "type", "enter": "type", "input": "type", "fill": "type", "write": "type",
    "scroll": "scroll", "swipe": "scroll", "drag": "scroll",
    "long": "long_press", "hold": "long_press",
    "back": "navigate_back", "return": "navigate_back",
}


def canon_action(text, strict_back=False):
    """Quy câu về một lớp thao tác.

    ⚠️ LỖI ĐÃ BIẾT (phát hiện 16/8/2026, giữ nguyên hành vi mặc định để ba nhánh đã
    chấm còn tái lập được): vòng quét chạy từ trái sang, mà `go` và `navigate` (→ tap)
    đứng trước `back` trong câu, nên `go back`, `navigate back`, `press the back
    button` đều ra "tap" — lớp `navigate_back` gần như không thể đạt tới. Đo được ảnh
    hưởng trên quần thể chấm (toàn bước chạm): 81 bước đổi phán quyết ở s1, 47 ở base,
    0 ở nhánh trần; điểm đổi 59,12 → 58,81 và 47,60 → 47,40, chênh lệch giữa hai nhánh
    gần như không đổi.

    Vì `report/106` khoá thước trước khi có điểm, ta KHÔNG chấm lại ba nhánh bằng bản
    vá — sửa thước sau khi thấy điểm đúng là thứ hồ sơ đăng ký sinh ra để chặn, kể cả
    khi sửa làm số xấu đi. Bản vá bật bằng `strict_back=True` và **bắt buộc** dùng cho
    phép kiểm không-gây-hại trên bước không-chạm (nơi thao tác `back` là thật và
    chiếm phần đáng kể), vì phép kiểm đó chưa chạy lần nào. Xem `report/106` mục sửa
    đổi (v)."""
    ws = re.findall(r"[a-z]+", (text or "").lower())
    if strict_back and "back" in ws:
        return "navigate_back"
    for w in ws:
        if w in ACTION_MAP:
            return ACTION_MAP[w]
    return "tap"


# ĐÃ THỬ VÀ BỎ: một lớp trái nghĩa lấy từ WordNet. Lý do bỏ, bằng số: nó chỉ bắt thêm 3 ca
# trong bộ bơm lỗi, nhưng đẻ mâu thuẫn giả vì đa nghĩa — "set" ↔ "rise", "enter" ↔ "leave",
# "top" ↔ "side" — khiến có câu gold tự bác chính nó. Chi phí lớn hơn lợi ích, nên luật
# quay về bảng tay và khai thẳng phần còn mù (cặp đặc thù giao diện như next/previous).
# Từ chỉ vị trí xuất hiện dày đặc trong hướng dẫn giao diện, và WordNet coi vài cặp trong
# đó là trái nghĩa (top ↔ side) — đủ để một câu gold tự mâu thuẫn với chính nó. Chặn hẳn.
POSITION_WORDS = {"top", "bottom", "left", "right", "side", "up", "down", "above", "below",
                  "front", "back", "center", "centre", "middle", "first", "last", "next",
                  "previous", "in", "out", "inside", "outside", "upper", "lower"}


def toggle_conflict(a, b):
    """True nếu câu a và câu b nhắm hai trạng-thái NGƯỢC nhau của cùng một chỗ (bật vs tắt).

    Chỉ dùng bảng cặp công tắc soạn tay, sau khi loại từ chỉ vị trí. Bơm lỗi cho thấy luật
    bắt hết cặp trong bảng nhưng mù với cặp ngoài bảng — giới hạn này được báo thẳng chứ
    không nhét thêm từ vào bảng cho điểm đẹp."""
    wa = set(re.findall(r"[a-z]+", (a or "").lower()))
    wb = set(re.findall(r"[a-z]+", (b or "").lower()))
    for w in wa - POSITION_WORDS:
        if w in _TOG and _TOG[w] in wb:
            return True
    return False


def _dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def hit_disk(pred, gold, wh, tau=0.14):
    """Cách CŨ (dễ dãi): điểm trong đĩa bán kính tau*cạnh quanh gold."""
    w, h = wh
    return abs(pred[0] - gold[0]) <= tau * w and abs(pred[1] - gold[1]) <= tau * h


def min_sep_px(wh):
    """Bán kính coi là 'cùng một nút' khi danh sách nút CHỈ có tâm, không có hộp.
    Lấy 24dp quy ra pixel theo bề ngang ảnh (điện thoại tham chiếu ~411dp).

    ⚠️ Đây là đường lui, không phải cách chấm chính. Ban đầu ngưỡng này được biện minh
    bằng chuẩn Material Design ("hai nút riêng phải cách nhau ≥48dp"), nhưng kiểm lại
    trên hộp thật thì sai: 286 cặp hộp có tâm cách nhau dưới ngưỡng này lại có IoU = 0,
    tức là phần tử RIÊNG BIỆT nằm sát nhau (phím bàn phím, dòng danh sách), không phải
    hộp trùng. Khi có hộp thì dùng `hit_nearest_box` bên dưới."""
    return 24.0 * (wh[0] / 411.0)


def dedupe_buttons(buttons, gold, wh):
    """Đường lui khi chỉ có tâm nút: bỏ tâm nằm sát gold rồi gộp tâm sát nhau.

    Cách này giữ được kết quả (chênh ổn định trong dải bán kính 12–28dp) nhưng lý do thì
    thô: nó xoá nhầm cả phần tử thật nằm gần. Khi có hộp, `hit_nearest_box` xử đúng bản
    chất hơn — xem chú thích ở đó."""
    ms = min_sep_px(wh)
    kept = []
    for b in buttons:
        if _dist(b, gold) < ms:          # coi là cùng nút với gold
            continue
        if any(_dist(b, k) < ms for k in kept):
            continue
        kept.append(b)
    return [gold] + kept


def _box_dist(pt, box):
    """Khoảng cách từ một điểm tới hộp (0 nếu điểm nằm trong hộp)."""
    dx = max(box[0] - pt[0], 0, pt[0] - box[2])
    dy = max(box[1] - pt[1], 0, pt[1] - box[3])
    return math.hypot(dx, dy)


def _in_box(pt, box):
    return box[0] <= pt[0] <= box[2] and box[1] <= pt[1] <= box[3]


def hit_nearest_box(pred, gold, boxes, wh, tau=0.14):
    """Chấm theo NÚT GẦN NHẤT, dùng HỘP của bộ dò thay vì tâm.

    Vì sao phải dùng hộp: toạ độ gold là **điểm người thật chạm**, không phải tâm nút, nên
    hộp của chính nút đang chạm thường có tâm lệch vài chục pixel so với gold. Nếu so theo
    tâm, hộp của chính nút gold sẽ 'gần hơn' gold và đánh rớt oan câu đúng — đo được là
    kết oan 59% số câu cùng nghĩa. Cách xử đúng bản chất: **mọi hộp CHỨA điểm gold đều là
    nút gold**, loại chúng ra khỏi danh sách đối thủ; phần còn lại mới là nút khác.

    Trúng khi: điểm nằm trong dung sai, và không nút nào khác gần điểm hơn nút gold."""
    if not hit_disk(pred, gold, wh, tau):
        return False
    others = [b for b in boxes if not _in_box(gold, b)]
    dg = _dist(pred, gold)
    for b in others:
        if _box_dist(pred, b) < dg:
            return False
    return True


def hit_voronoi(pred, gold, buttons, wh, tau=0.14):
    """Cách MỚI (chặt): trúng khi nút gold là nút GẦN NHẤT với điểm bộ trỏ.
    buttons = danh sách tâm mọi nút trên màn (kể cả gold). Vẫn yêu cầu trong đĩa tau
    để loại ca trỏ ra xa toàn màn."""
    if not hit_disk(pred, gold, wh, tau):
        return False
    dg = _dist(pred, gold)
    for b in dedupe_buttons(buttons, gold, wh):
        if _dist(b, gold) < 1e-6:      # chính nút gold
            continue
        if _dist(pred, b) < dg:        # có nút khác gần hơn → trỏ nhầm
            return False
    return True


def content_match(model_instr, gold_text, thresh=0.6):
    """Bước GÕ: câu model có nêu đúng nội dung cần gõ không (report/98 §4b(3)).
    Khớp khi chuỗi gold nằm trong câu, hoặc ≥thresh số token của gold xuất hiện."""
    if not gold_text:
        return False
    m = (model_instr or "").lower()
    g = str(gold_text).lower().strip()
    if not g:
        return False
    if g in m:
        return True
    gt = set(re.findall(r"[\w']+", g))
    mt = set(re.findall(r"[\w']+", m))
    if not gt:
        return False
    return len(gt & mt) / len(gt) >= thresh


def direction_match(model_instr, gold_dir):
    """Bước CUỘN: hướng nêu trong câu phải khớp hướng gold, và chỉ một hướng."""
    ws = set(re.findall(r"[a-z]+", (model_instr or "").lower()))
    named = {d for d in ("up", "down", "left", "right") if d in ws}
    if not named:
        return False               # không nêu hướng → không coi là khớp
    return named == {str(gold_dir).lower()}


def score_step(model_instr, gold_instr, pred_xy, gold_xy, buttons, wh, tau=0.14):
    """Chấm một bước. Trả dict: action_ok, toggle_ok, hit_disk, hit_voronoi, executable."""
    action_ok = canon_action(model_instr) == canon_action(gold_instr)
    toggle_ok = not toggle_conflict(model_instr, gold_instr)
    hd = hit_disk(pred_xy, gold_xy, wh, tau) if pred_xy else False
    hv = hit_voronoi(pred_xy, gold_xy, buttons, wh, tau) if pred_xy else False
    # executable (headline = Voronoi + action + không đảo nghĩa)
    executable = bool(action_ok and toggle_ok and hv)
    return {"action_ok": action_ok, "toggle_ok": toggle_ok,
            "hit_disk": hd, "hit_voronoi": hv, "executable": executable}


# ---- tự kiểm (chứng minh vá có tác dụng) ----
if __name__ == "__main__":
    W, H = 1080, 2400
    print("TEST 1 — trỏ nhầm sang nút cạnh (đúng lỗ density):")
    gold = (854, 2275)
    # nút cạnh THẬT phải cách gold ít nhất một vùng chạm (48dp ≈ 126px ở ảnh 1080) —
    # gần hơn thế thì theo chuẩn nền tảng nó là cùng một nút, không phải nút khác.
    confuser = (1010, 2275)         # cách gold 156px
    buttons = [gold, confuser, (200, 400)]
    pred = (960, 2275)              # cách gold 106, cách confuser 50 → gần nút cạnh hơn
    print("  đĩa 14% (cũ):", hit_disk(pred, gold, (W, H)), "← cho qua (SAI, dễ dãi)")
    print("  Voronoi (mới):", hit_voronoi(pred, gold, buttons, (W, H)), "← BÁC (đúng)")
    assert hit_disk(pred, gold, (W, H)) and not hit_voronoi(pred, gold, buttons, (W, H))

    print("\nTEST 2 — trỏ đúng nút gold (không có nút cạnh gần hơn):")
    pred2 = (860, 2270)
    print("  đĩa:", hit_disk(pred2, gold, (W, H)), "| Voronoi:", hit_voronoi(pred2, gold, buttons, (W, H)))
    assert hit_voronoi(pred2, gold, buttons, (W, H))

    print("\nTEST 3 — đảo nghĩa on/off (cùng toạ độ công tắc):")
    r = score_step("Turn off notifications", "Turn on notifications", (860, 2270), gold, buttons, (W, H))
    print("  toggle_ok:", r["toggle_ok"], "| executable:", r["executable"], "← BÁC (đúng, dù toạ độ trúng)")
    assert not r["executable"] and not r["toggle_ok"]

    print("\nTEST 4 — bước đúng hoàn chỉnh:")
    r2 = score_step("Tap the Filter button", "Click on filter option", (860, 2270), gold, buttons, (W, H))
    print("  ", r2)
    assert r2["executable"]

    # ── hai ca dưới đây phơi đúng chỗ Voronoi thủng khi inventory KHÔNG hoàn hảo
    print("\nTEST 5 — inventory NHIỄU: bộ dò trả thêm hộp trùng lên chính nút gold")
    dup = (gold[0] + 12, gold[1] - 9)      # hộp thứ hai của cùng nút gold, lệch 15px (< 63px)
    noisy = [gold, dup, confuser, (200, 400)]
    print("  chưa khử trùng, nút gold bị bản sao của nó đánh bại:",
          "gold thua" if _dist(pred2, dup) < _dist(pred2, gold) else "gold thắng")
    print("  sau khử trùng:", hit_voronoi(pred2, gold, noisy, (W, H)), "← giữ đúng (bản sao bị gộp)")
    assert hit_voronoi(pred2, gold, noisy, (W, H))

    print("\nTEST 6 — inventory THIẾU: bộ dò bỏ sót nút icon nằm cạnh gold")
    thieu = [gold, (200, 400)]              # confuser bị bỏ sót
    pred_lech = (960, 2275)                 # vẫn là điểm trỏ nhầm sang nút cạnh
    print("  Voronoi với inventory thiếu:", hit_voronoi(pred_lech, gold, thieu, (W, H)),
          "← LỌT (thước không thấy nút cạnh nên không bác được)")
    assert hit_voronoi(pred_lech, gold, thieu, (W, H))
    print("  → giới hạn thật: Voronoi chỉ chặt bằng đúng độ đầy đủ của bộ dò phần tử.")
    print("\n✅ tất cả test qua — vá density + toggle đúng; hai giới hạn inventory được nêu rõ.")
