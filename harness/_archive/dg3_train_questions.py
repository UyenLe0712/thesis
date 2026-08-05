# -*- coding: utf-8 -*-
"""
dg3_train_questions.py — SINH CAU HOI use-case cho pool train (report/53 §2.3).
Mo rong dg1_questions.py: 3 cau/man, temperature=0.6, DEDUPE bang Jaccard token tren cau chuan hoa.
Vision = Ollama qwen2.5vl:3b (LOCAL, free) — KHONG ton API cloud. Nguoi duyet luot truoc buoc teacher.

Phan SINH can Ollama; phan DEDUP thuan toan -> tu-kiem chay khong can mang.
Chay tu-kiem:  python dg3_train_questions.py --selftest
Chay that   :  VLM_MODEL=qwen2.5vl:3b python dg3_train_questions.py
"""
import os, sys, re, json, glob, argparse

HERE = os.path.dirname(__file__)
POOL_DIR = os.path.join(HERE, "..", "dataset_samples", "mv_train_pool")
SPLIT_FP = os.path.join(HERE, "train_eval_app_split.json")
OUT = os.path.join(HERE, "dg3_cache")
QFILE = os.path.join(OUT, "train_questions.json")
N_PER_SCREEN = 3
JACCARD_THRESH = 0.6                                  # >= nguong -> coi la trung, loai

QPROMPT = """Look at this app screenshot. Write ONE short, realistic use-case question a real user might ask about THIS screen — like "How do I ...?" or "Where do I tap to ...?".
It must be about something DOABLE right now on this screen (based on the visible buttons/fields), not something absent.
Return ONLY one question in English, no explanation, nothing else."""


def norm_q(s):
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", (s or "").lower().strip()))


def _toks(s):
    return set(norm_q(s).split())


def jaccard(a, b):
    ta, tb = _toks(a), _toks(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def dedupe(questions, thresh=JACCARD_THRESH):
    """Giu thu tu; loai cau co Jaccard >= thresh voi mot cau DA GIU. Tra list da loc."""
    kept = []
    for q in questions:
        if not (q or "").strip():
            continue
        if any(jaccard(q, k) >= thresh for k in kept):
            continue
        kept.append(q.strip())
    return kept


def _train_apps():
    d = json.load(open(SPLIT_FP, encoding="utf-8"))["mobileviews"]
    return set(d.get("train_apps_30", [])) | set(d.get("train_pool_expanded", []))


def app_of(screen):
    return screen.split("_")[0]


def gen_for_screen(img_path, vision_call):
    """Sinh N_PER_SCREEN cau roi dedupe. vision_call(img_path, prompt)->str (tiem de test)."""
    raw = []
    for _ in range(N_PER_SCREEN):
        try:
            q = vision_call(img_path, QPROMPT).splitlines()[0].strip().strip('"')
        except Exception as ex:
            q = f"[LOI {repr(ex)[:40]}]"
        raw.append(q)
    return dedupe([q for q in raw if not q.startswith("[LOI")])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return 0 if _selftest() else 1

    # Chay that: vision qua Ollama local.
    sys.path.insert(0, HERE)
    import base64
    from _apikey import get_key
    from _http import chat
    BASE = os.environ.get("VLM_BASE_URL", "http://localhost:11434/v1")
    MODEL = os.environ.get("VLM_MODEL", "qwen2.5vl:3b")

    def vision_call(img_path, prompt):
        with open(img_path, "rb") as f:
            uri = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
        msgs = [{"role": "user", "content": [
            {"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": uri}}]}]
        return chat(BASE, MODEL, msgs, get_key(), temperature=0.6).strip()

    os.makedirs(OUT, exist_ok=True)
    qs = json.load(open(QFILE, encoding="utf-8")) if os.path.exists(QFILE) else {}
    train = _train_apps()
    imgs = sorted(glob.glob(os.path.join(POOL_DIR, "*.jpg")))
    imgs = [p for p in imgs if app_of(os.path.basename(p).split(".")[0]) in train] if train else imgs
    for i, img in enumerate(imgs):
        name = os.path.basename(img).split(".")[0]
        if name in qs:                                # resume
            continue
        qs[name] = gen_for_screen(img, vision_call)
        json.dump(qs, open(QFILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"  [{i+1}/{len(imgs)}] {name}: {len(qs[name])} cau")
    print(f"xong {sum(len(v) for v in qs.values())} cau / {len(qs)} man -> {QFILE}")
    return 0


# ----------------------------- TU KIEM (fake data, khong mang) -----------------------------
def _selftest():
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok = ok and cond
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")

    # 1) jaccard / norm.
    chk("jaccard: giong het -> 1.0", abs(jaccard("How do I save?", "how do i save") - 1.0) < 1e-9)
    chk("jaccard: khac hoan toan -> 0", jaccard("save the file", "delete account now") == 0.0)

    # 2) dedupe loai cau gan trung, giu cau khac.
    qs = [
        "How do I turn on notifications?",
        "How do I turn on notifications",          # gan trung cau 1 -> loai
        "Where do I tap to save the file?",         # khac -> giu
        "",                                          # rong -> bo
    ]
    out = dedupe(qs)
    chk("dedupe: giu 2 cau khac nhau", len(out) == 2)
    chk("dedupe: giu cau dau", out[0] == "How do I turn on notifications?")
    chk("dedupe: giu cau save", "save" in out[1].lower())

    # 3) gen_for_screen voi vision_call gia (khong mang): tra <=3 cau, da dedupe.
    seq = iter(["How do I save?", "how do i save", "Where is settings?"])
    def fake_vision(img, prompt):
        return next(seq)
    got = gen_for_screen("x.jpg", fake_vision)
    chk("gen: dedupe con 2 cau", len(got) == 2)

    # 4) gen_for_screen bo cau loi.
    def fake_err(img, prompt):
        raise RuntimeError("no ollama")
    chk("gen: loi -> rong (khong crash)", gen_for_screen("x.jpg", fake_err) == [])

    print("\n=> " + ("TAT CA PASS" if ok else "CO FAIL — xem tren"))
    return ok


if __name__ == "__main__":
    sys.exit(main() or 0)
