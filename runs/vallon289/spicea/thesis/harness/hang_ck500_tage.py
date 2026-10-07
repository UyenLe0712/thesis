# -*- coding: utf-8 -*-
"""Sáu cột vị trí cho hai nhánh mới của luận văn (GRPO thưởng SPICE ck500, TAGE) — 0 giây GPU.

    python3 harness/hang_ck500_tage.py     # ghi runs/hang_ck500_tage.json

Dùng đúng hàm của các bảng đã in: `luat_d3.luat` (exec · D.3 · ±14% trục), `luat_aitw_day_du.aitw_full`,
`luat_aitw_moi_hop.aitw_moi_hop`, và `action_ok` của tệp thô. TAGE = tệp thô ck500, thay 219 bước
cổng nhận bằng `runs/tage_test/score_pred_cong_raw.jsonl` (đúng cách `tage_test_doc.py` gộp).
Kiểm: ck500 phải ra lại 60,65 · 67,02 · 76,25 (report/259), TAGE ra 60,23 · 66,44 · 76,07 (report/269).
"""
import json, os
import luat_d3 as L
from luat_aitw_day_du import aitw_full
from luat_aitw_moi_hop import aitw_moi_hop

R = L.RUNS


def cot(rows):
    n = len(rows)
    s = dict(vor=0, d3=0, d14_truc=0, aitw_full=0, aitw_moi_khung=0, action_ok=0)
    for k, r in rows.items():
        v = L.luat(r, k)
        for c in ("vor", "d3", "d14_truc"):
            s[c] += v[c]
        s["aitw_full"] += aitw_full(r, k)
        s["aitw_moi_khung"] += aitw_moi_hop(r, k)
        s["action_ok"] += int(r["action_ok"])
    return {c: round(100 * x / n, 2) for c, x in s.items()} | {"n": n}


def main():
    ck = L.nap(os.path.join(R, "grpo_spice", "score_ck500_test_raw.jsonl"))
    tg = dict(ck)
    thay = L.nap(os.path.join(R, "tage_test", "score_pred_cong_raw.jsonl"))
    assert set(thay) <= set(ck) and len(thay) == 219
    tg.update(thay)
    out = {"ck500": cot(ck), "TAGE": cot(tg)}
    assert len(ck) == 4463 and len(tg) == 4463
    for ten, mong in (("ck500", (60.65, 67.02, 76.25)), ("TAGE", (60.23, 66.44, 76.07))):
        o = out[ten]
        got = (o["vor"], o["d3"], o["aitw_full"])
        assert all(abs(a - b) < 0.006 for a, b in zip(got, mong)), (ten, got, mong)
        print(ten, o)
    # tệp thô gộp của TAGE, cùng thứ tự với tệp của ck500, cho các script đọc tệp thô (text_metrics, KTC)
    thu_tu = [L.kh(json.loads(l)) for l in open(os.path.join(R, "grpo_spice", "score_ck500_test_raw.jsonl"), encoding="utf-8")]
    with open(os.path.join(R, "tage_test", "score_tage_gop_raw.jsonl"), "w", encoding="utf-8") as f:
        for k in thu_tu:
            f.write(json.dumps(tg[k], ensure_ascii=False) + "\n")
    p = os.path.join(R, "hang_ck500_tage.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", os.path.relpath(p))


if __name__ == "__main__":
    main()
