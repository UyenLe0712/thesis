# -*- coding: utf-8 -*-
"""Thước đồng-báo theo Phụ lục D.3 của AndroidControl — tính lại từ tệp thô, 0 giây GPU.

    python3 harness/luat_d3.py            # in bảng + ghi runs/luat_d3.json

Luật (Li et al., NeurIPS 2024 D&B, App. D.3): điểm bộ trỏ nằm TRONG hộp phần tử vàng. Hộp lấy
từ `descriptors.jsonl` trường `box` (pixel, cùng lưới với `pred_xy`) — ⚠️ hộp do dự án suy
bằng quy tắc nút nhỏ nhất chứa điểm chạm (`descriptor_label_build.py:334`), KHÔNG phải nhãn
gốc; ~48% hộp là nút con không nhận chạm ⇒ chặt hơn nhãn gốc. Xem `report/139`.

Bốn biến thể, cùng giữ action_ok ∧ toggle_ok:
  d3        trong hộp
  d3_gate   trong hộp ∧ cửa sổ ±14% (hit_disk)            ← con số nên dùng khi bảo vệ
  d3_nocont trong hộp, hộp ≥25% diện tích màn tính TRƯỢT
  vor       Voronoi .14 (headline, chép từ `executable`)
Bước thiếu `box` tính TRƯỢT ở mọi biến thể D.3 (bảo thủ).
"""
import os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
RUNS = os.path.join(ROOT, "runs")
DESC = os.path.join(HERE, "dg1_cache", "test_ac", "descriptors.jsonl")
NHANH = [("Câu người (trần)", "score_ceiling_human_raw.jsonl"),
         ("MIN-DESC/101", "score_min_desc_seed101_raw.jsonl"),
         ("CE2-S2/101", "score_ce2_s2_seed101_raw.jsonl"),
         ("S1/202", "score_s1_seed202_raw.jsonl"),
         ("S1/101", "score_s1_seed101_raw.jsonl"),
         ("S2/101", "score_s2_seed101_raw.jsonl"),
         ("gui_sel/101", "sel/score_gui_sel_seed101_raw.jsonl"),
         ("Base", "score_base_raw.jsonl")]
SAN = [("f1 câu rỗng nghĩa", "floor/score_f1_trong_raw.jsonl"),
       ("f2 bỏ tên giữ vị trí", "floor/score_f2_khongten_raw.jsonl"),
       ("f3 đúng văn phong sai màn", "floor/score_f3_lechman_raw.jsonl")]
kh = lambda r: (str(r["episode_id"]), str(r["step_id"]))


def nap(p):
    out = {}
    for l in open(p, encoding="utf-8"):
        r = json.loads(l)
        for k in ("executable", "action_ok", "toggle_ok", "hit_disk"):
            r.setdefault(k, 0)
        out[kh(r)] = r
    return out


D = {kh(d): d for d in map(json.loads, open(DESC, encoding="utf-8"))}


def luat(r, k):
    d = D.get(k)
    vor = int(r["executable"])
    if not d or not d.get("box") or not r.get("pred_xy"):
        return dict(vor=vor, d3=0, d3_gate=0, d3_nocont=0)
    x1, y1, x2, y2 = d["box"]; x, y = r["pred_xy"]
    inb = x1 <= x <= x2 and y1 <= y <= y2
    ok = int(r["action_ok"] and r["toggle_ok"] and inb)
    return dict(vor=vor, d3=ok, d3_gate=int(ok and r["hit_disk"]),
                d3_nocont=int(ok and d["area_share"] < 0.25))


def bang(ten_tep, keys=None):
    R = nap(os.path.join(RUNS, ten_tep))
    K = sorted(keys) if keys else sorted(R)
    K = [k for k in K if k in R]
    acc = {c: 0 for c in ("vor", "d3", "d3_gate", "d3_nocont")}
    for k in K:
        for c, v in luat(R[k], k).items():
            acc[c] += v
    return {c: 100 * v / len(K) for c, v in acc.items()}, len(K)


def main():
    out = {"n4463": {}, "lat800": {}}
    print(f"{'nhánh':26s} {'n':>5s} {'Voronoi':>8s} {'D.3':>7s} {'D.3∧14%':>8s} {'D.3 -cont':>9s}")
    for ten, tep in NHANH:
        if not os.path.exists(os.path.join(RUNS, tep)):
            print(f"{ten:26s}  (thiếu {tep})"); continue
        v, n = bang(tep); out["n4463"][ten] = v
        print(f"{ten:26s} {n:5d} {v['vor']:8.2f} {v['d3']:7.2f} {v['d3_gate']:8.2f} {v['d3_nocont']:9.2f}")

    # sàn: cùng lát 800 của bộ sàn, trần đo trên cùng khoá
    f1 = nap(os.path.join(RUNS, SAN[0][1])); K800 = sorted(f1)
    print(f"\nLát 800 của bộ sàn (n={len(K800)}):")
    print(f"{'':26s} {'n':>5s} {'Voronoi':>8s} {'D.3':>7s} {'D.3∧14%':>8s} {'D.3 -cont':>9s}")
    v, n = bang(NHANH[0][1], K800); out["lat800"]["trần"] = v
    print(f"{'trần (câu người)':26s} {n:5d} {v['vor']:8.2f} {v['d3']:7.2f} {v['d3_gate']:8.2f} {v['d3_nocont']:9.2f}")
    for ten, tep in SAN:
        v, n = bang(tep, K800); out["lat800"][ten] = v
        print(f"{ten:26s} {n:5d} {v['vor']:8.2f} {v['d3']:7.2f} {v['d3_gate']:8.2f} {v['d3_nocont']:9.2f}")
    tr, s1 = out["lat800"]["trần"], out["lat800"]["f1 câu rỗng nghĩa"]
    print("dải dùng được (trần − f1): " + " · ".join(f"{c} {tr[c]-s1[c]:.2f}" for c in tr))

    p = os.path.join(RUNS, "luat_d3.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", p)


if __name__ == "__main__":
    main()
