# -*- coding: utf-8 -*-
"""
dg3_eval_no_vh.py — CHAM faithfulness khong-gold cho Tier 1 / Tier 2 (pre-reg report/56 §2-§5).
"Bia" = DA SO 3 co che KHAC HO dong thuan KHONG-khop nhan VH dung man:
    (1) bge-m3 cosine (tauB rieng)   (2) LLM-judge llama3.2 nhi phan   (3) token-overlap (thuan chuoi)
VH CHI vao luc CHAM. f do tren OUTPUT THO (vá A1-1). Gop macro-per-app -> exact sign-flip G=12.

matcher bge-m3 + judge llama3.2 la THAM SO TIEM (injectable) -> tu-kiem chay bang matcher gia,
KHONG can Ollama/API. token-overlap thuan toan. Thong ke goi dg3_stats (exact sign-flip + CI).

Chay tu-kiem:  python dg3_eval_no_vh.py --selftest
"""
import os, sys, re, json, argparse
from collections import defaultdict
sys.path.insert(0, os.path.dirname(__file__))
import dg3_stats

TAU_B = float(os.environ.get("TAU_B", "0.65"))       # bge-m3 (hieu chuan RIENG, KHONG lay tauA=0.55)
TOK_THRESH = 0.5                                      # nguong Jaccard token-overlap

# --- trich ten nut duoc nhac (report/56 §2 "trich ten nut trong cau tra loi") ---
_QUOTED = re.compile(r'"([^"]{1,60})"')              # ten nut render dang Tap "Settings"


def extract_mentions(text):
    """Tra list ten nut duoc nhac (chuoi trong ngoac kep). Cau mo-ta-chung khong co -> khong tinh."""
    return [m.strip() for m in _QUOTED.findall(text or "") if m.strip()]


def norm(s):
    return re.sub(r"\s+", " ", (s or "").lower().strip())


def _toks(s):
    return set(re.findall(r"[a-z0-9]+", norm(s)))


def token_overlap_present(name, labels):
    """CO CHE 3 (thuan chuoi): True neu ten 'co mat' o >=1 nhan (bang/chua-nhau/Jaccard>=nguong)."""
    nn = norm(name)
    tn = _toks(name)
    if not nn:
        return False
    for l in labels:
        nl = norm(l)
        if nn == nl or (len(nn) >= 3 and (nn in nl or nl in nn)):
            return True
        tl = _toks(l)
        if tn and tl and len(tn & tl) / len(tn | tl) >= TOK_THRESH:
            return True
    return False


def is_hallucinated(name, labels, mechs):
    """
    DA SO 3 co che dong thuan KHONG-khop -> bia. mechs = {'bge':fn, 'judge':fn} moi fn(name,labels)->present(bool).
    token-overlap tinh noi bo. Tra True neu >=2/3 co che noi 'khong co mat'.
    """
    present_votes = [
        bool(mechs["bge"](name, labels)),
        bool(mechs["judge"](name, labels)),
        token_overlap_present(name, labels),
    ]
    n_absent = sum(1 for p in present_votes if not p)
    return n_absent >= 2


def score_screen(text, labels, mechs):
    """
    Cham 1 man cho 1 arm. Tra dict: n_mention, n_bia, f (None neu 0-nhac-nut), zero_mention(bool).
    f = 1 - n_bia/n_mention (vá A1-2: 0-nhac-nut -> f=None, bao rieng).
    """
    mentions = extract_mentions(text)
    n = len(mentions)
    if n == 0:
        return {"n_mention": 0, "n_bia": 0, "f": None, "zero_mention": True}
    n_bia = sum(1 for m in mentions if is_hallucinated(m, labels, mechs))
    return {"n_mention": n, "n_bia": n_bia, "f": 1 - n_bia / n, "zero_mention": False}


def f_by_app(arm_outputs, screens, mechs):
    """
    arm_outputs: {screen: text}. screens: {screen: {app, labels}}.
    Tra: {app: f_app}, + thong ke phu {app: {n_screens_used, n_zero, ...}}.
    f_app = trung binh f cua cac man co n_mention>0 trong app. Man 0-nhac-nut bi LOAI khoi trung binh.
    """
    per_app = defaultdict(list)
    zero_app = defaultdict(int)
    tot_app = defaultdict(int)
    for scr, meta in screens.items():
        if scr not in arm_outputs:
            continue
        app = meta["app"]
        tot_app[app] += 1
        r = score_screen(arm_outputs[scr], meta["labels"], mechs)
        if r["zero_mention"]:
            zero_app[app] += 1
        else:
            per_app[app].append(r["f"])
    f_app = {a: sum(v) / len(v) for a, v in per_app.items() if v}
    stat = {a: {"n_used": len(per_app.get(a, [])), "n_zero": zero_app.get(a, 0),
                "n_total": tot_app.get(a, 0),
                "zero_rate": zero_app.get(a, 0) / (tot_app.get(a, 1))} for a in tot_app}
    return f_app, stat


def run_tier(arm1_out, arm2_out, screens, mechs, test_apps):
    """
    So arm1 vs arm2 tren DUNG test_apps (thu tu co dinh). d_j = f_app1 - f_app2.
    Tra dict: d (list theo test_apps co du 2 arm), t_obs, p, ci, n_apps, f1, f2.
    """
    f1, s1 = f_by_app(arm1_out, screens, mechs)
    f2, s2 = f_by_app(arm2_out, screens, mechs)
    d, used_apps = [], []
    for a in test_apps:                              # thu tu co dinh -> tai lap
        if a in f1 and a in f2:
            d.append(f1[a] - f2[a])
            used_apps.append(a)
    if len(d) < 2:
        return {"d": d, "used_apps": used_apps, "t_obs": 0.0, "p": 1.0,
                "ci": (0.0, 0.0), "n_apps": len(d), "f1": f1, "f2": f2, "stat1": s1, "stat2": s2}
    t_obs, p, _ = dg3_stats.exact_sign_flip(d)
    ci = dg3_stats.ci_sign_flip(d)
    return {"d": d, "used_apps": used_apps, "t_obs": t_obs, "p": p, "ci": ci,
            "n_apps": len(d), "f1": f1, "f2": f2, "stat1": s1, "stat2": s2}


def _test_apps():
    d = json.load(open(os.path.join(os.path.dirname(__file__), "train_eval_app_split.json"),
                      encoding="utf-8"))["mobileviews"]
    return d.get("test_apps_30", [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return 0 if _selftest() else 1
    print("Chay that can output cua 3 arm (student/student-RAW/teacher-BASE) + matcher bge-m3/llama3.2.")
    print("Chua co output model (chua train/gen) -> hay chay --selftest de kiem logic trong.")
    return 0


# ----------------------------- TU KIEM (fake data, khong mang) -----------------------------
def _fake_mechs(present_set):
    """bge + judge deu 'present' neu norm(name) nam trong present_set. present_set = set nhan chuan hoa."""
    def present(name, labels):
        return norm(name) in present_set
    return {"bge": present, "judge": present}


def _selftest():
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok = ok and cond
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")

    labels = ["Settings", "Notifications", "Save"]
    mechs = _fake_mechs({"settings", "notifications", "save"})

    # 1) extract_mentions chi lay ten trong ngoac kep.
    txt = '1. Tap "Settings"\n2. Look for the option on this screen and tap it.\n3. Toggle "Notifications"'
    chk("extract: 2 ten nut (bo cau chung)", extract_mentions(txt) == ["Settings", "Notifications"])

    # 2) token_overlap: 'Settings' co mat; 'Ghost Menu' khong.
    chk("tok: 'Settings' present", token_overlap_present("Settings", labels) is True)
    chk("tok: 'Ghost Menu' absent", token_overlap_present("Ghost Menu", labels) is False)
    chk("tok: 'Notification settings' overlap>=0.5", token_overlap_present("Notification Settings", labels) is True)

    # 3) is_hallucinated: 2/3 dong thuan.
    chk("bia: 'Ghost Menu' -> bia (3/3 absent)", is_hallucinated("Ghost Menu", labels, mechs) is True)
    chk("bia: 'Settings' -> khong bia", is_hallucinated("Settings", labels, mechs) is False)

    # 4) score_screen: 3 nhac, 1 bia -> f=2/3; man 0-nhac -> f=None.
    r = score_screen('1. Tap "Settings"\n2. Tap "Ghost Menu"\n3. Toggle "Notifications"', labels, mechs)
    chk("score: n_mention=3", r["n_mention"] == 3)
    chk("score: n_bia=1", r["n_bia"] == 1)
    chk("score: f=2/3", abs(r["f"] - 2 / 3) < 1e-9)
    r0 = score_screen("Look for the option on this screen and tap it.", labels, mechs)
    chk("score: 0-nhac-nut -> f=None, zero_mention", r0["f"] is None and r0["zero_mention"])

    # 5) f_by_app: loai man 0-nhac khoi trung binh.
    screens = {
        "appA_s1": {"app": "appA", "labels": labels},
        "appA_s2": {"app": "appA", "labels": labels},
        "appA_s3": {"app": "appA", "labels": labels},   # se la 0-nhac
    }
    arm = {
        "appA_s1": '1. Tap "Settings"',                        # f=1
        "appA_s2": '1. Tap "Ghost Menu"',                      # f=0
        "appA_s3": 'Find the relevant control and use it.',    # 0-nhac -> loai
    }
    fapp, stat = f_by_app(arm, screens, mechs)
    chk("f_by_app: appA = mean(1,0)=0.5", abs(fapp["appA"] - 0.5) < 1e-9)
    chk("f_by_app: dem 1 man 0-nhac", stat["appA"]["n_zero"] == 1 and stat["appA"]["n_used"] == 2)

    # 6) run_tier full: dung 12 test-app that, arm1 luon sach hon arm2 -> d duong dong deu -> p nho.
    test_apps = _test_apps()
    chk("split: du 12 test-app", len(test_apps) == 12)
    # d_j BIEN THIEN (khong dong nhat -> tranh suy bien var=0) nhung deu DUONG.
    sc, a1, a2 = {}, {}, {}
    for i, app in enumerate(test_apps):
        s = f"{app}_s1"
        sc[s] = {"app": app, "labels": labels}
        a1[s] = '1. Tap "Settings"\n2. Toggle "Notifications"'      # f1=1.0 (0 bia)
        if i % 2 == 0:
            a2[s] = '1. Tap "Ghost Menu"\n2. Toggle "Notifications"'                     # f2=0.5 -> d=0.5
        else:
            a2[s] = '1. Tap "Settings"\n2. Tap "Ghost Menu"\n3. Toggle "Notifications"\n4. Tap "Save"'  # f2=0.75 -> d=0.25
    res = run_tier(a1, a2, sc, mechs, test_apps)
    chk("tier: dung du 12 app", res["n_apps"] == 12)
    chk("tier: moi d_j DUONG", all(x > 0 for x in res["d"]))
    chk("tier: tach bach -> p<0.01", res["p"] < 0.01)
    chk("tier: CI nam tren 0", res["ci"][0] > 0)

    # 7) Truong hop NULL: 2 arm bang nhau -> d toan 0 -> p=1, CI chua 0.
    res0 = run_tier(a1, dict(a1), sc, mechs, test_apps)
    chk("tier-null: d toan 0 -> p=1.0", abs(res0["p"] - 1.0) < 1e-9)
    chk("tier-null: CI chua 0", res0["ci"][0] <= 0 <= res0["ci"][1])

    print("\n=> " + ("TAT CA PASS" if ok else "CO FAIL — xem tren"))
    return ok


if __name__ == "__main__":
    sys.exit(main() or 0)
