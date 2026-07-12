# -*- coding: utf-8 -*-
"""
CHAM TAT CA metric DG1 tren cac run (harness/dg1_cache/runs/): BASE vs design-E, theo tung model.
Metric: Faithfulness(khong-lenh-sai-tu-tin) · Dung-nhan(Clarity) · Grounded-existence · Format · Coverage(proxy).
Bao chenh BASE->design-E + bootstrap CI ghep-cap (per-man). Khong can numpy.
"""
import os, sys, json, glob, re, random
sys.path.insert(0, os.path.dirname(__file__))
from aloha_match import best_match, exact_label

RUNS = os.path.join(os.path.dirname(__file__), "dg1_cache", "runs")
TAU = 0.55
VERBS = ("bấm", "chọn", "nhập", "mở", "vào", "gõ", "kéo", "cuộn", "nhấn", "tìm", "tích", "bật", "tắt", "xem",
         # tieng Anh (phan dinh luong)
         "tap", "click", "select", "enter", "type", "open", "choose", "press", "find", "scroll",
         "toggle", "set", "view", "add", "create", "delete", "edit", "update", "change", "go",
         "navigate", "check", "switch", "swipe", "drag", "fill", "input", "pick", "turn")

def is_real(name, labels):
    _, sim = best_match(name, labels); return sim >= TAU
def starts_verb(verb):
    return any((verb or "").strip().lower().startswith(v) for v in VERBS)

def metrics(steps, labels, actionable, is_sysE):
    n = len(steps) or 1
    button_steps = [s for s in steps if s.get("status") != "fallback"]   # buoc tro toi nut
    # Faithfulness = 1 - tỉ lệ "claim nút mà nút KHONG ton tai"
    if is_sysE:
        confident_wrong = sum(1 for s in button_steps if not is_real(s["element"], labels))
    else:
        confident_wrong = sum(1 for s in steps if not is_real(s.get("element",""), labels))
    faith = 1 - confident_wrong / n
    # Dung-nhan (clarity): trong cac buoc tro-nut, % goi dung ten hien thi
    nb = len(button_steps) or 1
    label_fid = sum(1 for s in button_steps if exact_label(s["element"], labels)) / nb
    # Grounded-existence
    grounded = sum(1 for s in button_steps if is_real(s["element"], labels)) / n
    # Format: % buoc bat dau bang dong tu menh lenh
    fmt = sum(1 for s in steps if starts_verb(s.get("verb",""))) / n
    # Coverage proxy: so nut THAT duy nhat duoc nhac / nut actionable
    matched = set()
    for s in button_steps:
        e, sim = best_match(s["element"], labels)
        if sim >= TAU: matched.add(e)
    cov = len(matched) / (len(actionable) or 1)
    return {"faith": faith, "label_fid": label_fid, "grounded": grounded, "format": fmt, "coverage": cov,
            "n_fallback": sum(1 for s in steps if s.get("status")=="fallback"),
            "n_corrected": sum(1 for s in steps if s.get("status")=="corrected")}

def boot_ci(deltas, it=2000):
    if not deltas: return (0,0)
    n=len(deltas); means=[]
    for _ in range(it):
        s=[deltas[random.randrange(n)] for _ in range(n)]
        means.append(sum(s)/n)
    means.sort(); return (means[int(0.025*it)], means[int(0.975*it)])

def main():
    files=sorted(glob.glob(os.path.join(RUNS,"*.json")))
    if not files: print("Chua co run nao — chay dg1_run.py truoc."); return
    by_model={}
    for fp in files:
        r=json.load(open(fp,encoding="utf-8")); by_model.setdefault(r.get("model","?"),[]).append(r)
    for model, runs in by_model.items():
        print("="*78); print(f"MODEL = {model}  | {len(runs)} man"); print("="*78)
        agg={k:{"base":[],"sysE":[]} for k in ("faith","label_fid","grounded","format","coverage")}
        d_faith=[]; d_label=[]; corr=0; fb=0
        for r in runs:
            labels=r["elem_labels"]; act=r["actionable_labels"]
            mb=metrics(r["base"],labels,act,False); ms=metrics(r["sysE"],labels,act,True)
            for k in agg: agg[k]["base"].append(mb[k]); agg[k]["sysE"].append(ms[k])
            d_faith.append(ms["faith"]-mb["faith"]); d_label.append(ms["label_fid"]-mb["label_fid"])
            corr+=ms["n_corrected"]; fb+=ms["n_fallback"]
        def m(x): return sum(x)/len(x)*100
        print(f"  {'Metric':<22}{'BASE':>8}{'design-E':>10}   chenh [95% CI]")
        for k,lab in [("faith","Faithfulness"),("label_fid","Dung-nhan/Clarity"),
                      ("grounded","Grounded-exist"),("format","Format"),("coverage","Coverage(proxy)")]:
            b=m(agg[k]["base"]); s=m(agg[k]["sysE"])
            extra=""
            if k=="faith":
                lo,hi=boot_ci(d_faith); extra=f"   +{(s-b):.1f}pp  [{lo*100:+.1f},{hi*100:+.1f}]"
            if k=="label_fid":
                lo,hi=boot_ci(d_label); extra=f"   +{(s-b):.1f}pp  [{lo*100:+.1f},{hi*100:+.1f}]"
            print(f"  {lab:<22}{b:7.1f}%{s:9.1f}%{extra}")
        print(f"  (design-E: SUA {corr} buoc thanh nut THAT, FALLBACK {fb} buoc mo ta bang loi)")
    print("\nLUU Y: Faithfulness design-E ~100% la DO THIET KE (he khong phat ra lenh-sai-tu-tin);")
    print("gia tri do duoc = BASE bia bao nhieu + he SUA/FALLBACK bao nhieu. Dung-nhan tang la that.")

if __name__=="__main__":
    main()
