# -*- coding: utf-8 -*-
"""T2: ck500/202 (hạt GRPO thứ hai) dưới UI-Venus và Phi-4, so S1/101, S1/202, ck500 (0 GPU). Chạy: python3 -I harness/t2_ck202_doc.py
Kết quả Kaggle đặt ở runs/venus/ck202_7_11/out/score_m1_raw.jsonl (kernel trangphngngc/venus-ck202)
và runs/som/chon_phi4_ck202_diff.jsonl (kernel uyenle0712/som-ck202).
ck202 chỉ được chấm ở bước có câu chưa từng chấm; bước câu trùng một nhánh đã chấm thì dùng lại kết quả đó.
Câu rỗng tính 0. Δ ghép cặp + KTC95 bootstrap cụm app + McNemar chính xác (như venus_s1_202_doc.py, som_s1_202_doc.py)."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import score_run as S
R = os.path.join(HERE, "..", "runs")
key = lambda o: (str(o["episode_id"]), str(o["step_id"]))
def L(p): return {key(o): o for o in map(json.loads, open(os.path.join(R, p), encoding="utf-8"))}
F = {"s1_101": "score_s1_seed101_raw.jsonl", "s1_202": "score_s1_seed202_raw.jsonl",
     "ck500": "grpo_spice/score_ck500_test_raw.jsonl", "r3": "ra304_luat/score_R3_test_raw.jsonl",
     "ck202": "grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl"}
Z = {n: L(p) for n, p in F.items()}
K = sorted(Z["s1_101"]); assert all(set(v) == set(K) for v in Z.values())
sent = lambda n, k: (Z[n][k].get("sent") or "").strip()
APP = {k: (Z["s1_101"][k].get("app") or f"ep{k[0]}") for k in K}


def so(res, a, b):
    d = {k: res[a][k] - res[b][k] for k in K}
    pt, (lo, hi), G, _ = S.cluster_bootstrap(list(d.items()), lambda u: APP[u[0]], lambda u: u[1])
    x = sum(v > 0 for v in d.values()); y = sum(v < 0 for v in d.values()); n = x + y
    p = min(1, 2 * sum(math.comb(n, i) for i in range(min(x, y) + 1)) / 2 ** n) if n else 1
    print(f"  {a:7s}-{b:7s} Δ={100*pt:+.2f} [{100*lo:+.2f}; {100*hi:+.2f}] b={x} c={y} p={p:.3g}")


def bang(ten, res):
    print(f"\n== {ten}")
    for n in res: print(f"  {n:7s} = {100*sum(res[n].values())/len(K):.2f}")
    for a, b in (("ck202", "s1_101"), ("ck202", "s1_202"), ("ck202", "ck500"), ("ck500", "s1_101")): so(res, a, b)


# UI-Venus: tra theo (bước, câu) trên mọi lượt Venus đã có
V = {}
for p in ["venus/score_venus_s1_2532_raw.jsonl"] + [f"venus/ck500_r3_22_10/score_{n}_raw.jsonl" for n in ("s1", "ck500", "r3")] + \
         ["venus/bu_22_10/score_m1_raw.jsonl", "venus/s1_202_23_10/out/score_m1_raw.jsonl", "venus/ck202_7_11/out/score_m1_raw.jsonl"]:
    if not os.path.exists(os.path.join(R, p)):
        print("chưa có", p); continue
    for k, o in L(p).items():
        if "sent" in o: V[(k, o["sent"].strip())] = int(o["executable"])
res, thieu = {n: {} for n in Z}, 0
for k in K:
    for n in Z:
        s = sent(n, k)
        if not s: res[n][k] = 0
        elif (k, s) in V: res[n][k] = V[(k, s)]
        else: thieu += 1; res[n][k] = 0
if thieu: print(f"⛔ Venus thiếu {thieu} lượt chấm, chưa đọc được")
else: bang("UI-Venus-Ground-7B exec", res)

# Phi-4: kết quả theo bước của từng nhánh; ck202 lấy từ tệp diff, bước trùng câu nhánh khác thì dùng lại
ph = {"s1_101": "som/chon_phi4_s1_101.jsonl", "ck500": "som/chon_phi4_ck500.jsonl", "r3": "som/chon_phi4_r3.jsonl",
      "s1_202": "som/chon_phi4_s1_202_diff.jsonl", "ck202": "som/chon_phi4_ck202_diff.jsonl"}
if not os.path.exists(os.path.join(R, ph["ck202"])):
    print("chưa có", ph["ck202"]); sys.exit()
P = {n: L(p) for n, p in ph.items()}
res = {n: {} for n in Z}
for k in K:
    for n in ("s1_101", "ck500", "r3"): res[n][k] = int(P[n][k]["dung"])
    s2 = sent("s1_202", k)
    res["s1_202"][k] = 0 if not s2 else (res["s1_101"][k] if s2 == sent("s1_101", k) else int(P["s1_202"][k]["dung"]))
    c = sent("ck202", k)
    if not c: res["ck202"][k] = 0
    else:
        same = [n for n in ("s1_101", "ck500", "r3", "s1_202") if sent(n, k) == c]
        res["ck202"][k] = res[same[0]][k] if same else int(P["ck202"][k]["dung"])
bang("Phi-4 người nghe, chọn đúng", res)
