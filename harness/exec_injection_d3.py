# -*- coding: utf-8 -*-
"""
Bơm lỗi — BẢN D.3 (SOICT camera-ready, phản biện R2): chạy lại bộ kiểm bằng ĐÚNG luật chấm chính của bài.

Bản 3 (`exec_injection_v3.py`) phán vị trí bằng Voronoi, còn điểm chính của bài dùng D.3
(điểm nằm trong hộp phần tử vàng). Bản này giữ NGUYÊN mẫu (cùng hạt giống 20260805, n=400),
NGUYÊN mười tiêu chí và mười ngưỡng, chỉ đổi hàm phán vị trí:

  judge = action_ok ∧ toggle_ok ∧ (điểm dự đoán nằm trong `box` của phần tử vàng)

`box` lấy từ descriptors.jsonl, cùng nguồn `luat_d3.py`. Bước không có hộp bị loại khỏi ca kiểm
(luật chấm tính chúng là trượt, nên không dùng được làm ca "đúng").

Cách mô phỏng "điểm rơi vào phần tử lân cận" dưới D.3:
  · giữ cách chọn phần tử lân cận của bản 3 (khoảng cách tâm tới điểm chạm vàng: 30–80, 80–150,
    ≥ 25% bề ngang) và cách dịch 20% về phía điểm chạm vàng ⇒ phép dựng hình học y hệt;
  · điểm giả lập đặt trên đường nối TÂM phần tử lân cận → điểm chạm vàng, nên có thể rơi vào hộp
    vàng khi hai hộp lồng nhau hoặc chồng nhau; đó là hành vi thật của D.3, ghi vào kết quả.
  · biến thể độ nhạy `_khong_dich`: đặt đúng tại tâm phần tử lân cận.

Chạy:  ~/.venvs/thesis/bin/python harness/exec_injection_d3.py --n 400
"""
import os, sys, json, random, argparse, statistics as st, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import metric_exec as ME
import score_run as SR
import a11y_inventory as A11Y
import exec_injection_v3 as V3

TEST = V3.TEST
SEED = V3.SEED


def centres_of(rec):
    """Tâm mọi phần tử hiển thị — cùng bộ lọc với `score_run.buttons_of`."""
    pts = SR.buttons_of(rec)
    return pts


def judge_d3(model_instr, gold_instr, pt, it):
    r = ME.score_step(model_instr, gold_instr, pt, it["gold"], it["buttons"], it["wh"], V3.TOL)
    x1, y1, x2, y2 = it["box"]
    return bool(r["action_ok"] and r["toggle_ok"] and x1 <= pt[0] <= x2 and y1 <= pt[1] <= y2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--out", default=os.path.join(HERE, "exec_injection_d3_results.json"))
    a = ap.parse_args()
    rnd = random.Random(SEED)
    d = V3.d

    desc = {(str(x["episode_id"]), str(x["step_id"])): x
            for x in map(json.loads, open(os.path.join(TEST, "descriptors.jsonl"), encoding="utf-8"))}
    recs = [json.loads(l) for l in open(os.path.join(TEST, "test.jsonl"), encoding="utf-8")]
    taps = [r for r in recs if r["action"].get("action_type") in ("click", "long_press")
            and "x" in r["action"]]
    smp = random.Random(SEED).sample(taps, min(a.n, len(taps)))     # cùng mẫu với bản 3

    items, bo_qua = [], 0
    for r in smp:
        b = centres_of(r)
        bx = (desc.get((str(r["episode_id"]), str(r["step_id"]))) or {}).get("box")
        if not b or not bx:
            bo_qua += 1
            continue
        items.append({"instr": r["gold_instruction"],
                      "gold": (float(r["action"]["x"]), float(r["action"]["y"])),
                      "wh": (1080, 2400), "buttons": b, "box": bx})
    print(f"Ca kiểm: {len(items)} bước chạm của TẬP KIỂM (bỏ {bo_qua} bước thiếu hộp hoặc thiếu cây) · "
          f"trung vị {st.median([len(i['buttons']) for i in items]):.0f} phần tử mỗi màn")

    res = collections.defaultdict(lambda: [0, 0])

    def rec(key, ok):
        res[key][1] += 1
        res[key][0] += bool(ok)

    fp_curve = {}
    for frac in (0.01, 0.03, 0.05, 0.08, 0.13):
        bad = 0
        for it in items:
            g = it["gold"]
            off = frac * it["wh"][0] * 0.7
            bad += not judge_d3(V3.paraphrase(it["instr"]), it["instr"], (g[0] + off, g[1] + off), it)
        fp_curve[frac] = bad / max(len(items), 1)

    med_off = 0.03 * 1080
    for it in items:
        g, wh = it["gold"], it["wh"]
        sx = 1 if rnd.random() < 0.5 else -1
        sy = 1 if rnd.random() < 0.5 else -1
        real_ok = (g[0] + sx * med_off * 0.7, g[1] + sy * med_off * 0.7)
        pp = V3.paraphrase(it["instr"])
        rec("fp_paraphrase_thuc_te", not judge_d3(pp, it["instr"], real_ok, it))
        rec("fp_flip_rule", ME.toggle_conflict(pp, it["instr"]))

        others = [p for p in it["buttons"] if d(p, g) > 20]
        for key, lo, hi in (("det_nut_canh_gan", 30, 80), ("det_nut_canh_xa", 80, 150),
                            ("det_nut_rat_xa", 0.25 * wh[0], 10 ** 9)):
            cand = [p for p in others if lo <= d(p, g) < hi]
            if not cand:
                continue
            tgt = min(cand, key=lambda p: d(p, g))
            pt = (tgt[0] + 0.2 * (g[0] - tgt[0]), tgt[1] + 0.2 * (g[1] - tgt[1]))
            rec(key, not judge_d3(it["instr"], it["instr"], pt, it))
            rec(key + "_khong_dich", not judge_d3(it["instr"], it["instr"], tgt, it))

        sv = V3.swap_verb(it["instr"])
        if sv:
            rec("det_wrong_action", not judge_d3(sv, it["instr"], real_ok, it))

    for r in recs:
        instr, act = r["gold_instruction"], r["action"]
        f = V3.flip(instr, V3.FLIP_HELDOUT)
        if f:
            rec("det_flip_heldout", ME.toggle_conflict(f, instr))
        t = act.get("action_type")
        if t == "input_text" and act.get("text"):
            gt = str(act["text"]); bad = "zzq" + gt[::-1][:6]
            rec("det_wrong_content",
                not ME.content_match(instr.replace(gt, bad) if gt in instr else instr + " " + bad, gt))
        elif t == "scroll" and act.get("direction"):
            gd = act["direction"]
            bd = {"up": "down", "down": "up", "left": "right", "right": "left"}.get(gd)
            if bd:
                rec("det_wrong_direction", not ME.direction_match(f"Scroll {bd} on the screen", gd))

    for it in items:
        rec("fp_action_gate", ME.canon_action(V3.paraphrase(it["instr"])) != ME.canon_action(it["instr"]))

    print("=" * 78)
    print("BƠM LỖI DƯỚI D.3 — action_ok ∧ toggle_ok ∧ điểm trong hộp vàng")
    print("=" * 78)
    dat, tot_c, out = 0, 0, {}
    for k, (op, thr) in V3.THRESHOLDS.items():
        if k not in res:
            print(f"  {k:24} — không có ca nào"); continue
        hit, n = res[k]
        rate = hit / n
        ok = (rate <= thr) if op == "≤" else (rate >= thr)
        dat += ok; tot_c += 1
        out[k] = {"rate": rate, "n": n, "thr": thr, "op": op, "pass": ok}
        print(f"  {'✔' if ok else '✘'} {k:24} {rate:6.1%}  (ngưỡng {op}{thr:.0%}, n={n})")
    print("-" * 78)
    print(f"  ĐẠT {dat}/{tot_c}")
    for k in ("det_nut_canh_gan", "det_nut_canh_xa", "det_nut_rat_xa"):
        h, n = res[k + "_khong_dich"]
        print(f"  (độ nhạy, không dịch 20%) {k}: {h/n:6.1%} (n={n})")
        out[k + "_khong_dich"] = {"rate": h / n, "n": n}
    print("\n  Đường cong kết oan theo sai số bộ trỏ (D.3):")
    for f, v in fp_curve.items():
        print(f"    lệch {f:.0%} → kết oan {v:5.1%}")
    json.dump({"passed": dat, "total": tot_c, "criteria": out, "fp_curve": fp_curve,
               "n_items": len(items), "bo_qua": bo_qua, "instrument": "a11y + D.3 (hộp vàng)"},
              open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nĐã lưu {a.out}")


if __name__ == "__main__":
    main()
