# -*- coding: utf-8 -*-
"""
Bơm lỗi — BẢN 3, chạy bằng ĐÚNG DỤNG CỤ SẼ CHẤM LUẬN VĂN.

Vì sao phải có bản 3. Vòng rà 6/8 phát hiện bản 2 (`exec_injection_validate.py`) chấm
toạ độ bằng `hit_nearest_box` trên **hộp OmniParser** (trung vị 24 hộp mỗi màn), trong
khi đường chấm thật (`score_run.py` → `metric_exec.score_step`) dùng `hit_voronoi` trên
**tâm phần tử cây trợ năng** (trung vị 71 phần tử mỗi màn). Con số "8/10" vì vậy nói về
một cấu hình KHÔNG tồn tại trong luận văn. Bản 3 sửa đúng chỗ đó:

  · nguồn ca kiểm : test.jsonl (tập kiểm thật) thay cho lát 76 màn cũ
  · danh sách nút : cây trợ năng, qua đúng hàm `score_run.buttons_of`
  · hàm chấm      : `metric_exec.score_step` — chính hàm sẽ chấm

Giữ NGUYÊN mười tiêu chí và mười ngưỡng đã khoá của bản 2. Ngưỡng không được sửa theo
kết quả; con số ra sao khai vậy, kể cả khi xấu hơn 8/10.

Chạy:  ~/.venvs/thesis/bin/python harness/exec_injection_v3.py --n 400
"""
import os, sys, json, re, random, argparse, statistics as st, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import metric_exec as ME
import score_run as SR

TEST = os.path.join(HERE, "dg1_cache", "test_ac")
SEED = 20260805
TOL = 0.14

# ── ngưỡng: BÊ NGUYÊN từ bản 2, không sửa ────────────────────────────────────
THRESHOLDS = {
    "fp_paraphrase_thuc_te": ("≤", 0.10),
    "fp_action_gate":        ("≤", 0.15),
    "fp_flip_rule":          ("≤", 0.05),
    "det_nut_canh_gan":      ("≥", 0.80),
    "det_nut_canh_xa":       ("≥", 0.90),
    "det_nut_rat_xa":        ("≥", 0.95),
    "det_flip_heldout":      ("≥", 0.50),
    "det_wrong_action":      ("≥", 0.80),
    "det_wrong_content":     ("≥", 0.90),
    "det_wrong_direction":   ("≥", 0.90),
}
FLIP_HELDOUT = {"enable": "disable", "expand": "collapse", "mute": "unmute",
                "follow": "unfollow", "subscribe": "unsubscribe", "lock": "unlock"}
VERB_SWAP = {"tap": "scroll", "click": "scroll", "select": "type", "open": "scroll",
             "scroll": "tap", "type": "tap", "enter": "tap"}


def paraphrase(s):
    """Câu CÙNG NGHĨA viết khác đi — thước không được bác."""
    t = s.strip()
    for a, b in (("Click on ", "Tap "), ("Tap on ", "Tap "), ("click on ", "tap "),
                 ("Select ", "Tap "), ("Press ", "Tap ")):
        if t.startswith(a):
            t = b + t[len(a):]
            break
    t = re.sub(r"\bthe\b ", "", t, count=1)
    return t if t != s.strip() else "Please " + t[0].lower() + t[1:]


def swap_verb(s):
    """Đổi hẳn LOẠI thao tác — thước phải bắt."""
    m = re.match(r"\s*(\w+)", s)
    if not m:
        return None
    v = m.group(1).lower()
    if v not in VERB_SWAP:
        return None
    return re.sub(r"^\s*\w+", VERB_SWAP[v].capitalize(), s, count=1)


def flip(s, table):
    low = s.lower()
    for a, b in table.items():
        if re.search(rf"\b{a}\b", low):
            return re.sub(rf"\b{a}\b", b, low)
    return None


def d(p, q):
    return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5


def judge(model_instr, gold_instr, pt, it):
    """ĐÚNG hàm chấm của đường thật — khác bản 2 chính ở dòng này."""
    r = ME.score_step(model_instr, gold_instr, pt, it["gold"], it["buttons"], it["wh"], TOL)
    return bool(r["executable"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--out", default=os.path.join(HERE, "exec_injection_v3_results.json"))
    a = ap.parse_args()
    rnd = random.Random(SEED)

    recs = [json.loads(l) for l in open(os.path.join(TEST, "test.jsonl"), encoding="utf-8")]
    taps = [r for r in recs if r["action"].get("action_type") in ("click", "long_press")
            and "x" in r["action"]]
    smp = random.Random(SEED).sample(taps, min(a.n, len(taps)))

    items = []
    for r in smp:
        b = SR.buttons_of(r)
        if not b:
            continue
        items.append({"instr": r["gold_instruction"],
                      "gold": (float(r["action"]["x"]), float(r["action"]["y"])),
                      "wh": (1080, 2400), "buttons": b})
    print(f"Ca kiểm: {len(items)} bước chạm của TẬP KIỂM · trung vị "
          f"{st.median([len(i['buttons']) for i in items]):.0f} phần tử mỗi màn")

    res = collections.defaultdict(lambda: [0, 0])
    ex = {}

    def rec(key, ok, sample=None):
        res[key][1] += 1
        if ok:
            res[key][0] += 1
        elif sample and key not in ex:
            ex[key] = sample

    # đường cong kết oan theo mức lệch của bộ trỏ — đo lại bằng dụng cụ thật
    fp_curve = {}
    for frac in (0.01, 0.03, 0.05, 0.08, 0.13):
        bad = tot = 0
        for it in items:
            g = it["gold"]
            off = frac * it["wh"][0] * 0.7
            pt = (g[0] + off, g[1] + off)
            tot += 1
            if not judge(paraphrase(it["instr"]), it["instr"], pt, it):
                bad += 1
        fp_curve[frac] = bad / max(tot, 1)

    med_off = 0.03 * 1080          # giả định bộ trỏ đạt cổng A; ghi rõ là giả định
    for it in items:
        g, wh = it["gold"], it["wh"]
        sx = 1 if rnd.random() < 0.5 else -1
        sy = 1 if rnd.random() < 0.5 else -1
        real_ok = (g[0] + sx * med_off * 0.7, g[1] + sy * med_off * 0.7)
        pp = paraphrase(it["instr"])
        rec("fp_paraphrase_thuc_te", not judge(pp, it["instr"], real_ok, it),
            {"gold": it["instr"], "para": pp})
        rec("fp_flip_rule", ME.toggle_conflict(pp, it["instr"]))

        # lỗi toạ độ: chọn phần tử đích bằng tiêu chí HÌNH HỌC, không dùng hàm của thước
        others = [p for p in it["buttons"] if d(p, g) > 20]
        for key, lo, hi in (("det_nut_canh_gan", 30, 80),
                            ("det_nut_canh_xa", 80, 150),
                            ("det_nut_rat_xa", 0.25 * wh[0], 10 ** 9)):
            cand = [p for p in others if lo <= d(p, g) < hi]
            if not cand:
                continue
            tgt = min(cand, key=lambda p: d(p, g))
            pt = (tgt[0] + 0.2 * (g[0] - tgt[0]), tgt[1] + 0.2 * (g[1] - tgt[1]))
            rec(key, not judge(it["instr"], it["instr"], pt, it),
                {"gold_xy": g, "target": tgt, "pred": pt})

        sv = swap_verb(it["instr"])
        if sv:
            rec("det_wrong_action", not judge(sv, it["instr"], real_ok, it),
                {"gold": it["instr"], "swap": sv})

    # nhánh ngôn ngữ: chạy trên toàn bộ câu chuẩn của tập kiểm
    for r in recs:
        instr, act = r["gold_instruction"], r["action"]
        f = flip(instr, FLIP_HELDOUT)
        if f:
            rec("det_flip_heldout", ME.toggle_conflict(f, instr), {"gold": instr, "flip": f})
        t = act.get("action_type")
        if t == "input_text" and act.get("text"):
            gt = str(act["text"])
            bad = "zzq" + gt[::-1][:6]
            rec("det_wrong_content",
                not ME.content_match(instr.replace(gt, bad) if gt in instr else instr + " " + bad, gt))
        elif t == "scroll" and act.get("direction"):
            gd = act["direction"]
            bd = {"up": "down", "down": "up", "left": "right", "right": "left"}.get(gd)
            if bd:
                rec("det_wrong_direction", not ME.direction_match(f"Scroll {bd} on the screen", gd))

    # cổng thao tác: sai-dương trên cặp (câu chuẩn viết khác đi, câu chuẩn)
    for it in items:
        rec("fp_action_gate", ME.canon_action(paraphrase(it["instr"])) != ME.canon_action(it["instr"]),
            {"gold": it["instr"]})

    print("=" * 78)
    print("BƠM LỖI BẢN 3 — chấm bằng cây trợ năng + hit_voronoi (đúng đường chấm thật)")
    print("=" * 78)
    dat, tot_c = 0, 0
    out = {}
    for k, (op, thr) in THRESHOLDS.items():
        if k not in res:
            print(f"  {k:24} — không có ca nào")
            continue
        hit, n = res[k]
        rate = hit / n
        ok = (rate <= thr) if op == "≤" else (rate >= thr)
        dat += ok; tot_c += 1
        out[k] = {"rate": rate, "n": n, "thr": thr, "op": op, "pass": ok}
        print(f"  {'✔' if ok else '✘'} {k:24} {rate:6.1%}  (ngưỡng {op}{thr:.0%}, n={n})")
    print("-" * 78)
    print(f"  ĐẠT {dat}/{tot_c}    (bản 2 trên dụng cụ khác: 8/10)")
    print("\n  Đường cong kết oan theo sai số bộ trỏ (dụng cụ thật):")
    for f, v in fp_curve.items():
        print(f"    lệch {f:.0%} → kết oan {v:5.1%}")
    json.dump({"passed": dat, "total": tot_c, "criteria": out, "fp_curve": fp_curve,
               "n_items": len(items), "instrument": "a11y_centers + hit_voronoi"},
              open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nĐã lưu {a.out}")


if __name__ == "__main__":
    main()
