# -*- coding: utf-8 -*-
"""
Sinh tutorial tren mv_trace/ va LUU raw ra harness/gen_cache/<man>.json.
Sinh 1 lan (cham, CPU) -> sau do cham lai bao nhieu lan tuy y (mien phi, tuc thi).
"""
import os, sys, json, glob
sys.path.insert(0, os.path.dirname(__file__))
from dg1_scorer import load_screen
from run_dg1_trial import call_vlm, parse_steps

FOLDER = os.path.join(os.path.dirname(__file__), "..", "dataset_samples", "mv_trace")
OUT = os.path.join(os.path.dirname(__file__), "gen_cache")
os.makedirs(OUT, exist_ok=True)
Q = ("Trên màn hình này, hãy hướng dẫn người dùng CÁC BƯỚC thao tác chính "
     "(bấm hoặc nhập vào đâu) để dùng chức năng chính của màn. "
     "Gọi ĐÚNG TÊN nút/ô hiển thị, không bịa nút không có.")

def main():
    vhs = sorted(glob.glob(os.path.join(FOLDER, "*.viewhierarchy.json")))
    print(f"sinh + luu {len(vhs)} man, model={os.environ.get('VLM_MODEL')}")
    for vh in vhs:
        sc = load_screen(vh)
        img = vh.replace(".viewhierarchy.json", ".jpg")
        try:
            steps = parse_steps(call_vlm(img, Q))
        except Exception as ex:
            print(f"  {sc['name']}: LOI {repr(ex)[:80]}"); continue
        rec = {"screen": sc["name"], "question": Q,
               "elem_labels": [e["label"] for e in sc["elems"]],
               "actionable_labels": [e["label"] for e in sc["elems"] if e["actionable"]],
               "steps": [{"verb": s.get("verb", ""), "element": s.get("element", ""),
                          "note": s.get("note", "")} for s in steps]}
        with open(os.path.join(OUT, sc["name"] + ".json"), "w", encoding="utf-8") as f:
            json.dump(rec, f, ensure_ascii=False, indent=2)
        print(f"  {sc['name']}: luu {len(rec['steps'])} buoc")
    print("xong -> harness/gen_cache/")

if __name__ == "__main__":
    main()
