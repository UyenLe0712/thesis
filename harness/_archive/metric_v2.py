# -*- coding: utf-8 -*-
"""
Thước v2 — bản đã VÁ các lỗi cơ học mà report/90 §B chỉ ra. Giữ v1 (metric_v1_validate.py)
làm bản ghi lịch sử, KHÔNG sửa. Đây là thước dùng để chấm thật (khi có output model).

Các sửa so với v1:
 (1) target_of: bỏ verb CHỈ ở vị trí đầu câu → nhãn nút Next/Back/Open/Enter/Go SỐNG SÓT
     (v1 đưa chúng vào STOP → 3.2% bước rút về target rỗng).
 (2) đích rỗng: KHÔNG cho khớp (trả 0), đếm riêng thành "không phân xử được"
     (v1 để target_score(' ',' ')=1.0 → 'Tap Next' khớp 'Tap Back').
 (3) luật cứng: khác token TOGGLE (on/off, up/down, show/hide...) hoặc khác SỐ hoặc
     một bên là SIÊU-TẬP của bên kia (Tools ⊂ Tools & Hardware) → KHÔNG khớp bất kể điểm.
 (4) coverage: ghép 1-1 tối ưu (không cho 1 model-step phủ nhiều gold-step)
     (v1 là phủ-tập → 12.4% bước gold bị 1 gold-step khác phủ oan).
 (5) bỏ dấu câu khi tách token.
"""
import re, math, json, urllib.request

EMB_URL = "http://localhost:11434/v1/embeddings"
TAU_BGE = 0.85
J_MATCH = 0.5

# verb = từ HÀNH ĐỘNG, chỉ bỏ khi ở đầu câu (vì cũng có thể là nhãn nút: "Tap the Enter button")
VERBS = {"tap", "click", "press", "select", "choose", "touch", "type", "enter", "input",
         "fill", "write", "scroll", "swipe", "drag", "long", "long-press", "hold",
         "open", "launch", "go", "navigate", "return", "set", "toggle", "turn"}
ACTION_MAP = {
    "tap": "tap", "click": "tap", "press": "tap", "select": "tap", "choose": "tap", "touch": "tap",
    "type": "type", "enter": "type", "input": "type", "fill": "type", "write": "type",
    "scroll": "scroll", "swipe": "scroll", "drag": "scroll",
    "long": "long_press", "hold": "long_press",
    "open": "open", "launch": "open",
    "go": "navigate", "navigate": "navigate", "back": "navigate", "return": "navigate",
}
# filler = bỏ ở MỌI vị trí (KHÔNG chứa nhãn nút như next/back/open/enter/go/select)
FILLER = set("the a an on to of in into at for your my this that it is are be and or please "
             "then now with button icon buttons icons".split())
LOCATION = set("top bottom left right upper lower centre center corner side middle screen "
               "page here below above".split())
# cặp đối nghịch — khác một trong hai chiều = xung đột cứng
TOGGLE_PAIRS = [("on", "off"), ("enable", "disable"), ("enabled", "disabled"),
                ("show", "hide"), ("mute", "unmute"), ("up", "down"),
                ("add", "remove"), ("expand", "collapse"), ("start", "stop"),
                ("previous", "next"), ("forward", "back")]
TOGGLE = {w: i for i, (a, b) in enumerate(TOGGLE_PAIRS) for w in (a, b)}
TOGGLE_SIDE = {a: 0 for a, b in TOGGLE_PAIRS}
TOGGLE_SIDE.update({b: 1 for a, b in TOGGLE_PAIRS})


def words(text):
    return re.findall(r"[a-z0-9@._&]+", (text or "").lower())


def canon_action(text):
    for w in words(text):
        if w in ACTION_MAP:
            return ACTION_MAP[w]
    return "tap"


def target_of(text):
    """Lấy phần ĐÍCH: bỏ verb đầu câu + cụm vị trí + filler; GIỮ nhãn nút, số, từ phủ định."""
    t = (text or "").lower()
    t = re.sub(r'["“”\'.,!?:;()\[\]]', " ", t)                    # bỏ dấu câu
    t = re.sub(r"\b(at|in|on|to)\s+the\s+(top|bottom|left|right|upper|lower|centre|center)[\w\s]*", " ", t)
    toks = words(t)
    # bỏ verb CHỈ ở đầu (một hoặc hai token đầu nếu là verb)
    while toks and toks[0] in VERBS:
        toks.pop(0)
    out = [w for w in toks if w not in FILLER and w not in LOCATION and len(w) > 1]
    return " ".join(out)


def content_set(t):
    return set(w for w in words(t) if len(w) > 1)


def hard_conflict(t1, t2):
    """True nếu hai đích chắc chắn KHÁC nút (toggle ngược / số khác / siêu-tập)."""
    s1, s2 = content_set(t1), content_set(t2)
    # toggle ngược chiều
    for w in s1:
        if w in TOGGLE:
            opp = [b if a == w else a for a, b in TOGGLE_PAIRS if w in (a, b)][0]
            if opp in s2:
                return True
    # số khác nhau
    n1 = set(w for w in s1 if w.isdigit())
    n2 = set(w for w in s2 if w.isdigit())
    if (n1 or n2) and n1 != n2:
        return True
    # một bên là siêu-tập THỰC của bên kia + có thêm token nội dung → nút cụ thể hơn = nút khác
    core1 = s1 - {"of", "and"}
    core2 = s2 - {"of", "and"}
    if core1 and core2 and core1 != core2 and (core1 < core2 or core2 < core1):
        return True
    return False


_c = {}
def _emb(texts):
    miss = [t for t in dict.fromkeys(texts) if t not in _c]
    for i in range(0, len(miss), 64):
        ch = miss[i:i + 64]
        data = json.dumps({"model": "bge-m3", "input": ch}).encode()
        req = urllib.request.Request(EMB_URL, data=data, headers={"Content-Type": "application/json"})
        res = json.loads(urllib.request.urlopen(req, timeout=300).read())
        for t, d in zip(ch, res["data"]):
            _c[t] = d["embedding"]


def _cos(a, b):
    d = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(y * y for y in b))
    return d / (na * nb + 1e-9)


def target_score(t1, t2, use_bge=True):
    """Điểm khớp đích [0,1]. Đích rỗng → 0 (không phân xử). Xung đột cứng → 0."""
    if not t1.strip() or not t2.strip():
        return -1.0        # cờ "không phân xử được" (đích rỗng)
    if hard_conflict(t1, t2):
        return 0.0
    s1, s2 = content_set(t1), content_set(t2)
    j = len(s1 & s2) / len(s1 | s2) if (s1 | s2) else 0.0
    if j >= J_MATCH:
        return j
    if use_bge:
        _emb([t1, t2])
        b = _cos(_c[t1], _c[t2])
        if b >= TAU_BGE:
            return b
    return j


def step_match(m, g, use_bge=True):
    """(action, target) khớp? trả (bool, score, adjudicable)."""
    a_ok = canon_action(m) == canon_action(g)
    ts = target_score(target_of(m), target_of(g), use_bge)
    if ts < 0:
        return (False, ts, False)      # đích rỗng — không phân xử
    return (a_ok and ts >= J_MATCH, ts, True)


def coverage(model_steps, gold_steps, use_bge=True):
    """% gold-step phủ được, GHÉP 1-1 (mỗi model-step dùng tối đa 1 lần) — Kuhn."""
    if not gold_steps:
        return 1.0
    # cạnh: gold g <-> model m nếu step_match
    adj = [[j for j, m in enumerate(model_steps) if step_match(m, g, use_bge)[0]]
           for g in gold_steps]
    matchR = [-1] * len(model_steps)

    def try_k(u, seen):
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                if matchR[v] == -1 or try_k(matchR[v], seen):
                    matchR[v] = u
                    return True
        return False

    cov = 0
    for u in range(len(gold_steps)):
        if try_k(u, [False] * len(model_steps)):
            cov += 1
    return cov / len(gold_steps)
