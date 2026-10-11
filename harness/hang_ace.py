# -*- coding: utf-8 -*-
"""Các cột của bảng luận văn cho ACE (ck500 + RA-SFT, luật chọn R3 của report/304 §5) — 0 giây GPU.

    ~/.venvs/thesis/bin/python harness/hang_ace.py     # ghi runs/hang_ace.json

ACE = tệp thô ck500, thay các bước mà luật R3 lấy câu `ra_k4` (`runs/ra304_luat/score_R3_test_raw.jsonl`
đã gộp sẵn). Dùng đúng các hàm của `hang_ck500_tage.py` (vị trí) và `text_metrics.py` (BLEU-4 mức câu, ROUGE-L).
Kiểm: exec · D.3 · AitW phải ra 60,68 · 67,11 · 76,32 (report/304 §5.3).
"""
import json, os
import luat_d3 as L
from hang_ck500_tage import cot
import text_metrics as T

R = L.RUNS


def main():
    p = os.path.join(R, "ra304_luat", "score_R3_test_raw.jsonl")
    rows = L.nap(p)
    assert len(rows) == 4463
    out = cot(rows)
    got = (out["vor"], out["d3"], out["aitw_full"])
    assert all(abs(a - b) < 0.006 for a, b in zip(got, (60.68, 67.11, 76.32))), got
    hyp, ref, _ = T.load(os.path.relpath(p, T.ROOT))
    b, rl = T.metrics(hyp, ref)
    out |= {"bleu4": round(b, 2), "rougeL": round(rl, 2)}
    ck = os.path.join(R, "grpo_spice", "score_ck500_test_raw.jsonl")
    cau = lambda f: {(d["episode_id"], d["step_id"]): d.get("sent") or "" for d in map(json.loads, open(f, encoding="utf-8"))}
    a, b = cau(p), cau(ck)
    assert set(a) == set(b)
    out["cau_doi_so_ck500"] = sum(a[k] != b[k] for k in a)
    print(out)
    json.dump(out, open(os.path.join(R, "hang_ace.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
