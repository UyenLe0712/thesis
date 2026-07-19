# -*- coding: utf-8 -*-
"""
Pilot đo-nền để tính MDE trục ĐÚNG (report/85 §6). ✱ TỐN API (gpt-4o-mini, ~$0.3-1).
Lấy ~50 (ảnh + gold-step + app) từ app_unseen split → teacher sinh bước → chấm (action,target)
→ độ-dao-động điểm-đúng PER-APP → SD → MDE. Cache generation + ảnh (resume, không gọi trùng).

Chạy: ~/.venvs/thesis/bin/python harness/mde_pilot.py
"""
import os, sys, json, re, base64, math, random
sys.path.insert(0, os.path.dirname(__file__))
from huggingface_hub import HfApi, hf_hub_download
from datasets import load_dataset
from _http import chat
from _apikey import get_key
from metric_v1_validate import canon_action, target_of, target_score

HERE = os.path.dirname(__file__)
CACHE = os.path.join(HERE, "dg1_cache", "mde_pilot")
os.makedirs(CACHE, exist_ok=True)
GEN_CACHE = os.path.join(CACHE, "gen.json")
N_APPS = 15
STEPS_PER_APP = 4
MODEL = "gpt-4o-mini"
BASE = "https://api.openai.com/v1"
REPO = "wangyuanlei/android_control_test"

PROMPT = ("Below is a screenshot of a mobile app. The user's overall goal is: \"{goal}\".\n"
          "Write ONE short next-step instruction for a human to do on THIS screen to move toward the goal, "
          "in the style \"Tap the Search bar\" or \"Type your email in the input field\". "
          "Output ONLY the single instruction sentence, nothing else.")

def app_of(goal, actions):
    for a in actions or []:
        if a.get("action_type") == "open_app" and a.get("app_name"):
            return a["app_name"]
    m = re.search(r"\b(?:the |using |on |open )?([A-Z][A-Za-z0-9&\.\- ]{1,20}?) app\b", goal or "")
    return m.group(1).strip() if m else None

def main():
    api = HfApi()
    files = api.list_repo_files(REPO, repo_type="dataset")
    id2json = {}
    png_set = set(f for f in files if f.endswith(".png"))
    for f in files:
        if f.endswith(".json"):
            m = re.search(r"episode_(\d+)\.json", f)
            if m: id2json[int(m.group(1))] = f
    app_unseen = next(iter(load_dataset("reece124/android_control", split="test", streaming=True)))["app_unseen"]

    # thu thập tới N_APPS app, mỗi app STEPS_PER_APP bước (ảnh có click/type)
    rng = random.Random(7)
    ids = [i for i in app_unseen if i in id2json]; rng.shuffle(ids)
    per_app = {}     # app -> list of (goal, gold_instr, png_path)
    for eid in ids:
        if len([a for a in per_app if len(per_app[a]) >= STEPS_PER_APP]) >= N_APPS:
            break
        try:
            o = json.load(open(hf_hub_download(REPO, id2json[eid], repo_type="dataset"), encoding="utf-8"))
        except Exception:
            continue
        app = app_of(o.get("goal"), o.get("actions"))
        if not app:
            continue
        insts = o.get("step_instructions") or []; acts = o.get("actions") or []
        for si, ins in enumerate(insts):
            if per_app.get(app) and len(per_app[app]) >= STEPS_PER_APP:
                break
            at = acts[si].get("action_type") if si < len(acts) else None
            if at not in ("click", "long_press", "input_text"):
                continue
            png = f"android_control-{eid//1000:05d}"  # đoán shard sai -> tra png_set
            cand = [p for p in png_set if f"episode_{eid}_screenshot_{si}.png" in p]
            if not cand:
                continue
            per_app.setdefault(app, []).append((o.get("goal"), ins, cand[0]))
    per_app = {a: v for a, v in per_app.items() if len(v) >= 2}
    print(f"Thu thập: {len(per_app)} app, {sum(len(v) for v in per_app.values())} bước")

    gen = json.load(open(GEN_CACHE, encoding="utf-8")) if os.path.exists(GEN_CACHE) else {}
    key = get_key()
    n_call = 0
    app_scores = {}
    for app, items in per_app.items():
        scores = []
        for goal, gold, png in items:
            ck = png
            if ck not in gen:
                imgp = hf_hub_download(REPO, png, repo_type="dataset")
                uri = "data:image/png;base64," + base64.b64encode(open(imgp, "rb").read()).decode()
                msgs = [{"role": "user", "content": [
                    {"type": "text", "text": PROMPT.format(goal=goal)},
                    {"type": "image_url", "image_url": {"url": uri}}]}]
                gen[ck] = chat(BASE, MODEL, msgs, key, temperature=0)
                n_call += 1
                json.dump(gen, open(GEN_CACHE, "w", encoding="utf-8"), ensure_ascii=False)
            out = gen[ck]
            # chấm: action khớp VÀ target khớp
            a_ok = canon_action(out) == canon_action(gold)
            ts = target_score(target_of(out), target_of(gold))
            scores.append(1.0 if (a_ok and ts >= 0.5) else 0.0)
        app_scores[app] = sum(scores) / len(scores)
    print(f"Gọi API mới: {n_call} lần")

    vals = list(app_scores.values())
    G = len(vals)
    mean = sum(vals) / G
    sd = math.sqrt(sum((v - mean) ** 2 for v in vals) / (G - 1)) if G > 1 else float("nan")
    # SD của HIỆU (bảo thủ) ~ sqrt(2)*SD một arm (report/56)
    sd_diff = math.sqrt(2) * sd
    print("\n=== ĐIỂM-ĐÚNG per-app (teacher gpt-4o-mini) ===")
    for a, v in sorted(app_scores.items(), key=lambda x: -x[1]):
        print(f"    {a[:24]:24} {v:.3f}  (n={len(per_app[a])})")
    print(f"\n  mean={mean:.3f} | SD per-app(1 arm)={sd:.3f} | SD hiệu bảo thủ={sd_diff:.3f}")
    print("\n  MDE = 3.077 × SD_hiệu / sqrt(G):")
    for Gt in [G, 50, 100, 150, 200]:
        mde = 3.077 * sd_diff / math.sqrt(Gt)
        print(f"    G={Gt:4d} -> MDE = {mde:.3f} = {mde*100:.1f} điểm phần trăm")
    json.dump({"n_apps": G, "mean": mean, "sd_1arm": sd, "sd_diff": sd_diff,
               "app_scores": app_scores, "n_steps": sum(len(v) for v in per_app.values())},
              open(os.path.join(HERE, "mde_pilot_results.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nĐã lưu mde_pilot_results.json")

if __name__ == "__main__":
    main()
