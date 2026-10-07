# -*- coding: utf-8 -*-
"""
FREE · offline — chạy lại bộ dò OmniParser-v2 và lưu HỘP (không chỉ tâm).

Lý do: bản trước chỉ cache tâm nên không kiểm được giả thuyết "bộ dò trả nhiều hộp cho cùng
một nút". Có hộp thì kiểm được bằng IoU, và quan trọng hơn là chấm được theo cách đúng bản
chất: **loại hộp CHỨA điểm gold** (hộp của chính nút đang chạm) thay vì quét theo bán kính.

Chạy: ~/.venvs/thesis/bin/python harness/omni_boxes.py
"""
import os, sys, re, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
HF = os.path.expanduser("~/.cache/huggingface/hub/datasets--wangyuanlei--android_control_test/snapshots")
OUT = os.path.join(HERE, "dg1_cache", "omni_box")
os.makedirs(OUT, exist_ok=True)


def find_png(rel):
    h = glob.glob(os.path.join(HF, "*", rel))
    return h[0] if h else None


def key_of(rel):
    return re.sub(r"[^\w]", "_", os.path.basename(rel)) + ".json"


def boxes(rel, model):
    p = os.path.join(OUT, key_of(rel))
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8"))
    png = find_png(rel)
    if not png:
        return []
    r = model.predict(png, conf=0.05, iou=0.1, verbose=False)[0]
    bs = [[float(v) for v in b] for b in r.boxes.xyxy.tolist()]
    json.dump(bs, open(p, "w"), ensure_ascii=False)
    return bs


def main():
    from ultralytics import YOLO
    from huggingface_hub import hf_hub_download
    model = YOLO(hf_hub_download("microsoft/OmniParser-v2.0", "icon_detect/model.pt"))
    pred = json.load(open(os.path.join(HERE, "dg1_cache", "ground_pilot", "pred.json"), encoding="utf-8"))
    n = 0
    for rel in pred:
        bs = boxes(rel, model)
        n += 1
        if n % 20 == 0:
            print(f"  ...{n} màn")
    print(f"Xong {n} màn → {OUT}")


if __name__ == "__main__":
    main()
