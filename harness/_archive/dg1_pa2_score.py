# -*- coding: utf-8 -*-
"""
PA2 (review 2026-06-30): design-E = CHI matched/fallback (BO h?n correction llama).
  - He quyet matched/fallback bang matcher A = nomic (best_match), nguong tauA.
  - CHAM faithfulness/grounded bang matcher B = bge-m3 DOC LAP (pha tautology: A != B).
  - PA2 GIU NGUYEN chu o buoc matched -> dung-nhan KHONG tang (chi bao no-harm).
  - silent-error = 0 theo cau truc (khong con correction).
  - Suy PA2-sysE TU base da cache -> KHONG goi API sinh moi (free).
  - Fix bug: seed bootstrap (T2), exact_label guard rong + siet substring>=3 (T4),
            cache embedding key theo model (S1 -> dung module dg1_independent_score).

Chay:  PYTHONIOENCODING=utf-8 DG1_LIMIT=10 python dg1_pa2_score.py
"""
import os, sys, json, glob, re, random
sys.path.insert(0, os.path.dirname(__file__))
from aloha_match import best_match                 # matcher A = nomic (quyet matched/fallback)
from dg1_independent_score import max_sim as simB   # matcher B = bge-m3 (cham, DOC LAP)

RUNS = os.path.join(os.path.dirname(__file__), "dg1_cache", "runs")
SEED = 20260630
TAU_A = float(os.environ.get("TAU_A", "0.55"))      # nomic, quyet matched/fallback
TAUS_B = [0.60, 0.70, 0.80]                          # bge-m3 chay cao -> nguong cham cao hon
VERBS = ("bấm","chọn","nhập","mở","vào","gõ","kéo","cuộn","nhấn","tìm","tích","bật","tắt","xem",
         "tap","click","select","enter","type","open","choose","press","find","scroll","toggle",
         "set","view","add","create","delete","edit","update","change","go","navigate","check",
         "switch","swipe","drag","fill","input","pick","turn")

def norm(s): return re.sub(r"\s+", " ", (s or "").lower().strip())
def exact_label_safe(name, labels):                 # T4: guard rong + substring chi khi >=3 ky tu
    nn = norm(name)
    if not nn: return False
    return any(nn == norm(l) or (len(nn) >= 3 and (nn in norm(l) or norm(l) in nn)) for l in labels)
def starts_verb(v): return any((v or "").strip().lower().startswith(x) for x in VERBS)

def derive_pa2(base, labels, tauA):
    """Suy design-E PA2 tu base: khop (nomic>=tauA) -> matched; khong -> fallback."""
    out = []
    for s in base:
        el = s.get("element", "")
        _, sim = best_match(el, labels) if (el or "").strip() else (None, 0.0)
        if (el or "").strip() and sim >= tauA:
            out.append({**s, "status": "matched"})
        else:
            out.append({"verb": s.get("verb",""), "element": f"(describe) {el}",
                        "note": s.get("note",""), "status": "fallback"})
    return out

def score(steps, labels, tauB):
    """Cham bang matcher B (bge-m3). button_steps loai fallback; mau so n GOM fallback (bao thu)."""
    n = len(steps) or 1
    button = [s for s in steps if s.get("status") != "fallback"]
    wrong = sum(1 for s in button if simB(s["element"], labels) < tauB)
    faith = 1 - wrong / n
    grounded = sum(1 for s in button if simB(s["element"], labels) >= tauB) / n
    nb = len(button) or 1
    label_fid = sum(1 for s in button if exact_label_safe(s["element"], labels)) / nb
    fmt = sum(1 for s in steps if starts_verb(s.get("verb",""))) / n
    return {"faith": faith, "grounded": grounded, "label_fid": label_fid, "format": fmt,
            "n_fallback": sum(1 for s in steps if s.get("status") == "fallback"), "n": len(steps)}

def boot_ci_cluster(pairs, it=10000):
    """CLUSTER bootstrap theo APP (review ⑤): resample APP (co hoan lai) roi gom delta cua app do.
    Tranh CI gia-chat khi cac man cung app KHONG doc lap. pairs = [(app, delta), ...].
    Tra (lo, hi, p) — p = 1-sided bootstrap p-value cho H0: delta_trung_binh <= 0."""
    from collections import defaultdict
    by_app = defaultdict(list)
    for a, d in pairs:
        by_app[a].append(d)
    apps = list(by_app.keys()); A = len(apps)
    if A == 0: return (0.0, 0.0, 1.0)
    means = []
    for _ in range(it):
        pool = []
        for _ in range(A):                              # resample A app, gom delta moi app
            pool.extend(by_app[apps[random.randrange(A)]])
        if pool:
            means.append(sum(pool) / len(pool))
    means.sort(); n = len(means) or 1
    lo, hi = means[int(0.025 * n)], means[int(0.975 * n)]
    p = sum(1 for x in means if x <= 0) / n
    return (lo, hi, p)

def holm(pvals):
    """Holm-Bonferroni cho da-metric (review ⑤). pvals = {ten: p} -> {ten: p_da_hieu_chinh}."""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items); out = {}; prev = 0.0
    for i, (k, p) in enumerate(items):
        prev = min(1.0, max(prev, (m - i) * p)); out[k] = prev
    return out

def main():
    random.seed(SEED)
    files = sorted(glob.glob(os.path.join(RUNS, "*.json")))
    lim = int(os.environ.get("DG1_LIMIT", "0"))
    if lim: files = files[:lim]
    if not files: print("Khong co run."); return
    runs = [json.load(open(f, encoding="utf-8")) for f in files]
    apps = sorted({r["screen"].split("_")[0] for r in runs})

    print("=" * 84)
    print(f"PA2 (matched/fallback) | he-quyet=nomic τA={TAU_A} | cham=bge-m3 DOC LAP | {len(runs)} man | app={apps}")
    print("=" * 84)
    if len(apps) == 1:
        print(f"  /!\\ CHI 1 APP -> CI gia-chat, ngoai-suy yeu. Ban chinh PHAI nhieu app.\n")

    # tong hop hanh vi PA2 (khong phu thuoc tauB)
    tot_steps = tot_fb = 0
    pa2_by_run = []
    for r in runs:
        labels = r["elem_labels"]
        pa2 = derive_pa2(r["base"], labels, TAU_A)
        pa2_by_run.append(pa2)
        tot_steps += len(pa2); tot_fb += sum(1 for s in pa2 if s["status"] == "fallback")
    print(f"HANH VI PA2: {tot_steps} buoc, fallback {tot_fb} ({tot_fb/tot_steps*100:.0f}%), "
          f"matched {tot_steps-tot_fb} ({(tot_steps-tot_fb)/tot_steps*100:.0f}%); correction=0; silent-error=0 (cau truc).\n")

    # cham theo tung tauB (robustness)
    for tauB in TAUS_B:
        agg = {"faith": {"b": [], "e": []}, "grounded": {"b": [], "e": []}, "label_fid": {"b": [], "e": []},
               "format": {"b": [], "e": []}}
        d_faith = []; d_label = []
        for r, pa2 in zip(runs, pa2_by_run):
            app = r["screen"].split("_")[0]
            labels = r["elem_labels"]
            mb = score(r["base"], labels, tauB)                  # BASE: khong status -> all button
            me = score(pa2, labels, tauB)
            for k in agg: agg[k]["b"].append(mb[k]); agg[k]["e"].append(me[k])
            d_faith.append((app, me["faith"] - mb["faith"])); d_label.append((app, me["label_fid"] - mb["label_fid"]))
        def m(x): return sum(x)/len(x)*100
        lo_f, hi_f, p_f = boot_ci_cluster(d_faith); lo_l, hi_l, p_l = boot_ci_cluster(d_label)
        padj = holm({"faith": p_f, "label": p_l})                # Holm cho 2 metric headline
        print(f"--- CHAM voi tauB={tauB:.2f} (bge-m3) | CI = cluster bootstrap theo APP ---")
        print(f"  Faithfulness   BASE {m(agg['faith']['b']):5.1f}%  -> PA2 {m(agg['faith']['e']):5.1f}%   "
              f"chenh {m(agg['faith']['e'])-m(agg['faith']['b']):+5.1f}pp [{lo_f*100:+.1f},{hi_f*100:+.1f}]  p_Holm={padj['faith']:.3f}")
        print(f"  Grounded-exist BASE {m(agg['grounded']['b']):5.1f}%  -> PA2 {m(agg['grounded']['e']):5.1f}%")
        print(f"  Label-fidelity BASE {m(agg['label_fid']['b']):5.1f}%  -> PA2 {m(agg['label_fid']['e']):5.1f}%   "
              f"chenh {m(agg['label_fid']['e'])-m(agg['label_fid']['b']):+5.1f}pp [{lo_l*100:+.1f},{hi_l*100:+.1f}]  p_Holm={padj['label']:.3f} (ky vong ~0 = no-harm)")
        print(f"  Format         BASE {m(agg['format']['b']):5.1f}%  -> PA2 {m(agg['format']['e']):5.1f}%\n")

    print("DOC: PA2 claim DUY NHAT = giam tham-chieu-nut-khong-ton-tai (faithfulness, scorer DOC LAP),")
    print("gia = % fallback. Label-fidelity ~dung yen (no-harm). 'Sua-dung' de cho AndroidControl/DG2 (co gold).")

if __name__ == "__main__":
    main()
