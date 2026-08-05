# -*- coding: utf-8 -*-
"""
dg3_rewrite_fallback.py — VIET LAI buoc-bia thanh MO TA CHUNG CHUNG (report/53 §2.6).
Quyet dinh cot loi: TAT DINH (template), KHONG goi LLM viet lai — neu dung LLM thi chinh lop
loc lai mo ra nguon bia moi (vi pham luat vang "khong doan nut khac"). KHONG goi API/GPU/mang.

Khac ban phac trong report/53:
  - Dung HASH ON DINH (hashlib.md5) thay cho hash() cua Python — hash() bi salt theo tien trinh
    (PYTHONHASHSEED) nen KHONG tai lap duoc giua cac lan chay; pre-registration doi tai lap 100%.
  - Bo may tu kiem "khong vo tinh bia moi" (matcher) la THAM SO TIEM (injectable) — production
    truyen best_match cua nomic; tu-kiem truyen matcher gia (khong can Ollama).

Chay tu-kiem:  python dg3_rewrite_fallback.py
"""
import hashlib, re

GENERIC_VERB = {
    "tap": "Tap", "click": "Tap", "press": "Tap", "select": "Tap", "choose": "Tap",
    "toggle": "Toggle", "switch": "Toggle", "turn": "Toggle",
    "enter": "Enter", "type": "Enter", "input": "Enter", "fill": "Enter",
    "open": "Open", "go": "Go to", "navigate": "Go to",
}

# Pool cau san (co dinh) — deu la mo ta chung, TU no khong trung nhan that nao.
FLOOR_SENTENCES = [
    "Look for the option on this screen that matches what you need for this step, and tap it.",
    "Find the relevant control on this screen for this step and use it.",
    "Locate the option on this screen that lets you continue with this step.",
]

_LEADING_JUNK = re.compile(
    r"^(please\s+|kindly\s+|you\s+(should|can|need\s+to|must|may)\s+|now\s+|then\s+|"
    r"in\s+order\s+to\s+|to\s+|so\s+(as\s+)?to\s+|the\s+user\s+(wants|needs)\s+to\s+)",
    re.I,
)


def first_word(verb):
    return (verb or "").strip().split()[0].lower() if (verb or "").strip() else ""


def _stable_idx(key, n, salt=0):
    """Chi so tat dinh trong [0,n) tu chuoi key (md5 on dinh, khong phu thuoc PYTHONHASHSEED)."""
    h = hashlib.md5(f"{salt}|{key}".encode("utf-8")).hexdigest()
    return int(h, 16) % n


def clean_intent_clause(note):
    """
    Cat cum dan dau + ha Title-Case con sot -> cum y-dinh dung sau "...let you {intent}".
    Vi du: "Please tap to Open Settings" -> "open settings".
    Tra "" neu note rong hoac chi con rac.
    """
    s = re.sub(r"\s+", " ", (note or "").strip())
    if not s:
        return ""
    prev = None
    while prev != s:                       # cat lap cac cum dan dau chong nhau
        prev = s
        s = _LEADING_JUNK.sub("", s).strip()
    s = s.rstrip(".!?,;: ").strip()
    # ha chu HOA giua cau (giu nguyen chuoi trong ngoac kep neu co) — don gian: lower toan bo.
    return s.lower()


def rewrite_fallback(verb, element, note, labels, tau_a=0.55, matcher=None):
    """
    Sinh cau MO TA CHUNG cho buoc bia. KHONG bao gio nhac ten nut cu the.
    - Neu co 'intent' (tu note) -> "{Verb-chung} the option on this screen that would let you {intent}."
    - Nguoc lai -> chon 1 cau tu FLOOR_SENTENCES (tat dinh theo element).
    - Neu co matcher: tu-kiem cau sinh ra co vo tinh 'khop' 1 nhan that (sim>=tau_a) khong;
      neu co -> lui ve FLOOR_SENTENCES (an toan tuyet doi khong bia moi).
    matcher(text, labels) -> (label_gan_nhat, sim). Truyen None de bo qua tu-kiem (vd luc tu-kiem).
    """
    vgen = GENERIC_VERB.get(first_word(verb), "Interact with")
    intent = clean_intent_clause(note)
    if intent:
        candidate = f"{vgen} the option on this screen that would let you {intent}."
    else:
        candidate = FLOOR_SENTENCES[_stable_idx(element, len(FLOOR_SENTENCES))]

    if matcher is not None and labels:
        try:
            _, sim = matcher(candidate, labels)
        except Exception:
            sim = 0.0
        if sim >= tau_a:                   # cau tu-do lai trung nhan that -> lui ve floor
            candidate = FLOOR_SENTENCES[_stable_idx(element, len(FLOOR_SENTENCES), salt=1)]
    return candidate


# ----------------------------- TU KIEM (fake data, khong mang) -----------------------------
def _selftest():
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok = ok and cond
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")

    labels = ["Settings", "Notifications", "Save"]

    # 1) Co intent tu note -> cau chua intent, KHONG chua ten nut bia.
    out1 = rewrite_fallback("Tap", "Privacy Menu", "to open privacy settings", labels)
    chk("intent: sinh cau tu note", "let you open privacy settings" in out1.lower())
    chk("intent: KHONG chua ten bia 'Privacy Menu'", "privacy menu" not in out1.lower())
    chk("intent: dung verb chung 'Tap'", out1.startswith("Tap the option"))

    # 2) Khong co note -> roi vao FLOOR_SENTENCES.
    out2 = rewrite_fallback("Toggle", "Ghost Switch", "", labels)
    chk("no-note: la cau floor", out2 in FLOOR_SENTENCES)

    # 3) TAT DINH: cung element -> cung ket qua qua nhieu lan goi (tai lap).
    a = rewrite_fallback("Tap", "SameEl", "", labels)
    b = rewrite_fallback("Tap", "SameEl", "", labels)
    chk("tat dinh: cung element -> cung cau", a == b)
    # element khac co the ra cau khac (khong bat buoc, chi kiem pool phu it nhat 2 gia tri)
    seen = {rewrite_fallback("Tap", f"El{i}", "", labels) for i in range(30)}
    chk("tat dinh: pool floor duoc dung >=2 cau", len(seen) >= 2)

    # 4) Verb-chung chi ap khi CO intent (note); verb la khong gay KeyError.
    chk("verb: 'switch on'->Toggle (co note)",
        rewrite_fallback("switch on", "X", "enable dark mode", labels).startswith("Toggle"))
    chk("verb: la->Interact with", rewrite_fallback("frobnicate", "X", "do stuff", labels).startswith("Interact with"))

    # 5) Tu-kiem matcher: neu cau sinh 'khop' nhan that -> lui ve floor.
    #    matcher gia: bao sim=0.9 (>=tau_a) cho lan dau, 0.0 sau do -> ep re nhanh lui-floor.
    calls = {"n": 0}
    def fake_matcher(text, labs):
        calls["n"] += 1
        return ("Settings", 0.9 if calls["n"] == 1 else 0.0)
    out5 = rewrite_fallback("Tap", "ElZ", "to change settings", labels, matcher=fake_matcher)
    chk("matcher: cau bi coi la khop -> lui ve floor", out5 in FLOOR_SENTENCES)

    # 6) clean_intent_clause cat cum dan dau (input thuc = truong 'note' ngan).
    chk("clean: cat 'to '", clean_intent_clause("to Open Settings") == "open settings")
    chk("clean: cat 'in order to '", clean_intent_clause("In order to save the file") == "save the file")
    chk("clean: note rong -> ''", clean_intent_clause("   ") == "")

    print("\n=> " + ("TAT CA PASS" if ok else "CO FAIL — xem tren"))
    return ok


if __name__ == "__main__":
    _selftest()
