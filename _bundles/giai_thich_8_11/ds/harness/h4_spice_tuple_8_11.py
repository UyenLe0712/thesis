# -*- coding: utf-8 -*-
"""H4 (SPICE theo loại tuple) bản 8/11/2026: thêm lượt train lại ck500 (A/A) và ck500 hạt 202.
Dùng nguyên main() của h4_spice_tuple_7_11.py (tự kiểm Δtp 5 nhánh cũ giữ nguyên).

  python h4_spice_tuple_8_11.py --out ../runs/luoi/8_11/giai_thich/h4_spice_tuple_8_11.json [--n 100]
"""
import h4_spice_tuple_7_11 as H

H.NHANH += [("grpo_spice_aa", "runs/luoi/8_11/test_u_4/score_grpo_spice_aa_101_test_raw.jsonl"),
            ("ck500_s202", "runs/grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl")]

if __name__ == "__main__":
    H.main()
