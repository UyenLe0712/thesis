# -*- coding: utf-8 -*-
"""
Phép thử khả thi ĐƯỜNG TOẠ-ĐỘ (report/92 đường 3). ✱ TỐN API (~$0.5 gpt-4o-mini vision).
Câu hỏi: một "bộ trỏ" có định vị đúng nút từ CÂU HƯỚNG DẪN GOLD không? Nếu ngay cả câu-đúng
mà trỏ trật thì cả đường chấm-bằng-toạ-độ chết.

Cách: với mỗi ảnh có gold (x,y), đưa gpt-4o-mini vision (ảnh + câu gold) → nó trả (x,y).
So với gold (x,y), tính TRÚNG trong dung sai (báo ở nhiều mức để không cherry-pick).
Dùng câu GOLD (không phải output model) để tách "bộ trỏ có tìm được nút" khỏi "câu có tốt".
Cache lại, không gọi trùng.

Chạy: ~/.venvs/thesis/bin/python harness/ground_pilot.py
"""
import os, sys, json, re, glob, base64, io, time
sys.path.insert(0, os.path.dirname(__file__))
from _http import chat
from _apikey import get_key
from PIL import Image

MAXW = 512        # thu nhỏ ảnh để né rate-limit (đủ cho trỏ) — xin toạ độ CHUẨN HOÁ 0-1000

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, "dg1_cache", "mde_pilot", "gen.json")
CACHE = os.path.join(HERE, "dg1_cache", "ground_pilot")
os.makedirs(CACHE, exist_ok=True)
PRED = os.path.join(CACHE, "pred.json")
HF = os.path.expanduser("~/.cache/huggingface/hub/datasets--wangyuanlei--android_control_test/snapshots")
MODEL = "gpt-4o-mini"
BASE = "https://api.openai.com/v1"

PROMPT = ("This is a screenshot of a mobile app. A user is told: \"{instr}\". "
          "Give the location to tap to follow this instruction, as two integers 'x,y' "
          "in a 0-1000 normalized grid (x=0 left, x=1000 right, y=0 top, y=1000 bottom). "
          "Answer with ONLY 'x,y', nothing else.")


def find_episode(eid):
    hits = glob.glob(os.path.join(HF, "*", "test_output_json", "*", f"episode_{eid}.json"))
    return hits[0] if hits else None


def find_png(rel):
    hits = glob.glob(os.path.join(HF, "*", rel))
    return hits[0] if hits else None


def parse_xy(s):
    nums = re.findall(r"-?\d+\.?\d*", s or "")
    if len(nums) >= 2:
        return float(nums[0]), float(nums[1])
    return None


def main():
    gen = json.load(open(GEN, encoding="utf-8"))
    items = []
    for rel in gen:
        m = re.search(r"episode_(\d+)_screenshot_(\d+)\.png", rel)
        if not m:
            continue
        eid, si = int(m.group(1)), int(m.group(2))
        ep, png = find_episode(eid), find_png(rel)
        if not ep or not png:
            continue
        o = json.load(open(ep, encoding="utf-8"))
        acts = o.get("actions") or []
        insts = o.get("step_instructions") or []
        if si >= len(acts) or si >= len(insts):
            continue
        a = acts[si]
        if a.get("action_type") not in ("click", "long_press") or "x" not in a:
            continue                                   # chỉ bước CÓ toạ độ gold
        items.append({"rel": rel, "png": png, "instr": insts[si],
                      "gx": float(a["x"]), "gy": float(a["y"])})
    print(f"Bước có gold toạ độ + ảnh local: {len(items)}")

    pred = json.load(open(PRED, encoding="utf-8")) if os.path.exists(PRED) else {}
    key = get_key()
    if key == "ollama":
        print("⚠ Không thấy API key (harness/.openai_key) — dừng, không gọi được."); return
    n_call = 0
    for it in items:
        if it["rel"] in pred:
            continue
        im = Image.open(it["png"]).convert("RGB")
        w, h = im.size
        sc = im.resize((MAXW, int(h * MAXW / w)), Image.LANCZOS) if w > MAXW else im
        buf = io.BytesIO(); sc.save(buf, "JPEG", quality=85)
        uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        msgs = [{"role": "user", "content": [
            {"type": "text", "text": PROMPT.format(instr=it["instr"])},
            {"type": "image_url", "image_url": {"url": uri}}]}]
        out = chat(BASE, MODEL, msgs, key, temperature=0)
        xy = parse_xy(out)               # toạ độ chuẩn hoá 0-1000 → đổi về pixel gốc
        pred[it["rel"]] = {"w": w, "h": h, "raw": out,
                           "px": xy[0] / 1000.0 * w if xy else None,
                           "py": xy[1] / 1000.0 * h if xy else None}
        n_call += 1
        json.dump(pred, open(PRED, "w", encoding="utf-8"), ensure_ascii=False)
        if n_call % 10 == 0:
            print(f"  ...{n_call} lượt gọi")
        time.sleep(5.0)                  # giãn nhịp né rate-limit TPM
    print(f"Gọi API mới: {n_call} lượt")

    # ---- chấm trúng ở nhiều dung sai ----
    tols = [0.05, 0.10, 0.14]      # theo cạnh dài màn (AITW dùng ~14%)
    hit = {t: 0 for t in tols}
    scored, unparsed = 0, 0
    dists = []
    for it in items:
        p = pred.get(it["rel"])
        if not p or p["px"] is None:
            unparsed += 1; continue
        w, h = p["w"], p["h"]
        dx = (p["px"] - it["gx"]) / w
        dy = (p["py"] - it["gy"]) / h
        d = (dx * dx + dy * dy) ** 0.5     # khoảng cách chuẩn hoá theo kích thước màn
        dists.append(d)
        scored += 1
        for t in tols:
            if abs(p["px"] - it["gx"]) <= t * w and abs(p["py"] - it["gy"]) <= t * h:
                hit[t] += 1

    print("\n" + "=" * 68)
    print(f"CHẤM {scored} bước (bỏ {unparsed} không đọc được toạ độ)")
    for t in tols:
        print(f"  trúng trong ±{int(t*100)}% cạnh màn: {hit[t]}/{scored} = {hit[t]/max(scored,1):.1%}")
    if dists:
        dists.sort()
        md = dists[len(dists)//2]
        print(f"  khoảng cách chuẩn hoá trung vị = {md:.3f} (0=trùng khít)")
    print("=" * 68)
    print("\nĐọc số: trúng ±14% CAO (~80%+) → bộ trỏ đáng tin → đường toạ-độ SỐNG.")
    print("Thấp → model nhỏ trỏ kém / bài khó → cần bộ trỏ mạnh hơn (Colab).")

    json.dump({"n": scored, "unparsed": unparsed,
               "hit_5": hit[0.05]/max(scored,1), "hit_10": hit[0.10]/max(scored,1),
               "hit_14": hit[0.14]/max(scored,1),
               "median_dist": dists[len(dists)//2] if dists else None},
              open(os.path.join(HERE, "ground_pilot_results.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("Đã lưu ground_pilot_results.json")


if __name__ == "__main__":
    main()
