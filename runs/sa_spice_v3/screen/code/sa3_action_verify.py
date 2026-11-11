# -*- coding: utf-8 -*-
"""SA-SPICE-v3: action verifier (memo §5) + audit mù.

Verifier v3 (khoá version bằng VERSION + sha256 tệp này):
  trusted(gold) ⇔ action log hợp lệ ∧ canon(log) ∈ ACTIVE ∧ classify(câu chuẩn) == canon(log)
                  (wait/home không ACTIVE ⇒ untrusted; chưa chấm hướng scroll)
  A(y) = 0,5 nếu untrusted hoặc classify(y) là None
       = 0   nếu classify(y) ≠ canon, hoặc toggle ngược chiều câu chuẩn
       = 1   còn lại

  python3 sa3_action_verify.py selftest
  python3 sa3_action_verify.py build --src raft_mau_0.jsonl [raft_mau_1.jsonl …] --per-cell 30 --out DIR
        → DIR/audit_blind.jsonl (không có nhãn verifier) + DIR/audit_key.jsonl (nhãn verifier, KHÔNG mở khi chấm)
  python3 sa3_action_verify.py score --dir DIR --labels labels.jsonl [--human human.jsonl]
"""
import os, re, sys, json, random, hashlib, argparse, collections

VERSION = "sa3-verify-3"  # v3 11/11: khác loại ⇒ 0,5 (đường khác có thể hợp lý, user + 2 pilot); chỉ toggle ngược ⇒ 0.
# v2  # v2 11/11: động từ chạm đầu câu ⇒ tap; back-arrow ↔ go back ⇒ 0,5 (sau pilot 1)
ACTIVE = ("tap", "scroll", "back", "type", "open_app")
CANON = {"click": "tap", "long_press": "tap", "scroll": "scroll", "navigate_back": "back",
         "input_text": "type", "open_app": "open_app", "wait": "wait", "navigate_home": "home"}
ON = re.compile(r"\b(enable|turn on|switch on|activate)\b")
OFF = re.compile(r"\b(disable|turn off|switch off|deactivate)\b")


def toks(s):
    return " ".join(re.findall(r"[a-z0-9']+", (s or "").lower()))


LEAD_TAP = re.compile(r"^(click|tap|press|select|choose|long press|double tap|hit)\b")
BACK_TGT = re.compile(r"\b(back (arrow|button|icon|key)|arrow (icon )?(at|on) the (top )?left|left arrow)\b")


def classify(sentence):
    """v1 = reward_cpu_8_11.classify (pilot C1). v2: động từ chạm đứng đầu câu thắng từ khoá phía sau
    ("Click on the pause button" là tap, không phải wait)."""
    s = toks(sentence)
    if not s:
        return None
    if re.search(r"\b(go back|navigate back|return to (the )?(previous|last) screen|press (the )?back (button|key))\b", s):
        return "back"
    if LEAD_TAP.match(s):
        return "tap"
    if re.search(r"\b(scroll|swipe)\b", s):
        return "scroll"
    if re.search(r"\b(wait|pause|let (it|the page) load)\b", s):
        return "wait"
    if re.search(r"\b(type|enter|input|fill in|write)\b", s):
        return "type"
    if re.search(r"\b(open|launch|start)\b.*\bapp\b", s):
        return "open_app"
    if re.search(r"\b(tap|click|press|select|choose|check|enable|disable|turn on|turn off|open)\b", s):
        return "tap"
    return None


def toggle(s):
    s = toks(s)
    on, off = bool(ON.search(s)), bool(OFF.search(s))
    return "on" if on and not off else ("off" if off and not on else None)


def trusted(gold, action_type):
    c = CANON.get(action_type)
    return c in ACTIVE and classify(gold) == c


def score_action(cand, gold, action_type):
    """Trả (A, lý do)."""
    if not trusted(gold, action_type):
        return 0.5, "untrusted"
    c = classify(cand)
    if c is None:
        return 0.5, "unknown"
    canon = CANON[action_type]
    if canon == "tap" and c == "back" and BACK_TGT.search(toks(gold)):
        return 0.5, "back_equiv"
    if c != canon:
        # v3: khác loại thao tác KHÔNG phải "sai chắc chắn" — pilot người chấm 7/20 dòng v2 chấm 0 là đường đi khác hợp lý
        return 0.5, "mismatch_uncertain"
    tg, ty = toggle(gold), toggle(cand)
    if tg and ty and tg != ty:
        return 0.0, "toggle"
    return 1.0, "correct"


def selftest():
    assert score_action("Scroll down", "Swipe up to see more", "scroll") == (1.0, "correct")
    assert score_action("Click the down arrow", "Swipe up", "scroll") == (0.5, "mismatch_uncertain")
    assert score_action("Disable notifications", "Turn on notifications", "click") == (0.0, "toggle")
    assert score_action("Hmm", "Click Next", "click") == (0.5, "unknown")
    assert score_action("Click Next", "Click Next", "wait") == (0.5, "untrusted")
    assert score_action("Click Next", "Click Next", "scroll") == (0.5, "untrusted")   # gold lệch log
    assert score_action("", "Click Next", "click") == (0.5, "unknown")
    assert score_action("Click on the pause button", "Click on the stop button", "click") == (1.0, "correct")
    assert score_action("click on the type filter", "Click on the best match tab", "click") == (1.0, "correct")
    assert score_action("Go back to the previous page", "Click on the back arrow at the top left", "click") == (0.5, "back_equiv")
    assert score_action("Go back to the previous page", "Click on the menu icon", "click") == (0.5, "mismatch_uncertain")
    assert score_action("Type hello", "Enter hello in the box", "input_text") == (1.0, "correct")
    print("selftest ĐẠT", flush=True)


def build(a):
    rows = {}
    for f in a.src:
        for l in open(f, encoding="utf-8"):
            r = json.loads(l)
            for y in [r.get("greedy")] + list(r.get("samples") or []):
                y = (y or "").strip()
                if not y:
                    continue
                k = (r["key"], y)
                if k not in rows:
                    rows[k] = {"key": r["key"], "gold": r["gold"], "action_type": r["action_type"], "cand": y}
    if a.skip:
        bl = {r["id"]: r for r in map(json.loads, open(os.path.join(a.skip, "audit_blind.jsonl"), encoding="utf-8"))}
        for r in map(json.loads, open(os.path.join(a.skip, "audit_key.jsonl"), encoding="utf-8")):
            rows.pop((r["key"], bl[r["id"]]["cand"]), None)
    cells = collections.defaultdict(list)
    for r in rows.values():
        A, why = score_action(r["cand"], r["gold"], r["action_type"])
        if why in ("correct", "toggle"):
            cells[(CANON[r["action_type"]], "correct" if A == 1 else "known_wrong")].append({**r, "A": A, "why": why})
    rng = random.Random(a.seed)
    pick = []
    for k in sorted(cells):
        lst = sorted(cells[k], key=lambda r: (r["key"], r["cand"]))
        rng.shuffle(lst)
        pick += lst[:a.per_cell]
    rng.shuffle(pick)
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "audit_blind.jsonl"), "w", encoding="utf-8") as fb, \
         open(os.path.join(a.out, "audit_key.jsonl"), "w", encoding="utf-8") as fk:
        for i, r in enumerate(pick):
            fb.write(json.dumps({"id": i, "gold_action": CANON[r["action_type"]], "gold": r["gold"], "cand": r["cand"]}, ensure_ascii=False) + "\n")
            fk.write(json.dumps({"id": i, "key": r["key"], "A": r["A"], "why": r["why"]}, ensure_ascii=False) + "\n")
    info = {"version": VERSION, "verifier_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
            "src": a.src, "unique_pairs": len(rows),
            "cells_available": {f"{k[0]}|{k[1]}": len(v) for k, v in sorted(cells.items())},
            "picked": len(pick), "per_cell": a.per_cell}
    json.dump(info, open(os.path.join(a.out, "audit_info.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(info, ensure_ascii=False, indent=1), flush=True)


def cp(k, n, side):
    from scipy.stats import beta
    if side == "lo":
        return 0.0 if k == 0 else float(beta.ppf(0.05, k, n - k + 1))
    return 1.0 if k == n else float(beta.ppf(0.95, k + 1, n - k))


def score(a):
    key = {r["id"]: r for r in map(json.loads, open(os.path.join(a.dir, "audit_key.jsonl"), encoding="utf-8"))}
    blind = {r["id"]: r for r in map(json.loads, open(os.path.join(a.dir, "audit_blind.jsonl"), encoding="utf-8"))}
    lab = {r["id"]: r["label"] for r in map(json.loads, open(a.labels, encoding="utf-8"))}
    assert set(lab) == set(key), f"⛔ thiếu nhãn: {len(set(key) - set(lab))}"
    assert all(v in ("correct", "wrong", "unclear") for v in lab.values())
    out = {"by_cell": {}, "by_action": {}}
    for act in ACTIVE:
        for v in ("correct", "known_wrong"):
            ids = [i for i in key if blind[i]["gold_action"] == act and (key[i]["A"] == 1) == (v == "correct")]
            n = len(ids)
            if not n:
                continue
            agree = sum(1 for i in ids if lab[i] == ("correct" if v == "correct" else "wrong"))
            unc = sum(1 for i in ids if lab[i] == "unclear")
            out["by_cell"][f"{act}|{v}"] = {"n": n, "agree": agree, "unclear": unc, "ppv": round(agree / n, 4),
                                            "ppv_lo95": round(cp(agree, n, "lo"), 4), "pass_98": cp(agree, n, "lo") > 0.98}
        # false reject: người nói correct mà verifier 0; false accept: người nói wrong mà verifier 1
        tc = [i for i in key if blind[i]["gold_action"] == act and lab[i] == "correct"]
        tw = [i for i in key if blind[i]["gold_action"] == act and lab[i] == "wrong"]
        fr = sum(1 for i in tc if key[i]["A"] == 0); fa = sum(1 for i in tw if key[i]["A"] == 1)
        out["by_action"][act] = {"true_correct": len(tc), "false_reject": fr, "fr_hi95": round(cp(fr, len(tc), "hi"), 4) if tc else None,
                                 "true_wrong": len(tw), "false_accept": fa, "fa_hi95": round(cp(fa, len(tw), "hi"), 4) if tw else None}
    out["disagree_ids"] = sorted(i for i in key if lab[i] != ("correct" if key[i]["A"] == 1 else "wrong"))
    if a.human:
        hu = {r["id"]: r["label"] for r in map(json.loads, open(a.human, encoding="utf-8"))}
        both = [i for i in hu if i in lab]
        out["human_vs_claude"] = {"n": len(both), "agree": sum(hu[i] == lab[i] for i in both),
                                  "disagree_ids": [i for i in both if hu[i] != lab[i]]}
    json.dump(out, open(os.path.join(a.dir, "audit_result.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["selftest", "build", "score"])
    ap.add_argument("--src", nargs="*"); ap.add_argument("--skip"); ap.add_argument("--seed", type=int, default=20261111); ap.add_argument("--per-cell", type=int, default=30)
    ap.add_argument("--out"); ap.add_argument("--dir"); ap.add_argument("--labels"); ap.add_argument("--human")
    a = ap.parse_args()
    {"selftest": lambda a: selftest(), "build": build, "score": score}[a.cmd](a)
