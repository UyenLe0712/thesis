# -*- coding: utf-8 -*-
"""
Đo SÀN Exec(∅) (lỗ #4, report/96/97). ✱ TỐN API (~$0.3 gpt-4o-mini vision).
Thước executability: giá-trị-thật-của-câu = Exec(CÓ câu) − Exec(KHÔNG câu = sàn).
ground_pilot.py đã đo Exec(CÓ câu gold) = 51.3%. File này đo SÀN: đưa grounder ẢNH
nhưng KHÔNG đưa câu — nó chỉ ĐOÁN nút dễ-bấm-nhất → trúng ±14% gold bao nhiêu?
Sàn cao → dung sai rộng khiến đoán-bừa cũng hay trúng → hiệu số bị nén → "72−30=42"
của report/94 lạc quan.

Dùng ĐÚNG 76 bước + ảnh + cách chấm của ground_pilot.py để so sánh theo cặp.
Cache riêng, không gọi trùng.

Chạy: ~/.venvs/thesis/bin/python harness/ground_floor.py
"""
import os, sys, json, re, base64, io, time
sys.path.insert(0, os.path.dirname(__file__))
from _http import chat
from _apikey import get_key
from PIL import Image
from ground_pilot import find_episode, find_png, parse_xy, GEN, HF, MODEL, BASE, MAXW

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "dg1_cache", "ground_floor")
os.makedirs(CACHE, exist_ok=True)
PRED = os.path.join(CACHE, "pred.json")

# KHÔNG có câu hướng dẫn — grounder chỉ được nhìn ảnh, phải đoán nút dễ-bấm-nhất.
PROMPT = ("This is a screenshot of a mobile app. Without any instruction, predict the single "
          "location a user is most likely to tap next, as two integers 'x,y' in a 0-1000 "
          "normalized grid (x=0 left, x=1000 right, y=0 top, y=1000 bottom). "
          "Answer with ONLY 'x,y', nothing else.")


def build_items():
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
        if si >= len(acts):
            continue
        a = acts[si]
        if a.get("action_type") not in ("click", "long_press") or "x" not in a:
            continue
        items.append({"rel": rel, "png": png, "gx": float(a["x"]), "gy": float(a["y"])})
    return items


def main():
    items = build_items()
    print(f"Bước click có gold + ảnh local: {len(items)}")
    pred = json.load(open(PRED, encoding="utf-8")) if os.path.exists(PRED) else {}
    key = get_key()
    if key == "ollama":
        print("⚠ Không thấy API key — dừng."); return
    n_call = 0
    for it in items:
        if it["rel"] in pred:
            continue
        im = Image.open(it["png"]).convert("RGB"); w, h = im.size
        sc = im.resize((MAXW, int(h * MAXW / w)), Image.LANCZOS) if w > MAXW else im
        buf = io.BytesIO(); sc.save(buf, "JPEG", quality=85)
        uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        msgs = [{"role": "user", "content": [
            {"type": "text", "text": PROMPT},
            {"type": "image_url", "image_url": {"url": uri}}]}]
        out = chat(BASE, MODEL, msgs, key, temperature=0)
        xy = parse_xy(out)
        pred[it["rel"]] = {"w": w, "h": h, "raw": out,
                           "px": xy[0] / 1000.0 * w if xy else None,
                           "py": xy[1] / 1000.0 * h if xy else None}
        n_call += 1
        json.dump(pred, open(PRED, "w", encoding="utf-8"), ensure_ascii=False)
        if n_call % 10 == 0:
            print(f"  ...{n_call} lượt gọi")
        time.sleep(5.0)
    print(f"Gọi API mới: {n_call} lượt")

    tols = [0.05, 0.10, 0.14]
    hit = {t: 0 for t in tols}
    scored, unparsed, dists = 0, 0, []
    for it in items:
        p = pred.get(it["rel"])
        if not p or p["px"] is None:
            unparsed += 1; continue
        w, h = p["w"], p["h"]
        dx = (p["px"] - it["gx"]) / w; dy = (p["py"] - it["gy"]) / h
        dists.append((dx * dx + dy * dy) ** 0.5); scored += 1
        for t in tols:
            if abs(p["px"] - it["gx"]) <= t * w and abs(p["py"] - it["gy"]) <= t * h:
                hit[t] += 1
    dists.sort()
    floor14 = hit[0.14] / max(scored, 1)
    print("\n" + "=" * 68)
    print(f"SÀN Exec(∅) — grounder KHÔNG có câu, chấm {scored} bước (bỏ {unparsed})")
    for t in tols:
        print(f"  sàn trúng ±{int(t*100)}%: {hit[t]}/{scored} = {hit[t]/max(scored,1):.1%}")
    print(f"  khoảng cách chuẩn hoá trung vị = {dists[len(dists)//2]:.3f}" if dists else "")
    print("-" * 68)
    ceil14 = 0.5131578947368421   # ground_pilot: Exec(CÓ câu gold) ±14%
    print(f"  Exec(CÓ câu gold) ±14% = {ceil14:.1%}   [ground_pilot]")
    print(f"  Exec(∅) sàn ±14%       = {floor14:.1%}   [file này]")
    print(f"  ==> DẢI ĐỘNG THẬT = {ceil14-floor14:+.1%}  (câu đóng góp thêm bấy nhiêu so đoán bừa)")
    print("=" * 68)
    json.dump({"n": scored, "unparsed": unparsed,
               "floor_hit_5": hit[0.05]/max(scored,1),
               "floor_hit_10": hit[0.10]/max(scored,1),
               "floor_hit_14": floor14,
               "ceil_hit_14_from_ground_pilot": ceil14,
               "dynamic_range_14": ceil14 - floor14,
               "median_dist": dists[len(dists)//2] if dists else None},
              open(os.path.join(HERE, "ground_floor_results.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("Đã lưu ground_floor_results.json")


if __name__ == "__main__":
    main()
