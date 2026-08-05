# -*- coding: utf-8 -*-
"""
Tao CAU HOI use-case cho tung man (Qwen nhin man -> de xuat 1 cau hoi cu the).
Luu ra harness/dg1_cache/questions.json -> NGUOI DUYET truoc khi sinh tutorial (chong leak/thien vi).
"""
import os, sys, json, glob, base64, urllib.request

sys.path.insert(0, os.path.dirname(__file__))
import time
from _apikey import get_key
from _http import chat
FOLDER = os.path.join(os.path.dirname(__file__), "..", "dataset_samples", "mv_multiapp")
OUT = os.path.join(os.path.dirname(__file__), "dg1_cache"); os.makedirs(OUT, exist_ok=True)
QFILE = os.path.join(OUT, "questions.json")

BASE = os.environ.get("VLM_BASE_URL", "http://localhost:11434/v1")
MODEL = os.environ.get("VLM_MODEL", "qwen2.5vl:3b")

QPROMPT = """Look at this app screenshot. Write ONE short, realistic use-case question a real user might ask about THIS screen — like "How do I ...?" or "Where do I tap to ...?".
It must be about something DOABLE right now on this screen (based on the visible buttons/fields), not something absent.
Return ONLY one question in English, no explanation, nothing else."""

def vision_call(img_path, prompt):
    with open(img_path, "rb") as f:
        uri = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
    msgs = [{"role": "user", "content": [
        {"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": uri}}]}]
    return chat(BASE, MODEL, msgs, get_key(), temperature=0.2).strip()

def main():
    # giu lai cau da co (resume duoc) + 3 man goc da-app
    qs = json.load(open(QFILE, encoding="utf-8")) if os.path.exists(QFILE) else {}
    vhs = sorted(glob.glob(os.path.join(FOLDER, "*.viewhierarchy.json")))
    lim = int(os.environ.get("DG1_LIMIT", "0"))
    if lim: vhs = vhs[:lim]
    for i, vh in enumerate(vhs):
        name = os.path.basename(vh).split(".")[0]
        if name in qs:
            continue
        img = vh.replace(".viewhierarchy.json", ".jpg")
        try:
            q = vision_call(img, QPROMPT).splitlines()[0].strip().strip('"')
        except Exception as ex:
            q = f"[LOI {repr(ex)[:50]}]"
        qs[name] = q
        json.dump(qs, open(QFILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)  # luu dan (resume)
        print(f"  [{i+1}/{len(vhs)}] {name}: {q}")
        time.sleep(0.6)   # ne rate-limit
    print(f"xong {len(qs)} cau -> {QFILE}")

if __name__ == "__main__":
    main()
