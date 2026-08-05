# -*- coding: utf-8 -*-
"""Scan metadata AndroidControl test (smolagents) — KHONG luu anh, chi lay N/app/action de CHON episode da dang.

App-diversity: suy 'app' theo thu tu tin cay:
  1. action open_app -> app_name  (chac chan nhat)
  2. parse tu 'goal': mau '... on/in/using the <App> app'  (dataset thuong ghi ten app trong goal)
  3. neu van khong ra -> 'unknown'
Dung select_columns bo cot screenshots_b64 -> scan nhanh, khong tai anh.
Chay:  CAP=1600 PYTHONIOENCODING=utf-8 python harness/scan_androidcontrol.py
"""
import json, os, re
from datasets import load_dataset

OUT = "dataset_samples/androidcontrol_meta.json"
CAP = int(os.environ.get("CAP", "1600"))   # test set = 1542 ep

# mau bat ten app trong goal: "... on the Box app", "on Omio app", "in the Drive app"
APP_IN_GOAL = re.compile(r"\b(?:on|in|using|from|to|via|open|onto)\s+(?:the\s+|my\s+|your\s+)?"
                         r"([A-Z][A-Za-z0-9&.'+\- ]{1,28}?)\s+app\b")

def app_from_goal(goal):
    if not goal:
        return None
    m = APP_IN_GOAL.search(goal)
    if m:
        name = m.group(1).strip(" .'-")
        # loai vai tu chung de tranh nhieu
        if name and name.lower() not in ("the", "an", "a", "this", "that", "same"):
            return name
    return None

ds = load_dataset('smolagents/android-control', streaming=True, split='test')
try:
    ds = ds.select_columns(['episode_id', 'goal', 'actions'])   # bo screenshots_b64 -> nhanh
except Exception:
    pass  # neu ban datasets khong ho tro, van chay (cham hon)

meta = []
n = 0
src = {"open_app": 0, "goal": 0, "unknown": 0}
for row in ds:
    n += 1
    if n > CAP:
        break
    acts = row.get('actions') or []
    app = None
    atypes = set()
    for a in acts:
        if isinstance(a, dict):
            atypes.add(a.get('action_type'))
            if a.get('action_type') == 'open_app' and a.get('app_name'):
                app = a['app_name']
    how = "open_app" if app else None
    if not app:
        app = app_from_goal(row.get('goal'))
        how = "goal" if app else "unknown"
    src[how] = src.get(how, 0) + 1
    meta.append(dict(episode_id=row.get('episode_id'), N=len(acts),
                     app=app or 'unknown', app_src=how,
                     atypes=sorted(x for x in atypes if x)))
    if n % 100 == 0:
        json.dump(meta, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
        print(f"scanned {n} | #app={len(set(m['app'] for m in meta if m['app']!='unknown'))} "
              f"| src open_app={src['open_app']} goal={src['goal']} unknown={src['unknown']}")

json.dump(meta, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
napp = len(set(m['app'] for m in meta if m['app'] != 'unknown'))
print(f"DONE scanned {len(meta)} ep | #app xac dinh={napp} "
      f"| nguon: open_app={src['open_app']} goal={src['goal']} unknown={src['unknown']} -> {OUT}")
