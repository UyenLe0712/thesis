# -*- coding: utf-8 -*-
"""
DG1 — SINH BASE tren mv_multiapp DA LOC (man trong kept_screens.json).
Moi man: anh + cau hoi -> VLM sinh tutorial BASE (goi nut theo TEN, ep JSON). Luu base + nhan da-loc-rac.
PA2 (matched/fallback) + CHAM = lam SAU bang dg1_pa2_score.py (FREE). File nay CHI lo phan TON API (sinh).
Resume: bo qua man da co cache. Route qua _http.chat (retry 429 — va bug T1: truoc day urllib tho khong retry).

Chay (TON API ~$0.05 — HOI USER TRUOC):
  PYTHONIOENCODING=utf-8 VLM_MODEL=gpt-4o-mini VLM_BASE_URL=https://api.openai.com/v1 python dg1_run.py
(VLM nhin-anh local bat kha vi may KHONG GPU -> dung API cloud.)
"""
import os, sys, json, base64, time
sys.path.insert(0, os.path.dirname(__file__))
from run_dg1_trial import parse_steps                  # parse JSON steps (ngon-ngu-doc-lap)
from dg1_data import MV_DIR, is_junk, kept_screens, app_of
from dg1_scorer import load_screen
from _apikey import get_key
from _http import chat

CACHE = os.path.join(os.path.dirname(__file__), "dg1_cache")
RUNS = os.path.join(CACHE, "runs"); os.makedirs(RUNS, exist_ok=True)
QFILE = os.path.join(CACHE, "questions.json")
MODEL = os.environ.get("VLM_MODEL", "gpt-4o-mini")
BASE_URL = os.environ.get("VLM_BASE_URL", "https://api.openai.com/v1")

GEN_PROMPT = """You are an assistant that writes step-by-step app-usage instructions from a screenshot.
User's request: "{q}"
Write the steps. Each step must name the button/field by its EXACT on-screen text. Do NOT invent buttons that are not visible.
Return ONLY JSON, nothing else: {{"steps":[{{"verb":"<Tap/Select/Enter/Open/Type...>","element":"<exact on-screen name>","note":"<short>"}}]}}"""

def gen_tutorial(img_path, q):
    with open(img_path, "rb") as f:
        uri = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
    msgs = [{"role": "user", "content": [
        {"type": "text", "text": GEN_PROMPT.format(q=q)},
        {"type": "image_url", "image_url": {"url": uri}}]}]
    return chat(BASE_URL, MODEL, msgs, get_key(), temperature=0)      # retry/backoff (va T1)

def main():
    keep = kept_screens()
    if keep is None:
        print("Chua co kept_screens.json -> chay dg1_filter_data.py truoc."); return
    if not os.path.exists(QFILE):
        print("Chua co questions.json -> chay dg1_questions.py (affordance-seeded) truoc."); return
    qs = json.load(open(QFILE, encoding="utf-8"))
    tag = MODEL.replace(":", "_").replace("/", "_")
    lim = int(os.environ.get("DG1_LIMIT", "0"))
    names = sorted(keep)
    if lim: names = names[:lim]
    done = ok = 0
    for name in names:
        outfp = os.path.join(RUNS, f"{name}__{tag}.json")
        if os.path.exists(outfp):                 # resume — khong goi lai API
            ok += 1; continue
        q = qs.get(name)
        if not q or str(q).startswith("[LOI"):
            print(f"  {name}: thieu cau hoi -> bo qua"); continue
        vh = os.path.join(MV_DIR, name + ".viewhierarchy.json")
        img = os.path.join(MV_DIR, name + ".jpg")
        sc = load_screen(vh)
        elems = [e for e in sc["elems"] if not is_junk(e["label"])]     # loc nhan rac
        labels = [e["label"] for e in elems]
        act = [e["label"] for e in elems if e["actionable"]]
        try:
            base = parse_steps(gen_tutorial(img, q))
        except Exception as ex:
            print(f"  {name}: LOI sinh {repr(ex)[:70]}"); continue
        base = [{"verb": s.get("verb",""), "element": s.get("element",""), "note": s.get("note","")} for s in base]
        rec = {"screen": name, "app": app_of(name), "model": MODEL, "question": q,
               "elem_labels": labels, "actionable_labels": act, "base": base}
        json.dump(rec, open(outfp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        done += 1; ok += 1
        print(f"  [{done}] {name}: BASE {len(base)} buoc")
        time.sleep(0.4)
    print(f"xong: sinh moi {done} | tong san sang {ok}/{len(names)} man (model={MODEL}, tag={tag}) -> {RUNS}")

if __name__ == "__main__":
    main()
