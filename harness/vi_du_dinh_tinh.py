# -*- coding: utf-8 -*-
"""Ví dụ định tính và phân rã cho S1/101 → ck500 → ACE (R3) — 0 GPU.

    python3 -I harness/vi_du_dinh_tinh.py      # ghi report/321_VI_DU_DINH_TINH_CK500_ACE.md

Mỗi bước lấy `executable` UGround từ tệp thô của từng nhánh. Ví dụ rút ngẫu nhiên (hạt 20261023), không chọn lọc.
"""
import json, os, random, collections
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
F = {"S1": "runs/score_s1_seed101_raw.jsonl", "ck500": "runs/grpo_spice/score_ck500_test_raw.jsonl",
     "ACE": "runs/ra304_luat/score_R3_test_raw.jsonl"}
D = {n: {(o["episode_id"], o["step_id"]): o for o in map(json.loads, open(os.path.join(R, p), encoding="utf-8"))} for n, p in F.items()}
K = sorted(D["S1"]); assert all(set(D[n]) == set(K) for n in D)
ex = lambda n, k: int(D[n][k]["executable"]); s = lambda n, k: (D[n][k].get("sent") or "").strip()
ao = lambda n, k: int(D[n][k]["action_ok"] and D[n][k]["toggle_ok"])
out = ["# 321 — Ví dụ định tính và phân rã S1/101 → ck500 → ACE (23/10/2026)", "",
       "Sinh bởi `harness/vi_du_dinh_tinh.py`. Số test, 4.463 bước chạm. Ví dụ rút ngẫu nhiên, không chọn lọc.", ""]

def phanra(a, b):
    doi = [k for k in K if s(a, k) != s(b, k)]
    cuu = [k for k in doi if not ex(a, k) and ex(b, k)]; pha = [k for k in doi if ex(a, k) and not ex(b, k)]
    cu_t = [k for k in cuu if not ao(a, k)]; pa_t = [k for k in pha if not ao(b, k)]
    out.append(f"## {b} so với {a}\n")
    out.append(f"- câu đổi: {len(doi)}/{len(K)} bước ({100*len(doi)/len(K):.1f}%)")
    out.append(f"- cứu {len(cuu)} (sửa loại thao tác {len(cu_t)}, còn lại đổi phần tử/vị trí {len(cuu)-len(cu_t)}) · phá {len(pha)} (do sai loại thao tác {len(pa_t)}, còn lại {len(pha)-len(pa_t)}) · ròng {len(cuu)-len(pha):+d}")
    for ten, cond in (("đã thấy app", True), ("app chưa thấy", False)):
        g = [k for k in doi if D[a][k].get("app_seen_in_train") is cond]
        if g: out.append(f"- {ten}: câu đổi {len(g)}, cứu {sum(k in set(cuu) for k in g)}, phá {sum(k in set(pha) for k in g)}")
    nd = collections.Counter(); 
    for k in doi:
        l = len(s(a, k).split()); nd["≤5 từ" if l <= 5 else "6–10 từ" if l <= 10 else ">10 từ"] += 1
    out.append("- độ dài câu cũ của các bước bị đổi: " + ", ".join(f"{k} {v}" for k, v in nd.items()) + "\n")
    rng = random.Random(20261023)
    for ten, L in (("cứu", cuu), ("phá", pha)):
        out.append(f"### Ví dụ {ten} ({b} so với {a})\n")
        for k in rng.sample(L, min(6, len(L))):
            out.append(f"- ep{k[0]} bước {k[1]} · app {D[a][k].get('app') or '(không rõ)'}\n  - chuẩn: {D[a][k].get('gold_instruction')}\n  - {a}: {s(a,k)}\n  - {b}: {s(b,k)}")
        out.append("")
phanra("S1", "ck500"); phanra("ck500", "ACE")
open(os.path.join(R, "report/321_VI_DU_DINH_TINH_CK500_ACE.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out[:16]))
