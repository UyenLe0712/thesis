# -*- coding: utf-8 -*-
"""
FREE · offline — BƠM LỖI cho thước executability composite (metric_exec.py). BẢN 2.

Bản 1 (28/7 sáng) tuyên bố "đạt 9/10 ngưỡng độc lập". Một vòng phản biện chỉ ra phần lớn
nhánh của nó là **hằng đẳng thức**, tức không thể rớt:
  · nhánh "trỏ nút cạnh" chọn nút cạnh bằng chính hàm khử trùng của thước
  · nhánh "trỏ nút xa" đặt điểm TRÙNG tâm một hộp trong danh sách
  · nhánh "đảo nghĩa trong bảng" bơm bằng đúng tập con bảng của thước
  · ca ĐÚNG bơm lệch 1% cạnh, nhỏ hơn bán kính khử trùng, nên không thể rớt
Đó đúng là lỗi đã giết bộ bơm lỗi đời trước (report/90 mục 1), chỉ đổi vỏ.

Bản 2 sửa cách dựng ca:
  · ca lỗi toạ độ dựng bằng tiêu chí HÌNH HỌC độc lập (hộp bộ dò không chứa gold, khoảng
    cách nằm trong dải cho trước), KHÔNG gọi hàm nào của thước; báo tách theo dải khoảng cách
  · điểm bơm đặt lệch khỏi tâm đích, không đặt trùng
  · ca ĐÚNG bơm ở nhiều mức lệch, trong đó có mức lệch THẬT của bộ trỏ → báo cả đường cong
  · nhánh "đảo nghĩa trong bảng" gỡ khỏi tử số, đánh dấu là kiểm cơ học
  · thêm nhánh đo sai-dương của cổng thao tác trên 91 cặp (câu mô hình thật, câu gold)

Chạy: ~/.venvs/thesis/bin/python harness/exec_injection_validate.py
"""
import os, sys, re, json, glob, random, statistics as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metric_exec as ME
import omni_boxes as OB

HERE = os.path.dirname(os.path.abspath(__file__))
HF = os.path.expanduser("~/.cache/huggingface/hub/datasets--wangyuanlei--android_control_test/snapshots")
BOXDIR = os.path.join(HERE, "dg1_cache", "omni_box")
PRED = os.path.join(HERE, "dg1_cache", "ground_pilot", "pred.json")
GEN = os.path.join(HERE, "dg1_cache", "mde_pilot", "gen.json")
OUT = os.path.join(HERE, "exec_injection_results.json")
TOL = 0.14
random.seed(20260728)

# ───────────────── NGƯỠNG PRE-REGISTER (khoá trước khi chạy bản 2) ─────────────────
THRESHOLDS = {
    "fp_paraphrase_thuc_te": ("≤", 0.10),   # câu cùng nghĩa + điểm lệch bằng mức lệch THẬT
    "fp_action_gate":        ("≤", 0.15),   # cổng thao tác bác oan cặp (mô hình thật, gold)
    "fp_flip_rule":          ("≤", 0.05),   # luật đảo nghĩa kêu oan trên câu cùng nghĩa
    "det_nut_canh_gan":      ("≥", 0.80),   # trỏ nhầm sang phần tử cách gold 30-80px
    "det_nut_canh_xa":       ("≥", 0.90),   # trỏ nhầm sang phần tử cách gold 80-150px
    "det_nut_rat_xa":        ("≥", 0.95),   # trỏ nhầm sang phần tử cách gold hơn 25% cạnh
    "det_flip_heldout":      ("≥", 0.50),   # cặp đảo nghĩa giữ ngoài mọi bảng của thước
    "det_wrong_action":      ("≥", 0.80),   # câu đổi hẳn loại thao tác
    "det_wrong_content":     ("≥", 0.90),   # gõ sai nội dung
    "det_wrong_direction":   ("≥", 0.90),   # cuộn sai hướng
}
# nhánh chỉ để kiểm cơ học, KHÔNG tính vào tử số vì bơm bằng chính bảng của thước
MECHANICAL = {"det_flip_in_table"}

FLIP_IN_TABLE = [("on", "off"), ("enable", "disable"), ("show", "hide"),
                 ("expand", "collapse"), ("check", "uncheck"), ("mute", "unmute")]
# nhóm giữ riêng: cặp đặc thù giao diện, không bao giờ đưa vào bảng của thước
FLIP_HELDOUT = [("next", "previous"), ("subscribe", "unsubscribe"), ("follow", "unfollow"),
                ("allow", "block"), ("play", "pause"), ("bookmark", "unbookmark")]
VERB_SWAP = {"tap": "type into", "click": "type into", "press": "type into",
             "select": "scroll to", "choose": "scroll to", "open": "type into",
             "type": "tap", "enter": "tap", "scroll": "tap", "swipe": "tap"}
PARAPHRASE = [(r"^click on (the )?", "Tap the "), (r"^click (the )?", "Tap the "),
              (r"^tap on (the )?", "Tap the "), (r"^press (the )?", "Tap the "),
              (r"\bbutton\b", "control"), (r"\bicon\b", "symbol"), (r"\bat the\b", "located at the")]
DIRECTIONS = ["up", "down", "left", "right"]


def find_ep(eid):
    h = glob.glob(os.path.join(HF, "*", "test_output_json", "*", f"episode_{eid}.json"))
    return h[0] if h else None


def boxes_of(rel):
    p = os.path.join(BOXDIR, OB.key_of(rel))
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


def paraphrase(s):
    out = s
    for pat, rep in PARAPHRASE:
        out = re.sub(pat, rep, out, flags=re.I)
    return re.sub(r"\s+", " ", out).strip()


def flip(s, table):
    low = [w.lower() for w in re.findall(r"[A-Za-z]+", s)]
    for a, b in table:
        for src, dst in ((a, b), (b, a)):
            if src in low and dst not in low:
                return re.sub(rf"\b{src}\b", dst, s, count=1, flags=re.I)
    return None


def swap_verb(s):
    for w in re.findall(r"[A-Za-z]+", s):
        if w.lower() in VERB_SWAP:
            return re.sub(rf"\b{w}\b", VERB_SWAP[w.lower()], s, count=1, flags=re.I)
    return None


def d(p, q):
    return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5


def center(b):
    return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)


def load_items():
    pred = json.load(open(PRED, encoding="utf-8"))
    items = []
    for rel, p in pred.items():
        m = re.search(r"episode_(\d+)_screenshot_(\d+)\.png", rel)
        if not m:
            continue
        ep = find_ep(int(m.group(1)))
        if not ep:
            continue
        o = json.load(open(ep, encoding="utf-8"))
        acts, insts = o.get("actions") or [], o.get("step_instructions") or []
        si = int(m.group(2))
        if si >= len(acts) or si >= len(insts):
            continue
        a = acts[si]
        if a.get("action_type") not in ("click", "long_press") or "x" not in a:
            continue
        bs = boxes_of(rel)
        if not bs:
            continue
        items.append({"rel": rel, "instr": insts[si], "gold": (float(a["x"]), float(a["y"])),
                      "wh": (p["w"], p["h"]), "boxes": bs,
                      "pred": (p["px"], p["py"]) if p.get("px") is not None else None})
    return items


def judge(model_instr, gold_instr, pt, it):
    """Thước composite, chấm toạ độ bằng hộp của bộ dò."""
    action_ok = ME.canon_action(model_instr) == ME.canon_action(gold_instr)
    toggle_ok = not ME.toggle_conflict(model_instr, gold_instr)
    hv = ME.hit_nearest_box(pt, it["gold"], it["boxes"], it["wh"], TOL) if pt else False
    return bool(action_ok and toggle_ok and hv)


def real_offsets(items):
    """Phân phối sai số THẬT của bộ trỏ, lấy từ chính các ca nó trúng dung sai."""
    return [d(it["pred"], it["gold"]) for it in items
            if it["pred"] and ME.hit_disk(it["pred"], it["gold"], it["wh"], TOL)]


def run(items):
    res, examples = {}, {}

    def rec(key, ok, ex=None):
        r = res.setdefault(key, [0, 0])
        r[1] += 1
        if ok:
            r[0] += 1
        elif ex and key not in examples:
            examples[key] = ex

    offs = real_offsets(items)
    med_off = st.median(offs) if offs else 30.0
    print(f"Sai số THẬT của bộ trỏ (trong các ca trúng dung sai): trung vị {med_off:.0f}px "
          f"= {med_off/items[0]['wh'][0]:.1%} cạnh ngang, n={len(offs)}")

    # đường cong sai-dương theo mức lệch, thay cho một con số ở mức lệch tự chọn
    fp_curve = {}
    for frac in (0.01, 0.03, 0.05, 0.08, 0.13):
        bad = tot = 0
        for it in items:
            g, wh = it["gold"], it["wh"]
            off = frac * wh[0] * 0.7
            pt = (g[0] + off, g[1] + off)
            tot += 1
            if not judge(paraphrase(it["instr"]), it["instr"], pt, it):
                bad += 1
        fp_curve[frac] = bad / max(tot, 1)

    for it in items:
        g, wh, bs = it["gold"], it["wh"], it["boxes"]
        sx = 1 if random.random() < 0.5 else -1
        sy = 1 if random.random() < 0.5 else -1
        real_ok = (g[0] + sx * med_off * 0.7, g[1] + sy * med_off * 0.7)
        pp = paraphrase(it["instr"])
        rec("fp_paraphrase_thuc_te", not judge(pp, it["instr"], real_ok, it),
            {"gold": it["instr"], "para": pp})
        rec("fp_flip_rule", ME.toggle_conflict(pp, it["instr"]))

        # ── lỗi toạ độ: chọn phần tử đích bằng tiêu chí HÌNH HỌC, không dùng hàm của thước
        others = [b for b in bs if not (b[0] <= g[0] <= b[2] and b[1] <= g[1] <= b[3])]
        for key, lo, hi in (("det_nut_canh_gan", 30, 80),
                            ("det_nut_canh_xa", 80, 150),
                            ("det_nut_rat_xa", 0.25 * wh[0], 10 ** 9)):
            cand = [b for b in others if lo <= d(center(b), g) < hi]
            if not cand:
                continue
            tgt = center(min(cand, key=lambda b: d(center(b), g)))
            # đặt điểm lệch khỏi tâm đích 20% quãng đường về phía gold, để không trùng tâm
            pt = (tgt[0] + 0.2 * (g[0] - tgt[0]), tgt[1] + 0.2 * (g[1] - tgt[1]))
            rec(key, not judge(it["instr"], it["instr"], pt, it),
                {"gold_xy": g, "target": tgt, "pred": pt})

        sv = swap_verb(it["instr"])
        if sv:
            rec("det_wrong_action", not judge(sv, it["instr"], real_ok, it),
                {"gold": it["instr"], "swap": sv})

    # ── nhánh ngôn ngữ: đo trên toàn bộ câu gold trong cache
    for path in glob.glob(os.path.join(HF, "*", "test_output_json", "*", "episode_*.json"))[:400]:
        try:
            o = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        acts, insts = o.get("actions") or [], o.get("step_instructions") or []
        for i, a in enumerate(acts):
            if i >= len(insts):
                break
            t, instr = a.get("action_type"), insts[i]
            for key, table in (("det_flip_in_table", FLIP_IN_TABLE),
                               ("det_flip_heldout", FLIP_HELDOUT)):
                f = flip(instr, table)
                if f:
                    rec(key, ME.toggle_conflict(f, instr), {"gold": instr, "flip": f})
            if t == "input_text" and a.get("text"):
                gt = str(a["text"])
                bad = "zzq" + gt[::-1][:6]
                rec("det_wrong_content",
                    not ME.content_match(instr.replace(gt, bad) if gt in instr else instr + " " + bad, gt))
            elif t == "scroll" and a.get("direction") in DIRECTIONS:
                gd = a["direction"]
                bd = {"up": "down", "down": "up", "left": "right", "right": "left"}[gd]
                rec("det_wrong_direction", not ME.direction_match(f"Scroll {bd} on the screen", gd))

    # ── sai-dương của cổng thao tác, trên cặp (câu mô hình THẬT, câu gold)
    gen = json.load(open(GEN, encoding="utf-8"))
    for rel, model_sent in gen.items():
        m = re.search(r"episode_(\d+)_screenshot_(\d+)\.png", rel)
        if not m:
            continue
        ep = find_ep(int(m.group(1)))
        if not ep:
            continue
        o = json.load(open(ep, encoding="utf-8"))
        insts = o.get("step_instructions") or []
        si = int(m.group(2))
        if si >= len(insts):
            continue
        rec("fp_action_gate", ME.canon_action(model_sent) != ME.canon_action(insts[si]),
            {"model": model_sent, "gold": insts[si]})
    return res, examples, fp_curve, med_off


def report(res, examples, fp_curve, med_off, items):
    print("\n" + "=" * 82)
    print("BƠM LỖI BẢN 2 — chỉ tính điểm cho các nhánh CÓ THỂ RỚT")
    print("=" * 82)
    rows, npass, ncount = [], 0, 0
    for k, (hit, n) in res.items():
        if n == 0:
            continue
        rate = hit / n
        if k in MECHANICAL:
            rows.append({"metric": k, "rate": rate, "n": n, "mechanical": True})
            print(f"  {k:24}{rate:7.1%}  (n={n:4})   [kiểm cơ học, không tính điểm]")
            continue
        op, thr = THRESHOLDS[k]
        ok = rate <= thr if op == "≤" else rate >= thr
        npass += ok
        ncount += 1
        rows.append({"metric": k, "rate": rate, "n": n, "op": op, "threshold": thr, "pass": bool(ok)})
        print(f"  {k:24}{rate:7.1%}  (n={n:4})   ngưỡng {op}{thr:.0%}   {'đạt' if ok else '**RỚT**'}")
    print("-" * 82)
    print(f"  Đạt {npass}/{ncount} ngưỡng")
    print("\n  Kết oan theo mức lệch của điểm trỏ (câu cùng nghĩa, đáng lẽ đậu hết):")
    W = items[0]["wh"][0]
    for f, v in sorted(fp_curve.items()):
        mark = "   ← quanh mức lệch THẬT" if abs(f * W * 0.7 - med_off * 0.7) < 25 else ""
        print(f"     lệch {f:.0%} cạnh ({f*W*0.7:.0f}px): kết oan {v:.1%}{mark}")
    for k, ex in examples.items():
        if k in THRESHOLDS:
            op, thr = THRESHOLDS[k]
            r = res[k][0] / max(res[k][1], 1)
            if not (r <= thr if op == "≤" else r >= thr):
                print(f"  ví dụ [{k}]: {json.dumps(ex, ensure_ascii=False)[:140]}")
    return rows, npass, ncount


if __name__ == "__main__":
    items = load_items()
    print(f"Bộ ca: {len(items)} bước chạm có toạ độ gold + hộp bộ dò\n")
    res, ex, curve, med = run(items)
    rows, npass, ncount = report(res, ex, curve, med, items)
    json.dump({"n_items": len(items), "median_real_offset_px": med,
               "fp_curve": {str(k): v for k, v in curve.items()},
               "passed": npass, "counted": ncount, "rows": rows},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nĐã lưu", OUT)
