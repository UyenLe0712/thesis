# -*- coding: utf-8 -*-
"""Thước đồng-báo theo Phụ lục D.3 của AndroidControl — tính lại từ tệp thô, 0 giây GPU.

    python3 harness/luat_d3.py            # in bảng + ghi runs/luat_d3.json

Luật (Li et al., NeurIPS 2024 D&B, App. D.3): điểm bộ trỏ nằm TRONG hộp phần tử vàng. Hộp lấy
từ `descriptors.jsonl` trường `box` (pixel, cùng lưới với `pred_xy`) — ⚠️ hộp do dự án suy
bằng quy tắc nút nhỏ nhất chứa điểm chạm (`descriptor_label_build.py:334`), KHÔNG phải nhãn
gốc; ~48% hộp là nút con không nhận chạm ⇒ chặt hơn nhãn gốc. Xem `report/139`.

Bốn biến thể D.3, cùng giữ action_ok ∧ toggle_ok:
  d3        trong hộp
  d3_gate   trong hộp ∧ cửa sổ ±14% (hit_disk)            ← con số nên dùng khi bảo vệ
  d3_nocont trong hộp, hộp ≥25% diện tích màn tính TRƯỢT
  vor       Voronoi .14 (headline, chép từ `executable`)
Bước thiếu `box` tính TRƯỢT ở mọi biến thể D.3 (bảo thủ).

Ba luật ĐỘ NHẠY của `151` mục 6, thêm 9/9 vì trước đó KHÔNG có nguồn tái lập nào trong kho:
  d14_truc  |dx| ≤ .14·W ∧ |dy| ≤ .14·H, gated       GRPO 69,37
  aitw      √((dx/W)² + (dy/H)²) ≤ .14, gated        GRPO 68,90
  disk_thuan  trường `hit_disk` sẵn có, KHÔNG gated   GRPO 69,89

⛔⛔ BA CÁI TÊN, HAI LUẬT — chỗ này đã suýt đọc nhầm:
  · `151` gọi luật `aitw`, `report/136` gọi đúng luật ấy là **nL2 .14**. Một luật, hai tên.
  · `rule_sensitivity.py:37` có `disk_l2` = ‖p−g‖ ≤ .14·W — **LUẬT KHÁC**, chuẩn hoá một trục,
    cho GRPO 66,05 chứ không phải 68,90. Đừng lấy nó thay cho `aitw`.
  · `d14_truc` gated và `disk_thuan` chỉ khác nhau ở chỗ có nhân action_ok ∧ toggle_ok hay không
    (69,37 so 69,89) — chính là bẫy tên trường `exec_disk` đã ghi ở CLAUDE.md.
"""
import os, json, glob, math
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
RUNS = os.path.join(ROOT, "runs")
DESC = os.path.join(HERE, "dg1_cache", "test_ac", "descriptors.jsonl")
NHANH = [("Câu người (trần)", "score_ceiling_human_raw.jsonl"),
         ("GRPO-point/101", "grpo_point/score_grpo_point_seed101_raw.jsonl"),
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
COT = ("vor", "d3", "d3_gate", "d3_nocont", "d14_truc", "aitw", "disk_thuan")
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


def do_nhay(r):
    """Ba luật ĐỘ NHẠY — tính THẲNG từ toạ độ thô, không phụ thuộc descriptors."""
    g = int(r["action_ok"] and r["toggle_ok"])
    out = dict(d14_truc=0, aitw=0, disk_thuan=int(r.get("hit_disk", 0)))
    if not r.get("pred_xy"):
        return out
    (x, y), (gx, gy), (w, h) = r["pred_xy"], r["gold_xy"], r["wh"]
    out["d14_truc"] = int(g and abs(x - gx) <= .14 * w and abs(y - gy) <= .14 * h)
    out["aitw"] = int(g and math.hypot((x - gx) / w, (y - gy) / h) <= .14)
    return out


def luat(r, k):
    d = D.get(k)
    v = dict(vor=int(r["executable"]), **do_nhay(r))
    if not d or not d.get("box") or not r.get("pred_xy"):
        return dict(v, d3=0, d3_gate=0, d3_nocont=0)
    x1, y1, x2, y2 = d["box"]; x, y = r["pred_xy"]
    inb = x1 <= x <= x2 and y1 <= y <= y2
    ok = int(r["action_ok"] and r["toggle_ok"] and inb)
    return dict(v, d3=ok, d3_gate=int(ok and r["hit_disk"]),
                d3_nocont=int(ok and d["area_share"] < 0.25))


def bang(ten_tep, keys=None):
    R = nap(os.path.join(RUNS, ten_tep))
    K = sorted(keys) if keys else sorted(R)
    K = [k for k in K if k in R]
    acc = {c: 0 for c in COT}
    for k in K:
        for c, v in luat(R[k], k).items():
            acc[c] += v
    return {c: 100 * v / len(K) for c, v in acc.items()}, len(K)


# Số đã niêm ở `151` mục 6 / `report/136` / `report/140`. Chạy lại phải ra ĐÚNG các số này;
# lệch quá nửa bước (0,0224 pp trên n=4.463) là có gì đó đã đổi — dừng, đừng ghi đè kết quả.
NIEM = {("GRPO-point/101", "vor"): 60.07, ("GRPO-point/101", "d3"): 67.04,
        ("GRPO-point/101", "d3_gate"): 62.96, ("GRPO-point/101", "d14_truc"): 69.37,
        ("GRPO-point/101", "aitw"): 68.90, ("GRPO-point/101", "disk_thuan"): 69.89,
        ("MIN-DESC/101", "vor"): 60.05, ("MIN-DESC/101", "d3"): 66.55,
        ("MIN-DESC/101", "aitw"): 68.32, ("Câu người (trần)", "vor"): 75.73,
        ("Câu người (trần)", "d3"): 83.82, ("Câu người (trần)", "aitw"): 84.09,
        ("S1/101", "vor"): 59.11, ("gui_sel/101", "aitw"): 63.52,
        ("Base", "vor"): 47.59, ("Base", "aitw"): 55.28,
        # hàng "chữ nhật .14 (gated)" của `report/136` = cột d14_truc ở đây
        ("Câu người (trần)", "d14_truc"): 84.23, ("MIN-DESC/101", "d14_truc"): 68.72,
        ("S1/101", "d14_truc"): 67.24, ("gui_sel/101", "d14_truc"): 63.86,
        ("Base", "d14_truc"): 55.86,
        # `report/140`: thứ tự tám nhánh không đổi, và S1−Base giữ 11,89 dưới D.3
        ("S2/101", "vor"): 57.18, ("CE2-S2/101", "vor"): 59.42, ("S1/202", "vor"): 59.62,
        ("gui_sel/101", "vor"): 56.13, ("S1/101", "d3"): 65.49, ("Base", "d3"): 53.60}


def main():
    out = {"n4463": {}, "lat800": {}}
    H = f"{'nhánh':26s} {'n':>5s} {'Voronoi':>8s} {'D.3':>7s} {'D.3∧14%':>8s} {'-cont':>7s} " \
        f"{'±14%truc':>9s} {'AitW':>7s} {'disk':>7s}"
    dong = lambda t, n, v: (f"{t:26s} {n:5d} {v['vor']:8.2f} {v['d3']:7.2f} {v['d3_gate']:8.2f} "
                            f"{v['d3_nocont']:7.2f} {v['d14_truc']:9.2f} {v['aitw']:7.2f} "
                            f"{v['disk_thuan']:7.2f}")
    print(H)
    for ten, tep in NHANH:
        if not os.path.exists(os.path.join(RUNS, tep)):
            print(f"{ten:26s}  (thiếu {tep})"); continue
        v, n = bang(tep); out["n4463"][ten] = v
        print(dong(ten, n, v))

    f1 = nap(os.path.join(RUNS, SAN[0][1])); K800 = sorted(f1)
    print(f"\nLát 800 của bộ sàn (n={len(K800)}):")
    print(H)
    v, n = bang(NHANH[0][1], K800); out["lat800"]["trần"] = v
    print(dong("trần (câu người)", n, v))
    for ten, tep in SAN:
        v, n = bang(tep, K800); out["lat800"][ten] = v
        print(dong(ten, n, v))
    tr, s1 = out["lat800"]["trần"], out["lat800"]["f1 câu rỗng nghĩa"]
    print("dải dùng được (trần − f1): " + " · ".join(f"{c} {tr[c]-s1[c]:.2f}" for c in COT))

    # ── tự kiểm: mọi số đã niêm phải ra đúng ────────────────────────────────────
    xau = [(k, c, m, out["n4463"][k][c]) for (k, c), m in sorted(NIEM.items())
           if k in out["n4463"] and abs(out["n4463"][k][c] - m) > 0.0112]
    if xau:
        for k, c, m, g in xau:
            print(f"  ⛔ {k} · {c}: niêm {m:.2f} nhưng tính ra {g:.2f}")
        raise SystemExit("DỪNG: số đã niêm không tái lập — đừng ghi đè runs/luat_d3.json")
    print(f"✅ tự kiểm: {len(NIEM)} số đã niêm đều tái lập (sai lệch < nửa bước)")

    p = os.path.join(RUNS, "luat_d3.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", p)


if __name__ == "__main__":
    main()
