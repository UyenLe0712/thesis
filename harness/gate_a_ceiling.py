# -*- coding: utf-8 -*-
"""
FREE · offline — TRẦN CỦA THƯỚC, tính lại từ vết thô của cổng A.

Cổng A đo khoảng cách: bộ trỏ lệch bao nhiêu phần trăm bề ngang màn. Nhưng thước thật
không phải khoảng cách, mà là ô-Voronoi: trúng khi phần tử đích là phần tử GẦN điểm trỏ
NHẤT trên màn. Lệch 12% vẫn có thể nằm đúng ô nếu nút to; lệch 2% vẫn có thể sai ô nếu
nút chi chít. Nên "62,7% số bước dưới 3%" KHÔNG phải trần của thước.

Ở cổng A, câu đưa cho bộ trỏ là câu chuẩn do người viết — đầu vào hoàn hảo. Đem chính
các điểm trỏ đó chấm bằng `hit_voronoi` thì ra đúng câu hỏi cần: **nếu mô hình viết được
câu hoàn hảo thì thước cho tối đa bao nhiêu điểm.** Mọi con số S1/S2 về sau phải đọc trên
nền đó, chứ không đọc trên nền 100%.

Vì câu mô hình = câu chuẩn nên `action_ok` và `toggle_ok` đúng theo định nghĩa; điểm
executable rút gọn còn đúng phần định vị. Không gọi bộ trỏ lần nào — chỉ đọc lại vết đã
lưu, nên chạy bao nhiêu lần cũng miễn phí.

Chạy:  python harness/gate_a_ceiling.py [--raw ckpt/gate_A_raw.jsonl]
"""
import os, sys, json, argparse, statistics, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import metric_exec as M
import score_run as SR

TEST = os.path.join(HERE, "dg1_cache", "test_ac")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=os.path.join(os.path.dirname(HERE), "ckpt", "gate_A_raw.jsonl"))
    ap.add_argument("--out", default=os.path.join(os.path.dirname(HERE), "ckpt", "gate_A_ceiling.json"))
    a = ap.parse_args()

    idx = {}
    for l in open(os.path.join(TEST, "test.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        idx[(r["episode_id"], r["step_id"])] = r

    raw = [json.loads(l) for l in open(a.raw, encoding="utf-8")]
    units, n_nobtn = [], 0
    for x in raw:
        r = idx[(x["episode_id"], x["step_id"])]
        pred = tuple(x["pred_xy"]) if x.get("pred_xy") else None
        gold = tuple(x["gold_xy"]); wh = tuple(x["wh"])
        btns = SR.buttons_of(r)
        if not btns:
            n_nobtn += 1
        hv = M.hit_voronoi(pred, gold, btns, wh) if pred and btns else False
        hd = M.hit_disk(pred, gold, wh) if pred else False
        units.append({"episode_id": x["episode_id"], "app": r.get("app", ""),
                      "hv": int(hv), "hd": int(hd), "n_btn": len(btns),
                      "err": x.get("err_frac", 1.0)})

    key = lambda u: u["app"] or f"ep{u['episode_id']}"
    hv, ci_hv, G, geff = SR.cluster_bootstrap(units, key, lambda u: u["hv"])
    hd, ci_hd, _, _ = SR.cluster_bootstrap(units, key, lambda u: u["hd"])

    print("=" * 72)
    print(f"TRẦN CỦA THƯỚC — {len(units)} bước, câu đưa bộ trỏ là CÂU CHUẨN của người viết")
    print("=" * 72)
    print(f"  ô-Voronoi tâm (thước chính): {hv:6.1%}   KTC95 [{ci_hv[0]:.1%}, {ci_hv[1]:.1%}]")
    print(f"  đĩa dung sai  (báo kèm)    : {hd:6.1%}   KTC95 [{ci_hd[0]:.1%}, {ci_hd[1]:.1%}]")
    print(f"  cụm: {G} (hiệu dụng {geff:.1f})")
    nb = [u["n_btn"] for u in units]
    print(f"  phần tử mỗi màn: trung vị {statistics.median(nb):.0f}"
          f" · màn không có cây trợ năng: {n_nobtn}")

    print("-" * 72)
    print("  trần theo dải sai số của bộ trỏ:")
    bands = [(0, .03, "≤3%"), (.03, .05, "3-5%"), (.05, .08, "5-8%"),
             (.08, .14, "8-14%"), (.14, 9, ">14%")]
    for lo, hi, nm in bands:
        g = [u for u in units if lo <= u["err"] < hi]
        if g:
            print(f"    {nm:6} n={len(g):4}  Voronoi {sum(u['hv'] for u in g)/len(g):6.1%}"
                  f"   đĩa {sum(u['hd'] for u in g)/len(g):6.1%}")

    res = {"n": len(units), "ceiling_voronoi": hv, "ci_voronoi": list(ci_hv),
           "ceiling_disk": hd, "ci_disk": list(ci_hd), "G": G, "G_eff": geff,
           "median_buttons": statistics.median(nb), "screens_without_a11y": n_nobtn,
           "source_raw": a.raw}
    json.dump(res, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nĐã lưu {a.out}")


if __name__ == "__main__":
    main()
