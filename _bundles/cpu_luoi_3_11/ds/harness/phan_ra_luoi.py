# -*- coding: utf-8 -*-
"""Phân rã Δexec so với S1/101 thành phần sửa loại thao tác và phần đổi phần tử, cho các lượt lưới RL (H-A, report/328) — 0 GPU.

Cùng định nghĩa grpo_spice_test_doc.py: cứu = S1 trượt, nhánh trúng; ròng loại thao tác = (cứu mà S1 sai loại) − (phá mà nhánh sai loại);
phần còn lại là đổi phần tử. Tự kiểm: ck500 phải ra +28 và +41 (report/259). Ghi runs/luoi/test_2_11/phan_ra.json.
"""
import json, os, sys
K = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "runs")
T = "luoi/test_2_11/score_%s_101_test_raw.jsonl"
N = {"ck500": "grpo_spice/score_ck500_test_raw.jsonl", "xao101": "xao101/test/score_ck500_xao101_test_raw.jsonl",
     "SCST + SPICE": T % "scst_spice", "GRPO + CIDEr-D": T % "grpo_cider", "GRPO + METEOR": T % "grpo_meteor", "GRPO + ROUGE-L": T % "grpo_rougel"}
nap = lambda f: {(x["episode_id"], x["step_id"]): x for x in map(json.loads, open(os.path.join(K, f), encoding="utf-8"))}
e = lambda r: int(bool(r.get("executable", 0)))
a = lambda r: int(bool(r.get("action_ok", 0)))
s1 = nap("score_s1_seed101_raw.jsonl")
out = {}
for t, f in N.items():
    X = nap(f); assert set(X) == set(s1), (t, len(X))
    cuu = [k for k in s1 if not e(s1[k]) and e(X[k])]; pha = [k for k in s1 if e(s1[k]) and not e(X[k])]
    ca = sum(not a(s1[k]) for k in cuu); pa = sum(not a(X[k]) for k in pha)
    ro_a, ro_d = ca - pa, (len(cuu) - ca) - (len(pha) - pa)
    c2 = [k for k in s1 if a(s1[k]) and a(X[k])]
    out[t] = dict(cuu=len(cuu), pha=len(pha), cuu_sua_loai=ca, pha_sai_loai=pa, rong_loai=ro_a, rong_phan_tu=ro_d,
                  rong_tong=ro_a + ro_d, n_ca_hai_dung_loai=len(c2), exec_s1_cung_dung=round(100 * sum(e(s1[k]) for k in c2) / len(c2), 2),
                  exec_nhanh_cung_dung=round(100 * sum(e(X[k]) for k in c2) / len(c2), 2))
    print(t, out[t], flush=True)
if (out["ck500"]["rong_loai"], out["ck500"]["rong_phan_tu"]) != (28, 41):
    sys.exit(f"⛔ DỪNG, không tái lập ck500 +28/+41: {out['ck500']}")
print("✅ tái lập ck500 +28/+41", flush=True)
json.dump(out, open(os.path.join(K, "luoi/test_2_11/phan_ra.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
